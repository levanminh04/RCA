# T-065 L8b — G-c bản đề xuất cuối: dữ liệu/API đạt, UI mới chưa kiểm

2026-11-14T17:30:25.160Z. Codex người làm; Claude phản biện.

## Kết quả và phạm vi

Đã nối chỉ mục bản 2 sau đính chính T-064 vào bộ xuất và hai dashboard mới: t065-l8b-rca, t065-l8b-phat-lai. Ba bản p7, V082-V066+H8a và V071-V041+H8a dùng cùng 28 ca. Trang ca hiện trạng thái bản/chạy, hai quy ước hash cấu hình có tên riêng, hash mã nguồn/đầu ra và cửa sổ [t−300,t+300). Bảng thực thể/cờ/cạnh giữ dữ liệu nguồn; không có bước chấm lại.

V082 hiện “không có đầu ra cạnh”. Slot P7/ebd5ef38 hiện LOI_CHAY và đường dẫn loi_chay, không có hạng/cờ/thao tác giả. Cửa sổ điều hướng slot lỗi được ghi nguồn V082 cùng ca; P7 không sinh đầu ra. Trang chính và phát lại có dữ liệu tách riêng; đáp án chỉ nằm trong phát lại T-062.

Chặn L8 đã được điều phối sửa tại nguồn T-064. Đã tự kiểm hash chỉ mục mới, quy ước sha_cau_hinh, 56 metadata M1-FT và SHA byte 83 đầu ra. Các đầu ra và nội dung cấu hình giữ nguyên. Hồ sơ chặn L8 và hai bộ G-c thử trước giữ lịch sử. Nguồn đối chiếu: tiep-nhan.json#/index_sha256, /files; nguồn quyết định V082 là DECISIONS và WHY-98 đã đọc ở L8. L8b không thêm hoặc đổi quyết định nghiên cứu.

## Bằng chứng kiểm

- Bộ xuất: 84/84 slot, 1.410 dòng thực thể, 1.652 cờ, 26.266 đơn vị, 600 dòng cạnh xếp hạng và 19.971 dòng thao tác theo slot. Kiểm đủ thứ tự, khóa, tie_group, cờ từng thao tác/đơn vị, số mẫu, vùng, phép chiếu service và ns nguyên. Nguồn: may-l8b/kiem/kiem-xuat.json#/cases, /totals, /rows; đường dẫn chuẩn từ results/T-065 là may-l8b/kiem/kiem-xuat.json.
- Schema 0.5 đạt 84/84, gồm nhánh lỗi chạy có các mảng kết quả rỗng. Nguồn: may-l8b/kiem/kiem-schema.json#/passed. Schema ở dinh-dang/0.5/ca.schema.json; bộ kiểm ngữ nghĩa ở codex/l8b-kiem.py.
- 48.927 URL giải mã đúng một lần, đúng datasource/query/cửa sổ; hồi quy thao tác/đồ thị P7 của 9 ca T-062 đạt. Nguồn: may-l8b/kiem/kiem-xuat.json#/urls_decoded_once, /T062_P7_regression và /rows.
- API: 18/18 trang = ba bản × ba ca × chính/phát lại; 315 target/biến được đối chiếu. Mẫu 86dea661 có cạnh V071, ebd5ef38 phủ lỗi P7 và hai bản có đầu ra, 00eaea92 thuộc T-062. Kiểm hạng/cờ/cạnh, thông báo vắng cạnh, metadata/hash/window và biến chọn bản/ca/service/op. Nguồn: may-l8b/kiem/kiem-api.json#/pages, /rows và api-slots/; số target tổng ở tom-tat.json#/API_targets.
- Liên kết: 33 mẫu Tempo/Loki/Prometheus có dữ liệu, từ 12 request mới. Các mẫu còn lại dùng lại request/query/window trùng hệt và giữ giờ truy vấn gốc; không tính là bấm thật. P7 lỗi chạy không dựng link. Nguồn: may-l8b/kiem/kiem-links.json#/samples, /new_requests, /rows và link-requests/.
- Snapshot 20 query ở bốn ca/service mẫu: 15 có dữ liệu, 5 rỗng, 0 lỗi. Bảng panel 28 khớp request/response và cửa sổ. Nguồn: may-l8b/kiem/kiem-live.json#/rows, live-slots/ và live-panel28/. Các snapshot khác giữ giờ cũ hoặc ghi chua_truy_van.
- Sáu ca dev3 có raw trace/log và metric hiện có trên exp-obs. Đã kiểm raw theo manifest gói; 1.503.009 span nằm trong miền, trung gian span khớp đầu ra ở các bản có kết quả. Liên kết thao tác dùng owner/tên/route quan sát, log là ngữ cảnh service, metric lưu nguyên biểu thức có nguồn. Chi tiết: may-l8b/kiem/dev3/<ca>.json#/files, /spans; manifest nguồn lưu may-l8b/nguon-dev3/<ca>/manifest.json. Span link message vẫn chưa hỗ trợ. Chỉ nhận bộ xuất, không tải raw về laptop.

