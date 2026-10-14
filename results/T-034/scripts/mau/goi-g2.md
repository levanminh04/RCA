# Gói trình G2 (T-034): baseline trên dev, bản đồ hạn chế, căn cứ cho bước đồ thị

Ngày 13/10/2026. Người làm: Claude. Người phản biện kết quả: Codex. Trạng thái: chờ phản biện, chờ Minh duyệt.

**Minh cần duyệt gì ở cổng này** (MRP §7, cổng G2): bảng baseline trên dev (mục 2) và bản đồ hạn chế (mục 3). Các điểm cần quyết thêm nằm ở mục 8.

**Cách đọc.**

- Mọi số là trên phần **dev**: {{bl.re2.n}} ca RE2-TT (hệ Train Ticket) và {{bl.nz.n}} ca Nezha-OB (hệ Online Boutique). Chưa mở test và dataset giữ ngoài.
- *Root* là thành phần gốc gây lỗi theo nhãn. *Ô* là một cặp (root, loại lỗi). *Chế độ (a)*: phương pháp xếp hạng được cho biết mốc tiêm lỗi. *Chế độ (b)*: bộ phát hiện tự báo động, rồi phương pháp xếp hạng chạy tại báo động đầu.
- *Hit@1* là tỷ lệ ca root đứng hạng 1; khi hòa thì tính kỳ vọng. Ca không chạy được vẫn nằm trong mẫu số và tính trượt.
- Mỗi kết luận ghi một **mức bằng chứng** (WHY-51): **CT** can thiệp (đổi có kiểm soát một đầu vào hay một bước, xem đầu ra của chính phương pháp); **ĐC** đo trực tiếp đại lượng mà cơ chế giả định; **LĐ** liên hệ có đối chứng; **MT** mô tả; **CK** chưa kiểm.
- Câu “vì sao” có ba trạng thái: *đã xác lập ở mức X*, *đã loại giải thích Y*, *chưa phân xử vì Z*.
- Mọi con số trong file này được điền bằng máy từ file kết quả. Sổ (file, con trỏ JSON) của từng số: `results/T-034/runs/g2-build-008/render/registry.json`. Kết quả kiểm: `results/T-034/runs/g2-build-008/v4.json`. Bản này đã sửa sáu lần sau phản biện ngày 13/10/2026 và 14/10/2026; các bản trước lưu ở `results/T-034/runs/phat-hanh-001/` đến `phat-hanh-006/`.

## 0. Tóm tắt ba câu

**Câu 1 — Phương pháp nào tốt trong điều kiện nào.** Chỉ đọc theo ô và theo ca (mục 2).

- *RE2-TT, chế độ (a).* Theo điểm ước lượng, hai dòng đầu bảng là TORAI B (Hit@1 {{bl.re2.torai_B.h1:.3f}}) và SimpleRCA ({{bl.re2.simplerca.h1:.3f}}); khoảng bootstrap của bốn phương pháp đứng đầu chồng nhau, nên thứ tự giữa chúng chưa chắc. SimpleRCA không dùng quan hệ gọi. Ở TORAI B, bước nhân quả (RCD) không quyết định hạng của root ở đơn vị nào (G2-H15); khâu dựng bảng trace của nguồn B thì có dùng quan hệ cha–con của span. TORAI B đúng mọi ca ở {{dx.re2.torai_B.full}}/{{dx.re2.torai_B.cells}} ô, SimpleRCA ở {{dx.re2.simplerca.full}}, BARO ở {{dx.re2.baro.full}}, TraceRCA ở {{dx.re2.tracerca.full}}, CIRCA ở {{dx.re2.circa_ols_da.full}}, MicroRank ở {{dx.re2.microrank_full.full}}.
- *Không phương pháp nào tốt ở mọi ô.* Ở ô auth/delay BARO không đúng ca nào, trong khi SimpleRCA, TraceRCA và TORAI B đúng cả ba. Ở ô train/delay thì ngược lại: SimpleRCA chỉ đúng một ca, BARO và TORAI B đúng cả ba. Ở ô order/loss TraceRCA không đúng ca nào.
- *Nezha-OB, chế độ (a).* Mọi phương pháp chạy được đều yếu: BARO {{bl.nz.baro.h1:.3f}}, SimpleRCA {{bl.nz.simplerca.h1:.3f}}, TraceRCA {{bl.nz.tracerca.h1:.3f}}, MicroRank {{bl.nz.microrank_full.h1:.3f}}. CIRCA và TORAI B không chạy được trên dữ liệu này (Q-85). Với lỗi return, BARO, SimpleRCA và TraceRCA đúng {{dx.nz.baro.f.return.h1}}, {{dx.nz.simplerca.f.return.h1}} và {{dx.nz.tracerca.f.return.h1}} trên {{dx.nz.baro.f.return.n}} ca. Với lỗi trễ mạng: {{dx.nz.baro.f.network_delay.h1}}, {{dx.nz.simplerca.f.network_delay.h1}} và {{dx.nz.tracerca.f.network_delay.h1}} trên {{dx.nz.baro.f.network_delay.n}} ca.
- *Chế độ (b), RE2-TT.* Báo động đầu nằm ở hoặc sau mốc tiêm ở {{bl.det.bocpd.first_ok}}/{{bl.det.bocpd.n}} ca với BOCPD và {{bl.det.nsigma.first_ok}}/{{bl.det.nsigma.n}} ca với N-Sigma. Vì vậy thành công chung (phát hiện đúng rồi xếp đúng) cao nhất chỉ {{bl.b.baro_bocpd.joint1:.3f}}.

**Câu 2 — Thất bại ở đâu.** Bản đồ ở mục 3 có {{map.rows}} dòng. Tách theo nguồn:

- *Do bản cài trong thư viện hoặc đầu vào ta dựng:* bước chia trace của MicroRank (G2-H01); cách TraceRCA bản thư viện chấm thời gian chờ (G2-H03, G2-H04); bảng log của TORAI nguồn B (G2-H14); tiền xử lý nhìn cả bản ghi của BOCPD (G2-H20).
- *Do cách tính của phương pháp:* thang IQR của BARO (G2-H09); phiếu metric đếm theo mẫu của SimpleRCA bản M4 theo quy ước T-017 (G2-H08); phần dư gần bằng không cho điểm cực lớn ở CIRCA, rồi bước DA truyền điểm đó (G2-H12, G2-H13).
- *Do dữ liệu:* nền ngắn và metric thưa ở Nezha-OB; root không được dịch vụ nào gọi; không có onset và nền sạch được xác nhận độc lập (G2-H19, G2-H24).
- *Chưa phân xử:* vì sao hai bộ phát hiện báo trước mốc (G2-H21, G2-H22); vì sao dịch vụ không liên hệ với root đổi tại mốc (G2-H11); câu “lan có đáng kể” (mục 4).

**Câu 3 — Hạn chế nào cần bước đồ thị (P5/P6) giải quyết.** Mục 5 trình các ứng viên, chưa chọn.

- Có căn cứ ở mức CT hoặc ĐC để **đề xuất thử**, chia ba loại. *Dùng cạnh đồ thị dịch vụ:* gắn thời gian lời gọi lên cạnh, tính cho dịch vụ được gọi. *Dùng quan hệ cha–con trong trace:* thời gian tự xử lý; tiêu chí “yêu cầu bất thường” theo cả cây lời gọi. *Yêu cầu kỹ thuật:* chặn giá trị không hợp lệ trước khi lan điểm.
- **Chưa** có căn cứ để nói đồ thị sẽ giúp, cũng chưa có căn cứ để nói nó không giúp. Hai quan sát phải cân nhắc: ở MicroRank và BARO, phần lớn thực thể đứng trên root không nằm phía trên root ({{ch.both.microrank_full.up}}/{{ch.both.microrank_full.pairs}} và {{ch.both.baro.up}}/{{ch.both.baro.pairs}} cặp nằm phía trên). Hiện tượng “dịch vụ gọi chờ root” có cả ở ca đúng ({{h4.right.wait}}/{{h4.right.n}}). Hai tỷ lệ đầu chỉ nói về **quan hệ gọi** và về đầu ra của các bản cài đã xét; chúng không nói gì về cạnh cùng máy, thông điệp hay dữ liệu.
- Trên RE2-TT, mốc phải vượt ở P7 là baseline tốt nhất của P3 (Q-62), hiện là TORAI B và SimpleRCA.

## 1. K1 — Sáu câu của cổng (MRP §7) và năm đầu ra của P4

1. **Phục vụ câu nào của cô hoặc DT18?** Hai việc trong chuỗi cô yêu cầu: “mở rộng thực nghiệm ra các dataset public khác” (P3) và “chỉ ra vấn đề còn tồn đọng, hạn chế của các phương pháp đã có” (P4). Đây là bước nối sang “tiếp cận phương pháp đồ thị”. Theo DT18 (đoạn nhiệm vụ thứ ba): thực nghiệm trên dữ liệu công khai trước, và “phân tích các trường hợp phương pháp hoạt động hiệu quả hoặc còn hạn chế”.
2. **Dữ liệu có phân xử nổi không?** Một phần.
   - Phân xử được ở mức tính toán: bước nào của từng phương pháp làm đổi thứ hạng (các dòng mức CT ở mục 3).
   - Phân xử yếu: RE2-TT chỉ có năm root; Nezha-OB có nền trace ngắn và rất ít mẫu metric, CIRCA và TORAI B không chạy được.
   - Không phân xử được bằng dữ liệu hiện có: vì sao bộ phát hiện báo trước mốc (không có onset và nền sạch độc lập); vì sao dịch vụ không liên hệ đổi tại mốc (không có ánh xạ dịch vụ–máy); việc “dịch vụ gọi chờ root” ở {{d2.unmeasurable}}/{{d2.n}} ca.
   - Eadro-TT chưa được dùng tới G2 (Q-83).
