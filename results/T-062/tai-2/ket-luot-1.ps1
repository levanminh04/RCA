$ErrorActionPreference='Stop'
. "$PSScriptRoot/phan-tich.ps1"
while($true){
 if(Test-Path D:/RCA-overnight/STOP){Stop-Tai -Tag l1r20261112a;throw 'STOP: stopped first comparison run; checkpoint required'}
 $state=((Get-Tai -Tag l1r20261112a -May tai)-join "`n")|ConvertFrom-Json
 if(!$state.Running){break}
 Start-Sleep -Seconds 10
}
Receive-Tai -Scenario hanh-trinh -Tag l1r20261112a -May tai
Analyze-Tai -Tag l1r20261112a
$analysis=Get-Content -Raw -Encoding UTF8 "$script:L1Root/out/l1r20261112a/analysis.json"|ConvertFrom-Json
if($analysis.totals.journey_failed -or $analysis.totals.token_refresh_failure){throw 'First comparison run has journey/token failures; inspect before continuing'}
Invoke-L1Python -Auth -File "$script:L1Root/kiem-cuoi-api.py"|Set-Content -Encoding UTF8 "$script:L1Root/kiem-cuoi-api.jsonl"
Start-Tai -Scenario hanh-trinh -Seconds 600 -Tag l1r20261112b -May tai
Add-Content -Encoding UTF8 "$script:L1Root/CHECKPOINT.md" ("`n"+[DateTime]::UtcNow.ToString('o')+" - Run l1r20261112a received/analyzed. Read-only API probes saved in kiem-cuoi-api.jsonl between windows. Started l1r20261112b (600s), unchanged config. Check Get-Tai for actual state; do not repeat run a.")
