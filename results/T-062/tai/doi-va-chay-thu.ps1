$ErrorActionPreference='Stop'
. "$PSScriptRoot/chay-tai.ps1"
$deadline=[DateTime]::UtcNow.AddHours(8)
$gate="$script:C1Repo/results/T-062/ha-tang/A2-XONG"
while(!(Test-Path $gate)){
 Assert-C1Running
 if([DateTime]::UtcNow -gt $deadline){throw 'C1 blocked: A2-XONG not present after 8 hours'}
 $utc=[DateTime]::UtcNow.ToString('o')
 Add-Content -Encoding UTF8 "$PSScriptRoot/cho-a2.txt" "$utc A2-XONG absent; no load started"
 Set-Content -Encoding UTF8 "$PSScriptRoot/CHECKPOINT.md" "# C1 checkpoint`n`nHeartbeat UTC: $utc. Codex C1, Windows laptop; intent EXECUTE, scope results/T-062/tai and codex only. AWS primary per brief v3. Docker/k6/chrony verified; PKCE and fixture prepared; k6 inspect passed. Waiting for A2-XONG (max 8h); no load started. Stop flag checked every 5 seconds, gate every 5 minutes. Next: refresh login, reverify fixture through API, 300s at 5req/s, receive and summarize. Existing order tickets returned 500 before A2; do not guess cause. See thay-doi-may-tai.md and fixture-read-003.txt. Last command: doi-va-chay-thu.ps1 waiting loop. No task LOG/STATE write per brief."
 Write-Output "$utc waiting A2-XONG"
 for($i=0;$i -lt 60;$i++){Start-Sleep -Seconds 5; Assert-C1Running}
}
Assert-C1Running
Write-Output ('A2-XONG present '+[DateTime]::UtcNow.ToString('o'))
Copy-Item -LiteralPath $gate -Destination "$PSScriptRoot/a2-xong-c1.txt"
Initialize-C1Token -May tai | ConvertTo-Json -Compress | Add-Content -Encoding UTF8 "$PSScriptRoot/token-metadata.jsonl"
Invoke-C1 -May tai -Mutation -Command 'PYTHONDONTWRITEBYTECODE=1 python3 /opt/rca-tai/fixture.py --machine tai --create-if-empty' | Tee-Object -FilePath "$PSScriptRoot/fixture-sau-a2.txt"
$target=Get-C1Target tai
foreach($file in @('fixtures.json','fixture-evidence.json')){
 & 'C:/Program Files/Git/usr/bin/scp.exe' -i $target.Key -o BatchMode=yes -o StrictHostKeyChecking=yes "-oUserKnownHostsFile=$($target.Known)" "ubuntu@$($target.HostName):/opt/rca-tai/k6/$file" "$PSScriptRoot/k6/$file"
 if($LASTEXITCODE -ne 0){throw 'fixture receive failed'}
}
$tag='d'+[DateTime]::UtcNow.ToString('yyyyMMddHHmmss')
Set-Content -Encoding ASCII "$PSScriptRoot/pilot-tag.txt" $tag
Start-Tai -Seconds 300 -Rate 5 -Tag $tag -May tai
try{
 while($true){
  if(Test-Path D:/RCA-overnight/STOP){Stop-Tai -Tag $tag -May tai; throw 'STOP exists; load stopped, outputs retained'}
  $state=(Get-Tai -Tag $tag -May tai) -join "`n" | ConvertFrom-Json
  if(!$state.Running){Write-Output ('pilot exit '+$state.ExitCode); break}
  Write-Output ([DateTime]::UtcNow.ToString('o')+' pilot running '+$tag)
  for($i=0;$i -lt 4;$i++){
   Start-Sleep -Seconds 5
   if(Test-Path D:/RCA-overnight/STOP){Stop-Tai -Tag $tag -May tai; throw 'STOP exists; load stopped, outputs retained'}
  }
 }
}catch{
 Stop-Tai -Tag $tag -May tai
 throw
}
Receive-Tai -Tag $tag -May tai
New-Item -ItemType Directory -Force "$PSScriptRoot/chay-thu-5p" | Out-Null
Copy-Item -Path "$PSScriptRoot/out/$tag/*" -Destination "$PSScriptRoot/chay-thu-5p/"
Write-Output ('C1_PILOT_COLLECTED '+$tag)
