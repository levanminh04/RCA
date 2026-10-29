# Đặc tả phương pháp M1 — bản v1

- **Task:** T-043, bước 2. **Người làm:** Claude. **Người phản biện:** Codex. **Ngày:** 28/10/2026.
- **Quan hệ với SPEC:** bản này hoàn thiện Phụ lục B của `tasks/T-043-thiet-ke-rca-m1/SPEC.md`. Phần nào SPEC đã quyết (D1–D24) thì giữ nguyên và dẫn lại. Phần SPEC giao cho T-043 viết thì ghi ở đây và đánh dấu **[T-043]**. Khi bản này và SPEC lệch nhau, SPEC thắng; chỗ lệch phải báo ở `bao-cao.md`.
- **Trạng thái:** mọi thành phần là ứng viên (CANDIDATE), trừ phần đã quyết: điểm E4 (D24), luật C, luật chọn khối, danh sách đối chứng. Mọi dự đoán dưới đây **chưa kiểm**. Bản này không chọn thành phần và không khẳng định lợi ích của đồ thị.
- **File đi kèm:**
  - `hop-dong.json`: schema vào/ra, trạng thái, trường cấm, danh mục kênh, ánh xạ severity;
  - `dinh-nghia-pha2.json`: ô kích hoạt, O1–O4, hình dạng xếp hạng, RR theo ô (băm trước pha 2 của KS-16);
  - `fixture-dac-ta.json`: 82 ca giả có đáp án;
  - `ma-tran-thu.json`: ma trận thử (đóng băng ở bước 5).

## 0. Mười trường của mỗi thành phần [T-043]

SPEC yêu cầu "đủ 10 trường" nhưng không liệt kê. Danh sách dưới đây do người làm dựng từ ba nguồn:
- MRP P6 "Cấu trúc tổng": nguồn, dữ liệu cần dùng, cách xử lý khi thiếu, nhánh bỏ, ba kết cục;
- MRP P6 "Đầu ra": mục đích, loại căn cứ, phương án đã xét, điều kiện thất bại;
- AGENTS luật 18: nút, cạnh, nơi đặt tín hiệu, phép tính dùng cạnh.

| # | Trường | Nội dung |
|---|---|---|
| 1 | Mục đích, loại căn cứ | sửa hạn chế P4 / đáp ứng DT18 / nhu cầu kỹ thuật / công trình khác; mã nguồn |
| 2 | Đầu vào | tín hiệu, nguồn, đơn vị; khẳng định **không nhận nhãn** |
| 3 | Phép tính | công thức và tham số khai trước |
| 4 | Quan hệ dùng | nút, cạnh, phép tính dùng cạnh; hoặc "không dùng quan hệ" |
| 5 | Đầu ra, trạng thái | kênh, cờ, điểm, mã trạng thái |
| 6 | Thiếu dữ liệu, nhánh dự phòng | xử lý khi thiếu đầu vào; không điền số giả |
| 7 | Nhánh tắt | cấu hình khi tắt; thông tin còn giữ |
| 8 | Điều kiện thất bại | đã biết; chưa kiểm |
| 9 | Phép thử trên dev | bước ma trận, ô kích hoạt, kết cục và ngưỡng số |
| 10 | Phương án đã xét, trạng thái | phương án khác, lý do; ứng viên / cố định / chỉ báo cáo; nơi kiểm tiếp |

## 1. Hợp đồng dữ liệu

- **API.** Phương pháp nhận đúng các tham số: `spans`, `metrics`, `logs`, `inventory` (U), `aliases`, `t`, `params`. Không nhận tên ca, đường dẫn, mã mờ, nhãn hay mốc tiêm ngoài `t` của chế độ (a) (luật cứng 6; MRP §6.8). Schema chi tiết ở `hop-dong.json#/vao`.
- **Bản ghi ra.** Mở rộng `ban_ghi.tao` với `method = "M1"`, `variant = config_id`, cộng các khóa `classes`, `inherited_by`, `region`, `evidence_refs`, `coverage`, `worlds`, `verdict` (SPEC B1.7). Schema ở `hop-dong.json#/ra`.
- **Kiểm trường cấm.** Bộ kiểm M1 duyệt đệ quy qua dict, list và tuple. Tên cấm gồm danh sách `CAM` của `src/p3/ban_ghi.py` cộng các khóa cấm của `src/p3/nezha.py`. Phản ví dụ ở fixture 74. `ban_ghi.kiem` hiện hành không dùng làm bằng chứng (SPEC, Kiểm đúng đắn). Bộ kiểm cài ở task cài đặt (1), không sửa `src/p3`.
- **Bộ lọc tên không đủ.** Lọc tên trường không chứng minh đặc trưng không suy từ nhãn. Mỗi thành phần ở mục 7–8 ghi rõ đầu vào để lần theo đường truyền.

## 2. Cửa sổ và trạng thái quan sát

### 2.1 Cửa sổ (SPEC B1.1, giữ nguyên)

- Chế độ (a): N = [t−300, t), A = [t, t+300). Miền đọc là [t−300, t+300). Span vào miền khi start ≥ t−300 và end < t+300 (`cua_so.cat_span`).
- Span thuộc A khi end ≥ t.
- Mốc giả C-e (chỉ RE2-TT): t′ = t−300, miền [t−600, t).
- Chế độ (b) và biến thể nền lùi (D13): theo SPEC B1.1, không làm trong ma trận dev.

### 2.2 Luật trạng thái quan sát trên dữ liệu dev [T-043, hoàn thiện D12]

D12 yêu cầu T-043 hoàn thiện luật ô biên và ô OPEN có bản ghi trước khi áp ba thế giới. Luật dưới đây đặt **trước** khi chạy đủ KS-16 pha 1. Chỉ lượt thử nhanh 2 ca (`ks16/runs/thu-nhanh-001`, không nhãn) đã chạy trước đó; lý do sửa ghi ở LOG phiên 7.

1. **Độ phân giải mốc.** Mỗi bản ghi tại x phủ [x, x + r):
   - log và metric RE2-TT: r = 1 giây (mốc giây nguyên);
   - span RE2-TT: r = 1 µs;
   - Nezha-OB: r = 1 ns.
   Mốc của span là end, cùng quy ước chia N/A.
