# T-032 — Kết quả phiên 12 (11/10/2026): ba phép kiểm chạy trên laptop

Người làm: Claude. Ba phép kiểm này Minh duyệt chạy sau khi báo cáo chính đã viết (lời duyệt ghi ở LOG phiên 12). Thiết kế viết trước khi chạy: `thiet-ke-phep-doi-012.md`. File này nối tiếp `ket-qua-phien-11.md`; viết tắt KQ12.

**Ghi thêm ở phiên 13.** Ba chỗ của file này đã được kết quả sau sửa hoặc bổ sung: câu về `frontend` ở cuối mục 1 (đã sửa tại chỗ); câu "điểm nguồn là thay đổi thật" của mục 3 (xem `ket-qua-phien-13.md` mục 6); mục 4 (KT-9 đã chạy ở phiên 13). Bảng các câu bị sửa: `ket-qua-phien-13.md` mục 8.

**Cách đọc các số.** Mọi số là trên tập dev. Số của nhánh phép đổi đo tác động của bước tính, không phải thành tích của một phương pháp. Hạng 1 tính bi quan khi hòa. Đường dẫn tính từ `results/T-032/`; con trỏ JSON ghi sau dấu `→`.

## 1. KT-3 — MicroRank: ghép bộ chia theo bài gốc với đếm riêng

Nguồn: lượt `runs/microrank-kt3-001/` trên laptop (script `scripts/laptop_contrast_v7.py`); tổng hợp `runs/microrank-kt3-001/collect-001/summary.json` (script `scripts/laptop_contrast_collect_v5.py`). Hai bước bị đổi cùng lúc: hai tập trace (như nhánh `mo15`, `mo1p50` của KQ11 mục 4.2) và số đếm của nhóm bất thường (đếm riêng, như M-C1 của KQ9 mục 2).

**Kiểm.** 260/260 tiến trình con xong, 1.173 giây, RAM hệ thống đỉnh 73,5%, không lần chờ hay giết nào (`runs/microrank-kt3-001-launch/stdout.txt`, dòng cuối). Nhánh giữ nguyên `shampc` khớp bản đóng băng từng bit ở 52/52 ca (48 OK, 4 ERROR tái lập đúng ERROR) và hạng root trùng T-028 ở 52/52. Nhánh `c1h` (bộ chia native, đếm riêng qua chỗ móc mới) cho hạng root trùng nhánh M-C1 của phiên 9 ở 48/48 ca, tức chỗ móc tính đúng điều đã khai (`→ /summary/self_check`).

**Quan sát** (`→ /summary/<dataset>/<nhánh>`; 47 ca tính được ở cả nhánh ghép lẫn nhánh chỉ thay bộ chia: 25 RE2-TT, 22 Nezha-OB; 4 ca nguồn ERROR và 1 ca N/A theo mốc 90% giữ trạng thái):

| | RE2-TT (25 ca) | Nezha-OB (22 ca) | Cộng (47 ca) |
|---|---|---|---|
| Hạng 1: bản gốc | 2 | 0 | 2 |
| Hạng 1: chỉ thay bộ chia, luật của bài / luật của code | 14 / 15 | 7 / 7 | 21 / 22 |
| Hạng 1: chỉ đếm riêng (`c1h`), trên cùng các ca | 16 | 2 | 18 |
| Hạng 1: ghép, luật của bài / luật của code | 17 / 19 | 6 / 8 | 23 / 27 |
| Trong 5 hạng đầu: chỉ thay bộ chia → ghép, luật của bài | 23 → 25 | 14 → 13 | 37 → 38 |
| Trong 5 hạng đầu: chỉ thay bộ chia → ghép, luật của code | 23 → 25 | 14 → 16 | 37 → 41 |
| So với chỉ thay bộ chia, luật của bài: root tăng / không đổi / giảm hạng | 8 / 16 / 1 | 8 / 7 / 7 | 16 / 23 / 8 |
| So với chỉ thay bộ chia, luật của code: tăng / không đổi / giảm | 6 / 19 / 0 | 12 / 5 / 5 | 18 / 24 / 5 |
| Ca đang hạng 1 dưới nhánh chỉ thay bộ chia bị mất hạng 1, luật của bài / của code | 0/14; 0/15 | 2/7; 3/7 | 2/21; 3/22 |
| Ca root hòa với thực thể khác, luật của bài / của code | 0; 0 | 7; 3 | 7; 3 |

