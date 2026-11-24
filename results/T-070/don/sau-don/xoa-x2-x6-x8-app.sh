set -uo pipefail
date -u +%FT%TZ
echo "== X2 checkout cu"
for d in api-gateway booking-service discovery-server event-service keycloak payment-service t062-6b21ed5 t062-ac33155 t063-h3 t067-dc-640dbaf9 t067-dc-bb84d64f ticket-service user-service; do
  p=/opt/flash-ticket-build/$d
  if git -C /opt/flashticket/src worktree remove --force $p 2>/dev/null; then echo "worktree remove $d"; else sudo -n rm -rf -- "$p" && echo "rm -rf $d (worktree hong)"; fi
done
git -C /opt/flashticket/src worktree prune
sudo -n rmdir /opt/flash-ticket-build && echo "rmdir /opt/flash-ticket-build"
git -C /opt/flashticket/src worktree list
echo "== X3"; sudo -n docker rm rca-toxiproxy-cu
echo "== X4"; sudo -n docker volume rm 6360e5cb962dc8075aa003b4030c6272b9eefbf2a2ca7644b49c6ddf4913f8d4
echo "== X8"; sudo -n docker volume rm ft-init-verify-data
echo "== X5 image khong dung"
dung=$(for c in $(sudo -n docker ps -aq); do sudo -n docker inspect $c --format '{{.Image}}'; done | sort -u)
tat=$(sudo -n docker images -q --no-trunc | sort -u)
xoa=$(comm -23 <(echo "$tat") <(echo "$dung"))
n=$(echo "$xoa" | grep -c .); echo "so image se xoa: $n"
if [ "$n" = 25 ]; then for i in $xoa; do sudo -n docker rmi -f $i >/dev/null 2>&1 || echo "LOI rmi $i"; done; echo "da xoa 25"; else echo "DUNG: so image khac 25"; fi
echo "== X6 build cache"; sudo -n docker builder prune -a -f | tail -1
echo "== sau xoa"
sudo -n docker ps -a --format '{{.Names}} {{.Status}}'
sudo -n docker volume ls --format '{{.Name}}'
sudo -n docker images --format '{{.Repository}}:{{.Tag}}'
sudo -n docker system df
df -h / | tail -1
date -u +%FT%TZ
