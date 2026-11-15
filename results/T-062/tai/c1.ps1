$script:C1Root=$PSScriptRoot
$script:C1Repo=(Resolve-Path "$PSScriptRoot/../../..").Path
$script:C1Ssh='C:/Program Files/Git/usr/bin/ssh.exe'
function Assert-C1Running {
 if(Test-Path D:/RCA-overnight/STOP){throw 'STOP exists'}
}
function Get-C1Target {
 param([ValidateSet('obs','tai','app')][string]$May='tai')
 switch($May){
 'tai' {return @{HostName='3.24.8.49';Key='D:/RCA-ext/keys/Hahaa123.pem';Known='D:/RCA-ext/keys/known_hosts'}}
 'obs' {return @{HostName='213.35.116.128';Key='D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key';Known='D:/RCA-ext/overnight-T058/out/known_hosts'}}
 'app' {return @{HostName='129.221.208.47';Key='D:/RCA-ext/keys/exp-app/ssh-key-2026-11-10 (1).key';Known='D:/RCA-ext/overnight-T058/out/known_hosts'}}
 }
}
function Invoke-C1 {
 param([ValidateSet('obs','tai','app')][string]$May='tai',[string]$Command,[switch]$Mutation,[switch]$IgnoreStop)
 if(!$IgnoreStop){Assert-C1Running}
 if($May -eq 'app' -and $Mutation){throw 'exp-app is read-only'}
 $target=Get-C1Target $May
 if($Mutation){Add-Content -Encoding UTF8 "$script:C1Root/thay-doi-may-tai.md" ("`n## "+[DateTime]::UtcNow.ToString('o')+" - $May`n`n"+'```sh'+"`n$Command`n"+'```')}
 $encoded=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Command))
 & $script:C1Ssh -i $target.Key -o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=yes "-oUserKnownHostsFile=$($target.Known)" "ubuntu@$($target.HostName)" ('printf %s '+$encoded+' | base64 -d | bash')
 $exit=$LASTEXITCODE
 if($Mutation){Add-Content -Encoding UTF8 "$script:C1Root/thay-doi-may-tai.md" "`nExit: $exit"}
 if($exit -ne 0){throw "SSH $May exit $exit"}
}
function Send-C1File {
 param([ValidateSet('obs','tai')][string]$May='tai',[string]$Source,[string]$Destination)
 Assert-C1Running
 $target=Get-C1Target $May
 Add-Content -Encoding UTF8 "$script:C1Root/thay-doi-may-tai.md" ("`n"+[DateTime]::UtcNow.ToString('o')+" - $May : scp $Source -> $Destination ; sha256="+(Get-FileHash -Algorithm SHA256 -LiteralPath $Source).Hash)
 & 'C:/Program Files/Git/usr/bin/scp.exe' -i $target.Key -o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=yes "-oUserKnownHostsFile=$($target.Known)" $Source "ubuntu@$($target.HostName):$Destination"
 if($LASTEXITCODE -ne 0){throw 'SCP failed'}
}
function Initialize-C1Token {
 param([ValidateSet('obs','tai')][string]$May='tai')
 Assert-C1Running
 $pinManifest=Get-Content -Raw -Encoding UTF8 "$script:C1Repo/results/T-058/dem-2026-11-10/artifacts-sha256.json" | ConvertFrom-Json
 $authHash=(Get-FileHash -Algorithm SHA256 "$script:C1Repo/results/T-058/dem-2026-11-10/auth.py").Hash.ToLower()
 if($authHash -ne $pinManifest.files.'auth.py'.sha256){throw 'auth.py differs from source manifest; stopped'}
 $source=[IO.File]::ReadAllText("$script:C1Repo/results/T-058/dem-2026-11-10/auth.py")
 $source=$source.Substring(0,$source.IndexOf("if __name__=='__main__':"))
 $source=$source.Replace("return json.load(response)['access_token']",'return json.load(response)')
 $source+="`ntry:`n    print(json.dumps(role_token()))`nexcept Exception:`n    raise SystemExit(1)`n"
 # Capture stdout in memory. Tokens never become arguments or console output.
 $tokens=(Invoke-C1 -May app -Command ("python3 - <<'PY'`n"+$source+"`nPY")) -join "`n"
 try{$value=$tokens | ConvertFrom-Json -ErrorAction Stop}catch{throw 'Malformed PKCE response; secret values omitted'}
 if(!$value.access_token -or !$value.refresh_token){throw 'PKCE response incomplete'}
 $target=Get-C1Target $May
 Add-Content -Encoding UTF8 "$script:C1Root/thay-doi-may-tai.md" ("`n"+[DateTime]::UtcNow.ToString('o')+" - $May : PKCE memory pipe -> umask 077; cat > /opt/rca-tai/secret/tokens.json (values omitted)")
 $tokens | & $script:C1Ssh -i $target.Key -o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=yes "-oUserKnownHostsFile=$($target.Known)" "ubuntu@$($target.HostName)" 'umask 077; cat > /opt/rca-tai/secret/tokens.json'
 if($LASTEXITCODE -ne 0){throw 'Token pipe failed'}
 [PSCustomObject]@{utc=[DateTime]::UtcNow.ToString('o');machine=$May;flow='PKCE';expires_in=$value.expires_in;refresh_expires_in=$value.refresh_expires_in}
 $tokens=$null;$value=$null
}
