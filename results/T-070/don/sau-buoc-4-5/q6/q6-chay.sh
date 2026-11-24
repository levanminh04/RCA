set -euo pipefail
OUT=/srv/flashticket-rca/runs/2026-11-24-kiem-online-dev
test ! -e $OUT
install -d -m 700 $OUT
sudo -n test ! -e /srv/flashticket-rca/rca/results/online-dev-001
cd /opt/flashticket-rca
git rev-parse HEAD > $OUT/lab-commit.txt
RCA_ONLINE_OUT=$OUT RCA_M1_ROOT=/srv/flashticket-rca/rca/online-dev setsid nohup python3 -B rca/online/orchestrator.py mot --t 1795071679 \
  --ra /srv/flashticket-rca/rca/results/online-dev-001 \
  --dev-capture /srv/flashticket-rca/rca/online-dev/sim-capture/2d5a56fe \
  --dev-prom /srv/flashticket-rca/rca/cases/2d5a56fe/prometheus.json \
  --dev-bo-sung /srv/flashticket-rca/rca/bo-sung/2d5a56fe/prometheus-bo-sung.json > $OUT/orchestrator.out 2>&1 < /dev/null &
sleep 2; pgrep -af "orchestrator.py mot" | cut -c1-120; date -u +%FT%TZ
