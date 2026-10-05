# Đính chính task cũ — triển khai tại T-020, giữ lịch sử

Không sửa file task cũ. Bản đã áp hoặc bị Minh loại giữ đúng hiện trạng. Các mục dưới được kiểm từ JSON/CSV thành phần, code, snapshot và quyết định hiện hành. [CSV 90 mục](trung-gian/root/application-audit-final.csv) giữ nguyên từng đề xuất cũ→mới, lý do, câu đích và file:dòng đã đối chiếu; cột `review_status` là trạng thái kiểm cuối. Một section không tự là một thay đổi riêng.

## Hợp nhất 34 section đính chính T-013–T-019

Mỗi hàng trỏ đúng section và ID trong CSV. Cách triển khai T020: các định nghĩa/giới hạn được dùng trong hồ sơ 07, ma trận 04, nhãn 05 và bảng kiểm 09; không sửa lịch sử nguồn. Với mục đã áp, không lặp lại như sửa mới. Với mục không áp, không đưa vào hàng đợi duyệt lại. Với mục chưa áp, đề xuất sửa nguồn cũ chính là đoạn cũ→mới giữ nguyên trong CSV, cần Minh duyệt đúng file/đoạn.

| ID / nguồn section | Vấn đề hoặc hiện trạng đã kiểm | Sửa nguồn chung | Thẻ ảnh hưởng |
|---|---|---|---|
| 1 — `results/T-013/dinh-chinh-task-cu.md:5` | K1 chưa tách công thức bài hai phía với max có dấu/nhánh dict của code, hoặc case-level TP/FP. Bằng chứng đích: `docs/knowledge/K1-phuong-phap-rca.md:189; docs/knowledge/K1-phuong-phap-rca.md:191`. | chưa áp; chờ Minh | D1/D4/D5 |
| 2 — `results/T-013/dinh-chinh-task-cu.md:14` | Scale=1 chưa tự chứng minh IQR=0; T-013 có q25/q75/IQR thô nhưng T-006 chưa dẫn chứng đó. Bằng chứng đích: `results/T-006/kiem-dung-dan.md:132`. | chưa áp; chờ Minh | D1/D4/D5 |
| 3 — `results/T-013/dinh-chinh-task-cu.md:23` | Khớp 100 ca chưa chứng minh extraction: sentinel 600 nằm ngoài window 99/100; cần giữ giới hạn. Bằng chứng đích: `results/T-007/kiem-dung-dan.md:21; results/T-007/kiem-dung-dan.md:227`. | chưa áp; chờ Minh | D1/D4/D5 |
| 4 — `results/T-013/dinh-chinh-task-cu.md:31` | Recall=1 chỉ trên các ca đã chạy có alarm; cùng ca có thể góp TP và FP, không bảo đảm mọi dữ liệu. Bằng chứng đích: `results/T-006/kiem-dung-dan.md:83; results/T-006/kiem-dung-dan.md:287`. | chưa áp; chờ Minh | D1/D4/D5 |
| 5 — `results/T-013/dinh-chinh-task-cu.md:40` | Ma trận R 15.864 MiB không đại diện toàn detector: còn covariance và thời gian tính. Bằng chứng đích: `results/T-001/danh-sach-phuong-phap.md:276`. | chưa áp; chờ Minh | D1/D4/D5 |
| 6 — `results/T-013/dinh-chinh-task-cu.md:48` | Mục giới hạn, không nâng thành lỗi hoặc đề xuất sửa mới. Bằng chứng đích: `results/T-013/dinh-chinh-task-cu.md:48`. | không áp/sửa mới | D1/D4/D5 |
| 14 — `results/T-014/dinh-chinh-task-cu.md:6` | Tên không có dấu gạch dưới có thể IndexError; tên nhiều dấu bị cắt, không chỉ bị bỏ im lặng. Bằng chứng đích: `results/T-001/danh-sach-phuong-phap.md:60`. | chưa áp; chờ Minh | D1/D4/D5 |
| 15 — `results/T-014/dinh-chinh-task-cu.md:16` | Hashseed chỉ kiểm top-5 ở bốn ca × sáu hashseed; chưa chứng minh mọi dataset/ranking bất biến. Bằng chứng đích: `results/T-006/kiem-dung-dan.md:186; results/T-006/kiem-dung-dan.md:216`. | chưa áp; chờ Minh | D1/D4/D5 |
| 16 — `results/T-014/dinh-chinh-task-cu.md:25` | PC có thể loại isolate hoặc cho graph rỗng; tập ứng viên không tự bằng toàn metric. Bằng chứng đích: `results/T-001/danh-sach-phuong-phap.md:60; results/T-006/kiem-dung-dan.md:168`. | chưa áp; chờ Minh | D1/D4/D5 |
| 17 — `results/T-014/dinh-chinh-task-cu.md:33` | Adjacency có thể đảo cạnh PC có hướng; hồ sơ cũ chưa nêu khác biệt này. Bằng chứng đích: `results/T-001/danh-sach-phuong-phap.md:60; results/T-006/kiem-dung-dan.md:168`. | chưa áp; chờ Minh | D1/D4/D5 |
| 18 — `results/T-014/dinh-chinh-task-cu.md:42` | Khác graph/DA chưa đủ mô tả: cấu hình bài có empirical SVR sigmoid và DA. Bằng chứng đích: `results/T-001/danh-sach-phuong-phap.md:60; results/T-005/do-kha-thi.md:61`. | chưa áp; chờ Minh | D1/D4/D5 |
| 19 — `results/T-014/dinh-chinh-task-cu.md:52` | Cutoff 3 không trực tiếp lọc output ranking trong implementation; phân biệt ý tưởng bài và code. Bằng chứng đích: `docs/knowledge/K1-phuong-phap-rca.md:206`. | chưa áp; chờ Minh | D1/D4/D5 |
| 29 — `results/T-015/dinh-chinh-task-cu.md:3` | TraceRCA gốc mặc định multiplier 1, hai phía; tên hàm 3sigma không chứng minh multiplier 3. Bằng chứng đích: `results/T-001/danh-sach-phuong-phap.md:88`. | chưa áp; chờ Minh | D1/D4/D5 |
| 30 — `results/T-015/dinh-chinh-task-cu.md:13` | Self-time SLO gốc dùng quan hệ cha–con; mô tả PageRank riêng không bao phủ toàn pipeline. Bằng chứng đích: `docs/knowledge/K1-phuong-phap-rca.md:178; docs/MRP.md:54; docs/WHY.md:23`. | chưa áp; chờ Minh | D1/D4/D5 |
| 31 — `results/T-015/dinh-chinh-task-cu.md:23` | Các lỗi T-007 nêu ở đây đã sửa trước đó; không trình thành lỗi mới. Bằng chứng đích: `results/T-007/kiem-dung-dan.md:23; results/T-007/kiem-dung-dan.md:24; results/T-007/kiem-dung-dan.md:98; results/T-007/kiem-dung-dan.md:175; results/T-007/moi-truong-ec2.md:37; results/T-007/moi-truong-ec2.md:78`. | không áp/sửa mới | D1/D4/D5 |
| 32 — `results/T-015/dinh-chinh-task-cu.md:27` | Chỉ là phạm vi đọc, không chứng nhận lại toàn task cũ. Bằng chứng đích: `results/T-015/dinh-chinh-task-cu.md:27`. | không áp/sửa mới | D1/D4/D5 |
| 46 — `results/T-016/dinh-chinh-task-cu.md:7` | T-001 đã sửa hậu quả double-stride: không còn mô tả đơn giản là nửa cửa sổ lỗi. Bằng chứng đích: `results/T-001/danh-sach-phuong-phap.md:112; docs/DECISIONS.md:65`. | đã áp nguyên văn | D1/D4/D5 |
| 47 — `results/T-016/dinh-chinh-task-cu.md:16` | LOG T-006 giữ lịch sử và thêm đính chính; 15 giây thuộc docs/code, không gán cho bài. Bằng chứng đích: `tasks/T-006-kiem-dung-dan-laptop/LOG.md:334; tasks/T-006-kiem-dung-dan-laptop/LOG.md:371; docs/DECISIONS.md:65`. | đã áp biến thể | D1/D4/D5 |
| 48 — `results/T-016/dinh-chinh-task-cu.md:24` | T-006 đã tách khớp số công bố và lỗi cơ chế fallback/metric bên trong. Bằng chứng đích: `results/T-006/kiem-dung-dan.md:31; results/T-006/kiem-dung-dan.md:264; docs/DECISIONS.md:65`. | đã áp nguyên văn | D1/D4/D5 |
| 49 — `results/T-016/dinh-chinh-task-cu.md:33` | Ba vị trí đã cập nhật RCD 90 ca; vài checkpoint lịch sử 46 ca còn nguyên, không rút sửa đã áp. Bằng chứng đích: `results/T-006/kiem-dung-dan.md:56; results/T-006/kiem-dung-dan.md:229; results/T-006/kiem-dung-dan.md:314; results/T-006/kiem-dung-dan.md:235; results/T-006/kiem-dung-dan.md:307; docs/DECISIONS.md:65`. | đã áp biến thể | D1/D4/D5 |
| 50 — `results/T-016/dinh-chinh-task-cu.md:44` | Hai vị trí đã ghi kiểm loại giả thuyết Windows/Linux; chỉ dẫn lịch sử còn cần ghi closure riêng. Bằng chứng đích: `results/T-006/kiem-dung-dan.md:248; results/T-006/kiem-dung-dan.md:306; results/T-006/kiem-dung-dan.md:316; docs/DECISIONS.md:65`. | đã áp biến thể | D1/D4/D5 |
| 51 — `results/T-016/dinh-chinh-task-cu.md:51` | Đã thêm bằng chứng ca torai-TT trùng dev trong ô bảng T-005, không suy chỉ từ tên. Bằng chứng đích: `results/T-005/moi-truong.md:111; docs/DECISIONS.md:65`. | đã áp biến thể | D1/D4/D5 |
| 52 — `results/T-016/dinh-chinh-task-cu.md:58` | Không có sửa mới trong mục này. Bằng chứng đích: `results/T-016/dinh-chinh-task-cu.md:58`. | không áp/sửa mới | D1/D4/D5 |
| 63 — `results/T-017/dinh-chinh-task-cu.md:7` | Đã tách CLI orig NezhaRCA và lớp SimpleRCA riêng; bản thật mô tả đầy đủ hơn nháp. Bằng chứng đích: `results/T-001/danh-sach-phuong-phap.md:106; results/T-001/danh-sach-phuong-phap.md:138; docs/DECISIONS.md:63`. | đã áp biến thể | D1/D4/D5 |
| 64 — `results/T-017/dinh-chinh-task-cu.md:16` | Đã tách luật Type metric-hoặc-log với nhận xét log riêng RE3-OB. Bằng chứng đích: `results/T-001/danh-sach-phuong-phap.md:188; docs/DECISIONS.md:63`. | đã áp biến thể | D1/D4/D5 |
| 65 — `results/T-017/dinh-chinh-task-cu.md:25` | Đã bổ sung endswith ss→sock-shop và chuỗi preprocess; chưa định lượng accuracy RE3-SS. Bằng chứng đích: `results/T-001/danh-sach-phuong-phap.md:106; docs/DECISIONS.md:63`. | đã áp biến thể | D1/D4/D5 |
| 66 — `results/T-017/dinh-chinh-task-cu.md:34` | Giới hạn đã kiểm, không gọi thành lỗi mới; đơn vị duration và exact program vẫn OPEN. Bằng chứng đích: `results/T-017/dinh-chinh-task-cu.md:34`. | không áp/sửa mới | D1/D4/D5 |
| 71 — `results/T-018/dinh-chinh-task-cu.md:7` | Đã thêm đường rò nhãn qua bộ cột ở đúng thẻ RE2-TT được duyệt; không suy mọi thẻ đã sửa. Bằng chứng đích: `results/T-002/the-rcaeval.md:160; docs/DECISIONS.md:64`. | đã áp biến thể | D1/D4/D5 |
| 72 — `results/T-018/dinh-chinh-task-cu.md:19` | Đã làm rõ GDN val-threshold và median/IQR test; chưa biết log chương trình sinh bảng bài. Bằng chứng đích: `results/T-001/danh-sach-phuong-phap.md:91; results/T-001/danh-sach-phuong-phap.md:191; docs/DECISIONS.md:64`. | đã áp biến thể | D1/D4/D5 |
| 73 — `results/T-018/dinh-chinh-task-cu.md:30` | Q-56 không áp D3: giữ timing T-005, báo rủi ro tái dùng input; không cấp quyền đọc raw. Bằng chứng đích: `docs/DECISIONS.md:64; results/T-005/do-kha-thi.md:51; results/T-005/do-kha-thi.md:54`. | không áp/sửa mới | D1/D4/D5 |
| 74 — `results/T-018/dinh-chinh-task-cu.md:39` | Chú thích DecompRCA/PyRCA/RHT+DA/BARO đã áp; danh sách baseline không đổi. Bằng chứng đích: `results/T-001/danh-sach-phuong-phap.md:179; docs/DECISIONS.md:64`. | đã áp biến thể | D1/D4/D5 |
| 83 — `results/T-019/dinh-chinh-task-cu.md:5` | T-003 vẫn chỉ dẫn Sock Shop sang T-002/P2; cần cập nhật phạm vi hai mẫu và thẻ T-019. Bằng chứng đích: `results/T-003/the-dataset-ngoai-rcaeval.md:19`. | chưa áp; chờ Minh | D2/D3/D4 |
| 84 — `results/T-019/dinh-chinh-task-cu.md:16` | Đề xuất bổ sung public sources SS/F1–F5 chưa áp. Tám file không đồng nghĩa tám nhãn hợp lệ. Bằng chứng đích: `results/T-002/public-sources.md:61; results/T-019/dinh-chinh-task-cu.md:18; results/T-019/dinh-chinh-task-cu.md:19; results/T-019/dinh-chinh-task-cu.md:20`. | chưa áp; chờ Minh | D2/D3/D4 |
| 85 — `results/T-019/dinh-chinh-task-cu.md:22` | Chỉ là phạm vi audit 77 file, không có văn bản đích cần sửa. Bằng chứng đích: `results/T-019/dinh-chinh-task-cu.md:22`. | không áp/sửa mới | D2/D3/D4 |

