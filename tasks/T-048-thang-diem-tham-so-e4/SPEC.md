# T-048 — Độ nhạy ε/α và thang điểm trong cổng mới

- **Trạng thái:** đã duyệt tạo SPEC ngày 03/11/2026. Quyền chạy theo từng phần tại B0 và mục Chi phí ước lượng.
- **Người làm:** Codex.
- **Người phản biện:** Claude.
- **Thuộc gói MRP:** P6 — **Cổng:** chuẩn bị G3.
- **Nguồn điều phối:** `docs/KE-HOACH-SAU-T047.md`, B0–B5 và bảng chạy lại có điều kiện, theo Q-235. LOG nghiệm thu T-047 và Q-234 xác định phạm vi sử dụng kết quả cũ.

## Mục tiêu

**T4** khảo sát độ nhạy của chuỗi R0 với ε và α khi đơn vị phân vị dùng G3, đơn vị đếm dùng D1, và xếp hạng dùng E4+S1. Câu hỏi là thay tham số làm đổi cờ, hạng nguyên nhân gốc và hành vi ở cửa sổ giả đến đâu. Mặc định hiện hành là ε = 0,05 và α = 0,01.

**T4b** trả lời hai vế của Q5 trong SPEC T-043. Vế (1) kiểm miền giá trị, tính hữu hạn và công thức E4/z trong cổng mới. Vế (2) đo thay đổi thứ hạng khi đổi điểm của đơn vị phân vị, trên hai nền R0 và E1+E2. Phép so chính là **E4+S1 với z+S1** trong từng nền. Báo kèm **z+S0**. Tách tác động của đổi thang khỏi tác động của bỏ khóa phụ và tìm bằng chứng về bước làm đổi hạng.

Nguồn trực tiếp là SPEC T-043 §B1.3, §B2 E4, §B3–B4, Q5, D24 và Phụ lục C, đọc cùng các đính chính đã duyệt và WHY-56, WHY-67–70. Theo WHY-69, S1 là khóa phụ độ lớn T4c trên nền E4. D24 hiện hành giữ E4 cho chuỗi chính. Q-235 cho lập kế hoạch mở rộng phép so dev sang E1+E2 và áp luật C để xác định hành động đề xuất.

T-048 phục vụ DT18-NV2/NV3, bước 2 và 4 trong hướng dẫn của cô, và phần chọn thiết kế dev của MRP P6, RQ3b. Nó cung cấp một phần căn cứ cho đối chứng QT7 của RQ3d và cho phân tích cơ chế tính điểm. RQ3a cần giao thức phát hiện, RQ3c cần bằng chứng về vùng, RQ3d cần đối chứng cấu trúc tương ứng, và RQ5 cần thực nghiệm FlashTicket. Bằng chứng dev đã dùng qua nhiều lượt thiết kế chỉ cho phép mô tả, kiểm cơ chế tính toán trong các ca quan sát và trình lựa chọn thiết kế dev. Đánh giá với baseline mạnh trên dữ liệu độc lập thuộc P7.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi và nguồn | Lựa chọn hoặc giải thích cạnh tranh | Bằng chứng phân xử | Cách đọc và phần còn mở |
|---|---|---|---|
| **T4, B4 và QT3.** Mặc định ε/α có nhạy trong G3/D1? | Giữ mặc định, hoặc trình một điểm lưới khác. Chênh MRR có thể do đổi cờ, đổi giá trị E4, một vài ca hoặc độ phủ quan sát. | Lưới đủ, ghép cùng ca. Báo thay đổi `p`, biên, cờ, tầng, khóa, RR, M5 và N1/V0. Đọc theo dataset, ô và ba thế giới. | Chỉ trình đổi theo điều kiện khai ở B1. Lưới R0 chưa cho biết thứ tự 16 cấu hình K dưới tham số khác. |
| **T4b(1), Q5 và D24.** Điểm hợp lệ và cùng cờ? | Lỗi công thức, tràn số, hoặc hành vi dự phòng làm mất tính tương đương của cặp. | Oracle tính độc lập, ca biên, và kiểm cờ, `hop_le`, ứng viên, tầng, N1/V0 theo từng ca trước khi diễn giải. | Sai công thức hoặc mất cờ thực tế chặn kết luận “chỉ đổi điểm” ở phần phụ thuộc. Báo đầy đủ bản ghi native và trình cách xử lý. |
| **T4b(2), Q5, B3–B5.** Vì sao đổi hạng? | E4 mất thông tin độ lớn khi bão hòa. z lấn át kênh đếm. Cổng quyết định tập cờ có thể xếp. Chênh có thể phụ thuộc ít ca hoặc cực trị A. | Truy vết khóa tại điểm đảo hạng và các phép phát lại chẩn đoán B4. Đọc cả ca được sửa, ca bị hỏng và ca đúng có điều kiện tương ứng. | Có thể xác nhận đường tính trên ca dev. Nếu nhiều đường cùng giải thích hoặc thiếu nhóm tương ứng, ghi OPEN và nêu phép so còn thiếu. |
| **QT7 và bàn giao K-b.** z có vai trò nào sau T-048? | Đối chứng R0, ứng viên đổi thang nền E1+E2, hoặc giữ E4+S1. | Luật C đúng chế độ trên hai cặp chính, độ bền theo ô, giới hạn C-e và bằng chứng riêng về sức mạnh đối chứng. | GIÚP trên R0 đủ để đưa z vào danh sách đối chứng QT7 theo kế hoạch. Kết luận “đủ mạnh” còn cần so baseline đơn giản công bố theo cùng giao thức. GIÚP trên E1+E2 đưa việc đổi D24 ra cho Minh quyết. |

