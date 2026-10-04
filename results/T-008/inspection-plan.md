# Phạm vi đã kiểm theo Q-47

Đã tải và kiểm toàn 1.165 CSV của bốn ngày, không còn chờ quyền. Thẻ cuối và các run evidence-002/symptoms-003/trace-symptoms-002 ghi kết quả và giới hạn. Các đoạn dưới giữ kế hoạch trước khi Q-47 duyệt, không dùng trạng thái lịch sử làm kết luận hiện tại.

---

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
| OB | `construct_data/2022-08-22/metric/front_service.csv` | 187,712 |
| OB | `construct_data/2022-08-22/log/03_51_log.csv` | 12,965,305 |
| OB | `construct_data/2022-08-22/metric/emailservice-55fdc5b988-f6xth_metric.csv` | 430,468 |
| OB | `construct_data/2022-08-22/metric/dependency.csv` | 814 |
| OB | `construct_data/2022-08-22/trace/03_51_trace.csv` | 4,261,034 |
| OB | `construct_data/2022-08-22/traceid/03_51_traceid.csv` | 16,499 |
| OB | `construct_data/2022-08-23/metric/front_service.csv` | 112,586 |
| OB | `construct_data/2022-08-23/log/17_00_log.csv` | 12,442,369 |
| OB | `construct_data/2022-08-23/metric/adservice-5f6585d649-fnmft_metric.csv` | 198,291 |
| OB | `construct_data/2022-08-23/metric/dependency.csv` | 814 |
| OB | `construct_data/2022-08-23/trace/17_00_trace.csv` | 4,105,111 |
| OB | `construct_data/2022-08-23/traceid/17_00_traceid.csv` | 16,499 |
| OB | `rca_data/2022-08-22/metric/front_service.csv` | 187,712 |
| OB | `rca_data/2022-08-22/log/05_20_log.csv` | 2,977,309 |
| OB | `rca_data/2022-08-22/metric/emailservice-55fdc5b988-f6xth_metric.csv` | 430,468 |
| OB | `rca_data/2022-08-22/metric/dependency.csv` | 814 |
| OB | `rca_data/2022-08-22/trace/05_20_trace.csv` | 954,814 |
| OB | `rca_data/2022-08-22/traceid/05_20_traceid.csv` | 3,828 |
| OB | `rca_data/2022-08-23/metric/front_service.csv` | 112,586 |
| OB | `rca_data/2022-08-23/log/13_29_log.csv` | 3,664,450 |
| OB | `rca_data/2022-08-23/metric/adservice-5f6585d649-fnmft_metric.csv` | 198,291 |
| OB | `rca_data/2022-08-23/metric/dependency.csv` | 814 |
| OB | `rca_data/2022-08-23/trace/15_06_trace.csv` | 1,189,188 |
| OB | `rca_data/2022-08-23/traceid/13_29_traceid.csv` | 4,686 |
| TT | `construct_data/2023-01-29/metric/front_service.csv` | 126,560 |
| TT | `construct_data/2023-01-29/log/08_50_log.csv` | 1,695,007 |
| TT | `construct_data/2023-01-29/metric/ts-avatar-service-694fdc47c4-ppnsr_metric.csv` | 203,826 |
| TT | `construct_data/2023-01-29/trace/08_50_trace.csv` | 840,259 |
| TT | `construct_data/2023-01-29/traceid/08_50_traceid.csv` | 2,177 |
| TT | `construct_data/2023-01-30/metric/front_service.csv` | 101,522 |
| TT | `construct_data/2023-01-30/log/11_39_log.csv` | 2,159,606 |
| TT | `construct_data/2023-01-30/metric/ts-avatar-service-694fdc47c4-g7mwc_metric.csv` | 164,526 |
| TT | `construct_data/2023-01-30/trace/11_39_trace.csv` | 792,660 |
| TT | `construct_data/2023-01-30/traceid/11_39_traceid.csv` | 2,013 |
| TT | `rca_data/2023-01-29/metric/front_service.csv` | 126,560 |
| TT | `rca_data/2023-01-29/log/10_20_log.csv` | 141,253 |
| TT | `rca_data/2023-01-29/metric/ts-avatar-service-694fdc47c4-ppnsr_metric.csv` | 203,826 |
| TT | `rca_data/2023-01-29/trace/10_20_trace.csv` | 103,628 |
| TT | `rca_data/2023-01-29/traceid/10_20_traceid.csv` | 858 |
| TT | `rca_data/2023-01-30/metric/front_service.csv` | 101,522 |
| TT | `rca_data/2023-01-30/log/13_15_log.csv` | 215,323 |
| TT | `rca_data/2023-01-30/metric/ts-avatar-service-694fdc47c4-g7mwc_metric.csv` | 164,526 |
| TT | `rca_data/2023-01-30/trace/13_15_trace.csv` | 123,133 |
| TT | `rca_data/2023-01-30/traceid/13_17_traceid.csv` | 1,023 |

