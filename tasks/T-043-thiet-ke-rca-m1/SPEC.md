# T-043 — M1: thiết kế chuỗi chẩn đoán RCA và giao thức thử trên dev

- **Trạng thái:** đề xuất, bản 3 (24/10/2026), sửa ngày 26/10/2026 theo Q-199, Q-201 và Q-202. 27/10/2026: sửa dòng kiểm nhãn theo Q-204. 28/10/2026: sửa theo Q-205 (D24: E4 cố định, T4b chỉ báo cáo; cờ F_raw/F_I; severity; MicroHECL; dấu vết E5; phụ thuộc quan sát; ô kích hoạt; trôi nền). **Chưa duyệt triển khai.**
  - Bản 3 gộp các sửa sau năm lượt phản biện của Codex trong chat (hai lượt với bản 1, ba lượt với bản 2) và các điểm người làm tự tìm. Minh duyệt sửa và tạo file theo Q-194, Q-195.
  - D1–D12 đã duyệt (Q-199); D13–D19 đã duyệt (Q-201). Nội dung từng mục ở Phụ lục D.
  - Lượt sửa cuối của bản 3 được Codex phản biện ngày 25/10/2026 (R14–R16). Sửa R14–R16 ghi theo Q-196, sau khi Codex kiểm lại đề xuất sửa; Codex chưa kiểm văn bản đã ghi.
  - Cùng ngày, sau các lượt R17–R24 và lượt kiểm luật chọn, ghi theo Q-197: luật chọn khối tổ hợp (B4), hợp đồng chấm và bảng chuyển giao (B1.9), sửa R20 (cờ cần nhãn chuyển sang bộ đánh giá), R21 (span qua mốc t), phép đếm log–span ở KS-16, giới hạn của đơn vị đếm khi tải đổi. Codex đã kiểm nội dung đề xuất, chưa kiểm văn bản đã ghi.
  - Ngày 26/10/2026: hai phiên chat song song (bảng D1–D12; phản biện chuyển giao FlashTicket) được gộp thành một gói sửa, ghi theo Q-201 sau ba lượt Codex kiểm gói. Codex kiểm văn bản đã ghi ở lượt B21 (LOG phiên 4).
  - Cùng ngày, sau hai lượt Codex (B21, B22) và hai lượt người làm đáp: Minh chọn sửa D13 và D20–D23, kèm làm rõ danh sách trả về của E6b và C-g; ghi theo Q-202. Codex chưa kiểm văn bản đã ghi.
  - Lịch sử bản nháp, phản biện và xử lý: `LOG.md` của task này.
- **Người làm:** Claude (DECISIONS Q-200; trước đây dẫn mã Q-189 bị trùng, xem D10). **Người phản biện:** Codex.
- **Thuộc gói MRP:** P6 (M1 trong `docs/PLAN-P6.md`). **Cổng:** chuẩn bị G3.
- **Mã task:** người làm đề xuất T-043, vì thư mục task trước đó kết thúc ở T-042. Minh quyết (D1).

## Mục tiêu

**Câu hỏi nguồn:**
- DT18-NV2: log, trace, metric được ánh xạ lên đồ thị phụ thuộc để xác định vùng ảnh hưởng, phát hiện dấu hiệu bất thường và xếp hạng nguyên nhân (`docs/reference/sources/DT18-de-tai-va-nhiem-vu.md` §2).
- Cô: bước 2 và bước 4 (`docs/reference/sources/advisor-2026-09-23.md` §1).
- MRP: RQ3b; RQ3c (vùng nghi ngờ); RQ3d; P6 tầng 1–4; cấu trúc tổng (M-32, M-48 trong `docs/KE-HOACH-GIAI-DOAN-TOI.md`).
- MRP RQ5 và DT18-NV3 (áp dụng trên hệ bán vé): B1.9 chỉ bao phủ hợp đồng và kế hoạch phép so (D14); đánh giá ở P10.

**Loại task:** thiết kế. Có thêm một phép đếm mô tả chỉ đọc (KS-16) và một đặc tả fixture có đáp án tính tay. Task không cài phương pháp và không chạy thử thành phần trên dev.

**Đạt task này** cho đủ căn cứ để mở các task cài đặt và thử. Nó chưa đủ để chọn thành phần, khóa G3 hay khẳng định lợi ích của đồ thị (MRP §3).

**Phần nguồn chưa bao phủ và nơi nhận:**
- RQ3a: phần nghiên cứu của luật cảnh báo cần một SPEC phát hiện riêng (D3).
- P/R/F1 của vùng: chỉ đo được trên FlashTicket (P10).
- P7 và P8.
- RCA tại thời điểm báo động t̂ trên dev (chế độ (b)): task đến sau SPEC phát hiện nhận (D3, D16).

## Câu hỏi, bằng chứng và quyết định

Mọi dự đoán dưới đây đều **chưa kiểm**. Luật kết cục ở phần C áp cho mọi dòng có so bật/tắt.

| # | Câu hỏi và nguồn | Lựa chọn cần phân xử; giải thích khác | Phép kiểm | Bác bỏ hoặc hỗ trợ khi | Thiếu gì, quyết định phụ thuộc |
|---|---|---|---|---|---|
| Q1 | Thời gian độc quyền có đưa root lên ở ca bên gọi chờ root không? G2-H03, H06; UV-2 | E1 bật/tắt. Giải thích khác: thiếu span con, gọi bất đồng bộ, lệch đồng hồ | Khối K (B4) | HẠI hoặc KHÔNG TÁC DỤNG theo luật C, tính tại cấu hình thắng của khối, thì bác bỏ | Bên được gọi không có span (S7) là điều kiện thất bại đã biết |
| Q2 | Đường găng (CP) có khác hợp khoảng (U) không? KS-10, CRISP | E1-CP so với E1-U | KS-16 đếm tỷ lệ con chồng lấn; K-b | Tỷ lệ < 5% ở cả hai dataset thì khai trước "không đủ ca" | Mặc định dùng E1-U |
| Q3 | Gán khoảng ngoài span bên được gọi cho bên được gọi có giúp không? UV-1, G2-H06 | E2 bật/tắt | Khối K | Luật chọn khối | Root không được gọi ở 8 ca (G2-H19) |
| Q4 | Phủ đỉnh có hơn gán thẳng cho bên được gọi không? UV-5 | E2-VC so với E2-C | K-b | Luật chọn khối, bước 9 | Cạnh đơn lẻ vẫn không định danh được |
| Q5 | Thống kê vượt ngưỡng nền có chặn điểm không hợp lệ mà không mất ca đúng không? UV-7, G2-H09/H12 | Điểm E4 (cố định, D24) so với điểm z trên đơn vị phân vị, cùng cờ | T4b, chỉ báo cáo: (1) kiểm đúng công thức; (2) ΔRR, ca được sửa và ca đúng bị hỏng của nhánh z | Vế (1): điểm từng kênh của E4 phải hữu hạn và thuộc [0; 1]; điểm z được dùng phải hữu hạn, không áp [0; 1]; không áp [0; 1] cho số kênh hay tổng điểm trong khóa thực thể. Sai thì sửa cài đặt. Ở ca có kênh mang nền IQR nhỏ, báo phân bố z để mô tả, không đặt ngưỡng. Vế (2): chỉ mô tả, không đổi nền | E4 cố định là lựa chọn thiết kế có đánh đổi (D24), không phải kết luận E4 xếp tốt hơn. Bão hòa (B1.3); trôi nền (G2-H10) |
| Q6 | Tín hiệu hai chiều và log theo mẫu có giúp lỗi return/exception mà không làm hỏng ca đúng không? UV-6, G2-H07 | E3 bật/tắt | Khối K | Luật chọn khối và UV-6 | Chỉ 4 ô Nezha-OB |
| Q7 | Tín hiệu cấu trúc trace (tần suất, thao tác mới, thao tác ngừng) có ích không? KS-10 | E3b bật/tắt | T6 | Luật C | Ít ca có thay đổi cấu trúc |
| Q8 | Tách tự sinh/kế thừa có giảm số ca bên gọi đứng trên root mà không hại không? MRP P6 tầng 2; G2-H17 | E5 bật/tắt. C-d1, C-d3 chỉ để báo cáo | Khối K | Luật chọn khối và điều kiện riêng của E5 (Phụ lục C) | "Lan có đáng kể" còn mở (O09) |
| Q9 | PageRank trên đồ thị con bất thường có hơn xếp thẳng theo điểm không? Ví dụ của cô | E6b so với E6a | T9 | Luật C | Căn cứ là DT18, không phải sửa hạn chế P4 |
| Q10 | Vùng nghi ngờ có chứa root không, rộng bao nhiêu? DT18 | Hai cách dựng vùng (E7) | T10 | Chỉ mô tả | Không có nhãn vùng trên dữ liệu công khai |
| Q11 | Thứ tự xuất hiện có phủ quyết được kế thừa sai không? KS-10 E9 | E9 bật/tắt | T11 | Luật C | Nezha-OB chỉ dùng được trace |
| Q12 | Dùng quan hệ có đổi chất lượng so với cùng tín hiệu bỏ quan hệ và so với quy tắc đơn giản không? RQ3d | Chuỗi cuối so với C-a0, C-a1, C-d1, C-d3, C-c, C-g | T13, **chỉ báo cáo** | Trên dev chỉ là mô tả; P7 mới khẳng định | Không có đồ thị ngẫu nhiên (M-25). Phạm vi kết luận theo B3 (D23) |
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
| `results/T-042/runs/continuation-001/` (số severity ở E3) | `manifest.json` của chính lượt đó |

**Trạng thái T-042:** đã đóng (Q-193). Giới hạn được chấp nhận và vẫn OPEN (Q-192). Chưa chọn baseline.

**Code và môi trường:**
- `src/p3/` (cua_so, ban_ghi, danh_gia, nezha, selector); `src/do_thi/builder.py`.
- Môi trường `D:/RCA-ext/envs/py312-pin/Scripts/python.exe` (WHY-15; SciPy 1.14.1, NetworkX 2.5).

**Nguồn ngoài:**
- PetShop: `code/baseline_anomaly_traversal.py` và `code/requirements.txt` tại commit 2e96f937c4c044b8b4aad03217592cd52e66db5d (requirements ghim NetworkX 2.8.8).
- CRISP, USENIX ATC 2022, §5.1–5.2.
- MicroHECL, arXiv 2103.01782, §IV.A (hướng lan, chuỗi lan), §IV.B (phát hiện theo cạnh), §IV.C (tỉa bằng tương quan).
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
6. `the-doc/`: thẻ đọc sáu bài.
7. `why-de-xuat.md`: WHY đề xuất. Minh duyệt rồi mới chép vào `docs/WHY.md`.
8. `bao-cao.md`: bảng bao phủ nguồn, phần còn mở, dự toán cho task sau, giao diện cho P8/P9; trạng thái ba cách ứng viên của MRP P6 tầng 2 (phân rã theo cây lời gọi, hồi quy có điều kiện kiểu CIRCA, GNN kiểu GDN): chọn, hoãn hay không chọn, kèm lý do.
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
1. **Thẻ đọc sáu bài.** Mỗi thẻ ghi: cơ chế, đầu vào, phần ta có/thiếu, điều kiện thất bại, chỗ đổi trong B2 (kèm trang hoặc dòng code).
   - PetShop → C-d3: đủ ba hàm.
   - CRISP §5.1–5.2 → E1-CP: luật happensBefore, cắt biên, cây con.
   - TraceDiag → E1, E5, E7.
   - PRISM → C-h.
   - DiagMLP → C-a.
   - MicroHECL §IV.A (hướng lan, chuỗi lan), §IV.B (phát hiện theo cạnh), §IV.C (tỉa bằng tương quan) → B1.4, E2, E5, E7. Thẻ tách ba phần: cơ chế gốc; phần có thể chuyển sang M1; phần M1 tự đề xuất. Nếu đề xuất dùng tương quan cho E5, `why-de-xuat.md` ghi: chuỗi được so, cách căn thời gian, số mẫu tối thiểu, xử lý chuỗi hằng và thiếu dữ liệu, điều kiện thất bại. E5 có tương quan là ứng viên; không đưa vào `ma-tran-thu.json` khi chưa có hợp đồng khả thi, fixture phân xử và lời duyệt của Minh.
   - Các bài khác của KS-14 giao về nơi dùng (B6).
