# T-014 — Hồ sơ CIRCA: PC và đồ thị kiến trúc

- **Trạng thái:** tự duyệt theo ủy quyền Đợt 1 ngày 04/10/2026; đang làm.
- **Người làm:** Codex. **Người phản biện:** Claude.
- **Thuộc gói MRP:** P1 — **Cổng:** G1.
- **Intent:** EXECUTE. FACT lấy từ file/code/bài đã kiểm; USER_CONFIRMED là prompt Minh; cấu hình P3 vẫn OPEN (Q-54). Mọi đề xuất WHY trong task là CANDIDATE, không tự chuyển thành DECIDED.

## Mục tiêu

Giải thích CIRCA tới công thức và ví dụ tính lại độc lập, phục vụ nhận xét đầu tiên của cô, RQ1 và DT18-NV2/NV3. Dựng đồ thị metric theo CIRCA từ trace trước mốc, chạy scorer chính thức và kiểm quy mô Train Ticket. Không suy chênh hai đồ thị thành giá trị nhân quả của đồ thị (Q-38).

## Đầu vào

- AGENTS; STATE; LESSONS; MRP §2–7; WHY; DECISIONS; hai nguồn DT18/advisor; mẫu SPEC/LOG; review-prompt.
- T-001 danh-sach-phuong-phap.md §1/3/8.1/8.2/9; T-005 toàn gói; T-006 kiem-dung-dan.md §5/10/11, cham và scripts; T-007 moi-truong-ec2.md; K1 §3/C.6.
- RCAEval D:/RCA-ext/src/RCAEval revision 259ea4167160256a74ad30004aa3d96a998c846e; môi trường py312-pin đã duyệt WHY-15, chỉ đọc/chạy.
- CIRCA NetManAIOps revision 0215e1880096aa02a305c697f1c23cac4600ebd2, clone riêng; bài KDD22 chính thức.
- Chỉ 30 thư mục re2tt_* trực tiếp trong data/rcaeval. Không đọc data/locked. Các dữ liệu khác chỉ thuộc danh sách được Minh cho phép trong prompt. Không giải nén/tải thêm RE2-TT.

## Đầu ra

- ho-so-circa-pc.md và ho-so-circa-kien-truc.md: đủ 7 mục P1 và đường nhãn, đầu vào dataset khác.
- src/circa_kien_truc/: builder, ánh xạ metric, adapter scorer; README cách dùng. Không thay phần khoa học tác giả.
- results/T-014/scripts/, runs/, graphs/, paper/, audit/: nguồn, script độc lập tính điểm, dữ liệu trung gian, kiểm đúng, giữ mọi lượt hỏng và tiến độ.
- yeu-cau-dau-vao.csv: đúng 16 cột prompt; ca-da-chay.csv: ca/file nguồn/phương pháp/mục đích/lý do a,b,c.
- dinh-chinh-task-cu.md; de-xuat-tai-lieu-chung.md; moi-truong.md; manifest file/hash/revision; đối chiếu từng tiêu chí xong.

## Phạm vi ghi

tasks/T-014-ho-so-circa/SPEC.md và LOG.md; results/T-014/; src/circa_kien_truc/; D:/RCA-ext/work/T-014/; nếu thực sự cần, môi trường mới D:/RCA-ext/envs/T-014-<tên> ghim phiên bản. Trên EC2 chỉ ~/rca/T-014/ (cache/tmp/data/code/output đều trong đó). Đúng một dòng T-014 trong STATE, đọc trước/sau và thay chuỗi chính xác; không viết lại toàn file. Không commit/push, không gửi tin ngoài.

## Các bước (theo phụ thuộc)