## Đầu vào

1. **Revision phương pháp:** `6d9744ab0147dd526a0979ddcc7cc035f091d35d`, gồm C1 trên nền `c298188e`. Ghim `src/m1`, `src/m1_danh_gia`, dependency và phiên bản Python/NumPy/SciPy/pandas/PyArrow của mỗi máy. Giữ `method_version = M1-T046-1`. Ghi hash riêng của công cụ T-048 và cấu hình hiệu lực, gồm `che_do`, `nhanh_z`, tham số, trạng thái thành phần, thế giới quan sát và phiên bản đầu vào. Không dựa riêng vào `ma_noi_dung` của runner cũ để định danh cấu hình.
2. **Hợp đồng và cấu hình gốc:** `results/T-043/{hop-dong,ma-tran-thu,dinh-nghia-pha2}.json`, đính chính phiên 9–10 và `manifest.json`. Lấy R0 và E1+E2 trực tiếp từ `configs` trong `results/T-047/runs/b3-k-c1-that-001/command.json`, đối chiếu command C-e. R0 tắt E1/E2/E3/E3b/E5/E9/T12, dùng E6a. E1+E2 chỉ bật E1-U và E2-C trên nền ấy. Giữ tham số còn lại, cửa sổ, tập thực thể U, dữ liệu quan sát, alias và quy tắc giao thức. S1 ghi `thang='E4+T4c'`, S0 ghi `thang='E4'`. z bật bằng `nhanh_z=True`, vẫn giữ G3/D1.
3. **Dev chế độ (a):** 30 ca RE2-TT từ `results/T-022/allowlist-dev.json`, 22 ca Nezha-OB từ `results/T-026/allowlist-dev.json`. Ghim allowlist lần lượt bằng `results/T-022/mappings/universe-re2tt-dev.json#/nguon` và `results/T-026/runs/session-005/handoff-manifest.json#/files`. Giữ đúng 23 ô dev từ ánh xạ đã khai của pha 2/T0. C-e chỉ dùng 30 cửa sổ RE2-TT theo giao thức cũ, `t′ = t − 300`. Chỉ truyền mốc hợp lệ và đầu vào đã chuẩn hóa qua hợp đồng (a). Nhãn gốc và ánh xạ ô phục vụ chấm giữ riêng, ghép sau khi ghi hash pha 1. Giữ ca lỗi trong mẫu số theo giao thức và ghi trạng thái gốc.
4. **Đối chiếu T-047:** `results/T-047/manifest.json#/phase1` và `#/outputs`, `t1.json`, `khoi-k.json`, `so-sanh-t045.json`, `kiem-helper.json`, `runs/bo-sung-f9-f10-001/ket-qua.json`. Dùng bản ghi R0 thật/giả ở `runs/b2-c1-t1-seed0-001` và `runs/b2-c1-t1-ce-001`. Đối chiếu R0 và E1+E2 trong `runs/b3-k-c1-{that,ce}-001/theo-cau-hinh/{K-R0,K-E1+E2}/ban-ghi.jsonl`. Kiểm lại SHA-256 trước khi dùng từng đầu ra. Phần có hash lệch dừng tại phụ thuộc đó.
5. **Công cụ đọc để tái sử dụng:** `src/m1/{runner,chuoi,cong,e4,e2,xep_hang}.py`, `src/m1_danh_gia/{pha2,luat_c}.py`, `results/T-047/scripts/{adapter_t047,luat_c_t047}.py`. Adapter T-047 giới hạn T1/K và helper công khai của nó cố định `khoi_K`. Điểm nối T-048 nằm trong `results/T-048/`. Ghim các đầu vào cũ khác khi có nhu cầu dùng, kể cả bảng baseline nếu đưa ra kết luận QT7.

## Đầu ra

| File dưới `results/T-048/` | Nội dung |
|---|---|
| `manifest.json` | Revision, hash, môi trường, đường dẫn và con trỏ nguồn, lịch sử lượt và tham chiếu quyền chạy. |
| `ma-tran.json` | Ma trận đã khai, cấu hình hiệu lực, allowlist/hash, chính sách cặp, ngưỡng và biến thể chỉ báo cáo. |
| `scripts/chay.py`, `scripts/kiem.py`, `scripts/cham.py` | Điều phối chạy và lưu trung gian, oracle/kiểm tương đương, chấm và gọi luật C. |
| `runs/<run-id>/command.json`, `progress.jsonl`, `ban-ghi.jsonl`, `trung-gian.jsonl`, `kiem.json`, `stdout.log`, `stderr.log` | Lệnh, trạng thái, thời gian, bản ghi native và chẩn đoán theo ca/kênh, kiểm đối chiếu và nhật ký lỗi. Lượt lỗi giữ phần đã sinh. |
| `pilot.json` | Kiểm nguồn và tái lập, bảng khác biệt giữa máy, kết quả cache nếu có, dự toán và thời gian đã dùng. |
| `t4.json`, `t4b.json`, `luat-c.json`, `co-che.json` | Bảng theo cấu hình/ca/ô, kiểm công thức, kết cục theo thế giới, đường tính và phần OPEN. |
| `so-lan-nhin.jsonl`, `bao-cao.md` | Lịch sử xem kết quả dev. Báo cáo có đường dẫn và con trỏ JSON cho số liệu, tách quan sát, hành động theo luật và quyết định Minh. |

