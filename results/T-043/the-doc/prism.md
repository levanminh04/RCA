# Thẻ đọc — PRISM, "Graph-Free Root Cause Analysis" → đối chứng C-h

**Nguồn.** L. Pham, "Graph-Free Root Cause Analysis", arXiv 2601.21359v1. Đọc §2 (tr. 2), §3.1–3.3 (tr. 2–4). Theo tóm tắt (tr. 1), bài đánh giá trên 735 sự cố của 9 dataset thực. Phần thực nghiệm (§4) và phụ lục chưa đọc kỹ.

## Cơ chế

1. **Mô hình thành phần–thuộc tính** (§2, tr. 2). Mỗi thành phần có hai loại thuộc tính:
   - thuộc tính nội bộ: tài nguyên, độ dài hàng đợi, trạng thái;
   - thuộc tính bên ngoài: độ trễ, tỷ lệ lỗi.
   Bài đặt ba điều kiện:
   - Tiên đề 2.5: trong một thành phần, nội bộ là tổ tiên nhân quả của bên ngoài;
   - Tiên đề 2.6: ảnh hưởng giữa các thành phần chỉ đi qua thuộc tính bên ngoài;
   - Giả định 2.4: root có ít nhất một thuộc tính nội bộ và một thuộc tính bên ngoài được đo, và lỗi biểu hiện ở chúng.
2. **Chấm điểm** (§3.1, Định nghĩa 3.1, tr. 3): điểm lệch là |x − c(θ)| / s(θ), với tâm và thang ước lượng trên dữ liệu tham chiếu, ví dụ z-score hoặc theo IQR.
3. **Gộp** (§3.2, tr. 3): gộp điểm các thuộc tính của mỗi thành phần thành S^I (nội bộ) và S^E (bên ngoài), bằng max, trung bình hoặc tổng.
4. **Xếp hạng** (§3.3, Eq. 3–4, tr. 4):
   - M_add = S^I + S^E − log(1 + S^I + S^E);
   - M_conj = min(S^I, S^E).
   Lý do: root bất thường ở cả hai loại thuộc tính; thành phần bị ảnh hưởng chỉ bất thường ở thuộc tính bên ngoài.

## Đầu vào; phần ta có và thiếu

- **Không cần nhãn, không cần đồ thị.** Chỉ cần phân loại từng kênh thành nội bộ hay bên ngoài theo **loại tín hiệu**. Đây là tri thức trước, không phải nhãn ca.
- **Có:**
  - RE2-TT: metric `cpu`, `mem`, `diskio`, `socket` (nội bộ); `latency-50`, `latency-90`, `error` (bên ngoài); thời lượng span (bên ngoài).
  - Nezha-OB: CPU, bộ nhớ, syscall, byte mạng (nội bộ); độ trễ, tỷ lệ thành công của pod và của front (bên ngoài).
- **Thiếu:** cách gộp theo thời gian của PRISM nằm ở phụ lục, chưa đọc.

## Điều kiện thất bại

- Root không có thuộc tính nội bộ lệch, ví dụ lỗi mạng (DELAY). KHAO-SAT K1 trích từ bài: điều kiện "nội bộ trước" chỉ đúng 27,4% ca DELAY; điều kiện về thứ tự điểm đúng 66,5% ca.
- Thành phần bị ảnh hưởng cũng tăng tài nguyên, ví dụ khi tải dồn.
- Giả định 2.4 sai khi root không có thuộc tính nội bộ được đo, hoặc khi lỗi không biểu hiện.

## Chỗ đổi trong B2 (C-h)

- Bảng ứng viên của SPEC ghi: "C-h, PRISM — chỉ thêm nếu thẻ đọc cho được cách cài không cần nhãn". Thẻ này cho thấy C-h không cần nhãn, nhưng **chưa cho một cách cài xác định được**: thiếu quy tắc gộp thời gian, cổng/cờ E4, hướng chấm, thang khi IQR = 0, kênh thiếu. Câu "điều kiện đó thỏa" ở bản trước là quá mạnh. **Phiên 10: C-h đưa về ứng viên** (`dinh-chinh-phien10.md` Đ16). Các gạch dưới là định nghĩa của bản trước, giữ làm lịch sử.
- Vì vậy đặc tả v1 thêm C-h làm đối chứng **chỉ báo cáo** ở T13. C-h không có vai trò quyết định, nên không chạm D5 (C-c, C-g, C-a0, C-a1, C-d1, C-d3).
- **Định nghĩa trong đặc tả v1:**
  - nội bộ: lớp "tài nguyên" của B1.4;
  - bên ngoài: độ trễ, lỗi, tỷ lệ thành công, thời lượng cả span;
  - điểm theo nhánh z (IQR, quy tắc RobustScaler), cùng tiền xử lý với R0;
  - gộp bằng max; xếp theo M_conj; M_add báo kèm.
- **Vì sao đáng giữ:** C-h tách "tự sinh" khỏi "kế thừa" bằng loại tín hiệu, **không dùng quan hệ**. Đây là phiên bản không đồ thị của ý tưởng tầng 2. So E5 với C-h trả lời một phần câu RQ3d: dùng quan hệ có hơn quy tắc đơn giản không dùng quan hệ không.
- **Giới hạn:** C-h dùng điểm z, trong khi chuỗi M1 dùng điểm E4 (D24). Phép so vì vậy trộn hai cách chấm và chỉ để mô tả.
- Số công bố của PRISM trên RCAEval chưa trích; task cài đặt (3) cần tra trước khi so.
