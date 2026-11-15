. "$PSScriptRoot/remote.ps1"
Invoke-Oracle app 'set -e; sudo install -o ubuntu -g ubuntu -m 600 /var/lib/flash-ticket-ledger/ledger.jsonl /home/ubuntu/t058/ledger-export.jsonl'
Receive-Oracle app '/home/ubuntu/t058/ledger-export.jsonl' "$PSScriptRoot/ledger-received.jsonl"
py -3 -B -X utf8 "$PSScriptRoot/append-ledger.py" "$PSScriptRoot/ledger-received.jsonl" "$PSScriptRoot/so-tiem-loi.jsonl"
if($LASTEXITCODE -ne 0){throw 'Local ledger validation failed'}
Copy-Oracle obs "$PSScriptRoot/append-ledger.py" '/home/ubuntu/t058/append-ledger.py'
Copy-Oracle obs "$PSScriptRoot/ledger-received.jsonl" '/home/ubuntu/t058/ledger-received.jsonl'
Invoke-Oracle obs @'
set -e
chmod 600 /home/ubuntu/t058/ledger-received.jsonl
sudo python3 /home/ubuntu/t058/append-ledger.py /home/ubuntu/t058/ledger-received.jsonl /var/lib/flash-ticket-ledger/ledger.jsonl
sudo chown ledger:ledger /var/lib/flash-ticket-ledger/ledger.jsonl
sudo chmod 600 /var/lib/flash-ticket-ledger/ledger.jsonl
sudo -u rca test ! -r /var/lib/flash-ticket-ledger/ledger.jsonl
'@