## Phạm vi ghi

Gói duyệt đề xuất gồm tạo `tasks/T-048-thang-diem-tham-so-e4/SPEC.md` theo bản Minh duyệt, tạo và nối `tasks/T-048-thang-diem-tham-so-e4/LOG.md`, thêm hoặc cập nhật đúng dòng T-048 trong `docs/STATE.md`, và ghi các file kết quả liệt kê ở trên. `<run-id>` là mã riêng cho mỗi lượt. Danh sách này bao gồm file xuất kết quả lỗi.

Phần chạy thử EC2 cần quyền riêng trong lời duyệt. Đề xuất dùng thư mục mới `~/rca-t048/` trên **đúng instance Minh xác nhận**. Phạm vi ghi từ xa gồm bản sao nguồn/hợp đồng và công cụ đã ghim trong `~/rca-t048/work/`, môi trường Python riêng `~/rca-t048/.venv/`, các file đầu vào dev liệt kê từng đường dẫn trong manifest chuyển dữ liệu tại `~/rca-t048/staging/`, và file lượt chạy cùng cấu trúc trên tại `~/rca-t048/work/results/T-048/runs/<run-id>/`. Danh sách file, tổng byte và hash chốt trước khi chuyển. Chỉ sao chép danh sách dương từ allowlist, gồm đúng các đoạn nguồn Nezha phục vụ ca dev đã chọn. Nếu một file gốc chứa cả phần ngoài dev, phải chứng minh và kiểm tương đương bản trích dev được phép trước khi chuyển. Khi chưa có cách tách đã kiểm, phần EC2 phụ thuộc dừng ở đó.

Đề xuất đổi D24, tham số, cách xử lý lỗi, hoặc căn cứ mới trong WHY/DECISIONS được trình riêng với nội dung cụ thể. Quyền ghi bản phản biện do Minh cấp cho Claude theo lượt.

## Các bước

### B0. Kiểm nguồn, thử máy và tái lập

- Kiểm revision, hash, đường dẫn đã resolve, allowlist và số ca. Dùng đầu vào chỉ đọc. Kiểm cấu hình thực tế của EC2, CPU/RAM, ổ trống, loại lưu trữ, hệ điều hành, dependency, số worker và giá giờ máy áp dụng. `data/README.md` phân biệt máy T-007 và máy dùng cho T-003. “EC2 cũ” chưa đủ để suy danh tính, cấu hình hay giá.
- **Pilot đề xuất:** lấy trước khi chấm tối đa 6 ca thật, ba ca mỗi dataset đại diện đầu vào nhẹ, vừa và nặng theo byte hoặc số mẫu, phá hòa bằng ID mờ. Thêm C-e tương ứng cho ba ca RE2-TT. Cùng danh sách, revision, seed, cấu hình và số worker đã ghi trên hai máy. Chạy R0 mặc định và lát cắt có chi phí đại diện gồm một ε biên, hai α cùng ε, và z+S1 trên E1+E2. Đo từ đọc dữ liệu tới ghi kết quả, tách khởi tạo/chuyển dữ liệu, trích đặc trưng, G3/D1, xếp hạng, ghi và chấm. Ghi cold/warm, wall time, CPU, peak RAM, dung lượng và mức song song thực tế. Chọn lát cắt nhỏ hơn trước khi chạy nếu cần giữ ngân sách, ghi rõ phần chưa đo và độ bất định tăng thêm.
- So laptop/EC2 trên cùng cấu hình theo ca và thế giới: trạng thái, U, nhóm hòa có thứ tự, tầng, khóa số, `F_raw/F_I`, `hop_le`, tập cạnh E2 có cờ, `verdict`, N1, V0. Chuẩn hóa riêng metadata máy, đường dẫn và thời gian. Khóa so chính xác nếu biểu diễn cho phép. Mọi sai số số thực phải được báo kèm trường chịu ảnh hưởng và kiểm quan hệ thứ tự/hòa. Không dùng dung sai tổng hợp để bỏ qua đảo hạng, đổi cờ hoặc qua ngưỡng.
- Trước phép so chính thức, chạy lại **đủ 52 ca thật và 30 C-e của R0 mặc định** trên máy chọn. Đối chiếu với T1 và K-R0 T-047 ở toàn bộ trường quyết định chung vừa nêu, rồi tái lập bảng MRR/Hit@k, M5, N1/V0 và mẫu số. Pilot chỉ chứng minh trên tập con. Nếu lệch, lần theo input/adapter, số học và nhánh cổng. Nếu cần phép so tiếp, chạy cả hai vế trên một máy, cả đối chứng E4. Cách đó giữ được cặp nội bộ nhưng chưa xác lập tương đương với nền T-047. Lệch ảnh hưởng kết cục, hoặc lệch chưa giải thích, chặn diễn giải kế thừa T-047 và bàn giao T-049 cho tới khi Minh xử lý. Báo hai tập bằng chứng riêng.
- **Cache α là ứng viên.** Đọc cache sẵn của E4/G3 trước. Chỉ tái dùng `p` tại cùng ε và khóa giữ nguyên mẫu và mốc N/A, hướng, cửa sổ/biên khối, seed và quy tắc G3/G0, mọi tham số ảnh hưởng `p`, và với D1 cả phơi nhiễm theo thế giới, `φ` và đầu vào đếm. Tính lại so ngưỡng strict `p < α`, cờ và mọi phụ thuộc xuôi dòng. Không tái dùng `p_G3` qua ε vì biên vượt tham gia phép tính. Đối chiếu lượt cache với lượt riêng tắt tái dùng trên pilot, các thế giới, ca sát α và nhánh dự phòng. Yêu cầu trùng `p` ở cùng khóa và trùng cờ, khóa, hòa, thứ hạng, N1/V0. Khi dùng trên toàn bộ, đối chiếu lại lát cắt đã khai và giữ log hit/miss. Sai một trường quyết định thì dùng đường chạy riêng và cập nhật dự toán. Chỉ tính lợi ích theo thời gian cả đợt đã đo.

