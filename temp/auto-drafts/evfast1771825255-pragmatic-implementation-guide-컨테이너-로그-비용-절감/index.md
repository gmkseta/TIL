---
title: "Pragmatic implementation guide: 컨테이너 로그 비용 절감"
date: "2026-02-23"
update: "2026-02-23"
tags: ["auto-draft", "slack", "n8n"]
draft: true
---
# Pragmatic implementation guide: 컨테이너 로그 비용 절감

## Problem Definition
마이크로서비스로 전환하면서 컨테이너 로그의 양이 기하급수적으로 증가하여 클라우드 로그 스토리지 비용이 예산을 초과하는 문제가 발생합니다. 디버깅용 `DEBUG` 레벨 로그가 운영 환경에 그대로 남아 있고, 애플리케이션 로그 외에도 인프라 메타데이터가 로그에 포함되어 스토리지 효율을 떨어뜨립니다. 단순히 로그를 삭제하는 것은 장애 대응 능력을 저하시키므로, 비용 절감과 운영 효율 사이의 균형이 필요합니다.

## Why This Matters in Production
로그 비용은 단순한 스토리지 비용을 넘어, 로그 수집 및 인덱싱을 위한 컴퓨팅 리소스 비용으로 직결됩니다. 불필요한 로그는 네트워크 대역폭을 소모하고, 로그 분석 시스템(Elasticsearch, Loki 등)의 부하를 높여 장애 발생 시 분석 속도를 지연시킵니다. 특히, 금융이나 보안이 중요한 도메인에서는 로그 보관 주기가 길어야 하므로, 초기에 로그 최적화 전략을 수립하지 않으면 비용이 통제 불가능해집니다.

## Architecture / Technical Approach

로그 비용 절감을 위해서는 **생성 단계**, **수집 단계**, **저장 단계**의 3단계 접근이 필요합니다.

1.  **생성 단계 (Application Level)**
    *   **Log Level Control:** 운영 환경에서는 `INFO` 또는 `WARN` 이상의 로그만 출력하도록 설정합니다. `DEBUG` 로그는 개발/스테이징 환경으로 제한합니다.
    *   **Structured Logging:** JSON 포맷을 사용하여 로그를 구조화합니다. 이는 파싱 비용을 줄이고, 불필요한 자유 텍스트를 줄이는 데 도움이 됩니다.
    *   **Sampling:** 트래픽이 많은 엔드포인트의 경우 요청의 일부(예: 1%)만 로그를 남기는 샘플링 전략을 적용합니다.

2.  **수집 단계 (Agent/Shipper Level)**
    *   **Filtering & Dropping:** Fluentd나 Fluent Bit 같은 로그 수집 에이전트에서 특정 패턴(예: 헬스 체크 요청, `/healthz`)을 가진 로그를 즉시 폐기(drop)합니다.
    *   **Kubernetes Metadata Pruning:** `kubectl logs` 시에는 필요하지만, 로그 수집 시에는 불필요한 라벨이나 어노테이션 정보를 제거하여 로그 페이로드 크기를 줄입니다.

3.  **저장 단계 (Storage Backend)**
    *   **Tiered Storage:** 데이터 수명 주기(ILM) 정책을 통해 최근 데이터(핫 데이터)는 빠른 검색이 가능한 상태로 유지하고, 오래된 데이터(콜드 데이터)는 비용이 저렴한 오브젝트 스토리지(S3, GCS)로 이동하거나 인덱스를 닫아 저장 비용을 최적화합니다.
    *   **Compression:** 로그 전송 및 저장 시 Gzip 또는 Zstd 압축을 사용합니다.

## Code Example

### 1. Logback (Java) Configuration for Production
운영 환경에서는 `INFO` 레벨로 설정하고, 불필요한 로거는 비활성화합니다.

```xml
<configuration>
    <!-- 운영 환경 프로파일 적용 시 -->
    <springProfile name="prod">
        <root level="INFO">
            <appender-ref ref="JSON_CONSOLE" />
        </root>
        
        <!-- 불필요한 프레임워크 로그 비활성화 -->
        <logger name="org.springframework.web.servlet.DispatcherServlet" level="WARN"/>
        <logger name="org.hibernate.SQL" level="WARN"/>
    </springProfile>
</configuration>
```

