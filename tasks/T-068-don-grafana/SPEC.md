# T-068 — Dọn và dựng lại giao diện Grafana

- **Trạng thái:** đã duyệt (18/11/2026, bản 4)
- **Người làm:** Claude
- **Người phản biện:** Codex
- **Thuộc gói MRP:** P10 (demo) — **Cổng:** chuẩn bị G6

Lịch sử soạn: bốn bản trình trong chat 18/11/2026. Codex soát bản 1 (6 điểm chặn), bản 2 (5 điểm chặn), bản 3 (2 điểm chặn); Claude kiểm từng điểm (tất cả đúng, R4 đúng một phần). Bản 4 hợp nhất, thay toàn bộ bản 1–3. Minh duyệt bản 4 ("Duyệt bản 4"), gồm commit và push repo lab trong phạm vi ghi.

## Mục tiêu

- DT18: "mô hình đồ thị phụ thuộc", "giao diện minh họa kết quả phân tích".
- MRP §P10: demo báo sự cố → đồ thị con bất thường → nguyên nhân.
- Minh (18/11): dọn Grafana "sạch đẹp nhất có thể"; hỏi vì sao ca V082 không có đồ thị mức dịch vụ.

Task cài đặt giao diện. T-068 chỉ kiểm hiển thị đồ thị và bằng chứng; không kết luận lợi ích của việc dùng quan hệ.

## Lựa chọn chính

**Vai trò tính toán của đồ thị dịch vụ (luật 18): chỉ hiển thị.**

- **Nút:** service và thực thể hạ tầng của ca. Màu theo `ranking_rows` của đúng cặp bản + ca. Hiện cho cả P7, V071, V082. Ca `LOI_CHAY` hiện "không có đầu ra".
- **Cạnh liên dịch vụ:** gộp `canh_thao_tac` (span cha–con) theo chủ nguồn → chủ đích. Nhãn: số quan hệ quan sát được ở cửa sổ nền và cửa sổ sự cố.
- **Cạnh hạ tầng:** chỉ vẽ khi `dich_quan_sat` ánh xạ được tới thực thể trong `classes` theo bảng ánh xạ khai trước, có căn cứ là cấu hình hoặc inventory. Chỉ thể hiện sự có mặt, không ghi số. Lý do: 150 dòng thao tác có nhiều đích; cùng một địa chỉ xuất hiện ở SQL, cache và HTTP. Đích không ánh xạ được thì không vẽ và ghi số lượng.
- **Chú thích panel:** "cạnh là quan sát trace, không phải đầu ra phương pháp". Bảng `region` giữ riêng.

**Nguồn.** Bản gốc dashboard: JSON tại commit lab `ab1c52c` (trùng `results/T-065/grafana-l12/`). Dữ liệu: chỉ mục bản 3 `t065-l11-001` trên máy. File dẫn xuất riêng `rca-results/t065-l11-001/service-graph/<bản>/<ca>.json`; không sửa file ca.

**Nhãn `t066`:** nghĩa là tuyến xuất T-066 (ca đi qua `sau_v082.py`), không phải đợt thu.

## Đầu vào

- Repo lab `ab1c52c`: `observability/`, `campaigns/`.
- `results/T-065/`: `grafana-l12/`, `may-l11/`, `manifest.json`.
- `results/T-066/e2e-001/`: `hash-tren-may.sha256`, `SHA256SUMS`.
- `results/T-058/dem-2026-11-10/grafana-evidence.py`.
- Grafana qua tunnel. Minh tự đăng nhập; Claude không đọc `grafana.env`.

## Đầu ra

**Repo RCA, `results/T-068/`:**
- `truoc/`: `/api/search`, `/api/folders`, `/api/datasources`; tách 9 UID nạp từ file và 2 UID tạo tay; hash toàn cây dữ liệu ngay trước khi sửa.
- `manual-export/`: JSON hai dashboard tạo tay, kèm sha256.
- `kiem/BAO-CAO.md`.
- `thay-doi-may.md`: hash trước/sau, cách hoàn tác.

