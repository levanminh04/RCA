# T-046 — Thiết kế lại cổng kiểm định, quy tắc `verdict` và quyết thang điểm của M1

- **Trạng thái:** đã duyệt (01/11/2026, lời Minh trong chat: “duyệt tạo spec luôn, kèm prompt cho phiến claude mới độc lập hoàn toàn yêu cầu triển khai 46, trước khi triển khai cần tự rà soát spec độc lập dựa trên các thông tin đã có, nếu có vấn đề hoặc rủi ro lỗ hỏng, bỏ khó chọn dễ, thì cho phép sửa lại spec rồi mới bắt đầu triển khai task”). Bản này là bản 2: bản 1 do Claude soạn trong chat ngày 01/11/2026; Codex rà trong chat cùng ngày (bốn điểm CHẶN, đều được người soạn nhận đúng và sửa); lượt kiểm lại bản 2 không làm vì Minh duyệt thẳng. Minh duyệt nguyên đề xuất, nên các mức ở cột "Đề xuất" của bảng tiêu chí có hiệu lực.
- **Người làm:** Claude (một phiên mới, độc lập với phiên soạn SPEC). **Người phản biện:** Codex.
- **Bản 3** (01/11/2026, sau điểm dừng D-1): người làm thêm mục "Bản 3" (B1–B6) theo lời Minh giao quyền quyết ở D-1 (LOG phiên 1 (tiếp)). Bản 2 và các sửa S1–S10 giữ nguyên.
- **Bản 4** (01/11/2026, sau luật chọn bản 3): người làm thêm mục "Bản 4" (C1–C3): nới (a) theo minimax, thêm V4, theo lời Minh giao quyền (LOG phiên 1 (tiếp 2)). Các bản trước giữ nguyên.
- **Thuộc gói MRP:** P6 (M1). **Cổng:** chuẩn bị G3.
- **Phụ thuộc:** T-045 đã nghiệm thu (Q-222); code `bbef69dd`, commit kết quả `bc10d947`; D17 Q-a, Q-b (Q-218); LOG T-045 phiên 2 (gói quyết định bản sửa theo lượt 2: QĐ-2, QĐ-3, QĐ-4); `tasks/T-045-chay-khoi-k-dev/REVIEW-2-claude.md` U2, U3.
- **Nguồn chia task:** lời Minh chat 01/11/2026 “t46 claude làm, 47 codex làm” (QĐ-2 phương án (ii); dòng DECISIONS đề xuất Q-224, chưa ghi).
- **Quyền rà và sửa SPEC trước khi triển khai** (lời Minh ở dòng Trạng thái): phiên người làm đầu tiên tự rà SPEC độc lập trên thông tin trong repo; nếu thấy vấn đề, rủi ro, lỗ hổng hoặc chỗ SPEC chọn việc dễ bỏ việc khó, được sửa SPEC trước khi bắt đầu bước 0 của phần triển khai. Mọi sửa ghi ở LOG mục "Rà và sửa SPEC" (đoạn cũ → đoạn mới, lý do, ảnh hưởng). Không được dùng quyền này để: đổi mục tiêu hay câu hỏi nguồn; nới tiêu chí hay bỏ phép kiểm cho dễ đạt; thêm quyền đọc root, tính MRR, mở dữ liệu khóa; chọn ứng viên. Sửa nào làm tiêu chí lỏng hơn hoặc thu hẹp phạm vi thì dừng, trình Minh.

## Mục tiêu

**Câu hỏi nguồn:** MRP P6 (`docs/MRP.md:257`: trước G3 phải kiểm đầu vào, trung gian, hành vi trên dev, không chỉ chạy không lỗi); SPEC T-043 B6 (khóa chế độ tính cổng, α, ε, điều kiện của `verdict` trước G3); DT18-NV2.

**Hiện tượng (T-045):**
- `verdict` = CAUSE_FOUND ở 30/30 cửa sổ giả RE2-TT, ở mọi cấu hình; ở cửa sổ thật 52/52 (`results/T-045/t1.json`, `khoi-k.json`).
- Ở α = 0,001 vẫn khoảng 61 kênh có cờ mỗi cửa sổ giả (`results/T-045/t4.json#/cau_hinh/T4-e0.05-a0.001/moc_gia/kenh_co_theo_nhom`).
- Với cùng cờ, nhánh z cho MRR RE2-TT 0,983 so với 0,718 của R0 (`results/T-045/t4b.json`).

**Loại task:** chẩn đoán, thiết kế, cài đặt, kiểm hành vi. Không chọn thành phần khối K. **Không đọc root, không tính MRR.** Có dùng mốc tiêm (chế độ (a)) để biết cửa sổ nào có lỗi.

**Vai trò dữ liệu:** mọi dữ liệu trong task là dữ liệu dev dùng để chọn và kiểm lại; không có phần kiểm độc lập. RE2-TT dev chỉ có 720 giây trước t (đã đọc cột `time` của `metrics.parquet` ở 5 ca; kiểm đủ 30 ca ở bước 1). Phép A/A trên N nằm trong phía A của cửa sổ giả C-e (t′ = t − 300). Vì vậy:
- chọn ứng viên chỉ bằng A/A, dữ liệu tổng hợp và cửa sổ thật;
- khóa ứng viên (ghi LOG kèm hash) trước khi xem kết quả trên C-e;
- C-e chỉ báo sau khi khóa, như phép kiểm lại có chồng lấn dữ liệu, không là bằng chứng độc lập;
- T-047 dùng lại C-e cho vế mốc giả của luật C, kèm giới hạn này.

**Đạt task này cho:**
1. Chẩn đoán nguyên nhân cổng qua giả: phân xử hoặc thu hẹp.
2. Cổng và `verdict` chọn theo luật khai trước, hoặc xung đột trình Minh.
3. Quyết giữ hay đổi thang điểm theo tiêu chí khai trước.
4. Code có test, chế độ cũ làm mặc định.