2. **Khoảng ghi của file F_s** của nguồn s (trace, log, metric) trong ca: [min x, max x + r) trên mọi bản ghi của file nguồn.
   - Nguồn nhiều file (Nezha-OB: ba file phút): F_s là hợp các khoảng của từng file.
   - Khe giữa hai file dài hơn 10 giây nằm ngoài F_s.
3. **Bao bản ghi H_s:** [min x, max x + r) của bản ghi của s, mọi thực thể gộp lại, trong **cả cửa sổ đang xét** ([t−300, t+300); mốc giả: [t−600, t)).
   - A0 nói về "khoảng có bản ghi" của nguồn, nên H không cắt tại t.
   - Biến thể H tính riêng từng phía chỉ báo kèm, không dùng (xem LOG phiên 7).
4. **Trạng thái của từng phần thời gian:**
   - ngoài F_s: XÁC NHẬN THIẾU THU;
   - trong F_s ∩ H_s: QUAN SÁT THEO A0;
   - trong F_s, ngoài H_s: OPEN;
   - XÁC NHẬN CÓ QUAN SÁT không xảy ra trên dev, vì dev không có siêu dữ liệu collector.
5. **Ô biên.** Ô 10 giây chứa nhiều trạng thái được tách theo **giây thực**: phần A0 tính vào T^chắc; phần OPEN tính vào T^max; phần thiếu thu không tính. Bản ghi nằm trong ô biên được giữ, vì theo định nghĩa chúng nằm trong F ∩ H.
6. **Ô OPEN có bản ghi.** Với luật trên, một ô OPEN không thể chứa bản ghi của chính nguồn đó, vì mọi bản ghi nằm trong H_s. KS-16 pha 1 kiểm giá trị này bằng 0 (`ks16/dem-khong-nhan.json#/tong_hop/*/quan_sat/*/o_open_co_ban_ghi_cung_nguon`). Bản ghi của nguồn khác trong ô OPEN chỉ là bằng chứng hỗ trợ, không đổi trạng thái.
7. **Thời lượng quan sát** cho đơn vị đếm (B1.3b):
   - T^chắc = |F ∩ H ∩ phía|; T^max = |F ∩ phía|;
   - P: (T_N^chắc, T_A^chắc); S_lo: (T_N^max, T_A^chắc); S_hi: (T_N^chắc, T_A^max).
8. **Nguồn metric không tham gia T.** Mọi kênh metric là đơn vị phân vị, nên thời lượng quan sát không đổi điểm của chúng (B1.3b). Trạng thái ô của metric chỉ được báo.
   - Ở Nezha-OB, mẫu metric cách nhau 1 phút, nên phần đầu và cuối cửa sổ ngoài H là OPEN theo luật. Phần này không ảnh hưởng đơn vị nào.
9. **Dữ kiện dev do KS-16 pha 1 đo** (`ks16/dem-khong-nhan.json`):
   - RE2-TT: trace, log, metric phủ [t−720, t+720] ở mọi ca, trừ ca không có file log. Không ô OPEN nào; chỉ có ô biên ở hai đầu cửa sổ, phần OPEN dưới 1,4 giây.
   - Nezha-OB: trace và log chỉ phủ 42–97 giây ở N và 84–140 giây ở A. Phần còn lại ngoài khoảng ghi của ba file phút, nên là XÁC NHẬN THIẾU THU. Kết quả này thay câu "tối đa khoảng 150 giây" ở SPEC B1.5 và câu "[t−300, t−150) … là OPEN" ở B1.3b; SPEC đã cho phép KS-16 kết luận khác.
   - Hệ quả: trên dev, ba thế giới P, S_lo, S_hi chỉ khác nhau ở phần OPEN dưới 1,4 giây. OBS_DEPENDENT và RANK_CHANGED nhiều khả năng hiếm (chưa kiểm). Ba thế giới vẫn chạy và báo theo SPEC.

### 2.3 Ba thế giới, cờ chẩn đoán

Giữ nguyên SPEC B1.3b: OBS_DEPENDENT, RANK_CHANGED (phương pháp xuất) và WORLD_DEPENDENT (bộ đánh giá tính). Kết cục thành phần áp luật C trong cả ba thế giới, kết cục chính theo P (Phụ lục C).

## 3. Tiền xử lý span (SPEC B1.2)

- Khóa (traceID, spanID). Bỏ bản lặp y hệt và đếm. Khóa trùng mà nội dung khác thì cả ca trả `ERROR`.
  - Trên dev: Nezha-OB có 5.800 bản lặp y hệt trên 1.421.887 dòng adapter; RE2-TT 0. Không ca nào có khóa trùng khác nội dung.
- Quan hệ cha–con dựng trên toàn miền. Span gốc là span có parent rỗng. Span có parent không resolve là span mồ côi, đếm riêng.
  - Ở Nezha-OB, span vào của trace có parent không resolve, nên mọi span vào đều là mồ côi (32.584).
- **Cắt con về cha [T-043, theo CRISP §5.2]:**
  - con cắt về [s₀, s₁) của cha;
  - con nằm hẳn ngoài cha (độ dài sau cắt ≤ 0) bị bỏ khỏi phép tính của cha;
  - con vượt biên cha quá 1 ms được đếm để chẩn đoán (trên dev: RE2-TT 6.272, Nezha-OB 5.808 trên miền).
- **Span bọc w [T-043, dạng chặt]:** w có **đúng một con** và con đó ở thực thể khác; cha của w resolve và cùng thực thể với w.
  - Dạng lỏng (cho phép thêm con cùng thực thể) trùng dạng chặt ở mọi ca dev: RE2-TT 1.643.384, Nezha-OB 338.829.
  - Chọn dạng chặt vì khi đó g(w) đúng là phần ngoài span của bên được gọi.

## 4. Thống kê chung E4 (SPEC B1.3; cố định theo D24)

