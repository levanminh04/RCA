$ErrorActionPreference='Stop'
$root='D:/RCA-flashticket'
$run=Join-Path $root 'results/T-032/runs/chuan-bi-001'
$utf8=[Text.UTF8Encoding]::new($false)
function ReadText($p){[IO.File]::ReadAllText((Join-Path $root $p))}
function WriteJson($p,$o){[IO.File]::WriteAllText((Join-Path $root $p),(ConvertTo-Json -InputObject $o -Depth 50),$utf8)}
$statePath=Join-Path $root 'docs/STATE.md'
$state=[IO.File]::ReadAllText($statePath)
$stateLines=$state -split '(?<=\n)'
$n=0
for($i=0;$i -lt $stateLines.Length;$i++){
 if($stateLines[$i].StartsWith('| T-032 |')){
  $parts=$stateLines[$i].Split('|'); $n++
  $parts[6]=' Đang chuẩn bị (09/10, Q-93): nguồn/hash và chuyển Nezha đạt; chưa phát lại, chờ Minh xác nhận chuyển gói code/kết quả bị kiểm duyệt công cụ chặn; checkpoint LOG phiên 1 '
  $stateLines[$i]=[String]::Join('|',$parts)
 }
}
if($n -ne 1){throw 'Unexpected STATE row'}
[IO.File]::WriteAllText($statePath,($stateLines -join ''),$utf8)
$checks=Get-Content (Join-Path $run 'source-checks.json') -Raw | ConvertFrom-Json
if($checks.status -ne 'PASS'){throw 'Source checks incomplete'}
$scope=[ordered]@{}
$spec=ReadText 'tasks/T-032-g2-nguyen-nhan-xep-hang/SPEC.md'
$specBefore=[IO.File]::ReadAllText((Join-Path $run 'before/tasks__T-032-g2-nguyen-nhan-xep-hang__SPEC.md'))
$scope.SPEC_only_status=([regex]::Replace($spec,'(?m)^- \*\*Trạng thái:\*\*[^\r\n]*','') -ceq [regex]::Replace($specBefore,'(?m)^- \*\*Trạng thái:\*\*[^\r\n]*',''))
$whyBefore=[IO.File]::ReadAllText((Join-Path $run 'before/docs__WHY.md'))
$why=ReadText 'docs/WHY.md'
$scope.WHY_original_prefix_preserved=$why.StartsWith($whyBefore)
$appendix=(($specBefore -split '## Phụ lục — dự thảo WHY-40',2)[1] -split '## Prompt bàn giao',2)[0].Trim()
$scope.WHY40_exact_appendix=$why.Contains($appendix)
$scope.WHY40_one_header=([regex]::Matches($why,'(?m)^## WHY-40\.').Count -eq 1)
$decBefore=[IO.File]::ReadAllText((Join-Path $run 'before/docs__DECISIONS.md'))
$dec=ReadText 'docs/DECISIONS.md'
$scope.DECISIONS_original_prefix_preserved=$dec.StartsWith($decBefore)
$scope.Q93_one_row=([regex]::Matches($dec,'(?m)^\| Q-93 \|').Count -eq 1)
$scope.STATE_this_script_only_T032=([regex]::Replace($state,'(?m)^\| T-032 \|[^\r\n]*','') -ceq [regex]::Replace(($stateLines -join ''),'(?m)^\| T-032 \|[^\r\n]*',''))
foreach($k in $scope.Keys){if(-not $scope[$k]){throw "Scope check failed: $k"}}
WriteJson 'results/T-032/runs/chuan-bi-001/scope-checks.json' $scope

$log=@'

### Checkpoint cuối phiên 1 — 09/10/2026

