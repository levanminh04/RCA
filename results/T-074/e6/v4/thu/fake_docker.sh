#!/bin/bash
# docker GIẢ LẬP cho thử v4/chay.sh trên laptop — KHÔNG kết nối máy hay DB nào. (v4 = bản v3 + OID, lỗi DDL, lỗi băm bản hỏng, dịch vụ không dừng)
# Trạng thái ở $FAKE: db/<tên DB>/{truong,phu,hash,dml,oid}; svc_<container>; df_pg; size; các file điều khiển (xem chay_thu.sh).
set -u
F=$FAKE
echo "docker $*" >> "$F/goi.log"
cmd=$1; shift
case $cmd in
  stop)    n=$1; [ -f "$F/stop_khong_dung" ] || echo false > "$F/svc_$n"; echo "$n"; exit 0;;
  start)   n=$1; cat "$F/start_state" 2>/dev/null > "$F/svc_$n" || echo true > "$F/svc_$n"; [ -s "$F/svc_$n" ] || echo true > "$F/svc_$n"; echo "$n"; exit 0;;
  inspect) fmt=$2; n=$3; st=$(cat "$F/svc_$n" 2>/dev/null || echo true)
           case "$fmt" in *Health*) echo "$st|$(cat "$F/health" 2>/dev/null || echo healthy)";; *) echo "$st";; esac; exit 0;;
  exec)    ;;
  *)       echo "fake: lenh la $cmd" >&2; exit 99;;
esac
app=""
while [ $# -gt 0 ]; do case $1 in -i) shift;; -e) app=${2#PGAPPNAME=}; shift 2;; -*) shift;; *) break;; esac; done
shift   # container
prog=$1; shift
D=""; a=("$@"); for ((i=0; i<${#a[@]}; i++)); do [ "${a[$i]}" = -d ] && D=${a[$((i+1))]}; done
DD="$F/db/$D"
dem() { [ -f "$1" ] && cat "$1" || echo "$2"; }
ap_dung() { # $1 = all|mot : đổi trạng thái trường sang đích theo truong.txt
  awk -F'|' -v m="$1" 'FNR==NR {dich[$1]=$2; next} { if (m=="all" || FNR==1) print $1 "|" dich[$1]; else print }' "$FAKE_TRUONG" "$DD/truong" > "$DD/truong.n" && mv "$DD/truong.n" "$DD/truong"
  echo "BANG|z.da_ghi|1|ghi" >> "$DD/hash"; echo $(( $(cat "$DD/dml") + 1 )) > "$DD/dml"; }
case $prog in
  df) echo "Filesystem 1B-blocks Used Available Use% Mounted on"; echo "overlay 0 0 $(cat "$F/df_pg") 0% /var/lib/postgresql/data"; exit 0;;
  pg_dump)
    [ -d "$DD" ] || { echo "pg_dump: database \"$D\" does not exist" >&2; exit 1; }
    rc=$(dem "$F/dump_rc" 0); [ "$rc" = 0 ] || exit "$rc"
    echo FAKEDUMP; for k in truong phu hash dml; do echo "##$k"; cat "$DD/$k"; done
    [ -f "$F/ghi_xen" ] && echo "BANG|booking_schema.tbl_orders|9|app_ghi_xen" >> "$DD/hash"
    exit 0;;
  pg_restore)
    in=$(cat); [ "$(printf '%s\n' "$in" | head -1)" = FAKEDUMP ] || { echo "pg_restore: not a valid archive" >&2; exit 1; }
    for x in "$@"; do [ "$x" = -l ] && { echo "; Archive"; echo "1; 0 0 TABLE DATA s t1"; echo "2; 0 0 TABLE DATA s t2"; exit 0; }; done
    [ -d "$DD" ] || { echo "pg_restore: database \"$D\" does not exist" >&2; exit 1; }
    rc=$(dem "$F/restore_rc" 0)
    printf '%s\n' "$in" | awk -v d="$DD" 'NR==1 {next} /^##/ {k=substr($0,3); printf "" > (d "/" k); next} {print >> (d "/" k)}'
    if [ "$rc" != 0 ]; then echo "BANG|z.do_dang|0|x" >> "$DD/hash"; echo "pg_restore: error" >&2; exit "$rc"; fi
    exit 0;;
  psql) ;;
  *) echo "fake: chuong trinh la $prog" >&2; exit 98;;
