param(
    [Parameter(Mandatory=$true)][string]$BudgetFile,
    [Parameter(Mandatory=$true)][string]$BudgetSha256,
    [Parameter(Mandatory=$true)][string]$ControllerSha256,
    [Parameter(Mandatory=$true)][string]$WrapperSha256,
    [Parameter(Mandatory=$true)][string]$LauncherSha256,
    [Parameter(Mandatory=$true)][string]$MigrationFile,
    [Parameter(Mandatory=$true)][string]$MigrationSha256,
    [Parameter(Mandatory=$true)][ValidatePattern('^[0-9]{3}$')][string]$SegmentId,
    [switch]$Resume,
    [Parameter(Mandatory=$true)][string]$ForecastFile,
    [Parameter(Mandatory=$true)][string]$ForecastSha256,
    [ValidateRange(1,50)][int]$MaxCasesThisSegment = 50,
    [switch]$StopAfterFirstRe2,
    [switch]$Accountant,
    [switch]$Supervisor,
    [string]$AccountingStartedUtc,
    [double]$PriorPackageWallS = -1
)
# The accountant owns the supervisor process handle until its streams and full
# cohort seal are closed. Its final receipt is outside the immutable cohort.
$taskClock = [Diagnostics.Stopwatch]::StartNew()
$taskEntryUtc = [DateTime]::UtcNow.ToString('o')
$ErrorActionPreference = 'Stop'
$taskRepo = 'D:/RCA-flashticket'
$taskBase = "$taskRepo/results/T-032"
$taskOutput = "$taskBase/runs/microrank-laptop-cohort-001"
$taskSegment = "$taskOutput/segments/$SegmentId"
$taskAccounting = "$taskBase/runs/microrank-laptop-cohort-001-accounting/$SegmentId"
$taskController = "$taskBase/scripts/batch_microrank_laptop_exact_v3.py"
$taskWrapper = "$taskBase/scripts/replay_microrank_laptop_exact_v2.py"
$taskPython = 'D:/RCA-ext/envs/T-014-main/Scripts/python.exe'
$taskThreads = @('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')
$taskUtf8 = New-Object System.Text.UTF8Encoding($false)
$taskOwnSegment = $false
$taskOwnAccounting = $false
$taskProcess = $null
$taskSupervisorProcess = $null
$taskTimedOut = $false

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
        if (($_.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw "Redirected artifact: $($_.FullName)" }
        $taskRelative = $_.FullName.Substring($TaskRoot.Length+1).Replace('\','/')
        if ($TaskExcluded -notcontains $taskRelative) {
            $taskRows += [ordered]@{path=$taskRelative;bytes=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
        }
    }
    return ,$taskRows
}
function Convert-TaskArgument([string]$TaskArgument) {
    if ($TaskArgument -notmatch '[\s"]' -and $TaskArgument.Length -gt 0) { return $TaskArgument }
    return '"' + ([regex]::Replace(([regex]::Replace($TaskArgument, '(\\*)"', '$1$1\"')), '(\\+)$', '$1$1')) + '"'
}
function Get-TaskIdentity($TaskProcess, [string]$TaskRole) {
    return [ordered]@{pid=$TaskProcess.Id;creation_time_utc=$TaskProcess.StartTime.ToUniversalTime().ToString('o');role=$TaskRole}
}
function Test-TaskIdentityAlive($TaskIdentity) {
    if ($null -eq $TaskIdentity) { return $false }
    $taskCandidate = Get-Process -Id $TaskIdentity.pid -ErrorAction SilentlyContinue
    if (-not $taskCandidate) { return $false }
    return ($taskCandidate.StartTime.ToUniversalTime().ToString('o') -eq $TaskIdentity.creation_time_utc)
}
function Stop-TaskIdentityTree($TaskIdentity) {
    if (Test-TaskIdentityAlive $TaskIdentity) { & taskkill.exe /PID $TaskIdentity.pid /T /F | Out-Null }
}
function Assert-TaskRemaining {
    $taskAlreadyElapsed = if ($AccountingStartedUtc) { ([DateTime]::UtcNow - [DateTime]::Parse($AccountingStartedUtc).ToUniversalTime()).TotalSeconds } else { $taskClock.Elapsed.TotalSeconds }
    if (($PriorPackageWallS + $taskAlreadyElapsed) -ge 18000.0) { throw 'Whole package wall exceeds Q-126 five-hour ceiling' }
}

function Get-TaskRecovery($TaskMigration) {
    if ($TaskMigration.schema -ne 'T032-MicroRank-laptop-controller-migration-v3') { throw 'Expected v3 migration' }
    Assert-TaskPin $TaskMigration.previous_migration_path $TaskMigration.previous_migration_sha256
    $taskPreviousMigration = Get-Content -LiteralPath $TaskMigration.previous_migration_path -Raw | ConvertFrom-Json
    if ($taskPreviousMigration.schema -ne 'T032-MicroRank-laptop-controller-migration-v2' -or $taskPreviousMigration.root_verified -ne $true -or $taskPreviousMigration.authority -ne 'Q-126') { throw 'Previous migration not verified v2' }
    Assert-TaskPin "$taskBase/scripts/batch_microrank_laptop_exact_v2.py" $taskPreviousMigration.controller_sha256
    Assert-TaskPin "$taskBase/scripts/start_microrank_laptop_cohort_002.ps1" $taskPreviousMigration.launcher_sha256
    Assert-TaskPin "$taskBase/scripts/replay_microrank_laptop_exact_v2.py" $TaskMigration.wrapper_sha256
    if ($TaskMigration.wrapper_sha256 -ne $taskPreviousMigration.wrapper_sha256 -or $TaskMigration.old_source_pin_sha256 -ne $taskPreviousMigration.old_source_pin_sha256 -or $TaskMigration.plan_sha256 -ne $taskPreviousMigration.plan_sha256) { throw 'Historical source or unchanged wrapper differs' }
    Assert-TaskPin "$taskOutput/source-pin-manifest.json" $TaskMigration.old_source_pin_sha256
    Assert-TaskPin "$taskOutput/plan-52.json" $TaskMigration.plan_sha256
    Assert-TaskPin "$taskOutput/segments/001/launcher-closed.json" $TaskMigration.initial_segment_closed_sha256
    $taskAdditional = [double]$TaskMigration.additional_tool_wall_s
    if ($null -eq $TaskMigration.additional_tool_wall_s -or [double]::IsNaN($taskAdditional) -or [double]::IsInfinity($taskAdditional) -or $taskAdditional -lt 0 -or [math]::Abs([double]$TaskMigration.tool_validation_wall_s-[double]$taskPreviousMigration.tool_validation_wall_s-$taskAdditional) -gt 0.000001) { throw 'Tool charge must retain old wall plus additional exactly once' }
    Assert-TaskPin $TaskMigration.tool_abort_recovery_path $TaskMigration.tool_abort_recovery_sha256
    $taskRecovery = Get-Content -LiteralPath $TaskMigration.tool_abort_recovery_path -Raw | ConvertFrom-Json
    if ($taskRecovery.status -ne 'ROOT_VERIFIED_TOOL_ABORT_BEFORE_NATIVE_OBSERVED' -or $taskRecovery.authority -ne 'Q-108/Q-126' -or $taskRecovery.segment_id -ne '002' -or $taskRecovery.partial_dataset -ne 'Nezha-OB' -or $taskRecovery.partial_opaque_id -ne 'dev-63c30faf34' -or $taskRecovery.root_closed_cases_verified -ne 13 -or $taskRecovery.root_process_identities_closed -ne $true -or $taskRecovery.methods_executed -ne $false -or $taskRecovery.retry_method -ne $false) { throw 'Only exact root-verified pre-native segment002 tool abort may continue' }
    $taskFailedSegment = "$taskOutput/segments/002"
    Assert-TaskPin "$taskFailedSegment/failure.json" $taskRecovery.failure_sha256
    Assert-TaskPin "$taskFailedSegment/terminal.json" $taskRecovery.terminal_sha256
    Assert-TaskPin "$taskFailedSegment/launcher-terminal.json" $taskRecovery.launcher_terminal_sha256
    Assert-TaskPin "$taskFailedSegment/launcher-closed.json" $taskRecovery.launcher_closed_sha256
    Assert-TaskPin $taskRecovery.table_path $taskRecovery.table_sha256
    Assert-TaskPin $taskRecovery.cohort_manifest_path $taskRecovery.cohort_manifest_sha256
    $taskFailure = Get-Content -LiteralPath "$taskFailedSegment/failure.json" -Raw | ConvertFrom-Json
    $taskTerminal = Get-Content -LiteralPath "$taskFailedSegment/terminal.json" -Raw | ConvertFrom-Json
    $taskFailedLauncher = Get-Content -LiteralPath "$taskFailedSegment/launcher-terminal.json" -Raw | ConvertFrom-Json
    if ($taskFailure.state.error_type -ne 'NoSuchProcess' -or $taskFailure.traceback -notmatch 'attach_child' -or $taskFailure.traceback -notmatch 'pid=57736' -or $taskTerminal.status -ne 'FAIL_STOP' -or $null -ne $taskTerminal.active -or $taskTerminal.all_children_closed -ne $true -or $taskFailedLauncher.status -ne 'FAIL_STOP' -or $taskFailedLauncher.exit_code -ne 1 -or $taskFailedLauncher.timed_out -ne $false -or $null -ne $taskFailedLauncher.error -or $taskFailedLauncher.all_controller_streams_closed -ne $true) { throw 'Different or unclosed failure cannot resume' }
    $taskFailedAccount = "$taskBase/runs/microrank-laptop-cohort-001-accounting/002/accounting-failure-closed.json"
    Assert-TaskPin $taskFailedAccount $taskRecovery.accounting_failure_closed_sha256
    $taskAccount = Get-Content -LiteralPath $taskFailedAccount -Raw | ConvertFrom-Json
    if ($taskAccount.status -ne 'FAIL_STOP' -or $taskAccount.segment_id -ne '002' -or $taskAccount.timed_out -ne $false -or $taskAccount.all_supervisor_streams_closed -ne $true -or $taskRecovery.closing_tail_reserve_s -ne 20 -or [math]::Abs([double]$taskRecovery.actual_accountant_elapsed_s-[double]$taskAccount.elapsed_s) -gt 0.000001 -or [math]::Abs([double]$taskRecovery.charged_elapsed_s-[double]$taskAccount.elapsed_s-20) -gt 0.000001) { throw 'Failed actual accountant charge/closure differs' }
    return $taskRecovery
}
function Assert-TaskPreparedOnly($TaskRecovery) {
    Assert-TaskPin "$taskOutput/manifest.json" $TaskRecovery.cohort_manifest_sha256
    Assert-TaskPin "$taskOutput/52-cases.json" $TaskRecovery.table_sha256
    $taskPartial = "$taskOutput/cases/$($TaskRecovery.partial_dataset)/$($TaskRecovery.partial_opaque_id)"
    $taskPartialFiles = Get-TaskInventory $taskPartial @()
    if ($taskPartialFiles.Count -ne 3 -or @($TaskRecovery.current_partial_case_files).Count -ne 3) { throw 'Partial case must contain only three source-only prepare files' }
    foreach ($taskFile in $taskPartialFiles) {
        if ($taskFile.path -notin @('prepare/check.json','prepare/prepare.json','prepare/progress.jsonl')) { throw 'Method or extra partial artifact; no recovery' }
        $taskExpected = @($TaskRecovery.current_partial_case_files | Where-Object path -EQ $taskFile.path)
        if ($taskExpected.Count -ne 1 -or $taskExpected[0].sha256 -ne $taskFile.sha256 -or $taskExpected[0].bytes -ne $taskFile.bytes) { throw 'Partial prepare full-set pin differs' }
    }
    Assert-TaskPin "$taskPartial/prepare/check.json" $TaskRecovery.prepare_check_sha256
    Assert-TaskPin "$taskPartial/prepare/prepare.json" $TaskRecovery.prepare_payload_sha256
    $taskPrepare = Get-Content -LiteralPath "$taskPartial/prepare/check.json" -Raw | ConvertFrom-Json
    if ($taskPrepare.status -ne 'PASS' -or $taskPrepare.passed -ne $true -or $taskPrepare.source_checks_passed -ne $true -or $taskPrepare.methods_executed -ne $false -or $taskPrepare.dataset -ne $TaskRecovery.partial_dataset -or $taskPrepare.opaque_id -ne $TaskRecovery.partial_opaque_id -or $taskPrepare.prepare_sha256 -ne $TaskRecovery.prepare_payload_sha256) { throw 'Prepare proof not source-only PASS' }
}

function Get-TaskPriorWall($TaskMigration) {
    $taskValidationWall = [double]$TaskMigration.tool_validation_wall_s
    if ($null -eq $TaskMigration.tool_validation_wall_s -or [double]::IsNaN($taskValidationWall) -or [double]::IsInfinity($taskValidationWall) -or $taskValidationWall -lt 0) { throw 'Missing/invalid measured tool-validation wall' }
    $taskPriorSum = $taskValidationWall
    $taskPriorRows = @([ordered]@{segment_id='tool-validation';charged_s=$taskValidationWall;basis='actual tool-only runtime/fixture/benchmark wall, charged once from pinned migration';accounting_path=$null})
    foreach ($taskPriorFile in (Get-ChildItem -LiteralPath "$taskOutput/segments" -File -Recurse -Filter 'launcher-terminal.json' | Sort-Object FullName)) {
        $taskPrior = Get-Content -LiteralPath $taskPriorFile.FullName -Raw | ConvertFrom-Json
        $taskPriorId = $taskPriorFile.Directory.Name
        if ($taskPriorId -eq '002' -and $taskPrior.status -eq 'FAIL_STOP') {
            $taskRecovery = Get-TaskRecovery $TaskMigration
            $taskPriorSum += [double]$taskRecovery.charged_elapsed_s
            $taskPriorRows += [ordered]@{segment_id='002';charged_s=[double]$taskRecovery.charged_elapsed_s;basis='root-verified actual failed accountant elapsed plus20s closing reserve, no method executed';accounting_path="$taskBase/runs/microrank-laptop-cohort-001-accounting/002/accounting-failure-closed.json"}
            continue
        }
        if ($taskPrior.status -notin @('STOP_CHECKPOINT_PILOT','STOP_CHECKPOINT_BETWEEN_CASES','PASS_FULL52_LAPTOP_EXACT')) { throw 'Prior failed or incomplete segment; no retry/resume' }
        $taskPriorAccountingPath = "$taskBase/runs/microrank-laptop-cohort-001-accounting/$taskPriorId/accounting-closed.json"
        if (Test-Path -LiteralPath $taskPriorAccountingPath) {
            $taskPriorAccounting = Get-Content -LiteralPath $taskPriorAccountingPath -Raw | ConvertFrom-Json
            if ($taskPriorAccounting.status -ne 'PASS_ACCOUNTING_CLOSED' -or $taskPriorAccounting.supervisor_exit_code -ne 0 -or $taskPriorAccounting.segment_id -ne $taskPriorId -or $taskPriorAccounting.elapsed_s -lt $taskPrior.elapsed_s -or $taskPriorAccounting.closing_tail_reserve_s -ne 20 -or [math]::Abs([double]$taskPriorAccounting.charged_elapsed_s - [double]$taskPriorAccounting.elapsed_s - 20) -gt 0.000001) { throw 'Prior lifetime accounting invalid' }
            Assert-TaskPin $taskPriorFile.FullName $taskPriorAccounting.launcher_terminal_sha256
            Assert-TaskPin "$taskOutput/segments/$taskPriorId/launcher-closed.json" $taskPriorAccounting.launcher_closed_sha256
            $taskCharge = [double]$taskPriorAccounting.charged_elapsed_s
            $taskBasis = 'measured accountant start through supervisor exit, final inventory and cached hashes, plus 20s conservative final-receipt closing reserve'
        } else {
            if ($taskPriorId -ne '001' -or $TaskMigration.historical_unmeasured_tail_reserve_s -ne 20) { throw 'Prior v2 segment lacks lifetime accounting; no resume' }
            $taskCharge = [double]$taskPrior.elapsed_s + [double]$TaskMigration.historical_unmeasured_tail_reserve_s
            $taskBasis = 'historical measured launcher wall plus 20s conservative unmeasured sealing-tail reserve'
        }
        if ([double]::IsNaN($taskCharge) -or [double]::IsInfinity($taskCharge) -or $taskCharge -lt 0) { throw 'Prior wall invalid' }
        $taskPriorSum += $taskCharge
        $taskPriorRows += [ordered]@{segment_id=$taskPriorId;charged_s=$taskCharge;basis=$taskBasis;accounting_path=$(if(Test-Path -LiteralPath $taskPriorAccountingPath){$taskPriorAccountingPath}else{$null})}
    }
    return [ordered]@{total_s=$taskPriorSum;segments=$taskPriorRows}
}

try {
    if (-not $Resume -or [int]$SegmentId -lt 3 -or ($Accountant -and $Supervisor)) { throw 'Version3 is a continuation only, on a fresh segment003 or later' }
    foreach ($taskName in $taskThreads) {
        if ([Environment]::GetEnvironmentVariable($taskName,'Process') -ne $null) { throw "Q-124 requires unset $taskName" }
    }
    Assert-TaskPin $PSCommandPath $LauncherSha256
    Assert-TaskPin $taskController $ControllerSha256
    Assert-TaskPin $taskWrapper $WrapperSha256
    foreach ($taskInputName in @('BudgetFile','ForecastFile','MigrationFile')) {
        $taskInputPath = [IO.Path]::GetFullPath((Get-Variable -Name $taskInputName -ValueOnly))
        if (-not $taskInputPath.StartsWith(([IO.Path]::GetFullPath($taskBase)+[IO.Path]::DirectorySeparatorChar),[StringComparison]::OrdinalIgnoreCase)) { throw 'Pinned receipt outside T-032' }
        Set-Variable -Name $taskInputName -Value $taskInputPath
        Assert-TaskPin $taskInputPath (Get-Variable -Name ($taskInputName.Replace('File','Sha256')) -ValueOnly)
    }
    $taskMigration = Get-Content -LiteralPath $MigrationFile -Raw | ConvertFrom-Json
    if ($taskMigration.authority -ne 'Q-126' -or $taskMigration.root_verified -ne $true -or $taskMigration.controller_sha256 -ne $ControllerSha256 -or $taskMigration.wrapper_sha256 -ne $WrapperSha256) { throw 'Migration source or authority differs' }
    $taskRecovery = Get-TaskRecovery $taskMigration
    if (Get-ChildItem -LiteralPath "$taskOutput/segments" -File -Recurse -Filter 'supervisor-failure.json') { throw 'Prior supervisor failure; no retry/resume' }
    $taskAccountingRoot = "$taskBase/runs/microrank-laptop-cohort-001-accounting"
    if ((Test-Path -LiteralPath $taskAccountingRoot) -and (Get-ChildItem -LiteralPath $taskAccountingRoot -File -Recurse -Filter 'accounting-failure-closed.json' | Where-Object { $_.Directory.Name -ne '002' })) { throw 'Prior accountant failure; no retry/resume' }
    $taskPriorWall = Get-TaskPriorWall $taskMigration
    if ($PriorPackageWallS -lt 0) { $PriorPackageWallS = [double]$taskPriorWall.total_s }
    if ([math]::Abs($PriorPackageWallS - [double]$taskPriorWall.total_s) -gt 0.000001) { throw 'Prior package lifetime sum changed' }
    Assert-TaskRemaining
    $taskShell = (Get-Process -Id $PID).Path
    $taskCommon = @('-NoProfile','-File',$PSCommandPath,'-Resume','-BudgetFile',$BudgetFile,'-BudgetSha256',$BudgetSha256,
        '-ControllerSha256',$ControllerSha256,'-WrapperSha256',$WrapperSha256,'-LauncherSha256',$LauncherSha256,
        '-MigrationFile',$MigrationFile,'-MigrationSha256',$MigrationSha256,'-SegmentId',$SegmentId,
        '-ForecastFile',$ForecastFile,'-ForecastSha256',$ForecastSha256,'-MaxCasesThisSegment',[string]$MaxCasesThisSegment,
        '-PriorPackageWallS',$PriorPackageWallS.ToString('R',[Globalization.CultureInfo]::InvariantCulture))
    if ($StopAfterFirstRe2) { $taskCommon += '-StopAfterFirstRe2' }
    if (-not $Accountant -and -not $Supervisor) {
        if ((Test-Path -LiteralPath $taskSegment) -or (Test-Path -LiteralPath $taskAccounting)) { throw 'Segment/accounting already exists; no overwrite/retry' }
        $taskAccountantArguments = $taskCommon + '-Accountant'
        $taskAccountantProcess = Start-Process -FilePath $taskShell -ArgumentList (($taskAccountantArguments | ForEach-Object { Convert-TaskArgument $_ }) -join ' ') -WorkingDirectory $taskRepo -WindowStyle Hidden -PassThru
        Write-Output ("Hidden accountant PID {0}; segment {1}; accounting {2}/accounting-closed.json; cohort {3}/status.json" -f $taskAccountantProcess.Id,$SegmentId,$taskAccounting,$taskOutput)
        return
    }
    if ($Accountant) {
        if ((Test-Path -LiteralPath $taskSegment) -or (Test-Path -LiteralPath $taskAccounting)) { throw 'Segment/accounting already exists; no overwrite/retry' }
        New-Item -ItemType Directory -Path $taskAccounting -ErrorAction Stop | Out-Null
        $taskOwnAccounting = $true
        $AccountingStartedUtc = $taskEntryUtc
        $taskAccountantIdentity = Get-TaskIdentity (Get-Process -Id $PID) 'hidden accountant retaining supervisor handle'
        $taskSupervisorArguments = $taskCommon + @('-Supervisor','-AccountingStartedUtc',$AccountingStartedUtc)
        $taskSupervisorProcess = Start-Process -FilePath $taskShell -ArgumentList (($taskSupervisorArguments | ForEach-Object { Convert-TaskArgument $_ }) -join ' ') -WorkingDirectory $taskRepo -WindowStyle Hidden -PassThru -RedirectStandardOutput "$taskAccounting/supervisor-stdout.txt" -RedirectStandardError "$taskAccounting/supervisor-stderr.txt"
        $taskSupervisorIdentity = Get-TaskIdentity $taskSupervisorProcess 'hidden supervisor, lifetime measured through exit'
        Write-TaskNewJson "$taskAccounting/launch.json" ([ordered]@{at_utc=$AccountingStartedUtc;segment_id=$SegmentId;
            accountant_identity=$taskAccountantIdentity;supervisor_identity=$taskSupervisorIdentity;prior_package_wall_s=$PriorPackageWallS;
            prior_charges=$taskPriorWall.segments;launcher_sha256=$LauncherSha256;argv=$taskSupervisorArguments;retained_process_handle=$true})
        while (-not $taskSupervisorProcess.HasExited) {
            if ($PriorPackageWallS + $taskClock.Elapsed.TotalSeconds -ge 18000.0) {
                $taskTimedOut = $true
                Stop-TaskIdentityTree $taskSupervisorIdentity
                break
            }
            Start-Sleep -Milliseconds 250
            $taskSupervisorProcess.Refresh()
        }
        $taskSupervisorProcess.WaitForExit()
        $taskSupervisorExit = $taskSupervisorProcess.ExitCode
        if ($taskTimedOut -or $taskSupervisorExit -ne 0 -or $PriorPackageWallS+$taskClock.Elapsed.TotalSeconds+20 -gt 18000.0) { throw 'Supervisor failed or whole-package five-hour ceiling exceeded; partial outputs retained' }
        $taskClosed = Get-Content -LiteralPath "$taskSegment/launcher-closed.json" -Raw | ConvertFrom-Json
        if ($taskClosed.status -notin @('STOP_CHECKPOINT_PILOT','STOP_CHECKPOINT_BETWEEN_CASES','PASS_FULL52_LAPTOP_EXACT') -or $taskClosed.all_controller_streams_closed -ne $true) { throw 'Supervisor did not produce a valid closed seal' }
        $taskAccountingFiles = Get-TaskInventory $taskAccounting @('accounting-closed.json')
        $taskAccountingTerminalSha = (Get-FileHash -LiteralPath "$taskSegment/launcher-terminal.json" -Algorithm SHA256).Hash.ToLowerInvariant()
        $taskAccountingClosedSha = (Get-FileHash -LiteralPath "$taskSegment/launcher-closed.json" -Algorithm SHA256).Hash.ToLowerInvariant()
        $taskAccountingCohortSha = (Get-FileHash -LiteralPath "$taskOutput/manifest.json" -Algorithm SHA256).Hash.ToLowerInvariant()
        $taskAccountedElapsed = $taskClock.Elapsed.TotalSeconds
        $taskAccountedCharge = $taskAccountedElapsed + 20.0
        if ($PriorPackageWallS + $taskAccountedCharge -gt 18000.0) { throw 'Whole package wall including conservative final closing reserve exceeds five hours' }
        Write-TaskNewJson "$taskAccounting/accounting-closed.json" ([ordered]@{schema='T032-MicroRank-laptop-lifetime-accounting-v3';status='PASS_ACCOUNTING_CLOSED';
            segment_id=$SegmentId;elapsed_s=$taskAccountedElapsed;charged_elapsed_s=$taskAccountedCharge;closing_tail_reserve_s=20;started_utc=$AccountingStartedUtc;ended_utc=[DateTime]::UtcNow.ToString('o');
            supervisor_exit_code=$taskSupervisorExit;supervisor_pid=$taskSupervisorIdentity.pid;supervisor_creation_time_utc=$taskSupervisorIdentity.creation_time_utc;
            accountant_pid=$taskAccountantIdentity.pid;accountant_creation_time_utc=$taskAccountantIdentity.creation_time_utc;
            launcher_terminal_sha256=$taskAccountingTerminalSha;launcher_closed_sha256=$taskAccountingClosedSha;cohort_manifest_sha256=$taskAccountingCohortSha;
            prior_package_wall_s=$PriorPackageWallS;cumulative_package_wall_s=$PriorPackageWallS+$taskAccountedCharge;
            measurement='accountant entry through supervisor WaitForExit, then accounting artifact inventory and cached hashes; includes startup, preflight, controller, all stream closure and complete cohort inventories and seals';
            closing_reserve_note='20s is conservative charge for final accounting receipt serialization/write, not measured time';
            final_receipt_write_tail_unmeasured=$true;all_supervisor_streams_closed=$true;artifact_manifest=$taskAccountingFiles;manifest_excludes=@('accounting-closed.json');
            no_automatic_resume=$true;a_prime_authorized=$false})
        return
    }

    if (-not $AccountingStartedUtc -or (Test-Path -LiteralPath $taskSegment)) { throw 'Supervisor requires accountant start and a new segment' }
    New-Item -ItemType Directory -Path $taskSegment -ErrorAction Stop | Out-Null
    $taskOwnSegment = $true
    $taskSupervisorIdentity = Get-TaskIdentity (Get-Process -Id $PID) 'supervisor'
    [IO.File]::WriteAllText("$taskSegment/supervisor.pid",([string]$PID+"`n"),$taskUtf8)
    $taskPriorStatus = Get-Content -LiteralPath "$taskOutput/status.json" -Raw | ConvertFrom-Json
    if ($taskPriorStatus.status -eq 'FAIL_STOP' -and $taskPriorStatus.segment_id -eq '002') { Assert-TaskPreparedOnly $taskRecovery }
    elseif ($taskPriorStatus.status -notin @('STOP_CHECKPOINT_PILOT','STOP_CHECKPOINT_BETWEEN_CASES')) { throw 'No clean checkpoint; no retry/resume' }
    if (-not (Get-ChildItem -LiteralPath "$taskOutput/segments" -Recurse -File -Filter 'first-re2-peak.json') -and -not $StopAfterFirstRe2) { throw 'First RE2 checkpoint must remain enabled' }
    $env:PYTHONHASHSEED = '0'
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONPATH = 'D:/RCA-ext/src/RCAEval;D:/RCA-ext/src/baro;D:/RCA-ext/work/T-014/CIRCA;D:/RCA-flashticket/src'
    $env:TMP = "$taskOutput/tmp"
    $env:TEMP = "$taskOutput/tmp"
    $env:MPLCONFIGDIR = "$taskOutput/cache/mpl"
    foreach ($taskDirectory in @("$taskOutput/tmp","$taskOutput/cache","$taskOutput/cache/mpl")) {
        if (-not (Test-Path -LiteralPath $taskDirectory)) { New-Item -ItemType Directory -Path $taskDirectory -ErrorAction Stop | Out-Null }
    }
    $taskArguments = @('-B','-W','ignore','-X','utf8',$taskController,'run','--resume','--budget-file',$BudgetFile,
        '--budget-sha256',$BudgetSha256,'--wrapper-sha256',$WrapperSha256,'--segment-id',$SegmentId,
        '--max-cases-this-segment',[string]$MaxCasesThisSegment,'--forecast-file',$ForecastFile,'--forecast-sha256',$ForecastSha256,
        '--migration-file',$MigrationFile,'--migration-sha256',$MigrationSha256,'--prior-package-wall-s',
        $PriorPackageWallS.ToString('R',[Globalization.CultureInfo]::InvariantCulture),'--supervisor-started-utc',$AccountingStartedUtc)
    if ($StopAfterFirstRe2) { $taskArguments += '--stop-after-first-re2' }
    Write-TaskNewJson "$taskSegment/launcher.json" ([ordered]@{at=[DateTime]::UtcNow.ToString('o');supervisor_pid=$PID;supervisor_identity=$taskSupervisorIdentity;
        executable=$taskPython;argv=$taskArguments;cwd=$taskRepo;launcher_sha256=$LauncherSha256;controller_sha256=$ControllerSha256;wrapper_sha256=$WrapperSha256;
        budget_file=$BudgetFile;budget_sha256=$BudgetSha256;migration_file=$MigrationFile;migration_sha256=$MigrationSha256;
        segment_id=$SegmentId;resume=$true;forecast_file=$ForecastFile;forecast_sha256=$ForecastSha256;
        max_package_wall_s=18000;max_package_new_bytes=2684354560;max_local_bytes=4294967296;max_total_bytes=12884901888;
        max_case_wall_s=600;max_case_new_bytes=157286400;ram_rule='stop only insufficient worker RAM or laptop RAM >=95%';
        hidden_supervisor_independent_of_codex=$true;depends_on_laptop=$true;current_five_thread_variables='unset';historical_thread_environment='OPEN';
        process_environment=[ordered]@{PYTHONHASHSEED=$env:PYTHONHASHSEED;PYTHONDONTWRITEBYTECODE=$env:PYTHONDONTWRITEBYTECODE;PYTHONPATH=$env:PYTHONPATH;TMP=$env:TMP;TEMP=$env:TEMP;MPLCONFIGDIR=$env:MPLCONFIGDIR};
        one_worker=$true;no_retry_no_skip_no_tolerance=$true;a_prime_authorized=$false;max_remainder_cases_this_segment=$MaxCasesThisSegment;
        stop_after_first_re2=[bool]$StopAfterFirstRe2;prior_package_wall_s=$PriorPackageWallS;accountant_started_utc=$AccountingStartedUtc;
        supervisor_remaining_package_watchdog_s=18000.0-$PriorPackageWallS;whole_lifetime_receipt="$taskAccounting/accounting-closed.json"})
    $taskLauncherError = $null
    $taskExit = -1
    $taskRedirectorIdentity = $null
    $taskControllerIdentity = $null
    try {
        Assert-TaskRemaining
        Assert-TaskPin $taskController $ControllerSha256
        Assert-TaskPin $taskWrapper $WrapperSha256
        $taskProcess = Start-Process -FilePath $taskPython -ArgumentList (($taskArguments | ForEach-Object { Convert-TaskArgument $_ }) -join ' ') -WorkingDirectory $taskRepo -WindowStyle Hidden -PassThru -RedirectStandardOutput "$taskSegment/controller-stdout.txt" -RedirectStandardError "$taskSegment/controller-stderr.txt"
        $taskRedirectorIdentity = Get-TaskIdentity $taskProcess 'venv launcher/redirector handle; actual controller records own identity'
        [IO.File]::WriteAllText("$taskSegment/launcher.pid",([string]$taskProcess.Id+"`n"),$taskUtf8)
        Write-TaskNewJson "$taskSegment/launcher-process.json" $taskRedirectorIdentity
        while (-not $taskProcess.HasExited) {
            if (-not $taskControllerIdentity -and (Test-Path -LiteralPath "$taskSegment/controller.pid")) {
                $taskActualPid = [int](Get-Content -LiteralPath "$taskSegment/controller.pid" -Raw).Trim()
                $taskActualProcess = Get-Process -Id $taskActualPid -ErrorAction SilentlyContinue
                if ($taskActualProcess) { $taskControllerIdentity = Get-TaskIdentity $taskActualProcess 'actual Python controller'; Write-TaskNewJson "$taskSegment/actual-controller-process.json" $taskControllerIdentity }
            }
            try { Assert-TaskRemaining } catch { $taskTimedOut=$true;Stop-TaskIdentityTree $taskRedirectorIdentity;break }
            Start-Sleep -Milliseconds 250
            $taskProcess.Refresh()
        }
        $taskProcess.WaitForExit()
        $taskExit = $taskProcess.ExitCode
        if ((Test-TaskIdentityAlive $taskRedirectorIdentity) -or (Test-TaskIdentityAlive $taskControllerIdentity)) { throw 'Controller/redirector identity still alive after stream wait' }
    } catch {
        $taskLauncherError = $_.Exception.ToString()
        Stop-TaskIdentityTree $taskRedirectorIdentity
        if ($taskProcess) { $taskProcess.WaitForExit() }
    }
    $taskTerminal = $null
    if (Test-Path -LiteralPath "$taskSegment/terminal.json") { $taskTerminal = Get-Content -LiteralPath "$taskSegment/terminal.json" -Raw | ConvertFrom-Json }
    $taskVerdict = 'FAIL_STOP'
    if (-not $taskTimedOut -and -not $taskLauncherError -and $taskExit -eq 0 -and $taskTerminal.all_children_closed -eq $true -and $taskTerminal.status -in @('STOP_CHECKPOINT_PILOT','STOP_CHECKPOINT_BETWEEN_CASES','PASS_FULL52_LAPTOP_EXACT')) { $taskVerdict=$taskTerminal.status }
    Write-TaskNewJson "$taskSegment/launcher-terminal.json" ([ordered]@{at=[DateTime]::UtcNow.ToString('o');status=$taskVerdict;
        supervisor_pid=$PID;supervisor_identity=$taskSupervisorIdentity;controller_pid=$(if($taskProcess){$taskProcess.Id}else{$null});
        redirector_identity=$taskRedirectorIdentity;actual_controller_identity=$taskControllerIdentity;exit_code=$taskExit;elapsed_s=$taskClock.Elapsed.TotalSeconds;
        timed_out=$taskTimedOut;error=$taskLauncherError;all_controller_streams_closed=$true;
        terminal_sha256=$(if($taskTerminal){(Get-FileHash -LiteralPath "$taskSegment/terminal.json" -Algorithm SHA256).Hash.ToLowerInvariant()}else{$null});
        accounting_note='elapsed_s here precedes final inventories; authoritative actual lifetime is outside-cohort accounting-closed.json after supervisor exit';
        no_automatic_resume=$true;a_prime_authorized=$false;retained='All artifacts and failed streams retained; no retry'})
    Assert-TaskRemaining
    $taskPreviousManifest = "$taskOutput/manifest.json"
    if (Test-Path -LiteralPath $taskPreviousManifest) { Copy-Item -LiteralPath $taskPreviousManifest -Destination "$taskSegment/prior-cohort-manifest.json" -ErrorAction Stop }
    $taskSegmentFiles = Get-TaskInventory $taskSegment @('launcher-closed.json')
    Assert-TaskRemaining
    Write-TaskNewJson "$taskSegment/launcher-closed.json" ([ordered]@{at=[DateTime]::UtcNow.ToString('o');status=$taskVerdict;files=$taskSegmentFiles;
        manifest_excludes=@('launcher-closed.json');all_controller_streams_closed=$true;no_automatic_resume=$true;a_prime_authorized=$false})
    $taskAllFiles = Get-TaskInventory $taskOutput @('manifest.json')
    Assert-TaskRemaining
    $taskManifestValue = [ordered]@{at=[DateTime]::UtcNow.ToString('o');status=$taskVerdict;segment_id=$SegmentId;files=$taskAllFiles;
        manifest_excludes=@('manifest.json');all_controller_streams_closed=$true;no_automatic_resume=$true;a_prime_authorized=$false;
        note='Full current index; prior cohort index copied into this immutable segment before any rewrite; actual whole-segment time is in outside-cohort accounting receipt'}
    $taskManifestTemp = "$taskOutput/manifest.json.tmp"
    if (Test-Path -LiteralPath $taskManifestTemp) { throw 'Unexpected retained manifest temp; no overwrite' }
    [IO.File]::WriteAllText($taskManifestTemp,(($taskManifestValue|ConvertTo-Json -Depth 60)+"`n"),$taskUtf8)
    Move-Item -LiteralPath $taskManifestTemp -Destination $taskPreviousManifest -Force -ErrorAction Stop
    Assert-TaskRemaining
    if ($taskVerdict -eq 'FAIL_STOP') { exit 1 }
} catch {
    $taskOuterError = $_.Exception.ToString()
    if ($taskSupervisorProcess) { Stop-TaskIdentityTree $taskSupervisorIdentity; $taskSupervisorProcess.WaitForExit() }
    if ($taskProcess) { Stop-TaskIdentityTree $taskRedirectorIdentity; $taskProcess.WaitForExit() }
    if ($Accountant -and $taskOwnAccounting) {
        $taskFailureFiles = Get-TaskInventory $taskAccounting @('accounting-failure-closed.json')
        Write-TaskNewJson "$taskAccounting/accounting-failure-closed.json" ([ordered]@{status='FAIL_STOP';segment_id=$SegmentId;error=$taskOuterError;
            elapsed_s=$taskClock.Elapsed.TotalSeconds;prior_package_wall_s=$PriorPackageWallS;timed_out=$taskTimedOut;
            all_supervisor_streams_closed=$true;artifact_manifest=$taskFailureFiles;manifest_excludes=@('accounting-failure-closed.json');
            no_automatic_resume=$true;retained='All partial cohort/accounting artifacts retained; no retry'})
        exit 1
    }
    if ($Supervisor -and $taskOwnSegment) {
        Write-TaskNewJson "$taskSegment/supervisor-failure.json" ([ordered]@{at=[DateTime]::UtcNow.ToString('o');status='FAIL_STOP';supervisor_pid=$PID;
            error=$taskOuterError;controller_streams_waited_closed=$true;no_automatic_resume=$true;retained='Partial outputs retained; inspect before further work'})
        $taskFailureFiles = Get-TaskInventory $taskSegment @('supervisor-failure-closed.json')
        Write-TaskNewJson "$taskSegment/supervisor-failure-closed.json" ([ordered]@{status='FAIL_STOP';files=$taskFailureFiles;manifest_excludes=@('supervisor-failure-closed.json');
            all_controller_streams_closed=$true;no_automatic_resume=$true;a_prime_authorized=$false})
        exit 1
    }
    throw
}
