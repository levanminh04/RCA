# T-037 — tự rà và phản ví dụ chặn triển khai

**Task chưa đạt tiêu chí xong; không có graph toàn phạm vi được dựng.** Không sửa SPEC/hợp đồng chung. Tự rà người làm không thay Claude phản biện chính thức.

Pin/hash trước dùng: runs/tu-ra-001/preflight.json. T-036 187/187 và T-035 5.667/5.667 entries khớp; mã hiện hành khớp snapshot đã giao. Chưa mở REVIEW cũ trước khi ghi nhận xét độc lập trong LOG Phiên2. Sau đó đọc REVIEW và mốc đóng T-036: công cụ đã được nghiệm thu trong phạm vi trước, không là chứng cứ nó phủ SMTP.

## Chặn đã tái lập

B13 L199, B14 L82, B14-03 L9–12 quy định Ticket gửi SMTP ngoài transaction, timeout có thể đã gửi. T-036 hop-dong.md §2 và snapshot code/build.py L10–11, L161–169 chỉ nhận channel gọi http/rpc/internal. Với transport SMTP giữ nguyên, cả hai nhãn gọi tổng hợp đều bị `ValueError('relation_type')`. Kết quả: runs/smtp-002/result.json#/cases; input không bị sửa. Phản ví dụ và oracle literal: counterexample-smtp.json, được ghi trước runner phản ví dụ.

Đây là thiếu biểu diễn của hợp đồng nguồn tĩnh, không phải lỗi dataset, collector hoặc kết luận về thuật toán RCA. Không gán SMTP thành HTTP/RPC/internal, không biến nó thành messaging broker. Các trường context/provenance có thể giữ chữ SMTP nhưng không thay địa chỉ/channel cấu trúc bị thiếu. Cần Minh duyệt xử lý hợp đồng chung trước phần graph phụ thuộc.

## Tự phát hiện và giữ lỗi của lượt này

- oracle.json ban đầu xếp Ticket→SMTP vào http_edges. Nguồn bác bỏ đáp án ấy. Giữ file gốc, vô hiệu cho dựng graph; không sửa kết quả để theo oracle sai. Chưa có converter riêng T-037 tại thời điểm phát hiện.
- runs/smtp-001 giữ input/registry/oracle/code/failure. Lượt này lỗi ở phép đo RAM do ctypes chưa khai argtypes; đã sửa riêng runner T-037 và chạy tên mới smtp-002. Không phải finding khác của T-036.
- Lượt đọc gộp có đường dẫn WHY/DECISIONS nhầm cwd platform đã báo lỗi không có file; đã đọc đúng bản RCA. Các output bị cắt không được dùng thay toàn nguồn.

## Kiểm độc lập còn làm được

Partial records chỉ kiểm JSON/ID/reference/provenance/shared signal và các cạnh DB literal. Kết quả 24/24 tại runs/ket-phien-001/partial-record-checks.json. Đây không là kiểm build/project đầy đủ. Coverage từng requirement tới graph/chiếu chưa thực hiện vì graph dừng tại chặn SMTP.

Không mở test/heldout/telemetry thô, không chạy baseline/P6/T040/EC2. Không tải nguồn. Không commit/push hoặc sửa code chung. Các nhánh hỗ trợ là thu thập nguồn của người làm, không reviewer chính thức hay chat ngoài.

## Chi phí

Dự toán trước triển khai: 5–8 giờ công tổng, 5–15 phút máy, peak RAM <0,5 GiB và tối đa 200 MB kết quả cho 10 lượt, **chưa đo**. Không xác nhận dự toán full task từ phản ví dụ nhỏ. Full pilot, tự kiểm/phân xử/bàn giao đầy đủ vẫn chưa chạy; sau khi giải quyết hợp đồng phải dự toán lại theo phạm vi không đổi.

Phép đo nhỏ smtp-002: hai build calls 0.000550800 giây; peak working set 32768000 byte cho process. Trước chạy đã lấy mẫu CPU1giây không process vượt0,25CPU-second; chỉ có thu thập/ghi nguồn nhẹ. Không dừng process khác. Số này chỉ mô tả phản ví dụ, không ngoại suy whole task. Hash preflight khi hai nhánh đọc nguồn đồng thời không là benchmark.

Kích thước thực của tất cả lượt và snapshot sẽ ghi manifest.json#/total_output_bytes, gồm lượt lỗi, bản oracle bị vô hiệu, metadata, nguồn và script. Không sao lại toàn graph T035/T036 vào từng run; tải/giải nén mới =0. Q40 áp ngân sách baseline, không dùng nó để giảm coverage thiết kế.
