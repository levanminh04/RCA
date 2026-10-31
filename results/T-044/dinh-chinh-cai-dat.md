# Đính chính khi cài đặt — T-044

Theo Q-209 mục 8: lỗi hoặc chỗ mơ hồ của đặc tả lộ ra khi cài được ghi ở đây, kèm đáp án, chờ Minh duyệt; không mở lại T-043.

- **Phần I** gồm các đính chính người làm đề xuất sau khi tự rà SPEC. Minh duyệt toàn bộ trong chat ngày 29/10/2026 ("duyệt toàn bộ các đề xuất bên trên của bạn"). Chi tiết lập luận và bằng chứng ở `tasks/T-044-cai-dat-m1/LOG.md`, phiên 1: mục "Tự rà SPEC", "Lượt 2" và "Lượt 2, phần bổ sung".
- **Phần II** gồm các chỗ lệch lộ ra trong lúc cài. Mỗi mục ghi trạng thái; mục chưa được Minh quyết thì phần phụ thuộc dừng.
- Đáp án tự lập ở `results/T-044/fixture/dap-an-doi-chung.json`, `dap-an-thanh-phan.json`, `dap-an-van-ban.json` mang dấu "đáp án của người làm T-044, chưa qua phản biện" (Q-212, N1 mở rộng).
- Dòng DECISIONS cho các duyệt này chưa ghi; người làm đề xuất ở cuối phiên.

## Phần I — đã duyệt (29/10/2026)

### CĐ1. E1-CP là một chế độ của E1 (R2)

- Giá trị `params.bat_tat.E1 = "CP"` (đã có trong `hop-dong.json` dòng 13). Không thuộc ma trận dev; K-b không chạy E1-CP (Q2 của SPEC T-043; đặc tả v1 dòng 186).
- Cách tính theo thẻ CRISP (`results/T-043/the-doc/crisp.md`, §5.1–5.2 của bài) và đặc tả v1 dòng 171:
  - con được cắt về [s₀, s₁) của cha ở cả hai đầu; con nằm hẳn ngoài cha bị bỏ khỏi phép tính của cha (giống E1-U);
  - đường găng: lấy con kết thúc cuối (LFC); bỏ qua các con bắt đầu hay kết thúc trong khoảng của LFC; tìm con c có happensBefore(c, LFC), chọn con kết thúc muộn nhất; lặp tới hết;
  - happensBefore(c, d) khi c_end − 1 ms < d_start và không con nào khác của cùng cha bắt đầu hay kết thúc trong vùng chồng lấn;
  - u = d − |hợp các con trên đường găng đã cắt|; hợp khoảng nên u không âm.
- Ca tự lập (tính tay): cha [0; 100); con [10; 40), [20; 60), [65; 90) cùng đơn vị. Đường găng gồm [65; 90) và [20; 60). u_CP = 35; u_U = 25.

### CĐ2. Điều kiện riêng UV-6 của E3 (R3)

Cho cặp (c bỏ E3, c), tính trong từng thế giới P, S_lo, S_hi, trên cả 52 ca gộp (đúng câu chữ `ma-tran-thu.json#/dieu_kien_rieng/E3`):
- **ca đang đúng:** Hit@1(c bỏ E3) = 1 (kỳ vọng theo quy tắc hòa của WHY-28; tức root một mình ở hạng 1);
- **ca bị hỏng:** ca đang đúng mà Hit@1(c) < 1, kể cả khi root rơi vào hòa ở đầu;
- **ca được sửa:** loại lỗi thuộc nhóm lỗi mã (Nezha-OB {return, exception}; `dinh-nghia-pha2.json#/o_kich_hoat/E3`), Hit@1(c bỏ E3) < 1 và Hit@1(c) = 1. Loại lỗi là nhãn, chỉ đọc ở pha 2;
- **vi phạm** khi số ca bị hỏng lớn hơn số ca được sửa. Ca không OK có Hit@1 = 0 (WHY-28), nên không thể là ca đang đúng.
- Báo kèm, không dùng để quyết: số theo từng dataset; bản theo Hit@1 kỳ vọng (Σ phần giảm ở ca đang đúng so với Σ phần tăng ở ca lỗi mã); số ca lỗi mã có root lên hạng.
- Chỉ áp cho cặp khác nhau đúng thành phần E3 (xem CĐ6.4).

### CĐ3. Nhóm vòng của E5 (R4)

Câu gốc (đặc tả v1 dòng 308; SPEC T-043 dòng 671): "trong SCC của đồ thị con F_raw (D19), chỉ được giải thích bởi thành viên có bất thường không lan, hoặc bởi bên được gọi ngoài SCC".

- **Cách đọc chính (C′), co vòng:** với S là một nhóm vòng (SCC có ít nhất hai nút) của đồ thị con F_raw, và e ∈ S:
  - kênh lan ngược của e là kế thừa khi có thành viên m ∈ S, m ≠ e, có kênh F_raw = 1 lớp không lan (E1, E2, tài nguyên tăng); hoặc có b ∉ S mà một thành viên nào đó của S gọi, và b có kênh F_raw = 1 thuộc lớp giải thích được của luật chung (lan ngược, E1, E2, tài nguyên tăng, thao tác mới);
  - kênh lan xuôi của e là kế thừa khi có thành viên m ≠ e có kênh F_raw = 1 lớp không lan; hoặc có a ∉ S gọi một thành viên của S, và a có kênh F_raw = 1 bất kỳ;
  - thành viên khác trong S chỉ giải thích được qua kênh lớp không lan.
- **Cách đọc chẩn đoán (A), kề cạnh**, chỉ dùng cho D5 của T-045, không vào ma trận: kênh lan ngược của e được bên được gọi trực tiếp b giải thích theo luật chung nếu b ∉ S; nếu b ∈ S thì chỉ khi b có kênh F_raw lớp không lan. Kênh lan xuôi đối xứng, với bên gọi trực tiếp a.
- **Điều kiện thất bại thêm của (C′):** một cờ không lan yếu ở một thành viên xa vẫn xóa được bằng chứng mạnh của root nằm trong vòng (cùng loại fixture 57, tầm rộng hơn).
- Dữ kiện dev (không nhãn): RE2-TT có nhóm vòng {ts-seat-service, ts-travel-service, ts-travel2-service} ở 24/30 ca trên đồ thị gọi đầy đủ (`results/T-043/ks16/dem-khong-nhan.json#/cases/*/call_rows`); Nezha-OB 0/22. Số ca E5 gặp vòng trên đồ thị con F_raw chưa biết.

### CĐ4. Đường xử lý log của E3 (R5) — có một đổi thiết kế

1. **Chuỗi đưa vào Drain:**
   - Nezha-OB: lấy chuỗi `log` của JSON ngoài; nếu `log` giải mã được thành JSON object có khóa `message` kiểu chuỗi thì dùng `message`, không thì dùng `log`; JSON ngoài không giải mã được thì dùng nguyên chuỗi. Quy tắc không gọi tên dịch vụ (WHY-08) và cho cùng kết quả với `log_parsing.py` dòng 94–127 của Nezha (commit `d8140101fdb4`). Việc này thuộc adapter; `severity_raw` giữ đường đọc của `hop-dong.json` dòng 69;
   - RE2-TT: cột `message` nguyên văn.
2. **Khớp dòng A với mẫu học từ N** (`params.tham_so_E3.khop`). Theo Đ15 điểm 5, cả ba cách chỉ xét **mẫu đã biết của chính thực thể** (mẫu có ít nhất một dòng N của thực thể đó):
   - (a) `"hoan_toan"` — mặc định: khớp hoàn toàn như `Drain.match(…, full_search_strategy="fallback")` của drain3 0.9.11 ("Match shall be perfect (sim_th=1.0)", `drain3/template_miner.py` dòng 149–166): đi cây tiền tố rồi `fast_match` với sim_th = 1,0 và tham số `<*>` khớp mọi token; không thấy thì tìm hết các mẫu cùng số token;
   - (b) `"nguong"`: như `Drain.tree_search` (đi cây tiền tố, rồi `fast_match` với sim_th của E3, không tính tham số); không cập nhật mẫu;
   - (c) `"nguong_cung_lop"`: như (b) nhưng chỉ xét các mẫu cùng lớp với dòng, lớp lấy theo cặp (thực thể, mẫu): dòng lỗi chỉ khớp mẫu lớp lỗi; dòng không lỗi chỉ khớp mẫu lớp thường; dòng UNKNOWN khớp mọi mẫu đã biết. Đây là cơ chế mới, chưa có prior work; nếu được chọn ở T-045 thì cần WHY;
   - không khớp thì dòng vào ô "mẫu mới" của thực thể. Mọi cách khớp không học thêm từ A.
3. **Che token (đổi thiết kế: bỏ "chuỗi trong ngoặc" của đặc tả v1 dòng 227 và SPEC T-043 dòng 636):** che theo thứ tự, với ranh giới không dính chữ hoặc số (`(?<![A-Za-z0-9])…(?![A-Za-z0-9])`):
   - UUID 8-4-4-4-12 chữ số hex → `<UUID>`;
   - IPv4, cổng tùy chọn → `<IP>`;
   - `0x` theo sau ít nhất một chữ số hex, hoặc chuỗi hex dài ≥ 8 có ít nhất một chữ số và ít nhất một chữ a–f → `<HEX>`;
   - số nguyên hoặc thập phân, có dấu tùy chọn → `<NUM>`;
   - tắt phần che sẵn của drain3 (không có masking instruction).
   - Lý do bỏ che ngoặc: TrainTicket v1.0.0 trong repo (`results/T-038/sources/train-ticket-v1.0.0/`) ghi log dạng `[method][…][…][…]`; che nội dung trong ngoặc gộp mọi thông điệp cùng số nhóm ngoặc thành một token, gộp cả dòng lỗi với dòng thường. Chưa xác nhận RE2-TT chạy đúng bản này.
