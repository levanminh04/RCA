#!/bin/bash
# T-074 E6 v4 — bộ chạy biến thể B (giữ sức chứa 100.000, chỉ sửa ngày), CHỈ CHIỀU THUẬN, MỖI LẦN MỘT DB, có người theo dõi.
# Minh duyệt 24/11 ("Duyệt kết hợp"): giữ SQL thuận v2 B nguyên văn; bỏ SQL nghịch; hoàn tác bằng khôi phục dump chụp ngay trước khi ghi.
# Minh duyệt 24/11 ("Duyệt chạy thử"): thuận B + kiểm DICH trên DB nháp trước khi ghi DB thật.
# v4 = v3 sửa theo CX-45b, CX-46, CX-46b (đáp ở LOG T-074 phiên 12). SQL thuận/kiểm lấy NGUYÊN VĂN từ ../v2/sql/B, khớp ../v2/SHA256SUMS.
#
# Cách gọi (exp-app; chạy nền `setsid nohup bash chay.sh … > log 2>&1 &`, người trực đọc log):
#   MOC_PURCHASED=… MOC_HELD=… bash chay.sh mo-luot   # một lần đầu lượt E6, TRƯỚC DB đầu: so mốc vừa đọc ở b1c-yen với hằng số SQL B
#                                                    # (held/purchased trong thuan-booking.sql); lệch → dừng trước Event. Đạt → kiểm CU 4 DB,
#                                                    # lưu $E6_OUT/moc-luot.txt; mọi chế độ sau đọc mốc từ file này.
#   bash chay.sh chuan-bi  <db>                    # kiểm CU + đĩa, pg_dump, thử khôi phục vào DB nháp, so băm, thuận + kiểm DICH trên nháp, xóa nháp.
#   bash chay.sh ghi       <db> <thư-mục-chuẩn-bị> # dùng một lần một chuẩn-bị DAT còn hạn; chạy thuận v2; tự xác định kết cục.
#   bash chay.sh xac-dinh  <db> <thư-mục-ghi>      # chỉ đọc; chỉ kết luận khi tiến trình ghi của lượt đó đã kết thúc.
#   E6_KHOI_PHUC_MINH=<db> bash chay.sh khoi-phuc <db> <thư-mục-ghi>
#                                                  # chỉ cho lượt ghi có kết luận KHAC; dump lấy từ chuẩn-bị mà chính lượt ghi đó đã dùng.
#                                                  # E6_KHOI_PHUC_MINH = Minh đã duyệt khôi phục ĐÚNG ca này (CX-46 điểm 5).
#   bash chay.sh kiem      <CU|DICH> <db> [db…]    # chỉ đọc (FOR SHARE); so đúng tập tên theo nghĩa đen.
#
# Mã thoát: 0 đạt; 2 sai cách gọi/khóa/file v2 lệch/danh sách trường không đọc được/thiếu mốc lượt; 3 điều kiện trước ghi không đạt (CHƯA phát SQL
#   lên DB thật; chuẩn-bị lại sau khi sửa nguyên nhân); 5 lỗi đọc; 6 sai trạng thái; 7 thiếu/lạ/lặp tên; 8 PHU/BAO sai;
#   11 tiến trình/phiên ghi cũ còn (chờ rồi gọi lại xac-dinh); 20 ĐÃ GHI; 21 CHƯA GHI; 22 KHÁC cả đầu lẫn đích (KET_QUA ghi KHAC_TRUONG hoặc
#   KHAC_NGHIEP_VU) → giữ hiện trạng, trình Minh; 12 khôi phục: dịch vụ không dừng được; 17 khôi phục: còn kết nối sau khi dừng dịch vụ;
#   13 khôi phục không xong, DB gốc đã trả về tên cũ (đã xác nhận OID); 14 băm sau khôi phục khác dump; 15 dịch vụ không lên (KET_QUA ghi trạng thái
#   đọc được); 16 khôi phục lỗi và CHƯA xác nhận được DB nào mang tên chính (KET_QUA ghi tên + OID quan sát được).
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
V2=${E6_V2:-$HERE/../v2}
SQLD="$V2/sql/B"
OUTROOT=${E6_OUT:-/home/ubuntu/t074/e6}
PGC=${E6_PGC:-flash-ticket-infra-postgres-1}
PGDATA_DIR=${E6_PGDATA:-/var/lib/postgresql/data}
DK=${E6_DOCKER:-docker}
DFH=${E6_DF:-df}
PSX=${E6_PS:-ps}
TUOI=${E6_TUOI_TOI_DA:-1800}       # giây: chuẩn-bị cũ hơn thì phải làm lại
CHO_PHIEN=${E6_CHO_PHIEN:-120}     # giây chờ phiên ghi cũ kết thúc
CHO_DV=${E6_CHO_DICH_VU:-180}      # giây chờ dịch vụ lên lại
CHO_KN=${E6_CHO_KETNOI:-60}        # giây chờ kết nối tới DB hết sau khi dừng dịch vụ
NGU=${E6_NGU:-2}
GIB=1073741824
MOCF="$OUTROOT/moc-luot.txt"

CHE_DO=${1:-}; shift || true
case "$CHE_DO" in mo-luot|chuan-bi|ghi|xac-dinh|khoi-phuc|kiem) ;; *) echo "SAI_CACH_GOI che_do"; exit 2;; esac
db_hop_le() { case "$1" in event|booking|ticket|payment) return 0;; *) return 1;; esac; }
dich_vu() { case "$1" in
  event) echo flash-ticket-event-service-event-service-1;; booking) echo flash-ticket-booking-service-booking-service-1;;
  ticket) echo flash-ticket-ticket-service-ticket-service-1;; payment) echo flash-ticket-payment-service-payment-service-1;; esac; }

