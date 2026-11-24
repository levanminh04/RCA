Đã sửa hai lỗi trong bộ chấm W4 v2c. Chỉ tạo ba tệp mới và chỉ chạy trên ca giả.

- **CX-33 A.** Khi bắt đầu chấm ở giây 70, sự cố vào Alerting ở giây 80 vẫn được liệt kê với lớp `khoe-x1`. Tỷ lệ sửa từ **1 sự cố/1 phút** thành **0 sự cố/1 phút**. Phút duy nhất đủ điều kiện là `[120,180)`. Ca đối chứng vào Alerting đúng giây 120 vẫn được tính.
- **CX-33b D.** Khi thiếu các bước từ giây 30 đến 110, hai lịch sử khớp toàn bộ phần quan sát cho tử số lần lượt là **0** và **1**. Bản cũ trả **1**. Bản v2c gắn cờ thiếu lịch sử và trả **chưa phân xử**. Muốn chốt tử số cần lịch sử trạng thái Grafana.
- **Hồi quy.** Cả 9/9 ca cũ đạt trên bản gốc và v2c. `len(khoang_chay)` khớp kỳ vọng `[0, 1, 2, 2, 2, 2, 2, 2]`. Chạy lại cho biên bản giống từng byte. Cả sáu hash mã thực chạy trong biên bản đều khớp.

| Tệp mới | SHA-256 |
|---|---|
| [cham_offline_v2c.py](D:/RCA-flashticket/results/T-072/v2/cham_offline_v2c.py) | `cba0c1b0f31c71c5725425da746ca5712754fbd2fc2c16430116eef5b5bf7c48` |
| [thu_ca_gia_v2c.py](D:/RCA-flashticket/results/T-072/v2/thu_ca_gia_v2c.py) | `b2dc2213bfe8a0433ec2a24d88d71a5e17c61dab7a2357fc755df2208bb78188` |
| [ra/thu-ca-gia-v2c.txt](D:/RCA-flashticket/results/T-072/v2/ra/thu-ca-gia-v2c.txt) | `336e4ed183c28cc26786c4b20bd748a93b68a5f6be269c13e4e39ca2c24fd532` |

Bản v2c chờ phiên Codex khác kiểm độc lập. Lệnh tái hiện từ gốc repo là `py -3 -X utf8 -B results/T-072/v2/thu_ca_gia_v2c.py`.