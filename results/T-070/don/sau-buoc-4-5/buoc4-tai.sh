sudo -n bash -s <<'ROOT'
set -euo pipefail; set -x
N=/srv/flashticket-rca; A=$N/archive/2026-11
test ! -e $N; test ! -e /etc/flashticket-rca; test ! -e /opt/flashticket-rca
install -d -o root -g root -m 755 $N $N/archive $A $A/home
install -d -o ubuntu -g ubuntu -m 755 $N/runs
mv /srv/rca-lab/load-runs $A/load-runs
rmdir /srv/rca-lab
mv /etc/rca-lab /etc/flashticket-rca
mv /opt/rca-lab /opt/flashticket-rca
for x in x86-check uvenv arm-check.tgz arm-check2.tgz rec-x86linux.json dump_rec.py; do mv /home/ubuntu/$x $A/home/; done
set +x
stat -c '%U:%G %a %n' $N $N/runs $A $A/load-runs /etc/flashticket-rca /etc/flashticket-rca/load-secret /opt/flashticket-rca
ls $A/load-runs | wc -l; ls $A/home
ROOT
cd /opt/flashticket-rca && git fetch -q origin && git checkout -q --detach 85ace52d304712303097ca0f99faa16f0b52805c && git rev-parse HEAD && git status --short | head -3
ls -d /srv/rca-lab /etc/rca-lab /opt/rca-lab 2>&1 | head -3
