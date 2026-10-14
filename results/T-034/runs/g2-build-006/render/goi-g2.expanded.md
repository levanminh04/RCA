# Gói trình G2 (T-034): baseline trên dev, bản đồ hạn chế, căn cứ cho bước đồ thị

Ngày 13/10/2026. Người làm: Claude. Người phản biện kết quả: Codex. Trạng thái: chờ phản biện, chờ Minh duyệt.

**Minh cần duyệt gì ở cổng này** (MRP §7, cổng G2): bảng baseline trên dev (mục 2) và bản đồ hạn chế (mục 3). Các điểm cần quyết thêm nằm ở mục 8.

**Cách đọc.**

- Mọi số là trên phần **dev**: {{bl.re2.n}} ca RE2-TT (hệ Train Ticket) và {{bl.nz.n}} ca Nezha-OB (hệ Online Boutique). Chưa mở test và dataset giữ ngoài.
- *Root* là thành phần gốc gây lỗi theo nhãn. *Ô* là một cặp (root, loại lỗi). *Chế độ (a)*: phương pháp xếp hạng được cho biết mốc tiêm lỗi. *Chế độ (b)*: bộ phát hiện tự báo động, rồi phương pháp xếp hạng chạy tại báo động đầu.
- *Hit@1* là tỷ lệ ca root đứng hạng 1; khi hòa thì tính kỳ vọng. Ca không chạy được vẫn nằm trong mẫu số và tính trượt.
- Mỗi kết luận ghi một **mức bằng chứng** (WHY-51): **CT** can thiệp (đổi có kiểm soát một đầu vào hay một bước, xem đầu ra của chính phương pháp); **ĐC** đo trực tiếp đại lượng mà cơ chế giả định; **LĐ** liên hệ có đối chứng; **MT** mô tả; **CK** chưa kiểm.
- Câu “vì sao” có ba trạng thái: *đã xác lập ở mức X*, *đã loại giải thích Y*, *chưa phân xử vì Z*.
- Mọi con số trong file này được điền bằng máy từ file kết quả. Sổ (file, con trỏ JSON) của từng số: `results/T-034/runs/g2-build-006/render/registry.json`. Kết quả kiểm: `results/T-034/runs/g2-build-006/v4.json`. Bản này đã sửa bốn lần sau phản biện ngày 13/10/2026 và 14/10/2026; các bản trước lưu ở `results/T-034/runs/phat-hanh-001/` đến `phat-hanh-004/`.

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

1. **Hạn chế đã xác nhận và điều kiện** (mức của dòng là CT hoặc ĐC; mức đó thuộc phần nào thì ghi ở trường “Vì sao”): G2-H01, G2-H02, G2-H03, G2-H04, G2-H05, G2-H06, G2-H08, G2-H09, G2-H12, G2-H13, G2-H14, G2-H16, G2-H17, G2-H19, G2-H20, G2-H21, G2-H22, G2-H23, G2-H26. Điều kiện của từng dòng ghi ở trường “Vì sao” và “Giải thích khác”.
2. **Thuộc bản cài, đầu vào do ta dựng, giao thức hoặc thiếu dữ liệu** (loại A, G, D): G2-H01, G2-H03, G2-H04, G2-H05, G2-H06, G2-H07, G2-H08, G2-H10, G2-H11, G2-H13, G2-H14, G2-H15, G2-H16, G2-H17, G2-H19, G2-H20, G2-H21, G2-H23, G2-H24, G2-H25, G2-H26.
3. **Thuộc giả định hoặc cách tính của phương pháp** (loại M): G2-H02, G2-H05, G2-H06, G2-H07, G2-H08, G2-H09, G2-H10, G2-H12, G2-H13, G2-H17, G2-H21, G2-H22, G2-H23, G2-H26.
4. **Quan hệ giữa dịch vụ có thể bổ sung thông tin gì:** mục 5 (ứng viên), không phải bằng chứng đồ thị đã giúp.
5. **Câu chưa trả lời** (dòng còn phần “chưa phân xử”): G2-H01, G2-H02, G2-H05, G2-H06, G2-H07, G2-H09, G2-H10, G2-H11, G2-H12, G2-H13, G2-H15, G2-H17, G2-H18, G2-H20, G2-H21, G2-H22, G2-H23, G2-H24, G2-H25, G2-H26; chi tiết và nơi phân xử ở mục 6.

## 2. K2 — Bảng baseline trên dev

Bảng chính lấy nguyên số của T-024, T-025, T-026 (đã khóa); gói này không chạy lại phương pháp nào để thay bảng. Số máy đọc: `results/T-034/bang-baseline.json`. Phép kiểm V2 tính lại mọi số tổng từ bản ghi từng lượt bằng một bộ chấm viết riêng: {{bl.v2.status:x}}, {{bl.v2.problems}} lệch.

### 2.1 Xếp hạng, chế độ (a), RE2-TT ({{bl.re2.n}} ca, {{bl.re2.cells}} ô)

| Phương pháp | Trạng thái (số ca) | Hit@1 | Khoảng bootstrap của Hit@1 | Hit@3 | Hit@5 | MRR | NDCG@5 | Avg@5 | Retrieval@5 | Rerank@1 (K=5) |
|---|---|---|---|---|---|---|---|---|---|---|
| BARO | OK: {{a0001}} | {{a0004:.3f}} | [{{a0002:.2f}}; {{a0003:.2f}}] | {{a0005:.3f}} | {{a0006:.3f}} | {{a0007:.3f}} | {{a0008:.3f}} | {{a0009:.3f}} | {{a0010:.3f}} | {{a0011:.3f}} |
| SimpleRCA | OK: {{a0012}} | {{a0015:.3f}} | [{{a0013:.2f}}; {{a0014:.2f}}] | {{a0016:.3f}} | {{a0017:.3f}} | {{a0018:.3f}} | {{a0019:.3f}} | {{a0020:.3f}} | {{a0021:.3f}} | {{a0022:.3f}} |
| MicroRank | OK: {{a0023}}, ERROR: {{a0024}} | {{a0027:.3f}} | [{{a0025:.2f}}; {{a0026:.2f}}] | {{a0028:.3f}} | {{a0029:.3f}} | {{a0030:.3f}} | {{a0031:.3f}} | {{a0032:.3f}} | {{a0033:.3f}} | {{a0034:.3f}} |
| TraceRCA | OK: {{a0035}}, ERROR: {{a0036}} | {{a0039:.3f}} | [{{a0037:.2f}}; {{a0038:.2f}}] | {{a0040:.3f}} | {{a0041:.3f}} | {{a0042:.3f}} | {{a0043:.3f}} | {{a0044:.3f}} | {{a0045:.3f}} | {{a0046:.3f}} |
| CIRCA | OK: {{a0047}} | {{a0050:.3f}} | [{{a0048:.2f}}; {{a0049:.2f}}] | {{a0051:.3f}} | {{a0052:.3f}} | {{a0053:.3f}} | {{a0054:.3f}} | {{a0055:.3f}} | {{a0056:.3f}} | {{a0057:.3f}} |
| TORAI B | OK: {{a0058}} | {{a0061:.3f}} | [{{a0059:.2f}}; {{a0060:.2f}}] | {{a0062:.3f}} | {{a0063:.3f}} | {{a0064:.3f}} | {{a0065:.3f}} | {{a0066:.3f}} | {{a0067:.3f}} | {{a0068:.3f}} |

Khoảng bootstrap lấy mẫu theo ô, mức 95%. Avg@5 là trung bình AC@1 đến AC@5 theo cách của RCAEval. Retrieval@5 là tỷ lệ ca root lọt vào năm hạng đầu; Rerank@1 là tỷ lệ root hạng 1 trong các ca đó (Q-65).

Khoảng của BARO, SimpleRCA, TraceRCA và TORAI B chồng nhau: với {{bl.re2.n}} ca, bảng không phân định được thứ tự giữa bốn phương pháp này.

MicroRank và TraceRCA mỗi phương pháp có {{bl.re2.tracerca.st.ERROR}} ca dừng lỗi, tính trượt. CIRCA: {{h13.huge}} ca có nút điểm cực lớn (G2-H12), báo riêng ở mục 2.3.

### 2.2 RE2-TT theo ô: số ca root hạng 1 (kỳ vọng khi hòa) trên số ca

| Ô (root / loại lỗi) | Số ca | BARO | SimpleRCA | MicroRank | TraceRCA | CIRCA | TORAI B |
|---|---|---|---|---|---|---|---|
| auth / cpu | {{a0069}} | {{a0070:.3g}} | {{a0071:.3g}} | {{a0072:.3g}} | {{a0073:.3g}} | {{a0074:.3g}} | {{a0075:.3g}} |
| auth / delay | {{a0076}} | {{a0077:.3g}} | {{a0078:.3g}} | {{a0079:.3g}} | {{a0080:.3g}} | {{a0081:.3g}} | {{a0082:.3g}} |
| order / disk | {{a0083}} | {{a0084:.3g}} | {{a0085:.3g}} | {{a0086:.3g}} | {{a0087:.3g}} | {{a0088:.3g}} | {{a0089:.3g}} |
| order / loss | {{a0090}} | {{a0091:.3g}} | {{a0092:.3g}} | {{a0093:.3g}} | {{a0094:.3g}} | {{a0095:.3g}} | {{a0096:.3g}} |
| route / mem | {{a0097}} | {{a0098:.3g}} | {{a0099:.3g}} | {{a0101:.3g}} (ERROR: {{a0100}}) | {{a0103:.3g}} (ERROR: {{a0102}}) | {{a0104:.3g}} | {{a0105:.3g}} |
| route / socket | {{a0106}} | {{a0107:.3g}} | {{a0108:.3g}} | {{a0110:.3g}} (ERROR: {{a0109}}) | {{a0112:.3g}} (ERROR: {{a0111}}) | {{a0113:.3g}} | {{a0114:.3g}} |
| train / cpu | {{a0115}} | {{a0116:.3g}} | {{a0117:.3g}} | {{a0118:.3g}} | {{a0119:.3g}} | {{a0120:.3g}} | {{a0121:.3g}} |
| train / delay | {{a0122}} | {{a0123:.3g}} | {{a0124:.3g}} | {{a0126:.3g}} (ERROR: {{a0125}}) | {{a0128:.3g}} (ERROR: {{a0127}}) | {{a0129:.3g}} | {{a0130:.3g}} |
| travel / disk | {{a0131}} | {{a0132:.3g}} | {{a0133:.3g}} | {{a0134:.3g}} | {{a0135:.3g}} | {{a0136:.3g}} | {{a0137:.3g}} |
| travel / loss | {{a0138}} | {{a0139:.3g}} | {{a0140:.3g}} | {{a0142:.3g}} (ERROR: {{a0141}}) | {{a0144:.3g}} (ERROR: {{a0143}}) | {{a0145:.3g}} | {{a0146:.3g}} |

### 2.3 Nhóm ca theo Q-82: {{bl.re19.n}} ca CIRCA không có nút điểm cực lớn

| Phương pháp | Trạng thái (số ca) | Hit@1 | Khoảng bootstrap của Hit@1 | Hit@3 | Hit@5 | MRR | NDCG@5 | Avg@5 | Retrieval@5 | Rerank@1 (K=5) |
|---|---|---|---|---|---|---|---|---|---|---|
| BARO | OK: {{a0147}} | {{a0150:.3f}} | [{{a0148:.2f}}; {{a0149:.2f}}] | {{a0151:.3f}} | {{a0152:.3f}} | {{a0153:.3f}} | {{a0154:.3f}} | {{a0155:.3f}} | {{a0156:.3f}} | {{a0157:.3f}} |
| SimpleRCA | OK: {{a0158}} | {{a0161:.3f}} | [{{a0159:.2f}}; {{a0160:.2f}}] | {{a0162:.3f}} | {{a0163:.3f}} | {{a0164:.3f}} | {{a0165:.3f}} | {{a0166:.3f}} | {{a0167:.3f}} | {{a0168:.3f}} |
| MicroRank | OK: {{a0169}}, ERROR: {{a0170}} | {{a0173:.3f}} | [{{a0171:.2f}}; {{a0172:.2f}}] | {{a0174:.3f}} | {{a0175:.3f}} | {{a0176:.3f}} | {{a0177:.3f}} | {{a0178:.3f}} | {{a0179:.3f}} | {{a0180:.3f}} |
| TraceRCA | OK: {{a0181}}, ERROR: {{a0182}} | {{a0185:.3f}} | [{{a0183:.2f}}; {{a0184:.2f}}] | {{a0186:.3f}} | {{a0187:.3f}} | {{a0188:.3f}} | {{a0189:.3f}} | {{a0190:.3f}} | {{a0191:.3f}} | {{a0192:.3f}} |
| CIRCA | OK: {{a0193}} | {{a0196:.3f}} | [{{a0194:.2f}}; {{a0195:.2f}}] | {{a0197:.3f}} | {{a0198:.3f}} | {{a0199:.3f}} | {{a0200:.3f}} | {{a0201:.3f}} | {{a0202:.3f}} | {{a0203:.3f}} |
| TORAI B | OK: {{a0204}} | {{a0207:.3f}} | [{{a0205:.2f}}; {{a0206:.2f}}] | {{a0208:.3f}} | {{a0209:.3f}} | {{a0210:.3f}} | {{a0211:.3f}} | {{a0212:.3f}} | {{a0213:.3f}} | {{a0214:.3f}} |

Nhóm {{bl.re19.n}} ca này được chọn từ đầu ra của CIRCA, không phải mẫu ngẫu nhiên; cùng một tập cho mọi phương pháp (WHY-36). Trên nhóm này CIRCA đạt {{bl.re19.circa_ols_da.h1:.3f}}, so với {{bl.re2.circa_ols_da.h1:.3f}} trên cả {{bl.re2.n}} ca.

### 2.4 Xếp hạng, chế độ (a), Nezha-OB ({{bl.nz.n}} ca, {{bl.nz.cells}} ô)

| Phương pháp | Trạng thái (số ca) | Hit@1 | Khoảng bootstrap của Hit@1 | Hit@3 | Hit@5 | MRR | NDCG@5 | Avg@5 | Retrieval@5 | Rerank@1 (K=5) |
|---|---|---|---|---|---|---|---|---|---|---|
| BARO | OK: {{a0215}} | {{a0218:.3f}} | [{{a0216:.2f}}; {{a0217:.2f}}] | {{a0219:.3f}} | {{a0220:.3f}} | {{a0221:.3f}} | {{a0222:.3f}} | {{a0223:.3f}} | {{a0224:.3f}} | {{a0225:.3f}} |
| SimpleRCA | OK: {{a0226}} | {{a0229:.3f}} | [{{a0227:.2f}}; {{a0228:.2f}}] | {{a0230:.3f}} | {{a0231:.3f}} | {{a0232:.3f}} | {{a0233:.3f}} | {{a0234:.3f}} | {{a0235:.3f}} | {{a0236:.3f}} |
| MicroRank | OK: {{a0237}} | {{a0240:.3f}} | [{{a0238:.2f}}; {{a0239:.2f}}] | {{a0241:.3f}} | {{a0242:.3f}} | {{a0243:.3f}} | {{a0244:.3f}} | {{a0245:.3f}} | {{a0246:.3f}} | {{a0247:.3f}} |
| TraceRCA | OK: {{a0248}} | {{a0251:.3f}} | [{{a0249:.2f}}; {{a0250:.2f}}] | {{a0252:.3f}} | {{a0253:.3f}} | {{a0254:.3f}} | {{a0255:.3f}} | {{a0256:.3f}} | {{a0257:.3f}} | {{a0258:.3f}} |
| CIRCA | UNSUPPORTED: {{a0259}} | không chạy được |  |  |  |  |  |  |  |  |
| TORAI B | UNSUPPORTED: {{a0260}} | không chạy được |  |  |  |  |  |  |  |  |

| Ô (root / loại lỗi) | Số ca | BARO | SimpleRCA | MicroRank | TraceRCA | CIRCA | TORAI B |
|---|---|---|---|---|---|---|---|
| ad / cpu_contention | {{a0261}} | {{a0262:.3g}} | {{a0263:.3g}} | {{a0264:.3g}} | {{a0265:.3g}} | — | — |
| checkout / exception | {{a0266}} | {{a0267:.3g}} | {{a0268:.3g}} | {{a0269:.3g}} | {{a0270:.3g}} | — | — |
| checkout / network_delay | {{a0271}} | {{a0272:.3g}} | {{a0273:.3g}} | {{a0274:.3g}} | {{a0275:.3g}} | — | — |
| checkout / return | {{a0276}} | {{a0277:.3g}} | {{a0278:.3g}} | {{a0279:.3g}} | {{a0280:.3g}} | — | — |
| email / cpu_consumed | {{a0281}} | {{a0282:.3g}} | {{a0283:.3g}} | {{a0284:.3g}} | {{a0285:.3g}} | — | — |
| email / network_delay | {{a0286}} | {{a0287:.3g}} | {{a0288:.3g}} | {{a0289:.3g}} | {{a0290:.3g}} | — | — |
| frontend / return | {{a0291}} | {{a0292:.3g}} | {{a0293:.3g}} | {{a0294:.3g}} | {{a0295:.3g}} | — | — |
| payment / cpu_contention | {{a0296}} | {{a0297:.3g}} | {{a0298:.3g}} | {{a0299:.3g}} | {{a0300:.3g}} | — | — |
| productcatalog / exception | {{a0301}} | {{a0302:.3g}} | {{a0303:.3g}} | {{a0304:.3g}} | {{a0305:.3g}} | — | — |
| recommendation / cpu_consumed | {{a0306}} | {{a0307:.3g}} | {{a0308:.3g}} | {{a0309:.3g}} | {{a0310:.3g}} | — | — |
| recommendation / network_delay | {{a0311}} | {{a0312:.3g}} | {{a0313:.3g}} | {{a0314:.3g}} | {{a0315:.3g}} | — | — |
| shipping / cpu_consumed | {{a0316}} | {{a0317:.3g}} | {{a0318:.3g}} | {{a0319:.3g}} | {{a0320:.3g}} | — | — |
| shipping / cpu_contention | {{a0321}} | {{a0322:.3g}} | {{a0323:.3g}} | {{a0324:.3g}} | {{a0325:.3g}} | — | — |

