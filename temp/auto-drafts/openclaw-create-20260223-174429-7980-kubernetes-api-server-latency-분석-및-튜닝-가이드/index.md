---
title: "Kubernetes API Server Latency 분석 및 튜닝 가이드"
date: "2026-02-23"
update: "2026-02-23"
tags: ["auto-draft", "slack", "n8n"]
draft: true
---
# Kubernetes API Server Latency 분석 및 튜닝 가이드

## 1. Problem Definition

클러스터 규모가 커짐에 따라 kube-apiserver의 지연 시간이 지속적으로 증가하여, 컨트롤러의 리컨실(Reconcile) 루프 지연 및 배포 실패가 발생하는 문제입니다. 특히 노드 수가 1000개 이상, 파드 수가 수만 개에 달하는 대규모 환경에서는 API Server가 병목 지점이 되어 전체 시스템의 안정성을 저해합니다. 단순히 리소스를 증설하는 것만으로는 해결되지 않으며, etcd의 성능 저하와 불필요한 Watch 트래픽이 주요 원인으로 작용합니다.

## 2. Why This Matters in Production

API Server는 쿠버네티스 제어 평면의 두뇌 역할을 하므로, 여기서 발생한 지연은 클러스터 전체에 연쇄적인 장애를 유발합니다. 예를 들어, Deployment Controller가 새로운 ReplicaSet을 생성하는 API 호출이 타임아웃되면 롤아웃이 멈추거나 무한 루프에 빠질 수 있습니다. 또한, 클라이언트(예: kubectl, CI/CD 파이프라인)에서 `kubectl get pods`와 같은 간단한 명령어조차 응답하지 않는 상황이 발생하면 운영자의 장애 대응 시간을 크게 지연시킵니다. 대규모 트래픽을 처리하는 서비스 환경에서는 API Server의 응답 속도가 곧 배포 속도와 직결되므로 비즈니스 임팩트가 큽니다.

## 3. Architecture / Technical Approach

API Server의 지연 시간을 줄이기 위해서는 크게 네 가지 영역을 분석하고 튜닝해야 합니다.

**1. etcd 성능 최적화**
API Server의 모든 상태는 etcd에 저장됩니다. etcd의 디스크 쓰기 지연(latency)과 DB 사이즈가 API Server의 응답 시간을 결정짓는 가장 큰 요인입니다. etcd는 Raft 합의 알고리즘을 사용하므로 디스크 쓰기 속도가 느려지면 리더 선출 및 커밋 지연이 발생하여 전체 API 호출이 블로킹됩니다.

**2. Watch 캐시 및 이벤트 폭주 방지**
클라이언트는 리소스 변경 사항을 감지하기 위해 Watch API를 사용합니다. 수많은 컨트롤러와 kubelet이 동시에 Watch를 요청하면 API Server의 메모리 사용량이 급증하고 CPU 부하가 높아집니다. 특정 리소스(예: Endpoints, ConfigMap)에 빈번한 업데이트가 발생하면 이벤트 폭주(Event Storm) 상황이 되어 Watch 캐시 전파가 지연됩니다.

**3. 요청 속도 제한 (Priority and Fairness)**
무분별한 API 요청은 API Server를 과부하 상태로 만듭니다. `API Priority and Fairness`(APF)를 사용하여 중요한 시스템 컴포넌트(예: kubelet, scheduler)의 요청을 우선순위에 두고, 덜 중요한 사용자 요청을 제한하여 급격한 부하 증가로부터 시스템을 보호해야 합니다.

**4. 동시 요청 처리 한도 (Inflight Requests)**
APF가 적용되기 전에 API Server 자체의 동시 처리 가능 요청 수를 제어하는 파라미터 설정이 필수적입니다. `--max-requests-inflight`와 `--max-mutating-requests-inflight` 값을 적절히 조절하여 API Server가 과부하로 인해 멈추는 것을 방지하고, etcd로 가는 gRPC 스트림 수(`--grpc-max-concurrent-streams`)를 제한하여 etcd의 과부하를 막아야 합니다.

## 4. Code Example

**1. API Server 메트릭 분석 (Prometheus Query)**
API Server의 지연 상황을 파악하기 위해 다음 PromQL 쿼리를 사용하여 P99 레이턴시를 모니터링합니다. 정확한 분위수 계산을 위해 `le` 라벨을 제외하고 합산합니다.

```promql
# API Server 요청별 P99 레이턴시 (초 단위)
histogram_quantile(0.99,
  sum(rate(apiserver_request_duration_seconds_bucket{verb!="WATCH"}[5m])) by (le, verb, resource)
)
```

만약 `verb="LIST"`나 `verb="GET"`의 지연 시간이 급격히 증가한다면 etcd 쿼리 성능이나 Watch 캐시 미스를 의심해야 합니다.

**2. etcd DB 컴팩션 및 디플래그먼트**
오래된 리비전이 쌓이면 etcd DB 사이즈가 비대해져 조회 성능이 저하됩니다. 주기적으로 컴팩션을 수행하고 디스크 공간을 회수해야 합니다. 운영 자동화 시 파싱 오류를 방지하기 위해 `jq`를 사용합니다.