esac
SQL=$(cat)
if [ "$D" != postgres ] && [ ! -d "$DD" ]; then echo "psql: FATAL: database \"$D\" does not exist" >&2; exit 2; fi
ten_trong() { printf '%s\n' "$SQL" | sed -n "s/.*$1 *\"\{0,1\}\([A-Za-z0-9_]*\)\"\{0,1\}.*/\1/p" | head -1; }
case "$SQL" in
  *"-- E6V3 HASH"*)   case "$D" in *_hong_*) [ -f "$F/bam_loi_hong" ] && { echo "ERROR" >&2; exit 3; };; esac; cat "$DD/hash"; echo "SEQ|s.seq1|42"; echo "SO_BANG|$(grep -c '^BANG|' "$DD/hash")"; exit 0;;
  *"-- E6V3 DBINFO"*) echo "DBINFO|$(dem "$F/size" 50000000)|postgres|UTF8|C.UTF-8|C.UTF-8|$(dem "$F/acl" NULL)|0"; echo "KETNOI|$(dem "$F/ketnoi" 0)"; exit 0;;
  *"-- E6V3 DML"*)    [ -f "$F/dml_tang" ] && echo $(( $(cat "$DD/dml") + 1 )) > "$DD/dml"; echo "DML|$(cat "$DD/dml")"; exit 0;;
  *"-- E6V3 TONTAI"*) n=$(printf '%s\n' "$SQL" | sed -n "s/.*datname='\([^']*\)'.*/\1/p"); [ -d "$F/db/$n" ] && echo "TONTAI|1" || echo "TONTAI|0"; exit 0;;
  *"-- E6V3 PHIEN"*)  n=$(dem "$F/phien_con" 0); echo "PHIEN_CON|$n"; [ "$n" -gt 0 ] && [ ! -f "$F/phien_vinh_vien" ] && echo $((n-1)) > "$F/phien_con"; exit 0;;
  *"-- E6V3 OID"*)    n=$(printf '%s\n' "$SQL" | sed -n "s/.*datname='\([^']*\)'.*/\1/p"); [ -f "$F/db/$n/oid" ] && echo "OID|$(cat "$F/db/$n/oid")" || echo "OID|KHONG"; exit 0;;
  *"-- E6V3 KETNOI_DS"*) echo "KN|777|ung-dung|10.0.0.5|idle"; exit 0;;
  *"CREATE DATABASE"*) n=$(ten_trong "CREATE DATABASE"); [ -d "$F/db/$n" ] && { echo "ERROR: exists" >&2; exit 3; }
       case "$n" in e6n_*) ;; *) [ -f "$F/create_loi" ] && { echo "ERROR: create" >&2; exit 3; };; esac
       mkdir -p "$F/db/$n"; : > "$F/db/$n/truong"; : > "$F/db/$n/phu"; : > "$F/db/$n/hash"; echo 0 > "$F/db/$n/dml"
       o=$(( $(dem "$F/oid_dem" 50000) + 1 )); echo $o > "$F/oid_dem"; echo $o > "$F/db/$n/oid"; exit 0;;
  *"DROP DATABASE"*)  n=$(printf '%s\n' "$SQL" | sed -n 's/.*DROP DATABASE \(IF EXISTS \)\{0,1\}"\([^"]*\)".*/\2/p'); [ -f "$F/drop_rc" ] && exit "$(cat "$F/drop_rc")"; rm -rf "$F/db/$n"; exit 0;;
  *"ALTER DATABASE"*) a1=$(printf '%s\n' "$SQL" | sed -n 's/.*ALTER DATABASE "\([^"]*\)" RENAME TO "\([^"]*\)".*/\1/p')
       a2=$(printf '%s\n' "$SQL" | sed -n 's/.*ALTER DATABASE "\([^"]*\)" RENAME TO "\([^"]*\)".*/\2/p')
       k=$(( $(dem "$F/alter_dem" 0) + 1 )); echo $k > "$F/alter_dem"
       [ -f "$F/alter_loi_lan_$k" ] && { echo "ERROR: rename" >&2; exit 3; }
       mv "$F/db/$a1" "$F/db/$a2"; exit 0;;
  *"UPDATE "*)
    echo "PHIEN 4242 $app $(date -u +%FT%T)"
    mode=$(dem "$F/thuan_mode" ok)
    case $mode in
      ok)             ap_dung all; echo "DA_COMMIT $D $(date -u +%FT%T)"; exit 0;;
      ok_bao_doi)     ap_dung all; sed -i 's/^BAO|booking.purchased|.*/BAO|booking.purchased|41706/' "$DD/phu"; echo "DA_COMMIT $D x"; exit 0;;
      loi_truoc)      echo "ERROR: gia tri da khoa khac buoc 1" >&2; exit 3;;
      loi_sau_commit) ap_dung all; echo "ERROR: canceling statement due to user request" >&2; exit 3;;
      thieu_dau)      ap_dung all; exit 0;;
      mat_truoc)      echo "server closed the connection unexpectedly" >&2; exit 2;;
      mat_sau_commit) ap_dung all; echo "server closed the connection unexpectedly" >&2; exit 2;;
      mot_phan)       ap_dung mot; exit 3;;
      docker_loi)     echo "Error response from daemon" >&2; exit 125;;
    esac;;
  *"TRUONG|"*)
    if [ -f "$F/kiem_out" ]; then cat "$F/kiem_out"; exit "$(dem "$F/kiem_rc" 0)"; fi
    echo "PHIEN 4243 $app x"; awk '{print "TRUONG|" $0}' "$DD/truong"; cat "$DD/phu"; exit "$(dem "$F/kiem_rc" 0)";;
esac
echo "fake: SQL khong nhan dang" >&2; exit 97
