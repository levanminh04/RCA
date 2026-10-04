# Dựng chuỗi `logts` và `tracets` từ log và trace thô

T-016, S9. Mục đích: TORAI chỉ đọc chuỗi đã đếm theo 15 s (`logts.csv`, `tracets_err.csv`, `tracets_lat.csv`); RCAEval không kèm code dựng các chuỗi này (T-001 mục 8.3). Muốn chạy TORAI trên dataset ngoài RCAEval thì phải tự dựng. File này ghi đặc tả dò ngược được và mức khớp với bản Figshare của tác giả.

Script: `scripts/dung_logts.py`. Kết quả so: `runs/s9/so-sanh-lan1.json` (Drain mặc định, 3 chế độ), `runs/s9/so-sanh-lan2.json` (ngưỡng 0,3–0,7). Chuỗi đã dựng: `runs/s9/tracets_err.csv`, `runs/s9/tracets_lat.csv`, `runs/s9/logts_B_sim0.4.csv`.

## 1. Cùng một ca hay không (chứng minh trước khi so)

`data/rcaeval/re2ob_productcatalogservice_loss_1` (RCAEval RE2-OB, Hugging Face) và `D:\RCA-ext\data\torai-OB\productcatalogservice_loss\1` (Figshare TORAI) là cùng một ca (`runs/s0-cung-ca.json`, `scripts/kiem_cung_ca.py`):
- `inject_time.txt` hai bên bằng nhau (1705342830);
- `metrics.parquet` và `simple_metrics.csv`: cùng 73 cột, cùng 1 441 mốc thời gian, 103 752 ô, 0 ô lệch quá ngưỡng làm tròn (24 163 ô lệch chính xác do CSV ghi 16 chữ số có nghĩa; sai số tương đối lớn nhất 6,3e-14).
- Thêm: tổng số dòng log mỗi service trong `logs.parquet` trùng hệt tổng các cột `logts` của service đó (mục 4).

## 2. Đầu vào thô (RCAEval RE2)

| File | Cột dùng | Đơn vị |
|---|---|---|
| `logs.parquet` | `timestamp`, `container_name`, `message` | giây Unix (số nguyên) |
| `traces.parquet` | `serviceName`, `operationName`, `startTime`, `duration`, `statusCode` | `startTime` micro giây; `duration` micro giây (suy ra: span gRPC 0,1–5 ms); `statusCode` mã gRPC (0 = OK, 14 = UNAVAILABLE, …) |

## 3. Đặc tả `tracets` (dựng lại được)

1. **Lưới thời gian.** Bin 15 s, bắt đầu ở `t0` = thời điểm đầu của dữ liệu ca (ở đây 1705342110, cũng là dòng đầu của `logts.csv` và `tracets_*.csv` bản Figshare). Bin `k` = `[t0 + 15k, t0 + 15k + 15)`; thời điểm span = `startTime // 10⁶`.
2. **Tên cột.** Nếu `operationName` có dạng `[/][gói.]Service/Method` thì cột = `service viết thường + "_" + Method` (ví dụ `hipstershop.CartService/GetCart` → `cartservice_GetCart`, `grpc.health.v1.Health/Check` → `health_Check`, `opentelemetry.proto.collector.trace.v1.TraceService/Export` → `traceservice_Export`). Ngược lại cột = `serviceName + "_" + operationName` (span gốc `frontend` của `frontendservice` → `frontendservice_frontend`). Tức service của cột là **service được gọi** suy từ tên operation, không phải service phát ra span. 17/17 tên cột trùng bản Figshare.
3. **`tracets_err[bin, cột]` = tổng `statusCode`** của mọi span thuộc cột trong bin. Đây là tổng mã lỗi, không phải số span lỗi: 50 span mã 14 cho giá trị 700.
4. **`tracets_lat[bin, cột]` = số span có `duration > μ + 3σ`**, với `μ`, `σ` (pandas, ddof = 1) là trung bình và độ lệch chuẩn `duration` của cột đó **trên toàn file**, gồm cả đoạn sau mốc tiêm.

Mức khớp với bản Figshare (`runs/s9/so-sanh-lan1.json`):

