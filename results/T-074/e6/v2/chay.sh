#!/bin/bash
# T-074 E6 v2 — bộ chạy. Dùng trên exp-app (pha ghi chỉ khi được giao):
#   bash chay.sh thuan  <A|B>                     # ghi theo thứ tự event → booking → ticket → payment
#   bash chay.sh nghich <A|B> <db...>             # đảo, CHỈ các DB nêu tên (thuộc lượt đã xác định)
#   bash chay.sh kiem   <A|B> <CU|DICH|DOC> [db…] # chỉ SELECT
#   bash chay.sh kiem-khoa <A|B> <CU|DICH|DOC> [db…]  # như kiem nhưng FOR SHARE: chờ giao dịch ghi kết thúc (chỉ pha ghi, nhánh 50%)
# Mã thoát: 0 đạt; 2 sai cách gọi/thư mục lượt đã có; 3 lỗi SQL (giao dịch đã rollback); 4 MẤT KẾT NỐI (trạng thái COMMIT chưa biết);
#           5 lỗi psql khác; 6 trường sai trạng thái; 7 thiếu/trùng trường; 8 dòng PHU sai.
# Dừng ngay ở DB lỗi đầu tiên; không chạy DB sau. Mỗi lượt một thư mục riêng (không ghi đè).
set -u
HERE=$(cd "$(dirname "$0")" && pwd)
CHE_DO=${1:-}; BT=${2:-}
case "$CHE_DO" in thuan|nghich|kiem|kiem-khoa) ;; *) echo "SAI_CACH_GOI che_do"; exit 2;; esac
case "$BT" in A|B) ;; *) echo "SAI_CACH_GOI bien_the"; exit 2;; esac
shift 2
MONG=""
if [ "$CHE_DO" = kiem ] || [ "$CHE_DO" = kiem-khoa ]; then
  MONG=${1:-}; case "$MONG" in CU|DICH|DOC) ;; *) echo "SAI_CACH_GOI mong"; exit 2;; esac; shift
fi
if [ "$CHE_DO" = nghich ] && [ $# -eq 0 ]; then echo "SAI_CACH_GOI nghich can danh sach DB"; exit 2; fi
DBS=${*:-event booking ticket payment}
for db in $DBS; do case "$db" in event|booking|ticket|payment) ;; *) echo "SAI_CACH_GOI db=$db"; exit 2;; esac; done
SQLD="$HERE/sql/$BT"
RUN=${RUN_ID:-$(date -u +%Y%m%dT%H%M%SZ)-$$}
OUT="${E6_OUT:-/home/ubuntu/t074/e6}/$CHE_DO-$BT-$RUN"
if [ -e "$OUT" ]; then echo "SAI_CACH_GOI thu muc luot da co: $OUT"; exit 2; fi
mkdir -p "$OUT" || exit 2
# PSQL có thể thay bằng chương trình giả lập khi thử (biến môi trường PSQL); mặc định là psql trong container postgres.
chay_psql() {  # $1 = db (event…), $2 = app name; stdin = SQL
  if [ -n "${PSQL:-}" ]; then "$PSQL" "$1_db" "$2"
  else docker exec -i -e PGAPPNAME="$2" flash-ticket-infra-postgres-1 psql -U postgres -X -q -At -v ON_ERROR_STOP=1 -d "$1_db"; fi
}
echo "luot=$RUN che_do=$CHE_DO bien_the=$BT dbs=$DBS mong=$MONG bat_dau=$(date -u +%FT%T.%NZ)" > "$OUT/luot.txt"
for db in $DBS; do
  case "$CHE_DO" in thuan) f="$SQLD/thuan-$db.sql";; nghich) f="$SQLD/nghich-$db.sql";; kiem) f="$SQLD/kiem-$db.sql";; kiem-khoa) f="$SQLD/kiem-khoa-$db.sql";; esac
  app="t074-e6-$CHE_DO-$BT-$RUN-$db"
  echo "BAT_DAU $db $(date -u +%FT%T.%NZ) app=$app" >> "$OUT/tien-do.txt"
  chay_psql "$db" "$app" < "$f" > "$OUT/$db.out" 2> "$OUT/$db.err"; rc=$?
  echo "KET_THUC $db rc=$rc $(date -u +%FT%T.%NZ)" >> "$OUT/tien-do.txt"
  case $rc in
    0) ;;
    3) echo "LOI_SQL db=$db (giao dich da rollback; cac DB truoc da xong — xem tien-do.txt)"; echo "LOI_SQL $db" > "$OUT/KET_QUA"; exit 3;;
    2) { echo "MAT_KET_NOI luot=$RUN db=$db app=$app utc=$(date -u +%FT%T.%NZ)"; grep '^PHIEN ' "$OUT/$db.out" || echo "PHIEN (chua in)"; } > "$OUT/MAT_KET_NOI"
       echo "MAT_KET_NOI db=$db — trang thai COMMIT chua biet: tim phien theo application_name, cho ket thuc, roi 'kiem-khoa'"; exit 4;;
    *) echo "LOI_PSQL db=$db rc=$rc"; echo "LOI_PSQL $db $rc" > "$OUT/KET_QUA"; exit 5;;
  esac
  if [ "$CHE_DO" = thuan ] || [ "$CHE_DO" = nghich ]; then
    grep -q "^DA_COMMIT ${db}_db " "$OUT/$db.out" || { echo "KHONG_THAY_DA_COMMIT db=$db"; echo "KHONG_THAY_DA_COMMIT $db" > "$OUT/KET_QUA"; exit 5; }
  fi
