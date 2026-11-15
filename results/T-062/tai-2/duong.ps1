. "$PSScriptRoot/token-pool.ps1"
. "$PSScriptRoot/tunnel.ps1"
function Get-L1MockTransport {
 $url='http://127.0.0.1:19090'
 if(Test-Path "$script:L1Root/tunnel-mode.json"){
  $mode=Get-Content -Raw -Encoding UTF8 "$script:L1Root/tunnel-mode.json"|ConvertFrom-Json
  if($mode.mode -eq 'remote'){$url=$mode.transportUrl}
 }
 return $url
}
function Test-L1Duong {
 param([ValidateRange(1,100)][int]$TokenCount=20,[switch]$LamMoiToken)
 Assert-C1Running
 Assert-L1AppAvailable
 Invoke-L1 -May tai -Command 'test -z "$(sudo -n docker ps -q --filter name=rca-tai-)"'
 $source="RECOVER=True`n"+[IO.File]::ReadAllText("$script:L1Root/kiem-mock.py")
 $mock=((Invoke-L1 -May app -Mutation -Command ("python3 - <<'PY'`n"+$source+"`nPY"))-join "`n")|ConvertFrom-Json
 if($mock.restarted){Write-L1Event -Kind 'mock_restarted' -Detail $mock}
 $null=Start-L1Tunnel
 $url=Get-L1MockTransport
 $healthCommand='python3 -c "import urllib.request,json; r=urllib.request.urlopen('''+$url+'/health'',timeout=5); print(json.dumps({''status'':r.code,''up'':json.load(r).get(''status'')==''UP''}))"'
 try{$health=((Invoke-L1 -May tai -Command $healthCommand)-join "`n")|ConvertFrom-Json}catch{
  Write-L1Event -Kind 'tunnel_health_failed' -Detail @{action='rebuild verified SSH processes; preserve logs'}
  $null=Start-L1Tunnel -Rebuild
  $health=$null
  for($attempt=1;$attempt -le 3;$attempt++){
   try{$health=((Invoke-L1 -May tai -Command $healthCommand)-join "`n")|ConvertFrom-Json;break}catch{if($attempt -eq 3){throw};Start-Sleep -Seconds 5}
  }
 }
 if($health.status -ne 200 -or !$health.up){throw 'Load-machine to mock health failed'}
 $pool=((Invoke-L1Python -May tai -File "$script:L1Root/kiem-token-con-han.py")-join "`n")|ConvertFrom-Json
 if($LamMoiToken -or $pool.count -lt $TokenCount -or $pool.minAccessRemaining -lt 90 -or $pool.minRefreshRemaining -lt 300){
  $metadata=Initialize-L1Tokens -TokenCount $TokenCount
  Write-L1Event -Kind 'token_pool_renewed' -Detail $metadata
  $pool=((Invoke-L1Python -May tai -File "$script:L1Root/kiem-token-con-han.py")-join "`n")|ConvertFrom-Json
 }
 if($pool.count -lt $TokenCount -or !$pool.allBuyer -or $pool.minAccessRemaining -lt 90 -or $pool.permissionsOctal -ne '0o600'){throw 'Token pool validation failed; secrets omitted'}
 $result=[PSCustomObject]@{utc=[DateTime]::UtcNow.ToString('o');mock=$mock;tunnelHealth=$health;mockTransport=$url;tokens=$pool}
 Write-L1Event -Kind 'preflight_ok' -Detail $result
 return $result
}
