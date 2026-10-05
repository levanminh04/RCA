# Nhật ký T-021

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối, không sửa mục cũ. Mỗi phiên một mục. Mục phải đủ để một agent khác, trên máy khác, không có lịch sử chat, làm tiếp được.

---

## Phiên 1 — 05/10/2026 — Claude (Opus 5.5) — Windows 11 laptop — vai trò: người làm

**Mở phiên:** đã đọc AGENTS, STATE, SPEC. LOG chưa có trước phiên này (file tạo ở phiên này). `results/T-021/` chưa có, nên không có đầu ra phiên trước cần kiểm.

Lời giao của Minh (prompt mở phiên): làm Bước 0 trước; có vấn đề ảnh hưởng tính đúng hoặc phạm vi thì dừng, ghi LOG, báo Minh, chờ quyết; không tự sửa SPEC, không làm bước 1. Không coi SPEC, REVIEW T-020, phản hồi của Codex hay đầu ra T-020 là đáp án.

**Đã đọc cho Bước 0:** MRP (toàn bộ); DECISIONS Q-10…Q-60 (gồm phần chưa commit Q-58–Q-60); WHY-03, 04, 05, 16, 19, 20, 21; LESSONS; DT18; advisor-2026-09-23; REVIEW T-020 (gồm bảng phản hồi); LOG T-020 phiên 2–3; K2 §1–2. Kiểm trên file: `results/T-020/scripts/chia_theo_o.py` (seed), `results/T-020/chia-theo-o/A-da-tin-hieu.csv` (ô dev RE2-TT), `results/T-009/runs/inspect-004/root-degree-whole-file.json`, `results/T-008/runs/evidence-002/summary.json` (root_windows), `results/T-020/trung-gian/dataset_evidence/root-mapping.csv`, `results/T-018/de-xuat-tai-lieu-chung.md` (E2).

**Khai báo neo:** trong lúc soát SPEC tôi đã đọc REVIEW T-020 và WHY-21, có số của từng bộ (RE2-TT 5 root, Eadro-TT 27 root…). Vì vậy yêu cầu bước 1 "lập bảng nhu cầu trước khi xem lại số" không còn giữ được trọn vẹn với tôi. Bảng nhu cầu ở bước 1 vẫn sẽ chỉ dẫn MRP, không dẫn số của bộ nào.

### Tự soát SPEC

Kết luận: **có vấn đề ảnh hưởng tính đúng và phạm vi. Dừng, chưa làm bước 1.** Mức "CHẶN" dưới đây nghĩa là làm theo SPEC hiện tại sẽ ra kết quả sai, thiếu so với MRP, hoặc dẫn hướng đáp án.

**S1 — CHẶN. Định nghĩa vị trí Q-60(b) không tính được từ dữ liệu đã lưu, và chưa có quy tắc lá/giữa/hub.**
- Ở đâu: SPEC Đầu ra 3; Các bước 3; Kiểm đúng đắn dòng 2; Không làm dòng 1.
- Sai gì: Q-60(b) định nghĩa vị trí theo "đồ thị gọi từ trace **lúc bình thường**". SPEC cấm đọc dữ liệu đo mới, nên chỉ dùng được file bậc đã lưu. Không file nào là đồ thị lúc bình thường. SPEC cũng bắt gán nhóm "lá, giữa, hub" nhưng không ai định nghĩa ngưỡng. Q-60(b) chỉ nói "theo bậc vào/ra".
- Bằng chứng:
  - Eadro: `results/T-009/runs/inspect-004/root-degree-whole-file.json`, trường `scope` = "whole-file raw graph … not injection time graph". Toàn file gồm cả đoạn tiêm lỗi.
  - Nezha: `results/T-008/runs/evidence-002/summary.json` root_windows, `scope` = "Whole minute files overlapping injection +/-60s". Đây là đồ thị quanh lúc tiêm, không phải lúc bình thường. Có thêm hai giả thuyết đồng hồ.
  - RE2-TT: `results/T-020/trung-gian/dataset_evidence/root-mapping.csv` ghi "graph quan sát" theo từng ca; chưa rõ cửa sổ.
  - Định nghĩa còn mơ hồ ngay trong tài liệu đã duyệt: K2 ST3 (`docs/knowledge/K2-du-lieu.md`) gọi route và train là "không phải lá" dù chúng không gọi service nào (bậc ra 0). Theo nghĩa đồ thị thông thường, bậc ra 0 là lá.
- Đề xuất sửa (Minh chọn):
  - (a) Cho phép dùng bậc đã lưu làm xấp xỉ, ghi rõ từng bộ dùng đồ thị nào và lệch Q-60(b) ở đâu. Không đọc dữ liệu mới. Rẻ, nhưng vị trí có thể bị chính sự cố làm méo.
  - (b) Cho phép đọc trace phần trước mốc tiêm của các bộ dev/TX1 (đã có trên máy), chỉ để dựng đồ thị bình thường. Đúng Q-60(b), nhưng là đọc dữ liệu đo mới; cần sửa mục "Không làm" và ước lượng thời gian trước.
  - Về lá/giữa/hub: tôi đề xuất một quy tắc kèm phép thử độ nhạy (ví dụ lá: vào > 0, ra = 0; giữa: vào > 0, ra > 0; hub: tổng bậc thuộc nhóm cao nhất của chính đồ thị đó; nguồn: vào = 0, ra > 0; bậc 0; không có trong trace). Minh duyệt quy tắc trước khi tôi gán nhóm. Nếu Minh muốn, tôi chỉ trình bậc thô và không gán nhóm.

**S2 — CHẶN. Assert "RE2-TT giữ 30 dev / 60 test" quyết trước vai trò của RE2-TT, trước bước chọn gói.**
- Ở đâu: SPEC Các bước 5.
- Sai gì: bước 4 mới chọn gói. Assert ở bước 5 đã buộc RE2-TT có mặt và buộc 60 ca làm test. Đây đúng là khuyến nghị của T-020 (`results/T-020/g1-goi-quyet-dinh.md:5` "giữ RE2-TT 30 dev/60 test"). MRP §4:120 chỉ nói 60 ca "có thể dùng làm test **nếu P2 chọn RE2-TT**". Lời giao của Minh cũng nói không có dataset hay cách chia nào định sẵn.
- Bằng chứng: SPEC dòng 59; `docs/MRP.md:120`; g1 T-020 dòng 5.
- Đề xuất sửa: đổi assert thành điều kiện: "nếu gói có RE2-TT thì 30 ca TX2 (10 ô dev của v1) nằm ở dev; vai trò của 60 ca còn lại theo bước 4". Ghi chú: tôi đã kiểm, 10 ô dev v1 phủ đủ 6 loại lỗi (cpu 2, delay 2, disk 2, loss 2, mem 1, socket 1 ô; từ `results/T-020/chia-theo-o/A-da-tin-hieu.csv`). Nên phiên bản phân tầng theo loại lỗi không xung đột với 10 ô này.

**S3 — CHẶN. Phạm vi RQ quá hẹp: bỏ RQ2 (P4) và RQ4 (P8).**
- Ở đâu: SPEC Mục tiêu ("RQ1, khả năng đánh giá RQ3a–d"); Các bước 1 (nguồn: MRP §3, §4, P3, P7).
- Sai gì: cách chia quyết P4 được thấy gì, vì P4 "chỉ dùng phần dev" (MRP P4). Nhu cầu của RQ2 gồm: dev có đủ loại lỗi, có ca root không có tín hiệu hoặc không có cạnh (giả thuyết thứ ba của P4), có lỗi mã nguồn. Đây chính là chỗ R4 của T-020 nêu. RQ4 cần log và bằng chứng có cấu trúc cho P8. Bỏ hai RQ này thì bảng nhu cầu thiếu đúng phần quyết định cách chia.
- Bằng chứng: `docs/MRP.md` §3 (RQ2, RQ4), P4 (dòng 169–179), P8.
- Đề xuất sửa: mục tiêu ghi RQ1–RQ4 (RQ5 thuộc FlashTicket, ngoài phạm vi); bước 1 thêm P4 và P8 vào nguồn.

