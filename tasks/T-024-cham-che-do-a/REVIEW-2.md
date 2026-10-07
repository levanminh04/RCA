# Phản biện T-024 — lần 2

- **Người phản biện:** Claude — **Ngày:** 07/10/2026 — **Commit/diff đã đọc:** HEAD `3b1e0dd`. `git diff HEAD` chỉ có `docs/DECISIONS.md`, `docs/STATE.md`, `docs/WHY.md`. Mọi file T-024, `src/p3/` và kết quả T-022/T-030/T-031 chưa được git theo dõi; đã đọc trực tiếp.
- **Đã đọc:**
  - AGENTS.md; SPEC, LOG (cả phiên 1–5), REVIEW.md lần 1 của T-024.
  - `results/T-024/`: `cham-a.md`, `cham-a.json`, `ban-ghi-dua-vao-cham.json`, `kiem-truoc-chay.json`, `scripts/{run,evaluate,report,verify}.py`, `runs/*/{cau-hinh,tom-tat,tien-do}`, bản ghi từng lượt, `test-chay-lai/`, `work/protected-before.json`.
  - Code đã chạy: `src/p3/` (17 tệp: `danh_gia`, `ban_ghi`, `runner`, `worker`, `cua_so`, `selector`, `nhan`, mọi adapter); `src/simplerca/core.py`, `src/microrank/__init__.py` và `official.py` (phần xếp hạng), `src/torai/torai_sua.py` (phần cụm/RCD), `src/circa_kien_truc/scoring.py`; RCAEval `259ea41` `e2e/tracerca.py`, `benchmark/evaluation.py`.
  - Giao thức V2 §5, §6, §8–10; WHY-23, WHY-28, WHY-32; LESSONS; `results/T-031/moi-truong.json`, `runs/torai-B-ec2-001/cau-hinh.json`, `khoa-cau-hinh.md`; `results/T-017/so-cong-bo.csv`; DT18 và thư cô ngày 23/09.
- **Revision thực sự dùng:** hash `src/p3` tính lại hôm nay `8d4cc8196c87…`, trùng manifest và cấu hình cả 8 run nguồn. RCAEval `259ea41`, BARO `e35f4ec`, CIRCA `0215e18`: checkout sạch. `src/microrank`, `src/simplerca`, `src/circa_kien_truc`, `src/torai`: không đổi so commit `5636b69`. Vậy code hiện tại là code đã tạo bản ghi (trừ phần TORAI chạy trên EC2: hash code phương pháp ở EC2 không được ghi; T-031 đã phản biện phần này).

## Kết luận chung

Không có lỗi chặn. Tôi tự tính lại toàn bộ bảng chính dev30/dev19 từ 420 bản ghi gốc bằng code độc lập: khớp hết. Không thấy lỗi ở evaluator, bootstrap, mẫu số, ánh xạ thực thể hay tách nhãn. Hai điểm của REVIEW lần 1 đã được xử lý. Có một điểm mới, không chặn: báo cáo chưa nói thứ tự TraceRCA đưa vào chấm khác hẳn thứ tự hàm RCAEval trả về, và bảng "RCAEval riêng" của TraceRCA vì vậy không phải số RCAEval sẽ cho (N1).

## Đối chiếu điểm của REVIEW lần 1

| Điểm cũ | Tình trạng | Bằng chứng của tôi |
|---|---|---|
| R1 (nhóm 19 ca lệch theo chiều đo được) | **Đã xử lý** phần đứng vững | `cham-a.md:15–17` có Hit@1 loại 11/giữ 19 của sáu dòng chính, 3/1 ERROR, ô train/cpu mất; câu giới hạn ở dòng 17, 229, 400. Tôi tính lại Hit@1 từ bản ghi: khớp. Phần đề xuất "quy tắc một chiều" của R1 cũ không đứng vững hoàn toàn. Người làm chỉ ra đúng: MRR TraceRCA tăng (0,727 → 0,773) khi bỏ 11 ca, SimpleRCA gần như không đổi, nên "ca dễ" phụ thuộc phương pháp và độ đo. Không cần sửa thêm. |
| R2 (thiếu giới hạn hòa RCD) | **Đã xử lý** | `cham-a.md` mục "Kiểm hòa khối TORAI trong cohort thật" có câu "theo khóa đã lưu" và giới hạn RCD. Tôi đếm lại khối chứa root: B 81 đơn, 9 dự phòng, 0 RCD; A 63 đơn, 25 dự phòng, 2 RCD (đều ca dev-a5cabe5fa7). Khớp báo cáo. |