1. **Đã làm:** ghi lời duyệt/thẩm quyền thực hiện; đọc yêu cầu nguồn và đường code; kiểm hash 420 bản ghi T-024, 248 bản ghi T-026, các bảng/đặc trưng T-028 dùng chuẩn bị; kiểm 154 file raw Nezha. Chuyển Nezha dev theo allowlist vào EC2 và kiểm hash hai đầu đạt. Mới hoàn thành một phần chuẩn bị, chưa khóa danh mục nhóm/đối chứng hoặc phát lại lõi. Chưa trả lời cơ chế caller/root, chưa đánh giá khả năng đo chờ hoặc chạy A′; không nhận đạt tiêu chí xong/RQ2/G2.
2. **File thay đổi:** dòng Trạng thái SPEC T-032; tạo LOG; chỉ dòng T-032 của STATE; nối WHY-40 nguyên phụ lục; nối một dòng Q-93. Trong results/T-032 tạo scripts/mo_phien.ps1, kiem_nguon.ps1, capture_microrank.py, checkpoint_001.ps1 và runs/chuan-bi-001 (snapshot trước, kiểm nguồn, gói chuyển, hash, dự toán, checkpoint). EC2 chỉ ghi ~/rca/T-032/: raw dev ở repo/data/ngoai-rcaeval/nezha/..., gói raw ở inputs/. File set/hash tại checkpoint-manifest.json. Không sửa src/data/task khác, không commit/push, không mở test/locked/dataset giữ ngoài. Giữ mọi thay đổi có trước và thay đổi của phiên T-033.
3. **Kiểm và kết quả:** source-checks.json PASS; hash archive Nezha và 154/154 raw khớp allowlist. Môi trường EC2 main có các phiên bản thư viện chính khớp T-031; Python 3.12.3 khác 3.12.10, Minh đã duyệt trong phiên dùng sẵn có, giữ kiểm khớp tuyệt đối. Wrapper MicroRank mới chỉ đọc/soát code; chưa AST, fixture, phục hồi ma trận hay phát lại vì chưa chuyển được code. Không dùng wrapper làm bằng chứng trước khi đạt. Scope-checks.json xác nhận SPEC chỉ đổi trạng thái, prefix WHY/DECISIONS giữ nguyên, WHY-40 đúng phụ lục, Q-93 duy nhất, lần cập nhật STATE chỉ T-032.
4. **Điều còn chờ Minh:** kiểm duyệt công cụ tự động từ chối hai lần lệnh SCP gói metadata-001.tar.gz + source-checks.json + nezha-transfer-manifest.json tới ubuntu@3.26.62.217:rca/T-032/inputs/. Lý do trả về: gói xuất code/kết quả/metadata rộng hơn quyền raw Nezha; không công nhận trích SPEC làm quyền xuất dữ liệu nhạy cảm. Đã kiểm gói thực tế 13.484.397 byte nén (197.347.521 byte nội dung), 776 file nguồn dev/code; không có khóa/locked/T-033; lần hai giữ đúng lệnh, trình quyền SPEC, vẫn bị từ chối. Không vòng tránh. Đã hỏi Minh xác nhận trực tiếp đúng gói và đích qua ô câu hỏi; đang chờ. Phần raw Nezha được duyệt riêng đã làm xong độc lập. Rủi ro cần xác nhận là đưa code và kết quả nghiên cứu từ laptop lên EC2 của task. Chưa có bất đồng khoa học mới cần sửa SPEC; chưa đủ bằng chứng để nghiệm thu hay chọn thiết kế P5–P6. Quyết định ngoại lệ Python đã lưu LOG theo đúng quyền mới, không tự nối DECISIONS dòng thứ hai.
5. **EC2/laptop:** chưa có tiến trình nghiên cứu, PID nghiên cứu=N/A; stdout/stderr/progress nghiên cứu chưa tạo. remote-state-001.txt chỉ có shell của lệnh kiểm trạng thái, không phải worker. Tổng ~/rca/T-032 hiện 1.149.308.741 byte; đĩa còn 25.912.573.952 byte, RAM available 7.483.174.912 byte lúc kiểm. Chưa có ETA hoàn tất nghiên cứu; các ước lượng SPEC chưa được đo phát lại. **CẦN GIỮ LAPTOP MỞ nếu tiếp tục chặng chuyển code/kiểm ca đầu trong phiên:** chưa có lượt nền độc lập đạt kiểm để báo ổn định; khoảng thời gian còn cần giữ OPEN tới khi quyền chuyển và ca đầu được kiểm, không hứa giờ xong. Không có công việc đang chạy cần laptop duy trì; nếu dừng phiên thì dữ liệu đã nằm an toàn trên EC2 và làm tiếp từ checkpoint. Không tự bật/tắt EC2. EC2 vẫn cần cho bước kế tiếp, nhưng hiện không có lượt dài cần giữ chạy trong khi chờ Minh.
6. **Bước tiếp theo chính xác:** đọc mục này, SPEC, source-checks.json, transfer-estimate.json, nezha-remote-hashes.txt, checkpoint-manifest.json; kiểm lại process/hash trước chạy. Không chạy lại mo_phien.ps1 hoặc kiem_nguon.ps1 vào lượt cũ, không chuyển lại raw đạt hash. Sau Minh xác nhận trực tiếp gói: chạy đúng lệnh SCP bên dưới, kiểm hash gói theo manifest, giải nén vào ~/rca/T-032/repo (không ghi đè raw); kiểm mọi hash metadata nguồn/đích. Kiểm nguồn external trên EC2 theo results/T-026/runs/session-005/external-code-manifest.json, RE2 allowlist/config theo manifest nguồn; nguyên môi trường/code cũ chỉ đọc. Sau đó chuyển wrapper mới được quyền, kiểm AST + fixture OK/non-OK/error, phục hồi sparse/dense hash, thực hiện một ca MicroRank ERROR và một ca OK theo opaque_id trước; so trạng thái, điểm/khóa, nhóm hòa, thứ tự tuyệt đối với nguồn. Chưa có runner cohort; người nhận tiếp phải viết trong scripts/runs T-032, lưu PID/progress/stdout/stderr/status và lỗi tự dừng trước chạy nền. Đo RAM/đĩa/tốc độ ca đầu rồi mới dự toán phần còn lại và báo ổn định. Các phương pháp khác, danh mục nhóm/đối chứng, trace/đọc tay và A′ còn chưa làm; A′ chỉ sau lõi/danh mục/kiểm riêng đạt theo SPEC.
7. **Lệnh cuối có ghi checkpoint:** `& results/T-032/scripts/checkpoint_001.ps1` trên laptop; sau đó chỉ đọc diff/manifest/LOG. Đề xuất nội dung commit khi Minh yêu cầu: `T-032: ghi duyệt, kiểm nguồn và chuẩn bị Nezha dev trên EC2`; hiện không commit/push.

