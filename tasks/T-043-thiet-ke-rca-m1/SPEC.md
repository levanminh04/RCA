# T-043 — M1: thiết kế chuỗi chẩn đoán RCA và giao thức thử trên dev

- **Trạng thái:** đề xuất, bản 3 (24/10/2026). **Chưa duyệt triển khai.**
  - Bản 3 gộp các sửa sau năm lượt phản biện của Codex trong chat (hai lượt với bản 1, ba lượt với bản 2) và các điểm người làm tự tìm. Minh duyệt sửa và tạo file theo Q-194, Q-195.
  - Các mục D1–D12 (phần D) chờ Minh quyết.
  - Lượt sửa cuối của bản 3 được Codex phản biện ngày 25/10/2026 (R14–R16). Sửa R14–R16 ghi theo Q-196, sau khi Codex kiểm lại đề xuất sửa; Codex chưa kiểm văn bản đã ghi.
  - Cùng ngày, sau các lượt R17–R24 và lượt kiểm luật chọn, ghi theo Q-197: luật chọn khối tổ hợp (B4), hợp đồng chấm và bảng chuyển giao (B1.9), sửa R20 (cờ cần nhãn chuyển sang bộ đánh giá), R21 (span qua mốc t), phép đếm log–span ở KS-16, giới hạn của đơn vị đếm khi tải đổi. Codex đã kiểm nội dung đề xuất, chưa kiểm văn bản đã ghi.
  - Lịch sử bản nháp, phản biện và xử lý: `LOG.md` của task này.
- **Người làm:** Claude (DECISIONS, dòng Q-189 "duyệt claude làm thiết kế"). **Người phản biện:** Codex.
- **Thuộc gói MRP:** P6 (M1 trong `docs/PLAN-P6.md`). **Cổng:** chuẩn bị G3.
- **Mã task:** người làm đề xuất T-043, vì thư mục task trước đó kết thúc ở T-042. Minh quyết (D1).

## Mục tiêu

**Câu hỏi nguồn:**
- DT18-NV2: log, trace, metric được ánh xạ lên đồ thị phụ thuộc để xác định vùng ảnh hưởng, phát hiện dấu hiệu bất thường và xếp hạng nguyên nhân (`docs/reference/sources/DT18-de-tai-va-nhiem-vu.md` §2).
- Cô: bước 2 và bước 4 (`docs/reference/sources/advisor-2026-09-23.md` §1).
- MRP: RQ3b; RQ3c (vùng nghi ngờ); RQ3d; P6 tầng 1–4; cấu trúc tổng (M-32, M-48 trong `docs/KE-HOACH-GIAI-DOAN-TOI.md`).

**Loại task:** thiết kế. Có thêm một phép đếm mô tả chỉ đọc (KS-16) và một đặc tả fixture có đáp án tính tay. Task không cài phương pháp và không chạy thử thành phần trên dev.

**Đạt task này** cho đủ căn cứ để mở các task cài đặt và thử. Nó chưa đủ để chọn thành phần, khóa G3 hay khẳng định lợi ích của đồ thị (MRP §3).

**Phần nguồn chưa bao phủ và nơi nhận:**
- RQ3a: phần nghiên cứu của luật cảnh báo cần một SPEC phát hiện riêng (D3).
- P/R/F1 của vùng: chỉ đo được trên FlashTicket (P10).
- P7 và P8.

## Câu hỏi, bằng chứng và quyết định

Mọi dự đoán dưới đây đều **chưa kiểm**. Luật kết cục ở phần C áp cho mọi dòng có so bật/tắt.

| # | Câu hỏi và nguồn | Lựa chọn cần phân xử; giải thích khác | Phép kiểm | Bác bỏ hoặc hỗ trợ khi | Thiếu gì, quyết định phụ thuộc |
|---|---|---|---|---|---|
| Q1 | Thời gian độc quyền có đưa root lên ở ca bên gọi chờ root không? G2-H03, H06; UV-2 | E1 bật/tắt. Giải thích khác: thiếu span con, gọi bất đồng bộ, lệch đồng hồ | Khối K (B4) | HẠI hoặc KHÔNG TÁC DỤNG theo luật C, tính tại cấu hình thắng của khối, thì bác bỏ | Bên được gọi không có span (S7) là điều kiện thất bại đã biết |
| Q2 | Đường găng (CP) có khác hợp khoảng (U) không? KS-10, CRISP | E1-CP so với E1-U | KS-16 đếm tỷ lệ con chồng lấn; K-b | Tỷ lệ < 5% ở cả hai dataset thì khai trước "không đủ ca" | Mặc định dùng E1-U |
| Q3 | Gán khoảng ngoài span bên được gọi cho bên được gọi có giúp không? UV-1, G2-H06 | E2 bật/tắt | Khối K | Luật chọn khối | Root không được gọi ở 8 ca (G2-H19) |
| Q4 | Phủ đỉnh có hơn gán thẳng cho bên được gọi không? UV-5 | E2-VC so với E2-C | K-b | Luật chọn khối, bước 9 | Cạnh đơn lẻ vẫn không định danh được |
| Q5 | Thống kê vượt ngưỡng nền có chặn điểm không hợp lệ mà không mất ca đúng không? UV-7, G2-H09/H12 | E4 so với z vững không chặn | T4b; đọc trung gian ở ca có kênh thắng mang nền IQR = 0 | Bác bỏ khi còn điểm không hữu hạn hoặc không bị chặn đi vào E5/E6. Nền hằng **không** là tiêu chí loại | Mất phân biệt độ lớn khi bão hòa (B1.3) |
| Q6 | Tín hiệu hai chiều và log theo mẫu có giúp lỗi return/exception mà không làm hỏng ca đúng không? UV-6, G2-H07 | E3 bật/tắt | Khối K | Luật chọn khối và UV-6 | Chỉ 4 ô Nezha-OB |
| Q7 | Tín hiệu cấu trúc trace (tần suất, thao tác mới, thao tác ngừng) có ích không? KS-10 | E3b bật/tắt | T6 | Luật C | Ít ca có thay đổi cấu trúc |
| Q8 | Tách tự sinh/kế thừa có giảm số ca bên gọi đứng trên root mà không hại không? MRP P6 tầng 2; G2-H17 | E5 bật/tắt. C-d1, C-d3 chỉ để báo cáo | Khối K | Luật chọn khối và D.2 lượt 5 | "Lan có đáng kể" còn mở (O09) |
| Q9 | PageRank trên đồ thị con bất thường có hơn xếp thẳng theo điểm không? Ví dụ của cô | E6b so với E6a | T9 | Luật C | Căn cứ là DT18, không phải sửa hạn chế P4 |
| Q10 | Vùng nghi ngờ có chứa root không, rộng bao nhiêu? DT18 | Hai cách dựng vùng (E7) | T10 | Chỉ mô tả | Không có nhãn vùng trên dữ liệu công khai |
| Q11 | Thứ tự xuất hiện có phủ quyết được kế thừa sai không? KS-10 E9 | E9 bật/tắt | T11 | Luật C | Nezha-OB chỉ dùng được trace |
| Q12 | Dùng quan hệ có đổi chất lượng so với cùng tín hiệu bỏ quan hệ và so với quy tắc đơn giản không? RQ3d | Chuỗi cuối so với C-a0, C-a1, C-d1, C-d3, C-c, C-g | T13, **chỉ báo cáo** | Trên dev chỉ là mô tả; P7 mới khẳng định | Không có đồ thị ngẫu nhiên (M-25) |
| Q13 | Khi không có lỗi, chuỗi có "tìm ra" nguyên nhân không? MRP §6.7 | Mốc giả C-e, **chỉ RE2-TT** | Tỷ lệ `verdict = CAUSE_FOUND` trên các cặp cửa sổ giả so được | Ràng buộc nằm trong điều kiện HẠI | Nezha-OB không có cửa sổ giả (D6) |

## Đầu vào

**Quyền dữ liệu.**
- RE2-TT: 30 ca dev trong `data/rcaeval/`, chọn qua `src/p3/selector.py`.
- Nezha-OB: 22 ca dev trong `results/T-026/allowlist-dev.json`, đọc qua `src/p3/nezha.py`.
- Không đọc `data/locked/`, 34 ca test Nezha-OB hay RE3-OB.
- Nhãn chỉ dùng ở pha 2 của KS-16, sau khi số đếm không nhãn đã được ghi và băm (barrier như T-035).

**Nguồn phải kiểm hash trước khi dùng:**

| Nguồn | Manifest để đối chiếu |
|---|---|
| `results/T-041/` | `results/T-041/manifest.json` |
| `results/T-034/ban-do-g2.json`, `goi-g2.md` | `runs/manifest-cuoi-007` |
| `results/T-035/` | `manifest.json` của T-035 |
| T-036 | `runs/doi-chieu-smtp-001/` |
| T-032 `call-interval-001`, `call-slow-001`, `chain-position-002` | `results/T-032/chuoi-bang-chung.json` |
| `results/T-026/cham-a.json` | `runs/session-005/handoff-manifest.json` |
| Bản ghi P3 của T-024 | `results/T-024/work/danh-sach-tep-cuoi.json` |
| `results/T-042/runs/normal-source-001/` | `manifest.json` của chính lượt đó |

**Trạng thái T-042:** đã đóng (Q-193). Giới hạn được chấp nhận và vẫn OPEN (Q-192). Chưa chọn baseline.

**Code và môi trường:**
- `src/p3/` (cua_so, ban_ghi, danh_gia, nezha, selector); `src/do_thi/builder.py`.
- Môi trường `D:/RCA-ext/envs/py312-pin/Scripts/python.exe` (WHY-15; SciPy 1.14.1, NetworkX 2.5).

**Nguồn ngoài:**
- PetShop: `code/baseline_anomaly_traversal.py` và `requirements.txt` tại commit 2e96f937c4c044b8b4aad03217592cd52e66db5d (requirements ghim NetworkX 2.8.8).
- CRISP, USENIX ATC 2022, §5.1–5.2.
- Tài liệu `scipy.stats.mannwhitneyu` và `permutation_test`, phiên bản 1.14.1.
- B16: `D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md`, chỉ đọc.

