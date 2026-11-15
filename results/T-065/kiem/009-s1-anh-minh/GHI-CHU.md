# Ảnh bằng chứng S1 (T-065 REVIEW-3) — Minh chụp

- **Nguồn:** Minh tự chụp trên Chrome đã đăng nhập Grafana, qua tunnel `127.0.0.1:13000` tới `exp-obs`.
  - Ảnh 01–03 gửi trong chat phiên Claude `ed8b9c01` lúc 15/11/2026 khoảng 04:12Z.
  - Ảnh 04 gửi lúc khoảng 04:53Z.
  - Giờ lấy theo thời điểm file tới máy, chưa kiểm với giờ chụp.
- **Người lưu:** Claude, phiên `ed8b9c01`. Minh yêu cầu "triển khai phần còn lại giúp tôi".
- **Cách lưu:** chép nguyên byte, không chỉnh ảnh. Hash ở `SHA256SUMS`.
- **Không phải đầu ra của người làm (Codex).** Đây là bằng chứng bổ sung cho phần L10 (`kiem/008-s1/`) còn thiếu ảnh. Không có thao tác nào trên máy hay dashboard.

| Ảnh | URL (theo thanh địa chỉ) | Quan sát trên ảnh |
|---|---|---|
| `anh/01-muc-luc.png` | `/d/t065-l5-muc-luc/muc-luc-rca?from=now-1h&to=now&timezone=utc` | Breadcrumb: RCA FlashTicket › 0 · Bắt đầu tại đây › Mục lục RCA. Bộ bản hiện hành: p7 (khoa_P7), V082-V066+H8a (de_xuat), V071-V041+H8a (thay_the); 28 ca × 3 bản; cập nhật 15/11/2026. "RCA — bản đề xuất cuối V082" và "Phát lại có đáp án — T-062" ghi Hiện hành. Hai dòng L4 ghi "Lưu trữ — bộ bản tạm L4, không là bản đề xuất cuối". Mục "Trạng thái và giới hạn": "V082 là đề xuất cuối Minh chọn; V071 là bản thay thế có đầu ra cạnh". |
| `anh/02-l8b-rca-v082.png` | `/d/t065-l8b-rca/…?from=2026-11-14T08:00:55.000Z&to=2026-11-14T08:10:54.999Z…` | Folder 1 · Kết quả hiện hành. Bản V082-V066+H8a, trạng thái `de_xuat`, ca 86dea661, trạng thái chạy OK. Có hash cấu hình, hash mã nguồn `b0f79a4d…`, hash đầu ra và cửa sổ. Dòng mô tả ghi "Trang này dùng chỉ mục bản 2". |
| `anh/03-l8b-phat-lai-v082.png` | `/d/t065-l8b-phat-lai/…` (cùng cửa sổ) | Folder 1 · Kết quả hiện hành. Cùng bản, cùng ca, có liên kết "Về trang chính". Dòng mô tả ghi "chỉ mục bản 2". |
| `anh/04-folder-luu-tru.png` | `/dashboards` | RCA FlashTicket gồm các folder 0 · Bắt đầu tại đây, 1 · Kết quả hiện hành, 9 · Lưu trữ. Trong 9 · Lưu trữ có G2 bản 6 · 12-11, L3 · P7 · 13-11, L4 · Bộ bản tạm · 14-11. Folder L4 chứa "T-065 L4 — chọn bản M1 cùng ca" và "T-065 L4 — phát lại CÓ ĐÁP ÁN". |

**Ghi chú cho người phản biện.** Ảnh 02–03 ghi "chỉ mục bản 2". Sau khi sửa R9, T-064 đã lập chỉ mục bản 3: hai ô ca ebd5ef38 đổi nội dung đầu ra, hạng và cờ không đổi. Việc T-065 xuất lại hai ô này theo bản 3 nằm trong danh sách còn lại của điều phối, không thuộc S1.
