param([ValidateSet('seal','verify')][string]$Action='verify')
$ErrorActionPreference='Stop'
$taskRoot='D:/RCA-flashticket'
$taskBase=Join-Path $taskRoot 'results/T-065'
$utf8=New-Object Text.UTF8Encoding($false)
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLower()}
function WriteJson($path,$value){[IO.File]::WriteAllText($path,($value|ConvertTo-Json -Depth 100)+"`n",$utf8)}
if(Test-Path -LiteralPath D:/RCA-overnight/STOP){throw 'STOP local'}
if($Action -eq 'verify'){
  $m=Get-Content -Raw -Encoding UTF8 (Join-Path $taskBase 'manifest.json')|ConvertFrom-Json
  $bad=New-Object 'System.Collections.Generic.List[string]';$n=0
  foreach($e in $m.files.PSObject.Properties){$p=Join-Path $taskBase $e.Name;if(!(Test-Path -LiteralPath $p)){$bad.Add($e.Name)}elseif((Digest $p) -ne $e.Value.sha256 -or (Get-Item -LiteralPath $p).Length -ne $e.Value.bytes){$bad.Add($e.Name)};$n++}
  if((Digest (Join-Path $taskRoot $m.task_log.file)) -ne $m.task_log.sha256){$bad.Add('LOG')}
  if($bad.Count){throw ($bad -join ',')}
  Write-Output "VERIFIED: $n checksums and task LOG; status=$($m.status)"
  exit
}
$prior=Get-Content -Raw -Encoding UTF8 (Join-Path $taskBase 'codex/manifest-L8b-truoc.json')|ConvertFrom-Json
$reception=Get-Content -Raw -Encoding UTF8 (Join-Path $taskBase 'kiem/006-gc-cuoi/tiep-nhan.json')|ConvertFrom-Json
$control=Get-Content -Raw -Encoding UTF8 (Join-Path $taskBase 'kiem/006-gc-cuoi/doi-chieu-tep-dieu-phoi.json')|ConvertFrom-Json
$allowed=@('CHECKPOINT.md','XONG.md','thay-doi-may.md','prompt-ban-giao.md')
$files=[ordered]@{};$modified=New-Object 'System.Collections.Generic.List[string]'
foreach($e in $prior.files.PSObject.Properties){
  $p=Join-Path $taskBase $e.Name
  if(!(Test-Path -LiteralPath $p)){throw ('old file missing: '+$e.Name)}
  $v=@{sha256=Digest $p;bytes=(Get-Item -LiteralPath $p).Length}
  if($e.Name -eq 'codex/L8-trang-thai.json'){
    if($v.sha256 -ne $control.actual.sha256 -or $v.bytes -ne $control.actual.bytes){throw 'launcher L8 changed since recorded'}
    if((Digest (Join-Path $taskBase 'codex/L8-ket-qua-lich-su.json')) -ne $e.Value.sha256){throw 'historical L8 result not recovered exactly'}
    continue
  }
  $files[$e.Name]=$v
  if($v.sha256 -ne $e.Value.sha256 -or $v.bytes -ne $e.Value.bytes){$modified.Add($e.Name)}
}
foreach($p in $modified){if($p -notin $allowed){throw ('unexpected old file change: '+$p)}}
foreach($e in $reception.protected.PSObject.Properties){if((Digest (Join-Path $taskRoot $e.Name)) -ne $e.Value){throw ('protected changed: '+$e.Name)}}
foreach($pair in @(@('XONG.md','codex/XONG-L8b-truoc.md'),@('prompt-ban-giao.md','codex/prompt-ban-giao-L8b-truoc.md'))){if((Digest (Join-Path $taskBase $pair[1])) -ne $prior.files.($pair[0]).sha256){throw ('backup mismatch '+$pair[0])}}
$h=[Security.Cryptography.SHA256]::Create()
foreach($rel in @('CHECKPOINT.md','thay-doi-may.md')){
  $b=[IO.File]::ReadAllBytes((Join-Path $taskBase $rel));$v=$prior.files.$rel
  $hash=([BitConverter]::ToString($h.ComputeHash($b,0,[int]$v.bytes))).Replace('-','').ToLower()
  if($hash -ne $v.sha256){throw ('prefix changed: '+$rel)}
}
$logPath=Join-Path $taskRoot $prior.task_log.file
$log=[IO.File]::ReadAllBytes($logPath)
if(([BitConverter]::ToString($h.ComputeHash($log,0,[int]$prior.task_log.bytes))).Replace('-','').ToLower() -ne $prior.task_log.sha256){throw 'LOG prefix changed'}
$newPaths=@('codex/l8b-xuat.py','codex/l8b-kiem.py','codex/l8b-dong-goi.py','codex/l8b-local.ps1','codex/manifest-L8b-truoc.json','codex/l8b-payload-001.tgz','codex/l8b-ban-giao-001.tgz','codex/l8b-xuat-luot-001.txt','codex/l8b-kiem-xuat-luot-001.txt','codex/l8b-kiem-xuat-luot-002.txt','codex/l8b-deploy-luot-001.txt','codex/l8b-api-luot-001.txt','codex/l8b-api-luot-002.txt','codex/l8b-fix01-luot-001.txt','codex/l8b-lien-ket-live-luot-001.txt','codex/L8-ket-qua-lich-su.json','codex/L8b-ket-qua.json','codex/L8b-app-brief.md','codex/XONG-L8b-truoc.md','codex/prompt-ban-giao-L8b-truoc.md','README-L8b.md')
foreach($folder in @('nguon-l8b','may-l8b','grafana-l8b','kiem/006-gc-cuoi','dinh-dang/0.5')){foreach($p in Get-ChildItem -LiteralPath (Join-Path $taskBase $folder) -Recurse -File){$newPaths+=$p.FullName.Substring($taskBase.Length+1).Replace('\','/')}}
$reportRel='kiem/006-gc-cuoi/kiem-cuoi.json'
$new=New-Object 'System.Collections.Generic.List[string]'
foreach($rel in $newPaths|Sort-Object -Unique){
  if($rel -eq $reportRel){continue}
  $p=Join-Path $taskBase $rel
  if(!(Test-Path -LiteralPath $p)){throw ('new path missing: '+$rel)}
  if(!$files.Contains($rel)){$new.Add($rel)}
  $files[$rel]=@{sha256=Digest $p;bytes=(Get-Item -LiteralPath $p).Length}
}
$new.Add($reportRel)
$allChanges=@($modified)+@($new)+@('manifest.json','../../tasks/T-065-giao-dien-grafana/LOG.md')
WriteJson (Join-Path $taskBase $reportRel) @{utc=[DateTime]::UtcNow.ToString('o');status='dat_api_du_lieu_ui_chua_kiem';old_manifest_files=@($prior.files.PSObject.Properties).Count;old_results_preserved_except_allowed=$true;old_launcher_file_change='doi-chieu-tep-dieu-phoi.json';historical_L8_state_recovered_exactly='codex/L8-ket-qua-lich-su.json';modified_files=@($modified);new_files=@($new|Sort-Object -Unique);changed_file_set_relative_to_results_T065=$allChanges;log_append_only=$true;checkpoint_append_only=$true;machine_change_log_append_only=$true;protected_unchanged=$true;old_L8_history_preserved=$true;source_outputs=83;export_cases=84;API_pages=18;UI_new_dashboard='chua_kiem';no_research_decision_added=$true;scope='results/T-065 và nối LOG; hai dashboard mới và thư mục con mới trên exp-obs'}
$files[$reportRel]=@{sha256=Digest (Join-Path $taskBase $reportRel);bytes=(Get-Item -LiteralPath (Join-Path $taskBase $reportRel)).Length}
WriteJson (Join-Path $taskBase 'manifest.json') ([ordered]@{utc=[DateTime]::UtcNow.ToString('o');status='dat_api_du_lieu_ui_chua_kiem';status_scope='L8b';task_status='dat_mot_phan';prior_manifest='codex/manifest-L8b-truoc.json';prior_state_relocated=@{from='codex/L8-trang-thai.json';to='codex/L8-ket-qua-lich-su.json';sha256=$prior.files.'codex/L8-trang-thai.json'.sha256;reason='Bộ gọi ghi trạng thái tiến trình sau L8; giữ đúng byte kết quả cũ ở tên riêng'};excluded=@('manifest.json (self hash)','codex/L8-trang-thai.json và L8b-trang-thai.json: trạng thái tiến trình do bộ gọi ghi, kết quả ghim bằng tên ket-qua','Tệp điều phối và log CLI đang được bộ gọi ghi; danh mục kế thừa pin cũ và chỉ thêm đầu ra L8b được liệt kê');task_log=@{file=$prior.task_log.file;bytes=$log.Length;sha256=Digest $logPath};new_files=@($new|Sort-Object -Unique);modified_files=@($modified);files=$files})
Write-Output "SEALED: $($files.Count) files; old preserved; API/data passed; new UI unverified"
