# T-065 — Hoàn thiện giao diện Grafana cho kết quả RCA

- **Trạng thái:** đã duyệt (13/11/2026, Minh duyệt tổng thể gói chiến dịch; yêu cầu nhánh Grafana ở tin nhắn cùng ngày).
- **Người làm:** Codex (`gpt-6.1-sol`, reasoning high). **Người phản biện:** Claude (điều phối, kiểm kết quả, gọi lại Codex theo checkpoint khi hạn mức hồi).
- **Bổ sung đã duyệt 13/11/2026:** áp dụng phần bổ sung cuối file về G-c, phạm vi ghi và điều kiện hoàn thành. Căn cứ ở `docs/DECISIONS.md`, mục “Bổ sung quyền điều phối chiến dịch nhiều ngày”.
- **Thuộc:** `docs/techstack/KE-HOACH-GIAI-DOAN-2.md` §7 nhánh G (G2; lớp thao tác). Hồ sơ chiến dịch: `tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md`.

## Mục tiêu

DT18 đòi sản phẩm có giao diện minh họa kết quả phân tích. Dashboard trên Grafana `exp-obs` phải: (a) hết lỗi tồn; (b) cho bấm một service để xem bảng và đồ thị các thao tác bên trong, rồi mở bằng chứng từng thao tác; (c) nối với đầu ra M1 hiện có (P7) và bản M1 sau tinh chỉnh (T-064), ghi rõ phiên bản, cấu hình, cửa sổ phân tích.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Phép kiểm | Phụ thuộc |
|---|---|---|
| Bản 6 còn lỗi gì trên Grafana thật? | Rà lại theo `REVIEW-G1-5.md` (G-2, G-3) và `results/T-062/codex/g1-that-2/BAO-CAO.md`; **lấy bản 6 làm mốc hồi quy** (123 URL giải mã đúng một lần đã đạt — không làm lại) | G-a |
| Mỗi quan hệ vẽ ra có nguồn xác minh không? | Cạnh chỉ vẽ khi có quan hệ quan sát được; ghi loại quan hệ: cha–con (span), đích lời gọi (`server.address`, DB), span link của message (chỉ khi dữ liệu có) | G-b |
| Người xem có biết đang xem bản M1 nào? | Mỗi kết quả hiện phiên bản, hash cấu hình, cửa sổ `[t−300, t+300)` | G-c |

## Đầu vào

`results/T-062/giao-dien/` (bản 6: `dung-dashboard.py`, `chi-muc-*.py`, `grafana/`, `thay-doi.md`); `results/T-061/` (định dạng 0.2, `chuyen-doi.py`, `phat-lai.py` — **chỉ đọc**); `results/T-062/ca/*/outputs/*/method-output-1.json` (kênh `op`, vai trò, cạnh); `tasks/T-062-dem-chang-1-4/REVIEW-G1*.md`; `BOI-CANH.md` mục "Lớp thao tác"; đầu ra T-064 khi có. Mật khẩu Grafana: Minh đã cho Codex đọc file mật khẩu trên máy; không in ra.

## Việc

- **G-a (làm ngay):** liên kết Loki ở bảng bằng chứng (hiện 0 URL); điều hướng giữa danh sách → ca → chi tiết và trang phát lại; khung thời gian đúng cửa sổ ca ở mọi panel và liên kết; lời diễn giải panel rỗng (không để "No data" trần — nói rõ "không có vì …"); hiển thị vùng nghi ngờ; chữ "đáp án" ở điều hướng (G-3).
- **G-b (làm ngay trên đầu ra P7):** bấm một service → bảng thao tác (HTTP, SQL, job, message theo dữ liệu thực có; trạng thái/cờ M1; điểm `e` chỉ ở chi tiết; kích thước nút cố định) và đồ thị thao tác (cạnh cha–con quan sát được, áp đúng tiền xử lý `src/m1/chuoi.py`: cắt cửa sổ, `he_span`, alias) → mở bằng chứng từng thao tác trong Tempo/Loki/Prometheus. Ghi rõ loại quan hệ **đã hỗ trợ và đã kiểm**; loại chưa có dữ liệu (span link) ghi là chưa hỗ trợ. Cần mở rộng định dạng kết quả thì ra **phiên bản định dạng mới** trong `results/T-065/` (không sửa T-061), kèm bộ kiểm lược đồ.
- **G-c (sau khi T-064 có bản đề xuất):** chọn xem P7 hay M1-FT cho cùng một ca; hiện phiên bản, cấu hình, cửa sổ.

## Đầu ra (`results/T-065/`)

