set -euo pipefail
date -u +%FT%TZ
echo "== 5 agent"
cd /opt/flashticket-rca/observability/collector
sudo -n docker compose -f agent-compose.yaml --env-file ../../inventory/oracle-exp.env up -d 2>&1 | tail -2
echo "== 6 VNPay gia, duong ham"
cd /opt/flashticket-rca/load/controller/support
{ echo "RECOVER=True"; cat kiem-mock.py; } | python3 - | python3 -c "import json,sys;d=json.load(sys.stdin);print({k:d[k] for k in ('pid','alive','health200','restarted')}, 'cau_hinh_khong_doi', all(d['before'][n]==d['after'][n] for n in ('mock-runner.py','mock_vnpay.py','mock.env')))"
{ echo "ACTION='start'"; cat tunnel-remote.py; } | python3 - | python3 -c "import json,sys;d=json.load(sys.stdin);print({k:d[k] for k in ('supervisorPid','alive','startedNow','sshPid')})"
sleep 8
ps -eo pid,ppid,args | grep -E "mock-runner|tunnel-supervisor|ssh .*-R" | grep -v grep | cut -c1-170
echo "== trang thai"
sudo -n docker ps --format '{{.Names}} {{.Status}}'
sudo -n docker volume ls --format '{{.Name}}'
date -u +%FT%TZ