T-013 R1/N1–N3 đã sửa và task đã đóng; WHY phân bổ hiệu ứng vẫn pending. Q-57 đã áp các lý do TORAI/RCD và D1–D6 T-016; không đồng nghĩa chọn toàn cấu hình P3. WHY-17 đã ghi conventions M4. Q-56 không áp D3/E6 T-018; Retrieval E2 vẫn chờ G1. Nháp ghi “WHY-18 Retrieval” là mã cũ tạm, WHY-18 hiện là GDN diagnostic.

## Phản biện T-002: phân biệt lời reviewer và phản hồi đã kiểm

| Điểm/nguồn | Bằng chứng T020 / kết luận vừa đủ | Trạng thái và triển khai | Cũ→mới đề xuất / G1 |
|---|---|---|---|
| R1 REVIEW:15,157 | cases.json/boundaries theo32mẫu: metric centered quanh injection, không chứng minh exporter mechanism/onset; trace/log sai biên không cùng1s | aggregate đã kiểm; V4/05 ghi midpoint/crop leak, không chạy detector mới | Bổ sung biên lộ vị trí tiêm vànegativecoverage OPEN; không xóa khả năng known-injection / D4,D5 |
| R2 REVIEW:38,158 | probe theo kênh/q vàcontrol khác OR; tỷ lệ ngoài root không nhãn causalpropagation | V2C7 giữdescriptive, không gọi mọi ngưỡng mem làchính; không bỏmem/chọnqđểhạscore | “thống kê lệch theo kênh, cócontrol; không chứng minh lan nhân quả” / D2 |
| R3 REVIEW:60,159 | graph-degrees/cases: sáu graph nhỏ ởorder/travel; rootbậc phụ thuộc chínhca, khôngaveragegraph | root-mapping/V2 không suyhub cố định hay bookingflowngừng từzero | tách bậc root trong từngca; giữ workload/exporter CANDIDATE / D2,D3 |
| R4 REVIEW:86,160 | RE2OBmẫu root/candidates vắngservice khácmetric/log; RE3OB chưa telemetry | V5 giữcandidateceiling OPEN; không suytraceRE3OBtừRE2OB | “mẫuRE2OB cócoveragegap; RE3OBcần kiểm sau quyềnG1/G3” / D1,D2 |
| R5 REVIEW:106,161 | rootindicatorcensus vàstatus/log nguồn; regex/Exception trong INFO khônggroundtruth | V4 khôngfault→metric/regex→nhãnvùng; khôngmọiRE3codetrace đềuusable | phân biệt lời paper/rawlabel/labelindicator; vùngảnhhưởng OPEN / D2,D4 |

