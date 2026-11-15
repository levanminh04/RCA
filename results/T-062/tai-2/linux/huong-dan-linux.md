# Dùng tải từ exp-obs

Python 3.12, thư viện chuẩn. Không cài thêm gói. Chạy bằng user `ubuntu`. Mã và mọi file mới trên exp-obs nằm trong `~/rca-dieu-phoi/`. Khóa dùng tại chỗ trong `keys/`, không chép sang máy khác.

```sh
cd ~/rca-dieu-phoi
python3 tai_linux.py test-duong
python3 tai_linux.py start --tag ma-moi --seconds 1800 --buoc-tai 600 --multiplier 3
python3 tai_linux.py get --tag ma-moi
python3 tai_linux.py receive --tag ma-moi
python3 tai_linux.py stop --tag ma-moi
```

Mỗi lệnh in đúng một dòng JSON. `ok=false` đi với exit khác 0. `get` trả trạng thái Docker tại `result.state`; chờ `Running=false`, xem `ExitCode` và `OOMKilled`. `ok=true` của `receive` xác nhận việc chép và kiểm hash; vẫn phải xem kết quả workload và trạng thái container.

`start` trả ngay sau khi Docker chạy nền. Không cần giữ phiên SSH hoặc mạng laptop. Không có `--buoc-tai`: nhịp cả lượt là chuẩn × multiplier. Có bậc: chuẩn trước mốc, chuẩn × multiplier sau mốc. Tỷ lệ, image và hai file k6 giữ từ cấu hình hiện hành. Không có tham số chọn kịch bản vì bản Linux chỉ phục vụ `hanh-trinh`.

`start` và `test-duong` từ chối khi còn container `rca-tai-` đang chạy. Preflight kiểm mock, supervisor và health 19091, khôi phục tiến trình đã biết nếu chết; giữ log/state/audit. Pool được cấp qua PKCE trên exp-app, truyền bằng pipe vào file bí mật hiện có trên máy tải. Start luôn cấp mới 20 phiên; có bậc cấp 40 phiên cho cùng 20 người mua. Hạn refresh tối thiểu phải lớn hơn mốc bậc + 60 giây. Token không ghi trên exp-obs. Đăng nhập xong mới ghi thời gian đầu lượt.

`receive` chỉ chạy khi container đã kết thúc. Bản gốc được giữ trên máy tải và chép vào `~/rca-dieu-phoi/tai-out/<tag>/`. Kiểm manifest SHA-256 ở cả hai đầu. Nhận lại giữ nguyên manifest và thời gian của lần xuất đầu. Lỗi chép/hash giữ dữ liệu đang có. Không tái sử dụng tag.

STOP của bộ chạy trên máy chủ đặt tại `~/rca-dieu-phoi/STOP`. Mọi SSH do bản Python phát bị từ chối khi file này tồn tại; `stop` vẫn hoạt động. File STOP trên laptop được kiểm bởi helper triển khai/kiểm từ laptop; Python trên máy chủ không đọc được tín hiệu mới của laptop khi mất mạng. Bộ điều phối chuyển thao tác STOP sang máy chủ theo nơi chạy mới. `stop --tag ...` chỉ chọn container đúng tag. Bỏ tag giữ hành vi PowerShell: dừng mọi container có tiền tố `rca-tai-` đang chạy.

Hai marker bảo trì `EXP-APP-BAO-TRI-1-BAT-DAU` và `EXP-APP-BAO-TRI-1-XONG` có bản sao tại thư mục mã. Start/test so thời gian dòng đầu; thiếu hoặc cũ hơn thì từ chối. Khi điều phối mở bảo trì mới, cập nhật marker tại nơi chạy trước khi cho chạy tiếp. Các marker không bị ghim vì là trạng thái điều phối có thể cập nhật.

`linux-source-manifest.json` ghi đường dẫn nguồn repo và hash. Mọi lệnh trừ stop khẩn cấp kiểm toàn bộ nguồn đã triển khai trước khi dùng. Triển khai từ repo bằng `Install-LinuxTai` trong `trien-khai-linux.ps1`; không sửa các file PowerShell tải cũ. Mỗi khi đổi nguồn cần phát lại pin và kiểm phần hành vi bị ảnh hưởng. `tai-linux-events.jsonl` ghi sự kiện, lệnh thay đổi, UTC và hash pool trước/sau; không ghi giá trị bí mật. Đối chiếu với `thay-doi-may.md` và `linux/deploy.json` trong repo.

Hoàn tác: ngừng gọi bản Python; bản PowerShell cũ còn nguyên. Giữ dữ liệu và log. Nếu cần dừng tải, chọn đúng tag đang được giao. Không sửa image, cấu hình ứng dụng hoặc firewall để hoàn tác bộ điều khiển.
