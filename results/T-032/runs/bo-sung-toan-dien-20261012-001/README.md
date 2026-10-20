# Gói bổ sung chung T-032 và T-033 — 12/10/2026

Intent: EXECUTE. Minh trực tiếp cho phép lập và thực hiện toàn bộ phần còn kiểm được, còn giá trị cho P5/P6 của hai task; không tạo task mới, không chờ duyệt từng bước, cho dùng tối đa subagent và chạy dài/qua đêm. Đây là bổ sung, không thay kết quả hoặc nghiệm thu lịch sử. Codex điều phối/người làm gói; ba subagent hỗ trợ (T32, T33, kiểm độc lập GPT 6.1 Sol ultra), không tự đổi vai trò phản biện lịch sử trong SPEC.

## Phạm vi và ảnh hưởng

- Chỉ tạo kết quả/script/thiết kế/manifest mới trong `results/T-032/runs/bo-sung-toan-dien-20261012-001/` và `results/T-033/runs/bo-sung-toan-dien-20261012-001/`.
- Chỉ nối DECISIONS, WHY, LOG hai task; STATE chỉ hai dòng T032/T033. Không sửa SPEC, nguồn/data/env/code dùng chung, bản ghi baseline, số P3, báo cáo cũ hoặc lịch sử phản biện. Không commit/push, không mở test/locked/heldout hay archive.
- Mỗi phép đổi là chẩn đoán hậu kiểm trên dev. Root/nhãn/proxy dùng để đối chiếu, không truyền vào phương pháp ngoài chế độ mốc đã biết hoặc thiết kế chẩn đoán công khai.
- Ghi từng câu nguồn → bằng chứng đã có → phép phân xử mới → kết quả/giới hạn → quyết định P5/P6. Không biến yêu cầu hoàn tất thành kết luận không có bằng chứng. Thiếu onset/trạng thái khỏe/clock/kênh chưa từng ghi có thể là giới hạn nhận diện, phải có nguồn xác nhận và chỉ đúng phép thử không thể phân xử.

## Danh mục phải đối chiếu

T032: mọi KT1–KT16 và các OPEN sau REVIEW. Trọng tâm mới: đáp ứng return/exception so nền tương đương; M-D partition→graph→W→counts→score và factorial W/count; ca ghép còn thiếu chuỗi; CIRCA giữ nút/cha, tách độ dài/vị trí học và giai đoạn chấm; quy tín hiệu span phía gọi sang phía được gọi; TORAI nguồn A; bản tác giả TraceRCA; mẫu P99 đơn lẻ; tổng hợp giới hạn vật lý/nhãn lan/thiếu cạnh. Phép đã có kết quả hợp lệ chỉ đối chiếu và tái dùng, không tính lại vô cớ.

T033: mọi K1–K7 trong kiem-tiep cùng SPEC và bổ sung sau review. Trọng tâm mới: prior/covariance/chiều có định nghĩa; causal preprocessing và tính nhất quán trạng thái; tác động lặp bậc thang và đồng hồ hazard; N-Sigma lịch sử/std0/NaN/OR nhiều cột; độ nhạy endpoint D trên dự đoán đã lưu; semantics/coverage/log theo cửa sổ; vai trò quan hệ và bằng chứng có thể/không thể phân xử onset thật/báo giả. Không chọn thiết kế P6 từ điểm đẹp hoặc nhận phép kiểm trên dev là đánh giá lợi ích graph trên test.

## Máy và phụ thuộc

- EC2 T032 `3.26.62.217`: RAM available khoảng 7,1 GiB, disk khoảng 19 GiB ở kiểm đầu. Worker T32 và phần đọc/tính nhỏ độc lập; ghi chỉ thư mục lượt mới dưới `~/rca/T-032/`.
- EC2 T033 `3.107.246.249`: RAM available khoảng 7,1 GiB, disk chỉ khoảng 1,4 GiB. Worker detector một tiến trình nặng, tái dùng X/raw/trung gian có sẵn; đầu ra m/CP/mapping/thống kê và posterior chọn điểm, không chép lại ma trận R toàn run. Không xóa để lấy chỗ.
- Laptop: kiểm/source/điều phối; nhánh MicroRank/CIRCA cần tái lập môi trường laptop hoặc chuyển dữ liệu lớn. Tối đa một tiến trình nghiên cứu nặng trên laptop; các nhánh laptop tuần tự để tránh tranh RAM/BLAS. RAM available đầu khoảng 4,3 GiB.
- Nguồn/hash → native sham/invariant → phép đổi → toán/số kiểm độc lập → diễn giải theo ca/ô → tổng hợp. Hai luồng T32/T33 độc lập chạy ngay; chỉ kết luận liên nhiệm vụ đợi cả hai.
- Dự toán CHƯA ĐO: T32 khoảng 15–60 phút tính mới và 1–3 giờ nguồn/diễn giải; T33 30 ca nhân nhiều nhánh detector có thể nhiều giờ/qua đêm. Pilot cập nhật thời gian tổng trước lô; không đặt timeout một giờ để bỏ nhóm khó. Agent báo trực tiếp khi có tiến trình laptop và dự kiến qua đêm.

## Kiểm toàn vẹn và toán

Lập snapshot hash toàn bộ file cũ trong results/src/docs/tasks trước sử dụng; loại đúng hai thư mục bổ sung mới. Manifest nguồn tương ứng vẫn kiểm trước kết luận. Hash final so snapshot chỉ được đổi file docs/log/state đã khai và phải bảo toàn prefix/bản trước. Giữ mọi lượt lỗi; không thay package/version để cứu số. Mẫu số cohort/OK/eligible tách; seed/ca/k/cặp đa nhãn không độc lập. Tách quan sát, cơ chế tính toán, ứng viên và dữ liệu không nhận diện được. Không cộng các cơ chế chồng lấn thành phần trăm nguyên nhân.

Các lựa chọn chẩn đoán mới ghi trong WHY trước dùng kết quả. Thiết kế chi tiết riêng nằm ở thư mục worker và ghi trước chạy phép đổi. Báo cáo cuối cùng phải ghi mọi câu nguồn và lý do chốt: đã phân xử / giới hạn dữ liệu có bằng chứng / kết luận thuộc P6–P7 chưa có thiết kế hay dữ liệu; không để phép kiểm hiện hữu có giá trị ở trạng thái chưa làm mà không báo.

KT7 bổ sung sau probe locked-window: trước kết luận phải dùng raw trace toàn case dev, lọc đúng start-bin15s của các hàngA source-A CSV (nguồnA lệch lưới so mốc). Native-window probe giữ nguyên; không diễn giải thiếu cây trongwindowkhác thành thiếu thông tin củasourceA. Không tái dựng threshold tácgiả từphỏngđoán.
