---
title: "대규모 링크 기반 자동화 파이프라인의 회복탄력성 패턴 설계"
date: "2026-02-23"
update: "2026-02-23"
tags: ["auto-draft", "slack", "n8n"]
draft: true
---
# 대규모 링크 기반 자동화 파이프라인의 회복탄력성 패턴 설계

## Problem Definition
외부 링크를 수집하여 콘텐츠를 생성하는 자동화 파이프라인은 네트워크 불안정, 타겟 서버의 404/503 에러, 봇 탐지(Bot Detection) 등 예측 불가능한 외부 장애에 직면합니다. 단일 실패가 전체 파이프라인을 멈추게 하거나, 재시도 로직이 부재하여 데이터 유실이 발생하는 문제가 빈번합니다. 특히 대규모 처리 환경에서는 일시적인 장애가 연쇄적으로 시스템 자원을 고갈시켜 전체 서비스의 안정성을 저해합니다.

## Why This Matters in Production
생성형 AI 기반 콘텐츠 자동화 수요가 급증함에 따라, 웹 스크래핑 및 데이터 파이프라인의 안정성은 비즈니스 연속성을 좌우하는 핵심 요소가 되었습니다. 파이프라인이 중단되면 콘텐츠 갱신이 멈추고 트래픽 유입에 타격을 입습니다. 안정적인 운영을 위해서는 외부 의존성(Dependency)이 발생하는 지점에서의 회복탄력성(Resiliency) 설계가 필수적입니다.

## Architecture / Technical Approach
회복탄력성을 확보하기 위해 이벤트 드리븐 아키텍처(Event-Driven Architecture)를 기반으로 한 **멱등성(Idempotency) 보장** 및 **장애 격리** 패턴을 적용해야 합니다.

1. **메시지 큐(Message Queue) 도입**: Kafka 또는 SQS를 사용하여 링크 처리 요청을 비동기로 처리하고, 버퍼링을 통해 스파이크 트래픽을 흡수합니다.
2. **서킷 브레이커(Circuit Breaker)**: 외부 API 호출 실패율이 임계치를 넘으면 즉시 호출을 차단하여 시스템 리소스 낭비를 막고 빠르게 실패(Fail Fast) 처리합니다.
3. **재시도 정책(Retry Policy) 및 지수 백오프(Exponential Backoff)**: 일시적인 오류에 대응하기 위해 재시도를 수행하되, 대기 시간을 지수적으로 늘려 타겟 서버에 과부하를 주지 않습니다.
4. **데드 레터 큐(Dead Letter Queue)**: 지정된 횟수만큼 재시도 후에도 실패한 메시지는 별도 큐로 격리하여 수동 검수나 별도 로직으로 처리합니다.

## Code Example
Python과 `tenacity`, `pybreaker` 라이브러리를 활용하여 서킷 브레이커, 지수 백오프, 그리고 봇 탐지 방지를 포함한 웹 스크래핑 예제입니다.

```python
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import pybreaker
from bs4 import BeautifulSoup
import logging

# 타겟 서버의 일시적 오류나 봇 탐지(5xx, 429)를 가정
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}

class TargetServerError(Exception):
    pass

# 서킷 브레이커 설정: 5회 실패 시 Open 상태로 전환, 30초 후 Half-Open 시도
scraper_breaker = pybreaker.CircuitBreaker(
    fail_max=5,
    timeout_duration=30
)

@retry(
    stop=stop_after_attempt(5),  # 최대 5회 시도
    wait=wait_exponential(multiplier=1, min=2, max=10),  # 2초부터 시작, 최대 10초 대기
    retry=retry_if_exception_type(TargetServerError),
    before_sleep=lambda retry_state: logging.warning(f"Retrying... attempt {retry_state.attempt_number}")
)
@scraper_breaker
def fetch_content(url: str) -> str:
    try:
        # 봇 탐지 방지를 위해 User-Agent 헤더 설정
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # 연결 타임아웃(3.05초)과 읽기 타임아웃(5초)을 분리하여 설정
        response = requests.get(url, headers=headers, timeout=(3.05, 5))
        
        if response.status_code in RETRYABLE_STATUS_CODES:
            raise TargetServerError(f"Retryable status code: {response.status_code}")
        response.raise_for_status()
        
        # 웹 스크래핑 맥락에 맞게 HTML 파싱 수행
        soup = BeautifulSoup(response.text, 'html.parser')
        # 예시: 페이지 제목 추출 (비즈니스 로직에 따라 변경 필요)
        title = soup.find('title').get_text(strip=True) if soup.find('title') else "No Title"
        return title
        
    except requests.exceptions.RequestException as e:
        # 네트워크 오류나 타임아웃도 재시도 대상으로 간주
        raise TargetServerError(f"Request failed: {e}")

# 운영 환경에서는 이 함수를 큐 컨슈머 내부에서 실행
try:
    content_title = fetch_content("https://example.com/article")
    logging.info(f"Successfully fetched: {content_title}")
    # 성공 시 비즈니스 로직 처리
except pybreaker.CircuitBreakerError:
    # 서킷 브레이커가 열린 경우
    logging.error("Circuit breaker is open. Request blocked.")
except TargetServerError:
    # 최종 실패 시 로깅 및 DLQ(DLQ는 인프라 레벨에서 처리)로 이동
    logging.error("Failed to process URL after retries.")
```

## Operational Considerations
실제 운영 환경에서는 코드 레벨의 처리 외에도 인프라 모니터링이 필수입니다.
- **메트릭 수집**: Prometheus/Grafana를 통해 큐의 래깅(Lag) 길이, 서킷 브레이커의 열림(Open) 상태, DLQ로 전송되는 메시지의 비율을 실시간으로 모니터링해야 합니다.
- **헬스체크**: 외부 서비스의 상태를 주기적으로 확인하는 헬스체크 엔드포인트를 구성하여, 장애 발생 시 알림을 받을 수 있게 해야 합니다.
- **로그 상관관계**: 요청 ID(Request ID)를 추적하여 특정 링크 처리가 어느 단계에서 실패했는지 파악할 수 있어야 합니다.

## Trade-offs & Limitations
회복탄력성 패턴 도입 시 다음과 같은 트레이드오프를 고려해야 합니다.
- **외부 서버 부하**: 공격적인 재시도 정책은 타겟 서버를 공격으로 오인하게 만들어 IP 차단을 유발할 수 있습니다. 반드시 Rate Limiting을 병행해야 합니다.
- **운영 오버헤드**: 데드 레터 큐(DLQ)에 쌓인 메시지를 처리하고 재시도하는 별도의 운영 프로세스가 필요합니다. 이를 방치하면 스토리지 비용이 증가하고 데이터 처리 지연이 발생합니다.
- **복잡도 증가**: 서킷 브레이커와 재시도 로직은 분산 시스템의 복잡도를 높이며, 디버깅을 어렵게 만들 수 있습니다.

## Final Checklist
- [ ] 외부 API 호출에 타임아웃(Timeout)이 설정되어 있는가?
- [ ] 지수 백오프(Exponential Backoff)를 적용한 재시도 정책이 있는가?
- [ ] 서킷 브레이커를 통해 연쇄 장애(Cascading Failure)를 방지하는가?
- [ ] 처리 불가능한 메시지를 격리하기 위한 데드 레터 큐(DLQ)가 있는가?
- [ ] 큐 처리 지연(Lag) 및 에러율을 모니터링하는 대시보드가 구축되어 있는가?
- [ ] 재시도 로직이 타겟 서버의 Rate Limit을 위반하지 않도록 제어되는가?
