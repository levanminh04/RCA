$ErrorActionPreference='Stop'
. "$PSScriptRoot/../trien-khai-linux.ps1"
$refs=@(Get-Content -Encoding UTF8 "$script:LinuxRoot/linux/ps-reference.jsonl"|ForEach-Object {$_|ConvertFrom-Json})
if($refs.Count -ne 2){throw 'Both PowerShell references must finish first'}
$command=@'
set -euo pipefail
cd ~/rca-dieu-phoi
python3 tai_linux.py receive --tag l1ps20261113a > linux-check/ps-a-receive.json
python3 tai_linux.py receive --tag l1ps20261113b > linux-check/ps-b-receive.json
python3 doi-chieu-linux.py > linux-check/comparison.stdout.json
python3 tai_linux.py test-duong > linux-check/preflight-final.json
python3 kiem-hop-dong.py > linux-check/contract-final.json
python3 - <<'PY'
import ast,json,pathlib,tai_linux as ctl
tags=['l1linux20261113a','l1linux20261113b','l1ps20261113a','l1ps20261113b']
code='''import json,subprocess
tags=__TAGS__
names={'FT_TEST_ENVIRONMENT','FT_LOAD_SECONDS','FT_JOURNEY_RATE','FT_LOAD_MULTIPLIER','FT_LOAD_STEP_SECONDS','FT_MOCK_TRANSPORT_URL'}
result={}
for tag in tags:
 v=json.loads(subprocess.check_output(['sudo','-n','docker','inspect','rca-tai-'+tag]))[0]
 result[tag]={'image':v['Config']['Image'],'imageId':v['Image'],'cmd':v['Config']['Cmd'],
  'network':v['HostConfig']['NetworkMode'],'user':v['Config']['User'],
  'env':sorted(e for e in v['Config']['Env'] if e.split('=',1)[0] in names),
  'mounts':[{'destination':m['Destination'],'rw':m['RW'],'source':m['Source'].replace(tag,'<tag>')} for m in v['Mounts']]}
print(json.dumps(result))
'''.replace('__TAGS__',repr(tags))
data=ctl.remote_python('tai',code)
for left,right in [(tags[0],tags[2]),(tags[1],tags[3])]:
 assert data[left]==data[right],(left,right)
pathlib.Path('linux-check/docker-launches.json').write_text(json.dumps({'utc':ctl.utc(),'pairsExactlyEqual':True,'containers':data},indent=2)+'\n')
print(json.dumps({'ok':True,'pairsExactlyEqual':True,'sourceVerified':bool(ctl.verify_sources()['files'])}))
PY
'@
Invoke-LinuxObs -Command $command
$target=Get-C1Target obs
$scp='C:/Program Files/Git/usr/bin/scp.exe'
$opts=@('-i',$target.Key,'-o','BatchMode=yes','-o','ConnectTimeout=15','-o','StrictHostKeyChecking=yes',"-oUserKnownHostsFile=$($target.Known)")
& $scp -r @opts "ubuntu@$($target.HostName):/home/ubuntu/rca-dieu-phoi/linux-check/." "$script:LinuxRoot/linux/check"
if($LASTEXITCODE -ne 0){throw 'Metadata receive failed; retain partial files'}
foreach($name in @('tai_linux-v2.py','linux-source-v2-manifest.json','tai-linux-events.jsonl','linux-check-launch.log','linux-check.pid')){
 & $scp @opts "ubuntu@$($target.HostName):/home/ubuntu/rca-dieu-phoi/$name" "$script:LinuxRoot/linux/$name"
 if($LASTEXITCODE -ne 0){throw "Receive failed: $name"}
}
foreach($tag in @('l1linux20261113a','l1linux20261113b','l1ps20261113a','l1ps20261113b')){
 foreach($name in @('buoc-tai.json','buoc-tai-30s.csv')){
  & $scp @opts "ubuntu@$($target.HostName):/home/ubuntu/rca-dieu-phoi/tai-out/$tag/$name" "$script:LinuxRoot/out/$tag/$name"
  if($LASTEXITCODE -ne 0){throw "Receive failed: $tag/$name"}
 }
}
& $scp @opts "ubuntu@$($target.HostName):/home/ubuntu/rca-dieu-phoi/tai_linux.py" "$script:LinuxRoot/linux/deployed-tai_linux.py"
if($LASTEXITCODE -ne 0){throw 'Source receive failed'}
if((Get-FileHash "$script:LinuxRoot/tai_linux.py").Hash -ne (Get-FileHash "$script:LinuxRoot/linux/deployed-tai_linux.py").Hash){throw 'Deployed source mismatch'}
'All comparisons, raw hashes and deployed source verified'
