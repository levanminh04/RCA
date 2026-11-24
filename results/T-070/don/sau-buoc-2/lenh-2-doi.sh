sudo -n bash -s <<'ROOT'
set -euo pipefail; set -x
shopt -s dotglob nullglob
N=/srv/flashticket-rca; O=/srv/rca-lab; A=$N/archive/2026-11
H=b0f79a4dffd552f6e6026172b9058cd54ee9272475d927e35f19e22b04411b8d
test ! -e $N; test ! -e /etc/flashticket-rca; test ! -e /opt/flashticket-rca
test ! -e $O/runs/STOP; test ! -e $O/load-controller/STOP
install -d -o root -g root -m 755 $N
install -d -o ubuntu -g ubuntu -m 700 $N/runs $N/load $N/alerts $N/alerts/bo-nhan
install -d -o root -g root -m 755 $N/archive $A $A/home
install -d -o ubuntu -g ubuntu -m 700 $A/runs
install -d -o root -g rca -m 750 $A/m1
mv $O/m1 $N/rca
chmod 755 $N/rca
install -d -o root -g root -m 755 $N/rca/method
install -d -o ubuntu -g ubuntu -m 775 $N/rca/results
mv $O/m1-snapshots/$H $N/rca/method/
rmdir $O/m1-snapshots
mv $N/rca/t073-dev $N/rca/online-dev
mv $N/rca/t069-phan-tich $A/m1/
mv $O/rca-results/t065-l11-001 $N/rca/results/dev
mv $O/rca-results $A/rca-results
mv $O/ledger $N/ledger
for x in $O/runs/*; do mv "$x" $A/runs/; done
rmdir $O/runs
mv $O/load-controller/tai-linux-events.jsonl $O/load-controller/tai-linux.lock $N/load/
mv $O/load-controller/tai-out $A/load-tai-out
rmdir $O/load-controller
mv $O/collector-gateway $N/collector
mv $O/trace-goi $A/trace-goi
mv $O/rca-results-chep-2026-11-17.sha256 $A/
mv $O/venv-m1 $A/venv-m1
mv /home/ubuntu/t063 $A/home/t063
rmdir $O
mv /etc/rca-lab /etc/flashticket-rca
mv /opt/rca-lab /opt/flashticket-rca
cp -p $A/runs/t072-e3-01-cfg/webhook.env $N/alerts/receiver.env
sed -i 's#^T072_RA_DIR=.*#T072_RA_DIR=/srv/flashticket-rca/alerts/bo-nhan#' $N/alerts/receiver.env
set +x
echo "== ket qua"; ls -la $N $N/rca $A; stat -c '%U:%G %a %n' $N/rca $N/rca/cases $N/rca/outputs $N/rca/method $N/rca/method/$H $N/rca/results $N/rca/results/dev $N/ledger $N/runs $N/load $N/alerts $N/alerts/bo-nhan $N/alerts/receiver.env $N/collector $A/runs $A/m1 /etc/flashticket-rca /opt/flashticket-rca
grep -c . $N/alerts/receiver.env; grep '^T072_RA_DIR' $N/alerts/receiver.env
ROOT
