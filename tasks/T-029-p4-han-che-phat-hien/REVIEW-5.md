# Phản biện T-029 — lượt 5: rà soát độc lập sau sửa REVIEW-4

- **Người phản biện:** Claude — **Ngày:** 09/10/2026 — **Commit/diff đã đọc:** working tree so với `6c93e6dc31f0c991b4ac6d1cfd44fcc0e989c84c` (HEAD). `git diff` chỉ có `docs/DECISIONS.md` (Q-84–Q-86), `docs/STATE.md`, `docs/WHY.md` (nối WHY-39). Thư mục task và `results/T-029/` chưa được track, đã đọc trực tiếp.
- **Tên file:** theo prompt của Minh, `REVIEW.md` hiểu là `REVIEW-5.md`. Bốn file REVIEW cũ giữ nguyên.
- **Đã đọc:** `AGENTS.md`; SPEC; LOG (phiên 8–10 đầy đủ, các phiên trước qua REVIEW-4); REVIEW-4 và bảng phản hồi; năm báo cáo (toàn bộ phần sửa và các mục C1–C6, HP, định vị, P1/P2, bảng G); `theo-ca.json`, `bocpd-can-thiep.json`, `n-sigma-cot.json`, `dinh-vi.json`, `a-so-b.json`; artefact I1 trong `runs/ec2-complete-002/`; `runs/review4-repair-001/` (diff, summary, verification); `runs/V8-reports-003/verification.json`; `runs/handoff-session8-001/manifest.json`; `runs/final-verification-001/verification.json`; nguồn đóng băng `results/T-024/cham-a.json`, `results/T-025/cham-b.json`.
- **Lệnh đã chạy:** chỉ đọc. Python T-014-main theo `results/T-031/moi-truong.json → lenh_chay`, `-B -X utf8 -W ignore`, code qua stdin, không ghi file. Không chạy detector hay ranker, không đọc telemetry, không SSH/EC2, không mở `data/locked/`.

## Kết luận chung

Không có lỗi đáng kể. Ba điểm của REVIEW-4 đã được sửa đúng phạm vi Minh duyệt, và mọi số mới khớp JSON nguồn khi tôi tính lại. R1 (CHẶN) đã hết: chiều tác động của I1, nghĩa giới hạn của B2 và điều kiện của 3 ca S nay nằm ở câu mở đầu, C1, HP-6 và đọc tay. Phần chưa sửa trong lượt này (bảng G, P1/P2, định vị) tôi soát lại cũng không thấy lỗi.

## Các điểm

Không có điểm CHẶN hay KHÔNG CHẶN.

## Điều đã kiểm và thấy đúng

- **Hash trước khi dùng kết quả:**
  - 3378/3378 tệp trong `runs/review4-repair-001/verification.json` khớp SHA và kích thước, không thiếu tệp.
  - So với `handoff-session8-001/manifest.json` (3362 tệp): chỉ 3 báo cáo đã duyệt sửa đổi (`ban-do-han-che-phat-hien.md`, `dinh-vi.md`, `doc-tay.md`). SHA của `final-verification-001/verification.json` và `V8-reports-002/verification.json` trùng giá trị ghi trong manifest.
- **R1 — chiều can thiệp I1:** tính lại từ `bocpd-can-thiep.json#/cases` và `theo-ca.json#/rows`:
  - tổng điểm đổi Nv full/I1/I2 = 143/338/332;
  - số điểm đổi I1 tăng/bằng/giảm = 23/3/4;
  - báo đầu I1 sớm/bằng/muộn = 29/1/0; ca bằng là `dev-746fd74313` (102);
  - 17/17 ca B2/5 có báo đầu I1 sớm hơn;
  - 3 ca S: 748→246, 761→238, 752→214; Nv 0→12, 0→11, 0→16.
  - Bảng theo ô mới ở báo cáo chính khớp từng ô (n, full, I1, I2, sớm/bằng/muộn, tăng/bằng/giảm).
  - Đếm Nv full bằng số điểm đổi < 720 ở 30/30 ca. Báo đầu full bằng `min(full)` ở 30/30 ca, nên so `min(I1)` với t̂ là so cùng đại lượng.
  - Câu mới không nói quá: không viết "ít hơn" cho mọi ca, tách báo đầu khỏi số điểm đổi, giữ giới hạn "I1 vẫn nhìn trước trong tiền tố".
  - Câu "I1 đổi bộ cột": số chiều I1 nhỏ hơn full ở 13/30 ca, bằng ở 17/30 (`input_shape.cot_sau_tien_xu_ly` của artefact I1). Câu này đúng.
