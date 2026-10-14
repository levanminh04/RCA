#!/usr/bin/env bash
# T-034 E2 (thiet-ke-hai-phep-kiem.md, E2). Chi doc nguon T-033/T-025; chi ghi duoi /home/ubuntu/rca/T-034/e2.
set -u
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 TMPDIR=/home/ubuntu/rca/T-034/e2/tmp XDG_CACHE_HOME=/home/ubuntu/rca/T-034/e2/cache
cd "/home/ubuntu/rca/T-034/e2"
P=/home/ubuntu/rca/T-025/envs/main/bin/python
$P -B -X utf8 scripts/e2_bocpd_log.py chain /home/ubuntu/rca/T-033/runs/bocpd-factorial-rest-001/dev-ba831dbeb8--PF.npz runs/e2-001 dev-ba831dbeb8--PF /home/ubuntu/rca/T-025/src/baro inputs/zero-lineage-summary-001.json > "/home/ubuntu/rca/T-034/e2/runs/e2-001-launch/dev-ba831dbeb8--PF.out" 2> "/home/ubuntu/rca/T-034/e2/runs/e2-001-launch/dev-ba831dbeb8--PF.err"
echo "PF exit=$? $(date -u +%FT%TZ)" > "/home/ubuntu/rca/T-034/e2/runs/e2-001-launch/dev-ba831dbeb8.done.txt"
$P -B -X utf8 scripts/e2_bocpd_log.py chain /home/ubuntu/rca/T-033/runs/bocpd-rest-001/dev-ba831dbeb8--full.npz runs/e2-001 dev-ba831dbeb8--FF /home/ubuntu/rca/T-025/src/baro inputs/zero-lineage-summary-001.json > "/home/ubuntu/rca/T-034/e2/runs/e2-001-launch/dev-ba831dbeb8--FF.out" 2> "/home/ubuntu/rca/T-034/e2/runs/e2-001-launch/dev-ba831dbeb8--FF.err"
echo "FF exit=$? $(date -u +%FT%TZ)" >> "/home/ubuntu/rca/T-034/e2/runs/e2-001-launch/dev-ba831dbeb8.done.txt"
