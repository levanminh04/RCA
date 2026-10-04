#!/bin/bash
# T-016 S11: chạy tuần tự các khối trên EC2. Mỗi lúc một tiến trình nặng. Trước mỗi khối: nếu có tiến trình
# khác (không thuộc ~/rca/T-016) dùng > 50 % CPU thì chờ, ghi dòng CHO. Ghi uptime, free trước mỗi khối.
B=~/rca/T-016
P=$B/envs/py38/bin/python
H=$B/repo/results/T-016/scripts/chay_torai.py
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONIOENCODING=utf-8
export XDG_CACHE_HOME=$B/cache MPLCONFIGDIR=$B/cache/mpl TMPDIR=$B/tmp PYTHONPYCACHEPREFIX=$B/cache/pyc
cho_may_ranh() {
  while true; do
    n=$(ps -eo pcpu,args --no-headers | awk '$1>50' | grep -v "rca/T-016" | grep -v " ps " | wc -l)
    [ "$n" -eq 0 ] && break
    echo "$(date -u +%FT%TZ) CHO may ban: $(ps -eo pid,pcpu,args --sort=-pcpu --no-headers | head -1 | cut -c1-150)"
    sleep 60
  done
}
khoi() {
  ten=$1; shift
  if [ -e $B/runs/$ten/XONG ]; then echo "$(date -u +%FT%TZ) BO-QUA $ten (da xong)"; return; fi
  cho_may_ranh
  echo "$(date -u +%FT%TZ) BAT-DAU $ten"; uptime; free -m | head -2
  ( cd $B && $P $H --ra $B/runs/$ten "$@" > $B/runs/$ten.out 2>&1 ); rc=$?
  echo "$(date -u +%FT%TZ) XONG $ten rc=$rc"; uptime
  [ $rc -eq 0 ] && touch $B/runs/$ten/XONG
}
khoi s11-torai-goc-ob-len10 --data $B/data/torai-OB --dataset torai-ob --method torai --length 10 --seeds 0
khoi s11-torai-goc-ss-len10 --data $B/data/torai-SS --dataset torai-ss --method torai --length 10 --seeds 0
khoi s11-torai-sua-ob-len10 --data $B/data/torai-OB --dataset torai-ob --method torai_sua --length 10 --seeds 0
khoi s11-torai-sua-ss-len10 --data $B/data/torai-SS --dataset torai-ss --method torai_sua --length 10 --seeds 0
khoi s11-tt-torai-goc-len10 --data $B/data/torai-TT --dataset torai-tt --method torai --length 10 --seeds 0
khoi s11-tt-torai-sua-len10 --data $B/data/torai-TT --dataset torai-tt --method torai_sua --length 10 --seeds 0
khoi s11-tt-rcd-len10 --data $B/data/torai-TT --dataset torai-tt --method rcd --length 10 --seeds 0
khoi s11-rcd-ss-len10 --data $B/data/torai-SS --dataset torai-ss --method rcd --length 10 --seeds 0 --ngan-sach-s 10800
khoi s11-rcd-ob-len20 --data $B/data/torai-OB --dataset torai-ob --method rcd --length 20 --seeds 0 --thu-tu-ca $B/repo/results/T-016/runs/s11-thu-tu-rcd-ob-len20.txt --ngan-sach-s 10800
echo "$(date -u +%FT%TZ) HET"
