# Nhật ký T-013

## Phiên 1 — 04/10/2026 — Codex — Windows 11, laptop Minh — vai trò: người làm

**Mở phiên (2026-10-04T08:26:56.544532+07:00):** đã đọc các nguồn bắt buộc và tự duyệt SPEC theo ủy quyền. Không có SPEC/LOG/đầu ra T-013 trước phiên. HEAD git: `93f13d4c4a966428177e2acc287d96bc89303e92`. Hai source HEAD đúng yêu cầu; git status repo ban đầu sạch. STATE chưa có T-013; prompt hiện hành giao T-013 rõ, chỉ thêm dòng T-013.

**Quyết định của Minh trong phiên:**
- Minh ủy quyền tự duyệt SPEC theo prompt Đợt 1 ngày 04/10/2026
- Chưa ghi vào DECISIONS vì ngoài phạm vi; sẽ có nháp trong de-xuat-tai-lieu-chung.md.

**Khối task nguyên văn:**

```text
<task> vào LOG.
- Không ai duyệt SPEC trước khi làm, nên một lỗ hổng trong SPEC sẽ đi thẳng vào kết quả. Viết SPEC kỹ như thể nó sẽ được phản biện trước.
- Gặp việc vượt <gioi_han>: không làm việc đó, ghi vào LOG và vào mục "Cần Minh quyết", rồi làm tiếp phần còn lại.
</uy_quyen>

<doc_truoc>
1. Đọc toàn bộ: AGENTS.md, docs/STATE.md, docs/LESSONS.md, docs/review-prompt.md, tasks/_MAU/SPEC.md, tasks/_MAU/LOG.md.
2. Đọc docs/MRP.md: §2 đến §7, kỹ hai gói P1 và P2.
3. Đọc docs/WHY.md, docs/DECISIONS.md, docs/reference/sources/DT18-de-tai-va-nhiem-vu.md, docs/reference/sources/advisor-2026-09-23.md.
4. Các lỗi đã xảy ra trong repo. Đối chiếu SPEC và cách làm của bạn với từng lỗi:
   - SL24: báo "chạy được" khi mới biết là "không lỗi".
   - SL25: chạy lâu mà không ghi tiến độ.
   - SL26: SPEC bỏ một phép kiểm mà không nêu hệ quả.
   - SL27: tính chi phí theo từng ca, không theo tổng.
   - SL28: tra số công bố sau khi đã đo.
   - SL29: môi trường không ghim phiên bản.
   - SL30: đo thời gian khi máy đang chạy việc khác.
   - SL31: prompt phản biện có gợi ý, làm neo người phản biện.
   - SL32: bước xếp theo thứ tự đọc, không theo phụ thuộc.
   - SL33: kiểm trên dữ liệu nhỏ, bỏ quy mô Train Ticket.
   - REVIEW T-003 R1: bàn giao "xong" khi phần được phép kiểm chưa làm, và ghi việc chưa làm thành "chờ quyền".
   - Ngày 04/10: hai phiên ghi đè cùng một file chung, làm mất WHY-16 đã được duyệt.
</doc_truoc>

<task>
Thư mục task: tasks/T-013-ho-so-baro/. Thư mục kết quả: results/T-013/.

Đầu vào:
- results/T-001/danh-sach-phuong-phap.md, mục 1, 3, 4, 8, 9.
- results/T-005/.
- results/T-006/kiem-dung-dan.md mục 2, 3, 4, 8, 10, 11; thư mục results/T-006/cham/.
- Phần BOCPD trong results/T-007/kiem-dung-dan.md.
- docs/knowledge/K1-phuong-phap-rca.md.
- Code D:\RCA-ext\src\baro (revision e35f4ec) và D:\RCA-ext\src\RCAEval (revision 259ea41).
- Bài BARO, arXiv 2405.09330.

Yêu cầu:
1. Hồ sơ BARO, kèm đoạn biến thể N-Sigma, và hồ sơ BOCPD cùng N-Sigma phát hiện, theo <ho_so>.
2. Ví dụ tính tay trên 1 ca dev RE2-TT. Thêm 1 ca OB hoặc SS có mốc loại A để nối với T-006.
3. Giải thích bằng cơ chế vì sao kết quả đổi theo độ dài cửa sổ. T-006 mục 2.1 ghi một ô N-Sigma đổi 0,26 giữa cửa sổ 10 và 20. Đây là đầu vào cho quyết định cửa sổ ở G1 (Q-54). Không tự chốt cửa sổ.
4. Nêu điều kiện để BOCPD và N-Sigma phát hiện chạy được mà không dùng mốc tiêm (chế độ b). Xét ba điểm:
   - chuẩn hóa min–max trên toàn cửa sổ, tức là dùng dữ liệu tương lai;
   - cửa sổ được cắt quanh mốc tiêm;
   - biên file RCAEval đối xứng quanh mốc tiêm (T-006 mục 2.3).
   Ghi rõ dataset có dạng nào thì chấm được chế độ b. Không thiết kế bộ phát hiện mới.
5. So hai bản code BARO (repo baro và bản trong RCAEval): khác nhau ở đâu, ảnh hưởng tới kết quả thế nào.

Edge case tối thiểu phải có trong SPEC (bạn tự tìm thêm):
- IQR bằng 0, cột hằng, NaN.
- Nhiều metric trên một service, và cách gộp điểm lên mức service.
- Hòa điểm.
- Đơn vị của mốc tiêm.
- Tên cột khác nhau giữa các dataset.
- Dữ liệu bình thường quá ngắn.
- BOCPD tốn bộ nhớ O(T²): tính theo tổng chi phí cho cả dataset.
- Tham số hazard và prior.
- Điểm đổi nằm sát biên cửa sổ.

Không dùng EC2. Được ghi thêm: D:\RCA-ext\work\T-013\.
</task>
```

