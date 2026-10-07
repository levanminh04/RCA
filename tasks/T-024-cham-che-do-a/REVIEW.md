# Phản biện T-024

- **Người phản biện:** Claude — **Ngày:** 06/10/2026 — **Commit/diff đã đọc:** HEAD `3b1e0dd`; `git diff HEAD` chỉ có `docs/DECISIONS.md`, `docs/STATE.md`, `docs/WHY.md` (thay đổi của các task khác, cộng dòng T-024 trong STATE). Mọi file T-024 chưa được theo dõi; đọc trực tiếp.
- **Đã đọc:** AGENTS.md; SPEC, LOG T-024; `results/T-024/` (`cham-a.json`, `cham-a.md`, `ban-ghi-dua-vao-cham.json`, `kiem-truoc-chay.json`, `scripts/{run,evaluate,report,verify}.py`, `runs/*/{cau-hinh,tom-tat}.json` và bản ghi, `test-chay-lai/`, `work/` gồm `freeze.json`, `evaluator-00{1,2}*`, `kiem-cuoi.json`, `kiem-dung-dan.json`, `minh-duyet-kiem-tay.json`, bản báo cáo 001); `src/p3/danh_gia.py`, `worker.py`; `results/T-031/moi-truong.json`, `kiem-11-ca-hashseed.json`, `khoa-cau-hinh.md`; giao thức V2 §3–§10; WHY-36; LESSONS; `docs/review-prompt.md`; RCAEval `259ea41` (`benchmark/evaluation.py`, `README.md`, `main.py`); `results/T-017/so-cong-bo.csv`; test `results/T-030/tests/test_buoc2.py`; DT18 và hướng dẫn của cô.

## Kết luận chung

Không có lỗi chặn. Số trong `cham-a.md` khớp `cham-a.json`, và khớp phép tính lại độc lập của tôi từ 420 bản ghi gốc. Không thấy nhãn lọt vào phương pháp, không ghi ngoài phạm vi, tiêu chí xong đạt. Có hai điểm không chặn về cách đọc kết quả: nhóm 19 ca lệch theo một chiều đo được mà báo cáo chưa nêu (R1), và báo cáo thiếu một giới hạn về hòa mà giao thức yêu cầu ghi (R2).

## Các điểm

### R1. Nhóm 19 ca bỏ đúng những ca dễ với các phương pháp khác; báo cáo chưa nêu chiều lệch — KHÔNG CHẶN

- **Ở đâu:** `results/T-024/cham-a.md` mục "Phạm vi và cách đọc" (dòng 12–15) và các bảng dev19 (dòng 225–428), nhất là "Hiệu từng cặp trên cùng mẫu bootstrap — dev19" (từ dòng 327). Lập luận gốc nằm ở `docs/WHY.md` WHY-36, mục "Vì sao": báo riêng 19 ca "thì kiểm được kết luận có còn đứng khi bỏ 11 ca".
- **Sai gì:** Báo cáo chỉ nói nhóm 19 "không phải mẫu ngẫu nhiên", không nói lệch theo chiều nào. 11 ca bị loại (theo lỗi làm tròn của CIRCA) lại là những ca dễ với hầu hết phương pháp khác. Chúng còn chứa 3/4 ca ERROR của MicroRank và TraceRCA. Vì vậy hiệu một cặp trên dev19 trộn hai hiệu ứng: bỏ ca CIRCA bị lỗi, và bỏ ca dễ hoặc ca lỗi của phương pháp kia. Phép so chỉ kiểm được một chiều: một kết luận "X hơn CIRCA" mà vẫn đứng trên dev19 thì vững. Còn một khoảng nghiêng về CIRCA trên dev19 thì có thể chỉ do cách chọn ca. Các cặp không có CIRCA cũng đổi, chỉ vì tập ca do đầu ra CIRCA quyết định. Câu "Khoảng chứa 0 chưa cho thấy khác biệt" ở mục dev19 dễ khiến người đọc coi khoảng không chứa 0 là khác biệt thật.
- **Bằng chứng** (đọc `cham-a.json` → `methods.<m>.per_case`, tách theo `cohorts.dev19.excluded_case_ids`; lệnh Python chỉ đọc):
  - Hit@1 trên 11 ca bị loại so với 19 ca giữ lại: BARO 10/11 và 11/19; TORAI B 10/11 và 16/19; SimpleRCA 9/11 và 16/19; TraceRCA 8/11 và 13/19; CIRCA OLS+RHT+DA 3/11 và 13/19.
  - MicroRank và TraceRCA cùng ERROR ở dev-03d4910932, dev-4e68956051, dev-a5cabe5fa7 (cả ba thuộc 11 ca loại) và dev-16870e660c (giữ lại). Nên dev19 chỉ còn 1 ERROR.
  - Cả 3 ca của ô `ts-train-service|cpu` bị loại. dev19 còn 9 ô; ts-train-service chỉ còn 1 ca.
  - Bootstrap (`cham-a.json` → `bootstrap.<cohort>.hieu`). BARO − CIRCA OLS+DA, MRR: dev30 [−0,074; 0,343]; dev19 [−0,137; −0,006], tức đổi chiều và không chứa 0. CIRCA OLS+DA − SimpleRCA, Hit@1: dev30 [−0,567; −0,033]; dev19 [−0,455; 0,143]. CIRCA OLS+DA − TORAI B, Hit@1: dev30 [−0,633; −0,067]; dev19 [−0,500; 0,111]. Cặp không có CIRCA: SimpleRCA − TraceRCA, MRR: dev30 [0,028; 0,246]; dev19 [−0,094; 0,285].
  - Tôi cài lại bootstrap theo ô một cách độc lập (numpy, cùng seed 20261005, B = 10.000) và ra đúng các khoảng trên ở cả hai cohort. Số đúng; vấn đề nằm ở cách đọc.