4. **Thứ tự học:** mọi dòng N quan sát được của thế giới đang tính, của mọi thực thể, đưa vào **một Drain chung** (Đ15 điểm 5: "Drain học chung cho mọi thực thể"), theo thứ tự (mốc ns, thực thể, nội dung). Đơn vị phân loại và kênh là cặp (thực thể, mẫu) (Đ15 điểm 2).
5. **Ngưỡng:** giữ sim_th = 0,4, độ sâu 4 (đặc tả v1 dòng 228). Chưa có WHY; người làm soạn và trình riêng.
6. **Tham số drain3 còn lại:** mặc định 0.9.11 (`drain3/drain.py` dòng 54–61): max_children 100, max_clusters không giới hạn, extra_delimiters rỗng, parametrize_numeric_tokens True.

### CĐ5. Hồ sơ nguồn và tham số E3 trong hợp đồng (R6)

Đính chính hợp đồng theo cách Đ19 đã làm; không sửa `hop-dong.json`.
- `params.ho_so_nguon` = {
  - `kenh_metric`: {`kieu`: "hau_to" | "ten_kenh", `bang`: {khóa → lớp}};
  - `quy_tac_log`: {`kieu`: "tu_khoa", `tu_khoa`: [...], không phân biệt hoa thường, tìm chuỗi con} hoặc {`kieu`: "severity", `loi`: [...], `khong_loi`: [...]};
  - `nguon_khoi_phat`: danh sách nguồn dùng cho khởi phát E9 }.
- Giá trị:
  - RE2-TT: 8 hậu tố của `hop-dong.json` dòng 55; từ khóa ERROR, FAIL, EXCEPTION (`src/simplerca/core.py:22`, regex IGNORECASE ở dòng 87); khởi phát từ trace và metric;
  - Nezha-OB: 21 tên kênh của dòng 61; severity theo dòng 69; khởi phát chỉ từ trace (đặc tả v1 dòng 379).
- Runner điền từ `hop-dong.json`. Thiếu khóa hoặc gặp lớp không có trong bảng thì bản ghi ERROR; không suy từ dữ liệu. Bảng lớp → hướng → lớp lan (`hop-dong.json#/kenh/lop_huong`) như nhau cho mọi dataset, nên nằm trong lõi.
- `params.tham_so_E3` = {`khop`: "hoan_toan" | "nguong" | "nguong_cung_lop", `sim_th`: 0,4, `do_sau`: 4}; tham số drain3 còn lại theo CĐ4 mục 6.
- `params.tham_so_E5` = {`doc_nhom_vong`: "co_vong" (C′, mặc định) | "ke_canh" (A, chỉ chẩn đoán)}.

### CĐ6. Đáp án tự lập và các định nghĩa đi kèm (R7)

1. **Cờ M5** (điều kiện riêng E5): theo `results/T-028/codebook.md` §5 bảng nhãn (dòng 95): có e ≠ root với đường e → root trong G_N và e chắc chắn đứng trước root. G_N theo codebook §4 (dòng 72): cạnh caller → callee từ cha–con cùng trace, chỉ khi cả span cha lẫn span con thuộc N. Đếm với k = 1.
2. **Phụ thuộc quan sát:** theo SPEC T-043 Phụ lục C và D2f ("phụ thuộc quan sát" xử lý như KHÔNG ĐỦ CA); đáp án tự lập cho cả cặp và luật chọn khối bước 10.
3. **Bước 8 luật chọn khối ("mâu thuẫn với lựa chọn"):** với cấu hình thắng w và mỗi thành phần x của khối, đảo x trong cùng bối cảnh; xét cặp (w không có x, w có x) theo luật C:
   - x đang bật: GIÚP hoặc KHÔNG ĐỦ CA (D2a) là nhất quán; HẠI hoặc KHÔNG TÁC DỤNG là xung đột;
   - x đang tắt: HẠI hoặc KHÔNG TÁC DỤNG là nhất quán; GIÚP là xung đột; KHÔNG ĐỦ CA là xung đột với D2a;
   - TRÁI CHIỀU: chưa phân xử, trình Minh. "Phụ thuộc quan sát" xử lý như KHÔNG ĐỦ CA (D2f).
   - Xung đột chỉ được báo; không tự thay cấu hình thắng (SPEC T-043 dòng 807; bảng mặc định SPEC T-045).
4. **Cặp (R0, c) ở bước 4 luật chọn khối:** chỉ áp các vế không gắn với thành phần nào: mốc giả; M + M′ ≥ 3 và P + P′ = 0; TRÁI CHIỀU theo dataset; HẠI gộp. E_X của cặp là hợp các E_X của thành phần đang bật trong c. UV-6 và điều kiện M5 chỉ áp cho cặp khác nhau đúng một thành phần (E3, E5), vì ở (R0, c) số ca hỏng hay số cờ M5 có thể đổi do thành phần khác.
5. Các phần khác có đáp án tự lập: UV-6 (CĐ2), nhóm vòng cả hai cách đọc (CĐ3), che token và ba cách khớp (CĐ4), E1-CP (CĐ1), E7 (CĐ8), E9 (CĐ9), T4c (CĐ7), đối chứng C-a1, C-d1, C-d2, C-c (N1 gốc).

### CĐ7. T4c (R9)

- Khóa T4c: K′ = (max s, max m, số kênh, Σs), trên đúng tập kênh của khóa đang dùng (F_raw cho K_raw, F_I cho K_I).
- m của một đơn vị có cờ:
  - đơn vị phân vị: m = log(1 + |trung vị A − trung vị N| / max(|trung vị N|, r_u)); r_u là hiệu dương nhỏ nhất giữa hai giá trị khác nhau trong N ∪ A của đơn vị; nếu mọi giá trị bằng nhau thì m = 0;
  - đơn vị đếm: λ = n/T; m = log(1 + |λ_A − λ_N| / max(λ_N, r_u)), r_u = 1/T_N.
- Lý do đặt m ngay sau max s: mục đích của T4c là phân biệt độ lớn khi E4 bão hòa (SPEC T-043 dòng 408–409); đặt ở cuối chỉ phá hòa tuyệt đối. Lý do có m cho đơn vị đếm: đơn vị đếm cũng bão hòa (n_N = 0 cho e_up = 1, đặc tả v1 dòng 119; ô "mẫu mới" luôn có n_N = 0).
- T4c là thứ tự thứ hai, ghi trong cùng bản ghi pha 1 của lượt R0 mặc định (ε = 0,05; α = 0,01); không chấm lại; T4 vẫn là 9 cấu hình (`ma-tran-thu.json` dòng 34).

### CĐ8. Vùng E7, cách 1 (R9)

Trên đồ thị con F_raw (D19), với mỗi ứng viên r ∈ T:
- R_r = {r} ∪ Lên ∪ Xuống;
- Lên = {a ≠ r: có đường a → … → r, và mọi kênh F_raw = 1 của a đều "có giải thích"};
- Xuống = {b ≠ r: có đường r → … → b, và b có ít nhất một kênh F_raw = 1 lớp lan xuôi "có giải thích"};
- "có giải thích": kênh có mục trong `inherited_by` với trạng thái "đề xuất" (E5 tắt) hoặc "áp dụng" (E5 bật) (`hop-dong.json` dòng 26); trạng thái "bị E9 phủ quyết" không tính.
- Cách 2 (biến thể): thành phần liên thông vô hướng chứa r của đồ thị con F_raw.
- E5 tắt vẫn tính các giải thích ở trạng thái "đề xuất", vì E7 chỉ mô tả và không đổi thứ hạng.

### CĐ9. E9 (R9)

- Lưới ô 10 giây đặt từ t về hai phía. Mẫu vào ô theo end của span, hoặc theo mốc thật của nguồn metric. Ô không có mẫu bỏ qua.
- Khởi phát của đơn vị u theo hướng d: đầu ô đầu tiên trong A mà tỷ lệ mẫu vượt ngưỡng hướng d trong ô lớn hơn r_d(N) (đặc tả v1 dòng 375). Chỉ tính cho hướng có cờ. Đơn vị phân vị đã có cờ thì luôn có khởi phát, vì r_d(A) > r_d(N) buộc ít nhất một ô vượt r_d(N). Đơn vị không tính được khởi phát (đơn vị đếm, nguồn ngoài `nguon_khoi_phat`) thì không phủ quyết.
- Phủ quyết: kênh e không bị coi là kế thừa khi khởi phát của e sớm hơn khởi phát của mọi đơn vị b dùng để giải thích nó quá 2 ô cộng τ = 1 ms.
- "Tắt trên cạnh có E2 bất thường" chỉ áp khi E2 bật: cạnh dùng để giải thích có đơn vị E2 với F_raw,lên = 1 thì không phủ quyết. Khi E2 tắt không tính E2 ngầm, vì thành phần đang tắt không được đưa thông tin vào đường tính thứ hạng.

### CĐ10. Đối chứng C-d1 (R9)

- Nhóm 1: thực thể có K_raw,₁ > 0 mà không có bên được gọi nào có K_raw,₁ > 0 (cạnh N ∪ A, cộng cạnh tĩnh khi T12 bật); nhóm 2: các thực thể có cờ còn lại; nhóm 3: tầng 3 (không cờ). Trong nhóm xếp theo K_raw; hòa theo khóa chính xác.
- C-d1, C-d3 tính lại trên kết quả chấm của từng cấu hình; không phải cấu hình riêng.

### CĐ11. Adapter và mốc t (R8)

- Adapter dữ liệu dev → API M1 viết trong `src/m1` (RE2-TT qua `src/p3/selector.py`, `cua_so.py`; Nezha-OB qua `src/p3/nezha.py`).
- Runner nhận bảng mốc {mã mờ: t} làm đầu vào, không tự đọc file nhãn. T-045 tạo bảng bằng `p3.nhan.nap_moc` trong `results/T-045/`, như KS-16 (`results/T-043/ks16/ks16_pha1_v11.py` dòng 735).
- T-044 kiểm adapter trên bộ dữ liệu tổng hợp nhỏ do test sinh trong thư mục tạm, đi đúng đường đọc của `src/p3`.

### CĐ12. Chặn rò nhãn ở mức giá trị (R11)

