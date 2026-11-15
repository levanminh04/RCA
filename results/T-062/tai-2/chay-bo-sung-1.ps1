$ErrorActionPreference='Stop'
. "$PSScriptRoot/phan-tich.ps1"
. "$PSScriptRoot/cai-tunnel-remote.ps1"
$supplement="$PSScriptRoot/bo-sung-1"
function Save-L1Supplement([string]$Stage,[object]$Detail){
 $old=$null
 if(Test-Path "$supplement/checkpoint.json"){$old=Get-Content -Raw -Encoding UTF8 "$supplement/checkpoint.json"|ConvertFrom-Json}
 $value=@{utc=[DateTime]::UtcNow.ToString('o');stage=$Stage;detail=$Detail}
 [IO.File]::WriteAllText("$supplement/checkpoint.json",($value|ConvertTo-Json -Depth 12),(New-Object System.Text.UTF8Encoding($false)))
 if(!$old -or $old.stage -ne $Stage){[IO.File]::AppendAllText("$PSScriptRoot/CHECKPOINT.md",("`n"+$value.utc+" - L1 supplement: $Stage. See bo-sung-1/checkpoint.json.`n"),(New-Object System.Text.UTF8Encoding($false)))}
}
function Save-L1Json([string]$Path,[object]$Value){[IO.File]::WriteAllText($Path,($Value|ConvertTo-Json -Depth 15),(New-Object System.Text.UTF8Encoding($false)))}
function Wait-L1Idle {
 while($true){
  Assert-C1Running
  $names=@(Invoke-L1 -May tai -Command 'sudo -n docker ps --filter name=rca-tai- --format "{{.Names}}"')
  if(!$names.Count){return}
  Save-L1Supplement 'waiting_for_coordinator_load' @{containers=$names;action='Read only; never stop coordinator container'}
  Start-Sleep -Seconds 30
 }
}
function Collect-L1SupplementRun([string]$Tag){
 while($true){
  if(Test-Path D:/RCA-overnight/STOP){Stop-Tai -Tag $Tag;Save-L1Supplement 'STOP_own_run_stopped' @{tag=$Tag};throw 'STOP boundary reached'}
  $state=((Get-Tai -Tag $Tag -May tai)-join "`n")|ConvertFrom-Json
  if(!$state.Running){break}
  Start-Sleep -Seconds 10
 }
 Receive-Tai -Scenario hanh-trinh -Tag $Tag -May tai
 Analyze-Tai -Tag $Tag
 Save-L1Supplement 'run_received_and_analyzed' @{tag=$Tag;path="out/$Tag/analysis.json"}
}
try {
 Wait-L1Idle
 Assert-L1AppAvailable
 Save-L1Supplement 'install_remote_tunnel' @{reason='AWS idle; eliminate laptop/Codex process lifetime dependency'}
 if(!(Test-Path "$PSScriptRoot/tunnel-mode.json")){$null=Install-L1RemoteTunnel}
 $result=Test-L1Duong -TokenCount 40
 Save-L1Json "$supplement/preflight-remote-first.json" $result
 # A later SSH invocation, after launcher exit, must observe the same supervisor PID.
 $source="ACTION='status'`n"+[IO.File]::ReadAllText("$PSScriptRoot/tunnel-remote.py")
 $proof=((Invoke-L1 -May app -Command ("python3 - <<'PY'`n"+$source+"`nPY"))-join "`n")|ConvertFrom-Json
 Save-L1Json "$supplement/tunnel-independent-launcher-proof.json" $proof
 if(!$proof.alive){throw 'Remote supervisor did not survive SSH launcher exit'}
 if(!(Test-Path "$supplement/phuc-hoi-remote-ssh.json")){
  $kill=@'
import datetime as dt,json,os,signal,time
from pathlib import Path
root=Path('/opt/flash-ticket-app/l1-vnpay/tunnel')
pid=int((root/'ssh.pid').read_text())
cmdline=Path(f'/proc/{pid}/cmdline').read_bytes()
if b'forward-only.key' not in cmdline or b'127.0.0.1:19091:127.0.0.1:19090' not in cmdline:raise SystemExit('Not the dedicated L1 forward')
os.kill(pid,signal.SIGTERM)
print(json.dumps({'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'stoppedOnlyL1SshPid':pid,'purpose':'Recovery test with no workload; supervisor must reconnect'}))
'@
  $stopped=((Invoke-L1 -May app -Mutation -Command ("python3 - <<'PY'`n"+$kill+"`nPY"))-join "`n")|ConvertFrom-Json
  Write-L1Event -Kind 'remote_ssh_recovery_test' -Detail $stopped
  Start-Sleep -Seconds 7
  $result=Test-L1Duong -TokenCount 40
  Save-L1Json "$supplement/phuc-hoi-remote-ssh.json" @{stopped=$stopped;after=$result}
 }
 if(!(Test-Path "$supplement/phuc-hoi-mock.json")){
  $kill=@'
import datetime as dt,hashlib,json,os,signal,time
from pathlib import Path
root=Path('/opt/flash-ticket-app/l1-vnpay')
pid=int((root/'pid').read_text())
if str(root/'mock-runner.py').encode() not in Path(f'/proc/{pid}/cmdline').read_bytes():raise SystemExit('Not the L1 mock process')
before={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in ['mock-runner.py','mock_vnpay.py','mock.env','state.json','audit.jsonl']}
os.kill(pid,signal.SIGTERM)
for _ in range(20):
    if not Path(f'/proc/{pid}/cmdline').exists():break
    time.sleep(0.1)
print(json.dumps({'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'stoppedOnlyL1MockPid':pid,'before':before,'purpose':'Recovery test with no workload; preserve all state/audit/config'}))
'@
  $stopped=((Invoke-L1 -May app -Mutation -Command ("python3 - <<'PY'`n"+$kill+"`nPY"))-join "`n")|ConvertFrom-Json
  Write-L1Event -Kind 'mock_recovery_test' -Detail $stopped
  $result=Test-L1Duong -TokenCount 40
  Save-L1Json "$supplement/phuc-hoi-mock.json" @{stopped=$stopped;after=$result}
 }
 if(!(Test-Path "$supplement/giao-dich-sau-bao-tri.json")){
  Save-L1Supplement 'post_maintenance_purchase' @{}
  $value=((Invoke-L1Python -Auth -File "$PSScriptRoot/giao-dich-sau-bao-tri.py")-join "`n")|ConvertFrom-Json
  Save-L1Json "$supplement/giao-dich-sau-bao-tri.json" $value
  if($value.failureType -or $value.states[-1].state -ne 'COMPLETED' -or $value.tickets.tickets.Count -ne 1){throw 'Post-maintenance purchase failed; preserve evidence before retry'}
 }
 foreach($tag in @('l1maint20261113a','l1step20261113a')){
  if(Test-Path "$PSScriptRoot/out/$tag/analysis.json"){continue}
  Wait-L1Idle
  if($tag -eq 'l1maint20261113a'){
   Save-L1Supplement 'start_post_maintenance_5min' @{tag=$tag}
   Start-Tai -Scenario hanh-trinh -Seconds 300 -Tag $tag -May tai
  } else {
   Save-L1Supplement 'start_240s_step120_multiplier3' @{tag=$tag}
   Start-Tai -Scenario hanh-trinh -Seconds 240 -BuocTai 120 -Multiplier 3 -Tag $tag -May tai
  }
  Collect-L1SupplementRun $tag
 }
 $source="import sys`nsys.argv=['bins','/opt/rca-tai/out/l1step20261113a']`n"+[IO.File]::ReadAllText("$PSScriptRoot/bang-buoc-tai.py")
 $bins=Invoke-L1 -May tai -Mutation -Command ("python3 - <<'PY'`n"+$source+"`nPY")
 [IO.File]::WriteAllText("$supplement/buoc-tai.json",($bins -join "`n")+"`n",(New-Object System.Text.UTF8Encoding($false)))
 Save-L1Supplement 'measurements_complete_prepare_handoff' @{runs=@('l1maint20261113a','l1step20261113a')}
} catch {
 Save-L1Supplement 'needs_diagnosis' @{error=$_.Exception.Message;rule='Preserve all files and runs; never stop coordinator load'}
 throw
}
