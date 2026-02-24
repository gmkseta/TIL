---
title: "지수 백오프를 넘어서: Kubernetes Job의 지능형 재시도 정책 설계"
date: "2026-02-24"
update: "2026-02-24"
tags: ["auto-draft", "slack", "n8n"]
draft: true
---
# 지수 백오프를 넘어서: Kubernetes Job의 지능형 재시도 정책 설계

## Problem Definition

Kubernetes Job의 기본 재시도 전략은 단순한 지수 백오프(Exponential Backoff)에 의존합니다. 이는 일시적인 네트워크 장애에는 효과적이지만, 코드 버그나 잘못된 설정으로 인한 영구적인 장애(Permanent Failure)를 구분하지 못합니다. 결과적으로 클러스터 리소스가 불필요하게 점유되고, 장애 발생 시 복구 시간이 지연됩니다. 단순 반복 재시도는 비용 효율성을 저해하고, 중요한 배치 작업의 SLA를 위협하는 요인이 됩니다.

## Why This Matters in Production

대규모 배치 처리나 AI 모델 학습 워크로드가 쿠버네티스로 이동하면서, 단순한 '재시도'를 넘어선 '효율적인 장애 처리'가 필수적이 되었습니다. 수시간이 걸리는 학습 Job이 마지막 단계에서 설정 오류로 실패했을 때, 기본 전략은 이를 무의미하게 반복 재시도하며 비용을 낭비합니다. 운영 환경에서는 장애의 유형을 판단하여 즉시 중단하거나 알림을 발생시키는 지능형 정책이 필요합니다. 이는 리소스 절약뿐만 아니라 운영자의 신속한 대응을 가능하게 합니다.

## Architecture / Technical Approach

단순 재시도를 넘어선 지능형 전략을 구축하기 위해 다음과 같은 계층적 접근이 필요합니다.

1.  **Kubernetes Native 기능 활용**: `backoffLimit`을 통해 최대 재시도 횟수를 제한하고, `activeDeadlineSeconds`로 Job의 전체 수명을 관리하여 무한 루프를 방지합니다.
2.  **Custom Controller 도입**: Kubernetes Controller를 직접 작성하거나 Kubebuilder와 같은 프레임워크를 사용하여 Job의 상태를 감시합니다. 컨트롤러는 실패한 Pod의 로그나 Exit Code, 종료 원인(Termination Reason)을 분석하여 영구 장애 여부를 판단하고, `Finalizer`를 사용하여 안전하게 Job을 종료하거나 상태를 관리합니다.
3.  **External Orchestrator 연동**: Kueue와 같은 배치 작업 관리 도구를 통합하여 클러스터 전체의 리소스 가용성에 따라 Job을 스케줄링하거나, 우선순위 기반 재시도 큐를 관리합니다.

## Code Example

다음은 `kubebuilder`를 사용하여 실패한 Job의 구체적인 조건(예: Exit Code 1 및 Error 상태)을 감지했을 때, `Finalizer`를 통해 안전하게 Job을 실패 처리하는 커스텀 컨트롤러 로직 예시입니다. 이 코드는 불필요한 전체 Pod 조회를 줄이기 위해 Informer Cache를 활용하고, RBAC 최소 권한 원칙을 따릅니다.