- **Đoạn có thể phản bác:** WHY-36 và báo cáo đã ghi "không phải mẫu ngẫu nhiên". Báo cáo không kết luận CIRCA hơn BARO và có câu "Không dùng thứ tự trung bình để tuyên bố phương pháp tốt nhất". Minh đã quyết không sửa CIRCA (Q-82), nên không có phép so phản thực nào sạch hơn. Những điều này đúng. Nhưng chiều lệch tính được ngay từ `cham-a.json`, không phải chạy gì thêm, và nó quyết định cách đọc bảng dev19 ở G2.
- **Hậu quả:** Ở G2 và P4, người đọc có thể hiểu "bỏ lỗi làm tròn thì CIRCA ngang hoặc hơn BARO", hay "SimpleRCA không còn hơn TraceRCA". Thực ra một phần lớn thay đổi đến từ việc bỏ ca dễ của phương pháp kia, và bỏ 3 ca ERROR của nhóm trace.
- **Đề xuất sửa:** Thêm 2–3 câu vào `cham-a.md`, ở mục "Phạm vi và cách đọc" và đầu các bảng dev19. Nội dung: Hit@1 trên 11 ca bị loại của từng phương pháp, kèm nguồn `cham-a.json`; dev19 chỉ dùng để xem một kết luận "X hơn CIRCA" trên dev30 có còn đứng; một khoảng nghiêng về CIRCA trên dev19 không đủ để nói CIRCA hơn X; các cặp không có CIRCA trên dev19 không dùng để diễn giải. Không đổi số. Việc ghi thêm chiều lệch vào mục "Giới hạn" của WHY-36 nằm ngoài phạm vi ghi của T-024; Minh quyết.

### R2. Báo cáo thiếu giới hạn "hòa bên trong RCD" mà giao thức yêu cầu, và chưa nói root không rơi vào nhóm hòa nào — KHÔNG CHẶN

- **Ở đâu:** `results/T-024/cham-a.md` các mục "Tính tay ba ca dev khác nhau…" (dòng 2279–2295) và "Kiểm hòa khối TORAI trong cohort thật" (dòng 2297–2309). Căn cứ là `results/T-022/giao-thuc-v2.md` §6.6: "Hòa bên trong RCD: chưa kiểm, ghi giới hạn."
- **Sai gì:**
  - (a) Báo cáo không ghi giới hạn hòa bên trong RCD: tìm chữ "RCD" trong `cham-a.md` ra 0 dòng.
  - (b) Hàng "khóa đơn có hòa" là ca BARO dev-03d4910932. Ở ca này root đứng hạng 1, không hòa với ai; nhóm hòa nằm ở hạng 41–43 (ts-config-mongo, ts-notification-mongo, ts-security-mongo). Báo cáo không nói rằng không bản ghi nào có root nằm trong nhóm hòa. Đó là lý do mọi cận bi quan/lạc quan đều bằng kỳ vọng.
