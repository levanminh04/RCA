#!/usr/bin/env bash
# Chờ Codex hồi lượt (thông báo: "try again at 1:05 PM" giờ VN = 06:05Z 12/11) rồi phát lại lượt kiểm Grafana thật bản đang chạy.
until [ "$(date -u +%s)" -ge "$(date -u -d '2026-11-12T06:10:00Z' +%s)" ]; do
  [ -f D:/RCA-overnight/STOP ] && { echo STOP; exit 0; }
  sleep 60
done
cd /d/RCA-flashticket
powershell -NoProfile -Command "Set-Location D:\RCA-flashticket; Get-Content results\T-062\codex\G1-that-2-brief.md -Raw | codex exec -C D:\RCA-flashticket --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox -m gpt-6.1-sol -c model_reasoning_effort=high -o results\T-062\codex\G1-that-2-ketqua.md - *> results\T-062\codex\G1-that-2.log"
echo "codex xong $(date -u +%T)"; head -1 results/T-062/codex/G1-that-2-ketqua.md
