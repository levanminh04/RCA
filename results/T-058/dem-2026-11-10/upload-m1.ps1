. "$PSScriptRoot/remote.ps1"
Invoke-Oracle obs 'set -e; test -f /home/ubuntu/t058/resources-30m-obs.done; date -u'
foreach($name in @('stage-m1.py','run-m1.py','m1-p7-config.json','m1-source-pins.json','flashticket-inventory-source.json')) {
    Copy-Oracle obs "$PSScriptRoot/$name" "/home/ubuntu/t058/$name"
}
Copy-Oracle obs "$PSScriptRoot/src/m1/adapter_flashticket.py" '/home/ubuntu/t058/adapter_flashticket.py'
Invoke-Oracle obs @'
set -euo pipefail
sudo install -o root -g rca -m 440 /home/ubuntu/t058/adapter_flashticket.py /opt/flash-ticket-rca/src/m1/adapter_flashticket.py
for name in stage-m1.py run-m1.py m1-p7-config.json m1-source-pins.json flashticket-inventory-source.json; do
  sudo install -o root -g rca -m 440 /home/ubuntu/t058/$name /opt/flash-ticket-rca/$name
done
sudo find /opt/flash-ticket-rca/src -name '*.pyc' -type f -delete
sudo chown -R root:rca /opt/flash-ticket-rca/src
sudo chmod -R a-w /opt/flash-ticket-rca/src
sudo mkdir -p /opt/flash-ticket-rca/outputs
sudo chown rca:rca /opt/flash-ticket-rca/outputs
sudo -u rca test ! -r /var/lib/flash-ticket-ledger/ledger.jsonl
sudo -u rca /opt/flash-ticket-rca/venv/bin/python -B -c 'import sys; sys.path.insert(0,"/opt/flash-ticket-rca/src"); from m1.adapter_flashticket import adapt; print("Adapter import OK")'
sudo -u rca /opt/flash-ticket-rca/venv/bin/pip check
sudo -u rca /opt/flash-ticket-rca/venv/bin/pip list --format=json > /home/ubuntu/t058/python-packages.json
date -u
'@
Receive-Oracle obs '/home/ubuntu/t058/python-packages.json' "$PSScriptRoot/python-packages.json"
