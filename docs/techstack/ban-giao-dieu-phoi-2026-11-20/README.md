# Bàn giao điều phối giai đoạn 2 — 20/11/2026

Gói này giúp một phiên Claude mới, kể cả ở account hoặc máy khác, có **đủ ngữ cảnh mà không cần lịch sử chat**. Minh duyệt tạo gói trong chat 20/11/2026 10:06Z: "tạo file luôn cho tôi, ghi đầy đủ toàn bộ những gì claude và codex đã thống nhất trong phiên này và toàn bộ những mong muốn của Minh". Sửa lần 1 theo lượt Codex soát gói (`lich-su/12`), Minh duyệt: "duyệt sửa, sau đó soạn prompt chi tiết cho phiên claude mới yêu cầu triển khai task …" (nguyên văn cuối `lich-su/01`).

Người soạn: phiên Claude điều phối cũ (đã làm T-069 phiên 1–2 và kế hoạch bản 1–4). Gói **không thay** `AGENTS.md`, `docs/STATE.md`, LOG các task hay `docs/DECISIONS.md`. Khi lệch nhau, các file đó thắng; báo Minh.

## 1. Thứ tự đọc cho phiên mới

Phiên mới làm theo `prompt-phien-moi.md` (thứ tự đọc ở đó là chuẩn; phần dưới chỉ tóm tắt).

**Bước 1, tự soát trước khi đọc phản biện:**
1. `AGENTS.md`, `docs/STATE.md`.
2. File này.
3. `mong-muon-minh.md`.
4. `tasks/T-069-v082-ban-ghim/SPEC.md`, mục cuối `LOG.md` (phiên 3), `results/T-069/dinh-chinh-1.md`.
5. `docs/techstack/KE-HOACH-GIAI-DOAN-2.md` §8.
6. `lich-su/08-claude-ke-hoach-ban-4.md`, **chỉ mục "## 2. Kế hoạch điều phối bản 4"**.

Rồi trình phần tự soát cho Minh.

**Bước 2, sau khi trình tự soát:**
1. `thong-nhat.md` (những gì đã thống nhất và ba điểm còn chặn).
2. Phản biện của Codex: `lich-su/05-…` (bản 2), `07-…` (bản 3), `09-…` (bản 4), `12-…` (soát gói bàn giao).
3. Các lượt khác của Claude: `02`, `03`, `04`, `06`, `10`, `11`, `13`.

## 2. Trạng thái lúc bàn giao (bằng chứng ghi trong ngày 20/11/2026; mỗi mục ghi giờ của bằng chứng khi có)

**Máy:**
- exp-app, exp-obs, máy tải AWS: không có runner, k6 hay lệnh nền nào của các phiên này đang chạy. Lượt cuối là `t069-lap`, xong 19/11 20:45:36Z.
- `/opt/rca-lab` trên exp-app và exp-obs ở commit `407b4f5` (repo lab, đã push), cây sạch.
- Bản ghim FlashTicket `36a3725` đang chạy. Payment đã được tạo lại hai lần bởi ô RECREATE-PAY, cùng image và cấu hình `t067-compose/hieu-luc`.
- Dữ liệu sự kiện tải `3e7c1df9`: Event và Booking đã dời mốc +14 ngày (bán tới 02/12 22:16:31Z) theo quyết định B (`results/T-069/sua-su-kien/`). Bản sao ở Ticket/Payment **chưa** đồng bộ (vẫn 19–20/11). DB lúc 02:31Z 20/11: `tbl_orders` 40.069 dòng.
- File trạng thái của `inj3`: `/home/ubuntu/t063/inj/compose-dir` trỏ tới cấu hình hiệu lực (T-069).

**Lịch:** ứng dụng Claude không còn lịch nào (`list_scheduled_tasks` rỗng; kết quả công cụ lúc **03:58:49Z** 20/11, dòng 1292 của file chat `debcb98c…jsonl`; chưa xác minh lại sau giờ đó). Lịch M1 cũ `m1ft-tiep-nhan` không còn hoạt động.

**Repo RCA (chưa commit):**
- T-069: `tasks/T-069-v082-ban-ghim/`, `results/T-069/` (manifest `SHA256SUMS` 318 file, `SHA256SUMS-2` 348 file).
- `docs/DECISIONS.md` và `docs/WHY.md` (mục T-069, WHY-102, do phiên fork ghi theo duyệt).
- `docs/STATE.md`: lẫn thay đổi của T-066/T-067/T-068/T-069 và dòng trỏ tới gói này.
- `docs/techstack/KE-HOACH-GIAI-DOAN-2.md`, LOG T-067/T-068: thay đổi của phiên khác, chưa commit.
- Gói này.

