#!/usr/bin/env bash
# Mỗi phút: nếu có ca 'M1 xong' mới thì chạy e2.py --day (chuyển, băm, chỉ mục, đẩy; KHÔNG phát lại). Dừng khi E1 xong.
cd /d/RCA-flashticket
n0=0
while true; do
  n=$(grep -c '"M1 xong"' results/T-062/chay/e1-runner.log 2>/dev/null || echo 0)
  if [ "$n" != "$n0" ]; then
    echo "$(date -u +%FT%TZ) ca M1 xong: $n" ; py -3 -B results/T-062/e2.py --day 2>&1 | tail -3; n0=$n
  fi
  grep -q '"E1 xong"' results/T-062/chay/e1-runner.log 2>/dev/null && { echo "$(date -u +%FT%TZ) E1 xong"; break; }
  [ -f D:/RCA-overnight/STOP ] && { echo STOP; break; }
  sleep 60
done
