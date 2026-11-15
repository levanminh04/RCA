param([Parameter(Mandatory=$true)][ValidatePattern('^[a-zA-Z0-9]+$')][string]$Id)
. "$PSScriptRoot/remote.ps1"
Invoke-Oracle obs "set -e; sudo python3 /home/ubuntu/t058/safe-export.py case $Id"
Receive-Oracle obs "/home/ubuntu/t058/export-audit-$Id.json" "$PSScriptRoot/export-audit-$Id.json"
$remoteHash=Invoke-Oracle obs "set -e; sudo test -f /opt/flash-ticket-rca/outputs/$Id/summary.json; sudo tar -czf /home/ubuntu/t058/case-$Id.tgz -C /opt/flash-ticket-rca cases/$Id outputs/$Id; sudo chmod 644 /home/ubuntu/t058/case-$Id.tgz; sha256sum /home/ubuntu/t058/case-$Id.tgz"
$destination="$PSScriptRoot/rca-ban-dau"
$null=New-Item -ItemType Directory -Force -Path $destination
Receive-Oracle obs "/home/ubuntu/t058/case-$Id.tgz" "$destination/$Id.tgz"
$localHash=(Get-FileHash -Algorithm SHA256 -LiteralPath "$destination/$Id.tgz").Hash.ToLowerInvariant()
if(([string]$remoteHash).Split(' ')[0] -ne $localHash){throw 'Archive hash mismatch; extraction refused'}
& 'C:/Windows/System32/tar.exe' -xf "$destination/$Id.tgz" -C $destination
if($LASTEXITCODE -ne 0){throw 'Case extraction failed'}
Get-FileHash -Algorithm SHA256 -LiteralPath "$destination/$Id.tgz"
