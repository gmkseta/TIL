---
title: "LLM 기반 블로그 파이프라인에서 프롬프트 인젝션 방어 아키텍처 설계"
date: "2026-02-23"
update: "2026-02-23"
tags: ["auto-draft", "slack", "n8n"]
draft: true
---
# LLM 기반 블로그 파이프라인에서 프롬프트 인젝션 방어 아키텍처 설계

## Problem Definition
외부 링크를 통해 수집된 웹 콘텐츠나 사용자 입력을 LLM에 직접 전달하는 시스템은 악의적인 프롬프트 삽입(Prompt Injection)에 취약합니다. 공격자는 입력값에 시스템 프롬프트를 오버라이드하거나 비밀 정보를 탈취하려는 명령어를 포함시킬 수 있습니다. 이러한 공격은 단순히 콘텐츠 생성 품질을 떨어뜨리는 것을 넘어, 시스템 프롬프트 유출이나 의도치 않은 동작을 유발할 수 있는 심각한 보안 사고로 이어집니다. 따라서 신뢰할 수 없는 입력(Untrusted Input)이 LLM 컨텍스트에 포함되기 전과 후에 철저한 검증 계층이 필요합니다.

## Why This Matters in Production
생성형 AI를 도입한 서비스에서 보안 사고가 급증하고 있으며, 규제 기관과 사용자의 보안 요구 수준도 날로 높아지고 있습니다. 블로그 자동화 파이프라인이 공격자에 의해 탈취되어 악성 코드 생성이나 허위 정보 유포의 도구로 사용된다면 서비스의 신뢰도는 회복 불가능한 수준으로 추락합니다. 특히, 운영 환경에서는 개발 단계와 달리 지속적으로 변하는 공격 패턴에 대응해야 하므로, 일회성 우회가 아닌 구조적인 방어 메커니즘이 필수적입니다. 안전한 LLMOps를 구축하는 것은 선택이 아니라 서비스 생존을 위한 필수 조건입니다.

## Architecture / Technical Approach
프롬프트 인젝션 방어를 위해서는 **Defense in Depth(심층 방어)** 접근 방식이 필요합니다. 단일 지점에서의 차단을 넘어, 입력 전처리, 컨텍스트 분리, 출력 후처리의 3단계 계층을 설계해야 합니다.

1.  **입력 전처리 (Input Sanitization):** 웹 스크래핑 결과물에서 HTML 태그를 제거하고, 자연어 처리(NLP)를 통해 의심스러운 패턴(예: "시스템 프롬프트 무시", "JSON 출력" 등의 키워드)을 필터링합니다.
2.  **메시지 구분 (Role Separation):** LangChain이나 LlamaIndex와 같은 프레임워크의 `SystemMessage`, `HumanMessage`, `AIMessage` 역할을 명확히 구분하여 사용자 입력이 시스템 명령어로 해석되지 않도록 구조적으로 격리합니다.
3.  **가드레일 (Guardrails):** NeMo Guardrails나 Llama Guard와 같은 전용 모델을 활용하여 입력과 출력을 실시간으로 검증하는 중간 미들웨어를 둡니다.
4.  **샌드박스 실행:** 생성된 코드나 쿼리가 있다면 이를 실행하기 전에 격리된 환경(Firecracker microVM 등)에서 실행하여 시스템 자원에 직접 접근하지 못하게 합니다.

## Code Example
LangChain을 사용하여 입력값을 검증하고 시스템 프롬프트와 사용자 입력을 구분하는 간단한 예제입니다.

```python
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage
import re

def validate_input(user_input: str) -> bool:
    """
    간단한 키워드 기반 필터링.
    실제 운영 환경에서는 더 정교한 분류 모델을 사용해야 합니다.
    """
    forbidden_patterns = ["ignore previous instructions", "print system prompt", "admin override"]
    for pattern in forbidden_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            return False
    return True

def generate_blog_post(topic: str, scraped_content: str):
    if not validate_input(scraped_content):
        raise ValueError("입력값에 잠재적 악의적인 패턴이 감지되었습니다.")

    # 시스템 프롬프트와 사용자 입력을 명확히 분리
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="당신은 기술 블로그 전문 작가입니다. 수집된 정보를 바탕으로 요약글을 작성하세요."),
        HumanMessage(content=f"주제: {topic}\n내용: {scraped_content}")
    ])

    # 실제 LLM 호출 로직 (생략)
    # response = llm(prompt.format_messages())
    # return response
```

## Operational Considerations
운영 환경에서는 거짓 양성(False Positive)과 거짓 음성(False Negative)의 균형을 맞추는 것이 중요합니다. 정상적인 기술 블로그 글(예: "시스템 설계 시 고려할 점")이 필터링되지 않도록 규칙을 주기적으로 튜닝해야 합니다. 또한, 필터링 단계에서 발생한 지연 시간(Latency)이 전체 파이프라인의 SLA에 영향을 주지 않도록 비동기 처리를 고려해야 합니다. 보안 로그는 별도의 SIEM(Security Information and Event Management) 시스템으로 전송하여, 공격 시도 패턴을 분석하고 규칙을 업데이트하는 피드백 루프를 구성해야 합니다.

## Trade-offs & Limitations
가드레일과 검증 로직을 추가하면 그만큼 추론 비용과 지연 시간이 증가합니다. 모든 입력을 별도의 분류 모델(Classifier)에 통과시키는 것은 비용 효율적이지 않을 수 있으므로, 정규 표현식 등의 가벼운 룰 기반 필터와 모델 기반 필터를 하이브리드로 사용하는 것이 일반적입니다. 또한, 과도하게 보안을 강화하면 정상적인 콘텐츠 생성이 제한되어 결과물의 창의성이나 품질이 저하될 수 있습니다. 100% 안전한 필터링은 존재하지 않으므로, 이 아키텍처는 위험을 '감소'시키는 것이지 '완전히 제거'하는 것이 아님을 인지해야 합니다.

## Final Checklist
- [ ] 사용자 입력과 시스템 프롬프트가 메시지 객체 레벨에서 철저히 분리되어 있는가?
- [ ] 입력값에 대한 기본적인 정규 표현식 필터링이 구현되어 있는가?
- [ ] LLM 출력값을 검증하는 별도의 가드레일 모델이 배포되어 있는가?
- [ ] 필터링 로직으로 인한 파이프라인 지연 시간을 모니터링하고 있는가?
- [ ] 거짓 양성(차단된 정상 트래픽)을 분석하고 규칙을 주기적으로 리뷰하는 프로세스가 있는가?
