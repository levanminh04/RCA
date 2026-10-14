$ErrorActionPreference = 'Stop'
Set-Location D:/RCA-flashticket
$out = 'results/T-032/runs/ket-phien-002'
if (Test-Path -LiteralPath $out) { throw 'Checkpoint exists; do not overwrite' }
New-Item -ItemType Directory -Path $out | Out-Null
$encoding = [Text.UTF8Encoding]::new($false)
function ReadText($p) { [IO.File]::ReadAllText((Join-Path $PWD $p)) }
function Hash($p) {
    $stream = [IO.File]::OpenRead((Join-Path $PWD $p))
    $hasher = [Security.Cryptography.SHA256]::Create()
    try { ([BitConverter]::ToString($hasher.ComputeHash($stream))).Replace('-','').ToLowerInvariant() }
    finally { $stream.Dispose(); $hasher.Dispose() }
}
function JsonFile($p, $value) {
    [IO.File]::WriteAllText((Join-Path $PWD $p), ($value | ConvertTo-Json -Depth 20) + "`n", $encoding)
}
$before = 'results/T-032/runs/chuan-bi-001/before/'
$spec = ReadText 'tasks/T-032-g2-nguyen-nhan-xep-hang/SPEC.md'
$oldSpec = ReadText ($before + 'tasks__T-032-g2-nguyen-nhan-xep-hang__SPEC.md')
$stripStatus = '(?m)^- \*\*Trạng thái:\*\*.*\r?\n'
$checks = [ordered]@{
    SPEC_only_status_line = ([regex]::Replace($spec,$stripStatus,'') -eq [regex]::Replace($oldSpec,$stripStatus,''))
    WHY_original_prefix_preserved = (ReadText 'docs/WHY.md').StartsWith((ReadText ($before+'docs__WHY.md')))
    DECISIONS_original_prefix_preserved = (ReadText 'docs/DECISIONS.md').StartsWith((ReadText ($before+'docs__DECISIONS.md')))
    Q93_one_row = ([regex]::Matches((ReadText 'docs/DECISIONS.md'),'(?m)^\| Q-93 \|').Count -eq 1)
    WHY40_one_header = ([regex]::Matches((ReadText 'docs/WHY.md'),'(?m)^## WHY-40\.').Count -eq 1)
}
foreach($key in @($checks.Keys)) { if(-not $checks[$key]) { throw "Scope failure: $key" } }

# Reread immediately before editing only this task's row; preserve every other byte.
$state = ReadText 'docs/STATE.md'
$oldRow = @($state -split "`n" | Where-Object {$_ -match '^\| T-032 \|'})
if($oldRow.Count -ne 1) { throw 'T-032 row count' }
$row = '| T-032 | Lần theo nguyên nhân thất bại xếp hạng | P4 | Codex | Claude | Đang thực hiện: BARO RE2 chạy nền ổn định (LOG phiên 2); MicroRank lệch tuyệt đối cả native, dừng nhánh/A′; chưa khóa đối chứng hay kết luận cơ chế | `tasks/T-032-g2-nguyen-nhan-xep-hang/` |'
$newState = $state.Replace($oldRow[0], $row)
if($newState.Replace($row,'') -ne $state.Replace($oldRow[0],'')) { throw 'Unexpected STATE change' }
[IO.File]::WriteAllText((Join-Path $PWD 'docs/STATE.md'), $newState, $encoding)
$checks.STATE_this_checkpoint_only_T032 = $true
JsonFile "$out/scope-checks.json" $checks

$logText = @'

### Kết thúc phiên 2 — checkpoint để tiếp tục

