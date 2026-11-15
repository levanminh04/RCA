# T-063 — Thiết kế bộ chạy bản 2 (nháp 1, 12/11/2026 22:14Z)

Nền: `results/T-062/chay/runner.py` (dùng lại cấu trúc: sổ tiêm hash nối dòng, mã ca mờ, M1 qua `stage-m1.py`/`run-m1.py` ghim, luồng M1 nền tuần tự, STOP). Thay đổi có lý do đo được:

| # | Thay đổi | Lý do (bằng chứng) |
|---|---|---|
| 1 | Đầu dò **không gọi HTTP của app** trong cửa sổ `[t−300, t+300)`; chỉ đọc cgroup/toxiproxy/TCP connect/Redis PING/PG SSLRequest | `inj.py probe` gọi `/actuator/health` Booking → con mồ côi chỉ ở A (`span-goc/PHAN-TICH.md`) |
| 2 | Đầu dò **đối xứng**: t−240 và t+60 (cùng độ lệch 60 s sau đầu mỗi nửa); đầu dò dài (gồm health, nếu cần) ở t+330 (sau A) | T-062: nền t−300 (biên), lỗi t+60/t+480 — lệch; H1 không được ủng hộ nhưng đối xứng loại hẳn yếu tố này (`ca-nen/PHAN-TICH.md`) |
| 3 | Sau mỗi chu kỳ: ngoài gói ghim (`safe-export.py`), chạy `dong-goi/xuat_bo_sung.py --t <t>` trên `exp-obs`, chép về `results/T-063/ca/<id>/prometheus-bo-sung.json` + sha256 | Gói ghim chỉ 7 kênh (`quan-sat/bang-huong-tin-hieu.md`) |
| 4 | Phục hồi: lỗi stage/M1 của một ca → giữ thư mục cũ (đổi tên `…-loi-<n>`), stage lại cùng `t` với mã mới; không ghi đè `outputs/<id>` đã có | luật 21 (b); `stage-m1.py`/`run-m1.py` dùng `mkdir(exist_ok=False)` |
| 5 | Lịch ô theo `o-dev-bo-sung.md` + ô dev T-059; ca bình thường xen giữa, ít nhất 3 ca; FLASH-HEALTHY ≥ 1; khai trước trong `lich-2.json` (băm) | tiêu chí chọn mục 1 (tập chọn khai trước) |
| 6 | Tải: lệnh mới của L1 (`k6/hanh-trinh.js`), cùng giao diện `Start/Get/Stop/Receive` | phụ lục 2 |
| 7 | Nhịp tim bộ chạy mỗi 60 s vào `trang-thai.json`; tiến độ từng bước kèm thời gian | AGENTS 5.4 "ghi tiến độ và thời gian từng bước" |

**Hồ sơ luật 21 (lỗi ở 10%, 50%, 99%)** — ghi đủ ở `HO-SO-LUOT.md` khi chốt lịch. Nguyên tắc: một ô lỗi (tiêm không lên, M1 lỗi) chỉ chặn ô đó, ghi `cycle-error`, chạy tiếp ô sau; lỗi tải hoặc hạ tầng (k6 không chạy sau 2 lần thử, `exp-obs` không nhận dữ liệu) dừng lượt, giữ mọi ca đã thu; thu bù chỉ ô bị ảnh hưởng (quyền ở `CHIEN-DICH-M1-FT.md` mục 6). Chi phí lỗi: 10% → mất ≤ 1 chu kỳ (30 phút), chạy lại ô đó; 50% → như trên, phần đã thu dùng được; 99% → chỉ ô cuối; M1 lỗi ở ca bất kỳ → stage lại cùng t (~2 phút/ca), không thu lại.
