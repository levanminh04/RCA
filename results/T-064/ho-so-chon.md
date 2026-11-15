# T-064 — Hồ sơ chọn ứng viên M1-FlashTicket (bản nháp 1, 13/11/2026 ~22:26Z)

Người làm: Claude. Chưa qua phản biện của Codex. Chưa đủ để đóng task: xem mục 7.

Tiêu chí áp dụng: `results/T-064/tieu-chi-chon.md` (hash khớp LOG, kiểm 22:22Z). Không đổi tiêu chí sau khi xem kết quả.

## 1. Dữ liệu và số bản đã chấm

- Tập chọn: dev bản 2 của T-063, mỗi ô một lần thu.
  - Tập A, 12 ca, điều kiện xác nhận khai trước: 7 ca lỗi, 5 ca không lỗi (`tap-chon-dev2-12.json`).
  - Tập B, 13 ca: tập A cộng PAUSE-PAYMENT, theo "Sửa sau 1" **chờ Minh** (`tap-chon-dev2-13.json`).
- Tập không hồi quy: 9 ca T-062 (5 ca lỗi, 4 ca không lỗi), báo riêng.
- **Tổng số bản đã chấm trên tập chọn: 37** (lượt 1: 27; lượt 2: 10, trong đó 3 bản đối chứng mã nguồn). Lượt 2 được thiết kế sau khi đã xem kết quả lượt 1 trên cùng tập chọn.
- Mọi lần chạy tất định: lượt 1 351/351, lượt 2 220/220 (`kiem/kiem-luot2.json`: thiếu 0, không OK 0, không trùng SHA 0). Ba bản đối chứng V035–V037 trùng V015/V018/V019 của lượt 1 trên cả 22 ca, nên hai lượt so được với nhau.

Nguồn số: `cham/chon-dev2-luot1-tap{12,13}.json`, `cham/chon-dev2-luot2-tap{12,13}.json`, các file `-giu-bo.json` cùng tên, `cham/khong-hoi-quy-{1,2}.json`. Sổ: `so-bien-the.jsonl` (104 dòng).

## 2. Mốc P7

| Tập | AC@1 | AC@3 | Tổng hạng | K | Bảng cạnh |
|---|---|---|---|---|---|
| A (7 ca lỗi, 5 không lỗi) | 5 | 7 | 9 | 4/5 | UNSUPPORTED |
| B (8 ca lỗi) | 5 | 7 | 15 | 4/5 | UNSUPPORTED |
| T-062 (5 ca lỗi, 4 không lỗi) | 5 | 5 | 5 | 4/4 | UNSUPPORTED |

Ca trượt hạng 1 của P7: EVENT-DB-LAT (hạng 2), HTTP5-EVENT-FLASH (hạng 2), PAUSE-PAYMENT (đáp án vắng).

## 3. Giữ hay bỏ từng hướng

Phép 1 là thêm riêng vào P7; phép 2 là bỏ khỏi tổ hợp. "Không tác dụng" nghĩa là mọi đại lượng bằng nhau trên tập đó.

| Hướng | Bản | Tập A | Tập B | Vì sao |
|---|---|---|---|---|
| H8 sàn 1 ms | V002 | GIỮ (luật 2): K 4 → 3 | như A | Bỏ cờ nền có độ vượt dưới 1 ms. Đổi lại: EVENT-DB-LAT 2 → 1, CPU-BOOK-2 1 → 2 (cơ chế Q6) |
| H1c cạnh trong danh sách chung | V014 | GIỮ (luật 3): cạnh đúng top 3 ở 3/3 ô | như A | Thứ tự nút không đổi; tổng hạng +0,5 do phép chiếu cạnh về nút |
| H1a, H1b | V009, V010 | BỎ: AC@1 giảm | BỎ | Cạnh yếu đứng hạng 1 danh sách cạnh riêng (WHY-82) |
| H2 JVM/cgroup | V012 | BỎ: K 4 → 5 | đánh đổi (PAUSE-PAYMENT ∞ → 4, K +1) | Kênh tài nguyên gắn cờ ở ca không lỗi |
| H3 pool | V013 | không tác dụng | không tác dụng | **Không có ô lỗi pool trong tập chọn** — hiệu quả chưa phân xử |
| H4 queue | V017 | không tác dụng | không tác dụng | **Không có ô lỗi queue trong tập chọn** — hiệu quả chưa phân xử |
| H5 liveness (độ lớn) | V018 | không tác dụng | GIỮ (luật 1): PAUSE-PAYMENT ∞ → 4 | Tập A không có thành phần chết im |
| H5b liveness (chết im ≥ 60 s là bằng chứng tuyệt đối) | V032 | không tác dụng | GIỮ (luật 1): PAUSE-PAYMENT ∞ → 1; hơn H5 | Thiết kế sau khi xem đúng ca này; chỉ 1 ô |
| H6a luồng bảo trì | V003 | không tác dụng | không tác dụng | Cờ nền còn lại không nằm trên luồng bảo trì thư viện |
| H7 tải, H7c log theo lưu lượng | V005, V016 | không tác dụng | không tác dụng | Bỏ H7c khỏi tổ hợp cũng không đổi gì (V035 = V028). Trên T-062, H7c đưa K 1 → 0 (ca FLASH) |
| Bản gộp 8 thành phần | V019 | BỎ: K 5/5, cạnh 0/3 | BỎ | Kênh tài nguyên vào bước định vị cạnh (Q2). Bỏ pool + JVM khỏi định vị (V031) trả cạnh về 3/3 nhưng K vẫn 5/5 |

Tổ hợp so với P7 (lượt 2, `chon-dev2-luot2-tap{12,13}-giu-bo.json`):

| Bản | Thành phần | Tập A: tổng hạng, K, cạnh | Tập B: AC@1, tổng hạng, K | K trên T-062 | Luật |
|---|---|---|---|---|---|
| V028 | H1c + H8s1 | 10; 3/5; 3/3 | 5; 16; 3/5 | 1/4 | GIỮ (2, 3) |
| V015 = V035 | H1c + H7c + H8s1 | 10; 3/5; 3/3 | 5; 16; 3/5 | 0/4 | GIỮ (2, 3) |
| V029 | H1c + H5 + H7c + H8s1 | 10; 3/5; 3/3 | 5; 14,5; 3/5 | 0/4 | GIỮ (A: 2, 3; B: 1, 2, 3) |
| V034 | H1c + H5b + H8s1 | 10; 3/5; 3/3 | 6; 11; 3/5 | 1/4 | GIỮ (A: 2, 3; B: 1, 2, 3) |
| V033 | H1c + H5b + H7c + H8s1 | 10; 3/5; 3/3 | 6; 11; 3/5 | 0/4 | GIỮ (A: 2, 3; B: 1, 2, 3) |

