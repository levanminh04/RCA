$ErrorActionPreference='Stop'
. "$PSScriptRoot/phan-tich.ps1"
$dir="$PSScriptRoot/bo-sung-1"
while(!(Test-Path "$PSScriptRoot/out/l1step20261113a/analysis.json")){
 Assert-C1Running
 Start-Sleep -Seconds 10
}
$step=Get-Content -Raw -Encoding UTF8 "$PSScriptRoot/out/l1step20261113a/analysis.json"|ConvertFrom-Json
if($step.totals.journey_failed -or $step.totals.dropped_iterations -or $step.totals.gateway_401 -or $step.gateway.missing.Count -or $step.gateway.mismatches.Count){throw 'Step run not clean; no further pilot automatically authorized by this plan'}
$plan=@{utc=[DateTime]::UtcNow.ToString('o');reason='Initial 300s integration pilot has 33 create-payment 503/504 failures. Subsequent unchanged workload now completes 240s including x3 with no journey errors/dropped/401. Verify current standard rate for 300s once; preserve both periods and keep original cause open.';reuse='Do not repeat old valid pilot, original two 10min runs, account/event/mock setup or stepped run';cost='One additional 300s workload plus receive/analysis; no code/config/restart intervention';newEvidence='Distinguish current recovered standard behavior from earlier failing window; this does not identify the cause of the earlier 503/504';tag='l1maint20261113b'}
[IO.File]::WriteAllText("$dir/ke-hoach-kiem-lai-pilot.json",($plan|ConvertTo-Json -Depth 8),(New-Object System.Text.UTF8Encoding($false)))
[IO.File]::AppendAllText("$PSScriptRoot/CHECKPOINT.md",("`n"+$plan.utc+" - Additional standard 300s pilot planned only after clean stepped run; see bo-sung-1/ke-hoach-kiem-lai-pilot.json. Earlier failing pilot retained and cause remains OPEN.`n"),(New-Object System.Text.UTF8Encoding($false)))
if(Test-Path "$PSScriptRoot/out/l1maint20261113b"){throw 'Additional pilot exists; inspect/reuse instead of repeating'}
Start-Tai -Scenario hanh-trinh -Seconds 300 -Tag l1maint20261113b -May tai
while($true){
 if(Test-Path D:/RCA-overnight/STOP){Stop-Tai -Tag l1maint20261113b;throw 'STOP boundary reached'}
 $state=((Get-Tai -Tag l1maint20261113b -May tai)-join "`n")|ConvertFrom-Json
 if(!$state.Running){break}
 Start-Sleep -Seconds 10
}
Receive-Tai -Scenario hanh-trinh -Tag l1maint20261113b -May tai
Analyze-Tai -Tag l1maint20261113b
[IO.File]::AppendAllText("$PSScriptRoot/CHECKPOINT.md",("`n"+[DateTime]::UtcNow.ToString('o')+" - l1maint20261113b received/analyzed; current pilot in out/l1maint20261113b/analysis.json; keep earlier failing l1maint20261113a separate.`n"),(New-Object System.Text.UTF8Encoding($false)))
