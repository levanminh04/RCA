# Gói trình G2 (T-034): baseline trên dev, bản đồ hạn chế, căn cứ cho bước đồ thị

Ngày 13/10/2026. Người làm: Claude. Người phản biện kết quả: Codex. Trạng thái: chờ phản biện, chờ Minh duyệt.

**Minh cần duyệt gì ở cổng này** (MRP §7, cổng G2): bảng baseline trên dev (mục 2) và bản đồ hạn chế (mục 3). Các điểm cần quyết thêm nằm ở mục 8.

**Cách đọc.**

- Mọi số là trên phần **dev**: 30 ca RE2-TT (hệ Train Ticket) và 22 ca Nezha-OB (hệ Online Boutique). Chưa mở test và dataset giữ ngoài.
- *Root* là thành phần gốc gây lỗi theo nhãn. *Ô* là một cặp (root, loại lỗi). *Chế độ (a)*: phương pháp xếp hạng được cho biết mốc tiêm lỗi. *Chế độ (b)*: bộ phát hiện tự báo động, rồi phương pháp xếp hạng chạy tại báo động đầu.
- *Hit@1* là tỷ lệ ca root đứng hạng 1; khi hòa thì tính kỳ vọng. Ca không chạy được vẫn nằm trong mẫu số và tính trượt.
- Mỗi kết luận ghi một **mức bằng chứng** (WHY-51): **CT** can thiệp (đổi có kiểm soát một đầu vào hay một bước, xem đầu ra của chính phương pháp); **ĐC** đo trực tiếp đại lượng mà cơ chế giả định; **LĐ** liên hệ có đối chứng; **MT** mô tả; **CK** chưa kiểm.
- Câu “vì sao” có ba trạng thái: *đã xác lập ở mức X*, *đã loại giải thích Y*, *chưa phân xử vì Z*.
- Mọi con số trong file này được điền bằng máy từ file kết quả. Sổ (file, con trỏ JSON) của từng số: `results/T-034/runs/g2-build-001/render/registry.json`. Kết quả kiểm: `results/T-034/runs/g2-build-001/v4.json`.

## 0. Tóm tắt ba câu

**Câu 1 — Phương pháp nào tốt trong điều kiện nào.** Chỉ đọc theo ô và theo ca (mục 2).

- *RE2-TT, chế độ (a).* Theo điểm ước lượng, hai dòng đầu bảng là TORAI B (Hit@1 0,867) và SimpleRCA (0,833); khoảng bootstrap của bốn phương pháp đứng đầu chồng nhau, nên thứ tự giữa chúng chưa chắc. SimpleRCA không dùng quan hệ gọi; ở TORAI B bước nhân quả không tham gia xếp root (G2-H15). TORAI B đúng mọi ca ở 7/10 ô, SimpleRCA ở 7, BARO ở 5, TraceRCA ở 3, CIRCA ở 2, MicroRank ở 0.
- *Không phương pháp nào tốt ở mọi ô.* Ở ô auth/delay BARO không đúng ca nào, trong khi SimpleRCA, TraceRCA và TORAI B đúng cả ba. Ở ô train/delay thì ngược lại: SimpleRCA chỉ đúng một ca, BARO và TORAI B đúng cả ba. Ở ô order/loss TraceRCA không đúng ca nào.
- *Nezha-OB, chế độ (a).* Mọi phương pháp chạy được đều yếu: BARO 0,364, SimpleRCA 0,318, TraceRCA 0,106, MicroRank 0,000. CIRCA và TORAI B không chạy được trên dữ liệu này (Q-85). Với lỗi return, BARO, SimpleRCA và TraceRCA đúng 0, 0 và 0 trên 4 ca. Với lỗi trễ mạng: 0, 1 và 0 trên 6 ca.
- *Chế độ (b), RE2-TT.* Báo động đầu nằm ở hoặc sau mốc tiêm ở 3/30 ca với BOCPD và 0/30 ca với N-Sigma. Vì vậy thành công chung (phát hiện đúng rồi xếp đúng) cao nhất chỉ 0,067.

**Câu 2 — Thất bại ở đâu.** Bản đồ ở mục 3 có 26 dòng. Tách theo nguồn:

- *Do bản cài trong thư viện hoặc đầu vào ta dựng:* bước chia trace của MicroRank (G2-H01); cách TraceRCA bản thư viện chấm thời gian chờ (G2-H03, G2-H04); bảng log của TORAI nguồn B (G2-H14); tiền xử lý nhìn cả bản ghi của BOCPD (G2-H20).
- *Do cách tính của phương pháp:* thang IQR của BARO (G2-H09); phiếu metric đếm theo mẫu của SimpleRCA (G2-H08); phần dư gần bằng không và bước cộng điểm lên nút cha của CIRCA (G2-H12, G2-H13).
- *Do dữ liệu:* nền ngắn và metric thưa ở Nezha-OB; root không được dịch vụ nào gọi; không có onset và nền sạch được xác nhận độc lập (G2-H19, G2-H24).
- *Chưa phân xử:* vì sao hai bộ phát hiện báo trước mốc (G2-H21, G2-H22); vì sao dịch vụ không liên hệ với root đổi tại mốc (G2-H11); câu “lan có đáng kể” (mục 4).

**Câu 3 — Hạn chế nào cần bước đồ thị (P5/P6) giải quyết.** Mục 5 trình các ứng viên, chưa chọn.

- Có căn cứ ở mức CT hoặc ĐC để **đề xuất thử**: gắn thời gian lời gọi lên cạnh và tính cho dịch vụ được gọi; tách phần thời gian tự xử lý theo quan hệ cha–con của span; tiêu chí “yêu cầu bất thường” theo cả cây lời gọi; chặn giá trị không hợp lệ trước khi lan điểm.
- **Chưa** có căn cứ để nói đồ thị sẽ giúp. Phần lớn cặp sai của MicroRank và BARO không nằm phía trên root (24/252 và 15/162 cặp nằm phía trên). Hiện tượng “dịch vụ gọi chờ root” có cả ở ca đúng (83/96).
- Trên RE2-TT, mốc phải vượt ở P7 là baseline tốt nhất của P3 (Q-62), hiện là TORAI B và SimpleRCA.

## 1. K1 — Sáu câu của cổng (MRP §7) và năm đầu ra của P4

1. **Phục vụ câu nào của cô hoặc DT18?** Hai việc trong chuỗi cô yêu cầu: “mở rộng thực nghiệm ra các dataset public khác” (P3) và “chỉ ra vấn đề còn tồn đọng, hạn chế của các phương pháp đã có” (P4). Đây là bước nối sang “tiếp cận phương pháp đồ thị”. Theo DT18 (đoạn nhiệm vụ thứ ba): thực nghiệm trên dữ liệu công khai trước, và “phân tích các trường hợp phương pháp hoạt động hiệu quả hoặc còn hạn chế”.
2. **Dữ liệu có phân xử nổi không?** Một phần.
   - Phân xử được ở mức tính toán: bước nào của từng phương pháp làm đổi thứ hạng (các dòng mức CT ở mục 3).
   - Phân xử yếu: RE2-TT chỉ có năm root; Nezha-OB có nền trace ngắn và rất ít mẫu metric, CIRCA và TORAI B không chạy được.
   - Không phân xử được bằng dữ liệu hiện có: vì sao bộ phát hiện báo trước mốc (không có onset và nền sạch độc lập); vì sao dịch vụ không liên hệ đổi tại mốc (không có ánh xạ dịch vụ–máy); việc “dịch vụ gọi chờ root” ở 15/52 ca.
   - Eadro-TT chưa được dùng tới G2 (Q-83).
3. **Baseline đủ mạnh chưa?** Trên RE2-TT: có, và mạnh nhất là hai phương pháp không dựa vào quan hệ gọi. Trên Nezha-OB: chỉ bốn phương pháp chạy được, đều yếu. Ba điểm phải nói kèm: (i) TraceRCA và MicroRank đang dùng là bản trong thư viện RCAEval, khác bài gốc ở những bước quyết định (G2-H01, G2-H03); (ii) nhánh mã tác giả TraceRCA mới là chẩn đoán, chưa là baseline (mục 2.8, mục 8); (iii) trạng thái tái lập từng phương pháp ở mục 2.7, có phương pháp chưa tái lập được số công bố.
4. **Giá trị trung gian có hợp lý không?** Đã soi và thấy năm chỗ bất thường, đều đã lần tới bước gây ra: điểm cực lớn của CIRCA (G2-H12); khoảng một nửa trace bị MicroRank xếp bất thường (G2-H01); bảng log của TORAI B dồn điểm (G2-H14); thứ tự chứa giá trị không hữu hạn của TraceRCA (đã xử lý ở giao thức, WHY-32); underflow của BOCPD (phép E2). Số tổng của bảng baseline được tính lại độc lập từ bản ghi từng lượt: 0 lệch.
5. **Đã tách theo điều kiện và theo ca chưa?** Rồi: bảng theo ô ở mục 2.2 và 2.4, Phụ lục A và B; bảng theo ca nằm trong các file nguồn được dẫn.
6. **Còn lựa chọn nào chưa có câu trả lời “tại sao”?** Các lựa chọn của gói này có ở WHY-51. Các lựa chọn **chưa quyết** nằm ở mục 8: nhánh mã tác giả TraceRCA; có định nghĩa nhãn lan không; cách trình bốn ca ERROR; TORAI nguồn B; dòng độ nhạy MicroRank.

**Năm đầu ra của P4** (MRP mục P4) nằm ở đâu trong gói:

1. **Hạn chế đã xác nhận và điều kiện** (mức CT hoặc ĐC ở ít nhất một nguồn con): G2-H01, G2-H02, G2-H03, G2-H04, G2-H05, G2-H06, G2-H08, G2-H09, G2-H12, G2-H13, G2-H14, G2-H16, G2-H19, G2-H20, G2-H21, G2-H23, G2-H26. Điều kiện của từng dòng ghi ở trường “Vì sao” và “Giải thích khác”.
2. **Thuộc bản cài, đầu vào do ta dựng, giao thức hoặc thiếu dữ liệu** (loại A, G, D): G2-H01, G2-H03, G2-H04, G2-H05, G2-H06, G2-H07, G2-H08, G2-H10, G2-H11, G2-H13, G2-H14, G2-H15, G2-H16, G2-H17, G2-H19, G2-H20, G2-H21, G2-H23, G2-H24, G2-H25, G2-H26.
3. **Thuộc giả định hoặc cách tính của phương pháp** (loại M): G2-H02, G2-H05, G2-H06, G2-H07, G2-H08, G2-H09, G2-H10, G2-H12, G2-H13, G2-H17, G2-H21, G2-H22, G2-H23, G2-H26.
4. **Quan hệ giữa dịch vụ có thể bổ sung thông tin gì:** mục 5 (ứng viên), không phải bằng chứng đồ thị đã giúp.
5. **Câu chưa trả lời** (dòng còn phần “chưa phân xử”): G2-H01, G2-H02, G2-H05, G2-H06, G2-H07, G2-H09, G2-H10, G2-H11, G2-H13, G2-H15, G2-H17, G2-H18, G2-H20, G2-H21, G2-H22, G2-H23, G2-H24, G2-H25, G2-H26; chi tiết và nơi phân xử ở mục 6.

## 2. K2 — Bảng baseline trên dev

Bảng chính lấy nguyên số của T-024, T-025, T-026 (đã khóa); gói này không chạy lại phương pháp nào để thay bảng. Số máy đọc: `results/T-034/bang-baseline.json`. Phép kiểm V2 tính lại mọi số tổng từ bản ghi từng lượt bằng một bộ chấm viết riêng: PASS, 0 lệch.

### 2.1 Xếp hạng, chế độ (a), RE2-TT (30 ca, 10 ô)

| Phương pháp | Trạng thái (số ca) | Hit@1 | Khoảng bootstrap của Hit@1 | Hit@3 | Hit@5 | MRR | NDCG@5 | Avg@5 | Retrieval@5 | Rerank@1 (K=5) |
|---|---|---|---|---|---|---|---|---|---|---|
| BARO | OK: 30 | 0,700 | [0,47; 0,90] | 0,800 | 0,867 | 0,768 | 0,787 | 0,800 | 0,867 | 0,808 |
| SimpleRCA | OK: 30 | 0,833 | [0,67; 1,00] | 0,967 | 0,967 | 0,891 | 0,909 | 0,927 | 0,967 | 0,862 |
| MicroRank | OK: 26, ERROR: 4 | 0,067 | [0,00; 0,20] | 0,433 | 0,433 | 0,257 | 0,267 | 0,313 | 0,433 | 0,154 |
| TraceRCA | OK: 26, ERROR: 4 | 0,700 | [0,50; 0,87] | 0,800 | 0,833 | 0,756 | 0,773 | 0,787 | 0,833 | 0,840 |
| CIRCA | OK: 30 | 0,533 | [0,30; 0,73] | 0,600 | 0,900 | 0,641 | 0,700 | 0,700 | 0,900 | 0,593 |
| TORAI B | OK: 30 | 0,867 | [0,70; 1,00] | 1,000 | 1,000 | 0,917 | 0,938 | 0,953 | 1,000 | 0,867 |

Khoảng bootstrap lấy mẫu theo ô, mức 95%. Avg@5 là trung bình AC@1 đến AC@5 theo cách của RCAEval. Retrieval@5 là tỷ lệ ca root lọt vào năm hạng đầu; Rerank@1 là tỷ lệ root hạng 1 trong các ca đó (Q-65).

Khoảng của BARO, SimpleRCA, TraceRCA và TORAI B chồng nhau: với 30 ca, bảng không phân định được thứ tự giữa bốn phương pháp này.

MicroRank và TraceRCA mỗi phương pháp có 4 ca dừng lỗi, tính trượt. CIRCA: 11 ca có nút điểm cực lớn (G2-H12), báo riêng ở mục 2.3.

### 2.2 RE2-TT theo ô: số ca root hạng 1 (kỳ vọng khi hòa) trên số ca