Trước khi gọi phương pháp, runner kiểm không chuỗi mã mờ hay `case_dir` nào xuất hiện như giá trị (kể cả chuỗi con) trong `params`, `aliases`, `inventory`. Có test và một đột biến tương ứng.

### CĐ13. Giao diện bộ đánh giá cho T-045 (R12)

- Luật C và luật chọn khối nhận trọng số ca (bội số của ô) và δ_d cố định làm tham số.
- Bản ghi lưu chi tiết từng đơn vị theo thế giới: trạng thái, p, e, n_N, n_A, T_N, T_A (cho Đ5).
- Test: trọng số 2 cho một ô cho cùng kết quả như nhân đôi các ca của ô đó.

### CĐ14. Test bổ sung (R13)

- Các đáp án nằm trong văn bản (Đ10, đặc tả v1 dòng 349, SPEC T-043 dòng 392, Đ17) thành test; đầu vào người làm bổ sung được đánh dấu.
- Chạy đầu-cuối từ span cho S1–S7 với `fixture-dac-ta.json#/trace_mau_S`; đáp án vẫn là đáp án của fixture 1. Đầu vào người làm bổ sung, đánh dấu rõ: S3 (R trả lỗi nhanh, có dòng INFO ở cả N và A), S6 (span gốc R.newop chỉ có ở A), S7 (R không có span; span của X mồ côi).

### CĐ15. Môi trường (R14)

pyarrow 18.1.0 (bản T-043 đã dùng, `results/T-043/manifest.json#/runtime/parquet`). `requirements-m1.txt` đúng danh sách SPEC; `freeze-m1.txt` ghi đủ gói đã cài.

### CĐ16. Tự diễn giải áp dụng trong phạm vi (đã trình ở mục C của LOG)

- Sai số so đáp án: phân số hoặc số hữu tỉ ≤ 1e−12; số thập phân đã làm tròn trong fixture: lệch không quá nửa đơn vị của chữ số cuối đã ghi; thứ hạng, trạng thái, tập: khớp tuyệt đối.
- RR, MRR, ΔMRR tính bằng phân số chính xác để so đúng tại biên δ, δ_d.
- Tất định: Σs bằng `math.fsum`; tập, đồ thị, thứ tự nút sắp theo tên; hash pha 1 trên JSON chuẩn hóa (khóa sắp, không có trường thời gian hay mã lượt).
- Bản ghi cùng schema với `ban_ghi.tao` để `src/p3/danh_gia` đọc được, nhưng không gọi `ban_ghi.tao` hay `ban_ghi.kiem`.
- Khi E3 bật, kênh mẫu Drain thay kênh log lỗi cơ bản (`hop-dong.json` dòng 51).
- `params.coverage`: `khoang` = [mốc bản ghi đầu, mốc bản ghi cuối] của từng file; M1 cộng r_ns; danh sách rỗng là XÁC NHẬN THIẾU THU; thiếu khóa là UNSUPPORTED (Đ19 điểm 4).

## Phần II — chỗ lệch lộ ra khi cài (ghi 29/10/2026; mục A đã duyệt 29/10/2026)

- **Trạng thái mục A:** Minh duyệt giữ cả 20 cách hiểu, lời trong chat ngày 29/10/2026: "DUYỆT 20 ĐIỂM". Không đổi code.

**Tóm tắt.** Không có fixture hay đáp án nào của T-043 lệch với code: 97/97 phép kiểm trong phạm vi qua mà không sửa đáp án. Không có đáp án đặc tả nào cần đính chính. Phần này gồm các chỗ đặc tả không nói hoặc nói chưa đủ, nơi người làm phải chọn một cách hiểu để viết code (mục A, cần Minh quyết), các quy ước biểu diễn không đổi kết quả (mục B, để người phản biện kiểm), các sửa đã làm trong phiên theo đúng nguồn (mục C) và giới hạn (mục D). Theo tiêu chí 8 của SPEC, task ở trạng thái "chờ Minh" cho tới khi Minh quyết mục A; Minh đã quyết (dòng trạng thái ở đầu phần này).

### A. Cách hiểu đã cài ở chỗ đặc tả không nói (đã duyệt 29/10/2026)

Mỗi mục: chỗ; đã cài; phương án khác; ảnh hưởng. Đề xuất chung: giữ cách đã cài, trừ khi Minh chọn khác.

- **PII-01. Cổng qua khi p < α (chặt).** Đặc tả v1 và SPEC T-043 B1.3 không ghi ≤ hay <. Đã cài `<` cho đơn vị phân vị và đơn vị đếm, như KS-16 pha 2 (`results/T-043/ks16/ks16_pha2_v11.py` dòng 160) và E3b ở `dinh-nghia-pha2.json`. Phương án khác: ≤. Ảnh hưởng: chỉ khi p đúng bằng α; không fixture nào rơi vào biên, nên đột biến ≤ không bị test bắt (mục D).
- **PII-02. E9 tắt trên cạnh có E2 bất thường.** SPEC T-043 B2 E9 ghi "tắt trên cạnh có E2 bất thường". Đã cài: khi E2 bật, nếu bất kỳ cạnh nào trên bất kỳ đường giải thích nào của kênh (theo cả hai chiều) là cạnh có F_raw,lên = 1 ở đơn vị E2, thì không phủ quyết; `inherited_by` ghi lý do `tat_tren_canh_E2`. Phương án khác: chỉ xét cạnh trực tiếp giữa e và bên giải thích. Ảnh hưởng: chỉ khi E2 và E9 cùng bật (T11).
- **PII-03. Khởi phát của kênh E2-VC.** Đặc tả chỉ định nghĩa khởi phát cho đơn vị phân vị. Kênh `E2VC:v` gộp nhiều cạnh; đã cài khởi phát là khởi phát của cạnh có điểm lớn nhất (hòa theo tên cạnh), như cách lấy điểm của kênh. Phương án khác: khởi phát sớm nhất trong các cạnh đỉnh phủ. Ảnh hưởng: E9 và C-d2 khi E2-VC bật.
- **PII-04. Phá hòa của đường găng CRISP.** Thẻ CRISP không nói khi hai con cùng kết thúc. Đã cài: LFC là con kết thúc muộn nhất, hòa thì con bắt đầu muộn hơn; trong các ứng viên happensBefore chọn con kết thúc muộn nhất, rồi bắt đầu muộn nhất. Ảnh hưởng: chỉ E1-CP (không vào ma trận dev).
- **PII-05. Đếm con vượt biên cha.** Đã cài: đếm khi con bắt đầu trước cha hoặc kết thúc sau cha quá τ = 1 ms, ở một đầu bất kỳ (fixture 4, 5 chỉ có một đầu). Chỉ là chẩn đoán, không đổi điểm.
- **PII-06. Trạng thái NO_DATA của đơn vị phân vị.** `hop-dong.json#/trang_thai/don_vi` chỉ có OK, LOW_SUPPORT, NO_BASELINE, NO_A. Đơn vị không có giá trị hữu hạn nào ở cả N và A được ghi NO_DATA. Không đổi xếp hạng (không hợp lệ như các trạng thái khác OK).
- **PII-07. Vùng E7 của ứng viên không có kênh cờ.** Khi ứng viên r thuộc nhóm hòa đầu nhưng không có kênh F_raw = 1 (ví dụ mọi thực thể ở tầng 3), r không nằm trong đồ thị con nút có cờ; đã cài R_r = ∅. Phương án khác: R_r = {r}. Ảnh hưởng: chỉ mô tả ở T10.
- **PII-08. Cờ M5 "đứng trước hẳn" trên khối của M1.** Codebook T-028 §4 định nghĩa cho từng loại phương pháp; đã cài theo luật của TORAI vì M1 cũng ghi khối: khối của e có khóa lớn hơn khối của root, hoặc cùng khối và nhóm của e đứng trước. Khối khác nhưng cùng khóa, hay cùng nhóm, không tính. Root không được trả về thì không có cờ.
- **PII-09. Giá trị metric không hữu hạn.** Đặc tả v1 dòng 110 chỉ nói hỗ trợ tính trên giá trị hữu hạn. Đã cài: bỏ giá trị không hữu hạn ngay khi gom mẫu, nên cũng không vào khởi phát E9, T4c, nhánh z. Adapter đổi NaN, ±inf thành None.
- **PII-10. Đích của C-d3.** SPEC T-043 B2 ghi "span gốc của trace trong A". Đã cài: span gốc (parent rỗng) có end ≥ t, cùng luật chia N/A của span. Phương án khác: trace có ít nhất một span ở A.
- **PII-11. C-d1, C-d2, C-d3 tính trên thế giới P của từng cấu hình** và ghi vào `extra.doi_chung` của bản ghi (CĐ10 nói "tính lại trên kết quả chấm của từng cấu hình"). Khởi phát cho C-d2 luôn được tính; E5 chỉ dùng khi E9 bật. Phương án khác: chỉ tính ở chuỗi cuối.
- **PII-12. C-g với phiếu ngoài tập trả về.** SPEC ghi "không thêm thực thể ngoài đầu ra gốc". Đã cài: thực thể có phiếu nhưng không nằm trong danh sách SimpleRCA đã trả thì bị bỏ; nhóm điểm 0 là mọi thực thể đã trả có 0 phiếu, nối ở cuối thành một khối.
- **PII-13. Mẫu số C-e khi bản ghi lỗi.** SPEC: mẫu số là cặp mà cả hai nhánh khác INSUFFICIENT_EVIDENCE. Bản ghi ERROR không có verdict; đã cài loại cặp đó khỏi mẫu số và đếm vào số bị loại (`pha2.dem_moc_gia`). Phương án khác: giữ cặp, coi là không báo. Ảnh hưởng: chỉ khi lượt mốc giả có bản ghi lỗi.
- **PII-14. Danh sách T13 và C-e.** `ma-tran-thu.json#/buoc/<T13>` có 9 mục với "+ 8 đối chứng"; Đ16 bỏ C-h và đổi thành "+ 7 đối chứng" nhưng vẫn còn 8 mục. Đã cài: 7 đối chứng là C-a0, C-a1, C-d1, C-d2, C-d3, C-c, C-g; C-e là vế mốc giả, không là cấu hình riêng (căn cứ: `dinh-chinh-phien10.md` dòng 73 tách "vế mốc giả C-e"). C-a0, C-a1 chạy M1; C-d1, C-d2, C-d3 đọc từ bản ghi chuỗi cuối; C-c, C-g tính từ bản ghi P3. Ảnh hưởng: số cấu hình của T13 (RUN1: 13).
- **PII-15. Nền của T6, T9, T11, T12 và KB.** Runner không biết quyết định của bước trước khi sinh cấu hình. Mặc định đã cài: T6 dựa trên cấu hình thắng sau K-b; T9 thêm E3b theo chuỗi cuối; T11 thêm E6; T12 thêm E9; có tham số `nen` để T-045 truyền nền thật. KB bật lại một thành phần đang tắt bằng biến thể của khối K (E1-U, E2-C). K-b: cấu hình thắng không có E2 thì chỉ còn biến thể của cấu hình đầy đủ; trùng nhau thì giữ một.
- **PII-16. δ_d khi có trọng số ca.** Mặc định δ_d = 1/n_d với n_d là số ca của dataset trong danh sách đưa vào (không trọng số). Khi dùng trọng số, T-045 phải truyền δ_d cố định (CĐ13); test trọng số dùng cách này.
- **PII-17. Cờ trái chiều theo dataset trong luật chọn khối.** Bước 6 nói cờ "nằm ở cấu hình". Đã cài: cờ của cặp (a, b) gắn cho b, cấu hình có thêm thành phần, như lượt một gắn HẠI cho b. Cặp đảo tại cấu hình thắng đã được bước 8 xét riêng (TRÁI CHIỀU thì trình Minh). Phá hòa "E1, E2, E5, E3" với tên thành phần khác bốn tên này: xếp sau, theo thứ tự khai báo. Cấu hình có đồ thị tốt nhất (bước 8): MRR cao nhất, rồi ít thành phần.
- **PII-18. Lỗi mã của UV-6** đọc là: dataset Nezha-OB và loại lỗi thuộc {return, exception} (`dinh-nghia-pha2.json#/o_kich_hoat/E3`: RE2-TT không có loại lỗi mã). "Lên hạng" là hạng kỳ vọng giảm.
- **PII-19. Cột metric không khai nguồn.** Đ19 điểm 3 chỉ cho dùng `metrics.time` khi adapter xác nhận. Đã cài: cột không có trong `params.nguon_metric` không được chấm và ghi vào `diagnostics.cot_metric_chua_khai_nguon`. Phương án khác: bản ghi ERROR.
- **PII-20. Adapter.** RE2-TT: span có parent rỗng hoặc vắng là span gốc; mốc log giữ nguyên số; `message` đổi sang chuỗi. Nezha-OB: trace guard 0 như KS-16 pha 1; mã nguồn metric là `metric:<dịch vụ>`, riêng file front là `metric:front_service` (không đưa đường dẫn vào params, luật cứng 6); F của metric theo từng file (metric không tham gia T). Chuỗi cấm của runner gồm mã mờ, case_dir, tên thư mục ca, mọi đường dẫn tệp và tên file phút của Nezha-OB.

