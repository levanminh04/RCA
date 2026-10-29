# Đính chính phiên 10 — T-043

- **Ngày:** 29/10/2026. **Người làm:** Claude. **Phần hai (Đ19–Đ22)** ở cuối file. **Trạng thái phần một:** đã ghi theo lời Minh: "nếu không có mâu thuẫn giữa 2 bên thì duyệt sửa luôn, có mâu thuẫn thì trình codex phản biện". Hai bên không còn mâu thuẫn về R1–R4 (LOG phiên 10). Codex chưa kiểm bản đã ghi.
- **Nguồn:** hai lượt Codex phản biện ngày 29/10/2026 (R1–R4, rồi kiểm phản hồi), hai lượt người làm đáp. Tóm tắt từng điểm ở LOG T-043 phiên 10.
- **Nguyên tắc:**
  - không sửa 10 file đóng băng ở phiên 7;
  - không sửa `dinh-chinh-phien8.md`, `dinh-chinh-phien9.md`, để giữ lịch sử;
  - bản này thay đúng các câu nêu dưới đây. Câu nào của các bản trước không được nêu thì vẫn giữ.
- **Thời điểm nhìn dữ liệu:** mọi sửa đặt sau khi đã có pha 2 có nhãn và kết quả baseline P3, trước mọi kết quả M1. Không sửa nào đổi tập ô kích hoạt hay số T0 của ma trận.

## Đ15. Phân loại mẫu Drain khi có severity UNKNOWN (R1)

**Lý do:** đặc tả v1 §5 ghi "mỗi mẫu xếp lỗi hay thường theo đa số dòng của nó ở N. Hòa xếp vào lỗi". SPEC E3 ghi UNKNOWN không là lỗi, không là không lỗi, nhưng vẫn đi vào Drain. Với mẫu toàn UNKNOWN, phiếu là 0–0, nên luật hòa xếp mẫu thành lỗi. Với mẫu trộn, đặc tả không nói UNKNOWN có được tính phiếu hay tính vào số đếm. Người cài sẽ phải tự quyết.

**Dữ kiện dev:** ở Nezha-OB, adservice và cartservice có log nhưng không có dòng nào có severity xác định, ở cả N và A, trong 22/22 ca (`ks16/dem-khong-nhan.json#/cases/*/log/thuc_the_N_co_log_khong_xac_dinh`, `#/cases/*/log/thuc_the_A_co_log_khong_xac_dinh`; điều kiện tính ở `ks16/ks16_pha1_v11.py:644–645`: số dòng > 0 và số dòng xác định = 0).

**Thay câu "Mẫu Drain" trong đặc tả v1 §5 (Quy ước [T-043]) bằng:**

1. **Phạm vi.** Quy tắc severity dưới đây áp cho nguồn có severity (Nezha-OB). RE2-TT giữ bộ từ khóa SimpleRCA: mỗi dòng là lỗi hoặc không lỗi, không có UNKNOWN; luật đa số và luật hòa như cũ.
2. **Đơn vị phân loại** là cặp (thực thể, mẫu). Lớp tính từ dòng N quan sát được của thế giới đang tính, rồi giữ cố định khi đọc A.
3. **Phiếu.** n_lỗi, n_không là số dòng N của cặp có severity xác định là lỗi, không lỗi. Dòng UNKNOWN không là phiếu.
   - n_lỗi + n_không = 0: lớp **không xác định**. Cặp này không tạo kênh có hướng. Bản ghi vẫn lưu số dòng của cặp ở N và A.
   - n_lỗi + n_không > 0 và n_lỗi ≥ n_không: lớp **lỗi** (hòa có phiếu xác định vẫn xếp lỗi, như luật cũ).
   - n_lỗi < n_không: lớp **thường**.
4. **Kênh đếm** của cặp đã phân loại đếm **mọi** dòng khớp mẫu ở N và A, kể cả dòng UNKNOWN và dòng có severity ngược lớp. Tên đúng là "tần suất mẫu được phân loại lỗi (hoặc thường) từ N". Kênh này không phải số dòng lỗi đã xác nhận.
5. **Mẫu đã biết** của một thực thể là mẫu có ít nhất một dòng N của chính thực thể đó, kể cả mẫu thuộc lớp không xác định. Dòng A khớp một mẫu đã biết không vào ô "mẫu mới". Ô "mẫu mới" của thực thể gom dòng A không khớp mẫu đã biết nào của thực thể. Điểm này làm rõ chữ "mẫu nào học từ N" khi Drain học chung cho mọi thực thể.
6. **Báo kèm** theo cặp: n_lỗi, n_không, số UNKNOWN ở N và ở A.