AC@1 = 5 và AC@3 = 7 ở mọi bản trên tập A. Không bản nào trong bảng có ca tụt quá 2 bậc. Mọi bản trong bảng không hồi quy trên T-062 (AC@1 = 5, K ≤ 4).

## 4. Áp thứ tự chọn §5

Thứ tự §5: (1) xếp hạng nút; (2) K; (3) bảng cạnh; (4) ít thành phần; (5) nhanh hơn.

**Tập A (điều kiện khai trước):**

| Thứ tự | Bản | AC@1 | AC@3 | Tổng hạng | K | Cạnh top 3 | Số thành phần |
|---|---|---|---|---|---|---|---|
| 1 | **V002-H8s1** | 5 | 7 | 9 | 3 | không có đầu ra cạnh | 1 |
| 2–5 | V004, V006, V008, V007 (H8s1 kèm thành phần không tác dụng) | 5 | 7 | 9 | 3 | không | 2–3 |
| … | V014-H1c | 5 | 7 | 9,5 | 4 | 3/3 | 1 |
| … | V028-H1c+H8s1 | 5 | 7 | 10 | 3 | 3/3 | 2 |

**Tập B (nếu Minh chấp nhận "Sửa sau 1"):**

| Thứ tự | Bản | AC@1 | AC@3 | Tổng hạng | K | Cạnh top 3 | Số thành phần |
|---|---|---|---|---|---|---|---|
| 1 | **V032-H5b** | 6 | 8 | 10 | 4 | không | 1 |
| 2 | V034-H1c+H5b+H8s1 | 6 | 8 | 11 | 3 | 3/3 | 3 |
| 3 | V033 (V034 + H7c) | 6 | 8 | 11 | 3 | 3/3 | 4 |

**Áp đúng chữ §5:** bản đứng đầu là **V002-H8s1** trên tập A và **V032-H5b** trên tập B. Cả hai là bản một thành phần.

**Điểm phải nêu để Minh quyết, không tự đổi tiêu chí:**

1. Bản gom đủ các thành phần đạt luật giữ (V028 trên A, V034 trên B) xếp **sau** bản một thành phần chỉ vì tổng hạng lớn hơn 1,0. Đã kiểm: thứ tự nút của V002 và V028 **trùng nhau** ở cả ba ca liên quan (60166807, 98ea5ba4, 4af494a5). Phần chênh đến từ phép chiếu cạnh về nút của tiêu chí §2: cạnh hạng 2 (`event-service → event_db` ở CPU-BOOK-2, `keycloak → keycloak_db` ở HTTP5-EVENT-FLASH) cho đầu nút DB cùng hạng 2 với đáp án, hạng kỳ vọng 2 → 2,5. Đây là hệ quả của cách chấm đã khai, không phải thứ tự nút xấu đi.
2. Trên tập B, bản đứng đầu theo §5 (V032) giữ K = 4/5 như P7, vì §5 đặt xếp hạng nút trước K. Đính chính sau phản biện lượt 1 (R4): `docs/DECISIONS.md` mục "Bổ sung quyền điều phối chiến dịch nhiều ngày" đã giao Claude áp dụng tiêu chí đã trình, nên thứ tự §5 hiện hành **không** chờ xác nhận. Người làm áp đúng thứ tự đó. Muốn ưu tiên K hoặc đầu ra cạnh là đổi tiêu chí sau khi xem kết quả, phải trình Minh.

**Đề xuất của người làm:**

- **Bản đề xuất theo đúng §5:** V002-H8s1 (tập A).
- **Bản thay thế 1 (có đầu ra cạnh):** V028-H1c+H8s1. Cùng AC@1, AC@3, K với V002; thêm đúng cạnh ở hạng 2 tại 3/3 ô cạnh; mất 1,0 tổng hạng vì phép chiếu. Lý do giữ bản này là có đầu ra cạnh cho giao diện T-065. Nó **không** phải điều kiện để phương pháp "dùng đồ thị": V002 vẫn giữ nguyên các phép tính quan hệ của P7 (xem mục 8). Đầu ra cạnh hiện còn lỗi phân loại ở mục 9.
- **Bản thay thế 2 (nếu dùng tập B):** V034-H1c+H5b+H8s1. Thêm PAUSE-PAYMENT hạng 1. H5b thiết kế sau khi xem ca này, chỉ 1 ô.
- H7c không vào bản nào theo luật giữ (không tác dụng trên tập chọn). Ghi nhận: nó là thành phần duy nhất đưa ca FLASH của T-062 về `NO_INTRINSIC_ANOMALY`, nhưng T-062 là tập không hồi quy, không dùng để chọn.

Cấu hình: `bien-the/V002-H8s1/cau-hinh.json`, `bien-the/V028-H1c+H8s1/cau-hinh.json`, `bien-the/V034-H1c+H5b+H8s1/cau-hinh.json`. Mã nguồn lượt 2 `6ab3a59d…` (sổ).

## 5. Bảng từng ca (tập B; tập A là 12 dòng đầu trừ PAUSE-PAYMENT)

Ca lỗi: hạng kỳ vọng của đáp án (nút); `c=` là hạng đúng cạnh. Ca không lỗi: kết luận.

