# T-032 — Thiết kế bản 010: kênh metric và quan hệ gọi (việc 3), chia theo loại lỗi phần đối chiếu metric (việc 7)

Viết ngày 11/10/2026, trước khi chạy. Người viết: Claude. Căn cứ: gói bổ sung 007 việc 3 và việc 7 (Q-134). Đây là bảng mô tả: không gọi phương pháp, không đổi phép tính, không chấm Hit mới, **không định nghĩa nhãn "lan"**.

## 1. Điều tôi đã thấy trước khi viết

KQ9, KQ10, và `ket-qua-phien-11.md` mục 1–2. Riêng: ở RE2-TT, 44/103 thực thể đứng trên root của BARO không có span, 38 không liên hệ với root trên đồ thị gọi, 8 nằm phía trên; ở Nezha-OB vị trí của thực thể đứng trên root ngang tỷ lệ nền với BARO. Cột thắng của thực thể đứng trên root ở RE2-TT phần nhiều là mem (BARO 55/103, SimpleRCA 15/20); 19/55 và 6/15 cột mem đó thuộc nhóm "trôi nền" (KQ10 mục 4). Vì đã thấy các số này, tôi dự đoán bất thường metric ở dịch vụ khác phần lớn **không** đi theo quan hệ gọi; bảng dưới đây kiểm dự đoán đó.

## 2. Việc 3 — cột thắng của thực thể đứng trên root nằm đâu so với chuỗi gọi

**Câu hỏi:** bất thường metric ở dịch vụ khác root, thứ làm BARO và SimpleRCA xếp chúng trên root, có đi theo quan hệ gọi tới root không. Câu này nối KQ10 mục 4 ("cột có bậc tại mốc ở dịch vụ khác là lan, tải chung hay tác dụng phụ của tiêm lỗi: bảng không phân biệt được") với đồ thị gọi.

**Đầu vào, đều đã có:** vị trí của từng thực thể so với root (`runs/chain-position-002/units.json`, định nghĩa lớp ở bản 008 mục 3); cột thắng và nhóm xu hướng của mọi cột ở RE2-TT (`runs/baseline-trend-001/cases/`, định nghĩa ở bản 004 mục 3: `trôi nền`, `bậc tại mốc`, `khác`); loại cột thắng ở Nezha-OB (`runs/derived-tables-001/derived.json`); thêm một lượt đếm mới: số span và số trace của từng dịch vụ trước và sau mốc (`scripts/service_traffic_v1.py`, không dùng nhãn).

**Cột thắng:** BARO lấy cột có z lớn nhất của thực thể; SimpleRCA lấy cột nhiều phiếu nhất của thực thể (như bản 004). Tự kiểm: loại cột thắng tính lại phải trùng `derived.json` ở mọi cặp của RE2-TT.

**Lưu lượng:** tỷ số số span sau mốc trên số span trước mốc của dịch vụ (hai đoạn cùng dài 300 giây ở RE2-TT; ở Nezha-OB hai đoạn không cùng độ dài nên chỉ so tỷ số của dịch vụ với trung vị tỷ số của mọi dịch vụ trong cùng ca). "Lưu lượng đổi": tỷ số chuẩn hóa theo trung vị của ca nằm ngoài khoảng 0,8–1,25. Mốc này do tôi đặt, chỉ để đếm; tỷ số thô được lưu.

**Bảng:** với mỗi dataset và mỗi phương pháp (BARO, SimpleRCA), các cặp (thực thể đứng trên root, root) chia theo nhóm vị trí (phía trên, hai chiều, phía dưới, không liên hệ, không có span) × loại cột thắng; ở RE2-TT thêm × nhóm xu hướng. Kèm số thực thể có lưu lượng đổi theo nhóm vị trí. Mốc so: cùng các đại lượng cho mọi thực thể không đứng trên root.

**Cách đọc khai trước.**

- Nếu bất thường metric đi theo quan hệ gọi: các cột thắng thuộc nhóm `bậc tại mốc` (có đổi thật tại mốc) tập trung ở thực thể nằm trên chuỗi gọi qua root (phía trên, hai chiều, phía dưới) nhiều hơn hẳn tỷ lệ của nhóm đó trong mọi cột thắng; và lưu lượng qua các thực thể ấy đổi.
- Nếu không: các cột `bậc tại mốc` nằm phần lớn ở thực thể không liên hệ hoặc không có span; khi đó quan hệ gọi tới root không giải thích được chúng, và các giải thích còn lại (tải chung, tài nguyên chung của máy, tác dụng phụ của công cụ tiêm lỗi) không phân biệt được bằng dữ liệu hiện có.
- Cột `trôi nền` không cần quan hệ gọi để giải thích (đã có từ trước mốc).

**Giới hạn.** Nezha-OB không có nhóm xu hướng (5 mẫu mỗi phía). Thực thể không có span không có lưu lượng đo được. Vị trí trên đồ thị không chứng minh cơ chế. 9 ca sai của BARO và 5 ca sai của SimpleRCA ở RE2-TT: số nhỏ, không rút mẫu hình theo ô.

## 3. Việc 7 — chia theo loại lỗi phần đối chiếu metric của bảng vị trí tín hiệu

Lần soát phiên 10 ghi chỗ mỏng: ở bảng "tín hiệu của root nằm ở đâu" (KQ10 mục 3), z metric của root ở BARO và phiếu của root ở SimpleRCA mới tóm tắt theo dataset, chưa chia theo loại lỗi. Việc 7 lập bảng đó từ `runs/root-signal-location-001/summary.json` (trường `/cases/*/baro`, `/simplerca`, `/tracerca_t028`) và nhãn loại lỗi: với mỗi dataset × loại lỗi, số ca root đứng hạng 1 ở BARO, SimpleRCA, TraceRCA; số ca root đứng đầu ở ít nhất một vị trí trace; số ca root không có tín hiệu ở kênh nào. Chỉ đếm lại từ file đã có; ô dưới 3 ca chỉ liệt kê.

## 4. Đầu ra

- EC2 `~/rca/T-032/runs/service-traffic-001/`, `runs/metric-chain-001/`; file tổng hợp chép về laptop. Laptop: `runs/root-signal-by-fault-001/summary.json`.
- Script: `scripts/service_traffic_v1.py`, `scripts/metric_chain_v1.py`, `scripts/root_signal_by_fault_v1.py`.
- Diễn giải: `ket-qua-phien-11.md` mục 3 và mục 7.
