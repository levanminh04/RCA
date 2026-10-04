# Nhật ký T-000

Chỉ ghi thêm vào cuối, không sửa mục cũ.

---

## Phiên 1 — 02/10/2026 — Claude — laptop của Minh — vai trò: người làm

Phiên này diễn ra trước khi có cấu trúc task. Mục này được ghi lại vào cuối phiên từ diễn biến thực tế.

**Diễn biến:**

- **Đọc nguồn:** đọc nguồn của repo cũ: DT18, hướng dẫn của cô, LESSONS-v1, Task A, Task B, ghi chú dataset. Kiểm máy: i5-1240P, RAM 16 GB, không có GPU NVIDIA, ổ D còn khoảng 65 GB. Kiểm được hai điều về FlashTicket: chạy trên EC2, và đã chọn Gemini cho lớp giải thích.
- **Hỏi Minh hai lượt.** Các câu trả lời được ghi ở `docs/DECISIONS.md`, từ Q-01 đến Q-12.
- **Dựng repo mới:** `git init`; soạn MRP v3, AGENTS, STATE, DECISIONS, WHY, LESSONS, review-prompt; chép tài liệu tham khảo vào `docs/reference/`.
- **Vi phạm.** Minh chỉ hỏi Task A, B được chắt lọc hay copy nguyên văn, nhưng Claude đã tự lược Task A, xóa một file và sửa AGENTS. Minh yêu cầu hoàn tác toàn bộ và đặt Luật 0. Đã hoàn tác; Luật 0 thêm vào AGENTS theo nguyên văn Minh duyệt.
- **K1, K2.** Minh duyệt Đề xuất 1. Đã tạo `docs/knowledge/K1-phuong-phap-rca.md` (từ Task A, bỏ phần gap, novelty, REVIEWER ANALYSIS, §M, §N, §P, §Q) và `docs/knowledge/K2-du-lieu.md` (từ Task B, ST1–ST3, Task A §O). Đã xóa các bản chép Task A, Task B, `when_graph_helps.md`. Đã gỡ đường dẫn về repo cũ trong MRP, AGENTS và bộ nhớ.
- **Đề xuất khung làm việc.** Tìm bài chia sẻ thực tế (HN, dev.to, arXiv, ARIS), soạn `docs/DE-XUAT-KHUNG-LAM-VIEC.md`. Minh không duyệt nhóm cưỡng chế bằng settings/hooks; quyết dùng file luật là đủ.
- **Nhóm A — sửa định tuyến** (Minh duyệt):
  - global Codex `~/.codex/AGENTS.md`: thêm ngoại lệ cho RCA → `D:/RCA-flashticket`;
  - platform: `AGENTS.md` dòng 33, cùng dòng 1 của bốn file trong `docs/research-rca/` (README, CURRENT-STATE, MASTER-RESEARCH-PROGRAM, SESSION-BOOTSTRAP);
  - repo cũ: thêm dòng "LƯU TRỮ" ở đầu `AGENTS.md`, `README.md`, `docs/STATE.md`.
  - Audit quản trị của platform: PASS, 1 cảnh báo về số file trong diff (7 file, gồm cả các thay đổi chưa commit có sẵn từ đợt G0).
- **Nhóm B — tổ chức theo task, hai agent ngang hàng** (Minh duyệt):
  - viết lại AGENTS;
  - tạo `tasks/_MAU/` và task T-000 này;
  - STATE thành mục lục task;
  - review-prompt trung lập giữa hai agent;
  - `data/README.md`;
  - bộ nhớ Claude chỉ còn một con trỏ;
  - ghi quyết định Q-13 đến Q-16.

**Quyết định của Minh trong phiên:** đều đã ghi vào `docs/DECISIONS.md`.

**Kết thúc phiên:**
1. Đã làm gì: như trên.
2. File đã thay đổi: toàn bộ repo mới (chưa commit); các file ở platform, repo cũ và global Codex như mục "Nhóm A".
3. Kiểm tra đã chạy: audit quản trị của platform PASS (1 cảnh báo). So byte khi hoàn tác Task A: khớp bản gốc. Quét K1: không còn từ khóa gap hay novelty, không còn link về repo cũ.
4. Điều chưa chắc hoặc cần Minh quyết:
   - Duyệt G0 (MRP).
   - Ba câu ở MRP §10.
   - Các quyết định cũ "chờ xác nhận lại" trong DECISIONS.
   - Số phận `docs/DE-XUAT-KHUNG-LAM-VIEC.md`: nhóm C đã bị bác, nên file này giờ lỗi thời một phần.
   - Các mục DX-06 đến DX-16 cũ chưa được quyết.
   - Tạo remote GitHub.
   - Commit đầu tiên.
5. Bước tiếp theo chính xác: Minh chạy phản biện G0 bằng Codex theo prompt ở cuối file này, rồi mở phiên Claude để trả lời phản biện.
6. Lệnh cuối cùng đã chạy: audit quản trị của platform (`.agents/skills/govern-capstone-work/scripts/audit-governance.ps1`).

---

## Prompt phản biện cho agent còn lại

Chạy: `codex exec -s read-only -C D:\RCA-flashticket -o tasks\T-000-nen-tang\REVIEW.md "<prompt dưới>"`

