#!/bin/bash
# Phép thử giả lập trên laptop cho chay.sh (không kết nối DB). Chạy: bash chay_thu.sh
set -u
V=$(cd "$(dirname "$0")/.." && pwd); T=$(mktemp -d); dat=0; truot=0
export PSQL="$V/thu/fake_psql.sh"
moi() { rm -rf "$T/fake" "$T/out"; mkdir -p "$T/fake" "$T/out"; export FAKE_DIR="$T/fake" E6_OUT="$T/out"; unset RUN_ID; }
goi() { cat "$T/fake/goi.log" 2>/dev/null | awk '{print $1}' | tr '\n' ' '; }
kq() { # ten, rc thuc, rc mong, [goi thuc], [goi mong]
  if [ "$2" = "$3" ] && [ "${4-}" = "${5-}" ]; then echo "DAT  $1 (rc=$2${4:+ goi=$4})"; dat=$((dat+1)); else echo "TRUOT $1 (rc=$2 mong=$3; goi='${4-}' mong='${5-}')"; truot=$((truot+1)); fi; }
# tạo đầu ra kiểm giả: $1=A|B, $2=trạng thái mặc định, các tham số sau dạng ten=trangthai để ghi đè, hoặc -ten để bỏ, +ten để nhân đôi
kiem_gia() { bt=$1; mac=$2; shift 2
  for db in event booking ticket payment; do : > "$T/fake/$db.out"; done
  while IFS='|' read -r ten m; do db=${ten%%.*}; st=$mac
    [ "$mac" = MONG ] && st=$m
    for o in "$@"; do case "$o" in "$ten="*) st=${o#*=};; "-$ten") st=BO;; esac; done
    [ "$st" = BO ] && continue
    echo "TRUONG|$ten|$st" >> "$T/fake/$db.out"
    for o in "$@"; do [ "$o" = "+$ten" ] && echo "TRUONG|$ten|$st" >> "$T/fake/$db.out"; done
  done < "$V/sql/$bt/truong.txt"
  while IFS='|' read -r ten v; do db=${ten%%.*}; for o in "$@"; do case "$o" in "PHU:$ten="*) v=${o#*=};; esac; done; echo "PHU|$ten|$v" >> "$T/fake/$db.out"; done < "$V/sql/$bt/phu.txt"
  echo "BAO|booking.purchased|41705" >> "$T/fake/booking.out"; }

