# Nhật ký T-020

## Phiên 1 — 04/10/2026 — Codex — Windows 11 — người làm

Mở phiên: đã đọc luật và nguồn bắt buộc. Task mới, chưa có đầu ra phiên trước. HEAD 5636b6984dd5acae8a6de56f26d182f8867d1e56; git status/diff HEAD lúc bắt đầu không có thay đổi.

Minh ủy quyền tự duyệt SPEC theo prompt G1 ngày 04/10/2026

Quyết định Minh trong phiên (prompt; chưa ghi tài liệu chung): "không giới hạn số subagent, chỉ giới hạn dùng model gpt 6.1 sol ultra".

## Nguyên văn nhiệm vụ

<nhiem_vu> vào LOG.
- Không ai duyệt SPEC trước khi bạn làm, nên lỗ hổng trong SPEC sẽ đi thẳng vào kết quả mà không ai chặn. Viết SPEC kỹ như thể một người phản biện sẽ đọc nó trước.
- Gặp việc vượt <gioi_han>: không làm việc đó; ghi vào LOG và vào mục "Cần Minh quyết"; làm tiếp phần còn lại.
</uy_quyen>

<doc_truoc>
1. Đọc toàn bộ: AGENTS.md, docs/STATE.md, docs/LESSONS.md, docs/review-prompt.md, tasks/_MAU/SPEC.md, tasks/_MAU/LOG.md.
2. Đọc toàn bộ docs/MRP.md. Đọc kỹ §4 (dataset, chia dữ liệu), P1, P2, §6, §7.
3. Đọc toàn bộ docs/WHY.md và docs/DECISIONS.md. Khi trích một quyết định, nói rõ nó là lời Minh trực tiếp, quyết định agent thực hiện theo ủy quyền, hay đề xuất chưa duyệt.
4. Đọc docs/knowledge/K1 đến K4 (MRP §11 ghi là chưa kiểm lại), docs/reference/sources/DT18-de-tai-va-nhiem-vu.md, docs/reference/sources/advisor-2026-09-23.md.
5. Từ commit 93f13d4 đến nay, nhiều file chung đã đổi và các task T-013 đến T-019 chưa commit. Chạy git status, git diff HEAD --stat, git diff HEAD -- docs/ (chỉ đọc) để biết bản hiện hành. Đừng dựa vào trí nhớ về nội dung MRP hay WHY.
6. Các lỗi đã xảy ra trong repo, không được lặp:
   - SL8, SL15, QT16: đo giá trị đồ thị trên dữ liệu không phân xử được; chọn dataset rồi mới biết nó không phân xử nổi.
   - SL14, SL21: nêu mẫu hình từ trung bình nhóm (thực ra một ô); rồi kết luận quá tay theo chiều ngược.
   - SL17, QT17: viết số từ trí nhớ, không từ file kết quả.
   - SL20, QT4: gắn "hoàn thành" với "đồ thị phải thắng"; chọn theo mức chênh giữa nhánh đồ thị và không đồ thị.
   - SL23: đề xuất chưa kiểm nhưng nói như sự thật.
   - SL24: báo "chạy được" khi mới biết "không lỗi".
   - SL25: chạy lâu mà không ghi tiến độ.
   - SL26: SPEC bỏ một phép kiểm mà không nêu hệ quả.
   - SL27: tính chi phí theo từng ca, không theo tổng.
   - SL28: tra số công bố sau khi đã đo.
   - SL29: môi trường không ghim phiên bản.
   - SL30: đo thời gian khi máy đang chạy việc khác.
   - SL31: prompt phản biện có gợi ý, làm neo người phản biện.
   - SL32: bước xếp theo thứ tự đọc, không theo phụ thuộc.
   - SL33: kiểm trên dữ liệu nhỏ, bỏ quy mô Train Ticket.
   - SL34: regex suy tên làm gộp nhầm.
   - SL35: viết câu phổ quát ("mọi", "đều") sau khi chỉ nhìn một thư mục.
   - SL36: kết luận "khớp" chỉ vì điểm cuối khớp số công bố, trong khi cơ chế bên trong sai.
   - REVIEW T-003 R1: bàn giao "xong" khi phần được phép kiểm chưa làm; ghi việc chưa làm thành "chờ quyền".
   - REVIEW T-003 R2: thẻ dataset bỏ sót đường lộ mốc tiêm qua cấu trúc file.
   - Q-31: thiên vị RCAEval vì "đã có sẵn".
   - Ngày 04/10: hai phiên ghi đè cùng một file chung, làm mất WHY-16 đã được duyệt.
   - Từng có script kiểm (T-003 verify_final.py) ghi thẳng vào thư mục run của task cũ.
</doc_truoc>

<nguyen_tac_doc_lap>
1. Không có đáp án định sẵn. Prompt này cố ý không nêu dataset nào nên chọn, và thứ tự liệt kê trong prompt chỉ là thứ tự thư mục, không phải thứ tự ưu tiên. Tự lập danh sách ứng viên từ MRP §4/P2 và từ các thẻ; không mặc định bộ nào vì "đã có sẵn", "đã được bảo toàn", hay "đứng đầu danh sách" (Q-31).
2. Ghi tiên nghiệm trước khi điền bảng: trong SPEC, ghi quy tắc đủ điều kiện cho từng vai trò, cách so các phương án, cách xử lý hòa và dữ liệu thiếu, quy tắc lấy mẫu kiểm chéo, các seed. Sau đó mới điền.
3. Số liệu quan trọng lấy từ file kết quả gốc (JSON, CSV, log trong results/), không từ văn xuôi của thẻ hay báo cáo. Số công bố và số đếm file lệch nhau thì giữ cả hai, không chọn một.
4. Kiểm chéo có kế hoạch, không theo cảm tính: quy tắc lấy mẫu ghi trong SPEC trước khi đọc giá trị, có seed. Tối thiểu: mọi đại lượng xuất hiện ở từ hai tài liệu trở lên; ít nhất 5 số liệu quan trọng từ mỗi task đầu vào, chọn theo quy tắc.
5. Xung đột lợi ích. WHY-13 và Q-49 (giữ OpenRCA Bank) là quyết định Codex thực hiện theo ủy quyền, không phải lời Minh chọn Bank. Coi như đề xuất của người khác và đánh giá lại bằng cùng bảng tiêu chí như mọi ứng viên.
6. Mỗi khuyến nghị kèm lập luận mạnh nhất chống lại nó, và bằng chứng nào sẽ làm bạn đổi ý.
7. Kết quả phương pháp trên các ca đã chạy (T-005 đến T-018) KHÔNG được dùng để chọn dataset, cửa sổ hay cách chia theo hướng "bên nào thắng". Chỉ được dùng để: (a) xác định ca nào đã bị nhìn; (b) giải thích cơ chế; (c) đối chiếu số công bố; (d) đánh giá khả năng phân xử (còn chỗ để các phương pháp tách nhau không), kèm nguyên nhân khả thi khác (Q-33).
8. Mỗi câu phải rõ nó thuộc loại nào: yêu cầu của DT18 hay cô; lời Minh trực tiếp; quyết định theo ủy quyền; đề xuất của agent; ứng viên; FACT đo trên file; FACT từ nguồn công bố.
9. Nếu kết cục dễ xảy ra nhất là "không bộ nào phân xử nổi một RQ" hoặc "không có bộ giữ ngoài nào đủ tiêu chí", nói ngay trong nửa trang đầu (QT16).
10. Không nêu rủi ro thời hạn hay rủi ro FlashTicket (Q-34). Hướng đúng ưu tiên hơn tốc độ (MRP §7).
</nguyen_tac_doc_lap>

<dau_vao>
Phương pháp (P1):
- results/T-001/danh-sach-phuong-phap.md (mục 8 là danh sách đã chốt, Q-37 và Q-38; mục 9 là revision), results/T-005/do-kha-thi.md, results/T-006/kiem-dung-dan.md, results/T-007/kiem-dung-dan.md.
- Hồ sơ và bảng đầu vào của T-013 (BARO, BOCPD, N-Sigma phát hiện), T-014 (CIRCA PC và kiến trúc), T-015 (MicroRank, TraceRCA, detector trace), T-016 (TORAI, RCD), T-017 (SimpleRCA), T-018 (GDN, DecompRCA). Trong mỗi results/T-0xx/ có ho-so-*.md, yeu-cau-dau-vao.csv, ca-da-chay.csv, dinh-chinh-task-cu.md, de-xuat-tai-lieu-chung.md; báo cáo cuối nằm ở LOG hoặc bao-cao-cuoi.md. Các file này chưa commit.
- Mã đã cài trong src/ (circa_kien_truc, microrank, simplerca, torai): chỉ đọc.