**Giả định (chưa kiểm):** lớp học từ N còn đúng nghĩa ở A.
- Sai khi một mẫu Drain gộp dòng có ý nghĩa khác nhau.
- Sai khi severity của cùng mẫu đổi giữa N và A.
- Khi UNKNOWN chiếm phần lớn mẫu, kênh đo thay đổi tần suất hành vi, không đo lỗi tăng.

Đây là điều kiện thất bại của E3, ghi thêm vào đặc tả v1 §7.3 điểm 8.

**Hệ quả trên dev (suy từ dữ kiện trên, chưa chạy M1):** ở Nezha-OB, mọi cặp của adservice và cartservice thuộc lớp không xác định, nên hai thực thể này không có kênh mẫu Drain. Chúng vẫn có ô "mẫu mới". UNKNOWN chưa được chứng minh là log bình thường. Lớp không xác định chỉ có nghĩa là không có căn cứ chọn hướng.

**Đáp án đặc tả** (ví dụ giả, không phải dữ liệu thật; dùng làm fixture cho task cài đặt):

| # | Nguồn | Dòng N của cặp | Dòng A của cặp | Lớp | Kênh, giá trị N → A | Ghi chú |
|---|---|---|---|---|---|---|
| U1 | Nezha-OB | 100 UNKNOWN | 200 UNKNOWN | không xác định | không có kênh | lưu 100, 200; dòng A không vào ô mẫu mới |
| U2 | Nezha-OB | 1 ERROR, 99 UNKNOWN | 200 UNKNOWN | lỗi (1 > 0) | tần suất mẫu lỗi: 100 → 200, hướng lên | số lỗi xác định 1 → 0, báo kèm; cờ của kênh, nếu có, không có nghĩa lỗi tăng |
| U3 | Nezha-OB | 3 ERROR, 3 INFO | 6 dòng bất kỳ | lỗi (hòa có phiếu) | tần suất mẫu lỗi: 6 → 6 | như luật cũ |
| U4 | Nezha-OB | 2 ERROR, 5 INFO, 10 UNKNOWN | 34 dòng bất kỳ | thường (2 < 5) | tần suất mẫu thường: 17 → 34, hướng xuống | dòng UNKNOWN tính vào số đếm |
| U5 | Nezha-OB | 0 dòng của thực thể X (mẫu chỉ có dòng N ở thực thể khác) | 5 dòng của X khớp mẫu | — | 5 dòng vào ô mẫu mới của X | theo điểm 5 |
| U6 | RE2-TT | 4 dòng có từ khóa, 6 dòng không | 10 dòng bất kỳ | thường (4 < 6) | tần suất mẫu thường: 10 → 10 | không có UNKNOWN |

Tỷ lệ chấm, cổng và trạng thái (LOW_SUPPORT, NO_BASELINE…) theo B1.3 như mọi đơn vị đếm; bảng trên chỉ chốt lớp và cách đếm.

**Thu hẹp hai câu của phản hồi lượt 1 (người làm):**
- "Log bình thường bị đọc như log lỗi": UNKNOWN chưa được chứng minh là log bình thường. Câu đúng: luật hòa cũ gán hướng lỗi cho mẫu không có căn cứ severity.
- "Số kênh trong khóa K phình ra": theo SPEC (dòng 397), khóa K chỉ đếm kênh có cờ. Câu đúng: luật cũ tạo thêm kênh có hướng cho hai thực thể này. Kênh chỉ vào khóa K khi qua cổng và có cờ; chưa có kết quả M1 để nói đã xảy ra.

