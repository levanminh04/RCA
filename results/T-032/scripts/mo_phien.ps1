$ErrorActionPreference = 'Stop'
$root = 'D:/RCA-flashticket'
$run = Join-Path $root 'results/T-032/runs/chuan-bi-001'
$utf8 = [Text.UTF8Encoding]::new($false)
if (Test-Path -LiteralPath $run) { throw 'Run already exists; do not overwrite.' }
[IO.Directory]::CreateDirectory((Join-Path $run 'before')) | Out-Null
$paths = @('docs/STATE.md','docs/WHY.md','docs/DECISIONS.md','tasks/T-032-g2-nguyen-nhan-xep-hang/SPEC.md')
foreach ($p in $paths) {
  [IO.File]::Copy((Join-Path $root $p),(Join-Path $run ('before/' + $p.Replace('/','__'))))
}
$specPath = Join-Path $root 'tasks/T-032-g2-nguyen-nhan-xep-hang/SPEC.md'
$spec = [IO.File]::ReadAllText($specPath)
$old = ($spec -split '\r?\n' | Where-Object { $_.StartsWith('- **Trạng thái:**') })
if (@($old).Count -ne 1) { throw 'Unexpected SPEC status.' }
$new = '- **Trạng thái:** Minh duyệt SPEC và thực hiện ngày 09/10/2026, lời duyệt "ĐÃ CHỐT" (Q-93); chọn A′, được chạy khi lõi đạt điều kiện trong SPEC. Ngân sách theo SPEC, tối đa 8 GiB mới; thực hiện qua nhiều phiên trên EC2 3.26.62.217. Nội dung thiết kế đã khóa.'
[IO.File]::WriteAllText($specPath,$spec.Replace($old,$new),$utf8)
$whyPath = Join-Path $root 'docs/WHY.md'
$why = [IO.File]::ReadAllText($whyPath)
if ($why -match '(?m)^## WHY-40\.') { throw 'WHY-40 already exists.' }
$appendix = ($spec -split '## Phụ lục — dự thảo WHY-40',2)[1] -split '## Prompt bàn giao',2
[IO.File]::AppendAllText($whyPath,"`n`n## WHY-40. Lần theo nguyên nhân thất bại xếp hạng — Đã quyết (Minh duyệt SPEC T-032 ngày 09/10/2026)`n`n" + $appendix[0].Trim() + "`n",$utf8)
$decPath = Join-Path $root 'docs/DECISIONS.md'
$dec = [IO.File]::ReadAllText($decPath)
if ($dec -match '\| Q-93 \|') { throw 'Q-93 already exists.' }
$q93 = '| Q-93 | 09/10 | Minh: "ĐÃ CHỐT". Duyệt SPEC T-032/T-033 theo bản trên file (Q-91, Q-92), chọn A′; duyệt thực hiện cả hai, gồm chạy A′ khi lõi T-032 đạt đúng điều kiện SPEC. Duyệt ngân sách giờ máy theo dự toán SPEC, tối đa 8 GiB dung lượng mới cho T-032; được chạy dài/qua đêm, vượt dự toán hoặc dung lượng thì checkpoint, dừng và trình Minh. Cho chuyển Nezha-OB dev đúng allowlist lên EC2: đo một lượt nhỏ, ghi dự toán thời gian vào LOG trước chuyển toàn bộ, kiểm hash hai đầu. T-032 dùng EC2 3.26.62.217 (key2.pem), T-033 chạy song song ở phiên Codex khác trên 3.107.246.249; mỗi phiên chỉ ghi phạm vi task, đọc lại file chung trước sửa/nối; phiên T-032 nối WHY-40, Q-93 này và sửa đúng dòng trạng thái SPEC/dòng STATE T-032. Ưu tiên tính đúng trên tiến độ và câu chữ SPEC: khi thấy bước/kiểm/tham số/chọn ca/tiêu chí khớp/diễn giải không ổn, nêu chỗ, bằng chứng, hậu quả, phương án; dừng phần phụ thuộc và trình Minh, không tự đổi SPEC/cách làm; phần độc lập được tiếp tục. Chạy dài EC2 phải độc lập SSH/laptop, có progress, stdout/stderr, PID, trạng thái, lệnh xem tiến độ trong LOG; chỉ báo EC2 T-032 ổn định sau ca/bước đầu đạt kiểm nguồn/hash/trung gian, đã đo tốc độ/RAM/đĩa đủ và lỗi tự dừng; trước đó báo cần giữ laptop mở. Khi ổn định báo ước lượng giờ xong, lệnh kiểm và việc tiếp tục phiên sau; không tự bật/tắt EC2, khi không còn cần báo Minh có thể tắt. Không mở test/data locked/dataset giữ ngoài; không commit/push. | lời duyệt và chỉ đạo Minh trong chat 09/10/2026; SPEC/LOG T-032 và SPEC T-033 |'
[IO.File]::AppendAllText($decPath,"`n$q93`n",$utf8)
$statePath = Join-Path $root 'docs/STATE.md'
$state = [IO.File]::ReadAllText($statePath)
$lines = $state -split '(?<=\n)'
$count = 0
for ($i=0; $i -lt $lines.Length; $i++) {
  if ($lines[$i].StartsWith('| T-032 |')) {
    $count++
    $parts = $lines[$i].Split('|')
    $parts[6] = ' Đã duyệt thực hiện 09/10 (Q-93); đang chuẩn bị nguồn/môi trường EC2 3.26.62.217, A′ sau lõi đạt; chưa có kết quả '
    $lines[$i] = [String]::Join('|',$parts)
  }
}
if ($count -ne 1) { throw 'Unexpected T-032 STATE row.' }
[IO.File]::WriteAllText($statePath,($lines -join ''),$utf8)
$logPath = Join-Path $root 'tasks/T-032-g2-nguyen-nhan-xep-hang/LOG.md'
if (Test-Path -LiteralPath $logPath) { throw 'LOG already exists.' }
$log = @'
# Nhật ký T-032

