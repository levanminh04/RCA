# T-073 — Đính chính 2 cho E5: phân xử trên file ca `7577dd5b` (Q1)

Ngày 23/11/2026, phiên `rca-w5` (Claude, người làm), lượt 19. File này bổ sung `dinh-chinh-e5-1.md` (sha256 `421f6b13…`), không sửa nó.

Chỗ nào hai file khác nhau thì theo file này. Cụ thể, file này thay §2 (phần nguyên nhân), §3, §4 và §7 của đính chính 1.

**Dữ liệu dùng.** 58 file của ca `7577dd5b`, chép từ exp-obs về `results/T-073/e5/ca-7577dd5b/` theo Q1. sha256 trên máy và trên laptop khớp 58/58; manifest ở `results/T-073/e5/ca-7577dd5b.SHA256SUMS`.

**Phép tính.** Chỉ đọc, chạy trong RAM cho một ca, bằng hai script:
- `results/T-073/dap-cx21/phan_tich_ca.py`, ra `phan-tich-ca.json`;
- `results/T-073/dap-cx21/so_hang_metric.py`, ra `so-hang-metric.json`.

Hai script này dùng `src/m1/adapter_flashticket.py`, và chép nguyên thân `dung_lai_metric` cùng phép ánh xạ cổng của H5. Lý do chép nguyên: laptop không có numpy, nên không import được `src/m1_ft/chay.py`.

Không đọc sổ tiêm. Các mốc fault-start và gỡ lấy từ bản chấm của điều phối.

## 1. Phạm vi đầu vào V082 (CX-21 điểm 1): đã kiểm đủ

Nguồn: `so-hang-metric.json`.

**Phần cơ sở.** Dựng lại hàng metric chỉ từ `prometheus.json` của ca cho **4.711 hàng, trùng đúng hàng của đầu vào P7**, và giờ mẫu từng nguồn cũng trùng. `method-input.json` có sha256 `d1341fee…`. Vậy phần cơ sở mà V082 dùng chính là 61 nguồn đã kiểm phủ.

**Đường V082.** Đường V082 gồm `prometheus.json` cộng `live-down`/`live-ms` của gói bổ sung, rồi đi qua phép ánh xạ cổng của H5. Đường này cho 5.367 hàng:
- mọi hàng của P7 đều có mặt;
- thêm 656 hàng (= 16 nguồn × 41 mẫu);
- 77 nguồn metric;
- 0 URL bị bỏ, 0 chuỗi không ánh xạ được, 0 truy vấn rỗng.

16 nguồn thêm là `live-down` và `live-ms` của 8 dịch vụ. Cổng 8761 `discovery-server` được gộp tên thành `config-discovery`.

**Phủ của 16 nguồn thêm.** Theo cùng hàm lỗ của `check_core_input.py`: mỗi nguồn có 40 mẫu trong [t̂−300, t̂+300), lỗ lớn nhất 15 s, dưới ngưỡng 60 s. **Đủ cả 16** (`phan-tich-ca.json` `#/phu_live`).

**Câu đúng phạm vi:** "Đầu vào metric thực của V082 gồm 77 nguồn: 61 nguồn cơ sở trùng P7 và 16 nguồn `live-*`. Trong đó 71 nguồn đủ phủ; 6 nguồn của `payment-service` thiếu." Kết luận phủ không đổi: **đã hiển thị nhưng thiếu phủ**.

## 2. Biên phải của H5 (CX-21 điểm 2): không ảnh hưởng ca E5

Nguồn: `phan-tich-ca.json` `#/h5`, `#/v082`.

- **Mẫu biên có mặt.** Cả 8 chuỗi `live-down` đều có mẫu đúng tại t̂+300 (02:23:30Z): mỗi chuỗi có 41 mẫu, từ 02:13:30Z đến 02:23:30Z.
- **Kết quả H5 như nhau khi giữ hay bỏ mẫu biên.** Chạy `_chet_im` (ngưỡng 60 s) theo cả hai cách đều cho **rỗng**. Điều này khớp chú thích V082 đã lưu: `chet_im.thanh_phan = {}`, `khong_trong_thu_hang = []`, `chuoi_url_bo = 0`.
- **Lý do từng chuỗi không đạt, như nhau ở cả hai cách:**
  - 7 dịch vụ: A không có mẫu báo lỗi, tức đầu dò luôn phản hồi.
  - `payment-service`: **N có mẫu bằng 1 lúc 02:17:45, 02:18:00, 02:18:15Z.** Điều kiện (i) của H5 đòi mọi mẫu ở N bằng 0, nên chuỗi bị loại trước khi xét đến A. Chuỗi Payment là 0 tới 02:17:30Z, rồi 1 liên tục từ 02:17:45Z đến 02:23:30Z.
- **Kết luận.** Ở ca này, mẫu tại t̂+300 không đổi kết quả H5. Vì vậy hạng 1 `booking-service` **không do** lỗi biên.

  Mâu thuẫn trong code mà CX-21 nêu vẫn đúng. Bộ xuất cấp mẫu tại t̂+300, và H5 không có cận trên. Với một ca khác, khi điều kiện (i) đạt, mẫu này có thể đổi kết quả. Phần đó còn mở, nhưng không áp dụng cho ca E5.

## 3. N4 và N5 trong đính chính 1: đính chính và xác nhận