MONG=""; DBS=""; THAM=""
if [ "$CHE_DO" = kiem ]; then
  MONG=${1:-}; case "$MONG" in CU|DICH) ;; *) echo "SAI_CACH_GOI mong"; exit 2;; esac; shift
  [ $# -ge 1 ] || { echo "SAI_CACH_GOI kiem can it nhat mot DB"; exit 2; }
  for d in "$@"; do db_hop_le "$d" || { echo "SAI_CACH_GOI db=$d"; exit 2; }
    case " $DBS " in *" $d "*) echo "SAI_CACH_GOI db lap: $d"; exit 2;; esac; DBS="$DBS $d"; done
  DBS=${DBS# }; DB=$(echo "$DBS" | tr ' ' '+')
elif [ "$CHE_DO" = mo-luot ]; then
  [ $# -eq 0 ] || { echo "SAI_CACH_GOI mo-luot khong nhan doi so"; exit 2; }
  MONG=CU; DBS="event booking ticket payment"; DB=tat-ca
else
  DB=${1:-}; db_hop_le "$DB" || { echo "SAI_CACH_GOI db=$DB (moi lan mot DB)"; exit 2; }; DBS=$DB
  case "$CHE_DO" in ghi|xac-dinh|khoi-phuc) THAM=${2:-}; [ -n "$THAM" ] && [ $# -eq 2 ] || { echo "SAI_CACH_GOI can dung <db> <thu-muc>"; exit 2; }
      case "$THAM" in /*) ;; *) THAM="$OUTROOT/$THAM";; esac; [ -d "$THAM" ] || { echo "SAI_CACH_GOI khong co $THAM"; exit 2; };;
    *) [ $# -eq 1 ] || { echo "SAI_CACH_GOI thua doi so"; exit 2; };; esac
fi

# ---- file v2 phải khớp manifest v2 (giữ SQL thuận v2 B nguyên văn)
kiem_v2() { local f want got
  for f in "$@"; do
    want=$(awk -v p="*./sql/B/$f" '$2==p {print $1}' "$V2/SHA256SUMS" 2>/dev/null)
    got=$(sha256sum "$SQLD/$f" 2>/dev/null | cut -d' ' -f1)
    if [ -z "$want" ] || [ "$want" != "$got" ]; then echo "SAI_CACH_GOI file v2 lech manifest hoac thieu: $f"; return 1; fi
  done; }
FILES="truong.txt phu.txt thuan-booking.sql"; for d in $DBS; do FILES="$FILES thuan-$d.sql kiem-khoa-$d.sql"; done
kiem_v2 $FILES || exit 2

# ---- mốc lượt (CX-46 điểm 4, CX-45b): hằng số held/purchased trong SQL thuận Booking đã ghim là điều kiện phát
read -r SQL_HELD SQL_PURCHASED < <(sed -n 's/.*ri\.held IS DISTINCT FROM \([0-9][0-9]*\) OR ri\.purchased IS DISTINCT FROM \([0-9][0-9]*\).*/\1 \2/p' "$SQLD/thuan-booking.sql" | head -1)
case "${SQL_HELD:-}${SQL_PURCHASED:-}" in ''|*[!0-9]*) echo "SAI_CACH_GOI khong doc duoc hang so held/purchased trong thuan-booking.sql"; exit 2;; esac
so_nguyen() { case "${1:-}" in ''|*[!0-9]*) return 1;; *) return 0;; esac; }
if [ "$CHE_DO" = mo-luot ]; then
  so_nguyen "${MOC_PURCHASED:-}" && so_nguyen "${MOC_HELD:-}" || { echo "SAI_CACH_GOI mo-luot can MOC_PURCHASED, MOC_HELD (doc tu b1c-yen.sh vua chay)"; exit 2; }
  [ ! -e "$MOCF" ] || { echo "SAI_CACH_GOI da co $MOCF (luot E6 da mo; muon mo lai: Minh/dieu phoi quyet, doi ten file cu bang tay)"; exit 2; }
else
  [ -r "$MOCF" ] || { echo "SAI_CACH_GOI chua co $MOCF: chay 'mo-luot' truoc DB dau"; exit 2; }
  read -r F_P F_H < <(awk -F= '$1=="purchased"{p=$2} $1=="held"{h=$2} END{print p, h}' "$MOCF")
  so_nguyen "$F_P" && so_nguyen "$F_H" || { echo "SAI_CACH_GOI $MOCF sai dang"; exit 2; }
  if [ -n "${MOC_PURCHASED:-}${MOC_HELD:-}" ] && { [ "${MOC_PURCHASED:-}" != "$F_P" ] || [ "${MOC_HELD:-}" != "$F_H" ]; }; then
    echo "SAI_CACH_GOI MOC_* trong moi truong khac $MOCF"; exit 2; fi
  MOC_PURCHASED=$F_P; MOC_HELD=$F_H
fi

# ---- danh sách trường/dòng phụ của từng DB; không đọc được, sai dạng, rỗng, lặp → dừng
doc_ds() { # $1 db → TRUONG_DS, PHU_DS
  [ -r "$SQLD/truong.txt" ] && [ -r "$SQLD/phu.txt" ] || return 1
  TRUONG_DS=$(awk -F'|' -v d="$1" 'NF!=2 || $1=="" || ($2!="CU" && $2!="DICH") {bad=1; next}
     index($1, d".")==1 {if (seen[$1]++) bad=1; print} END {exit bad}' "$SQLD/truong.txt") || return 1
  [ -n "$TRUONG_DS" ] || return 1
  PHU_DS=$(awk -F'|' -v d="$1" 'NF!=2 || $1=="" || $2=="" {bad=1; next}
     index($1, d".")==1 {if (seen[$1]++) bad=1; print} END {exit bad}' "$SQLD/phu.txt") || return 1
  return 0; }
for d in $DBS; do doc_ds "$d" || { echo "SAI_CACH_GOI khong doc duoc/ sai dang truong.txt hoac phu.txt cho $d"; exit 2; }; done

# ---- khóa ghi toàn cục (nguyên tử) và thư mục lượt (nguyên tử, không ghi đè)
mkdir -p "$OUTROOT" || exit 2
KHOA="$OUTROOT/.khoa-ghi-B"
case "$CHE_DO" in mo-luot|chuan-bi|ghi|khoi-phuc)
  mkdir "$KHOA" 2>/dev/null || { echo "SAI_CACH_GOI dang co khoa $KHOA ($(cat "$KHOA/chu" 2>/dev/null)); kiem tien trinh roi moi xoa bang tay"; exit 2; }
  trap 'rm -rf "$KHOA"' EXIT;;
esac
RUN=${RUN_ID:-$(date -u +%Y%m%dT%H%M%SZ)-$$}
case "$RUN" in *[!A-Za-z0-9T-]*) echo "SAI_CACH_GOI RUN_ID"; exit 2;; esac
OUT="$OUTROOT/$CHE_DO-B-$DB-$RUN"
mkdir "$OUT" 2>/dev/null || { echo "SAI_CACH_GOI thu muc luot da co hoac khong tao duoc: $OUT"; exit 2; }
[ -d "$KHOA" ] && [ -w "$KHOA" ] && case "$CHE_DO" in mo-luot|chuan-bi|ghi|khoi-phuc) echo "$$ $CHE_DO $DB $RUN" > "$KHOA/chu";; esac
echo "$$" > "$OUT/pid"
log() { echo "$(date -u +%FT%T.%3NZ) $*" | tee -a "$OUT/nhat-ky.txt"; }
ket() { echo "$1" > "$OUT/KET_QUA"; log "KET_QUA $1"; }
echo "luot=$RUN che_do=$CHE_DO db=$DB mong=$MONG tham=$THAM moc_purchased=${MOC_PURCHASED:-} moc_held=${MOC_HELD:-} sql_purchased=$SQL_PURCHASED sql_held=$SQL_HELD thu_thuan_nhap=bat_buoc" > "$OUT/luot.txt"
log "BAT_DAU $CHE_DO $DB"

