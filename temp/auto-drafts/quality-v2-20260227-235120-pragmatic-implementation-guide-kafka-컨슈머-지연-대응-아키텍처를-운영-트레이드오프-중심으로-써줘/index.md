---
title: "Pragmatic implementation guide: Kafka 컨슈머 지연 대응 아키텍처를 운영/트레이드오프 중심으로 써줘"
date: "2026-02-27"
update: "2026-02-27"
tags: ["auto-draft", "slack", "n8n"]
draft: true
---
# Kafka 컨슈머 지연 대응 아키텍처 설계 및 운영 가이드

## 1. TL;DR
* 컨슈머 랙(Lag)은 단순히 스레드를 늘리는 것만으로 해결되지 않으며, 파티션 할당 전략과 I/O 병목 지점을 분석하여 접근해야 한다.
* 운영 환경에서는 `max.poll.records`와 `fetch.min.bytes`를 튜닝하여 처리량(Throughput)과 지연(Latency) 사이의 트레이드오프를 명확히 정의해야 한다.
* 장애 상황을 대비하여 재시도 정책과 데드 레터 큐(DLQ)를 분리하고, 랙 모니터링을 통해 선제적으로 스케일 아웃(Scale-out)을 트리거하는 자동화된 런북이 필수적이다.

## 2. Problem Definition
Kafka 컨슈머 랙이 누적되면 이벤트 처리 지연이 발생하여 비즈니스 로직의 타임라인이 무너진다. 단순히 컨슈머 인스턴스를 증설할 경우 파티션 개수 제약으로 인해 병렬 처리 효과가 없거나, DB 라이트백(Write-back) 지연으로 인해 오히려 랙이 가속화될 수 있다. ASSUMPTION: 현재 시스템은 프로듀서의 트래픽 폭주보다는 컨슈머의 처리 능력 부족이 주된 병목 원인으로 간주한다.

## 3. Production Context and Constraints
* **파티션 제약**: 운영 중인 클러스터의 파티션 개수를 변경하는 것은 리밸런싱 오버헤드가 크므로, 기존 파티션 수를 기준으로 컨슈머 수를 조정해야 한다.
* **순서 보장 (Ordering)**: 특정 키(Key)에 대한 이벤트 순서가 보장되어야 하므로, 임의의 파티션 할당보다는 스티키(Sticky) 할당을 유지해야 한다.
* **멱등성 (Idempotency)**: 재처리 시 데이터 중복을 방지하기 위해 DB 레벨의 멱등성 체크가 필수적이다.
* **리소스 한계**: 컨슈머 그룹의 오토스케일링은 비용 증가로 직결되므로, 인스턴스 수 상한선을 설정해야 한다.

## 4. Design Options and Trade-offs

| 옵션 | 설명 | 장점 | 단점 | 운영 영향 |
| :--- | :--- | :--- | :--- | :--- |
| **Scale-up (Vertical)** | 컨슈머 인스턴스의 사양(CPU/Memory) 증설 | 파티션 재분배 불필요, 구현 단순 | 비용 선형 증가, 단일 장애점(SPOF) 위험 | 하드웨어 교체 시 다운타임 필요 |
| **Scale-out (Horizontal)** | 컨슈머 인스턴스 수 증설 (파티션 수 ≤ 컨슈머 수) | 비용 효율적, 장애 격리 용이 | 파티션 수 제한, 리밸런싱 오버헤드 | 리밸런싱 시 일시적 랙 급증 가능 |
| **Batch Processing Tuning** | `max.poll.records` 증설 및 배치 크기 조정 | 네트워크 왕복(RTT) 감소, 처리량 증가 | 지연(Latency) 증가, 메모리 사용량 증가 | 튜닝 실패 시 OOM 위험 |
| **Async Processing** | 메시지 수신 후 비동기 워커에게 위임 | 컨슈머 랙 해소 빠름, 처리량 극대화 | 오프셋 커밋 관리 복잡, 순서 보장 어려움 | 메시지 유실 가능성 높음, 복잡도 증가 |