Hai dataset khác nhịp metric và độ dài nền (WHY-37); so giữa hai dataset chỉ để mô tả.

### 2.5 Phát hiện, chế độ (b), RE2-TT

| Bộ phát hiện | Precision | Recall | F1 | Báo động trên đoạn bình thường theo nhãn proxy | Mỗi giờ bình thường | Độ trễ từ mốc tiêm, giây: trung vị (nhỏ nhất–lớn nhất) | Ca có báo động đầu ở hoặc sau mốc |
|---|---|---|---|---|---|---|---|
| BOCPD | {{a0326:.3f}} | {{a0327:.3f}} | {{a0328:.3f}} | {{a0329}} / {{a0330}} giây | {{a0331:.1f}} | {{a0332:.0f}} ({{a0333}}–{{a0334}}) | {{a0335}}/{{a0336}} |
| N-Sigma (bộ cột chính) | {{a0337:.3f}} | {{a0338:.3f}} | {{a0339:.3f}} | {{a0340}} / {{a0341}} giây | {{a0342:.1f}} | {{a0343:.0f}} ({{a0344}}–{{a0345}}) | {{a0346}}/{{a0347}} |
| N-Sigma (bộ cột đối chứng) | {{a0348:.3f}} | {{a0349:.3f}} | {{a0350:.3f}} | {{a0351}} / {{a0352}} giây | {{a0353:.1f}} | {{a0354:.0f}} ({{a0355}}–{{a0356}}) | {{a0357}}/{{a0358}} |

**Phải đọc kèm ba điều.**

- Nhãn dùng để chấm là nhãn proxy của giao thức (WHY-35): từ mốc tiêm tới cuối file là “bất thường”. Dataset không xác nhận độc lập đoạn trước mốc là khỏe, lúc lỗi bắt đầu có tác động, hay lúc hết lỗi.
- Vì vậy “báo động trên đoạn bình thường” **không** phải tỷ lệ báo động sai trong vận hành thật, và độ trễ là tính từ **mốc tiêm**, không phải từ lúc sự cố bắt đầu biểu hiện.
- Precision, Recall, F1 tính theo cửa sổ 60 giây.

Theo ô:

| Ô (root / loại lỗi) | Số ca | BOCPD: ca có báo động đầu ở hoặc sau mốc | N-Sigma: ca có báo động đầu ở hoặc sau mốc |
|---|---|---|---|
| auth / cpu | {{a0359}} | {{a0360}} | {{a0361}} |
| auth / delay | {{a0362}} | {{a0363}} | {{a0364}} |
| order / disk | {{a0365}} | {{a0366}} | {{a0367}} |
| order / loss | {{a0368}} | {{a0369}} | {{a0370}} |
| route / mem | {{a0371}} | {{a0372}} | {{a0373}} |
| route / socket | {{a0374}} | {{a0375}} | {{a0376}} |
| train / cpu | {{a0377}} | {{a0378}} | {{a0379}} |
| train / delay | {{a0380}} | {{a0381}} | {{a0382}} |
| travel / disk | {{a0383}} | {{a0384}} | {{a0385}} |
| travel / loss | {{a0386}} | {{a0387}} | {{a0388}} |

**Độ nhạy theo điểm cuối D** (T-033; không chấm lại): số ca BOCPD có ít nhất một điểm đổi trong D giây sau mốc là {{k7.d30}}, {{k7.d60}}, {{k7.d120}}, {{k7.d300}}, {{k7.d600}} trên {{bl.det.bocpd.n}} ca, với D lần lượt `30`, `60`, `120`, `300`, `600`. D không phải thời điểm hết lỗi.

### 2.6 Chế độ (b): xếp hạng tại báo động đầu, và bảng điểm chạy

| Ghép | Ca có báo động đầu đúng | Thành công chung Hit@1 | Thành công chung Hit@5 | Hit@1 khi chạy tại mốc tiêm | Hit@1 tại báo động đầu sau mốc | Hit@1 tại báo động đầu |
|---|---|---|---|---|---|---|
| BARO + BOCPD | {{a0389}}/{{a0390}} | {{a0391:.3f}} | {{a0392:.3f}} | {{a0393:.3f}} | {{a0394:.3f}} | {{a0395:.3f}} |
| BARO + N-Sigma | {{a0396}}/{{a0397}} | {{a0398:.3f}} | {{a0399:.3f}} | {{a0400:.3f}} | {{a0401:.3f}} | {{a0402:.3f}} |
| CIRCA + BOCPD | {{a0403}}/{{a0404}} | {{a0405:.3f}} | {{a0406:.3f}} | {{a0407:.3f}} | {{a0408:.3f}} | {{a0409:.3f}} |
| CIRCA + N-Sigma | {{a0410}}/{{a0411}} | {{a0412:.3f}} | {{a0413:.3f}} | {{a0414:.3f}} | {{a0415:.3f}} | {{a0416:.3f}} |
| TORAI B + BOCPD | {{a0417}}/{{a0418}} | {{a0419:.3f}} | {{a0420:.3f}} | {{a0421:.3f}} | {{a0422:.3f}} | {{a0423:.3f}} |
| TORAI B + N-Sigma | {{a0424}}/{{a0425}} | {{a0426:.3f}} | {{a0427:.3f}} | {{a0428:.3f}} | {{a0429:.3f}} | {{a0430:.3f}} |

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

| Dataset | Đơn vị thời lượng | Ngưỡng chọn đặc trưng | Số ca (mẫu số) | Trạng thái | Ca hạng 1, bi quan | Ca hạng 1, kỳ vọng khi hòa | Ca hạng 1, lạc quan | Ca root nhận điểm mặc định |
|---|---|---|---|---|---|---|---|---|
| Nezha-OB | ms | {{a0433:.0f}} | {{a0434}} | OK: {{a0431}}, NO_EVIDENCE: {{a0432}} | {{a0435}} | {{a0436:.3g}} | {{a0437}} | {{a0438}} |
| Nezha-OB | ms | {{a0441:.0f}} | {{a0442}} | OK: {{a0439}}, NO_EVIDENCE: {{a0440}} | {{a0443}} | {{a0444:.3g}} | {{a0445}} | {{a0446}} |
| Nezha-OB | us | {{a0449:.0f}} | {{a0450}} | OK: {{a0447}}, NO_EVIDENCE: {{a0448}} | {{a0451}} | {{a0452:.3g}} | {{a0453}} | {{a0454}} |
| Nezha-OB | us | {{a0457:.0f}} | {{a0458}} | OK: {{a0455}}, NO_EVIDENCE: {{a0456}} | {{a0459}} | {{a0460:.3g}} | {{a0461}} | {{a0462}} |
| RE2-TT | ms | {{a0465:.0f}} | {{a0466}} | OK: {{a0463}}, NO_EVIDENCE: {{a0464}} | {{a0467}} | {{a0468:.3g}} | {{a0469}} | {{a0470}} |
| RE2-TT | ms | {{a0473:.0f}} | {{a0474}} | OK: {{a0471}}, NO_EVIDENCE: {{a0472}} | {{a0475}} | {{a0476:.3g}} | {{a0477}} | {{a0478}} |
| RE2-TT | us | {{a0481:.0f}} | {{a0482}} | OK: {{a0479}}, NO_EVIDENCE: {{a0480}} | {{a0483}} | {{a0484:.3g}} | {{a0485}} | {{a0486}} |
| RE2-TT | us | {{a0489:.0f}} | {{a0490}} | OK: {{a0487}}, NO_EVIDENCE: {{a0488}} | {{a0491}} | {{a0492:.3g}} | {{a0493}} | {{a0494}} |

Để đặt cạnh, trên cùng mẫu số: BARO ở Nezha-OB đúng {{bl.nz.baro.h1n:.3g}} ca kỳ vọng; TORAI B ở RE2-TT đúng {{bl.re2.torai_B.h1n:.3g}} ca kỳ vọng. Các số của nhánh này lấy từ đầu ra đã lưu của gói bổ sung T-032; không chọn ngưỡng theo điểm dev. Đây là dev đã nhìn, chưa có khoảng tin cậy.

**MicroRank với bộ chia theo công thức của bài gốc.** Chỉ thay bước chia trace; span đầu của yêu cầu do ta quy ước. Không phải MicroRank gốc.

| Dataset | Nhánh bộ chia | Số ca | Ca xét được | Ca hạng 1, bản thư viện (trên các ca xét được) | Ca hạng 1, sau khi thay bộ chia |
|---|---|---|---|---|---|
| RE2-TT | `mo15`: luật của bài | {{a0495}} | {{a0496}} | {{a0497}} | {{a0498}} |
| RE2-TT | `mo1p50`: luật chia nhóm trong mã của tác giả | {{a0499}} | {{a0500}} | {{a0501}} | {{a0502}} |
| Nezha-OB | `mo15`: luật của bài | {{a0503}} | {{a0504}} | {{a0505}} | {{a0506}} |
| Nezha-OB | `mo1p50`: luật chia nhóm trong mã của tác giả | {{a0507}} | {{a0508}} | {{a0509}} | {{a0510}} |

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

| Mã | Hạn chế | Chế độ | Mức cao nhất | Loại nguồn | Trạng thái của câu “vì sao” | Mã gốc |
|---|---|---|---|---|---|---|
| G2-H01 | MicroRank (bản RCAEval): bước chia trace bất thường/bình thường | (a) | CT | A | Đã xác lập; Chưa phân xử | H1, T-032:KT1 |
| G2-H02 | MicroRank: đếm phủ của spectrum và trọng số PageRank | (a) | CT | M | Đã xác lập; Chưa phân xử | H2, H3, T-032:KT3 |
| G2-H03 | TraceRCA (bản RCAEval): thời gian chờ root được chấm thành bất thường của dịch vụ gọi | (a) | CT | A | Đã xác lập | H4, T-032:KT2, T-032:KT13 |
| G2-H04 | TraceRCA (bản RCAEval): điểm đi theo số span mang cờ tuyệt đối | (a) | CT | A | Đã xác lập; Đã loại | H5, T-032:KT4 |
| G2-H05 | TraceRCA cài theo lời văn của bài: dịch vụ gọi hoặc frontend đứng trên root | (a) | CT | M + A | Đã xác lập; Đã loại; Chưa phân xử | H6, T-032:KT11 |
| G2-H06 | Trễ mạng: dấu hiệu nằm ở span phía gọi của lời gọi tới root | (a) | CT | M + D | Đã xác lập; Chưa phân xử | H7, M6, T-032:KT5 |
| G2-H07 | Lỗi return ở Nezha-OB: root không hạng 1 dù có dấu hiệu | (a) | LĐ | M + A + D | Đã loại; Chưa phân xử | H8 |
| G2-H08 | SimpleRCA: phiếu metric đếm theo mẫu lấn át trace và log | (a) | CT | A + M | Đã xác lập | H9 |
| G2-H09 | BARO: chia cho IQR của nền gần phẳng | (a) | CT | M | Đã xác lập; Đã loại; Chưa phân xử | H10, T-032:KT12 |
| G2-H10 | Kênh bộ nhớ trôi ngay trong đoạn nền | (a) | MT | D + M | Chưa phân xử | H11 |
| G2-H11 | Thực thể đứng trên root phần lớn nằm ngoài chuỗi gọi qua root | (a) | MT | D | Chưa phân xử | H12, T-032:KT6 |
| G2-H12 | CIRCA: phần dư gần bằng không cho điểm cực lớn, bước DA cộng nó sang tổ tiên | (a) | CT | M | Đã xác lập; Chưa phân xử | H13, H14, M4, T-032:KT15 |
| G2-H13 | CIRCA: hồi quy theo nút cha làm điểm cao hơn bản không cạnh; nhạy với cửa sổ | (a) | CT | M + G | Đã xác lập; Đã loại; Chưa phân xử | H15, T-032:KT9 |
| G2-H14 | TORAI nguồn B: bảng log do ta dựng dồn điểm về vài dịch vụ | (a) | CT | A | Đã xác lập | H16, T-032:KT7 |
| G2-H15 | TORAI: bước nhân quả (RCD) không quyết định vị trí root | (a) | MT | A | Chưa phân xử | H17 |
| G2-H16 | Rào cản tập ứng viên, hòa cắt biên và ca dừng lỗi vì thao tác thiếu nền | (a) | CT | D + G | Đã xác lập | M1, M2, M3, D4, T-032:KT8 |
| G2-H17 | Dịch vụ phía trên đứng trước root (cờ M5) và câu “lan có đáng kể” | (a) | ĐC | M + D | Chưa phân xử | M5, T-032:KT10 |
| G2-H18 | Ca sai chưa gắn được cờ cơ chế nào (M0) | (a) | MT | chưa xếp | Chưa phân xử | M0 |
| G2-H19 | Giới hạn của dữ liệu trace và metric | (a) | ĐC | D | Đã xác lập | D1, D2, D3, D5, D6, D7 |
| G2-H20 | BOCPD: tiền xử lý trên cả bản ghi làm vị trí báo đầu phụ thuộc dữ liệu sau mốc | (b) | CT | A + G | Đã xác lập; Chưa phân xử | HP-6, T-033:K4 |
| G2-H21 | BOCPD: có báo động trước mốc; nhạy với prior; underflow số học | (b) | CT | M + A + D | Chưa phân xử; Đã loại; Đã xác lập | HP-5, HP-7, HP-8, HP-9, T-033:K3 |
| G2-H22 | N-Sigma: báo dày ngay trên đoạn nền | (b) | CT | M | Chưa phân xử; Đã xác lập | HP-1, HP-2, HP-3, HP-4, HP-14, T-033:K2 |
| G2-H23 | Đầu vào bậc thang: nhiều hàng metric lặp lại | (b) | CT | D + M | Đã xác lập; Chưa phân xử | T-033:K4 |
| G2-H24 | Nhãn proxy, thời lượng lỗi và onset chưa được xác nhận độc lập | (b) | MT | D | Chưa phân xử | HP-12, T-033:K1, T-033:K5, T-033:K7 |
| G2-H25 | Schema metric đổi theo ca và liên hệ với root | (a), (b) | LĐ | D | Chưa phân xử | HP-13 |
| G2-H26 | Chế độ (b): thành công chung bị chặn ở báo động đầu; RCA phụ thuộc điểm chạy | (b) | CT | G + M | Đã xác lập; Chưa phân xử | HP-10, HP-11 |

Không đưa vào bản đồ:

- `T-032:KT14`: Câu về độ phủ đọc tay (các đơn vị sai đã đọc; các đơn vị không chạy được ghi theo lý do); là kiểm quy trình, không phải một hạn chế.
- `T-032:KT16`: Câu về kết quả trên test; thuộc đánh giá sau khóa thiết kế (G3), đưa vào mục 6 nhóm 3.
- `T-033:K6`: Phép thử khả thi của một phép tính dùng cạnh (không phải hạn chế của baseline); dùng làm căn cứ kỹ thuật ở mục 5.

### 3.2 Từng dòng

#### G2-H01 — MicroRank (bản RCAEval): bước chia trace bất thường/bình thường

- **Phương pháp; dataset; chế độ:** MicroRank, bản trong RCAEval đã sửa đầu vào; RE2-TT, Nezha-OB; (a).
- **Mã gốc:** H1, T-032:KT1.
- **Hiện tượng:** Root hiếm khi đứng hạng 1. Luật “trace bất thường khi có bất kỳ span nào vượt nền cộng ba lần độ lệch chuẩn” xếp khoảng một nửa trace vào nhóm bất thường.
- **Số:** Hạng 1: {{t28.re2.microrank_full.dung}}/{{t28.re2.microrank_full.n}} ca RE2-TT ({{t28.re2.microrank_full.khongok}} ca ERROR) và {{t28.nz.microrank_full.dung}}/{{t28.nz.microrank_full.n}} ca Nezha-OB. Thay riêng bước chia bằng công thức của bài gốc (hai biến thể `mo15` và `mo1p50`): hạng 1 từ {{h1.mo15.native}} lên {{h1.mo15.hit1}}–{{h1.mo1p50.hit1}} trên {{h1.mo15.evaluable}} ca xét được; {{h1.mo1p50.gone}}–{{h1.mo15.gone}}/{{h1.mo15.pairs}} cặp (thực thể đứng trên root, root) mất. Tỷ lệ trace bất thường ở RE2-TT (trung vị): {{h1.share.native:pct0}} xuống {{h1.share.mo15:pct0}}. Mốc giả không có lỗi: vẫn {{h1.fake.median:pct1}} trace bị xếp bất thường (trung vị {{h1.fake.n}} ca RE2-TT).
- **Vì sao:** Đã xác lập ở mức CT: bước chia của bản thư viện là bước làm mất thông tin “trace nào thật sự chậm”. Chưa phân xử phần còn lại sau khi thay bộ chia.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: phép đổi bộ chia trace (T-032, KQ11 mục 4) — CT; mốc giả cùng độ dài cửa sổ (T-032, KQ13 mục 1) — LĐ.
- **Loại nguồn hạn chế:** A.
- **Giải thích khác còn lại:** Bộ chia thay thế dùng quy ước span đầu của ta, nghĩ ra sau khi xem dev; không phải MicroRank gốc. Sau khi thay vẫn còn hơn một nửa số ca chưa hạng 1 (xem G2-H02).
- **Tác giả có nêu không:** Không áp dụng: bài gốc chia theo thời gian của cả yêu cầu, không theo từng span.
- **Ảnh hưởng tới:** RQ1, RQ2.
- **Số ca theo ô:** Phụ lục A, các bảng RE2-TT / MicroRank; Nezha-OB / MicroRank.

