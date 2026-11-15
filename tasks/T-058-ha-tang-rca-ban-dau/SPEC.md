# T-058 — Hạ tầng quan sát và RCA bản đầu trên FlashTicket

- **Trạng thái:** đã duyệt (10/11/2026, Minh: "Duyệt, tạo file")
- **Người làm:** Claude
- **Người phản biện:** Codex
- **Thuộc gói MRP:** P9b, và phần chuẩn bị của P10 — **Cổng:** không có cổng riêng; đầu ra phục vụ G6

## Mục tiêu

Nguồn chi phối:
- **DT18-NV2** và hướng dẫn của cô, "Phần 2: tích hợp vào hệ thống đặt vé" (MRP §2.1, dòng P9, P10).
- **MRP §5 P9b:** dịch vụ RCA đọc Tempo, Loki, Prometheus rồi đổi sang cùng định dạng nội bộ mà các bộ dataset dùng.
- **RQ5** (MRP §3): kết quả có giữ được trên FlashTicket không.
- **DECISIONS 09/11/2026:** RCA bản đầu chạy trên FlashTicket tới 16/11/2026.

Câu hỏi của task: FlashTicket có sinh đủ trace, metric, log để M1 bản P7 khóa chạy được không; nếu thiếu thì thiếu gì.

Loại task: **cài đặt và kiểm khả thi**, không phải đánh giá. Task chỉ bao phủ phần "chạy được" của P9b. Nó không trả lời RQ5 và không cho kết luận nào về hiệu quả của M1 trên FlashTicket. Đạt task này đủ căn cứ để soạn T-059 (kịch bản, tiêm lỗi, sổ, nền), chưa đủ để khóa bản FlashTicket.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi và nguồn | Lựa chọn cần phân xử; giải thích khác | Phép kiểm và bằng chứng | Kết quả phân xử | Phần còn thiếu, quyết định phụ thuộc |
|---|---|---|---|---|
| C1. Agent 2.33.1 có chạy với Spring Boot 4.1.1 không (TS §4.1) | Chạy được; lỗi khởi động; chạy nhưng thiếu span | Bốn điều "Cách kiểm" của TS §4.1 trên một request gateway → booking → DB/Redis/RabbitMQ | Đạt cả bốn là hỗ trợ; thiếu span JDBC/Redis/RabbitMQ là đạt một phần | Không đạt thì chuyển phương án starter (sửa pom); Minh quyết |
| C2. Dữ liệu có đáp ứng R-01–R-10 không (`results/T-040/yeu-cau-quan-sat-p9.md`) | Đáp ứng; thiếu do agent; thiếu do cấu hình; thiếu do code | Bảng từng yêu cầu: có/không, ví dụ span và log thật, lệnh truy vấn | Từng dòng: đạt, không đạt, chưa kiểm | Dòng không đạt thành việc của T-059 hoặc việc code Q6 |
| C3. Hai máy 8 GiB có đủ không (PLAN §2.1, toàn ước lượng) | Đủ; thiếu ở máy ứng dụng; thiếu ở máy kho | 1 giờ rảnh và 1 giờ tải nhẹ: RAM, CPU, drop của Collector, GB/giờ | Số đo thật thay ước lượng | Thiếu thì Minh quyết máy lớn hơn (Q11) |
| C4. M1 bản P7 khóa có chạy thẳng trên dữ liệu FlashTicket không (hợp đồng `results/T-043/hop-dong.json`) | Chạy thẳng; cần sửa adapter; thiếu đầu vào bắt buộc | 3 sự cố thử và 1 cửa sổ không lỗi; soi trung gian: số span, số nút, số cạnh, số lần rơi nhánh dự phòng | Có xếp hạng ở 4/4, hoặc danh sách đầu vào thiếu | Không dùng thứ hạng làm bằng chứng hiệu quả; 3 sự cố không đủ phân xử |

"TS" là `docs/techstack/TECHSTACK-NGHIEN-CUU.md`; "PLAN" là `docs/techstack/PLAN-TRIEN-KHAI.md`.

## Đầu vào

- **Kế hoạch:** PLAN (§5, §6.1) và TS (§4.1, §4.4, §4.7, §5).
- **Code M1:** `src/m1/` (bản P7 khóa, chỉ đọc), `results/T-043/hop-dong.json`, `results/T-037/` (mô hình nút FlashTicket).
- **Repo FlashTicket:** `D:/Project/flash-ticket-platform`, commit `1d40c97`, chỉ đọc.
- **Máy:**
  - `exp-app` (`3.27.110.61`, sau khi Minh đổi loại sang `m7i-flex.large`) và `exp-obs` (Minh tạo): được cài đặt và chạy trong phạm vi các bước dưới. Khóa: `D:\RCA-ext\keys\Hahaa123.pem`, ngoài repo.
  - Máy 84: chỉ lệnh đọc, để lấy digest ở `state/<svc>.current`. Cách truy cập ở `docs/STATE.md`.
