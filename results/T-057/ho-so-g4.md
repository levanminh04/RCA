# Hồ sơ G4 — kết quả và phân tích P7(a)

T-057. Người làm: Claude. Người phản biện: Codex. Ngày lập: 09/11/2026. Trạng thái: **chờ phản biện**.
Hồ sơ này xin Minh quyết G4 (MRP §7: "kết quả và phân tích; báo cáo tiến độ cho cô"). Nó không mở dữ liệu mới, không chọn lại thiết kế, không khóa bản FlashTicket.

**Cách đọc.**

- Mọi số là **world P**, chế độ (a): phương pháp được cho biết mốc tiêm lỗi.
- Ba bộ test: RE2-TT 60 ca (Train Ticket), Nezha-OB 34 ca (Online Boutique), RE3-OB 30 ca (Online Boutique, lỗi mã nguồn, dataset giữ ngoài). Không gộp số giữa các bộ (WHY-06).
- *Root* là thành phần gốc theo nhãn. *Ô* là cặp (root, loại lỗi). *Δ* là vế trái trừ vế phải. *T/H/T* là số ca thắng/hòa/thua.
- CI là bootstrap cặp theo ô (10.000 mẫu), chỉ để mô tả, trừ A4 đã khóa.
- Câu của T-054, T-055, T-056 được trích theo **câu hiện hành** đã gộp đính chính: [`cau-hien-hanh.md`](cau-hien-hanh.md) (mã C01–C28).
- Viết tắt nguồn: A = `results/T-054/reports/main-013-v2/a4.json`; PT = `results/T-054/reports/p7a-013-v2/phan-tich-nhom.json`; R = `results/T-055/reports/re3/phan-tich-re3.json`; K, K2 = `results/T-056/ket-qua.json`, `ket-qua-002.json`; DEV = `results/T-052/ket-qua-dev.json`. File của T-057 dẫn bằng tên trong `results/T-057/`.
- Mọi số được soát bằng máy: [`soat-so.json`](soat-so.json).

---

## 0. Tóm tắt

**Câu trả lời ngắn cho câu hỏi "phương pháp đồ thị có tốt hơn baseline không".** Không bộ nào cho thấy M1 hơn rõ baseline mạnh nhất.

| Bộ | Mốc so sánh (Q-247) | Kết quả | Đọc |
|---|---|---|---|
| RE2-TT | TORAI B, MRR | Δ = 0,044, CI [−0,033; 0,149], T/H/T 7/50/3 | Đạt E-04 theo công thức; chưa phân biệt hơn/kém |
| Nezha-OB | SimpleRCA M4, Hit@5 | Δ = 0,088 (3/34), 3 ô hữu hiệu, không đạt | Chưa phân xử; dữ liệu không đủ sức (p nhỏ nhất có thể 1/8) |
| RE3-OB | SimpleRCA M4, MRR (mô tả) | Δ = −0,050, CI [−0,133; 0,033], T/H/T 1/25/4 | M1 thấp hơn theo điểm; CI chứa 0 |

Nguồn: `A#/TT/P/delta`, `A#/TT/P/E04`, `A#/TT/P/counts`; `A#/OB/P/delta`, `A#/OB/P/pass_formula`; `R#/so_cap/M1-simplerca|rr`.

**Dùng quan hệ có giúp không (RQ3d).** Chỉ có điều kiện:

- Trên Nezha-OB, M1 hơn nhánh bỏ quan hệ C-a0: MRR 0,875 so với 0,711, T/H/T 11/20/3. Phần hơn nằm ở **bước dựng bằng chứng dùng quan hệ cha–con của span** (E1, E2), không ở bước xếp hạng trên đồ thị: M1 gần bằng quy tắc "khởi phát sớm nhất" C-d2 (Δ −0,0025).
- Trên RE2-TT và RE3-OB, M1 bằng C-a0 (Δ = 0 ở cả hai bộ).
- Không có đối chứng đồ thị ngẫu nhiên (M-25). Vì vậy không kết luận gì về lợi ích của cấu trúc phụ thuộc thật.

**Cơ chế đọc được.** Có cơ chế đủ chuỗi đầu vào → trung gian → đầu ra cho: E2 ở lỗi trễ mạng OB (C08), E1 ở lỗi CPU, và điều kiện làm khóa xếp max-z sai ở 8/14 ca sai (§10). Còn mở: nguồn của các kênh hẹp cực trị, vai trò riêng của E2 trong tương tác E1×E5 (C07), và R1 trên OB.

**Thiếu so với DT18 và cô.** Không có Precision/Recall/F1 phát hiện (RQ3a, Q-245), không có P/R/F1 vùng (thiếu nhãn vùng), chưa có LLM (P8 hoãn), chưa có FlashTicket. Cạnh dữ liệu và thông điệp không có trong trace của dataset công khai.

---

## 1. Toàn vẹn nguồn và tiếp xúc test

- **Hash.** `verify_manifest.py --documents` của T-054: 515 mục, lệch duy nhất `docs/LESSONS.md` (đã biết). Kiểm 16 manifest của T-034, T-052, T-054, T-055, T-056: 1062/1065 file khớp; 3 file `src` lệch pin cũ của T-052 nhưng khớp pin của lượt test main013-v2 ([`b0-kiem-hash.json`](b0-kiem-hash.json)).
- **Tiếp xúc test trong T-057.** Chỉ đọc đầu ra đã lưu và nhãn đã ghép sau seal. Không đọc `data/locked/`, không đọc lại dữ liệu thô test, không chạy phương pháp. Mọi phân tích trên test là **mô tả sau khi đã xem**.