### B1. T4 — độ nhạy trên R0

| Nền | Điểm và khóa | Lưới | Dữ liệu |
|---|---|---|---|
| R0 | E4+S1 | ε ∈ {0, 0,05, 0,2} × α ∈ {0,001, 0,01, 0,05} | 9 × 52 cửa sổ thật và 9 × 30 C-e, đủ P/S_lo/S_hi theo hợp đồng |

Dùng lại lượt tái lập mặc định nếu khớp toàn bộ cấu hình và trường cần phân tích. T4c là khóa phụ lấy từ cùng lượt chấm, lưu cả khóa trước và sau khi thêm `m`. Báo MRR chính, Hit@1/3/5, NDCG@5, Retrieval@5, Rerank@1, RR theo ca, M5 và thay đổi cờ. N1 là số thực thể tầng 1. V0 báo theo `verdict`, gồm tỷ lệ `CAUSE_FOUND`, số `INSUFFICIENT_EVIDENCE` và mẫu số hợp lệ C-e. Tách bảng thật và giả. Hòa tính theo kỳ vọng. ERROR/UNSUPPORTED xử lý theo hợp đồng, giữ trong bảng trạng thái và mẫu số chấm tương ứng.

**Điều kiện đề xuất đổi, chờ Minh duyệt cùng SPEC:** giữ mặc định trừ khi một điểm lưới tăng MRR gộp **> 0,01**, số ô tăng RR lớn hơn số ô giảm, không dataset nào giảm quá `1/n_d`, và hướng kết luận giữ ở ba thế giới. Đề xuất đổi còn cần chuỗi cờ/khóa giải thích kết quả, không tăng M5 trên từng dataset, không có tăng V0 `CAUSE_FOUND` hoặc N1 trung bình ở C-e ghép hợp lệ, và báo rõ thay đổi coverage/mẫu số. Thiếu cặp C-e hợp lệ hoặc kết quả tập trung vào ít ca thì ghi giới hạn và giữ mặc định trong đề xuất. Đây là tiêu chuẩn trình thay đổi thận trọng trên dev, không phải luật chọn tự động hoặc kiểm định. Báo cả chín điểm và mọi ứng viên đạt, không chọn theo mức đồ thị hơn R0.

Xác nhận ε/α dùng cho T4b trước khi dùng kết quả T4b để trình chọn thang. Giữ mặc định đã có là đường tiếp theo khi chưa có đề xuất đổi. Nếu Minh chọn giá trị khác, dừng phần chọn thang phụ thuộc để xác nhận chi phí, làm lại các kiểm T1 cần thiết và tái lập các vế E4 tại giá trị mới. E1+E2 lúc đó chỉ là nền so cố định cho T4b. Bộ chọn K phải được chạy lại trên nền cuối trước khi chuyển bước.

### B2. T4b(1) — công thức và ngoại lệ

