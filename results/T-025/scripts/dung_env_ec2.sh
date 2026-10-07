#!/bin/bash
# T-025 bước 0 (SPEC, sửa C1): dựng env riêng trên EC2, chỉ ghi trong ~/rca/T-025/.
# Python 3.12.3 do uv cài vào ~/rca/T-025/python; gói như T-031 main + matplotlib/requests/tqdm như laptop.
# uv lấy của T-031 (chỉ chạy). Mọi cache trong ~/rca/T-025/cache.
set -euo pipefail
B=~/rca/T-025
mkdir -p $B/cache $B/tmp $B/python $B/envs $B/runs
export XDG_CACHE_HOME=$B/cache UV_CACHE_DIR=$B/cache/uv PIP_CACHE_DIR=$B/cache/pip TMPDIR=$B/tmp
export MPLCONFIGDIR=$B/cache/mpl MPLBACKEND=Agg
export UV_PYTHON_INSTALL_DIR=$B/python UV_PYTHON_BIN_DIR=$B/python/bin
UV=${UV:-~/rca/T-031/envs/tools/bin/uv}  # máy hai: UV=~/rca/T-025/tools/uv (chép từ máy một)
echo "$(date -u +%FT%TZ) cài Python 3.12.3"
$UV python install 3.12.3
PY=$(ls -d $B/python/cpython-3.12.3-linux-x86_64-gnu)/bin/python3
$PY -V
echo "$(date -u +%FT%TZ) env main"
$UV venv --python $PY $B/envs/main
$UV pip install --python $B/envs/main/bin/python numpy==1.26.4 pandas==2.2.3 pyarrow==18.1.0 scipy==1.14.1 \
  psutil==6.1.1 python-dateutil==2.8.2 pytz==2023.3 tzdata==2023.3 matplotlib==3.10.0 requests==2.30.0 tqdm==4.65.0
$UV pip check --python $B/envs/main/bin/python || true
$UV pip freeze --python $B/envs/main/bin/python > $B/runs/freeze-main.txt
echo "$(date -u +%FT%TZ) thử import BARO"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$B/src/baro:$B/repo/src $B/envs/main/bin/python -B -c \
  "import baro.utility, baro._bocpd, baro.anomaly_detection, p3.adapters.phat_hien, numpy, scipy; print('import OK', numpy.__version__, scipy.__version__)"
echo "$(date -u +%FT%TZ) XONG"
