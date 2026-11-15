param([string]$Nhom='kiem')
$ErrorActionPreference='Stop'
if(Test-Path D:/RCA-overnight/STOP){throw 'STOP local'}
$r=Get-Content -Raw -Encoding utf8 D:/RCA-flashticket/results/T-065/l5-obs.py | & 'C:/Program Files/Git/usr/bin/ssh.exe' -i D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key -o BatchMode=yes -o ConnectTimeout=15 -o UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts -o StrictHostKeyChecking=yes ubuntu@213.35.116.128 'python3 - machine'
if($LASTEXITCODE -ne 0){throw 'SSH machine failed'}
$obj=$r | ConvertFrom-Json
$obj | Add-Member -NotePropertyName nhom -NotePropertyValue $Nhom
$obj | ConvertTo-Json -Compress | Add-Content -Encoding utf8 D:/RCA-flashticket/results/T-065/kiem/003-trinh-duyet/may.jsonl
$s=Get-Content -Raw D:/RCA-flashticket/results/T-065/codex/L5-trang-thai.json|ConvertFrom-Json
$s.cap_nhat=[DateTime]::UtcNow.ToString('o');$s.buoc=$Nhom
$s|ConvertTo-Json|Set-Content -Encoding utf8 D:/RCA-flashticket/results/T-065/codex/L5-trang-thai.json
if($obj.stop){throw 'STOP remote'}
$obj | ConvertTo-Json -Compress