**Phần nguồn chưa bao phủ:**
- **Hiệu chuẩn metric Nezha-OB: OPEN.** Chỉ có 5 điểm ở N, 5 điểm ở A (SPEC T-043 dòng 349; `m_metric` = 5 ở `results/T-043/ma-tran-thu.json#/tham_so_E4`), nên không làm A/A được. Xử lý: không đổi cổng cho loại đơn vị này, trừ khi ứng viên được chọn là một quy tắc chung áp được theo cùng công thức; ghi giới hạn; kiểm trên FlashTicket. Không hạ hỗ trợ tối thiểu.
- Báo nhầm của Nezha-OB khi hệ khỏe (D6): FlashTicket.
- Đối chứng không đồ thị đủ mạnh (LESSONS QT7): task (3), trước khi khóa danh sách so sánh ở G3.
- Chọn lại khối K: T-047.

## Câu hỏi, bằng chứng và quyết định

Mọi dự đoán là **chưa kiểm**.

| # | Câu hỏi | Giải thích khác | Phép kiểm | Hỗ trợ / bác bỏ khi | Còn thiếu |
|---|---|---|---|---|---|
| C1 | Vì sao cổng từng đơn vị qua giả nhiều hơn α? | Tự tương quan; trôi nền; mẫu lớn nhạy với chênh nhỏ; tải đổi | Trên N của 52 ca, theo loại đơn vị và nguồn (trừ metric Nezha-OB): hàm tự tương quan; tỷ lệ qua cổng A/A với G0, G1, G3. Cửa sổ A/A theo A1: RE2-TT nửa đầu so nửa sau của N, mỗi nửa 150 giây; Nezha-OB chia đôi phần N có span. Chẩn đoán phụ theo A2 | Cổng có tính tới tự tương quan đưa A/A về gần α: tự tương quan đủ giải thích phần qua giả. Không loại được trôi nhỏ, vì G1 giảm cỡ mẫu hiệu dụng; phân biệt bằng A2. Vẫn cao: hỗ trợ trôi nền hoặc không dừng, hoặc khối chưa đủ dài (b chạm trần 60) | A/A 150 + 150 giây khác cỡ 300 + 300 của phép thật; A/A Nezha-OB mỗi nửa 20–48 giây |
| C2 | Quy tắc gộp của `verdict` | Lỗi chỉ ở cổng | Tỷ lệ CAUSE_FOUND ở cửa sổ A/A và cửa sổ thật, theo tổ hợp cổng × quy tắc | Tiêu chí (a), (b), (c1) | — |
| C3 | Giữ hay đổi thang điểm? | Nhánh z còn đổi cách ghép đơn vị phân vị (không bị chặn) với kênh đếm (trong [0; 1]) | Tỷ lệ kênh phân vị có cờ đạt rA = 1 theo hướng đang xét (bão hòa đúng nghĩa; trần e = 1 − rN, `src/m1/e4.py` hàm `cham_phan_vi`). Báo riêng NEW_OP, STOPPED vì bị gán 1 theo quy tắc (`cham_dem`). Số thực thể hòa ở phần tử đầu của khóa tầng 1. Đo trên R0 với cổng đã khóa, cửa sổ thật | Tiêu chí (S) | Tương tác với E1, E2: T-047 |
| C4 | Còn phản ứng với lỗi không? | Giảm báo nhầm bằng cách làm đầu ra mất tác dụng; CAUSE_FOUND ở cửa sổ thật có thể do nhiễu | (c1) CAUSE_FOUND ở 52 cửa sổ thật. (c2), báo sau khi khóa: cặp cùng ca RE2-TT, số đơn vị có cờ ở cửa sổ thật so với C-e | (c1) dùng để chọn; (c2) chỉ báo | — |

**Phạm vi phép kiểm (đặc tả trước khi đánh giá):**
- Đơn vị: mọi đơn vị trong U, hợp lệ (`hop_le`), ở thế giới đang tính. Mỗi hướng trong `huong_cham` là một phép. `verdict` tính ở P như hiện hành; S_lo, S_hi áp cùng quy tắc.
- Ứng viên cổng chỉ đổi p của đơn vị phân vị. Ngưỡng h, l và cách tính e giữ nguyên.
- Đơn vị đếm giữ kiểm nhị thức hiện hành. Nếu A/A ở bước 3 cho thấy đơn vị đếm cũng qua giả nhiều hơn mức (a) thì dừng ở D-1, trình Minh; không tự thêm ứng viên.
- NEW_OP, STOPPED giữ là cờ trực tiếp, không thuộc họ phép kiểm để hiệu chỉnh. Báo riêng số cửa sổ chỉ CAUSE_FOUND nhờ các cờ này.
- Quy tắc `verdict` mới chỉ đổi `verdict`, không đổi `F_raw`, tầng hay thứ hạng.

**Ứng viên** (không chọn trước):
- **Cổng:**
  - G0: Mann–Whitney hiện hành.
  - G1: Mann–Whitney trên trung bình của các khối thời gian không chồng. Độ dài khối b là độ trễ nhỏ nhất mà hệ số tự tương quan trên N dưới 0,2, chặn trong [5; 60] giây, đo riêng từng đơn vị chỉ trên N. Cần ít nhất 5 khối mỗi phía; nếu không thì giữ G0 cho đơn vị đó và đếm số đơn vị như vậy.
  - G3: kiểm hoán vị theo khối cùng b, thống kê rA − rN, 2.000 hoán vị, seed cố định, một phía theo hướng. Chi tiết ở A3. G3 lệch nguyên tắc "Không dùng Monte Carlo" của SPEC T-043 B1.3; nếu chọn G3, WHY ở D-2 phải nêu lý do. Với 2.000 hoán vị, p nhỏ nhất là 1/2.001, lớn hơn ngưỡng Holm nhỏ nhất α/m khi m > 20; tổ hợp G3 × V1 xử lý theo A3 điểm 6.
  - Không xét cỡ mẫu hiệu dụng gắn vào Mann–Whitney: chưa có công thức p kiểm được.
