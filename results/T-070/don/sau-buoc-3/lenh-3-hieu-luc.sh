set -euo pipefail
cd /opt/flashticket-rca && git fetch -q origin && git checkout -q --detach 85ace52d304712303097ca0f99faa16f0b52805c && git rev-parse HEAD && git status --short | head -3
git -C /opt/flashticket/src worktree repair /opt/flashticket/build/36a3725d 2>&1 | tail -2 || true
git -C /opt/flashticket/build/36a3725d rev-parse HEAD; git -C /opt/flashticket/build/36a3725d status --short | head -3
git -C /opt/flashticket/src worktree list | grep 36a3725d
cd /opt/flashticket-rca/test-environment/scripts
sudo -n python3 hieu_luc.py --worktree /opt/flashticket/build/36a3725d --overrides /opt/flashticket-rca/test-environment/overrides \
  --out /opt/flashticket/compose --image-tag arm64-t067-36a3725d --service-version 36a3725d9b201e868f9e2e18d1c07180a12502df \
  --env-dir /opt/flashticket/env --fault-dir /srv/flashticket-rca/faults --secrets-dir /opt/flashticket/secrets \
  --ngrok-env /etc/flashticket-rca/payment-ngrok-gia.env | tail -3
sudo -n chown ubuntu:ubuntu /opt/flashticket/compose/*
ls -la /opt/flashticket/compose
echo "== so voi bo T-067 (sau khi thay duong cu -> moi trong ban cu)"
for s in discovery-server api-gateway user-service event-service ticket-service booking-service payment-service; do
  if diff <(sed -e 's#/opt/flash-ticket-app/env-t062#/opt/flashticket/env#g' -e 's#/opt/flash-ticket-app/rca-faults#/srv/flashticket-rca/faults#g' \
               -e 's#/opt/flash-ticket-app/secrets#/opt/flashticket/secrets#g' -e 's#/opt/flash-ticket-build/t067-36a3725d#/opt/flashticket/build/36a3725d#g' \
               -e 's#/etc/rca-lab#/etc/flashticket-rca#g' -e 's#/opt/rca-lab#/opt/flashticket-rca#g' \
               /opt/flash-ticket-build/t067-compose/hieu-luc/$s.yml) /opt/flashticket/compose/$s.yml > /tmp/d-$s.txt; then echo "$s: trung (chi khac duong dan)"; else echo "$s: KHAC"; head -20 /tmp/d-$s.txt; fi
done
grep -h "/opt/\|/srv/\|/etc/" /opt/flashticket/compose/event-service.yml | sort -u
