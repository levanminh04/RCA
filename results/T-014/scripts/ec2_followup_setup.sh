#!/usr/bin/env bash
set -euo pipefail
BASE=/home/ubuntu/rca/T-014
export XDG_CACHE_HOME="$BASE/cache" UV_CACHE_DIR="$BASE/cache/uv" PIP_CACHE_DIR="$BASE/cache/pip" TMPDIR="$BASE/tmp" PYTHONDONTWRITEBYTECODE=1
mkdir -p "$BASE/cache" "$BASE/tmp" "$BASE/python" "$BASE/runs/setup-ec2-2" "$BASE/src"
date -u
if [ ! -d "$BASE/python/cpython-3.12.3-linux-x86_64-gnu" ]; then cp -a /home/ubuntu/rca/T-015/python/cpython-3.12.3-linux-x86_64-gnu "$BASE/python/"; fi
cp /home/ubuntu/rca/T-015/bin/uv "$BASE/uv"
if [ ! -d "$BASE/env" ]; then "$BASE/uv" venv --python "$BASE/python/cpython-3.12.3-linux-x86_64-gnu/bin/python3.12" "$BASE/env"; fi
"$BASE/python/cpython-3.12.3-linux-x86_64-gnu/bin/python3.12" "$BASE/scripts/ec2_download_wheels.py"
"$BASE/uv" pip install --python "$BASE/env/bin/python" --no-deps --no-index --find-links "$BASE/wheels" -r "$BASE/requirements-followup.txt"
"$BASE/uv" pip check --python "$BASE/env/bin/python"
tar -xf "$BASE/rcaeval-source.tar" -C "$BASE/src"
sha256sum "$BASE/rcaeval-source.tar" "$BASE/data/re2tt_ts-order-service_loss_3/metrics.parquet"
"$BASE/env/bin/python" "$BASE/scripts/ec2_followup.py" --mode preflight
date -u