### B. Quy ước biểu diễn (không đổi kết quả; để người phản biện kiểm)

- Tên kênh E2: `E2:a->b` (E2-C, cạnh không định danh) và `E2VC:v` (đỉnh định danh). Cạnh nối hai đỉnh định danh ghi gán cho bên được gọi; cả hai đỉnh tính cạnh này vào điểm của mình (`src/m1/e2.py`).
- `inherited_by`: một mục cho mỗi kênh giải thích; đường là đường ngắn nhất (BFS, láng giềng theo tên) trong nhóm vòng.
- Khóa khối: E6a (3 − tầng, K); E6b (π làm tròn 12 chữ số có nghĩa, K_I, K_raw); T4c (3 − tầng, max s, max m, số kênh, Σs); C-d1 (3 − nhóm, K_raw); C-d2 (1, −khởi phát, K_raw) hoặc (0, 0, K_raw); C-d3 (điểm); C-c (điểm RRF); C-g nhóm điểm 0 có khóa (0, 0), Σs_g = 0 dùng khóa giảm dần theo vị trí. Khóa chỉ để `src/p3/danh_gia` đọc thứ tự và hòa.
- Nguyên nhân của WORLD_DEPENDENT (fixture 29) ghi dạng cấu trúc: loại (cổng đổi hay chỉ điểm đổi) và cặp (thực thể, kênh mạnh nhất).
- Trong test luật C, khi đáp án không phụ thuộc ô nào thuộc E_X, hàm dựng E_X đưa các ô có ca đổi vào trước rồi thêm ô khác cho đủ số.
- Bản ghi NO_EVIDENCE khi không có thực thể nào được xếp, như quy ước của `ban_ghi.tao` (OK cần danh sách khác rỗng).
- Bản ghi thêm `extra.doi_chung`, `extra.T4c`, `extra.kenh_co`, `extra.kenh_co_the_gioi` (kênh có cờ trong U theo từng thế giới, cho giải thích WORLD_DEPENDENT ở pha 2), `extra.thong_ke_log` (C3, S9), `extra.G_N`, `extra.don_vi_phan_vi`, `worlds.*.don_vi_dem.*.loai_thay_doi` (tên `nhan` là trường cấm). Không trường nào chứa nhãn.
- Mã ô của luật C phải duy nhất giữa hai dataset (hàm báo lỗi nếu trùng).

### C. Sửa đã làm trong phiên (theo đúng nguồn; ghi để kiểm)

- Chuỗi trước đây dùng `metrics.time` cho cột không khai nguồn: trái Đ19 điểm 3; đã đổi như PII-19.
- Bản đầu của adapter đưa đường dẫn tệp metric Nezha-OB vào `params.nguon_metric`: trái luật cứng 6; đã đổi như PII-20. Tệp front và tệp pod frontend từng cùng mã nguồn; đã tách.
- Phép tất định lộ hai phụ thuộc thứ tự: `e2.gan_canh` trả danh sách theo thứ tự đầu vào; `e5.phan_loai` ghi `inherited_by` theo thứ tự kênh đầu vào. Đã sắp theo (bên gọi, bên được gọi) và theo mã kênh (`runs/tat-dinh-000-truoc-sua/ghi-chu.md`).
- Thiếu đáp án tự lập cho T4c (SPEC bước 3) và thứ tự T4c trong bản ghi (CĐ7): đã thêm 7 mục T4C và gắn T4c vào chuỗi.
- Phép đột biến lộ hai lỗ hổng test (cắt con qua `chuan_bi`; cách đọc nhóm vòng mặc định): đã thêm test (`runs/dot-bien-001`, `runs/dot-bien-002`).

### C2. Sửa sau phản biện lượt 1 (Codex, chat 29/10/2026; Minh duyệt "DUYỆT SỬA LUÔN" ngày 29/10/2026)

Mỗi mục: lỗi; nguồn; đã sửa; phép kiểm mới. Chi tiết và phản hồi từng điểm ở LOG T-044, mục "Phản hồi phản biện lượt 1 và gói sửa".

- **S1. Bội số ô chưa vào P, M, cờ M5, UV-6, mốc giả (CHẶN).** SPEC T-045 dòng 88–89: ô được lấy k lần thì tính k lần cho P/M/P′/M′, M5, UV-6 và mẫu số C-e; E_X, |E_X| và δ_d giữ từ T0. Code cũ chỉ dùng bội số cho MRR. Phản ví dụ: một ô lấy 3 lần, giảm, đếm M = 1 thay vì 3. Đã sửa: `luat_c.tong_hop` đếm ô theo bội số và bắt các ca của một ô phải cùng bội số nguyên không âm; `pha2.ket_cuc_cap` đếm M5 và truyền bội số cho UV-6; `uv6.dem` đếm theo `trong_so`; `pha2.dem_moc_gia` nhận `trong_so`. Test cũ của CĐ13 nhân đôi ca *trong cùng ô*, nên không phân biệt được "ô lấy 2 lần" với "ô có thêm ca"; đã viết lại: so ô lấy 2 lần với một ô bản sao mang mã ô mới. Đáp án mới TS2–TS5. Đột biến D22–D25.
- **S2. Chuỗi chưa xuất trạng thái quan sát của nguồn metric (CHẶN).** Đặc tả v1 dòng 73; Đ19 điểm 3–4: báo F/H/số ô theo từng nguồn metric, hoặc UNSUPPORTED. Code cũ chỉ có `coverage.trace`, `coverage.log`. Đã sửa: `chuoi.chay` ghi `coverage[<mã nguồn metric>]` từ mốc riêng của nguồn trong cửa sổ; nguồn không có mốc riêng ghi `UNSUPPORTED` kèm `ly_do = khong_co_moc_rieng` và `cham_NA`; thiếu khai coverage ghi `UNSUPPORTED`, `ly_do = thieu_coverage`; mã nguồn metric trùng `trace`/`log` là ERROR. Adapter Nezha-OB khai coverage theo từng nguồn `metric:<dịch vụ>` từ cột Time của file nguồn (bỏ mục gộp cũ). Metric vẫn không tham gia T (PII-20). Test mới H1–H3 qua chuỗi, kiểm coverage trong test adapter. Đột biến D26.
- **S3. Giải thích WORLD_DEPENDENT chọn nhầm cặp (CHẶN).** SPEC T-043 B1.3b dòng 464: cặp là thực thể đổi thứ tự với root. Code cũ lấy thực thể đầu bảng ở thế giới khác, kể cả khi thực thể đó đã đứng trước root ở P, và trả cặp cả khi không có thay đổi. Đã sửa: `the_gioi.nguyen_nhan` so vị trí "đứng trước hẳn" (khối khóa lớn hơn, hoặc cùng khối và nhóm trước, như PII-08) giữa P và từng thế giới; ghi `vuot`, `bi_vuot`, cặp (root, kênh mạnh nhất) – (thực thể, kênh mạnh nhất) theo từng thế giới; không có thay đổi thì `cap = None`. Pha 2 ghi `nguyen_nhan_WD` cho ca WORLD_DEPENDENT từ `extra.kenh_co_the_gioi`. Đáp án mới WD1; fixture 29 viết lại phần cấu trúc. Đột biến D27.
- **S4. Lập luận E3 trong đề xuất WHY quá mạnh (KHÔNG CHẶN).** Khớp hoàn toàn cũng có thể gộp dòng ERROR mới qua token `<*>`. Đã sửa câu trong `de-xuat-why.md` đề xuất 1: lý do chọn (a) chỉ là bám hàm suy luận gốc; cách khớp nào giữ bằng chứng log lỗi tốt hơn là chưa kiểm, T-045 đo bằng D3. Không đổi code.
- **N1. Manifest lệch trên Windows (người làm tự thêm, Minh duyệt cùng gói).** `.gitattributes` chỉ đặt `-text` cho `results/**`, nên git đổi `src/*.py` sang CRLF khi checkout trên Windows và sha256 lệch dù nội dung cam kết không đổi. Không sửa `.gitattributes` (ngoài phạm vi). Đã sửa `scripts/tao_manifest.py`: ghi thêm `git_blob` cho file ngoài `results/`; `--kiem` chấp nhận file lệch sha256 nhưng khớp `git_blob`, liệt kê riêng ở `khop_git_blob`. File trong `results/` vẫn so sha256. Kiểm trên checkout CRLF giả lập (`runs/manifest-crlf-001`): PASS, 29 file `src/` khớp `git_blob`; chưa chạy trên Windows thật.