1. **Đã làm:** chuyển và kiểm gói nguồn theo quyền Minh; kiểm kê schema thô/danh mục nhóm/trung gian sáu phương pháp; fixture MicroRank và BARO; tái lập đúng ERROR MicroRank, phát hiện lệch ca OK và chạy đúng một chẩn đoán được Minh duyệt. BARO ca RE2 đầu đạt; đã khởi queue 29 ca còn lại có fail-stop. Lời duyệt Python hiện có và chuyển nguồn/diagnostic nằm trong các mục Quyết định của Minh ở LOG này; không suy thành quyền nới khớp tuyệt đối.
2. **File thay đổi trong phiên:** scripts/runs và trung-gian-nguon.md dưới results/T-032; nối LOG T-032; chỉ dòng T-032 của docs/STATE.md. Phiên này không sửa thêm SPEC/WHY/DECISIONS; các thay đổi được duyệt ở phiên 1 vẫn giữ. Không sửa source phương pháp, dữ liệu hoặc kết quả cũ; không đọc/ghi T-033, không mở locked/test/giữ ngoài, không commit/push. Danh sách/hash toàn bộ file T-032 đã có tại checkpoint ket-phien-002/files.json; không gồm kết quả remote còn đang sinh.
3. **Kiểm và kết quả:** 1.058 kiểm nguồn EC2 PASS; 776 file gói + hai manifest hash hai đầu đạt. MicroRank fixture PASS; real ERROR replay PASS; real OK có 161 trường số lệch, native không observer vẫn lệch 161 và khớp observed 0 khác. Không dùng lượt lệch. BARO fixture và ca RE2 đầu PASS tuyệt đối, artifact tải về 254/254 và 2.856/2.856 khớp. Queue đã có hai ca mới PASS tại mốc 23:21; số cuối phải đọc status/manifest remote, không suy từ mốc này. Nhóm003 và archive checkpoint hash đạt. Kiểm diff SPEC chỉ dòng trạng thái; WHY/DECISIONS giữ prefix cũ và đúng một WHY-40/Q-93; cập nhật STATE vừa kiểm chỉ dòng T-032. Source/code cũ và nguồn chứng cứ được kiểm trước khi dùng; bảng kiểm kê không thay bằng chứng theo ca.
4. **Chưa chắc/cần Minh quyết:** T-032 chưa hoàn thành; chưa trả lời cơ chế caller/root hay đủ căn cứ chọn P5–P6/G2. MicroRank/A′ dừng do không đạt điều kiện tuyệt đối; chưa biết thành phần Python/OS/BLAS/hardware nào gây lệch. Muốn đổi môi trường/tiêu chí hoặc chuyển tính toán về laptop phải trình Minh đúng phạm vi/chi phí trước, không tự thử hoặc coi độ lệch nhỏ là được phép. BARO Nezha và bốn phương pháp còn lại chưa phát lại; đối chứng/đọc tay/M5/coverage/semantics và A′ chưa xong. Kiểm kê đã chỉ đúng trung gian thiếu và nguồn code cần bổ sung; nguyên nhân vật lý chưa phân xử, chưa có nhãn lan hay lợi ích đồ thị. Nội dung commit dự kiến khi Minh cho phép: `T-032: checkpoint nguồn, wrapper và phát lại lõi`; chưa thực hiện.

**EC2 và việc Minh cần làm:** lượt BARO RE2 nền đã ổn định, có thể tắt laptop; giữ EC2 bật để hoàn thành. Ước lượng 23:31–23:42 ngày 09/10/2026 giờ Việt Nam cho queue này, không cho toàn task. EC2 chưa hết nhu cầu của task; agent không tự bật/tắt. Khi Minh mở lại phiên, agent kiểm trạng thái và hash trước, thu kết quả, ghi từng ca đã xong vào LOG, rồi tiếp phần độc lập. Không khởi lại run đang chạy/đã hợp lệ. Nếu STOPPED thì giữ lượt, đọc lỗi và trình phần cần thay đổi trước khi chạy phụ thuộc.

**Bước tiếp chính xác:**

```powershell
ssh -i D:/RCA-ext/keys/key2.pem -o BatchMode=yes -o StrictHostKeyChecking=yes ubuntu@3.26.62.217 'cat ~/rca/T-032/runs/baro-re2-batch-001/status.json; cat ~/rca/T-032/runs/baro-re2-batch-001-monitor/status.json; ps -p 115175,115176 -o pid,ppid,pgid,sid,etime,args'
```

Đọc results/T-032/trung-gian-nguon.md; runs/baro-re2-plan-001/{plan,estimates,manifest}.json; runs/groups-003/{catalog,unit-universe,counterpart-candidates,selection-open,manifest}.json. Manifest đầu ra batch chỉ được tin sau kiểm hash completed-cases.jsonl → từng check.json/artifact_manifest. Nếu PASS, thu bằng archive mới trong T-032, kiểm hai đầu, không ghi đè checkpoint hoặc lượt cũ. Sau đó chọn ca đầu BARO Nezha từ nguồn main/allowlist, kiểm lại nhánh pilot/full bằng wrapper hiện hành và thư mục mới; chưa được báo ổn định cho nhánh Nezha trước kiểm ca đầu. SimpleRCA/TraceRCA/CIRCA/TORAI tiếp từ bảng trung gian thiếu, giữ raw/source read-only. Chỉ tiếp MicroRank/A′ sau khi vấn đề khớp được giải quyết hoặc Minh duyệt đề xuất khác rõ ràng.

