# T-073 — Đính chính 1 cho kết quả E5 (đáp CX-21, CX-21b)

Ngày 23/11/2026. Phiên `rca-w5`, Claude, người làm.

File này **không thay** `results/T-073/e5-ket-qua.md` (sha256 `c51fdbe2…`) hay `results/T-073/e5/SHA256SUMS` (`54583b2d…`). Hai file đó đã được T-070 dẫn hash nên giữ nguyên. Khi đọc E5, đọc bản gốc kèm file này; chỗ nào khác nhau thì theo file này.

Phạm vi: chỉ dữ liệu đã có trên laptop. Không SSH, không chạy lại. Phần cần file trên exp-obs ghi ở mục 7, chờ chép theo Q1.

## 1. Mốc giờ

| Mốc | Bản gốc ghi | Đính chính |
|---|---|---|
| Gây lỗi | "02:17:30Z theo nhật ký điều khiển" | Theo sổ, do điều phối chấm (LOG T-070 mục 02:40Z): `mark` 02:17:31.841Z, `fault-start` (trường `t` của inj3) **02:17:34.233Z**. t̂ − fault-start = **55,767 s**, thuộc [0, 600). Tiêu chí (a) **đạt theo sổ**. Mốc 02:17:30.311Z của `e5/luot/nhat-ky.jsonl` là lúc laptop bắt đầu gửi lệnh, không phải lúc gây lỗi. |
| Gỡ lỗi | "02:27:40–02:27:44Z; verify sau gỡ: sạch" | 02:27:40–44Z (đồng hồ laptop) và `fault-stop` 02:27:42.397Z (sổ) chỉ là **giờ của lệnh gỡ**, không phải giờ Payment chạy lại. `inj3.py start` có hẹn một tiến trình tự gỡ ở mốc gọi + 600 + 5 s trên exp-app, tức khoảng 02:27:39Z. Lệnh gỡ tay hủy tiến trình đó nếu còn, và vẫn báo thành công khi container đã chạy lại (`inj3.py` hàm `stop`: bỏ qua lỗi "is not paused"). Vì vậy giờ unpause thật nằm khoảng 02:27:39–02:27:44Z và **không muộn hơn** lúc `verify` sạch (02:27:46.497Z theo sổ). Muốn biết chính xác cần sự kiện Docker `unpause` hoặc `PAUSE-PAYMENT.het-han.log` trên exp-app. Hiện chưa có file nào trong hai thứ đó. |
| Ghi chỉ mục G1 | 02:32:47.165Z; t̂ → G1 = 857,2 s | Giữ nguyên. Đây là mốc phụ (lúc bước `g1` kết thúc). |
| Dashboard hiện ca | Đích đo ghi "14,8 phút (API)" | Theo `khai-truoc-e5.json` `N.diem_ket_thuc`, đích đo là **lúc thấy ca trên Grafana**: **898,8 s (15,0 phút)**, tức 02:33:28.8Z. Lần truy vấn API panel danh sách lúc 02:33:16.8Z (886,8 s) là mốc phụ. Mốc này chỉ có trong LOG: phản hồi API đó **không được lưu** trong 52 file của `e5/`, nên không tái kiểm độc lập được. Hai mốc đều là cận trên, vì tôi mở dashboard sau khi bộ điều phối báo xong. Hai ảnh `s49-anh-*.jpg` có giờ ghi file trên laptop khoảng 02:34:12Z, là bằng chứng phụ cho thấy ca hiện trước hạn 02:43:30Z. Kết luận: **đạt N** (898,8 s < 1500 s). |

Phạm vi của "hiện ca": E5 chứng minh ca được xuất tự động và xem được trong hạn khi mở hoặc làm mới trang. Dashboard đặt `refresh: ""`, nên E5 **không** chứng minh một trang đang mở sẵn tự cập nhật mà không cần thao tác.

## 2. Phủ cửa sổ của Payment: hai nhóm, không phải một

Bản gốc ghi "6 metric, lỗ lớn nhất 365 s, ngưỡng 40 s". Câu đó gộp sai hai nhóm. Số đúng, lấy từ `e5/su-co/bbc0a6d44f.json` `#/du_lieu_loi/phu/nguon/metric:<kênh>:payment-service`:

| Nhóm | Nguồn | Bước | Mẫu trong [t̂−300, t̂+300) | Lỗ lớn nhất | Ngưỡng |
|---|---|---:|---:|---:|---:|
| Container | `cpu`, `mem` | 10 s | 16 mỗi nguồn | 364,999 s | 40 s |
| HTTP (dẫn xuất `rate[1m]` / phân vị histogram) | `error`, `latency-50`, `latency-90`, `workload` | 15 s | 20 mỗi nguồn | 315 s | 60 s |

Cửa sổ lõi là 02:13:30–02:23:30Z. Theo `check_core_input.py` (bản E5, hàm `lo_lon_nhat`), lỗ được tính cả hai biên: mẫu đầu − (t̂−300), khoảng giữa hai mẫu liền nhau, và (t̂+300) − mẫu cuối.

**Suy luận từ số đếm, chưa kiểm trên giờ mẫu thô:**
- Nhóm HTTP: 20 mẫu cách đều 15 s phủ 285 s. Có 285 + 315 = 600, nên số đếm khớp đúng một trường hợp: mẫu chạy liên tục từ 02:13:30Z đến khoảng 02:18:15Z, rồi mất tới hết cửa sổ. Mẫu cuối sau `fault-start` khoảng 41 s. Điều này phù hợp với việc `rate[1m]` còn tính được trong khoảng một phút sau mẫu thô cuối.
- Nhóm container: các dịch vụ khác có 40 mẫu và lỗ lớn nhất 20,001 s, tức khoảng cách thực xen kẽ 10 s và 20 s, trung bình 15 s. Với 16 mẫu ở nhịp đó, mẫu cuối rơi khoảng 02:17:25Z, trước `fault-start`, và không có mẫu nào trở lại trong cửa sổ.

**Nguyên nhân: giữ mở.** Các giải thích khả thi:
- (i) Payment bị pause nên ngừng phát mẫu HTTP thô, và bộ thu Docker ngừng hoặc không trả số đo cho container đang pause.
- (ii) Bộ thu hoặc Prometheus mất mẫu vì lý do khác trùng thời điểm.
- (iii) Truy vấn dẫn xuất trả rỗng dù mẫu thô vẫn còn.

Có hai lý do hiện chưa phân xử được. Thứ nhất, laptop chỉ có số đếm và lỗ, không có giờ từng mẫu. Thứ hai, cửa sổ lõi kết thúc 02:23:30Z, trước khi gỡ, nên không thấy mẫu có trở lại sau unpause hay không.

Phép phân xử: dùng `prometheus.json` của ca `7577dd5b` và gói rộng đến t̂+600 (02:28:30Z). Đối chiếu giờ mẫu cuối, mẫu trở lại của từng chuỗi Payment với mốc `fault-start`/gỡ, và với một dịch vụ còn chạy cùng lúc. Chi phí: chép file đã lưu và xử lý một ca, không cần tải hay tiêm lại.

Hai giới hạn còn lại sau phép đó: gói chỉ lưu kết quả truy vấn dẫn xuất, không có bộ đếm HTTP thô, nên (iii) với nhóm HTTP có thể vẫn không tách được. Nếu sau gỡ vẫn thiếu mẫu, giữ nguyên giới hạn.

Kết luận theo khai trước vẫn là **"đã hiển thị nhưng thiếu phủ"**. Không lặp lượt.

Bằng chứng toàn hệ thống khi Payment im: trace gộp có 122.780 mẫu, lỗ lớn nhất 0,395 s. Riêng `payment-service` chỉ có span và log ở N: 17.502 span và 584 dòng log (`#/buoc/4/tom_tat/span_theo_thuc_the/payment-service`, `log_theo_thuc_the/payment-service`). Booking vẫn có 10.222 span ở A.

## 3. Phạm vi phép kiểm phủ: 61 nguồn cơ sở, chưa gồm hai kênh H5

Bản gốc và `khai-truoc-e5.json` gọi đầu vào được kiểm là "đầu vào V082 thực dùng". Đọc code thì thấy câu này rộng hơn những gì đã kiểm.