Giữ nguyên SPEC B1.3 và B1.8:
- hỗ trợ tối thiểu m_span = 20, m_metric = 5;
- ngưỡng Q₀.₉₅, Q₀.₀₅ nội suy type 7; ε = 0,05;
- cổng một phía: chính xác có điều kiện khi n ≤ 100, xấp xỉ có hiệu chỉnh khi n > 100; α = 0,01;
- e_d = max(0, r_d(A) − r_d(N)) khi qua cổng;
- đơn vị đếm: kiểm nhị thức chính xác với p₀ = T_A / (T_N + T_A), tổng tối thiểu 10, λ = n_N · T_A / T_N;
- cờ F_raw, F_I; khóa K_raw, K_I.

Phần [T-043] làm rõ:
- **Trạng thái đơn vị phân vị:**
  - OK: n_N ≥ m và n_A ≥ m, tính trên giá trị hữu hạn;
  - LOW_SUPPORT: có dữ liệu ở cả hai phía nhưng thiếu hỗ trợ;
  - NO_BASELINE: n_N = 0;
  - NO_A: n_A = 0.
- **Trạng thái đơn vị đếm:**
  - NO_BASELINE khi T_N = 0; NO_A khi T_A = 0;
  - với kênh dựa trên severity: NO_BASELINE khi N có dòng nhưng không dòng nào có severity xác định; NO_A tương tự ở A;
  - LOW_SUPPORT khi n_N + n_A < 10;
  - còn lại OK.
- **NEW_OP:** n_N = 0, n_A ≥ 10, T_N > 0. Khi đó F_raw,lên = 1, e_up = 1.
- **STOPPED:** n_A = 0, n_N ≥ 10, T_A > 0. Khi đó F_raw,xuống = 1, e_dn = 1.
- Dưới 10 sự kiện thì là LOW_SUPPORT, theo ngưỡng tổng tối thiểu của B1.3.
- **Cache cổng** theo khóa nội dung (SPEC B1.3). Phép tính dùng float64. Cổng chính xác dùng mã B1.8. Fixture so với oracle phân số, sai số ≤ 1e−12.
- **Nhánh z (T4b, chỉ báo cáo; D24):** theo SPEC B2 E4. Phép biến đổi đầu vào khai ở `hop-dong.json#/nhanh_z`: giữ đơn vị nguồn, không đổi. Thời lượng span tính bằng µs ở cả hai dataset. Metric giữ đơn vị của cột.

## 5. Danh mục kênh và lớp tín hiệu [T-043]

Bảng lớp của SPEC B1.4 giữ nguyên. Ánh xạ cụ thể theo dataset ở `hop-dong.json#/kenh`. Tóm tắt:

| Kênh | Đơn vị | Hướng chấm | Lớp | Có khi |
|---|---|---|---|---|
| Thời lượng cả span theo thao tác | phân vị | lên; E3 thêm xuống | lan ngược | E1 tắt |
| Thời gian độc quyền theo thao tác (bỏ span bọc) | phân vị | lên; E3 thêm xuống | không lan | E1 bật |
| Khoảng ngoài span g(w) theo cạnh | phân vị | lên | không lan, gán theo E2-C hoặc E2-VC | E2 bật |
| Metric tài nguyên (RE2-TT: cpu, mem, diskio, socket; Nezha-OB: CPU, bộ nhớ, syscall, byte mạng) | phân vị | lên (không lan); xuống (lan xuôi) | theo hướng | mọi cấu hình |
| Metric độ trễ (RE2-TT: latency-50, latency-90; Nezha-OB: Pod/Front Latency P50–P99) | phân vị | lên | lan ngược | mọi cấu hình |
| Metric lỗi (RE2-TT: error) | phân vị | lên | lan ngược | mọi cấu hình |
| Metric lưu lượng (RE2-TT: workload; Nezha-OB: PodWorkload) | phân vị | lên (lan ngược); xuống (lan xuôi) | theo hướng | mọi cấu hình |
| Tỷ lệ thành công (Nezha-OB: PodSuccessRate, FrontSuccessRate) | phân vị | xuống | lan ngược | E3 bật |
| Mật độ dòng log lỗi theo thực thể | đếm | lên | lan ngược | E3 tắt (D2d) |
| Mẫu Drain lỗi theo (thực thể, mẫu); ô "mẫu mới" | đếm | lên | lan ngược | E3 bật |
| Mẫu Drain thường theo (thực thể, mẫu) | đếm | xuống | lan xuôi ("log thường giảm") | E3 bật |
| Tần suất theo thao tác; NEW_OP; STOPPED | đếm | lên (lan ngược); xuống (lan xuôi) | theo hướng | E3b bật |

**Quy ước [T-043]:**
- **Giữ mọi cột metric có trong file của ca.** Theo WHY-27: không bỏ cột, không điền cột vắng. Hệ quả: nhiều phân vị tương quan của cùng một độ trễ làm tăng "số kênh" trong khóa K. Đây là giới hạn đã khai.
  - Phương án đã xét: chỉ giữ P90. Lý do không chọn: là một lựa chọn riêng, chưa có căn cứ, và lệch WHY-27.
- **Tỷ lệ thành công chỉ chấm khi E3 bật.** D2d: E3 bật bổ sung hướng xuống cho tỷ lệ thành công. Vì vậy khi E3 tắt, kênh này không có hướng chấm.
- **Metric tài nguyên chấm cả hai hướng ở mọi cấu hình.** B1.4 liệt kê "tài nguyên giảm" thành lớp riêng, không gắn với E3.
  - Phương án đã xét: chỉ chấm hướng giảm khi E3 bật. Không chọn vì SPEC không gắn hướng này với E3.
- **Mẫu Drain:** mỗi mẫu xếp lỗi hay thường theo đa số dòng của nó ở N (severity hoặc từ khóa). Hòa xếp vào lỗi.
- **Ô "mẫu mới"** gom các dòng A không khớp mẫu nào học từ N. Lớp lan ngược, như "thao tác mới".
- **Metric front của Nezha-OB** gắn vào thực thể `frontend`. Metric dùng chung chỉ gắn một lần.

## 6. Ứng viên, tầng, trạng thái thực thể, kết luận