Chỉ người làm ghi; chỉ nối thêm. Codex là người làm, Claude là người phản biện.

## Phiên 1 — 09/10/2026 — Codex — Windows laptop / EC2 3.26.62.217 — người làm

**Mở phiên — EXECUTE:** Minh duyệt SPEC ngày 09/10/2026. Đã đọc AGENTS, STATE, SPEC; chưa có LOG/kết quả T-032 trước phiên. Đã đọc mục tiêu MRP/RQ2/P4, DT18-NV2/NV3, hướng dẫn cô §1, LESSONS và Q-88–92. Lời duyệt mới giải quyết trạng thái chờ duyệt trong STATE/SPEC; chỉ cập nhật dòng được Minh cho phép, giữ các câu lịch sử khác.

**Quyết định của Minh:** "ĐÃ CHỐT"; thực hiện/ngân sách/A′/chuyển allowlist/ưu tiên tính đúng/vận hành hai EC2 đã ghi Q-93. WHY-40 nối nguyên nội dung phụ lục; chữ "chưa là quyết định chạy" trong phụ lục mô tả thiết kế trước Q-93, quyền chạy hiện tại theo Q-93 và dòng trạng thái SPEC. Không tự sửa phụ lục.

**Công đoạn:** chuẩn bị nguồn, manifest, môi trường và trung gian thiếu. Chưa có kết luận cơ chế hoặc khả năng đo chờ. Dự toán được duyệt: lõi RE2 2–6 giờ máy, Nezha 1–4 giờ, A′ 0,5–2 giờ; chuyển tính riêng; tối đa 8 GiB mới. Công agent theo SPEC 24–48 giờ, chưa kiểm. Qua nhiều phiên theo Q-91/Q-93.

**Diễn biến:**
- Khởi tạo: lưu bản trước bốn file điều phối tại results/T-032/runs/chuan-bi-001/before; giữ nguyên mọi thay đổi có trước, không commit/push. T-033 có phiên khác xử lý; không đọc/ghi kết quả T-033.
- SSH chỉ đọc: dùng key2.pem tại D:/RCA-ext/keys, StrictHostKeyChecking=yes, BatchMode=yes. Sandbox chặn network lượt đầu; lượt được cấp quyền kết nối thành công, không sửa key/known_hosts. EC2 có 27.062.398.976 byte trống, 7.492.190.208 byte RAM available; chưa có ~/rca/T-032. Có môi trường T-025/main, py38 và nguồn/data T-031. Lệnh ls trả 1 do T-032 chưa tồn tại, không phải lỗi kết nối.
- Một trợ lý Codex chỉ đọc code/trung gian để hỗ trợ người làm; không mở vòng phản biện, không thay vai trò Claude, không được ghi hoặc chạy nghiên cứu.
- Python launcher py không có trong PATH; venv T-014-main không khởi tạo được base Python trong sandbox. Chưa chạy nghiên cứu trên laptop; sẽ dùng môi trường EC2 sau kiểm.
- CẦN GIỮ LAPTOP MỞ: chưa có ca nghiên cứu chạy nền đạt kiểm, chưa đo tốc độ chuyển hoặc kiểm môi trường.

'@
[IO.File]::WriteAllText($logPath,$log,$utf8)
Write-Output 'PASS: SPEC status, WHY-40, Q-93, STATE T-032, LOG initialized; before snapshots preserved.'