3. **Baseline đủ mạnh chưa?** Trên RE2-TT: có; theo điểm ước lượng, đứng đầu là SimpleRCA (không dùng quan hệ gọi) và TORAI B (bước nhân quả không quyết định hạng của root). Trên Nezha-OB: chỉ bốn phương pháp chạy được, đều yếu. Ba điểm phải nói kèm: (i) TraceRCA và MicroRank đang dùng là bản trong thư viện RCAEval, khác bài gốc ở những bước quyết định (G2-H01, G2-H03); (ii) nhánh mã tác giả TraceRCA mới là chẩn đoán, chưa là baseline (mục 2.8, mục 8); (iii) trạng thái tái lập từng phương pháp ở mục 2.7, có phương pháp chưa tái lập được số công bố.
4. **Giá trị trung gian có hợp lý không?** Đã soi và thấy năm chỗ bất thường, đều đã lần tới bước gây ra: điểm cực lớn của CIRCA (G2-H12); khoảng một nửa trace bị MicroRank xếp bất thường (G2-H01); bảng log của TORAI B dồn điểm (G2-H14); thứ tự chứa giá trị không hữu hạn của TraceRCA (đã xử lý ở giao thức, WHY-32); underflow của BOCPD (phép E2). Số tổng của bảng baseline được tính lại độc lập từ bản ghi từng lượt: {{bl.v2.problems}} lệch.
5. **Đã tách theo điều kiện và theo ca chưa?** Rồi: bảng theo ô ở mục 2.2 và 2.4, Phụ lục A và B; bảng theo ca nằm trong các file nguồn được dẫn.
6. **Còn lựa chọn nào chưa có câu trả lời “tại sao”?** Các lựa chọn của gói này có ở WHY-51. Các lựa chọn **chưa quyết** nằm ở mục 8: nhánh mã tác giả TraceRCA; có định nghĩa nhãn lan không; cách trình bốn ca ERROR; TORAI nguồn B; dòng độ nhạy MicroRank.

**Năm đầu ra của P4** (MRP mục P4) nằm ở đâu trong gói:

@@k3_p4@@

## 2. K2 — Bảng baseline trên dev

Bảng chính lấy nguyên số của T-024, T-025, T-026 (đã khóa); gói này không chạy lại phương pháp nào để thay bảng. Số máy đọc: `results/T-034/bang-baseline.json`. Phép kiểm V2 tính lại mọi số tổng từ bản ghi từng lượt bằng một bộ chấm viết riêng: {{bl.v2.status:x}}, {{bl.v2.problems}} lệch.

### 2.1 Xếp hạng, chế độ (a), RE2-TT ({{bl.re2.n}} ca, {{bl.re2.cells}} ô)

@@k2_rank:RE2-TT_dev30@@

Khoảng bootstrap lấy mẫu theo ô, mức 95%. Avg@5 là trung bình AC@1 đến AC@5 theo cách của RCAEval. Retrieval@5 là tỷ lệ ca root lọt vào năm hạng đầu; Rerank@1 là tỷ lệ root hạng 1 trong các ca đó (Q-65).

Khoảng của BARO, SimpleRCA, TraceRCA và TORAI B chồng nhau: với {{bl.re2.n}} ca, bảng không phân định được thứ tự giữa bốn phương pháp này.

MicroRank và TraceRCA mỗi phương pháp có {{bl.re2.tracerca.st.ERROR}} ca dừng lỗi, tính trượt. CIRCA: {{h13.huge}} ca có nút điểm cực lớn (G2-H12), báo riêng ở mục 2.3.

### 2.2 RE2-TT theo ô: số ca root hạng 1 (kỳ vọng khi hòa) trên số ca

@@k2_cell:RE2-TT_dev30@@

### 2.3 Nhóm ca theo Q-82: {{bl.re19.n}} ca CIRCA không có nút điểm cực lớn

@@k2_rank:RE2-TT_dev19@@

Nhóm {{bl.re19.n}} ca này được chọn từ đầu ra của CIRCA, không phải mẫu ngẫu nhiên; cùng một tập cho mọi phương pháp (WHY-36). Trên nhóm này CIRCA đạt {{bl.re19.circa_ols_da.h1:.3f}}, so với {{bl.re2.circa_ols_da.h1:.3f}} trên cả {{bl.re2.n}} ca.

### 2.4 Xếp hạng, chế độ (a), Nezha-OB ({{bl.nz.n}} ca, {{bl.nz.cells}} ô)

@@k2_rank:Nezha-OB_main@@

@@k2_cell:Nezha-OB_main@@

Hai dataset khác nhịp metric và độ dài nền (WHY-37); so giữa hai dataset chỉ để mô tả.

### 2.5 Phát hiện, chế độ (b), RE2-TT

@@k2_det@@

**Phải đọc kèm ba điều.**

- Nhãn dùng để chấm là nhãn proxy của giao thức (WHY-35): từ mốc tiêm tới cuối file là “bất thường”. Dataset không xác nhận độc lập đoạn trước mốc là khỏe, lúc lỗi bắt đầu có tác động, hay lúc hết lỗi.
- Vì vậy “báo động trên đoạn bình thường” **không** phải tỷ lệ báo động sai trong vận hành thật, và độ trễ là tính từ **mốc tiêm**, không phải từ lúc sự cố bắt đầu biểu hiện.
- Precision, Recall, F1 tính theo cửa sổ 60 giây.

Theo ô:

@@k2_det_cell@@

**Độ nhạy theo điểm cuối D** (T-033; không chấm lại): số ca BOCPD có ít nhất một điểm đổi trong D giây sau mốc là {{k7.d30}}, {{k7.d60}}, {{k7.d120}}, {{k7.d300}}, {{k7.d600}} trên {{bl.det.bocpd.n}} ca, với D lần lượt `30`, `60`, `120`, `300`, `600`. D không phải thời điểm hết lỗi.

### 2.6 Chế độ (b): xếp hạng tại báo động đầu, và bảng điểm chạy

@@k2_modeb@@

- “Thành công chung” đòi báo động đầu đúng **và** root trong k hạng đầu.
- Ba cột cuối (bảng G của T-029) cho cùng một phương pháp xếp hạng chạy ở ba điểm. Cột giữa chọn báo động nhờ nhãn mốc, nên chỉ là chẩn đoán, không phải cận trên.
- BARO ghép BOCPD: trong {{bl.g.baro_bocpd.far.n}} ca báo động đầu cách xa mốc, Hit@1 tại báo động đầu là {{bl.g.baro_bocpd.far.that:.3f}}, so với {{bl.g.baro_bocpd.far.a:.3f}} khi chạy tại mốc tiêm.

### 2.7 Trạng thái kiểm tái lập

| Phương pháp | Trạng thái | Nguồn |
|---|---|---|
| BARO | Đã tái lập số công bố trên dataset của bài (mốc có lệnh của tác giả). Trên RE2-TT chỉ so tham khảo với số README theo loại lỗi; khác tập ca, cửa sổ, bộ cột | `results/T-006/kiem-dung-dan.md` mục 1 và 3; `results/T-024/cham-a.md`, mục “Đối chiếu mốc công bố BARO RE2-TT” |
| SimpleRCA (M4) | Chưa tái lập số công bố: bài báo trên cả bộ RE2-TT, phần test đang khóa. Bản cài theo mô tả của bài, có chỗ bài để ngỏ | `results/T-017/kiem-dung-dan.md`, mục “Tái lập và số công bố”; WHY-17 |
| MicroRank | Bản thư viện nguyên trạng khớp số của bài TORAI ở cấu hình tham chiếu trên dataset khác, nhưng thứ hạng gần như cố định theo lưu lượng. Bản dùng ở P3 (sửa đầu vào) chưa có số công bố | `results/T-007/kiem-dung-dan.md` mục 2 và 10 |
| TraceRCA | Chỉ so tham khảo: kết quả bản thư viện phụ thuộc thứ tự dòng span. Bản dùng ở P3 (lọc giá trị hữu hạn) chưa có số công bố | `results/T-007/kiem-dung-dan.md` mục 3 và 10; WHY-32 |
| CIRCA (đồ thị kiến trúc) | Chưa có số công bố cho cấu hình này. Biến thể CIRCA-PC lệch ở mức ô so với bài, chưa tìm đủ nguyên nhân | `results/T-006/kiem-dung-dan.md` mục 1 và 5; `results/T-014/` |
| TORAI | Bản gốc khớp số công bố trên dataset của bài. Bản dùng ở P3 (sửa hai chỗ, nguồn B) chưa có số công bố | `results/T-006/kiem-dung-dan.md` mục 1 và 7; WHY-19, WHY-29 |
| N-Sigma (phát hiện) | Khớp một phần số của bài BARO: một dataset khớp, một dataset lệch, chưa tìm ra nguyên nhân | `results/T-006/kiem-dung-dan.md` mục 1 và 8 |
| BOCPD | Mã chạy đúng như tác giả trên dataset của bài; cách tái lập của tác giả đưa mốc tiêm vào đầu vào. Ở chế độ tự phát hiện trên RE2-TT chưa có số công bố | `results/T-007/kiem-dung-dan.md` mục 4 và 10 |