Nguồn thống nhất: `tasks/T-002-the-dataset-rcaeval/REVIEW.md`, `results/T-002/local-inspection/run-002/{cases.json,summary.json,graph-degrees.csv,probe-case-summary.csv}`, `results/T-019/census-summary.json`; review-rechecks.json giữ phạm vi32mẫu và6graph nhỏ. Không đọc lại rawTX1để kiểm cácclaim ngoàiaggregate.

## Phản biện T-003 đã sửa: kiểm lại hiện trạng

| Điểm/nguồn | Kiểm lại nguồn gốc | Trạng thái / triển khaiT020 | Cũ→mới đề xuất / G1 |
|---|---|---|---|
| R1 REVIEW:14,82,95 | archivecensus/hash/CRCđã cóT012; TRCA1165CSV+4labels trùngNezha, FSEreduced10folders/8khônginvalid; AnoModtarget khôngruntimegold | đãsửa; bảng40phần giữscope, khôngghi“chờquyền” việc đãđượcphép | giữ nguyênfacts, khôngphóng tothành1430fullbenchmark / D2 |
| R2 REVIEW:32,83,96 | sampling-leakage101labelrecords, minute-file chỉđúng3phút quanhtiêm mỗi modality; metricngày khácphần | đãsửa; V4 táchtrace/log vsmetricday, clock/link OPEN | đổi tênfile khôngphục hồi continuousnegativecoverage; khôngloạitoànNezha / D4 |
| R3 REVIEW:44,84,97 | record.csvđếm136labels/14components/8reasons/9ngày/52cells; Bank podlevel, UTC+8, remote mutable | đãsửacensus; chưaMinhchọnBankgiữ ngoài;40tiêuchí/C9đánhđộc lập | bảotoàn theoủyquyềnkhôngthànhselection; khôngcodefaultclaim / D2,D3 |
| R4 REVIEW:55,85,98 | officialcatalogFcodes khôngbranch/instance rootgold; F23–25khôngcatalogđọc; traceanomaly132485 khôngincidentcount | đãsửa; V4khôngtựcreate RCAcells từfaultcatalog | “gợi ý vị trí, cầnbinding độc lập trướcRCA; khônggoldhiệncó” / D2 |

