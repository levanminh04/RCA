# Kế hoạch kiểm file — CANDIDATE chưa kiểm

Chưa được tải/đọc telemetry. Q-46 chỉ nói LEMMA metadata; không cấp quyền Nezha/Eadro. Chủ quyết định: Minh. Kế hoạch chọn theo đường dẫn/nhãn/byte trước số đo; không chọn ca vì kết quả đẹp. File đầy đủ, URL và byte ở [proposed_files.json](runs/run-001/proposed_files.json).

Phương án phủ đầy đủ nếu Minh cho phép: toàn bộ metric/trace/log/traceid của bốn ngày trong revision ghim, cả construct_data và rca_data. Phủ toàn bộ event/root/fault/repetition đã đếm; không dùng một ca để suy toàn bộ. Chưa chạy downloader telemetry; script metadata từ chối URL này.

| Hệ | File | Byte raw | Ca nhãn được phủ |
|---|---:|---:|---:|
| OB | 566 | 2,677,369,464 | 56 |
| TT | 599 | 360,765,178 | 45 |

Mẫu schema đầu tiên dưới đây chỉ để xác minh định dạng, chọn file nhỏ nhất theo byte rồi đường dẫn trong từng hệ/nhóm; không dùng mẫu này kết luận chất lượng toàn bộ. Khi được đọc và định dạng hợp lệ, tiếp phạm vi đầy đủ trên để kiểm mỗi root tại ca nó là root. Với Eadro, no-fault nằm nested: schema/nhãn nested chưa biết, không giả định cùng fault-phase.

| Hệ | File mẫu dự kiến | Byte |
|---|---|---:|
| OB | `construct_data/2022-08-22/log/03_51_log.csv` | 12,965,305 |
| OB | `construct_data/2022-08-22/metric/dependency.csv` | 814 |
| OB | `construct_data/2022-08-22/trace/03_51_trace.csv` | 4,261,034 |
| OB | `construct_data/2022-08-22/traceid/03_51_traceid.csv` | 16,499 |
| OB | `construct_data/2022-08-23/log/17_00_log.csv` | 12,442,369 |
| OB | `construct_data/2022-08-23/metric/dependency.csv` | 814 |
| OB | `construct_data/2022-08-23/trace/17_00_trace.csv` | 4,105,111 |
| OB | `construct_data/2022-08-23/traceid/17_00_traceid.csv` | 16,499 |
| OB | `rca_data/2022-08-22/log/05_20_log.csv` | 2,977,309 |
| OB | `rca_data/2022-08-22/metric/dependency.csv` | 814 |
| OB | `rca_data/2022-08-22/trace/05_20_trace.csv` | 954,814 |
| OB | `rca_data/2022-08-22/traceid/05_20_traceid.csv` | 3,828 |
| OB | `rca_data/2022-08-23/log/13_29_log.csv` | 3,664,450 |
| OB | `rca_data/2022-08-23/metric/dependency.csv` | 814 |
| OB | `rca_data/2022-08-23/trace/15_06_trace.csv` | 1,189,188 |
| OB | `rca_data/2022-08-23/traceid/13_29_traceid.csv` | 4,686 |
| TT | `construct_data/2023-01-29/log/08_50_log.csv` | 1,695,007 |
| TT | `construct_data/2023-01-29/metric/front_service.csv` | 126,560 |
| TT | `construct_data/2023-01-29/trace/08_50_trace.csv` | 840,259 |
| TT | `construct_data/2023-01-29/traceid/08_50_traceid.csv` | 2,177 |
| TT | `construct_data/2023-01-30/log/11_39_log.csv` | 2,159,606 |
| TT | `construct_data/2023-01-30/metric/front_service.csv` | 101,522 |
| TT | `construct_data/2023-01-30/trace/11_39_trace.csv` | 792,660 |
| TT | `construct_data/2023-01-30/traceid/11_39_traceid.csv` | 2,013 |
| TT | `rca_data/2023-01-29/log/10_20_log.csv` | 141,253 |
| TT | `rca_data/2023-01-29/metric/front_service.csv` | 126,560 |
| TT | `rca_data/2023-01-29/trace/10_20_trace.csv` | 103,628 |
| TT | `rca_data/2023-01-29/traceid/10_20_traceid.csv` | 858 |
| TT | `rca_data/2023-01-30/log/13_15_log.csv` | 215,323 |
| TT | `rca_data/2023-01-30/metric/front_service.csv` | 101,522 |
| TT | `rca_data/2023-01-30/trace/13_15_trace.csv` | 123,133 |
| TT | `rca_data/2023-01-30/traceid/13_17_traceid.csv` | 1,023 |

Các bước sau quyền đọc: xác minh hash/CRC → schema → kiểm clock/nhãn/biên → parent unique bằng (trace,span) với sentinel tách riêng → graph ca và bậc root → mapping ba nguồn → normal/cadence/NaN/gap/constant → probe theo SPEC nếu quyền đọc cho phép. Không chạy RCA, không tự sửa clock hoặc nhãn. Nếu mâu thuẫn ảnh hưởng phép chấm, dừng phần phụ thuộc và trình Minh.

Giả định chưa kiểm: các file thuộc cùng revision sử dụng schema tương thích; sai khi instrumentation thay giữa ngày hoặc nested release khác. Thời gian/RAM chưa đo; chia bước ngắn có thời gian, không khởi chạy lượt quá một giờ trước duyệt. Số liệu toàn bộ/chất lượng/lan còn OPEN cho tới phép kiểm thật. Nếu Minh chọn giữ ngoài, chỉ schema/nhãn theo quyền cụ thể; tiêu chí 7 để G3.