| Ô (root / loại lỗi) | Số ca | BARO | SimpleRCA | MicroRank | TraceRCA | CIRCA | TORAI B |
|---|---|---|---|---|---|---|---|
| auth / cpu | 3 | 1 | 3 | 0 | 3 | 2 | 1 |
| auth / delay | 3 | 0 | 3 | 2 | 3 | 0 | 3 |
| order / disk | 3 | 3 | 3 | 0 | 2 | 3 | 3 |
| order / loss | 3 | 2 | 2 | 0 | 0 | 2 | 2 |
| route / mem | 3 | 2 | 3 | 0 (ERROR: 1) | 2 (ERROR: 1) | 2 | 3 |
| route / socket | 3 | 3 | 3 | 0 (ERROR: 1) | 2 (ERROR: 1) | 1 | 3 |
| train / cpu | 3 | 3 | 3 | 0 | 3 | 0 | 3 |
| train / delay | 3 | 3 | 1 | 0 (ERROR: 1) | 2 (ERROR: 1) | 1 | 3 |
| travel / disk | 3 | 3 | 3 | 0 | 2 | 3 | 3 |
| travel / loss | 3 | 1 | 1 | 0 (ERROR: 1) | 2 (ERROR: 1) | 2 | 2 |

### 2.3 Nhóm ca theo Q-82: 19 ca CIRCA không có nút điểm cực lớn

| Phương pháp | Trạng thái (số ca) | Hit@1 | Khoảng bootstrap của Hit@1 | Hit@3 | Hit@5 | MRR | NDCG@5 | Avg@5 | Retrieval@5 | Rerank@1 (K=5) |
|---|---|---|---|---|---|---|---|---|---|---|
| BARO | OK: 19 | 0,579 | [0,33; 0,85] | 0,737 | 0,842 | 0,683 | 0,717 | 0,737 | 0,842 | 0,688 |
| SimpleRCA | OK: 19 | 0,842 | [0,62; 1,00] | 0,947 | 0,947 | 0,889 | 0,902 | 0,916 | 0,947 | 0,889 |
| MicroRank | OK: 18, ERROR: 1 | 0,105 | [0,00; 0,30] | 0,316 | 0,316 | 0,260 | 0,224 | 0,253 | 0,316 | 0,333 |
| TraceRCA | OK: 18, ERROR: 1 | 0,684 | [0,42; 0,94] | 0,842 | 0,895 | 0,773 | 0,800 | 0,821 | 0,895 | 0,765 |
| CIRCA | OK: 19 | 0,684 | [0,41; 0,93] | 0,789 | 0,842 | 0,748 | 0,766 | 0,779 | 0,842 | 0,812 |
| TORAI B | OK: 19 | 0,842 | [0,65; 1,00] | 1,000 | 1,000 | 0,895 | 0,921 | 0,937 | 1,000 | 0,842 |

Nhóm 19 ca này được chọn từ đầu ra của CIRCA, không phải mẫu ngẫu nhiên; cùng một tập cho mọi phương pháp (WHY-36). Trên nhóm này CIRCA đạt 0,684, so với 0,533 trên cả 30 ca.

### 2.4 Xếp hạng, chế độ (a), Nezha-OB (22 ca, 13 ô)

| Phương pháp | Trạng thái (số ca) | Hit@1 | Khoảng bootstrap của Hit@1 | Hit@3 | Hit@5 | MRR | NDCG@5 | Avg@5 | Retrieval@5 | Rerank@1 (K=5) |
|---|---|---|---|---|---|---|---|---|---|---|
| BARO | OK: 22 | 0,364 | [0,14; 0,62] | 0,545 | 0,727 | 0,527 | 0,551 | 0,573 | 0,727 | 0,500 |
| SimpleRCA | OK: 22 | 0,318 | [0,09; 0,57] | 0,682 | 0,841 | 0,538 | 0,597 | 0,632 | 0,841 | 0,378 |
| MicroRank | OK: 22 | 0,000 | [0,00; 0,00] | 0,091 | 0,364 | 0,170 | 0,153 | 0,118 | 0,364 | 0,000 |
| TraceRCA | OK: 22 | 0,106 | [0,00; 0,25] | 0,455 | 0,523 | 0,330 | 0,332 | 0,368 | 0,523 | 0,203 |
| CIRCA | UNSUPPORTED: 22 | không chạy được |  |  |  |  |  |  |  |  |
| TORAI B | UNSUPPORTED: 22 | không chạy được |  |  |  |  |  |  |  |  |

| Ô (root / loại lỗi) | Số ca | BARO | SimpleRCA | MicroRank | TraceRCA | CIRCA | TORAI B |
|---|---|---|---|---|---|---|---|
| ad / cpu_contention | 1 | 1 | 1 | 0 | 0 | — | — |
| checkout / exception | 2 | 1 | 0 | 0 | 0 | — | — |
| checkout / network_delay | 2 | 0 | 1 | 0 | 0 | — | — |
| checkout / return | 2 | 0 | 0 | 0 | 0 | — | — |
| email / cpu_consumed | 1 | 1 | 0 | 0 | 0,333 | — | — |
| email / network_delay | 2 | 0 | 0 | 0 | 0 | — | — |
| frontend / return | 2 | 0 | 0 | 0 | 0 | — | — |
| payment / cpu_contention | 2 | 2 | 2 | 0 | 0 | — | — |
| productcatalog / exception | 1 | 0 | 1 | 0 | 0 | — | — |
| recommendation / cpu_consumed | 2 | 1 | 0 | 0 | 1 | — | — |
| recommendation / network_delay | 2 | 0 | 0 | 0 | 0 | — | — |
| shipping / cpu_consumed | 1 | 0 | 0 | 0 | 1 | — | — |
| shipping / cpu_contention | 2 | 2 | 2 | 0 | 0 | — | — |

Hai dataset khác nhịp metric và độ dài nền (WHY-37); so giữa hai dataset chỉ để mô tả.

### 2.5 Phát hiện, chế độ (b), RE2-TT

| Bộ phát hiện | Precision | Recall | F1 | Báo động trên đoạn bình thường theo nhãn proxy | Mỗi giờ bình thường | Độ trễ từ mốc tiêm, giây: trung vị (nhỏ nhất–lớn nhất) | Ca có báo động đầu ở hoặc sau mốc |
|---|---|---|---|---|---|---|---|
| BOCPD | 0,662 | 0,478 | 0,555 | 143 / 21.570 giây | 23,9 | 34 (2–317) | 3/30 |
| N-Sigma (bộ cột chính) | 0,562 | 0,833 | 0,671 | 6.033 / 18.600 giây | 1167,7 | 9 (0–54) | 0/30 |
| N-Sigma (bộ cột đối chứng) | 0,545 | 1,000 | 0,706 | 18.409 / 18.600 giây | 3563,0 | 0 (0–0) | 0/30 |

**Phải đọc kèm ba điều.**

- Nhãn dùng để chấm là nhãn proxy của giao thức (WHY-35): từ mốc tiêm tới cuối file là “bất thường”. Dataset không xác nhận độc lập đoạn trước mốc là khỏe, lúc lỗi bắt đầu có tác động, hay lúc hết lỗi.
- Vì vậy “báo động trên đoạn bình thường” **không** phải tỷ lệ báo động sai trong vận hành thật, và độ trễ là tính từ **mốc tiêm**, không phải từ lúc sự cố bắt đầu biểu hiện.
- Precision, Recall, F1 tính theo cửa sổ 60 giây.

Theo ô:

| Ô (root / loại lỗi) | Số ca | BOCPD: ca có báo động đầu ở hoặc sau mốc | N-Sigma: ca có báo động đầu ở hoặc sau mốc |
|---|---|---|---|
| auth / cpu | 3 | 1 | 0 |
| auth / delay | 3 | 0 | 0 |
| order / disk | 3 | 0 | 0 |
| order / loss | 3 | 1 | 0 |
| route / mem | 3 | 0 | 0 |
| route / socket | 3 | 0 | 0 |
| train / cpu | 3 | 1 | 0 |
| train / delay | 3 | 0 | 0 |
| travel / disk | 3 | 0 | 0 |
| travel / loss | 3 | 0 | 0 |

**Độ nhạy theo điểm cuối D** (T-033; không chấm lại): số ca BOCPD có ít nhất một điểm đổi trong D giây sau mốc là 12, 23, 27, 29, 30 trên 30 ca, với D lần lượt `30`, `60`, `120`, `300`, `600`. D không phải thời điểm hết lỗi.

### 2.6 Chế độ (b): xếp hạng tại báo động đầu, và bảng điểm chạy

| Ghép | Ca có báo động đầu đúng | Thành công chung Hit@1 | Thành công chung Hit@5 | Hit@1 khi chạy tại mốc tiêm | Hit@1 tại báo động đầu sau mốc | Hit@1 tại báo động đầu |
|---|---|---|---|---|---|---|
| BARO + BOCPD | 3/30 | 0,067 | 0,100 | 0,700 | 0,633 | 0,267 |
| BARO + N-Sigma | 0/30 | 0,000 | 0,000 | 0,700 | 0,700 | 0,033 |
| CIRCA + BOCPD | 3/30 | 0,000 | 0,033 | 0,533 | 0,133 | 0,133 |
| CIRCA + N-Sigma | 0/30 | 0,000 | 0,000 | 0,533 | 0,300 | 0,033 |
| TORAI B + BOCPD | 3/30 | 0,000 | 0,067 | 0,867 | 0,400 | 0,233 |
| TORAI B + N-Sigma | 0/30 | 0,000 | 0,000 | 0,867 | 0,700 | 0,033 |

- “Thành công chung” đòi báo động đầu đúng **và** root trong k hạng đầu.
- Ba cột cuối (bảng G của T-029) cho cùng một phương pháp xếp hạng chạy ở ba điểm. Cột giữa chọn báo động nhờ nhãn mốc, nên chỉ là chẩn đoán, không phải cận trên.
- BARO ghép BOCPD: trong 18 ca báo động đầu cách xa mốc, Hit@1 tại báo động đầu là 0,000, so với 0,667 khi chạy tại mốc tiêm.

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
| Nezha-OB | ms | 1 | 22 | OK: 16, NO_EVIDENCE: 6 | 10 | 11 | 12 | 0 |
| Nezha-OB | ms | 3 | 22 | OK: 13, NO_EVIDENCE: 9 | 9 | 9,5 | 10 | 0 |
| Nezha-OB | us | 1 | 22 | OK: 16, NO_EVIDENCE: 6 | 10 | 11 | 12 | 0 |
| Nezha-OB | us | 3 | 22 | OK: 13, NO_EVIDENCE: 9 | 9 | 9,5 | 10 | 0 |
| RE2-TT | ms | 1 | 30 | OK: 29, NO_EVIDENCE: 1 | 17 | 17 | 17 | 0 |
| RE2-TT | ms | 3 | 30 | OK: 25, NO_EVIDENCE: 5 | 15 | 15 | 15 | 2 |
| RE2-TT | us | 1 | 30 | OK: 29, NO_EVIDENCE: 1 | 17 | 17 | 17 | 0 |
| RE2-TT | us | 3 | 30 | OK: 25, NO_EVIDENCE: 5 | 15 | 15 | 15 | 2 |

Để đặt cạnh, trên cùng mẫu số: BARO ở Nezha-OB đúng 8 ca kỳ vọng; TORAI B ở RE2-TT đúng 26 ca kỳ vọng. Các số của nhánh này lấy từ đầu ra đã lưu của gói bổ sung T-032; không chọn ngưỡng theo điểm dev. Đây là dev đã nhìn, chưa có khoảng tin cậy.

**MicroRank với bộ chia theo công thức của bài gốc.** Chỉ thay bước chia trace; span đầu của yêu cầu do ta quy ước. Không phải MicroRank gốc.

| Dataset | Nhánh bộ chia | Số ca | Ca xét được | Ca hạng 1, bản thư viện (trên các ca xét được) | Ca hạng 1, sau khi thay bộ chia |
|---|---|---|---|---|---|
| RE2-TT | `mo15`: luật của bài | 30 | 25 | 2 | 14 |
| RE2-TT | `mo1p50`: luật chia nhóm trong mã của tác giả | 30 | 25 | 2 | 15 |
| Nezha-OB | `mo15`: luật của bài | 22 | 22 | 0 | 7 |
| Nezha-OB | `mo1p50`: luật chia nhóm trong mã của tác giả | 22 | 22 | 0 | 7 |

### 2.9 Đọc bảng theo điều kiện

Chỉ nêu điều thấy ở từng ô; một ô ba ca không phải mẫu hình.

- **Theo loại lỗi ở RE2-TT.** Lỗi đĩa (6 ca): BARO 6, SimpleRCA 6, CIRCA 6, TORAI B 6, TraceRCA 4. Lỗi mất gói: không phương pháp nào vượt 4/6. Lỗi trễ mạng: BARO 3, SimpleRCA 4, TraceRCA 5, TORAI B 6 trên 6 ca.
- **Theo root ở RE2-TT.** Với root `ts-auth-service` (không được dịch vụ nào gọi trong trace): BARO 1, SimpleRCA 6, TraceRCA 6, TORAI B 4 trên 6 ca.
- **Nezha-OB.** Lỗi tranh chấp CPU: BARO và SimpleRCA đúng 5 và 5 trên 5 ca; TraceRCA 0. Lỗi return và trễ mạng: gần như không phương pháp nào đúng (xem câu 1 ở mục 0).
- **Phát hiện.** Không ô nào có quá một ca BOCPD báo động đầu đúng; N-Sigma không có ca nào.

## 3. K3 — Bản đồ hạn chế hợp nhất

Bản đồ gộp bốn nguồn: mã HP của T-029 (phát hiện), mã M của T-028 (cờ cơ chế xếp hạng), mã H và D của T-032 (nguyên nhân xếp hạng và giới hạn dữ liệu), cùng các câu hỏi KT của T-032 và K của T-033 trong sổ đối chiếu của gói bổ sung. Với H6, H8, CIRCA và KT11, bản đồ dùng **trạng thái đã đính chính ngày 13/10**, không dùng câu cũ.