1. **Nguồn và SPEC.** Đọc luật/nguồn, ghi HEAD và ủy quyền; kiểm tồn tại/revision/hash đầu ra cũ, ghi manifest. Tự phản biện SPEC trước chạy. Lệnh kiểm: git status --short, git rev-parse HEAD, git -C <clone> rev-parse HEAD, đọc/parse đầu ra cũ. Không ghi lại nguồn chung.
2. **Ba nhánh độc lập sau bước 1:** (a) đọc bài/code và số công bố; (b) kiểm T-000–012 liên quan kết luận CIRCA, không sửa task cũ; (c) census 30 schema/normal/trace, chỉ metadata/tín hiệu dev, chưa đọc nhãn để chọn ca. Tối đa 2 subagent, ghi vào paper/ và audit/ riêng. Lệnh kiểm: scripts/inventory.py và manifest; nguồn paper có hash, số công bố lưu trước phép đo.
3. **Chốt quy tắc ca và cấu hình trước điểm, cần bước 2c.** Ca tính tay = ca có ít cột không hằng nhất sau preprocess RCAEval trên ±300 s, hòa theo tên thư mục tăng dần. Tên chỉ được runner dùng tìm file, không đưa vào builder/scorer. Ca quy mô mặc định = chính ca này; census báo cả ca lớn nhất T-005 để tránh nhầm với đại diện toàn dataset. Chỉ dùng nhãn service sau lưu ranking. Không chọn ca theo chạy thành công hay điểm. Cấu hình tham chiếu PC = pc_default nguyên trạng (alpha=.05/stable=True/Fisher-Z/không giới hạn depth theo thư viện ghim); RHT tham chiếu RCAEval; RHT+DA chạy để hiểu/kiểm, không chọn theo chất lượng. Cửa sổ ±300 s là cấu hình tái lập, không chốt P3. Các lựa chọn quan trọng chưa có WHY đánh dấu chờ WHY.
4. **EC2, cần 2a+3; không chờ builder.** Kiểm uptime/free/ps, phiên bản, chạy một tiến trình nặng; không stop/restart máy. Chỉ chép metrics/inject_time của ca dev cần thiết vào T014/data. Nohup chạy PC mặc định, chia log PC/RHT, checkpoint 30 s CPU/RSS/stack và depth/CI nếu có thể quan sát không đổi thuật toán. Tối đa 120 phút cho mặc định, tổng phương pháp/dataset ≤180 phút. Nếu tiến trình nặng khác xuất hiện, ghi tải và dừng/hoãn tiến trình của mình, giữ kết quả; thời gian đó không là số chính thức. Xong khối nào chép về ngay và kiểm hash. Lệnh kiểm: ssh uptime/free/ps; scripts/ec2_run.py; SHA256.
5. **Builder kiến trúc, cần 2a+2c.** Parent span resolve bằng (traceID,spanID), cả parent/child có startTime<mốc; service edge caller→callee. Dựng các cạnh T/S/L/E theo structural.py và cấu hình tests/alg/sgraph/index.yml tại revision. Gán cột theo schema: workload T; cpu/mem/socket/diskio S; latency-50/-90 L; error E; cột lạ/không có service đánh dấu và không tự đoán. Giữ metric của service thiếu trace, không thêm cạnh đoán; kiểm chu trình/SCC/cô lập/count từng ca. Lệnh kiểm: scripts/build_all.py và scripts/check_builder.py với trace giả resolve/collision/boundary/missing service, đối chiếu bộ dựng StructuralGraphFactory chính thức.
6. **Chạy kiến trúc và ví dụ tính tay, cần 3+5 và đồ thị PC nếu hoàn tất.** Gọi RHTScorer/DAScorer chính thức, lưu parents/train/test/coeff/residual/mean/std/z/conf/DA/ranking đầy đủ. Script độc lập không gọi hàm tác giả tính lại từng metric, tới điểm cuối và hòa điểm; sai số số học dùng atol=1e-7, rtol=1e-7 và báo max error. Giữ DAG/SCC semantics code; không sửa cạnh để đẹp. Nếu PC mặc định chưa xong, dành tối đa 45 phút còn lại cho PC giới hạn độ sâu 0,1 và alpha .01/.1 trên ca đã chọn; ghi rõ đây là cấu hình khác, không thay tên PC mặc định. Không hạ số biến theo nhãn. Tính tay cấu hình hoàn tất nếu có nhưng không gọi đó là ví dụ mặc định. Lệnh kiểm: scripts/independent_scores.py --compare; scripts/check_scoring.py.
7. **Chênh công bố, cần 2b+6.** Dùng lại T006 bảng/chấm, soi từng ô/dự phòng/lệnh cửa sổ. Thử code gốc scorer và graph chỉ trên 1–2 ca hoặc cấu hình mới liên quan trên dữ liệu được phép (a/b/c); phân biệt bằng chứng loại trừ với chưa phân xử. Kiểm R/pcalg khả dụng chỉ đọc; nếu cần gói mới không-admin thì môi trường riêng, ghi phiên bản; không đổi hệ thống/readonly env. Không grid-search theo số công bố để chọn cấu hình. Lệnh kiểm: scripts/audit_*; file kết quả cũ parse được; source byte/diff comparison.
8. **Hồ sơ, cần 2a+5–7.** Viết công thức/giả định/đường nhãn/file:dòng; CSV đầu vào, correction và nháp WHY/DECISIONS. Mỗi số trỏ file kết quả. Lệnh kiểm: scripts/verify_outputs.py (schema CSV, file tồn tại, số đối chiếu, inventory đầy đủ).
9. **Rà và bàn giao, cần mọi nhánh.** Đối chiếu từng tiêu chí; làm ngay việc còn khả thi trong giới hạn. Kiểm complete diff/file set phạm vi riêng T014 và bảo toàn unrelated user changes; không suy git diff là toàn phạm vi review. LOG đủ 6 ý + A–H + prompt nguyên văn chung/G1, danh sách mọi file bằng manifest. STATE chờ phản biện nếu phần khả thi đã làm và lý do ngoài giới hạn rõ. Lệnh kiểm: git diff -- src/circa_kien_truc tasks/T014 docs/STATE.md; scripts/verify_outputs.py.

