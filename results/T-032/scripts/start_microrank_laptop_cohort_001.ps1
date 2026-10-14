param(
    [Parameter(Mandatory=$true)][string]$BudgetFile,
    [Parameter(Mandatory=$true)][string]$BudgetSha256,
    [Parameter(Mandatory=$true)][string]$ControllerSha256,
    [Parameter(Mandatory=$true)][string]$WrapperSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9]{3}$')][string]$SegmentId,
    [switch]$Resume,
    [string]$ForecastFile,
    [string]$ForecastSha256,
    [ValidateRange(1,50)][int]$MaxCasesThisSegment = 50,
    [switch]$Supervisor
)
$ErrorActionPreference = 'Stop'
$taskRepo = 'D:/RCA-flashticket'
$taskBase = "$taskRepo/results/T-032"
$taskOutput = "$taskBase/runs/microrank-laptop-cohort-001"
$taskSegment = "$taskOutput/segments/$SegmentId"
$taskController = "$taskBase/scripts/batch_microrank_laptop_exact_v1.py"
$taskWrapper = "$taskBase/scripts/replay_microrank_laptop_exact_v1.py"
$taskPython = 'D:/RCA-ext/envs/T-014-main/Scripts/python.exe'
$taskThreads = @('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')
$taskUtf8 = New-Object System.Text.UTF8Encoding($false)

