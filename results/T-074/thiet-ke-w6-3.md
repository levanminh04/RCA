# T-074 — Thiết kế W6, bản 3 (bổ sung bản 2)

- **Soạn:** Claude, phiên `danh-gia-w6`, 22/11/2026. Không dùng máy, không truy vấn Prometheus.
- **Cách đọc:** bản 3 = `thiet-ke-w6-2.md` + các mục thay dưới đây. Chỗ hai bản khác nhau thì theo bản này. Bản 1, bản 2 giữ nguyên (ghim ở `SHA256SUMS`, `SHA256SUMS-2`).
- **Nguồn sửa:** Codex CX-08 (`results/T-070/codex/CX-08-tin-cuoi.md`) điểm 1–3 (§A–§D, phiên 3) và điểm 4–7 (§E–§H, bổ sung cùng ngày theo giao việc thứ hai của điều phối T-070). Bản 3 trước bổ sung có sha256 ghi ở LOG phiên 3.
- **Dự toán bản 3:** `du-toan-3.json` (sinh bằng `du_toan_3.py`) thay các mục sức chứa, phương án, khối của `du-toan.json`.
- **Trạng thái:** đề xuất; câu hỏi mới ở `cau-hoi-minh-3.md` (Q-W6-09…12).

---

## A. Thay §9.1 — giá trị G (CX-08 điểm 1)

**Sự thật đã kiểm** (`results/T-072/bieu-thuc.json`): `#/grafana/eval_interval_s` = 10; `#/tham_so_co_dinh/cua_so_rate_s` = 300; `for_s` = 60 ở các luật p95 route. Theo công thức của chính bản 2 (G ≥ `for` + `eval_interval` + khoảng nhìn lùi), **G ≥ 370 s**. Bản 2 vừa đề xuất G = 120 s vừa ghi công thức này: mâu thuẫn. Ví dụ: cảnh báo đầu tiên ở t+800 là bỏ sót nếu G = 120, là TP nếu G = 370.

Hai phương án trả lời **hai câu hỏi khác nhau**:

| | G1 = 370 s (theo luật đã khóa) | G2 = 120 s (mục tiêu vận hành) |
|---|---|---|
| Câu hỏi | Luật như đã cấu hình có phát hiện được sự cố tiêm không | Luật có báo trong 120 s sau khi gỡ lỗi không |
| Cửa sổ dương | `[t, t+970)` | `[t, t+720)` |
| Mặt trái | dung sai dài → dễ ghép một cảnh báo không liên quan; sự cố ghép cuối cửa sổ cần dữ liệu RCA vượt biên chu kỳ (dưới) | phạt luật vì độ trễ do chính cấu hình (`for` + cửa sổ rate) tạo ra; Recall thấp không phân biệt "luật không thấy" với "luật thấy muộn" |

**Hệ quả vượt biên chu kỳ (chỉ ở G1).** t = S+600; sự cố có t̂ gần t+970 = S+1570 cần A = `[t̂, t̂+300)` tới S+1870, quá S+1800 (hết chu kỳ). Cách xử lý đề xuất:
- Bộ chụp gói (b) chụp theo t̂ đúng như mọi sự cố, **không cắt** ở biên chu kỳ (telemetry vẫn chạy giữa hai chu kỳ). Runner W7 chờ tới t̂ + 300 + thời gian xả (đo ở pilot) trước khi bắt đầu đoạn K của chu kỳ sau có lỗi; nếu không chờ được thì gói vẫn chụp, phần A sau S+1800 nằm trong khoảng nghỉ/khởi động của chu kỳ sau.
- Mỗi gói (b) mang cờ `A_vuot_bien_chu_ky` (có/không) và số giây vượt.
- **TP phát hiện tách khỏi trạng thái RCA.** TP chỉ do t̂ quyết định. Kết quả RCA của sự cố đó có trạng thái riêng (`du_phu` / `thieu_phu` / `vuot_bien_chu_ky`), báo trong bảng xếp hạng như một cột; ca vẫn trong mẫu số xếp hạng (b), không bỏ.
- Chi phí thời gian nếu chọn chờ: tối đa ~70 s + thời gian xả mỗi chu kỳ có sự cố muộn (chưa đo).

