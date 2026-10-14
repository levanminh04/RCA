$ErrorActionPreference = 'Stop'
$repoRoot = 'D:/RCA-flashticket'
$taskRoot = Join-Path $repoRoot 'results/T-032'
$targetRoot = Join-Path $taskRoot 'runs/microrank-cohort-failure-001'
$remoteRoot = '/home/ubuntu/rca/T-032/runs'
$stage = 'microrank-approved-cohort-001'
$sshIdentity = 'D:/RCA-ext/keys/key2.pem'
$hostAddress = 'ubuntu@3.26.62.217'
$groups = @(
    @{ Subdir = 'cohort'; Remote = "$remoteRoot/$stage"; Files = @('status.json', '52-cases.json', 'events.jsonl') },
    @{ Subdir = 'monitor'; Remote = "$remoteRoot/$stage-monitor"; Files = @('status.json', 'progress.jsonl', 'stdout.txt', 'stderr.txt', 'supervisor.pid', 'worker.pid') },
    @{ Subdir = 'failed-case'; Remote = "$remoteRoot/$stage/cases/RE2-TT/dev-3defe3d34b"; Files = @('check.json', 'roundoff-comparison.json', 'native-observed-exact.json', 'observer-integrity.json', 'guard-final.json', 'invocation.json') }
)
$rows = [System.Collections.Generic.List[object]]::new()
foreach ($group in $groups) {
    $localDir = Join-Path $targetRoot $group.Subdir
    New-Item -ItemType Directory -Force -Path $localDir | Out-Null
    $remoteFiles = @($group.Files | ForEach-Object { "$($group.Remote)/$_" })
    $hashBefore = @(& ssh -i $sshIdentity -o BatchMode=yes -o StrictHostKeyChecking=yes $hostAddress ('sha256sum ' + ($remoteFiles -join ' ')))
    if ($LASTEXITCODE -ne 0) { throw 'remote pre-transfer hash failed' }
    $scpArgs = @('-i', $sshIdentity, '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=yes')
    $scpArgs += @($remoteFiles | ForEach-Object { $hostAddress + ':' + $_ })
    $scpArgs += $localDir
    & scp @scpArgs
    if ($LASTEXITCODE -ne 0) { throw 'SCP failed; no receipt will be written' }
    $hashAfter = @(& ssh -i $sshIdentity -o BatchMode=yes -o StrictHostKeyChecking=yes $hostAddress ('sha256sum ' + ($remoteFiles -join ' ')))
    if ($LASTEXITCODE -ne 0) { throw 'remote post-transfer hash failed' }
    if (($hashBefore -join "`n") -cne ($hashAfter -join "`n")) { throw 'remote file changed during transfer' }
    foreach ($name in $group.Files) {
        $remotePath = "$($group.Remote)/$name"
        $matched = @($hashBefore | Where-Object { $_.EndsWith('  ' + $remotePath) })
        if ($matched.Count -ne 1) { throw 'missing/duplicate remote hash' }
        $expected = ($matched[0] -split '  ', 2)[0]
        $localPath = Join-Path $localDir $name
        $actual = (Get-FileHash -LiteralPath $localPath -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actual -cne $expected) { throw ('two-ended hash mismatch: ' + $name) }
        $rows.Add(@{ remote = $remotePath; local = $localPath; sha256 = $actual; bytes = (Get-Item -LiteralPath $localPath).Length; pass = $true })
    }
}
@{ status = 'PASS'; checked_at = [DateTimeOffset]::Now.ToString('o'); closed_stage = $stage; files = $rows; no_method_executed = $true } |
    ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $targetRoot 'transport-check.json') -Encoding utf8
Write-Output ('PASS: verified ' + $rows.Count + ' closed control/verdict files, two-ended SHA256; no method executed')
