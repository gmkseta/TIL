---
title: "LLM 기반 블로그 파이프라인에서 프롬프트 인젝션 방어 아키텍처 설계"
date: "2026-02-23"
update: "2026-02-23"
tags: ["auto-draft", "slack", "n8n"]
draft: true
---
# LLM 기반 블로그 파이프라인에서 프롬프트 인젝션 방어 아키텍처 설계

## Problem Definition
외부 웹 콘텐츠나 사용자 입력을 LLM에 직접 전달하면 프롬프트 인젝션 공격에 취약합니다. 공격자는 시스템 프롬프트를 오버라이드하거나 비밀 정보를 탈취할 수 있습니다. 이는 콘텐츠 품질 저하를 넘어 시스템 유출이나 심각한 보안 사고로 이어집니다. 신뢰할 수 없는 입력은 LLM 전달 전후로 다단계 검증이 필수입니다.

## Why This Matters in Production
생성형 AI 도입으로 보안 사고가 급증하고 있으며, 규제와 보안 요구 수준도 높아지고 있습니다. 블로그 파이프라인이 탈취되어 악성 코드나 허위 정보 유포에 악용되면 서비스 신뢰도는 회복 불가능합니다. 운영 환경은 변화하는 공격 패턴에 지속적으로 대응해야 하므로, 일회성 우회가 아닌 구조적 방어가 필수적입니다. 안전한 LLMOps는 서비스 생존을 위한 필수 조건입니다.

## Architecture / Technical Approach
프롬프트 인젝션 방어를 위해 **Defense in Depth(심층 방어)** 접근 방식이 필요합니다. 단일 차단을 넘어 입력 전처리, 컨텍스트 분리, 출력 후처리의 3단계 계층을 설계해야 합니다.

1.  **입력 전처리 (Input Sanitization):** 웹 스크래핑 결과물에서 HTML 태그를 제거하고, 정규 표현식과 LLM 기반 분류기를 혼용하여 의심스러운 패턴을 필터링합니다. 단순 키워드 매칭만으로는 우회가 가능하므로, 의도를 분석하는 검증 계층이 추가로 필요합니다.
2.  **메시지 구분 (Role Separation):** LangChain이나 LlamaIndex의 `SystemMessage`, `HumanMessage`, `AIMessage` 역할을 명확히 구분하여 사용자 입력이 시스템 명령어로 해석되지 않도록 구조적으로 격리합니다.
3.  **가드레일 (Guardrails):** NeMo Guardrails나 Llama Guard와 같은 전용 모델을 활용하여 입력과 출력을 실시간으로 검증하는 중간 미들웨어를 둡니다. 비용 효율을 위해 경량 모델을 사용하거나 캐싱 전략을 병행합니다.
4.  **샌드박스 실행:** 생성된 코드나 쿼리는 격리된 환경(Firecracker microVM 등)에서 실행하여 시스템 자원 접근을 차단합니다.

## Code Example
LangChain을 사용하여 입력값을 정교하게 검증하고 시스템 프롬프트와 사용자 입력을 구분하는 예제입니다.

```python
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage
import re

def validate_input(user_input: str) -> bool:
    """
    정규 표현식 1차 필터링 및 LLM 기반 분류기 호출 시뮬레이션.
    실제 운영 환경에서는 별도의 분류 모델 API를 호출하여 의도를 분석합니다.
    """
    # 1차: 룰 기반 필터링 (유니코드 변형 등에 취약할 수 있음)
    forbidden_patterns = ["ignore previous instructions", "print system prompt", "admin override"]
    for pattern in forbidden_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            return False
    
    # 2차: LLM 기반 분류기 (예시)
    # is_malicious = llm_classifier.predict(user_input)
    # if is_malicious: return False
    
    return True

def generate_blog_post(topic: str, scraped_content: str):
    if not validate_input(scraped_content):
        raise ValueError("입력값에 잠재적 악의적인 패턴이 감지되었습니다.")

    # 시스템 프롬프트와 사용자 입력을 명확히 분리
    messages = [
        SystemMessage(content="당신은 기술 블로그 전문 작가입니다. 수집된 정보를 바탕으로 요약글을 작성하세요."),
        HumanMessage(content=f"주제: {topic}\n내용: {scraped_content}")
    ]
    
    prompt = ChatPromptTemplate.from_messages(messages)

    # 실제 LLM 호출 로직 (생략)
    # response = llm(prompt.format_messages())
    # return response
```

## Operational Considerations
운영 환경에서는 거짓 양성(False Positive)과 거짓 음성(False Negative)의 균형이 중요합니다. 정상 콘텐츠가 차단되지 않도록 규칙을 주기적으로 튜닝하고, 필터링된 케이스는 인간의 확인(Human-in-the-loop) 프로세스를 통해 예외 처리 경로를 마련해야 합니다. 또한, 필터링 지연 시간이 파이프라인 SLA에 영향을 주지 않도록 비동기 처리를 고려해야 합니다. 보안 로그는 SIEM 시스템으로 전송하여 공격 패턴을 분석하고 규칙을 업데이트하는 피드백 루프를 구성해야 합니다.

## Trade-offs & Limitations
가드레일과 검증 로직 추가는 추론 비용과 지연 시간을 증가시킵니다. 모든 입력을 무거운 분류 모델에 통과시키는 것은 비효율적이므로, 가벼운 룰 기반 필터와 모델 기반 필터를 하이브리드로 사용해야 합니다. 과도한 보안 강화는 정상 콘텐츠의 창의성을 저하시킬 수 있습니다. 100% 안전한 필터링은 존재하지 않으므로, 이 아키텍처는 위험을 '감소'시키는 것이지 '완전히 제거'하는 것이 아님을 인지해야 합니다.

## Final Checklist
- [ ] 사용자 입력과 시스템 프롬프트가 메시지 객체 레벨에서 철저히 분리되어 있는가?
- [ ] 입력값에 대한 정규 표현식 필터링과 LLM 기반 분류가 하이브리드로 구현되어 있는가?
- [ ] LLM 출력값을 검증하는 별도의 가드레일 모델이 배포되어 있는가?
- [ ] 필터링 로직으로 인한 파이프라인 지연 시간을 모니터링하고 있는가?
- [ ] 거짓 양성(차단된 정상 트래픽)을 분석하고 Human-in-the-loop 프로세스가 있는가?