```text
Bạn là người phản biện độc lập cho task T-000 của repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Bạn chỉ được ghi đúng một file: tasks/T-000-nen-tang/REVIEW.md, theo mẫu tasks/_MAU/REVIEW.md.
Không sửa file nào khác, không commit.

Đọc: tasks/T-000-nen-tang/SPEC.md, tasks/T-000-nen-tang/LOG.md, docs/MRP.md, docs/WHY.md, docs/DECISIONS.md,
docs/LESSONS.md, docs/knowledge/K1-phuong-phap-rca.md, docs/knowledge/K2-du-lieu.md, AGENTS.md.
Nguồn đối chiếu đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Trả lời trọng tâm:
1. Chuỗi gói việc P1–P10 có đi đúng chuỗi cô yêu cầu không
   (hiểu sâu phương pháp → nhiều dataset → hạn chế → 5 bước đồ thị → tích hợp sản phẩm)?
2. Có bước nào cô yêu cầu mà MRP bỏ sót hoặc hiểu sai không?
3. Cách hiểu "graph-based anomaly detection" ở MRP §2.3 có hợp lý không? Có cách hiểu nào tốt hơn không?
4. Câu hỏi nghiên cứu nào không trả lời được bằng dữ liệu dự kiến?
5. Có lựa chọn nào lặp lại một sai lầm trong LESSONS không? Có lựa chọn nào thiếu câu trả lời "tại sao" không?
6. K1, K2 có còn phần kết luận cũ dễ gây neo (research gap, novelty, diễn giải hướng dẫn của cô) không?
7. AGENTS.md có chỗ nào mâu thuẫn, mơ hồ, hoặc không đủ để một agent mới trên máy mới làm tiếp được không?

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.
Mỗi điểm: mức CHẶN hoặc KHÔNG CHẶN; ở đâu; sai gì; bằng chứng; đề xuất sửa ngắn. Tiếng Việt, câu ngắn.
```

---

## Phiên 1 (tiếp) — 02/10/2026 — Claude — laptop của Minh — vai trò: người làm

**Quyết định của Minh trong phiên:** duyệt E1. Chưa trả lời các mục (a)–(d): số phận `docs/DE-XUAT-KHUNG-LAM-VIEC.md`, DX-06…DX-16, chú thích cho Q-08, remote GitHub và commit đầu tiên.

**Kết thúc phiên:**
1. Đã làm gì: thêm mục 5a "Task khó, phiên dài" vào AGENTS.md, đúng nguyên văn E1.
2. File đã thay đổi: `AGENTS.md`, file LOG này.
3. Kiểm tra đã chạy: không có (chỉ chèn văn bản).
4. Điều chưa chắc hoặc cần Minh quyết: các mục (a)–(d) ở trên; duyệt G0.
5. Bước tiếp theo chính xác: Minh chạy Codex phản biện T-000 bằng lệnh và prompt ở mục "Prompt phản biện" bên trên.
6. Lệnh cuối cùng đã chạy: ghi thêm mục này vào LOG.

---

## Phiên 2 — 02/10/2026 — Claude — laptop của Minh — vai trò: người làm (phản hồi phản biện)

**Mở phiên:** đã đọc AGENTS, STATE, SPEC, mục cuối LOG. Kiểm đầu ra phiên trước: `REVIEW.md` có thật, 12 điểm (9 CHẶN, 3 KHÔNG CHẶN), bảng phản hồi còn trống. STATE ghi "Chờ phản biện G0", khớp LOG. Phiên phản biện của Codex không ghi LOG (prompt chỉ cho ghi REVIEW; xem R7).

**Việc Minh giao (nguyên lời):** "Đọc AGENTS.md. Task T-000 đã có REVIEW.md, hãy ghi ý kiến cho từng điểm vào bảng cuối REVIEW.md và vào LOG, chưa sửa gì khác."

**Diễn biến:**
- Đọc lại các chỗ REVIEW dẫn: MRP, WHY, DECISIONS, LESSONS, LESSONS-v1 (SL7, SL15, SL21, SL22, ST3–ST5), K1 (phần I §1, A.1, B.1, C.3, C.7, §E, §H), K2, review-prompt, CLAUDE.md, mẫu task.
- Đọc code bên ngoài (chỉ đọc, bằng `curl` từ raw.githubusercontent.com):
  - RCAEval tại revision MRP P1 dẫn: `RCAEval/e2e/__init__.py`, `circa.py`, `cloudranger.py`, `easyrca.py`, `microcause.py`, `baro.py`, `main.py`;
  - Eadro `codes/base.py`, nhánh main;
  - MicroRank `online_rca.py`, nhánh main.
- Ghi ý kiến cho R1–R12 vào bảng cuối `REVIEW.md`. Cột "Minh quyết" để trống.

**Ý kiến người làm cho từng điểm** (lý do đầy đủ ở bảng cuối `REVIEW.md`):
- **R1 — Đúng.** MRP §4 hứa không nhìn bộ giữ ngoài, P2 bắt đọc schema mọi ứng viên. Gốc lỗi là MRP chưa định nghĩa "nhìn"; v1 cũng đã đọc schema cả 90 ca RE2-TT (K2 §1). Đề nghị định nghĩa: được đọc metadata, schema, đếm nhãn; không xem dữ liệu đo hay kết quả phương pháp từng ca.
- **R2 — Đúng.** Code Eadro chọn checkpoint theo HR@1 trên `test_loader`. Cần chốt ở G1: nhãn nào để học, nhãn nào để chọn mô hình, nhãn nào chỉ để chấm. Mô hình có giám sát không chuyển sang bộ giữ ngoài có tập service khác; đụng R1.
- **R3 — Đúng; phản ví dụ cần nói hẹp lại.** Đồ thị con theo cạnh (kiểu MicroRCA) vẫn kéo được B vào qua cạnh A→B. Lỗ hổng còn với gốc không có cạnh hoặc không có tín hiệu. "PageRank anomaly" ở tầng xếp hạng trái K1 §E.
- **R4 — Đúng, không chặn.** RE2-TT chỉ có thời điểm tiêm; gọi đúng tên độ trễ phát hiện.
- **R5 — Đúng một phần.** WHY-10 "mọi cách chia đều lộ đáp án" sai; nguy cơ thật là mô hình có giám sát thu hẹp tập ứng viên xuống 5 service gốc (lập luận, chưa kiểm). WHY-03 đúng ở chỗ không tách được vị trí khỏi danh tính service, nhưng "gần như chắc chắn" là quá tay (SL21).
- **R6 — Đúng, không chặn.** Đề nghị thêm ghi chú ở đầu K1, K2 thay vì sửa từng dòng, vì đây là bản trích nguyên văn.
- **R7 — Đúng.** AGENTS §4, §6, §7, §9, review-prompt dòng 17 và mẫu REVIEW không nhất quán về quyền ghi; CLAUDE.md dòng 3 "agent chính" trái Q-13. Không ảnh hưởng nội dung MRP.
- **R8 — Đúng.** WHY-02 dựng phương án đối lập sai; MRP dòng 194 khẳng định cơ chế tách tự sinh/kế thừa trước P4. Ghi là ứng viên gắn với giả thuyết đầu của P4, chưa kiểm.
- **R9 — Đúng.** Wrapper `rca` vẫn trả thứ tự cột khi lỗi, chỉ thêm cảnh báo. Nhánh `_failed.json` trong `main.py` nằm sau `raise e` nên không chạy. MRP P3 và WHY-05 nói "đã sửa" là sai.
- **R10 — Đúng; phạm vi rộng hơn.** `main.py` chọn SLI theo service gốc lấy từ tên thư mục ca. Ngoài CloudRanger, EasyRCA và MicroCause cũng dùng `sli`.
- **R11 — Đúng.** Nhánh "không đồ thị" phải nói rõ có giữ self-time và đặc trưng theo nút cha không. Chốt ở G3; có thể thêm một câu vào WHY-07 ngay.
- **R12 — Đúng, không chặn.** Code tác giả dùng PageRank làm trọng số cho spectrum analysis rồi mới xếp hạng.

