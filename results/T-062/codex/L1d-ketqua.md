L1 XONG

Đã triển khai [tai_linux.py](D:/RCA-flashticket/results/T-062/tai-2/tai_linux.py) trên exp-obs. 17 nguồn PowerShell cũ nguyên hash.

- Linux: 180 và 433 hành trình; PowerShell tương ứng: 181 và 434. Chênh lệch đã ghi rõ.
- Cả bốn lượt: 0 lỗi hành trình/401/dropped; 48 hash khớp; 11 kiểm hợp đồng đạt.
- Đã sửa lỗi SSH con lấy stdin của caller và kiểm hồi quy.
- `EXP-APP-XONG` cũ giữ nguyên. Bốn lượt L1 đã xong; máy hiện có tải khác, không bị L1 can thiệp.

[Bàn giao, bằng chứng và cách chạy](D:/RCA-flashticket/results/T-062/tai-2/BAN-GIAO-4-linux.md).

```sh
python3 ~/rca-dieu-phoi/tai_linux.py start --tag ma-moi --seconds 1800 --buoc-tai 600 --multiplier 3
```