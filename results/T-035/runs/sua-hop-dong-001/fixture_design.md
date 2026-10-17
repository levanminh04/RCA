# Oracle độc lập trước sửa bốn lỗi hợp đồng — T-035

Nguồn: hợp đồng T-035 hiện hành, bốn phản ví dụ do Minh chuyển, và phạm vi sửa Q-155. Đây là bộ kiểm đầu vào tổng hợp cho người làm, không là lượt phản biện chính thức. Không có dữ liệu dev, test hoặc nhãn trong oracle.

`oracle.py` khai literal đầu vào và đáp án trước khi mã bộ dựng được sửa. Đáp án không lấy từ bộ dựng cũ hoặc mới. Chỉ nhập các API công khai Prepared, build, project qua module được chọn. Không gọi helper nội bộ làm oracle. ID thao tác được viết theo cú pháp JSON của cặp đã công bố. Cạnh và đích đối chứng khai trực tiếp, không suy từ đầu ra bộ dựng.

## Phạm vi

- Tên thao tác: None, NaN, pd.NA; object, float, nullable string; một và nhiều dòng, có tên và thiếu tên lẫn nhau. Các giá trị thiếu dùng một khóa null. Khóa span trùng với biểu diễn thiếu khác nhau được khử lặp đúng, vocabulary/count giữ đúng.
- Định danh: DB, cache, peer, broker phía PRODUCER/CONSUMER, host; đụng ID thao tác của chính phía gọi hoặc phía khác. Phủ service ID, alias sau chuẩn hóa, thao tác được giữ chỗ trên toàn Prepared kể cả ngoài cửa sổ. Collision từ chối ValueError(identifier_collision). Tên thực thể trông như JSON nhưng không đụng ID hiện hữu vẫn hợp lệ. Inventory không quan sát không là nút đồ thị, nên riêng một tên trong inventory không tạo collision. project nhận cả đồ thị literal hợp lệ và đồ thị literal mâu thuẫn, kiểm đích trực tiếp.
- Thời gian: microsecond và nanosecond âm, thiếu, không nguyên, không hữu hạn, chuỗi không phải số; int64 và uint64/object/string vượt miền; cộng và nhân bị tràn. Tất cả lỗi này trả ValueError(invalid_time). Đối chứng 0, max_int64 ở ns, max_us=floor(max_int64/1000), tổng us sát biên, số nguyên dạng string/object/uint64. Khi có đủ cặp ns, ns được ưu tiên: vẫn yêu cầu từng cột us hợp lệ trong int64, nhưng không tính phép chuyển us không được dùng. Không đồng nhất ns với us đã làm tròn.
- Kiểu thực thể: known+known khác nhau bị từ chối ValueError(conflicting_entity_type); hai thứ tự dòng, inventory với span/endpoint, span với endpoint, endpoint với endpoint. unknown không hạ known; unknown được nâng thành known; các known giống nhau hợp lệ. Đối chứng giữ cạnh/count/witness và component_context đúng.

## Cách đối chiếu và giới hạn

Mỗi ca build được gọi qua Prepared.graph và build; project chạy trên graph sinh ra. Ca project literal gọi project độc lập. Ca hợp lệ so nút, cạnh, belongs_to, component_context, đích phép chiếu bằng đáp án literal. Những ca tên thiếu kiểm thêm số đếm và vocabulary; ca thời gian kiểm mảng ns thực tế. JSON strict không cho NaN hoặc pd.NA lọt ra. Mỗi ca lỗi yêu cầu đúng lớp ValueError và mã lỗi; một lỗi tình cờ khác không được tính đạt.

Chạy bằng Python -X utf8 -B. Mỗi output là một thư mục mới dưới chính thư mục run; giữ cả lượt thất bại. `--builder-path` cho phép kiểm bản cũ được sao lưu. Kết quả ghi actual/expected/pass, hash oracle và builder. `--list` chỉ liệt kê ca, không nhập builder hoặc ghi kết quả.

Các ca này kiểm hành vi hợp đồng và những ranh giới cụ thể, không chứng minh dữ liệu dev từng chứa lỗi, không chứng minh instrumentation FlashTicket thực tế, và không đánh giá lợi ích RCA.