**Đề xuất sửa, gom theo file** (chưa làm; mỗi file sẽ trình đoạn cũ → đoạn mới theo Luật 0 sau khi Minh quyết từng điểm):
- `docs/MRP.md`: R1 (§4 định nghĩa "nhìn"), R3 và R8 (§2.3, P6 tầng 2–4), R4 (§4 tiêu chí 2, P7 độ đo), R9 (P3 dòng 150), R12 (§2.3, P6). R2 chốt ở G1, R10 ở P3, R11 ở G3.
- `docs/WHY.md`: R5 (WHY-03, WHY-10), R8 (WHY-02), R9 (WHY-05), R11 (WHY-07).
- `docs/knowledge/K1-phuong-phap-rca.md`, `K2-du-lieu.md`: R6 (ghi chú đầu file).
- `AGENTS.md`, `docs/review-prompt.md`, `tasks/_MAU/REVIEW.md`, `CLAUDE.md`: R7.

**Quyết định của Minh trong phiên:** chưa có.

**Kết thúc phiên:**
1. Đã làm gì: kiểm 12 điểm phản biện trên file repo và trên code gốc; ghi ý kiến vào bảng cuối `REVIEW.md` và vào mục này.
2. File đã thay đổi: `tasks/T-000-nen-tang/REVIEW.md` (chỉ các dòng R1–R12 của bảng cuối); `tasks/T-000-nen-tang/LOG.md` (thêm mục này). Không sửa file nào khác. STATE chưa cập nhật vì Minh dặn "chưa sửa gì khác".
3. Kiểm tra đã chạy và kết quả:
   - Đối chiếu từng dòng REVIEW dẫn trong MRP, WHY, K1, K2, AGENTS, CLAUDE.md: các trích dẫn khớp.
   - RCAEval: xác nhận R9 (fallback thứ tự cột; nhánh `_failed.json` không chạy) và R10 (SLI lấy theo service gốc; dùng ở CloudRanger, EasyRCA, MicroCause).
   - Eadro: xác nhận R2 (chọn checkpoint theo HR@1 trên test).
   - MicroRank: xác nhận R12 (PageRank → spectrum → xếp hạng).
   - Không chạy thực nghiệm, không tải dataset, không mở `data/locked/`, không đọc repo cũ.
4. Điều chưa chắc hoặc cần Minh quyết:
   - Cột "Minh quyết" cho R1–R12.
   - R1: cách định nghĩa "nhìn" với bộ giữ ngoài (đề nghị ở trên, hoặc một trong hai cách reviewer nêu).
   - R7: phiên phản biện chỉ ghi REVIEW, hay được thêm một mục LOG.
   - Dòng T-000 trong STATE vẫn ghi "Chờ phản biện G0". Đề nghị đổi thành "Đã có phản biện và phản hồi; chờ Minh quyết từng điểm".
   - Code Eadro và MicroRank đọc ở nhánh main, chưa ghim revision.
   - Ngoài phản biện, không chặn: bảng §1 của MRP, hàng "Bài học v1/v2", bị vỡ dòng và trỏ sang K1/K2 thay vì `LESSONS.md`.
5. Bước tiếp theo chính xác: Minh điền cột "Minh quyết" ở bảng cuối `tasks/T-000-nen-tang/REVIEW.md` (hoặc trả lời trong chat). Phiên sau: đọc bảng đó, trình đề xuất sửa theo từng file ở mục "Đề xuất sửa" bên trên (đoạn cũ → đoạn mới), chờ Minh duyệt rồi mới sửa. Sau đó Minh duyệt G0.
6. Lệnh cuối cùng đã chạy: `curl -sL https://raw.githubusercontent.com/IntelligentDDS/MicroRank/main/online_rca.py | grep -n -E "pagerank|spectrum|def |sorted|sort"`.

---

## Phiên 1 (tiếp 2) — 02/10/2026 — Claude — laptop của Minh — vai trò: người làm

**Quyết định của Minh trong phiên** (nguyên ý; chưa ghi vào DECISIONS, đang chờ duyệt dòng ghi):
- LLM không bắt buộc phải là Gemini.
- Minh sẽ dựng bộ tạo tải và bộ tiêm lỗi.
- Đồng ý chuyển `DE-XUAT-KHUNG-LAM-VIEC.md` vào T-000 làm lịch sử.
- Bỏ DX-06 đến DX-13. Đồng ý DX-14, DX-15. Muốn dọn các chữ lỗi thời, không còn tàn dư của repo cũ.
- DX-16 chọn (i).

**Kết thúc phiên:**
1. Đã làm gì:
   - Chuyển `docs/DE-XUAT-KHUNG-LAM-VIEC.md` vào `tasks/T-000-nen-tang/`, thêm dòng "LỊCH SỬ".
   - DX-14: trong WHY, đổi 3 chỗ "Task A §" thành "K1 §". LESSONS không có chỗ nào cần đổi.
   - DX-15: sửa câu ở MRP P6.
   - DX-16 (i): tạo `docs/knowledge/K3-dataset-ung-vien.md` và `K4-ho-thuat-toan.md`, chỉ giữ "Cited Findings"; xóa `docs/reference/notes/`; sửa đường dẫn trong MRP §4 và `docs/reference/README.md`.
   - Cập nhật STATE.