| Chuỗi | Ô trùng | Ô lệch | Ghi chú |
|---|---|---|---|
| `tracets_err` | 1 598 / 1 598 (100 %) | 0 | coi 7 ô NaN ở dòng cuối của bản Figshare là 0 (torai làm `ffill` rồi điền 0, `torai.py:99-100`) |
| `tracets_lat` | 99,75 % | 4 ô (3 ô `health_Check`, 1 ô `adservice_GetAds`), ngoài 7 ô NaN như trên | |

Khác biệt nhỏ không ảnh hưởng tới phương pháp: bản Figshare có 94 dòng (bỏ 2 bin cuối), bản dựng 96 dòng; `main.py` cắt cửa sổ quanh mốc tiêm nên 2 bin cuối không được dùng.

**Lưu ý về rò dữ liệu tương lai.** Ngưỡng `μ + 3σ` tính trên cả đoạn lỗi. Đoạn bình thường của `tracets_lat` vì vậy đã chịu ảnh hưởng của đoạn lỗi. Ở chế độ biết trước thời điểm, đây không phải rò nhãn, nhưng ở chế độ tự phát hiện (MRP P3 b) thì không làm được như vậy: ngưỡng phải học từ quá khứ. Đề xuất (chưa kiểm): khi dựng cho dataset khác, tính `μ`, `σ` chỉ trên đoạn trước mốc (hoặc trước cửa sổ chẩn đoán). Giả định: ngưỡng học từ quá khứ cho chuỗi đếm span chậm tương đương; sai nếu phân phối độ trễ lúc bình thường thay đổi trong ca. Chưa kiểm vì không có bản tác giả để so và đổi cách dựng là thay đổi phương pháp.

## 4. Đặc tả `logts` (không dựng lại chính xác được)

Theo bài (§3.1): tách mẫu log bằng Drain, rồi đếm số lần mỗi mẫu xuất hiện theo khoảng thời gian. Tên cột bản Figshare: `<service>_<số>`, số chạy liên tục 1…73, mỗi số thuộc đúng một service.

Đã thử (`runs/s9/so-sanh-lan1.json`, `so-sanh-lan2.json`), mọi lần cùng lưới 15 s bắt đầu ở `t0`:

| Chế độ Drain (drain3 0.9.11) | Ngưỡng | Số cột dựng / mẫu | Cột khớp hoàn toàn | **Ô trùng / toàn bảng** (SPEC S9) | Độ phủ bảng mẫu | Cặp cột cùng tổng | Tương quan TB |
|---|---|---|---|---|---|---|---|
| A: một Drain cho mọi service, cột `<service>_<id cụm>` | 0,4 | 95 / 73 | 25 | 46,9 % | 66,8 % | — | — |
| B: Drain riêng mỗi service, id toàn cục theo thứ tự xuất hiện | 0,3 | 77 / 73 | 25 | 50,2 % | 59,2 % | 46 | 0,825 |
| B | **0,4 (mặc định)** | 95 / 73 | 25 | **46,9 %** | 66,8 % | 46 | 0,833 |
| B | 0,5 | 293 / 73 | 25 | 16,2 % | 67,1 % | 56 | 0,807 |
| B | 0,6 | 1 098 / 73 | 31 | 4,5 % | 68,4 % | 57 | 0,901 |
| B | 0,7 | 1 398 / 73 | 36 | 3,7 % | 71,3 % | 61 | 0,965 |
| C: một Drain trên chuỗi "`<service> <message>`" | 0,3–0,7 | 51–1 127 / 73 | 17–31 | 4,4–47,0 % | 44,1–68,4 % | 31–57 | 0,78–0,90 |

- "Ô trùng / toàn bảng" là tiêu chí SPEC S9: mẫu số = 96 dòng × Σ theo service max(số cột mẫu, số cột dựng), tức cột thừa của bản dựng cũng tính là sai (`scripts/tinh_lai_s9.py` → `runs/s9/ty-le-toan-bang.txt`, tính lại từ kết quả đã lưu, không chạy lại Drain). Bản trước của file này chỉ báo "độ phủ bảng mẫu" (mẫu số = ô của bảng mẫu) và gọi nhầm là tỉ lệ khớp; đã sửa theo REVIEW R1.
- Vì phép gán chọn cách ghép có lợi nhất, cả hai tỉ lệ đều là cận trên của mức khớp thật.

