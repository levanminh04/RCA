# Tự rà SPEC T-038 trước triển khai

Codex là người làm; Claude phản biện kết quả. Lượt này không là phản biện chính thức. Nhận xét dưới được lập từ nguồn gốc, code và đầu ra trước khi mở REVIEW/kết luận phản hồi cũ. Bắt đầu phiên ngày 15/10/2026; qua ngày 16/10 theo giờ Việt Nam trong khi làm.

Đã đọc nguyên văn Prompt chung, Soát SPEC và G3 trong `docs/review-prompt.md`. Quyền thực thi lấy từ lời giao mới của Minh, đã chép nguyên văn vào LOG Phiên 2. Trạng thái ĐỀ XUẤT ở SPEC là mốc trước lời giao.

## Phần phù hợp với nguồn

- DT18 §2 đoạn 2–3, hướng dẫn cô §1 và MRP RQ3/RQ5/P5 đòi mô hình quan hệ có nguồn, ánh xạ tín hiệu và khảo sát trên hệ công khai. SPEC giữ inventory nguồn khác nút quan sát; đồ thị dùng để lập khóa, giao và phần riêng. Chưa dùng cạnh để chấm bất thường hoặc xếp hạng. Việc chọn phép tính đó thuộc P6.
- Các lựa chọn về thực thể, thao tác có bằng chứng, nguồn tĩnh khác runtime, alias có nguồn và chia nhánh đã có căn cứ ở WHY-52/53 và phương án P5b gốc LOG T-036 Phiên 1. Không cần tạo lựa chọn phương pháp mới để triển khai đúng SPEC.
- Đã đọc toàn bộ code build/compare/project và hợp đồng T-036 sau kiểm pin. Comparator giữ owner thao tác, tách endpoints/typed, unknown, exclusions/members và mẫu số rỗng. Snapshot code hiện hành khớp bản ghim. Chưa có phản ví dụ Train Ticket để kết luận hợp đồng cần đổi.
- Selector root của manifest T-035 đúng phạm vi hiện hành, không trộn runs. Cửa sổ full, N, A và các ảnh chụp có sẵn đều còn trong nghĩa vụ. Không dựng cửa sổ mới.
- SPEC không lấy nhãn chọn mapping/quan hệ, không coi nguồn tĩnh là ground truth runtime, không buộc độ khớp cao hoặc đồ thị thắng. Nó bao phủ phần mô hình và đối chiếu của P5, chưa trả lời lợi ích RQ3 hay tính giữ được trên FlashTicket của RQ5.

## Những phần phải dừng và trình Minh

| Điểm | Trạng thái và bằng chứng | Ảnh hưởng và xử lý tối thiểu |
|---|---|---|
| Khả thi một phiên | **CHẶN triển khai toàn chuỗi trong một phiên; chưa phân xử.** SPEC mục Chi phí đã yêu cầu kiểm trước. Nguồn ứng dụng chưa được phép đọc; danh sách ứng viên v1.0.0 có 2.827 blob trong 3.921 mục cây; có vendor, template, cấu hình, mã đa ngôn ngữ, symlink và archive. Chỉ phía trace đã có 1.069 graph. Không suy thời gian đọc/phân xử từ số byte hay tốc độ kiểm hash. | Đề xuất tách truy nguồn/coverage khỏi dựng–đối chiếu–phân tích; chỉ Minh quyết sửa phạm vi SPEC và tạo task nối tiếp. Không giảm kiểm, không tự chia mã task. Phần còn lại phải được ước lượng lại từ coverage/bản ghi thực. |
| Quyền nguồn | **CHẶN phần cần ứng dụng mới; chưa là lỗi SPEC.** Registry chỉ có nguồn RCAEval và ghi revision ứng dụng OPEN. Minh chưa duyệt tải repository/code mới. | Trình gói tải cụ thể ở de-xuat-nguon-va-tach.md và danh sách từng blob trong runs/metadata-de-xuat-001/de-xuat-tai.json. Chưa thực hiện tải. |
| Chuỗi revision | **OPEN, KHÔNG CHẶN đối chiếu tham khảo sau khi đủ nguồn.** Paper đã lưu dẫn repository không ghim revision. Metadata code RCAEval, dataset, ứng dụng, image, instrumentation và deployment là các trục khác nhau. | `conditional_reference=true` phải giữ ở mọi kết quả về sau nếu chưa nối được chuỗi. Không quy mismatch cho instrumentation. Chủ nguồn RCAEval cung cấp manifest build/image/deployment; không tự liên hệ tác giả. |
| Kiểu trace | **FACT về đầu vào, KHÔNG CHẶN.** Toàn bộ cạnh trong các graph hiện hành là gọi-chưa-phân-kiểu; xem runs/mien-graph-002/graph-scope.json. | Vẫn chạy cả hai view khi được triển khai. Mẫu số typed phía trace sẽ không thể chứa cạnh có kiểu đã xác minh từ các đầu vào này; không lấp kiểu bằng kiến trúc hoặc bỏ view để làm báo cáo đẹp. Mapping chưa có nên chưa báo tỷ lệ khớp. |

Chưa thấy mâu thuẫn khoa học bắt buộc sửa nghĩa hợp đồng hoặc bỏ nghĩa vụ trong SPEC. Điều kiện khả thi chưa được giải quyết nên không tuyên bố “tự rà đạt, triển khai toàn bộ ngay”. Các phần kiểm đầu vào/truy nguồn có sẵn và lập đề xuất đã làm trong quyền.

## Bằng chứng và giới hạn kiểm

- `runs/kiem-dau-vao-002/input-verification.json`: pin, hash/bytes của 187 artifacts T-036, code hiện hành/snapshot, nguồn RCAEval theo T-002 và 1.069 graph T-035 đều đạt. Lượt 001 lỗi runner tìm sai đường dẫn snapshot, được giữ nguyên.
- `runs/mien-graph-002/graph-scope.json`: selector/allowlist, miền whole_dev_trace_table, interval, hai mức và kiểu cạnh. Lượt 001 lỗi runner thêm trùng tiền tố dev, được giữ nguyên. Không phải đầu vào sai hoặc pin lệch.
- `runs/metadata-de-xuat-001/de-xuat-tai.json`: danh sách tải **đề xuất**, chưa là nguồn ứng dụng đã tải/đọc. Các Git tree object được tính lại từ metadata và khớp; blob nội dung chưa được tải nên chưa xác minh payload hay coverage nội dung.
- Chưa có inventory nguồn, bản ghi quan hệ, mapping, oracle riêng, graph tĩnh hoặc kết quả đối chiếu. Không tạo file rỗng để coi là đã có đầu ra. Không đo pilot/RAM/tổng máy vì chưa có chuỗi triển khai đủ nguồn trong quyền và chưa xác nhận môi trường đo độc lập với các nhánh khác.

Không có kết luận phản biện T-038 trước được cung cấp trên đĩa để đối chiếu. Minh cho biết đã dừng lượt phản biện ba SPEC; lời đó chỉ xác định quyền hiện tại, không thay bằng chứng tự rà. Sau ghi nhận xét độc lập này mới đọc REVIEW và mốc đóng của T-036 theo đầu vào SPEC.
