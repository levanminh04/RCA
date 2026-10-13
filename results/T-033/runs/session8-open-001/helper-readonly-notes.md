# Ghi nhận trợ lý chỉ đọc — phiên 8

Đây là đầu vào hỗ trợ Codex người làm, không phải phản biện Claude chính thức. Không sửa nguồn, không EC2, không chạy detector. Người làm phải tự đối chiếu lại file thật trước khi dùng các scalar dưới đây trong báo cáo chính thức. Hash được trợ lý kiểm trước đọc: sáu file chứng cứ session8 (`bao-phu-nhom`, `chuoi-bang-chung`, `tai-log`, `nsigma-nguong-co-dinh`, `do-tre-sau-moc`, `digest`) theo inventory evidence; gzip `point_source` theo inventory extraction; context JSON/NPZ phiên6 theo inventory checkpoint phiên6. Hash nguồn và manifest nằm trong các inventory, không chép lại ở văn bản này.

## Các chuỗi cùng cột trợ lý đã đọc

- **dev-03d4910932/nsigma, security latency:** i124 x=0.0425, mean=0.039647744728389896, std=0.001627882853017031, margin=-0.0020313932874409853; i125 x=0.046875, mean=0.03967056277056278, std=0.0016412539339323835, margin=0.0022806754276400694. Cùng cột chuyển từ không vượt sang vượt. Workload raw 0.067→0.2 đồng xuất hiện; không có span/log service quan sát trong hai bin. Chưa xác định tải gây tăng latency.
- **dev-f81f88234e/nsigma, contacts latency:** i489 x=0.01371224481050681, mean=0.017449236628223272, std=0.001562369863702511, margin=-0.0009501177733910703; i490 x=0.009624476030349776, mean=0.017441610114309565, std=0.00156987515169026, margin=0.0031075086288890087. Quy tắc hai phía báo khi latency giảm đủ xa khỏi mean. Đã giải thích cờ tính toán; chưa chứng minh báo giả vận hành. Workload 0.667→0.933; không có span/log contacts quan sát trong hai bin.
- **dev-746fd74313/nsigma, inside-payment latency:** i100 x≈0.03125, mean=0.021316195030833887, std=0.00268066184112647, margin=0.0018918194457866952; i114 x=0.03125, mean=0.02308438160599463, std=0.005460126624224999, margin=-0.008214761478669626. Gói mean/std lịch sử đổi quyết định tại hai giá trị x gần như bằng nhau. Không tách riêng mean khỏi std. Workload raw cùng 0.067; không có span/log service quan sát trong hai bin.
- **dev-3defe3d34b/wide, N4:** i100 `ts-admin-route-service_socket` raw/x=4, n=100, mean=3, std=0, threshold=0, margin=1, flag True. i570 x=3, mean=3.066666666666667, std=0.24966292448837704, margin=-0.6823221067984643, False. Nhưng i100 còn 11 cột khác bật cờ. Std0 giải thích một nhánh OR, không là giải thích độc nhất merged alarm. Ca thiếu log; admin-route không có workload column/trace entity trong context.

Các cặp narrow còn lại đã đọc trong gzip:

| Ca rút gọn | Cột tại báo đầu | i báo / i không báo | margin báo / không báo |
|---|---|---|---|
| 12 | ui-dashboard latency | 101 / 100 | 0.02249454 / -0.02298036 |
| 14 | preserve latency | 107 / 106 | 0.02588038 / -0.43539731 |
| 168 | order latency | 102 / 101 | 0.00005847 / -0.00027571 |
| 1e | auth latency | 154 / 153 | 0.00370466 / -0.02349166 |
| 3ae | inside-payment latency | 100 / 117 | 0.01213499 / -0.01654452 |
| 575 | assurance latency | 100 / 107 | 0.00062005 / -0.00020730 |
| 801 | station latency | 101 / 100 | 0.00001813 / -0.00010598 |
| 98 | order-other latency | 102 / 101 | 0.00002683 / -0.00016455 |
| a505 | price latency | 106 / 105 | 0.00012073 / -0.00011555 |

Wide cùng cột đã đọc cho 03,12,14,165,168,1e,3def,a505,b8bd,bcbd. Ví dụ 03/config CPU i100 x=2.1054500412882122, mean=1.4374133344464197, std=0.21147625050019342, margin=0.0336079553412123; đối chứng i434 margin=-1.1842181489995514. Điểm này cách xa báo đầu; không gọi là lân cận hoặc nền sạch.

Đủ60 fixed_summary: first_updated_merged==first_fixed_merged. Freeze không hỗ trợ lời giải thích hẹp rằng cập nhật sau proxy làm báo đầu muộn hơn nền `[:720]`; không bác bỏ mọi tác động lịch sử/nền. Lịch cờ về sau đổi: 12/narrow thêm153/bớt19 điểm merged; 03/narrow thêm330/bớt0. Không suy fixed tốt hơn.

## Câu còn mở

- N1: tỷ lệ cờ đầu/cuối là mô tả; chưa phân xử thích ứng lịch sử với telemetry/coverage thật trên toàn nhóm.
- N2/N3: mật độ không là nguyên nhân. Margin giải thích cờ tại điểm, chưa là cơ chế chung cả nhóm.
- N4: tính toán std0 tại cột đã đọc được; nguồn vật lý/vai trò độc nhất merged chưa xác nhận.
- Matching cross-case ghi khác coverage ở mọi cặp, nhiều cặp khác ô/d. Đối chứng mô tả, không là can thiệp giữ mọi yếu tố.
- Wide N2/5, wide E-xa và hai nhóm native OK không có ca ngoài nhóm. Không bịa đối chứng.
- Wide first-post==proxy ở30 ca đều thuộc chuỗi báo bắt đầu trước proxy; narrow có11 ca theo digest. Không gọi là vừa phát hiện sự cố.

## Thiếu ở projection, nguồn còn đủ

1. Chuỗi rút gọn ở noalarm thường chỉ giữ một cột, có thể khác cột báo ở điểm cạnh. Phải đọc đúng cùng cột từ gzip đầy đủ.
2. V2 lọc `metric_*`, context lưu `workload_raw/workload_nan/workload_inf`; duration lưu `trace_group_duration_*`. Thiếu projection không phải thiếu instrumentation. Người làm đã bổ sung workload trên EC2 vào `session8-stats-001/workload-at-locked-points.json`; duration chưa được bổ sung vào chuỗi rút gọn.
3. Duration có trong NPZ phiên6: tra `trace_group_second==timestamp` và `trace_group_entity==vị trí service trong summary.trace.entities`. Ví dụ 168/order i101 count3 median_raw1793 max_raw4245; i102 count4 median_raw3449 max_raw7234. Đơn vị vật lý vẫn OPEN. 03/security và 3def/admin-route không có group duration ở điểm đang xét.
4. Các span quan sát trong ví dụ có status-present=0. Hai log mẫu đầu/cuối chỉ minh họa nội dung, không chứng minh cả bin không lỗi. Không đưa token/userID trong log vào văn bản công khai.

Căn cứ ở đây đủ trình quy tắc hai phía/OR/lịch sử/std0 như chuỗi tính toán ở điểm đã đọc, chưa đủ chọn ngưỡng/SLI hay khẳng định đồ thị sửa được hạn chế. Bảng theo ca, tổng hợp SPEC và căn cứ P6 vẫn OPEN.
