# T-022 — Văn bản mục WHY trình Minh duyệt (bản 2)

Ngày 05/10/2026. T-022 phiên 3, người soạn Claude. **Cập nhật 06/10/2026: Minh duyệt văn bản, gồm D1–D12 (DECISIONS Q-76); đã chép nguyên văn mục WHY-22–35 và hai ghi chú WHY-17, WHY-19 vào `docs/WHY.md`. `docs/WHY.md` là bản hiệu lực; file này giữ làm lịch sử.** Đoạn dưới là trạng thái lúc soạn: Minh duyệt văn bản một lần (Q-74 Q15); khi duyệt thì chép nguyên các mục dưới vào cuối `docs/WHY.md`. Bản 1 (`de-xuat-why.md`) giữ nguyên làm lịch sử.

**Mã mục.** Đề xuất WHY-22 đến WHY-35, theo thứ tự dưới. Nếu T-023 ghi mục WHY trước thì dịch mã; nội dung không đổi.

**Đã sửa so với bản 1** (theo phản biện giao thức, Q15):
- A1 (cửa sổ): bỏ suy luận "300 + 300 s trùng `--length 10` nên cùng cấu hình đã tái lập". Cùng độ dài, không cùng thông tin (WHY-22, "Giới hạn").
- A2 (Retrieval/Rerank): bỏ "phá hòa theo tên"; Retrieval/Rerank ở bảng chính theo quy tắc hòa chung; hàm RCAEval ở bảng riêng (WHY-23).
- A4 (cột BOCPD): bỏ "chạy từng ca nên không thành đường học nhãn"; nêu schema là kênh thông tin hồi cứu (WHY-25).
- Mọi mục C cũ viết lại theo Q-74.

**Sửa sau phản biện V2 (06/10/2026)**, Minh duyệt "sửa theo đề xuất" (LOG phiên 4); sửa tại chỗ. Phản biện và phản hồi: `tasks/T-022-giao-thuc-p3/REVIEW.md`, phần "Phản biện T-022 — giao thức P3 bản 2".
- WHY-22: thêm ngoại lệ thời điểm thông tin cho TORAI A và BOCPD (V2-R3).
- WHY-23: bỏ suy luận "cho P4 biết tìm cơ chế ở bước nào"; quy về bước dùng bốn tập của WHY-26 (V2-R4).
- WHY-28: khóa TORAI hai cấp (V2-R2).
- WHY-29: luật tên cột trace TT; K-B1 so theo tên cột; giới hạn câu "cho biết B có dựng đúng đặc tả" (V2-R1, N1).
- WHY-34: thay lý do chọn cả bản ghi; thêm giới hạn nền 720 s (N2).

**Sửa sau phản biện tiếp (06/10/2026)**, Minh duyệt "sửa theo đề xuất" (LOG "Phiên 5 (tiếp 2)"); sửa tại chỗ. Phản biện và phản hồi: `REVIEW.md`, phần "Phản biện tiếp T-022 — bản V2 sau sửa ngày 06/10/2026".
- WHY-28: `ERROR` gồm cả đầu ra vi phạm điều kiện hợp lệ đã khai (V2-S1); cận do hòa chỉ cho độ đo đơn điệu, Rerank@1 không có cận (V2-S2).
- WHY-34: kiểm posterior BOCPD hữu hạn, không đạt → `ERROR` (V2-S1); lý do danh sách cột theo cả bản ghi không đổi báo động N-Sigma tới τ (V2-S3).

**Sửa sau kiểm lại (06/10/2026)**, Minh duyệt "sửa theo đề xuất" (LOG "Phiên 6 (tiếp)"); sửa tại chỗ. Phản biện và phản hồi: `REVIEW.md`, phần "Kiểm lại T-022 sau sửa V2-S1–S3".
- WHY-30: phép kiểm (2) tính route hồi quy từng nút; nút có cha rơi về z-score sau `ValueError` không tính là SVR chạy thành công; ghi route cho mô hình được khóa, cả OLS (V2-T1).
- WHY-28: giới hạn `TIMEOUT` khai trước khi chạy; cách tính khi hết ngân sách tổng (N3).

**Chi tiết thực thi D1–D12.** Q-74 chưa nói tới các chi tiết này; văn bản dưới viết theo đề xuất của Claude. Minh duyệt văn bản là duyệt cả các chi tiết này. Không đồng ý điểm nào thì Minh nói, Claude sửa văn bản. Bảng đầy đủ: `giao-thuc-v2.md` mục 15. Vị trí: D1, D2, D3 (WHY-22, WHY-30); D4 (WHY-29); D5 (WHY-30); D6, D12 (WHY-31, WHY-28); D7, D8 (WHY-35); D9 (WHY-34); D10 (WHY-28); D11 (WHY-32).

**Không viết WHY cho:** Q1 (tách T-030) và Q16 (chỗ ghi phản biện) là tổ chức công việc, đã có ở DECISIONS Q-74. Cách chọn ca pilot chỉ ảnh hưởng phép chiếu chi phí, không vào số khoa học; nó nằm trong SPEC T-030 và `giao-thuc-v2.md` mục 12.

---

## Văn bản đề xuất ghi vào `docs/WHY.md`

## WHY-22. Cửa sổ dữ liệu P3 và cách cắt trên từng nguồn — Đã quyết (Q-64, Q-74 Q2)