- Bản máy đọc: `results/T-034/ban-do-g2.json` (mỗi dòng có mã gốc, mức, số kèm con trỏ nguồn, bảng theo ô).
- Phép kiểm V3: 68/68 mã gốc có mặt trong ít nhất một dòng hoặc trong danh sách “không đưa vào”; 26 dòng của sổ đối chiếu đều có chỗ. Kết quả: PASS.
- Các dòng **chồng nhau** trên cùng một ca. Không cộng các dòng thành tỷ lệ nguyên nhân.
- Loại nguồn hạn chế: **D** dữ liệu hoặc thiếu đầu vào; **G** giao thức đánh giá; **A** bản cài, adapter hoặc đầu vào do ta dựng; **M** giả định hoặc cách tính của phương pháp.

### 3.1 Bảng tóm tắt

| Mã | Hạn chế | Chế độ | Mức cao nhất | Loại nguồn | Trạng thái của câu “vì sao” | Mã gốc |
|---|---|---|---|---|---|---|
| G2-H01 | MicroRank (bản RCAEval): bước chia trace bất thường/bình thường | (a) | CT | A | Đã xác lập; Chưa phân xử | H1, T-032:KT1 |
| G2-H02 | MicroRank: đếm phủ của spectrum và trọng số PageRank | (a) | CT | M | Đã xác lập; Chưa phân xử | H2, H3, T-032:KT3 |
| G2-H03 | TraceRCA (bản RCAEval): thời gian chờ root được chấm thành bất thường của dịch vụ gọi | (a) | CT | A | Đã xác lập | H4, T-032:KT2, T-032:KT13 |
| G2-H04 | TraceRCA (bản RCAEval): điểm đi theo số span mang cờ tuyệt đối | (a) | CT | A | Đã xác lập; Đã loại | H5, T-032:KT4 |
| G2-H05 | TraceRCA cài theo lời văn của bài: dịch vụ gọi hoặc frontend đứng trên root | (a) | CT | M + A | Đã loại; Đã xác lập; Chưa phân xử | H6, T-032:KT11 |
| G2-H06 | Trễ mạng: dấu hiệu nằm ở span phía gọi của lời gọi tới root | (a) | ĐC | M + D | Đã xác lập; Chưa phân xử | H7, T-032:KT5 |
| G2-H07 | Lỗi return ở Nezha-OB: root không hạng 1 dù có dấu hiệu | (a) | LĐ | M + A + D | Đã loại; Chưa phân xử | H8, M6 |
| G2-H08 | SimpleRCA: phiếu metric đếm theo mẫu lấn át trace và log | (a) | CT | A + M | Đã xác lập | H9 |
| G2-H09 | BARO: chia cho IQR của nền gần phẳng | (a) | CT | M | Đã xác lập; Đã loại; Chưa phân xử | H10, T-032:KT12 |
| G2-H10 | Kênh bộ nhớ trôi ngay trong đoạn nền | (a) | MT | D + M | Chưa phân xử | H11 |
| G2-H11 | Thực thể đứng trên root phần lớn nằm ngoài chuỗi gọi qua root | (a) | MT | D | Chưa phân xử | H12, T-032:KT6 |
| G2-H12 | CIRCA: phần dư gần bằng không cho điểm cực lớn, bước DA cộng nó sang tổ tiên | (a) | CT | M | Đã xác lập | H13, H14, M4, T-032:KT15 |
| G2-H13 | CIRCA: hồi quy theo nút cha làm điểm cao hơn bản không cạnh; nhạy với cửa sổ | (a) | CT | M + G | Đã xác lập; Đã loại; Chưa phân xử | H15, T-032:KT9 |
| G2-H14 | TORAI nguồn B: bảng log do ta dựng dồn điểm về vài dịch vụ | (a) | CT | A | Đã xác lập | H16, T-032:KT7 |
| G2-H15 | TORAI: bước nhân quả (RCD) không quyết định vị trí root | (a) | MT | A | Chưa phân xử | H17 |
| G2-H16 | Rào cản tập ứng viên, hòa cắt biên và ca dừng lỗi vì thao tác thiếu nền | (a) | CT | D + G | Đã xác lập | M1, M2, M3, D4, T-032:KT8 |
| G2-H17 | Dịch vụ phía trên đứng trước root (cờ M5) và câu “lan có đáng kể” | (a) | LĐ | M + D | Chưa phân xử | M5, T-032:KT10 |
| G2-H18 | Ca sai chưa gắn được cờ cơ chế nào (M0) | (a) | MT | chưa xếp | Chưa phân xử | M0 |
| G2-H19 | Giới hạn của dữ liệu trace và metric | (a) | ĐC | D | Đã xác lập | D1, D2, D3, D5, D6, D7 |
| G2-H20 | BOCPD: tiền xử lý trên cả bản ghi làm vị trí báo đầu phụ thuộc dữ liệu sau mốc | (b) | CT | A + G | Đã xác lập; Chưa phân xử | HP-6, T-033:K4 |
| G2-H21 | BOCPD: có báo động trước mốc; nhạy với prior; underflow số học | (b) | CT | M + A + D | Chưa phân xử; Đã loại; Đã xác lập | HP-5, HP-7, HP-8, HP-9, T-033:K3 |
| G2-H22 | N-Sigma: báo dày ngay trên đoạn nền | (b) | LĐ | M | Chưa phân xử; Đã xác lập | HP-1, HP-2, HP-3, HP-4, HP-14, T-033:K2 |
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
- **Số:** Hạng 1: 2/30 ca RE2-TT (4 ca ERROR) và 0/22 ca Nezha-OB. Thay riêng bước chia bằng công thức của bài gốc (hai biến thể `mo15` và `mo1p50`): hạng 1 từ 2 lên 21–22 trên 47 ca xét được; 176–177/243 cặp (thực thể đứng trên root, root) mất. Tỷ lệ trace bất thường ở RE2-TT (trung vị): 50% xuống 10%. Mốc giả không có lỗi: vẫn 36,6% trace bị xếp bất thường (trung vị 26 ca RE2-TT).
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
- **Số:** Đếm riêng thay đếm phủ: hạng 1 từ 2 lên 19 trên 48 ca; 115/252 cặp mất; 5 ca root giảm hạng. Trọng số đơn vị: hạng 1 từ 2 lên 11; 28/252 cặp mất; 12 ca tăng hạng, 5 ca giảm.
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
- **Số:** Trong các cặp (dịch vụ phía trên đứng trên root) xét được, từ một nửa span mang cờ trở lên là span bao lời gọi chậm tới root: 4/4 cặp RE2-TT, 9/15 cặp Nezha-OB. Ở ca **đúng** của RE2-TT cũng vậy: 83/96 dịch vụ phía trên. Đổi cờ sang phần span không do span con phủ: số ca có dịch vụ gọi trên root 4 → 2 (RE2-TT), 16 → 15 (Nezha-OB). Mốc giả so mốc thật: tỷ lệ span mang cờ ở thao tác phía trên root 0,8% → 6,2%; ở thao tác không liên hệ 1,1% → 1,2%.
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
- **Số:** Xếp theo tỷ lệ a/n: 11/15 cặp RE2-TT và 43/75 cặp Nezha-OB mất, nhưng 11/21 ca đang đúng của RE2-TT mất hạng 1. Xếp theo số tuyệt đối a: giữ 14/15 và 68/75 cặp.
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
- **Số:** 13 cặp thuộc 11 ca; 12 cặp có quan hệ cũ. Mã tác giả, ngưỡng chọn đặc trưng bằng một: root trên 3/4 cặp RE2-TT (trong đó 2 do dịch vụ gọi nhận điểm mặc định) và 7/8 cặp Nezha-OB. **Phép E1** (chỉ đổi quy tắc pattern, giữ mọi thứ khác của bản cài theo lời văn): ở cờ một lần độ lệch chuẩn, 1/7 cặp Nezha-OB có hiện tượng đổi chiều và 0/3 cặp RE2-TT; ở cờ ba lần, 4/5 cặp Nezha-OB và 0/3 cặp RE2-TT.
- **Vì sao:** Đã loại ở mức CT, trong 13 cặp đã khai: ở cờ một lần độ lệch chuẩn (mặc định của bài), việc chấm qua tập nhiều dịch vụ không phải bước đưa dịch vụ gọi lên trên root. Đã xác lập ở mức CT rằng ở cờ ba lần nó là bước quyết định ở phần lớn cặp Nezha-OB. Chưa phân xử bước gây chênh giữa hai pipeline ở cờ một lần; trung gian của E1 chỉ ra hai ứng viên: frontend mang cờ lời gọi đi ra ở gần như mọi trace bất thường, và ở RE2-TT tập chỉ gồm root bị bước chọn tập theo điểm loại.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: phép E1 của T-034 (hai-phep-kiem.md) — CT; đối chiếu các cặp với mã tác giả (bản đính chính ngày 13/10) — MT; đọc bài và mã (thiết kế E1 mục 2) — MT.
- **Loại nguồn hạn chế:** M + A.
- **Giải thích khác còn lại:** Hai pipeline còn khác ở cách dựng lời gọi, chọn đặc trưng theo cặp, chuẩn nền và cách chọn tập; E1 không đụng tới các bước đó. Cả hai chỉ dùng một đặc trưng (độ trễ) và nền ngắn. Suy rộng cũ “trị tuyệt đối không mang hướng nên phải giữ dấu” đã rút (WHY-47, đính chính ngày 13/10).
- **Tác giả có nêu không:** Nêu một phần: bài tự ghi giới hạn khi bất thường lan cả hai chiều. Lời văn của bài chấm qua mọi tập; mã tác giả chỉ chấm tập một dịch vụ.
- **Ảnh hưởng tới:** RQ2, RQ3.
- **Số ca theo ô:** Phụ lục A, các bảng RE2-TT / TraceRCA; Nezha-OB / TraceRCA.

#### G2-H06 — Trễ mạng: dấu hiệu nằm ở span phía gọi của lời gọi tới root

- **Phương pháp; dataset; chế độ:** BARO, SimpleRCA, TraceRCA (bản RCAEval); Nezha-OB (network_delay); RE2-TT để đối chiếu; (a).
- **Mã gốc:** H7, T-032:KT5.
- **Hiện tượng:** Với lỗi trễ mạng, span của chính root ít vượt ngưỡng; span phía gọi của lời gọi tới root thì vượt. Cách tính theo dịch vụ sở hữu span chấm dịch vụ gọi.
- **Số:** Nezha-OB, 6 ca trễ mạng: root đứng đầu theo span của mình ở 1 ca, theo span phía gọi ở 5 ca; BARO, SimpleRCA, TraceRCA xếp root hạng 1 ở 0, 1, 0 ca. Phần span không do span con phủ tách được root ở 26/26 ca RE2-TT (theo thời lượng cả span: 8/26) và 10/22 ca Nezha-OB. Span phía gọi của lời gọi tới root: 19/20 ca RE2-TT, 13/20 ca Nezha-OB.
- **Vì sao:** Đã xác lập ở mức ĐC **nơi có dấu hiệu** trong trace (đo trực tiếp theo vị trí, có mốc giả đối chứng). Chưa phân xử vì sao mỗi phương pháp xếp sai ở từng ca: mới là quan sát đặt cạnh thứ hạng.
- **Mức bằng chứng cao nhất:** ĐC (đo cơ chế). Nguồn con: bảng vị trí tín hiệu của root (T-032, KQ10 mục 3) — ĐC; mốc giả lùi vào nền (KQ10 mục 3) — LĐ; phép thử gán tín hiệu theo cạnh (gói bổ sung, KT5) — CT.
- **Loại nguồn hạn chế:** M + D.
- **Giải thích khác còn lại:** “Root đứng đầu theo một vị trí” không phải Hit@1 của một phương pháp. Định nghĩa vị trí đặt sau khi xem dev. Ở Nezha-OB một phần span có span con chạy chồng nhau, phép trừ phải xử lý chồng lấn.
- **Tác giả có nêu không:** Nêu một phần.
- **Ảnh hưởng tới:** RQ2, RQ3.
- **Số ca theo ô:** Phụ lục A, các bảng Nezha-OB / BARO; Nezha-OB / SimpleRCA; Nezha-OB / TraceRCA.

#### G2-H07 — Lỗi return ở Nezha-OB: root không hạng 1 dù có dấu hiệu

