#!/bin/bash
# T-025 (SPEC sửa đổi môi trường, Minh duyệt 06/10/2026): thêm vào env T-025 các gói cho BARO, CIRCA, TORAI B
# (phiên bản theo laptop T-014-main; drain3 theo T-031), dựng env py38 cho TORAI theo lock T-016 (như T-031
# dung_env.sh). Chỉ ghi trong ~/rca/T-025/. Cần trước: ~/rca/T-025/python (3.12.3), envs/main (dung_env_ec2.sh),
# src/RCAEval (259ea41), src/CIRCA (0215e18), repo/src/{p3,circa_kien_truc,torai}, repo/results/T-016 lock.
set -euo pipefail
B=~/rca/T-025
mkdir -p $B/cache $B/tmp $B/runs
export XDG_CACHE_HOME=$B/cache UV_CACHE_DIR=$B/cache/uv PIP_CACHE_DIR=$B/cache/pip TMPDIR=$B/tmp
export MPLCONFIGDIR=$B/cache/mpl MPLBACKEND=Agg UV_PYTHON_INSTALL_DIR=$B/python UV_PYTHON_BIN_DIR=$B/python/bin
UV=${UV:-~/rca/T-031/envs/tools/bin/uv}
M=$B/envs/main/bin/python
echo "$(date -u +%FT%TZ) main: torch 2.5.1 CPU (không deps) + gói theo laptop"
$UV pip install --python $M --no-deps --index-url https://download.pytorch.org/whl/cpu torch==2.5.1
$UV pip install --python $M numpy==1.26.4 pandas==2.2.3 scipy==1.14.1 scikit-learn==1.6.0 joblib==1.2.0 \
  threadpoolctl==3.1.0 networkx==2.8.8 statsmodels==0.14.4 patsy==1.0.1 causal-learn==0.1.3.8 pingouin==0.5.5 \
  pandas-flavor==0.6.0 tabulate==0.9.0 seaborn==0.12.2 scikit-network==0.33.1 tigramite==5.2.7.0 \
  xarray==2024.10.0 pydot==1.4.2 graphviz==0.20.1 PyYAML==6.0.2 pyparsing==3.0.9 sympy==1.13.1 filelock==3.12.0 \
  fsspec==2023.5.0 Jinja2==3.1.5 MarkupSafe==3.0.2 mpmath==1.3.0 typing_extensions==4.12.2 \
  drain3==0.9.11 cachetools==4.2.1 jsonpickle==1.5.1 matplotlib==3.10.0 requests==2.30.0 tqdm==4.65.0 \
  setuptools==75.6.0  # joblib 1.2.0 import distutils; Python 3.12 lấy distutils từ setuptools (laptop 75.6.0)
$UV pip check --python $M || true
$UV pip freeze --python $M > $B/runs/freeze-main-rca.txt
echo "$(date -u +%FT%TZ) py38 + lock T-016 + RCAEval editable + 5 tệp vá (như T-031)"
$UV python install 3.8.20
[ -x $B/envs/py38/bin/python ] || $UV venv --python 3.8.20 $B/envs/py38  # chạy lại an toàn
P=$B/envs/py38/bin/python
$UV pip install --python $P -r $B/repo/results/T-016/requirements_py38_ec2.lock
$UV pip install --python $P --no-deps -e $B/src/RCAEval
SP=$($P -c "import site;print(site.getsitepackages()[0])")
for f in pyAgrum/lib/image.py causallearn/search/ConstraintBased/FCI.py causallearn/utils/Fas.py causallearn/utils/PCUtils/SkeletonDiscovery.py causallearn/graph/GraphClass.py; do
  [ -f $SP/$f.orig ] || cp $SP/$f $SP/$f.orig; cp $B/src/RCAEval/lib/$f $SP/$f; sha256sum $B/src/RCAEval/lib/$f $SP/$f
done
$UV pip check --python $P || true
$UV pip freeze --python $P > $B/runs/freeze-py38.txt
echo "$(date -u +%FT%TZ) thử import"
cd $B/repo
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$B/src/RCAEval:$B/src/baro:$B/repo/src:$B/src/CIRCA $M -B -W ignore -c \
  "import RCAEval.e2e.baro, RCAEval.io.time_series, RCAEval.classes.data, RCAEval.graph_heads.rht, RCAEval.benchmark.evaluation, p3.adapters.baro, p3.adapters.circa, p3.adapters.torai, p3.adapters.phat_hien, p3.worker, circa_kien_truc, circa.graph.structural, drain3, baro.anomaly_detection; print('main import OK')"
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$B/src/RCAEval:$B/repo/src $P -B -W ignore -c "import torai.torai_sua, p3.adapters.torai, p3.worker; print('py38 import OK')"
echo "$(date -u +%FT%TZ) XONG"