2. **Hoàn thiện đặc tả v1** từ B1–B3. Kiểm: mỗi thành phần đủ 10 trường; không trường nào nhận nhãn. Định nghĩa ô kích hoạt của từng ứng viên viết ở bước này; ghi hash vào LOG trước pha 2 của KS-16; không sửa sau khi thấy số ô.
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
     - số ô kích hoạt của từng ứng viên, theo định nghĩa đã băm ở bước 2;
     - kiểu quan sát O1–O4 của root;
     - hình dạng xếp hạng của baseline.
   - Kiểm: so các số đếm chung với T-035 và T-032.
5. **Đóng băng `ma-tran-thu.json`.** Ghi hash vào LOG trước bước 6.
6. **WHY đề xuất, bảng bao phủ, giao diện P8/P9, dự toán** cho task sau, dựa trên thời gian đo ở bước 4.
7. **Báo cáo, LOG, STATE**, kèm prompt cho Codex soát kết quả.

Phụ thuộc: bước 1 trước bước 2. Bước 3 và pha 1 của bước 4 làm song song được; pha 2 của bước 4 chạy sau bước 2. Bước 5 cần bước 2–4.

## Kiểm đúng đắn

- **Không nhãn trong phương pháp.** API chỉ nhận spans, metrics, logs, inventory, aliases, t, params. KS-16 tách hai pha.
  - Bản ghi M1 qua bộ kiểm trường cấm duyệt đệ quy qua đối tượng, danh sách và tuple. `ban_ghi.kiem` hiện hành không duyệt danh sách và tuple (phản biện Codex 27/10/2026), nên không dùng làm bằng chứng. Yêu cầu, tên cấm và phản ví dụ ghi ở `hop-dong.json`, `fixture-dac-ta.json`. Cài trong task cài đặt (1); không sửa `src/p3`, vì hash `ban_ghi.py` đã ghim ở manifest T-041, T-031 và T-029.
  - Bộ lọc tên trường không chứng minh đặc trưng không suy từ nhãn; vẫn lần đường truyền đầu vào.
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
4. Fixture có đủ 82 ca dưới đây, kèm đáp án:
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
   31. Mọi kênh LOW_SUPPORT: `INSUFFICIENT_EVIDENCE`. E7 trả vùng rỗng ở cả hai cách dựng (D19).
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
   42. Một kênh metric N = A = 5 số 0: p = 1, F_raw = 0, `NO_INTRINSIC_ANOMALY`, ở cả điểm E4 và nhánh z báo cáo. E7 trả vùng rỗng ở cả hai cách dựng (D19).
   43. Mẫu số C-e bằng 0: vế C-e của HẠI ghi "chưa kiểm được" và không áp.
   44. Span qua mốc: cha [99,8; 100,2], con [99,85; 99,95], t = 100. Đáp án: quan hệ dựng trên toàn miền; self-time của cha 0,3 và cha thuộc A; con thuộc N.
   45. Khối, phản ví dụ R17 (hai ca, đồ thị F→R→X): MRR của gốc, E1, E5, E1 + E5 là 0,750; 0,500; 0,417; 1,000. Đáp án: chọn E1 + E5.
   46. Khối, R22: R0 0,5000; B 0,7500; B + X 0,7115; X ít ca. Đáp án: chọn B; X tắt vì cặp B / B + X cho HẠI.
   47. Khối, R23: R0 0,750000; cấu hình có đồ thị 0,746795. Đáp án: chọn R0, trình Minh vì cấu hình thắng không có E1, E2, E5.
   48. Kiểm bối cảnh, R24: X tắt khi chọn; ở chuỗi cuối, bật X tăng MRR. Đáp án: phép đảo trạng thái báo "phụ thuộc bối cảnh".
   49. Khối, hai cấu hình cách nhau dưới 0,01: chọn cấu hình bật ít thành phần hơn.
   50. Khối, X và Y ít ca: B 0,5000; B + X 0,4872; B + Y 0,4872; B + X + Y 0,5385. Đáp án: chọn B + X + Y.
   51. Luật C, X không thuộc E3 hay E5: RE2-TT ba ca hạng 2 → 1 (ΔMRR_d = +0,05); Nezha-OB năm ca hạng 1 → 2 (−0,1136); gộp −0,01923; P + P′ = 3; mốc giả không đổi. Đáp án: các vế HẠI riêng không kích hoạt; TRÁI CHIỀU theo dataset (bước 2).
   52. E5, số ca có cờ M5 không đổi; không ca nào đổi hạng; |E_X| = 8. Đáp án: không HẠI theo điều kiện riêng của E5; xét tiếp luật C; KHÔNG TÁC DỤNG.
   53. E5 làm tăng một ca có cờ M5: HẠI theo điều kiện riêng của E5.
   54. Mốc giả có 9 cặp hợp lệ; nhánh tắt 0/9, nhánh bật 1/9 có `CAUSE_FOUND`: tăng 0,111 > 0,10 → HẠI; báo n = 9.
   55. E3 tắt theo phương án A: một thực thể có 2 dòng log lỗi ở N, 30 dòng ở A, T_N = T_A = 300 giây. Đáp án: p = 1,2 × 10⁻⁷, e_up = 0,933. Không có ô "mẫu mới", không có "log thường giảm".
   56. Vế mốc giả ở trần: cặp có nhánh tắt 19/20 và nhánh bật 20/20: vế này không kích hoạt; ghi "không phân xử được" (D17); xét tiếp các vế khác. Cặp 2/10 → 5/10: tăng 0,30 → HẠI.
   57. Phản ví dụ E5: Payment có log lỗi e = 0,9 và tỷ lệ thành công e = 0,8 (lớp lan ngược); payment_db có CPU e = 0,05 (tài nguyên tăng); cạnh Payment → payment_db. Đáp án theo luật hiện hành: K_I(Payment) = (0, 0, 0); payment_db đứng đầu tầng 1; Payment đứng đầu tầng 2. Đây là điều kiện thất bại đã biết, không phải hành vi mong muốn.
   58. D19: cạnh quan sát B → A; cạnh tĩnh A → broker → B, broker không có tín hiệu; A có log lỗi 0,8, B có log lỗi 0,9 (lớp lan ngược). Đáp án: nhóm vòng xét trên đồ thị con bất thường {A, B}, không có vòng; K_I(B) = 0; A đứng đầu, như khi không có cạnh tĩnh. (Phương án không dùng, xét trên toàn đồ thị: {A, B, broker} là một nhóm vòng; B giữ 0,9 và đứng trước A.)
   59. D13: truy vấn kiểu điểm `rate(x[60s])`, không offset, to = 0, nên g = 60; t_p = 1000; t̂ = 1090. Đáp án: N chính [790, 1090); N′ [640, 940).
   60. Luật C: số ca có cờ M5 không đổi; RE2-TT bốn ca hạng 2 → 3 và một ca hạng 5 → 4; Nezha-OB không đổi; |E_X| = 8. ΔMRR gộp = −0,011859. Đáp án: không HẠI riêng (P + P′ = 1); không TRÁI CHIỀU; HẠI gộp (bước 3).
   61. D13: luật dùng recording rule, không đọc được cửa sổ gốc. Đáp án: biến thể UNSUPPORTED; giữ lượt chính; số ca bị ảnh hưởng tăng 1.
   62. D13, cách tính g: t_p = 1200; truy vấn kiểu khoảng, from = 600, to = 0, step = 60, u = 0, `rate(x[5m] offset 1m)`. Đáp án: e₀ = 600; g = 960 giây. Truy vấn kiểu điểm `rate(x[5m])`, không offset, to = 0: g = 300 giây.
   63. D13, subquery: truy vấn kiểu điểm, to = 0, `max_over_time(rate(x[5m])[10m:1m])`, t_p = 1800. Đáp án: g = 900; N′ [600, 900). Công thức trước Q-202 cho g = 600.
   64. D13, selector tức thời: truy vấn kiểu điểm, to = 0, `x > 10`, Δ = 300 đã xác minh, t_p = 1000. Đáp án: g = 300; N′ [400, 700). Cùng luật, Δ chưa xác minh: UNSUPPORTED.
   65. D13: truy vấn kiểu điểm `rate(x[300s])`, to = 60, t_p = 1000. Đáp án: e₀ = 940; g = 360; N′ [340, 640).
   66. D13: truy vấn kiểu khoảng `rate(x[300s])`, from = 600, to = 0, step = 60, u = 0, t_p = 1000. Đáp án: e₀ = 360; g = 940.
   67. D13: `rate(x[5m] @ 1000)`: UNSUPPORTED. Luật đọc Loki: UNSUPPORTED. Biến chưa giải được giá trị: UNSUPPORTED.
   68. C-g: không có cạnh; A có 1 phiếu; B có 0 phiếu, nằm trong nhóm điểm 0 mà SimpleRCA trả về; root B. Đáp án: danh sách C-g (A; B); RR = 1/2. Không thêm thực thể ngoài đầu ra SimpleRCA.
   69. E6b, không có cạnh: X có K_I,₁ > 0; Y có K_I,₁ = 0 và K_raw,₁ > 0; Z có K_raw,₁ = 0 và có kênh OK; root Z. Đáp án: Y thuộc tập PageRank, π(Y) = 0; Z ngoài tập, π(Z) = 0; danh sách (X; Y; Z); RR = 1/3.
   70. E7(c): ba ứng viên hòa đầu A, B, C; R_A = {A, B}, R_B = {A, B}, R_C = {C}; root A. Đáp án: p = 2/3; |R| kỳ vọng = 5/3; vùng hợp {A, B, C} chỉ là đầu ra phụ, |hợp| = 3.
   71. Cấu hình E1 tắt, E5 bật; cạnh A → R. Thời lượng cả span: A tăng e = 0,8; R tăng e = 0,6; không kênh nào khác. Đáp án: kênh của A thuộc lớp lan ngược và là kế thừa; K_I(A) = (0; 0; 0); R đứng đầu tầng 1; A đứng đầu tầng 2.
   72. Span w của A có đúng một con ở R; cha của w cũng thuộc A. Cấu hình E1 tắt: w là một mẫu thời lượng cả span của thao tác (A, tên của w). Cấu hình E1 bật: w không là mẫu của thao tác; u(w) chỉ vào mẫu g của cạnh A → R khi E2 bật.
   73. Cấu hình E1 tắt; thời lượng cả span của A giảm, e_dn = 0,6; không kênh nào khác. Đáp án: E3 bật thì kênh được chấm hướng xuống, lớp lan ngược, K_raw(A) = (0,6; 1; 0,6). E3 tắt thì không chấm hướng xuống, A không có kênh dương.
   74. Bộ kiểm trường cấm M1: worlds = [{"root": "A"}], worlds = {"P": [{"root": "A"}]}, evidence_refs = ({"label": 1},) bị từ chối; bản ghi hợp lệ được chấp nhận.
   75. Cờ và điểm: N = 28 số 0 + 2 số 100; A = 30 số 1. h = 57,75; p ≈ 9,65 × 10⁻¹³ (qua cổng); e_up = 0, nên F_raw = 0; ở nhánh z, F_raw = 0 nên max z = 1 không được dùng. Cờ lấy riêng theo p (cho F = 1) là cách bị loại.
   76. Nhánh z, ba phần. (a) Minh họa công thức thô, cố ý không chuyển đơn vị, không phải đáp án của chuỗi đã chuẩn hóa đơn vị: A có N = 20 số 30, A = 20 số 33 tính theo ms → z = 3; cùng dữ liệu tính theo µs → z = 3.000; B có N = 0, 1, 2, 3, 4 lặp bốn lần, A = 20 số 10 → z = 4; thứ tự A, B đảo. (b) Điểm E4: A và B cùng F_raw,lên = 1, p = 1/C(40,20) ≈ 7,25 × 10⁻¹², s = 1, hòa; không đổi theo đơn vị. (c) N = {0,…,19} × 10⁻¹⁶, A = 10⁻¹⁴ + {0,…,19} × 10⁻¹⁶: IQR ≈ 9,5 × 10⁻¹⁶ < 10·ε_mach nên c = 1, z ≈ 1,095 × 10⁻¹⁴.
   77. Severity: `error`, `ERROR`, ` Error `, `warning`, `""`, `"   "`, null, 5, `SEVERE` → lỗi, lỗi, lỗi, không lỗi, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN.
   78. N có 50 dòng severity xác định, 10 dòng lỗi; A có 100 dòng, toàn UNKNOWN: kênh severity NO_A, không chấm hướng nào. Khi E3 bật, 100 dòng vẫn đi vào Drain.
   79. T_N = T_A = 300. N: 100 dòng xác định, 10 lỗi. A: 100 dòng, 50 xác định, 10 lỗi. e = 0, p = 0,588. Độ phủ 1,0 và 0,5 ghi trong bản ghi; tên kênh "mật độ dòng lỗi có severity xác định".
   80. Dấu vết E5 trên dữ liệu fixture 57: `inherited_by` ghi Payment/log lỗi và Payment/tỷ lệ thành công, trạng thái "áp dụng", giải thích bởi payment_db/CPU tăng, qua cạnh Payment → payment_db, quy tắc lan ngược. Payment không còn kênh F_I; K_I(Payment) = (0; 0; 0). Bộ đánh giá, với root giả định là Payment: mất 2/2 kênh F_raw, không còn bằng chứng tự sinh, hạng 1 khi bỏ E5, hạng 2 khi bật.
   81. Trôi nền: N = 2000…2299, A = 2300…2599. Mọi phép nhân hoặc dời gốc áp cho cả N và A; ε = 0,05 trừ ca ghi ε = 0. p ≈ 5,27 × 10⁻¹⁰⁰ (xấp xỉ, hiệu chỉnh liên tục); e_up = 0,67; với ε = 0: 0,95; nhân 10: 0,67; trừ 2000: 0,9967; cộng 10.000: 0. Đây là điều kiện thất bại đã khai, không phải hành vi mong muốn.
   82. Một kênh đếm, n_N = n_A = 10, T_N = T_A: p = 0,588, điểm E4 = 0, phép chấm hợp lệ; ở cả điểm E4 và nhánh z báo cáo, kết luận NO_INTRINSIC_ANOMALY, không phải INSUFFICIENT_EVIDENCE.
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
- **Đầu ra** dưới 50 MB. Không tải trên 5 GB, không EC2, không subagent. Có thể đọc PDF/web của sáu bài, dưới 50 MB.
- **Cho các task thử sau này:**
  - cổng chính xác mất khoảng 0,1–0,5 giây cho mỗi đơn vị có n ≤ 100, có cache theo nội dung;
  - lượt S_lo và S_hi chỉ chạy cho ca có ô OPEN;
  - tối đa 30 cửa sổ giả, chỉ RE2-TT;
  - khối K (B4): tối đa 25 cấu hình × 52 ca = 1.300 lượt chấm; chưa gồm các bước khác, ba thế giới và FlashTicket; thời gian chưa đo.
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
- Cổng giả định các mẫu và sự kiện độc lập (B1.3).
- `CAUSE_FOUND` không xét số phép kiểm (B1.7).
- Tác động của D19 trên đồ thị hợp với cạnh quan sát của dev.
- Ngữ nghĩa thời gian của Grafana và Prometheus ở phiên bản sẽ dùng; cách căn bước của subquery; việc t_p trong lịch sử trạng thái là thời điểm đánh giá (D13).
- D13 cần manifest ghi phiên bản Grafana, Prometheus và Δ. Thiếu thì biến thể nền lùi là UNSUPPORTED.

