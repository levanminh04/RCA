#!/usr/bin/env bash
set -Eeuo pipefail
id rca >/dev/null 2>&1 || sudo useradd --system --create-home --home-dir /opt/flash-ticket-rca --shell /usr/sbin/nologin rca
id ledger >/dev/null 2>&1 || sudo useradd --system --create-home --home-dir /var/lib/flash-ticket-ledger --shell /usr/sbin/nologin ledger
sudo mkdir -p /opt/flash-ticket-rca /var/lib/flash-ticket-ledger
sudo tar -xzf /home/ubuntu/t058/rca-src.tgz -C /opt/flash-ticket-rca
sudo chown -R rca:rca /opt/flash-ticket-rca
sudo chmod 750 /var/lib/flash-ticket-ledger
sudo chown ledger:ledger /var/lib/flash-ticket-ledger
sudo -u ledger sh -c 'umask 077; touch /var/lib/flash-ticket-ledger/ledger.jsonl'
sudo -u rca python3 -m venv /opt/flash-ticket-rca/venv
sudo -u rca /opt/flash-ticket-rca/venv/bin/pip install -r /opt/flash-ticket-rca/results/T-044/requirements-m1.txt -c /opt/flash-ticket-rca/results/T-044/freeze-m1.txt
sudo -u rca /opt/flash-ticket-rca/venv/bin/pip check
sudo -u rca test ! -r /var/lib/flash-ticket-ledger/ledger.jsonl
date -u
touch /home/ubuntu/t058/m1-environment.done
