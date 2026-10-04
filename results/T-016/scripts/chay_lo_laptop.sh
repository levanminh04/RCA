#!/bin/bash
# T-016 S7/S8: chạy tuần tự một danh sách khối trên laptop. Cách dùng: bash chay_lo_laptop.sh <ob|ss>
# Mỗi khối: harness chay_torai.py, có --thu-thap. Ghi giờ bắt đầu/kết thúc từng khối vào runs/lo-<ds>.log.
DS=$1
R=/d/RCA-flashticket
P=/d/RCA-ext/envs/py38-rcdlock/Scripts/python.exe
H=$R/results/T-016/scripts/chay_torai.py
W=D:/RCA-ext/work/T-016
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONIOENCODING=utf-8
if [ "$DS" = ob ]; then D=D:/RCA-ext/data/torai-OB; N=torai-ob; else D=D:/RCA-ext/data/torai-SS; N=torai-ss; fi
LOG=$R/results/T-016/runs/lo-$DS.log
khoi() {
  ten=$1; shift
  if [ -e $W/$ten/XONG ]; then echo "$(date '+%F %T') BO-QUA $ten" >> $LOG; return; fi
  echo "$(date '+%F %T') BAT-DAU $ten $*" >> $LOG
  $P $H --data $D --dataset $N --ra $W/$ten --thu-thap "$@" > $W/$ten.out 2>&1; rc=$?
  echo "$(date '+%F %T') XONG $ten rc=$rc" >> $LOG
  [ $rc -eq 0 ] && touch $W/$ten/XONG
}
S=0,1,2,3,4
khoi s7-$DS-goc-len10 --method torai --length 10 --seeds $S
khoi s7-$DS-sua-len10 --method torai_sua --length 10 --seeds $S
khoi s7-$DS-goc-len20 --method torai --length 20 --seeds $S
khoi s7-$DS-sua-len20 --method torai_sua --length 20 --seeds $S
khoi s8-$DS-goc-len10-placebo --method torai --length 10 --seeds 0 --placebo
khoi s8-$DS-sua-len10-placebo --method torai_sua --length 10 --seeds 0 --placebo
khoi s8-$DS-goc-len10-hoanvi --method torai --length 10 --seeds 0,1,2 --hoan-vi-cot 12345
khoi s8-$DS-sua-len10-hoanvi --method torai_sua --length 10 --seeds 0,1,2 --hoan-vi-cot 12345
if [ "$DS" = ob ]; then
  khoi s7-ob-suaA-len10 --method torai_sua_a --length 10 --seeds 0
  khoi s7-ob-goc-len10-ML --method torai --length 10 --seeds $S --khong-trace
  khoi s7-ob-sua-len10-ML --method torai_sua --length 10 --seeds $S --khong-trace
fi
echo "$(date '+%F %T') HET" >> $LOG