- Dựng oracle theo hướng trên cùng mẫu hữu hạn. Với phân vị, đối chiếu tỷ phần vượt biên `r_A`, `r_N`, `e = max(0,r_A−r_N)` và điểm dùng sau cổng. Điểm E4 từng kênh phải hữu hạn trong `[0,1]`. Kiểm E4 ở đơn vị đếm theo nhánh D1 và giữ đúng nhánh trực tiếp NEW_OP/STOPPED. Miền `[0,1]` áp cho điểm từng kênh E4.
- Với z, đối chiếu float64, trung vị N, IQR nội suy tuyến tính, `c = IQR` khi `IQR ≥ 10·eps_machine`, còn lại `c = 1`. Điểm theo hướng là `max(A − med_N)/c` hoặc `max(med_N − A)/c`. Điểm được dùng phải hữu hạn. Kiểm hướng, IQR bằng 0/sát biên, IQR nhỏ, trùng mẫu, điểm lớn và mẫu hữu hạn cực trị có thể tràn khi trừ, tính phân vị hoặc chia. Báo phân bố z theo nền IQR, kể cả cực trị A và nhánh `c=1`. Công thức này kiểm quy tắc chuẩn hóa ghi trong SPEC T-043. Phép so BARO đầy đủ có giao thức riêng.
- **Kiểm ngoại lệ trước khi đọc N1/V0.** `chuoi.py` hiện đánh dấu `hop_le=False` nếu một trong hai hướng z không hữu hạn và xóa `F_raw` cùng điểm của hướng đang có cờ. Điều này có thể đổi tập cạnh có cờ, tầng hoặc `verdict` ngay cả khi hướng đang dùng có giá trị hữu hạn. Kiểm cả fixture cực trị và toàn bộ bản ghi dev thật/giả. Lưu cờ và trạng thái trước/sau thay điểm theo từng hướng, rồi đối chiếu ứng viên, N1 và V0 từng cửa sổ. Nếu xảy ra khác biệt thực tế, báo native riêng và chỉ gọi phép so điểm thuần ở nơi đã chứng minh cùng cờ. Không bỏ ca khỏi bảng chính, không thay NaN/Inf bằng một điểm tự chọn. Phần quyết định phụ thuộc dừng để Minh chọn sửa đặc tả/cài đặt hoặc chấp nhận giới hạn mô tả.

### B3. T4b(2) — ma trận ghép cặp

| Nền cố định | Tham chiếu | Vế chính | Báo kèm | Dữ liệu |
|---|---|---|---|---|
| R0 | E4+S1 | z+S1 | z+S0 | 52 thật + 30 C-e |
| E1-U+E2-C | E4+S1 | z+S1 | z+S0 | 52 thật + 30 C-e |

Giữ ε/α đã xác nhận, cùng cửa sổ, U, giao thức, ba thế giới và xử lý lỗi. Dùng lại E4+S1 của B0/B1 hoặc T-047 chỉ khi thỏa điều kiện tái lập, cùng máy theo quy tắc B0 và đủ trường cho B4. Nếu thiếu thì chạy lại đúng vế. Báo cùng bộ độ đo B1, thêm ΔRR, ca được sửa/ca đúng bị hỏng và chuyển nhóm hòa. Báo riêng z+S1 so với z+S0 để đọc ảnh hưởng khóa phụ dưới z. Chênh giữa hai nền mô tả tương tác với cả gói E1+E2.

### B4. Phân xử cơ chế theo ca và kênh

**Trung gian bắt buộc.** Ghi ID mờ, dataset, cửa sổ, thế giới, cấu hình, U và trạng thái quan sát. Với mỗi đơn vị/hướng lưu loại phân vị/đếm, nguồn, thực thể/cạnh, hash và con trỏ mẫu N/A, cỡ mẫu, biên, `r_A/r_N`, `e` thô và hiệu lực, `p`, cách cổng, fallback G3→G0, `φ`, số đếm và phơi nhiễm D1, trung vị, IQR, `c`, cực trị, z hai hướng và tính hữu hạn, `m` T4c, cờ trước/sau và nguồn khóa. Lưu `r_A=1` riêng với `e=1`. Lưu tập cạnh có cờ, gán E2-C và điểm đã gán. Theo thực thể, lưu `F_raw/F_I`, tầng, `K_raw/K_I`, khóa S0/S1 có thứ tự, kênh đạt max, kênh đóng góp `m`, số kênh, tổng điểm, nhóm hòa, hạng, N1/V0. Tham chiếu mẫu từ nguồn dev đã ghim. Với ca cần giải thích, giữ đủ giá trị đã đưa vào công thức để replay độc lập.

R0 dựng cạnh quan sát nhưng E6a trên R0 xếp bằng điểm cục bộ. E1 dùng quan hệ cha–con trong trace để tính thời lượng riêng. E2 dùng cạnh gọi có hướng và mẫu span bọc để gán tín hiệu cạnh có cờ theo E2-C. Log và metric đóng góp ở thực thể phát/chủ sở hữu theo hợp đồng. Giữ bằng chứng từng bước gán. Trong cùng nền, một thay đổi ở kênh cạnh phải được truy tới thực thể nhận điểm trước khi quy cho khóa E6a.

**Phép so tối thiểu bổ sung vào kế hoạch B4, xin duyệt trong SPEC này:**