- **Phương pháp; dataset; chế độ:** BARO, SimpleRCA, TraceRCA, MicroRank; Nezha-OB (return); (a).
- **Mã gốc:** H8, M6.
- **Hiện tượng:** Root không đứng hạng 1 dưới các cách chấm đã xét, trong khi log lỗi tại root tăng và tỷ lệ thành công ở frontend giảm.
- **Số:** 4 ca return; BARO, SimpleRCA, TraceRCA xếp root hạng 1 ở 0, 0, 0 ca; ở 3 ca root cũng không đứng đầu theo vị trí trace nào. Số dòng log khớp từ khóa lỗi tại root (cửa sổ giả → sớm → muộn sau mốc): 0 → 124 → 156; 0 → 3 → 4; 0 → 104 → 124; 0 → 5 → 13.
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
- **Số:** 60/64 cặp do riêng phiếu metric quyết định. Đếm theo cột thay đếm theo mẫu (RE2-TT): 16/20 cặp mất, nhưng số ca hạng 1 tính bi quan từ 25 xuống 10 vì hòa (tính lạc quan: 23).
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
- **Số:** RE2-TT, đổi sang thang độ lệch chuẩn: 43/103 cặp mất; hạng 1 từ 21 lên 24; 0 ca đúng bị hỏng. Nezha-OB: 8 → 7, 3 ca đúng bị hỏng. Không lọc cột hằng: hạng root không đổi ở 52/52 ca.
- **Vì sao:** Đã xác lập ở mức CT cho RE2-TT. Đã loại giải thích “bước lọc cột hằng làm mất kênh của root”. Chưa phân xử các cặp còn lại: cột của dịch vụ khác đổi thật tại mốc, nguyên nhân vật lý không phân xử được bằng dữ liệu hiện có.
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
- **Số:** Trong 55 cột bộ nhớ thắng root ở BARO, 19 cột thuộc nhóm trôi nền.
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
- **Số:** Trong 103 cặp của BARO: 44 không có span, 34 rời chuỗi gọi, 4 chỉ chung phía trên; chỉ 5 cặp là dịch vụ phía trên thắng bằng cột độ trễ.
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
- **Hiện tượng:** Một cột đứng yên ở đoạn học rồi đổi ở đoạn chấm; hồi quy theo nút cha cho phần dư học gần bằng không và điểm cực lớn (vượt ngưỡng báo riêng của Q-82); DA chép điểm đó cho các nút cha.
- **Số:** 11/30 ca có nút điểm cực lớn. Trong 11 ca đó, số ca root hạng 1: bản có DA 3; bản có cạnh nhưng không DA 0; bỏ mọi cạnh 9, và còn 0 nút cực lớn. Ở 19 ca còn lại: bản có DA 13; bản có cạnh nhưng không DA 12; bỏ mọi cạnh 12.
- **Vì sao:** Đã xác lập ở mức CT: chuỗi bằng chứng đủ từ đầu vào tới hạng, không có nút cực lớn nào thiếu nguồn.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: phép đổi K-2 bỏ cạnh (T-032, KQ10 mục 1) — CT; mô tả phần được cộng ở bước DA (KT15) — ĐC.
- **Loại nguồn hạn chế:** M.
- **Giải thích khác còn lại:** Không đọc số CIRCA thành “cấu trúc gọi giúp” hay “hại” khi chưa tách 11 ca này. Minh đã chốt giữ bản gốc, không sửa (Q-82).
- **Tác giả có nêu không:** H13: không nêu. H14: nêu một phần (DA cần kiểm thêm trên dữ liệu thật).
- **Ảnh hưởng tới:** RQ1, RQ2, RQ3.
- **Số ca theo ô:** Phụ lục A, các bảng RE2-TT / CIRCA.

#### G2-H13 — CIRCA: hồi quy theo nút cha làm điểm cao hơn bản không cạnh; nhạy với cửa sổ

- **Phương pháp; dataset; chế độ:** CIRCA (đồ thị kiến trúc, OLS+RHT+DA); RE2-TT; (a).
- **Mã gốc:** H15, T-032:KT9.
- **Hiện tượng:** Phần dư ở đoạn học nhỏ mà phần dư ở đoạn chấm không nhỏ theo, nên điểm có cạnh cao hơn điểm không cạnh.
- **Số:** 3.285/4.526 nút có hồi quy tăng điểm. Nhóm 183 nút có nhiều nút cha (nhóm `at_least8_parents`), trung vị tỷ số có cạnh/không cạnh: 7,38 (đoạn học ngắn gần mốc, `native111_late`), 3,49 (đoạn học dài, `long291_late`), 7,51 (đoạn ngắn sớm, `early111_late`), 3,73 / 3,26 / 3,55 (cùng số điểm như đoạn ngắn nhưng trải đều trên đoạn dài).
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
- **Số:** Bỏ nguồn log (seed 0): 3/4 ca sai thành hạng 1; 0 ca đúng bị hỏng.
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
- **Hiện tượng:** Root không bao giờ nằm trong khối do nhánh RCD xếp.
- **Số:** 0/90 đơn vị (ca × seed) có root thuộc khối do RCD xếp; 9 đơn vị root rơi nhánh dự phòng.
- **Vì sao:** Chưa phân xử vai trò của đồ thị nhân quả: trên bản ghi, bước đó không tham gia xếp root, nên không rút được kết luận nào về đồ thị nhân quả từ TORAI.
- **Mức bằng chứng cao nhất:** MT (mô tả). Nguồn con: phân rã khối trên các bản ghi đóng băng (T-032, KQ9 mục 7) — MT.
- **Loại nguồn hạn chế:** A.
- **Giải thích khác còn lại:** Thuộc bản cài trong thư viện (lỗi giảm mẫu hai lần đã nêu ở T-016); chưa kiểm bản tác giả đã dùng để tạo số công bố.
- **Tác giả có nêu không:** Không nêu.
- **Ảnh hưởng tới:** RQ1, RQ3.
- **Số ca theo ô:** Phụ lục A, các bảng RE2-TT / TORAI B.

#### G2-H16 — Rào cản tập ứng viên, hòa cắt biên và ca dừng lỗi vì thao tác thiếu nền

- **Phương pháp; dataset; chế độ:** TraceRCA, MicroRank (bản RCAEval); SimpleRCA; RE2-TT, Nezha-OB; (a).
- **Mã gốc:** M1, M2, M3, D4, T-032:KT8.
- **Hiện tượng:** Root nằm ngoài tập quan sát hoặc tập trả về; hòa cắt ngang biên top-k; một thao tác chỉ có sau mốc làm phương pháp dừng lỗi.
- **Số:** Ở TraceRCA trên Nezha-OB, trong 20 ca sai: M1 (root ngoài tập quan sát) 0 ca; M2 (root quan sát được nhưng không được trả về) 1 ca; M3 (hòa cắt biên) 1 ca. Các phương pháp khác: xem cột cờ ở Phụ lục A (cột chỉ hiện khi có ca mang cờ). ERROR: 4 ca RE2-TT ở MicroRank và 4 ca ở TraceRCA, đang tính trượt. Bỏ thao tác thiếu nền (đổi đầu vào, chẩn đoán): TraceRCA xếp root hạng 1 ở 3/4 ca đó.
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
- **Số:** Cờ M5 trên số ca sai hạng 1 (đa nhãn): TraceRCA 4/5 và 16/20; MicroRank 5/24 và 20/22; SimpleRCA 5/5 và 9/15; BARO 3/9 và 7/14; CIRCA 10/14; TORAI B 1/4 (RE2-TT trước, Nezha-OB sau). Khả năng đo việc “dịch vụ gọi chờ root”: 16 ca Nezha-OB đo được có điều kiện, 21 ca RE2-TT đo được một phần, 15 ca không đo được.
- **Vì sao:** Chưa phân xử “lan có đáng kể”, vì cờ M5 không đồng nghĩa “sai vì dịch vụ gọi”, cơ chế khác nhau theo phương pháp, và chưa có định nghĩa “đáng kể” được chọn. Xem mục 4.
- **Mức bằng chứng cao nhất:** LĐ (liên hệ có đối chứng). Nguồn con: cờ M5 so mức nền P0 (T-028) — LĐ; bảng theo ca cho các đơn vị có cờ M5 (T-032 mục 5.3) — ĐC; mức đo được theo ca (T-032 mục 5.4) — MT.
- **Loại nguồn hạn chế:** M + D.
- **Giải thích khác còn lại:** Dịch vụ gọi tự bất thường; tác động chung qua hạ tầng; cách chấm ưu tiên dịch vụ đông lưu lượng; giá trị cực lớn qua DA (CIRCA); sai lệch cửa sổ, đồng hồ hoặc đồ thị.
- **Tác giả có nêu không:** Bài TraceRCA có mô tả hiện tượng ở phần bài học triển khai.
- **Ảnh hưởng tới:** RQ2, RQ3.
- **Số ca theo ô:** Phụ lục A, các bảng RE2-TT / BARO; RE2-TT / SimpleRCA; RE2-TT / MicroRank; RE2-TT / TraceRCA; RE2-TT / CIRCA; RE2-TT / TORAI B; Nezha-OB / BARO; Nezha-OB / SimpleRCA; Nezha-OB / MicroRank; Nezha-OB / TraceRCA.

#### G2-H18 — Ca sai chưa gắn được cờ cơ chế nào (M0)

- **Phương pháp; dataset; chế độ:** BARO, MicroRank, CIRCA, TORAI B, TraceRCA, SimpleRCA; RE2-TT, Nezha-OB; (a).
- **Mã gốc:** M0.
- **Hiện tượng:** Ca sai không có cờ M1–M6; đọc tay ở T-032 đã gắn phần lớn về các bước ở G2-H01 đến G2-H15, phần còn lại ghi là chưa rõ.
- **Số:** Nhãn chính M0 trên số ca sai hạng 1: MicroRank 19/24 (RE2-TT); BARO 6/9 và 7/14; CIRCA 4/14; TORAI B 3/4; SimpleRCA 6/15 (Nezha-OB).
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
- **Hiện tượng:** Nền trace ngắn và metric thưa ở Nezha-OB; root không được dịch vụ nào gọi; không có span mang mã lỗi; không công bố phiên bản mã và công cụ ghi span.
- **Số:** Nezha-OB: 22/22 ca có nền trace ngắn và chỉ vài mẫu metric mỗi phía (mã D1 của T-032); CIRCA và TORAI B không chạy được ở 22/22 ca. 15/52 ca không đủ lời gọi tới root: 8 ca root không được dịch vụ nào gọi trong trace, 7 ca cạnh gọi tới root quá thưa. RE2-TT: 21 ca chỉ đo được một phần vì thiếu thông tin công cụ ghi span.
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
- **Số:** Cắt dữ liệu sau mốc rồi tiền xử lý lại: báo động đầu sớm hơn ở 29/30 ca, bằng ở 1, muộn hơn ở 0; tổng điểm đổi trước mốc 143 → 338 (nhánh đổi hazard, I2: 332). Tiền xử lý chỉ dùng quá khứ (hai biến thể chẩn đoán): tập điểm đổi khác bản gốc ở 30/30 và 30/30 ca.
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
- **Số:** Báo động đầu ở hoặc sau mốc: 3/30 ca. Đổi prior trên cùng đầu vào: tập điểm đổi khác ở 30/30, 30/30, 30/30 ca (tổng điểm đổi 437 → 443, 425, 952). **Phép E2** (posterior trong miền log, bốn chuỗi của hai ca): MAP và điểm đổi trùng bản gốc ở 3/4 chuỗi; ở chuỗi full của dev-3ae0a6c15a MAP khác tại 12 điểm liên tiếp, bản gốc có 1 điểm đổi mà phép tính trong miền log không có, và thiếu 3 điểm đổi mà phép tính trong miền log có; tất cả nằm trong 45 giây đầu sau mốc.
- **Vì sao:** Chưa phân xử vì sao có báo động trước mốc: không có nền sạch và onset được xác nhận độc lập. Đã loại hazard trên miền được chấm (I2). Đã xác lập ở mức CT độ nhạy với prior. Đã xác lập ở mức CT rằng underflow làm đổi MAP và điểm đổi ở một trong bốn chuỗi đã kiểm, trong một đoạn ngắn sau mốc; đã loại underflow như giải thích cho các báo động trước mốc của hai ca đó.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: can thiệp I2 và cờ B1, B4, D0 (T-029) — CT / LĐ; ba mức prior trên cùng X, d (T-033, K3) — CT; phép E2 của T-034 (hai-phep-kiem.md) — CT.
- **Loại nguồn hạn chế:** M + A + D.
- **Giải thích khác còn lại:** Nền không sạch; biến động tải; bước nhảy telemetry (cờ B4 cũng phổ biến ở điểm không báo); hiệp phương sai và prior. Số điểm đổi không phải thước đo chất lượng.
- **Tác giả có nêu không:** Chưa thấy trong nguồn đã khảo sát.
- **Ảnh hưởng tới:** RQ1, RQ2, RQ3a.
- **Số ca theo ô:** Phụ lục B, các cột HP-5, HP-7, HP-8, HP-9 (D0).

#### G2-H22 — N-Sigma: báo dày ngay trên đoạn nền

- **Phương pháp; dataset; chế độ:** N-Sigma (cấu hình đã khóa của T-025); RE2-TT; (b).
- **Mã gốc:** HP-1, HP-2, HP-3, HP-4, HP-14, T-033:K2.
- **Hiện tượng:** Báo động đầu luôn trước mốc; rất nhiều báo động trên giờ bình thường theo nhãn proxy.
- **Số:** Báo động đầu ở hoặc sau mốc: 0/30 ca; 1168 báo động mỗi giờ bình thường theo nhãn proxy (bộ cột chính). Lịch sử trượt có độ dài cố định thay cho lịch sử mở rộng: báo động đầu sau mốc sớm hơn ở 18 ca, bằng 7, muộn hơn 5.
- **Vì sao:** Chưa phân xử nguyên nhân thống kê: các cờ (lịch sử ngắn, cột báo dày, độ lệch chuẩn bằng không, nền mở rộng nhận dữ liệu sau mốc) mới là liên hệ. Đã xác lập ở mức CT rằng độ dài lịch sử và phép OR nhiều cột đi vào kết quả.
- **Mức bằng chứng cao nhất:** LĐ (liên hệ có đối chứng). Nguồn con: cờ N1–N4, N6 và đọc tay (T-029) — LĐ; đối chiếu lịch sử trượt/mở rộng (T-033, K2) — CT.
- **Loại nguồn hạn chế:** M.
- **Giải thích khác còn lại:** Đuôi không chuẩn; nền không dừng; nhiều cột cùng được xét (phép OR); lượng hóa của metric. Không có nền sạch độc lập để gọi một báo động là “sai trong vận hành”.
- **Tác giả có nêu không:** Bài BARO nêu baseline báo sai nhiều; chưa thấy cơ chế cụ thể.
- **Ảnh hưởng tới:** RQ1, RQ2, RQ3a.
- **Số ca theo ô:** Phụ lục B, các cột HP-1, HP-2, HP-3, HP-4.

#### G2-H23 — Đầu vào bậc thang: nhiều hàng metric lặp lại

