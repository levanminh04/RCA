# T-026 — Kiểm đầu vào

Ngày 07/10/2026. Codex, người làm. **Đã kiểm parse Time và đếm N/A thực (0.2/0.3). Dừng tại bảng phương pháp dự kiến, chờ Minh quyết phạm vi trước adapter theo Q-84. Chưa chạy phương pháp.** Rà SPEC và phép kiểm phiên 1 nằm trong `tasks/T-026-nezha-ob-che-do-a/LOG.md`. Lượt ghi Q-84 chỉ cập nhật quyết định. Các kết quả kiểm của phiên 2 nằm ở mục dưới; không có kết quả xếp hạng.

## Điều kiện đã kiểm và việc còn OPEN

| Điều kiện SPEC bước 0 | Kết quả | Bằng chứng/phần còn thiếu |
|---|---|---|
| 0.1 — allowlist, hash, selector | **ĐẠT GUARD AUDIT; P3 OPEN** | In-memory allowlist 22 dev, selector từ chối 34 test trước I/O; 154 file khớp hash/byte nguồn tải. Chưa viết allowlist/selector thực thi P3. Bằng chứng 001 và mã trong LOG phiên 2. |
| 0.2 — mốc và đồng hồ | **ĐẠT PARSE TIME; ĐỒNG BỘ TUYỆT ĐỐI OPEN** | Time có +0000 UTC, phần lẻ 5–9 chữ số. Parse đầy đủ, so bằng Unix ns; đơn vị giây = ns/10^9. Mốc và ba bảng giữ Q-84. Hai cách parse độc lập khớp. Không xác nhận thời điểm tiêm thật. |
| 0.3 — N/A và chồng lần tiêm trước | **ĐÃ ĐẾM; NỀN SẠCH OPEN** | Từng ca/từng nguồn Time, span start/end và timestamp log có số trong 001/002. N không chứa mốc tiêm trước; recovery chưa biết. Báo hàng lặp và giây có bản ghi, không coi là độ phủ liên tục. |
| 0.4 — ánh xạ, U, tương thích TORAI | **OPEN** | Chưa chốt U hay ánh xạ. Audit schema T-008 cho biết metric có cadence 59/60/61 s và trace thiếu `statusCode`; code TORAI giả định metric 1 s rồi lấy mỗi 15 dòng. Nguồn: `results/T-008/runs/file-audit-001/summary.json:5943,5993,8025`; `src/torai/torai_sua.py:102`. Đây là căn cứ kiểm tương thích, chưa phải kết quả chạy. |
| 0.5 — xử lý phần thiếu theo phương pháp/nguồn | **CODE ĐÃ ĐỐI CHIẾU; THỰC THI OPEN** | Tách quan sát thật/lưới/điền theo WHY-35 ở mục dưới. Chưa chạy loader, dựng bảng hay phương pháp để đo số ô bù. Chưa chốt lưới/ánh xạ cho adapter. |
| 0.6 — trạng thái không hỗ trợ | **ĐÃ BÁO DỰ KIẾN; RUNTIME OPEN** | Bảng sáu phương pháp ở dưới. TORAI B dự kiến UNSUPPORTED do thiếu statusCode/cadence; các phương pháp khác có điều kiện. Không phát bản ghi NO_EVIDENCE/ERROR/OK khi chưa gọi phương pháp. |

## Mâu thuẫn nguồn mốc của một ca dev

- Ca có trong phần dev tại `results/T-021/chia-theo-o/A-phan-tang.csv:210`.
- Nhãn tác giả: `results/T-008/sources/labels/2022-08-22-fault_list.json:126–129`.
- Audit giữ nguyên: `results/T-008/runs/run-001/labels.json:258–260`.

| Trường | Giá trị nguồn | Hiểu UTC |
|---|---|---|
| `inject_time` | `2022-08-22 07:10:43` | 07:10:43 |
| `inject_timestamp` | `1661152183` (Unix giây) | 07:09:43 |

Chênh 60 s, không phải một độ lệch múi giờ chung: 21 ca dev khác khớp hai trường. Kiểm lại bằng chuyển đổi `datetime` độc lập và đối chiếu record nguồn, không dùng kết quả phương pháp; lệnh và thời gian kiểm tại LOG phiên 1.

Hai mốc làm N/A dịch 60 s và có thể đổi dữ liệu phương pháp nhận. **Chưa có bằng chứng chọn một trường làm thời điểm tiêm thật.** Không tự sửa nhãn, chọn mốc bằng tên minute-file hoặc dùng chất lượng xếp hạng để phân xử.

## Quy ước và giới hạn đã duyệt — Q-84 (07/10/2026)

Quyết định được ghi tại `docs/DECISIONS.md`, Q-84; sáu mục nguyên văn ở LOG phần "Quyết định của Minh trong phiên". Các đề xuất chưa duyệt ở LOG phiên 1 đã được Q-84 thay thế. Không sửa nhãn gốc, SPEC hay WHY trong lượt này.

### Mốc và ba bảng khai trước

Mốc chính = `inject_time` cho cả 22 ca dev, theo quy ước code tác giả (`results/T-008/sources/pattern_ranker.py:232–251,522`; QT2). Code tác giả bỏ phần giây khi chọn phút dữ liệu, nên chưa xác nhận mốc tới giây. **Thời điểm tiêm thật: OPEN.**

| Bảng khai trước | Tập ca | Mốc |
|---|---|---|
| Chính | 22 ca dev | `inject_time` cho cả 22 ca |
| Độ nhạy A | Cùng 22 ca dev | Riêng `OB\|recommendationservice\|cpu_consumed\|2022-08-22 07:10:43` dùng `inject_timestamp`; 21 ca khác giữ nguyên |
| Độ nhạy B | 21 ca có hai trường đồng thuận theo audit nhãn T-008 | `inject_time`; không đưa ca tranh chấp vào bảng này |

Ba bảng được khai trước khi chạy, chưa có kết quả. Kết luận giữ ở cả ba bảng thì báo ổn định; đổi chiều thì báo kèm điều kiện (QT3). Cận 1/22 chỉ áp cho trung bình Hit@k của một phương pháp; không dùng cho hiệu giữa hai phương pháp, Rerank hay bootstrap.

### Metric và các điểm OPEN của đồng hồ

- Đọc thời gian metric theo cột `Time`, như `results/T-008/sources/alarm.py:268–270`.
- **Quy tắc parse Time đã kiểm ở phiên 2:** dùng ngày giờ UTC + phần lẻ đầy đủ; bỏ hậu tố m=...; giữ Unix ns để so biên, chia 10^9 để biểu diễn giây. Bằng chứng chuỗi dev và hai phép kiểm ở mục dưới. Không suy đồng bộ tuyệt đối từ định dạng.
- Đồng bộ tuyệt đối của metric với trace/log: **OPEN**.
- Độ lệch khoảng −41 s ngày 22/08 và −32 s ngày 23/08 là giữa nội dung trace với phút trong tên tệp; nguyên nhân **OPEN**, không tự dịch đồng hồ hay ranh giới.
- Ghép log–trace chỉ kiểm được độ lệch tương đối, không xác nhận đồng bộ tuyệt đối với nhãn hoặc metric.

### N/A thực và điểm dừng hiện tại

Đã kiểm 0.2/0.3 ở phiên 2. Số theo nguồn và bảng trạng thái dự kiến nằm dưới. Dừng chờ Minh quyết phạm vi trước adapter; chưa chạy phương pháp hay evaluator.

## Kết quả phiên 2 — 0.2/0.3

Rà độc lập không thấy lỗi chặn mới của SPEC cho phạm vi phiên này. Đã kiểm parse Time và đếm N/A; chưa viết adapter, chạy pilot, phương pháp hay evaluator. Dừng theo Q-84 để Minh quyết phạm vi. Mọi số dưới đây lấy từ hai khối JSON bằng chứng cuối chính file này: `kiem-na-001` và `kiem-na-002-doc-lap`. Mỗi ca giữ đường dẫn từng nguồn; manifest giữ byte và SHA-256.

### 0.1 — guard trước đọc timestamp

Allowlist trong bộ kiểm có đúng 22 dev; chặn đủ 34 tên test và 2 tên giả trước I/O. 154 file nguồn, 1.041.219.665 byte, khớp manifest tải `results/T-008/runs/download-001/manifest.json`; chỉ `online-boutique/rca_data/` của hai ngày OB. Đây là guard audit đầu vào, chưa là allowlist/selector P3 thực thi cuối cùng. Không mở số đo test, locked, TT, construct hay repo lưu trữ.

Metric được đọc qua bộ lọc timestamp của các cửa sổ dev; người phân tích không mở raw file ngày. Trace/log chỉ ba minute-file thuộc chính ca dev. Độ nhạy A dùng cùng các file của ca tranh chấp, đổi cửa sổ theo mốc đã duyệt; không tìm thêm file để bù. Chỉ thống kê timestamp, ID và schema/operation trong cửa sổ, không phân tích số đo ngoài cửa sổ.

### 0.2 — quy tắc Time đã kiểm

Chuỗi nguồn là `YYYY-MM-DD HH:MM:SS.<1–9 chữ số> +0000 UTC m=<số có dấu>`. Ví dụ dev trong `online-boutique/rca_data/2022-08-22/metric/adservice-5f6585d649-fnmft_metric.csv`: `2022-08-22 03:57:19.601329777 +0000 UTC m=+360.107283757`. Các chuỗi được chọn thực tế có 5–9 chữ số phần lẻ. `+0000 UTC` là offset/múi giờ ghi trực tiếp trong nguồn; `m=...` là hậu tố monotonic (đồng hồ đơn điệu), không phải epoch.

Parse đầy đủ ngày giờ với UTC; phần lẻ đệm bên phải tới 9 chữ số. Bộ kiểm giữ Unix nanosecond bằng số nguyên để so biên; đổi sang đơn vị giây bằng ns/10^9, không làm tròn/floor giây và không dùng TimeStamp. Không lấy 19 ký tự đầu làm kết quả parse: cách đó bỏ phần lẻ. Hai mã độc lập (datetime + số nguyên; calendar + Decimal) khớp số dòng và first/last của mọi nguồn Time trong cả 23 cửa sổ kiểm. Code tác giả `alarm.py:268–270` chọn cột Time bằng regex; bằng chứng múi giờ ở chuỗi dev, không suy từ regex hoặc nhãn.

Thời điểm tiêm thật, độ chính xác giây của inject_time và đồng bộ tuyệt đối metric–trace–log vẫn OPEN. Mốc UTC trong kiểm là tọa độ của quy ước Q-84, không xác nhận injection thật. Độ lệch −41 s/−32 s giữa nội dung trace và tên minute-file vẫn OPEN; không dịch timestamp, file hay nhãn.

Log: `Timestamp` là RFC3339 UTC với Z; `TimeUnixNano` là Unix ns. Hai biểu diễn khớp từng dòng được chọn (0 lệch ở cả 23 cửa sổ). Cửa sổ log dùng chính TimeUnixNano, không suy từ trace. Trace: StartTimeUnixNano/EndTimeUnixNano là ns; Duration là µs. End−Start và Duration chênh dưới 1 µs do phần bị bỏ; 0 trường hợp sai kiểm này, 0 trường hợp đổi membership tại t hoặc t+300 khi so End nguồn với cách đổi µs của giao thức. Không chạy phương pháp để kiểm các số này.

### 0.3 — định nghĩa số đếm và phạm vi metric

N = [t−300,t), A = [t,t+300). Metric/log lọc nửa mở theo timestamp nguồn. Span chỉ vào khi start≥t−300 và end<t+300; báo cả split theo start (SimpleRCA/TORAI bin) và theo end (MicroRank/TraceRCA, đồ thị N CIRCA). N end nghĩa là span đã kết thúc trước t, không lấy min/max StartTime thay số này.

Metric đã đếm 11 file Time/ngày: 10 file resource `<pod>_metric.csv` và front_service.csv. Mỗi file mỗi ca có 5 dòng N và 5 dòng A; không coi 55 hàng của 11 nguồn là 55 thời điểm chung. source_50.csv/destination_50.csv có cột `time` chữ thường, dependency.csv không có thời gian (`results/T-008/runs/file-audit-001/summary.json`, entries cùng path). Chưa chọn chúng làm kênh phương pháp, chưa parse/chuyển clock của chúng; ánh xạ kênh và lưới chung vẫn OPEN ở 0.4/0.5. Các con số metric bên dưới chỉ đại diện nguồn Time đã duyệt, không khẳng định đã có bảng đầu vào chung.

Audit cũ T-008 bỏ phần lẻ của Time khi đếm nên báo 59/60/61 s; đó không phải các bước full precision (đầy đủ độ chính xác). Cadence thật trong cửa sổ là khoảng 59,54–60,49 s; 5 phép đo mỗi phía trải từ khoảng 239,59–240,33 s giữa first/last. Báo giây có bản ghi = số bucket giây UTC có ít nhất một timestamp; hull = last−first. Cả hai đều không chứng minh độ phủ liên tục. Không nội suy hay thêm hàng khi đếm.

Mốc tiêm trước theo inject_time cách mốc chính 488–1.037 s; tất cả N bắt đầu sau mốc trước, tất cả A kết thúc trước mốc kế. Ca độ nhạy A có khoảng cách mốc trước 498 s và cũng đạt. Đây chỉ kiểm không chứa lần tiêm kế/trước theo metadata; thời lượng lỗi, recovery và nền sạch vẫn OPEN (`results/T-021/goi-g1.md:185`; `results/T-008/the-dataset.md:52,61,67`). Không lấy construct làm nền.

### Bảng số hàng theo ca

Metric ghi số hàng **mỗi file Time**. Trace end ghi hàng đã hoàn tất, trace start ghi hàng bắt đầu mỗi phía; chưa tự loại hàng lặp. Nhãn/locator chỉ nằm trong audit này; không có đầu ra để truyền cho phương pháp. Đường dẫn nguồn đầy đủ nằm tại `cases[].metric[].path`, `trace.sources[].path`, `log.sources[].path` của khối 001.

| Ca (OB; ngày giờ / service / fault) | Metric N/A mỗi file | Trace N/A theo end | Trace N/A theo start | Log N/A |
|---|---:|---:|---:|---:|
| 2022-08-23 16:31:35 / adservice / cpu_contention | 5 / 5 | 25,764 / 37,743 | 25,776 / 37,731 | 27,713 / 40,608 |
| 2022-08-22 05:01:13 / checkoutservice / exception | 5 / 5 | 20,859 / 51,956 | 20,873 / 51,942 | 22,598 / 55,360 |
| 2022-08-23 13:02:09 / checkoutservice / exception | 5 / 5 | 16,158 / 54,565 | 16,158 / 54,565 | 17,413 / 58,207 |
| 2022-08-22 04:52:55 / checkoutservice / network_delay | 5 / 5 | 38,966 / 34,979 | 38,975 / 34,970 | 41,865 / 37,466 |
| 2022-08-23 12:53:52 / checkoutservice / network_delay | 5 / 5 | 31,749 / 37,654 | 31,761 / 37,642 | 34,084 / 40,324 |
| 2022-08-22 05:09:50 / checkoutservice / return | 5 / 5 | 36,362 / 34,917 | 36,376 / 34,903 | 38,961 / 37,392 |
| 2022-08-23 13:10:36 / checkoutservice / return | 5 / 5 | 26,329 / 44,004 | 26,333 / 44,000 | 28,314 / 47,067 |
| 2022-08-23 14:03:48 / emailservice / cpu_consumed | 5 / 5 | 31,951 / 40,546 | 31,955 / 40,542 | 34,111 / 43,476 |
| 2022-08-22 05:43:48 / emailservice / network_delay | 5 / 5 | 34,960 / 35,203 | 34,964 / 35,199 | 37,378 / 37,846 |
| 2022-08-23 13:54:37 / emailservice / network_delay | 5 / 5 | 27,490 / 44,746 | 27,490 / 44,746 | 29,327 / 48,056 |
| 2022-08-22 04:02:07 / frontend / return | 5 / 5 | 18,497 / 29,714 | 18,504 / 29,707 | 19,846 / 36,041 |
| 2022-08-23 12:10:21 / frontend / return | 5 / 5 | 19,751 / 26,759 | 19,757 / 26,753 | 21,473 / 32,302 |
| 2022-08-22 06:01:18 / paymentservice / cpu_contention | 5 / 5 | 23,054 / 48,834 | 23,060 / 48,828 | 24,650 / 52,195 |
| 2022-08-23 14:21:54 / paymentservice / cpu_contention | 5 / 5 | 34,784 / 36,526 | 34,784 / 36,526 | 38,134 / 39,890 |
| 2022-08-23 15:04:28 / productcatalogservice / exception | 5 / 5 | 25,037 / 14,113 | 25,069 / 14,081 | 26,940 / 19,467 |
| 2022-08-22 07:10:43 / recommendationservice / cpu_consumed | 5 / 5 | 21,736 / 19,617 | 21,773 / 19,580 | 23,374 / 20,849 |
| 2022-08-23 15:29:49 / recommendationservice / cpu_consumed | 5 / 5 | 32,892 / 20,105 | 32,892 / 20,105 | 35,854 / 21,389 |
| 2022-08-22 06:52:56 / recommendationservice / network_delay | 5 / 5 | 37,756 / 28,338 | 37,784 / 28,310 | 40,506 / 30,423 |
| 2022-08-23 15:12:49 / recommendationservice / network_delay | 5 / 5 | 32,101 / 35,618 | 32,101 / 35,618 | 34,367 / 38,000 |
| 2022-08-23 15:56:24 / shippingservice / cpu_consumed | 5 / 5 | 22,533 / 47,600 | 22,537 / 47,596 | 24,294 / 51,118 |
| 2022-08-22 07:26:48 / shippingservice / cpu_contention | 5 / 5 | 33,470 / 34,443 | 33,487 / 34,426 | 36,012 / 37,459 |
| 2022-08-23 15:47:43 / shippingservice / cpu_contention | 5 / 5 | 30,522 / 41,186 | 30,524 / 41,184 | 32,819 / 44,367 |
| 2022-08-22 07:10:43 / recommendationservice / cpu_consumed (độ nhạy A) | 5 / 5 | 9,128 / 32,225 | 9,132 / 32,221 | 9,794 / 34,429 |

### Giây có bản ghi và số span duy nhất

Các giây trace dưới đây đếm theo end. Metric có 5 giây có bản ghi mỗi phía ở mỗi nguồn Time; cột train là số quan sát thật trong [t−120,t−10], không phải kích thước train hiệu lực.

| Ca (ngày giờ / service / fault) | Trace giây N/A | Log giây N/A | Span khóa duy nhất N/A end | Metric train mỗi nguồn |
|---|---:|---:|---:|---:|
| 2022-08-23 16:31:35 / adservice / cpu_contention | 68 / 113 | 68 / 113 | 25,463 / 37,743 | 1 |
| 2022-08-22 05:01:13 / checkoutservice / exception | 54 / 128 | 54 / 128 | 20,859 / 51,956 | 2 |
| 2022-08-23 13:02:09 / checkoutservice / exception | 42 / 140 | 42 / 140 | 16,158 / 54,475 | 2 |
| 2022-08-22 04:52:55 / checkoutservice / network_delay | 96 / 86 | 96 / 86 | 38,794 / 34,979 | 2 |
| 2022-08-23 12:53:52 / checkoutservice / network_delay | 85 / 97 | 85 / 97 | 31,749 / 37,654 | 2 |
| 2022-08-22 05:09:50 / checkoutservice / return | 91 / 90 | 91 / 90 | 36,246 / 34,869 | 2 |
| 2022-08-23 13:10:36 / checkoutservice / return | 69 / 113 | 69 / 113 | 26,267 / 44,004 | 1 |
| 2022-08-23 14:03:48 / emailservice / cpu_consumed | 81 / 101 | 81 / 101 | 31,951 / 40,298 | 2 |
| 2022-08-22 05:43:48 / emailservice / network_delay | 89 / 93 | 89 / 93 | 34,763 / 35,092 | 2 |
| 2022-08-23 13:54:37 / emailservice / network_delay | 70 / 112 | 70 / 112 | 27,490 / 44,562 | 1 |
| 2022-08-22 04:02:07 / frontend / return | 48 / 133 | 48 / 133 | 18,497 / 29,381 | 2 |
| 2022-08-23 12:10:21 / frontend / return | 53 / 127 | 53 / 127 | 19,751 / 26,759 | 2 |
| 2022-08-22 06:01:18 / paymentservice / cpu_contention | 59 / 121 | 59 / 121 | 23,054 / 48,724 | 2 |
| 2022-08-23 14:21:54 / paymentservice / cpu_contention | 86 / 94 | 86 / 94 | 34,546 / 36,405 | 2 |
| 2022-08-23 15:04:28 / productcatalogservice / exception | 61 / 120 | 61 / 120 | 24,894 / 14,030 | 2 |
| 2022-08-22 07:10:43 / recommendationservice / cpu_consumed | 85 / 101 | 85 / 101 | 20,826 / 19,116 | 2 |
| 2022-08-23 15:29:49 / recommendationservice / cpu_consumed | 82 / 105 | 82 / 105 | 32,768 / 19,578 | 2 |
| 2022-08-22 06:52:56 / recommendationservice / network_delay | 97 / 85 | 97 / 85 | 37,706 / 28,165 | 2 |
| 2022-08-23 15:12:49 / recommendationservice / network_delay | 82 / 100 | 82 / 100 | 32,039 / 35,373 | 2 |
| 2022-08-23 15:56:24 / shippingservice / cpu_consumed | 57 / 125 | 57 / 125 | 22,533 / 47,188 | 2 |
| 2022-08-22 07:26:48 / shippingservice / cpu_contention | 89 / 92 | 89 / 92 | 33,355 / 34,381 | 2 |
| 2022-08-23 15:47:43 / shippingservice / cpu_contention | 75 / 105 | 75 / 105 | 30,522 / 41,124 | 2 |
| 2022-08-22 07:10:43 / recommendationservice / cpu_consumed (độ nhạy A) | 25 / 161 | 25 / 161 | 9,128 / 30,814 | 2 |

Độ nhạy A chỉ thay ca tranh chấp; 21 ca khác tái dùng số chính. Độ nhạy B tái dùng đúng 21 ca đồng thuận, không chạy/đếm lại hay chọn ca theo số. Cả hai mốc tranh chấp giữ 5/5 metric mỗi nguồn, nhưng trace/log N/A đổi rõ như hai dòng trong bảng. Chưa có kết luận xếp hạng để gọi ổn định hay đổi chiều.

### Quan sát thật và phần hiệu lực — WHY-35

Ở 22 ca chính, trace N có 42–97 giây có bản ghi; A có 85–140 giây. Log được đếm riêng, cũng cho khoảng 42–97 / 85–140 giây; sự trùng khoảng này là kết quả hai phép đếm, không phải suy log từ trace. First/last và hull cụ thể của mọi nguồn có trong khối 001. Các khoảng này không phải 300 s thu thập liên tục và không chứng minh phần trước t sạch lỗi.

Kiểm độc lập 002 thấy 5.800 hàng span lặp khóa giữa minute-file ở 19/22 ca chính; 0 nội dung mâu thuẫn khi so toàn row. Log có 6.433 hàng giống hệt lặp trong các cửa sổ chính. Đây là hàng theo file, không phải sự kiện độc lập. Khối 002 báo số khóa span duy nhất N/A và số log lặp N/A cho từng ca. Không xóa/gộp dữ liệu gốc và chưa chọn chính sách dedup (loại bản ghi lặp) chung cho adapter. Giữ cách xử lý của từng phương pháp; riêng MicroRank kiểm conflicts trên các cột đầu vào và xử lý graph theo code (`src/microrank/__init__.py:40–41`; `graph.py:15–25`).

Ghép log–trace chỉ dùng khóa TraceID/SpanID trong cửa sổ; kiểm tương thích thời gian tương đối với start/end, không dịch đồng hồ. Các khoảng lệch tương đối và số dòng thiếu span trong cửa sổ nằm ở `cases[].log.join`; span lặp đã kiểm giống hệt nên không có chọn bản ghi mâu thuẫn khi nối. Một log có thể ở trước end của span là bình thường về thứ tự; phép nối này không chứng minh đồng bộ tuyệt đối với nhãn/metric.

BARO dùng các hàng metric có thật; SimpleRCA dùng các hàng có thật theo kênh, có thể bỏ kênh thiếu điều kiện của code. MicroRank/TraceRCA dùng span trong cửa sổ và split theo end. Chưa gọi các phương pháp, nên chưa có số hàng sau preprocess, kênh được dùng hay trạng thái runtime.

CIRCA: mỗi nguồn Time có 1 hoặc 2 quan sát thật trong [t−120,t−10] (bảng trên và khối 001). Code scoring đặt interval 1 s; loader resample, interpolate và bfill (`src/circa_kien_truc/scoring.py:39`; `D:/RCA-ext/src/RCAEval/RCAEval/classes/data.py:89–104,175`). 111 điểm train là số trên lưới hiệu lực theo code, không phải 111 phép đo. Chưa nạp loader/scorer trong phiên này; số điểm được nội suy/điền cụ thể, các kênh hữu hạn sau mapping, current sau chuyển schema và khả năng dựng graph còn OPEN. Adapter phải khai các số đó trước khi dùng kết quả, giữ current theo quan sát thật cuối A và code gốc OLS.

TORAI B: code dựng 40 bin 15 s, mỗi phía 20 bin, rồi fillna(0) (`src/p3/torai_b.py:73,78,106,113`). Số 0 vào bin thiếu thu thập là phần bù, không phải quan sát thật. Chưa dựng logts/tracets hay đo số ô bù, vì thiếu statusCode và chưa được viết adapter. Cadence metric khoảng 60 s, trong khi TORAI lấy mỗi 15 **hàng** (`src/torai/torai_sua.py:102–103`): trên một chuỗi 10 điểm gốc chỉ giữ điểm đầu N và không có điểm A. Lưới/pivot chung của 11 nguồn còn chưa chốt; không suy rằng đã tạo bảng 10 hàng cho TORAI. Không đổi stride, giả statusCode=0 hoặc nội suy 1 s để cứu phương pháp.

Không tạo file payload dẫn xuất (bảng metric/span/log đầu vào) trên đĩa; không có file cần xóa sau giữ manifest. Chỉ giữ thống kê và manifest nguồn trong báo cáo. 001 mất 33,391 s; 002 mất 33,156 s. Mọi lượt lỗi/hỏng trong thao tác đọc/soạn lệnh được ghi LOG; không có lượt phương pháp/evaluator.

### Bảng phương pháp × trạng thái dự kiến × lý do

Đây là CANDIDATE có điều kiện, **không phải kết quả chạy hoặc bản ghi trạng thái**. `UNSUPPORTED` dùng cho dữ liệu/trường bắt buộc không tương thích. `NO_EVIDENCE` là trả về bình thường nhưng không có bằng chứng; `ERROR` là ngoại lệ/lỗi hợp đồng, theo giao thức §8.3 (`results/T-022/giao-thuc-v2.md:278–285`). Không tự đổi loại thiếu dữ liệu thành một trạng thái runtime.

| Phương pháp | Trạng thái dự kiến có điều kiện | Lý do / bằng chứng |
|---|---|---|
| BARO | Có thể xét triển khai; chưa xác nhận OK | 5 N/5 A mỗi nguồn Time. Chia theo time<t, dùng hàng thật, không tạo lưới (`src/p3/adapters/baro.py:18–25,34`). Phụ thuộc ánh xạ kênh, bảng chung và giá trị hữu hạn; chưa kiểm bằng gọi phương pháp. |
| SimpleRCA M4 | Có thể xét triển khai; có thể NO_EVIDENCE theo code | Có metric N/A, trace N/A và log A. Metric cần ≥2 giá trị hữu hạn N; kênh trace cần N/A; log chỉ cần A (`src/simplerca/core.py:63–99`). Thiếu điều kiện một kênh không tự là UNSUPPORTED; abstain → NO_EVIDENCE (`src/p3/adapters/simplerca.py:25–27`). Mapping, kênh và bản ghi lặp chưa chốt. |
| MicroRank | Có thể xét triển khai; NO_EVIDENCE/ERROR phụ thuộc lời gọi | Span N/A end khác rỗng ở mọi cửa sổ. Audit native (PodName,OperationName) không thấy operation A thiếu N hay N<2, nhưng chưa là mapping operation/service của phương pháp. Code thiếu cửa sổ → missing_window/NO_EVIDENCE, operation mới/std NaN → ERROR (`src/microrank/__init__.py:49–56,68–70`). Không khẳng định sẽ OK hoặc có trace bất thường. |
| TraceRCA | Có thể xét triển khai; NO_EVIDENCE/ERROR phụ thuộc lời gọi | Có N/A end; không cần statusCode. Operation mới sau mapping có thể KeyError, ji không hữu hạn hết → NO_EVIDENCE (`D:/RCA-ext/src/RCAEval/RCAEval/e2e/tracerca.py:53–60`; `src/p3/adapters/tracerca.py:53–59`). Audit pod/operation chưa thay được methodName và ánh xạ đã kiểm. |
| CIRCA OLS kiến trúc | Có thể xét với điều kiện phải báo nội suy/điền theo code | Có span đã kết thúc ở N để khảo sát graph; metric train chỉ 1–2 điểm thật mỗi nguồn, khác 111 điểm lưới. Phụ thuộc mapping hậu tố (`src/circa_kien_truc/builder.py:8–25`), lưới chung, graph từ span N (`src/p3/adapters/circa.py:36–43`) và current A thật (`:116–120`). Giữ OLS gốc/Q-80,Q-82; chưa có score hay route. |
| TORAI B | Dự kiến UNSUPPORTED với schema/cấu hình hiện hành | Toàn 66 trace-file dev được hash đều không có statusCode; tracets_err bắt buộc tổng statusCode (`src/p3/torai_b.py:60,66,72`). Cadence 60 s còn không khớp ý nghĩa stride 15 hàng; bộ lọc ts-* hiện là TT (`src/p3/adapters/torai.py:18–20`). Không chế field, đổi stride/lọc kênh hay fallback TORAI A của TT (WHY-29). |

**Điểm dừng:** 0.2 parse và 0.3 thống kê đã làm; chưa hoàn thành 0.4/0.5 hay hợp đồng adapter. Cần Minh quyết phạm vi phương pháp/adapter sau bảng này, gồm TORAI B không tương thích, cách trình bày CIRCA trên ít phép đo thật, ánh xạ kênh/lưới chung và cách giữ bản ghi lặp. Chưa đánh dấu task xong/chờ phản biện. Không sửa SPEC, WHY, DECISIONS hoặc code; chưa có quyết định khoa học mới.

## Manifest và số theo từng nguồn

Path trong hai khối JSON dưới đây tính từ `D:/RCA-flashticket/data/ngoai-rcaeval/nezha/`. Đây chỉ là thống kê/hash, không chứa các giá trị metric, message log hay bảng span dẫn xuất. `seconds_with_rows` là giây UTC có ít nhất một bản ghi; `hull_s` là khoảng first/last. Không gọi hai số này là độ phủ liên tục.

<!-- T026_AUDIT_JSON_START -->