- **`verdict`:**
  - V0: hiện hành.
  - V1: Holm trên họ phép kiểm của cửa sổ ở mức α. Họ phép kiểm: mọi phép hợp lệ ở thế giới P, mỗi cặp (đơn vị, hướng thuộc `huong_cham` của đơn vị), gồm đơn vị phân vị và đơn vị đếm, chỉ đơn vị của thực thể thuộc U; không gồm NEW_OP, STOPPED. CAUSE_FOUND khi có ít nhất một phép bị bác ở thủ tục Holm (bước xuống) mà cặp (đơn vị, hướng) đó có F_I = 1 (nên có e > 0 như điều kiện cờ), hoặc có đơn vị NEW_OP/STOPPED với F_I = 1.
  - V3: cần ít nhất k = 2 đơn vị khác nhau (thực thể thuộc U) có F_I = 1 ở ít nhất một hướng; NEW_OP, STOPPED tính là đơn vị có cờ.
  - V1, V3 dùng F_I như V0 (V0 xét tầng 1, tức F_I sau E5). Ở R0, F_I = F_raw. NO_INTRINSIC_ANOMALY và INSUFFICIENT_EVIDENCE giữ như V0.
  - Không xét Benjamini–Hochberg: `verdict` trả lời câu hỏi theo cửa sổ ("có bất thường tự sinh không"), nên mục tiêu là kiểm soát sai theo cửa sổ.
- **Thang điểm:** S0 E4 (D24); S1 E4 cộng khóa phụ độ lớn (T4c, đã cài); S2 z có chặn. Ứng viên phải giữ việc so được kênh phân vị với kênh đếm (WHY-56).
- **Thứ tự ưu tiên khi nhiều ứng viên đạt:** cổng G0 < G1 < G3; `verdict` V0 < V3 < V1. Lý do: ít giả định thêm và rẻ hơn đứng trước. Tổ hợp xét theo cổng trước: (G0, V0), (G0, V3), (G0, V1), (G1, V0), (G1, V3), (G1, V1), (G3, V0), (G3, V3), (G3, V1). Lý do: (a) chỉ phụ thuộc cổng; cổng còn đổi cờ và thứ hạng ở T-047, còn `verdict` không đổi gì khác; nên chọn cổng ít giả định nhất đạt hiệu chuẩn trước, rồi `verdict` đơn giản nhất đạt với cổng đó.

**Mức tiêu chí** (đề xuất của người soạn; Minh duyệt nguyên đề xuất, nên cột "Đề xuất" có hiệu lực):

| Tiêu chí | Dùng để | Đề xuất (hiệu lực) | Phương án khác đã xét | Đánh đổi |
|---|---|---|---|---|
| (a) Tỷ lệ qua cổng ở A/A, theo loại đơn vị và nguồn (trừ metric Nezha-OB), gồm mọi loại đơn vị phân vị của R0 và của cấu hình K-đủ (A5); ô dưới 100 phép là không đo được (A6, D-1) | Chọn | ≤ 2α | ≤ 3α | Chặt hơn thì mất độ nhạy; trôi nền còn OPEN, nên không đòi bằng đúng α |
| (b) Tỷ lệ CAUSE_FOUND ở cửa sổ A/A của R0, tính và áp mức riêng từng dataset, trên cửa sổ có ít nhất một phép chấm hợp lệ; cửa sổ INSUFFICIENT_EVIDENCE báo riêng, không vào mẫu số; dataset dưới 10 cửa sổ đo được là không đo được (A6, D-1); báo kèm số gộp (Nezha-OB không có metric) | Chọn | ≤ 0,20 | 0,10; 0,33 | Báo kèm khoảng Wilson. Gộp hai dataset, hoặc tính cửa sổ không có phép hợp lệ là "không báo động", làm tiêu chí đạt được khi đầu ra mất tác dụng ở một dataset |
| (c1) Tỷ lệ CAUSE_FOUND ở cửa sổ thật của R0, tính và áp mức riêng từng dataset (30 RE2-TT, 22 Nezha-OB); cửa sổ không CAUSE_FOUND, kể cả INSUFFICIENT_EVIDENCE, tính là không phản ứng; báo kèm số gộp 52 | Chọn | ≥ 0,80 | 0,90; 0,70 | Với G0, V0 đã là 52/52 |
| (b′), (c2) CAUSE_FOUND ở 30 C-e; so cặp thật với C-e | Báo sau khi khóa | — | — | Không đạt (b′) ở mức (b) thì dừng, trình Minh, không chọn lại |
| (S) Mở thay thang điểm khi tỷ lệ kênh phân vị có cờ đạt rA = 1 ở cửa sổ thật; tính riêng từng dataset và gộp, mở khi một trong ba số đạt mức | Quyết thang | ≥ 25% | 15%; 40% | Chưa đo; mức đặt trước khi đo. Từ mức này, khoảng một phần tư bằng chứng phân vị không còn phân biệt độ lớn, thứ hạng dựa nhiều vào khóa phụ |

**Luật chọn:** tổ hợp cổng × `verdict` đạt (a), (b), (c1), lấy tổ hợp đầu tiên theo thứ tự ưu tiên (cổng trước). Tổ hợp G3 × V1 xử lý theo A3 điểm 6. Không tổ hợp nào đạt thì dừng, trình Minh.

### Đặc tả bổ sung khi rà (người làm, phiên 1, 01/11/2026; trước bước 0)