2. File đã thay đổi: `docs/WHY.md`, `docs/MRP.md`, `docs/STATE.md`, `docs/reference/README.md`. Tạo mới `docs/knowledge/K3-dataset-ung-vien.md`, `docs/knowledge/K4-ho-thuat-toan.md`, `tasks/T-000-nen-tang/DE-XUAT-KHUNG-LAM-VIEC.md`. Xóa `docs/DE-XUAT-KHUNG-LAM-VIEC.md`, `docs/reference/notes/`.
3. Kiểm tra đã chạy: mỗi lần thay chữ đều kiểm khớp đúng số chỗ; quét K3, K4 để tìm phần suy luận còn sót.
   - **Phát hiện lỗi:** bảng "Căn cứ" ở MRP dòng 18–19 bị dính dòng, mất chữ. Lỗi này có từ lượt sửa K1/K2 của Claude. Chưa sửa, đang chờ Minh duyệt (đề xuất D1).
4. Điều chưa chắc hoặc cần Minh quyết:
   - Các đề xuất dọn D1–D6.
   - Dòng ghi quyết định mới.
   - Q-08 và cách lấy dữ liệu thô.
   - Các quyết định cũ.
5. Bước tiếp theo chính xác: Minh duyệt các đề xuất D1–D6. Sau đó mở phiên Claude mới để trả lời `REVIEW.md`. Codex đã chạy phản biện xong; `REVIEW.md` có sẵn.
6. Lệnh cuối cùng đã chạy: ghi thêm mục này vào LOG.

---

## Phiên 1 (tiếp 3) — 02/10/2026 — Claude — laptop của Minh — vai trò: người làm

**Quyết định của Minh trong phiên** (đã ghi vào DECISIONS, từ Q-18 đến Q-27):
- D-01 giữ nhưng không được làm nhẹ phần nghiên cứu.
- D-02 bỏ.
- "D-04 giữ nhưng không được xem nhẹ anomaly detect, không chỉ tập trung RCA". Danh sách không có D-04; agent đoán là D-07, **chưa xác nhận**.
- D-09: Minh hỏi "khắt khe" nghĩa là gì; **chưa quyết**.
- Các quyết định cũ còn lại: đồng ý.
- Duyệt D1, D2, D3, D4 (soát lại cả K1, K2), D5 (mang dữ liệu cũ về nếu dùng được, tải cái thiếu sau khi trình dung lượng), D6.

**Kết thúc phiên:**
1. Đã làm gì:
   - Sửa bảng hỏng ở MRP dòng 18–19 (D1).
   - Bỏ chữ "Task A/B" trong MRP (D2), README (D3), K1 và K2 (D4).
   - Soát K1–K4: bảng nào cũng đủ cột; không còn tên task cũ hay đường dẫn ra ngoài repo.
   - D5: chú thích Q-08; ngoại lệ dữ liệu thô trong AGENTS luật cứng 7; sửa MRP §11; kiểm 287 file dữ liệu cũ khớp hash Hugging Face rồi chép sang `data/`, trong đó 60 ca chưa nhìn và `cases.parquet` (có nhãn) để trong `data/locked/`; viết `data/README.md`.
   - D6: thêm Q-18 đến Q-27 vào DECISIONS; sửa MRP P8, P10, §10.
2. File đã thay đổi: `docs/MRP.md`, `docs/DECISIONS.md`, `AGENTS.md`, `README.md`, `docs/knowledge/K1-phuong-phap-rca.md`, `docs/knowledge/K2-du-lieu.md`, `data/README.md`, file LOG này, `docs/STATE.md`. Thêm `data/rcaeval/` và `data/locked/` (không đưa vào git).
3. Kiểm tra đã chạy:
   - So hash với Hugging Face: 287/287 file và `cases.parquet` khớp.
   - So bản chép với bản gốc: 287/287 giống hệt.
   - `git status`: chỉ `data/README.md` không bị bỏ qua.
   - Kiểm số cột các bảng trong K1–K4 và MRP: không lệch.
   - Quét tên task cũ trong K1–K4: không còn.
   - Script kiểm nằm ở thư mục tạm của phiên (`verify_old_data.py`, `tables.py`), không thuộc repo.
4. Điều chưa chắc hoặc cần Minh quyết:
   - D-07 hay D-04.
   - Nghĩa của D-09.
   - Các phát hiện khi soát K1, K2: báo trong chat, chưa sửa.
   - Tải 89 file `inject_time.txt` (890 byte).
5. Bước tiếp theo chính xác: mở phiên Claude mới, trả lời `REVIEW.md` của T-000.
6. Lệnh cuối cùng đã chạy: ghi thêm mục này vào LOG.

---

## Phiên 1 (tiếp 4) — 02/10/2026 — Claude — laptop của Minh — vai trò: người làm

**Quyết định của Minh trong phiên** (đã ghi Q-28, Q-29, Q-30):
- "D-04" là gõ nhầm, ý là D-07: giữ, nhưng không xem nhẹ phát hiện bất thường.
- D-09: giữ cả hai nghĩa (a) và (b).
- Duyệt D7.
- Duyệt S2 đến S6.
- S1: Minh hỏi tám phương pháp là gì và có dùng hết không; chưa duyệt sửa.
- inject_time: Minh hỏi tải để làm gì; chưa quyết.

**Kết thúc phiên:**
1. Đã làm gì:
   - S2: bỏ dòng "Ngoài pilot" khỏi K2.
   - S6: sửa tham chiếu §5.6 thành P6 trong MRP.
   - S3, S4, S5: giữ nguyên, không sửa.
   - D7: thêm phát hiện bất thường vào RQ1, RQ2, P1, P3, P4.
   - Sửa câu demo ở P10 theo Q-28; bỏ mục 1 của MRP §10.
   - DECISIONS: thêm Q-28 đến Q-30; bỏ mục "chờ làm rõ"; sửa câu mở đầu.
   - Cập nhật STATE.