Review T003 tại dòng91 đã kết luận cácsửa đúng; không dùngfinding banđầu nhưchặn chưa xửlý. Raw/processedTRCA/Deepcùnglineage khôngheldoutđộc lập.

## Điểm mới và lỗi verifier T020

### MicroRank: bộ đếm parent không còn cùng định nghĩa

**T-015, nguồn:** `results/T-015/runs/tt-local/auth/example.json`, bốn khóa `groups.normal/anomaly.audit.missing_parent_spans/explicit_root_spans`. Snapshot normal ghi 1326/0; anomaly ghi 1403/0. Tính độc lập theo định nghĩa null-root hiện hành cho 0/1326 và 0/1403. Archived `runs/source-versions/graph-before-null-audit-fix.py:26` không nhận `<NA>` là explicit root; `src/microrank/graph.py:32` hiện nhận. Join độc lập tại `results/T-015/scripts/independent_inputs.py:45` phân biệt unresolved nonroot và explicit root.

**Ảnh hưởng G1:** D1 cần ghi phiên bản bộ đếm; D2/C3 không được dùng số missing cũ làm bằng chứng mất parent trace. Bốn graph relations, trace counts và SLO của ca kiểm đều khớp; `src/microrank/__init__.py:85` chỉ truyền graph vào PageRank, audit lưu riêng. Không suy lỗi thứ hạng hoặc chứng nhận mọi ca từ một ca này.