Theo quyền rà và sửa ở đầu tệp; lý do ở LOG mục "Rà và sửa SPEC" (R1–R10). Không đổi ứng viên hay mức tiêu chí; chỉ làm đầy đủ đặc tả trước khi xem số.

**A1. Cửa sổ A/A.**
- Chạy chuỗi M1 nguyên vẹn tại t″, với đầu vào cắt về [t − 300, t): span có start ≥ t − 300 và end < t (đúng tập span thuộc N của phép thật); metric và log có mốc trong [t − 300, t); khoảng ghi của từng nguồn (coverage) cắt về cùng đoạn. Phần ngoài đoạn này nằm ngoài khoảng ghi, không là OPEN. Không sửa `src`.
- RE2-TT: t″ = t − 150.
- Nezha-OB: t″ = (s₀ + t) / 2, với s₀ là end sớm nhất của span thuộc N. Lý do: nửa đầu N không có trace và log ở 22/22 ca (SPEC T-043 dòng 472), nên chia ở t − 150 làm mọi đơn vị trace và log thành NO_BASELINE. s₀ chỉ lấy từ dữ liệu N, không dùng nhãn. Ghi s₀ từng ca.
- Trong A/A, b của G1, G3 đo trên N″ (nửa đầu), như phép thật đo trên N.

**A2. Chẩn đoán phụ của C1** (chỉ báo cáo, không vào luật chọn):
- tỷ lệ qua cổng tách theo: phép dùng G1/G3 hay rơi về G0; nhóm b (b < 60; b = 60 vì chạm trần hoặc vì tự tương quan chưa dưới 0,2 tới độ trễ 60); hướng;
- tỷ lệ p < α/10 và p < α/100 (phần đuôi mà Holm dùng);
- tỷ lệ có cờ F_raw bên cạnh tỷ lệ qua cổng; độ lớn rA − rN của các phép qua giả;
- tỷ lệ đơn vị rơi về G0 ở cỡ A/A so với ở cửa sổ thật (chỉ tính b và số khối; không xem p của cửa sổ thật trước bước 5).

**A3. Đặc tả G1, G3** (áp cho đơn vị phân vị; đơn vị đếm giữ kiểm nhị thức):
1. Chuỗi 1 giây: mỗi phía chia thành ô 1 giây canh theo t (N lùi từ t, A tiến từ t). Giá trị ô là trung bình các mẫu có mốc trong ô (metric: `time`; thao tác và cạnh: `end` của span). Ô không có mẫu là thiếu.
2. Tự tương quan trên N: ρ(k), k = 1…60, dùng các cặp ô cùng có giá trị cách nhau k giây; trung bình và phương sai (chia cho số ô) tính trên mọi ô có giá trị của N. Cần ít nhất 10 cặp; thiếu thì ρ(k) không xác định. b = k nhỏ nhất có ρ(k) xác định và < 0,2, chặn về [5; 60]; không có k nào thì b = 60. N có dưới 10 ô có giá trị, hoặc phương sai bằng 0: dùng G0 cho đơn vị đó, đếm riêng.
3. Khối: N chia thành [t − (j+1)·b, t − j·b), A chia thành [t + j·b, t + (j+1)·b), j = 0, 1, …; chỉ giữ khối nằm trọn trong phía (300 giây); bỏ khối không có mẫu. Cần ít nhất 5 khối có mẫu mỗi phía; thiếu thì dùng G0, đếm riêng. Ở A/A, t thay bằng t″.
   - **Sửa 17:52, sau phản biện lượt 1 (R1; LOG phiên 1 (tiếp 3)):** "phía" là phần giao giữa phía của cửa sổ và bao bản ghi H của nguồn của đơn vị (`coverage.<nguồn>.H`, B1.3b; trace cho thao tác và cạnh, nguồn metric của cột cho metric): N = [max(t − 300, H₀), t), A = [t, min(t + 300, H₁)). Khối chỉ được giữ khi nằm trọn trong đoạn đó. Bản cài trước đó dùng 300 giây cố định, nên ở A/A giữ khối dở (ví dụ b = 37 giữ khối 2 giây thứ năm). Áp như nhau ở A/A, cửa ổ thật và C-e. **Sửa 20:44 (N4):** H làm tròn ra ngoài theo ô 10 giây của B1.3b và chặn bởi khoảng ghi F, vì mép bản ghi lệch vài mili giây làm b = 60 mất một khối. Dữ liệu tổng hợp ở bước 2 (cỡ 150) chịu cùng lỗi ở φ > 0; các số đó chỉ báo cáo, không chạy lại (điều kiện đạt ở φ = 0 có b = 5 chia hết 150 nên không bị ảnh hưởng).
