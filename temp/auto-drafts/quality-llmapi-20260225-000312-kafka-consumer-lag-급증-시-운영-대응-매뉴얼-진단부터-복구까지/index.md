---
title: "Kafka Consumer Lag 급증 시 운영 대응 매뉴얼: 진단부터 복구까지"
date: "2026-02-24"
update: "2026-02-24"
tags: ["auto-draft", "slack", "n8n"]
draft: true
---
# Kafka Consumer Lag 급증 시 운영 대응 매뉴얼: 진단부터 복구까지

## 1. Problem Definition

프로덕션 환경에서 Kafka Consumer Lag가 예기치 않게 급증하여 데이터 처리 지연이 발생하고, SLA 위반 위기에 처한 상황입니다. 단순히 메시지가 쌓이는 것을 넘어, 타임아웃으로 인한 컨슈머 그룹 불안정성이나 다운스트림 서비스의 장애로 이어질 수 있는 복합적인 문제입니다. 근본 원인(네트워크, DB 병목, 로직 오류)을 명확히 파악하지 못한 상태에서의 무조건적인 재시작이나 증설은 상황을 악화시킬 수 있습니다. 본 문서는 장애 상황에서의 신속한 진단과 안정적인 복구 절차를 정리합니다.

## 2. Why This Matters in Production

이벤트 기반 아키텍처에서 Kafka는 데이터의 중추 역할을 수행하므로, Lag는 곧 시스템의 심각한 병목을 의미합니다. 실시간성이 요구되는 서비스(결제 알림, 추천 시스템 등)에서 Lag는 사용자 경험을 직접적으로 저해하며, 데이터 유실이나 순서 보장 실패로 이어질 수 있습니다. 특히, Kubernetes와 같은 동적 환경에서는 인스턴스의 불안정성이 Rebalancing을 유발하고, 이는 다시 Lag를 가중시키는 악순환을 만듭니다. 따라서 모니터링 관점에서의 즉각적인 탐지와 운영 관점에서의 체계적인 대응 역량이 필수적입니다.

## 3. Architecture / Technical Approach

운영 대응 아키텍처는 크게 **탐지(Detection)**, **진단(Diagnosis)**, **대응(Action)**의 3단계로 구성해야 합니다.

1.  **탐지**: 단순한 JMX 메트릭 수집을 넘어, Burrow와 같은 도구를 사용하여 Consumer Group의 상태(Stalled, Recovering 등)를 추론합니다. Prometheus를 통해 Lag가 임계치를 넘으면 Alertmanager가 즉시 알림을 발송합니다.
2.  **진단**: Lag 발생 시점의 시스템 메트릭(CPU, Memory, I/O Wait)과 로그를 상관 분석합니다. 특히 `max.poll.interval.ms` 초과 여부와 Rebalancing 빈도를 확인하여 병목이 '처리 속도' 문제인지 '그룹 불안정' 문제인지 판별합니다.
3.  **대응**:
    *   **Throttling**: 일시적으로 트래픽을 줄여 안정화를 도모합니다.
    *   **Scaling**: 파티션 수와 Consumer 수의 관계를 고려하여 수평 확장을 진행합니다.
    *   **Tuning**: `fetch.min.bytes`, `max.poll.records` 등의 파라미터를 조정하여 처리량을 최적화합니다.

## 4. Code Example

Lag 진단을 위한 스크립트와 Consumer 설정 예시입니다.

**Lag 확인 스크립트 (kafka-consumer-groups.sh 활용)**
```bash
#!/bin/bash
# Consumer Group의 상태와 Lag 확인

GROUP_ID="my-service-group"
BOOTSTRAP_SERVER="kafka-broker-1:9092"
# 보안 설정 파일 경로 (SASL/SSL 인증 정보 포함)
KAFKA_CONFIG="/path/to/kafka-client.properties"

# 현재 Lag 상태 출력
echo "Checking Lag for group: $GROUP_ID"
kafka-consumer-groups.sh --bootstrap-server $BOOTSTRAP_SERVER \
  --command-config $KAFKA_CONFIG \
  --group $GROUP_ID \
  --describe

# [주의] Offset 리셋은 데이터 유실 위험이 있으므로 신중해야 합니다.
# 아래 명령어는 파티션 전체의 메시지를 처음부터 다시 읽거나 특정 시점으로 되돌립니다.
# 운영 장애 시 복구 전략으로 사용하며, 실행 전 반드시 리더의 승인을 득하십시오.
# 안전을 위해 실행 전 확인 절차(Interactive prompt)를 거치도록 구성되어야 합니다.
#
# kafka-consumer-groups.sh --bootstrap-server $BOOTSTRAP_SERVER \
#   --command-config $KAFKA_CONFIG \
#   --group $GROUP_ID \
#   --topic target-topic \
#   --reset-offsets --to-earliest --execute
```

