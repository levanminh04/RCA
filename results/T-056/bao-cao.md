# T-056 — Phân tích bổ sung trước G4 (2.1–2.5)

Claude làm, Codex phản biện. Ngày 08/11/2026. Chỉ đọc kết quả, trung gian và parquet đã mở (TT/OB ở T-054, RE3 ở T-055). Không chạy phương pháp, không sửa thiết kế. Mọi số là **mô tả sau khi xem**, không phải kiểm định.

Nguồn: **K** = `results/T-056/ket-qua.json` (sinh bởi `results/T-056/scripts/phan_tich.py`; số đếm trên EC2 ở `results/T-056/runs/ec2-001/`, từ `signals_ec2.py` và `redis_diskio_ec2.py`).

## Tóm tắt

| Câu | Trả lời ngắn |
|---|---|
| 2.1 Mã lỗi span có chỉ ra root ở RE3? | **Không.** Root không có span lỗi tăng ở ca nào (0/30). Lỗi chỉ hiện ở bên gọi (checkout, frontend). Root không có trong trace ở 12/30 ca |
| 2.2 Log lỗi có tách root? | **Một phần.** Root có log lỗi tăng ở 18/30 ca, nhưng chỉ đứng đầu theo số log lỗi tăng ở 4/30. Checkout/frontend ghi nhiều log lỗi hơn |
| 2.3 IQR nền = 0 phổ biến không? | Có. 12% kênh metric bị cờ ở TT và 27% ở RE3 có IQR = 0. Nhưng nó chỉ trực tiếp gây **1** ca sai (RE3), và giúp root ở 2 ca đúng (RE3). Ca sai ở P7(a) đến từ kênh trace hẹp, không phải IQR = 0 |
| 2.4 BARO, TORAI B | BARO chọn `redis_diskio` ở 30/30 ca: IQR = 0 nên điểm bằng đỉnh I/O tính theo đơn vị gốc. TORAI B xếp đầu bên gọi trực tiếp của root ở 15/30 ca |
| 2.5 Vùng và vị trí | Vùng cách 1 chứa root với tỷ lệ kỳ vọng TT 0,95, OB 0,82, RE3 0,90. Ở RE3, M1 đúng hết 12 ca root không có trong trace; sai ở nhóm "lá" (0,875 so với M4 0,986) |

## 2.1 Mã lỗi span ở RE3 (`K#/2_1_status_span_RE3`)

- **Quan sát.**
  - Đếm span có status ≠ 0 theo service, ở N = [t−300, t) và A = [t, t+300).
  - Root có span lỗi tăng: **0/30**. Root có "lỗi riêng" (span lỗi không có span con lỗi) trong A: 0/30.
  - Service có "lỗi riêng" tăng nhiều nhất: checkoutservice 15, frontend 15 (`#/tom_tat/top_d_own_counter`).
  - Xếp theo chênh span lỗi cho MRR 0,156; theo lỗi riêng 0,154; theo tỷ lệ lỗi 0,153 (`#/tom_tat/MRR_rule_*`). Thấp hơn M1 (0,925) và M4 (0,975) rất nhiều.
- **Root vắng khỏi trace:** adservice 9/9 ca và cartservice 3/3 ca (`#/theo_ca/*/root_in_traces`).
- **Suy luận.**
  - Lỗi mã nguồn ở RE3 không hiện thành status lỗi trên span của chính root, có thể vì service không được trace hoặc không đặt status.
  - Lỗi hiện ở span của bên gọi, nơi lỗi được bắt hoặc trả về.
  - Một kênh status gán cho owner của span sẽ **chỉ vào bên gọi**. Muốn dùng được, phải chuyển lỗi xuống bên được gọi theo cạnh gọi, nhưng ở 12/30 ca bên được gọi lại không có trong trace.
- **Hệ quả.** Đề xuất "thêm kênh status span" ở báo cáo RE3 §6 phải sửa thành: kênh status gán theo cạnh (caller→callee), kèm yêu cầu instrumentation đủ mọi service. Đây là ứng viên, chưa kiểm.

## 2.2 Log lỗi ở RE3 (`K#/2_2_log_loi_RE3`)

- **Quan sát.**
  - Root có log (container) ở 30/30 ca. Root có log từ khóa ERROR/FAIL/EXCEPTION tăng ở 18/30.
  - Xếp container theo số log lỗi tăng cho MRR 0,448. Root đứng đầu 4/30. Đứng đầu thường là checkoutservice (15) và frontend (11).
  - Ở 4 ca M1 sai: root currencyservice (2 ca f1) không có log lỗi; root emailservice có 12 và 6 log lỗi trong A, nhưng checkout có nhiều hơn.