**Đề xuất của người làm:** G1 = 370 s là quy ước **chính** (đánh giá đúng luật đã khóa ở W4, không đổi luật); G2 = 120 s báo **phụ**, khai trước, gọi đúng là "phát hiện trong 120 s sau khi gỡ lỗi (mục tiêu vận hành)". Cả hai tính trên cùng tập sự cố; không chọn quy ước sau khi xem số. Phương án khác: chỉ G2 (đơn giản, không vượt biên, nhưng đo sai câu hỏi về luật). → Q-W6-09.

Bảng đoạn của bản 2 giữ nguyên, chỉ thay G. Đoạn H của ca lỗi (không chấm) bắt đầu từ t+600+G.

---

## B. Thay §8.4–§8.5 và phần mẫu số của §9.1 — giữ ca, thay lượt, giờ khỏe (CX-08 điểm 2)

### B.1 Thiếu tín hiệu

| Tình huống | Bằng chứng | Xử lý |
|---|---|---|
| Hỏng đường thu | có bằng chứng **độc lập với can thiệp**: Prometheus khởi động lại hoặc `up` của Collector/exporter xuống; Collector báo lỗi xuất/rớt; thiếu mẫu ở thực thể đối chứng khai trước | ca không hợp lệ; thay 1 lần bằng lịch con |
| Thiếu do can thiệp | có bằng chứng nối thiếu tín hiệu với can thiệp: đầu dò cho thấy thực thể bị tiêm ngừng/treo (ví dụ `Paused=true`), và chỉ thực thể đó hoặc phụ thuộc của nó thiếu | giữ ca, cờ `thieu_do_can_thiep` |
| **Chưa phân loại** | thiếu tín hiệu (kể cả gói thiếu cả một nguồn cho mọi thực thể) mà **chưa** có bằng chứng thuộc hai dòng trên | **giữ ca**, cờ `thieu_chua_phan_loai`; không thay, không gán nguyên nhân |

Bản 2 coi "gói thiếu cả một nguồn cho mọi thực thể" là hỏng đường thu. Bản 3 bỏ: một nguồn rỗng chưa tách được lỗi xuất khỏi việc đường xử lý ngừng tạo sự kiện.

### B.2 Can thiệp (một quy tắc cho cả §8.4 và §8.5)

| Sổ ghi | Nghĩa | Xử lý |
|---|---|---|
| `fault-start-failed` | lệnh tiêm không chạy được; chưa có can thiệp | không vào mẫu số lỗi; **bù 1 lần** bằng lịch con (lỗi bộ tiêm, như hạ tầng) |
| `fault-start` có, đầu dò không xác nhận | can thiệp đã chạy nhưng không đạt điều kiện xác nhận | **giữ**, nhóm "can thiệp chưa xác nhận", báo riêng; **không bù** |
| `fault-start` có, đầu dò xác nhận | ca lỗi hợp lệ | mẫu số chính |

Bản 2 §8.5 ghi "tiêm không khởi động → bù" và §8.4 ghi "chưa xác nhận → không thay": hai câu nói về hai trường hợp khác nhau nhưng không tách rõ. Bảng trên tách.

### B.3 Giờ khỏe và báo động giả theo mức tải

- FP và thời gian khỏe tính trên **cùng tập phút đủ điều kiện**, riêng từng mức tải.
- **×1:** phút đủ điều kiện = phút trong đoạn âm được xếp `khoe_x1` bằng bộ phân loại của T-071 (`results/T-071/khai-truoc-e2.json#/phan_loai_phut`, áp nguyên quy tắc, không chỉnh). Bản 2 dùng "tổng thời lượng đoạn âm" và ngầm coi mọi phút của ca đối chứng là khỏe: sai, vì "không tiêm" ≠ "khỏe" (I2).
- **×3:** bộ phân loại T-071 chỉ có nhãn `khoe_x1`; ×3 và flash chỉ mô tả. Hai phương án:
  - (a) **Đề xuất:** giữ nguyên bộ phân loại; ở ×3 báo **"sự cố trên giờ quan sát ×3"** (mẫu số = mọi phút đoạn âm ×3 trừ phút có bằng chứng hỏng đường thu độc lập), không gọi là báo động giả mỗi giờ khỏe; câu "báo động giả mỗi giờ khỏe ×3" để OPEN. Dùng được ngay, không chọn ngưỡng mới.
  - (b) Định nghĩa `khoe_x3` riêng trước W7: cùng các tiêu chí K1–K5, B1–B2 của T-071 với mức kỳ vọng nhân theo hệ số tải, khai trước và ghi WHY. Mặt trái: tiêu chí mới chưa kiểm trên dữ liệu ×3 nào; chọn mức kỳ vọng ×3 là thêm một lựa chọn cần căn cứ.
  → Q-W6-10.