**Tài liệu:**
- MRP §2–3, P5–P7, §6.
- WHY-01, 02, 06, 07, 08, 10, 22, 26, 28, 51, 52, 54.
- LESSONS; DT18; thư cô.
- KE-HOACH Phần A, D.1–D.7, D.12, D.14.
- KHAO-SAT mục 1, K1, K4, mục 3–4, Phụ lục C.
- PLAN-P6 §3; T-040 `ban-giao-p6.md`.

## Đầu ra (`results/T-043/`)

1. `dac-ta-phuong-phap-v1.md`: đặc tả đủ từng thành phần như B2.
2. `hop-dong.json`: schema vào/ra, các trạng thái, gói bằng chứng, trường cấm; đơn vị đầu ra, tập ứng viên và luật "quan sát được" trên FlashTicket (B1.9).
3. `ks16/`: script chỉ đọc; `dem-khong-nhan.json`; `dem-sau-ghep-nhan.json`; trạng thái quan sát theo nguồn (B1.3b); nhật ký thời gian và RAM; hash.
4. `ma-tran-thu.json`: ma trận B4, vai trò của từng phép so, kết cục "không đủ ca" khai trước. Đóng băng trước mọi code thành phần.
5. `fixture-dac-ta.json`: các ca giả ở "Tiêu chí xong", mỗi ca có đáp án tính tay và lời giải.
6. `the-doc/`: thẻ đọc năm bài.
7. `why-de-xuat.md`: WHY đề xuất. Minh duyệt rồi mới chép vào `docs/WHY.md`.
8. `bao-cao.md`: bảng bao phủ nguồn, phần còn mở, dự toán cho task sau, giao diện cho P8/P9.
9. `bang-chuyen-giao.json`: bảng chuyển giao theo thành phần (B1.9).
10. `manifest.json`.

## Phạm vi ghi

Khi SPEC được duyệt triển khai, người làm chỉ ghi vào:
- `results/T-043/`;
- `tasks/T-043-thiet-ke-rca-m1/LOG.md`;
- dòng T-043 trong `docs/STATE.md`.

Không ghi `src/`, `docs/WHY.md`, MRP, DECISIONS, KE-HOACH hoặc task cũ.

## Các bước

0. **Kiểm hash** mọi nguồn ở mục Đầu vào. Lệch thì dừng phần phụ thuộc.
1. **Thẻ đọc năm bài.** Mỗi thẻ ghi: cơ chế, đầu vào, phần ta có/thiếu, điều kiện thất bại, chỗ đổi trong B2 (kèm trang hoặc dòng code).
   - PetShop → C-d3: đủ ba hàm.
   - CRISP §5.1–5.2 → E1-CP: luật happensBefore, cắt biên, cây con.
   - TraceDiag → E1, E5, E7.
   - PRISM → C-h.
   - DiagMLP → C-a.
   - Các bài khác của KS-14 giao về nơi dùng (B6).
2. **Hoàn thiện đặc tả v1** từ B1–B3. Kiểm: mỗi thành phần đủ 10 trường; không trường nào nhận nhãn.
3. **Đặc tả fixture và đáp án**, viết trước mọi code thành phần.
   - Kiểm: hai cách tính độc lập trong bộ nhớ cho cùng đáp án.
   - Nhánh cổng chính xác khớp oracle với sai số ≤ 1e−12.
4. **KS-16 chỉ đọc** (T0).
   - Pha 1, không nhãn:
     - cấu trúc trace;
     - mức hỗ trợ của từng đơn vị;
     - trạng thái quan sát bốn mức theo từng nguồn, từng ô 10 giây;
     - đối chiếu khoảng ghi của file trong allowlist;
     - số đơn vị theo từng chế độ tính cổng;
     - dữ liệu cho mốc giả RE2-TT;
     - ô biên và ô OPEN có bản ghi, đếm riêng theo nguồn (B1.3b);
     - nối log–span trên Nezha-OB dev: số dòng có TraceID/SpanID, khớp đúng một span, không khớp, khớp nhiều span, khớp nhưng lệch thời gian, theo file và cửa sổ; với RE2-TT ghi có hay không có cột ID.
   - Pha 2, ghép nhãn:
     - số ô kích hoạt của từng ứng viên;
     - kiểu quan sát O1–O4 của root;
     - hình dạng xếp hạng của baseline.
   - Kiểm: so các số đếm chung với T-035 và T-032.
5. **Đóng băng `ma-tran-thu.json`.** Ghi hash vào LOG trước bước 6.
6. **WHY đề xuất, bảng bao phủ, giao diện P8/P9, dự toán** cho task sau, dựa trên thời gian đo ở bước 4.
7. **Báo cáo, LOG, STATE**, kèm prompt cho Codex soát kết quả.

Phụ thuộc: bước 1 trước bước 2. Bước 3 và bước 4 làm song song được. Bước 5 cần bước 2–4.

## Kiểm đúng đắn

- **Không nhãn trong phương pháp.** API chỉ nhận spans, metrics, logs, inventory, aliases, t, params. Bản ghi qua `ban_ghi.kiem` (danh sách trường cấm CAM). KS-16 tách hai pha.
- **Fixture** dùng đáp án literal, không sinh từ chính code được kiểm.
- **KS-16** đối chiếu với T-035 K3 (22.834.238 span RE2-TT) và với T-032.
- **Không kiểm được trong task:**
  - hiệu quả của thành phần (thuộc task thử);
  - nghĩa vật lý của cạnh (O03);
  - giả định A0 trên dữ liệu công khai.

## Tiêu chí xong

1. Mọi thành phần và đối chứng ở phần C đủ 10 trường. Mỗi kết cục có ngưỡng số.
2. KS-16 xong 52/52 ca, hoặc liệt kê ca lỗi kèm lý do. Hash khớp. Có số ô kích hoạt cho từng ứng viên; có trạng thái quan sát cho từng nguồn, từng cửa sổ.
3. `ma-tran-thu.json` đóng băng trước mọi code thành phần. Số cấu hình hữu hạn. Ghi rõ vai trò của từng phép so: quyết định hay báo cáo.
4. Fixture có đủ 50 ca dưới đây, kèm đáp án:
   1. S1–S7 ở B5 (bảy ca: S1, S2, S2b, S3, S5, S6, S7).
   2. Con chồng lấn thật: cha [0,100], con [20,80] và [50,90]. Đáp án: U = 30, CP = 60.
   3. Chồng lấn 0,2 ms: con [0; 50,2] và [50; 100]. Đáp án: U = 0, CP theo CRISP = 0.
   4. Con bắt đầu trước cha 0,3: con bị cắt.
   5. Con sống lâu hơn cha: U = 10.
   6. Bản lặp y hệt bị bỏ; khóa trùng khác nội dung cho ERROR.
   7. Span mồ côi được đếm.
   8. Chu trình gọi (SCC) ở E5.
   9. E2 trên chuỗi A→B→C→D cùng hiệu ứng: gán B, C, D, cờ "không định danh".
   10. E2 một cạnh: gán R, cờ "không định danh".
   11. E2 ba bên gọi cùng vào R: gán R.
   12. E2 R gọi ra hai nơi: gán R.
   13. E2 sao quanh R có đuôi X→Y: gán R, Y gán dự phòng.
   14. E6b với Σs = 0: NO_POSITIVE_MASS.
   15. E6b với K_I = (1, 0, 1): π = (0,5; 0; 0,5).
   16. E6b với K_I = (0, 0, 1): π = (0; 0; 1).
   17. C-d3 có chu trình: UNSUPPORTED_CYCLIC.
   18. C-d3 một đích trùng root: không trả root.
   19. C-d3 không có đích: NO_TARGET.
   20. C-d3 hai đích U→V: U giữ điểm 1,4.
   21. Nửa cửa sổ không có dữ liệu: ô OPEN.
   22. N có 50 sự kiện dồn trong 150 giây, thu đủ 300 giây; A có 100 sự kiện trong 300 giây. Đáp án: e_up = 0,5.
   23. Như ca 22, nhưng 150 giây đầu N được xác nhận thiếu thu. Đáp án: e = 0.
   24. Dịch vụ sập trong khoảng có quan sát: STOPPED.
   25. Nền hằng 30 → 45, 5 + 5 mẫu: e_up = 1, p = 1/252.
   26. Cổng, A = 13 số 0 + 7 số 1, N = 20 số 0: p = 2/481, e_up = 0,35.
   27. Cổng, A = 14 số 0 + 6 số 1, N = 20 số 0: p = 0,010098, không qua cổng.
   28. Phản ví dụ R12 (mỗi phía 150 giây chắc + 150 giây OPEN, 100 sự kiện mỗi phía). Đáp án: P bình thường, S_lo tăng 0,5, S_hi giảm 0,5, OBS_DEPENDENT.
   29. Phản ví dụ R11 cộng một ứng viên điểm 0,6 ở nguồn khác: phương pháp xuất cờ RANK_CHANGED; bộ đánh giá, sau khi ghép nhãn, ghi WORLD_DEPENDENT.
   30. Hai đơn vị **đếm** cùng nguồn, cùng ca, cùng nhãn tăng: thứ tự giữa chúng không đổi qua ba thế giới.
   31. Mọi kênh LOW_SUPPORT: `INSUFFICIENT_EVIDENCE`.
   32. Mốc giả có `INSUFFICIENT_EVIDENCE`: cặp đó bị loại khỏi mẫu số.
   33. C-g với Σs_g = 0: dùng thứ tự SimpleRCA.
   34. Luật C, phản ví dụ R9: TRÁI CHIỀU theo dataset.
   35. Luật C, cả hai dataset +0,05: GIÚP.
   36. Luật C, không đổi, đủ ô: KHÔNG TÁC DỤNG.
   37. Luật C, mỗi dataset lệch một ca ngược chiều: KHÔNG TÁC DỤNG.
   38. Luật C, ít ô kích hoạt, có lợi: KHÔNG ĐỦ CA.
   39. Luật C, ít ô, chỉ hại 3 ô: HẠI.
   40. Luật C, gộp tăng nhưng P ≤ M: TRÁI CHIỀU theo ô.
   41. Cổng với nhóm trùng lớn: A = N = 50 số 0 → p = 1; A = 40 số 0 + 10 số 1, N = 50 số 0 → p = C(90,40)/C(100,50) ≈ 0,0005934196726.
   42. Cấu hình không có E4 (z vững), một kênh metric N = A = 5 số 0: z = 0, `NO_INTRINSIC_ANOMALY`. Cùng dữ liệu, có E4: p = 1, `NO_INTRINSIC_ANOMALY`.
   43. Mẫu số C-e bằng 0: vế C-e của HẠI ghi "chưa kiểm được" và không áp.
   44. Span qua mốc: cha [99,8; 100,2], con [99,85; 99,95], t = 100. Đáp án: quan hệ dựng trên toàn miền; self-time của cha 0,3 và cha thuộc A; con thuộc N.
   45. Khối, phản ví dụ R17 (hai ca, đồ thị F→R→X): MRR của gốc, E1, E5, E1 + E5 là 0,750; 0,500; 0,417; 1,000. Đáp án: chọn E1 + E5.
   46. Khối, R22: R0 0,5000; B 0,7500; B + X 0,7115; X ít ca. Đáp án: chọn B; X tắt vì cặp B / B + X cho HẠI.
   47. Khối, R23: R0 0,750000; cấu hình có đồ thị 0,746795. Đáp án: chọn R0, trình Minh vì cấu hình thắng không có E1, E2, E5.
   48. Kiểm bối cảnh, R24: X tắt khi chọn; ở chuỗi cuối, bật X tăng MRR. Đáp án: phép đảo trạng thái báo "phụ thuộc bối cảnh".
   49. Khối, hai cấu hình cách nhau dưới 0,01: chọn cấu hình bật ít thành phần hơn.
   50. Khối, X và Y ít ca: B 0,5000; B + X 0,4872; B + Y 0,4872; B + X + Y 0,5385. Đáp án: chọn B + X + Y.
