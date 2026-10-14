param([Parameter(Mandatory=$true)][long]$OtherTaskBytes)
$ErrorActionPreference = 'Stop'
$taskRepo = 'D:/RCA-flashticket'
$taskOutput = "$taskRepo/results/T-032/runs/microrank-laptop-diagnostic-001"
$taskPython = 'D:/RCA-ext/envs/T-014-main/Scripts/python.exe'
$taskWrapper = "$taskRepo/results/T-032/scripts/diagnose_microrank_laptop_v2.py"
$taskWrapperHash = '3f9eb062d72b2a3316b6208d33cd9168b42a097de873c26e20bb1b6e96e2de10'
$taskThreads = @('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')
foreach ($taskName in $taskThreads) {
    if ([Environment]::GetEnvironmentVariable($taskName, 'Process') -ne $null) { throw "Q-100 requires unset $taskName" }
}
if ((Get-FileHash -LiteralPath $taskWrapper -Algorithm SHA256).Hash.ToLowerInvariant() -ne $taskWrapperHash) { throw 'Wrapper pin differs; no launch' }
if (Test-Path -LiteralPath $taskOutput) { throw 'Run already exists; no overwrite or retry' }
if ($OtherTaskBytes -lt 0 -or $OtherTaskBytes -gt (12GB - 150MB)) { throw 'Combined task budget insufficient' }

# These values are process-local, as in the frozen source invocation. The five
# thread variables are checked and left untouched. No persistent settings change.
$env:PYTHONHASHSEED = '0'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONPATH = 'D:/RCA-ext/src/RCAEval;D:/RCA-ext/src/baro;D:/RCA-ext/work/T-014/CIRCA;D:/RCA-flashticket/src'
$env:TMP = "$taskOutput/tmp"
$env:TEMP = "$taskOutput/tmp"
$env:MPLCONFIGDIR = "$taskOutput/cache/mpl"
New-Item -ItemType Directory -Path $taskOutput -ErrorAction Stop | Out-Null
$taskUtf8 = New-Object System.Text.UTF8Encoding($false)
function Write-TaskNewJson([string]$TaskPath, $TaskValue) {
    if (Test-Path -LiteralPath $TaskPath) { throw "Refuse overwrite: $TaskPath" }
    [IO.File]::WriteAllText($TaskPath, (($TaskValue | ConvertTo-Json -Depth 30) + "`n"), $taskUtf8)
}
$taskArguments = @('-B','-W','ignore','-X','utf8',$taskWrapper,'run','--other-task-bytes',[string]$OtherTaskBytes)
Write-TaskNewJson "$taskOutput/launcher.json" ([ordered]@{
    at = (Get-Date).ToString('o'); launcher_pid = $PID; executable = $taskPython;
    argv = $taskArguments; cwd = $taskRepo; wrapper_sha256 = $taskWrapperHash;
    launcher_sha256 = (Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();
    other_task_bytes = $OtherTaskBytes; max_wall_s = 600; max_new_bytes = 150MB;
    process_local_environment = [ordered]@{PYTHONHASHSEED=$env:PYTHONHASHSEED;PYTHONDONTWRITEBYTECODE=$env:PYTHONDONTWRITEBYTECODE;PYTHONPATH=$env:PYTHONPATH;TMP=$env:TMP;TEMP=$env:TEMP;MPLCONFIGDIR=$env:MPLCONFIGDIR};
    historical_thread_environment = 'OPEN'; current_five_thread_variables = 'unset';
    native_calls_allowed = 1; observed_only_after_native_exact = $true; retry_allowed = $false
})
$taskClock = [Diagnostics.Stopwatch]::StartNew()
$taskProcess = Start-Process -FilePath $taskPython -ArgumentList $taskArguments -WorkingDirectory $taskRepo -WindowStyle Hidden -PassThru -RedirectStandardOutput "$taskOutput/controller-stdout.txt" -RedirectStandardError "$taskOutput/controller-stderr.txt"
[IO.File]::WriteAllText("$taskOutput/launcher.pid", ([string]$taskProcess.Id + "`n"), $taskUtf8)
Write-Output ("Diagnostic controller PID {0}; progress {1}/progress.jsonl" -f $taskProcess.Id,$taskOutput)
$taskTimedOut = $false
while (-not $taskProcess.HasExited) {
    if ($taskClock.Elapsed.TotalSeconds -ge 600) {
        $taskTimedOut = $true
        & taskkill.exe /PID $taskProcess.Id /T /F | Out-Null
        break
    }
    Start-Sleep -Milliseconds 500
    $taskProcess.Refresh()
}
$taskProcess.WaitForExit()
$taskExit = $taskProcess.ExitCode
$taskClock.Stop()
$taskFiles = @()
Get-ChildItem -LiteralPath $taskOutput -File -Recurse | Sort-Object FullName | ForEach-Object {
    $taskFiles += [ordered]@{path=$_.FullName.Substring($taskOutput.Length+1).Replace('\','/');bytes=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
}
$taskCheck = $null
if (Test-Path -LiteralPath "$taskOutput/check.json") { $taskCheck = Get-Content -LiteralPath "$taskOutput/check.json" -Raw | ConvertFrom-Json }
$taskVerdict = 'FAIL_STOP'
if (-not $taskTimedOut -and $taskExit -eq 0 -and $taskCheck.status -eq 'PASS_SINGLE_CASE_EXACT_DIAGNOSTIC') { $taskVerdict = 'PASS_SINGLE_CASE_EXACT_DIAGNOSTIC' }
Write-TaskNewJson "$taskOutput/launcher-closed.json" ([ordered]@{
    at = (Get-Date).ToString('o'); status = $taskVerdict; controller_pid = $taskProcess.Id;
    exit_code = $taskExit; elapsed_s = $taskClock.Elapsed.TotalSeconds; timed_out = $taskTimedOut;
    files = $taskFiles; manifest_excludes = @('launcher-closed.json');
    all_controller_streams_closed = $true; intermediates_eligible = $false;
    cohort_resume_authorized = $false; a_prime_authorized = $false; retained = 'All artifacts retained; no retry'
})
Write-Output ("Diagnostic {0}; wall {1:F3}s; closed manifest {2}/launcher-closed.json" -f $taskVerdict,$taskClock.Elapsed.TotalSeconds,$taskOutput)
if ($taskVerdict -ne 'PASS_SINGLE_CASE_EXACT_DIAGNOSTIC') { exit 1 }
