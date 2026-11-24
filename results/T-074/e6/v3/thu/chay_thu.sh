#!/bin/bash
# Phép thử giả lập cho v3/chay.sh trên laptop: docker/psql/pg_dump/pg_restore/df GIẢ (fake_docker.sh, fake_df.sh). KHÔNG kết nối máy hay DB.
# Gọi: bash chay_thu.sh            (SCRIPT=đường dẫn bộ chạy khác để thử đột biến)
set -u
THU=$(cd "$(dirname "$0")" && pwd)
SCRIPT=${SCRIPT:-$THU/../chay.sh}
V2=$(cd "$THU/../../v2" && pwd)
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
export FAKE="$TMP/fake" E6_OUT="$TMP/out" E6_DOCKER="$THU/fake_docker.sh" E6_DF="$THU/fake_df.sh"
export E6_NGU=1 E6_CHO_PHIEN=2 E6_CHO_KETNOI=2 E6_CHO_DICH_VU=2 FAKE_TRUONG="$V2/sql/B/truong.txt"
unset E6_V2 E6_XAC_NHAN_KHOI_PHUC MOC_PURCHASED MOC_HELD RUN_ID
dat=0; truot=0
moi() { rm -rf "$FAKE" "$E6_OUT"; mkdir -p "$FAKE/db"
  for d in event booking ticket payment; do DD="$FAKE/db/${d}_db"; mkdir -p "$DD"
    awk -F'|' -v d="$d" 'index($1, d".")==1 {print $1 "|CU"}' "$V2/sql/B/truong.txt" > "$DD/truong"
    awk -F'|' -v d="$d" 'index($1, d".")==1 {print "PHU|" $0}' "$V2/sql/B/phu.txt" > "$DD/phu"
    [ $d = booking ] && echo "BAO|booking.purchased|41705" >> "$DD/phu"
    printf 'BANG|%s_schema.tbl_a|10|aa%s\nBANG|%s_schema.tbl_b|3|bb%s\n' $d $d $d $d > "$DD/hash"; echo 100 > "$DD/dml"; done
  echo 9000000000 > "$FAKE/df_host"; echo 9000000000 > "$FAKE/df_pg"; echo 50000000 > "$FAKE/size"; }