**Sổ C-15 B: phần nào là kết quả đầu của bản khóa, phần nào là sửa hoặc phân tích sau khi xem test.**

| Mục | Loại | Hệ quả cho kết luận |
|---|---|---|
| A4 TT/OB, bảng chính P7(a) (`results/T-054/reports/main-013-v2/`) | Kết quả đầu của bản khóa | Kết quả chính |
| RE3-OB lượt chính (T-055) | Kết quả đầu, mở một lần cho bản cuối | Kết quả chính, chỉ mô tả |
| v1 → v2 (quy tắc INSUFFICIENT_NORMAL_SPANS) | Sửa phân loại lỗi trước khi xem điểm/nhãn; 740/740 slot trùng | Không đổi kết quả |
| D1: adapter OB sửa sau khi đọc cấu trúc thời gian của cohort OB | Đã dùng dữ liệu test để sửa cài đặt | OB không là phép kiểm độc lập hoàn toàn; phần E1 OB giảm còn +0,079 khi bỏ 4 ca D1 (C02) |
| C-d3 OB bổ sung (wrapper span gốc) | Sửa sau khi xem test | Chỉ mô tả (C09, C10) |
| Lệch số worker RE3 (2 thay vì 1) | Lệch bố trí chưa khai lúc chạy | Không slot TIMEOUT; chưa chứng minh không ảnh hưởng mọi baseline (C17) |
| Đính chính T-054 001–004, T-055 001, T-056 và T-057 | Phân tích sau khi xem | Chỉ mô tả; ứng viên sửa thiết kế ở §13 là "chưa kiểm" |

---

## 2. Bảng kết quả chính ba bộ

MRR, Hit@1, Avg@5 (= trung bình AC@1..5 của RCAEval), NDCG@5. Nguồn: [`so-cong-bo.json`](so-cong-bo.json)`#/bang/<bộ>/<vế>`, tính lại từ bảng dòng và khớp PT, R (0 lệch; dòng CIRCA RE3 dùng R).

| Vế | TT MRR | TT Hit@1 | TT Avg@5 | OB MRR | OB Hit@1 | OB Avg@5 | RE3 MRR | RE3 Hit@1 | RE3 Avg@5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| M1 | 0,975 | 0,950 | 0,990 | 0,875 | 0,794 | 0,924 | 0,925 | 0,867 | 0,960 |
| C-a0 (bỏ E1/E2/E5) | 0,975 | 0,950 | 0,990 | 0,711 | 0,559 | 0,788 | 0,925 | 0,867 | 0,960 |
| C-d2 (khởi phát sớm nhất) | 0,964 | 0,933 | — | 0,877 | 0,794 | — | 0,789 | 0,667 | — |
| SimpleRCA M4 | 0,876 | 0,800 | 0,923 | 0,689 | 0,529 | 0,756 | 0,975 | 0,950 | 0,990 |
| TORAI B | 0,931 | 0,894 | 0,946 | không hỗ trợ | — | — | 0,544 | 0,133 | 0,793 |
| BARO | 0,806 | 0,733 | 0,830 | 0,534 | 0,324 | 0,618 | 0,487 | 0,000 | 0,773 |

- Hit@5 của M1 bằng 1 ở 60/60, 34/34, 30/30 ca: độ đo **chạm trần** ([`kha-nang-phan-xu.json`](kha-nang-phan-xu.json)`#/tran`).
- CIRCA và TORAI B không hỗ trợ Nezha-OB theo thiết kế (không phải điểm 0).
- Bảng đủ mọi vế: T-054 `bao-cao.md` §4 (với C01), T-055 `bao-cao-re3.md` §2.

---

## 3. Trạng thái từng câu hỏi nghiên cứu

| Câu | Trạng thái | Điều kiện đúng / không đúng | Cơ chế | Phần thiếu và dữ liệu cần | Quyết định phụ thuộc |
|---|---|---|---|---|---|
| RQ3a (P/R/F1 phát hiện) | **Chưa trả lời** | — | M1 trả CAUSE_FOUND ở 58/58 ca TT tại t−300 (trước tiêm, nền lành chưa xác nhận), trung bình 16,4 thực thể tầng 1/ca: M1 không có ngưỡng phát hiện đã hiệu chuẩn | Chế độ (b) hoãn (Q-245). Mức hệ thống giao luật Grafana (M-38). Cần đợt có (b) hoặc FlashTicket có đoạn nền xác nhận | Khóa bản FlashTicket (D3/D16); câu hỏi cô M-20 |
| RQ3b (xếp hạng so baseline) | **Một phần** | TT: không thua quá 0,05 theo công thức, chưa phân biệt hơn/kém. OB: chênh dương, chưa phân xử. RE3: thấp hơn M4 theo điểm, CI chứa 0 | M1 hơn M4 ở lỗi trễ mạng OB nhờ E2; kém M4 khi root lệch bền nhưng đối thủ có một kênh cực trị (§10) | Dữ liệu khó hơn, nhiều ô hữu hiệu hơn (§4 câu 2) | G4; thiết kế FlashTicket |
| RQ3c (vùng ảnh hưởng) | **Chỉ vùng nghi ngờ** | Vùng cách 1 chứa root: TT 0,950, OB 0,824, RE3 0,900; cỡ 3,90 / 1,38 / 1,60 thực thể | Vùng dựng quanh nhóm đầu, nên tỷ lệ chứa root đi theo độ đúng hạng 1 | Nhãn vùng độc lập với đầu vào RCA (P10, SL18) | P10 |
| RQ3d (dùng quan hệ) | **Một phần** | OB: có, ở lỗi mạng và CPU, do bước dựng kênh. TT, RE3: không thấy. Quy tắc đơn giản: OB M1 ≈ C-d2; RE3 M1 hơn C-d2 (Δ 0,136, CI [0,028; 0,258]) nhưng chưa hơn C-d1 (Δ −0,025) | §5, §6 | Không có đồ thị ngẫu nhiên (M-25): không nói về cấu trúc thật. Phân rã E1/E2/E5 trên OB cần cấu hình chưa chạy (H12) | Câu kết luận cho cô; thiết kế FlashTicket |
| RQ4 | Hoãn (P8) | — | — | — | — |
| RQ5 | Không thuộc G4 | — | — | P10 | — |

