#!/usr/bin/env bash
# Hoàn tác A2: chạy lại image cũ với compose-exp/env cũ (ghi trong ~/t062/truoc-trien-khai.json)
set -Eeuo pipefail
A=/opt/flash-ticket-app; R=/home/ubuntu/t062
for s in discovery-server user-service event-service ticket-service booking-service payment-service api-gateway; do
  img=$(python3 -c "import json;print(json.load(open('$R/truoc-trien-khai.json'))['flash-ticket-$s-$s-1'])")
  ( cd $A/compose-exp && IMAGE=$img docker compose -p flash-ticket-$s -f $s.yml up -d --force-recreate )
done