function Assert-TaskPin([string]$TaskPath, [string]$TaskHash) {
    if ($TaskHash -notmatch '^[0-9a-f]{64}$') { throw 'Missing or invalid reviewed hash; no launch' }
    if ((Get-FileHash -LiteralPath $TaskPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $TaskHash) { throw "Reviewed pin differs: $TaskPath" }
}
function Write-TaskNewJson([string]$TaskPath, $TaskValue) {
    if (Test-Path -LiteralPath $TaskPath) { throw "Refuse overwrite: $TaskPath" }
    [IO.File]::WriteAllText($TaskPath, (($TaskValue | ConvertTo-Json -Depth 60) + "`n"), $taskUtf8)
}
function Get-TaskInventory([string]$TaskRoot, [string[]]$TaskExcluded) {
    $taskRows = @()
    Get-ChildItem -LiteralPath $TaskRoot -File -Recurse | Sort-Object FullName | ForEach-Object {
        $taskRelative = $_.FullName.Substring($TaskRoot.Length+1).Replace('\','/')
        if ($TaskExcluded -notcontains $taskRelative) {
            $taskRows += [ordered]@{path=$taskRelative;bytes=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
        }
    }
    return ,$taskRows
}
function Convert-TaskArgument([string]$TaskArgument) {
    # Start-Process joins ArgumentList; quote using Windows argv rules rather
    # than shell syntax, including paths with spaces and trailing backslashes.
    if ($TaskArgument -notmatch '[\s"]' -and $TaskArgument.Length -gt 0) { return $TaskArgument }
    return '"' + ([regex]::Replace(([regex]::Replace($TaskArgument, '(\\*)"', '$1$1\"')), '(\\+)$', '$1$1')) + '"'
}

$taskOwnSegment = $false
$taskPackageRemainingS = 10800.0
$taskSupervisorClock = [Diagnostics.Stopwatch]::StartNew()
try {

foreach ($taskName in $taskThreads) {
    if ([Environment]::GetEnvironmentVariable($taskName, 'Process') -ne $null) { throw "Q-124 requires unset $taskName" }
}
Assert-TaskPin $taskController $ControllerSha256
Assert-TaskPin $taskWrapper $WrapperSha256
$taskBudgetPath = [IO.Path]::GetFullPath($BudgetFile)
if (-not $taskBudgetPath.StartsWith(([IO.Path]::GetFullPath($taskBase) + [IO.Path]::DirectorySeparatorChar), [StringComparison]::OrdinalIgnoreCase)) { throw 'Budget receipt outside T-032' }
Assert-TaskPin $taskBudgetPath $BudgetSha256
if ($Resume) {
    if (-not $ForecastFile -or -not $ForecastSha256) { throw 'Root forecast pin required before resume' }
    $ForecastFile = [IO.Path]::GetFullPath($ForecastFile)
    if (-not $ForecastFile.StartsWith(([IO.Path]::GetFullPath($taskBase) + [IO.Path]::DirectorySeparatorChar), [StringComparison]::OrdinalIgnoreCase)) { throw 'Forecast receipt outside T-032' }
    Assert-TaskPin $ForecastFile $ForecastSha256
    if (Get-ChildItem -LiteralPath "$taskOutput/segments" -File -Recurse -Filter 'supervisor-failure.json' -ErrorAction Stop) { throw 'An appended supervisor failure blocks the whole branch; no resume' }
    foreach ($taskPriorLauncherFile in (Get-ChildItem -LiteralPath "$taskOutput/segments" -File -Recurse -Filter 'launcher-terminal.json' -ErrorAction Stop)) {
        $taskPriorLauncher = Get-Content -LiteralPath $taskPriorLauncherFile.FullName -Raw | ConvertFrom-Json
        if ($taskPriorLauncher.status -eq 'FAIL_STOP') { throw 'A failed launcher segment blocks the whole branch; no retry/resume' }
    }
} elseif ($ForecastFile -or $ForecastSha256) { throw 'First segment must stop at pilot checkpoint' }

if (-not $Supervisor) {
    # The hidden supervisor, not this Codex/terminal invocation, owns the
    # controller watchdog and final stream closure. No visible app window.
    if (Test-Path -LiteralPath $taskSegment) { throw 'Segment already exists; no overwrite/retry' }
    $taskShell = (Get-Process -Id $PID).Path
    $taskSupervisorArguments = @('-NoProfile','-File',$PSCommandPath,'-Supervisor','-BudgetFile',$taskBudgetPath,
        '-BudgetSha256',$BudgetSha256,'-ControllerSha256',$ControllerSha256,'-WrapperSha256',$WrapperSha256,'-SegmentId',$SegmentId,
        '-MaxCasesThisSegment',[string]$MaxCasesThisSegment)
    if ($Resume) { $taskSupervisorArguments += @('-Resume','-ForecastFile',$ForecastFile,'-ForecastSha256',$ForecastSha256) }
    $taskSupervisorProcess = Start-Process -FilePath $taskShell -ArgumentList (($taskSupervisorArguments | ForEach-Object { Convert-TaskArgument $_ }) -join ' ') -WorkingDirectory $taskRepo -WindowStyle Hidden -PassThru
    Write-Output ("Cohort supervisor PID {0}; segment {1}; progress {2}/progress.jsonl. Laptop must remain on." -f $taskSupervisorProcess.Id,$SegmentId,$taskOutput)
    return
}

if (Test-Path -LiteralPath $taskSegment) { throw 'Segment already exists; no overwrite/retry' }
if (-not (Test-Path -LiteralPath "$taskOutput/segments")) { New-Item -ItemType Directory -Path "$taskOutput/segments" -ErrorAction Stop | Out-Null }
New-Item -ItemType Directory -Path $taskSegment -ErrorAction Stop | Out-Null
$taskOwnSegment = $true
[IO.File]::WriteAllText("$taskSegment/supervisor.pid", ([string]$PID + "`n"), $taskUtf8)
if ($Resume) {
    $taskPriorStatus = Get-Content -LiteralPath "$taskOutput/status.json" -Raw | ConvertFrom-Json
    if ($taskPriorStatus.status -notin @('STOP_CHECKPOINT_PILOT','STOP_CHECKPOINT_BETWEEN_CASES') -or $taskPriorStatus.segment_id -notmatch '^[0-9]{3}$') { throw 'No clean prior segment; no resume' }
    $taskPriorTerminal = Get-Content -LiteralPath "$taskOutput/segments/$($taskPriorStatus.segment_id)/terminal.json" -Raw | ConvertFrom-Json
    if ($taskPriorTerminal.status -ne $taskPriorStatus.status -or $null -eq $taskPriorTerminal.guard.wall_used_s -or $taskPriorTerminal.guard.wall_used_s -lt 0 -or $taskPriorTerminal.guard.wall_used_s -ge 10800) { throw 'Prior cumulative package wall invalid' }
    $taskPackageRemainingS -= [double]$taskPriorTerminal.guard.wall_used_s
}
$env:PYTHONHASHSEED = '0'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONPATH = 'D:/RCA-ext/src/RCAEval;D:/RCA-ext/src/baro;D:/RCA-ext/work/T-014/CIRCA;D:/RCA-flashticket/src'
$env:TMP = "$taskOutput/tmp"
$env:TEMP = "$taskOutput/tmp"
$env:MPLCONFIGDIR = "$taskOutput/cache/mpl"
foreach ($taskDirectory in @("$taskOutput/tmp", "$taskOutput/cache", "$taskOutput/cache/mpl")) {
    if (-not (Test-Path -LiteralPath $taskDirectory)) { New-Item -ItemType Directory -Path $taskDirectory -ErrorAction Stop | Out-Null }
}
$taskArguments = @('-B','-W','ignore','-X','utf8',$taskController,'run','--budget-file',$taskBudgetPath,
    '--budget-sha256',$BudgetSha256,'--wrapper-sha256',$WrapperSha256,'--segment-id',$SegmentId,
    '--max-cases-this-segment',[string]$MaxCasesThisSegment)
if ($Resume) { $taskArguments += @('--resume','--forecast-file',$ForecastFile,'--forecast-sha256',$ForecastSha256) }
Write-TaskNewJson "$taskSegment/launcher.json" ([ordered]@{
    at=(Get-Date).ToString('o'); supervisor_pid=$PID; executable=$taskPython; argv=$taskArguments; cwd=$taskRepo;
    launcher_sha256=(Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant();
    controller_sha256=$ControllerSha256; wrapper_sha256=$WrapperSha256; budget_file=$taskBudgetPath; budget_sha256=$BudgetSha256;
    segment_id=$SegmentId; resume=[bool]$Resume; forecast_file=$ForecastFile; forecast_sha256=$ForecastSha256;
    max_package_wall_s=10800; max_package_new_bytes=2684354560; max_local_bytes=4294967296; max_total_bytes=12884901888;
    max_case_wall_s=600; max_case_new_bytes=157286400; min_available_ram=4554752000; max_worker_tree_rss=4286316544;
    hidden_supervisor_independent_of_codex=$true; depends_on_laptop=$true; current_five_thread_variables='unset'; historical_thread_environment='OPEN';
    process_environment=[ordered]@{PYTHONHASHSEED=$env:PYTHONHASHSEED;PYTHONDONTWRITEBYTECODE=$env:PYTHONDONTWRITEBYTECODE;PYTHONPATH=$env:PYTHONPATH;TMP=$env:TMP;TEMP=$env:TEMP;MPLCONFIGDIR=$env:MPLCONFIGDIR};
    first_segment_stops_after_pilot=$true; one_worker=$true; no_retry_no_skip_no_tolerance=$true; a_prime_authorized=$false
    max_remainder_cases_this_segment=$MaxCasesThisSegment
    supervisor_remaining_package_watchdog_s=$taskPackageRemainingS
})
$taskClock = $taskSupervisorClock
$taskProcess = $null
$taskTimedOut = $false
$taskExit = -1
$taskLauncherError = $null
try {
    Assert-TaskPin $taskController $ControllerSha256
    Assert-TaskPin $taskWrapper $WrapperSha256
    $taskProcess = Start-Process -FilePath $taskPython -ArgumentList (($taskArguments | ForEach-Object { Convert-TaskArgument $_ }) -join ' ') -WorkingDirectory $taskRepo -WindowStyle Hidden -PassThru -RedirectStandardOutput "$taskSegment/controller-stdout.txt" -RedirectStandardError "$taskSegment/controller-stderr.txt"
    [IO.File]::WriteAllText("$taskSegment/launcher.pid", ([string]$taskProcess.Id + "`n"), $taskUtf8)
    while (-not $taskProcess.HasExited) {
        if ($taskClock.Elapsed.TotalSeconds -ge $taskPackageRemainingS) {
            $taskTimedOut = $true
            & taskkill.exe /PID $taskProcess.Id /T /F | Out-Null
            break
        }
        Start-Sleep -Milliseconds 500
        $taskProcess.Refresh()
    }
    $taskProcess.WaitForExit()
    $taskExit = $taskProcess.ExitCode
} catch {
    $taskLauncherError = $_.Exception.ToString()
    if ($taskProcess -and -not $taskProcess.HasExited) { & taskkill.exe /PID $taskProcess.Id /T /F | Out-Null; $taskProcess.WaitForExit() }
} finally {
    $taskClock.Stop()
}
# WaitForExit closes controller streams before any final hash. Case children
# are checked by the controller and are also included in this full inventory.
$taskTerminal = $null
if (Test-Path -LiteralPath "$taskSegment/terminal.json") { $taskTerminal = Get-Content -LiteralPath "$taskSegment/terminal.json" -Raw | ConvertFrom-Json }
$taskVerdict = 'FAIL_STOP'
if (-not $taskTimedOut -and -not $taskLauncherError -and $taskExit -eq 0 -and $taskTerminal.all_children_closed -eq $true -and $taskTerminal.status -in @('STOP_CHECKPOINT_PILOT','STOP_CHECKPOINT_BETWEEN_CASES','PASS_FULL52_LAPTOP_EXACT')) { $taskVerdict = $taskTerminal.status }
Write-TaskNewJson "$taskSegment/launcher-terminal.json" ([ordered]@{
    at=(Get-Date).ToString('o'); status=$taskVerdict; supervisor_pid=$PID; controller_pid=$(if($taskProcess){$taskProcess.Id}else{$null});
    exit_code=$taskExit; elapsed_s=$taskClock.Elapsed.TotalSeconds; timed_out=$taskTimedOut; error=$taskLauncherError;
    all_controller_streams_closed=$true; terminal_sha256=$(if(Test-Path -LiteralPath "$taskSegment/terminal.json"){(Get-FileHash -LiteralPath "$taskSegment/terminal.json" -Algorithm SHA256).Hash.ToLowerInvariant()}else{$null});
    no_automatic_resume=$true; a_prime_authorized=$false; retained='All artifacts and failed streams retained; no retry'
})
# Preserve the previous cohort index before sealing this segment: every file
# written here, including this copy, must be present in the closed inventory.
$taskPreviousManifest = "$taskOutput/manifest.json"
if (Test-Path -LiteralPath $taskPreviousManifest) {
    if (Test-Path -LiteralPath "$taskSegment/prior-cohort-manifest.json") { throw 'Prior manifest copy already exists' }
    Copy-Item -LiteralPath $taskPreviousManifest -Destination "$taskSegment/prior-cohort-manifest.json" -ErrorAction Stop
}
$taskSegmentFiles = Get-TaskInventory $taskSegment @('launcher-closed.json')
Write-TaskNewJson "$taskSegment/launcher-closed.json" ([ordered]@{
    at=(Get-Date).ToString('o'); status=$taskVerdict; files=$taskSegmentFiles; manifest_excludes=@('launcher-closed.json');
    all_controller_streams_closed=$true; no_automatic_resume=$true; a_prime_authorized=$false
})
$taskAllFiles = Get-TaskInventory $taskOutput @('manifest.json')
$taskManifestValue = [ordered]@{at=(Get-Date).ToString('o');status=$taskVerdict;segment_id=$SegmentId;files=$taskAllFiles;
    manifest_excludes=@('manifest.json');all_controller_streams_closed=$true;no_automatic_resume=$true;a_prime_authorized=$false;
    note='Current full cohort index; immutable case and segment manifests preserve prior outputs. Root verifies before research use.'}
$taskManifestTemp = "$taskOutput/manifest.json.tmp"
if (Test-Path -LiteralPath $taskManifestTemp) { throw 'Unexpected manifest temp retained; no overwrite' }
[IO.File]::WriteAllText($taskManifestTemp, (($taskManifestValue | ConvertTo-Json -Depth 60) + "`n"), $taskUtf8)
Move-Item -LiteralPath $taskManifestTemp -Destination $taskPreviousManifest -Force -ErrorAction Stop
if ($taskVerdict -eq 'FAIL_STOP') { exit 1 }
} catch {
    $taskOuterError = $_.Exception.ToString()
    # A foreground preflight error is returned to the caller. Hidden failures
    # get a fresh segment receipt when safe; no existing segment is overwritten.
    if ($Supervisor -and -not $taskOwnSegment -and -not (Test-Path -LiteralPath $taskSegment)) {
        if (-not (Test-Path -LiteralPath "$taskOutput/segments")) { New-Item -ItemType Directory -Path "$taskOutput/segments" -ErrorAction Stop | Out-Null }
        New-Item -ItemType Directory -Path $taskSegment -ErrorAction Stop | Out-Null
        $taskOwnSegment = $true
    }
    if ($Supervisor -and $taskOwnSegment) {
        if ($taskProcess -and -not $taskProcess.HasExited) {
            & taskkill.exe /PID $taskProcess.Id /T /F | Out-Null
            $taskProcess.WaitForExit()
        }
        Write-TaskNewJson "$taskSegment/supervisor-failure.json" ([ordered]@{
            at=(Get-Date).ToString('o');status='FAIL_STOP';supervisor_pid=$PID;error=$taskOuterError;
            controller_streams_waited_closed=$true;no_automatic_resume=$true;retained='Partial outputs retained; inspect before further work'
        })
        # This final failure receipt remains separate if a prior seal was
        # produced before a later inventory/index error. It does not rewrite it.
        $taskFailureFiles = Get-TaskInventory $taskSegment @('supervisor-failure-closed.json')
        Write-TaskNewJson "$taskSegment/supervisor-failure-closed.json" ([ordered]@{
            status='FAIL_STOP';files=$taskFailureFiles;manifest_excludes=@('supervisor-failure-closed.json');
            all_controller_streams_closed=$true;no_automatic_resume=$true;a_prime_authorized=$false
        })
        exit 1
    }
    throw
}