**S4 — CHẶN. Thiếu các nội dung MRP bắt buộc ở G1; và đề nghị dời cửa sổ/ngân sách nhãn sang P3 mà không nêu xung đột với MRP.**
- Ở đâu: SPEC Đầu ra 1.
- Sai gì, bằng chứng:
  - MRP §4:119 bắt G1 ghi cách dùng nhãn (nhãn học, nhãn dev chọn cấu hình, nhãn chỉ chấm) và "baseline nào chạy được trên dataset giữ ngoài với đúng đầu vào và ngân sách nhãn". SPEC không yêu cầu cả hai. R3 của T-020 cũng nêu phần thứ hai.
  - MRP §7: ở mỗi cổng agent trả lời sáu câu. SPEC không yêu cầu.
  - MRP §4:111 (Q-31): nếu chọn bộ RCAEval phải chỉ ra nó hơn ứng viên khác ở tiêu chí nào. SPEC không yêu cầu.
  - SPEC cho Minh chọn "quyết ngay ở G1 hay chuyển xuống đầu P3" cho cửa sổ và ngân sách nhãn. MRP §4:118–119 và Q-54 đặt việc này ở G1. Minh có quyền đổi, nhưng thẻ phải nói rõ là đổi MRP/Q-54. Thêm nữa, độ dài cửa sổ quyết bộ nào đủ dữ liệu bình thường, nên có thể đổi chính lựa chọn dataset.
- Đề xuất sửa: thêm bốn mục trên vào Đầu ra 1; câu hỏi dời sang P3 ghi rõ nó sửa MRP §4/Q-54 và hệ quả cho lựa chọn dataset.

**S5 — CHẶN. Tiêu chí 3, 4, 8 của MRP §4 không nằm ở lớp nào.**
- Ở đâu: SPEC Đầu ra 1 ("bảng phủ … theo tiêu chí 5, 6, 7, 9"), Đầu ra 2.
- Sai gì: Q-58 có lớp 1 (tải được, quyền, nhãn root, thời điểm, tín hiệu phương pháp cần) và lớp 2 (5, 6, 7, 9). Tiêu chí 3 và 4 có thể hiểu là gộp vào "tín hiệu phương pháp cần". Nhưng tiêu chí 3 của MRP còn một điều kiện riêng: bộ không có trace chỉ dùng có chủ đích, làm kịch bản đồ thị từ kiến trúc. Tiêu chí 8 (đủ dữ liệu bình thường) không có ở lớp nào. Trong khi RQ3a và phần chấm phát hiện ở P3 (báo động sai mỗi giờ bình thường) cần nó. SPEC lại xếp "chất lượng dữ liệu bình thường" vào OPEN.
- Bằng chứng: `docs/DECISIONS.md` Q-58; `docs/MRP.md:93, 100, 162`.
- Đề xuất: Minh cho biết tiêu chí 8 xét ở lớp nào (đề xuất của tôi: lớp 2, cho cả gói, vì nó chỉ cần cho phát hiện và một số phương pháp); và giữ điều kiện "bộ không trace chỉ dùng có chủ đích" của tiêu chí 3. Tôi không tự gán.

**S6 — CHẶN nhẹ (sửa nhanh). Kiểm census bằng file phái sinh của T-020, trái yêu cầu kiểm từ nguồn gốc.**
- Ở đâu: SPEC Các bước 2 ("kiểm bằng: đếm lại census từ `public-census.csv`").
- Sai gì: `public-census.csv` là file T-020 tự dựng, chính sổ này đã ghi sai tiếp xúc (R1). SPEC dòng 92 và lời giao của Minh đòi số giữ/loại phải kiểm từ file kết quả gốc.
- Đề xuất: đếm lại từ thẻ và kết quả gốc (T-002, T-008, T-009, T-010, T-011, T-019 …); `public-census.csv` chỉ để đối chiếu. Mức TX không lấy từ sổ T-020.

**S7 — CHẶN nhẹ (sửa nhanh). SPEC nói "seed ghi trong SPEC này" nhưng không có seed.**
- Ở đâu: Đầu ra 6.
- Bằng chứng: không có giá trị seed nào trong SPEC. T-020 dùng `SEED = '20261004'` (`results/T-020/scripts/chia_theo_o.py:11`).
- Đề xuất: Minh chọn: dùng lại 20261004 (so được với T-020), hoặc một seed mới. Tôi đề xuất dùng lại 20261004, vì seed không mang thông tin gì về kết quả và giữ được so sánh.

**Không chặn:**
- K1. Đầu ra 1 chỉ nối WHY-05, 19, 20. WHY-04 (chia theo ô, giữ ngoài) và WHY-16 (cửa sổ tham chiếu) cũng đang "Đề xuất (G1)" (`docs/WHY.md:38, 137`). Nên thêm vào bảng giữ/sửa/thay.
- K2. R5 của T-020: BOCPD theo số đo vượt Q-40 trên Train Ticket (`results/T-005/do-kha-thi.md:49`, 1.440 s/ca). Việc này quyết RQ3a có baseline BOCPD trên TT hay không. Mục "Không làm" cho sửa khi lỗi "đổi lựa chọn G1"; đề xuất ghi rõ R5 thuộc diện này.
- K3. STATE ghi T-020 "chờ phản biện", nhưng LOG T-020 cho thấy đã phản biện và đã phản hồi (phiên 2–3), cột "Minh quyết" còn trống. SPEC không nói quan hệ T-020 và T-021: T-021 thay gói G1 của T-020, còn T-020 đóng thế nào. Theo AGENTS mục 6, đây là chỗ STATE lệch LOG, cần Minh xác nhận.
- K4. "≤ khoảng 5 trang" với ít nhất bảy bảng bắt buộc có thể không vừa. Đề xuất: chi tiết nằm trong các CSV, `goi-g1.md` chỉ trích dòng cần quyết.

**Điểm đã kiểm và thấy đúng:**
- 60 ca RE2-TT là TX1: khớp `docs/MRP.md:120` và `docs/knowledge/K2-du-lieu.md` dòng 15, 17 (v1 đọc schema và độ phủ trace của cả 90 ca). Đúng với Q-60(a).
- Phạm vi ghi không chồng lên task cũ hay docs chung.
- Yêu cầu trả lời riêng Sock Shop và LEMMA-RCA đúng MRP §4:87.
- Không chọn theo kết quả phương pháp (Q-33, QT4): đúng.

**Quyết định của Minh trong phiên:** chưa có. Chờ Minh quyết S1–S7 và K1–K4.

**Kết thúc lượt (dừng ở Bước 0):**
1. Đã làm gì: tự soát SPEC; kiểm bảy điểm nghi trên file gốc.
2. File đã thay đổi: tạo `tasks/T-021-goi-g1-thu-gon/LOG.md` (file này). Cập nhật dòng T-021 trong `docs/STATE.md`. Không sửa SPEC.
3. Kiểm tra đã chạy: đọc trường `scope` của hai file bậc; đếm ô dev RE2-TT theo loại lỗi; tìm seed trong SPEC và trong script T-020. Không đọc `data/locked/`, không đọc dữ liệu đo.
4. Cần Minh quyết: S1 (cách tính vị trí và quy tắc lá/giữa/hub), S2, S3, S4, S5 (tiêu chí 8 và 3), S6, S7 (seed), K3 (quan hệ T-020/T-021).
5. Bước tiếp theo chính xác: Minh trả lời S1–S7. Nếu Minh duyệt sửa SPEC, người làm sửa đúng các dòng đã nêu, ghi "Minh duyệt sửa SPEC ngày …" vào LOG, rồi làm bước 1 (bảng nhu cầu dữ liệu theo RQ từ MRP §3, §4, P3, P4, P7, P8, ghi vào LOG).
6. Lệnh cuối cùng đã chạy: `head -1 results/T-020/01-bang-tieu-chi-hop-nhat.csv; wc -l …` (chỉ đọc).

