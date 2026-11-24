# T-074 E6 bước 0 — exp-obs (+ máy tải qua khóa bộ điều khiển) — CHỈ ĐỌC
set -u
echo "== utc $(date -u +%FT%T.%NZ) host $(hostname)"
echo "== git"; git -C /opt/rca-lab rev-parse HEAD; echo "dirty_lines=$(git -C /opt/rca-lab status --porcelain | wc -l)"
echo "== STOP"; for f in /srv/rca-lab/runs/STOP /srv/rca-lab/load-controller/STOP; do [ -e $f ] && echo "CO $f" || echo "khong $f"; done
echo "== ps"; ps -eo pid,etimes,args | grep -E 'runner4|tai_linux|chuoi_tai|[k]6 |stage_m1|run_m1|xuat_bo_sung|sau_v082|safe_export|orchestrator' | grep -v -E 'grep|b0-obs' || echo "(khong co)"
echo "== docker ps -a"; docker ps -a --format '{{.Names}}|{{.Image}}|{{.Status}}'
echo "== compose ls"; docker compose ls -a 2>&1
echo "== cron"; crontab -l 2>&1 | head; echo "-- timers"; systemctl list-timers --all --no-pager 2>&1 | grep -iE 'rca|t06|t07|m1|tai' || echo "(khong timer khop)"
echo "== clock"; chronyc tracking 2>&1 | head -6
echo "== MAY TAI"
K=/etc/rca-lab/controller; T=$(python3 -c "import sys; sys.path.insert(0,'/opt/rca-lab'); from campaigns.lib import inventory; print(inventory.public_ip('load-generator'))" 2>&1)
echo "tai_ip=$T"
sudo -n ssh -i $K/id_ed25519 -o BatchMode=yes -o IdentitiesOnly=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=yes -o UserKnownHostsFile=$K/known_hosts ubuntu@$T 'echo "utc $(date -u +%FT%T.%NZ) host $(hostname)"; echo "-- rca-tai dang chay:"; sudo -n docker ps --filter name=rca-tai- --format "{{.Names}}|{{.Status}}"; echo "-- rca-tai tong (ps -a): $(sudo -n docker ps -a -q --filter name=rca-tai- | wc -l)"; echo "-- k6 ps:"; ps -eo pid,args | grep -E "[k]6 " || echo "(khong)"; echo "-- cron:"; crontab -l 2>&1 | head -3; echo "-- images k6:"; sudo -n docker images --format "{{.Repository}}:{{.Tag}}|{{.ID}}" | grep -i k6; echo "-- clock:"; chronyc tracking 2>&1 | head -4' 2>&1
echo "== utc ket thuc $(date -u +%FT%T.%NZ)"
