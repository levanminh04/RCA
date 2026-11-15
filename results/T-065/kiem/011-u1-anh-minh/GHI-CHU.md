# Ảnh bằng chứng U1 (T-065 REVIEW-5) — Minh chụp, chỉ mục bản 3

- **Nguồn:** Minh tự chụp trên Chrome đã đăng nhập Grafana, qua tunnel `127.0.0.1:13000` tới `exp-obs`; gửi trong chat phiên điều phối `local_feddcc0c` ngày 15/11/2026, file tới máy lúc khoảng 13:09 giờ máy (06:09Z). Giờ chụp chưa kiểm.
- **Người lưu:** Claude, phiên điều phối `local_feddcc0c`, 06:11Z 15/11/2026, theo lời Minh: "T-065 nghiệm thu sau khi lưu ảnh S1 và bổ sung ảnh U1".
- **Cách lưu:** chép nguyên byte (so `cmp` với file nhận), không chỉnh ảnh. Hash ở `SHA256SUMS`.
- **Không phải đầu ra của người làm (Codex).** Bổ sung phần ảnh còn thiếu của L11b (`kiem/010-chi-muc-3/l11b/ANH-CAN-CHUP.md`). Không có thao tác nào trên máy hay dashboard.

| Ảnh | URL (theo thanh địa chỉ) | Quan sát trên ảnh |
|---|---|---|
| `anh/01-l8b-rca-v082-ebd5ef38.png` | `/d/t065-l8b-phat-lai?var-ban=V082-V066%2BH8a&var-ca=ebd5ef38&…from=2026-11-14T10:06:40.000Z…` | Breadcrumb: 1 · Kết quả hiện hành › "T-065 L8b — M1-FT đề xuất cuối V082"; có liên kết "Mở trang phát lại (sau khi chấm xong)" — tức trang chính, dù chuỗi URL đầu hiển thị `t065-l8b-phat-lai` (chưa phân xử; có thể Grafana đã điều hướng). Mô tả: "Bản V082-V066+H8a, ca ebd5ef38 … Trang này dùng chỉ mục bản 3". Bảng: bản V082-V066+H8a, trạng thái chạy OK, nguồn đầu ra `results/T-064/kiem/nhan-r9/r9/dev3/d0/V082-V066+H8a/ebd5ef38/method-output-1.json`, trạng thái bản de_xuat, kết luận CAUSE_FOUND, hash mã nguồn `b0f79a4d…`. |
| `anh/02-l8b-phat-lai-v082-ebd5ef38.png` | `/d/t065-l8b-phat-lai/t-065-l8b-e28094-phat-lai-co-dap-an?var-ban=V082…&var-ca=ebd5ef38…` | "T-065 L8b — phát lại CÓ ĐÁP ÁN"; "chỉ mục bản 3"; hash cấu hình (JSON chuẩn hóa) `451a8437…`, hash byte file `01a64b60…`, hash đầu ra `563f449d…` (trùng sha256 của file nhan-r9 V082 ebd5ef38), cửa sổ 2026-11-14T10:06:40.000Z – 10:16:40.000Z. |
| `anh/03-muc-luc-ban-3.png` | `/d/t065-l5-muc-luc/muc-luc-rca?…` | Mục lục: bộ bản hiện hành p7, V082 (de_xuat), V071 (thay_the); 28 ca × 3 bản; "Nguồn giao diện: T-065 / L11, chỉ mục bản 3; cập nhật 15/11/2026. Ảnh Chrome L8c thuộc bản 2"; câu nguồn cuối "results/T-064/ban-xuat/chi-muc-ban.json (chỉ mục bản 3)". Hai dòng L4 ghi Lưu trữ. |
| `anh/04-l8b-rca-v071-ebd5ef38.png` | `/d/t065-l8b-rca/t-065-l8b-e28094-m1-ft-de-xuat-cuoi-v082?var-ban=V071-V041%2BH8a&var-ca=ebd5ef38…` | Bản V071-V041+H8a (thay_the), ca ebd5ef38, "chỉ mục bản 3"; hash cấu hình `a8b262fb…`, byte `87e882c5…`, hash đầu ra `5b329045…` (trùng file nhan-r9 V071), nguồn đầu ra nhan-r9; cửa sổ như trên. |
| `anh/05-l8b-phat-lai-v071-ebd5ef38.png` | `/d/t065-l8b-phat-lai/…?var-ban=V071-V041%2BH8a&var-ca=ebd5ef38…` | Trang phát lại, cùng bản/ca/hash như ảnh 04; "chỉ mục bản 3"; liên kết "Về trang chính". |

**Chưa thấy trên ảnh (giới hạn):** bảng toàn bộ cờ 64 dòng của hai slot (ảnh chỉ tới phần bảng bản/hash); bấm liên kết từ Mục lục tới hai trang hiện hành (ảnh mở URL trực tiếp; API đã xác nhận đích ở L11b — REVIEW-4 T3 chấp nhận giới hạn). Số cờ 64 đã kiểm bằng dữ liệu/API ở L11b và REVIEW-5.
