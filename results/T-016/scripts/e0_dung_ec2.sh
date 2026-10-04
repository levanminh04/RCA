#!/bin/bash
# T-016 S11: dựng môi trường Python 3.8 riêng trên EC2, chỉ ghi trong ~/rca/T-016/.
# ~/rca/envs, ~/rca/src, ~/rca/data chỉ đọc. uv lấy từ ~/rca/envs/tools (chỉ chạy, không ghi vào đó).
set -euo pipefail
B=~/rca/T-016
mkdir -p $B/{envs,src,data,runs,cache,tmp,python,repo}
export XDG_CACHE_HOME=$B/cache PIP_CACHE_DIR=$B/cache/pip UV_CACHE_DIR=$B/cache/uv MPLCONFIGDIR=$B/cache/mpl TMPDIR=$B/tmp
export UV_PYTHON_INSTALL_DIR=$B/python
# REVIEW T-016 R6: không có dòng dưới, `uv python install` tạo ~/.local/bin/python3.8 (ngoài phạm vi). Đặt thư mục liên kết thực thi trong T-016.
export UV_PYTHON_BIN_DIR=$B/python/bin
UV=~/rca/envs/tools/bin/uv
echo "$(date -u +%FT%TZ) clone RCAEval tu ban doc ~/rca/src/RCAEval"
if [ ! -d $B/src/RCAEval ]; then git clone -q ~/rca/src/RCAEval $B/src/RCAEval; fi
cd $B/src/RCAEval && git checkout -q 259ea4167160256a74ad30004aa3d96a998c846e
test "$(git rev-parse HEAD)" = "259ea4167160256a74ad30004aa3d96a998c846e" || { echo "SAI REVISION"; exit 1; }
echo "$(date -u +%FT%TZ) cai Python 3.8 (uv, python-build-standalone)"
$UV python install 3.8 --no-cache
$UV venv --no-cache --python 3.8 $B/envs/py38
P=$B/envs/py38/bin/python
echo "$(date -u +%FT%TZ) cai goi theo lock (bo tigramite, torch)"
$UV pip install --no-cache --python $P -r $B/repo/results/T-016/requirements_py38_ec2.lock
$UV pip install --no-cache --python $P --no-deps -e $B/src/RCAEval
echo "$(date -u +%FT%TZ) chep 5 file va (nhu results/T-006/moi-truong.md muc 3)"
SP=$($P -c "import site;print(site.getsitepackages()[0])")
for f in pyAgrum/lib/image.py causallearn/search/ConstraintBased/FCI.py causallearn/utils/Fas.py causallearn/utils/PCUtils/SkeletonDiscovery.py causallearn/graph/GraphClass.py; do
  cp $SP/$f $SP/$f.orig
  cp $B/src/RCAEval/lib/$f $SP/$f
  sha256sum $B/src/RCAEval/lib/$f $SP/$f
done
$UV pip check --python $P || true
$UV pip freeze --python $P > $B/runs/freeze-py38-ec2.txt
$P -V
echo "$(date -u +%FT%TZ) XONG"
