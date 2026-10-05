# T-021 — Gói G1 thu gọn

- **Trạng thái:** đề xuất (05/10/2026). Minh duyệt cho viết SPEC ("duyệt bước 0 1"); người làm phải tự soát SPEC trước khi làm (mục "Bước 0"). Sau tự soát (LOG phiên 1), Minh duyệt sửa S1–S7, K1, K2, K4 ngày 05/10/2026 ("đồng ý sửa giúp tôi các lỗi trên"; S1 chọn (a) và quy tắc bậc + độ nhạy). Sau tự soát lần 2 (LOG phiên 2), Minh duyệt sửa S8–S12 và K5–K7 ngày 05/10/2026 ("đồng ý sửa SPEC theo đề xuất, S8 chọn (i)").
- **Người làm:** Claude
- **Người phản biện:** Codex
- **Thuộc gói MRP:** P1, P2 — **Cổng:** G1

## Mục tiêu

Đưa Minh một gói đủ để duyệt G1, tức ba thứ MRP §7 yêu cầu: danh sách phương pháp, dataset, cách chia dev/test. Gói phục vụ hai nhận xét của cô: hiểu sâu phương pháp, và mở rộng thực nghiệm sang dataset công khai khác. Câu hỏi nghiên cứu là đích: RQ1, RQ2 (P4 chỉ dùng dev, nên cách chia quyết P4 thấy được gì), khả năng đánh giá RQ3a–d, và RQ4 (bằng chứng cho P8). RQ5 thuộc FlashTicket, ngoài phạm vi.

T-020 đã thu thập nhiều bằng chứng đúng nhưng trình quá rộng (6 thẻ, 40 phần dataset, ma trận 1.680 ô) và có ba lỗi CHẶN (REVIEW T-020 R1–R3). T-021 dùng lại bằng chứng của T-020, áp các quyết định mới Q-58, Q-59, Q-60 (WHY-21), và trình gọn.

Cách làm: đi **từ câu hỏi nghiên cứu xuống**, không từ danh sách dataset lên. Với mỗi RQ, hỏi cần dữ liệu gì; rồi chọn số bộ ít nhất phủ được các nhu cầu đó.

## Đầu vào

- Luật và quyết định: AGENTS.md; docs/MRP.md (§3, §4, P1–P4, §7); docs/DECISIONS.md (đặc biệt Q-37, Q-38, Q-54, Q-56, Q-58–Q-60); docs/WHY.md (WHY-03–05, 16, 19–21); docs/LESSONS.md.
- Nguồn đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md, advisor-2026-09-23.md.
- T-020: `tasks/T-020-tong-hop-g1/REVIEW.md` (gồm bảng phản hồi của người làm), LOG.md phiên 2 trở đi; `results/T-020/` là **kho bằng chứng**, chỉ đọc. Các file hay dùng: `trung-gian/exposure_ledger/public-census.csv`, `02-so-ca-da-nhin.csv`, `01-bang-tieu-chi-hop-nhat.csv`, `03-task-cham-duoc-va-che-do-b.md`, `trung-gian/dataset_evidence/{independence-axes.csv, root-mapping.csv}`, `07-danh-sach-phuong-phap-va-doc-nhanh.md`, `yeu-cau-dau-vao-hop-nhat.csv`, `scripts/chia_theo_o.py`.
- Bằng chứng gốc khi cần kiểm lại: thẻ và kết quả của T-002, T-003, T-008–T-012, T-019 (đặc biệt `results/T-009/runs/inspect-004/root-degree-whole-file.json`, `results/T-008/runs/evidence-002/summary.json` mục root_windows, `results/T-002/local-inspection/run-002/cases.json`, `results/T-002/local-inspection/run-002/all-service-positions.csv`); hồ sơ phương pháp T-013–T-018.
- Nguồn mức tiếp xúc (TX), ba nhóm (S11): (1) v1: `docs/MRP.md:120`, `docs/knowledge/K2-du-lieu.md` §1–2, `docs/LESSONS.md`; (2) TX1 từ các task thẻ: T-002, T-003, T-008–T-012, T-019; (3) TX2 từ sổ chạy phương pháp của T-005, T-006, T-007, T-013–T-018. Mỗi mức TX trỏ về một trong ba nhóm.
- Tập ứng viên (S12): 40 dòng của `results/T-020/01-bang-tieu-chi-hop-nhat.csv`, cộng các bộ có trong `docs/knowledge/K3-dataset-ung-vien.md` và `results/T-012/` mà bảng đó không có (ít nhất FAMOS TrainTicket, GAIA/MicroSS, DejaVu).

Không đọc `data/locked/`. Không đọc dữ liệu đo mới (chỉ dùng kết quả đã lưu trong `results/`).

## Đầu ra