#### G2-H02 — MicroRank: đếm phủ của spectrum và trọng số PageRank

- **Phương pháp; dataset; chế độ:** MicroRank, bản trong RCAEval đã sửa đầu vào; RE2-TT, Nezha-OB; (a).
- **Mã gốc:** H2, H3, T-032:KT3.
- **Hiện tượng:** Một thao tác được tính cho mọi trace bất thường chứa nó; trọng số PageRank theo nhóm trace nhân vào spectrum.
- **Số:** Đếm riêng thay đếm phủ: hạng 1 từ {{h2.c1.native}} lên {{h2.c1.hit1}} trên {{h2.c1.n}} ca; {{h2.c1.gone}}/{{h2.c1.pairs}} cặp mất; {{h2.c1.down}} ca root giảm hạng. Trọng số đơn vị: hạng 1 từ {{h2.w.native}} lên {{h2.w.hit1}}; {{h2.w.gone}}/{{h2.w.pairs}} cặp mất; {{h2.w.up}} ca tăng hạng, {{h2.w.down}} ca giảm.
- **Vì sao:** Đã xác lập ở mức CT rằng mỗi bước có tác động lên hạng. Chưa phân xử tác dụng của trọng số khi nhóm trace đổi: gói bổ sung cho thấy đổi trọng số có lúc giúp, có lúc làm kém, tùy phân nhóm.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: phép đổi M-C1 và A′ (T-032, KQ9 mục 2) — CT; đối chứng trọng số × số đếm trên support chung (gói bổ sung, KT3) — CT.
- **Loại nguồn hạn chế:** M.
- **Giải thích khác còn lại:** Hai phép đổi chạy trên nhóm trace của bản thư viện (G2-H01), nên không cộng được với phép đổi bộ chia. Không có căn cứ cho quy tắc chung “bỏ trọng số là sửa được”.
- **Tác giả có nêu không:** Không nêu.
- **Ảnh hưởng tới:** RQ1, RQ2.
- **Số ca theo ô:** Phụ lục A, các bảng RE2-TT / MicroRank; Nezha-OB / MicroRank.

#### G2-H03 — TraceRCA (bản RCAEval): thời gian chờ root được chấm thành bất thường của dịch vụ gọi

- **Phương pháp; dataset; chế độ:** TraceRCA, bản trong RCAEval có lọc giá trị không hữu hạn; RE2-TT, Nezha-OB; (a).
- **Mã gốc:** H4, T-032:KT2, T-032:KT13.
- **Hiện tượng:** Span của dịch vụ gọi bao lời gọi tới root; khi lời gọi đó chậm, span của dịch vụ gọi vượt ngưỡng và cờ được tính cho dịch vụ gọi.
- **Số:** Trong các cặp (dịch vụ phía trên đứng trên root) xét được, từ một nửa span mang cờ trở lên là span bao lời gọi chậm tới root: {{h4.re2.wait}}/{{h4.re2.n}} cặp RE2-TT, {{h4.nz.wait}}/{{h4.nz.n}} cặp Nezha-OB. Ở ca **đúng** của RE2-TT cũng vậy: {{h4.right.wait}}/{{h4.right.n}} dịch vụ phía trên. Đổi cờ sang phần span không do span con phủ: số ca có dịch vụ gọi trên root {{h4.td.re2.before}} → {{h4.td.re2.after}} (RE2-TT), {{h4.td.nz.before}} → {{h4.td.nz.after}} (Nezha-OB). Mốc giả so mốc thật: tỷ lệ span mang cờ ở thao tác phía trên root {{h4.up.fake:pct1}} → {{h4.up.real:pct1}}; ở thao tác không liên hệ {{h4.unrel.fake:pct1}} → {{h4.unrel.real:pct1}}.
- **Vì sao:** Đã xác lập ở mức CT (RE2-TT) và ĐC (hai dataset) cho chuỗi: lời gọi tới root chậm → span bao nó mang cờ → dịch vụ gọi được điểm. Hiện tượng có cả ở ca đúng, nên riêng nó không phân biệt ca sai.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: phép đổi T-D (T-032, KQ9 mục 3) — CT; bảng nối lời gọi chậm với span mang cờ (KQ11 mục 2.1) — ĐC; mốc giả theo thao tác (KQ13 mục 2) — LĐ.
- **Loại nguồn hạn chế:** A.
- **Giải thích khác còn lại:** Ở RE2-TT phải giả định công cụ ghi span, vì dataset không công bố. Phần chậm nằm ngoài span của root (đường truyền, hàng đợi, xử lý phía gọi) không tách được: mỗi lời gọi chỉ có hai span.
- **Tác giả có nêu không:** Có nêu, và bài gốc có bước xử lý; bản thư viện bỏ bước đó.
- **Ảnh hưởng tới:** RQ2, RQ3.
- **Số ca theo ô:** Phụ lục A, các bảng RE2-TT / TraceRCA; Nezha-OB / TraceRCA.

#### G2-H04 — TraceRCA (bản RCAEval): điểm đi theo số span mang cờ tuyệt đối

- **Phương pháp; dataset; chế độ:** TraceRCA, bản trong RCAEval; RE2-TT, Nezha-OB; (a).
- **Mã gốc:** H5, T-032:KT4.
- **Hiện tượng:** Điểm `2a/(n + H)` lớn khi thao tác có nhiều span; thao tác của root ít span hơn thao tác của dịch vụ khác.
- **Số:** Xếp theo tỷ lệ a/n: {{h5.re2.tr1.gone}}/{{h5.re2.pairs}} cặp RE2-TT và {{h5.nz.tr1.gone}}/{{h5.nz.pairs}} cặp Nezha-OB mất, nhưng {{h5.re2.right.lose}}/{{h5.re2.right}} ca đang đúng của RE2-TT mất hạng 1. Xếp theo số tuyệt đối a: giữ {{h5.re2.ts.still}}/{{h5.re2.pairs}} và {{h5.nz.ts.still}}/{{h5.nz.pairs}} cặp.
- **Vì sao:** Đã xác lập ở mức CT rằng thứ hạng gần như theo số tuyệt đối. Đã loại “đổi sang tỷ lệ” như một cách chữa: nó làm hỏng nhiều ca đúng.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: phép đổi công thức điểm T-R (T-032, KQ11 mục 8) — CT.
- **Loại nguồn hạn chế:** A.
- **Giải thích khác còn lại:** Mức cờ tự nhiên của thao tác đông span ngay khi không có lỗi cũng tạo khối lượng; công thức không tách được tỷ lệ với khối lượng.
- **Tác giả có nêu không:** Không áp dụng: bài gốc đếm trace, không đếm span.
- **Ảnh hưởng tới:** RQ2.
- **Số ca theo ô:** Phụ lục A, các bảng RE2-TT / TraceRCA; Nezha-OB / TraceRCA.

#### G2-H05 — TraceRCA cài theo lời văn của bài: dịch vụ gọi hoặc frontend đứng trên root

- **Phương pháp; dataset; chế độ:** Bước xếp hạng của bài TraceRCA, do ta cài theo lời văn (chẩn đoán); đối chiếu mã tác giả nhánh chỉ độ trễ (chẩn đoán); RE2-TT, Nezha-OB; (a).
- **Mã gốc:** H6, T-032:KT11.
- **Hiện tượng:** Ở các cặp “chủ yếu là chờ root”, bản cài theo lời văn không đưa root lên trên dịch vụ gọi; mã tác giả (nhánh chỉ độ trễ) thì đưa root lên ở phần lớn cặp.
- **Số:** {{h6.pairs}} cặp thuộc {{h6.cases}} ca; {{h6.oldpairs}} cặp có quan hệ cũ. Mã tác giả, ngưỡng chọn đặc trưng bằng một: root trên {{h6.author.re2.t1.above}}/{{h6.author.re2.t1.pairs}} cặp RE2-TT (trong đó {{h6.author.re2.t1.above_with_caller_fallback}} do dịch vụ gọi nhận điểm mặc định) và {{h6.author.nz.t1.above}}/{{h6.author.nz.t1.pairs}} cặp Nezha-OB. **Phép E1** (chỉ đổi quy tắc pattern, giữ mọi thứ khác của bản cài theo lời văn): ở cờ một lần độ lệch chuẩn, {{e1.top.nz.flip}}/{{e1.top.nz.phen}} cặp Nezha-OB có hiện tượng đổi chiều và {{e1.top.re2.flip}}/{{e1.top.re2.phen}} cặp RE2-TT; ở cờ ba lần, {{e1.top3.nz.flip}}/{{e1.top3.nz.phen}} cặp Nezha-OB và {{e1.top3.re2.flip}}/{{e1.top3.re2.phen}} cặp RE2-TT.
- **Vì sao:** Đã xác lập ở mức CT rằng việc chấm qua tập nhiều dịch vụ có đóng góp: ở cờ một lần độ lệch chuẩn (mặc định của bài) nó là bước quyết định ở {{e1.top.nz.flip}} cặp Nezha-OB (ca đã nhìn trước, không suy rộng) và ở cờ ba lần ở phần lớn cặp Nezha-OB. Đã loại nó như giải thích đủ ở cờ một lần: ở {{e1.top.nz.unch_both}} cặp điểm dịch vụ gọi giảm mà chưa đảo chiều; ở {{e1.top.nz.rootnone}} cặp Nezha-OB và các cặp RE2-TT root không có tập được chấm nên điểm và quan hệ giữ nguyên. Chưa phân xử bước gây chênh giữa hai pipeline ở cờ một lần; trung gian của E1 chỉ ra hai ứng viên: frontend mang cờ lời gọi đi ra ở gần như mọi trace bất thường, và ở RE2-TT tập chỉ gồm root bị bước chọn tập theo điểm loại.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: phép E1 của T-034 (hai-phep-kiem.md) — CT; đối chiếu các cặp với mã tác giả (bản đính chính ngày 13/10) — MT; đọc bài và mã (thiết kế E1 mục 2) — MT.
- **Loại nguồn hạn chế:** M + A.
- **Giải thích khác còn lại:** Hai pipeline còn khác ở cách dựng lời gọi, chọn đặc trưng theo cặp, chuẩn nền và cách chọn tập; E1 không đụng tới các bước đó. Cả hai chỉ dùng một đặc trưng (độ trễ) và nền ngắn. Suy rộng cũ “trị tuyệt đối không mang hướng nên phải giữ dấu” đã rút (WHY-47, đính chính ngày 13/10).
- **Tác giả có nêu không:** Nêu một phần: bài tự ghi giới hạn khi bất thường lan cả hai chiều. Lời văn của bài chấm qua mọi tập; mã tác giả chỉ chấm tập một dịch vụ.
- **Ảnh hưởng tới:** RQ2, RQ3.
- **Số ca theo ô:** Phụ lục A, các bảng RE2-TT / TraceRCA; Nezha-OB / TraceRCA.

#### G2-H06 — Trễ mạng: dấu hiệu nằm ở span phía gọi của lời gọi tới root

- **Phương pháp; dataset; chế độ:** BARO, SimpleRCA, TraceRCA (bản RCAEval); Nezha-OB (network_delay); RE2-TT để đối chiếu; (a).
- **Mã gốc:** H7, M6, T-032:KT5.
- **Hiện tượng:** Với lỗi trễ mạng, span của chính root ít vượt ngưỡng; span phía gọi của lời gọi tới root thì vượt. Cách tính theo dịch vụ sở hữu span chấm dịch vụ gọi.
- **Số:** Nezha-OB, {{h7.nd.n}} ca trễ mạng: root đứng đầu theo span của mình ở {{h7.nd.own}} ca, theo span phía gọi ở {{h7.nd.in}} ca; BARO, SimpleRCA, TraceRCA xếp root hạng 1 ở {{h7.nd.baro}}, {{h7.nd.simplerca}}, {{h7.nd.tracerca}} ca. Phần span không do span con phủ tách được root ở {{h7.re2.ownu}}/{{h7.re2.n}} ca RE2-TT (theo thời lượng cả span: {{h7.re2.ownd}}/{{h7.re2.n}}) và {{h7.nz.ownu}}/{{h7.nz.n}} ca Nezha-OB. Span phía gọi của lời gọi tới root: {{h7.re2.inu}}/{{h7.re2.inn}} ca RE2-TT, {{h7.nz.inu}}/{{h7.nz.inn}} ca Nezha-OB.
- **Vì sao:** Đã xác lập ở mức ĐC **nơi có dấu hiệu** trong trace (đo trực tiếp theo vị trí, có mốc giả đối chứng). Chưa phân xử vì sao mỗi phương pháp xếp sai ở từng ca: mới là quan sát đặt cạnh thứ hạng. Mức CT của dòng chỉ thuộc phép thử gán tín hiệu theo cạnh (đổi cạnh thì đổi điểm, ở mức tính toán).
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: bảng vị trí tín hiệu của root (T-032, KQ10 mục 3) — ĐC; mốc giả lùi vào nền (KQ10 mục 3) — LĐ; phép thử gán tín hiệu theo cạnh (gói bổ sung, KT5) — CT.
- **Loại nguồn hạn chế:** M + D.
- **Giải thích khác còn lại:** Cờ M6 của T-028 (root thiếu bằng chứng cục bộ dương theo luật riêng của từng phương pháp) có ở trễ mạng trên Nezha-OB: SimpleRCA {{t28.nz.simplerca.M6}} ca, MicroRank {{t28.nz.microrank_full.M6}} ca, TraceRCA {{t28.nz.tracerca.M6}} ca; không có ở lỗi return. M6 không đồng nghĩa root không hạng 1 hay thiếu mọi tín hiệu. “Root đứng đầu theo một vị trí” không phải Hit@1 của một phương pháp. Định nghĩa vị trí đặt sau khi xem dev. Ở Nezha-OB một phần span có span con chạy chồng nhau, phép trừ phải xử lý chồng lấn.
- **Tác giả có nêu không:** Nêu một phần.
- **Ảnh hưởng tới:** RQ2, RQ3.
- **Số ca theo ô:** Phụ lục A, các bảng Nezha-OB / BARO; Nezha-OB / SimpleRCA; Nezha-OB / TraceRCA.

#### G2-H07 — Lỗi return ở Nezha-OB: root không hạng 1 dù có dấu hiệu

- **Phương pháp; dataset; chế độ:** BARO, SimpleRCA, TraceRCA, MicroRank; Nezha-OB (return); (a).
- **Mã gốc:** H8.
- **Hiện tượng:** Root không đứng hạng 1 dưới các cách chấm đã xét, trong khi log lỗi tại root tăng và tỷ lệ thành công ở frontend giảm.
- **Số:** {{h8.n}} ca return; BARO, SimpleRCA, TraceRCA xếp root hạng 1 ở {{h8.baro}}, {{h8.simplerca}}, {{h8.tracerca}} ca; ở {{h8.norank}} ca root cũng không đứng đầu theo vị trí trace nào. Số dòng log khớp từ khóa lỗi tại root (cửa sổ giả → sớm → muộn sau mốc): {{h8.log.0.placebo}} → {{h8.log.0.early}} → {{h8.log.0.late}}; {{h8.log.1.placebo}} → {{h8.log.1.early}} → {{h8.log.1.late}}; {{h8.log.2.placebo}} → {{h8.log.2.early}} → {{h8.log.2.late}}; {{h8.log.3.placebo}} → {{h8.log.3.early}} → {{h8.log.3.late}}.
- **Vì sao:** Đã loại ở mức LĐ giải thích “dữ liệu không có đáp ứng do lỗi”. Chưa phân xử cách dùng dấu hiệu nào định vị được root: SimpleRCA chỉ đếm giá trị tăng, BARO bỏ cột hằng ở nền, log chỉ cho một phiếu.
- **Mức bằng chứng cao nhất:** LĐ (liên hệ có đối chứng). Nguồn con: cửa sổ đối xứng trước và sau mốc cho log và tỷ lệ thành công (gói bổ sung, đính chính mục 5) — LĐ; đọc mã SimpleRCA và adapter BARO — MT.
- **Loại nguồn hạn chế:** M + A + D.
- **Giải thích khác còn lại:** Số dòng log không phải số yêu cầu lỗi. Hai ca root là checkoutservice có phản ứng metric ở frontend, không ở chính root. Đáp ứng thời lượng theo từng thao tác và onset vật lý còn mở.
- **Tác giả có nêu không:** Bài MicroRank nêu giới hạn khi lỗi không đổi độ trễ; chưa xác nhận điều kiện ấy cho từng ca.
- **Ảnh hưởng tới:** RQ2.
- **Số ca theo ô:** Phụ lục A, các bảng Nezha-OB / BARO; Nezha-OB / SimpleRCA; Nezha-OB / TraceRCA; Nezha-OB / MicroRank.

#### G2-H08 — SimpleRCA: phiếu metric đếm theo mẫu lấn át trace và log

