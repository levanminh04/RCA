# Bàn giao lượt đêm T-058

Đọc [báo cáo sáng](bao-cao-sang.md) trước. `bao-cao.md` là bản sao của cùng báo cáo theo tên đầu ra SPEC. Cách SSH/MobaXterm, tunnel và từng lệnh đã chạy nằm ở [hướng dẫn triển khai](huong-dan-trien-khai.md).

| Cần xem | File chính |
|---|---|
| Trạng thái tiếp tục/dừng | CHECKPOINT.md, LOG-dem.md, DONE.md khi đã dừng |
| Môi trường/image/agent | moi-truong.md, manifest-digest.json, runtime-*.json, environment-*.json |
| C1/C2 | kiem-agent.md, kiem-telemetry.md, grafana-evidence.json |
| C3/OOM/bộ nhớ | kiem-bo-nho.md, so-do-tai-nguyen.json, resources-30m-*.jsonl, unplanned-oom.json, memory-after-fix-summary.json |
| C4 và thiếu kênh | rca-ban-dau.md, m1-feasibility-details.json, rca-ban-dau/cases/, rca-ban-dau/outputs/ |
| Kế hoạch trước đầu ra | m1-execution-plan.json (v1 hủy), m1-execution-plan-v2.json, m1-plan-v2-deviations.json |
| Nhãn/tác động độc lập, ngoài M1 | so-tiem-loi.jsonl, load-impact.json, load-impact-detail.json, light-load*.jsonl |
| Cấu hình công khai cuối | config-public/, public-*-config.tgz và audit JSON; không chứa env/realm bí mật/key-ring |
| Việc chờ quyết | CAN-MINH-QUYET.md, prompt-ban-giao-Claude.md |
| Tự kiểm và toàn bộ file | self-check.json, artifacts-sha256.json |

Hai tar case và bản giải nén là cùng dữ liệu đã so SHA với Oracle. Không sửa gói/đầu ra cũ để thử tiếp. Sổ chỉ ghi thêm, không phải đầu vào RCA. File `credential-hash-catalog.json` chỉ có SHA-256 của giá trị ngẫu nhiên phục vụ quét trước export; không có giá trị credential và không đi vào M1.

Các script còn trong out là công cụ đã dùng hoặc bản chuẩn bị được giữ để truy nguyên. `pause-probe.py` và `fix-booking-memory.py` là bản chuẩn bị cũ không chạy; v2 đã dùng `pause-probe-v2.py`, sửa thực tế bằng `fix-jvm-memory.py`. Không tự chạy lại các script lịch cũ hoặc mã ca cũ.

Tất cả ghi trên laptop của lượt này nằm trong out. Repo chính chỉ đọc; chưa cập nhật STATE/LOG chính thức hoặc đóng T-058. Các file cần đưa vào repo sau này phải theo quyền Minh duyệt. Không tự gửi prompt bàn giao sang agent khác.