4. G1: `p_cong` hiện hành trên trung bình khối (chính xác khi tổng số khối ≤ 100, xấp xỉ khi lớn hơn), một phía theo hướng.
5. G3: thống kê T = r_d(A) − r_d(N), tính trên mẫu gốc trong các khối được giữ; ngưỡng h, l tính lại từ phần N của từng cách chia (công thức B1.3, cùng ε); so T* với T bằng phân số chính xác. Hoán vị nhãn N/A của khối, giữ số khối mỗi phía. Khi số cách chia C(n_N + n_A, n_A) (đếm theo khối) ≤ 2.000 thì duyệt hết, p là tỷ lệ cách chia có T* ≥ T. Ngược lại lấy 2.000 hoán vị ngẫu nhiên, p = (1 + #{T* ≥ T}) / 2.001. Seed: `numpy.random.default_rng(20261101 + int(h[:16], 16))`, h là sha256 hex của chuỗi "mã đơn vị|hướng"; không dùng `hash` của Python. Thiếu khối: G0, như G1.
6. G3 × V1: với 2.000 hoán vị, một phép chỉ bị bác ở bước i của Holm khi 1/2.001 ≤ α/(m − i + 1). Tổ hợp này vẫn được tính và báo ở 2.000 hoán vị, kèm số phép không thể qua ngưỡng Holm vì phân giải. Khi luật chọn đi tới G3 × V1, các phép có 0 lần vượt trong 2.000 hoán vị đầu được thêm hoán vị (cùng dãy seed) tới B = ⌈m/α⌉ (m của cửa sổ đó) trước khi áp Holm. Ước lượng thời gian trước; quá 1 giờ thì dừng, trình Minh (luật cứng 8).
7. G1 × V1: báo số phép mà p nhỏ nhất đạt được với số khối của chúng lớn hơn ngưỡng Holm. Đây là giới hạn thông tin khi có ít khối, không sửa.

**A4. Họ phép kiểm và cờ của V1, V3:** theo mục Ứng viên.

**A5. Cấu hình K-đủ:** E1-U, E2-C, E3, E5 bật; các khóa khác như R0. Chạy ở cửa sổ A/A để đo (a) cho các loại đơn vị T-047 sẽ dùng: op_excl, canh, thao tác và metric hai hướng khi E3 bật, đơn vị mẫu Drain. Đơn vị đếm của K-đủ vào phép D-1 như đơn vị đếm của R0. Ô mẫu mới của E3 là cờ trực tiếp như NEW_OP, báo riêng. (b) của K-đủ ở cửa sổ A/A tính sau khi khóa, chỉ báo cáo. Đơn vị E3b thuộc task (2), không đo ở đây.

**A6. Mức đo được:** ô (loại đơn vị, nguồn) của (a) cần ít nhất 100 phép hợp lệ ở A/A; dataset của (b) cần ít nhất 10 cửa sổ A/A có phép hợp lệ. Thiếu thì ghi "không đo được" và xử lý ở D-1.

**A7. Bước 2, điều kiện đạt khai trước:**
- Tái lập: G0 trên AR(1) theo cài đặt ở LOG T-043 dòng 1829 phải ra 0,011; 0,073; 0,288; 0,386 (φ = 0; 0,5; 0,9; 0,98). Không khớp thì dừng, tìm nguyên nhân ở phần sinh dữ liệu trước khi dùng các số còn lại.
- G1, G3 ở φ = 0 (300 + 300 và 150 + 150): khoảng Wilson 99% của tỷ lệ qua cổng phải chứa α hoặc nằm dưới α; không thì coi là lỗi cài đặt, sửa rồi chạy lại.
- φ = 0,5; 0,9; 0,98 và trôi bậc thang: chỉ báo cáo. Trôi bậc thang: AR(1) φ = 0,5 cộng bước nhảy c·σ (σ là độ lệch chuẩn biên) ở ranh giới N/A, c ∈ {0,25; 0,5}.
- Kiểm đáp án biết trước (test trong `results/T-046/tests/`): G1 bằng `p_cong` trên trung bình khối tính tay; G3 duyệt hết khớp tính tay ở ví dụ nhỏ; chuỗi hằng cho p = 1; cùng seed cho cùng p; không đổi theo PYTHONHASHSEED.
- Số lần lặp: G0, G1 2.000 mỗi mức; G3 2.000 nếu đo ở bước 1 cho thấy mỗi mức dưới 5 phút, ngược lại 500.

### Bản 3 (người làm, 01/11/2026, sau điểm dừng D-1; theo quyền Minh giao, LOG phiên 1 (tiếp))

Không đổi mục tiêu, câu hỏi nguồn, các mức (a), (b), (c1), (S), A1–A7. Chỉ thêm ứng viên và mở rộng luật chọn cho ứng viên mới. Ứng viên mới được thiết kế sau khi đã xem A/A của dev (`results/T-046/chan-doan-cong.json`); C-e chưa xem.

**B1. Ứng viên cổng đơn vị phân vị thêm**
- **G4 — theo loại mẫu.**
  - Đơn vị metric dùng làm trắng AR(1). Chuỗi 1 giây theo A3 điểm 1. φ̂ = max(0; ρ(1)), với ρ(1) tính trên N theo A3 điểm 2.
  - Phần dư của ô s: r_s = x_s − φ̂·x_{s−1}, chỉ tính khi ô liền trước (s − 1 giây) có giá trị. Ô liền trước của ô A đầu tiên là ô N cuối. Khi φ̂ = 0 thì r_s = x_s, dùng mọi ô.
  - Kiểm `p_cong` một phía trên phần dư A so với phần dư N.
  - Rơi về G0 (đếm riêng) khi: ρ(1) không xác định; N có dưới 30 phần dư; hoặc A có dưới 5 phần dư.
  - Đơn vị sự kiện (thao tác, cạnh) dùng G3 (lấy lại p của G3).
- **GE — phương án cuối, hiệu chuẩn theo thực nghiệm.**
  - p tính theo G4. Mỗi ô (dataset, nhóm đơn vị, hướng) có ngưỡng α_ô: giá trị lớn nhất trong lưới {0,01; 0,005; 0,002; 0,001; 5·10⁻⁴; 2·10⁻⁴; 10⁻⁴; 10⁻⁵; 10⁻⁶} sao cho tỷ lệ p < α_ô ở A/A ≤ α. Không có giá trị nào thì ô đó trượt.
  - Cờ khi p < α_ô và chênh dương.
  - Ô lấy từ A/A của R0 (op_full, metric) và của K-đủ (op_excl, canh).
  - GE dùng A/A hai lần, nên (a) của GE tính trên A/A không có nghĩa. Thay bằng (a′) sau khóa: tỷ lệ qua cổng ở C-e theo từng ô RE2-TT ≤ 2α. Nezha-OB không có C-e, ghi giới hạn.
  - GE không đi với V1, vì đuôi p không được hiệu chuẩn.

**B2. Ứng viên cổng đơn vị đếm** (thay câu "Đơn vị đếm giữ kiểm nhị thức hiện hành")
- **D0:** kiểm nhị thức hiện hành.
- **D1 — kiểm nhị thức có hiệu chỉnh phân tán.**
  - Hệ số φ̂_d = max(1; s²/ȳ). ȳ và s² (chia n − 1) là trung bình và phương sai số sự kiện của đơn vị trong các ô 10 giây trọn của N, canh lùi từ t, chỉ trong [h₀, t). h₀ là mốc dòng log sớm nhất của nguồn trong cửa sổ đang tính (mọi thực thể). Cần ít nhất 3 ô; thiếu, hoặc ȳ = 0, thì φ̂_d = 1.
  - p theo đuôi nhị thức mở rộng cho số đếm không nguyên: k′ = n_A/φ̂_d, n′ = (n_N + n_A)/φ̂_d, p₀ = T_A/(T_N + T_A).
    - p_lên = I_{p₀}(k′, n′ − k′ + 1) khi n_A > 0; ngược lại 1.
    - p_xuống = I_{1−p₀}(n′ − k′, k′ + 1) (bằng 1 − I_{p₀}(k′ + 1, n′ − k′)) khi n′ − k′ > 0; ngược lại 1.
    - I là hàm beta không đầy đủ chuẩn hóa.
  - Khi φ̂_d = 1, D1 trùng D0. e, λ, NEW_OP, STOPPED, count_min giữ nguyên.
- **DE:** như GE, trên p của D1, theo ô (dataset, nhóm, hướng) từ A/A; kiểm (a′) trên C-e.
- (a) của cổng đếm xét trên các ô đếm đo được (A6). Ô đếm không đo được báo tỷ lệ kèm khoảng Wilson và ghi OPEN (log_loi RE2-TT, mau_loi RE2-TT; quyết định ở LOG phiên 1 (tiếp)).

**B3. Luật chọn** (mở rộng luật cũ)
- Duyệt theo thứ tự:
  - cổng phân vị G0 < G1 < G3 < G4 < GE;
  - trong mỗi cổng phân vị, cổng đếm D0 < D1 < DE;
  - trong mỗi cặp, `verdict` V0 < V3 < V1 (bỏ V1 khi có GE hoặc DE).
- Chọn bộ đầu tiên đạt cả bốn điều kiện: (a) của cổng phân vị trên mọi ô phân vị (trừ metric Nezha-OB); (a) của cổng đếm trên các ô đếm đo được; (b) và (c1) cho từng dataset.
- GE, DE thay (a) bằng (a′) sau khóa.
- Bộ có V1 cùng G3 hoặc G4: phần p của G3 xử lý theo A3 điểm 6 trước khi xét.
- Không bộ nào đạt thì dừng, trình Minh.
- Lý do đặt cổng đếm trong cổng phân vị: (a) của hai loại cổng độc lập nhau; cổng phân vị ảnh hưởng nhiều đơn vị hơn ở R0 nên xét trước.

**B4. Bước 2 bổ sung** (khai trước khi chạy)
- G4 trên AR(1) như A7: φ ∈ {0; 0,5; 0,9; 0,98}, hai cỡ, hai hướng.
- Thêm chuỗi AR(1) φ = 0,9 cộng xu hướng tuyến tính tăng một σ mỗi 300 giây (σ là độ lệch chuẩn biên), chỉ báo cáo.
- Điều kiện đạt của G4: ở φ = 0, khoảng Wilson 99% chứa α hoặc nằm dưới α.
- D1 trên số đếm tổng hợp, cỡ 300 + 300 giây, tốc độ khai trong script:
  - Poisson (không phân tán);
  - Poisson gộp cụm: số cụm theo Poisson, mỗi cụm có số sự kiện theo phân phối hình học trung bình 3, các sự kiện của một cụm rơi trong cùng ô 10 giây.
- Điều kiện đạt của D1: với Poisson, khoảng Wilson 99% chứa α hoặc nằm dưới α. Poisson gộp cụm chỉ báo cáo.
- Test đáp án biết trước: G4 với φ̂ = 0 trùng G0; D1 với φ̂_d = 1 trùng nhị thức tới 10⁻¹²; chọn ngưỡng GE đúng trên ví dụ.

**B5. Bước 3 lại.** Lượt mới tính G4, D1 (và G0 để đối chiếu) cho cùng 52 ca và cùng cửa sổ. Ghép với p của G1, G3 ở `runs/b3-aa-001` theo (ca, cửa sổ, đơn vị, hướng); kiểm p của G0 trùng.

**B6. Kiểm sau khóa thêm.** Bộ khóa có GE hoặc DE thì kiểm thêm (a′) trên C-e; trượt thì dừng, trình Minh, không chọn lại.

### Bản 4 (người làm, 01/11/2026, sau luật chọn bản 3; theo quyền Minh giao, LOG phiên 1 (tiếp 2))

Bản 3 không có bộ nào đạt (a). Bản 4 nới (a) bằng luật khai trước dưới đây. Đây là nới tiêu chí, làm theo quyền Minh giao và ghi rõ là đặt sau khi đã nhìn số (a) ở A/A. Không đổi (b), (c1), (b′), (S), C-e sau khóa, D-2.

**C1. Chọn cổng theo minimax** (thay điều kiện (a) của luật chọn)
- Cổng phân vị g* là cổng trong {G0, G1, G3, G4} có tỷ lệ qua cổng lớn nhất trên các ô phân vị (trừ metric Nezha-OB) thấp nhất. Hòa thì theo thứ tự ưu tiên cũ. GE bị loại vì trượt ở metric RE2-TT.
- Cổng đếm c* là cổng trong {D0, D1} có tỷ lệ qua cổng lớn nhất trên các ô đếm đo được thấp nhất. DE bị loại vì trượt ở mau_thuong RE2-TT.
- Tỷ lệ qua giả còn lại của mọi ô dưới (g*, c*) được báo trong báo cáo và WHY. Không gọi g*, c* là "đã hiệu chuẩn".

**C2. `verdict`**
- Với (g*, c*), xét V0, V3, V1 theo thứ tự cũ. Chọn cái đầu tiên đạt (b) và (c1) cho từng dataset.
- Khi tới V1 mà g* là G3 hoặc G4: tinh p của G3 theo A3 điểm 6 trước khi xét. Ước lượng giờ trước; quá 1 giờ thì dừng, trình Minh.
- **V4 (phương án (B), chỉ xét khi V0, V3, V1 đều không đạt; sửa lúc 15:01, trước khi tính bất kỳ số nào của V4):**
  - CAUSE_FOUND khi tỷ lệ q_w = (số đơn vị khác nhau có F_I = 1 ở ít nhất một hướng, kể cả NEW_OP và STOPPED) / (số đơn vị có ít nhất một phép chấm hợp lệ), chỉ xét thực thể thuộc U, đạt ≥ q*.
  - q* là giá trị nhỏ nhất trong lưới {0,005; 0,010; …; 1,000} sao cho tỷ lệ CAUSE_FOUND ở cửa sổ A/A của R0 với (g*, c*) ≤ 0,20 ở mọi dataset đo được. Một q* chung cho hai dataset: đây là tham số của phương pháp.
  - Bản ghi lúc 14:58 dùng số đơn vị tuyệt đối k*. Đổi sang tỷ lệ vì số phép hợp lệ ở một cửa sổ A/A chênh 10–20 lần giữa hai dataset (bước 1: RE2-TT 456, Nezha-OB 35 ở ca thử), nên một ngưỡng tuyệt đối chung không có nghĩa. FlashTicket cũng sẽ có số đơn vị khác. Lý do này dựa trên số hỗ trợ, không dựa trên kết quả của V4.
  - V4 phải đạt (c1) cho từng dataset; không đạt thì dừng, trình Minh.
  - (b) của V4 trên A/A đạt do cách chọn, nên phép kiểm thật là (b′) trên C-e. A/A dài 150 giây có thể có ít cờ hơn cửa sổ 300 giây, nên (b′) có thể trượt; trượt thì dừng, trình Minh, không chọn lại.
- NO_INTRINSIC_ANOMALY và INSUFFICIENT_EVIDENCE giữ như V0.

**C3. Khóa.** Bộ (g*, c*, v*), kèm q* nếu là V4, ghi vào `ung-vien.json`. Hash ghi vào LOG trước khi chạy C-e.
- **Thêm lúc 15:49, sau khi V0, V3, V1, V4 đều không đạt** (theo quyền Minh giao, LOG phiên 1 (tiếp 2)): không khóa `verdict`. Khóa riêng cặp cổng (g*, c*) = (G3, D1) theo C1, ghi `ung-vien.json` kèm hash ở LOG. Rồi chạy phép sau khóa trên C-e để đo:
  - tỷ lệ qua cổng theo ô ở cỡ 300 + 300 giây, chỉ báo cáo, không có mức đạt;
  - (c2);
  - tỷ lệ CAUSE_FOUND của V0, V3, V4:q* ở C-e, chỉ báo cáo;
  - K-đủ (A5) và thang điểm (S) với cổng khóa.
  - Đề xuất WHY ở D-2 ghi `verdict` là chưa chọn được trên dữ liệu dev, kèm lý do.

## Đầu vào

- Bản ghi T-045, kiểm theo `results/T-045/manifest.json`.
- Dữ liệu dev RE2-TT 30 ca, Nezha-OB 22 ca, đọc lại chuỗi gốc qua adapter M1 khi cần; ưu tiên bản ghi cũ.
- Mốc t theo chế độ (a) (`p3.nhan.nap_moc`, chỉ mốc tiêm); C-e như T-045.
- **Không đọc:** root, loại lỗi, ô, MRR; `data/locked/`; test Nezha-OB; RE3-OB.
- Môi trường: `results/T-045/scripts/moi_truong.sh`; lệnh và script của T-045 dùng lại được (`results/T-045/scripts/`).

## Đầu ra (`results/T-046/`)

`chan-doan-cong.json` (C1), `ung-vien.json` (C2, C4; gồm hash của phần khóa), `kiem-sau-khoa.json` ((b′), (c2)), `thang-diem.json` (C3), `so-lan-nhin.jsonl`, `bao-cao.md`, `manifest.json`, `runs/`, `tests/`. Đề xuất WHY trình trong LOG.

## Phạm vi ghi

- `results/T-046/`; `tasks/T-046-cong-verdict-thang-diem/LOG.md`; SPEC này theo quyền rà và sửa ở đầu tệp (chỉ trước bước 0 của phần triển khai); dòng T-046 trong `docs/STATE.md`.
- `src/m1/` chỉ phần cổng, `verdict`, thang điểm và tham số chọn chế độ, sau điểm dừng D-2; mỗi thay đổi một commit.
- Không ghi `results/T-043/`, `results/T-044/`, `results/T-045/`, DECISIONS, WHY, MRP, KE-HOACH, task khác.

## Các bước

0. **Mở phiên.** Đọc AGENTS, STATE, SPEC này, LOG T-045 phiên 2, báo cáo T-045. Tự rà SPEC theo quyền ở đầu tệp; ghi kết quả rà vào LOG trước khi làm bước nào khác. Kiểm hash T-045; chạy test T-044 (374), T-045 (16); ghi dòng mở phiên.
1. **Kiểm dữ liệu:** độ dài trước t ở 52 ca; số đơn vị đủ hỗ trợ cho A/A theo loại và nguồn; đo chi phí G3 trên 1 ca. Thêm: s₀ và số phép A/A Nezha-OB theo A1; chi phí G3 trên dữ liệu tổng hợp (A7).
2. **Kiểm ứng viên trên dữ liệu tổng hợp:** AR(1) như SPEC T-043 dòng 415, cộng trôi bậc thang. Mục đích: xác nhận G1, G3 cài đúng và hiệu chuẩn được trong điều kiện đã biết. Điều kiện đạt theo A7.
3. **Chẩn đoán C1 trên dev** (A/A, tự tương quan) với G0, G1, G3, theo loại đơn vị và nguồn. Cửa sổ A/A theo A1; cấu hình R0 và K-đủ (A5); chẩn đoán phụ A2.
4. **Điểm dừng D-1:** trình Minh nếu đơn vị đếm qua giả nhiều hơn mức (a), cần ứng viên ngoài danh sách, hoặc một tiêu chí không đo được.
5. **Đánh giá và khóa:** tính (a), (b), (c1); áp luật chọn; ghi LOG tổ hợp đã khóa kèm hash `ung-vien.json`, **trước** khi xem C-e.
6. **Kiểm sau khóa:** (b′), (c2) trên C-e. Không đạt thì dừng, trình Minh; không chọn lại. Báo thêm (b) của K-đủ ở cửa sổ A/A (A5), chỉ báo cáo.
7. **Thang điểm:** đo C3; áp (S). Giữ S0, hoặc đề xuất S1/S2; đổi D24 thì Minh quyết. Nếu (S) mở: đề xuất ở D-2 phải định nghĩa đủ S2 (cách chặn, cách đưa về [0; 1], xử lý IQR gần 0 như fixture 76) trước mọi phép tính S2 trên dev, và chỉ lập luận bằng tính chất không nhãn (bão hòa, số thực thể hòa, so được với kênh đếm theo WHY-56, fixture); không dùng MRR, kể cả số T-045 đã biết. Báo kèm bão hòa trên đơn vị của K-đủ ở cửa sổ thật, chỉ báo cáo.
8. **Điểm dừng D-2:** trình đề xuất WHY (cổng, `verdict`, thang điểm, phần metric Nezha-OB OPEN); Minh duyệt rồi mới cài.
9. **Cài vào `src/m1`:** chế độ mới bật bằng tham số, mặc định giữ hành vi cũ. Test ở `results/T-046/tests/`. Test T-044 qua ở chế độ mặc định; `tat_dinh` qua ở chế độ mới. Khai cách T-047 bật chế độ mới mà không sửa `results/T-043/`.
10. **Kiểm hành vi bằng code đã cài:** R0 chế độ mới trên 52 ca, cửa sổ A/A và 30 C-e, không đọc root; tái lập số bước 5–7; bất biến seed 0/1/2 và thứ tự hàng ở 2 ca mỗi dataset; QT5.
11. **Báo cáo** tách quan sát, suy luận, chưa phân xử. Manifest, LOG, STATE, prompt phản biện cho Codex.

## Kiểm đúng đắn

- Bước 2 kiểm cài đặt ứng viên trên dữ liệu đã biết đáp án.
- Bước 10 tái lập số của bước 5–7 bằng code đã cài.
- Khóa trước khi xem C-e có hash trong LOG.
- Không tính MRR; mọi lần nhìn số dev ghi `so-lan-nhin.jsonl`.
- Không kiểm được: hiệu chuẩn metric Nezha-OB; trôi nền với tải đổi trên dữ liệu công khai; tính độc lập của C-e.

## Tiêu chí xong

1. Test T-044, T-045 qua ở đầu phiên và sau mỗi commit `src`.
2. C1 có kết quả theo loại đơn vị và nguồn: phân xử, hoặc "chưa phân xử" kèm bằng chứng còn thiếu. Metric Nezha-OB ghi OPEN.
3. Tổ hợp cổng × `verdict` được khóa theo luật trước khi xem C-e (có hash); kiểm sau khóa đã báo; hoặc xung đột đã trình Minh.
4. Thang điểm quyết theo (S) với bão hòa đo bằng rA = 1; đổi D24 có Minh duyệt.
5. WHY được duyệt trước khi cài; chế độ cũ không đổi hành vi (374/374).
6. Bước 10 tái lập số.
7. Không đọc root, không tính MRR; mọi lần nhìn số đã ghi.

## Không làm

Chọn E1–E5; tính MRR; sửa luật chọn khối hay ma trận T-043; hạ hỗ trợ tối thiểu; đổi kiểm định của đơn vị đếm khi chưa qua D-1; đối chứng QT7; mở test hay RE3-OB; chạy khối K.

## Chi phí ước lượng

- Ba ứng viên cổng (G0, G1, G3) × (52 cửa sổ A/A + 52 cửa sổ thật + 30 C-e). Quy tắc `verdict` tính lại từ cùng p, rẻ. Thêm K-đủ ở 52 cửa sổ A/A (A5).
- G0, G1 rẻ hơn một lượt R0 (T-045 đo khoảng 20 giây cho một cấu hình trên một ca RE2-TT). G3 với 2.000 hoán vị chưa đo; đo ở bước 1, quá 1 giờ một lượt thì báo Minh (luật cứng 8).
- Dự kiến 1–2 phiên, nghỉ ở D-2.

## Rủi ro và điều chưa chắc

- Không tổ hợp nào đạt nếu trôi nền mạnh.
- Kiểm theo khối làm yếu tín hiệu của lỗi ngắn.
- A/A 150 + 150 giây hiệu chuẩn ở cỡ mẫu khác phép thật.
- C-e chồng lấn dữ liệu chọn.
- Mọi ứng viên chưa kiểm.

## Prompt bàn giao

Prompt triển khai cho phiên Claude mới trình trong chat ngày 01/11/2026 (chép ở LOG). Cuối task, người làm soạn prompt phản biện cho Codex theo `docs/review-prompt.md`.
