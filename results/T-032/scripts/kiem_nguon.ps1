$ErrorActionPreference='Stop'
$root='D:/RCA-flashticket'
$run=Join-Path $root 'results/T-032/runs/chuan-bi-001'
$utf8=[Text.UTF8Encoding]::new($false)
$checked=[Collections.Generic.List[object]]::new()
$transfer=[Collections.Generic.HashSet[string]]::new()
function ReadJson([string]$rel) { Get-Content -LiteralPath (Join-Path $root $rel) -Raw | ConvertFrom-Json -Depth 100 }
function Check([string]$rel,[string]$expected,[string]$source,[bool]$ship=$true) {
 if ($rel -match '(^|/)(locked|T-033)(/|$)' -or $rel -match 'flash-ticket-rca-research') { throw 'Forbidden path' }
 $p=Join-Path $root $rel
 $actual=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash.ToLowerInvariant()
 $ok=$actual -eq $expected
 $checked.Add([ordered]@{path=$rel;expected=$expected;actual=$actual;pass=$ok;source=$source;bytes=(Get-Item -LiteralPath $p).Length})
 if (-not $ok) { throw "Hash mismatch: $rel" }
 if ($ship) { [void]$transfer.Add($rel) }
}
try {
 $m29='results/T-029/runs/compare-rca-preparation-001/manifest.json'
 $m=ReadJson $m29
 $ix24='results/T-024/ban-ghi-dua-vao-cham.json'
 Check $ix24 $m.source_hashes.$ix24 "$m29#/source_hashes"
 [void]$transfer.Add($m29)
 $i24=ReadJson $ix24
 foreach($r in $i24.records) {
  Check $r.path $r.sha256 "$ix24#/records"
  Check $r.source_config $r.source_config_sha256 "$ix24#/records/source_config"
 }
 Write-Output ('T024 record/config hashes PASS; records=' + $i24.records.Count)
 $mh='results/T-026/runs/session-005/handoff-manifest.json'
 $h=ReadJson $mh
 [void]$transfer.Add($mh)
 $ix26='results/T-026/ban-ghi-dua-vao-cham.json'
 Check $ix26 $h.files.$ix26.sha256 "$mh#/files"
 $i26=ReadJson $ix26
 foreach($r in $i26.unique_records) { Check $r.path $r.sha256 "$ix26#/unique_records" }
 foreach($p in $i26.source_hashes.PSObject.Properties) {
  if ($p.Name -match '^src/' -or $p.Name -in @('results/T-026/allowlist-dev.json','results/T-026/mappings/ob.json','results/T-026/config/adapter-config.json','results/T-026/runs/full-001/source-integrity-final.json','results/T-026/runs/session-005/external-code-manifest.json','results/T-026/runs/full-001/plan.json','results/T-022/giao-thuc-v2.md')) {
   Check $p.Name $p.Value "$ix26#/source_hashes"
  }
 }
 Write-Output ('T026 record/code/input hashes PASS; records=' + $i26.unique_records.Count)
 $m28='results/T-028/runs/phan-hoi-review-001/manifest.json'
 [void]$transfer.Add($m28)
 $m=ReadJson $m28
 foreach($r in $m.outputs) {
  if ($r.path -match '/(ca-sai|summary-tables|features-no-label-index|BARO-root-data|within-cell|schema-audit|grouped|mechanism).*\.json$') { Check $r.path $r.sha256 "$m28#/outputs" }
 }
 $fi='results/T-028/runs/phan-hoi-review-001/features-no-label-index.json'
 $idx=ReadJson $fi
 foreach($ds in $idx.cases.PSObject.Properties) {
  foreach($r in $ds.Value.PSObject.Properties) { Check $r.Value.path $r.Value.sha256 "$fi#/cases" }
 }
 Write-Output 'T028 selected outputs and all feature hashes PASS'
 $allow='results/T-026/allowlist-dev.json'
 $al=ReadJson $allow
 $raw=@{}
 foreach($c in $al.cases) {
  foreach($p in $c.files.PSObject.Properties) {
   if ($raw.ContainsKey($p.Name) -and $raw[$p.Name].sha256 -ne $p.Value.sha256) { throw 'Allowlist hash conflict' }
   $raw[$p.Name]=$p.Value
  }
 }
 foreach($rel in ($raw.Keys | Sort-Object)) { Check $rel $raw[$rel].sha256 "$allow#/cases/files" $false }
 $rawRows=@($raw.Keys | Sort-Object | ForEach-Object { $raw[$_] })
 [IO.File]::WriteAllText((Join-Path $run 'nezha-transfer-manifest.json'),(ConvertTo-Json -Depth 20 -InputObject ([ordered]@{allowlist=$allow;files=$rawRows;total_bytes=($rawRows | Measure-Object -Property bytes -Sum).Sum})),$utf8)
 Write-Output ('Nezha allowlist raw hashes PASS; files=' + $raw.Count)
 # Source p3 environment and RE2 allowlist/config are located by the frozen runner source.
 foreach($p in @('results/T-031/moi-truong.json','results/T-022/allowlist-dev.json','results/T-022/cau-hinh/p3-re2tt-v2.json')) {
  if(Test-Path -LiteralPath (Join-Path $root $p)) { [void]$transfer.Add($p) }
 }
 [IO.File]::WriteAllLines((Join-Path $run 'metadata-file-list.txt'),[string[]]@($transfer | Sort-Object),$utf8)
 $status='PASS'
} catch {
 $status='FAIL'; $errorText=$_.ToString(); Write-Output $errorText
} finally {
 $result=[ordered]@{status=$status;error=$errorText;checked_at=(Get-Date -Format o);checks=@($checked.ToArray());metadata_files=@($transfer | Sort-Object)}
 [IO.File]::WriteAllText((Join-Path $run 'source-checks.json'),(ConvertTo-Json -InputObject $result -Depth 30),$utf8)
 [IO.File]::AppendAllText((Join-Path $root 'tasks/T-032-g2-nguyen-nhan-xep-hang/LOG.md'),"`n- $(Get-Date -Format HH:mm) — kiểm hash nguồn $status; chi tiết results/T-032/runs/chuan-bi-001/source-checks.json. $errorText`n",$utf8)
}
if($status -ne 'PASS') { exit 1 }