5. Có bảng bao phủ DT18/cô/MRP, nêu phần chưa bao phủ, nơi nhận và quyết định phụ thuộc.
6. Không có câu "đã chọn" hay "giúp". Mọi dự đoán ghi "chưa kiểm".

Đạt các tiêu chí này chỉ xác nhận thiết kế đủ để thử, không xác nhận cơ chế.

## Không làm

- Cài thành phần hoặc chạy thử trên dev (giao task sau, D1).
- Phần nghiên cứu luật cảnh báo; nhánh G/H.
- L1 và mọi phần dùng LLM.
- Sửa baseline P3.
- Mở test.
- Ghi WHY chính thức.

## Chi phí ước lượng (chưa đo)

- **KS-16:** khoảng 30–60 phút laptop, RAM ≤ 3 GiB. Mốc tham chiếu: T-035 đọc cùng khối span mất 20–37 phút, RAM đỉnh 2,76 GiB.
- **Đầu ra** dưới 50 MB. Không tải trên 5 GB, không EC2, không subagent. Có thể đọc PDF/web của năm bài, dưới 50 MB.
- **Cho các task thử sau này:**
  - cổng chính xác mất khoảng 0,1–0,5 giây cho mỗi đơn vị có n ≤ 100, có cache theo nội dung;
  - lượt S_lo và S_hi chỉ chạy cho ca có ô OPEN;
  - tối đa 30 cửa sổ giả, chỉ RE2-TT;
  - khối K (B4): tối đa 26 cấu hình × 52 ca ≈ 1.352 lượt chấm; chưa gồm các bước khác, ba thế giới và FlashTicket; thời gian chưa đo.
- **Đợt phát triển FlashTicket:** chi phí OPEN, vì chưa có số ô, số lượt và thời lượng. Duyệt SPEC này không cấp quyền chạy chiến dịch.
- Không chạm ngưỡng của luật cứng 8.

## Rủi ro và điều chưa chắc

**Chưa kiểm:**
- Tỷ lệ span bọc trên mọi cặp. Mới đo quanh root: 99,95% ở RE2-TT, 100% ở Nezha-OB (`call-interval-001`, sau ghép nhãn).
- Tỷ lệ con chồng lấn.
- Nghĩa phía gọi trong RE2-TT (O03).
- Nửa đầu N của Nezha-OB trống vì thiếu thu hay vì không có sự kiện thật.
- Giả định A0.
- Đơn vị đếm coi thay đổi tải là bất thường (B1.3). Chưa có phép kiểm hành vi RCA trên dữ liệu có tải đổi mà hệ khỏe.

**Đề xuất chưa duyệt:**
- Các ngưỡng δ, δ_d là ngưỡng thực dụng (D2).
- Baseline Nezha-OB chưa chọn (D4).

**Thứ tự thử** có thể phụ thuộc đường đi. Cách xử lý: khối tổ hợp K và phép kiểm bối cảnh ở chuỗi cuối (B4). Không bảo đảm tối ưu toàn chuỗi.

## Prompt bàn giao

Prompt hiện hành nằm ở mục cuối của `LOG.md`.

---

## Phụ lục B — Đặc tả

### B1. Kiến trúc và hợp đồng dữ liệu

```
Đầu vào chuẩn hóa (span, metric, log, inventory U, alias, t)
 → A: ánh xạ, chuẩn hóa — E1, E2, E3, E3b, E4                (tầng 1)
 → B: tách tự sinh/kế thừa — E5 (+ phủ quyết E9, + E8 ở FT)   (tầng 2: phát hiện mức thành phần)
 → C: xếp hạng — E6a | E6b                                    (tầng 4)
 → D: vùng nghi ngờ — E7                                      (tầng 3)
 → E: gói bằng chứng (P8, giao diện)
```

**B1.1 Cửa sổ**
- N = [t−300, t), A = [t, t+300), cắt theo `cua_so.cat_*` (Q-64).
- Span thuộc A khi `end ≥ t`, tức chia theo thời điểm kết thúc, như MicroRank và TraceRCA ở P3. Phương án khác là chia theo start; lý do chọn ghi vào WHY.
- t ở chế độ (a) là mốc tiêm (Q-66). Ở chế độ (b), t là t̂ của báo động. Kết quả có ở t + 300 cộng thời gian tính.
- Nezha-OB: miền của adapter là [t−300, t+300). Metric có 5 điểm ở N và 5 điểm ở A, mỗi kênh giữ mốc thời gian thật.

**B1.2 Tiền xử lý span** (nhu cầu kỹ thuật, theo `Prepared` của P5)
- Khóa span là (traceID, spanID).
- Bỏ bản lặp y hệt và đếm số bản bỏ. Khóa trùng mà nội dung khác thì trả ERROR.
- Quan hệ cha–con dựng trên toàn miền được phép đọc ([t−300, t+300) ở chế độ (a)). Tính đặc trưng của từng span trên quan hệ đó, rồi mới chia mẫu theo thời điểm kết thúc (B1.1). Span mồ côi trong miền được đếm riêng.

**B1.3 Thống kê chung (E4)**

Áp cho mỗi đơn vị u: một thao tác, một cạnh hoặc một kênh metric.

*Định nghĩa:*
- **Hỗ trợ tối thiểu:** m_span = 20; m_metric = 5.
- **Ngưỡng nền:** q_hi = Q₀.₉₅(X_N), q_lo = Q₀.₀₅(X_N), nội suy tuyến tính (type 7).
- **Biên:** h = q_hi + ε·|q_hi|; l = q_lo − ε·|q_lo|; ε = 0,05.
- **Tỷ lệ vượt:** r_up(X) = #{x ∈ X : x > h} / |X|. r_dn(X) tính tương tự với l.

*Cổng kiểm định cho đơn vị phân vị.* Phép kiểm một phía, thống kê là tổng hạng trung bình của A. **Không dùng Monte Carlo.**

| Cỡ mẫu | Cách tính |
|---|---|
| n_N + n_A ≤ 100 | Chính xác có điều kiện, có xử lý giá trị trùng: quy hoạch động theo nhóm giá trị trùng (code ở B1.8). |
| n_N + n_A > 100 | `mannwhitneyu(method="asymptotic")`, có hiệu chỉnh trùng và hiệu chỉnh liên tục. |

- Không dùng `method="exact"` của SciPy, vì tùy chọn này không hiệu chỉnh giá trị trùng.
- Với nhánh xấp xỉ, đánh dấu "sát ngưỡng" khi |p − α| ≤ 0,002. Việc đánh dấu là tất định.
- α = 0,01.
- Kết quả cổng được cache theo khóa nội dung: (khóa đơn vị, mẫu N và A đã sắp, tham số E4). Khóa không phụ thuộc `config_id` hay cờ của thành phần phía sau. Nếu thành phần phía trước làm đổi mẫu thì coi là đơn vị khác.

*Hiệu ứng:*
- e_up = max(0, r_up(A) − r_up(N)) nếu qua cổng; ngược lại e_up = 0.
- e_dn tính tương tự.
- Cả hai nằm trong [0; 1].

*Trạng thái của đơn vị:* OK | LOW_SUPPORT | NO_BASELINE | NO_A.

*Đơn vị đếm (log, tần suất):*
- Dùng thời lượng quan sát T_N, T_A của thế giới đang tính (B1.3b).
- Kiểm nhị thức chính xác với p₀ = T_A / (T_N + T_A); tổng số sự kiện tối thiểu 10.
- Đặt λ = n_N · T_A / T_N. Khi đó e_up = max(0, (n_A − λ) / max(n_A, 1)) và e_dn = max(0, (λ − n_A) / max(λ, 1)).
- Thao tác mới NEW_OP: e_up = 1. Thao tác ngừng STOPPED: e_dn = 1.

*Giới hạn khi tải đổi:*
- Tải tăng mà hệ khỏe cũng làm đơn vị đếm báo tăng. Ví dụ 100 → 200 sự kiện trong hai khoảng quan sát bằng nhau: e_up = 0,5; p ≈ 4,0 × 10⁻⁹.
- Ứng viên (chưa kiểm): thêm kênh tỷ số (sự kiện chia số request của cùng thao tác), khai rõ mẫu số; giữ kênh đếm gốc và trạng thái không có request. Tỷ số có thể che lỗi khi request và sự kiện cùng giảm.
- Chỉ thử ở chặng phát triển chuyển giao (B1.9), với ba điều kiện: tải tăng mà hệ khỏe; lỗi khi tải giữ nguyên; cùng lỗi dưới tải khác.

