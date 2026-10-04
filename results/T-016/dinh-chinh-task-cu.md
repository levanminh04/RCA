# Vấn đề ở task cũ (T-000 … T-012) liên quan TORAI, RCD

> **Đã áp D1–D6 (Minh duyệt 04/10/2026).** D6: câu được thêm vào ô cuối của dòng 111 trong `results/T-005/moi-truong.md` (không chèn dòng mới, vì dòng 111 nằm giữa bảng). D2: ghi chú nối vào cuối `tasks/T-006-kiem-dung-dan-laptop/LOG.md` (LOG chỉ ghi thêm).

T-016. Không sửa file nào của task cũ. Mỗi mục: task, file:dòng, sai gì, bằng chứng, kết luận bị ảnh hưởng, đã làm gì trong T-016, đề xuất đoạn cũ → đoạn mới (chờ Minh duyệt). Mức: **sai** (khẳng định không đúng), **thiếu** (khẳng định đúng nhưng bỏ sót điều làm đổi cách hiểu), **cập nhật** (điểm còn mở, nay có số).

## D1 — T-001: mô tả sai hậu quả của giảm mẫu hai lần (mức: sai)

- **Ở đâu:** `results/T-001/danh-sach-phuong-phap.md:112` (mục 3a, dòng 9, TORAI).
- **Sai gì:** "Với `--length 10` … lõi RCD chỉ nhận khoảng 3 dòng metric, phần lớn ô bị điền 0." Thực tế: sau lần giảm thứ hai, nửa lỗi chỉ còn 1 dòng, nên mọi cột metric bị bỏ vì hằng; lõi RCD nhận **0 cột metric**, chỉ có cột log trên 21 + 21 dòng, mỗi nửa có 1 dòng giả toàn 0 do ghép theo chỉ số.
- **Bằng chứng:** `runs/s4-soi-dau-vao-OB-len10.jsonl` (90/90 ca: 2 + 1 dòng, 0 cột sống sót); giá trị trung gian lượt chính thức `cham/s7-tong-hop.json` (184/184 cụm OB: 0 cột metric, 21 + 21 dòng); ví dụ tay `vi-du-tinh-tay.md` mục 4. T-005 đã ghi đúng (`results/T-005/do-kha-thi.md:42`).
- **Kết luận bị ảnh hưởng:** chỉ phần mô tả cơ chế; danh sách phương pháp không đổi.
- **Đã làm:** `giam-mau-hai-lan.md`.
- **Đề xuất sửa** (`danh-sach-phuong-phap.md:112`): "lõi RCD chỉ nhận khoảng 3 dòng metric, phần lớn ô bị điền 0." → "nửa lỗi chỉ còn 1 dòng metric nên mọi cột metric bị bỏ vì hằng; lõi RCD chỉ nhận cột log, mỗi nửa thêm 1 dòng giả toàn 0 do ghép theo chỉ số (đã kiểm ở T-016, `results/T-016/giam-mau-hai-lan.md`)." Đồng thời đổi "**Chưa kiểm bằng chạy, suy từ code:**" thành "**Đã kiểm ở T-016:**".

## D2 — T-006 LOG: gán cho bài TORAI một câu bài không có (mức: sai)

- **Ở đâu:** `tasks/T-006-kiem-dung-dan-laptop/LOG.md:334` (ghi chú chuyển từ T-005, REVIEW T-005 R1): "(bài TORAI nói metric lấy lại mẫu 15 s)". Câu này cũng được chép vào prompt của T-016.
- **Sai gì:** văn bản bài TORAI (`arXiv 2604.13522v1`, bản HTML) không nêu chu kỳ 15 s ở đâu; §3.1 chỉ nói đếm mẫu log theo thời gian. Chu kỳ 15 s chỉ có trong `RCAEval/docs/TORAI.md` (mục Data Format) và chú thích `torai.py:80`.
- **Bằng chứng:** tìm "15 s", "15-second", "second", "resampl", "interval", "sampling" trong văn bản bài (LOG T-016 08:35); chỉ thấy "requests per minute" ở §3.1.
- **Kết luận bị ảnh hưởng:** lập luận "lỗi hay chủ ý" không được dựa vào bài; T-016 dựa vào tài liệu RCAEval và code (`giam-mau-hai-lan.md` mục 4).
- **Đề xuất:** LOG chỉ ghi thêm, nên thêm vào cuối `tasks/T-006-kiem-dung-dan-laptop/LOG.md` một ghi chú: "Đính chính 04/10 (T-016): câu '(bài TORAI nói metric lấy lại mẫu 15 s)' ở ghi chú chuyển từ T-005 không đúng: bài không nêu chu kỳ; 15 s có ở `RCAEval/docs/TORAI.md` và chú thích `torai.py:80`."