- **Phương pháp; dataset; chế độ:** BOCPD (bản BARO); RE2-TT; (b).
- **Mã gốc:** T-033:K4.
- **Hiện tượng:** Chuỗi đầu vào có nhiều vectơ lặp liên tiếp; số quan sát hiệu lực ít hơn số hàng.
- **Số:** Bỏ hàng lặp: tập điểm đổi khác bản gốc ở 29/30 ca (hazard theo hàng) và 29/30 ca (hazard theo thời gian); tổng điểm đổi 437 → 360 và 361.
- **Vì sao:** Đã xác lập ở mức CT rằng gói thay đổi “bỏ hàng lặp” làm đổi điểm đổi. Chưa phân xử riêng từng yếu tố: phép nén đổi cùng lúc số lần cập nhật, đơn vị run length và quy tắc CP.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: hai nhánh nén (T-033 gói bổ sung, K4) — CT.
- **Loại nguồn hạn chế:** D + M.
- **Giải thích khác còn lại:** Không chứng minh lượng hóa của bộ thu thập là nguyên nhân, cũng không chứng minh nén là cách sửa.
- **Tác giả có nêu không:** Chưa thấy trong nguồn đã khảo sát.
- **Ảnh hưởng tới:** RQ2, RQ5.
- **Số ca theo ô:** Không tách theo ô: nguồn có theo ca (`engine-final-summary-001.json#/slots`), không tổng theo ô.

#### G2-H24 — Nhãn proxy, thời lượng lỗi và onset chưa được xác nhận độc lập

- **Phương pháp; dataset; chế độ:** Mọi phép chấm phát hiện; RE2-TT; (b).
- **Mã gốc:** HP-12, T-033:K1, T-033:K5, T-033:K7.
- **Hiện tượng:** Nhãn chỉ có mốc tiêm; không biết lúc lỗi bắt đầu có tác động, lúc hết, và đoạn trước mốc có sạch không.
- **Số:** Số ca BOCPD có điểm đổi trong D giây sau mốc: 12, 23, 27, 29, 30 trên 30 ca, với D lần lượt là các mức `30`, `60`, `120`, `300`, `600` giây. Log có ghi kết quả ở vị trí cụ thể: access log 65.544 dòng HTTP `200`, 28 dòng `500`, 9 dòng `503`; phản hồi backend 336.754 lần trạng thái `1` và 27.278 lần trạng thái `0`.
- **Vì sao:** Chưa phân xử, vì dataset không cung cấp onset có tác động, lúc hết lỗi, đoạn khỏe được kiểm độc lập, sai số đồng hồ và phép nối đã xác minh giữa dòng log với từng lời gọi.
- **Mức bằng chứng cao nhất:** MT (mô tả). Nguồn con: đường độ nhạy theo D (T-033, K7) — MT; đọc toàn bộ thông điệp log ở vùng khóa (T-033, K1, K5) — MT; nguồn chưa xác nhận D (T-029, HP-12) — CK.
- **Loại nguồn hạn chế:** D.
- **Giải thích khác còn lại:** Số dòng log không phải số yêu cầu hay số sự cố. HTTP `200` hay trạng thái `1` không chứng minh hệ khỏe; `500` hay `503` không tự cho onset.
- **Tác giả có nêu không:** RCAEval mô tả mốc tiêm và cách thu; chưa thấy thời lượng lỗi cho các ca này.
- **Ảnh hưởng tới:** RQ3a, RQ5.
- **Số ca theo ô:** Không tách theo ô: đại lượng theo ca hoặc theo vùng log; không có bảng theo ô.

#### G2-H25 — Schema metric đổi theo ca và liên hệ với root

- **Phương pháp; dataset; chế độ:** BARO, SimpleRCA, CIRCA, TORAI, BOCPD, N-Sigma; RE2-TT; (a), (b).
- **Mã gốc:** HP-13.
- **Hiện tượng:** Tập cột metric khác nhau giữa các ca; sự có mặt của một số cột liên hệ với root.
- **Số:** Không có con số tổng trong gói này; bảng chéo ở `results/T-029/nhan-proxy-va-schema.json`.
- **Vì sao:** Chưa phân xử ảnh hưởng của schema lên kết quả: bảng chéo trên dev không tách được schema với việc mất tín hiệu lỗi (WHY-27).
- **Mức bằng chứng cao nhất:** LĐ (liên hệ có đối chứng). Nguồn con: bảng chéo schema × root (T-029, P2) — LĐ.
- **Loại nguồn hạn chế:** D.
- **Giải thích khác còn lại:** Triển khai và thu thập khác nhau theo dịch vụ; root và loại lỗi chưa giao chéo đầy đủ trong dev.
- **Tác giả có nêu không:** Chưa thấy trong nguồn đã khảo sát.
- **Ảnh hưởng tới:** RQ1, RQ2.
- **Số ca theo ô:** Không tách theo ô: bảng chéo theo cột và root nằm ở `results/T-029/nhan-proxy-va-schema.json`.

#### G2-H26 — Chế độ (b): thành công chung bị chặn ở báo động đầu; RCA phụ thuộc điểm chạy

- **Phương pháp; dataset; chế độ:** BARO, CIRCA, TORAI B ghép với BOCPD hoặc N-Sigma; RE2-TT; (b).
- **Mã gốc:** HP-10, HP-11.
- **Hiện tượng:** RCA chạy tại báo động đầu; báo động đầu sai thì ca trượt. Cùng một ranker cho kết quả khác nhau khi chạy tại mốc tiêm, tại báo động đầu sau mốc, và tại báo động đầu.
- **Số:** BARO ghép BOCPD, Hit@1 trên 30 ca: 0,70 tại mốc tiêm, 0,63 tại báo động đầu sau mốc, 0,27 tại báo động đầu; TORAI B ghép BOCPD: 0,87, 0,40, 0,23. Thành công chung Hit@1 cao nhất: 0,067 (BARO ghép BOCPD).
- **Vì sao:** Đã xác lập ở mức CT rằng điểm chạy RCA làm đổi kết quả. Chưa phân xử từng đường tác động: đổi cửa sổ còn đổi nền, cột ứng viên và đồ thị của CIRCA.
- **Mức bằng chứng cao nhất:** CT (can thiệp). Nguồn con: can thiệp I3 và bảng G (T-029) — CT.
- **Loại nguồn hạn chế:** G + M.
- **Giải thích khác còn lại:** Báo động đầu sau mốc được chọn nhờ nhãn mốc, nên không phải cận trên của chất lượng RCA. Thứ tự báo động của các dịch vụ không phải bằng chứng nhân quả hay lan.
- **Tác giả có nêu không:** Bài BARO có nêu độ nhạy theo thời điểm.
- **Ảnh hưởng tới:** RQ1, RQ2.
- **Số ca theo ô:** Không tách theo ô: bảng G theo ô nằm ở `results/T-029/a-so-b.json#/by_detector/*/*/by_cell`.

## 4. K4 — “Nhầm triệu chứng lan với nguyên nhân” có đáng kể không (Q-86)

MRP đặt câu này ở P4: nếu cơ chế “độ trễ lan lên dịch vụ gọi, nên dịch vụ gọi bị xếp trên root” chiếm phần đáng kể các ca sai thì định nghĩa nhãn “lan” cho từng ca; nếu không thì không tách.

### 4.1 Điều đã thấy

**Hỗ trợ.**

- *Hiện tượng chờ có thật và quan sát được ở phần lớn ca đo được* (ĐC). Ngưỡng “lời gọi chậm” của một cạnh lấy từ dữ liệu bình thường: phân vị 95 của thời lượng phía gọi trước mốc. Ở các ca có cạnh gọi tới root, có ít nhất một cạnh với từ một nửa số lời gọi sau mốc là chậm ở 19/21 ca RE2-TT và 10/16 ca Nezha-OB. Hạ mức xuống một phần năm: 20 và 12 ca. Trước mốc tỷ lệ này khoảng 5% theo cách đặt ngưỡng.
- *Với TraceRCA bản thư viện, chuỗi “chờ → cờ → điểm” được xác lập* (CT ở RE2-TT, ĐC ở hai dataset; G2-H03): trong các cặp dịch vụ phía trên đứng trên root, span mang cờ chủ yếu là span bao lời gọi chậm tới root ở 4/4 cặp RE2-TT và 9/15 cặp Nezha-OB.
- *Với lỗi trễ mạng ở Nezha-OB* (ĐC; G2-H06): dấu hiệu nằm ở span phía gọi của lời gọi tới root ở 5/6 ca, ở span của chính root chỉ 1 ca.

**Bất lợi cho cách đọc “phần lớn ca sai là do nhầm triệu chứng”.**

- Hiện tượng chờ có cả ở ca **đúng**: 83/96 dịch vụ phía trên ở các ca TraceRCA xếp root hạng 1. Tự nó không phân biệt ca sai.
- Bỏ phần chờ khỏi cờ của TraceRCA (phép T-D) chỉ đổi ít: số ca có dịch vụ gọi trên root 4 → 2 ở RE2-TT và 16 → 15 ở Nezha-OB; số ca hạng 1 23 → 25 trên 47 ca.
- Ở MicroRank và BARO, phần lớn thực thể đứng trên root **không** nằm phía trên root: chỉ 24/252 và 15/162 cặp. Với kênh metric của BARO ở RE2-TT, chỉ 5/103 cặp là dịch vụ phía trên thắng bằng cột độ trễ.
- Ở CIRCA, dịch vụ gọi đứng trên root là do giá trị cực lớn đi qua bước cộng điểm (G2-H12), không phải do chờ.
- Cờ “có dịch vụ phía trên đứng trước root” (M5 của T-028) không đồng nghĩa “sai vì dịch vụ gọi”. Số đơn vị có cờ trên số đơn vị sai hạng 1: TraceRCA 4/5 và 16/20; MicroRank 5/24 và 20/22; SimpleRCA 5/5 và 9/15; BARO 3/9 và 7/14; CIRCA 10/14 (RE2-TT trước, Nezha-OB sau). Các cờ này chồng nhau và không phải tỷ lệ nguyên nhân.

**Khả năng đo.** Việc “dịch vụ gọi chờ root” đo được có điều kiện ở 16 ca Nezha-OB, đo được một phần ở 21 ca RE2-TT (thiếu thông tin công cụ ghi span), và không đo được ở 15 ca (8 ca root không được dịch vụ nào gọi, 7 ca cạnh quá thưa). Đây là khả năng quan sát trên 52 ca; không phải nhãn lan, tỷ lệ lan, hay tỷ lệ nguyên nhân thất bại.

### 4.2 Trả lời

- **Đã xác lập** (ĐC): độ trễ của root hiện lên ở span phía gọi trong phần lớn ca đo được. Lan, hiểu là hiện tượng quan sát được, là phổ biến.
- **Đã xác lập** (CT): với TraceRCA bản thư viện, phần chờ đó được chấm thành bất thường của dịch vụ gọi.
- **Chưa phân xử:** lan có là nguyên nhân của “phần đáng kể các ca sai” không. Bằng chứng hiện có nghiêng về **không chiếm đa số**: nó giải thích một phần ca sai của TraceRCA bản thư viện và các ca trễ mạng ở Nezha-OB. Ở BARO và CIRCA, phần lớn ca sai có cơ chế khác đã xác lập (G2-H09, G2-H12). Ở MicroRank, phần lớn thực thể đứng trên root không nằm phía trên root, nhưng đường gián tiếp “chờ → cờ → trace bị xếp bất thường → điểm” **chưa được phân xử đầy đủ** (T-032 mục 5.2), nên chưa loại được vai trò của chờ ở phương pháp này. Chưa có một định nghĩa “đáng kể” được chọn để biến các điều trên thành một tỷ lệ, và hai phép E1, E2 không đo lan.

### 4.3 Nhãn “lan”: nháp có điều kiện, chưa đề xuất khóa

Các thành phần sau **đã có số đo** trên dev, đủ để viết một nháp:

- *Đại lượng:* với mỗi ca, tỷ lệ lời gọi chậm sau mốc trên từng cạnh gọi tới root.
- *Ngưỡng từ dữ liệu bình thường:* phân vị 95 của thời lượng phía gọi trước mốc, theo từng cạnh.
- *Nhãn nháp:* ca “có lan” nếu ít nhất một cạnh tới root có tỷ lệ lời gọi chậm sau mốc từ một mức θ trở lên.
- *Độ nhạy đã đo:* hai mức θ (một nửa và một phần năm) cho 19 và 20 ca RE2-TT, 10 và 12 ca Nezha-OB.
- *Không vòng lặp:* định nghĩa không dùng thứ hạng của bất kỳ phương pháp nào.
- *Không áp dụng được:* 15 ca không có cạnh tới root đủ lời gọi. Các ca này phải là nhóm thứ ba, không gộp vào “không lan”.

**Còn thiếu trước khi có thể khóa ở G3:** (i) độ nhạy ở nhiều mức θ hơn và theo phân vị nền khác; (ii) cách xử lý nền rất ngắn của Nezha-OB; (iii) ở RE2-TT, điều kiện về công cụ ghi span (tác giả không công bố); (iv) quyết định có tính lan qua nhiều tầng gọi không. Các phép này chỉ đọc bảng lời gọi đã lưu, chưa được giao, chi phí chưa đo.

**Quyết định phụ thuộc** (mục 8): nếu Minh muốn P7 báo riêng nhóm “lan” và “không lan”, cần một task nhỏ hoàn thiện nháp trên và khóa ở G3. Nếu không, P7 không tách theo nhãn này; gói G2 không tự khóa nhãn.

## 5. K5 — Căn cứ và ứng viên cho P5/P6

Đây là **ứng viên để thử**, không phải lựa chọn, và không xếp theo kỳ vọng thắng. Thành phần cụ thể chốt ở spec P6, sau khi so phương án và kiểm trên dev. Mức căn cứ theo bảng ở MRP §3: mọi ứng viên dưới đây mới đạt bậc “đủ để đề xuất thử”. Để **chọn** còn thiếu: so phương án, kiểm đầu vào, trung gian và hành vi của chính bản cài mới trên dev. Để **khẳng định hiệu quả** còn thiếu: đánh giá sau khóa thiết kế, với nhánh cùng bằng chứng không dùng quan hệ và đồ thị ngẫu nhiên giữ bậc.