**Việc đang chờ:**
- T-069: Codex kiểm lại kết quả, bằng prompt ở mục cuối `tasks/T-069-v082-ban-ghim/LOG.md` ("Prompt cho Codex — kiểm lại phản hồi và sửa T-069"); sau đó Minh nghiệm thu và quyết commit.
- Đã đề xuất nhưng chưa làm: nối dòng đính chính hash vào LOG T-069 (`thong-nhat.md` §1.1).
- Kế hoạch điều phối: Q1–Q8 và ba điểm chặn (`thong-nhat.md` §2) chờ phiên mới đáp và Minh quyết.
- T-066, T-068: chờ Codex kiểm lại (xem STATE).

**Phiên Claude cũ:** không phiên nào còn giữ quyền ghi. Phiên fork T-069 (`local_40716c6f…`) đã xong phiên 3, đang rảnh; phiên fork `local_45149465…` không rõ trạng thái. Phiên mới **không** được coi các phiên này là chủ việc nào.

## 3. Chỉ mục file

| File | Nội dung |
|---|---|
| `mong-muon-minh.md` | Mong muốn và quyết định của Minh, tách ba mức chắc chắn; đề xuất dòng ghi DECISIONS (**chưa ghi, chờ Minh duyệt**) |
| `thong-nhat.md` | Những gì Claude và Codex đã thống nhất; kế hoạch hiệu lực = bản 4 + sửa; ba điểm còn chặn và số liệu đã kiểm; mã task dự kiến |
| `prompt-phien-moi.md` | Prompt mở phiên Claude điều phối mới: kiểm trạng thái, tự rà soát toàn bộ plan (1A độc lập rồi 1B đọc phản biện), sửa lỗi nhỏ, triển khai; lỗi chặn thì dừng trình (theo duyệt của Minh) |
| `prompt-codex-soat-ban-giao.md` | Prompt cho Codex soát gói này có lệch với lịch sử thật không |
| `lich-su/01-minh-tin-nhan.md` | Nguyên văn 17 tin nhắn của Minh (19–20/11) |
| `lich-su/02`, `03`, `04` | Claude: kế hoạch bản 1, bản 2, trả lời về DB/reset |
| `lich-su/05` | Minh chuyển: báo cáo phiên fork T-069 và phản biện Codex cho bản 2 |
| `lich-su/06`, `07` | Claude kế hoạch bản 3; Codex phản biện bản 3 |
| `lich-su/08`, `09` | Claude kế hoạch bản 4; Codex phản biện bản 4 |
| `lich-su/10`, `11` | Claude: trả lời sau bản 4; đề xuất bàn giao |
| `lich-su/12`, `13` | Codex soát gói bàn giao (Minh chuyển); Claude đáp và đề xuất sửa hẹp (Minh duyệt) |
| `prompt-codex-kiem-lai-sua-ban-giao.md` | Prompt cho Codex kiểm lại các sửa của gói (sửa lần 1) |
| `SHA256SUMS` | Hash mọi file trong gói |

`lich-su/*` được trích bằng script từ lịch sử chat Claude (và phiên Codex cho tin Minh gửi Codex). Script nằm trong scratchpad của phiên cũ, không vào repo. Quy ước:
- Các file `02`–`13`: nguyên văn, chỉ bỏ thẻ bọc `<pasted_content>`.
- `01-minh-tin-nhan.md`: 14/17 tin trong chat Claude là nguyên văn; 3 tin có khối dán được thay bằng dẫn chiếu sang file chứa khối dán (`05`, `07`, `09`). Phần cuối có tin Minh gửi Codex (03:33:57Z, nguyên văn) và tin duyệt mới nhất.
- Số "dòng" trong các file là chỉ số **đếm từ 0** của dòng trong file jsonl; mở bằng trình soạn thảo thì cộng 1.

## 4. Nguồn thô ngoài repo (chỉ dự phòng, có trên máy laptop của Minh)

- Lịch sử chat Claude: `C:/Users/84583/.claude/projects/D--RCA-flashticket/debcb98c-9a36-447f-b07c-8820bd290ab4.jsonl` (đầy đủ nhất). Thêm `72bf1f3f-…jsonl` (phần trước khi nén) và `40716c6f-…jsonl` (phiên fork T-069).
- Phiên Codex phản biện kế hoạch: `C:/Users/84583/.codex/sessions/2026/11/20/rollout-2026-11-20T09-25-06-01a1f6c5-96df-70f0-bba2-930bc5c27cd9.jsonl`.
- Bản chép các trả lời của Claude mà Minh đưa sang Codex: `C:/Users/84583/.codex/attachments/12aba7a5-…/Pasted text.txt` (bản 3), `0c2d893d-…/Pasted text.txt` (bản 4).