**Repo lab** (tên file, thư mục tiếng Anh):
1. Providers: mỗi folder một provider, tên hiển thị tiếng Việt có dấu qua `folder`: "Bắt đầu tại đây", "Hệ thống FlashTicket", "RCA — sự cố", "RCA — phát lại có đáp án". **Sáu JSON lưu trữ giữ nguyên ở `dashboards/90-archive/`**, không provider nào quét. `observability/grafana/README.md` ghi cách W5 nạp lại: thêm tạm provider trỏ `/etc/grafana/dashboards/90-archive`.
2. Mục lục mới: bỏ liên kết tới UID lưu trữ; thêm liên kết theo ca có `from`/`to` từ `cua_so_ms` (`to = cua_so_ms[1] − 1`). Giữ liên kết đang đúng ở bảng ca.
3. Dashboard sự cố: bản gốc `ab1c52c` + panel đồ thị dịch vụ.
4. Dashboard "Hệ thống FlashTicket": lượng gọi, độ trễ (p90), lỗi (5xx/giây) theo service; JVM và log từ T-058; bản đồ Tempo nếu metric service graph có dữ liệu.
5. `campaigns/g1/service_graph.py`: bảng ánh xạ hạ tầng; lệnh `--ban <bản> --ca <ca>` sinh lại từ JSON ca đã lưu.
6. `campaigns/runner/sau_v082.py`: nhãn `t066` cho ca mới; gọi `service_graph.py` **sau khi** file ca và chỉ mục đã ghi xong. Chỉ bước đồ thị lỗi thì ghi trạng thái vào `service-graph/<bản>/<ca>.status.json`, in stdout, thoát 0, để runner không chạy lại M1. Không sửa `runner4.py`.
7. `campaigns/g1/relabel_case.py`: đổi `nguon_ca` trong file ca và `nguon` ở dòng `7ffb2305` của chỉ mục V082; giữ nguyên `chi-muc-ban.json`. Thiếu dòng hoặc thiếu file ca thì dừng, không ghi file nào.

## Phạm vi ghi

- Repo RCA: `results/T-068/`, `tasks/T-068-don-grafana/LOG.md`, dòng T-068 trong `docs/STATE.md`.
- Repo lab: `observability/grafana/**`, `campaigns/runner/sau_v082.py`, `campaigns/g1/service_graph.py`, `campaigns/g1/relabel_case.py`; commit và push trong phạm vi này.
- exp-obs: `git pull` ở `/opt/rca-lab`; ghi `rca-results/t065-l11-001/service-graph/`; đổi hai giá trị nhãn của 7ffb2305 (có sao lưu); restart Grafana. Qua API Grafana: xóa 2 dashboard tạo tay sau khi xuất JSON (`t058-flashticket` chỉ khi trang hệ thống đạt); xóa folder cũ khi `/api/folders/<uid>/counts` toàn 0, danh sách ghi LOG trước khi xóa; xóa `loki-1` khi không dashboard hay alert rule nào tham chiếu UID của nó, chưa xác minh được thì giữ.
- Không đụng: code M1, cấu hình V082, goc-12, gói đầu vào, `l8b-xuat.py`, `runner4.py`; file ca và đầu ra M1 (trừ hai giá trị nhãn); Prometheus/Loki/Tempo/Collector; exp-app; máy tải.

## Các bước