- **Phương pháp; dataset; chế độ:** SimpleRCA (M4, quy ước T-017); RE2-TT, Nezha-OB; (a).
- **Mã gốc:** H9.
- **Hiện tượng:** Một cột metric vượt ngưỡng gần suốt cửa sổ cho số phiếu bằng số mẫu vượt ngưỡng; trace và log mỗi loại chỉ cho nhiều nhất một phiếu.
- **Số:** {{h9.metric}}/{{h9.pairs}} cặp do riêng phiếu metric quyết định. Đếm theo cột thay đếm theo mẫu (RE2-TT): {{h9.s1.re2.gone}}/{{h9.s1.re2.pairs}} cặp mất, nhưng số ca hạng 1 tính bi quan từ {{h9.s1.re2.native}} xuống {{h9.s1.re2.changed}} vì hòa (tính lạc quan: {{h9.s1.re2.optimistic}}).
- **Vì sao:** Đã xác lập ở mức CT. Đếm theo mẫu vừa là thứ gây sai vừa là thứ cho phương pháp khả năng phân biệt; đổi cách đếm không chữa được.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: phân rã cộng của điểm (T-032, KQ9 mục 4) — ĐC; phép đổi S-1 — CT.
- **Loại nguồn hạn chế:** A + M.
- **Giải thích khác còn lại:** Đơn vị “mỗi mẫu một phiếu” là quy ước của T-017 ở chỗ bài không khóa. Điểm tăng theo số cột và độ dài cửa sổ (WHY-17).
- **Tác giả có nêu không:** Nêu một phần.
- **Ảnh hưởng tới:** RQ1, RQ2.
- **Số ca theo ô:** Phụ lục A, các bảng RE2-TT / SimpleRCA; Nezha-OB / SimpleRCA.

#### G2-H09 — BARO: chia cho IQR của nền gần phẳng

- **Phương pháp; dataset; chế độ:** BARO; RE2-TT (kết luận); Nezha-OB (không kết luận); (a).
- **Mã gốc:** H10, T-032:KT12.
- **Hiện tượng:** Cột của dịch vụ khác gần phẳng ở đoạn nền; thay đổi nhỏ sau mốc thành điểm lớn.
- **Số:** RE2-TT, đổi sang thang độ lệch chuẩn: {{h10.gone}}/{{h10.pairs}} cặp mất; hạng 1 từ {{h10.native}} lên {{h10.changed}}; {{h10.lose}} ca đúng bị hỏng. Nezha-OB: {{h10.nz.native}} → {{h10.nz.changed}}, {{h10.nz.lose}} ca đúng bị hỏng. Không lọc cột hằng: hạng root không đổi ở {{h10.b1.same}}/{{h10.b1.n}} ca.
- **Vì sao:** Đã xác lập ở mức CT cho RE2-TT. Đã loại việc lọc cột hằng như nguyên nhân làm root mất hạng dưới quy tắc chấm hiện tại; bước lọc có bỏ cột của root ở {{h10.b1.added}}/{{h10.b1.n}} ca, nhưng hạng của root không đổi ở ca nào. Đổi thang đưa root lên hạng 1 ở {{h10.re2.fixed}}/{{h10.re2.wrong}} ca sai RE2-TT và {{h10.nz.fixed}}/{{h10.nz.wrong}} ca sai Nezha-OB, nên thang IQR không giải thích hết các ca sai của BARO. Chưa phân xử các cặp còn lại: cột của dịch vụ khác đổi thật tại mốc, nguyên nhân vật lý không phân xử được bằng dữ liệu hiện có.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: phép đổi B-2 và B-1 (T-032, KQ9 mục 5) — CT; chuỗi cột độ trễ ở ba cặp ca cùng ô (KQ13 mục 3) — MT.
- **Loại nguồn hạn chế:** M.
- **Giải thích khác còn lại:** Ở Nezha-OB mỗi phía chỉ có vài mẫu metric (mã D1 của T-032), IQR kém ổn định; phép đổi thang không kết luận được. Phép đổi nghĩ ra sau khi xem dev.
- **Tác giả có nêu không:** Không nêu.
- **Ảnh hưởng tới:** RQ1, RQ2.
- **Số ca theo ô:** Phụ lục A, các bảng RE2-TT / BARO; Nezha-OB / BARO.

#### G2-H10 — Kênh bộ nhớ trôi ngay trong đoạn nền

- **Phương pháp; dataset; chế độ:** BARO, SimpleRCA; RE2-TT; (a).
- **Mã gốc:** H11.
- **Hiện tượng:** Cột bộ nhớ của dịch vụ không liên quan trôi gần tuyến tính ở nền; chuẩn hóa theo độ biến thiên nền cho nó điểm cao.
- **Số:** Trong {{h11.memall}} cột bộ nhớ thắng root ở BARO, {{h11.mem}} cột thuộc nhóm trôi nền.
- **Vì sao:** Chưa phân xử, vì mới là mô tả có phân nhóm; nhóm trôi nền chỉ giải thích một phần số cột thắng.
- **Mức bằng chứng cao nhất:** MT (mô tả). Nguồn con: bảng xu hướng nền của cột metric (T-032, KQ10 mục 4) — MT.
- **Loại nguồn hạn chế:** D + M.
- **Giải thích khác còn lại:** Một phần cột bộ nhớ có bậc tại mốc; phần còn lại không thuộc nhóm nào. Mốc chia nhóm đặt trước nhưng bảng dựng sau khi xem dev.
- **Tác giả có nêu không:** Không nêu.
- **Ảnh hưởng tới:** RQ2.
- **Số ca theo ô:** Phụ lục A, các bảng RE2-TT / BARO; RE2-TT / SimpleRCA.

#### G2-H11 — Thực thể đứng trên root phần lớn nằm ngoài chuỗi gọi qua root

- **Phương pháp; dataset; chế độ:** BARO (kênh metric); RE2-TT; (a).
- **Mã gốc:** H12, T-032:KT6.
- **Hiện tượng:** Metric của dịch vụ không liên hệ với root đổi tại mốc; quan hệ gọi tới root không mang thông tin về chúng.
- **Số:** Trong {{h12.pairs}} cặp của BARO: {{h12.nospan}} không có span, {{h12.roi}} rời chuỗi gọi, {{h12.chung}} chỉ chung phía trên; chỉ {{h12.up.latency}} cặp là dịch vụ phía trên thắng bằng cột độ trễ.
- **Vì sao:** Chưa phân xử, vì dữ liệu không có ánh xạ dịch vụ–máy, metric mức máy hay nhật ký của bộ tiêm lỗi; không tách được “cùng máy”, “cùng tải” với quan hệ ẩn.
- **Mức bằng chứng cao nhất:** MT (mô tả). Nguồn con: bảng vị trí trên chuỗi gọi (T-032, KQ11 mục 1, 3) — MT.
- **Loại nguồn hạn chế:** D.
- **Giải thích khác còn lại:** Cùng máy hoặc cùng tài nguyên; tải đổi theo lỗi; bộ tiêm tác động rộng hơn nhãn; quan hệ dữ liệu hoặc thông điệp không hiện trong trace.
- **Tác giả có nêu không:** Không áp dụng.
- **Ảnh hưởng tới:** RQ2, RQ5.
- **Số ca theo ô:** Phụ lục A, các bảng RE2-TT / BARO; Nezha-OB / BARO.

#### G2-H12 — CIRCA: phần dư gần bằng không cho điểm cực lớn, bước DA cộng nó sang tổ tiên

- **Phương pháp; dataset; chế độ:** CIRCA (đồ thị kiến trúc, OLS+RHT+DA); RE2-TT; (a).
- **Mã gốc:** H13, H14, M4, T-032:KT15.
- **Hiện tượng:** Một cột đứng yên ở đoạn học rồi đổi ở đoạn chấm; hồi quy theo nút cha cho phần dư học gần bằng không và điểm cực lớn (vượt ngưỡng báo riêng của Q-82); bước DA cộng điểm đó sang nút khác khi điểm vượt ngưỡng.
- **Số:** {{h13.huge}}/{{h13.n}} ca có nút điểm cực lớn. Trong {{h13.huge}} ca đó, số ca root hạng 1: bản có DA {{h13.da}}; bản có cạnh nhưng không DA {{h13.rht}}; bỏ mọi cạnh {{h13.k2}}, và còn {{h13.hugek2}} nút cực lớn. Ở {{h13.clean.n}} ca còn lại: bản có DA {{h13.clean.da}}; bản có cạnh nhưng không DA {{h13.clean.native}}; bỏ mọi cạnh {{h13.clean.k2}}.
- **Vì sao:** Đã xác lập ở mức CT hai bước, trên cùng điểm đầu vào: (i) hồi quy theo nút cha tạo điểm cực lớn, và root đã không hạng 1 trước DA ở mọi ca của nhóm (hạng 1: {{h13.rht}}/{{h13.huge}} ca); (ii) DA nhận đúng các điểm đó và đổi hạng của root (trên {{h13.n}} ca: giảm {{h13.da.down}}, tăng {{h13.da.up}}, giữ {{h13.da.same}}). Bỏ mọi cạnh đổi cả hồi quy lẫn DA, không cô lập riêng bước nào. Chưa phân xử nguồn vật lý của tín hiệu và đóng góp của việc chờ.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: phép đổi K-2 bỏ cạnh (T-032, KQ10 mục 1) — CT; mô tả phần được cộng ở bước DA (KT15) — ĐC.
- **Loại nguồn hạn chế:** M.
- **Giải thích khác còn lại:** Không đọc số CIRCA thành “cấu trúc gọi giúp” hay “hại” khi chưa tách {{h13.huge}} ca này. Minh đã chốt giữ bản gốc, không sửa (Q-82).
- **Tác giả có nêu không:** H13: không nêu. H14: nêu một phần (DA cần kiểm thêm trên dữ liệu thật).
- **Ảnh hưởng tới:** RQ1, RQ2, RQ3.
- **Số ca theo ô:** Phụ lục A, các bảng RE2-TT / CIRCA.

#### G2-H13 — CIRCA: hồi quy theo nút cha làm điểm cao hơn bản không cạnh; nhạy với cửa sổ

- **Phương pháp; dataset; chế độ:** CIRCA (đồ thị kiến trúc, OLS+RHT+DA); RE2-TT; (a).
- **Mã gốc:** H15, T-032:KT9.
- **Hiện tượng:** Phần dư ở đoạn học nhỏ mà phần dư ở đoạn chấm không nhỏ theo, nên điểm có cạnh cao hơn điểm không cạnh.
- **Số:** {{h15.raise}}/{{h15.reg}} nút có hồi quy tăng điểm. Nhóm {{h15.nodes}} nút có nhiều nút cha (nhóm `at_least8_parents`), trung vị tỷ số có cạnh/không cạnh: {{h15.n111:.2f}} (đoạn học ngắn gần mốc, `native111_late`), {{h15.l291:.2f}} (đoạn học dài, `long291_late`), {{h15.e111:.2f}} (đoạn ngắn sớm, `early111_late`), {{h15.s0:.2f}} / {{h15.s1:.2f}} / {{h15.s2:.2f}} (cùng số điểm như đoạn ngắn nhưng trải đều trên đoạn dài).
- **Vì sao:** Đã xác lập phép tính và độ nhạy cửa sổ ở mức CT. Đã loại giải thích “chỉ do số điểm học ít”. Chưa phân xử giữa thành phần mẫu, độ gần đoạn chấm, pha lấy mẫu và thang phần dư.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: hai nhánh cửa sổ (T-032, KQ13 mục 6) — CT; giữ nút và cha, đổi cách lấy điểm học (gói bổ sung, KT9) — CT.
- **Loại nguồn hạn chế:** M + G.
- **Giải thích khác còn lại:** Đổi đoạn học ngắn thành đoạn dài còn đổi phân phối; lấy mẫu trải đều còn đổi pha và tần suất. Không coi “tăng số điểm học” là lời giải đã chứng minh.
- **Tác giả có nêu không:** Có nêu dạng tổng quát.
- **Ảnh hưởng tới:** RQ2.
- **Số ca theo ô:** Phụ lục A, các bảng RE2-TT / CIRCA.

#### G2-H14 — TORAI nguồn B: bảng log do ta dựng dồn điểm về vài dịch vụ

- **Phương pháp; dataset; chế độ:** TORAI (bản sửa), nguồn B tự dựng; RE2-TT; (a).
- **Mã gốc:** H16, T-032:KT7.
- **Hiện tượng:** Dòng log mang dữ liệu của từng yêu cầu bị tách thành nhiều mẫu hiếm; điểm z của log dồn về vài dịch vụ, không phụ thuộc root.
- **Số:** Bỏ nguồn log (seed 0): {{h16.fixed}}/{{h16.wrong}} ca sai thành hạng 1; {{h16.lose}} ca đúng bị hỏng.
- **Vì sao:** Đã xác lập ở mức CT. Với bảng log của tác giả (nguồn A) hiện tượng không lặp lại.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: phép đổi tl1, tl2 (T-032, KQ10 mục 8) — CT; TORAI nguồn A, mọi cột đóng góp (gói bổ sung, KT7) — ĐC.
- **Loại nguồn hạn chế:** A.
- **Giải thích khác còn lại:** Một ca có hạng root đổi theo seed. Nguồn A lệch lưới thời gian và dùng ngưỡng toàn file (WHY-29), nên không thay được nguồn B làm dòng chính mà không khai lệch.
- **Tác giả có nêu không:** Nêu một phần.
- **Ảnh hưởng tới:** RQ1.
- **Số ca theo ô:** Phụ lục A, các bảng RE2-TT / TORAI B.

#### G2-H15 — TORAI: bước nhân quả (RCD) không quyết định vị trí root

- **Phương pháp; dataset; chế độ:** TORAI (bản sửa), nguồn B; RE2-TT; (a).
- **Mã gốc:** H17.
- **Hiện tượng:** Root không bao giờ nằm trong khối do nhánh RCD xếp; vị trí của root do điểm cụm và nhánh dự phòng quyết định.
- **Số:** Trên {{h17.units}} đơn vị (ca × seed): root là cụm một dịch vụ ở {{h17.don}} đơn vị, rơi nhánh dự phòng ở {{h17.fallback}}, thuộc khối do RCD xếp ở {{h17.rcd}}.
- **Vì sao:** Chưa phân xử vai trò của đồ thị nhân quả: trên bản ghi, bước đó không tham gia xếp root, nên không rút được kết luận nào về đồ thị nhân quả từ TORAI.
- **Mức bằng chứng cao nhất:** MT (mô tả). Nguồn con: phân rã khối trên các bản ghi đóng băng (T-032, KQ9 mục 7) — MT.
- **Loại nguồn hạn chế:** A.
- **Giải thích khác còn lại:** Đây là bản đã sửa hai chỗ theo WHY-19 (lần giảm mẫu thứ hai đã bỏ), nên hiện tượng không do lỗi giảm mẫu đó. Kết luận chỉ về bước RCD; khâu dựng bảng trace của nguồn B có dùng quan hệ cha–con của span. Chưa kiểm bản tác giả đã dùng để tạo số công bố.
- **Tác giả có nêu không:** Không nêu.
- **Ảnh hưởng tới:** RQ1, RQ3.
- **Số ca theo ô:** Phụ lục A, các bảng RE2-TT / TORAI B.

#### G2-H16 — Rào cản tập ứng viên, hòa cắt biên và ca dừng lỗi vì thao tác thiếu nền

- **Phương pháp; dataset; chế độ:** TraceRCA, MicroRank (bản RCAEval); SimpleRCA; RE2-TT, Nezha-OB; (a).
- **Mã gốc:** M1, M2, M3, D4, T-032:KT8.
- **Hiện tượng:** Root nằm ngoài tập quan sát hoặc tập trả về; hòa cắt ngang biên top-k; một thao tác chỉ có sau mốc làm phương pháp dừng lỗi.
- **Số:** Ở TraceRCA trên Nezha-OB, trong {{t28.nz.tracerca.sai}} ca sai: M1 (root ngoài tập quan sát) {{t28.nz.tracerca.M1}} ca; M2 (root quan sát được nhưng không được trả về) {{t28.nz.tracerca.M2}} ca; M3 (hòa cắt biên) {{t28.nz.tracerca.M3}} ca. Các phương pháp khác: xem cột cờ ở Phụ lục A (cột chỉ hiện khi có ca mang cờ). ERROR: {{t28.re2.microrank_full.khongok}} ca RE2-TT ở MicroRank và {{t28.re2.tracerca.khongok}} ca ở TraceRCA, đang tính trượt. Bỏ thao tác thiếu nền (đổi đầu vào, chẩn đoán): TraceRCA xếp root hạng 1 ở {{d4.tracerca.hit1}}/{{t28.re2.tracerca.khongok}} ca đó.
- **Vì sao:** Đã xác lập ở mức CT rằng bốn ca ERROR là do đầu vào thiếu nền của một thao tác, không phải do cách chấm điểm. Rào cản tập (M1–M3) được kiểm trực tiếp và hiếm.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: kiểm thành viên tập (T-028) — ĐC; phép bỏ thao tác thiếu nền (T-032, KQ12 mục 2, KQ13 mục 4) — CT.
- **Loại nguồn hạn chế:** D + G.
- **Giải thích khác còn lại:** Cách ghi bốn ca ERROR là quyết định giao thức (WHY-28, WHY-31): giữ ở mẫu số, tính trượt. Đổi cách ghi làm đổi số hạng 1 của TraceRCA.
- **Tác giả có nêu không:** Chưa thấy trong nguồn đã khảo sát.
- **Ảnh hưởng tới:** RQ1.
- **Số ca theo ô:** Phụ lục A, các bảng RE2-TT / MicroRank; RE2-TT / TraceRCA; Nezha-OB / TraceRCA; Nezha-OB / SimpleRCA.

#### G2-H17 — Dịch vụ phía trên đứng trước root (cờ M5) và câu “lan có đáng kể”