*Hai khóa thực thể:*
- **K_raw(e)** = (max e, số kênh có e > 0, Σe), tính trên mọi kênh **trước** E5.
- **K_I(e)** cùng dạng, nhưng tính **sau** E5 và E9; kênh bị coi là kế thừa đặt bằng 0.
- Metric dùng chung chỉ gắn một lần. Hòa xét theo khóa chính xác.

*Giới hạn bão hòa:*
- Khi mọi mẫu A đều vượt ngưỡng, E4 không phân biệt được độ lớn. Ví dụ 30 → 45 và 30 → 60 cho cùng khóa. Khóa phụ chỉ phân biệt số kênh.
- Biến thể T4c thêm phần tử m = log(1 + |trung vị A − trung vị N| / max(|trung vị N|, r_u)), với r_u là bước giá trị nhỏ nhất khác 0 quan sát được. T4c chỉ là phép độ nhạy.
- Không tuyên bố đã hết hòa giả.

**B1.3b Khoảng quan sát theo nguồn**

*Bốn trạng thái* của mỗi ô 10 giây, xét theo từng nguồn (trace, log, metric):

| Trạng thái | Điều kiện | Xử lý |
|---|---|---|
| **XÁC NHẬN CÓ QUAN SÁT** | Có siêu dữ liệu thu thập phủ ô (chỉ số collector, manifest lượt chạy theo B16, trace lấy mẫu 100%), **và** nguồn bắt buộc phát bản ghi cho sự kiện được chấm. | Số 0 là số 0 thật. |
| **QUAN SÁT THEO GIẢ ĐỊNH A0** | Không có siêu dữ liệu, nhưng ô nằm trong bao thời gian có bản ghi của nguồn đó (mọi thực thể gộp lại), trong cửa sổ đang xét. | Dùng ở lượt chính. Kết luận ghi "dưới A0". |
| **XÁC NHẬN THIẾU THU** | Có bằng chứng phía thu thập: ô ngoài khoảng ghi của file; collector báo drop, refused hoặc failed > 0; hoặc manifest ghi gián đoạn. | Loại khỏi mẫu số. |
| **OPEN** | Các trường hợp còn lại. Bản ghi của dịch vụ khác và metric lưu lượng chỉ là bằng chứng hỗ trợ. | Xử lý theo ba thế giới bên dưới. |

*Giả định A0 — chưa kiểm:* "Trong khoảng có bản ghi của một nguồn, việc thu thập liên tục và đầy đủ cho mọi thực thể."
- A0 sai khi một số dịch vụ bị mất bản ghi cục bộ, hoặc lấy mẫu không đều.
- Trên dữ liệu công khai, A0 không kiểm được.
- FlashTicket cho phép thu thêm bằng chứng cho **từng khâu** của A0:
  - cấu hình lấy mẫu và exporter trong manifest lượt chạy (B16 mục 8);
  - chỉ số dropped, export failure, hàng đợi của collector và kho (B16, dòng 83 và 108);
  - request kiểm tra có trace biết trước đi xuyên các dịch vụ.
- Các bằng chứng này giúp kiểm từng khâu instrumentation, lấy mẫu, xuất dữ liệu, collector và kho. Chúng **không** bảo đảm xác minh đủ A0: instrumentation hoặc exporter của một dịch vụ có thể ngừng mà collector không báo (T-041 `bao-cao.md:244`; B16 dòng 103, 108).
- Có dùng A0 hay không: Minh quyết (D12).

*Ba thế giới quan sát.* Trạng thái OPEN gắn với cả nguồn trong một ô, không gắn với từng đơn vị. Vì vậy mỗi thế giới áp **cùng một cách gán** cho mọi ô OPEN của mọi nguồn, trong từng cửa sổ:

| Thế giới | Ô OPEN ở N | Ô OPEN ở A | Tỷ lệ r = T_A / T_N |
|---|---|---|---|
| **P (lượt chính)** | loại | loại | r_P = T_A^chắc / T_N^chắc |
| **S_lo** | quan sát, số 0 thật | thiếu thu | r_min = T_A^chắc / T_N^max |
| **S_hi** | thiếu thu | quan sát, số 0 thật | r_max = T_A^max / T_N^chắc |

- "Chắc" gồm XÁC NHẬN CÓ QUAN SÁT và QUAN SÁT THEO A0. Luôn có r_min ≤ r_P ≤ r_max.
- Ba thế giới trong bảng áp dụng khi các ô OPEN được thêm hoặc loại không chứa bản ghi được chấm và tập mẫu giữ nguyên giữa các thế giới. Không mặc nhiên coi điều kiện này đúng trên dev. Việc dùng A0 chờ D12; cách xử lý ô biên và ô OPEN có bản ghi phải được đặc tả trước khi áp dụng ba thế giới cho ca liên quan, kể cả trên dev. Phần này thuộc đầu ra thiết kế T-043.
- KS-16 (bước 4) đếm riêng ô biên và ô OPEN có bản ghi theo nguồn, không gán trạng thái cho chúng.
- **Tính đơn điệu (đơn vị đếm).** Khi số sự kiện cố định và r tăng:
  - e_up giảm, e_dn tăng;
  - p₀ = r / (1 + r) tăng, nên p của chiều tăng tăng và p của chiều giảm giảm.
  - Vì vậy nhãn đi theo một chiều tăng → bình thường → giảm, không quay lại, và có thể đổi hai lần (fixture 28). Nhãn ở S_lo và S_hi giống nhau thì nhãn không đổi trên cả đoạn [r_min, r_max].
- Khi các thế giới chỉ thay thời lượng quan sát và giữ nguyên tập mẫu, điểm của đơn vị phân vị không đổi.
- **Thứ tự.** Chỉ bất biến theo r giữa hai đơn vị đếm cùng nguồn, cùng ca, cùng nhãn, khi số sự kiện cố định:
  - nhãn tăng: e₁ − e₂ = r · (n_N2/n_A2 − n_N1/n_A1);
  - nhãn giảm, khi λ ≥ 1: e₁ − e₂ = (n_A2/n_N2 − n_A1/n_N1) / r.
- Thứ hạng có thể đổi khi: cổng đổi kết quả; so hai đơn vị đếm khác nhãn; so đơn vị đếm với đơn vị phân vị; so khác nguồn.
- Trong mỗi thế giới, nhãn và điểm được xác định đúng theo B1.3. Lượt chính dùng P. Ghi nhãn và điểm của cả ba thế giới.
- **OBS_DEPENDENT:** đơn vị có nhãn khác nhau giữa ba thế giới. Đây là nhãn chẩn đoán; đơn vị vẫn được chấm theo P.
- **RANK_CHANGED** (phương pháp xuất, không cần nhãn): thứ tự ứng viên đổi giữa ba thế giới. Phương pháp xuất thứ hạng ở cả ba thế giới.
- **WORLD_DEPENDENT** (bộ đánh giá tính, sau khi ghép nhãn): ca có thứ hạng root khác nhau giữa ba thế giới. Báo nguyên nhân: có cổng đổi kết quả hay chỉ điểm đổi, kèm cặp đơn vị làm đảo thứ tự. Phương pháp không tính cờ này.
- **Kết cục thành phần:** áp luật C trong cả ba thế giới; kết cục chính theo P. Nếu S_lo hoặc S_hi cho kết cục khác thì ghi "phụ thuộc quan sát, chưa phân xử" và xử lý như KHÔNG ĐỦ CA.
- S_lo và S_hi chỉ là độ nhạy, không chặn mọi trường hợp trung gian. Ví dụ "một phần ô OPEN được quan sát" hay "trace theo S_lo, log theo S_hi" không được chạy.
- Mọi kết luận ghi giả định: "dưới A0; ô OPEN bị loại ở cả hai phía; độ nhạy chỉ gồm S_lo và S_hi."

*Nezha-OB:*
- Không có metric lưu lượng ở front: `src/p3/nezha.py:60–66` chỉ giữ tỷ lệ thành công và độ trễ.
- `PodWorkload(Ops)` (`nezha.py:57`) chỉ là bằng chứng hỗ trợ ở độ phân giải phút; nghĩa khoảng đo của nó là OPEN.
- Nửa đầu N, tức [t−300, t−150), không có trace và log ở cả 22 ca: 22/22 file `F2.json.gz` khớp manifest `results/T-042/runs/normal-source-001/manifest.json`. Đoạn này nằm ngoài bao có bản ghi, nên là OPEN, trừ khi KS-16 đối chiếu khoảng ghi của file và cho kết luận khác.

**B1.4 Lớp tín hiệu** (chi phối E5)

| Kênh | Hướng chấm | Lớp |
|---|---|---|
| Thời gian độc quyền (E1); khoảng ngoài span (E2) | lên (E3 thêm hướng xuống) | không lan (tự sinh) |
| Tài nguyên tăng | lên | không lan |
| Tài nguyên giảm; tần suất giảm; thao tác ngừng; log thường giảm | xuống | lan xuôi: bên gọi → bên được gọi |
| Thời lượng cả span (chỉ C-a0); metric độ trễ; log lỗi; tỷ lệ thành công giảm; span lỗi (FT); tần suất tăng; thao tác mới | lên (riêng tỷ lệ thành công: xuống) | lan ngược: bên được gọi → bên gọi |

**B1.5 Năm câu về nguồn nền** (PLAN-P6 §3, cho bộ chấm mức thành phần)
1. **Nguồn nền:** N của chính ca. Ở Nezha-OB, trace và log có tối đa khoảng 150 giây quan sát.
2. **Dùng vào đâu:** học trên N; chọn trên dev 52 ca theo luật C; đánh giá ở P7. Số dev chỉ có giá trị mô tả.
3. **Thông tin có tại lúc quyết định:** tới t + 300. Không chọn cột hay chuẩn hóa trên toàn file.
4. **Khoảng chưa chấm được:** LOW_SUPPORT, NO_BASELINE, NO_DATA, ô OPEN và ô thiếu thu báo riêng. OBS_DEPENDENT và RANK_CHANGED là nhãn chẩn đoán của phương pháp; WORLD_DEPENDENT do bộ đánh giá tính.
5. **Ngưỡng:** α và ε khai trước; độ nhạy ở T4.

