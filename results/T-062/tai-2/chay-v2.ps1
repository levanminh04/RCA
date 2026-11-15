$ErrorActionPreference='Stop'
. "$PSScriptRoot/phan-tich.ps1"
function Wait-L1Run([string]$Tag){
 while($true){
  if(Test-Path D:/RCA-overnight/STOP){
   Stop-Tai -Tag $Tag
   Add-Content -Encoding UTF8 "$script:L1Root/CHECKPOINT.md" ("`n"+[DateTime]::UtcNow.ToString('o')+" STOP: stopped $Tag; outputs retained; receive after handoff.")
   throw 'STOP boundary reached'
  }
  $state=((Get-Tai -Tag $Tag -May tai)-join "`n")|ConvertFrom-Json
  if(!$state.Running){return}
  Start-Sleep -Seconds 10
 }
}
function Collect-L1Run([string]$Tag){
 Wait-L1Run $Tag
 Receive-Tai -Scenario hanh-trinh -Tag $Tag -May tai
 Analyze-Tai -Tag $Tag
 Add-Content -Encoding UTF8 "$script:L1Root/CHECKPOINT.md" ("`n"+[DateTime]::UtcNow.ToString('o')+" Completed and received $Tag; see out/$Tag/analysis.json. No repeat needed for valid outputs.")
}
$pin=(Get-FileHash -Algorithm SHA256 "$script:L1Root/k6/hanh-trinh.js").Hash
Collect-L1Run 'l1p20261112v2'
$a=Get-Content -Raw -Encoding UTF8 "$script:L1Root/out/l1p20261112v2/analysis.json"|ConvertFrom-Json
if($a.totals.journey_failed -or $a.totals.dropped_iterations -or $a.totals.gateway_401 -or $a.totals.token_refresh_failure -or $a.gateway.missing.Count -or $a.gateway.mismatches.Count){throw 'Pilot needs diagnosis; comparison runs not started'}
$b=[IO.File]::ReadAllText("$script:L1Root/BAN-GIAO-2-template.md")
$mix=($a.journeys.journey_started|ConvertTo-Json -Compress)
$matched=($a.gateway.matchedRoutes.PSObject.Properties|Measure-Object -Property Value -Sum).Sum
$r=@{'@UTC@'=[DateTime]::UtcNow.ToString('o');'@STARTED@'=[string]$a.totals.journey_started;'@MIX@'=$mix;'@FINISHED@'=[string]$a.totals.journey_finished;'@FAILED@'=[string][int]$a.totals.journey_failed;'@DROPPED@'=[string][int]$a.totals.dropped_iterations;'@UNAUTH@'=[string][int]$a.totals.gateway_401;'@REFRESH@'=[string]$a.totals.token_refresh_success;'@REQUESTS@'=[string]$a.totals.route_responses;'@MATCHED@'=[string]$matched;'@MISSING@'=[string]$a.gateway.missing.Count;'@MISMATCH@'=[string]$a.gateway.mismatches.Count}
foreach($k in $r.Keys){$b=$b.Replace($k,$r[$k])}
[IO.File]::WriteAllText("$script:L1Root/BAN-GIAO-2-kich-ban.md",$b,(New-Object System.Text.UTF8Encoding($false)))
foreach($tag in @('l1r20261112v2a','l1r20261112v2b')){
 if((Get-FileHash -Algorithm SHA256 "$script:L1Root/k6/hanh-trinh.js").Hash -ne $pin){throw 'Source changed between comparison runs'}
 Start-Tai -Scenario hanh-trinh -Seconds 600 -Tag $tag -May tai
 Add-Content -Encoding UTF8 "$script:L1Root/CHECKPOINT.md" ("`n"+[DateTime]::UtcNow.ToString('o')+" Started $tag (600s), unchanged source/config; use Get-Tai for current state.")
 Collect-L1Run $tag
}
