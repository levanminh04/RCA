# Lời nhắn tiếp cho L1 (Claude điều phối, 13/11/2026 ~05:15Z) — chuyển lệnh tải sang Python chạy trên exp-obs

Minh quyết (docs/DECISIONS.md, mục "Chạy bộ điều phối đợt thu trên `exp-obs`"): bộ điều phối đợt thu chạy trên `exp-obs`, không phụ thuộc mạng laptop (mạng laptop mất ~40 phút lúc 04:19Z). Tính đúng đắn trên hết.

**Việc:** viết `results/T-062/tai-2/tai_linux.py` (Python 3.12, chỉ thư viện chuẩn, chạy trên `exp-obs` Ubuntu, user `ubuntu`) **tương đương đúng hành vi** các lệnh hiện hành của bạn cho kịch bản `hanh-trinh`: `Test-L1Duong` (gồm làm mới token pool qua `exp-app`), `Start-Tai -Scenario hanh-trinh -Seconds N -Tag T [-BuocTai S -Multiplier K]`, `Get-Tai`, `Stop-Tai`, `Receive-Tai`. Giữ nguyên: kiểm không có container `rca-tai-` đang chạy, kiểm hạn token với `BuocTai`, cùng image/cấu hình/script k6 (đọc từ bản sao trên exp-obs, kiểm hash với file trong repo), cùng cách chép đầu ra và kiểm hash. Bí mật không in, không ghi ra ngoài các file bí mật hiện có.
- Giao diện: `python3 tai_linux.py <test-duong|start|get|stop|receive> [--tag T --seconds N --buoc-tai S --multiplier K]`, in **một dòng JSON** kết quả, mã thoát ≠ 0 khi lỗi. `receive` chép về `~/rca-dieu-phoi/tai-out/<tag>/` trên exp-obs và kiểm hash.
- Khóa trên exp-obs (Claude đã đặt, quyền 600): `~/rca-dieu-phoi/keys/exp-app.key` (ubuntu@129.221.208.47), `~/rca-dieu-phoi/keys/may-tai.pem` (ubuntu@3.24.8.49), `~/rca-dieu-phoi/keys/known_hosts`. Không chép khóa đi nơi khác, không in nội dung.
- Bạn được ghi trên exp-obs **chỉ** trong `~/rca-dieu-phoi/` (mã, bản sao k6, `tai-out/`). Ngoài ra giữ quyền cũ trên máy tải/exp-app của phụ lục 2.
- **Kiểm:** `test-duong` đạt; một lượt ngắn `start --seconds 150` (không bậc) và một lượt `--seconds 180 --buoc-tai 90 --multiplier 3`, đều chạy từ exp-obs, `get` tới khi xong, `receive` khớp hash, so số hành trình/lỗi/401/dropped với lượt PowerShell tương đương. Ghi `results/T-062/tai-2/BAN-GIAO-4-linux.md`. Trong lúc bạn kiểm, Claude không chạy tải.
- Không sửa bản PowerShell (giữ làm lịch sử). Không sửa code nghiệp vụ, không mở firewall.

Báo xong như cũ (dòng đầu `L1 XONG` / `L1 XONG MỘT PHẦN` / `L1 CHẶN`).