{
  "run": "kiem-na-001",
  "scope": "22 OB dev main + disputed sensitivity A; sensitivity B reuses 21 unchanged cases; no method/evaluator",
  "hash_s": 1.3130000000019209,
  "metric_s": 0.2969999999986612,
  "elapsed_s": 33.39099999999962,
  "manifest": [
    {
      "path": "online-boutique/rca_data/2022-08-22/log/04_02_log.csv",
      "sha256": "686424bdcd1359fcfa0336224dc0dc1e8724e1e7f200eff88a7656241cfb542f",
      "bytes": 12293045
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/04_03_log.csv",
      "sha256": "95709831d65c54a558139e4b62dbae380cc5624242ca68a75298a35fd8c16a14",
      "bytes": 7758376
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/04_04_log.csv",
      "sha256": "b76b4b79513d8b65e8023f038091776a66a46bf35186641887cf859f7677ea8f",
      "bytes": 8694407
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/04_52_log.csv",
      "sha256": "d8633aa9d8f9609394474dfe3c50136259fac8e9f062e82e60f3c55b169647ef",
      "bytes": 13350542
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/04_53_log.csv",
      "sha256": "bcfaaa998b66e77e57400a870c245c50a1cebdbf6cc947d6421c5843df5cd235",
      "bytes": 13376452
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/04_54_log.csv",
      "sha256": "71caf25509841da500cb5b3d1b49010d4901a94a9c47bc711f4ac27fffc755db",
      "bytes": 13493991
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/05_01_log.csv",
      "sha256": "d17b2b1781aaa0896cc575fca353bb93bb283b6de2e5fc6879910993d7eb62b8",
      "bytes": 12890991
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/05_02_log.csv",
      "sha256": "e3498e0f7f9869baee92bd7231e5dbde660517cfde37b1ee5c9bc934cef01ac9",
      "bytes": 13639031
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/05_03_log.csv",
      "sha256": "71bb29593d72f763f1fd3f6602d65b737f20cadf63c3d71faeb2d4640db9657c",
      "bytes": 12950913
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/05_09_log.csv",
      "sha256": "b66cb04d169cbf644f791f96a8f37eefd860e3a9aeb07dd6ceadd7fbd9d1dbc6",
      "bytes": 13016538
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/05_10_log.csv",
      "sha256": "ebd8e0caccbbded85449e68eb4604005c9b16afa07baf2ba0b8f0a7b29d15d94",
      "bytes": 12813617
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/05_11_log.csv",
      "sha256": "fbb5ee9543ab163c01386d51d2e59ed6828c0492d7d35d6156f5435b71d2a6f7",
      "bytes": 12864203
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/05_43_log.csv",
      "sha256": "71285d0de8055c246f00dad851be3616dda3b6f606af4e657f4c16d58049e524",
      "bytes": 12748877
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/05_44_log.csv",
      "sha256": "9fdb702a1987e98f6f919182071c41fb71a974fb190f471e646b1697625915b2",
      "bytes": 12529193
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/05_45_log.csv",
      "sha256": "a23bfd841d5ac898f746e8d7cc73415914d31ad64b44d935ce19a9d34e3ffeda",
      "bytes": 12859575
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/06_01_log.csv",
      "sha256": "a64b1caac492857252b2448682d0f15360fd2ad6d66d6fec2445d174f9caea70",
      "bytes": 12786231
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/06_02_log.csv",
      "sha256": "5580a136e89df97cd318c8d79bbbdcaba3e8248fa3b695976a2d0b95785c550e",
      "bytes": 13314671
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/06_03_log.csv",
      "sha256": "c87643cce92033d857f31bec5a88b79dd35ea99faef77d777eae140fbe74015e",
      "bytes": 12842159
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/06_52_log.csv",
      "sha256": "03283347fd9da40ede6c3bd7a24a00cf8807ece7c1ede9e88e9a9355e70bebc5",
      "bytes": 13008363
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/06_53_log.csv",
      "sha256": "12092f105186107a1c1198bef5317e56a32f11faa5e702d0f157859f9eb26562",
      "bytes": 11907448
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/06_54_log.csv",
      "sha256": "556d50cda0be6620d435a99dc767bda7d87df957e51d7b36bef0f446aca5611e",
      "bytes": 11053693
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/07_10_log.csv",
      "sha256": "f4db2a85a381ed16f6dfb110a182ac920cdaff297b219b195bb61720df9b12ea",
      "bytes": 9274188
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/07_11_log.csv",
      "sha256": "0185b605376d872267d018fb51eb566857113103cd1852947a3d8757d73d22dd",
      "bytes": 6307860
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/07_12_log.csv",
      "sha256": "8364b582a48d16c97d28773dbbf966e56c7b96387c7fb314811bce98236543fe",
      "bytes": 6836660
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/07_26_log.csv",
      "sha256": "9b269ae0e6a246e8a425f842d5b53b9df24818bddebc0d093f4272705eec3b2b",
      "bytes": 12506732
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/07_27_log.csv",
      "sha256": "056d2fa8d73fd5e6a2fdcaa7403823c289b7ebc3c26ef3a2e02a17416c6e414c",
      "bytes": 12301905
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/log/07_28_log.csv",
      "sha256": "d5a6e427943c2847b4610e68a8a56d799662f12273fcc8608d1b1fef104d25d9",
      "bytes": 12442621
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/metric/adservice-5f6585d649-fnmft_metric.csv",
      "sha256": "9be62744e0cae2149832a25db2f69994dd70acb803c1db1fb9cb8aaf416f24c0",
      "bytes": 438579
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/metric/cartservice-579f59597d-wc2lz_metric.csv",
      "sha256": "75f14417cc9d51de722e6f1369f4e60e5e5a8073d8d8b97488135a3b74700b0d",
      "bytes": 449258
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
      "sha256": "b15e657df68f4f5b75f0b895170fb4fbe1fe25025a45654f88a65766c044ab85",
      "bytes": 444826
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
      "sha256": "e7c956af459dad836b2e29d59d0162ceeeda13c87c55d090b8c4a17358ac198a",
      "bytes": 491789
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/metric/emailservice-55fdc5b988-f6xth_metric.csv",
      "sha256": "84807415f0c781f35d72cc9fe388b12d16505038334dd77728490913f4e45255",
      "bytes": 430468
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/metric/front_service.csv",
      "sha256": "fc3a33fe996e19ba9e9e45da12de014f1a90962c162ad7ba318ab8c307326aac",
      "bytes": 187712
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/metric/frontend-579b9bff58-t2dbm_metric.csv",
      "sha256": "b57425d0f68d2043d39a96c7298bfb455c7e5429ae7796f89e20be56049b02c2",
      "bytes": 472074
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/metric/paymentservice-9cdb6588f-554sm_metric.csv",
      "sha256": "1f826edb68857dfb8d3a4d684971b06ba9c2a01a4a30881beb272852cac4c675",
      "bytes": 432559
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/metric/productcatalogservice-668d5f85fb-wckp8_metric.csv",
      "sha256": "a4ff21e16aa3df699576db8a5f399d3f83af45e47c554004daab6277688e8cc8",
      "bytes": 468397
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
      "sha256": "b37c3347bd680d8d5534cb539e6896f963084758e5a5825464177668e1944475",
      "bytes": 495393
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
      "sha256": "9ef8c32d61b0cc424145ce275a9a61862c68d9b922a13c938ce77c71e08946f2",
      "bytes": 433368
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/04_02_trace.csv",
      "sha256": "24fcfd6de86a274f1048a501a47187e59b86c24269bb3391e8ca72a954c585df",
      "bytes": 3996213
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/04_03_trace.csv",
      "sha256": "58476bcf1bc3221f2290fe0314a149210e8d97c7fc63d5046c6ba080b0998766",
      "bytes": 2152040
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/04_04_trace.csv",
      "sha256": "5564d31f9b74682acd83760fa6ffb6d4b9d50ac1dd98ad08a580f849db27c365",
      "bytes": 2474824
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/04_52_trace.csv",
      "sha256": "cdfeb06f813fb0edab5dce91ee00bcb8c5388d42b628af3012d104282181e0e5",
      "bytes": 4360945
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/04_53_trace.csv",
      "sha256": "e3e6dd32aae86956c0a2efc48e8b4146b5a0052f126f56916bbbbb0959d3bd80",
      "bytes": 4447122
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/04_54_trace.csv",
      "sha256": "48886552282135888a60de4613d19c46107591e39196e6bd6f166ecacef77278",
      "bytes": 4418148
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/05_01_trace.csv",
      "sha256": "aea0fa820bb0908b5b6aba71fc727ba8c3a9b9a36f79f27c81f71de7426d0bff",
      "bytes": 4211092
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/05_02_trace.csv",
      "sha256": "159cc3dde371b9b2277c3634cd2c2e63b5b38ffc774b8281946f49743d30e916",
      "bytes": 4530583
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/05_03_trace.csv",
      "sha256": "342c64137db0fbc8e83b2bdc931d52c2ae270b4750386e30c65afbd801471dcf",
      "bytes": 4274960
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/05_09_trace.csv",
      "sha256": "162e230c8c6a0a8396128224cf2a1306efb5b467fd2e459f9fb9a1d297e56493",
      "bytes": 4312495
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/05_10_trace.csv",
      "sha256": "52515ba354dac6082920817ef435d354bc4b673cd14938a4611c4b0038c8e1f8",
      "bytes": 4171672
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/05_11_trace.csv",
      "sha256": "a44c439f4c579a14f2e8a5bb0dcdde3dcfefd55a25e44739a7f5825f8868a611",
      "bytes": 4259860
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/05_43_trace.csv",
      "sha256": "311b0777f6bfd25415dc0b787791b4c2e597e5cd19ab0d0677d3f8535db60b30",
      "bytes": 4183294
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/05_44_trace.csv",
      "sha256": "4fdce2a132ec29c90049259fd228e831f15401fc66647add2cc13629e08097b2",
      "bytes": 4141816
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/05_45_trace.csv",
      "sha256": "0a19a32a9ba00a6617ca93babe465db30be4646fedfea647a786a284b096b882",
      "bytes": 4221201
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/06_01_trace.csv",
      "sha256": "ab71ea18b448dd7368348fdfc7178d14d41027e2459352cb74d6b5b8b42e5fdd",
      "bytes": 4220263
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/06_02_trace.csv",
      "sha256": "b204391d5aba57a6341c41ce901035995df517fc90978e8047c8ba3d4debc9cf",
      "bytes": 4415708
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/06_03_trace.csv",
      "sha256": "d5a7f3607eda77861d1cd2a55fb5d5ef770ed3e4e8c3c5767ce7eb722a2f439f",
      "bytes": 4220595
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/06_52_trace.csv",
      "sha256": "f3ce1a32e193aaee0cdd754c9c89630bd004650c52db7349a248d5e3cb745890",
      "bytes": 4280948
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/06_53_trace.csv",
      "sha256": "d78b42b437a6eb20e6fcfcb91a8af65c4b5a628541a263bb9144c2828f31c555",
      "bytes": 3924761
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/06_54_trace.csv",
      "sha256": "5a004ba36d62521c3bf992e8e3fb6d2c1fbd61d05872ed501bd2b0dfa31aab5f",
      "bytes": 3614241
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/07_10_trace.csv",
      "sha256": "ad5408c76e17888e90e584b9cfa3953ad8a685ef5f644f4e4d5ee5ce6c930008",
      "bytes": 3055523
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/07_11_trace.csv",
      "sha256": "c4fbb0bac25de18f99f799bfa0907dbe0b86dada6398a70fc5829e946d9e2a8d",
      "bytes": 2079098
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/07_12_trace.csv",
      "sha256": "969adde7532ca58aa8fa8abd64ae4688f3358b1e98ffce30d2f2c4cbfca68386",
      "bytes": 2265108
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/07_26_trace.csv",
      "sha256": "c8b71a0093eaa11621cee6e0839b6d6714ae05fd91d81f770498eb17133e9275",
      "bytes": 4109561
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/07_27_trace.csv",
      "sha256": "a396332f34da560a7f71198a52ba99af7cfcce01c035429e0f1895cc99e8fd57",
      "bytes": 4003842
    },
    {
      "path": "online-boutique/rca_data/2022-08-22/trace/07_28_trace.csv",
      "sha256": "931d3a8af74f3face4102845b1a97ecaf113296c324013770f8c53d72f9ea114",
      "bytes": 4030205
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/12_10_log.csv",
      "sha256": "06831a5dbd529fe5bbdaf81bf5fa94ad7d303b67680e6a8ad377c52fc96f6754",
      "bytes": 11779777
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/12_11_log.csv",
      "sha256": "4ad0c5a0b8d4ebc17c9c7aa63db5e0146c75a8e1c8cf52cb39f177cb92ed6f6c",
      "bytes": 7673767
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/12_12_log.csv",
      "sha256": "09644e17066c43423920b699fb3e10d0abea4f03601844e18b8f7ccc4c616ff7",
      "bytes": 8082508
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/12_53_log.csv",
      "sha256": "11592fbbda026353b528e5c017b3fc99be6c4c5a847dcedfdbd1dea2f5ab5e32",
      "bytes": 12304566
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/12_54_log.csv",
      "sha256": "d9e686349212ea1d86bc99f9e83c64e61afaf5d5da9465e66902b4dff45b7faf",
      "bytes": 12784758
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/12_55_log.csv",
      "sha256": "381610257aca29dc0cbfd29b77b67c5f1c9ac1f020a26b6303ae2829778057ea",
      "bytes": 12455224
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/13_02_log.csv",
      "sha256": "58de40ff36be03b7b232cc86f16f2e08e8598a5624eb92451beec0f96d48d483",
      "bytes": 12680389
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/13_03_log.csv",
      "sha256": "e136cc7f0446962e6cfe67af27722facb0f8b1ce5168e8355c1f3a51da340bdb",
      "bytes": 12626158
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/13_04_log.csv",
      "sha256": "47ce7526a2f5bc137620335819a83af193e48415c63f87ff7b3fcb6793dddffc",
      "bytes": 12795155
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/13_10_log.csv",
      "sha256": "3a508fe8ec3afbca15ca0668d43f14834d082669a2467d120d6e787c5ffab57c",
      "bytes": 12731275
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/13_11_log.csv",
      "sha256": "7dab96d639909623a8067c96371c0789c288b996076653d6780ae8cce79af8d1",
      "bytes": 12386024
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/13_12_log.csv",
      "sha256": "76936ff7d25994ff848e30c2e6b72c7ff548b303797e225ef80114a2ce33634f",
      "bytes": 12901646
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/13_54_log.csv",
      "sha256": "1823703ca345427bf28fbe7dd755342b1398f45c4baeec04ac18452af73c196b",
      "bytes": 12978774
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/13_55_log.csv",
      "sha256": "ca85e0fc61554caf7450f1e78aa25b69ee7c1128de873ff42c13bcbd517d9791",
      "bytes": 12770348
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/13_56_log.csv",
      "sha256": "0a7bd4fc1ff6cbf6986f12d79cef4908e7e202e78575210339f2ced334428e6a",
      "bytes": 13271913
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/14_03_log.csv",
      "sha256": "16a8cdbaf83c0c35c408d3b8872b41a07bada4878a9e29775c7daa6a637efceb",
      "bytes": 12808698
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/14_04_log.csv",
      "sha256": "abe75ff026d8ae14247d8854ba8d7153b65f9a4769d439c6e5e5cf35ced594d9",
      "bytes": 12805997
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/14_05_log.csv",
      "sha256": "5a0bbb2179a5b5abd7f3a0692d0b8016454b8ef89d7747b72a9ca2e3a1cb4ec5",
      "bytes": 13524716
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/14_21_log.csv",
      "sha256": "0cdbf6211158ff483c2c53495695785a3b4d2763b33f2a1e56abeacf5b2d892f",
      "bytes": 13299378
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/14_22_log.csv",
      "sha256": "495a8c3d17c488bc8395e3d5bf848b7b18e1a064420cd583b9b57334fbf4e991",
      "bytes": 13336569
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/14_23_log.csv",
      "sha256": "9f8eefb958f8a358c727800f7e1b2aa5a9d6b8d6d3d9ab1af56901bd32c04df9",
      "bytes": 12726134
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/15_04_log.csv",
      "sha256": "aca84c36619ddb2b9dc98ffb5669f1e62f8b493f43156356c69c42faf1c645ac",
      "bytes": 13541407
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/15_05_log.csv",
      "sha256": "e6f0f591dcf7fdacf7689df08834494acbc284494049c0f8405d8f2321dcc199",
      "bytes": 5499026
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/15_06_log.csv",
      "sha256": "0957df6f765d3523c31ad969acb98177c9d66772cef7d883395d02b737a62997",
      "bytes": 5046501
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/15_12_log.csv",
      "sha256": "0decbabf4910c05e54672135c8b669835b80098f88b0bc9a69c0f75f0ff9826a",
      "bytes": 12421007
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/15_13_log.csv",
      "sha256": "e9503ab82647b8a0d24ec7cf932d1a276d7b7c46493473977f16725d54c632c5",
      "bytes": 12501069
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/15_14_log.csv",
      "sha256": "772d086c4d01d45add2c6060e7061d4c9e71f69a80913d1123a5412d598d797e",
      "bytes": 11573309
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/15_29_log.csv",
      "sha256": "b9c9efb358b6bccff89d6341ccd90a5feabdcddad607f90073d4e8f0fed605f3",
      "bytes": 13396182
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/15_30_log.csv",
      "sha256": "4d7af2c315e6469e474e6ebcd687e5f13035c05a7d0d369fc289f15ae438131e",
      "bytes": 8784977
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/15_31_log.csv",
      "sha256": "b53c6382aabc42b6eed1495d5f53998e2821a89ac68b6dd54f211f30739ba8fd",
      "bytes": 6711292
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/15_47_log.csv",
      "sha256": "e51f8ba5d6716b968749832f20e3084c53e6255a74818e5e24e0dc206db26ad5",
      "bytes": 12970041
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/15_48_log.csv",
      "sha256": "8d594b268561b00fb0f16daef9e336b04d0eb7b08fa0ee03a32efdf196b9864e",
      "bytes": 13456709
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/15_49_log.csv",
      "sha256": "24d39e147bf92424a9a6264c567b2e150895a1c2edd921c31f90f03c3697eac3",
      "bytes": 12506960
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/15_56_log.csv",
      "sha256": "3aca75211d65e60539038b4122df39d367d2f9716e40c0f103d9c93227f53b92",
      "bytes": 13115075
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/15_57_log.csv",
      "sha256": "18b0cb2e0e1e522bd266862747c336e6e6353f071061a08406519d609a25e424",
      "bytes": 12496416
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/15_58_log.csv",
      "sha256": "464ef120c69e1c4fa3b7663a064e4f6f0b8d8e0ec9b7537edb3b08094af230ef",
      "bytes": 12434145
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/16_31_log.csv",
      "sha256": "569e691634237015fea0f6d48e3b1b134ac1fdc55e98d4e979ecec8353cfb7dd",
      "bytes": 12430721
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/16_32_log.csv",
      "sha256": "203f21770994fdffbee5584d5b253589573220216ce4c77ecf8984325d2038c1",
      "bytes": 11661827
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/log/16_33_log.csv",
      "sha256": "9592fab5a750bbc946f1fbe1416fae09ac9b2001cdd984c7d72facc1d1bff799",
      "bytes": 10413756
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/metric/adservice-5f6585d649-fnmft_metric.csv",
      "sha256": "90cfda1fbc2140245bc478e4439f27aef1ca6345caecb05a2c680fd774a89243",
      "bytes": 198291
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/metric/cartservice-579f59597d-wc2lz_metric.csv",
      "sha256": "187e1ac099f86083c256c9e5e938c6410fb7462dff221b15e86b350a4d0a8144",
      "bytes": 263915
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
      "sha256": "f8658101a777d1a6762ba61e67e0ac4a31e8e9649c6e0eca911352c7ba0031b0",
      "bytes": 267964
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
      "sha256": "01ea8f5c2a12a128b26897475bef660e1416491d5cee59f1df010e5c97c3a0d1",
      "bytes": 290274
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/metric/emailservice-55fdc5b988-f6xth_metric.csv",
      "sha256": "db0eb16b4a058f9724d9f6b84c7a840ba96c5073ddcf082103345a0068005ac6",
      "bytes": 248468
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/metric/front_service.csv",
      "sha256": "bb954d76cc2b0a514ed7025e63cec0f65ad8f8f50a3bab8d16a275aad91e6074",
      "bytes": 112586
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/metric/frontend-579b9bff58-t2dbm_metric.csv",
      "sha256": "3ed4dd169d675649e5d56b5205099602142315c2b675993e3986415daa447d10",
      "bytes": 279154
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/metric/paymentservice-9cdb6588f-554sm_metric.csv",
      "sha256": "1a05ee5adce4f9b90a2a41c0ca02c8e9947181cec3fcf258a507fa50cd2727de",
      "bytes": 255149
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/metric/productcatalogservice-668d5f85fb-jhwx9_metric.csv",
      "sha256": "c5377f8c11e114d4e3ee22234507de5a0bfe5c9a04fe17caefada2210b1fe5a6",
      "bytes": 280301
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
      "sha256": "b8aedd0871fcf8d02dee5611bdb94315b688610f61821a16ea0a0c4ea349c55d",
      "bytes": 290617
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
      "sha256": "db108f871e4b9b5f1b857f86de4df52f9043fd66e745d8801da3abfd605f4fee",
      "bytes": 263806
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/12_10_trace.csv",
      "sha256": "0ccc564c91fbebe33d716e3383f36c95b481b318bed80f9a43e8111a29889fc4",
      "bytes": 3822840
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/12_11_trace.csv",
      "sha256": "e677d267aa25641450851a6be4a4de153f960bf3be8dedb652be1f79d8a36fa6",
      "bytes": 2191152
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/12_12_trace.csv",
      "sha256": "12d32e69b8fefce854b0efa7944fd8b1ad54ccb488616d228a2126b3c29e7089",
      "bytes": 2300080
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/12_53_trace.csv",
      "sha256": "6feab10d99e534af28be2607ef2321636d98b771c67e779e8b221ed5a16918f6",
      "bytes": 4068246
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/12_54_trace.csv",
      "sha256": "6b7c9d39183693eac80217ee3b62f55ed807cc1a0064990f3d1614aad913f143",
      "bytes": 4208246
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/12_55_trace.csv",
      "sha256": "d510fa06329cfbf67971da0236b2c6968c9f41684f0add6228c717400b04428a",
      "bytes": 4123302
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/13_02_trace.csv",
      "sha256": "02b92c00fdcd2dcb4900e93a02eb166606dcefaa9e46cb102741cc3e8711d4f7",
      "bytes": 4147609
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/13_03_trace.csv",
      "sha256": "5088975ace0856bd7bca4126cb60d01190e01627efdf41b9ba1e1e84eaa1ea8e",
      "bytes": 4219100
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/13_04_trace.csv",
      "sha256": "ddcb6b1297a41d269f3376a253366cab9ef977b46becb612e875f5169b50fc7c",
      "bytes": 4268624
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/13_10_trace.csv",
      "sha256": "577eb7420aa18adbaa02d60743c98816e36552bfa70969bcc3c94d716c8a3632",
      "bytes": 4187059
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/13_11_trace.csv",
      "sha256": "8eee59db83f4cfb09e61fea053ad8a61cf7cbf9b69adcf6c53f780755becce89",
      "bytes": 4080106
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/13_12_trace.csv",
      "sha256": "43d52d7ff25820567bf87b5d90d3577626fdc3783aaff9f507e764c5f0923926",
      "bytes": 4295262
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/13_54_trace.csv",
      "sha256": "7699d8a231f929c7ee6215c2f8c02dcbc89863203e5fe3ab1769490ab53d2472",
      "bytes": 4344531
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/13_55_trace.csv",
      "sha256": "1c63f8b50f08ee383affff8fbca959f61b9f6e068cc5008e7d721d70ed63be99",
      "bytes": 4218188
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/13_56_trace.csv",
      "sha256": "72cb3000b79d7797a4d8e75ca3f53ea9de354ba4db3f5f5802d9fabc294c5bb7",
      "bytes": 4347455
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/14_03_trace.csv",
      "sha256": "c34547c0329147f32929825894bf81a8deae2c00e8fd85402addcc045edfb191",
      "bytes": 4260377
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/14_04_trace.csv",
      "sha256": "406145115576306f4b291f670b7bcacc91678ff61a7688f384a6e7e780cd8b44",
      "bytes": 4223287
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/14_05_trace.csv",
      "sha256": "0586350e0f2005462715278635ca10633fd29c0377ab04aff8af170ac7271166",
      "bytes": 4474655
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/14_21_trace.csv",
      "sha256": "4e53cff3ec0ce6b9ccf6b7361e8ad707f2a67bfac117b15408fff735dd62615e",
      "bytes": 4316883
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/14_22_trace.csv",
      "sha256": "65775c5d7fbf806b647a2aaa4af8f8bf092a4f07cf8b5d16780bba54df4603c9",
      "bytes": 4300870
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/14_23_trace.csv",
      "sha256": "1c550b518312da711ba3bebed1859e9c5546fa86871b44cc6540e9d1f31bd412",
      "bytes": 4128658
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/15_04_trace.csv",
      "sha256": "a9dab65d21882e86af9295f8c4b4622a0bd8881e0e751d0063d463a9ce938a41",
      "bytes": 4460731
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/15_05_trace.csv",
      "sha256": "78e3fb1b59c78c501e4754b1c7d8b87ed83132f2193ead0659e9f51d82bd0152",
      "bytes": 1336697
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/15_06_trace.csv",
      "sha256": "d00d9d2555d1ada4bd1ef2350b6044a865b26540d465bf3bffccd8dff5ecd862",
      "bytes": 1189188
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/15_12_trace.csv",
      "sha256": "49e68fe4d3b2d224eea894513f52ce2dc92c5328d0a1609ec28e35c7ab974255",
      "bytes": 4105918
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/15_13_trace.csv",
      "sha256": "b4bb1d0e3ad9500e526ac40d0b7544dc7623bb188c79e554948873c30b1a289f",
      "bytes": 4162230
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/15_14_trace.csv",
      "sha256": "726c6674fdffea5e96b839ec6a65c490ce91b0d482b099d0aa3ce13870ac066c",
      "bytes": 3837785
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/15_29_trace.csv",
      "sha256": "43ab1860232475759600575885332d68c922c87a40648c34b6081fd5166a662a",
      "bytes": 4379418
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/15_30_trace.csv",
      "sha256": "839cf2fe30b9e82154af6339cf3d8c139c9c5af3fb0fbdb299443f82eba7f15a",
      "bytes": 2869787
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/15_31_trace.csv",
      "sha256": "a0978cfb312481f839863c23939519329c258ad1ce55537d13f02293e587d7d4",
      "bytes": 2227684
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/15_47_trace.csv",
      "sha256": "7a5adc5502effa68815c7353a446881d4d3580b3ea2f6b9a4245bfaf81dc2ce5",
      "bytes": 4254543
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/15_48_trace.csv",
      "sha256": "8dfea48b4e9249872a4627820ef96d593988a6b72004f101b0888ef522b8066b",
      "bytes": 4458063
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/15_49_trace.csv",
      "sha256": "5d2bc872aaef3d0d7cf22d4dcd1f8f46c8d64cf125e422da2e5c06e15e401496",
      "bytes": 4103014
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/15_56_trace.csv",
      "sha256": "2dd83075da020a95fbd6ab35c6680a1afcba5b67aae38cff3520244ab89ce05d",
      "bytes": 4319307
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/15_57_trace.csv",
      "sha256": "414b07b0f4be40edc5d345ceb20cdf9981e8f0651221e6d18c0e1ba913b53419",
      "bytes": 4077771
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/15_58_trace.csv",
      "sha256": "e68d30de0658229d2532b233f9b59bffd9936d4322dddffcba36ab766329f2e9",
      "bytes": 4137728
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/16_31_trace.csv",
      "sha256": "fce8652944763057be041b51a3a17fda774acc48a51fe5d416e8a17dee64e626",
      "bytes": 4102780
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/16_32_trace.csv",
      "sha256": "98e9a839f961f52b977d5894c6114c3ae8f62790802d08f47d3a0c6e77d4f4e6",
      "bytes": 3833809
    },
    {
      "path": "online-boutique/rca_data/2022-08-23/trace/16_33_trace.csv",
      "sha256": "61b0bd75b89faa0df8b1942c96d57483c95fedd755fbb6e72f7755b9a583ffb4",
      "bytes": 3419140
    }
  ],
  "metric_Time_samples": {
    "online-boutique/rca_data/2022-08-22/metric/adservice-5f6585d649-fnmft_metric.csv": "2022-08-22 03:57:19.601329777 +0000 UTC m=+360.107283757",
    "online-boutique/rca_data/2022-08-22/metric/cartservice-579f59597d-wc2lz_metric.csv": "2022-08-22 03:57:19.651248613 +0000 UTC m=+360.157202594",
    "online-boutique/rca_data/2022-08-22/metric/checkoutservice-578fcf4766-9csqn_metric.csv": "2022-08-22 03:57:19.743787534 +0000 UTC m=+360.249741515",
    "online-boutique/rca_data/2022-08-22/metric/currencyservice-cf787dd48-vpjrd_metric.csv": "2022-08-22 03:57:19.791070043 +0000 UTC m=+360.297024023",
    "online-boutique/rca_data/2022-08-22/metric/emailservice-55fdc5b988-f6xth_metric.csv": "2022-08-22 03:57:19.820898677 +0000 UTC m=+360.326852658",
    "online-boutique/rca_data/2022-08-22/metric/front_service.csv": "2022-08-22 03:57:19.552898907 +0000 UTC m=+360.058852887",
    "online-boutique/rca_data/2022-08-22/metric/frontend-579b9bff58-t2dbm_metric.csv": "2022-08-22 03:57:19.863442594 +0000 UTC m=+360.369396578",
    "online-boutique/rca_data/2022-08-22/metric/paymentservice-9cdb6588f-554sm_metric.csv": "2022-08-22 03:57:19.905923507 +0000 UTC m=+360.411877601",
    "online-boutique/rca_data/2022-08-22/metric/productcatalogservice-668d5f85fb-wckp8_metric.csv": "2022-08-22 03:57:19.949654612 +0000 UTC m=+360.455608592",
    "online-boutique/rca_data/2022-08-22/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv": "2022-08-22 03:57:20.011277721 +0000 UTC m=+360.517231710",
    "online-boutique/rca_data/2022-08-22/metric/shippingservice-7b598fc7d-lmggd_metric.csv": "2022-08-22 03:57:20.073211466 +0000 UTC m=+360.579165447",
    "online-boutique/rca_data/2022-08-23/metric/adservice-5f6585d649-fnmft_metric.csv": "2022-08-23 12:05:28.115581244 +0000 UTC m=+360.098017519",
    "online-boutique/rca_data/2022-08-23/metric/cartservice-579f59597d-wc2lz_metric.csv": "2022-08-23 12:05:28.154239624 +0000 UTC m=+360.136675900",
    "online-boutique/rca_data/2022-08-23/metric/checkoutservice-578fcf4766-9csqn_metric.csv": "2022-08-23 12:05:28.209115841 +0000 UTC m=+360.191552116",
    "online-boutique/rca_data/2022-08-23/metric/currencyservice-cf787dd48-vpjrd_metric.csv": "2022-08-23 12:05:28.242353437 +0000 UTC m=+360.224789712",
    "online-boutique/rca_data/2022-08-23/metric/emailservice-55fdc5b988-f6xth_metric.csv": "2022-08-23 12:05:28.26828503 +0000 UTC m=+360.250721320",
    "online-boutique/rca_data/2022-08-23/metric/front_service.csv": "2022-08-23 12:05:28.076108083 +0000 UTC m=+360.058544365",
    "online-boutique/rca_data/2022-08-23/metric/frontend-579b9bff58-t2dbm_metric.csv": "2022-08-23 12:05:28.322360107 +0000 UTC m=+360.304796382",
    "online-boutique/rca_data/2022-08-23/metric/paymentservice-9cdb6588f-554sm_metric.csv": "2022-08-23 12:05:28.362549681 +0000 UTC m=+360.344986031",
    "online-boutique/rca_data/2022-08-23/metric/productcatalogservice-668d5f85fb-jhwx9_metric.csv": "2022-08-23 12:05:28.417219375 +0000 UTC m=+360.399655658",
    "online-boutique/rca_data/2022-08-23/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv": "2022-08-23 12:05:28.483801095 +0000 UTC m=+360.466237370",
    "online-boutique/rca_data/2022-08-23/metric/shippingservice-7b598fc7d-lmggd_metric.csv": "2022-08-23 12:05:28.544646838 +0000 UTC m=+360.527083114"
  },
  "fraction_digits_in_selected_metric_rows": {
    "9": 2103,
    "8": 191,
    "7": 24,
    "6": 2,
    "5": 1
  },
  "cases": [
    {
      "case": "OB|adservice|cpu_contention|2022-08-23 16:31:35",
      "view": "main",
      "t_ns": 1661272295000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272048325370612,
            "last_ns": 1661272288321858331,
            "hull_s": 239.996487719
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272348287771266,
            "last_ns": 1661272588318313233,
            "hull_s": 240.030541967
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.968569301,
            60.035814542,
            59.949918303,
            60.042185573,
            59.965912935,
            60.030443772,
            60.061969671,
            59.904035556,
            60.034092968
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272048392615301,
            "last_ns": 1661272288384692581,
            "hull_s": 239.99207728
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272348323938299,
            "last_ns": 1661272588372324624,
            "hull_s": 240.048386325
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.936277577,
            60.069800812,
            59.911885225,
            60.074113666,
            59.939245718,
            60.061219229,
            60.064418796,
            59.949384292,
            59.973364008
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272048481116593,
            "last_ns": 1661272288476829111,
            "hull_s": 239.995712518
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272348384286714,
            "last_ns": 1661272588432430161,
            "hull_s": 240.048143447
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.919299873,
            60.100193391,
            59.866308904,
            60.10991035,
            59.907457603,
            60.095994771,
            60.035863831,
            60.012203357,
            59.904081488
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272048542920844,
            "last_ns": 1661272288543112680,
            "hull_s": 240.000191836
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272348423634371,
            "last_ns": 1661272588469511182,
            "hull_s": 240.045876811
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.893251429,
            60.136309359,
            59.831490003,
            60.139141045,
            59.880521691,
            60.121365975,
            60.005010779,
            60.013852001,
            59.905648056
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272048576316965,
            "last_ns": 1661272288601000254,
            "hull_s": 240.024683289
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272348461527071,
            "last_ns": 1661272588611952681,
            "hull_s": 240.15042561
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.894631289,
            60.155175639,
            59.810140302,
            60.164736059,
            59.860526817,
            60.141547996,
            59.970107511,
            60.025206169,
            60.013563934
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272048257072618,
            "last_ns": 1661272288258920718,
            "hull_s": 240.0018481
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272348249654643,
            "last_ns": 1661272588254115716,
            "hull_s": 240.004461073
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.993318745,
            60.00724009,
            59.988548395,
            60.01274087,
            59.990733925,
            60.004777324,
            60.000735993,
            59.992739873,
            60.006207883
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272048632991771,
            "last_ns": 1661272288680201189,
            "hull_s": 240.047209418
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272348532516522,
            "last_ns": 1661272588719657078,
            "hull_s": 240.187140556
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.905645608,
            60.176275951,
            59.783042109,
            60.18224575,
            59.852315333,
            60.153478048,
            59.938405847,
            60.031813939,
            60.063442722
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272048661803884,
            "last_ns": 1661272288744119128,
            "hull_s": 240.082315244
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272348565725411,
            "last_ns": 1661272588757633010,
            "hull_s": 240.191907599
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.912512182,
            60.18834928,
            59.765139719,
            60.216314063,
            59.821606283,
            60.179864146,
            59.907646672,
            60.033542949,
            60.070853832
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/productcatalogservice-668d5f85fb-jhwx9_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272048695616781,
            "last_ns": 1661272288775099276,
            "hull_s": 240.079482495
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272348601314387,
            "last_ns": 1661272588803507675,
            "hull_s": 240.202193288
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.920999659,
            60.189386332,
            59.757072287,
            60.212024217,
            59.826215111,
            60.209398142,
            59.871163511,
            60.036705232,
            60.084926403
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272048727323453,
            "last_ns": 1661272288809893321,
            "hull_s": 240.082569868
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272348635409485,
            "last_ns": 1661272588848189676,
            "hull_s": 240.212780191
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.923589018,
            60.214382527,
            59.729818939,
            60.214779384,
            59.825516164,
            60.240595387,
            59.831816172,
            60.046061266,
            60.094307366
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272048762635175,
            "last_ns": 1661272288843400753,
            "hull_s": 240.080765578
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661272348666249503,
            "last_ns": 1661272588900446612,
            "hull_s": 240.234197109
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.917467882,
            60.235401001,
            59.714180426,
            60.213716269,
            59.82284875,
            60.272495841,
            59.803290299,
            60.047096789,
            60.11131418
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/16_31_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 22953,
                "seconds_with_rows": 62,
                "first_ns": 1661272227874681329,
                "last_ns": 1661272288606186767,
                "hull_s": 60.731505438
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "end_split": {
              "N": {
                "rows": 22953,
                "seconds_with_rows": 62,
                "first_ns": 1661272227878646528,
                "last_ns": 1661272288610770033,
                "hull_s": 60.732123505
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/16_32_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 2823,
                "seconds_with_rows": 8,
                "first_ns": 1661272287552068421,
                "last_ns": 1661272294999011376,
                "hull_s": 7.446942955
              },
              "A": {
                "rows": 18607,
                "seconds_with_rows": 53,
                "first_ns": 1661272295000940800,
                "last_ns": 1661272347578177792,
                "hull_s": 52.577236992
              }
            },
            "end_split": {
              "N": {
                "rows": 2811,
                "seconds_with_rows": 8,
                "first_ns": 1661272287562825800,
                "last_ns": 1661272294995246592,
                "hull_s": 7.432420792
              },
              "A": {
                "rows": 18619,
                "seconds_with_rows": 53,
                "first_ns": 1661272295001110016,
                "last_ns": 1661272347579828585,
                "hull_s": 52.578718569
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/16_33_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 19124,
                "seconds_with_rows": 60,
                "first_ns": 1661272348195165261,
                "last_ns": 1661272408433425298,
                "hull_s": 60.238260037
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 19124,
                "seconds_with_rows": 60,
                "first_ns": 1661272348199741082,
                "last_ns": 1661272408437890669,
                "hull_s": 60.238149587
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 25776,
            "seconds_with_rows": 68,
            "first_ns": 1661272227874681329,
            "last_ns": 1661272294999011376,
            "hull_s": 67.124330047
          },
          "A": {
            "rows": 37731,
            "seconds_with_rows": 113,
            "first_ns": 1661272295000940800,
            "last_ns": 1661272408433425298,
            "hull_s": 113.432484498
          }
        },
        "end_split": {
          "N": {
            "rows": 25764,
            "seconds_with_rows": 68,
            "first_ns": 1661272227878646528,
            "last_ns": 1661272294995246592,
            "hull_s": 67.116600064
          },
          "A": {
            "rows": 37743,
            "seconds_with_rows": 113,
            "first_ns": 1661272295001110016,
            "last_ns": 1661272408437890669,
            "hull_s": 113.436780653
          }
        },
        "straddle_t": 12,
        "duplicate_keys": 301,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/log/16_31_log.csv",
            "N": {
              "rows": 24655,
              "seconds_with_rows": 62,
              "first_ns": 1661272227874712434,
              "last_ns": 1661272288610742533,
              "hull_s": 60.736030099
            },
            "A": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/16_32_log.csv",
            "N": {
              "rows": 3058,
              "seconds_with_rows": 8,
              "first_ns": 1661272287552103095,
              "last_ns": 1661272294998983199,
              "hull_s": 7.446880104
            },
            "A": {
              "rows": 20026,
              "seconds_with_rows": 53,
              "first_ns": 1661272295001143476,
              "last_ns": 1661272347579795693,
              "hull_s": 52.578652217
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/16_33_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 20582,
              "seconds_with_rows": 60,
              "first_ns": 1661272348195216845,
              "last_ns": 1661272408437866134,
              "hull_s": 60.242649289
            }
          }
        ],
        "N": {
          "rows": 27713,
          "seconds_with_rows": 68,
          "first_ns": 1661272227874712434,
          "last_ns": 1661272294998983199,
          "hull_s": 67.124270765
        },
        "A": {
          "rows": 40608,
          "seconds_with_rows": 113,
          "first_ns": 1661272295001143476,
          "last_ns": 1661272408437866134,
          "hull_s": 113.436722658
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 68321,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.592e-06,
            4.906202311
          ],
          "relative_end_s": [
            -5.494092182,
            0.061537937
          ]
        }
      },
      "previous_inject_time_ns": 1661271773000000000,
      "previous_gap_s": 522.0,
      "next_gap_s": 562.0,
      "elapsed_s": 1.2340000000003783
    },
    {
      "case": "OB|checkoutservice|exception|2022-08-22 05:01:13",
      "view": "main",
      "t_ns": 1661144473000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144179685725173,
            "last_ns": 1661144419685911827,
            "hull_s": 240.000186654
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144479866140522,
            "last_ns": 1661144719684308197,
            "hull_s": 239.818167675
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.960033748,
            60.22402243,
            59.990776824,
            59.825353652,
            60.180228695,
            59.772672607,
            59.992273243,
            60.018177006,
            60.035044819
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144179764712835,
            "last_ns": 1661144419842804096,
            "hull_s": 240.078091261
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144479714122985,
            "last_ns": 1661144719750138756,
            "hull_s": 240.036015771
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.914140974,
            60.064405473,
            59.945291674,
            60.15425314,
            59.871318889,
            59.956723344,
            59.988871619,
            60.034605349,
            60.055815459
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144179962943423,
            "last_ns": 1661144419927450109,
            "hull_s": 239.964506686
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144479953715712,
            "last_ns": 1661144719825970969,
            "hull_s": 239.872255257
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.775855471,
            60.084438968,
            59.932598335,
            60.171613912,
            60.026265603,
            59.805404168,
            59.947342428,
            60.047389914,
            60.072118747
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144180077423529,
            "last_ns": 1661144419962550131,
            "hull_s": 239.885126602
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144480017171033,
            "last_ns": 1661144719869600113,
            "hull_s": 239.85242908
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.700818208,
            60.086075233,
            59.931745923,
            60.166487238,
            60.054620902,
            59.812212085,
            59.913618729,
            60.052431394,
            60.074166872
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144180123243458,
            "last_ns": 1661144419989440611,
            "hull_s": 239.866197153
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144480082116006,
            "last_ns": 1661144719901054665,
            "hull_s": 239.818938659
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.702874635,
            60.066959914,
            59.93160661,
            60.164755994,
            60.092675395,
            59.911246775,
            59.792178395,
            60.038914206,
            60.076599283
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144179618465617,
            "last_ns": 1661144419615994358,
            "hull_s": 239.997528741
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144479615048931,
            "last_ns": 1661144719618007794,
            "hull_s": 240.002958863
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.995042778,
            59.999453118,
            59.997776455,
            60.00525639,
            59.999054573,
            59.993033521,
            59.994010557,
            60.01237974,
            60.003535045
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144180184453373,
            "last_ns": 1661144420032400450,
            "hull_s": 239.847947077
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144480153290576,
            "last_ns": 1661144719945257450,
            "hull_s": 239.791966874
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.693037005,
            60.060203027,
            59.934429189,
            60.160277856,
            60.120890126,
            59.904648234,
            59.766794926,
            60.050445318,
            60.070078396
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144180243264488,
            "last_ns": 1661144420061531670,
            "hull_s": 239.818267182
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144480212336940,
            "last_ns": 1661144719979266229,
            "hull_s": 239.766929289
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.668209312,
            60.063110315,
            59.931505517,
            60.155442038,
            60.15080527,
            59.882785054,
            59.758492584,
            60.065641002,
            60.060010649
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/productcatalogservice-668d5f85fb-wckp8_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144180282105001,
            "last_ns": 1661144420110968523,
            "hull_s": 239.828863522
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144480277935168,
            "last_ns": 1661144720012998074,
            "hull_s": 239.735062906
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.684345152,
            60.06644298,
            59.928869208,
            60.149206182,
            60.166966645,
            59.848505574,
            59.764780019,
            60.075528284,
            60.046249029
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144180314503464,
            "last_ns": 1661144420176937691,
            "hull_s": 239.862434227
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144480339419281,
            "last_ns": 1661144720045519304,
            "hull_s": 239.706100023
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.827326393,
            59.939461701,
            59.934657484,
            60.160988649,
            60.16248159,
            59.813574396,
            59.780856588,
            60.077961487,
            60.033707552
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144180356024537,
            "last_ns": 1661144420246522772,
            "hull_s": 239.890498235
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144480403614205,
            "last_ns": 1661144720082048435,
            "hull_s": 239.67843423
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.863853291,
            59.897046585,
            59.94595891,
            60.183639449,
            60.157091433,
            59.780273199,
            59.794620629,
            60.093453816,
            60.010086586
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/05_01_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 20873,
                "seconds_with_rows": 54,
                "first_ns": 1661144419432388150,
                "last_ns": 1661144472999742976,
                "hull_s": 53.567354826
              },
              "A": {
                "rows": 2681,
                "seconds_with_rows": 7,
                "first_ns": 1661144473000060296,
                "last_ns": 1661144479214217715,
                "hull_s": 6.214157419
              }
            },
            "end_split": {
              "N": {
                "rows": 20859,
                "seconds_with_rows": 54,
                "first_ns": 1661144419439520315,
                "last_ns": 1661144472999796736,
                "hull_s": 53.560276421
              },
              "A": {
                "rows": 2695,
                "seconds_with_rows": 7,
                "first_ns": 1661144473000425972,
                "last_ns": 1661144479216196528,
                "hull_s": 6.215770556
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/05_02_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 25346,
                "seconds_with_rows": 61,
                "first_ns": 1661144479622159950,
                "last_ns": 1661144539204194270,
                "hull_s": 59.58203432
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 25346,
                "seconds_with_rows": 61,
                "first_ns": 1661144479631844183,
                "last_ns": 1661144539208628906,
                "hull_s": 59.576784723
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/05_03_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 23915,
                "seconds_with_rows": 62,
                "first_ns": 1661144539441450741,
                "last_ns": 1661144600100487474,
                "hull_s": 60.659036733
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 23915,
                "seconds_with_rows": 62,
                "first_ns": 1661144539441708568,
                "last_ns": 1661144600103232377,
                "hull_s": 60.661523809
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 20873,
            "seconds_with_rows": 54,
            "first_ns": 1661144419432388150,
            "last_ns": 1661144472999742976,
            "hull_s": 53.567354826
          },
          "A": {
            "rows": 51942,
            "seconds_with_rows": 128,
            "first_ns": 1661144473000060296,
            "last_ns": 1661144600100487474,
            "hull_s": 127.100427178
          }
        },
        "end_split": {
          "N": {
            "rows": 20859,
            "seconds_with_rows": 54,
            "first_ns": 1661144419439520315,
            "last_ns": 1661144472999796736,
            "hull_s": 53.560276421
          },
          "A": {
            "rows": 51956,
            "seconds_with_rows": 128,
            "first_ns": 1661144473000425972,
            "last_ns": 1661144600103232377,
            "hull_s": 127.102806405
          }
        },
        "straddle_t": 14,
        "duplicate_keys": 0,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-22/log/05_01_log.csv",
            "N": {
              "rows": 22598,
              "seconds_with_rows": 54,
              "first_ns": 1661144419432431953,
              "last_ns": 1661144472999910267,
              "hull_s": 53.567478314
            },
            "A": {
              "rows": 2816,
              "seconds_with_rows": 7,
              "first_ns": 1661144473001243585,
              "last_ns": 1661144479216160062,
              "hull_s": 6.214916477
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/log/05_02_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 26953,
              "seconds_with_rows": 61,
              "first_ns": 1661144479622209488,
              "last_ns": 1661144539208597794,
              "hull_s": 59.586388306
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/log/05_03_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 25591,
              "seconds_with_rows": 62,
              "first_ns": 1661144539441505740,
              "last_ns": 1661144600103205038,
              "hull_s": 60.661699298
            }
          }
        ],
        "N": {
          "rows": 22598,
          "seconds_with_rows": 54,
          "first_ns": 1661144419432431953,
          "last_ns": 1661144472999910267,
          "hull_s": 53.567478314
        },
        "A": {
          "rows": 55360,
          "seconds_with_rows": 128,
          "first_ns": 1661144473001243585,
          "last_ns": 1661144600103205038,
          "hull_s": 127.101961453
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 77958,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.765e-06,
            1.946309923
          ],
          "relative_end_s": [
            -1.946304674,
            0.022425942
          ]
        }
      },
      "previous_inject_time_ns": 1661143975000000000,
      "previous_gap_s": 498.0,
      "next_gap_s": 517.0,
      "elapsed_s": 1.5
    },
    {
      "case": "OB|checkoutservice|exception|2022-08-23 13:02:09",
      "view": "main",
      "t_ns": 1661259729000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259448170976652,
            "last_ns": 1661259688159298385,
            "hull_s": 239.988321733
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259748186786489,
            "last_ns": 1661259988189050835,
            "hull_s": 240.002264346
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.979165149,
            60.062238094,
            59.944858841,
            60.002059649,
            60.027488104,
            59.995092603,
            59.985384138,
            59.988506304,
            60.033281301
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259448205333822,
            "last_ns": 1661259688205496172,
            "hull_s": 240.00016235
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259748243258917,
            "last_ns": 1661259988256862230,
            "hull_s": 240.013603313
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.979112913,
            60.109146583,
            59.898065784,
            60.01383707,
            60.037762745,
            59.977721115,
            59.9843446,
            59.983630082,
            60.067907516
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259448267907551,
            "last_ns": 1661259688287782304,
            "hull_s": 240.019874753
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259748312740904,
            "last_ns": 1661259988344042121,
            "hull_s": 240.031301217
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.982823627,
            60.30497176,
            59.691186713,
            60.040892653,
            60.0249586,
            59.982718917,
            59.970712471,
            59.978413089,
            60.09945674
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259448302108933,
            "last_ns": 1661259688355652792,
            "hull_s": 240.053543859
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259748362651735,
            "last_ns": 1661259988411593442,
            "hull_s": 240.048941707
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.984216953,
            60.345258213,
            59.645289598,
            60.078779095,
            60.006998943,
            59.96998231,
            59.983293333,
            59.968648282,
            60.127017782
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259448330486184,
            "last_ns": 1661259688421950201,
            "hull_s": 240.091464017
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259748421676427,
            "last_ns": 1661259988474525285,
            "hull_s": 240.052848858
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.983144735,
            60.364251941,
            59.623460784,
            60.120606557,
            59.999726226,
            59.944376087,
            59.977660759,
            59.973512092,
            60.15729992
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259448124419154,
            "last_ns": 1661259688120079486,
            "hull_s": 239.995660332
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259748122111776,
            "last_ns": 1661259988131366987,
            "hull_s": 240.009255211
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.993550311,
            60.022388364,
            59.985263906,
            59.994457751,
            60.00203229,
            60.010108047,
            59.992811658,
            59.996312201,
            60.010023305
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259448385671297,
            "last_ns": 1661259688511023384,
            "hull_s": 240.125352087
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259748499844769,
            "last_ns": 1661259988562602121,
            "hull_s": 240.062757352
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.979832076,
            60.387674681,
            59.598487122,
            60.159358208,
            59.988821385,
            59.925804404,
            59.969641489,
            59.984673783,
            60.182637676
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259448440429346,
            "last_ns": 1661259688561286231,
            "hull_s": 240.120856885
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259748537339692,
            "last_ns": 1661259988635042432,
            "hull_s": 240.09770274
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.957234979,
            60.392829407,
            59.644207046,
            60.126585453,
            59.976053461,
            59.923060047,
            59.98565252,
            59.969153082,
            60.219837091
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/productcatalogservice-668d5f85fb-jhwx9_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259448498254432,
            "last_ns": 1661259688598982718,
            "hull_s": 240.100728286
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259748578344117,
            "last_ns": 1661259988798478288,
            "hull_s": 240.220134171
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.9314665,
            60.426397033,
            59.694152136,
            60.048712617,
            59.979361399,
            59.91932318,
            60.006816949,
            59.959381249,
            60.334612793
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259448538344547,
            "last_ns": 1661259688692515394,
            "hull_s": 240.154170847
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259748627131722,
            "last_ns": 1661259988845272848,
            "hull_s": 240.218141126
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.926874878,
            60.457425839,
            59.66818382,
            60.10168631,
            59.934616328,
            59.907424088,
            60.170102113,
            59.928785673,
            60.211829252
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259448592614234,
            "last_ns": 1661259688804051369,
            "hull_s": 240.211437135
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259748667833992,
            "last_ns": 1661259988911174628,
            "hull_s": 240.243340636
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.909101545,
            60.487154916,
            59.643655807,
            60.171524867,
            59.863782623,
            59.913559805,
            60.176362435,
            59.910207363,
            60.243211033
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/13_02_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 16158,
                "seconds_with_rows": 42,
                "first_ns": 1661259687526987593,
                "last_ns": 1661259728728233728,
                "hull_s": 41.201246135
              },
              "A": {
                "rows": 7044,
                "seconds_with_rows": 19,
                "first_ns": 1661259729058907279,
                "last_ns": 1661259747797806904,
                "hull_s": 18.738899625
              }
            },
            "end_split": {
              "N": {
                "rows": 16158,
                "seconds_with_rows": 42,
                "first_ns": 1661259687588714496,
                "last_ns": 1661259728730374674,
                "hull_s": 41.141660178
              },
              "A": {
                "rows": 7044,
                "seconds_with_rows": 19,
                "first_ns": 1661259729063254528,
                "last_ns": 1661259747800625986,
                "hull_s": 18.737371458
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/13_03_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 23625,
                "seconds_with_rows": 61,
                "first_ns": 1661259748124929738,
                "last_ns": 1661259808002155264,
                "hull_s": 59.877225526
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 23625,
                "seconds_with_rows": 61,
                "first_ns": 1661259748125213863,
                "last_ns": 1661259808003986641,
                "hull_s": 59.878772778
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/13_04_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 23896,
                "seconds_with_rows": 62,
                "first_ns": 1661259807382520338,
                "last_ns": 1661259869408032260,
                "hull_s": 62.025511922
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 23896,
                "seconds_with_rows": 62,
                "first_ns": 1661259807482124800,
                "last_ns": 1661259869413061076,
                "hull_s": 61.930936276
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 16158,
            "seconds_with_rows": 42,
            "first_ns": 1661259687526987593,
            "last_ns": 1661259728728233728,
            "hull_s": 41.201246135
          },
          "A": {
            "rows": 54565,
            "seconds_with_rows": 140,
            "first_ns": 1661259729058907279,
            "last_ns": 1661259869408032260,
            "hull_s": 140.349124981
          }
        },
        "end_split": {
          "N": {
            "rows": 16158,
            "seconds_with_rows": 42,
            "first_ns": 1661259687588714496,
            "last_ns": 1661259728730374674,
            "hull_s": 41.141660178
          },
          "A": {
            "rows": 54565,
            "seconds_with_rows": 140,
            "first_ns": 1661259729063254528,
            "last_ns": 1661259869413061076,
            "hull_s": 140.349806548
          }
        },
        "straddle_t": 0,
        "duplicate_keys": 90,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/log/13_02_log.csv",
            "N": {
              "rows": 17413,
              "seconds_with_rows": 42,
              "first_ns": 1661259687527020006,
              "last_ns": 1661259728730348003,
              "hull_s": 41.203327997
            },
            "A": {
              "rows": 7711,
              "seconds_with_rows": 19,
              "first_ns": 1661259729058957073,
              "last_ns": 1661259747800601067,
              "hull_s": 18.741643994
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/13_03_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 25068,
              "seconds_with_rows": 61,
              "first_ns": 1661259748124988955,
              "last_ns": 1661259808003952905,
              "hull_s": 59.87896395
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/13_04_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 25428,
              "seconds_with_rows": 62,
              "first_ns": 1661259807382562257,
              "last_ns": 1661259869413033704,
              "hull_s": 62.030471447
            }
          }
        ],
        "N": {
          "rows": 17413,
          "seconds_with_rows": 42,
          "first_ns": 1661259687527020006,
          "last_ns": 1661259728730348003,
          "hull_s": 41.203327997
        },
        "A": {
          "rows": 58207,
          "seconds_with_rows": 140,
          "first_ns": 1661259729058957073,
          "last_ns": 1661259869413033704,
          "hull_s": 140.354076631
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 75620,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.55e-06,
            1.949387061
          ],
          "relative_end_s": [
            -1.949361459,
            0.010455442
          ]
        }
      },
      "previous_inject_time_ns": 1661259232000000000,
      "previous_gap_s": 497.0,
      "next_gap_s": 507.0,
      "elapsed_s": 1.4059999999990396
    },
    {
      "case": "OB|checkoutservice|network_delay|2022-08-22 04:52:55",
      "view": "main",
      "t_ns": 1661143975000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661143699618578986,
            "last_ns": 1661143939860718132,
            "hull_s": 240.242139146
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661143999688235803,
            "last_ns": 1661144239645758921,
            "hull_s": 239.957523118
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.028270967,
            60.035513333,
            60.187476915,
            59.990877931,
            59.827517671,
            60.181489507,
            59.958914713,
            59.85708515,
            59.960033748
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661143699654636186,
            "last_ns": 1661143939721442243,
            "hull_s": 240.066806057
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661143999758146089,
            "last_ns": 1661144239678853809,
            "hull_s": 239.92070772
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.036247671,
            60.061469854,
            59.985765233,
            59.983323299,
            60.036703846,
            59.949888086,
            60.202142282,
            59.854536378,
            59.914140974
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661143699712439467,
            "last_ns": 1661143939825828344,
            "hull_s": 240.113388877
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661143999831258279,
            "last_ns": 1661144239738798894,
            "hull_s": 239.907540615
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.062955258,
            60.061935327,
            59.986060039,
            60.002438253,
            60.005429935,
            59.93062559,
            60.246077575,
            59.954981979,
            59.775855471
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661143699745772957,
            "last_ns": 1661143939897207204,
            "hull_s": 240.151434247
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661143999871928293,
            "last_ns": 1661144239778241737,
            "hull_s": 239.906313444
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.086664358,
            60.061777954,
            59.99517103,
            60.007820905,
            59.974721089,
            59.923770171,
            60.264248637,
            60.017476428,
            59.700818208
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661143699771202084,
            "last_ns": 1661143939932089465,
            "hull_s": 240.160887381
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661143999909509570,
            "last_ns": 1661144239826118093,
            "hull_s": 239.916608523
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.230776141,
            59.922806163,
            60.010027333,
            59.997277744,
            59.977420105,
            59.912428028,
            60.275776343,
            60.025529517,
            59.702874635
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661143699581149241,
            "last_ns": 1661143939609973137,
            "hull_s": 240.028823896
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661143999621045377,
            "last_ns": 1661144239613508395,
            "hull_s": 239.992463018
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.014164054,
            60.02211473,
            59.994468518,
            59.998076594,
            60.01107224,
            59.998574367,
            59.996010473,
            60.0028354,
            59.995042778
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661143699809498239,
            "last_ns": 1661143939975796857,
            "hull_s": 240.166298618
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661143999959944196,
            "last_ns": 1661144239877490378,
            "hull_s": 239.917546182
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.350204612,
            59.806411147,
            60.024210794,
            59.985472065,
            59.984147339,
            59.898736314,
            60.291084995,
            60.034687868,
            59.693037005
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661143699839404000,
            "last_ns": 1661143940007236504,
            "hull_s": 240.167832504
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661143999995129067,
            "last_ns": 1661144239911473800,
            "hull_s": 239.916344733
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.3669813,
            59.789620895,
            60.029150156,
            59.982080153,
            59.987892563,
            59.890807106,
            60.304025474,
            60.053302841,
            59.668209312
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/productcatalogservice-668d5f85fb-wckp8_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661143699875694454,
            "last_ns": 1661143940043055591,
            "hull_s": 240.167361137
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144000064958050,
            "last_ns": 1661144239966450153,
            "hull_s": 239.901492103
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.380661947,
            59.775277374,
            60.030954946,
            59.98046687,
            60.021902459,
            59.850416681,
            60.312694806,
            60.054035464,
            59.684345152
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661143699911379219,
            "last_ns": 1661143940073821115,
            "hull_s": 240.162441896
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144000127719973,
            "last_ns": 1661144240141829857,
            "hull_s": 240.014109884
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.395566593,
            59.75254928,
            60.06339346,
            59.950932563,
            60.053898858,
            59.814499148,
            60.319387685,
            60.052896658,
            59.827326393
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661143699953506711,
            "last_ns": 1661143940109804628,
            "hull_s": 240.156297917
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144000192767845,
            "last_ns": 1661144240219877828,
            "hull_s": 240.027109983
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.400928793,
            59.737597817,
            60.090897438,
            59.926873869,
            60.082963217,
            59.776702729,
            60.339860818,
            60.046693145,
            59.863853291
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/04_52_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 24380,
                "seconds_with_rows": 61,
                "first_ns": 1661143879175620677,
                "last_ns": 1661143939688024832,
                "hull_s": 60.512404155
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "end_split": {
              "N": {
                "rows": 24380,
                "seconds_with_rows": 61,
                "first_ns": 1661143879179800832,
                "last_ns": 1661143939692088990,
                "hull_s": 60.512288158
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/04_53_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 14595,
                "seconds_with_rows": 36,
                "first_ns": 1661143939452881258,
                "last_ns": 1661143974999080192,
                "hull_s": 35.546198934
              },
              "A": {
                "rows": 10273,
                "seconds_with_rows": 25,
                "first_ns": 1661143975000551134,
                "last_ns": 1661143999236398122,
                "hull_s": 24.235846988
              }
            },
            "end_split": {
              "N": {
                "rows": 14586,
                "seconds_with_rows": 36,
                "first_ns": 1661143939456728593,
                "last_ns": 1661143974999784704,
                "hull_s": 35.543056111
              },
              "A": {
                "rows": 10282,
                "seconds_with_rows": 25,
                "first_ns": 1661143975000504856,
                "last_ns": 1661143999241759926,
                "hull_s": 24.24125507
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/04_54_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 24697,
                "seconds_with_rows": 62,
                "first_ns": 1661143999296474143,
                "last_ns": 1661144060112401161,
                "hull_s": 60.815927018
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 24697,
                "seconds_with_rows": 62,
                "first_ns": 1661143999301179136,
                "last_ns": 1661144060116867728,
                "hull_s": 60.815688592
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 38975,
            "seconds_with_rows": 96,
            "first_ns": 1661143879175620677,
            "last_ns": 1661143974999080192,
            "hull_s": 95.823459515
          },
          "A": {
            "rows": 34970,
            "seconds_with_rows": 86,
            "first_ns": 1661143975000551134,
            "last_ns": 1661144060112401161,
            "hull_s": 85.111850027
          }
        },
        "end_split": {
          "N": {
            "rows": 38966,
            "seconds_with_rows": 96,
            "first_ns": 1661143879179800832,
            "last_ns": 1661143974999784704,
            "hull_s": 95.819983872
          },
          "A": {
            "rows": 34979,
            "seconds_with_rows": 86,
            "first_ns": 1661143975000504856,
            "last_ns": 1661144060116867728,
            "hull_s": 85.116362872
          }
        },
        "straddle_t": 9,
        "duplicate_keys": 172,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-22/log/04_52_log.csv",
            "N": {
              "rows": 26318,
              "seconds_with_rows": 61,
              "first_ns": 1661143879175657447,
              "last_ns": 1661143939692063766,
              "hull_s": 60.516406319
            },
            "A": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/log/04_53_log.csv",
            "N": {
              "rows": 15547,
              "seconds_with_rows": 36,
              "first_ns": 1661143939452912444,
              "last_ns": 1661143974999396538,
              "hull_s": 35.546484094
            },
            "A": {
              "rows": 10850,
              "seconds_with_rows": 25,
              "first_ns": 1661143975000517170,
              "last_ns": 1661143999241723168,
              "hull_s": 24.241205998
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/log/04_54_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 26616,
              "seconds_with_rows": 62,
              "first_ns": 1661143999296502865,
              "last_ns": 1661144060116769001,
              "hull_s": 60.820266136
            }
          }
        ],
        "N": {
          "rows": 41865,
          "seconds_with_rows": 96,
          "first_ns": 1661143879175657447,
          "last_ns": 1661143974999396538,
          "hull_s": 95.823739091
        },
        "A": {
          "rows": 37466,
          "seconds_with_rows": 86,
          "first_ns": 1661143975000517170,
          "last_ns": 1661144060116769001,
          "hull_s": 85.116251831
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 79331,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.573e-06,
            2.032038906
          ],
          "relative_end_s": [
            -2.032040136,
            0.018268677
          ]
        }
      },
      "previous_inject_time_ns": 1661143456000000000,
      "previous_gap_s": 519.0,
      "next_gap_s": 498.0,
      "elapsed_s": 1.5780000000013388
    },
    {
      "case": "OB|checkoutservice|network_delay|2022-08-23 12:53:52",
      "view": "main",
      "t_ns": 1661259232000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661258968170650805,
            "last_ns": 1661259208200466539,
            "hull_s": 240.029815734
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259268188693802,
            "last_ns": 1661259508150141801,
            "hull_s": 239.961447999
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.990300604,
            60.026687961,
            59.9619026,
            60.050924569,
            59.988227263,
            59.96089168,
            60.01939122,
            60.00199995,
            59.979165149
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661258968209473775,
            "last_ns": 1661259208250563351,
            "hull_s": 240.041089576
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259268258084162,
            "last_ns": 1661259508184446735,
            "hull_s": 239.926362573
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.988489654,
            60.056911851,
            59.929329114,
            60.066358957,
            60.007520811,
            59.939149049,
            60.009616374,
            59.998484237,
            59.979112913
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661258968268959546,
            "last_ns": 1661259208324046884,
            "hull_s": 240.055087338
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259268355543513,
            "last_ns": 1661259508250731178,
            "hull_s": 239.895187665
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.998614099,
            60.060319532,
            59.91462095,
            60.081532757,
            60.031496629,
            59.910283564,
            60.013551775,
            59.988528699,
            59.982823627
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661258968318877741,
            "last_ns": 1661259208363233134,
            "hull_s": 240.044355393
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259268399993122,
            "last_ns": 1661259508286325886,
            "hull_s": 239.886332764
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.001396207,
            60.049298286,
            59.907174778,
            60.086486122,
            60.036759988,
            59.915103474,
            60.006435568,
            59.980576769,
            59.984216953
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661258968350653041,
            "last_ns": 1661259208389548282,
            "hull_s": 240.038895241
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259268432937354,
            "last_ns": 1661259508313630919,
            "hull_s": 239.880693565
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.004557535,
            60.052647423,
            59.897893082,
            60.083797201,
            60.043389072,
            59.939857292,
            59.98323312,
            59.974458418,
            59.983144735
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661258968117450549,
            "last_ns": 1661259208125108772,
            "hull_s": 240.007658223
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259268123608963,
            "last_ns": 1661259508117969465,
            "hull_s": 239.994360502
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.000118184,
            60.006683663,
            59.992084059,
            60.008772317,
            59.998500191,
            59.981056031,
            60.020603769,
            59.999150391,
            59.993550311
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661258968410200381,
            "last_ns": 1661259208455705661,
            "hull_s": 240.04550528
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259268495215523,
            "last_ns": 1661259508365503373,
            "hull_s": 239.87028785
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.001345015,
            60.048294604,
            59.897940668,
            60.097924993,
            60.039509862,
            59.962810501,
            59.96139077,
            59.966254503,
            59.979832076
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661258968462779182,
            "last_ns": 1661259208487725109,
            "hull_s": 240.024945927
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259268535248145,
            "last_ns": 1661259508397664325,
            "hull_s": 239.86241618
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.978374805,
            60.05100134,
            59.895537917,
            60.100031865,
            60.047523036,
            59.976916132,
            59.948826327,
            59.979438742,
            59.957234979
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/productcatalogservice-668d5f85fb-jhwx9_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661258968510382447,
            "last_ns": 1661259208543426970,
            "hull_s": 240.033044523
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259268579991919,
            "last_ns": 1661259508429720932,
            "hull_s": 239.849729013
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.959196953,
            60.059375433,
            59.900132759,
            60.114339378,
            60.036564949,
            59.967780676,
            59.951924151,
            59.998557686,
            59.9314665
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661258968561334265,
            "last_ns": 1661259208583831330,
            "hull_s": 240.022497065
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259268666805941,
            "last_ns": 1661259508465219425,
            "hull_s": 239.798413484
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.937923089,
            60.091855964,
            59.897630446,
            60.095087566,
            60.082974611,
            59.915482977,
            59.945792225,
            60.010263404,
            59.926874878
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661258968596437658,
            "last_ns": 1661259208634479362,
            "hull_s": 240.038041704
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259268817745825,
            "last_ns": 1661259508501715779,
            "hull_s": 239.683969954
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.949076601,
            60.095353318,
            59.904686652,
            60.088925133,
            60.183266463,
            59.81028396,
            59.931177495,
            60.033406954,
            59.909101545
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/12_53_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 22775,
                "seconds_with_rows": 61,
                "first_ns": 1661259147774974729,
                "last_ns": 1661259207830612375,
                "hull_s": 60.055637646
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "end_split": {
              "N": {
                "rows": 22775,
                "seconds_with_rows": 61,
                "first_ns": 1661259147777921062,
                "last_ns": 1661259207835954062,
                "hull_s": 60.058033
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/12_54_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 8986,
                "seconds_with_rows": 24,
                "first_ns": 1661259208053050616,
                "last_ns": 1661259231999926016,
                "hull_s": 23.9468754
              },
              "A": {
                "rows": 14562,
                "seconds_with_rows": 36,
                "first_ns": 1661259232001725011,
                "last_ns": 1661259267953170713,
                "hull_s": 35.951445702
              }
            },
            "end_split": {
              "N": {
                "rows": 8974,
                "seconds_with_rows": 24,
                "first_ns": 1661259208060939735,
                "last_ns": 1661259231999967232,
                "hull_s": 23.939027497
              },
              "A": {
                "rows": 14574,
                "seconds_with_rows": 36,
                "first_ns": 1661259232000116603,
                "last_ns": 1661259267956000345,
                "hull_s": 35.955883742
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/12_55_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 23080,
                "seconds_with_rows": 61,
                "first_ns": 1661259268292730554,
                "last_ns": 1661259328107589813,
                "hull_s": 59.814859259
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 23080,
                "seconds_with_rows": 61,
                "first_ns": 1661259268293002870,
                "last_ns": 1661259328110865174,
                "hull_s": 59.817862304
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 31761,
            "seconds_with_rows": 85,
            "first_ns": 1661259147774974729,
            "last_ns": 1661259231999926016,
            "hull_s": 84.224951287
          },
          "A": {
            "rows": 37642,
            "seconds_with_rows": 97,
            "first_ns": 1661259232001725011,
            "last_ns": 1661259328107589813,
            "hull_s": 96.105864802
          }
        },
        "end_split": {
          "N": {
            "rows": 31749,
            "seconds_with_rows": 85,
            "first_ns": 1661259147777921062,
            "last_ns": 1661259231999967232,
            "hull_s": 84.22204617
          },
          "A": {
            "rows": 37654,
            "seconds_with_rows": 97,
            "first_ns": 1661259232000116603,
            "last_ns": 1661259328110865174,
            "hull_s": 96.110748571
          }
        },
        "straddle_t": 12,
        "duplicate_keys": 0,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/log/12_53_log.csv",
            "N": {
              "rows": 24378,
              "seconds_with_rows": 61,
              "first_ns": 1661259147775009922,
              "last_ns": 1661259207835926551,
              "hull_s": 60.060916629
            },
            "A": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/12_54_log.csv",
            "N": {
              "rows": 9706,
              "seconds_with_rows": 24,
              "first_ns": 1661259208053103534,
              "last_ns": 1661259231999997660,
              "hull_s": 23.946894126
            },
            "A": {
              "rows": 15624,
              "seconds_with_rows": 36,
              "first_ns": 1661259232000023161,
              "last_ns": 1661259267955970990,
              "hull_s": 35.955947829
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/12_55_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 24700,
              "seconds_with_rows": 61,
              "first_ns": 1661259268292785226,
              "last_ns": 1661259328110843756,
              "hull_s": 59.81805853
            }
          }
        ],
        "N": {
          "rows": 34084,
          "seconds_with_rows": 85,
          "first_ns": 1661259147775009922,
          "last_ns": 1661259231999997660,
          "hull_s": 84.224987738
        },
        "A": {
          "rows": 40324,
          "seconds_with_rows": 97,
          "first_ns": 1661259232000023161,
          "last_ns": 1661259328110843756,
          "hull_s": 96.110820595
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 74408,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.633e-06,
            1.3429733
          ],
          "relative_end_s": [
            -1.342975224,
            0.019484404
          ]
        }
      },
      "previous_inject_time_ns": 1661258708000000000,
      "previous_gap_s": 524.0,
      "next_gap_s": 497.0,
      "elapsed_s": 1.375
    },
    {
      "case": "OB|checkoutservice|return|2022-08-22 05:09:50",
      "view": "main",
      "t_ns": 1661144990000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144719684308197,
            "last_ns": 1661144959886273269,
            "hull_s": 240.201965072
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661145019642225688,
            "last_ns": 1661145259864029382,
            "hull_s": 240.221803694
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.126124249,
            59.833255477,
            60.002177023,
            60.240408323,
            59.755952419,
            60.225956572,
            59.995212639,
            60.000698705,
            59.999935778
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144719750138756,
            "last_ns": 1661144959730712368,
            "hull_s": 239.980573612
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661145019685034123,
            "last_ns": 1661145259686510322,
            "hull_s": 240.001476199
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.97539179,
            59.967554047,
            60.002593582,
            60.035034193,
            59.954321755,
            60.051937063,
            59.993604495,
            59.972068277,
            59.983866364
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144719825970969,
            "last_ns": 1661144959799744843,
            "hull_s": 239.973773874
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661145019766399173,
            "last_ns": 1661145259741495893,
            "hull_s": 239.97509672
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.969665554,
            60.01426925,
            59.976963056,
            60.012876014,
            59.96665433,
            60.041206794,
            60.00618709,
            59.951341633,
            59.976361203
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144719869600113,
            "last_ns": 1661144959832348940,
            "hull_s": 239.962748827
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661145019809782128,
            "last_ns": 1661145259774373684,
            "hull_s": 239.964591556
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.976270581,
            60.123647877,
            59.884711782,
            59.978118587,
            59.977433188,
            60.031735612,
            60.025137519,
            59.934927179,
            59.972791246
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144719901054665,
            "last_ns": 1661144959855911843,
            "hull_s": 239.954857178
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661145019836067790,
            "last_ns": 1661145259800746671,
            "hull_s": 239.964678881
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.974321264,
            60.126669677,
            59.961177992,
            59.892688245,
            59.980155947,
            60.042080225,
            60.036228676,
            59.914922857,
            59.971447123
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144719618007794,
            "last_ns": 1661144959609977697,
            "hull_s": 239.991969903
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661145019601716345,
            "last_ns": 1661145259615499446,
            "hull_s": 240.013783101
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.994553204,
            59.992270374,
            59.999392758,
            60.005753567,
            59.991738648,
            60.00779349,
            59.997057338,
            60.026908691,
            59.982023582
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144719945257450,
            "last_ns": 1661144959895414270,
            "hull_s": 239.95015682
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661145019872530360,
            "last_ns": 1661145259840695544,
            "hull_s": 239.968165184
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.996512228,
            60.112939491,
            60.096663637,
            59.744041464,
            59.97711609,
            60.045369968,
            60.06246202,
            59.890044338,
            59.970288858
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144719979266229,
            "last_ns": 1661144959928901315,
            "hull_s": 239.949635086
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661145019904252784,
            "last_ns": 1661145259865603919,
            "hull_s": 239.961351135
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.011235813,
            60.126192926,
            60.236642898,
            59.575563449,
            59.975351469,
            60.04133678,
            60.080160143,
            59.876819807,
            59.963034405
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/productcatalogservice-668d5f85fb-wckp8_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144720012998074,
            "last_ns": 1661144959970569803,
            "hull_s": 239.957571729
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661145019944101955,
            "last_ns": 1661145259899449245,
            "hull_s": 239.95534729
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.019553879,
            60.138835878,
            60.257699344,
            59.541482628,
            59.973532152,
            60.039206327,
            60.104677212,
            59.86056916,
            59.950894591
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144720045519304,
            "last_ns": 1661144960114630242,
            "hull_s": 240.069110938
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661145019988569467,
            "last_ns": 1661145259926265161,
            "hull_s": 239.937695694
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.02493877,
            60.144512197,
            60.248374672,
            59.651285299,
            59.873939225,
            60.024269567,
            60.140464452,
            59.835779529,
            59.937182146
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661144720082048435,
            "last_ns": 1661144960200732994,
            "hull_s": 240.118684559
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661145020043220938,
            "last_ns": 1661145259966301619,
            "hull_s": 239.923080681
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.019994856,
            60.149486514,
            60.24750724,
            59.701695949,
            59.842487944,
            60.004166889,
            60.15460847,
            59.822791183,
            59.941514139
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/05_09_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 24112,
                "seconds_with_rows": 61,
                "first_ns": 1661144899490657905,
                "last_ns": 1661144959480039168,
                "hull_s": 59.989381263
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "end_split": {
              "N": {
                "rows": 24112,
                "seconds_with_rows": 61,
                "first_ns": 1661144899494633216,
                "last_ns": 1661144959482320832,
                "hull_s": 59.987687616
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/05_10_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 12264,
                "seconds_with_rows": 31,
                "first_ns": 1661144959256635852,
                "last_ns": 1661144989999779847,
                "hull_s": 30.743143995
              },
              "A": {
                "rows": 11064,
                "seconds_with_rows": 30,
                "first_ns": 1661144990000290326,
                "last_ns": 1661145019385378104,
                "hull_s": 29.385087778
              }
            },
            "end_split": {
              "N": {
                "rows": 12250,
                "seconds_with_rows": 31,
                "first_ns": 1661144959260082176,
                "last_ns": 1661144989999744368,
                "hull_s": 30.739662192
              },
              "A": {
                "rows": 11078,
                "seconds_with_rows": 30,
                "first_ns": 1661144990000195505,
                "last_ns": 1661145019390084190,
                "hull_s": 29.389888685
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/05_11_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 23839,
                "seconds_with_rows": 61,
                "first_ns": 1661145019255880694,
                "last_ns": 1661145079691611136,
                "hull_s": 60.435730442
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 23839,
                "seconds_with_rows": 61,
                "first_ns": 1661145019267563529,
                "last_ns": 1661145079696374223,
                "hull_s": 60.428810694
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 36376,
            "seconds_with_rows": 91,
            "first_ns": 1661144899490657905,
            "last_ns": 1661144989999779847,
            "hull_s": 90.509121942
          },
          "A": {
            "rows": 34903,
            "seconds_with_rows": 90,
            "first_ns": 1661144990000290326,
            "last_ns": 1661145079691611136,
            "hull_s": 89.69132081
          }
        },
        "end_split": {
          "N": {
            "rows": 36362,
            "seconds_with_rows": 91,
            "first_ns": 1661144899494633216,
            "last_ns": 1661144989999744368,
            "hull_s": 90.505111152
          },
          "A": {
            "rows": 34917,
            "seconds_with_rows": 90,
            "first_ns": 1661144990000195505,
            "last_ns": 1661145079696374223,
            "hull_s": 89.696178718
          }
        },
        "straddle_t": 14,
        "duplicate_keys": 164,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-22/log/05_09_log.csv",
            "N": {
              "rows": 25692,
              "seconds_with_rows": 61,
              "first_ns": 1661144899490722888,
              "last_ns": 1661144959482272924,
              "hull_s": 59.991550036
            },
            "A": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/log/05_10_log.csv",
            "N": {
              "rows": 13269,
              "seconds_with_rows": 31,
              "first_ns": 1661144959256664390,
              "last_ns": 1661144989998745492,
              "hull_s": 30.742081102
            },
            "A": {
              "rows": 11992,
              "seconds_with_rows": 30,
              "first_ns": 1661144990000024836,
              "last_ns": 1661145019390058151,
              "hull_s": 29.390033315
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/log/05_11_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 25400,
              "seconds_with_rows": 61,
              "first_ns": 1661145019255924643,
              "last_ns": 1661145079696320582,
              "hull_s": 60.440395939
            }
          }
        ],
        "N": {
          "rows": 38961,
          "seconds_with_rows": 91,
          "first_ns": 1661144899490722888,
          "last_ns": 1661144989998745492,
          "hull_s": 90.508022604
        },
        "A": {
          "rows": 37392,
          "seconds_with_rows": 90,
          "first_ns": 1661144990000024836,
          "last_ns": 1661145079696320582,
          "hull_s": 89.696295746
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 76353,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.638e-06,
            2.125775791
          ],
          "relative_end_s": [
            -2.125787265,
            0.012211136
          ]
        }
      },
      "previous_inject_time_ns": 1661144473000000000,
      "previous_gap_s": 517.0,
      "next_gap_s": 499.0,
      "elapsed_s": 1.4530000000013388
    },
    {
      "case": "OB|checkoutservice|return|2022-08-23 13:10:36",
      "view": "main",
      "t_ns": 1661260236000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259988189050835,
            "last_ns": 1661260228215702000,
            "hull_s": 240.026651165
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661260288182750528,
            "last_ns": 1661260528186287759,
            "hull_s": 240.003537231
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.957183143,
            60.163746846,
            59.896288629,
            60.009432547,
            59.967048528,
            59.979820341,
            60.132694685,
            59.86784677,
            60.023175435
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259988256862230,
            "last_ns": 1661260228274239868,
            "hull_s": 240.017377638
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661260288226839553,
            "last_ns": 1661260528252282773,
            "hull_s": 240.02544322
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.951507355,
            60.161547686,
            59.899300747,
            60.00502185,
            59.952599685,
            59.986210364,
            60.20387722,
            59.802231198,
            60.033124438
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259988344042121,
            "last_ns": 1661260228332502687,
            "hull_s": 239.988460566
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661260288290521335,
            "last_ns": 1661260528331796864,
            "hull_s": 240.041275529
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.940913057,
            60.163472061,
            59.910988379,
            59.973087069,
            59.958018648,
            60.014880926,
            60.19799695,
            59.942052932,
            59.886344721
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259988411593442,
            "last_ns": 1661260228364873448,
            "hull_s": 239.953280006
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661260288343217325,
            "last_ns": 1661260528368248004,
            "hull_s": 240.025030679
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.929577818,
            60.167036866,
            59.90769506,
            59.948970262,
            59.978343877,
            60.033000765,
            60.169627815,
            59.944433707,
            59.877968392
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259988474525285,
            "last_ns": 1661260228395229020,
            "hull_s": 239.920703735
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661260288378992761,
            "last_ns": 1661260528400676301,
            "hull_s": 240.02168354
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.893128463,
            60.169925233,
            59.912543735,
            59.945106304,
            59.983763741,
            60.061287836,
            60.13899866,
            59.939333871,
            59.882063173
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259988131366987,
            "last_ns": 1661260228145249142,
            "hull_s": 240.013882155
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661260288130596689,
            "last_ns": 1661260528127350773,
            "hull_s": 239.996754084
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.981141381,
            60.003880794,
            60.020945328,
            60.007914652,
            59.985347547,
            59.998226515,
            60.00774574,
            59.994549559,
            59.99623227
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259988562602121,
            "last_ns": 1661260228452345352,
            "hull_s": 239.889743231
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661260288444672921,
            "last_ns": 1661260528478346138,
            "hull_s": 240.033673217
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.854843995,
            60.168698947,
            59.923557697,
            59.942642592,
            59.992327569,
            60.080245293,
            60.109811395,
            59.929564777,
            59.914051752
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259988635042432,
            "last_ns": 1661260228482474239,
            "hull_s": 239.847431807
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661260288483105020,
            "last_ns": 1661260528655052403,
            "hull_s": 240.171947383
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.812974558,
            60.165928476,
            59.933522196,
            59.935006577,
            60.000630781,
            60.112616933,
            60.081886598,
            59.912961993,
            60.064481859
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/productcatalogservice-668d5f85fb-jhwx9_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259988798478288,
            "last_ns": 1661260228515870725,
            "hull_s": 239.717392437
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661260288534481685,
            "last_ns": 1661260528715653612,
            "hull_s": 240.181171927
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.713222577,
            60.153239082,
            59.921718841,
            59.929211937,
            60.01861096,
            60.12460296,
            60.065688053,
            59.892381086,
            60.098499828
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259988845272848,
            "last_ns": 1661260228551789370,
            "hull_s": 239.706516522
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661260288587004575,
            "last_ns": 1661260528778272573,
            "hull_s": 240.191267998
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.824009442,
            60.035081674,
            59.928650563,
            59.918774843,
            60.035215205,
            60.113893146,
            60.080705399,
            59.861857953,
            60.1348115
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661259988911174628,
            "last_ns": 1661260228594577097,
            "hull_s": 239.683402469
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661260288648690087,
            "last_ns": 1661260528813974138,
            "hull_s": 240.165284051
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.81183703,
            60.0235809,
            59.941103358,
            59.906881181,
            60.05411299,
            60.10223991,
            60.062902576,
            59.855040676,
            60.145100889
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/13_10_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 23436,
                "seconds_with_rows": 62,
                "first_ns": 1661260167415572763,
                "last_ns": 1661260228083144140,
                "hull_s": 60.667571377
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "end_split": {
              "N": {
                "rows": 23436,
                "seconds_with_rows": 62,
                "first_ns": 1661260167491729664,
                "last_ns": 1661260228087648095,
                "hull_s": 60.595918431
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/13_11_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 2897,
                "seconds_with_rows": 9,
                "first_ns": 1661260227292865381,
                "last_ns": 1661260235998846720,
                "hull_s": 8.705981339
              },
              "A": {
                "rows": 19945,
                "seconds_with_rows": 52,
                "first_ns": 1661260236001432748,
                "last_ns": 1661260287674881844,
                "hull_s": 51.673449096
              }
            },
            "end_split": {
              "N": {
                "rows": 2893,
                "seconds_with_rows": 9,
                "first_ns": 1661260227385588224,
                "last_ns": 1661260235999439616,
                "hull_s": 8.613851392
              },
              "A": {
                "rows": 19949,
                "seconds_with_rows": 52,
                "first_ns": 1661260236003952717,
                "last_ns": 1661260287676508760,
                "hull_s": 51.672556043
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/13_12_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 24055,
                "seconds_with_rows": 62,
                "first_ns": 1661260287933747567,
                "last_ns": 1661260348294963968,
                "hull_s": 60.361216401
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 24055,
                "seconds_with_rows": 62,
                "first_ns": 1661260287936592128,
                "last_ns": 1661260348388856041,
                "hull_s": 60.452263913
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 26333,
            "seconds_with_rows": 69,
            "first_ns": 1661260167415572763,
            "last_ns": 1661260235998846720,
            "hull_s": 68.583273957
          },
          "A": {
            "rows": 44000,
            "seconds_with_rows": 113,
            "first_ns": 1661260236001432748,
            "last_ns": 1661260348294963968,
            "hull_s": 112.29353122
          }
        },
        "end_split": {
          "N": {
            "rows": 26329,
            "seconds_with_rows": 69,
            "first_ns": 1661260167491729664,
            "last_ns": 1661260235999439616,
            "hull_s": 68.507709952
          },
          "A": {
            "rows": 44004,
            "seconds_with_rows": 113,
            "first_ns": 1661260236003952717,
            "last_ns": 1661260348388856041,
            "hull_s": 112.384903324
          }
        },
        "straddle_t": 4,
        "duplicate_keys": 62,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/log/13_10_log.csv",
            "N": {
              "rows": 25228,
              "seconds_with_rows": 62,
              "first_ns": 1661260167415608178,
              "last_ns": 1661260228087580204,
              "hull_s": 60.671972026
            },
            "A": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/13_11_log.csv",
            "N": {
              "rows": 3086,
              "seconds_with_rows": 9,
              "first_ns": 1661260227292895592,
              "last_ns": 1661260235999558403,
              "hull_s": 8.706662811
            },
            "A": {
              "rows": 21462,
              "seconds_with_rows": 52,
              "first_ns": 1661260236001447191,
              "last_ns": 1661260287676475741,
              "hull_s": 51.67502855
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/13_12_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 25605,
              "seconds_with_rows": 62,
              "first_ns": 1661260287933804442,
              "last_ns": 1661260348388827567,
              "hull_s": 60.455023125
            }
          }
        ],
        "N": {
          "rows": 28314,
          "seconds_with_rows": 69,
          "first_ns": 1661260167415608178,
          "last_ns": 1661260235999558403,
          "hull_s": 68.583950225
        },
        "A": {
          "rows": 47067,
          "seconds_with_rows": 113,
          "first_ns": 1661260236001447191,
          "last_ns": 1661260348388827567,
          "hull_s": 112.387380376
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 75381,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.597e-06,
            1.55355633
          ],
          "relative_end_s": [
            -1.553553827,
            0.00944251
          ]
        }
      },
      "previous_inject_time_ns": 1661259729000000000,
      "previous_gap_s": 507.0,
      "next_gap_s": 510.0,
      "elapsed_s": 1.4219999999986612
    },
    {
      "case": "OB|emailservice|cpu_consumed|2022-08-23 14:03:48",
      "view": "main",
      "t_ns": 1661263428000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263168216369118,
            "last_ns": 1661263408208737798,
            "hull_s": 239.99236868
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263468219459206,
            "last_ns": 1661263708219084173,
            "hull_s": 239.999624967
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.975262924,
            60.045705349,
            59.957969453,
            60.013430954,
            60.010721408,
            60.013646928,
            60.016284977,
            59.989028373,
            59.980664689
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263168264426411,
            "last_ns": 1661263408267210065,
            "hull_s": 240.002783654
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263468261343985,
            "last_ns": 1661263708282441277,
            "hull_s": 240.021097292
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.959206402,
            60.084373013,
            59.945373057,
            60.013831182,
            59.99413392,
            60.032547483,
            60.086536599,
            59.927625853,
            59.974387357
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263168338135680,
            "last_ns": 1661263408352146210,
            "hull_s": 240.01401053
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263468337161456,
            "last_ns": 1661263708360594300,
            "hull_s": 240.023432844
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.953517193,
            60.098953344,
            59.948932576,
            60.012607417,
            59.985015246,
            60.023005387,
            60.132078273,
            59.937700285,
            59.930648899
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263168378946025,
            "last_ns": 1661263408413985645,
            "hull_s": 240.03503962
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263468414749165,
            "last_ns": 1661263708412141116,
            "hull_s": 239.997391951
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.95306492,
            60.097353458,
            59.97577328,
            60.008847962,
            60.00076352,
            59.979170953,
            60.131842592,
            60.038466004,
            59.847912402
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263168415594753,
            "last_ns": 1661263408450376683,
            "hull_s": 240.03478193
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263468484378472,
            "last_ns": 1661263708452082070,
            "hull_s": 239.967703598
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.946093295,
            60.101860572,
            60.001386485,
            59.985441578,
            60.034001789,
            59.936426286,
            60.137602609,
            60.049588842,
            59.844085861
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263168166768149,
            "last_ns": 1661263408158769123,
            "hull_s": 239.992000974
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263468164526532,
            "last_ns": 1661263708170996641,
            "hull_s": 240.006470109
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.988083767,
            60.011919537,
            59.991400298,
            60.000597372,
            60.005757409,
            60.006921136,
            60.00230647,
            59.994833075,
            60.002409428
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263168472521661,
            "last_ns": 1661263408501206734,
            "hull_s": 240.028685073
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263468600036482,
            "last_ns": 1661263708555723678,
            "hull_s": 239.955687196
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.949686882,
            60.104629536,
            60.023877347,
            59.950491308,
            60.098829748,
            59.869690543,
            60.150740451,
            60.045036474,
            59.890219728
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263168508193479,
            "last_ns": 1661263408532826876,
            "hull_s": 240.024633397
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263468679368037,
            "last_ns": 1661263708704953747,
            "hull_s": 240.02558571
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.972909964,
            60.093904462,
            60.040043694,
            59.917775277,
            60.146541161,
            59.817646732,
            60.180925302,
            60.023962325,
            60.003051351
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/productcatalogservice-668d5f85fb-jhwx9_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263168543342236,
            "last_ns": 1661263408561334012,
            "hull_s": 240.017991776
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263468755890622,
            "last_ns": 1661263708773121088,
            "hull_s": 240.017230466
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.001321264,
            60.069210046,
            60.044963258,
            59.902497208,
            60.19455661,
            59.770104713,
            60.20142191,
            60.019781008,
            60.025922835
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263168584375298,
            "last_ns": 1661263408589776941,
            "hull_s": 240.005401643
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263468799896474,
            "last_ns": 1661263708837333684,
            "hull_s": 240.03743721
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.019546503,
            60.056250315,
            60.033906357,
            59.895698468,
            60.210119533,
            59.757308815,
            60.226425682,
            60.024468955,
            60.029233758
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263168631853296,
            "last_ns": 1661263408616316995,
            "hull_s": 239.984463699
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661263468844212722,
            "last_ns": 1661263708905121646,
            "hull_s": 240.060908924
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.033241572,
            60.039538671,
            60.031697229,
            59.879986227,
            60.227895727,
            59.742306067,
            60.260752118,
            60.012648366,
            60.045202373
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/14_03_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 23839,
                "seconds_with_rows": 61,
                "first_ns": 1661263347242042098,
                "last_ns": 1661263407679288684,
                "hull_s": 60.437246586
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "end_split": {
              "N": {
                "rows": 23839,
                "seconds_with_rows": 61,
                "first_ns": 1661263347483894784,
                "last_ns": 1661263407691042682,
                "hull_s": 60.207147898
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/14_04_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 8116,
                "seconds_with_rows": 20,
                "first_ns": 1661263408041874948,
                "last_ns": 1661263427999476981,
                "hull_s": 19.957602033
              },
              "A": {
                "rows": 15509,
                "seconds_with_rows": 41,
                "first_ns": 1661263428000234044,
                "last_ns": 1661263468331987843,
                "hull_s": 40.331753799
              }
            },
            "end_split": {
              "N": {
                "rows": 8112,
                "seconds_with_rows": 20,
                "first_ns": 1661263408044349952,
                "last_ns": 1661263427997415626,
                "hull_s": 19.953065674
              },
              "A": {
                "rows": 15513,
                "seconds_with_rows": 41,
                "first_ns": 1661263428002357791,
                "last_ns": 1661263468336837979,
                "hull_s": 40.334480188
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/14_05_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 25033,
                "seconds_with_rows": 62,
                "first_ns": 1661263467478861751,
                "last_ns": 1661263528305395282,
                "hull_s": 60.826533531
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 25033,
                "seconds_with_rows": 62,
                "first_ns": 1661263467486223616,
                "last_ns": 1661263528310773911,
                "hull_s": 60.824550295
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 31955,
            "seconds_with_rows": 81,
            "first_ns": 1661263347242042098,
            "last_ns": 1661263427999476981,
            "hull_s": 80.757434883
          },
          "A": {
            "rows": 40542,
            "seconds_with_rows": 101,
            "first_ns": 1661263428000234044,
            "last_ns": 1661263528305395282,
            "hull_s": 100.305161238
          }
        },
        "end_split": {
          "N": {
            "rows": 31951,
            "seconds_with_rows": 81,
            "first_ns": 1661263347483894784,
            "last_ns": 1661263427997415626,
            "hull_s": 80.513520842
          },
          "A": {
            "rows": 40546,
            "seconds_with_rows": 101,
            "first_ns": 1661263428002357791,
            "last_ns": 1661263528310773911,
            "hull_s": 100.30841612
          }
        },
        "straddle_t": 4,
        "duplicate_keys": 248,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/log/14_03_log.csv",
            "N": {
              "rows": 25397,
              "seconds_with_rows": 61,
              "first_ns": 1661263347242083807,
              "last_ns": 1661263407691016143,
              "hull_s": 60.448932336
            },
            "A": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/14_04_log.csv",
            "N": {
              "rows": 8714,
              "seconds_with_rows": 20,
              "first_ns": 1661263408041912199,
              "last_ns": 1661263427999271000,
              "hull_s": 19.957358801
            },
            "A": {
              "rows": 16659,
              "seconds_with_rows": 41,
              "first_ns": 1661263428000244715,
              "last_ns": 1661263468336806713,
              "hull_s": 40.336561998
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/14_05_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 26817,
              "seconds_with_rows": 62,
              "first_ns": 1661263467478908964,
              "last_ns": 1661263528310748208,
              "hull_s": 60.831839244
            }
          }
        ],
        "N": {
          "rows": 34111,
          "seconds_with_rows": 81,
          "first_ns": 1661263347242083807,
          "last_ns": 1661263427999271000,
          "hull_s": 80.757187193
        },
        "A": {
          "rows": 43476,
          "seconds_with_rows": 101,
          "first_ns": 1661263428000244715,
          "last_ns": 1661263528310748208,
          "hull_s": 100.310503493
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 77587,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.691e-06,
            1.937438782
          ],
          "relative_end_s": [
            -1.937429286,
            0.011039338
          ]
        }
      },
      "previous_inject_time_ns": 1661262877000000000,
      "previous_gap_s": 551.0,
      "next_gap_s": 544.0,
      "elapsed_s": 1.5469999999986612
    },
    {
      "case": "OB|emailservice|network_delay|2022-08-22 05:43:48",
      "view": "main",
      "t_ns": 1661147028000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661146759862541543,
            "last_ns": 1661146999814921839,
            "hull_s": 239.952380296
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147059733886478,
            "last_ns": 1661147299692708230,
            "hull_s": 239.958821752
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.851042017,
            60.010870643,
            59.964839696,
            60.12562794,
            59.918964639,
            60.038757342,
            60.114313788,
            59.924919829,
            59.880830793
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661146759696975640,
            "last_ns": 1661146999708865210,
            "hull_s": 240.01188957
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147059809048397,
            "last_ns": 1661147299759379686,
            "hull_s": 239.950331289
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.067927985,
            60.011237498,
            60.070811919,
            59.861912168,
            60.100183187,
            60.023956933,
            59.868359315,
            60.008173558,
            60.049841483
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661146759758836619,
            "last_ns": 1661146999771615672,
            "hull_s": 240.012779053
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147059889751447,
            "last_ns": 1661147299854178140,
            "hull_s": 239.964426693
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.099635196,
            59.978032951,
            60.131280394,
            59.803830512,
            60.118135775,
            60.020061561,
            59.845771003,
            60.01365476,
            60.084939369
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661146759801490704,
            "last_ns": 1661146999842978863,
            "hull_s": 240.041488159
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147059939542514,
            "last_ns": 1661147299920655740,
            "hull_s": 239.981113226
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.127278153,
            59.95023909,
            60.129270142,
            59.834700774,
            60.096563651,
            60.002998463,
            59.84983494,
            60.014361248,
            60.113918575
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661146759834186837,
            "last_ns": 1661146999903324027,
            "hull_s": 240.06913719
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147059976420470,
            "last_ns": 1661147299984646560,
            "hull_s": 240.00822609
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.156177665,
            59.919222585,
            60.130937508,
            59.862799432,
            60.073096443,
            59.991030304,
            59.854288041,
            60.017708066,
            60.145199679
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661146759628493237,
            "last_ns": 1661146999640054583,
            "hull_s": 240.011561346
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147059655442362,
            "last_ns": 1661147299647887938,
            "hull_s": 239.992445576
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.015926643,
            60.016719268,
            59.971790017,
            60.007125418,
            60.015387779,
            59.983807541,
            59.995654598,
            60.002600888,
            60.010382549
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661146759875659200,
            "last_ns": 1661146999962059830,
            "hull_s": 240.08640063
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147060031084608,
            "last_ns": 1661147300061553929,
            "hull_s": 240.030469321
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.195290425,
            59.890158263,
            60.124075455,
            59.876876487,
            60.069024778,
            59.974732604,
            59.856540322,
            60.023959716,
            60.175236679
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661146759903610666,
            "last_ns": 1661146999997632992,
            "hull_s": 240.094022326
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147060075037197,
            "last_ns": 1661147300124915762,
            "hull_s": 240.049878565
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.228213843,
            59.869744443,
            60.121282575,
            59.874781465,
            60.077404205,
            59.956139216,
            59.861238416,
            60.051102493,
            60.18139844
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/productcatalogservice-668d5f85fb-wckp8_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661146759937706329,
            "last_ns": 1661147000060059087,
            "hull_s": 240.122352758
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147060111559723,
            "last_ns": 1661147300178488981,
            "hull_s": 240.066929258
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.248841711,
            59.859270441,
            60.112732522,
            59.901508084,
            60.051500636,
            59.949628908,
            59.886155251,
            60.069129015,
            60.162016084
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661146759972499979,
            "last_ns": 1661147000265809114,
            "hull_s": 240.293309135
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147060142606038,
            "last_ns": 1661147300215133290,
            "hull_s": 240.072527252
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.252816488,
            59.856991798,
            60.10392542,
            60.079575429,
            59.876796924,
            59.948982308,
            59.914625487,
            60.075420106,
            60.133499351
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661146760015705902,
            "last_ns": 1661147000324535051,
            "hull_s": 240.308829149
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147060176520870,
            "last_ns": 1661147300247356962,
            "hull_s": 240.070836092
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.245278786,
            59.860999906,
            60.093173618,
            60.109376839,
            59.851985819,
            59.945634618,
            59.948378358,
            60.080231366,
            60.09659175
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/05_43_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 23397,
                "seconds_with_rows": 61,
                "first_ns": 1661146939388355123,
                "last_ns": 1661146999904946903,
                "hull_s": 60.51659178
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "end_split": {
              "N": {
                "rows": 23397,
                "seconds_with_rows": 61,
                "first_ns": 1661146939393897472,
                "last_ns": 1661146999908604629,
                "hull_s": 60.514707157
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/05_44_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 11567,
                "seconds_with_rows": 29,
                "first_ns": 1661146999161136894,
                "last_ns": 1661147027970905432,
                "hull_s": 28.809768538
              },
              "A": {
                "rows": 11593,
                "seconds_with_rows": 32,
                "first_ns": 1661147028269514489,
                "last_ns": 1661147059694894080,
                "hull_s": 31.425379591
              }
            },
            "end_split": {
              "N": {
                "rows": 11563,
                "seconds_with_rows": 29,
                "first_ns": 1661146999193766400,
                "last_ns": 1661147027965627948,
                "hull_s": 28.771861548
              },
              "A": {
                "rows": 11597,
                "seconds_with_rows": 32,
                "first_ns": 1661147028274369541,
                "last_ns": 1661147059697283908,
                "hull_s": 31.422914367
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/05_45_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 23606,
                "seconds_with_rows": 63,
                "first_ns": 1661147058593727703,
                "last_ns": 1661147120496332032,
                "hull_s": 61.902604329
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 23606,
                "seconds_with_rows": 63,
                "first_ns": 1661147058604709700,
                "last_ns": 1661147120498209258,
                "hull_s": 61.893499558
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 34964,
            "seconds_with_rows": 89,
            "first_ns": 1661146939388355123,
            "last_ns": 1661147027970905432,
            "hull_s": 88.582550309
          },
          "A": {
            "rows": 35199,
            "seconds_with_rows": 93,
            "first_ns": 1661147028269514489,
            "last_ns": 1661147120496332032,
            "hull_s": 92.226817543
          }
        },
        "end_split": {
          "N": {
            "rows": 34960,
            "seconds_with_rows": 89,
            "first_ns": 1661146939393897472,
            "last_ns": 1661147027965627948,
            "hull_s": 88.571730476
          },
          "A": {
            "rows": 35203,
            "seconds_with_rows": 93,
            "first_ns": 1661147028274369541,
            "last_ns": 1661147120498209258,
            "hull_s": 92.223839717
          }
        },
        "straddle_t": 4,
        "duplicate_keys": 308,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-22/log/05_43_log.csv",
            "N": {
              "rows": 25138,
              "seconds_with_rows": 61,
              "first_ns": 1661146939388402086,
              "last_ns": 1661146999908570405,
              "hull_s": 60.520168319
            },
            "A": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/log/05_44_log.csv",
            "N": {
              "rows": 12240,
              "seconds_with_rows": 29,
              "first_ns": 1661146999161166526,
              "last_ns": 1661147027970878483,
              "hull_s": 28.809711957
            },
            "A": {
              "rows": 12479,
              "seconds_with_rows": 32,
              "first_ns": 1661147028269603580,
              "last_ns": 1661147059697226219,
              "hull_s": 31.427622639
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/log/05_45_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 25367,
              "seconds_with_rows": 63,
              "first_ns": 1661147058593763796,
              "last_ns": 1661147120498152740,
              "hull_s": 61.904388944
            }
          }
        ],
        "N": {
          "rows": 37378,
          "seconds_with_rows": 89,
          "first_ns": 1661146939388402086,
          "last_ns": 1661147027970878483,
          "hull_s": 88.582476397
        },
        "A": {
          "rows": 37846,
          "seconds_with_rows": 93,
          "first_ns": 1661147028269603580,
          "last_ns": 1661147120498152740,
          "hull_s": 92.22854916
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 75224,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.384e-06,
            2.019552445
          ],
          "relative_end_s": [
            -2.019576643,
            0.010371087
          ]
        }
      },
      "previous_inject_time_ns": 1661146534000000000,
      "previous_gap_s": 494.0,
      "next_gap_s": 546.0,
      "elapsed_s": 1.4530000000013388
    },
    {
      "case": "OB|emailservice|network_delay|2022-08-23 13:54:37",
      "view": "main",
      "t_ns": 1661262877000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262628196026192,
            "last_ns": 1661262868198752189,
            "hull_s": 240.002725997
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262928200073016,
            "last_ns": 1661263168216369118,
            "hull_s": 240.016296102
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            60.035786293,
            59.972273843,
            60.021458048,
            59.973207813,
            60.001320827,
            59.996154019,
            60.035477863,
            60.015996916,
            59.968667304
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262628245810673,
            "last_ns": 1661262868234348446,
            "hull_s": 239.988537773
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262928250237408,
            "last_ns": 1661263168264426411,
            "hull_s": 240.014189003
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            60.056181232,
            59.94749014,
            60.030790023,
            59.954076378,
            60.015888962,
            60.007501598,
            60.045199925,
            59.992299269,
            59.969188211
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262628441974518,
            "last_ns": 1661262868303684600,
            "hull_s": 239.861710082
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262928321841700,
            "last_ns": 1661263168338135680,
            "hull_s": 240.01629398
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.952033441,
            59.937853828,
            60.031605992,
            59.940216821,
            60.0181571,
            60.010218939,
            60.060970085,
            59.973089283,
            59.972015673
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262628478907187,
            "last_ns": 1661262868368361782,
            "hull_s": 239.889454595
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262928371363898,
            "last_ns": 1661263168378946025,
            "hull_s": 240.007582127
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.970325369,
            59.942820923,
            60.033923438,
            59.942384865,
            60.003002116,
            59.993708506,
            60.096339683,
            59.944249994,
            59.973283944
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262628503334156,
            "last_ns": 1661262868429750834,
            "hull_s": 239.926416678
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262928422151899,
            "last_ns": 1661263168415594753,
            "hull_s": 239.993442854
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            59.984097982,
            59.962271809,
            60.033861661,
            59.946185226,
            59.992401065,
            59.969489598,
            60.129988908,
            59.916830404,
            59.977133944
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262628154034818,
            "last_ns": 1661262868156550715,
            "hull_s": 240.002515897
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262928157291710,
            "last_ns": 1661263168166768149,
            "hull_s": 240.009476439
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            60.006812957,
            59.999571188,
            60.000152472,
            59.99597928,
            60.000740995,
            60.001021827,
            60.009145219,
            60.020233015,
            59.979076378
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262628553275113,
            "last_ns": 1661262868496875532,
            "hull_s": 239.943600419
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262928512480554,
            "last_ns": 1661263168472521661,
            "hull_s": 239.960041107
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            60.003160768,
            59.958362191,
            60.05142253,
            59.93065493,
            60.015605022,
            59.93166047,
            60.161652212,
            59.895171812,
            59.971556613
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262628585023183,
            "last_ns": 1661262868526240395,
            "hull_s": 239.941217212
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262928581846246,
            "last_ns": 1661263168508193479,
            "hull_s": 239.926347233
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            60.018330329,
            59.947035909,
            60.081549982,
            59.894300992,
            60.055605851,
            59.890869379,
            60.170033393,
            59.896854551,
            59.96858991
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/productcatalogservice-668d5f85fb-jhwx9_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262628613046556,
            "last_ns": 1661262868558169169,
            "hull_s": 239.945122613
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262928649441008,
            "last_ns": 1661263168543342236,
            "hull_s": 239.893901228
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            60.14338599,
            59.834639711,
            60.088269205,
            59.878827707,
            60.091271839,
            59.85022674,
            60.176215888,
            59.899866337,
            59.967592263
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262628646875150,
            "last_ns": 1661262868590508229,
            "hull_s": 239.943633079
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262928728819288,
            "last_ns": 1661263168584375298,
            "hull_s": 239.85555601
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            60.204347177,
            59.808723725,
            60.060789402,
            59.869772775,
            60.138311059,
            59.798634021,
            60.188849216,
            59.898003134,
            59.970069639
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262628673727126,
            "last_ns": 1661262868622577475,
            "hull_s": 239.948850349
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661262928807261277,
            "last_ns": 1661263168631853296,
            "hull_s": 239.824592019
          },
          "circa_train_observed_rows": 1,
          "cadence_window_s": [
            60.224071008,
            59.813312062,
            60.062739652,
            59.848727627,
            60.184683802,
            59.750205634,
            60.189212513,
            59.90411678,
            59.981057092
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/13_54_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 24315,
                "seconds_with_rows": 62,
                "first_ns": 1661262807604582076,
                "last_ns": 1661262868000901376,
                "hull_s": 60.3963193
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "end_split": {
              "N": {
                "rows": 24315,
                "seconds_with_rows": 62,
                "first_ns": 1661262807685463552,
                "last_ns": 1661262868004810163,
                "hull_s": 60.319346611
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/13_55_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 3175,
                "seconds_with_rows": 9,
                "first_ns": 1661262868345967537,
                "last_ns": 1661262876933504000,
                "hull_s": 8.587536463
              },
              "A": {
                "rows": 20426,
                "seconds_with_rows": 52,
                "first_ns": 1661262877118033803,
                "last_ns": 1661262928560463872,
                "hull_s": 51.442430069
              }
            },
            "end_split": {
              "N": {
                "rows": 3175,
                "seconds_with_rows": 9,
                "first_ns": 1661262868351438592,
                "last_ns": 1661262876935462513,
                "hull_s": 8.584023921
              },
              "A": {
                "rows": 20426,
                "seconds_with_rows": 52,
                "first_ns": 1661262877123500082,
                "last_ns": 1661262928562070175,
                "hull_s": 51.438570093
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/13_56_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 24320,
                "seconds_with_rows": 62,
                "first_ns": 1661262927250294406,
                "last_ns": 1661262988847252624,
                "hull_s": 61.596958218
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 24320,
                "seconds_with_rows": 62,
                "first_ns": 1661262927266478000,
                "last_ns": 1661262988852458266,
                "hull_s": 61.585980266
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 27490,
            "seconds_with_rows": 70,
            "first_ns": 1661262807604582076,
            "last_ns": 1661262876933504000,
            "hull_s": 69.328921924
          },
          "A": {
            "rows": 44746,
            "seconds_with_rows": 112,
            "first_ns": 1661262877118033803,
            "last_ns": 1661262988847252624,
            "hull_s": 111.729218821
          }
        },
        "end_split": {
          "N": {
            "rows": 27490,
            "seconds_with_rows": 70,
            "first_ns": 1661262807685463552,
            "last_ns": 1661262876935462513,
            "hull_s": 69.249998961
          },
          "A": {
            "rows": 44746,
            "seconds_with_rows": 112,
            "first_ns": 1661262877123500082,
            "last_ns": 1661262988852458266,
            "hull_s": 111.728958184
          }
        },
        "straddle_t": 0,
        "duplicate_keys": 184,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/log/13_54_log.csv",
            "N": {
              "rows": 25761,
              "seconds_with_rows": 62,
              "first_ns": 1661262807604609367,
              "last_ns": 1661262868004784417,
              "hull_s": 60.40017505
            },
            "A": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/13_55_log.csv",
            "N": {
              "rows": 3566,
              "seconds_with_rows": 9,
              "first_ns": 1661262868346021050,
              "last_ns": 1661262876935438566,
              "hull_s": 8.589417516
            },
            "A": {
              "rows": 21766,
              "seconds_with_rows": 52,
              "first_ns": 1661262877118100854,
              "last_ns": 1661262928562025612,
              "hull_s": 51.443924758
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/13_56_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 26290,
              "seconds_with_rows": 62,
              "first_ns": 1661262927250328011,
              "last_ns": 1661262988852432813,
              "hull_s": 61.602104802
            }
          }
        ],
        "N": {
          "rows": 29327,
          "seconds_with_rows": 70,
          "first_ns": 1661262807604609367,
          "last_ns": 1661262876935438566,
          "hull_s": 69.330829199
        },
        "A": {
          "rows": 48056,
          "seconds_with_rows": 112,
          "first_ns": 1661262877118100854,
          "last_ns": 1661262988852432813,
          "hull_s": 111.734331959
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 77383,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.352e-06,
            2.05736601
          ],
          "relative_end_s": [
            -2.057352047,
            0.027073435
          ]
        }
      },
      "previous_inject_time_ns": 1661262353000000000,
      "previous_gap_s": 524.0,
      "next_gap_s": 551.0,
      "elapsed_s": 1.5159999999996217
    },
    {
      "case": "OB|frontend|return|2022-08-22 04:02:07",
      "view": "main",
      "t_ns": 1661140927000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140639601329777,
            "last_ns": 1661140879622485917,
            "hull_s": 240.02115614
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140939614100149,
            "last_ns": 1661141179628807702,
            "hull_s": 240.014707553
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.996828674,
            60.010146035,
            60.013510548,
            60.000670883,
            59.991614232,
            60.028130173,
            59.969090433,
            60.249136759,
            59.768350188
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140639651248613,
            "last_ns": 1661140879691477047,
            "hull_s": 240.040228434
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140939652681829,
            "last_ns": 1661141179666194317,
            "hull_s": 240.013512488
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.986946385,
            60.16605611,
            59.874575845,
            60.012650094,
            59.961204782,
            60.029485453,
            59.961151122,
            60.066378336,
            59.956497577
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140639743787534,
            "last_ns": 1661140879783809293,
            "hull_s": 240.040021759
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140939719747038,
            "last_ns": 1661141179716445705,
            "hull_s": 239.996698667
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.959337217,
            60.204960392,
            59.990623538,
            59.885100612,
            59.935937745,
            60.017627845,
            59.957149334,
            60.113521652,
            59.908399836
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140639791070043,
            "last_ns": 1661140879847531398,
            "hull_s": 240.056461355
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140939752371816,
            "last_ns": 1661141179746755863,
            "hull_s": 239.994384047
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.95082391,
            60.231046876,
            59.964412884,
            59.910177685,
            59.904840418,
            60.029300875,
            59.944152278,
            60.159695652,
            59.861235242
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140639820898677,
            "last_ns": 1661140880067313780,
            "hull_s": 240.246415103
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140939783064231,
            "last_ns": 1661141179770928820,
            "hull_s": 239.987864589
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.954418747,
            60.256862901,
            59.933489473,
            60.101643982,
            59.715750451,
            60.023632787,
            59.949750472,
            60.198253037,
            59.816228293
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140639552898907,
            "last_ns": 1661140879584228913,
            "hull_s": 240.031330006
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140939576577994,
            "last_ns": 1661141179584545395,
            "hull_s": 240.007967401
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.007298663,
            60.015335864,
            60.002657802,
            60.006037677,
            59.992349081,
            60.011377454,
            59.990131241,
            60.011634877,
            59.994823829
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140639863442594,
            "last_ns": 1661140880144142076,
            "hull_s": 240.280699482
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140939822586147,
            "last_ns": 1661141179801777041,
            "hull_s": 239.979190894
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.949063173,
            60.283444427,
            59.903395895,
            60.144795987,
            59.678444071,
            60.020216087,
            59.957690293,
            60.232778166,
            59.768506348
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140639905923507,
            "last_ns": 1661140880206751220,
            "hull_s": 240.300827713
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140939852948474,
            "last_ns": 1661141179825304305,
            "hull_s": 239.972355831
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.956549307,
            60.297460726,
            59.867411481,
            60.179406199,
            59.646197254,
            60.018709133,
            59.989875839,
            60.224604883,
            59.739165976
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/productcatalogservice-668d5f85fb-wckp8_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140639949654612,
            "last_ns": 1661140880274368620,
            "hull_s": 240.324714008
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140939887604125,
            "last_ns": 1661141179855709431,
            "hull_s": 239.968105306
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.971626331,
            60.303658286,
            59.833801998,
            60.215627393,
            59.613235505,
            60.016619128,
            60.01986774,
            60.213420463,
            59.718197975
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140640011277721,
            "last_ns": 1661140880339523354,
            "hull_s": 240.328245633
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140940043901718,
            "last_ns": 1661141179888592048,
            "hull_s": 239.84469033
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.972230254,
            60.300612386,
            59.803793396,
            60.251609597,
            59.704378364,
            59.893188475,
            60.047394455,
            60.184166031,
            59.719941369
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140640073211466,
            "last_ns": 1661140880406723172,
            "hull_s": 240.333511706
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661140940117098327,
            "last_ns": 1661141179934829367,
            "hull_s": 239.81773104
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.955483387,
            60.316221187,
            59.771385295,
            60.290421837,
            59.710375155,
            59.857300646,
            60.071022792,
            60.158952721,
            59.730454881
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/04_02_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 18504,
                "seconds_with_rows": 48,
                "first_ns": 1661140879339835301,
                "last_ns": 1661140926999062638,
                "hull_s": 47.659227337
              },
              "A": {
                "rows": 3841,
                "seconds_with_rows": 13,
                "first_ns": 1661140927000199073,
                "last_ns": 1661140939405410336,
                "hull_s": 12.405211263
              }
            },
            "end_split": {
              "N": {
                "rows": 18497,
                "seconds_with_rows": 48,
                "first_ns": 1661140879344439719,
                "last_ns": 1661140926997820160,
                "hull_s": 47.653380441
              },
              "A": {
                "rows": 3848,
                "seconds_with_rows": 13,
                "first_ns": 1661140927000179647,
                "last_ns": 1661140939408842466,
                "hull_s": 12.408662819
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/04_03_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 12029,
                "seconds_with_rows": 61,
                "first_ns": 1661140939240674905,
                "last_ns": 1661140999993681242,
                "hull_s": 60.753006337
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 12029,
                "seconds_with_rows": 61,
                "first_ns": 1661140939247147520,
                "last_ns": 1661140999996116150,
                "hull_s": 60.74896863
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/04_04_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 13837,
                "seconds_with_rows": 61,
                "first_ns": 1661140999126030852,
                "last_ns": 1661141059155031808,
                "hull_s": 60.029000956
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 13837,
                "seconds_with_rows": 61,
                "first_ns": 1661140999128441856,
                "last_ns": 1661141059157455768,
                "hull_s": 60.029013912
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 18504,
            "seconds_with_rows": 48,
            "first_ns": 1661140879339835301,
            "last_ns": 1661140926999062638,
            "hull_s": 47.659227337
          },
          "A": {
            "rows": 29707,
            "seconds_with_rows": 133,
            "first_ns": 1661140927000199073,
            "last_ns": 1661141059155031808,
            "hull_s": 132.154832735
          }
        },
        "end_split": {
          "N": {
            "rows": 18497,
            "seconds_with_rows": 48,
            "first_ns": 1661140879344439719,
            "last_ns": 1661140926997820160,
            "hull_s": 47.653380441
          },
          "A": {
            "rows": 29714,
            "seconds_with_rows": 133,
            "first_ns": 1661140927000179647,
            "last_ns": 1661141059157455768,
            "hull_s": 132.157276121
          }
        },
        "straddle_t": 7,
        "duplicate_keys": 333,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-22/log/04_02_log.csv",
            "N": {
              "rows": 19846,
              "seconds_with_rows": 48,
              "first_ns": 1661140879339870647,
              "last_ns": 1661140926999117319,
              "hull_s": 47.659246672
            },
            "A": {
              "rows": 4354,
              "seconds_with_rows": 13,
              "first_ns": 1661140927001886668,
              "last_ns": 1661140939408815080,
              "hull_s": 12.406928412
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/log/04_03_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 14918,
              "seconds_with_rows": 61,
              "first_ns": 1661140939240710174,
              "last_ns": 1661140999996088448,
              "hull_s": 60.755378274
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/log/04_04_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 16769,
              "seconds_with_rows": 61,
              "first_ns": 1661140999126060371,
              "last_ns": 1661141059157428680,
              "hull_s": 60.031368309
            }
          }
        ],
        "N": {
          "rows": 19846,
          "seconds_with_rows": 48,
          "first_ns": 1661140879339870647,
          "last_ns": 1661140926999117319,
          "hull_s": 47.659246672
        },
        "A": {
          "rows": 36041,
          "seconds_with_rows": 133,
          "first_ns": 1661140927001886668,
          "last_ns": 1661141059157428680,
          "hull_s": 132.155542012
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 55887,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.652e-06,
            1.642897176
          ],
          "relative_end_s": [
            -1.6428988,
            0.01035053
          ]
        }
      },
      "previous_inject_time_ns": 1661140434000000000,
      "previous_gap_s": 493.0,
      "next_gap_s": 493.0,
      "elapsed_s": 1.0309999999990396
    },
    {
      "case": "OB|frontend|return|2022-08-23 12:10:21",
      "view": "main",
      "t_ns": 1661256621000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256328115581244,
            "last_ns": 1661256568161199804,
            "hull_s": 240.04561856
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256628117272490,
            "last_ns": 1661256868156787084,
            "hull_s": 240.039514594
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.052866776,
            59.950166892,
            60.016729445,
            60.025855447,
            59.956072686,
            60.021265956,
            60.008336092,
            59.983526545,
            60.026386001
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256328154239624,
            "last_ns": 1661256568201055178,
            "hull_s": 240.046815554
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256628151672887,
            "last_ns": 1661256868193442432,
            "hull_s": 240.041769545
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.051424443,
            59.944533365,
            60.026301411,
            60.024556335,
            59.950617709,
            60.025885502,
            60.019916407,
            59.974376579,
            60.021591057
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256328209115841,
            "last_ns": 1661256568267276632,
            "hull_s": 240.058160791
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256628224526469,
            "last_ns": 1661256868260022430,
            "hull_s": 240.035495961
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.057593171,
            59.931708337,
            60.053171517,
            60.015687766,
            59.957249837,
            60.007096309,
            60.048809122,
            59.962166439,
            60.017424091
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256328242353437,
            "last_ns": 1661256568311918803,
            "hull_s": 240.069565366
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256628271271700,
            "last_ns": 1661256868305997675,
            "hull_s": 240.034725975
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.06472874,
            59.922345596,
            60.071393965,
            60.011097065,
            59.959352897,
            60.000831612,
            60.080126146,
            59.95192541,
            60.001842807
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256328268285030,
            "last_ns": 1661256568371555260,
            "hull_s": 240.10327023
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256628331918436,
            "last_ns": 1661256868354954997,
            "hull_s": 240.023036561
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.077812539,
            59.908144333,
            60.087765106,
            60.029548252,
            59.960363176,
            59.971756034,
            60.106065089,
            59.945945718,
            59.99926972
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256328076108083,
            "last_ns": 1661256568106369594,
            "hull_s": 240.030261511
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256628086925025,
            "last_ns": 1661256868098759933,
            "hull_s": 240.011834908
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.050407049,
            59.961984366,
            60.007364727,
            60.010505369,
            59.980555431,
            60.011988991,
            59.998725496,
            59.995714472,
            60.005405949
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256328322360107,
            "last_ns": 1661256568437935327,
            "hull_s": 240.11557522
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256628410529528,
            "last_ns": 1661256868416365411,
            "hull_s": 240.005835883
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.07929014,
            59.896115068,
            60.088755931,
            60.051414081,
            59.972594201,
            59.960380515,
            60.128960745,
            59.916681395,
            59.999813228
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256328362549681,
            "last_ns": 1661256568474507962,
            "hull_s": 240.111958281
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256628472741983,
            "last_ns": 1661256868454128487,
            "hull_s": 239.981386504
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.071413307,
            59.893185537,
            60.091855849,
            60.055503588,
            59.998234021,
            59.936611094,
            60.1527136,
            59.889609428,
            60.002452382
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/productcatalogservice-668d5f85fb-jhwx9_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256328417219375,
            "last_ns": 1661256568507780317,
            "hull_s": 240.090560942
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256628533265664,
            "last_ns": 1661256868488125430,
            "hull_s": 239.954859766
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.050156823,
            59.889557031,
            60.095336173,
            60.055510915,
            60.025485347,
            59.927552263,
            60.156640168,
            59.868526299,
            60.002141036
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256328483801095,
            "last_ns": 1661256568549120686,
            "hull_s": 240.065319591
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256628582142841,
            "last_ns": 1661256868532475265,
            "hull_s": 239.950332424
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.020138722,
            59.883670796,
            60.096867195,
            60.064642878,
            60.033022155,
            59.917444634,
            60.164316571,
            59.867029556,
            60.001541663
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256328544646838,
            "last_ns": 1661256568583965720,
            "hull_s": 240.039318882
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661256628614098577,
            "last_ns": 1661256868585232943,
            "hull_s": 239.971134366
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.993780464,
            59.882801506,
            60.113363001,
            60.049373911,
            60.030132857,
            59.935935508,
            60.163470067,
            59.874042892,
            59.997685899
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/12_10_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 19757,
                "seconds_with_rows": 53,
                "first_ns": 1661256568153084159,
                "last_ns": 1661256620995397846,
                "hull_s": 52.842313687
              },
              "A": {
                "rows": 1631,
                "seconds_with_rows": 7,
                "first_ns": 1661256621001048538,
                "last_ns": 1661256627860748158,
                "hull_s": 6.85969962
              }
            },
            "end_split": {
              "N": {
                "rows": 19751,
                "seconds_with_rows": 53,
                "first_ns": 1661256568157590460,
                "last_ns": 1661256620995346364,
                "hull_s": 52.837755904
              },
              "A": {
                "rows": 1637,
                "seconds_with_rows": 7,
                "first_ns": 1661256621000954431,
                "last_ns": 1661256627861159945,
                "hull_s": 6.860205514
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/12_11_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 12257,
                "seconds_with_rows": 60,
                "first_ns": 1661256628186259583,
                "last_ns": 1661256687783244800,
                "hull_s": 59.596985217
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 12257,
                "seconds_with_rows": 60,
                "first_ns": 1661256628186672551,
                "last_ns": 1661256687785933363,
                "hull_s": 59.599260812
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/12_12_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 12865,
                "seconds_with_rows": 60,
                "first_ns": 1661256688023062687,
                "last_ns": 1661256747792622336,
                "hull_s": 59.769559649
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 12865,
                "seconds_with_rows": 60,
                "first_ns": 1661256688023353919,
                "last_ns": 1661256747794564748,
                "hull_s": 59.771210829
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 19757,
            "seconds_with_rows": 53,
            "first_ns": 1661256568153084159,
            "last_ns": 1661256620995397846,
            "hull_s": 52.842313687
          },
          "A": {
            "rows": 26753,
            "seconds_with_rows": 127,
            "first_ns": 1661256621001048538,
            "last_ns": 1661256747792622336,
            "hull_s": 126.791573798
          }
        },
        "end_split": {
          "N": {
            "rows": 19751,
            "seconds_with_rows": 53,
            "first_ns": 1661256568157590460,
            "last_ns": 1661256620995346364,
            "hull_s": 52.837755904
          },
          "A": {
            "rows": 26759,
            "seconds_with_rows": 127,
            "first_ns": 1661256621000954431,
            "last_ns": 1661256747794564748,
            "hull_s": 126.793610317
          }
        },
        "straddle_t": 6,
        "duplicate_keys": 0,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/log/12_10_log.csv",
            "N": {
              "rows": 21473,
              "seconds_with_rows": 53,
              "first_ns": 1661256568153135011,
              "last_ns": 1661256620995439446,
              "hull_s": 52.842304435
            },
            "A": {
              "rows": 1838,
              "seconds_with_rows": 7,
              "first_ns": 1661256621000854824,
              "last_ns": 1661256627861126723,
              "hull_s": 6.860271899
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/12_11_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 14821,
              "seconds_with_rows": 60,
              "first_ns": 1661256628186310710,
              "last_ns": 1661256687785903101,
              "hull_s": 59.599592391
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/12_12_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 15643,
              "seconds_with_rows": 60,
              "first_ns": 1661256688023114337,
              "last_ns": 1661256747794537619,
              "hull_s": 59.771423282
            }
          }
        ],
        "N": {
          "rows": 21473,
          "seconds_with_rows": 53,
          "first_ns": 1661256568153135011,
          "last_ns": 1661256620995439446,
          "hull_s": 52.842304435
        },
        "A": {
          "rows": 32302,
          "seconds_with_rows": 127,
          "first_ns": 1661256621000854824,
          "last_ns": 1661256747794537619,
          "hull_s": 126.793682795
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 53775,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.691e-06,
            1.322782192
          ],
          "relative_end_s": [
            -1.322770741,
            0.009540987
          ]
        }
      },
      "previous_inject_time_ns": 1661256085000000000,
      "previous_gap_s": 536.0,
      "next_gap_s": 482.0,
      "elapsed_s": 1.1090000000003783
    },
    {
      "case": "OB|paymentservice|cpu_contention|2022-08-22 06:01:18",
      "view": "main",
      "t_ns": 1661148078000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147779683073296,
            "last_ns": 1661148019693864581,
            "hull_s": 240.010791285
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661148079868144690,
            "last_ns": 1661148319811403539,
            "hull_s": 239.943258849
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.130401165,
            59.890041643,
            60.165170089,
            59.825178388,
            60.174280109,
            59.825694613,
            59.994525173,
            60.006769904,
            60.116269159
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147779719125199,
            "last_ns": 1661148019732841416,
            "hull_s": 240.013716217
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661148079707581645,
            "last_ns": 1661148319699880536,
            "hull_s": 239.992298891
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.994351571,
            60.056868871,
            59.918546638,
            60.043949137,
            59.974740229,
            60.047800306,
            59.969232961,
            60.030482192,
            59.944783432
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147779780194600,
            "last_ns": 1661148019872687107,
            "hull_s": 240.092492507
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661148079762052512,
            "last_ns": 1661148319755929025,
            "hull_s": 239.993876513
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.002154495,
            60.067859619,
            59.892882913,
            60.12959548,
            59.889365405,
            60.072013673,
            59.949303598,
            60.033911117,
            59.938648125
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147779819398152,
            "last_ns": 1661148020004202300,
            "hull_s": 240.184804148
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661148079797920356,
            "last_ns": 1661148319799360240,
            "hull_s": 240.001439884
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.002784976,
            60.065439996,
            59.887764305,
            60.228814871,
            59.793718056,
            60.079003812,
            59.946635533,
            60.036768177,
            59.939032362
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147779868507230,
            "last_ns": 1661148020036539063,
            "hull_s": 240.168031833
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661148079825802050,
            "last_ns": 1661148319823505620,
            "hull_s": 239.99770357
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.986236674,
            60.061634454,
            59.887535852,
            60.232624853,
            59.789262987,
            60.085046381,
            59.940599573,
            60.044914104,
            59.927143512
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147779624147254,
            "last_ns": 1661148019638401495,
            "hull_s": 240.014254241
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661148079626677751,
            "last_ns": 1661148319642747171,
            "hull_s": 240.01606942
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.011895846,
            60.000986191,
            59.989140267,
            60.012231937,
            59.988276256,
            60.00636617,
            60.019301023,
            59.996978915,
            59.993423312
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147779947500100,
            "last_ns": 1661148020090837419,
            "hull_s": 240.143337319
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661148079869229162,
            "last_ns": 1661148319855924331,
            "hull_s": 239.986695169
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.966147757,
            60.063605292,
            59.871995445,
            60.241588825,
            59.778391743,
            60.096038136,
            59.927408451,
            60.055373662,
            59.90787492
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147780018800383,
            "last_ns": 1661148020127311099,
            "hull_s": 240.108510716
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661148079916341284,
            "last_ns": 1661148319881321421,
            "hull_s": 239.964980137
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.941179965,
            60.051849098,
            59.864787544,
            60.250694109,
            59.789030185,
            60.076138352,
            59.935138263,
            60.063884871,
            59.889818651
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/productcatalogservice-668d5f85fb-wckp8_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147780115978901,
            "last_ns": 1661148020178916334,
            "hull_s": 240.062937433
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661148079953081091,
            "last_ns": 1661148319913192497,
            "hull_s": 239.960111406
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.890987668,
            60.037257894,
            59.862306751,
            60.27238512,
            59.774164757,
            60.069324165,
            59.941936184,
            60.085420206,
            59.863430851
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147780309378193,
            "last_ns": 1661148020245722809,
            "hull_s": 239.936344616
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661148079985364559,
            "last_ns": 1661148319944782827,
            "hull_s": 239.959418268
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.729681421,
            60.034552899,
            59.859397353,
            60.312712943,
            59.73964175,
            60.068020497,
            59.9454666,
            60.110654766,
            59.835276405
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661147780376949421,
            "last_ns": 1661148020314407126,
            "hull_s": 239.937457705
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661148080027043122,
            "last_ns": 1661148319975179222,
            "hull_s": 239.9481361
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.702006042,
            60.02699772,
            59.854429018,
            60.354024925,
            59.712635996,
            60.057868311,
            59.94946536,
            60.133652683,
            59.807149746
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/06_01_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 23060,
                "seconds_with_rows": 59,
                "first_ns": 1661148019325432938,
                "last_ns": 1661148077999096532,
                "hull_s": 58.673663594
              },
              "A": {
                "rows": 550,
                "seconds_with_rows": 2,
                "first_ns": 1661148078046452263,
                "last_ns": 1661148079529956084,
                "hull_s": 1.483503821
              }
            },
            "end_split": {
              "N": {
                "rows": 23054,
                "seconds_with_rows": 59,
                "first_ns": 1661148019341571076,
                "last_ns": 1661148077999078723,
                "hull_s": 58.657507647
              },
              "A": {
                "rows": 556,
                "seconds_with_rows": 2,
                "first_ns": 1661148078052797746,
                "last_ns": 1661148079533042256,
                "hull_s": 1.48024451
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/06_02_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 24687,
                "seconds_with_rows": 62,
                "first_ns": 1661148078328889440,
                "last_ns": 1661148139558803968,
                "hull_s": 61.229914528
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 24687,
                "seconds_with_rows": 62,
                "first_ns": 1661148078792520704,
                "last_ns": 1661148139560786899,
                "hull_s": 60.768266195
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/06_03_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 23591,
                "seconds_with_rows": 60,
                "first_ns": 1661148139723655810,
                "last_ns": 1661148198746482416,
                "hull_s": 59.022826606
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 23591,
                "seconds_with_rows": 60,
                "first_ns": 1661148139729344256,
                "last_ns": 1661148198750104625,
                "hull_s": 59.020760369
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 23060,
            "seconds_with_rows": 59,
            "first_ns": 1661148019325432938,
            "last_ns": 1661148077999096532,
            "hull_s": 58.673663594
          },
          "A": {
            "rows": 48828,
            "seconds_with_rows": 121,
            "first_ns": 1661148078046452263,
            "last_ns": 1661148198746482416,
            "hull_s": 120.700030153
          }
        },
        "end_split": {
          "N": {
            "rows": 23054,
            "seconds_with_rows": 59,
            "first_ns": 1661148019341571076,
            "last_ns": 1661148077999078723,
            "hull_s": 58.657507647
          },
          "A": {
            "rows": 48834,
            "seconds_with_rows": 121,
            "first_ns": 1661148078052797746,
            "last_ns": 1661148198750104625,
            "hull_s": 120.697306879
          }
        },
        "straddle_t": 6,
        "duplicate_keys": 110,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-22/log/06_01_log.csv",
            "N": {
              "rows": 24650,
              "seconds_with_rows": 59,
              "first_ns": 1661148019325464420,
              "last_ns": 1661148077999155829,
              "hull_s": 58.673691409
            },
            "A": {
              "rows": 587,
              "seconds_with_rows": 2,
              "first_ns": 1661148078046491924,
              "last_ns": 1661148079533018673,
              "hull_s": 1.486526749
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/log/06_02_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 26271,
              "seconds_with_rows": 62,
              "first_ns": 1661148078328920202,
              "last_ns": 1661148139560762564,
              "hull_s": 61.231842362
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/log/06_03_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 25337,
              "seconds_with_rows": 60,
              "first_ns": 1661148139723703913,
              "last_ns": 1661148198750077314,
              "hull_s": 59.026373401
            }
          }
        ],
        "N": {
          "rows": 24650,
          "seconds_with_rows": 59,
          "first_ns": 1661148019325464420,
          "last_ns": 1661148077999155829,
          "hull_s": 58.673691409
        },
        "A": {
          "rows": 52195,
          "seconds_with_rows": 121,
          "first_ns": 1661148078046491924,
          "last_ns": 1661148198750077314,
          "hull_s": 120.70358539
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 76845,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.619e-06,
            1.914076402
          ],
          "relative_end_s": [
            -1.914071953,
            0.037971571
          ]
        }
      },
      "previous_inject_time_ns": 1661147574000000000,
      "previous_gap_s": 504.0,
      "next_gap_s": 2061.0,
      "elapsed_s": 1.5940000000009604
    },
    {
      "case": "OB|paymentservice|cpu_contention|2022-08-23 14:21:54",
      "view": "main",
      "t_ns": 1661264514000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264248200129535,
            "last_ns": 1661264488246855353,
            "hull_s": 240.046725818
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264548251275068,
            "last_ns": 1661264788244614271,
            "hull_s": 239.993339203
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.044229782,
            59.986420568,
            59.996560117,
            60.019515351,
            60.004419715,
            59.988762555,
            59.984078407,
            60.003340947,
            60.017157294
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264248239818795,
            "last_ns": 1661264488314271804,
            "hull_s": 240.074453009
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264548376018260,
            "last_ns": 1661264788305815903,
            "hull_s": 239.929797643
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.056092183,
            59.967300671,
            60.016982399,
            60.034077756,
            60.061746456,
            59.925400527,
            59.965566718,
            59.995943087,
            60.042887311
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264248305326197,
            "last_ns": 1661264488422403474,
            "hull_s": 240.117077277
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264548548845740,
            "last_ns": 1661264788391020625,
            "hull_s": 239.842174885
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.059164055,
            59.956237471,
            60.050854139,
            60.050821612,
            60.126442266,
            59.843082873,
            59.943152828,
            59.99995268,
            60.055986504
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264248348098320,
            "last_ns": 1661264488474115962,
            "hull_s": 240.126017642
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264548620279091,
            "last_ns": 1661264788452522584,
            "hull_s": 239.832243493
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.076930919,
            59.936373423,
            60.080511453,
            60.032201847,
            60.146163129,
            59.964947381,
            59.786980606,
            60.031551636,
            60.04876387
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264248389804534,
            "last_ns": 1661264488503530829,
            "hull_s": 240.113726295
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264548674573358,
            "last_ns": 1661264788504450614,
            "hull_s": 239.829877256
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.080631723,
            59.937275748,
            60.081514872,
            60.014303952,
            60.171042529,
            59.97168756,
            59.757415203,
            60.061294069,
            60.039480424
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264248163239638,
            "last_ns": 1661264488179018687,
            "hull_s": 240.015779049
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264548181848433,
            "last_ns": 1661264788178098061,
            "hull_s": 239.996249628
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.024629074,
            59.996048006,
            59.996742148,
            59.998359821,
            60.002829746,
            60.002189472,
            59.989794385,
            60.010371703,
            59.993894068
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264248443435748,
            "last_ns": 1661264488565300123,
            "hull_s": 240.121864375
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264548729660420,
            "last_ns": 1661264788581681170,
            "hull_s": 239.85202075
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.094255166,
            59.938487874,
            60.080006926,
            60.009114409,
            60.164360297,
            59.997100589,
            59.879077017,
            59.946421639,
            60.029421505
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264248481835409,
            "last_ns": 1661264488596956116,
            "hull_s": 240.115120707
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264548778116383,
            "last_ns": 1661264788630862910,
            "hull_s": 239.852746527
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.10283057,
            59.94532897,
            60.095735242,
            59.971225925,
            60.181160267,
            59.982327639,
            59.880406713,
            59.95412139,
            60.035890785
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/productcatalogservice-668d5f85fb-jhwx9_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264248517339684,
            "last_ns": 1661264488630279836,
            "hull_s": 240.112940152
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264548824752966,
            "last_ns": 1661264788663673198,
            "hull_s": 239.838920232
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.113809677,
            59.9430385,
            60.099291943,
            59.956800032,
            60.19447313,
            59.976281794,
            59.874066503,
            60.109743442,
            59.878828493
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264248550488675,
            "last_ns": 1661264488663861261,
            "hull_s": 240.113372586
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264548866401274,
            "last_ns": 1661264788709154729,
            "hull_s": 239.842753455
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.117860073,
            59.962132865,
            60.079224386,
            59.954155262,
            60.202540013,
            59.967778116,
            59.876442055,
            60.133779277,
            59.864754007
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264248580693960,
            "last_ns": 1661264488699674659,
            "hull_s": 240.118980699
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661264548897603703,
            "last_ns": 1661264788757517813,
            "hull_s": 239.85991411
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.145335691,
            59.941794035,
            60.075355318,
            59.956495655,
            60.197929044,
            59.97353706,
            59.877849,
            60.130711823,
            59.877816227
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/14_21_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 24149,
                "seconds_with_rows": 61,
                "first_ns": 1661264428046884802,
                "last_ns": 1661264488334745139,
                "hull_s": 60.287860337
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "end_split": {
              "N": {
                "rows": 24149,
                "seconds_with_rows": 61,
                "first_ns": 1661264428049704913,
                "last_ns": 1661264488339655977,
                "hull_s": 60.289951064
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/14_22_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 10635,
                "seconds_with_rows": 27,
                "first_ns": 1661264487555737033,
                "last_ns": 1661264513554833783,
                "hull_s": 25.99909675
              },
              "A": {
                "rows": 13423,
                "seconds_with_rows": 34,
                "first_ns": 1661264514113330218,
                "last_ns": 1661264547984467712,
                "hull_s": 33.871137494
              }
            },
            "end_split": {
              "N": {
                "rows": 10635,
                "seconds_with_rows": 27,
                "first_ns": 1661264487597886208,
                "last_ns": 1661264513557527265,
                "hull_s": 25.959641057
              },
              "A": {
                "rows": 13423,
                "seconds_with_rows": 34,
                "first_ns": 1661264514117641653,
                "last_ns": 1661264547986465122,
                "hull_s": 33.868823469
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/14_23_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 23103,
                "seconds_with_rows": 61,
                "first_ns": 1661264547844493202,
                "last_ns": 1661264608200910080,
                "hull_s": 60.356416878
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 23103,
                "seconds_with_rows": 61,
                "first_ns": 1661264547850454262,
                "last_ns": 1661264608202977374,
                "hull_s": 60.352523112
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 34784,
            "seconds_with_rows": 86,
            "first_ns": 1661264428046884802,
            "last_ns": 1661264513554833783,
            "hull_s": 85.507948981
          },
          "A": {
            "rows": 36526,
            "seconds_with_rows": 94,
            "first_ns": 1661264514113330218,
            "last_ns": 1661264608200910080,
            "hull_s": 94.087579862
          }
        },
        "end_split": {
          "N": {
            "rows": 34784,
            "seconds_with_rows": 86,
            "first_ns": 1661264428049704913,
            "last_ns": 1661264513557527265,
            "hull_s": 85.507822352
          },
          "A": {
            "rows": 36526,
            "seconds_with_rows": 94,
            "first_ns": 1661264514117641653,
            "last_ns": 1661264608202977374,
            "hull_s": 94.085335721
          }
        },
        "straddle_t": 0,
        "duplicate_keys": 359,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/log/14_21_log.csv",
            "N": {
              "rows": 26360,
              "seconds_with_rows": 61,
              "first_ns": 1661264428046921968,
              "last_ns": 1661264488339624754,
              "hull_s": 60.292702786
            },
            "A": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/14_22_log.csv",
            "N": {
              "rows": 11774,
              "seconds_with_rows": 27,
              "first_ns": 1661264487555765102,
              "last_ns": 1661264513557498829,
              "hull_s": 26.001733727
            },
            "A": {
              "rows": 14670,
              "seconds_with_rows": 34,
              "first_ns": 1661264514113378304,
              "last_ns": 1661264547986437130,
              "hull_s": 33.873058826
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/14_23_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 25220,
              "seconds_with_rows": 61,
              "first_ns": 1661264547844555761,
              "last_ns": 1661264608202951842,
              "hull_s": 60.358396081
            }
          }
        ],
        "N": {
          "rows": 38134,
          "seconds_with_rows": 86,
          "first_ns": 1661264428046921968,
          "last_ns": 1661264513557498829,
          "hull_s": 85.510576861
        },
        "A": {
          "rows": 39890,
          "seconds_with_rows": 94,
          "first_ns": 1661264514113378304,
          "last_ns": 1661264608202951842,
          "hull_s": 94.089573538
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 76523,
          "missing_span_in_selected_window": 1501,
          "relative_start_s": [
            2.623e-06,
            1.283405728
          ],
          "relative_end_s": [
            -1.283386226,
            0.011969856
          ]
        }
      },
      "previous_inject_time_ns": 1661263972000000000,
      "previous_gap_s": 542.0,
      "next_gap_s": 496.0,
      "elapsed_s": 1.6719999999986612
    },
    {
      "case": "OB|productcatalogservice|exception|2022-08-23 15:04:28",
      "view": "main",
      "t_ns": 1661267068000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661266768251088798,
            "last_ns": 1661267008287344884,
            "hull_s": 240.036256086
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267068283859221,
            "last_ns": 1661267308228472744,
            "hull_s": 239.944613523
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.987106258,
            59.973069963,
            60.020299984,
            60.055779881,
            59.996514337,
            59.940943331,
            60.003543224,
            60.047034054,
            59.953092914
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661266768285177667,
            "last_ns": 1661267008457708821,
            "hull_s": 240.172531154
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267068353236582,
            "last_ns": 1661267308267016721,
            "hull_s": 239.913780139
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.987322703,
            59.975030069,
            60.01626646,
            60.193911922,
            59.895527761,
            59.930758113,
            59.979966927,
            60.081577647,
            59.921477452
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661266768354449961,
            "last_ns": 1661267008567460545,
            "hull_s": 240.213010584
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267068448473067,
            "last_ns": 1661267308329043756,
            "hull_s": 239.880570689
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.983990134,
            59.97235752,
            60.010979364,
            60.245683566,
            59.881012522,
            59.899933607,
            59.979102067,
            60.111673135,
            59.88986188
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661266768393309769,
            "last_ns": 1661267008632106012,
            "hull_s": 240.238796243
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267068520970689,
            "last_ns": 1661267308362730972,
            "hull_s": 239.841760283
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.985989412,
            59.975012584,
            60.01468722,
            60.263107027,
            59.888864677,
            59.857387115,
            59.990028276,
            60.128731879,
            59.865613013
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661266768426763525,
            "last_ns": 1661267008667425354,
            "hull_s": 240.240661829
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267068659131315,
            "last_ns": 1661267308392920779,
            "hull_s": 239.733789464
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.97901868,
            59.97464845,
            60.017982147,
            60.269012552,
            59.991705961,
            59.742626437,
            60.000276348,
            60.134811734,
            59.856074945
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661266768199586337,
            "last_ns": 1661267008209118750,
            "hull_s": 240.009532413
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267068211033200,
            "last_ns": 1661267308192218107,
            "hull_s": 239.981184907
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.996103733,
            59.985759448,
            60.016496138,
            60.011173094,
            60.00191445,
            59.979544107,
            60.003663996,
            60.012484615,
            59.985492189
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661266768493198527,
            "last_ns": 1661267008719354108,
            "hull_s": 240.226155581
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267068797475544,
            "last_ns": 1661267308454616026,
            "hull_s": 239.657140482
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.967332516,
            59.962742464,
            60.022788389,
            60.273292212,
            60.078121436,
            59.650383348,
            60.012368934,
            60.158958105,
            59.835430095
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661266768525512906,
            "last_ns": 1661267008750735473,
            "hull_s": 240.225222567
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267068861823949,
            "last_ns": 1661267308496116589,
            "hull_s": 239.63429264
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.976576937,
            59.947742623,
            60.026728539,
            60.274174468,
            60.111088476,
            59.617637879,
            60.010971863,
            60.166320243,
            59.839362655
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/productcatalogservice-668d5f85fb-jhwx9_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661266768561175486,
            "last_ns": 1661267008788657322,
            "hull_s": 240.227481836
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267068923090527,
            "last_ns": 1661267308532121704,
            "hull_s": 239.609031177
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.980049078,
            59.935492599,
            60.030381884,
            60.281558275,
            60.134433205,
            59.595894781,
            60.013517343,
            60.16993499,
            59.829684063
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661266768595035439,
            "last_ns": 1661267008823388822,
            "hull_s": 240.228353383
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267068984294872,
            "last_ns": 1661267308577683260,
            "hull_s": 239.593388388
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.993901933,
            59.91492788,
            60.030029863,
            60.289493707,
            60.16090605,
            59.656172257,
            59.936900749,
            60.162963405,
            59.837351977
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661266768628333158,
            "last_ns": 1661267008857492855,
            "hull_s": 240.229159697
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267069018181753,
            "last_ns": 1661267308613600584,
            "hull_s": 239.595418831
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.020381818,
            59.888366445,
            60.026725159,
            60.293686275,
            60.160688898,
            59.727785054,
            59.865034322,
            60.163421112,
            59.839178343
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/15_04_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 24897,
                "seconds_with_rows": 61,
                "first_ns": 1661267007763036044,
                "last_ns": 1661267067999774556,
                "hull_s": 60.236738512
              },
              "A": {
                "rows": 69,
                "seconds_with_rows": 1,
                "first_ns": 1661267068000588555,
                "last_ns": 1661267068086541568,
                "hull_s": 0.085953013
              }
            },
            "end_split": {
              "N": {
                "rows": 24883,
                "seconds_with_rows": 61,
                "first_ns": 1661267007784122112,
                "last_ns": 1661267067996108364,
                "hull_s": 60.211986252
              },
              "A": {
                "rows": 83,
                "seconds_with_rows": 1,
                "first_ns": 1661267068001058191,
                "last_ns": 1661267068089840964,
                "hull_s": 0.088782773
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/15_05_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 172,
                "seconds_with_rows": 1,
                "first_ns": 1661267067642736653,
                "last_ns": 1661267067999774556,
                "hull_s": 0.357037903
              },
              "A": {
                "rows": 7330,
                "seconds_with_rows": 60,
                "first_ns": 1661267068000002200,
                "last_ns": 1661267127097068619,
                "hull_s": 59.097066419
              }
            },
            "end_split": {
              "N": {
                "rows": 154,
                "seconds_with_rows": 1,
                "first_ns": 1661267067646121472,
                "last_ns": 1661267067996108364,
                "hull_s": 0.349986892
              },
              "A": {
                "rows": 7348,
                "seconds_with_rows": 60,
                "first_ns": 1661267068000993400,
                "last_ns": 1661267127100029550,
                "hull_s": 59.09903615
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/15_06_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 6682,
                "seconds_with_rows": 60,
                "first_ns": 1661267128311456738,
                "last_ns": 1661267187460794255,
                "hull_s": 59.149337517
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 6682,
                "seconds_with_rows": 60,
                "first_ns": 1661267128311705971,
                "last_ns": 1661267187463459480,
                "hull_s": 59.151753509
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 25069,
            "seconds_with_rows": 61,
            "first_ns": 1661267007763036044,
            "last_ns": 1661267067999774556,
            "hull_s": 60.236738512
          },
          "A": {
            "rows": 14081,
            "seconds_with_rows": 120,
            "first_ns": 1661267068000002200,
            "last_ns": 1661267187460794255,
            "hull_s": 119.460792055
          }
        },
        "end_split": {
          "N": {
            "rows": 25037,
            "seconds_with_rows": 61,
            "first_ns": 1661267007784122112,
            "last_ns": 1661267067996108364,
            "hull_s": 60.211986252
          },
          "A": {
            "rows": 14113,
            "seconds_with_rows": 120,
            "first_ns": 1661267068000993400,
            "last_ns": 1661267187463459480,
            "hull_s": 119.46246608
          }
        },
        "straddle_t": 32,
        "duplicate_keys": 226,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/log/15_04_log.csv",
            "N": {
              "rows": 26752,
              "seconds_with_rows": 61,
              "first_ns": 1661267007763068230,
              "last_ns": 1661267067999580000,
              "hull_s": 60.23651177
            },
            "A": {
              "rows": 80,
              "seconds_with_rows": 1,
              "first_ns": 1661267068000601886,
              "last_ns": 1661267068089793604,
              "hull_s": 0.089191718
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/15_05_log.csv",
            "N": {
              "rows": 188,
              "seconds_with_rows": 1,
              "first_ns": 1661267067642762420,
              "last_ns": 1661267067999580000,
              "hull_s": 0.35681758
            },
            "A": {
              "rows": 10074,
              "seconds_with_rows": 60,
              "first_ns": 1661267068000233868,
              "last_ns": 1661267127099997153,
              "hull_s": 59.099763285
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/15_06_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 9313,
              "seconds_with_rows": 60,
              "first_ns": 1661267128311510869,
              "last_ns": 1661267187463422586,
              "hull_s": 59.151911717
            }
          }
        ],
        "N": {
          "rows": 26940,
          "seconds_with_rows": 61,
          "first_ns": 1661267007763068230,
          "last_ns": 1661267067999580000,
          "hull_s": 60.23651177
        },
        "A": {
          "rows": 19467,
          "seconds_with_rows": 120,
          "first_ns": 1661267068000233868,
          "last_ns": 1661267187463422586,
          "hull_s": 119.463188718
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 46407,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.778e-06,
            1.455069391
          ],
          "relative_end_s": [
            -1.455058755,
            0.022376284
          ]
        }
      },
      "previous_inject_time_ns": 1661266555000000000,
      "previous_gap_s": 513.0,
      "next_gap_s": 501.0,
      "elapsed_s": 0.9690000000009604
    },
    {
      "case": "OB|recommendationservice|cpu_consumed|2022-08-22 07:10:43",
      "view": "main",
      "t_ns": 1661152243000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151979713219724,
            "last_ns": 1661152219756135321,
            "hull_s": 240.042915597
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152279748020803,
            "last_ns": 1661152519742623624,
            "hull_s": 239.994602821
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.023121121,
            60.007589541,
            60.13953872,
            59.872666215,
            59.991885482,
            59.988136756,
            59.96956974,
            60.006604645,
            60.03029168
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151979751208494,
            "last_ns": 1661152219923068367,
            "hull_s": 240.171859873
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152279788216626,
            "last_ns": 1661152519782019359,
            "hull_s": 239.993802733
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.051798573,
            60.00883442,
            60.122857431,
            59.988369449,
            59.865148259,
            59.986336638,
            59.981348497,
            60.001443862,
            60.024673736
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151979813490862,
            "last_ns": 1661152220009796009,
            "hull_s": 240.196305147
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152280020046632,
            "last_ns": 1661152519839084273,
            "hull_s": 239.819037641
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.151043256,
            59.93408892,
            60.090601506,
            60.020571465,
            60.010250623,
            59.816955638,
            59.992973778,
            60.005621845,
            60.00348638
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151979847234847,
            "last_ns": 1661152220076602240,
            "hull_s": 240.229367393
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152280090655411,
            "last_ns": 1661152519876628864,
            "hull_s": 239.785973453
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.167383332,
            59.93155834,
            60.072486972,
            60.057938749,
            60.014053171,
            59.813872111,
            59.992365301,
            59.993833764,
            59.985902277
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151979874573094,
            "last_ns": 1661152220134844318,
            "hull_s": 240.260271224
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152280132564067,
            "last_ns": 1661152519904262638,
            "hull_s": 239.771698571
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.173524986,
            59.957895657,
            60.034475459,
            60.094375122,
            59.997719749,
            59.805576133,
            60.021793946,
            59.963633765,
            59.980694727
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151979675310848,
            "last_ns": 1661152219685660849,
            "hull_s": 240.010350001
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152279703980821,
            "last_ns": 1661152519683909177,
            "hull_s": 239.979928356
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.019702454,
            59.990490356,
            60.039822517,
            59.960334674,
            60.018319972,
            59.985247058,
            59.986415577,
            59.992911057,
            60.015354664
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151979922225857,
            "last_ns": 1661152220179018986,
            "hull_s": 240.256793129
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152280207564388,
            "last_ns": 1661152519946096060,
            "hull_s": 239.738531672
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.184086052,
            59.974314638,
            59.994844112,
            60.103548327,
            60.028545402,
            59.913690351,
            59.911504628,
            59.946531634,
            59.966805059
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151979961767258,
            "last_ns": 1661152220209862619,
            "hull_s": 240.248095361
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152280273102479,
            "last_ns": 1661152519976959585,
            "hull_s": 239.703857106
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.187080887,
            59.990431556,
            59.982902391,
            60.087680527,
            60.06323986,
            59.880533904,
            60.000928323,
            59.8722257,
            59.950169179
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/productcatalogservice-668d5f85fb-wckp8_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151979992961332,
            "last_ns": 1661152220264361174,
            "hull_s": 240.271399842
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152280342265930,
            "last_ns": 1661152520006819750,
            "hull_s": 239.66455382
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.20342949,
            59.974818481,
            59.98098168,
            60.112170191,
            60.077904756,
            59.842908062,
            60.036420057,
            59.845256442,
            59.939969259
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151980022305161,
            "last_ns": 1661152220306970791,
            "hull_s": 240.28466563
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152280403686492,
            "last_ns": 1661152520032642858,
            "hull_s": 239.628956366
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.227537275,
            59.948472058,
            59.978778977,
            60.12987732,
            60.096715701,
            59.808638906,
            60.057821539,
            59.830941264,
            59.931554657
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151980054761608,
            "last_ns": 1661152220341959116,
            "hull_s": 240.287197508
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152280466323317,
            "last_ns": 1661152520063189891,
            "hull_s": 239.596866574
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.237374266,
            59.936315393,
            59.978083049,
            60.1354248,
            60.124364201,
            59.773843713,
            60.064479704,
            59.836842918,
            59.921700239
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/07_10_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 17077,
                "seconds_with_rows": 66,
                "first_ns": 1661152158984489303,
                "last_ns": 1661152223790440448,
                "hull_s": 64.805951145
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "end_split": {
              "N": {
                "rows": 17077,
                "seconds_with_rows": 66,
                "first_ns": 1661152158988283136,
                "last_ns": 1661152223792908013,
                "hull_s": 64.804624877
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/07_11_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 4696,
                "seconds_with_rows": 27,
                "first_ns": 1661152216051059589,
                "last_ns": 1661152242750234222,
                "hull_s": 26.699174633
              },
              "A": {
                "rows": 6923,
                "seconds_with_rows": 40,
                "first_ns": 1661152243050802144,
                "last_ns": 1661152282861932969,
                "hull_s": 39.811130825
              }
            },
            "end_split": {
              "N": {
                "rows": 4659,
                "seconds_with_rows": 27,
                "first_ns": 1661152216057724654,
                "last_ns": 1661152242747940140,
                "hull_s": 26.690215486
              },
              "A": {
                "rows": 6960,
                "seconds_with_rows": 40,
                "first_ns": 1661152243049168232,
                "last_ns": 1661152282864259242,
                "hull_s": 39.81509101
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/07_12_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 12657,
                "seconds_with_rows": 70,
                "first_ns": 1661152274943484432,
                "last_ns": 1661152343272189822,
                "hull_s": 68.32870539
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 12657,
                "seconds_with_rows": 70,
                "first_ns": 1661152274956351776,
                "last_ns": 1661152343274744344,
                "hull_s": 68.318392568
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 21773,
            "seconds_with_rows": 85,
            "first_ns": 1661152158984489303,
            "last_ns": 1661152242750234222,
            "hull_s": 83.765744919
          },
          "A": {
            "rows": 19580,
            "seconds_with_rows": 101,
            "first_ns": 1661152243050802144,
            "last_ns": 1661152343272189822,
            "hull_s": 100.221387678
          }
        },
        "end_split": {
          "N": {
            "rows": 21736,
            "seconds_with_rows": 85,
            "first_ns": 1661152158988283136,
            "last_ns": 1661152242747940140,
            "hull_s": 83.759657004
          },
          "A": {
            "rows": 19617,
            "seconds_with_rows": 101,
            "first_ns": 1661152243049168232,
            "last_ns": 1661152343274744344,
            "hull_s": 100.225576112
          }
        },
        "straddle_t": 37,
        "duplicate_keys": 1411,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-22/log/07_10_log.csv",
            "N": {
              "rows": 18301,
              "seconds_with_rows": 66,
              "first_ns": 1661152158984552439,
              "last_ns": 1661152223792870349,
              "hull_s": 64.80831791
            },
            "A": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/log/07_11_log.csv",
            "N": {
              "rows": 5073,
              "seconds_with_rows": 27,
              "first_ns": 1661152216051095406,
              "last_ns": 1661152242749822000,
              "hull_s": 26.698726594
            },
            "A": {
              "rows": 7357,
              "seconds_with_rows": 40,
              "first_ns": 1661152243054620719,
              "last_ns": 1661152282864231805,
              "hull_s": 39.809611086
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/log/07_12_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 13492,
              "seconds_with_rows": 70,
              "first_ns": 1661152274943552253,
              "last_ns": 1661152343274713782,
              "hull_s": 68.331161529
            }
          }
        ],
        "N": {
          "rows": 23374,
          "seconds_with_rows": 85,
          "first_ns": 1661152158984552439,
          "last_ns": 1661152242749822000,
          "hull_s": 83.765269561
        },
        "A": {
          "rows": 20849,
          "seconds_with_rows": 101,
          "first_ns": 1661152243054620719,
          "last_ns": 1661152343274713782,
          "hull_s": 100.220093063
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 44223,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.676e-06,
            5.745277666
          ],
          "relative_end_s": [
            -5.745272941,
            0.018596316
          ]
        }
      },
      "previous_inject_time_ns": 1661151685000000000,
      "previous_gap_s": 558.0,
      "next_gap_s": 432.0,
      "elapsed_s": 1.0780000000013388
    },
    {
      "case": "OB|recommendationservice|cpu_consumed|2022-08-23 15:29:49",
      "view": "main",
      "t_ns": 1661268589000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268328231467190,
            "last_ns": 1661268568280670367,
            "hull_s": 240.049203177
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268628285094810,
            "last_ns": 1661268868260618485,
            "hull_s": 239.975523675
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.10425112,
            59.908155528,
            60.02510647,
            60.011690059,
            60.004424443,
            60.007643947,
            60.000845869,
            59.976707666,
            59.990326193
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268328263164634,
            "last_ns": 1661268568353194288,
            "hull_s": 240.090029654
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268628329652512,
            "last_ns": 1661268868324682758,
            "hull_s": 239.995030246
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.150489373,
            59.871276008,
            60.023896214,
            60.044368059,
            59.976458224,
            60.034783634,
            59.978801737,
            59.96435266,
            60.017092215
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268328318641940,
            "last_ns": 1661268568439528868,
            "hull_s": 240.120886928
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268628391273887,
            "last_ns": 1661268868386887218,
            "hull_s": 239.995613331
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.181525836,
            59.85235171,
            60.033633064,
            60.053376318,
            59.951745019,
            60.063242677,
            60.08877192,
            59.828971085,
            60.014627649
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268328349578383,
            "last_ns": 1661268568487305369,
            "hull_s": 240.137726986
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268628428204073,
            "last_ns": 1661268868432239514,
            "hull_s": 240.004035441
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.186836075,
            59.87535087,
            60.015490792,
            60.060049249,
            59.940898704,
            60.10077427,
            60.051670323,
            59.85513169,
            59.996459158
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268328375945140,
            "last_ns": 1661268568532899037,
            "hull_s": 240.156953897
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268628455725056,
            "last_ns": 1661268868471439837,
            "hull_s": 240.015714781
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.186687343,
            59.898448579,
            60.003924079,
            60.067893896,
            59.922826019,
            60.124464509,
            60.028029641,
            59.884290069,
            59.978930562
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268328201083725,
            "last_ns": 1661268568215970260,
            "hull_s": 240.014886535
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268628225259674,
            "last_ns": 1661268868215134679,
            "hull_s": 239.989875005
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.994969827,
            60.002963209,
            60.017088703,
            59.999864796,
            60.009289414,
            59.996517254,
            59.999987744,
            60.000668622,
            59.992701385
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268328427527933,
            "last_ns": 1661268568608664896,
            "hull_s": 240.181136963
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268628515384891,
            "last_ns": 1661268868542684058,
            "hull_s": 240.027299167
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.190589327,
            59.929438583,
            59.990419988,
            60.070689065,
            59.906719995,
            60.130539044,
            60.023149807,
            59.903478094,
            59.970132222
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268328455581750,
            "last_ns": 1661268568668727946,
            "hull_s": 240.213146196
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268628547404057,
            "last_ns": 1661268868581520961,
            "hull_s": 240.034116904
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.195083626,
            60.095252692,
            59.824348622,
            60.098461256,
            59.878676111,
            60.157943969,
            59.99736268,
            59.935210544,
            59.943599711
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/productcatalogservice-668d5f85fb-jhwx9_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268328487969142,
            "last_ns": 1661268568740134313,
            "hull_s": 240.252165171
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268628579796869,
            "last_ns": 1661268868621072496,
            "hull_s": 240.041275627
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.19701741,
            60.133558935,
            59.795854783,
            60.125734043,
            59.839662556,
            60.176478017,
            59.977791691,
            59.981156473,
            59.905849446
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268328517208605,
            "last_ns": 1661268568795703741,
            "hull_s": 240.278495136
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268628609352804,
            "last_ns": 1661268868657006521,
            "hull_s": 240.047653717
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.199189017,
            60.139193744,
            59.793470725,
            60.14664165,
            59.813649063,
            60.203469445,
            59.976558245,
            59.991891611,
            59.875734416
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268328549154500,
            "last_ns": 1661268568836064516,
            "hull_s": 240.286910016
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661268628640541060,
            "last_ns": 1661268868707294944,
            "hull_s": 240.066753884
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.193226365,
            60.147779506,
            59.797276249,
            60.148627896,
            59.804476544,
            60.247337675,
            59.956745142,
            60.051744266,
            59.810926801
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/15_29_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 24489,
                "seconds_with_rows": 62,
                "first_ns": 1661268507028346275,
                "last_ns": 1661268568508184930,
                "hull_s": 61.479838655
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "end_split": {
              "N": {
                "rows": 24489,
                "seconds_with_rows": 62,
                "first_ns": 1661268507092409344,
                "last_ns": 1661268568512553381,
                "hull_s": 61.420144037
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/15_30_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 8403,
                "seconds_with_rows": 22,
                "first_ns": 1661268567882590046,
                "last_ns": 1661268588794955439,
                "hull_s": 20.912365393
              },
              "A": {
                "rows": 7647,
                "seconds_with_rows": 43,
                "first_ns": 1661268589156784595,
                "last_ns": 1661268631901106176,
                "hull_s": 42.744321581
              }
            },
            "end_split": {
              "N": {
                "rows": 8403,
                "seconds_with_rows": 22,
                "first_ns": 1661268567888224768,
                "last_ns": 1661268588797606886,
                "hull_s": 20.909382118
              },
              "A": {
                "rows": 7647,
                "seconds_with_rows": 43,
                "first_ns": 1661268589160828928,
                "last_ns": 1661268631903123945,
                "hull_s": 42.742295017
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/15_31_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 12458,
                "seconds_with_rows": 71,
                "first_ns": 1661268623768255634,
                "last_ns": 1661268693375508067,
                "hull_s": 69.607252433
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 12458,
                "seconds_with_rows": 71,
                "first_ns": 1661268623771418081,
                "last_ns": 1661268693378149257,
                "hull_s": 69.606731176
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 32892,
            "seconds_with_rows": 82,
            "first_ns": 1661268507028346275,
            "last_ns": 1661268588794955439,
            "hull_s": 81.766609164
          },
          "A": {
            "rows": 20105,
            "seconds_with_rows": 105,
            "first_ns": 1661268589156784595,
            "last_ns": 1661268693375508067,
            "hull_s": 104.218723472
          }
        },
        "end_split": {
          "N": {
            "rows": 32892,
            "seconds_with_rows": 82,
            "first_ns": 1661268507092409344,
            "last_ns": 1661268588797606886,
            "hull_s": 81.705197542
          },
          "A": {
            "rows": 20105,
            "seconds_with_rows": 105,
            "first_ns": 1661268589160828928,
            "last_ns": 1661268693378149257,
            "hull_s": 104.217320329
          }
        },
        "straddle_t": 0,
        "duplicate_keys": 651,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/log/15_29_log.csv",
            "N": {
              "rows": 26551,
              "seconds_with_rows": 62,
              "first_ns": 1661268507028379559,
              "last_ns": 1661268568512527908,
              "hull_s": 61.484148349
            },
            "A": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/15_30_log.csv",
            "N": {
              "rows": 9303,
              "seconds_with_rows": 22,
              "first_ns": 1661268567882625577,
              "last_ns": 1661268588797576360,
              "hull_s": 20.914950783
            },
            "A": {
              "rows": 8084,
              "seconds_with_rows": 43,
              "first_ns": 1661268589156835247,
              "last_ns": 1661268631903095062,
              "hull_s": 42.746259815
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/15_31_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 13305,
              "seconds_with_rows": 71,
              "first_ns": 1661268623768303776,
              "last_ns": 1661268693378122828,
              "hull_s": 69.609819052
            }
          }
        ],
        "N": {
          "rows": 35854,
          "seconds_with_rows": 82,
          "first_ns": 1661268507028379559,
          "last_ns": 1661268588797576360,
          "hull_s": 81.769196801
        },
        "A": {
          "rows": 21389,
          "seconds_with_rows": 105,
          "first_ns": 1661268589156835247,
          "last_ns": 1661268693378122828,
          "hull_s": 104.221287581
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 57243,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.718e-06,
            5.768891406
          ],
          "relative_end_s": [
            -5.768877316,
            0.010390281
          ]
        }
      },
      "previous_inject_time_ns": 1661268101000000000,
      "previous_gap_s": 488.0,
      "next_gap_s": 543.0,
      "elapsed_s": 1.1869999999980791
    },
    {
      "case": "OB|recommendationservice|network_delay|2022-08-22 06:52:56",
      "view": "main",
      "t_ns": 1661151176000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661150899684579051,
            "last_ns": 1661151139723915095,
            "hull_s": 240.039336044
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151199739064206,
            "last_ns": 1661151439778158424,
            "hull_s": 240.039094218
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.045325552,
            60.121339539,
            59.835978366,
            60.036692587,
            60.015149111,
            59.985913902,
            60.018393298,
            59.97060939,
            60.064177628
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661150899718903341,
            "last_ns": 1661151139762027880,
            "hull_s": 240.043124539
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151199807218799,
            "last_ns": 1661151439851217640,
            "hull_s": 240.043998841
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.068416899,
            60.158573957,
            59.791776045,
            60.024357638,
            60.045190919,
            59.962036505,
            60.011565058,
            59.968994399,
            60.101402879
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661150899774562667,
            "last_ns": 1661151139825401020,
            "hull_s": 240.050838353
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151199892150163,
            "last_ns": 1661151439941405980,
            "hull_s": 240.049255817
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.083690067,
            60.185007808,
            59.875220323,
            59.906920155,
            60.066749143,
            59.945198022,
            59.998580866,
            59.967554054,
            60.137922875
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661150899807374591,
            "last_ns": 1661151139876789695,
            "hull_s": 240.069415104
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151199962243948,
            "last_ns": 1661151439992482163,
            "hull_s": 240.030238215
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.113764643,
            60.196751216,
            59.910281328,
            59.848617917,
            60.085454253,
            59.928266769,
            60.0001343,
            59.94770732,
            60.154129826
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661150899832865190,
            "last_ns": 1661151139909643128,
            "hull_s": 240.076777938
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151200024703896,
            "last_ns": 1661151440028431585,
            "hull_s": 240.003727689
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.147477602,
            60.194817891,
            59.900538091,
            59.833944354,
            60.115060768,
            59.914894968,
            59.995359583,
            59.93138821,
            60.162084928
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661150899654110568,
            "last_ns": 1661151139684178950,
            "hull_s": 240.030068382
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151199688579967,
            "last_ns": 1661151439698106011,
            "hull_s": 240.009526044
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.011730162,
            59.989662295,
            59.994113304,
            60.034562621,
            60.004401017,
            59.99361871,
            60.004728457,
            59.9920457,
            60.019133177
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661150899871465811,
            "last_ns": 1661151139964800946,
            "hull_s": 240.093335135
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151200105318934,
            "last_ns": 1661151440094364103,
            "hull_s": 239.989045169
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.16732434,
            60.200909936,
            59.89125301,
            59.833847849,
            60.140517988,
            59.885755402,
            59.988539286,
            59.933200119,
            60.181550362
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661150899898737757,
            "last_ns": 1661151140016395864,
            "hull_s": 240.117658107
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151200171783374,
            "last_ns": 1661151440149385441,
            "hull_s": 239.977602067
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.169747726,
            60.225846412,
            59.876780251,
            59.845283718,
            60.15538751,
            59.855542176,
            59.990686891,
            59.928376522,
            60.202996478
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/productcatalogservice-668d5f85fb-wckp8_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661150899931951287,
            "last_ns": 1661151140186994291,
            "hull_s": 240.255043004
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151200238103474,
            "last_ns": 1661151440192729512,
            "hull_s": 239.954626038
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.170655439,
            60.246796248,
            59.863916448,
            59.973674869,
            60.051109183,
            59.828216497,
            59.992793139,
            59.920582536,
            60.213033866
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661150899959403456,
            "last_ns": 1661151140224056163,
            "hull_s": 240.264652707
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151200300690464,
            "last_ns": 1661151440232012152,
            "hull_s": 239.931321688
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.170456489,
            60.263872621,
            59.854999817,
            59.97532378,
            60.076634301,
            59.795985498,
            60.001339815,
            59.90990304,
            60.224093335
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661150899993148633,
            "last_ns": 1661151140257113145,
            "hull_s": 240.263964512
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151200366560478,
            "last_ns": 1661151440273318169,
            "hull_s": 239.906757691
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.167887273,
            60.281148633,
            59.839473246,
            59.97545536,
            60.109447333,
            59.767431049,
            60.00676769,
            59.897429281,
            60.235129671
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/06_52_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 23935,
                "seconds_with_rows": 61,
                "first_ns": 1661151079047829372,
                "last_ns": 1661151139511034055,
                "hull_s": 60.463204683
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "end_split": {
              "N": {
                "rows": 23935,
                "seconds_with_rows": 61,
                "first_ns": 1661151079057204200,
                "last_ns": 1661151139513729286,
                "hull_s": 60.456525086
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/06_53_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 13849,
                "seconds_with_rows": 37,
                "first_ns": 1661151139451395192,
                "last_ns": 1661151175999132845,
                "hull_s": 36.547737653
              },
              "A": {
                "rows": 8103,
                "seconds_with_rows": 24,
                "first_ns": 1661151176000690111,
                "last_ns": 1661151199789255936,
                "hull_s": 23.788565825
              }
            },
            "end_split": {
              "N": {
                "rows": 13821,
                "seconds_with_rows": 37,
                "first_ns": 1661151139458246960,
                "last_ns": 1661151175997086532,
                "hull_s": 36.538839572
              },
              "A": {
                "rows": 8131,
                "seconds_with_rows": 24,
                "first_ns": 1661151176000693128,
                "last_ns": 1661151199793604469,
                "hull_s": 23.792911341
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/06_54_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 20207,
                "seconds_with_rows": 63,
                "first_ns": 1661151198813907587,
                "last_ns": 1661151260216302481,
                "hull_s": 61.402394894
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 20207,
                "seconds_with_rows": 63,
                "first_ns": 1661151198846673179,
                "last_ns": 1661151260218643111,
                "hull_s": 61.371969932
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 37784,
            "seconds_with_rows": 97,
            "first_ns": 1661151079047829372,
            "last_ns": 1661151175999132845,
            "hull_s": 96.951303473
          },
          "A": {
            "rows": 28310,
            "seconds_with_rows": 85,
            "first_ns": 1661151176000690111,
            "last_ns": 1661151260216302481,
            "hull_s": 84.21561237
          }
        },
        "end_split": {
          "N": {
            "rows": 37756,
            "seconds_with_rows": 97,
            "first_ns": 1661151079057204200,
            "last_ns": 1661151175997086532,
            "hull_s": 96.939882332
          },
          "A": {
            "rows": 28338,
            "seconds_with_rows": 85,
            "first_ns": 1661151176000693128,
            "last_ns": 1661151260218643111,
            "hull_s": 84.217949983
          }
        },
        "straddle_t": 28,
        "duplicate_keys": 223,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-22/log/06_52_log.csv",
            "N": {
              "rows": 25648,
              "seconds_with_rows": 61,
              "first_ns": 1661151079047873077,
              "last_ns": 1661151139513703272,
              "hull_s": 60.465830195
            },
            "A": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/log/06_53_log.csv",
            "N": {
              "rows": 14858,
              "seconds_with_rows": 37,
              "first_ns": 1661151139451430889,
              "last_ns": 1661151175996335434,
              "hull_s": 36.544904545
            },
            "A": {
              "rows": 8636,
              "seconds_with_rows": 24,
              "first_ns": 1661151176000748934,
              "last_ns": 1661151199793516285,
              "hull_s": 23.792767351
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/log/06_54_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 21787,
              "seconds_with_rows": 63,
              "first_ns": 1661151198813955615,
              "last_ns": 1661151260218609315,
              "hull_s": 61.4046537
            }
          }
        ],
        "N": {
          "rows": 40506,
          "seconds_with_rows": 97,
          "first_ns": 1661151079047873077,
          "last_ns": 1661151175996335434,
          "hull_s": 96.948462357
        },
        "A": {
          "rows": 30423,
          "seconds_with_rows": 85,
          "first_ns": 1661151176000748934,
          "last_ns": 1661151260218609315,
          "hull_s": 84.217860381
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 70929,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.712e-06,
            1.702942603
          ],
          "relative_end_s": [
            -1.702955791,
            0.018475046
          ]
        }
      },
      "previous_inject_time_ns": 1661150139000000000,
      "previous_gap_s": 1037.0,
      "next_gap_s": 509.0,
      "elapsed_s": 1.5159999999996217
    },
    {
      "case": "OB|recommendationservice|network_delay|2022-08-23 15:12:49",
      "view": "main",
      "t_ns": 1661267569000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267308228472744,
            "last_ns": 1661267548283452183,
            "hull_s": 240.054979439
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267608231896551,
            "last_ns": 1661267848292555491,
            "hull_s": 240.06065894
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.147024189,
            59.869473339,
            59.99733284,
            60.041149071,
            59.948444368,
            60.023586376,
            60.150972856,
            59.854033839,
            60.032065869
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267308267016721,
            "last_ns": 1661267548351502903,
            "hull_s": 240.084486182
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267608267534448,
            "last_ns": 1661267848365817605,
            "hull_s": 240.098283157
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.175176793,
            59.865476165,
            59.975813936,
            60.068019288,
            59.916031545,
            60.03627082,
            60.154632411,
            59.868901214,
            60.038478712
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267308329043756,
            "last_ns": 1661267548437937220,
            "hull_s": 240.108893464
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267608344379574,
            "last_ns": 1661267848467692407,
            "hull_s": 240.123312833
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.164843284,
            59.910646243,
            59.94805346,
            60.085350477,
            59.906442354,
            60.053352443,
            60.125358982,
            59.898972028,
            60.04562938
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267308362730972,
            "last_ns": 1661267548495875539,
            "hull_s": 240.133144567
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267608415351517,
            "last_ns": 1661267848519908361,
            "hull_s": 240.104556844
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.167669315,
            59.957311542,
            59.909070092,
            60.099093618,
            59.919475978,
            60.023927622,
            60.125460219,
            59.933971449,
            60.021197554
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267308392920779,
            "last_ns": 1661267548555684298,
            "hull_s": 240.162763519
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267608480087334,
            "last_ns": 1661267848568383239,
            "hull_s": 240.088295905
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.163844879,
            60.007717087,
            59.862665243,
            60.12853631,
            59.924403036,
            59.991753925,
            60.124812037,
            60.069075009,
            59.902654934
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267308192218107,
            "last_ns": 1661267548219154553,
            "hull_s": 240.026936446
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267608195438437,
            "last_ns": 1661267848220123720,
            "hull_s": 240.024685283
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.015862171,
            59.989860278,
            59.998303977,
            60.02291002,
            59.976283884,
            60.013751649,
            60.03087108,
            59.968220882,
            60.011841672
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267308454616026,
            "last_ns": 1661267548626851279,
            "hull_s": 240.172235253
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267608564827841,
            "last_ns": 1661267848660831465,
            "hull_s": 240.096003624
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.153261756,
            60.161300242,
            59.720683823,
            60.136989432,
            59.937976562,
            59.977275145,
            60.117793558,
            60.06934911,
            59.931585811
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267308496116589,
            "last_ns": 1661267548664118740,
            "hull_s": 240.168002151
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267608598011790,
            "last_ns": 1661267848727300792,
            "hull_s": 240.129289002
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.137901071,
            60.193635117,
            59.697586181,
            60.138879782,
            59.93389305,
            60.000524085,
            60.096641632,
            60.0652612,
            59.966862085
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/productcatalogservice-668d5f85fb-jhwx9_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267308532121704,
            "last_ns": 1661267548696825914,
            "hull_s": 240.16470421
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267608631820768,
            "last_ns": 1661267848804177240,
            "hull_s": 240.172356472
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.131009703,
            60.199701684,
            59.700705732,
            60.133287091,
            59.934994854,
            60.031215608,
            60.071679612,
            60.071196367,
            59.998264885
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267308577683260,
            "last_ns": 1661267548731133194,
            "hull_s": 240.153449934
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267608669467533,
            "last_ns": 1661267848867057933,
            "hull_s": 240.1975904
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.112181756,
            60.216852813,
            59.692741154,
            60.131674211,
            59.938334339,
            60.058535128,
            60.036853511,
            60.075653457,
            60.026548304
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267308613600584,
            "last_ns": 1661267548762045774,
            "hull_s": 240.14844519
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661267608706224823,
            "last_ns": 1661267849024230944,
            "hull_s": 240.318006121
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.099711657,
            60.231105171,
            59.687576857,
            60.130051505,
            59.944179049,
            60.085000895,
            60.021186277,
            60.071540849,
            60.1402781
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/15_12_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 22979,
                "seconds_with_rows": 61,
                "first_ns": 1661267487959838555,
                "last_ns": 1661267547968740352,
                "hull_s": 60.008901797
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "end_split": {
              "N": {
                "rows": 22979,
                "seconds_with_rows": 61,
                "first_ns": 1661267487962475264,
                "last_ns": 1661267547970647494,
                "hull_s": 60.00817223
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/15_13_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 9122,
                "seconds_with_rows": 22,
                "first_ns": 1661267547891148448,
                "last_ns": 1661267568971574150,
                "hull_s": 21.080425702
              },
              "A": {
                "rows": 14160,
                "seconds_with_rows": 40,
                "first_ns": 1661267569111832982,
                "last_ns": 1661267608694692864,
                "hull_s": 39.582859882
              }
            },
            "end_split": {
              "N": {
                "rows": 9122,
                "seconds_with_rows": 22,
                "first_ns": 1661267547894473472,
                "last_ns": 1661267568974732755,
                "hull_s": 21.080259283
              },
              "A": {
                "rows": 14160,
                "seconds_with_rows": 40,
                "first_ns": 1661267569117429665,
                "last_ns": 1661267608701652881,
                "hull_s": 39.584223216
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/15_14_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 21458,
                "seconds_with_rows": 62,
                "first_ns": 1661267607375684771,
                "last_ns": 1661267668895322880,
                "hull_s": 61.519638109
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 21458,
                "seconds_with_rows": 62,
                "first_ns": 1661267607509083400,
                "last_ns": 1661267668900396414,
                "hull_s": 61.391313014
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 32101,
            "seconds_with_rows": 82,
            "first_ns": 1661267487959838555,
            "last_ns": 1661267568971574150,
            "hull_s": 81.011735595
          },
          "A": {
            "rows": 35618,
            "seconds_with_rows": 100,
            "first_ns": 1661267569111832982,
            "last_ns": 1661267668895322880,
            "hull_s": 99.783489898
          }
        },
        "end_split": {
          "N": {
            "rows": 32101,
            "seconds_with_rows": 82,
            "first_ns": 1661267487962475264,
            "last_ns": 1661267568974732755,
            "hull_s": 81.012257491
          },
          "A": {
            "rows": 35618,
            "seconds_with_rows": 100,
            "first_ns": 1661267569117429665,
            "last_ns": 1661267668900396414,
            "hull_s": 99.782966749
          }
        },
        "straddle_t": 0,
        "duplicate_keys": 307,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/log/15_12_log.csv",
            "N": {
              "rows": 24629,
              "seconds_with_rows": 61,
              "first_ns": 1661267487959872934,
              "last_ns": 1661267547970619849,
              "hull_s": 60.010746915
            },
            "A": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/15_13_log.csv",
            "N": {
              "rows": 9738,
              "seconds_with_rows": 22,
              "first_ns": 1661267547891190559,
              "last_ns": 1661267568974704531,
              "hull_s": 21.083513972
            },
            "A": {
              "rows": 15056,
              "seconds_with_rows": 40,
              "first_ns": 1661267569111880996,
              "last_ns": 1661267608701600379,
              "hull_s": 39.589719383
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/15_14_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 22944,
              "seconds_with_rows": 62,
              "first_ns": 1661267607375737620,
              "last_ns": 1661267668900361615,
              "hull_s": 61.524623995
            }
          }
        ],
        "N": {
          "rows": 34367,
          "seconds_with_rows": 82,
          "first_ns": 1661267487959872934,
          "last_ns": 1661267568974704531,
          "hull_s": 81.014831597
        },
        "A": {
          "rows": 38000,
          "seconds_with_rows": 100,
          "first_ns": 1661267569111880996,
          "last_ns": 1661267668900361615,
          "hull_s": 99.788480619
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 72367,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.471e-06,
            1.449726642
          ],
          "relative_end_s": [
            -1.449740096,
            0.012953535
          ]
        }
      },
      "previous_inject_time_ns": 1661267068000000000,
      "previous_gap_s": 501.0,
      "next_gap_s": 532.0,
      "elapsed_s": 1.4840000000003783
    },
    {
      "case": "OB|shippingservice|cpu_consumed|2022-08-23 15:56:24",
      "view": "main",
      "t_ns": 1661270184000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269888256152540,
            "last_ns": 1661270128361260608,
            "hull_s": 240.105108068
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661270188281715359,
            "last_ns": 1661270428308560720,
            "hull_s": 240.026845361
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.030629103,
            59.975361382,
            59.995915169,
            60.103202414,
            59.920454751,
            60.028369103,
            59.957402069,
            60.044661726,
            59.996412463
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269888317092988,
            "last_ns": 1661270128414763514,
            "hull_s": 240.097670526
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661270188531712588,
            "last_ns": 1661270428346990332,
            "hull_s": 239.815277744
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.013456358,
            59.98184093,
            59.985213617,
            60.117159621,
            60.116949074,
            59.954136798,
            59.820750328,
            60.059124208,
            59.98126641
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269888419849657,
            "last_ns": 1661270128494667356,
            "hull_s": 240.074817699
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661270188606517308,
            "last_ns": 1661270428418814752,
            "hull_s": 239.812297444
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.974080503,
            59.997945727,
            59.986149521,
            60.116641948,
            60.111849952,
            59.974833222,
            59.805029206,
            60.06159733,
            59.970837686
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269888645159942,
            "last_ns": 1661270128533492271,
            "hull_s": 239.888332329
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661270188675284471,
            "last_ns": 1661270428459492599,
            "hull_s": 239.784208128
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.78119536,
            60.024004369,
            59.994617327,
            60.088515273,
            60.1417922,
            59.973012212,
            59.789583723,
            60.059122177,
            59.962490016
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269888696580138,
            "last_ns": 1661270128573901563,
            "hull_s": 239.877321425
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661270188741159638,
            "last_ns": 1661270428491687767,
            "hull_s": 239.750528129
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.755862356,
            60.036633399,
            60.000586356,
            60.084239314,
            60.167258075,
            59.958548435,
            59.785022477,
            60.059010916,
            59.947946301
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269888214137288,
            "last_ns": 1661270128255427056,
            "hull_s": 240.041289768
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661270188231930783,
            "last_ns": 1661270428238165998,
            "hull_s": 240.006235215
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.006170117,
            60.00358254,
            59.996896462,
            60.034640649,
            59.976503727,
            60.006533506,
            59.990957995,
            60.009768173,
            59.998975541
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269888766331596,
            "last_ns": 1661270128666082315,
            "hull_s": 239.899750719
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661270188826587546,
            "last_ns": 1661270428573828233,
            "hull_s": 239.747240687
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.763679396,
            60.041432242,
            59.982727105,
            60.111911976,
            60.160505231,
            59.931883258,
            59.799779407,
            60.060805109,
            59.954772913
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269888799302360,
            "last_ns": 1661270128714766817,
            "hull_s": 239.915464457
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661270188887837986,
            "last_ns": 1661270428636527615,
            "hull_s": 239.748689629
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.779193881,
            60.067378508,
            59.947672507,
            60.121219561,
            60.173071169,
            59.928343261,
            59.790562913,
            60.054709921,
            59.975073534
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/productcatalogservice-668d5f85fb-jhwx9_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269888835880554,
            "last_ns": 1661270128758551429,
            "hull_s": 239.922670875
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661270188941107296,
            "last_ns": 1661270428709883303,
            "hull_s": 239.768776007
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.797345178,
            60.076156843,
            59.920956284,
            60.12821257,
            60.182555867,
            59.928270369,
            59.796392133,
            60.039127276,
            60.004986229
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269888870294235,
            "last_ns": 1661270128806927885,
            "hull_s": 239.93663365
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661270188982145116,
            "last_ns": 1661270428770498347,
            "hull_s": 239.788353231
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.858302891,
            60.020620757,
            59.91191176,
            60.145798242,
            60.175217231,
            59.927510285,
            59.818504004,
            60.027958919,
            60.014380023
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269888906949757,
            "last_ns": 1661270128839687246,
            "hull_s": 239.932737489
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661270189018791393,
            "last_ns": 1661270428823878271,
            "hull_s": 239.805086878
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.963356673,
            59.913733366,
            59.94943939,
            60.10620806,
            60.179104147,
            59.933432274,
            59.917328183,
            59.945203417,
            60.009123004
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/15_56_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 22537,
                "seconds_with_rows": 57,
                "first_ns": 1661270127846663376,
                "last_ns": 1661270183999134538,
                "hull_s": 56.152471162
              },
              "A": {
                "rows": 1629,
                "seconds_with_rows": 5,
                "first_ns": 1661270184000367894,
                "last_ns": 1661270188742766080,
                "hull_s": 4.742398186
              }
            },
            "end_split": {
              "N": {
                "rows": 22533,
                "seconds_with_rows": 57,
                "first_ns": 1661270127851796135,
                "last_ns": 1661270183999284792,
                "hull_s": 56.147488657
              },
              "A": {
                "rows": 1633,
                "seconds_with_rows": 5,
                "first_ns": 1661270184000354137,
                "last_ns": 1661270188744763387,
                "hull_s": 4.74440925
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/15_57_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 22819,
                "seconds_with_rows": 63,
                "first_ns": 1661270187906564020,
                "last_ns": 1661270249103126016,
                "hull_s": 61.196561996
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 22819,
                "seconds_with_rows": 63,
                "first_ns": 1661270187914680300,
                "last_ns": 1661270249186773988,
                "hull_s": 61.272093688
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/15_58_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 23148,
                "seconds_with_rows": 62,
                "first_ns": 1661270247108446471,
                "last_ns": 1661270308458198784,
                "hull_s": 61.349752313
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 23148,
                "seconds_with_rows": 62,
                "first_ns": 1661270247188300288,
                "last_ns": 1661270308460032447,
                "hull_s": 61.271732159
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 22537,
            "seconds_with_rows": 57,
            "first_ns": 1661270127846663376,
            "last_ns": 1661270183999134538,
            "hull_s": 56.152471162
          },
          "A": {
            "rows": 47596,
            "seconds_with_rows": 125,
            "first_ns": 1661270184000367894,
            "last_ns": 1661270308458198784,
            "hull_s": 124.45783089
          }
        },
        "end_split": {
          "N": {
            "rows": 22533,
            "seconds_with_rows": 57,
            "first_ns": 1661270127851796135,
            "last_ns": 1661270183999284792,
            "hull_s": 56.147488657
          },
          "A": {
            "rows": 47600,
            "seconds_with_rows": 125,
            "first_ns": 1661270184000354137,
            "last_ns": 1661270308460032447,
            "hull_s": 124.45967831
          }
        },
        "straddle_t": 4,
        "duplicate_keys": 412,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/log/15_56_log.csv",
            "N": {
              "rows": 24294,
              "seconds_with_rows": 57,
              "first_ns": 1661270127846709029,
              "last_ns": 1661270183999207469,
              "hull_s": 56.15249844
            },
            "A": {
              "rows": 1704,
              "seconds_with_rows": 5,
              "first_ns": 1661270184001194671,
              "last_ns": 1661270188744682817,
              "hull_s": 4.743488146
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/15_57_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 24754,
              "seconds_with_rows": 63,
              "first_ns": 1661270187906631497,
              "last_ns": 1661270249186747775,
              "hull_s": 61.280116278
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/15_58_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 24660,
              "seconds_with_rows": 62,
              "first_ns": 1661270247108474706,
              "last_ns": 1661270308459974020,
              "hull_s": 61.351499314
            }
          }
        ],
        "N": {
          "rows": 24294,
          "seconds_with_rows": 57,
          "first_ns": 1661270127846709029,
          "last_ns": 1661270183999207469,
          "hull_s": 56.15249844
        },
        "A": {
          "rows": 51118,
          "seconds_with_rows": 125,
          "first_ns": 1661270184001194671,
          "last_ns": 1661270308459974020,
          "hull_s": 124.458779349
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 75412,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.541e-06,
            2.073822393
          ],
          "relative_end_s": [
            -2.073841195,
            0.01118209
          ]
        }
      },
      "previous_inject_time_ns": 1661269663000000000,
      "previous_gap_s": 521.0,
      "next_gap_s": 518.0,
      "elapsed_s": 1.5780000000013388
    },
    {
      "case": "OB|shippingservice|cpu_contention|2022-08-22 07:26:48",
      "view": "main",
      "t_ns": 1661153208000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152939714608628,
            "last_ns": 1661153179711348886,
            "hull_s": 239.996740258
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661153239715473612,
            "last_ns": 1661153479761981812,
            "hull_s": 240.0465082
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.006581238,
            60.003491034,
            60.033453966,
            59.95321402,
            60.004124726,
            60.004407978,
            60.039396793,
            59.959536649,
            60.04316678
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152939746097830,
            "last_ns": 1661153179739641756,
            "hull_s": 239.993543926
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661153239754186346,
            "last_ns": 1661153479826142653,
            "hull_s": 240.071956307
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.029880863,
            59.988331014,
            60.063990121,
            59.911341928,
            60.01454459,
            60.002525621,
            60.070442177,
            59.92375555,
            60.075232959
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152939801483283,
            "last_ns": 1661153179786155405,
            "hull_s": 239.984672122
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661153239822950586,
            "last_ns": 1661153479910227066,
            "hull_s": 240.08727648
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.058996826,
            59.970887687,
            60.095772549,
            59.85901506,
            60.036795181,
            59.98974744,
            60.107927371,
            59.883686627,
            60.105915042
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152939859503165,
            "last_ns": 1661153179814098969,
            "hull_s": 239.954595804
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661153239885464398,
            "last_ns": 1661153479973428547,
            "hull_s": 240.087964149
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.063172172,
            59.95116327,
            60.129212659,
            59.811047703,
            60.071365429,
            59.962632215,
            60.123425644,
            59.864121497,
            60.137784793
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152939900159647,
            "last_ns": 1661153179837004762,
            "hull_s": 239.936845115
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661153239928632530,
            "last_ns": 1661153480029567108,
            "hull_s": 240.100934578
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.083220695,
            59.921546592,
            60.16061544,
            59.771462388,
            60.091627768,
            59.947804571,
            60.12718103,
            59.856193552,
            60.169755425
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152939681448724,
            "last_ns": 1661153179680909696,
            "hull_s": 239.999460972
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661153239682125513,
            "last_ns": 1661153479696700436,
            "hull_s": 240.014574923
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.000908843,
            60.002408068,
            60.007650125,
            59.988493936,
            60.001215817,
            60.003176834,
            60.007791338,
            59.994470967,
            60.009135784
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152939949075989,
            "last_ns": 1661153179874963392,
            "hull_s": 239.925887403
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661153239990122211,
            "last_ns": 1661153480101723326,
            "hull_s": 240.111601115
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.099980592,
            59.902016801,
            60.193029448,
            59.730860562,
            60.115158819,
            59.932943489,
            60.133966607,
            59.84226346,
            60.202427559
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152939999064780,
            "last_ns": 1661153179900194138,
            "hull_s": 239.901129358
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661153240033678873,
            "last_ns": 1661153480151121982,
            "hull_s": 240.117443109
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.089172695,
            59.896642366,
            60.224674628,
            59.690639669,
            60.133484735,
            59.924037307,
            60.138165979,
            59.831746065,
            60.223493758
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/productcatalogservice-668d5f85fb-wckp8_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152940181168100,
            "last_ns": 1661153179932084338,
            "hull_s": 239.750916238
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661153240082466245,
            "last_ns": 1661153480202791184,
            "hull_s": 240.120324939
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.949537688,
            59.889180333,
            60.234197595,
            59.678000622,
            60.150381907,
            59.935195024,
            60.126770968,
            59.816990221,
            60.241368726
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152940240144682,
            "last_ns": 1661153179958165286,
            "hull_s": 239.718020604
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661153240133558982,
            "last_ns": 1661153480237612819,
            "hull_s": 240.104053837
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.92466964,
            59.898939009,
            60.228275139,
            59.666136816,
            60.175393696,
            59.932450814,
            60.114296695,
            59.814430417,
            60.242875911
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152940297041452,
            "last_ns": 1661153179997941090,
            "hull_s": 239.700899638
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661153240180061136,
            "last_ns": 1661153480279898384,
            "hull_s": 240.099837248
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.909388893,
            59.891623912,
            60.230547554,
            59.669339279,
            60.182120046,
            59.949407189,
            60.091957232,
            59.829079878,
            60.229392949
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/07_26_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 22985,
                "seconds_with_rows": 61,
                "first_ns": 1661153119303526319,
                "last_ns": 1661153179608252672,
                "hull_s": 60.304726353
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "end_split": {
              "N": {
                "rows": 22985,
                "seconds_with_rows": 61,
                "first_ns": 1661153119339819047,
                "last_ns": 1661153179612149998,
                "hull_s": 60.272330951
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/07_27_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 10502,
                "seconds_with_rows": 29,
                "first_ns": 1661153179397956548,
                "last_ns": 1661153207998144270,
                "hull_s": 28.600187722
              },
              "A": {
                "rows": 11891,
                "seconds_with_rows": 32,
                "first_ns": 1661153208000246110,
                "last_ns": 1661153239503502504,
                "hull_s": 31.503256394
              }
            },
            "end_split": {
              "N": {
                "rows": 10485,
                "seconds_with_rows": 29,
                "first_ns": 1661153179400119808,
                "last_ns": 1661153207997666182,
                "hull_s": 28.597546374
              },
              "A": {
                "rows": 11908,
                "seconds_with_rows": 32,
                "first_ns": 1661153208019849717,
                "last_ns": 1661153239508723154,
                "hull_s": 31.488873437
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/07_28_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 22535,
                "seconds_with_rows": 61,
                "first_ns": 1661153239274640930,
                "last_ns": 1661153299699587840,
                "hull_s": 60.42494691
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 22535,
                "seconds_with_rows": 61,
                "first_ns": 1661153239285816576,
                "last_ns": 1661153299703292459,
                "hull_s": 60.417475883
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 33487,
            "seconds_with_rows": 89,
            "first_ns": 1661153119303526319,
            "last_ns": 1661153207998144270,
            "hull_s": 88.694617951
          },
          "A": {
            "rows": 34426,
            "seconds_with_rows": 92,
            "first_ns": 1661153208000246110,
            "last_ns": 1661153299699587840,
            "hull_s": 91.69934173
          }
        },
        "end_split": {
          "N": {
            "rows": 33470,
            "seconds_with_rows": 89,
            "first_ns": 1661153119339819047,
            "last_ns": 1661153207997666182,
            "hull_s": 88.657847135
          },
          "A": {
            "rows": 34443,
            "seconds_with_rows": 92,
            "first_ns": 1661153208019849717,
            "last_ns": 1661153299703292459,
            "hull_s": 91.683442742
          }
        },
        "straddle_t": 17,
        "duplicate_keys": 177,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-22/log/07_26_log.csv",
            "N": {
              "rows": 24680,
              "seconds_with_rows": 61,
              "first_ns": 1661153119303558060,
              "last_ns": 1661153179612121860,
              "hull_s": 60.3085638
            },
            "A": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/log/07_27_log.csv",
            "N": {
              "rows": 11332,
              "seconds_with_rows": 29,
              "first_ns": 1661153179397984354,
              "last_ns": 1661153207998836337,
              "hull_s": 28.600851983
            },
            "A": {
              "rows": 12925,
              "seconds_with_rows": 32,
              "first_ns": 1661153208001221780,
              "last_ns": 1661153239508686084,
              "hull_s": 31.507464304
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/log/07_28_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 24534,
              "seconds_with_rows": 61,
              "first_ns": 1661153239274666258,
              "last_ns": 1661153299703265527,
              "hull_s": 60.428599269
            }
          }
        ],
        "N": {
          "rows": 36012,
          "seconds_with_rows": 89,
          "first_ns": 1661153119303558060,
          "last_ns": 1661153207998836337,
          "hull_s": 88.695278277
        },
        "A": {
          "rows": 37459,
          "seconds_with_rows": 92,
          "first_ns": 1661153208001221780,
          "last_ns": 1661153299703265527,
          "hull_s": 91.702043747
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 73471,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.573e-06,
            2.19128433
          ],
          "relative_end_s": [
            -2.191288673,
            0.010296193
          ]
        }
      },
      "previous_inject_time_ns": 1661152675000000000,
      "previous_gap_s": 533.0,
      "next_gap_s": 1052.0,
      "elapsed_s": 1.5469999999986612
    },
    {
      "case": "OB|shippingservice|cpu_contention|2022-08-23 15:47:43",
      "view": "main",
      "t_ns": 1661269663000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269408275544304,
            "last_ns": 1661269648304705769,
            "hull_s": 240.029161465
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269708254086078,
            "last_ns": 1661269948286781643,
            "hull_s": 240.032695565
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.99718919,
            60.034831124,
            59.943742287,
            60.053398864,
            59.949380309,
            60.093278902,
            59.907509888,
            60.001277672,
            60.030629103
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269408315504584,
            "last_ns": 1661269648377620616,
            "hull_s": 240.062116032
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269708295047637,
            "last_ns": 1661269948330549346,
            "hull_s": 240.035501709
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.999467521,
            60.073430644,
            59.89223178,
            60.096986087,
            59.917427021,
            60.118648329,
            59.873059706,
            60.030337316,
            60.013456358
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269408415027353,
            "last_ns": 1661269648482856772,
            "hull_s": 240.067829419
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269708367089970,
            "last_ns": 1661269948393930160,
            "hull_s": 240.02684019
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.964736519,
            60.107900942,
            59.845989223,
            60.149202735,
            59.884233198,
            60.136314748,
            59.839906409,
            60.07653853,
            59.974080503
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269408537165659,
            "last_ns": 1661269648572118283,
            "hull_s": 240.034952624
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269708410232108,
            "last_ns": 1661269948426355302,
            "hull_s": 240.016123194
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.890300658,
            60.132369649,
            59.811108726,
            60.201173591,
            59.838113825,
            60.134594514,
            59.83512751,
            60.26520581,
            59.78119536
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269408603686195,
            "last_ns": 1661269648712314223,
            "hull_s": 240.108628028
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269708445299409,
            "last_ns": 1661269948452442494,
            "hull_s": 240.007143085
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.861224633,
            60.160756742,
            59.775268816,
            60.311377837,
            59.732985186,
            60.142001714,
            59.819153842,
            60.290125173,
            59.755862356
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269408215252300,
            "last_ns": 1661269648232168512,
            "hull_s": 240.016916212
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269708215237365,
            "last_ns": 1661269948220307405,
            "hull_s": 240.00507004
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.013766781,
            60.004062722,
            59.985904025,
            60.013182684,
            59.983068853,
            60.013914391,
            59.992037128,
            59.992948404,
            60.006170117
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269408677221635,
            "last_ns": 1661269648816264703,
            "hull_s": 240.139043068
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269708505282343,
            "last_ns": 1661269948530010992,
            "hull_s": 240.024728649
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.850737245,
            60.160960242,
            59.76406295,
            60.363282631,
            59.68901764,
            60.135429376,
            59.81593999,
            60.309679887,
            59.763679396
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269408707591566,
            "last_ns": 1661269648852317010,
            "hull_s": 240.144725444
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269708544240695,
            "last_ns": 1661269948578496241,
            "hull_s": 240.034255546
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.851160796,
            60.161751713,
            59.761487658,
            60.370325277,
            59.691923685,
            60.150551726,
            59.791929623,
            60.312580316,
            59.779193881
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/productcatalogservice-668d5f85fb-jhwx9_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269408745914169,
            "last_ns": 1661269648896984646,
            "hull_s": 240.151070477
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269708584083708,
            "last_ns": 1661269948633225732,
            "hull_s": 240.049142024
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.853507827,
            60.155445445,
            59.757413566,
            60.384703639,
            59.687099062,
            60.172613696,
            59.765775664,
            60.313407486,
            59.797345178
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269408775341013,
            "last_ns": 1661269648951871113,
            "hull_s": 240.1765301
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269708614022136,
            "last_ns": 1661269948728597126,
            "hull_s": 240.11457499
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.89041393,
            60.130166334,
            59.743139644,
            60.412810192,
            59.662151023,
            60.202846,
            59.736858721,
            60.316567378,
            59.858302891
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-23/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269408811990421,
            "last_ns": 1661269649014910888,
            "hull_s": 240.202920467
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661269708649140399,
            "last_ns": 1661269948870306430,
            "hull_s": 240.221166031
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            59.996155486,
            60.015151052,
            59.744346073,
            60.447267856,
            59.634229511,
            60.218282705,
            59.718720969,
            60.320805684,
            59.963356673
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/15_47_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 23809,
                "seconds_with_rows": 60,
                "first_ns": 1661269588131839170,
                "last_ns": 1661269647717098240,
                "hull_s": 59.58525907
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "end_split": {
              "N": {
                "rows": 23809,
                "seconds_with_rows": 60,
                "first_ns": 1661269588135696896,
                "last_ns": 1661269647719516176,
                "hull_s": 59.58381928
              },
              "A": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/15_48_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 6715,
                "seconds_with_rows": 15,
                "first_ns": 1661269648113814003,
                "last_ns": 1661269662996597986,
                "hull_s": 14.882783983
              },
              "A": {
                "rows": 18225,
                "seconds_with_rows": 46,
                "first_ns": 1661269663001824256,
                "last_ns": 1661269708000477538,
                "hull_s": 44.998653282
              }
            },
            "end_split": {
              "N": {
                "rows": 6713,
                "seconds_with_rows": 15,
                "first_ns": 1661269648117636937,
                "last_ns": 1661269662996582762,
                "hull_s": 14.878945825
              },
              "A": {
                "rows": 18227,
                "seconds_with_rows": 46,
                "first_ns": 1661269663002125312,
                "last_ns": 1661269708004487641,
                "hull_s": 45.002362329
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/trace/15_49_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 22959,
                "seconds_with_rows": 61,
                "first_ns": 1661269707033015400,
                "last_ns": 1661269767882436096,
                "hull_s": 60.849420696
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 22959,
                "seconds_with_rows": 61,
                "first_ns": 1661269707489872896,
                "last_ns": 1661269767884709142,
                "hull_s": 60.394836246
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 30524,
            "seconds_with_rows": 75,
            "first_ns": 1661269588131839170,
            "last_ns": 1661269662996597986,
            "hull_s": 74.864758816
          },
          "A": {
            "rows": 41184,
            "seconds_with_rows": 105,
            "first_ns": 1661269663001824256,
            "last_ns": 1661269767882436096,
            "hull_s": 104.88061184
          }
        },
        "end_split": {
          "N": {
            "rows": 30522,
            "seconds_with_rows": 75,
            "first_ns": 1661269588135696896,
            "last_ns": 1661269662996582762,
            "hull_s": 74.860885866
          },
          "A": {
            "rows": 41186,
            "seconds_with_rows": 105,
            "first_ns": 1661269663002125312,
            "last_ns": 1661269767884709142,
            "hull_s": 104.88258383
          }
        },
        "straddle_t": 2,
        "duplicate_keys": 62,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-23/log/15_47_log.csv",
            "N": {
              "rows": 25708,
              "seconds_with_rows": 60,
              "first_ns": 1661269588131892956,
              "last_ns": 1661269647719482464,
              "hull_s": 59.587589508
            },
            "A": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/15_48_log.csv",
            "N": {
              "rows": 7111,
              "seconds_with_rows": 15,
              "first_ns": 1661269648113857195,
              "last_ns": 1661269662995689001,
              "hull_s": 14.881831806
            },
            "A": {
              "rows": 19581,
              "seconds_with_rows": 46,
              "first_ns": 1661269663002080870,
              "last_ns": 1661269708004463043,
              "hull_s": 45.002382173
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-23/log/15_49_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 24786,
              "seconds_with_rows": 61,
              "first_ns": 1661269707033050404,
              "last_ns": 1661269767884682794,
              "hull_s": 60.85163239
            }
          }
        ],
        "N": {
          "rows": 32819,
          "seconds_with_rows": 75,
          "first_ns": 1661269588131892956,
          "last_ns": 1661269662995689001,
          "hull_s": 74.863796045
        },
        "A": {
          "rows": 44367,
          "seconds_with_rows": 105,
          "first_ns": 1661269663002080870,
          "last_ns": 1661269767884682794,
          "hull_s": 104.882601924
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 77186,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.381e-06,
            1.814730423
          ],
          "relative_end_s": [
            -1.814712787,
            0.009854141
          ]
        }
      },
      "previous_inject_time_ns": 1661269132000000000,
      "previous_gap_s": 531.0,
      "next_gap_s": 521.0,
      "elapsed_s": 1.5940000000009604
    },
    {
      "case": "OB|recommendationservice|cpu_consumed|2022-08-22 07:10:43",
      "view": "sensitivity_A",
      "t_ns": 1661152183000000000,
      "metric": [
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/adservice-5f6585d649-fnmft_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151919704261154,
            "last_ns": 1661152159883469106,
            "hull_s": 240.179207952
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152219756135321,
            "last_ns": 1661152459712331944,
            "hull_s": 239.956196623
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.00895857,
            60.023121121,
            60.007589541,
            60.13953872,
            59.872666215,
            59.991885482,
            59.988136756,
            59.96956974,
            60.006604645
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/cartservice-579f59597d-wc2lz_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151919732457152,
            "last_ns": 1661152159934698918,
            "hull_s": 240.202241766
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152219923068367,
            "last_ns": 1661152459757345623,
            "hull_s": 239.834277256
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.018751342,
            60.051798573,
            60.00883442,
            60.122857431,
            59.988369449,
            59.865148259,
            59.986336638,
            59.981348497,
            60.001443862
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/checkoutservice-578fcf4766-9csqn_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151919783490370,
            "last_ns": 1661152159989224544,
            "hull_s": 240.205734174
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152220009796009,
            "last_ns": 1661152459835597893,
            "hull_s": 239.825801884
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.030000492,
            60.151043256,
            59.93408892,
            60.090601506,
            60.020571465,
            60.010250623,
            59.816955638,
            59.992973778,
            60.005621845
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/currencyservice-cf787dd48-vpjrd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151919817200553,
            "last_ns": 1661152160018663491,
            "hull_s": 240.201462938
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152220076602240,
            "last_ns": 1661152459890726587,
            "hull_s": 239.814124347
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.030034294,
            60.167383332,
            59.93155834,
            60.072486972,
            60.057938749,
            60.014053171,
            59.813872111,
            59.992365301,
            59.993833764
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/emailservice-55fdc5b988-f6xth_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151919849750249,
            "last_ns": 1661152160040469196,
            "hull_s": 240.190718947
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152220134844318,
            "last_ns": 1661152459923567911,
            "hull_s": 239.788723593
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.024822845,
            60.173524986,
            59.957895657,
            60.034475459,
            60.094375122,
            59.997719749,
            59.805576133,
            60.021793946,
            59.963633765
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/front_service.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151919674305606,
            "last_ns": 1661152159725326175,
            "hull_s": 240.051020569
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152219685660849,
            "last_ns": 1661152459668554513,
            "hull_s": 239.982893664
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.001005242,
            60.019702454,
            59.990490356,
            60.039822517,
            59.960334674,
            60.018319972,
            59.985247058,
            59.986415577,
            59.992911057
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/frontend-579b9bff58-t2dbm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151919899528130,
            "last_ns": 1661152160075470659,
            "hull_s": 240.175942529
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152220179018986,
            "last_ns": 1661152459979291001,
            "hull_s": 239.800272015
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.022697727,
            60.184086052,
            59.974314638,
            59.994844112,
            60.103548327,
            60.028545402,
            59.913690351,
            59.911504628,
            59.946531634
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/paymentservice-9cdb6588f-554sm_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151919932440037,
            "last_ns": 1661152160122182092,
            "hull_s": 240.189742055
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152220209862619,
            "last_ns": 1661152460026790406,
            "hull_s": 239.816927787
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.029327221,
            60.187080887,
            59.990431556,
            59.982902391,
            60.087680527,
            60.06323986,
            59.880533904,
            60.000928323,
            59.8722257
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/productcatalogservice-668d5f85fb-wckp8_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151919965657143,
            "last_ns": 1661152160152190983,
            "hull_s": 240.18653384
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152220264361174,
            "last_ns": 1661152460066850491,
            "hull_s": 239.802489317
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.027304189,
            60.20342949,
            59.974818481,
            59.98098168,
            60.112170191,
            60.077904756,
            59.842908062,
            60.036420057,
            59.845256442
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151920003235798,
            "last_ns": 1661152160177093471,
            "hull_s": 240.173857673
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152220306970791,
            "last_ns": 1661152460101088201,
            "hull_s": 239.79411741
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.019069363,
            60.227537275,
            59.948472058,
            59.978778977,
            60.12987732,
            60.096715701,
            59.808638906,
            60.057821539,
            59.830941264
          ]
        },
        {
          "path": "online-boutique/rca_data/2022-08-22/metric/shippingservice-7b598fc7d-lmggd_metric.csv",
          "N": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661151920037945129,
            "last_ns": 1661152160206534316,
            "hull_s": 240.168589187
          },
          "A": {
            "rows": 5,
            "seconds_with_rows": 5,
            "first_ns": 1661152220341959116,
            "last_ns": 1661152460141489652,
            "hull_s": 239.799530536
          },
          "circa_train_observed_rows": 2,
          "cadence_window_s": [
            60.016816479,
            60.237374266,
            59.936315393,
            59.978083049,
            60.1354248,
            60.124364201,
            59.773843713,
            60.064479704,
            59.836842918
          ]
        }
      ],
      "trace": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/07_10_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 9132,
                "seconds_with_rows": 25,
                "first_ns": 1661152158984489303,
                "last_ns": 1661152182998879744,
                "hull_s": 24.014390441
              },
              "A": {
                "rows": 7945,
                "seconds_with_rows": 41,
                "first_ns": 1661152183001287401,
                "last_ns": 1661152223790440448,
                "hull_s": 40.789153047
              }
            },
            "end_split": {
              "N": {
                "rows": 9128,
                "seconds_with_rows": 25,
                "first_ns": 1661152158988283136,
                "last_ns": 1661152182999837184,
                "hull_s": 24.011554048
              },
              "A": {
                "rows": 7949,
                "seconds_with_rows": 41,
                "first_ns": 1661152183001277205,
                "last_ns": 1661152223792908013,
                "hull_s": 40.791630808
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/07_11_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 11619,
                "seconds_with_rows": 67,
                "first_ns": 1661152216051059589,
                "last_ns": 1661152282861932969,
                "hull_s": 66.81087338
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 11619,
                "seconds_with_rows": 67,
                "first_ns": 1661152216057724654,
                "last_ns": 1661152282864259242,
                "hull_s": 66.806534588
              }
            },
            "rejected_end_at_or_after_hi": 0
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/trace/07_12_trace.csv",
            "statusCode_present": false,
            "start_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 12657,
                "seconds_with_rows": 70,
                "first_ns": 1661152274943484432,
                "last_ns": 1661152343272189822,
                "hull_s": 68.32870539
              }
            },
            "end_split": {
              "N": {
                "rows": 0,
                "seconds_with_rows": 0,
                "first_ns": null,
                "last_ns": null,
                "hull_s": 0
              },
              "A": {
                "rows": 12657,
                "seconds_with_rows": 70,
                "first_ns": 1661152274956351776,
                "last_ns": 1661152343274744344,
                "hull_s": 68.318392568
              }
            },
            "rejected_end_at_or_after_hi": 0
          }
        ],
        "start_split": {
          "N": {
            "rows": 9132,
            "seconds_with_rows": 25,
            "first_ns": 1661152158984489303,
            "last_ns": 1661152182998879744,
            "hull_s": 24.014390441
          },
          "A": {
            "rows": 32221,
            "seconds_with_rows": 161,
            "first_ns": 1661152183001287401,
            "last_ns": 1661152343272189822,
            "hull_s": 160.270902421
          }
        },
        "end_split": {
          "N": {
            "rows": 9128,
            "seconds_with_rows": 25,
            "first_ns": 1661152158988283136,
            "last_ns": 1661152182999837184,
            "hull_s": 24.011554048
          },
          "A": {
            "rows": 32225,
            "seconds_with_rows": 161,
            "first_ns": 1661152183001277205,
            "last_ns": 1661152343274744344,
            "hull_s": 160.273467139
          }
        },
        "straddle_t": 4,
        "duplicate_keys": 1411,
        "duration_bad": 0,
        "end_membership_diff_ns_vs_us": 0,
        "operations_A_without_N": 0,
        "operations_N_lt2": 0
      },
      "log": {
        "sources": [
          {
            "path": "online-boutique/rca_data/2022-08-22/log/07_10_log.csv",
            "N": {
              "rows": 9794,
              "seconds_with_rows": 25,
              "first_ns": 1661152158984552439,
              "last_ns": 1661152182999890590,
              "hull_s": 24.015338151
            },
            "A": {
              "rows": 8507,
              "seconds_with_rows": 41,
              "first_ns": 1661152183002350688,
              "last_ns": 1661152223792870349,
              "hull_s": 40.790519661
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/log/07_11_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 12430,
              "seconds_with_rows": 67,
              "first_ns": 1661152216051095406,
              "last_ns": 1661152282864231805,
              "hull_s": 66.813136399
            }
          },
          {
            "path": "online-boutique/rca_data/2022-08-22/log/07_12_log.csv",
            "N": {
              "rows": 0,
              "seconds_with_rows": 0,
              "first_ns": null,
              "last_ns": null,
              "hull_s": 0
            },
            "A": {
              "rows": 13492,
              "seconds_with_rows": 70,
              "first_ns": 1661152274943552253,
              "last_ns": 1661152343274713782,
              "hull_s": 68.331161529
            }
          }
        ],
        "N": {
          "rows": 9794,
          "seconds_with_rows": 25,
          "first_ns": 1661152158984552439,
          "last_ns": 1661152182999890590,
          "hull_s": 24.015338151
        },
        "A": {
          "rows": 34429,
          "seconds_with_rows": 161,
          "first_ns": 1661152183002350688,
          "last_ns": 1661152343274713782,
          "hull_s": 160.272363094
        },
        "Timestamp_vs_TimeUnixNano_disagree": 0,
        "join": {
          "matched": 44223,
          "missing_span_in_selected_window": 0,
          "relative_start_s": [
            2.676e-06,
            5.745277666
          ],
          "relative_end_s": [
            -5.745272941,
            0.018596316
          ]
        }
      },
      "previous_inject_time_ns": 1661151685000000000,
      "previous_gap_s": 498.0,
      "next_gap_s": 492.0,
      "elapsed_s": 0.9219999999986612
    }
  ],
  "derived_payload_files": []
}
<!-- T026_AUDIT_JSON_END -->

