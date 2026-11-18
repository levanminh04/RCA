# T-066 bước 9 — tuyến một ca mới `e2e-001` (mã ca 7ffb2305)

Chạy 17/11/2026 12:14:26–12:45:58Z trên exp-obs từ repo lab `ab1c52c` (`/opt/rca-lab`), hệ thống FlashTicket đang chạy (bản T-062 `6b21ed55`, chưa đổi).
Lệnh: `RCA_DP_OUT=/srv/rca-lab/runs/e2e-001 python3 -B /opt/rca-lab/campaigns/runner/runner4.py thu --lich /opt/rca-lab/campaigns/schedules/e2e-t066.json` (1 chu kỳ, ô PAUSE-PAYMENT).

| Khâu | Thời điểm (UTC) | Kết quả | Bằng chứng |
|---|---|---|---|
| Tải k6 `t3-7ffb2305` (×1, 30 phút) qua khóa bộ điều khiển mới | 12:15:04 → nhận về 12:45:48 | chạy trọn; đầu ra nhận về kiểm hash (`tai-outputs.sha256`) | `nhat-ky-3.jsonl` |
| Tiêm (inj3 từ `/opt/rca-lab` trên exp-app) | fault-start 12:25:04, fault-stop 12:35:05; đầu dò t−240, t+60, t+330, hồi+60 | đủ sự kiện | `so-tiem-e2e-001.jsonl` (sổ, ghi bằng user ledger; chép về sau khi lượt xong) |
| stage → P7 (`run_m1.py`, user rca) | xong 12:39:30 | `status` OK, hai lần chạy trùng SHA | `p7-summary.json`, `ca-manifest.json` |
| Gói bổ sung (live-down theo lần dò mới nhất) | 12:39 | `m1/bo-sung/7ffb2305/` | `hash-tren-may.sha256` |
| V082 (`chay_ca.py` bản chụp, user rca) | xong 12:40:03 | hai lần trùng SHA `183a405d…`; `cau_hinh_sha256` = `451a8437…`, `ma_nguon_sha256` = `b0f79a4d…` (khớp danh sách bảo vệ) | `v082-summary.json` |
| G1 + chỉ mục (`sau_v082.py`) | xong 12:40:15 | ca có trong `chi-muc-ban.json` và `V082-V066+H8a/chi-muc.json`; `vue/`, ca, `phat-lai/` phục vụ qua `/public/rca/` của Grafana trùng hash file trên đĩa | `hash-tren-may.sha256`, LOG |

Mở trong Grafana: `/d/t065-l8b-rca?var-ban=V082-V066%2BH8a&var-ca=7ffb2305` (cần đăng nhập; agent chưa xem giao diện).

Ghi chú:
- Đây là phép kiểm đường chạy, không phải phép đánh giá. Không chấm hạng; không diễn giải nhóm hạng 1 của P7 hay V082.
- Chỉ mục ghi `nguon: "dev3"` cho ca mới vì bộ chuyển dùng lại nhánh dev3 của T-065; tên này sai nghĩa với ca mới (xem LOG, đề xuất sửa).
- Gói ca `runs/e2e-001/ca/7ffb2305.tgz` và mọi đầu ra giữ trên exp-obs (luật cứng 10); hash ở `hash-tren-may.sha256`.