```bash
# 현재 리비전 확인 및 1시간 전 리비전 계산 (jq 사용)
CURRENT_REV=$(ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  endpoint status --write-out=json | jq -r '.[0].Status.header.revision')

COMPACT_REV=$((CURRENT_REV - 1000)) # 예시: 안전하게 1000 리비전 이전으로 설정

# etcd 리비전 컴팩션
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  compact $COMPACT_REV

# 디플래그먼트 실행 (실제 디스크 공간 회수)
ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  defrag
```

**3. Priority and Fairness 구성 예시 (YAML)**
높은 리소스를 소비하는 일반 애플리케이션(예: CI/CD 파이프라인)을 제한하여 시스템 안정성을 확보하는 `FlowSchema`와 `PriorityLevelConfiguration` 예시입니다.

```yaml
apiVersion: flowcontrol.apiserver.k8s.io/v1beta3
kind: PriorityLevelConfiguration
metadata:
  name: workload-low-priority
spec:
  type: Limited
  limited:
    nominalConcurrencyShares: 10 # 낮은 값 할당으로 제한
    limitResponse:
      type: Queue
      queuing:
        queues: 4
        handSize: 3
        queueLengthLimit: 20
---
apiVersion: flowcontrol.apiserver.k8s.io/v1beta3
kind: FlowSchema
metadata:
  name: limit-ci-workloads
spec:
  priorityLevelConfiguration:
    name: workload-low-priority
  distinguisherMethod:
    type: ByUser
  rules:
  - subjects:
    - kind: ServiceAccount
      name: ci-bot
      namespace: ci-system
    resourceRules:
    - resources: ["pods", "services", "configmaps"]
      apiGroups: [""]
      verbs: ["get", "list", "create", "delete"]
```

## 5. Operational Considerations

실제 운영 환경에서는 다음 사항을 주의 깊게 모니터링해야 합니다.

*   **etcd 디스크 IOPS 모니터링:** API Server 지연 발생 시 가장 먼저 `etcd_disk_wal_fsync_duration_seconds` 메트릭을 확인하여 디스크 쓰기 성능 병목 여부를 판단해야 합니다. 클라우드 환경이라면 블록 스토리지의 프로비저닝된 IOPS가 충분한지 확인합니다.
*   **Watch Cache Hit Rate:** `apiserver_watch_cache_hits_total`과 `apiserver_watch_cache_misses_total`의 비율을 확인하여 캐시 히트율이 낮은 리소스를 식별합니다. 히트율이 낮다면 `--watch-cache-sizes` 플래그를 통해 해당 리소스의 캐시 크기를 늘려야 할 수 있습니다.
*   **Open Connections:** 너무 많은 클라이언트가 장기간 연결을 유지하면 API Server의 파일 디스크립터(FD) 한계에 도달할 수 있습니다. `apiserver_longrunning_requests` 메트릭을 통해 비정상적으로 긴 요청을 식별합니다.
*   **Inflight Requests 제한 모니터링:** `apiserver_current_inflight_requests` 메트릭을 통해 설정한 `--max-requests-inflight` 한계에 근접하는지 확인합니다. 지속적으로 한계에 도달한다면 API Server 파라미터를 조정하거나 클라이언트 요청 패턴을 제어해야 합니다.

## 6. Trade-offs & Limitations

이 접근 방식에는 명확한 트레이드오프가 존재합니다.

*   **메모리 사용량 증가:** Watch 캐시 크기를 늘리면 조회 성능은 향상되지만 kube-apiserver의 메모리 사용량이 급증합니다. 메모리 제한( Limit )을 초과하여 OOMKill이 발생하지 않도록 신중하게 튜닝해야 합니다.
*   **데이터 일관성:** Watch 캐시는 etcd의 데이터를 기반으로 하지만 약간의 지연이 발생할 수 있습니다. 강한 일관성(Strong Consistency)이 요구되는 애플리케이션에는 캐시 설정이 오히려 문제를 야기할 수 있습니다.
*   **하드웨어 의존성:** 아무리 튜닝을 해도 etcd가 구동되는 디스크의 물리적 성능 한계를 넘을 수는 없습니다. 저사양의 네트워크 스토리지(NAS 등) 위에 etcd를 구성하는 것은 치명적인 설계 오류입니다.
*   **요청 처리량 제한:** `--max-requests-inflight`를 너무 낮게 설정하면 API Server가 정상적인 트래픽도 처리하지 못해 병목 현상이 발생할 수 있습니다. 반대로 너무 높게 설정하면 etcd가 과부하로 다운될 위험이 있으므로 클러스터 규모에 맞는 적정치를 찾아야 합니다.

## 7. Final Checklist

*   [ ] etcd의 `fsync` 지연 시간이 정상 범위(10ms 이하)인지 확인했는가?
*   [ ] 주요 리소스(Deployment, Endpoints 등)의 Watch 캐시 히트율을 모니터링하고 있는가?
*   [ ] API Priority and Fairness가 활성화되어 있으며, 높은 리소스를 소비하는 워크로드를 제한하는 FlowSchema가 적용되었는가?
*   [ ] `--max-requests-inflight` 및 `--max-mutating-requests-inflight` 값이 클러스터 규모에 맞게 설정되었는가?
*   [ ] 주기적인 etcd 컴팩션 및 디플래그먼트 작업이 CronJob 등으로 자동화되어 있는가?
*   [ ] kube-apiserver의 메모리 사용량이 캐시 설정 증가 후에도 Limit 내에 안정적으로 유지되는가?