**Đã triển khai T020:** giữ bốn MISMATCH với hai giá trị trong [09](09-kiem-cheo-so-lieu.md), giữ failed replay và [mismatches.csv](trung-gian/method_evidence/mismatches.csv); các kết luận hợp nhất dùng phạm vi định nghĩa hiện hành. **Đề xuất sửa nguồn cũ, chờ Minh:** giữ snapshot lịch sử; thêm ghi chú “audit null-root theo phiên bản trước sửa; 1326/1403 missing gồm null roots, không đồng nghĩa parent bị mất. Tính lại theo phiên bản hiện hành: missing=0, explicit roots=1326/1403”. Không ghi đè snapshot hoặc tự đổi trạng thái T-015.

- Ledger T0191245dòngquan hệ khôngđếm bằnguniqueincidents. T020bổ sunglocalRE1OB125đã TX2ngoài lineage trước;40identitysameFSEđược merge,85local↔HFcònOPEN. Không épalias theo tên vàkhôngchọnHFRE1OBtest từTX0/TX1. Đây mởrộngcoverageđượckiểm, khôngkết luận T019fakehaymọinguồnHFđã TX2. SổV3vàD3giữgiớihạn.
- NezhaTT45 label records, hailabel cùngepochkháctexttime; khônggộp thành44physicalinjects hoặc gọi45đãuniqueđúngclock. Source labels.json và unresolved-aliases.csv giữOPEN.
- V1tagT001đãđược sửa: classifier banđầu dùngcontext “danh sách” quá rộng, biến dòngdatasetG1thànhclosed. Root chuyển sangcontentlocal vàauditsemantic;533coverage làmechanical, khôngtựchứngminhclassifyđúng.
- Rootverifier001 đếmRE3TTexpected từtrínhớ rồi fail; sửaexpected từcount-summary:2root/8cells. RootTORAI001/002count literals/ASTtotal fail vì compatibilityguard còncâu stride; retry003 kiểmdefaultTrue,1activestride và2gốc. Rootcost001lấyminimumcảinfer-onlytime0; sửa scopefitpositive. Failure/scripts giữởruns/trung-gian. Đây lỗiT020, khôngsửa sốtaskcũ.
- DraftT020 đã sửa cácfinding nội bộ: physicaldurationunit cònOPEN; LEMMAotherdatestracechưa kiểm khácngày mẫu; SimpleRCAmetricrule chỉmetric; thờiđiểmmodea cầnngânsáchD4, khôngcấmvìblanket “time chỉevaluator”.
- [Sự cố phạm vi đọc](trung-gian/dataset_evidence/scope-incident.md): schema-samples.json củaT010trộn rawsampleTX1đãbịđọc/in đoạn. ĐãbáoMinh,dừng, loại khỏischema-proof vàghi trongmanifest; khôngnewmethod/notTX0heldout. Khôngtuyênbố chưađọcrawtoànlượt. Giữlịch sử đểClaudeđánhgiá.

Đề nghị sửafilecũ sauMinhduyệt: nguyênvănproposal/cũ→mới từngmục ởCSVapplication-audit-final, khôngappendđoạncũđãápnhưproposalnew. CácOPEN cầnthiếtnhãn/normal/source thuộclựa chọnG1/P3+, khôngbịa đểđóngchecklist.
