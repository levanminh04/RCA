# V5 bổ sung, lượt sửa thứ năm (14/10/2026)

Phép đọc, không phải phép máy. Bản trước: `results/T-034/runs/phat-hanh-005/`. Lượt dựng dùng để phát hành: `g2-build-007`.

## Vì sao có lượt này

Minh hỏi vì sao còn chỗ chưa đạt tiêu chí xong của SPEC theo chữ. Kiểm lại thì thấy:

- G2-H19 vẫn ghi "không tách theo ô" trong khi nguồn có mức đo được theo từng ca. Người làm đã bỏ sót dòng này ở các báo cáo trước.
- G2-H24 ghi "không tách theo ô" theo hướng coi là giới hạn chung; phần mô tả theo mốc tiêm vẫn tách được.
- Các thành phần DT18 yêu cầu nằm trong danh sách ứng viên (UV-10) dù không có dự đoán kiểm được trên dev.

## Điều đã đổi và căn cứ

| Chỗ | Nội dung | Nguồn và phép kiểm |
|---|---|---|
| G2-H19; Phụ lục C | Bảng theo ô cho hai dataset: số ca "đo được / đo được một phần / không đo được" | `results/T-032/kha-nang-do-trace.json#/ca`; tổng theo ô ghi ở `runs/g2-build-007/t032-dan-xuat.json#/by_cell`; bước dựng tự kiểm tổng số ca và tổng "không đo được" |
| G2-H24; Phụ lục C | Bảng theo ô: số ca BOCPD có ít nhất một điểm đổi trong D giây sau mốc tiêm, năm mức D | Tính lại từ `engine-final-summary-001.json#/slots` (trường `native_alarm_times`) và mốc tiêm ở `results/T-022/nhan-dev.json`; ghi ở `runs/g2-build-007/t033-dan-xuat.json#/bocpd_post_any_by_cell`; bước dựng tự kiểm tổng 10 ô bằng đúng dãy của `fast-summary-001.json#/bocpd_post_any_byD` |
| Mục 5 | UV-10 đổi thành mục con "Thành phần DT18 yêu cầu (không phải ứng viên rút từ P4)"; nội dung giữ nguyên | Tiêu chí xong của K5 áp cho ứng viên |

## Giới hạn và điều cần nói rõ

- **Nguồn của bảng G2-H24 khác nguồn T-033 đã dùng để ra dãy tổng.** T-033 cộng từ 30 file `dev-<ca>--context.json`; trên laptop chỉ có 1 trong 30 file đó khớp mã băm ghi trong `fast-summary-001.json` (29 file còn lại không có ở máy này). Người làm vì vậy tính lại từ thời điểm điểm đổi đã lưu trong `engine-final-summary-001.json`. Phép tính lại khớp cả năm tổng (12, 23, 27, 29, 30) và khớp ca duy nhất có file gốc. Đây là khớp ở mức tổng và một ca, không phải đối chiếu từng ca với file gốc.
- Bảng G2-H24 dùng mốc tiêm của nhãn dev để đếm. Nhãn chỉ dùng để chấm và phân tích, không vào phương pháp.
- Bảng G2-H24 không cho biết lúc sự cố bắt đầu có tác động hay lúc hết lỗi; mỗi ô ba ca.
- **Chưa làm một phần của B8:** chuyển phần (ii) của UV-7 (cách gộp điểm) ra khỏi mục ứng viên. Đề xuất đã duyệt ghi "mục 6.3", nhưng mục 6.3 là "thuộc đánh giá sau khi khóa thiết kế", còn cách gộp điểm là câu hỏi thiết kế trên dev, trước khi khóa. Đặt vào 6.3 là xếp sai loại; đặt vào 6.1 là làm khác đề xuất. Người làm dừng phần này, chờ Minh quyết. Hiện UV-7 vẫn ghi phần (ii) là "câu hỏi thiết kế, chưa là ứng viên".

## Điều không đổi

Số của bảng baseline, `hai-phep-kiem.md`, `hai-phep-kiem.json`, `bang-baseline.json`. Các câu còn mở như ở bản V5 bổ sung thứ tư.
