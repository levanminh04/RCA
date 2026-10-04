# Phản biện T-014

- **Người phản biện:** Claude — **Ngày:** 04/10/2026 — **Commit/diff đã đọc:** HEAD `93f13d4`. `git diff 93f13d4` chỉ đổi `docs/STATE.md` (+7 dòng, trong đó một dòng T-014). Mọi file T-014 chưa được track.
- **Đã đọc:** AGENTS, SPEC, LOG (cả ba báo cáo A–H và ba bản prompt), `manifest-files.csv` (đọc cấu trúc, không duyệt từng dòng trong 38 450 dòng), README, hai hồ sơ, `yeu-cau-dau-vao.csv`, `ca-da-chay.csv` (xem cấu trúc), `dinh-chinh-task-cu.md`, `de-xuat-tai-lieu-chung.md`, `moi-truong.md`, `kiem-tra-va-doi-chieu-spec.md`, `bao-cao-cuoi.md`, `bo-sung-ec2.md`, `normal-doi-chieu-so-hoc.md`, `paper/nguon-va-moc-cong-bo.md`, `paper/dinh-chinh-k1-threshold.md`, `paper/cong-bo-circa.csv`, `audit/bao-cao.md`, `audit/cost-summary.json`, `audit/direction.json`, `runs/*.json` chính, `graphs/summary.csv`, `src/circa_kien_truc/*`. Code gốc: CIRCA `0215e18` (`structural.py`, `ci/__init__.py`, `model/graph.py`, `model/case.py`, `models.py`), RCAEval `259ea41` (`e2e/circa.py`, `graph_heads/rht.py`, `classes/data.py`, `io/time_series.py`), causal-learn 0.1.3.8 (`cit.py`, `SkeletonDiscovery.py`, `PC.py`). Bài KDD22 bản text đã lưu. DT18 và advisor. Không đọc từng file trong `/home/ubuntu/rca/T-014/` của hai EC2; chỉ đọc bản copyback trong `results/T-014/runs/`.

## Kết luận chung

Không có lỗi chặn. Các phép tính, đọc code gốc và mô tả hướng cạnh PC đều đúng khi tôi tự kiểm lại. Có bốn điểm KHÔNG CHẶN: một lập luận trong nháp WHY yếu hơn kết luận của nó, một chỗ thiếu số so sánh làm người đọc dễ hiểu quá tay, một đoạn trạng thái cũ còn sót, và một cách tính ngân sách Q-40 cần Minh biết.

## Các điểm

### R1. Nháp WHY "scorer chung" — kết luận mạnh hơn lập luận — KHÔNG CHẶN

- **Bước chịu ảnh hưởng:** chọn scorer tham chiếu cho hai nguồn đồ thị (yêu cầu 3 của task: "chọn theo prior work và theo cơ chế"). Hiện chỉ là CANDIDATE, chờ WHY.
- **Ở đâu:** `results/T-014/de-xuat-tai-lieu-chung.md` §2 ("Vì sao", "Phương án đã xét"); `ho-so-circa-kien-truc.md` §5; `paper/nguon-va-moc-cong-bo.md` mục "Đề xuất scorer trước kết quả".
- **Sai gì:**
  1. Lý do bác DA chỉ nêu cho đồ thị PC ("cạnh hai chiều, đảo cạnh có hướng, không có bảo đảm DAG"). Lý do đó không áp dụng cho đồ thị kiến trúc: đồ thị metric là DAG ở 30/30 ca (`graphs/summary.csv`, cột `dag` = True ×30). Với nhánh kiến trúc, prior work (Table 4: AC@5 .677→.763) và cơ chế đều ủng hộ RHT+DA. Lý do còn lại để chọn RHT-only chỉ là "khớp scorer của RCAEval", tức lý do so sánh, không phải prior work hay cơ chế.
  2. "Phương án đã xét" chỉ có một phương án đối lập: SVR+RHT+DA cho cả hai nguồn. Phương án tự nhiên hơn không được xét: mỗi nguồn dùng cấu hình sát prior work của nó (PC: RHT-only theo RCAEval; kiến trúc: RHT+DA), báo riêng.
  3. Câu "giữ cùng scorer giúp soi riêng nguồn đồ thị" bị chính hồ sơ làm yếu: hai nguồn còn khác tập ứng viên (272 so với 270; gốc CIRCA chỉ chấm 124), số metric không cha (156/272 so với 30/270, đo từ `runs/regression-route-summary.json`) và ngữ nghĩa chiều cạnh. Hồ sơ kiến trúc §7 đã nói thế, nhưng nháp WHY thì không.
