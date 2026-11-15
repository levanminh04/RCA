set -euo pipefail
date -u --iso-8601=seconds
test ! -e /opt/rca-tai
dpkg-query -W docker.io docker-ce containerd runc 2>/dev/null || true
sudo -n install -d -m 0755 -o ubuntu -g ubuntu /opt/rca-tai
mkdir -p /opt/rca-tai/k6 /opt/rca-tai/out
install -d -m 0700 /opt/rca-tai/secret
sudo -n apt-get update -qq
sudo -n env DEBIAN_FRONTEND=noninteractive apt-get install -y ca-certificates curl chrony
sudo -n install -m 0755 -d /etc/apt/keyrings
sudo -n curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo -n chmod a+r /etc/apt/keyrings/docker.asc
. /etc/os-release
printf 'Types: deb\nURIs: https://download.docker.com/linux/ubuntu\nSuites: %s\nComponents: stable\nArchitectures: %s\nSigned-By: /etc/apt/keyrings/docker.asc\n' "$VERSION_CODENAME" "$(dpkg --print-architecture)" | sudo -n tee /etc/apt/sources.list.d/docker.sources
sudo -n apt-get update -qq
sudo -n env DEBIAN_FRONTEND=noninteractive apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo -n systemctl enable --now docker chrony
sudo -n docker pull grafana/k6:1.4.2
sudo -n docker image inspect grafana/k6:1.4.2 --format '{{json .RepoDigests}} {{.Architecture}} {{.Size}}'
sudo -n docker version
chronyc tracking
timedatectl show -p NTPSynchronized
date -u --iso-8601=seconds