**B1.6 Ứng viên, tầng và trạng thái**
- Ứng viên là toàn bộ inventory U (WHY-26). Thực thể có ít nhất một kênh OK được xếp theo ba tầng:
  - **Tầng 1:** K_I,₁ > 0, sắp theo K_I.
  - **Tầng 2:** K_I,₁ = 0 và K_raw,₁ > 0, sắp theo K_raw.
  - **Tầng 3:** còn lại, một khối hòa.
- Thực thể UNOBSERVED không được trả về. Nếu root là UNOBSERVED thì RR = 0 (WHY-28).
- Thành phần thiếu đầu vào ghi UNSUPPORTED ở mức thành phần; chuỗi chạy với phần còn lại.
- Ca ERROR vẫn ở mẫu số.
- Báo bốn tập theo `danh_gia.bon_tap`.

**B1.7 Đầu ra và kết luận chẩn đoán**

Bản ghi mở rộng `ban_ghi.tao` (method = "M1", variant = config_id) với:
- `classes`: tự sinh / kế thừa / bình thường / thiếu dữ liệu;
- `inherited_by`;
- `region`;
- `evidence_refs`: khóa span, cột, ID mẫu log;
- `coverage`: trạng thái quan sát theo nguồn;
- `worlds`: nhãn và điểm ở P, S_lo, S_hi; thứ hạng ứng viên ở ba thế giới; cờ OBS_DEPENDENT, RANK_CHANGED (không cần nhãn);
- `verdict`.

**Phép chấm hợp lệ:** đơn vị có trạng thái OK, đủ hỗ trợ, đủ đầu vào, và đã tính xong phép chấm của cấu hình đang chạy, xét trong thế giới đang tính:
- cấu hình có E4: đã tính kiểm định (kể cả khi không qua cổng);
- cấu hình không có E4 (z vững, ở T4b hoặc khi luật C bỏ E4): đã tính được z hữu hạn.

| `verdict` | Điều kiện |
|---|---|
| `CAUSE_FOUND` | Tầng 1 không rỗng. |
| `NO_INTRINSIC_ANOMALY` | Tầng 1 rỗng và có ít nhất một phép chấm hợp lệ. |
| `INSUFFICIENT_EVIDENCE` | Không có phép chấm hợp lệ nào. |

- Thứ hạng vẫn được trả để tính MRR.
- Mỗi ca báo độ phủ chấm: tỷ lệ thực thể quan sát được có ít nhất một phép chấm hợp lệ.
- Cửa sổ chính báo số ca `INSUFFICIENT_EVIDENCE`; các ca này vẫn ở mẫu số MRR.

**B1.8 Code cổng chính xác** (đã chạy trong bộ nhớ ngày 24 và 25/10/2026, chưa nằm trong `src/`)

```python
import numpy as np
from math import comb
from scipy.stats import rankdata

def exact_tied_greater(A, N):
    """P(W_A >= w_obs) chính xác có điều kiện; W = tổng hạng trung bình của A; giá trị trùng xử lý theo nhóm."""
    A = np.asarray(A, float); N = np.asarray(N, float)
    x = np.r_[A, N]; nA = len(A)
    vals, counts = np.unique(x, return_counts=True)
    start = np.cumsum(np.r_[0, counts[:-1]])
    mid2 = (2 * start + counts + 1).astype(np.int64)        # 2 × hạng trung bình, là số nguyên
    Wmax = int((mid2 * counts).sum())
    dp = np.zeros((nA + 1, Wmax + 1)); dp[0, 0] = 1.0       # dp[k, w]: trọng số khi đã chọn k phần tử cho A
    for m, w in zip(counts, mid2):
        new = np.zeros_like(dp)
        for k in range(0, min(m, nA) + 1):
            c = float(comb(int(m), k))  # float trước khi nhân; số nguyên quá lớn làm mảng thành object
            if k == 0:
                new += dp * c
                continue
            new[k:, k * w:] += dp[:nA + 1 - k, :Wmax + 1 - k * w] * c
        dp = new
    wobs = int(round(2 * rankdata(x)[:nA].sum()))
    return dp[nA][wobs:].sum() / dp[nA].sum()
```

Kết quả đã chạy trong môi trường `py312-pin`:
- 13+7 / 20 → 0,004158004158 (2/481).
- 14+6 / 20 → 0,010098010098.
- 5+5 nền hằng → 0,003968 (1/252).
- 10+10 không trùng → 0,00259802, khớp `method="exact"`.
- A = N = 50 số 0 → 1. A = 40 số 0 + 10 số 1, N = 50 số 0 → 0,0005934196726 (= C(90,40)/C(100,50), so bằng `Fraction`).
- Thời gian: 0,07–0,45 giây với n = 100.
- Giới hạn: tổ hợp đổi sang float64 trước khi nhân; chỉ áp khi n ≤ 100. Bản trước có thể lỗi khi một hệ số tổ hợp thực sự được dùng vượt miền số nguyên NumPy (NumPy 1.26.4: `UFuncTypeError`). Nhóm trùng từ 68 phần tử có thể chạm trường hợp này nếu n_A đủ lớn; với nhóm 68 phần tử, lỗi từ n_A = 31.

**B1.9 Hợp đồng chấm và chuyển giao sang FlashTicket**

*Ba chặng* (lịch ở `docs/KE-HOACH-GIAI-DOAN-TOI.md` D.9, D.12):
1. **Lõi trên dữ liệu công khai:** thử và chọn trên dev 52 ca (B4); khóa bản dùng cho P7.
2. **Phát triển chuyển giao** trên OTel Demo và FlashTicket dev: phần dùng thông tin phong phú (kiểu span, DB/cache/pool, thông điệp, máy, nối log–span, siêu dữ liệu thu); hiệu chỉnh tham số theo tải; ứng viên LLM ở khâu giữa.
3. **Đánh giá** trên phần FlashTicket dành riêng, bằng các lượt mới sau khi khóa.
- Có hai bản được ghi rõ: bản P7 và bản FlashTicket. Kết quả P7 chỉ nói về bản P7.

*Hợp đồng đầu ra* (ghi vào `hop-dong.json`):
- Đầu ra chung là xếp hạng thực thể. Trên FlashTicket, tập ứng viên gồm các nút của mô hình T-037 (WHY-52: dịch vụ, gateway, DB logic, cache, broker, đối tác ngoài, máy), khai trước theo loại nút.
- Định vị cạnh là đầu ra tùy chọn, chỉ có khi có bằng chứng ở cạnh (E2, E8).
- Nút được coi là quan sát được khi có ít nhất một tín hiệu đã xác minh: span của chính nó; span CLIENT phía gọi có đích đã xác minh; metric hoặc log của nó. Nút chỉ thấy qua bên gọi được chấm theo bằng chứng của cạnh và gắn cờ riêng.

*Nhãn và chấm* (giao SPEC P10, khai trước chiến dịch):
- Nhãn có ba trường: vị trí tiêm; cơ chế; đáp án mà telemetry phân biệt được. Mỗi can thiệp (pool, DB, đường mạng) có số đo xác nhận độc lập. Thiếu quan sát thì ghi giới hạn; không đổi nhãn thật cho khớp với điều phương pháp trả được.
- Nhãn là cạnh a→b: khai trước cho mọi phương pháp tập đáp án chấp nhận theo cơ chế, cộng một bảng định vị cạnh riêng. Baseline không có đầu ra cạnh ghi UNSUPPORTED ở bảng đó.
- Báo riêng hai điểm: điểm xác định đúng nguyên nhân theo nhãn thật, và điểm định vị theo tập đáp án chấp nhận. Không gọi điểm thứ hai là xác định đúng nguyên nhân.
- Vùng ảnh hưởng: đo độc lập ở từng thành phần, hoặc đưa cả dự đoán lẫn nhãn về mức endpoint và gọi đúng là "ảnh hưởng endpoint".

*Bảng chuyển giao* (`bang-chuyen-giao.json`), mỗi thành phần một dòng:
- Cột: thông tin cần; phép dùng thông tin đó; nơi phát triển; điều kiện thất bại; trạng thái trên RE2-TT, Nezha-OB, OTel Demo, FlashTicket dev; tham số giữ nguyên; tham số hiệu chỉnh trên FlashTicket dev; nguồn dữ liệu nền; mốc khóa; phép kiểm chất lượng telemetry trước các lượt dùng để kết luận.
- Phép kiểm chất lượng telemetry nối với R-01–R-10 (`results/T-040/yeu-cau-quan-sat-p9.md`) và B16: định danh, DB/MQ/host, nối log–span, lấy mẫu, rớt dữ liệu, tài nguyên.
- Các dòng tối thiểu: kiểu span và cặp CLIENT–SERVER; DB/cache và pool; RabbitMQ, retry, fan-out; instance–host; log–span; thời điểm đến và siêu dữ liệu thu.

*LLM ở khâu giữa:* đánh giá ở chặng 2 (gom mẫu log; đề xuất cạnh tĩnh). So với Drain và quy tắc trên cùng dữ liệu; có nhánh bỏ LLM, cache, ngân sách riêng. Quyết giữ hay bỏ trước khi khóa bản FlashTicket. Trước khi dùng cần đoạn sửa MRP P8 theo hướng C-05 đã duyệt (chưa soạn). T-043 không cài LLM.

### B2. Đặc tả thành phần

**E1 — thời gian độc quyền**
- Nguồn: G2-H03, G2-H06; UV-2; CRISP. Dùng quan hệ cha–con trong trace.
- **E1-U:** cắt con về [s₀, s₁); u(s) = (s₁ − s₀) − |hợp các con|. Con vượt biên cha quá 1 ms chỉ được đếm để chẩn đoán.
- **E1-CP:** đi lùi từ s₁. Hai con c, d có quan hệ "trước–sau" theo CRISP §5.2 khi c_end − 1 ms < d_start và không con nào khác của cùng cha bắt đầu hay kết thúc trong khoảng chồng lấn. Thẻ đọc kiểm nguyên văn.
- Đơn vị chấm: thao tác (thực thể, tên), trừ span bọc.
- Dữ liệu: RE2-TT, Nezha-OB, FT.
- Điều kiện thất bại: bên được gọi không có span (S7); gọi bất đồng bộ; lỗi không làm tăng thời gian.
- Nhánh tắt: thời lượng cả span.

