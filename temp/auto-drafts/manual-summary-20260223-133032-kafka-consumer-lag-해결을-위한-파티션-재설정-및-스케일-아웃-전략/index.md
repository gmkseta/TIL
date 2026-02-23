---
title: "Kafka Consumer Lag 해결을 위한 파티션 재설정 및 스케일 아웃 전략"
date: "2026-02-23"
update: "2026-02-23"
tags: ["auto-draft", "slack", "n8n"]
draft: true
---
# Kafka Consumer Lag 해결을 위한 파티션 재설정 및 스케일 아웃 전략

## Problem Definition
데이터 처리량이 급증하여 특정 파티션에 Consumer Lag이 누적되고, 기존 컨슈머 인스턴스 추가만으로는 병목이 해결되지 않는 상황에 직면했습니다. 단일 파티션의 처리량 한계를 초과하는 트래픽이 몰리면, 컨슈머 그룹 내 다른 인스턴스가 유휴 상태여도 전체 처리 속도는 가장 느린 파티션에 종속됩니다. 이는 메시지 지연을 가속화하고 SLA 위배로 이어집니다.

## Why This Matters in Production
마이크로서비스 아키텍처에서 이벤트 기반 처리가 보편화되면서, 트래픽 스파이크 시 메시지 지연이 곧장 장애로 이어지는 사례가 증가하고 있습니다. 특히 이벤트 소싱(Event Sourcing)이나 CQRS 패턴을 사용할 경우, 컨슈머 랙은 데이터 일관성을 깨뜨리고 사용자 경험을 저하시키는 주요 원인이 됩니다. 단순히 컨슈머를 늘리는 것만으로는 파티션 수의 물리적 한계를 극복할 수 없으므로, 파티션 재설정 전략은 필수적입니다.

## Architecture / Technical Approach

컨슈머 랙을 해결하기 위해서는 파티션 수와 컨슈머 수의 관계를 이해하고 이를 동적으로 조정하는 아키텍처가 필요합니다.

1.  **파티션과 컨슈머의 1:1 매핑 원칙**
    Kafka 컨슈머 그룹 내에서 하나의 파티션은 하나의 컨슈머 스레드에만 할당됩니다. 따라서 파티션 수가 컨슈머 수보다 적으면 일부 컨슈머는 일을 하지 못합니다. 처리량을 선형으로 늘리려면 파티션 수를 늘려야 합니다.

2.  **스케일 아웃 절차 (Scale-out Procedure)**
    *   **파티션 증설:** `kafka-topics.sh` 등을 사용하여 토픽의 파티션 수를 늘립니다. (ASSUMPTION: 브로커 버전이 파티션 증설을 지원한다고 가정)
    *   **컨슈머 인스턴스 추가:** 애플리케이션(컨슈머)의 인스턴스 수를 늘립니다.
    *   **리밸런싱(Rebalancing):** Kafka Group Coordinator가 새로운 파티션과 컨슈머를 매핑합니다.

3.  **안정적인 리밸런싱을 위한 전략**
    *   **Cooperative Rebalance (Incremental):** `Eager` 리밸런스는 모든 컨슈머가 멈추고 할당을 다시 받지만, `Cooperative` 방식은 일부 컨슈머만 할당을 조정하여 전체 파이프라인의 중단 시간을 최소화합니다.
    *   **Sticky Partitioning:** 리밸런스 시 가능한 한 기존 파티션 할당을 유지하여, 캐시 워밍업이나 로컬 상태 복구 비용을 줄입니다.

## Code Example

Spring Kafka를 사용하여 `CooperativeStickyAssignor`를 설정하고, 안정적인 롤링 재시작을 유도하는 설정 예제입니다.

**Configuration (Java)**

