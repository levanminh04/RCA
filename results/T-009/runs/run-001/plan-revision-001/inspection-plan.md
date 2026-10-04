# Kế hoạch kiểm file — CANDIDATE chưa kiểm

Chưa được tải/đọc telemetry. Q-46 chỉ nói LEMMA metadata; không cấp quyền Nezha/Eadro. Chủ quyết định: Minh. Kế hoạch chọn theo đường dẫn/nhãn/byte trước số đo; không chọn ca vì kết quả đẹp. File đầy đủ, URL và byte ở [proposed_files.json](runs/run-001/proposed_files.json).

Phương án ít byte đường truyền: tải đúng hai ZIP, xác minh MD5 từ Zenodo rồi kiểm từng member/CRC; không tải đồng thời từng member và ZIP. Proposed_files là inventory thành phần cần kiểm, không phải yêu cầu tải lặp. Giải nén nested có thể tăng dung lượng và lặp nội dung; phải census tên/hash trước chọn corpus.

| Hệ | Member dự kiến | Byte member ngoài cộng | Sự kiện nhãn ngoài |
|---|---:|---:|---:|
| TT | 265 | 617,529,959 | 81 |
| SN | 60 | 669,476,230 | 36 |

ZIP tải dự kiến (chưa duyệt): SN Dataset.zip = 78,753,809 byte; TT Dataset.zip = 48,923,113 byte. Tổng 127,676,922 byte; checksum nguồn trong sources/zenodo.json.


Mẫu schema đầu tiên dưới đây chỉ để xác minh định dạng, chọn file nhỏ nhất theo byte rồi đường dẫn trong từng hệ/nhóm; không dùng mẫu này kết luận chất lượng toàn bộ. Khi được đọc và định dạng hợp lệ, tiếp phạm vi đầy đủ trên để kiểm mỗi root tại ca nó là root. Với Eadro, no-fault nằm nested: schema/nhãn nested chưa biết, không giả định cùng fault-phase.

| Hệ | File mẫu dự kiến | Byte |
|---|---|---:|
| TT | `TT Dataset/no fault/TT-no-fault.txz` | 2,378,304 |
| TT | `TT Dataset/data/TT.2022-04-18T150729D2022-04-18T165511/logs.json` | 1,065,147 |
| TT | `TT Dataset/data/TT.2022-04-18T150729D2022-04-18T165511/metrics/ts-order-other-service.csv` | 524,184 |
| TT | `TT Dataset/data/TT.2022-04-19T001753D2022-04-19T020534/spans.json` | 41,246,373 |
| SN | `SN Dataset/no fault/SN.2022-04-20T182405D2022-04-20T184806.tar.xz` | 7,362,264 |
| SN | `SN Dataset/data/SN.2022-04-17T190213D2022-04-17T192544/logs.json` | 1,089,651 |
| SN | `SN Dataset/data/SN.2022-04-17T183729D2022-04-17T190100/metrics/unique-id-service.csv` | 118,305 |
| SN | `SN Dataset/data/SN.2022-04-17T190213D2022-04-17T192544/spans.json` | 138,591,913 |

Các bước sau quyền đọc: xác minh hash/CRC → schema → kiểm clock/nhãn/biên → parent unique bằng (trace,span) với sentinel tách riêng → graph ca và bậc root → mapping ba nguồn → normal/cadence/NaN/gap/constant → probe theo SPEC nếu quyền đọc cho phép. Không chạy RCA, không tự sửa clock hoặc nhãn. Nếu mâu thuẫn ảnh hưởng phép chấm, dừng phần phụ thuộc và trình Minh.

Giả định chưa kiểm: các file thuộc cùng revision sử dụng schema tương thích; sai khi instrumentation thay giữa ngày hoặc nested release khác. Thời gian/RAM chưa đo; chia bước ngắn có thời gian, không khởi chạy lượt quá một giờ trước duyệt. Số liệu toàn bộ/chất lượng/lan còn OPEN cho tới phép kiểm thật. Nếu Minh chọn giữ ngoài, chỉ schema/nhãn theo quyền cụ thể; tiêu chí 7 để G3.
