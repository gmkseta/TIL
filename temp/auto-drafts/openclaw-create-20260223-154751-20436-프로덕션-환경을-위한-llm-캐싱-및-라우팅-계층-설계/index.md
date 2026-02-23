---
title: "프로덕션 환경을 위한 LLM 캐싱 및 라우팅 계층 설계"
date: "2026-02-23"
update: "2026-02-23"
tags: ["auto-draft", "slack", "n8n"]
draft: true
---
# 프로덕션 환경을 위한 LLM 캐싱 및 라우팅 계층 설계

## Problem Definition
LLM API 호출은 타 서비스에 비해 단가가 높고 지연 시간이 길어, 트래픽이 증가하면 비용 폭발과 사용자 경험 저하로 직결됩니다. 단순한 키-값 저장소 캐싱만으로는 문맥이 포함된 질의(Query)의 중복 호출을 효율적으로 막을 수 없습니다. 또한, 모든 요청에 고성능 모델을 사용하는 것은 리소스 낭비이며, 실시간 성능 요구사항을 충족하기 어렵습니다. 따라서 비용과 성능의 균형을 맞추는 중간 계층의 설계가 필수적입니다.

## Why This Matters in Production
백엔드 시스템에서 LLM을 단순한 외부 API 호출로만 처리할 경우, 트래픽 스파이크 시 장애로 이어질 가능성이 매우 높습니다. 특히 토큰 기 과금 구조에서는 불필요한 중복 호출이 비용에 직접적인 타격을 줍니다. 안정적인 서비스를 위해서는 응답 시간을 줄이고 API 호출 비용을 획기적으로 절감할 수 있는 캐싱 전략과, 요청의 중요도에 따라 적절한 모델을 배분하는 라우팅 로직이 운영의 핵심이 됩니다.

## Architecture / Technical Approach

### 1. 의미론적 캐싱 (Semantic Caching)
정확히 일치하는 문자열 매칭이 아닌, 임베딩 벡터 간의 코사인 유사도(Cosine Similarity)를 기반으로 캐시를 적중시키는 방식입니다.
- **저장소**: Redis(Redis Stack) 또는 전용 Vector DB(Milvus, Pinecone 등)를 사용하여 임베딩 벡터와 메타데이터(토큰 수, 모델 버전, 타임스탬프)를 저장합니다.
- **흐름**: 사용자 요청 -> 임베딩 생성 -> Vector Search(유사도 검색) -> 임계값(Threshold) 이상이면 캐시 반환, 미만이면 LLM API 호출 후 결과 캐싱.

### 2. 모델 라우팅 (Model Routing)
요청의 복잡도나 긴급성에 따라 서로 다른 규모의 모델(Small/Medium/Large)로 요청을 분산합니다.
- **라우팅 로직**:
    - **Simple Task**: 요약, 간단한 분류 -> 소형 모델 (예: GPT-3.5-Turbo, Llama-3-8B)
    - **Complex Task**: 복잡한 추론, 코드 생성 -> 대형 모델 (예: GPT-4o, Claude-3.5-Sonnet)
- **폴백(Fallback) 메커니즘**: 소형 모델의 응답 품질이 신뢰 점수(Confidence Score) 미만일 경우 대형 모델로 자동 재시도합니다.

### 3. 계층 구조
`[Client] -> [Load Balancer] -> [API Gateway / Router Service] -> [Semantic Cache Layer] -> [LLM Provider]`

## Code Example

Python과 Redis(유사도 검색 기능 가정)를 활용한 의미론적 캐싱의 간단한 구현 예시입니다.