Giữ SPEC B1.6–B1.7. Phần [T-043] làm rõ:
- **Tập quan sát O** của một cấu hình: thực thể của U có ít nhất một kênh có dữ liệu, bất kể trạng thái.
- **Tập trả về R:** thực thể có ít nhất một kênh OK, xếp theo ba tầng.
- Thực thể thuộc O nhưng không có kênh OK nào ghi `NO_VALID_CHANNEL`, không được trả về. Nếu đó là root thì RR = 0, như UNOBSERVED (WHY-28). Bộ đánh giá báo riêng số ca root rơi vào trường hợp này. Đây là cách đọc đúng câu "thực thể có ít nhất một kênh OK được xếp" của B1.6, không là luật mới.
- **Khóa sắp trong tầng:** so tuple chính xác (max s, số kênh, Σs). Tầng 3 là một khối hòa.
- **`verdict`:** theo SPEC B1.7, xét trên thế giới P.

## 7. Thành phần

### 7.1 E1 — thời gian độc quyền (gói hai thay đổi, D21)

1. **Mục đích, căn cứ.** Sửa hạn chế P4. G2-H03 (TraceRCA bản thư viện chấm thời gian chờ root thành bất thường của bên gọi) và G2-H06; ứng viên UV-2 (mức ĐC: phần không do con phủ tách được root ở 26/26 ca RE2-TT, so với 8/26 theo thời lượng cả span; Nezha-OB 10/22). Công trình khác: CRISP, TraceDiag (thẻ đọc).
2. **Đầu vào.** Span trong miền: start, end, owner, operation, parent. Không nhận nhãn.
3. **Phép tính.**
   - E1-U: u(s) = d(s) − |∪ con đã cắt về [s₀, s₁)|.
   - E1-CP: u(s) = d(s) − |∪ con trên đường găng CRISP đã cắt|; happensBefore(c, d) khi c_end − 1 ms < d_start và không con nào khác bắt đầu hay kết thúc trong vùng chồng lấn (thẻ CRISP).
   - Đơn vị: thao tác (thực thể, tên), bỏ span bọc. Mẫu u(s) chia N/A theo end.
4. **Quan hệ dùng.** Cha–con trong trace: hợp khoảng con; nhận dạng span bọc.
5. **Đầu ra.** Kênh "độc quyền" của thao tác; lớp không lan; lên (E3 bật thêm xuống).
6. **Thiếu dữ liệu.** Thao tác chỉ có span bọc thì không có đơn vị E1 (thời gian đi sang g(w) khi E2 bật). Span mồ côi vẫn là mẫu của thao tác: u tính trên con của nó. Thiếu span con thì u = d, không bù.
7. **Nhánh tắt (D21).** Thời lượng cả span; giữ span bọc như mẫu của thao tác thuộc chủ span; lớp lan ngược. Nhánh tắt không dùng quan hệ ở mức thao tác.
8. **Điều kiện thất bại.**
   - bên được gọi không có span (S7);
   - gọi bất đồng bộ;
   - lỗi không làm tăng thời gian;
   - lệch đồng hồ quá 1 ms (RE2-TT có 14,8% lời gọi kết thúc sau cha, theo `call-interval-001`);
   - "thời gian chưa được con phủ" chưa phải thời gian CPU (KE-HOACH D.2 ghi chú 4).
9. **Phép thử.**
   - Khối K, cặp bật/tắt E1, luật chọn khối;
   - ô kích hoạt theo `dinh-nghia-pha2.json#/o_kich_hoat/E1`;
   - K-b E1-CP chỉ chạy khi tỷ lệ chồng lấn ≥ 5% (Q2). KS-16 pha 1 đo RE2-TT 0%, Nezha-OB 0,16%, nên E1-CP khai trước KHÔNG ĐỦ CA và K-b không chạy E1-CP.
10. **Phương án, trạng thái.**
   - Đã xét: trừ tổng duration con (sai khi chồng lấn; MRP P6); CP theo CRISP (biến thể K-b).
   - Trạng thái: ứng viên. Kiểm tiếp E1-CP trên FlashTicket, nơi có lời gọi song song và kind.

### 7.2 E2 — khoảng ngoài span của bên được gọi

1. **Mục đích, căn cứ.** Sửa hạn chế P4. G2-H06 (trễ mạng: dấu hiệu nằm ở span phía gọi); UV-1 (mức ĐC: 19/20 ca RE2-TT, 13/20 ca Nezha-OB theo span phía gọi); UV-5. Công trình khác: MicroHECL (gắn bằng chứng theo cạnh; thẻ đọc).
2. **Đầu vào.** Span bọc w và con c của nó. Không nhận nhãn.
3. **Phép tính.**
   - g(w) = d(w) − |c đã cắt về w|, tức u(w) theo E1-U.
   - Mỗi cạnh a → b có mẫu g ở N và A, chấm theo E4, chỉ hướng lên.
   - E2-C: gán kênh cạnh cho bên được gọi b.
   - E2-VC:
     - S là tập cạnh có F_raw,lên = 1;
     - liệt kê mọi phủ đỉnh nhỏ nhất của S;
     - đỉnh nằm trong mọi phủ nhỏ nhất là đỉnh định danh; nó nhận điểm lớn nhất của các cạnh nó phủ;
     - cạnh còn lại gán cho bên được gọi, kèm cờ "không định danh";
     - S có hơn 25 đỉnh thì dùng E2-C cho mọi cạnh và đếm số lần.
4. **Quan hệ dùng.** Cạnh dịch vụ có hướng a → b, lấy qua span bọc; phủ đỉnh trên đồ thị con của các cạnh có cờ.
5. **Đầu ra.** Kênh "E2:a→b" của thực thể nhận; lớp không lan; cờ "không định danh"; số lần dự phòng.
6. **Thiếu dữ liệu.** Cạnh không có span bọc thì không có kênh. Cạnh dưới 20 mẫu ở một phía thì LOW_SUPPORT.
7. **Nhánh tắt.** Chuỗi không có kênh cạnh. Khi E1 tắt mà E2 bật, thời gian của span bọc có mặt ở cả mẫu thao tác của bên gọi và mẫu g(w) (SPEC B2, đã khai).
8. **Điều kiện thất bại.**
   - cạnh đơn lẻ do trễ chiều ra (không định danh được);
   - cạnh thưa;
   - không có span bọc;
   - g(w) gộp cả đường truyền, hàng đợi và xử lý phía gọi (T-032 bảng C).