Nguồn RQ3c: [`vung-ve-bo-quan-he.json`](vung-ve-bo-quan-he.json)`#/tom_tat/<bộ>/M1/cach_1`. RQ3a: [`kha-nang-phan-xu.json`](kha-nang-phan-xu.json)`#/H7`. RQ3d RE3: `R#/so_cap/M1-C-d2|rr`, `R#/so_cap/M1-C-d1|rr` (C15).

---

## 4. Sáu câu của cổng (MRP §7)

**Câu 1 — Phục vụ câu nào của cô hoặc DT18?**
Bước 3 và 4 của cô: thử trên dataset công khai, so với RCA cơ sở bằng MRR, NDCG (§2). DT18-NV3: "phân tích các trường hợp phương pháp hoạt động hiệu quả hoặc còn hạn chế" (§10, §6). DT18-NV2 phần xếp hạng và một phần vùng ảnh hưởng (§3). Bước 2 của cô (đồ thị tham gia phát hiện bất thường) được đo ở §7. Phần chưa phục vụ: P/R/F1 (bước 4) và LLM (bước 5).

**Câu 2 — Dữ liệu có phân xử nổi câu hỏi không?** Phần lớn là không. Số ô hữu hiệu của từng phép so ([`kha-nang-phan-xu.json`](kha-nang-phan-xu.json)`#/A4`, `#/cap_MRR`):

| Phép so | Ô có chênh khác 0 / tổng ô | Phân xử nổi? |
|---|---|---|
| TT M1 − TORAI B (A4) | 6/20 | Không: power câu E-04 khoảng 0,19 (WHY-06) |
| TT M1 − C-a0 | 3/20 | Không |
| OB M1 − M4 (A4, Hit@5) | 3/20 | Không: p nhỏ nhất có thể 1/8 |
| OB M1 − M4 (MRR, mô tả) | 14/20 | Mô tả, CI [0,011; 0,364] |
| OB M1 − C-a0 (MRR, mô tả) | 12/20 | Mô tả, CI [0,054; 0,282] |
| OB M1 − C-d2 | 3/20 | Không |
| RE3 M1 − M4 | 4/10 | Không |
| RE3 M1 − C-a0 | 2/10 | Không |

Thêm ba lý do:

- Hit@5 chạm trần ở cả ba bộ (§2).
- RE2-TT chỉ có 5 root, RE3-OB 4 root.
- Một quy tắc đếm đơn giản (R1: số mẫu metric vượt nền + 3σ) đặt root lệch bền nhất ở 48/60 ca TT và 28/30 ca RE3 (`K2#/tom_tat/<bộ>/root_events_hon_moi_service_khac`). Ở hai bộ này, bài toán gần như giải được bằng tín hiệu của chính root. OB chưa tính được R1 (H11).

**Câu 3 — Baseline đủ mạnh chưa?** Đủ để làm mốc, có ba giới hạn:

- Trên TT, TORAI B (0,931) và SimpleRCA (0,876) mạnh. SimpleRCA trên đủ 90 ca RE2-TT có Hit@1 0,811, cùng cỡ với số bài FSE 2026 báo (0,80; `docs/LESSONS.md:10`, chưa đối chiếu bản in) ([`so-cong-bo.json`](so-cong-bo.json)`#/simplerca_RE2_TT_90_ca`). Chưa gọi là tái lập.
- Trên OB chỉ so được với M4, BARO, TraceRCA, MicroRank; CIRCA và TORAI B không hỗ trợ. M4 có giới hạn tái lập Q-192.
- TraceRCA và MicroRank là bản RCAEval khác bài gốc ở bước quyết định (T-034 G2-H01, G2-H03). TORAI A chỉ có 6/180 slot (C05). Trên RE3, SimpleRCA là vế mạnh nhất (0,975).

**Câu 4 — Giá trị trung gian có hợp lý không?** Đã soi và lần các chỗ bất thường:

- Hạng tính lại từ khối khớp bảng 658/658 (T-054 §1).
- E5: tổng thực thể tầng 2 tính lại từ `result.json` khớp PT (TT 273, OB 21) ([`e5-thanh-phan.json`](e5-thanh-phan.json)).
- Vùng E7 dựng lại khớp 248/248 bản ghi ([`vung-ve-bo-quan-he.json`](vung-ve-bo-quan-he.json)`#/kiem_tai_dung_tren_ban_ghi_co_E7`).
- Trạng thái đồng loạt đã lần tới đầu vào:
  - BARO chọn `redis_diskio` 30/30 ca RE3 vì IQR nền = 0 (C21);
  - C-d3 OB 22/22 NO_TARGET do lỗi adapter span gốc (C09);
  - C-d3 TT 46/60 UNSUPPORTED_CYCLIC do đồ thị con có chu trình (T-054 §4).
