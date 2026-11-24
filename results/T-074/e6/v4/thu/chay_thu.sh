#!/bin/bash
# Phép thử giả lập cho v4/chay.sh trên laptop: docker/psql/pg_dump/pg_restore/df/ps GIẢ. KHÔNG kết nối máy hay DB.
# Gọi: bash chay_thu.sh            (SCRIPT=đường dẫn bộ chạy khác để thử đột biến)
set -u
THU=$(cd "$(dirname "$0")" && pwd)
SCRIPT=${SCRIPT:-$THU/../chay.sh}
V2=$(cd "$THU/../../v2" && pwd)
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
export FAKE="$TMP/fake" E6_OUT="$TMP/out" E6_DOCKER="$THU/fake_docker.sh" E6_DF="$THU/fake_df.sh" E6_PS="$THU/fake_ps.sh"
export E6_NGU=1 E6_CHO_PHIEN=2 E6_CHO_KETNOI=2 E6_CHO_DICH_VU=2 FAKE_TRUONG="$V2/sql/B/truong.txt"
unset E6_V2 E6_KHOI_PHUC_MINH MOC_PURCHASED MOC_HELD RUN_ID
dat=0; truot=0
moi() { rm -rf "$FAKE" "$E6_OUT"; mkdir -p "$FAKE/db"; o=40000
  for d in event booking ticket payment; do DD="$FAKE/db/${d}_db"; mkdir -p "$DD"; o=$((o+1)); echo $o > "$DD/oid"
    awk -F'|' -v d="$d" 'index($1, d".")==1 {print $1 "|CU"}' "$V2/sql/B/truong.txt" > "$DD/truong"
    awk -F'|' -v d="$d" 'index($1, d".")==1 {print "PHU|" $0}' "$V2/sql/B/phu.txt" > "$DD/phu"
    [ $d = booking ] && echo "BAO|booking.purchased|41705" >> "$DD/phu"
    printf 'BANG|%s_schema.tbl_a|10|aa%s\nBANG|%s_schema.tbl_b|3|bb%s\n' $d $d $d $d > "$DD/hash"; echo 100 > "$DD/dml"; done
  echo 9000000000 > "$FAKE/df_host"; echo 9000000000 > "$FAKE/df_pg"; echo 50000000 > "$FAKE/size"; }
