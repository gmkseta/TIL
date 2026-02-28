---
title: "Pragmatic implementation guide: 주제: 오픈클로로 쿠팡 주문/발주 자동화시키기. 한국어로 실무형 기술 블로그로 써줘. 필수: 운영 제약, 인증(HMAC), 멱등성, 재시도, 실패 시나리오, "
date: "2026-02-28"
update: "2026-02-28"
tags: ["auto-draft", "slack", "n8n"]
draft: true
---
# 쿠팡 오픈 API 기반 주문/발주 자동화 아키텍처 설계

## 1. TL;DR
* 쿠팡 오픈 API의 HMAC 인증과 Rate Limit 제약을 준수하기 위해 **API Gateway 패턴과 중앙 집중식 인증 모듈**을 도입해야 한다.
* 주문/발주 데이터의 정합성을 보장하기 위해 **멱등성 키(Idempotency Key) 처리와 DB 기반 트랜잭션 아웃박스(Outbox) 패턴**을 적용하여 중복 발주를 방지한다.
* 외부 API 장애에 대응하기 위해 **지수 백오프(Exponential Backoff) 재시도 정책과 데드 레터 큐(Dead Letter Queue)**를 구성하여 운영 부담을 줄인다.

## 2. Problem Definition
쿠팡 오픈 API를 활용해 자사 시스템(ERP/WMS)과 쿠팡 로지스틱 네트워크를 연동하여 주문 수집 및 발주(입고 요청) 프로세스를 자동화해야 한다. 단순한 API 호출을 넘어, 높은 트래픽 구간에서의 안정적인 데이터 동기화, 인증 보안, 그리고 외부 시스템 장애 시 데이터 유실 방지가 핵심 과제다. 특히 쿠팡의 엄격한 Rate Limit 정책과 HMAC 보안 요구사항을 충족하면서도 비즈니스의 연속성을 확보하는 것이 어렵다.