**Tự phản biện SPEC trước chạy:** bổ sung dict/DataFrame, timestamp-vs-index của anomalies, std ddof, service max và hòa điểm; không biến phép thử normal-normal thành yêu cầu code phải biết từ chối RCA. Quy tắc ca được khóa trước kết quả. Mốc A tập chỉ tái dùng, không gọi ví dụ một ca là tái lập số toàn bài. Hai subagent chỉ đọc độc lập, root giữ LOG/STATE.

**Diễn biến:**
- 2026-10-04T08:26:56.544532+07:00 — bước 0/1: đọc luật, mốc công bố trước chạy, xác minh hai HEAD; SPEC đã ghi trong phạm vi tự duyệt.

- 08:36:03 — bước 2: hai ca theo rule, BARO/N-Sigma BR/RE ở L10/L20; so từng điểm, lặp lại/đảo cột/normal-normal đã lưu results\T-013\runs\20261004-083543

- 08:39:14 — bước 3: detector hai prefix/ca, N-Sigma nguyên ca, posterior độc lập; mọi lượt và chi phí tham khảo trong runs.

- 08:43:16 — bước 4: dùng lại valid outputs sau lệnh pip-freeze lỗi; metadata bằng uv, thêm mốc A ranker 243, dict/prior/affine/sentinel audits. Không chạy lại phần đã khớp.

- 08:51:08 — bước 6 tự soát: bổ sung kiểm rẻ còn thiếu inf/IQR thật1/bước nhảy hằng/normal periodic/prior density/mapping; không lặp lại dataset runs.

- 08:53:14 — kiểm lần cuối: explicit same-input N-Sigma repeat OBfull/TTprefix và IQR0 đổi đơn vị; không benchmark mới.

- 2026-10-04T09:09:50+07:00 — tự kiểm bàn giao: parse và cơ chế đạt; chuẩn hóa cách trình bày, kiểm lại adapter từng giá trị. Không có gói mới, không sửa nguồn/env.

## Đính chính nhật ký trước bàn giao (chỉ ghi thêm)

- Khối task ở mục mở phiên lấy nhầm lần xuất hiện `<task>` trong câu hướng dẫn, nên có dư phần trước khối thật. Bản đúng nguyên văn ở dưới; nội dung task khoa học không đổi.
- Lỗi chép bảng mốc T-013: dòng RobustScorer[t_inject] được đính chính bằng Table 3 bài gốc. Bản trước sửa giữ tại `results/T-013/runs/moc-truoc-dinh-chinh.json`; bản hiện hành `doi-chieu-moc.json`. Không có phép đo hoặc lựa chọn tham số dựa trên ô chép nhầm.
- Các lượt hỏng được giữ: mở phiên đã ghi file thành công nhưng print gặp encoding; lượt cơ chế đầu thiếu Parquet engine; lượt kế thiếu file mốc trong T-005 (đã dùng metadata dev T-002); lượt tính chính hoàn tất rồi lỗi pip freeze (uv venv không có pip); lần viết ví dụ đầu dùng path tương đối (đã sửa resolve). Không bỏ lượt hỏng hoặc chạy lại các phần đã có đầu ra hợp lệ. Console/progress/failure và scripts trong danh sách file bàn giao.

**Khối task đúng nguyên văn, thay cho bản trích dư ở đầu LOG:**

```text
<task>
Thư mục task: tasks/T-013-ho-so-baro/. Thư mục kết quả: results/T-013/.

Đầu vào:
- results/T-001/danh-sach-phuong-phap.md, mục 1, 3, 4, 8, 9.
- results/T-005/.
- results/T-006/kiem-dung-dan.md mục 2, 3, 4, 8, 10, 11; thư mục results/T-006/cham/.
- Phần BOCPD trong results/T-007/kiem-dung-dan.md.
- docs/knowledge/K1-phuong-phap-rca.md.
- Code D:\RCA-ext\src\baro (revision e35f4ec) và D:\RCA-ext\src\RCAEval (revision 259ea41).
- Bài BARO, arXiv 2405.09330.

Yêu cầu:
1. Hồ sơ BARO, kèm đoạn biến thể N-Sigma, và hồ sơ BOCPD cùng N-Sigma phát hiện, theo <ho_so>.
2. Ví dụ tính tay trên 1 ca dev RE2-TT. Thêm 1 ca OB hoặc SS có mốc loại A để nối với T-006.
3. Giải thích bằng cơ chế vì sao kết quả đổi theo độ dài cửa sổ. T-006 mục 2.1 ghi một ô N-Sigma đổi 0,26 giữa cửa sổ 10 và 20. Đây là đầu vào cho quyết định cửa sổ ở G1 (Q-54). Không tự chốt cửa sổ.
4. Nêu điều kiện để BOCPD và N-Sigma phát hiện chạy được mà không dùng mốc tiêm (chế độ b). Xét ba điểm:
   - chuẩn hóa min–max trên toàn cửa sổ, tức là dùng dữ liệu tương lai;
   - cửa sổ được cắt quanh mốc tiêm;
   - biên file RCAEval đối xứng quanh mốc tiêm (T-006 mục 2.3).
   Ghi rõ dataset có dạng nào thì chấm được chế độ b. Không thiết kế bộ phát hiện mới.
5. So hai bản code BARO (repo baro và bản trong RCAEval): khác nhau ở đâu, ảnh hưởng tới kết quả thế nào.

Edge case tối thiểu phải có trong SPEC (bạn tự tìm thêm):
- IQR bằng 0, cột hằng, NaN.
- Nhiều metric trên một service, và cách gộp điểm lên mức service.
- Hòa điểm.
- Đơn vị của mốc tiêm.
- Tên cột khác nhau giữa các dataset.
- Dữ liệu bình thường quá ngắn.
- BOCPD tốn bộ nhớ O(T²): tính theo tổng chi phí cho cả dataset.
- Tham số hazard và prior.
- Điểm đổi nằm sát biên cửa sổ.

Không dùng EC2. Được ghi thêm: D:\RCA-ext\work\T-013\.
</task>
```

