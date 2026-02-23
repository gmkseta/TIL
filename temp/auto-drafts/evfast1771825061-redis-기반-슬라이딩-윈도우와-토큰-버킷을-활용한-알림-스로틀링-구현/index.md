---
title: "Redis 기반 슬라이딩 윈도우와 토큰 버킷을 활용한 알림 스로틀링 구현"
date: "2026-02-23"
update: "2026-02-23"
tags: ["auto-draft", "slack", "n8n"]
draft: true
---
# Redis 기반 슬라이딩 윈도우와 토큰 버킷을 활용한 알림 스로틀링 구현

## 문제 정의
마케팅 이벤트 급증이나 시스템 장애 복구 과정에서 특정 사용자에게 알림이 폭주하여 사용자 경험을 심각하게 저해합니다. 또한, 불필요한 메시지 발송으로 인해 메시징 비용(SMS, APNS 등)이 통제 불능 상태로 급증하는 문제가 발생합니다. 단순한 고정 제한(Fixed Limit)은 트래픽 패턴의 변화에 유연하게 대응하지 못해 서비스 전체의 안정성을 위협합니다.

## 왜 프로덕션에서 중요한가
마이크로서비스 환경에서는 여러 노드가 분산되어 있어, 로컬 메모리 기반의 속도 제어는 정확성을 보장하기 어렵습니다. 특히 알림 시스템은 외부 API(SMS 게이트웨이, FCM)와 연동되므로, 속도 제어 실패는 즉각적인 과금 청구나 외부 서비스로부터의 차단(IP Ban)으로 이어집니다. Redis 7.0 이상의 기능을 활용하면 분산 환경에서도 정확한 제어가 가능하며, 비용 최적화와 서비스 안정성을 동시에 확보할 수 있습니다.

## 아키텍처 및 기술적 접근
분산 환경에서의 정확한 속도 제어를 위해 중앙 집중식 저장소인 Redis를 사용합니다. 네트워크 왕복(Round Trip)을 최소화하고 원자성(Atomicity)을 보장하기 위해 Redis Lua 스크립트를 활용합니다.

주요 알고리즘 비교:
1. **Sliding Window Log (슬라이딩 윈도우 로그)**: 요청의 타임스탬프를 모두 저장하여 매우 정밀한 제어가 가능하지만, 메모리 사용량이 트래픽에 비례하여 급증합니다.
2. **Token Bucket (토큰 버킷)**: 버킷에 토큰을 채워두고 소비하는 방식으로, 버스트(Burst) 트래픽을 흡수하는 데 유리하며 메모리 효율이 좋습니다.

알림 시스템의 특성상 순간적인 폭주를 막으면서도 일정량의 버스트를 허용해야 하므로, **Token Bucket** 방식이 주로 적합합니다. 하지만 "1분에 5회"와 같은 엄격한 정책이 필요한 경우 Sliding Window Log를 병행하여 사용할 수 있습니다.

## 코드 예제
다음은 Redis Lua 스크립트를 활용한 토큰 버킷 알고리즘의 구현 예제입니다. 이 스크립트는 `eval` 명령을 통해 원자적으로 실행됩니다.

**Lua Script (`token_bucket.lua`)**

```lua
-- KEYS[1]: Rate Limit Key (예: user:1234:notification)
-- ARGV[1]: capacity (버킷 용량, 최대 토큰 수)
-- ARGV[2]: rate (초당 리필되는 토큰 수, tokens per second)
-- ARGV[3]: now (현재 Unix 타임스탬프, 애플리케이션에서 전달)
-- ARGV[4]: requested (요청한 토큰 수, 보통 1)

local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])
local requested = tonumber(ARGV[4])

local current_info = redis.call('hmget', key, 'tokens', 'last_refill')
local current_tokens = tonumber(current_info[1])
local last_refill = tonumber(current_info[2])

-- 초기화
if current_tokens == nil then
    current_tokens = capacity
    last_refill = now
end

-- 경과 시간에 따른 토큰 리필 계산
local delta = math.max(0, now - last_refill)
local filled_tokens = math.min(capacity, current_tokens + (delta * rate))

-- 토큰 소비 가능 여부 확인
if filled_tokens >= requested then
    local new_tokens = filled_tokens - requested
    redis.call('hmset', key, 'tokens', new_tokens, 'last_refill', now)
    redis.call('expire', key, 600) -- 정리를 위해 TTL 설정 (예: 10분)
    return 1 -- 허용 (Allowed)
else
    -- 거부 시에는 상태 갱신 없이 TTL만 연장하여 불필요한 쓰기 최소화
    redis.call('expire', key, 600)
    return 0 -- 거부 (Denied)
end
```

