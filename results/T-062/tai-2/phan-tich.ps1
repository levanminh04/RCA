. "$PSScriptRoot/chay-tai.ps1"
function Analyze-Tai {
 param([Parameter(Mandatory)][ValidatePattern('^[a-z0-9][a-z0-9-]{0,47}$')][string]$Tag)
 $root="$script:L1Root/out/$Tag"
 $state=Get-Content -Raw -Encoding UTF8 "$root/state.json"|ConvertFrom-Json
 $start=Get-Content -Raw -Encoding UTF8 "$root/start-utc.txt"
 $source='SINCE = '+('"'+$start.Trim()+'"')+"`nUNTIL = "+('"'+$state.FinishedAt+'"')+"`n"+[IO.File]::ReadAllText("$script:L1Root/gateway-log.py")
 $gateway=Invoke-L1 -May app -Command ("python3 - <<'PY'`n"+$source+"`nPY")
 [IO.File]::WriteAllText("$root/gateway.jsonl",($gateway -join "`n")+"`n",(New-Object System.Text.UTF8Encoding($false)))
 $files=@{'analyze.py'=[Convert]::ToBase64String([IO.File]::ReadAllBytes("$script:L1Root/analyze.py"));'gateway.jsonl'=[Convert]::ToBase64String([IO.File]::ReadAllBytes("$root/gateway.jsonl"))}
 $prepare="import base64,pathlib`nroot=pathlib.Path('/opt/rca-tai/out/$Tag')`nfiles="+($files|ConvertTo-Json -Compress)+"`nfor name,b64 in files.items(): (root/name).write_bytes(base64.b64decode(b64))`n"
 Invoke-L1 -May tai -Mutation -Command ("python3 - <<'PY'`n"+$prepare+"`nPY`npython3 /opt/rca-tai/out/$Tag/analyze.py /opt/rca-tai/out/$Tag")
 $target=Get-C1Target tai
 foreach($name in @('analysis.json','routes.csv','analyze.py')){
  & 'C:/Program Files/Git/usr/bin/scp.exe' -i $target.Key -o BatchMode=yes -o StrictHostKeyChecking=yes "-oUserKnownHostsFile=$($target.Known)" "ubuntu@$($target.HostName):/opt/rca-tai/out/$Tag/$name" "$root/$name"
  if($LASTEXITCODE -ne 0){throw "Receive analysis failed: $name"}
 }
}