- **Chọn:** đoạn bình thường N = [t−300 s, t), đoạn sự cố A = [t, t+300 s), theo timestamp, nửa mở; N không chồng lần tiêm trước. Metric theo cột thời gian. Span chỉ vào khi bắt đầu ≥ t−300 và kết thúc < t+300. Log theo thời điểm dòng log. Runner cắt trước; tiền xử lý của tác giả chạy sau, chỉ trên dữ liệu trong cửa sổ. Bên trong cửa sổ, mỗi phương pháp chia N/A theo code tác giả đã kiểm ở P1. CIRCA dùng điểm quan sát thật cuối cùng trước t+300 làm điểm test cuối; đồ thị gọi dựng từ span đã kết thúc trước t. Thiếu dữ liệu thì ghi độ dài thực, không kéo dài cửa sổ. Nezha: chỉ áp cho metric. Eadro: dữ liệu bình thường lấy từ phiên no-fault (chưa kiểm; T-023).
- **Vì sao:** độ dài cửa sổ quyết định bộ nào có đủ dữ liệu bình thường, nên phải chốt cùng gói dataset ở G1. RE2-TT có 720 s trước mốc; Nezha có 482–521 s giữa hai lần tiêm; Eadro không có đoạn bình thường trước tiêm trong phiên. Biên cửa sổ là giới hạn thông tin: kết quả RCA có lúc t+300, nên chỉ dữ liệu đã có lúc đó được vào. Vì vậy span chưa kết thúc bị loại, điểm ngoài cửa sổ không được điền vào biên, và giá trị trước t−300 không được kéo vào bằng `ffill`. Ngoại lệ có khai báo: TORAI nguồn A dùng bin của tác giả phủ tới t+305 và ngưỡng `tracets_lat` tính trên toàn file (WHY-29); BOCPD ở chế độ (b) tiền xử lý trên cả bản ghi nên t̂ chỉ có sau cuối bản ghi (WHY-34). Các nhánh này chỉ có kết quả sau cuối file; chúng là hồi cứu, không cùng giới hạn thông tin t+300 / t̂+300 với các nhánh khác.
- **Phương án đã xét:** ±600 s (`--length 20`, cấu hình so mốc bài TORAI, WHY-16): không đủ nền ở Nezha. Toàn bản ghi: chỉ có ở RE2. Cắt theo số dòng như `main.py`: sai nghĩa khi dữ liệu có lỗ hoặc nhịp khác 1 s. Lọc span theo thời điểm bắt đầu: nhận span chưa kết thúc lúc t+300. Giữ thứ tự `main.py` (ffill toàn file rồi cắt): ô trống đầu cửa sổ nhận giá trị trước t−300. CIRCA `current = t+300`: điểm test cuối là giá trị điền, không quan sát.
- **Bằng chứng:** `results/T-021/goi-g1.md` §6 câu 2; `results/T-022/runs/allowlist-001/kiem-allowlist.json` (30/30 ca dev RE2-TT có mốc ở giây 720); RCAEval `259ea41` `main.py:308–315`, `RCAEval/classes/data.py:89–104`; `src/circa_kien_truc/scoring.py:38`; `tasks/T-022-giao-thuc-p3/REVIEW.md` (phản biện giao thức, điểm 1 và Q2).
- **Giới hạn:** cùng 300 + 300 s không có nghĩa cùng thông tin với `main.py --length 10` hay với cấu hình T-006 đã tái lập: khác thứ tự `ffill`, điểm cuối của CIRCA, lưới 15 s của dữ liệu TORAI tác giả. Kết quả nhạy với độ dài nền: trên 25 ca fse-OB DELAY, nền 300 → 360 dòng làm Avg@5 BARO giảm 0,224 (`results/T-013/cua-so-va-che-do-b.md:18`); không chọn cửa sổ theo phân tích đó. MicroRank khớp mốc bài ở ±600 s (T-007), nên số MicroRank, TraceRCA P3 không so trực tiếp với Bảng 2 bài TORAI.
- **Kết luận phụ thuộc:** mọi số P3 chế độ (a); cửa sổ RCA quanh báo động ở chế độ (b) (WHY-35); WHY-19 (ghi chú dưới).

## WHY-23. Báo Retrieval@K và Rerank@1 — Đã quyết (Q-65, Q-74 Q10)

- **Chọn:** với mọi phương pháp RCA, báo Retrieval@K (service gốc nằm trong K thực thể đầu) và Rerank@1 = AC@1 / Retrieval@K, K ∈ {5, 10}. Bảng chính tính hai độ đo này theo cùng quy tắc hòa với mọi độ đo khác (WHY-28). Bảng RCAEval riêng gọi `Evaluator.retrieval_service` và `rerank_service` của RCAEval `259ea41` (`RCAEval/benchmark/evaluation.py:162–210`) với `max_k = 10`, trên thứ tự gốc của phương pháp; ca không `OK` nạp danh sách rỗng.
- **Vì sao:** Hit@1 không cho biết root ở gần đầu hay ở xa. Retrieval@K và Rerank@1 tách hai trường hợp trên danh sách cuối: root nằm ngoài K thực thể đầu, và root nằm trong K đầu nhưng không đứng đầu (bài DecompRCA). Với phương pháp chỉ trả một thứ hạng, chính bài DecompRCA lấy tập ứng viên là K phần tử đầu (`results/T-018/decomprca.md:16`), nên "không truy hồi" ở đây là quy ước định nghĩa trên thứ hạng cuối, không chỉ ra bước nào của phương pháp hỏng. Muốn quy về bước, dùng bốn tập của WHY-26: root ngoài tập quan sát (đầu vào không có tín hiệu của root); trong tập quan sát nhưng không được trả về; được trả về nhưng hạng > K (lỗi ở điểm hoặc thứ tự). Tính từ thứ hạng đã có, không tốn chạy thêm. Bảng RCAEval giữ đúng hàm mà Q-65 chỉ định và cho phép so với số công bố.
- **Phương án đã xét:** định nghĩa theo K metric như Bảng 1 DecompRCA: với hệ ít service, bộ chọn ngẫu nhiên 15 metric đã trúng 0,82–0,90 (RE1-OB, RE1-SS), nên mức trần chủ yếu do cấu trúc. Không báo: mất phép tách. Chỉ dùng hàm RCAEval cho bảng chính: hàm không xử lý hòa, nên thứ tự cột thành bằng chứng.
- **Bằng chứng:** `results/T-018/decomprca.md` mục 3–4; `results/T-018/runs/b9-retrieval-ngau-nhien.json`; `results/T-021/goi-g1.md` §6 câu 3.
- **Giới hạn:** ở mức thực thể với một root, Retrieval@K = Hit@K và Rerank@1 là tỉ số gộp của hai tỉ lệ (`evaluation.py:203–210`); đây là cách trình bày khác của cùng thứ hạng, không phải bằng chứng độc lập (WHY-06). `Evaluator` mặc định `max_k = 5` trả `None` cho K = 10 (`evaluation.py:9`). `main.py:552–553` bỏ ca lỗi khỏi mẫu; bảng RCAEval của P3 không bỏ.
- **Kết luận phụ thuộc:** mô tả ở P4 root nằm ngoài K đầu hay trong K đầu nhưng không đứng đầu của danh sách cuối. Việc quy hạn chế về một bước của phương pháp dựa trên bốn tập (WHY-26) và giá trị trung gian đã lưu, không dựa riêng trên Retrieval/Rerank.

## WHY-24. Mốc tiêm ở chế độ (a) và ngân sách nhãn — Đã quyết (Q-66)