Không dòng nào ở trên được gọi là “khớp” khi hồ sơ ghi lệch hoặc không có mốc.

### 2.8 Nhánh chẩn đoán, báo riêng — chưa là baseline

**TraceRCA theo mã tác giả, nhánh chỉ dùng độ trễ.** Đầu vào của hai dataset chỉ hỗ trợ nhánh này: thiếu trạng thái HTTP gắn với từng lời gọi, thiếu bộ giải mã dữ liệu thô và thiếu nền nhiều ngày. Đây không phải tái lập bài hay cấu hình mặc định của bài. Ca không có bằng chứng và ca root vắng tính trượt trong mẫu số. Dịch vụ không có tập một dịch vụ được giữ nhận điểm mặc định.

@@k2_author@@

Để đặt cạnh, trên cùng mẫu số: BARO ở Nezha-OB đúng {{bl.nz.baro.h1n:.3g}} ca kỳ vọng; TORAI B ở RE2-TT đúng {{bl.re2.torai_B.h1n:.3g}} ca kỳ vọng. Các số của nhánh này lấy từ đầu ra đã lưu của gói bổ sung T-032; không chọn ngưỡng theo điểm dev. Đây là dev đã nhìn, chưa có khoảng tin cậy.

**MicroRank với bộ chia theo công thức của bài gốc.** Chỉ thay bước chia trace; span đầu của yêu cầu do ta quy ước. Không phải MicroRank gốc.

@@k2_mrsplit@@

### 2.9 Đọc bảng theo điều kiện

Chỉ nêu điều thấy ở từng ô; một ô ba ca không phải mẫu hình.

- **Theo loại lỗi ở RE2-TT.** Lỗi đĩa ({{dx.re2.baro.f.disk.n}} ca): BARO {{dx.re2.baro.f.disk.h1:.3g}}, SimpleRCA {{dx.re2.simplerca.f.disk.h1:.3g}}, CIRCA {{dx.re2.circa_ols_da.f.disk.h1:.3g}}, TORAI B {{dx.re2.torai_B.f.disk.h1:.3g}}, TraceRCA {{dx.re2.tracerca.f.disk.h1:.3g}}. Lỗi mất gói: không phương pháp nào vượt {{dx.re2.torai_B.f.loss.h1:.3g}}/{{dx.re2.torai_B.f.loss.n}}. Lỗi trễ mạng: BARO {{dx.re2.baro.f.delay.h1:.3g}}, SimpleRCA {{dx.re2.simplerca.f.delay.h1:.3g}}, TraceRCA {{dx.re2.tracerca.f.delay.h1:.3g}}, TORAI B {{dx.re2.torai_B.f.delay.h1:.3g}} trên {{dx.re2.baro.f.delay.n}} ca.
- **Theo root ở RE2-TT.** Với root `ts-auth-service` (không được dịch vụ nào gọi trong trace): BARO {{dx.re2.baro.r.auth.h1:.3g}}, SimpleRCA {{dx.re2.simplerca.r.auth.h1:.3g}}, TraceRCA {{dx.re2.tracerca.r.auth.h1:.3g}}, TORAI B {{dx.re2.torai_B.r.auth.h1:.3g}} trên {{dx.re2.baro.r.auth.n}} ca.
- **Nezha-OB.** Lỗi tranh chấp CPU: BARO và SimpleRCA đúng {{dx.nz.baro.f.cpu_contention.h1:.3g}} và {{dx.nz.simplerca.f.cpu_contention.h1:.3g}} trên {{dx.nz.baro.f.cpu_contention.n}} ca; TraceRCA {{dx.nz.tracerca.f.cpu_contention.h1:.3g}}. Lỗi return và trễ mạng: gần như không phương pháp nào đúng (xem câu 1 ở mục 0).
- **Phát hiện.** Không ô nào có quá một ca BOCPD báo động đầu đúng; N-Sigma không có ca nào.

## 3. K3 — Bản đồ hạn chế hợp nhất

Bản đồ gộp bốn nguồn: mã HP của T-029 (phát hiện), mã M của T-028 (cờ cơ chế xếp hạng), mã H và D của T-032 (nguyên nhân xếp hạng và giới hạn dữ liệu), cùng các câu hỏi KT của T-032 và K của T-033 trong sổ đối chiếu của gói bổ sung. Với H6, H8, CIRCA và KT11, bản đồ dùng **trạng thái đã đính chính ngày 13/10**, không dùng câu cũ.

- Bản máy đọc: `results/T-034/ban-do-g2.json` (mỗi dòng có mã gốc, mức, số kèm con trỏ nguồn, bảng theo ô).
- Phép kiểm V3: {{v3.covered}}/{{v3.required}} mã gốc có mặt trong ít nhất một dòng hoặc trong danh sách “không đưa vào”; {{v3.ledger}} dòng của sổ đối chiếu đều có chỗ. Kết quả: {{v3.status:x}}.
- Các dòng **chồng nhau** trên cùng một ca. Không cộng các dòng thành tỷ lệ nguyên nhân.
- Loại nguồn hạn chế: **D** dữ liệu hoặc thiếu đầu vào; **G** giao thức đánh giá; **A** bản cài, adapter hoặc đầu vào do ta dựng; **M** giả định hoặc cách tính của phương pháp.

### 3.1 Bảng tóm tắt

@@k3_summary@@

Không đưa vào bản đồ:

@@k3_excluded@@

### 3.2 Từng dòng

@@k3_rows@@

## 4. K4 — “Nhầm triệu chứng lan với nguyên nhân” có đáng kể không (Q-86)

MRP đặt câu này ở P4: nếu cơ chế “độ trễ lan lên dịch vụ gọi, nên dịch vụ gọi bị xếp trên root” chiếm phần đáng kể các ca sai thì định nghĩa nhãn “lan” cho từng ca; nếu không thì không tách.

### 4.1 Điều đã thấy

**Hỗ trợ.**

- *Hiện tượng chờ có thật và quan sát được ở phần lớn ca đo được* (ĐC). Ngưỡng “lời gọi chậm” của một cạnh lấy từ dữ liệu bình thường: phân vị 95 của thời lượng phía gọi trước mốc. Ở các ca có cạnh gọi tới root, có ít nhất một cạnh với từ một nửa số lời gọi sau mốc là chậm ở {{cs.re2.ge05}}/{{cs.re2.edge}} ca RE2-TT và {{cs.nz.ge05}}/{{cs.nz.edge}} ca Nezha-OB. Hạ mức xuống một phần năm: {{cs.re2.ge02}} và {{cs.nz.ge02}} ca. Trước mốc tỷ lệ này khoảng {{cs.re2.before:pct0}} theo cách đặt ngưỡng.
- *Với TraceRCA bản thư viện, chuỗi “chờ → cờ → điểm” được xác lập* (CT ở RE2-TT, ĐC ở hai dataset; G2-H03): trong các cặp dịch vụ phía trên đứng trên root, span mang cờ chủ yếu là span bao lời gọi chậm tới root ở {{h4.re2.wait}}/{{h4.re2.n}} cặp RE2-TT và {{h4.nz.wait}}/{{h4.nz.n}} cặp Nezha-OB.
- *Với lỗi trễ mạng ở Nezha-OB* (ĐC; G2-H06): dấu hiệu nằm ở span phía gọi của lời gọi tới root ở {{h7.nd.in}}/{{h7.nd.n}} ca, ở span của chính root chỉ {{h7.nd.own}} ca.

**Bất lợi cho cách đọc “phần lớn ca sai là do nhầm triệu chứng”.**

- Hiện tượng chờ có cả ở ca **đúng**: {{h4.right.wait}}/{{h4.right.n}} dịch vụ phía trên ở các ca TraceRCA xếp root hạng 1. Tự nó không phân biệt ca sai.
- Bỏ phần chờ khỏi cờ của TraceRCA (phép T-D) chỉ đổi ít: số ca có dịch vụ gọi trên root {{h4.td.re2.before}} → {{h4.td.re2.after}} ở RE2-TT và {{h4.td.nz.before}} → {{h4.td.nz.after}} ở Nezha-OB; số ca hạng 1 {{h4.td.hit1.native}} → {{h4.td.hit1.td}} trên {{h4.td.n}} ca.
- Ở MicroRank và BARO, phần lớn thực thể đứng trên root **không** nằm phía trên root: chỉ {{ch.both.microrank_full.up}}/{{ch.both.microrank_full.pairs}} và {{ch.both.baro.up}}/{{ch.both.baro.pairs}} cặp. Với kênh metric của BARO ở RE2-TT, chỉ {{h12.up.latency}}/{{h12.pairs}} cặp là dịch vụ phía trên thắng bằng cột độ trễ.
- Ở CIRCA, phần lớn ca có cờ M5 thuộc nhóm có nút điểm cực lớn (G2-H12), nhưng không phải mọi ca. Trong nhóm đó, nút cực lớn là một dịch vụ gọi root gián tiếp và đã đứng trên root trước bước DA. Đóng góp của việc chờ ở các ca này: chưa phân xử; phép bỏ cạnh đổi cả hồi quy nên không loại riêng được chờ.
- Cờ “có dịch vụ phía trên đứng trước root” (M5 của T-028) không đồng nghĩa “sai vì dịch vụ gọi”. Số đơn vị có cờ trên số đơn vị sai hạng 1: TraceRCA {{m5.re2.tracerca.m5}}/{{m5.re2.tracerca.sai}} và {{m5.nz.tracerca.m5}}/{{m5.nz.tracerca.sai}}; MicroRank {{m5.re2.microrank_full.m5}}/{{m5.re2.microrank_full.sai}} và {{m5.nz.microrank_full.m5}}/{{m5.nz.microrank_full.sai}}; SimpleRCA {{m5.re2.simplerca.m5}}/{{m5.re2.simplerca.sai}} và {{m5.nz.simplerca.m5}}/{{m5.nz.simplerca.sai}}; BARO {{m5.re2.baro.m5}}/{{m5.re2.baro.sai}} và {{m5.nz.baro.m5}}/{{m5.nz.baro.sai}}; CIRCA {{m5.re2.circa_ols_da.m5}}/{{m5.re2.circa_ols_da.sai}} (RE2-TT trước, Nezha-OB sau). Các cờ này chồng nhau và không phải tỷ lệ nguyên nhân.

