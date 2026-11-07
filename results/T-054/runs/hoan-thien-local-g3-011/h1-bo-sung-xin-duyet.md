# Hai phạm vi H1 cần Minh quyết — chưa thực hiện

## A. Sửa guard status RE3 theo nguồn tác giả mới

Nguồn chính thức mới: `docs/CONVERT.md` của RCAEval ở revision ghi trong `upstream-main-ref.json`, mục Traces và Derived series. Tác giả khai các dataset phát hành lưu mã trạng thái gRPC, 0 là OK; bảng lỗi cũ cộng giá trị mã thay vì đếm span lỗi. Đây không phải cờ nhị phân0/1.

H2 hiện chỉ cho `trace_status_kind=binary_error` vào TORAI RE3 và từ chối mã khác0/1. Guard này là giả định phòng lỗi, chưa có căn cứ từ benchmark; nguồn mới cho thấy nó có thể chặn dữ liệu đúng định dạng. Kernel TORAI đã ghim vốn cộng mã; không đổi kernel hoặc biến phép cộng ấy thành đếm lỗi.

Đề xuất đúng hai file code:

- `src/p3/re3.py`: thêm giá trị profile tường minh `grpc_status_code` bên cạnh `binary_error`; kiểm bằng chứng khai `trace_status_kind` khi chọn gRPC. Không mặc định chọn gRPC hoặc tự suy từ số đo.
- `results/T-054/scripts/worker.py`: ở nhánh prep TORAI RE3, profile binary giữ kiểm0/1 cũ; profile gRPC cho mã nguyên không âm trong miền khai tường minh, giữ nguyên giá trị khi gọi `chuan_bi_B`. Thiếu/sai semantics thì BLOCKED. Ghi rõ bảng trace error của baseline này là tổng mã native, không gọi là số span lỗi.

Đồng bộ đúng phần quyền vào SPEC và nối WHY/DECISIONS: lý do là hợp đồng input theo nguồn tác giả; giữ TT/Nezha, kernel, seed, cửa sổ và mọi kết quả cũ. Output/check/LOG/STATE thuộc T054. Kiểm fixture mã0/1/2/13/16, sai kiểu/âm/thiếu profile; tổng mã phải đúng kernel cũ, không chuyển sang0/1. Không mở telemetry RE3 trong phần A.

## B. Đọc riêng metadata định danh owner để xác định inventory

Hợp đồng hiện chỉ cho metadata/schema; footer không liệt kê giá trị serviceName/container_name. Archive gốc không có inventory/deployment trong mục lục. Không lấy4root hoặc tự coi tất cả tiền tố metric là deployment.

Đề xuất cho phép thêm đúng dữ liệu cấu trúc sau, vẫn trước G3:

- 30 `traces.parquet`: chỉ column chunk `serviceName`.
- 30 `logs.parquet`: chỉ column chunk `container_name`.
- Revision HF giữ đúng revision đã ghim; kiểm lại footer hash cũ để lấy offset và request đúng byte của hai cột. Không tải toàn bộ Parquet. Giới hạn metadata+chunk tổng16MiB; vượt thì dừng báo trước.
- Không đọc metric values, timestamp, duration, operation, IDs, message hay statusCode; không chạy phương pháp hoặc đánh giá. Chỉ xuất **hợp tên owner toàn cohort**, không tần suất, không phân bố hoặc liên kết theo ca/fault.
- Raw page/owner rows không lưu ra disk. Lưu receipt range/hash/phạm vi và tập tên toàn cục vào results/T054. Không biến tên quan sát thành khẳng định deployment; alias không có căn cứ vẫn OPEN.

Mục đích là inventory độc lập nhãn, không tìm triệu chứng hoặc chọn thiết kế theo RE3. Đây là mở rộng rõ ràng ngoài quyền footer/schema cũ; chỉ thực hiện nếu Minh duyệt coi hai trường định danh này là metadata inventory được phép. Không suy quyết định này thành quyền mở các tín hiệu/đánh giá RE3 bản cuối.