**Lệnh cuối ghi checkpoint/kiểm file:** `& ./results/T-032/scripts/checkpoint_002.ps1` trong PowerShell 7 của phiên. Lệnh khởi queue, môi trường, PID, progress/stdout/stderr và lệnh Minh tự xem đã ghi ngay trước mục kết thúc này. Kiểm hash/checkpoint không chạy nghiên cứu laptop.

### Prompt cho Claude — Minh chọn chuyển hoặc để phiên sau

Đây là prompt soát đầu ra hiện có, chưa là yêu cầu nghiệm thu task. Chưa cấp quyền ghi REVIEW; chỉ trả lời trong chat.

```text
'@
$template = ReadText 'docs/review-prompt.md'
function Block($heading) {
    $pattern = '(?s)' + [regex]::Escape($heading) + '\r?\n\r?\n```text\r?\n(.*?)\r?\n```'
    $match = [regex]::Match($template,$pattern)
    if(-not $match.Success){throw "Prompt block missing: $heading"}
    $match.Groups[1].Value
}
$prompt = Block '## Prompt chung'
$replacements = [ordered]@{
    '<mã và đường dẫn; nếu đề xuất đang trong chat, dán nguyên văn>'='T-032, tasks/T-032-g2-nguyen-nhan-xep-hang/'
    '<soát SPEC / soát kết quả / người làm đáp phản biện / kiểm lại phản hồi và sửa>'='soát kết quả'
    '<gói, cổng hiện tại; ngoài task thì ghi loại đề xuất>'='P4, G2'
    '<tên theo SPEC; ngoài task thì ghi vai trò dự kiến>'='Codex làm; Claude phản biện'
    '<danh sách đường dẫn và git diff từ commit gốc nếu có>'='AGENTS.md; docs/STATE.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; hai nguồn đề tài được dẫn bên dưới; SPEC và LOG T-032; diff làm việc của các đường dẫn T-032'
    '<đường dẫn theo thứ tự thời gian; không có thì ghi không có>'='không có bản phản biện kết quả T-032 trên file'
    '<đường dẫn, revision, manifest, hướng dẫn môi trường/lệnh chạy; không áp dụng thì ghi không áp dụng>'='results/T-032/; nguồn T-022/T-024/T-026/T-028/T-029/T-031 theo SPEC; results/T-032/trung-gian-nguon.md; runs/ket-phien-002/files.json; các manifest của từng run; môi trường/lệnh tại LOG phiên 2 và scripts/start_stage.sh, start_stage_baro.sh, start_baro_batch.sh'
    '<chỉ trả lời trong chat, hoặc file và phần được phép ghi chính xác>'='chỉ đọc và trả lời trong chat'
}
foreach($pair in $replacements.GetEnumerator()){$prompt=$prompt.Replace($pair.Key,$pair.Value)}
$prompt += "`n`n"+(Block '### Soát kết quả')+"`n`n"+(Block '### G2 — Baseline và phân tích hạn chế')
Add-Content -LiteralPath tasks/T-032-g2-nguyen-nhan-xep-hang/LOG.md -Encoding utf8 -Value ($logText+"`n"+$prompt+"`n"+'```'+"`n")

$fileRows = foreach($file in Get-ChildItem -LiteralPath results/T-032 -Recurse -File | Sort-Object FullName) {
    $relative=$file.FullName.Substring($PWD.Path.Length+1).Replace('\','/')
    if($relative.StartsWith($out+'/')) { continue }
    [pscustomobject]@{path=$relative;bytes=$file.Length;sha256=(Hash $relative)}
}
JsonFile "$out/files.json" @{at=(Get-Date -Format o);files=@($fileRows);count=@($fileRows).Count;bytes=($fileRows|Measure-Object bytes -Sum).Sum;remote_running_outputs_included=$false}
$control = foreach($path in @('tasks/T-032-g2-nguyen-nhan-xep-hang/LOG.md','tasks/T-032-g2-nguyen-nhan-xep-hang/SPEC.md','docs/STATE.md',"$out/files.json","$out/scope-checks.json")) {
    [pscustomobject]@{path=$path;sha256=(Hash $path)}
}
JsonFile "$out/checkpoint-manifest.json" @{status='PASS_LOCAL_CHECKPOINT_REMOTE_BATCH_RUNNING_AT_LAST_CHECK';files=@($control);remote_status_is_snapshot=$true}
Write-Output ('CHECKPOINT_PASS files='+@($fileRows).Count+' bytes='+($fileRows|Measure-Object bytes -Sum).Sum)