- **Có thể phản bác không:** có. Nháp ghi rõ "Đề xuất, chờ G1", "không chốt P3", và task đã chạy cả RHT+DA lẫn SVR+DA trên nhánh kiến trúc (`yeu-cau-dau-vao.csv` dòng 3 và 5). Nên đây không phải lỗi kết quả. Nó là lỗi lập luận trong văn bản sẽ được chép vào WHY.
- **Đề xuất sửa:** trong nháp WHY, ghi lý do chọn RHT-only cho kiến trúc là "so sánh được với PC", không phải "theo prior work". Thêm phương án "mỗi nguồn theo prior work của nó". Chép nguyên câu hạn chế về coverage và cạnh vào chính mục WHY.

### R2. Thiếu số đặt cạnh nhau giữa cửa sổ lỗi và đối chứng — KHÔNG CHẶN

- **Bước chịu ảnh hưởng:** diễn giải ví dụ (tập ứng viên → điểm → xếp hạng); RQ1 về giới hạn của CIRCA.
- **Ở đâu:** `ho-so-circa-pc.md` §7 ("Quy mô và kiểm trên ca thật"); `ho-so-circa-kien-truc.md` §7 ("Đối chứng trước mốc không đạt").
- **Sai gì:** hồ sơ nêu số điểm ≥3 của đối chứng (60/270 kiến trúc, 93/270 PC) nhưng không nêu số tương ứng của cửa sổ lỗi cùng ca. Số đó nhỏ hơn hoặc ngang đối chứng. Người đọc phải tự đoán độ nghiêm trọng, trong khi hai hồ sơ đồng thời đưa ví dụ top-1 trùng service gốc.
- **Bằng chứng:** tôi đếm `rht_score ≥ 3` từ các `snapshot.json`: `runs/example-pc` 88/270; `runs/normal-normal-pc-full` 93/270; `runs/example-architecture` 64/272; `runs/normal-normal-architecture-pretrace` 60/270. Phần có cha trong nhóm ≥3: PC lỗi 82/88, PC đối chứng 85/93, kiến trúc lỗi 33/64, kiến trúc đối chứng 32/60. Riêng nhánh PC, đối chứng còn có nhiều điểm ≥3 hơn cửa sổ lỗi.
- **Có thể phản bác không:** hồ sơ đã viết "ví dụ khớp code không đủ kết luận" và "không coi top1 là root có nghĩa". Chính vì vậy, thêm số cạnh nhau chỉ làm lời ấy rõ hơn. Đối chứng PC dùng n=720 và 275 cột, khác lượt lỗi (n=600, 273 cột), nên so sánh trực tiếp hai số 88 và 93 chỉ nên đọc là "cùng bậc", không là chênh lệch.
- **Đề xuất sửa:** thêm một câu vào mỗi hồ sơ, lấy số từ các snapshot trên, kèm chú thích n và số cột khác nhau.

### R3. Đoạn trạng thái cũ còn sót, mâu thuẫn với kết quả cuối — KHÔNG CHẶN

- **Ở đâu:** `results/T-014/kiem-tra-va-doi-chieu-spec.md`, mục "Trạng thái phép kiểm EC2 cuối" (dòng 39).
- **Sai gì:** đoạn viết "Full PC permutation chưa khởi worker: chờ EC2 có job khác tới hết 4171.455 giây ngân sách" và "Không còn worker T014 chạy sau bàn giao". Cả bảng tiêu chí 6 ở đầu file lẫn `bo-sung-ec2.md` đều nói permutation đã xong (1725.452 s, `runs/ec2-2-permuted/status.json`). Tiêu đề mục nói "cuối" nhưng nội dung là trạng thái giữa chừng.
- **Có thể phản bác không:** mục kế tiếp ("Kiểm bổ sung…") có câu "Các ghi thiếu ngân sách ở bảng trước là trạng thái lịch sử". Câu ấy chỉ nói đến "ghi thiếu ngân sách", không nói đến đoạn này. Người đọc từng mục riêng lẻ vẫn bị đánh lừa.
- **Đề xuất sửa:** đổi tiêu đề thành "Trạng thái trước lượt EC2₂ (lịch sử)" hoặc xóa đoạn.