### Sửa SPEC theo tự soát — 05/10/2026

**Quyết định của Minh trong phiên** (nguyên lời):
- "đồng ý sửa giúp tôi các lỗi trên" — duyệt sửa SPEC theo S1–S7.
- Trả lời câu hỏi chọn: S1 đồ thị = "(a) Bậc đã lưu, ghi lệch"; quy tắc nhóm = "Quy tắc bậc + độ nhạy"; K1/K2/K4 = "Sửa cả ba".
- S5: theo đề xuất, tiêu chí 8 xét ở lớp gói; giữ điều kiện "bộ không trace chỉ dùng có chủ đích" của tiêu chí 3. Các quyết định này **chưa ghi vào DECISIONS** (ngoài phạm vi ghi); đề xuất dòng DECISIONS đã trình Minh trong chat.

**Đã sửa trong SPEC:** dòng Trạng thái (ghi lần duyệt sửa); Mục tiêu (RQ1–RQ4); Đầu ra 1 (sáu câu cổng, WHY-04/16, Q-40/BOCPD, tiêu chí 8 và 3, Q-31, cách dùng nhãn, baseline trên bộ giữ ngoài, hệ quả nếu dời sang P3, chi tiết để trong CSV); Đầu ra 3 (đồ thị (a) và quy tắc nhóm có độ nhạy); Đầu ra 6 (seed 20261004); Các bước 1, 2, 3, 5; Kiểm đúng đắn dòng vị trí; Không làm (R4–R6 thuộc diện đổi lựa chọn G1).

**Còn chờ Minh:** K3 (STATE ghi T-020 "chờ phản biện" trong khi LOG T-020 đã có phản hồi; T-020 đóng thế nào khi T-021 thay gói G1). Chưa làm bước 1.

**Kết thúc lượt:**
1. Đã làm gì: sửa SPEC theo S1–S7, K1, K2, K4.
2. File đã thay đổi: `tasks/T-021-goi-g1-thu-gon/SPEC.md`, LOG này, dòng T-021 trong `docs/STATE.md`.
3. Kiểm tra: đọc lại SPEC sau sửa.
4. Cần Minh: K3; duyệt dòng DECISIONS cho tiêu chí 8 và lựa chọn S1; cho phép bắt đầu bước 1.
5. Bước tiếp theo chính xác: khi Minh cho phép, làm bước 1: lập bảng nhu cầu dữ liệu theo RQ từ `docs/MRP.md` §3, §4, P3, P4, P7, P8, ghi vào LOG trước bước 2.
6. Lệnh cuối cùng đã chạy: ghi thêm mục này vào LOG.

---

## Phiên 2 — 05/10/2026 — Claude (Opus 5.5) — Windows 11 laptop — vai trò: người làm

**Mở phiên:** đã đọc AGENTS, STATE, SPEC (bản đã sửa theo S1–S7), LOG phiên 1. `results/T-021/` chưa có. Lời giao của Minh: làm lại Bước 0 độc lập trên SPEC hiện tại; có vấn đề về tính đúng hoặc phạm vi thì dừng, ghi LOG, báo Minh; không tự sửa SPEC, không làm bước 1.

**Đã đọc cho Bước 0:** MRP toàn bộ; DECISIONS (gồm Q-58–Q-60 chưa commit); WHY-03–05, 16, 19–21; LESSONS; K2 §1–2; K3 Q5, Q7; DT18; advisor-2026-09-23; REVIEW T-020 (gồm bảng phản hồi); SPEC T-020 (tiên nghiệm 2, 6); `docs/review-prompt.md` (có khối G1). Kiểm trên file: `results/T-009/runs/inspect-004/{root-degree-whole-file.json, root-positions.json}`, `results/T-008/runs/evidence-002/summary.json` (root_windows), `results/T-002/local-inspection/run-002/{cases.json, all-service-positions.csv, graph-degrees.csv}`, `results/T-020/01-bang-tieu-chi-hop-nhat.csv` (40 dòng), `results/T-012/final-leads.md`, `data/README.md`.

**Khai báo neo:** tôi đã đọc tự soát phiên 1 và WHY-21. Phần "Vì sao" của WHY-21 nêu sẵn ví dụ RE2-TT, Eadro-TT, RE3. Tôi coi đó là ví dụ, không phải gói đã chọn. Bảng nhu cầu ở bước 1 vẫn chỉ dẫn MRP.

### Tự soát SPEC (lần 2, trên SPEC đã sửa)

Kết luận: **còn vấn đề ảnh hưởng tính đúng và phạm vi. Dừng, chưa làm bước 1.** Các sửa S1–S7 đã có trong SPEC. Các điểm dưới đây là điểm mới.

**S8 — CHẶN. Quy tắc hub (phân vị 75 của mọi nút) không tính được cho Eadro và Nezha từ dữ liệu đã lưu.**
- Ở đâu: SPEC Đầu ra 3 (quy tắc nhóm); Các bước 3 ("tính lại bậc và nhóm từ file nguồn, cả hai ngưỡng hub").
- Sai gì: muốn biết root có phải hub không thì cần bậc của mọi nút trong đồ thị. Eadro và Nezha chỉ lưu bậc của root. SPEC lại cấm đọc dữ liệu đo mới. Phép kiểm của bước 3 không thể đạt.
- Bằng chứng:
  - Eadro: mỗi dòng của `results/T-009/runs/inspect-004/root-degree-whole-file.json` chỉ có các khóa dataset, session, root, fault, root_present, whole_file_in_degree, whole_file_out_degree, scope, alias_verified (117 dòng). `root-positions.json` cũng chỉ có bậc của root.
  - Nezha: mỗi dòng root_windows của `results/T-008/runs/evidence-002/summary.json` chỉ có in_neighbors, out_neighbors của root (202 dòng). Không có bậc của nút khác.
  - RE2-TT thì tính được: `results/T-002/local-inspection/run-002/all-service-positions.csv` có bậc của cả 27 service cho 30 ca dev.
- Đề xuất (Minh chọn):
  - (i) Với Eadro, Nezha: gán bậc 0, nguồn, lá, không có trong trace từ bậc của root; gộp "giữa hoặc hub" thành một nhóm; hub để OPEN. Không đọc dữ liệu mới. Mất: không tách được hub ở hai bộ này.
  - (ii) Cho phép đọc trace của Eadro, Nezha (đã TX1, có sẵn trên laptop) chỉ để dựng đồ thị đầy đủ. Mức TX không đổi. Sửa luôn được chỗ lệch Q-60(b) nếu lấy đoạn trước mốc tiêm. Nhưng đây là đọc dữ liệu đo mới, trái mục "Không làm"; thời gian chạy chưa ước lượng.
  - Tôi đề xuất (i) cho T-021, ghi hub của hai bộ thành giới hạn; dựng đồ thị đầy đủ để P5 làm (P5 phải dựng đồ thị cho mọi dataset).

**S9 — CHẶN nhẹ. Thiếu quy tắc gộp vị trí từ ca lên ô.**
- Ở đâu: SPEC Đầu ra 3 ("nhóm vị trí, số ô").
- Sai gì: bậc tính theo từng ca, nhưng bảng phải báo số ô mỗi nhóm. Một ô có thể rơi vào nhiều nhóm. SPEC không nói xử lý thế nào, nên người làm phải tự đặt quy tắc.
- Bằng chứng: Nezha có 24/101 sự kiện mà hai giả thuyết đồng hồ cho nhóm vị trí khác nhau (đếm trên root_windows của `evidence-002/summary.json`, khóa theo dataset, ngày, root, lỗi, mốc tiêm). RE2-TT có 2 đồ thị khác nhau trong 30 ca dev (LESSONS ST3).
- Đề xuất: báo theo ca; một ô có nhóm X khi mọi ca của nó cùng nhóm X, nếu không thì ghi "không ổn định"; Nezha báo riêng từng giả thuyết đồng hồ.