**Đã duyệt nhưng vẫn là lựa chọn thực dụng:**
- Các ngưỡng δ, δ_d (D2f, Q-199) không phải kiểm định.
- Baseline Nezha-OB là cấu hình M4 (D4, Q-199); vượt M4 chỉ nói về bản M4 đó.

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
- **Hợp đồng nhận báo động (chế độ (b), D3):**
  - Bản ghi báo động gồm: t̂; tín hiệu và luật kích hoạt; dữ liệu đã có tới lúc chạy; cửa sổ N/A; cách gom sự cố; thời điểm trả kết quả.
  - Lượt chính: N = [t̂ − 300, t̂), A = [t̂, t̂ + 300).
  - Giới hạn: báo động trễ thì N có thể chứa phần đầu sự cố. Mọi kết luận ở chế độ (b) ghi giới hạn này.
  - Baseline chạy lại tại cùng t̂, cùng N và A.
- **Biến thể nền lùi (D13, sửa theo Q-202), chỉ báo cáo:**
  - t_p: lúc đầu tiên trạng thái rời Normal trong đợt báo động (vào Pending; hoặc vào thẳng Alerting khi thời gian chờ bằng 0), lấy từ lịch sử trạng thái Grafana. Bản Grafana tự cài phải bật lưu lịch sử trạng thái vào Loki. t_p phải là thời điểm đánh giá của luật, không phải lúc ghi lịch sử (chưa kiểm trên phiên bản sẽ dùng).
  - **Miền hỗ trợ:**
    - luật do Grafana quản lý, truy vấn nguồn Prometheus;
    - phiên bản Grafana và Prometheus lấy từ manifest lượt chạy (B16 mục 8); ngữ nghĩa thời gian đối chiếu với code ở đúng phiên bản đó;
    - biểu thức PromQL đã thay mọi biến (`$__interval`, `$__rate_interval`…) bằng giá trị của lần đánh giá; không dùng `@`; không phải recording rule;
    - khoảng nhìn lùi Δ của Prometheus (mặc định 300 giây) được xác minh từ cấu hình máy chủ trong manifest và không bị tham số truy vấn thay. Không mặc nhiên lấy 300 giây.
  - **Khoảng nhìn lùi L của biểu thức**, tính theo cây biểu thức:
    - selector khoảng `v[w] offset o`: o + w;
    - selector tức thời `v offset o`: o + Δ;
    - subquery `q[R:r] offset o`: o + R + L(q);
    - hàm, phép gộp, phép hai ngôi: L lớn nhất của các con; hằng: 0.
  - **Mốc đánh giá sớm nhất e₀** của mỗi truy vấn:
    - truy vấn kiểu điểm: e₀ = t_p − to (Grafana đánh giá tại mốc cuối của khoảng tương đối);
    - truy vấn kiểu khoảng: e₀ = ⌊(t_p − from + u) / step⌋ · step − u, với step đã giải và u là độ lệch múi giờ của truy vấn (Grafana làm tròn mốc đầu xuống theo bước).
  - g = lớn nhất, qua mọi truy vấn của luật, của (t_p − e₀) + L. Trong miền hỗ trợ, g là cận trên của khoảng dữ liệu mà lần đánh giá tại t_p đọc tới. Giả định chưa kiểm: ở phiên bản Prometheus sẽ dùng, subquery chỉ đánh giá tại các mốc không sớm hơn t − o − R.
  - N′ = [t_p − g − 300, t_p − g). Baseline chạy ở biến thể này dùng cùng N′.
  - UNSUPPORTED khi: luật hoặc biểu thức ngoài miền hỗ trợ (kể cả luật trên Loki và nguồn khác, chờ đặc tả riêng); không xác minh được Δ, phiên bản hoặc giá trị biến; thiếu lịch sử trạng thái; hoặc thiếu dữ liệu trước t_p − g − 300. Khi đó giữ lượt chính và báo số ca bị ảnh hưởng.
  - Không bảo đảm nền sạch: lỗi khởi phát từ từ có thể bắt đầu trước t_p − g.
- **RCA tại t̂ trên RE2-TT dev (D16):** chỉ báo cáo. t̂ lấy từ phát lại luật cảnh báo (SPEC phát hiện, D3). Task đến sau SPEC phát hiện nhận phép này. Hạn: trước mọi kết luận về RCA ở chế độ (b) và trước khi khóa bản FlashTicket. Ma trận B4 chỉ chạy chế độ (a), nên việc chọn cấu hình chưa xét điều kiện báo động thật.
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
- Tải tăng cũng có thể làm đơn vị phân vị báo tăng. Ví dụ giả: độ trễ 40 + 40 span, A tăng 25% so với N: p = 0,005, e_up = 0,05, qua cổng.

*Cờ, điểm và trạng thái* (áp cho mọi cấu hình):
- Trạng thái của đơn vị như trên.
- F_raw,d(u), cờ thô theo hướng d ∈ {lên, xuống}: bằng 1 khi u ở trạng thái OK, đủ hỗ trợ và thỏa toàn bộ điều kiện tạo e_d > 0 của E4 (đơn vị phân vị: qua cổng hướng d và chênh tỷ lệ vượt ngưỡng hướng d dương; đơn vị đếm: qua kiểm nhị thức hướng d và chênh dương; NEW_OP: F_raw,lên = 1; STOPPED: F_raw,xuống = 1). Chỉ tính cho hướng chấm của kênh (B1.4). E5 và E9 không đổi F_raw.
- F_I,d(u) = 1 khi F_raw,d(u) = 1 và kênh không bị coi là kế thừa sau E5. Kênh mà E9 phủ quyết việc giải thích giữ F_I = 1, với điểm gốc.
- Điểm s_d(u) chỉ dùng khi F_raw,d(u) = 1; ngược lại bằng 0. Điểm của chuỗi là e_d của E4 (D24).