## Edge case (liệt kê trước kết quả)

| Trường hợp | Cách kiểm | Cách xử lý và hệ quả |
|---|---|---|
| PC singular/đồ thị rỗng | cột trùng, hạng ma trận, fixture độc lập; exception và 0 node/edge | lỗi có bằng chứng, không chấm fallback cột. PC rỗng có thể rht mất nút; báo coverage, không tự thêm |
| Cột hằng/normal hằng, residual gần 0 | census raw và processed; synthetic hằng và perfect regression | giữ chính xác preprocess/StandardScaler gốc; ghi scale=1 và score lớn, không tự sàn |
| Alpha/depth | đọc phiên bản/CI defaults; log depth, fixture alpha .01/.05/.1, độ sâu0/1 | mặc định không cap; cấu hình cap là biến thể thăm dò, chưa chọn P3; DA không sửa vấn đề thời gian PC |
| PC học cả sau mốc | lưu time range học và train/test RHT | biết mốc là đầu vào của chế độ RCA; graph chứa fault distribution, không coi đây là tự phát hiện hay kiến trúc normal |
| Service không trace (auth) | census service metric trừ service trace/cạnh, inspect isolates | giữ các node metric có cạnh nội bộ theo structural rules; không tạo service call giả |
| Metric không thuộc service/unknown kiểu | parse suffix longest-known; unknown list đầy đủ | đánh dấu, không suy service từ nhãn; unknown không bị âm thầm xóa |
| Hòa điểm | đảo thứ tự cột, thay hashseed, so nhóm điểm/tie set | báo tie; raw tác giả và thứ hạng phụ deterministic theo tên chỉ cho trình bày/chấm riêng; không gọi sai thứ tự nhóm hòa là đổi khoa học |
| Ứng viên metric/service | số metric raw/processed/in graph/scored; mapping service không nhãn | CIRCA xếp metric. Service dedup first occurrence chỉ là bước chấm, không gán score service tùy ý |
| Cycle/PC hai chiều | DAG check/SCC; DA trên chain và SCC toy + ca | ghi mã gốc xử lý SCC; không tuyên bố DAG causal nếu cyclic; RHT chung tham chiếu, DA riêng |
| Span orphan/collision/self-call/boundary | fixtures traceID key, startTime, parent pre-child post | không nối bằng spanID global; chỉ pre-mốc; giữ thống kê bỏ; không mở nhãn |
| NaN/Inf/time trùng/đơn vị/độ dài thiếu | validate numeric/time and source preprocessing load range | báo lỗi hoặc bước fill chính thức; không tự impute mới; đủ 2 điểm không có nghĩa reference đủ ổn định |
| Tên metric có underscore | kiểm parser chính thức name.split('_')[1] | báo không tương thích code RE, kiến trúc parser lossless, adapter metric node rõ ràng; không âm thầm chập nút |
| SLI ngẫu nhiên và subtree filter | xem CaseData.prune và load_data | không truyền SLI từ nhãn; chứng minh phạm vi candidate thực tế |
| Normal-normal và cực đại nhiễu | cắt hai đoạn đều trước mốc, số candidate score≥3, phân phối score | ranker vẫn luôn xếp hạng; không gọi top1 là root có nghĩa khi thiếu incident; báo false positive ≥3 thay vì tự thêm detector |
| Concurrent jobs | ps/free/uptime trước và trong lượt | một heavy process; time không chính thức nếu tranh tài nguyên; không kill tiến trình khác |