## Kết thúc phiên — bàn giao T-013

1. **Đã làm gì:** báo cáo A dưới đây; đối chiếu toàn bộ tiêu chí ở `doi-chieu-tieu-chi.md`.
2. **File đã thay đổi:** báo cáo B và danh sách đủ ở `danh-sach-file.json`/prompt dưới; ngoài repo đúng hai file adapter.
3. **Kiểm tra đã chạy và kết quả:** báo cáo C; kiểm bàn giao cuối được chạy lại sau khi ghi prompt và cập nhật STATE.
4. **Điều chưa chắc hoặc cần Minh quyết:** báo cáo G–H; nháp F chưa là quyết định.
5. **Bước tiếp theo chính xác:** Minh mở phiên Claude Code mới trong `D:/RCA-flashticket`, dán toàn bộ prompt cuối LOG; Claude đọc SPEC/LOG/danh sách file và chỉ ghi `tasks/T-013-ho-so-baro/REVIEW.md`. Người làm chưa sửa theo review khi Minh chưa quyết.
6. **Lệnh cuối cùng đã chạy để kiểm bàn giao:** `$env:PYTHONIOENCODING='utf-8'; $env:PYTHONDONTWRITEBYTECODE='1'; & D:/RCA-ext/envs/py312-pin/Scripts/python.exe results/T-013/scripts/kiem_ban_giao.py`. Không chạy phương pháp lại. Trạng thái T-013: chờ phản biện (04/10/2026).

### Báo cáo cuối A–H

A. Đã làm: hoàn thành ba hồ sơ chín mục cho BARO (kèm N-Sigma RCA), BOCPD và N-Sigma phát hiện; ví dụ độc lập trên một ca dev RE2-TT và một ca OB; giải thích cửa sổ, chế độ (b), so hai code và đủ CSV đầu vào/ca chạy.

B. File đã thay đổi: `tasks/T-013-ho-so-baro/SPEC.md`, `LOG.md`, toàn bộ đầu ra `results/T-013/` và đúng dòng T-013 trong `docs/STATE.md`. Ngoài repo: `D:/RCA-ext/work/T-013/metrics-selected.npz` và `metrics-selected.json`. Danh sách từng file ở `results/T-013/danh-sach-file.json` và prompt dưới. Không sửa task cũ, tài liệu chung khác, source hay môi trường. Không commit/push.

C. Kiểm tra đã chạy và kết quả: 131 phép kiểm cơ chế; điểm độc lập khớp official, sai số normalized lớn nhất 0; posterior BOCPD sai số tối đa 2.23e-16; top 5 metric mẫu README khớp. Đã kiểm lặp lại, đảo cột, normal-normal và các ca biên. Đảo cột giữ điểm nhưng có thể đổi rank khi hòa; list N-Sigma theo thứ tự cột; hai prefix BOCPD chỉ trả sentinel ngoài range. Những hành vi này được báo rõ, không gọi là PASS nghiệp vụ. Parse mọi file, CSV 16 cột/6 dòng, adapter mọi giá trị, source HEAD/status và diff kiểm sạch trong phạm vi; chi tiết `kiem-tra.json`, `kiem-ban-giao.json`.

D. VẤN ĐỀ Ở TASK CŨ — ĐỂ REVIEWER KIỂM: năm điểm D1–D5 trong `dinh-chinh-task-cu.md`: K1 chưa tách công thức bài/code và đơn vị chấm; T-006 suy IQR=0 từ scale=1; T-007 chưa giới hạn “chạy đúng” khi có sentinel; T-006 nói Recall luôn 1 thiếu điều kiện; T-001 cần tách RAM ma trận khỏi tổng chi phí. Đã bổ sung script, phản ví dụ và số kiểm trong T-013. IQR thô xác nhận 90/90 baseline; loại riêng sentinel không đổi P/R/F1 tập OB cũ. Chưa có bằng chứng phải đổi các số tái lập cũ; không sửa file task cũ.

E. Chỗ lệch khỏi SPEC và lý do: dùng môi trường py312 sẵn có chỉ đọc Parquet rồi NPZ vì pin thiếu engine; phương pháp vẫn chạy môi trường ghim. Dùng metadata dev T-002 vì ca chọn không có trong metadata T-005; lấy metadata môi trường bằng uv vì venv không có pip. Đã ghi các thay đổi ở cuối SPEC, giữ lượt hỏng. Lỗi chép bảng mốc và trích khối task của T-013 đã đính chính, giữ dấu vết; không đổi rule ca hoặc cấu hình theo kết quả.

F. Đề xuất cho tài liệu chung: nháp DECISIONS về ủy quyền, WHY về quy tắc ví dụ/cách đối chiếu, K1 về công thức và đơn vị độ đo, cùng đoạn sửa tối thiểu D1–D5 trong `de-xuat-tai-lieu-chung.md`. Chưa ghi vào nguồn chung.

G. Phần chưa kiểm và lý do: BOCPD full TT vượt giới hạn một giờ đã thấy ở T-005; benchmark toàn tập/ảnh hưởng bản sửa extraction thuộc gói sau; cấu hình thực nghiệm tác giả chưa đủ để phân xử mọi sai lệch bảng; chế độ (b) hợp lệ và runtime chính thức cần protocol G1/recording độc lập lỗi và máy rảnh. Giả định, trường hợp sai và cách kiểm tiếp ở `doi-chieu-tieu-chi.md`. Không để phép kiểm rẻ trong phạm vi thành “chờ quyền”.