```go
func (r *JobReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := log.FromContext(ctx)

    var job batchv1.Job
    if err := r.Get(ctx, req.NamespacedName, &job); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    // Job이 이미 완료되었거나 실패한 경우 처리하지 않음
    if job.Status.Succeeded > 0 || job.Status.Failed >= *job.Spec.BackoffLimit {
        return ctrl.Result{}, nil
    }

    // Finalizer가 없는 경우 추가 (종료 제어를 위해)
    if !controllerutil.ContainsFinalizer(&job, r.finalizerName) {
        controllerutil.AddFinalizer(&job, r.finalizerName)
        if err := r.Update(ctx, &job); err != nil {
            return ctrl.Result{}, err
        }
        return ctrl.Result{}, nil
    }

    // 실패한 Pod 목록 조회 (Informer Cache 활용)
    var pods corev1.PodList
    if err := r.List(ctx, &pods, client.InNamespace(req.Namespace), client.MatchingLabels(job.Spec.Selector.MatchLabels)); err != nil {
        return ctrl.Result{}, err
    }

    for _, pod := range pods.Items {
        // Pod가 실패 상태인지 확인
        if pod.Status.Phase == corev1.PodFailed && len(pod.Status.ContainerStatuses) > 0 {
            state := pod.Status.ContainerStatuses[0].State.Terminated
            // Exit Code 1이면서 Reason이 'Error'인 경우 비즈니스 로직 오류로 가정 (ASSUMPTION)
            // OOMKilled 등의 리소스 문제는 제외하여 일시적 장애로 간주
            if state != nil && state.ExitCode == 1 && state.Reason == "Error" {
                log.Info("Detected permanent failure, stopping retries", "pod", pod.Name, "exitCode", state.ExitCode, "reason", state.Reason)
                
                // Job의 Status에 실패 Condition을 추가하여 강제 종료 처리
                job.Status.Conditions = append(job.Status.Conditions, batchv1.JobCondition{
                    Type:    batchv1.JobFailed,
                    Status:  corev1.ConditionTrue,
                    Reason:  "PermanentFailureDetected",
                    Message: "Job stopped due to permanent error logic",
                })
                
                // 상태 업데이트 후 Finalizer 제거 및 종료
                if err := r.Status().Update(ctx, &job); err != nil {
                    return ctrl.Result{}, err
                }
                
                controllerutil.RemoveFinalizer(&job, r.finalizerName)
                if err := r.Update(ctx, &job); err != nil {
                    return ctrl.Result{}, err
                }
                return ctrl.Result{}, nil
            }
        }
    }

    return ctrl.Result{}, nil
}
```

## Operational Considerations

지능형 재시도 정책을 운영할 때는 다음 사항을 고려해야 합니다.

*   **로그 수집 및 모니터링**: 재시도가 중단된 이유를 명확히 파악하기 위해 Pod의 로그를 중앙 집중식 로깅 시스템(예: ELK, Loki)으로 수집해야 합니다.
*   **Alerting 규칙 설정**: 단순한 재시도가 아닌 '영구 장애로 판단되어 중단된' 경우에만 Ops 팀에게 알림을 보내도록 Prometheus Alert 규칙을 세분화해야 합니다.
*   **Dead Letter Queue (DLQ)**: 재시도를 포기한 작업을 나중에 재검사하거나 수동으로 재처리하기 위해 실패한 Job의 메타데이터를 외부 큐나 데이터베이스에 저장하는 파이프라인을 구축해야 합니다.
*   **안전장치 및 승인 절차**: 잘못된 판단으로 인한 Job 중단을 방지하기 위해, 컨트롤러에 'Dry-run' 모드를 도입하거나 특정 임계값 이상의 중단이 발생할 때 운영자의 승인을 요구하는 절차를 마련해야 합니다.

## Trade-offs & Limitations

*   **운영 오버헤드**: 커스텀 컨트롤러를 직접 개발하고 운영하는 것은 추가적인 관리 부담을 줍니다. 컨트롤러 자체의 버그가 전체 배치 시스템의 가용성에 영향을 줄 수 있습니다.
*   **복잡성 증가**: 장애 유형별로 세분화된 정책을 적용할수록 로직이 복잡해지고 디버깅이 어려워집니다.
*   **API 호환성**: Kubernetes 버전 업그레이드 시 `batch` API의 필드 변경이나 동작 방식 차이로 인해 커스텀 로직이 의도치 않게 동작할 수 있는 위험이 있습니다.
*   **보안 리스크**: 커스텀 컨트롤러에 Job의 Spec이나 Status를 수정할 수 있는 권한을 부여할 때는 최소 권한 원칙(Least Privilege)을 엄격히 준수해야 합니다. 불필요한 수정 권한은 제한하여 잠재적인 보안 위협을 차단해야 합니다.

## Final Checklist

- [ ] Job에 `activeDeadlineSeconds`를 설정하여 좀비 프로세스 방지
- [ ] `backoffLimit`을 합리적인 값으로 설정하여 무한 리소스 소모 방지
- [ ] 영구 장애(Exit Code, Termination Reason, Log Pattern)를 식별하는 로직 정의
- [ ] 커스텀 컨트롤러의 고가용성(HA) 구성 검토
- [ ] 실패한 Job의 재처리(Replay) 절차 수립
- [ ] 재시도 중단 시 알림(Notification) 채널 연동
- [ ] RBAC 최소 권한 원칙 적용 및 보안 리스크 검토
