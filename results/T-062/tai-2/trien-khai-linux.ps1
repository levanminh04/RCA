# Transport only. Does not modify or replace the PowerShell load controller.
. "$PSScriptRoot/../tai/c1.ps1"
$script:LinuxRoot=$PSScriptRoot
function Invoke-LinuxObs {
 param([Parameter(Mandatory)][string]$Command)
 Assert-C1Running
 $target=Get-C1Target obs
 $encoded=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Command.Replace("`r`n","`n")+"`n"))
 $encoded | & $script:C1Ssh -i $target.Key -o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=yes "-oUserKnownHostsFile=$($target.Known)" "ubuntu@$($target.HostName)" 'base64 --decode --ignore-garbage | bash'
 if($LASTEXITCODE -ne 0){throw "exp-obs command failed: $LASTEXITCODE"}
}
function Install-LinuxTai {
 Assert-C1Running
 $old=Get-Content -Raw -Encoding UTF8 "$script:LinuxRoot/bo-sung-1/manifest-bo-sung-1.json"|ConvertFrom-Json
 $auth=Get-Content -Raw -Encoding UTF8 "$script:C1Repo/results/T-058/dem-2026-11-10/artifacts-sha256.json"|ConvertFrom-Json
 $mapping=[ordered]@{'tai_linux.py'='results/T-062/tai-2/tai_linux.py';'k6/hanh-trinh.js'='results/T-062/tai-2/k6/hanh-trinh.js';'k6/cau-hinh.json'='results/T-062/tai-2/k6/cau-hinh.json';'linux-support/auth.py'='results/T-058/dem-2026-11-10/auth.py'}
 foreach($name in @('kiem-mock.py','kiem-token-con-han.py','tunnel-remote.py','analyze.py','gateway-log.py','verify-outputs.py')){$mapping["linux-support/$name"]="results/T-062/tai-2/$name"}
 $files=[ordered]@{};$payload=[ordered]@{}
 foreach($name in $mapping.Keys){
  $path=Join-Path $script:C1Repo $mapping[$name]
  $hash=(Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash.ToLower()
  if($name -eq 'linux-support/auth.py' -and $hash -ne $auth.files.'auth.py'.sha256){throw 'Old PKCE hash mismatch'}
  $relative=$mapping[$name].Replace('results/T-062/tai-2/','')
  if($old.files.$relative -and $old.files.$relative.sha256 -ne $hash){throw "Previous source hash mismatch: $relative"}
  $files[$name]=@{repo=$mapping[$name];sha256=$hash;bytes=(Get-Item -LiteralPath $path).Length}
  $payload[$name]=[Convert]::ToBase64String([IO.File]::ReadAllBytes($path))
 }
 $pin=@{utc=[DateTime]::UtcNow.ToString('o');purpose='Exact repo bytes deployed for exp-obs controller';files=$files}|ConvertTo-Json -Depth 7
 [IO.File]::WriteAllText("$script:LinuxRoot/linux-source-manifest.json",$pin,(New-Object Text.UTF8Encoding($false)))
 $payload['linux-source-manifest.json']=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($pin))
 foreach($name in @('EXP-APP-BAO-TRI-1-BAT-DAU','EXP-APP-BAO-TRI-1-XONG')){$payload[$name]=[Convert]::ToBase64String([IO.File]::ReadAllBytes("$script:LinuxRoot/$name"))}
 $source=@'
import base64,hashlib,json,os,pathlib
root=pathlib.Path.home()/'rca-dieu-phoi'
os.umask(0o077)
root.mkdir(exist_ok=True)
files=__PAYLOAD__
changes=[]
for name,value in files.items():
    path=root/name
    before=hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
    data=base64.b64decode(value)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(data)
    changes.append({'file':name,'before':before,'after':hashlib.sha256(data).hexdigest()})
manifest=json.loads((root/'linux-source-manifest.json').read_text())
for name,info in manifest['files'].items():
    assert hashlib.sha256((root/name).read_bytes()).hexdigest()==info['sha256'],name
    if name.endswith('.py'): compile((root/name).read_bytes(),name,'exec')
print(json.dumps({'deployed':True,'root':str(root),'changes':changes}))
'@
 $source=$source.Replace('__PAYLOAD__',($payload|ConvertTo-Json -Compress -Depth 4))
 $result=(Invoke-LinuxObs -Command ("python3 - <<'PY'`n"+$source+"`nPY"))-join "`n"
 $dir="$script:LinuxRoot/linux"
 New-Item -ItemType Directory -Force $dir|Out-Null
 [IO.File]::WriteAllText("$dir/deploy.json",$result,(New-Object Text.UTF8Encoding($false)))
 $result
}