**Khả năng đo.** Việc “dịch vụ gọi chờ root” đo được có điều kiện ở {{d.nz.ok}} ca Nezha-OB, đo được một phần ở {{d.re2.part}} ca RE2-TT (thiếu thông tin công cụ ghi span), và không đo được ở {{d2.unmeasurable}} ca ({{d2.nocaller}} ca root không được dịch vụ nào gọi, {{d2.fewcalls}} ca cạnh quá thưa). Đây là khả năng quan sát trên {{d2.n}} ca; không phải nhãn lan, tỷ lệ lan, hay tỷ lệ nguyên nhân thất bại.

### 4.2 Trả lời

- **Đã xác lập** (ĐC): độ trễ của root hiện lên ở span phía gọi trong phần lớn ca đo được. Lan, hiểu là hiện tượng quan sát được, là phổ biến.
- **Đã xác lập** (CT): với TraceRCA bản thư viện, phần chờ đó được chấm thành bất thường của dịch vụ gọi.
- **Chưa phân xử:** lan có là nguyên nhân của “phần đáng kể các ca sai” không. Chưa có căn cứ nói lan gây ra phần lớn ca sai; cũng chưa có căn cứ nói nó chỉ là thiểu số. Điều đã xác lập: với TraceRCA bản thư viện, bỏ phần chờ khỏi cờ làm số ca có dịch vụ gọi trên root giảm {{h4.td.re2.before}} → {{h4.td.re2.after}} (RE2-TT) và {{h4.td.nz.before}} → {{h4.td.nz.after}} (Nezha-OB); đó là số ca có dịch vụ gọi trên root, không phải số ca root hạng 1. Với trễ mạng ở Nezha-OB mới xác lập nơi có dấu hiệu; vì sao từng phương pháp xếp sai chưa phân xử (G2-H06). Ở BARO và CIRCA đã tìm thấy một cơ chế chấm khác (G2-H09, G2-H12), nhưng điều đó **không loại** vai trò của lan: đổi thang của BARO chỉ đưa root lên hạng 1 ở {{h10.re2.fixed}}/{{h10.re2.wrong}} ca sai RE2-TT và {{h10.nz.fixed}}/{{h10.nz.wrong}} ca sai Nezha-OB, và hai cơ chế có thể cùng góp phần. Ở MicroRank, phần lớn thực thể đứng trên root không nằm phía trên root, nhưng đường gián tiếp “chờ → cờ → trace bị xếp bất thường → điểm” **chưa được phân xử đầy đủ** (T-032 mục 5.2). Chưa có một định nghĩa “đáng kể” được chọn để biến các điều trên thành một tỷ lệ, và hai phép E1, E2 không đo lan.

### 4.3 Nhãn “lan”: nháp có điều kiện, chưa đề xuất khóa

Các thành phần sau **đã có số đo** trên dev, đủ để viết một nháp:

- *Đại lượng:* với mỗi ca, tỷ lệ lời gọi chậm sau mốc trên từng cạnh gọi tới root.
- *Ngưỡng từ dữ liệu bình thường:* phân vị 95 của thời lượng phía gọi trước mốc, theo từng cạnh.
- *Nhãn nháp:* ca “có lan” nếu ít nhất một cạnh tới root có tỷ lệ lời gọi chậm sau mốc từ một mức θ trở lên.
- *Độ nhạy đã đo:* hai mức θ (một nửa và một phần năm) cho {{cs.re2.ge05}} và {{cs.re2.ge02}} ca RE2-TT, {{cs.nz.ge05}} và {{cs.nz.ge02}} ca Nezha-OB.
- *Không vòng lặp:* định nghĩa không dùng thứ hạng của bất kỳ phương pháp nào.
- *Không áp dụng được:* {{d2.unmeasurable}} ca không có cạnh tới root đủ lời gọi. Các ca này phải là nhóm thứ ba, không gộp vào “không lan”.

**Còn thiếu trước khi có thể khóa ở G3:** (i) độ nhạy ở nhiều mức θ hơn và theo phân vị nền khác; (ii) cách xử lý nền rất ngắn của Nezha-OB; (iii) ở RE2-TT, điều kiện về công cụ ghi span (tác giả không công bố); (iv) quyết định có tính lan qua nhiều tầng gọi không. Các phép này chỉ đọc bảng lời gọi đã lưu, chưa được giao, chi phí chưa đo.

**Quyết định phụ thuộc** (mục 8): nếu Minh muốn P7 báo riêng nhóm “lan” và “không lan”, cần một task nhỏ hoàn thiện nháp trên và khóa ở G3. Nếu không, P7 không tách theo nhãn này; gói G2 không tự khóa nhãn.

## 5. K5 — Căn cứ và ứng viên cho P5/P6

Đây là **ứng viên để thử**, không phải lựa chọn, và không xếp theo kỳ vọng thắng. Thành phần cụ thể chốt ở spec P6, sau khi so phương án và kiểm trên dev. Mức căn cứ theo bảng ở MRP §3: UV-1 đến UV-9 mới đạt bậc “đủ để đề xuất thử”. Hai phần **không** nằm trong danh sách ứng viên: cách gộp điểm từ nút con lên nút cha là câu hỏi thiết kế, chưa có phương án cụ thể và chưa có dự đoán (mục 6.1); các thành phần DT18 yêu cầu (mục con cuối của mục này) không phải ứng viên rút từ P4 và chưa có dự đoán kiểm được trên dev vì dữ liệu thiếu đầu vào. Chúng vẫn phải được thiết kế và kiểm khi có đầu vào phù hợp (FlashTicket, P10); đây không phải miễn kiểm. Để **chọn** còn thiếu: so phương án, kiểm đầu vào, trung gian và hành vi của chính bản cài mới trên dev. Để **khẳng định hiệu quả** còn thiếu: đánh giá sau khóa thiết kế, với nhánh cùng bằng chứng không dùng quan hệ và đồ thị ngẫu nhiên giữ bậc.

### UV-1 — Gắn thời gian lời gọi lên cạnh, tính cho dịch vụ được gọi

- **Mục đích:** sửa hạn chế G2-H03 và G2-H06.
- **Điều kiện ở MRP P6** (chỉ giữ cơ chế tách tự sinh/kế thừa nếu P4 xác nhận hạn chế): hạn chế được xác nhận ở G2-H03 cho TraceRCA **bản thư viện** (bài gốc có bước xử lý, bản thư viện bỏ) và ở phép đo vị trí của G2-H06. Chưa xác nhận nó gây bao nhiêu ca sai (mục 4).
- **Căn cứ và mức:** ĐC. Root đứng đầu theo span phía gọi của lời gọi đi vào ở {{h7.re2.inu}}/{{h7.re2.inn}} ca RE2-TT và {{h7.nz.inu}}/{{h7.nz.inn}} ca Nezha-OB; theo thời lượng span của chính dịch vụ chỉ {{h7.re2.ownd}}/{{h7.re2.n}} ca RE2-TT. Phép thử gán tín hiệu theo cạnh của gói bổ sung T-032 (KT5) cho thấy đổi cạnh thì đổi điểm (CT ở mức tính toán).
- **Giải thích khác còn lại:** “root đứng đầu theo một vị trí” không phải Hit@1 của một phương pháp hoàn chỉnh; định nghĩa vị trí đặt sau khi xem dev; phần chậm ngoài span của root không tách được.
- **Cơ chế dự kiến:** lời gọi tới root chậm làm span phía gọi dài ra; gán phần đó cho dịch vụ **được gọi** thay vì dịch vụ sở hữu span.
- **Nút, cạnh, ánh xạ, phép tính dùng cạnh:** nút là dịch vụ; cạnh có hướng là lời gọi đồng bộ (span phía gọi → span phía được gọi); trace được ánh xạ lên cạnh; với mỗi nút, phép tính gộp tỷ lệ lời gọi **đi vào** có thời lượng phía gọi vượt nền của chính cạnh đó.
- **Dự đoán trên dev, khai trước:** (i) xếp root hạng 1 ở nhiều ca hơn nhánh dùng cùng tín hiệu nhưng gán theo dịch vụ sở hữu span; (ii) ở mốc giả không có lỗi, không đưa một dịch vụ cố định lên đầu quá mức nền; (iii) với đồ thị ngẫu nhiên giữ bậc, lợi thế ở (i) mất. **Bác bỏ** nếu (i) không xảy ra ở cả hai dataset, hoặc (iii) không mất.
- **Điều kiện thất bại đã biết:** {{d2.nocaller}} ca root không được gọi; {{d2.fewcalls}} ca cạnh thưa; lỗi không làm chậm lời gọi (return).
- **Tầng:** ánh xạ và chấm điểm (tầng 1–2).

