# T-072 — W4b: luật cảnh báo Grafana, chọn ngưỡng và đo báo động giả

- **Trạng thái:** đã duyệt triển khai 20/11/2026 theo quyền Minh cho phiên điều phối (SPEC T-070), **trừ** các mục "chờ Minh". Soạn bởi phiên điều phối T-070.
- **Người làm:** Claude (phiên `luat-w4`, mức High).
- **Người phản biện:** Codex.
- **Thuộc gói MRP:** P9, P10 — **Cổng:** chuẩn bị G6.

## Mục tiêu

Kế hoạch giai đoạn 2 §8.2 W4: "Luật cảnh báo Grafana bằng file (`provisioning/alerting/`): lỗi, p95 theo route ở gateway; liveness theo 'lần dò mới nhất'. Ngưỡng chọn trên [khoảng] nền 1, đo báo động giả trên [khoảng] nền 2. Khai trước quy tắc gom cảnh báo. Xong khi: báo động giả dưới ngưỡng khai trước; webhook chạy." Đây là mức phát hiện thứ nhất (MRP §2.3, M-38) và là đầu vào t̂ của chế độ (b) (W5). Độ đo phát hiện đầy đủ (Precision/Recall/F1, độ trễ) thuộc W6–W7, không thuộc task này.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Giải thích khác | Phép kiểm | Phần còn mở |
|---|---|---|---|
| "p95 theo route ở gateway" tính trên chuỗi nào? | Nhãn `http_route` của `api-gateway` là mã route (`booking`, `event`, `payment`, `ticket`, `user`, health, rỗng) trong một giờ đã truy vấn 20/11; có thể khác ở giờ khác | Liệt kê nhãn trên dữ liệu đã xuất của T-067/T-069 và một truy vấn nhẹ ngoài E2/E4; chốt biểu thức, nhãn, nhịp đánh giá, khoảng nhìn lùi trước E2 | Mức route của gateway (không phải từng đường dẫn API) là lựa chọn quan trọng → đề xuất mục WHY (Minh duyệt, R2) |
| Luật có báo động giả dưới ngưỡng khai trước trên giờ khỏe ×1 không? | DB tích lũy làm p95 trôi; flash làm suy giảm thật; mất quan sát | Ngưỡng chọn bằng **quy tắc khai trước** chỉ trên E2; đo trên E4 sau giờ luật có hiệu lực; mẫu số theo phân loại phút của T-071 | Ngưỡng chấp nhận **chờ Minh (R5)**, ứng viên ≤ 1 sự cố / 6 giờ khỏe ×1 |
| Grafana đánh giá luật giống bộ chấm offline không? | Khác nhịp, khác `for`, khác xử lý thiếu dữ liệu | Tín hiệu dương có kiểm soát ở E3, ngoài khoảng chấm; so trạng thái luật với bộ chấm offline trên cùng chuỗi | — |

## Đầu vào

- Dữ liệu đã có (chỉ đọc file): `results/T-067/tai-1-gio.md` và đầu ra liên quan; `results/T-069/thu/` (ca khỏe ×1, ×3, flash `124242f0`); `results/T-069/phan-tich/troi-trong-luot.txt`.
- Repo lab `407b4f5`: `observability/` (compose gắn `./grafana/provisioning`), `campaigns/runner/xuat_bo_sung.py` (kênh `live-down` theo lần dò mới nhất, WHY-99).
- Hợp đồng `tasks/T-070-dieu-phoi-giai-doan-2/HOP-DONG.md` (I1, I2, I3, I7, I11, I12); `LICH-MAY.md` (Grafana chỉ ở S2).
- `docs/WHY.md` WHY-99; `docs/MRP.md` §2.3; T-059 SPEC (tiêu chí flash khỏe).

## Đầu ra

- `results/T-072/bieu-thuc.json`: biểu thức PromQL từng luật, nhãn, `eval_interval`, `for`, khoảng nhìn lùi, xử lý thiếu dữ liệu, liveness ba trạng thái. **Phải có trước E2** (cổng E2 điều kiện 3).
- `results/T-072/quy-tac-gom.json`: gom cảnh báo thành sự cố; cách đếm sự cố vắt qua biên lượt.
- `results/T-072/quy-tac-chon-nguong.json`: quy tắc tính ngưỡng từ dữ liệu E2, khai trước E2; sha256 ghi LOG trước khi T-071 phát E2.
- `results/T-072/i1-schema.json`: đề xuất bản ghi cảnh báo theo I1 cho T-073.
- `results/T-072/cham_offline.py`: bộ chấm offline; kiểm trên dữ liệu T-067/T-069 (chỉ để kiểm code, không để chọn ngưỡng).
- Sau E2: `nguong.json` (tính máy móc theo quy tắc); file luật ở worktree lab `observability/grafana/provisioning/alerting/`; bộ nhận webhook nhẹ.
- Sau E3: `e3.md` (giờ luật có hiệu lực, kết quả tín hiệu dương, khớp offline).
- Sau E4: `bang-bao-dong-gia.md/.json` theo mức tải và loại phút; kết luận so ngưỡng R5.

