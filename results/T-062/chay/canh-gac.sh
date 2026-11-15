#!/usr/bin/env bash
# Nhịp tim CHECKPOINT mỗi 20 phút; thoát khi E1 xong hoặc có lỗi trong nhật ký bộ chạy (để phiên điều phối xử lý).
cd /d/RCA-flashticket
L=results/T-062/chay/e1-runner.log
n0=$(grep -c 'LỖI\|DỪNG\|Traceback' $L)
while true; do
  py -3 -B -c "
import re,datetime
p='tasks/T-062-dem-chang-1-4/CHECKPOINT.md'
s=open(p,encoding='utf-8').read()
s=re.sub(r'NHIP_TIM_UTC: .*','NHIP_TIM_UTC: '+datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),s,1)
open(p,'w',encoding='utf-8').write(s)"
  for i in $(seq 1 40); do
    grep -q '"E1 xong"' $L && { echo "E1 xong $(date -u +%T)"; exit 0; }
    n=$(grep -c 'LỖI\|DỪNG\|Traceback' $L); [ "$n" != "$n0" ] && { echo "CÓ LỖI $(date -u +%T)"; grep 'LỖI\|DỪNG\|Traceback' $L | tail -3 | cut -c1-600; exit 1; }
    sleep 30
  done
done