- Điểm z cực lớn (s tới 376.832) do nhánh c = 1 khi IQR = 0 (C13).

**Câu 5 — Kết luận đã tách theo điều kiện và theo ca chưa?** Rồi: theo loại lỗi và vị trí N (§10, [`ban-do-dieu-kien.json`](ban-do-dieu-kien.json)`#/nhom`), theo cặp từng ca (T/H/T ở mọi bảng), và từng ca sai của M1 (14 ca, §10). Mọi nhóm đều nhỏ (3–24 ca); không nhóm nào được gọi là mẫu hình chắc (QT15).

**Câu 6 — Còn lựa chọn nào chưa có câu trả lời "tại sao"?**

- *Vì sao chọn M1 trên dev khi C-a0 hơn ở TT dev (0,983 so với 0,928).* Cấu hình được chọn theo MRR dev gộp hai bộ. Gộp 52 ca dev: M1 0,904, C-a0 0,847 (C-a0 kém nhiều ở OB dev: 0,662 so với 0,873). Lệnh tính ở LOG phiên 2. T-053 ghi E2 là TRAI_CHIEU_DATASET trên dev (`results/T-053/bao-cao.md:118`). C-d2 dev gộp 0,909 cao hơn M1 0,904, nhưng C-d2 là đối chứng chỉ báo cáo (T-043 §11), không là ứng viên.
- *Lựa chọn còn thiếu "tại sao" ở cấp G4:* không có. Các lựa chọn thiết kế có ở WHY-55 đến WHY-69, WHY-79.
- *Câu "vì sao" của kết quả còn mở:* xem §12.

---

## 5. Ba nhận định chính và giải thích khác

### 5.1 "E2 giúp trên Nezha-OB ở lỗi trễ mạng"

| Bằng chứng | Hỗ trợ / bác bỏ / chưa phân xử |
|---|---|
| Test OB: bỏ E2 làm MRR giảm 0,115, T/H/T 7/25/2 (`PT#/so_cap/Nezha-OB|M1-bo-E2|RR`) | Hỗ trợ |
| Dev OB: bỏ E2 giảm 0,152, 6/16/0, cùng chiều ([`dev-test.json`](dev-test.json)`#/so_sanh_M1_tru_ve/Nezha-OB/bo-E2`) | Hỗ trợ; dev OB tính bằng code trùng bản khóa 22/22 ca (`#/kiem_cau_hinh_OB`) |
| Bỏ 4 ca D1: M1 − bo-E2 = +0,131 trên 30 ca (C02) | Hỗ trợ: không do bản sửa adapter |
| Trễ mạng OB: M1 0,900, C-a0 0,408, M4 0,380 (`PT#/tach_MRR/Nezha-OB|fault/network_delay`) | Hỗ trợ theo nhóm (10 ca) |
| C-a0 sai 15 ca OB, ở 8 ca thực thể đứng đầu là bên gọi trực tiếp của root; M1 sai 7 ca, 0 ca như vậy ([`truy-vet-han-che.json`](truy-vet-han-che.json)`#/dem`) | Hỗ trợ: đúng loại sai mà G2-H03/H06 dự báo đã biến mất |
| Cơ chế (C08): E2-C tính phần thời gian của span bọc ở bên gọi không nằm trong span nhận, rồi gán cho bên được gọi | Cơ chế tính toán có trung gian. Định vị vật lý của độ trễ (mạng hay phía client) chưa phân xử |
| TT: E2 không đổi RR root ở ca nào; dev TT bỏ E2 lại tăng MRR (0,967 so với 0,928) | Không hỗ trợ trên TT; ngược chiều dev |

**Mức kết luận theo tiêu chí khai trước (SPEC, tiêu chí xong 3):** dev và test cùng chiều, vững khi bỏ 4 ca D1 → "**mô tả, nhất quán**" cho OB. Không mở rộng sang TT hay RE3.

### 5.2 "TT và RE3 không cần quan hệ"

| Giải thích | Bằng chứng | Trạng thái |
|---|---|---|
| (a) Dữ liệu đơn giản: tín hiệu của chính root đủ | R1 đúng 48/60 TT, 28/30 RE3; M4 (đếm sự kiện) cao trên RE3; C-a0 = M1 trên cả hai bộ | Hỗ trợ (a) |
| (b) Thành phần quan hệ kém | E5 làm hại 1 ca RE3 (`428c`, C14); E1 vừa giúp vừa hại trên TT (C07) | Hỗ trợ một phần (b) |
| (c) Hit@5 chạm trần, ít ô, nên không phân biệt được | §4 câu 2 | Hỗ trợ (c) |

**Không phân xử được giữa (a) và (b)** bằng dữ liệu đã có: ở hai bộ này, mọi vế M1-family đều đúng ở gần như mọi ca, nên không còn ca nào để tách tác dụng của quan hệ. Dữ liệu phân xử được cần ca mà quy tắc đơn giản thất bại: lỗi lan mạnh, tải thay đổi, nhiều root ở giữa đồ thị. FlashTicket với kịch bản flash sale là ứng viên (P10). Kết luận phụ thuộc: câu RQ3d cho TT/RE3 và hướng thiết kế FlashTicket.

