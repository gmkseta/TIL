---
title: "Pragmatic implementation guide: 쿠버네티스 운영 장애 대응 체크리스트"
date: "2026-02-23"
update: "2026-02-23"
tags: ["auto-draft", "slack", "n8n"]
draft: true
---
# Pragmatic implementation guide: 쿠버네티스 운영 장애 대응 체크리스트

## Problem Definition
쿠버네티스 환경에서는 파드(Pod)의 순간적인 재시작부터 노드 전체의 장애, 혹은 컨트롤 플레인의 무응답까지 다양한 형태의 장애가 발생합니다. 분산 시스템의 특성상 단일 실패 지점을 찾기 어렵고, 로그가 흩어져 있어 장애 근본 원인(Root Cause) 파악에 지연이 발생합니다. 운영자가 수동으로 대응하면 인지 부하가 높아져 오판의 가능성이 커지며, 복구 시간(MTTR)이 길어집니다. 이를 해결하기 위해 체계적인 모니터링, 사전 정의된 런북(Runbook), 그리고 자동화된 대응 절차가 필수적입니다.

## Why This Matters in Production
백엔드 서비스의 SLA(서비스 수준 계약)를 준수하기 위해서는 장애 감지부터 복구까지의 시간을 최소화해야 합니다. 쿠버네티스는 자가 치유 기능을 제공하지만, 애플리케이션 레벨의 장애나 리소스 고갈 같은 시나리오에서는 기본 설정만으로는 대응이 불가능합니다. 장애 상황에서 효과적인 대응 체계가 없으면 장애 전파(Storm)로 이어져 전체 시스템의 장애로 확대될 수 있습니다. 견고한 장애 대응 체크리스트는 운영 팀의 패닉을 방지하고 시스템의 신뢰성을 보장하는 핵심 요소입니다.

## Architecture / Technical Approach
장애 대응을 위한 아키텍처는 크게 **관측성(Observability)**, **경보(Alerting)**, **자동화된 대응(Automation)** 세 가지 계층으로 구성해야 합니다.

1. **관측성 계층**: Prometheus를 사용하여 메트릭을 수집하고, Loki 혹은 ELK Stack을 통해 로그를 집계합니다. 분산 추적(Distributed Tracing, 예: Jaeger, Tempo)은 마이크로서비스 간 호출 오류를 추적하는 데 필수적입니다.
2. **경보 계층**: Alertmanager를 통해 단순한 리소스 임계치 초과뿐만 아니라, `CrashLoopBackOff`와 같은 쿠버네티스 특정 이벤트 및 사전 정의된 복합 조건(예: Error Rate 증가 + Latency 증가)을 감지합니다.
3. **대응 계층**: 경보 발생 시 OpsGenie나 PagerDuty 등의 온콜 관리 도구로 알림을 전송합니다. 심각한 장애의 경우 Argo CD나 Kubernetes Operator를 활용해 롤백(Rollback)이나 파드 재시작을 자동화합니다.

## Code Example

### 1. PodDisruptionBudget(PDB) 설정 예시
장애 상황이나 노드 업데이트 중에도 최소한의 가용성을 보장하기 위해 PDB를 설정합니다.

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: api-server-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: api-server
```

### 2. Liveness/Readiness Probe 설정 예시
비정상적인 컨테이너를 빠르게 감지하여 재시작하거나 트래픽을 제외합니다.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-worker
spec:
  template:
    spec:
      containers:
      - name: worker
        image: my-backend:latest
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
          failureThreshold: 1
```

### 3. Prometheus AlertRule 예시
`CrashLoopBackOff` 상태인 파드가 감지되었을 때 즉시 경보를 보내는 규칙입니다.

```yaml
groups:
- name: kubernetes-pods
  rules:
  - alert: PodCrashLooping
    expr: rate(kube_pod_container_status_restarts_total{namespace="production"}[15m]) > 0
    labels:
      severity: critical
    annotations:
      summary: "Pod {{ $labels.pod }} is crash looping."
      description: "Namespace: {{ $labels.namespace }}, Pod: {{ $labels.pod }} has restarted {{ $value }} times in the last 15 minutes."
```

## Operational Considerations
장애 대응 시나리오를 문서화(Runbook화)하고 정기적으로 드릴(Chaos Engineering 등)을 수행해야 합니다. 로그와 메트릭은 반드시 중앙 집중화되어야 하며, 장애 발생 시 `kubectl` 접근 권한을 신속하게 부여할 수 있는 절차(IAM)가 마련되어 있어야 합니다. 또한, 장애 복구 후에는 반드시 Post-Mortem(사후 검토)을 진행하여 재발 방지 대책을 수립해야 합니다.

## Trade-offs & Limitations
과도한 자동화는 장애를 확산시킬 수 있습니다. 예를 들어, 단순한 CPU 스파이크에 대해 파드를 강제로 재시작하면 오히려 시스템에 더 큰 부하를 줄 수 있습니다. PDB를 설정하면 클러스터 업데이트나 노드 드레인(Drain) 작업이 지연될 수 있으므로 가용성 리소스와 운영 효율성 사이의 균형이 필요합니다. 모니터링 시스템 자체의 장애(Single Point of Failure)를 방지하기 위해 Prometheus나 Alertmanager 자체의 고가용성 구성이 필요하며, 이는 운영 복잡도를 증가시킵니다.

## Final Checklist
- [ ] **리소스 제한(Request/Limit)**: 모든 컨테이너에 CPU/Memory 요청量和 제한이 설정되어 있는가?
- [ ] **Probe 설정**: Liveness와 Readiness Probe가 애플리케이션 상태를 정확히 반영하고 있는가?
- [ ] **PodDisruptionBudget**: 주요 서비스에 대해 PDB가 설정되어 최소 가용성이 보장되는가?
- [ ] **HPA/VPA**: 트래픽 급증에 대비하여 Horizontal/Autoscaler가 구성되어 있는가?
- [ ] **노드 안정성**: 노드의 Auto-scaling 그룹과 Unhealthy 노드 자체 교체 정책이 활성화되어 있는가?
- [ ] **백업 및 복구**: etcd 백업이 정기적으로 수행되고 복구 절차가 검증되었는가?
- [ ] **경보 수신**: Critical 경보가 온콜 팀에게 실시간으로 전달되는가?
- [ ] **런북 접근성**: 장애 상황별 대응 매뉴얼이 전체 팀에게 공유되어 있는가?