### 2. Fluent Bit Config for Dropping Health Check Logs
JSON 파싱 후 `uri` 필드를 기준으로 `/healthz` 또는 `/readiness` 요청 로그를 버립니다. 프로덕션 환경을 고려하여 메모리 버퍼를 늘리고 디스크 버퍼를 설정합니다.

```ini
[INPUT]
    Name tail
    Path /var/log/containers/*.log
    Parser json
    Tag kube.*
    Mem_Buf_Limit 50MB
    Skip_Long_Lines On
    # 데이터 유실 방지를 위해 디스크 버퍼 활성화
    storage.type filesystem
    storage.path /var/log/flb-storage/
    storage.max_chunks_up 128
    storage.sync normal

[FILTER]
    Name modify
    Match kube.*
    # PII(개인정보)가 포함될 수 있는 필드 마스킹 처리
    Mask credit_card *******
    Mask ssn *********

[FILTER]
    Name grep
    Match kube.*
    # JSON 파싱 후 파싱된 필드(uri)를 기준으로 필터링
    Exclude uri /healthz
    Exclude uri /readiness

[OUTPUT]
    Name s3
    Match kube.*
    bucket my-log-bucket
    region us-east-1
    compress gzip
    total_file_size 100M
```

## Operational Considerations

*   **Log Retention Policy:** 법적 요구사항과 장애 복구 시점(RPO/RTO)을 고려하여 보관 주기를 정의합니다. 예: 7일 인덱싱, 30일 압축 저장, 90일 삭제.
*   **Alerting on Log Volume:** 로그 발생량이 급증하는 경우(예: 로직 오류로 인한 무한 루프 로그)를 감지하기 위해 로그 스토리지 사용량 모니터링을 설정합니다.
*   **Redaction:** 비용 절감과 별개로, 개인정보(PII)가 포함된 로그는 마스킹 처리해야 합니다. 로그 생성 시점에 처리하는 것이 가장 좋지만, 수집 에이전트(Fluent Bit의 `modify` 필터 등)를 통해 필드 레벨에서 마스킹 처리를 수행할 수도 있습니다. 이는 파싱 오류를 줄이고 스토리지 낭비를 막는 데도 기여합니다.
*   **Failure Scenario:** 로그 수집 에이전트(Fluent Bit)가 다운되면 노드의 디스크 공간이 가득 차서 컨테이너가 `CrashLoopBackOff` 상태에 빠질 수 있습니다. 반드시 로그 로테이션과 디스크 사용량 리밋을 설정해야 합니다.

## Trade-offs & Limitations

*   **Debugging Difficulty:** `DEBUG` 로그를 끄면 운영 환경에서 발생하는 미세한 버그를 추적하기 어려워집니다. 이를 해결하기 위해 **Dynamic Log Level** 변경 기능(예: Spring Boot Actuator, Logback JMX)을 도입하여 특정 파드에만 일시적으로 디버그 로그를 활성화하는 기능을 준비해야 합니다.
*   **Sampling Risks:** 로그 샘플링을 적용하면 드물게 발생하는 에러를 놓칠 수 있습니다. 에러 로그는 샘플링 대상에서 제외하거나 별도의 에러 트래킹 시스템(Sentry 등)과 연동해야 합니다.
*   **Parsing Overhead:** 구조화된 로그(JSON)는 가독성은 좋지만, 텍스트 로그보다 용량이 클 수 있습니다. 네트워크 비용보다 파싱 비용이 더 중요한지 상황에 따라 판단해야 합니다.

## Final Checklist

- [ ] 운영 환경 애플리케이션 로그 레벨이 `INFO` 또는 `WARN` 이상인가?
- [ ] 헬스 체크 등 무의미한 로그를 수집 에이전트 레벨에서 필터링하고 있는가?
- [ ] 로그를 JSON 등 구조화된 포맷으로 출력하고 있는가?
- [ ] 오래된 로그에 대해 저렴한 오브젝트 스토리지(S3, GCS)로 이동하는 정책(ILM)이 있는가?
- [ ] 로그 압축(Gzip)을 사용하여 네트워크 및 스토리지 비용을 절감하고 있는가?
- [ ] 장애 상황에서 동적으로 로그 레벨을 조절할 수 있는 Runbook이 준비되어 있는가?