done
if [ "$CHE_DO" = thuan ] || [ "$CHE_DO" = nghich ]; then echo "DAT" > "$OUT/KET_QUA"; echo "DAT $CHE_DO $BT luot=$RUN"; exit 0; fi
# ---- đánh giá kiểm: đúng một dòng cho mỗi trường thuộc các DB đã kiểm; trạng thái đúng mong đợi; PHU đúng
cat "$OUT"/*.out > "$OUT/tat-ca.txt"
loi=0; thieu=0
while IFS='|' read -r ten mong_dich; do
  db=${ten%%.*}; case " $DBS " in *" $db "*) ;; *) continue;; esac
  n=$(grep -c "^TRUONG|$ten|" "$OUT/tat-ca.txt")
  if [ "$n" -ne 1 ]; then echo "SO_DONG_TRUONG $ten=$n"; thieu=1; continue; fi
  st=$(grep "^TRUONG|$ten|" "$OUT/tat-ca.txt" | cut -d'|' -f3-)
  case "$MONG" in
    CU) want=CU;; DICH) want=$mong_dich;;
    DOC) case "$st" in CU|DICH) want=$st;; *) want=CU_HOAC_DICH;; esac;;
  esac
  echo "$ten=$st mong=$want"
  [ "$st" = "$want" ] || loi=1
done < "$SQLD/truong.txt"
# trường lạ (không có trong danh sách) cũng là lỗi
lag=$(grep '^TRUONG|' "$OUT/tat-ca.txt" | cut -d'|' -f2 | sort | uniq -d | wc -l)
[ "$lag" -eq 0 ] || { echo "TRUONG_TRUNG"; thieu=1; }
phu_loi=0
while IFS='|' read -r ten v; do
  db=${ten%%.*}; case " $DBS " in *" $db "*) ;; *) continue;; esac
  got=$(grep "^PHU|$ten|" "$OUT/tat-ca.txt" | cut -d'|' -f3)
  n=$(grep -c "^PHU|$ten|" "$OUT/tat-ca.txt")
  echo "PHU $ten=$got mong=$v"
  { [ "$n" -eq 1 ] && [ "$got" = "$v" ]; } || phu_loi=1
done < "$SQLD/phu.txt"
grep '^BAO|' "$OUT/tat-ca.txt"
if [ $thieu -ne 0 ]; then echo "THIEU_TRUNG_TRUONG" > "$OUT/KET_QUA"; exit 7; fi
if [ $loi -ne 0 ]; then echo "SAI_TRANG_THAI" > "$OUT/KET_QUA"; exit 6; fi
if [ $phu_loi -ne 0 ]; then echo "PHU_SAI" > "$OUT/KET_QUA"; exit 8; fi
echo "DAT" > "$OUT/KET_QUA"; echo "DAT kiem $BT $MONG luot=$RUN"; exit 0