### 5.3 "Khóa xếp max-z làm M1 sai khi đối thủ có một kênh cực trị hẹp"

| Bằng chứng | Trạng thái |
|---|---|
| Test: 8/14 ca M1 sai có nhãn "kênh hẹp của đối thủ" (TT 2, OB 4, RE3 2) ([`ban-do-dieu-kien.json`](ban-do-dieu-kien.json)`#/ca_theo_nhan`) | Quan sát |
| Dev OB (code khóa): 2/5 ca sai do kênh hẹp (`dev-3b92690644`, `dev-63c30faf34`) ([`maxz-dev.json`](maxz-dev.json)`#/OB_dev/theo_huong`) | **Đã hiện trên dev** OB |
| Dev TT: bản ghi dev không có độ rộng kênh | Không đủ dữ liệu |
| Trước G3, T-053 đã ghi "cực trị A và ca hại" là giả thuyết chưa xác nhận (`results/T-053/bao-cao.md:250`) | Đã thấy dấu hiệu trước G3, chưa xác nhận |
| Cùng đặc tính giúp root ở ca đúng: TT 30/57, OB 5/27 (T-054 §7.5); dev OB 3/17 | Đặc tính hai chiều, không là nguyên nhân riêng |
| R1 đúng ở 6/7 ca M1 sai có R1 (TT+RE3) | Hỗ trợ ứng viên "khóa theo độ bền"; chưa kiểm |

Kết luận: trong điều kiện một thực thể khác có kênh với z (tính từ max(A)) lớn hơn z lớn nhất của root, bước E6a đặt max s ngay sau tầng sẽ đặt thực thể đó lên trên. Thông tin độ rộng của lệch không được dùng ở vị trí khóa đó. Điều kiện này đã hiện trên dev OB, nên không phải chỉ thấy ở test. Chưa có bằng chứng một khóa khác hơn tổng thể. Thử khóa mới trên test là thiết kế theo test (C-15 B), nên không làm.

---

## 6. Hạn chế P4 nào M1 khắc phục (H2)

Nguồn: [`truy-vet-han-che.json`](truy-vet-han-che.json). Ánh xạ thành phần lấy từ `results/T-043/bao-cao.md` §7 và `results/T-034/goi-g2.md` §5.

| Dòng G2 | Thành phần M1 | Kết quả trên test (mô tả) | Đánh giá |
|---|---|---|---|
| G2-H03, G2-H06: dịch vụ gọi bị chấm thay root; dấu hiệu trễ mạng nằm ở span phía gọi | E2 (UV-1), E1 (UV-2) | OB: ca sai do bên gọi trực tiếp đứng đầu từ 8 (C-a0) xuống 0 (M1). Trễ mạng OB 0,900 so với 0,408 | Khắc phục trên OB; TT, RE3 không đổi |
| G2-H17: dịch vụ phía trên đứng trước root | E5, E1, E2 | Đối thủ phía trên root ở ca sai: OB 8 → 0; TT 1 → 0; RE3 2 → 1 (C-a0 → M1). E5 riêng đổi RR root 1/60 TT, 0/34 OB, 1/30 RE3 (hại) | Khắc phục chủ yếu nhờ E1/E2; E5 gần như không tác dụng lên RR root |
| G2-H07: lỗi return OB | Không có thành phần riêng (E3 tắt) | Return OB (3 ca): M1 0,75, C-a0 0,778, M4 0,712 | Không khắc phục |
| G2-H09: chia cho IQR của nền phẳng | Không sửa; E4 có cùng suy biến | Gây 1 ca sai RE3 (C13) và giúp 2 ca đúng RE3 | Hạn chế còn nguyên trong M1 |
| G2-H12: giá trị không hợp lệ lan qua cấu trúc | Yêu cầu kỹ thuật UV-7 | Không đo riêng | — |
| G2-H16: rào cản tập ứng viên | Tầng 3 giữ thực thể không cờ | Root trong tập trả về 60/60, 34/34, 30/30 | Khắc phục |

19 dòng còn lại không thuộc M1, có lý do ở `#/khong_thuoc_M1`: lỗi bản cài của baseline, hạn chế dữ liệu, hoặc chế độ (b).

**Giải thích khác cho dòng H03/H06/H17.** C-a0 và M1 khác nhau ở cả E1, E2 lẫn E5, nên phần "8 → 0" chưa tách được từng thành phần (H12, OPEN). Bỏ riêng E5 không đổi RR root OB ở ca nào, nên phần này đến từ E1/E2 là có khả năng nhất. Đây là suy luận từ hai phép bỏ riêng, chưa phải phân rã.

---

## 7. Đồ thị thực dùng so với DT18 và ba ví dụ của cô (H6, H4)

**Nút và cạnh** ([`do-thi-dt18.json`](do-thi-dt18.json)):

| Bộ | Nút có cạnh | Cạnh quan sát | Thực thể xếp hạng | Thực thể không có cạnh mỗi ca |
|---|---:|---:|---:|---|
| RE2-TT | 26 | 55 | 68 | 42–50 (gồm 26 thực thể DB/cache) |
| Nezha-OB | 10 | 13 | 10 | 0 |
| RE3-OB | 7 | 9 | 12 | 5 |

