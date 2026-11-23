# Claude: đề xuất gói bàn giao

> Nguyên văn, trích bằng script từ `debcb98c-9a36-447f-b07c-8820bd290ab4.jsonl` (dòng 1351). Không biên tập.

Câu trả lời ngắn: **chưa có bàn giao đủ trong repo.** Hiện ngữ cảnh nằm rải rác ở ba nơi, đều ngoài repo:

| Nội dung | Đang nằm ở đâu | Rủi ro khi đổi account/máy |
|---|---|---|
| Kế hoạch điều phối bản 2–4, các câu trả lời của tôi | Lịch sử chat Claude (`C:/Users/84583/.claude/projects/D--RCA-flashticket/*.jsonl`); bản chép Minh dán sang Codex (`C:/Users/84583/.codex/attachments/12aba7a5…`, `0c2d893d…/Pasted text.txt`) | File còn trên máy này, nhưng là file thô, khó đọc, máy khác không có. Prompt mở phiên mới của Codex lại đọc đúng file đính kèm này |
| Ba lượt phản biện kế hoạch của Codex | Chỉ có trong chat (Minh dán vào đây) và phiên Codex | Mất nếu không chép ra |
| Các quyết định Minh nói trong chat 19–20/11 (chạy ban ngày không đợi đêm, dùng nhiều phiên với một phiên điều phối, Codex qua terminal `gpt-6.2-astra` high, ưu tiên tính đúng hơn tốc độ, chuyển sang phiên mới) | Chỉ có trong chat | Theo AGENTS §4 phải ghi DECISIONS; hiện chưa ghi |

Những gì **đã có trong repo** thì đủ cho T-069: SPEC, LOG phiên 1–3, `dinh-chinh-1.md`, hai manifest, mục T-069 trong DECISIONS, WHY-102, dòng STATE.

## Đề xuất: gói bàn giao trong repo (cần Minh duyệt, Luật 0)

**1. Tạo thư mục `docs/techstack/ban-giao-dieu-phoi-2026-11-20/`** với các file sau:

| File | Nội dung | Cách ghi |
|---|---|---|
| `README.md` | Trạng thái lúc bàn giao. Máy: exp-app, exp-obs, máy tải rảnh, không job hay lịch nào chạy. Repo: các file chưa commit (T-069, `docs/DECISIONS.md`, `docs/WHY.md`, các thay đổi còn treo của T-066/67/68). T-069 đang chờ Codex kiểm lại (prompt ở LOG:396), chưa commit. Các phiên Claude cũ không còn giữ việc gì. Thứ tự đọc cho phiên mới. Đường dẫn tới lịch sử thô (jsonl, file đính kèm Codex), chỉ làm nguồn dự phòng | Tôi soạn |
| `ke-hoach-ban-4.md` | Nguyên văn mục "2. Kế hoạch điều phối bản 4", **kèm các sửa Codex đã đồng tình**: lượt ×1 dài 60 phút xen lượt flash 30 phút (tăng tải ở phút 10), đồng bộ ngày sự kiện theo giá trị đích, mục "mất tối đa một lượt" chỉ đúng với lỗi cục bộ | Chép nguyên văn từ chat |
| `diem-chan-mo.md` | Ba điểm còn chặn ở lượt 4 của Codex (lịch tự tiếp nhận; tiến trình server chạy cả danh sách lượt; dữ liệu và mẫu số của W4), cùng các số đã kiểm: histogram gateway theo mã route (`booking`, `event`, `payment`, `ticket`, `user`); `runner4.py` với `RCA_PHASE=600` chạy cả danh sách chu kỳ trên server, đã đo 31,3 phút/chu kỳ; phép tính 380 phút ×1 và 40 phút ×3 | Tôi soạn, có đường dẫn bằng chứng |
| `codex-phan-bien-ban-2.md`, `-ban-3.md`, `-ban-4.md` | Nguyên văn ba lượt phản biện kế hoạch của Codex mà Minh đã dán | Chép nguyên văn; **tách file riêng** để phiên mới tự soát trước rồi mới đọc |
| `prompt-phien-moi.md` | Prompt mở phiên mới hai bước, chỉ trỏ vào file trong repo, không còn đọc `.codex/attachments`. Bước 1: đọc AGENTS, STATE, README, `ke-hoach-ban-4.md`, `diem-chan-mo.md`, tự soát. Bước 2: đọc ba file `codex-phan-bien-*`, đáp từng điểm. Giữ đúng yêu cầu điều phối trong khối A của Codex | Tôi soạn |

**2. Thêm vào `docs/DECISIONS.md` một mục "Điều phối giai đoạn 2, 19–20/11/2026"**, ghi nguyên văn các câu Minh đã nói trong chat. Lượt ghi đầu tiên tôi trình nguyên văn từng dòng để Minh duyệt.

**3. Thêm một dòng vào `docs/STATE.md`:** "Điều phối giai đoạn 2: chưa mở task; bàn giao ở `docs/techstack/ban-giao-dieu-phoi-2026-11-20/README.md`". Chỉ thêm dòng này, không sửa dòng của task khác.

**Không làm trong lượt bàn giao:** commit, mở task T-070, sửa T-069, chạy máy. Commit gói bàn giao để máy khác cũng đọc được thì xin Minh riêng.

Thời gian: khoảng 15–20 phút ghi file, sau đó tôi kiểm lại bằng cách đọc gói như một phiên chưa có lịch sử, xem có thiếu gì không. Sau khi đổi account, Minh chỉ cần dán `prompt-phiên-moi.md` vào phiên mới.
