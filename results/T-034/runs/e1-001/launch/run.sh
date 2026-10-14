#!/usr/bin/env bash
# T-034 E1 (thiet-ke-hai-phep-kiem.md, E1). Chi doc nguon T-032; chi ghi duoi /home/ubuntu/rca/T-034/e1.
set -u
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8 PYTHONHASHSEED=0 TMPDIR=/home/ubuntu/rca/T-034/e1/tmp XDG_CACHE_HOME=/home/ubuntu/rca/T-034/e1/cache MPLCONFIGDIR=/home/ubuntu/rca/T-034/e1/cache/mpl
export PYTHONPATH="/home/ubuntu/rca/T-034/e1/scripts:/home/ubuntu/rca/T-032/scripts:/home/ubuntu/rca/T-032/repo/src:/home/ubuntu/rca/T-025/src/RCAEval"
cd "/home/ubuntu/rca/T-034/e1"
nice -n 10 /home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8 scripts/e1_pattern_rule.py runs/e1-001 inputs/closure-ledger-review-001.json > "/home/ubuntu/rca/T-034/e1/runs/e1-001-launch/out.txt" 2> "/home/ubuntu/rca/T-034/e1/runs/e1-001-launch/err.txt"
echo "exit=$? $(date -u +%FT%TZ)" > "/home/ubuntu/rca/T-034/e1/runs/e1-001-launch/done.txt"
