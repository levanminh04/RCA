# LEMMA-RCA — kế hoạch kiểm file sau metadata

**Q-47 đã được thực hiện: bốn ZIP tải đúng LFS/hash, toàn bộ member đã kiểm trong inspect-008 (tái dùng các lượt trước).** Xem [báo cáo kiểm](kiem-file.md), [summary](file-inspection-summary.json). Phần dưới giữ kế hoạch chọn trước số đo; mở rộng ngoài bốn ZIP chưa được duyệt. Q-49/WHY-13 bảo toàn OpenRCA Bank, không phải LEMMA. License NC/ND chính xác chưa giải quyết. Giao quyền của cả hai cho phép sao chép/kiểm nội bộ phi thương mại; không chia sẻ dataset hoặc payload đã biến đổi. Root ghi lý do trước tải đúng mẫu Q-47. Tất cả revision và LFS SHA-256 nằm trong [inventory](runs/run-001/inventory.csv).

## Mẫu khởi đầu theo mục tiêu

- Product Review 20211203: README tác giả chỉ rõ MongoDB-v1 và PPTX nhãn. Chọn để xác minh nhãn root, timezone JST/UTC, alias pod/service, metric–log alignment và cấu trúc NPY; không chọn vì nhỏ.
- Cloud Computing 20240124: có file nhãn riêng với epoch/time/entity/fault, chọn để kiểm thời gian và host/pod mapping ở hệ khác. Ca này không đại diện cho mọi schema Cloud.
- Dùng cả metric và log mỗi ca để kiểm cross-modality; chỉ schema chưa đủ xét triệu chứng. Nếu chưa quyền telemetry, tiếp nhận chỉ metadata/label đúng phạm vi, không parent-quality/graph/symptom.

| Dataset | File đề xuất | Byte | Mục tiêu |
|---|---|---:|---|
| Product_Review_Preprocessed | `Log Data/20211203.zip` | 1.327.897.003 | Mapping nhãn/clock và hai modality ở ca có nguồn nhãn |
| Product_Review_Preprocessed | `Metrics Data/20211203.zip` | 144.944.525 | Mapping nhãn/clock và hai modality ở ca có nguồn nhãn |
| Cloud_Computing_Preprocessed | `Log Data/20240124.zip` | 839.493 | Mapping nhãn/clock và hai modality ở ca có nguồn nhãn |
| Cloud_Computing_Preprocessed | `Metrics Data/20240124.zip` | 109.462.305 | Mapping nhãn/clock và hai modality ở ca có nguồn nhãn |

Tổng bốn ZIP đề xuất: **1.583.143.326 byte**. Mục lục ZIP đã được parent kiểm trong runs/sizes-001: tổng member 17.500.872.729 byte, đã được toàn bộ member đọc qua decompressor tới EOF/CRC; không extract nguyên cây. RAM và thời gian các lượt nằm trong kiem-file.md, không dùng lượt reuse như thời gian toàn scan. Chi tiết member và chi phí xem ../T-003/dung-luong-tai-va-giai-nen.md; không lặp tải mục lục.

## Phủ phần còn lại trước kết luận toàn release

Mẫu trên chỉ trả lời hai ca, chưa phủ nhiều root/fault/lặp. Các date token ở bảng sau là tầng metadata chưa biết schema; phải lấy nhãn/schema từng ngày trước, rồi kiểm ít nhất mỗi schema và mỗi root tại đúng ca root. Nếu so repetition phải kiểm đủ repetition. Không coi bốn/sáu date token là bốn/sáu incident khi chưa nhãn nội bộ.