- **Suy luận.**
  - Log lỗi có thông tin về root, nhưng bên gọi cũng ghi log lỗi khi nhận lỗi, thường nhiều hơn.
  - Vì vậy cơ chế 2 ở báo cáo RE3 (log bị chặn thang ở 1) **không** phải nguyên nhân duy nhất. Kể cả không bị chặn, xếp theo số log lỗi vẫn ưu tiên bên gọi.
  - Điều M1 cần là phân biệt log lỗi tự sinh với log lỗi do lan ngược. E5 có quy tắc lan ngược cho log lỗi, nhưng chỉ hiệu lực khi có cạnh và bên được gọi có cờ.
- **Câu hỏi mở.** SimpleRCA đạt Hit@1 0,95 dù log lỗi một mình chỉ cho MRR 0,448. Phần tín hiệu nào của M4 tách được root (metric của chính root như mem/latency?) chưa lần.

## 2.3 IQR nền = 0 (`K#/2_3_iqr0`)

- **Kiểm phép tính lại.** z tính lại trên dữ liệu thật khớp s của M1 ở **2634/2634** kênh metric (TT) và **273/273** (RE3) (`#/counts`).
- **Tần suất.**
  - TT: IQR = 0 ở 319/2634 kênh metric bị cờ (12%).
  - RE3: 73/273 (27%).
  - OB: chỉ có dấu hiệu thay thế (s ≥ 100 và độ rộng ≤ 0,05), 0/241 kênh. Reader metric Nezha thô không được chạy lại.
- **Ảnh hưởng đến ca** (kênh mạnh nhất của đối thủ hoặc của root có IQR = 0; `#/by_dataset`):

  | Bộ | Ca sai | Sai do đối thủ có IQR = 0 | Ca đúng mà root thắng nhờ IQR = 0 |
  |---|---:|---:|---:|
  | TT | 3 | 0 | 0 |
  | OB | 7 | 0 (dấu hiệu thay thế) | 0 |
  | RE3 | 4 | 1 (`0d4b`, shippingservice mem) | 2 |

- **Đính chính diễn giải.**
  - Ở P7(a) §7.5, 6/10 ca sai là do **kênh trace** (self-time E1, cạnh E2) có z lớn từ max(A) với độ rộng thấp, không phải do IQR = 0.
  - Báo cáo RE3 §4 gộp hai hiện tượng làm "cơ chế 1". Nên tách: (a) z theo max(A) ở kênh hẹp — chính, lặp ở cả ba bộ; (b) IQR = 0 ở metric — hiếm, 1 ca sai.

## 2.4 BARO và TORAI B ở RE3 (`K#/2_4_baro_torai_RE3`)

- **BARO.**
  - **Quan sát:** đầu bảng là `redis_diskio` ở 30/30 ca. Ở cả 30 ca, `redis_diskio` trong N có trung vị 0 và IQR 0, và điểm BARO bằng đúng max(A) (`results/T-056/runs/ec2-001/*-redis-diskio.json`). Ở 14/30 ca, đỉnh trong N cao hơn đỉnh trong A, tức đột biến I/O có sẵn ở nền. Root thường đứng thứ 2 sau redis.
  - **Suy luận:** trong điều kiện metric thưa (đa số 0, đôi khi có đột biến) ở nền, phép chuẩn hóa robust (trung vị/IQR) của BARO suy biến về đơn vị gốc, nên một kênh I/O không bất thường vẫn đứng đầu. Đây là cùng loại suy biến với nhánh c = 1 của E4 ở M1.
- **TORAI B** (seed 0): đầu bảng là frontend 14, checkout 12, email 3, cart 1. Thực thể đứng đầu là bên gọi trực tiếp của root (theo cạnh quan sát của M1) ở 15/30 ca; là root ở 4/30.
  - **Suy luận, ứng viên:** TORAI dựa trên chuỗi lỗi và độ trễ của trace; lỗi và trễ hiện ở bên gọi (khớp 2.1), nên TORAI chọn bên gọi.

## 2.5 Vùng nghi ngờ và vị trí N (`K#/2_5_vung`, `K#/2_5_vi_tri_N`)

**Vùng của M1, cách 1 / cách 2:**