<!-- T026_QA_JSON_START -->

{
  "run": "kiem-na-002-doc-lap",
  "elapsed_s": 33.15599999999904,
  "cases": [
    {
      "case": "OB|adservice|cpu_contention|2022-08-23 16:31:35",
      "view": "main",
      "trace_duplicate_rows": 301,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 25463,
      "trace_unique_A_end": 37743,
      "log_identical_duplicate_N": 343,
      "log_identical_duplicate_A": 0
    },
    {
      "case": "OB|checkoutservice|exception|2022-08-22 05:01:13",
      "view": "main",
      "trace_duplicate_rows": 0,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 20859,
      "trace_unique_A_end": 51956,
      "log_identical_duplicate_N": 0,
      "log_identical_duplicate_A": 0
    },
    {
      "case": "OB|checkoutservice|exception|2022-08-23 13:02:09",
      "view": "main",
      "trace_duplicate_rows": 90,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 16158,
      "trace_unique_A_end": 54475,
      "log_identical_duplicate_N": 0,
      "log_identical_duplicate_A": 92
    },
    {
      "case": "OB|checkoutservice|network_delay|2022-08-22 04:52:55",
      "view": "main",
      "trace_duplicate_rows": 172,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 38794,
      "trace_unique_A_end": 34979,
      "log_identical_duplicate_N": 176,
      "log_identical_duplicate_A": 0
    },
    {
      "case": "OB|checkoutservice|network_delay|2022-08-23 12:53:52",
      "view": "main",
      "trace_duplicate_rows": 0,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 31749,
      "trace_unique_A_end": 37654,
      "log_identical_duplicate_N": 0,
      "log_identical_duplicate_A": 0
    },
    {
      "case": "OB|checkoutservice|return|2022-08-22 05:09:50",
      "view": "main",
      "trace_duplicate_rows": 164,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 36246,
      "trace_unique_A_end": 34869,
      "log_identical_duplicate_N": 131,
      "log_identical_duplicate_A": 48
    },
    {
      "case": "OB|checkoutservice|return|2022-08-23 13:10:36",
      "view": "main",
      "trace_duplicate_rows": 62,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 26267,
      "trace_unique_A_end": 44004,
      "log_identical_duplicate_N": 82,
      "log_identical_duplicate_A": 0
    },
    {
      "case": "OB|emailservice|cpu_consumed|2022-08-23 14:03:48",
      "view": "main",
      "trace_duplicate_rows": 248,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 31951,
      "trace_unique_A_end": 40298,
      "log_identical_duplicate_N": 0,
      "log_identical_duplicate_A": 328
    },
    {
      "case": "OB|emailservice|network_delay|2022-08-22 05:43:48",
      "view": "main",
      "trace_duplicate_rows": 308,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 34763,
      "trace_unique_A_end": 35092,
      "log_identical_duplicate_N": 247,
      "log_identical_duplicate_A": 123
    },
    {
      "case": "OB|emailservice|network_delay|2022-08-23 13:54:37",
      "view": "main",
      "trace_duplicate_rows": 184,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 27490,
      "trace_unique_A_end": 44562,
      "log_identical_duplicate_N": 0,
      "log_identical_duplicate_A": 206
    },
    {
      "case": "OB|frontend|return|2022-08-22 04:02:07",
      "view": "main",
      "trace_duplicate_rows": 333,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 18497,
      "trace_unique_A_end": 29381,
      "log_identical_duplicate_N": 0,
      "log_identical_duplicate_A": 414
    },
    {
      "case": "OB|frontend|return|2022-08-23 12:10:21",
      "view": "main",
      "trace_duplicate_rows": 0,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 19751,
      "trace_unique_A_end": 26759,
      "log_identical_duplicate_N": 0,
      "log_identical_duplicate_A": 0
    },
    {
      "case": "OB|paymentservice|cpu_contention|2022-08-22 06:01:18",
      "view": "main",
      "trace_duplicate_rows": 110,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 23054,
      "trace_unique_A_end": 48724,
      "log_identical_duplicate_N": 0,
      "log_identical_duplicate_A": 130
    },
    {
      "case": "OB|paymentservice|cpu_contention|2022-08-23 14:21:54",
      "view": "main",
      "trace_duplicate_rows": 359,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 34546,
      "trace_unique_A_end": 36405,
      "log_identical_duplicate_N": 258,
      "log_identical_duplicate_A": 123
    },
    {
      "case": "OB|productcatalogservice|exception|2022-08-23 15:04:28",
      "view": "main",
      "trace_duplicate_rows": 226,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 24894,
      "trace_unique_A_end": 14030,
      "log_identical_duplicate_N": 177,
      "log_identical_duplicate_A": 80
    },
    {
      "case": "OB|recommendationservice|cpu_consumed|2022-08-22 07:10:43",
      "view": "main",
      "trace_duplicate_rows": 1411,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 20826,
      "trace_unique_A_end": 19116,
      "log_identical_duplicate_N": 934,
      "log_identical_duplicate_A": 507
    },
    {
      "case": "OB|recommendationservice|cpu_consumed|2022-08-23 15:29:49",
      "view": "main",
      "trace_duplicate_rows": 651,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 32768,
      "trace_unique_A_end": 19578,
      "log_identical_duplicate_N": 164,
      "log_identical_duplicate_A": 545
    },
    {
      "case": "OB|recommendationservice|network_delay|2022-08-22 06:52:56",
      "view": "main",
      "trace_duplicate_rows": 223,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 37706,
      "trace_unique_A_end": 28165,
      "log_identical_duplicate_N": 51,
      "log_identical_duplicate_A": 187
    },
    {
      "case": "OB|recommendationservice|network_delay|2022-08-23 15:12:49",
      "view": "main",
      "trace_duplicate_rows": 307,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 32039,
      "trace_unique_A_end": 35373,
      "log_identical_duplicate_N": 64,
      "log_identical_duplicate_A": 295
    },
    {
      "case": "OB|shippingservice|cpu_consumed|2022-08-23 15:56:24",
      "view": "main",
      "trace_duplicate_rows": 412,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 22533,
      "trace_unique_A_end": 47188,
      "log_identical_duplicate_N": 0,
      "log_identical_duplicate_A": 444
    },
    {
      "case": "OB|shippingservice|cpu_contention|2022-08-22 07:26:48",
      "view": "main",
      "trace_duplicate_rows": 177,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 33355,
      "trace_unique_A_end": 34381,
      "log_identical_duplicate_N": 120,
      "log_identical_duplicate_A": 82
    },
    {
      "case": "OB|shippingservice|cpu_contention|2022-08-23 15:47:43",
      "view": "main",
      "trace_duplicate_rows": 62,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 30522,
      "trace_unique_A_end": 41124,
      "log_identical_duplicate_N": 0,
      "log_identical_duplicate_A": 82
    },
    {
      "case": "OB|recommendationservice|cpu_consumed|2022-08-22 07:10:43",
      "view": "sensitivity_A",
      "trace_duplicate_rows": 1411,
      "trace_conflicting_rows": 0,
      "trace_unique_N_end": 9128,
      "trace_unique_A_end": 30814,
      "log_identical_duplicate_N": 0,
      "log_identical_duplicate_A": 1441
    }
  ],
  "count_assertions": "all source N/A counts and metric first/last matched",
  "derived_payload_files": []
}
<!-- T026_QA_JSON_END -->