## Kiểm đúng đắn

- Tra trước chạy: paper CIRCA real/synthetic, BARO B3/B5/B6, TORAI B2/B3 và T006 mốc máy; dùng số như mốc chỉ khi nguồn đã kiểm.
- Chạy lại 1–2 ca theo (a), cùng seed; đổi hashseed để tách stochastic khỏi tie. Không nhầm numeric equality với rank equality trong tie.
- Đầu ra không rỗng/hữu hạn; không nhánh dự phòng; không trùng thứ tự cột một cách tình cờ; caller dùng hàm unwrapped để exception minh bạch.
- Đảo thứ tự cột và parents: so metric→score, graph có nhãn node, ranking ties. Chênh numeric quá tolerance thì tìm nguyên nhân, không bỏ qua.
- Normal-normal; soi tất cả residual và score cực lớn; tách từng metric/case/ô.
- Builder so với code tác giả trên fixture và ca dev; coverage schema cả30 và số cạnh/chu trình/cô lập từng ca.
- Không bỏ phép kiểm chủ động. Ngoại lệ PC default không hoàn tất ở ngân sách: không có full ranking/ví dụ mặc định/repeat/permutation/normal mặc định, nên kết luận chỉ tới feasibility/bước đã hoàn tất. Kiểm các phép này trên kiến trúc và biến thể capped, ghi rõ không thay thế bằng chứng mặc định. R/pcalg vắng nếu không dựng được trong quyền/dung lượng: nguồn chênh số công bố vẫn OPEN.

## Tiêu chí xong

1. Hai hồ sơ đủ9 mục, công thức, file:dòng tại đúng revision, nguồn paper và công bố lưu trước chạy.
2. Builder chạy được từ input không nhãn; 30 graph/schema reports; mọi unknown liệt kê; cycle/isolate/edge mỗi ca; equivalence với cấu hình StructuralGraphFactory.
3. Lựa chọn RHT/DA giải thích prior work, không theo accuracy; cảhai thực thi và independent scores khớp trên ca/fixture hợp lệ; chỗ pending WHY rõ.
4. Một ca RE2TT chọn trước điểm có ví dụ từng metric cho cảhai graph; PC default thiếu phải ghi lý do ngân sách và không tự gọi capped là default.
5. Điều tra lệch T006 có file chứng cứ/rerun mới nếu rẻ; mọi giả thuyết ghi checked/excluded/open và các nguyên nhân khác; không sửa task cũ.
6. PC TrainTicket trên EC2 có tiến độ/thời gian từng bước, exit/timeout, tổng≤3h, copyback; nếu tranh máy/SSH không thể chạy thì log nguyên nhân cụ thể, làm laptop phần nhẹ.
7. CSV đúng schema; registry đầy đủ từng ca/method/purpose/reason; mandatory empty files ghi không có.
8. LOG đủ6 ý/A–H/prompt chung+G1 nguyên văn, manifests mọi file; STATE đúng dòng, complete diff/self-audit không có mutation ngoài scope.

## Không làm

Không P3 benchmark toàn dataset, P4 phân tích hạn chế bằng số liệu, P5 thiết kế phương pháp mới; không khóa P3 window/split/dataset; không tìm config cho điểm cao; không test/holdout; không raw CIRCA real dataset mới; không sửa task cũ/file chung; không cài admin; không stop EC2, commit/push/gửi ngoài.

## Chi phí ước lượng