**Thu hẹp N1 (người làm):** E3 có 4 ô kích hoạt (`ks16/dem-sau-ghep-nhan.json#/o_kich_hoat/E3/tong_o`), nên là thành phần ít ca. Luật chọn khối vẫn xét HẠI ở lượt một trước, rồi mới giữ thành phần ít ca ở lượt hai. Luật C cũng xét bước 1–3 trước bước 4. Vì vậy chưa biết cấu hình cuối có E3 hay không. R1 vẫn chặn cài E3, vì mọi cấu hình thử có E3 đều cần định nghĩa xác định được.

## Đ16. C-h (PRISM) về trạng thái ứng viên (R2)

**Lý do:** định nghĩa C-h ở đặc tả v1 §8 và thẻ PRISM chưa xác định được từ đầu vào tới thứ hạng. Còn thiếu:
- có dùng cổng và cờ E4 hay không;
- chấm độ lệch tuyệt đối hay theo hướng;
- xử lý tỷ lệ thành công khi R0 tắt E3 (đặc tả §5: khi đó kênh này không có hướng chấm);
- gộp theo thời gian (phụ lục PRISM chưa cho đủ quy tắc);
- thang khi IQR = 0, kênh thiếu, thực thể không có thuộc tính bên ngoài.

Câu "điều kiện đó thỏa" ở thẻ đọc là quá mạnh. Câu "|x − trung vị|/IQR đúng như PRISM" trong phản hồi lượt 1 cũng quá mạnh: bài đưa một họ điểm lệch với thang dương; IQR chỉ là một lựa chọn.

**Thay:**
- Đặc tả v1 §8, dòng C-h: bỏ khỏi bảng đối chứng của bản P7. C-h là ứng viên.
- `ma-tran-thu.json#/buoc/13` (mục `"ma": "T13"`): bỏ "C-h" khỏi `so_sanh`; `so_cau_hinh` đổi "+ 8 đối chứng" thành "+ 7 đối chứng".
- Dự toán T13 (báo cáo §9): bỏ C-h; không đổi khoảng thời gian đã ước.

**Hệ quả:** chưa có phép so với quy tắc phân biệt thuộc tính nội bộ và bên ngoài. Các đối chứng đã duyệt khác giữ nguyên (C-a0, C-a1, C-d1, C-d2, C-d3, C-c, C-g; vế mốc giả C-e).

**Điều kiện thêm lại:** công thức C-h khóa trọn vẹn trước khi chạy, ghi rõ phần kế thừa PRISM và phần tự thích nghi, Minh duyệt. Phép so với M1 khi đó vẫn trộn cách chấm và cách dùng quan hệ, nên không dùng riêng để quy lợi ích cho E5.

## Đ17. Diễn giải luật C khi P ≤ M (R3)

**Lý do:** luật C dừng ở bước đầu tiên khớp (SPEC Phụ lục C). Câu "ca có ΔMRR gộp > δ nhưng P ≤ M đi tới bước 7" bỏ điều kiện ấy. Ngoài ra, P ≤ M không có nghĩa lợi ích chỉ nằm ngoài nhóm.

**Phản ví dụ** (Codex; người làm tính lại): trong nhóm, một ca từ hạng 5 lên 1 (+0,8), hai ca từ hạng 9 xuống 10 (−0,0111 mỗi ca); ngoài nhóm không đổi. P = 1, M = 2, ΔMRR gộp = (0,8 − 0,0222)/52 ≈ 0,01496 > δ = 0,01. Lợi ích đến từ trong nhóm.

**Thay câu ở `dinh-chinh-phien9.md` Đ10** ("Ca có ΔMRR gộp > δ nhưng P ≤ M (lợi ích chỉ có ngoài nhóm) đi tới bước 7: TRÁI CHIỀU theo ô, Minh quyết.") bằng:
> "Nếu chưa dừng ở bước 1–4, ca có ΔMRR gộp > δ nhưng P ≤ M không đạt GIÚP; bước 6 không áp vì |ΔMRR gộp| > δ; nên tới bước 7: TRÁI CHIỀU theo ô, Minh quyết. P ≤ M không có nghĩa lợi ích chỉ nằm ngoài nhóm. Với E3 (|E_X| = 4 < 6), luật dừng ở bước 4 nếu chưa dừng ở bước 1–3."

