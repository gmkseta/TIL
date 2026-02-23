---
title: "RAG 기반 LLM 서비스에서의 검색 정확도 향상을 위한 Hybrid Search 구현"
date: "2026-02-23"
update: "2026-02-23"
tags: ["auto-draft", "slack", "n8n"]
draft: true
---
# RAG 기반 LLM 서비스에서의 검색 정확도 향상을 위한 Hybrid Search 구현

## Problem Definition
순수 벡터 검색(Dense Retrieval)은 의미적 유사성을 잘 포착하지만, 도메인 특화된 고유 명사나 정확한 키워드 매칭에서 취약점을 보입니다. 이로 인해 LLM이 문맥을 왜곡하거나 사실과 다른 답변을 생성하는 환각(Hallucination) 현상이 발생하여 서비스 신뢰도를 떨어뜨립니다. 특히 기술 문서나 법률 검색처럼 정확성이 중요한 도메인에서 단일 검색 방식은 한계가 명확합니다.

## Why This Matters in Production
기업용 LLM 서비스에서 검색 품질은 사용자 경험과 직결되는 핵심 지표입니다. 검색 결과가 부정확하면 아무리 생성 모델이 성능이 좋아도 신뢰할 수 있는 답변을 만들 수 없습니다. 검색 단계에서의 재현율(Recall)과 정밀도(Precision)를 동시에 높이지 못하면, 후처리 과정에서의 비용이 증가하고 최종적으로 사용자 이탈로 이어집니다.

## Architecture / Technical Approach
하이브리드 검색은 키워드 매칭에 강한 Sparse Retrieval(주로 BM25)과 의미적 유사성에 강한 Dense Retrieval(벡터 임베딩)을 결합하는 방식입니다. 두 검색 결과를 병합할 때 단순 점수 합산보다는 순위 기반 병합 알고리즘인 Reciprocal Rank Fusion(RRF)을 사용하는 것이 일반적입니다. RRF는 각 결과 집합에서 문서의 순위를 활용해 점수를 재계산하므로, 서로 다른 척도의 점수를 정규화할 필요 없이 강건한 결과를 도출합니다.

아키텍처적으로는 Elasticsearch나 OpenSearch와 같은 검색 엔진 내에서 벡터 인덱스와 텍스트 인덱스를 동시에 구성하고, 단일 쿼리 요청으로 두 결과를 모두 가져와 애플리케이션 레이어나 검색 엔진의 Script 기능을 통해 병합합니다. 최신 버전의 검색 엔진들은 내장된 `rrf` 검색 타입을 제공하므로, 네트워크 오버헤드를 줄이고 성능을 높이기 위해 검색 엔진 내부에서 병합을 수행하는 방식을 권장합니다.

## Code Example
다음은 Python을 사용하여 OpenSearch 클라이언트로 하이브리드 검색을 수행하는 예제입니다. 운영 환경의 지연 시간을 최소화하기 위해 `concurrent.futures`를 사용하여 Sparse와 Dense 검색을 병렬로 수행하며, 사용자 입력에 대한 기본적인 검증 로직을 포함합니다.