9. **Phép thử.**
   - Khối K, cặp bật/tắt E2-C;
   - K-b đổi E2-VC cho E2-C tại cấu hình thắng, chỉ thay khi luật C cho GIÚP;
   - ô kích hoạt: `dinh-nghia-pha2.json#/o_kich_hoat/E2`, `#/E2-VC`.
10. **Phương án, trạng thái.**
    - Đã xét: gán cho chủ span (giải thích khác của UV-1); giữ dấu khi so cạnh vào/ra (UV-5, không còn bắt buộc).
    - Ứng viên. Trên FlashTicket, đo bằng cặp CLIENT–SERVER là thành phần mới (D15).

### 7.3 E3 — log theo mẫu và tín hiệu hai chiều

1. **Mục đích, căn cứ.** Sửa hạn chế P4. G2-H07 (lỗi return ở Nezha-OB); UV-6 (mức LĐ, 4 ca return). Nguồn: Nezha, Eadro (KE-HOACH D.2).
2. **Đầu vào.** Dòng log (thời điểm, thực thể, nội dung, severity nếu có); kênh thời lượng đang dùng; tỷ lệ thành công. Không nhận nhãn.
3. **Phép tính.**
   - Che token biến: số, hex ≥ 8, UUID, IP, chuỗi trong ngoặc.
   - Drain: độ sâu 4, ngưỡng giống 0,4; học **chỉ trên dòng ở phần N quan sát được** của thế giới đang tính. Bản cài khuyến nghị: `drain3` 0.9.11, có sẵn ở `D:/RCA-ext/envs/T-016-cong-cu`.
   - Đơn vị đếm theo (thực thể, mẫu) và ô "mẫu mới", chấm theo B1.3 với T của nguồn log.
   - Thêm hướng xuống cho kênh thời lượng đang dùng (độc quyền hoặc cả span) và tỷ lệ thành công.
4. **Quan hệ dùng.** Không. Log gắn lên nút theo thực thể và thời gian. Nối log–span là ứng viên chưa dùng (xem 7.3b).
5. **Đầu ra.** Kênh mẫu lỗi, mẫu thường, mẫu mới, hướng xuống; số dòng UNKNOWN theo thực thể và cửa sổ.
6. **Thiếu dữ liệu.**
   - Không có file log (RE2-TT, 1 ca): mọi đơn vị log ở trạng thái NO_BASELINE.
   - Severity UNKNOWN: vẫn đi vào Drain, không tính là lỗi.
7. **Nhánh tắt (D2d, phương án A).** Một đơn vị đếm mỗi thực thể: số dòng log lỗi; chỉ hướng lên; không Drain; không hướng xuống.
8. **Điều kiện thất bại.**
   - số dòng log không bằng số request;
   - lỗi lan lên bên gọi (cần E5);
   - độ phủ severity khác nhau giữa N và A (N9, OPEN);
   - mẫu Drain học trên N quá ngắn ở Nezha-OB (42–97 giây).
9. **Phép thử.**
   - Khối K, cặp bật/tắt E3; luật chọn khối;
   - điều kiện riêng UV-6: số ca đang đúng bị hỏng không được vượt số ca lỗi mã được sửa;
   - ô kích hoạt: `dinh-nghia-pha2.json#/o_kich_hoat/E3`.
10. **Phương án, trạng thái.**
    - Đã xét: LLM gom mẫu (D7, chặng 2); bỏ hẳn log khi E3 tắt (không chọn: khối K mất kênh log).
    - Ứng viên.

#### 7.3b Nối log–span (SPEC E3, quyết sau KS-16)

KS-16 pha 1 trên Nezha-OB dev (`ks16/dem-khong-nhan.json#/cases/*/log_span_join`):
- 1.539.335 dòng log trong miền đều có TraceID và SpanID;
- 1.537.834 dòng khớp đúng một span của miền (99,90%); 1.501 dòng không khớp; 0 dòng khớp nhưng lệch thời gian quá 1 giây.

RE2-TT không có cột ID; không thông điệp nào chứa chuỗi hex 32 ký tự.

**Đề xuất [T-043]: không dùng nối log–span trong bản P7.** Lý do ghi ở `why-de-xuat.md` (WHY-E3-NOI):
- chỉ một dataset nối được, nên phép tính không chung cho hai dataset;
- chưa có câu hỏi trên dev mà nối log–span phân xử được, khác với đếm theo thực thể;
- giữ làm ứng viên chặng 2 trên FlashTicket, nơi B16 yêu cầu trace_id trong log.

### 7.4 E3b — cấu trúc trace

1. **Mục đích, căn cứ.** Công trình khác (KS-10, ghi chú 6), nhắm lỗi return.
2. **Đầu vào.** Số span theo thao tác ở N và A; T của nguồn trace. Không nhận nhãn.
3. **Phép tính.** Đơn vị đếm theo thao tác (B1.3); NEW_OP, STOPPED (mục 4).
4. **Quan hệ dùng.** Không.
5. **Đầu ra.** Kênh tần suất lên (lan ngược), xuống (lan xuôi); NEW_OP; STOPPED.
6. **Thiếu dữ liệu.** T_N = 0 thì NO_BASELINE.
7. **Nhánh tắt.** Không có kênh tần suất từ trace.
8. **Điều kiện thất bại.**
   - thao tác mới xuất hiện ở bên gọi;
   - tần suất giảm lan xuôi;
   - tải đổi làm đơn vị đếm báo đổi (B1.3);
   - ở Nezha-OB, thao tác gần biên file phút có thể ngừng vì khoảng ghi bị cắt. KS-16 pha 1 thấy 22 STOPPED ở Nezha-OB, 0 ở RE2-TT; nguyên nhân chưa phân xử.