- **N4 cần đính chính một phần.** `payment-service` vắng trong thứ hạng **P7** (16 thực thể), nhưng **có** trong thứ hạng **V082**, ở nhóm hòa cuối (`tie_group` 6). V082 có 17 thực thể. Lý do Payment có mặt: V082 thêm hàng `live-*` của Payment.

  Vì Payment có trong thứ hạng V082, lập luận (a) của đính chính 1 ("H5 không thể đưa Payment lên vì Payment ngoài thứ hạng") **không đúng với V082**. Lý do thực tế khiến H5 không đưa Payment lên là (b), xem dưới.
- **N5 được xác nhận trên ca này.** Ở chế độ (b), t̂ = 02:18:30Z là `startsAt` của `t072-live`. Đầu dò Payment đã báo lỗi từ 02:17:45Z, tức 3 mẫu nằm trong N. Vì vậy điều kiện (i) của H5 không đạt, và H5 không bao giờ xét Payment.

  Theo bản chấm của điều phối, fault-start là 02:17:34.233Z. Mẫu đầu dò bằng 1 đầu tiên rơi khoảng 11 s sau đó.

  **Hệ quả cho W6, quan sát trên một ca:** khi t̂ lấy từ chính cảnh báo liveness của thành phần chết, H5 không thể kích hoạt cho thành phần đó. Như vậy, ở chế độ (b), V082 mất đúng cơ chế mà H5 được thêm vào để xử lý. Đây là quan sát trên một ca, không phải đánh giá độ chính xác.

  Lần dời mốc lớn nhất đã thử với V082 trên dev là +30 s (T-064). E5 dời khoảng 55,8 s. Đề xuất đưa vào câu hỏi mở của W6. Không sửa H5 hay M1 ghim trong T-073.

## 4. Nguyên nhân thiếu phủ của Payment (CX-21 điểm 4): được hỗ trợ là do chính lỗi pause

Nguồn: `phan-tich-ca.json` `#/prometheus_json`. Gói `prometheus.json` phủ 02:08:30–02:28:30Z, tức t̂±600, bao cả lúc gỡ.

| Chuỗi | Mẫu cuối trước khi mất | Mẫu đầu khi có lại | Khoảng mất | Đối chứng Booking, cùng bộ thu |
|---|---|---|---|---|
| `cpu`, `mem` của Payment. Giờ mẫu thật lấy từ `native_timestamps`, là mốc ghi của chính số đo, khác với mốc lưới truy vấn | 02:17:25Z | 02:27:55Z | 629,999 s | 81 mẫu thật, khoảng lớn nhất 20 s |
| `workload`, `error`, `latency-50`, `latency-90` của Payment (lưới truy vấn 15 s, dẫn xuất từ `rate[1m]` hoặc phân vị) | 02:18:15Z | 02:27:45Z | 570 s | 81 mẫu, khoảng lớn nhất 15 s |

Theo bản chấm của điều phối, fault-start là 02:17:34.233Z. Payment chạy lại trong khoảng 02:27:39–44Z, không muộn hơn lúc verify (02:27:46.497Z).

**Phân xử các giải thích:**
- **(i) Do chính lỗi pause: được hỗ trợ.**
  - Mẫu thật cuối của cpu/mem rơi 9 s trước fault-start, tức một chu kỳ thu 10 s. Mẫu có lại 02:27:55Z, ngay sau khi gỡ.
  - Booking dùng cùng bộ thu và cùng truy vấn, nhưng không mất mẫu.
  - Hai nhóm chuỗi dừng và có lại đúng quanh hai mốc pause và gỡ.
- **(ii) Bộ thu hoặc Prometheus mất mẫu vì lý do khác: bị bác** cho khoảng này, vì dịch vụ đối chứng trên cùng bộ thu vẫn liên tục.
- **(iii) Truy vấn dẫn xuất rỗng trong khi mẫu thô vẫn còn: không còn hợp lý** với nhóm HTTP.
  - Chuỗi dẫn xuất dừng 41 s sau fault-start. Cửa sổ `rate[1m]` còn chứa mẫu trước pause cho đến khoảng lúc đó.
  - Chuỗi có lại ngay sau khi gỡ.
  - Không có bộ đếm HTTP thô, nên không kiểm được trực tiếp. Riêng việc chuỗi `rate[1m]` đã có giá trị tại 02:27:45Z, chỉ vài giây sau khi gỡ, **chưa giải thích được** từ dữ liệu đã lưu. Muốn giải thích cần bộ đếm thô quanh 02:27:40Z.

**Kết luận:** thiếu phủ 6 nguồn Payment trong cửa sổ lõi là **hệ quả của chính lỗi pause**: container bị pause thì không phát số đo. Không phải lỗi hạ tầng.

Kết luận "đã hiển thị nhưng thiếu phủ" giữ nguyên theo khai trước. Nhãn "thiếu có thể do chính lỗi, chưa phân xử" của bản gốc nay đổi thành "thiếu do chính lỗi, được hỗ trợ bởi giờ mẫu thật và đối chứng Booking".

## 5. Những gì còn mở sau Q1

- **H5 ở chế độ (b) (N5).** Đây là câu hỏi thiết kế cho W6: đối chứng t = mốc tiêm và t = t̂ trên các ô có lỗi làm chết thành phần. E5 chỉ có một ca.
- **Biên phải H5.** Ở ca khác, khi điều kiện (i) đạt, mẫu t̂+300 có thể đổi đoạn chết im. Đây là mâu thuẫn code, chưa có ca chịu ảnh hưởng. Đề xuất ghi vào danh sách W6/W9a; không sửa M1 ghim.
- **Giá trị `rate[1m]` tại 02:27:45Z.** Cần bộ đếm thô; không ảnh hưởng kết luận phủ.
- Kết quả chức năng E5 **không đổi**.