### R4. Ngân sách Q-40 được đo bằng thời gian worker, không phải "chờ thực tế" — KHÔNG CHẶN

- **Bước chịu ảnh hưởng:** tiêu chí xong 6 của SPEC ("tổng ≤3h"); tuân thủ Q-40.
- **Ở đâu:** `bo-sung-ec2.md` (đoạn "Ngân sách thực tế"); `runs/followup-cost.json`; `de-xuat-tai-lieu-chung.md` §8.
- **Sai gì:** Q-40 (`docs/DECISIONS.md:46`) viết "tối đa 3 giờ **chờ thực tế**". Tổng 10235.006 s ≤ 10800 s chỉ đúng nếu loại 4171.455 s xếp hàng không có worker. Cộng lại, thời gian chờ thực tế vượt 3 giờ rõ rệt: 10235 + 4171 ≈ 14 406 s ≈ 4,0 giờ. Hai file trên có ghi cả hai số, nên không ai bị giấu. Điểm cần nói là: khẳng định "≤ 3h" trong báo cáo cuối dựa trên một cách đo đã được đổi sau khi lượt đầu hết ngân sách.
- **Có thể phản bác không:** có. LOG ghi Minh đã trả lời "vậy dùng ec2 chạy lại và hoàn thành toàn bộ task" sau đề xuất sửa cách tính. Văn bản đề xuất đó nằm trong chat, không nằm trong repo; `de-xuat-tai-lieu-chung.md` §8 chỉ tóm tắt lại. Tôi không thể kiểm Minh đã đồng ý đúng cách tính này hay chỉ đồng ý chạy tiếp.
- **Đề xuất sửa:** trong báo cáo cuối, ghi "≤3h theo thời gian worker; chờ thực tế tổng ≈4h, theo cách tính Minh đã duyệt ngày …". Nếu Minh chỉ đồng ý chạy tiếp, để Minh quyết có coi đây là ngoại lệ Q-40 hay không.

## Điều đã kiểm và thấy đúng

