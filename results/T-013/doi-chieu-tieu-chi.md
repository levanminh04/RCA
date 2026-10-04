# Đối chiếu tiêu chí xong và giới hạn

| Tiêu chí SPEC | Bằng chứng | Kết luận |
|---|---|---|
| 1. Hồ sơ 9 mục, defaults/công thức/so hai code | Ba ho-so-*.md; source refs; checks falling/dict/defaultdataset | Đủ; bài và code tách rõ |
| 2. Hai ca rule trước rank; từng score; mốc A | chon-ca.json; mọi *metric.csv/ranks.json; OB-README-A-cut243; T006-moc-A-reused | Sai số normalized0 ở hai ca; top 5README khớp. Nhãn root nối sau rank |
| 3. Detector và edge cases | posterior NPZ, detailJSON, nsigma CSV/hits, kiem-tra.json; runs/sua-N1-20261004-195501/ket-qua.json | Posterior sai số ≤2.23e-16; Nslist khớp. Sửa helper gần hằng, kiểm 8 synthetic và 1.316 điểm thật; câu điều kiện pandas/BOCPD đã sửa. Sentinel/NaN/[] và false alarms không là PASS nghiệp vụ |
| 4. Window và 3 leak paths | cua-so-cu.json; trung-gian/cua-so-delay-ca.csv, -metric.csv, -variants.csv, -summary.json; cua-so-va-che-do-b.md §1–3 | Đã sửa R1: đủ 25 DELAY × 4 phối hợp, 50 endpoint khớp từng metric/service rank, 100 kiểm lặp/đảo cột giữ điểm. Phân bổ hai thứ tự: nền −0,240, hậu −0,016; bao gồm đổi candidate, không là nhân quả hoặc lựa chọn L |
| 5. CSV/file bắt buộc | yeu-cau-dau-vao.csv 16 cột; ca-da-chay; dinh-chinh; de-xuat | Đủ. Hai ca gốc vẫn là ví dụ chạy code tác giả; bổ sung số học 25 DELAY đã chạy T-006 để sửa R1, không benchmark mới. Mọi run được giữ |
| 6. LOG/prompt/STATE | LOG append-only, mở phiên HEAD/ủyquyền/khối task; common+G1 lịch sử trích nguyên văn; bảng phản hồi REVIEW; dòng T-013 | Đã thực hiện sửa theo Minh 04/10/2026; Minh đã duyệt đóng task. Không sửa thân REVIEW, task cũ hoặc nguồn chung ngoài đúng dòng STATE |
| 7. Kiểm diff/file set/parse | scripts/kiem_ban_giao.py, kiem-ban-giao.json, danh-sach-file.json | Kiểm trước/sau bàn giao; source/env cũ giữ nguyên |

Các phương pháp tất định đã kiểm lặp lại. Đảo cột giữ score, nhưng tie giữ thứ tự cột nên ranks có thể khác; N-Sigma detector list cũng khác dù multiset giữ nguyên. Hai prefix BOCPD chỉ có sentinel ngoài range; normal-normal ranker vẫn cho danh sách. Đây là kết quả **không đạt kỳ vọng hành vi** của các invariant ban đầu, đã tìm cơ chế, không sửa criterion để ép đạt.

## Kiểm sau sửa phản biện — 04/10/2026

- **N1:** phản ví dụ gần hằng trước sửa cho điểm 5,057563; helper sửa và StandardScaler ghim cùng cho 18, scale hiệu dụng 1. Tám cấu hình hai ca × hai cửa sổ × BR/RE khớp cả 1.316 điểm chính thức, sai số normalized 0; so điểm lịch sử sai số lớn nhất 2,35e-16, mọi thứ hạng giữ nguyên. Nguồn: `runs/sua-N1-20261004-195501/ket-qua.json` và tám CSV/ranks cùng run. Không ghi đè điểm lịch sử.
- **N2/N3:** pandas count 3 nhưng chỉ 2 giá trị hữu hạn trong phản ví dụ; BOCPD core có mass 0 và posterior NaN, còn mass dương cho (0,02; 0,98). Hai câu đã bổ sung đúng điều kiện. Đây là kiểm xác nhận giới hạn, không gọi NaN là đầu ra hợp lệ hoặc suy wrapper cũng lỗi.
- **R1:** bốn Avg@5 là 0,936 / 0,712 / 0,936 / 0,680; tổng đóng góp 25 ca bằng −0,256. Bốn ca đổi tập candidate. Trung gian từng metric và ba ca diễn giải ở §1 đã nối số với cơ chế; mẫu top memory không được gọi là nguyên nhân lỗi. Lựa chọn hạch toán hai thứ tự chờ WHY trong nháp nguồn chung.

19 phép kiểm tập trung N1–N3 đạt. R1 có 50 endpoint và 100 phối hợp đạt các kiểm số học, lặp lại và đảo cột. Các kết quả này hoàn tất sửa đã duyệt; không thay các giới hạn dưới đây và Minh đã duyệt đóng task sau khi xem kết quả sửa.

## Chưa kiểm thực sự và hệ quả

- **BOCPD full TT:** T-005 đã vượt 1 giờ, task cấm lượt >1 giờ; T-013 chỉ kiểm prefix 120. Giả định cùng recurrence/pipeline cho chuỗi dài; sai nếu underflow, trạng thái/dimension hoặc chi phí phát sinh về sau. Kiểm được bằng task riêng có cấu hình/quy mô và ngân sách duyệt. Không kết luận full TT chạy đúng/khả thi.
- **Benchmark cả dataset mới và tác động bản sửa index:** thuộcP3/P4/G1, ngoài giới hạn. Bỏ riêng sentinel ở artifactOB được kiểm, chưa coi là cài hoàn chỉnh extraction mới. Chưa đo ảnh hưởng sửa indexing đến mọi changepoint thật.
- **Bảng bài vs lượt thực nghiệm tác giả, cấu hình N-Sigma savedSS:** artifact/code hiện có không cho biết đủ cấu hình. Có giả định phiên bản/columns/k khác; sai nếu bảng có lỗi chép hoặc file lưu thuộc lượt khác. Cần cấu hình/lượt thực nghiệm nguồn mới để phân xử; không dò tham số theo nhãn.
- **Chế độb hợp lệ và runtime chính thức:** chưa có recording được chọn độc lập lỗi/giao thứcG1 và máy rảnh. Không gọi case-level P/R/F1 hoặc seconds trên laptop bận là số đánh giá giám sát online.
- **WHY và tài liệu chung:** chỉ nháp vì prompt cấm ghi nguồn chung; chưa biến rule ca/mapping/protocol thành quyết địnhG1. Minh quyết việc đưa nháp vào nguồn chung.

Không để kiểm rẻ còn thiếu thành “chờ quyền”: IQR thô trên 90 baseline, same-input repeats, NaN/inf/hằng/hòa/đơn vị/tên cột/nền ngắn/prior/hazard/biên/normal control đều đã kiểm trong task. Không có quyết định khoa học mới được tự chốt.