*Hai khóa thực thể:*
- K_raw = (max s, số kênh, Σs) trên các kênh có F_raw = 1; K_I cùng dạng trên các kênh có F_I = 1; tập rỗng cho (0; 0; 0). "Bất thường thô" nghĩa là F_raw = 1. Với điểm E4, các định nghĩa này trùng định nghĩa cũ.
- Metric dùng chung chỉ gắn một lần. Hòa xét theo khóa chính xác.

*Giới hạn bão hòa:*
- Khi mọi mẫu A đều vượt ngưỡng, E4 không phân biệt được độ lớn. Ví dụ 30 → 45 và 30 → 60 cho cùng khóa. Khóa phụ chỉ phân biệt số kênh.
- Biến thể T4c thêm phần tử m = log(1 + |trung vị A − trung vị N| / max(|trung vị N|, r_u)), với r_u là bước giá trị nhỏ nhất khác 0 quan sát được. T4c chỉ là phép độ nhạy.
- Không tuyên bố đã hết hòa giả.

*Giả định của cổng — chưa kiểm:*
- Phép tổng hạng và phép nhị thức coi các mẫu, các sự kiện là độc lập. Tài liệu SciPy 1.14.1 của `mannwhitneyu` yêu cầu hai mẫu độc lập.
- Giả định sai khi chuỗi metric tự tương quan, hoặc khi một request ghi nhiều dòng log. Khi đó cổng qua thường hơn α.
- Mô phỏng AR(1), 300 + 300 điểm, không có lỗi, 2.000 lần lặp mỗi mức, `numpy.random.default_rng(0)`, `mannwhitneyu(method="asymptotic", use_continuity=True)` một phía: tỷ lệ qua cổng 1,1%; 7,3%; 28,8%; 38,6% ở hệ số 0; 0,5; 0,9; 0,98. Dữ liệu giả, chưa đo trên dev.
- Vì vậy α là ngưỡng thực dụng, không phải mức sai đã xác nhận. Mức nhiễu có thể khác nhau giữa RE2-TT (metric 1 giây), Nezha-OB (1 phút) và FlashTicket (nhịp scrape).
- T1 báo tỷ lệ qua cổng ở mốc giả RE2-TT, tách theo loại đơn vị và nguồn.
- Đơn vị đếm dòng log gọi đúng là "mật độ dòng log lỗi", không gọi là tỷ lệ request lỗi.

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
| Thời lượng cả span (nhánh E1 tắt, C-a0); metric độ trễ; log lỗi; tỷ lệ thành công giảm; span lỗi (FT); tần suất tăng; thao tác mới | lên (riêng tỷ lệ thành công: xuống; thời lượng cả span: E3 thêm hướng xuống) | lan ngược: bên được gọi → bên gọi |

*Ghi chú — chưa kiểm:*
- "Tần suất tăng" có hai cơ chế: retry (bên được gọi lỗi, bên gọi gửi lại; lan ngược như bảng) và tải vào (lan xuôi từ cổng). Dữ liệu công khai giữ tải gần đều nên không phân xử được. Bản P7 giữ bảng này; bản FlashTicket xét lại ở chặng phát triển (B1.9, dòng "tải vào").
- Bảng chỉ cho quan hệ gọi. Cạnh dữ liệu đồng bộ được coi như lời gọi. Cạnh thông điệp chưa có luật lan riêng; trên dev, tác động của nút không có tín hiệu theo D19.
- Thời lượng cả span (nhánh E1 tắt, D21) thuộc lớp lan ngược ở cả hai hướng. Bên được gọi chậm làm bên gọi chậm theo; bên được gọi lỗi trả nhanh làm bên gọi ngắn theo.

**B1.5 Năm câu về nguồn nền** (PLAN-P6 §3, cho bộ chấm mức thành phần)
1. **Nguồn nền:** N của chính ca. Ở Nezha-OB, trace và log chỉ phủ 41–97 giây ở N và 84–140 giây ở A.
2. **Dùng vào đâu:** học trên N; chọn trên dev 52 ca theo luật C; đánh giá ở P7. Số dev chỉ có giá trị mô tả.
3. **Thông tin có tại lúc quyết định:** tới t + 300. Không chọn cột hay chuẩn hóa trên toàn file.
4. **Khoảng chưa chấm được:** LOW_SUPPORT, NO_BASELINE, NO_DATA, ô OPEN và ô thiếu thu báo riêng. OBS_DEPENDENT và RANK_CHANGED là nhãn chẩn đoán của phương pháp; WORLD_DEPENDENT do bộ đánh giá tính.
5. **Ngưỡng:** α và ε khai trước; độ nhạy ở T4.

**B1.6 Ứng viên, tầng và trạng thái**
- Ứng viên là toàn bộ inventory U (WHY-26). Thực thể có ít nhất một kênh OK được xếp theo ba tầng:
  - **Tầng 1:** có ít nhất một kênh F_I = 1; sắp theo K_I.
  - **Tầng 2:** không có kênh F_I = 1 nhưng có kênh F_raw = 1; sắp theo K_raw.
  - **Tầng 3:** còn lại, một khối hòa.
- Thực thể UNOBSERVED không được trả về. Nếu root là UNOBSERVED thì RR = 0 (WHY-28).
- Thành phần thiếu đầu vào ghi UNSUPPORTED ở mức thành phần; chuỗi chạy với phần còn lại.
- Ca ERROR vẫn ở mẫu số.
- Báo bốn tập theo `danh_gia.bon_tap`.

**B1.7 Đầu ra và kết luận chẩn đoán**

Bản ghi mở rộng `ban_ghi.tao` (method = "M1", variant = config_id) với:
- `classes`: tự sinh / kế thừa / bình thường / thiếu dữ liệu;
- `inherited_by`: với mỗi kênh có đề xuất giải thích: thực thể, kênh, hướng, điểm trước E5; đơn vị dùng để giải thích (thực thể, kênh); cạnh hoặc đường; quy tắc (lan ngược, lan xuôi, nhóm vòng); trạng thái (đề xuất, áp dụng, bị E9 phủ quyết). Tên trường không trùng danh sách cấm.
- `region`: vùng R_r của từng ứng viên đứng đầu ở thế giới P, và vùng hợp (E7, D20);
- `evidence_refs`: khóa span, cột, ID mẫu log;
- `coverage`: trạng thái quan sát theo nguồn;
- `worlds`: nhãn và điểm ở P, S_lo, S_hi; thứ hạng ứng viên ở ba thế giới; cờ OBS_DEPENDENT, RANK_CHANGED (không cần nhãn);
- `verdict`.

**Phép chấm hợp lệ:** đơn vị có trạng thái OK, đủ hỗ trợ, đủ đầu vào, và đã tính xong phép chấm của cấu hình đang chạy, xét trong thế giới đang tính:
- Đã hoàn tất phép chấm theo quy tắc của loại đơn vị, gồm kiểm định của cờ khi quy tắc yêu cầu, kể cả khi không qua cổng. Ở nhánh z báo cáo, điều kiện z hữu hạn chỉ áp cho đơn vị phân vị được chấm bằng z; đơn vị đếm, NEW_OP và STOPPED giữ điều kiện hợp lệ của E4. Khi F_raw = 0, điểm bằng 0 (B1.3).

| `verdict` | Điều kiện |
|---|---|
| `CAUSE_FOUND` | Tầng 1 không rỗng. |
| `NO_INTRINSIC_ANOMALY` | Tầng 1 rỗng và có ít nhất một phép chấm hợp lệ. |
| `INSUFFICIENT_EVIDENCE` | Không có phép chấm hợp lệ nào. |

- Thứ hạng vẫn được trả để tính MRR.
- Mỗi ca báo độ phủ chấm: tỷ lệ thực thể quan sát được có ít nhất một phép chấm hợp lệ.
- Cửa sổ chính báo số ca `INSUFFICIENT_EVIDENCE`; các ca này vẫn ở mẫu số MRR.
- *Giới hạn — chưa kiểm:* `CAUSE_FOUND` chỉ cần một đơn vị ở tầng 1 và không xét số phép kiểm. Đơn vị lớp không lan không bao giờ được E5 giải thích. Vì vậy tỷ lệ `CAUSE_FOUND` khi hệ khỏe có thể cao và tăng theo số đơn vị. Báo tỷ lệ tuyệt đối ở mốc giả cho mọi cấu hình (D17). Kết luận sai của RCA tại mốc giả khác tỷ lệ báo động sai của cả chuỗi phát hiện–chẩn đoán; hai số báo riêng.

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

*Phép so trên FlashTicket (D14):*
- Bắt buộc ba bản: (1) bản P7 đã khóa, chạy thẳng trên phần thông tin thuộc hợp đồng chung; (2) bản FlashTicket đã khóa; (3) bản FlashTicket đã khóa, che từng nhóm thông tin phong phú.
- Tùy chọn (4): gói thông tin chung được tối ưu riêng trên FlashTicket dev. Gọi đúng là "gói tối ưu riêng"; không gọi là phép đo tác dụng của thông tin.
- Mọi bản dùng cùng ca và cùng cách chấm. Che cả đầu vào lẫn phần dẫn xuất trực tiếp từ nó. Thông tin bị che đi theo nhánh dự phòng khai trước; không điền số 0 giả; không bỏ ca.
- Báo cả chế độ (a) (runner đọc mốc tiêm từ sổ thực nghiệm, như thông tin vận hành biết trước) và chế độ (b).
- RQ5 báo riêng hai câu: bản P7 chuyển thẳng được tới đâu (bản 1); sau thích nghi đạt chất lượng nào (bản 2). Thiếu bản 1 thì không kết luận "bản công khai tự chuyển tốt".

*Thử thành phần trên FlashTicket (D15):*
- Mỗi lần thử ghi: bản nào; thay đổi gì; lý do kỹ thuật (prior work, khả năng quan sát của FlashTicket, hoặc cơ chế thất bại trên dữ liệu công khai nếu đã biết); kết cục trên dữ liệu công khai (GIÚP, HẠI, KHÔNG ĐỦ CA hoặc chưa thử); phép phân xử; ngân sách.
- Giữ nguyên kết luận của bản P7.
- Đổi cách đo (ví dụ E2 dùng cặp CLIENT–SERVER thay span bọc đoán) là thành phần mới, có dòng riêng trong bảng chuyển giao. Chạy cùng cách đo trên dữ liệu khác là thử lại thành phần cũ, báo kèm kết cục cũ.
- Mọi lần thử tính vào ngân sách phát triển FlashTicket.

*Hợp đồng đầu ra* (ghi vào `hop-dong.json`):
- Đầu ra chung là xếp hạng thực thể. Trên FlashTicket, tập ứng viên gồm các nút của mô hình T-037 (WHY-52: dịch vụ, gateway, DB logic, cache, broker, đối tác ngoài, máy), khai trước theo loại nút.
- Định vị cạnh là đầu ra tùy chọn, chỉ có khi có bằng chứng ở cạnh (E2, E8).
- Nút được coi là quan sát được khi có ít nhất một tín hiệu đã xác minh: span của chính nó; span CLIENT phía gọi có đích đã xác minh; metric hoặc log của nó. Nút chỉ thấy qua bên gọi được chấm theo bằng chứng của cạnh và gắn cờ riêng.