- **Chọn:** ở chế độ (a), mốc tiêm là thông tin vận hành biết trước, chỉ runner chế độ (a) đọc. Chỉ service gốc và loại lỗi là nhãn chấm. Ngân sách nhãn root của mọi baseline bằng 0: không học, không chọn cấu hình, không chọn ca bằng nhãn root. Kết quả chế độ (a) luôn báo cạnh chế độ (b).
- **Vì sao:** trong RCAEval, bản code P1 đã kiểm, mọi baseline tầng 1 nhận mốc tiêm (`main.py:311–315`); bài BARO báo riêng các dòng `[t_inject]`; RCAEval chạy TORAI bằng mốc tiêm thay `t̂_A` (`results/T-016/ho-so-torai.md:35`). Bỏ chế độ (a) thì không so được với số công bố. MicroRank bài gốc có bộ phát hiện trace riêng; bản P3 là bản RCAEval sửa đầu vào, nhận mốc tiêm. Không baseline nào trong Q-38 học từ nhãn root.
- **Phương án đã xét:** chỉ chạy chế độ (b): mất phép so với bài gốc, không tách được lỗi phát hiện khỏi lỗi xếp hạng.
- **Giới hạn:** chế độ (a) dễ hơn thực tế vì biết đúng lúc lỗi bắt đầu. Mốc tiêm không phải lúc biểu hiện. Ở chế độ (b), mọi đường suy ra mốc (tên ca, đường dẫn, file nhãn, cắt quanh mốc) bị cấm (luật cứng 6).
- **Bằng chứng:** `results/T-021/goi-g1.md` §6 câu 4; MRP §4, P3; `results/T-013/ho-so-baro.md` §1, §8.
- **Kết luận phụ thuộc:** cách đọc mọi số chế độ (a); tách nhãn chấm khỏi đầu vào phương pháp trong mọi adapter P3.

## WHY-25. Tập cột BOCPD và chạy qua đêm — Đã quyết (Q-67, Q-72)

- **Chọn:** BOCPD dùng **tập cột** theo `reproduce_bocpd`: tên chứa `latency-50` hoặc `_error`, bỏ `queue-master` và `rabbitmq_` (BARO `e35f4ec`, `baro/reproducibility.py:140–145`). Q-67 chỉ chọn tập cột, không chọn cách cắt 300 + 300 quanh mốc của hàm đó. Q-72: BOCPD chế độ (b) trên RE2-TT dev chạy qua đêm trên EC2 ở T-025, tối đa 20 giờ, đầu vào không chọn theo mốc tiêm, ghi tiến độ từng ca, giữ lượt hỏng; kết luận chi phí ghi cho bản cài BARO, không cho thuật toán BOCPD.
- **Vì sao:** đây là quy ước tác giả dùng khi báo kết quả phát hiện. Hàm `bocpd()` tự chọn mọi cột chứa `latency` và `_error`; ở T-005 nó chọn 76 cột và mất 1.440 s cho 600 điểm; cả ca 1.441 điểm không xong trong 1 giờ. Chi phí xấp xỉ O(T²d³) (`results/T-013/ho-so-bocpd.md` §9), nên giảm số cột theo đúng tác giả là cách giảm chi phí. Q-40 giới hạn 3 giờ cho toàn ca một dataset; Q-72 là ngoại lệ riêng cho BOCPD.
- **Phương án đã xét:** báo "không chạy đủ trong ngân sách" (áp cho CIRCA-PC ở Q-67); chạy một mẫu ca; cắt quanh mốc như `reproduce_bocpd` (cấm ở chế độ b, luật cứng 6); giữ 76 cột của `bocpd()`.
- **Giới hạn:** trên RE2-TT dev, tập cột này có 25–48 cột thô mỗi ca; số cột `_error` 3–20 và đổi theo ca (`results/T-022/cot-bocpd-dev.csv`). Sự có mặt cột `_error` tương quan với service gốc (`results/T-018/dinh-chinh-task-cu.md`, D1). Vậy số chiều đầu vào, chi phí và độ nhạy của BOCPD đổi theo lỗi. Tập cột và bước bỏ cột hằng dùng cả bản ghi, nên ở chế độ (b) đây là thông tin hồi cứu; chạy riêng từng ca không loại được ảnh hưởng này. Chi phí trên 1.441 điểm với tập cột này **chưa đo**; ngoại suy từ cấu hình cũ (≈ 69 giờ cho 30 ca) không áp cho cấu hình này.
- **Bằng chứng:** `results/T-005/do-kha-thi.md` bảng 2b; `results/T-013/trung-gian/chi-phi-va-sentinel.json`; `results/T-021/goi-g1.md` §6 câu 5; DECISIONS Q-67, Q-72.
- **Kết luận phụ thuộc:** mọi số phát hiện BOCPD P3; lịch và chi phí T-025.

## WHY-26. Tập ứng viên, ánh xạ thực thể và bốn tập báo cáo — Đã quyết (Q-74 Q4)

- **Chọn:** chấm ở mức thực thể (service hoặc thành phần như DB). Universe U = 68 thực thể `ts-*` của RE2-TT, chốt từ metadata 30 ca dev, không từ nhãn: 41 `-service`, 26 DB, `ts-ui-dashboard`. Ánh xạ: metric → tiền tố trước `_` đầu tiên; span → `serviceName`; TORAI → `<service>_A`; bỏ trùng giữ lần đầu. Báo riêng bốn tập: inventory (U), tập quan sát của phương pháp, tập chấm (U), tập trả về (gồm cả thực thể ngoài U, đếm riêng). Phương pháp không có bằng chứng cho một thực thể thì không xếp nó; không điền phần thiếu. Mức ngẫu nhiên tính trên tập quan sát của phương pháp, kèm trên U.
- **Vì sao:** DT18 coi nút là "dịch vụ hoặc thành phần hệ thống"; RCAEval và TORAI xếp cả DB. Điền phần thiếu cho phương pháp điểm nhờ may. Mức ngẫu nhiên đúng phải dựa trên các thực thể phương pháp thật sự xếp; RCAEval cũng đếm ứng viên sau tiền xử lý (`main.py:322–329`).
- **Phương án đã xét:** chỉ `-service` (lệch RCAEval, TORAI); gộp DB vào service chủ (chưa có bảng sở hữu từ kiến trúc); điền ngẫu nhiên phần thiếu; mức ngẫu nhiên trên U (sai khi phương pháp chỉ thấy một phần U).
- **Bằng chứng:** `results/T-022/mappings/universe-re2tt-dev.json`, `runs/universe-001/`; `results/T-015/bang-ung-vien-tt.csv` (3 ca: 27 thực thể có trace trong ±600 s).
- **Giới hạn:** phương pháp trace chỉ thấy phần U có trace; trần coverage thấp không phải bằng chứng các thực thể vắng là vô can.
- **Kết luận phụ thuộc:** mọi độ đo xếp hạng; trần coverage MicroRank, TraceRCA.

## WHY-27. Bộ cột metric — Đã quyết (Q-74 Q5)

