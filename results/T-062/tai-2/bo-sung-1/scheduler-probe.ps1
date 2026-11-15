$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$value=@{utc=[DateTime]::UtcNow.ToString('o');pid=$PID;identity=[Security.Principal.WindowsIdentity]::GetCurrent().Name;purpose='Verify Task Scheduler launch independent of Codex process'}|ConvertTo-Json -Compress
[IO.File]::AppendAllText("$root/scheduler-proof.jsonl",$value+"`n",(New-Object System.Text.UTF8Encoding($false)))
Start-Sleep -Seconds 15
[IO.File]::AppendAllText("$root/scheduler-proof.jsonl",([DateTime]::UtcNow.ToString('o')+" finished`n"),(New-Object System.Text.UTF8Encoding($false)))