*Nhãn và chấm* (giao SPEC P10, khai trước chiến dịch):
- Nhãn có ba trường: vị trí tiêm; cơ chế; đáp án mà telemetry phân biệt được. Mỗi can thiệp (pool, DB, đường mạng) có số đo xác nhận độc lập. Thiếu quan sát thì ghi giới hạn; không đổi nhãn thật cho khớp với điều phương pháp trả được.
- Nhãn là cạnh a→b: khai trước cho mọi phương pháp tập đáp án chấp nhận theo cơ chế, cộng một bảng định vị cạnh riêng. Baseline không có đầu ra cạnh ghi UNSUPPORTED ở bảng đó.
- Báo riêng hai điểm: điểm xác định đúng nguyên nhân theo nhãn thật, và điểm định vị theo tập đáp án chấp nhận. Không gọi điểm thứ hai là xác định đúng nguyên nhân.
- Vùng ảnh hưởng: đo độc lập ở từng thành phần, hoặc đưa cả dự đoán lẫn nhãn về mức endpoint và gọi đúng là "ảnh hưởng endpoint".
- Trước khi nhóm hệ thống cài cờ lỗi: kiểm kê vị trí có ý nghĩa của từng họ lỗi, nhu cầu cài lỗi và thiếu hụt quan sát. Họ chỉ có một vị trí hợp lệ xử lý theo KE-HOACH D.9; không tạo vị trí giả để đủ hai phía.

*Bảng chuyển giao* (`bang-chuyen-giao.json`), mỗi thành phần một dòng:
- Cột: thông tin cần; phép dùng thông tin đó; nơi phát triển; điều kiện thất bại; trạng thái trên RE2-TT, Nezha-OB, OTel Demo, FlashTicket dev; tham số giữ nguyên; tham số hiệu chỉnh trên FlashTicket dev; nguồn dữ liệu nền; mốc khóa; phép kiểm chất lượng telemetry trước các lượt dùng để kết luận.
- Phép kiểm chất lượng telemetry nối với R-01–R-10 (`results/T-040/yeu-cau-quan-sat-p9.md`) và B16: định danh, DB/MQ/host, nối log–span, lấy mẫu, rớt dữ liệu, tài nguyên.
- Các dòng tối thiểu: kiểu span và cặp CLIENT–SERVER; DB/cache và pool; RabbitMQ, retry, fan-out; instance–host; log–span; thời điểm đến và siêu dữ liệu thu; tải vào (thông tin: tốc độ request ở cổng, số lời gọi theo cạnh; phép dùng ứng viên: so mức tăng của bên gọi và bên được gọi trên cùng cạnh; thất bại khi tải gây cạn tài nguyên thật); hướng lan theo loại cạnh (thông điệp, dữ liệu, máy, callback, scheduler).

*LLM ở khâu giữa:* đánh giá ở chặng 2 (gom mẫu log; đề xuất cạnh tĩnh). So với Drain và quy tắc trên cùng dữ liệu; có nhánh bỏ LLM, cache, ngân sách riêng. Quyết giữ hay bỏ trước khi khóa bản FlashTicket. Trước khi dùng cần đoạn sửa MRP P8 theo hướng C-05 đã duyệt (chưa soạn). T-043 không cài LLM.

### B2. Đặc tả thành phần

**E1 — thời gian độc quyền**
- Nguồn: G2-H03, G2-H06; UV-2; CRISP. Dùng quan hệ cha–con trong trace.
- **E1-U:** cắt con về [s₀, s₁); u(s) = (s₁ − s₀) − |hợp các con|. Con vượt biên cha quá 1 ms chỉ được đếm để chẩn đoán.
- **E1-CP:** đi lùi từ s₁. Hai con c, d có quan hệ "trước–sau" theo CRISP §5.2 khi c_end − 1 ms < d_start và không con nào khác của cùng cha bắt đầu hay kết thúc trong khoảng chồng lấn. Thẻ đọc kiểm nguyên văn.
- Đơn vị chấm: thao tác (thực thể, tên), trừ span bọc.
- Dữ liệu: RE2-TT, Nezha-OB, FT.
- Điều kiện thất bại: bên được gọi không có span (S7); gọi bất đồng bộ; lỗi không làm tăng thời gian.
- **Nhánh tắt (D21, Q-202):** thời lượng cả span. Không loại span bọc, như C-a0 (D18): mỗi span là một mẫu của thao tác thuộc chủ span. Kênh này thuộc lớp lan ngược (B1.4). Nhận ra span bọc cần quan hệ cha–con, nên nhánh tắt không dùng quan hệ ở mức thao tác.
  - Vì vậy E1 là một gói hai thay đổi: trừ thời gian con, và bỏ span bọc khỏi mẫu thao tác. Cặp bật/tắt E1 đo tác dụng của việc dùng quan hệ cha–con ở mức thao tác, không đo riêng phép trừ con. Phép so thay cùng lúc cách tính thời lượng và tập mẫu.
  - Quyết định giữ span bọc tác động cả 8/16 cấu hình có E1 tắt của khối K. Trong 4/16 cấu hình có E1 tắt và E2 bật, thời gian của span bọc có mặt ở cả mẫu thao tác của bên gọi và mẫu g(w) của cạnh (E2).

**E2 — khoảng ngoài span bên được gọi**
- Nguồn: UV-1, UV-5; G2-H06.
- **Span bọc w:** có đúng một con c ở thực thể khác, và cha của w cùng thực thể với w. Đặt g(w) = u(w).
- Mỗi cạnh a→b có mẫu g ở N và A, chấm theo E4, chỉ hướng lên.
- **E2-VC:**
  - Tìm mọi phủ đỉnh nhỏ nhất của tập cạnh có F_raw,lên = 1 (S).
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
  - Nếu có severity (Nezha-OB): lấy giá trị severity trong JSON lồng của message, theo hợp đồng nguồn T-042 `continuation-001`. Chuẩn hóa giá trị chuỗi: bỏ khoảng trắng hai đầu, đổi chữ hoa. Ánh xạ khai theo từng nguồn trong `hop-dong.json`; với Nezha-OB, {ERROR, FATAL, CRITICAL} là lỗi, {TRACE, DEBUG, INFO, WARN, WARNING} là không lỗi (giá trị quan sát trên dev: INFO, info, error, warning). Giá trị rỗng, sai kiểu, không đọc được hoặc ngoài ánh xạ: UNKNOWN. Chỉ giá trị thuộc ánh xạ mới tính vào độ phủ severity xác định. UNKNOWN không tính là lỗi, không tính là không lỗi, không đổi thành INFO.
    - Độ phủ trên dev: 1.426.748/1.539.335 lượt dòng có severity (`results/T-042/runs/continuation-001/contracts/histogram-001/full-summary.json#/counts/resolved_rows`, `#/counts/rows`); giá trị ở `#/values`. So khớp nguyên chữ `ERROR` cho 0 dòng lỗi.
    - Bản ghi lưu theo thực thể và cửa sổ N/A: số dòng, số dòng có severity xác định, số dòng lỗi, số UNKNOWN.
    - Kênh dựa trên severity chỉ đếm dòng lỗi xác định; gọi đúng là "mật độ dòng lỗi có severity xác định". Có log ở N nhưng không dòng nào xác định: NO_BASELINE; ở A: NO_A. Không đặt ngưỡng độ phủ. Độ phủ N và A khác nhau là hạn chế OPEN, báo kèm; chưa có căn cứ chọn cách hiệu chỉnh.
    - Dòng UNKNOWN vẫn đi vào các kênh không dựa trên severity, ví dụ mẫu Drain khi E3 bật.
  - RE2-TT không có severity: dùng bộ từ khóa cố định của SimpleRCA (T-017).
- Kênh thời lượng đang dùng chấm thêm hướng xuống: thời gian độc quyền khi E1 bật, thời lượng cả span khi E1 tắt (D21). Tỷ lệ thành công chấm hướng xuống.
- Điều kiện thất bại: số dòng log không bằng số request; lỗi lan lên bên gọi (cần E5).
- **Nhánh tắt (D2d, phương án A):** giữ một kênh log lỗi cơ bản. Mỗi thực thể có một đơn vị đếm: số dòng log lỗi trong N và A, chấm theo B1.3, chỉ hướng lên, thuộc lớp "log lỗi". Dòng lỗi xác định như trên: theo mức nghiêm trọng nếu có; RE2-TT dùng bộ từ khóa của SimpleRCA. Không che token, không chạy Drain, không có ô "mẫu mới", không có "log thường giảm", không thêm hướng xuống.
  - E3 bật bổ sung: đếm theo mẫu Drain và ô "mẫu mới"; "log thường giảm"; hướng xuống cho kênh thời lượng đang dùng (thời gian độc quyền hoặc thời lượng cả span) và tỷ lệ thành công.
  - Mặt trái: khối K không còn đo tác dụng của việc có log. Bật/tắt E3 chỉ đo cả gói thay đổi, không tách được phần Drain với phần tín hiệu hai chiều.
  - Phương án này phụ thuộc A0 (D12). Kênh này là mật độ dòng log lỗi (B1.3).
- **Nối log–span:** phép tính hiện hành đếm theo thực thể và thời gian. MRP P6 tầng 1 nói gắn log vào span qua trace_id nếu có. Dùng nối hay không quyết sau khi KS-16 đếm tỷ lệ nối và số ô (bước 4); lý do ghi vào `why-de-xuat.md`. Ứng viên khi dùng:
  - (a) tỷ lệ lần thực hiện thao tác có log lỗi: số span phân biệt có ít nhất một dòng lỗi chia số span của thao tác. Giữ tên này tới khi xác minh quan hệ span–request;
  - (b) E5 xét theo từng request trong cùng trace.

**E3b — cấu trúc trace**
- Tần suất theo thao tác, tính như B1.3 và B1.3b. Có NEW_OP và STOPPED.
- Tách "chưa từng quan sát" với "ngừng sau mốc".
- Điều kiện thất bại: thao tác mới xuất hiện ở bên gọi; tần suất giảm lan xuôi.
- Trên Nezha-OB, đơn vị tần suất nhiều khả năng OBS_DEPENDENT vì nửa đầu N là OPEN. Dự kiến kết cục "không đủ ca".

**E4 — chuẩn hóa chung:** như B1.3. Điểm E4 là điểm của chuỗi và nền khối K (D24).
- **Nhánh z (chỉ báo cáo, T4b):** cờ F_raw, F_I như B1.3. Chỉ đơn vị phân vị (thao tác, cạnh, kênh metric) đổi điểm: s_lên = max_{x∈A}(x − med_N)/c; s_xuống = max_{x∈A}(med_N − x)/c. Phép tính dùng float64; đặt ε_mach = np.finfo(np.float64).eps. c = IQR_N (nội suy tuyến tính) khi IQR_N ≥ 10·ε_mach; ngược lại c = 1. Quy tắc này trùng `RobustScaler` trong môi trường ghim (`sklearn/preprocessing/_data.py:111`), bộ chuẩn hóa của adapter BARO P3 (`src/p3/adapters/baro.py:23`); nhánh z chỉ dùng cùng quy tắc chuẩn hóa, không tái lập BARO. Không chặn giá trị lớn. Đơn vị đếm, NEW_OP, STOPPED giữ điểm E4.
- Phép biến đổi đầu vào của nhánh z (đơn vị cho từng loại tín hiệu) khai trong `hop-dong.json`, kèm lý do.
- Hạn chế của nhánh z: khi IQR_N trước và sau phép đổi đều ≥ 10·ε_mach và tính toán chính xác, z bất biến khi nhân toàn bộ mẫu của một kênh với cùng hệ số dương. IQR nhỏ khuếch đại thay đổi nhỏ (G2-H09). Khi c = 1, điểm phụ thuộc đơn vị biểu diễn. Điểm z có thể lớn hơn 1 và chi phối kênh đếm trong khóa max; ΔRR của nhánh z đo cả cách chấm đơn vị phân vị lẫn cách ghép hai thang.
- Điều kiện thất bại của E4: bão hòa (B1.3); trôi nền trong N tiếp diễn sang A cho điểm cao khi không có lỗi (G2-H10; fixture 81); biên ε·|q| phụ thuộc mức tuyệt đối của chuỗi.

