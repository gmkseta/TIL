---
title: "Pragmatic implementation guide: 백엔드 장애 대응 런북 설계"
date: "2026-02-23"
update: "2026-02-23"
tags: ["auto-draft", "slack", "n8n"]
draft: true
---
# Pragmatic implementation guide: 백엔드 장애 대응 런북 설계

## Problem Definition
장애는 발생하기 마련이며, 이에 대한 대응 속도와 정확도는 시스템의 신뢰성을 좌우합니다. 많은 조직이 장애 대응 매뉴얼을 보유하고 있지만, 실제 운영 단계에서는 문서가 최신화되지 않거나 상황에 맞지 않아 무용지물이 되는 경우가 빈번합니다. 엔지니어는 긴박한 상황에서 판단을 유보하거나 잘못된 명령을 수행하여 장애 시간을 오히려 늘리기도 합니다. 본 가이드는 문서화된 지식이 아닌, 실행 가능한 형태의 런북(Runbook)을 설계하고 구현하는 방법에 초점을 맞춥니다.

## Why This Matters in Production
운영 환경에서 장애 대응 시간(MTTD, MTTR)은 곧 비용과 직결됩니다. 수동으로 로그를 뒤지거나 슬랙 메시지를 찾아 헤매는 시간은 서비스 중단 시간을 증가시키고, 고객 신뢰도를 떨어뜨립니다. 잘 설계된 런북은 온콜(On-call) 엔지니어의 인지 부하를 줄여주고, 주관적인 판단에 의한 실수를 방지합니다. 또한, 팀원 간의 대응 방식을 표준화하여 누가 대응하더라도 일관된 결과를 보장합니다.

## Architecture / Technical Approach
런북은 단순한 위키(Wiki) 페이지가 아니라, 시스템의 상태를 진단하고 자동화된 스크립트를 실행할 수 있는 접점이어야 합니다.

1. **계층적 진단 구조 (Hierarchical Diagnosis)**
   - **Level 1 (Symptom):** 알람 발생 (예: CPU 90%, Error Rate Spike).
   - **Level 2 (Check):** 자동화된 스크립트 실행 (예: `kubectl logs`, `curl health_check`).
   - **Level 3 (Action):** 사전 정의된 대응책 실행 (예: Rollout, Restart, Scale-up).

2. **런북 저장소 및 버전 관리**
   - 런북 자체를 코드로 관리합니다. (GitOps)
   - 각 런북은 시스템 컴포넌트(예: API, DB, Queue)별로 분리되어 있어야 합니다.

3. **자동화와의 통합**
   - 런북의 'Action' 단계는 Ansible, Terraform, 또는 Kubernetes Operator와 같은 도구와 연동되어 즉시 실행 가능해야 합니다.
   - 완전 자동화가 어려운 경우, 엔지니어가 실행해야 할 정확한 CLI 명령어를 제공합니다.

## Code Example

다음은 간단한 Python 기반의 런북 실행기 예시입니다. 이 스크립트는 장애 상황을 입력받아 미리 정의된 진단 및 복구 절차를 수행합니다.