- EC2 PC RE2TT tổng tối đa180 phút, một lượt mặc định tối đa120 phút. Ước lượng trước điểm: T005 >1h/ca nên 30 ca >30h, vượt Q40; BARO công bố fse-TT khoảng2.1h/ca (khác dữ liệu/máy, cần đối chiếu bài). Không suy chính xác chi phí từ một ca. Giới hạn đã được Minh giao trong prompt ec2; không cần xin lại.
- Laptop: census/build/scoring khoảng10–30 phút tổng, không lượt dự kiến>1h. Hai subagent đọc/viết độc lập, không chạy heavy trong lúc đo trên cùng máy. Không deep research.
- Tải chỉ code/paper, ước lượng<50MB, tối đa1GB; ghi nguồn/byte trước, hash sau. Data upload ca dev metrics vài MB, không tính là tải dataset mới, không trace nếu PC không cần.
- R/pcalg: chỉ kiểm khả dụng trước; nếu dựng cần >1GB/admin hay xâm phạm readonly thì dừng phần đó, ghi Cần Minh quyết; làm phần khác.

## Rủi ro và điều chưa chắc

PC có thể >2h hoặc singular; graph kiến trúc có thể cyclic, manual mapping chưa có WHY; prior work window1min khác RE1s, noise Gaussian/linear và normal reference ngắn không tự bảo đảm đúng. EC2/laptop dùng chung: thời gian chỉ đo chính thức khi đủ bằng chứng không heavy concurrent; vẫn có OS/background load. Một ví dụ không chứng minh tính đúng toàn dataset. Paper artifact/config chạy baseline BARO/TORAI có thể không xác định đầy đủ; không gọi chênh loạiB là lỗi code khi chưa có chứng cứ.

## Tự phản biện SPEC trước triển khai

Đã bổ sung: tách dữ liệu PC toàn cửa sổ khỏi RHT111/10 điểm; phép kiểm graph rỗng mất isolated candidates; SCC/DA và ties; trace key có traceID; TIME/cột có underscore; budget tổng gồm mọi biến thể/repeat; normal-normal không ép ranker thành detector; capped không thay default; lineage/output cũ độc lập; bảo toàn state bằng cập nhật một dòng. Đây là chỉnh SPEC trước triển khai, không dựa kết quả.

## Thay đổi trong lúc làm — trước mọi điểm phương pháp
Nguồn mốc tiêm: thiếu29 inject_time.txt trong data/dev; dùng lại đúng30 metadata đã xác minh ở T002 run002, chỉ từng ca được phép. Không mở cases.parquet trong locked. Tiền xử lý runner PC dùng quy trình main.py/T005 (bỏ latency-50, rename latency-90 thành latency, inf→ffill→0) trước preprocess để cấu hình tham chiếu nhất quán; chọn ca theo số cột sau quy trình này, chưa nhìn điểm. Đếm cả schema gốc parquet riêng khi builder kiểm coverage.

## Thay đổi trong lúc làm — điều tra ô MEM fseOB
Sau fixture chứng minh đảo chiều directedPC và original R-pcalg khác đồ thị trên2ca cố định, mở kiểm targeted25ca MEMfseOB với backend R gốc, cùng RHT/cửa sổ. Đây là cấu hình mới lý do(b), không benchmark toàn100ca và không chọn cấu hình từ điểm. Dùng lại RE T006, tổngmethod nhánh audit≤15phút/dataset nếu ước lượng2ca cho phép; nếu không thì chỉ ghi lý do/giới hạn. Mục tiêu phân xử ô0.148 thay vì suy từ2ca. Không thay kết quả/taskcũ.

## Thay đổi trong lúc làm — tách hồi quy/DA trên MEM25
Giữ25graphR đã tính, kiểm thêm SVR(sigmoid)RHT, linearRHT+DA(threshold3), SVRRHT+DA(threshold3) theo prior work. Chi phí trước chạy1–2phút, khôngrerunPC; tổngaudit≤15min/dataset. Không chọn mô hình từ độkhớp/accuracy. Nếu khớp một ô cũng không xác nhận giao thức tác giả khi không có lệnh/bảncode sinh bảng.