1. **Tách khóa phụ.** Phát lại E4+S0 từ đúng bản ghi E4+S1 bằng cách tính lại khóa, sắp và gộp hòa. Kiểm replay native E4+S1 và z+S1/z+S0 trước. Như vậy có bốn ô điểm × khóa phụ trên cùng cổng, gồm một ô chẩn đoán không cần đọc lại raw. S1 sắp `(max điểm, m, số kênh, tổng điểm)`. `m` có thể phân xử một số ca bằng nhau ở `max điểm`. Chỉ so E4+S1 với z+S0 sẽ trộn hai thay đổi.
2. **Kiểm mất thông tin do bão hòa.** Tìm cặp root–đối thủ có cùng tầng, `r_A=1`, điểm E4 tối đa bằng nhau hoặc mất phân biệt ở biên vượt, và độ lớn khác nhau. Đọc thành phần khóa đầu tiên gây đảo hạng, kể cả `r_N` và `m`. Phát lại thay điểm phân vị bằng z **chỉ trên nhóm bão hòa**, giữ cờ, kênh đếm và S1, rồi đối chiếu nhóm phân vị chưa bão hòa và ca đúng có điều kiện tương ứng. Nếu bão hòa đã được `m` phân xử hoặc phép thay chỉ có tác dụng khi đưa một cực trị A vào max, ghi riêng kết quả đó. Chỉ thấy `r_A=1` cùng ΔRR chưa đủ quy cơ chế.
3. **Kiểm lấn át kênh đếm.** Tìm đảo hạng có hai loại bằng chứng cùng cạnh tranh trong tầng, kênh đếm giữ nguyên giá trị/cờ, và điểm z phân vị trở thành thành phần đầu tiên thắng khóa của đối thủ dựa vào kênh đếm. Phát lại khóa giữ cờ và gán cạnh, đưa nhóm phân vị gây đảo hạng về điểm E4, rồi so lại hạng. Kiểm cả ca z giúp và hại. `z > 1` riêng lẻ chưa đủ. Một đảo hạng có thể đồng thời có bão hòa và lấn át. Báo phần chồng lấn theo ca.
4. **Kiểm giải thích do cổng và do mẫu.** Cặp chính giữ G3/D1. Nếu các tập cờ bằng nhau, cổng không đổi giữa hai vế, song nó vẫn có thể tạo bối cảnh để z giúp hoặc hại. T4 cho biết độ nhạy ở cổng mới. Bảng T-047 có E4 theo hai gói cổng nhưng thiếu z ghép cùng S1 trên cổng cũ. Vì vậy tác động tương tác **gói cổng × điểm** còn OPEN nếu kết luận cần đến nó. Phép bổ sung tối thiểu là thêm z+S1 ở G0/D0 và ghép với E4+S1 cùng gói trên các ca đã khai, cùng revision, rồi mở rộng tập ca nếu cần kết luận theo ô. Cần trình quyền và chi phí riêng. Để đọc sự phụ thuộc mẫu, báo kiểm dấu, bootstrap ghép theo ô, bỏ lần lượt một ô, ảnh hưởng của cực trị A và ca đúng tương ứng. Các phép này đo độ mong manh trên dev. Dữ liệu độc lập cần thiết để kiểm khả năng lặp lại.

Phát lại chẩn đoán giữ cờ, U và dữ liệu quan sát. Với thay điểm trên cạnh, kiểm lại đường gán E2-C hoặc chứng minh tập gán giữ nguyên trước khi replay khóa. Chỉ dùng các lượt phát lại để xác định bước đổi khóa. Chúng không thêm cấu hình ứng viên vào luật chọn.

### B5. Luật C, hành động và bàn giao

Gọi `pha2.ket_cuc_cap` và phần kết hợp thế giới với `buoc='luat_C'`. Dùng **cả 23 ô** làm `E_X` trong mỗi cặp T4b, đối chiếu tập ô ghim của T0/pha 2 trước chấm. Số ô có cờ hoặc có đổi hạng báo riêng. Không dùng wrapper T-047 cố định `khoi_K`. UV-6 chỉ cho E3 và vế M5 riêng chỉ cho E5. Với phép đổi điểm, M5 vẫn là đại lượng mô tả.

Áp thứ tự Phụ lục C, với `δ=0,01`, `δ_d=1/30` và `1/22`. HẠI riêng nếu tất cả ô lệch đều giảm và có ít nhất ba ô giảm. Kế tiếp là trái chiều theo dataset, hại gộp, thiếu ô, giúp, không tác dụng, rồi trái chiều theo ô. GIÚP cần ΔMRR gộp `> δ`, `P > M` và không dataset nào giảm vượt `δ_d`. Báo kết cục P/S_lo/S_hi trước khi áp xử lý phụ thuộc quan sát. Nếu thế giới khác P thì kết hợp theo `luat_C` thành **KHÔNG ĐỦ CA**, giữ kết cục P trong báo cáo. Với `E_X=23`, nhánh ít hơn 6 ô không kích hoạt trên tập hợp lệ đã khai. Báo kèm kiểm dấu, khoảng bootstrap theo ô, độ nhạy δ = 0,005/0,02.

**Mốc giả.** Báo N1/V0 và mẫu số theo cửa sổ. Khi đối chiếu xác nhận z giữ cờ, độ hợp lệ và tầng, ghi **“không phân xử được do cấu tạo phép thử”** và không đưa vế C-e vào HẠI riêng. Mẫu số bằng 0 ghi thêm **“chưa kiểm được”**. Nếu ngoại lệ z làm đổi cờ hoặc độ hợp lệ, áp B2 và báo thay đổi thật. Không kế thừa ngưỡng N1 của Q-231 sang phép này hoặc suy đã đạt chuẩn mốc giả.