psqlx() { "$DK" exec -i -e PGAPPNAME="$2" "$PGC" psql -U postgres -X -q -At -v ON_ERROR_STOP=1 -d "$1"; }   # $1 tên DB, $2 app; stdin = SQL
ten_an() { case "$1" in *[!A-Za-z0-9_.-]*|'') return 1;; *) return 0;; esac; }

# ---- SQL phụ (chỉ đọc trừ CREATE/DROP/ALTER DATABASE ở nhánh riêng)
sql_bam() { cat <<'SQL'
-- E6V3 HASH
BEGIN ISOLATION LEVEL REPEATABLE READ READ ONLY;
SELECT format('SELECT %L||''|''||count(*)||''|''||coalesce(md5(string_agg(md5(e6v3_r::text), '''' ORDER BY md5(e6v3_r::text))),''-'') FROM %I.%I e6v3_r',
              'BANG|'||n.nspname||'.'||c.relname, n.nspname, c.relname)
  FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
 WHERE c.relkind='r' AND n.nspname NOT IN ('pg_catalog','information_schema') AND n.nspname NOT LIKE 'pg\_toast%' AND n.nspname NOT LIKE 'pg\_temp%'
 ORDER BY n.nspname, c.relname \gexec
SELECT 'SEQ|'||schemaname||'.'||sequencename||'|'||coalesce(last_value::text,'null') FROM pg_sequences ORDER BY 1;
SELECT 'SO_BANG|'||count(*) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace
 WHERE c.relkind='r' AND n.nspname NOT IN ('pg_catalog','information_schema') AND n.nspname NOT LIKE 'pg\_toast%' AND n.nspname NOT LIKE 'pg\_temp%';
COMMIT;
SQL
}
sql_dbinfo() { cat <<'SQL'
-- E6V3 DBINFO
SELECT 'DBINFO|'||pg_database_size(d.datname)||'|'||pg_get_userbyid(d.datdba)||'|'||pg_encoding_to_char(d.encoding)||'|'||d.datcollate||'|'||d.datctype||'|'||coalesce(d.datacl::text,'NULL')||'|'||(SELECT count(*) FROM pg_db_role_setting s WHERE s.setdatabase=d.oid)
  FROM pg_database d WHERE d.datname=current_database();
SELECT 'KETNOI|'||count(*) FROM pg_stat_activity WHERE datname=current_database() AND pid<>pg_backend_pid();
SQL
}
sql_dml() { echo "-- E6V3 DML"; echo "SELECT 'DML|'||coalesce(sum(n_tup_ins+n_tup_upd+n_tup_del),0) FROM pg_stat_user_tables;"; }
sql_tontai() { echo "-- E6V3 TONTAI"; echo "SELECT 'TONTAI|'||count(*) FROM pg_database WHERE datname='$1';"; }
sql_oid() { echo "-- E6V3 OID"; echo "SELECT 'OID|'||coalesce((SELECT oid::text FROM pg_database WHERE datname='$1'),'KHONG');"; }
sql_phien() { echo "-- E6V3 PHIEN"; echo "SELECT 'PHIEN_CON|'||count(*) FROM pg_stat_activity WHERE application_name='$1';"; }
sql_ketnoi_ds() { echo "-- E6V3 KETNOI_DS"; echo "SELECT 'KN|'||pid||'|'||coalesce(application_name,'')||'|'||coalesce(client_addr::text,'local')||'|'||state FROM pg_stat_activity WHERE datname='$1';"; }

lay() { # $1 tiền tố, $2 file → giá trị sau "tiền tố|"; rỗng nếu thiếu
  awk -F'|' -v p="$1" '$1==p {sub(/^[^|]*\|/, ""); print; exit}' "$2"; }
doc_dbinfo() { # $1 tên DB → DB_SIZE OWNER ENC COLL CTYPE ACL ROLESET KETNOI
  sql_dbinfo | psqlx "$1" "t074-e6v4-info-$RUN" > "$OUT/dbinfo-$1.txt" 2>> "$OUT/loi.txt" || return 1
  IFS='|' read -r _ DB_SIZE OWNER ENC COLL CTYPE ACL ROLESET < <(grep '^DBINFO|' "$OUT/dbinfo-$1.txt")
  KETNOI=$(lay KETNOI "$OUT/dbinfo-$1.txt")
  so_nguyen "${DB_SIZE:-}" && so_nguyen "${KETNOI:-}" || return 1
  ten_an "$OWNER" && ten_an "$ENC" && ten_an "$COLL" && ten_an "$CTYPE" || return 1; }
dml() { sql_dml | psqlx "$1" "t074-e6v4-dml-$RUN" > "$OUT/dml.tmp" 2>> "$OUT/loi.txt" || return 1; lay DML "$OUT/dml.tmp"; }
bam() { # $1 tên DB, $2 file đích
  sql_bam | psqlx "$1" "t074-e6v4-bam-$RUN" > "$2.raw" 2>> "$OUT/loi.txt" || return 1
  grep -E '^(BANG|SEQ|SO_BANG)\|' "$2.raw" > "$2"; [ "$(lay SO_BANG "$2")" -gt 0 ] 2>/dev/null; }
tontai() { sql_tontai "$1" | psqlx postgres "t074-e6v4-tt-$RUN" > "$OUT/tt.tmp" 2>> "$OUT/loi.txt" || return 2; lay TONTAI "$OUT/tt.tmp"; }
oid_cua() { sql_oid "$1" | psqlx postgres "t074-e6v4-oid-$RUN" > "$OUT/oid.tmp" 2>> "$OUT/loi.txt" || { echo LOI_DOC; return 1; }; lay OID "$OUT/oid.tmp"; }
sql_ddl() { psqlx postgres "t074-e6v4-ddl-$RUN" >> "$OUT/nhat-ky.txt" 2>> "$OUT/loi.txt"; }   # stdin = một lệnh CREATE/DROP/ALTER DATABASE
dia_trong() { # in: host_avail pg_avail
  local h p
  h=$("$DFH" -PB1 "$OUTROOT" 2>> "$OUT/loi.txt" | awk 'NR==2 {print $4}')
  p=$("$DK" exec "$PGC" df -PB1 "$PGDATA_DIR" 2>> "$OUT/loi.txt" | awk 'NR==2 {print $4}')
  so_nguyen "$h" && so_nguyen "$p" || return 1; echo "$h $p"; }

# ---- đánh giá đầu ra kiểm của MỘT DB: đúng tập tên TRUONG/PHU/BAO theo nghĩa đen, mỗi tên đúng một lần, không tên lạ
bao_cho_phep() { case "$1" in booking) echo "booking.purchased";; *) echo "";; esac; }
danh_gia() { # $1 db, $2 file đầu ra, $3 mong CU|DICH → 0 đạt; 7 thiếu/lạ/lặp; 6 sai trạng thái; 8 PHU/BAO sai
  doc_ds "$1" || { echo "KHONG_DOC_DUOC_DS"; return 7; }
  printf '%s\n' "$TRUONG_DS" > "$OUT/ds-$1.txt"
  if [ -n "$PHU_DS" ]; then printf '%s\n' "$PHU_DS" > "$OUT/phu-$1.txt"; else : > "$OUT/phu-$1.txt"; fi
  awk -F'|' -v mong="$3" -v db="$1" -v mp="${MOC_PURCHASED:-}" -v mh="${MOC_HELD:-}" -v baocp="$(bao_cho_phep "$1")" '
    BEGIN { nb = split(baocp, bl, " "); for (i = 1; i <= nb; i++) baook[bl[i]] = 1 }
    FILENAME==ARGV[1] {dich[$1]=$2; next}
    FILENAME==ARGV[2] {phu[$1]=$2; next}
    $1=="TRUONG" { t=$2; v=substr($0, length($1)+length($2)+3); if (!(t in dich)) {print "TRUONG_LA " t; la=1; next} dem[t]++; got[t]=v; next }
    $1=="PHU"    { t=$2; v=substr($0, length($1)+length($2)+3); if (!(t in phu))  {print "PHU_LA " t; la=1; next} pd[t]++; pg[t]=v; next }
    $1=="BAO"    { t=$2; v=substr($0, length($1)+length($2)+3); if (!(t in baook)) {print "BAO_LA " t; la=1; next} bd[t]++; bg[t]=v; next }
    END {
      for (t in dich) { if (dem[t]!=1) {print "SO_DONG_TRUONG " t "=" dem[t]+0; la=1; continue}
        w = (mong=="CU") ? "CU" : dich[t]; print t "=" got[t] " mong=" w; if (got[t]!=w) sai=1 }
      for (t in phu) { if (pd[t]!=1) {print "SO_DONG_PHU " t "=" pd[t]+0; la=1; continue}
        print "PHU " t "=" pg[t] " mong=" phu[t]; if (pg[t]!=phu[t]) ps=1 }
      for (t in baook) { if (bd[t]!=1) {print "SO_DONG_BAO " t "=" bd[t]+0; la=1} }
      if (db=="booking" && bd["booking.purchased"]==1) {
        print "BAO booking.purchased=" bg["booking.purchased"] " moc=" mp; if (bg["booking.purchased"]!=mp) ps=1 }
      if (db=="booking" && pd["booking.held"]==1) {print "MOC booking.held=" pg["booking.held"] " moc=" mh; if (pg["booking.held"]!=mh) ps=1}
      if (la) exit 7; if (sai) exit 6; if (ps) exit 8; exit 0 }' "$OUT/ds-$1.txt" "$OUT/phu-$1.txt" "$2"
}
kiem_khoa() { # $1 db, $2 tên DB thật/nháp, $3 nhãn → file $OUT/kiem-$3.out; rc psql
  psqlx "$2" "t074-e6v4-kiem-$RUN-$3" < "$SQLD/kiem-khoa-$1.sql" > "$OUT/kiem-$3.out" 2> "$OUT/kiem-$3.err"; }
KHAC_LOAI=""
phan_loai() { # $1 db, $2 file đầu ra → 20 đích, 21 đầu, 22 khác cả hai (KHAC_LOAI), 7 không đọc được
  local rd rc
  danh_gia "$1" "$2" DICH > "$OUT/pl-dich.txt"; rd=$?
  danh_gia "$1" "$2" CU   > "$OUT/pl-dau.txt"; rc=$?
  cat "$OUT/pl-dich.txt" >> "$OUT/nhat-ky.txt"
  if [ $rd -eq 7 ] || [ $rc -eq 7 ]; then return 7; fi
  if [ $rd -eq 0 ]; then return 20; fi
  if [ $rc -eq 0 ]; then return 21; fi
  # khác cả hai: trường E6 đúng một đầu nhưng PHU/BAO lệch → nghiệp vụ đổi; ngược lại → trường E6 lẫn/giá trị thứ ba
  if [ $rd -eq 8 ] || [ $rc -eq 8 ]; then KHAC_LOAI=KHAC_NGHIEP_VU; else KHAC_LOAI=KHAC_TRUONG; fi
  return 22; }

xac_dinh() { # $1 db, $2 app name của phiên ghi → mã 11/20/21/22/5/7
  local t=0 n rc
  while :; do
    sql_phien "$2" | psqlx postgres "t074-e6v4-phien-$RUN" > "$OUT/phien.tmp" 2>> "$OUT/loi.txt" || { log "LOI_DOC pg_stat_activity"; return 5; }
    n=$(lay PHIEN_CON "$OUT/phien.tmp"); so_nguyen "$n" || { log "LOI_DOC phien"; return 5; }
    [ "$n" -eq 0 ] && break
    if [ $t -ge "$CHO_PHIEN" ]; then log "PHIEN_CON app=$2 so=$n — cho them roi goi: bash chay.sh xac-dinh $1 <thu-muc-ghi>"; return 11; fi
    sleep "$NGU"; t=$((t+NGU))
  done
  log "phien ghi cu da ket thuc (app=$2)"
  kiem_khoa "$1" "${1}_db" xac-dinh || { log "LOI_DOC kiem-khoa rc=$?"; return 5; }
  phan_loai "$1" "$OUT/kiem-xac-dinh.out"; rc=$?
  case $rc in
    20) log "DA_GHI $1: ca nhom truong dung DICH B, PHU/BAO dung moc luot";;
    21) log "CHUA_GHI $1: ca nhom truong dung DAU, PHU/BAO dung moc luot";;
    22) log "$KHAC_LOAI $1: khac ca dau lan dich (xem nhat-ky: tung truong, PHU, BAO) → GIU HIEN TRANG, trinh Minh (khong tu khoi phuc)";;
    7)  log "KHONG_DOC_DUOC $1: thieu/la/lap ten trong dau ra; goi lai xac-dinh";;
  esac
  return $rc; }
ket_xd() { case $1 in 20) ket DA_GHI;; 21) ket CHUA_GHI;; 22) ket "$KHAC_LOAI";; 11) ket PHIEN_CON;; *) ket "CHUA_RO_LOI_DOC_$1";; esac; }

case "$CHE_DO" in
# =====================================================================================
mo-luot)
  log "moc vua doc: purchased=$MOC_PURCHASED held=$MOC_HELD; SQL B doi: purchased=$SQL_PURCHASED held=$SQL_HELD"
  if [ "$MOC_PURCHASED" != "$SQL_PURCHASED" ] || [ "$MOC_HELD" != "$SQL_HELD" ]; then
    ket "KHONG_DAT moc_lech_SQL_B (dung truoc Event; trinh Minh)"; exit 3; fi
  tong=0
  for d in $DBS; do
    kiem_khoa "$d" "${d}_db" "$d" || { log "LOI_DOC $d"; tong=5; continue; }
    danh_gia "$d" "$OUT/kiem-$d.out" CU >> "$OUT/nhat-ky.txt"; rc=$?; log "$d CU rc=$rc"; [ $rc -eq 0 ] || tong=$rc
  done
  [ $tong -eq 0 ] || { ket "KHONG_DAT kiem_CU_rc$tong"; exit 3; }
  printf 'purchased=%s\nheld=%s\nluot=%s\nutc=%s\n' "$MOC_PURCHASED" "$MOC_HELD" "$RUN" "$(date -u +%FT%TZ)" > "$MOCF.tmp" && mv "$MOCF.tmp" "$MOCF"
  ket DAT; echo "DAT mo-luot: moc $MOCF"; exit 0;;
# =====================================================================================
chuan-bi)
  D="${DB}_db"
  doc_dbinfo "$D" || { log "LOI_DOC dbinfo"; ket "KHONG_DAT dbinfo"; exit 3; }
  log "dbinfo size=$DB_SIZE owner=$OWNER enc=$ENC coll=$COLL ctype=$CTYPE acl=$ACL roleset=$ROLESET ketnoi=$KETNOI"
  printf '%s|%s|%s|%s|%s\n' "$DB_SIZE" "$OWNER" "$ENC" "$COLL" "$CTYPE" > "$OUT/dbinfo.txt"
  # CX-46b N2: đường hoàn tác đã duyệt là thay DB từ dump; DB có ACL/role setting riêng thì đường đó không giữ được cấu hình → không chuẩn bị ghi
  if [ "$ACL" != NULL ] || [ "$ROLESET" != 0 ]; then echo khong > "$OUT/khoi-phuc-tu-dong"
    ket "KHONG_DAT db_co_ACL_hoac_role_setting_rieng (dung DB nay; trinh phuong an khoi phuc tay)"; exit 3; fi
  echo co > "$OUT/khoi-phuc-tu-dong"
  read -r HA PA < <(dia_trong) || true
  so_nguyen "${HA:-}" || { log "LOI_DOC df"; ket "KHONG_DAT df"; exit 3; }
  CANH=$((DB_SIZE + GIB)); CANP=$((2 * DB_SIZE + GIB))
  log "dia host_trong=$HA can=$CANH pg_trong=$PA can=$CANP"
  if [ "$HA" -lt "$CANH" ] || [ "$PA" -lt "$CANP" ]; then ket "KHONG_DAT thieu_dia"; exit 3; fi
  kiem_khoa "$DB" "$D" truoc; rc=$?
  [ $rc -eq 0 ] || { log "LOI_DOC kiem-khoa rc=$rc"; ket "KHONG_DAT kiem_truoc_loi_doc"; exit 3; }
  danh_gia "$DB" "$OUT/kiem-truoc.out" CU >> "$OUT/nhat-ky.txt"; rc=$?
  [ $rc -eq 0 ] || { ket "KHONG_DAT dau_khong_dung_CU_rc$rc"; exit 3; }
  S0=$(dml "$D") || { ket "KHONG_DAT dml"; exit 3; }; log "dml_truoc_dump=$S0"
  DUMP="$OUT/$D.dump"
  "$DK" exec "$PGC" pg_dump -U postgres -Fc -d "$D" > "$DUMP" 2> "$OUT/pg_dump.err"; rc=$?
  [ $rc -eq 0 ] && [ -s "$DUMP" ] || { log "pg_dump rc=$rc"; ket "KHONG_DAT pg_dump"; exit 3; }
  (cd "$OUT" && sha256sum "$D.dump" > dump.sha256); log "dump $(stat -c %s "$DUMP") byte sha256=$(cut -d' ' -f1 "$OUT/dump.sha256")"
  "$DK" exec -i "$PGC" pg_restore -l < "$DUMP" > "$OUT/dump-list.txt" 2>> "$OUT/loi.txt" || { ket "KHONG_DAT pg_restore_l"; exit 3; }
  log "dump_list TABLE_DATA=$(grep -c 'TABLE DATA' "$OUT/dump-list.txt")"
  NHAP="e6n_${DB}_$(echo "$RUN" | tr -cd 'A-Za-z0-9' | tr 'A-Z' 'a-z' | tail -c 24)"; echo "$NHAP" > "$OUT/nhap.txt"
  [ "$(tontai "$NHAP")" = 0 ] || { ket "KHONG_DAT db_nhap_da_co_hoac_loi_doc"; exit 3; }
  echo "CREATE DATABASE \"$NHAP\" OWNER \"$OWNER\" TEMPLATE template0 ENCODING '$ENC' LC_COLLATE '$COLL' LC_CTYPE '$CTYPE';" | sql_ddl \
    || { ket "KHONG_DAT tao_db_nhap"; exit 3; }
  CON_NHAP=""
  xoa_nhap() { echo "DROP DATABASE \"$NHAP\";" | sql_ddl
    if [ "$(tontai "$NHAP")" = 0 ]; then log "da xoa db nhap $NHAP"; return 0; fi
    CON_NHAP="; CON_DB_NHAP $NHAP (xoa tay)"; log "CANH_BAO chua xoa duoc db nhap $NHAP"; return 1; }
  dung() { xoa_nhap; ket "$1$CON_NHAP"; exit 3; }
  "$DK" exec -i "$PGC" pg_restore -U postgres --exit-on-error -d "$NHAP" < "$DUMP" > "$OUT/thu-khoi-phuc.out" 2>&1; rc=$?
  [ $rc -eq 0 ] || { log "thu khoi phuc rc=$rc"; dung "KHONG_DAT thu_khoi_phuc"; }
  bam "$D" "$OUT/bam-that.txt" && bam "$NHAP" "$OUT/bam-nhap.txt" || dung "KHONG_DAT bam_loi_doc"
  if ! cmp -s "$OUT/bam-that.txt" "$OUT/bam-nhap.txt"; then
    diff "$OUT/bam-that.txt" "$OUT/bam-nhap.txt" > "$OUT/bam-khac.txt"; log "BAM_KHAC: $(wc -l < "$OUT/bam-khac.txt") dong"
    dung "KHONG_DAT bam_khac"; fi
  # CX-46 (không chặn): chỉ kết luận đúng điều đo được
  log "bam noi dung bang (relkind r) + sequence cua DB that tai luc bam KHOP dump da khoi phuc: $(lay SO_BANG "$OUT/bam-that.txt") bang, $(grep -c '^SEQ|' "$OUT/bam-that.txt") sequence"
  {   # BẮT BUỘC — Minh duyệt 24/11 ("Duyệt chạy thử")
    APPN="t074-e6v4-thuan-nhap-$RUN"
    psqlx "$NHAP" "$APPN" < "$SQLD/thuan-$DB.sql" > "$OUT/thuan-nhap.out" 2> "$OUT/thuan-nhap.err"; rc=$?
    log "thuan tren nhap rc=$rc"
    if [ $rc -ne 0 ] || ! awk -v n="$NHAP" '$1=="DA_COMMIT" && $2==n {f=1} END {exit !f}' "$OUT/thuan-nhap.out"; then
      dung "KHONG_DAT thuan_tren_nhap (dung DB nay, khong ghi DB that, bao dieu phoi)"; fi
    kiem_khoa "$DB" "$NHAP" nhap-dich || dung "KHONG_DAT kiem_nhap_loi_doc (dung DB nay, bao dieu phoi)"
    danh_gia "$DB" "$OUT/kiem-nhap-dich.out" DICH >> "$OUT/nhat-ky.txt"; rc=$?
    [ $rc -eq 0 ] || dung "KHONG_DAT kiem_dich_tren_nhap_rc$rc (dung DB nay, khong ghi DB that, bao dieu phoi)"
    log "thuan + kiem DICH tren nhap: DAT"; echo DAT > "$OUT/thuan-nhap-dat"
  }
  xoa_nhap || { ket "KHONG_DAT xoa_db_nhap$CON_NHAP"; exit 3; }
  S1=$(dml "$D") || { ket "KHONG_DAT dml"; exit 3; }
  [ "$S1" = "$S0" ] || { log "bo dem DML doc duoc doi trong luc chuan bi: $S0 → $S1"; ket "KHONG_DAT dml_doi"; exit 3; }
  echo "$S1" > "$OUT/dml-cuoi.txt"; echo "$DB" > "$OUT/db.txt"
  ket DAT; echo "DAT chuan-bi $DB → $OUT"; exit 0;;
# =====================================================================================
ghi)
  CB=$THAM; D="${DB}_db"
  [ "$(cat "$CB/KET_QUA" 2>/dev/null)" = DAT ] && [ "$(cat "$CB/db.txt" 2>/dev/null)" = "$DB" ] || { ket "SAI chuan_bi_khong_DAT_hoac_khac_db"; exit 2; }
  case "$CB" in *"/chuan-bi-B-$DB-"*) ;; *) ket "SAI khong_phai_thu_muc_chuan_bi"; exit 2;; esac
  [ "$(cat "$CB/thuan-nhap-dat" 2>/dev/null)" = DAT ] || { ket "SAI chuan_bi_chua_dat_thuan_tren_nhap"; exit 2; }
  [ "$(cat "$CB/khoi-phuc-tu-dong" 2>/dev/null)" = co ] || { ket "SAI chuan_bi_khong_co_duong_khoi_phuc"; exit 2; }
  tuoi=$(( $(date +%s) - $(stat -c %Y "$CB/KET_QUA") )); [ "$tuoi" -le "$TUOI" ] || { ket "KHONG_DAT chuan_bi_qua_han_${tuoi}s"; exit 3; }
  mkdir "$CB/DA_DUNG" 2>/dev/null || { ket "SAI chuan_bi_da_dung"; exit 2; }; echo "$OUT" > "$CB/DA_DUNG/boi"
  echo "$CB" > "$OUT/chuan-bi.txt"
  (cd "$CB" && sha256sum -c dump.sha256 > /dev/null 2>&1) || { ket "KHONG_DAT dump_lech_sha"; exit 3; }
  S=$(dml "$D") || { ket "KHONG_DAT dml"; exit 3; }
  [ "$S" = "$(cat "$CB/dml-cuoi.txt")" ] || { log "bo dem DML doi tu luc chuan bi: $(cat "$CB/dml-cuoi.txt") → $S"; ket "KHONG_DAT dml_doi"; exit 3; }
  kiem_khoa "$DB" "$D" truoc; rc=$?
  [ $rc -eq 0 ] || { ket "KHONG_DAT kiem_truoc_loi_doc"; exit 3; }
  danh_gia "$DB" "$OUT/kiem-truoc.out" CU >> "$OUT/nhat-ky.txt"; rc=$?
  [ $rc -eq 0 ] || { ket "KHONG_DAT dau_khong_dung_CU_rc$rc"; exit 3; }
  APP="t074-e6v4-ghi-$RUN-$DB"; [ ${#APP} -le 63 ] || { ket "SAI app_name_dai"; exit 2; }
  echo "$APP" > "$OUT/app.txt"     # có app.txt = có thể đã phát SQL lên DB thật (CX-46b N3)
  log "GHI_BAT_DAU $D app=$APP"
  psqlx "$D" "$APP" < "$SQLD/thuan-$DB.sql" > "$OUT/thuan.out" 2> "$OUT/thuan.err"; RC=$?
  echo "$RC" > "$OUT/PSQL_XONG"
  log "GHI_KET_THUC rc=$RC"
  if [ $RC -eq 0 ] && awk -v n="$D" '$1=="DA_COMMIT" && $2==n {f=1} END {exit !f}' "$OUT/thuan.out"; then
    kiem_khoa "$DB" "$D" sau; rc=$?
    if [ $rc -eq 0 ]; then danh_gia "$DB" "$OUT/kiem-sau.out" DICH >> "$OUT/nhat-ky.txt"; rc=$?
      if [ $rc -eq 0 ]; then ket "DA_GHI"; echo "DA_GHI $DB (rc 0, DA_COMMIT, kiem DICH dat) luot=$RUN"; exit 20; fi; fi
    log "rc 0 + DA_COMMIT nhung kiem sau khong dat (rc=$rc) → xac dinh"
  else
    log "CHUA_RO: rc=$RC hoac thieu DA_COMMIT → xac dinh (khong suy 'da rollback' tu ma thoat)"
  fi
  xac_dinh "$DB" "$APP"; rc=$?; ket_xd $rc; exit $rc;;
# =====================================================================================
xac-dinh)
  G=$THAM
  case "$G" in *"/ghi-B-$DB-"*) ;; *) ket "SAI khong_phai_thu_muc_ghi_cua_$DB"; exit 2;; esac
  APP=$(cat "$G/app.txt" 2>/dev/null)
  [ -n "$APP" ] || { ket "SAI luot_ghi_khong_co_app.txt: chua phat SQL len DB that (loi truoc ghi, xem KET_QUA cua luot do; sua nguyen nhan, chuan bi lai)"; exit 2; }
  # CX-46 điểm 6: chỉ kết luận khi tiến trình ghi của lượt đã kết thúc
  if [ ! -e "$G/PSQL_XONG" ]; then
    P=$(cat "$G/pid" 2>/dev/null)
    if [ -n "$P" ] && kill -0 "$P" 2>/dev/null; then log "TIEN_TRINH_GHI_CON pid=$P — theo doi chinh luot do"; ket "PHIEN_CON tien_trinh_ghi"; exit 11; fi
    if $PSX -eo pid,args 2>/dev/null | grep -F -- "$APP" | grep -v -F "grep" | grep -q .; then
      log "con tien trinh mang app=$APP tren may"; ket "PHIEN_CON tien_trinh_psql"; exit 11; fi
    log "tien trinh ghi pid=$P khong con, khong thay PSQL_XONG (bi ngat) — chi doc trang thai DB"
  fi
  xac_dinh "$DB" "$APP"; rc=$?; ket_xd $rc; exit $rc;;
# =====================================================================================
khoi-phuc)
  G=$THAM; D="${DB}_db"; SV=$(dich_vu "$DB")
  [ "${E6_KHOI_PHUC_MINH:-}" = "$DB" ] || { ket "SAI can E6_KHOI_PHUC_MINH=$DB (Minh duyet khoi phuc dung ca nay)"; exit 2; }
  case "$G" in *"/ghi-B-$DB-"*) ;; *) ket "SAI can thu muc LUOT GHI cua $DB"; exit 2;; esac
  case "$(cat "$G/KET_QUA" 2>/dev/null)" in KHAC_TRUONG|KHAC_NGHIEP_VU) ;; *) ket "SAI luot_ghi_khong_co_ket_luan_KHAC"; exit 2;; esac
  # CX-46 điểm 1: dump lấy từ chuẩn-bị mà CHÍNH lượt ghi này đã dùng; kiểm liên kết hai chiều trước khi dừng dịch vụ
  CB=$(cat "$G/chuan-bi.txt" 2>/dev/null)
  [ -n "$CB" ] && [ -d "$CB" ] && [ "$(cat "$CB/DA_DUNG/boi" 2>/dev/null)" = "$G" ] && [ "$(cat "$CB/db.txt" 2>/dev/null)" = "$DB" ] \
    || { ket "SAI lien_ket_ghi_chuan_bi_khong_khop"; exit 2; }
  echo "$G" > "$OUT/luot-ghi.txt"; echo "$CB" > "$OUT/chuan-bi.txt"
  [ "$(cat "$CB/khoi-phuc-tu-dong" 2>/dev/null)" = co ] || { ket "SAI db_co_ACL_rieng_khoi_phuc_tay"; exit 2; }
  (cd "$CB" && sha256sum -c dump.sha256 > /dev/null 2>&1) || { ket "KHONG_DAT dump_lech_sha"; exit 3; }
  IFS='|' read -r CB_SZ CB_OWNER CB_ENC CB_COLL CB_CTYPE < "$CB/dbinfo.txt"
  doc_dbinfo "$D" || { ket "KHONG_DAT dbinfo"; exit 3; }
  # tự soát A1: tạo DB mới theo thuộc tính lúc chuẩn-bị; khác hiện tại thì dừng
  [ "$OWNER|$ENC|$COLL|$CTYPE" = "$CB_OWNER|$CB_ENC|$CB_COLL|$CB_CTYPE" ] || { log "thuoc tinh DB doi: $CB_OWNER|$CB_ENC|$CB_COLL|$CB_CTYPE → $OWNER|$ENC|$COLL|$CTYPE"; ket "KHONG_DAT thuoc_tinh_db_doi"; exit 3; }
  read -r HA PA < <(dia_trong) || true
  so_nguyen "${PA:-}" || { ket "KHONG_DAT df"; exit 3; }
  [ "$PA" -ge $((2 * DB_SIZE + GIB)) ] || { log "pg_trong=$PA can=$((2 * DB_SIZE + GIB))"; ket "KHONG_DAT thieu_dia"; exit 3; }
  HONG="${D}_hong_$(echo "$RUN" | tr -cd 'A-Za-z0-9' | tr 'A-Z' 'a-z' | tail -c 24)"
  [ "$(tontai "$HONG")" = 0 ] || { ket "KHONG_DAT ten_ban_hong_da_co"; exit 3; }
  OID_GOC=$(oid_cua "$D"); so_nguyen "$OID_GOC" || { ket "KHONG_DAT oid_goc"; exit 3; }; echo "$OID_GOC" > "$OUT/oid-goc.txt"
  log "dung dich vu $SV"; "$DK" stop "$SV" >> "$OUT/nhat-ky.txt" 2>&1
  st=$("$DK" inspect -f '{{.State.Running}}' "$SV" 2>/dev/null)
  [ "$st" = false ] || { ket "KHONG_DAT dich_vu_khong_dung (Running=$st quan sat)"; exit 12; }
  t=0; while :; do doc_dbinfo "$D" || { ket "KHONG_DAT dbinfo (dich vu DUNG, DB chua doi)"; exit 17; }
    [ "$KETNOI" -eq 0 ] && break
    if [ $t -ge "$CHO_KN" ]; then sql_ketnoi_ds "$D" | psqlx postgres "t074-e6v4-kn-$RUN" >> "$OUT/nhat-ky.txt" 2>&1
      ket "CON_KET_NOI $KETNOI (dich vu DUNG, DB chua doi; nguoi truc xu ly roi goi lai)"; exit 17; fi
    sleep "$NGU"; t=$((t+NGU)); done
  echo "ALTER DATABASE \"$D\" RENAME TO \"$HONG\";" | sql_ddl
  [ "$(oid_cua "$HONG")" = "$OID_GOC" ] && [ "$(oid_cua "$D")" = KHONG ] || {
    ket "TRANG_THAI_DB_CHUA_RO sau_doi_ten: $D oid=$(oid_cua "$D"), $HONG oid=$(oid_cua "$HONG"), goc=$OID_GOC (dich vu DUNG)"; exit 16; }
  log "giu ban hien tai la $HONG (oid $OID_GOC)"
  OID_MOI=""
  tra_ve() { # chỉ xóa DB do chính lượt này tạo (OID_MOI); trả bản gốc về tên cũ; xác nhận bằng OID
    local o; o=$(oid_cua "$D")
    if [ -n "$OID_MOI" ] && [ "$o" = "$OID_MOI" ]; then echo "DROP DATABASE \"$D\";" | sql_ddl; o=$(oid_cua "$D"); fi
    if [ "$o" != KHONG ]; then log "ten $D dang mang oid=$o khong phai DB luot nay tao (moi=$OID_MOI) — khong xoa"; return 1; fi
    echo "ALTER DATABASE \"$HONG\" RENAME TO \"$D\";" | sql_ddl
    [ "$(oid_cua "$D")" = "$OID_GOC" ] && [ "$(oid_cua "$HONG")" = KHONG ] || return 1
    log "da tra DB goc (oid $OID_GOC) ve ten $D; dich vu $SV de DUNG"; return 0; }
  bao16() { ket "TRANG_THAI_DB_CHUA_RO $1: $D oid=$(oid_cua "$D"), $HONG oid=$(oid_cua "$HONG"), goc=$OID_GOC, moi=${OID_MOI:-chua_tao} (dich vu DUNG)"; exit 16; }
  bam "$HONG" "$OUT/bam-hong.txt" || { log "bam ban hien tai loi"; tra_ve || bao16 "bam_hong_loi"; ket "KHONG_DAT bam_ban_hien_tai_loi (da tra ten cu; dich vu DUNG)"; exit 13; }
  diff "$CB/bam-nhap.txt" "$OUT/bam-hong.txt" > "$OUT/bang-khac-so-voi-dump.txt"
  log "dong bam khac giua dump va ban hien tai: $(grep -c '^[<>]' "$OUT/bang-khac-so-voi-dump.txt")"
  echo "CREATE DATABASE \"$D\" OWNER \"$CB_OWNER\" TEMPLATE template0 ENCODING '$CB_ENC' LC_COLLATE '$CB_COLL' LC_CTYPE '$CB_CTYPE';" | sql_ddl
  o=$(oid_cua "$D")
  if ! so_nguyen "$o"; then tra_ve || bao16 "tao_db_loi"; ket "KHONG_DAT tao_db (da tra ten cu; dich vu DUNG)"; exit 13; fi
  OID_MOI=$o; echo "$OID_MOI" > "$OUT/oid-moi.txt"
  "$DK" exec -i "$PGC" pg_restore -U postgres --exit-on-error -d "$D" < "$CB/$D.dump" > "$OUT/khoi-phuc.out" 2>&1; rc=$?
  [ $rc -eq 0 ] || { log "pg_restore rc=$rc"; tra_ve || bao16 "pg_restore_loi"; ket "KHONG_DAT pg_restore (da tra ten cu; dich vu DUNG)"; exit 13; }
  bam "$D" "$OUT/bam-sau.txt" || { ket "KHONG_DAT bam_sau_loi_doc (dich vu DUNG; $D = DB moi oid $OID_MOI)"; exit 14; }
  cmp -s "$CB/bam-nhap.txt" "$OUT/bam-sau.txt" || { diff "$CB/bam-nhap.txt" "$OUT/bam-sau.txt" > "$OUT/bam-sau-khac.txt"; ket "KHONG_DAT bam_sau_khac_dump (dich vu DUNG; $D = DB moi oid $OID_MOI)"; exit 14; }
  log "bam sau khoi phuc = bam dump"
  kiem_khoa "$DB" "$D" sau-khoi-phuc && danh_gia "$DB" "$OUT/kiem-sau-khoi-phuc.out" CU >> "$OUT/nhat-ky.txt" \
    || { ket "KHONG_DAT kiem_CU_sau_khoi_phuc (dich vu DUNG)"; exit 14; }
  log "khoi dong $SV"; "$DK" start "$SV" >> "$OUT/nhat-ky.txt" 2>&1
  t=0; while :; do
    st=$("$DK" inspect -f '{{.State.Running}}|{{if .State.Health}}{{.State.Health.Status}}{{else}}khong{{end}}' "$SV" 2>/dev/null)
    case "$st" in "true|healthy"|"true|khong") break;; esac
    [ $t -ge "$CHO_DV" ] && { ket "KHONG_DAT dich_vu_chua_len (quan sat $st; DB da khoi phuc)"; exit 15; }
    sleep "$NGU"; t=$((t+NGU)); done
  log "dich vu $SV: $st; ban hong giu o $HONG (xoa can Minh duyet)"
  ket "DA_KHOI_PHUC"; echo "DA_KHOI_PHUC $DB tu $CB/$D.dump; ban truoc khoi phuc: $HONG"; exit 0;;
# =====================================================================================
kiem)
  tong=0
  uu_tien() { # giữ mã nặng nhất: 5 > 7 > 6 > 8 > 0
    local r; for r in 5 7 6 8; do { [ "$tong" -eq $r ] || [ "$1" -eq $r ]; } && { tong=$r; return; }; done; }
  for d in $DBS; do
    kiem_khoa "$d" "${d}_db" "$d"; rc=$?
    [ $rc -eq 0 ] || { log "LOI_DOC $d rc=$rc"; uu_tien 5; continue; }
    danh_gia "$d" "$OUT/kiem-$d.out" "$MONG" | tee -a "$OUT/nhat-ky.txt"; rc=${PIPESTATUS[0]}
    log "$d mong=$MONG rc=$rc"
    uu_tien "$rc"
  done
  [ $tong -eq 0 ] && ket DAT || ket "KHONG_DAT_$tong"; exit $tong;;
esac