**E5 — tách tự sinh/kế thừa**
- Dùng cạnh phụ thuộc quan sát trong N ∪ A, có hướng.
- **Lớp lan ngược** ở e là kế thừa khi có bên được gọi b có kênh F_raw = 1 thuộc: lớp lan ngược, E1, E2, tài nguyên tăng hoặc thao tác mới. Áp bắc cầu theo kênh F_raw = 1.
- **Lớp lan xuôi** ở e là kế thừa khi có bên gọi có kênh F_raw = 1 bất kỳ.
- Trong một SCC, chỉ được giải thích bởi thành viên có bất thường không lan, hoặc bởi bên được gọi ngoài SCC. SCC tính trên đồ thị con gồm các nút có kênh F_raw = 1 (D19).
- Kênh kế thừa đặt bằng 0 trong K_I.
- Phản ví dụ: root ở bên gọi gửi lại nhiều lần làm bên được gọi quá tải; hai dịch vụ cùng máy; hai lỗi đồng thời; bên được gọi có một bất thường thô yếu (có thể do cổng qua giả) vẫn xóa bằng chứng mạnh của bên gọi, và xác suất này tăng theo số đơn vị của bên được gọi (fixture 57); kênh tài nguyên trôi nền ở bên được gọi (G2-H10) có thể làm E5 xóa kênh lan ngược của bên gọi, khi có cạnh phù hợp, E5 bật và E9 không phủ quyết.
- Đơn vị lớp không lan không bao giờ được giải thích. Cải tiến (giải thích theo cùng họ tín hiệu, theo thứ tự thời gian E9, theo từng request) là ứng viên, cần căn cứ ngoài độ lớn điểm.

**E6a / E6b — xếp hạng**
- **E6a:** theo ba tầng ở B1.6.
- **E6b:**
  - Tập nút PageRank: thực thể có kênh F_raw = 1, gồm cả tầng 2 (không có kênh F_I = 1, nhận π = 0 theo thiết kế).
  - Danh sách trả về: mọi thực thể được xếp ở B1.6. Thực thể ngoài tập nút PageRank (tầng 3) nhận π = 0. Sắp toàn bộ theo khóa hòa dưới đây; thứ tự là các thực thể có π > 0, rồi tầng 2, rồi tầng 3.
  - Trọng số s(e) = K_I,₁(e), dùng cho xác suất chuyển a→b (b là bên được gọi, tỷ lệ với s(b)), tự lặp (tỷ lệ với s(a)) và vector v (tỷ lệ với s).
  - Dòng có tổng 0 nhảy về v. Hệ số tắt dần 0,85; dung sai 1e−12; tối đa 1000 vòng.
  - Σs = 0: trả NO_POSITIVE_MASS và dùng thứ tự E6a.
  - Khóa hòa: (π làm tròn 12 chữ số có nghĩa, K_I, K_raw). Lưu cả π gốc. Làm tròn không bảo đảm giống hệt giữa các máy khi π sát ranh giới.
  - Nút kế thừa được giữ trong tập nút để lưu cấu trúc cho vùng và gói bằng chứng. Nút có K_I = 0 không nhận và không truyền điểm. Đây là lựa chọn có chủ ý: nút đã được E5 giải thích không chuyển khối lượng giữa hai ứng viên tự sinh. Biến thể truyền qua nút kế thừa chưa có câu hỏi nào cần, nên không đưa vào ma trận.
- Căn cứ của E6b là ví dụ của cô và MicroRCA (DT18), không phải sửa hạn chế P4.

**E7 — vùng nghi ngờ**
- **Ứng viên đứng đầu (D20, Q-202):** T là nhóm hòa đứng đầu thứ hạng cuối của cấu hình đang chạy, ở thế giới P. Mỗi r ∈ T dựng một vùng R_r theo một trong hai cách dưới đây; r thay cho r*. Không chọn một r theo tên hay thứ tự duyệt. Chỉ báo vùng ở thế giới P.
- R = {r*} ∪ {bên gọi có đường tới r* qua nút bất thường theo K_raw, mọi kênh bị coi là kế thừa} ∪ {bên được gọi lan xuôi từ r*}.
- Biến thể: thành phần liên thông vô hướng chứa r*.
- Cả hai cách dựng tính trên đồ thị con gồm các nút có kênh F_raw = 1 (với điểm E4, tương đương K_raw,₁ > 0 của D19). Đồ thị đầy đủ vẫn được dựng và lưu trong bản ghi và gói bằng chứng.
- Đồ thị con rỗng thì R = ∅: báo root ∉ R, |R| = 0; trạng thái chẩn đoán và thứ hạng giữ nguyên.
- Báo theo trọng số từng ứng viên trong T. Đây là kỳ vọng theo quy tắc phá hòa đều, như cách chấm hòa của MRR; không phải xác suất phương pháp tin một thực thể là nguyên nhân.
  - p = Σ_{r∈T} 1[root ∈ R_r] / |T|;
  - |R| kỳ vọng = Σ_{r∈T} |R_r| / |T|; và |R| kỳ vọng / |O|.
  - Hai ứng viên sinh cùng một vùng vẫn tính hai lần; không gộp vùng trùng.
- Vùng hợp ∪_{r∈T} R_r chỉ là đầu ra phụ cho gói bằng chứng. Báo |hợp| riêng; không dùng |R| kỳ vọng để mô tả vùng hợp.
- Khi |T| = 1, các số trên trùng với cách báo một vùng.

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
| C-a0 | Gán theo chủ span, thời lượng cả span; không E1, E2, E5, E6b, E7; dùng tín hiệu của chuỗi cuối. K_I = K_raw. Không loại span bọc: mỗi span là một mẫu của thao tác thuộc chủ span, dùng thời lượng cả span, không phải một kênh riêng (D18). |
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
- Tập nút PageRank: thực thể có s_g > 0. Xác suất chuyển, tự lặp và vector v đều theo s_g. Cạnh lấy từ đồ thị N ∪ A của chuỗi.
- Danh sách trả về: đúng tập thực thể SimpleRCA đã trả trong bản ghi P3. Phần có s_g > 0 sắp theo khóa (π làm tròn 12 chữ số có nghĩa, s_g); khóa bằng nhau là hòa. Nhóm điểm 0 của SimpleRCA nối nguyên khối ở cuối, giữ là một nhóm hòa. Không thêm thực thể ngoài đầu ra gốc.
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

**Phạm vi kết luận (D23, Q-202).** C-a0 và C-a1 là phép bỏ thành phần khỏi chuỗi đã chọn. Lựa chọn tín hiệu E3, E3b giữ theo chuỗi cuối, và được chọn khi chuỗi có đồ thị. Điểm E4 cố định (D24); phép so với điểm z chỉ báo cáo trên R0. Các phép so này trả lời câu: bỏ quan hệ khỏi chuỗi đã chọn làm đổi chất lượng bao nhiêu (MRP RQ3d, nhánh cùng tín hiệu). Chúng không trả lời câu: phương pháp có quan hệ hơn phương pháp không quan hệ được chọn bằng cùng luật. Muốn trả lời câu sau thì phải khai nhánh chọn riêng trong `ma-tran-thu.json` trước khi đóng băng; Minh không chọn phương án này (MRP P7, đoạn giữ tương đương).

### B4. Ma trận thử trên dev

**Giữ cố định ở mọi bước:**
- 52 ca, chế độ (a); cửa sổ; U; tham số E4; bảng lớp; trạng thái quan sát.
- `danh_gia`: hòa tính theo kỳ vọng; ERROR tính là trượt.
- Độ đo chính MRR (MRP P6 tầng 4). Báo kèm Hit@1/3/5, NDCG@5, Retrieval@5, Rerank@1.
- **Chuỗi gốc (D22, Q-202):** R0 cộng nhánh chấm. R0 tắt cả E1, E2, E3, E5 như ở khối K; E3b tắt; E6a; E9 tắt. Cạnh quan sát được dựng nhưng không thành phần nào dùng. R0 không dùng quan hệ. T1, T4, T4b chạy trên R0 với điểm E4; phép so z ở T4b chỉ báo cáo (D24).

**Vai trò của phép so:**
- **Quyết định theo luật C:** T6, T9, T11, T12. Mỗi bước so "chuỗi đã xây tới bước trước, có X" với "cùng chuỗi đó, không có X".
- **Quyết định theo luật chọn khối** (dưới bảng): khối K, K-b và phép kiểm bối cảnh KB.
- **Chỉ báo cáo:** T4b; T13; C-d1 và C-d3 ở khối K; C-g và C-c ở T9.
- Chọn theo MRR riêng của từng cấu hình (MRP P6 tầng 4). Không chọn theo khoảng chênh so với đối chứng (QT4). Ghi lại mọi lần đã nhìn số.
- Số dev dùng để chọn và mô tả; không dùng làm bằng chứng hiệu quả trên dữ liệu chưa dùng để thiết kế. MRR dev của cấu hình được chọn lạc quan, vì được chọn trong nhiều cấu hình.
- Ca có ô OPEN chạy thêm S_lo và S_hi.