- **Phương pháp; dataset; chế độ:** Cả sáu phương pháp; RE2-TT, Nezha-OB; (a).
- **Mã gốc:** M5, T-032:KT10.
- **Hiện tượng:** Ở một phần ca sai, có dịch vụ phía trên root (gọi root trực tiếp hoặc gián tiếp) chắc chắn đứng trước root.
- **Số:** Cờ M5 trên số ca sai hạng 1 (đa nhãn): TraceRCA {{t28.re2.tracerca.M5}}/{{t28.re2.tracerca.sai}} và {{t28.nz.tracerca.M5}}/{{t28.nz.tracerca.sai}}; MicroRank {{t28.re2.microrank_full.M5}}/{{t28.re2.microrank_full.sai}} và {{t28.nz.microrank_full.M5}}/{{t28.nz.microrank_full.sai}}; SimpleRCA {{t28.re2.simplerca.M5}}/{{t28.re2.simplerca.sai}} và {{t28.nz.simplerca.M5}}/{{t28.nz.simplerca.sai}}; BARO {{t28.re2.baro.M5}}/{{t28.re2.baro.sai}} và {{t28.nz.baro.M5}}/{{t28.nz.baro.sai}}; CIRCA {{t28.re2.circa_ols_da.M5}}/{{t28.re2.circa_ols_da.sai}}; TORAI B {{t28.re2.torai_B.M5}}/{{t28.re2.torai_B.sai}} (RE2-TT trước, Nezha-OB sau). Khả năng đo việc “dịch vụ gọi chờ root”: {{d.nz.ok}} ca Nezha-OB đo được có điều kiện, {{d.re2.part}} ca RE2-TT đo được một phần, {{d2.unmeasurable}} ca không đo được.
- **Vì sao:** Chưa phân xử “lan có đáng kể”, vì cờ M5 không đồng nghĩa “sai vì dịch vụ gọi”, cơ chế khác nhau theo phương pháp, và chưa có định nghĩa “đáng kể” được chọn. Xem mục 4. Mức ĐC của dòng chỉ thuộc bảng theo ca đo việc chờ ở các đơn vị có cờ M5; nó không trả lời câu “đáng kể”.
- **Mức bằng chứng cao nhất:** ĐC (đo cơ chế). Nguồn con: cờ M5 so mức nền P0 (T-028) — LĐ; bảng theo ca cho các đơn vị có cờ M5 (T-032 mục 5.3) — ĐC; mức đo được theo ca (T-032 mục 5.4) — MT.
- **Loại nguồn hạn chế:** M + D.
- **Giải thích khác còn lại:** Dịch vụ gọi tự bất thường; tác động chung qua hạ tầng; cách chấm ưu tiên dịch vụ đông lưu lượng; giá trị cực lớn qua DA (CIRCA); sai lệch cửa sổ, đồng hồ hoặc đồ thị.
- **Tác giả có nêu không:** Bài TraceRCA có mô tả hiện tượng ở phần bài học triển khai.
- **Ảnh hưởng tới:** RQ2, RQ3.
- **Số ca theo ô:** Phụ lục A, các bảng RE2-TT / BARO; RE2-TT / SimpleRCA; RE2-TT / MicroRank; RE2-TT / TraceRCA; RE2-TT / CIRCA; RE2-TT / TORAI B; Nezha-OB / BARO; Nezha-OB / SimpleRCA; Nezha-OB / MicroRank; Nezha-OB / TraceRCA.

#### G2-H18 — Ca sai chưa gắn được cờ cơ chế nào (M0)

- **Phương pháp; dataset; chế độ:** BARO, MicroRank, CIRCA, TORAI B, TraceRCA, SimpleRCA; RE2-TT, Nezha-OB; (a).
- **Mã gốc:** M0.
- **Hiện tượng:** Ca sai không có cờ M1–M6; đọc tay ở T-032 đã gắn phần lớn về các bước ở G2-H01 đến G2-H15, phần còn lại ghi là chưa rõ.
- **Số:** Nhãn chính M0 trên số ca sai hạng 1: MicroRank {{t28.re2.microrank_full.M0.primary}}/{{t28.re2.microrank_full.sai}} (RE2-TT); BARO {{t28.re2.baro.M0.primary}}/{{t28.re2.baro.sai}} và {{t28.nz.baro.M0.primary}}/{{t28.nz.baro.sai}}; CIRCA {{t28.re2.circa_ols_da.M0.primary}}/{{t28.re2.circa_ols_da.sai}}; TORAI B {{t28.re2.torai_B.M0.primary}}/{{t28.re2.torai_B.sai}}; SimpleRCA {{t28.nz.simplerca.M0.primary}}/{{t28.nz.simplerca.sai}} (Nezha-OB).
- **Vì sao:** Chưa phân xử ở mức nhóm: M0 là nhãn “chưa phân loại” của codebook T-028, không phải một cơ chế.
- **Mức bằng chứng cao nhất:** MT (mô tả). Nguồn con: bảng nhãn chính T-028 — MT; đọc tay các đơn vị sai (T-032, doc-tay.md) — MT.
- **Loại nguồn hạn chế:** chưa xếp.
- **Giải thích khác còn lại:** Nhãn chính theo thứ tự cố định M1 → M6 → M0 chỉ để trình bày, không phải nguyên nhân trội.
- **Tác giả có nêu không:** Không áp dụng.
- **Ảnh hưởng tới:** RQ2.
- **Số ca theo ô:** Phụ lục A, các bảng RE2-TT / BARO; RE2-TT / MicroRank; RE2-TT / CIRCA; RE2-TT / TORAI B; RE2-TT / TraceRCA; Nezha-OB / BARO; Nezha-OB / SimpleRCA; Nezha-OB / MicroRank; Nezha-OB / TraceRCA.

#### G2-H19 — Giới hạn của dữ liệu trace và metric

- **Phương pháp; dataset; chế độ:** Mọi phương pháp dùng trace; CIRCA và TORAI ở Nezha-OB; RE2-TT, Nezha-OB; (a).
- **Mã gốc:** D1, D2, D3, D5, D6, D7.
- **Hiện tượng:** Nền trace ngắn và metric thưa ở Nezha-OB (D1); root không được dịch vụ nào gọi hoặc quá ít lời gọi (D2); cửa sổ dev của RE2-TT không có span mang mã lỗi (D3); một ca RE2-TT mất nhiều span cha (D5); RE2-TT không công bố phiên bản mã, công cụ ghi span, quan hệ dịch vụ–máy (D6); trace của Nezha-OB không có trường trạng thái và metric có nhịp thưa (D7).
- **Số:** Nezha-OB: {{d.nz.n}}/{{d.nz.n}} ca có nền trace ngắn và chỉ vài mẫu metric mỗi phía (mã D1 của T-032); CIRCA và TORAI B không chạy được ở {{t28.nz.circa_ols_da.khongok}}/{{t28.nz.circa_ols_da.n}} ca. {{d2.unmeasurable}}/{{d2.n}} ca không đủ lời gọi tới root: {{d2.nocaller}} ca root không được dịch vụ nào gọi trong trace, {{d2.fewcalls}} ca cạnh gọi tới root quá thưa. RE2-TT: {{d.re2.part}} ca chỉ đo được một phần vì thiếu thông tin công cụ ghi span. D5: ở ca `dev-746fd74313`, {{d5.orphan}}/{{d5.n}} trace sau mốc có span mất cha; ca này không qua cổng kiểm cây lời gọi (trường `gate/pass`: {{d5.gate}}), nên công thức chia trace của bài MicroRank không áp được ở đó.
- **Vì sao:** Đã xác lập ở mức ĐC (đo trực tiếp trên dữ liệu) rằng các thông tin này không có trong dataset; bộ thu thập không khôi phục được thứ chưa từng được ghi.
- **Mức bằng chứng cao nhất:** ĐC (đo cơ chế). Nguồn con: thẻ dataset và phép đo độ phủ (T-032 mục 3.7, 5.4) — ĐC.
- **Loại nguồn hạn chế:** D.
- **Giải thích khác còn lại:** Không áp dụng: đây là thiếu đầu vào, không phải cơ chế của phương pháp.
- **Tác giả có nêu không:** Tác giả dataset không nêu các giới hạn này trong nguồn đã khảo sát.
- **Ảnh hưởng tới:** RQ1, RQ2, RQ5.
- **Số ca theo ô:** Không tách theo ô: giới hạn áp cho cả dataset hoặc theo ca đã đếm; bảng theo ca ở `results/T-032/kha-nang-do-trace.json#/ca`.

#### G2-H20 — BOCPD: tiền xử lý trên cả bản ghi làm vị trí báo đầu phụ thuộc dữ liệu sau mốc

- **Phương pháp; dataset; chế độ:** BOCPD (bản BARO); RE2-TT; (b).
- **Mã gốc:** HP-6, T-033:K4.
- **Hiện tượng:** Bước bỏ cột hằng và chuẩn hóa min–max dùng cả bản ghi, gồm dữ liệu sau mốc.
- **Số:** Cắt dữ liệu sau mốc rồi tiền xử lý lại: báo động đầu sớm hơn ở {{hp.i1.earlier}}/{{hp.i1.n}} ca, bằng ở {{hp.i1.equal}}, muộn hơn ở {{hp.i1.later}}; tổng điểm đổi trước mốc {{hp.nv.full}} → {{hp.nv.i1}} (nhánh đổi hazard, I2: {{hp.nv.i2}}). Tiền xử lý chỉ dùng quá khứ (hai biến thể chẩn đoán): tập điểm đổi khác bản gốc ở {{k3.causal_fixed.changed}}/{{k3.causal_fixed.cases}} và {{k3.causal_expanding.changed}}/{{k3.causal_expanding.cases}} ca.
- **Vì sao:** Đã xác lập ở mức CT rằng vị trí báo động đầu phụ thuộc dữ liệu sau mốc qua tiền xử lý. Chưa phân xử vì sao có báo động trước mốc; bỏ nhìn trước không cho thấy sẽ giảm báo sai.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: can thiệp I1, I2 (T-029) — CT; biến thể tiền xử lý chỉ dùng quá khứ (T-033 gói bổ sung, K4) — CT.
- **Loại nguồn hạn chế:** A + G.
- **Giải thích khác còn lại:** Cắt sau mốc còn đổi bộ cột và số chiều của prior. Biến thể chỉ dùng quá khứ đổi cùng lúc mặt nạ cột, số chiều và thang; không cô lập riêng việc chuẩn hóa.
- **Tác giả có nêu không:** Code tiền xử lý toàn chuỗi là của tác giả; chưa thấy tác giả nêu hạn chế này.
- **Ảnh hưởng tới:** RQ1, RQ2, RQ3a.
- **Số ca theo ô:** Phụ lục B, các cột HP-6.

#### G2-H21 — BOCPD: có báo động trước mốc; nhạy với prior; underflow số học

- **Phương pháp; dataset; chế độ:** BOCPD (bản BARO); RE2-TT; (b).
- **Mã gốc:** HP-5, HP-7, HP-8, HP-9, T-033:K3.
- **Hiện tượng:** Báo động đầu nằm trước mốc tiêm ở phần lớn ca. Posterior nhạy với prior. Khối lượng của nhiều dòng dõi bị làm tròn về không.
- **Số:** Báo động đầu ở hoặc sau mốc: {{bl.det.bocpd.first_ok}}/{{bl.det.bocpd.n}} ca. Đổi prior trên cùng đầu vào: tập điểm đổi khác ở {{k3.prior_df4.changed}}/{{k3.prior_df4.cases}}, {{k3.prior_kappa4.changed}}/{{k3.prior_kappa4.cases}}, {{k3.prior_precision4.changed}}/{{k3.prior_precision4.cases}} ca (tổng điểm đổi {{k3.native.cp}} → {{k3.prior_df4.cp}}, {{k3.prior_kappa4.cp}}, {{k3.prior_precision4.cp}}). **Phép E2** (posterior trong miền log, bốn chuỗi của hai ca): MAP và điểm đổi trùng bản gốc ở {{e2.chains_equal}}/{{e2.chains}} chuỗi; ở chuỗi full của {{e2.diff.case:x}} MAP khác tại {{e2.diff.m}} điểm liên tiếp, bản gốc có {{e2.diff.cp_only_native}} điểm đổi mà phép tính trong miền log không có, và thiếu {{e2.diff.cp_only_log}} điểm đổi mà phép tính trong miền log có; tất cả nằm trong {{e2.diff.window_s}} giây đầu sau mốc.
- **Vì sao:** Chưa phân xử vì sao có báo động trước mốc: không có nền sạch và onset được xác nhận độc lập. Đã loại hazard trên miền được chấm (I2). Đã xác lập ở mức CT độ nhạy với prior. Đã xác lập ở mức CT rằng underflow làm đổi MAP và điểm đổi ở một trong bốn chuỗi đã kiểm, trong một đoạn ngắn sau mốc; đã loại underflow như giải thích cho các báo động trước mốc của hai ca đó.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: can thiệp I2 và cờ B1, B4, D0 (T-029) — CT / LĐ; ba mức prior trên cùng X, d (T-033, K3) — CT; phép E2 của T-034 (hai-phep-kiem.md) — CT.
- **Loại nguồn hạn chế:** M + A + D.
- **Giải thích khác còn lại:** Nền không sạch; biến động tải; bước nhảy telemetry (cờ B4 cũng phổ biến ở điểm không báo); hiệp phương sai và prior. Số điểm đổi không phải thước đo chất lượng. HP-5: không ca nào có cờ “đầu chuỗi thiếu dữ liệu được điền không” ở báo động đầu; điều đó không bác ảnh hưởng của thiếu dữ liệu nói chung. HP-9 (D0): ca không có cờ chính nào; thuộc nhóm chưa giải thích, không ép vào một cơ chế.
- **Tác giả có nêu không:** Chưa thấy trong nguồn đã khảo sát.
- **Ảnh hưởng tới:** RQ1, RQ2, RQ3a.
- **Số ca theo ô:** Phụ lục B, các cột HP-5, HP-7, HP-8, HP-9 (D0).

#### G2-H22 — N-Sigma: báo dày ngay trên đoạn nền

- **Phương pháp; dataset; chế độ:** N-Sigma (cấu hình đã khóa của T-025); RE2-TT; (b).
- **Mã gốc:** HP-1, HP-2, HP-3, HP-4, HP-14, T-033:K2.
- **Hiện tượng:** Báo động đầu luôn trước mốc; rất nhiều báo động trên giờ bình thường theo nhãn proxy.
- **Số:** Báo động đầu ở hoặc sau mốc: {{bl.det.nsigma.first_ok}}/{{bl.det.nsigma.n}} ca; {{bl.det.nsigma.fa:.0f}} báo động mỗi giờ bình thường theo nhãn proxy (bộ cột chính). Lịch sử trượt có độ dài cố định thay cho lịch sử mở rộng: báo động đầu sau mốc sớm hơn ở {{k2.roll.earlier}} ca, bằng {{k2.roll.equal}}, muộn hơn {{k2.roll.later}}.
- **Vì sao:** Chưa phân xử nguyên nhân thống kê: các cờ (lịch sử ngắn, cột báo dày, độ lệch chuẩn bằng không, nền mở rộng nhận dữ liệu sau mốc) mới là liên hệ. Đã xác lập ở mức CT rằng độ dài lịch sử và phép OR nhiều cột đi vào kết quả. Mức CT của dòng chỉ thuộc phần này.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: cờ N1–N4, N6 và đọc tay (T-029) — LĐ; đối chiếu lịch sử trượt/mở rộng (T-033, K2) — CT.
- **Loại nguồn hạn chế:** M.
- **Giải thích khác còn lại:** Đuôi không chuẩn; nền không dừng; nhiều cột cùng được xét (phép OR); lượng hóa của metric. Không có nền sạch độc lập để gọi một báo động là “sai trong vận hành”.
- **Tác giả có nêu không:** Bài BARO nêu baseline báo sai nhiều; chưa thấy cơ chế cụ thể.
- **Ảnh hưởng tới:** RQ1, RQ2, RQ3a.
- **Số ca theo ô:** Phụ lục B, các cột HP-1, HP-2, HP-3, HP-4.

#### G2-H23 — Đầu vào bậc thang: nhiều hàng metric lặp lại

- **Phương pháp; dataset; chế độ:** BOCPD (bản BARO); RE2-TT; (b).
- **Mã gốc:** T-033:K4.
- **Hiện tượng:** Chuỗi đầu vào có nhiều vectơ lặp liên tiếp; số quan sát hiệu lực ít hơn số hàng.
- **Số:** Bỏ hàng lặp: tập điểm đổi khác bản gốc ở {{k3.compressed_row.changed}}/{{k3.compressed_row.cases}} ca (hazard theo hàng) và {{k3.compressed_calendar.changed}}/{{k3.compressed_calendar.cases}} ca (hazard theo thời gian); tổng điểm đổi {{k3.native.cp}} → {{k3.compressed_row.cp}} và {{k3.compressed_calendar.cp}}.
- **Vì sao:** Đã xác lập ở mức CT rằng gói thay đổi “bỏ hàng lặp” làm đổi điểm đổi. Chưa phân xử riêng từng yếu tố: phép nén đổi cùng lúc số lần cập nhật, đơn vị run length và quy tắc CP.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: hai nhánh nén (T-033 gói bổ sung, K4) — CT.
- **Loại nguồn hạn chế:** D + M.
- **Giải thích khác còn lại:** Không chứng minh lượng hóa của bộ thu thập là nguyên nhân, cũng không chứng minh nén là cách sửa. Tổng điểm đổi giảm ở phần lớn ô nhưng tăng ở ô route/mem ({{k3.cell.routemem.native}} → {{k3.cell.routemem.row}} và {{k3.cell.routemem.calendar}}); mỗi ô ba ca, không coi là mẫu hình.
- **Tác giả có nêu không:** Chưa thấy trong nguồn đã khảo sát.
- **Ảnh hưởng tới:** RQ2, RQ5.
- **Số ca theo ô:** Phụ lục C, bảng của G2-H23.

#### G2-H24 — Nhãn proxy, thời lượng lỗi và onset chưa được xác nhận độc lập