**Câu quá rộng ở LOG phiên 9 (dòng N9 và bảng phương án):** "lợi ích ngoài nhóm vẫn được trình Minh" chỉ đúng khi luật chưa dừng ở bước 1–4. LOG chỉ ghi thêm, nên không sửa dòng cũ; câu đúng là câu trên.

**Chính sách A′ (Q-207) và SPEC giữ nguyên.** Q-207 là quyết định đã ghi; ghi chú đính chính phần diễn giải trong `docs/DECISIONS.md` là đề xuất riêng, chờ Minh duyệt (LOG phiên 10).

## Đ18. Lý do hoãn nối log–span (R4)

**Lý do:** hai lý do cũ không đứng được.
- "Chỉ một dataset nối được, nên phép tính không chung cho hai dataset": WHY-08 đòi một lõi và một định dạng chung, không đòi mọi dataset có cùng loại thông tin. E3 hiện đã có nhánh theo dataset (severity ở Nezha-OB, từ khóa ở RE2-TT).
- "Chưa có câu hỏi trên dev mà nối log–span phân xử được": SPEC E3 đã nêu hai ứng viên dùng được liên kết, và Nezha-OB có 1.537.834/1.539.335 dòng khớp đúng một span (`ks16/dem-khong-nhan.json#/cases/*/log_span_join/tong`).

**Thay đặc tả v1 §7.3b, đoạn "Đề xuất [T-043]" và ba gạch đầu dòng, bằng:**
> "Đề xuất [T-043]: chưa dùng nối log–span trong bản P7. Đây là lựa chọn ưu tiên phạm vi, không phải kết luận rằng nối quá tốn hay không thử được trên dev. Phương án một lõi có nhánh khi thiếu liên kết là khả thi và không trái WHY-08. Dùng nối cần thiết kế thêm: kênh (a) và trạng thái khi thiếu liên kết; hợp đồng E5 theo request cho (b); phạm vi phép thử. Phạm vi phép thử chưa thiết kế, nên chưa nói được phải nhân rộng khối K hay không. Chưa ước lượng phần việc. Câu hỏi OPEN: nối log–span có cải thiện RCA không; Nezha-OB dev phân xử được câu này. Nơi nhận: chặng 2, khóa trước chặng 3 (`bang-chuyen-giao.json`, dòng `log_span`). Hoãn có thể đẩy một phép phân xử khả thi trên dev ra sau. Chưa có bằng chứng buộc phải cài nối ngay, cũng chưa có bằng chứng bỏ nối không mất lợi ích."

WHY-M1-07 trong `why-de-xuat.md` được viết lại theo đúng nội dung này.

## Ghi chú: dung sai đồng hồ (không sửa)

Hai bên thống nhất: khuyến nghị giữ τ = 1 ms cố định. τ xuất hiện trong `happensBefore` của E1-CP và trong E9; E1-U trừ hợp các khoảng con đã cắt, không dùng τ. Giữ cố định không phải bằng chứng 1 ms đã được hiệu chỉnh cho dữ liệu này. Mục này vẫn chờ Minh quyết ở báo cáo §11.

---

## Phần hai — Đ19–Đ22 (sau bản đánh giá toàn bộ T-043 của Codex, F1–F3)

- **Trạng thái:** đã ghi theo lời Minh "Duyệt ghi Đ19–Đ22" (29/10/2026), sau hai lượt Codex (F1–F3, rồi kiểm phản hồi) và hai lượt người làm đáp. Codex chưa kiểm bản đã ghi.
- Nguyên tắc như phần một: không sửa SPEC, file đóng băng, các bản đính chính trước.

## Đ19. Hợp đồng thời gian và đầu vào cạnh tĩnh (F1)

**Lý do:**
- `hop-dong.json#/vao/metrics/cot/time` và `#/vao/logs/cot/timestamp` ghi "giây hoặc ns" mà không nói M1 biết đơn vị bằng cách nào.
- Adapter Nezha (`src/p3/nezha.py:248`) ghi `metric.time` là mốc của front_service; thời gian thật từng nguồn nằm trong `provenance`. Phép kiểm ở `nezha.py:304` chỉ bảo đảm cùng phân hoạch N/A, không bảo đảm cùng khoảng H hay cùng ô 10 giây.
- SPEC cố định API 7 tham số (SPEC dòng 156); T12 cần cạnh tĩnh (SPEC dòng 787, D8) nhưng `params` chỉ có cờ `T12`.
- Không có căn cứ nói cách dùng mốc frontend đã làm sai phân hoạch hiện tại. Đây là thiếu sót của đặc tả giao diện, không phải bằng chứng số KS-16 sai.

