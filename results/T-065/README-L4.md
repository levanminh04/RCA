# T-065 L4 — chọn bản cho cùng ca

L4 giữ dashboard bản 6 và L3. Hai UID mới: `t065-l4-rca`, `t065-l4-phat-lai`. Dữ liệu mới: `/opt/flash-ticket-obs/rca-ket-qua/t065-l4-001/`. Provider hiện vẫn đặt dashboard trong folder Grafana `RCA`; không đổi provider. Thư mục dữ liệu là thư mục mới.

Nguồn chuẩn là `results/T-064/ban-xuat/chi-muc-ban.json`: ba bản, mỗi bản cùng 22 ca. Bộ xuất kiểm SHA của mọi đầu ra trước khi dùng. P7 có hai hash cấp bản là `null` trong chỉ mục: trang ca giữ đúng giá trị và chú thích nguồn chưa cấp; không suy hash cây mã từ hash file pin. Các hash từng đầu ra vẫn đã kiểm.

Giao diện đọc nguyên `entity_ranking`, `extra.kenh_co`, `extra.don_vi_phan_vi` và `extra.m1_ft.canh_xep_hang`. Cột nhóm thực thể là `tie_group + 1` theo quy ước L3, giữ thứ tự nguồn; không chấm lại. Cột `hang` của cạnh lấy nguyên nguồn, kể cả hạng có khoảng trống. P7 và V032 hiện “không có đầu ra cạnh”; cạnh cha–con của đồ thị thao tác là quan hệ quan sát riêng, không thay đầu ra cạnh M1-FT.

13 ca dev có trace/log/metric trong gói `results/T-063/thu2/ca/*.tgz`, kiểm hash theo `thu2/SHA256SUMS`. Chỉ trích đầu vào, metric, manifest vào `nguon-l4/`; raw trace đọc theo luồng từ archive, kiểm hash theo manifest ca trước khi dùng để phân loại thao tác và tạo metric route. Không bung thêm nhiều GB raw. Đây là xử lý dữ liệu đã lưu trên laptop; không có lượt tính M1 hay thực nghiệm nặng mới. Nguồn đã nằm ở laptop nên không chuyển dữ liệu qua máy khác để làm lại bước xuất nhỏ này.

Log thao tác dev chỉ là ngữ cảnh service. Chỉ có metric theo thao tác khi raw span có đủ route/method. Span link message chưa hỗ trợ. Phát lại 9 ca T-062 ghép riêng đáp án gốc, bỏ nhận xét/hạng chấm P7; giao diện không tự chấm. Dev chưa có nguồn đáp án được cấp cho lớp phát lại, nên hiện giới hạn thay vì dựng đáp án. Trang chính không đọc file phát lại.

Các file dữ liệu đầy đủ ở `<bản>/<ca>.json` và `thao-tac/`. File phục vụ Infinity ở `vue/` và `thao-tac-vue/` là phép chiếu của cùng dữ liệu, giảm đọc lặp tài liệu lớn cho mỗi panel. Không thay phương pháp hoặc kết quả nguồn. Định dạng mới là 0.4; schema ở `dinh-dang/schema-0.4.json`, không sửa schema 0.3 hay T-061.

`trang-thai/<ca>/<service>.json` lưu kết quả API của năm truy vấn sống, cùng giờ UTC và cửa sổ. Panel 28 chỉ đọc các trường sẵn có: `co_du_lieu`, `rong`, `loi`, số dòng, lời diễn giải. Rỗng chỉ có nghĩa không có dữ liệu khớp trong cửa sổ ở kho lúc kiểm; không suy nguyên nhân rỗng hay service khỏe. Snapshot dùng chung ba bản vì truy vấn và cửa sổ của cùng ca/service không đổi theo bản. Không thử thêm JSONata để suy trạng thái rỗng.

Mã và tái lập:

- `l4-xuat.mjs::buildL4()` xuất ba bản từ chỉ mục và đầu vào đã kiểm. Giữ số nguyên ns bằng `JSON.rawJSON`.
- `l4-raw.mjs::enrichRawL4()` đối chiếu raw span và bổ sung loại/route cho dev.
- `l4-vue.mjs::projectL4()` tạo phép chiếu phục vụ panel.
- `l4-dashboard.mjs::dashboardL4()` dựng hai dashboard.
- `l4-kiem.mjs::verifyL4()` so toàn bộ hạng/cờ/đơn vị/thao tác/URL với nguồn và hồi quy 9 ca P7; `verifyApiL4(<tên file>)` so từng dòng API/biến với dữ liệu xuất.
- `l4-api.py` chạy bằng Python trên exp-obs qua SSH stdin, không in credential. `snapshot` ghi tiến độ slot trong đúng thư mục L4, trả JSON trạng thái; `verify` giữ từng trang/biến để nhận tiếp; `links` gọi URL ba kho. Không chạy `snapshot` lại khi snapshot đã lưu còn đủ trả lời yêu cầu. Muốn làm snapshot mới phải giữ lượt cũ.

Trong Node REPL, import tuần tự các hàm trên từ đường dẫn tuyệt đối `file:///D:/RCA-flashticket/results/T-065/`. Chỉ tái dựng phần bị ảnh hưởng; không chạy lại M1. Lệnh SSH dùng khóa/known_hosts của brief L3, không chép khóa vào repo. Ví dụ gọi API kiểm:

```powershell
Get-Content -Raw -Encoding UTF8 results/T-065/l4-api.py | ssh -i D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key -o UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts -o StrictHostKeyChecking=yes ubuntu@213.35.116.128 "python3 - verify"
```

Lượt kiểm, lỗi giữ lại và giới hạn: `kiem/002/BAO-CAO.md`. Checkpoint: `CHECKPOINT.md`. Biên bản máy: `thay-doi-may.md`. Manifest gốc liệt kê tập file ổn định; log bộ gọi đang chạy được loại riêng. Chưa có bằng chứng bấm thật/ảnh vì browser host không khả dụng; API không thay kiểm render/href trong Grafana.


## L5 UI06 — 2026-11-14T09:26:52.372474+00:00

Điều hướng dashboard hiện hành dùng ISO UTC cho from/to, cả header, danh sách ca và biến thời gian ẩn. Phép kiểm hiện tại ghi nhận hard navigation bằng thời gian số tạo request NaN; cùng instant qua ISO có request hợp lệ. URL số cũ trong hồ sơ giữ làm lịch sử; để mở lại, đổi from/to sang ISO của đúng instant hoặc chọn ca từ danh sách hiện hành. Explore đã kiểm trước đó giữ nguyên.

Chỉ dựng dashboard: `node --input-type=module -e "import {dashboardL4} from './results/T-065/l4-dashboard.mjs'; await dashboardL4({outputFolder:'grafana-l5/ui06/rebuilt-final-fixed'});"`. Chọn thư mục đầu ra mới nếu cần giữ lượt cũ. Không cần chạy l4-xuat, raw, M1 hoặc snapshot. Bản dựng cuối đã so JSON: kiem/003-trinh-duyet/ui06-rebuild-final-check.json. Bằng chứng Chrome/Inspector ở BAO-CAO.md mục UI06; kiểm file đã lưu bằng `py -3 -X utf8 results/T-065/l5-ui06-validate.py`.
