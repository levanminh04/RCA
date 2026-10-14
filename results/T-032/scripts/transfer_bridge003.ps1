$ErrorActionPreference = 'Stop'
$repoRoot = 'D:/RCA-flashticket'
$keyPath = 'D:/RCA-ext/keys/key2.pem'
$hostTarget = 'ubuntu@3.26.62.217'
$remoteRoot = '/home/ubuntu/rca/T-032/'
$inventoryPath = "$repoRoot/results/T-032/runs/tiep-tuc-003/bridge003-transfer.json"
$inventory = Get-Content -LiteralPath $inventoryPath -Raw | ConvertFrom-Json
foreach ($entry in $inventory.files) {
    if ($entry.remote_path -notmatch '^[a-zA-Z0-9_./-]+$' -or $entry.remote_path.Contains('..')) { throw 'Unsafe path' }
    $sourcePath = Join-Path $repoRoot $entry.path
    if ((Get-FileHash -Algorithm SHA256 -LiteralPath $sourcePath).Hash.ToLower() -ne $entry.sha256) { throw 'Local hash changed' }
}
$scriptSources = @($inventory.files | Where-Object { $_.remote_path.StartsWith('scripts/') } | ForEach-Object { Join-Path $repoRoot $_.path })
& scp -i $keyPath -o BatchMode=yes -o StrictHostKeyChecking=yes @scriptSources "${hostTarget}:${remoteRoot}scripts/"
if ($LASTEXITCODE -ne 0) { throw 'Script transfer failed' }
$snapshot = @($inventory.files | Where-Object { $_.remote_path.StartsWith('repo/') })
if ($snapshot.Count -ne 1) { throw 'Snapshot cardinality' }
& scp -i $keyPath -o BatchMode=yes -o StrictHostKeyChecking=yes (Join-Path $repoRoot $snapshot[0].path) "${hostTarget}:$remoteRoot$($snapshot[0].remote_path)"
if ($LASTEXITCODE -ne 0) { throw 'Snapshot transfer failed' }
$paths = @($inventory.files | ForEach-Object { $remoteRoot + $_.remote_path })
$remoteLines = @(& ssh -i $keyPath -o BatchMode=yes -o StrictHostKeyChecking=yes $hostTarget ('sha256sum ' + ($paths -join ' ')))
if ($LASTEXITCODE -ne 0 -or $remoteLines.Count -ne $inventory.files.Count) { throw 'Remote hash command failed' }
$checks = for ($idx = 0; $idx -lt $remoteLines.Count; $idx++) {
    $parts = $remoteLines[$idx] -split '\s+', 2
    $entry = $inventory.files[$idx]
    if ($parts[0] -ne $entry.sha256 -or $parts[1] -ne $paths[$idx]) { throw 'Remote byte/path mismatch' }
    [ordered]@{ path=$entry.path; remote_path=$paths[$idx]; bytes=$entry.bytes; sha256=$parts[0]; passed=$true }
}
$receipt = [ordered]@{ status='PASS'; methods_executed=$false; inventory_sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $inventoryPath).Hash.ToLower(); files=@($checks); new_transferred_bytes=$inventory.new_bytes_to_transfer }
$outPath = "$repoRoot/results/T-032/runs/tiep-tuc-003/bridge003-transfer-check.json"
if (Test-Path -LiteralPath $outPath) { throw 'Receipt exists; no overwrite' }
[IO.File]::WriteAllText($outPath, ($receipt | ConvertTo-Json -Depth 8) + "`n", [Text.UTF8Encoding]::new($false))
$receipt | ConvertTo-Json -Depth 8
