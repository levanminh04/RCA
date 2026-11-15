# Định dạng kết quả RCA 0.3 — T-065

Mở rộng 0.2 ở T-061 và phần phát lại của T-062. Không sửa hai task đó. Phục vụ giao diện DT18; không thêm phép xếp hạng, đổi M1 hoặc chấm kết quả nghiên cứu.

`schema-0.3.json` là lược đồ JSON Schema. `../kiem.mjs::validate` kiểm các keyword có trong lược đồ và từ chối keyword chưa triển khai. `verify()` kiểm lược đồ, tính nhất quán với nguồn và liên kết. Đọc/sinh bằng Node có `JSON.rawJSON` để giữ nguyên số nguyên nanosecond khi ghi lại các trường cũ.

Các trường mới:

| Trường | Nghĩa và nguồn |
|---|---|
| `ban` | Chiều bản, phiên bản phương pháp, cấu hình/hash, đường dẫn/hash đầu vào và đầu ra. P7 dùng cấu hình gốc `T-062/ca/_nguon/m1-p7-config.json`. M1-FT sẽ dùng chỉ mục xuất theo hợp đồng T-064. |
| `thao_tac[]` | Nhóm theo `(owner sau alias, operation)` của span qua cửa sổ. `trang_thai_m1`, cờ và `don_vi_m1` lấy thẳng từ `extra.don_vi_phan_vi`; kênh từ `extra.kenh_co` có tiền tố `op|`. Không tự kết luận thao tác là nguyên nhân. |
| `n_N/n_A` | Số span, gồm span bọc. |
| `mau_N/mau_A` | Số mẫu phương pháp dùng: bỏ span bọc khi E1 bật. Kiểm với `n_N/n_A` của đơn vị M1. |
| `canh_thao_tac[]` | Cùng trace, cha resolve sau cắt cửa sổ; hướng cha → con. Gộp theo cặp thao tác, giữ số lần N/A và tối đa 3 ví dụ trace/span. Cạnh tự nối vẫn giữ nếu nguồn có. |
| `tien_xu_ly` | Các bộ đếm đối chiếu trực tiếp với `diagnostics.span` đã lưu. |
| `quan_he` | Loại đã hỗ trợ, loại chưa hỗ trợ. Thuộc tính đích gọi chỉ dùng mô tả; không tự dựng cạnh DB/cache từ địa chỉ. |
| `lien_ket[].url/pham_vi` | Explore URL mã hóa một lần và phạm vi bằng chứng. Liên kết không có nhãn. |

Tiền xử lý theo code P7 đã kiểm pin: `src/m1/chuoi.py` phần span và `src/m1/span.py`. Đổi us → ns bằng hệ số 1000; giữ `start >= t−300`, `end < t+300`; alias trước dựng quan hệ; khóa span gồm trace ID và span ID; bỏ bản trùng y hệt, từ chối trùng khác nội dung. Chia N/A theo end. Không gọi lại E4/E5/xếp hạng.

Phân loại thao tác lấy từ thuộc tính raw span: `http.*` → HTTP, `db.system*` → SQL/cache, `messaging.system` hoặc PRODUCER/CONSUMER → message, scope scheduling/quartz → job; phần khác ghi `khac`. Đây là phân loại quan sát để hiển thị, không là quyết định nghiên cứu. Không suy loại chỉ từ tên hàm.

Giá trị enum theo [định nghĩa OTLP chính thức](https://github.com/open-telemetry/opentelemetry-proto/blob/main/opentelemetry/proto/trace/v1/trace.proto): CLIENT=3, PRODUCER=4, CONSUMER=5. Tự kiểm đã phát hiện và sửa nhầm CLIENT thành message ở lượt dựng đầu; giữ ghi nhận trong báo cáo. Không dùng lượt đó để kết luận dữ liệu có message.

Liên kết:

- Tempo: service + tên thao tác trong cửa sổ. Không gọi đây là trace M1 đã chọn.
- Loki của kênh M1 `log_loi`: service + JSON severity ERROR/FATAL, theo `ho_so_nguon.quy_tac_log` của đầu vào.
- Loki của thao tác: tối đa 20 trace ID quan sát có log tương quan trong gói ca. Ghi rõ log cùng trace không có nghĩa thao tác đó phát log. Nếu thiếu tương quan, chỉ mở ngữ cảnh service và ghi rõ giới hạn.
- Prometheus của thao tác: chỉ dựng khi raw span có cặp route HTTP/method; không dựng metric SQL/job/message. Cửa sổ truy vấn không quá 10 phút.

File phụ `du-lieu/<ban>/thao-tac/<ca>/<service>.json` chứa bảng thao tác của service và đồ thị gồm các nút trong service, cộng đầu mút qua biên một bước. Service không có span vẫn có file rỗng và thông báo; không suy vì service khỏe hoặc thu nhận lỗi. Điểm e chỉ ở bảng chi tiết/menu; bán kính nút cố định 32.

Mọi bản phát lại nằm riêng trong `phat-lai/`. Trang chính không đọc khối đáp án. G-c hiện mới có chiều bản P7; có chỉ mục T-064 chưa đồng nghĩa đã tích hợp/kiểm ứng viên cuối.