| Ca | Ô | P7 | V002 | V028 | V034 |
|---|---|---|---|---|---|
| 4af494a5 | EVENT-DB-LAT | 2 | 1 | 1, c=2 | 1, c=2 |
| 19b17e22 | CPU-BOOK-1 | 1 | 1 | 1 | 1 |
| e9c9679b | HTTP5-EVENT | 1 | 1 | 1 | 1 |
| 6949870c | REDIS-BOOK | 1 | 1 | 1, c=2 | 1, c=2 |
| 5fb8208f | NET-GW-BOOK | 1 | 1 | 1, c=2 | 1, c=2 |
| 60166807 | CPU-BOOK-2 | 1 | 2 | 2,5 | 2,5 |
| 98ea5ba4 | HTTP5-EVENT-FLASH | 2 | 2 | 2,5 | 2,5 |
| 46aab4be | PAUSE-PAYMENT | vắng | vắng | vắng | 1 |
| eb48d6b3 | BINH-THUONG | CAUSE_FOUND | CAUSE_FOUND | CAUSE_FOUND | CAUSE_FOUND |
| 729604d2 | BINH-THUONG | CAUSE_FOUND | NO_INTRINSIC_ANOMALY | NO_INTRINSIC_ANOMALY | NO_INTRINSIC_ANOMALY |
| 83073ed1 | BINH-THUONG | NO_INTRINSIC_ANOMALY | NO_INTRINSIC_ANOMALY | NO_INTRINSIC_ANOMALY | NO_INTRINSIC_ANOMALY |
| f20b0ca5 | BINH-THUONG | CAUSE_FOUND | CAUSE_FOUND | CAUSE_FOUND | CAUSE_FOUND |
| fb1cf0e9 | FLASH-HEALTHY | CAUSE_FOUND | CAUSE_FOUND | CAUSE_FOUND | CAUSE_FOUND |

Cột V002 lấy từ `chon-dev2-luot1-tap13.json`; các cột khác từ `chon-dev2-luot2-tap13.json`.

## 6. Ca sai còn lại và cơ chế

Chi tiết và bằng chứng: `phan-tich/ghi-chu-co-che-dev2.md`.

| Ca | Trạng thái | Cơ chế hoặc phần chưa biết |
|---|---|---|
| CPU-BOOK-2 | cơ chế đã lần (Q6) | Sàn 1 ms bỏ hai thao tác vài chục µs là bằng chứng mạnh nhất của Booking; khóa `max s` đảo thứ tự với chênh 3%. Chưa có sửa nào tách được ca này với EVENT-DB-LAT bằng nguyên lý độc lập đáp án |
| HTTP5-EVENT-FLASH | một phần (Q5) | Một thao tác Keycloak có nhịp riêng (s = 962) thắng gốc thật (s = 124,8). Chưa biết nhịp nào gây ra và vì sao cổng cho p khác nhau giữa các ca |
| eb48d6b3, f20b0ca5 (BINH-THUONG) | chưa xác định (Q4) | Autovacuum và checkpoint không phân biệt ca bị cờ với ca không bị cờ. Khóa hàng chưa phân xử. Giải thích còn lại là dao động ngẫu nhiên, cần chạy lặp hoặc dời mốc |
| FLASH-HEALTHY | câu hỏi định nghĩa (Q4) | Độ trễ thật tăng dưới tải ×3. Có nên trả `NO_INTRINSIC_ANOMALY` hay không là việc **chờ Minh** |
| PAUSE-PAYMENT (bản không có H5) | cơ chế đã lần (Q3) | P7 loại thành phần mất mọi kênh |

## 7. Chưa xong so với tiêu chí kết thúc (hồ sơ chiến dịch mục 5)

- **(a) mỗi hướng một bản đã chấm:** H1, H2, H5, H6, H7, H8-sàn đã chấm có ô phân xử. **H3, H4 đã cài và chạy nhưng tập chọn không có ô lỗi pool/queue**, nên chưa phân xử hiệu quả; ô POOL-EVENT cần sửa hook thử `RcaFaults.java` (chờ Minh). **H8-adapter (container tạo lại) và H8-log nghiệp vụ chưa cài.**
- **(b) tổ hợp:** đã xét (mục 3).
- **(c) cơ chế ca sai:** có, với phần "chưa xác định" ghi ở mục 6.
- **(d) hồ sơ:** file này là bản nháp. Còn thiếu: phép dời mốc ±30 s (§7 tiêu chí; `chay_ca.py` chưa có tham số dời `t`), `chu-thich-thao-tac-nen.md`, `cau-hinh-de-xuat.json`, `ban-xuat/chi-muc-ban.json` cho T-065, `manifest.json`.

## 8. Giới hạn

- Mỗi ô một lần thu: chưa đo dao động giữa các lần chạy. Chênh lệch quyết định ở đây là 1 ca (K 4 → 3) và 0,5–1,0 hạng. Bản chọn là **tạm** cho tới khi chạy lặp.
- Chọn trên dữ liệu đã xem; 37 bản trên 12–13 ca. H1c, H7c thiết kế sau khi xem 9 ca T-062; lượt 2 và H5b thiết kế sau khi xem tập chọn.
- Chưa so baseline. Chưa dùng ô đánh giá. Không rút được: tốt hơn baseline, hiệu quả trên tập đánh giá, lợi ích đồ thị nói chung.
- Đính chính sau phản biện lượt 1 (R2): V002 so với V028 là phép **thêm/bỏ H1c trên nền P7 đang dùng quan hệ**, không phải đối chứng "bỏ quan hệ". V002 không tắt E1/E2/E5 của P7: nó vẫn tính mẫu độc quyền theo quan hệ cha–con và vẫn xét kế thừa qua cạnh trước khi xếp hạng. Phép so này chỉ cho thấy H1c (hậu xử lý xuất cạnh) không đổi thứ tự nút ở 13/13 ca. **Đối chứng bỏ quan hệ mà SPEC hỏi chưa được chạy trong T-064**; kết luận về tác dụng tính toán của quan hệ trên FlashTicket còn mở và phụ thuộc phép so đó.

## 9. Đính chính sau phản biện lượt 1 (13/11/2026 22:48Z)

Nguồn: `tasks/T-064-m1-flashticket/REVIEW.md` và bảng phản hồi cuối file đó. Các số ở mục 2–5 không đổi.

