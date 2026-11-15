# CHECKPOINT T-062

Mọi agent cập nhật file này sau mỗi bước và ít nhất 30 phút một lần. Dòng đầu là nhịp tim.

NHIP_TIM_UTC: 2026-11-12T01:51:47Z
DIEU_PHOI: XONG — phiên claude-tiep-quan-20261112 kết thúc 2026-11-12T01:23:01Z; mọi việc còn lại chờ Minh (results/T-062/bao-cao-sang.md §8)

## Trạng thái bước (SPEC §runbook)

| Bước | Trạng thái | Ghi chú |
|---|---|---|
| A1 FlashTicket review, nhánh, PR, CI | XONG (CI xanh) | PR nháp levanminh04/flash-ticket-platform#17 đầu `6b21ed55`: 14 check đạt, 1 bỏ qua (Frontend), MERGEABLE; KHÔNG merge (chờ Minh) |
| A2 Triển khai exp-app | XONG lượt 2 19:21Z | commit `6b21ed55`; `results/T-062/ha-tang/A2-kiem.md`; hoàn tác `~/rollback-t062.sh` |
| B1 Kiểm chất lượng dữ liệu | XONG lượt đầu | `results/T-062/kiem-du-lieu/bao-cao-B1.md` (R-06, R-08, R-10 đạt; R-04, R-09 chưa kiểm được với tải đọc) |
| C1 Máy tải | XONG (Codex) | `results/T-062/tai/bao-cao-C1.md`; thử 5 phút 1501 req, 0×401; tickets 500 (lỗi nền có sẵn, xem `tiem-loi/o-loi.md`) |
| D1 Bộ tiêm | XONG (chờ D2) | `results/T-062/tiem-loi/o-loi.md`, `scripts/inj.py` (exp-app `~/inj.py`), Toxiproxy `rca-toxiproxy` |
| D2 Xác nhận B4 | XONG 20:25Z | `results/T-062/tiem-loi/d2-tong-hop.md`: 5 ô đạt (EVENT-DB-LAT ở 30 ms), REDIS-BOOK không đạt → bỏ |
| E1 Chu kỳ | XONG 01:20Z | 9/9 chu kỳ, M1 9/9 OK |
| E2 Chuyển định dạng, đẩy giao diện | XONG | 9 ca + phát lại trên exp-obs |
| G1 Giao diện G2 | XONG MỘT PHẦN | chưa xem trên chính exp-obs (cần đăng nhập); kiểm trên bản thử với ca thật |
| H1 Bàn giao sáng | XONG | `results/T-062/bao-cao-sang.md`, `spec-chang-4-de-xuat.md`, `manifest.json` |

## Việc tay của Minh (trước khi ngủ)

- [x] `gh auth login` — xong, tài khoản levanminh04 (Claude đã kiểm `gh auth status`)
- [x] Oracle Security List: TCP 8081, 8080 từ `3.24.8.49/32` — xong, đã kiểm từ máy tải 12/11
- [ ] (khuyến nghị) Boot volume backup `exp-app`, `exp-obs`; chặn bypass nhánh `main` trên GitHub
- [ ] Windows Power: không bao giờ ngủ khi cắm sạc; để ứng dụng Claude mở

## Sao lưu

- FlashTicket trước khi sửa: `D:/RCA-ext/backup-flashticket-20261112/`
- RCA repo trước lượt: `D:/RCA-ext/backup-rca-20261112/` (HEAD `c3d27f8a…`, diff, file mới)

## Việc tiếp theo

Sau D2: `py -3 -B results/T-062/tiem-loi/phan-tich-d2.py <tag d2>` → sửa lịch nếu ô không đạt → `runner.py e1` (nền) → mỗi ca xong chạy `e2.py --day`; hết đợt `e2.py --phat-lai --day`; B1 trên gói ca bình thường.

(cũ)

Phiên điều phối: đọc `SPEC.md`, chạy A1 ∥ giao C1 cho Codex ∥ mở phiên giao diện G1.

- ~18:37Z 11/11: Minh bật chế độ bỏ qua quyền; trước đó bộ phân loại chặn iptables, Codex bypass và start_session.

- 12/11 ~02:00Z: Codex kiểm Grafana thật (đạt một phần) + phản biện REVIEW.md; người làm đã điền bảng phản hồi; chưa sửa gì, chờ Minh.

- 12/11 ~02:45Z: Codex hết lượt (tới 06:05Z) khi kiểm Grafana thật bản dashboard 6; lệnh nền `results/T-062/codex/cho-codex-G1-that-2.sh` tự phát lại lúc 06:10Z, kết quả `results/T-062/codex/G1-that-2-ketqua.md`.