| Bước | Có X | Không X | Đo | Kết cục |
|---|---|---|---|---|
| T0 | KS-16, chỉ đọc | — | Cấu trúc, hỗ trợ, trạng thái quan sát, ô kích hoạt, kiểu O1–O4, hình dạng xếp hạng, số đơn vị theo chế độ cổng | Ô kích hoạt < 6 thì khai trước "không đủ ca" |
| T1 | Chuỗi gốc R0 với E4 (D22) | — | Phân bố điểm, QT5, mốc giả RE2-TT, bất biến theo thứ tự hàng và hash seed 0/1/2 | Sai thì sửa cài đặt |
| T4 | ε ∈ {0; 0,05; 0,2}; α ∈ {0,001; 0,01; 0,05}; T4c | Chuỗi gốc | Độ nhạy | Chỉ báo cáo (QT3) |
| T4b | Nhánh z (cùng cờ E4) | Chuỗi gốc R0 với E4 | Q5 vế (1), (2); dẫn kết quả T4c của T4, không chạy lại | Chỉ báo cáo. Không đổi nền khối K (D24); muốn đổi phải trình Minh như thay đổi thiết kế sau khi đã nhìn số dev |
| K | Khối E1-U, E2-C, E3, E5: đủ 16 cấu hình | R0 (cả bốn tắt) | ΔRR; ca đúng bị hỏng so với ca được sửa; cờ M5; mốc giả theo `verdict`; dấu vết E5 theo ca và kênh. Bộ đánh giá ghép nhãn sau: root mất kênh nào, còn bằng chứng tự sinh không, hạng trước/sau E5 (từ cặp c bỏ E5, c). Ở mốc giả: số kênh F_raw thuộc lớp lan bị coi là kế thừa trên tổng số kênh F_raw thuộc lớp lan. Các số tổng chỉ để mô tả, không xác nhận cơ chế | Luật chọn khối; UV-6 cho E3; điều kiện riêng của E5 (Phụ lục C); C-d1, C-d3 chỉ báo cáo |
| K-b | E1-CP thay E1-U; E2-VC thay E2-C | Cấu hình thắng của K | ΔRR | Luật chọn khối, bước 9. E1-CP chỉ chạy khi tỷ lệ chồng lấn ≥ 5% |
| T6 | E3b | Chuỗi tới K-b | ΔRR | Luật C |
| T9 | E6b | E6a | ΔRR | Luật C; C-g, C-c chỉ báo cáo |
| T10 | E7, hai cách | — | Root có thuộc R; \|R\| | Mô tả |
| T11 | E9 | tắt E9 | ΔRR | Luật C |
| T12 | Cạnh quan sát ∪ cạnh tĩnh (T-038 cho RE2-TT, T-039 cho Nezha-OB; phép hợp, D8) | Cạnh quan sát | ΔRR | Luật C; ghi điều kiện revision |
| KB | Chuỗi cuối, đảo trạng thái từng thành phần của K | Chuỗi cuối | ΔRR | Luật chọn khối, bước 11 |
| T13 | Chuỗi cuối, bỏ lần lượt từng thành phần; so với C-a0, C-a1, C-d1, C-d3, C-c, C-g, C-e | — | Bảng theo ca; khoảng tin cậy bootstrap theo ô của ΔMRR so với TORAI B | Chỉ báo cáo; E-04 phân xử ở P7; phạm vi kết luận theo B3 (D23) |

Thứ tự rẻ trước: T0 chỉ đọc. T1, T4, T4b và K dùng chung một lần trích đặc trưng, có cache. K-b, T6–T12 và KB là các phép trên cache. C-c gần như không tốn.

*T12 (D8):* cạnh thay đổi chỉ dùng ở E5, E6b, E7, C-d1, C-d3; E1 và E2 vẫn lấy từ span. Nút chỉ có trong mô hình tĩnh vẫn là UNOBSERVED. Cạnh trùng hướng gộp làm một. Nhóm vòng của E5 và vùng của E7 tính theo D19. Tác dụng thực tế vẫn OPEN.

*Mức tuyệt đối ở mốc giả (D17):* nếu đặt, Minh quyết sau T1 và trước T4b. Phép so đầu tiên dùng luật C là khối K. Ghi rõ mức được đặt sau khi xem dữ liệu dev T1.

**Luật chọn khối** (khai trước; đề xuất thuộc D2):
1. **Nền cố định:** điểm E4 (D24); E3b tắt; E6a; E9 tắt; cạnh quan sát; tham số và trạng thái quan sát như trên.
2. **Khối chính:** đủ 16 cấu hình, mỗi thành phần E1-U, E2-C, E3, E5 bật hoặc tắt. R0 là cấu hình tắt cả bốn. Một cặp là hai cấu hình chỉ khác trạng thái của một thành phần.
3. **Thành phần ít ca:** thành phần có dưới 6 ô kích hoạt, khai ở T0 trước mọi kết quả.
4. **Lượt một, loại vì hại.** Cấu hình c bị loại nếu c bị HẠI so với R0, hoặc nếu c có một thành phần x đang bật mà cặp (c bỏ x, c) cho HẠI theo luật C, kể cả điều kiện riêng UV-6, điều kiện riêng của E5 (Phụ lục C) và mốc giả. Tập còn lại sau lượt một là **tập cố định**.
5. **Lượt hai, giữ thành phần ít ca** (M-48). Xét độc lập từng cấu hình c của tập cố định, không xóa dần. Với thành phần ít ca x đang tắt trong c: nếu c thêm x thuộc tập cố định và cặp (c, c thêm x) cho KHÔNG ĐỦ CA thì loại c.
6. **Cặp trái chiều theo dataset:** không loại cấu hình, chỉ gắn cờ. Trình Minh khi cờ nằm ở cấu hình thắng, hoặc ở cấu hình có MRR cao hơn cấu hình thắng. Các cặp còn lại không được coi là đã phân xử.
7. **Chọn:** tập gần tốt nhất gồm các cấu hình còn lại có MRR gộp không thấp hơn MRR cao nhất còn lại quá 0,01. Chọn cấu hình bật ít thành phần nhất; còn hòa thì chọn MRR cao hơn; vẫn hòa thì theo thứ tự E1, E2, E5, E3. Không còn cấu hình thì báo xung đột. Báo MRR từng dataset của các cấu hình trong tập gần tốt nhất; không thêm bộ lọc theo dataset (D2e).
8. **Kiểm cấu hình thắng**, sau mọi bước trên:
   - không có E1, E2 hay E5 thì trình Minh, kèm cấu hình có đồ thị tốt nhất còn lại và mức chênh; không tự ép chọn cấu hình đồ thị kém hơn;
   - kết cục của từng thành phần tính bằng cách đảo trạng thái thành phần đó trong cùng bối cảnh; mâu thuẫn với lựa chọn thì báo xung đột, không tự thay cấu hình thắng.
9. **Biến thể (K-b):** hoán đổi riêng E1-CP và E2-VC tại cấu hình thắng và tại cấu hình đầy đủ, tối đa 4 cấu hình. Biến thể chỉ thay bản gốc khi luật C cho GIÚP tại cấu hình thắng; kết quả ở cấu hình đầy đủ chỉ báo kèm. Nếu cả hai đều GIÚP, chạy thêm đúng một cấu hình ghép rồi mới quyết; không ghép thành cấu hình chưa chạy.
10. **Ba thế giới:** chọn theo P. S_lo hoặc S_hi cho cấu hình thắng khác thì ghi "phụ thuộc quan sát" và trình Minh.
11. **Kiểm bối cảnh (KB),** sau T6, T9, T11, T12: đảo trạng thái từng thành phần của K (4 cấu hình). Kết cục khác lúc chọn thì ghi "phụ thuộc bối cảnh" và trình Minh; không tự đổi. Phép này không bao tương tác của nhiều thành phần cùng lúc; không kiểm sự phụ thuộc vào cách chấm ở chuỗi cuối (D24).
12. **Chi phí:** tối đa 25 cấu hình × 52 ca = 1.300 lượt chấm, chỉ tính K, K-b và KB. Thời gian chưa đo.

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

**Áp theo thứ tự; dừng ở bước đầu tiên khớp** (thứ tự theo D2b, Q-199):
1. **HẠI riêng → bỏ**, nếu có ít nhất một điều sau:
   - vi phạm UV-6 (với E3);
   - vi phạm điều kiện riêng của E5 (dưới đây);
   - tỷ lệ `CAUSE_FOUND` ở mốc giả RE2-TT tăng quá 0,10 trên mẫu số C-e, khi mẫu số > 0;
   - M + M′ ≥ 3 và P + P′ = 0.
2. **TRÁI CHIỀU theo dataset → Minh quyết:** ΔMRR_d > +δ_d ở một dataset và ΔMRR_d′ < −δ_d′ ở dataset kia.
3. **HẠI gộp → bỏ:** ΔMRR gộp < −δ.
4. **KHÔNG ĐỦ CA → giữ, kiểm trên FlashTicket** (M-48): |E_X| < 6. Trong bản P7, thành phần được giữ bật (D2a; luật chọn khối, bước 5).
5. **GIÚP → giữ:** ΔMRR gộp > +δ, P > M, và không dataset nào có ΔMRR_d < −δ_d.
6. **KHÔNG TÁC DỤNG:** |ΔMRR gộp| ≤ δ. Đề xuất bỏ, trừ khi X là phần cuối cùng còn đáp ứng MRP P6 tầng 2 hoặc DT18. Kết cục này nghĩa là chưa thấy lợi ích đủ để giữ trong bản đang chọn, không chứng minh X vô tác dụng.
7. **TRÁI CHIỀU theo ô → Minh quyết:** các trường hợp còn lại.

Bước 4 của luật chọn khối loại cấu hình theo cả HẠI riêng lẫn HẠI gộp. Bước 6 của luật chọn khối chỉ gắn cờ cho TRÁI CHIỀU.

**Điều kiện riêng của E5** (D2c, thay cho "D.2 lượt 5"):
- Bộ đánh giá tính sau khi ghép nhãn, trên 52 ca dev.
- Đại lượng đếm: số ca có cờ M5 ở k = 1, theo `results/T-028/codebook.md:95`. Cờ M5 bật khi có thực thể khác root có đường tới root trên đồ thị cha–con trước mốc, và đứng trước root hẳn; hòa không tính.
- So cặp (c bỏ E5, c) trong cùng bối cảnh. HẠI khi số ca này của c lớn hơn của c bỏ E5.
- Không đổi hoặc giảm thì xét tiếp theo luật C chung.
- E5 không có vế mốc giả riêng; E5 dùng chung vế mốc giả của mọi thành phần.

**Vế mốc giả:**
- Mẫu số bằng 0 thì vế này ghi "chưa kiểm được" và không áp (D2f).
- Mỗi cặp báo tỷ lệ của nhánh bật, nhánh tắt và mẫu số n. Mẫu số nhỏ làm một cặp đổi đã vượt ngưỡng (n = 9: 0,111).
- Cặp có 1 − tỷ lệ của nhánh tắt ≤ 0,10 thì vế này không thể kích hoạt; ghi "không phân xử được" (D17). Nhãn này không có nghĩa là đã đạt mức chấp nhận được.
- Vế này chỉ đo mức hại tương đối. Tỷ lệ tuyệt đối báo riêng cho mọi cấu hình (B1.7); mức tuyệt đối, nếu đặt, theo D17 (B4).

**Phụ thuộc quan sát:** áp luật trong cả ba thế giới (B1.3b). Ghi riêng ba thông tin: kết cục tại P; kết cục tại S_lo, S_hi; hành động chọn. Nếu S_lo hoặc S_hi cho kết cục khác P thì ghi "phụ thuộc quan sát, chưa phân xử"; kết cục tại P, kể cả HẠI, vẫn được ghi và báo.
- Ở bước quyết định theo luật C (T6, T9, T11, T12): xử lý như KHÔNG ĐỦ CA (D2f).
- Trong khối K: cặp phụ thuộc quan sát không là căn cứ loại ở bước 4. Bước 5 chỉ áp cho thành phần ít ca (bước 3). Thành phần không ít ca không bị ép bật; cấu hình chứa nó đi tiếp vào bước 7, chọn theo MRR tại P, nếu không bị loại bởi cặp khác theo luật khối.

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
| E4 (UV-7) | mọi ô | Cố định (D24); Q5 vế (1) kiểm đúng công thức; vế (2) chỉ báo cáo |
| E5 (MRP tầng 2) | ô có cờ M5 | luật C và điều kiện riêng của E5 |
| E6b (KS-10) | ô có root nằm trên cạnh | Luật C (T9). KHÔNG ĐỦ CA: giữ E6b bật (D2a, D2f). Kết cục khác theo luật C |
| E7 | — | mô tả (DT18 bắt buộc) |
| E8 | 0 | giữ, kiểm ở FT |
| E9 (KS-10) | chờ KS-16 | luật C |
| C-a0, C-a1, C-d1, C-d3, C-g (KS-11) | — | Cài được và không suy biến: báo kèm. Suy biến: bỏ, ghi lý do. Không chạy được: chuyển FT |
| C-h, PRISM (KS-11) | — | chỉ thêm nếu thẻ đọc cho được cách cài không cần nhãn |
| KS-14 thẻ đọc | — | Đổi công thức: sửa trước khi đóng băng. Bác giả định: bỏ hoặc sửa. Không đổi gì: giữ làm tham chiếu |
| KS-16 | — | Đủ ô: chạy thử. Thiếu ô: khai trước "không đủ ca". Không đếm được: UNSUPPORTED, kèm lý do |

