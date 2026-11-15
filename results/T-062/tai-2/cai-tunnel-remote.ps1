. "$PSScriptRoot/l1.ps1"
function Install-L1RemoteTunnel {
 Assert-L1AppAvailable
 Assert-C1Running
 Invoke-L1 -May tai -Command 'test -z "$(sudo -n docker ps -q --filter name=rca-tai-)"'
 $target=Get-C1Target tai
 $known=@([IO.File]::ReadAllLines($target.Known)|Where-Object {($_ -split '\s+')[0].Split(',') -contains $target.HostName}) -join "`n"
 if(!$known){throw 'Pinned host key for AWS absent; do not trust an unverified keyscan'}
 $source="ACTION='prepare'`nSOURCE_B64='"+[Convert]::ToBase64String([IO.File]::ReadAllBytes("$script:L1Root/tunnel-supervisor.py"))+"'`nKNOWN_B64='"+[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($known+"`n"))+"'`n"+[IO.File]::ReadAllText("$script:L1Root/tunnel-remote.py")
 $prepared=((Invoke-L1 -May app -Mutation -Command ("python3 - <<'PY'`n"+$source+"`nPY"))-join "`n")|ConvertFrom-Json
 Write-L1Event -Kind 'remote_tunnel_prepared' -Detail @{utc=$prepared.utc;before=$prepared.before;after=$prepared.after;privateKeyStoredOnlyOn=$prepared.privateKeyStoredOnlyOn}
 $install=@'
import datetime as dt,hashlib,json,os,sys
from pathlib import Path
public=sys.stdin.read().strip()
fingerprint=hashlib.sha256(public.encode()).hexdigest()
marker=Path('/opt/rca-tai/secret/l1-forward-key.json')
if marker.exists():
    if json.loads(marker.read_text())['publicKeySha256']!=fingerprint:raise SystemExit('A different L1 key is already provisioned')
    print(json.dumps({'alreadyProvisioned':True,'publicKeySha256':fingerprint}))
else:
    # Append only. Never read ~/.ssh or an existing authorized_keys file.
    target=Path.home()/'.ssh'/'authorized_keys'
    options='restrict,port-forwarding,command="/bin/false",permitlisten="127.0.0.1:19091",permitopen="127.0.0.1:19091",from="129.221.208.47" '
    fd=os.open(target,os.O_WRONLY|os.O_APPEND)
    try:os.write(fd,('\n'+options+public+'\n').encode())
    finally:os.close(fd)
    os.umask(0o077)
    value={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'publicKeySha256':fingerprint,
        'authorization':'new dedicated forward-only key, app source IP, AWS loopback port 19091; no shell',
        'rollback':'Stop L1 remote supervisor; an administrator may revoke exactly the l1-mock-forward-only authorized key. Existing keys were never read or changed.'}
    marker.write_text(json.dumps(value));os.chmod(marker,0o600)
    print(json.dumps(value))
'@
 Add-Content -Encoding UTF8 "$script:L1Root/thay-doi-may.md" ("`n"+[DateTime]::UtcNow.ToString('o')+" - tai: append a new constrained public key via memory stdin; no existing .ssh content read, no key material retained in command log. New-key fingerprint in bo-sung-1/tunnel-key-installed.json.")
 $target=Get-C1Target tai
 $code64=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($install))
 Invoke-L1 -May tai -Mutation -Command ("umask 077; mkdir -p /opt/rca-tai/bo-sung-1; printf %s "+$code64+" | base64 -d > /opt/rca-tai/bo-sung-1/install-forward-key.py")
 $remoteCommand='python3 /opt/rca-tai/bo-sung-1/install-forward-key.py'
 $result=$prepared.publicKey | & $script:C1Ssh -i $target.Key -o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=yes "-oUserKnownHostsFile=$($target.Known)" "ubuntu@$($target.HostName)" $remoteCommand
 if($LASTEXITCODE -ne 0){throw 'Constrained forward key provisioning failed; key omitted'}
 [IO.File]::WriteAllText("$script:L1Root/bo-sung-1/tunnel-key-installed.json",($result -join "`n")+"`n",(New-Object System.Text.UTF8Encoding($false)))
 $mode=@{mode='remote';transportUrl='http://127.0.0.1:19091';installedUtc=[DateTime]::UtcNow.ToString('o');root='/opt/flash-ticket-app/l1-vnpay/tunnel'}
 [IO.File]::WriteAllText("$script:L1Root/tunnel-mode.json",($mode|ConvertTo-Json),(New-Object System.Text.UTF8Encoding($false)))
 return @{utc=$prepared.utc;before=$prepared.before;after=$prepared.after;keyMaterial='Not retained in local output'}
}
