# Instrumentation — lượt nguồn 001, chưa khóa deployment

Q-120 cho phép truy nguồn ứng dụng và nơi tạo span. Đây là bước truy xuất nguồn, chưa xác nhận semantics của 22 ca Nezha hoặc 30 ca RE2. Không đổi `kha-nang-do-trace.json`, không gọi duration hay chồng lấn là chờ.

Nguồn chính thức [IntelligentDDS/Augmented-OnlineBoutique](https://github.com/IntelligentDDS/Augmented-OnlineBoutique) nêu ứng dụng được instrument cho nghiên cứu Nezha. Đã khóa snapshot bằng `git ls-remote`, lưu đúng revision và chín file nguồn; URL, thời điểm tải, bytes và hash ở `source-manifest.json#/rows`. Tổng tải 75.227 byte. GitHub API trả rate-limit 403, không dùng API lỗi làm căn cứ revision; lệnh Git chỉ đọc trả revision ở `ls-remote.txt`.

**FACT ở snapshot mã, chưa là FACT về deployment dataset:**

- `src/frontend/main.go:212` bọc HTTP handler bằng `otelhttp.NewHandler`; kết nối gRPC ở dòng238–239 gắn client interceptor. `src/frontend/handlers.go:402` gọi `PlaceOrder` và nhận kết quả trước bước xử lý sau. Cần lần đúng route của cặp caller/root đã khóa; một route không đại diện mọi request frontend.
- `src/checkoutservice/main.go:170` gắn server interceptor. `PlaceOrder` từ dòng197 lần lượt gọi chuẩn bị giỏ, charge, ship, empty cart, email rồi trả response. Trong thân hàm đã đọc không có goroutine tách các lời gọi ấy. Điều này xác định thứ tự thực thi ở snapshot, chưa xác định khoảng chờ từng RPC trong dữ liệu cũ.
- `chargeCard` dòng484–510 và `shipOrder` dòng562–581 tạo span nội bộ bằng `tracer.Start(ctx,...)`, `defer ...End()` rồi gọi RPC dùng `ctx`; biên span bao gồm tạo kết nối, log và xử lý khác, không đồng nhất toàn bộ span với chờ mạng/root.
- `convertCurrency` dòng454 tạo span từ `ctx`, nhưng lời gọi `Convert` dòng471 dùng `context.TODO()`. Đây là ứng viên mất nối context ở đường gọi này của snapshot. Chưa chứng minh deployment dữ liệu dùng mã này, chưa đối chiếu trace thô/route/parent, nên không quy lỗi dataset hay collector và không đổi kết luận ca.
- Frontend, checkout và shipping đều cấu hình `AlwaysSample` trong mã đã tải. Cấu hình source không chứng minh export/thu thập đầy đủ, không xác nhận đồng hồ hoặc span không mất.

**OPEN và hậu quả:** revision ứng dụng/image digest triển khai để tạo Nezha-OB dev chưa được nối với snapshot này. Dataset pin Nezha và revision code phương pháp RCA không thay thế revision ứng dụng. README còn mục Features về OpenCensus bên cạnh phần mô tả OpenTelemetry; dùng code cụ thể làm căn cứ snapshot, không lấy mô tả chung làm semantics mọi service. RE2-TT cũng chưa có revision ứng dụng triển khai được xác minh. Vì thế phần chờ vật lý và gắn semantics theo ca giữ OPEN, không dùng các quan sát source trên để khẳng định caller đang await root trong 52 ca.

Bước tiếp: kiểm nguồn paper/manifest công khai đã khóa để tìm commit/image digest tạo dữ liệu; nếu không có, ghi rõ thiếu deployment binding và trình Minh. Chỉ sau binding mới đọc đủ route/span cho các cặp caller/root đã khóa và đối chiếu raw allowlist, biên cửa sổ, parent resolve, clock/coverage. Không thay bằng latest hoặc suy từ tên operation. Các nhánh cơ chế tính toán vẫn tiếp tục độc lập.