2. File đã thay đổi: `docs/MRP.md`, `docs/DECISIONS.md`, `docs/knowledge/K2-du-lieu.md`, `docs/STATE.md`, file LOG này.
3. Kiểm tra đã chạy: mỗi lần thay chữ đều kiểm khớp đúng một chỗ.
4. Điều chưa chắc hoặc cần Minh quyết: S1; tải `inject_time.txt` (đề nghị: để task P3 quyết).
5. Bước tiếp theo chính xác: mở phiên Claude mới, trả lời `REVIEW.md` của T-000.
6. Lệnh cuối cùng đã chạy: ghi thêm mục này vào LOG.

---

## Phiên 1 (tiếp 5) — 02/10/2026 — Claude — vai trò: người làm

**Quyết định của Minh:** duyệt S1.

**Kết thúc phiên:**
1. Đã làm gì: sửa câu "Tám phương pháp là danh sách bắt buộc" ở K1 §1; bỏ dòng S1 khỏi STATE.
2. File đã thay đổi: `docs/knowledge/K1-phuong-phap-rca.md`, `docs/STATE.md`, file LOG này.
3. Kiểm tra đã chạy: câu cũ khớp đúng một chỗ.
4. Điều chưa chắc hoặc cần Minh quyết: xem trả lời trong chat về GNN, adapter, RCAEval; có đề xuất ghi vào MRP, chờ duyệt.
5. Bước tiếp theo chính xác: mở phiên Claude mới, trả lời `REVIEW.md` của T-000.
6. Lệnh cuối cùng đã chạy: ghi thêm mục này vào LOG.

---

## Phiên 1 (tiếp 6) — 02/10/2026 — Claude — vai trò: người làm

**Quyết định của Minh:** "note lại để bước chọn dataset không bị thiên vị RCAEval" (Q-31). E2 chưa được duyệt; chỉ ý thứ ba của E2 được làm, qua Q-31.

**Kết thúc phiên:**
1. Đã làm gì: thêm mục "Chống thiên vị RCAEval khi chọn dataset" vào MRP §4; thêm Q-31 vào DECISIONS.
2. File đã thay đổi: `docs/MRP.md`, `docs/DECISIONS.md`, file LOG này.
3. Kiểm tra đã chạy: chỗ chèn khớp đúng một vị trí.
4. Điều chưa chắc hoặc cần Minh quyết: hai ý còn lại của E2 (cách xử lý phương pháp khó chạy ở P1; adapter chỉ viết sau G1).
5. Bước tiếp theo chính xác: mở phiên Claude mới, trả lời `REVIEW.md` của T-000.
6. Lệnh cuối cùng đã chạy: ghi thêm mục này vào LOG.

---

## Phiên 2 (tiếp) — 02/10/2026 — Claude — laptop của Minh — vai trò: người làm (sửa theo phản biện)

**Quyết định của Minh trong phiên** (nguyên lời; chưa ghi vào DECISIONS, chờ duyệt dòng ghi): "R7: chốt 1 hướng nhất quán để sau này không bị nhập nhằng. R1 đồng ý với đề xuất, sửa r1 đến R12".

**Hướng chốt cho R7:** phiên phản biện chỉ ghi `REVIEW.md`, không ghi LOG hay STATE. Người làm điền bảng "Phản hồi của người làm" ở cuối `REVIEW.md`, ghi LOG, cập nhật STATE. Lý do chọn: Codex phản biện chạy chế độ chỉ đọc (`-s read-only`) và chỉ xuất ra `REVIEW.md`, nên không ghi được LOG; mỗi phiên phản biện một file thì phạm vi rõ.

**Ghi chú về phiên song song:** trong lúc chờ Minh, một phiên Claude khác (các mục "Phiên 1 tiếp 2" đến "tiếp 6" ở trên) đã sửa MRP, K1, K2, AGENTS, DECISIONS, STATE. Phiên này đọc lại bản mới trước khi sửa. Mục S1 của phiên kia đã sửa câu "Tám phương pháp ... bắt buộc" ở K1 §1, nên R6 chỉ còn A.1, C.1, §H của K1 và dòng Leakage của K2.

**Kết thúc phiên:**
1. Đã làm gì (điểm → chỗ sửa):
   - R1: MRP §4 (định nghĩa "nhìn" với dataset giữ ngoài; nghĩa của "chưa mở" ở 60 ca RE2-TT), P2; WHY-04; AGENTS luật cứng 1.
   - R2: MRP §4 (G1 ghi rõ nhãn để học, để chọn, để chấm), P3 (code chọn mô hình bằng test phải đổi sang dev, ví dụ Eadro); WHY-05.
   - R3: MRP §2.3 (tầng 3 thành "vùng nghi ngờ"), P6 tầng 3, tầng 4 (không loại ứng viên chỉ vì chưa vượt ngưỡng).
   - R4: MRP §4 tiêu chí 2, P2 đầu ra, P3, P7 (mốc của độ trễ phát hiện).
   - R5: WHY-03, WHY-10.
   - R6: ghi chú ở đầu K1 và K2; không sửa phần trích nguyên văn.
   - R7: AGENTS §4 (bảng quyền ghi LOG, REVIEW), §5 bước 6 và 7, §6 bước 6, §7, §9; CLAUDE.md (bỏ "agent chính"); `tasks/_MAU/LOG.md` (chỉ người làm ghi).
   - R8: MRP §2.3, P6 (khung bốn tầng là ứng viên; cơ chế tách tự sinh/kế thừa chưa kiểm); WHY-02 (bỏ phương án đối lập sai).
   - R9: MRP P3, bảng rủi ro §9; WHY-05.
   - R10: MRP P2 (kiểm cả runner; SLI không chọn theo nhãn), §6 mục 8; AGENTS luật cứng 6.
   - R11: MRP P7; WHY-07.
   - R12: MRP §2.3, P6 tầng 4 (MicroRank: PageRank làm trọng số cho spectrum analysis).