Trong `results/T-021/`:

1. `goi-g1.md` — gói quyết định, **tối đa khoảng 5 trang**, viết để Minh và cô đọc hiểu không cần repo. Gồm:
   - Nửa trang đầu: Minh cần duyệt gì; đề xuất; điều gì làm đề xuất đổi; câu hỏi nào dữ liệu không phân xử nổi.
   - **Sáu câu của cổng** (MRP §7), mỗi câu trả lời ngắn có nguồn.
   - **Phương pháp:** giữ Q-37/Q-38; bảng ngắn ghi bản nào dùng làm baseline so sánh, bản nào chỉ để tái lập, và nối tới WHY-04, WHY-05, WHY-16, WHY-19, WHY-20 (giữ, sửa hay thay). Nêu các cặp phương pháp × dataset dự kiến vượt ngân sách Q-40 theo số đã đo (ví dụ BOCPD trên Train Ticket, `results/T-005/do-kha-thi.md`), ghi là phép chiếu chưa kiểm, kèm các phương án để Minh chọn.
   - **Dataset:** bảng "nhu cầu của từng RQ → bộ phủ nhu cầu đó"; bảng điều kiện tối thiểu (Q-58) cho các bộ được đề xuất; bảng phủ của cả gói theo tiêu chí 5, 6, 7, 8, 9 (tiêu chí 8 xét ở lớp gói, Minh duyệt 05/10/2026); bảng "đã xét, không dùng", mỗi bộ một câu lý do, phủ cả các bộ ở K3 và T-012 không có trong bảng T-020, ghi "chưa kiểm trên file" khi lý do chỉ dựa trên README/bài báo; bộ trông đủ mạnh mà chỉ thiếu kiểm file thì thành câu hỏi cho Minh (tải hay không), không tự tải (S12). Bảng phủ báo theo phía (dev, test, giữ ngoài): loại lỗi và nhóm vị trí nào vắng ở một phía (K6). Vị trí OPEN là "chưa biết", không tính là trượt; khi một bộ thua vì OPEN thì nói ra (K7). Bộ không có trace chỉ dùng có chủ đích, làm kịch bản đồ thị từ kiến trúc, và ghi rõ (MRP §4 tiêu chí 3). Với mỗi bộ RCAEval được đề xuất, chỉ ra nó phủ nhu cầu nào mà ứng viên khác không phủ (MRP §4, Q-31). Trả lời riêng vì sao dùng hay không dùng Sock Shop và LEMMA-RCA.
   - **Cách chia:** dev, test, giữ ngoài cho từng bộ; mức tiếp xúc TX đã sửa; số ô và số ca mỗi phía; ô chỉ một lần lặp; giới hạn của khoảng tin cậy. Cách dùng nhãn (MRP §4): nhãn nào để học, nhãn dev nào để chọn cấu hình, nhãn nào chỉ để chấm. Với bộ giữ ngoài: baseline nào dự kiến chạy được với đúng đầu vào và ngân sách nhãn, theo schema công bố, ghi "chưa kiểm trên file".
   - **Giới hạn của kết luận:** phần gói không phủ được (Q-58).
   - **Câu hỏi còn cho Minh:** chỉ những câu thật sự cần, mỗi câu có ngữ cảnh, các phương án, được/mất, đề xuất. Riêng cửa sổ, ngân sách nhãn và Retrieval@K (Q-54, Q-56 ghi quyết ở G1): trình ngắn mỗi việc một đoạn và hỏi Minh quyết ngay ở G1 hay chuyển xuống đầu P3. Không tự chuyển. Ghi rõ: chuyển sang P3 là sửa MRP §4 và Q-54; và độ dài cửa sổ có thể đổi bộ nào đủ dữ liệu bình thường, tức đổi lựa chọn dataset.
   - Chi tiết nằm trong các CSV; `goi-g1.md` chỉ trích các dòng cần quyết, để giữ độ dài.
