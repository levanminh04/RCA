# T-032 — Thiết kế phép đổi tất định, bản 002 (bổ sung cho bản 001)

Viết ngày 11/10/2026, trước khi chạy hai phép dưới đây. Người viết: Claude. Bản 001 giữ nguyên; các quy tắc chung ở mục 3 của bản 001 áp dụng y nguyên.

## 1. Điều tôi đã thấy trước khi viết

Khác bản 001, hai phép này được nghĩ ra **sau khi đã xem kết quả mô tả** của chính BARO và SimpleRCA:

- BARO, RE2-TT: ở 54/103 cặp, thực thể đứng trên root có mức lệch tương đối nhỏ hơn root nhưng z lớn hơn; IQR nền của cột thắng bằng trung vị 0,4% median nền (`runs/derived-tables-001/derived.json` → `/baro/summary/RE2-TT`).
- SimpleRCA, RE2-TT: cột nhiều phiếu nhất của thực thể đứng trên root là cột mem ở 15/20 cặp, vượt ngưỡng ở trung vị 288/300 mẫu (cùng file → `/simplerca/summary/RE2-TT`).
- Phép B-1 đã cho kết quả: bỏ lọc cột hằng không đổi hạng root ở 52/52 ca.

Vì vậy hai phép này là kiểm một ứng viên rút ra từ dữ liệu dev, không phải giả thuyết đặt trước. Chưa thấy kết quả của B-2 hay S-1. Mục 7 của bản 001 từng ghi không dùng cấu hình `channels` để phân xử cơ chế; bản này đổi nhận định đó và nêu lý do ở mục 3.

## 2. B-2 — BARO với thang độ lệch chuẩn thay cho thang IQR

- **Ứng viên cần kiểm:** chia cho IQR của đoạn nền làm các cột gần như phẳng ở nền có z lớn với thay đổi nhỏ, và nhờ đó vượt root.
- **Đổi (một bước):** lớp chuẩn hóa `RobustScaler` (trừ median, chia IQR) được thay bằng `StandardScaler` (trừ mean, chia độ lệch chuẩn) của cùng thư viện scikit-learn 1.6.0, ở cả lời gọi trong `RCAEval/e2e/baro.py` và lời gọi tính lại khóa trong adapter. Không có tham số nào được chọn.
- **Giữ:** tiền xử lý, lọc cột hằng, phép giao cột, lấy max theo cột, max theo dịch vụ, cửa sổ, dữ liệu.
- **Vì sao phép này không tùy ý:** độ lệch chuẩn là thang đối ứng chuẩn của IQR; phương pháp N-Sigma mà bài BARO dùng làm đối chứng chính là phép tính này. Không cần đặt sàn hay ngưỡng.
- **Dự đoán đối lập:**
  - H-IQR: ưu thế của thực thể đứng trên root đến từ IQR rất nhỏ. Khi đó dưới thang độ lệch chuẩn, root tăng hạng ở các ca sai, nhất là các cặp có mức lệch tương đối nhỏ hơn root.
  - H-nền: độ lệch chuẩn của các cột đó cũng rất nhỏ, hạng root không đổi. Khi đó hạn chế thuộc việc chuẩn hóa theo độ biến thiên nền nói chung, không riêng IQR.
- **Phải báo kèm:** số ca đúng bị hỏng đi dưới B-2.
- **Sham:** dùng nhánh sham của lượt `baro-b1-001` (đã khớp bản đóng băng từng bit ở 52/52 ca); không chạy lại.
- **Giới hạn:** B-2 không cho biết thay đổi nhỏ ở cột mem/cpu của dịch vụ khác là do sự cố hay trôi tự nhiên. Nó không đề xuất N-Sigma làm phương pháp.

## 3. S-1 — SimpleRCA đếm theo cột thay cho đếm theo mẫu

- **Ứng viên cần kiểm:** điểm metric đếm số mẫu vượt ngưỡng, nên một cột vượt ngưỡng gần suốt cửa sổ cho tới 300 phiếu, lấn át phiếu trace và log (mỗi kênh tối đa 1).
- **Đổi (một bước):** tham số có sẵn `metric_aggregation` của `simplerca.core.Config` từ `'events'` sang `'channels'`: mỗi cột metric cho 1 phiếu nếu có ít nhất một mẫu vượt ngưỡng. Không sửa mã nguồn; chỉ đổi giá trị cấu hình trong tiến trình chạy.
- **Giữ:** ngưỡng mean + 3·std, phiếu trace, phiếu log, phép cộng, quy tắc hòa, cửa sổ, dữ liệu.
- **Vì sao đổi nhận định so với bản 001:** bản 001 coi `channels` chỉ là cấu hình độ nhạy. Sau khi thấy 15/20 cặp RE2 do một cột vượt ngưỡng gần suốt cửa sổ, `channels` trở thành đúng phép đổi cần có để tách "đếm theo thời lượng vượt ngưỡng" khỏi "có nhiều kênh vượt ngưỡng". Cả hai giá trị đều do người viết SimpleRCA M4 định nghĩa sẵn (T-017), không phải tôi đặt.
- **Dự đoán đối lập:**
  - H-đếm-mẫu: ưu thế đến từ việc đếm số mẫu. Khi đó dưới `channels`, root tăng hạng ở các ca sai của RE2.
  - H-số-kênh: ưu thế đến từ việc dịch vụ kia có nhiều cột vượt ngưỡng hơn. Khi đó hạng root không đổi hoặc giảm. Ở Nezha, thực thể đứng trên root có nhiều cột có phiếu hơn root ở 37/44 cặp, nên dự đoán trước là `channels` không giúp ở Nezha.
- **Phải báo kèm:** số ca đúng bị hỏng đi; số nhóm hòa tăng lên (điểm nguyên nhỏ dễ hòa), vì Hit tính bi quan theo hòa.
- **Sham:** nhánh `events` chạy lại đường native và phải khớp bản đóng băng từng bit.

## 4. Nơi chạy và chi phí

EC2, mỗi nhánh của mỗi ca một tiến trình, ưu tiên thấp. Ước lượng chưa đo: B-2 khoảng 13 phút (52 lượt), S-1 khoảng 25 phút (104 lượt).

## 5. Nháp bổ sung đoạn WHY (chưa nối `docs/WHY.md`)

**Chọn thêm:** B-2 (thang độ lệch chuẩn cho BARO) và S-1 (đếm theo cột cho SimpleRCA). **Vì sao:** hai bảng mô tả cùng chỉ về một ứng viên là chuẩn hóa hoặc đếm theo độ biến thiên nền; cần phép đổi để phân biệt "nơi chênh xuất hiện" với "bước làm đổi hạng". **Phương án đã xét:** đặt sàn cho IQR (phải chọn giá trị, tùy ý); bỏ hẳn cột mem (đổi tập kênh, mất cả tín hiệu của root); chỉ mô tả (không phân xử). **Giới hạn:** hai phép được nghĩ ra sau khi xem dữ liệu dev, nên kết quả chỉ là bằng chứng trên dev cho ứng viên, không phải kiểm định độc lập.
