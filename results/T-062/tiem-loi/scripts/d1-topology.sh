#!/usr/bin/env bash
# T-062 D1: topology cố định cho cả chiến dịch (nền, lỗi, hồi phục đều đi qua đây).
#  - Toxiproxy (host network, API 127.0.0.1:8474): event-jdbc 15433→5432, booking-redis 16379→6379,
#    gateway-booking-http 18082→8082 (Booking đăng ký Eureka cổng 18082 nên chỉ Gateway (lb://) đi qua proxy;
#    Payment/Event gọi Booking trực tiếp 8082).
#  - Booking: quota CPU cố định 1.0 (cho ô CPU-BOOK), cả ba pha.
set -Eeuo pipefail
A=/opt/flash-ticket-app; R=/home/ubuntu/t062; T=$A/rca-toxiproxy
sudo install -d -o ubuntu -g ubuntu $T
cat > $T/proxies.json <<'J'
[
 {"name":"event-jdbc","listen":"127.0.0.1:15433","upstream":"127.0.0.1:5432","enabled":true},
 {"name":"booking-redis","listen":"127.0.0.1:16379","upstream":"127.0.0.1:6379","enabled":true},
 {"name":"gateway-booking-http","listen":"127.0.0.1:18082","upstream":"127.0.0.1:8082","enabled":true}
]
J
chmod 0644 $T/proxies.json
if ! docker ps --format '{{.Names}}' | grep -qx rca-toxiproxy; then
  docker run -d --name rca-toxiproxy --network host --restart unless-stopped --read-only --cap-drop ALL \
    --security-opt no-new-privileges:true --memory 128m --label t062=topology \
    -v $T/proxies.json:/config/proxies.json:ro ghcr.io/shopify/toxiproxy:2.12.0 \
    -host=127.0.0.1 -port=8474 -config=/config/proxies.json
fi
for i in $(seq 1 20); do curl -sf http://127.0.0.1:8474/proxies >/dev/null && break; sleep 1; done
curl -s http://127.0.0.1:8474/proxies | python3 -c 'import sys,json;print({k:(v["listen"],v["upstream"],v["enabled"]) for k,v in json.load(sys.stdin).items()})'
docker image inspect ghcr.io/shopify/toxiproxy:2.12.0 --format 'toxiproxy {{.Id}} {{.Architecture}} {{json .RepoDigests}}'
# env: đổi đích qua proxy (chỉ cổng/host, không đụng mật khẩu)
E=$A/env-t062
sed -i 's#^EVENT_DB_URL=jdbc:postgresql://127.0.0.1:5432/#EVENT_DB_URL=jdbc:postgresql://127.0.0.1:15433/#' $E/event-service.env
grep -q '^EVENT_DB_URL=jdbc:postgresql://127.0.0.1:15433/' $E/event-service.env
sed -i 's#^REDIS_PORT=6379$#REDIS_PORT=16379#' $E/booking-service.env
grep -q '^REDIS_PORT=16379$' $E/booking-service.env
grep -q '^EUREKA_INSTANCE_NONSECUREPORT=' $E/booking-service.env || echo 'EUREKA_INSTANCE_NONSECUREPORT=18082' >> $E/booking-service.env
grep -q 'cpus:' $A/compose-t062/booking-service.yml || sed -i 's#^    mem_limit: 1g#    mem_limit: 1g\n    cpus: 1.0#' $A/compose-t062/booking-service.yml
grep -q 'cpus: 1.0' $A/compose-t062/booking-service.yml
sha256sum $E/event-service.env $E/booking-service.env $A/compose-t062/booking-service.yml