mo() { MOC_PURCHASED=41705 MOC_HELD=0 bash "$SCRIPT" mo-luot > "$TMP/mo.out" 2>&1; }   # mở lượt với mốc đúng SQL B
moi_mo() { moi; mo; }
chay() { bash "$SCRIPT" "$@" > "$TMP/last.out" 2>&1; echo $?; }
kq() { # tên, mong, được, [điều kiện phụ: lệnh trả 0]
  local ten=$1 mong=$2 duoc=$3; shift 3; local phu=0
  if [ $# -gt 0 ]; then eval "$*" > /dev/null 2>&1 || phu=1; fi
  if [ "$mong" = "$duoc" ] && [ $phu -eq 0 ]; then echo "DAT   $ten (rc=$duoc)"; dat=$((dat+1))
  else echo "TRUOT $ten (mong rc=$mong, duoc rc=$duoc, dieu_kien_phu=$([ $phu -eq 0 ] && echo dat || echo truot))"; sed 's/^/      | /' "$TMP/last.out" | tail -5; truot=$((truot+1)); fi; }
truong() { cut -d'|' -f2 "$FAKE/db/$1/truong" | sort | uniq -c | tr -s ' ' | tr '\n' ';'; }
cb() { ls -d "$E6_OUT"/chuan-bi-B-$1-* | tail -1; }
gd() { ls -d "$E6_OUT"/ghi-B-$1-* | tail -1; }
kp() { ls -d "$E6_OUT"/khoi-phuc-B-$1-* | tail -1; }
kqf() { cat "$1/KET_QUA" 2>/dev/null; }
khong_nhap() { ! ls "$FAKE/db" | grep -q '^e6n_'; }
SVE=flash-ticket-event-service-event-service-1

echo "== Mở lượt: mốc so với hằng số SQL B (CX-46 điểm 4, CX-45b)"
moi; kq T01_mo_luot_dat 0 "$(MOC_PURCHASED=41705 MOC_HELD=0 bash "$SCRIPT" mo-luot > "$TMP/last.out" 2>&1; echo $?)" '[ -s "$E6_OUT/moc-luot.txt" ]'
moi; kq T02_mo_luot_moc_41706_dung_truoc_Event 3 "$(MOC_PURCHASED=41706 MOC_HELD=0 bash "$SCRIPT" mo-luot > "$TMP/last.out" 2>&1; echo $?)" '[ ! -e "$E6_OUT/moc-luot.txt" ] && [ "$(truong event_db)" = " 6 CU;" ]'
moi; kq T03_mo_luot_thieu_moc 2 "$(chay mo-luot)"
moi; kq T04_chuan_bi_khi_chua_mo_luot 2 "$(chay chuan-bi event)"
moi_mo; kq T05_mo_luot_lan_hai 2 "$(MOC_PURCHASED=41705 MOC_HELD=0 bash "$SCRIPT" mo-luot > "$TMP/last.out" 2>&1; echo $?)"
moi_mo; kq T06_MOC_moi_truong_khac_file 2 "$(MOC_PURCHASED=41706 MOC_HELD=0 bash "$SCRIPT" kiem CU booking > "$TMP/last.out" 2>&1; echo $?)"
moi; sed -i '1s/|CU$/|DICH/' "$FAKE/db/ticket_db/truong"; kq T07_mo_luot_kiem_CU_4_DB 3 "$(MOC_PURCHASED=41705 MOC_HELD=0 bash "$SCRIPT" mo-luot > "$TMP/last.out" 2>&1; echo $?)"
moi; sed -i 's/^BAO|booking.purchased|41705$/BAO|booking.purchased|41706/' "$FAKE/db/booking_db/phu"; kq T08_moc_khop_DB_nhung_lech_SQL_B 3 "$(MOC_PURCHASED=41706 MOC_HELD=0 bash "$SCRIPT" mo-luot > "$TMP/last.out" 2>&1; echo $?)" '[ ! -e "$E6_OUT/moc-luot.txt" ] && grep -rq moc_lech_SQL_B "$TMP/last.out" "$E6_OUT"'

echo "== Luồng đạt"
moi_mo
kq T10_chuan_bi_event 0 "$(chay chuan-bi event)" 'khong_nhap && [ -s "$(cb event)/event_db.dump" ] && [ "$(kqf "$(cb event)")" = DAT ]'
kq T11_ghi_event_5DICH_1CU_la_DA_GHI 20 "$(chay ghi event "$(cb event)")" '[ "$(truong event_db)" = " 1 CU; 5 DICH;" ] && [ -s "$(gd event)/PSQL_XONG" ]'
kq T12_chuan_bi_dung_lai 2 "$(chay ghi event "$(cb event)")"
for d in booking ticket payment; do
  kq T13_chuan_bi_$d 0 "$(chay chuan-bi $d)"
  kq T13_ghi_$d 20 "$(chay ghi $d "$(cb $d)")"
done
kq T14_booking_4DICH_2CU 0 0 '[ "$(truong booking_db)" = " 2 CU; 4 DICH;" ]'
kq T15_kiem_DICH_ca_4 0 "$(chay kiem DICH event booking ticket payment)"
kq T16_kiem_CU_sau_ghi 6 "$(chay kiem CU event)"

echo "== Chuẩn bị không đạt (chưa phát SQL lên DB thật)"
moi_mo; echo 100 > "$FAKE/df_host"; kq T20_thieu_dia_host 3 "$(chay chuan-bi event)" '! ls "$(cb event)"/*.dump'
moi_mo; echo 100 > "$FAKE/df_pg";   kq T21_thieu_dia_pg 3 "$(chay chuan-bi event)" '! ls "$(cb event)"/*.dump'
moi_mo; touch "$FAKE/ghi_xen";      kq T22_ghi_xen_sau_dump_bam_khac 3 "$(chay chuan-bi event)" 'khong_nhap && [ -s "$(cb event)/bam-khac.txt" ]'
moi_mo; echo 1 > "$FAKE/restore_rc"; kq T23_thu_khoi_phuc_loi 3 "$(chay chuan-bi event)" 'khong_nhap'
moi_mo; echo 1 > "$FAKE/dump_rc";   kq T24_pg_dump_loi 3 "$(chay chuan-bi event)"
moi_mo; sed -i '1s/|CU$/|DICH/' "$FAKE/db/event_db/truong"; kq T25_dau_khong_dung_CU 3 "$(chay chuan-bi event)"
moi_mo; echo "{x}" > "$FAKE/acl"; kq T26_acl_rieng_khong_chuan_bi 3 "$(chay chuan-bi event)" '[ "$(cat "$(cb event)/khoi-phuc-tu-dong")" = khong ] && ! ls "$(cb event)"/*.dump && grep -q db_co_ACL "$(cb event)/KET_QUA"'
moi_mo; touch "$FAKE/dml_tang"; kq T27_dml_doi_trong_chuan_bi 3 "$(chay chuan-bi event)"
moi_mo; echo 1 > "$FAKE/restore_rc"; echo 3 > "$FAKE/drop_rc"; kq T28_khong_xoa_duoc_nhap_bao_trong_KET_QUA 3 "$(chay chuan-bi event)" 'grep -q CON_DB_NHAP "$(cb event)/KET_QUA"'

echo "== Thuận + kiểm DICH trên DB nháp (bắt buộc, Minh duyệt 24/11)"
moi_mo; kq T30_thu_thuan_tren_nhap 0 "$(chay chuan-bi event)" \
  'khong_nhap && [ "$(truong event_db)" = " 6 CU;" ] && grep -q "thuan + kiem DICH tren nhap: DAT" "$(cb event)/nhat-ky.txt"'
moi_mo; echo loi_truoc > "$FAKE/thuan_mode"; kq T31_thuan_tren_nhap_loi 3 "$(chay chuan-bi event)" 'khong_nhap && [ "$(truong event_db)" = " 6 CU;" ] && grep -q thuan_tren_nhap "$(cb event)/KET_QUA"'
moi_mo; echo ok_bao_doi > "$FAKE/thuan_mode"; kq T32_kiem_DICH_tren_nhap_that_bai_rc8 3 "$(chay chuan-bi booking)" \
  'khong_nhap && [ "$(truong booking_db)" = " 6 CU;" ] && grep -q "kiem_dich_tren_nhap_rc8" "$(cb booking)/KET_QUA" && grep -q "thuan tren nhap rc=0" "$(cb booking)/nhat-ky.txt"'
moi_mo; chay chuan-bi event > /dev/null; rm -f "$(cb event)/thuan-nhap-dat"; kq T33_ghi_tu_choi_thieu_dau_thu_nhap 2 "$(chay ghi event "$(cb event)")" '[ "$(truong event_db)" = " 6 CU;" ]'
moi_mo; chay chuan-bi event > /dev/null; echo khong > "$(cb event)/khoi-phuc-tu-dong"; kq T34_ghi_tu_choi_co_khong 2 "$(chay ghi event "$(cb event)")" '[ "$(truong event_db)" = " 6 CU;" ]'

echo "== File v2 và danh sách trường"
mkdir -p "$TMP/v2a"; cp -r "$V2/sql" "$V2/SHA256SUMS" "$TMP/v2a/"; echo "-- sua" >> "$TMP/v2a/sql/B/thuan-event.sql"
moi_mo; kq T40_sql_thuan_v2_bi_sua 2 "$(E6_V2="$TMP/v2a" bash "$SCRIPT" chuan-bi event > "$TMP/last.out" 2>&1; echo $?)"
mkdir -p "$TMP/v2b"; cp -r "$V2/sql" "$TMP/v2b/"; printf 'event.sale_ends_at|DICH|x\n' >> "$TMP/v2b/sql/B/truong.txt"
(cd "$TMP/v2b" && sha256sum ./sql/B/* | sed 's/  / */' > SHA256SUMS)
moi_mo; kq T41_truong_txt_sai_dang 2 "$(E6_V2="$TMP/v2b" bash "$SCRIPT" chuan-bi event > "$TMP/last.out" 2>&1; echo $?)"
mkdir -p "$TMP/v2c"; cp -r "$V2/sql" "$TMP/v2c/"; : > "$TMP/v2c/sql/B/phu.txt"; : > "$TMP/v2c/sql/B/truong.txt"
(cd "$TMP/v2c" && sha256sum ./sql/B/* | sed 's/  / */' > SHA256SUMS)
moi_mo; kq T42_truong_txt_rong 2 "$(E6_V2="$TMP/v2c" bash "$SCRIPT" kiem DICH event > "$TMP/last.out" 2>&1; echo $?)"
mkdir -p "$TMP/v2d"; cp -r "$V2/sql" "$TMP/v2d/"; rm -f "$TMP/v2d/sql/B/phu.txt"
(cd "$TMP/v2d" && sha256sum ./sql/B/* | sed 's/  / */' > SHA256SUMS)
moi_mo; kq T43_phu_txt_khong_co 2 "$(E6_V2="$TMP/v2d" bash "$SCRIPT" kiem DICH event > "$TMP/last.out" 2>&1; echo $?)"

echo "== Ghi: mọi rc khác 0 → chưa rõ → xác định bằng so cả nhóm trường"
for c in "loi_truoc 21 CHUA_GHI" "loi_sau_commit 20 DA_GHI" "thieu_dau 20 DA_GHI" "mat_truoc 21 CHUA_GHI" "mat_sau_commit 20 DA_GHI" "mot_phan 22 KHAC_TRUONG" "docker_loi 21 CHUA_GHI"; do
  set -- $c; moi_mo; chay chuan-bi event > /dev/null; echo "$1" > "$FAKE/thuan_mode"
  kq "T50_ghi_$1" "$2" "$(chay ghi event "$(cb event)")" "[ \"\$(kqf \"\$(gd event)\")\" = $3 ]"
done
moi_mo; chay chuan-bi booking > /dev/null; echo ok_bao_doi > "$FAKE/thuan_mode"
kq T51_booking_dung_dich_purchased_doi_KHAC_NGHIEP_VU 22 "$(chay ghi booking "$(cb booking)")" '[ "$(kqf "$(gd booking)")" = KHAC_NGHIEP_VU ]'
moi_mo; chay chuan-bi event > /dev/null; echo mat_sau_commit > "$FAKE/thuan_mode"; echo 99 > "$FAKE/phien_con"; touch "$FAKE/phien_vinh_vien"
kq T52_phien_cu_con 11 "$(chay ghi event "$(cb event)")"
rm -f "$FAKE/phien_vinh_vien"; echo 0 > "$FAKE/phien_con"
kq T53_xac_dinh_sau_khi_phien_ket_thuc 20 "$(chay xac-dinh event "$(gd event)")"

echo "== xac-dinh gọi riêng khi tiến trình ghi còn (CX-46 điểm 6) và lỗi trước ghi (CX-46b N3)"
moi_mo; mkdir -p "$E6_OUT/ghi-B-event-R9"; echo t074-e6v4-ghi-R9-event > "$E6_OUT/ghi-B-event-R9/app.txt"
sleep 30 & SP=$!; echo $SP > "$E6_OUT/ghi-B-event-R9/pid"
kq T60_tien_trinh_ghi_con_song 11 "$(chay xac-dinh event "$E6_OUT/ghi-B-event-R9")"
kill $SP 2>/dev/null; wait $SP 2>/dev/null
echo "4242 docker exec -i -e PGAPPNAME=t074-e6v4-ghi-R9-event x psql" > "$FAKE/ps.txt"
kq T61_con_tien_trinh_psql_mang_app 11 "$(chay xac-dinh event "$E6_OUT/ghi-B-event-R9")"
rm -f "$FAKE/ps.txt"
kq T62_tien_trinh_da_chet_doc_trang_thai 21 "$(chay xac-dinh event "$E6_OUT/ghi-B-event-R9")"
moi_mo; chay chuan-bi event > /dev/null; touch "$FAKE/dml_tang"; chay ghi event "$(cb event)" > /dev/null; rm -f "$FAKE/dml_tang"
kq T63_loi_truoc_ghi_khong_co_app_txt 2 "$(chay xac-dinh event "$(gd event)")" '[ ! -e "$(gd event)/app.txt" ] && [ "$(truong event_db)" = " 6 CU;" ]'

echo "== Khôi phục dump (chỉ lượt ghi KHAC; dump của chính lượt đó)"
khac_event() { moi_mo; chay chuan-bi event > /dev/null; echo mot_phan > "$FAKE/thuan_mode"; chay ghi event "$(cb event)" > /dev/null; rm -f "$FAKE/thuan_mode"; }
khac_event; kq T70_thieu_duyet_Minh 2 "$(chay khoi-phuc event "$(gd event)")"
khac_event; kq T71_dua_thu_muc_chuan_bi_thay_vi_luot_ghi 2 "$(E6_KHOI_PHUC_MINH=event bash "$SCRIPT" khoi-phuc event "$(cb event)" > "$TMP/last.out" 2>&1; echo $?)"
moi_mo; chay chuan-bi event > /dev/null; chay ghi event "$(cb event)" > /dev/null
kq T72_luot_ghi_DA_GHI_khong_khoi_phuc 2 "$(E6_KHOI_PHUC_MINH=event bash "$SCRIPT" khoi-phuc event "$(gd event)" > "$TMP/last.out" 2>&1; echo $?)"
khac_event; G=$(gd event); C2=$(cb event); echo "$TMP/khac" > "$C2/DA_DUNG/boi"
kq T73_lien_ket_nguoc_khong_khop 2 "$(E6_KHOI_PHUC_MINH=event bash "$SCRIPT" khoi-phuc event "$G" > "$TMP/last.out" 2>&1; echo $?)"
khac_event
kq T74_khoi_phuc_dat 0 "$(E6_KHOI_PHUC_MINH=event bash "$SCRIPT" khoi-phuc event "$(gd event)" > "$TMP/last.out" 2>&1; echo $?)" \
  '[ "$(truong event_db)" = " 6 CU;" ] && cmp -s "$(cb event)/bam-nhap.txt" "$(kp event)/bam-sau.txt" && [ "$(cat "$FAKE/svc_$SVE")" = true ] && [ "$(cat "$FAKE/db"/event_db_hong_*/oid)" = 40001 ]'
khac_event; echo 1 > "$FAKE/restore_rc"
kq T75_pg_restore_loi_tra_ten_cu_xac_nhan_OID 13 "$(E6_KHOI_PHUC_MINH=event bash "$SCRIPT" khoi-phuc event "$(gd event)" > "$TMP/last.out" 2>&1; echo $?)" \
  '[ "$(cat "$FAKE/db/event_db/oid")" = 40001 ] && ! ls -d "$FAKE"/db/event_db_hong_* && [ "$(cat "$FAKE/svc_$SVE")" = false ]'
khac_event; echo 1 > "$FAKE/restore_rc"; touch "$FAKE/alter_loi_lan_2"
kq T76_tra_ten_loi_bao_16 16 "$(E6_KHOI_PHUC_MINH=event bash "$SCRIPT" khoi-phuc event "$(gd event)" > "$TMP/last.out" 2>&1; echo $?)" \
  'grep -q "TRANG_THAI_DB_CHUA_RO" "$(kp event)/KET_QUA" && ls -d "$FAKE"/db/event_db_hong_*'
khac_event; touch "$FAKE/alter_loi_lan_1"
kq T77_doi_ten_dau_loi_bao_16 16 "$(E6_KHOI_PHUC_MINH=event bash "$SCRIPT" khoi-phuc event "$(gd event)" > "$TMP/last.out" 2>&1; echo $?)" '[ -d "$FAKE/db/event_db" ]'
khac_event; touch "$FAKE/create_loi"
kq T78_tao_db_loi_tra_ten_cu 13 "$(E6_KHOI_PHUC_MINH=event bash "$SCRIPT" khoi-phuc event "$(gd event)" > "$TMP/last.out" 2>&1; echo $?)" '[ "$(cat "$FAKE/db/event_db/oid")" = 40001 ]'
khac_event; touch "$FAKE/bam_loi_hong"
kq T79_bam_ban_hien_tai_loi_tra_ten_cu 13 "$(E6_KHOI_PHUC_MINH=event bash "$SCRIPT" khoi-phuc event "$(gd event)" > "$TMP/last.out" 2>&1; echo $?)" '[ "$(cat "$FAKE/db/event_db/oid")" = 40001 ] && ! ls -d "$FAKE"/db/event_db_hong_*'
khac_event; touch "$FAKE/stop_khong_dung"
kq T80_dich_vu_khong_dung 12 "$(E6_KHOI_PHUC_MINH=event bash "$SCRIPT" khoi-phuc event "$(gd event)" > "$TMP/last.out" 2>&1; echo $?)" 'grep -q "Running=true" "$(kp event)/KET_QUA" && [ -d "$FAKE/db/event_db" ]'
khac_event; echo 2 > "$FAKE/ketnoi"
kq T81_con_ket_noi 17 "$(E6_KHOI_PHUC_MINH=event bash "$SCRIPT" khoi-phuc event "$(gd event)" > "$TMP/last.out" 2>&1; echo $?)" '[ -d "$FAKE/db/event_db" ]'
khac_event; echo unhealthy > "$FAKE/health"
kq T82_dich_vu_khong_khoe_bao_trang_thai 15 "$(E6_KHOI_PHUC_MINH=event bash "$SCRIPT" khoi-phuc event "$(gd event)" > "$TMP/last.out" 2>&1; echo $?)" 'grep -q "true|unhealthy" "$(kp event)/KET_QUA"'

echo "== Bộ kiểm sau ghi"
moi_mo; mk() { printf '%s\n' "$@" > "$FAKE/kiem_out"; }
BOOK_DICH=(TRUONG\|booking.sale_ends_at\|DICH TRUONG\|booking.json.saleEndsAt\|DICH TRUONG\|booking.json.eventStartsAt\|DICH TRUONG\|booking.json.eventEndsAt\|DICH TRUONG\|booking.json.configuredQuantity\|CU TRUONG\|booking.inventory.configured_capacity\|CU PHU\|booking.ticketTypes_khop\|1 PHU\|booking.held\|0)
mk "${BOOK_DICH[@]}" "BAO|booking.purchased|41705"; kq T90_booking_dung 0 "$(chay kiem DICH booking)"
mk "${BOOK_DICH[@]}" "BAO|booking.purchased|41706"; kq T91_purchased_41706 8 "$(chay kiem DICH booking)"
mk "${BOOK_DICH[@]}"; kq T92_thieu_BAO 7 "$(chay kiem DICH booking)"
mk "${BOOK_DICH[@]}" "BAO|booking.purchased|41705" "BAO|booking.autre|9"; kq T93_BAO_la 7 "$(chay kiem DICH booking)"
EV=(TRUONG\|event.sale_ends_at\|DICH TRUONG\|event.starts_at\|DICH TRUONG\|event.checkin_starts_at\|DICH TRUONG\|event.ends_at\|DICH TRUONG\|event.checkin_ends_at\|DICH TRUONG\|event.ticket_types.configured_quantity\|CU PHU\|event.so_dong_events\|1)
mk "${EV[@]}"; kq T94_event_dung 0 "$(chay kiem DICH event)"
mk "${EV[@]}" "BAO|event.x|1"; kq T95_BAO_la_o_event 7 "$(chay kiem DICH event)"
mk "${EV[@]/event.starts_at/eventXstarts_at}"; kq T96_ten_eventXstarts_at 7 "$(chay kiem DICH event)"
mk "${EV[@]}" "TRUONG|event.la|DICH"; kq T97_ten_la 7 "$(chay kiem DICH event)"
mk "${EV[@]}" "TRUONG|event.ends_at|DICH"; kq T98_ten_lap 7 "$(chay kiem DICH event)"
mk "${EV[@]:1}"; kq T99_thieu_ten 7 "$(chay kiem DICH event)"
mk "${EV[@]/event.ends_at|DICH/event.ends_at|KHAC:2026-12-05}"; kq T100_gia_tri_thu_ba 6 "$(chay kiem DICH event)"
mk "${EV[@]/event.so_dong_events|1/event.so_dong_events|2}"; kq T101_PHU_sai 8 "$(chay kiem DICH event)"
rm -f "$FAKE/kiem_out"; echo 2 > "$FAKE/kiem_rc"; kq T102_psql_loi_khi_kiem 5 "$(chay kiem DICH event)"; rm -f "$FAKE/kiem_rc"
kq T103_ten_DB_lap 2 "$(chay kiem DICH event event)"

echo "== Khóa, lượt, hạn"
moi_mo; mkdir -p "$E6_OUT/.khoa-ghi-B"; kq T110_khoa_dang_giu 2 "$(chay chuan-bi event)"
moi_mo; mkdir -p "$E6_OUT/chuan-bi-B-event-R1"; kq T111_trung_ma_luot 2 "$(RUN_ID=R1 bash "$SCRIPT" chuan-bi event > "$TMP/last.out" 2>&1; echo $?)"
moi_mo; chay chuan-bi event > /dev/null; sleep 2; kq T112_chuan_bi_qua_han 3 "$(E6_TUOI_TOI_DA=1 bash "$SCRIPT" ghi event "$(cb event)" > "$TMP/last.out" 2>&1; echo $?)" '[ "$(truong event_db)" = " 6 CU;" ]'
moi_mo; chay chuan-bi event > /dev/null; touch "$FAKE/dml_tang"; kq T113_dml_doi_tu_luc_chuan_bi 3 "$(chay ghi event "$(cb event)")" '[ "$(truong event_db)" = " 6 CU;" ]'
moi_mo; chay chuan-bi event > /dev/null; kq T114_chuan_bi_khac_db 2 "$(chay ghi ticket "$(cb event)")"
moi_mo; chay chuan-bi event > /dev/null; sed -i '1s/|CU$/|DICH/' "$FAKE/db/event_db/truong"; kq T115_ghi_khi_dau_da_doi 3 "$(chay ghi event "$(cb event)")"
moi_mo; kq T116_thua_doi_so 2 "$(chay chuan-bi event booking)"

echo "TONG: dat=$dat truot=$truot"
[ $truot -eq 0 ]