- **Env, Minh cấp và đặt thẳng lên `exp-app`, không qua chat:**
  - 8 file `env/<svc>.env` (discovery-server, api-gateway, user, event, ticket, booking, payment, keycloak).
  - File `.env` gốc cho hạ tầng.
  - `key-ring.json` của ticket.
  - Giá trị phải khác 84: mật khẩu DB/Redis/RabbitMQ, `KC_HOSTNAME`, URL VNPay (không dùng ngrok).
- **Không dùng:** tập test và dataset giữ ngoài.

## Đầu ra

Tất cả trong `results/T-058/`:
- `moi-truong.md`: hai máy, phiên bản, cách dựng lại, lệnh đã chạy.
- `manifest-digest.json`: digest 9 image, commit repo FlashTicket, bản agent, phiên bản kho.
- `kiem-agent.md` (C1) và `kiem-telemetry.md` (C2): kèm ví dụ thật và lệnh truy vấn.
- `so-do-tai-nguyen.json` (C3): RAM, CPU, drop, GB/giờ.
- `rca-ban-dau/`: gói dữ liệu 4 cửa sổ có hash, đầu ra M1, trung gian, sổ tiêm lỗi (C4).
- `bao-cao.md`: trả lời C1–C4, phần thiếu, việc chuyển sang T-059.

## Phạm vi ghi

Chỉ được ghi vào các đường dẫn dưới đây, cộng `LOG.md` của task này và dòng của task trong `docs/STATE.md`. Ghi ra ngoài thì dừng, đề xuất.

- `results/T-058/`
- `src/m1/adapter_flashticket.py`: file mới. Không sửa `src/m1/adapter.py`, vì file đó có thể đang ghim trong manifest của các lượt cũ (chưa kiểm).
- `infra/exp/`: thư mục mới, chứa script dựng máy, script tiêm lỗi, công cụ sổ, và cấu hình kho quan sát bản thử ở `infra/exp/obs/`. Khi cấu hình kho ổn định, Minh chuyển sang repo FlashTicket (PLAN Q13).
- Trên `exp-app` và `exp-obs`: cài Docker, tạo thư mục, chạy container. Không ghi gì lên máy 84 và repo FlashTicket.

## Các bước

Phụ thuộc thật ghi trong ngoặc.

1. Lấy digest từ máy 84, ghi `manifest-digest.json`. Kiểm bằng: 9 digest đúng dạng `sha256`. (Không phụ thuộc; làm ngay.)
2. Dựng `exp-app`: Docker, `git clone` ở commit ghim, 4 hạ tầng, 9 ứng dụng bằng compose và script của nhóm. Kiểm bằng: Eureka báo UP cho mọi service; `docker inspect` khớp digest; không restart. (Cần máy 8 GiB và env.)
3. Gắn agent bằng jar tạm; chạy `otel-lgtm` trên `exp-obs`. Kiểm bằng: bốn điều TS §4.1. (Cần bước 2 và `exp-obs`.)
4. Viết adapter từ trace mẫu của bước 3. Kiểm bằng: đối chiếu quy ước dữ liệu (span gốc, đơn vị thời gian, alias tên service) với K3 và `builder.py`, theo SL39. (Cần bước 3; chạy song song bước 5.)
5. Thay bằng kho ghim phiên bản; chrony; đo 1 giờ rảnh và 1 giờ tải nhẹ. Kiểm bằng: tiêu chí H2 của PLAN §6.1 bước 8. (Cần bước 3.)
6. Kiểm R-01–R-10. Kiểm bằng: mỗi dòng có lệnh và ví dụ. (Cần bước 5.)
7. Sổ tiêm lỗi và bộ điều phối chế độ (a); 3 sự cố thử và 1 cửa sổ không lỗi; đóng gói, băm; chạy M1. Kiểm bằng: kiểm trường cấm đạt; trung gian không rỗng đồng loạt. (Cần bước 4, 5.)
8. Viết báo cáo, tự kiểm, mục LOG kết thúc, prompt bàn giao.

## Kiểm đúng đắn

- **Không cần nhãn:** chạy lại M1 trên cùng gói ra cùng kết quả; cửa sổ không lỗi là phép thử giả; đếm số lần rơi nhánh dự phòng (SL24, SL36).
- **Trạng thái đồng loạt** (toàn rỗng, toàn `NO_TARGET`): lần tới đầu vào trước khi ghi kết quả (SL39).
- **Rò nhãn:** tên lượt là mã mờ; log của Toxiproxy và Pumba bị loại khỏi Loki; RCA chạy bằng user không đọc được sổ (PLAN §5).
- **Tách nguồn lỗi:** hạ tầng, agent, adapter, phương pháp. Lỗi hạ tầng không ghi thành kết quả khoa học.
- **Không kiểm được trong task:** hiệu quả M1 (3 sự cố là quá ít); overhead của agent dưới tải cao; lỗi cần cờ trong code. Kết luận về RQ5 vì vậy vẫn OPEN, chuyển T-059, T-060.

## Tiêu chí xong