2. `dieu-kien-toi-thieu.csv` — mỗi bộ được xét: năm điều kiện tối thiểu của Q-58, đạt/không/OPEN, nguồn file:dòng.
3. `vi-tri-root.csv` — theo Q-60(b): mỗi bộ dev/TX1 có dữ liệu bậc: root, bậc vào/ra, nhóm vị trí, số ô, nguồn. Bộ TX0 ghi OPEN.
   - **Đồ thị dùng** (Minh chọn phương án (a) ngày 05/10/2026): bậc đã lưu trong `results/`, không đọc dữ liệu đo. Mỗi bộ ghi đồ thị đã dùng và chỗ lệch Q-60(b) (đồ thị lúc bình thường): Eadro toàn file, có cả đoạn tiêm; Nezha các file phút chồng ±60 s quanh lúc tiêm, hai giả thuyết đồng hồ; RE2-TT theo từng ca, dùng đồ thị trước mốc tiêm (`all-service-positions.csv`, window = pre_injection) làm chính, báo kèm đồ thị full (K5). Lệch này ghi thành giới hạn của kết luận theo vị trí.
   - **Quy tắc nhóm** (Minh duyệt 05/10/2026), trên đồ thị service có hướng, cạnh từ service gọi tới service bị gọi: không có trong trace; bậc 0 (vào = 0, ra = 0); nguồn (vào = 0, ra > 0); lá (vào > 0, ra = 0); hub (vào > 0, ra > 0, tổng bậc từ phân vị 75 của các nút trong chính đồ thị đó trở lên); giữa (các nút vào > 0, ra > 0 còn lại). Độ nhạy: báo thêm nhóm khi ngưỡng hub là phân vị 90.
   - **Bộ chỉ lưu bậc của root** (Eadro, Nezha; S8 phương án (i), Minh chọn 05/10/2026): gán không có trong trace, bậc 0, nguồn, lá như trên; gộp "giữa hoặc hub" thành một nhóm; hub ghi OPEN và ghi thành giới hạn. Đồ thị đầy đủ để P5 dựng.
   - **Gộp từ ca lên ô** (S9): báo nhóm theo từng ca; một ô có nhóm X khi mọi ca của ô cùng nhóm X, nếu không thì ghi "không ổn định"; Nezha báo riêng từng giả thuyết đồng hồ.
4. `doc-lap.csv` — mỗi bộ ngoài RCAEval: ba trục (tác giả, công cụ tiêm lỗi, hệ thu thập) so với RCAEval, kết luận theo Q-60(c): khác / trùng / OPEN, nguồn.
5. `tiep-xuc.csv` — mức TX đã sửa cho các bộ được đề xuất và các ứng viên giữ ngoài, mỗi mức có nguồn thuộc một trong ba nhóm ở Đầu vào (S10, S11): 60 ca RE2-TT là TX1 (MRP §4:120, K2 §1); ca đã bị dò triệu chứng theo từng ca ghi cột riêng (Q-60(a)).
6. `chia-theo-o/*.csv` và `scripts/chia.py` — chia toàn ô, seed `20261004` (dùng lại seed T-020 để so được; seed không mang thông tin về kết quả). Trình hai phiên bản để Minh chọn: tỷ lệ chia như T-020, và phân tầng theo loại lỗi (REVIEW T-020 R4). Nêu lý do của tỷ lệ; không viết như FACT rằng tỷ lệ đến từ v1 nếu không có nguồn.
7. `runs/` — đầu ra kiểm (assert) của script.

## Phạm vi ghi

Chỉ ghi vào các đường dẫn dưới đây, cộng `tasks/T-021-goi-g1-thu-gon/LOG.md` và dòng T-021 trong `docs/STATE.md`. Ghi ra ngoài thì dừng, đề xuất.

- `results/T-021/`
- `tasks/T-021-goi-g1-thu-gon/SPEC.md` chỉ khi Minh duyệt sửa SPEC.

Không sửa `results/T-020/`, task cũ, `src/`, docs chung. Đề xuất sửa docs chung (nếu có) ghi trong `results/T-021/de-xuat-tai-lieu-chung.md`.

## Các bước

