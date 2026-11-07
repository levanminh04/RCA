# Hệ quả nếu mất dữ liệu trên hai EC2

Ngày 06/11/2026. Báo cáo theo yêu cầu của Minh, trong T-054.

**Tài khoản AWS bị tạm khóa là thông tin Minh xác nhận. Dữ liệu đã bị xóa vẫn chưa được xác nhận.** Đã tạm dừng riêng SSH, chuyển dữ liệu, triển khai và kiểm máy cloud. Không tự bật/tắt hoặc cấp máy; không tự chuyển main sang laptop.

## 1. Những phần đã có bản local

Đã kiểm SHA256 và kích thước theo các manifest tương ứng:

| Gói | Số mục khớp | Phạm vi |
|---|---:|---|
| T-048 | 2.168/2.168 | outputs và closed_outputs local |
| T-049 | 1.020/1.020 | đầu ra trong manifest |
| T-053 | 2.654/2.654 | đầu ra trong manifest |
| T-032 | 6.224/6.224 | gói bổ sung trong manifest-final |
| T-033 | 29/29 | gói báo cáo session9-report-002 |
| T-011 | 142/142 | tạo tác khảo sát, không phải toàn raw dataset |

Chi tiết từng nhóm nằm trong `aws-loss-local-audit.json#/groups`. Đây là kiểm các gói cụ thể; không chứng minh mọi file từng nằm trên EC2 đều đã được sao lưu. T-010 có 93/94 mục khớp manifest cũ, riêng `the-dataset.md` khác hash. Không dùng thẻ đó để kết luận mất raw hoặc xác nhận toàn gói, không mở lại hay sửa task đã đóng.

Nguồn P7 còn trên laptop, đã đối chiếu số file/kích thước hiện tại với metadata nguồn được kiểm hash:

| Nguồn | File có mặt, đúng kích thước | Tổng byte |
|---|---:|---:|
| TT60 | 180/180 | 1.309.388.082 |
| Nezha-OB | 226/226 | 1.598.103.311 |
| TORAI A | 180/180 CSV | 9.244.910 |

Xem `aws-loss-main-source-presence.json`. Không mở giá trị test và không băm lại toàn raw trong lượt này; biên nhận xác minh nguồn 006 được giữ. Mất bản staging trên EC2 không đồng nghĩa mất nguồn P7. Main chưa chạy nên chưa có kết quả main P7 bị mất. Code, đặc tả và đầu ra checkpoint008 đang ở local.

## 2. Rủi ro cụ thể: bản đầy đủ T4/T4b của T-048

`results/T-048/manifest.json#/remote_frozen_artifacts` kê 925 file trên EC2_2. Có 587 bản local đúng hash. Còn 338 mục không có tại các đường local tương ứng trong manifest, tổng 1.814.750.134 byte:

- 48 file `ban-ghi.jsonl`: 152.768.449 byte.
- 48 file `trung-gian.jsonl`: 1.655.201.305 byte.
- Phần còn lại: command, kiểm, progress, stdout và stderr.

Chúng thuộc 24 lượt `t4-ec2-001-*`, 24 lượt `t4b-ec2-001-*` và hai log cha. Không tìm thấy counterpart `.gz` hoặc archive trong manifest T-048. Đây chưa phải chứng minh không có bất kỳ backup nào ở vị trí khác. Chi tiết: `aws-loss-consequences.json#/T048_remote_catalog_missing_local`.

**Nếu EC2 mất và không có backup khác, phần bản ghi/trung gian gốc này sẽ mất.** Các bảng tổng hợp, luật chọn và phân tích đã nhận về local vẫn còn, không tự biến thành sai. Hệ quả là giảm khả năng kiểm lại chi tiết hoặc làm phân tích mới cần full intermediate. Manifest/hash không khôi phục được nội dung.

Nếu sau này cần tái chạy, đó là lượt mới với provenance và môi trường mới; không được gọi là khôi phục byte của lượt cũ. Chỉ trình chạy phần thật sự thiếu và cần cho câu hỏi hiện tại, không tự chạy lại toàn bộ hoặc mở lại task đã đóng.

## 3. Dữ liệu thô và môi trường khác

Theo inventory005 và `data/README.md`, raw DeepTraLog/LEMMA được giữ dưới `rca-t003` trên EC2_2. Các cây local đã rà chưa xác nhận bản raw tương ứng; hồ sơ khảo sát, nguồn tải và biên nhận còn local. Nếu mất raw, có thể cần tải lại đúng revision/hash khi nguồn còn truy cập được. Chưa tải lại, chưa có ETA khôi phục. Đây không phải nguồn TT/Nezha của main hiện tại.

Mất môi trường Linux/T025/py38, package và cache sẽ tốn công dựng lại từ pin/recipe, rồi kiểm nguồn, môi trường và parity đúng phần khác. Không tự coi máy mới tương đương máy cũ. Cũng không lấy việc đổi máy làm lý do chạy lại các kết quả đã hợp lệ. Số đo runtime và identity máy cũ giữ ý nghĩa lịch sử.

Các scratch, full raw và lượt hỏng khác chỉ ở remote chưa có đối chiếu toàn bộ vẫn OPEN. Không dùng sự có mặt của một báo cáo local để khẳng định toàn bộ remote đã backup.

## 4. Ảnh hưởng đến công việc tiếp theo

Tạm dừng triển khai 35/25 trên hai EC2 theo Minh. Tiếp phần local được phép: kiểm code, chuẩn bị metadata/hợp đồng RE3 và hồ sơ. Bản vá OB đã có 44 kiểm tổng hợp cho source/default, 92 kiểm tích hợp và một ca OB dev qua worker thật cho bản ghi/digest đầu vào exact. Plan ứng viên008 vẫn `WAIT_G3`.

Chưa hoàn tất bước3 cloud hoặc đủ G3. Còn thiếu máy chạy thực đã xác minh, staging/nguồn/binding và phần đơn vị/inventory/support/adapter RE3. Khi Minh giải quyết tài khoản hoặc quyết hạ tầng khác, chỉ làm lại phần chuẩn bị chịu ảnh hưởng và phần bằng chứng thực sự thiếu. Nếu truy cập EC2 trở lại, ưu tiên bảo toàn phần full T-048 đang có rủi ro trước khi dọn hoặc thay máy; chưa tự thực hiện thao tác này.