### UV-2 — Thời gian tự xử lý theo quan hệ cha–con của span

- **Mục đích:** sửa hạn chế G2-H03.
- **Điều kiện ở MRP P6** (chỉ giữ cơ chế tách tự sinh/kế thừa nếu P4 xác nhận hạn chế): hạn chế được xác nhận ở G2-H03 cho TraceRCA **bản thư viện** (bài gốc có bước xử lý, bản thư viện bỏ) và ở phép đo vị trí của G2-H06. Chưa xác nhận nó gây bao nhiêu ca sai (mục 4).
- **Căn cứ và mức:** ĐC. Phần span không do span con phủ tách được root ở {{h7.re2.ownu}}/{{h7.re2.n}} ca RE2-TT, so với {{h7.re2.ownd}}/{{h7.re2.n}} theo thời lượng cả span; ở Nezha-OB chỉ {{h7.nz.ownu}}/{{h7.nz.n}} ca. CT: đổi cờ sang phần chưa phủ làm số ca có dịch vụ gọi trên root giảm {{h4.td.re2.before}} → {{h4.td.re2.after}} (RE2-TT).
- **Giải thích khác còn lại:** ở Nezha-OB một phần span có span con chạy chồng nhau, phép trừ đơn giản sai; ở RE2-TT phải giả định công cụ ghi span.
- **Cơ chế dự kiến:** trừ khỏi thời lượng span phần đã do span con phủ, có xử lý chồng lấn và song song.
- **Nút, cạnh, ánh xạ, phép tính dùng cạnh:** quan hệ dùng là cha–con **trong trace** (không phải đồ thị dịch vụ); span ánh xạ lên nút dịch vụ; phép tính dùng quan hệ: hợp các khoảng thời gian của span con.
- **Dự đoán trên dev, khai trước:** số ca root đứng đầu theo đại lượng này cao hơn theo thời lượng cả span ở cả hai dataset, và không cao bất thường ở mốc giả. **Bác bỏ** nếu ở Nezha-OB sau khi xử lý chồng lấn vẫn không hơn thời lượng cả span.
- **Điều kiện thất bại đã biết:** lời gọi bất đồng bộ; thiếu span con; lỗi tài nguyên không làm tăng độ trễ; lỗi trả về nhanh.
- **Tầng:** ánh xạ (tầng 1).

### UV-3 — Tiêu chí “yêu cầu bất thường” theo cả cây lời gọi

- **Mục đích:** sửa hạn chế G2-H01.
- **Căn cứ và mức:** CT. Thay riêng bước chia trace của MicroRank bản thư viện bằng công thức của bài gốc: hạng 1 từ {{h1.mo15.native}} lên {{h1.mo15.hit1}}–{{h1.mo1p50.hit1}} trên {{h1.mo15.evaluable}} ca xét được. Ở mốc giả không lỗi, luật theo từng span vẫn xếp {{h1.fake.median:pct0}} trace là bất thường.
- **Giải thích khác còn lại:** bộ chia thay thế dùng quy ước span đầu của ta; sau khi thay vẫn còn hơn một nửa số ca chưa hạng 1.
- **Cơ chế dự kiến:** quyết định “bất thường” ở mức cả yêu cầu, so với tổng mức nền của các thao tác trong cây.
- **Nút, cạnh, ánh xạ, phép tính dùng cạnh:** dùng cây lời gọi của từng yêu cầu để gom thao tác; chưa dùng đồ thị dịch vụ; có dùng quan hệ cha–con trong trace, nên theo MRP P7 vẫn tính là dùng cấu trúc khi làm đối chứng.
- **Dự đoán trên dev, khai trước:** tỷ lệ trace bị xếp bất thường ở mốc giả thấp hơn luật theo từng span, và tỷ lệ trace bất thường có span của root cao hơn. **Bác bỏ** nếu một trong hai không xảy ra.
- **Điều kiện thất bại đã biết:** thao tác chỉ xuất hiện sau mốc (không có nền; G2-H16); cây lời gọi không đầy đủ vì mất span cha (mã D5 ở G2-H19: {{d5.orphan}}/{{d5.n}} trace của một ca).
- **Tầng:** phát hiện ở mức yêu cầu (tầng 2).

### UV-4 — Quy tắc gộp điểm qua tập dịch vụ (kiểu TraceRCA)

- **Mục đích:** sửa hạn chế G2-H05, nếu P6 dùng cách chấm theo tập.
- **Căn cứ và mức:** CT, trong {{e1.pairs}} cặp của phép E1. Ở cờ ba lần độ lệch chuẩn, chỉ chấm tập một dịch vụ làm {{e1.top3.nz.flip}}/{{e1.top3.nz.phen}} cặp Nezha-OB đổi sang root trên. Ở cờ một lần (mặc định của bài): {{e1.top.nz.flip}}/{{e1.top.nz.phen}} cặp đảo chiều (ca đã nhìn trước); ở {{e1.top.nz.unch_both}} cặp khác điểm của dịch vụ gọi giảm nhưng chưa đảo chiều.
- **Giải thích khác còn lại:** tác dụng phụ thuộc mức cờ; ở RE2-TT bước quyết định là bước chọn tập, không phải quy tắc gộp; mới thử trên ít cặp, các cặp chung ca không độc lập.
- **Cơ chế dự kiến:** không cho một dịch vụ xuất hiện rộng (như frontend) thừa hưởng điểm của tập chứa root.
- **Nút, cạnh, ánh xạ, phép tính dùng cạnh:** không dùng cạnh; dùng tập dịch vụ cùng xuất hiện trong trace bất thường.
- **Dự đoán trên dev, khai trước:** tác dụng lên thứ hạng rõ ở mức cờ cao, yếu ở mức cờ mặc định. **Bác bỏ** nếu trên toàn bộ ca dev (không chỉ {{e1.pairs}} cặp) đổi quy tắc không đổi số ca root hạng 1.
- **Tầng:** xếp hạng (tầng 4).

### UV-5 — Giữ hướng của cạnh khi so lời gọi đi vào với đi ra

- **Mục đích:** ứng viên để so sánh; **không** còn là điều kiện bắt buộc.
- **Căn cứ và mức:** MT. Suy rộng cũ “trị tuyệt đối không mang hướng nên phải giữ dấu” đã rút (đính chính ngày 13/10, WHY-47). Mã tác giả TraceRCA dùng trị tuyệt đối mà vẫn đưa root lên trên dịch vụ gọi ở {{h6.author.nz.t1.above}}/{{h6.author.nz.t1.pairs}} cặp Nezha-OB.
- **Giải thích khác còn lại:** toàn bộ phép chấm (độ tương đồng nhân hiệu số) có thể tách root mà không cần dấu.
- **Tín hiệu; phép dùng quan hệ:** thời lượng lời gọi theo cạnh có hướng; so hiệu số giữa lời gọi đi vào và đi ra của một nút, có dấu hoặc trị tuyệt đối.
- **Dự đoán trên dev, khai trước:** nếu thử, bản giữ dấu phải hơn bản trị tuyệt đối trên cùng đầu vào. **Bác bỏ** nếu không hơn.
- **Tầng:** chấm điểm (tầng 2).

### UV-6 — Dùng tín hiệu giảm và log tại root cho lỗi trả về sớm

- **Mục đích:** sửa hạn chế G2-H07.
- **Căn cứ và mức:** LĐ. Ở {{h8.n}} ca return, log lỗi tại root tăng sau mốc ở cả {{h8.logvote}} ca và tỷ lệ thành công ở frontend giảm; các phép chấm hiện có bỏ qua tín hiệu giảm hoặc chỉ cho log một phiếu.
- **Giải thích khác còn lại:** số dòng log không phải số yêu cầu lỗi; hai ca có phản ứng metric ở frontend chứ không ở chính root; chỉ bốn ca.
- **Cơ chế dự kiến:** chấm cả chiều giảm của tỷ lệ thành công; dùng mật độ log lỗi theo dịch vụ thay cho một phiếu có/không.
- **Nút, cạnh, ánh xạ, phép tính dùng cạnh:** log ánh xạ lên nút theo dịch vụ và thời gian (qua trace_id nếu có); chưa có phép tính dùng cạnh.
- **Dự đoán trên dev, khai trước:** root lên hạng ở các ca return mà không làm tụt các ca đang đúng. **Bác bỏ** nếu số ca đang đúng bị hỏng nhiều hơn số ca return được sửa.
- **Tầng:** ánh xạ và chấm điểm (tầng 1–2).

### UV-7 — Xử lý giá trị không hợp lệ trước khi lan điểm trên đồ thị

- **Mục đích:** nhu cầu kỹ thuật, rút từ G2-H12.
- **Căn cứ và mức:** CT cho câu “một giá trị không hợp lệ đi qua cấu trúc làm hỏng thứ hạng”: ở {{h13.huge}}/{{h13.n}} ca của CIRCA có nút điểm cực lớn; trong nhóm đó số ca đúng là {{h13.da}} (có DA), {{h13.rht}} (có cạnh, không DA), {{h13.k2}} (bỏ mọi cạnh). **Chưa** có căn cứ cho một cách gộp điểm cụ thể: phép bỏ cạnh đổi cả hồi quy lẫn bước cộng điểm, không cô lập bước cộng; và bước DA trong mã chỉ cộng khi điểm của nút vượt ngưỡng.
- **Nội dung:** yêu cầu kỹ thuật: kiểm và xử lý giá trị không hợp lệ ở một nút trước khi lan. Cách gộp điểm từ nút con lên nút cha là câu hỏi thiết kế, không thuộc ứng viên này; xem mục 6.1.
- **Dự đoán trên dev, khai trước:** không còn ca nào mà một nút điểm cực lớn quyết định thứ hạng. **Bác bỏ** nếu vẫn còn.
- **Tầng:** chấm điểm và xếp hạng (tầng 2, 4).

