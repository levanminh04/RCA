$ErrorActionPreference = 'Stop'
Set-Location D:/RCA-flashticket
$out = 'results/T-032/runs/tiep-tuc-003'
if (Test-Path -LiteralPath $out) { throw 'Do not overwrite session' }
$handoff = Get-Content -Raw -LiteralPath results/T-032/runs/ket-phien-002/handoff-final.json | ConvertFrom-Json
$checks = @()
foreach ($row in $handoff.files) {
    if ($row.path -eq 'docs/STATE.md') { continue } # shared mutable index, reread below
    $actual = (Get-FileHash -LiteralPath $row.path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $row.sha256) { throw "Checkpoint mismatch $($row.path)" }
    $checks += [ordered]@{path=$row.path; sha256=$actual; pass=$true}
}
New-Item -ItemType Directory -Path $out | Out-Null
$encoding = [Text.UTF8Encoding]::new($false)
function WriteText($path,$text) { [IO.File]::WriteAllText((Join-Path $PWD $path),$text,$encoding) }
foreach($path in @('AGENTS.md','docs/STATE.md','docs/WHY.md','docs/DECISIONS.md','tasks/T-032-g2-nguyen-nhan-xep-hang/SPEC.md')) {
    [IO.File]::WriteAllBytes((Join-Path $PWD ($out+'/'+$path.Replace('/','__'))),[IO.File]::ReadAllBytes((Join-Path $PWD $path)))
}
WriteText ($out+'/checkpoint-check.json') (($checks | ConvertTo-Json -Depth 10)+"`n")
$entry = @'


## Phiên 3 — 10/10/2026 — Codex — laptop Windows / EC2 3.26.62.217 — người làm

- Minh duyệt SPEC ngày 09/10/2026. Intent EXECUTE: Minh yêu cầu kiểm tiến độ và tiếp đúng T-032 theo cùng quyền, ngân sách và ưu tiên tính đúng. Codex tiếp vai trò người làm; Claude vẫn là người phản biện chính thức. Không tiếp công việc T-033.
- Đã đọc lại AGENTS, STATE, toàn SPEC và checkpoint LOG phiên 2. Kiểm control handoff trước nối LOG đạt; STATE là index dùng chung nên đọc hiện hành, không ép hash snapshot cũ. Không nối trùng WHY-40/Q-93, không sửa SPEC.
- Live check 09:12 ngày 10/10 (+07): baro-re2-batch-001 và monitor đều PASS, 29 ca mới + 1 pilot = 30 ca; kết thúc 23:29:44 ngày 09/10 (+07), exit 0, PID cũ đã kết thúc. Đây là trạng thái worker, còn phải kiểm manifest/hash từng ca trước dùng. Không chạy lại queue.
- MicroRank và A′ vẫn dừng: native diagnostic đã dùng đúng quyền, native–observed khớp nhưng native–frozen còn lệch 161 trường. Không nới tolerance hoặc đổi môi trường. Các phần độc lập được tiếp trong phạm vi SPEC.
- Hai trợ lý nội bộ hỗ trợ coverage trace và capture TraceRCA, không là lượt phản biện chính thức; không tự gửi prompt Claude. Sandbox process mặc định lỗi khởi tạo; gọi ngoài sandbox được auto-review cho phép. Không thay package/môi trường.
- CẦN GIỮ LAPTOP MỞ trong bước kiểm nguồn/ca đầu BARO Nezha và nhánh mới; dự kiến 30–60 phút, mốc báo lại sau pilot và đo RAM/dung lượng/tốc độ. Chưa có lượt mới được coi ổn định.
'@
[IO.File]::AppendAllText((Join-Path $PWD 'tasks/T-032-g2-nguyen-nhan-xep-hang/LOG.md'),$entry+"`n",$encoding)
WriteText ($out+'/opened.json') (([ordered]@{status='PASS';at=(Get-Date).ToString('o');checkpoint_controls=$checks;shared_state_snapshot_only=$true;log_append_only=$true} | ConvertTo-Json -Depth 10)+"`n")
Write-Output 'PASS_SESSION3_OPEN_CONTROL_HASHES'