**Bổ sung `hop-dong.json#/vao/params` (không đổi chữ ký API):**

1. **Đơn vị.** `params.don_vi_thoi_gian` = {`spans.start_us`: "us", `metrics.time`: "s" | "ns", `logs.timestamp`: "s" | "ns"}. Adapter khai theo dataset. M1 không suy đơn vị từ độ lớn giá trị; thiếu khai thì bản ghi ERROR.
2. **Chuẩn hóa chỉ áp cho mốc thời gian.** M1 đổi mọi mốc sang ns, kiểu int64, để chia N/A, tính F/H, chia ô 10 giây và tính khởi phát. Giá trị đặc trưng giữ đơn vị gốc: thời lượng span theo µs, metric theo đơn vị cột (`hop-dong.json#/nhanh_z`; fixture 76). Đổi µs sang ns không làm tăng độ chính xác.
3. **Thời gian riêng của nguồn metric.**
   - `params.nguon_metric` = {kênh: nguồn}.
   - `params.thoi_gian_nguon` = {nguồn: danh sách mốc ns, hoặc chuỗi `"metrics.time"`}.
   - Chuỗi `"metrics.time"` chỉ dùng khi adapter xác nhận cột chung là thời gian thật của các kênh thuộc nguồn đó (ví dụ RE2-TT: một file metric mỗi ca).
   - Nguồn không có thời gian riêng và không có xác nhận đó:
     - các phép cần thời gian của nguồn (F/H, ô, khởi phát) ghi UNSUPPORTED theo nguồn;
     - kênh của nguồn vẫn được chấm N/A nếu `params.phan_hoach_NA_da_kiem[nguồn]` = true (adapter đã kiểm cùng phân hoạch, như `nezha.py:304`);
     - nếu chưa kiểm: kênh không được chấm, ghi UNSUPPORTED theo nguồn trong `chan_doan`.
   - Không thay thời gian nguồn bằng thời gian của nguồn khác rồi chỉ gắn cờ.
   - Trên Nezha-OB dev, runner truyền mốc ns thật của từng nguồn từ `provenance`; nhánh thiếu không xảy ra. E9 trên Nezha-OB vẫn chỉ dùng trace.
4. **Độ phân giải.** `params.coverage` đổi từ `{nguồn: [khoảng ghi]}` (Đ2) thành `{nguồn: {"khoang": [[đầu, cuối]], "r_ns": int}}`. `r_ns` là bước nhỏ nhất của mốc thời gian nguồn ghi, đơn vị ns; là độ phân giải của mốc, không phải độ chính xác thật. Trên dev, runner lấy từ `hop-dong.json#/quan_sat/do_phan_giai_r`. M1 không tự đặt mặc định; thiếu thì F/H của nguồn là UNSUPPORTED.
5. **Cạnh tĩnh.** `params.canh_tinh` = {`revision`: str, `canh`: [[nguồn, đích], …]}, tên sau alias. Chỉ đọc khi T12 bật.
   - Thiếu khóa khi T12 bật: bản ghi UNSUPPORTED.
   - Khóa có mặt, `canh` = []: hợp lệ; phép hợp không đổi; ghi `so_canh_tinh = 0`.
   - Đồ thị kiến trúc không phải nhãn; bộ kiểm trường cấm vẫn duyệt cả `params`.

**Đáp án đặc tả** (ví dụ giả):

| # | Đầu vào | Kết quả |
|---|---|---|
| H1 | nguồn S có mốc riêng `[0, 60e9, 120e9]` ns; `metrics.time` = `[1e9, 61e9, 121e9]` | H của S tính theo mốc riêng |
| H2 | nguồn S thiếu mốc riêng, `phan_hoach_NA_da_kiem[S]` = true | kênh của S vẫn chấm N/A; F/H của S là UNSUPPORTED |
| H3 | như H2 nhưng `phan_hoach_NA_da_kiem[S]` vắng | kênh của S không chấm; UNSUPPORTED theo nguồn |
| H4 | T12 bật, thiếu `canh_tinh` | bản ghi UNSUPPORTED |
| H5 | T12 bật, `canh` = [] | kết quả bằng cạnh quan sát; `so_canh_tinh = 0` |
| H6 | `don_vi_thoi_gian` vắng | bản ghi ERROR |