- **Chọn:** mỗi ca dùng cột có trong file của ca, qua tiền xử lý của từng phương pháp. Không bỏ cột `_error`. Không điền cột vắng. Không chạy bộ cột cố định L\*. Evaluator ghi audit số cột và cột vắng; P4 kiểm ảnh hưởng của schema.
- **Vì sao:** bỏ cột `_error` làm yếu baseline (LESSONS QT7). L\* (giao cột 30 ca dev, T-018) bỏ 23/25 cột `_error`, nên chênh giữa bản dùng cột trong file và L\* trộn hiệu ứng schema với việc mất tín hiệu lỗi; phép so đó không tách được hai phần.
- **Phương án đã xét:** hợp cố định, cột vắng điền NaN/0; giao cố định L\*; đối chứng L\* chạy kèm (đề xuất của phản biện; không chọn vì lý do trên).
- **Bằng chứng:** `results/T-018/dinh-chinh-task-cu.md` D1; `results/T-018/ho-so-gdn.md`; REVIEW T-022 (phản biện giao thức, điểm 6, Q5).
- **Giới hạn:** schema là một kênh thông tin. Số và loại cột đổi theo ca và tương quan root; nó đổi số alert SimpleRCA (WHY-17), số chiều BOCPD (WHY-25), tập ứng viên BARO, đồ thị metric CIRCA. Chạy riêng từng ca chỉ loại đường học xuyên ca, không loại ảnh hưởng này. Ở chế độ (a), cột bị bỏ vì hằng trong cửa sổ được xác định từ dữ liệu có sẵn lúc t+300.
- **Kết luận phụ thuộc:** BARO, CIRCA, TORAI, SimpleRCA, BOCPD, N-Sigma; mọi nhận định P4 có thể do schema.

## WHY-28. Chấm xếp hạng: trạng thái lỗi, một quy tắc hòa, bootstrap theo cặp ô — Đã quyết (Q-74 Q9, Q10)

- **Chọn:**
  - Trạng thái mỗi lượt: `OK` (danh sách khác rỗng); `NO_EVIDENCE` (phương pháp trả về bình thường với danh sách rỗng, giữ status gốc); `ERROR` (phương pháp ném ngoại lệ, giữ thông điệp; hoặc đầu ra vi phạm điều kiện hợp lệ đã khai trước: posterior BOCPD không hữu hạn, WHY-34); `TIMEOUT` (vượt giới hạn mỗi lượt khai trong SPEC của task chạy, trước khi chạy); `UNSUPPORTED`. Mọi trạng thái khác `OK` ở mẫu số, tính trượt. Ngân sách tổng (Q-40, Q-72): phép chiếu pilot vượt ngân sách thì quyết trước khi chạy, như Q-67 ("không chạy đủ trong ngân sách", không báo số); đã cam kết chạy đủ cohort mà hết ngân sách giữa chừng thì ca chưa chạy là `TIMEOUT`. Lỗi dữ liệu và lỗi runner sửa trước bảng khoa học, giữ lượt hỏng.
  - Hòa: hai phần tử hòa khi khóa xếp hạng thật của phương pháp bằng nhau. Khóa: BARO max robust z (tính lại bằng đúng lời gọi của hàm, phải ra đúng thứ tự chính thức); SimpleRCA, MicroRank điểm trong đầu ra; TraceRCA `ji` (WHY-32); CIRCA DA `(score, −index, z-score)`, RHT-only `score`; TORAI khóa hai cấp: khối là cụm (khóa = điểm cụm), trong khối là thứ tự RCD hoặc `y_train` ở nhánh dự phòng; dựng lại từ biến cục bộ, nối khối theo đúng code và phải ra đúng thứ tự chính thức. Các cụm cùng điểm chỉ hoán vị cả khối, giữ thứ tự trong khối; kỳ vọng tính chính xác trên các hoán vị khối (`giao-thuc-v2.md` §8.4), không coi mọi service của các cụm đó là một nhóm hòa. Mọi độ đo của bảng chính (MRR, NDCG@5, Hit@1/3/5, Avg@5, Retrieval@5/10, Rerank@1) tính kỳ vọng khi thứ tự trong nhóm hòa ngẫu nhiên đều. Cận lạc quan và bi quan (root ở hạng nhỏ nhất, lớn nhất) chỉ báo cho độ đo đơn điệu theo hạng root (Hit@k, MRR, NDCG@5, Avg@5, Retrieval@K). Rerank@1 là tỉ số gộp, mẫu số đổi theo hạng nên không đơn điệu (`giao-thuc-v2.md` §8.4 có phản ví dụ): chỉ báo giá trị chính và bootstrap. Root vắng → 0.
  - Bảng RCAEval riêng (WHY-23) trên thứ tự gốc.
  - Bootstrap: lấy lại 10 ô dev (root × loại lỗi) có hoàn lại, mỗi ô mang cả 3 ca; B = 10.000; seed 20261005; khoảng phân vị 95 %. So hai phương pháp thì dùng cùng mẫu lấy lại. Phương pháp nhiều seed: trung bình theo seed của từng ca trước. Mẫu có Retrieval = 0 thì Rerank là N/A, đếm số mẫu N/A.
  - Báo theo loại lỗi, ô, nhóm vị trí root và từng ca; số ca theo trạng thái.
- **Vì sao:** hai quy tắc hòa cho hai độ đo khác nhau trên cùng thứ hạng (hai thực thể cùng điểm, root đứng trước theo tên: Hit@1 kỳ vọng 0,5, AC@1 theo tên 1). Phá hòa theo tên hay thứ tự cột biến chúng thành bằng chứng (MRP P3). Điểm vô hướng bằng nhau chưa chắc là hòa khi phương pháp sắp theo khóa nhiều thành phần (CIRCA DA). TORAI nối trọn từng khối cụm (`src/torai/torai_sua.py:296–360`), nên hòa điểm cụm chỉ cho phép đổi chỗ cả khối: hai khối cùng điểm AB, CD với root A cho E[RR] = 2/3; coi bốn service là một nhóm hòa cho 25/48 (REVIEW T-022, V2-R2). Bỏ ca lỗi khỏi mẫu như `main.py:552–553` làm số đẹp hơn thật. Ba lần lặp của một ô gần như giống nhau, nên lấy mẫu theo ô (WHY-04, MRP P7); ghép cặp vì khác biệt giữa hai phương pháp mới là đại lượng cần khoảng.
- **Phương án đã xét:** kỳ vọng cho Hit/RR/DCG nhưng phá hòa theo tên cho hàm RCAEval (bản 1, mâu thuẫn); coi phương pháp chỉ trả thứ tự là không hòa (giữ thứ tự cột làm bằng chứng); TORAI coi mọi service của các cụm cùng điểm là một nhóm hòa, hoặc sắp phẳng theo tuple (trái cách code nối khối); bỏ ca lỗi khỏi mẫu; bootstrap theo ca; bootstrap không ghép cặp.
- **Bằng chứng:** REVIEW T-022 (phản biện giao thức, điểm 4, Q9, Q10); `RCAEval/graph_heads/rht.py:285`; `src/circa_kien_truc/scoring.py:66–68`; `RCAEval/e2e/baro.py:52–55`; `src/torai/torai_sua.py:286–366`; WHY-17 (quy ước hòa của SimpleRCA).
- **Giới hạn:** 10 cụm là ít; khoảng phân vị có thể hẹp hơn thực, và chỉ nói về tập ô này. Hòa bên trong bước RCD của TORAI chưa kiểm.
- **Kết luận phụ thuộc:** mọi bảng xếp hạng P3, P7.

