# The old file stays byte-identical. Existing read workload commands remain available.
. "$PSScriptRoot/../tai/chay-tai.ps1"
$script:L1OldStart=${function:Start-Tai}
$script:L1OldReceive=${function:Receive-Tai}
. "$PSScriptRoot/token-pool.ps1"
. "$PSScriptRoot/tunnel.ps1"
function Start-Tai {
 param([ValidateRange(1,3600)][int]$Seconds=300,[ValidateRange(0,100)][int]$Rate=0,
 [Parameter(Mandatory)][ValidatePattern('^[a-z0-9][a-z0-9-]{0,47}$')][string]$Tag,
 [ValidateSet('tai','obs')][string]$May='tai',[ValidateSet('doc','hanh-trinh')][string]$Scenario='doc',
 [ValidateRange(1,3)][int]$Multiplier=1)
 if($Scenario -eq 'doc') {if(!$Rate){$Rate=5}; & $script:L1OldStart -Seconds $Seconds -Rate $Rate -Tag $Tag -May $May; return}
 if($May -ne 'tai'){throw 'L1 journey workload is authorized on AWS only'}
 Assert-C1Running
 $null=Start-L1Tunnel
 Invoke-L1 -May tai -Command "test ! -e /opt/rca-tai/out/$Tag; test -z `"`$(sudo -n docker ps -q --filter name=rca-tai-)`"; curl -fsS --max-time 10 http://127.0.0.1:19090/health"
 $metadata=Initialize-L1Tokens
 $cfg=Get-Content -Raw -Encoding UTF8 "$script:L1Root/k6/cau-hinh.json"|ConvertFrom-Json
 if(!$Rate){$Rate=$cfg.rate}
 $files=@{}
 foreach($name in @('hanh-trinh.js','cau-hinh.json')){$files[$name]=[Convert]::ToBase64String([IO.File]::ReadAllBytes("$script:L1Root/k6/$name"))}
 $prepare=@'
import base64,json,hashlib,pathlib
root=pathlib.Path('/opt/rca-tai/out/__TAG__')
root.mkdir()
files=__FILES__
for name,value in files.items():
    (root/name).write_bytes(base64.b64decode(value))
(root/'token-metadata.json').write_text(json.dumps(__META__))
(root/'inputs.sha256').write_text(''.join(hashlib.sha256((root/n).read_bytes()).hexdigest()+'  '+n+'\n' for n in files))
'@
 $prepare=$prepare.Replace('__TAG__',$Tag).Replace('__FILES__',($files|ConvertTo-Json -Compress)).Replace('__META__',($metadata|ConvertTo-Json -Compress))
 $launch=@'
set -euo pipefail
cd /opt/rca-tai
date -u --iso-8601=seconds > out/__TAG__/start-utc.txt
printf '{"scenario":"hanh-trinh","seconds":__SECONDS__,"rate":__RATE__,"timeUnit":"10s","multiplier":__MULT__}\n' > out/__TAG__/run.json
sudo -n docker run -d --name rca-tai-__TAG__ --user "$(id -u):$(id -g)" --network host \
 -v /opt/rca-tai/out/__TAG__:/scripts:ro -v /opt/rca-tai/secret:/secret:ro -v /opt/rca-tai/out/__TAG__:/out \
 -e FT_TEST_ENVIRONMENT=true -e FT_LOAD_SECONDS=__SECONDS__ -e FT_JOURNEY_RATE=__RATE__ -e FT_LOAD_MULTIPLIER=__MULT__ \
 __IMAGE__ run --quiet --log-format raw --out json=/out/raw.json --out csv=/out/raw.csv --summary-export /out/summary.json /scripts/hanh-trinh.js
'@
 $launch=$launch.Replace('__TAG__',$Tag).Replace('__SECONDS__',[string]$Seconds).Replace('__RATE__',[string]$Rate).Replace('__MULT__',[string]$Multiplier).Replace('__IMAGE__',$cfg.image)
 Invoke-L1 -May tai -Mutation -Command ("python3 - <<'PY'`n"+$prepare+"`nPY`n"+$launch)
}
function Stop-Tai {
 param([ValidatePattern('^[a-z0-9][a-z0-9-]{0,47}$')][string]$Tag,[ValidateSet('tai','obs')][string]$May='tai')
 if($May -ne 'tai'){throw 'exp-obs read only'}
 # Emergency stop may run while STOP exists; source is explicit and has no deletion.
 $target=Get-C1Target tai
 $selector=if($Tag){'name=^rca-tai-'+$Tag+'$'}else{'name=^rca-tai-'}
 $command="ids=`$(sudo -n docker ps -q --filter '$selector'); if [ -n `"`$ids`" ]; then sudo -n docker stop --time 90 `$ids; fi"
 Add-Content -Encoding UTF8 "$script:L1Root/thay-doi-may.md" ("`n"+[DateTime]::UtcNow.ToString('o')+" - tai : $command")
 $encoded=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($command+"`n"))
 $encoded | & $script:C1Ssh -i $target.Key -o BatchMode=yes -o StrictHostKeyChecking=yes "-oUserKnownHostsFile=$($target.Known)" "ubuntu@$($target.HostName)" 'base64 --decode --ignore-garbage | bash'
 if($LASTEXITCODE -ne 0){throw 'Stop failed'}
}
function Receive-Tai {
 param([Parameter(Mandatory)][ValidatePattern('^[a-z0-9][a-z0-9-]{0,47}$')][string]$Tag,
 [ValidateSet('tai','obs')][string]$May='tai',[ValidateSet('doc','hanh-trinh')][string]$Scenario='doc')
 if($Scenario -eq 'doc'){& $script:L1OldReceive -Tag $Tag -May $May;return}
 if($May -ne 'tai'){throw 'L1 journey workload is authorized on AWS only'}
 Invoke-L1 -May tai -Command "test `"`$(sudo -n docker inspect rca-tai-$Tag --format '{{.State.Running}}')`" = false"
 Invoke-L1 -May tai -Mutation -Command "set -eu; sudo -n docker logs rca-tai-$Tag > /opt/rca-tai/out/$Tag/container.log 2>&1; sudo -n docker inspect rca-tai-$Tag --format '{{json .State}}' > /opt/rca-tai/out/$Tag/state.json; date -u --iso-8601=seconds > /opt/rca-tai/out/$Tag/received-utc.txt; cd /opt/rca-tai/out/$Tag; sha256sum *.json *.js *.log *.txt *.csv inputs.sha256 > outputs.sha256"
 $destination="$script:L1Root/out/$Tag"
 New-Item -ItemType Directory -Force $destination|Out-Null
 $target=Get-C1Target tai
 & 'C:/Program Files/Git/usr/bin/scp.exe' -r -i $target.Key -o BatchMode=yes -o StrictHostKeyChecking=yes "-oUserKnownHostsFile=$($target.Known)" "ubuntu@$($target.HostName):/opt/rca-tai/out/$Tag/." $destination
 if($LASTEXITCODE -ne 0){throw 'Receive failed; retain partial output'}
 Get-ChildItem -LiteralPath $destination|Select-Object Name,Length
}