## Đ20. Sửa hàm tìm khe tham chiếu (F2)

- `fixture/kiem_bo_sung.py` `quan_sat_khe`: bản cũ so hai khoảng kề nhau sau khi sắp xếp, không hợp khoảng lồng nhau. Bản mới hợp khoảng trước khi tìm khe (cùng cách `F_tu_khoi`, `ks16/ks16_pha1_v11.py:357`).
- Fixture B8 (`fixture/fixture-bo-sung.json`), đầu vào của Codex: `r_s` = 1, `file` = `[[0,99],[10,19],[30,39]]`, cửa sổ `[0,100)`. Bản cũ cho T_chắc N = 40; đáp án 50.
- Lượt `fixture/runs/kiem-bo-sung-002.json`: 8/8 khớp. Lượt 001 (bản cũ, 7 mục) giữ.
- Không ảnh hưởng số KS-16: `F_tu_khoi` đúng; `runs/khe-open-002` đọc đầu ra pha 1, không gọi hàm này.

## Đ21. Diễn giải E1-CP (F3)

Thay ba câu: báo cáo dòng 20 ("gần như không có ca để phân xử"), báo cáo dòng 229 ("không có ca để phân xử"), thẻ CRISP ("chỉ kiểm được trên dữ liệu có lời gọi song song"). Câu mới:
> "Không đạt điều kiện chạy K-b theo Q2 (ngưỡng 5%). Nezha-OB có 444/277.534 cha có chồng lấn hơn 1 ms (`ks16/dem-khong-nhan.json#/cases/*/trace/parents_with_overlap`, `parents_with_ge2_children`); khác biệt E1-CP so với E1-U trên các trace này chưa được kiểm. Chồng lấn chưa chứng minh là song song thật; τ = 1 ms chưa được hiệu chỉnh cho dataset này."

Quyết định không chạy E1-CP ở K-b giữ nguyên.

## Đ22. Dự toán nối log–span (bổ sung Đ18)

**Đã có, dùng lại được:**
- code nối của KS-16 (`ks16/ks16_pha1_v11.py`, khối `log_span_join`);
- số đo: 1.537.834/1.539.335 dòng khớp đúng một span (`ks16/dem-khong-nhan.json#/cases/*/log_span_join/tong`);
- thời gian máy đã đo cho toàn bộ pha 1 trên 22 ca Nezha-OB, gồm cả phần nối: tổng 92,2 s, tối đa 4,72 s/ca, RSS tối đa 1,41 GB (`ks16/dem-khong-nhan.json#/cases/*/cost`). Đây là cận trên chi phí đọc và nối.

**Chưa có, phải thiết kế:**
- (a) kênh "tỷ lệ lần thực hiện có log lỗi": đơn vị, mẫu số, trạng thái khi thiếu liên kết, nhánh RE2-TT, fixture;
- (b) E5 theo request: hợp đồng mới, gồm đường giải thích theo trace và điều kiện thất bại;
- phạm vi phép thử: đề xuất một cặp bật/tắt (a) tại cấu hình thắng, chỉ trên Nezha-OB, thay vì nhân rộng khối K.
- Cache M1 (báo cáo §9) là phần sẽ xây ở task cài đặt, chưa có sẵn.

**Dự toán (chưa kiểm):**
- (a): khoảng nửa đến một phiên thiết kế cộng một lượt phản biện; phần cài nằm trong task cài đặt (1); thời gian máy thêm dưới vài phút trên cache M1, khi cache đó đã được xây.
- (b): ít nhất một phiên thiết kế riêng cộng phản biện; chưa ước được phần cài.
- Dự toán sai khi: 1.501 dòng không khớp tập trung ở thực thể quan trọng; span không tương đương request (chưa kiểm); cache M1 không giữ khóa span.

Quyết định hoãn hay làm vẫn chờ Minh (báo cáo §11).
