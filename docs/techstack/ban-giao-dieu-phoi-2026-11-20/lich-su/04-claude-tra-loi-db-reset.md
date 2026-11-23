# Claude: trả lời về ngày sự kiện, số bản ghi, truy vấn chậm, mốc DB, reset có phải sửa kết quả

> Nguyên văn, trích bằng script từ `debcb98c-9a36-447f-b07c-8820bd290ab4.jsonl` (dòng 994). Không biên tập.

Lượt này chỉ đọc, không sửa file nào. Có một chỗ tôi tự đính chính: việc dời ngày ở Ticket/Payment **không gấp** như tôi nói trước đó (mục 1).

**1. Ngày sự kiện ở `ticket_db`/`payment_db` là gì?**

Khi sự kiện được publish (12/11), Event gửi bản sao lịch của nó sang các service khác. Ba bản sao hiện như sau:

| Nơi | Giá trị | Dùng vào việc gì (đọc code bản ghim) |
|---|---|---|
| `ticket_db.tbl_event_access_snapshots` | `event_starts_at` 19/11 22:16Z, `event_ends_at` 20/11 22:16Z | Lưu cho check-in và hiển thị vé; tải không đi qua check-in |
| `payment_db.tbl_event_finance_snapshots` | `event_ends_at` 20/11 22:16Z | Chỉ dùng để xét "đủ điều kiện quyết toán" trong màn hình tài chính (`FinanceServiceImpl` dòng 195). `PaymentWorker` không có job quyết toán tự động |
| Booking (đã dời ở T-069) | bán tới 02/12, diễn 03–04/12 | Kiểm còn bán hay không |

Vậy sau 20/11 22:16Z, luồng mua vé không bị ảnh hưởng; chỉ là ba service hiểu lệch nhau về ngày diễn. Câu "có thể sinh payout hoặc chặn check-in, phải làm trước 22:16Z" lúc trước là **nói quá**: không có quyết toán tự động. Việc này chỉ để dữ liệu nhất quán, không gấp, Minh có thể bỏ.

**2. DB hiện có bao nhiêu bản ghi?** (đếm lúc 02:31Z hôm nay)

| | Số dòng |
|---|---|
| `tbl_orders` | 40.069 (hoàn tất 26.166, hủy 6.586, hết hạn 7.317) — 67 MB |
| `tbl_issuances` / `tbl_ticket_deliveries` / `tbl_tickets` | 26.166 mỗi bảng |
| Toàn DB | `booking_db` 189 MB, `ticket_db` 116 MB |

Lúc thu ca cũ đợt 2 (13/11), bảng đơn khoảng 3.700 dòng; lúc thu bù 3 (14/11) khoảng 15.100.

**3. Đã có bằng chứng truy vấn chậm chưa?** Có, ở ba mức:
- **Cũ so với mới, cùng câu lệnh** (span thô ở `phan-tich/span-*.txt`):

| Truy vấn | Cũ p50 | Mới p50 |
|---|---|---|
| Worker hết hạn đơn của Booking | 3,9 ms | 34,8 ms |
| Join đơn–giữ chỗ | 6,3 ms | 42,6 ms |
| Giao vé của Ticket | 2,7 ms | 19,2 ms |

  Nguyên nhân thấy trực tiếp: `EXPLAIN` cho thấy quét tuần tự, `pg_stat` ghi khoảng 93 tỉ dòng đã đọc, và CPU PostgreSQL ở nền tăng 4–5 lần.
- **Chậm dần trong chính một lượt** (vừa đo, `phan-tich/troi-trong-luot.txt`, cửa sổ nền của ca đầu, giữa và cuối lượt chính hôm qua):

| Truy vấn (p50) | 09:40Z | 15:26Z | 18:03Z |
|---|---|---|---|
| Worker hết hạn đơn | 18,5 ms | 26,5 ms | 31,0 ms |
| Join đơn–giữ chỗ | 23,1 ms | 35,0 ms | 42,8 ms |
| Giao vé của Ticket | 18,3 ms | 26,9 ms | 31,2 ms |

  Sau khoảng 8,5 giờ tải, các truy vấn này chậm khoảng 1,7 lần. Đây là bằng chứng cho câu "đầu lượt và cuối lượt không cùng điều kiện".