### C3. Sửa sau phản biện lượt 2 (Codex, chat 29/10/2026; Minh: "NẾU KHÔNG CÓ ĐIỂM NÀO XUNG ĐỘT THÌ SỬA NGAY")

Phạm vi: các điểm hai bên không còn bất đồng. E1-CP và bước 5 luật chọn khối không sửa, chờ Minh quyết (mục D). Chi tiết ở LOG T-044, mục "Phản hồi phản biện lượt 2 và gói sửa".

- **S5. MRR mất độ chính xác tại biên 0,01 (CHẶN).** CĐ16; SPEC T-043 B4 bước 7. `pha2.cham` đổi MRR sang số thực; chênh 1/100 thành 0,010000000000000009 nên loại nhầm cấu hình ít thành phần. Đã sửa: `pha2` giữ phân số; `chon_khoi.chon` từ chối số thực (không đổi ngầm); lưu/đọc JSON qua `pha2.ma_hoa_json` / `giai_ma_json`, phân số ghi thành `{"phan_so": [tử, mẫu]}`. Số thực còn lại trong kết quả (tỷ lệ mốc giả, dấu vết E5) chỉ để trình bày; phép quyết định dùng phân số. Đáp án TS6. Đột biến D28.
- **S6. Ô bội số 0 làm chia cho 0 (CHẶN).** SPEC T-045 bước 7. `rr.rr_o` bỏ ô có tổng trọng số 0 (không đóng góp vào RR_o, P, M); `rr.mrr` báo lỗi khi tổng trọng số của tập ca bằng 0 (lấy mẫu trong từng dataset giữ số ô nên không xảy ra). E_X, |E_X|, δ_d giữ từ T0. Đáp án TS7. Đột biến D29.
- **S7. Bước 8 đọc kết cục tại P của cặp phụ thuộc quan sát (CHẶN).** CĐ6.3. `chon_khoi.kiem_cau_hinh_thang` đọc cặp có `phu_thuoc_quan_sat` là KHÔNG ĐỦ CA. Chỉ sửa bước 8; bước 5 giữ nguyên (mục D). Đáp án CK8. Đột biến D30.
- **S8. Thiếu khai báo bắt buộc vẫn chạy với mặc định (CHẶN).** Đ19 điểm 1, 5; CĐ5. `chuoi._kiem_params` kiểm đủ khóa và giá trị: ba khóa `don_vi_thoi_gian` (span "us"; metric, log "s" hoặc "ns"), ba khóa `ho_so_nguon`, ba khóa `tham_so_E3` khi E3 bật: thiếu hay sai là ERROR. T12 bật mà `canh_tinh` thiếu hoặc thiếu `revision`/`canh`: UNSUPPORTED (Đ19 điểm 5); có khóa nhưng sai kiểu: ERROR. Bỏ các mặc định ngầm trong `chuoi.py`, `e3.py`. `tham_so_E5` vẫn mặc định "co_vong" vì CĐ5 ghi đó là mặc định. Đáp án HD1 (15 biến thể). Đột biến D31. Các khóa được kiểm hai lớp (kiểm trước, rồi đọc không mặc định), nên đột biến bỏ một lớp vẫn cho ERROR; chỉ đột biến của T12 đổi được trạng thái.
- **S9. Bản ghi mất thống kê severity và cặp mẫu Drain (CHẶN).** SPEC T-043 dòng 641; Đ15 điểm 3, 6. Bản ghi thêm `extra.thong_ke_log`: `theo_thuc_the[e][N|A]` = {dong, xac_dinh, loi, unknown} (luôn có); khi E3 bật thêm `cap_drain` (mỗi cặp thực thể–mẫu, kể cả lớp không xác định: lop, n_N, n_A, phieu_loi, phieu_khong, unknown_N, unknown_A, loi_xac_dinh_N, loi_xac_dinh_A, khuôn mẫu) và `mau_moi` theo thực thể. Không đổi kênh. Đáp án LOG1. Đột biến D32.
- **S10. Giải thích WORLD_DEPENDENT bỏ sót hòa và thực thể vắng (CHẶN phần giải thích).** `the_gioi.nguyen_nhan` so quan hệ của từng thực thể với root ở P và ở w theo bốn trạng thái: trước, hòa, sau, vắng (`_quan_he`); mọi thay đổi vào `doi`, kèm `vuot`, `bi_vuot`, `cap`. Cờ M5 giữ quy tắc riêng. Đáp án WD2, WD3; phép kiểm cấu trúc của fixture 29 thêm `doi`. Đột biến D33, D34; D27 đổi chỗ đột biến cho khớp code mới (cùng ý: lấy cả thực thể đã đứng trước ở P).
- **S11. Nguồn metric rỗng mất trạng thái (KHÔNG CHẶN).** Chuỗi xuất trạng thái mọi nguồn metric đã khai, kể cả khi không có hàng metric. Đáp án MET2. Đột biến D35; D26 đổi chỗ theo thụt dòng mới.

### C4. Sửa sau phản biện lượt 3 (Codex, chat 30/10/2026; Minh: "duyệt sửa", chat 30/10/2026)

Minh duyệt gói S12–S17 người làm trình trong chat. Người làm đọc là S12–S16; S17 trình kèm "tùy Minh" nên chưa làm. S14 dừng giữa chừng và trình lại (mục D).

- **S12. Hai kênh khác đơn vị trùng mã (CHẶN).** Mã cũ `thực thể|tên|hướng` cho thao tác `cpu` của S và metric `S_cpu` cùng mã; E5 ghi đè `F_I`, xếp hạng và E7 áp chung. Kết quả phụ thuộc thứ tự đầu vào và tên thao tác (phản ví dụ của Codex; người làm tái hiện ở mức hàm và qua `chay`). Cùng lỗi khi hai cột metric khác tiền tố được alias về cùng thực thể và đuôi. Đã sửa: `Kenh.ma` = `thực thể|đơn vị|tên|hướng`; mã đơn vị mang tiền tố loại (`op|`, `metric|`, `log|`, `canh|`, `tan_suat|`). E5 báo lỗi khi hai kênh trùng mã (chuỗi trả ERROR), ghi thêm `ma`, `don_vi`, `giai_thich_ma` vào `inherited_by`. E7 tra giải thích theo mã. Bản ghi `extra.kenh_co` và `extra.kenh_co_the_gioi` lưu `ma` (và `don_vi`). Pha 2 (`the_gioi`, `dau_vet.root_E5_tu_ban_ghi`) đọc `ma` từ bản ghi, không dựng lại từ tên. `ke_thua` và `giai_thich` giữ dạng (thực thể, tên) để đọc (đáp án fixture T-043 dùng dạng này); định danh nằm ở các trường mã. Đáp án KM1 (mức hàm, ba biến thể), KM2 (alias; trùng mã), KM3 (qua `chay`, hai tên thao tác). Đột biến D36–D38. Chưa biết dữ liệu dev có ca trùng tên không (T-044 không đọc dữ liệu); sau sửa, trùng mã không còn xảy ra theo cách dựng.
- **S13. Giải thích WORLD_DEPENDENT chọn kênh mạnh nhất thay kênh đổi (CHẶN phần giải thích).** SPEC T-043 dòng 464 ("cặp đơn vị làm đảo thứ tự"). Đã sửa `the_gioi.nguyen_nhan`: mỗi thế giới w ghi `kenh_doi` (kênh của root và của thực thể đổi quan hệ mà xuất hiện, mất cờ, đổi điểm hoặc đổi F_I giữa P và w), `phan_khoa` (phần đầu tiên của khóa khối phân định quan hệ e–root ở P và ở w: tầng, max s, số kênh, Σs; với E6b: π, K_I, K_raw). `cap` ghi mã kênh: kênh đổi của mỗi bên; bên không có kênh đổi thì ghi kênh có điểm lớn nhất ở w, tức kênh không đổi đứng trong cặp. `khong_co_kenh_doi` = true khi cả root và mọi thực thể đổi quan hệ không có kênh đổi (ví dụ khối lượng PageRank ở E6b; N2 của người làm). Đổi đáp án tự lập WD1–WD3 theo định nghĩa mới (WD3: kênh mất cờ của B nay đứng trong cặp, trước đây là null); phép kiểm cấu trúc của fixture 29 ghi mã kênh (đáp án T-043 "cặp U1 của A, U2 của B" không đổi). Đáp án WD4 (phản ví dụ của Codex). Đột biến D39, D40.
- **S15. Freeze trỏ tới wheel Linux trong thư mục cloud (KHÔNG CHẶN).** `freeze-m1.txt` dòng pyarrow đổi thành `pyarrow==18.1.0`. Nguồn gốc bản cài cloud ghi ở `bao-cao.md` mục 2. Chưa chạy lại lệnh dựng môi trường (cần mạng; chưa được duyệt).
- **S16. Thiếu báo kèm UV-6 theo Hit@1 kỳ vọng (KHÔNG CHẶN).** CĐ2 dòng 28. `uv6.dem` trả thêm `ky_vong`: Σ bội số × (1 − Hit@1(c)) ở ca đang đúng và Σ bội số × max(0, Hit@1(c) − Hit@1(c bỏ E3)) ở ca lỗi mã, gộp và theo dataset, phân số chính xác. Chỉ báo kèm, không vào phép quyết định. Đáp án UV6-3. Đột biến D41.