### UV-1 — Gắn thời gian lời gọi lên cạnh, tính cho dịch vụ được gọi

- **Mục đích:** sửa hạn chế G2-H03 và G2-H06.
- **Căn cứ và mức:** ĐC. Root đứng đầu theo span phía gọi của lời gọi đi vào ở 19/20 ca RE2-TT và 13/20 ca Nezha-OB; theo thời lượng span của chính dịch vụ chỉ 8/26 ca RE2-TT. Phép thử gán tín hiệu theo cạnh của gói bổ sung T-032 (KT5) cho thấy đổi cạnh thì đổi điểm (CT ở mức tính toán).
- **Giải thích khác còn lại:** “root đứng đầu theo một vị trí” không phải Hit@1 của một phương pháp hoàn chỉnh; định nghĩa vị trí đặt sau khi xem dev; phần chậm ngoài span của root không tách được.
- **Cơ chế dự kiến:** lời gọi tới root chậm làm span phía gọi dài ra; gán phần đó cho dịch vụ **được gọi** thay vì dịch vụ sở hữu span.
- **Nút, cạnh, ánh xạ, phép tính dùng cạnh:** nút là dịch vụ; cạnh có hướng là lời gọi đồng bộ (span phía gọi → span phía được gọi); trace được ánh xạ lên cạnh; với mỗi nút, phép tính gộp tỷ lệ lời gọi **đi vào** có thời lượng phía gọi vượt nền của chính cạnh đó.
- **Dự đoán trên dev, khai trước:** (i) xếp root hạng 1 ở nhiều ca hơn nhánh dùng cùng tín hiệu nhưng gán theo dịch vụ sở hữu span; (ii) ở mốc giả không có lỗi, không đưa một dịch vụ cố định lên đầu quá mức nền; (iii) với đồ thị ngẫu nhiên giữ bậc, lợi thế ở (i) mất. **Bác bỏ** nếu (i) không xảy ra ở cả hai dataset, hoặc (iii) không mất.
- **Điều kiện thất bại đã biết:** 8 ca root không được gọi; 7 ca cạnh thưa; lỗi không làm chậm lời gọi (return).
- **Tầng:** ánh xạ và chấm điểm (tầng 1–2).

### UV-2 — Thời gian tự xử lý theo quan hệ cha–con của span

- **Mục đích:** sửa hạn chế G2-H03.
- **Căn cứ và mức:** ĐC. Phần span không do span con phủ tách được root ở 26/26 ca RE2-TT, so với 8/26 theo thời lượng cả span; ở Nezha-OB chỉ 10/22 ca. CT: đổi cờ sang phần chưa phủ làm số ca có dịch vụ gọi trên root giảm 4 → 2 (RE2-TT).
- **Giải thích khác còn lại:** ở Nezha-OB một phần span có span con chạy chồng nhau, phép trừ đơn giản sai; ở RE2-TT phải giả định công cụ ghi span.
- **Cơ chế dự kiến:** trừ khỏi thời lượng span phần đã do span con phủ, có xử lý chồng lấn và song song.
- **Nút, cạnh, ánh xạ, phép tính dùng cạnh:** quan hệ dùng là cha–con **trong trace** (không phải đồ thị dịch vụ); span ánh xạ lên nút dịch vụ; phép tính dùng quan hệ: hợp các khoảng thời gian của span con.
- **Dự đoán trên dev, khai trước:** số ca root đứng đầu theo đại lượng này cao hơn theo thời lượng cả span ở cả hai dataset, và không cao bất thường ở mốc giả. **Bác bỏ** nếu ở Nezha-OB sau khi xử lý chồng lấn vẫn không hơn thời lượng cả span.
- **Điều kiện thất bại đã biết:** lời gọi bất đồng bộ; thiếu span con; lỗi tài nguyên không làm tăng độ trễ; lỗi trả về nhanh.
- **Tầng:** ánh xạ (tầng 1).

### UV-3 — Tiêu chí “yêu cầu bất thường” theo cả cây lời gọi

- **Mục đích:** sửa hạn chế G2-H01.
- **Căn cứ và mức:** CT. Thay riêng bước chia trace của MicroRank bản thư viện bằng công thức của bài gốc: hạng 1 từ 2 lên 21–22 trên 47 ca xét được. Ở mốc giả không lỗi, luật theo từng span vẫn xếp 37% trace là bất thường.
- **Giải thích khác còn lại:** bộ chia thay thế dùng quy ước span đầu của ta; sau khi thay vẫn còn hơn một nửa số ca chưa hạng 1.
- **Cơ chế dự kiến:** quyết định “bất thường” ở mức cả yêu cầu, so với tổng mức nền của các thao tác trong cây.
- **Nút, cạnh, ánh xạ, phép tính dùng cạnh:** dùng cây lời gọi của từng yêu cầu để gom thao tác; chưa dùng đồ thị dịch vụ. Đây là thành phần đầu vào cho bước phát hiện, không phải cơ chế đồ thị.
- **Dự đoán trên dev, khai trước:** tỷ lệ trace bị xếp bất thường ở mốc giả thấp hơn luật theo từng span, và tỷ lệ trace bất thường có span của root cao hơn. **Bác bỏ** nếu một trong hai không xảy ra.
- **Điều kiện thất bại đã biết:** thao tác chỉ xuất hiện sau mốc (không có nền; G2-H16).
- **Tầng:** phát hiện ở mức yêu cầu (tầng 2).

### UV-4 — Quy tắc gộp điểm qua tập dịch vụ (kiểu TraceRCA)

- **Mục đích:** sửa hạn chế G2-H05, nếu P6 dùng cách chấm theo tập.
- **Căn cứ và mức:** CT, trong 13 cặp của phép E1. Ở cờ ba lần độ lệch chuẩn, chỉ chấm tập một dịch vụ làm 4/5 cặp Nezha-OB đổi sang root trên. Ở cờ một lần (mặc định của bài): 1/7.
- **Giải thích khác còn lại:** tác dụng phụ thuộc mức cờ; ở RE2-TT bước quyết định là bước chọn tập, không phải quy tắc gộp; mới thử trên ít cặp, các cặp chung ca không độc lập.
- **Cơ chế dự kiến:** không cho một dịch vụ xuất hiện rộng (như frontend) thừa hưởng điểm của tập chứa root.
- **Nút, cạnh, ánh xạ, phép tính dùng cạnh:** không dùng cạnh; dùng tập dịch vụ cùng xuất hiện trong trace bất thường.
- **Dự đoán trên dev, khai trước:** chỉ có ích ở mức cờ cao. **Bác bỏ** nếu trên toàn bộ ca dev (không chỉ 13 cặp) đổi quy tắc không đổi số ca root hạng 1.
- **Tầng:** xếp hạng (tầng 4).

### UV-5 — Giữ hướng của cạnh khi so lời gọi đi vào với đi ra

- **Mục đích:** ứng viên để so sánh; **không** còn là điều kiện bắt buộc.
- **Căn cứ và mức:** MT. Suy rộng cũ “trị tuyệt đối không mang hướng nên phải giữ dấu” đã rút (đính chính ngày 13/10, WHY-47). Mã tác giả TraceRCA dùng trị tuyệt đối mà vẫn đưa root lên trên dịch vụ gọi ở 7/8 cặp Nezha-OB.
- **Giải thích khác còn lại:** toàn bộ phép chấm (độ tương đồng nhân hiệu số) có thể tách root mà không cần dấu.
- **Dự đoán trên dev, khai trước:** nếu thử, bản giữ dấu phải hơn bản trị tuyệt đối trên cùng đầu vào. **Bác bỏ** nếu không hơn.
- **Tầng:** chấm điểm (tầng 2).

### UV-6 — Dùng tín hiệu giảm và log tại root cho lỗi trả về sớm

- **Mục đích:** sửa hạn chế G2-H07.
- **Căn cứ và mức:** LĐ. Ở 4 ca return, log lỗi tại root tăng sau mốc ở cả 4 ca và tỷ lệ thành công ở frontend giảm; các phép chấm hiện có bỏ qua tín hiệu giảm hoặc chỉ cho log một phiếu.
- **Giải thích khác còn lại:** số dòng log không phải số yêu cầu lỗi; hai ca có phản ứng metric ở frontend chứ không ở chính root; chỉ bốn ca.
- **Cơ chế dự kiến:** chấm cả chiều giảm của tỷ lệ thành công; dùng mật độ log lỗi theo dịch vụ thay cho một phiếu có/không.
- **Nút, cạnh, ánh xạ, phép tính dùng cạnh:** log ánh xạ lên nút theo dịch vụ và thời gian (qua trace_id nếu có); chưa có phép tính dùng cạnh.
- **Dự đoán trên dev, khai trước:** root lên hạng ở các ca return mà không làm tụt các ca đang đúng. **Bác bỏ** nếu số ca đang đúng bị hỏng nhiều hơn số ca return được sửa.
- **Tầng:** ánh xạ và chấm điểm (tầng 1–2).

### UV-7 — Hai yêu cầu kỹ thuật cho mọi bước lan điểm trên đồ thị

- **Mục đích:** nhu cầu kỹ thuật, rút từ G2-H12.
- **Căn cứ và mức:** CT. Ở 11/30 ca của CIRCA có nút điểm cực lớn; trong nhóm đó bản có DA đúng 3 ca, bỏ mọi cạnh thì đúng 9 ca.
- **Nội dung:** (i) chặn giá trị không hợp lệ ở một nút trước khi lan; (ii) không chép nguyên điểm lớn nhất của nút con sang mọi nút cha.
- **Dự đoán trên dev, khai trước:** với hai chặn này, không còn ca nào mà một nút điểm cực lớn quyết định thứ hạng. **Bác bỏ** nếu vẫn còn.
- **Tầng:** chấm điểm và xếp hạng (tầng 2, 4).

### UV-8 — Hồi quy có điều kiện theo nút cha (kiểu CIRCA)

- **Mục đích:** ứng viên có sẵn ở MRP P6; ghi lại để không bỏ sót.
- **Căn cứ và mức:** CT, **bất lợi** trên dev: G2-H12 và G2-H13. 3.285/4.526 nút có hồi quy làm tăng điểm so với bản không cạnh; kết quả nhạy với cửa sổ học.
- **Giải thích khác còn lại:** chưa tách được thành phần mẫu, độ gần đoạn chấm và thang phần dư.
- **Dự đoán trên dev, khai trước:** nếu thử lại, phải kèm UV-7 và một cách chuẩn phần dư; bản có cạnh phải hơn bản bỏ cạnh trên nhóm ca không có nút cực lớn. **Bác bỏ** nếu không hơn (hiện, với bản không DA: 12 so với 12 trên 19 ca).
- **Tầng:** chấm điểm (tầng 2).

### UV-9 — Phát hiện: tiền xử lý chỉ dùng quá khứ và số học ổn định

- **Mục đích:** sửa hạn chế G2-H20; nhu cầu kỹ thuật từ phép E2.
- **Căn cứ và mức:** CT. Cắt dữ liệu sau mốc rồi tiền xử lý lại làm báo động đầu sớm hơn ở 29/30 ca. Tính trong miền log làm đổi điểm đổi ở 1/4 chuỗi đã kiểm.
- **Giải thích khác còn lại:** bỏ nhìn trước không cho thấy sẽ giảm báo động trước mốc; nguyên nhân của các báo động đó chưa phân xử (G2-H21).
- **Nội dung:** bộ phát hiện ở P6 chỉ được dùng dữ liệu tới thời điểm đang xét; phép tính xác suất làm trong miền log.
- **Dự đoán trên dev, khai trước:** với tiền xử lý chỉ dùng quá khứ, vị trí báo động đầu không đổi khi thêm dữ liệu tương lai. **Bác bỏ** nếu còn đổi.
- **Tầng:** phát hiện (tầng 2).

### UV-10 — Các thành phần DT18 yêu cầu mà P4 không cung cấp bằng chứng

- **Mục đích:** đáp ứng DT18 và bước 1–2 của cô: cạnh trao đổi thông điệp và phụ thuộc dữ liệu; vùng nghi ngờ (đồ thị con bất thường); xếp hạng trên đồ thị.
- **Căn cứ:** yêu cầu của đề tài (đoạn nhiệm vụ thứ hai của DT18), **không** phải một hạn chế đã thấy ở P4. Hai dataset dev chưa có kiểm tra về loại span cho cạnh có kiểu; không có nhãn vùng ảnh hưởng.
- **Hệ quả:** các thành phần này ghi đúng lý do là “đáp ứng DT18”; không dựng một hạn chế để hợp thức hóa. Bằng chứng về lợi ích chỉ có thể đến từ P7 và P10.
- **Tầng:** mô hình đồ thị (P5), tầng 3 và 4.

**Hai căn cứ kỹ thuật đã có về việc “cạnh có tham gia phép tính”:** phép dò cạnh của gói bổ sung T-032 (KT5) và phép dò đồ thị của T-033 (K6) cho thấy đổi cạnh thì đổi điểm trên cùng tín hiệu. Cả hai là kiểm khả thi của phép tính, không phải bằng chứng lợi ích.

## 6. K6 — Câu còn mở và nơi phân xử

### 6.1 Còn kiểm được trên dev hiện có