9. **Phép thử.** T6, luật C; ô kích hoạt: `dinh-nghia-pha2.json#/o_kich_hoat/E3b`.
10. **Phương án, trạng thái.** Ứng viên. SPEC dự kiến Nezha-OB OBS_DEPENDENT; dự kiến này mất căn cứ vì không có ô OPEN (mục 2.2).

### 7.5 E4 — chuẩn hóa chung

Cố định theo D24; mười trường như SPEC B1.3 và mục 4:
1. **Mục đích:** nhu cầu kỹ thuật, sửa G2-H09/H12 (UV-7).
2. **Đầu vào:** mẫu của đơn vị. Không nhận nhãn.
3. **Phép tính:** B1.3, B1.8.
4. **Quan hệ dùng:** không.
5. **Đầu ra:** trạng thái, cờ, điểm, p.
6. **Thiếu dữ liệu:** trạng thái của mục 4.
7. **Nhánh tắt:** không có (cố định). T4b chỉ báo cáo nhánh z.
8. **Điều kiện thất bại:**
   - bão hòa;
   - trôi nền (G2-H10, fixture 81);
   - biên ε·|q| phụ thuộc mức tuyệt đối;
   - giả định mẫu độc lập ở cổng (AR(1): tỷ lệ qua cổng 7,3–38,6% khi hệ số 0,5–0,98).
9. **Phép thử:**
   - T1: phân bố điểm; QT5; tỷ lệ qua cổng ở mốc giả RE2-TT; bất biến theo thứ tự hàng và hash seed;
   - T4: độ nhạy ε, α, T4c;
   - T4b: nhánh z, chỉ báo cáo. Vế (1) là kiểm công thức (ngưỡng: điểm kênh E4 hữu hạn và thuộc [0; 1]; điểm z hữu hạn). Vế (2) chỉ mô tả.
10. **Phương án, trạng thái:** điểm z kiểu BARO (nhánh báo cáo); cố định.

### 7.6 E5 — tách tự sinh và kế thừa

1. **Mục đích, căn cứ.** Đáp ứng MRP P6 tầng 2 (đồ thị tham gia điểm bất thường; DT18, bước 2 của cô), nhắm giả thuyết P4 "nhầm triệu chứng với nguyên nhân" (G2-H17, cờ M5). "Lan có đáng kể" còn mở (O09). Công trình khác: MicroHECL, TraceDiag, PetShop.
2. **Đầu vào.** Cờ F_raw của mọi kênh; lớp kênh; cạnh quan sát N ∪ A (cộng cạnh tĩnh khi T12 bật). Không nhận nhãn.
3. **Phép tính.** Theo SPEC B2 E5:
   - kênh lan ngược của e là kế thừa khi có bên được gọi b có kênh F_raw = 1 thuộc lớp lan ngược, E1, E2, tài nguyên tăng hoặc thao tác mới;
   - kênh lan xuôi của e là kế thừa khi có bên gọi a có kênh F_raw = 1 bất kỳ;
   - trong SCC của đồ thị con F_raw (D19), chỉ được giải thích bởi thành viên có bất thường không lan, hoặc bởi bên được gọi ngoài SCC;
   - kênh kế thừa có F_I = 0.
4. **Quan hệ dùng.** Cạnh có hướng giữa thực thể; hướng giải thích theo lớp tín hiệu.
5. **Đầu ra.** `classes`; `inherited_by` theo kênh: kênh, điểm trước E5, đơn vị giải thích, cạnh, quy tắc, trạng thái.
6. **Thiếu dữ liệu.** Thực thể không có cạnh thì không bị giải thích. Bên được gọi UNOBSERVED không giải thích được ai.
7. **Nhánh tắt.** F_I = F_raw.
8. **Điều kiện thất bại.**
   - root ở bên gọi gửi lại nhiều lần;
   - hai dịch vụ cùng máy;
   - hai lỗi đồng thời;
   - cờ yếu, có thể do cổng qua giả, ở bên được gọi xóa bằng chứng mạnh của bên gọi; xác suất này tăng theo số đơn vị của bên được gọi (fixture 57; tự tương quan, mục 7.5);
   - kênh tài nguyên trôi nền ở bên được gọi.
9. **Phép thử.**
   - Khối K, cặp (c bỏ E5, c);
   - điều kiện riêng E5: HẠI khi số ca có cờ M5 của c lớn hơn của c bỏ E5;
   - vế mốc giả chung; dấu vết theo kênh;
   - ô kích hoạt: `dinh-nghia-pha2.json#/o_kich_hoat/E5`.
10. **Phương án, trạng thái.**
    - Đã xét: Traversal (PetShop) — dùng làm đối chứng C-d3; phân bổ Shapley (TraceDiag) — chưa đưa vào; tương quan kiểu MicroHECL — ứng viên chưa có hợp đồng khả thi (thẻ MicroHECL); giải thích cùng loại tín hiệu — ứng viên.
    - Giải thích chéo loại tín hiệu là đề xuất của M1, không có trong MicroHECL.
    - Ứng viên.

### 7.7 E6a — xếp theo tầng

1. Nhu cầu kỹ thuật: thứ tự mặc định. 2. Khóa K_I, K_raw; không nhãn. 3. Ba tầng (mục 6). 4. Không dùng quan hệ ngoài phần đã có trong F_I. 5. Thứ hạng khối. 6. Không có kênh OK thì không xếp. 7. Là nhánh tắt của E6b. 8. Hòa nhiều ở tầng 3 và khi điểm bão hòa. 9. Nền của T9. 10. Cố định làm nền.

### 7.8 E6b — PageRank cá nhân hóa trên đồ thị con bất thường

1. **Mục đích, căn cứ.** Đáp ứng DT18 và ví dụ "PageRank" của cô; công trình khác MicroRCA (MRP §2.3). Không phải sửa hạn chế P4.
2. **Đầu vào.** K_I, K_raw; cạnh N ∪ A. Không nhận nhãn.
3. **Phép tính.** Theo SPEC B2 E6b:
   - s(e) = K_I,₁(e);
   - chuyển a → b tỷ lệ s(b), tự lặp tỷ lệ s(a), v tỷ lệ s;
   - dòng tổng 0 nhảy về v;
   - hệ số tắt dần 0,85; dung sai 1e−12; tối đa 1000 vòng;
   - Σs = 0 thì trả `NO_POSITIVE_MASS` và dùng E6a;
   - khóa hòa (π làm tròn 12 chữ số có nghĩa, K_I, K_raw).