```java
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.RoundRobinAssignor;
import org.apache.kafka.clients.consumer.CooperativeStickyAssignor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.annotation.EnableKafka;
import org.springframework.kafka.core.ConsumerFactory;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import java.util.HashMap;
import java.util.Map;

@Configuration
@EnableKafka
public class KafkaConsumerConfig {

    @Bean
    public ConsumerFactory<String, String> consumerFactory() {
        Map<String, Object> props = new HashMap<>();
        
        // 기본 설정
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka-broker:9092");
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "order-processing-group");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
        
        // 리밸런스 전략 설정 (Cooperative Sticky)
        props.put(ConsumerConfig.PARTITION_ASSIGNMENT_STRATEGY_CONFIG, 
                  CooperativeStickyAssignor.class.getName());

        // 롤링 재시작 및 안정성을 위한 타임아웃 설정
        // 세션 타임아웃을 넉넉하게 잡아 불필요한 리밸런스 방지
        props.put(ConsumerConfig.SESSION_TIMEOUT_MS_CONFIG, "30000"); 
        props.put(ConsumerConfig.HEARTBEAT_INTERVAL_MS_CONFIG, "10000");
        // 처리 시간이 길어질 경우를 대비한 Max Poll Interval
        props.put(ConsumerConfig.MAX_POLL_INTERVAL_MS_CONFIG, "300000");

        return new DefaultKafkaConsumerFactory<>(props);
    }
}
```

**Rolling Restart 시나리오**
1.  새로운 파티션을 토픽에 추가 (`kafka-topics --alter ... --partitions 12`).
2.  배포 파이프라인을 통해 컨슈머 애플리케이션을 순차적으로 재시작합니다.
3.  첫 번째 인스턴스가 재시작되면 리밸런스가 발생하며, `CooperativeStickyAssignor`에 의해 새 파티션이 할당됩니다.
4.  이 과정을 반복하여 전체 클러스터가 새로운 파티션 할당을 완료할 때까지 서비스 중단 없이 전환합니다.

## Operational Considerations

*   **롤링 재시작(Rolling Restart) 필수:** 파티션 수가 변경된 후 컨슈머를 한 번에 재시작하면 "Stop-the-world"가 발생하여 메시지 처리가 완전히 중단됩니다. 반드시 인스턴스 단위로 순차적으로 재시작해야 합니다.
*   **모니터링:** Burrow나 Kafka Exporter 등을 사용하여 리밸런스 발생 횟수와 컨슈머 랙 추이를 실시간으로 감시해야 합니다.
*   **오프셋 커밋:** 리밸런스 도중 장애가 발생하면 중복 처리가 발생할 수 있습니다. `enable.auto.commit=false`로 설정하고 처리 완료 후 명시적으로 커밋하는 것이 안전합니다.

## Trade-offs & Limitations

*   **순서 보장(Ordering) 훼손:** 파티션 수를 늘리면 기존 키(Key) 해싱 로직에 따라 데이터가 다른 파티션으로 분산될 수 있습니다. 이로 인해 특정 키에 대한 순차적 처리 보장이 깨질 수 있습니다. ASSUMPTION: 메시지 키가 파티션 결정에 사용되는 경우.
*   **파티션 증가의 단방향성:** Kafka는 파티션 수를 늘리는 것은 지원하지만, 줄이는 것은 데이터 삭제 및 재배치가 필요하므로 운영상 매우 위험하고 권장되지 않습니다. 신중하게 결정해야 합니다.
*   **브로커 부하:** 파티션 수가 과도하게 많아지면(예: 수천 개), 브로커의 메모리 사용량과 파일 핸들 개수가 급증하여 오히려 클러스터 성능을 저하시킬 수 있습니다.

## Final Checklist

- [ ] 현재 파티션 수와 컨슈머 수의 비율을 확인했는가?
- [ ] 파티션 증설 시 메시지 키 순서 보장 요건에 영향이 없는지 검토했는가?
- [ ] `CooperativeStickyAssignor` 등 안정적인 할당 전략을 적용했는가?
- [ ] `session.timeout.ms`와 `max.poll.interval.ms`가 롤링 재시작 시간을 고려하여 설정되었는가?
- [ ] 배포 시 인스턴스 단위의 롤링 재시작 전략이 수립되어 있는가?
- [ ] 브로커의 리소스(CPU, Memory, File Handles)가 증가된 파티션 수를 감당할 수 있는가?
