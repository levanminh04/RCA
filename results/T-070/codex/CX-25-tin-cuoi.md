Đã tạo đúng hai file mới. SHA-256 sau khi ghi khớp với SHA-256 đã báo trước khi ghi.

| File | SHA-256 sau khi ghi |
|---|---|
| [results/T-072/dinh-chinh-cx19-co-hoc.md](D:/RCA-flashticket/results/T-072/dinh-chinh-cx19-co-hoc.md) | `b8438ddc8a6a4bd73f2ab804405e2ea43bc491632a569d556e0ae30fb35229d3` |
| [results/T-071/dinh-chinh-cx19-co-hoc.md](D:/RCA-flashticket/results/T-071/dinh-chinh-cx19-co-hoc.md) | `564250a6a1a0fcd80306664783f8ac8c32b4d8ac8de02c16efa7bb5d5b946ea2` |

**T-072.** `06:06:10Z` là nhịp truy vấn tổng hợp đầu tiên sau khi Grafana báo khỏe. Cửa sổ E4 bắt đầu lúc `10:13Z`, nên R5 vẫn là **0 sự cố trên 383 phút khỏe ×1**.

**T-071.** Đã đối chiếu E2 và E4. Cả hai có cùng **12 container có chuỗi restart**. Container vắng suốt khoảng không thể nhận cờ thiếu theo tên. Trường `OOMKilled` được đọc từ trạng thái của container tải k6.