- Thực thể đứng đầu khi root chưa hạng 1 dưới nhánh ghép (`→ /top_entity_when_root_not_first`): ở Nezha-OB là `frontend` ở 14/16 ca (luật của bài) và 11/14 ca (luật của code); root không phải `frontend` ở ca nào trong số đó (đếm từ `→ /cases`). Ở RE2-TT: `ts-auth-service` 3 ca, `ts-admin-travel-service` 2 ca.
- Dưới bộ chia mới có trace bất thường không chứa span nào mang cờ ở 33 ca (luật của bài) và 25 ca (luật của code) (`→ /abnormal_traces_without_flagged_span`).

**Đối chiếu với dự đoán khai trước** (mốc: nhánh ghép hơn nhánh chỉ thay bộ chia từ 4 ca hạng 1 ở ít nhất một luật, và số ca tụt ít hơn số ca tăng).

- Luật của code: hơn 5 ca (22 → 27), tăng 18 so với giảm 5. **Đạt mốc.** Luật của bài: hơn 2 ca (21 → 23), tăng 16 so với giảm 8; không đạt phần "từ 4 ca". Theo đúng chữ đã khai ("ở ít nhất một luật"), dự đoán "một phần của số ca còn lại là do đếm phủ" **được hỗ trợ**, và tôi ghi kèm là hai luật không cho cùng mức.
- Phần được hỗ trợ nằm ở RE2-TT: 14 → 17 và 15 → 19 trên 25 ca, không ca đang đúng nào mất hạng 1, chỉ 1 và 0 ca tụt hạng. Ở Nezha-OB kết quả không ổn định (7 → 6 và 7 → 8; 7 và 5 ca tụt hạng; 7 và 3 ca hòa), đúng như giới hạn đã nêu về số trace bất thường rất ít.

**Kết luận ở mức tính toán.** Ở RE2-TT, sau khi thay bộ chia, bước đếm phủ vẫn là nơi làm root mất hạng ở thêm 3–4 ca; ghép hai phép đổi đưa root lên hạng 1 ở 17–19/25 ca và vào 5 hạng đầu ở 25/25 ca. Phần còn lại chưa giải thích giảm từ 25–26/47 ca xuống 20–24/47 ca (RE2-TT 6–8 ca, Nezha-OB 14–16 ca).

**Quan sát thêm, đã kiểm theo ca (sửa ở phiên 13).** Ở Nezha-OB, thực thể đứng đầu của phần còn lại gần như luôn là `frontend`, dịch vụ ở đầu mọi yêu cầu. Bản đầu của đoạn này viết rằng điều đó "khớp với hạn chế H4, H7"; câu đó **không được hỗ trợ ở phần lớn ca**. Kiểm theo tên thao tác (lệnh chỉ-đọc trên bản ghi của lượt này, `cases/Nezha-OB/*/mo15c1|mo1p50c1/ban-ghi-0.json → /ranking`): thao tác cao nhất của `frontend` là lời gọi tới root ở 3/14 ca (luật của bài) và 3/11 ca (luật của code). Bảng nối theo cây span (`ket-qua-phien-13.md` mục 5) cho cùng kết quả: "gắn với root" ở 3/14 và 3/11 ca, không tìm thêm ca gián tiếp nào; ở các ca còn lại, thao tác cao nhất của `frontend` là lời gọi tới dịch vụ khác và các trace tạo ra điểm của nó không chứa root, hoặc chỉ có dưới 5 span.

