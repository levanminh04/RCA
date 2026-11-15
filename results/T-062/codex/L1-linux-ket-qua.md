L1 XONG

Đã chuyển năm lệnh tải hanh-trinh sang tai_linux.py, stdlib Python3.12 trên exp-obs ~/rca-dieu-phoi/. Quyết định nơi chạy ở docs/DECISIONS.md, mục Chạy bộ điều phối đợt thu trên exp-obs. Không thay quyết định nghiên cứu, cấu hình k6, nghiệp vụ hoặc firewall. Không commit/push. 17 nguồn PowerShell cũ nguyên hash.

Đầu ra: results/T-062/tai-2/tai_linux.py; trien-khai-linux.ps1; linux-source-manifest.json; BAN-GIAO-4-linux.md; PROMPT-CLAUDE-linux.md; linux/ (script kiểm, báo cáo JSON/CSV, lỗi đã giữ, các bản nguồn/pin, manifest-linux.json); out/l1linux20261113a,b và out/l1ps20261113a,b. Nối CHECKPOINT.md, thay-doi-may.md, results/T-062/ha-tang/thay-doi.md. Hàm PowerShell lịch sử cập nhật tunnel-state.json là trạng thái chạy, không sửa source.

Linux150: 180 hành trình/36 mua/773 gateway. PS150: 181/36/779. Linux180 bậc90x3: 433/88/1869. PS tương ứng: 434/88/1880. Cả bốn 0 lỗi hành trình/401/dropped, exit0, không OOM, 48 hash gốc khớp, gateway thiếu/lệch0. Cấu hình Docker thực từng cặp bằng nhau. Chênh1 hành trình ở mỗi cặp có thêm lượt xem PS tại 150.001s/180.001s; còn lại chênh poll. Không đặt ngưỡng lưu lượng. Nguồn số linux/check/comparison.json, comparison-routes.csv, docker-launches.json; kiểm local linux/final-local-check.json.

11 kiểm hợp đồng đạt. Một lỗi ở bước ghép lệnh sau đo đã sửa: SSH con lấy stdin caller. Giữ collect-attempt-1.txt, stdin-regression.json, nguồn/pin v1-v3. Chỉ nhận/kiểm lại, không phát lại tải. Bản cuối kiểm ghép get/start từ chối máy bận/stop không tồn tại và caller tiếp tục; bằng chứng linux/check/composed-cli.json. Driver hai lượt Linux sống độc lập parent1; lệnh start trả sau Docker -d.

EXP-APP-XONG cũ còn nguyên. Mock/tunnel không đổi cấu hình, không phải restart; chỉ cấp pool tại file bí mật cũ. Preflight cuối 05:40:47Z: health200, mock sống, tunnel parent1, pool20 BUYER 0600, access286s/refresh1786s lúc kiểm. Start luôn cấp mới. Chìa khóa không chép, token không ghi trên exp-obs. Bốn container L1 đã exited. Khi đóng gói 05:44Z có container tải mới ngoài L1; guard từ chối start, không dừng hoặc sửa container đó. Lỗi503/504 pilot cũ vẫn theo bàn giao3; việc chuyển controller không giải quyết cơ chế đó.

Claude tiếp nhận vào runner; đánh giá chênh lệch đã báo. Không còn bước cài/kiểm của yêu cầu Linux chưa làm. Chưa chạy đợt thu chính hoặc M1. Prompt kiểm độc lập ở PROMPT-CLAUDE-linux.md. Đề xuất nội dung commit khi điều phối trình lưu: feat(T-062): add verified exp-obs load controller; chưa thực hiện commit.

Lệnh bộ chạy:
cd ~/rca-dieu-phoi
python3 tai_linux.py test-duong
python3 tai_linux.py start --tag ma-moi --seconds 1800 --buoc-tai 600 --multiplier 3
python3 tai_linux.py get --tag ma-moi
python3 tai_linux.py receive --tag ma-moi
python3 tai_linux.py stop --tag ma-moi

Tiếp nhận: đọc BAN-GIAO-4-linux.md, linux/huong-dan-linux.md, CHECKPOINT.md. Kiểm linux-source-manifest.json và linux/manifest-linux.json trước khi dùng. STOP và marker bảo trì của runner ở ~/rca-dieu-phoi/. Lệnh công việc cuối: ghép CLI, xác nhận máy trống và nguồn triển khai khớp; kiểm 48 hash/17PS, quét bí mật, ghi manifest bàn giao. UTC kết thúc bản ghi: 2026-11-13T05:45:24.6601113Z.