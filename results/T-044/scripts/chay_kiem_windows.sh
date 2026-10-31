#!/usr/bin/env bash
# Chạy lại phép kiểm T-044 trên Windows (Git Bash). Ghi vào results/T-044/runs/<lượt>.
# Tên lượt và cây so: TX_LUOT, TD_LUOT, DB_LUOT, KH_LUOT, GOC_CU (mặc định là lượt 3: 004/005/005/005, 253dbe46).
set -u
R=/d/RCA-flashticket
PY=D:/RCA-ext/envs/py312-pin/Scripts/python.exe
export PYTHONPATH="D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages"
export PYTHONIOENCODING=utf-8
GOC_CU=${GOC_CU:-253dbe46}  # cây so bản ghi trước sửa
TX=$R/results/T-044/runs/${TX_LUOT:-test-xanh-004}
TD=$R/results/T-044/runs/${TD_LUOT:-tat-dinh-005}
DB=$R/results/T-044/runs/${DB_LUOT:-dot-bien-005}
KH=$R/results/T-044/runs/${KH_LUOT:-kiem-hash-t043-005}
mkdir -p "$TX" "$TD" "$KH"
cd $R/results/T-044/tests
t0=$(date +%s)
PYTHONHASHSEED=0 M1_KET_QUA="$TX/ket-qua.json" $PY -B -m pytest -v -p no:cacheprovider -W ignore > "$TX/stdout.txt" 2>&1
echo "giay test $(( $(date +%s) - t0 ))" > "$TX/thoi-gian.txt"
tail -1 "$TX/stdout.txt"
for hs in 0 1 2; do
  PYTHONHASHSEED=$hs $PY -B $R/results/T-044/scripts/tat_dinh.py > "$TD/ban-ghi-h$hs.json"
  for x in 0 1 2 3; do
    if [ $x = 0 ]; then XA=""; else XA=$x; fi
    PYTHONHASHSEED=$hs M1_XAO=$XA M1_KET_QUA="$TD/pytest-h$hs-x$x.json" $PY -B -m pytest -q -p no:cacheprovider -W ignore > "$TD/pytest-h$hs-x$x.txt" 2>&1
  done
done
# so với cây trước sửa: commit GOC_CU, hoặc thư mục CAY_CU (cây chưa commit, chụp trước khi sửa; GOC_CU là nhãn)
CU=$(mktemp -d)
if [ -n "${CAY_CU:-}" ]; then
  CUW="$CAY_CU"
else
  git -C $R archive $GOC_CU src results/T-043 results/T-044 | tar -x -C "$CU"
  CUW=$(cygpath -m "$CU")
fi
PYTHONHASHSEED=0 $PY -B $R/results/T-044/scripts/so_ban_ghi_truoc_sau.py "$CUW" > "$TD/bo-truong-moi-$GOC_CU.json"
PYTHONHASHSEED=0 $PY -B $R/results/T-044/scripts/so_ban_ghi_truoc_sau.py "D:/RCA-flashticket" > "$TD/bo-truong-moi-sau-sua.json"
$PY -B $R/results/T-044/scripts/so_truong_ban_ghi.py "$CUW" "D:/RCA-flashticket" ${SO_DAY_DU:+--day-du} > "$TD/so-truong-$GOC_CU.json"
rm -rf "$CU"
cd $R
$PY -B results/T-044/scripts/kiem_hash_t043.py > "$KH/stdout.txt" 2>&1
tail -1 "$KH/stdout.txt"
$PY -B results/T-044/scripts/dot_bien.py "$DB" > "$DB.stdout.txt" 2>&1; mv "$DB.stdout.txt" "$DB/stdout.txt"
echo "dot bien xong: $?"