## WHY-29. Nguồn đầu vào TORAI: chạy cả dữ liệu tác giả và bản tự dựng — Đã quyết (Q-74 Q3)

- **Chọn:** chạy TORAI bản sửa (WHY-19) trên hai nguồn. A: `logts.csv`, `tracets_err.csv`, `tracets_lat.csv` của tác giả (torai-TT). B: tự dựng từ parquet RE2 trên lưới 15 s gốc ở t−300 (20 bin mỗi phía); tên cột trace theo luật TT ở `giao-thuc-v2.md` §6.6 (operation chuẩn hóa; span chỉ có tên phương thức HTTP gán cho service của span con); `tracets_lat` học ngưỡng μ + 3σ trên span đã kết thúc trước t; `logts` bằng Drain riêng mỗi service (drain3 0.9.11, ngưỡng 0,4) học trên log trong cửa sổ. B làm dòng chính nếu qua cả ba phép kiểm khai báo trước, không dùng nhãn; không qua thì A làm dòng chính, ghi lệch lưới và ngưỡng toàn file. Không đổi sau khi thấy số.
  - K-B1: dựng `tracets_err`, `tracets_lat` theo quy ước tác giả (lưới của file tác giả, ngưỡng toàn file) và luật tên cột TT cho 30 ca dev; so với file tác giả theo đúng tên cột (cột, bin), không gộp về service; mọi ô của cột không ghép được tính là sai; ≥ 95 % ô trùng cho từng chuỗi, gộp 30 ca (như S9 của T-016). Thử tối đa 3 cách dựng, giữ mọi lần thử, chỉ so với file tác giả, chưa chạy TORAI. Luật tên cột sai ở ca khác mà không sửa được thì K-B1 để OPEN và trình Minh.
  - K-B2: tổng đếm mỗi service trong `logts` B bằng số dòng log của service đó trong cửa sổ, ở cả 30 ca.
  - K-B3: TORAI sửa chạy trên B ở 30 ca × 3 seed không lỗi.
- **Vì sao:** A không nhận cùng cửa sổ thông tin với các phương pháp khác: ở ca `re2tt_ts-auth-service_cpu_1`, lưới tác giả lệch 10 s so với đầu file, nên N phủ [t−295, t+5) và A phủ [t+5, t+305); ngưỡng `tracets_lat` tính trên toàn file, gồm sau mốc. B cùng nguồn và cùng cửa sổ với các phương pháp khác, nhưng là đầu vào khác tác giả và chưa kiểm trên TT. Phép kiểm khai báo trước, không nhìn kết quả xếp hạng. K-B1 cho biết phần trace của B (tên cột, gán service, đếm theo bin) có khớp file tác giả hay không khi dựng theo cùng quy ước; nó không kiểm `logts` (K-B2 chỉ kiểm tổng log tự nhất quán) và không kiểm lưới, ngưỡng riêng của B. K-B1 phải so theo cột vì TORAI tính z từng cột, chia tổng cả nguồn rồi mới cộng theo service (`src/torai/torai_sua.py:176–200, 206–235`); tổng (service, bin) trùng vẫn có thể cho điểm khác (REVIEW T-022, V2-R1). Ngưỡng 95 % và cách so theo tên cột lấy từ tiêu chí S9 của T-016 (`tasks/T-016-ho-so-torai/SPEC.md:95`).
- **Phương án đã xét:** chỉ A (đúng dữ liệu tác giả, lệch cửa sổ); chỉ B làm chính không điều kiện (đề xuất của phản biện; B chưa kiểm trên TT); A chính, B kiểm độ nhạy (bản 1).
- **Bằng chứng:** `results/T-016/dung-logts-tracets.md` §3–5 (đặc tả `tracets` khớp 100 % / 99,75 % trên OB; `logts` tốt nhất 50,2 % ô); LOG T-022 phiên 1 (20:25); REVIEW T-022 (phản biện giao thức, điểm 1, Q3); header `tracets_err.csv` của torai-TT (tên cột TT khác quy tắc OB); luật tên cột TT cho 157/157 tên cột ở ca dev `re2tt_ts-auth-service_cpu_1` (LOG T-022 phiên 4).
- **Giới hạn:** `logts` B khác tác giả (mốc thời gian log và cấu hình Drain chưa biết). Ca `re2tt_ts-auth-service_cpu_1` không có log parquet nhưng file tác giả có 223.924 lượt log; A và B nhận bằng chứng log khác nhau ở ca này. Lệch lưới A mới kiểm ở 1/30 ca. Luật tên cột TT mới kiểm tên ở 1/30 ca, chưa so giá trị ô. Ở Nezha, Eadro chỉ dựng được kiểu B.
- **Kết luận phụ thuộc:** mọi số TORAI P3; so TORAI với SimpleRCA (cùng dùng log); TORAI ở chế độ (b).

## WHY-30. CIRCA đồ thị kiến trúc ở P3 — Đã quyết (Q-74 Q6)