**E2 — khoảng ngoài span bên được gọi**
- Nguồn: UV-1, UV-5; G2-H06.
- **Span bọc w:** có đúng một con c ở thực thể khác, và cha của w cùng thực thể với w. Đặt g(w) = u(w).
- Mỗi cạnh a→b có mẫu g ở N và A, chấm theo E4, chỉ hướng lên.
- **E2-VC:**
  - Tìm mọi phủ đỉnh nhỏ nhất của tập cạnh bất thường S.
  - Đỉnh nằm trong mọi phủ nhỏ nhất là đỉnh "được định danh"; nhận bằng chứng của các cạnh nó phủ (lấy giá trị lớn nhất).
  - Cạnh còn lại gán cho bên được gọi, kèm cờ "không định danh".
  - "Định danh" chỉ có nghĩa trong giả định phủ bằng ít đỉnh nhất, chưa xác nhận nguyên nhân.
  - Nếu S có hơn 25 đỉnh: dùng E2-C cho mọi cạnh và đếm số lần.
- **E2-C:** gán mọi cạnh cho bên được gọi.
- Điều kiện thất bại: cạnh đơn lẻ do trễ chiều ra; cạnh thưa; không có span bọc.
- Nhánh tắt: chuỗi chưa có E2.

**E3 — log và tín hiệu hai chiều**
- Che token biến (số, hex ≥ 8, UUID, IP, chuỗi trong ngoặc).
- Drain (độ sâu 4, ngưỡng giống 0,4) học **chỉ trên phần N quan sát được** theo thế giới đang tính. Dòng A không khớp đi vào ô "mẫu mới" của thực thể.
- Xác định dòng lỗi:
  - Nếu có severity: lấy ERROR, FATAL, CRITICAL. Nezha-OB có severity trong JSON lồng (1.426.748/1.539.335 dòng, theo T-042).
  - RE2-TT không có severity: dùng bộ từ khóa cố định của SimpleRCA (T-017).
- Thời gian độc quyền chấm thêm hướng xuống; tỷ lệ thành công chấm hướng xuống.
- Điều kiện thất bại: số dòng log không bằng số request; lỗi lan lên bên gọi (cần E5).

**E3b — cấu trúc trace**
- Tần suất theo thao tác, tính như B1.3 và B1.3b. Có NEW_OP và STOPPED.
- Tách "chưa từng quan sát" với "ngừng sau mốc".
- Điều kiện thất bại: thao tác mới xuất hiện ở bên gọi; tần suất giảm lan xuôi.
- Trên Nezha-OB, đơn vị tần suất nhiều khả năng OBS_DEPENDENT vì nửa đầu N là OPEN. Dự kiến kết cục "không đủ ca".

**E4 — chuẩn hóa chung:** như B1.3. Nhánh tắt: max z vững có dấu (IQR = 0 thì scale = 1, như sklearn).

**E5 — tách tự sinh/kế thừa**
- Dùng cạnh phụ thuộc quan sát trong N ∪ A, có hướng.
- **Lớp lan ngược** ở e là kế thừa khi có bên được gọi b có bất thường thô thuộc: lớp lan ngược, E1, E2, tài nguyên tăng hoặc thao tác mới. Áp bắc cầu theo bất thường thô.
- **Lớp lan xuôi** ở e là kế thừa khi có bên gọi có bất thường thô bất kỳ.
- Trong một SCC, chỉ được giải thích bởi thành viên có bất thường không lan, hoặc bởi bên được gọi ngoài SCC.
- Kênh kế thừa đặt bằng 0 trong K_I.
- Phản ví dụ: root ở bên gọi gửi lại nhiều lần làm bên được gọi quá tải; hai dịch vụ cùng máy; hai lỗi đồng thời.

**E6a / E6b — xếp hạng**
- **E6a:** theo ba tầng ở B1.6.
- **E6b:**
  - Tập nút: thực thể có K_raw,₁ > 0.
  - Trọng số s(e) = K_I,₁(e), dùng cho xác suất chuyển a→b (b là bên được gọi, tỷ lệ với s(b)), tự lặp (tỷ lệ với s(a)) và vector v (tỷ lệ với s).
  - Dòng có tổng 0 nhảy về v. Hệ số tắt dần 0,85; dung sai 1e−12; tối đa 1000 vòng.
  - Σs = 0: trả NO_POSITIVE_MASS và dùng thứ tự E6a.
  - Khóa hòa: (π làm tròn 12 chữ số có nghĩa, K_I, K_raw). Lưu cả π gốc. Làm tròn không bảo đảm giống hệt giữa các máy khi π sát ranh giới.
  - Nút kế thừa được giữ trong tập nút để lưu cấu trúc cho vùng và gói bằng chứng. Nút có K_I = 0 không nhận và không truyền điểm. Đây là lựa chọn có chủ ý: nút đã được E5 giải thích không chuyển khối lượng giữa hai ứng viên tự sinh. Biến thể truyền qua nút kế thừa chưa có câu hỏi nào cần, nên không đưa vào ma trận.
- Căn cứ của E6b là ví dụ của cô và MicroRCA (DT18), không phải sửa hạn chế P4.

**E7 — vùng nghi ngờ**
- R = {r*} ∪ {bên gọi có đường tới r* qua nút bất thường theo K_raw, mọi kênh bị coi là kế thừa} ∪ {bên được gọi lan xuôi từ r*}.
- Biến thể: thành phần liên thông vô hướng chứa r*.
- Báo: root có thuộc R không; |R|; |R| / |O|.

**E8 — cạnh dữ liệu, thông điệp, triển khai (chỉ FT)**
- Span CLIENT có `peer.entity` hoặc `db.entity` đã xác minh, nhưng không có span ở bên được gọi:
  - bằng chứng trên cạnh là toàn bộ d(w), gán theo luật E2;
  - không tách được lỗi DB với đường mạng tới DB hay chờ pool phía gọi. Phép phân biệt để OPEN, giao P10. Đối chứng ngược: kịch bản "cạn pool" và "thao tác chậm bên trong" ở D.9.
- Thông điệp: nối bằng span link đã xác minh. Metric hàng đợi gắn vào nút broker.
- Máy: tài nguyên bất thường ở nhiều dịch vụ cùng máy được giải thích bằng metric của máy.
- Dev: UNSUPPORTED.

**E9 — phủ quyết theo thứ tự thời gian (tùy chọn)**
- Không coi e là kế thừa nếu e khởi phát sớm hơn mọi b dùng để giải thích nó, quá 2 ô + τ.
- Tắt trên cạnh có E2 bất thường. Nezha-OB chỉ dùng trace.

**Đối chứng**

| Mã | Định nghĩa |
|---|---|
| C-a0 | Gán theo chủ span, thời lượng cả span; không E1, E2, E5, E6b, E7; dùng tín hiệu của chuỗi cuối. K_I = K_raw. |
| C-a1 | Chuỗi cuối bỏ mọi chỗ dùng cạnh dịch vụ (E2, E5, E6b, E7); giữ E1. |
| C-d1 | Quy tắc "sâu nhất" tự định nghĩa, dùng K_raw: ưu tiên nút không có bên được gọi bất thường, rồi xếp theo khóa. |
| C-d2 | Quy tắc "sớm nhất". |
| C-d3 | Quy tắc Traversal theo PetShop 2e96f93, chạy trên bằng chứng của ta, dùng K_raw (chi tiết dưới bảng). |
| C-c | RRF, k = 60, trên đúng ba baseline không dùng quan hệ khi chấm: BARO, SimpleRCA M4, TraceRCA bản RCAEval lọc giá trị hữu hạn (căn cứ: `results/T-041/bao-cao.md` §3.2; `docs/KE-HOACH-GIAI-DOAN-TOI.md:334`). Trong nhóm hòa dùng hạng trung bình. Danh sách bị ERROR đóng góp 0. Không gộp MicroRank, CIRCA, TORAI B. Gộp đủ sáu baseline là định nghĩa khác ("C-c6, có dùng quan hệ"), chỉ làm khi Minh quyết. |
| C-g | SimpleRCA cộng bước E6b (chi tiết dưới bảng). |
| C-e | Mốc giả t′ = t − 300, chỉ RE2-TT, cần dữ liệu từ t − 600. "Bị báo" nghĩa là `verdict = CAUSE_FOUND`. Mẫu số: các cặp cửa sổ giả mà cả cấu hình bật lẫn tắt đều khác `INSUFFICIENT_EVIDENCE`; số cặp bị loại báo riêng. Mẫu số bằng 0: vế C-e của HẠI ghi "chưa kiểm được" và không áp; không coi là tỷ lệ bằng 0 hay đã qua vế này; kết luận của phép so ghi kèm giới hạn này (đề xuất thuộc D2, chờ Minh quyết). |
| C-f | Công cụ Grafana, chỉ trên FT. |

*C-d3 — chi tiết:*
- Đảo đồ thị gọi thành chiều nhân quả.
- Ứng viên: nút bất thường không có cha nhân quả bất thường.
- Chỉ giữ ứng viên có đường đơn tới đích, đi qua toàn nút bất thường. Điểm = tổng lớn nhất trên các đường đó.
- Chạy riêng từng đích, rồi gộp: điểm của ứng viên = lớn nhất qua các đích. Không loại nút đích khỏi tập ứng viên chung. Chỉ khi có đúng một đích thì đích đó mới không thể là root (hành vi gốc).
- Đồ thị con bất thường có chu trình: mã gốc báo lỗi. Quy ước của giao thức ta là UNSUPPORTED_CYCLIC, tính trượt.
- Đích ở chế độ (a): thực thể sở hữu span gốc của trace trong A và có bất thường lớp lan ngược. Ở chế độ (b): thực thể có chuỗi metric làm luật cảnh báo kích hoạt.
- Không có đích: NO_TARGET, tính trượt.
- Đây là quy tắc Traversal chạy trên bằng chứng của ta, không phải tái lập phương pháp PetShop.