```python
import subprocess
import sys
import socket
from enum import Enum

class IncidentType(Enum):
    HIGH_CPU = "high_cpu"
    DB_CONNECTION_FAIL = "db_connection_fail"
    MEMORY_LEAK = "memory_leak"

def run_command(command_args):
    """
    쉘 인젝션 방지를 위해 shell=True를 제거하고 리스트 형태의 인자를 사용합니다.
    """
    try:
        print(f"Executing: {' '.join(command_args)}")
        result = subprocess.run(command_args, check=True, capture_output=True, text=True)
        print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)
        return False
    except FileNotFoundError:
        print("Error: Command not found. Please check dependencies.")
        return False

def check_db_connectivity(host, port, timeout=5):
    """
    외부 의존성(nc) 없이 Python 내장 라이브러리(socket)를 사용하여 연결 확인.
    타임아웃을 설정하여 스크립트 멈춤 방지.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, int(port)))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Connectivity check failed: {e}")
        return False

def handle_high_cpu():
    print("[Runbook] Handling High CPU...")
    # 1. Check top processes
    run_command(["kubectl", "top", "pods", "-n", "production"])
    # 2. HPA status check
    run_command(["kubectl", "get", "hpa", "-n", "production"])
    # 3. Action: Manual intervention required if HPA is maxed
    print("[Action] Verify HPA limits. If maxed, consider scaling up manually or capping traffic.")

def handle_db_connection_fail():
    print("[Runbook] Handling DB Connection Failure...")
    
    # 환경 변수 검증 로직 추가 (실제 운영 시 os.getenv 사용 권장)
    db_host = "db.example.com" # ASSUMPTION: Placeholder for actual env var
    db_port = "5432"

    # 1. Check DB connectivity using Python socket
    if not check_db_connectivity(db_host, db_port):
        # 2. Check DB Pod status
        run_command(["kubectl", "get", "pods", "-n", "database"])
        
        # 3. Pre-check: Verify connection pool status and DB load before restart
        print("[Check] Verifying DB Max Connections and Application Connection Pool status...")
        # (실제 운영에서는 메트릭 서버 쿼리 또는 로그 분석 로직이 여기에 위치)
        
        # 4. Action: Rolling restart with safety strategy
        print("[Action] Initiating Rolling Restart of API pods to clear connection pool.")
        print("[Safety] Ensuring maxSurge and maxUnavailable settings are safe to prevent downtime.")
        
        # 안전한 롤링 업데이트를 위해 명령어 구체화 (예: 설정 확인 후 실행)
        # 실제 실행 전 Dry-run 수행 권장
        run_command(["kubectl", "rollout", "restart", "deployment/api", "-n", "production"])
    else:
        print("[Info] DB is reachable. Check application connection string.")

def main(incident_type_str):
    try:
        incident = IncidentType(incident_type_str)
    except ValueError:
        print(f"Unknown incident type: {incident_type_str}")
        sys.exit(1)

    if incident == IncidentType.HIGH_CPU:
        handle_high_cpu()
    elif incident == IncidentType.DB_CONNECTION_FAIL:
        handle_db_connection_fail()
    # Add other handlers...

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python runbook.py <incident_type>")
        sys.exit(1)
    main(sys.argv[1])
```

## Operational Considerations
런북은 작성하는 것보다 유지보수가 훨씬 어렵습니다. 다음 운영적 측면을 고려해야 합니다.

- **정기적인 드릴(Drill):** 분기별로 게임데이(Game Day)를 진행하여 런북이 실제로 작동하는지 검증합니다. 문서와 실제 환경이 다를 경우 런북을 즉시 수정합니다.
- **가독성 및 접근성:** 장애 상황에서는 PagerDuty, Slack, Opsgenie 등에서 바로 런북 링크에 접근할 수 있어야 합니다. 로그인이 필요하거나 검색이 어려운 위키는 적합하지 않습니다.
- **실행 권한 관리:** 런북에 포함된 명령어가 프로덕션 환경에 영향을 줄 수 있으므로, 실행 권한을 최소한의 원칙(Least Privilege)으로 관리해야 합니다.
- **피드백 루프:** 장애 대응 후(Post-mortem)에 런북이 도움이 되었는지, 무엇이 부족했는지를 기록하고 반영해야 합니다.

## Trade-offs & Limitations
- **자동화의 함정:** 모든 것을 자동화하려 하면 오히려 장애를 확산시킬 수 있습니다(예: 잘못된 롤백으로 DB 다운). 런북은 '가이드'이자 '보조 수단'이어야 하며, 중요한 결정에는 사람의 개입을 유지해야 합니다.
- **특수 케이스:** 런북은 정의된 시나리오에만 강력합니다. 예상치 못한 복합 장애(예: 네트워크 분단과 DB 락 동시 발생) 상황에서는 런북이 큰 도움이 되지 않을 수 있습니다.
- **유지보수 비용:** 인프라가 변경될 때마다 런북도 함께 수정되어야 합니다. 이를 코드화(Code as Infrastructure)하지 않으면 런북은 빠르게 노후화됩니다.

## Final Checklist
- [ ] 장애 유형별 명확한 트리거(Trigger)가 정의되어 있는가?
- [ ] 런북에 포함된 명령어가 현재 인프라에서 유효한가?
- [ ] 런북 실행이 시스템에 미칠 영향(부하, 잠금 등)을 고려하였는가?
- [ ] 온콜 엔지니어가 장애 발생 1분 이내에 런북을 찾을 수 있는가?
- [ ] 최근 3개월 이내에 런북을 실제로 테스트(드릴)해보았는가?
- [ ] 장애 대응 후(Post-mortem) 런북 업데이트가 이루어졌는가?