- **Chọn:** scorer RHT + DA (θ = 3), báo kèm RHT-only cùng lượt. Mô hình hồi quy khóa trước khi chạy evaluator: `ANMRegressor(regressor=SVR(kernel="sigmoid"))` như thực nghiệm bài nếu qua bốn phép kiểm không dùng nhãn, không thì LinearRegression. Bốn phép kiểm: (1) đúng cấu hình bài, gọi qua lớp RCAEval `RHTScorer(regressor=…)`, không sửa code; (2) 30/30 ca dev chạy không ném lỗi, mọi z hữu hạn, và không nút có cha hiệu lực nào rơi về z-score sau `ValueError` (ghi route từng nút: không cha, hồi quy thành công, `value_error_fallback`); (3) chạy hai lần cho đầu ra giống hệt; (4) tổng 30 ca ≤ 3 giờ (Q-40). Tên trong bảng: "CIRCA kiến trúc, SVR(sigmoid)+RHT+DA, cấu hình P3" hoặc "…, OLS+RHT+DA, cấu hình P3". Đồ thị gọi dựng từ span có thời điểm bắt đầu ≥ t−300 và kết thúc < t. Giữ metric cô lập làm ứng viên không cha. Điểm test cuối là điểm quan sát thật cuối cùng trước t+300. Builder chạy với `PYTHONHASHSEED=0`; dựng lại với hash seed 1, 2 ở 30 ca để đo độ nhạy (đếm ca đổi cạnh và đổi thứ hạng DA), không chọn seed theo kết quả.
- **Vì sao:** CIRCA theo bài là RHT + DA; thực nghiệm bài dùng SVR(sigmoid) (`CIRCA/circa/experiment/comparison/models.py:583–586`). "Đã kiểm" không chứng minh OLS là bản mạnh nhất, nhưng chọn mô hình bằng accuracy dev là dùng nhãn root (Q-66); phép kiểm không dùng nhãn chỉ trả lời "SVR có chạy đúng và đủ ngân sách không". Đồ thị chỉ từ span đã kết thúc trước mốc để không chứa cạnh do sự cố tạo ra. Builder nhạy với hash seed: seed 1 đổi cạnh ở 24 ca có call/meta graph chu trình.
- **Phương án đã xét:** OLS + RHT-only (khớp RCAEval CIRCA-PC, không phải CIRCA của bài); OLS + RHT + DA không xét SVR; chọn SVR hay OLS theo accuracy dev (cấm); coverage gốc (mất metric im lặng); đồ thị từ trace N∪A.
- **Bằng chứng:** `results/T-014/ho-so-circa-kien-truc.md:107–117, 148–150`; `results/T-014/dinh-chinh-task-cu.md:45–49`; `RCAEval/graph_heads/rht.py:133–164, 285`; REVIEW T-022 (phản biện giao thức, điểm 6, Q6).
- **Giới hạn:** T-014 đã thấy số SVR trên 25 ca MEM fse-OB (`results/T-014/ho-so-circa-pc.md:141`); số đó không được dùng làm căn cứ chọn. Cửa sổ RHT 1 s khác ý nghĩa thời gian của bài (1 phút). 300 s trace có thể thiếu cạnh ít lưu lượng so với 720 s của T-014; ghi số cạnh. Metric graph là DAG ở 30/30 ca, nhưng điều đó không chứng minh cấu trúc đúng giả định nhân quả của tác giả. RHT bắt `ValueError` của hồi quy rồi dùng z-score trực tiếp, không báo lỗi (`RCAEval/graph_heads/rht.py:118–124`); đường này có ở cả SVR và OLS, nên đầu ra hữu hạn không chứng minh hồi quy đã chạy. Vì vậy ghi route từng nút cho mô hình được khóa (như `src/circa_kien_truc/scoring.py:44–57`) và báo số nút rơi về z-score cạnh bảng CIRCA; lỗi do đầu vào NaN/inf xảy ra như nhau với OLS (REVIEW T-022, V2-T1). Số nút này trên 30 ca TT chưa kiểm.
- **Kết luận phụ thuộc:** mọi số CIRCA P3; mọi nhận định "đồ thị kiến trúc giúp hay không" ở P4.

## WHY-31. MicroRank-RCAEval sửa đầu vào ở P3 — Đã quyết (Q-74 Q7)

- **Chọn:** cửa sổ WHY-22. Xếp đầy đủ mọi operation có điểm làm chính; báo kèm danh sách cắt top-11 của code. Thực thể = `serviceName`; điểm thực thể = điểm operation cao nhất. Giữ hợp đồng lỗi của code: `ValueError` khi có operation sau mốc không có nền, std nền không xác định (< 2 span), ID trùng khác nội dung, khóa mơ hồ, điểm không hữu hạn → `ERROR`, giữ thông điệp; trả về rỗng với `missing_window`, `no_anomalous_traces`, `no_normal_traces` → `NO_EVIDENCE`, giữ status gốc. `PYTHONHASHSEED=0`, kiểm thêm seed 1 trên ca pilot. Trước pilot, T-030 chạy MicroRank trên 30 ca chỉ để đếm ca lỗi theo nguyên nhân (không chạy evaluator) và báo Minh; có ≥ 1 ca lỗi thì dừng chờ Minh.
- **Vì sao:** `top_max` là tham số định dạng, không thuộc công thức điểm (T-015 §2.5); MRR, NDCG cần đủ thứ hạng. Đổi cách xử lý operation thiếu nền là đổi phương pháp. Mỗi ca lỗi tính trượt (WHY-28), nên nếu cửa sổ ±300 s làm nhiều operation thiếu nền, MicroRank bị phạt có hệ thống vì lựa chọn cửa sổ; Minh cần thấy số này trước khi có số khoa học.
- **Phương án đã xét:** giữ top-11 làm chính; coi operation mới là bất thường hoặc bỏ qua nó (đổi phương pháp, chưa có nguồn); ngưỡng dừng 3 ca (một ô).
- **Bằng chứng:** `src/microrank/__init__.py:31–56, 68–70, 94–103`; `results/T-015/ho-so-microrank.md`; REVIEW T-022 (phản biện giao thức, điểm 2, Q7).
- **Giới hạn:** chưa đếm số ca lỗi ở ±300 s (T-007 khớp mốc ở ±600 s). Không dùng số T-007 làm đích cho bản sửa.
- **Kết luận phụ thuộc:** số MicroRank P3; trần coverage.

## WHY-32. TraceRCA bản lọc hữu hạn ở P3 — Đã quyết (Q-74 Q8)

- **Chọn:** gọi hàm RCAEval `e2e/tracerca.py` nguyên trạng; đọc `ji_dict` lúc hàm trả về bằng `sys.setprofile` (cùng cách `src/circa_kien_truc/scoring.py:60–65` đọc `DAScorer`); giữ operation có `ji` hữu hạn, sắp giảm dần. `ji` NaN (support 0, hoặc không có span bất thường) → không xếp. Danh sách rỗng → `NO_EVIDENCE`; `KeyError` khi có operation mới sau mốc → `ERROR`. Thực thể = `serviceName`, lấy từ cặp (operation, serviceName) trong dữ liệu; một operation ứng nhiều service → `ERROR`. Điểm thực thể = `ji` cao nhất. Kiểm: khi không có NaN, danh sách sắp từ `ji_dict` phải trùng danh sách chính thức; trên ca pilot, `ji` phải khớp phép tính độc lập của T-015.
- **Vì sao:** hàm sắp cả NaN rồi mới bỏ (`tracerca.py:86–93`); NaN phá phép so sánh nên thứ tự sai, và lọc danh sách trả về không sửa được. `ji_dict` là biến cục bộ; đọc nó lúc trả về giữ nguyên công thức của tác giả. Bỏ NaN trùng ý định "ignore ji nan" của tác giả (`:90`).
- **Phương án đã xét:** lọc danh sách trả về (bản 1, không sửa được thứ tự); cài lại công thức (cầu nối, rủi ro lệch); support 0 xếp cuối với điểm 0 (thêm ứng viên giả ở đáy); giữ lỗi sắp (chỉ để tái dựng T-007).
- **Bằng chứng:** `results/T-015/tracerca-rcaeval.md` §2, §5–6; `results/T-015/runs/tracerca-audit/seed0/` (T-007: đổi thứ tự dòng làm đổi thứ hạng; lọc hữu hạn đổi vị trí service gốc ở 14/90 ca, gồm cả đổi quy tắc hòa); REVIEW T-022 (phản biện giao thức, điểm 3, Q8).
- **Giới hạn:** tác động NaN và hòa báo gộp, không quy cho một lỗi. Zero-support nhiều thì Retrieval thấp do quy ước; phải báo.
- **Kết luận phụ thuộc:** số TraceRCA P3.