- **R2 — B4 và D0:**
  - HP-8, chú giải V7 và đọc tay nay ghi B4 là mô tả, không dùng riêng làm lời giải thích. Đọc tay liệt kê đủ 4 ca B4/w60/k2 bằng đúng số.
  - Không đổi cờ, D0 hay ngưỡng, đúng phạm vi Minh duyệt.
  - Ở 3 ca S, cả 26/26 cờ đều N/A. Vì vậy D0 ở S là hệ quả của miền hợp lệ. HP-9 viết "có thể do miền N/A", yếu hơn dữ liệu nhưng không sai, vì đã kèm "không tính thành thất bại báo sớm".
- **R3 — coverage mức nền:** tính lại từ `n-sigma-cot.json` và `dinh-vi.json`:
  - Số dịch vụ có cột khớp bảng 8 dòng: N-Sigma chính 22–28, 13–27, 17–28, 18–28; đối chứng 68, 64–68, 68, 68.
  - Số ca root hết cột khớp: 0/4/2/1 cho N-Sigma chính, 0 cho đối chứng.
  - 60/60 dòng coverage theo ca khớp.
  - C3 và `dinh-vi.md` nay ghi rõ mức nền 68 gồm dịch vụ không thể báo, và chênh so với mức nền chưa tách được phần do tập cột. Mức nền đã khóa giữ nguyên.
- **V8:** `V8-reports-003/verification.json` cho PASS, 0 lệch. File chứa đúng SHA hiện tại của cả năm báo cáo.
- **Bảng G (C4), soát lại độc lập:**
  - 1440 giá trị Hit@1/Hit@5 (2 bộ × 4 phương pháp × 30 ca × 3 điểm × 2 chỉ số) khớp công thức hòa kỳ vọng từ `rank_min`/`rank_max`/status, lấy trung bình seed cho TORAI.
  - Điểm (a) và t̂ khớp nguồn đóng băng `cham-a.json` và `cham-b.json` theo `frozen_score_sources`.
  - Δ cửa sổ và Δ sự kiện khớp hiệu từng ca.
  - t̂⁺ và nhóm S/E-gần/E-xa trùng `theo-ca.json` ở mọi dòng.
- **P2:** định nghĩa "tách hoàn toàn" (đồng nhất trong từng root, khác giữa ít nhất hai root) được ghi rõ. Liên hệ một phía của 6 cột latency vắng ở 4/6 ca order được báo, không bị che. Câu trả lời C5 không nói quá.
- **Nhãn và phạm vi ghi:**
  - Phần sửa chỉ dùng root để chấm và để đếm "cột root". Không đưa nhãn vào đặc trưng hay cờ.
  - Script mới `repair_review4.py` và `verify_reports_review4.py` chỉ đọc JSON đã đóng băng.
  - Không thấy ghi ra ngoài `results/T-029/`, LOG, dòng T-029 của STATE và bảng người làm của REVIEW-4. WHY và DECISIONS giữ hash.
- **DT18 và hướng dẫn của cô:** không đổi so với REVIEW-4. Task vẫn đúng bước "chỉ ra hạn chế của phương pháp đã có" (DT18-NV2/NV3). Không cam kết thiết kế P5/P6, không kết luận "lan".
- **Tiêu chí xong:** giữ như REVIEW-4 đã kiểm. Phần sửa không làm mất đầu ra nào. Còn phải chờ Minh duyệt đóng.

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
