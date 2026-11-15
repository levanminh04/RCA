# T-065 L8b — bộ xuất và dashboard G-c cuối

Hai UID mới: t065-l8b-rca và t065-l8b-phat-lai. Dữ liệu máy ở /opt/flash-ticket-obs/rca-ket-qua/t065-l8b-001/du-lieu; bản nhận nguyên ở may-l8b/du-lieu. Hai JSON thuận tiện đọc ở grafana-l8b/. Nguồn chỉ mục mới chụp ở nguon-l8b/chi-muc-ban.json; bản bị chặn L8 giữ nguon-l8/ và kiem/005-gc-cuoi/.

Báo cáo: kiem/006-gc-cuoi/BAO-CAO.md. Tóm tắt số và con trỏ: kiem/006-gc-cuoi/tom-tat.json. Schema: dinh-dang/0.5/ca.schema.json. Bộ xuất/kiểm chạy bằng Python chuẩn trên exp-obs qua SSH; kiểm schema cần jsonschema đã có. Các lệnh chỉ đọc/kiểm đã chạy:

    sudo python3 -B /opt/flash-ticket-obs/rca-ket-qua/t065-l8b-001/codex/l8b-kiem.py export
    sudo python3 -B /opt/flash-ticket-obs/rca-ket-qua/t065-l8b-001/codex/l8b-kiem.py schema

Các kiểm API/links/live đã có checkpoint; dùng lại dữ liệu hợp lệ. Bộ xuất l8b-xuat.py đọc nguồn đã chụp và template L4 đã băm; cache dev3 được kiểm hash trước dùng lại. Các action export/dashboards/deploy ghi file nên chỉ chạy trong phạm vi SPEC, không chạy lại deploy trên file đã tồn tại. Sửa service_options đã được đưa vào đường export mặc định; action service-options chỉ ghi lịch sử bản sửa lượt đầu.

Kiểm toàn vẹn local sau bàn giao:

    & ./results/T-065/codex/l8b-local.ps1 -Action verify

PowerShell 5.1: nếu script UTF-8 không BOM không nạp đúng tiếng Việt, dùng đọc tường minh:

    & ([ScriptBlock]::Create((Get-Content -Raw -Encoding UTF8 results/T-065/codex/l8b-local.ps1))) -Action verify

Phần UI mới chưa thực hiện; dùng codex/L8b-app-brief.md. Prompt Claude gộp L6/L7/L8/L8b ở prompt-ban-giao.md và mục cuối LOG T-065. Không có quyết định nghiên cứu mới trong lượt này.