0. **Tự soát SPEC trước khi làm.** Đọc SPEC này như người phản biện. Nếu thấy lỗi, thiếu, mâu thuẫn với MRP/DECISIONS, hoặc chỗ dẫn hướng đáp án: dừng, ghi vào LOG, báo Minh, chưa làm bước 1. — kiểm bằng: mục "Tự soát SPEC" trong LOG.
1. Lập bảng "nhu cầu dữ liệu theo RQ" từ MRP §3, §4, P3, P4, P7, P8, trước khi xem lại số của từng bộ. Bảng chỉ dẫn MRP, không dẫn số của bộ nào. — kiểm bằng: bảng ghi vào LOG trước bước 2.
2. Áp điều kiện tối thiểu (Q-58, Q-59) cho tập ứng viên ở Đầu vào (40 dòng của `results/T-020/01-bang-tieu-chi-hop-nhat.csv` cộng các bộ K3/T-012 bảng đó thiếu). Số dùng để giữ/loại phải lấy từ file kết quả gốc, không từ văn xuôi. — kiểm bằng: đếm lại số ca, root, ô từ thẻ và kết quả gốc của T-002, T-003, T-008–T-012, T-019; `results/T-020/trung-gian/exposure_ledger/public-census.csv` chỉ dùng để đối chiếu, lệch thì ghi; mức TX không lấy từ sổ T-020 mà từ ba nhóm nguồn ở Đầu vào; mỗi hàng có nguồn.
3. Lập `vi-tri-root.csv`, `doc-lap.csv`, `tiep-xuc.csv` từ dữ liệu đã có. — kiểm bằng: tính lại bậc và nhóm từ file nguồn (cả hai ngưỡng hub ở bộ có bậc của mọi nút; bộ chỉ có bậc root theo S8 (i)); đối chiếu số root/ô với số đếm ở bước 2.
4. Chọn gói nhỏ nhất phủ được bảng nhu cầu ở bước 1. Có ít nhất một phương án khác để so, trong đó có một gói lớn hơn kèm được/mất ("nhỏ nhất" là tiêu chí chi phí) (K7); mỗi đề xuất có lập luận mạnh nhất chống lại nó và bằng chứng sẽ làm đổi ý. Không chọn theo kết quả phương pháp đã chạy (Q-33, QT4). — kiểm bằng: mỗi nhu cầu RQ trỏ tới ít nhất một bộ hoặc một dòng giới hạn.
5. Chia ô bằng script, hai phiên bản. — kiểm bằng assert: mỗi ô đúng một phía; không ca TX2 ở test hay giữ ngoài; mọi ca của bộ giữ ngoài là TX0 (MRP §4:117; S10); tổng ô và ca khớp số đếm ở bước 2; nếu gói có RE2-TT thì 30 ca TX2 (10 ô dev của v1) nằm ở dev, còn vai trò của 60 ca kia theo lựa chọn ở bước 4. Script báo loại lỗi và nhóm vị trí có ở dev, ở test, và liệt kê cái vắng ở một phía (K6).
6. Viết `goi-g1.md`. — kiểm bằng: mọi số có đường dẫn nguồn; độ dài ≤ khoảng 5 trang; mỗi câu cần Minh quyết có ngữ cảnh và được/mất.
7. Báo cáo cuối phiên trong LOG theo AGENTS mục 7; viết prompt phản biện cho Codex theo `docs/review-prompt.md` (Prompt chung + khối G1, chỉ điền thông tin trung tính).

## Kiểm đúng đắn

- Số census, root, ô, TX: tính lại từ file gốc bằng script, lưu ở `runs/`.
- Vị trí root: tính lại từ file bậc; nêu rõ phạm vi (toàn file, ±60 s quanh lúc tiêm, hai giả thuyết đồng hồ của Nezha) và chỗ lệch Q-60(b).
- Không kiểm được trong task: vị trí root và lan triệu chứng của bộ TX0 (cần mở dữ liệu đo); giấy phép bằng văn bản; chất lượng dữ liệu bình thường. Ghi thành OPEN kèm hệ quả cho kết luận.

## Tiêu chí xong

- Có đủ 7 đầu ra; `goi-g1.md` ≤ khoảng 5 trang.
- R1–R3 của REVIEW T-020 được xử lý trong gói (ghi rõ chỗ).
- Mọi bộ trong tập ứng viên ở Đầu vào (T-020 cộng các bộ K3/T-012 bảng T-020 thiếu) hoặc được đề xuất, hoặc có một câu lý do không dùng.
- Assert của script chia đạt; không đọc `data/locked/`; không ghi ngoài phạm vi.
- LOG có tự soát SPEC, bảng nhu cầu RQ (ghi trước khi chọn), báo cáo cuối và prompt phản biện.

## Không làm

- Không chạy phương pháp, không đọc dữ liệu đo mới, không tải dữ liệu.
- Không dựng adapter hay evaluator (việc của P3).
- Không sửa T-020 hay các lỗi KHÔNG CHẶN của nó (R4–R6, N1–N5), trừ khi chúng đổi lựa chọn G1. R4 (tỷ lệ chia), R5 (BOCPD và Q-40) và R6 (nối WHY) thuộc diện đổi lựa chọn G1, nên được xử lý trong gói (xem Đầu ra 1, 6).
- Không tự quyết thay Minh: chỉ đề xuất.
- Không thêm quy trình, cổng, phép kiểm mới.

## Chi phí ước lượng

Một phiên. Chỉ đọc file đã có và chạy script nhẹ (dưới 1 phút). Không cần báo trước theo luật cứng 8. Không dùng subagent trừ khi Minh cho phép.

## Rủi ro và điều chưa chắc

- Gói có thể vẫn không phân xử được RQ3a chế độ tự phát hiện (mốc tiêm lộ qua biên file) và RQ3c (không có nhãn vùng công khai). Nếu đúng, nói ở nửa trang đầu.
- Bằng chứng của T-020 có thể còn lỗi chưa phát hiện; số dùng để giữ/loại phải kiểm lại từ nguồn gốc.
- SPEC này do Claude viết sau khi phản biện T-020, nên có thể đã mang sẵn quan điểm của phản biện. Bước 0 tồn tại để chặn điều đó.
