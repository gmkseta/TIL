---
title: "Kubernetes API Server Latency 분석 및 튜닝 가이드"
date: "2026-02-23"
update: "2026-02-23"
tags: ["auto-draft", "slack", "n8n"]
draft: true
---
# Kubernetes API Server Latency 분석 및 튜닝 가이드

## 1. Problem Definition

클러스터 규모가 수천 개의 노드와 수십만 개의 파드로 확장되면, Kubernetes API Server는 제어 평면(Control Plane)의 주요 병목 지점이 됩니다. API Server의 지연 시간(Latency)이 증가하면 kube-controller-manager, kube-scheduler 등의 컨트롤러 동작이 지연되고, 결과적으로 배포 속도 저하 및 클러스터 상태 동기화 불일치 문제가 발생합니다. 이는 단순히 느린 응답을 넘어, 오토스케일링 실패나 장애 복구 지연으로 이어질 수 있는 심각한 운영 이슈입니다.

## 2. Why This Matters in Production

대규모 클러스터(노드 5,000개 이상) 운영 환경에서는 API Server의 성능 저하가 시스템 전체의 가용성에 직접적인 타격을 줍니다. 예를 들어, Deployment 컨트롤러가 ReplicaSet의 상태를 확인하는 데 시간이 오래 걸리면, 롤링 업데이트 중에 원치 않는 파드 증설 현상이 발생하거나 배포가 멈춰버릴 수 있습니다. 또한, `kubectl get` 명령어나 CI/CD 파이프라인의 API 호출이 타임아웃되면 운영자는 시스템 상태를 모니터링하거나 변경 사항을 적용하는 것조차 불가능해져 "Control Plane Storm" 상태에 빠질 위험이 있습니다.

## 3. Architecture / Technical Approach

Kubernetes API Server의 성능은 크게 **네트워크 계층**, **API 처리 계층(인가/검증/준비)**, **스토리지 계층(etcd)**으로 나누어 분석해야 합니다.

*   **요청 큐 관리**: 들어오는 요청은 `MaxInFlightLimit`에 의해 제한되며, `PriorityFairness` 알고리즘에 따라 큐잉됩니다. 시스템 과부하 시 우선순위가 낮은 요청이 먼저 거부되거나 지연됩니다.
*   **캐시 전략**: etcd 조회 부하를 줄이기 위해 `Watch` 캐시와 `List` 캐시가 사용됩니다. 캐시 미스(Miss)가 빈번하면 디스크 I/O가 급증합니다.
*   **etcd I/O**: API Server의 모든 상태는 etcd에 저장됩니다. etcd의 디스크 쓰기 성능(WAL 및 DB 파일)과 네트워크 대역폭은 API Server 응답 속도의 절대적인 제약 요소입니다.

튜닝은 주로 API Server 파라미터 조정(`--max-mutating-requests-inflight`, `--watch-cache-sizes` 등)과 etcd의 디스크/네트워크 성능 최적화를 통해 이루어집니다.

## 4. Code Example

### Prometheus 쿼리를 통한 병목 지점 식별

API Server의 지연 시간을 분석할 때는 단순 평균값보다는 P99(99번째 백분위수) 지표를 확인해야 합니다. 급격한 스파이크를 놓치지 않기 위해서입니다.

```promql
# API Server 요청 지연 시간 (P99)
# 1분 단위로 집계하여 급격한 성능 저하 감지
# le 라벨을 제외하고 그룹화하여 정확한 퍼센타일 계산
histogram_quantile(0.99,
  sum(rate(apiserver_request_duration_seconds_bucket{verb=~"LIST|GET|POST|PUT|DELETE"}[5m])) by (verb, resource)
)

# etcd 디스크 쓰기 지연 시간 확인
# etcd가 병목인지 확인하는 핵심 지표
histogram_quantile(0.99,
  sum(rate(etcd_disk_wal_fsync_duration_seconds_bucket[5m]))
)
```

### kube-apiserver 설정 튜닝 (Manifest 예시)