| Câu | Phép phân xử (giữ gì, đổi gì) | Đầu vào | Chi phí | Quyết định phụ thuộc |
|---|---|---|---|---|
| Ở cờ một lần độ lệch chuẩn, bước nào đưa dịch vụ gọi lên trên root trong bản TraceRCA theo lời văn? (sau E1) | Giữ mọi thứ như E1, chỉ đổi **bước chọn tập** (luôn giữ tập một dịch vụ đã khai phá) | Trung gian của lượt `e1-001` | Chưa đo; E1 mất 30 giây máy | Có đưa cách chấm theo tập vào P6 không (UV-4) |
| Cờ ở lời gọi đi ra của frontend đến từ đâu? (sau E1) | Đối chiếu cờ theo từng lời gọi giữa bản theo lời văn và nhánh mã tác giả, trên 7 cặp | Bảng lời gọi đã phát lại trên EC2 của T-032 | Chưa đo | Như trên; và cách dùng số TraceRCA ở bảng baseline |
| Underflow có đổi MAP hoặc điểm đổi ở các ca dev còn lại không? (sau E2) | Chạy bản miền log đã kiểm trên đầu vào full của các ca còn lại | NPZ nguồn của T-033 trên EC2 | Mỗi chuỗi full khoảng 909 giây máy; cả lượt vượt một giờ nên phải xin duyệt | Có ghi chú số BOCPD của T-025 không; yêu cầu số học cho P6 (UV-9) |
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
Trên RE2-TT, khi biết mốc tiêm, theo điểm ước lượng: TORAI B (Hit@1 0,867) và SimpleRCA (0,833), cả hai không dựa vào quan hệ gọi để xếp root; khoảng bootstrap của chúng chồng với BARO và TraceRCA. Trên Nezha-OB không phương pháp nào mạnh: cao nhất là BARO 0,364. Không phương pháp nào tốt ở mọi ô. *Mức: MT (bảng chấm đã kiểm lại độc lập). Nguồn:* mục 2.1–2.4; `results/T-034/bang-baseline.json`.

**5. Số của nhóm có khớp số đã công bố không?**
BARO và TORAI bản gốc khớp số công bố trên dataset của bài. SimpleRCA chưa tái lập được vì bài báo trên cả bộ, phần test đang khóa. MicroRank và TraceRCA trong thư viện khác bài gốc; CIRCA lệch ở mức ô. Trên RE2-TT với giao thức của nhóm thì chỉ so tham khảo. *Mức: MT. Nguồn:* mục 2.7.

**6. Các phương pháp xếp hạng hỏng ở đâu, vì sao?**
Đã lần được tới bước gây sai ở phần lớn nhóm: bước chia trace của MicroRank; TraceRCA bản thư viện chấm thời gian chờ thành bất thường của dịch vụ gọi; BARO chia cho độ biến thiên của nền gần phẳng; SimpleRCA để phiếu metric lấn át; CIRCA có phần dư gần bằng không rồi cộng điểm lên nút cha. Phần chưa phân xử: vì sao dịch vụ không liên hệ đổi tại mốc. *Mức: CT ở các dòng nêu trên. Nguồn:* mục 3, dòng G2-H01 đến G2-H15.

**7. Bộ phát hiện hỏng ở đâu, vì sao?**
Cả hai bộ đều báo động trước mốc tiêm ở hầu hết ca (3/30 và 0/30 ca có báo động đầu đúng). Đã xác lập: tiền xử lý của BOCPD dùng cả dữ liệu sau mốc; kết quả nhạy với prior. Chưa phân xử: các báo động trước mốc là sai hay là biến động thật, vì dataset không có nền sạch và onset được xác nhận độc lập. *Mức: CT cho hai điều đã xác lập; CK cho điều chưa phân xử. Nguồn:* mục 2.5 và dòng G2-H20 đến G2-H24.

**8. “Nhầm triệu chứng lan với nguyên nhân” có đáng kể không?**
Lan là hiện tượng phổ biến ở mức quan sát: độ trễ của root hiện ở phía gọi trong phần lớn ca đo được. Nhưng chưa có căn cứ nói nó gây ra phần lớn ca sai: nó được xác lập cho TraceRCA bản thư viện và lỗi trễ mạng ở Nezha-OB; ở MicroRank và BARO, đa số thực thể đứng trên root không nằm phía trên root (riêng MicroRank còn một đường gián tiếp chưa phân xử). Hiện tượng chờ cũng có ở ca đúng. Câu “đáng kể” chưa phân xử thành một tỷ lệ. *Mức: ĐC cho hiện tượng; CT cho TraceRCA; chưa phân xử cho câu tổng. Nguồn:* mục 4.

**9. Lỗi là do dữ liệu, do bản cài hay do phương pháp?**
Cả ba, và đã tách ở từng dòng của bản đồ. Do bản cài hoặc đầu vào ta dựng: MicroRank, TraceRCA bản thư viện, bảng log TORAI nguồn B. Do cách tính: BARO, SimpleRCA, CIRCA. Do dữ liệu: nền ngắn ở Nezha-OB, root không được gọi, thiếu onset. *Mức: theo từng dòng. Nguồn:* mục 3.1, cột “Loại nguồn”.

**10. TraceRCA theo mã tác giả cho kết quả thế nào?**
Nhánh chỉ dùng độ trễ của mã tác giả đúng 11/22 ca kỳ vọng ở Nezha-OB và 17/30 ca ở RE2-TT (ngưỡng chọn đặc trưng một). Đây là chẩn đoán trên dev đã nhìn, không phải tái lập bài: đầu vào thiếu trạng thái HTTP và nền nhiều ngày. Có đưa nó vào kế hoạch baseline hay không là việc Minh quyết. *Mức: MT. Nguồn:* mục 2.8.

**11. Hai phép kiểm bổ sung cho biết gì?**
Phép E1: ở cấu hình mặc định của bài TraceRCA, quy tắc chấm qua tập nhiều dịch vụ không phải bước đưa dịch vụ gọi lên trên root (1/7 cặp đổi chiều); ở mức cờ cao thì có (4/5). Phép E2: underflow làm đổi điểm đổi của BOCPD ở 1/4 chuỗi, trong một đoạn ngắn sau mốc; không giải thích báo động trước mốc. *Mức: CT, trong phạm vi đã khai. Nguồn:* `results/T-034/hai-phep-kiem.md`.

**12. Câu nào chưa trả lời được, và kế hoạch?**
Ba nhóm. Còn kiểm được trên dev: sáu phép ở mục 6.1. Thiếu quan sát: onset, nền sạch, quan hệ dịch vụ–máy; chuyển thành yêu cầu quan sát cho FlashTicket. Thuộc đánh giá sau: đồ thị có giúp không. *Mức: CK. Nguồn:* mục 6.

**13. Đồ thị sẽ nhắm vào hạn chế nào?**
Bốn ứng viên có căn cứ để thử: gắn thời gian lời gọi lên cạnh và tính cho dịch vụ được gọi; thời gian tự xử lý theo quan hệ cha–con; tiêu chí yêu cầu bất thường theo cây lời gọi; chặn giá trị không hợp lệ khi lan điểm. Các thành phần khác (cạnh thông điệp, cạnh dữ liệu, vùng nghi ngờ) làm vì DT18 yêu cầu, không vì một hạn chế đã thấy. *Mức: ĐC hoặc CT cho căn cứ đề xuất; chưa có bằng chứng lợi ích. Nguồn:* mục 5.

**14. Khi nào biết đồ thị có giúp không?**
Sau P7, khi đủ ba thứ: hơn nhánh cùng bằng chứng không dùng quan hệ; hơn đồ thị ngẫu nhiên giữ bậc; báo theo ô và theo ca. Trên dev đã có các điều bất lợi: baseline không dựa vào quan hệ gọi mạnh trên RE2-TT; phần lớn cặp sai của hai phương pháp không nằm phía trên root. “Đồ thị không giúp ở điều kiện X, vì Y” là một kết quả hợp lệ. *Mức: CK. Nguồn:* MRP §6; mục 0 và mục 5.

**15. Vì sao chưa trình kết quả phương pháp đồ thị?**
Cô yêu cầu chỉ ra hạn chế của phương pháp đã có rồi mới sang đồ thị. Gói này là bước đó. Thiết kế đồ thị (P5, P6) bắt đầu sau khi Minh duyệt cổng này; kết quả dự kiến cuối tháng 11/2026. *Nguồn:* MRP §2.1, §7; quyết định Q-70.

## 8. Điểm Minh quyết ở G2

**Đã quyết từ trước, gói này giữ nguyên:** bảng baseline và cách chấm đã khóa (T-024, T-025, T-026); CIRCA dùng bản gốc và báo riêng nhóm ca (Q-82); không dùng Eadro tới G2 (Q-83); câu “lan” xử lý ở gói này (Q-86).

**Cần Minh quyết:**

1. **Duyệt cổng G2:** bảng baseline trên dev (mục 2) và bản đồ hạn chế (mục 3).
2. **Nhánh TraceRCA theo mã tác giả** (mục 2.8): (a) chỉ giữ làm chẩn đoán; hay (b) đưa vào kế hoạch baseline của P7, khi đó phải khai hợp đồng đầu vào, cấu hình, quy tắc hòa và cách xử lý ca thiếu bằng chứng trước khi mở test. Tôi không tự chọn ngưỡng theo điểm dev.
3. **Nhãn lan** (mục 4.3): (a) mở một task nhỏ hoàn thiện nháp và khóa ở G3; hay (b) không tách nhóm lan ở P7.
4. **Bốn ca ERROR** của MicroRank và TraceRCA ở RE2-TT: gói giữ cách chấm đã khóa (tính trượt, WHY-28). Đề nghị trình kèm một dòng chẩn đoán: khi bỏ thao tác thiếu nền, TraceRCA xếp root hạng 1 ở 3/4 ca đó (G2-H16). Minh quyết có trình kèm không.
5. **TORAI nguồn B:** bảng log do ta dựng làm sai 4 ca, bỏ nguồn log thì sửa 3 ca (G2-H14). Giữ nguồn B làm dòng chính như đã khóa, hay thêm một dòng độ nhạy “bỏ nguồn log” khi trình bảng. Không đổi baseline.
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
| auth / cpu | 3 | 3 | 0 | 0 | 3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 |
| auth / delay | 3 | 1 | 0 | 0 | 1 | 0/1 | 0/1 | 1/1 | 1/1 | 0/1 |
| order / disk | 3 | 3 | 0 | 1 | 2 | 1/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| order / loss | 3 | 3 | 0 | 1 | 2 | 0/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| route / mem | 3 | 2 | 1 | 0 | 2 | 2/2 | 2/2 | 2/2 | 1/2 | 1/2 |
| route / socket | 3 | 2 | 1 | 0 | 2 | 1/2 | 1/2 | 2/2 | 1/2 | 0/2 |
| train / cpu | 3 | 3 | 0 | 0 | 3 | 0/3 | 1/3 | 3/3 | 3/3 | 0/3 |
| train / delay | 3 | 2 | 1 | 0 | 2 | 1/2 | 1/2 | 2/2 | 2/2 | 0/2 |
| travel / disk | 3 | 3 | 0 | 1 | 2 | 2/3 | 3/3 | 2/3 | 1/3 | 0/3 |
| travel / loss | 3 | 2 | 1 | 2 | 0 | 2/2 | 2/2 | 0/2 | 0/2 | 0/2 |

**Nezha-OB / MicroRank**

| Ô | Số ca | Sai hạng 1 (chạy được) | Không chạy được | Cờ M5 | Cờ M6 | Cờ M0 | Phép đổi: chia trace theo bài gốc (mo15) | Phép đổi: chia trace theo bài gốc (mo1p50) | Phép đổi: đếm riêng (M-C1) | Phép đổi: trọng số đơn vị (A′) | Phép đổi: cờ theo phần chưa phủ (M-D) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ad / cpu_contention | 1 | 1 | 0 | 1 | 0 | 0 | 1/1 | 1/1 | 0/1 | 0/1 | 0/1 |
| checkout / exception | 2 | 2 | 0 | 2 | 0 | 0 | 1/2 | 1/2 | 0/2 | 0/2 | 0/2 |
| checkout / network_delay | 2 | 2 | 0 | 2 | 0 | 0 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| checkout / return | 2 | 2 | 0 | 2 | 0 | 0 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| email / cpu_consumed | 1 | 1 | 0 | 1 | 0 | 0 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 |
| email / network_delay | 2 | 2 | 0 | 2 | 1 | 0 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| frontend / return | 2 | 2 | 0 | 0 | 0 | 2 | 2/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| payment / cpu_contention | 2 | 2 | 0 | 2 | 0 | 0 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| productcatalog / exception | 1 | 1 | 0 | 1 | 0 | 0 | 0/1 | 0/1 | 0/1 | 0/1 | 1/1 |
| recommendation / cpu_consumed | 2 | 2 | 0 | 2 | 0 | 0 | 1/2 | 2/2 | 1/2 | 0/2 | 0/2 |
| recommendation / network_delay | 2 | 2 | 0 | 2 | 0 | 0 | 1/2 | 2/2 | 0/2 | 0/2 | 0/2 |
| shipping / cpu_consumed | 1 | 1 | 0 | 1 | 0 | 0 | 1/1 | 1/1 | 1/1 | 0/1 | 0/1 |
| shipping / cpu_contention | 2 | 2 | 0 | 2 | 0 | 0 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 |

**RE2-TT / TraceRCA**

| Ô | Số ca | Sai hạng 1 (chạy được) | Không chạy được | Cờ M5 | Cờ M0 | Phép đổi: cờ theo phần chưa phủ (T-D) | Phép đổi: bước xếp hạng theo lời văn (to_p) |
|---|---|---|---|---|---|---|---|
| auth / cpu | 3 | 0 | 0 | 0 | 0 | — | — |
| auth / delay | 3 | 0 | 0 | 0 | 0 | — | — |
| order / disk | 3 | 1 | 0 | 1 | 0 | 0/1 | 0/1 |
| order / loss | 3 | 3 | 0 | 2 | 1 | 0/3 | 0/3 |
| route / mem | 3 | 0 | 1 | 0 | 0 | — | — |
| route / socket | 3 | 0 | 1 | 0 | 0 | — | — |
| train / cpu | 3 | 0 | 0 | 0 | 0 | — | — |
| train / delay | 3 | 0 | 1 | 0 | 0 | — | — |
| travel / disk | 3 | 1 | 0 | 1 | 0 | 1/1 | 0/1 |
| travel / loss | 3 | 0 | 1 | 0 | 0 | — | — |