**S10 — CHẶN (sửa nhanh). Bộ giữ ngoài không còn điều kiện TX0.**
- Ở đâu: SPEC Các bước 5 (assert "không ca TX2 ở test hay giữ ngoài"); Đầu ra 5 (`tiep-xuc.csv` chỉ cho "các bộ được đề xuất").
- Sai gì: assert cho phép đặt một bộ TX1 làm giữ ngoài. MRP §4 yêu cầu bộ giữ ngoài "hoàn toàn ngoài thiết kế": trước G3 không xem dữ liệu đo. TX1 là đã xem thống kê dữ liệu đo. Q-60(a) chỉ cho TX1 vào **test**, không nói tới giữ ngoài. SPEC T-020 (tiên nghiệm 2) có câu "Giữ ngoài: chỉ TX0"; SPEC T-021 làm rơi câu này.
- Bằng chứng: `docs/MRP.md:117`; `docs/DECISIONS.md` Q-60(a); `tasks/T-020-tong-hop-g1/SPEC.md:24`.
- Đề xuất: assert thêm "mọi ca của bộ giữ ngoài là TX0"; `tiep-xuc.csv` ghi cả các ứng viên giữ ngoài.

**S11 — CHẶN nhẹ. SPEC cấm lấy mức TX từ sổ T-020 nhưng không nêu lấy từ đâu.**
- Ở đâu: SPEC Đầu vào; Các bước 2.
- Sai gì: R1 của T-020 sinh ra vì sổ tiếp xúc thiếu một nguồn (v1). SPEC chỉ liệt kê thẻ dataset (T-002, T-003, T-008–T-012, T-019) và hồ sơ T-013–T-018. TX2 đến từ các lượt chạy phương pháp, gồm cả T-005, T-006, T-007, không có trong Đầu vào. Không liệt kê nguồn thì lỗi kiểu R1 có thể lặp lại.
- Bằng chứng: T-020 ghi RE2-OB, RE2-SS TX2 = 90, BARO-FSE-OB TX2 = 100 (`results/T-020/01-bang-tieu-chi-hop-nhat.csv` cột exposure). Số này phải kiểm lại từ sổ chạy gốc, mà sổ chạy của T-005–T-007 không nằm trong Đầu vào.
- Đề xuất: ghi rõ ba nhóm nguồn TX: (1) v1: `docs/MRP.md:120`, K2 §1–2, LESSONS; (2) TX1 từ các task thẻ: T-002, T-003, T-008–T-012, T-019; (3) TX2 từ sổ chạy của T-005, T-006, T-007, T-013–T-018. Mỗi mức TX trỏ về một trong ba nhóm.

**S12 — CHẶN (phạm vi). Tập ứng viên bị bó vào 40 dòng của T-020; ít nhất ba bộ đã biết không có lý do loại ở đâu.**
- Ở đâu: SPEC Các bước 2 ("các ứng viên trong `01-bang-tieu-chi-hop-nhat.csv`"); Tiêu chí xong ("mọi bộ ứng viên của T-020").
- Sai gì: lời giao nói không có dataset nào định sẵn. Lấy đúng tập của T-020 là một bộ lọc có sẵn. Bảng của T-020 thiếu:
  - FAMOS TrainTicket: `results/T-012/final-leads.md:9` dặn "không tự bỏ khỏi cân nhắc G1". Không có trong 40 dòng.
  - GAIA/MicroSS (K3 Q5: có trace, Apache 2.0, 1.448 lần tiêm lỗi, nhóm tác giả khác RCAEval) và DejaVu (K3 Q7). Không task nào lập thẻ hay ghi lý do loại (grep `results/` và `tasks/`).
- Lưu ý: MRP §4 không liệt kê GAIA và DejaVu; lượt tìm 2025–2026 cũng không phủ chúng vì công bố sớm hơn. Như vậy chúng rơi ra ngoài mà chưa ai quyết.
- Đề xuất: bảng "đã xét, không dùng" phủ cả các bộ ở K3 và T-012 không có trong bảng T-020, mỗi bộ một câu lý do từ thông tin đã có, ghi "chưa kiểm trên file". Nếu một bộ trông đủ mạnh mà chỉ thiếu kiểm file, đưa thành câu hỏi cho Minh (tải hay không), không tự tải.

**Không chặn:**
- K5. RE2-TT có sẵn đồ thị **trước mốc tiêm** (`all-service-positions.csv`, cột window = pre_injection, 30 ca dev × 27 service). Đồ thị này gần Q-60(b) hơn mô tả "theo từng ca" của SPEC. Đề xuất: dùng pre_injection làm chính cho RE2-TT, báo kèm bản full.
- K6. Bảng phủ của gói không tách theo phía. RQ2 (P4) cần phủ ở dev; RQ3 cần phủ ở test hoặc giữ ngoài. Một gói có thể phủ đủ tiêu chí nhưng chỉ ở một phía (đúng chỗ R4 của T-020). Đề xuất: sau khi chia, báo loại lỗi và nhóm vị trí có ở dev, ở test; liệt kê cái vắng ở một phía.
- K7. Với tiêu chí chọn "gói nhỏ nhất", bộ có vị trí OPEN (TX0, chưa dò) dễ thua bộ đã dò, dù OPEN chỉ là chưa biết. Đây là một dạng "đã có sẵn" mà Q-31 cấm tính là lý do. Đề xuất: ghi rõ OPEN không tính là trượt; khi một bộ thua vì OPEN thì nói ra. Thêm nữa, "nhỏ nhất" là tiêu chí chi phí; phương án so sánh nên có một gói lớn hơn, kèm được/mất.
- K8. Các quyết định ngày 05/10 trong phiên 1 (tiêu chí 8 xét ở lớp gói; S1 chọn (a); quy tắc nhóm và độ nhạy) mới nằm trong SPEC và LOG, chưa có trong `docs/DECISIONS.md` (AGENTS mục 4). Cần Minh duyệt dòng ghi; file này ngoài phạm vi ghi của T-021.
- K3 (từ phiên 1) vẫn mở: STATE ghi T-020 "chờ phản biện", nhưng T-020 đã có REVIEW và phản hồi; cột "Minh quyết" còn trống.

**Về Q-58–Q-60:** ở Bước 0 tôi chưa thấy bằng chứng mâu thuẫn với ba quyết định. Một điểm cần biết: theo Q-60(a), tập test của Nezha, Eadro (nếu dùng) chứa ca đã dò triệu chứng theo từng ca, gắn nhãn root. Như vậy kết luận RQ3 về "nhầm triệu chứng với nguyên nhân" trên các ca này không còn mù hoàn toàn. Q-60 đã yêu cầu khai báo riêng; gói sẽ nêu ở phần giới hạn.

**Điểm đã kiểm và thấy đúng:** S1–S7, K1, K2, K4 của phiên 1 đã có trong SPEC (RQ1–RQ4; sáu câu cổng; cách dùng nhãn; baseline trên bộ giữ ngoài; Q-31; seed 20261004; assert RE2-TT có điều kiện; nguồn census gốc). Khối G1 có trong `docs/review-prompt.md`. Bảng 40 dòng của T-020 phủ các họ MRP §4 nêu tên và các bộ T-012 (trừ FAMOS).

**Quyết định của Minh trong phiên:** chưa có. Chờ Minh quyết S8–S12, K5–K8 và K3.

