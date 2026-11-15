# T-061 — Định dạng kết quả RCA cho giao diện (G1)

- **Trạng thái:** đã duyệt (11/11/2026). Minh (chat 11/11): "t59 codex làm, t61 claude làm, ... nếu không có bất đồng quản điểm thì duyệt ghi". Phản biện SPEC: Codex lượt 1, Claude đáp, Codex lượt 2 đề nghị dừng phản biện T-061 (chat 11/11).
- **Người làm:** Claude
- **Người phản biện:** Codex
- **Thuộc gói MRP:** P10, nhánh G của `docs/techstack/KE-HOACH-GIAI-DOAN-2.md` §7 — **Cổng:** không có cổng riêng.

## Mục tiêu

- DT18: sản phẩm cuối có giao diện minh họa kết quả phân tích.
- MRP P10, Q-28: demo báo sự cố → đồ thị con bất thường → danh sách nguyên nhân → giải thích.
- Quyết định của Minh (11/11, M6): phương án A, Grafana panel Node graph, trước; B thử sau nếu A không ổn; G2 do Minh làm.

Task thiết kế và cài một định dạng chung cho A, B và dịch vụ RCA (G3), kèm bộ chuyển đổi từ đầu ra M1. Không đánh giá M1.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Cần phân xử | Phép kiểm | Phần thiếu |
|---|---|---|---|
| 1. Định dạng cần trường gì | Đủ cho demo: sự cố, nút, cạnh, vai trò nút, xếp hạng, nhóm đồng hạng, vùng nghi ngờ, bằng chứng, liên kết, truy vết nguồn (`method_version`, `config_id`, hash file nguồn) | Đối chiếu trường Node graph (`docs/DE-XUAT-HUONG-GRAFANA-RCA.md` §7.2, tham khảo theo Q-188; tài liệu Grafana về Node graph) | — |
| 2. Chuyển đổi có giữ đúng kết luận của M1 không | Không làm mất, không bịa, không đổi ý nghĩa | Kiểm theo giá trị các con trỏ `/verdict`, `/mode`, `/classes/*`, `/entity_ranking[].tie_group`, `/region`, hai đầu mỗi cạnh `/extra/canh`, `/evidence_refs`, `/method_version`, `/config_id` | — |
| 3. Nhãn không lọt | Đáp án chỉ dùng khi phát lại | Bộ chuyển đổi thường chỉ đọc đầu ra M1 và nguồn bằng chứng được phép. Bản phát lại ghép đáp án ở bước trình bày, sau khi đầu ra của cả đợt đã băm, bằng quyền đọc nhãn riêng (PLAN §5.2–5.3). Kiểm: thêm hay bỏ phần phát lại thì kết luận, hạng, vùng, màu dự đoán không đổi | — |
| 4. Grafana hiển thị được không | Node graph đọc được hai mẫu | Grafana 13.3.0 chạy cục bộ trên laptop (Docker), nguồn TestData, dựng khung `nodes`, `edges` từ dữ liệu chuyển đổi; kiểm màu, hạng, danh tính nút. Không thay đổi `exp-obs` | Nếu không chạy được cục bộ: phần hiển thị OPEN, phần schema và chuyển đổi vẫn nghiệm thu được |

Điều phải giữ với hai mẫu thật:
- Ca bình thường `c12e47ab`: `NO_INTRINSIC_ANOMALY`, 17 thực thể đồng hạng, không có bằng chứng → không tô nút nào là nguồn.
- Ca pause `f4a8c021`: `CAUSE_FOUND`, 16 thực thể có hạng; `event-service` lớp `thieu_du_lieu` → hiện thiếu dữ liệu, không gán hạng.
- Cả hai chế độ `a`: bản ghi sự cố nêu mốc lấy từ đâu. Ca bình thường ghi "mốc tham chiếu do bộ điều phối cấp", vì không có lỗi được tiêm. Không để người xem hiểu là Grafana tự phát hiện.
- Liên kết sang trace, log, metric chỉ sinh khi có truy vấn, cửa sổ hoặc định danh từ nguồn tương ứng; không có thì để trống.

## Đầu vào

- `results/T-058/dem-2026-11-10/rca-ban-dau/outputs/c12e47ab/method-output-1.json`, `.../f4a8c021/method-output-1.json`, `rca-ban-dau.md`; kiểm hash theo `results/T-058/dem-2026-11-10/artifacts-sha256.json`.
- `docs/DE-XUAT-HUONG-GRAFANA-RCA.md` §6–7; `docs/techstack/PLAN-TRIEN-KHAI.md` §5.
- Image `grafana/grafana:13.3.0` (cùng bản trên `exp-obs`), chạy cục bộ.

## Đầu ra

`results/T-061/`:
- `dinh-dang-ket-qua-rca.md`: ý nghĩa từng trường, quy tắc hiển thị, cách ghép phát lại.
- `schema.json`: JSON Schema.
- `chuyen-doi.py`: đầu ra M1 → định dạng.
- `mau/`: hai mẫu đã chuyển.
- `kiem-chuyen-doi.md`: bảng đối chiếu theo con trỏ JSON.
- `kiem-hien-thi.md`: cách chạy Grafana cục bộ, ảnh chụp, kết quả.
- Đề xuất cách cấp dữ liệu cho G2 (Infinity hoặc PostgreSQL) kèm lý do và điều kiện triển khai, trong `dinh-dang-ket-qua-rca.md`.

## Phạm vi ghi

- `results/T-061/`
- `tasks/T-061-dinh-dang-ket-qua-rca/LOG.md`
- Dòng T-061 trong `docs/STATE.md`
- Container Grafana cục bộ trên laptop (tạo, xóa); không đụng `exp-obs`, `exp-app`.

## Các bước

1. Kiểm hash hai mẫu; đọc cấu trúc đầu ra M1.
2. Viết `schema.json` và `dinh-dang-ket-qua-rca.md`.
3. Viết `chuyen-doi.py`; chạy trên hai mẫu — kiểm theo giá trị (câu 2) và phép kiểm phát lại (câu 3).
4. Chạy Grafana cục bộ, nạp hai mẫu — kiểm hiển thị (câu 4).
5. Viết đề xuất cấp dữ liệu cho G2.

## Kiểm đúng đắn

Như bảng trên. Không chạy lại M1. Một trạng thái đồng loạt (17 thực thể đồng hạng) là kết quả đúng của `NO_INTRINSIC_ANOMALY`, phải hiện như vậy.

## Tiêu chí xong

- Hai mẫu đạt schema.
- Bảng đối chiếu theo con trỏ JSON khớp; không có phần tử bỏ mà không có lý do.
- Bốn điều phải giữ với hai mẫu đều đạt; phép kiểm phát lại cho kết quả không đổi.
- Node graph cục bộ hiện hai mẫu đúng, hoặc ghi rõ phần hiển thị OPEN và lý do.
- Minh xác nhận định dạng đủ để bắt đầu G2.

## Không làm

Sửa M1; dịch vụ RCA (G3); giao diện hoàn chỉnh (G2); cài plugin hay thêm nguồn dữ liệu trên `exp-obs`.

## Chi phí ước lượng

Khoảng 1 ngày. Tải image Grafana vài trăm MB. Không thuộc luật cứng 8.

## Rủi ro và điều chưa chắc

- Chưa kiểm: TestData cho dựng đúng kiểu khung Node graph cần.
- Đầu ra M1 có thể thiếu cạnh của thực thể hạ tầng; khi đó ghi đúng thiếu, không bịa cạnh.

## Prompt bàn giao

Người làm soạn theo `docs/review-prompt.md` sau lượt báo cáo.