- **Hệ quả phụ cho chính T-069:** ô chạy cuối lượt gặp DB lớn hơn ô chạy đầu, nên thứ tự chạy các ô cũng là một biến lẫn vào kết quả. Tôi chưa ghi điều này vào `phan-tich-nguyen-nhan.md`; sẽ bổ sung nếu Minh đồng ý.

**4. Lấy mốc nào làm tham chiếu?** Tôi chưa chốt. Có ba lựa chọn:
- **(a) Dump DB ở trạng thái hiện tại (~40k đơn).** Tôi đề xuất cái này: đây là trạng thái W3 vừa đo, và chọn nó không dựa trên việc nó có lợi cho phương pháp nào.
- (b) Bản sao lưu của T-067 ngày 18/11 (`/srv/rca-lab/backups/t067-20261118`). Kích thước chưa kiểm.
- (c) Thu nhỏ về cỡ lúc thu ca cũ (~4k đơn). Tôi không đề xuất: phải xóa dữ liệu nghiệp vụ, và dễ bị hiểu là sửa cho giống điều kiện cũ.

**5. Khôi phục DB như vậy có phải là sửa để làm đẹp kết quả không?**

Không, nếu thỏa đủ bốn điều kiện; vi phạm bất kỳ điều nào thì đúng là sửa để làm kết quả:
1. Khai trước khi thu, ghi trong SPEC.
2. Áp như nhau cho mọi ô và mọi phương pháp (V082, P7, baseline).
3. Mốc được chọn không dựa trên việc nó làm điểm của ai đẹp hơn.
4. Báo cáo công khai cả hiện tượng trôi, không giấu.

Khi đó nó giống việc ghim image hay ghim cấu hình: cố định một điều kiện thí nghiệm.

Không khôi phục cũng là lựa chọn hợp lệ, vì hệ thống thật cũng tích dữ liệu. Vì vậy đề xuất của tôi khác nhau theo mục đích:
- **W4 (cảnh báo):** không khôi phục giữa lượt, đo độ trôi. Luật cảnh báo cần chịu được hệ thống "già" dần.
- **W7 (đánh giá):** khôi phục về mốc trước đợt và trộn thứ tự ô. Nếu không, ô chạy sau luôn gặp DB lớn hơn ô chạy trước, và thứ tự trở thành biến lẫn.

T-069 không khôi phục gì. Kết quả đã báo nguyên trạng.

**6. W4, W5, W6, W8 có chạy song song hoàn toàn được không?**

**Phần viết code và thiết kế thì song song được; phần chạy trên máy và phần tích hợp thì không.**

| Song song được ngay | Phải nối tiếp hoặc chờ |
|---|---|
| W4 viết luật và quy tắc gom cảnh báo | Ngưỡng W4 cần dữ liệu nền đã thu |
| W5 viết bộ xuất, hợp đồng G1, bộ điều phối | Kiểm W5 từ đầu tới cuối cần luật W4 đang chạy, dịch vụ W5, và một khung exp-app cùng máy tải lúc không có lượt nền |
| W6 thiết kế đánh giá | Một số mục cần Minh chốt trước (mốc DB, danh sách baseline) |
| W8 viết LLM trên đầu ra G1 đã có | Cần Minh chọn mức P8; tích hợp với W5 làm sau |
| — | W9a cần W4, W5 (và W8) xong |

Hai giới hạn khác:
- **Tài nguyên dùng chung:** exp-app và máy tải chỉ chạy một lượt tại một thời điểm. Truy vấn nặng vào Prometheus có thể làm nó khởi động lại và mất dữ liệu nền.
- **Người duyệt:** mỗi gói cần một SPEC Minh duyệt và một lượt Codex phản biện. Mở 4–5 gói cùng lúc thì nút thắt là thời gian duyệt của Minh. Tôi đề xuất mở theo thứ tự đường găng: hạ tầng + nền trước, rồi W4 và W5, sau đó W6 và W8.

Phiên tách nhánh [T-069 task review and implementation (fork)](#local_40716c6f-27ed-4022-9b8f-de5646248553) đã kiểm 7 điểm phản biện của Codex (6 điểm đúng, R2 đúng một phần) và đang chờ Minh trả lời.
