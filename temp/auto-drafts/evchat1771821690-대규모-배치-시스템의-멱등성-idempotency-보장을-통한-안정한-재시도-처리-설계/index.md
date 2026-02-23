---
title: "대규모 배치 시스템의 멱등성(Idempotency) 보장을 통한 안정한 재시도 처리 설계"
date: "2026-02-23"
update: "2026-02-23"
tags: ["auto-draft", "slack", "n8n"]
draft: true
---
# 대규모 배치 시스템의 멱등성(Idempotency) 보장을 통한 안정한 재시도 처리 설계

## Problem Definition
배치 작업 중 네트워크 오류나 타임아웃 등의 일시적인 장애가 발생했을 때, 단순히 작업을 재시도하면 이미 처리된 레코드가 다시 처리되어 데이터 중복이 발생합니다. 특히 결제, 정산, 재고와 같이 데이터 정합성이 생명인 백오피스 시스템에서는 이러한 중복 처리가 치명적인 비즈니스 오류로 이어집니다. 장애 복구를 위해 운영자가 수동으로 중복 데이터를 제거하거나 복잡한 SQL을 실행해야 하는 상황은 운영 부채를 증가시킵니다.

## Why This Matters in Production
마이크로서비스 아키텍처로 전환되면서 배치 간의 의존성이 복잡해지고, 데이터 파이프라인의 처리량이 기하급수적으로 증가하고 있습니다. 이 환경에서 배치 실패는 단순한 작업 중단을 넘어 연쇄적인 데이터 파손을 유발할 수 있습니다. 멱등성이 보장되지 않은 배치는 "실패 시 재시도"라는 가장 기본적인 복구 전략조차 사용할 수 없게 만들어, 시스템의 회복 탄력성(Resiliency)을 극도로 낮춥니다. 안정적인 재시도를 통해 SLA를 준수하고 운영 개입을 최소화하는 것은 필수적입니다.

## Architecture / Technical Approach
멱등성을 보장하기 위해서는 시스템이 "이미 처리된 요청"인지 식별할 수 있는 고유한 메커니즘이 필요합니다. 크게 **Unique Key 전략**과 **상태 저장소(State Store) 활용** 두 가지 방식으로 접근합니다.

1.  **Unique Key 전략 (DB 레벨 제약):**
    비즈니스 로직의 결과물을 저장하는 테이블에 유니크 제약조건(Unique Constraint)을 걸고, `INSERT IGNORE`나 `ON DUPLICATE KEY UPDATE` 구문을 사용합니다. 이 방식은 데이터베이스 자체의 무결성을 의존하므로 가장 안전하지만, 비즈니스 키가 복합적일 경우 인덱스 설계가 까다로울 수 있습니다. 또한, 쿼리 실행 후 반환되는 결과(Affected Rows 등)를 통해 실제 생성된 건인지, 중복으로 인해 스킵된 건인지 애플리케이션 레벨에서 명확히 구분하는 로직이 필요합니다.

2.  **상태 저장소 활용 (Deduplication Store):**
    Redis나 DynamoDB와 같은 고속 저장소에 배치 실행 ID와 처리 대상 ID를 조합한 키(Key)를 저장하여 처리 여부를 판단합니다. 배치 실행 전 해당 키의 존재 여부를 확인하고, 없을 때만 로직을 수행한 뒤 키를 저장합니다. 이는 기존 스키마 변경 없이 적용하기 쉽지만, 별도의 저장소 관리 비용이 발생합니다. 대규모 배치 환경에서는 네트워크 왕복(RTT)으로 인한 레이턴시를 줄이기 위해 Redis Pipeline이나 `MGET`/`MSET` 같은 배치 연산을 사용하는 것이 권장됩니다.

3.  **Exactly-Once 시맨틱 구현:**
    메시지 큐(Kafka 등)를 사용하는 경우, 단순히 Consumer Offset Commit과 비즈니스 로직 처리를 순차적으로 실행하는 것으로는 원자성을 보장할 수 없습니다. Kafka Transactions API를 사용하거나 Idempotent Producer/Consumer 설정을 통해 메시지 유실 없이 정확히 한 번만 처리되도록 설계해야 합니다.

## Code Example
다음은 상태 저장소(Redis)를 활용하여 배치 처리의 멱등성을 보장하는 예제입니다. 예외 발생 시 키를 삭제하여 재시도 기회를 제공하는 대신, 실패 상태를 유지하여 중복 처리를 방지하고 DLQ로 전송하는 방식을 채택했습니다.

