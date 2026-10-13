# T-026 — Chi phí chạy đầy đủ và chấm

Ngày 07/10/2026. Nguồn lượt: `runs/full-001/summary-continued-001.json`, từng `cost.json`/record; danh sách duy nhất trong `ban-ghi-dua-vao-cham.json`. Không cộng lại các tham chiếu A/B/BARO guard vào thời gian máy.

248 bản ghi nguồn: 27 dùng lại pilot, 221 mới. Tổng wall các nguồn duy nhất 2088.308 s; phần chạy mới 1873.861 s (31.23 phút), phần dùng lại 214.447 s. Elapsed ghi trong `runs/full-001/summary-continued-001.json` là 1885.521 s. Elapsed lấy nguyên trường nguồn và có thể gồm điều phối/chờ xử lý điểm dừng; wall từng bản ghi không cộng thời gian đọc/viết báo cáo hoặc chờ hội thoại.

| View nguồn | Phương pháp | Lượt | Dùng lại | Wall tổng s | Min–max s | Median s | RSS max MiB | Trạng thái |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| main | baro | 22 | 3 | 471.320 | 15.851–31.085 | 20.931 | 503.6000 | {'OK': 22} |
| main | simplerca | 22 | 3 | 140.897 | 3.531–21.668 | 5.466 | 327.1000 | {'OK': 22} |
| main | microrank | 22 | 3 | 128.148 | 3.894–7.669 | 6.013 | 346.9000 | {'OK': 22} |
| main | tracerca | 22 | 3 | 579.597 | 15.715–33.550 | 27.956 | 526.5000 | {'OK': 22} |
| main | circa | 22 | 3 | 7.300 | 0.145–1.193 | 0.208 | 78.7000 | {'UNSUPPORTED': 22} |
| main | torai | 22 | 3 | 7.180 | 0.135–1.325 | 0.188 | 79.0000 | {'UNSUPPORTED': 22} |
| sensitivity_A | baro | 1 | 0 | 24.603 | 24.603–24.603 | 24.603 | 398.0000 | {'OK': 1} |
| sensitivity_A | simplerca | 1 | 0 | 3.968 | 3.968–3.968 | 3.968 | 212.9000 | {'OK': 1} |
| sensitivity_A | microrank | 1 | 0 | 4.004 | 4.004–4.004 | 4.004 | 228.7000 | {'OK': 1} |
| sensitivity_A | tracerca | 1 | 0 | 23.254 | 23.254–23.254 | 23.254 | 407.1000 | {'OK': 1} |
| sensitivity_A | circa | 1 | 0 | 0.173 | 0.173–0.173 | 0.173 | N/A | {'UNSUPPORTED': 1} |
| sensitivity_A | torai | 1 | 0 | 0.138 | 0.138–0.138 | 0.138 | N/A | {'UNSUPPORTED': 1} |
| trace_guard | simplerca | 22 | 3 | 108.979 | 3.683–5.892 | 5.095 | 327.2000 | {'OK': 22} |
| trace_guard | microrank | 22 | 3 | 116.869 | 3.789–6.679 | 5.397 | 340.5000 | {'OK': 21, 'ERROR': 1} |
| trace_guard | tracerca | 22 | 3 | 467.528 | 15.231–29.886 | 19.462 | 519.5000 | {'OK': 22} |
| trace_guard | circa | 22 | 0 | 2.354 | 0.074–0.160 | 0.104 | N/A | {'UNSUPPORTED': 22} |
| trace_guard | torai | 22 | 0 | 1.997 | 0.067–0.109 | 0.093 | N/A | {'UNSUPPORTED': 22} |

RSS lấy mẫu cây tiến trình mỗi 0,1 s, tính theo MiB; có thể bỏ qua đỉnh ngắn hơn nhịp lấy mẫu. UNSUPPORTED mới tạo ở parent, không đo RSS riêng; pilot dùng lại có RSS cây tiến trình kiểm nguồn, không phải RSS phương pháp. N/A không có nghĩa 0 RAM. Thời gian UNSUPPORTED chỉ kiểm selector/hash và ghi metadata, không chạy method.

Pilot không nhãn: tổng 231,404 s, RSS đỉnh 526,5 MiB, 30 bản ghi (24 OK/6 UNSUPPORTED), nguồn `runs/pilot-001/summary.json`. Phép chiếu cũ main22+guard22 là 1545,454 s (25,8 phút), chưa gồm đổi mốc, kiểm/evaluator. Trước full đã khai thêm các phần đó và dùng lại pilot, scenario tổng 25–35 phút là chưa kiểm, không khoảng tin cậy. `new_supported_estimate_s` trong plan trừ thêm wall sáu unsupported pilot; đây là sai số nhỏ của phép chiếu, không thay danh sách hoặc thiết kế. Tổng thực tế ở bảng này dùng nguồn duy nhất.

