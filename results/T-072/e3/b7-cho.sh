#!/bin/bash
# Laptop: chờ điều kiện thoát (điều phối 22/11): [4 luật thử có firing HOẶC quá 25 phút từ DA-PHAT] VÀ [lượt xong + 7 phút].
K=/d/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key; O=/d/RCA-flashticket/results/T-072/e3/b7-theo-doi.jsonl
T0=$(date +%s)
while true; do
  L=$(ssh -i $K -o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=/d/RCA-ext/overnight-T058/out/known_hosts ubuntu@213.35.116.128 'bash -s' < /d/RCA-flashticket/results/T-072/e3/b7-mot-lan.sh 2>&1 | tail -1)
  echo "$L" >> $O
  KQ=$(printf '%s' "$L" | py -3 -c "
import json,sys,datetime
try: o=json.loads(sys.stdin.read())
except Exception: print('loi-doc'); raise SystemExit
uids=['t072-thu-p95-booking','t072-thu-p95-event','t072-thu-p95-payment','t072-thu-p95-ticket']
c1=all(o['firing'].get(u,0)>0 for u in uids) or (o['da_phat'] and o['now']>o['da_phat']+1500)
t=o.get('tai') or {}; c2=False
if t.get('ok') and t.get('Running') is False and t.get('FinishedAt'):
    f=datetime.datetime.fromisoformat(t['FinishedAt'][:26].rstrip('Z')+'+00:00').timestamp(); c2=o['now']>=f+420
print('xong' if (c1 and c2) else 'cho')")
  [ "$KQ" = xong ] && { echo "{\"thoat\":\"du_dieu_kien\",\"utc\":\"$(date -u +%FT%TZ)\"}" >> $O; exit 0; }
  [ $(( $(date +%s) - T0 )) -gt 4500 ] && { echo "{\"thoat\":\"het_gio_75_phut\",\"utc\":\"$(date -u +%FT%TZ)\"}" >> $O; exit 2; }
  sleep 60
done
