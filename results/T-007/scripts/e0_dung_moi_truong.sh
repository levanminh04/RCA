#!/usr/bin/env bash
# T-007 E0: dựng môi trường trên EC2 (Ubuntu 24.04, Python 3.12.3 hệ thống).
# Mọi thứ nằm trong ~/rca, trừ gói hệ thống cài bằng apt (SPEC T-007, Phạm vi ghi).
# Cache của pip, uv, matplotlib và thư mục tạm cũng đặt trong ~/rca để không ghi ra ngoài.
# Chạy: mkdir -p ~/rca/runs/e0 && nohup bash ~/rca/scripts/e0_dung_moi_truong.sh > ~/rca/runs/e0/e0.log 2>&1 &
set -euo pipefail

R=$HOME/rca
export XDG_CACHE_HOME=$R/cache PIP_CACHE_DIR=$R/cache/pip UV_CACHE_DIR=$R/cache/uv \
       MPLCONFIGDIR=$R/cache/mpl TMPDIR=$R/tmp PIP_DISABLE_PIP_VERSION_CHECK=1
mkdir -p $R/src $R/envs $R/cache $R/tmp $R/runs/e0
ts() { date -u +%FT%TZ; }
buoc() { echo; echo "=== $(ts) $* ==="; }

REV_RCAEVAL=259ea4167160256a74ad30004aa3d96a998c846e
REV_BARO=e35f4ec1095e5cac891d52de9ad18a5b32a37ec8
NGAY_GHIM=2024-12-22   # như SPEC T-006: chỉ lấy bản phát hành trước ngày nộp bài RCAEval

buoc "1. Gói hệ thống (README RCAEval + python3.12-venv)"
sudo DEBIAN_FRONTEND=noninteractive apt-get update -y
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
  build-essential libxml2 libxml2-dev zlib1g-dev python3-tk graphviz python3.12-venv
dpkg -l build-essential libxml2 libxml2-dev zlib1g-dev python3-tk graphviz python3.12-venv | tail -n +6

buoc "2. Clone code, đúng revision"
[ -d $R/src/RCAEval ] || git clone https://github.com/phamquiluan/RCAEval $R/src/RCAEval
git -C $R/src/RCAEval checkout -q $REV_RCAEVAL
[ -d $R/src/baro ] || git clone https://github.com/phamquiluan/baro $R/src/baro
git -C $R/src/baro checkout -q $REV_BARO
echo "RCAEval HEAD: $(git -C $R/src/RCAEval rev-parse HEAD)"
echo "baro    HEAD: $(git -C $R/src/baro rev-parse HEAD)"
[ "$(git -C $R/src/RCAEval rev-parse HEAD)" = $REV_RCAEVAL ]
[ "$(git -C $R/src/baro rev-parse HEAD)" = $REV_BARO ]
git -C $R/src/RCAEval status --short | head; git -C $R/src/baro status --short | head

buoc "3. uv trong môi trường riêng envs/tools"
[ -x $R/envs/tools/bin/uv ] || { python3 -m venv $R/envs/tools && $R/envs/tools/bin/pip install --no-cache-dir uv; }
UV=$R/envs/tools/bin/uv
$UV --version

buoc "4. py312: bản mới nhất, như T-005 trên laptop (pip install -e .[default], thêm pyarrow psutil)"
if [ ! -x $R/envs/py312/bin/python ]; then
  python3 -m venv $R/envs/py312
  $R/envs/py312/bin/python -m pip install --no-cache-dir --upgrade pip
fi
( cd $R/src/RCAEval && $R/envs/py312/bin/python -m pip install --no-cache-dir -e ".[default]" )
$R/envs/py312/bin/python -m pip install --no-cache-dir pyarrow psutil
echo "--- pip check py312"; $R/envs/py312/bin/python -m pip check || echo "PIP_CHECK_LOI py312"

buoc "5. py312-pin: uv --exclude-newer $NGAY_GHIM (TZ máy: $(date +%Z))"
if [ ! -x $R/envs/py312-pin/bin/python ]; then
  python3 -m venv $R/envs/py312-pin
fi
$UV pip install --no-cache --python $R/envs/py312-pin/bin/python --exclude-newer $NGAY_GHIM \
  -e "$R/src/RCAEval[default]" pyarrow psutil
echo "--- pip check py312-pin"; $R/envs/py312-pin/bin/python -m pip check || echo "PIP_CHECK_LOI py312-pin"

buoc "6. Import thử và phiên bản thư viện chính"
for E in py312 py312-pin; do
  echo "--- $E"
  ( cd $R/src/baro && $R/envs/$E/bin/python - <<'PY'
import sys, importlib
sys.path.insert(0, ".")  # baro lấy từ repo, không cài fse-baro (như T-005)
from RCAEval.e2e.microrank import microrank
from RCAEval.e2e.tracerca import tracerca
from baro.anomaly_detection import bocpd
import baro.reproducibility
import RCAEval
print("RCAEval tu:", RCAEval.__file__)
print("python", sys.version.split()[0])
for m in ["numpy", "pandas", "scipy", "sklearn", "pyarrow", "tqdm", "matplotlib", "torch", "causallearn", "networkx"]:
    try:
        print(m, importlib.import_module(m).__version__)
    except Exception as e:
        print(m, "LOI", type(e).__name__, e)
PY
  )
  $R/envs/$E/bin/python -m pip freeze --exclude-editable > $R/runs/e0/freeze-$E.txt
  echo "freeze: $(wc -l < $R/runs/e0/freeze-$E.txt) gói"
done

buoc "7. Dung lượng"
du -sh $R/envs/* $R/src $R/cache 2>/dev/null || true
df -h /
echo "$(ts) E0_XONG"
