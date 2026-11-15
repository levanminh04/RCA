param([ValidateSet('init','seal','verify')][string]$Action='init')
$ErrorActionPreference='Stop'
$taskRoot='D:/RCA-flashticket'
$taskBase=Join-Path $taskRoot 'results/T-065'
$utf8=New-Object System.Text.UTF8Encoding($false)
function WriteJson($path,$value){[IO.File]::WriteAllText($path,($value|ConvertTo-Json -Depth 100)+"`n",$utf8)}
function Digest($path){(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLower()}
if(Test-Path -LiteralPath D:/RCA-overnight/STOP){throw 'STOP local'}
if($Action -eq 'init'){
  $prior=Join-Path $taskBase 'codex/manifest-L8-truoc.json'
  if(Test-Path -LiteralPath $prior){throw 'L8 already initialized'}
  $m=Get-Content -Raw -Encoding UTF8 (Join-Path $taskBase 'manifest.json')|ConvertFrom-Json
  $bad=New-Object 'System.Collections.Generic.List[string]'
  $n=0
  foreach($e in $m.files.PSObject.Properties){
    $p=Join-Path $taskBase $e.Name
    if(!(Test-Path -LiteralPath $p)){$bad.Add($e.Name)}elseif((Digest $p) -ne $e.Value.sha256 -or (Get-Item -LiteralPath $p).Length -ne $e.Value.bytes){$bad.Add($e.Name)}
    $n++
  }
  if((Digest (Join-Path $taskRoot $m.task_log.file)) -ne $m.task_log.sha256){$bad.Add('LOG.md')}
  if($bad.Count){throw ($bad -join ', ')}
  $iPath=Join-Path $taskRoot 'results/T-064/ban-xuat/chi-muc-ban.json'
  if((Digest $iPath) -ne '7e893ec237ce55c04bdea13d8981670e9e8f3e19e848959e1067d6d6bac9b6e6'){throw 'index hash mismatch'}
  $index=Get-Content -Raw -Encoding UTF8 $iPath|ConvertFrom-Json
  $proof=New-Object System.Collections.Generic.List[object]
  foreach($b in $index.ban){foreach($c in $b.cac_ca){if($c.dau_ra){$p=Join-Path $taskRoot $c.dau_ra;if((Digest $p) -ne $c.sha256){throw "source mismatch $p"};$proof.Add(@{ban=$b.ban;ca=$c.ca;file=$c.dau_ra;sha256=$c.sha256;bytes=(Get-Item -LiteralPath $p).Length})}}}
  $out=Join-Path $taskBase 'kiem/005-gc-cuoi'
  [IO.Directory]::CreateDirectory($out)|Out-Null
  Copy-Item -LiteralPath (Join-Path $taskBase 'manifest.json') -Destination $prior
  $protected=@{}
  $paths=@('AGENTS.md','docs/STATE.md','docs/DECISIONS.md','docs/WHY.md','tasks/T-065-giao-dien-grafana/SPEC.md','tasks/T-065-giao-dien-grafana/REVIEW.md','tasks/T-065-giao-dien-grafana/REVIEW-2.md','results/T-064/ban-xuat/chi-muc-ban.json','results/T-064/ban-xuat/chi-muc-ban-tam-1.json','results/T-064/cau-hinh-de-xuat.json','src/m1/chuoi.py','src/m1/span.py')
  foreach($p in $paths){$protected[$p]=Digest (Join-Path $taskRoot $p)}
  WriteJson (Join-Path $out 'tiep-nhan.json') @{utc=[DateTime]::UtcNow.ToString('o');manifest_files=$n;manifest_match=$true;source_outputs=$proof;protected=$protected;log_prefix=$m.task_log;errors=@('py/rg unavailable in sandbox PATH; installed Python/Node executables denied; using PowerShell and Node REPL','Initial Node REPL full-manifest verification timed out; not counted as passed','Read-only exp-obs inventory first failed permission on root-owned cases; repeated with sudo read-only')}
  $inputRoot=Join-Path $taskBase 'nguon-l8'
  [IO.Directory]::CreateDirectory($inputRoot)|Out-Null
  Copy-Item -LiteralPath $iPath -Destination (Join-Path $inputRoot 'chi-muc-ban.json')
  foreach($b in $index.ban){foreach($c in $b.cac_ca){$d=Join-Path $inputRoot ($b.ban+'/'+$c.ca);[IO.Directory]::CreateDirectory($d)|Out-Null;if($c.dau_ra){Copy-Item -LiteralPath (Join-Path $taskRoot $c.dau_ra) -Destination (Join-Path $d 'method-output-1.json')}elseif($c.loi_chay){Copy-Item -LiteralPath (Join-Path $taskRoot $c.loi_chay) -Destination (Join-Path $d 'loi-chay.json')}}}
  Copy-Item -LiteralPath (Join-Path $taskBase 'grafana-l5/ui06/t065-l4-rca.json') -Destination (Join-Path $inputRoot 'dashboard-chinh.json')
  Copy-Item -LiteralPath (Join-Path $taskBase 'grafana-l5/ui06/t065-l4-phat-lai.json') -Destination (Join-Path $inputRoot 'dashboard-phat-lai.json')
  $now=[DateTime]::UtcNow.ToString('o')
  $text="`n`n## L8 — $now — Codex CLI, laptop Minh, người làm — mở kiểm G-c cuối`n`nPhân loại EXECUTE. Tiếp nhận brief L8 do Minh giao, quyền SPEC bổ sung và DECISIONS điều phối chiến dịch. Codex làm, Claude phản biện. Phạm vi tác động đã giao: results/T-065/ (nguồn chụp, bộ xuất/dashboard mới, kiểm 005, checkpoint/XONG/manifest/thay-doi-may/prompt) và chỉ nối LOG này; exp-obs chỉ thư mục kết quả mới t065-l8-001 và file dashboard mới, restart riêng Grafana nếu cần. Giữ bản G-c thử, không sửa STATE/docs/SPEC/REVIEW/T-064/src. Đã kiểm $n mục manifest, LOG và 83 đầu ra nguồn khớp. Chỉ mục bản 2 có ba bản × 28 ca; một slot P7 lỗi chạy không dựng hạng. Chưa thêm/đổi quyết định nghiên cứu.`n`nDùng lại dữ liệu L4 đã băm cho 22 ca; chỉ dựng thêm sáu ca dev3 trên exp-obs từ nguồn hiện có, không chạy M1 hay chấm. Các lệnh xử lý/API chia thành bước ngắn, dự kiến mỗi lượt dưới một giờ. Nếu công việc kéo dài: lỗi ở 10% giữ nguyên nguồn/hồ sơ tiếp nhận, chỉ chạy lại bước xuất lỗi (vài phút); ở 50% giữ từng ca xuất đã xong, chỉ bổ sung ca lỗi và slot phụ thuộc (vài phút); ở 99% giữ dashboard/dữ liệu đã kiểm, chỉ tiếp slot API hoặc hồ sơ còn thiếu (vài phút), không chạy lại M1/raw toàn bộ. Lỗi nguồn/hash chặn phần phụ thuộc; giữ mọi lượt hỏng. STOP local/remote kiểm trước mỗi bước. Không có lượt tính toán hơn một giờ được phát.`n"
  [IO.File]::AppendAllText((Join-Path $taskRoot $m.task_log.file),$text,$utf8)
  [IO.File]::AppendAllText((Join-Path $taskBase 'CHECKPOINT.md'),"`n`n## $now — L8 bước 1: tiếp nhận G-c bản cuối`n`nĐã đọc SPEC, L4/L7, nguồn đề tài, quyền điều phối và quyết định V082. Kiểm $n file cũ/LOG và 83 đầu ra nguồn khớp; bản chỉ mục 2 khớp hash. Giữ manifest trước tại codex/manifest-L8-truoc.json. Nguồn chụp tại nguon-l8/. exp-obs có trace/log/metric cả sáu ca dev3, P7 ebd5ef38 lỗi adapter và không có method-input. Chưa đổi máy. Phạm vi/lỗi giữa chừng ghi LOG L8. Tiếp: triển khai bộ xuất mới t065-l8-001, đọc/kiểm nguồn dev3 trên exp-obs, tạo dashboard UID mới. Không dùng nguồn T-064 trước khi khớp hash. Không chạy lại M1/chấm.`n",$utf8)
  Write-Output "INIT OK: $n prior files, $($proof.Count) outputs; LOG appended; source snapshots ready"
  exit
}
if($Action -eq 'seal'){
  $prior=Get-Content -Raw -Encoding UTF8 (Join-Path $taskBase 'codex/manifest-L8-truoc.json')|ConvertFrom-Json
  $reception=Get-Content -Raw -Encoding UTF8 (Join-Path $taskBase 'kiem/005-gc-cuoi/tiep-nhan.json')|ConvertFrom-Json
  $allowed=@('CHECKPOINT.md','XONG.md','thay-doi-may.md','prompt-ban-giao.md')
  $files=[ordered]@{};$missing=New-Object 'System.Collections.Generic.List[string]';$modified=New-Object 'System.Collections.Generic.List[string]'
  foreach($e in $prior.files.PSObject.Properties){
    $p=Join-Path $taskBase $e.Name
    if(!(Test-Path -LiteralPath $p)){$missing.Add($e.Name);continue}
    $value=@{sha256=Digest $p;bytes=(Get-Item -LiteralPath $p).Length}
    $files[$e.Name]=$value
    if($value.sha256 -ne $e.Value.sha256 -or $value.bytes -ne $e.Value.bytes){$modified.Add($e.Name)}
  }
  if($missing.Count){throw ('missing: '+($missing -join ','))}
  foreach($p in $modified){if($p -notin $allowed){throw "unexpected old file changed: $p"}}
  foreach($e in $reception.protected.PSObject.Properties){if((Digest (Join-Path $taskRoot $e.Name)) -ne $e.Value){throw ('protected changed: '+$e.Name)}}
  $logPath=Join-Path $taskRoot $prior.task_log.file
  $logBytes=[IO.File]::ReadAllBytes($logPath)
  $h=[Security.Cryptography.SHA256]::Create()
  $prefixHash=([BitConverter]::ToString($h.ComputeHash($logBytes,0,[int]$prior.task_log.bytes))).Replace('-','').ToLower()
  if($prefixHash -ne $prior.task_log.sha256){throw 'LOG prefix changed'}
  $new=New-Object 'System.Collections.Generic.List[string]'
  $newPaths=@('codex/l8-local.ps1','codex/l8-xuat.py','codex/L8-trang-thai.json','codex/manifest-L8-truoc.json','codex/l8-payload-001.tgz','codex/l8-xuat-luot-001.txt','codex/XONG-L8-truoc.md','codex/prompt-ban-giao-L8-truoc.md')
  foreach($folder in @('nguon-l8','kiem/005-gc-cuoi')){
    foreach($p in Get-ChildItem -LiteralPath (Join-Path $taskBase $folder) -Recurse -File){$newPaths+=$p.FullName.Substring($taskBase.Length+1).Replace('\','/')}
  }
  $reportRel='kiem/005-gc-cuoi/kiem-cuoi.json'
  foreach($rel in $newPaths|Sort-Object -Unique){
    if($rel -eq $reportRel){continue}
    $p=Join-Path $taskBase $rel
    if(!(Test-Path -LiteralPath $p)){throw ('new path missing '+$rel)}
    if(!$files.Contains($rel)){$new.Add($rel)}
    $files[$rel]=@{sha256=Digest $p;bytes=(Get-Item -LiteralPath $p).Length}
  }
  $new.Add($reportRel)
  $report=@{utc=[DateTime]::UtcNow.ToString('o');status='CHAN_NGUON';prior_files_checked=@($prior.files.PSObject.Properties).Count;missing=@();modified_files=@($modified);new_files=@($new|Sort-Object -Unique);protected_unchanged=$true;log_append_only=$true;source_outputs_verified=83;index_version=2;metadata_conflicts=28;dashboard_deployed=$false;api_checks_new_dashboard='chưa chạy vì nguồn chưa thống nhất';research_decisions_added=@();STATE_not_modified=$true;remote_before_after='may-sau-chan.json';prompt_template_check='prompt-kiem.json';draft_code='l8-xuat.py chỉ qua cú pháp và guard metadata, chưa được kiểm chức năng xuất/dashboard';scope='results/T-065 và chỉ nối LOG T-065; exp-obs chỉ thư mục con mới t065-l8-001'}
  WriteJson (Join-Path $taskBase $reportRel) $report
  $files[$reportRel]=@{sha256=Digest (Join-Path $taskBase $reportRel);bytes=(Get-Item -LiteralPath (Join-Path $taskBase $reportRel)).Length}
  $result=[ordered]@{utc=[DateTime]::UtcNow.ToString('o');status='chan_nguon';status_scope='L8';task_status='dat_mot_phan';prior_manifest='codex/manifest-L8-truoc.json';excluded=$prior.excluded;task_log=@{file=$prior.task_log.file;bytes=$logBytes.Length;sha256=Digest $logPath};new_files=@($new|Sort-Object -Unique);modified_files=@($modified);files=$files}
  WriteJson (Join-Path $taskBase 'manifest.json') $result
  Write-Output "SEALED: $($files.Count) files; source blocked; $($modified.Count) existing result files changed"
  exit
}
if($Action -eq 'verify'){
  $m=Get-Content -Raw -Encoding UTF8 (Join-Path $taskBase 'manifest.json')|ConvertFrom-Json
  $n=0;$bad=New-Object 'System.Collections.Generic.List[string]'
  foreach($e in $m.files.PSObject.Properties){$p=Join-Path $taskBase $e.Name;if(!(Test-Path -LiteralPath $p)){$bad.Add($e.Name)}elseif((Digest $p) -ne $e.Value.sha256 -or (Get-Item -LiteralPath $p).Length -ne $e.Value.bytes){$bad.Add($e.Name)};$n++}
  if((Digest (Join-Path $taskRoot $m.task_log.file)) -ne $m.task_log.sha256){$bad.Add('LOG')}
  if($bad.Count){throw ($bad -join ',')}
  Write-Output "VERIFIED: $n checksums and task LOG; status=$($m.status)"
}