Lệnh chuyển đang chờ Minh xác nhận trực tiếp (không tự chạy lại khi chưa có câu trả lời):
```powershell
scp -i D:/RCA-ext/keys/key2.pem -o BatchMode=yes -o StrictHostKeyChecking=yes results/T-032/runs/chuan-bi-001/metadata-001.tar.gz results/T-032/runs/chuan-bi-001/nezha-transfer-manifest.json results/T-032/runs/chuan-bi-001/source-checks.json ubuntu@3.26.62.217:rca/T-032/inputs/
```

Lệnh xem tiến độ sau mở lại (hiện chưa có lượt nghiên cứu):
```powershell
ssh -i D:/RCA-ext/keys/key2.pem -o BatchMode=yes -o StrictHostKeyChecking=yes ubuntu@3.26.62.217 'find ~/rca/T-032/runs -maxdepth 2 -type f -print; du -sb ~/rca/T-032; df -h /home/ubuntu'
```

### Prompt bàn giao tùy Minh chuyển cho Claude

Task chưa hoàn thành; không đề nghị nghiệm thu hoặc tự mở vòng phản biện. Nếu Minh chọn kiểm checkpoint, chỉ trả lời trong chat. Prompt dùng nguyên mẫu hiện hành, không tự cấp quyền ghi REVIEW.