## Phiên 3 — 0.4/0.5: kiểm hợp đồng và đề xuất triển khai, chưa duyệt

Ngày 07/10/2026. **Đã kiểm để lập đề xuất 0.4/0.5; hợp đồng đầu vào và phạm vi triển khai vẫn CANDIDATE.** Mục này cập nhật trạng thái và điểm dừng của báo cáo phiên 2 ở trên. Giữ nguyên hai khối 001/002 và mọi số cũ. Chưa adapter, loader/scorer/ranker, pilot hay evaluator; chưa quyết định mới trong WHY/DECISIONS. Rà trước bước B ở LOG, mục “Rà SPEC và đầu vào — phiên 3”; không thấy lỗi chặn việc kiểm và lập đề xuất. Không dùng adapter TT nguyên trạng để giải quyết các điểm OPEN.

### Bằng chứng và phạm vi lượt mới

Lượt **kiem-hop-dong-003** kiểm trong RAM đúng 22 cửa sổ chính và một cửa sổ độ nhạy A đã duyệt. Độ nhạy B tái dùng 21 ca đồng thuận. Guard từ chối 34 tên test và hai tên giả trước I/O; 154 file khớp hash/byte trước đọc; chỉ lấy định danh, Time và thống kê giá trị trong cửa sổ từng nguồn. Không mở raw ngày cho người phân tích, construct, TT hay locked; không xuất payload. Mất **13,387 s**, không phải chi phí phương pháp. Code tái lập và tiến độ ở LOG phiên 3; khối 003 cuối mục này giữ thống kê, manifest dùng lại 001.