**Consumer 설정 튜닝 (Spring Kafka 예시)**
```properties
# 처리량 증대를 위한 설정
# max.poll.records 설정 시 평균 메시지 처리 시간(Latency)을 고려해야 합니다.
# 설정 공식: (평균 처리 시간 * 레코드 수) < max.poll.interval.ms
# 예: 평균 처리 시간이 100ms(0.1s)라면, 500개 * 0.1s = 50s 소요되므로
#     max.poll.interval.ms(300s) 내에 충분히 처리 가능합니다.
spring.kafka.consumer.max-poll-records=500
spring.kafka.consumer.fetch-max-bytes=5242880 # 5MB
spring.kafka.consumer.fetch-min-bytes=1024 # 1KB

# Rebalancing 방지를 위한 타임아웃 설정 (DB 쿼리 등 긴 작업 고려)
spring.kafka.listener.ack-mode=MANUAL_IMMEDIATE
spring.kafka.properties.max.poll.interval.ms=300000 # 5분 (배치 처리 시간 고려하여 상향 조정)
spring.kafka.properties.session.timeout.ms=30000
```

## 5. Operational Considerations

실제 운영 환경에서는 다음 사항을 고려해야 합니다.

*   **Rebalancing 폭탄**: Lag가 발생했다고 무작정 Consumer를 재시작하거나 Scale-out하면 Rebalancing이 발생하고, 그 동안 전체 처리가 멈추어 Lag이 폭증합니다. 반드시 전체 파티션의 처리가 중단되는 것을 방지하기 위해 파티션 소유권을 점진적으로 재할당하는 Cooperative Sticky Assignor(Incremental Cooperative Assignor) 사용을 고려해야 합니다.
*   **Dead Letter Queue(DLQ) 활성화**: 반복적으로 처리 실패하여 재시도 로직이 걸리는 메시지가 하나라도 있으면 전체 파티션의 처리가 멈출 수 있습니다. 예외 처리 로직을 통해 문제 메시지를 즉시 DLQ로 이관시켜 흐름을 유지해야 합니다.
*   **디스크 용량 확인**: Consumer가 처리를 못 하더라도 Producer는 계속 메시지를 쌓습니다. Broker의 디스크 용량이 가득 차면 클러스터 전체가 장애 상태가 되므로, Retention 정책을 동적으로 조절하거나 디스크 확보가 우선되어야 합니다.

## 6. Trade-offs & Limitations

*   **Scale-out의 한계**: Consumer의 수는 Topic의 파티션 수를 초과할 수 없습니다. 파티션이 3개인데 Consumer를 5개로 늘려도 2개는 유휴 상태가 되어 처리량이 늘어나지 않습니다. 파티션 증설은 리더 선출 및 데이터 재분배 오버헤드가 크므로, 설계 단계에서 충분히 할당해야 합니다.
*   **순서 보장(Ordering) vs 처리량**: 하나의 파티션 내 메시지 순서를 보장하기 위해선 단일 스레드로 처리해야 합니다. 순서가 중요하지 않은 데이터라면 파티션을 늘려 병렬 처리를 높이는 것이 유리하지만, 순서가 중요한 경우 처리량 향상에 명확한 한계가 있습니다.
*   **모니터링 지연**: JMX 메트릭 수집 주기나 Burrow의 계산 주기 때문에, 실제 Lag 발생과 알림 수신 사이에 필연적인 지연이 발생합니다. 이를 최소화하기 위해 너무 잦은 폴링은 Broker에 부하를 주므로 적절한 타협점이 필요합니다.

## 7. Final Checklist

- [ ] **Burrow/Prometheus 대시보드**에서 실시간 Lag 추적이 활성화되어 있는가?
- [ ] **Consumer Group**이 Rebalancing 상태에 빈번히 진입하지 않는지 확인했는가?
- [ ] **파티션 수** 대비 **Consumer 인스턴스 수**가 적절한가? (Consumer <= Partition)
- [ ] **DLQ(Dead Letter Queue)** 전략이 수립되어 있어, 실패 메시지가 파이프라인을 막지 않는가?
- [ ] 장애 복구 시 **Offset Reset** 전략(최신 vs 초기)이 명확히 정의되어 있는가?
- [ ] 급격한 Scale-out 시 **Cooperative Rebalancing**이 적용되어 전체 중지(Stop-the-world) 없이 점진적으로 파티션을 재할당하는가?