### UV-8 — Hồi quy có điều kiện theo nút cha (kiểu CIRCA)

- **Mục đích:** ứng viên có sẵn ở MRP P6; ghi lại để không bỏ sót.
- **Căn cứ và mức:** CT, **bất lợi** trên dev: G2-H12 và G2-H13. {{h15.raise}}/{{h15.reg}} nút có hồi quy làm tăng điểm so với bản không cạnh; kết quả nhạy với cửa sổ học.
- **Giải thích khác còn lại:** chưa tách được thành phần mẫu, độ gần đoạn chấm và thang phần dư.
- **Tín hiệu; phép dùng quan hệ:** metric theo nút; hồi quy giá trị của nút theo các nút cha trong đồ thị kiến trúc, chấm phần dư.
- **Dự đoán trên dev, khai trước:** nếu thử lại, cần một cách xử lý giá trị không hợp lệ và một cách chuẩn phần dư; bản có cạnh phải hơn bản bỏ cạnh trên nhóm ca không có nút cực lớn. **Bác bỏ** nếu không hơn (hiện, với bản không DA: {{h13.clean.native}} so với {{h13.clean.k2}} trên {{h13.clean.n}} ca).
- **Tầng:** chấm điểm (tầng 2).

### UV-9 — Phát hiện: tiền xử lý chỉ dùng quá khứ và số học ổn định

- **Mục đích:** sửa hạn chế G2-H20; nhu cầu kỹ thuật từ phép E2.
- **Căn cứ và mức:** CT. Cắt dữ liệu sau mốc rồi tiền xử lý lại làm báo động đầu sớm hơn ở {{hp.i1.earlier}}/{{hp.i1.n}} ca. Tính trong miền log làm đổi điểm đổi ở {{e2.chains_differ}}/{{e2.chains}} chuỗi đã kiểm.
- **Giải thích khác còn lại:** bỏ nhìn trước không cho thấy sẽ giảm báo động trước mốc; nguyên nhân của các báo động đó chưa phân xử (G2-H21).
- **Nội dung:** bộ phát hiện ở P6 chỉ được dùng dữ liệu tới thời điểm đang xét; phép tính xác suất làm trong miền log.
- **Dự đoán trên dev, khai trước:** với tiền xử lý chỉ dùng quá khứ, vị trí báo động đầu không đổi khi thêm dữ liệu tương lai. **Bác bỏ** nếu còn đổi. Đây là kiểm tính đúng của bản cài (không nhìn trước), không phải bằng chứng phát hiện tốt hơn.
- **Tầng:** phát hiện (tầng 2).

### Thành phần DT18 yêu cầu (không phải ứng viên rút từ P4)

- **Mục đích:** đáp ứng DT18 và bước 1–2 của cô: cạnh trao đổi thông điệp và phụ thuộc dữ liệu; vùng nghi ngờ (đồ thị con bất thường); xếp hạng trên đồ thị.
- **Căn cứ:** yêu cầu của đề tài (đoạn nhiệm vụ thứ hai của DT18), **không** phải một hạn chế đã thấy ở P4. Đã khảo sát ở P2: trace RE2-TT không có loại span hay thuộc tính đủ dựng cạnh có kiểu (`results/T-002/the-rcaeval.md`); Nezha-OB chưa đủ bằng chứng cho cạnh thông điệp và phụ thuộc dữ liệu (`results/T-008/the-dataset.md`). Điều này không nói các quan hệ ấy không tồn tại. Hai loại cạnh này chỉ dựng được từ nguồn tĩnh hoặc trên FlashTicket; các thành phần này không có dự đoán kiểm được trên dev. Không có nhãn vùng ảnh hưởng.
- **Hệ quả:** các thành phần này ghi đúng lý do là “đáp ứng DT18”; không dựng một hạn chế để hợp thức hóa. Bằng chứng về lợi ích chỉ có thể đến từ P7 và P10.
- **Tầng:** mô hình đồ thị (P5), tầng 3 và 4.

**Hai căn cứ kỹ thuật đã có về việc “cạnh có tham gia phép tính”:** phép dò cạnh của gói bổ sung T-032 (KT5) và phép dò đồ thị của T-033 (K6) cho thấy đổi cạnh thì đổi điểm trên cùng tín hiệu. Cả hai là kiểm khả thi của phép tính, không phải bằng chứng lợi ích.

## 6. K6 — Câu còn mở và nơi phân xử

### 6.1 Còn kiểm được trên dev hiện có

| Câu | Phép phân xử (giữ gì, đổi gì) | Đầu vào | Chi phí | Quyết định phụ thuộc |
|---|---|---|---|---|
| Ở cờ một lần độ lệch chuẩn, bước nào đưa dịch vụ gọi lên trên root trong bản TraceRCA theo lời văn? (sau E1) | Giữ mọi thứ như E1, chỉ đổi **bước chọn tập** (luôn giữ tập một dịch vụ đã khai phá) | Trung gian của lượt `e1-001` | Chưa đo; E1 mất {{e1.wall:.0f}} giây máy | Có đưa cách chấm theo tập vào P6 không (UV-4) |
| Cờ ở lời gọi đi ra của frontend đến từ đâu? (sau E1) | Đối chiếu cờ theo từng lời gọi giữa bản theo lời văn và nhánh mã tác giả, trên {{e1.front.pairs}} cặp | Bảng lời gọi đã phát lại trên EC2 của T-032 | Chưa đo | Như trên; và cách dùng số TraceRCA ở bảng baseline |
| Underflow có đổi MAP hoặc điểm đổi ở các ca dev còn lại không? (sau E2) | Chạy bản miền log đã kiểm trên đầu vào full của các ca còn lại | NPZ nguồn của T-033 trên EC2 | Mỗi chuỗi full khoảng {{e2.3ae.ff.total_s:.0f}} giây máy; cả lượt vượt một giờ nên phải xin duyệt | Có ghi chú số BOCPD của T-025 không; yêu cầu số học cho P6 (UV-9) |
| Hoàn thiện nháp nhãn lan (mục 4.3) | Đọc bảng lời gọi đã lưu; quét mức θ và phân vị nền | `results/T-032/runs/call-slow-001/` | Chưa đo | Có khóa nhãn ở G3 không |
| Phần ca sai còn lại của MicroRank sau khi thay bộ chia và cách đếm | Đã đọc ở T-032; còn hai ca chưa rõ bước gây sai | Bảng nối của T-032 | Đã làm phần đọc; phần còn lại chưa có phép | Cách xếp hạng kiểu MicroRank ở P6 |
| Đáp ứng thời lượng theo từng thao tác ở lỗi return | Bảng theo thao tác, cửa sổ đối xứng trước và sau mốc | Span đã lưu | Chưa đo | UV-6 |
| Cách gộp điểm từ nút con lên nút cha nên là gì? (câu hỏi thiết kế, chưa là ứng viên) | So các cách gộp trên cùng điểm đầu vào; chưa có phương án cụ thể. Phép bỏ cạnh của T-032 đổi cả hồi quy lẫn bước cộng, không dùng để chọn | Bản ghi CIRCA đã lưu của T-032 (điểm trước và sau bước DA) | Chưa đo | Spec P6: có dùng bước cộng điểm lên nút cha không, và theo cách nào |

Hai phép E1 và E2 đã được giao và **đã chạy xong** trong task này (`results/T-034/hai-phep-kiem.md`). Ba dòng đầu là phần còn lại sau chúng. Dòng cuối là câu hỏi thiết kế phải giải quyết trên dev trước khi khóa thiết kế. Cả bảy dòng đều chưa được giao.

### 6.2 Thiếu quan sát hoặc nhãn độc lập (không phục hồi được từ dữ liệu hiện có)