'@
$template=ReadText 'docs/review-prompt.md'
function PromptBlock([string]$heading){
 $after=($template -split [regex]::Escape($heading),2)[1]
 return [regex]::Match($after,'(?s)```text\r?\n(.*?)\r?\n```').Groups[1].Value
}
$prompt=PromptBlock '## Prompt chung'
$pairs=@{
 '<mã và đường dẫn; nếu đề xuất đang trong chat, dán nguyên văn>'='T-032; tasks/T-032-g2-nguyen-nhan-xep-hang/'
 '<soát SPEC / soát kết quả / người làm đáp phản biện / kiểm lại phản hồi và sửa>'='soát kết quả checkpoint'
 '<gói, cổng hiện tại; ngoài task thì ghi loại đề xuất>'='P4, G2'
 '<tên theo SPEC; ngoài task thì ghi vai trò dự kiến>'='Codex làm, Claude phản biện'
 '<danh sách đường dẫn và git diff từ commit gốc nếu có>'='tasks/T-032-g2-nguyen-nhan-xep-hang/SPEC.md; docs/MRP.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; bản trước tại results/T-032/runs/chuan-bi-001/before/'
 '<đường dẫn theo thứ tự thời gian; không có thì ghi không có>'='không có bản phản biện trong thư mục T-032'
 '<đường dẫn, revision, manifest, hướng dẫn môi trường/lệnh chạy; không áp dụng thì ghi không áp dụng>'='results/T-032/scripts/; results/T-032/runs/chuan-bi-001/checkpoint-manifest.json; tasks/T-032-g2-nguyen-nhan-xep-hang/LOG.md; môi trường nguồn results/T-031/moi-truong.json'
 '<chỉ trả lời trong chat, hoặc file và phần được phép ghi chính xác>'='chỉ đọc và trả lời trong chat; không chạy nghiên cứu hoặc ghi file'
}
foreach($k in $pairs.Keys){$prompt=$prompt.Replace($k,$pairs[$k])}
$prompt += "`n`n" + (PromptBlock '### Soát kết quả') + "`n`n" + (PromptBlock '### G2 — Baseline và phân tích hạn chế')
[IO.File]::AppendAllText((Join-Path $root 'tasks/T-032-g2-nguyen-nhan-xep-hang/LOG.md'),$log + "`n" + '```text' + "`n" + $prompt + "`n" + '```' + "`n",$utf8)
$files=Get-ChildItem (Join-Path $root 'results/T-032') -File -Recurse | Where-Object Name -ne 'checkpoint-manifest.json'
$rows=@($files | Sort-Object FullName | ForEach-Object {[ordered]@{path=$_.FullName.Substring($root.Length+1).Replace('\','/');bytes=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName).Hash.ToLowerInvariant()}})
$controls=@('docs/STATE.md','docs/WHY.md','docs/DECISIONS.md','tasks/T-032-g2-nguyen-nhan-xep-hang/SPEC.md','tasks/T-032-g2-nguyen-nhan-xep-hang/LOG.md') | ForEach-Object {[ordered]@{path=$_;sha256=(Get-FileHash -LiteralPath (Join-Path $root $_)).Hash.ToLowerInvariant()}}
WriteJson 'results/T-032/runs/chuan-bi-001/checkpoint-manifest.json' ([ordered]@{at=(Get-Date -Format o);stage='preparation; pending direct approval for code/results upload';research_started=$false;new_local_bytes=($files|Measure-Object Length -Sum).Sum;remote_bytes=1149308741;files=$rows;control_snapshots=@($controls);scope_checks=$scope;excludes='self hash; concurrent shared docs may advance after checkpoint'})
Write-Output 'PASS: checkpoint, LOG, STATE T-032, handoff prompt and manifest written.'