- **Phương pháp; dataset; chế độ:** Mọi phép chấm phát hiện; RE2-TT; (b).
- **Mã gốc:** HP-12, T-033:K1, T-033:K5, T-033:K7.
- **Hiện tượng:** Nhãn chỉ có mốc tiêm; không biết lúc lỗi bắt đầu có tác động, lúc hết, và đoạn trước mốc có sạch không.
- **Số:** Số ca BOCPD có điểm đổi trong D giây sau mốc: {{k7.d30}}, {{k7.d60}}, {{k7.d120}}, {{k7.d300}}, {{k7.d600}} trên {{bl.det.bocpd.n}} ca, với D lần lượt là các mức `30`, `60`, `120`, `300`, `600` giây. Log có ghi kết quả ở vị trí cụ thể: access log {{k5.http200}} dòng HTTP `200`, {{k5.http500}} dòng `500`, {{k5.http503}} dòng `503`; phản hồi backend {{k5.app1}} lần trạng thái `1` và {{k5.app0}} lần trạng thái `0`.
- **Vì sao:** Chưa phân xử, vì dataset không cung cấp onset có tác động, lúc hết lỗi, đoạn khỏe được kiểm độc lập, sai số đồng hồ và phép nối đã xác minh giữa dòng log với từng lời gọi.
- **Mức bằng chứng cao nhất:** MT (mô tả). Nguồn con: đường độ nhạy theo D (T-033, K7) — MT; đọc toàn bộ thông điệp log ở vùng khóa (T-033, K1, K5) — MT; nguồn chưa xác nhận D (T-029, HP-12) — CK.
- **Loại nguồn hạn chế:** D.
- **Giải thích khác còn lại:** Số dòng log không phải số yêu cầu hay số sự cố. HTTP `200` hay trạng thái `1` không chứng minh hệ khỏe; `500` hay `503` không tự cho onset.
- **Tác giả có nêu không:** RCAEval mô tả mốc tiêm và cách thu; chưa thấy thời lượng lỗi cho các ca này.
- **Ảnh hưởng tới:** RQ3a, RQ5.
- **Số ca theo ô:** Không tách theo ô: đây là giới hạn chung của bộ dữ liệu. Không có nhãn thời điểm sự cố bắt đầu có tác động, nên không dựng tỷ lệ theo ô.

#### G2-H25 — Schema metric đổi theo ca và liên hệ với root

- **Phương pháp; dataset; chế độ:** BARO, SimpleRCA, CIRCA, TORAI, BOCPD, N-Sigma; RE2-TT; (a), (b).
- **Mã gốc:** HP-13.
- **Hiện tượng:** Tập cột metric khác nhau giữa các ca; sự có mặt của một số cột liên hệ với root.
- **Số:** Số cột bộ phát hiện nhận và số chiều sau tiền xử lý, theo từng ca trong từng ô: Phụ lục C. Bảng chéo cột × root ở `results/T-029/nhan-proxy-va-schema.json`.
- **Vì sao:** Chưa phân xử ảnh hưởng của schema lên kết quả: bảng chéo trên dev không tách được schema với việc mất tín hiệu lỗi (WHY-27).
- **Mức bằng chứng cao nhất:** LĐ (liên hệ có đối chứng). Nguồn con: bảng chéo schema × root (T-029, P2) — LĐ.
- **Loại nguồn hạn chế:** D.
- **Giải thích khác còn lại:** Triển khai và thu thập khác nhau theo dịch vụ; root và loại lỗi chưa giao chéo đầy đủ trong dev.
- **Tác giả có nêu không:** Chưa thấy trong nguồn đã khảo sát.
- **Ảnh hưởng tới:** RQ1, RQ2.
- **Số ca theo ô:** Phụ lục C, bảng của G2-H25.

#### G2-H26 — Chế độ (b): thành công chung bị chặn ở báo động đầu; RCA phụ thuộc điểm chạy

- **Phương pháp; dataset; chế độ:** BARO, CIRCA, TORAI B ghép với BOCPD hoặc N-Sigma; RE2-TT; (b).
- **Mã gốc:** HP-10, HP-11.
- **Hiện tượng:** RCA chạy tại báo động đầu; báo động đầu sai thì ca trượt. Cùng một ranker cho kết quả khác nhau khi chạy tại mốc tiêm, tại báo động đầu sau mốc, và tại báo động đầu.
- **Số:** BARO ghép BOCPD, Hit@1 trên {{bl.det.bocpd.n}} ca: {{bl.g.baro_bocpd.a:.2f}} tại mốc tiêm, {{bl.g.baro_bocpd.tplus:.2f}} tại báo động đầu sau mốc, {{bl.g.baro_bocpd.that:.2f}} tại báo động đầu; TORAI B ghép BOCPD: {{bl.g.torai_bocpd.a:.2f}}, {{bl.g.torai_bocpd.tplus:.2f}}, {{bl.g.torai_bocpd.that:.2f}}. Thành công chung Hit@1 cao nhất: {{bl.b.baro_bocpd.joint1:.3f}} (BARO ghép BOCPD).
- **Vì sao:** Đã xác lập ở mức CT rằng điểm chạy RCA làm đổi kết quả. Chưa phân xử từng đường tác động: đổi cửa sổ còn đổi nền, cột ứng viên và đồ thị của CIRCA.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: can thiệp I3 và bảng G (T-029) — CT.
- **Loại nguồn hạn chế:** G + M.
- **Giải thích khác còn lại:** Báo động đầu sau mốc được chọn nhờ nhãn mốc, nên không phải cận trên của chất lượng RCA. Thứ tự báo động của các dịch vụ không phải bằng chứng nhân quả hay lan.
- **Tác giả có nêu không:** Bài BARO có nêu độ nhạy theo thời điểm.
- **Ảnh hưởng tới:** RQ1, RQ2.
- **Số ca theo ô:** Phụ lục C, bảng của G2-H26.

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

Đây là **ứng viên để thử**, không phải lựa chọn, và không xếp theo kỳ vọng thắng. Thành phần cụ thể chốt ở spec P6, sau khi so phương án và kiểm trên dev. Mức căn cứ theo bảng ở MRP §3: UV-1 đến UV-6, UV-8, UV-9 và phần (i) của UV-7 mới đạt bậc “đủ để đề xuất thử”. Hai phần **chưa** đạt bậc đó: phần (ii) của UV-7 (cách gộp điểm) là câu hỏi thiết kế, chưa có phương án cụ thể và chưa có dự đoán; UV-10 là yêu cầu của DT18, chưa có dự đoán kiểm được trên dev vì dữ liệu thiếu đầu vào. UV-10 vẫn phải được thiết kế và kiểm khi có đầu vào phù hợp (FlashTicket, P10); đây không phải miễn kiểm. Để **chọn** còn thiếu: so phương án, kiểm đầu vào, trung gian và hành vi của chính bản cài mới trên dev. Để **khẳng định hiệu quả** còn thiếu: đánh giá sau khóa thiết kế, với nhánh cùng bằng chứng không dùng quan hệ và đồ thị ngẫu nhiên giữ bậc.

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

### UV-7 — Xử lý giá trị không hợp lệ và cách gộp điểm khi lan trên đồ thị

- **Mục đích:** nhu cầu kỹ thuật, rút từ G2-H12.
- **Căn cứ và mức:** CT cho câu “một giá trị không hợp lệ đi qua cấu trúc làm hỏng thứ hạng”: ở {{h13.huge}}/{{h13.n}} ca của CIRCA có nút điểm cực lớn; trong nhóm đó số ca đúng là {{h13.da}} (có DA), {{h13.rht}} (có cạnh, không DA), {{h13.k2}} (bỏ mọi cạnh). **Chưa** có căn cứ cho một cách gộp điểm cụ thể: phép bỏ cạnh đổi cả hồi quy lẫn bước cộng điểm, không cô lập bước cộng; và bước DA trong mã chỉ cộng khi điểm của nút vượt ngưỡng.
- **Nội dung:** (i) yêu cầu kỹ thuật: kiểm và xử lý giá trị không hợp lệ ở một nút trước khi lan; (ii) câu hỏi thiết kế để spec P6 giải quyết, chưa là ứng viên: cách gộp điểm từ nút con lên nút cha.
- **Dự đoán trên dev, khai trước:** với (i), không còn ca nào mà một nút điểm cực lớn quyết định thứ hạng. **Bác bỏ** nếu vẫn còn. Với (ii): so các cách gộp trên cùng điểm đầu vào; đây là câu cần chọn phương án ở spec P6, chưa có dự đoán.
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

### UV-10 — Các thành phần DT18 yêu cầu mà P4 không cung cấp bằng chứng

- **Mục đích:** đáp ứng DT18 và bước 1–2 của cô: cạnh trao đổi thông điệp và phụ thuộc dữ liệu; vùng nghi ngờ (đồ thị con bất thường); xếp hạng trên đồ thị.
- **Căn cứ:** yêu cầu của đề tài (đoạn nhiệm vụ thứ hai của DT18), **không** phải một hạn chế đã thấy ở P4. Đã khảo sát ở P2: trace RE2-TT không có loại span hay thuộc tính đủ dựng cạnh có kiểu (`results/T-002/the-rcaeval.md`); Nezha-OB chưa đủ bằng chứng cho cạnh thông điệp và phụ thuộc dữ liệu (`results/T-008/the-dataset.md`). Điều này không nói các quan hệ ấy không tồn tại. Hai loại cạnh này chỉ dựng được từ nguồn tĩnh hoặc trên FlashTicket; UV-10 không có dự đoán kiểm được trên dev. Không có nhãn vùng ảnh hưởng.
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

Hai phép E1 và E2 đã được giao và **đã chạy xong** trong task này (`results/T-034/hai-phep-kiem.md`). Ba dòng đầu là phần còn lại sau chúng. Cả sáu dòng đều chưa được giao.

### 6.2 Thiếu quan sát hoặc nhãn độc lập (không phục hồi được từ dữ liệu hiện có)

| Thông tin thiếu | Vì sao dữ liệu hiện có không cung cấp | Câu bị chặn | Đối chiếu chuẩn quan sát B16 của FlashTicket | Ai cung cấp |
|---|---|---|---|---|
| Lúc lỗi bắt đầu có tác động, lúc hết lỗi, đoạn nền được xác nhận khỏe | RE2-TT chỉ ghi mốc tiêm | Vì sao báo trước mốc (G2-H21, G2-H22); báo động sai trong vận hành; D (G2-H24) | B16 mục 8 yêu cầu manifest ghi lỗi đã tiêm và độ lệch đồng hồ; **chưa** yêu cầu mốc có tác động, mốc hồi phục và lượt nền được kiểm riêng | Nhóm hệ thống (bộ tiêm lỗi do Minh dựng, Q-19) |
| Nhật ký của bộ tạo tải | Dataset không công bố | Tách “tải đổi” khỏi “sự cố” ở các báo động trước mốc | B16 mục 8 có ghi workload trong manifest; chưa có log theo thời gian của bộ tạo tải | Nhóm hệ thống |
| Ánh xạ dịch vụ–máy và metric mức máy | Không có trong hai dataset | Vì sao dịch vụ không liên hệ đổi tại mốc (G2-H11) | B16 mục 4 có `hostId`; mục 5 có metric hạ tầng | Đã nằm trong chuẩn; cần kiểm khi chạy |
| Loại span và thuộc tính thông điệp, cơ sở dữ liệu | Trace của hai dataset không ghi (thẻ dataset của T-002 và T-008) | Dựng cạnh thông điệp và cạnh dữ liệu của DT18 (UV-10) | B16 mục 3 có quy định span hoặc link cho bên gửi và bên nhận thông điệp; chưa thấy yêu cầu ghi loại span và thuộc tính cơ sở dữ liệu | Nhóm hệ thống |
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
Ba nhóm. Còn kiểm được trên dev: sáu phép ở mục 6.1. Thiếu quan sát: onset, nền sạch, quan hệ dịch vụ–máy; chuyển thành yêu cầu quan sát cho FlashTicket. Thuộc đánh giá sau: đồ thị có giúp không. *Mức: CK. Nguồn:* mục 6.

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

**RE2-TT / MicroRank**

| Ô | Số ca | Sai hạng 1 (chạy được) | Không chạy được | Cờ M5 | Cờ M0 | Phép đổi: chia trace theo bài gốc (mo15) | Phép đổi: chia trace theo bài gốc (mo1p50) | Phép đổi: đếm riêng (M-C1) | Phép đổi: trọng số đơn vị (A′) | Phép đổi: cờ theo phần chưa phủ (M-D) |
|---|---|---|---|---|---|---|---|---|---|---|
| auth / cpu | {{a0511}} | {{a0512}} | {{a0513}} | {{a0514}} | {{a0515}} | {{a0516}}/{{a0517}} | {{a0518}}/{{a0519}} | {{a0520}}/{{a0521}} | {{a0522}}/{{a0523}} | {{a0524}}/{{a0525}} |
| auth / delay | {{a0526}} | {{a0527}} | {{a0528}} | {{a0529}} | {{a0530}} | {{a0531}}/{{a0532}} | {{a0533}}/{{a0534}} | {{a0535}}/{{a0536}} | {{a0537}}/{{a0538}} | {{a0539}}/{{a0540}} |
| order / disk | {{a0541}} | {{a0542}} | {{a0543}} | {{a0544}} | {{a0545}} | {{a0546}}/{{a0547}} | {{a0548}}/{{a0549}} | {{a0550}}/{{a0551}} | {{a0552}}/{{a0553}} | {{a0554}}/{{a0555}} |
| order / loss | {{a0556}} | {{a0557}} | {{a0558}} | {{a0559}} | {{a0560}} | {{a0561}}/{{a0562}} | {{a0563}}/{{a0564}} | {{a0565}}/{{a0566}} | {{a0567}}/{{a0568}} | {{a0569}}/{{a0570}} |
| route / mem | {{a0571}} | {{a0572}} | {{a0573}} | {{a0574}} | {{a0575}} | {{a0576}}/{{a0577}} | {{a0578}}/{{a0579}} | {{a0580}}/{{a0581}} | {{a0582}}/{{a0583}} | {{a0584}}/{{a0585}} |
| route / socket | {{a0586}} | {{a0587}} | {{a0588}} | {{a0589}} | {{a0590}} | {{a0591}}/{{a0592}} | {{a0593}}/{{a0594}} | {{a0595}}/{{a0596}} | {{a0597}}/{{a0598}} | {{a0599}}/{{a0600}} |
| train / cpu | {{a0601}} | {{a0602}} | {{a0603}} | {{a0604}} | {{a0605}} | {{a0606}}/{{a0607}} | {{a0608}}/{{a0609}} | {{a0610}}/{{a0611}} | {{a0612}}/{{a0613}} | {{a0614}}/{{a0615}} |
| train / delay | {{a0616}} | {{a0617}} | {{a0618}} | {{a0619}} | {{a0620}} | {{a0621}}/{{a0622}} | {{a0623}}/{{a0624}} | {{a0625}}/{{a0626}} | {{a0627}}/{{a0628}} | {{a0629}}/{{a0630}} |
| travel / disk | {{a0631}} | {{a0632}} | {{a0633}} | {{a0634}} | {{a0635}} | {{a0636}}/{{a0637}} | {{a0638}}/{{a0639}} | {{a0640}}/{{a0641}} | {{a0642}}/{{a0643}} | {{a0644}}/{{a0645}} |
| travel / loss | {{a0646}} | {{a0647}} | {{a0648}} | {{a0649}} | {{a0650}} | {{a0651}}/{{a0652}} | {{a0653}}/{{a0654}} | {{a0655}}/{{a0656}} | {{a0657}}/{{a0658}} | {{a0659}}/{{a0660}} |

**Nezha-OB / MicroRank**