| Kết cục quan sát của z | Hành động trên R0 | Hành động trên E1+E2 |
|---|---|---|
| GIÚP | Đưa z vào danh sách đối chứng QT7. Trước khi gọi đối chứng đủ mạnh, kiểm cùng dữ liệu, quy tắc chấm và baseline công bố tương ứng. | Dừng chọn nền, trình Minh có đổi D24 hay giữ E4+S1. Nếu đổi, chạy lại K. |
| HẠI riêng hoặc HẠI gộp | Giữ E4, báo điều kiện hại. | Giữ E4, báo điều kiện hại. |
| TRÁI CHIỀU | Trình Minh. Mặc định giữ E4, kèm cờ và nhóm xung đột. | Trình Minh. Mặc định giữ E4, kèm cờ và nhóm xung đột. |
| KHÔNG TÁC DỤNG | Giữ E4, báo mức thay đổi quan sát. | Giữ E4, báo mức thay đổi quan sát. |
| KHÔNG ĐỦ CA hoặc phụ thuộc quan sát | Giữ E4, ghi chưa phân xử. | Giữ E4, ghi chưa phân xử và trình Minh. |

**Chạy lại theo phụ thuộc.**

- Đổi ε/α: so lại cờ, độ hợp lệ, ứng viên, tầng và hành vi thật/giả tại R0. Khi cờ hoặc trạng thái phụ thuộc đổi, kiểm lại T1 từ đầu ở tham số mới, gồm bất biến seed/xáo hàng, QT5 và C-e. Ngay cả khi cờ giữ nguyên, kiểm lại các đại lượng T1 chịu ảnh hưởng bởi thay điểm/khóa trước khi dùng chúng. Chạy lại toàn bộ khối K ở tham số mới vì T4 trên R0 chưa kiểm phản ứng của các thành phần K.
- Đổi thang điểm: khi đã chứng minh chỉ đổi điểm và giữ cờ, dùng lại phần kiểm T1 về cổng/cờ và giữ T4 như kết quả của thang đã khảo sát. Kiểm lại điểm, khóa, bất biến hạng và điều kiện hữu hạn trên thang mới. Khi cờ hoặc độ hợp lệ đổi, kiểm lại T1 phụ thuộc như trên. Chạy lại K với thang mới rồi làm các bước sau trên nền mới. Nếu cần tuyên bố độ nhạy ε/α của thang mới, lưới E4 hiện tại chưa trả lời câu đó.
- Mỗi lượt chạy lại K cần SPEC riêng theo kế hoạch. T-049 được chuẩn bị công cụ với nền để trống. Chỉ chạy chính thức K-b/T6 khi Minh xác nhận bộ tham số, thang điểm và quyền dùng cấu hình K tương ứng, đã xử lý các cờ bước 8/E5 và giới hạn C-e có liên quan của T-047, và đã có lượt K mới nếu nền đổi. T-047 đã nghiệm thu chạy/kiểm/phân tích dev. Quyền dùng E1+E2 làm nền task tiếp theo vẫn là quyết định riêng.

## Kiểm đúng đắn

- Kiểm cấu hình hiệu lực và bản ghi theo từng ca, đủ tập ID, đủ thế giới, đúng cặp và đúng mẫu số. Kiểm pha 1 chạy với nhãn chấm tách khỏi phương pháp. Ghi hash trước pha 2. Tái lập số T-047 đã dùng làm đối chiếu từ bản ghi và hàm chấm, ghi con trỏ nguồn. Nếu dùng bảng baseline cho QT7, kiểm hash và tái lập đúng các dòng được trích.
- Kiểm oracle độc lập và bất biến khi đổi thứ tự biểu diễn. So công thức, cờ, trạng thái, tầng, khóa và hòa trước khi tin điểm tổng. Theo QT5, soi điểm cực lớn, toàn hòa, ngưỡng lớn và trường hợp một nhóm kênh chiếm ưu thế.
- Hồi quy luật C bằng đầu vào giả trong `scripts/kiem.py`. Có cặp ba thế giới khác nhau để phân biệt `luat_C` với `khoi_K`. Kiểm đúng 23 ô và mẫu số, thứ tự HẠI riêng → trái chiều dataset → hại gộp, các biên strict, hai vế UV-6/E5 không áp, C-e không phân xử và mẫu số 0. Kiểm kết quả theo thế giới, kết cục kết hợp và hành động theo bảng riêng.
- Khi phân tích sai, tách dữ liệu/thiếu tín hiệu, giao thức, adapter/cài đặt và giả định của điểm. Đối chiếu ca đúng có điều kiện tương ứng. Nếu thiếu tín hiệu được xác nhận, chỉ nêu yêu cầu quan sát FlashTicket rút ra từ đúng tín hiệu thiếu và hệ quả đối với phép đánh giá. Không cộng nhóm chồng lấn thành tỷ lệ nguyên nhân.

## Tiêu chí xong

