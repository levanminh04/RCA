# W4 v2 — phần cơ học của bộ chấm

Với luật `<`, bộ chấm và script giải thích dùng giá trị lớn nhất trong mỗi cửa sổ đủ mẫu. Script giải thích lấy giá trị nhỏ nhất giữa các cửa sổ đó. Với luật `>`, thứ tự là min trong cửa sổ rồi max giữa các cửa sổ.

Sau khi gom sự cố và quy về phút, bộ chấm gắn cờ `chong-quan-sat` lên sự cố hệ thống nếu hai khoảng nửa mở giao nhau. Hai khoảng chỉ chạm đầu mút có thời gian giao bằng 0. Khoảng chưa hết kéo dài tới cuối phần quan sát.

Lệnh `chon-nguong` trả mã 1 khi thiếu ngưỡng. Thông báo lỗi ghi route, loại ngưỡng và số bước đủ mẫu. Lệnh dừng trước khi ghi JSON.

**Phần Claude T-072 phụ trách.** Hàm `quy_ve()`, logic Pending (trạng thái chờ) và kỳ vọng của ca `t0+60` giữ nguyên, có chú thích tại cả ba vị trí. Việc phân loại sự cố đã cháy trước đầu khoảng còn mở. Phiên Codex khác kiểm kỹ thuật; Claude T-072 kiểm trước khi tích hợp.

## Chạy từ gốc repo

```powershell
py -3 -X utf8 -B results/T-072/v2/thu_ca_gia.py
```

Thêm `--ghi` để lưu kết quả vào `v2/ra/thu-ca-gia.txt`. Biên bản gồm hai ca cửa sổ, sáu ca giao khoảng và một ca thiếu riêng p95 Ticket. Ca Ticket chạy lệnh chọn ngưỡng trong một tiến trình Python riêng với chuỗi và lớp phút giả trong bộ nhớ. Kiểm tra mã thoát và thông báo lỗi của tiến trình.

Các lệnh của bộ chấm nhận chuỗi và lớp phút ở định dạng v1. Ví dụ dưới đây dùng `$xuat` và `$phut` là đường dẫn tới hai file đầu vào tương ứng.

```powershell
py -3 -B results/T-072/v2/cham_offline_v2.py tu-kiem
py -3 -B results/T-072/v2/cham_offline_v2.py cham --xuat $xuat --phut $phut --ra cham.json
py -3 -B results/T-072/v2/cham_offline_v2.py chon-nguong --xuat $xuat --phut $phut --ra nguong.json
```

Cấu hình ghim nằm ở `results/T-072/*.json`. Lệnh `cham` mặc định dùng `nguong.json` tại đó. Bộ chấm ghi `v2/ra/<tên lệnh>.json` hoặc tên JSON truyền qua `--ra`. Trường `dau_vao_sha256` chứa hash của file Python thực chạy.

Điểm vào của script giải thích là `py -3 -B results/T-072/v2/e4_giai_thich_khac_v2.py`. Script nạp bộ chấm v2 theo đường dẫn và xuất `v2/ra/giai-thich-khac.json` kèm hash của cả hai script. Phiên này chỉ chạy hàm giải thích trên chuỗi giả. E4 chưa được chấm lại.

## SHA-256

```text
39f56bde8247ce8640a8b28a023caea5a7eaf7ec8ec3d71772bf0b0c0e6dac44  cham_offline_v2.py
cfae7a8af7be93bd31f14f3f7d5a44d04306c10db8069f5e6d4417025f212b8f  e4_giai_thich_khac_v2.py
0e2da83deb2135bb73cc6409eb966ae79774a56e0e3759eb2742f1377dc247bb  thu_ca_gia.py
89ceebf4989caeca886f7ae323e9055e642fca8a8a306b6bc5e58362bdc2cb1b  ra/thu-ca-gia.txt
```
