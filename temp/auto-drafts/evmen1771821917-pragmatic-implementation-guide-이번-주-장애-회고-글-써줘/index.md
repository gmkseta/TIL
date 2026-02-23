---
title: "Pragmatic implementation guide: 이번 주 장애 회고 글 써줘"
date: "2026-02-23"
update: "2026-02-23"
tags: ["auto-draft", "slack", "n8n"]
draft: true
---
# Pragmatic implementation guide: 이번 주 장애 회고 글 쓰기

## Problem Definition
장애 회고(Incident Review) 문서는 단순히 "무엇이 잘못되었는가"를 나열하는 보고서가 아닙니다. 핵심은 동일한 장애가 재발하지 않도록 시스템과 프로세스를 어떻게 개선할 것인가를 정의하는 데 있습니다. 많은 팀이 형식적인 절차를 따르거나, 비난(blame)을 회피하기 위해 기술적인 세부사항을 흐리는 실수를 범합니다. 이로 인해 근본 원인(Root Cause)이 가려지고 실질적인 액션 아이템 도출이 불가능해집니다. 본 가이드는 생산 환경에서 즉시 적용 가능한 장애 회고 문서화 프레임워크를 제공합니다.

## Why This Matters in Production
운영 환경에서 장애는 필연적으로 발생합니다. 중요한 것은 장애 자체가 아니라, 장애 발생 시 시스템이 얼마나 빠르게 복구되었는가(MTTTR), 그리고 우리가 얼마나 많은 것을 배웠는가입니다. 잘 작성된 회고는 엔지니어링 팀의 심리적 안전감(Psychological Safety)을 높이고, 온콜(On-call) 엔지니어의 번아웃을 방지합니다. 또한, 후임자들이 동일한 함정에 빠지지 않도록 지식 베이스(Knowledge Base)를 축적하는 핵심 자산이 됩니다.

## Architecture / Technical Approach
장애 회고 문서는 다음과 같은 구조를 가져야 합니다.

1.  **개요 (Executive Summary):** 경영진이나 타 팀이 1분 안에 상황을 파악할 수 있는 요약.
2.  **타임라인 (Timeline):** 장애 발생, 감지, 대응, 복구 시점의 로그 기반 정확한 시간대.
3.  **영향도 (Impact):** SLA 위반 수준, 영향받은 사용자 수, 매출 손실 등의 정량적 지표.
4.  **근본 원인 분석 (Root Cause Analysis):** 5 Whys 기법 등을 활용한 기술적/프로세스적 원인.
5.  **대응 및 복구 (Response & Resolution):** 당시 수행한 명령어, 롤백 절차 등.
6.  **Follow-up Actions:** 담당자, 마감기한(Due Date)이 명시된 실행 가능한 과제.

**접근 방식:**
*   **Blameless Postmortem:** "누가"가 아니라 "어떤 프로세스나 시스템 결함이" 문제를 야기했는지에 집중합니다.
*   **자동화된 데이터 수집:** 모니터링 툴(Prometheus, Datadog 등)의 링크를 타임라인에 직접 삽입하여 주관적 해석을 배제합니다.

## Code Example
장애 회고 문서를 위한 마크다운 템플릿입니다. 이 템플릿을 저장소에 `.md` 파일로 저장하여 사용하세요.

```markdown
# [Date] Incident Report: [Incident Title]

## Summary
[2-3 sentences explaining what happened and the impact.]

## Impact
- **Duration:** [Start Time] to [End Time] ([Total Duration])
- **Affected Services:** [Service A, Service B]
- **User Impact:** [e.g., 5% of users experienced errors]
- **SLA Breach:** [Yes/No]

## Root Cause
[Describe the technical root cause clearly.]
[Example: A recent deployment to Service B introduced a memory leak in the caching layer, causing OOM kills.]

## Timeline
| Time (UTC) | Description |
|------------|-------------|
| 10:00 | Alert triggered: High Error Rate on Service B |
| 10:05 | On-call engineer acknowledged the alert |
| 10:10 | Identified correlation with recent deployment `v1.2.3` |
| 10:15 | Rolled back to `v1.2.2` |
| 10:20 | Error rates normalized; Incident closed |

## Resolution
[Steps taken to fix the issue immediately.]

## Follow-up Actions
| Action Item | Owner | Due Date | Status |
|-------------|-------|----------|--------|
| Add memory usage limits to caching layer config | @backend-team | YYYY-MM-DD | Pending |
| Implement integration test for cache eviction logic | @qa-team | YYYY-MM-DD | Pending |
```

## Operational Considerations
*   **작성 시점:** 장애가 완전히 종료된 후, 최소 24시간 이내에 초안을 작성하는 것이 좋습니다. 너무 빠르면 감정이 개입되고, 너무 늦으면 세부 사항을 잊어버립니다.
*   **공유 범위:** 내부 기술 공유(Confluence, Notion 등)에 공개하고, 고객에게는 별도의 정제된 공지(Summary)를 전송해야 합니다.
*   **회고 미팅:** 문서 작성 후 짧은 미팅을 통해 팀원들이 이해관계를 정리하고, 액션 아이템의 현실성을 검증합니다.

## Trade-offs & Limitations
*   **시간 비용:** 철저한 회고 작성에는 상당한 시간이 소요됩니다. 모든 사소한 장애에 대해 이 양식을 적용하면 엔지니어링 리소스가 낭비될 수 있습니다. (예: Sev 3 이하의 사소한 장애는 간소화된 양식 사용)
*   **주관적 해석:** 로그가 부족한 상황에서는 엔지니어의 기억에 의존해야 하므로, 타임라인의 객관성이 떨어질 수 있습니다.
*   **액션 아이템의 방치:** 문서화만 하고 이행하지 않으면 회고는 무의미한 종이 조각이 됩니다. 반드시 프로젝트 관리 툴(Jira 등)과 연동하여 추적해야 합니다.

## Final Checklist
- [ ] 장애의 시작과 종료 시간이 명확한가?
- [ ] 근본 원인이 "사람의 실수"가 아니라 "시스템/프로세스의 결함"으로 기술되었는가?
- [ ] 영향도(Impact)가 정량적 데이터(에러율, 지연 시간 등)로 뒷받침되는가?
- [ ] 모든 Follow-up Action에 담당자와 마감기한이 지정되었는가?
- [ ] 관련 모니터링 대시보드나 로그 링크가 포함되었는가?