4. **Quan hệ dùng.** Cạnh có hướng giữa các nút có F_raw = 1.
5. **Đầu ra.** π gốc và đã làm tròn; thứ tự.
6. **Thiếu dữ liệu.** Nút không cạnh chỉ tự lặp.
7. **Nhánh tắt.** E6a.
8. **Điều kiện thất bại.** Nút sâu nhất hút khối lượng: ví dụ A(0,8) → R(0,6) cho π(R) ≈ 0,833 > π(A) (tính trong bộ nhớ khi soạn bản này). Cạnh sai hướng.
9. **Phép thử.** T9, luật C; C-g, C-c chỉ báo cáo; ô kích hoạt `#/E6b`. KHÔNG ĐỦ CA thì giữ bật (D2a).
10. **Phương án, trạng thái.** Đã xét: biến thể truyền qua nút kế thừa (không có câu hỏi cần); kiểu MicroRank (cần trace bình thường riêng). Ứng viên.

### 7.9 E7 — vùng nghi ngờ

1. **Mục đích:** đáp ứng DT18 ("vùng ảnh hưởng") và ví dụ subgraph của cô; gọi đúng là vùng nghi ngờ.
2. **Đầu vào:** thứ hạng cuối ở thế giới P; F_raw; cạnh. Không nhận nhãn.
3. **Phép tính:** SPEC B2 E7 (D19, D20).
4. **Quan hệ dùng:** đường đi và liên thông trên đồ thị con F_raw.
5. **Đầu ra:** R_r theo từng ứng viên đứng đầu; vùng hợp là đầu ra phụ.
6. **Thiếu dữ liệu:** đồ thị con rỗng thì vùng rỗng.
7. **Nhánh tắt:** top-k, không vùng.
8. **Điều kiện thất bại:** root không có tín hiệu hoặc không có cạnh; hai lỗi độc lập liền kề.
9. **Phép thử:** T10, chỉ mô tả: p của root thuộc vùng; |R| kỳ vọng.
10. **Phương án, trạng thái:** hai cách dựng; mô tả. P/R/F1 vùng chỉ ở FlashTicket (P10).

### 7.10 E8 — cạnh dữ liệu, thông điệp, triển khai

Chỉ FlashTicket; trên dev là UNSUPPORTED (SPEC B2 E8). Mười trường giao SPEC P10 và bảng chuyển giao (`bang-chuyen-giao.json`).

### 7.11 E9 — phủ quyết theo thứ tự thời gian

1. **Mục đích:** công trình khác (KS-10: PAL, FChain, LagRCA).
2. **Đầu vào:** mẫu theo ô 10 giây ở A. Không nhận nhãn.
3. **Phép tính [T-043, làm rõ khởi phát]:**
   - khởi phát của đơn vị u theo hướng d là đầu ô 10 giây đầu tiên trong A mà tỷ lệ mẫu vượt ngưỡng hướng d trong ô lớn hơn r_d(N);
   - kênh e không bị coi là kế thừa khi khởi phát của e sớm hơn khởi phát của mọi đơn vị b dùng để giải thích nó quá 2 ô cộng τ = 1 ms.
4. **Quan hệ dùng:** cạnh dùng ở E5.
5. **Đầu ra:** trạng thái "bị E9 phủ quyết" trong `inherited_by`.
6. **Thiếu dữ liệu:** đơn vị không xác định được khởi phát thì không phủ quyết. Nezha-OB chỉ dùng trace.
7. **Nhánh tắt:** E5 không phủ quyết.
8. **Điều kiện thất bại:** lệch đồng hồ; độ phân giải thô; lỗi mạng (tắt trên cạnh có E2 bất thường).
9. **Phép thử:** T11, luật C; ô kích hoạt `#/E9`.
10. **Phương án, trạng thái:** tùy chọn; ứng viên.

### 7.12 Cạnh tĩnh (T12, D8)

1. **Mục đích:** đáp ứng DT18 (đồ thị từ kiến trúc); bàn giao P5.
2. **Đầu vào:** đồ thị thực thể T-038 (RE2-TT), T-039 (Nezha-OB). Không nhận nhãn.
3. **Phép tính:** hợp cạnh quan sát và cạnh tĩnh; chỉ dùng ở E5, E6b, E7, C-d1, C-d3. Ghép tên chính xác.
4. **Quan hệ dùng:** cạnh tĩnh.
5. **Đầu ra:** cạnh có nguồn "tĩnh".
6. **Thiếu dữ liệu:** nút chỉ có trong mô hình tĩnh vẫn là UNOBSERVED.
7. **Nhánh tắt:** chỉ cạnh quan sát.
8. **Điều kiện thất bại:** revision mô hình tĩnh chưa nối với dataset (T-038, T-039 ghi chưa xác minh runtime).
9. **Phép thử:** T12, luật C; ô kích hoạt `#/T12`.
10. **Phương án, trạng thái:** ứng viên; tác dụng OPEN.

## 8. Đối chứng

Mỗi đối chứng có đủ mười trường. Phép tính theo SPEC B2 bảng đối chứng; ghi thêm phần [T-043].