- Cạnh quan sát là cặp (bên gọi, bên được gọi) dựng từ trace, **không có kiểu**. Trace của dataset công khai không cho dựng cạnh dữ liệu hay thông điệp (`results/T-040/ban-giao-p6.md:19-20`).
- T12-on thêm cạnh tĩnh, gồm nút DB và broker (TT 84 nút, 181 cạnh). Tên nút DB tĩnh (ví dụ `database-default:ts-auth-service:ts-auth-mysql`) khác tên thực thể DB đang xếp hạng (ví dụ `ts-auth-mongo`). T12-on không đổi RR root ở 94/94 ca (C06).
- **So với DT18-NV2** ("cạnh biểu diễn quan hệ gọi hàm, trao đổi thông điệp hoặc phụ thuộc dữ liệu"): trên dữ liệu công khai, chỉ cạnh gọi service–service vào phép tính. Cạnh dữ liệu và thông điệp chỉ kiểm được ở FlashTicket.

**Ba ví dụ của cô (bước 2):**

| Ví dụ | Trong M1 | Kết quả |
|---|---|---|
| Phát hiện bất thường có dùng đồ thị (nghĩa hẹp, MRP §2.3) | E5: tách bất thường tự sinh với kế thừa theo cạnh | E5 hạ 273 thực thể xuống tầng 2 ở 59/60 ca TT, 21 ở 14/34 ca OB, 40 ở 21/30 ca RE3. Root bị hạ nhầm: 0/60, 1/34, 0/30. RR root đổi khi bỏ E5: 1 ca TT (giúp), 1 ca RE3 (hại) ([`e5-thanh-phan.json`](e5-thanh-phan.json)) |
| PageRank anomaly | E6b (PageRank cá nhân hóa) tắt trong M1; thử làm vế C-g (SimpleRCA + PageRank trên cạnh của M1) | C-g kém M4 ở TT (0,778) và OB (0,645), hơn M4 ở RE3 (0,992, nhờ 1 ca). Trái dấu giữa bộ |
| Subgraph anomaly detection | E7: đồ thị con bất thường → vùng nghi ngờ | Có vùng (§3 RQ3c). Chưa là "subgraph anomaly detection" theo nghĩa hẹp: không có điểm và quy tắc quyết định cho đồ thị con (T-043 §6) |
| GNN | Không làm | WHY-10: chưa đủ ba tiêu chí (chưa thấy hiện tượng phụ thuộc ngữ cảnh mà chấm theo phần tử bỏ sót; thiếu dữ liệu học không lộ nhãn; CPU laptop). Đây là thiếu căn cứ, không là bằng chứng GNN thất bại |

**Độ đúng của E5 khi hạ thực thể không phải root** không đo được: không có nhãn mức thành phần. P10 có thể gán nhãn này.

**Vùng của vế bỏ quan hệ (Đ-1)** ([`vung-ve-bo-quan-he.json`](vung-ve-bo-quan-he.json)`#/tom_tat`, cách 1, tỷ lệ chứa root / cỡ):

| Bộ | M1 | C-a0 | bo-E5 |
|---|---|---|---|
| RE2-TT | 0,950 / 3,90 | 0,950 / 5,03 | 0,933 / 3,90 |
| Nezha-OB | 0,824 / 1,38 | 0,735 / 2,29 | 0,824 / 1,38 |
| RE3-OB | 0,900 / 1,60 | 0,900 / 1,73 | 0,900 / 1,60 |

C-a0 vốn không có E7; số của C-a0 là "nếu áp E7 lên kênh và cạnh của C-a0". Vùng dựng quanh nhóm đầu của khối đầu, nên tỷ lệ chứa root đi theo độ đúng hạng 1 và không là bằng chứng độc lập. Mô tả: quan hệ làm vùng nhỏ hơn ở cả ba bộ và chứa root nhiều hơn ở OB.

---

## 8. Dev và test có cùng chiều không (H3)

Nguồn: [`dev-test.json`](dev-test.json). Dev OB tính bằng code trùng bản khóa (22/22 ca, RR root khớp). Dev TT: diff code giữa T-052 và lượt test chỉ thêm nhánh tùy chọn cho metric Nezha và C-d3, không chạm đường TT; chưa kiểm bằng chạy lại.

| Phép so (M1 − vế) | Dev TT | Test TT | Dev OB | Test OB |
|---|---|---|---|---|
| C-a0 (bỏ E1/E2/E5) | −0,056 | 0 | +0,211 | +0,164 |
| bo-E1 | +0,070 | +0,093 | 0 | +0,130 |
| bo-E2 | −0,039 | 0 | +0,152 | +0,115 |
| bo-E5 | −0,017 | +0,008 | +0,067 | 0 |
| C-d2 | +0,011 | +0,011 | −0,027 | −0,002 |
| SimpleRCA | +0,037 | +0,099 | +0,335 | +0,186 |

- Cùng chiều: E2 trên OB; E1 trên TT; C-d2 và mọi baseline trên cả hai bộ.
- Ngược chiều: E5 (cả hai bộ), E1 trên OB, E2 và C-a0 trên TT.
- **Hệ quả.** Tác dụng của từng thành phần không ổn định giữa dev và test, trừ E2 trên OB. Một thành phần "giúp trên dev" chưa đủ để chờ nó giúp trên dữ liệu mới, nhất là khi chênh chỉ do 1–5 ca. Bài học cho thiết kế FlashTicket: chỉ giữ thành phần có cơ chế đọc được, không chỉ dựa trên chênh MRR dev.

---

## 9. Phát hiện bất thường (RQ3a) — đã có gì