- **R1 — lỗi phân loại cạnh trong H1 (đúng, chưa sửa mã).** `h1_canh.py` lấy mẫu cạnh gọi từ `m1.span.mau_canh` (gộp theo cặp service) rồi gán mọi cạnh loại `http`. Trên tải mua vé, bốn tuyến giữa Booking, Payment, Ticket chứa mẫu PRODUCER → CONSUMER (message), riêng Payment → Booking trộn cả hai loại.
  - Phạm vi đã đếm trên đầu ra V028: 4 cạnh `http` sai loại ở **13/13** ca dev bản 2, 0 ở 9 ca T-062 (tải đọc). **Không cạnh nào trong số đó có cờ** ở 13 ca, nên chúng nằm cuối danh sách cạnh và không tham gia chèn cạnh của H1c.
  - Chưa biết: sau khi tách mẫu theo loại, phép chấm từng nhóm có sinh cờ mới hay không. Vì vậy bảng cạnh và tổng hạng của mọi bản có H1 (H1a, H1b, H1c và các bản gộp, tổ hợp chứa chúng) là **kết quả của mã có lỗi này**, giữ nguyên làm lịch sử, chưa dùng để chốt bản có cạnh.
  - Không bị ảnh hưởng: các bản không bật H1, gồm P7, V002 và V032 đang đứng đầu theo §5.
  - Sửa dự kiến: tách mẫu theo loại span (CLIENT → SERVER, PRODUCER → CONSUMER) trước khi gộp và chấm, trong `src/m1_ft` (không sửa `src/m1`); mã nguồn mới, sổ mới, chạy lại các bản H1 trên 22 ca, giữ lượt cũ.
- **R2 — tên phép so (đúng, đã sửa ở mục 4 và 8).**
- **R3 — thiếu WHY (đúng, đã thêm WHY-85 và WHY-86, ghi rõ là ghi muộn).** Sàn 1 ms là ngưỡng thực dụng; lý do "hạt lập lịch" là giả thuyết chưa kiểm.
- **R4 — trạng thái quyền (đúng, đã sửa ở mục 4).** Theo quyền đã cấp và đúng §5: bản đề xuất của người làm là **V002-H8s1 trên tập A**; nếu Minh nhận tập B thì là **V032-H5b**. Đây vẫn là kết quả tạm: còn R1, các hướng chưa hoàn tất và đầu ra thiếu ở mục 7.

## 10. Tập chọn chính: 13 ca (ghi 13/11/2026 23:21Z)

Minh nhận "Sửa sau 1" và quyết dùng tập 13 ca (`docs/DECISIONS.md`, mục "Tập chọn dev bản 2: nhận "Sửa sau 1", dùng 13 ca"). Tập 12 ca giữ làm lịch sử và báo độ nhạy.

- Theo đúng §5 trên tập 13 ca, với số đã chấm ở lượt 1 và 2: **bản đề xuất tạm là V032-H5b** (AC@1 6/8, AC@3 8/8, tổng hạng 10, K 4/5; không hồi quy trên T-062, K 4/4 bằng P7). V032 không bật H1 nên không chịu lỗi R1.
- Đứng thứ hai: V034-H1c+H5b+H8s1 (AC@1 6/8, tổng hạng 11, K 3/5, cạnh 3/3) — bản có H1, chờ kết quả lượt 3.
- Hệ quả phải nêu: bản đứng đầu theo §5 **không giảm K** so với P7 (4/5) và không có đầu ra cạnh. V032 hơn P7 ở đúng một ca (PAUSE-PAYMENT), bằng thành phần được thiết kế sau khi xem ca đó.
- Mục 4 và mục 9 viết trước quyết định này; phần "nếu Minh nhận tập B" ở đó nay là trường hợp áp dụng.

## 11. Kết quả lượt chọn 3 — sau khi sửa R1 (14/11/2026 00:31Z)

Nguồn: `kiem/kiem-luot3.json`, `cham/chon-dev2-luot3-tap{12,13}.json`, `cham/khong-hoi-quy-3.json`; sổ 10 dòng `chon_dev2_luot3` trước và sau chấm. Mã nguồn `7b4249ff…`.

- **Hợp lệ:** 220/220 (bản, ca) có kết quả, không lỗi, hai lần chạy trùng SHA. Đối chứng mã nguồn: V046 (cấu hình V028 với `gop_loai_cu`) trùng V028 lượt 2 và V047 trùng V002 lượt 1 ở 13/13 ca dev bản 2 và 9/9 ca T-062, ngoài siêu dữ liệu.
- **Phân loại sau sửa:** không có cạnh loại `khong_ro` ở bất kỳ (bản, ca) nào.
- **Tác động của bản sửa lên kết quả:** ở tám bản có H1, thứ tự nút (thực thể, nhóm hòa) **trùng bản cha ở 22/22 ca**. Danh sách cạnh có cờ trùng bản cha ở mọi bản trừ V043-H1a tại ba ca (19b17e22, fb1cf0e9, 60166807). AC@1, AC@3, tổng hạng, K và bảng cạnh của cả tám bản **bằng bản cha** trên tập 12 ca, tập 13 ca và T-062.
- **Diễn giải.** Quan sát: tách message khỏi http không đổi điểm nào trên dữ liệu này. Suy luận: ở các bản H1b/H1c, các cạnh tách ra không được định vị là cạnh riêng nên không vào danh sách chung; ở H1a có cạnh đổi cờ nhưng không chạm đáp án. Chưa lần từng cạnh đổi cờ của V043.
- **Bản thay thế có cạnh nay dẫn tới bản đã sửa:** V039-R1-H1c+H8s1 (thay V028) và V041-R1-H1c+H5b+H8s1 (thay V034). Các bản H1 của lượt 1 và 2 giữ làm lịch sử.
- **Thứ tự §5 trên tập 13 ca không đổi:** V032-H5b đứng đầu (AC@1 6, AC@3 8, tổng hạng 10, K 4/5); kế đó V041 (= V034: tổng hạng 11, K 3/5, cạnh 3/3). Tổng số bản đã chấm trên tập chọn: 47 (27 + 10 + 10), trong đó 5 bản là đối chứng mã nguồn.

## 12. Đối chứng bỏ quan hệ, lượt 4 (14/11/2026 05:20Z)

