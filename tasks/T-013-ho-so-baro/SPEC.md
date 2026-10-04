# T-013 — Hồ sơ BARO, biến thể N-Sigma và hai bộ phát hiện

- **Trạng thái:** đã tự duyệt theo ủy quyền Minh ngày 04/10/2026.
- **Người làm:** Codex. **Người phản biện:** Claude.
- **Thuộc gói MRP:** P1 — **Cổng:** G1. **Ý định:** EXECUTE.

## Mục tiêu

Trả lời nhận xét “chưa sâu kỹ thuật của từng phương pháp” của cô và RQ1. Giải thích cơ chế, đầu vào, điều kiện chạy; cung cấp dữ kiện cho G1. Không chọn dataset, cửa sổ P3 hay phương pháp đồ thị.

## Đầu vào

Đã đọc AGENTS, STATE, LESSONS, review-prompt, hai mẫu SPEC/LOG, MRP §2–7, WHY, DECISIONS, DT18 và hướng dẫn cô. Đọc và kiểm lại T-001 mục 1/3/4/8/9, T-005, T-006 mục 2/3/4/8/10/11 và cham, BOCPD T-007, K1 §3 và BARO. Code chỉ đọc: D:/RCA-ext/src/baro (e35f4ec), D:/RCA-ext/src/RCAEval (259ea41). Bài: https://arxiv.org/html/2405.09330v1; BOCPD gốc https://arxiv.org/abs/0710.3742. Revision đầy đủ và hash ghi trong manifest.

FACT: HEAD hai repo khớp; chưa có thư mục T-013 khi mở phiên. USER_CONFIRMED: prompt cho tự duyệt SPEC và triển khai trong phạm vi nêu dưới. OPEN: cửa sổ P3 (Q-54), protocol chế độ b, mọi lựa chọn chưa có WHY. Không biến kết quả kỹ thuật thành DECIDED.

## Đầu ra và tác động

- `ho-so-baro.md`: chín mục, kèm N-Sigma RCA và so hai bản code.
- `ho-so-bocpd.md`, `ho-so-nsigma-phat-hien.md`: chín mục mỗi hồ sơ.
- `vi-du-tinh-tay.md`, `cua-so-va-che-do-b.md`: ví dụ hai ca và giải thích cửa sổ/ba đường rò.
- `yeu-cau-dau-vao.csv`: đúng 16 cột của prompt; BARO DataFrame/dict, RCAEval BARO, N-Sigma RCA, BOCPD, N-Sigma detector là các dòng riêng.
- `ca-da-chay.csv`, `dinh-chinh-task-cu.md`, `de-xuat-tai-lieu-chung.md` bắt buộc.
- `moi-truong.md`, `manifest.json`, `kiem-tra.json`, `doi-chieu-moc.json`, `scripts/`, `runs/`, `trung-gian/`: cách dựng/chạy, bằng chứng độc lập, mọi lượt kể cả hỏng.

Tác động chỉ T-013 và một dòng mục lục STATE; task cũ và tài liệu chung giữ nguyên. Nháp đính chính nằm trong T-013. Đây là danh sách triển khai nằm trong đúng outcome và phạm vi đã được Minh ủy quyền trong prompt, không cần gate duyệt SPEC lần nữa.

## Phạm vi ghi

Chỉ `tasks/T-013-ho-so-baro/SPEC.md`, `LOG.md`, `results/T-013/`, `D:/RCA-ext/work/T-013/`, và đúng một dòng T-013 trong `docs/STATE.md`. Root giữ quyền ghi LOG/STATE. Hai subagent chỉ đọc và báo bằng chứng, không reviewer chính, không ghi file. Không ghi vào source/env cũ; đặt PYTHONDONTWRITEBYTECODE=1. Không cài gói mới nếu môi trường ghim có đủ. Không commit/push.

## Chọn ca trước khi nhìn kết quả

