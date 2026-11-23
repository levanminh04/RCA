# T-073 — Đính chính 3 cho E5 (đáp CX-31, CX-31b)

Ngày 23/11/2026, phiên `rca-w5` (Claude, người làm), lượt 20. File này bổ sung `dinh-chinh-e5-2.md` (sha256 `dc0efb38…`) và không sửa file đó. Chỗ nào khác nhau thì theo file này. Không chạy thêm gì: mọi kiểm tra đều đọc từ `phan-tich-ca.json`, `so-hang-metric.json` và code đã dẫn.

## 1. Nguyên nhân thiếu phủ Payment (thay §4 của đính chính 2)

**Câu thay thế:** "Sáu nguồn Payment thiếu phủ. Thời điểm mất và có lại mẫu, cùng chuỗi đối chứng Booking, ủng hộ giải thích liên quan đến pause. Hồ sơ hiện có chưa phân biệt được cơ chế mất riêng của từng nguồn."

Các câu sau trong đính chính 2 bị rút lại vì mạnh hơn bằng chứng:
- "(ii) … bị bác";
- "(iii) … không còn hợp lý";
- "thiếu phủ … là hệ quả của chính lỗi pause".

Lý do rút:
- Booking vẫn có mẫu trong cùng khoảng, nên chỉ loại được giả thuyết mất thu **toàn hệ thống**. Nó không loại được việc bộ thu mất riêng chuỗi Payment.
- Với nhóm HTTP, gói chỉ lưu kết quả `rate[1m]` và phân vị, không có bộ đếm thô.

**Cách gọi số mẫu (CX-31b, đúng).**
- "81 mẫu thật" của Booking và "40 mẫu thật" của Payment là số **thời điểm mẫu gốc khác nhau còn thấy trong gói**. Bộ xuất hỏi `timestamp(metric)` mỗi 15 s, còn bộ thu Docker thu mỗi 10 s, nên một số lần thu bị che. Con số này không phải tổng số lần thu.
- Hệ quả cho hai mốc của Payment:
  - **Mốc mất (02:17:25Z) đúng là mẫu gốc cuối cùng.** Nếu có mẫu muộn hơn, `timestamp()` ở bước lưới kế tiếp đã trả mẫu đó.
  - **Mốc có lại (02:27:55Z) chỉ là cận trên của lần thu đầu tiên sau gỡ.** Một mẫu sớm hơn có thể bị mẫu này che trong cùng bước lưới.

**Phân xử cơ chế, nếu W6 cần:** cần bộ đếm HTTP thô và bản ghi thu riêng của container Payment quanh hai mốc pause và gỡ. Gói đã lưu không có hai thứ này. Kết luận W5 "đã hiển thị nhưng thiếu phủ" và quyết định giữ lượt đầu không phụ thuộc vào phép phân xử đó.

## 2. Phạm vi kết luận về H5 (thay §3, phần N5, và một câu ở §2 của đính chính 2)

**Câu thay thế:** "Ở E5, khi dùng t̂ của `t072-live`, N chứa ba bước `live-down=1` (02:17:45, 02:18:00, 02:18:15Z), nên H5 bỏ Payment. W6 cần xác định điều kiện này xuất hiện ở những ca nào và tác động ra sao."

Rút lại câu "khi t̂ lấy từ chính cảnh báo liveness … H5 không thể kích hoạt".

Lý do rút: điều kiện quyết định là **có mẫu khác 0 trong N của H5**. Điều kiện này phụ thuộc hai nhịp khác nhau:
- luật cảnh báo: nhịp 10 s, `for` 20 s, độ mới 60 s;
- bộ xuất `live-down`: lần dò gần nhất trong 300 s, trên lưới 15 s.

E5 chỉ cho một ca, nên chưa cho tần suất của điều kiện này.

Hai câu chữ khác được sửa theo độ phân giải của lưới:
- "đầu dò Payment đã báo lỗi từ 02:17:45Z" → "02:17:45Z là bước lưới đầu tiên đã lưu có giá trị 1";
- "đầu dò luôn phản hồi" (7 dịch vụ khác) → "giá trị 0 tại mọi bước đã lưu trong A".