Các mẫu trên là mẫu schema độc lập; log/trace/metric có thể thuộc cửa sổ khác nhau. Không dùng chúng để tính parent/log linkage hay so đồng thời ba nguồn.

Phân loại file trước khi đọc: `*_metric.csv` là ứng viên metric tài nguyên vì `sources/alarm.py` dòng 41/62–63 và 265–275 chọn tên chứa metric, đọc CpuUsageRate(%), MemoryUsageRate(%), Time, PodName; generate_threshold còn yêu cầu SyscallRead/SyscallWrite. `dependency.csv` được giữ riêng như ứng viên cấu trúc/mapping theo tên, nội dung chưa kiểm. `front_service.csv`/destination_50.csv là nhóm ứng viên application, không thay mẫu resource. Mọi schema vẫn chưa xác minh trên file.

Mẫu ghép đa nguồn đề xuất riêng, chọn trước bằng metadata. Nezha dùng cùng phase/ngày và tên cửa sổ log/trace/traceid, cộng mọi file resource metric của phase/ngày; Eadro dùng cùng phiên chứa spans/logs/metrics. Tên cửa sổ giống nhau chưa chứng minh clock hay khoảng đo trùng: phải kiểm timestamp thực sau quyền đọc, rồi mới tính liên kết; nếu không trùng thì dừng kết luận linkage. Các file này đều đã nằm trong toàn corpus đề xuất, không thêm hoặc giảm phạm vi.

| Hệ | Nhóm/cửa sổ | Số file | Byte |
|---|---|---:|---:|
| OB | `construct_data/2022-08-22` / 03_51 | 13 | 21,799,549 |
| OB | `construct_data/2022-08-23` / 17_00 | 13 | 19,201,918 |
| OB | `rca_data/2022-08-22` / 03_53 | 13 | 21,277,035 |
| OB | `rca_data/2022-08-23` / 12_01 | 13 | 19,853,672 |
| TT | `construct_data/2023-01-29` / 08_50 | 49 | 16,329,386 |
| TT | `construct_data/2023-01-30` / 11_39 | 49 | 14,125,917 |
| TT | `rca_data/2023-01-29` / 08_43 | 49 | 16,189,413 |
| TT | `rca_data/2023-01-30` / 11_51 | 49 | 13,478,406 |

Đường dẫn/URL/byte từng file ghép: [paired_samples_proposed.json](runs/run-001/paired_samples_proposed.json). Mẫu ghép chỉ kiểm cơ chế đọc/ghép ở cửa sổ này; chất lượng toàn corpus và vị trí mỗi root vẫn cần kiểm toàn phần được duyệt.

Các bước sau quyền đọc: xác minh hash/CRC → schema → kiểm clock/nhãn/biên → parent unique bằng (trace,span) với sentinel tách riêng → graph ca và bậc root → mapping ba nguồn → normal/cadence/NaN/gap/constant → probe theo SPEC nếu quyền đọc cho phép. Không chạy RCA, không tự sửa clock hoặc nhãn. Nếu mâu thuẫn ảnh hưởng phép chấm, dừng phần phụ thuộc và trình Minh.

Giả định chưa kiểm: các file thuộc cùng revision sử dụng schema tương thích; sai khi instrumentation thay giữa ngày hoặc nested release khác. Thời gian/RAM chưa đo; chia bước ngắn có thời gian, không khởi chạy lượt quá một giờ trước duyệt. Số liệu toàn bộ/chất lượng/lan còn OPEN cho tới phép kiểm thật. Nếu Minh chọn giữ ngoài, chỉ schema/nhãn theo quyền cụ thể; tiêu chí 7 để G3.