2. File đã thay đổi: `docs/MRP.md`, `docs/WHY.md`, `docs/knowledge/K1-phuong-phap-rca.md`, `docs/knowledge/K2-du-lieu.md`, `AGENTS.md`, `CLAUDE.md`, `tasks/_MAU/LOG.md`, file LOG này. Chưa sửa STATE, DECISIONS, cột "Minh quyết" của REVIEW.
3. Kiểm tra đã chạy và kết quả:
   - Sửa bằng một script đối chiếu 43 đoạn cũ; mỗi đoạn phải khớp đúng một chỗ, lệch thì không ghi file nào. Lần chạy đầu dừng vì 5 file dùng CRLF, không file nào bị ghi; sửa script giữ CRLF rồi chạy lại: 43/43 khớp. Script nằm ở thư mục tạm của phiên, không thuộc repo.
   - Không còn dòng xuống dòng lẫn kiểu trong 5 file CRLF.
   - Các bảng trong MRP và AGENTS đủ cột.
   - Tìm các câu cũ ("bản sau lần sửa", "chính là vùng đó", "mọi cách chia đều lộ", "so PageRank giữa", "agent chính", "đang phản biện task", "ít rủi ro nhất"): không còn trong AGENTS, CLAUDE, docs, mẫu task.
4. Điều chưa chắc hoặc cần Minh quyết:
   - Ghi quyết định của Minh vào cột "Minh quyết" của `REVIEW.md` và thêm một dòng vào DECISIONS (đề xuất trong chat).
   - Cập nhật dòng T-000 trong STATE (đề xuất trong chat).
   - Có phiên Claude khác cùng sửa repo; nếu phiên đó còn mở, hai phiên có thể ghi đè nhau.
   - Ngoài R1–R12, chưa sửa: ở MRP §3, câu "Phát hiện bất thường không phải phần phụ của RCA..." nằm chen giữa RQ2 và RQ3 làm vỡ danh sách.
   - Code Eadro và MicroRank đọc ở nhánh main, chưa ghim revision.
5. Bước tiếp theo chính xác: Minh xem diff của 7 file trên; duyệt các đề xuất ở mục 4; duyệt G0 (`docs/MRP.md`). Sau đó agent đề xuất commit đầu tiên.
6. Lệnh cuối cùng đã chạy: ghi thêm mục này vào LOG.

---

## Phiên 2 (tiếp 2) — 02/10/2026 — Claude — laptop của Minh — vai trò: người làm

**Quyết định của Minh trong phiên:** "duyệt" cho ba đề xuất (a), (b), (c) ở mục trên.

**Kết thúc phiên:**
1. Đã làm gì: (a) điền cột "Minh quyết" cho R1–R12 trong `REVIEW.md`; (b) thêm Q-32 vào DECISIONS; (c) STATE: T-000 thành "Đã trả lời và sửa R1–R12; chờ Minh duyệt G0", bước tiếp theo là Minh duyệt G0.
2. File đã thay đổi: `tasks/T-000-nen-tang/REVIEW.md`, `docs/DECISIONS.md`, `docs/STATE.md`, file LOG này.
3. Kiểm tra đã chạy: mỗi chỗ sửa khớp đúng một vị trí; 12/12 dòng bảng đã điền; DECISIONS và STATE giữ CRLF, không có dòng xuống dòng lẫn kiểu.
4. Điều chưa chắc hoặc cần Minh quyết: duyệt G0; câu chen giữa RQ2 và RQ3 ở MRP §3 (chưa sửa, chưa đề xuất chi tiết); commit đầu tiên và remote GitHub.
5. Bước tiếp theo chính xác: Minh xem diff của `docs/MRP.md`, `docs/WHY.md`, `AGENTS.md`, rồi duyệt G0. Sau đó agent đề xuất commit đầu tiên.
6. Lệnh cuối cùng đã chạy: ghi thêm mục này vào LOG.

---

## Phiên 2 (tiếp 3) — 02/10/2026 — Claude — laptop của Minh — vai trò: người làm (soát lại G0)

**Quyết định của Minh trong phiên** (nguyên lời): "đồng ý với đề xuất nhỏ, còn về duyệt G0 thì bạn hãy chạy và soát lại 1 lần nữa rồi báo cho tôi, cái tôi cần chủ yếu là mức độ nghiêm trọng và tính khả thi của dự án, tỉ lệ xảy ra kết quả xấu ở bước cuối cùng".

**Diễn biến:**
- Đề xuất nhỏ: chuyển câu "Phát hiện bất thường không phải phần phụ của RCA… (Q-30)" ở MRP §3 xuống sau RQ5, giữ nguyên chữ.
- Soát G0 (chỉ đọc): đọc lại MRP sau sửa, DT18, hướng dẫn của cô, LESSONS-v1, K3, `data/README.md`; xem repo FlashTicket (chỉ đọc, bản clone trên máy, không fetch); kiểm môi trường Python và ổ đĩa.

**Dữ kiện tìm được:**
- Repo RCA chưa có code: `src/`, `results/` rỗng. `py -3` (3.12.10) chưa có pandas, numpy, pyarrow, scipy, sklearn; có torch, networkx. Ổ D còn 63 GB.
- FlashTicket, bản clone trên máy (nhánh hiện tại và `origin/main`): mỗi service trong 5 service chỉ có file khởi động 12 dòng; commit code cuối ngày 19/09; chưa thấy cấu hình OTel, Tempo, Loki. Chưa biết ba bạn có code ở nơi khác không.
- Baseline đơn giản rất mạnh: SimpleRCA (không đồ thị) top-1 0,80 trên RE2-TT (LESSONS ST10) và 0,93 trên Nezha-TT; bài FSE 2026 ghi nó ngang hoặc hơn SOTA trên nhiều dataset (K3 Q2, Q4). Chưa đối chiếu bản in.
- 67% ca RE2-TT triệu chứng chỉ ở service gốc (ST10, số của bài ngoài, chưa kiểm). v1: đồ thị chỉ giúp 1/10 ô trên dev30 (ST6).
- Thời gian: còn 18 ngày tới mốc 20/10 (G4), 89 ngày tới 30/12.