### C5. Hai OPEN đã được Minh quyết (chat 30/10/2026: "duyệt E1-CP, bước 5 như trên"; biên E1-CP: "Biên mở")

- **S18. Quy tắc E1-CP của M1.** τ = 1 ms (bài CRISP §5.2, thẻ đọc, CĐ1); khi kiểm vùng chồng lấn xét mọi con khác của cùng cha, kể cả con đã chọn vào đường găng (câu chữ CĐ1); biên mở: con khác chỉ chặn khi một đầu mút nằm hẳn trong vùng, trùng mút vùng không tính; phá hòa PII-04. Câu "bỏ qua các con bắt đầu hay kết thúc trong khoảng của LFC" đọc là đã nằm trong happensBefore có τ: LFC kết thúc muộn nhất, nên con nào có c_end > LFC_start đều kết thúc trong khoảng LFC; bỏ qua nguyên chữ thì τ không bao giờ có tác dụng. Đây là cách đọc của M1, không phải câu chữ của bài. Lý do chọn biên mở: mốc thời gian thô (ms) hay trùng mút; biên đóng thì con trùng mút chặn, làm τ gần như mất tác dụng. Lệch đã biết: code CRISP chính thức (revision trước ATC) dùng ngưỡng 1% thời lượng cha và biên đóng, cho 3000 ở ca phản ví dụ; ở ca này chính biên đóng cho 3000 dù xét con nào; chưa xác minh bản code bài báo dùng (giới hạn chưa kiểm). Đã sửa `span.duong_gang`. Ca phản ví dụ: 2600 ở cả 24 thứ tự (code cũ 2000). Đáp án CP1, fixture 2, 3 không đổi. Ảnh hưởng: không vào ma trận dev, K-b không chạy E1-CP; đổi số mô tả D4 của T-045; xét lại khi dùng E1-CP ở chặng 2 (FlashTicket). Đáp án CP2. Đột biến D42 (chỉ con còn lại), D43 (biên đóng).
- **S19. Bước 5 luật chọn khối đọc cặp phụ thuộc quan sát là KHÔNG ĐỦ CA.** D2f; SPEC T-043 dòng 898 ("Bước 5 chỉ áp cho thành phần ít ca… Thành phần không ít ca không bị ép bật"). Bước 4 vẫn không loại vì phụ thuộc quan sát. `chon_khoi.chon` lượt hai và `kiem_cau_hinh_thang` (bước 8) dùng chung `_kc_ptqs`, nên hai bước đọc cùng một cặp theo một cách; trước đây bước 5 đọc kết cục tại P còn bước 8 đọc KHÔNG ĐỦ CA, có thể sinh xung đột giả ở bước 8. Hệ quả Minh duyệt cùng: thành phần ít ca có kết cục HẠI tại P nhưng khác ở S_lo hoặc S_hi vẫn được giữ bật (D2a, M-48); phải báo khi xảy ra trên dev. Đáp án CK5 (hai biến thể; biến thể b là trường hợp HẠI tại P). Đột biến D44; D30 đổi chỗ theo code mới (cùng ý).

### C6. Sửa sau phản biện lượt 4 (Codex, chat 30/10/2026; Minh: "Duyệt cả gói", chat 30/10/2026)

- **S20. Điểm bằng nhau theo công thức bị tách hòa vì số thực (CHẶN; F1, N1).** Hai đơn vị phân vị cùng e = 1/10 cho 0,09999999999999999 và 0,1 (tỷ lệ vượt chia ra số thực rồi mới trừ); hai đơn vị đếm cùng n_N/n_A lệch ở chữ số cuối khi T = (590, 310), (610, 290), (7, 3); Σs cộng số thực tách hai tổng bằng nhau (1,9 và 1,9000000000000001). Khóa hòa "theo khóa chính xác" (B1.6) vì thế sai, đổi RR (ví dụ 3/4 thành 1/2) và thứ tự giữa các thế giới. Đã sửa: `e4` tính tỷ lệ vượt, hiệu, λ và e bằng phân số, đổi sang số thực một lần, trả kèm `e_<hướng>_q`; `Kenh.s_q` mang điểm chính xác (`s_chinh_xac`); E2 truyền nguyên phân số; `xep_hang.khoa_q` (max, số kênh, Σs chính xác) dùng để sắp và gộp hòa, `key` ghi ra vẫn là số thực; C-d1, C-d2, C-d3 so khóa chính xác (C-d3 cộng điểm đường chính xác). Không thêm dung sai. Hệ quả: Σs ghi ra có thể đổi ở chữ số cuối so với bản cũ. Đáp án SS1, SS2, SS3. Đột biến D45–D47; D03, D13 đổi chỗ theo dòng mới (cùng ý). N2: m của T4c nay tính log1p của x chính xác (S21), nên hai x bằng nhau cho cùng m; chỉ còn khả năng hai x khác nhau làm tròn ra cùng số thực. π của E6b làm tròn 12 chữ số như đặc tả; C-g giữ số thực (chỉ báo cáo, nối bản ghi P3).
- **S21. Giá trị không hữu hạn làm dừng pha 1 (CHẶN đường ghi; F2).** m của T4c tràn thành vô hạn từ đầu vào hữu hạn; nhánh z giữ cờ và điểm vô hạn dù đặt `hop_le = False`; `runner._json` ném lỗi ngoài `chay`. Đã sửa: m của T4c tính trên phân số (trung vị chính xác; x chính xác; log1p của x làm tròn một lần, x quá lớn thì log của tử và mẫu nguyên), hữu hạn với mọi đầu vào hữu hạn; m của T4c trong bản ghi cũ đổi ở chữ số cuối (16/104 bản ghi tất định; `scripts/so_truong_ban_ghi.py`); nhánh z gặp điểm không hữu hạn thì bỏ cờ của đơn vị (đơn vị không hợp lệ); chuỗi kiểm bản ghi ghi được JSON chuẩn trước khi trả, không được thì trả bản ghi ERROR (ca vẫn ở mẫu số, WHY-28). Đáp án T4C1, Z1. Đột biến D48–D50.
- **S22. `bat_tat` không được kiểm (KHÔNG CHẶN; F3).** `_kiem_params` đòi đúng tám khóa của `hop-dong.json#/vao/params/bat_tat` và giá trị trong tập cho phép (chuỗi đúng, bool thật); sai là ERROR. Bỏ các mặc định ngầm khi đọc. Đáp án BT1. Đột biến D51.
- **S23. E6b không lưu π gốc (KHÔNG CHẶN; F4).** Đặc tả v1 dòng 346. Bản ghi thêm `extra.E6b_pi` theo thế giới khi E6 = b. Đáp án PI1. Đột biến D52.
- **S24. Mốc metric lệch số hàng bị cắt bớt (KHÔNG CHẶN; F5).** Mốc riêng của nguồn phải có đúng số phần tử bằng số hàng metric, lệch là ERROR. Đáp án MET3. Đột biến D53.
- **S25. Map bội số thưa tự lấy 1 (KHÔNG CHẶN; F7).** `rr.boi_so`: `trong_so` None là mọi ca 1; map đã truyền (kể cả rỗng) phải có đủ mọi ca, gồm ca bội số 0; thiếu là lỗi. Dùng chung ở `rr.rr_o`, `rr.mrr`, `luat_c`, `pha2._w`; UV-6 báo lỗi khi chỉ một phần ca mang `trong_so`. Đáp án tự lập TS2 sửa đầu vào thành map đủ (c1–c3 bội số 1), đáp án không đổi. Đáp án BS1. Đột biến D54.
- **S26. Pha 2 không kiểm bản ghi trùng, thiếu, lệch metadata (KHÔNG CHẶN; F6).** `pha2.doc` kiểm số dòng thật bằng `so_ban_ghi`, mỗi (config_id, opaque_id) đúng một bản ghi, đủ tích cấu hình × ca, và khớp `cau_hinh`, `so_ca` của `pha1.json` khi có; lệch là `LoiDuLieuPha2`. `cham` trả số dòng thật. Đáp án P2D. Đột biến D55, D56.
- **S14 (phương án a).** `runner._params` truyền `doi_chung` cho cấu hình đối chứng chạy M1; chuỗi không dựng vùng E7 khi `doi_chung` là C-a0 hoặc C-a1 (`region = None`; đặc tả v1 dòng 361, 405); giá trị lạ là ERROR. Không đổi `bat_tat` (hợp đồng T-043 không có khóa E7). Các trung gian khác dựng từ cạnh (inherited_by trạng thái `de_xuat`, nhóm vòng, C-d1/C-d3) vẫn ghi để báo; "không quan hệ" của C-a0 chỉ áp cho thứ hạng. Đáp án CA0E7. Đột biến D57.
- **S17.** `chon_khoi.chon` dựng tập cặp luật cần ((R0, c) và (c bỏ x, c); cặp (c, c thêm x) của lượt hai nằm trong tập này) trước mọi bước; thiếu là lỗi, không trả cấu hình thắng. Đáp án CK9. Đột biến D58.
- **Không sửa, ghi lại:** C-e theo verdict tại P (đúng hợp đồng hiện hành; đổi là đổi đặc tả, Minh quyết). Tối ưu C-d3: đo ở T-045 bước 1 trước. Ứng viên E5 giữ phần dư: chưa kiểm; điểm các loại kênh chưa chắc so được; đổi ma trận, cần đặc tả và Minh duyệt.