001/002 vẫn parse JSON nghiêm ngặt, tổng/biên/quan hệ hàng–khóa và hash nguồn khớp. Không chạy lại đếm 0.2/0.3. 5.800 span lặp và 6.433 log lặp là hàng theo file, không là quan sát độc lập.

### 0.4 — thực thể, operation và universe U

**FACT:** trong cả 23 cửa sổ, trace/log có đúng 10 service sau đối chiếu PodName với danh sách pod nguồn metric; không có pod ngoài danh sách. Code Nezha bỏ hai hậu tố pod để lấy service (results/T-008/sources/data_integrate.py:254–260). Adapter đề xuất dùng alias tường minh, không regex tổng quát. Không lấy inventory từ tập root nhãn.

| Pod đã thấy trong nguồn trực tiếp | Service đề xuất trong P3 |
|---|---|
| adservice-5f6585d649-fnmft | adservice |
| cartservice-579f59597d-wc2lz | cartservice |
| checkoutservice-578fcf4766-9csqn | checkoutservice |
| currencyservice-cf787dd48-vpjrd | currencyservice |
| emailservice-55fdc5b988-f6xth | emailservice |
| frontend-579b9bff58-t2dbm | frontend |
| paymentservice-9cdb6588f-554sm | paymentservice |
| productcatalogservice-668d5f85fb-wckp8 | productcatalogservice |
| productcatalogservice-668d5f85fb-jhwx9 | productcatalogservice |
| recommendationservice-6cfdd55578-gfj6q | recommendationservice |
| shippingservice-7b598fc7d-lmggd | shippingservice |