*C-g — chi tiết:*
- s_g(e) = số phiếu SimpleRCA của e chia cho số phiếu lớn nhất. Lấy từ bản ghi P3 đã lưu: T-024 cho RE2-TT, T-026 cho Nezha-OB (M4).
- Tập nút: thực thể có s_g > 0. Xác suất chuyển, tự lặp và vector v đều theo s_g. Cạnh lấy từ đồ thị N ∪ A của chuỗi.
- Σs_g = 0: dùng thứ tự gốc của SimpleRCA. SimpleRCA không cho kết quả thì ghi NO_EVIDENCE.
- Giới hạn: C-g chỉ đo tác dụng của **bước E6b** đặt sau một bộ chấm mạnh. E5 không áp được, vì phiếu SimpleRCA không mang lớp kênh.

### B3. Cạnh làm phép tính gì

| Thành phần | Quan hệ | Phép tính | Nhánh cùng tín hiệu bỏ quan hệ | Nhánh đó còn giữ |
|---|---|---|---|---|
| E1 | cha–con trong trace | trừ hợp khoảng con | C-a0 | không |
| E2 | cạnh có hướng, span bọc | gán qua phủ đỉnh | C-a1 | cha–con (E1) |
| E5 | cạnh N ∪ A, hướng theo lớp | giải thích loại trừ | tắt E5 | E1, E2 |
| E6b | đồ thị con bất thường | PageRank cá nhân hóa | E6a | E1, E2, E5 |
| E7 | đường đi, tính liên thông | dựng vùng | top-k, không vùng | — |
| C-d1, C-d3 | cùng đồ thị | quy tắc độ sâu, đường đi | — | — |

So với C-a1 chỉ nói về cạnh dịch vụ. Muốn nói về toàn bộ quan hệ thì phải so với C-a0.

### B4. Ma trận thử trên dev

**Giữ cố định ở mọi bước:**
- 52 ca, chế độ (a); cửa sổ; U; tham số E4; bảng lớp; trạng thái quan sát.
- `danh_gia`: hòa tính theo kỳ vọng; ERROR tính là trượt.
- Độ đo chính MRR (MRP P6 tầng 4). Báo kèm Hit@1/3/5, NDCG@5, Retrieval@5, Rerank@1.

**Vai trò của phép so:**
- **Quyết định theo luật C:** T4b, T6, T9, T11, T12. Mỗi bước so "chuỗi đã xây tới bước trước, có X" với "cùng chuỗi đó, không có X".
- **Quyết định theo luật chọn khối** (dưới bảng): khối K, K-b và phép kiểm bối cảnh KB.
- **Chỉ báo cáo:** T13; C-d1 và C-d3 ở khối K; C-g và C-c ở T9.
- Chọn theo MRR riêng của từng cấu hình (MRP P6 tầng 4). Không chọn theo khoảng chênh so với đối chứng (QT4). Ghi lại mọi lần đã nhìn số.
- Số dev dùng để chọn và mô tả; không dùng làm bằng chứng hiệu quả trên dữ liệu chưa dùng để thiết kế. MRR dev của cấu hình được chọn lạc quan, vì được chọn trong nhiều cấu hình.
- Ca có ô OPEN chạy thêm S_lo và S_hi.

| Bước | Có X | Không X | Đo | Kết cục |
|---|---|---|---|---|
| T0 | KS-16, chỉ đọc | — | Cấu trúc, hỗ trợ, trạng thái quan sát, ô kích hoạt, kiểu O1–O4, hình dạng xếp hạng, số đơn vị theo chế độ cổng | Ô kích hoạt < 6 thì khai trước "không đủ ca" |
| T1 | Tầng bằng chứng gốc | — | Phân bố điểm, QT5, mốc giả RE2-TT, bất biến theo thứ tự hàng và hash seed 0/1/2 | Sai thì sửa cài đặt |
| T4 | ε ∈ {0; 0,05; 0,2}; α ∈ {0,001; 0,01; 0,05}; T4c | Chuỗi gốc | Độ nhạy | Chỉ báo cáo (QT3) |
| T4b | E4 | z vững không chặn | ΔRR; điểm không hữu hạn | Luật C và Q5, trên chuỗi gốc |
| K | Khối E1-U, E2-C, E3, E5: đủ 16 cấu hình | R0 (cả bốn tắt) | ΔRR; ca đúng bị hỏng so với ca được sửa; cờ M5; mốc giả theo `verdict` | Luật chọn khối; UV-6 cho E3; D.2 lượt 5 cho E5; C-d1, C-d3 chỉ báo cáo |
| K-b | E1-CP thay E1-U; E2-VC thay E2-C | Cấu hình thắng của K | ΔRR | Luật chọn khối, bước 9. E1-CP chỉ chạy khi tỷ lệ chồng lấn ≥ 5% |
| T6 | E3b | Chuỗi tới K-b | ΔRR | Luật C |
| T9 | E6b | E6a | ΔRR | Luật C; C-g, C-c chỉ báo cáo |
| T10 | E7, hai cách | — | Root có thuộc R; \|R\| | Mô tả |
| T11 | E9 | tắt E9 | ΔRR | Luật C |
| T12 | Cạnh tĩnh (T-038, T-039) | Cạnh quan sát | ΔRR | Luật C; ghi điều kiện revision |
| KB | Chuỗi cuối, đảo trạng thái từng thành phần của K và nhánh E4/z | Chuỗi cuối | ΔRR | Luật chọn khối, bước 11 |
| T13 | Chuỗi cuối, bỏ lần lượt từng thành phần; so với C-a0, C-a1, C-d1, C-d3, C-c, C-g, C-e | — | Bảng theo ca; khoảng tin cậy bootstrap theo ô của ΔMRR so với TORAI B | Chỉ báo cáo; E-04 phân xử ở P7 |

Thứ tự rẻ trước: T0 chỉ đọc. T1, T4, T4b và K dùng chung một lần trích đặc trưng, có cache. K-b, T6–T12 và KB là các phép trên cache. C-c gần như không tốn.

**Luật chọn khối** (khai trước; đề xuất thuộc D2):
1. **Nền cố định:** nhánh chấm (E4 hoặc z) theo kết cục T4b; E3b tắt; E6a; E9 tắt; cạnh quan sát; tham số và trạng thái quan sát như trên.
2. **Khối chính:** đủ 16 cấu hình, mỗi thành phần E1-U, E2-C, E3, E5 bật hoặc tắt. R0 là cấu hình tắt cả bốn. Một cặp là hai cấu hình chỉ khác trạng thái của một thành phần.
3. **Thành phần ít ca:** thành phần có dưới 6 ô kích hoạt, khai ở T0 trước mọi kết quả.
4. **Lượt một, loại vì hại.** Cấu hình c bị loại nếu c bị HẠI so với R0, hoặc nếu c có một thành phần x đang bật mà cặp (c bỏ x, c) cho HẠI theo luật C, kể cả điều kiện riêng UV-6, D.2 lượt 5 và mốc giả. Tập còn lại sau lượt một là **tập cố định**.
5. **Lượt hai, giữ thành phần ít ca** (M-48). Xét độc lập từng cấu hình c của tập cố định, không xóa dần. Với thành phần ít ca x đang tắt trong c: nếu c thêm x thuộc tập cố định và cặp (c, c thêm x) cho KHÔNG ĐỦ CA thì loại c.
6. **Cặp trái chiều theo dataset:** không loại cấu hình, chỉ gắn cờ. Trình Minh khi cờ nằm ở cấu hình thắng, hoặc ở cấu hình có MRR cao hơn cấu hình thắng. Các cặp còn lại không được coi là đã phân xử.
7. **Chọn:** tập gần tốt nhất gồm các cấu hình còn lại có MRR gộp không thấp hơn MRR cao nhất còn lại quá 0,01. Chọn cấu hình bật ít thành phần nhất; còn hòa thì chọn MRR cao hơn; vẫn hòa thì theo thứ tự E1, E2, E5, E3. Không còn cấu hình thì báo xung đột.
8. **Kiểm cấu hình thắng**, sau mọi bước trên:
   - không có E1, E2 hay E5 thì trình Minh, kèm cấu hình có đồ thị tốt nhất còn lại và mức chênh; không tự ép chọn cấu hình đồ thị kém hơn;
   - kết cục của từng thành phần tính bằng cách đảo trạng thái thành phần đó trong cùng bối cảnh; mâu thuẫn với lựa chọn thì báo xung đột, không tự thay cấu hình thắng.
9. **Biến thể (K-b):** hoán đổi riêng E1-CP và E2-VC tại cấu hình thắng và tại cấu hình đầy đủ, tối đa 4 cấu hình. Biến thể chỉ thay bản gốc khi luật C cho GIÚP tại cấu hình thắng; kết quả ở cấu hình đầy đủ chỉ báo kèm. Nếu cả hai đều GIÚP, chạy thêm đúng một cấu hình ghép rồi mới quyết; không ghép thành cấu hình chưa chạy.
10. **Ba thế giới:** chọn theo P. S_lo hoặc S_hi cho cấu hình thắng khác thì ghi "phụ thuộc quan sát" và trình Minh.
11. **Kiểm bối cảnh (KB),** sau T6, T9, T11, T12: đảo trạng thái từng thành phần của K (4 cấu hình) và đảo nhánh E4/z (1 cấu hình). Kết cục khác lúc chọn thì ghi "phụ thuộc bối cảnh" và trình Minh; không tự đổi. Phép này không bao tương tác của nhiều thành phần cùng lúc.
12. **Chi phí:** tối đa 26 cấu hình × 52 ca ≈ 1.352 lượt chấm, chỉ tính K, K-b và KB. Thời gian chưa đo.

### B5. Thử logic trong bộ nhớ (ngày 24/10/2026)

Đồ thị thử: F→A→R→X, F→B, và một nút I cô lập. **Đây là kiểm logic, không phải bằng chứng.** Thứ hạng chạy với công thức của bản 1; đáp án fixture sẽ tính lại theo B1.3 của bản này.

| Tình huống | C-a0 | + E1 | + E2 | + E2-VC | + E5 | + E3b + E5 |
|---|---|---|---|---|---|---|
| S1: R tự chậm | hòa F, A, R | R | R | R | R | R |
| S2: trễ mạng vào R | A, F | A | R | R | R | R |
| S2b: trễ cả vào và ra R | hòa | hòa A, R | hòa R, X | R | R | R |
| S3: lỗi trả nhanh | hòa | hòa | hòa | hòa | R | R |
| S5: nút cô lập | I | I | I | I | I | I |
| S6: chỉ có thao tác mới | hòa | hòa | hòa | hòa | hòa | R |
| S7: R không có span | A (sai) | A | A | A | A | A |