| Bộ | Tỷ lệ kỳ vọng chứa root | Cỡ kỳ vọng | Cỡ / số thực thể quan sát |
|---|---|---|---|
| TT | 0,95 / 0,967 | 3,9 / 12,0 | 0,057 / 0,177 |
| OB | 0,824 / 0,912 | 1,38 / 3,62 | 0,138 / 0,362 |
| RE3 | 0,90 / 0,967 | 1,6 / 2,37 | 0,13 / 0,19 |

Đây chỉ là vùng nghi ngờ. Không có nhãn vùng, nên không gọi là độ đúng vùng ảnh hưởng.

**Vị trí N (MRR theo nhóm):**
- TT: nhóm bậc 0 (13 ca) M1 1,0, M4 0,836, TORAI B 0,733; nhóm lá (23) M1 1,0, M4 0,812.
- OB: nhóm lá (24) M1 0,927, M4 0,612; nhóm nguồn (6, frontend) M1 0,708, M4 0,958.
- RE3: "không có trong trace" (12) M1 1,0, M4 0,958; nhóm lá (18) M1 0,875, M4 0,986.

**Suy luận:** M1 mạnh khi root ít hoặc không có quan hệ quan sát (bậc 0, vắng khỏi trace), vì xếp tầng theo kênh của chính root không cần cạnh. M1 yếu khi root là nút nguồn (OB frontend) hoặc là lá có bên gọi cùng lệch (RE3). Số ca mỗi nhóm nhỏ; không là mẫu hình chắc.

## Hệ quả cho G4 và FlashTicket

1. **Sửa diễn giải trong G4:** tách cơ chế "z từ max(A) ở kênh hẹp" (chính) khỏi "IQR = 0" (phụ); bỏ khẳng định log bị chặn thang là nguyên nhân chính ở RE3.
2. **Lỗi mã nguồn lan lên bên gọi** ở cả status, log và trace. Đây là chỗ đồ thị **có thể** giúp: chuyển bằng chứng lỗi từ bên gọi xuống bên được gọi theo cạnh. Nhưng cần đủ trace ở mọi service; RE3 thiếu trace cho 12/30 root.
3. **FlashTicket, yêu cầu quan sát:**
   - mọi service phải có span (kể cả service lá);
   - span phía client ghi peer service (bên được gọi);
   - lỗi ghi ở span của service phát sinh (exception event);
   - log lỗi có `errorType` để tách lỗi tự sinh với lỗi nhận từ downstream.
   - Đây là đề xuất, chưa kiểm.
4. **Ứng viên sửa M1 cho P10** (thiết kế trên dev FlashTicket):
   - z không dựa max(A) hoặc có xét độ rộng;
   - xử lý IQR = 0 không phụ thuộc đơn vị;
   - kênh lỗi theo cạnh caller→callee.

## OPEN

- OB 2.3 chỉ có dấu hiệu thay thế.
- Phần tín hiệu M4 dùng để tách root ở RE3 chưa lần.
- TORAI B mới đọc seed 0.
- Quan hệ giữa vắng trace và cách instrumentation của RE3 chưa có nguồn.

---

## Phần 2 (Minh yêu cầu ghi, 08/11/2026) — Vì sao SimpleRCA cao nhất, "dữ liệu đơn giản", độ khó I/II/III

Nguồn: **K2** = `results/T-056/ket-qua-002.json`, sinh bởi `results/T-056/scripts/phan_tich_002.py`. Số đếm trên EC2 do `rules_ec2.py` xuất ở `results/T-056/runs/ec2-002/`. OB không tính được vì dữ liệu thô không có trên EC2.

### Vì sao SimpleRCA cao nhất

SimpleRCA M4 (`src/simplerca/core.py`) cho mỗi service điểm = **số mẫu A vượt mean_N + 3·std_N, cộng qua mọi kênh metric**, + 1 phiếu trace (p95 > 3 × p95 nền) + 1 phiếu log lỗi. Tính lại riêng phần metric (R1):

| Bộ | R1 | M4 thật | Hạng 1 R1 trùng M4 | R2 lệch trung bình | R3 z kiểu M1 | R4 log lỗi | M1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| TT | 0,876 | 0,876 | 60/60 | 0,269 | 0,581 | 0,086 | 0,975 |
| RE3 | 0,975 | 0,975 | 30/30 | 0,881 | 0,503 | 0,434 | 0,925 |

Nguồn: `K2#/tom_tat/<bộ>/MRR`, `/R1_top1_trung_M4_top1`.

**Mức I.** Sức mạnh của M4 nằm ở đếm độ bền/độ rộng của lệch trên metric. Phiếu trace và log không đổi hạng 1 ở ca nào. M1 xếp theo z từ một mẫu cực trị, nên bỏ đúng thông tin này.

