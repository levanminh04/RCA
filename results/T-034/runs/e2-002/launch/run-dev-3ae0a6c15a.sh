#!/usr/bin/env bash
# T-034 E2 luot 002 (thiet-ke-hai-phep-kiem.md, E2 va Muc noi 3). Khong dat bien luong BLAS: dung cau hinh cua luot goc T-033.
set -u
unset OPENBLAS_NUM_THREADS OMP_NUM_THREADS MKL_NUM_THREADS
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8 TMPDIR=/home/ubuntu/rca/T-034/e2/tmp XDG_CACHE_HOME=/home/ubuntu/rca/T-034/e2/cache
cd "/home/ubuntu/rca/T-034/e2"
P=/home/ubuntu/rca/T-025/envs/main/bin/python
$P -B -X utf8 scripts/e2_bocpd_log_v3.py chain /home/ubuntu/rca/T-033/runs/bocpd-factorial-rest-001/dev-3ae0a6c15a--PF.npz runs/e2-002 dev-3ae0a6c15a--PF /home/ubuntu/rca/T-025/src/baro inputs/zero-lineage-summary-001.json > "/home/ubuntu/rca/T-034/e2/runs/e2-002-launch/dev-3ae0a6c15a--PF.out" 2> "/home/ubuntu/rca/T-034/e2/runs/e2-002-launch/dev-3ae0a6c15a--PF.err"
echo "PF exit=$? $(date -u +%FT%TZ)" > "/home/ubuntu/rca/T-034/e2/runs/e2-002-launch/dev-3ae0a6c15a.done.txt"
$P -B -X utf8 scripts/e2_bocpd_log_v3.py chain /home/ubuntu/rca/T-033/runs/bocpd-rest-001/dev-3ae0a6c15a--full.npz runs/e2-002 dev-3ae0a6c15a--FF /home/ubuntu/rca/T-025/src/baro inputs/zero-lineage-summary-001.json > "/home/ubuntu/rca/T-034/e2/runs/e2-002-launch/dev-3ae0a6c15a--FF.out" 2> "/home/ubuntu/rca/T-034/e2/runs/e2-002-launch/dev-3ae0a6c15a--FF.err"
echo "FF exit=$? $(date -u +%FT%TZ)" >> "/home/ubuntu/rca/T-034/e2/runs/e2-002-launch/dev-3ae0a6c15a.done.txt"