**Quan sát (từ file chấm, không suy rộng).** Bốn bản V048–V051 là bản cha có thêm DC-bo-quan-he (tắt E1, E2, E5 của P7). Nhận 88/88 `summary.json` (52 dev bản 2 + 36 T-062), status OK, trùng SHA hai lần chạy; gói `results/T-064/kiem/nhan-luot4/luot4-out.tgz` trùng hash hai đầu (`1bc349bc…`). Chấm: `cham/dc-luot4-tap{12,13}.json`, `dc-luot4-t062.json`; so cặp: `cham/dc-luot4-so-cha.json`.
- Trên cả tập 12 và tập 13, cả bốn cặp: AC@1 và K không đổi, AC@3 giảm 2 (7→5 ở P7/V002/V041 trên tập 12; 8→6 ở V032/V041 tập 13), tổng hạng cắt tăng 4–6. Ba ô đổi hạng ở mỗi cặp (chung: e9c9679b hạng 1 → 4–5,5 và 98ea5ba4 hạng 2–2,5 → 4–5,5; thêm 4af494a5 hoặc 60166807). Verdict giữ CAUSE_FOUND ở mọi ô khác.
- Cặp V051 so V041 còn có 98ea5ba4 trong nhóm tụt quá 2 bậc.
**Suy luận (chưa kiểm cơ chế).** Quan hệ có tác dụng tính toán trên các ô e9c9679b, 98ea5ba4 và 4af494a5/60166807: bỏ chúng làm hạng xấu đi. Chưa đọc trung gian từng ô nên chưa nêu được bước nào mất thông tin; chưa phân xử cạnh nào (E1, E2 hay E5) đóng góp vì ba cạnh tắt cùng lúc.
**Chưa làm.** So cặp trên T-062 (đã chấm, chưa lập bảng cặp); tách từng loại E1/E2/E5; đây là phép kiểm hiệu quả của việc dùng quan hệ, không đổi thứ tự chọn ở §11.

## 13. Dời mốc ±30 s và H8 (phiên C; ghi 14/11/2026 07:40Z)

Nguồn: `results/T-064/phien-c/BAN-GIAO-C.md` §3–5, WHY-87, 88, 89. Số liệu lấy từ bàn giao đó; điều phối chưa tự tính lại từ `cham/doi-moc*.json`, `cham/h8.json` (chưa kiểm lại).

- **Quan sát (dời mốc).** Tập 13 ca: P7, V032, V041 giữ AC@1 5/6/6 ở d = 0 và −30; ở +30 V041 xuống 4, V032 xuống 5, P7 giữ 5. Thử giả d = −300 làm AC@1 P7 5 → 1. Ô nhạy: HTTP5-EVENT (e9c9679b, 98ea5ba4), PAUSE-PAYMENT (V032, V041 1 → 3 ở +30), BINH-THUONG 83073ed1. 9 ca T-062 ở +30: AC@1 P7 và V032 5 → 3.
- **Cơ chế đã xác nhận trên trung gian (phiên C):** C1 ngưỡng E4 nhảy vào phân bố lỗi khi N chứa 30 s lỗi; C2 H5b mất điều kiện liveness; C3 `nhanh_z` chia IQR_N chuỗi phẳng. Chưa kiểm: REDIS-BOOK của V041 đổi `phia_dich`, CPU-BOOK-2 của V041, ngưỡng từng đơn vị ở 83073ed1, 98ea5ba4 ở −30.
- **Suy luận.** Mọi bản M1 nhạy với mốc muộn 30 s; lợi thế của V032 ở PAUSE-PAYMENT mất ở +30. Hệ quả cho RCA trực tuyến (mốc từ cảnh báo): yêu cầu thiết kế, **chưa kiểm**.
- **H8-adapter (WHY-88).** Chỉ thuong01 (ca chạy thử) làm adapter ghim ném lỗi; 22 ca hai tập không có tình huống nên KHONG_TAC_DUNG theo chữ §4 nhưng đúng nghĩa là **chưa thử được hiệu quả xếp hạng**. Thành phần đáp ứng nhu cầu kỹ thuật (P7 ERROR cả ca), không là xử lý hạn chế phương pháp (luật 18). Chờ ô RECREATE-PAY của phiên B.
- **H8-log (WHY-89).** V062, V063, V065: KHONG_TAC_DUNG. V064 (H8lc, phép 1): tổng hạng cắt 15 → 13, GIU (l1), lợi từ **một ô** PAUSE-PAYMENT (payment lên hạng 4 nhờ `log-kq-ok`), ô người làm đã thấy khi đếm log. Phép 2 (trên V032): không tác dụng vì V032 đã giải ô bằng H5b. Theo §5 (4), thêm H8lc vào V032 không có căn cứ trên tập này.
- **Còn mở (quyết định phụ thuộc):** có đưa H8-log-chuoi vào ứng viên cuối không (nghiêng: không, lý do trên; chờ ô mới của B để phân xử); chạy d ∈ {−60, −15, +15} sau đợt thu B (~1 giờ máy, trong quyền, chưa phát); biến thể bền với mốc muộn cần sổ + WHY riêng.

## 14. Đính chính sau phản biện lượt 3 (REVIEW-3; ghi 14/11/2026 ~12:05Z, phiên 5)

Nguồn: `tasks/T-064-m1-flashticket/REVIEW-3.md` và bảng phản hồi cuối file. Số ở §12, §13 không đổi; chỉ thu hẹp diễn giải.

- **R6 — phạm vi §12.** Lượt 4 là phép **tắt E1/E2/E5 của P7**, không phải bỏ toàn bộ quan hệ ở mọi cặp.
  - V048 (P7), V049 (V002), V050 (V032): với E1 = `tat`, E2 = `tat`, E5 = False, E6 = `a`, lõi `src/m1` không còn phép tính dùng cạnh khi xếp hạng (PageRank chỉ ở E6b; E7 chỉ dựng vùng báo cáo; H8s1, H5b không đọc cạnh). Ba cặp này là bỏ quan hệ trọn vẹn so với bản cha của chúng.
  - V051 (V041 + DC) **còn H1c**: đọc cặp span cha–con khác chủ, chấm cạnh, chèn cạnh vào danh sách chung; bộ chấm chiếu cạnh về nút. Người phản biện đếm 312 bản ghi cạnh, 12 cạnh có cờ ở 8 ca của V051. Vì vậy cặp V041 → V051 chỉ đo tác dụng của E1/E2/E5 khi H1c vẫn bật.
  - Câu "quan hệ có tác dụng tính toán" ở §12 chỉ đứng cho ba cặp đầu, trong phạm vi E1/E2/E5 và 12–13 ca dev đã thấy. Đối chứng bỏ toàn bộ quan hệ của V041 là V067 (lô 5, WHY-96); tách riêng H1c là V066.