- **Bằng chứng:**
  - Tôi đếm trên 420 bản ghi trong manifest, nối với `nhan-dev.json`: 0 bản ghi có root trong nhóm hòa hay trong khối cùng điểm. Bản ghi có hòa ở thực thể khác: SimpleRCA 30, BARO 18, TraceRCA 17, MicroRank 2.
  - Nhánh của khối TORAI chứa root (`extra.nhanh_khoi`): nguồn B có 81 khối một service, 9 khối dự phòng, 0 khối RCD; nguồn A có 63 khối một service, 25 khối dự phòng, 2 khối RCD (root đứng vị trí 1 trong khối).
  - Công thức nhóm hòa nhiều phần tử đã có test riêng ở T-030 (`results/T-030/tests/test_buoc2.py`, `test_nhom_hoa`; chạy lại 57/57 ở `test-chay-lai/`). Vì vậy không có lỗi tính toán.
- **Hậu quả:** Không đổi số nào. Người đọc có thể tưởng quy tắc hòa đã được kiểm trên ca thật, và báo cáo thiếu một giới hạn mà giao thức yêu cầu. Trên dev, giới hạn RCD không chạm dòng chính TORAI B; với TORAI A, nó chạm nhiều nhất 2/90 lượt.
- **Đề xuất sửa:** Thêm hai câu vào `cham-a.md`, nguồn là các bản ghi trong manifest. Câu một: root không nằm trong nhóm hòa ở mọi bản ghi `OK`, nên cận bằng kỳ vọng; công thức nhóm hòa được kiểm ở test T-030. Câu hai: hòa bên trong RCD chưa kiểm; trên dev, root TORAI B không nằm trong khối RCD nào, TORAI A có 2/90 lượt.

## Điều đã kiểm và thấy đúng

- **Tiêu chí xong:**
  - Ba file đầu ra có thật và parse được.
  - Dòng LOG chốt manifest lúc 22:20:19 đứng trước lượt evaluator đầu tiên; hash manifest trong `evaluator-001`/`002` trùng `freeze.json`.
  - Đủ sáu phương pháp × 30 ca, TORAI × 3 seed. 8 ERROR (MicroRank 4, TraceRCA 4) nằm ở mẫu số.
  - `cham-a.md` có đủ các mục SPEC liệt kê (54 bảng). Prompt phản biện chép nguyên văn mẫu.
- **Phạm vi ghi:** Từ 21:30 tới nay, ngoài `results/T-024/` chỉ đổi `docs/STATE.md`, `tasks/T-024/{LOG,SPEC}.md` (câu SPEC:62 có lời duyệt của Minh; `kiem-cuoi.json` kiểm đúng một chỗ thay) và `results/T-030/work/` (được phép). `results/T-025` và `tasks/T-025` là của phiên T-025. Không có `__pycache__` mới.
- **Số liệu:** Tôi tính lại Hit@1/3/5 và MRR cho 10 biến thể × 2 cohort trực tiếp từ bản ghi và nhãn: khớp hết. Bootstrap cài lại độc lập: khớp.
  - 11 ca bị loại trùng đúng tập ca có nút RHT > 1e10 trong bản ghi OLS. Tập này giống nhau ở hash seed 0, 1, 2 (`kiem-11-ca-hashseed.json`) và không dùng nhãn.
  - `window.t` bằng mốc tiêm ở cả 420 bản ghi; N và A mỗi bên 300 s.
- **Tách nhãn:** `worker.py` chỉ đưa bảng đã cắt và `t` vào adapter. TORAI A nhận DataFrame, không nhận đường dẫn chứa tên ca. `run.py` chỉ gọi `nhan.nap_moc`. `evaluate.py` nạp nhãn sau khi kiểm hash manifest, mã và cấu hình, và chặn `data/locked`.
- **Benchmark chính thức:** RCAEval `259ea41` là bản checkout sạch. `Evaluator(max_k=10)` và retrieval/rerank khớp §8.6. Có 383 bản ghi-ca không hòa cho AC@k bằng Hit@k.
  - Số README của BARO trùng nguồn. Lệnh tạo số đó dùng `--length 20` mặc định, tức 600 s mỗi phía (`main.py:122, 314–315`), còn P3 dùng 300 s. Báo cáo đã nêu cửa sổ là một nguyên nhân lệch, đúng.
