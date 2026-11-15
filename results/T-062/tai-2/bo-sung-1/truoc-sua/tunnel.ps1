. "$PSScriptRoot/l1.ps1"
function Start-L1Tunnel {
 Assert-C1Running
 $state="$script:L1Root/tunnel-state.json"
 if(Test-Path $state){
  $existing=Get-Content -Raw $state|ConvertFrom-Json
  if((Get-Process -Id $existing.appPid -ErrorAction SilentlyContinue) -and (Get-Process -Id $existing.taiPid -ErrorAction SilentlyContinue)){return $existing}
  throw 'Tunnel state exists but a process ended; inspect retained stderr before restarting'
 }
 $pids=@{}
 foreach($machine in @('app','tai')){
  $target=Get-C1Target $machine
  $forward=if($machine -eq 'app'){'-L 127.0.0.1:29090:127.0.0.1:19090'}else{'-R 127.0.0.1:19090:127.0.0.1:29090'}
  $args="-i `"$($target.Key)`" -o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=yes -o UserKnownHostsFile=`"$($target.Known)`" -o ExitOnForwardFailure=yes -o ServerAliveInterval=20 -o ServerAliveCountMax=3 -N $forward ubuntu@$($target.HostName)"
  Add-Content -Encoding UTF8 "$script:L1Root/thay-doi-may.md" ("`n"+[DateTime]::UtcNow.ToString('o')+" - local SSH tunnel $machine : $forward; rollback Stop-Process only recorded PIDs after checking command line. No remote firewall/config change.")
  $p=Start-Process -FilePath $script:C1Ssh -ArgumentList $args -WindowStyle Hidden -PassThru -RedirectStandardError "$script:L1Root/tunnel-$machine.stderr.txt" -RedirectStandardOutput "$script:L1Root/tunnel-$machine.stdout.txt"
  $pids[$machine+'Pid']=$p.Id
 }
 $pids.utc=[DateTime]::UtcNow.ToString('o')
 $pids|ConvertTo-Json|Set-Content -Encoding UTF8 $state
 return $pids
}
