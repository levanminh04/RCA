#!/usr/bin/env bash
set -Eeuo pipefail
trap 'rc=$?; date -u; printf "bootstrap exit %s at line %s\n" "$rc" "$LINENO"; exit "$rc"' ERR
export DEBIAN_FRONTEND=noninteractive
export NEEDRESTART_MODE=a
role=${1:?app or obs}
date -u
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y ca-certificates curl git tmux python3-venv chrony iptables-persistent
if ! command -v docker >/dev/null; then
 curl -fsSL https://get.docker.com -o /home/ubuntu/t058/get-docker.sh
 sudo sh /home/ubuntu/t058/get-docker.sh
fi
sudo usermod -aG docker ubuntu
if [ "$role" = app ]; then
 sudo apt-get install -y openjdk-21-jdk-headless maven
fi
sudo iptables -C INPUT -s 10.0.0.0/24 -j ACCEPT 2>/dev/null || sudo iptables -I INPUT 1 -s 10.0.0.0/24 -j ACCEPT
sudo netfilter-persistent save
sudo systemctl enable docker chrony netfilter-persistent
sudo docker version
sudo docker compose version
sudo docker run --rm hello-world
uname -m
free -m
df -h /
chronyc tracking
sudo iptables -S INPUT
date -u
touch /home/ubuntu/t058/bootstrap.done