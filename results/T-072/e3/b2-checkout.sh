#!/bin/bash
set -e
cd /opt/rca-lab
echo "truoc=$(git rev-parse HEAD) $(date -u +%FT%TZ)"
test -z "$(git status --porcelain)" || { echo "CAY BAN - dung"; exit 2; }
if pgrep -af "chuoi_tai|runner4|tai_linux|stage_b|orchestrator|inj3|xuat_chuoi" | grep -v pgrep; then echo "CO JOB - dung"; exit 3; fi
git fetch origin t070-e3 2>&1 | tail -2
test "$(git rev-parse FETCH_HEAD)" = d6772444e0177a2bee484e6fc79ebc32182524c5 || { echo "FETCH_HEAD lech: $(git rev-parse FETCH_HEAD)"; exit 4; }
git checkout --quiet d6772444e0177a2bee484e6fc79ebc32182524c5
echo "sau=$(git rev-parse HEAD) $(date -u +%FT%TZ)"
echo "sach=[$(git status --porcelain)]"
git diff --stat e9a0857 HEAD | tail -1
ls -la observability/grafana/provisioning/alerting observability/t072-bo-nhan observability/compose.t073-webhook.yaml
sha256sum observability/grafana/provisioning/alerting/* observability/t072-bo-nhan/bo_nhan.py