- **Hướng cạnh PC bị đảo (N4).** `rht.py:318–343` rồi `graph.reverse()`. CIRCA `MemoryGraph.parents` = `predecessors` (`model/graph.py:169–172`), nên quy ước là cause→effect. causal-learn: `add_directed_edge(a,b)` cho `adj[a,b]=−1, adj[b,a]=1` (`audit/direction.json`). Kết quả: scorer nhận b→a. Phát hiện đúng.
- **Mất nút cô lập (N3).** `rht.py` chỉ gọi `add_edge`, không `add_nodes`. Đúng.
- **Công thức PC và Fisher-Z.** Đối chiếu `cit.py:138–171`, `SkeletonDiscovery.py:61–116`, `PC.py:22–26`: `r=−inv[0,1]/√|inv[0,0]·inv[1,1]|`, `T=√(n−|S|−3)·|atanh r|`, cạnh bị xóa theo cả độ sâu khi `stable`, không giới hạn depth. Khớp hồ sơ.
- **Cửa sổ RHT.** `classes/data.py:163–243`: train = `lookup−detect+1 = 111` điểm đầu, test = 10 điểm cuối; ở `current=t_d+300` là `t_d−120…t_d−10` và `t_d+291…t_d+300`. `prune=True` bỏ chuỗi hằng trong cửa sổ nạp 421 điểm, không phải 600 điểm. Hồ sơ nêu đúng.
- **DA.** `ci/__init__.py:120–160` khớp công thức hồ sơ (gom child score trước khi sửa, threshold 3 ở `models.py:629–634`, default lớp là 0). Cộng tay: PC 1515.3248+1237.9341=2753.2589; kiến trúc 1880.5743+1.7265=1882.3008 và `order_mem` 4.9146+1880.5743=1885.4889, đều khớp.
- **Bộ dựng kiến trúc.** `src/circa_kien_truc/builder.py`: không nhận nhãn, tên ca, SLI; cha span resolve theo `(traceID, spanID)`, chỉ lấy span trước mốc; luật T/S/L/E chép đúng `tests/alg/sgraph/index.yml`; chiều `dependencies` đúng caller→callee (`structural.py:36–45,175–185`).
- **Tính lại điểm.** Với `runs/example-pc/snapshot.json` và `runs/example-architecture/snapshot.json`, tôi tự chạy OLS bằng sklearn trên `train_x/train_y/test_x/test_y` đã lưu: z lớn nhất 1515.3247929 và 1880.5742947, trùng `rht_score` đến 1e-12. Rank X: PC 4/4, kiến trúc 6/6 (chưa trung tâm hóa).
- **Hoán vị cột.** Tôi hoán `adj.npy` của `ec2-default-003` về thứ tự cột của `ec2-2-permuted`: skeleton giống hệt; 667 cặp đổi, trong đó 613 cạnh có hướng bị đảo chiều ở lượt hoán vị (phần lớn trong khoảng 875 cạnh có hướng) và 54 cặp còn lại đổi giữa các kiểu (15 đảo chiều, 18 từ có hướng sang vô hướng, 21 từ vô hướng sang có hướng). Khớp con số 667 trong hồ sơ và `comparison.json`; chưa được hồ sơ phân loại, nhưng không sai. Số lệnh CI bằng nhau (14 630 641) ủng hộ việc phần đổi hướng là do thứ tự định hướng chứ không phải số học làm đổi skeleton. Đây là lập luận hỗ trợ cơ chế, không thay chứng cứ replay.
- **Số trong văn bản so với file.** 1796.269 s; 60/270; 76/268; 93/270; 957.1628; 10235.006 s; 0.888→0.864/0.960/0.856/0.864 (`audit/mem-target-summary.json`); số công bố .404/.616/.763/.603 và Table 5 (`paper/cong-bo-circa.csv` so với `KDD22-CIRCA.txt` dòng 803–813, 1141). Đều khớp.
- **Chọn ca trước điểm.** `runs/selection-before-scores.json` (08:27) sớm hơn lượt PC đầu (01:30 UTC = 08:30 ICT). Quy tắc theo số cột, không dùng nhãn.
- **Nhãn vào phương pháp.** Không thấy đường nào. `inject_time` là đầu vào của chế độ tái lập và hai hồ sơ ghi rõ. `locked` được chặn bằng `assert` trong các script kiểm. Dữ liệu sau mốc ảnh hưởng tập cột, `drop_constant` và đồ thị PC; hồ sơ nêu đúng điều này, không giấu.
- **Phạm vi ghi.** `runs/verification-final.json` 31/31; `verify_outputs.py --read-only` tôi chạy lại: `{"pass_": true, "count": 31, "failed": []}`. STATE: chỉ dòng T-014 thuộc task này. Không thấy ghi vào file chung hay task cũ.
- **Lệnh/dữ liệu ngoài phạm vi:** `D:/RCA-flasicket/` (sai chính tả) còn thư mục rỗng; đã khai báo trong báo cáo, không có file bên trong (`find` chỉ trả ba thư mục).
- **Phân biệt FAIL và PASS.** Hồ sơ giữ riêng "số học PASS" và "đối chứng âm tính FAIL" (60/270, 93/270; permutation FAIL; đối chiếu laptop–EC2 FAIL bốn metric). Không thấy chỗ nào gọi kết quả FAIL là đạt.

## Lưu ý không phải finding