| Ô | Số ca | Sai hạng 1 (chạy được) | Không chạy được | Cờ M5 | Cờ M6 | Cờ M0 | Phép đổi: chia trace theo bài gốc (mo15) | Phép đổi: chia trace theo bài gốc (mo1p50) | Phép đổi: đếm riêng (M-C1) | Phép đổi: trọng số đơn vị (A′) | Phép đổi: cờ theo phần chưa phủ (M-D) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ad / cpu_contention | {{a0661}} | {{a0662}} | {{a0663}} | {{a0664}} | {{a0665}} | {{a0666}} | {{a0667}}/{{a0668}} | {{a0669}}/{{a0670}} | {{a0671}}/{{a0672}} | {{a0673}}/{{a0674}} | {{a0675}}/{{a0676}} |
| checkout / exception | {{a0677}} | {{a0678}} | {{a0679}} | {{a0680}} | {{a0681}} | {{a0682}} | {{a0683}}/{{a0684}} | {{a0685}}/{{a0686}} | {{a0687}}/{{a0688}} | {{a0689}}/{{a0690}} | {{a0691}}/{{a0692}} |
| checkout / network_delay | {{a0693}} | {{a0694}} | {{a0695}} | {{a0696}} | {{a0697}} | {{a0698}} | {{a0699}}/{{a0700}} | {{a0701}}/{{a0702}} | {{a0703}}/{{a0704}} | {{a0705}}/{{a0706}} | {{a0707}}/{{a0708}} |
| checkout / return | {{a0709}} | {{a0710}} | {{a0711}} | {{a0712}} | {{a0713}} | {{a0714}} | {{a0715}}/{{a0716}} | {{a0717}}/{{a0718}} | {{a0719}}/{{a0720}} | {{a0721}}/{{a0722}} | {{a0723}}/{{a0724}} |
| email / cpu_consumed | {{a0725}} | {{a0726}} | {{a0727}} | {{a0728}} | {{a0729}} | {{a0730}} | {{a0731}}/{{a0732}} | {{a0733}}/{{a0734}} | {{a0735}}/{{a0736}} | {{a0737}}/{{a0738}} | {{a0739}}/{{a0740}} |
| email / network_delay | {{a0741}} | {{a0742}} | {{a0743}} | {{a0744}} | {{a0745}} | {{a0746}} | {{a0747}}/{{a0748}} | {{a0749}}/{{a0750}} | {{a0751}}/{{a0752}} | {{a0753}}/{{a0754}} | {{a0755}}/{{a0756}} |
| frontend / return | {{a0757}} | {{a0758}} | {{a0759}} | {{a0760}} | {{a0761}} | {{a0762}} | {{a0763}}/{{a0764}} | {{a0765}}/{{a0766}} | {{a0767}}/{{a0768}} | {{a0769}}/{{a0770}} | {{a0771}}/{{a0772}} |
| payment / cpu_contention | {{a0773}} | {{a0774}} | {{a0775}} | {{a0776}} | {{a0777}} | {{a0778}} | {{a0779}}/{{a0780}} | {{a0781}}/{{a0782}} | {{a0783}}/{{a0784}} | {{a0785}}/{{a0786}} | {{a0787}}/{{a0788}} |
| productcatalog / exception | {{a0789}} | {{a0790}} | {{a0791}} | {{a0792}} | {{a0793}} | {{a0794}} | {{a0795}}/{{a0796}} | {{a0797}}/{{a0798}} | {{a0799}}/{{a0800}} | {{a0801}}/{{a0802}} | {{a0803}}/{{a0804}} |
| recommendation / cpu_consumed | {{a0805}} | {{a0806}} | {{a0807}} | {{a0808}} | {{a0809}} | {{a0810}} | {{a0811}}/{{a0812}} | {{a0813}}/{{a0814}} | {{a0815}}/{{a0816}} | {{a0817}}/{{a0818}} | {{a0819}}/{{a0820}} |
| recommendation / network_delay | {{a0821}} | {{a0822}} | {{a0823}} | {{a0824}} | {{a0825}} | {{a0826}} | {{a0827}}/{{a0828}} | {{a0829}}/{{a0830}} | {{a0831}}/{{a0832}} | {{a0833}}/{{a0834}} | {{a0835}}/{{a0836}} |
| shipping / cpu_consumed | {{a0837}} | {{a0838}} | {{a0839}} | {{a0840}} | {{a0841}} | {{a0842}} | {{a0843}}/{{a0844}} | {{a0845}}/{{a0846}} | {{a0847}}/{{a0848}} | {{a0849}}/{{a0850}} | {{a0851}}/{{a0852}} |
| shipping / cpu_contention | {{a0853}} | {{a0854}} | {{a0855}} | {{a0856}} | {{a0857}} | {{a0858}} | {{a0859}}/{{a0860}} | {{a0861}}/{{a0862}} | {{a0863}}/{{a0864}} | {{a0865}}/{{a0866}} | {{a0867}}/{{a0868}} |

**RE2-TT / TraceRCA**

| Ô | Số ca | Sai hạng 1 (chạy được) | Không chạy được | Cờ M5 | Cờ M0 | Phép đổi: cờ theo phần chưa phủ (T-D) | Phép đổi: bước xếp hạng theo lời văn (to_p) |
|---|---|---|---|---|---|---|---|
| auth / cpu | {{a0869}} | {{a0870}} | {{a0871}} | {{a0872}} | {{a0873}} | — | — |
| auth / delay | {{a0874}} | {{a0875}} | {{a0876}} | {{a0877}} | {{a0878}} | — | — |
| order / disk | {{a0879}} | {{a0880}} | {{a0881}} | {{a0882}} | {{a0883}} | {{a0884}}/{{a0885}} | {{a0886}}/{{a0887}} |
| order / loss | {{a0888}} | {{a0889}} | {{a0890}} | {{a0891}} | {{a0892}} | {{a0893}}/{{a0894}} | {{a0895}}/{{a0896}} |
| route / mem | {{a0897}} | {{a0898}} | {{a0899}} | {{a0900}} | {{a0901}} | — | — |
| route / socket | {{a0902}} | {{a0903}} | {{a0904}} | {{a0905}} | {{a0906}} | — | — |
| train / cpu | {{a0907}} | {{a0908}} | {{a0909}} | {{a0910}} | {{a0911}} | — | — |
| train / delay | {{a0912}} | {{a0913}} | {{a0914}} | {{a0915}} | {{a0916}} | — | — |
| travel / disk | {{a0917}} | {{a0918}} | {{a0919}} | {{a0920}} | {{a0921}} | {{a0922}}/{{a0923}} | {{a0924}}/{{a0925}} |
| travel / loss | {{a0926}} | {{a0927}} | {{a0928}} | {{a0929}} | {{a0930}} | — | — |

**Nezha-OB / TraceRCA**

| Ô | Số ca | Sai hạng 1 (chạy được) | Không chạy được | Cờ M2 | Cờ M3 | Cờ M5 | Cờ M6 | Cờ M0 | Phép đổi: cờ theo phần chưa phủ (T-D) | Phép đổi: bước xếp hạng theo lời văn (to_p) |
|---|---|---|---|---|---|---|---|---|---|---|
| ad / cpu_contention | {{a0931}} | {{a0932}} | {{a0933}} | {{a0934}} | {{a0935}} | {{a0936}} | {{a0937}} | {{a0938}} | {{a0939}}/{{a0940}} | {{a0941}}/{{a0942}} |
| checkout / exception | {{a0943}} | {{a0944}} | {{a0945}} | {{a0946}} | {{a0947}} | {{a0948}} | {{a0949}} | {{a0950}} | {{a0951}}/{{a0952}} | {{a0953}}/{{a0954}} |
| checkout / network_delay | {{a0955}} | {{a0956}} | {{a0957}} | {{a0958}} | {{a0959}} | {{a0960}} | {{a0961}} | {{a0962}} | {{a0963}}/{{a0964}} | {{a0965}}/{{a0966}} |
| checkout / return | {{a0967}} | {{a0968}} | {{a0969}} | {{a0970}} | {{a0971}} | {{a0972}} | {{a0973}} | {{a0974}} | {{a0975}}/{{a0976}} | {{a0977}}/{{a0978}} |
| email / cpu_consumed | {{a0979}} | {{a0980}} | {{a0981}} | {{a0982}} | {{a0983}} | {{a0984}} | {{a0985}} | {{a0986}} | {{a0987}}/{{a0988}} | {{a0989}}/{{a0990}} |
| email / network_delay | {{a0991}} | {{a0992}} | {{a0993}} | {{a0994}} | {{a0995}} | {{a0996}} | {{a0997}} | {{a0998}} | {{a0999}}/{{a1000}} | {{a1001}}/{{a1002}} |
| frontend / return | {{a1003}} | {{a1004}} | {{a1005}} | {{a1006}} | {{a1007}} | {{a1008}} | {{a1009}} | {{a1010}} | {{a1011}}/{{a1012}} | {{a1013}}/{{a1014}} |
| payment / cpu_contention | {{a1015}} | {{a1016}} | {{a1017}} | {{a1018}} | {{a1019}} | {{a1020}} | {{a1021}} | {{a1022}} | {{a1023}}/{{a1024}} | {{a1025}}/{{a1026}} |
| productcatalog / exception | {{a1027}} | {{a1028}} | {{a1029}} | {{a1030}} | {{a1031}} | {{a1032}} | {{a1033}} | {{a1034}} | {{a1035}}/{{a1036}} | {{a1037}}/{{a1038}} |
| recommendation / cpu_consumed | {{a1039}} | {{a1040}} | {{a1041}} | {{a1042}} | {{a1043}} | {{a1044}} | {{a1045}} | {{a1046}} | {{a1047}}/{{a1048}} | {{a1049}}/{{a1050}} |
| recommendation / network_delay | {{a1051}} | {{a1052}} | {{a1053}} | {{a1054}} | {{a1055}} | {{a1056}} | {{a1057}} | {{a1058}} | {{a1059}}/{{a1060}} | {{a1061}}/{{a1062}} |
| shipping / cpu_consumed | {{a1063}} | {{a1064}} | {{a1065}} | {{a1066}} | {{a1067}} | {{a1068}} | {{a1069}} | {{a1070}} | — | — |
| shipping / cpu_contention | {{a1071}} | {{a1072}} | {{a1073}} | {{a1074}} | {{a1075}} | {{a1076}} | {{a1077}} | {{a1078}} | {{a1079}}/{{a1080}} | {{a1081}}/{{a1082}} |

**Nezha-OB / BARO**

| Ô | Số ca | Sai hạng 1 (chạy được) | Không chạy được | Cờ M5 | Cờ M0 | Phép đổi: thang độ lệch chuẩn (B-2) |
|---|---|---|---|---|---|---|
| ad / cpu_contention | {{a1083}} | {{a1084}} | {{a1085}} | {{a1086}} | {{a1087}} | — |
| checkout / exception | {{a1088}} | {{a1089}} | {{a1090}} | {{a1091}} | {{a1092}} | {{a1093}}/{{a1094}} |
| checkout / network_delay | {{a1095}} | {{a1096}} | {{a1097}} | {{a1098}} | {{a1099}} | {{a1100}}/{{a1101}} |
| checkout / return | {{a1102}} | {{a1103}} | {{a1104}} | {{a1105}} | {{a1106}} | {{a1107}}/{{a1108}} |
| email / cpu_consumed | {{a1109}} | {{a1110}} | {{a1111}} | {{a1112}} | {{a1113}} | — |
| email / network_delay | {{a1114}} | {{a1115}} | {{a1116}} | {{a1117}} | {{a1118}} | {{a1119}}/{{a1120}} |
| frontend / return | {{a1121}} | {{a1122}} | {{a1123}} | {{a1124}} | {{a1125}} | {{a1126}}/{{a1127}} |
| payment / cpu_contention | {{a1128}} | {{a1129}} | {{a1130}} | {{a1131}} | {{a1132}} | — |
| productcatalog / exception | {{a1133}} | {{a1134}} | {{a1135}} | {{a1136}} | {{a1137}} | {{a1138}}/{{a1139}} |
| recommendation / cpu_consumed | {{a1140}} | {{a1141}} | {{a1142}} | {{a1143}} | {{a1144}} | {{a1145}}/{{a1146}} |
| recommendation / network_delay | {{a1147}} | {{a1148}} | {{a1149}} | {{a1150}} | {{a1151}} | {{a1152}}/{{a1153}} |
| shipping / cpu_consumed | {{a1154}} | {{a1155}} | {{a1156}} | {{a1157}} | {{a1158}} | {{a1159}}/{{a1160}} |
| shipping / cpu_contention | {{a1161}} | {{a1162}} | {{a1163}} | {{a1164}} | {{a1165}} | — |

**Nezha-OB / SimpleRCA**

| Ô | Số ca | Sai hạng 1 (chạy được) | Không chạy được | Cờ M5 | Cờ M6 | Cờ M0 | Phép đổi: đếm theo cột (S-1) |
|---|---|---|---|---|---|---|---|
| ad / cpu_contention | {{a1166}} | {{a1167}} | {{a1168}} | {{a1169}} | {{a1170}} | {{a1171}} | — |
| checkout / exception | {{a1172}} | {{a1173}} | {{a1174}} | {{a1175}} | {{a1176}} | {{a1177}} | {{a1178}}/{{a1179}} |
| checkout / network_delay | {{a1180}} | {{a1181}} | {{a1182}} | {{a1183}} | {{a1184}} | {{a1185}} | {{a1186}}/{{a1187}} |
| checkout / return | {{a1188}} | {{a1189}} | {{a1190}} | {{a1191}} | {{a1192}} | {{a1193}} | {{a1194}}/{{a1195}} |
| email / cpu_consumed | {{a1196}} | {{a1197}} | {{a1198}} | {{a1199}} | {{a1200}} | {{a1201}} | {{a1202}}/{{a1203}} |
| email / network_delay | {{a1204}} | {{a1205}} | {{a1206}} | {{a1207}} | {{a1208}} | {{a1209}} | {{a1210}}/{{a1211}} |
| frontend / return | {{a1212}} | {{a1213}} | {{a1214}} | {{a1215}} | {{a1216}} | {{a1217}} | {{a1218}}/{{a1219}} |
| payment / cpu_contention | {{a1220}} | {{a1221}} | {{a1222}} | {{a1223}} | {{a1224}} | {{a1225}} | — |
| productcatalog / exception | {{a1226}} | {{a1227}} | {{a1228}} | {{a1229}} | {{a1230}} | {{a1231}} | — |
| recommendation / cpu_consumed | {{a1232}} | {{a1233}} | {{a1234}} | {{a1235}} | {{a1236}} | {{a1237}} | {{a1238}}/{{a1239}} |
| recommendation / network_delay | {{a1240}} | {{a1241}} | {{a1242}} | {{a1243}} | {{a1244}} | {{a1245}} | {{a1246}}/{{a1247}} |
| shipping / cpu_consumed | {{a1248}} | {{a1249}} | {{a1250}} | {{a1251}} | {{a1252}} | {{a1253}} | {{a1254}}/{{a1255}} |
| shipping / cpu_contention | {{a1256}} | {{a1257}} | {{a1258}} | {{a1259}} | {{a1260}} | {{a1261}} | — |

**RE2-TT / SimpleRCA**

| Ô | Số ca | Sai hạng 1 (chạy được) | Không chạy được | Cờ M5 | Phép đổi: đếm theo cột (S-1) |
|---|---|---|---|---|---|
| auth / cpu | {{a1262}} | {{a1263}} | {{a1264}} | {{a1265}} | — |
| auth / delay | {{a1266}} | {{a1267}} | {{a1268}} | {{a1269}} | — |
| order / disk | {{a1270}} | {{a1271}} | {{a1272}} | {{a1273}} | — |
| order / loss | {{a1274}} | {{a1275}} | {{a1276}} | {{a1277}} | {{a1278}}/{{a1279}} |
| route / mem | {{a1280}} | {{a1281}} | {{a1282}} | {{a1283}} | — |
| route / socket | {{a1284}} | {{a1285}} | {{a1286}} | {{a1287}} | — |
| train / cpu | {{a1288}} | {{a1289}} | {{a1290}} | {{a1291}} | — |
| train / delay | {{a1292}} | {{a1293}} | {{a1294}} | {{a1295}} | {{a1296}}/{{a1297}} |
| travel / disk | {{a1298}} | {{a1299}} | {{a1300}} | {{a1301}} | — |
| travel / loss | {{a1302}} | {{a1303}} | {{a1304}} | {{a1305}} | {{a1306}}/{{a1307}} |

**RE2-TT / BARO**

| Ô | Số ca | Sai hạng 1 (chạy được) | Không chạy được | Cờ M5 | Cờ M0 | Phép đổi: thang độ lệch chuẩn (B-2) |
|---|---|---|---|---|---|---|
| auth / cpu | {{a1308}} | {{a1309}} | {{a1310}} | {{a1311}} | {{a1312}} | {{a1313}}/{{a1314}} |
| auth / delay | {{a1315}} | {{a1316}} | {{a1317}} | {{a1318}} | {{a1319}} | {{a1320}}/{{a1321}} |
| order / disk | {{a1322}} | {{a1323}} | {{a1324}} | {{a1325}} | {{a1326}} | — |
| order / loss | {{a1327}} | {{a1328}} | {{a1329}} | {{a1330}} | {{a1331}} | {{a1332}}/{{a1333}} |
| route / mem | {{a1334}} | {{a1335}} | {{a1336}} | {{a1337}} | {{a1338}} | {{a1339}}/{{a1340}} |
| route / socket | {{a1341}} | {{a1342}} | {{a1343}} | {{a1344}} | {{a1345}} | — |
| train / cpu | {{a1346}} | {{a1347}} | {{a1348}} | {{a1349}} | {{a1350}} | — |
| train / delay | {{a1351}} | {{a1352}} | {{a1353}} | {{a1354}} | {{a1355}} | — |
| travel / disk | {{a1356}} | {{a1357}} | {{a1358}} | {{a1359}} | {{a1360}} | — |
| travel / loss | {{a1361}} | {{a1362}} | {{a1363}} | {{a1364}} | {{a1365}} | {{a1366}}/{{a1367}} |

**RE2-TT / CIRCA**

| Ô | Số ca | Sai hạng 1 (chạy được) | Không chạy được | Cờ M4 | Cờ M5 | Cờ M0 | Phép đổi: bỏ mọi cạnh, RHT (K-2) |
|---|---|---|---|---|---|---|---|
| auth / cpu | {{a1368}} | {{a1369}} | {{a1370}} | {{a1371}} | {{a1372}} | {{a1373}} | {{a1374}}/{{a1375}} |
| auth / delay | {{a1376}} | {{a1377}} | {{a1378}} | {{a1379}} | {{a1380}} | {{a1381}} | {{a1382}}/{{a1383}} |
| order / disk | {{a1384}} | {{a1385}} | {{a1386}} | {{a1387}} | {{a1388}} | {{a1389}} | — |
| order / loss | {{a1390}} | {{a1391}} | {{a1392}} | {{a1393}} | {{a1394}} | {{a1395}} | {{a1396}}/{{a1397}} |
| route / mem | {{a1398}} | {{a1399}} | {{a1400}} | {{a1401}} | {{a1402}} | {{a1403}} | {{a1404}}/{{a1405}} |
| route / socket | {{a1406}} | {{a1407}} | {{a1408}} | {{a1409}} | {{a1410}} | {{a1411}} | {{a1412}}/{{a1413}} |
| train / cpu | {{a1414}} | {{a1415}} | {{a1416}} | {{a1417}} | {{a1418}} | {{a1419}} | {{a1420}}/{{a1421}} |
| train / delay | {{a1422}} | {{a1423}} | {{a1424}} | {{a1425}} | {{a1426}} | {{a1427}} | {{a1428}}/{{a1429}} |
| travel / disk | {{a1430}} | {{a1431}} | {{a1432}} | {{a1433}} | {{a1434}} | {{a1435}} | — |
| travel / loss | {{a1436}} | {{a1437}} | {{a1438}} | {{a1439}} | {{a1440}} | {{a1441}} | {{a1442}}/{{a1443}} |