## Các điểm mới

### N1. TraceRCA: thứ tự đưa vào chấm khác thứ tự hàm RCAEval ở 26/26 ca; báo cáo chưa nói, và bảng "RCAEval riêng" bị gọi là "thứ tự gốc" — KHÔNG CHẶN

- **Ở đâu:**
  - Bước chịu ảnh hưởng: bảng RCAEval riêng (§8.6) và phần diễn giải TraceRCA ở bước 4.
  - `results/T-024/cham-a.md:77`: "Bảng giữ thứ tự gốc, bỏ trùng thực thể, `Evaluator(max_k=10)`". Dòng TraceRCA ở dòng 60 và bảng tương ứng của dev19.
  - Đường thực thi: `src/p3/adapters/tracerca.py:53–64` đặt `ranking_native` = danh sách `ji` hữu hạn do adapter tự sắp. Thứ tự hàm chính thức chỉ lưu ở `extra.ranks_chinh_thuc`. `src/p3/danh_gia.py:191` (`bang_rcaeval`) nạp `ranking_native`.
  - Căn cứ: WHY-23 nói bảng RCAEval "cho phép so với số công bố". WHY-32, mục Giới hạn, nói tác động NaN "phải báo".
- **Sai gì:**
  - Code không sai: lọc NaN rồi sắp lại đúng thiết kế đã duyệt (WHY-32, giao thức §6.4).
  - Lỗi nằm ở diễn giải và báo cáo. Với TraceRCA, "thứ tự gốc" trong bảng RCAEval riêng là thứ tự adapter đã sửa, không phải thứ tự hàm RCAEval trả về. Người đọc so dòng này với số TraceRCA của RCAEval sẽ so hai thứ khác nhau.
  - Báo cáo cũng không nêu tác động của việc lọc trên cohort này, dù WHY-32 yêu cầu báo.
  - Phép kiểm §6.4 "danh sách chính thức phải trùng danh sách sắp từ `ji_dict` khi không có NaN" không áp được lượt nào ở T-024. Cả 26 lượt OK đều có NaN. Vì vậy ở T-024 không lượt nào được đối chiếu thứ tự với code chính thức. Báo cáo và LOG ghi `key_check` đã chạy nhưng không nói điều này.
- **Bằng chứng** (Python `-B`, chỉ đọc manifest, bản ghi và `nhan-dev.json` sau đầu ra; không ghi file):
  - `runs/tracerca-30-001/tom-tat.json`: 26/26 lượt OK có `diagnostics.key_check = nan_present`, `ji_nan` từ 16 đến 71.
  - So `ranking_native` với `extra.ranks_chinh_thuc`: cùng tập operation, khác thứ tự ở 26/26 lượt. Hạng root ở mức thực thể khác nhau ở 9/26 lượt (adapter → chính thức): dev-12a1a88069 2→12, dev-20acb4402d 4→10, dev-260d332c8d 9→18, dev-3defe3d34b 1→14, dev-59f696a169 1→15, dev-7f1b6b071d 1→12, dev-8017c6dc70 1→3, dev-a915aa2424 1→12, dev-f36d0647d5 3→13.
  - Cùng quy tắc bỏ trùng và giữ ERROR ở mẫu số, dev30: adapter cho AC@1/3/5 = 0,7000/0,8000/0,8333, MRR 0,7565 (khớp `cham-a.json`). Thứ tự chính thức cho 0,5333/0,6000/0,6000, MRR 0,5818. Dev19: 0,6842/0,8421/0,8947 so với 0,4737/0,5789/0,5789.