Hai phản ví dụ:
- Ở S3, C-d1 chọn X vì X mất lưu lượng.
- Ở S7, mọi biến thể đều đổ lỗi cho bên gọi.

### B6. Khóa trước G3 / để sau

**Khóa trước G3:**
- Code và revision.
- Mọi tham số: ε, α, m, δ, δ_d; bảng lớp; luật phủ đỉnh; luật SCC; hệ số tắt dần; chế độ tính cổng.
- Luật trạng thái quan sát, ba thế giới, A0.
- U và cách xử lý các trạng thái; khóa hòa.
- Luật vùng; điều kiện của `verdict`.
- Kết cục của từng thành phần; luật chọn khối và phép kiểm bối cảnh (B4).
- Hợp đồng đầu ra và luật "quan sát được" (B1.9).
- Độ đo chính; phép thống kê P7 (A4); cách đọc E-04.
- Danh sách so sánh (D4, D5); giao thức mốc giả; định dạng báo cáo theo ca.
- Nhãn lan (O09), nếu dùng.
- Cách ghi kết quả sau sửa (C-15 B).

**Để sau:**
- E8, C-f, P/R/F1 vùng → P10.
- Nhãn ba trường, luật chấm cạnh và vùng, chia đợt FlashTicket → SPEC P10 (B1.9; KE-HOACH D.9).
- L1, L5 → P8, chờ C-05.
- G/H → M-20.
- GNN → C15.
- KS-14 còn lại:
  - OTel messaging semconv → hạ tầng và E8;
  - Urbano, FDA → A4;
  - CNSS, GRLIA, DiLink → G/H;
  - TraceContrast, MicroDig, OpenRCA 2.0 → tham khảo.

---

## Phụ lục C — Luật kết cục và bảng ứng viên

**Ký hiệu:**
- ΔMRR_d: chênh MRR giữa bật và tắt X ở dataset d. ΔMRR gộp: chênh trên đủ 52 ca.
- δ = 0,01. δ_d = 1/n_d, tức 0,033 cho RE2-TT và 0,045 cho Nezha-OB. **Đây là ngưỡng thực dụng, không phải kiểm định.**
- E_X: các ô kích hoạt thành phần X (đếm ở T0).
- P, M: số ô trong E_X có RR tăng, giảm. P′, M′: số ô ngoài E_X có RR tăng, giảm.

**Áp theo thứ tự; dừng ở bước đầu tiên khớp:**
1. **HẠI → bỏ**, nếu có ít nhất một điều sau:
   - ΔMRR gộp < −δ;
   - M + M′ ≥ 3 và P + P′ = 0;
   - vi phạm điều kiện đã khai: UV-6; D.2 lượt 5; tỷ lệ `CAUSE_FOUND` ở mốc giả RE2-TT tăng quá 0,10 trên mẫu số C-e.
2. **TRÁI CHIỀU theo dataset → Minh quyết:** ΔMRR_d > +δ_d ở một dataset và ΔMRR_d′ < −δ_d′ ở dataset kia.
3. **KHÔNG ĐỦ CA → giữ, kiểm trên FlashTicket** (M-48): |E_X| < 6.
4. **GIÚP → giữ:** ΔMRR gộp > +δ, P > M, và không dataset nào có ΔMRR_d < −δ_d.
5. **KHÔNG TÁC DỤNG:** |ΔMRR gộp| ≤ δ. Đề xuất bỏ, trừ khi X là phần cuối cùng còn đáp ứng MRP P6 tầng 2 hoặc DT18.
6. **TRÁI CHIỀU theo ô → Minh quyết:** các trường hợp còn lại.

**Phụ thuộc quan sát:** áp luật trong cả ba thế giới (B1.3b). Nếu S_lo hoặc S_hi cho kết cục khác P thì ghi "phụ thuộc quan sát, chưa phân xử" và xử lý như KHÔNG ĐỦ CA.

**Báo kèm, không dùng để quyết định:** p của kiểm dấu chính xác trên các ô lệch; khoảng tin cậy bootstrap theo ô; kết cục ở δ = 0,005 và δ = 0,02. Sáu ô chỉ là cỡ nhỏ nhất để một kết quả toàn cùng chiều có thể đạt p < 0,05 (kiểm dấu 6/6 cho 0,03125).

**Ràng buộc với MRP:** E1, E2, E5 cùng bảo đảm đồ thị tham gia điểm bất thường. Nếu cả ba đều bị bỏ thì mâu thuẫn MRP P6 tầng 2: dừng và trình Minh. Với khối K, ràng buộc này kiểm trên cấu hình thắng (B4, luật chọn khối bước 8).

**Luật chọn khối:** với E1, E2, E3, E5, luật C áp cho từng cặp bật/tắt trong cùng bối cảnh, theo luật chọn khối ở B4. Không chọn tuần tự từng thành phần.

**Bảng ứng viên.** Số ô kích hoạt là xem trước, đếm sau khi ghép nhãn từ `results/T-032/runs/call-interval-001/summary.json` (sha256 fd65b51a…, ghim trong `chuoi-bang-chung.json`). Chưa phải KS-16.

| Ứng viên (nguồn) | Ô kích hoạt xem trước | Kết cục |
|---|---|---|
| E1-U (UV-2) | RE2-TT 8, Nezha-OB 11 | luật C |
| E1-CP (KS-10) | chờ KS-16 | Giúp: thay E1-U. Hại: giữ E1-U. Không đủ ca: thử ở FT |
| Dung sai đồng hồ (KS-10) | RE2-TT: 14,8% lời gọi lệch biên sau | luật C |
| E2-C, E2-VC (UV-1, UV-5) | Khoảng ngoài span tăng gấp 2: RE2-TT 2 ô, Nezha-OB 6 ô | luật C |
| E3 (UV-6) | Nezha-OB 4 | luật C và UV-6; dự kiến không đủ ca |
| E3b, ghi chú 6 (KS-10) | ít | luật C |
| E4 (UV-7) | mọi ô | luật C và Q5 |
| E5 (MRP tầng 2) | ô có cờ M5 | luật C và D.2 lượt 5 |
| E6b (KS-10) | ô có root nằm trên cạnh | Giúp: thay E6a. Còn lại: giữ E6a |
| E7 | — | mô tả (DT18 bắt buộc) |
| E8 | 0 | giữ, kiểm ở FT |
| E9 (KS-10) | chờ KS-16 | luật C |
| C-a0, C-a1, C-d1, C-d3, C-g (KS-11) | — | Cài được và không suy biến: báo kèm. Suy biến: bỏ, ghi lý do. Không chạy được: chuyển FT |
| C-h, PRISM (KS-11) | — | chỉ thêm nếu thẻ đọc cho được cách cài không cần nhãn |
| KS-14 thẻ đọc | — | Đổi công thức: sửa trước khi đóng băng. Bác giả định: bỏ hoặc sửa. Không đổi gì: giữ làm tham chiếu |
| KS-16 | — | Đủ ô: chạy thử. Thiếu ô: khai trước "không đủ ca". Không đếm được: UNSUPPORTED, kèm lý do |

---

## Phụ lục D — Các điều cần Minh quyết

| # | Điều cần quyết | Đề xuất của người làm |
|---|---|---|
| D1 | Mã T-043; Claude làm, Codex phản biện; phạm vi gồm thẻ đọc, KS-16 (T0), fixture; không cài phương pháp. Cài và thử chia ba task: (1) T1, T4, T4b và khối K; (2) K-b, T6, T9, T10, T11, T12 và KB; (3) T13 và hồ sơ G3. T0/KS-16 thuộc task thiết kế T-043 | Duyệt |
| D2 | Luật C (phần C): kết cục 5 và 6 nằm ngoài M-48; thứ tự ưu tiên; δ và δ_d; cách xử lý "phụ thuộc quan sát"; mẫu số C-e bằng 0. Luật chọn khối và kiểm bối cảnh (B4) | Duyệt |
| D3 | Tách nghiên cứu luật cảnh báo mức hệ thống (RQ3a) sang SPEC riêng; M1 chỉ khóa hợp đồng nhận t̂ | Duyệt tách |
| D4 | Baseline Nezha-OB. (a) Giữ bảng P3 đã khóa (T-026, Q-85); mục tiêu "cải thiện" so với MRR 0,538 của SimpleRCA (`results/T-026/cham-a.json#/tables/main/methods/simplerca/summary/main/mrr`); các nhánh T-042 báo như dòng chẩn đoán (lý do ở `results/T-042/runs/continuation-001/bao-cao-bo-sung.md:18`). (b) Thêm MAIN M0 | (a) |
| D5 | C-g định nghĩa như B2, kết luận chỉ về bước E6b; C-c dùng ba baseline không dùng quan hệ; có cần C-c6 không | Duyệt; không cần C-c6 |
| D6 | Nezha-OB không có mốc giả; giới hạn ghi vào kết luận | Duyệt |
| D7 | Hoãn L1 | Hoãn |
| D8 | Đưa T12 (cạnh tĩnh) vào dev, chạy cuối | Duyệt |
| D9 | Phép thống kê P7 (A4) quyết trước G3, không cần trước M1 | — |
| D10 | Đổi dòng Q-189 thứ hai (trùng mã) sang mã trống kế tiếp; sửa DECISIONS cần duyệt riêng | Duyệt |
| D11 | Dự đoán UV-1 bỏ vế (iii), vì M-25 đã bỏ đối chứng đồ thị ngẫu nhiên | Duyệt |
| D12 | Có dùng giả định A0 cho dữ liệu công khai không. Không dùng thì trên RE2-TT và Nezha-OB không ô nào được coi là có quan sát: đơn vị đếm (tần suất, log) không chấm được ở cả ba thế giới, và E3, E3b chỉ còn kiểm được trên FT. Đơn vị phân vị có bị ảnh hưởng hay không tùy cách xử lý bản ghi trong ô OPEN, chưa đặc tả (B1.3b) | Dùng, ghi rõ là giả định chưa kiểm |