대규모 클러스터에서 기본 설정은 종종 부족합니다. 다음은 동시 요청 처리량을 늘리고 메모리 효율성을 높이기 위한 설정 예시입니다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - name: kube-apiserver
    command:
    - kube-apiserver
    # 기본값(400)에서 증설. 쓰기 작업이 많은 클러스터 필수 조정
    - --max-mutating-requests-inflight=1000
    # 기본값(400)에서 증설. 읽기 작업 병목 완화
    - --max-requests-inflight=1600
    # 클라이언트 요청 타임아웃 설정. 너무 길게 설정하면 리소스가 해제되지 않아
    # 서버 부하가 가중될 수 있으므로 주의 필요. etcd 부하는 In-flight limit 등으로 관리.
    - --request-timeout=30s
    # 리소스별 캐시 크기 설정 (Endpoints, ConfigMaps 등 트래픽이 많은 리소스 우선)
    # 대규모 클러스터에서 메모리 효율성을 위해 특정 리소스에만 큰 캐시 할당
    - --watch-cache-sizes=events#1000,endpoints#1500,configmaps#1500
    # 기본 캐시 크기는 적절 수준으로 유지하여 메모리 낭비 방지
    - --default-watch-cache-size=400
```

## 5. Operational Considerations

*   **메트릭 기반 튜닝**: 설정 변경 전 반드시 Prometheus/Grafana 대시보드를 통해 현재 병목이 CPU, 메모리, Network, Disk 중 어디에 있는지 확인해야 합니다. 예를 들어, `etcd_disk_backend_commit_duration_seconds`가 높다면 API Server 파라미터가 아닌 etcd 디스크 성능을 점검해야 합니다.
*   **롤링 업데이트 주의**: API Server는 클러스터의 심장과 같습니다. 튜닝 적용 시 반드시 하나의 파드씩 순차적으로 롤링 업데이트를 진행하고, 업데이트 간격을 충분히 두어 etcd 리더 선출(Leader Election) 과정에서의 혼잡을 방지해야 합니다.
*   **장애 시나리오 테스트**: 부하 테스트 도구(예: Locust, k6)를 사용하여 튜닝 전후의 API 처리량(RPS)과 지연 시간을 비교 검증해야 합니다.

## 6. Trade-offs & Limitations

*   **메모리 사용량 증가**: `--watch-cache-sizes`를 통해 특정 리소스의 캐시를 늘리면 조회 성능은 향상되지만 API Server의 메모리 사용량이 증가합니다. 메모리 부족으로 인한 OOMKill 발생 시 클러스터 전체 장애로 이어질 수 있으므로 여유 리소스가 필수적입니다.
*   **데이터 일관성(Consistency) 지연**: 캐시를 적극적으로 활용하면 성능은 좋아지지만, etcd에 기록된 데이터와 API Server가 반환하는 데이터 사이에 미세한 지연이 발생할 수 있습니다. 강한 일관성이 요구되는 금융 거래 등의 워크로드에서는 주의가 필요합니다.
*   **우선순위 역전**: `PriorityFairness` 큐를 잘못 구성하면, 중요한 시스템 컴포넌트의 요청이 일반 사용자의 대량 요청에 의해 밀려나는 현상이 발생할 수 있습니다.

## 7. Final Checklist

- [ ] **현재 병목 지점 확인**: API Server의 P99 지연 시간과 etcd의 디스크 fsync 지연 시간을 비교 분석했는가?
- [ ] **In-flight Limit 조정**: 클러스터 규모에 맞춰 `--max-mutating-requests-inflight`와 `--max-requests-inflight`를 조정했는가?
- [ ] **캐시 전략 검토**: 자주 조회되는 리소스(Endpoints, ConfigMaps)의 캐시 크기를 `--watch-cache-sizes`를 통해 리소스별로 적절히 설정했는가?
- [ ] **리소스 모니터링**: 튜닝 후 API Server 파드의 CPU 및 메모리 사용량이 안정적인지 모니터링하고 있는가?
- [ ] **etcd 성능 점검**: etcd가 배포되는 노드의 디스크(IOPS) 및 네트워크 대역폭이 충분한가?
- [ ] **장애 복구 계획**: 잘못된 튜닝으로 인해 API Server가 응답하지 않을 경우, 즉시 롤백할 수 있는 절차가 준비되어 있는가?