```python
import numpy as np
from typing import Optional, Tuple

# ASSUMPTION: redis_client는 이미 연결된 상태이며 HNSW 기능을 지원한다고 가정합니다.
# 실제 운영에서는 redis-py-cluster 또는 유사한 드라이버를 사용합니다.

SIMILARITY_THRESHOLD = 0.95  # 유사도 임계값 (0~1 사이)

class SemanticCache:
    def __init__(self, redis_client, embedding_model):
        self.redis = redis_client
        self.embedding_model = embedding_model

    def _get_embedding(self, text: str) -> list:
        # 실제 운영에서는 별도의 임베딩 서버를 호출하거나 로컬 모델을 사용합니다.
        return self.embedding_model.encode(text)

    def get(self, query: str) -> Optional[str]:
        query_vector = self._get_embedding(query)
        
        # Redis Vector Search 예시 (FT.SEARCH)
        # 실제 쿼리 문법은 사용하는 Redis 버전과 모듈에 따라 다릅니다.
        try:
            results = self.redis.ft("idx:llm_cache").search(
                query=f"*=>[KNN 5 @embedding $vec AS score]",
                query_params={"vec": np.array(query_vector).astype(np.float32).tobytes()}
            )
            
            if results.total == 0:
                return None

            # 가장 유사한 결과 확인
            first_doc = results.docs[0]
            score = 1 - float(first_doc['score']) # 거리를 유사도로 변환 (ASSUMPTION)

            if score >= SIMILARITY_THRESHOLD:
                return first_doc['response']
            
        except Exception as e:
            # 캐시 장애 시 LLM 호출로 우회하여 서비스 중단 방지
            print(f"Cache lookup failed: {e}")
            
        return None

    def set(self, query: str, response: str, ttl: int = 3600):
        query_vector = self._get_embedding(query)
        key = f"llm_cache:{hash(query)}"
        
        # 파이프라인을 사용하여 원자성 확보
        pipe = self.redis.pipeline()
        pipe.hset(key, mapping={
            "embedding": np.array(query_vector).astype(np.float32).tobytes(),
            "response": response,
            "timestamp": str(time.time())
        })
        pipe.expire(key, ttl)
        pipe.execute()

# 사용 예시
# cache = SemanticCache(redis_client, embedding_model)
# cached_response = cache.get("서울의 날씨 어때?")
# if cached_response:
#     return cached_response
# else:
#     llm_response = call_llm_api("서울의 날씨 어때?")
#     cache.set("서울의 날씨 어때?", llm_response)
#     return llm_response
```

## Operational Considerations

1. **임베딩 생성 비용**: 캐시 적중 여부를 판단하기 위해 매 요청마다 임베딩을 생성해야 하므로, 이에 대한 비용과 지연 시간이 추가로 발생합니다. 임베딩 모델은 LLM 본체보다 가볍고 빨라야 합니다.
2. **캐시 스토리지 관리**: 벡터 데이터는 일반 텍스트 로그보다 훨씬 큽니다. Redis 메모리나 Vector DB 스토리지가 가득 차지 않도록 LRU(Least Recently Used) 정책이나 TTL(Time To Live)을 엄격하게 관리해야 합니다.
3. **PII(개인정보) 처리**: 사용자 질문에 민감 정보가 포함될 수 있습니다. 캐싱 전에 PII를 마스킹(Masking) 처리하거나, 벡터화 과정에서 정보가 복원 불가능한 수준으로 변환되는지 검증해야 합니다.
4. **임계값(Threshold) 튜닝**: 유사도 임계값이 너무 낮으면 부정확한 답변을 반환(Hallucination 유발)하고, 너무 높으면 캐시 적중률이 떨어져 비용 절감 효과가 없습니다. 운영 환경에서 A/B 테스트를 통해 지속적으로 튜닝해야 합니다.

## Trade-offs & Limitations

- **정확성 vs 비용**: 의미론적 캐싱은 100% 일치가 아니므로, 미묘한 뉘앙스 차이가 중요한 질의에 대해 오래된(Stale)하거나 약간 다른 답변을 제공할 위험이 있습니다.
- **복잡도 증가**: 시스템에 Vector DB, 임베딩 서비스, 라우팅 로직이 추가되어 장애 지점이 늘어납니다. 캐시 계층이 다운되더라도 LLM로 직접 우회할 수 있는 회로 차단기(Circuit Breaker) 패턴이 반드시 필요합니다.
- **캐시 부정합(Staleness)**: LLM 모델이 업데이트되거나 시스템 프롬프트가 변경되면, 과거에 캐싱된 답변이 현재 정책과 맞지 않을 수 있습니다. 모델 버전을 캐시 키의 일부로 포함하거나, 배포 시 캐시를 무효화(Purge)하는 전략이 필요합니다.

## Final Checklist

- [ ] 캐시 적중률(Hit Rate)과 유사도 분포를 모니터링하는 대시보드 구축 여부
- [ ] 임베딩 생성 지연 시간이 전체 응답 시간(SLA)에 미치는 영향 검증
- [ ] PII 포함 여부를 사전에 필터링하는 파이프라인 구성 여부
- [ ] 캐시 스토리지 용량 한계 도달 시 자동 삭제(Eviction) 정책 설정 여부
- [ ] 모델 라우팅 실패 시 안전한 Fallback 로직 및 재시도 정책 구현 여부
- [ ] 캐시 키에 모델 버전 및 시스템 프롬프트 해시를 포함하여 부정합 방지 여부
