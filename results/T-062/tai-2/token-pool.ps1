. "$PSScriptRoot/l1.ps1"
function Initialize-L1Tokens {
 param([ValidateRange(1,100)][int]$TokenCount=20)
 Assert-L1AppAvailable
 $source=Get-L1AuthSource
 $source=$source.Replace("def role_token(role='BUYER'):","def role_token(role='BUYER', selected=None):")
 $source=$source.Replace("user=next(x for x in users if role in x.get('realmRoles',[]))","user=selected or next(x for x in users if role in x.get('realmRoles',[]))")
 $source=$source.Replace("return json.load(response)['access_token']",'return json.load(response)')
 $source+=@'

try:
    pool=json.loads((ROOT/'env/l1-buyers.json').read_text())
    values=[role_token(selected=pool[i % len(pool)]) for i in range(__TOKEN_COUNT__)]
    print(json.dumps({'tokens':values}))
except Exception:
    raise SystemExit('Pool PKCE failed; secret values omitted')
'@
 $source=$source.Replace('__TOKEN_COUNT__',[string]$TokenCount)
 $json=(Invoke-L1 -May app -Command ("python3 - <<'PY'`n"+$source+"`nPY")) -join "`n"
 try{$pool=$json|ConvertFrom-Json -ErrorAction Stop}catch{throw 'Invalid token pool; secrets omitted'}
 if($pool.tokens.Count -ne $TokenCount){throw 'Token session count mismatch'}
 $target=Get-C1Target tai
 Add-Content -Encoding UTF8 "$script:L1Root/thay-doi-may.md" ("`n## "+[DateTime]::UtcNow.ToString('o')+" - tai`nPKCE pool in memory -> umask 077; cat > /opt/rca-tai/secret/l1-tokens.json. No secret arguments/output. Reversible by minting a new pool; old session data stays outside repo.")
 $json | & $script:C1Ssh -i $target.Key -o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=yes "-oUserKnownHostsFile=$($target.Known)" "ubuntu@$($target.HostName)" 'umask 077; cat > /opt/rca-tai/secret/l1-tokens.json'
 if($LASTEXITCODE -ne 0){throw 'Token transfer failed'}
 [PSCustomObject]@{utc=[DateTime]::UtcNow.ToString('o');count=$pool.tokens.Count;expires_in=$pool.tokens[0].expires_in;refresh_expires_in=$pool.tokens[0].refresh_expires_in}
 $json=$null;$pool=$null
}