## Thay đổi trong lúc làm — giữ tiến độ khi EC2 tranh máy
Hai lượt PC bịdừng sau360s/780s bởiPython T015/T016; monitor banđầu quá bảo thủ coi cảbuildwheel làjobkhác. Đổi launcher trongscopeT014: khiPython ngoàiT014 xuất hiện thì SIGSTOP đúngworker T014, khi hết thì SIGCONT; khôngtácđộngjobkhác. GiữPCcache thayvì mất tiếnđộ; logpause/resume, vẫn tính cảthờigianpause vào hạnwallclock. Lượt3 limit6060s để tổngmặcđịnh (360+780+6060)≤120min. Lượt1/2 giữnguyên/copyback. Runtime cópause khôngsốchínhthức. Khôngthêmqueue/lockglobal haythayđổihệthống.

## Thay đổi trong lúc làm — kiểm native factory và graph cyclic
Kiểm bổ sung YAML/factory gặp ba lỗi cơ khí khác nhau trong script kiểm (import MemoryDataLoader sai module; SafeLoader không biết !include của template; truy cập entity trên tuple cạnh). Đây không phải lỗi CIRCA. Dừng cách đọc private EdgeView, chuyển sang MemoryGraph.dump native rồi đối chiếu node/edge từ JSON; giữ cả ba log. Phép kiểm độc lập DAG đã PASS6ca; không ép công thức DAG cho24cyclic để có PASS giả. Native YAML/factory và hashseed thực thi dùng kiểm equivalence code ở cyclic; không biến nó thành bảo đảm causal.

## Thay đổi trong lúc làm — lưu hashseed của builder
24call/meta cyclic làm native visit nhạy thứ tự set. Graph report lượt đầu không lưu hashseed nên không suy hashseed đó là0. Giữ toàn bộ raw graph/summary đầu ở graphs/initial-unrecorded-hashseed/, chạy lại cùng input/code với PYTHONHASHSEED=0 đã chọn trong protocol; so seed0/1 và YAML native dưới cùng seed0. Không chọn seed theo metricscore/label. Các số cạnh sau dùng graph canonical0, nguồn cũ giữnguyên để review. Ca tính tay nhỏ cócall/metaDAG nên các kết quả điểm đã kiểm vẫn độc lập với thay hash graph cyclic.

## Thay đổi trong lúc làm — default PC đã hoàn tất, kiểm lặp/đảo cột
Lượt3 PC default xong trên EC2, PC1796.269s/RHT0.832s,270điểm, parent1830.590s. Cộng hai lượt dừng là2971.129s; còn dưới120phút default. Dùng một lượt default nữa trên cùngca, đảo thứ tự cột, seed0, khôngoverridePC; vừa kiểm graphlặp theo labeled input vừa kiểm permutation. Giới hạn4170s gồm cảđợi máy, tổngdefault≤120phút vớiđệm. Chỉkhởi worker khi máy khôngcòn Python/R job khác và đủRAM; khôngtácđộngjobkhác. Máy hiệnT016 nặng nênlauncher riêngchỉchờ; hếtngânsáchvẫngiữ log vàbáo chưa kiểmfullPCrepeat. Scorer trên graph cached được kiểm ngay tại laptop, khôngđợi. PCdepth0 local hết45phút đãdừngworkerđúngPID; khôngchạy thêmdepth1/.01/.1 quy môTT trongbudgetcap, cácfixturealpha/depth nhỏvẫnlàmđủ.

## Thay đổi trong lúc làm — kiểm scorer kiến trúc bằng CIRCA gốc
Đối chiếu source và2ca fse chứng minh hai scorer cùng cơ chế nhưng chưa trực tiếp so official CIRCA0215 trên graph kiến trúc RE2TT đã chạy. Bổ sung phép so cùng graph/candidate và context1s111/10 của ca chọn, không học graph mới, không đổi label/window; dự kiến≤1phút. Lý do(b) code khác, kiểm equivalence implementation theo yêu cầu. Kết quả từng metric và route/timer lưu audit; cấu hình native1min không được gộp với cấu hình tham chiếu.