### "Dữ liệu đơn giản" như tác giả SimpleRCA nói?

- **TT, RE3 — đúng theo một nghĩa đo được (mức I).** Số mẫu lệch bền của chính root lớn hơn mọi service khác ở 48/60 ca TT và 28/30 ca RE3 (`/root_events_hon_moi_service_khac`). Một thống kê đơn lẻ trên metric của chính root là đủ, không cần đồ thị.
- **Nezha-OB — không (mức II).** M4 chỉ đạt 0,689, M1 đạt 0,875 nhờ E1/E2. Chưa tính R1 trên OB thô.
- **Không có nghĩa phương pháp nào cũng làm tốt.** Baseline trace (TraceRCA, MicroRank) thất bại trên RE3.
- **Lý do vì sao đơn giản (mức III, chưa kiểm):** lỗi tiêm gây triệu chứng cục bộ trong điều kiện tải đều. Muốn kiểm phải đo độ lan theo thời gian từ root sang hàng xóm.

### M1 và R1 bù nhau (`/M1_top1_R1_top1`, `/ca_lech_M1_R1`)

- **TT:** cả hai đúng 45; chỉ R1 đúng 3 (đúng 3 ca M1 sai; root có 1505/1239/1218 mẫu lệch, so với 726/901/952 của service khác); chỉ M1 đúng 12, đều là lỗi `loss`/`delay` (service khác có nhiều mẫu lệch hơn root, M1 thắng nhờ E1/E2).
- **RE3:** cả hai đúng 25; chỉ R1 đúng 3 (3/4 ca M1 sai); chỉ M1 đúng 1; cả hai sai 1 (`428c`, email f5).
- **Pattern (mức II):** lỗi tài nguyên và lỗi mã nguồn cho triệu chứng bền ở chính root, nên đếm là đủ. Lỗi mạng cho triệu chứng ở bên gọi, nên cần quan hệ. Mới thấy theo nhóm; chưa lần trung gian từng ca trong 12 ca TT.

### Độ khó từng ca

- **Theo dữ liệu** (`/do_kho_theo_du_lieu`; I = R1 đặt root hạng 1; II = chỉ M1; III = cả hai không):

  | Bộ | I | II | III |
  |---|---:|---:|---:|
  | TT | 48 | 12 | 0 |
  | RE3 | 28 | 1 | 1 |

- **Theo số phương pháp** (`K2#/do_kho_theo_phuong_phap`; I = ít nhất nửa số phương pháp đặt root hạng 1): TT I 53 / II 7 / III 0; OB I 13 / II 20 / III 1; RE3 I 3 / II 27 / III 0.
  - Ở RE3, mức II nhiều là vì baseline trace yếu, không vì ca khó. Cách phân loại theo dữ liệu phản ánh độ khó đúng hơn.

### Phân loại mức bằng chứng các pattern

| Mức | Nhận định |
|---|---|
| I (đã xác nhận bằng tính lại/đếm) | M4 = R1; TT/RE3 đơn giản theo nghĩa root lệch bền nhất; R1 đúng ở 6/7 ca M1 sai (TT+RE3); lỗi mã nguồn không hiện status ở root, lan lên bên gọi; IQR = 0 làm suy biến M1 và BARO; dữ liệu ít đa dạng (TT 5 root, RE3 4 root, Hit@5 chạm trần) |
| II (có bằng chứng, còn giải thích khác) | M1 hơn R1 ở lỗi mạng nhờ E1/E2; Nezha-OB không đơn giản; TORAI B chọn bên gọi vì lỗi/trễ lan lên (seed 0) |
| III (giả thuyết) | Dữ liệu đơn giản vì triệu chứng cục bộ và tải đều; khóa xếp theo độ bền sửa được M1 mà không làm hỏng ca đúng (chỉ thử được trên dev FlashTicket, C-15 B); FlashTicket giống TT/RE3 hay giống OB (flash sale tải đột biến) |

### Bài học thiết kế (ứng viên cho P10, chưa kiểm)

1. Khóa xếp hạng dùng độ bền/độ rộng lệch thay cho max(A).
2. Dùng quan hệ ở lỗi mạng và lỗi lan; với lỗi mã nguồn, gán lỗi từ bên gọi xuống bên được gọi theo cạnh, và cần trace đủ.
3. Chuẩn hóa không phụ thuộc đơn vị khi IQR = 0.
4. Giữ SimpleRCA và thêm R1 làm đối chứng "quy tắc đơn giản" chính thức trên FlashTicket.