## WHY-33. SimpleRCA ở P3 dùng quy ước M4 của T-017 — Đã quyết (Q-74 "Thêm")

- **Chọn:** SimpleRCA ở P3 là "SimpleRCA (M4, quy ước T-017)" theo đúng WHY-17: metric mean + 3σ (ddof 0, một phía, `>`), đơn vị alert "events"; trace P95 tỉ lệ 3; log từ khóa ERROR/FAIL/EXCEPTION, ngưỡng 0; tổng điểm toàn 0 → abstain (`NO_EVIDENCE`); hòa theo nhóm điểm. Cửa sổ WHY-22: runner lọc span (kết thúc < t+300) trước khi gọi adapter T-017, vì adapter chỉ lọc theo thời điểm bắt đầu.
- **Vì sao:** WHY-17 đã ghi lý do từng quy ước và để ngỏ việc chọn cho P3; giữ nguyên tránh chọn lại sau khi T-017 đã thấy số dev. Lọc span trước là để theo giới hạn thông tin của WHY-22 mà không sửa code T-017.
- **Phương án đã xét:** đơn vị "channels"; P95 cho metric; ngưỡng log khác (đã kiểm độ nhạy ở T-017, không chọn theo accuracy).
- **Bằng chứng:** WHY-17; `src/simplerca/adapter.py:55–82`; `results/T-017/runs/fix-n1n2-001/`.
- **Giới hạn:** số `results/T-017/runs/run-dev-005/` (±300 s, lọc span theo thời điểm bắt đầu) không dùng lại nguyên trạng ở P3. Điểm "events" tăng theo số cột và độ dài cửa sổ (WHY-17).
- **Kết luận phụ thuộc:** số SimpleRCA P3.

## WHY-34. Chế độ (b): chuỗi đầu vào và hai bộ phát hiện — Đã quyết (Q-74 Q11, Q12)

- **Chọn:** gọi là **phát hiện hồi cứu trên bản ghi đã chọn vì có sự cố**. Bộ phát hiện nhận cả bản ghi 1.441 điểm, một lần, không khởi động lại, không nhận mốc tiêm, root, loại lỗi, tên hay đường dẫn ca.
  - BOCPD: tập cột WHY-25; tiền xử lý giữ code tác giả trên cả chuỗi (bỏ cột hằng, `ffill`, điền 0, min–max), khai báo là look-ahead. Gọi `online_changepoint_detection` nguyên trạng, rồi tính lại run length `m[i] = argmax R[:, i+1]` (sau khi thấy điểm i), i = 0..T−1; điểm đổi là i ≥ 1 có `|m[i] − m[i−1]| > 1` (luật `find_cps`). Không còn sentinel. Ghi kèm điểm đổi của `maxes` gốc để đối chiếu. Trước `argmax`, mọi phần tử R[:, 1..T] phải hữu hạn; không đạt → `ERROR` (WHY-28), ca ở mẫu số, tính trượt; không điền 0, không cắt chuỗi.
  - N-Sigma: k = 3, `startsfrom = 100`, mean/std chỉ dùng quá khứ. Cột chính = tập cột BOCPD; đối chứng = mọi cột. Tiền xử lý: `inf → NaN`, `ffill`; không min–max, không bỏ cột hằng. Báo động gộp mọi cột, sắp thời gian, bỏ trùng.
- **Vì sao:** Q-74 Q11 chọn cả bản ghi. Cách này không phải chọn độ dài và bước đoạn, và SPEC T-022 cấm chia đoạn để vừa chi phí. Mốc luôn ở giây 720 không phải lý do để chọn giữa cả bản ghi và chia đoạn: cả hai đều đặt mốc ở vị trí cố định. Code gốc gán `maxes[t]` từ posterior chưa thấy điểm t và để `maxes[T] = 0`, sinh một điểm đổi giả ở cuối mọi ca (`_bocpd.py:196, 212–225`); tính lại từ R sửa cả hai mà không đổi code. Cùng tập cột thì so được hai bộ phát hiện; đối chứng mọi cột cho biết kết luận có phụ thuộc việc giới hạn cột không. Luật N-Sigma không đổi dưới biến đổi affine và cột hằng không bao giờ báo, nên không cần min–max (runner T-006 dùng min–max toàn chuỗi, tức dữ liệu tương lai). Posterior BOCPD có thể thành NaN khi tổng mật độ tràn về 0 hoặc ∞ (`_bocpd.py:86–108, 211, 220`); NumPy `argmax` trên cột NaN trả 0, nên nếu không kiểm, lỗi số học thành điểm đổi giả hoặc "không báo động" giả (`results/T-013/kiem-tra.json`, check `N3-positive-mass-condition`). Danh sách cột lấy theo cả bản ghi là hồi cứu với BOCPD (cùng bỏ cột hằng, min–max cả chuỗi), nhưng không đổi báo động N-Sigma tới mọi thời điểm τ: hàm xét từng cột, chỉ dùng giá trị tới τ (`baro/anomaly_detection.py:24–34`), tiền xử lý nhân quả, và cột chưa có dữ liệu trước τ không báo trước τ. Vì vậy kết quả RCA sau báo động N-Sigma có lúc t̂+300 (WHY-22); BOCPD thì không.
- **Phương án đã xét:** đoạn 600 điểm bước 300 (phải chọn độ dài và bước; SPEC cấm chia đoạn để vừa chi phí); tiền xử lý nhân quả cho BOCPD (biến thể mới); giữ sentinel (mọi ca có một "báo động" sau mốc); nối các ca thành một dòng (cấm); N-Sigma chỉ mọi cột.
- **Bằng chứng:** `D:/RCA-ext/src/baro/baro/_bocpd.py:187–227`; `baro/utility.py:208–214`; `baro/anomaly_detection.py:7–35`; `baro/reproducibility.py:140–166`; `results/T-013/cua-so-va-che-do-b.md` §2–4; `results/T-013/ho-so-nsigma-phat-hien.md`; REVIEW T-022 (phản biện giao thức, điểm 5, Q11, Q12).
- **Giới hạn:** vị trí điểm đổi BOCPD không phải thời điểm cảnh báo được, vì min–max và bỏ cột hằng dùng cả chuỗi; báo nó là "độ lệch vị trí điểm đổi hồi cứu". Không đo được cảnh báo trực tuyến hay báo động sai trong vận hành liên tục; dữ liệu bình thường chỉ 720 s/ca. Mọi ca có đúng 720 s nền trước lỗi; số phát hiện chỉ nói cho cấu hình nền cố định này. Với BOCPD, t̂ chỉ có sau cuối bản ghi (WHY-22). Chi phí BOCPD trên 1.441 điểm chưa đo (WHY-25).
- **Kết luận phụ thuộc:** mọi số phát hiện P3 (T-025); RCA chế độ (b).