## Lỗi đã gặp và sửa

API lượt đầu phát hiện biến service trả chuỗi chứa mảng một phần tử thay vì tên service. Lần lỗi giữ trong codex/l8b-api-luot-001.txt và may-l8b/kiem/api-luot/p7/86dea661/. Đọc response cho thấy JSONata dùng $ trên mảng chuỗi tạo giá trị mảng; thay bằng service_options gồm trường ma/ten do bộ xuất cấp sẵn. Chỉ thêm projection service vào 168 file case/vue và đổi biến của hai dashboard mới; giữ số M1, raw và dữ liệu thử cũ. Dashboard trước sửa giữ trong may-l8b/rollback/fix01; hash trước/sau tại may-l8b/kiem/deploy-fix01.json và fix01-service-options.json. Sau sửa: kiểm ngữ nghĩa 84 slot và 18 trang API đạt.

Một lần SCP vào thư mục kiểm mới do root sở hữu bị từ chối; đã nhận pin lịch sử qua thư mục gốc mới thuộc ubuntu, không đổi quyền/thư mục cũ. Lần kiểm nguồn đầu có lỗi cú pháp biểu thức Node trước tác động, đã sửa và kiểm đủ. PSDrive không trả số dung lượng; DriveInfo xác nhận đủ chỗ trước nhận gói. Các lỗi công cụ/thu nhận không là kết quả phương pháp.

## Thay đổi máy, toàn vẹn và tiếp nhận

Chỉ thêm thư mục /opt/flash-ticket-obs/rca-ket-qua/t065-l8b-001 và hai file provisioning L8b trong thư mục kết quả hiện hành. Grafana tự nạp; không restart. 3.019 file máy có trước và 91 file hồ sơ L8 giữ hash. Hash hai dashboard mới, trước/sau fix01 và trạng thái máy ở may-l8b/kiem/may-sau.json, deploy.json, deploy-fix01.json. Không đổi compose/provider/datasource/Collector hoặc kho quan sát.

Gói nhận nén 21.195.332 byte; SHA hai đầu và 2.477 file trong manifest máy khớp. Nguồn: nhan-goi.json và kiem-nhan-goi.json#/files_verified. Gói cùng snapshot nguồn nằm trong codex/l8b-ban-giao-001.tgz; bản giải ở may-l8b/. Hash đầy đủ nằm trong manifest/JSON, không rải vào báo cáo.

## Giới hạn và bước tiếp

FACT: dữ liệu/API đạt các phép kiểm trên. Chưa bấm hoặc chụp ảnh Chrome cho hai UID mới trong lượt CLI. Ảnh L4–L7 giữ là lịch sử. Bước app ở codex/L8b-app-brief.md: mở đúng UID/cửa sổ ISO, đổi bản giữ ca, kiểm trang lỗi chạy và các data link đã đổi nguồn. Đây là bằng chứng UI còn thiếu trước khi khẳng định trọn luồng thao tác mới; dự kiến chưa kiểm 15–30 phút nếu Chrome/tunnel sẵn. Không cần chạy lại M1/raw hoặc các mẫu API đã đạt khi nguồn/target không đổi.

Các query rỗng chỉ chứng minh không có dữ liệu khớp ở kho tại giờ ghi. Chưa phân xử không phát sinh chuỗi, nhãn/query khác hoặc retention; raw của gói có không xác định được hiện trạng index của kho. Muốn quy nguyên nhân cần đối chiếu request với series/log/trace được lưu tại cùng giờ và cấu hình retention/nhãn tương ứng. Kết luận nguyên nhân rỗng vẫn OPEN; việc này không được thay bằng suy đoán collector hỏng.

Đề nghị Claude kiểm lại L6/L7 và L8/L8b theo prompt gộp; Minh quyết nghiệm thu T-065 sau phần UI cần thiết. T-065 còn một phần. G-c ở lượt này trả lời khả năng truy vết/hiển thị đầu ra cuối; RQ5 và hiệu quả phương pháp cần bằng chứng nghiên cứu của T-064/P10. Các giới hạn lựa chọn V082 giữ theo nguồn. Không mở dữ liệu khóa, không ghi STATE/docs/SPEC/REVIEW/src/T-064, không commit/push.


## Ghi chú chốt manifest

Bản kết quả L8 từng dùng tên codex/L8-trang-thai.json. Bộ gọi đã ghi đè tên đó bằng trạng thái tiến trình lúc 16:55:52Z, trước lượt L8b. Kiểm cuối phát hiện lệch checksum; chưa ghi manifest mới trong lần chốt lỗi. Đã tái dựng đúng byte bản kết quả L8 từ nội dung đã ghi và xác nhận SHA/byte khớp manifest trước, lưu codex/L8-ket-qua-lich-su.json. Kết quả L8b lưu codex/L8b-ket-qua.json. Giữ hai tên trang-thai cho bộ gọi, không ghim chúng làm kết quả bền. Biên bản: doi-chieu-tep-dieu-phoi.json. Không ảnh hưởng số, dữ liệu hoặc dashboard; manifest trước giữ nguyên.