`dung-dashboard.py` và nguồn dashboard; `dinh-dang/` (nếu mở rộng); `du-lieu/` (file cấp cho Infinity); `kiem/<lượt>/BAO-CAO.md` + ảnh chụp thao tác thật trên trình duyệt (bấm thật, không chỉ dựng URL) + bảng đối chiếu số hiển thị với file nguồn; `thay-doi-may.md` (hash trước/sau, cách hoàn tác); `CHECKPOINT.md` riêng của nhánh; nhật ký Codex ở `results/T-065/codex/`.

## Phạm vi ghi

`results/T-065/`; trên `exp-obs` **chỉ**: file dashboard **mới** trong `/opt/flash-ticket-obs/pinned/provisioning/dashboards/` (giữ dashboard bản 6), thư mục con mới trong `/opt/flash-ticket-obs/rca-ket-qua/`, khởi động lại container Grafana. Không đổi Prometheus/Loki/Tempo/Collector (thuộc T-063). Nếu `pinned/compose.json` đổi hash thì ghi trước/sau. Không ghi LOG/STATE của task khác.

## Kiểm đúng đắn

Mỗi lượt: 9 ca T-062 hiển thị khớp nguồn (hồi quy so bản 6); mọi liên kết bằng chứng giải mã đúng một lần và mở đúng datasource, cửa sổ, truy vấn; bấm thật ít nhất một liên kết mỗi loại (Tempo, Loki, Prometheus) ở ít nhất 3 ca; lớp thao tác: số thao tác và cờ khớp `method-output-1.json`; trang phát lại vẫn tách đáp án. Không dùng đáp án trong trang chính.

## Tiêu chí xong

G-a, G-b đạt các phép kiểm trên với bằng chứng lưu; G-c nối được bản M1-FT khi có. Phần chưa làm được ghi rõ lý do và bằng chứng thiếu.

## Không làm

Không chấm điểm trong Grafana; không sửa M1; không sửa T-061/T-062; ô LLM (G4) để trống.

## Chi phí ước lượng

Chưa kiểm: G-a khoảng 1 ngày, G-b 2–3 ngày của Codex.

## Rủi ro và điều chưa chắc

Node graph cần 10–20 s tính bố cục; file provisioning gắn bind mount phải `docker restart` mới nạp; Infinity đọc file tĩnh nên lớp thao tác có thể cần chỉ mục riêng theo service (chưa kiểm).

## Bổ sung đã duyệt — tích hợp sớm và hoàn thành, 13/11/2026

Phần này thay thế phụ thuộc “sau khi T-064 có bản đề xuất” của G-c và cụ thể hóa phần chưa hoàn thành ở mục “Tiêu chí xong”. Nội dung trước bổ sung giữ làm lịch sử.

- G-a và G-b làm ngay trên nguồn P7 đã kiểm, song song các nhánh tải và phương pháp. Thống nhất hợp đồng đầu ra với T-064 từ sớm. G-c tích hợp thử từ đầu ra phù hợp đầu tiên, có đánh dấu biến thể, rồi kiểm lại trên bản M1-FT đề xuất cuối. Giữ truy vết phiên bản, cấu hình và cửa sổ.
- Thiếu dữ liệu do đường xuất, định dạng hoặc chỉ mục thuộc quyền T-065 thì Codex tự hoàn thiện và kiểm tiếp. Thiếu tín hiệu do thu nhận thì Claude phối hợp T-063. Trong lúc chờ, tiếp tục các phần giao diện độc lập. Không suy nguyên nhân panel rỗng khi chưa có bằng chứng, mô tả rõ kết quả truy vấn và phần chưa xác định.
- Hoàn thành task khi G-a, G-b đạt các phép kiểm và G-c được kiểm trên bản M1-FT đề xuất cuối. Chức năng còn thiếu giữ trạng thái đạt một phần, kèm nguyên nhân, bằng chứng thiếu và bước tiếp theo. Việc ghi lý do không thay cho hoàn thành chức năng đã giao.
- Bổ sung phạm vi ghi `tasks/T-065-giao-dien-grafana/LOG.md`, checkpoint riêng đã liệt kê trong đầu ra và dòng T-065 trong `docs/STATE.md`, theo vai trò người làm. Giữ các phạm vi máy và hồ sơ khác đã cấp.
- Các ước lượng ngày công dùng để cập nhật tiến độ. Codex hết hạn mức thì lưu checkpoint, Claude kiểm trạng thái và gọi tiếp khi công cụ hồi. Sau báo cáo tiếp tục tới đầu ra đã giao. Việc restart Grafana được phối hợp với L2 và lịch đo chung.