**Giới hạn.** Hai bước đổi cùng lúc, không quy được cho riêng bước nào. Không phải MicroRank gốc (span đầu do ta quy ước, mức nền ngắn). Nghĩ ra sau khi xem kết quả dev. Ba ca đã đọc tay đổi theo các hướng khác nhau: `dev-3ae0a6c15a` vẫn hạng 4 dưới cả hai luật; `dev-12a1a88069` hạng 2 (luật của bài) và hạng 1 (luật của code); `dev-9b9397a4dc` hạng 9 và hạng 1.

## 2. KT-8 (nửa MicroRank) — bốn ca ERROR khi bỏ thao tác không có ở đoạn nền

Nguồn: nhánh `dropnew` của cùng lượt; `collect-001/summary.json → /summary/dropnew_error_cases`. Đây là đổi đầu vào, không phải đổi một bước tính; không thay số đã chấm.

**Kiểm.** Ở 48 ca không có thao tác mới, nhánh `dropnew` khớp bản đóng băng từng bit ở 48/48 ca (`→ /summary/self_check/dropnew_exact_where_native_ok`).

**Quan sát.** Ở cả 4 ca chỉ có một thao tác thiếu nền, `ts-order-other-service_getMore ts.orders`. Sau khi bỏ span của nó, phương pháp chạy được ở 4/4 ca:

| Ca | Ô | Span bị bỏ / tổng span sau mốc | Trace có span bị bỏ / tổng | Hạng root | Số thực thể trên root | Thực thể đứng đầu |
|---|---|---|---|---|---|---|
| `dev-03d4910932` | route, socket | 527 / 158.370 | 195 / 1.320 | 2 | 1 | `ts-station-service` |
| `dev-16870e660c` | route, mem | 444 / 148.073 | 167 / 1.280 | 2 | 1 | `ts-station-service` |
| `dev-4e68956051` | train, delay | 339 / 123.487 | 130 / 1.006 | 3 | 2 | `ts-station-service` |
| `dev-a5cabe5fa7` | travel, loss | 210 / 174.798 | 71 / 1.507 | 12 | 11 | `ts-station-service` |

**Đọc.** Bốn ca này cư xử như 24 ca sai khác của MicroRank ở RE2-TT: `ts-station-service` đứng đầu, root không hạng 1 ở 0/4 ca, trong 5 hạng đầu ở 3/4 ca. Vậy việc đang tính 4 ca là "trượt" ở hạng 1 không làm lệch kết luận nào; ở mức 5 hạng đầu thì 3 ca đang bị tính trượt sẽ thành trúng nếu bỏ thao tác thiếu nền.

**Chưa làm.** Nửa TraceRCA của KT-8 (chạy trên EC2) chưa được duyệt, chưa chạy.

## 3. KT-15 — CIRCA: bước DA cộng gì, cho nút nào

Nguồn: `runs/circa-da-addition-001/summary.json` (script `scripts/circa_da_addition_v1.py`); chỉ đọc 30 file trung gian của nhánh quan sát ở lượt `runs/circa-laptop-k2-001` (nhánh đó khớp bản đóng băng từng bit ở 30/30 ca). Không chạy phương pháp.

**Kiểm** (`→ /summary/self_check`, `/summary/all`). Khóa sau DA bằng điểm trước DA cộng phần được cộng ở 1.574/1.574 nút được cộng. Nút không được cộng giữ nguyên điểm ở 7.031/7.031. Phần được cộng bằng đúng điểm lớn nhất trong các nút con với tới (đi theo chiều cạnh; nút con dưới ngưỡng 3 thì chuyển tiếp nút con của nó) ở 1.574/1.574 nút; chiều cạnh khớp ở 30/30 ca.

**Quan sát trên 19 ca không có nút cực lớn** (`→ /summary/khong_co_nut_cuc_lon`).

- Tỷ lệ nút được cộng nhận cùng một giá trị phổ biến nhất: nhỏ nhất 9%, trung vị 15%, lớn nhất 35%. Số ca mà hơn nửa số nút được cộng nhận cùng một giá trị: 0/19.
- Tương quan hạng giữa số hậu duệ của nút và phần được cộng: dương ở 16/19 ca, âm ở 3; trung vị 0,21 (từ −0,10 tới 0,68).
- Dịch vụ của nút nguồn cho giá trị phổ biến nhất: `ts-preserve-service` ở 9/19 ca.

