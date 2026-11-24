# T-074 E6 v2 — bước 0 làm lại khi nhận S5 (CHỈ ĐỌC). Cùng một bộ lọc tiến trình cho cả ba máy (CX-39b).
# exp-app: bash -s < b0-v2.sh app ; exp-obs: bash -s < b0-v2.sh obs (phần máy tải chạy qua khóa bộ điều khiển)
set -u
MAY=${1:-app}
CAM='runner4|tai_linux|chuoi_tai|inj3|_het_han|_renew|rcaburn|stage_m1|run_m1|xuat_bo_sung|sau_v082|safe_export|orchestrator|k6 run|/usr/bin/k6'
echo "== utc $(date -u +%FT%T.%NZ) host $(hostname) may=$MAY"
echo "== git"; git -C /opt/rca-lab rev-parse HEAD 2>&1; echo "dirty_lines=$(git -C /opt/rca-lab status --porcelain 2>&1 | wc -l)"
echo "== tien trinh cam (toan may, co doi so; loai chinh lenh do nay)"
ps -eo pid=,args= | awk -v me=$$ '$1!=me' | grep -E "$CAM" | grep -vE 'grep|b0-v2' || echo "(khong co)"
echo "== docker ps -a (ten|trang thai)"; docker ps -a --format '{{.Names}}|{{.State}}|{{.Status}}' 2>&1
if [ "$MAY" = obs ]; then
  echo "== STOP"; for f in /srv/rca-lab/runs/STOP /srv/rca-lab/load-controller/STOP; do [ -e $f ] && echo "CO $f" || echo "khong $f"; done
  echo "== compose ls"; docker compose ls -a 2>&1
  K=/etc/rca-lab/controller; T=$(python3 -c "import sys; sys.path.insert(0,'/opt/rca-lab'); from campaigns.lib import inventory; print(inventory.public_ip('load-generator'))")
  echo "== MAY TAI $T"
  sudo -n ssh -i $K/id_ed25519 -o BatchMode=yes -o IdentitiesOnly=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=yes -o UserKnownHostsFile=$K/known_hosts ubuntu@$T "CAM='$CAM'; "'echo "utc $(date -u +%FT%T.%NZ)"; echo "-- rca-tai theo trang thai:"; sudo -n docker ps -a --filter name=rca-tai- --format "{{.State}}" | sort | uniq -c; echo "-- tien trinh cam:"; ps -eo pid=,args= | grep -E "$CAM" | grep -v grep || echo "(khong co)"; crontab -l 2>&1 | head -3' 2>&1
fi
if [ "$MAY" = app ]; then
  echo "== inj"; if [ -d /home/ubuntu/t063/inj ]; then ls /home/ubuntu/t063/inj | grep -E 'deadline|\.pid$' || echo "(khong deadline/pid)"; else echo khong_co_dir; fi
  echo "== paused"; docker ps -aq | xargs -r docker inspect -f '{{.Name}} paused={{.State.Paused}} running={{.State.Running}}'
  echo "== toxics"; curl -s -m 5 127.0.0.1:8474/proxies | python3 -c 'import json,sys; d=json.load(sys.stdin); print({k:[t.get("name") for t in v.get("toxics",[])] for k,v in d.items()})' 2>&1
  echo "== lease"; for s in booking-service event-service; do printf '%s: ' $s; sudo -n cat /opt/flash-ticket-app/rca-faults/$s/control/control.json 2>&1 | head -c 300; echo; done
fi
echo "== cron"; crontab -l 2>&1 | head -3; systemctl list-timers --all --no-pager 2>&1 | grep -iE 'rca|t06|t07|m1|tai' || echo "(khong timer khop)"
echo "== utc ket thuc $(date -u +%FT%T.%NZ)"
