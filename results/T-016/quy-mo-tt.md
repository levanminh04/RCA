# TORAI và RCD ở quy mô Train Ticket

T-016, yêu cầu 5. Lý do làm (SL33): RE2-TT là ứng viên dataset chính, nhưng T-006/T-007 chỉ kiểm trên Online Boutique, Sock Shop.

## 1. Dữ liệu dùng, và chứng minh trùng ca dev

- `D:\RCA-ext\data\torai-TT\ts-route-service_socket\1` (T-005 đã giải nén) và 29 ca khác cùng tên 10 ô dev × 3, giải nén từ `D:\RCA-ext\dl\torai-data.zip` vào `D:\RCA-ext\work\T-016\data\torai-TT\` (chỉ 30 thư mục này; zip có 90 thư mục `torai-TT`, gồm ca test, không giải nén).
- Trước khi chạy: **30/30 ca trùng ca dev RE2-TT** trong `data/rcaeval/re2tt_*`: cùng 376 cột, cùng mốc thời gian, mốc tiêm = đầu file + 720 s (hoặc bằng `inject_time.txt` nếu ca dev có), 0 ô metric lệch quá ngưỡng làm tròn (sai số tương đối lớn nhất ≤ 1,04e-13) (`runs/s10-cung-ca.json`, `runs/s0-cung-ca.json`).
- Kết quả trên 30 ca dev chỉ dùng để chẩn đoán. Không so với Bảng 4 bài TORAI được: bảng tính trên 90 ca, 60 ca còn lại là test, không được mở.

## 2. Kích thước đầu vào

Ca `ts-route-service_socket/1`, cửa sổ 10 (`D:\RCA-ext\work\T-016\ec2\s11-tt-*`): metric 600 × 348 cột (sau khi `main.py` chỉ giữ cột `ts-*` và bỏ `*_latency-50`), logts 40 × 178, tracets 40 × 158 mỗi bảng. Metric không hằng: 272–301 cột mỗi ca (`runs/s4-soi-dau-vao-TT-len10.jsonl`).

**Ứng viên: 68** mỗi ca (bài Bảng 1: 64 service). Trong 68 có 26 database (`ts-*-mongo`, `ts-food-mysql`, `ts-voucher-mysql`) và `ts-ui-dashboard`. Không có va chạm tiền tố (các tên đều kết thúc bằng `-service`, `-mongo`, `-mysql`).

## 3. Lỗi giảm mẫu ở TT

Như OB, SS (`giam-mau-hai-lan.md` mục 3): cửa sổ 10, bản gốc đưa 0 cột metric vào RCD ở 30/30 ca; cửa sổ 20, 257–267 cột sống sót trên 3 + 3 dòng. Bản sửa: 7–220 cột metric mỗi cụm (TB 113,3) ở cửa sổ 10.

## 4. Kết quả trên 30 ca dev (3 seed; `cham/s10-tong-hop.json`)

| Cấu hình | AC@1 | AC@3 | Avg@5 | Cụm dự phòng / cụm ≥ 2 service (seed 0) | Ca thứ hạng = chỉ mức nghiêm trọng | SeverityScorer không cụm (Avg@5) |
|---|---|---|---|---|---|---|
| gốc 10 | 0,700 | 0,933 | 0,880 | 72 / 72 | 30 / 30 | 0,873 |
| sửa 10 | 0,700 | 0,933 | 0,880 | 67 / 72 | 28 / 30 | 0,873 |
| gốc 20 | 0,733 | 0,833 | 0,820 | 81 / 85 | 27 / 30 | 0,820 |
| sửa 20 | 0,733 | 0,800 | 0,813 | 78 / 85 | 25 / 30 | 0,820 |

- Mọi lượt chạy hết, 0 lỗi, 0 rỗng; không gặp `assert min_nodes < len(data)` dù cụm có tới 220 cột metric. Lý do: số dòng vào RCD (40 với cửa sổ 10, 80 với cửa sổ 20) vẫn lớn hơn số biến ở pha 2. Pha 2 có thể nhận hơn 5 biến: mức cuối của pha 1 còn tới 29 cột (bản trước viết sai "pha 2 chỉ nhận ≤ 5 biến"; sửa theo tự soát N1).
- GMM chọn 2–9 cụm; **cụm lớn nhất tới 57 service**. Với cụm lớn như vậy, RCD gần như không bao giờ trả đủ 57 service, nên chắc chắn rơi nhánh dự phòng: ở TT, CausalRanker thực tế không đóng góp.
- Theo lỗi (Avg@5, gốc 10): CPU 0,900, MEM 1,000, DISK 1,000, SOCKET 1,000, DELAY 0,600, LOSS 0,900 (`cham/bang-so-cong-bo.md`). Lỗi mạng (DELAY) yếu nhất — chỉ ghi nhận, phân tích là việc của P4 (chưa kiểm).

**RCD (biến thể), 30 ca dev, cửa sổ 10, seed 0** (EC2; SPEC "Thay đổi trong lúc làm" mục 4; `cham/s11-tt30-rcd-len10.json`): AC@1 0,133; AC@3 0,267; Avg@5 **0,240**; đầu ra 1–18 metric; 0 lỗi. Theo lỗi Avg@5: CPU 0,333, MEM 0,333, DISK 0,533, SOCKET 0, DELAY 0, LOSS 0,167. Ví dụ ca `ts-route-service_socket/1`: RCD trả 5 metric `ts-assurance-mongo_mem, ts-order-service_socket, ts-user-service_mem, ts-ticketinfo-service_socket, ts-execute-service_diskio`, không có service gốc; TORAI cùng ca xếp service gốc hạng 1. Ở quy mô TT, RCD trên toàn bộ metric gần như không tìm ra service gốc; một seed, 30 ca dev, không so được với bài (Bảng 4 gồm ca test).

**Linux và Windows ở TT:** TORAI gốc, sửa cửa sổ 10 seed 0: 30/30 ca giống hệt (`runs/s11-linux-vs-win-tt30-torai-*.json`).

## 5. Chi phí

| Lượt | Máy | Thời gian | Mốc bài Bảng 8 (TT, giây/ca) |
|---|---|---|---|
| TORAI gốc, 30 ca dev, cửa sổ 10 | EC2 (rảnh) | TB 1,51 s/ca, lớn nhất 3,3 s (tổng 45 s) | 20,59 |
| TORAI sửa, 30 ca dev, cửa sổ 10 | EC2 | TB 2,19 s/ca, lớn nhất 3,5 s (tổng 66 s) | — |
| RCD, 30 ca dev, cửa sổ 10 | EC2 | TB 49,4 s/ca, lớn nhất 126,1 s (tổng 1 482 s) | 20,87 |
| TORAI 30 ca, gốc / sửa, cửa sổ 10 | laptop (tải nặng, không chính thức) | TB 8,8 / 9,0 s/ca, lớn nhất 35,9 / 15,5 s | |
| TORAI 30 ca, gốc / sửa, cửa sổ 20 | laptop | TB 8,2 / 5,8 s/ca | |

Ước lượng tổng cho P3 (chưa kiểm, quy về tổng theo SL27): TORAI bản sửa trên 90 ca TT khoảng 90 × 2–10 s ≈ 3–15 phút mỗi seed; 3 seed dưới 1 giờ; trong ngân sách Q-40. RCD trên TT: 49 s/ca trên EC2 (`runs/s11-tt30-thoi-gian.txt`) → khoảng 74 phút cho 90 ca, mỗi seed; 2 seed khoảng 2,5 giờ, 3 seed khoảng 3,7 giờ (vượt trần Q-40).

## 6. Điều chưa kiểm và hệ quả

- Không so được với Bảng 4 (ca test). Hệ quả: chỉ biết TORAI chạy được, ổn định và hành vi trung gian ở quy mô TT; không biết nó tái lập số công bố trên TT.
- RCD chỉ chạy 1 seed trên 30 ca dev. Hệ quả: chưa biết dao động của RCD ở TT; với dao động lớn của RCD ở OB, SS (`ngau-nhien.md` mục 5), số 0,240 chỉ là một lần đo.
