. "$PSScriptRoot/l1.ps1"
function Get-L1TunnelProcess {
 param([int]$PidValue,[string]$CreatedUtc)
 $p=Get-Process -Id $PidValue -ErrorAction SilentlyContinue
 if(!$p){return $null}
 if($p.ProcessName -ne 'ssh'){throw 'Recorded tunnel PID belongs to another process; not stopping it'}
 if(!$p.Path -or $p.Path.Replace('\','/') -ne $script:C1Ssh){throw 'Cannot verify the recorded SSH executable'}
 if([Math]::Abs(($p.StartTime.ToUniversalTime()-[DateTime]::Parse($CreatedUtc).ToUniversalTime()).TotalSeconds) -gt 30){throw 'SSH PID start time differs from saved tunnel state'}
 return $p
}
function Start-L1Tunnel {
 param([switch]$Rebuild)
 Assert-C1Running
 Assert-L1AppAvailable
 if(Test-Path "$script:L1Root/tunnel-mode.json"){
  $mode=Get-Content -Raw -Encoding UTF8 "$script:L1Root/tunnel-mode.json"|ConvertFrom-Json
  if($mode.mode -eq 'remote'){
   $statePath="$script:L1Root/tunnel-state.json"
   $previous=Get-Content -Raw -Encoding UTF8 $statePath|ConvertFrom-Json
   if($previous.appPid -or $previous.taiPid){
    Invoke-L1 -May tai -Command 'test -z "$(sudo -n docker ps -q --filter name=rca-tai-)"'
    Write-L1Event -Kind 'legacy_tunnels_preserved' -Detail @{appPid=$previous.appPid;taiPid=$previous.taiPid;reason='Do not stop coordinator-owned Windows processes; remote route uses separate AWS loopback port 19091'}
    $stamp=[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ')
    Copy-Item -LiteralPath $statePath -Destination "$script:L1Root/bo-sung-1/local-tunnel-before-remote-$stamp.json"
   }
   $source="ACTION='start'`n"+[IO.File]::ReadAllText("$script:L1Root/tunnel-remote.py")
   $value=((Invoke-L1 -May app -Mutation -Command ("python3 - <<'PY'`n"+$source+"`nPY"))-join "`n")|ConvertFrom-Json
   $result=@{mode='remote';utc=[DateTime]::UtcNow.ToString('o');remote=$value}
   [IO.File]::WriteAllText($statePath,($result|ConvertTo-Json -Depth 8),(New-Object System.Text.UTF8Encoding($false)))
   if($value.startedNow){Write-L1Event -Kind 'remote_tunnel_started' -Detail $value}
   return $result
  }
 }
 $state="$script:L1Root/tunnel-state.json"
 $existing=$null
 if(Test-Path $state){
  $existing=Get-Content -Raw -Encoding UTF8 $state|ConvertFrom-Json
  $app=Get-L1TunnelProcess -PidValue $existing.appPid -CreatedUtc $existing.utc
  $tai=Get-L1TunnelProcess -PidValue $existing.taiPid -CreatedUtc $existing.utc
  if($app -and $tai -and !$Rebuild){return $existing}
  foreach($p in @($app,$tai)){if($p){Stop-Process -Id $p.Id -ErrorAction Stop}}
 }
 $stamp=[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ')
 $dir="$script:L1Root/bo-sung-1/tunnels/$stamp"
 New-Item -ItemType Directory -Force $dir|Out-Null
 if($existing){Copy-Item -LiteralPath $state -Destination "$dir/state-before.json"}
 $pids=@{utc=[DateTime]::UtcNow.ToString('o');logs=$dir}
 foreach($machine in @('app','tai')){
  $target=Get-C1Target $machine
  $forward=if($machine -eq 'app'){'-L 127.0.0.1:29090:127.0.0.1:19090'}else{'-R 127.0.0.1:19090:127.0.0.1:29090'}
  $args="-i `"$($target.Key)`" -o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=yes -o UserKnownHostsFile=`"$($target.Known)`" -o ExitOnForwardFailure=yes -o ServerAliveInterval=20 -o ServerAliveCountMax=3 -N $forward ubuntu@$($target.HostName)"
  Add-Content -Encoding UTF8 "$script:L1Root/thay-doi-may.md" ("`n"+[DateTime]::UtcNow.ToString('o')+" - local SSH tunnel $machine : $forward; previous state/logs retained; rollback stop verified new SSH PIDs only.")
  $p=Start-Process -FilePath $script:C1Ssh -ArgumentList $args -WindowStyle Hidden -PassThru -RedirectStandardError "$dir/$machine.stderr.txt" -RedirectStandardOutput "$dir/$machine.stdout.txt"
  $pids[$machine+'Pid']=$p.Id
 }
 [IO.File]::WriteAllText($state,($pids|ConvertTo-Json),(New-Object System.Text.UTF8Encoding($false)))
 Write-L1Event -Kind 'tunnel_started' -Detail $pids
 return $pids
}
