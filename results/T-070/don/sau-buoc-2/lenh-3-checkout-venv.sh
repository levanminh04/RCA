set -euo pipefail
cd /opt/flashticket-rca && git fetch -q origin && git checkout -q --detach 85ace52d304712303097ca0f99faa16f0b52805c && git rev-parse HEAD && git status --short | head -5
sudo -n bash -s <<'ROOT'
set -euo pipefail
V=/srv/flashticket-rca/rca/venv
test ! -e $V
/usr/bin/python3 -m venv $V
$V/bin/pip install -q --no-deps --no-cache-dir -r /opt/flashticket-rca/rca/requirements-m1.txt
$V/bin/python --version
$V/bin/python -m pip freeze --all
cat $V/pyvenv.cfg
ROOT