- C1–C4 mỗi câu có trả lời kèm bằng chứng. "Không đạt" hoặc "chưa phân xử" là đầu ra hợp lệ nếu đã chạy phép kiểm và nêu phần thiếu.
- Môi trường dựng lại được từ `moi-truong.md` và manifest.
- Báo cáo ghi rõ đây không phải đánh giá, và không rút kết luận về hiệu quả M1.

## Không làm

- Không sửa repo FlashTicket, không deploy lên 84, không tiêm lỗi trên 84.
- Không chạy tải cao; không dựng máy `loadgen`; không làm danh mục kịch bản đầy đủ (T-059).
- Không sửa M1, không thử thành phần mới, không chạy baseline (T-060).
- Không làm nginx, VNPay giả, cờ lỗi: đó là việc code Q6 của Minh.

## Chi phí ước lượng

- **Công agent:** 4–5 ngày, 11–16/11.
- **Máy:** khoảng 4 giờ cho các phép đo. Lượt dài nhất là 2 giờ (bước 5), vượt 1 giờ; SPEC này là lời báo trước theo luật cứng 8.
- **Tải về:** image kéo lên EC2, ước lượng 5–10 GB (chưa kiểm). Laptop chỉ nhận gói kết quả, ước lượng dưới 1 GB.
- **Lỗi giữa chừng ở bước 5** (luật 21): chỉ là đo, không sinh kết quả khoa học. Hỏng ở 10%, 50% hay 99% đều chạy lại riêng giờ bị hỏng, mất tối đa 1 giờ.
- **Lỗi ở bước 7:** dữ liệu thu trước, RCA chạy sau trên gói đã đóng. Lỗi phương pháp chỉ chạy lại RCA, tính bằng phút.

## Rủi ro và điều chưa chắc

- **Chưa kiểm:** agent với Boot 4.1.1; Docker trên Ubuntu 26.04; kéo image từ GHCR; `netem` với host network; mọi số RAM ở PLAN §2.1.
- **`deploy-service.sh` trên máy mới:** script đòi token GHCR qua stdin và kiểm sức khỏe qua Eureka. Chạy được trên máy khác 84 hay không là chưa kiểm. Hỏng thì chạy compose trực tiếp với cùng file, và ghi chỗ lệch.
- **Luồng đặt vé:** dừng ở bước tạo thanh toán vì chưa có VNPay giả. Các cạnh sau thanh toán (ticket, Saga bù trừ) không có trong dữ liệu bản đầu.
- **Mốc 16/11:** cần Minh xong đổi loại máy, tạo `exp-obs` và cấp env trong 11–12/11.

## Prompt bàn giao

Theo `docs/review-prompt.md`; prompt từng lượt nằm ở cuối mục LOG tương ứng.

## Đính chính 11/11/2026 (Minh duyệt trong chat: "tôi quyết định sử dụng oracle, không dùng aws nữa"; "duyệt dùng codex"; "duyệt ghi")

Thân SPEC ở trên giữ nguyên như lúc duyệt 10/11. Các điểm dưới đây thay phần tương ứng.

1. **Hạ tầng.** `exp-app` = Oracle `129.221.208.47` (IP nội bộ `10.0.0.158`); `exp-obs` = Oracle `213.35.116.128` (`10.0.0.215`). Cả hai `VM.Standard.A1.Flex`, ARM `aarch64`, 2 OCPU, 11 GB RAM, Ubuntu 24.04.5, vùng `ap-singapore-1`. Thay máy AWS x86. Khóa ở `D:\RCA-ext\keys\exp-app\` và `exp-obs\`.
2. **Vai trò lượt đêm 10–11/11.** Codex làm (model `gpt-6.1-sol`, toàn quyền, thư mục `D:\RCA-ext\overnight-T058`); Claude điều phối và giám sát. Vì Codex đã làm một phần task, người phản biện của T-058 cần Minh chỉ định lại (AGENTS mục 1, mục 8).
3. **Nguồn image.** Image `arm64` build ngay trên `exp-app` từ đúng commit của từng image đang chạy trên máy 84 lúc 19:46Z ngày 10/11 (`dem-2026-11-10/dieu-phoi/revisions.json`). Bảy service Spring build bỏ test. Không dùng digest của 84 (chỉ có `amd64`). Bỏ `frontend`.
4. **Env và dữ liệu.** Sinh mới trên `exp-app`, không chép từ máy 84; dữ liệu khởi tạo trống bằng script và DDL của repo FlashTicket, thêm một sự kiện thử.
5. **Máy 84.** Lượt đêm không truy cập (trừ lệnh đọc của Claude để chụp mốc và giám sát).
6. **Phạm vi ghi thêm:** `results/T-058/dem-2026-11-10/` (bản sao `out/` của lượt đêm và hồ sơ điều phối).
7. **Rút gọn so với SPEC:** đo tài nguyên 30 phút rảnh + 30 phút tải (SPEC: 1 giờ + 1 giờ); M1 chạy trên 1 cửa sổ bình thường + 1 lỗi (SPEC: 3 lỗi + 1). C1–C4 vì vậy mới trả lời một phần; xem LOG phiên 3.