1. **Nguồn và máy:** hash, cấu hình và tập ca đã kiểm. R0 thật/giả tái lập trên máy chạy hoặc sai khác đã được định vị, ghi hậu quả và xử lý phần phụ thuộc theo B0. Có pilot và dự toán từ đo cả đợt. Cache chỉ được tính vào chi phí nếu đã kiểm tương đương.
2. **ε/α:** đủ lưới T4 với ca, ô, thế giới và cửa sổ giả. Có đường tính cho chênh quan trọng và quyết định giữ mặc định hoặc hồ sơ trình đổi theo điều kiện khai trước. Chốt giá trị dùng trước kết luận T4b.
3. **z:** kiểm công thức và miền điểm, xác định có hay không có trường hợp mất cờ/độ hợp lệ trên dev. Với cặp được diễn giải là đổi điểm, chứng minh cờ, tầng, U và điều kiện C-e tương ứng. Nếu có sai khác, ghi đúng kết luận bị chặn.
4. **Cơ chế:** có cặp chính và báo kèm, replay khớp native, và bằng chứng theo ca chỉ được khóa/kênh đổi hạng. Với mỗi nhóm quan trọng, báo kết quả hỗ trợ, bác bỏ hoặc chưa phân xử bão hòa/lấn át/cổng/phụ thuộc mẫu. Mỗi OPEN chỉ rõ trường thiếu, phép bổ sung và quyết định phụ thuộc. Có thể nghiệm thu phần mô tả dev khi cơ chế còn OPEN.
5. **Luật và bàn giao:** hồi quy phân biệt hai chế độ helper đạt, kết cục và hành động tách rõ. Bàn giao nêu điều kiện dùng nền và nhánh chạy lại K/T1. Kiểm toàn bộ diff, đúng file, hash đầu ra, LOG và dòng STATE. Trình Claude soát kết quả qua prompt mẫu để Minh chuyển.

## Không làm

G3, test, dữ liệu khóa, dataset giữ ngoài, hiệu chuẩn `verdict`, chế độ (b), K/K-b/T6 chính thức, đối chứng cấu trúc hoàn chỉnh, thử FlashTicket và kết luận hiệu quả P7 nằm ngoài lượt này. Nếu cần phân xử cổng × điểm, hoặc xác nhận sức mạnh QT7 vượt phần baseline đã ghim, trình phép bổ sung theo B4/B5. Tách phần chạy lại thành task theo kế hoạch đã chốt.

## Chi phí ước lượng

- **Pilot, đề xuất xin duyệt:** tối đa **45 phút chạy/đo trên EC2 và 45 phút trên laptop**, tính cả thử thất bại và kiểm cache. Tổng phần kết nối, chuẩn bị, chuyển và chạy trên EC2 đề xuất tối đa **60 phút hoạt động**. Chốt chi phí tiền sau khi xác nhận instance và đơn giá, trước khi thực hiện phần tính phí. Đo byte trước khi chuyển. Vượt giới hạn đã duyệt hoặc cần tải hơn 5 GB thì trình Minh trước.
- **Lượt dài:** 4,5–6 giờ là dự báo laptop trong kế hoạch, chưa đo và chưa phải trần. Ma trận có tối đa **15 × 82 = 1.230 lượt cấu hình–cửa sổ** trước tái sử dụng, gồm 9 cấu hình T4 và 6 vế T4b. R0 E4+S1 mặc định trùng giữa hai bước nếu giữ tham số, nên còn **14 × 82 = 1.148** trước các tái sử dụng khác. Tính riêng lượt khôi phục, tái lập, replay, ghi trung gian và kiểm. Sau pilot, ngoại suy theo dataset, kích thước ca, nhánh cổng, số worker thực đo và thời gian I/O. Báo khoảng dự toán và điều kiện dễ vượt. Trình Minh **trần wall time, số worker, chi phí EC2 và phạm vi lượt dài** trước khi chạy chính thức. Q-40 là chuẩn so ngân sách từng phương pháp trên từng dataset. Trần T-047 ở Q-233 chỉ thuộc T-047.
- Tách phần pilot và phần thực nghiệm dài thành hai phần có thể duyệt riêng trong cùng đề xuất. Ghi checkpoint đủ để chuyển phiên nếu đo cho thấy công việc không vừa một phiên. Tách task mới nếu phát sinh chạy lại K hoặc cần thiết kế phép kiểm ngoài ma trận đã duyệt.

## Rủi ro và điều chưa chắc

- **OPEN về EC2:** danh tính instance, quyền dùng thư mục, cấu hình, chi phí, tương đương đầu ra và dung lượng dev có thể chuyển nguyên trạng đều chờ xác nhận. Những phần này ảnh hưởng quyền chạy pilot và dự toán.
- **Cache chưa kiểm:** giả định α chỉ đổi ngưỡng sau khi tính `p` trong khóa cố định. Sai nếu khóa bỏ sót đầu vào hoặc tái sử dụng kết quả đã áp α. Kiểm trong pilot. Lợi ích thời gian còn OPEN đến lúc đo.
- **z chưa kiểm trên dev ở cổng mới:** phân tích code xác định nhánh mất cờ có tồn tại. Tần suất và ảnh hưởng thực tế còn OPEN. Nếu phát sinh, điều kiện áp vế mốc giả và phép so thuần điểm bị ảnh hưởng.
- **Giới hạn dữ liệu:** chỉ 23 ô dev đã được nhìn qua nhiều lượt. Mốc giả RE2-TT là đại lượng gián tiếp ở chế độ (a). Bằng chứng cơ chế trên ca và độ bền theo ô chưa xác nhận lợi ích trên dữ liệu độc lập. Phép thử bão hòa/lấn át có thể cùng khớp. Khi thiếu ca hoặc thiếu tương phản, ghi nhóm còn thiếu và giữ quyết định phụ thuộc OPEN.

## Prompt bàn giao

Dùng prompt soát SPEC dưới đây khi Minh chuyển cho Claude. Khi có kết quả, dùng đúng khối soát kết quả và khối G3 trong `docs/review-prompt.md`, theo quyền ghi của lượt đó.
