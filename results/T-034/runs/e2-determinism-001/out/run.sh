#!/usr/bin/env bash
# T-034 E2: kiem tat dinh cua ban goc theo cau hinh luong BLAS (thiet ke, Muc noi 2). Chi doc nguon.
set -u
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8 TMPDIR=/home/ubuntu/rca/T-034/e2/tmp XDG_CACHE_HOME=/home/ubuntu/rca/T-034/e2/cache
cd "/home/ubuntu/rca/T-034/e2"
P=/home/ubuntu/rca/T-025/envs/main/bin/python
N=/home/ubuntu/rca/T-033/runs/bocpd-factorial-rest-001/dev-ba831dbeb8--PF.npz
( unset OPENBLAS_NUM_THREADS OMP_NUM_THREADS MKL_NUM_THREADS; $P -B -X utf8 scripts/e2_bocpd_log_v2.py determinism $N /home/ubuntu/rca/T-034/e2/runs/e2-determinism-001/ba83-PF--threads-unset.json /home/ubuntu/rca/T-025/src/baro > /home/ubuntu/rca/T-034/e2/runs/e2-determinism-001/ba83-PF--threads-unset.out 2> /home/ubuntu/rca/T-034/e2/runs/e2-determinism-001/ba83-PF--threads-unset.err ) &
( export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1; $P -B -X utf8 scripts/e2_bocpd_log_v2.py determinism $N /home/ubuntu/rca/T-034/e2/runs/e2-determinism-001/ba83-PF--threads-1.json /home/ubuntu/rca/T-025/src/baro > /home/ubuntu/rca/T-034/e2/runs/e2-determinism-001/ba83-PF--threads-1.out 2> /home/ubuntu/rca/T-034/e2/runs/e2-determinism-001/ba83-PF--threads-1.err ) &
wait
( export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1; $P -B -X utf8 scripts/e2_bocpd_log_v2.py determinism $N /home/ubuntu/rca/T-034/e2/runs/e2-determinism-001/ba83-PF--threads-1-repeat.json /home/ubuntu/rca/T-025/src/baro > /home/ubuntu/rca/T-034/e2/runs/e2-determinism-001/ba83-PF--threads-1-repeat.out 2> /home/ubuntu/rca/T-034/e2/runs/e2-determinism-001/ba83-PF--threads-1-repeat.err ) &
( unset OPENBLAS_NUM_THREADS OMP_NUM_THREADS MKL_NUM_THREADS; $P -B -X utf8 scripts/e2_bocpd_log_v2.py determinism /home/ubuntu/rca/T-033/runs/bocpd-factorial-rest-001/dev-3ae0a6c15a--PF.npz /home/ubuntu/rca/T-034/e2/runs/e2-determinism-001/3ae-PF--threads-unset.json /home/ubuntu/rca/T-025/src/baro > /home/ubuntu/rca/T-034/e2/runs/e2-determinism-001/3ae-PF--threads-unset.out 2> /home/ubuntu/rca/T-034/e2/runs/e2-determinism-001/3ae-PF--threads-unset.err ) &
wait
echo "exit=0 $(date -u +%FT%TZ)" > /home/ubuntu/rca/T-034/e2/runs/e2-determinism-001/done.txt