Bằng chứng: 003.aliases_evidence, metric_identifiers, cases[].trace_services/log_services; metadata T-008 file-audit-001/summary.json:5943,6155,6354,6553,6789,7005,7204,7403,7602,7801,20022. **FACT mới:** ServiceName trong front_service.csv là **Frontend**, cả hai ngày trong cửa sổ được phép. **CANDIDATE:** alias đúng một tên Frontend → frontend; không tự lower-case mọi định danh hoặc suy alias chỉ từ tên file.

**CANDIDATE U=10 service** trong bảng, productcatalog chỉ một thực thể. Đây là inventory đã quan sát của dev, không khẳng định toàn kiến trúc Online Boutique chỉ có 10 thành phần. Không thêm DB/node/service không quan sát để khép tập, không dùng U=68/ts-* TT (WHY-26:247). Giữ bốn tập và thực thể trả ngoài U như giao thức §8.1. Root chỉ nối ở evaluator sau ghi đầu ra.

**CANDIDATE chuyển schema:**

- TraceID→traceID, SpanID→spanID, ParentID→parentSpanID, giữ chuỗi; PodName→serviceName qua alias. OperationName→operationName và methodName, giữ nguyên nội dung. Khóa method = service + dấu gạch dưới + OperationName. Không áp luật HTTP→service con hoặc chuẩn hóa ký tự của TORAI TT.
- Cắt outer span bằng Start/End ns nguồn: start≥t−300, end<t+300. Sau cắt mới startTime=StartTimeUnixNano//1000 và duration theo Duration µs nguồn. Giữ ns gốc trong provenance, kiểm membership trước/sau đổi đơn vị. SimpleRCA split start; MicroRank/TraceRCA split end; graph CIRCA chỉ span kết thúc trước t. Không dịch clock.
- Log cắt bằng TimeUnixNano; Log→message, PodName→container_name qua alias. SimpleRCA dùng log A. Timestamp RFC3339/ns gốc giữ trong provenance; không thay thời gian log bằng thời gian trace.
- Kiểm cấu trúc mapping đề xuất ở 23 cửa sổ: operation ứng nhiều service=0; operation A thiếu N=0; operation N dưới hai hàng=0; dưới hai khóa span duy nhất ở N=0 (003.cases). Chưa chứng minh std/score hữu hạn sau code, đủ nhóm normal/anomaly, nền sạch, recovery hay độc lập thống kê. Chưa có OK runtime.

