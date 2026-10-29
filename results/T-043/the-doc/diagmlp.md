# Thẻ đọc — DiagMLP → C-a0, C-a1

**Nguồn.** F. Gao, R. Xin, X. Li, Y. Zhang, "Are GNNs Actually Effective for Multimodal Fault Diagnosis in Microservice Systems?", arXiv 2501.02766. Đọc tóm tắt, §III (tr. 2–3), §V (tr. 5).

## Cơ chế

- **DiagMLP** thay mô-đun GNN trong Eadro và TVDiag bằng MLP. Mỗi nút giữ nhúng đa nguồn (metric, log, trace) do **cùng bước tiền xử lý** tạo ra. MLP gộp theo nguồn, rồi gộp theo nút; không mô hình hóa đồ thị.
- Đây là mô hình **có giám sát**: mỗi cửa sổ lỗi có nhãn root (§III.B).
- **Kết quả:** trên năm dataset, DiagMLP ngang các phương pháp GNN ở phát hiện, định vị và phân loại.
- **Hình UMAP** (Hình 3): đặc trưng sau tiền xử lý, chưa dùng topo, đã tách cụm theo root ở SN và TT của Eadro.
- **Tác giả kết luận** (§V): tiền xử lý đã mang thông tin phụ thuộc cần thiết; GNN thêm ít ngoài việc gộp đa nguồn.

## Đầu vào; phần ta có và thiếu

- DiagMLP cần nhãn root để học. M1 không học có giám sát (luật cứng 6; WHY-10, tiêu chí 2). Vì vậy **không dùng DiagMLP làm phương pháp hay đối chứng**.
- Thứ lấy được là **bài học thiết kế đối chứng:** nhánh "bỏ đồ thị, giữ tiền xử lý" chỉ đo phần đóng góp của bước bị bỏ. Nếu tiền xử lý đã dùng quan hệ thì nhánh đó vẫn dùng quan hệ.

## Điều kiện thất bại của phép so kiểu DiagMLP

- Đặc trưng tiền xử lý tạo từ quan hệ (ví dụ self-time từ cha–con, hay gán theo cạnh), làm phép so không tách được lợi ích của quan hệ.
- Dataset nhỏ, ít thành phần, khiến thông tin topo toàn cục ít tác dụng (tác giả tự nêu).

## Chỗ đổi trong B2

Không đổi công thức. Kiểm lại B3 theo bài học này:
- **C-a0** bỏ mọi chỗ dùng quan hệ ở bốn chặng: đặc trưng (không E1, E2), điểm, tập ứng viên, xếp hạng (không E5, E6b, E7). Đơn vị thời lượng cả span không loại span bọc (D18), vì nhận ra span bọc cần quan hệ cha–con. Vì vậy C-a0 là nhánh "không quan hệ" thật ở mức phép tính.
- **C-a1** còn giữ cha–con qua E1. B3 đã ghi kết luận của C-a1 chỉ nói về cạnh dịch vụ.
- **Phần còn lại không tách được:** lựa chọn tín hiệu E3, E3b của chuỗi cuối được chọn khi chuỗi có đồ thị (D23). Đặc tả v1 giữ câu giới hạn này.
