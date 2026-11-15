# L5 — lỗi và sửa

## UI-01 — metadata bị cắt ở cửa sổ thường

- Quan sát thật: bảng 10 cột, hash/nguồn/cửa sổ/giới hạn bị cắt. URL trong nhật ký bước 3; ảnh `anh/001-meta-truoc-sua-p7-eb48d6b3.png`.
- Ảnh hưởng: khó xác định bản và nguồn kết quả; phần hiển thị G-c chưa đạt.
- Sửa trong `l4-dashboard.mjs`: panel 3 thành hai cột Trường/Giá trị, 10 dòng; xuống dòng, tăng chiều cao, đẩy panel phía dưới. Không đổi giá trị nguồn, hạng/cờ/cạnh, dashboard L3/G2.
- Dựng lại đúng hai JSON L4; giữ bản trước ở `grafana-l5/*-truoc-ui.json`. Triển khai qua Git SCP vào thư mục hiện hành sau chuyển folder. Hash trước/sau trong manifest máy cuối.
- API `api-meta-sua-1.json`: ba bản HTTP 200, không lỗi. Kiểm lại Chrome sẽ ghi trong đối chiếu hiển thị.

## ENV-01 — OpenSSH Windows từ chối ACL khóa

- Lệnh SSH đầu thất bại trước kết nối: unprotected private key / bad permissions.
- Dùng Git SSH đã ghi trong `results/T-058/dem-2026-11-10/remote.ps1`, thành công. Không đổi khóa, ACL hoặc file ngoài phạm vi.

## ENV-02 — địa chỉ public bị trình duyệt chặn

- Tạo tab mới tới public IP: ERR_BLOCKED_BY_CLIENT. Không đổi thiết lập bảo mật.
- Đọc metadata duy nhất tab Grafana của Minh để xác định origin `http://127.0.0.1:13000`; mở trên tab riêng 217960284 thành công. Không điều khiển tab Minh 217960254.

## ENV-03 — Node REPL timeout

- Lần đầu gọi node_repl đọc/băm nguồn hết 30 giây, kernel reset. Chuyển sang Node CLI có sẵn; kiểm 66 nguồn và 3.134 file L4 đạt. Không chạy lại M1.

## UI-03 — chữ trạng thái snapshot lỗi mã hóa và lời báo rỗng quá mạnh

- DOM ca `p7/e8661e0a` và các trang cùng ca có lời `Truy vấn … trả 0 chuỗi`. Snapshot L4 và phép đối chiếu API lúc tiếp nhận đều trả dữ liệu cho 10 quan sát rỗng trên cùng các dịch vụ và cửa sổ. Có 7 truy vấn nguồn khác nhau. Chưa có Query Inspector của đúng lượt Chrome để xác định trạng thái tải, tham số truy vấn hoặc lỗi hiển thị. Giữ loại (iii).
- Bảng snapshot có chuỗi kiểu `C? d? li?u` trong `du-lieu-l4/trang-thai/` và DOM. Chữ hỏng có từ file xuất, còn trạng thái, số dòng, giờ và truy vấn có thể đọc được. Lời `noValue` dài cũng xuất hiện ở ô thiếu giá trị của bảng hoặc một chuỗi metric, dù panel có dữ liệu. `doi-chieu-rong-snapshot.json` giữ cả những trường hợp bộ đếm cũ nhận nhầm.
- Đã dựng ứng viên `grafana-l5/ui03/` từ `dashboardL4({ui03:true})`. Ứng viên dùng ánh xạ nhãn trên trạng thái có sẵn và hướng người xem tới bảng snapshot khi panel hiển thị rỗng. Hạng, cờ, nguồn xuất và truy vấn sống giữ nguyên. Bản đang chạy còn ở `grafana-l4/`. Thay đổi ứng viên chưa triển khai vì cần Chrome để kiểm lại panel 24, 28, 31–35 và phát lại.

## ENV-04 — gián đoạn hạn mức sau khi mở Explore