**Đánh giá đã báo Minh trong chat (ước lượng chủ quan, chưa kiểm):**
- Không có kết quả G4 đủ phạm vi MRP trước 20/10: khoảng 80–90%.
- P7: phương pháp đồ thị không hơn rõ baseline mạnh nhất trên tổng thể (RQ3b, dữ liệu giữ ngoài): khoảng 65–80%.
- P7: không có điều kiện con nào mà đồ thị giúp và qua được cả hai đối chứng: khoảng 40–60%.
- P10: FlashTicket không cho được số đo định lượng (RQ5, RQ3c): khoảng 50–65%.
- Kết luận: về tính đúng, MRP sau R1–R12 không còn lỗi chặn. Rủi ro lớn là phạm vi so với thời gian, và việc MRP chưa nói thẳng kết cục dễ xảy ra nhất của RQ3b (QT16).

**Đề xuất chờ Minh quyết (chưa sửa):**
1. Thêm "đường tối thiểu tới 20/10" vào MRP §7 (cắt phạm vi, thứ tự ưu tiên).
2. Nói thẳng ở MRP §3 kết cục dễ xảy ra nhất của RQ3b; đưa vào báo cáo tiến độ đầu tiên cho cô.
3. Ghi trạng thái thật của FlashTicket vào MRP §1, §9; tách demo (bắt buộc) với số đo RQ5.
4. Sửa ba chỗ còn ghi "chờ xác nhận lại" dù đã xác nhận: MRP §2.3 (D-12 → Q-24), MRP §7 (mốc 30/12 → Q-23), WHY-10 (D-14 → Q-25).

**Kết thúc phiên:**
1. Đã làm gì: đề xuất nhỏ ở MRP §3; soát lại G0 và báo đánh giá.
2. File đã thay đổi: `docs/MRP.md` (chuyển một câu), file LOG này.
3. Kiểm tra đã chạy: chỗ chuyển câu khớp đúng một vị trí, giữ CRLF; các lệnh chỉ đọc ở repo FlashTicket, môi trường Python, ổ đĩa.
4. Điều chưa chắc hoặc cần Minh quyết: đề xuất 1–4 ở trên; tiến độ thật của hệ FlashTicket; cô chấp nhận kết quả "đồ thị không thắng" tới đâu (Q-05 chưa hỏi cô).
5. Bước tiếp theo chính xác: Minh quyết đề xuất 1–4, rồi duyệt G0. Sau G0, agent đề xuất commit đầu tiên và SPEC cho task đầu của P1, P2.
6. Lệnh cuối cùng đã chạy: ghi thêm mục này vào LOG.

---

## Phiên 2 (tiếp 4) — 02/10/2026 — Claude — laptop của Minh — vai trò: người làm

**Quyết định của Minh trong phiên** (nguyên lời): "flash ticket tôi đảm bảo sẽ xong nên không cần nhắc lại, cả vấn đề thời hạn nữa. đồng ý đề xuất 4, bỏ đề xuất 3, đề xuất 1 2 thì tôi chưa hiểu, giải thích dễ hiểu". Minh không phản đối việc đọc v1, nhưng yêu cầu mọi nhận định có phản biện đa chiều: kết quả là thế, nhưng có nguyên nhân khả thi nào khác giải thích nó không.

**Diễn biến:**
- Đề xuất 4: MRP §2.3 "(quyết định cũ D-12, chờ Minh xác nhận lại)" → "(Q-24)"; MRP §7 mốc 30/12 → "(Q-23)"; WHY-10 "(quyết định cũ D-14, chờ xác nhận lại)" → "(Q-25)". Đề xuất 3 bỏ.
- Đọc abstract arXiv 2510.04711 (bài FSE 2026): trên benchmark mới của họ, 11 phương pháp SOTA đạt Top@1 trung bình 0,21, tốt nhất 0,37. Abstract không nêu số của SimpleRCA trên benchmark này.
- Trả lời Minh: vì sao SimpleRCA mạnh mà vẫn có phương pháp mới; v1 đọc từ `docs/LESSONS.md`, `docs/reference/LESSONS-v1.md`, K2 (không mở repo cũ); các cách giải thích khác cho kết quả "đồ thị giúp 1/10 ô" của v1. Rút lại hai ước lượng P7 ở mục trước vì căn cứ yếu hơn đã trình bày.
- Giải thích đề xuất 1 và 2; đề nghị bỏ đề xuất 1 vì lý do chính của nó là thời hạn.

**Kết thúc phiên:**
1. Đã làm gì: như trên.
2. File đã thay đổi: `docs/MRP.md`, `docs/WHY.md`, file LOG này.
3. Kiểm tra đã chạy: ba chỗ thay đều khớp đúng một vị trí; không còn chữ "chờ xác nhận lại" trong MRP, WHY.
4. Điều chưa chắc hoặc cần Minh quyết: đề xuất 1 (đề nghị bỏ), đề xuất 2; đề xuất ghi Q-33, Q-34 vào DECISIONS và thêm một dòng vào AGENTS §11 (nguyên văn trong chat).
5. Bước tiếp theo chính xác: Minh quyết các mục ở 4, rồi duyệt G0.
6. Lệnh cuối cùng đã chạy: ghi thêm mục này vào LOG.

---

## Phiên 2 (tiếp 5) — 02/10/2026 — Claude — laptop của Minh — vai trò: người làm

**Quyết định của Minh trong phiên:**
- Duyệt Q-33, Q-34 và một dòng thêm vào AGENTS §11 (đã làm).
- Nguyên lời: "tôi quyết định là không nhất thiết kết quả phải đẹp nhưng phải chỉ ra được lí do, như cô hướng dẫn là tìm được chưa được rồi từ đó tiến đến đồ thị. quan trọng là phải chỉ ta được lí do dù kết quả tệ hay tốt". Chưa ghi vào DECISIONS; đã đề xuất Q-35.