1. Kiểm chỉ đọc, lưu `truoc/`: 9 + 2 UID, folder, datasource; tham chiếu `loki-1`; trong cửa sổ ca 7ffb2305 ghi kết quả **riêng cho lượng gọi, độ trễ, lỗi theo service** theo nguồn đã xác minh (metric HTTP ứng dụng, span metrics, service graph); mở thử bản đồ Tempo. So hash theo 3 mốc: (a) file lịch sử L11 so manifest T-065; (b) các file có dòng trong `hash-tren-may.sha256` so T-066 (gồm hai chỉ mục và file của 7ffb2305); (c) các file khác so bản chụp hash ngay trước T-068. Khác các điều trên thì dừng, trình lại.
2. Xuất JSON 2 dashboard tạo tay; đối chiếu nguồn T-058/T-061; ghi từng panel T-058 giữ ở đâu hoặc lý do bỏ (trace mẫu cố định đã hết hạn lưu thì bỏ).
3. Viết `service_graph.py` và bảng ánh xạ; kiểm bằng script đếm độc lập trên 85 cặp bản–ca.
4. Dựng 4 dashboard bằng script từ bản gốc; ghi hash bản gốc.
5. Providers và README; sáu JSON ở `90-archive/` giữ nguyên.
6. `relabel_case.py`, sửa `sau_v082.py`; kiểm trên bản sao: relabel dừng khi thiếu dòng (không ghi file); cố ý làm bước đồ thị lỗi → có file trạng thái lỗi, đầu ra ca không đổi, `service_graph.py --ban --ca` sinh lại được đồ thị đúng ca. Mã thoát 0 một mình chưa đủ.
7. Triển khai: commit lab → pull → sinh đồ thị → đổi nhãn → restart Grafana → xóa qua API theo điều kiện.
8. Kiểm giao diện bằng bấm thật.

## Kiểm đúng đắn

| Ca | Bản | Cần thấy |
|---|---|---|
| `7ffb2305` | V082 | Nhãn `t066` trong bảng ca; có đồ thị; mở từ **mục lục mới** đúng cửa sổ ca |
| `ebd5ef38` | V082, V071, P7 | V082: `payment-service` 35 kênh cờ. V071: bảng 24 cạnh phương pháp giữ riêng. P7: `LOI_CHAY`, đồ thị "không có đầu ra" |
| `1ad3afeb` | P7, V082, V071 | `keycloak`: P7 hạng 2 `tu_sinh` → V082 hạng 3 `binh_thuong`, màu đổi theo. V071/V082: đường dẫn JSON panel thực sự đọc là `<bản>/<ca>` |

- Đồ thị: nút và cạnh khớp script đếm độc lập trên 85 cặp; cạnh hạ tầng không có số.
- Tách đáp án: grep JSON và xem giao diện.
- Toàn vẹn: theo 3 mốc; sau đổi nhãn, so JSON chỉ khác đúng hai giá trị đã khai, cộng file mới dưới `service-graph/`; file bảo vệ V082 trước = sau.

## Tiêu chí xong

1. Grafana chỉ còn 4 folder mới; không còn dashboard lưu trữ hay tạo tay (trừ ngoại lệ ở tiêu chí 4); `loki-1` xóa hoặc giữ có lý do.
2. Đồ thị dịch vụ đạt phép kiểm trên **85 cặp**: 84 lịch sử + 7ffb2305 ở V082. P7 có 27 `OK` và 1 `LOI_CHAY`, mỗi ca hiện đúng trạng thái.
3. Hồi quy, nhãn, tách đáp án, toàn vẹn đạt.
4. Trang hệ thống ghi kết quả riêng cho **lượng gọi, độ trễ, lỗi**. Đủ ba: đạt, xóa `t058-flashticket`. Thiếu tín hiệu nào: ghi tín hiệu thiếu, giữ `t058-flashticket`, trình Minh quyết mức nghiệm thu.
5. `truoc/` có 9 + 2 UID; README ghi cách nạp lại `90-archive` cho W5.

## Không làm

- Không ghi số lời gọi DB; muốn có phải trình riêng nguồn span.
- Không làm xếp hạng cạnh theo phương pháp, W4, W5, W8.
- Không sửa panel log `payment-service`: bộ lọc `error|exception|warn` rỗng là đúng với dữ liệu đã ghi ở T-066.

## Chi phí ước lượng

Khoảng một phiên (chưa kiểm). Không chạy M1, không tải. Grafana gián đoạn vài phút. Không thuộc luật cứng 8.

## Rủi ro và điều chưa chắc

- Đổi provider có thể làm Grafana tạo lại dashboard; UID giữ nguyên (chưa kiểm).
- Bảng ánh xạ có thể không phủ hết đích; phần không phủ ghi lại, không đoán.

## Prompt bàn giao

Theo `docs/review-prompt.md`; người làm ghi trong mục LOG cuối phiên.