---

## C. Thay §7.1 bước 7–8 và bổ sung — BARO/SimpleRCA trên gói FlashTicket (CX-08 điểm 3)

### C.1 Ánh xạ ngược tên thực thể khi chấm

- **Sự thật:** `src/m1/adapter_flashticket.py::normalize_metrics` dựng tiền tố cột bằng `entity.replace('_', '-')` và giữ bảng `aliases[prefix] = entity` (dòng 126–134). `src/p3/ban_ghi.py::thuc_the_metric` lấy phần trước `_` đầu tiên → cột `booking-db_db-size` cho `booking-db`. Đầu ra P7 và nhãn T-059 dùng tên chuẩn `booking_db` (CX-08 kiểm 5 tên `_db` ở `#/entity_ranking` ca `03573b63`).
- **Quy ước (ĐX):** adapter W7 trả bảng alias cùng bảng metric. Ở **biên trả kết quả** của mỗi baseline (trước khi ghi đầu ra), đổi mọi tên thực thể qua bảng alias về tên chuẩn inventory. Tên không có trong bảng alias và không có trong inventory → lỗi adapter (dừng slot, không chấm). Bộ chấm chỉ so tên chuẩn. Bước 8 của §7.1 bản 2 ghi danh sách thực thể **sau** ánh xạ ngược.

### C.2 Đầu vào nhiều chuỗi runtime

- **Sự thật:** `normalize_metrics` ném lỗi "Multiple runtime series map to one logical metric…" khi nhiều định danh runtime cùng về một metric logic (dòng 154). Ca dev thật: RECREATE-PAY, P7 `ERROR`, V082 `OK` hạng 1 (`results/T-069/bang-theo-o-chinh.json#/hang/16/moi`).
- **Đề xuất:** baseline gặp lỗi này ghi trạng thái riêng `LOI_ADAPTER_DA_CHUOI`, **giữ trong mẫu số chính như trượt**, báo riêng số ca. Không tự gộp chuỗi cho baseline.
- **Phương án khác:** cho mọi baseline dùng bước nối chuỗi H8a như **tiền xử lý chung bổ sung**, khai rõ; khi đó BARO/SimpleRCA không còn đúng đường dữ liệu của P3, và V082 mất phần lợi H8a trong phép so. → Q-W6-11.

### C.3 Dựng bảng theo thời gian