## 5. Chosen Architecture / Technical Approach
**동적 스케일링과 배치 튜닝을 결합한 하이브리드 아키텍처**를 채택한다.
기본적으로 파티션 수에 맞춰 컨슈머를 수평 확장(Scale-out)하되, 순간적인 트래픽 스파이크를 대비해 배치 크기를 동적으로 조정한다. 또한, 처리 실패 시 재시도 루프가 메인 파이프라인을 막지 않도록 **사이드카(Sidecar) 패턴 기반의 재시도 큐**와 **DLQ(Dead Letter Queue)**를 분리한다.

* **컨슈머 그룹**: 파티션 수와 동일한 수의 인스턴스를 유지하여 `Idle` 컨슈머를 최소화한다. 오토스케일링 시 파티션 수를 초과하여 인스턴스가 생성되는 것을 방지하기 위해 상한선을 파티션 개수로 설정하고, `CooperativeAssignor`를 사용하여 리밸런싱 폭주(Rebalance Storm)를 완화한다.
* **처리 로직**: DB 벌크 인서트(Bulk Insert)를 활용하여 I/O 병목을 줄인다.
* **오프셋 전략**: `enable.auto.commit=false`로 설정하여 메시지 처리 완료 후 명시적으로 커밋한다.

## 6. Implementation Details

### 6.1 배치 처리 및 폴백 전략
`max.poll.records`를 통해 한 번의 폴(Poll)로 가져올 최대 메시지 수를 제어한다. 너무 높게 설정하면 처리 시간이 `max.poll.interval.ms`를 초과하여 리밸런싱이 발생할 수 있다. 실패한 메시지는 즉시 재시도하지 않고 별도의 재시도 토픽(Retry Topic)으로 발행하여 메인 컨슈머의 속도를 저하시키지 않는다.

### 6.2 리밸런싱 최적화
`StickyAssignor`를 사용하여 리밸런싱 발생 시 가능한 기존 파티션 할당을 유지한다. 이는 캐시 워밍업 비용을 줄이고 랙 회복 시간을 단축한다.

### 6.3 병목 지점 분석
컨슈머 메트릭(`records-lag`, `fetch-latency-avg`)을 모니터링하여 병목이 네트워크인지(DB Fetch), 처리 로직인지(CPU) 판단한다. 네트워크 병목 시 `fetch.min.bytes`를 늘리고, 처리 로직 병목 시 스레드 풀 크기를 조정한다.

## 7. Code and Config Examples

### 7.1 Kafka Consumer Configuration (Java/Spring)
```java
Map<String, Object> props = new HashMap<>();
props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka-broker:9092");
props.put(ConsumerConfig.GROUP_ID_CONFIG, "order-processor-group");
props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false"); // 수동 커밋
props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "latest");
props.put(ConsumerConfig.MAX_POLL_RECORDS_CONFIG, 500); // 정수형으로 수정
props.put(ConsumerConfig.MAX_POLL_INTERVAL_MS_CONFIG, "300000"); // 5분
props.put(ConsumerConfig.FETCH_MIN_BYTES_CONFIG, "1024"); // 1KB
props.put(ConsumerConfig.FETCH_MAX_WAIT_MS_CONFIG, "500"); // 500ms 대기

// 보안 설정 (SASL/SSL 예시)
props.put(CommonClientConfigs.SECURITY_PROTOCOL_CONFIG, "SASL_SSL");
props.put(SaslConfigs.SASL_MECHANISM, "PLAIN");
props.put(SaslConfigs.SASL_JAAS_CONFIG, "org.apache.kafka.common.security.plain.PlainLoginModule required username=\"user\" password=\"password\";");
props.put(SslConfigs.SSL_TRUSTSTORE_LOCATION_CONFIG, "/path/to/truststore.jks");
props.put(SslConfigs.SSL_TRUSTSTORE_PASSWORD_CONFIG, "truststore-password");

// 리밸런싱 시 할당 전략
props.put(ConsumerConfig.PARTITION_ASSIGNMENT_STRATEGY_CONFIG, 
    StickyAssignor.class.getName());
```