- Lượt trước ghi sự kiện mở Prometheus cho `p7/00eaea92/booking-service`, thao tác `oc0d4761ef55d4ae54aa0`, trước khi đọc kết quả. `sau-tien-do.json` giữ tab `217960455`, truy vấn dự kiến và cửa sổ. Tab L5 chính là `217960284`. Sau hồi hạn mức, Browser Use báo `Local browser access is unavailable for this chat` khi kiểm tab và liệt kê browser. Trạng thái tab sau hồi hạn mức chưa kiểm được.
- Đã xác minh đủ 66 PNG, 66 bản đối chiếu qua 3 bản, 8 service, 16 thao tác và 39 liên kết đã hoàn tất. Giữ nguyên các phép kiểm đã lưu. Nếu tab phụ còn truy cập được, đọc nó từ checkpoint. Nếu tab phụ đã mất, mở lại riêng phép bấm Prometheus đang dở từ tab chính và ghi lần mới vào nhật ký.

## UI-02 — panel rỗng chỉ hiện dấu gạch

- Ảnh gốc: anh/004-canh-rong-p7-eb48d6b3.png; DOM có Panel data error message với chữ gạch, không phải lỗi truy vấn. Trạng thái cạnh ở trên đã nói không có đầu ra cạnh, nhưng chính bảng rỗng thiếu lời giải thích.
- Sửa noValue của các panel cạnh/cờ/bằng chứng/thao tác và năm truy vấn sống, chỉ giải thích kết quả rỗng hoặc cần chọn thao tác; không suy nguyên nhân. Thời điểm SCP xong: ui02-deploy-utc.txt. Không đổi truy vấn và số liệu.
- Kiểm lại bằng Chrome trong doi-chieu-hien-thi.json; API nguồn cũ vẫn được dùng để đối chiếu.



## 2026-11-14T07:02:49.3542647Z — lượt nối sau cập nhật Codex

- Chrome điều khiển được tab mới 217960473. Đọc lại đúng link Prometheus thứ 40.
- Bộ đếm instance cũ ghi đè bảng tổng hợp. Khôi phục 28 liên kết, 11 thao tác, 5 service, 2 lượt đổi bản từ nhật ký/DOM/ảnh. Thêm đối chiếu UTC trên đĩa trước khi lưu trong l5-sau.mjs.
- Loki V041/2e2a5541/payment-service/GET payment có log, editor tải muộn. Giữ ảnh/DOM lần chưa thấy editor, lần đọc lại khớp truy vấn 712 ký tự. Lượt Loki V032/00eaea92/booking-service/o24b7697fd9762cd664d5 có URL và No logs found, editor chưa hiện, cần bấm lại riêng.
- Ảnh đồ thị lấy sai vùng cuộn ở một số service. Đã thay thao tác focus/zoom trong bộ kiểm. Cần rà ảnh hiện có trước khi chụp bổ sung. UI-03 chưa triển khai.

- Ảnh phát lại V041/2e2a5541 cho thấy panel 7 cắt cả dòng giới hạn và chuỗi đáp án ở cửa sổ thường. DOM đã đọc đủ 6 đối chiếu chức năng. Phần đọc trực tiếp đáp án trên ảnh còn thiếu. Rà bố cục panel 7 trong lượt sửa giao diện và kiểm lại cả chiều mở/quay về.


## 2026-11-14T07:20:37.762Z — triển khai UI-03/UI-04, phần kiểm còn mở

- Lỗi gốc ở ảnh phát lại 167-phat-lai-V041-R1-H1c_H5b_H8s1-2e2a5541.png và chi tiết bảng trong DOM đã lưu. Bản mới dùng hai cột xuống dòng. Snapshot dùng nhãn ánh xạ từ trạng thái sẵn có, lời rỗng hướng kiểm snapshot. Hash và hoàn tác ở ui04-deploy.jsonl, thay-doi-may.md.
- API ui04-kiem.json đạt 12 slot. So source cho thấy target ngoài 7/24/28 giữ nguyên. Giữ phản hồi cũ khi so trường null từng bị comparator coi lệch. Chuẩn đọc null hiện đã xử lý, không ép thành giá trị số.
- Tách dữ liệu quan sát lịch sử khỏi cấu hình mới khi phân loại noValue, dùng backup JSON trước UI-04. Giữ đúng 177 loại i và 10 loại iii.
- Browser runtime báo quyền local browser của chat không khả dụng. Computer Use vào được tab Grafana rồi công cụ dừng theo chính sách xác định URL. Thử đã lưu trong ket-noi-chrome-0707.json. Kiểm Chrome sau sửa vẫn mở, status mot_phan.