**Node.js (ioredis) 호출 예제**

```javascript
const Redis = require('ioredis');
const redis = new Redis();
const fs = require('fs');

const luaScript = fs.readFileSync('./token_bucket.lua', 'utf8');

async function checkRateLimit(userId) {
    const key = `rate_limit:user:${userId}`;
    const capacity = 10;
    const rate = 0.1; // 초당 0.1개의 토큰 리필 (즉, 10초에 1개)
    const requested = 1;
    const now = Math.floor(Date.now() / 1000); // 애플리케이션 레벨에서 시간 전달

    const result = await redis.eval(
        luaScript,
        1, // KEYS count
        key, // KEYS[1]
        capacity, // ARGV[1]
        rate, // ARGV[2]
        now, // ARGV[3]
        requested // ARGV[4]
    );

    return result === 1;
}

// 사용
checkRateLimit(1234).then(allowed => {
    if (allowed) {
        console.log('알림 전송 허용');
    } else {
        console.log('알림 전송 거부 (Rate Limit 초과)');
    }
});
```

## 운영상 고려사항
1. **Redis 지연(Latency)**: 알림 전송 로직의 Critical Path에 Redis 조회가 포함되므로, Redis 응답 시간이 전체 지연에 직접적인 영향을 미칩니다. 반드시 P99 지연을 모니터링해야 합니다.
2. **SPOF (Single Point of Failure)**: Redis가 다운되면 모든 알림 전송이 중단되거나, Fail-open(모두 허용) 정책을 선택할 경우 비용 폭증 위험이 있습니다. 알림 시스템의 특성상 비용 폭증을 방지하기 위해 기본 전략은 **Fail-closed(모두 거부)**로 설정하여 장애 시 서비스를 보호해야 하며, 유실된 메시지는 Dead Letter Queue(DLQ) 등으로 우회하여 재시도 처리하는 절차가 마련되어야 합니다. Redis Cluster나 Sentinel 구성을 통해 고가용성을 확보해야 합니다.
3. **키 관리 전략**: 사용자 ID, 알림 타입(마케팅, 시스템 등)을 조합하여 키를 구성해야 합니다. 예: `throttle:user:{id}:type:marketing`. TTL을 적절히 설정하여 Redis 메모리 누수를 방지해야 합니다.
4. **모니터링 및 알림**: 특정 사용자가 제한에 자주 걸리는지, 혹은 전체 트래픽이 제한에 막혀 누적되고 있는지(Drop rate) 모니터링 대시보드를 구축해야 합니다.

## 트레이드오프 및 제한사항
- **정확도 vs 성능**: Sliding Window Log는 매우 정확하지만 O(N)의 메모리를 사용하므로 대규모 트래픽에서는 비효율적입니다. Token Bucket은 메모리 효율이 좋지만 짧은 시간 내의 연속 요청을 완벽하게 차단하지 못할 수 있습니다.
- **네트워크 의존성**: 분산 환경에서는 네트워크 지연이나 분단(Partition) 상황에서 제어 로직이 느려지거나 실패할 수 있습니다. 로컬 캐시와 함께 사용하여 최악의 경우에도 방어막이 되도록 구성하는 것을 고려해야 합니다.
- **클럭 동기화**: Redis 서버와 애플리케이션 서버 간의 시간 차이가 클 경우 토큰 리필 시점에 오차가 발생할 수 있습니다. 이를 방지하기 위해 Lua 스크립트 내부에서 `redis.call('time')`을 사용하는 대신, 애플리케이션 레벨에서 타임스탬프를 인자로 전달하여 레플리카 환경에서의 쓰기 작업 차단 문제를 회피해야 합니다.

## 최종 체크리스트
- [ ] Redis Lua 스크립트를 사용하여 Rate Limit 로직의 원자성을 보장했는가?
- [ ] 알림 타입별로 독립적인 정책(예: 마케팅은 엄격, 시스템 알림은 관대)을 적용할 수 있는가?
- [ ] Redis 장애 시 기본 전략을 Fail-closed로 설정하고, 재시도를 위한 Dead Letter Queue(DLQ) 등으로 메시지를 우회시키는 절차가 수립되어 있는가?
- [ ] 현재 설정된 Limit이 실제 비용 절감과 사용자 경험 개선에 기여하는지 데이터로 검증되었는가?
- [ ] Redis 메모리 사용량이 키의 TTL 설정에 의해 안정적으로 유지되고 있는가?