## Phạm vi ghi

Ngoài `LOG.md` của task này và dòng T-072 trong `docs/STATE.md`:
- `results/T-072/`.
- Repo lab: worktree `D:/Project/rca-lab-wt/T-072` nhánh `t072-luat` từ `407b4f5`: `observability/grafana/provisioning/alerting/` (mới), bộ nhận webhook nhẹ (đường dẫn trong worktree, ghi ở LOG). Không commit/push khi Minh chưa duyệt.
- Khung S2 (khi điều phối mở): exp-obs `/opt/rca-lab` checkout commit luật đã duyệt (I7), tải lại provisioning/khởi động lại Grafana theo cách ghi trong LOG; bộ nhận webhook nhẹ chạy tạm ở exp-obs `/srv/rca-lab/runs/t072-*`.

**Không sửa:** dashboard hiện có, datasource, file của T-068, lõi M1, bộ tải.

## Các bước

1. Khảo sát nhãn và chuỗi trên dữ liệu đã có; truy vấn nhẹ Prometheus chỉ khi ngoài E2/E4 (I11). Chốt `bieu-thuc.json`, `quy-tac-gom.json`; báo điều phối để T-071 kiểm xuất được. — kiểm bằng: mỗi chuỗi có mẫu ở mọi phút của cửa sổ thử.
2. Viết `cham_offline.py`; kiểm trên dữ liệu T-067/T-069 (số sự cố, phút có dữ liệu); phép thử giả: chèn bước nhảy giả vào chuỗi → luật phải bắt.
3. Viết `quy-tac-chon-nguong.json`, `i1-schema.json`; ghi sha256 vào LOG; báo điều phối (cổng E2).
4. Viết file luật provisioning và bộ nhận nhẹ ở worktree; kiểm cú pháp provisioning bằng công cụ của Grafana nếu có (offline).
5. Sau E2 (dữ liệu từ T-071): tính `nguong.json` máy móc; điền vào luật; trình diff + commit đề xuất qua điều phối (Minh duyệt).
6. E3 (S2): nạp luật, xác nhận luật được đánh giá, ghi giờ hiệu lực, tín hiệu dương có kiểm soát ngoài khoảng chấm, kiểm webhook tới bộ nhận nhẹ. Cách tạo tín hiệu dương: đề xuất trong LOG (ví dụ một luật thử ngưỡng thấp tạm thời), điều phối duyệt trước.
7. Sau E4: chấm, bảng theo mức tải và loại phút; đề xuất mục WHY.

## Kiểm đúng đắn

- Ngưỡng tính máy móc từ quy tắc khai trước; đổi sau khi xem E4 → ghi là sửa sau, giữ kết quả lần đầu, kiểm bản sửa trên khoảng mới (`thong-nhat.md` §1.3).
- Phép thử giả cho bộ chấm; so trạng thái luật Grafana với bộ chấm offline ở E3.
- Không trộn phút flash, biên, mất quan sát vào mẫu số khỏe ×1.

## Tiêu chí xong

1. Biểu thức, quy tắc gom, quy tắc chọn ngưỡng có hash trước E2.
2. Luật nạp ở E3, giờ hiệu lực ghi; webhook kiểm bằng tín hiệu dương ngoài khoảng chấm.
3. Báo động giả trên E4 theo mức tải, so ngưỡng R5; kết luận đạt / không đạt / chưa đủ giờ khỏe.

## Không làm

Độ đo phát hiện đầy đủ (W6–W7); dịch vụ RCA (T-073); đổi dashboard; thu tải (T-071).

## Chi phí ước lượng

Không giờ máy ngoài S2 (ước dưới 1 giờ, đo thật). Phụ thuộc thời gian E2, E4 của T-071.

## Rủi ro và điều chưa chắc

- Nhãn route có thể đổi theo phiên bản gateway [chưa kiểm ngoài một giờ 20/11].
- Cách Grafana tải lại provisioning luật (API hay khởi động lại) [chưa kiểm]; khởi động lại Grafana làm gián đoạn đánh giá luật — ghi giờ.

## Prompt bàn giao

Ở `LOG.md`, mục cuối mỗi lượt.
