# Brief C1 cho Codex — máy tải k6 (T-062, chặng 2)

Bạn là Codex, người làm bước C1 của task T-062 trong repo `D:\RCA-flashticket`. Đọc `AGENTS.md` mục 3 và `tasks/T-062-dem-chang-1-4/SPEC.md` (nhất là "Luật cứng của lượt" 1–10 và bảng máy) trước khi làm. Phiên Claude điều phối giao việc này; Minh đang ngủ và đã duyệt cho bạn full access trong phạm vi dưới đây.


## SỬA ĐỔI v2 (phiên điều phối tiếp quản, 18:35Z 11/11) — đọc trước, đè lên phần dưới khi mâu thuẫn

- Kiểm lúc 18:30Z từ máy tải: `:8080` vào được (302); `:8081` bị từ chối (iptables INPUT trên exp-app, Gateway chạy host network). Phiên điều phối không mở được iptables đêm nay (bị chặn quyền). **Không thử mở cổng, không tìm cách vòng.**
- Vì vậy dùng phương án dự phòng của SPEC: **tải thật đêm nay chạy trên `exp-obs`** (`ubuntu@213.35.116.128`, khóa `D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key`, known_hosts `D:/RCA-ext/overnight-T058/out/known_hosts`), cùng VCN, đích nội bộ `http://10.0.0.158:8081` (Gateway) và `http://10.0.0.158:8080` (Keycloak; issuer khớp vì KC_HOSTNAME ghim 10.0.0.158). Đã kiểm từ exp-obs: gw 200, kc 200.
- Trên `exp-obs` bạn CHỈ được: tạo `/opt/rca-tai/` và chạy container k6 tên bắt đầu `rca-tai-` (image k6 ghim digest). **Cấm** đụng container/compose/cấu hình của stack quan sát (Grafana, Prometheus, Loki, Tempo, collector), thư mục `/opt/flash-ticket-obs/`, iptables. Ghi thay đổi trên exp-obs vào `results/T-062/tai/thay-doi-may-tai.md` (ghi rõ máy).
- Máy tải AWS `3.24.8.49`: vẫn làm bước 1 (Docker, k6 cùng digest, chrony) để sẵn sàng khi Minh mở 8081; kiểm cổng 8081 một lần khi bắt đầu, một lần khi kết thúc, ghi `ket-noi.md`. Không chờ 30 phút.
- Kịch bản k6 và `chay-tai.ps1` phải nhận tham số máy: `-May obs|tai` (mặc định `obs`), URL gốc tương ứng (`obs`: 10.0.0.158; `tai`: 129.221.208.47). Đầu ra trên máy `/opt/rca-tai/out/<mã mờ>/`.
- Ghi đồng hồ: kiểm offset giờ của exp-obs (chronyc/timedatectl, chỉ đọc) và ghi vào `may-tai.md`.
- Laptop là Windows: gọi ssh bằng `C:/Program Files/Git/usr/bin/ssh.exe`; mẫu bọc lệnh ở `results/T-058/dem-2026-11-10/remote.ps1` (chỉ đọc, có thể chép ý vào script của bạn).

## Mục tiêu

Máy tải AWS `3.24.8.49` chạy k6 theo một kịch bản cố định, tự làm mới token Keycloak, chạy thử 5 phút ổn định, số liệu lưu trong `results/T-062/tai/`.

## Máy

- Máy tải: `ssh -i D:/RCA-ext/keys/Hahaa123.pem -o UserKnownHostsFile=D:/RCA-ext/keys/known_hosts -o BatchMode=yes ubuntu@3.24.8.49` (x86_64, 2 vCPU, 7,7 GB). **Bạn là agent duy nhất được thay đổi máy này.**
- Đích tải: Gateway của `exp-app` `http://129.221.208.47:8081`, Keycloak `http://129.221.208.47:8080` (realm `flash-ticket`, client công khai `frontend`, token sống 300 s, có refresh token; `KC_HOSTNAME` ghim `10.0.0.158` nên trang đăng nhập/issuer trỏ địa chỉ nội bộ).
- `exp-app` (`ubuntu@129.221.208.47`, khóa `D:/RCA-ext/keys/exp-app/ssh-key-2026-11-10 (1).key`, known_hosts `D:/RCA-ext/overnight-T058/out/known_hosts`): **chỉ được chạy lệnh đọc**, không ghi file, không đổi container/iptables/cấu hình. Phiên Claude điều phối giữ máy này. Tài khoản thử nằm ở `/opt/flash-ticket-app/env/test-users.json` trên `exp-app`; cách đăng nhập PKCE mẫu ở `results/T-058/dem-2026-11-10/auth.py` (hàm `role_token('BUYER')`).

## Việc