1. TT: trong đúng 30 thư mục `data/rcaeval/re2tt_*`, chọn `metrics.parquet` có dung lượng lớn nhất; hòa thì đường dẫn tương đối tăng dần. Chỉ metadata kích thước dùng để chọn. Không xét service, loại lỗi, rank. Dùng bảng số đo; chỉ đọc mốc tiêm cho chế độ (a). Nhãn service chỉ đọc sau khi lưu ranks.
2. OB: đối chiếu hash `simple_data.csv` trong `D:/RCA-ext/data/fse-ob` với mẫu README đã tải ở T-006 (`D:/RCA-ext/dl/baro-simple_data.csv`). Nếu có bản trùng, chọn đường dẫn tăng dần đầu tiên; nếu không, chọn ca `simple_data.csv` đầu tiên theo đường dẫn tăng dần có kết quả code chính thức trong khối mốc A T-006. Quy tắc không xét nhãn/rank. Liên kết mốc A tái lập toàn dataset được dùng lại, không gọi một ca là tái lập toàn bảng bài báo.
3. Detector kiểm trên prefix tối đa 120 điểm của cùng hai ca (cấu hình/quy mô mới, lý do b) và mẫu tổng hợp; N-Sigma có thêm nguyên ca đã chọn. BOCPD full TT đã vượt 1 giờ ở T-005: không chạy lại. Dùng số T-005/T-007 cho tổng chi phí. Không benchmark toàn dataset.

## Các bước (phụ thuộc và lệnh kiểm)

0. Kiểm file thật/HEAD, dữ liệu được phép và đầu ra cũ; ghi manifest và LOG mở phiên. Tra bảng công bố TRƯỚC mọi lượt mới; lưu bảng số mốc và loại A/B/C. Kiểm: `git rev-parse HEAD`; đọc JSON/cham và tar chỉ các thành viên cho phép; kiểm danh sách đầu vào bằng script.
1. Sau bước 0 về source, audit song song hai nhóm code/bài: RCA và detector. Hai subagent chỉ đọc. Root soát SPEC độc lập, bổ sung edge case trước chạy. Kiểm: source file có dòng/section; `git status --short` ở hai source.
2. Sau SPEC và môi trường/mốc ở 0, chọn hai ca theo quy tắc. Script độc lập tự làm sạch/tách/công thức; gọi code chính thức trong nhánh so sánh riêng, thu điểm bằng lớp ghi lại scaler, không sửa source. Lưu từng metric, quantile/mean/scale/max và ranks. Kiểm: `D:/RCA-ext/envs/py312-pin/Scripts/python.exe results/T-013/scripts/kiem_co_che.py`; sai số tương đối/ tuyệt đối ≤1e-10 cho từng điểm hữu hạn, ranks bằng nhau ngoài hòa.
3. Cùng đầu vào bước 2: chạy lại, đảo thứ tự cột, hai đoạn đều trước mốc; kiểm detector prefix và synthetic bằng cài lại độc lập (không gọi hàm tác giả trong nhánh độc lập), posterior/điểm/hit. Kiểm đầu ra rỗng/dự phòng và trung gian; ghi tiến độ từ trước lời gọi đầu. Không ép phép thử giả phải đạt: ghi thẳng rank là tương đối, detector có thể báo động giả hoặc nhánh dự phòng.
4. Sau 0 và 2: dùng lại số cửa sổ T-006; phân rã trên hai ca ở 10/20 phút để giải thích median/IQR hoặc mean/std, thay tập cột và max hậu sự cố; không chọn cửa sổ. Kiểm từng ô JSON cũ và giá trị mới; không chỉ trung bình. Đọc các kết luận liên quan trong T-000–012, không sửa task cũ. Có lỗi thì có phản ví dụ/mã sửa trong T-013.
5. Sau 1–4: viết hồ sơ/csv và nháp tài liệu chung, đánh dấu chờ WHY tại chỗ lựa chọn mới. Kiểm đủ chín mục, đúng header CSV, không số từ trí nhớ, mỗi kết luận nêu nguyên nhân khả thi khác.
6. Sau 5: tự kiểm toàn diff/file set, mọi tiêu chí, đối chiếu prompt reviewer nguyên văn; thêm báo cáo A–H và sáu ý bàn giao LOG. Chỉ chuyển một dòng STATE sang chờ phản biện. Kiểm script `kiem_ban_giao.py`, `git diff --check`, inventory đầy đủ, source/env không đổi; không dùng diff làm phạm vi review.

## Edge case: cách kiểm và cách xử lý

