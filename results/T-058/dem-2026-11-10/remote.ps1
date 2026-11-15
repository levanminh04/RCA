function Invoke-Oracle {
 param([ValidateSet('app','obs')][string]$Machine,[string]$Command)
 if($Machine -eq 'app'){ $key='D:/RCA-ext/keys/exp-app/ssh-key-2026-11-10 (1).key'; $target='ubuntu@129.221.208.47' }else{ $key='D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key'; $target='ubuntu@213.35.116.128' }
 & 'C:/Program Files/Git/usr/bin/ssh.exe' -i $key -o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts $target ('printf %s ' + [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Command)) + ' | base64 -d | bash')
 if($LASTEXITCODE -ne 0){ throw "SSH $Machine exit $LASTEXITCODE" }
}
function Copy-Oracle {
 param([ValidateSet('app','obs')][string]$Machine,[string]$Source,[string]$Destination)
 if($Machine -eq 'app'){ $key='D:/RCA-ext/keys/exp-app/ssh-key-2026-11-10 (1).key'; $target='ubuntu@129.221.208.47' }else{ $key='D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key'; $target='ubuntu@213.35.116.128' }
 & 'C:/Program Files/Git/usr/bin/scp.exe' -i $key -o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts $Source "${target}:$Destination"
 if($LASTEXITCODE -ne 0){ throw "SCP $Machine exit $LASTEXITCODE" }
}function Receive-Oracle {
 param([ValidateSet('app','obs')][string]$Machine,[string]$Source,[string]$Destination)
 if($Machine -eq 'app'){ $key='D:/RCA-ext/keys/exp-app/ssh-key-2026-11-10 (1).key'; $target='ubuntu@129.221.208.47' }else{ $key='D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key'; $target='ubuntu@213.35.116.128' }
 & 'C:/Program Files/Git/usr/bin/scp.exe' -i $key -o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts "${target}:$Source" $Destination
 if($LASTEXITCODE -ne 0){ throw "Receive $Machine exit $LASTEXITCODE" }
}