## WHY-35. Chế độ (b): chấm phát hiện và tích hợp với ranker — Đã quyết (Q-74 Q13, Q14)

- **Chọn:**
  - Nhãn proxy, chỉ evaluator đọc: bất thường = [t_tiêm, cuối file], bình thường = trước đó (README RCAEval).
  - Chấm phát hiện bằng báo động thô, không gộp episode. Cửa sổ 60 s tính từ đầu file; cửa sổ dương nếu có báo động; không point-adjust. Chỉ chấm cửa sổ mà mọi điểm được bộ phát hiện đánh giá (N-Sigma từ chỉ số 100, BOCPD từ chỉ số 1); bỏ cửa sổ cuối chỉ có 1 điểm. Theo ca: phát hiện nếu có báo động trong đoạn bất thường; mỗi ca tối đa một sự kiện. Báo động sai mỗi giờ: mẫu số là giờ bình thường được đánh giá của từng bộ. Độ trễ: báo động đầu ≥ t_tiêm trừ t_tiêm ("độ trễ từ lúc tiêm" cho N-Sigma; "độ lệch vị trí điểm đổi hồi cứu" cho BOCPD).
  - Lượt RCA: báo động đầu mở lượt RCA ở t̂; thời gian trơ 300 s; báo động sau thời gian trơ là thông báo mới, được đếm, không chạy RCA. Cửa sổ RCA theo WHY-22 quanh t̂, cắt ở biên file.
  - Ranker: BARO, CIRCA kiến trúc, TORAI (nguồn chính theo WHY-29), mỗi cái với hai bộ phát hiện. Tên: "tích hợp P3: `<ranker>[<bộ phát hiện>]`".
  - Thành công chung: báo động đầu ghép đúng sự kiện (t̂ ≥ t_tiêm) và RCA tại đó xếp root trong top-k (quy tắc hòa WHY-28). Báo động đầu sai thì ca trượt. Thứ hạng tại báo động đầu, kể cả khi sai, được lưu và báo riêng.
- **Vì sao:** gộp episode với thời gian trơ để chấm làm một báo động sai trước mốc che các báo động đúng sau mốc (báo động sai ở t−100 trơ tới t+200). RCA tại báo động sai vẫn có thể trúng root do may, schema hoặc cửa sổ A chồng vào sự cố; đó không phải "phát hiện đúng rồi chẩn đoán đúng". README RCAEval là nguồn quy ước nhãn của chính dataset. Bài BARO ghép bộ phát hiện với CIRCA bản PC, không phải bản kiến trúc; TORAI giả định mốc từ bộ phát hiện ngoài nhưng không kiểm cặp cụ thể, nên các cặp ở đây là tích hợp của nhóm. RCA ở báo động đầu theo cách BARO dùng điểm đổi đầu tiên (`root_cause_analysis.py:284–290`).
- **Phương án đã xét:** chấm theo episode (bản 1); RCA ở mọi thông báo và lấy thông báo ghép đúng đầu tiên (tốn thêm lượt RCA; tách được chất lượng RCA khỏi báo động sai, nhưng lệch chính sách báo động đầu); chấm mọi cửa sổ, coi điểm chưa đánh giá là âm; nhãn theo bài BARO (corpus khác); MicroRank, TraceRCA ở chế độ (b) (cần suy trường trace thiếu: biến thể mới).
- **Bằng chứng:** `results/T-002/public-metadata/run-002/sources/hf-README.md:97`; `results/T-014/ho-so-circa-pc.md:100`; `results/T-016/ho-so-torai.md:25`; `results/T-015/ho-so-microrank.md` §9.1; REVIEW T-022 (phản biện giao thức, điểm 5, Q13, Q14).
- **Giới hạn:** thời điểm lỗi thật bắt đầu và kết thúc chưa biết; nhãn proxy giả định lỗi kéo dài tới cuối file. Biên cửa sổ 60 s trùng mốc vì mốc ở giây 720 (đặc điểm RE2-TT). Dữ liệu bình thường 6 giờ cho 30 ca.
- **Kết luận phụ thuộc:** bảng phát hiện P3 (Q-30); RCA chế độ (b); chi phí T-025.

---

## Ghi chú bổ sung cho mục WHY đã có

### WHY-19 (cửa sổ)

- **Đoạn cũ (giữ nguyên):** "Cửa sổ P3 chưa chốt (Q-54)."
- **Thêm ngay sau:** "Ghi chú 05/10/2026: cửa sổ P3 đã chốt ở Q-64 và Q-74 Q2, xem WHY-22. Bằng chứng ở mục này dùng `--length 10` của RCAEval, cùng độ dài 300 + 300 s nhưng không cùng cửa sổ thông tin với P3 (lưới 15 s của dữ liệu tác giả lệch mốc; ngưỡng `tracets_lat` toàn file). Nguồn đầu vào TORAI ở P3: WHY-29. Câu trước là trạng thái lúc ghi WHY-19 (04/10/2026), giữ để thấy lịch sử."

### WHY-17 (trạng thái P3)

- **Đoạn cũ (giữ nguyên):** tiêu đề "— Ghi nhận triển khai T017 (Minh duyệt ghi 04/10/2026, Q-55; chưa chốt P3)".
- **Thêm vào cuối mục:** "Ghi chú 05/10/2026: P3 dùng quy ước này (Q-74), xem WHY-33. Số `results/T-017/runs/run-dev-005/` không dùng lại nguyên trạng vì cửa sổ P3 đòi span kết thúc trước t+300 (WHY-22)."