| Ca biên | Kiểm | Cách xử lý trong hồ sơ/phép kiểm |
|---|---|---|
| IQR=0 nhưng không hằng | synthetic normal có nhiều 0 và một gai; hậu thay đổi | soi sklearn scale=1, điểm thô và ảnh hưởng đơn vị; không sửa code |
| Hằng toàn cửa sổ hoặc chỉ một nửa | synthetic trước/sau | kiểm bỏ cột từng nửa và giao cột; có thể loại chính kênh đổi mức |
| NaN/inf/NaN đầu chuỗi | synthetic đủ các vị trí | tách core và runner ffill/fill0; báo lỗi/NaN hoặc im lặng, không gán “đúng” |
| Nhiều metric/service | hai ca và synthetic | max metric/service tương đương bỏ trùng lần xuất hiện đầu; không cộng điểm |
| Hòa điểm | synthetic và đảo cột | stable sort giữ thứ tự đầu vào khi hòa; báo khoảng rank/tie, không tự chọn luật G1 |
| Mốc tiêm có đơn vị khác | timestamp giây và ×1000; BOCPD timestamp so index | phân biệt timestamp/index, `anomalies[0]` DataFrame dùng head/tail; minh họa lỗi khi timestamp epoch bị dùng làm vị trí |
| Tên cột khác dataset | time/Time, suffix latency/latency-90/lat50/error/mem | so chọn cột, fallback BOCPD, rename của runner; cần mapping schema rõ |
| Bình thường quá ngắn/rỗng | 0/1/3 điểm; detector T<100 | ghi lỗi/đầu ra rỗng; tối thiểu code khác tối thiểu thống kê; không đặt ngưỡng mới |
| BOCPD O(T²) bộ nhớ | matrix shape source và prefix | tính tổng runtime N×t và peak RAM tuần tự, không cộng peak mọi ca; không chạy >1h |
| Hazard/prior | ghi default theo dimension và thử synthetic nhỏ hai giá trị | không chọn lại hyperparameter bằng nhãn; giải thích phụ thuộc prior |
| Changepoint sát biên | synthetic đổi ở đầu/cuối | hậu quá ngắn, diff heuristic và phần khởi động/fallback; không khẳng định online từ kết quả batch |
| Đảo cột BOCPD/N-Sigma | synthetic + hai ca | so tập/sort timestamps riêng với order list; N-Sigma trả theo cột, trùng timestamp |
| Dict/DataFrame BARO | synthetic n chẵn/lệch âm | quantile theo index và abs(max-med) khác signed max; không gộp hai implementation |
| Tỷ lệ lấy mẫu không phải 1Hz | synthetic irregular time | row window không là time window; find_cps trả index, merge theo đơn vị time |
| Chuỗi đều bình thường | hai đoạn trước mốc và synthetic | ranking luôn ra ứng viên không phải cảnh báo có nghĩa; detector ghi false positive/fallback |

## Kiểm đúng đắn

Tra Table 2/3/5/6 BARO trước chạy; đối chiếu mốc A T-006 và T-007 đã lưu với file thật. Không tái benchmark cả bảng (P3), nên chưa khẳng định tái lập toàn bảng trên cấu hình T-013. Chỉ 1–2 ca mới để kiểm lặp lại và cơ chế.

Mọi nhánh tính tay không gọi helper tác giả. So từng score/prediction/posterior với nhánh chính thức. Lặp lại tất định, đảo cột, không rỗng, không trùng thứ tự cột ngoài hòa có giải thích, không fallback im lặng, phép thử normal-normal và soi trung gian. Nếu code không đạt invariant thì ghi thất bại của code, không làm yếu tiêu chí để đạt. Detector có cost matrix/prefix chỉ chứng minh cơ chế, không chứng minh phát hiện toàn ca TT. Không bỏ kiểm rẻ nào thuộc phạm vi. Phần bỏ: benchmark full dataset và BOCPD full TT; hệ quả không có số hiệu quả/khả thi toàn tập mới.

## Tiêu chí xong