**RE2-TT / TORAI B**

| Ô | Số ca | Sai hạng 1 (chạy được) | Không chạy được | Cờ M5 | Cờ M0 | Phép đổi: bỏ nguồn log, seed 0 (tl1) |
|---|---|---|---|---|---|---|
| auth / cpu | {{a1444}} | {{a1445}} | {{a1446}} | {{a1447}} | {{a1448}} | {{a1449}}/{{a1450}} |
| auth / delay | {{a1451}} | {{a1452}} | {{a1453}} | {{a1454}} | {{a1455}} | — |
| order / disk | {{a1456}} | {{a1457}} | {{a1458}} | {{a1459}} | {{a1460}} | — |
| order / loss | {{a1461}} | {{a1462}} | {{a1463}} | {{a1464}} | {{a1465}} | {{a1466}}/{{a1467}} |
| route / mem | {{a1468}} | {{a1469}} | {{a1470}} | {{a1471}} | {{a1472}} | — |
| route / socket | {{a1473}} | {{a1474}} | {{a1475}} | {{a1476}} | {{a1477}} | — |
| train / cpu | {{a1478}} | {{a1479}} | {{a1480}} | {{a1481}} | {{a1482}} | — |
| train / delay | {{a1483}} | {{a1484}} | {{a1485}} | {{a1486}} | {{a1487}} | — |
| travel / disk | {{a1488}} | {{a1489}} | {{a1490}} | {{a1491}} | {{a1492}} | — |
| travel / loss | {{a1493}} | {{a1494}} | {{a1495}} | {{a1496}} | {{a1497}} | {{a1498}}/{{a1499}} |

## Phụ lục B — Phát hiện theo ô: các cờ HP của T-029

Mỗi ô ghi số ca có cờ trên số ca hợp lệ. Ý nghĩa từng cờ ở `results/T-029/ban-do-han-che-phat-hien.md`.

**HP-6** (thuộc G2-H20)

| Ô | BOCPD |
|---|---|
| auth / cpu | {{a1500}}/{{a1501}} |
| auth / delay | {{a1502}}/{{a1503}} |
| order / disk | {{a1504}}/{{a1505}} |
| order / loss | {{a1506}}/{{a1507}} |
| route / mem | {{a1508}}/{{a1509}} |
| route / socket | {{a1510}}/{{a1511}} |
| train / cpu | {{a1512}}/{{a1513}} |
| train / delay | {{a1514}}/{{a1515}} |
| travel / disk | {{a1516}}/{{a1517}} |
| travel / loss | {{a1518}}/{{a1519}} |

**HP-5** (thuộc G2-H21)

| Ô | BOCPD |
|---|---|
| auth / cpu | {{a1520}}/{{a1521}} |
| auth / delay | {{a1522}}/{{a1523}} |
| order / disk | {{a1524}}/{{a1525}} |
| order / loss | {{a1526}}/{{a1527}} |
| route / mem | {{a1528}}/{{a1529}} |
| route / socket | {{a1530}}/{{a1531}} |
| train / cpu | {{a1532}}/{{a1533}} |
| train / delay | {{a1534}}/{{a1535}} |
| travel / disk | {{a1536}}/{{a1537}} |
| travel / loss | {{a1538}}/{{a1539}} |

**HP-7** (thuộc G2-H21)

| Ô | BOCPD |
|---|---|
| auth / cpu | {{a1540}}/{{a1541}} |
| auth / delay | {{a1542}}/{{a1543}} |
| order / disk | {{a1544}}/{{a1545}} |
| order / loss | {{a1546}}/{{a1547}} |
| route / mem | {{a1548}}/{{a1549}} |
| route / socket | {{a1550}}/{{a1551}} |
| train / cpu | {{a1552}}/{{a1553}} |
| train / delay | {{a1554}}/{{a1555}} |
| travel / disk | {{a1556}}/{{a1557}} |
| travel / loss | {{a1558}}/{{a1559}} |

**HP-8** (thuộc G2-H21)

| Ô | BOCPD |
|---|---|
| auth / cpu | {{a1560}}/{{a1561}} |
| auth / delay | {{a1562}}/{{a1563}} |
| order / disk | {{a1564}}/{{a1565}} |
| order / loss | {{a1566}}/{{a1567}} |
| route / mem | {{a1568}}/{{a1569}} |
| route / socket | {{a1570}}/{{a1571}} |
| train / cpu | {{a1572}}/{{a1573}} |
| train / delay | {{a1574}}/{{a1575}} |
| travel / disk | {{a1576}}/{{a1577}} |
| travel / loss | {{a1578}}/{{a1579}} |

**HP-9 (D0)** (thuộc G2-H21)

| Ô | BOCPD | N-Sigma | N-Sigma đối chứng |
|---|---|---|---|
| auth / cpu | {{a1580}}/{{a1581}} | {{a1582}}/{{a1583}} | {{a1584}}/{{a1585}} |
| auth / delay | {{a1586}}/{{a1587}} | {{a1588}}/{{a1589}} | {{a1590}}/{{a1591}} |
| order / disk | {{a1592}}/{{a1593}} | {{a1594}}/{{a1595}} | {{a1596}}/{{a1597}} |
| order / loss | {{a1598}}/{{a1599}} | {{a1600}}/{{a1601}} | {{a1602}}/{{a1603}} |
| route / mem | {{a1604}}/{{a1605}} | {{a1606}}/{{a1607}} | {{a1608}}/{{a1609}} |
| route / socket | {{a1610}}/{{a1611}} | {{a1612}}/{{a1613}} | {{a1614}}/{{a1615}} |
| train / cpu | {{a1616}}/{{a1617}} | {{a1618}}/{{a1619}} | {{a1620}}/{{a1621}} |
| train / delay | {{a1622}}/{{a1623}} | {{a1624}}/{{a1625}} | {{a1626}}/{{a1627}} |
| travel / disk | {{a1628}}/{{a1629}} | {{a1630}}/{{a1631}} | {{a1632}}/{{a1633}} |
| travel / loss | {{a1634}}/{{a1635}} | {{a1636}}/{{a1637}} | {{a1638}}/{{a1639}} |

**HP-1** (thuộc G2-H22)

| Ô | N-Sigma | N-Sigma đối chứng |
|---|---|---|
| auth / cpu | {{a1640}}/{{a1641}} | {{a1642}}/{{a1643}} |
| auth / delay | {{a1644}}/{{a1645}} | {{a1646}}/{{a1647}} |
| order / disk | {{a1648}}/{{a1649}} | {{a1650}}/{{a1651}} |
| order / loss | {{a1652}}/{{a1653}} | {{a1654}}/{{a1655}} |
| route / mem | {{a1656}}/{{a1657}} | {{a1658}}/{{a1659}} |
| route / socket | {{a1660}}/{{a1661}} | {{a1662}}/{{a1663}} |
| train / cpu | {{a1664}}/{{a1665}} | {{a1666}}/{{a1667}} |
| train / delay | {{a1668}}/{{a1669}} | {{a1670}}/{{a1671}} |
| travel / disk | {{a1672}}/{{a1673}} | {{a1674}}/{{a1675}} |
| travel / loss | {{a1676}}/{{a1677}} | {{a1678}}/{{a1679}} |

**HP-2** (thuộc G2-H22)

| Ô | N-Sigma | N-Sigma đối chứng |
|---|---|---|
| auth / cpu | {{a1680}}/{{a1681}} | {{a1682}}/{{a1683}} |
| auth / delay | {{a1684}}/{{a1685}} | {{a1686}}/{{a1687}} |
| order / disk | {{a1688}}/{{a1689}} | {{a1690}}/{{a1691}} |
| order / loss | {{a1692}}/{{a1693}} | {{a1694}}/{{a1695}} |
| route / mem | {{a1696}}/{{a1697}} | {{a1698}}/{{a1699}} |
| route / socket | {{a1700}}/{{a1701}} | {{a1702}}/{{a1703}} |
| train / cpu | {{a1704}}/{{a1705}} | {{a1706}}/{{a1707}} |
| train / delay | {{a1708}}/{{a1709}} | {{a1710}}/{{a1711}} |
| travel / disk | {{a1712}}/{{a1713}} | {{a1714}}/{{a1715}} |
| travel / loss | {{a1716}}/{{a1717}} | {{a1718}}/{{a1719}} |

**HP-3** (thuộc G2-H22)

| Ô | N-Sigma | N-Sigma đối chứng |
|---|---|---|
| auth / cpu | {{a1720}}/{{a1721}} | {{a1722}}/{{a1723}} |
| auth / delay | {{a1724}}/{{a1725}} | {{a1726}}/{{a1727}} |
| order / disk | {{a1728}}/{{a1729}} | {{a1730}}/{{a1731}} |
| order / loss | {{a1732}}/{{a1733}} | {{a1734}}/{{a1735}} |
| route / mem | {{a1736}}/{{a1737}} | {{a1738}}/{{a1739}} |
| route / socket | {{a1740}}/{{a1741}} | {{a1742}}/{{a1743}} |
| train / cpu | {{a1744}}/{{a1745}} | {{a1746}}/{{a1747}} |
| train / delay | {{a1748}}/{{a1749}} | {{a1750}}/{{a1751}} |
| travel / disk | {{a1752}}/{{a1753}} | {{a1754}}/{{a1755}} |
| travel / loss | {{a1756}}/{{a1757}} | {{a1758}}/{{a1759}} |

**HP-4** (thuộc G2-H22)

| Ô | N-Sigma | N-Sigma đối chứng |
|---|---|---|
| auth / cpu | {{a1760}}/{{a1761}} | {{a1762}}/{{a1763}} |
| auth / delay | {{a1764}}/{{a1765}} | {{a1766}}/{{a1767}} |
| order / disk | {{a1768}}/{{a1769}} | {{a1770}}/{{a1771}} |
| order / loss | {{a1772}}/{{a1773}} | {{a1774}}/{{a1775}} |
| route / mem | {{a1776}}/{{a1777}} | {{a1778}}/{{a1779}} |
| route / socket | {{a1780}}/{{a1781}} | {{a1782}}/{{a1783}} |
| train / cpu | {{a1784}}/{{a1785}} | {{a1786}}/{{a1787}} |
| train / delay | {{a1788}}/{{a1789}} | {{a1790}}/{{a1791}} |
| travel / disk | {{a1792}}/{{a1793}} | {{a1794}}/{{a1795}} |
| travel / loss | {{a1796}}/{{a1797}} | {{a1798}}/{{a1799}} |

## Phụ lục C — Chế độ (b), đầu vào bậc thang và schema theo ô (G2-H23, G2-H25, G2-H26)

**G2-H26 — Hit@1 theo ô khi ghép với BOCPD:** tại mốc tiêm / tại báo động đầu sau mốc / tại báo động đầu. Mỗi ô chỉ có ba ca; điểm giữa chọn nhờ nhãn mốc.

| Ô | Số ca | BARO | CIRCA | TORAI B |
|---|---|---|---|---|
| auth / cpu | {{a1800}} | {{a1801:.2f}} / {{a1802:.2f}} / {{a1803:.2f}} | {{a1804:.2f}} / {{a1805:.2f}} / {{a1806:.2f}} | {{a1807:.2f}} / {{a1808:.2f}} / {{a1809:.2f}} |
| auth / delay | {{a1810}} | {{a1811:.2f}} / {{a1812:.2f}} / {{a1813:.2f}} | {{a1814:.2f}} / {{a1815:.2f}} / {{a1816:.2f}} | {{a1817:.2f}} / {{a1818:.2f}} / {{a1819:.2f}} |
| order / disk | {{a1820}} | {{a1821:.2f}} / {{a1822:.2f}} / {{a1823:.2f}} | {{a1824:.2f}} / {{a1825:.2f}} / {{a1826:.2f}} | {{a1827:.2f}} / {{a1828:.2f}} / {{a1829:.2f}} |
| order / loss | {{a1830}} | {{a1831:.2f}} / {{a1832:.2f}} / {{a1833:.2f}} | {{a1834:.2f}} / {{a1835:.2f}} / {{a1836:.2f}} | {{a1837:.2f}} / {{a1838:.2f}} / {{a1839:.2f}} |
| route / mem | {{a1840}} | {{a1841:.2f}} / {{a1842:.2f}} / {{a1843:.2f}} | {{a1844:.2f}} / {{a1845:.2f}} / {{a1846:.2f}} | {{a1847:.2f}} / {{a1848:.2f}} / {{a1849:.2f}} |
| route / socket | {{a1850}} | {{a1851:.2f}} / {{a1852:.2f}} / {{a1853:.2f}} | {{a1854:.2f}} / {{a1855:.2f}} / {{a1856:.2f}} | {{a1857:.2f}} / {{a1858:.2f}} / {{a1859:.2f}} |
| train / cpu | {{a1860}} | {{a1861:.2f}} / {{a1862:.2f}} / {{a1863:.2f}} | {{a1864:.2f}} / {{a1865:.2f}} / {{a1866:.2f}} | {{a1867:.2f}} / {{a1868:.2f}} / {{a1869:.2f}} |
| train / delay | {{a1870}} | {{a1871:.2f}} / {{a1872:.2f}} / {{a1873:.2f}} | {{a1874:.2f}} / {{a1875:.2f}} / {{a1876:.2f}} | {{a1877:.2f}} / {{a1878:.2f}} / {{a1879:.2f}} |
| travel / disk | {{a1880}} | {{a1881:.2f}} / {{a1882:.2f}} / {{a1883:.2f}} | {{a1884:.2f}} / {{a1885:.2f}} / {{a1886:.2f}} | {{a1887:.2f}} / {{a1888:.2f}} / {{a1889:.2f}} |
| travel / loss | {{a1890}} | {{a1891:.2f}} / {{a1892:.2f}} / {{a1893:.2f}} | {{a1894:.2f}} / {{a1895:.2f}} / {{a1896:.2f}} | {{a1897:.2f}} / {{a1898:.2f}} / {{a1899:.2f}} |

**G2-H23 — Bỏ hàng lặp, theo ô:** tổng số điểm đổi của BOCPD trên các ca của ô, và số ca có tập điểm đổi khác bản gốc. Số điểm đổi không phải thước đo chất lượng; mỗi ô chỉ có ba ca.

| Ô | Số ca | Tổng điểm đổi, bản gốc | Nén, hazard theo hàng | Nén, hazard theo thời gian | Ca đổi tập điểm đổi (theo hàng) | Ca đổi tập điểm đổi (theo thời gian) |
|---|---|---|---|---|---|---|
| auth / cpu | {{a1900}} | {{a1901}} | {{a1902}} | {{a1903}} | {{a1904}} | {{a1905}} |
| auth / delay | {{a1906}} | {{a1907}} | {{a1908}} | {{a1909}} | {{a1910}} | {{a1911}} |
| order / disk | {{a1912}} | {{a1913}} | {{a1914}} | {{a1915}} | {{a1916}} | {{a1917}} |
| order / loss | {{a1918}} | {{a1919}} | {{a1920}} | {{a1921}} | {{a1922}} | {{a1923}} |
| route / mem | {{a1924}} | {{a1925}} | {{a1926}} | {{a1927}} | {{a1928}} | {{a1929}} |
| route / socket | {{a1930}} | {{a1931}} | {{a1932}} | {{a1933}} | {{a1934}} | {{a1935}} |
| train / cpu | {{a1936}} | {{a1937}} | {{a1938}} | {{a1939}} | {{a1940}} | {{a1941}} |
| train / delay | {{a1942}} | {{a1943}} | {{a1944}} | {{a1945}} | {{a1946}} | {{a1947}} |
| travel / disk | {{a1948}} | {{a1949}} | {{a1950}} | {{a1951}} | {{a1952}} | {{a1953}} |
| travel / loss | {{a1954}} | {{a1955}} | {{a1956}} | {{a1957}} | {{a1958}} | {{a1959}} |

**G2-H25 — Schema theo ô (đầu vào của BOCPD):** số cột bộ phát hiện nhận và số chiều sau tiền xử lý, từng ca. Bảng mô tả; không tách được ảnh hưởng của schema lên kết quả.

| Ô | Số ca | Số cột nhận (từng ca) | Số chiều sau tiền xử lý (từng ca) |
|---|---|---|---|
| auth / cpu | {{a1960}} | {{a1961}}, {{a1962}}, {{a1963}} | {{a1964}}, {{a1965}}, {{a1966}} |
| auth / delay | {{a1967}} | {{a1968}}, {{a1969}}, {{a1970}} | {{a1971}}, {{a1972}}, {{a1973}} |
| order / disk | {{a1974}} | {{a1975}}, {{a1976}}, {{a1977}} | {{a1978}}, {{a1979}}, {{a1980}} |
| order / loss | {{a1981}} | {{a1982}}, {{a1983}}, {{a1984}} | {{a1985}}, {{a1986}}, {{a1987}} |
| route / mem | {{a1988}} | {{a1989}}, {{a1990}}, {{a1991}} | {{a1992}}, {{a1993}}, {{a1994}} |
| route / socket | {{a1995}} | {{a1996}}, {{a1997}}, {{a1998}} | {{a1999}}, {{a2000}}, {{a2001}} |
| train / cpu | {{a2002}} | {{a2003}}, {{a2004}}, {{a2005}} | {{a2006}}, {{a2007}}, {{a2008}} |
| train / delay | {{a2009}} | {{a2010}}, {{a2011}}, {{a2012}} | {{a2013}}, {{a2014}}, {{a2015}} |
| travel / disk | {{a2016}} | {{a2017}}, {{a2018}}, {{a2019}} | {{a2020}}, {{a2021}}, {{a2022}} |
| travel / loss | {{a2023}} | {{a2024}}, {{a2025}}, {{a2026}} | {{a2027}}, {{a2028}}, {{a2029}} |
