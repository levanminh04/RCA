#!/bin/bash
C=/srv/rca-lab/runs/t072-e3-01-cfg; L=$C/grafana-log-sau-restart.txt
echo "--- ngalert"; grep -E 'logger=ngalert' $L | cut -c1-500
echo "--- plugin.prometheus (5 dong dau)"; grep 'logger=plugin.prometheus' $L | head -5 | cut -c1-500
echo "--- plugin.prometheus theo msg"; grep 'logger=plugin.prometheus' $L | grep -o 'msg="[^"]*"' | sort | uniq -c
echo "--- plugin.prometheus theo phut"; grep 'logger=plugin.prometheus' $L | grep -o 't=2026-11-22T05:1[0-9]:[0-9]' | sort | uniq -c
echo "--- log moi tu 05:18:46"; docker logs --since 2026-11-22T05:18:46Z flash-ticket-obs-grafana 2>&1 | grep -v -E 'plugin.prometheus|search-manifest|bleve|resource-search' | cut -c1-300 | head -20
echo "--- level moi"; docker logs --since 2026-11-22T05:18:46Z flash-ticket-obs-grafana 2>&1 | grep -o 'level=[a-z]*' | sort | uniq -c
sha256sum $L
echo "--- bo nhan"; wc -l < /srv/rca-lab/runs/t072-e3-01/webhook.jsonl; date -u +%FT%TZ