Dataset (P2):
- Họ RCAEval: results/T-002/ (the-rcaeval.md, mau-the-dataset.md, public-metadata/, local-inspection/); results/T-019/ (the-sock-shop.md, census-cases.csv, census-cells.csv, so-ca-da-nhin.csv, ledger-summary.json).
- Ngoài RCAEval: results/T-003/ (bang-tieu-chi.md, task-cham-duoc.md, the-dataset-ngoai-rcaeval.md, bao-toan-openrca-bank.md, source-manifest.json); thẻ ở results/T-008, T-009, T-010, T-011; results/T-012/ (the-dataset.md, task-and-source-matrix.md, independence-matrix.md, profiles.json).
- data/README.md; tasks/*/REVIEW.md của T-002, T-003, T-013 đến T-019 (điểm phản biện và phản hồi của người làm).

Quyết định và lý do liên quan: Q-31, Q-33, Q-34, Q-37, Q-38, Q-40, Q-41, Q-43, Q-44, Q-47, Q-48, Q-49, Q-54, Q-56; WHY-03 đến WHY-07, WHY-10, WHY-13 đến WHY-20.

Trạng thái T-013: đọc dòng T-013 trong STATE. Lúc viết prompt này, T-013 có điểm phản biện R1 (CHẶN) chờ Minh quyết sửa. Nếu T-013 đã sửa, dùng bản mới. Nếu chưa, dùng bản hiện có, và đánh dấu mọi kết luận của bạn phụ thuộc vào phần R1. Đừng chờ, đừng sửa file của T-013.
</dau_vao>

<nhiem_vu>
Thư mục task: tasks/T-020-tong-hop-g1/. Thư mục kết quả: results/T-020/. Người làm: Codex. Người phản biện: Claude. Gói P1 và P2, cổng G1.

Phải làm đủ 10 việc V1 đến V10. Mỗi việc có đầu ra ở <dau_ra>.

V1. Kiểm kê mọi mục đã chuyển sang G1.
- Đọc mục "Cần Minh quyết" của báo cáo cuối, REVIEW và bảng phản hồi, de-xuat-tai-lieu-chung.md, dinh-chinh-task-cu.md, dòng STATE của T-001 đến T-019. Lập 08-so-chuyen-g1.csv: id, nguồn (file:dòng), nội dung, loại, trạng thái, thẻ quyết định tương ứng.
- Loại: (a) MRP §7 yêu cầu quyết ở G1; (b) Minh đã chuyển sang G1 bằng lời (đọc DECISIONS); (c) task đề nghị, Minh chưa chuyển; (d) thuộc P3 trở đi; (e) đã đóng.
- (a) và (b) bắt buộc có thẻ quyết định. (c) có thẻ nếu ảnh hưởng (a) hoặc (b); nếu không thì một dòng "chuyển P3" kèm lý do. Không làm G1 phình ra (luật cứng 9).
- Kiểm bao phủ: tìm tự động mọi chỗ trong LOG, REVIEW, báo cáo, nháp của T-001 đến T-019 có chữ "G1" hoặc "chốt ở". Mỗi chỗ phải ánh xạ tới một dòng của 08-so-chuyen-g1.csv. Báo số chỗ tìm được và số chỗ đã ánh xạ.

V2. Bảng chín tiêu chí hợp nhất.
- Ứng viên: mọi bộ trong MRP §4/P2 ("Ứng viên cần kiểm ở P2") và mọi bộ có thẻ trong results/. Đối chiếu hai danh sách; bộ nào có ở một nơi mà thiếu ở nơi kia thì ghi.
- Một bảng, một định nghĩa cho mỗi tiêu chí (chép từ MRP §4), áp cho mọi ứng viên, kể cả họ RCAEval (Q-31). Mỗi ô có: trạng thái (FACT đo trên file; FACT từ nguồn công bố; OPEN kèm người giải quyết và đầu vào cần), con số, đường dẫn tới file kết quả gốc.
- Chi phí (tải, dung lượng, công viết adapter) ở cột riêng, không dùng để loại hay xếp hạng phân xử.
- Ô quyết định việc giữ, loại hay vai trò của một bộ phải được kiểm lại từ file kết quả gốc, không từ văn xuôi của thẻ. Ô khác có thể trích từ thẻ, nhưng ghi "trích thẻ, chưa kiểm lại".
- Nếu một bộ RCAEval có mặt trong phương án đề xuất, nêu nó hơn các ứng viên khác ở tiêu chí nào (MRP §4).
- Phân biệt "chưa kiểm vì chưa làm" với "không kiểm được vì MRP §4 cấm trước G1" (ví dụ chạy phương pháp trên bộ giữ ngoài).

V3. Sổ ca đã nhìn hợp nhất.
- Định nghĩa theo MRP §4: ca "chưa mở" nghĩa là chưa ai xem kết quả phương pháp trên từng ca. Bộ "giữ ngoài" nghĩa là trước G3 chỉ được đọc metadata, schema, đếm nhãn, không xem dữ liệu đo. Đề xuất ký hiệu (tránh trùng M1 đến M4 của T-001 và loại mốc A/B/C của T-006): TX0 = chỉ metadata, schema, đếm nhãn; TX1 = đã đọc thống kê mô tả của dữ liệu đo, chưa thấy kết quả phương pháp theo ca; TX2 = đã thấy kết quả phương pháp theo ca. Nếu MRP §4 mơ hồ ở điểm nào, nêu và đưa vào thẻ quyết định; không tự diễn giải rộng.
- Nguồn: lượt chạy của T-005, T-006, T-007; ca-da-chay.csv của T-013 đến T-018 và ca-da-chay-lich-su.csv của T-017; so-ca-da-nhin.csv của T-019; các khảo sát số đo ở T-008 đến T-012 (mức TX1). Cột của các file khác nhau: chuẩn hóa bằng script, không bằng tay.
- Đếm sự cố duy nhất, không đếm hàng (ledger-summary.json của T-019 đã cảnh báo). Quan hệ trùng giữa các bản (bản sao, bản đã xử lý, artifact cùng byte) phải có bằng chứng (mốc tiêm, hash, so nội dung) lấy từ file gốc, không suy từ tên.
- Đầu ra: theo từng (dataset, ô) mức tiếp xúc cao nhất; tổng kết số ca và số ô còn ở TX0 và TX1. Script tái lập được. Tổng theo nguồn phải bằng tổng hợp nhất (assert).
- Xác nhận 60 ca RE2-TT trong data/locked/ không có mặt trong bất kỳ lượt chạy nào của sổ, bằng sổ và metadata công khai. Không mở data/locked/, kể cả cases.parquet.

V4. Task chấm được, chế độ (b) và đường lộ nhãn.
- Với mỗi ứng viên và mỗi loại task: xếp hạng nguyên nhân gốc; phát hiện theo thời gian ở chế độ (a) biết trước thời điểm sự cố và chế độ (b) tự phát hiện; vùng ảnh hưởng; bất thường theo trace; học có giám sát hay chuyển hệ. Ghi: nhãn thật có theo nguồn; đơn vị chấm (service, pod, instance, operation...) và bảng ánh xạ kèm nguồn; phạm vi; giới hạn.
- Phân biệt nhãn theo khoảng tiêm lỗi với nhãn bất thường quan sát được (MRP P2). Nhãn thời gian là lúc tiêm, onset hay end: ghi rõ. Nếu chỉ có thời điểm tiêm thì độ trễ phát hiện chỉ được gọi là "tính từ lúc tiêm" (MRP P7).
- Chế độ (b): liệt kê mọi đường lộ thời điểm tiêm của từng dataset: biên file đối xứng quanh mốc tiêm; chỉ có file quanh lúc tiêm; tên file hay đường dẫn mang mốc; thống kê toàn file chứa mốc; thứ tự file; v.v. Lấy từ thẻ, T-006 mục 2.3, T-008 (sampling-leakage), T-013 (cua-so-va-che-do-b.md), T-018. Kiểm lại từ file kết quả gốc ít nhất các đường lộ mà kết luận dựa vào. Kết luận: dataset nào chấm được RQ3a ở chế độ (b), theo loại nhãn thời gian nào.
- Đường lộ ở runner và adapter, không chỉ ở dữ liệu (ví dụ runner chọn SLI theo service gốc, MRP P2). Kiểm các adapter của T-013 đến T-018 có nhận tên ca, đường dẫn hay mốc tiêm ở chế độ (b) hay không.

V5. Ma trận phương pháp x dataset.
- Hợp nhất sáu yeu-cau-dau-vao.csv thành yeu-cau-dau-vao-hop-nhat.csv; kiểm cột có trùng khớp; liệt kê các ô "chua_kiem".
- Mỗi cặp (phương pháp, biến thể hoặc bộ phát hiện) x (dataset, hoặc phần dataset khác về tín hiệu), một trong bốn trạng thái: chạy nguyên trạng; cần adapter (mô tả, công sức, suy được từ dữ liệu mà không dùng nhãn hay không); không chạy được (lý do); chưa kiểm. Mỗi ô nêu: tín hiệu cần và tín hiệu có; đơn vị xếp hạng; dữ liệu bình thường tối thiểu và dữ liệu có; tập ứng viên có chứa nguyên nhân gốc không (trần Hit@k); điều kiện bài toán (biết thời điểm hay tự phát hiện; nhãn nào được dùng). Phương pháp khác điều kiện thì không xếp chung bảng nếu không ghi rõ (MRP §4).
- Chi phí chạy: từ số đo đã có (T-005, T-013 đến T-018), quy về tổng cho cả dataset (SL27) và so với ngân sách Q-40 (3 giờ). Cột riêng, không dùng để loại dataset.
- Không chạy phương pháp nào để lấp ô. Ô chỉ kiểm được bằng cách chạy trên dữ liệu mới thì ghi: "chưa kiểm: MRP §4 chốt cách chia ở G1 trước khi chạy phương pháp trên dữ liệu mới", kèm giả định, khi nào giả định sai, việc nào ở P3 sẽ kiểm.

V6. Cách dùng nhãn, độ dài cửa sổ, Retrieval@K.
(a) Nhãn (MRP §4): bảng cho từng phương pháp: nhãn nào để học (cột can_nhan_de_hoc); nhãn dev nào dùng để chọn cấu hình hay checkpoint; nhãn nào chỉ để chấm (nhãn test chỉ để chấm). Baseline nào chạy được trên dataset giữ ngoài với đúng đầu vào và ngân sách nhãn. Phương pháp có giám sát học theo tập service của từng hệ nên không chuyển hệ khác được.
(b) Cửa sổ (Q-54):
- Liệt kê mọi tham số độ dài hay vị trí cửa sổ thật sự khác nhau giữa phương pháp, chế độ và dataset. Tự tìm đủ từ hồ sơ và kết quả. Đơn vị khác nhau (phút, giây, số dòng, số điểm) và tần số lấy mẫu khác nhau: quy đổi trước khi so.
- Giải thích bằng cơ chế vì sao kết quả đổi theo cửa sổ, kèm bằng chứng từ ca đã thấy (T-006 mục 2.1, T-007, T-013 cua-so-va-che-do-b.md và REVIEW của T-013, T-015 kiem-cua-so-ob.csv, T-016 giam-mau-hai-lan.md, T-018). Tự tính lại ít nhất một đại lượng từ file kết quả gốc.
- MRP P3 yêu cầu cùng cửa sổ cho mọi phương pháp. Đề xuất ít nhất hai phương án cùng quy tắc chọn đặt TRƯỚC khi nhìn điểm; độ nhạy báo kèm (QT3); và nói điều gì xảy ra với phương pháp mà cửa sổ của tác giả khác.
- Khuyến nghị theo cơ chế và prior work (QT2), không theo điểm (QT4). Q-54 ghi chưa đủ căn cứ để chọn một số. Nếu bằng chứng vẫn chưa đủ, nói thẳng, nêu việc nào ở P3 sẽ quyết và quy tắc quyết, thay vì ép một con số.
(c) Retrieval@K và Rerank@1 (Q-56, mục E2): trình bày đề xuất ở results/T-018/de-xuat-tai-lieu-chung.md (mục E2); điều kiện để tính được trên từng dataset (quy đổi metric sang service; tập ứng viên); các phương án; khuyến nghị.

V7. Phương án gói dataset, vai trò và cách chia.
- Từ bảng V2 đến V6, tự thiết kế ít nhất ba phương án khác nhau về cấu trúc (prompt này không đặt sẵn phương án). Mỗi phương án nêu: danh sách dataset và vai trò (dev, test, giữ ngoài, chỉ tái lập); đơn vị chia (ô); số ô và số ca mỗi phía; RQ nào trả lời được và đến đâu (RQ1, RQ3a đến RQ3d; RQ3c chỉ FlashTicket mới có nhãn vùng); tiêu chí 9 (bộ độc lập) có đạt không và theo mấy trục (nhóm tác giả, công cụ tiêm lỗi, stack thu thập); phương pháp nào chạy được trên từng bộ; mất gì nếu chọn; so với yêu cầu của cô ("mở rộng ra các dataset public khác").
- Chia theo ô (thành phần gốc x loại lỗi): mọi lần lặp của một ô cùng một phía. Chỉ dùng census nhãn công khai (results/T-002/public-metadata/, results/T-019/census-*.csv, thẻ ngoài RCAEval), không đọc dữ liệu đo, không đọc data/locked/. Viết script tái lập; seed và quy tắc phân tầng (nếu dùng) ghi vào SPEC trước khi chạy. Assert: mỗi ô đúng một phía; không ca TX2 nào ở phía test hay giữ ngoài; số ô khớp census. Dataset đã có cách chia từ v1 (30 ca dev và 60 ca khóa của RE2-TT): nêu giữ hay đổi, vì sao.
- Nêu số ô mỗi phía đủ cho khoảng tin cậy bootstrap theo ô (MRP P7) đến đâu; ô chỉ có một lần lặp; dataset quá ít ô để chia. Không giấu bằng con số trung bình.
- Dataset giữ ngoài: đánh giá lại độc lập mọi ứng viên bằng cùng bảng, kể cả OpenRCA Bank. Nêu cả phương án "không bộ nào đủ tiêu chí" nếu đúng (QT16).
- Bộ giữ ngoài đã bị đọc thống kê dữ liệu đo (TX1) thì không còn "hoàn toàn ngoài thiết kế" theo MRP §4. Nêu hệ quả cho vai trò của bộ đó.
- Đọc schema thật của bộ được đề nghị giữ ngoài (MRP §4 cho phép đọc schema) chỉ được làm nếu bảo đảm đọc đúng dòng tiêu đề, dừng ở ký tự xuống dòng đầu tiên, không đọc dòng dữ liệu nào, không giải nén thêm, mỗi loại tín hiệu tối đa một file. Ghi số byte đã đọc và cách bảo đảm. Không bảo đảm được thì không làm; ghi vào "Cần Minh quyết" kèm lý do.

V8. Danh sách phương pháp.
- Danh sách đã chốt ở Q-37 và Q-38 (results/T-001/danh-sach-phuong-phap.md mục 8). Kiểm từng phương pháp, biến thể và bộ phát hiện đã có hồ sơ đủ các mục của MRP P1 (cơ chế, công thức, mặc định có file:dòng, khác biệt bài-code, giả định, ví dụ tính tay) và đã chạy được một ca. Lập bảng kiểm có đường dẫn tới đúng mục. Thiếu gì thì ghi; không tự viết lại hồ sơ của task khác.
- Phủ các họ của MRP P1: họ nào chưa có đại diện RCA (Minh đã biết ở Q-37) thì nêu một dòng kèm hệ quả cho RQ; không đòi sửa.
- Kiểm tên gọi các biến thể có nhất quán giữa hồ sơ, WHY, DECISIONS, T-001 (ví dụ các tên "bản RCAEval", "sửa đầu vào", "sửa").
- Bản đọc nhanh cho Minh: mỗi phương pháp, biến thể, bộ phát hiện một đoạn tối đa 350 từ, tiếng Việt đơn giản. Gồm: làm gì; đầu vào và đầu ra; chấm điểm thế nào; đồ thị tham gia ở đâu; khác bài ở đâu; điều kiện hỏng; cần gì để chạy ở dataset khác; link tới mục hồ sơ. Mục đích: MRP P1 "Minh đọc hiểu được cơ chế mà không cần đọc code". Viết từ hồ sơ rồi kiểm lại với bài hoặc code gốc ở revision ghi trong T-001 mục 9.
- Kiểm chéo ít nhất hai phương pháp với bài và code gốc: công thức, tham số mặc định (file:dòng), khác biệt bài-code. Quy tắc chọn ghi trong SPEC trước khi đọc; ít nhất một hồ sơ do Claude viết (T-016 hoặc T-018) và một do Codex viết.
- Chạy lại các script "tính lại độc lập" của hồ sơ nếu nhẹ (dưới 5 phút mỗi script), chỉ trên dữ liệu của ca TX2. Chỉ chạy khi bảo đảm script không ghi vào thư mục task cũ: chép script sang results/T-020/ và đổi đường dẫn ghi, hoặc dùng tham số đầu ra. So git status trước và sau mỗi lần chạy. Script không chạy lại được thì ghi lý do. Ghi các lượt này vào ca-da-chay.csv (lý do: kiểm tính lặp lại).

V9. Đính chính và đề xuất tài liệu chung.
- Gộp dinh-chinh-task-cu.md của T-013 đến T-019 và các đính chính từ REVIEW của T-002, T-003. Mỗi mục: kiểm lại bằng chứng (toàn bộ nếu ít, lấy mẫu theo quy tắc nếu nhiều); trạng thái (đã áp vào tài liệu chung, chờ Minh, hay không áp dụng); kết luận G1 nào bị ảnh hưởng.
- Gộp de-xuat-tai-lieu-chung.md của T-013 đến T-019. Đối chiếu từng đề xuất với bản hiện hành của WHY, DECISIONS, LESSONS, K1, MRP: đã áp đúng nguyên văn, đã áp biến thể, hay chưa áp. Lập danh sách "chờ Minh duyệt". Không ghi.
- Mâu thuẫn mới giữa các tài liệu hiện hành mà bạn phát hiện: nêu kèm file:dòng.
- Nháp dòng DECISIONS và mục WHY cho từng lựa chọn G1 (viết trong de-xuat-tai-lieu-chung.md, ghi rõ "nháp, chưa duyệt"). Luật cứng 3: lựa chọn quan trọng cần mục WHY trước khi dùng trong kết quả. Vì G1 chưa duyệt, mọi chỗ trong gói dùng một lựa chọn như vậy ghi "(chờ WHY)".

V10. Gói quyết định G1.
- Tệp g1-goi-quyet-dinh.md, tối đa khoảng 3.000 từ không tính bảng. Bảng rộng và chi tiết nằm ở file phụ lục có link. Viết để cô đọc hiểu mà không cần đọc repo (AGENTS mục 10): mã nội bộ (T-xxx, Q-xx, WHY-xx) luôn kèm một cụm giải thích ở lần đầu.
- Nửa trang đầu: Minh cần quyết gì; bạn khuyến nghị gì; điều gì làm khuyến nghị đổi; chỗ nào dữ liệu có thể không phân xử nổi một RQ.
- Trả lời riêng từng câu trong sáu câu của cổng (MRP §7). Chỗ nào câu trả lời là "chưa" thì nói "chưa" và nói vì sao.
- Thẻ quyết định D1, D2, ...: câu hỏi; vì sao phải quyết ở G1 (trỏ MRP hoặc Q-xx); các phương án (mỗi phương án: nghĩa là gì, bằng chứng, được gì, mất gì, có đảo ngược được sau G1 không); khuyến nghị; lập luận mạnh nhất chống khuyến nghị; bằng chứng sẽ làm đổi khuyến nghị; hệ quả cho từng RQ; nháp dòng DECISIONS nếu chọn.
- Trả lời bắt buộc: vì sao dùng hay không dùng Sock Shop và LEMMA-RCA (MRP §4, cô đã nêu tên), mỗi bộ một đoạn có bằng chứng; bộ nào đạt tiêu chí 9 và theo mấy trục; RQ nào có nguy cơ không phân xử nổi; đối chiếu gói đề xuất với từng yêu cầu trong advisor-2026-09-23.
- Phụ lục 10-ke-hoach-p3-de-xuat.md (luật cứng 12; chưa kiểm; Minh duyệt rồi mới làm): thứ tự P3 theo phụ thuộc; việc chạy song song được; việc nặng nên chạy qua đêm hay trên máy khác; ước lượng thời gian theo Q-40 từ số đo đã có; việc dùng lại kết quả sẵn có. Không nêu rủi ro thời hạn (Q-34).
</nhiem_vu>

## Diễn biến

- Đóng băng 5.771 file docs/tasks/src/results T001–T019 bằng SHA256, byte, mtime; không mở data/locked.
- Ghi SPEC trước mọi script triển khai. Tự phản biện SPEC: bổ sung TX2 gián tiếp, không cộng trace/file-minute vào số incident, C9 không suy từ khác miền, chi phí tổng×seed, script cũ có write ngoài phạm vi. Seed kiểm/split 20261004; không chọn theo accuracy. Không thay V1–V10.
- Chọn kiểm sâu trước đọc giá trị theo hash seed: T-015|MicroRank.
- Chọn kiểm sâu trước đọc giá trị theo hash seed: T-016|TORAI.
- Giai đoạn A: sinh sổ V1 trên LOG/REVIEW và mọi Markdown results T001–T019: 533 match, 533 ánh xạ; 322 dòng ngữ cảnh cần Minh, 877 dòng tổng. Đã soát các dòng chưa gắn thẻ, tách tham chiếu mẫu/lịch sử khỏi lựa chọn. Script governance_inventory.py và g1-coverage.json.
- Ba subagent đã bắt đầu: dataset_evidence V2/V4, exposure_ledger V3/census V7, method_evidence V5/V6 evidence/V8; model gpt-6.1-sol, reasoning ultra, fork none; chỉ thư mục results/T-020/trung-gian/<luồng>. Thời gian chính xác có trong trạng thái công cụ; chưa benchmark chính thức.
- Bổ sung hash data/README.md vào input-freeze: chỉ file mô tả dữ liệu, không locked.

### Checkpoint 04/10/2026 21:17 (UTC+7)

- Ngữ cảnh được nén; tiếp tục từ file đã có, không làm lại kết quả hợp lệ. A có bảng33 candidate, ledger/census và checklist42 hàng ở trung-gian; chưa hợp nhất cuối. B đang bắt đầu: ma trận tương thích, nhãn/cửa sổ, ba gói chia. Root vẫn tự quyết đề xuất, subagent chỉ bằng chứng.
- 49 phép đếm độc lập từ nguồn T002/T012/T019 khớp. Lượt verifier001 hỏng vì expected RE3-TT do root nhập từ trí nhớ (3root/10ô); đã giữ script/output hỏng và sửa lấy expected count-summary.json: 2root/8ô. Đây là lỗi verifier T020, không phải lỗi nguồn T002. Lượt002 đạt49/49.
- Index số JSON167766 lá là inventory bổ trợ, chưa gọi là checked; chỉ các phép thực sự tính lại được vào bảng09. Input freeze5772 sau bổ sung README metadata. Không raw mới, không locked.
- Bước tiếp: hợp nhất dữ liệu V2–V8, chạy split metadata/identity assertions; đọc đầu ra subagent rồi kiểm nguồn trọng yếu; V9/V10 và audit phạm vi.

- 21:26–21:34 giai đoạn B: hợp nhất37phần dataset ×42hàng method=1554cặp; giữ đủheaders/source/chua_kiem. Ba split metadata đạt one-side/census/noTX2test và v130/60. Viết05 nhãn/windows,06gói/split và10P3 đề xuất, g1 draftD1–D6; chưaquyếtđịnh. Root kiểm lại code gốcTORAI15hai lần/bản sửa một lần,needle/hashMicroRank/BARO/CIRCA (17 phép).

- Root-code001/002 fail preserved: bản sửa có hai câu lệnh stride, nhưng câu thứhai nằm trong if not sua_giam_mau; hai hàm mặc địnhTrue. Retry003 root_code_audit.py kiểm guard/defaults,2gốc/1active mặc định và17checksPASS. Dòng tiến độ cũ tóm tắt trướccheck hoàn tất được đính chính ở đây, không sửa LOG lịch sử.

### Tiếp tục sau usage limit — 04/10/2026 21:32 (UTC+7)

- Minh yêu cầu đảm bảo tiến độ/chất lượng và kiểm3subagent. list_agents xác nhận cả3interrupted; followup_task tiếp tục cả3đúng việc chưa xong, không tạoagent/modelmới.
- File đầu ra hiện còn đầy đủ, gitstatus chỉ docs/STATE và hai thư mục T020. Rehash input5772: 1changed/0missing; chi tiết resume-freeze-audit.json. Chỉ STATE dòngT020 là thay đổi dự kiến. Chưa finish, còn V9/bảng09/manifest/reviewerprompt/finalaudit và sửa đọc hiểu.

### Sự cố phạm vi đọc — báo Minh ngay trong chat

- Dataset subagent báo đã đọc/in một đoạn results/T-010/runs/schema-samples.json; file schema chứa cả ví dụ dòng số đo TX1. Không chạy phương pháp mới/không đọc data/locked, nhưng đây là đọc raw vượt giới hạn. Đã yêu cầu dừng, ghi exactincident trong trung-gian/dataset_evidence, không dùng payload làm số/role, loại proof từ sample này và chỉ aggregate/metadata cho phần còn lại. Không xóa dấu vết. Mọi tuyên bố “không đọc raw” tuyệt đối phải thay bằng phạm vi/ngoại lệ đã nêu.
- Audit subagent phát hiện “time/unit đã kiểm” của draft G1 quá rộng; root đã sửa chỉ nhãn/census/mốc tiêm trên mẫu, physicaldurationunit vẫnOPEN theoT002/T015. Không thay decision/tài liệu chung.

### Checkpoint 04/10/2026 22:03 (UTC+7)

- Sau nén ngữ cảnh tiếp tục cùng T020, không khởi động lại phần hợp lệ. Dataset và method đã bàn giao, exposure còn audit ngữ nghĩa V1. Kiểm live status cả ba, không coi interrupted là hoàn thành.
- Method cuối có 208 phép kiểm chuẩn hóa và 16 lượt thử (12 exit0, bốn lượt lỗi được giữ: ba môi trường/API, một kiểm MicroRank). Bốn bộ đếm chẩn đoán normal/anomaly khác do định nghĩa null-root; root đang kiểm nguồn và gộp vào09/đính chính, không giấu bằng cách chỉ lấy retry đạt.
- Bước kế: chốt override V1, hợp nhất checks/replays, kiểm đọc hiểu và phạm vi toàn bộ, ghi prompt phản biện/manifest rồi mới chuyển dòng T020 sang chờ phản biện. Chưa đóng G1 và không ghi tài liệu quyết định chung.


## Kết thúc phiên — 04/10/2026 22:23:30 (UTC+7) — Codex — Windows laptop — người làm

### Diễn biến giai đoạn C

- Hợp nhất 40 phần dataset, 42 hàng yêu cầu, 1680 cặp; 728 cần adapter, 825 chưa kiểm, 127 không chạy được trong phần tín hiệu chỉ định. Không coi “có file” là schema đã kiểm.
- V1 audit ngữ nghĩa giữ 877 dòng/533 occurrence; áp 683 override với exact ID+source+content. Root đọc 18 mẫu theo hash seed và các dòng bắt buộc a/b; các sai phân loại ban đầu đã sửa. Sau hợp nhất: a2/b2/c257/d18/e598. Bốn gate bắt buộc đủ D1–D6.
- V9 đối chiếu 90 section: 4 áp nguyên văn, 23 biến thể, 50 chưa áp, 13 không áp. Giữ từng body cũ→mới và evidence đích; không coi section là thay đổi độc lập. Không tự sửa WHY/DECISIONS.
- Tính lại 3248 phép: 3235 MATCH, 4 MISMATCH MicroRank, 9 OPEN. Chín OPEN là mẫu bổ trợ, pool quan trọng mỗi task đủ ít nhất năm; T004 không có nguồn triển khai để tạo mẫu.
- 16 replay TX2/fixture: 12 exit0, bốn lỗi giữ đủ (ba môi trường/API; một kiểm audit MicroRank). Tổng wall subprocess 78.406 giây; không là runtime chính thức. Bốn graph relations/SLO/counts của ca MicroRank khớp, audit null-root khác định nghĩa.
- Tự đọc G1 và phụ lục, sửa: physical duration unit OPEN; trace LEMMA ngày khác chưa kiểm; SimpleRCA metric-rule chỉ metric; ngân sách mốc chế độ a; Bank raw-provider OPEN; ô bootstrap chưa chứng minh độc lập; RE1-SS 100TX2+25TX1; GDN học một lần/hệ/seed. G1 1816 từ thân trước chỉnh câu cuối, dưới khoảng 3000; 42 đoạn biến thể tối đa209 từ trước link edit cuối.
- Root final verifier lần đầu so bytes worktree CRLF với git blob LF nên fail; kiểm lại bằng SHA input freeze chứng minh không đổi byte ngoài dòng T020. Verifier sửa dùng hash byte gốc và đối chiếu HEAD sau chuẩn hóa newline; không sửa nguồn để PASS.

### Ba subagent và bàn giao

Đã dùng đúng ba agent, cùng model **gpt-6.1-sol**, reasoning **ultra**, fork none. Luồng dataset_evidence làm V2/V4; exposure_ledger làm V3/census và audit V1/V9; method_evidence làm V5/V6/V8 factual. Chỉ root viết file cuối/thẻ/khuyến nghị/STATE. Không giao quyền quyết định.

Usage limit làm cả ba interrupted; list_agents xác nhận, followup tiếp tục đúng luồng. Dataset bàn giao kiểm cuối khoảng14:55 UTC, bổ sung đọc draft sau đó; method bàn giao nhận lúc15:03 UTC; exposure bàn giao nhận trước15:19 UTC. Đây là mốc quan sát bàn giao, không giả thời gian bắt đầu/CPU. Thời gian chính xác từng script ở run JSON; 16 replay78.406s, V1 replay0.452709s, build ledger1.425971s và independent validate0.346354s. Toàn bộ kiểm hash đóng băng đạt, không thay model để né limit. Worker folders nằm `results/T-020/trung-gian/{dataset_evidence,exposure_ledger,method_evidence}/`; manifest từng luồng giữ hash payload.

### Đối chiếu V1–V10 và tiêu chí xong

| Việc | Đầu ra và kiểm |
|---|---|
| V1 | 08, coverage533/533, 877dòng và683semanticoverrides; nguồn exact line, root18mẫu |
| V2 | 01 đủ40phần, C1–C9 cùng định nghĩa; 0ôtrống, schema/license/provenance ghiOPEN đúng phạm vi |
| V3 | 02, build_ledger và independent_validate;1417identityunits, không phải1417physicalincidents; 60lockedTT không có exposure/method-result |
| V4 | 03, task/leakage/root-mapping; không gọi injection là onset hoặc traceclass là service-root |
| V5 | 04 1680cặp và42requirement;16cột nguyên+bốnprovenance,0header mismatch,chua_kiem giữ nguyên |
| V6 | 05; budget fit/tune/score/normal/heldout, known/blind riêng; W-time/W-feasible chưa chốt số |
| V7 | 06, baCSV chia-theo-o vàassert; wholecell/census/noTX2test/v130/60 đạt; CIgiớihạn theo ô |
| V8 | 07,42đoạn vàchecklist;MicroRank/TORAIghim sâu,16replay dưới5phút;failures/inventory giữ đủ |
| V9 | Hai fileđínhchính/nhápchung;90section đối chiếu hiện hành,34section đínhchính; T002R1–5/T003R1–4 kiểm hiện trạng |
| V10 | G1 sáucâu trảlời riêng/D1–D6 đủ phươngán/phảnđối/đổibằngchứng/RQ/nháp;10P3 theo phụ thuộc vàQ40toàn bộ×seed |

Tiêu chí1–7 và9–11: các file/checks/coverage/split/nháp và prompt đủ theo bảng trên. Tiêu chí8 về ghi file đạt: chỉ SPEC/LOG/resultsT020 và dòngSTATE; không data/locked, không method mới. Tuy nhiên **phạm vi đọc có sự cố raw TX1** bên dưới; không trình toàn bộ tuân thủ tuyệt đối. Manifest và final-audit giữ ngoại lệ này. Tiêu chí G1 là đủ gói để phản biện/quyết, không tự duyệt G1.

| Yêu cầu gốc | Bằng chứng |
|---|---|
| P1 hiểu cơ chế/công thức/default/bài-code/giả định/tính tay | 07; method-checklist.csv; deep-source-audit.md;09; replaystdout/intermediate |
| P2 cùng tiêu chí/task chấm được/dataset/split | 01–06; C9 từng trục; source/license/schema; chia_theo_o.py vàsplit-assertions |
| G1 danh sách/dataset/chia vàQ54/Q56 | g1-goi-quyet-dinh.md D1–D6,08,nhápWHY/DEC; chưa P3/P5 |

### Bảng việc còn lại

| Việc | Làm được trong giới hạn T020? | Loại/lý do và người hoặc đầu vào cần |
|---|---|---|
| Duyệt D1–D6/WHY và các sửa nguồn chung | Không | Cần Minh quyết; chỉ nháp đã được phép ghi |
| Chốt mốc chế độ a so với MRP “test labels chỉ chấm” | Không | Cần Minh làm rõ D4; không tự cấp nhãn test |
| Mở test/giữ ngoài, raw TX0/TX1 để xác nhận adapter/clock/normal | Không | MRP§4 và giới hạn đọc; G3+Minh cho phép |
| Bank tiêu đề thật | Không với artifact/cơ chế hiện có | V7 đã cấp first-line có điều kiện; cần nguồn bất biến và cơ chế exact newline/noinflate, không thiếu quyền đã cấp |
| Chín lá bổ trợ OPEN | Không với nguồn hiện có | T008/T010/T011 cầnrawTX1; T003 cầnthànhphầnmetadatađộc lập. Cần nguồn phù hợp doMinh cấp/xác nhận, không dùngsốđóquyếtrole |
| Runtime mới toàn bộ/normal calibration/CI theo kết quả | Không | P3/P7+, cầndataset/protocol đãduyệt; không chạy trongT020 |
| C9 injector/collector/raw-provider và giấy phép | Không thể xác nhận từ nguồn đã có | Cầnnguồn tácgiả/provider hoặcquyếtđịnh vai tròMinh; khôngbịađểđóng |
| Phản biện task/G1 | Không thuộc người làm | Claude phiên riêng theo prompt cuốiLOG; Minh quyết findings |

Không có việc kiểm được phép và có đủ đầu vào còn bỏ dở. Không có đầu ra cần lấy riêng từ EC2 trongT020.

### Báo cáo A–I

**A. Đã làm:** đủ V1–V10 và gói G1 đề xuất; giữ sáu thẻ, ba cấu trúc split, nguồn/OPEN và kiểm số. Chưa đóng G1.

**B. File đã thay đổi:** `tasks/T-020-tong-hop-g1/SPEC.md`, LOG.md; mọi file trong `results/T-020/` (manifest kê đủ); đúng dòng T020 của `docs/STATE.md` chuyển chờ phản biện. Không tạo file ngoài repo; không sửa task cũ/src/shareddocs. Byte mọi dòngSTATEkhác giữ nguyên.

**C. Kiểm:** 3248 phép kiểm số với3235khớp/4sai khácgiải thích/9OPEN; metadata census/split assertions đạt;17rootcode/24rootcost/49rootcounts; 42đoạn≤350từ; 40parts×42=1680; coverage533/533; sourcepins/hash inputs/giới hạn ghi/link/diffcheck đạt. Final-audit.json là kết quả kiểm cuối, không phải OS-wide trace chứng minh mọi lần đọc.

**D. VẤN ĐỀ Ở TASK CŨ — ĐỂ REVIEWER KIỂM:** xem `dinh-chinh-task-cu.md`. Mới: bốn audit counters MicroRank khác null-root version; V3 thêm125localRE1OBTX2 (40copyFSE,85aliasHFOPEN); NezhaTT45records cóclockxungđột; giữ những proposal chưaáp/phạmvi đãáp và bỏ mục Minh loại. T002/T003 đã sửa được kiểm hiện trạng, không dùng review banđầu làm chặn. T020dùngphạmvigiớihạn đãđínhchính, không sửa nguồn cũ.

**E. Lệch SPEC:** sự cố dataset worker đọc nhầm file schema chứa raw TX1, đã báo Minh ngay và giữ scope-incident.md/json. Không có file cũ bị đổi, không locked hoặc method mới; loại payload khỏi schema proof. Ngoài ra, ba agent interrupted được tiếp tục, không thay mô hình/quy tắc; sửa verifier và phrasing sau kiểm nguồn, không đổi seed/selection. Đọc hợp lệ sau sự cố dùng aggregate/header witness thay sample payload. Không đề nghị coi sự cố là hợp lệ hồi tố.

**F. Tài liệu chung/commit:** xem `de-xuat-tai-lieu-chung.md`; pending chưa ghi, các templateWHY/DEC phải Minh chọn rồi duyệt. Nội dung commit đề xuất: `docs(T-020): tổng hợp gói quyết định G1 và bằng chứng kiểm chéo`. Chưa commit/push.

**G. Chưa kiểm:** chín mẫu OPEN; schema/unit/normal các bộ chưa được mở; Bank header thật, license/provenance C9; P3 calibration và blind evaluation. Không tuyên bố có heldout đạt3trục hoặc vùng ảnh hưởng publicgold. Sự cố rawread đãnêu làgiớihạn audit, không che bằnghashequal.

**H. Cần Minh quyết:** D1 biến thể; D2 gói/vai trò; D3 TX1/test/split; D4 nhãn/normal/mốc; D5 quy tắc window; D6 Retrieval/Rerank. Ngoài thẻ: nguồn/license/provenance/header đápứngV7; sửa tài liệu chung đúngđoạn; cách xửlýQ40chi phílịch sửCIRCA nếu cần. Không yêu cầu duyệt lại đề xuất bịloại.

**I. Xung đột lợi ích:** thẻ Codex/T013/T014/T015/T017 và Q49/WHY13 bảo toànBank được đối xử như nguồn cầnkiểm. Tính từ gốccomponent/Census/hashselectedsamples; deep MicroRank chọn trước cùngTORAIcủaClaude; root code/count/cost kiểm riêng. V9 đọc từng câu hiện hành/exception, V1 nguồn exact-content. Những câuquárộng được sửa; Bank không tựđượcchọnvìCodexđãbảo toàn. Subagent làđầu vào, không thay phảnbiệnClaude.

### Sáu ý kết thúc theo mẫu LOG

1. Đã làm: A/V1–V10 ở trên; gói chờ phản biện.
2. File: B và manifest.json; không có outputngoàirepo.
3. Kiểm: C,09,runs/final-audit.json; failures vàscopeincident giữ đủ.
4. Chưa chắc/cần Minh: G/H và Bảng việc còn lại. Không ghi quyếtđịnhG1thayMinh.
5. Bước tiếp chính xác: Minh mở **Claude Code phiên mới trong D:\RCA-flashticket**, dán nguyên prompt cuối LOG. Claude đọc SPEC/LOG và mọi file liệt kê, chỉ ghi REVIEW.md. Sau review người làm tự soát trước rồi phản hồi từng finding theoAGENTS; chưa sửa task cũ tự động.
6. Lệnh cuối: `py -3 -X utf8 -B results/T-020/scripts/prepare_handoff.py`; script gọi final_audit.py, ghi prompt/filelist/manifest rồi kiểm hashes. Phản biệnkhông dùnggitdiff làm phạmvi duy nhất.


## Prompt phản biện cho Claude — chép vào phiên mới

```text
Bạn là người phản biện độc lập cho task T-020 của repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Bạn chỉ được ghi đúng một file: tasks/T-020-tong-hop-g1/REVIEW.md, theo mẫu tasks/_MAU/REVIEW.md.
Không sửa file nào khác, không commit.

Đọc: tasks/T-020-tong-hop-g1/SPEC.md, tasks/T-020-tong-hop-g1/LOG.md, các file đầu ra: docs/STATE.md,
results/T-020/01-bang-tieu-chi-hop-nhat.csv,
results/T-020/01-bang-tieu-chi-hop-nhat.md,
results/T-020/02-so-ca-da-nhin.csv,
results/T-020/02-so-ca-da-nhin.md,
results/T-020/03-task-cham-duoc-va-che-do-b.md,
results/T-020/04-phuong-phap-x-dataset.csv,
results/T-020/04-phuong-phap-x-dataset.md,
results/T-020/05-nhan-va-cua-so.md,
results/T-020/06-phuong-an-dataset-va-chia.md,
results/T-020/07-danh-sach-phuong-phap-va-doc-nhanh.md,
results/T-020/08-so-chuyen-g1.csv,
results/T-020/09-kiem-cheo-so-lieu.csv,
results/T-020/09-kiem-cheo-so-lieu.md,
results/T-020/10-ke-hoach-p3-de-xuat.md,
results/T-020/ca-da-chay.csv,
results/T-020/chia-theo-o/A-da-tin-hieu.csv,
results/T-020/chia-theo-o/B-kien-truc-khong-trace.csv,
results/T-020/chia-theo-o/C-test-TX0.csv,
results/T-020/de-xuat-tai-lieu-chung.md,
results/T-020/dinh-chinh-task-cu.md,
results/T-020/g1-goi-quyet-dinh.md,
results/T-020/manifest.json,
results/T-020/runs/crosscheck-merge-assertions.json,
results/T-020/runs/final-audit.json,
results/T-020/runs/final-source-pins.json,
results/T-020/runs/matrix-assertions.json,
results/T-020/runs/numeric-inventory-console.txt,
results/T-020/runs/readability-final.json,
results/T-020/runs/resume-freeze-audit.json,
results/T-020/runs/review-prompt-audit.json,
results/T-020/runs/root-checks-001-failed.csv,
results/T-020/runs/root-checks-001-failure.txt,
results/T-020/runs/root-checks-001-script.py,
results/T-020/runs/root-checks-002-console.txt,
results/T-020/runs/root-cost-failed-001.py,
results/T-020/runs/root-cost-failed-001.txt,
results/T-020/runs/spacing-applied.json,
results/T-020/runs/split-assertions.json,
results/T-020/scripts/chia_theo_o.py,
results/T-020/scripts/final_audit.py,
results/T-020/scripts/finish_readability.py,
results/T-020/scripts/governance_inventory.py,
results/T-020/scripts/hop_nhat.py,
results/T-020/scripts/kiem_cheo_hop_nhat.py,
results/T-020/scripts/numeric_inventory.py,
results/T-020/scripts/prepare_handoff.py,
results/T-020/scripts/refine_text.py,
results/T-020/scripts/root_checks.py,
results/T-020/scripts/root_code_audit.py,
results/T-020/scripts/root_cost_audit.py,
results/T-020/scripts/tai_lap_so_ca.py,
results/T-020/trung-gian/dataset_evidence/01-bang-tieu-chi-hop-nhat.csv,
results/T-020/trung-gian/dataset_evidence/01-bang-tieu-chi-hop-nhat.md,
results/T-020/trung-gian/dataset_evidence/03-task-cham-duoc-va-che-do-b.md,
results/T-020/trung-gian/dataset_evidence/HANDOFF.md,
results/T-020/trung-gian/dataset_evidence/T004-no-scientific-pool.json,
results/T-020/trung-gian/dataset_evidence/build_evidence.py,
results/T-020/trung-gian/dataset_evidence/build_provenance.py,
results/T-020/trung-gian/dataset_evidence/census-cells.csv,
results/T-020/trung-gian/dataset_evidence/check_root_sample.py,
results/T-020/trung-gian/dataset_evidence/checks.csv,
results/T-020/trung-gian/dataset_evidence/extract_public_pdf.py,
results/T-020/trung-gian/dataset_evidence/final-package-audit.md,
results/T-020/trung-gian/dataset_evidence/final-validation.json,
results/T-020/trung-gian/dataset_evidence/final_audit.py,
results/T-020/trung-gian/dataset_evidence/freeze-recheck.csv,
results/T-020/trung-gian/dataset_evidence/heldout-schema-provenance.md,
results/T-020/trung-gian/dataset_evidence/independence-axes.csv,
results/T-020/trung-gian/dataset_evidence/input-hashes-used.json,
results/T-020/trung-gian/dataset_evidence/leakage-data.csv,
results/T-020/trung-gian/dataset_evidence/license-revision.csv,
results/T-020/trung-gian/dataset_evidence/nezha-paper-text.json,
results/T-020/trung-gian/dataset_evidence/output-manifest.json,
results/T-020/trung-gian/dataset_evidence/provenance-input-hashes.json,
results/T-020/trung-gian/dataset_evidence/provenance-run.json,
results/T-020/trung-gian/dataset_evidence/public-source-claims-checked.csv,
results/T-020/trung-gian/dataset_evidence/public-source-verification.json,
results/T-020/trung-gian/dataset_evidence/review-rechecks.json,
results/T-020/trung-gian/dataset_evidence/root-final-dataset-audit.md,
results/T-020/trung-gian/dataset_evidence/root-mapping.csv,
results/T-020/trung-gian/dataset_evidence/root-sample-run-001.txt,
results/T-020/trung-gian/dataset_evidence/root-sample-run-002.txt,
results/T-020/trung-gian/dataset_evidence/root-selected-checks.csv,
results/T-020/trung-gian/dataset_evidence/run-002.txt,
results/T-020/trung-gian/dataset_evidence/run-003.txt,
results/T-020/trung-gian/dataset_evidence/run-004.txt,
results/T-020/trung-gian/dataset_evidence/runner-leakage-method-worker.csv,
results/T-020/trung-gian/dataset_evidence/schema-provenance.csv,
results/T-020/trung-gian/dataset_evidence/schema-witnesses.json,
results/T-020/trung-gian/dataset_evidence/schema_and_spacing.py,
results/T-020/trung-gian/dataset_evidence/scope-incident.json,
results/T-020/trung-gian/dataset_evidence/scope-incident.md,
results/T-020/trung-gian/dataset_evidence/seeded-checks.csv,
results/T-020/trung-gian/dataset_evidence/spacing-fixes.csv,
results/T-020/trung-gian/dataset_evidence/supporting.json,
results/T-020/trung-gian/dataset_evidence/task-matrix.csv,
results/T-020/trung-gian/exposure_ledger/02-so-ca-da-nhin.csv,
results/T-020/trung-gian/exposure_ledger/02-so-ca-da-nhin.md,
results/T-020/trung-gian/exposure_ledger/application-audit-reviewed.csv,
results/T-020/trung-gian/exposure_ledger/application-audit-reviewed.md,
results/T-020/trung-gian/exposure_ledger/archive-audit.csv,
results/T-020/trung-gian/exposure_ledger/audit-repair-001.json,
results/T-020/trung-gian/exposure_ledger/build_ledger.py,
results/T-020/trung-gian/exposure_ledger/build_v1_semantic_overrides.py,
results/T-020/trung-gian/exposure_ledger/cell-exposure.csv,
results/T-020/trung-gian/exposure_ledger/csv-normalization-audit.csv,
results/T-020/trung-gian/exposure_ledger/dataset-census-membership.csv,
results/T-020/trung-gian/exposure_ledger/dataset-exposure.csv,
results/T-020/trung-gian/exposure_ledger/dataset-membership-exposure.csv,
results/T-020/trung-gian/exposure_ledger/exposure-evidence.csv,
results/T-020/trung-gian/exposure_ledger/failed-run-001.json,
results/T-020/trung-gian/exposure_ledger/failed-run-002.json,
results/T-020/trung-gian/exposure_ledger/independent-assertions.json,
results/T-020/trung-gian/exposure_ledger/independent_validate.py,
results/T-020/trung-gian/exposure_ledger/input-read-manifest.json,
results/T-020/trung-gian/exposure_ledger/locked-public-60.csv,
results/T-020/trung-gian/exposure_ledger/numeric-check-all.csv,
results/T-020/trung-gian/exposure_ledger/numeric-check-selected.csv,
results/T-020/trung-gian/exposure_ledger/numeric-leaf-pool.csv,
results/T-020/trung-gian/exposure_ledger/output-manifest.json,
results/T-020/trung-gian/exposure_ledger/public-census.csv,
results/T-020/trung-gian/exposure_ledger/root-draft-audit-snapshots.json,
results/T-020/trung-gian/exposure_ledger/root-draft-audit.md,
results/T-020/trung-gian/exposure_ledger/run-assertions.json,
results/T-020/trung-gian/exposure_ledger/source-intersections.csv,
results/T-020/trung-gian/exposure_ledger/source-reconciliation.csv,
results/T-020/trung-gian/exposure_ledger/unresolved-aliases.csv,
results/T-020/trung-gian/exposure_ledger/unresolved-source-rows.csv,
results/T-020/trung-gian/exposure_ledger/v1-replay-failures.json,
results/T-020/trung-gian/exposure_ledger/v1-review-input.csv,
results/T-020/trung-gian/exposure_ledger/v1-semantic-assertions.json,
results/T-020/trung-gian/exposure_ledger/v1-semantic-audit.md,
results/T-020/trung-gian/exposure_ledger/v1-semantic-overrides.csv,
results/T-020/trung-gian/exposure_ledger/v1-semantic-review-plan.json,
results/T-020/trung-gian/git-status-initial.txt,
results/T-020/trung-gian/input-freeze.json,
results/T-020/trung-gian/method_evidence/05-evidence.md,
results/T-020/trung-gian/method_evidence/07-checklist-doc-nhanh.md,
results/T-020/trung-gian/method_evidence/HANDOFF.md,
results/T-020/trung-gian/method_evidence/T001-checks.csv,
results/T-020/trung-gian/method_evidence/ca-da-chay.csv,
results/T-020/trung-gian/method_evidence/checks-normalized.csv,
results/T-020/trung-gian/method_evidence/checks.csv,
results/T-020/trung-gian/method_evidence/deep-source-audit.md,
results/T-020/trung-gian/method_evidence/header-audit.csv,
results/T-020/trung-gian/method_evidence/independent-script-inventory.csv,
results/T-020/trung-gian/method_evidence/label-budget.csv,
results/T-020/trung-gian/method_evidence/method-checklist.csv,
results/T-020/trung-gian/method_evidence/mismatches.csv,
results/T-020/trung-gian/method_evidence/numeric-sample-candidates.csv,
results/T-020/trung-gian/method_evidence/output-manifest.json,
results/T-020/trung-gian/method_evidence/runner-leakage.csv,
results/T-020/trung-gian/method_evidence/runs/all-replay-copy-audit.json,
results/T-020/trung-gian/method_evidence/runs/all-replays.json,
results/T-020/trung-gian/method_evidence/runs/build-001-failed.json,
results/T-020/trung-gian/method_evidence/runs/build-summary.json,
results/T-020/trung-gian/method_evidence/runs/circa-arithmetic-001/comparison.csv,
results/T-020/trung-gian/method_evidence/runs/circa-arithmetic-001/comparison.json,
results/T-020/trung-gian/method_evidence/runs/circa-graph-independent-001.json,
results/T-020/trung-gian/method_evidence/runs/circa-window-002/window-comparison.json,
results/T-020/trung-gian/method_evidence/runs/deep-001-failed.json,
results/T-020/trung-gian/method_evidence/runs/deep-source-audit.json,
results/T-020/trung-gian/method_evidence/runs/deep-status-after.json,
results/T-020/trung-gian/method_evidence/runs/deep-status-before.json,
results/T-020/trung-gian/method_evidence/runs/final-audit-summary.json,
results/T-020/trung-gian/method_evidence/runs/gdn-A_bien_the_b.npy,
results/T-020/trung-gian/method_evidence/runs/gdn-A_tay.npy,
results/T-020/trung-gian/method_evidence/runs/gdn-analysis-001.json,
results/T-020/trung-gian/method_evidence/runs/input-freeze-verification.json,
results/T-020/trung-gian/method_evidence/runs/microrank-fixture-001/anomaly-iterations.csv,
results/T-020/trung-gian/method_evidence/runs/microrank-fixture-001/anomaly-operations.csv,
results/T-020/trung-gian/method_evidence/runs/microrank-fixture-001/anomaly-traces.csv,
results/T-020/trung-gian/method_evidence/runs/microrank-fixture-001/comparison.csv,
results/T-020/trung-gian/method_evidence/runs/microrank-fixture-001/normal-iterations.csv,
results/T-020/trung-gian/method_evidence/runs/microrank-fixture-001/normal-operations.csv,
results/T-020/trung-gian/method_evidence/runs/microrank-fixture-001/normal-traces.csv,
results/T-020/trung-gian/method_evidence/runs/microrank-fixture-001/progress.jsonl,
results/T-020/trung-gian/method_evidence/runs/microrank-fixture-001/spectrum-scores.csv,
results/T-020/trung-gian/method_evidence/runs/microrank-fixture-001/summary.json,
results/T-020/trung-gian/method_evidence/runs/microrank-fixture-002/anomaly-iterations.csv,
results/T-020/trung-gian/method_evidence/runs/microrank-fixture-002/anomaly-operations.csv,
results/T-020/trung-gian/method_evidence/runs/microrank-fixture-002/anomaly-traces.csv,
results/T-020/trung-gian/method_evidence/runs/microrank-fixture-002/comparison.csv,
results/T-020/trung-gian/method_evidence/runs/microrank-fixture-002/normal-iterations.csv,
results/T-020/trung-gian/method_evidence/runs/microrank-fixture-002/normal-operations.csv,
results/T-020/trung-gian/method_evidence/runs/microrank-fixture-002/normal-traces.csv,
results/T-020/trung-gian/method_evidence/runs/microrank-fixture-002/progress.jsonl,
results/T-020/trung-gian/method_evidence/runs/microrank-fixture-002/spectrum-scores.csv,
results/T-020/trung-gian/method_evidence/runs/microrank-fixture-002/summary.json,
results/T-020/trung-gian/method_evidence/runs/microrank-inputs-001/failed.json,
results/T-020/trung-gian/method_evidence/runs/microrank-inputs-001/progress.jsonl,
results/T-020/trung-gian/method_evidence/runs/microrank-inputs-002/comparison.json,
results/T-020/trung-gian/method_evidence/runs/microrank-inputs-002/failed.json,
results/T-020/trung-gian/method_evidence/runs/microrank-inputs-002/input-calculation.json,
results/T-020/trung-gian/method_evidence/runs/microrank-inputs-002/progress.jsonl,
results/T-020/trung-gian/method_evidence/runs/package-failed-001.json,
results/T-020/trung-gian/method_evidence/runs/r1s-re2tt5-cham-tinh-tay.json,
results/T-020/trung-gian/method_evidence/runs/replay-01-t-013-stderr.txt,
results/T-020/trung-gian/method_evidence/runs/replay-01-t-013-stdout.txt,
results/T-020/trung-gian/method_evidence/runs/replay-02-t-014-stderr.txt,
results/T-020/trung-gian/method_evidence/runs/replay-02-t-014-stdout.txt,
results/T-020/trung-gian/method_evidence/runs/replay-03-t-015-stderr.txt,
results/T-020/trung-gian/method_evidence/runs/replay-03-t-015-stdout.txt,
results/T-020/trung-gian/method_evidence/runs/replay-04-t-016-stderr.txt,
results/T-020/trung-gian/method_evidence/runs/replay-04-t-016-stdout.txt,
results/T-020/trung-gian/method_evidence/runs/replay-05-t-016-stderr.txt,
results/T-020/trung-gian/method_evidence/runs/replay-05-t-016-stdout.txt,
results/T-020/trung-gian/method_evidence/runs/replay-06-t-016-stderr.txt,
results/T-020/trung-gian/method_evidence/runs/replay-06-t-016-stdout.txt,
results/T-020/trung-gian/method_evidence/runs/replay-07-t-017-stderr.txt,
results/T-020/trung-gian/method_evidence/runs/replay-07-t-017-stdout.txt,
results/T-020/trung-gian/method_evidence/runs/replay-08-t-018-stderr.txt,
results/T-020/trung-gian/method_evidence/runs/replay-08-t-018-stdout.txt,
results/T-020/trung-gian/method_evidence/runs/replay-09-t-014-stderr.txt,
results/T-020/trung-gian/method_evidence/runs/replay-09-t-014-stdout.txt,
results/T-020/trung-gian/method_evidence/runs/replay-10-t-014-stderr.txt,
results/T-020/trung-gian/method_evidence/runs/replay-10-t-014-stdout.txt,
results/T-020/trung-gian/method_evidence/runs/replay-11-t-015-stderr.txt,
results/T-020/trung-gian/method_evidence/runs/replay-11-t-015-stdout.txt,
results/T-020/trung-gian/method_evidence/runs/replay-12-t-017-stderr.txt,
results/T-020/trung-gian/method_evidence/runs/replay-12-t-017-stdout.txt,
results/T-020/trung-gian/method_evidence/runs/replay-13-t-018-stderr.txt,
results/T-020/trung-gian/method_evidence/runs/replay-13-t-018-stdout.txt,
results/T-020/trung-gian/method_evidence/runs/replay-14-t-014-stderr.txt,
results/T-020/trung-gian/method_evidence/runs/replay-14-t-014-stdout.txt,
results/T-020/trung-gian/method_evidence/runs/replay-15-t-014-stderr.txt,
results/T-020/trung-gian/method_evidence/runs/replay-15-t-014-stdout.txt,
results/T-020/trung-gian/method_evidence/runs/replay-16-t-015-stderr.txt,
results/T-020/trung-gian/method_evidence/runs/replay-16-t-015-stdout.txt,
results/T-020/trung-gian/method_evidence/runs/replay-copy-audit.json,
results/T-020/trung-gian/method_evidence/runs/runtime-detail-summary.json,
results/T-020/trung-gian/method_evidence/runs/selected-summary.json,
results/T-020/trung-gian/method_evidence/runs/simplerca-arithmetic-001.json,
results/T-020/trung-gian/method_evidence/runs/simplerca-comparison-001.json,
results/T-020/trung-gian/method_evidence/runs/t013-window-root/runs/sua-R1-20261004-213933/checks.json,
results/T-020/trung-gian/method_evidence/runs/t013-window-root/runs/sua-R1-20261004-213933/manifest.json,
results/T-020/trung-gian/method_evidence/runs/t013-window-root/runs/sua-R1-20261004-213933/per-case.csv,
results/T-020/trung-gian/method_evidence/runs/t013-window-root/runs/sua-R1-20261004-213933/per-metric.csv,
results/T-020/trung-gian/method_evidence/runs/t013-window-root/runs/sua-R1-20261004-213933/rankings.json,
results/T-020/trung-gian/method_evidence/runs/t013-window-root/runs/sua-R1-20261004-213933/script.py,
results/T-020/trung-gian/method_evidence/runs/t013-window-root/runs/sua-R1-20261004-213933/summary.json,
results/T-020/trung-gian/method_evidence/runs/t013-window-root/runs/sua-R1-20261004-213933/tien-do.jsonl,
results/T-020/trung-gian/method_evidence/runs/t013-window-root/runs/sua-R1-20261004-213933/variants.csv,
results/T-020/trung-gian/method_evidence/runs/t013-window-root/trung-gian/cua-so-delay-ca.csv,
results/T-020/trung-gian/method_evidence/runs/t013-window-root/trung-gian/cua-so-delay-metric.csv,
results/T-020/trung-gian/method_evidence/runs/t013-window-root/trung-gian/cua-so-delay-summary.json,
results/T-020/trung-gian/method_evidence/runs/t013-window-root/trung-gian/cua-so-delay-variants.csv,
results/T-020/trung-gian/method_evidence/runs/torai-arithmetic-001.json,
results/T-020/trung-gian/method_evidence/runs/torai-full-goc-001.json,
results/T-020/trung-gian/method_evidence/runs/torai-full-sua-001.json,
results/T-020/trung-gian/method_evidence/runtime-ledger.csv,
results/T-020/trung-gian/method_evidence/runtime.csv,
results/T-020/trung-gian/method_evidence/scripts/build_method_evidence.py,
results/T-020/trung-gian/method_evidence/scripts/circa_graph_copy.py,
results/T-020/trung-gian/method_evidence/scripts/circa_independent_copy.py,
results/T-020/trung-gian/method_evidence/scripts/circa_window_copy.py,
results/T-020/trung-gian/method_evidence/scripts/deep_replay.py,
results/T-020/trung-gian/method_evidence/scripts/final_audit.py,
results/T-020/trung-gian/method_evidence/scripts/gdn_analysis_copy.py,
results/T-020/trung-gian/method_evidence/scripts/gdn_independent_copy.py,
results/T-020/trung-gian/method_evidence/scripts/guarded_runner.py,
results/T-020/trung-gian/method_evidence/scripts/harness_input_only.py,
results/T-020/trung-gian/method_evidence/scripts/microrank_independent_copy.py,
results/T-020/trung-gian/method_evidence/scripts/microrank_inputs_copy.py,
results/T-020/trung-gian/method_evidence/scripts/package_handoff.py,
results/T-020/trung-gian/method_evidence/scripts/prepare_additional_replays.py,
results/T-020/trung-gian/method_evidence/scripts/prepare_all_replays.py,
results/T-020/trung-gian/method_evidence/scripts/prepare_replays.py,
results/T-020/trung-gian/method_evidence/scripts/retry_supported_environment.py,
results/T-020/trung-gian/method_evidence/scripts/run_additional_replays.py,
results/T-020/trung-gian/method_evidence/scripts/run_all_replays.py,
results/T-020/trung-gian/method_evidence/scripts/run_retry_replays.py,
results/T-020/trung-gian/method_evidence/scripts/runtime_details.py,
results/T-020/trung-gian/method_evidence/scripts/selected_recompute.py,
results/T-020/trung-gian/method_evidence/scripts/simplerca_compare_copy.py,
results/T-020/trung-gian/method_evidence/scripts/simplerca_independent_copy.py,
results/T-020/trung-gian/method_evidence/scripts/t013_window_copy.py,
results/T-020/trung-gian/method_evidence/scripts/torai_full_independent_copy.py,
results/T-020/trung-gian/method_evidence/scripts/torai_s9_copy.py,
results/T-020/trung-gian/method_evidence/selected-root-checks.csv,
results/T-020/trung-gian/method_evidence/window-parameters.csv,
results/T-020/trung-gian/method_evidence/yeu-cau-hop-nhat.csv,
results/T-020/trung-gian/root/application-audit-final.csv,
results/T-020/trung-gian/root/application-audit.csv,
results/T-020/trung-gian/root/g1-coverage.json,
results/T-020/trung-gian/root/g1-occurrences.csv,
results/T-020/trung-gian/root/independent-counts.csv,
results/T-020/trung-gian/root/numeric-inventory-exclusions.json,
results/T-020/trung-gian/root/numeric-leaves.csv,
results/T-020/trung-gian/root/proposal-correction-sections.csv,
results/T-020/trung-gian/root/root-code-check-failed-001.txt,
results/T-020/trung-gian/root/root-code-checks.csv,
results/T-020/trung-gian/root/root-cost-checks.csv,
results/T-020/trung-gian/root/supplemental-inputs.json,
results/T-020/trung-gian/root/v1-override-applied.json,
results/T-020/trung-gian/root/v1-semantic-root-sample.csv,
results/T-020/yeu-cau-dau-vao-hop-nhat.csv,
tasks/T-020-tong-hop-g1/LOG.md,
tasks/T-020-tong-hop-g1/SPEC.md,
và kết quả `git diff 5636b6984dd5acae8a6de56f26d182f8867d1e56` nếu có.
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


## Phiên 2 — 04/10/2026 — Codex — Windows 11 laptop — người làm, bước 7

Mở phiên: Minh giao tự soát độc lập trước khi mở REVIEW, rồi kiểm từng điểm và ghi phản hồi. Intent EXECUTE chỉ cho LOG (ghi thêm) và bảng cuối REVIEW; không sửa STATE hay bất kỳ đầu ra/tài liệu chung nào. Đã đọc AGENTS, STATE, toàn bộ SPEC và LOG; dòng T-020 đang chờ phản biện là trạng thái bàn giao trước phiên này. REVIEW chưa mở. Hai luồng trợ lý chỉ đọc hỗ trợ kiểm phương pháp và dataset/split; root kiểm bằng chứng và ghi kết luận, không thay reviewer Claude.

Quyết định của Minh trong phiên: phạm vi chỉ hai file trên theo yêu cầu bước 7; chưa duyệt sửa các lỗi nội dung hoặc quyết định G1. Giữ cột Minh quyết trống.

### Tự soát độc lập — ghi TRƯỚC khi mở REVIEW.md

Tại lúc ghi mục này, root và hai trợ lý chưa đọc REVIEW T-020. Đã đọc SPEC/LOG như nguồn cần kiểm, không dùng tổng kết LOG làm chứng minh. Đọc/parse đủ 297 file kết quả T-020 theo định dạng; các bảng lớn đọc toàn trong RAM, kiểm cấu trúc và đối chiếu những đại lượng/nhận định quan trọng với nguồn. Đọc byte không được gọi là đã kiểm khoa học mọi hàng. Code, công thức, schema/nhãn, splits, runners, nguồn DT18 và advisor được soi ở các phần liên quan; không đọc archive RCA cũ hoặc data/locked. Không chạy lại writer của T-020 hay phương pháp trên dữ liệu mới.

Danh sách tự tìm được (FACT trừ chỗ ghi OPEN/CANDIDATE):

- **S1 — CHẶN V5: sai biến thể SimpleRCA metric rule ở 6 cặp.** `scripts/hop_nhat.py:55` đặt need metric nhưng nhánh `:69–70` hạ modality cho mọi SimpleRCA trừ trace/log. CSV 04 dòng 1369, 1371, 1375, 1376, 1385, 1386 vẫn ghi cần adapter trên Nezha OB/TT trace+log, DeepTraLog raw/processed và TRCA TT/OB trace+log dù thiếu resource metric. Root đếm lại đúng 6 hàng; đối chiếu `results/T-017/yeu-cau-dau-vao.csv:10`, `src/simplerca/core.py:62–79`. Hạ metric rule sang log/trace đổi thuật toán, không chỉ adapter. Q-33: có thể dựng latency từ trace, nhưng cần đề xuất tín hiệu mới chưa kiểm; processed event graph còn thiếu time-series/window. Đề xuất giới hạn nhánh giảm modality cho các cấu hình M4 tổng hợp; sáu ô không chạy được với đúng tín hiệu hiện có, hoặc giữ một đề xuất dẫn xuất riêng ở mức chưa kiểm. Không tự quyết thay Minh.
- **S2 — CHẶN mức bằng chứng V5: 95 cặp dùng tín hiệu dẫn xuất chưa kiểm được nâng thành cần adapter.** Root đếm CSV 04 theo trạng thái và lý do: BARO 15, N-Sigma 10, BOCPD 5, CIRCA 40, TORAI 5, RCD 5, GDN 15. Nhánh `hop_nhat.py:71–72` ghi CANDIDATE/chưa kiểm nhưng không đổi trạng thái mặc định; trái định nghĩa `04-phuong-phap-x-dataset.md:5` rằng tín hiệu và đường chuyển đã xác nhận. Q-33: trace có duration có thể sinh latency, nhưng chưa chứng minh cadence, phép gộp service/operation, normal coverage và điều kiện phương pháp. Lỗi là mức khẳng định, không bằng chứng các cặp không thể chạy. Đề xuất giữ mô tả ứng viên và chuyển trạng thái sang chưa kiểm; không cần chạy dữ liệu mới để sửa mô tả.
- **S3 — KHÔNG CHẶN: FACT biên RE1-SS quá rộng.** `03-task-cham-duoc-va-che-do-b.md:11`, `trung-gian/dataset_evidence/task-matrix.csv:6`, `leakage-data.csv:34` và template `build_evidence.py:121–122` nói tất cả metric midpoint=injection. Root tính từ `results/T-019/inspection/boundaries.csv`: 123/125 đúng; catalogue_disk_3 dòng 39 midpoint -37 s, end +286 s; user_mem_1 dòng 122 midpoint -57 s, end +246 s. Cả hai start -360 s. Q-33: hậu sự cố ngắn giải thích midpoint lệch; không cần suy exporter hoặc onset. Mốc vẫn suy start+360, nên kết luận chưa blind giữ nguyên. Đề xuất nêu 123/125 và hai ngoại lệ; không đổi split.
- **S4 — KHÔNG CHẶN: mô tả kiểm TORAI đã lỗi thời.** `07-danh-sach-phuong-phap-va-doc-nhanh.md:75` nói không tái chạy toàn Psi-PC. Nhưng `ca-da-chay.csv:6–7`, deep-source-audit/HANDOFF và `runs/torai-full-{goc,sua}-001.json` có full independent causal replay: cột, bins, F-neighbors, p-values, fallback/ranks đều đối chiếu. Root đọc kết quả: bản gốc các cụm có 50/28/0 lần PC; bản sửa 24/34/43; ranks_cuoi=True, sai lệch p-value tối đa khoảng 8e-15. Q-33: có thể câu cũ chỉ muốn nói không gọi code tác giả, nhưng giới hạn ghi không phản ánh replay độc lập đã làm. Đề xuất ghi đúng một ca TX2/window/seed, không suy toàn dataset hoặc tương đương bài.
- **S5 — KHÔNG CHẶN: lệnh/nguồn chi phí RCD/TORAI phụ thuộc đường trên máy.** `scripts/root_cost_audit.py:12–16`, runtime.csv, root-cost-checks.csv và phụ lục 10 dẫn D:/RCA-ext/work/T-016/.../meta.jsonl. Nghi ngờ ban đầu rằng dữ liệu không nằm trong repo đã bị bác: root đọc member metadata trong RAM từ `results/T-016/runs/s11-ket-qua-ec2.tar.gz` và `s11-ket-qua-ec2-tt30.tar.gz`; byte hash khớp supplemental-inputs, số dòng 90/30/30/30, tổng giây 5623.3043326419975 / 1481.5980411359924 / 45.16271692498776 / 65.6531029810103. Đây chỉ là hạn chế citation/lệnh tái lập, không lỗi số hay thiếu dữ liệu. Đề xuất trỏ archive/member và đọc member trực tiếp, không sao/tải timer mới.

Kiểm đạt và giới hạn:

- Đếm lại 3248 hàng kiểm: 3235 MATCH, 4 MISMATCH, 9 OPEN; số này mô tả bảng kiểm, không chứng nhận tự tính lại toàn 3248 phép trong phiên này. 40 phần × 42 hàng = 1680; cả 42 hàng/16 trường khớp sáu bảng nguồn, 27 hàng chua_kiem giữ nguyên.
- Ba split A/B/C có 438/365/473 hàng, toàn ô cùng phía, không TX2 ngoài dev. Census/seed/allowlist và 60 ca locked được kiểm bằng metadata công khai, không mở locked. Ledger 1417 identity units không gọi thành physical incidents; alias RE1-OB còn OPEN và tránh test.
- Root tìm lại 533 occurrence trên source files và đối chiếu exact source với 08: 533/533, không coi mechanical coverage là kiểm ngữ nghĩa đầy đủ. Đếm nguồn SimpleRCA: 30 ca, tổng Hit@1 fractional 25, MRR 0.8911111111111112, khớp source. Bốn timer và 30 projection runtime được tính lại; dữ liệu runtime có trong repo.
- 297 file parse/decode không lỗi, CSV không thừa field; stderr rỗng của run thành công là hợp lệ. Hai NPY output GDN đều float64, 1436 phần tử, không là telemetry mới. Manifest đầu ra khớp trừ LOG đã được append đúng phạm vi phiên này.
- Không thấy root gold lọt thêm vào phần tổng hợp; mode a/time label, GDN test threshold/future normalization và các mapping OPEN đã tách. Dataset không được chọn bằng chi phí/điểm thắng. C9/normal/schema/license/chuyển hệ/continuous detection/độc lập bootstrap vẫn OPEN có đầu vào cần, không điền giả để đạt checklist. DT18 và advisor không buộc phải cài mọi tên dataset hay dùng PageRank ranking như detector.
- Hai truy vấn kiểm trong RAM dừng do gọi sai tên cột exposure/reciprocal_rank; đã đọc header rồi tính lại với TX/mrr_fractional, kết quả đạt. Một truy vấn metric rule dùng tên phương pháp quá hẹp cho 0 hàng; đã sửa startswith và xác nhận 6, không dùng kết quả 0 làm bằng chứng. Không có artifact bị ghi bởi các lượt này; dấu vết thất bại ghi ở đây, output công cụ còn giữ trong phiên.

**Tiêu chí xong:** đầu ra/census/split/pins/nhãn có bằng chứng; tuyên bố đủ V5 cần được thu hẹp/sửa theo S1–S2 trước dùng ma trận để chốt G1. S3–S5 không đổi số liệu/role/split cốt lõi. Chưa thay trạng thái task hoặc quyết định vật chất nào. Danh sách này được khóa theo thứ tự thời gian trong LOG; chỉ sau mục này mới mở REVIEW để so sánh.

### Đối chiếu REVIEW — 05/10/2026 (UTC+7), sau tự soát

Sau khi S1–S5 đã nằm trong LOG, root mới mở REVIEW. Trợ lý dataset hoàn tất đọc bổ sung toàn các script/handoff/run của hai luồng, không có finding mới; trợ lý này chưa đọc REVIEW trong phần tự soát bổ sung. Sau đó hai trợ lý hỗ trợ kiểm R2–R6 chỉ đọc; root đối chiếu nguồn và tính lại các đại lượng trọng yếu. Bảng cuối REVIEW đã điền R1–R6, ghi chú DA reviewer nêu, và N1–N5 tương ứng S1–S5; mọi ô Minh quyết để trống. Nội dung phản biện gốc được giữ nguyên.

Kết luận của người làm (ý kiến phản hồi, chưa phải quyết định Minh):

1. **R1: đúng một phần; CHẶN.** (a) Đúng: `docs/MRP.md:120`, `docs/knowledge/K2-du-lieu.md:15–17,26` ghi v1 đọc thống kê trace cả 90 RE2-TT. Việc K2 ghi chưa kiểm lại không xóa lịch sử tiếp xúc. 60 ca khóa là TX1 theo định nghĩa T-020, không TX0. Điều không thay đổi là chưa thấy method-result, nên MRP vẫn cho làm test. Ledger bỏ nguồn v1 ngoài results, independent_validate đồng thời assert chỉ có public-census: phạm vi sửa rộng hơn prose/split. (b) Đúng về thiếu khai báo: root đọc aggregate thật, 52.335 hàng Nezha ứng với 56 OB/45 TT label-event; Eadro 54.999 hàng injection ứng với 36 SN/81 TT tuple root/fault/start/duration. Đơn vị Eadro là injection tuple, không số archive/session (SN 4 session và TT 9 session trong probe). Có exceed và root gắn từng ca. Nhưng Nezha scope ghi root thêm sau aggregation; đây là probe 3q theo P2/C7, không bảng detector streaming hoặc root-ranking đã xác lập. Phân loại TX1/TX2 của probe này còn OPEN, owner Minh, input định nghĩa method-result trong D3 và phạm vi probe đã đọc; không tự nâng lên TX2 hoặc kết luận mọi ca không được làm test. Phản hồi tự soát trước đó xác nhận 60 TX0 chỉ đối chiếu sổ hiện tại đã thiếu nguồn, không chứng nhận lịch sử tiếp xúc; đánh giá đó được thu hẹp tại đây.
2. **R2: đúng một phần; CHẶN.** Thiếu tổng hợp vị trí root/định nghĩa trong D2 và lý do vai trò Eadro-TT là thật. Reviewer quá rộng ở mọi C5 cùng OPEN: chỉ 4/40 có đúng chuỗi trích; C5 Eadro/Nezha đã dẫn bậc, nhưng chưa tổng hợp khả năng phân xử theo vị trí. Nezha root-mapping chỉ alias, bậc thật ở T008 evidence-002 summary.root_windows (hai clock, không 202 incident độc lập). Root tính Eadro từ 117 hàng: SN 33/36 root_present, TT 54/81; TT 9/27 root vắng, 3 root có mặt nhưng bậc 0/0. Nhiều root không chứng minh đồ thị tốt hơn, graph whole-file không injection-time graph. Aliasing, missing instrumentation, clock/window và workload là lời giải thích khác. Không tự gọi root vắng là isolate hoặc đưa Eadro-TT vào gói chỉ vì có 27 root. Đề xuất tận dụng bậc đã có, trình định nghĩa và lý do TT/SN; không cần thêm phương án thứ tư nếu so TT như lựa chọn trong các gói hiện có là đủ.
3. **R3: đúng một phần; CHẶN.** Có FACT từng trục nhưng 40 c9_state cùng OPEN, thiếu kết luận theo cặp/trục và định nghĩa khác stack trong D2. Eadro khác danh sách tác giả và framework injector; stack chung Jaeger/cAdvisor/Prometheus/ES. Nezha khác tác giả/runtime code injector, resource/network exact injector OPEN; stack có phần chung RCAEval. Không tự quyết common open-source components nghĩa là đạt/trượt cả stack. “Chưa chứng minh 3/3” vẫn đúng như chưa biết, không phải chứng minh thế giới không có bộ độc lập. C9 khác điều kiện giữ ngoài của SPEC/MRP; template prose hiện nhập nhằng. Reviewer nói RE3-OB bị loại quá rộng: B vẫn giữ 30 ca giu-ngoai-ung-vien. Normal/chất lượng/adapter/candidates còn OPEN ngoài schema, nên không thể gọi baseline ready chỉ từ schema công bố. 42 hàng mỗi Bank/RE3-OB đã giữ yêu cầu/normal/budget; cần thêm tóm tắt tương thích CANDIDATE có điều kiện, không hạ độ chắc của “chưa kiểm” một cách tùy ý.
4. **R4: đúng; KHÔNG CHẶN.** Root tính từ split: A RE3-TT f3/f4 chỉ test 4 ô/16 ca; B RE3-SS f2/f3 4 ô/13 ca; C RE1-TT cpu 5 ô/25 ca; C RE3-OB f2/f5 3 ô/9 ca. 1/3 đã ghi tiên nghiệm nhưng thiếu lý do và hệ quả tại D3. Không viết bổ sung như FACT rằng tỷ lệ bắt nguồn v1 nếu không có bằng chứng chọn đó. Giữ split để đánh khái quát sang fault chưa thiết kế có thể là một phương án hợp lệ nếu Minh chọn; phân tầng bảo đảm dev thấy fault là phương án khác, không mặc nhiên tốt hơn. Nó thay mục tiêu khái quát hóa/cân bằng ô/test size và vẫn phải giữ TX2 ép dev, whole-cell. Chưa đổi gì.
5. **R5: đúng một phần; KHÔNG CHẶN.** Root đọc T005 dòng timer và crop code 300+300 điểm; 1440.133 s là số đo một ca. Phép chiếu 30 ca 12.001108 h/90 ca 36.003325 h khớp T013 chi-phi-va-sentinel. Toàn dev 12 h chưa đo, phải ghi CANDIDATE cùng giả định T/d/máy/library/load. D1/D5 thiếu các lựa chọn để Minh quyết budget/completeness; phụ lục là đề xuất chưa duyệt, chưa phải tự đổi Q-40. Giảm window/cột riêng đổi điều kiện và detector, lấy mẫu ca riêng đổi denominator, chuyển máy/chia lượt không reset 3 h. Window 1200-point chưa có timer; crop có mốc không chứng minh runtime chế độ b liên tục.
6. **R6: đúng một phần; KHÔNG CHẶN.** Cần nối WHY-04/05 hiện hành vào D1/D3, WHY-16 vào D5 (cấu hình tái lập riêng), WHY-19/20 vào D1 (variant/seed), không chỉ snapshot T003 trong 08. Nhưng de-xuat:72 đã nhận biết WHY19/20/Q57 và WHY05 cho phép đổi giao thức có lý do: không tự kết luận mọi bản sửa trái toàn WHY05. Phạm vi thật rộng hơn reviewer: nháp đổi heading WHY19/20 thành lý do kiểm cơ chế thu hẹp nội dung P3 đã được Minh duyệt ghi. Q57 ghi áp đề xuất P3 bản TORAI/seed; WHY vẫn nói Đề xuất G1, Minh duyệt ghi. Phải giữ hai lớp này, không biến thành diagnostic giống WHY18 hoặc tự nâng DECIDED. Nội dung cần trình rõ TORAI ít nhất 3 seed và RCD số seed vừa Q40, không nói chỉ “chọn từ nguồn”.
7. **Ghi chú DA reviewer: đúng; KHÔNG CHẶN.** Root đọc code ghim graph_heads/rht.py:348–365: chỉ RHTScorer, không DAScorer. Câu vai trò chung trong 07 không đúng cho tất cả variant dù Defaults đã tách. Sửa mô tả theo variant, giữ DA cho +DA và bài; không cần rerun score.

**N1/N2 là hai lỗi CHẶN mới reviewer không nêu; N3/N4/N5 không chặn.** Chúng được ghi S1–S5 trước khi mở REVIEW, không phải bổ sung do đọc reviewer. Không bác toàn bộ finding nào: R4 đúng đầy đủ, R1/R2/R3/R5/R6 đúng một phần vì phạm vi hoặc mức khẳng định của reviewer cần thu hẹp. Nghi ngờ nguồn timer thiếu trong repo bị bác bằng byte và tổng trong tar, giữ N5 chỉ về citation/lệnh tái lập.

### Đề xuất sửa gom theo file — CANDIDATE, CHƯA DUYỆT/CHƯA THỰC HIỆN

Đây là bản đồ ảnh hưởng để Minh chọn sửa. Không phải quyền chạy lại generator hoặc ghi mọi file của SPEC. Sửa nguồn sinh trước, sau đó đồng bộ đầu ra phụ thuộc; giữ failed runs/snapshot lịch sử. Các lựa chọn tỷ lệ/phân tầng, vị trí, stack, TX của probe và vai trò test còn OPEN do Minh quyết; chỉ sửa số liệu/mô tả đã có bằng chứng không tự chọn những phương án này. Không thêm quy trình, cổng hay phép kiểm mới.

Các đường dẫn ở bảng dưới tương đối với D:/RCA-flashticket. Hai cột đầu ghi file cụ thể và cũ → mới đề xuất; cột cuối nêu ảnh hưởng/lý do. Các file results đều thuộc T-020, không đề nghị sửa task cũ hoặc docs chung trong gói sửa này.

| File nguồn hoặc bản chính | Cũ → mới đề xuất | Ảnh hưởng/lý do |
|---|---|---|
| `results/T-020/trung-gian/exposure_ledger/build_ledger.py` | Nguồn results-only, locked60 TX0 → thêm nguồn tiếp xúc v1 MRP/K2 đã có, locked60 TX1 nhưng ran/rank/detector False. Ghi scope probe 3q gắn root trong nguồn/ambiguity; TX của probe theo Minh chọn | R1; sửa lịch sử tiếp xúc, không mở khóa và không đưa nhãn vào method |
| `results/T-020/trung-gian/exposure_ledger/independent_validate.py` | Assert locked60 TX0/chỉ public-census → assert tiếp xúc v1 TX1 có đúng nguồn, tách khỏi điều kiện không method-result; giữ 60 identity và allowlist | R1; sửa nghĩa của các phép kiểm đã có, không tạo phép kiểm mới |
| `results/T-020/scripts/chia_theo_o.py` | C tên/claim test chỉ TX0 nhưng chứa RE2-TT; giữ ngoài thiếu C9 → theo Minh chọn: giữ RE2-TT test TX1 và đổi tên/claim C, hoặc C chỉ TX0 thì bỏ RE2-TT test; tách C9 khỏi điều kiện giữ ngoài. Chỉ đổi tỷ lệ/phân tầng nếu Minh chọn R4 | R1/R3/R4; whole-cell/không TX2 test giữ nguyên, không chọn dựa score |
| `results/T-020/scripts/hop_nhat.py` | Nhánh reduced-modality áp metric rule; CANDIDATE latency vẫn cần adapter → giới hạn giảm modality cho M4 tổng hợp, metric rule thiếu tín hiệu ghi không chạy với input hiện có hoặc dẫn xuất chưa kiểm; 95 cặp latency đã đếm chuyển chưa kiểm. Thêm nguồn/normal/budget tương thích dự kiến giữ ngoài nếu có nguồn công bố | N1/N2/R3; không tuyên bố derived metric không thể dùng hay đồng nhất resource metric |
| `results/T-020/trung-gian/dataset_evidence/build_evidence.py` | RE1SS mọi midpoint bằng injection, C5 chưa tổng hợp vị trí, exposure RE2TT TX0 → nêu 123/125 và hai hậu ngắn; tổng hợp bậc quan sát đã có từ nguồn, chưa tự gán lá/hub; cập nhật exposure từ ledger đã sửa | N3/R1/R2; giữ root vắng/0-degree, whole-file/two-clock, causal propagation OPEN |
| `results/T-020/trung-gian/dataset_evidence/build_provenance.py` | C9 một OPEN giống nhau, exposure/schema provenance cũ → kết luận từng trục theo cặp từ nguồn hiện có: khác/trùng/trùng một phần/OPEN; ghi câu stack chờ Minh và tách giữ ngoài; cập nhật tiếp xúc/schema scope | R1/R3; không tự công nhận độc lập 3/3 |
| `results/T-020/trung-gian/method_evidence/scripts/build_method_evidence.py` | Vai trò DA chung cả variant không DA, mô tả TORAI arithmetic-only → role theo variant, TORAI có full independent replay đúng ca/window/seed; giữ điều kiện chưa tương đương bài | N4/ghi chú DA; mô tả bằng chứng, không đổi thuật toán |
| `results/T-020/scripts/root_cost_audit.py` | Chỉ mở timer bằng D:/RCA-ext → đọc metadata member trong hai tar T016 đã có, dùng cùng phép tổng/đếm/chiếu | N5; tái lập từ repo, không download/copy timer hoặc benchmark mới |
| `results/T-020/scripts/governance_inventory.py` | WHY04/05 chỉ đi vào sổ qua snapshot → nối các WHY04/05/16/19/20 hiện hành vào thẻ, giữ provenance snapshot/historical và Q57 | R6; không thêm gate hoặc tự đổi trạng thái lựa chọn |
| `results/T-020/scripts/refine_text.py` | Nháp đổi WHY19/20 thành lý do kiểm cơ chế → giữ đúng đề xuất P3/Q57, thêm crosswalk giữ/sửa/thay sau Minh chọn | R6; tránh lần sinh lại phục hồi nháp thu hẹp sai |
| `results/T-020/scripts/final_audit.py` | Expected counts/status cũ → đối chiếu counts/output hiện hành sau những sửa được duyệt, giữ phạm vi và kiểm đã có | Số 877/728/825/127 có thể đổi sau mapping/ma trận; không sửa verifier để giấu lỗi |
| `results/T-020/g1-goi-quyet-dinh.md` | C/test-TX0 và heldout-C9 nhập nhằng, D2 thiếu vị trí/EadroTT/stack, D3 thiếu probe/tỷ lệ, D1/D5 thiếu budget/crosswalk → đưa bằng chứng và câu Minh quyết từ R1–R6, giữ lựa chọn CANDIDATE/chờ WHY; nêu N1/N2 là giới hạn ma trận trước sửa | Tác động trực tiếp việc chốt G1, không chốt thay Minh |
| `results/T-020/06-phuong-an-dataset-va-chia.md` | RE2TT test TX0, bỏ EadroTT không lý do, giữ ngoài chưa đủ C9 → cập nhật theo lựa chọn R1/R3/R4, so TT/SN theo C1–C9 và coverage/clock, nêu fault vắng dev và lý do ratio thực | R1/R2/R3/R4; không tự thêm TT vì số root nhiều |
| `results/T-020/02-so-ca-da-nhin.md`, `.csv` | TX0 RE2TT60 và descriptive chung → TX1 có nguồn v1 và probe scope rõ; giữ unique-identity và method-result flags | R1; thay tiếp xúc, không thay physical incident count |
| `results/T-020/01-bang-tieu-chi-hop-nhat.md`, `.csv` | C5/C9 và exposure diễn giải cũ → đồng bộ bậc/nguồn/trục/tiếp xúc sau sửa nguồn sinh | R1/R2/R3; root count không thay phân loại vị trí |
| `results/T-020/03-task-cham-duoc-va-che-do-b.md` | Mọi RE1SS midpoint bằng injection → 123/125, hai hậu ngắn; vẫn lộ start+360 | N3; không đổi kết luận mode b |
| `results/T-020/04-phuong-phap-x-dataset.md`, `.csv` | 6 metric-rule và 95 CANDIDATE gán cần adapter → đồng bộ trạng thái/adapter/số hàng theo sửa source; thêm dự kiến giữ ngoài có điều kiện | N1/N2/R3; không chạy data mới để lấp ô |
| `results/T-020/05-nhan-va-cua-so.md` | WHY/window/budget chưa nối rõ → tách author-reference WHY16 và common window, nêu budget BOCPD cùng giả định; nhãn/probe theo lựa chọn Minh | R5/R6; không đổi một window riêng để thắng hoặc fit quota |
| `results/T-020/07-danh-sach-phuong-phap-va-doc-nhanh.md` | TORAI giới hạn chưa chạy toàn Psi-PC; DA generic → phạm vi full independent replay một ca và DA theo variant | N4/DA; tránh suy kiểm toàn dataset |
| `results/T-020/08-so-chuyen-g1.csv` | Mapping current WHY/vị trí chưa tới câu hỏi thẻ → nối nguồn hiện hành tới D1/D2/D3/D5, giữ snapshot như lịch sử | R2/R3/R6; coverage cơ học không thay câu trả lời thẻ |
| `results/T-020/10-ke-hoach-p3-de-xuat.md` | Timer path theo máy, BOCPD thiếu lựa chọn rõ trong thẻ → trỏ tar/member, nguồn/12h scenario chưa kiểm và lựa chọn budget/completeness theo Minh | N5/R5; không tự bỏ baseline hoặc sửa Q40 |
| `results/T-020/de-xuat-tai-lieu-chung.md` | Nháp heading WHY19/20 thu hẹp sai, WHY crosswalk thiếu → giữ đề xuất P3/Q57 và thêm map giữ/sửa/thay đúng quyết định G1 sau này | R6; docs/WHY và DECISIONS vẫn chưa sửa |
| `results/T-020/dinh-chinh-task-cu.md` | Đoạn tự kiểm nói metric-rule đã đúng và claims tiếp xúc cũ → ghi đính chính lỗi T020 cùng bằng chứng R1/N1/N2/N3/N4; giữ lịch sử nguồn task cũ | Không ghi đè hoặc sửa task khác |
| `results/T-020/09-kiem-cheo-so-lieu.md`, `.csv` | Đếm/nguồn thành phần derived cũ → tính lại các aggregate đã có sau sửa được duyệt, giữ mismatch/open/replay failures và phân biệt count với verification | N1/N2/R1/R3/N5; không thêm phép kiểm mới |

Đầu ra phụ thuộc cần đi cùng sửa nguồn (chỉ ghi khi Minh duyệt gói có những đường dẫn này, không mặc định generator được phép ghi mọi file):

- **Luồng ledger:** `results/T-020/trung-gian/exposure_ledger/02-so-ca-da-nhin.md`, `.csv`, `exposure-evidence.csv`, `public-census.csv`, `locked-public-60.csv`, `dataset-exposure.csv`, `cell-exposure.csv`, `dataset-census-membership.csv`, `dataset-membership-exposure.csv`, `source-reconciliation.csv`, `source-intersections.csv`, `numeric-leaf-pool.csv`, `numeric-check-selected.csv`, `numeric-check-all.csv`, `run-assertions.json`, `independent-assertions.json`, `input-read-manifest.json`. Chỉ nguồn/exposure/aggregate thực sự thay đổi mới cập nhật; không xóa/rewrite archive hay failed runs. Alias chưa có bằng chứng giữ OPEN, không đổi canonical identity tùy tiện.
- **Luồng dataset:** `results/T-020/trung-gian/dataset_evidence/01-bang-tieu-chi-hop-nhat.md`, `.csv`, `03-task-cham-duoc-va-che-do-b.md`, `task-matrix.csv`, `leakage-data.csv`, `root-mapping.csv`, `independence-axes.csv`, `schema-provenance.csv`, `heldout-schema-provenance.md`, `supporting.json`, `input-hashes-used.json`, `provenance-input-hashes.json`, `provenance-run.json`, `root-final-dataset-audit.md`. Bậc hiện có được tổng hợp, các vị trí categorical chưa gán cho tới khi Minh quyết.
- **Luồng phương pháp/chi phí:** `results/T-020/trung-gian/method_evidence/07-checklist-doc-nhanh.md`, `method-checklist.csv`, `runtime.csv`, `runtime-ledger.csv`; `results/T-020/trung-gian/root/root-cost-checks.csv`, `supplemental-inputs.json`. Giữ mọi replay/run và giá trị timer, bổ sung archive/member thay đường máy là nguồn tái lập chính.
- **Split/bao phủ/audit:** `results/T-020/chia-theo-o/A-da-tin-hieu.csv`, `B-kien-truc-khong-trace.csv`, `C-test-TX0.csv` (nếu đổi tên C thì phải duyệt tên đích/rename riêng); `results/T-020/runs/split-assertions.json`, `matrix-assertions.json`, `crosscheck-merge-assertions.json`, `final-audit.json`; `results/T-020/trung-gian/root/g1-coverage.json`, `g1-occurrences.csv`, `application-audit-final.csv`; `results/T-020/trung-gian/exposure_ledger/v1-semantic-overrides.csv`, `v1-semantic-assertions.json`, `v1-semantic-audit.md`. Chỉ cập nhật những hàng/đếm phụ thuộc đúng lựa chọn, không chạy lại semantic overrides mà chưa đọc phạm vi ghi.
- **Manifest:** `results/T-020/manifest.json` và các `results/T-020/trung-gian/{dataset_evidence,exposure_ledger,method_evidence}/output-manifest.json` khi nội dung được sửa. Manifest hiện là snapshot bàn giao trước REVIEW; LOG append phiên này làm hash LOG khác dự kiến. Phiên bước7 không được Minh giao ghi manifest, nên giữ snapshot, không refresh chỉ để hiện PASS.

Các điểm **chưa kiểm/OPEN** trong đề xuất sửa: số hàng trạng thái sau N1 tùy cách xử lý tín hiệu dẫn xuất; nhóm lá/giữa/hub tùy định nghĩa; C9 stack tùy cách hiểu chia sẻ thành phần; variant/seed/role/split/budget tùy Minh chọn G1. Giả định gói sửa chỉ dùng nguồn đã có và không đọc locked/raw TX1 mới; nếu thiếu source hoặc cần thay scope/đổi SPEC đã khóa thì phải trình lại đúng file/nội dung theo Luật0, không thực hiện ngoài bảng. Đề xuất nhanh/rẻ: tái sử dụng census, aggregate bậc, tar timer và replay sẵn có; không cần RCA run/EC2/tải dataset/benchmark mới để sửa các mô tả đã xác nhận. Đây là đề xuất, chưa chạy.

### Kết thúc phiên bước 7 — 05/10/2026 (UTC+7)

1. **Đã làm:** tự soát trước REVIEW, ghi S1–S5; kiểm R1–R6 bằng nguồn thật và phép tính RAM, thêm ghi chú DA và N1–N5; lập bản đồ file/đề xuất sửa. R1/R2/R3 có phần CHẶN đúng; N1/N2 CHẶN V5. R4 đúng đầy đủ; các R còn lại đúng một phần. Chưa sửa kết quả, chưa đóng task/G1.
2. **File đã thay đổi:** chỉ append `tasks/T-020-tong-hop-g1/LOG.md` và bảng cuối `tasks/T-020-tong-hop-g1/REVIEW.md`. STATE/SPEC/results/src/docs chung không đổi trong phiên. Không thêm quyết định Minh hoặc đổi trạng thái material decision; cột Minh quyết trống. Phạm vi lời giao được ghi vào LOG, không tự ghi DECISIONS chưa được phép.
3. **Kiểm và kết quả:** parse toàn 297 output không lỗi; số nguồn/split/census/42 hàng đầu vào/533 mappings/30 SimpleRCA score/timer trong tar khớp. Phát hiện 6 metric-rule/95 candidate-adapter, RE1SS 123/125 midpoint, phạm vi replay TORAI, bỏ nguồn v1 và thiếu tổng hợp C5/C9. Split script hiện hành tái lập được nhưng TX0 claim sai do source coverage thiếu; không gọi PASS đó chứng minh sổ tiếp xúc đúng. Hash nhóm 6065 file ngoài LOG/REVIEW khớp đầu phiên, REVIEW phần reviewer giữ byte, LOG phần lịch sử giữ byte; các checks kết phiên sẽ đối chiếu lại sau append. Không mở locked, không chạy lại writer/method hoặc thay dữ liệu để PASS. Hai query RAM lỗi KeyError và filter quá hẹp được ghi trong tự soát, sửa query sau đọc header; kết quả đúng dùng nguồn thật.
4. **Điều chưa chắc/cần Minh:** chọn điểm sửa và phạm vi file ở bản đồ; cách phân loại probe TX; định nghĩa vị trí/khác stack; giữ RE2TT test TX1 hay bỏ khỏi C chỉ TX0; tỷ lệ/phân tầng; xử lý BOCPD/Q40 và crosswalk WHY19/20. Người làm đề nghị sửa lỗi đã xác nhận trước dùng gói để chốt G1; chưa chọn thay Minh. Không đề nghị thêm vòng review hoặc cơ chế kiểm soát mới. Nội dung formal documentation cần cập nhật sau Minh chọn: lịch sử tiếp xúc, khả năng phân xử theo vị trí/candidates/C9, WHY bản/seed/window và ngân sách; trong phiên chỉ ghi nháp/ý kiến ở LOG/REVIEW.
5. **Bước tiếp chính xác:** Minh đọc `tasks/T-020-tong-hop-g1/REVIEW.md` bảng cuối và mục Đề xuất sửa gom theo file của LOG, chọn các sửa/lựa chọn còn OPEN. Phiên sửa tiếp theo đọc lại AGENTS, SPEC, mục cuối LOG và các source tương ứng trong bảng; chỉ sau Minh duyệt đúng phạm vi mới sửa source generator rồi derived artifacts. Không chạy `prepare_handoff.py` nguyên trạng vì nó còn ghi STATE/append báo cáo/prompt cũ. Trong phiên này không cập nhật STATE theo chỉ thị “Chưa sửa file nào khác” của Minh.
6. **Lệnh cuối:** `git diff --check`, chạy sau truy vấn chỉ đọc trong RAM so nhóm hash, prefix LOG/REVIEW và cột Minh quyết. Các số/hash chi tiết ở manifest snapshot và output công cụ; không rải hash trong văn xuôi. Đề xuất commit nếu Minh yêu cầu ở bước sau: `docs(T-020): ghi tự soát và phản hồi phản biện G1`; chưa commit/push.


## Phiên 3 — 05/10/2026 — Codex — Windows 11 laptop — người làm, bước 7

Mở phiên: Minh trả lời “CHỐT SỬA” cho đề xuất ngay trước đó: chỉnh các dòng R2/R3/N1/N2 trong bảng người làm của REVIEW và ghi thêm đính chính/cập nhật đề xuất trong LOG. Intent EXECUTE; phạm vi được duyệt đúng hai file này. Đã đọc AGENTS, STATE, SPEC và mục cuối LOG; T-020 vẫn đang ở bước phản hồi. Nguồn đã kiểm của lượt chỉ đọc trước còn nguyên, dùng lại các phép đếm và đối chiếu code; không chạy phương pháp mới.

Quyết định của Minh trong phiên (USER_CONFIRMED): duyệt ghi cập nhật phản hồi theo đề xuất hai file. Cột Minh quyết tiếp tục để trống đúng đề xuất đã duyệt; các lựa chọn nghiên cứu G1 chưa được chốt bởi lệnh này.

### Đính chính phản hồi phiên 2 sau phản biện lại

Mục này cập nhật ý kiến người làm của phiên 2; giữ nguyên lịch sử tự soát S1–S5 và thứ tự trước/sau mở REVIEW. Bốn dòng R2/R3/N1/N2 ở bảng người làm đã chỉnh theo đề xuất Minh duyệt. R1/R4/R5/R6, ghi chú DA và N3/N4/N5 không đổi.

1. **R2 — giữ nội dung và mức CHẶN.** Tự đọc toàn C5 của `results/T-020/01-bang-tieu-chi-hop-nhat.csv`: 40/40 hàng chưa kết luận vị trí, 39 giao P3 hoặc G1/P3, riêng Bank dòng 28 tới G3. Số 4/40 chỉ là số hàng chứa nguyên câu trích, không thu hẹp finding. Bậc Nezha nằm ở `results/T-008/runs/evidence-002/summary.json` root_windows, không ở bảng alias. Tự tính từ `results/T-009/runs/inspect-004/root-degree-whole-file.json` vẫn khớp SN 33/36 ca có root trong trace; TT 54/81, 9/27 root vắng và 3 root có mặt nhưng bậc 0/0. Các ca này có ích cho giả thuyết P4 tại `docs/MRP.md:174`; không là lý do tự bỏ Eadro-TT. Reviewer không nói TT tốt hơn SN; Codex đã thêm một phản bác không cần thiết. Giới hạn vẫn phải ghi: root_present chỉ xét trace.services, cạnh là hợp toàn file, alias/instrumentation/clock/window/coverage còn có thể giải thích; chưa chứng minh thiếu metric/log hoặc cơ chế xếp sai. OPEN hợp lệ của TX0/giữ ngoài hoặc tác vụ thiếu gold không bị lấp bằng suy đoán.
2. **R3 — giữ nội dung và mức CHẶN.** REVIEW gốc dòng 51 nói “theo đúng quy tắc SPEC… chỉ thiếu schema”, về điều kiện giữ ngoài. Dòng 52/55 còn yêu cầu baseline dự kiến và ghi chưa kiểm trên file; không khẳng định ready. Codex đã phản bác lệch sang readiness. Theo `tasks/T-020-tong-hop-g1/SPEC.md:24`, điều kiện là TX0, C1 và nhãn/schema; không tự thêm C9, normal/chất lượng/mapping. Ba mục sau là giới hạn khi chạy phương pháp, báo riêng. Chữ “loại” của reviewer cần đính chính vì CSV B vẫn giữ RE3-OB 30 ca ứng viên, nhưng việc 06 hạ vai trò vì C9 và thiếu kết luận từng trục/định nghĩa stack trong D2 vẫn là lỗi. Không dùng đính chính câu chữ để làm yếu finding.
3. **N1/N2 — KHÔNG CHẶN G1.** Phạm vi 6 ô metric rule và 95 ô tín hiệu dẫn xuất khớp CSV 04. N1 ban đầu nằm ở sáu phần trace+log/event graph Nezha-OB/TT, DeepTraLog raw/processed và hai TRCA; N2 có 19 ô ở mỗi năm phần trace+log Nezha-OB/TT, DeepTraLog raw và hai TRCA. Phần metric ngày Nezha-OB có trạng thái adapter riêng cho BARO/CIRCA/N-Sigma/BOCPD/GDN/RCD, không bị hạ theo trace+log. DeepTraLog/TRCA/Nezha-TT không có trong ba cấu trúc; sửa hai lỗi không buộc đổi D1/D2/census/split đã đề xuất. Cần sửa mức bằng chứng/ý nghĩa/số tổng của V5 trước gọi ma trận chính xác; mức CHẶN V5 trong phiên 2 quá cao, không tự tạo điều kiện chặn G1 mới. R1–R3 vẫn CHẶN.
4. **N1 mở rộng thêm 42 ô sau đối chiếu reviewer.** Tự đếm CSV 04: trace factor2/factor4 mỗi 10, log threshold1/threshold10 mỗi 6, metric P95/channels mỗi 5. Nguồn cấu hình `results/T-017/scripts/run_dev.py:127` chỉ đổi một tham số mỗi biến thể. `src/simplerca/core.py:62–74`, `:75–86`, `:88–100` chỉ đọc các tham số tại nhánh metric/trace/log tương ứng; thiếu modality đó thì score/ranks/ties/status trùng primary reduced-modality, metadata config vẫn khác. `results/T-017/yeu-cau-dau-vao.csv:3–8` cho ít nhất một modality nên 42 ô vẫn chạy được. Chúng cần ghi tham số không hoạt động/tương đương primary trên phần này, không tính thành sensitivity riêng; không chuyển cả 42 sang không chạy được. Các ô đi qua SS, metric ngày, LEMMA sample và BARO-FSE, nhưng không buộc bỏ M4 primary hoặc gói B. Nhánh code liên quan là `hop_nhat.py:69–70`, không :58–59. Cách sửa cũ chỉ giới hạn reduced-modality vào M4 tổng hợp chưa bao phủ lỗi này. 42 ô do phản biện lại nêu rồi Codex kiểm, không ghi thành tự tìm trước REVIEW.

### Cập nhật đề xuất sửa theo file — chưa thực hiện các sửa đầu ra

Bản đồ file/đầu ra phụ thuộc của phiên 2 vẫn là đề xuất chờ Minh chọn, đọc cùng đính chính này. Chỉ hai file phản hồi được ghi trong phiên 3; các đề xuất sửa nội dung/code/results dưới đây chưa được lệnh “CHỐT SỬA” cho hai file phản hồi cấp quyền thực hiện.

| File | Điều chỉnh đề xuất cũ → mới | Vì sao/ảnh hưởng |
|---|---|---|
| `results/T-020/scripts/hop_nhat.py` | Giới hạn reduced-modality vào M4 tổng hợp vẫn cần cho 6 metric rule; bổ sung ghi rõ 42 sensitivity có tham số không hoạt động khi thiếu modality tương ứng. Giữ chúng là cấu hình chạy được bằng modality còn lại nhưng tương đương primary; không tạo trạng thái mới. 95 ô derived latency chuyển từ cần adapter sang chưa kiểm, giữ giả định/nguồn | N1 gồm hai lỗi khác nghĩa; sửa cũ bỏ sót 42 ô. N2 sửa mức khẳng định, không tuyên bố bất khả thi |
| `results/T-020/04-phuong-phap-x-dataset.md`, `.csv` | Đồng bộ 6/95 trạng thái và số tổng sau sửa source; 42 ô có chú thích đúng ý nghĩa sensitivity, không tự hạ trạng thái chỉ vì trùng primary | Không cộng 42 như các baseline/sensitivity độc lập; giữ đầy đủ hàng gốc/provenance |
| `results/T-020/g1-goi-quyet-dinh.md`, `06-phuong-an-dataset-va-chia.md` | R2 trình định nghĩa/vị trí/nhóm root thiếu trace và lý do Eadro-TT; R3 tách đúng điều kiện giữ ngoài khỏi C9. Không dùng normal/chất lượng/mapping làm điều kiện giữ ngoài bổ sung; nêu riêng tương thích baseline dự kiến có giới hạn. N1/N2 là đính chính ma trận, không đòi đổi D1/D2 hoặc thêm điều kiện chặn | Giữ lựa chọn nghiên cứu thuộc Minh; root vắng trong trace có vai trò P4 nhưng chưa chứng minh cơ chế |
| Các source/derived của R2/R3 và ma trận/audit trong bản đồ phiên 2 | Cập nhật những nội dung/đếm phụ thuộc đúng các sửa được Minh chọn; các giới hạn nguồn Nezha/Eadro và trạng thái OPEN hợp lệ giữ nguyên | Không chạy lại method, đọc locked hoặc thêm quy trình/phép kiểm để ghi các đính chính đã có nguồn |

### Kết thúc phiên 3 — 05/10/2026 (UTC+7)

1. **Đã làm:** ghi đính chính R2/R3, hạ N1/N2 thành KHÔNG CHẶN trong ý kiến người làm, mở rộng N1 thêm 42 ô sau đối chiếu reviewer, cập nhật đề xuất sửa. R1–R3 vẫn CHẶN. Không đóng T-020/G1.
2. **File thay đổi:** chỉ bảng người làm của `tasks/T-020-tong-hop-g1/REVIEW.md` (bốn dòng) và append `tasks/T-020-tong-hop-g1/LOG.md`. Giữ nguyên phần reviewer, mọi dòng khác trong bảng, cột Minh quyết và lịch sử LOG. Không ghi STATE/SPEC/docs chung/results/src/manifest; phạm vi hai file là đề xuất Minh đã duyệt.
3. **Kiểm và kết quả:** dùng lại nguồn đã kiểm ở lượt chỉ đọc; các phép đếm C5 40/39/4, N1 6, N2 95, phần mở rộng 42 và phân nhóm 10+10+6+6+5+5 khớp. Đối chiếu code và điều kiện SPEC xác nhận 42 ô chỉ trùng kết quả, không bất khả thi; không thêm điều kiện giữ ngoài. Một lượt lấy snapshot đọc hash trả về khi còn chạy, agent xử lý nhầm trạng thái chưa hoàn tất; lượt kế tiếp được chờ hoàn tất trước sửa. Không ghi đầu ra hoặc dùng snapshot thiếu. Kiểm kết phiên sau append: so lịch sử LOG, phần reviewer/dòng ngoài phạm vi, toàn bộ hash ngoài hai file và kiểm diff; đọc lại toàn phần thay đổi. Không chạy phương pháp hoặc dựng phép kiểm khoa học mới.
4. **Chưa chắc/cần Minh:** các sửa results chưa được thực hiện; các lựa chọn probe TX1/TX2, vị trí, stack, split/phân tầng, BOCPD/Q40 và WHY giữ trạng thái OPEN. Nội dung formal documentation cần cập nhật sau quyết định G1 vẫn theo bản đồ phiên 2 đã đính chính; phiên này chỉ sửa bản phản hồi. Không thêm vòng review hay cơ chế kiểm soát.
5. **Bước tiếp chính xác:** đọc bảng cuối REVIEW và phần cập nhật đề xuất theo file của phiên 3, rồi Minh chọn phạm vi sửa results và các lựa chọn OPEN. Phiên sửa đầu ra đọc AGENTS, SPEC, mục cuối LOG và source tương ứng; sửa source trước derived trong đúng phạm vi được duyệt. Giữ STATE như chỉ thị hai file; không chạy `prepare_handoff.py` ngoài phạm vi.
6. **Lệnh cuối:** `git diff --check`, sau đối chiếu hash/phạm vi và đọc toàn diff trong RAM. Đề xuất commit khi Minh duyệt: `docs(T-020): đính chính phản hồi R2 R3 và phạm vi N1 N2`; chưa commit/push.

Kiểm kết phiên đã hoàn tất: toàn phần thay đổi đã đọc; LOG chỉ ghi thêm và lịch sử khớp đầu phiên; REVIEW chỉ đổi dòng 100/101/106/107, phần reviewer và tám dòng phản hồi còn lại giữ nguyên; 12 ô Minh quyết vẫn trống; 6.065 file ngoài hai file được duyệt khớp đầu phiên. Đối chiếu độc lập nội dung cập nhật không phát hiện lỗi. `git diff --check` đạt. Dòng kết quả này được ghi thêm trong LOG rồi kiểm lại phạm vi LOG/REVIEW và chạy lại lệnh cuối trên.

## Đóng task — 05/10/2026 — Claude (Opus 5.5), người làm của T-021 ghi thay

- Minh đồng ý đề xuất 0 trong chat ngày 05/10/2026: đóng T-020, thay bằng T-021. R1–R3 của REVIEW được xử lý ở `results/T-021/goi-g1.md` mục 7. Các đề xuất sửa `results/T-020/` trong phiên 3 không thực hiện; `results/T-020/` giữ làm kho bằng chứng chỉ đọc.
- Quyết định G1: Q-61–Q-69 trong `docs/DECISIONS.md`.