1. Máy tải: cài Docker (repo chính thức), k6 **ghim phiên bản** (image `grafana/k6:<phiên bản cụ thể>` kèm digest, hoặc binary .deb ghim), `chrony` đồng bộ giờ. Ghi phiên bản, digest, offset chrony vào `results/T-062/tai/may-tai.md`. Thư mục làm việc trên máy: `/opt/rca-tai/` (tạo mới).
2. Kết nối: kiểm từ máy tải tới `129.221.208.47:8081` và `:8080` (curl, timeout ngắn). Nếu bị chặn, ghi rõ vào `results/T-062/tai/ket-noi.md` (giờ UTC, lệnh, kết quả) rồi **thử lại mỗi 5 phút tối đa 30 phút**. Mở cổng phía Oracle là việc của Minh (Security List) và Claude (`iptables` trên exp-app) — bạn không đụng. Nếu sau 30 phút vẫn chặn: ghi "C1 CHẶN: cổng" vào file kết quả và dừng phần cần mạng; phần cài đặt vẫn làm xong.
3. Token: lấy token người mua lần đầu (access + refresh) bằng luồng PKCE như `auth.py`. Cách được phép: chạy một đoạn Python **chỉ đọc** trên `exp-app` qua SSH (in-memory, không ghi file trên exp-app), đưa thẳng refresh token sang máy tải bằng pipe (`ssh exp-app ... | ssh may-tai 'umask 077; cat > /opt/rca-tai/secret/refresh'`). **Không bao giờ in token/mật khẩu ra màn hình, log, file trong repo.** Kịch bản k6 tự làm mới access token bằng `grant_type=refresh_token` tới `http://129.221.208.47:8080/realms/flash-ticket/protocol/openid-connect/token` trước khi hết 300 s (ví dụ mỗi VU làm mới khi token già hơn 200 s). Nếu cổng 8080 không vào được từ máy tải: dùng phương án dự phòng — một vòng lặp trên laptop (PowerShell nền) mỗi 3 phút lấy access token mới qua exp-app và ghi đè `/opt/rca-tai/secret/access` trên máy tải; k6 đọc lại file đó (dùng `k6/experimental/fs` hoặc chia lượt chạy ngắn); ghi rõ phương án đã dùng. Phiên Keycloak tối đa 10 giờ: ghi cách đăng nhập lại.
4. Kịch bản: `results/T-062/tai/k6/workload-t062.js`, dựa trên `D:/Project/flash-ticket-platform/deploy/rca-test/workload.js` (chỉ đọc file đó; không sửa repo FlashTicket). Giữ hỗn hợp cố định 50/25/15/10 (GET event / order / order payment / order tickets), executor `constant-arrival-rate`, thêm làm mới token. Nhịp mặc định `FT_LOAD_RATE=5` req/s (tham số, ghi vào file cấu hình `results/T-062/tai/k6/cau-hinh.json`). **Không gửi tên ca, trạng thái tiêm lỗi hay nhãn nào tới ứng dụng.** Xuất kết quả k6 dạng JSON/CSV (`--out json=` hoặc `csv=`) và summary.
5. Fixture: `results/T-062/tai/k6/fixtures.json` gồm `events[] {eventId}` và `orders[] {orderId}` của người mua thử. Lấy event qua API công khai (`GET /api/v1/events`, ví dụ event `68bbd408-d7c0-4236-b139-0ecf9cd5d826` từ `results/T-058/dem-2026-11-10/seed-fixture.json`). Đơn: lấy đơn có sẵn của người mua qua API đọc; nếu chưa có đơn nào thì **chờ** tới khi file `results/T-062/ha-tang/A2-XONG` tồn tại rồi mới tạo tối đa 3 đơn qua API đặt vé bình thường (có idempotency key), ghi lại orderId. Không sửa DB trực tiếp.
6. Chạy thử 5 phút ở 5 req/s **chỉ sau khi** `results/T-062/ha-tang/A2-XONG` tồn tại (Claude đang triển khai lại exp-app; tải trong lúc đó làm bẩn dữ liệu). Kiểm file đó mỗi 5 phút, chờ tối đa 8 giờ. Trong lúc chờ, làm xong 1–5. Sau chạy thử: ghi `results/T-062/tai/chay-thu-5p.md` (tỷ lệ 2xx/4xx/429/5xx theo route, p95, số lần làm mới token, có 401 không) và lưu dữ liệu thô k6 vào `results/T-062/tai/chay-thu-5p/`.
7. Script khởi động/dừng tải dùng cho bộ chạy E1: `results/T-062/tai/chay-tai.ps1` với hai lệnh `Start-Tai -Seconds <n> -Rate <r> -Tag <mã mờ>` và `Stop-Tai`, chạy k6 trong container nền trên máy tải, đầu ra `/opt/rca-tai/out/<mã mờ>/`, và `Receive-Tai -Tag` chép về `results/T-062/tai/out/<mã mờ>/`. Mã mờ do bộ chạy cấp, không mang nghĩa.

## Luật cứng (tóm tắt SPEC, bắt buộc)

1. Không push/merge gì, không đụng repo FlashTicket hay GitHub.
2. Không chạm máy 84 (`52.64.237.84`) hay khóa `FlashTicket-Control-Diagnosis.ppk`.
3. Chỉ ghi trong `results/T-062/tai/` và `results/T-062/codex/`. Không sửa `src/`, `docs/`, `results/T-0xx/` khác, `tasks/`.
4. Không đụng M1, không đọc dữ liệu khóa (`data/locked/`), không tải > 5 GB.
5. Không ghi sổ tiêm lỗi, không đọc nhật ký điều khiển tiêm lỗi.
6. Không xóa dữ liệu/container của người khác. Mọi thay đổi trên máy tải ghi vào `results/T-062/tai/thay-doi-may-tai.md` (lệnh, giờ UTC).
7. Không in mật khẩu/token vào bất kỳ file hay log nào.
8. Nếu tồn tại `D:/RCA-overnight/STOP` thì dừng ngay, ghi trạng thái.
9. Lỗi hạ tầng: ghi lại, không xóa dữ liệu đã thu, không đoán.
10. `exp-app`, `exp-obs`: chỉ đọc.

## Báo xong

Kết thúc bằng một báo cáo ngắn (file `-o` của lệnh này) gồm: đã làm gì; file đã tạo; kiểm đã chạy và kết quả (kèm số); phần chưa làm/bị chặn và vì sao; lệnh để bộ chạy E1 dùng tải. Dòng đầu tiên của báo cáo là một trong: `C1 XONG`, `C1 XONG MỘT PHẦN`, `C1 CHẶN`.