| Thông tin thiếu | Vì sao dữ liệu hiện có không cung cấp | Câu bị chặn | Đối chiếu chuẩn quan sát B16 của FlashTicket | Ai cung cấp |
|---|---|---|---|---|
| Lúc lỗi bắt đầu có tác động, lúc hết lỗi, đoạn nền được xác nhận khỏe | RE2-TT chỉ ghi mốc tiêm | Vì sao báo trước mốc (G2-H21, G2-H22); báo động sai trong vận hành; D (G2-H24) | B16 mục 8 yêu cầu manifest ghi lỗi đã tiêm và độ lệch đồng hồ; **chưa** yêu cầu mốc có tác động, mốc hồi phục và lượt nền được kiểm riêng | Nhóm hệ thống (bộ tiêm lỗi do Minh dựng, Q-19) |
| Nhật ký của bộ tạo tải | Dataset không công bố | Tách “tải đổi” khỏi “sự cố” ở các báo động trước mốc | B16 mục 8 có ghi workload trong manifest; chưa có log theo thời gian của bộ tạo tải | Nhóm hệ thống |
| Ánh xạ dịch vụ–máy và metric mức máy | Không có trong hai dataset | Vì sao dịch vụ không liên hệ đổi tại mốc (G2-H11) | B16 mục 4 có `hostId`; mục 5 có metric hạ tầng | Đã nằm trong chuẩn; cần kiểm khi chạy |
| Loại span và thuộc tính thông điệp, cơ sở dữ liệu | Trace của hai dataset không ghi (thẻ dataset của T-002 và T-008) | Dựng cạnh thông điệp và cạnh dữ liệu của DT18 (mục 5, thành phần DT18 yêu cầu) | B16 mục 3 có quy định span hoặc link cho bên gửi và bên nhận thông điệp; chưa thấy yêu cầu ghi loại span và thuộc tính cơ sở dữ liệu | Nhóm hệ thống |
| Mốc thời gian yêu cầu tới phía được gọi, trước hàng đợi | Mỗi lời gọi chỉ có hai span | Phần chậm ngoài span của root là gì (T-032, KT13) | B16 chưa có | Nhóm hệ thống, nếu Minh quyết cần |
| Kết quả của từng yêu cầu nối được với trace và span | Log có kết quả ở vài nơi nhưng chưa có phép nối được xác minh | Chuẩn “khỏe/hỏng” độc lập cho phát hiện (G2-H24) | B16 mục 4: log có `outcome`, `traceId`, `spanId` | Đã nằm trong chuẩn; cần kiểm khi chạy |
| Phiên bản mã, công cụ ghi span, cấu hình lấy mẫu | Tác giả RE2-TT không công bố | Mức đo “chờ root” ở RE2-TT (mục 4) | B16 mục 8: manifest ghi phiên bản và cấu hình lấy mẫu | Đã nằm trong chuẩn |
| Nền đủ dài, metric đủ dày | Nezha-OB chỉ có nền trace rất ngắn | CIRCA không chạy được (Q-85); thống kê nền kém ổn định | B16 mục 6: thời gian lưu; mục phụ lục giữ OPEN cửa sổ trước lỗi ở từng lượt | Nhóm hệ thống |

Bộ thu thập không khôi phục được thông tin chưa từng được ghi. Các dòng “chưa có” ở trên là **nội dung đề nghị** cho bản “Yêu cầu quan sát cho RCA” (P9a); gói này không tự sửa yêu cầu P9a.

### 6.3 Thuộc đánh giá sau khi khóa thiết kế

| Câu | Bằng chứng cần | Ở đâu |
|---|---|---|
| Phương pháp đồ thị có khắc phục các hạn chế ở mục 3 không (RQ3)? | Kết quả trên test và dataset giữ ngoài, so với baseline tốt nhất của P3 | P7, sau G3 |
| Lợi ích có đến từ quan hệ thật không (RQ3d)? | Nhánh cùng bằng chứng không dùng quan hệ; đồ thị ngẫu nhiên giữ bậc; báo theo ô và theo ca | P7 |
| Các phát hiện trên dev có giữ trên ca chưa nhìn không (T-032, KT16)? | Chạy một lần trên test sau khi khóa | P7; Minh cho phép mở test ở G3 |
| Có khác biệt giữa nhóm “lan” và “không lan” không? | Chỉ khi nhãn lan được định nghĩa và khóa ở G3 | P7 |
| Hướng lan có giúp phân biệt “tải tăng” với “sự cố” không (câu phụ của RQ5)? | Dữ liệu FlashTicket với kịch bản flash sale | P10 |
| Vùng ảnh hưởng (RQ3c) | Nhãn vùng lấy từ tín hiệu mà bộ chẩn đoán không dùng | P10 |

Không dùng test để hoàn tất một lựa chọn thiết kế còn thiếu căn cứ trên dev.

## 7. K7 — Hỏi–đáp cho cô

Mỗi câu ghi mức bằng chứng và nguồn. Con trỏ JSON của từng số nằm trong sổ số liệu nêu ở đầu file.

**1. Vì sao dùng RE2-TT và Nezha-OB?**
RE2-TT là bộ Train Ticket duy nhất vừa có ba lần lặp mỗi ô, đủ ba tín hiệu, lỗi tài nguyên và mạng, vừa còn ca chưa chạy phương pháp. Nezha-OB thêm lỗi mã nguồn, một hệ thứ hai và một nhóm tác giả độc lập. Chọn theo tiêu chí, kiểm trên file thật ở P2. *Mức: MT (kiểm kê dữ liệu). Nguồn:* `results/T-021/goi-g1.md` mục 3.1–3.3; quyết định Q-61 đến Q-69.

**2. Vì sao không dùng Sock Shop và LEMMA-RCA?**
Sock Shop trong bộ RCAEval không có file trace ở toàn bộ bản phát hành, nên không ánh xạ được trace lên đồ thị. LEMMA-RCA: mẫu đã kiểm không có trace, nhãn root chỉ là một thực thể mỗi ngày, giấy phép còn mâu thuẫn. Sock Shop có thể dùng có chủ đích cho kịch bản “đồ thị dựng từ kiến trúc”; chưa đề xuất. *Mức: MT. Nguồn:* `results/T-021/goi-g1.md` mục 3.4; `results/T-019/the-sock-shop.md` (bảng tiêu chí, dòng “Parent trace”); `results/T-011/the-dataset.md` mục 2.

**3. Vì sao chưa có Eadro-TT trong bảng?**
Phép kiểm điều kiện dùng cho thấy đồng hồ của trace, cách ghép theo cửa sổ và tính đại diện của dữ liệu tham chiếu còn mở. Minh quyết không đưa Eadro vào thực nghiệm tới G2 và không kết luận là không dùng được về sau. *Mức: MT. Nguồn:* quyết định Q-83; `results/T-023/kiem-eadro.md`.

**4. Baseline nào mạnh nhất, trong điều kiện nào?**
Trên RE2-TT, khi biết mốc tiêm, theo điểm ước lượng: TORAI B (Hit@1 {{bl.re2.torai_B.h1:.3f}}) và SimpleRCA ({{bl.re2.simplerca.h1:.3f}}), SimpleRCA không dùng quan hệ gọi, còn ở TORAI B bước nhân quả không quyết định hạng của root; khoảng bootstrap của chúng chồng với BARO và TraceRCA. Trên Nezha-OB không phương pháp nào mạnh: cao nhất là BARO {{bl.nz.baro.h1:.3f}}. Không phương pháp nào tốt ở mọi ô. *Mức: MT (bảng chấm đã kiểm lại độc lập). Nguồn:* mục 2.1–2.4; `results/T-034/bang-baseline.json`.

**5. Số của nhóm có khớp số đã công bố không?**
BARO và TORAI bản gốc khớp số công bố trên dataset của bài. SimpleRCA chưa tái lập được vì bài báo trên cả bộ, phần test đang khóa. MicroRank và TraceRCA trong thư viện khác bài gốc; CIRCA lệch ở mức ô. Trên RE2-TT với giao thức của nhóm thì chỉ so tham khảo. *Mức: MT. Nguồn:* mục 2.7.

**6. Các phương pháp xếp hạng hỏng ở đâu, vì sao?**
Đã lần được tới bước gây sai ở phần lớn nhóm: bước chia trace của MicroRank; TraceRCA bản thư viện chấm thời gian chờ thành bất thường của dịch vụ gọi; BARO chia cho độ biến thiên của nền gần phẳng (giải thích một phần ca sai); SimpleRCA để phiếu metric lấn át; CIRCA có phần dư gần bằng không cho điểm cực lớn, root mất hạng 1 trước cả bước cộng điểm. Phần chưa phân xử: vì sao dịch vụ không liên hệ đổi tại mốc. *Mức: CT ở các dòng nêu trên. Nguồn:* mục 3, dòng G2-H01 đến G2-H15.

**7. Bộ phát hiện hỏng ở đâu, vì sao?**
Cả hai bộ đều báo động trước mốc tiêm ở hầu hết ca ({{bl.det.bocpd.first_ok}}/{{bl.det.bocpd.n}} và {{bl.det.nsigma.first_ok}}/{{bl.det.nsigma.n}} ca có báo động đầu đúng). Đã xác lập: tiền xử lý của BOCPD dùng cả dữ liệu sau mốc; kết quả nhạy với prior. Chưa phân xử: các báo động trước mốc là sai hay là biến động thật, vì dataset không có nền sạch và onset được xác nhận độc lập. *Mức: CT cho hai điều đã xác lập; CK cho điều chưa phân xử. Nguồn:* mục 2.5 và dòng G2-H20 đến G2-H24.

**8. “Nhầm triệu chứng lan với nguyên nhân” có đáng kể không?**
Lan là hiện tượng phổ biến ở mức quan sát: độ trễ của root hiện ở phía gọi trong phần lớn ca đo được. Với TraceRCA bản thư viện, chuỗi chờ → cờ → điểm đã xác lập, nhưng bỏ phần chờ chỉ đổi ít ca. Với trễ mạng mới biết dấu hiệu nằm ở phía gọi. Lan gây bao nhiêu ca sai thì chưa phân xử ở mọi phương pháp: chưa có căn cứ nói nó gây phần lớn ca sai, cũng chưa có căn cứ nói nó là thiểu số; tìm thấy một cơ chế chấm khác không loại được vai trò của lan. Hiện tượng chờ cũng có ở ca đúng. *Mức: ĐC cho hiện tượng; CT cho chuỗi tính của TraceRCA; chưa phân xử cho câu tổng. Nguồn:* mục 4.

**9. Lỗi là do dữ liệu, do bản cài hay do phương pháp?**
Cả ba, và đã tách ở từng dòng của bản đồ. Do bản cài hoặc đầu vào ta dựng: MicroRank, TraceRCA bản thư viện, bảng log TORAI nguồn B. Do cách tính: BARO, SimpleRCA bản M4 theo quy ước T-017, CIRCA. Do dữ liệu: nền ngắn ở Nezha-OB, root không được gọi, thiếu onset. *Mức: theo từng dòng. Nguồn:* mục 3.1, cột “Loại nguồn”.

