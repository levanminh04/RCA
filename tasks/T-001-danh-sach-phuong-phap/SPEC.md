# T-001 — Chốt danh sách phương pháp cho P1

- **Trạng thái:** đã duyệt (02/10/2026)
- **Người làm:** Claude
- **Người phản biện:** Codex
- **Thuộc gói MRP:** P1 — **Cổng:** G1

## Mục tiêu

Chọn 8–12 phương pháp RCA và các bộ phát hiện bất thường cho P1, theo ba tiêu chí ở MRP P1: phủ đủ các họ; có code chạy được; được các bài gần đây dùng làm baseline. Phục vụ nhận xét đầu tiên của cô ("chưa sâu kỹ thuật của từng phương pháp") và RQ1.

## Đầu vào

- `docs/MRP.md` P1 (danh sách ứng viên, ba tiêu chí, Q-30 về bộ phát hiện).
- `docs/knowledge/K1-phuong-phap-rca.md`, `docs/knowledge/K4-ho-thuat-toan.md`.
- Code RCAEval tại revision ghi ở MRP P1.
- Repo gốc của các tác giả.

## Đầu ra

`results/T-001/danh-sach-phuong-phap.md`. Mỗi phương pháp một dòng, ghi:
- họ phương pháp; bài toán nó giải (phát hiện, xếp hạng, hay cả hai);
- đầu vào (metric, log, trace); có cần biết trước thời điểm sự cố không;
- có cần nhãn để học không;
- code ở đâu, giấy phép, chạy được trên CPU không;
- các bài gần đây dùng nó làm baseline;
- đề xuất chọn hay không, kèm lý do.

Cuối file: danh sách đề xuất và các phương án đã xét, để Minh duyệt ở G1.

## Phạm vi ghi

Chỉ được ghi vào các đường dẫn dưới đây, cộng `LOG.md` của task này và dòng của task trong `docs/STATE.md`. Ghi ra ngoài thì dừng, đề xuất.

- `results/T-001/`

## Các bước

1. Liệt kê các phương pháp có trong RCAEval bằng cách đọc code thật — kiểm bằng: danh sách module kèm đường dẫn file.
2. Với phương pháp không có trong RCAEval (ví dụ Eadro, TraceRCA, SimpleRCA, DeepTraLog, GDN), tìm code chính thức và giấy phép — kiểm bằng: link repo hoặc ghi "không tìm thấy".
3. Điền bảng; mỗi ô có nguồn (file và dòng code, hoặc link) — kiểm bằng: không còn ô nào thiếu nguồn hoặc thiếu chữ "chưa kiểm".
4. Đề xuất danh sách, kèm phương án đã xét.

## Tiêu chí xong

- Mọi ứng viên trong MRP P1 có một dòng.
- Mỗi họ phương pháp có ít nhất một đại diện, hoặc có lý do vì sao không.
- SimpleRCA có trong danh sách, hoặc có lý do vì sao không chạy được.
- Mỗi nhận định dựa trên kết quả có nêu nguyên nhân khả thi khác (Q-33).

## Không làm

- Chưa chạy phương pháp nào, chưa dựng môi trường.
- Chưa viết hồ sơ kỹ thuật chi tiết (task P1 sau).
- Không tải dữ liệu.

## Chi phí ước lượng

Chỉ đọc code và web. Không cần báo trước theo luật cứng 8.

## Rủi ro và điều chưa chắc

- Số "top-1" của các bài đánh giá (ví dụ SimpleRCA) chưa đối chiếu bản in; chỉ dùng làm thông tin, không làm căn cứ chọn.
- Một số code chỉ có trong artifact (ví dụ Zenodo); có thể không tải được trang. Khi đó ghi "chưa kiểm".