- **Đường đi của dữ liệu.** `check_core_input.py` đọc `outputs/7577dd5b/method-input.json` của P7 (`#/du_lieu_loi/nguon_dau_vao_loi/kieu` = "p7-method-input (V082 đọc lại)"). Sau khi đọc file đó, V082 còn đi thêm một chặng trong `src/m1_ft/chay.py` `_duong_ong_metric`. Chặng này lấy `prometheus.json` của ca, cộng hai kênh `live-down` và `live-ms` từ gói bổ sung (thành phần `H5-liveness`, `kenh_moi`). Tiếp theo, `KenhLiveness.bien_doi_bundle` ánh xạ cổng đầu dò sang dịch vụ (`CONG`) và bỏ URL không ánh xạ được. Cuối cùng, `dung_lai_metric` dựng lại hàng metric và giờ mẫu.
- **Phần đã kiểm.** `#/du_lieu_loi/phu/nguon` có 63 mục: trace, log và **61 nguồn metric cơ sở**. Không có nguồn `live-down` hay `live-ms` nào.
- **Phần chưa kiểm.** Hai kênh H5 sau ánh xạ, gồm URL nào được gán, URL nào bị bỏ (`chuoi_url_bo`) và mẫu nào tới bước chấm. Cũng chưa kiểm hàng metric cơ sở sau khi dựng lại có trùng hàng của P7 hay không. Cùng hàm, cùng `prometheus.json` và cùng inventory thì dự kiến trùng, nhưng đây là suy luận, chưa đếm.
- **Câu đúng phạm vi:** "Phủ theo mẫu thực đã kiểm trên trace và 61 nguồn metric cơ sở của đầu vào P7 mà V082 đọc lại. Hai kênh `live-down`, `live-ms` mà V082 thêm sau đó chưa được kiểm phủ."

Lỗi gốc nằm ở câu chữ của khai trước (`tieu_chi.ket_qua_phu_cua_so.mo_ta`), do tôi soạn ở lượt 7: nó định nghĩa "đầu vào V082 thực dùng" là method-input của P7. Đây là thu hẹp phạm vi so với đầu vào thật của V082. Không sửa file khóa; ghi giới hạn ở đây.

## 4. Biên phải của H5 và ảnh hưởng lên ca E5

- **Code: xác nhận.**
  - `xuat_bo_sung.py` (bản E5, dòng 106–120) truy vấn khúc cuối tới `e = min(E, …)` với `E = t̂ + 300`, nên gói có thể chứa mẫu đúng tại t̂+300.
  - `KenhLiveness._chet_im` (`src/m1_ft/thanh_phan/h4_h5.py`) lấy A là các mẫu có `ts >= t`, không có cận trên.
  - Vậy câu "mọi phép tính V082 dùng cửa sổ nửa mở [t̂, t̂+300)" là sai với H5. `kiem_t = true` chỉ xác nhận các mốc `window` ghi trong đầu ra.
- **Ảnh hưởng lên hạng 1 của ca `7577dd5b`: chưa kiểm.** File chú thích `H5-liveness` và chuỗi `live-down` của ca nằm trên exp-obs. Có hai quan sát làm giảm khả năng mẫu biên đổi kết quả ở ca này. Cả hai đều là suy luận, chưa kiểm:
  - (a) `payment-service` **không có** trong `entity_ranking` của P7: 16 thực thể, có `payment_db` nhưng không có `payment-service` (`#/buoc/1/tom_tat/entity_ranking`). H5 chỉ đưa lên nhóm đầu thực thể có trong `rec['entity_ranking']`; thực thể ngoài hạng chỉ vào `khong_trong_thu_hang`. Nếu thứ hạng V082 cũng không có `payment-service`, H5 không thể đưa Payment lên, dù có hay không có mẫu biên.
  - (b) H5 đòi mọi mẫu `live-down` ở N bằng 0 (điều kiện i). Ở chế độ (b), t̂ là `startsAt` của `t072-live` (`for` 20 s). Vì vậy đầu dò Payment có thể đã báo lỗi ít nhất một bước trước t̂, tức mẫu bằng 1 nằm trong N, và H5 bỏ qua chuỗi đó.
- Phép phân xử: đọc `extra.m1_ft.chu_thich.H5-liveness` (gồm `chet_im`, `khong_trong_thu_hang`) trong đầu ra V082 của ca. Đọc chuỗi `live-down` sau ánh xạ, kiểm điều kiện (i) trước, rồi so kết quả H5 khi giữ và khi bỏ mẫu tại t̂+300. Chờ chép file theo Q1.
- Không quy hạng 1 `booking-service` cho lỗi biên hay cho (a)/(b) trước khi có các file đó. E5 không đánh giá độ chính xác (W6–W7).

## 5. Sáu trang lưu trữ: giới hạn của hai trang L4