---

## Phụ lục D — Quyết định của Minh

Bảng đề xuất trước ngày 26/10/2026 nằm trong lịch sử git và LOG. Bảng dưới là nội dung Minh đã duyệt: D1–D12 theo Q-199, D13–D19 theo Q-201; D13 sửa và D20–D23 theo Q-202; D17 sửa và D24 theo Q-205.

| # | Điều cần quyết | Quyết định | Nguồn |
|---|---|---|---|
| D1 | Phạm vi T-043; chia ba task cài đặt | Mã T-043; Claude làm, Codex phản biện. Phạm vi gồm thẻ đọc, KS-16 (T0), fixture; không cài phương pháp. Cài và thử chia ba task: (1) T1, T4, T4b và khối K; (2) K-b, T6, T9, T10, T11, T12 và KB; (3) T13 và hồ sơ G3. Dự toán từng task lấy từ bước 6 | Q-199 |
| D2a | M-48 "không đủ ca thì giữ lại" | Giữ thành phần bật trong bản P7 (luật chọn khối, bước 5) | Q-199 |
| D2b | Hai dataset đổi theo hai chiều rõ | Thứ tự luật C ở Phụ lục C: Minh quyết TRÁI CHIỀU theo dataset trước khi xét HẠI gộp | Q-199 |
| D2c | Điều kiện riêng của E5 | Theo Phụ lục C, thay cho "D.2 lượt 5" | Q-199 |
| D2d | Nhánh tắt E3 | Phương án A (B2, E3): giữ một kênh log lỗi cơ bản theo thực thể | Q-199 |
| D2e | Bước chọn cuối | Chỉ báo MRR từng dataset của các cấu hình gần tốt nhất; không lọc (B4, luật chọn khối, bước 7) | Q-199 |
| D2f | Phần còn lại của luật C | δ = 0,01; δ_d = 1/n_d; "phụ thuộc quan sát" xử lý như KHÔNG ĐỦ CA; mẫu số C-e bằng 0 ghi "chưa kiểm được"; báo n của C-e; E6b thiếu ca đi theo D2a | Q-199 |
| D3 | Tách nghiên cứu cảnh báo | Tách SPEC riêng. Hợp đồng gồm: t̂; tín hiệu và luật kích hoạt; dữ liệu có tới lúc chạy; cửa sổ N/A; cách gom sự cố; thời điểm trả kết quả. Ghi giới hạn N nhiễm lỗi khi báo trễ. Baseline chạy lại tại t̂ (B1.1) | Q-199 |
| D4 | Baseline Nezha-OB | Cấu hình M4 (T-026) chạy trên cùng tập đánh giá; 0,538 chỉ là số dev; các nhánh T-042 chỉ để chẩn đoán | Q-199 |
| D5 | Đối chứng | C-c gộp ba baseline; C-g chỉ kiểm E6b; giữ C-a0, C-a1, C-d1, C-d3; không thêm C-c6 | Q-199 |
| D6 | Nezha-OB không có mốc giả | Ghi "chưa đánh giá"; kiểm báo nhầm khi hệ khỏe trên FlashTicket | Q-199 |
| D7 | L1 (LLM tách mẫu log) | Không đưa vào lõi chạy trên dữ liệu công khai. Thử ở chặng 2, trước khi khóa bản FlashTicket. So chất lượng RCA khi dùng Drain và khi dùng LLM | Q-199 |
| D8 | T12 (cạnh tĩnh) | Phép hợp cạnh: cạnh quan sát cộng cạnh tĩnh (T-038 cho RE2-TT, T-039 cho Nezha-OB); chỉ dùng ở E5, E6b, E7, C-d1, C-d3; E1, E2 lấy từ span; nút chỉ có trong mô hình tĩnh là UNOBSERVED; cạnh trùng hướng gộp một; ghi điều kiện revision chưa xác minh; tác dụng OPEN (B4) | Q-199 |
| D9 | Thống kê | Luật chọn trên dev theo D2. WHY-06 ghi biên E-04 trước task cài đặt (1). Phép suy luận P7 chốt ở A4, trước G3 | Q-199 |
| D10 | Hai dòng Q-189 trùng mã | Giữ dòng cũ; nối dòng Q-200 làm mã tham chiếu cho quyết định giao Claude thiết kế; sửa tham chiếu ở mục Người làm | Q-199 |
| D11 | Dự đoán UV-1 | Bỏ vế (iii) và câu bác bỏ phụ thuộc vế đó trong kế hoạch còn hiệu lực; không sửa `goi-g2.md` | Q-199 |
| D12 | Giả định A0 (thu thập liên tục, đầy đủ) | Dùng có điều kiện, ghi "dưới A0"; không gọi ba thế giới là xác minh A0; luật ô biên và ô OPEN có bản ghi hoàn thiện trong T-043 trước khi áp dụng | Q-199 |
| D13 | Biến thể nền lùi ở chế độ báo động | Biến thể độ nhạy, chỉ báo cáo (B1.1). t_p: lúc đầu tiên trạng thái rời Normal trong đợt báo động (Pending, hoặc Alerting khi thời gian chờ bằng 0), lấy từ lịch sử trạng thái Grafana. g (sửa theo Q-202): trong miền hỗ trợ (luật Grafana trên Prometheus; phiên bản từ manifest; biểu thức đã thay biến, không `@`, không recording rule; Δ đã xác minh), g = lớn nhất qua các truy vấn của (t_p − e₀) + L. L tính theo cây biểu thức; e₀ là mốc đánh giá sớm nhất (truy vấn kiểu điểm: t_p − to; truy vấn kiểu khoảng: mốc đầu làm tròn xuống theo bước). N′ = [t_p − g − 300, t_p − g); baseline dùng cùng N′. UNSUPPORTED khi ngoài miền hỗ trợ, không xác minh được Δ, phiên bản hoặc biến, thiếu lịch sử trạng thái, hoặc thiếu dữ liệu trước t_p − g − 300; khi đó giữ lượt chính và báo số ca bị ảnh hưởng. Không bảo đảm nền sạch | Q-201; sửa Q-202 |
| D14 | Các phép so trên FlashTicket | B1.9. Bắt buộc: bản P7 đã khóa chạy thẳng; bản FlashTicket đã khóa; bản FlashTicket đã khóa che từng nhóm thông tin. Tùy chọn: gói thông tin chung tối ưu riêng, gọi đúng tên. Cùng ca, cùng cách chấm; che cả đầu vào lẫn phần dẫn xuất; nhánh dự phòng khai trước; không điền số 0 giả; không bỏ ca. Báo chế độ (a) (runner đọc mốc tiêm) và (b). RQ5 báo riêng câu "chuyển thẳng" và câu "sau thích nghi" | Q-201 |
| D15 | Thử thành phần trên FlashTicket | B1.9. Mỗi lần thử ghi bản, thay đổi, lý do kỹ thuật, kết cục trên dữ liệu công khai, phép phân xử, ngân sách. Giữ nguyên kết luận P7. Đổi cách đo là thành phần mới; cùng cách đo trên dữ liệu khác là thử lại thành phần cũ, báo kèm kết cục cũ. Tính vào ngân sách phát triển FlashTicket | Q-201 |
| D16 | RCA tại t̂ trên RE2-TT dev | Chỉ báo cáo; t̂ từ phát lại luật cảnh báo. Task đến sau SPEC phát hiện (D3) nhận. Hạn: trước mọi kết luận về RCA ở chế độ (b) và trước khi khóa bản FlashTicket (B1.1) | Q-201 |
| D17 | Vế mốc giả và tỷ lệ tuyệt đối | Cặp có 1 − tỷ lệ của nhánh tắt ≤ 0,10 ghi "không phân xử được" (không phải đã đạt). Báo tỷ lệ `CAUSE_FOUND` tuyệt đối cho mọi cấu hình. Mức tuyệt đối, nếu đặt, Minh quyết sau T1 và trước T4b; khối K là phép so đầu tiên dùng luật C; ghi rõ đặt sau khi xem dev T1 (Phụ lục C, B1.7, B4) | Q-201; sửa theo Q-205 (D24) |
| D18 | Đơn vị chấm của C-a0 | Không loại span bọc; mỗi span là một mẫu của thao tác thuộc chủ span, dùng thời lượng cả span, không phải một kênh riêng (B2, bảng đối chứng) | Q-201 |
| D19 | Phạm vi đồ thị cho nhóm vòng E5 và vùng E7 | Tính trên đồ thị con gồm nút có K_raw,₁ > 0 (cạnh quan sát, cộng cạnh tĩnh khi bật T12). Đồ thị đầy đủ vẫn được dựng và lưu trong bản ghi và gói bằng chứng. Đồ thị con rỗng thì cả hai cách dựng E7 trả vùng rỗng; trạng thái chẩn đoán và thứ hạng giữ nguyên. Đánh đổi: có thể cắt đường phụ thuộc thật qua thành phần trung gian không biểu hiện bất thường (B2, E5, E7) | Q-201 |
| D20 | E7 khi nhiều ứng viên cùng đứng đầu | Phương án (c): dựng vùng cho từng ứng viên trong nhóm hòa đứng đầu, ở thế giới P; báo p và \|R\| kỳ vọng theo trọng số ứng viên; vùng hợp chỉ là đầu ra phụ (B2, E7) | Q-202 |
| D21 | Nhánh E1 tắt | Phương án (i): thời lượng cả span, giữ span bọc như D18, lớp lan ngược; E3 thêm hướng xuống cho kênh thời lượng đang dùng; cặp bật/tắt E1 đo gói "dùng quan hệ cha–con ở mức thao tác" (B1.4; B2, E1, E3) | Q-202 |
| D22 | Chuỗi gốc của T1, T4b | R0 cộng nhánh chấm (B4) | Q-202 |
| D23 | Phạm vi RQ3d | Phương án A: C-a0, C-a1 là phép bỏ thành phần khỏi chuỗi đã chọn; ghi giới hạn; không thêm nhánh không quan hệ chọn riêng (B3; B4, T13) | Q-202 |
| D24 | Vai trò T4b và nhánh z | Điểm E4 cố định làm điểm của chuỗi và nền khối K; T4b chỉ báo cáo nhánh z: cờ chung, chỉ đổi điểm đơn vị phân vị, thang theo quy tắc RobustScaler (phương án A); KB bỏ phép đảo E4/z | Q-205 |