**Kết thúc lượt (dừng ở Bước 0):**
1. Đã làm gì: tự soát SPEC lần 2; kiểm trên file các điểm S8–S12, K5.
2. File đã thay đổi: `tasks/T-021-goi-g1-thu-gon/LOG.md` (mục này), dòng T-021 trong `docs/STATE.md`. Không sửa SPEC.
3. Kiểm tra đã chạy (chỉ đọc): liệt kê khóa của file bậc Eadro, Nezha; đếm sự kiện Nezha lệch nhóm giữa hai giả thuyết đồng hồ (24/101); đếm ca và nút trong đồ thị pre_injection RE2-TT (30 ca, 27 nút); liệt kê 40 dòng ứng viên T-020; grep FAMOS, GAIA, DejaVu trong `results/`, `tasks/`. Không đọc `data/locked/`, không đọc dữ liệu đo.
4. Cần Minh quyết: S8 (chọn (i) hay (ii)); S9 (quy tắc gộp); duyệt sửa SPEC theo S10, S11, S12; K5–K7 (sửa hay không); K8 (dòng DECISIONS); K3.
5. Bước tiếp theo chính xác: Minh trả lời. Nếu Minh duyệt sửa SPEC, người làm sửa đúng các dòng đã nêu, ghi "Minh duyệt sửa SPEC ngày …" vào LOG, rồi làm bước 1: lập bảng nhu cầu dữ liệu theo RQ từ `docs/MRP.md` §3, §4, P3, P4, P7, P8, ghi vào LOG trước bước 2.
6. Lệnh cuối cùng đã chạy: grep FAMOS/GAIA/DejaVu trong `results/`, `tasks/` (chỉ đọc).

### Sửa SPEC theo tự soát lần 2 — 05/10/2026

**Quyết định của Minh trong phiên** (nguyên lời): "đồng ý sửa SPEC theo đề xuất, S8 chọn (i)". Tôi hiểu "theo đề xuất" gồm mọi đề xuất sửa SPEC ở mục trên: S8 (i), S9, S10, S11, S12, K5, K6, K7. K8 (dòng DECISIONS) và K3 chưa được trả lời; chúng không nằm trong SPEC.

**Đã sửa trong SPEC:** dòng Trạng thái; Đầu vào (nguồn TX ba nhóm; tập ứng viên gồm cả bộ K3/T-012 T-020 thiếu; `all-service-positions.csv`); Đầu ra 1 mục Dataset (bảng "đã xét" phủ cả bộ ngoài T-020; bảng phủ theo phía; OPEN không tính trượt); Đầu ra 3 (RE2-TT dùng pre_injection; bộ chỉ có bậc root theo S8 (i); gộp ca lên ô); Đầu ra 5 (thêm ứng viên giữ ngoài, nguồn TX); Các bước 2, 3, 4, 5; Tiêu chí xong (tập ứng viên).

### Bước 1 — Bảng nhu cầu dữ liệu theo RQ (ghi trước bước 2; chỉ dẫn MRP)

| Mã | RQ / gói | Nhu cầu dữ liệu | Nguồn MRP |
|---|---|---|---|
| N1 | RQ1, P3 xếp hạng chế độ (a) | Mỗi ca có nhãn service gốc và thời điểm lỗi; có tín hiệu mà phương pháp Q-38 cần: metric (BARO, N-Sigma, CIRCA, RCD), trace có span cha–con (MicroRank, TraceRCA), metric + log (TORAI), đa nguồn (SimpleRCA) | §3 RQ1; §4 tc 2–4; P3 |
| N2 | RQ1 "giữa các dataset" | Ít nhất hai hệ hoặc hai bộ khác nhau | §3 RQ1; §0 |
| N3 | RQ1, RQ2 theo loại lỗi | Có lỗi tài nguyên, mạng, mã nguồn | §3 RQ1; §4 tc 6 |
| N4 | RQ1, RQ3d theo vị trí root | Nhiều root, ở nhiều nhóm vị trí | §3 RQ1; §4 tc 5; P7 báo theo vị trí |
| N5 | RQ1 phát hiện (Q-30), RQ3a | Đủ dữ liệu bình thường để học ngưỡng; nhãn thời gian ghi rõ là lúc tiêm hay onset; chế độ (b) cần mốc tiêm không lộ qua biên file; chấm báo động sai mỗi giờ bình thường | §4 tc 2, 8; P3; P7 độ đo |
| N6 | RQ2, P4 (chỉ dev) | Dev có đủ loại lỗi và vị trí; có lỗi mã nguồn ở dev (giả thuyết 2); có ca root không tín hiệu hoặc không cạnh (giả thuyết 3); có ca triệu chứng lan (giả thuyết 1, tc 7) | P4; §4 tc 7 |
| N7 | RQ3, P7 | Test không TX2; ít nhất một bộ giữ ngoài TX0; trace có span cha–con để ánh xạ lên đồ thị; đủ ô để bootstrap theo ô | §3 RQ3; §4 chia dữ liệu; §6 mục 1; P7 |
| N8 | RQ3c | Nhãn vùng ảnh hưởng. Công khai không có; chỉ báo "vùng nghi ngờ có chứa root" | P7; WHY-06 |
| N9 | RQ3d, P7 | Đồ thị quan sát có cấu trúc thật (để so với đồ thị ngẫu nhiên giữ bậc); biết kiến trúc để so đồ thị tĩnh với đồ thị quan sát | §3 RQ3d; §6 mục 3; P5, P7 |
| N10 | P5, P6 (ánh xạ) | Span có kind/thuộc tính để dựng cạnh có kiểu (gọi, thông điệp, dữ liệu); log có trace_id hoặc ít nhất service + thời gian | P5; P6 tầng 1 |
| N11 | RQ4, P8 | Log đọc được để lấy dòng tiêu biểu; nhãn root và loại lỗi để chấm "đúng" | §3 RQ4; P8 |
| N12 | tc 9 | Ít nhất một bộ độc lập theo Q-60(c) | §4 tc 9 |
| N13 | tc 1 | Quyền dùng theo Q-59 | §4 tc 1 |
| N14 | §4 cách dùng nhãn | Với bộ giữ ngoài: baseline nào chạy được với đúng đầu vào và ngân sách nhãn | §4 dòng 119 |
| N15 | P3 kiểm tái lập | Ít nhất một bộ có số công bố của tác giả để so | P3 |
| N16 | Q-40 | Mỗi phương pháp chạy hết một dataset trong 3 giờ | DECISIONS Q-40 |

### Tiến độ bước 2–5 (05/10/2026)

- Bước 2: `scripts/census.py` → `runs/census-001` (bản đầu, Nezha/Eadro tín hiệu ghi True theo thẻ) và `runs/census-002` (sửa: tín hiệu của Nezha/Eadro để trống, lấy theo thẻ ở mức bộ). Đối chiếu sổ T-020 ở `runs/census-002/doi-chieu-T020.csv`: khớp số ca và số ô ở 15 bộ; lệch TX ở hai bộ: RE2-TT (60 ca TX1, T-020 ghi TX0; đúng R1) và **RE1-OB** (TX2 cả 125 ca, T-020 ghi 124 TX0 + 1 TX1). Nguồn RE1-OB: `results/T-006/runs/kiem-chay-fse-baro-main-re1-ob.tar.gz` có 125 file kết quả của `main.py` trên bản Zenodo của RE1-OB; `results/T-006/kiem-dung-dan.md:60-66`. Bản HF chưa đối chiếu byte với bản Zenodo, nên ghi TX2 thận trọng.
- Bước 3: `scripts/vi_tri.py` → `runs/vi-tri-001` (theo ca, theo ô, tóm tắt). Nezha lệch nhóm giữa hai đồng hồ: 24/101 sự kiện. `scripts/build_bang.py` → `dieu-kien-toi-thieu.csv`, `doc-lap.csv`, `tiep-xuc.csv`, `vi-tri-root.csv`.
- Bước 5: `scripts/chia.py` → `runs/chia-001` (lỗi: ô test RE2-TT ghi OPEN thay vì suy theo root), `runs/chia-002` (sửa), `runs/chia-003` (xếp socket vào nhóm tài nguyên theo `results/T-002/the-rcaeval.md:17`). Bản dùng: chia-003 và `chia-theo-o/{A,B}-{ty-le,phan-tang}.csv`. Mọi assert đạt.
- Phát hiện khi chia: ở Eadro, Nezha nhiều lần tiêm nằm trong cùng một file phiên/ngày; chia theo ô làm 29–30 cặp ca liền kề nằm khác phía (Eadro-TT nghỉ 114–124 s giữa hai lần tiêm). `scripts/kiem_phien.py` → `runs/kiem-phien-001`: lần tiêm đầu của mỗi phiên Eadro chỉ cách đầu phiên 2,5–4,2 s. Ghi thành câu hỏi cho Minh trong `goi-g1.md`, không tự đổi đơn vị chia.

