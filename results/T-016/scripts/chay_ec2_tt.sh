#!/bin/bash
# T-016 S10 (thay đổi 4): RCD và TORAI gốc/sửa, cửa sổ 10, seed 0, trên 30 ca TT dev đã chứng minh trùng. Một tiến trình mỗi lúc.
B=~/rca/T-016; P=$B/envs/py38/bin/python; H=$B/repo/results/T-016/scripts/chay_torai.py
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONIOENCODING=utf-8
export XDG_CACHE_HOME=$B/cache MPLCONFIGDIR=$B/cache/mpl TMPDIR=$B/tmp PYTHONPYCACHEPREFIX=$B/cache/pyc
D=$B/data/tt-dev30/torai-TT
for x in "s11-tt30-torai-goc-len10 torai" "s11-tt30-torai-sua-len10 torai_sua" "s11-tt30-rcd-len10 rcd"; do
  set -- $x
  while [ $(ps -eo pcpu,args --no-headers | awk '$1>50' | grep -v rca/T-016 | grep -v " ps " | wc -l) -gt 0 ]; do echo "$(date -u +%FT%TZ) CHO"; sleep 60; done
  echo "$(date -u +%FT%TZ) BAT-DAU $1"; uptime
  ( cd $B && $P $H --data $D --dataset torai-tt --method $2 --length 10 --seeds 0 --ra $B/runs/$1 --ngan-sach-s 3600 > $B/runs/$1.out 2>&1 )
  echo "$(date -u +%FT%TZ) XONG $1 rc=$?"
done
echo "$(date -u +%FT%TZ) HET"