## D3 — T-006: "TORAI khớp" thiếu phép kiểm nhánh dự phòng bên trong (mức: thiếu)

- **Ở đâu:** `results/T-006/kiem-dung-dan.md:31` (mục 1, dòng TORAI) và `:252` (mục 7, "Kết luận: khớp.").
- **Thiếu gì:** T-006 kiểm "đầu ra rỗng, trùng thứ tự cột, lỗi" cho TORAI, nhưng không kiểm nhánh dự phòng **bên trong** `torai()` (`torai.py:330-334`) và không soi đầu vào của bước nhân quả. Ở đúng cấu hình T-006 chạy (cửa sổ 10), 176/184 cụm OB và 171/173 cụm SS rơi nhánh dự phòng; 0 cột metric vào RCD; thứ hạng cuối trùng thứ hạng "chỉ mức nghiêm trọng" ở 86/90 ca OB, 88/90 SS. "Khớp" đúng về số, nhưng không cho biết TORAI chạy đúng phương pháp của bài (SL24: khớp số ≠ đúng).
- **Bằng chứng:** `cham/s7-tong-hop.json`, `giam-mau-hai-lan.md` mục 5; điểm bản gốc seed 0–4 = 0,913 (OB), trùng T-006.
- **Kết luận bị ảnh hưởng:** câu "TORAI khớp" trong T-006 mục 1, 7 nếu được dùng làm căn cứ "TORAI đã kiểm đúng đắn" ở G1.
- **Đã làm:** đo tỉ lệ nhánh dự phòng mọi cấu hình; bản sửa (`src/torai/`); `kiem-khong-nhan.md` mục 4b.
- **Đề xuất sửa** (`kiem-dung-dan.md`, cuối mục 7, thêm một gạch đầu dòng): "- Khớp ở đây là khớp số công bố, chưa phải chạy đúng phương pháp. T-016 đo trên cùng cấu hình: lõi RCD không nhận cột metric nào (lỗi giảm mẫu hai lần) và 176/184 cụm (OB), 171/173 (SS) rơi nhánh dự phòng về thứ tự mức nghiêm trọng (`results/T-016/giam-mau-hai-lan.md`)." Và ở mục 1 dòng TORAI, cột Kết luận: "**Khớp**" → "**Khớp số công bố** (xem T-016: lõi nhân quả gần như không đóng góp ở cấu hình này)".

## D4 — T-006: RCD torai-OB cửa sổ 20 chỉ 46/90 ca (mức: cập nhật, điểm mở 11.3)

- **Ở đâu:** `results/T-006/kiem-dung-dan.md:229` (mục 6, dòng torai-OB cửa sổ 20), `:56` (mục 2.1, "RCD: chưa phân xử được"), `:313` (mục 11.3).
- **Nay có số:** EC2, 1 lần, seed 0, đủ 90/90 ca trong 5 624 s: AVERAGE Avg@5 **0,742** (Bảng 2: 0,74), AC@1 0,644, AC@3 0,778. 46 ca chung: EC2 0,865, T-006 3 lần 0,839/0,896/0,835. 44 ca T-006 chưa chạy: 0,614. Tức 46 ca của T-006 không đại diện (T-006 đã cảnh báo đúng).
- **Bằng chứng:** `cham/s11-rcd-ob-len20.json`, `runs/s11-rcd-ob-len20-so-t006.txt`.
- **Kết luận bị ảnh hưởng:** mục 2.1 "RCD: chưa phân xử được": nay ở OB, cửa sổ 20 tái lập AVERAGE của bài (lệch +0,002, nhưng MEM lệch −0,197, DISK +0,110); ở SS, cả 10 (0,533) và 20 (0,664) vẫn không tái lập 0,57. Bằng chứng về cửa sổ của bài cho RCD vì vậy vẫn mâu thuẫn giữa hai dataset.
- **Đề xuất sửa:**
  - `:229`, cột 3–4: "**không so được với bài**: mỗi lần bị dừng ở 3 giờ (Q-40) với 46/90 ca" → giữ nguyên, thêm: "T-016 chạy đủ 90 ca trên EC2 (1 lần, seed 0): 0,742 (+0,002); 46 ca chung 0,865 so với 0,857 (TB 3 lần ở đây) (`results/T-016/diem-mo-t006.md`)."
  - `:56`: "Ở torai-OB, cửa sổ 20 chưa đủ ca (mục 6)." → "Ở torai-OB, cửa sổ 20 đủ 90 ca (T-016) cho 0,742 so với 0,74 của bài; nhưng torai-SS không khớp ở cả hai cửa sổ, nên vẫn chưa phân xử được cửa sổ của bài cho RCD."
  - `:313` (11.3): thêm "Đã làm ở T-016 (`results/T-016/diem-mo-t006.md`)."