## Thay đổi trong lúc làm — Minh yêu cầu tiếp tục bằng EC2 thứ hai
Minh yêu cầu “vậy dùng ec2 chạy lại và hoàn thành toàn bộ task”, sau đề xuất sửa cách tính thời gian chờ và hai phép kiểm. Ghi riêng queue4171.454560293s không có worker, loại khỏi compute budget; giữ lịch sử accounting cũ. Không reset budget theo máy. Actual wall các worker cũ=360.192319926+780.346918319+1830.589938131+2703.969=5675.098176376s; giữ900sreservation kiểm khác. Còn4224.901823624s cho hai lượt. Lượt1 đảo thứ tự toàn bộ cột sau preprocessing, seed0, học PC mặc định từ đầu trên600điểm, hạn2100s. Lượt2 fullnormalPC: raw/time<td thật, pseudo_detect=td−301; dùng720điểm pre-fault giống control kiến trúc, current=td−1, train/test111/10, PC học trên toàn720điểm normalproxy. Hạn lượt2 lấy phần còn lại sau actual lượt1 trừ đệm10s. Không thay alpha/depth hay số biến theo kết quả. Hai lượt dự kiến tổng~60phút; nếu quá~70phút actual thì timeout là kết quả, không tự tăng ngân sách. Chạy tuần tự bằngnohup, pause đúngworker khi có jobkhác; queue/pause báo riêng. Trước mốc thật không bảo đảm healthy; không coi top1 là root có nghĩa khi thiếu incident.
EC2₂ mọi ghi trong~/rca/T-014/, runtime/source/env riêng. GóiPyPI dự kiến~150MB, trần250MB, tổngtask gồm conservativeaccounting cũ phải<1GB; giữ wheel/hash/byte vàURL. Source RCAEval dùnggitarchive đúngrevision từcheckoutreadonly. Import leafpc bằng namespace loader chỉ tránh import các phương pháp không dùng; codepc/preprocess/rht giữ nguyên/hash đối chiếu. Lệnhkiểm: ec2_followup.py preflight; supervisor/progress/status; compare_followup.py; independent_scores.py vàindependent_window.py; verify_outputs.py.
`n## Thay đổi trong lúc làm — phân xử chiều/candidate khi PC đang chạy`nDùng25R-pcalg graph MEM đã lưu, cố định trước điểm ba counterfactual:forward_drop/reverse_keep/reverse_drop; baselineforward_keep dùnglại. Scorerlinear/window1s111/10 giữ nguyên; không họcPCmới. Mụcđích tách tác động chiều và giữisolate có điều kiện trênRgraph, không đồng nhất với riêngbackendcausal-learn. Chi phí dự kiến<90s/tổngtargetedMEMaudit<15min theo các đoạn đã đo, timinglaptopchỉchẩnđoán. Lệnh kiểm:isolate_graph_factors.py, verify_saved_factors.py. Không chọn cấu hình theo số gầnpaper.
`n## Thay đổi trong lúc làm — giải thích full-PC permutation không đạt`nSau khi full-PC đảo cột xong, skeletonkhớp nhưngorientation/scorekhác. Bổ sung fixture4node không códataset/nhãn: cốđịnhchain a-b-c-d vàseparating sets∅ đểhai colliderxungđột; chỉđảonodeorder, gọi UCSepset priority2 nguyêntrạng vàso rulemanualđộc lập. Dự kiến<10s trongreservation900s. Khôngsuy fixture thànhreplaytoàn667cặpcathật; ghi thayhost/compiler vàcácnguyênnhânkhác. Lệnhkiểm:check_orientation_order.py.
`n## Thay đổi trong lúc làm — chênh bốn điểm normal EC2/laptop`nDirectRHT EC2 vàadapterlocalnormalkhớp266/270,4nodevượttolerance; authlatency41.9829vs287.4143, X rankthiếu/near-cutoff. Khôngnới tolerance. Bổ sungcapture returnframes của rht.py nguyêntrạng trên cùngEC2 vàcùngPCsaved, khônghọcPCmới; repeatedrhtđối chiếu exact với lầnnormal. Tính lạiđộc lập từofficialcapturedarrays, sorawparentorder/singval/value giữaofficial/local; dùngrelative/tolerance đãchốt. Dự kiến<60s trong900sreserve; nếu khôngkhớp thìgiữfailvàkếtluậnnumericalsensitivity, khôngtựsửa thuậttoán. Lệnh:capture_normal_official.py; independent_scores/window; diagnose_normal_capture.py.
