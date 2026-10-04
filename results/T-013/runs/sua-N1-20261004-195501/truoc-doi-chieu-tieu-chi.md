# Đối chiếu tiêu chí xong và giới hạn

| Tiêu chí SPEC | Bằng chứng | Kết luận |
|---|---|---|
| 1. Hồ sơ 9 mục, defaults/công thức/so hai code | Ba ho-so-*.md; source refs; checks falling/dict/defaultdataset | Đủ; bài và code tách rõ |
| 2. Hai ca rule trước rank; từng score; mốc A | chon-ca.json; mọi *metric.csv/ranks.json; OB-README-A-cut243; T006-moc-A-reused | Sai số normalized0 ở hai ca; top 5README khớp. Nhãn root nối sau rank |
| 3. Detector và edge cases | posterior NPZ, detailJSON, nsigma CSV/hits, kiem-tra.json | Posterior sai số ≤2.23e-16; Nslist khớp. Không coi sentinel/NaN/[] hoặc false alarms làPASS nghiệp vụ |
| 4. Window và 3 leak paths | cua-so-cu.json, service-rank-ca.csv, cua-so-va-che-do-b.md | ChênhDELAY0.256; không chốtL; phân biệt hồi cứu/online |
| 5. CSV/file bắt buộc | yeu-cau-dau-vao.csv 16 cột; ca-da-chay; dinh-chinh; de-xuat | Đủ; các ca thật chỉ hai ca đã chọn; baselineIQR audit không chạy phương pháp toàn tập |
| 6. LOG/prompt/STATE | LOG append-only, mở phiên HEAD/ủyquyền/khối task; common+G1 trích nguyên văn; dòng T-013 | Bàn giao reviewer Claude; không sửa task cũ/common ngoài 1 dòng |
| 7. Kiểm diff/file set/parse | scripts/kiem_ban_giao.py, kiem-ban-giao.json, danh-sach-file.json | Kiểm trước/sau bàn giao; source/env cũ giữ nguyên |

Các phương pháp tất định đã kiểm lặp lại. Đảo cột giữ score, nhưng tie giữ thứ tự cột nên ranks có thể khác; N-Sigma detector list cũng khác dù multiset giữ nguyên. Hai prefix BOCPD chỉ có sentinel ngoài range; normal-normal ranker vẫn cho danh sách. Đây là kết quả **không đạt kỳ vọng hành vi** của các invariant ban đầu, đã tìm cơ chế, không sửa criterion để ép đạt.

## Chưa kiểm thực sự và hệ quả

- **BOCPD full TT:** T-005 đã vượt 1 giờ, task cấm lượt >1 giờ; T-013 chỉ kiểm prefix 120. Giả định cùng recurrence/pipeline cho chuỗi dài; sai nếu underflow, trạng thái/dimension hoặc chi phí phát sinh về sau. Kiểm được bằng task riêng có cấu hình/quy mô và ngân sách duyệt. Không kết luận full TT chạy đúng/khả thi.
- **Benchmark cả dataset mới và tác động bản sửa index:** thuộcP3/P4/G1, ngoài giới hạn. Bỏ riêng sentinel ở artifactOB được kiểm, chưa coi là cài hoàn chỉnh extraction mới. Chưa đo ảnh hưởng sửa indexing đến mọi changepoint thật.
- **Bảng bài vs lượt thực nghiệm tác giả, cấu hình N-Sigma savedSS:** artifact/code hiện có không cho biết đủ cấu hình. Có giả định phiên bản/columns/k khác; sai nếu bảng có lỗi chép hoặc file lưu thuộc lượt khác. Cần cấu hình/lượt thực nghiệm nguồn mới để phân xử; không dò tham số theo nhãn.
- **Chế độb hợp lệ và runtime chính thức:** chưa có recording được chọn độc lập lỗi/giao thứcG1 và máy rảnh. Không gọi case-level P/R/F1 hoặc seconds trên laptop bận là số đánh giá giám sát online.
- **WHY và tài liệu chung:** chỉ nháp vì prompt cấm ghi nguồn chung; chưa biến rule ca/mapping/protocol thành quyết địnhG1. Minh quyết việc đưa nháp vào nguồn chung.

Không để kiểm rẻ còn thiếu thành “chờ quyền”: IQR thô trên 90 baseline, same-input repeats, NaN/inf/hằng/hòa/đơn vị/tên cột/nền ngắn/prior/hazard/biên/normal control đều đã kiểm trong task. Không có quyết định khoa học mới được tự chốt.
