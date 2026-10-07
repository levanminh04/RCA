#!/bin/bash
# T-031: dựng môi trường trên EC2, chỉ ghi trong ~/rca/T-031/ (theo cách T-016 e0_dung_ec2.sh).
set -euo pipefail
B=~/rca/T-031
export XDG_CACHE_HOME=$B/cache PIP_CACHE_DIR=$B/cache/pip UV_CACHE_DIR=$B/cache/uv TMPDIR=$B/tmp
export UV_PYTHON_INSTALL_DIR=$B/python UV_PYTHON_BIN_DIR=$B/python/bin
UV=$B/envs/tools/bin/uv
echo "$(date -u +%FT%TZ) env main (3.12, dùng cho vai main và drain)"
$UV venv --python ~/rca/T-014/python/cpython-3.12.3-linux-x86_64-gnu/bin/python3 $B/envs/main
$UV pip install --python $B/envs/main/bin/python numpy==1.26.4 pandas==2.2.3 pyarrow==18.1.0 scipy==1.14.1 scikit-learn==1.6.0 joblib==1.2.0 threadpoolctl==3.1.0 psutil==6.1.1 python-dateutil==2.8.2 pytz==2023.3 tzdata==2023.3 drain3==0.9.11 cachetools==4.2.1 jsonpickle==1.5.1
echo "$(date -u +%FT%TZ) Python 3.8 + lock T-016"
$UV python install 3.8
$UV venv --python 3.8 $B/envs/py38
P=$B/envs/py38/bin/python
$UV pip install --python $P -r $B/repo/results/T-016/requirements_py38_ec2.lock
$UV pip install --python $P --no-deps -e $B/src/RCAEval
SP=$($P -c "import site;print(site.getsitepackages()[0])")
for f in pyAgrum/lib/image.py causallearn/search/ConstraintBased/FCI.py causallearn/utils/Fas.py causallearn/utils/PCUtils/SkeletonDiscovery.py causallearn/graph/GraphClass.py; do
  cp $SP/$f $SP/$f.orig; cp $B/src/RCAEval/lib/$f $SP/$f; sha256sum $B/src/RCAEval/lib/$f $SP/$f
done
$UV pip check --python $P || true
$UV pip freeze --python $P > $B/runs/freeze-py38.txt
$UV pip freeze --python $B/envs/main/bin/python > $B/runs/freeze-main.txt
$P -V; $B/envs/main/bin/python -V
echo "$(date -u +%FT%TZ) XONG"