- **R7 — câu §13 "lợi thế của V032 ở PAUSE-PAYMENT mất ở +30".** Sửa thành: ở +30, **H5b mất ưu tiên hạng 1** (điều kiện chết im không còn thỏa); H5 vẫn đưa payment lên **hạng 3**, trong khi P7 vắng. Tại +30, V032 vẫn hơn P7 ở AC@3 (8 so 7) và tổng hạng cắt (13 so 16) (`phien-c/cham/doi-moc.json#/ban/V056-DM-V032-t+30/dev2/tong`, `#/ban/V055-DM-P7-t+30/dev2/tong`). "Hệ quả cho RCA trực tuyến" sửa thành: cần xử lý hoặc đánh giá phía N bị lẫn dữ liệu lỗi khi mốc muộn; phép thử ±30 s không xác lập điều kiện cần cho mọi độ trễ (**chưa kiểm**).
- **N1 (người làm tự tìm) — K khi dời mốc.** §13 bỏ sót: K của P7 và V032 tăng 4 → 5 ở cả d = −30 và +30 (ca 83073ed1 BINH-THUONG chuyển `CAUSE_FOUND`); V041 giữ 3 (`phien-c/cham/doi-moc.json#/ban/<bản>/dev2/K`). K = 4/5 của V032 ở d = 0 nhạy mốc như xếp hạng.
- **R8.** WHY-87–89 ghi sau kết quả; đính chính ở WHY-94.

## 15. Lô 5 trên tập dev bản 3 và bản đề xuất cuối V082 (ghi 14/11/2026 ~16:25Z, phiên 5)

**Dữ liệu.** Tập chọn `tap-chon-dev3-17.json` (13 ca dev2 + 4 ca thu bù 3; 11 ca lỗi, 6 ca không lỗi; WHY-95); tập độ nhạy `tap-dev3-19-do-nhay.json` (+2 ca lặp bản 3); 9 ca T-062. Đáp án `dap-an-dev3.json` (A, chính) và `dap-an-dev3-B.json` (B; WHY-97). Đầu ra lô 5 phần d = 0 và V082: `kiem/nhan-luot5/` (hash `NHAN-D0.sha256`; mọi cặp hai lần trùng SHA). 31 lỗi chạy ở ca ebd5ef38 (RECREATE-PAY), bản không H8-adapter, "Multiple runtime series…" — khai trước ở WHY-96, tính trượt (§2).

**Quan sát (điểm thô; AC@1, AC@3 là tổng trên 11 ca lỗi; nguồn `cham/chon-dev3-d0-v082-A.json#/ban/<bản>/chon/tong`, `/K`).**

| Bản | AC@1 | AC@3 | Tổng hạng cắt | K | Cạnh đúng top 3 | T-062 (AC@1, K) |
|---|---|---|---|---|---|---|
| P7 | 7 (0,64) | 9 (0,82) | 23 | 5/6 | – | 5/5, 4/4 |
| V061 = H5b + H8a | 9 (0,82) | 11 (1,00) | 13 | 5/6 | – | 5/5, 4/4 |
| **V082 = H5b + H8s1 + H8a** | 9 (0,82) | 11 (1,00) | 13 | 4/6 | – | 5/5, 1/4 |
| V071 = V082 + H1c | 9 (0,82) | 11 (1,00) | 14 | 4/6 | 3/4 ô | 5/5, 1/4 |
| V072 = V071 + H3 + H4 | 9 | 11 | 13,5 | 4/6 | 0/4 ô | 5/5, 1/4 |

- Đáp án A và B cho kết quả giống hệt ở mọi bản (mọi bản xếp booking-service hạng 1 ở ca 659a9dfb1ab0); thứ tự §5 không đổi.
- Theo ca (P7 → V082): PAUSE-PAYMENT vắng → 1 (H5b); RECREATE-PAY lỗi chạy → 1 (H8a); EVENT-DB-LAT 2 → 1 và CPU-BOOK-2 1 → 2 (H8s1); BINH-THUONG 729604d2 và ba ca BINH-THUONG T-062 hết báo nhầm (H8s1). Các ca khác giữ hạng.
- Luật giữ (§4; `cham/giu-bo-dev3-d0-v082-A.json`): phép 1 so P7 — giữ H8s1 (l2), H5 (l1), H5b (l1), H8a (l1), H8lc (l1), H1c (l3); không tác dụng H8s0, H6a, H7, H7c, H3, H4, H8lk; đánh đổi H2; bỏ H1a, H1b. Phép 2 quanh bản gộp — H8a giữ (V082 vs V066; V061 vs V032; V071 vs V041), H8s1 giữ l2 (V082 vs V061), H5b giữ (V061 vs V060), H1c giữ l3 nhưng X xấu đi (V071 vs V082: 14 so 13), H3, H4, H3+H4 không tác dụng (V068–V070 vs V061), H8lk, H8lc không tác dụng khi đã có H5b.
- §5 (`.../xep_5`): 1 V082, 2 V061, 3–5 V068–V070, 6 V072, 7 V071. Mọi ứng viên không hồi quy T-062.
- **Đối chứng quan hệ (REVIEW-3 R6).** Bỏ toàn bộ quan hệ của V041 (V067 = H5b + H8s1 + bỏ E1/E2/E5, không H1c): 8/10/19 → 7/8/24, K không đổi. Bỏ E1/E2/E5 trên nền không H1 (V066 → V067): 8/10/18 → 7/8/24. Riêng H1c (V041 vs V066): 19 so 18, xấu đi nửa hạng ở hai ca. Trên P7, V002, V032 kết quả cùng chiều (bảng `quan_he`).