moi; bash "$V/chay.sh" thuan A >/dev/null; kq "T01 thuan tat ca dat" $? 0 "$(goi)" "event_db booking_db ticket_db payment_db "
moi; echo 3 > "$T/fake/booking.rc"; bash "$V/chay.sh" thuan A >/dev/null; kq "T02 thuan loi SQL o booking dung ngay" $? 3 "$(goi)" "event_db booking_db "
moi; echo 2 > "$T/fake/event.rc"; bash "$V/chay.sh" thuan B >/dev/null; r=$?; f=$(ls "$T"/out/*/MAT_KET_NOI 2>/dev/null | wc -l); kq "T03 thuan mat ket noi o event: ma 4, co file MAT_KET_NOI" "$r/$f" "4/1" "$(goi)" "event_db "
moi; echo 1 > "$T/fake/ticket.rc"; bash "$V/chay.sh" thuan A >/dev/null; kq "T04 thuan loi psql khac o ticket" $? 5 "$(goi)" "event_db booking_db ticket_db "
moi; printf 'PHIEN 1 x\n' > "$T/fake/payment.out"; bash "$V/chay.sh" thuan A >/dev/null; kq "T05 thuan rc=0 nhung khong in DA_COMMIT" $? 5
moi; bash "$V/chay.sh" nghich A >/dev/null; kq "T06 nghich khong ten DB bi tu choi" $? 2 "$(goi)" ""
moi; echo 3 > "$T/fake/event.rc"; bash "$V/chay.sh" nghich A event booking >/dev/null; kq "T07 nghich loi o event khong sang booking" $? 3 "$(goi)" "event_db "
moi; bash "$V/chay.sh" nghich B booking ticket >/dev/null; kq "T08 nghich chi DB neu ten" $? 0 "$(goi)" "booking_db ticket_db "
moi; export RUN_ID=cung; bash "$V/chay.sh" thuan A >/dev/null; h=$(sha256sum "$T/out/thuan-A-cung/tien-do.txt"); bash "$V/chay.sh" thuan A >/dev/null; r=$?; h2=$(sha256sum "$T/out/thuan-A-cung/tien-do.txt"); [ "$h" = "$h2" ] && g=giu || g=doi; kq "T09 cung ma luot: tu choi, log cu giu nguyen" "$r/$g" "2/giu"
moi; bash "$V/chay.sh" thuan A >/dev/null; sleep 1; bash "$V/chay.sh" thuan A >/dev/null; n=$(ls -d "$T"/out/thuan-A-* | wc -l); kq "T10 hai luot: hai thu muc rieng" "$n" 2
moi; for db in event booking ticket payment; do echo 42 > "$T/fake/$db.rc"; done; bash "$V/chay.sh" kiem A CU >/dev/null; kq "T11 kiem: psql loi 42 -> khong tra 0" $? 5
moi; kiem_gia A CU; bash "$V/chay.sh" kiem A CU >/dev/null; kq "T12 kiem A CU dat" $? 0
moi; kiem_gia A CU; bash "$V/chay.sh" kiem A DICH >/dev/null; kq "T13 kiem A mong DICH khi con CU" $? 6
moi; kiem_gia A MONG; bash "$V/chay.sh" kiem A DICH >/dev/null; kq "T14 kiem A DICH dat (15 truong)" $? 0
moi; kiem_gia B MONG; bash "$V/chay.sh" kiem B DICH >/dev/null; kq "T15 kiem B DICH: suc chua CU, con lai DICH" $? 0
moi; kiem_gia B DICH; bash "$V/chay.sh" kiem B DICH >/dev/null; kq "T16 kiem B: suc chua bi ghi (DICH) -> sai" $? 6
moi; kiem_gia A MONG -booking.json.saleEndsAt; bash "$V/chay.sh" kiem A DICH >/dev/null; kq "T17 kiem thieu mot truong" $? 7
moi; kiem_gia A MONG +ticket.event_ends_at; bash "$V/chay.sh" kiem A DICH >/dev/null; kq "T18 kiem trung mot truong" $? 7
moi; kiem_gia A MONG booking.json.saleEndsAt=THIEU; bash "$V/chay.sh" kiem A DICH >/dev/null; kq "T19 kiem khoa JSON mat (THIEU)" $? 6
moi; kiem_gia A MONG payment.event_ends_at=THIEU_DONG; bash "$V/chay.sh" kiem A DICH >/dev/null; kq "T20 kiem mat dong Payment" $? 6
moi; kiem_gia A MONG PHU:booking.held=1; bash "$V/chay.sh" kiem A DICH >/dev/null; kq "T21 kiem PHU held sai" $? 8
moi; kiem_gia A MONG PHU:payment.payouts=1; bash "$V/chay.sh" kiem A DICH >/dev/null; kq "T22 kiem co payout" $? 8
moi; kiem_gia A CU event.starts_at=DICH; bash "$V/chay.sh" kiem A DOC >/dev/null; kq "T23 kiem DOC: lan cu/dich duoc bao, ma 0" $? 0
moi; kiem_gia A CU 'event.starts_at=KHAC:2026-01-01'; bash "$V/chay.sh" kiem A DOC >/dev/null; kq "T24 kiem DOC gap gia tri thu ba" $? 6
moi; kiem_gia A CU; bash "$V/chay.sh" kiem-khoa A CU event payment >/dev/null; kq "T25 kiem-khoa chi DB neu ten" $? 0 "$(goi)" "event_db payment_db "
moi; bash "$V/chay.sh" thuan C >/dev/null; kq "T26 bien the sai" $? 2
echo "TONG dat=$dat truot=$truot"; rm -rf "$T"; [ $truot -eq 0 ]