## 3. Production Context and Constraints
* **인증 방식**: HMAC-SHA256 알고리즘을 사용한 서명 인증이 필수이며, `Authorization` 헤더와 `X-Requested-By` 헤더 설정이 요구됨 (참고: [Coupang OPEN API](https://developers.coupangcorp.com/hc/en-us/articles/360033917473-Coupang-OPEN-API)).
* **Rate Limit**: 쿠팡 API는 엄격한 호출 횟수 제한이 있으며, 이를 초과 시 429 에러가 발생하거나 계정이 일시 정지될 수 있음 (ASSUMPTION: 구체적인 수치는 공개 문서에 명시되지 않으나 실무에서는 1초당 몇 회 수준으로 제한됨).
* **데이터 일관성**: 주문 상태(결제, 배송 시작 등)와 발주 요청의 순서가 보장되어야 하며, 네트워크 오류로 인한 중복 처리가 금지됨.
* **운영 환경**: 온프레미스 또는 클라우드 환경의 내부 서버에서 쿠팡 외부로 요청을 보내며, 방화벽 및 아웃바운드 프록시 설정이 필요할 수 있음.

## 4. Design Options and Trade-offs

| 옵션 | 설명 | 장점 | 단점 | 적합성 |
| :--- | :--- | :--- | :--- | :--- |
| **A. Sync API 호출 (Webhook 방식)** | 쿠팡 이벤트 발생 시 즉시 내부 API를 호출하여 처리 | 구현이 단순하고 실시간성 보장 | 쿠팡 서버 장애 시 내부 시스템 영향, 재시도 로직 구현 난이도 높음 | 부적합 (안정성 저하) |
| **B. Polling + Batch Job** | 주기적으로 쿠팡 API를 조회하여 변경 데이터 수집 | 제어권이 내부 시스템에 있음, 구현 쉬움 | 실시간성 저하, 불필요한 API 호출로 Rate Limit 소모, 리소스 낭비 | 보통 (초기 구축 시) |
| **C. Event-Driven + Queue (선택)** | 메시지 큐를 통해 API 요청을 비동기 처리하고 순차 실행 | Rate Limit 제어 용이, 장애 격리 및 재시도 용이, 확장성 우수 | 인프라 복잡도 증가, 메시지 순서 보장 설정 필요 | **최적 (Production Grade)** |

## 5. Chosen Architecture / Technical Approach
**이벤트 기반 비동기 아키텍처(Event-Driven Architecture)**를 채택한다.
내부 시스템에서 발생한 주문/발주 이벤트는 메시지 브로커(Kafka/RabbitMQ)로 전송되며, **API Worker**가 이를 소비하여 쿠팡 API를 호출한다. Rate Limit를 준수하기 위해 Worker의 동시성(Concurrency)을 제어하고, 요청 실패 시 지수 백오프(Exponential Backoff)를 적용하여 재시도한다. 인증(HMAC) 생성 로직은 공통 라이브러리로 분리하여 보안성을 높이고 관리 포인트를 줄인다.

## 6. Implementation Details

### 6.1 인증(HMAC) 생성 모듈
쿠팡 API는 `HmacSHA256`을 요구한다. 요청 데이터(타임스탬프, HTTP 메서드, 경로, 쿼리 스트링)를 조합하여 서명을 생성한다. 타임스탬프는 시스템 간 시간 차이로 인한 인증 실패를 방지하기 위해 API 서버 시간을 기준으로 동기화하거나 여유를 두어 설정해야 한다.

### 6.2 멱등성(Idempotency) 보장
네트워크 타임아웃 등으로 인해 클라이언트가 요청 결과를 확인하지 못하고 재요청을 보낼 경우, 중복 발주를 방지하기 위해 **멱등성 키**를 사용한다. 쿠팡 API 명세서에 별도의 멱등성 키 헤더가 언급되어 있지 않으므로(ASSUMPTION), 내부 DB에 `request_id` (또는 `vendorItemId` + `timestamp`)를 저장하여 중복 요청을 사전에 필터링한다. 이때 DB 레벨의 유니크 제약 조건(Unique Constraint)을 활용하여 Race Condition을 방지해야 한다.

### 6.3 재시도(Retry) 및 회로 차단(Circuit Breaker)
일시적인 네트워크 오류나 5XX 서버 에러 발생 시, **지수 백오프(Exponential Backoff)** 전략을 사용하여 재시도한다. 연속적인 실패가 발생하면 **Circuit Breaker**를 열어 일시적으로 요청을 차단하고, 장애 복구 시점까지 시스템 부하를 줄인다.

## 7. Code and Config Examples

### 7.1 HMAC Signature 생성 (Python 예시)
공식 문서의 로직을 참조하여 작성된 HMAC 생성 코드다. 타임스탬프 포맷과 메시지 조합 순서를 명시하여 검증한다.

```python
import hmac
import hashlib
import time

def generate_hmac_signature(access_key, secret_key, method, url_path, query_string=""):
    """
    쿠팡 OPEN API HMAC Signature 생성
    Reference: https://developers.coupangcorp.com/hc/en-us/articles/360033988873-OPEN-API-Test-Guide
    """
    # 타임스탬프 포맷: yyyyMMddTHHmmssZ (예: 20231027T123000Z)
    timestamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

    # message 구성: datetime + method + path + querystring
    # 문서 예시: [timestamp, httpMethod, requestPath, queryString].join("")
    message = f"{timestamp}{method.upper()}{url_path}{query_string}"
    
    # HMAC-SHA256 Hash 생성
    signature = hmac.new(
        secret_key.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    # Authorization Header 조립
    # CEA algorithm=HmacSHA256, access-key=..., signed-date=..., signature=...
    auth_header = f"CEA algorithm=HmacSHA256, access-key={access_key}, signed-date={timestamp}, signature={signature}"
    
    return auth_header
```

### 7.2 API 요청 및 재시도 로직 (Pseudo-code)
보안 키는 환경 변수에서 로드하며, 429 에러 발생 시에도 재시도하도록 설정한다.

```python
import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# API 기본 설정 (환경 변수 사용)
VENDOR_ID = os.getenv("COUPANG_VENDOR_ID")
ACCESS_KEY = os.getenv("COUPANG_ACCESS_KEY")
SECRET_KEY = os.getenv("COUPANG_SECRET_KEY")
BASE_URL = "https://api-gateway.coupang.com"

class RateLimitError(Exception):
    """429 Rate Limit 에러 처리를 위한 커스텀 예외"""
    pass

def is_rate_limit_error(retry_state):
    """429 에러인 경우 재시도하도록 판별"""
    return retry_state.outcome.exception() is not None and \
           isinstance(retry_state.outcome.exception(), RateLimitError)

@retry(
    stop=stop_after_attempt(5), 
    wait=wait_exponential(multiplier=2, min=4, max=60),
    retry=is_rate_limit_error,
    reraise=True
)
def call_coupang_api(method, path, payload=None):
    # HMAC 생성
    auth_header = generate_hmac_signature(ACCESS_KEY, SECRET_KEY, method, path)
    
    headers = {
        "Authorization": auth_header,
        "X-Requested-By": VENDOR_ID,
        "Content-Type": "application/json"
    }
    
    url = f"{BASE_URL}{path}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=payload, headers=headers)
        
        # 429 에러 발생 시 커스텀 예외 발생시켜 재시도 트리거
        if response.status_code == 429:
            raise RateLimitError(f"Rate limit exceeded: {response.text}")
            
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.HTTPError as err:
        # 429는 위에서 처리했으므로 여기서는 5xx 등 기타 에러 로깅
        print(f"API Error: {response.status_code} - {response.text}")
        raise
```

### 7.3 Infrastructure Config (Terraform HCL 예시)
Rate Limiting을 위한 API Gateway 설정 (AWS 기준 가정).

```hcl
resource "aws_api_gateway_rest_api" "coupang_proxy" {
  name        = "CoupangOrderProxy"
  description = "Proxy for Coupang Open API with Rate Limiting"
}

resource "aws_api_gateway_method_settings" "coupang_settings" {
  rest_api_id = aws_api_gateway_rest_api.coupang_proxy.id
  stage_name  = var.stage_name
  method_path = "*/*"

  settings {
    throttling_burst_limit = 10  # 버스트 제한
    throttling_rate_limit  = 5   # 초당 요청 수 (Rate Limit 준수)
  }
}
```

## 8. Verification and Metrics
시스템 안정성을 모니터링하기 위해 다음 지표를 수집한다.

* **API Error Rate (4xx, 5xx)**: 쿠팡 API 호출 실패율. 특히 429(Too Many Requests) 발생 빈도를 주시한다.
* **P95 Latency**: API 요청부터 응답까지의 소요 시간. 슬로우 쿼리나 네트워크 지연을 조기에 발견한다.
* **Queue Depth (메시지 큐 길이)**: 처리 대기 중인 주문/발주 건수. 급증 시 Worker 스케일 아웃 트리거로 활용한다.
* **Idempotency Conflict Rate**: 중복 요청이 필터링된 비율. 클라이언트 로직의 문제나 타임아웃 설정 문제를 파악한다.

## 9. Operational Runbook
* **Rate Limit 초과 발생 시**:
    1. CloudWatch/Dashboards에서 429 에러 급증 여부 확인.
    2. Worker의 동시성(Concurrency) 설정을 낮추거나, 배치 처리 간격을 늘려 요청 밀도를 감소시킴.
    3. 쿠팡 개발자 포털에서 현재 계정의 제한 상태 확인 (ASSUMPTION).
* **인증 실패(401/403) 발생 시**:
    1. Access Key/Secret Key의 유효성 및 만료 여부 확인.
    2. 서버 시간(NTP) 동기화 여부 확인 (HMAC 타임스탬프 오류 가능성).
* **주문 누락 발생 시**:
    1. Outbox 테이블의 `status`가 'PENDING'인 레코드 조회.
    2. Worker 로그 확인