- `results/T-014/` hiện nặng ≈240 MB, 737 file; riêng `manifest-files.csv` 11 MB (38 450 dòng, kể cả site-packages). Khi Minh duyệt commit theo Luật cứng 11, nên quyết file nào vào git.
- Phần "danh sách phương pháp có phủ đủ họ không; dataset phân xử RQ1/RQ3; chia dev/test" thuộc task tổng hợp G1, không thuộc phạm vi T-014 (một phương pháp, 30 ca dev). Tôi không phản biện các mục đó ở đây. Với CIRCA, hồ sơ kỹ thuật được kiểm với bài và code gốc ở hai nơi, ghi ở phần trên.

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| R1 | Đúng một phần — KHÔNG CHẶN | Nhận phần thiếu phương án mỗi nguồn theo prior riêng và câu “soi riêng nguồn đồ thị” quá mạnh. Nháp đã nêu coverage/density/mapping/fault ở de-xuat-tai-lieu-chung.md:31, nên chi tiết “nháp không nêu” chưa đúng. 272/156 không cha so với 270/30 và native coverage124 được kiểm ở runs/regression-route-summary.json. Metric DAG30/30 không bảo đảm giả định cấu trúc: call/meta cyclic24/30 (graphs/aggregate.json). Table4 hỗ trợ DA theo cơ chế/prior, không tự chọn từ accuracy. Reviewer nói đã chạy kiến trúc SVR+DA là sai: yeu-cau-dau-vao.csv:4 là linear RHT+DA đã chạy; :6 là empirical SVR+DA chưa kiểm. Đề xuất sửa lý do đối chiếu cấu hình, thêm phương án từng nguồn theo prior, giữ P3 OPEN; không suy graph hoặc DA hợp lệ nhân quả chỉ từ output DAG. | Minh: “duyệt, sửa toàn bộ” (04/10); đã sửa theo phản hồi. |
| R2 | Đúng — KHÔNG CHẶN | Đếm lại file thật: PC lỗi88/270 (có cha82/88), normal93/270 (85/93); kiến trúc lỗi64/272 (33/64), normal60/270 (32/60). Các snapshot reviewer dẫn khớp. Normal RHT chính thức cũng93/270 và85/93 tại runs/normal-normal-pc-official-capture/snapshot.json, kiểm thêm scores.json của ec2-2-normal để tránh dùng điểm laptop lệch. PC học600×273 so với720×275; ứng viên kiến trúc272 so với270. Chỉ đặt cạnh để thấy cùng bậc, không dùng hiệu số hoặc gọi tỷ lệ báo nhầm; ngưỡng DA3 không phải detector có calibration. Đề xuất thêm câu và giới hạn này trong hai hồ sơ. | Minh: “duyệt, sửa toàn bộ” (04/10); đã sửa theo phản hồi. |
| R3 | Đúng — KHÔNG CHẶN | kiem-tra-va-doi-chieu-spec.md:37–39 vẫn có tiêu đề “Trạng thái phép kiểm EC2 cuối” và nội dung chưa khởi worker. Status ec2-2-permuted/normal đều complete=true; đoạn này chỉ đúng ở lần bàn giao trước. Câu lịch sử ở đoạn sau chưa đủ rõ. Đề xuất đổi tiêu đề thành “Trạng thái trước lượt EC2 thứ hai (lịch sử)” và dẫn kết quả hiện hành; giữ lịch sử thay vì xóa bằng chứng. | Minh: “duyệt, sửa toàn bộ” (04/10); đã sửa theo phản hồi. |
| R4 | Đúng một phần — KHÔNG CHẶN; quyền đổi cách tính CHƯA KIỂM ĐƯỢC từ repo | Q-40 tại docs/DECISIONS.md:46 nói 3 giờ chờ thực tế; tách queue không chứng minh tuân thủ định nghĩa ấy. Tính lại followup-cost.json: worker đã ghi9335,006s; +dự phòng900=10235,006s. Queue cũ4171,455s: các khối worker+queue=13506,461s (225,1 phút≈3,752h), chưa cộng mọi kiểm nhỏ. Số14406,461s≈4,002h có cả900s dự phòng, không phải thời gian thực tế đã đo. LOG:201 lưu lệnh Minh chạy tiếp, không có nguyên đề xuất chat chứng minh Minh duyệt riêng định nghĩa mới; không suy lệnh ấy thành duyệt sửa Q-40. Đề xuất báo cả số đã ghi và dự phòng, bỏ khẳng định vô điều kiện tuân thủ3h; để Minh quyết ngoại lệ cho lượt tiếp tục. Không ghi “cách tính Minh đã duyệt” khi chưa có bằng chứng xác nhận. | Minh: “duyệt, sửa toàn bộ” (04/10); đã sửa theo phản hồi. Ngoại lệ Q-40 chưa có quyết định riêng. |