### 0.4 — kênh, đơn vị và timestamp giữa nguồn

**FACT về nguồn:** mỗi pod có 19 cột số, front_service có 5. Đơn vị dưới đây là khai báo header; công thức collector chưa được xác minh.

| Nguồn | Kênh cung cấp/phạm vi |
|---|---|
| 10 pod resource, Time | CpuUsage(m), CpuUsageRate(%); MemoryUsage(Mi), MemoryUsageRate(%); SyscallRead/Write; NetworkReceive/TransmitBytes; PodClientLatencyP90/P95/P99(s), PodServerLatencyP90/P95/P99(s); PodWorkload(Ops), PodSuccessRate(%); NodeCpuUsageRate(%), NodeMemoryUsageRate(%), NodeNetworkReceiveBytes |
| front_service, Time | SuccessRate(%), LatencyP50/P90/P95/P99(s) |
| source_50/destination_50 | Có time chữ thường, timestamp và cột source_destination. Không thuộc 11 nguồn Time đã kiểm; clock/đơn vị/quyền gán endpoint chưa xác lập |
| dependency | Source, Target, Weight, không có thời gian. Không thay graph từ trace N |

Nguồn schema: results/T-008/runs/file-audit-001/summary.json; tác giả chọn Time ở alarm.py:268–275. Không dùng TimeStamp để cắt hay chuyển schema.

