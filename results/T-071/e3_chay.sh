#!/bin/bash
# T-071 E3 (a): một lượt ×1 1800 s t071-e3-duong-01 bằng tai_linux.py (chạy nền trên exp-obs, từ /opt/rca-lab).
# Ghi: start.json, DA-PHAT (tag + StartedAt, ngay khi container Running), get.log, DA-XONG (FinishedAt), receive.json.
# Không gọi stop thiếu --tag. Quá seconds+90+900 s vẫn chạy: stop --tag một lần, ghi CAN-CAN-THIEP, không receive.
set -u
T=t071-e3-duong-01; D=/srv/rca-lab/runs/t071-e3; TL="python3 load/controller/tai_linux.py"
mkdir -p $D; cd /opt/rca-lab
st() { python3 -c 'import json,sys; d=json.load(sys.stdin); s=d["result"]["state"] if d.get("ok") else {}; print(d.get("ok"), s.get("Running"), s.get("StartedAt"), s.get("FinishedAt"), s.get("ExitCode"), s.get("OOMKilled"))'; }
date -u +%FT%T.%NZ > $D/start-goi-utc.txt
$TL start --tag $T --seconds 1800 > $D/start.json 2>&1
for i in 1 2 3; do
  read ok run sa fa ec oom < <($TL get --tag $T | st)
  [ "$ok" = True ] && break; sleep 5
done
if [ "$ok" != True ] || [ "$run" != True ]; then echo "{\"loi\": \"khong thay container Running sau start\", \"get_ok\": \"$ok\", \"running\": \"$run\"}" > $D/LOI-START; exit 3; fi
printf '{"tag": "%s", "StartedAt": "%s", "ghi_utc": "%s"}\n' "$T" "$sa" "$(date -u +%FT%T.%NZ)" > $D/DA-PHAT.tmp && mv $D/DA-PHAT.tmp $D/DA-PHAT
han=$(( $(date +%s) + 1800 + 90 + 900 )); da_stop=0; loi=0
while :; do
  sleep 30
  read ok run sa fa ec oom < <($TL get --tag $T | st)
  echo "$(date -u +%FT%TZ) ok=$ok running=$run" >> $D/get.log
  if [ "$ok" = True ]; then
    loi=0
    [ "$run" = False ] && break
    if [ $(date +%s) -gt $han ]; then
      if [ $da_stop = 0 ]; then $TL stop --tag $T >> $D/get.log 2>&1; da_stop=$(date +%s);
      elif [ $(( $(date +%s) - da_stop )) -gt 300 ]; then echo "van Running sau stop --tag" > $D/CAN-CAN-THIEP; exit 4; fi
    fi
  else
    loi=$((loi+1)); [ $loi -ge 20 ] && { echo "20 lan get loi lien" > $D/CHUA-XAC-MINH; exit 5; }
  fi
done
printf '{"tag": "%s", "StartedAt": "%s", "FinishedAt": "%s", "ExitCode": "%s", "OOMKilled": "%s"}\n' "$T" "$sa" "$fa" "$ec" "$oom" > $D/DA-XONG
for i in 1 2 3; do $TL receive --tag $T > $D/receive.json 2>&1 && break; sleep 60; done
echo "$(date -u +%FT%TZ) xong" >> $D/get.log