**10. TraceRCA theo mã tác giả cho kết quả thế nào?**
Nhánh chỉ dùng độ trễ của mã tác giả đúng {{bl.author.nz.ms1.exp:.3g}}/{{bl.author.nz.ms1.n}} ca kỳ vọng ở Nezha-OB và {{bl.author.re2.ms1.exp:.3g}}/{{bl.author.re2.ms1.n}} ca ở RE2-TT (ngưỡng chọn đặc trưng một). Đây là chẩn đoán trên dev đã nhìn, không phải tái lập bài: đầu vào thiếu trạng thái HTTP và nền nhiều ngày. Có đưa nó vào kế hoạch baseline hay không là việc Minh quyết. *Mức: MT. Nguồn:* mục 2.8.

**11. Hai phép kiểm bổ sung cho biết gì?**
Phép E1: ở cấu hình mặc định của bài TraceRCA, quy tắc chấm qua tập nhiều dịch vụ có đóng góp nhưng không đủ: nó đảo chiều {{e1.top.nz.flip}}/{{e1.top.nz.phen}} cặp và làm giảm điểm dịch vụ gọi ở {{e1.top.nz.unch_both}} cặp khác mà chưa đảo chiều; ở mức cờ cao nó đảo chiều {{e1.top3.nz.flip}}/{{e1.top3.nz.phen}} cặp. Phép E2: underflow làm đổi điểm đổi của BOCPD ở {{e2.chains_differ}}/{{e2.chains}} chuỗi, trong một đoạn ngắn sau mốc; không giải thích báo động trước mốc. *Mức: CT, trong phạm vi đã khai. Nguồn:* `results/T-034/hai-phep-kiem.md`.

**12. Câu nào chưa trả lời được, và kế hoạch?**
Ba nhóm. Còn kiểm được trên dev: bảy dòng ở mục 6.1. Thiếu quan sát: onset, nền sạch, quan hệ dịch vụ–máy; chuyển thành yêu cầu quan sát cho FlashTicket. Thuộc đánh giá sau: đồ thị có giúp không. *Mức: CK. Nguồn:* mục 6.

**13. Đồ thị sẽ nhắm vào hạn chế nào?**
Các ứng viên có căn cứ để thử chia ba loại. Dùng cạnh đồ thị dịch vụ: gắn thời gian lời gọi lên cạnh, tính cho dịch vụ được gọi. Dùng quan hệ cha–con trong trace: thời gian tự xử lý; tiêu chí yêu cầu bất thường theo cây lời gọi. Yêu cầu kỹ thuật: chặn giá trị không hợp lệ khi lan điểm. Các thành phần khác (cạnh thông điệp, cạnh dữ liệu, vùng nghi ngờ) làm vì DT18 yêu cầu, không vì một hạn chế đã thấy. *Mức: ĐC hoặc CT cho căn cứ đề xuất; chưa có bằng chứng lợi ích. Nguồn:* mục 5.

**14. Khi nào biết đồ thị có giúp không?**
Sau P7, khi đủ ba thứ: hơn nhánh cùng bằng chứng không dùng quan hệ; hơn đồ thị ngẫu nhiên giữ bậc; báo theo ô và theo ca. Trên dev có hai điều bất lợi cho giả thuyết “xử lý triệu chứng ở phía gọi”: trên RE2-TT, SimpleRCA không dùng quan hệ gọi mà vẫn thuộc nhóm đứng đầu; phần lớn cặp sai của MicroRank và BARO không nằm phía trên root theo quan hệ gọi. Chúng chưa nói được về đồ thị nói chung. “Đồ thị không giúp ở điều kiện X, vì Y” là một kết quả hợp lệ. *Mức: CK. Nguồn:* MRP §6; mục 0 và mục 5.

**15. Vì sao chưa trình kết quả phương pháp đồ thị?**
Cô yêu cầu chỉ ra hạn chế của phương pháp đã có rồi mới sang đồ thị. Gói này là bước đó. Thiết kế đồ thị (P5, P6) bắt đầu sau khi Minh duyệt cổng này; kết quả dự kiến cuối tháng 11/2026. *Loại: kế hoạch, không phải kết quả. Nguồn:* MRP §2.1, §7; quyết định Q-70.

**16. Vì sao chọn các phương pháp này?**
MRP đặt ba tiêu chí: phủ các cách tiếp cận khác nhau, có mã chạy được, được bài gần đây dùng làm baseline. Theo đó: thống kê trên metric (BARO, N-Sigma); nhân quả (CIRCA, TORAI); dựa trên trace (MicroRank, TraceRCA); đa nguồn (SimpleRCA, TORAI). Minh chốt danh sách gọn và chia hai tầng; tầng hai (RCD, GDN, CIRCA-PC) chưa chạy tới G2. Họ “học có đồ thị” chưa có đại diện xếp hạng: ứng viên duy nhất là Eadro, bị loại vì cần nhãn để học và có lỗi trong cách đánh giá. *Mức: MT. Nguồn:* MRP mục P1; `results/T-001/danh-sach-phuong-phap.md` (bảng phủ các họ); quyết định Q-37, Q-38, Q-62.

## 8. Điểm Minh quyết ở G2

**Đã quyết từ trước, gói này giữ nguyên:** bảng baseline và cách chấm đã khóa (T-024, T-025, T-026); CIRCA dùng bản gốc và báo riêng nhóm ca (Q-82); không dùng Eadro tới G2 (Q-83); câu “lan” xử lý ở gói này (Q-86).

**Cần Minh quyết:**

1. **Duyệt cổng G2:** bảng baseline trên dev (mục 2) và bản đồ hạn chế (mục 3).
2. **Nhánh TraceRCA theo mã tác giả** (mục 2.8): (a) chỉ giữ làm chẩn đoán; hay (b) đưa vào kế hoạch baseline của P7, khi đó phải khai hợp đồng đầu vào, cấu hình, quy tắc hòa và cách xử lý ca thiếu bằng chứng trước khi mở test. Tôi không tự chọn ngưỡng theo điểm dev.
3. **Nhãn lan** (mục 4.3): (a) mở một task nhỏ hoàn thiện nháp và khóa ở G3; hay (b) không tách nhóm lan ở P7.
4. **Bốn ca ERROR** của MicroRank và TraceRCA ở RE2-TT: gói giữ cách chấm đã khóa (tính trượt, WHY-28). Đề nghị trình kèm một dòng chẩn đoán: khi bỏ thao tác thiếu nền, TraceRCA xếp root hạng 1 ở {{d4.tracerca.hit1}}/{{t28.re2.tracerca.khongok}} ca đó (G2-H16). Minh quyết có trình kèm không.
5. **TORAI nguồn B:** bảng log do ta dựng làm sai {{h16.wrong}} ca, bỏ nguồn log thì sửa {{h16.fixed}} ca (G2-H14). Giữ nguồn B làm dòng chính như đã khóa, hay thêm một dòng độ nhạy “bỏ nguồn log” khi trình bảng. Không đổi baseline.
6. **Dòng độ nhạy MicroRank** (bộ chia theo công thức bài gốc): trình như dòng chẩn đoán ở mục 2.8, hay đưa thành một biến thể baseline của P7.
7. **Sau E1 và E2** (mục 6.1): có giao các phép còn kiểm được trên dev không, và phép nào. Phép chạy miền log trên các ca còn lại cần hơn một giờ máy; phải có lời duyệt riêng.
8. **Ghi sổ quyết định.** Chưa có dòng nào trong `docs/DECISIONS.md` cho các lời duyệt của T-034 (duyệt SPEC bản ba, sửa R1–R5, đưa E1 và E2 vào task). Tôi sẽ trình nguyên văn dòng đề xuất trong chat. Nguyên văn lời cho phép của Q-144 cũng còn để mở trong sổ đối chiếu.
9. **Nội dung đề nghị cho P9a** (mục 6.2): có chuyển các dòng “chưa có” thành yêu cầu quan sát gửi nhóm hệ thống không.
10. **Cập nhật tài liệu sau G2** (PLAN, STATE, MRP nếu cần): tôi chỉ đề xuất sau khi Minh quyết các điểm trên.

**Gói này không làm:** không chọn thành phần P5/P6; không khóa nhãn lan; không mở test; không sửa bảng baseline hay quy tắc chấm.

## Phụ lục A — Xếp hạng theo ô: ca sai, cờ T-028, tác dụng của các phép đổi của T-032

Mỗi bảng là một cặp (dataset, phương pháp). “Sai hạng 1” tính hạng bi quan khi hòa, trên các ca chạy được. Cột “Phép đổi” ghi: số ca sai mà root lên hạng 1 sau phép đổi, trên số ca sai có kết quả ở nhánh đổi. Các phép đổi là chẩn đoán, nghĩ ra sau khi xem dev.

@@appendix_a@@

## Phụ lục B — Phát hiện theo ô: các cờ HP của T-029

Mỗi ô ghi số ca có cờ trên số ca hợp lệ. Ý nghĩa từng cờ ở `results/T-029/ban-do-han-che-phat-hien.md`.

@@appendix_b@@

## Phụ lục C — Bảng theo ô của các dòng không thuộc Phụ lục A, B (G2-H19, G2-H23, G2-H24, G2-H25, G2-H26)

@@appendix_c@@