**Kết thúc phiên:**
1. Đã làm gì: thêm Q-33, Q-34 vào DECISIONS; thêm dòng "Dùng một kết quả làm căn cứ mà chưa nêu các nguyên nhân khả thi khác có thể giải thích nó." vào AGENTS §11.
2. File đã thay đổi: `docs/DECISIONS.md`, `AGENTS.md`, file LOG này.
3. Kiểm tra đã chạy: mỗi chỗ chèn khớp đúng một vị trí, giữ CRLF.
4. Điều chưa chắc hoặc cần Minh quyết: đề xuất 1 (em đề nghị bỏ), đề xuất 2 (tách ca lỗi lan và không lan), Q-35, câu "lý do" ở MRP §3, câu "phát hiện bằng đồ thị là bắt buộc" ở P6 tầng 2.
5. Bước tiếp theo chính xác: Minh quyết các mục ở 4, rồi duyệt G0.
6. Lệnh cuối cùng đã chạy: ghi thêm mục này vào LOG.

---

## Phiên 2 (tiếp 6) — 02/10/2026 — Claude — laptop của Minh — vai trò: người làm

**Quyết định của Minh trong phiên:** duyệt mục 3 (Q-35), 4 (lý do trong "Hoàn thành nghĩa là gì"), 5 (phát hiện bằng đồ thị là bắt buộc). Mục 1 (vòng hẹp) và 2 (tách ca lan/không lan): Minh hỏi thêm, chưa quyết.

**Kết thúc phiên:**
1. Đã làm gì: thêm Q-35 vào DECISIONS; sửa MRP §3 và MRP P6 tầng 2.
2. File đã thay đổi: `docs/DECISIONS.md`, `docs/MRP.md`, file LOG này.
3. Kiểm tra đã chạy: mỗi chỗ sửa khớp đúng một vị trí, giữ CRLF.
4. Điều chưa chắc hoặc cần Minh quyết: mục 1, mục 2 (đã giải thích thêm trong chat).
5. Bước tiếp theo chính xác: Minh quyết mục 1, 2; duyệt G0.
6. Lệnh cuối cùng đã chạy: ghi thêm mục này vào LOG.

---

## Phiên 2 (tiếp 7) — 02/10/2026 — Claude — laptop của Minh — vai trò: người làm

**Quyết định của Minh trong phiên:** đồng ý bỏ đề xuất 1 (vòng hẹp); MRP giữ thứ tự hiện tại. Duyệt mục 2 theo cách nhẹ: không gắn nhãn "lan" ở P2; P4 phân loại ca sai theo cơ chế; chỉ định nghĩa nhãn "lan" nếu P4 thấy cần, khóa ở G3, dùng ở P7.

**Kết thúc phiên:**
1. Đã làm gì: sửa MRP P2 (ước lượng thô tiêu chí 7), P4 (điều kiện và cách định nghĩa nhãn "lan"), P7 (báo theo nhóm nếu có nhãn).
2. File đã thay đổi: `docs/MRP.md`, file LOG này.
3. Kiểm tra đã chạy: ba chỗ sửa khớp đúng một vị trí, giữ CRLF.
4. Điều chưa chắc hoặc cần Minh quyết: duyệt G0; Minh để trống mục 3 ở tin nhắn trước.
5. Bước tiếp theo chính xác: Minh duyệt G0 (`docs/MRP.md`). Sau đó agent đề xuất commit đầu tiên, cập nhật STATE, và đề xuất SPEC cho task đầu của P1, P2.
6. Lệnh cuối cùng đã chạy: ghi thêm mục này vào LOG.

---

## Phiên 2 (tiếp 8) — 02/10/2026 — Claude — laptop của Minh — vai trò: người làm

**Quyết định của Minh trong phiên** (nguyên lời): "duyệt G0". Các việc đi kèm (ghi DECISIONS, đổi trạng thái MRP, WHY, SPEC, STATE, commit đầu tiên) đã đề xuất trong chat, chờ duyệt.

**Quyết định của Minh** (nguyên lời): "duyệt A, còn về commit thì chưa commit vội … tôi muốn để codex commit và push".

**Kết thúc phiên (đóng T-000):**
1. Đã làm gì: gói A — Q-36 vào DECISIONS; MRP dòng 3 thành "đã duyệt G0"; WHY-01, 02, 08, 09 thành "Đã quyết (Q-36)"; SPEC T-000 thành "xong"; STATE: cổng G1, T-000 xong, bước tiếp theo tạo task P1, P2, P9a. Chưa commit.
2. File đã thay đổi: `docs/DECISIONS.md`, `docs/MRP.md`, `docs/WHY.md`, `docs/STATE.md`, `tasks/T-000-nen-tang/SPEC.md`, file LOG này.
3. Kiểm tra đã chạy: mỗi chỗ sửa khớp đúng số vị trí dự kiến, giữ kiểu xuống dòng của từng file.
4. Điều chưa chắc hoặc cần Minh quyết: commit đầu tiên do Codex làm (repo chưa có commit, chưa có remote); SPEC task đầu của P1, P2.
5. Bước tiếp theo chính xác: Minh mở phiên Codex để commit và push; sau đó agent đề xuất SPEC task đầu tiên của P1 và P2.
6. Lệnh cuối cùng đã chạy: ghi thêm mục này vào LOG.

---

## Bổ sung sau khi đóng — 03/10/2026 — Claude — laptop của Minh

**Quyết định của Minh:** duyệt prompt mạnh hơn cho người làm ở bước 7 (tự soát độc lập trước khi đọc REVIEW, không mặc nhiên đồng ý reviewer, thêm điểm N1, N2… tự tìm).

**Đã làm:** thêm mục "Prompt cho người làm phản hồi phản biện" vào `docs/review-prompt.md` và sửa dòng 17 trỏ tới mục đó; thêm câu "Prompt mẫu ở `docs/review-prompt.md`." vào AGENTS §5 bước 7. Mỗi chỗ sửa khớp đúng một vị trí. Chưa commit. Đề xuất ghi Q-37 vào DECISIONS đang chờ Minh duyệt.
Minh duyệt; đã ghi Q-37 vào DECISIONS.
Đính chính dòng trên: Q-37, Q-38 đã được phiên T-001 dùng trước; quyết định này ghi thành Q-39.