- **Đoạn có thể phản bác:** tên dòng đã là "TraceRCA lọc hữu hạn". WHY-32 đã quyết bỏ thứ tự lỗi. T-015 đã đo hiện tượng này (14/90 ca). Thứ tự chính thức khi có NaN còn phụ thuộc thứ tự dòng span, nên không phải một "đáp án đúng" để báo thay. Những điều này đúng, và tôi không đề xuất đổi số chính. Nhưng cỡ tác động trên chính cohort này (Hit@1 lệch 0,17) đủ lớn để làm đổi cách đọc các cặp có TraceRCA, nhất là khi so với số công bố. Cỡ đó tính được ngay từ bản ghi đã chốt.
- **Hậu quả:** người đọc ở G2/P4 có thể coi dòng TraceRCA trong bảng RCAEval riêng là số RCAEval sẽ cho trên cùng ca. Họ cũng có thể không biết rằng dùng thứ tự của code gốc thì TraceRCA ngang CIRCA OLS+DA về Hit@1 trên dev30, không ngang BARO.
- **Đề xuất sửa:** chỉ sửa văn bản ở `scripts/report.py` rồi sinh lại `cham-a.md`; không đổi `cham-a.json`, số hay bảng. Thêm 2–3 câu cạnh bảng RCAEval riêng và trong phần giới hạn:
  - Với TraceRCA, "thứ tự gốc" là danh sách `ji` hữu hạn do adapter sắp (WHY-32), không phải thứ tự hàm RCAEval trả về.
  - Hai thứ tự khác nhau ở 26/26 lượt OK; hạng root khác ở 9/26. Nếu dùng thứ tự hàm thì AC@1 = 0,5333 (nguồn: `extra.ranks_chinh_thuc` trong bản ghi đã chốt). Chỉ ghi số này để mô tả, không thay số chính.
  - Mọi lượt OK có NaN, nên phép kiểm thứ tự khi không có NaN (§6.4) không áp được lượt nào ở T-024.

## Điều đã kiểm và thấy đúng

- **Tính lại độc lập:**
  - Tôi viết lại phép chấm, không import `danh_gia`. Code đọc 420 bản ghi qua manifest (kiểm SHA-256), tính phân bố hạng root (nhóm hòa phẳng; TORAI liệt kê mọi hoán vị khối) rồi tính Hit@1/3/5/10, MRR, NDCG@5, Avg@5, Rerank@1(K=5).
  - So với `summaries.<cohort>.main` cho 11 dòng × 2 cohort: 0 lệch.
  - Dựng lại `cham-a.md` trong bộ nhớ từ `cham-a.json` bằng `report.Report`: giống từng byte (301.665 ký tự).
- **Evaluator** (`danh_gia.py`):
  - Công thức khối TORAI: xác suất 1/[s·C(s−1,m)] cho tập con m khối đứng trước, đúng §8.4.
  - Cận lạc quan/bi quan chỉ cho độ đo đơn điệu; Rerank là tỉ số gộp.
  - Ca không OK cho mọi độ đo bằng 0 và vẫn ở mẫu số.
  - Bootstrap: lấy lại ô, ghép cặp bằng cùng ma trận trọng số; Rerank N/A khi mẫu số 0.
  - Random theo O/U đúng §8.7.
  - `khoi_tu_ban_ghi` chặn khóa không hữu hạn, thực thể trùng và khối không giảm dần.
- **Hòa:** 0 bản ghi OK có root trong nhóm hòa theo khóa đã lưu. Vì vậy mọi cận bằng kỳ vọng và quy tắc hòa không đổi số nào của cohort. TORAI: 0/180 bản ghi có hai khối cùng điểm.
- **Adapter và khóa:**
  - BARO: tính lại điểm và kiểm khớp thứ tự chính thức ở 30/30.
  - SimpleRCA: thứ tự gốc sắp theo `(−score, tên)`; adapter dùng `score` làm khóa và coi thứ tự theo tên là hòa. Đúng WHY-17.
  - MicroRank: `full_ranks` sắp giảm dần theo `scores` (`official.py:230`); khóa đúng.
  - CIRCA: khóa DA `(score, −index, z)` theo §8.4.
  - TORAI: khối dựng lại phải khớp `ranks` chính thức; seed 0/1/2 đổi thứ tự ở 16 cặp ca × nguồn nhưng không đổi hạng root.
