# T-054 — Đánh giá hai EC2 mới và phản biện kế hoạch tiếp theo

Ngày 07/11/2026. Codex làm, Claude phản biện theo SPEC. Đây là checkpoint012 trong pha chuẩn bị G3(a). Minh cấp hai máy và duyệt gói chuẩn bị gồm môi trường riêng, fixture và dev, nhận kết quả, hồ sơ và bàn giao.

## Bằng chứng trên hai máy mới

SSH dùng khóa máy chủ đã ghim và xác nhận hai instance khác nhau. Cả hai dùng Ubuntu 26.04.1, m7i-flex.large, 2 vCPU và khoảng 7,6 GiB RAM. Đĩa gốc lần lượt là 30 và 8 GiB. Python hệ thống 3.14.4. Môi trường M1 riêng dùng Python 3.12.3 và phiên bản các gói tính toán theo tuyến đã dùng ở T-025. Thư mục trên mỗi máy là `/home/ubuntu/rca-p7/T-054/checkpoint012/`. [Kiểm kê](inventory.json) · [Dựng máy đĩa lớn](ec2-large-disk-bootstrap.json) · [Dựng máy đĩa nhỏ](ec2-small-disk-bootstrap.json)

| Máy | Đĩa trống sau kiểm | M1 TT dev | RSS đỉnh | Khoảng giám sát dài nhất |
|---|---:|---:|---:|---:|
| 16.176.181.251 | 25,11 GiB | 69,34 giây | 1,65 GiB | 0,126 giây |
| 13.236.44.106 | 3,76 GiB | 68,31 giây | 1,65 GiB | 0,112 giây |
| Lượt EC2 cũ dùng làm đối chiếu | — | 66,98 giây | — | — |

Số thời gian là `wall_s` của một slot TT dev `dev-a915aa2424`, một worker mỗi máy. Đã đối chiếu cùng nguồn, cấu hình, seed và cửa sổ. Đầu vào chuẩn hóa và toàn bộ bản ghi M1 khớp giữa hai máy và với lượt EC2 cũ. Đầu ra dev được kiểm qua snapshot và receipt sau khi nhận về. Một ca và một vế chỉ phân xử tương đương của đúng tuyến này. Chưa có căn cứ nhân tốc độ đó lên toàn ma trận, hoặc áp cho hai worker, TORAI, BARO, MicroRank hay TraceRCA. [Thời gian và đối chiếu, `/hosts` và `/between_hosts`](comparison.json) · [RAM và giám sát, `/cloud`](resources.json)

Cả hai máy nhận gói 119 tệp đã ghim và xác minh hash trước khi chạy. Dữ liệu thật trong gói chỉ gồm ba tệp của ca TT dev đã duyệt, tổng 33.659.810 byte. OB đi qua reader và M1 trên fixture. File metric OB theo ngày có đoạn ngoài dev, nên dữ liệu OB thật cần quyền và phương án nguồn riêng trước khi thử tuyến cloud. [Phạm vi gói và pin](package.json) · [Nhận gói trên máy đĩa lớn](ec2-large-disk-stage.json) · [Nhận gói trên máy đĩa nhỏ](ec2-small-disk-stage.json)

Hai bộ fixture đạt 92 phép mỗi máy, gồm TT/OB, seal, khóa nguồn, giám sát, lỗi và điều kiện chặn A4. Wrapper lần đầu thoát mã 1 khi dùng hàm ghi mới để cập nhật `progress.json` đã tồn tại. M1 dev và fixture đã có kết quả đầy đủ trước lỗi đó. Kiểm lại 314 tệp trong mỗi archive và 16 envelope reader mỗi máy, sau đó dùng evaluator hiện có trên laptop để chấm lại hai bộ fixture. Hai bảng 89 dòng và A4 khớp từng byte. Bản ghi lần lỗi, file partial và đầu ra thu hồi đều được giữ. Lượt sau cần ghi trạng thái mỗi bước vào tệp riêng khi dùng hàm ghi mới. [Lượt máy đĩa lớn](ec2-large-disk-pilot.json) · [Lượt máy đĩa nhỏ](ec2-small-disk-pilot.json) · [Chấm sau khi nhận](fixture-score-parity.json)

RAM laptop lần đo cuối đủ hơn khoảng 339 MiB so với ngưỡng slot lớn nhất cộng dự phòng đã ghi ở 011. Cần đo lại lúc phát lô. RSS của M1 dev trên EC2 vượt số ước lượng slot lớn nhất ở 011. Cần cập nhật dự toán RAM theo nhóm việc trên đúng máy trước khi chọn hai worker. [Biên nhận tài nguyên, `/laptop` và `/cloud`](resources.json)

## Đánh giá kế hoạch Claude

N4 đúng. Lệnh cũ phụ thuộc PowerShell 7. Bản thay dùng `PSObject.Properties` đã kiểm 106/106 đầu ra bất biến trên Windows PowerShell 5.1 và được nối LOG. N1–N3 có đủ bằng chứng để dừng phản biện checkpoint011. Gói trình khóa cần lượt phản biện riêng vì máy và bằng chứng vận hành đã đổi.

