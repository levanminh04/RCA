Bạn là Codex, người làm của lượt chạy đêm task T-058 (dự án RCA trên hệ thống bán vé FlashTicket). Claude điều phối và giám sát. Minh đang ngủ; không hỏi Minh.

Đọc theo thứ tự, trước khi chạy lệnh nào:
1. `AGENTS.md` trong thư mục hiện tại (luật lượt đêm; ưu tiên khi bàn về quyền ghi).
2. `inputs/AGENTS-repo-RCA.md` (luật chung của repo RCA).
3. `inputs/ban-giao-chay-dem.md` (kế hoạch 6 chặng; mục 6 là văn phong tài liệu).
4. `inputs/thay-doi-ha-tang-2026-11-11.md`, `inputs/SPEC.md`, `inputs/revisions.json`.
5. Khi cần: `inputs/TECHSTACK-NGHIEN-CUU.md` (§4.1 agent, §4.4 và §6.1, §6.2 Collector, §5 phiên bản ghim), `inputs/PLAN-TRIEN-KHAI.md` (§5 sổ tiêm lỗi, §6.1), `inputs/LESSONS.md`, `inputs/yeu-cau-quan-sat-p9.md` (R-01–R-10).

Kế hoạch là 6 chặng trong `inputs/ban-giao-chay-dem.md` mục 4, với các **sửa đổi bắt buộc** sau (Claude thu hẹp để giảm rủi ro; chúng thay chỗ tương ứng trong file bàn giao):

A. **Không dùng GitHub CI, không push gì.** Chặng 2 chỉ dùng "Nguồn B": build image ARM ngay trên `exp-app`. Với mỗi service trong `inputs/revisions.json`, `git checkout` đúng `commit` của nó (dùng `git worktree` trong bản clone trên `exp-app`), build JAR bằng Maven wrapper của service (`./mvnw -B -ntp -DskipTests package`; Keycloak: `mvn -B -ntp clean verify` hoặc tương đương trong `services/keycloak-spi`, cần Maven), rồi `docker build` bằng Dockerfile của service. Tên image `ft-local/<service>:arm64-<8 ký tự đầu của commit>`. Bỏ `frontend`. Ghi rõ trong tài liệu là build bỏ test.

B. **Không truy cập máy 84.** Env và bí mật **sinh mới** trên `exp-app`, không chép từ đâu:
   - Lấy danh sách biến từ `.env.example` trong repo (gốc và từng service), `deploy/app/README.md` (bảng biến khác bản local), `deploy/README.md`.
   - Mật khẩu, client secret sinh ngẫu nhiên bằng `openssl rand`; file env mode 600, nằm ở `/opt/flash-ticket-app/env/<svc>.env` và `.env` gốc trong bản clone trên `exp-app`. Không in giá trị.
   - `KC_HOSTNAME` và `KEYCLOAK_ISSUER_URI` của gateway phải khớp nhau và phải là địa chỉ mà các service trên `exp-app` gọi được.
   - Không chạy ngrok. Payment: URL VNPay để giá trị giả; ghi rõ luồng đặt vé dừng ở bước thanh toán.
   - `key-ring.json` của ticket: tạo mới theo đúng định dạng code của ticket-service đọc (đọc code để biết định dạng); nếu không làm được thì ghi vào `out/CAN-MINH-QUYET.md` và cho ticket-service chạy sau cùng.

C. **Dữ liệu khởi tạo trống** (phương án (b) trong file bàn giao): compose hạ tầng của repo (`deploy/docker-compose.postgresql.yml`, `redis.yml`, `rabbitmq.yml`, `deploy/mongodb/`), script `deploy/postgres/00-business-databases.sh`, DDL `docs/architecture/data/postgres/`, realm `deploy/keycloak/import/flash-ticket-realm.json`. Cần dữ liệu tối thiểu để gọi API (ví dụ một sự kiện, một người dùng thử): tạo qua API hoặc SQL, ghi lại cách tạo.

D. Bố trí thư mục trên `exp-app` giống máy 84: `/opt/flash-ticket-app/{compose,env,state,secrets/ticket-qr}`, `/opt/flash-ticket-infra`. Ứng dụng chạy bằng `deploy/app/*.yml` của nhóm (`IMAGE=<image arm64>`, `docker compose -f ... -p flash-ticket-<svc> up -d`); bản compose có thêm mount agent thì để riêng trong `/opt/flash-ticket-app/compose-exp/`, không sửa file của repo.

E. **Kho quan sát:** chạy `grafana/otel-lgtm:0.40.0` trên `exp-obs` trước để có kết quả sớm; nếu còn thời gian thì chuyển sang kho ghim riêng (Collector 0.165.0, Prometheus v3.16.0, Loki 3.7.9, Tempo 3.1.1, Grafana 13.3.0). Collector tại chỗ trên `exp-app` (`otel/opentelemetry-collector-contrib:0.165.0`, `network_mode: host`) theo TECHSTACK §6.2, xuất sang `10.0.0.215`. Mở `iptables` trên hai máy cho `10.0.0.0/24`, và lưu để còn sau khi khởi động lại. Mọi cổng web chỉ nghe nội bộ.

F. **Agent:** `opentelemetry-javaagent.jar` v2.33.1, biến theo TECHSTACK §6.1 thêm vào file env của từng service; `JAVA_TOOL_OPTIONS` phải giữ `-XX:MaxRAMPercentage=50.0 -Duser.timezone=UTC`.

G. **M1 (chặng 5, mục tiêu thêm, không bắt buộc):** chép `src/` của repo RCA (chỉ đọc trên laptop) lên `exp-obs`, dựng Python 3.12 với `results/T-044/requirements-m1.txt` và `-c results/T-044/freeze-m1.txt`. Bộ đọc mới viết ở `out/src/m1/adapter_flashticket.py` (và bản trên `exp-obs`), không sửa file nào của repo. Lỗi tiêm thử chỉ là `docker pause`/`docker stop` một service trên `exp-app`; mốc ghi vào `out/so-tiem-loi.jsonl`, M1 không được đọc file này.

Thời gian: bây giờ khoảng 19:50Z ngày 10/11/2026 (02:50 giờ Việt Nam). **Từ 23:15Z** ngừng việc mới, viết `out/bao-cao-sang.md`, cập nhật `out/huong-dan-trien-khai.md`, tạo `out/DONE.md` trước **23:40Z**. Kiểm giờ bằng `date -u`.

Thứ tự ưu tiên khi thiếu thời gian: chặng 1 → 2 → 3 (FlashTicket chạy, gọi được API) → 4 (thấy trace, log, metric trên Grafana) → tài liệu → 5. Một chặng hỏng thì ghi lại và làm phần không phụ thuộc. Thử cùng một chỗ 3 lần không được thì dừng chỗ đó.

Lệnh chạy lâu (Maven, docker build, kéo image) chạy trong `tmux` hoặc `nohup` trên máy Oracle, ghi log ra file trên máy, để mất kết nối SSH không làm hỏng việc. Cập nhật `out/CHECKPOINT.md` thường xuyên: nếu bạn hết usage giữa chừng, lượt sau (của bạn hoặc của Claude) làm tiếp từ đó.

Bắt đầu: ghi dòng mở phiên vào `out/LOG-dem.md`, rồi làm chặng 1.