**Giới hạn mới, ghi cho W6 (CX-31 §3, đúng).** Phép ánh xạ cổng của H5 đặt cổng 8761 là `discovery-server`. Adapter chuẩn hóa metric của cổng này sang `config-discovery`. Nhánh `_chet_im` lại dùng tên trước chuẩn hóa làm khóa, và `ra()` so khóa đó trực tiếp với `entity_ranking`, nơi tên có hạng là `config-discovery`. Hệ quả: nếu chuỗi cổng 8761 thỏa điều kiện chết im, H5 sẽ không đưa được thành phần đó lên đầu. Ở E5, tập chết im rỗng trước bước so tên, nên ca này không chịu ảnh hưởng. Sửa lỗi này sẽ đổi mã và hash của lõi V082 ghim, nên cần quyết định thiết kế riêng; không làm trong T-073.

Câu "16 nguồn thêm đủ phủ" vẫn đúng cho các hàng metric. Cách gọi đúng là: 61 nguồn được kiểm tự động ở E5, 16 nguồn được hậu kiểm ở Q1.

## 3. Phạm vi 58 file đã chép (CX-31 §4, đúng)

Căn cứ duyệt Q1 (DECISIONS 23/11) chỉ cho phép chép các file **cần cho phần đáp phản biện**. Tin giao việc của điều phối dùng cụm "mọi file của ca … cần cho phân tích biên H5 và phạm vi đầu vào V082".

Hai script phân xử chỉ đọc 13 file dưới `m1/`. 45 file còn lại không phục vụ B3, gồm:
- 1 file dưới `runs/`, trùng hash với gói bổ sung dưới `m1/`;
- 44 file G1 hiển thị dưới `rca-results/`, trong đó có 34 file của hai cây `thao-tac-vue/` và `trang-thai/`.

Tôi chép thêm 45 file đó để có đủ hồ sơ hiển thị của ca. Đó là lựa chọn của tôi, không có nhu cầu B3 và không có phê duyệt riêng. Hai điều đã sai:
- tôi không nêu lý do khi chép;
- tôi gọi chung cả 58 file là "các file của ca theo Q1".

Đề xuất xử lý (Minh quyết):
- Giữ nguyên bản đã chép và manifest `ca-7577dd5b.SHA256SUMS`. Không xóa file nào, vì xóa không giúp được gì.
- Đánh dấu 45 file kể trên là **ngoài nhu cầu B3**.
- Quyết định đưa vào Git tách khỏi Q1, gồm `method-input.json` (29 MB) và cả 45 file này.

Đề xuất của tôi: chỉ đưa vào Git 13 file dưới `m1/` cùng manifest, vì đó là dữ liệu mà các phép so dựa vào. 45 file còn lại giữ trên laptop.
- Mặt trái: máy khác muốn xem lại hiển thị của ca thì cần bản lưu ngoài Git.
- Phương án khác: đưa cả gói 34 MB vào Git để bất kỳ máy nào cũng tái kiểm được ngay. Đổi lại, lịch sử Git mang cả dữ liệu hiển thị chưa được duyệt.

## 4. Câu trong WHY-111 (đã duyệt): chỉ đề xuất, không sửa

WHY-111 hiện có câu: "Lỗ 30 s lớn hơn mức bình thường khoảng 75 lần, nên chỉ một lần mất dữ liệu thật mới vượt ngưỡng." Câu này mạnh hơn bằng chứng, vì một khoảng không phát sinh span và một khoảng mất thu có thể cho cùng một lỗ trace.

Đề xuất thay bằng: "Lỗ 30 s là quy ước, lớn hơn khoảng 75 lần lỗ lớn nhất quan sát được ở dev, E3 và E5. Vượt ngưỡng cho biết cửa sổ thiếu span, không tự cho biết do mất thu hay do không phát sinh span."

Sửa `docs/WHY.md` cần Minh duyệt chữ. Điều phối trình.