## 2026-11-14T08:33:29.546Z — tiếp nhận chat mới

- Chrome CUA hoạt động; tab cũ không còn nên mở tab riêng.162 link đủ kiểm, editor Loki đọc lại đạt.
- Các lần đọc role/filter không đúng dòng, bảng op còn cũ và timeout CDP giữ trong nhật ký/tiep-nhan-*.json/graph-qa-runtime.jsonl. Adapter chỉ đổi cách điều khiển và chờ link; không đổi dashboard/M1.
- Rà36 ảnh graph cũ phát hiện nhiều ảnh lệch/cuộn/Computing layout. Giữ cũ, dùng lại2 ảnh đủ và bổ sung34 graph (54 ảnh/khung).9 graph lớn cần nhiều khung tại giới hạn zoom; hợp node nhìn thấy không thiếu. Đây là giới hạn xem graph, không mất đầu ra M1.
- Menu graph mở tab mới; focus panel24 ở tab View cũ thất bại. Đã đọc đúng tab mới và7/7 check đạt. Cổng13000 mất listener, mở tunnel riêng đã hồi. Máy không restart.
- Chưa sửa nguồn UI trong lượt. Chưa kiểm Chrome còn lại của UI04/phát lại/Inspector;10 quan sát cũ vẫn loạiiii, chưa quy nguyên nhân.


## 2026-11-14T08:46:18.857Z — quyền Chrome của chat chưa khả dụng

Ba lần thử trước thao tác trang cùng lỗi local browser access. Đã dừng sau ba lần; không có sửa UI hoặc quan sát mới trên trang. Chưa xác định nguyên nhân. Xem ket-noi-Chrome-tiep-UI04.json.

Rà khac cục bộ đạt; không thay nhãn hoặc phương pháp. Không chạy lại API/M1. Giữ 10 panel loại (iii) lịch sử và toàn bộ ảnh/DOM cũ. Phần Chrome UI-04/phát lại/Inspector chưa làm được.


## 2026-11-14T09:06:17.566951+00:00 — URL thời gian và Inspector hiện tại

UI06: đối chứng hiện tại cùng p7/e8661e0a/event-service/panel31: hard navigation numeric URL tạo request from/to NaN và step8760h; ISO cùng instant tạo from1794444870000/to1794445469999, step15s và40dòng/chuỗi. DOM/ảnh inspector-ui05-* giữ nguyên. Không suy nguyên nhân10quan sát lịch sử. Sửa nguồn và hai JSON L4: default time, header, biến ẩn và thời gian danh sách dùng ISO UTC; mọi panel live targets và panel7/24 targets không đổi. Deploy qua stdin SSH, không restart; hash/backup tại ui06-plan.json, ui06-deploy.jsonl và grafana-l5/ui06. Hoàn tác dùng /opt/flash-ticket-obs/rca-ket-qua/t065-l4-001/rollback/l5-ui06/ về vị trí ghi trong manifest deploy; source local có bản sao trước. Numeric bookmark cũ chưa được biến thành hợp lệ; cần ISO URL hoặc chọn ca sau bản sửa.


## 2026-11-14T09:26:52.372474+00:00 — kết quả UI05/UI06 và các lượt lỗi giữ lại

Xem BAO-CAO.md mục cùng giờ, ui05/06-plan.json và ui06-kiem-cuoi.json. Đã sửa race header và đường thời gian số tạo NaN ở phép kiểm hiện tại. Giữ loại(iii) lịch sử. Giữ ảnh trắng/cắt, bảng0dòng, clipboard0byte và các lỗi thao tác; chỉ ảnh View/Inspector cuối là bằng chứng đạt. Lỗi selector/timeout không tự là lỗi Grafana. V032 và V041 vẫn là bản đề xuất tạm/thay thế.

Không tiếp tục cách gộp mở drawer+chọn Query khi các lần trước mất trạng thái; chuyển sang ba công đoạn mở → Query → lưu ở các lượt CUA riêng. Với log lớn, bỏ thao tác snapshot toàn trang đã timeout, lưu toàn cây drawer. Bằng chứng kết quả hiện tại đầy đủ, không cần chạy query lại.