### C7. Sửa sau phản biện lượt 5 (Claude, phiên phản biện trong chat 31/10/2026; Minh: "duyệt theo đề xuất", chat 31/10/2026)

Lượt này do một phiên Claude soát (Claude là người làm của T-044, nên lượt này không thay lượt phản biện chính thức của Codex theo SPEC). Mọi điểm có phản ví dụ chạy được trên ca giả ngoài repo. Minh duyệt gói sửa và sáu điểm chọn (Q1–Q6) theo đề xuất trong chat. Trên bộ ca tất định, mọi bản ghi giống bản trước sửa ở mọi trường (`runs/tat-dinh-009`); các sửa chỉ đổi kết quả ở đúng các ca phản ví dụ.

- **G1. Luật chọn khối không kiểm đủ cấu hình (CHẶN bắt đầu T-045).** `chon_khoi.chon` lấy danh sách cấu hình từ `MRR`; thiếu hẳn một cấu hình (và các cặp của nó) thì phép kiểm cặp của S17 vẫn qua và bước 5 không xét cấu hình đó. Phản ví dụ: đủ 4 cấu hình chọn E1+E3; bỏ E1+E3 thì chọn E1, không báo. Đã sửa: `MRR` phải có đúng 2^n tên chuẩn theo `thanh_phan`; `it_ca`, `do_thi` phải là danh sách con của `thanh_phan` (chuỗi `'E3'` hay tên lạ `'E3b'` trước đây làm bước 5 không làm gì); `kiem_cau_hinh_thang` báo lỗi khi thiếu cặp thay vì trả `thieu_cap`. Đáp án CK10. Đột biến D59–D61.
- **G2. Luật C nhận số thực (CHẶN bắt đầu T-045).** `luat_c._fr` đổi lặng lẽ số thực sang phân số; δ_d = 1/30 viết dạng số thực nhỏ hơn 1/30 nên ΔMRR_d = 1/30 đúng biên cho TRÁI CHIỀU DATASET thay vì KHÔNG TÁC DỤNG hay HẠI. Đã sửa: `_fr` chỉ nhận Fraction hoặc int; `rr.boi_so` chỉ nhận bội số nguyên không âm kiểu int/Fraction (chuỗi `'2'`, 2,5, bool là lỗi); `uv6.dem` chỉ nhận `trong_so` nguyên không âm và Hit@1 phân số. Test UV6-1..3 đọc Hit@1 của fixture (viết số thực) qua `phan_so` như các fixture luật C; đáp án không đổi. Đáp án LC1. Đột biến D62–D64.
- **G3. E_X không được kiểm với tập ô của ca (CHẶN bắt đầu T-045; Q4).** Mã ô trong E_X khác kiểu với mã ô của ca thì P = M = 0 mà số ô E_X vẫn đủ: GIÚP thành TRÁI CHIỀU Ô. Đã sửa: `luat_c.tong_hop` báo lỗi khi E_X là chuỗi, có ô không thuộc `ds`, hoặc `ds` có mã ca trùng. Hệ quả (Minh duyệt Q4): ca không được lấy vào mẫu phải nằm trong `ds` với bội số 0, không được bỏ khỏi `ds`; test TS7 đổi vế "bỏ hẳn ca b" thành phải báo lỗi. Đáp án LC2. Đột biến D65, D66.
- **G4. Pha 2 tin nhãn thành phần của cặp (CHẶN bắt đầu T-045).** Nhãn khác đúng `'E3'`/`'E5'` thì UV-6/M5 bị bỏ mà không báo. Đã sửa: với cấu hình khối K (`K-R0`, `K-E1+E3`, …), `ket_cuc_cap` đòi cặp lồng nhau theo chiều tắt → bật; thêm một thành phần thì nhãn phải đúng thành phần đó; so với R0 thêm nhiều thành phần thì nhãn phải là `'R0,c'`. Tên cấu hình khác dạng `K-…` (test, K-b, T6–T13) giữ như cũ. Đáp án P2K. Đột biến D67.
- **G5. Bước 8 với thành phần không ít ca (Q1, phương án a).** CĐ6.3 đọc mọi cặp phụ thuộc quan sát ở bước 8 là KHÔNG ĐỦ CA, lệch SPEC T-043 dòng 898 ("thành phần không ít ca không bị ép bật"). Đã sửa: `kiem_cau_hinh_thang(thang, thanh_phan, cap, it_ca)` (`it_ca` bắt buộc); cặp phụ thuộc quan sát của thành phần ít ca vẫn đọc là KHÔNG ĐỦ CA như bước 5; của thành phần không ít ca thì ghi `phu_thuoc_quan_sat` và `trinh_Minh`, không gọi là nhất quán hay xung đột. CĐ6.3 được thay ở điểm này. Đáp án B8-1..3 thêm `it_ca` (B8-3: W ít ca, vì KHÔNG ĐỦ CA là |E_X| < 6 chỉ xảy ra với thành phần ít ca; kết quả không đổi), CK8 tách hai biến thể (E1 ít ca: không đổi; E1 không ít ca: ca 1, 2 thành `phu_thuoc_quan_sat`). Đột biến D68.
- **G6. Mã nội dung cấu hình bỏ `doi_chung`.** `T13-C-a0` trùng mã với `T1-R0`, `K-R0`, `KB-dao-E1`, `T13-bo-E1`; `T13-C-a1` trùng với `K-E1`. Dùng lại kết quả theo mã sẽ làm hỏng S14. Đã sửa: `_ma_noi_dung` thêm `doi_chung` khi có; mã của mọi cấu hình khác không đổi. Đáp án MND1. Đột biến D69.
- **S27. Mã đơn vị trùng khi tên chứa `|`.** `op|{chủ}|{thao tác}` của (A, `x|y`) và (`A|x`, `y`) trùng nhau; A nhận điểm của đơn vị bất thường. Đã sửa: chuỗi báo ERROR khi hai đơn vị trùng mã (chỉ khi thật sự trùng, không chặn mọi tên có `|`); tên cạnh E2-VC tra từ bảng dựng sẵn thay vì `split('->')`, trùng tên cạnh là ERROR. Đáp án KM4 (phần `->` chỉ kiểm bằng đọc code). Đột biến D70.
- **S28. Verdict đếm phép chấm ngoài U (Q2).** `so_hop_le` đếm cả đơn vị của thực thể không thuộc inventory, trong khi tầng, O, độ phủ đã lọc theo U. Đã sửa: chỉ đếm đơn vị có thực thể thuộc U. Hệ quả: ca chỉ có phép chấm ngoài U là INSUFFICIENT_EVIDENCE và bị loại khỏi mẫu số mốc giả. Đáp án CU1. Đột biến D71.
- **S29. Ngưỡng E4 tràn thành vô hạn.** `h = q_hi + ε|q_hi|` tràn với giá trị hữu hạn trên khoảng 1,71e308; bản ghi không ghi được JSON nên cả ca ERROR. Đã sửa: chặn h, l ở số thực lớn nhất (cùng kết quả phép so x > h, x < l); không đổi giá trị thường. Đáp án E4T. Đột biến D72. Giới hạn: Σs của hai điểm z rất lớn ở nhánh z (T4b, chỉ báo cáo) vẫn có thể tràn khi đổi sang số thực, cho ERROR.
- **S30. NEW_OP/STOPPED ở hướng không chấm (Q5).** STOPPED bật cờ xuống cho đơn vị chỉ chấm hướng lên (log lỗi, mẫu lỗi), làm lệch OBS_DEPENDENT và T4c. Đã sửa: NEW_OP chỉ khi chấm hướng lên, STOPPED chỉ khi chấm hướng xuống; ngược lại đơn vị đi nhánh chung, nhãn `binh_thuong`, không cờ. Đáp án STP1. Đột biến D73.
- **S31. Khóa params thiếu hoặc sai kiểu.** `nhanh_z` phải là bool (`'false'` trước đây thành True); `tham_so_E4` phải có đúng tám khóa của `hop-dong.json` (trước đây thiếu `q_hi`, `q_lo`, `n_exact_max` thì lấy mặc định); `params_ca` của ca không được mang `doi_chung`. Đáp án BT2. Đột biến D74–D76.
- **S32. E1-CP chọn con lồng trong LFC (Q3).** happensBefore không đòi con trước bắt đầu trước nút đang xét; con ngắn hơn τ nằm trong LFC được chọn rồi kéo thêm con khác. Đã sửa: con bắt đầu sau start của nút đang xét không là bước trước (CRISP: bỏ con bắt đầu trong khoảng của LFC); bắt đầu đúng bằng start vẫn xét (biên mở, như C5). Phản ví dụ: u_CP 94200 → 99100 ở cả 6 thứ tự. CP1, CP2, fixture 2, 3 không đổi. Đáp án CP3. Đột biến D77; D09 đổi chỗ theo dòng mới (cùng ý).
- **S33. Vế mốc giả che phụ thuộc quan sát.** Vế C-e tính theo verdict tại P và áp chung ba thế giới, nên che kết cục từng thế giới tính theo RR. Đã thêm (chỉ báo cáo): khi có vế mốc giả, `ket_cuc_cap` ghi `khong_moc_gia` = kết cục từng thế giới khi chưa áp vế này. Không đổi kết cục. Đáp án CE1. Đột biến D78.
- **Test và công cụ kiểm.** Ca biên cho các đột biến đổi hành vi còn sống của lượt 5: BC1, BC2 (luật C), MG2 (mốc giả), CB1 (luật chọn khối), XH1 (khóa E6b, so chính xác, π làm tròn), CP4 (biên E1-CP), P2D2 (pha 2), E4B (cache theo hướng, NEW_OP tại count_min, p = α), UV6-4, E5X, E9X, RR0 (tổng bội số 0), TD2 (đường E5 qua 8 hash seed và hai thứ tự; log trùng mốc), TD3 (đầu ra luật chọn khối và luật C qua 4 hash seed và hai thứ tự khóa). Đột biến D79–D110 tương ứng. Sửa ba test tự so với chính nó: Z1 (phép `json.dumps(...) is not None` luôn đúng), PI1 (làm tròn theo đặc tả, không gọi hàm của code), CK9. `dot_bien.py` tách D07, D08 (chỉ bị phép quét tĩnh bắt) khỏi số đột biến hành vi và đếm đột biến chỉ bị đúng một phép bắt. `tat_dinh.py` ghi hash seed vào đầu ra, `tong_hop_tat_dinh.py` kiểm seed khớp. `so_truong_ban_ghi.py` so cả `inherited_by` (trừ trường mã) và có `--day-du`. `chay_kiem_windows.sh` nhận cây trước sửa chưa commit qua `CAY_CU`.
- **Q6. Cặp giải thích WORLD_DEPENDENT: không sửa, ghi giới hạn (mục D).**