- **Đối chiếu khác:** SimpleRCA dev30 (0,8333 / 0,9667 / 0,8911) trùng số T-017 trên cùng 30 ca. Số công bố FSE 2026 trên 90 ca RE2-TT là Top@1 0,80 (`results/T-017/so-cong-bo.csv`).
  - MicroRank xếp ts-station-service đầu ở 21/26 ca OK; `service_ranks_top11` của code gốc cũng vậy. Đây là hành vi của phương pháp, T-015 đã thấy.
  - TORAI: hạng root giống nhau ở cả ba seed.
- **Lượt hỏng được giữ:** job TraceRCA bị ngắt vẫn còn (31 thư mục lượt, 1 thư mục không có bản ghi). Khi tiếp tục, script dùng lại 2 bản ghi sau khi kiểm hash. Test 57/57 đạt lúc 21:59, trước evaluator.
- **DT18 và hướng dẫn của cô:** báo MRR và NDCG ở mức xếp hạng. Precision/Recall/F1 thuộc phần phát hiện (Q-30, T-025), nên ở đây không thiếu. Báo cáo không kết luận về đồ thị.
- **LESSONS:** không thấy lặp sai lầm. Số lấy từ file (SL17); tách theo ô và theo ca (QT15); không nêu mẫu hình từ trung bình (SL14).

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| R1 | **Đúng một phần — KHÔNG CHẶN** | Kiểm độc lập từ `cham-a.json.methods.<id>.per_case` và 420 bản ghi: mọi số Hit@1, bốn khoảng bootstrap, 3/4 ERROR bị loại và ô train/cpu bị loại đều khớp. Tuy nhiên “ca dễ” phụ thuộc phương pháp/độ đo: Hit@1 loại 11 → giữ 19 của SimpleRCA là 9/11→16/19, MicroRank 0/11→2/19; MRR TraceRCA tăng 0,7273→0,7734, trong khi BARO giảm 0,9148→0,6833. Không có một chiều lệch chung hoặc phép tách nhân quả chứng minh “một phần lớn” thay đổi do ca dễ. Báo cáo đã giới hạn nhóm 19 không ngẫu nhiên (`cham-a.md:12,393`) và chưa kết luận CIRCA hơn BARO; lỗi là thiếu mô tả cụ thể để đọc G2, không phải số hoặc kết luận sai đã xảy ra. Đồng ý thêm thành phần ca/ERROR và giới hạn mọi phép so dev19. Không đồng ý quy tắc “X hơn CIRCA vẫn đứng thì vững”: đó chỉ là bằng chứng độ nhạy trên hai cohort đã chọn, không bảo đảm tổng quát hóa. Cũng không cấm diễn giải cặp không CIRCA: vẫn mô tả hợp lệ **có điều kiện trên 19 ca**, không suy sang toàn 30/test. Sửa tối thiểu ở generator `scripts/report.py` và báo cáo `cham-a.md`, giữ số/bảng/CI; không tự sửa WHY hoặc thêm quy tắc diễn giải một chiều. Chi tiết số và đề xuất trong LOG phiên 4. | |
| R2 | **Đúng — KHÔNG CHẶN** | Báo cáo thiếu giới hạn yêu cầu tại `giao-thuc-v2.md:216` và `WHY.md:274`. Tự đếm nguồn: hòa ở thực thể khác BARO 18/SimpleRCA 30/TraceRCA 17/MicroRank 2; không root hòa **theo khóa đã lưu**. BARO dev-03d4910932 root hạng 1; nhóm hòa ở 41–43. TORAI root: B 81 đơn + 9 dự phòng + 0 RCD; A 63 đơn + 25 dự phòng + 2 RCD; hai lượt A là cùng dev-a5cabe5fa7, seed 0/1, root đứng 1 trong khối, hạng toàn cục 2. `_khoi` tạo nhóm đơn từ thứ tự RCD (`src/p3/adapters/torai.py:68–69`); `_rcd_multimodal` chỉ trả ranks (`src/torai/torai_sua.py:86–87`). Code RCD chính thức xếp theo p-value nhưng bản ghi không giữ khóa bên trong, nên đếm 0 không loại trừ hòa ẩn RCD. Phạm vi tiềm năng trực tiếp đối với độ đo root: B 0/90, A tối đa 2/90 lượt thuộc 1 ca; chưa có bằng chứng hai lượt đó thật sự hòa hoặc số hiện tại sai. Đồng ý bổ sung “theo khóa đã lưu” và giới hạn RCD, dẫn nguồn/test T-030; không đổi số, không chạy lại hay sửa thuật toán. Việc thiếu giới hạn này đã bị bỏ sót trong tự soát trước REVIEW; đính chính tại LOG phiên 4. | |