Không cấu hình nào đạt tiêu chí 95 % ô trùng toàn bảng (SPEC S9); cao nhất 50,2 %. Hai nguyên nhân, tách được nhờ chỉ số phụ:
1. **Mốc thời gian khác.** Tổng số dòng log mỗi service trong `logs.parquet` trùng hệt tổng các cột `logts` của service đó (10/10 service; riêng `redis`, 20 dòng, không có trong `logts`). Nhưng phân bố theo bin khác: với mẫu đơn giản nhất ("Getting supported currencies...", "conversion request successful" của `currencyservice`), chỉ 15,6 % bin trùng; dịch biên bin từ −7 đến +7 s không cải thiện (lớn nhất 15,6 % ở độ dịch 0; `scripts/thu_dich_bien.py` → `runs/s9/thu-dich-bien.txt`, cũng ghi tổng 37 635 dòng hai bên bằng nhau). Tức bản Figshare đếm theo một mốc thời gian khác cột `timestamp` (giây) của parquet, ví dụ thời điểm ghi trong chính dòng log hoặc thời điểm thu thập. Parquet không có mốc đó, nên không dựng lại được từng bin.
2. **Cấu hình Drain chưa biết.** Bài không ghi phiên bản, ngưỡng, quy tắc che biến của Drain. Mặc định của drain3 cho 95 mẫu so với 73; ngưỡng cao hơn tách quá nhiều mẫu (tới 1 398).

Nguyên nhân khả thi khác, chưa loại được: tác giả có thể lọc trước một số dòng (ví dụ `redis`), hoặc gom mẫu theo quy tắc riêng trước Drain.

**Ảnh hưởng tới TORAI trên ca này** (`runs/s9/so-thu-hang-ban-dung-vs-figshare.txt`): chạy TORAI gốc và sửa, seed 0–4, trên bản tự dựng (logts chế độ B ngưỡng 0,4 + tracets tự dựng) và bản Figshare. 4 hạng đầu giống nhau ở cả 10 lượt (`recommendationservice, productcatalogservice, frontend, currencyservice`); khác từ hạng 5 (`cartservice` và `adservice` đổi chỗ). Một ca không đủ để khái quát.

## 5. Đặc tả đề xuất khi dựng cho dataset khác (lựa chọn cấu hình Drain của nhóm: chờ WHY, chưa có nháp; quyết khi có dataset ngoài RCAEval cần dựng)

Đề xuất, **chưa kiểm** trên dataset ngoài RCAEval:

| Bước | Quy ước | Lý do |
|---|---|---|
| Lưới | bin 15 s, gốc ở thời điểm đầu của ca; bin chứa mốc tiêm tính là bình thường như code (`time < inject_time`) | khớp `main.py` cắt `L·2` dòng mỗi phía |
| Log | Drain (drain3 0.9.11, chế độ B, ngưỡng 0,4 mặc định), mỗi service một Drain, đếm theo mốc thời gian của dòng log; cột `<service>_<id>` | gần nhất với tên cột của tác giả; ghi rõ là cấu hình của nhóm |
| Trace | như mục 3; ngưỡng độ trễ chỉ học trên dữ liệu trước cửa sổ chẩn đoán (đổi so với tác giả, xem lưu ý mục 3) | tránh dùng dữ liệu tương lai |
| Tên service | phải thống nhất giữa metric, log, trace (TORAI gộp theo tiền tố trước `_`); service không có dấu `_` trong tên; không service nào là tiền tố của service khác | `torai.py:185, 200, 295-310` |
| Service thiếu nguồn | để trống, TORAI điền 0 | bài §3.2 |

Giả định chung: đếm theo 15 s đủ mịn cho sự cố kéo dài vài phút. Sai khi sự cố ngắn hơn vài bin hoặc khi log thưa (nhiều bin bằng 0, nhiều cột bị bỏ vì hằng).