**FACT 003:** không có timestamp trùng chính xác giữa cả 11 nguồn; hợp timestamp là **110 thời điểm mỗi cửa sổ**, không phải 10. Khi so 10 quan sát theo thứ tự sau cắt từng nguồn, khoảng max−min giữa nguồn là **0,317031394–0,894812915 s**. Cả 23 cửa sổ có cùng membership N/A ở cùng thứ tự (5+5). Chưa có scrape-ID chung để chứng minh đo đồng thời. Lượt này không làm tròn, ghép bảng, resample hay nội suy.

**FACT về giá trị:** N có 5 giá trị hữu hạn mỗi kênh; A có 5 ở nhóm khác, client latency có 1–5 và server latency có 2–5. Vậy 5 hàng không luôn là 5 phép đo hữu hạn. 003.channel_checks giữ số hằng riêng; 230 source-window resource = 22×10 chính + 10 độ nhạy A, không là 230 ca. Front SuccessRate hằng ở N của 23/23 view; BARO bỏ cột hằng riêng N/A rồi lấy giao (RCAEval/e2e/baro.py:22–51; io/time_series.py:99–111), nên “có kênh” không bảo đảm “kênh được dùng”.

**CANDIDATE bộ kênh:**

1. BARO/SimpleRCA: **16 kênh pod** (19 trừ ba Node*) + **5 kênh front**, tổng 165 cột trước preprocess. Loại Node* vì thiếu NodeName/ownership để gán tín hiệu host vào service; lựa chọn này cần Minh duyệt. Giữ giá trị native, kể cả success rate; không chế error-count/error-rate. Tên service_suffix với suffix tường minh không có dấu gạch dưới, ví dụ CpuUsage-m, MemoryUsage-Mi, PodServerLatencyP90-s, FrontLatencyP90-s. Manifest giữ tên/đơn vị nguồn. Điều này tránh SimpleRCA rsplit dấu gạch dưới cuối khác P3 lấy tiền tố đầu (simplerca/adapter.py:45–54; p3/ban_ghi.py:7–9).
2. CIRCA: bốn kênh mỗi pod + front P90 ở bảng dưới, tối đa 41 nút trước preprocess. Đây là **chọn kênh khoa học**, không chỉ đổi tên. Không tự gán mọi cột khác làm S/L/E hoặc chế E từ success rate.
3. source_50/destination_50, dependency và ba Node* không vào gói này. Không kết luận chúng vô ích/sai; muốn dùng thêm cần bằng chứng clock/đơn vị/ownership và đề xuất khác.

| Kênh CIRCA đề xuất | Tên/loại builder | Đơn vị/giới hạn |
|---|---|---|
| CpuUsage(m) mỗi pod | service_cpu, S | Giữ số nguồn, m theo header; không chọn riêng CPU theo loại lỗi |
| MemoryUsage(Mi) mỗi pod | service_mem, S | CANDIDATE Mi×2^20→byte trước preprocess /10^6→MB. Không gán MemoryUsageRate(%) làm byte; quy ước Mi dựa header, collector còn chưa xác minh |
| PodWorkload(Ops) mỗi pod | service_workload, T | Giữ số/đơn vị nguồn; không tự coi counter để lấy sai phân |
| PodServerLatencyP90(s) mỗi pod | service_latency, L | Giữ giây; không gọi network delay/statusCode |
| LatencyP90(s) của Frontend | frontend_lat90, L | Khác pod server P90, không gộp hoặc chọn SLI theo root |

Builder chấp nhận các hậu tố này (src/circa_kien_truc/builder.py:8–25). Rate, syscall/network, client latency, percentile khác và success rate không vào CIRCA trong CANDIDATE này vì chưa có mapping nhiều-kênh/role được duyệt. Bộ cột khác nhau phải báo cạnh so sánh. SimpleRCA M4 cộng events theo kênh; usage/rate và percentile tương quan không là bằng chứng độc lập (core.py:69–72,100; WHY-27/33). Hàm một phía có thể không coi success rate giảm là alert; không đảo chiều kênh sau thấy thứ hạng.

### 0.5 — thời gian, thiếu và lặp theo từng phương pháp

**CANDIDATE BARO:** bảng biểu diễn 5N+5A theo thứ tự quan sát của từng nguồn sau cắt ns. Time tham chiếu từ front_service thật theo cùng thứ tự, chỉ là marker chia N/A; timestamp thật mỗi cột giữ riêng trong provenance. Không tuyên bố đo đồng thời, không union 110 timestamp rồi ffill để nhân quan sát, không lưới chung 1/15/60 s. BARO tính từng cột và time chỉ chia N/A (baro.py:22–51); equivalence wrapper **chưa kiểm** bằng fixture/lời gọi. Giữ P3 inf→NaN, ffill, fillna(0) trên 10 hàng đã cắt; đếm ô bù trong 10 quan sát, không thêm hàng. Cột hằng/thiếu theo code, không ép trả đủ U.

**CANDIDATE SimpleRCA:** arrays N/A riêng kênh vào core M4, trace/log cắt/split riêng nguồn. Không union hoặc điền metric; _finite bỏ nonfinite và báo số bỏ. Metric ≥2 hữu hạn N và ≥1 A; trace có duration hữu hạn hai phía; log chỉ cần A. Không kênh đủ→ValueError/ERROR; đủ nhưng tổng điểm 0→abstain/NO_EVIDENCE (core.py:39–41,63–110). Equivalence wrapper/core với adapter cũ còn chưa kiểm.

**CANDIDATE CIRCA — cần Minh giải quyết hợp đồng biên trước code:**

- Giữ Time_ns từng node; không bảng ordinal của BARO. Wrapper cũ zip một frame.time cho mọi node và int(current), không đáp ứng OB nguyên trạng (scoring.py:34–39; p3/adapters/circa.py:119). Preprocess trên hàng quan sát đã cắt của từng nguồn/kênh; không tạo giá trị ở timestamp nguồn khác; giữ thứ tự P3 và báo ô ffill/0/cột hằng/thiếu.
- Đề xuất chuyển chung gốc t→0 **chỉ cho scoring**, (Time_ns−t_ns)/10^9. Giữ ns nguyên để cắt/audit; kiểm roundtrip cả float vào pd.to_datetime của loader. Đây là đổi gốc tọa độ chung, không sửa lệch clock từng nguồn/ngày. Graph trace vẫn dùng t tuyệt đối và ns nguồn. Precision không đạt thì dừng, không floor Time/current.
- current là A thật cuối có giá trị hữu hạn của ít nhất một kênh đã chọn, giữ phần lẻ; không lấy điểm sau ffill làm quan sát thật. Ghi t/current_ns gốc. Giữ OLS/RHT/DA, prune, interval 1 s, train 111/test 10 điểm, SLI lex-first hiện hành; không chọn SLI theo root/frontend (scoring.py:39).
- Mỗi nguồn có 1–2 phép đo thật trong train theo 001. Loader toàn [t−120,current], resample 1 s, interpolate hai hướng/bfill **trước** split train (RCAEval/classes/data.py:89–104,175–176,225–238). 003 cho thấy **19/22 ca chính** và ca độ nhạy A có bin N cuối trước t−10. Nếu giữ anchor hữu hạn, đuôi train có thể dùng điểm A kế tiếp. Số điểm sau chọn kênh/preprocess **chưa kiểm** vì phiên này cấm loader; 111 không là phép đo thật/mẫu độc lập.
- **Biên phải OPEN ảnh hưởng kết quả:** 7/22 view chính và view A có last A thô của 11 nguồn nằm ở hơn một bin giây. current chung thật không bảo đảm mọi node có phép đo ở bin cuối; nguồn kết thúc sớm/NaN có thể được điền tới current. Câu “không có điểm điền ở biên phải” trong giao thức §6.5:182 không được bảo đảm với per-node này. **Khuyến nghị xin duyệt:** giữ loader gốc cho OB, khai riêng phần biên phải điền và phần train dùng anchor A; bổ sung ngoại lệ OB trong giao thức/WHY trước code. Phương án còn lại: giữ yêu cầu mọi node có điểm thật ở biên phải, chưa triển khai CIRCA tới khi có hợp đồng đáp ứng. Không tự bỏ node/đổi current để đạt.
- **Chưa kiểm** loader/scorer/route/số ô hiệu lực/equivalence. Giả định mapping/đơn vị đúng, precision đạt. Sai nếu Mi khác nghĩa header, relative float→datetime đổi ns hoặc wrapper khác preprocess/OLS/DA. Các phép kiểm này bắt buộc sau duyệt. Giữ Q-80/Q-82; nút >1e10 báo riêng, chưa gọi là lỗi làm tròn đã xác nhận trên OB.

**FACT về lặp; CANDIDATE chính sách:** giữ toàn bộ hàng giống hệt và provenance, không dedup chung. SimpleRCA dùng hàng cho đếm/quantile; MicroRank giữ multiplicity (__init__.py:38–56; graph.py:21–23); TraceRCA support/confidence đếm hàng (tracerca.py:73–77). CIRCA dedup lookup cha rồi cạnh là set (builder.py:35–44), là hành vi method. Nếu thấy xung đột mới, dừng reader/input để xác minh, không chọn phiên bản theo thứ hạng. Log–trace chỉ kiểm tương thích thời gian tương đối; nền sạch/recovery/đồng bộ tuyệt đối/−41 và −32 s theo ngày giữ OPEN. Không ghép construct N.

**TORAI B:** thiếu statusCode chặn tracets_err B (torai_b.py:60–73); stride metric mỗi 15 **hàng**, không 15 giây (torai_sua.py:102–112). Code B có 40 bin 15 s rồi fillna(0); bin không thu không là quan sát thật bằng 0. Không dựng giả field/bin, đổi stride, nội suy 1 s, bỏ trace để bật nhánh khác hoặc fallback A TT. TORAI có nhánh không trace (torai_sua.py:99,120,129) nhưng không chứng minh B đã khóa tương thích. **CANDIDATE:** mỗi ca/view một record UNSUPPORTED, variant B, seed null, nêu schema/cadence/luật TT; không tạo ba lượt đã chạy giả. Giữ ca ở mẫu số §8.3 và tách không hỗ trợ dữ liệu khỏi chất lượng xếp hạng.

### Bảng đề xuất cuối — chưa lựa chọn nào được duyệt

| Method | Nguồn/kênh | Ánh xạ/biểu diễn | Thiếu/lặp | Trạng thái dự kiến | Minh cần duyệt |
|---|---|---|---|---|---|
| BARO | 16/pod + 5 front | Alias, 165 cột, 5N+5A ordinal, marker Time front | P3 ffill/0 trên hàng thật, cột hằng qua code, giữ hàng | Chưa OK; trả rỗng→NO_EVIDENCE; ngoại lệ method→ERROR | Kênh/loại Node* và nguồn khác, Frontend alias, ordinal/marker |
| SimpleRCA M4 | Cùng metric; trace N/A start; log A | Arrays native, alias | Bỏ nonfinite, không điền, giữ lặp | Abstain→NO_EVIDENCE; thiếu mọi kênh/lỗi method→ERROR | Kênh, arrays wrapper và lặp; giữ M4 |
| MicroRank full (+top11) | Trace outer, split end | ID chuỗi, alias+OperationName nguyên | Giữ lặp, không thêm nền/operation | Mapping/N cơ học đạt; std/normal/anomaly/score/runtime chưa kiểm | Mapping/đơn vị; full chính và hợp đồng lỗi |
| TraceRCA hữu hạn | Trace như MicroRank | Cùng service/operation, ji gốc | Giữ lặp; lọc ji nonfinite theo adapter khóa | Operation mới→ERROR; rỗng hữu hạn→NO_EVIDENCE; chưa runtime | Mapping/đơn vị; không chữa N/công thức |
| CIRCA OLS+DA (+RHT) | 4/pod + front P90; graph trace N end | T/S/L, Time per-node; gốc scoring t→0; current A thật | Loader gốc 1 s; báo điền/train/biên/prune/route; graph lặp riêng | Chưa triển khai khi biên/precision chưa duyệt/kiểm; chưa mặc định OK/UNSUPPORTED | 41 kênh tối đa, mem, per-node wrapper, ngoại lệ biên/train hiệu lực |
| TORAI B | Không dựng đủ B hiện hành | Không áp ts-*/HTTP TT | Không giả field/bin/A TT | Đề xuất UNSUPPORTED B, chưa phát record | Policy ghi B/seed null; không chạy biến thể cứu |

Hash/selector/cắt/schema reader hoặc khóa/equivalence wrapper sai là lỗi runner; sửa trước bảng khoa học và giữ lượt hỏng. N ngắn không tự UNSUPPORTED. Chưa bảng method đã chạy, chất lượng xếp hạng hoặc kết luận đồ thị.

### Gói xin duyệt — file, thứ tự, kiểm và ảnh hưởng

**Khuyến nghị:** tiếp tục BARO/SimpleRCA/MicroRank/TraceRCA; CIRCA OLS có điều kiện duyệt biên phải và kiểm wrapper đạt; TORAI B không hỗ trợ cấu hình hiện hành. Giữ Q-84 ba bảng, A chỉ chạy thêm ca tranh chấp, B tái dùng 21 ca. Không đổi lựa chọn theo thứ hạng.

**Nguồn quyết định trước kết quả**, chỉ ghi sau duyệt đúng gói:

| File đề xuất sửa | Nội dung cụ thể | Ảnh hưởng |
|---|---|---|
| docs/DECISIONS.md | Quyết định mã kế tiếp: 5 method có điều kiện/TORAI B; U/alias; kênh/nguồn; biểu diễn từng method; lặp; biên CIRCA và audit quan sát/hiệu lực. Q-84 nguyên | Nguồn quyền triển khai; chưa ghi “Minh đã duyệt” |
| docs/WHY.md | Mục T-026: chọn/lý do/phương án/bằng chứng 001–003/giới hạn; Node* ownership, ordinal so union, per-node CIRCA, T/S/L, precision, train và biên điền | Mọi số OB/so RE2 phụ thuộc |
| results/T-022/giao-thuc-v2.md | Ghi chú OB §5/6.5/8.2: U/alias riêng, bảng marker, Time/current phần lẻ per-node; nếu duyệt thì ngoại lệ biên phải chỉ OB, báo node/ô điền | Làm rõ khung TT không đáp ứng, giữ hợp đồng TT/code gốc |

**File adapter/test/script đề xuất tạo**, chưa tạo:

| File | Nội dung |
|---|---|
| src/p3/nezha.py | Guard/selector Nezha riêng, mã mờ/path/hash; CSV lọc ns trước trả; provenance/alias/U/channel dictionary; coverage không dùng hull+1 TT |
| src/p3/adapters/nezha.py | BARO ordinal, Simple arrays, CIRCA per-node/relative và chẩn đoán tương đương; gọi trace adapters cũ; record §13; TORAI unsupported trước lời gọi |
| src/p3/nezha_worker.py | Worker nối reader/wrapper; không root vào method/job, ghi từng bước/chi phí/lỗi runner; giữ worker RE2 |
| results/T-026/tests/test_nezha.py | Fixture guard/hash/ns/alias/split/thiếu/lặp/conflict; BARO không nhân hàng; CIRCA current/relative datetime/train/biên/equivalence input đồng bộ |
| results/T-026/scripts/prepare_inputs.py | allowlist-dev.json, nhan-dev.json tách nhãn; mappings/manifest cấu hình/kênh/U; không chọn theo root |
| results/T-026/scripts/run_pilot.py | Pilot không nhãn §12 sau preprocess, chi phí/RSS/chẩn đoán; dừng theo ngưỡng chi phí đã có |
| results/T-026/scripts/run.py | Main/A theo SPEC, B tái dùng; tiến độ/timeout/hash/seed/mọi lượt; không evaluator |
| results/T-026/scripts/evaluate.py | Chốt manifest trước evaluator; ba bảng Q-84, U=10/13 ô dev thay cohort TT, hòa/bốn tập/nhóm CIRCA; nhãn giả và tính độc lập |
| results/T-026/scripts/report.py | Trạng thái/quan sát/hiệu lực/ca/ô/chi phí/so T-024; TORAI unsupported tách diễn giải chất lượng |

Đầu ra khác đúng SPEC: allowlist/nhãn/mappings/config, runs/lỗi, manifest chốt, cham-a.json/md, chi-phi.md, LOG và dòng STATE. Không sửa SPEC/code method/data/task khác hoặc commit/push; ba nguồn quyết định ở bảng là phạm vi bổ sung xin duyệt tường minh. Payload Nezha chỉ RAM hoặc work được SPEC cho phép sau duyệt; nếu ghi thì giữ manifest và xóa payload theo Q-59 trước bàn giao.

**Bản đồ ảnh hưởng/thứ tự:** nguồn quyết định/WHY/giao thức trước; reader/wrapper chỉ nhánh OB; fixture+57 test T-030 bảo vệ RE2; pilot cho chi phí thật; chạy/chốt/evaluator/báo cáo theo SPEC khi điều kiện đã duyệt đạt. Không dùng T-031 để gọi wrapper OB đã kiểm, không chạy lại T-024/T-025. Thiết kế cần khác gói thì dừng trình lại.

**Tiêu chí kiểm sau duyệt:**

- Guard reject 34 tên test trước I/O, mã sai/traversal/locked/TT/hash sai bị chặn. Job chỉ locator được phép; method không mã/path/root/fault.
- Time_ns nguyên; biên ns/hai mốc Q-84; membership ns→µs khớp. Relative float→datetime roundtrip precision đạt; không floor hoặc dịch clock.
- 5N/5A nguồn, BARO không nhân quan sát; Simple finite/drop đúng core; wrapper input đồng bộ khớp khóa/rank cũ; T-030 57/57 đạt/hash src/p3 mới.
- OperationName/ID/exact repeats giữ; fixture conflict/operation mới đúng code; không statusCode giả/construct nền.
- CIRCA OLS/RHT/DA gốc, current finite A thật/phần lẻ; từng node báo đo thật/grid/interpolate/ffill/0/bfill/biên/prune/anchor A train; route, >1e10, hashseed 0/1/2. Không suy train hiệu lực từ độ dài thô như T-025 R2.
- Pilot chọn không nhãn, giữ lỗi/soi trung gian; MicroRank ERROR báo Minh theo WHY-31; không chữa operation/ngưỡng. Đổi locator giữ nội dung phải khớp.
- Chốt record trước evaluator; nhãn giả/tính độc lập trước số thật; main/A/B đúng cohort; không dùng cận 1/22 cho hiệu/bootstrap. TORAI unsupported không giả lượt 3 seed.

**Chi phí — chưa kiểm:** SPEC:84 ước lượng 0,5–3 giờ máy, 0,5–3 GB RAM, 0,5–2 GB đĩa; chưa đo method OB để xác nhận/thu hẹp. 13,387 s của 003 không chiếu ranker. Pilot tối đa ba ca/method, timeout 3.600 s/lượt theo SPEC; chiếu theo phân bố yếu tố chi phí 22 ca, không trung vị×22. Lượt dự kiến/chiếu hơn một giờ báo và chờ Minh theo luật cứng 8.

**OPEN/điểm dừng:** Minh quyết gói, nhất là kênh/U/marker/lặp và biên phải CIRCA. Mốc tiêm thật/nền sạch/recovery/đồng bộ tuyệt đối/lệch trace theo ngày vẫn OPEN. Collector units/scrape-ID/ownership chưa xác minh nguồn độc lập; không điền unknown để đóng checklist. Dừng trước adapter/pilot/method/evaluator. Task chưa xong/chưa chờ phản biện, chưa prompt Claude chính thức.

### Bằng chứng máy — kiem-hop-dong-003

Chỉ thống kê/định danh, không payload/giá trị từng hàng. Unix ns nguyên trong JSON; số ô sau preprocess/loader là chưa kiểm.

<!-- T026_CONTRACT_JSON_START -->

{"run": "kiem-hop-dong-003", "scope": "0.4/0.5 input only; no loader/scorer/method/evaluator", "test_names_rejected_before_IO": 34, "files_hash_verified": 154, "elapsed_s": 13.387, "aliases_evidence": {"adservice-5f6585d649-fnmft": "adservice", "cartservice-579f59597d-wc2lz": "cartservice", "checkoutservice-578fcf4766-9csqn": "checkoutservice", "currencyservice-cf787dd48-vpjrd": "currencyservice", "emailservice-55fdc5b988-f6xth": "emailservice", "frontend-579b9bff58-t2dbm": "frontend", "paymentservice-9cdb6588f-554sm": "paymentservice", "productcatalogservice-668d5f85fb-wckp8": "productcatalogservice", "recommendationservice-6cfdd55578-gfj6q": "recommendationservice", "shippingservice-7b598fc7d-lmggd": "shippingservice", "productcatalogservice-668d5f85fb-jhwx9": "productcatalogservice"}, "metric_identifiers": {"online-boutique/rca_data/2022-08-22/metric/adservice-5f6585d649-fnmft_metric.csv": ["adservice-5f6585d649-fnmft"], "online-boutique/rca_data/2022-08-22/metric/cartservice-579f59597d-wc2lz_metric.csv": ["cartservice-579f59597d-wc2lz"], "online-boutique/rca_data/2022-08-22/metric/checkoutservice-578fcf4766-9csqn_metric.csv": ["checkoutservice-578fcf4766-9csqn"], "online-boutique/rca_data/2022-08-22/metric/currencyservice-cf787dd48-vpjrd_metric.csv": ["currencyservice-cf787dd48-vpjrd"], "online-boutique/rca_data/2022-08-22/metric/emailservice-55fdc5b988-f6xth_metric.csv": ["emailservice-55fdc5b988-f6xth"], "online-boutique/rca_data/2022-08-22/metric/front_service.csv": ["Frontend"], "online-boutique/rca_data/2022-08-22/metric/frontend-579b9bff58-t2dbm_metric.csv": ["frontend-579b9bff58-t2dbm"], "online-boutique/rca_data/2022-08-22/metric/paymentservice-9cdb6588f-554sm_metric.csv": ["paymentservice-9cdb6588f-554sm"], "online-boutique/rca_data/2022-08-22/metric/productcatalogservice-668d5f85fb-wckp8_metric.csv": ["productcatalogservice-668d5f85fb-wckp8"], "online-boutique/rca_data/2022-08-22/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv": ["recommendationservice-6cfdd55578-gfj6q"], "online-boutique/rca_data/2022-08-22/metric/shippingservice-7b598fc7d-lmggd_metric.csv": ["shippingservice-7b598fc7d-lmggd"], "online-boutique/rca_data/2022-08-23/metric/adservice-5f6585d649-fnmft_metric.csv": ["adservice-5f6585d649-fnmft"], "online-boutique/rca_data/2022-08-23/metric/cartservice-579f59597d-wc2lz_metric.csv": ["cartservice-579f59597d-wc2lz"], "online-boutique/rca_data/2022-08-23/metric/checkoutservice-578fcf4766-9csqn_metric.csv": ["checkoutservice-578fcf4766-9csqn"], "online-boutique/rca_data/2022-08-23/metric/currencyservice-cf787dd48-vpjrd_metric.csv": ["currencyservice-cf787dd48-vpjrd"], "online-boutique/rca_data/2022-08-23/metric/emailservice-55fdc5b988-f6xth_metric.csv": ["emailservice-55fdc5b988-f6xth"], "online-boutique/rca_data/2022-08-23/metric/front_service.csv": ["Frontend"], "online-boutique/rca_data/2022-08-23/metric/frontend-579b9bff58-t2dbm_metric.csv": ["frontend-579b9bff58-t2dbm"], "online-boutique/rca_data/2022-08-23/metric/paymentservice-9cdb6588f-554sm_metric.csv": ["paymentservice-9cdb6588f-554sm"], "online-boutique/rca_data/2022-08-23/metric/productcatalogservice-668d5f85fb-jhwx9_metric.csv": ["productcatalogservice-668d5f85fb-jhwx9"], "online-boutique/rca_data/2022-08-23/metric/recommendationservice-6cfdd55578-gfj6q_metric.csv": ["recommendationservice-6cfdd55578-gfj6q"], "online-boutique/rca_data/2022-08-23/metric/shippingservice-7b598fc7d-lmggd_metric.csv": ["shippingservice-7b598fc7d-lmggd"]}, "channel_checks": [{"kind": "front", "column": "LatencyP50(s)", "source_windows": 23, "finite_N_min_max": [5, 5], "finite_A_min_max": [5, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 0, "windows_A_constant_finite": 0}, {"kind": "front", "column": "LatencyP90(s)", "source_windows": 23, "finite_N_min_max": [5, 5], "finite_A_min_max": [5, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 0, "windows_A_constant_finite": 0}, {"kind": "front", "column": "LatencyP95(s)", "source_windows": 23, "finite_N_min_max": [5, 5], "finite_A_min_max": [5, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 0, "windows_A_constant_finite": 0}, {"kind": "front", "column": "LatencyP99(s)", "source_windows": 23, "finite_N_min_max": [5, 5], "finite_A_min_max": [5, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 0, "windows_A_constant_finite": 0}, {"kind": "front", "column": "SuccessRate(%)", "source_windows": 23, "finite_N_min_max": [5, 5], "finite_A_min_max": [5, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 23, "windows_A_constant_finite": 16}, {"kind": "resource", "column": "CpuUsage(m)", "source_windows": 230, "finite_N_min_max": [5, 5], "finite_A_min_max": [5, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 0, "windows_A_constant_finite": 0}, {"kind": "resource", "column": "CpuUsageRate(%)", "source_windows": 230, "finite_N_min_max": [5, 5], "finite_A_min_max": [5, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 0, "windows_A_constant_finite": 0}, {"kind": "resource", "column": "MemoryUsage(Mi)", "source_windows": 230, "finite_N_min_max": [5, 5], "finite_A_min_max": [5, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 144, "windows_A_constant_finite": 146}, {"kind": "resource", "column": "MemoryUsageRate(%)", "source_windows": 230, "finite_N_min_max": [5, 5], "finite_A_min_max": [5, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 144, "windows_A_constant_finite": 146}, {"kind": "resource", "column": "NetworkReceiveBytes", "source_windows": 230, "finite_N_min_max": [5, 5], "finite_A_min_max": [5, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 0, "windows_A_constant_finite": 0}, {"kind": "resource", "column": "NetworkTransmitBytes", "source_windows": 230, "finite_N_min_max": [5, 5], "finite_A_min_max": [5, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 0, "windows_A_constant_finite": 0}, {"kind": "resource", "column": "NodeCpuUsageRate(%)", "source_windows": 230, "finite_N_min_max": [5, 5], "finite_A_min_max": [5, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 0, "windows_A_constant_finite": 0}, {"kind": "resource", "column": "NodeMemoryUsageRate(%)", "source_windows": 230, "finite_N_min_max": [5, 5], "finite_A_min_max": [5, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 0, "windows_A_constant_finite": 0}, {"kind": "resource", "column": "NodeNetworkReceiveBytes", "source_windows": 230, "finite_N_min_max": [5, 5], "finite_A_min_max": [5, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 0, "windows_A_constant_finite": 0}, {"kind": "resource", "column": "PodClientLatencyP90(s)", "source_windows": 230, "finite_N_min_max": [5, 5], "finite_A_min_max": [1, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 17, "windows_A_constant_finite": 17}, {"kind": "resource", "column": "PodClientLatencyP95(s)", "source_windows": 230, "finite_N_min_max": [5, 5], "finite_A_min_max": [1, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 2, "windows_A_constant_finite": 2}, {"kind": "resource", "column": "PodClientLatencyP99(s)", "source_windows": 230, "finite_N_min_max": [5, 5], "finite_A_min_max": [1, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 0, "windows_A_constant_finite": 2}, {"kind": "resource", "column": "PodServerLatencyP90(s)", "source_windows": 230, "finite_N_min_max": [5, 5], "finite_A_min_max": [2, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 40, "windows_A_constant_finite": 34}, {"kind": "resource", "column": "PodServerLatencyP95(s)", "source_windows": 230, "finite_N_min_max": [5, 5], "finite_A_min_max": [2, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 6, "windows_A_constant_finite": 4}, {"kind": "resource", "column": "PodServerLatencyP99(s)", "source_windows": 230, "finite_N_min_max": [5, 5], "finite_A_min_max": [2, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 2, "windows_A_constant_finite": 2}, {"kind": "resource", "column": "PodSuccessRate(%)", "source_windows": 230, "finite_N_min_max": [5, 5], "finite_A_min_max": [5, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 230, "windows_A_constant_finite": 230}, {"kind": "resource", "column": "PodWorkload(Ops)", "source_windows": 230, "finite_N_min_max": [5, 5], "finite_A_min_max": [5, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 0, "windows_A_constant_finite": 0}, {"kind": "resource", "column": "SyscallRead", "source_windows": 230, "finite_N_min_max": [5, 5], "finite_A_min_max": [5, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 0, "windows_A_constant_finite": 0}, {"kind": "resource", "column": "SyscallWrite", "source_windows": 230, "finite_N_min_max": [5, 5], "finite_A_min_max": [5, 5], "windows_N_lt2": 0, "windows_A_empty": 0, "windows_N_constant_finite": 1, "windows_A_constant_finite": 0}], "cases": [{"case": "OB|adservice|cpu_contention|2022-08-23 16:31:35", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 383504636, "ordinal_skew_ns_max": 684313377, "front_anchor_max_abs_diff_ns": 684313377, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661272588254115716, "metric_last_A_ns_max": 1661272588900446612, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 0, "circa_train_tail_after_last_N_bin_points_max": 0}, {"case": "OB|checkoutservice|exception|2022-08-22 05:01:13", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 376415024, "ordinal_skew_ns_max": 788565274, "front_anchor_max_abs_diff_ns": 788565274, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661144719618007794, "metric_last_A_ns_max": 1661144720082048435, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 43, "circa_train_tail_after_last_N_bin_points_max": 44}, {"case": "OB|checkoutservice|exception|2022-08-23 13:02:09", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 383746314, "ordinal_skew_ns_max": 848512866, "front_anchor_max_abs_diff_ns": 848512866, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661259988131366987, "metric_last_A_ns_max": 1661259988911174628, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 31, "circa_train_tail_after_last_N_bin_points_max": 31}, {"case": "OB|checkoutservice|network_delay|2022-08-22 04:52:55", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 349850830, "ordinal_skew_ns_max": 759122209, "front_anchor_max_abs_diff_ns": 759122209, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661144239613508395, "metric_last_A_ns_max": 1661144240219877828, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 25, "circa_train_tail_after_last_N_bin_points_max": 26}, {"case": "OB|checkoutservice|network_delay|2022-08-23 12:53:52", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 383746314, "ordinal_skew_ns_max": 694136862, "front_anchor_max_abs_diff_ns": 694136862, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661259508117969465, "metric_last_A_ns_max": 1661259508501715779, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 14, "circa_train_tail_after_last_N_bin_points_max": 14}, {"case": "OB|checkoutservice|return|2022-08-22 05:09:50", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 350802173, "ordinal_skew_ns_max": 894812915, "front_anchor_max_abs_diff_ns": 894812915, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661145259615499446, "metric_last_A_ns_max": 1661145259966301619, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 20, "circa_train_tail_after_last_N_bin_points_max": 21}, {"case": "OB|checkoutservice|return|2022-08-23 13:10:36", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 449327955, "ordinal_skew_ns_max": 779807641, "front_anchor_max_abs_diff_ns": 779807641, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661260528127350773, "metric_last_A_ns_max": 1661260528813974138, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 0, "circa_train_tail_after_last_N_bin_points_max": 0}, {"case": "OB|emailservice|cpu_consumed|2022-08-23 14:03:48", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 415071121, "ordinal_skew_ns_max": 734125005, "front_anchor_max_abs_diff_ns": 734125005, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661263708170996641, "metric_last_A_ns_max": 1661263708905121646, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 10, "circa_train_tail_after_last_N_bin_points_max": 10}, {"case": "OB|emailservice|network_delay|2022-08-22 05:43:48", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 387212665, "ordinal_skew_ns_max": 684480468, "front_anchor_max_abs_diff_ns": 684480468, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661147299647887938, "metric_last_A_ns_max": 1661147300247356962, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 18, "circa_train_tail_after_last_N_bin_points_max": 19}, {"case": "OB|emailservice|network_delay|2022-08-23 13:54:37", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 399153374, "ordinal_skew_ns_max": 736950359, "front_anchor_max_abs_diff_ns": 736950359, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661263168166768149, "metric_last_A_ns_max": 1661263168631853296, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 0, "circa_train_tail_after_last_N_bin_points_max": 0}, {"case": "OB|frontend|return|2022-08-22 04:02:07", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 350283972, "ordinal_skew_ns_max": 822494259, "front_anchor_max_abs_diff_ns": 822494259, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661141179584545395, "metric_last_A_ns_max": 1661141179934829367, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 37, "circa_train_tail_after_last_N_bin_points_max": 38}, {"case": "OB|frontend|return|2022-08-23 12:10:21", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 332729310, "ordinal_skew_ns_max": 615864640, "front_anchor_max_abs_diff_ns": 615864640, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661256868098759933, "metric_last_A_ns_max": 1661256868585232943, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 43, "circa_train_tail_after_last_N_bin_points_max": 43}, {"case": "OB|paymentservice|cpu_contention|2022-08-22 06:01:18", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 332432051, "ordinal_skew_ns_max": 752802167, "front_anchor_max_abs_diff_ns": 752802167, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661148319642747171, "metric_last_A_ns_max": 1661148319975179222, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 48, "circa_train_tail_after_last_N_bin_points_max": 49}, {"case": "OB|paymentservice|cpu_contention|2022-08-23 14:21:54", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 417454322, "ordinal_skew_ns_max": 715755270, "front_anchor_max_abs_diff_ns": 715755270, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661264788178098061, "metric_last_A_ns_max": 1661264788757517813, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 16, "circa_train_tail_after_last_N_bin_points_max": 16}, {"case": "OB|productcatalogservice|exception|2022-08-23 15:04:28", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 355631903, "ordinal_skew_ns_max": 807148553, "front_anchor_max_abs_diff_ns": 807148553, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661267308192218107, "metric_last_A_ns_max": 1661267308613600584, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 50, "circa_train_tail_after_last_N_bin_points_max": 50}, {"case": "OB|recommendationservice|cpu_consumed|2022-08-22 07:10:43", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 379280714, "ordinal_skew_ns_max": 762342496, "front_anchor_max_abs_diff_ns": 762342496, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661152519683909177, "metric_last_A_ns_max": 1661152520063189891, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 13, "circa_train_tail_after_last_N_bin_points_max": 14}, {"case": "OB|recommendationservice|cpu_consumed|2022-08-23 15:29:49", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 348070775, "ordinal_skew_ns_max": 691143610, "front_anchor_max_abs_diff_ns": 691143610, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661268868215134679, "metric_last_A_ns_max": 1661268868707294944, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 11, "circa_train_tail_after_last_N_bin_points_max": 11}, {"case": "OB|recommendationservice|network_delay|2022-08-22 06:52:56", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 339038065, "ordinal_skew_ns_max": 786681514, "front_anchor_max_abs_diff_ns": 786681514, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661151439698106011, "metric_last_A_ns_max": 1661151440273318169, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 26, "circa_train_tail_after_last_N_bin_points_max": 27}, {"case": "OB|recommendationservice|network_delay|2022-08-23 15:12:49", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 421382477, "ordinal_skew_ns_max": 804107224, "front_anchor_max_abs_diff_ns": 804107224, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661267848220123720, "metric_last_A_ns_max": 1661267849024230944, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 11, "circa_train_tail_after_last_N_bin_points_max": 11}, {"case": "OB|shippingservice|cpu_consumed|2022-08-23 15:56:24", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 512692779, "ordinal_skew_ns_max": 786860610, "front_anchor_max_abs_diff_ns": 786860610, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661270428238165998, "metric_last_A_ns_max": 1661270428823878271, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 46, "circa_train_tail_after_last_N_bin_points_max": 46}, {"case": "OB|shippingservice|cpu_contention|2022-08-22 07:26:48", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 317031394, "ordinal_skew_ns_max": 636186051, "front_anchor_max_abs_diff_ns": 636186051, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661153479696700436, "metric_last_A_ns_max": 1661153480279898384, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 19, "circa_train_tail_after_last_N_bin_points_max": 19}, {"case": "OB|shippingservice|cpu_contention|2022-08-23 15:47:43", "view": "main", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 348657204, "ordinal_skew_ns_max": 782742376, "front_anchor_max_abs_diff_ns": 782742376, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661269948220307405, "metric_last_A_ns_max": 1661269948870306430, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 4, "circa_train_tail_after_last_N_bin_points_max": 5}, {"case": "OB|recommendationservice|cpu_consumed|2022-08-22 07:10:43", "view": "sensitivity_A", "exact_common_times": 0, "union_times": 110, "ordinal_skew_ns_min": 363639523, "ordinal_skew_ns_max": 762342496, "front_anchor_max_abs_diff_ns": 762342496, "ordinal_NA_same": true, "metric_last_A_ns_min": 1661152459668554513, "metric_last_A_ns_max": 1661152460141489652, "trace_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "log_services": ["adservice", "cartservice", "checkoutservice", "currencyservice", "emailservice", "frontend", "paymentservice", "productcatalogservice", "recommendationservice", "shippingservice"], "method_operations": 55, "operation_service_collisions": 0, "mapped_A_operations_without_N": 0, "mapped_N_operations_rows_lt2": 0, "mapped_N_operations_unique_spans_lt2": 0, "circa_train_tail_after_last_N_bin_points_min": 13, "circa_train_tail_after_last_N_bin_points_max": 14}], "derived_payload_files": []}

<!-- T026_CONTRACT_JSON_END -->