| Mục | Đánh giá độc lập và đề xuất để Minh chốt |
|---|---|
| D1 — tiếp xúc 006 | Đồng ý khai riêng việc adapter OB được sửa sau khi dùng cấu trúc thời gian của chính cohort. Minh xác nhận phạm vi đã được giao lúc 006, hoặc xác nhận cách xử lý nếu quyền khi đó chưa đủ rõ. Ghi quyết định hiện tại và giữ ngày thực tế của lần đọc. Khi báo kết quả, giới hạn tính độc lập đối với thay đổi adapter. |
| D2 — H1 RE3 | Đồng ý để H1 mở riêng cho RE3 và cho TT/OB đi tiếp khi các điều kiện của hai bộ này đạt. Trước khi xem kết quả main, ghi quy tắc owner/alias từ bằng chứng nguồn đúng revision. Giữ tên tường minh, chỉ ánh xạ khi có căn cứ nguồn, dừng khi thiếu chủ sở hữu hoặc có xung đột. Mọi thay đổi lõi chung cần đánh giá lại ảnh hưởng đến TT/OB. |
| D3 — AC sleep | Khuyến nghị hoàn tác khi chưa có lịch chạy local, bằng script sẵn có. Cần Minh quyết việc đổi thiết lập Windows. Mốc đọc hiện tại cho thấy AC vẫn là 0. |
| D4 — độ nhạy OB | Đồng ý thêm bảng mô tả ngoài A4 nếu Minh chốt trước khi xem điểm. Cố định nhóm bốn ca bằng audit 006 và báo riêng chênh Hit@5 theo cặp cho 34 ca, 30 ca còn lại và nhóm bốn ca. Kèm mẫu số và diễn giải tập đích đã đổi. Giữ giả thuyết, chuyển mức và kết luận chính trên 34 ca theo A4. So sánh theo nhóm cho thấy mức phụ thuộc vào các ca đó, chưa tách tác động của adapter khỏi độ khó của ca. |
| D5 — môi trường trong gói khóa | Không nhận đề xuất tách môi trường khỏi gói khóa. Hai máy mới đã truy cập được. Bằng chứng 012 còn hẹp, nên nên ghim môi trường và hoàn tất đối chiếu các tuyến thay đổi trước trình khóa theo SPEC. Đánh giá máy và dựng môi trường có thể làm song song với các quyết định D1–D4. Chọn máy theo điều kiện dưới đây. |
| D6 — revision | Đồng ý cần revision tái dựng cho gói trình khóa. HEAD `dc01bc0d` không đủ để mô tả byte đã chạy. Dùng packet ghim để tái kiểm lượt 012. Đề xuất commit sau khi đã tách và kiểm chính xác diff cần đưa vào gói, rồi xin duyệt theo phạm vi file. |

### Phản biện lịch cloud của Claude

1. **Thiếu dữ liệu trên máy mới.** Bước chuyển năm ca TT giả định máy còn 30 ca đã chép. Hai instance mới chưa có dữ liệu dự án. Theo phân vùng cũ, role 35 ca cần 105 tệp TT, role 25 ca cần 75 tệp TT và role OB cần 226 tệp. Kiểm lại inventory trước khi truyền và chỉ truyền đúng nguồn, đích và quyền Minh cấp. Gói 012 chỉ vận chuyển một ca TT dev.
2. **Đĩa quyết định role ứng viên.** Theo cùng hệ số dự phòng đầu ra 4× của 011 và 2 GiB khoảng trống vận hành, 35 TT cần 5,27 GiB và 25 TT + OB cần 6,19 GiB, chưa tính môi trường còn thiếu và tệp tạm đang hoạt động. Máy đĩa lớn có thể xét cho role mang OB. Máy đĩa nhỏ thiếu khoảng 1,51 GiB ngay ở kịch bản 35 TT. Dùng lại 35/25 chỉ sau khi có đủ đĩa và parity. Nếu giữ ổ nhỏ, giảm lô trên máy đó rồi so lại đường găng, nguồn và chi phí nhận/chấm. Hệ số 4× là kịch bản lập kế hoạch. [Công thức và số byte, `/old_35_25_provisional_mapping`](resources.json)
3. **Tập trung kiểm đúng tuyến mới.** Kết quả TT dev và fixture 012 đã đủ cho tuyến M1 đã đo. Ưu tiên dựng và kiểm TORAI B với Python 3.8, các baseline thật và OB trên máy đích khi chốt quyền nguồn. Kiểm đầu vào chuẩn hóa, kết quả, phiên bản, tải đĩa và hai worker chỉ ở nhóm cần. Một tỷ lệ từ T-048 hoặc một ca M1 của 012 chưa đủ để chốt lịch toàn bộ. Laptop tiếp tục là nơi điều phối, nhận và chấm trong phương án hiện hành. Phương án chạy toàn bộ trên laptop giữ ở mức dự phòng vì RAM dao động và chưa có phép đo lịch đầy đủ.

Gói 012 xác nhận chuẩn bị và tương đương cho phần vừa kiểm. Trước khi trình G3 cần Minh xử lý D1–D4, chốt điều kiện đĩa và tuyến môi trường, hoàn tất gói ghim và grant riêng. Ở A4, 012 chỉ có số trên dữ liệu giả. RQ3b và RQ3d vẫn chờ dữ liệu test hợp lệ. RQ3a, độ đúng vùng và áp dụng FlashTicket giữ theo phạm vi MRP và DT18.