### Bước 4, 6 và tự kiểm (05/10/2026)

- Bước 4: chọn gói A (RE2-TT, Eadro-TT, Nezha-OB chia; RE3-OB giữ ngoài); so với B (lớn hơn) và C (nhỏ hơn); lập luận mạnh nhất chống A và điều làm đổi ý ghi ở `results/T-021/goi-g1.md` mục 0, 3.6. Không dùng kết quả phương pháp đã chạy để chọn.
- Bước 6: `results/T-021/goi-g1.md` (khoảng 3.600 từ kể cả bảng và đường dẫn), `results/T-021/de-xuat-tai-lieu-chung.md` (E1 dòng DECISIONS cho K8, E2 WHY-04, E3 ghi chú sổ T-020).
- Tự kiểm:
  - Census tính từ cây file HF (T-002) khớp census riêng của T-019 cho RE1-SS 125/5/25, RE2-SS 90/5/30, RE3-SS 30/3/9; Nezha 56 + 23... ô khớp `results/T-008/runs/run-001/cells.json` (56 ô = 33 + 23); Eadro 117 ô = 36 + 81 khớp `results/T-009/runs/run-001/cells.json`; Bank 136/14/52 khớp `results/T-012/runs/bank-label-reproduce-002/census.json`.
  - Vị trí 5 root RE2-TT (auth bậc 0; route, train lá; order giữa/hub; travel hub) khớp mô tả LESSONS ST3 (`docs/knowledge/K2-du-lieu.md` ST3), trừ cách gọi "không phải lá" của ST3 với route, train (quy tắc Minh duyệt xếp bậc ra 0 là lá).
  - Mọi script chỉ đọc `results/`; grep không có đường đọc `data/locked/`.
  - `git status`: chỉ có `results/T-021/`, `tasks/T-021-goi-g1-thu-gon/` và dòng T-021 trong STATE thay đổi trong phiên này (DECISIONS, WHY, T-020 là thay đổi có từ trước phiên).
- Điều cần biết: các CSV `chia-theo-o/*.csv` của lượt chia-001, chia-002 bị lượt chia-003 ghi đè (cùng tên file); báo cáo JSON và stdout của cả ba lượt vẫn giữ trong `runs/`. Trong `bao-cao-chia.json`, mục `vang_mot_phia` của RE2-TT liệt kê nhóm vị trí "vắng một phía" chỉ vì nhãn test có hậu tố "(suy theo root, chưa kiểm)"; không phải vắng thật.

### Kết thúc phiên 2

1. **Đã làm:** tự soát SPEC lần 2; sửa SPEC theo duyệt; bước 1–6.
2. **File đã thay đổi:** `tasks/T-021-goi-g1-thu-gon/SPEC.md`, LOG này, dòng T-021 trong `docs/STATE.md`, toàn bộ `results/T-021/` (goi-g1.md, 4 CSV chính, de-xuat-tai-lieu-chung.md, chia-theo-o/4 CSV, scripts/ 6 file, runs/ 7 lượt).
3. **Kiểm tra đã chạy:** assert của `scripts/chia.py` đạt ở 4 bản (mỗi ô một phía; không TX2 ở test/giữ ngoài; giữ ngoài toàn TX0; tổng khớp census; RE2-TT 10 ô/30 ca TX2 ở dev); đối chiếu census với T-019, T-008, T-009, T-012 như trên.
4. **Cần Minh quyết:** 6 câu hỏi ở `goi-g1.md` mục 6 (đơn vị chia Eadro/Nezha; cửa sổ; Retrieval@K; mốc tiêm ở chế độ (a); CIRCA-PC và BOCPD so với Q-40; gói A/B và bộ giữ ngoài); E1–E3 ở `de-xuat-tai-lieu-chung.md`; K3 (trạng thái T-020). Tôi hiểu lời duyệt "theo đề xuất" gồm cả K5–K7; nếu sai, cần hoàn tác các dòng K5–K7 trong SPEC.
5. **Bước tiếp theo chính xác:** Minh mở phiên Codex phản biện, dán prompt dưới. Sau REVIEW, người làm phản hồi theo `docs/review-prompt.md` mục "Prompt cho người làm phản hồi phản biện".
6. **Lệnh cuối cùng đã chạy:** `git status --short` (chỉ đọc).

### Prompt phản biện cho Codex

```text
Bạn là người phản biện độc lập cho task T-021 của repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Bạn chỉ được ghi đúng một file: tasks/T-021-goi-g1-thu-gon/REVIEW.md, theo mẫu tasks/_MAU/REVIEW.md.
Không sửa file nào khác, không commit.

Đọc: tasks/T-021-goi-g1-thu-gon/SPEC.md, tasks/T-021-goi-g1-thu-gon/LOG.md, các file đầu ra: results/T-021/goi-g1.md, results/T-021/dieu-kien-toi-thieu.csv, results/T-021/vi-tri-root.csv, results/T-021/doc-lap.csv, results/T-021/tiep-xuc.csv, results/T-021/chia-theo-o/*.csv, results/T-021/scripts/*.py, results/T-021/runs/, results/T-021/de-xuat-tai-lieu-chung.md,
và kết quả `git diff 5636b69` nếu có. Script chạy bằng `py -3 -X utf8 results/T-021/scripts/<tên>.py --run <run-id mới>` (build_bang.py không cần --run).
Nguồn đối chiếu đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: mức CHẶN hoặc KHÔNG CHẶN; ở đâu; sai gì; bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); đề xuất sửa ngắn.
Tiếng Việt, câu ngắn.

Danh sách phương pháp có phủ đủ các họ không; hồ sơ kỹ thuật có đúng với bài và code gốc không
(kiểm ngẫu nhiên ít nhất 2 phương pháp); dataset đã chọn có phân xử được RQ1, RQ3 không;
cách chia dev/test có lộ đáp án không; có đường nào để nhãn lọt vào phương pháp không.
```

## Phiên 3 — 05/10/2026 — Claude (Opus 5.5) — Windows 11 laptop — vai trò: người làm (bước 7, phản hồi phản biện)

### Tự soát độc lập (ghi TRƯỚC khi mở REVIEW.md)

Đọc lại SPEC, LOG, `goi-g1.md`, các CSV và `runs/` trên file thật. Điểm tự tìm:

- **N1 (CHẶN đề xuất)** — Vị trí root Eadro-TT dựa trên đồ thị trace toàn file mà thẻ T-009 cảnh báo không được diễn giải: trace có timestamp lịch sử, lệch biểu kiến với metric/nhãn; "không được diễn giải bậc 0 là cô lập" (`results/T-009/the-dataset.md:95`, `:282`). `goi-g1.md` mục 0 và 3.1 (N4, N6) vẫn dùng "27 root ở 5 nhóm vị trí", "27 ô root không có trong trace", "7 ca bậc 0" làm lý do chính chọn Eadro-TT và làm dữ liệu cho giả thuyết 3 của P4. Nguyên nhân khác chưa loại (Q-33): tải sinh ra không gọi các service đó trong đoạn trace được export; export trace không khớp phiên. Dấu hiệu: `vi-tri-root.csv` xếp ts-travel-service là "nguồn" (bậc vào 0) và ts-user-service, ts-payment-service, ts-seat-service, ts-travel-plan-service là "không có trong trace" — trái với cấu trúc gọi thường thấy của Train Ticket. Mục 5 có nêu lệch "toàn file", nhưng không nêu cảnh báo diễn giải của T-009.
- **N2 (KHÔNG CHẶN)** — Bộ giữ ngoài RE3-OB trùng hệ (OB) với Nezha-OB ở dev và trùng bộ công cụ (RCAEval) với RE2-TT ở dev. Mục 5 chỉ nói "kiểm có khớp riêng Train Ticket không"; thực ra cấu hình chọn trên dev đã thấy cả OB lẫn bộ công cụ RCAEval, nên RE3-OB không kiểm riêng được trục nào. Câu "hệ không có trong dev của họ RCAEval" (mục 0) đúng chữ nhưng dễ đọc thành "hệ mới".
- **N3 (KHÔNG CHẶN)** — Câu 1 mục 6 và mục 6 câu 2 gọi khoảng giữa hai lần tiêm Nezha là "nghỉ ≈ 8,5 phút". Nezha không ghi thời lượng tiêm (`runs/kiem-phien-001/ket-qua.json`, ghi_chu), nên đó là khoảng giữa hai mốc tiêm, không phải thời gian nghỉ. Đề xuất (a) cho Nezha và cửa sổ "trước mốc tối đa 300 s" dựa trên giả định lỗi trước đã hết; chưa kiểm.
- **N4 (KHÔNG CHẶN)** — Mục 3.1 N6 "11 ca Eadro root không có trong trace, 7 ca bậc 0" mơ hồ: theo `chia-theo-o/A-phan-tang.csv`, dev Eadro-TT có 11 ca "không có trong trace" nhưng chỉ 1 ca bậc 0; 7 là cộng cả 6 ca auth của RE2-TT. Cần ghi tách theo bộ.
- **N5 (KHÔNG CHẶN)** — Mục 3.5 dòng "RE2-OB, RE2-SS, RE1-OB, RE1-SS (100 ca)": số 100 không khớp tổng nào (90 + 90 + 125 + 125); RE1-SS còn 25 ca TX1, không "TX2" toàn bộ (`tiep-xuc.csv`). BARO-FSE-OB có trong `dieu-kien-toi-thieu.csv` nhưng không có dòng ở bảng 3.5 (tiêu chí xong vẫn đạt nhờ CSV).
- **N6 (KHÔNG CHẶN)** — RE3-OB TX0 dựa trên "không thấy nguồn tiếp xúc trong ba nhóm" (`tiep-xuc.csv`): là vắng bằng chứng, không phải bằng chứng vắng. Nên ghi rõ thế trong gói, vì đây là điều kiện giữ ngoài.

Kiểm đã chạy (chỉ đọc): đếm vị trí theo phía từ `chia-theo-o/A-phan-tang.csv`; đọc `results/T-009/runs/inspect-004/root-degree-whole-file.json`, `results/T-009/the-dataset.md`; nhân lại các phép chiếu Q-40 ở mục 2 (khớp: 44,9 h; 36 h; 5,95 h / 2,5 h; 73,5 phút).

(Ghi chú: trong bảng REVIEW.md, N3 tự soát ở trên được gộp vào ý kiến R1; các điểm tự soát N4, N5, N6 ở trên được đánh lại số thành N3, N4, N5 trong REVIEW.md.)

### Đánh giá phản biện (sau khi mở REVIEW.md)

- R1 đúng, CHẶN. Kiểm `results/T-008/the-dataset.md:72-80`: trace/log Nezha chỉ có quanh mốc tiêm. Rộng hơn N3 tự soát.
- R2 đúng. Đếm lại labels OB: 23/33 ô, 46/56 ca có ở cả hai ngày.
- R3 đúng một phần: thiếu bản TraceRCA và các lựa chọn CANDIDATE của T-014/T-015; nhưng SPEC không đòi chốt scorer ở G1.
- R4 đúng: TraceRCA, MicroRCA data vắng; GAIA cần thành câu hỏi cho Minh theo S12.
- Chi tiết và lý do: bảng cuối `REVIEW.md`.

### Đề xuất sửa (chờ Minh duyệt; chưa sửa)

`results/T-021/goi-g1.md`:
- R1: mục 0, 3.1 (N5), 5, câu 1 và câu 2 mục 6: đổi "nghỉ" thành "khoảng giữa hai mốc tiêm"; thêm giới hạn: trace/log Nezha chỉ có phút tiêm +2, chọn theo nhãn, nên chỉ hợp ranking biết trước cửa sổ, không hợp phát hiện liên tục; cửa sổ trước mốc cho Nezha chỉ có metric ngày (normal, clock OPEN).
- R2: câu 1 phương án (b): bỏ "không rò"; nêu chia theo ngày đưa 23/33 ô, 46/56 ca sang hai phía.
- R3: mục 2: ghi rõ bản TraceRCA (nguyên trạng là bản tái lập; bản lọc finite-before-sort là baseline, CANDIDATE); thêm bảng ngắn "OPEN, quyết trước khi chạy P3": scorer CIRCA, full-score/mapping MicroRank, policy TraceRCA, trỏ `results/T-014/de-xuat-tai-lieu-chung.md`, `results/T-015/de-xuat-tai-lieu-chung.md`.
- R4: bảng 3.5: thêm dòng dữ liệu TraceRCA, MicroRCA, BARO-FSE-OB; sửa dòng GAIA; mục 6 thêm câu hỏi "kiểm file GAIA hay không" (dung lượng phải trình trước nếu chọn tải).
- N1: mục 0, 3.1 (N4, N6), 5: cảnh báo đồ thị trace Eadro theo `results/T-009/the-dataset.md:95`; thêm vào "điều làm đề xuất đổi".
- N2: mục 5: RE3-OB không kiểm riêng trục hệ hay trục bộ công cụ.
- N3: mục 3.1 N6: tách số theo bộ.
- N4: mục 3.5: sửa "(100 ca)" và TX RE1-SS.
- N5: mục 4 hoặc 5: ghi TX0 của RE3-OB là "không thấy nguồn tiếp xúc".

`results/T-021/dieu-kien-toi-thieu.csv`: R4 — thêm dòng TraceRCA data, MicroRCA data (sửa qua `scripts/build_bang.py` rồi chạy lại).

`results/T-021/de-xuat-tai-lieu-chung.md`: R3 — nếu Minh muốn ghi WHY cho policy TraceRCA, trỏ nháp có sẵn ở T-015.

Không cần chạy lại census, vị trí, chia: không điểm nào đổi bốn CSV chia.

### Kết thúc phiên 3

1. **Đã làm:** tự soát độc lập (ghi trước khi mở REVIEW); kiểm lại bằng chứng R1–R4; điền bảng phản hồi.
2. **File đã thay đổi:** `tasks/T-021-goi-g1-thu-gon/REVIEW.md` (chỉ bảng cuối), LOG này, dòng T-021 trong `docs/STATE.md`.
3. **Kiểm tra đã chạy (chỉ đọc):** đếm vị trí theo phía từ `chia-theo-o/A-phan-tang.csv`; đếm ô OB theo ngày từ `results/T-008/runs/run-001/labels.json` (23/33, 46/56); đọc `results/T-008/the-dataset.md:72-80`, `results/T-009/the-dataset.md:95`, K3:210-216, T-014/T-015 đề xuất; nhân lại phép chiếu Q-40 (khớp).
4. **Cần Minh quyết:** cột "Minh quyết" cho R1–R4, N1–N5; duyệt danh sách đề xuất sửa trên.
5. **Bước tiếp theo:** Minh duyệt điểm nào sửa → người làm sửa `goi-g1.md` (và `build_bang.py` nếu R4), ghi LOG.
6. **Lệnh cuối cùng đã chạy:** script Python ghi bảng phản hồi vào REVIEW.md.

## Phiên 3 (tiếp) — sửa theo phản biện

- Minh duyệt ngày 05/10/2026: "duyệt sửa R1–R4 và N1–N5 theo đề xuất" (phạm vi: danh sách "Đề xuất sửa" của phiên 3).
- Sửa `results/T-021/goi-g1.md`:
  - R1: mục 0 (RQ3a), 3.1 (N5), 5, câu 1, câu 2 về trace/log Nezha.
  - R2: câu 1 phương án (b).
  - R3: tách dòng TraceRCA trong bảng mục 2; thêm bảng "Còn mở, phải quyết trước khi chạy P3".
  - R4: bảng 3.5 thêm dòng BARO-FSE-OB, dữ liệu TraceRCA, MicroRCA; sửa dòng GAIA; thêm câu 7 (kiểm file GAIA); tóm tắt ghi 7 câu hỏi.
  - N1: mục 0 (bảng và "điều làm đề xuất đổi"), 3.1 N6, 5.
  - N2: mục 0, 5. N3: 3.1 N6. N4: 3.5. N5: mục 0, 4.