```python
import redis

class IdempotentBatchProcessor:
    def __init__(self, redis_client):
        self.redis = redis_client

    def process_record(self, batch_id, record_id, business_logic):
        # 멱등성 키 생성: 배치ID + 레코드ID
        dedupe_key = f"batch:{batch_id}:record:{record_id}"
        
        # 이미 처리된 작업인지 확인 (SETNX: Set if Not eXists)
        # nx=True는 키가 존재하지 않을 때만 설정함을 의미합니다.
        is_already_processed = self.redis.set(dedupe_key, "1", nx=True, ex=86400)
        
        if not is_already_processed:
            print(f"Record {record_id} already processed in batch {batch_id}. Skipping.")
            return

        try:
            # 실제 비즈니스 로직 수행
            business_logic(record_id)
            
            # 성공 시 로깅 등 추가 작업
            print(f"Record {record_id} processed successfully.")
            
        except Exception as e:
            # 실패 시 키를 삭제하지 않음 (멱등성 보장)
            # 비즈니스 로직 수행 중 실패했거나 DB 커밋 후 Redis 저장 실패 등의
            # 부분 실패 상황에서 재시도 시 중복 처리를 방지하기 위함입니다.
            # 대신 Dead Letter Queue(DLQ) 등으로 이동시켜 수동 개입이 필요함을 알립니다.
            print(f"Failed to process record {record_id}: {e}")
            # 실제 구현에서는 여기서 DLQ에 레코드를 적재하고 예외를 처리해야 합니다.
            raise

# 사용 예시
def update_user_balance(record_id):
    # DB 업데이트 로직
    pass

redis_cli = redis.StrictRedis(host='localhost', port=6379, db=0)
processor = IdempotentBatchProcessor(redis_cli)

# 배치 실행 시 루프 내에서 호출
processor.process_record("batch_20231027", "user_123", update_user_balance)
```

## Operational Considerations
운영 환경에서는 멱등성 키의 수명(TTL) 관리가 중요합니다. 무한정 키를 쌓아두면 저장소 메모리를 고갈시킬 수 있으므로, 배치 주기나 데이터 보관 정책에 맞춰 적절한 TTL을 설정해야 합니다. 또한, 재시도 로직에서 "최대 재시도 횟수"를 초과했을 때의 폴백(Fallback) 전략이 필요합니다. 예를 들어, Dead Letter Queue(DLQ)로 실패 레코드를 이동시키고 알림을 발송하여 수동 개입이 필요하다는 것을 명확히 해야 합니다. 모니터링 대시보드에서는 `Processed vs Skipped(중복)` 비율을 확인하여 장애 상황을 직관적으로 파악할 수 있어야 합니다.

## Trade-offs & Limitations
멱등성을 위한 유니크 키 생성 로직 자체가 성능 병목이 될 수 있습니다. 특히 분산 환경에서는 락(Lock) 획득이나 원격 저장소 조회로 인해 레이턴시가 증가할 수 있습니다. 상태 저장소를 사용하는 대규모 배치에서는 단건 조회 대신 배치 연산(Pipeline 등)을 활용하여 성능 저하를 방지해야 합니다. 기존 레거시 시스템의 경우, 이미 존재하는 테이블에 유니크 제약조건을 추가하는 것이 불가능하여 대대적인 리팩토링이나 스키마 변경이 필요할 수 있습니다. 또한, 멱등성은 "같은 요청을 여러 번 보내도 결과가 같다"는 것을 보장하지만, "처음 실패한 요청을 성공시켜주는 것"까지 보장하지는 않으므로, 재시도 가능한 예외와 그렇지 않은 예외를 명확히 구분해야 합니다.

## Final Checklist
- [ ] 모든 배치 작업에 고유한 `Batch Execution ID`가 부여되는가?
- [ ] 처리 대상 데이터를 식별할 수 있는 `Unique Key` 전략이 수립되었는가?
- [ ] 멱등성 체크 로직이 비즈니스 로직 수행 **이전**에 이루어지는가?
- [ ] 상태 저장소(Redis 등)를 사용할 경우 장애 발생 시 데이터 유실 가능성에 대비했는가?
- [ ] 예외 발생 시 키 삭제로 인한 멱등성 파괴(Race Condition)를 방지하기 위해 실패 상태를 유지하거나 DLQ로 전송하는가?
- [ ] 대규모 배치 처리 시 Redis Pipeline이나 MGET/MSET 등을 사용하여 레이턴시를 최적화하는가?
- [ ] DB 레벨 제약조건 사용 시 `Affected Rows` 등을 통해 실제 생성/수정 건과 중복 스킵 건을 구분하는 로직이 있는가?
- [ ] 멱등성 키의 TTL(Time To Live)이 운영 정책에 맞게 설정되었는가?
- [ ] 재시도 한도 초과 시 레코드를 격리하고 알림을 보내는 DLQ 메커니즘이 있는가?