**Suy luận và cơ chế.**
- Lợi của H8a chỉ đến từ một ca: ebd5ef38 có nhiều chuỗi runtime cho một metric logic sau khi pod payment tạo lại; P7 dừng lỗi, H8-adapter gộp chuỗi nên chạy được và xếp payment hạng 1.
- H3 và H4 **chưa được phân xử**: ô của chúng (POOL-EVENT 86dea661, CONSUMER 659a9dfb1ab0) đã hạng 1 ở P7 và mọi bản, nên tập dev không chứa ca nào để thành phần có thể giúp. Đây không là bằng chứng có hay không có lợi. Phân xử cần ô có tín hiệu pool/queue mà P7 xếp sai.
- V072 mất bảng cạnh (EVENT-DB-LAT, REDIS-BOOK, NET-GW-BOOK hạng cạnh 2 → ~30): H3 thêm kênh `metric|event-service_pool-used`, `pool-wait` lớp `khong_lan` có cờ ở bên gọi; bước định vị cạnh `CanhDinhVi` (`src/m1_ft/thanh_phan/h1_canh.py`) coi đó là bằng chứng riêng của bên gọi → `dinh_vi = phia_goi`, `co = 0`. Đúng điều kiện thất bại đã ghi trong docstring và lý do của tham số `bo_kenh_dinh_vi` (mặc định rỗng). Ứng viên sửa (chưa kiểm): đặt `bo_kenh_dinh_vi` là tên kênh pool khi gộp H1c với H3.
- H8s1 đổi CPU-BOOK-2 1 → 2: ở V082, điểm mạnh nhất của booking-service giảm (khóa thứ hai 1325,5 → 758,7; số kênh có cờ 60 → 45) nên event-service lên đầu (`kiem/nhan-luot5/l5/dev2/d0/V082-V066+H8a/60166807/method-output-1.json#/entity_ranking`). Giải thích ứng viên: sàn 1 ms làm giảm điểm chuẩn hóa của kênh có độ phân tán nền dưới 1 ms; kênh cụ thể bị giảm **chưa kiểm**. Cùng cơ chế giải thích hết báo nhầm ở bốn ca không lỗi (dao động dưới 1 ms không còn bị gắn cờ) — **chưa kiểm** từng kênh.

**Ứng viên và quyết định.** Theo §5 đã khóa, bản đứng đầu là V082. Minh chọn V082 (DECISIONS 14/11 "Bản đề xuất cuối…", WHY-98). Cấu hình: `cau-hinh-de-xuat.json`; chỉ mục xuất cho T-065: `ban-xuat/chi-muc-ban.json` (bản 2: P7, V082 đề xuất, V071 thay thế có đầu ra cạnh; bản tạm trước giữ ở `chi-muc-ban-tam-1.json`).

**Giới hạn.**
- V082 được thiết kế sau khi xem điểm tập chọn (sổ dòng 180); số dev của nó lạc quan. Các bản đầu bảng chênh nhau một ca.
- H3, H4 chưa phân xử (xem trên). H8a chỉ có một ca bằng chứng.
- V082 không có đầu ra cạnh; vai trò tính toán của quan hệ trong V082 là E1/E2/E5 của lõi P7 (đối chứng V066 → V067 cho thấy bỏ đi làm xấu xếp hạng trên tập dev này).
- Độ nhạy dời mốc của V082 chưa chạy (chờ Minh duyệt; lượt > 1 giờ). Bảng độ nhạy cho P7, V032, V041 ở d ∈ {−60, −30, −15, +15, +30} đang chạy (lô 5, phần dời mốc).

**Câu hỏi còn mở.** Lợi của H8s1 có giữ trên dữ liệu khác không (đánh đổi CPU-BOOK-2); H3/H4 có ích khi P7 xếp sai ô pool/queue không; H1c có nên đi kèm `bo_kenh_dinh_vi` không nếu cần đầu ra cạnh.

## 16. Độ nhạy dời mốc trên tập dev bản 3 (ghi 14/11/2026 ~18:31Z, phiên 5)

**Dữ liệu và cách chạy.** Dời mốc t′ = t + d, d ∈ {−60, −30, −15, +15, +30} s, dựng lại đầu vào và xuất bù gói metric quanh t′ (đường WHY-87/WHY-96). P7, V032, V041: lô 5 (`V052–V057`, `V073–V081`; dev2 ±30 từ phiên C); V082: Minh duyệt 16:29Z (sổ `chay_them`), 140 cặp. Đầu ra `kiem/nhan-luot5/l5/<nhóm>/d<d>/` (`l5-dm.tgz`, hash trong `NHAN-D0.sha256`); mọi cặp trùng SHA; 15 lỗi chạy ebd5ef38 ở P7/V032/V041 (không H8-adapter), không cặp thiếu gói. Chấm: `cham/spec-dev3-doi-moc.json` → `cham/doi-moc-dev3-A.json` (B cho cùng kết quả).

**Quan sát** (tập chọn 17 ca: AC@1/11, AC@3/11, tổng hạng cắt, K/6; T-062: AC@1/5, K/4; nguồn `cham/doi-moc-dev3-A.json#/ban/<bản> d<d>/<tập>`):

| d (s) | P7 | V032 | V041 | **V082** | V082 T-062 |
|---|---|---|---|---|---|
| −60 | 7/8/25,9/K6 | 8/9/21/K6 | 8/9/20/K5 | **9/11/14/K5** | 5, K3 |
| −30 | 7/10/20/K6 | 8/10/18/K6 | 8/9/20,5/K4 | **9/11/14/K4** | 5, K2 |
| −15 | 7/9/23/K6 | 8/10/19/K6 | 8/9/20,5/K5 | **9/11/14/K5** | 5, K1 |
| 0 | 7/9/23/K5 | 8/10/18/K5 | 8/10/19/K4 | **9/11/13/K4** | 5, K1 |
| +15 | 7/9/24/K4 | 8/10/19/K4 | 9/9/19/K3 | **10/11/13/K3** | 4, K1 |
| +30 | 6/9/25/K6 | 6/10/22/K6 | 5/9/25/K4 | **6/11/18/K4** | 4, K1 |

- V082 không kém P7 ở mọi d trên AC@1, AC@3 và tổng hạng; AC@3 giữ 11/11 ở cả sáu mức. K của V082 dao động 3–5 (P7: 4–6).
- Ở +30 mọi bản tụt AC@1 (P7 6, V032 6, V041 5, V082 6). Với V082, sáu ca đổi hạng 1 → 2/3 (HTTP5-EVENT, REDIS-BOOK, PAUSE-PAYMENT, CONSUMER, HTTP5-EVENT-FLASH 2 → 3, T-062 NET-GW-BOOK); CPU-BOOK-2 2 → 1.
- Ở −60, V082 thêm báo nhầm ở bốn ca BINH-THUONG (729604d2, 83073ed1, 6c1a9fd8, e8661e0a) và bớt ở eb48d6b3; HTTP5-EVENT 1 → 3.