| Mã | 1. Mục đích, căn cứ | 2–3. Đầu vào, phép tính | 4. Quan hệ dùng | 5–6. Đầu ra; thiếu dữ liệu | 7. Nhánh tắt | 8. Thất bại | 9. Phép thử | 10. Trạng thái |
|---|---|---|---|---|---|---|---|---|
| C-a0 | RQ3d nhánh cùng tín hiệu bỏ quan hệ (WHY-07; DiagMLP) | Tín hiệu của chuỗi cuối; thời lượng cả span theo chủ span, giữ span bọc (D18); K_I = K_raw | Không ở cả bốn chặng | Thứ hạng E6a; như chuỗi | — | Lựa chọn tín hiệu E3, E3b của chuỗi cuối được chọn khi có đồ thị (D23) | T13, chỉ báo cáo | Giữ |
| C-a1 | Bỏ cạnh dịch vụ | Chuỗi cuối bỏ E2, E5, E6b, E7; giữ E1 | Còn cha–con (E1) | Như chuỗi | — | Kết luận chỉ về cạnh dịch vụ | T13 | Giữ |
| C-d1 | Quy tắc "sâu nhất" (M-19) | K_raw; ưu tiên nút không có bên được gọi có F_raw = 1, rồi theo khóa | Cạnh N ∪ A | Thứ hạng | — | Bên được gọi có cờ giả che root | Khối K, T13; chỉ báo cáo | Giữ |
| C-d2 | Quy tắc "sớm nhất" | Khởi phát như E9; sớm hơn đứng trước; hòa theo K_raw | Không | Thứ hạng | — | Độ phân giải thô | T13 nếu cài được [T-043] | Giữ, có điều kiện |
| C-d3 | Traversal (PetShop 2e96f93) | Thẻ đọc PetShop; điểm nút = K_raw,₁; đích theo B2 | Cạnh nhân quả (đảo) | `UNSUPPORTED_CYCLIC`, `NO_TARGET` tính trượt | — | Mục 8 thẻ đọc | Khối K, T13; chỉ báo cáo | Giữ |
| C-c | Gộp baseline không quan hệ (M-26) | RRF k = 60 trên BARO, SimpleRCA M4, TraceRCA lọc hữu hạn; hòa hạng trung bình | Không (ba baseline không dùng quan hệ khi chấm) | ERROR đóng góp 0 | — | Baseline lỗi | T9, T13; chỉ báo cáo | Giữ |
| C-g | Tách tác dụng bước E6b sau bộ chấm mạnh | Phiếu SimpleRCA từ bản ghi P3 (T-024, T-026) | Cạnh N ∪ A | Danh sách = tập SimpleRCA trả; NO_EVIDENCE | — | E5 không áp được | T9, T13; chỉ báo cáo | Giữ |
| C-e | Phép thử giả (MRP §6.7) | Mốc giả t′ = t − 300, chỉ RE2-TT | Như cấu hình được kiểm | Tỷ lệ `CAUSE_FOUND`; mẫu số = cặp không INSUFFICIENT | — | Đoạn trước mốc có thể không sạch | Mọi cặp ở luật C | Giữ |
| C-f | Tham chiếu công nghiệp | Công cụ Grafana | — | — | — | — | Chỉ FlashTicket | Giữ |
| C-h | [T-043] PRISM, tách tự sinh không dùng quan hệ (thẻ đọc PRISM) | Kênh nội bộ = lớp tài nguyên; bên ngoài = độ trễ, lỗi, tỷ lệ thành công, thời lượng cả span; điểm z trên R0; gộp max; M_conj, kèm M_add | Không | Thứ hạng; thực thể không có kênh nội bộ có S^I = 0 | — | Lỗi mạng (root không có lệch nội bộ); tải | T13, chỉ báo cáo | Thêm theo bảng ứng viên SPEC |

**C-d2 [T-043]:** SPEC liệt kê C-d2 ở bảng đối chứng nhưng không đặt ở bước nào của B4. Bản này đặt C-d2 ở T13, chỉ báo cáo, dùng khởi phát của E9. Nếu task cài đặt thấy khởi phát không xác định được ở phần lớn ca, ghi C-d2 là UNSUPPORTED kèm số ca.

**Dung sai đồng hồ (bảng ứng viên SPEC):** không có bước riêng trong B4. Dung sai 1 ms nằm trong E1 (cắt con, happensBefore) và E9 (τ). Bản này không mở phép so riêng; ghi là giới hạn ở `bao-cao.md`.

## 9. Bộ đánh giá

- RR theo ô, P, M, MRR theo dataset và gộp: `dinh-nghia-pha2.json#/rr_theo_o`.
- Luật C, luật chọn khối, điều kiện riêng E5, vế mốc giả, phụ thuộc quan sát: giữ nguyên SPEC Phụ lục C và B4. Fixture 34–40, 45–54, 56, 60 kiểm luật.
- WORLD_DEPENDENT: bộ đánh giá tính sau ghép nhãn (SPEC B1.3b).
- Báo kèm, không quyết định: p kiểm dấu; khoảng tin cậy bootstrap theo ô (`danh_gia.bootstrap`, B = 10.000, seed 20261005); kết cục ở δ = 0,005 và 0,02.

## 10. Ô kích hoạt, kiểu quan sát O1–O4, hình dạng xếp hạng

Định nghĩa đầy đủ ở `dinh-nghia-pha2.json`, băm vào LOG phiên 7 trước pha 2. Không sửa sau khi thấy số ô. Kết quả đếm ở `ks16/dem-sau-ghep-nhan.json`.

## 11. Giao diện cho P8 và P9 (tóm; chi tiết ở `hop-dong.json#/goi_bang_chung`)

- **Gói bằng chứng cho P8:** thứ hạng kèm khóa; đồ thị con bất thường; vùng R_r; `inherited_by`; kênh lệch nhất theo thực thể; vài dòng log tiêu biểu theo mẫu; `coverage`; `worlds`; `verdict`. LLM không đổi thứ hạng (MRP P8).
- **Yêu cầu cho P9:**
  - định dạng nội bộ chung (WHY-08);
  - siêu dữ liệu thu thập theo B16 mục 8, để có trạng thái XÁC NHẬN CÓ QUAN SÁT và XÁC NHẬN THIẾU THU;
  - trace_id trong log;
  - kind của span;
  - danh tính DB, MQ, host (R-01–R-10).

## 12. Điều còn mở

- A0; giả định mẫu độc lập ở cổng; bảng lớp lan (đặc biệt "tần suất tăng": retry hay tải vào); nghĩa vật lý của cạnh (O03).
- Hiệu quả của mọi thành phần.
- Các lựa chọn [T-043] ở mục 2.2, 3, 5, 6, 7.3b, 7.11, 8 cần Codex phản biện. Lý do của lựa chọn đáng kể ghi ở `why-de-xuat.md`.