**Nezha-OB / TraceRCA**

| Ô | Số ca | Sai hạng 1 (chạy được) | Không chạy được | Cờ M2 | Cờ M3 | Cờ M5 | Cờ M6 | Cờ M0 | Phép đổi: cờ theo phần chưa phủ (T-D) | Phép đổi: bước xếp hạng theo lời văn (to_p) |
|---|---|---|---|---|---|---|---|---|---|---|
| ad / cpu_contention | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0/1 | 0/1 |
| checkout / exception | 2 | 2 | 0 | 0 | 0 | 2 | 0 | 0 | 0/2 | 0/2 |
| checkout / network_delay | 2 | 2 | 0 | 0 | 0 | 2 | 0 | 0 | 0/2 | 0/2 |
| checkout / return | 2 | 2 | 0 | 0 | 0 | 2 | 0 | 0 | 0/2 | 0/2 |
| email / cpu_consumed | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 1/1 | 0/1 |
| email / network_delay | 2 | 2 | 0 | 1 | 0 | 1 | 1 | 0 | 0/2 | 0/2 |
| frontend / return | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0/2 | 0/2 |
| payment / cpu_contention | 2 | 2 | 0 | 0 | 0 | 2 | 0 | 0 | 0/2 | 0/2 |
| productcatalog / exception | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0/1 | 0/1 |
| recommendation / cpu_consumed | 2 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0/1 | 0/1 |
| recommendation / network_delay | 2 | 2 | 0 | 0 | 0 | 2 | 0 | 0 | 0/2 | 0/2 |
| shipping / cpu_consumed | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | — |
| shipping / cpu_contention | 2 | 2 | 0 | 0 | 0 | 2 | 0 | 0 | 0/2 | 0/2 |

**Nezha-OB / BARO**

| Ô | Số ca | Sai hạng 1 (chạy được) | Không chạy được | Cờ M5 | Cờ M0 | Phép đổi: thang độ lệch chuẩn (B-2) |
|---|---|---|---|---|---|---|
| ad / cpu_contention | 1 | 0 | 0 | 0 | 0 | — |
| checkout / exception | 2 | 1 | 0 | 1 | 0 | 0/1 |
| checkout / network_delay | 2 | 2 | 0 | 0 | 2 | 0/2 |
| checkout / return | 2 | 2 | 0 | 1 | 1 | 0/2 |
| email / cpu_consumed | 1 | 0 | 0 | 0 | 0 | — |
| email / network_delay | 2 | 2 | 0 | 1 | 1 | 1/2 |
| frontend / return | 2 | 2 | 0 | 0 | 2 | 0/2 |
| payment / cpu_contention | 2 | 0 | 0 | 0 | 0 | — |
| productcatalog / exception | 1 | 1 | 0 | 1 | 0 | 0/1 |
| recommendation / cpu_consumed | 2 | 1 | 0 | 0 | 1 | 0/1 |
| recommendation / network_delay | 2 | 2 | 0 | 2 | 0 | 0/2 |
| shipping / cpu_consumed | 1 | 1 | 0 | 1 | 0 | 1/1 |
| shipping / cpu_contention | 2 | 0 | 0 | 0 | 0 | — |

**Nezha-OB / SimpleRCA**

| Ô | Số ca | Sai hạng 1 (chạy được) | Không chạy được | Cờ M5 | Cờ M6 | Cờ M0 | Phép đổi: đếm theo cột (S-1) |
|---|---|---|---|---|---|---|---|
| ad / cpu_contention | 1 | 0 | 0 | 0 | 0 | 0 | — |
| checkout / exception | 2 | 2 | 0 | 2 | 0 | 0 | 0/2 |
| checkout / network_delay | 2 | 1 | 0 | 1 | 1 | 0 | 0/1 |
| checkout / return | 2 | 2 | 0 | 1 | 0 | 1 | 0/2 |
| email / cpu_consumed | 1 | 1 | 0 | 1 | 0 | 0 | 1/1 |
| email / network_delay | 2 | 2 | 0 | 1 | 0 | 1 | 0/2 |
| frontend / return | 2 | 2 | 0 | 0 | 0 | 2 | 0/2 |
| payment / cpu_contention | 2 | 0 | 0 | 0 | 0 | 0 | — |
| productcatalog / exception | 1 | 0 | 0 | 0 | 0 | 0 | — |
| recommendation / cpu_consumed | 2 | 2 | 0 | 0 | 0 | 2 | 0/2 |
| recommendation / network_delay | 2 | 2 | 0 | 2 | 1 | 0 | 0/2 |
| shipping / cpu_consumed | 1 | 1 | 0 | 1 | 0 | 0 | 1/1 |
| shipping / cpu_contention | 2 | 0 | 0 | 0 | 0 | 0 | — |

**RE2-TT / SimpleRCA**

| Ô | Số ca | Sai hạng 1 (chạy được) | Không chạy được | Cờ M5 | Phép đổi: đếm theo cột (S-1) |
|---|---|---|---|---|---|
| auth / cpu | 3 | 0 | 0 | 0 | — |
| auth / delay | 3 | 0 | 0 | 0 | — |
| order / disk | 3 | 0 | 0 | 0 | — |
| order / loss | 3 | 1 | 0 | 1 | 1/1 |
| route / mem | 3 | 0 | 0 | 0 | — |
| route / socket | 3 | 0 | 0 | 0 | — |
| train / cpu | 3 | 0 | 0 | 0 | — |
| train / delay | 3 | 2 | 0 | 2 | 0/2 |
| travel / disk | 3 | 0 | 0 | 0 | — |
| travel / loss | 3 | 2 | 0 | 2 | 0/2 |

**RE2-TT / BARO**

| Ô | Số ca | Sai hạng 1 (chạy được) | Không chạy được | Cờ M5 | Cờ M0 | Phép đổi: thang độ lệch chuẩn (B-2) |
|---|---|---|---|---|---|---|
| auth / cpu | 3 | 2 | 0 | 0 | 2 | 2/2 |
| auth / delay | 3 | 3 | 0 | 0 | 3 | 0/3 |
| order / disk | 3 | 0 | 0 | 0 | 0 | — |
| order / loss | 3 | 1 | 0 | 1 | 0 | 0/1 |
| route / mem | 3 | 1 | 0 | 0 | 1 | 1/1 |
| route / socket | 3 | 0 | 0 | 0 | 0 | — |
| train / cpu | 3 | 0 | 0 | 0 | 0 | — |
| train / delay | 3 | 0 | 0 | 0 | 0 | — |
| travel / disk | 3 | 0 | 0 | 0 | 0 | — |
| travel / loss | 3 | 2 | 0 | 2 | 0 | 0/2 |

**RE2-TT / CIRCA**

| Ô | Số ca | Sai hạng 1 (chạy được) | Không chạy được | Cờ M4 | Cờ M5 | Cờ M0 | Phép đổi: bỏ mọi cạnh, RHT (K-2) |
|---|---|---|---|---|---|---|---|
| auth / cpu | 3 | 1 | 0 | 0 | 0 | 1 | 1/1 |
| auth / delay | 3 | 3 | 0 | 0 | 0 | 3 | 0/3 |
| order / disk | 3 | 0 | 0 | 0 | 0 | 0 | — |
| order / loss | 3 | 1 | 0 | 0 | 1 | 0 | 0/1 |
| route / mem | 3 | 1 | 0 | 1 | 1 | 0 | 1/1 |
| route / socket | 3 | 2 | 0 | 2 | 2 | 0 | 2/2 |
| train / cpu | 3 | 3 | 0 | 3 | 3 | 0 | 3/3 |
| train / delay | 3 | 2 | 0 | 2 | 2 | 0 | 2/2 |
| travel / disk | 3 | 0 | 0 | 0 | 0 | 0 | — |
| travel / loss | 3 | 1 | 0 | 0 | 1 | 0 | 0/1 |

**RE2-TT / TORAI B**

| Ô | Số ca | Sai hạng 1 (chạy được) | Không chạy được | Cờ M5 | Cờ M0 | Phép đổi: bỏ nguồn log, seed 0 (tl1) |
|---|---|---|---|---|---|---|
| auth / cpu | 3 | 2 | 0 | 0 | 2 | 2/2 |
| auth / delay | 3 | 0 | 0 | 0 | 0 | — |
| order / disk | 3 | 0 | 0 | 0 | 0 | — |
| order / loss | 3 | 1 | 0 | 1 | 0 | 0/1 |
| route / mem | 3 | 0 | 0 | 0 | 0 | — |
| route / socket | 3 | 0 | 0 | 0 | 0 | — |
| train / cpu | 3 | 0 | 0 | 0 | 0 | — |
| train / delay | 3 | 0 | 0 | 0 | 0 | — |
| travel / disk | 3 | 0 | 0 | 0 | 0 | — |
| travel / loss | 3 | 1 | 0 | 0 | 1 | 1/1 |

## Phụ lục B — Phát hiện theo ô: các cờ HP của T-029

Mỗi ô ghi số ca có cờ trên số ca hợp lệ. Ý nghĩa từng cờ ở `results/T-029/ban-do-han-che-phat-hien.md`.

**HP-6** (thuộc G2-H20)

| Ô | BOCPD |
|---|---|
| auth / cpu | 2/2 |
| auth / delay | 2/3 |
| order / disk | 3/3 |
| order / loss | 2/2 |
| route / mem | 1/3 |
| route / socket | 2/3 |
| train / cpu | 0/2 |
| train / delay | 2/3 |
| travel / disk | 2/3 |
| travel / loss | 1/3 |

**HP-5** (thuộc G2-H21)

| Ô | BOCPD |
|---|---|
| auth / cpu | 0/2 |
| auth / delay | 0/3 |
| order / disk | 0/3 |
| order / loss | 0/2 |
| route / mem | 0/3 |
| route / socket | 0/3 |
| train / cpu | 0/2 |
| train / delay | 0/3 |
| travel / disk | 0/3 |
| travel / loss | 0/3 |

**HP-7** (thuộc G2-H21)

| Ô | BOCPD |
|---|---|
| auth / cpu | 0/0 |
| auth / delay | 0/1 |
| order / disk | 0/0 |
| order / loss | 0/0 |
| route / mem | 0/2 |
| route / socket | 0/1 |
| train / cpu | 0/2 |
| train / delay | 0/1 |
| travel / disk | 0/1 |
| travel / loss | 0/2 |

**HP-8** (thuộc G2-H21)

| Ô | BOCPD |
|---|---|
| auth / cpu | 2/2 |
| auth / delay | 2/3 |
| order / disk | 3/3 |
| order / loss | 2/2 |
| route / mem | 1/3 |
| route / socket | 2/3 |
| train / cpu | 1/2 |
| train / delay | 3/3 |
| travel / disk | 2/3 |
| travel / loss | 2/3 |

**HP-9 (D0)** (thuộc G2-H21)

| Ô | BOCPD | N-Sigma | N-Sigma đối chứng |
|---|---|---|---|
| auth / cpu | 1/3 | 0/3 | 0/3 |
| auth / delay | 0/3 | 0/3 | 0/3 |
| order / disk | 0/3 | 0/3 | 0/3 |
| order / loss | 1/3 | 0/3 | 0/3 |
| route / mem | 2/3 | 0/3 | 0/3 |
| route / socket | 0/3 | 0/3 | 0/3 |
| train / cpu | 2/3 | 0/3 | 0/3 |
| train / delay | 0/3 | 0/3 | 0/3 |
| travel / disk | 1/3 | 0/3 | 0/3 |
| travel / loss | 1/3 | 0/3 | 0/3 |

**HP-1** (thuộc G2-H22)

| Ô | N-Sigma | N-Sigma đối chứng |
|---|---|---|
| auth / cpu | 0/3 | 1/3 |
| auth / delay | 0/3 | 0/3 |
| order / disk | 2/3 | 0/3 |
| order / loss | 1/3 | 0/3 |
| route / mem | 1/3 | 1/3 |
| route / socket | 0/3 | 1/3 |
| train / cpu | 1/3 | 0/3 |
| train / delay | 0/3 | 0/3 |
| travel / disk | 0/3 | 1/3 |
| travel / loss | 0/3 | 0/3 |

**HP-2** (thuộc G2-H22)

| Ô | N-Sigma | N-Sigma đối chứng |
|---|---|---|
| auth / cpu | 1/3 | 3/3 |
| auth / delay | 2/3 | 3/3 |
| order / disk | 0/3 | 3/3 |
| order / loss | 1/3 | 3/3 |
| route / mem | 0/3 | 3/3 |
| route / socket | 0/3 | 2/3 |
| train / cpu | 1/3 | 3/3 |
| train / delay | 0/3 | 3/3 |
| travel / disk | 0/3 | 3/3 |
| travel / loss | 1/3 | 3/3 |

**HP-3** (thuộc G2-H22)

| Ô | N-Sigma | N-Sigma đối chứng |
|---|---|---|
| auth / cpu | 2/3 | 0/3 |
| auth / delay | 1/3 | 0/3 |
| order / disk | 3/3 | 0/3 |
| order / loss | 2/3 | 0/3 |
| route / mem | 3/3 | 0/3 |
| route / socket | 3/3 | 1/3 |
| train / cpu | 2/3 | 0/3 |
| train / delay | 3/3 | 0/3 |
| travel / disk | 3/3 | 0/3 |
| travel / loss | 2/3 | 0/3 |

**HP-4** (thuộc G2-H22)

| Ô | N-Sigma | N-Sigma đối chứng |
|---|---|---|
| auth / cpu | 0/3 | 1/3 |
| auth / delay | 0/3 | 2/3 |
| order / disk | 0/3 | 0/3 |
| order / loss | 0/3 | 0/3 |
| route / mem | 0/3 | 0/3 |
| route / socket | 0/3 | 0/3 |
| train / cpu | 0/3 | 0/3 |
| train / delay | 0/3 | 0/3 |
| travel / disk | 0/3 | 0/3 |
| travel / loss | 0/3 | 0/3 |