- Sửa `results/T-021/scripts/build_bang.py` (R4: thêm 2 dòng vào bảng điều kiện), chạy lại `py -3 -X utf8 results/T-021/scripts/build_bang.py`: `dieu-kien-toi-thieu.csv` thêm 2 dòng. Script ghi lại cả `doc-lap.csv`, `tiep-xuc.csv`, `vi-tri-root.csv` từ cùng đầu vào; các file này chưa theo dõi bằng git nên không so được bằng diff.
- Không đổi census, vị trí, chia. Không sửa REVIEW.md ngoài bảng phản hồi (cột "Minh quyết" để Minh điền).
- Thấy thêm, chưa sửa (ngoài phạm vi duyệt): dòng DejaVu trong `build_bang.py` trỏ `K3:213`; dòng đúng là `K3:214`.

### Kết thúc phiên 3

1. **Đã làm:** phản hồi phản biện; sửa theo duyệt R1–R4, N1–N5.
2. **File đã thay đổi:** `results/T-021/goi-g1.md`, `results/T-021/scripts/build_bang.py`, bốn CSV do `build_bang.py` sinh, `tasks/T-021-goi-g1-thu-gon/REVIEW.md` (bảng cuối), LOG này, dòng T-021 trong `docs/STATE.md`.
3. **Kiểm tra:** mỗi chuỗi thay thế khớp đúng một lần (assert); `dieu-kien-toi-thieu.csv` có dòng 30–31 mới.
4. **Cần Minh quyết:** cột "Minh quyết" trong REVIEW.md; 7 câu hỏi ở `goi-g1.md` mục 6; sửa trỏ dòng DejaVu; duyệt đóng task và nội dung commit.
5. **Bước tiếp theo:** Minh đọc `results/T-021/goi-g1.md` mục 0 và 6, trả lời các câu hỏi G1.
6. **Lệnh cuối cùng đã chạy:** `py -3 -X utf8 results/T-021/scripts/build_bang.py`.

## Phiên 4 — 05/10/2026 — Claude (Opus 5.5) — Windows 11 laptop — vai trò: người làm (phản hồi phản biện lần 2)

- Minh yêu cầu Codex phản biện lại độc lập; Codex ghi `REVIEW-2.md`: 0 CHẶN, 2 KHÔNG CHẶN (R1 báo phủ vị trí giả; R2 bỏ sót trace construct Nezha).
- Kiểm lại: cả hai đúng (chi tiết ở bảng cuối `REVIEW-2.md`).
- Minh duyệt ngày 05/10/2026: "duyệt sửa R1, R2 và dòng DejaVu theo đề xuất".
- Đã sửa:
  - `results/T-021/scripts/chia.py`: so phủ theo nhóm vị trí bỏ hậu tố; thêm trường `ca_vi_tri_suy_theo_root_chua_kiem`. Chạy `py -3 -X utf8 results/T-021/scripts/chia.py --run chia-004` → `runs/chia-004/`, `runs/chia-004.stdout.txt`. Assert đạt. `vang_mot_phia` của gói A rỗng ở cả hai bản; gói B bản tỷ lệ còn đúng RE3-TT f2/f3/f4 như gói đã viết. Bốn CSV `chia-theo-o/` giống byte với bản chia-003 (so bằng `cmp` với bản sao trước khi chạy).
  - `results/T-021/goi-g1.md`: mục 3.1 N5 và câu 2 (trace construct Nezha, OPEN); mục 4 trỏ `runs/chia-004` và nói phủ vị trí.
  - `results/T-021/scripts/build_bang.py`: dòng DejaVu `K3:213` → `K3:214`; chạy lại, `dieu-kien-toi-thieu.csv` cập nhật.
  - `REVIEW-2.md`: bảng phản hồi (cột "Minh quyết" để trống).

### Kết thúc phiên 4

1. **Đã làm:** đánh giá REVIEW-2; sửa R1, R2, dòng DejaVu theo duyệt.
2. **File đã thay đổi:** `results/T-021/scripts/chia.py`, `results/T-021/runs/chia-004/`, `results/T-021/runs/chia-004.stdout.txt`, `results/T-021/chia-theo-o/*.csv` (ghi lại, giống byte), `results/T-021/goi-g1.md`, `results/T-021/scripts/build_bang.py`, các CSV do build_bang sinh, `tasks/T-021-goi-g1-thu-gon/REVIEW-2.md` (bảng cuối), LOG này, dòng T-021 trong `docs/STATE.md`.
3. **Kiểm tra:** assert chia đạt; `cmp` bốn CSV chia: giống byte; mọi chuỗi thay thế khớp đúng một lần.
4. **Cần Minh quyết:** cột "Minh quyết" ở REVIEW.md và REVIEW-2.md; độ dài `goi-g1.md` (khoảng 4.400 từ so với "khoảng 5 trang"); 7 câu hỏi G1 ở `goi-g1.md` mục 6; duyệt đóng task và nội dung commit.
5. **Bước tiếp theo:** Minh trả lời các câu hỏi G1 ở `results/T-021/goi-g1.md` mục 6.
6. **Lệnh cuối cùng đã chạy:** `py -3 -X utf8 results/T-021/scripts/build_bang.py`.

## Phiên 5 — 05/10/2026 — Claude (Opus 5.5) — Windows 11 laptop — vai trò: người làm (ghi quyết định G1)

- Minh trả lời G1 trong chat: "đồng ý với đề xuất 1 2, chấp nhận yếu cho nhận xét 'mở rộng dataset' của cô"; "đồng ý 7 câu hỏi"; "duyệt Q-61 đến Q-69, đưa TORAI lên tầng 1, đồng ý đề xuất 0".
- Đề xuất 1: gói A chạy theo bậc, Eadro-TT có điều kiện. Đề xuất 2: phương pháp hai tầng. Đề xuất 0: chốt G1 ngay, không thêm vòng phản biện T-021, đóng T-020 (thay bằng T-021), đặt lại mốc G4.
- Đã ghi Q-61–Q-69 vào `docs/DECISIONS.md`; cập nhật `docs/STATE.md` (cổng, dòng T-020, T-021, mục Task đang mở, Đang chờ Minh).

### Kết thúc phiên 5

1. **Đã làm:** ghi quyết định G1; đóng T-021.
2. **File đã thay đổi:** `docs/DECISIONS.md`, `docs/STATE.md`, LOG này, `tasks/T-020-tong-hop-g1/LOG.md` (mục đóng task).
3. **Kiểm tra:** mỗi chuỗi thay thế khớp đúng một lần (assert).
4. **Cần Minh quyết:** ngày mốc mới thay 20/10; cột "Minh quyết" ở hai REVIEW; nội dung commit.
5. **Bước tiếp theo:** viết SPEC task P3 bậc 1 (Q-61, Q-62), đọc `docs/MRP.md` P3 và `results/T-021/goi-g1.md` mục 2, 4.
6. **Lệnh cuối cùng đã chạy:** script Python ghi DECISIONS, STATE, hai LOG.

### Bổ sung phiên 5 — Minh duyệt bốn mục (05/10/2026, lời Minh: "duyệt")

- Q-70 vào `docs/DECISIONS.md`; sửa mốc ở `docs/MRP.md` §7 (G2 15–18/10, G4 cuối tháng 11/2026).
- `docs/STATE.md`: dòng test/giữ ngoài; bỏ hai mục chờ đã xong.
- Cột "Minh quyết" ở `REVIEW.md` (R1–R4, N1–N5) và `REVIEW-2.md` (R1, R2): "Duyệt sửa (05/10/2026)", theo lời duyệt ghi ở phiên 3 và phiên 4.
- Commit và push theo duyệt: `docs(G1): duyệt G1 (Q-61–Q-70); đóng T-020, T-021`.