`e5/s47b-3-sau-trang.txt` dòng 11–13: trang `t065-l4-rca` và `t065-l4-phat-lai` mở ca `00eaea92` nhưng `from/to` trong URL mặc định thuộc ca khác. Vì vậy:
- "nạp được, có ca, 0 'No data', 0 lỗi" đúng cho cả 6 trang;
- với 2 trang L4, **chưa xác nhận** các panel phụ thuộc thời gian hiển thị đúng cửa sổ của ca đã chọn.

Phép đếm "No data" dựa trên chữ hiển thị, không đọc từng phản hồi truy vấn. Không cần bật lại provider chỉ để chứng minh trang nạp được.

## 6. Các câu khác cần đọc lại

- **Hash dữ liệu lưu trữ.** "Hash trước và sau trùng `c94da63c…`" chỉ đúng cho hai mốc **01:58:56Z** (trước khi bật P) và **02:05Z** (sau khi trả về E5), trước lúc G1 ghi ca mới (02:32:47Z). Hồ sơ không xác nhận các thư mục lưu trữ còn nguyên sau 02:05Z.
- **Chú thích "Hash do chỉ mục T-064 cấp" trên trang ca `t073-b`: sai với ca này.** Chuỗi do `campaigns/runner/sau_v082.py` hàm `dung_mot_ca` gán cố định cho mọi bản khác `p7`. `g1_b.py` dùng lại hàm này nguyên văn. Trên trang, chú thích nằm cùng bảng với "Hash đầu ra", nhưng hash đầu ra của ca `7577dd5b` (`23b873ae…`) do `g1_b.py` tính từ đầu ra V082 của lượt T-073, không do chỉ mục T-064 cấp. Hash cấu hình và hash mã nguồn lấy từ chỉ mục bản V082 và được `g1_b.py` đối chiếu với `extra.m1_ft` của đầu ra. Chỉ phần đó có nguồn gốc từ chỉ mục. Không sửa G1 trong E5 vì file G1 thuộc bản ghim T-067. Việc sửa thuộc W8/W9a.
- **Tên hợp đồng G1.** SPEC ghi "G1 bản 0.3". Ca E5 thực sự mang `phien_ban_dinh_dang` 0.5 cộng khối `che_do_b` `phien_ban_khoi: "b-1"` (`e5/s49-che-do-b.txt`), như `results/T-073/g1-0.3.md` đã trình hai phương án. Câu "đúng bản 0.3" không đúng nguyên văn. Tên do Minh chốt.
- **Đối chiếu E3 của t̂.** Ba cảnh báo thật của E5 đều mang `da_doi_chieu_E3 = false`. E3 chỉ đối chiếu `startsAt` với giờ chuyển trạng thái cho bốn luật p95 thử, không cho `t072-live`.
- **Chấm sổ đã có.** Điều phối đã chấm sổ lúc 02:40Z. Không ai cần đọc sổ lần nữa.

## 7. Chờ chép file ca `7577dd5b` (theo Q1)

Mục 2, 3 và 4 cần các file sau, hiện nằm trên exp-obs. Chưa chép, chờ Minh duyệt Q1:

| File | Dùng cho |
|---|---|
| `/srv/rca-lab/m1/cases/7577dd5b/prometheus.json` (sha256 `c15bea42…` theo `#/buoc/0/tom_tat/files`) | mục 2: giờ mẫu từng chuỗi Payment; mục 3: đếm lại nguồn cơ sở |
| `inventory.json` của ca (`8311ef52…`) | mục 3: ánh xạ thực thể |
| gói bổ sung của ca (sha256 `4b16f899…`, `T066-bo-sung-4-r9`) | mục 3, 4: chuỗi `live-down`/`live-ms` trước ánh xạ, mẫu tại t̂+300 |
| đầu ra V082 `method-output-1.json` của ca (`23b873ae…`) và `summary.json` | mục 4: `chu_thich.H5-liveness`, thứ hạng V082 |
| gói rộng đến t̂+600 (nếu stage đã lưu) | mục 2: mẫu Payment sau gỡ |

Các phép tính trên chạy trong RAM cho một ca, không cần tải hay tiêm lại.

Kết luận nào phụ thuộc vào các file này:
- phạm vi phủ đầy đủ của đầu vào V082 (mục 3);
- việc H5 có liên quan tới hạng 1 của ca hay không (mục 4);
- nguyên nhân thiếu phủ của Payment (mục 2).

Kết quả chức năng E5 **không** phụ thuộc vào các file này.
