# T-066 — Đính chính sau phản biện soát kết quả (Codex, 18/11/2026)

Minh duyệt 5 nhóm sửa ngày 18/11/2026 ("Duyệt 5 nhóm sửa"). File này ghi các câu cần sửa; các file gốc giữ nguyên để làm mốc (riêng `bao-ve.tsv` đang được T-067 dùng làm danh sách bảo vệ nên không sửa).

## 1. `bao-ve.tsv` dòng 171 — nguồn của `results/T-064/manifest-3.json` (R1)

- Bảng ghi nguồn đối chiếu là "git (repo RCA, đã commit)". **Sai.** File chưa từng được track: commit T-064 `25550d2a5` chỉ gồm kết quả nhẹ, và `git ls-files --error-unmatch` báo không có.
- Đúng ra: tại thời điểm T-066 file chỉ có trên laptop, 1.055.393 byte, sha256 `faa7d29285892f880ddc186cb248382af93f36b4e0f12a99559567578ca2bfea` (khớp cột `sha256_tinh_lai`).
- Đã sửa: file được commit nguyên byte vào repo RCA cùng commit chứa file đính chính này. Kiểm sha256 ngay trước khi add.
- Phép so hồi quy V082 của T-066 không đổi kết luận, vì file trên laptop khớp hash đã ghi.

## 2. `danh-sach-xoa.md` hàng 1.2 — `outputs/` của `/opt/flash-ticket-rca` (R3)

- Hàng 1.2 viết "33 ca có tgz trên laptop …; tgz chứa cả `cases/<id>` và `outputs/<id>`". **Nói quá.**
- Đếm lại ngày 18/11 trên laptop: hợp các mã `outputs/<id>` trong 35 tgz ở `results/T-058|T-062|T-063` với các thư mục `outputs/` đã giải nén. Kết quả là **32 mã khác nhau**, so với 38 thư mục đã xóa.
- 12 ca trong `D:/RCA-archive/exp-obs/cases/` (`659a9dfb`, `ebd5ef38`, `ebd5ef381d1a`, `gia*`, `kte*`, `thuong01`) chỉ có `cases/`, không có `outputs/`.
- **6 thư mục `outputs/` không xác định được tên**, vì không còn danh sách trước khi xóa. Khả năng là đầu ra của các ca thử trong archive (**chưa kiểm**). Đầu ra dùng cho đánh giá (T-064) có bản riêng ở `results/T-064/`.
- Phạm vi chứng minh được:
  - `cases/`: hợp tgz, thư mục đã giải nén và archive cho **45 mã khác nhau**, bằng số 45 đã xóa. Không còn danh sách tên trước khi xóa nên không so được từng mã.
  - `outputs/`: **32/38** có bản.

## 3. Thứ tự "kiểm phát lại trước khi trình danh sách xóa" (R4)

- W1 (kế hoạch §8.2) và SPEC bước 7 yêu cầu mở được ca cũ trên trang phát lại trước khi trình danh sách xóa. Thứ tự đã xảy ra:
  - 12:52Z 17/11: trình danh sách xóa.
  - 12:53Z: Minh duyệt nhóm 1 và xóa ngay.
  - 15:30Z: xem Grafana, nhưng là ca **mới** 7ffb2305 trên trang **sự cố**, không phải ca cũ trên trang phát lại.
- Kết luận: tiêu chí W1 chưa đạt đúng thời điểm. Minh chấp nhận giới hạn lịch sử này (18/11).
- Xác nhận hành vi hiện tại: xem LOG T-066 phiên 3 (mở ca cũ trên trang phát lại).

## 4. `cach-ly-nhan.md` — câu "không bước nào đọc sổ"

- Thu hẹp lại như sau. Helper `campaigns/runner/ledger_append.py` chạy bằng user `ledger`, đọc dòng cuối của sổ để nối hash. User `rca` (chạy P7/V082) bị từ chối khi đọc sổ thật. Không có đường đưa nội dung sổ hay tên ô vào P7/V082 của ca 7ffb2305.

## 5. Ghi chú nhỏ

- Hai địa chỉ IP còn xuất hiện trong docstring ví dụ của `campaigns/lib/inventory.py`. Chúng không cấp địa chỉ cho tiến trình nào. Câu "IP ngoài `inventory/` chỉ còn trong tài liệu lịch sử" vì vậy đúng một phần.
