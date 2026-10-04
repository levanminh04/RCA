# Dung lượng thực và cách xử lý T-003

Đã tải đúng gói Q-47 và phần all-log có điều kiện của DeepTraLog. Tổng payload dataset: **5,477,786,503 byte (5,478 GB thập phân)**. Đây không phải tổng lưu lượng mạng mọi request. Nguồn, từng file, byte/hash và thời gian: [tổng kiểm](runs/resources-final-001/summary.json) và các download manifest được dẫn trong đó. Các lần thử lỗi vẫn giữ.

| Phần | File tải | Byte thực | Thời gian download của run (giây) |
|---|---:|---:|---:|
| Nezha | 1165 | 3,038,134,642 | 287.828 |
| Eadro | 2 | 127,676,922 | 204.672 |
| DeepTraLog base | 32 | 515,614,981 | 17.81 |
| DeepTraLog all-log | 5 | 213,216,632 | 7.75 |
| LEMMA IT sample | 4 | 1,583,143,326 | 27.54 |

## Sau giải nén

| Phần | Byte nội dung member | Phạm vi |
|---|---:|---|
| Nezha | 3.038.134.642 | CSV không nén, không cộng bản giải nén lần nữa |
| Eadro | 3,520,219,318 | File cuối CSV/JSON trong outer và nested; không gồm TAR header/padding, có biểu diễn trùng |
| DeepTraLog base | 7.517.863.017 | Raw/normal và graph: [mục lục](runs/sizes-001/archive-index-results.json), CRC và parsing ở T-010 |
| DeepTraLog all-log | 3.085.469.085 | Một member log, đọc tới EOF/CRC đạt: [inspect-007](../T-010/runs/inspect-007/summary.json) |
| LEMMA bốn ZIP IT | 17.500.872.729 | 2.431 member đọc tới EOF/CRC đạt: [báo cáo](../T-011/kiem-file.md) |

Tổng logical theo biểu diễn: 34,662,558,791 byte. Đây là lượng nội dung qua decompressor; **không phải số byte đang chiếm đĩa**, cũng không phải số quan sát độc lập. Eadro nested trùng outer được chứng minh bằng hash; không cộng chúng thành sự cố mới. Kiểm bằng streaming nên không cần ghi toàn bộ nội dung ra đĩa. Lượt mục lục cũ [sizes-summary-001](runs/sizes-summary-001/summary.json) chỉ cộng bảy XZ, bỏ phần GZip SN-all.tgz nên số 2,974 GB không phải cận trên cho toàn nested. Giữ lịch sử; số file cuối ở bảng này thay ước lượng thiếu đó. Sau bỏ bản nested trùng đã xác minh, Eadro có 2.305.204.734 byte file cuối duy nhất; [bảng byte và duplicate](../T-009/runs/inspect-004/logical-member-sizes.json).

## Hai máy, thời gian và giữ dữ liệu

Nezha/Eadro lưu laptop trong data/ngoai-rcaeval/. DeepTraLog/LEMMA lưu EC2 mới 3.26.62.217, /home/ubuntu/rca-t003/data/. Không dùng instance T-007. ZIP nguồn còn giữ; Deep có bản ZIP ghép trung gian nên cần cộng riêng khi đo đĩa. Không tải Original LEMMA hoặc OT, không tải telemetry Bank. [Kế hoạch/phạm vi đã thực hiện](ke-hoach-kiem-file.md) và [hướng dẫn dựng lại](../../data/README.md).

Thời gian kiểm thực được ghi riêng trong từng run: [Nezha](../T-008/the-dataset.md), [Eadro](../T-009/the-dataset.md), [DeepTraLog](../T-010/the-dataset.md), [LEMMA](../T-011/kiem-file.md). Các bước chồng thời gian, lần sửa tái dùng kết quả và lượt dừng không được cộng thành benchmark throughput toàn dataset. Chưa có số tiền AWS thực từ billing; không gán ước lượng thành chi phí hóa đơn. EC2 vẫn chạy, không tự Stop/terminate hoặc xóa sau khảo sát. Mục đích tải là kiểm file thật cho thẻ và cho phản biện tái lập, chưa chọn dataset thí nghiệm.

Kiểm sau khảo sát: [resource-postflight-001](runs/resource-postflight-001/result.json) SSH đọc df/du/free đạt. EC2 còn35.260.207.104byte, cây data T003 có2.707.156.934byte apparent; RAM available7.579.430.912byte. LaptopD còn53.388.070.912byte tại thời điểm đó. Apparent du và df available có cách tính khác; không gọi35GB là đủ tải toànOriginal86,6GB. Streaming đã giảm lượng cần lưu so với logical giải nén34,663GB toàn hai máy. Không xóa/StopEC2.


## Bổ sung sửa REVIEW — 04/10

[Resource snapshot mới](runs/review-propagation-001/resources.json): thêm628.411.611byte payload đạt checksum (AnoMod201.917.396/TRCA335.076.044/FSE91.418.171),6.464.210.793byte logical member; tổng gói6.106.198.114byte payload,41.126.769.584logicalbyte. Đây là tổng representation, khôngunique observations: TRCA duplicateNezha; artifact còn vendor/code/coverage. TRCA lượt1 bịthiếu20.804byte, giữ335.055.240bytefilelỗi; transferdataset quan sát cộng lỗi6.441.253.354byte, chưa tính metadata/range/env. Không giấu lượt lỗi.

Bank không tảifullZIP: metadata2.829.139.841byte nén/26.400.499.433logicalbyte; onlylabelrange đượcread. Streaming3archive khôngghi toàn cây vào ổ. Isolatedpyarrow23.0.1/tzdata2025.2 dưới data/ngoai-rcaeval/T-012/python-packages. Thời gian CRC+semantic ởvalidation nhánh; FSE132.609s,AnoMod161.594s,followup2.875s; downloadTRCAretry424.5s và lượtfailed1056.453s theo manifests. Thời gian parser không ngân sách RCA/adapter. KhôngStop/xóa EC2/nguồn.