- **ERROR:** MicroRank và TraceRCA lỗi ở cùng 4 ca, cùng một operation `ts-order-other-service_getMore ts.orders` có sau mốc mà không có trong 300 s trước. Đây là hợp đồng trạng thái đã khai trước (§6.3, §6.4). Báo cáo giữ 4 ca ở mẫu số và ghi giới hạn.
- **Tách nhãn:**
  - Runner chỉ gọi `nap_moc`. Worker đưa bảng đã cắt và `t` vào adapter. `ban_ghi.kiem` chặn trường nhãn.
  - `evaluate.py` nạp nhãn sau khi kiểm hash manifest, mã và cấu hình.
  - Tập 19 ca lấy từ `kiem-11-ca-hashseed.json` (đầu ra CIRCA, không dùng nhãn).
  - TORAI A suy thư mục file tác giả từ tên ca ở runner. Phương pháp chỉ nhận DataFrame; giới hạn hồi cứu của nguồn A đã ghi.
- **Cửa sổ:** `window` của mỗi lượt có N và A đúng 300 s, `spans_N`/`spans_A` khác 0; span cắt theo µs.
- **Phạm vi ghi:** so `work/protected-before.json` (4.734 tệp) với hiện tại: chỉ `tasks/T-024-cham-che-do-a/SPEC.md` đổi, đúng câu Minh duyệt (LOG phiên 3).
- **Tiêu chí xong:** ba file đầu ra có thật và parse được. Dòng chốt manifest (22:20:19) đứng trước evaluator. Đủ 6 phương pháp × 30 ca, TORAI × 3 seed. 8 ERROR ở mẫu số. Đủ các mục SPEC liệt kê.
- **Đối chiếu số công bố:** báo cáo chỉ so BARO với README theo đúng phạm vi SPEC (`docs/knowledge/`). Ngoài phạm vi đó, `results/T-017/so-cong-bo.csv` và LESSONS ST10 có Top@1 FSE 2026 trên 90 ca RE2-TT: SimpleRCA 0,80; BARO 0,67. Số dev30 (0,8333; 0,7000) gần các mốc này. Đây là ghi chú, không phải lỗi.
- **DT18 và thư cô:** bảng có MRR và NDCG. Precision/Recall/F1 thuộc phần phát hiện (T-025). Báo cáo không kết luận về đồ thị.
- **LESSONS:** không thấy lặp sai lầm. Số lấy từ file (SL17); tách theo ô và theo ca (QT15); có phép thử hoán vị root.

**Lệnh đã chạy** (đều chỉ đọc, bằng `py -3 -B` hoặc `D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B`; script tạm ở scratchpad ngoài repo):

1. Tính lại hash `src/p3`, `git status` và `rev-parse` của RCAEval, BARO, CIRCA.
2. Tính lại 11 dòng × 2 cohort từ bản ghi và so `cham-a.json`.
3. Đếm root trong nhóm hòa, khối TORAI theo nhánh, thứ tự TORAI giữa các seed.
4. So thứ tự TraceRCA adapter với thứ tự chính thức; tính AC@k/MRR theo cả hai thứ tự.
5. Đếm thực thể ngoài U (SimpleRCA có `istio-init` ở 1 ca, đúng §8.1).
6. So `protected-before.json` với hiện tại.
7. Dựng báo cáo trong bộ nhớ và so với `cham-a.md`.

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| N1 | **Đúng — KHÔNG CHẶN** | Tự kiểm adapter, WHY-32 và 30 bản ghi có hash khớp: 26/26 OK có NaN và khác thứ tự hàm gốc; hạng root đổi 9/26. Hit@1 dev30 adapter 21/30, hàm 16/30; dev19 13/19 và 9/19. Code lọc hữu hạn đúng thiết kế; lỗi là gọi thứ tự adapter là “thứ tự gốc” và thiếu phạm vi phép kiểm không NaN. Đã sửa nguồn sinh báo cáo và sinh lại cham-a.md: nêu rõ thứ tự bản triển khai, mức ảnh hưởng và giới hạn; số hàm chỉ mô tả, không làm đáp án thay số chính. Giữ nguyên số/bảng, không sửa thuật toán hoặc chạy lại. Chi tiết và tự soát sau sửa ở LOG phiên 6. | |