```python
import concurrent.futures
from opensearchpy import OpenSearch, RequestsHttpConnection

def validate_query_input(query_text):
    """사용자 입력 검증: 비어있거나 너무 긴 쿼리 방지"""
    if not query_text or not isinstance(query_text, str):
        raise ValueError("Invalid query text")
    if len(query_text) > 1000:
        raise ValueError("Query text too long")
    return query_text.strip()

def get_hybrid_search_results(client, index_name, query_text, query_vector, k=5):
    try:
        # 입력값 검증
        validated_query = validate_query_input(query_text)
    except ValueError as e:
        print(f"Input validation error: {e}")
        return []

    # 1. Sparse Search (BM25)
    def execute_sparse_search():
        sparse_query = {
            "size": k * 2,
            "query": {
                "match": {
                    "content": {
                        "query": validated_query
                    }
                }
            }
        }
        try:
            resp = client.search(index=index_name, body=sparse_query)
            return {hit['_id']: hit for hit in resp['hits']['hits']}
        except Exception as e:
            print(f"Sparse search failed: {e}")
            return {}

    # 2. Dense Search (k-NN)
    def execute_dense_search():
        dense_query = {
            "size": k * 2,
            "query": {
                "knn": {
                    "content_vector": {
                        "vector": query_vector,
                        "k": k * 2
                    }
                }
            }
        }
        try:
            resp = client.search(index=index_name, body=dense_query)
            return {hit['_id']: hit for hit in resp['hits']['hits']}
        except Exception as e:
            print(f"Dense search failed: {e}")
            return {}

    # 3. 병렬 검색 실행 (Network RTT 최소화)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_sparse = executor.submit(execute_sparse_search)
        future_dense = executor.submit(execute_dense_search)
        
        sparse_hits = future_sparse.result()
        dense_hits = future_dense.result()

    # 4. Reciprocal Rank Fusion (RRF)
    # RRF 공식: score = sum(1 / (k + rank_i))
    # k_rrf 상수는 검색 결과 크기에 따라 조절 필요. 소규모(top_k=5~10)에서는 20 정도가 적절할 수 있음.
    k_rrf = 20  
    doc_scores = {}

    for rank, doc_id in enumerate(sparse_hits.keys(), start=1):
        score = 1 / (k_rrf + rank)
        doc_scores[doc_id] = doc_scores.get(doc_id, 0) + score

    for rank, doc_id in enumerate(dense_hits.keys(), start=1):
        score = 1 / (k_rrf + rank)
        doc_scores[doc_id] = doc_scores.get(doc_id, 0) + score

    # 5. 결과 정렬 및 반환
    ranked_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:k]
    
    final_results = []
    for doc_id, score in ranked_docs:
        # Sparse 결과에 우선순위를 두어 메타데이터 가져오기 (필요시 로직 변경)
        doc = sparse_hits.get(doc_id) or dense_hits.get(doc_id)
        if doc:
            doc['_score'] = score
            final_results.append(doc)

    return final_results

# Usage
# client = OpenSearch(...)
# results = get_hybrid_search_results(client, "docs-index", "Redis 설정", [0.1, 0.2, ...])
```

## Operational Considerations
운영 환경에서는 임베딩 모델의 선택과 인덱싱 전략이 중요합니다. 도메인에 맞는 임베딩 모델을 사전 학습(Fine-tuning)하지 않으면 벡터 검색의 성능이 저하될 수 있습니다. 또한, 벡터 차원수에 따른 인덱스 크기 증가와 메모리 사용량을 모니터링해야 합니다. OpenSearch의 경우 `nmslib`이나 `faiss` 같은 라이브러리를 사용하여 HNSW 파라미터(`ef_construction`, `m`)를 튜닝하여 검색 속도와 정확도 사이의 균형을 맞춰야 합니다.

## Trade-offs & Limitations
하이브리드 검색의 가장 큰 트레이드오프는 지연 시간(Latency)과 비용입니다. 두 가지 검색을 순차 혹은 병렬로 수행해야 하므로 단일 검색보다 소요 시간이 길어집니다. 또한, 벡터 인덱스를 유지하기 위한 리소스 비용이 추가로 발생합니다. 검색 결과의 가중치(Alpha) 조정은 정량적인 기준보다는 사용자 피드백에 의존하는 경향이 있어, A/B 테스트를 통한 지속적인 튜닝이 필요합니다. RRF 상수(`k_rrf`) 설정 시 검색 결과의 개수(`top_k`)를 고려해야 하며, 소규모 결과 세트에서는 너무 높은 값(예: 60)을 사용하면 순위 차이에 따른 점수 변화가 미미하여 정렬 효과가 떨어질 수 있습니다. ASSUMPTION: 특정 도메인에서는 BM25와 벡터 검색의 결과 편차가 커서 RRF 상수 조정만으로는 해결되지 않을 수 있습니다.

## Final Checklist
- [ ] 검색 엔진(Elasticsearch/OpenSearch) 버전이 벡터 검색 및 Hybrid Search를 지원하는지 확인
- [ ] 임베딩 모델의 성능 벤치마크 및 도메인 적합성 검토
- [ ] RRF 알고리즘 구현 및 파라미터(k) 튜닝 (결과 크기에 따른 상수 값 조절 포함)
- [ ] 인덱스 매핑 시 벡터 필드와 텍스트 필드의 동시 구성
- [ ] 검색 지연 시간 최소화를 위한 병렬 처리(Async/Thread) 적용
- [ ] 사용자 입력 검증(Sanitization) 및 에러 핸들링 로직 추가
- [ ] 비용 대비 효과 분석을 위한 메트릭 정의(Recall@K, MRR 등)