1. Ba hồ sơ đủ chín mục; BARO có N-Sigma RCA, so hai code và dict; mọi default có file:dòng, tác giả có section/link.
2. Hai ca được chọn bằng rule ghi trước; CSV mọi metric với trung gian, sai số ≤1e-10 và official ranks; label chỉ nối sau rank. Có mốc A dùng lại file thật và báo phạm vi của mốc.
3. BOCPD và N-Sigma detector có ví dụ độc lập, posterior/threshold đối chiếu; mọi edge case trong bảng có kết quả hoặc lý do thực sự ngoài giới hạn.
4. Window 10/20: chênh ô N-Sigma cũ kiểm bằng JSON và cơ chế từng ca; ba leak paths và điều kiện dataset chế độ b rõ; không tự chốt.
5. Đủ bốn file bắt buộc prompt, header 16 cột chính xác; ledger mọi ca/phương pháp/mục đích/a-b-c. Không có thì ghi không có.
6. LOG append-only đủ mở phiên/HEAD/ủy quyền/khối task nguyên văn/tiến độ/sáu ý cuối/A–H/prompt nguyên văn common+G1 và liệt kê toàn đầu ra; STATE chỉ dòng T-013.
7. Hoàn tất kiểm diff/phạm vi nguồn bất biến, parse JSON/CSV và báo mọi chưa kiểm/cần Minh quyết. Không sửa task cũ.

## Không làm

Không data/locked, không RE2-TT ngoài 30 ca dev và một ca torai-TT cho phép, không archive. Không EC2, deep research, hơn hai subagent, benchmark P3, phân tích hạn chế P4 bằng số toàn tập, thiết kế detector/đồ thị mới, tải dataset mới, gói phần mềm mới, commit/push hay tin ra ngoài. Source/env cũ chỉ đọc.

## Chi phí ước lượng

Hai subagent chỉ đọc độc lập để giảm thời gian chờ, theo ủy quyền prompt tối đa hai subagent. Không tải dataset; tải văn bản bài nếu cần <5 MB, ghi URL/byte/hash. Runs BARO/N-Sigma hai ca + synthetic ước lượng <5 phút; detector prefix hai ca + synthetic <10 phút; N-Sigma nguyên ca <2 phút; tổng dự kiến <20 phút compute, không lượt >1h. Chi phí toàn dataset suy từ kết quả cũ, không đo mới khi máy bận. Không số thời gian chính thức. Dung lượng output dự kiến <30 MB.

## Rủi ro và điều chưa chắc

OPEN: tài liệu code-vs-bài cần audit; môi trường py312-pin đúng WHY-15 nhưng bộ của tác giả không công bố đầy đủ; không suy tương đương mọi nền tảng. Mốc tập không xác minh từng score; ví dụ độc lập bổ sung. STATE phần “Task đang mở” lỗi thời so mục lục nhưng prompt hiện hành giao T-013 rõ, chỉ thêm dòng T-013, không sửa phần chung. Lựa chọn mapping/service hoặc protocol mới ghi nháp WHY và chờ Minh, không dùng như quyết định G1.

## Thay đổi trong lúc làm (chỉ thêm)

- 04/10: `py312-pin` không có engine Parquet. Lượt đầu dừng trước khi chạy phương pháp, giữ progress/failure. Dùng môi trường `py312` đã có chỉ để đọc Parquet và xuất mảng float64 NPZ trong `D:/RCA-ext/work/T-013/`; tính toán phương pháp vẫn bằng pin. Kiểm hash nguồn, hash NPZ, shape và round-trip mảng; không cài gói hay sửa env/source. Đầu ra ngoài repo thêm `metrics-selected.npz`, `metrics-selected.json` trong phạm vi work đã cho phép. Không đổi rule chọn ca.
- 04/10: mốc tiêm ca TT chọn theo rule không có trong sáu file T-005; dùng đúng file nhãn dev đã kiểm và lưu ở T-002, không mở cases.parquet trong locked và không suy midpoint. Lệnh pipfreeze không có trong uv venv; dùng uv metadata và phục hồi checks đã lưu thay vì lặp lại runs. Các điều chỉnh đều trong phạm vi ghi/đọc ban đầu.
- 04/10: tự kiểm cuối phát hiện JSON mốc T-013 chép nhầm các ô RobustScorer[t_inject]; đối chiếu Table3 nguồn gốc, sửa đúng dòng và giữ bản trước sửa ở runs/moc-truoc-dinh-chinh.json. Không có phép đo toàn bảng hoặc lựa chọn tham số nào dựa vào các ô chép nhầm, nên không chạy lại method chỉ để sửa lỗi chép bảng.