- `normalize_metrics` trả hàng thưa theo nguồn, mốc nano giây, không điền xuôi. SimpleRCA đòi epoch giây (`src/simplerca/adapter.py::prepare`, lỗi "metric epoch must be seconds"; hàm này đã nhận tham số `aliases`); BARO điền xuôi theo thứ tự hàng.
- **Quy ước (ĐX):** dựng bảng rộng trên lưới đều bước `step_seconds` của bundle (15 s, `collect_metrics`), mốc = epoch **giây nguyên** (ns // 10⁹ làm tròn xuống về lưới). Nhiều điểm cùng ô lưới của một cột: lấy điểm có mốc native muộn nhất; ghi số ô trùng. Ô trống để NaN; việc điền (ffill rồi 0) chỉ do bước 1 của §7.1 (quy ước P3) làm. Ghi cho mỗi ca: số ô trống trước điền theo cột.

### C.4 Đính chính §7.1 bước 4

Câu "chia 1e6 không đổi điểm (RobustScaler bất biến theo tỉ lệ)" **sai trong trường hợp IQR = 0**: cột không hằng vẫn có thể có IQR = 0 (ví dụ N = `[0,0,0,0,1]` qua được `drop_constant`), khi đó RobustScaler dùng thang thay thế 1 và chia `_mem` cho 10⁶ đổi điểm và thứ tự giữa kênh. Giữ phép chia của tác giả; bỏ khẳng định bất biến. Đếm số cột IQR = 0 ở N mỗi ca (đưa vào bước 8).

---

## D. WHY đề xuất chịu ảnh hưởng (thay phần tương ứng của `de-xuat-why-2.md`)

- **W6-I (bản 3):** G1 = 370 s chính theo cấu hình luật khóa (`bieu-thuc.json`), G2 = 120 s báo phụ; TP do t̂, trạng thái RCA tách; FP và giờ khỏe trên cùng phút đủ điều kiện từng mức tải; ×3 báo "sự cố trên giờ quan sát". Trạng thái: CHỜ-MINH (Q-W6-09, Q-W6-10).
- **W6-G (bản 3):** ba lớp thiếu tín hiệu (hỏng đường thu có bằng chứng độc lập / do can thiệp có bằng chứng / chưa phân loại → giữ ca); `fault-start-failed` bù 1 lần, can thiệp chưa xác nhận giữ không bù. Trạng thái: ĐX.
- **W6-E (bản 3):** G-live = `live-down` + `live-ms`; che cờ, đặc trưng, `chet_im`, ghi đè H5b; gói bổ sung giữ schema và mốc, hai kênh `result` rỗng; kiểm che đủ bằng trung gian, không bằng khác biệt với P7. Trạng thái: ĐX.
- **W6-A (bản 3):** K0 + K3 (dùng lại 3 đối chứng ×1 ở vị trí cố định, hoặc thêm 3 mốc — Q-W6-12); K2 khôi phục 3 lần (mỗi khối) về dump E6 sau sửa; ô mốc chỉ mô tả; "truy vấn nền chậm dần trong khi DB tích lũy", chưa tách DB/cache/CPU/thời điểm. Trạng thái: CHỜ-MINH (Q-W6-01, Q-W6-12).
- **W6-K (bản 3):** ánh xạ ngược alias ở biên trả kết quả; `LOI_ADAPTER_DA_CHUOI` trong mẫu số như trượt; lưới 15 s, epoch giây; bỏ khẳng định bất biến tỉ lệ. Trạng thái: ĐX, Q-W6-11.

## E. Thay §3.3 dòng G-live và §9.4 dòng "Thông tin nào mang thay đổi" (CX-08 điểm 4)

**Sự thật đã kiểm:** `H5-liveness` khai **hai** kênh mới, `live-down` (tài nguyên) và `live-ms` (độ trễ) (`src/m1_ft/thanh_phan/h4_h5.py::kenh_moi`), và gán cả hai về service theo cổng (`bien_doi_bundle`). CX-08 thấy 3/17 đầu ra V082 của T-069 có cờ `live-ms` (ví dụ `metric|booking-service_live-ms` ở `c446b6ae`). Bản 1–2 chỉ che `live-down` → bỏ sót một dẫn xuất đã quan sát. Khi cấu hình có H5, `chay_ca.py` (dòng 108–109) **bắt buộc** đọc file `--bo-sung`; "chạy không có gói bổ sung" như bản 2 viết sẽ dừng trước khi xếp hạng.

**G-live (bản 3, ĐX):**
- Nhóm thông tin = hai kênh `live-down` + `live-ms`.
- Che cả: cờ của hai kênh trong `#/extra/kenh_co`; đặc trưng và điểm tính từ chúng; chẩn đoán `chet_im` và khóa ghi đè của H5b.
- **Cách che:** giữ một gói bổ sung **đúng schema và đúng mốc** (`t` của gói = t của ca), giữ nguyên mọi bundle khác; với hai kênh của nhóm, giữ mục bundle nhưng bỏ dữ liệu (`result` rỗng). Không xóa file, không điền 0.
- Nhánh dự phòng: H5 không có chuỗi → không gắn cờ, không ghi đè khóa; kênh ghi thiếu trong độ phủ (không phải giá trị 0).
- **Phép kiểm trên dev trước khi khóa** (chỉ tính toán): trên cùng ca, so trung gian V082 và V082-che-G-live: hai kênh vắng khỏi `#/extra/kenh_co`; `chet_im` rỗng; khóa của thực thể không còn ghi đè H5b; mọi kênh khác giữ nguyên. Gói rỗng kênh có làm `chay_ca.py` hay H5 báo lỗi không: **CHƯA-KIỂM**.

**§9.4, bỏ quy tắc** "bản che còn khác P7 ⇒ còn dẫn xuất chưa che". Lý do: H8s1 (phép tính, không che) và nhóm chưa che (G-inst khi chỉ che G-live) làm bản che khác P7 hợp lệ; ngược lại, đầu ra giữ nguyên hạng cũng không chứng minh thành phần không kích hoạt. Thay bằng: kiểm che đủ bằng trung gian (danh sách trên), báo so V082 với V082-che theo từng ca, không suy "còn dẫn xuất" từ khác biệt với P7.

---

## F. Thay §5.2, §5.3 phần chi phí, §5.5 và §11 — sức chứa, khối (CX-08 điểm 5)

Số ở `du-toan-3.json` (sinh bằng `du_toan_3.py`; thay các mục tương ứng của `du-toan.json`, mục khác giữ).

**Sức chứa (dự toán tại mốc E1; số thật đọc lại ở E6):** 73.834 vé còn ở E1 − 26.136 (E2 + E4 tám lượt + E5) − 648 (D1: thêm một lượt ×1 1.800 s ở E4) − 648 (lượt dương E3 ×1) = **46.402** vé cho W7, theo mô hình 648 đơn/lượt ×1. Đơn ×3 dùng 1.944/chu kỳ (đo ở ca khỏe `0bec9eca`; ca lỗi ×3 `785bfd0c` có 1.765) — cận trên, chưa có căn cứ mọi ô ×3 đạt số này.

**Định nghĩa khối (một định nghĩa cho §5.2, §5.3 và JSON):** một khối = một lần của mỗi cặp (ô, mức tải) + 3 đối chứng (+1 ô mốc nếu thêm K3). Ba lần lặp ⇒ **3 khối**. K2 khôi phục trước mỗi khối ⇒ **3 lần** (thay "khối 6–9 chu kỳ, 6–10 lần khôi phục" của bản 1–2). Trộn trong khối chỉ cân bằng vị trí **theo kỳ vọng**; một seed cụ thể không bảo đảm các ô cùng vị trí trung bình → báo vị trí thực của từng ô.

| Phương án | K3 | Chu kỳ | Giờ thu | Chu kỳ/khối | Đơn bảo thủ | Ước hoàn tất | Đủ 46.402? |
|---|---|---|---|---|---|---|---|
| A | dùng lại 3 đối chứng ×1 | 27 | 14,1 | 9 | 35.640 | 23.274 | đủ |
| A | thêm 3 mốc | 30 | 15,7 | 10 | 37.584 | 24.543 | đủ |
| A + CPU-EVENT | dùng lại | 33 | 17,3 | 11 | 43.416 | 28.352 | đủ |
| A + CPU-EVENT | thêm | 36 | 18,8 | 12 | 45.360 | 29.621 | đủ |
| A + B | dùng lại | 51 | 26,7 | 17 | 66.744 | 43.585 | chỉ theo ước hoàn tất |
| A + B | thêm | 54 | 28,3 | 18 | 68.688 | 44.855 | chỉ theo ước hoàn tất |
| A + B + CPU-EVENT | dùng lại | 57 | 29,8 | 19 | 74.520 | 48.663 | không |
| A + B + CPU-EVENT | thêm | 60 | 31,4 | 20 | 76.464 | 49.933 | không |

**K0 dùng ba đối chứng ×1 có sẵn làm ô mốc (phương án mới, ĐX):** đặt trước vị trí của 3 ô BINH-THUONG ×1 — mỗi khối một ô, cùng vị trí trong khối (ví dụ chu kỳ đầu) — thay vì trộn. Ưu: tiết kiệm 3 chu kỳ (~1,6 giờ, 1.944 đơn). Mặt trái: ba đối chứng này không còn trộn ngẫu nhiên, nên vị trí của chúng gắn với thời gian; K (kết luận ca khỏe ×1) đo ở vị trí cố định, không đại diện mọi thời điểm đợt. Phương án khác: thêm 3 chu kỳ mốc riêng (đối chứng vẫn trộn). → Q-W6-12.

**Mốc của K2:** nếu chọn K2, dump dùng để khôi phục phải chụp ở E6 **sau** khi sửa hạn bán và sức chứa. Khôi phục dump E1 (`results/T-071/e1/moc-db.json#/kho_ticket_type`: sức chứa 100.000, hạn bán cũ) sẽ đưa hệ về giá trị trước sửa. Khôi phục hỏng không phát hiện mất cả khối (9–20 chu kỳ tùy phương án) → kiểm nhất quán sau mỗi lần khôi phục trước chu kỳ đầu khối.

---

## G. Thay §5.4 mục 5, §10 mục 4 và WHY W6-A — hạ hai kết luận cơ chế xuống mô tả (CX-08 điểm 6)

- **§10 mục 4 bỏ** câu "so BARO với V082 … là phép phân xử miễn phí". Hai bên khác đồng thời tín hiệu (cột metric so với kênh thao tác gộp từ span), tiền xử lý, đơn vị chấm và cách xếp hạng; cùng đúng hay cùng sai không tách được "do lấy max một mẫu" khỏi "do gộp thao tác". Giữ so BARO–V082 làm **mô tả**.
- **§5.4 mục 5 bỏ** (hai chu kỳ CPU-BOOK-1, HTTP5-EVENT ngay sau khôi phục ở E6 để "tách DB lớn khỏi code đường mua"). Lý do: khôi phục về mốc E1 (40.069 đơn, `moc-db.json#/so_dong_bang_chinh`) **không** cho trạng thái "DB nhỏ hơn" so với ca T-069 (cuối lượt chính 37.477, `results/T-069/phan-tich/kiem-db.txt`); và chỉ đo được một trạng thái mới. Nếu quyết định thực sự phụ thuộc nguyên nhân: cần hai trạng thái DB có độ chênh đã ghi, cùng image, tải, cấu hình, cùng ô ở cả hai trạng thái; chi phí lớn hơn hai chu kỳ, chưa ước lượng. Q-W6-06 việc 3 rút lại.
- Ba ô mốc (K3) chỉ **mô tả** trôi trong đợt.
- **WHY W6-A** thay câu "DB tích lũy làm truy vấn nền chậm dần" bằng: "truy vấn nền chậm dần **trong khi** DB tích lũy (`troi-trong-luot.txt`); dữ liệu hiện có chưa tách được ảnh hưởng DB, cache, CPU và thời điểm".

---

## H. Thay §6 và §9.3 phần "CHƯA-KIỂM k6" — R-07 (CX-08 điểm 7)

- **Đã có** dữ liệu theo request: `tai_linux.py` (`407b4f5`) xuất `raw.json` và `raw.csv`; CX-08 đọc một `Point` của `http_req_duration` trong gói T-069 khớp hash, có thời gian, giá trị, `route`, `routeId`, `status`, `step` (ví dụ `results/T-069/thu/t069-chinh/tai-out/t3-124242f0/raw.json`). Câu "CHƯA-KIỂM k6 hiện ghi gì" của bản 1–2 bỏ.
- Giữ **"độ trễ theo mốc tiêm"** là số chính (không đổi).
- Nếu Minh chọn câu onset/vùng endpoint (Q-W6-05): thiết kế quy tắc onset, số request đủ cho từng route và cách đưa dự đoán vùng về cấp endpoint **trên dữ liệu k6 đã lưu của T-069** (phân tích offline, 0 giờ tải). Còn thiếu: ba thứ vừa nêu.

---

## I. Chưa xử lý trong bản 3

Phạm vi RQ3d (CX-06 dòng 44, CX-08 bảng: `DC-bo-quan-he` chỉ đo tác dụng các bước dùng quan hệ trong **xếp hạng**; C-d1 dùng cạnh gọi, C-d2 chỉ thứ tự khởi phát, C-d3 có thể `NO_TARGET`/`UNSUPPORTED_CYCLIC`) — chưa được giao sửa §3.4/W6-M.
