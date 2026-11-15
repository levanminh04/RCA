. "$PSScriptRoot/c1.ps1"

function Start-Tai {
 param([ValidateRange(1,3600)][int]$Seconds=300,[ValidateRange(1,100)][int]$Rate=5,
       [Parameter(Mandatory)][ValidatePattern('^[a-z0-9][a-z0-9-]{0,47}$')][string]$Tag,
       [ValidateSet('tai','obs')][string]$May='tai')
 Assert-C1Running
 if(!(Test-Path "$script:C1Repo/results/T-062/ha-tang/A2-XONG")){throw 'A2-XONG missing: load prohibited'}
 $config=Get-Content -Raw -Encoding UTF8 "$script:C1Root/k6/cau-hinh.json" | ConvertFrom-Json
 if($May -eq 'obs'){
  # Brief v3: caller selects obs only for an AWS failure and records the reason.
  foreach($file in @('workload-t062.js','cau-hinh.json','fixtures.json')){
   Send-C1File -May obs -Source "$script:C1Root/k6/$file" -Destination "/opt/rca-tai/k6/$file"
  }
 }
 # Check run uniqueness and single load process before issuing a fresh login.
 Invoke-C1 -May $May -Command "set -eu; test ! -e /opt/rca-tai/out/$Tag; test -z `"`$(sudo -n docker ps -q --filter name=rca-tai-)`""
 Initialize-C1Token -May $May
 $command=@'
set -euo pipefail
cd /opt/rca-tai
test ! -e out/__TAG__
mkdir out/__TAG__
cp k6/workload-t062.js k6/cau-hinh.json k6/fixtures.json out/__TAG__/
date -u --iso-8601=seconds > out/__TAG__/start-utc.txt
printf '{"machine":"__MAY__","seconds":__SECONDS__,"rate":__RATE__,"image":"__IMAGE__"}\n' > out/__TAG__/run.json
sha256sum out/__TAG__/workload-t062.js out/__TAG__/cau-hinh.json out/__TAG__/fixtures.json > out/__TAG__/inputs.sha256
sudo -n docker run -d --name rca-tai-__TAG__ --user "$(id -u):$(id -g)" --network host \
  -v /opt/rca-tai/out/__TAG__:/scripts:ro -v /opt/rca-tai/secret:/secret:ro -v /opt/rca-tai/out/__TAG__:/out \
  -e FT_TEST_ENVIRONMENT=true -e FT_MACHINE=__MAY__ -e FT_LOAD_SECONDS=__SECONDS__ -e FT_LOAD_RATE=__RATE__ \
  __IMAGE__ run --quiet --out json=/out/raw.json --summary-export /out/summary.json /scripts/workload-t062.js
'@
 $command=$command.Replace('__TAG__',$Tag).Replace('__MAY__',$May).Replace('__SECONDS__',[string]$Seconds).Replace('__RATE__',[string]$Rate).Replace('__IMAGE__',$config.image)
 Invoke-C1 -May $May -Mutation -Command $command
}
function Stop-Tai {
 param([ValidatePattern('^[a-z0-9][a-z0-9-]{0,47}$')][string]$Tag,[ValidateSet('tai','obs')][string]$May='tai')
 # Emergency stop must work even when local STOP exists. No container or output deletion.
 if($Tag){$selector="name=^rca-tai-$Tag`$"}else{$selector='name=^rca-tai-'}
 Invoke-C1 -May $May -IgnoreStop -Mutation -Command "set -eu; ids=`$(sudo -n docker ps -q --filter '$selector'); if [ -n `"`$ids`" ]; then sudo -n docker stop --time 45 `$ids; fi"
}
function Get-Tai {
 param([Parameter(Mandatory)][ValidatePattern('^[a-z0-9][a-z0-9-]{0,47}$')][string]$Tag,[ValidateSet('tai','obs')][string]$May='tai')
 Invoke-C1 -May $May -Command "sudo -n docker inspect rca-tai-$Tag --format '{{json .State}}'"
}
function Receive-Tai {
 param([Parameter(Mandatory)][ValidatePattern('^[a-z0-9][a-z0-9-]{0,47}$')][string]$Tag,[ValidateSet('tai','obs')][string]$May='tai')
 Assert-C1Running
 $target=Get-C1Target $May
 Invoke-C1 -May $May -Command "test `"`$(sudo -n docker inspect rca-tai-$Tag --format '{{.State.Running}}')`" = false"
 Invoke-C1 -May $May -Mutation -Command "sudo -n docker logs rca-tai-$Tag > /opt/rca-tai/out/$Tag/container.log 2>&1; sudo -n docker inspect rca-tai-$Tag --format '{{json .State}}' > /opt/rca-tai/out/$Tag/state.json; date -u --iso-8601=seconds > /opt/rca-tai/out/$Tag/received-utc.txt; cd /opt/rca-tai/out/$Tag; sha256sum *.json *.js *.log *.txt inputs.sha256 > outputs.sha256"
 $destination="$script:C1Root/out/$Tag"
 New-Item -ItemType Directory -Force $destination | Out-Null
 & 'C:/Program Files/Git/usr/bin/scp.exe' -r -i $target.Key -o BatchMode=yes -o StrictHostKeyChecking=yes "-oUserKnownHostsFile=$($target.Known)" "ubuntu@$($target.HostName):/opt/rca-tai/out/$Tag/." $destination
 if($LASTEXITCODE -ne 0){throw 'Receive failed'}
 Get-ChildItem -LiteralPath $destination
}
