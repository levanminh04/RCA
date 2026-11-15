param([ValidateSet('before','apply','after','render','rollback')][string]$Action='before',[string]$OutputName='')
$ErrorActionPreference='Stop'
$OutputEncoding=[Console]::OutputEncoding=[System.Text.UTF8Encoding]::new($false)
$taskDir='D:/RCA-flashticket/results/T-065/kiem/008-s1'
if(Test-Path -LiteralPath 'D:/RCA-overnight/STOP'){throw 'STOP local'}
if(Test-Path -LiteralPath (Join-Path $HOME 'rca-dieu-phoi/STOP')){throw 'STOP home'}
if(!$OutputName){$OutputName=$Action+'-001.json'}
if([IO.Path]::GetFileName($OutputName) -ne $OutputName){throw 'OutputName must be a filename'}
$outputPath=Join-Path $taskDir $OutputName
if(Test-Path -LiteralPath $outputPath){throw 'Preserve prior attempt; use a new OutputName'}
$raw=Get-Content -Raw -Encoding UTF8 -LiteralPath (Join-Path $taskDir 's1-may.py') | & 'C:/Program Files/Git/usr/bin/ssh.exe' -i 'D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key' -o BatchMode=yes -o ConnectTimeout=15 -o UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts -o StrictHostKeyChecking=yes -o UpdateHostKeys=no ubuntu@213.35.116.128 ('python3 -B - '+$Action)
$sshExit=$LASTEXITCODE
[IO.File]::WriteAllText($outputPath,($raw -join [Environment]::NewLine)+[Environment]::NewLine,[System.Text.UTF8Encoding]::new($false))
Write-Output ('Saved '+$OutputName+'; SSH exit '+$sshExit)
if($sshExit -ne 0){throw ('SSH '+$Action+' exit '+$sshExit+'; evidence retained')}