### 7.2 Safe Commit Logic (Kotlin)
```kotlin
fun processMessages(consumer: KafkaConsumer<String, String>) {
    while (true) {
        val records = consumer.poll(Duration.ofMillis(1000))
        
        if (records.isEmpty) continue

        val offsetsToCommit = mutableMapOf<TopicPartition, OffsetAndMetadata>()
        val failedRecords = mutableListOf<ConsumerRecord<String, String>>()

        try {
            // 1. 레코드 처리 및 성공 분리
            for (record in records) {
                try {
                    // 개별 메시지 처리 (DB 저장 등)
                    repository.save(record.value())
                    
                    // 성공한 레코드만 오프셋에 추가
                    offsetsToCommit[TopicPartition(record.topic(), record.partition())] = 
                        OffsetAndMetadata(record.offset() + 1)
                } catch (e: Exception) {
                    logger.error("Record processing failed: offset=${record.offset()}", e)
                    failedRecords.add(record)
                }
            }

            // 2. 성공한 메시지에 대해서만 오프셋 커밋
            if (offsetsToCommit.isNotEmpty()) {
                consumer.commitSync(offsetsToCommit)
            }

            // 3. 실패한 메시지는 DLQ로 전송
            if (failedRecords.isNotEmpty()) {
                sendToDlq(failedRecords)
            }
            
        } catch (e: Exception) {
            logger.error("Critical error during batch processing", e)
            // 치명적인 오류 발생 시 커밋하지 않음 (재시도 유도)
        }
    }
}
```

### 7.3 Infrastructure Monitoring (Prometheus Query)
```promql
# 컨슈머 랙 모니터링 (sum by topic)
# ASSUMPTION: JMX Exporter 또는 Burrow를 통해 제공되는 메트릭 이름 사용
kafka_consumer_lag{group="order-processor-group"}

# 처리량 (records per second)
rate(kafka_consumer_records_consumed_total[1m])

# 평균 지연 시간
rate(kafka_consumer_fetch_latency_avg_sum[5m]) / rate(kafka_consumer_fetch_latency_avg_count[5m])
```

## 8. Verification and Metrics
* **컨슈머 랙 (Consumer Lag)**: 파티션별 랙이 지속적으로 증가하는지 확인 (ASSUMPTION: Prometheus Exporter를 통해 수집).
* **P95 처리 지연 (P95 Processing Latency)**: 메시지가 폴(Poll)된 시점부터 처리 완료까지의 시간.
* **처리량 (Throughput)**: 초당 처리하는 메시지 수(RPS). 스케일 아웃 시 선형적으로 증가하는지 검증.
* **리밸런싱 빈도**: 불필요한 리밸런싱이 발생하여 처리가 멈추는 구간이 없는지 확인.

## 9. Operational Runbook
1. **랙 감지 (Lag Detection)**: 랙이 10,000개를 초과하고 5분간 지속될 경우 경고 발생.
2. **원인 분석**:
   * `fetch-latency`가 높다면 네트워크 또는 브로커 부하 확인.
   * `records-lag`은 증가하나 `fetch-rate`가 정상이라면 컨슈머 처리 로직(CPU/DB) 병목 확인.
3. **대응 조치**:
   * **단계 1**: `max.poll.records`를 일시적으로 낮춰 처리 시간 단축 후 안정화 확인. (주의: 설정 변경 시 애플리케이션 재시작 필요)
   * **단계 2**: 컨슈머 인스턴스를 파티션 수까지만 늘려 스케일 아웃.
   * **단계 3**: DB 커넥션 풀 증설 및 인덱스 튜닝.
4. **복구 후**: 랙이 해소되면 증설된 리소스를 원복하여 비용 최적화.

## 10. Failure Scenarios and Rollback

### 시나리오 1: 리밸런싱 루프 (Rebalance Loop)
* **현상**: 세션 타임아웃(`session.timeout.ms`) 내에 처리가 완료되지 않아 컨슈머가 그룹에서 이탈하고 반복적으로 리밸런싱 발생.
* **원인**: GC(Garbage Collection) 장애 또는 DB 쿼리 응답 지연.
* **대응**: `max.poll.interval.ms`와 `session.timeout.ms`를 상향 조정. 처리 로직의 병목
