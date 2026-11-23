#!/bin/bash
set -e
cd /opt/rca-lab
echo "truoc=$(git rev-parse HEAD) $(date -u +%FT%TZ)"
test -z "$(git status --porcelain)" || { echo "CAY BAN"; exit 2; }
if pgrep -af "chuoi_tai|runner4|tai_linux|stage_b|orchestrator|inj3|xuat_chuoi|webhook_receiver" | grep -v pgrep; then echo "CO JOB"; exit 3; fi
git fetch origin t070-e3 2>&1 | tail -1
G=$(git rev-parse FETCH_HEAD); echo "fetch_head=$G"
case $G in ecdeed2*) ;; *) echo "FETCH_HEAD khac ecdeed2"; exit 4;; esac
test "$(git rev-parse $G^)" = d6772444e0177a2bee484e6fc79ebc32182524c5 || { echo "cha khac d677244"; exit 5; }
echo "--- diff d677244..G"; git diff --name-status d677244 $G
git show $G:observability/grafana/provisioning/alerting/t072-thu-e3-go.yaml | sha256sum
git checkout --quiet $G
echo "sau=$(git rev-parse HEAD) $(date -u +%FT%TZ) sach=[$(git status --porcelain)]"
ls observability/grafana/provisioning/alerting/
