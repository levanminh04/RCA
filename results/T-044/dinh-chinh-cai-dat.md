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

## Phần II — chỗ lệch lộ ra khi cài

Chưa có.