**Suy luận.** Lợi của V082 so với P7 không phụ thuộc mốc trong khoảng [−60, +15] s trên tập này. Mốc muộn +30 s là điểm yếu chung (cửa sổ N lẫn dữ liệu lỗi, như §13/§14 R7 đã nêu) — không do thành phần riêng của V082. Đây là độ nhạy trên dev, không là đánh giá giữ ngoài; giải thích cửa sổ N ở +30 vẫn là ứng viên **chưa kiểm** từng ca.

## 17. Sửa sau phản biện lượt 4 (REVIEW-4 R9, R10; Minh duyệt 15/11/2026 "Duyệt cả ba"; ghi ~03:52Z, phiên 5)

**R9 — H5b nhận "chết im" sai ở RECREATE-PAY.** Kênh `live-down` cũ (biểu thức T-063 qua `query_range`) giữ mẫu lỗi trong lookback, nên ở ebd5ef38 payment bị coi là không phản hồi 285 s dù đã phản hồi lại từ t+53. Điều kiện thất bại này đã ghi ở WHY-93 nhưng §15 và WHY-98 không nêu — bỏ sót của người làm.
- Sửa (WHY-99): kênh theo "lần dò mới nhất", dựng từ mẫu thô (`kiem/r9/xuat_live_down_moi.py`); không đổi `src/m1_ft`. Phép kiểm chỉ đọc trước khi sửa (`kiem/r9/so-live-down-2.json`): trên 140 gói có kênh, chỉ 6 gói ebd5ef38 lệch; PAUSE-PAYMENT 46aab4be giữ chết im ở mọi mốc. Biểu thức thử đầu (`max_over_time[15s]`) bị loại vì làm mất chết im thật ở 46aab4be (`kiem/r9/so-live-down.json`).
- Chạy lại 12 cặp (V061, V068–V072, V082 ở d = 0; V082 ở d −60, −30, −15, +15, +30), đầu ra `kiem/nhan-r9/r9/` (hash `kiem/nhan-r9/NHAN-R9.sha256`), mọi cặp trùng SHA. Ở đầu ra mới `#/extra/m1_ft/chu_thich/H5-liveness/chet_im/thanh_phan` rỗng; payment vẫn hạng 1 (nhờ H8-adapter, như V060).
- Chấm lại với `goc_uu_tien` (`cham/spec-dev3-d0-v082-r9.json`, `cham/spec-dev3-doi-moc-r9.json`): **mọi tổng, K, luật giữ/bỏ, thứ tự §5 và bảng dời mốc giống hệt** bản trước (so `.txt` từng dòng); 26 slot dùng đầu ra R9, không slot nào đổi hạng, p1, p3, k, verdict hay nhóm hạng 1; chỉ byte đầu ra đổi. A và B vẫn giống nhau. Nguồn: `cham/chon-dev3-d0-v082-r9-A.json`, `giu-bo-dev3-d0-v082-r9-A.json`, `doi-moc-dev3-r9-A.json`.
- Hệ quả: lợi của H8a ở RECREATE-PAY không nhờ H5b; H5b đúng nguyên lý trên hai ca liveness của tập (PAUSE-PAYMENT kích hoạt, RECREATE-PAY không). Chỉ mục xuất bản 3 (`ban-xuat/chi-muc-ban.json`; bản 2 giữ `chi-muc-ban-2.json`) đổi đúng 2 slot ebd5ef38 (V082, V071); cấu hình đề xuất cập nhật nguồn điểm (bản trước `cau-hinh-de-xuat-2.json`). Dashboard T-065 L8b dựng từ chỉ mục bản 2: hai slot này cần T-065 xuất lại để khớp hash (hạng và cờ hiển thị không đổi).

**R10 — ca 1e5a3dc5.** Xem `phan-tich/ghi-chu-co-che-dev2.md` Q7 và `chu-thich-thao-tac-nen.md` §5: báo nhầm do một cờ CPU Payment tự sinh (có ở mọi bản, cả P7); ca đối chứng tải ×1 7d1ee32f cùng cờ, mạnh hơn, nên không gán cho tải ×3; nguyên nhân CPU đổi **chưa phân xử** (khả năng và dữ liệu cần nêu ở Q7).

**Đính chính §15.** Câu "kênh cụ thể bị giảm **chưa kiểm**" (H8s1 ở CPU-BOOK-2) sai: Q6 trong `phan-tich/ghi-chu-co-che-dev2.md` (13/11) đã lần đủ — sàn 1 ms bỏ hai đơn vị trong tiến trình của Booking (`Session.persist …Reservation`, `TicketTypeInventoryRepository.saveAll`), `max s` Booking 1.325,5 → 758,7 < 782,2 của Event. Phần "hết báo nhầm ở bốn ca không lỗi" vẫn là ứng viên (Q6 đo tỉ lệ độ vượt/h ≤ 0,8 ở bốn ca BINH-THUONG, chưa kiểm từng kênh ở ca T-062).

**Đính chính §17 (15/11 05:00Z, theo T-065 REVIEW-4 T2).** Câu "chỉ byte đầu ra đổi" và "hạng và cờ không đổi" (§17, LOG, brief L11 của T-065) nói hẹp hơn thực tế. Ở ebd5ef38, cả V082 và V071: thứ tự thực thể và `tie_group` không đổi, các chỉ số chấm không đổi; nhưng `#/extra/kenh_co` 65 → 64 (mất `metric|payment-service_live-down`), khóa của payment-service [3, 0, 0, 0, 0] (khóa H5b ghi đè) → [2; 4.511,15; 1,8; 30; 12.625,94] (khóa P7 gốc), và chú thích H5b `chet_im.thanh_phan` rỗng (`kiem/nhan-luot5/l5/dev3/d0/<bản>/ebd5ef38/` so `kiem/nhan-r9/r9/dev3/d0/<bản>/ebd5ef38/`).