Độ nhạy B tái dùng hoàn toàn 21 ca; A tái dùng 21 ca và có 6 record riêng cho ca đổi mốc; bảng cắt N có 66 trace-method records và 44 UNSUPPORTED riêng, BARO dùng lại 22 main. Không tự tạo tích chéo. MicroRank hashseed 1/locator và fixture/hồi quy hợp lệ đã giữ, không chạy lại. Nhánh cắt N giữ điểm dừng ERROR theo Q-77 và gói tiếp tục có điều kiện của Minh; lỗi trong `summary-continued-001.json` vẫn là lượt thực, không thời gian hoàn tất thành công.

Wall của kiểm nhãn giả, evaluator và xác minh cuối nằm trong `runs/session-005/timing.json`; RSS chỉ có ở các lượt được wrapper đo, không suy RSS chưa đo thành 0; không đưa công agent/chờ hội thoại vào runtime phương pháp. TIMEOUT 3600 s đã khai trước. Không sửa nguồn/code phương pháp, không payload dẫn xuất/bytecode mới. Clock/nền sạch/cadence vẫn là giới hạn khoa học.

## Chi phí kiểm, evaluator và tổng thời gian máy hoạt động

Nguồn `runs/session-005/timing.json`; coverage đối chiếu trường `elapsed_s` trong `runs/session-005/trace-N-coverage.json`. Các phần dưới là thời gian riêng của điều phối và kiểm/chấm, không cộng lại wall từng record.

| Phần | Giây |
| --- | --- |
| Điều phối lượt đầy đủ trước điểm dừng | 1830.887 |
| Điều phối phần MicroRank tiếp tục | 54.634 |
| Evaluator dùng nhãn giả trên cohort đủ | 7.368 |
| Xác minh trước chốt | 12.908 |
| Đo metadata nền trace | 76.213 |
| Evaluator thật và kiểm độc lập | 7.463 |

Tổng các phần máy hoạt động đã đo là 1989.472 s (33.16 phút), không cộng thời gian Minh/agent trao đổi hoặc chờ quyết định và không cộng pilot lịch sử. Đây là tổng các phần được liệt kê, không là thời gian tính riêng của phương pháp; wall nguồn duy nhất ở bảng trên gồm pilot được dùng lại và lượt ERROR, nên không cộng hai tổng này.

Chi phí/RSS của các tiến trình phụ đã hoàn tất trước lúc viết báo cáo:

| Thao tác | Wall s | RSS đỉnh MiB | Nguồn |
| --- | --- | --- | --- |
| coverage | 78.459 | 345.9000 | runs/aux-coverage-001/cost.json |
| evaluate | 7.463 | 171.4000 | runs/aux-evaluate-001/cost.json |

Những dòng này mô tả lại các phần kiểm/chấm trong tổng trên, không cộng thêm lần nữa. Chi phí của chính lượt viết báo cáo và xác minh sau bàn giao được wrapper ghi khi chúng kết thúc; khi chưa có file không suy thành 0 RAM hoặc 0 giây.

## Bổ sung sau khi báo cáo và xác minh đã kết thúc

Nguồn `runs/session-005/timing.json` (trường tương ứng) và `runs/aux-report-001/cost.json`, `runs/aux-final-verify-001/cost.json`.

| Phần bổ sung | Wall s | RSS đỉnh MiB |
| --- | --- | --- |
| Chốt manifest | 5.946 | N/A |
| Khởi động/thu wrapper coverage ngoài elapsed reader | 2.246 | N/A |
| Hai kiểm bằng chứng điểm dừng, kể cả kiểm lỗi index | 8.844 | N/A |
| Viết báo cáo | 0.508 | 42.2 |
| Xác minh cuối | 7.094 | 62.9 |

Tổng các phần máy đã liệt kê, gồm phần bổ sung trên: 2014.111 s (33.57 phút). Không cộng lại wall từng record hoặc các dòng auxiliary đã nằm trong tổng. Tổng này không gồm công agent, chờ hội thoại hoặc mọi thao tác đọc/kiểm metadata ngắn; không phải thời gian thực trôi qua của cả phiên. RSS của kiểm nhãn giả/trước chốt/chốt và kiểm bằng chứng không được lấy mẫu; N/A là chưa đo. Payload chỉ RAM, không có file cần xóa.
