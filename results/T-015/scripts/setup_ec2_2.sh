#!/usr/bin/env bash
set -eu
TASK_ROOT="$HOME/rca/T-015"
export UV_PYTHON_INSTALL_DIR="$TASK_ROOT/python" UV_PYTHON_BIN_DIR="$TASK_ROOT/bin" UV_CACHE_DIR="$TASK_ROOT/cache" XDG_CACHE_HOME="$TASK_ROOT/cache" TMPDIR="$TASK_ROOT/tmp" PYTHONDONTWRITEBYTECODE=1
UV="$TASK_ROOT/bin/uv"
date -u
"$UV" python install 3.12.3 --no-bin
"$UV" venv --no-project --managed-python --python 3.12.3 "$TASK_ROOT/env"
"$UV" pip install --python "$TASK_ROOT/env/bin/python" numpy==1.26.4 pandas==2.2.3 pyarrow==18.1.0 python-dateutil==2.8.2 pytz==2023.3 six==1.16.0 tzdata==2023.3
"$UV" pip check --python "$TASK_ROOT/env/bin/python"
"$UV" pip freeze --python "$TASK_ROOT/env/bin/python" > "$TASK_ROOT/runs/setup/freeze.txt"
"$TASK_ROOT/env/bin/python" -B -c 'import sys,numpy,pandas,pyarrow; print(sys.version); print(numpy.__version__,pandas.__version__,pyarrow.__version__)'
find "$TASK_ROOT/python" "$TASK_ROOT/cache" -type f -name '*.whl' -o -name '*.tar.gz' | sort > "$TASK_ROOT/runs/setup/download-artifacts.txt"
date -u