- M1 có lớp phát hiện **mức thành phần** (E4 cờ kênh, E5 tách tự sinh/kế thừa), nhưng không có ngưỡng mức hệ thống đã hiệu chuẩn. Phép thử giả C-e trên TT: ở cửa sổ trước tiêm, M1 trả CAUSE_FOUND ở 58/58 ca, trung bình 16,4 thực thể tầng 1/ca. RR của root tương lai 0,130, so với mức ngẫu nhiên 0,071 ([`kha-nang-phan-xu.json`](kha-nang-phan-xu.json)`#/H7`).
- Nghĩa: thứ hạng trong cửa sổ lỗi dựa vào độ lớn tương đối, không vào một ngưỡng phát hiện. Phát hiện mức hệ thống giao luật Grafana (M-38). Baseline phát hiện chỉ có ở P3 trên dev (T-034 §2.5–2.6).
- Đây là phần DT18 "phát hiện dấu hiệu bất thường" và bước 4 của cô (P/R/F1) còn thiếu rõ nhất.

---

## 10. Bản đồ điều kiện liên bộ (H9)

Nguồn: [`ban-do-dieu-kien.json`](ban-do-dieu-kien.json). Ca sai M1 (root không đứng riêng khối đầu): TT 3, OB 7, RE3 4. Nhãn cơ chế chép từ báo cáo và đính chính, không gán mới. Một ca có thể có nhiều nhãn; không cộng thành tỷ lệ nguyên nhân.

| Nhãn | Số ca | Ca |
|---|---:|---|
| Đối thủ có kênh hẹp với z cực trị | 8 | TT `053c`, `5e8f`; OB `07fe`, `3218`, `4dbc`, `d46d`; RE3 `cde8`, `d07d` |
| E5 hạ root hoặc bỏ cờ kênh mạnh của root | 2 | OB `88dc`; RE3 `428c` |
| Root là nút nguồn (frontend) | 2 | OB `4dbc`, `88dc` |
| Cả hai kênh hẹp hoặc cả hai rộng | 2 | OB `3eca`; TT `7a22` |
| Nền IQR = 0 | 1 | RE3 `0d4b` |
| Root chỉ có kênh log | 1 | OB `fd2c` |

Ở 14 ca sai: C-a0 đúng ở 3 ca; R1 đúng ở 6/7 ca có R1; đối thủ là bên gọi trực tiếp của root ở 1 ca.

**Điều kiện M1 làm tốt hơn baseline mạnh** (mô tả, nhóm nhỏ):

- Lỗi trễ mạng và mất gói, khi trễ hiện ở span phía gọi: OB network_delay M1 0,900 so với M4 0,380; TT loss M1 1,000 so với TORAI B 0,725 (`PT#/tach_MRR`). Ở TT loss, C-a0 cũng 1,000, nên phần này không đòi quan hệ.
- Root là nút lá ở OB: M1 0,927 so với M4 0,612 (24 ca).

**Điều kiện M1 làm kém hơn:**

- Root là nút nguồn: OB frontend M1 0,708 so với M4 0,958 (6 ca). E2 không gán bằng chứng cho nút không có bên gọi.
- Lỗi exception OB: M1 0,688 so với M4 0,938 (4 ca).
- Lỗi mã nguồn RE3: M1 thấp hơn M4 ở f1, f2, f5; bằng ở f3, f4. Lỗi lan lên bên gọi ở status, log và trace (T-056 §2.1–2.2, C26).
- Root lệch bền, đối thủ có một kênh cực trị: §5.3.

---

## 11. Giới hạn độc lập của kết quả

- Kết quả chính của bản khóa: A4 TT, A4 OB, bảng chính P7(a), RE3 lượt chính. Giữ nguyên, báo nguyên.
- OB: adapter sửa sau khi đọc cấu trúc cohort (D1); cả 34 ca từng được dò triệu chứng (T-054 §2 mục 7). Kết luận OB là mô tả, không là kiểm độc lập hoàn toàn.
- RE3: lệch số worker chưa khai (C17).
- Mọi phân tích ở T-056 và T-057 là sau khi xem. Ứng viên sửa M1 sinh từ đây phải thiết kế trên dev FlashTicket và kiểm độc lập trên lượt FlashTicket mới (C-15 B). RE3 đã dùng một lần, không dùng lại để kiểm.

---

## 12. Câu còn mở (giải thích theo review-prompt mục 19)