## D5 — T-006: "Windows thay vì Linux" là nguyên nhân khả thi chưa kiểm (mức: cập nhật, điểm mở 11.5)

- **Ở đâu:** `results/T-006/kiem-dung-dan.md:248` (mục 6, nguyên nhân chưa kiểm), `:305` (mục 10), `:313-316` (mục 11.5).
- **Nay có số:** cùng seed, TORAI gốc, sửa × OB, SS cửa sổ 10: Linux và Windows cho thứ hạng giống hệt 90/90 ca mỗi cặp; RCD torai-SS cửa sổ 10: cũng giống hệt 90/90 ca (`diem-mo-t006.md` mục 2). 34 gói được nạp cùng phiên bản trên hai máy.
- **Kết luận bị ảnh hưởng:** "Windows thay vì Linux" không còn là nguyên nhân khả thi cho phần lệch của TORAI (và của RCD). CIRCA thuộc T-014, không kiểm ở đây.
- **Đề xuất sửa:** `:248` "- Windows thay vì Linux." → "- Windows thay vì Linux: đã loại cho TORAI và RCD ở T-016 (cùng seed, thứ hạng giống hệt; `results/T-016/diem-mo-t006.md`)."; `:305` thêm "(đã kiểm cho RCD, TORAI ở T-016; CIRCA chưa)".

## D6 — T-005: dùng ca `torai-TT` mà chưa chứng minh trùng ca dev (mức: thiếu, không đổi kết quả)

- **Ở đâu:** `tasks/T-005-do-kha-thi/LOG.md:37`, `results/T-005/moi-truong.md:111` — giải nén và chạy TORAI trên `torai-TT/ts-route-service_socket/1`, ghi là ca có trong `data/`, nhưng không có bằng chứng trùng với `re2tt_ts-route-service_socket_1` (zip `torai-TT` có cả ca test).
- **Bằng chứng nay:** trùng hệt (`runs/s0-cung-ca.json`: mốc tiêm = đầu file + 720 s; 540 375 ô, 0 ô lệch quá ngưỡng làm tròn). Không có rò dữ liệu test.
- **Kết luận bị ảnh hưởng:** không.
- **Đề xuất:** thêm một dòng vào `results/T-005/moi-truong.md` sau dòng 111: "Trùng ca dev `re2tt_ts-route-service_socket_1` đã được chứng minh ở T-016 (`results/T-016/runs/s0-cung-ca.json`)."

## Không thấy vấn đề

Đã rà và không thấy sai trong phạm vi TORAI/RCD: T-001 mục 4 (đường nhãn: `torai` không đọc `service`, `fault_type`, `case`), mục 3a dòng 4 (RCD), mục 8.1 (bảng biến thể RCD); T-005 dòng TORAI (`do-kha-thi.md:42`, đúng về giảm mẫu); T-006 mục 2.4 (không đọc `sli`), mục 6 (RCD không bọc `@rca`, không seed), mục 7 (số TORAI 0,913 / 0,951 trùng lượt có seed ở T-016). T-002, T-003, T-007–T-012 không có khẳng định về TORAI/RCD cần kiểm ở đây.