**Ba ca DA làm root tụt hạng mà không dính giá trị cực lớn** (`→ /summary/da_lowers_root_without_huge`); root của cả ba là `ts-auth-service`, có 5 hậu duệ trong đồ thị metric:

| Ca | Hạng root trước → sau DA | Điểm của root trước DA; phần root được cộng | Giá trị phổ biến nhất; nút nguồn | Thực thể mới vượt root sau DA nhận đúng giá trị đó |
|---|---|---|---|---|
| `dev-16597725c1` (auth, cpu) | 2 → 15 | 823,68; 405,65 | 2.027,36; `ts-preserve-service_latency` | 13/13 |
| `dev-f81f88234e` (auth, delay) | 10 → 22 | 7,56; 29,85 | 61,71; `ts-preserve-service_latency` | 11/12 |
| `dev-57546fd87b` (auth, delay) | 40 → 46 | 11,48; 1,42 | 68,77; `ts-preserve-other-service_latency` | 4/7 |

Hai ca DA giúp root mà không dính giá trị cực lớn (`→ /summary/da_raises_root_without_huge`), cả hai là order, loss: root có 19 và 24 hậu duệ, được cộng 206,83 và 296,02 (điểm trước DA 176,29 và 83,66).

**Đối chiếu với hai giải thích khai trước.**

- (b) "chuyển một điểm lớn": mốc đã khai (hơn nửa số nút nhận cùng một giá trị ở từ 2/3 số ca) **không đạt**: 0/19.
- (a) "thiên lệch theo số hậu duệ": tương quan dương nhưng yếu; không đủ để nói phần được cộng do số hậu duệ quyết định.
- Vậy xét trên mọi nút, **không giải thích nào trong hai giải thích khai trước mô tả đúng**. Phần được cộng đến từ nhiều nút nguồn khác nhau.

**Kết luận ở mức mô tả, cho đúng điều đã kiểm.** DA cộng cho mỗi nút điểm lớn nhất của các nút con. Khi một nút của dịch vụ không liên quan có điểm cao, mọi nút cha của nó được nâng cùng một lượng. Ở ba ca root tụt hạng, các thực thể vượt root là các thực thể nhận lượng đó (13/13, 11/12, 4/7). Cách đọc tôi viết ở `doc-tay.md` trước khi chạy phép kiểm này, "DA bất lợi cho dịch vụ không có cạnh", **sai**: root có hậu duệ và cũng được cộng. Đã sửa ở `doc-tay.md` mục 5.3, 5.5, 7.2, báo cáo chính mục 3.5 và 6, `kiem-tiep.md` mục KT-15.

**Còn mở.** Vì sao cột độ trễ của `ts-preserve-service` có điểm cao ở các ca root là `ts-auth-service`: thuộc câu "metric của dịch vụ không liên hệ đổi tại mốc", không phân xử được bằng dữ liệu hiện có (`kiem-tiep.md` mục KT-6).

**Giới hạn.** Mô tả trên trung gian, không phải phép đổi. Dự đoán của mục này viết sau khi tôi đã mở trung gian của một ca (ghi ở đầu file thiết kế). Chỉ RE2-TT; đồ thị gần như giống nhau giữa các ca.

## 4. Phép kiểm cần laptop mà không chạy

**KT-9** (đổi cửa sổ train và đoạn chấm của CIRCA). Ở phiên 12 không chạy; lý do tôi nêu lúc đó (ước 1–2 giờ máy; chưa có thiết kế) không đứng được: lượt CIRCA tương tự trên laptop đã đo là 595 và 407 giây. Minh duyệt chạy; phiên 13 đã chạy với thiết kế `thiet-ke-phep-doi-013.md` mục 5, hết 985 giây. Kết quả: `ket-qua-phien-13.md` mục 6.
