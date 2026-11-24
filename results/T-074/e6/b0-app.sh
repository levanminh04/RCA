# T-074 E6 bước 0 — exp-app — CHỈ ĐỌC
set -u
echo "== utc $(date -u +%FT%T.%NZ) host $(hostname)"
echo "== git"; git -C /opt/rca-lab rev-parse HEAD; echo "dirty_lines=$(git -C /opt/rca-lab status --porcelain | wc -l)"
echo "== ps"; ps -eo pid,etimes,args | grep -E 'runner4|tai_linux|chuoi_tai|inj3|_het_han|_renew|rcaburn|[k]6 |stage_m1|run_m1|xuat_bo_sung|sau_v082|safe_export|orchestrator' | grep -v -E 'grep|b0-app' || echo "(khong co)"
echo "== docker ps -a"; docker ps -a --format '{{.Names}}|{{.Image}}|{{.Status}}'
echo "== paused/running"; docker ps -aq | xargs -r docker inspect -f '{{.Name}} running={{.State.Running}} paused={{.State.Paused}} started={{.State.StartedAt}}'
echo "== inj dir"; if [ -d /home/ubuntu/t063/inj ]; then echo dir_ton_tai; ls -la /home/ubuntu/t063/inj | grep -E 'deadline|\.pid' || echo "(khong deadline/pid)"; else echo khong_co_dir; fi
echo "== toxics"; curl -s -m 5 127.0.0.1:8474/proxies | python3 -c 'import json,sys; d=json.load(sys.stdin); print({k:[t.get("name") for t in v.get("toxics",[])] for k,v in d.items()})' 2>&1
echo "== lease"; for s in booking-service event-service; do printf '%s: ' $s; sudo -n cat /opt/flash-ticket-app/rca-faults/$s/control/control.json 2>&1 | head -c 400; echo; done
echo "== cron"; crontab -l 2>&1 | head; echo "-- timers"; systemctl list-timers --all --no-pager 2>&1 | grep -iE 'rca|t06|t07|m1|tai' || echo "(khong timer khop)"
echo "== rabbit"; R=$(docker ps --format '{{.Names}}' | grep -i rabbit | head -1); echo "container=$R"; docker exec "$R" rabbitmqctl list_queues -q name messages messages_unacknowledged 2>&1 | awk 'NR==1 || $2!=0 || $3!=0' | head -40; echo "tong_hang_doi=$(docker exec "$R" rabbitmqctl list_queues -q name 2>/dev/null | tail -n +2 | wc -l)"
echo "== clock"; chronyc tracking 2>&1 | head -6
echo "== utc ket thuc $(date -u +%FT%T.%NZ)"
