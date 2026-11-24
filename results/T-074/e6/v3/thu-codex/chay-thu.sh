#!/usr/bin/env bash
# Chạy từ bất kỳ thư mục nào. Chỉ in ra stdout, kể cả khi chạy lại.
set -eu -o pipefail
thu=$(cd "$(dirname "$0")" && pwd)
v3=$(dirname "$thu")
export PATH="$thu/bin:$PATH"
[[ $(command -v docker) = "$thu/bin/docker" ]] || exit 90
for script in b1c-yen.sh b0.sh; do
  bash -n "$v3/$script"
  echo "bash -n $script: DAT"
done
n=0
loi=0
thu_ca() {
  local ca=$1 mode=$2 phut=$3 expect=$4 rc=0 ok=1 out marker
  shift 4
  local -a cmd
  if [[ $mode = yen ]]; then
    cmd=(bash "$v3/b1c-yen.sh")
    if [[ $phut != - ]]; then cmd+=(--phut-khong-tai "$phut"); fi
  else
    cmd=(bash -s -- "$mode")
  fi
  out=$(CA="$ca" MAY_GIA="$mode" BASH_ENV="$thu/gia-lap.sh" "${cmd[@]}" < "$v3/b0.sh" 2>&1) || rc=$?
  printf '\n=== %s / %s / phút=%s ===\n%s\nrc=%s\n' "$ca" "$mode" "$phut" "$out" "$rc"
  [[ $rc = "$expect" ]] || ok=0
  for marker do
    if [[ $out != *"$marker"* ]]; then echo "Thiếu: $marker"; ok=0; fi
  done
  if [[ $mode = yen && $expect != 0 && $'\n'$out$'\n' = *$'\nYEN\n'* ]]; then ok=0; fi
  if [[ $mode != yen && ( $out = *tu-do.js* || $out = *'900001 '* ) ]]; then ok=0; fi
  if [[ $expect = 0 && $out = *LOI_THU_THAP* ]]; then ok=0; fi
  if [[ $ca = *-ps-loi || $ca = ps-rong ]]; then
    # Máy obs có thể đã báo rỗng hợp lệ trước khi ps trên máy tải lỗi.
    local cuoi=${out##*'== tien trinh cam'}
    [[ $cuoi != *'(khong co)'* ]] || ok=0
  fi
  n=$((n+1))
  if (( ok )); then echo DAT; else echo SAI; loi=$((loi+1)); fi
}
thu_ca sach yen 10 0 'don|CHUA_KET_THUC|0' 'don|COMPLETED|7' 'held=0 purchased=7' \
  'outbox_chua_gui|event_db|0' 'outbox_chua_gui|booking_db|0' 'outbox_chua_gui|ticket_db|0' \
  'outbox_chua_gui|payment_db|0' 'queue_so=1 queue_khac_0=0' $'\nYEN'
thu_ca chua-ro-phut yen - 2 'Người trực đối chiếu'
thu_ca chua-10-phut yen 9 1 KHONG_YEN
thu_ca don-loi yen 10 3 'LOI_THU_THAP booking_db / don'
thu_ca don-thieu yen 10 2 'thiếu kết quả theo trạng thái'
thu_ca don-ban yen 10 1 'don|ISSUING|1' 'don|PENDING_PAYMENT|2' 'don|CHUA_KET_THUC|3' KHONG_YEN
thu_ca kho-thieu yen 10 2 'LOI_THU_THAP kho'
thu_ca kho-ban yen 10 1 'held=2 purchased=7' KHONG_YEN
thu_ca bang-thieu yen 10 3 'does not exist' 'LOI_THU_THAP ticket_db / outbox'
thu_ca outbox-thieu yen 10 2 'LOI_THU_THAP payment_db'
thu_ca outbox-sai yen 10 2 'LOI_THU_THAP booking_db'
thu_ca outbox-ban yen 10 1 'outbox_chua_gui|event_db|2' KHONG_YEN
thu_ca rabbit-loi yen 10 1 'LOI_THU_THAP rabbitmqctl'
thu_ca rabbit-thieu yen 10 2 'LOI_THU_THAP RabbitMQ'
thu_ca rabbit-sai yen 10 2 'LOI_THU_THAP RabbitMQ'
thu_ca rabbit-ban yen 10 1 'queue|first|messages=2|unacked=1' 'queue_so=2 queue_khac_0=1' KHONG_YEN

thu_ca sach app - 0 '(khong co)' 'paused=false' '== inj' '== toxics' '== lease' '== cron' '(khong timer khop)'
thu_ca sach obs - 0 '(khong co)' '== STOP' '== compose ls' '== MAY TAI load.fixture' '1 exited' '== cron'
for host in app obs tai; do
  mode=$host
  if [[ $host = tai ]]; then mode=obs; fi
  thu_ca "$host-tien-trinh" "$mode" - 0 'k6 --quiet run load.js' 'runner4.py --output /tmp/grep.log'
  thu_ca "$host-ps-loi" "$mode" - 6 "LOI_THU_THAP $host / ps"
  thu_ca "$host-cron-loi" "$mode" - 1 "LOI_THU_THAP $host / crontab" 'permission denied'
done
thu_ca cron-dong-5 app - 0 '* * * * * /fixture/lich-la-app'
thu_ca cron-dong-5 obs - 0 '* * * * * /fixture/lich-la-obs' '* * * * * /fixture/lich-la-tai'
thu_ca cron-trong obs - 0 'no crontab for'
thu_ca ps-rong app - 2 'LOI_THU_THAP app / ps'
thu_ca docker-loi app - 4 'LOI_THU_THAP app / docker'
thu_ca tai-docker-loi obs - 5 'LOI_THU_THAP tai / docker'
thu_ca ssh-loi obs - 255 'LOI_THU_THAP obs / ssh'
thu_ca git-loi app - 1 'LOI_THU_THAP app / git'
thu_ca timers-loi obs - 7 'LOI_THU_THAP obs / timers'
printf '\nKết quả: %d/%d đạt.\n' "$((n-loi))" "$n"
(( loi == 0 ))