| Dataset/biến thể | File | Byte | Phạm vi/dependency |
|---|---|---:|---|
| Product_Review_Original | `20210517.zip` | 14.040.008.257 | Original: truy schema/trace hoặc nhãn không còn ở Preprocessed; chưa duyệt tải |
| Product_Review_Original | `20210524.zip` | 11.721.862.708 | Original: truy schema/trace hoặc nhãn không còn ở Preprocessed; chưa duyệt tải |
| Product_Review_Original | `20211203.zip` | 18.012.496.133 | Original: truy schema/trace hoặc nhãn không còn ở Preprocessed; chưa duyệt tải |
| Product_Review_Original | `20220606.zip` | 9.859.441.848 | Original: truy schema/trace hoặc nhãn không còn ở Preprocessed; chưa duyệt tải |
| Product_Review_Preprocessed | `Log Data/20210517.zip` | 1.601.666.419 | Phủ ngày và kiểm mapping/schema trước khi suy toàn release |
| Product_Review_Preprocessed | `Log Data/20210524.zip` | 1.596.661.007 | Phủ ngày và kiểm mapping/schema trước khi suy toàn release |
| Product_Review_Preprocessed | `Log Data/20211203.zip` | 1.327.897.003 | Mẫu Q-47 đã duyệt; kiểm nội bộ phi thương mại theo giao quyền license |
| Product_Review_Preprocessed | `Log Data/20220606.zip` | 1.443.654.612 | Phủ ngày và kiểm mapping/schema trước khi suy toàn release |
| Product_Review_Preprocessed | `Metrics Data/20210517.zip` | 231.033.802 | Phủ ngày và kiểm mapping/schema trước khi suy toàn release |
| Product_Review_Preprocessed | `Metrics Data/20210524.zip` | 240.598.842 | Phủ ngày và kiểm mapping/schema trước khi suy toàn release |
| Product_Review_Preprocessed | `Metrics Data/20211203.zip` | 144.944.525 | Mẫu Q-47 đã duyệt; kiểm nội bộ phi thương mại theo giao quyền license |
| Product_Review_Preprocessed | `Metrics Data/20220606.zip` | 69.027.896 | Phủ ngày và kiểm mapping/schema trước khi suy toàn release |
| Cloud_Computing_Original | `20231207.zip` | 1.397.313.780 | Original: truy schema/trace hoặc nhãn không còn ở Preprocessed; chưa duyệt tải |
| Cloud_Computing_Original | `20231221.zip` | 11.862.407.960 | Original: truy schema/trace hoặc nhãn không còn ở Preprocessed; chưa duyệt tải |
| Cloud_Computing_Original | `20240115.zip` | 15.017.523.286 | Original: truy schema/trace hoặc nhãn không còn ở Preprocessed; chưa duyệt tải |
| Cloud_Computing_Original | `20240124.zip` | 698.928.495 | Original: truy schema/trace hoặc nhãn không còn ở Preprocessed; chưa duyệt tải |
| Cloud_Computing_Original | `20240207.zip` | 3.353.720.843 | Original: truy schema/trace hoặc nhãn không còn ở Preprocessed; chưa duyệt tải |
| Cloud_Computing_Original | `20240215.zip` | 672.237.705 | Original: truy schema/trace hoặc nhãn không còn ở Preprocessed; chưa duyệt tải |
| Cloud_Computing_Preprocessed | `Log Data/20231207.zip` | 277.339.693 | Phủ ngày và kiểm mapping/schema trước khi suy toàn release |
| Cloud_Computing_Preprocessed | `Log Data/20231221.zip` | 1.502.855.434 | Phủ ngày và kiểm mapping/schema trước khi suy toàn release |
| Cloud_Computing_Preprocessed | `Log Data/20240115.zip` | 2.283.508.927 | Phủ ngày và kiểm mapping/schema trước khi suy toàn release |
| Cloud_Computing_Preprocessed | `Log Data/20240124.zip` | 839.493 | Mẫu Q-47 đã duyệt; kiểm nội bộ phi thương mại theo giao quyền license |
| Cloud_Computing_Preprocessed | `Log Data/20240215.zip` | 47.710.432 | Phủ ngày và kiểm mapping/schema trước khi suy toàn release |
| Cloud_Computing_Preprocessed | `Metrics Data/20231207.zip` | 36.190.702 | Phủ ngày và kiểm mapping/schema trước khi suy toàn release |
| Cloud_Computing_Preprocessed | `Metrics Data/20231221.zip` | 87.942.904 | Phủ ngày và kiểm mapping/schema trước khi suy toàn release |
| Cloud_Computing_Preprocessed | `Metrics Data/20240115.zip` | 193.081.082 | Phủ ngày và kiểm mapping/schema trước khi suy toàn release |
| Cloud_Computing_Preprocessed | `Metrics Data/20240124.zip` | 109.462.305 | Mẫu Q-47 đã duyệt; kiểm nội bộ phi thương mại theo giao quyền license |
| Cloud_Computing_Preprocessed | `Metrics Data/20240207.zip` | 197.312.252 | Ngoại lệ CloudTrail, cần counterpart CSV raw/label; không suy không có log |
| Cloud_Computing_Preprocessed | `Metrics Data/20240215.zip` | 1.281.241 | Phủ ngày và kiểm mapping/schema trước khi suy toàn release |

Toàn bộ Preprocessed ZIP: 11.393.008.571 byte; toàn bộ Original ZIP: 86.635.941.015 byte. Đây là chi phí census file public, **không phải đề nghị tải trọn hoặc ngân sách đã duyệt**. Giới hạn >5 GB phải trình Minh.

Nếu cần kiểm trace thật, ưu tiên cùng ca có label 20211203/20240124 để đối chiếu raw–processed; bản Original tương ứng có byte chính xác trong bảng, PR lớn nên cần tìm metadata/member hoặc xin tác giả file riêng trước. Chưa có file sample độc lập công khai trong tree đã kiểm. Không tải Original chỉ để lấp ô “trace”. Có thể giữ trace OPEN nếu chưa quyền hoặc tác giả chưa làm rõ; không gọi “không có trace”.

OT bỏ hẳn khỏi phạm vi mới theo Q-47. Giữ catalog/nguồn lịch sử; không khảo sát, tải hoặc đề xuất dùng OT tiếp.

## Kiểm và tiếp nhận

Sau quyền phù hợp: kiểm hash/CRC/member sizes trước extract; giữ mọi lượt. Phân biệt label injection/onset; giữ clock gốc rồi đối chiếu JST/UTC; graph parent dùng khóa ghép; log ID cột/payload/match tách riêng. Chọn SLI độc lập nhãn; case-dependent selector trong code công bố không tự được phép. Đo normal/quality từng kênh, rồi q theo SPEC chỉ khi có quyền số đo. Lượt >1 giờ cần Minh cho phép.

Lệnh chỉ đọc kết quả đã có: `py -3 -B results/T-011/scripts/collect_metadata.py --verify --validate-counts`. Không chạy `--sources` đè lượt cũ. Build thẻ là bước ghi trong phạm vi SPEC; nguồn số là run-001.