### C8. Sửa sau kiểm lại lượt 5 (phiên Claude kiểm lại, chat 31/10/2026; Minh: "Duyệt cả gói", chat 31/10/2026)

Phiên Claude mới kiểm lại gói C7 (Minh chọn). Mọi điểm đã được người làm tái hiện ngoài repo; phản hồi ở LOG, mục "Lượt 5, kiểm lại của phiên Claude mới: phản hồi của người làm".

- **S34. `khong_moc_gia` bỏ cả điều kiện riêng (sửa S33).** Bản C7 tính lại với nhãn `'X'` và không truyền M5/UV-6, nên cặp E5/E3 có thể ghi GIÚP trong khi bỏ vế mốc giả thật là HẠI. Đã sửa: tính trong cùng vòng thế giới, cùng `thanh_phan`, M5/UV-6 của thế giới đó, chỉ đặt `moc_gia=None`. Đáp án CE1 thêm cặp E5, E3. Đột biến D111.
- **S35. Khóa ghi ra và khóa chính xác.** `_nhom` tách khối theo khóa chính xác nhưng ghi `key` số thực; hai khóa chính xác khác nhau mà ghi ra cùng số thực tạo hai khối liền nhau cùng `key`, và `src/p3/danh_gia` đọc đó là hòa. Đã sửa: sắp vẫn theo khóa chính xác; gộp hòa theo khóa ghi ra (làm tròn đơn điệu nên khóa ghi ra bằng nhau luôn liền nhau); số lần gộp hai khóa chính xác khác nhau ghi ở `diagnostics.gop_khoa_ghi_ra` theo thế giới. Câu "gộp hòa theo khóa chính xác" của C6/S20 được thay ở điểm này; phần "hai điểm bằng nhau theo công thức không bị tách" không đổi. RR, M5, WORLD_DEPENDENT do bộ đánh giá tính không đổi (bộ đánh giá vốn đọc là hòa); chỉ đổi `T` (vùng E7), `thu_tu`, `RANK_CHANGED`, khối của T4c. Đáp án XH1 `chinh_xac` của C7 (hai khối) sai, nay một khối. Đột biến D80 đổi thành đột biến ngược (gộp theo khóa chính xác), D112.
- **S36. Luật chọn khối theo thế giới (bước 10).** `chon(..., the_gioi='P')`. Ở S_lo, S_hi mọi giá trị của `cap` phải là kết quả `ket_hop_the_gioi`, kết cục dùng là `theo_the_gioi[w]` (không đọc phụ thuộc quan sát, vì đó là phép so giữa các thế giới); `MRR` là MRR của thế giới đó; chuỗi ở S_lo, S_hi hoặc tên thế giới lạ là lỗi. Đáp án CW1. Đột biến D113.
- **S37. MRR theo bội số và lấy mẫu ô.** `pha2.mrr_cau_hinh(kq, trong_so, the_gioi)` cho MRR gộp và theo dataset của mọi cấu hình, phân số chính xác. `rr.lay_mau_o(ds, rng)`: trong từng dataset lấy có hoàn lại đúng số ô trên danh sách ô đã sắp, trả map bội số đủ mọi ca (gồm 0). Vòng 1.000 mẫu, seed và báo cáo vẫn do T-045 bước 7 viết. Đáp án MB1, LM1. Đột biến D114–D116.
- **S38. Cache cổng theo ca.** `runner.pha1` lặp ca ở vòng ngoài và đặt cache mới cho mỗi ca; dòng ghi ra vẫn sắp theo cấu hình rồi ca, nên tệp và hash không đổi; `config_id` hay mã mờ trùng là lỗi. Khóa cache gồm khóa đơn vị (không có mã ca) nên vẫn dùng lại giữa các cấu hình của cùng ca. Đáp án RN1. Đột biến D117.
- **S39. Giá trị `tham_so_E4`.** Số hữu hạn, không bool; `m_span`, `m_metric`, `n_exact_max`, `count_min` nguyên ≥ 1; 0 < α < 1; 0 ≤ ε < 1; 0 < q_lo < q_hi < 1. Sai là ERROR. Đáp án BT3. Đột biến D118.
- **S40. Chín vùng có đột biến sống sót của phiên kiểm lại.** Ca kiểm: MG3 (mốc giả loại cặp có bản ghi lỗi, PII-13), T4C2 (phần K_I của m theo F_I), M5W (M5 theo khối của từng thế giới), E2V (E2-VC lấy cạnh điểm cao nhất), WD5 (WORLD_DEPENDENT theo phân bố), CD3A (đích C-d3 phía A), GN3 (G_N khi cả cha lẫn con thuộc N), E9O (ô E9 10 giây), E9E2B (cạnh E2 hai chiều ở E9). Đột biến D120–D128 (tên gốc của phiên kiểm lại trong mô tả). Hành vi của code ở cả chín vùng không đổi.
- **S41. G_N hai cách.** Docstring `m5.G_N_tu_span` ghi: chỉ dùng cho kiểm, pha 2 dùng `extra.G_N`; ba chỗ khác với chuỗi (alias, miền, khóa trùng). Ca GN2: trên S1–S7 (span trong miền, không alias) hai cách cho cùng tập cạnh.
- **S42. Đủ độ đo ở pha 2.** `cham` lưu thêm `do` = `src/p3/danh_gia.do_ca` (Hit@1–10, RR, nDCG@5, Avg@5, cận lạc quan/bi quan) cho mọi ca và thế giới; chỉ báo cáo (M-02, M-07), không dùng để quyết. Đáp án DO1. Đột biến D119.
- **Ngoài T-044, chưa làm:** dòng mặc định cho bảng của SPEC T-045: "Bước 8: cặp phụ thuộc quan sát của thành phần không ít ca (C7, G5) | Giữ cấu hình thắng; ghi 'phụ thuộc quan sát' | Không". SPEC T-045 do Codex làm và đã khóa; người làm T-044 không sửa. Minh và người làm T-045 áp khi mở T-045.

### D. Giới hạn và phần chưa kiểm

- Biên p = α không có fixture (PII-01); lượt 5 thêm phép kiểm giả lập p = α (E4B, C7).
- Luật C chưa tính khoảng tin cậy bootstrap theo ô (báo kèm, không dùng để quyết); T-045 dùng `p3.danh_gia.bootstrap`.
- Adapter chỉ kiểm trên bộ dữ liệu tổng hợp đúng schema của `src/p3`; chưa chạy trên dữ liệu dev (T-045 bước 0).
- C-g, C-c chỉ kiểm bằng fixture và đáp án tự lập; chưa nối với bản ghi P3 thật.
- Cạnh tĩnh T12 chỉ kiểm bằng ca giả; chưa đọc mô hình T-038, T-039.
- Thời gian và RAM trên ca thật chưa đo (T-045 T1).
- **E1-CP (phản biện lượt 2 điểm 7): đã quyết ngày 30/10/2026, xem C5 (S18).**
- **S14 (E7 ở C-a0/C-a1): đã sửa theo phương án (a), xem C6.**
- **S17 (thiếu cặp): đã sửa, xem C6.**
- **Bước 5 luật chọn khối với cặp phụ thuộc quan sát: đã quyết ngày 30/10/2026, xem C5 (S19).**
- **Lượt 5 (C7):** Q6 — cặp giải thích WORLD_DEPENDENT (`the_gioi.nguyen_nhan`, `cap`) có thể ghi kênh đổi không phân định phần khóa (ví dụ root mất kênh mạnh nhất, A thêm kênh 0,01: cặp ghi kênh 0,01 của A, trong khi kênh đứng đối diện root là kênh 0,8 không đổi). Chỉ ảnh hưởng phần giải thích; `kenh_doi`, `phan_khoa` vẫn lưu đủ để đọc lại. Minh chọn ghi giới hạn (31/10/2026).
- **Lượt 5 (C7):** trùng tên cạnh E2-VC khi tên chứa `->` chỉ kiểm bằng đọc code, chưa có ca giả qua toàn chuỗi. Phụ thuộc hash seed của đường E5 kiểm bằng TD2 (8 seed, phép kiểm riêng), không thêm ca vào bộ ca của `tat_dinh.py`.
- **Lượt 5 (C7):** phép độ bền 1.000 mẫu theo bội số (SPEC T-045 bước 7) chưa có hàm dựng sẵn trong `m1_danh_gia`; T-045 tự viết, phải giữ đủ 52 ca trong `ds` với bội số 0 (G3), lấy mẫu trong từng dataset trên danh sách ô đã sắp, truyền δ_d dạng phân số. `p3.danh_gia.bootstrap` gộp ô của hai dataset và dùng số thực nên không dùng cho phép này. Bước 10 luật chọn khối (chọn lại ở S_lo, S_hi) cũng do T-045 gọi `chon` theo từng thế giới. Lượt 5b (C8) thêm `chon(..., the_gioi)`, `pha2.mrr_cau_hinh`, `rr.lay_mau_o` để T-045 dùng; vòng 1.000 mẫu vẫn do T-045 viết.
- **Lượt 5b (C8):** khóa ghi ra gộp hai khóa chính xác khác nhau thành hòa (S35); số lần gộp có ở `diagnostics.gop_khoa_ghi_ra`. Tần suất trên dev chưa biết (T-045 báo). Bản ghi trên bộ ca tất định chỉ thêm trường này.