| Câu mở | Vì sao chưa xác định | Giải thích còn lại | Phép phân xử, dữ liệu, chi phí | Kết luận phụ thuộc |
|---|---|---|---|---|
| OB có "đơn giản" theo nghĩa R1 không | Chưa tính R1 trên OB: metric thô OB test không có trên EC2 | Đơn giản như TT/RE3; hoặc không (M4 thấp 0,689 gợi ý không) | H11: đọc lại metric thô OB test trên laptop, 2–3 giờ; cần Minh cấp quyền | Câu "dữ liệu công khai đơn giản" cho cô |
| Phân rã chênh M1 − C-a0 trên OB thành E1/E2/E5 | Ma trận thiếu vế (E1 tắt + E2 bật + E5 tắt…) | Cộng tuyến; tương tác E1×E5 | Chạy cấu hình mới trên dev OB (22 ca) hoặc FlashTicket; không chạy trên test (C-15 B) | Câu "thành phần nào giúp" |
| Vai trò riêng của E2 trong tương tác E1×E5 trên TT (C07) | Bật E1 đổi cả giá trị đặc trưng lẫn lớp kênh | E5 xóa bằng chứng qua kênh E2 hoặc qua kênh khác | Như trên, trên dev TT | Thiết kế E5 cho FlashTicket |
| Nguồn của kênh hẹp cực trị ở đối thủ (adservice, auth) | TT: không hỗ trợ "bất thường nền" ở 2/2 ca (C03); OB không có vế C-e | Lan truyền thật qua đường không quan sát; tranh chấp tài nguyên chung; bất thường gián đoạn | OB: cần cửa sổ nền khác trên dữ liệu thô (đọc thô test, cần quyền); FlashTicket: đo được trực tiếp | Có nên đổi khóa xếp/chuẩn hóa z |
| Max-z trên dev TT | Bản ghi dev TT không lưu độ rộng kênh | Có hoặc không có trên dev TT | H14: chạy lại M1 trên 30 ca dev TT đủ trung gian, 0,5–1,5 giờ EC2 | Câu "đã thấy trước G3" cho TT |
| Định vị vật lý của trễ E2-C (C08) | `g` gộp mạng, phía client, hàng đợi | Trễ mạng thật; trễ phía client | Span server và client hai đầu cạnh (FlashTicket, instrumentation đủ) | Diễn giải E2 |
| TORAI B mất thông tin gì ở auth loss TT | Chưa đọc trung gian nội bộ TORAI B | Hợp nhất bốn nguồn, nguồn thiếu điền 0 (C22) | Đọc trung gian đã lưu, khoảng 1–2 giờ (H16, đã bỏ khỏi T-057) | Chỉ câu "vì sao" của baseline |
| Tác động D1 lên E1 trên OB | 4 ca D1 trùng 3/8 ca E1 giúp | Tác dụng E1 thật nhỏ hơn; hoặc D1 không liên quan | Dữ liệu OB độc lập chưa dùng | Câu E1 trên OB |
| Độ đúng của E5 khi hạ thực thể không phải root | Không có nhãn mức thành phần | E5 hạ đúng triệu chứng; hoặc hạ nhầm | Nhãn thành phần trên FlashTicket (P10) | Nghĩa hẹp "graph-based anomaly detection" |

---

## 13. Ứng viên chuyển sang FlashTicket (chưa kiểm)

Mọi mục dưới đây sinh từ phân tích sau khi xem test. Chưa kiểm. Thiết kế trên dev FlashTicket, kiểm độc lập trên lượt FlashTicket mới (C-15 B).

| Ứng viên | Giả định | Sai khi | Kết luận phụ thuộc |
|---|---|---|---|
| Khóa xếp dùng độ bền/độ rộng lệch, không chỉ max(A) | Root lệch bền hơn đối thủ có kênh cực trị | Lỗi chỉ tạo một đỉnh ngắn ở root | Thiết kế E6a |
| Chuẩn hóa không phụ thuộc đơn vị khi IQR = 0 | Kênh nền hằng không mang thông tin | Kênh hằng đổi thật trong lỗi | Thiết kế E4 |
| Kênh lỗi gán theo cạnh caller→callee | Lỗi mã nguồn hiện ở bên gọi | Bên được gọi không có trace (12/30 ca RE3) | Kênh lỗi; yêu cầu P9 |
| Giữ SimpleRCA và R1 làm mốc so sánh chính | Quy tắc đơn giản mạnh trên dữ liệu "đơn giản" | — | Đánh giá P10 |

**Yêu cầu quan sát rút ra** (đề xuất, chưa kiểm): mọi service có span; span phía client ghi peer service; lỗi ghi ở span của service phát sinh (exception event); log lỗi có `errorType`; span server và client ở hai đầu mỗi cạnh để định vị trễ. Nguồn: T-056 "Hệ quả cho G4 và FlashTicket" mục 3; C16.

---

## 14. Điểm chờ Minh quyết (kèm đề xuất, review-prompt mục 20)

| Điểm | Đề xuất của Claude | Vì sao | Mặt trái | Phương án khác |
|---|---|---|---|---|
| Duyệt G4 | Duyệt G4 với kết luận "không hơn rõ baseline; quan hệ giúp có điều kiện (OB, E1/E2)" và các OPEN ở §12 | Đủ sáu câu; kết quả báo trung thực theo MRP §3 | RQ3a và P8 còn thiếu; cô có thể muốn thêm thực nghiệm | Hoãn G4 tới khi có H11 |
| H11 (R1 trên OB) | Cấp | Đóng câu "OB có đơn giản không", câu cô dễ hỏi | Thêm tiếp xúc test (đã mở toàn bộ) | Giữ OPEN |
| H14 (dev TT đủ trung gian) | Không làm trong T-057; tách sang task chuẩn bị thiết kế FlashTicket | Không đổi kết luận G4; chỉ bổ sung câu "thấy trước G3" cho TT | Câu G4-Q6 cho TT còn "không đủ dữ liệu" | Làm ngay trên EC2 (0,5–1,5 giờ) |
| Câu xin cô định hướng | (a) đồ thị tham gia quyết định báo động (M-20); (b) đánh giá P/R/F1 chỉ trên FlashTicket; (c) thêm dataset khó hay dồn lực FlashTicket; (d) GNN có bắt buộc | Bốn điểm đổi hướng việc kế tiếp | Hỏi nhiều câu một lần | Chỉ hỏi (c) |
| Định dạng báo cáo cho cô | `.md` làm nguồn, xuất `.docx` khi gửi | Soát số bằng máy được | Giữ hai bản khớp nhau | Chỉ `.docx` |
