#!/usr/bin/env bash
# T-034 E2 luot 003: hai chuoi FF chay TUAN TU (moi luc mot tien trinh), khong dat bien luong BLAS nhu luot goc T-033.
set -u
unset OPENBLAS_NUM_THREADS OMP_NUM_THREADS MKL_NUM_THREADS
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8 TMPDIR=/home/ubuntu/rca/T-034/e2/tmp XDG_CACHE_HOME=/home/ubuntu/rca/T-034/e2/cache
cd "/home/ubuntu/rca/T-034/e2"
P=/home/ubuntu/rca/T-025/envs/main/bin/python
for C in dev-3ae0a6c15a dev-ba831dbeb8; do
  $P -B -X utf8 scripts/e2_bocpd_log_v3.py chain /home/ubuntu/rca/T-033/runs/bocpd-rest-001/$C--full.npz runs/e2-003 $C--FF /home/ubuntu/rca/T-025/src/baro inputs/zero-lineage-summary-001.json > "/home/ubuntu/rca/T-034/e2/runs/e2-003-launch/$C--FF.out" 2> "/home/ubuntu/rca/T-034/e2/runs/e2-003-launch/$C--FF.err"
  echo "$C FF exit=$? $(date -u +%FT%TZ)" >> "/home/ubuntu/rca/T-034/e2/runs/e2-003-launch/done.txt"
done