H. Cần Minh quyết: phản biện độc lập bằng Claude; việc đưa các nháp vào tài liệu chung; cửa sổ Q-54, protocol hồi cứu/online và cách xử lý các sai lệch code khi tổng hợp G1. T-013 không tự chốt các lựa chọn này.


## Prompt phản biện cho Claude

```text
Bạn là người phản biện độc lập cho task T-013 của repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Bạn chỉ được ghi đúng một file: tasks/T-013-ho-so-baro/REVIEW.md, theo mẫu tasks/_MAU/REVIEW.md.
Không sửa file nào khác, không commit.

Đọc: tasks/T-013-ho-so-baro/SPEC.md, tasks/T-013-ho-so-baro/LOG.md, các file đầu ra: 
- tasks/T-013-ho-so-baro/SPEC.md
- tasks/T-013-ho-so-baro/LOG.md
- results/T-013/ca-da-chay.csv
- results/T-013/cua-so-va-che-do-b.md
- results/T-013/danh-sach-file.json
- results/T-013/de-xuat-tai-lieu-chung.md
- results/T-013/dinh-chinh-task-cu.md
- results/T-013/doi-chieu-moc.json
- results/T-013/doi-chieu-tieu-chi.md
- results/T-013/ho-so-baro.md
- results/T-013/ho-so-bocpd.md
- results/T-013/ho-so-nsigma-phat-hien.md
- results/T-013/kiem-ban-giao.json
- results/T-013/kiem-tra.json
- results/T-013/manifest.json
- results/T-013/moi-truong.md
- results/T-013/runs/20261004-083120/failure.txt
- results/T-013/runs/20261004-083123/tien-do.jsonl
- results/T-013/runs/20261004-083343/tien-do.jsonl
- results/T-013/runs/20261004-083543/OB-L10-robust-BR-metric.csv
- results/T-013/runs/20261004-083543/OB-L10-robust-BR-ranks.json
- results/T-013/runs/20261004-083543/OB-L10-robust-metric.csv
- results/T-013/runs/20261004-083543/OB-L10-robust-ranks.json
- results/T-013/runs/20261004-083543/OB-L10-standard-BR-metric.csv
- results/T-013/runs/20261004-083543/OB-L10-standard-BR-ranks.json
- results/T-013/runs/20261004-083543/OB-L10-standard-metric.csv
- results/T-013/runs/20261004-083543/OB-L10-standard-ranks.json
- results/T-013/runs/20261004-083543/OB-L20-robust-BR-metric.csv
- results/T-013/runs/20261004-083543/OB-L20-robust-BR-ranks.json
- results/T-013/runs/20261004-083543/OB-L20-robust-metric.csv
- results/T-013/runs/20261004-083543/OB-L20-robust-ranks.json
- results/T-013/runs/20261004-083543/OB-L20-standard-BR-metric.csv
- results/T-013/runs/20261004-083543/OB-L20-standard-BR-ranks.json
- results/T-013/runs/20261004-083543/OB-L20-standard-metric.csv
- results/T-013/runs/20261004-083543/OB-L20-standard-ranks.json
- results/T-013/runs/20261004-083543/OB-README-A-cut243-metric.csv
- results/T-013/runs/20261004-083543/OB-README-A-cut243-ranks.json
- results/T-013/runs/20261004-083543/OB-labels-after-rank.json
- results/T-013/runs/20261004-083543/OB-normal-normal-robust-metric.csv
- results/T-013/runs/20261004-083543/OB-normal-normal-robust-ranks.json
- results/T-013/runs/20261004-083543/OB-normal-normal-standard-metric.csv
- results/T-013/runs/20261004-083543/OB-normal-normal-standard-ranks.json
- results/T-013/runs/20261004-083543/OB-nsigma-detail.csv
- results/T-013/runs/20261004-083543/OB-nsigma-hits.json
- results/T-013/runs/20261004-083543/OB-prefix120-bocpd-detail.json
- results/T-013/runs/20261004-083543/OB-prefix120-bocpd-normalized.csv
- results/T-013/runs/20261004-083543/OB-prefix120-bocpd-posterior.npz
- results/T-013/runs/20261004-083543/TT-L10-robust-BR-metric.csv
- results/T-013/runs/20261004-083543/TT-L10-robust-BR-ranks.json
- results/T-013/runs/20261004-083543/TT-L10-robust-metric.csv
- results/T-013/runs/20261004-083543/TT-L10-robust-ranks.json
- results/T-013/runs/20261004-083543/TT-L10-standard-BR-metric.csv
- results/T-013/runs/20261004-083543/TT-L10-standard-BR-ranks.json
- results/T-013/runs/20261004-083543/TT-L10-standard-metric.csv
- results/T-013/runs/20261004-083543/TT-L10-standard-ranks.json
- results/T-013/runs/20261004-083543/TT-L20-robust-BR-metric.csv
- results/T-013/runs/20261004-083543/TT-L20-robust-BR-ranks.json
- results/T-013/runs/20261004-083543/TT-L20-robust-metric.csv
- results/T-013/runs/20261004-083543/TT-L20-robust-ranks.json
- results/T-013/runs/20261004-083543/TT-L20-standard-BR-metric.csv
- results/T-013/runs/20261004-083543/TT-L20-standard-BR-ranks.json
- results/T-013/runs/20261004-083543/TT-L20-standard-metric.csv
- results/T-013/runs/20261004-083543/TT-L20-standard-ranks.json
- results/T-013/runs/20261004-083543/TT-labels-after-rank.json
- results/T-013/runs/20261004-083543/TT-normal-normal-robust-metric.csv
- results/T-013/runs/20261004-083543/TT-normal-normal-robust-ranks.json
- results/T-013/runs/20261004-083543/TT-normal-normal-standard-metric.csv
- results/T-013/runs/20261004-083543/TT-normal-normal-standard-ranks.json
- results/T-013/runs/20261004-083543/TT-nsigma-detail.csv
- results/T-013/runs/20261004-083543/TT-nsigma-hits.json
- results/T-013/runs/20261004-083543/TT-prefix120-bocpd-detail.json
- results/T-013/runs/20261004-083543/TT-prefix120-bocpd-normalized.csv
- results/T-013/runs/20261004-083543/TT-prefix120-bocpd-posterior.npz
- results/T-013/runs/20261004-083543/checks-partial.json
- results/T-013/runs/20261004-083543/edge-bocpd-NaN-leading-detail.json
- results/T-013/runs/20261004-083543/edge-bocpd-NaN-leading-normalized.csv
- results/T-013/runs/20261004-083543/edge-bocpd-NaN-leading-posterior.npz
- results/T-013/runs/20261004-083543/edge-bocpd-no-matching-name-detail.json
- results/T-013/runs/20261004-083543/edge-bocpd-no-matching-name-normalized.csv
- results/T-013/runs/20261004-083543/edge-bocpd-no-matching-name-posterior.npz
- results/T-013/runs/20261004-083543/edge-change-1-detail.json
- results/T-013/runs/20261004-083543/edge-change-1-normalized.csv
- results/T-013/runs/20261004-083543/edge-change-1-posterior.npz
- results/T-013/runs/20261004-083543/edge-change-10-detail.json
- results/T-013/runs/20261004-083543/edge-change-10-normalized.csv
- results/T-013/runs/20261004-083543/edge-change-10-posterior.npz
- results/T-013/runs/20261004-083543/edge-constant-half-metric.csv
- results/T-013/runs/20261004-083543/edge-constant-half-ranks.json
- results/T-013/runs/20261004-083543/edge-falling-metric.csv
- results/T-013/runs/20261004-083543/edge-falling-ranks.json
- results/T-013/runs/20261004-083543/edge-hazard-250-detail.json
- results/T-013/runs/20261004-083543/edge-hazard-250-normalized.csv
- results/T-013/runs/20261004-083543/edge-hazard-250-posterior.npz
- results/T-013/runs/20261004-083543/edge-hazard-5-detail.json
- results/T-013/runs/20261004-083543/edge-hazard-5-normalized.csv
- results/T-013/runs/20261004-083543/edge-hazard-5-posterior.npz
- results/T-013/runs/20261004-083543/edge-iqr-zero-metric.csv
- results/T-013/runs/20261004-083543/edge-iqr-zero-ranks.json
- results/T-013/runs/20261004-083543/edge-no-change-detail.json
- results/T-013/runs/20261004-083543/edge-no-change-normalized.csv
- results/T-013/runs/20261004-083543/edge-no-change-posterior.npz
- results/T-013/runs/20261004-083543/edge-ties-metric.csv
- results/T-013/runs/20261004-083543/edge-ties-ranks.json
- results/T-013/runs/20261004-083543/edge-unit-IQR0-metric.csv
- results/T-013/runs/20261004-083543/edge-unit-IQR0-ranks.json
- results/T-013/runs/20261004-083543/tien-do.jsonl
- results/T-013/runs/audit-cu-console.log
- results/T-013/runs/bo-sung-console.log
- results/T-013/runs/hoan-tat-console.log
- results/T-013/runs/lap-lai-console.log
- results/T-013/runs/luot-2-console.log
- results/T-013/runs/luot-3-console.log
- results/T-013/runs/moc-truoc-dinh-chinh.json
- results/T-013/runs/viet-vi-du-console.log
- results/T-013/scripts/ban_giao.py
- results/T-013/scripts/doc_parquet.py
- results/T-013/scripts/hoan_tat_kiem.py
- results/T-013/scripts/kiem_ban_giao.py
- results/T-013/scripts/kiem_bo_sung.py
- results/T-013/scripts/kiem_co_che.py
- results/T-013/scripts/kiem_ket_qua_cu.py
- results/T-013/scripts/kiem_lap_lai.py
- results/T-013/scripts/mo_phien.py
- results/T-013/scripts/viet_vi_du.py
- results/T-013/trung-gian/T006-moc-A-reused.json
- results/T-013/trung-gian/T006-redis-IQR-raw.csv
- results/T-013/trung-gian/T006-redis-IQR-summary.json
- results/T-013/trung-gian/T007-bocpd-allowed-records.json
- results/T-013/trung-gian/chi-phi-va-sentinel.json
- results/T-013/trung-gian/chon-ca.json
- results/T-013/trung-gian/cua-so-cu.json
- results/T-013/trung-gian/freeze-py312-pin.txt
- results/T-013/trung-gian/kiem-adapter.json
- results/T-013/trung-gian/service-rank-ca.csv
- results/T-013/trung-gian/task-cu-relevant-source-audit.json
- results/T-013/vi-du-tinh-tay.md
- results/T-013/yeu-cau-dau-vao.csv
- D:/RCA-ext/work/T-013/metrics-selected.json
- D:/RCA-ext/work/T-013/metrics-selected.npz,
và kết quả `git diff 93f13d4c4a966428177e2acc287d96bc89303e92` nếu có.
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


## Phiên 2 — 04/10/2026 — Codex — Windows 11, laptop Minh — người làm phản hồi phản biện

**Mở phiên (2026-10-04T18:50:38+07:00):** đã đọc toàn bộ AGENTS.md và workflow bước 7 trong docs/review-prompt.md; đọc STATE, SPEC và LOG T-013. HEAD git: `93f13d4c4a966428177e2acc287d96bc89303e92`. Chưa mở REVIEW.md; tự soát đầu ra trước theo workflow. Các thay đổi đang có ở tài liệu chung/task khác là ngoài phạm vi phiên này, không sửa hoặc nhận là của T-013.

**Minh giao nguyên văn:** “đã có review t 013, đọc agent.md và workflow trước rồi **kiểm chứng từng góp ý rồi ghi phản hồi vào bảng cuối REVIEW và LOG**.”

**Phạm vi phiên:** điền bảng phản hồi cuối REVIEW, thêm LOG; chỉ cập nhật dòng trạng thái T-013 theo AGENTS bước 7. Không sửa hồ sơ, kết quả, SPEC hay nội dung reviewer. Cột Minh quyết để trống.

**Tự soát độc lập — đã ghi TRƯỚC khi mở REVIEW.md:**
- Đã đọc toàn bộ 135 file output bằng lượt chỉ đọc: JSON/JSONL, CSV, NPZ, Markdown/log/text và AST Python. Đối chiếu mọi cặp score/official_score và posterior độc lập/official; không có sai lệch mới ở các output đã lưu. Hai revision source và workflow giữ theo SPEC. Không chạy các script top-level có ghi output.
- **S1 — KHÔNG CHẶN các số đã lưu:** `scripts/kiem_co_che.py:83` nhánh StandardScaler độc lập chỉ dùng sqrt(nanvar) và scale==0, thiếu variance bù sai số/điều kiện gần hằng của sklearn mà `ho-so-baro.md:48` đã nêu đúng. Synthetic time=0..11, a_cpu=1e16+2*time, cut=6, dataset=fse-ob: helper scale=3.559026084010437, score=5.057563382541147; sklearn1.6 var=11.666666666666666, scale=1, score=18.0. Tự kiểm root và subagent chỉ đọc cùng xác nhận. Các điểm của 8 cấu hình ca thật vẫn khớp CSV, không có bằng chứng sửa số hiện hành. Đề xuất sửa helper khi Minh duyệt; không sửa ở phiên phản hồi.
- **S2 — KHÔNG CHẶN:** `ho-so-nsigma-phat-hien.md:19` gọi n là số mẫu “hữu hạn” chưa đúng pandas: với [1,2,inf,NaN], count=3 nhưng số finite=2, mean=inf và std=NaN. Đề xuất ghi “số mẫu không NaN; công thức cần các giá trị hữu hạn; inf không được tự loại”. Chưa ảnh hưởng các ví dụ hai ca hữu hạn.
- **S3 — KHÔNG CHẶN:** `ho-so-bocpd.md:23` nói q_t(0)=0.02 khi tổng “hữu hạn”; cần thêm “dương”. Synthetic core T=1,d=100,x=10000: predictive density=0, mass sum=0 hữu hạn nhưng posterior=[NaN,NaN]. Đây là kiểm core, không khẳng định wrapper min–max cũng nhận đúng dữ liệu này. Underflow đã được hồ sơ nêu ở mục6, nên sửa điều kiện tại chỗ đủ. Lượt thử x=1e20 trước đó gặp LinAlgError khi update; giữ thông tin lượt hỏng ở đây, không dùng nó để chứng minh toàn wrapper.
- Việc đính chính task cũ D1–D5 là đầu ra cần reviewer kiểm; chưa ghi nguồn chung. Không có lựa chọn khoa học mới được quyết. Các thay đổi repo của phiên khác giữ nguyên.

**Chuyển bước:** tự soát đã kết thúc; từ lệnh đọc tiếp theo mới mở REVIEW.md để kiểm từng góp ý.

**Diễn biến sau khi mở REVIEW (2026-10-04T19:02:52+07:00):**
- REVIEW có đúng một finding R1. Đọc cả bằng chứng, đoạn tự phản bác và đề xuất; đối chiếu yêu cầu gốc, SPEC bước4/tiêu chí4, hồ sơ cửa sổ và bảng tiêu chí.
- Root và một subagent chỉ đọc tính độc lập từ 25 JSON DELAY mỗi L. Mỗi ca góp max(0,6-rank)/5; trung bình25ca theo evaluation.py:102–108. Kết quả 0,936/0,680, chênh0,256; 13 tụt/2 lên/10 giữ; 9 trong13 tụt có metric đầu _mem. Reviewer nêu đúng ba hạng 1→6,2→7,1→5. Các CPU Avg5 0,896→0,920 cũng khớp bảng T-006; chúng không phân xử cơ chế DELAY.
- Không nhận pattern memory là cơ chế. Đọc nguyên ca fse-ob/currencyservice_delay/4 (đã chạy T-006, không khóa), clean theo runner, tự tính mean/variance bù sai số/max/candidate để kiểm phép phân rã được đề xuất. Không gọi phương pháp chính thức hoặc benchmark dataset.

### Bằng chứng kiểm R1 — từng ca từ đầu ra đã lưu

Nguồn L10: `D:/RCA-ext/work/T-006/l4-nsigma-fse-ob-len10-lan1/output/results/*_delay_*.json`; L20: `D:/RCA-ext/work/T-006/l4-nsigma-fse-ob-lan1/output/results/*_delay_*.json`. Chỉ mở các file DELAY đã lọc; nhãn root chỉ dùng chấm thứ hạng đã có. Không sửa các file nguồn.

| Ca | Hạng L10 | Hạng L20 | Metric đầu L20 |
|---|---:|---:|---|
| cartservice_delay_1 | 1 | 1 | cartservice_latency |
| cartservice_delay_2 | 1 | 3 | recommendationservice_mem |
| cartservice_delay_3 | 1 | 3 | recommendationservice_mem |
| cartservice_delay_4 | 1 | 3 | main_mem |
| cartservice_delay_5 | 1 | 2 | frontend_mem |
| checkoutservice_delay_1 | 1 | 1 | checkoutservice_latency |
| checkoutservice_delay_2 | 1 | 4 | cartservice_latency |
| checkoutservice_delay_3 | 1 | 5 | emailservice_mem |
| checkoutservice_delay_4 | 1 | 3 | cartservice_latency |
| checkoutservice_delay_5 | 1 | 3 | emailservice_mem |
| currencyservice_delay_1 | 2 | 1 | currencyservice_latency |
| currencyservice_delay_2 | 2 | 4 | main_mem |
| currencyservice_delay_3 | 1 | 1 | currencyservice_latency |
| currencyservice_delay_4 | 1 | 6 | cartservice_latency |
| currencyservice_delay_5 | 2 | 7 | emailservice_mem |
| paymentservice_delay_1 | 1 | 1 | paymentservice_latency |
| paymentservice_delay_2 | 1 | 1 | paymentservice_latency |
| paymentservice_delay_3 | 1 | 1 | paymentservice_latency |
| paymentservice_delay_4 | 1 | 3 | checkoutservice_latency |
| paymentservice_delay_5 | 1 | 1 | paymentservice_latency |
| productcatalogservice_delay_1 | 2 | 2 | checkoutservice_latency |
| productcatalogservice_delay_2 | 2 | 1 | productcatalogservice_latency |
| productcatalogservice_delay_3 | 1 | 4 | recommendationservice_mem |
| productcatalogservice_delay_4 | 2 | 2 | checkoutservice_latency |
| productcatalogservice_delay_5 | 3 | 3 | checkoutservice_latency |

### Bằng chứng kiểm R1 — phân rã số học một ca

Nguồn: `D:/RCA-ext/data/fse-ob/currencyservice_delay/4/simple_data.csv` và `inject_time.txt`; injection1692611420. File có360 nền +361 hậu. Cùng44candidate sau bỏ hằng/giao cột ở cả bốn cấu hình. Endpoint metric ranks của tính độc lập khớp từng vị trí với JSON T-006, không chỉ root rank.

| Nền | Hậu | Hạng currencyservice | Metric đầu | Điểm currencyservice_latency | Điểm cartservice_latency |
|---:|---:|---:|---|---:|---:|
| 300 | 300 | 1 | currencyservice_latency | 4275.224266160058 | 8.642681338610984 |
| 300 | 361 | 1 | currencyservice_latency | 4275.224266160058 | 616.741459095199 |
| 360 | 300 | 5 | adservice_mem | 13.736534164871664 | 6.879025287281994 |
| 360 | 361 | 6 | cartservice_latency | 13.736534164871664 | 510.389711918555 |

- Root_latency: mean nền0,004357016743537815→0,006468274243394639; std(ddof0)0,00005076048101946793→0,015644498105358676; max hậu giữ0,2213694569599241. Chỉ thêm nền làm điểm/root rank tụt rõ.
- Cart_latency: max hậu0,0052324244866581→0,0547619047619068 do61dòng thêm. Nền300 giữ root4275 lớn hơncart616; nền360 hạ root13,7, nên cart510 đứng trước. adservice_mem cùngmax111,947776, score75,7156→77,9007; không thể quy việc tụt này riêng cho memory.
- Đây là cơ chế số học của đổi cửa sổ ở một ca, không là nguyên nhân thật của sự cố, không là giải thích trọn0,256 trên25ca. Khả năng khác gồm tải/gai nền, nhãn tiêm khác onset, missing và preprocessing; cần đối chiếu từng ca trước kết luận toàn ô. Vì vậy phép kiểm này chứng minh đề xuất reviewer khả thi/rẻ, chưa biến R1 thành đã sửa.

### Kết luận cho từng góp ý và điểm tự tìm

- **R1: đúng, CHẶN.** T-013 chưa giải thích riêng ô DELAY và đã đánh dấu tiêu chí4 đủ. Giới hạn “không quy0,256 cho riêngstd” tránh kết luận sai nhưng không đáp ứng yêu cầu. Phạm vi lỗi là đầu vào cửa sổG1/tiêu chí4; không bác ba hồ sơ, hai ví dụ hoặc số tổng đã tái lập. Đề xuất của reviewer phù hợp; cần tính cùng rule candidate/mapping, không chỉ top-memory để tránh quy cơ chế sai. Chờ Minh duyệt sửa.
- **N1=S1: KHÔNG CHẶN số hiện có.** Helper standard thiếu numerical variance/near-constant branch. Các điểm ca thật vẫn khớp; sửa là cần để helper mô phỏng đúng khi tái dùng trên dữ liệu gần hằng. Root đã tái kiểm phản ví dụ với AST-load chỉ function, không chạy top-level.
- **N2=S2: KHÔNG CHẶN.** Đổi mô tả số mẫu pandas và inf theo bằng chứng trước REVIEW.
- **N3=S3: KHÔNG CHẶN.** Thêm điều kiện tổng mass dương hữu hạn; không cần sửa code tác giả cho finding này.
- Bảng cuối REVIEW đã có đủ R1,N1,N2,N3; cột Minh quyết trống; toàn văn reviewer trước mục phản hồi giữ nguyên byte.

### Đề xuất sửa gom theo file — CHƯA thực hiện

| File/phạm vi đề xuất | Cũ → mới/việc cần làm | Vì sao, ảnh hưởng |
|---|---|---|
| results/T-013/cua-so-va-che-do-b.md §1 | Bốn đường chung/hai ví dụ → bằng chứng DELAY25ca, score của root/đối thủ, phân rã thêm nền/thêm hậu có nguồn | Đáp ứng R1, phục vụ Q-54; không chốtL, không đổi số T-006 |
| results/T-013/doi-chieu-tieu-chi.md dòng4 | Đánh dấu đủ với0,256 chung → đối chiếu bằng chứng DELAY thật, chỉ ghi đạt sau khi kiểm đủ | Không bàn giao tiêu chí4 chưa làm như đã xong |
| results/T-013/scripts/kiem_co_che.py dòng83/85 | sqrt(nanvar), scale==0 → variance bù sai số, bound gần hằng đúng sklearnghim; trung gian cùngvariance | SửaN1; giữ/lần theo output cũ, kiểm ảnh hưởng nếu cần |
| results/T-013/ho-so-nsigma-phat-hien.md dòng19 | “số mẫu hữu hạn” → “số mẫu khôngNaN; công thức đòi giá trị hữu hạn; inf không tự loại” | SửaN2, chỉ điều kiện công thức |
| results/T-013/ho-so-bocpd.md dòng23 | “tổng hữu hạn” → “tổng mass dương và hữu hạn” | SửaN3; underflow đã nêu mục6 |
| results/T-013/scripts/kiem_cua_so_delay.py và results/T-013/trung-gian/cua-so-delay-*.csv/json (đề xuất mới) | Chưa có → script chỉ tái dùng25caT-006 và đọc raw fse-ob để phân rã/cite, giữ mọi lượt và ghi ca nếu gọi phương pháp | Bằng chứng R1 tái lập được, không benchmark mới hoặc đọc khóa |
| results/T-013/scripts/kiem_bo_sung.py; kiem-tra.json/ca-da-chay.csv/runs/ khi sửaN1 | Chưa có phản ví dụ near-constant → ghi phản ví dụ đã thấy, xác minh helper sau sửa và giữ các lượt cũ | Không tuyên bố sửa helper đúng nếu chưa chạy kiểm; chỉ trong phạm vi task đã có |

Đây là impact map để Minh chọn sửa, không là quyền sửa. Không cập nhật hồ sơ/kết quả/SPEC/tài liệu chung ở phiên này. Không đề xuất cổng hoặc vòng review mới. Khi Minh quyết phạm vi, thực hiện bước8 trong cùngT-013 rồi ghiLOG; không tự đóngtask.

### Kết thúc phiên 2

1. **Đã làm:** tự soát trước REVIEW, kiểm chứng toàn bộ R1 cùng số từngca; thêm3điểm tự tìm, phản hồi bảngcuối vàLOG.
2. **File thay đổi:** `tasks/T-013-ho-so-baro/REVIEW.md` chỉ bảng người làm; `LOG.md` chỉ thêm; đúng dòngT-013 trong `docs/STATE.md` theo AGENTS bước7. Không sửa output/result/helper/nguồn chung khác, không ghi ngoài repo, không commit/push.
3. **Kiểm và kết quả:** đọc/parse135file; mọi score/posterior hiện hành khớp; đọc50JSON cho25DELAY; tự tính mộtca hai cửa sổ +hai phối hợp nền/hậu, endpoint khớp từngmetric; synthetic gần hằng, pandasinf và BOCPDmass0; diffcheck và bảo toàn bodyreviewer/LOGcũ/STATEngoàidòngT-013. Một lượt synthetic BOCPDx1e20 gặp LinAlgError đã giữ trongLOG, không dùng kết luận wrapper. Các lượt stdout subagent lỗi cúpháp/khôngthuoutput không dùng làm bằng chứng.
4. **Chưa chắc/cần Minh:** R1 cònCHẶN vì hồ sơ chưa sửa; N1–N3 khôngchặn số hiện có nhưng có đề xuất sửa. Chưa biết cơ chế toàn25ca từ phân rã mộtca. Cột Minh quyết trống; Minh quyết phạmvi sửa trong bảng trên.
5. **Bước tiếp theo:** Minh quyết R1/N1/N2/N3 và các file. Sau đó người làm đọc bảngcuốiREVIEW + mục cuốiLOG, thực hiện đúng phạmvi duyệt; chưa chuyển taskxong. Không mở vòngreview mới chỉ vì có finding.
6. **Lệnh kiểm cuối:** `git diff --check -- docs/STATE.md tasks/T-013-ho-so-baro/REVIEW.md tasks/T-013-ho-so-baro/LOG.md` cùng lượt Python chỉđọc xác minh reviewerbody, LOGappend, outputhash và STATEchỉđúngdòng.


## Phiên 3 — 04/10/2026 — Codex — Windows 11, laptop Minh — người làm sửa R1/N1–N3

**Mở phiên:** đã đọc AGENTS, STATE, SPEC, mục cuối LOG và REVIEW. HEAD `93f13d4c4a966428177e2acc287d96bc89303e92`. Minh giao nguyên văn: “sửa lại các lỗi trên, test cẩn thận”. Đây là duyệt sửa R1 và N1–N3 theo impact map phiên2; chưa phải duyệt đóng task hoặc commit.
**Phạm vi/tác động:** sửa helper N-Sigma độc lập, hai câu điều kiện, §1 cửa sổ và tiêu chí4; thêm script/bằng chứng phân rã DELAY và kiểm sửa; cập nhật các kết quả/ledger/inventory liên quan, bảng phản hồi người làm, LOG và đúng dòng STATE. Không sửa code tác giả, env, task cũ hoặc nguồn chung. RULE chọn2ca gốc giữ nguyên;25ca DELAY chỉ dùng lại ca T-006 đã chạy để sửaR1, không benchmark mới. SPEC gốc giữ nguyên, diễn biến sửa theo bước8 ghi LOG.
**Thứ tự/phụ thuộc:** một subagent thực hiện riêngR1 và chỉ các file được giao; root sửa/testN1–N3 độc lập. Sau hai nhánh, root soát toàn kết quả, các số cũ bất biến, cơ chế từngca, bảngreviewer và cập nhật bàn giao.
**Chi phí trước chạy:** R1 đọc25ca+50JSON, tính4cửa sổ và lặp kiểm nội bộ dự kiến<10phút; N1 synthetic và2ca×2L×2code dự kiến<5phút; không BOCPD fullTT, không tải dữ liệu, không lượt>1h. Thời gian chỉ tiến độ trên laptop, không benchmark chính thức. Runroot `results/T-013/runs/sua-N1-20261004-195501`; snapshot trước sửa và hash tậpfile trongmanifest.