chay() { bash "$SCRIPT" "$@" > "$TMP/last.out" 2>&1; echo $?; }
kq() { # tên, mong, được, [điều kiện phụ: lệnh trả 0]
  local ten=$1 mong=$2 duoc=$3; shift 3; local phu=0
  if [ $# -gt 0 ]; then eval "$*" > /dev/null 2>&1 || phu=1; fi
  if [ "$mong" = "$duoc" ] && [ $phu -eq 0 ]; then echo "DAT   $ten (rc=$duoc)"; dat=$((dat+1))
  else echo "TRUOT $ten (mong rc=$mong, duoc rc=$duoc, dieu_kien_phu=$([ $phu -eq 0 ] && echo dat || echo truot))"; sed 's/^/      | /' "$TMP/last.out" | tail -5; truot=$((truot+1)); fi; }
truong() { cut -d'|' -f2 "$FAKE/db/$1/truong" | sort | uniq -c | tr -s ' ' | tr '\n' ';'; }   # đếm CU/DICH
cb() { ls -d "$E6_OUT"/chuan-bi-B-$1-* | tail -1; }
gd() { ls -d "$E6_OUT"/ghi-B-$1-* | tail -1; }
khong_nhap() { ! ls "$FAKE/db" | grep -q '^e6n_'; }
BK="MOC_PURCHASED=41705 MOC_HELD=0"

echo "== Luồng đạt"
moi
kq T01_chuan_bi_event 0 "$(chay chuan-bi event)" 'khong_nhap && [ -s "$(cb event)/event_db.dump" ] && [ "$(cat "$(cb event)/KET_QUA")" = DAT ]'
kq T02_ghi_event_5DICH_1CU_la_DA_GHI 20 "$(chay ghi event "$(cb event)")" '[ "$(truong event_db)" = " 1 CU; 5 DICH;" ]'
kq T03_chuan_bi_dung_lai_bi_tu_choi 2 "$(chay ghi event "$(cb event)")"
for d in booking ticket payment; do
  kq T04_chuan_bi_$d 0 "$(env $BK bash "$SCRIPT" chuan-bi $d > "$TMP/last.out" 2>&1; echo $?)"
  kq T04_ghi_$d 20 "$(env $BK bash "$SCRIPT" ghi $d "$(cb $d)" > "$TMP/last.out" 2>&1; echo $?)"
done
kq T04_booking_4DICH_2CU 0 0 '[ "$(truong booking_db)" = " 2 CU; 4 DICH;" ]'
kq T05_kiem_DICH_ca_4 0 "$(env $BK bash "$SCRIPT" kiem DICH event booking ticket payment > "$TMP/last.out" 2>&1; echo $?)"
kq T06_kiem_CU_sau_ghi_sai_trang_thai 6 "$(chay kiem CU event)"

echo "== Chuẩn bị không đạt (chưa ghi DB thật)"
moi; echo 100 > "$FAKE/df_host"; kq T07_thieu_dia_host 3 "$(chay chuan-bi event)" '! ls "$(cb event)"/*.dump'
moi; echo 100 > "$FAKE/df_pg";   kq T08_thieu_dia_pg 3 "$(chay chuan-bi event)" '! ls "$(cb event)"/*.dump'
moi; touch "$FAKE/ghi_xen";      kq T09_ghi_xen_sau_dump_bam_khac 3 "$(chay chuan-bi event)" 'khong_nhap && [ -s "$(cb event)/bam-khac.txt" ]'
moi; echo 1 > "$FAKE/restore_rc"; kq T10_thu_khoi_phuc_loi 3 "$(chay chuan-bi event)" 'khong_nhap'
moi; echo 1 > "$FAKE/dump_rc";   kq T11_pg_dump_loi 3 "$(chay chuan-bi event)"
moi; sed -i '1s/|CU$/|DICH/' "$FAKE/db/event_db/truong"; kq T12_dau_khong_dung_CU 3 "$(chay chuan-bi event)"
moi; kq T13_booking_thieu_moc 2 "$(chay chuan-bi booking)"
moi; kq T14_booking_moc_purchased_lech 3 "$(MOC_PURCHASED=41704 MOC_HELD=0 bash "$SCRIPT" chuan-bi booking > "$TMP/last.out" 2>&1; echo $?)"
moi; echo "{x}" > "$FAKE/acl"; kq T15_acl_rieng_tat_khoi_phuc_tu_dong 0 "$(chay chuan-bi event)" '[ "$(cat "$(cb event)/khoi-phuc-tu-dong")" = khong ]'
moi; touch "$FAKE/dml_tang"; kq T16_dml_doi_trong_chuan_bi 3 "$(chay chuan-bi event)"

echo "== File v2 và danh sách trường"
mkdir -p "$TMP/v2a"; cp -r "$V2/sql" "$V2/SHA256SUMS" "$TMP/v2a/"; echo "-- sua" >> "$TMP/v2a/sql/B/thuan-event.sql"
moi; kq T17_sql_thuan_v2_bi_sua 2 "$(E6_V2="$TMP/v2a" bash "$SCRIPT" chuan-bi event > "$TMP/last.out" 2>&1; echo $?)"
mkdir -p "$TMP/v2b"; cp -r "$V2/sql" "$TMP/v2b/"; printf 'event.sale_ends_at|DICH|x\n' >> "$TMP/v2b/sql/B/truong.txt"
(cd "$TMP/v2b" && sha256sum ./sql/B/* | sed 's/  / */' > SHA256SUMS)
moi; kq T18_truong_txt_sai_dang 2 "$(E6_V2="$TMP/v2b" bash "$SCRIPT" chuan-bi event > "$TMP/last.out" 2>&1; echo $?)"
mkdir -p "$TMP/v2c"; cp -r "$V2/sql" "$TMP/v2c/"; : > "$TMP/v2c/sql/B/phu.txt"; rm "$TMP/v2c/sql/B/truong.txt"; touch "$TMP/v2c/sql/B/truong.txt"
(cd "$TMP/v2c" && sha256sum ./sql/B/* | sed 's/  / */' > SHA256SUMS)
moi; kq T19_truong_txt_rong 2 "$(E6_V2="$TMP/v2c" bash "$SCRIPT" kiem DICH event > "$TMP/last.out" 2>&1; echo $?)"
mkdir -p "$TMP/v2d"; cp -r "$V2/sql" "$TMP/v2d/"; chmod 000 "$TMP/v2d/sql/B/phu.txt" 2>/dev/null; rm -f "$TMP/v2d/sql/B/phu.txt"
(cd "$TMP/v2d" && sha256sum ./sql/B/* | sed 's/  / */' > SHA256SUMS)
moi; kq T20_phu_txt_khong_doc_duoc 2 "$(E6_V2="$TMP/v2d" bash "$SCRIPT" kiem DICH event > "$TMP/last.out" 2>&1; echo $?)"

echo "== Ghi: mọi rc khác 0 → chưa rõ → xác định bằng so cả nhóm trường"
for c in "loi_truoc 21 1_CU;5_DICH_khong" "loi_sau_commit 20 x" "thieu_dau 20 x" "mat_truoc 21 x" "mat_sau_commit 20 x" "mot_phan 22 x" "docker_loi 21 x"; do
  set -- $c; moi; chay chuan-bi event > /dev/null; echo "$1" > "$FAKE/thuan_mode"
  kq "T21_ghi_$1" "$2" "$(chay ghi event "$(cb event)")"
done
moi; chay chuan-bi event > /dev/null; echo mat_sau_commit > "$FAKE/thuan_mode"; echo 99 > "$FAKE/phien_con"; touch "$FAKE/phien_vinh_vien"
kq T22_phien_cu_con_chay 11 "$(chay ghi event "$(cb event)")"
rm -f "$FAKE/phien_vinh_vien"; echo 0 > "$FAKE/phien_con"
kq T23_xac_dinh_sau_khi_phien_ket_thuc 20 "$(chay xac-dinh event "$(gd event)")"
moi; env $BK bash "$SCRIPT" chuan-bi booking > /dev/null 2>&1; echo ok_bao_doi > "$FAKE/thuan_mode"
kq T24_booking_dung_dich_nhung_purchased_doi_la_KHAC 22 "$(env $BK bash "$SCRIPT" ghi booking "$(cb booking)" > "$TMP/last.out" 2>&1; echo $?)"

echo "== Khôi phục dump"
moi; chay chuan-bi event > /dev/null; echo mot_phan > "$FAKE/thuan_mode"; chay ghi event "$(cb event)" > /dev/null
kq T25_khoi_phuc_thieu_xac_nhan 2 "$(chay khoi-phuc event "$(cb event)")"
kq T26_khoi_phuc_dat 0 "$(E6_XAC_NHAN_KHOI_PHUC=event bash "$SCRIPT" khoi-phuc event "$(cb event)" > "$TMP/last.out" 2>&1; echo $?)" \
  '[ "$(truong event_db)" = " 6 CU;" ] && cmp -s "$(cb event)/bam-nhap.txt" "$(ls -d "$E6_OUT"/khoi-phuc-B-event-* | tail -1)/bam-sau.txt" && [ "$(cat "$FAKE/svc_flash-ticket-event-service-event-service-1")" = true ] && ls -d "$FAKE"/db/event_db_hong_*'
moi; chay chuan-bi event > /dev/null; echo mot_phan > "$FAKE/thuan_mode"; chay ghi event "$(cb event)" > /dev/null; echo 1 > "$FAKE/restore_rc"
kq T27_khoi_phuc_pg_restore_loi_tra_ten_cu 13 "$(E6_XAC_NHAN_KHOI_PHUC=event bash "$SCRIPT" khoi-phuc event "$(cb event)" > "$TMP/last.out" 2>&1; echo $?)" \
  '[ -d "$FAKE/db/event_db" ] && ! ls -d "$FAKE"/db/event_db_hong_* && grep -q "z.da_ghi" "$FAKE/db/event_db/hash" && [ "$(cat "$FAKE/svc_flash-ticket-event-service-event-service-1")" = false ]'
moi; chay chuan-bi event > /dev/null; echo mot_phan > "$FAKE/thuan_mode"; chay ghi event "$(cb event)" > /dev/null; echo 2 > "$FAKE/ketnoi"
kq T28_khoi_phuc_con_ket_noi 12 "$(E6_XAC_NHAN_KHOI_PHUC=event bash "$SCRIPT" khoi-phuc event "$(cb event)" > "$TMP/last.out" 2>&1; echo $?)" '[ -d "$FAKE/db/event_db" ]'
moi; chay chuan-bi event > /dev/null; echo mot_phan > "$FAKE/thuan_mode"; chay ghi event "$(cb event)" > /dev/null; echo unhealthy > "$FAKE/health"
kq T29_khoi_phuc_dich_vu_khong_khoe 15 "$(E6_XAC_NHAN_KHOI_PHUC=event bash "$SCRIPT" khoi-phuc event "$(cb event)" > "$TMP/last.out" 2>&1; echo $?)"

echo "== Bộ kiểm sau ghi (phản ví dụ CX-41/41b)"
moi; mk() { printf '%s\n' "$@" > "$FAKE/kiem_out"; }
BOOK_DICH=(TRUONG\|booking.sale_ends_at\|DICH TRUONG\|booking.json.saleEndsAt\|DICH TRUONG\|booking.json.eventStartsAt\|DICH TRUONG\|booking.json.eventEndsAt\|DICH TRUONG\|booking.json.configuredQuantity\|CU TRUONG\|booking.inventory.configured_capacity\|CU PHU\|booking.ticketTypes_khop\|1 PHU\|booking.held\|0)
mk "${BOOK_DICH[@]}" "BAO|booking.purchased|41705"; kq T30_booking_dung 0 "$(env $BK bash "$SCRIPT" kiem DICH booking > "$TMP/last.out" 2>&1; echo $?)"
mk "${BOOK_DICH[@]}" "BAO|booking.purchased|41706"; kq T31_purchased_41706 8 "$(env $BK bash "$SCRIPT" kiem DICH booking > "$TMP/last.out" 2>&1; echo $?)"
mk "${BOOK_DICH[@]}"; kq T32_thieu_BAO 7 "$(env $BK bash "$SCRIPT" kiem DICH booking > "$TMP/last.out" 2>&1; echo $?)"
EV=(TRUONG\|event.sale_ends_at\|DICH TRUONG\|event.starts_at\|DICH TRUONG\|event.checkin_starts_at\|DICH TRUONG\|event.ends_at\|DICH TRUONG\|event.checkin_ends_at\|DICH TRUONG\|event.ticket_types.configured_quantity\|CU PHU\|event.so_dong_events\|1)
mk "${EV[@]}"; kq T33_event_dung 0 "$(chay kiem DICH event)"
mk "${EV[@]/event.starts_at/eventXstarts_at}"; kq T34_ten_eventXstarts_at 7 "$(chay kiem DICH event)"
mk "${EV[@]}" "TRUONG|event.la|DICH"; kq T35_ten_la 7 "$(chay kiem DICH event)"
mk "${EV[@]}" "TRUONG|event.ends_at|DICH"; kq T36_ten_lap 7 "$(chay kiem DICH event)"
mk "${EV[@]:1}"; kq T37_thieu_ten 7 "$(chay kiem DICH event)"
mk "${EV[@]/event.ends_at|DICH/event.ends_at|KHAC:2026-12-05}"; kq T38_gia_tri_thu_ba 6 "$(chay kiem DICH event)"
mk "${EV[@]/event.so_dong_events|1/event.so_dong_events|2}"; kq T39_PHU_sai 8 "$(chay kiem DICH event)"
rm -f "$FAKE/kiem_out"; echo 2 > "$FAKE/kiem_rc"; kq T40_psql_loi_khi_kiem 5 "$(chay kiem DICH event)"; rm -f "$FAKE/kiem_rc"
kq T41_ten_DB_lap 2 "$(chay kiem DICH event event)"

echo "== Khóa, lượt, hạn"
moi; mkdir -p "$E6_OUT/.khoa-ghi-B"; kq T42_khoa_dang_giu 2 "$(chay chuan-bi event)"
moi; mkdir -p "$E6_OUT/chuan-bi-B-event-R1"; kq T43_trung_ma_luot 2 "$(RUN_ID=R1 bash "$SCRIPT" chuan-bi event > "$TMP/last.out" 2>&1; echo $?)"
moi; chay chuan-bi event > /dev/null; sleep 2; kq T44_chuan_bi_qua_han 3 "$(E6_TUOI_TOI_DA=1 bash "$SCRIPT" ghi event "$(cb event)" > "$TMP/last.out" 2>&1; echo $?)" '[ "$(truong event_db)" = " 6 CU;" ]'
moi; chay chuan-bi event > /dev/null; touch "$FAKE/dml_tang"; kq T45_dml_doi_tu_luc_chuan_bi 3 "$(chay ghi event "$(cb event)")" '[ "$(truong event_db)" = " 6 CU;" ]'
moi; chay chuan-bi event > /dev/null; kq T46_thu_muc_chuan_bi_khac_db 2 "$(chay ghi ticket "$(cb event)")"
moi; chay chuan-bi event > /dev/null; echo DICH > /dev/null; sed -i '1s/|CU$/|DICH/' "$FAKE/db/event_db/truong"
kq T47_ghi_khi_dau_da_doi 3 "$(chay ghi event "$(cb event)")"
moi; kq T48_kiem_thua_doi_so_chuan_bi 2 "$(chay chuan-bi event booking)"

echo "== Thuận + kiểm DICH trên DB nháp (bắt buộc, Minh duyệt 24/11)"
moi; kq T49_thu_thuan_tren_nhap 0 "$(chay chuan-bi event)" \
  'khong_nhap && [ "$(truong event_db)" = " 6 CU;" ] && grep -q "thuan + kiem DICH tren nhap: DAT" "$(cb event)/nhat-ky.txt"'
moi; echo loi_truoc > "$FAKE/thuan_mode"; kq T50_thu_thuan_tren_nhap_loi 3 "$(chay chuan-bi event)" 'khong_nhap && [ "$(truong event_db)" = " 6 CU;" ]'
moi; echo mot_phan > "$FAKE/thuan_mode"; kq T51_kiem_DICH_tren_nhap_khong_dat 3 "$(chay chuan-bi event)" 'khong_nhap && [ "$(truong event_db)" = " 6 CU;" ]'
moi; chay chuan-bi event > /dev/null; rm -f "$(cb event)/thuan-nhap-dat"; kq T52_ghi_tu_choi_chuan_bi_thieu_thu_tren_nhap 2 "$(chay ghi event "$(cb event)")" '[ "$(truong event_db)" = " 6 CU;" ]'

echo "TONG: dat=$dat truot=$truot"
[ $truot -eq 0 ]
