#!/bin/bash
# T-016 S10: TORAI gốc/sửa × cửa sổ 10/20 × 3 seed trên 30 ca dev torai-TT đã chứng minh trùng (runs/s10-cung-ca.json).
R=/d/RCA-flashticket
P=/d/RCA-ext/envs/py38-rcdlock/Scripts/python.exe
H=$R/results/T-016/scripts/chay_torai.py
W=D:/RCA-ext/work/T-016
D=D:/RCA-ext/work/T-016/data/torai-TT
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONIOENCODING=utf-8
LOG=$R/results/T-016/runs/lo-tt.log
khoi() {
  ten=$1; shift
  if [ -e $W/$ten/XONG ]; then echo "$(date '+%F %T') BO-QUA $ten" >> $LOG; return; fi
  echo "$(date '+%F %T') BAT-DAU $ten $*" >> $LOG
  $P $H --data $D --dataset torai-tt --ra $W/$ten --thu-thap "$@" > $W/$ten.out 2>&1; rc=$?
  echo "$(date '+%F %T') XONG $ten rc=$rc" >> $LOG
  [ $rc -eq 0 ] && touch $W/$ten/XONG
}
khoi s10-tt-goc-len10 --method torai --length 10 --seeds 0,1,2
khoi s10-tt-sua-len10 --method torai_sua --length 10 --seeds 0,1,2
khoi s10-tt-goc-len20 --method torai --length 20 --seeds 0,1,2
khoi s10-tt-sua-len20 --method torai_sua --length 20 --seeds 0,1,2
echo "$(date '+%F %T') HET" >> $LOG
