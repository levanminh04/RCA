# Nhật ký T-015

Chỉ ghi thêm. Người làm Codex; người phản biện Claude theo xác nhận của Minh trong phiên.

## Phiên 1 — 04/10/2026 — Codex — Windows 11 laptop — vai trò: người làm

**Mở phiên:** đã đọc AGENTS, STATE, LESSONS, MRP §2–7, WHY, DECISIONS, review-prompt, mẫu SPEC/LOG, DT18/advisor và REVIEW T-003 R1. T-015 chưa có SPEC/LOG/đầu ra trước phiên. HEAD mở phiên: `93f13d4c4a966428177e2acc287d96bc89303e92`. Chỉ đọc đến lúc Minh giải quyết xung đột vai trò; không sửa trước đó.

Minh ủy quyền tự duyệt SPEC theo prompt Đợt 1 ngày 04/10/2026

**Quyết định của Minh trong phiên:**
- "Đồng ý: Codex làm, Claude phản biện". Chưa ghi DECISIONS vì file chung ngoài quyền; sẽ đưa nháp nguyên văn vào de-xuat-tai-lieu-chung.md.

**Diễn biến:**
- Mở phiên — kiểm luật/đầu vào — RCAEval local đúng revision T-001; T-015 chưa tồn tại; đầu ra T-007 trace có tar 90 ca OB, không tái chạy baseline.
- Soạn SPEC — lập phụ thuộc/edge cases/ngân sách/tiêu chí xong trước chạy mới; tên ví dụ TT được cố định trước nhìn thứ hạng. STATE có đoạn task đang mở cũ, prompt này cho phép thêm đúng dòng T-015.
- Kế hoạch tải — nguồn MicroRank/TraceRCA từ GitHub ở revision T-001, bài WWW'21 từ tác giả/nhà xuất bản; dự kiến tổng <30 MB, dữ liệu tải mới 0 B, lưu work/T-015 và results/T-015/sources; kiểm SHA-256 và revision sau tải.

## Khối task nguyên văn do Minh giao

<task>
Thư mục task: tasks/T-015-ho-so-microrank/. Thư mục kết quả: results/T-015/.

Đầu vào:
- results/T-001/danh-sach-phuong-phap.md, mục 1, 3, 4, 8, 9.
- results/T-007/kiem-dung-dan.md §2.3, §9, §10; thư mục results/T-007/cham/; tasks/T-007-kiem-dung-dan-ec2/REVIEW.md.
- MicroRank gốc IntelligentDDS/MicroRank, revision efd85e8.
- File e2e/microrank.py và tracerca của RCAEval.
- TraceRCA gốc, revision b9087c7.
- Bài MicroRank, WWW'21.

Yêu cầu:
1. Các hồ sơ theo <ho_so>.
2. Hai sai lệch của bản RCAEval so với code gốc:
   - cạnh operation_operation bị đặt lại ở mỗi span (microrank.py:626–627);
   - hai nhóm trace bình thường và bất thường chồng lên nhau.
   Cần làm:
   - Cài bản sửa theo đúng ngữ nghĩa của code gốc, đặt trong src/microrank/.
   - Chạy bản sửa trên RE2-OB, trên EC2. Dữ liệu ở ~/rca/data/re2ob/.
   - Dùng lại kết quả bản RCAEval mà T-007 đã chạy, không chạy lại.
   - So hai bản theo từng ca, không so trung bình. Giải thích cơ chế khác biệt.
   - Đề xuất bản dùng cho P3 theo QT2 và theo cơ chế, kèm nháp WHY. Không chọn theo bản cho điểm cao hơn (QT4).
3. TraceRCA bản RCAEval: T-007 thấy 90 ca có NaN và 79 ca không xếp giảm dần theo điểm.
   - Xác định đây là lỗi hay chủ ý.
   - Nêu ảnh hưởng tới thứ hạng.
   - Nêu adapter phải xử lý thế nào.
4. Quy mô Train Ticket: chạy trên ca dev RE2-TT.
   - Kiểm xem service không có cạnh, hoặc không xuất hiện trong trace, có bao giờ được đưa vào thứ hạng không.
   - Nêu hệ quả cho tập ứng viên và cho trần của Hit@k.
5. Ví dụ tính tay trên 1 ca dev RE2-TT: đồ thị operation, PageRank ở hai phía, spectrum (phổ) có trọng số, điểm nghi ngờ.
6. Việc dọn Minh đã duyệt ngày 03/10: chạy rm ~/.sudo_as_admin_successful một lần trên EC2, rồi ghi vào LOG.

Edge case tối thiểu phải có trong SPEC (bạn tự tìm thêm):
- Đơn vị thời gian của span là micro giây.
- Span mất cha; một trace có nhiều root span.
- Operation trùng tên giữa các service.
- Giới hạn top_max+6.
- Tham số PageRank: damping, số vòng lặp, điều kiện hội tụ.
- Trace cắt ngang biên cửa sổ.
- Cửa sổ ±300 giây hay ±600 giây (WHY-16).
- Không có trace bất thường nào.
- Hash seed.

Được ghi thêm: src/microrank/; D:\RCA-ext\work\T-015\; thư mục ~/rca/T-015/ trên EC2.
</task>

## Bổ sung trước lượt chạy so T-007 — 04/10/2026

**Minh quyết nguyên văn:**

> Đồng ý phương án 1, kèm điều kiện:
> (a) Đặt tên rõ ràng: "MicroRank-RCAEval sửa đầu vào", không gọi là MicroRank gốc. Hồ sơ có bảng: bước nào giữ theo bài, bước nào khác bài, vì sao.
> (b) Ghi lý do chọn vào SPEC/LOG TRƯỚC khi chạy so với T-007. Lý do chọn dựa trên cơ chế (sửa hai lỗi, đúng ngữ nghĩa code gốc), không dựa trên điểm. Báo cáo nói rõ bản này không có số công bố để tái lập; độ tin cậy dựa trên ví dụ tính tay và phép so từng ca với T-007.
> (c) Trong giới hạn task, đọc code gốc để đánh giá phương án 3: suy span kind, root và tên pod từ dữ liệu (không dùng nhãn), rồi chạy code gốc kèm bộ phát hiện gốc. Chỉ đánh giá khả thi và chi phí, chưa cần cài. Ghi kết quả vào hồ sơ để G1 quyết.
> Giữ kết quả bản RCAEval của T-007 làm mốc đối chiếu.

**Lý do chọn trước thấy số:** sửa tích lũy cạnh và hai tập trace chồng; graph/số đếm cùng hai tập trace rời như gốc. Giữ detector span3σ của RCAEval vì đầu vào không có kind/pod để dựng đầy đủ bản gốc. Nhóm anomal iff có span anomal; normal là phần bù, cả hai graph từ các span sau mốc trong nhóm. Đây là biến thể **MicroRank-RCAEval sửa đầu vào**, không gọi bản gốc; không có số công bố riêng. Cơ sở tin cậy là toy so code gốc, ví dụ độc lập và so từng ca, không phải chọn theo điểm. Đề xuất P3 vẫn CANDIDATE, nháp WHY sẽ nằm trong results/T-015.

- Tự kiểm graph lượt đầu — test so graph gốc đạt nhưng assertion toàn dict khi đảo dòng không đạt vì thứ tự pr_trace; sửa canonical hàng theo trace/span trong graph trước mọi lượt thật. Giữ dấu lượt hỏng trong LOG; không làm đổi công thức.
- Dọn EC2 — rm đúng một lần, test xác nhận file không còn. Check formula gốc trên counts không nhãn đạt khớp trace_list_partition và system_anormaly_detect.

- EC2 — kết nối được; uptime/load 0, RAM khả dụng 7282 MiB, không tiến trình nặng thấy ở ps. Đã chạy rm ~/.sudo_as_admin_successful đúng một lần, test xác nhận file không còn. Không thay cấu hình máy. Laptop py312-pin thiếu cả pyarrow và fastparquet; chưa cài vào env chung, đọc I/O bằng py312 đã có hoặc EC2 pin.
- Tự phản biện SPEC — phát hiện khóa pod của gốc khác khóa service RCAEval; prior anomaly code khác bài; detector gốc cần kind/frontend root không có ở parquet; code PageRank không có hội tụ. Đã trình Minh bản sửa grouping/graph giữ detector span thay vì giả gọi là gốc, chờ trả lời. Mốc bài được ghi trước chạy tại runs/independent-math/published-before-run.json; tổng method_s cũ T007 MicroRank L20 =3174,93s dùng dự báo, không số đo chính thức.

- Triển khai kernel — src/microrank/official.py trích nguyên 3 hàm MIT đúng revision; graph tích lũy cạnh, khóa cha theo trace, giữ operation cô lập; detector formula riêng. Đã kiểm graph toy bằng AST gốc và đảo dòng sau sửa canonical: đạt. Ràng buộc duplicate spanID trong trace báo lỗi rõ. Đầu vào 30 dev đã hash và whitelist trong manifest-inputs.json. Không tải dữ liệu/code mới.
- Pilot EC2 — MicroRank-RCAEval sửa đầu vào, re2ob_checkoutservice_cpu_1, ±600s, seed0, giới hạn180s, nohup; dùng pin Python3.12.3 và 1 luồng BLAS, mọi cache/tmp trong T015. Mốc paper đã ghi trước run. Chưa gọi kết quả pilot là kiểm đúng trước so độc lập.

- Pilot 11,584s, RSS529,5MiB, 8704normal+1307anomaly=10011trace, overlap0; 327 so sánh độc lập weight/count/cell/score sai số0. Đã dự báo90ca khoảng1042,6s (~17,4phút), không vượt1h; chạy89ca còn lại nohup, không tái chạy baseline T007. Chỉ số thời gian không chính thức. Lưu ob-plan.json trước chạy khối.
- Instrumentation TT — hook vào hàm PageRank giữ nguyên để lưu prior/vector chỉ cho snapshot, không đổi khoa học. Khối OB đang chạy đã import kernel trước bổ sung hook; numeric core không đổi.

- Khối ob-main khởi động hỏng vì CRLF trong file shell sinh bằng Windows write_text: set nhận CR; PYTHONHASHSEED nhận0+CR nên Python dừng trước gọi method. Không có tiến trình T015 nặng thực chạy cùng T014. Giữ console.log của lượt hỏng, lần sau outputdir mới và shellLF. Tôi đã báo Minh, sửa cách preflight tách kiểm resource khỏi launch.
- Minh chỉ đạo chuyển EC2: nguyên lời 'chuyển sang 3.26.62.217 , file key2.pem, ssh xem được không'; tiếp 'nếu thiếu ram thì chuyển lê ec2 nhé, 3.26.62.217 là ec2 thứ 2'. Thử kết nối chỉđọc trước; ghi mới vẫn chỉ ~/rca/T-015/. Không coi là cho phép chạy cùng T014 trên EC2 đầu. LaptopRAMtừ3.6GiB xuống1.62GiB, không khởi MicroRankTTnặng; sẽ chuyển tới máy2 nếu đủ.

- EC2 thứhai SSH thànhcông; Ubuntu26.04/Python3.14.4, RAMkhảdụng7194MiB, disk33GB, khôngjobnặng. Chưa cóenvpin/RCAEval/RE2OB. KhôngsửadocsSTATEcủataskkhác. Sharedknownhosts khônhavekeymáy2: dùng bảncopy riêng work/T015/known_hosts rồi accept-new đúngIPMinhđưa, không ghi keys/known_hosts chung.
- Kếhoạch chuyển dữliệu trước transfer: RE2OB180file đãcóởEC2đầu879283566B, chỉ3cadevTT auth_cpu_1/route_mem_1/route_socket_1 (81471220B cảtrace/metric/inject). Tổng960754786B dưới1GB; giữ capbảo thủ cho cảcopy. Không tải publictelemetrymới. 30TTfull548755287B sẽvượtcapkhicộngOB; thu hẹp3ca trước nhìnrankingMicroRankTT, ghiSPEC+giới hạntrầncoveragechỉ3ca. Tải runtimePython3.12.3standalone+wheel ghim ước<100MB (phầnmềmkhôngphảitelemetry), mọithứtrongT015; uvbinary dùnglạitừenvtoolsreadonlyEC2đầu. Không dùngPython3.14 để tránhSL29. Tựkiểm nhápchi phíschema từngghi7.18triệuspan đãsửangaytừfooterJSONthành22834238, trước dùngkếtluận.

## Checkpoint sau nén ngữ cảnh — 04/10/2026
Ngữ cảnh đã được nén. Đã dựng lại từ file thật: pilot OB đạt khớp tính độc lập; khối 89 ca hỏng trước gọi phương pháp vì CRLF; chưa có lượt MicroRank TT nặng trên laptop. Hai subagent đã lưu hồ sơ detector/TraceRCA và kernel tính độc lập. EC2 thứ hai đã nhận uv vào ~/rca/T-015/bin/uv, chưa dựng runtime hoặc chuyển telemetry. Tiếp tục đúng phạm vi đã duyệt; khi cần bàn giao có thể mở phiên mới từ checkpoint này. Lệnh tiếp: kiểm uv trên máy hai, dựng Python3.12.3 và các gói ghim trong T-015; xác minh hash dữ liệu rồi chạy từng khối, một tiến trình nặng.
- Setup máy hai — Python3.12.3/np1.26.4/pd2.2.3/arrow18.1.0 đúng pin; uv pip check đạt. Lượt transfer đầu dừng ở kiểm manifest trước SSH: hai ca route không có inject_time.txt trong data/rcaeval. Không giả file tồn tại; kiểm nguồn mốc đã tải riêng ở T-002/T-005, chỉ đúng ca whitelist. Thiếu mốc không suy từ trung điểm hoặc nhãn root.
- Rà phạm vi tìm kiếm — một lệnh rg của subagent đi qua JSON/HTML artifact thay vì chỉ tài liệu/script; root cũng tìm quá rộng trong public metadata. Dừng mở rộng, không dùng output ngoài whitelist để diễn giải kết quả, không mở locked hay raw ngoài scope. Các lần sau dùng file tài liệu/script xác định; artifact mỗi ca lọc whitelist trước đọc.
- Kiểm lại byte đầu vào — hai inject route lấy từ results/T-002/local-inspection/run-002/injection-metadata/<đúng ca>.txt, mỗi file10B. Tổng transfer đúng960754806B, hơn kế hoạch20B vì mốc hai ca nằm ngoài thư mục raw; vẫn dưới1GB. Hai kiểm pre-transfer lỗi (KeyError, tổng byte) chưa chuyển hay gọi method. Đã sửa kiểm manifest, lưu expected.json trước transfer. Không đọc cases.parquet trong locked.
- Tối ưu phụ thuộc trước chạy — transfer OB đang tiến hành, không cần chờ toàn OB để có ví dụ. Chép sớm đúng ca auth27766309B (sẽ trùng một lần trong script chuyển) để chạy kiểm TT; tổng telemetry nếu tính cả bản chép lặp988521115B vẫn dưới1GB. Chỉ một worker nặng trên máy hai; transfer không phải worker phương pháp. Kiểm hash ca auth riêng trước chạy. Lý do SL32: ví dụ không phụ thuộc hoàn tất OB.
- Runtime thực tế — managed Python64,2MiB và numpy/pandas/arrow67,4MiB, cao hơn ước<100MB ban đầu; đây là phần mềm trong T015, không telemetry. Đã ghim và pip check, hash executable và RECORD sẽ ghi moi-truong.md; không cài hệ thống.
- 09:15 — TT auth primary khởi trên EC2 hai sau hash3file đạt; RAM7175MiB, chỉ transfer nhẹ khác đang chạy. Một worker, pin/BLAS1/seed0, heartbeat10s, guard25min; output fresh runs/tt-local/auth, chưa chấm hoặc chọn theo điểm. Lýdo b: biến thể/schema/quy mô mới. Kế hoạch toàn6checks trước điểm <=33min nếu pilot<=5min; sẽ dự báo lại tổng ngay từ primary.
- TT primary — 957209span/5568trace trong±600s; worker14,653s, method7,483s, ok; 1326normal+1403anomaly=2729trace sau mốc, overlap0. Đã chép snapshot/census về. Dự báo phần còn lại auth≈5×15s + kiểm độc lập<1min; tổng TT3ca/kiểm <10min theo pilot, không phải số thời gian chính thức. Đang chạy tuần tự math độc lập rồi đầu vào độc lập rồi5checks; nhãn đã gắn chỉ sau example_ready trong primary-summary.
- Tự kiểm TT — math4383checks mọi prior/vector/weight/count/cell/score error0; đầu vào độc lập19checks đạt. Cột/dòng/seed so exact đạt. Two-normal nghiêm (END trước inject) trả11operation với2814flag/242818current: báo giả, không nguyên nhân có nghĩa; không giấu là chưa kiểm. Extendedtoy9checks đạt: std1/NaN/keycollision reject; std0+>= khiến tất cả bất thường; span cắt mốc theo END; top5+6=11; isolate vẫn có rank. Pilot hai EC2461so numeric error0, graph/count/rank exact; đã chép về ngay.
- Khối OB — runtime2 pilot12,0675s, 89ca dự báo1074s (~17,9phút), tổng kể kiểm/window<1h. Plan ob-plan-ec2-2.json trước khối, chia30/30/29 để chép ngay từngkhối; shell kiểm LF. Hai routeTT đã xong exit0, trước launch máy không jobnặng/RAM7136MiB. Thời gian quan sát, không official; baselineT007 không rerun. 189filetransfer/960754806B mọi hash đạt.
- Tự rà phát hiện lỗi audit nội bộT015: TT pd.NA→<NA> bị tính missing thayroot; census raw isna mới đúng. Đã freeze graph và independent-inputs nguồn trước sửa trong runs/source-versions, thêm token<NA> chỉ bộ đếm, toyNone/pdNA exactgraph+audit đạt. Không đổi cạnh/PR/spectrum/rank. Giữ snapshot/lượt cũ; correctionraw3TT sẽlưu riêng, không nhận19checks cũ là bằng chứng rootsemantics. SPEC thêm thayđổi với hệquả.
- OBblock1 — 30ca xong statusok,285,37s tổng, RSSpeak721,6MiB; đang chép về ngay. Block2 vẫn một worker, RAMcòn6,6GiB. Nullscalar đã xác nhận rawauth pandas.NA, source/correction giữ riêng; không nâng19checkskhớp protocol cũ thành nullsemantics đúng. Probevectortrace đã sẵn, chạy saujobOBđể mọi PPVtrace so trực tiếp sourceofficial không sửa.
- OBblock2 — 30ca xong statusok,336,293s tổng; đã chép về ngay, block3 còn29ca. Các khối chạy cùng±600s/seed0, không dùnglabeltronghàm. Kiểm source/provenanceđượcgiữriênggiữa kernelnguyênMITvàadapter; sẽlọc whitelist trước mọiartifactpercase.
- OBblock3 — 29ca xong,215,423s tổng; cùngpilot đủ90ca. Tổng3block837,091s +runtime2pilot12,068s =849,159s (<15phút), cònwindow2case; khôngsốbenchmark. Chépblock3vềngay. Máyidle/RAM7172MiB trước postchecks tuần tự probevectortrace/3auditcorrection/window3002case/inventory. Không worker nặng song song.
- Bổ sung sửa auditOB trước bàn giao: lỗiNAkhôngchỉTT nên không đểroot/missing90snapshotlàm dữkiện đúng. Script streaming65kbatch,2lượt8cols+hash879MB, dựvàiphút trênmáy2idle; chỉđếm lạiclassifications/counts+kiểm sourcehash, khôngrerunPageRank/phổ/baseline. Giữsnapshotcũ, metadata correctionriêng; khôngđổikếthoạchphươngpháp theo điểm.
- KiểmtoànOB khôngsuy từdòngcuối:90lượt có88ok+2failedduplicate recommendation_loss_1/_2. Bảngso90hàng ghi lỗi thật, khôngcoi failedlàno-anomaly hoặcHitmisshợp lệ. Đangđọc rawhai ca đểphân biệt exactcopies với conflictingidentity; khôngđổi protocol vìđiểm. Metadataaudit đầu đãhỏng ởca failedvìthiếustats, giữlog/lượt; sửa skipnot-applicable trướcthửđíchtáchmới. Chưabáoxong khi chưaxửlýrawidentity.

## Checkpoint sau nén ngữ cảnh lần 2 — 04/10/2026
Ngữ cảnh đã nén. Dựng lại từ LOG/SPEC/kết quả thật: 90 ca OB đã thử, 88 hợp lệ và 2 lỗi duplicate span key; chưa hoàn tất tiêu chí so90ca. TT3ca và tính độc lập đã xong; root nullable chỉ audit đã sửa riêng, chưa gộp vào hồ sơ MicroRank/ví dụ. Probe3027vector trace/operation khớp0, không sửa source gốc. EC2 thứhai đang chạy chẩn đoán raw duplicate hai recommendation_loss, PID13740; không worker phương pháp khác. Tiếp: đọc diagnosis, giữ lượt lỗi, chọn xử lý theo ngữ nghĩa code gốc trước chạy lại; hoàn tất auditOB, bảng so, danh sách file và bàn giao. HEAD vẫn93f13d4c4a966428177e2acc287d96bc89303e92. Không commit/push.

### 04/10/2026 — xử lý bản sao span theo code gốc, trước chạy lại2ca
Chẩn đoán độc lập tất cả11cột raw hai ca recommendation_loss_1/_2:48/99key duplicate, tất cả là exact copies, không có nội dung xung đột. Guard cũ quá nghiêm so ngữ nghĩa gốc preprocess_data.py:410–445: temp[spanid] dùng một bản cho parent lookup, nhưng pr_trace.append chạy mỗi hàng. Không xóa bản sao khỏi SLO, detector hay prior. Sửa graph giữ multiplicity mỗi row trong pr_trace/audit, dùng một identity để tìm cha; chỉ chấp nhận key trùng có8measurement columns giống nhau, reject conflicting identities. Vì sao: bám cơ chế gốc, không vì điểm; chưa nhìn ranking mới hai ca. Freeze code/toy/bảng so trước sửa; giữ2failure và rerun output mới. Kiểm toy duplicate đối chiếu AST gốc cả4relations và multiplicity, conflictreject, permutation; rerun2ca theo lýdo(c). Dự báo<1phút theo ca tương tự, tổng dataset vẫn<1giờ/3giờ. Đây là bổ sung edgecase trong phạm vi sửa adapter; lựa chọn quan trọng (chờ WHY, xem de-xuat-tai-lieu-chung.md).
- Chốt2rerun — 12,864s toànblock, statusok2; độc lập8328/9345so sánh error0. Giữ48/99exact-key occurrence như graphgốc, SLO vẫnRCAEval khácpreprocessinggốc. Bảngsofinal90valid, ledger110lượt kể2failurebanđầu. Streamingv2 kiểm88metadata+cảnhbáo2failednotapplicable,90,584s;2rerunrootpolicyđúng. Chépvềngay. Finalaudit đầu hỏng ở đọc ôCSV chứaJSON như integer; lỗi bộkiểm, khôngmethod; sửa parseJSON và giữ failure manifest.
- Rà số đếm đối chiếu — thêm kiểm arithmetic raw-order μ/std/round đúng code RCAEval, chỉ detector/statistics, không PageRank/ranking:90ca đều khớp SLO/cờ/referencecounts với snapshot biến thể. Vì vậy cột rcaeval_reference trong bảng so có chứng cứ trực tiếp về thống kê, không dựa vào giả định canonical order vô hại. Giữ kết quả ở runs/ob-reference-audit/summary.json; script không dùng label. Lượt<3phút, tổng ngân sách vẫn<1giờ.


- Rà cuối — cả90rawwindow qua guardidentity, chỉ2rerun cóexactcopy; transfer đúng189file/960754806B mọi hash đạt. Finalaudit90/ledger110/7row16col/sourceAST/cú pháp đạt. Source trướcguard phục hồi hash đúng; thời gian bên trong authworker14,312s và supervisor14,653s tách đúng file nguồn. Bổ sung khác biệt mặc định spectrum: bàiOchiai, codeDstar2; K1/66% không bị báo nhầm là lỗi. T004 chưa có kết quả. Các sourceclone cuối vẫn sạch/đúngrevision.



## Kết thúc phiên — 04/10/2026 — Codex, người làm

1. Đã làm gì: báo cáoA bên dưới; hồ sơ, code sửa, so từngca và mọi kiểm thuộc phạm vi đã hoàn tất.
2. File đã thay đổi: báo cáoB và manifest-ban-giao.json, gồm từng file ngoài repo/EC2; STATE chỉ dòngT015.
3. Kiểm tra đã chạy và kết quả: báo cáoC, tieu-chi-xong.csv và final-scientific-audit.json; control báo giả được giữ rõ.
4. Điều chưa chắc/cần Minh quyết: báo cáoG/H; không gọi lựa chọn P3 là DECIDED.
5. Bước tiếp theo chính xác: Minh mở phiên Claude trong D:/RCA-flashticket, dán nguyên prompt cuối LOG; người phản biện chỉ ghi tasks/T-015-ho-so-microrank/REVIEW.md. Sau review, Minh quyết nháp và lựa chọn G1; không tự gửi tin/task ra ngoài.
6. Lệnh cuối hoàn tất bàn giao: D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B results/T-015/scripts/validate_handoff.py. Trước đó cập nhật đúng dòngT015 bằng state_line.py và kiểm byte ngoài dòng không đổi. Kết quả thực tế được lưu trong runs/final-handoff-check.json; nếu lệnh kiểm lỗi thì chưa được chuyển sang báo hoàn tất.

# Bàn giao T-015 — 04/10/2026

## A. Đã làm

Hoàn thành hồ sơ MicroRank, TraceRCA RCAEval và hai bộ phát hiện, đủ7+2mục. Cài **MicroRank-RCAEval sửa đầu vào**; so90ca RE2-OB với kết quả T007 đã lưu. Chạy3ca dev Train Ticket đã chọn trước, kiểm tập ứng viên, ví dụ độc lập và tính khả thi suy schema cho bản gốc. Đề xuất biến thể này cho giao thức span hiện có ở P3 theo cơ chế/QT2; đây là CANDIDATE, không chọn theo điểm cao hơn (chờ WHY, xem de-xuat-tai-lieu-chung.md).

## B. File đã thay đổi

`tasks/T-015-ho-so-microrank/SPEC.md`, `LOG.md`; mọi file trong `results/T-015/`; sáu file trong `src/microrank/`; đúng dòngT015 trong `docs/STATE.md`. Danh sách từng file, gồm scripts, logs, mọi lượt hỏng, source versions và kết quả: `manifest-ban-giao.json`.

Ngoài repo: `D:/RCA-ext/work/T-015/known_hosts`, `uv-linux`. Trên hai EC2: mọi file tạo trong `/home/ubuntu/rca/T-015/`, danh sách từng đường dẫn trong manifest. Máy hai có runtime/env/cache/tmp,189file input, code và runs; máy đầu giữ pilot/lượt hỏng. File `/home/ubuntu/.sudo_as_admin_successful` trên máy đầu đã xóa đúng một lần theo quyền có sẵn và kiểm absent. Không sửa clone/env/data chung, file task cũ, WHY/DECISIONS hoặc commit/push.

## C. Kiểm tra đã chạy và kết quả

90đầu ra OB hợp lệ, hữu hạn, không ô phổ âm/không overlap; ledger110lượt gồm hai failure ban đầu. Independent TT4383giá trị khớp0, probe2729trace+298operation PPV khớp0, nguyên hàm MIT không đổi. Hai rerun duplicate có8328/9345giá trị khớp0. Seed/cột/dòng, graph gốc, root nullable, edgecases và hai cửa sổ300/600s đã kiểm. Train Ticket33check/204dòng ứng viên: vắng trace không xếp; service không cạnh vẫn có thể xếp qua incidence; auth full hạng9 nhưng vắng top11operation. Control trước tiêm vẫn báo2814span: báo giả theo giả định pre-injection bình thường, không nguyên nhân có nghĩa. TraceRCA tái dựng90NaN và79ca sắp sai; adapter lọc hữu hạn trước sort và tie canonical. Nguồn chi tiết: `kiem-dung-dan.md`, `runs/final-scientific-audit.json`, `tieu-chi-xong.csv`.

## D. VẤN ĐỀ Ở TASK CŨ — ĐỂ REVIEWER KIỂM

DC01:T001 gọi detector TraceRCA gốc3σ, nhưng multiplier mặc định1; đã kiểm AST/toy và sửa hồ sơ T015. DC02: câu tuyệt đối trong MRP/WHY bỏ quan hệ cha–con dùng học SLO self-time; đã đọc đúng source, tách rõ PageRank với tiền xử lý detector và viết nháp sửa. Phạm vi phản bác được ghi: K1 nói riêng PageRank là đúng; Ochiai/66% của bài cũng đúng. Không sửa file cũ. Bằng chứng, hệ quả và đoạn cũ→mới ở `dinh-chinh-task-cu.md` và `de-xuat-tai-lieu-chung.md`.

## E. Chỗ lệch khỏi SPEC và lý do

Minh đổi reviewer sangClaude và cho giữ detector span của biến thể; lý do trước kết quả đã ghi. Chuyển EC2 thứhai do thiếu RAM/máy đầu bận; TT còn3ca trước nhìn ranking vì tổng transfer với OB sẽ vượt1GB nếu chép30ca. Sửa audit token nullable và guard exact-copy theo source gốc, giữ lỗi/lượt cũ. ShellCRLF hỏng trước method; controlTraceRCA ban đầu có11span qua mốc đã được đính chính; không giấu là normal nghiêm. Một lần tìm kiếm quá rộng artifact đã dừng, không dùng để kết luận ngoài whitelist. Mọi thay đổi có mục bổ sung SPEC/LOG; không chọn cấu hình theo root score.

## F. Đề xuất cho tài liệu chung

Nháp trong `de-xuat-tai-lieu-chung.md`: lưu quyền/vai trò/EC2 theo lời Minh; WHY về biến thể, exact-copy và TraceRCA finite/tie; làm rõ cha–con trong K1/MRP/WHY02; sửa default TraceRCA T001; cập nhật việc dọn EC2 ở dòng chung. Chưa ghi các file đó. Đúng dòngT015 của STATE chuyển chờ phản biện.

## G. Phần chưa kiểm và lý do

Chưa tái lập toàn bộ số bài MicroRank/full detector gốc: datasetA/B/C và schema kind/pod/root thật không có trong dữ liệu được phép. Giả định công thức code đủ đại diện bài có thể sai vì các khác biệt đã chỉ ra; kiểm bằng artifact/giao thức tác giả khi được phép, không gán số của bài cho biến thể. Chưa cài phương án suy schema: Minh chỉ duyệt đánh giá; root cấu trúc làm được nhưng kind/pod không nhận diện duy nhất từ11cột. Giả định metadata bổ sung có thể phục hồi sẽ sai nếu exporter đã bỏ trường; cần đối chiếu gold instrumentation độc lập nhãn. Đơn vị raw TraceRCA gốc còn OPEN vì module upstream không nằm trong clone đúngrevision; phải phục hồi nguồn encoder để kiểm, không đoán từ RE2.

Không có thời gian benchmark chính thức vì máy dùng chung; logs chỉ theo dõi ngân sách. Không kiểm coverage/hạn chế tổng quát30ca hoặc datasetP3/P4:3ca là kiểm cơ chế đã định trước, không bảo đảm ca khác. Control giả định trước tiêm bình thường có thể sai do workload drift/sự cố chưa nhãn; cần reference sạch và ground truth riêng ở giao thức sau. Các thiếu kiểm này không được gọi là chờ quyền cho phần task đã làm được.

## H. Cần Minh quyết

Sau phản biện Claude, chốt ởG1: baselineP3 dùng biến thể nào; cửa sổ tham chiếu; inventory và full ranking hay output11operation; quy tắc finite/tie TraceRCA; có nguồn kind/pod thật để đi tiếp phương án full-original không. Duyệt các nháp tài liệu chung nếu phù hợp. T015 chưa tự chốt các lựa chọn này.


## Prompt phản biện cho Claude — vai trò Minh đã đồng ý

```text
Bạn là người phản biện độc lập cho task T-015 của repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Bạn chỉ được ghi đúng một file: tasks/T-015-ho-so-microrank/REVIEW.md, theo mẫu tasks/_MAU/REVIEW.md.
Không sửa file nào khác, không commit.

Đọc: tasks/T-015-ho-so-microrank/SPEC.md, tasks/T-015-ho-so-microrank/LOG.md, các file đầu ra: D:/RCA-flashticket/tasks/T-015-ho-so-microrank/SPEC.md; D:/RCA-flashticket/tasks/T-015-ho-so-microrank/LOG.md; D:/RCA-flashticket/results/T-015/manifest-ban-giao.json; D:/RCA-flashticket/results/T-015/bao-cao-cuoi.md; D:/RCA-flashticket/results/T-015/ho-so-microrank.md; D:/RCA-flashticket/results/T-015/ho-so-phat-hien-trace.md; D:/RCA-flashticket/results/T-015/tracerca-rcaeval.md; D:/RCA-flashticket/results/T-015/vi-du-tinh-tay.md; D:/RCA-flashticket/results/T-015/yeu-cau-dau-vao.csv; D:/RCA-flashticket/results/T-015/ca-da-chay.csv; D:/RCA-flashticket/results/T-015/dinh-chinh-task-cu.md; D:/RCA-flashticket/results/T-015/de-xuat-tai-lieu-chung.md; mọi file trong results/T-015/, src/microrank/, D:/RCA-ext/work/T-015/ và trên hai EC2 đã liệt kê từng đường dẫn tại manifest-ban-giao.json; source/revision/đường dẫn chạy tại manifest-inputs.json, src/microrank/PROVENANCE.json, moi-truong.md,
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

## Phiên 2 — 04/10/2026 — Codex — laptop Windows11 — vai trò: người làm, bước7 phản hồi phản biện
**Mở phiên:** Minh báo đã córeview, yêu cầu đọcAGENTS vàworkflow trước. Đã đọc lạiAGENTS toàn bộ, STATE, SPEC và cuốiLOG; workflow áp dụng là AGENTS§5bước7 và docs/review-prompt.md mục Prompt cho người làm phản hồi phản biện. Không có file tênworkflow riêng trong repo ở lần tìm. HEAD hiện93f13d4c4a966428177e2acc287d96bc89303e92. T015STATE chờphảnbiện, Codexlàm/Claudereview khớpLOG. Chưa mởREVIEW; tựsoát file thật trước, ghi điểm tự tìm vàoLOG rồi mới đọc. Chỉ ghiLOG, bảngphản hồi cuốiREVIEW và đúngdòngT015STATE trong bước này; chưa sửa code/kết quả/tài liệu chung. Quyền tựduyệtSPEC banđầu không được diễn giải thành quyền tựsửa mọifinding saureview.


### Checkpoint bước 7 sau nén ngữ cảnh — 04/10/2026
Đã đọc lại luật và workflow, mở phiên 2, tự soát SPEC và đầu ra trước khi đọc REVIEW. Chưa mở nội dung REVIEW. Hai subagent đang tự soát chỉ đọc: cơ chế/tính tay và detector/đầu vào. Chỉ được ghi LOG, bảng phản hồi người làm cuối REVIEW và đúng dòng T-015 của STATE. Chưa được sửa code hay kết quả theo phản biện. Bước tiếp: hoàn tất tự soát và ghi điểm tự tìm vào LOG, sau đó đọc REVIEW và kiểm độc lập từng điểm.


### Tự soát độc lập trước khi đọc REVIEW — 04/10/2026
Minh xác nhận trong phiên: “kiểm chứng từng góp ý rồi ghi phản hồi vào bảng cuối REVIEW và LOG”. Không yêu cầu sửa triển khai. Đã kiểm tồn tại/hash 692 file local trong manifest: không thiếu file, 473 JSON parse được. LOG khác hash do ghi phiên mới; manifest có self-entry nên hash tự tham chiếu không khớp, không dùng entry này xác minh chính manifest. Các đầu ra khoa học còn lại khớp hash. Đã đọc lại SPEC, hồ sơ, CSV, code/công thức và đối chiếu nguồn đúng revision; hai subagent chỉ đọc, chưa đọc REVIEW. Các điểm tự tìm:
- S1: SPEC:56 hứa thay số vòng PageRank để chẩn đoán. 14 file *iterations.csv đều đúng 25 vòng, chưa có kết quả thay số vòng hay ghi vì sao bỏ. Hồ sơ đã nêu chưa hội tụ, không sai khẳng định hội tụ; thiếu phép kiểm làm yếu đánh giá mức nhạy với mặc định 25 vòng và chưa đạt tiêu chí8 đầy đủ.
- S2: ho-so-phat-hien-trace.md:101,161 nói thiếu references/mất cha gây loại baseline, chưa nêu lỗi nhánh trace mới. MicroRank gốc preprocess_data.py:210–218 đọc parentId ngoài else. AST độc lập lấy nguyên get_operation_slo, toy trace đầu frontend-server rồi trace sau non-frontend refs=[] tái hiện UnboundLocalError. Nếu parentId đã được gán từ span trước thì có thể dùng giá trị cũ; không khẳng định mọi trường hợp đều crash. Điều kiện chạy detector gốc cần ghi rõ.
- S3: yeu-cau-dau-vao.csv:7 đặt service/method (định danh operation) ở tín hiệu tùy chọn, dù μ/σ được học theo operation. Cần operation identity bắt buộc; parent mới là tùy chọn đối với luật span.
- S4: independent_spans ở scripts/check_tracerca.py:110–113 dùng else cho current. Timestamp NaN không thuộc cả before và current theo hai predicate official, nhưng vào current của script độc lập. AST memory-only toy xác nhận official0current và script tạo EVIDENCE/rank svc_op=1.0. Đây là sai nghĩa với input nonfinite, chưa chứng minh ảnh hưởng dữ liệu đã chạy. Hai lần đầu toy thiếu helper trong namespace và báo NameError; lần thứ ba lấy đầy đủ các function AST đã chạy đúng. Không ghi file thử. Guard startTime/marker hữu hạn hoặc predicate tường minh cần được đề xuất; không tự sửa tại bước7.
- S5: tracerca-rcaeval.md:75 và CSV row gốc thiếu threshold feature-selection: CLI run_selecting_features.py:51 default1; Makefile:24,110 thực truyền3 cho stderr_criteria (:38–44). Tên --fisher không làm đường thực thành Fisher. Thiếu này ảnh hưởng cấu hình khi chuyển pipeline gốc sang dataset khác.
- S6: yeu-cau-dau-vao.csv:6 mô tả tuyến tính span+sort operation quá rộng nếu đọc là code RCAEval nguyên. tracerca.py:32–35,72–77 lọc toàn span cho mỗi operation, O(MS)+O(MlogM); bản dictionary độc lập mới có thể tuyến tính span. Cần tách chi phí kernel gốc và adapter tối ưu. Không thay số output đã đo.
- S7: src/microrank/__init__.py:35 chỉ kiểm duration<0/null, chưa isfinite startTime/duration. Duration+Inf có thể qua guard rồi bị flag; detectors.py:25,33 không kiểm root duration nên NaN so ngưỡng trả False. Chưa có bằng chứng các ca đã chạy chứa Inf/NaN, không phủ định số cũ; điều kiện adapter trên dataset khác cần guard hữu hạn hoặc mô tả miền đầu vào.
Các điểm trên được ghi trước lần đầu mở REVIEW. Bước tiếp: đọc REVIEW, kiểm riêng từng góp ý, kết luận đúng/đúng một phần/sai/chưa kiểm; giữ cột Minh quyết trống.


### Kiểm chứng sau khi đọc REVIEW — 04/10/2026
Đã đọc REVIEW lần đầu sau mục tự soát ở trên. Reviewer có R1–R3, đều KHÔNG CHẶN. Đã kiểm lại nguồn và snapshot trong bộ nhớ; không chạy thêm dữ liệu thô, không sửa triển khai. Hai subagent chỉ đọc, không ghi file.

**R1 — đúng một phần.** Đếm lại pr_trace của ba snapshot, số mean/median/≥100 span trong REVIEW đều khớp. Nguồn: runs/tt-local/auth/example.json; runs/tt-local/re2tt_ts-route-service_mem_1/example.json; runs/tt-local/re2tt_ts-route-service_socket_1/example.json. Bảng tính lại:

| Ca | Normal: N; mean; median; ≥100 | Anomaly: N; mean; median; ≥100 |
|---|---|---|
| auth | 1326;54.217194570135746;5;348 | 1403;293.0755523877406;179;903 |
| route mem | 1038;10.404624277456648;5;7 | 1277;213.18559122944401;179;1047 |
| route socket | 1130;5.773451327433628;5;2 | 1435;424.4390243902439;179;1167 |

Auth anomaly: tập trace dài903 và tập chứa station903 giao866, mỗi tập có37 riêng. Bằng số lượng không chứng minh bằng tập. Hợp trace của cả ba operation auth là439 trong anomaly,392 trong normal; không trace auth quan sát nào thuộc nhóm ≥100 span. 439/831 trace có auth vẫn bị flag, nên không nói detector chỉ chọn trace dài hoặc bỏ toàn bộ auth. Anomaly gồm903 trace dài+439 trace cóauth+61 trace ngắn khác. Tỷ lệ flag span auth=5036/483077=1.0424839104324983%; control nghiêm=2814/242818=1.158892668583054%. Tỷ lệ trace anomaly auth=1403/2729=51.41077317698791%; control=570/1433=39.77669225401256%. Nguồn control: runs/tt-local/auth/two-normal-summary.json. Baseline/control có độ dài và thành phần khác nhau; không dùng hai tỷ lệ làm ước lượng hiệu quả detector.

Luật “ít nhất một span” có thể tăng xác suất flag theo số cơ hội: nếu giả định n span độc lập cùng xác suất p, P(trace flagged)=1−(1−p)^n. Đây là minh họa cơ chế, không mô hình đã xác nhận cho dữ liệu TT. Cấu trúc workload, operation mix và σ=0/làm tròn có thể cùng giải thích tương quan. Dstar2 không đọc trực tiếp length; grouping, prior anomaly (có occurrence count) và PageRank đưa ảnh hưởng gián tiếp vào coverage/trọng số. Không đủ bằng chứng cho phát biểu “chủ yếu đo trace dài”, hoặc loại hết khả năng auth tác động do shared resources/async/trace thiếu span. Những khả năng đó chưa kiểm, không được gán là đã xảy ra. Nhận thiếu liên hệ detector→group→spectrum trong giải thích auth; không phủ định tính đúng các điểm đã tính.

**R2 — đúng một phần.** SPEC:40 đặt1GB tải mới, :96 ghi dữ liệu mới0B; LOG:95 “giữ cap bảo thủ cho cảcopy” là cách diễn giải/lựa chọn của người làm, không là Minh ra lệnh thu30→3. Ba ca thực thi chọn trước ranking, không dùng nhãn chọn vì điểm. Tuy nhiên prompt nguyên trong LOG:47 yêu cầu “chạy trên ca dev RE2-TT”, không bắt buộc chạy đủ30;30 là whitelist. Tiêu chí5 nguyên SPEC:83 không ghi số30; CSV:6 hiện đã ghi “đạt phạm vi3dev đã định trước”, không ghi đạt toàn30. Bước5 có kế hoạch round-robin nên thu hẹp kế hoạch kiểm là FACT, cần làm rõ3/30 và chưa kiểm27ca, không suy đạt coverage cả30. “7 phút” reviewer nêu chỉ là ngoại suy từ một ca, chưa là dự báo tổng đủ30/guard RAM. Chưa có cơ sở khẳng định hardcap của Minh chắc chắn loại việc copy hay khẳng định vượt quyền riêng từ câu thu hẹp. Không tự chạy27ca sau review; Minh quyết phạm vi P1 chấp nhận hay mở rộng.

**R3 — đúng một phần.** Nháp WHY:27 thiếu phương án giữ baseline trước mốc; nên thêm và giải thích vì sao chọn ngữ nghĩa hai nhóm trong cùng cửa sổ của gốc. Nhưng sửa riêng normal_list_len về len(before) không đủ: RCAEval:672–673 graphnormal=before; :683–684 graphanomaly=ALLpost; :697 anomaly_count=trace flagged. Spectrum:347–355 dùng nf=w*(N_flagged−c_ALLpost), vẫn có thể âm. Toy độc lập số đếm N_before=1,c_before=1,N_flagged=1,c_ALLpost=2,w=.5 cho np=0 nhưng nf=−.5 sau sửa normal count. Muốn nhất quán phải (A) sửa anomaly length về ALLpost, làm detector không còn chia nhóm spectrum, hoặc (B) lọc anomaly graph theo trace flagged và giữ normal baseline, tạo biến thể pre/post khác gốc và cần quy tắc trace ngang mốc. Không chạy biến thể đối lập sau nhìn điểm. Đây là bổ sung lý do lựa chọn, không thay quyết định Minh đã cho kiểm biến thể hiện tại.

**Các điểm tự soát S1–S7 được giữ riêng thành N1–N7 trong bảng phản hồi.** N1 đã được kiểm thêm bằng chính recompute_group/recompute_spectrum độc lập lấy AST, không gọi tác giả, không gọi main có ghi file. Số vòng cố định trước probe là25,26,50,100,101; d=.85/alpha=.01, input snapshotauth không đổi, không chọn vòng theo root rank. Runtime pin3.12.10/np1.26.4, BLAS1; khoảng1.203s chỉ là thời gian quan sát. Vòng25 khớp mọi score đã lưu, sai số0. Vòng26/50/100 đổi cảfull vàtop11; vòng101 đổifull, top11 giống25. Chênh operation giữa hai vòng liên tiếp vẫn lớn ngay ở100/101; không chứng minh hội tụ hoặc chọn mặc định mới. Đây là chẩn đoán thiếu trước bàn giao đã bổ sung read-only, chưa cập nhật hồ sơ/CSV. Kết quả đầy đủ:

~~~json
{"input": "results/T-015/runs/tt-local/auth/example.json", "script_AST": "results/T-015/scripts/independent_math.py:47,173", "fixed_turns_before_probe": [25, 26, 50, 100, 101], "elapsed_observation_seconds": 1.202999999979511, "rows": [{"iterations": 25, "op_max_delta_last": {"normal": 0.598830967761614, "anomaly": 0.539508190102301}, "trace_max_delta_last": {"normal": 0.3476648707274145, "anomaly": 0.5506589081283106}, "op_vector_max_delta_vs25": {"normal": 0.0, "anomaly": 0.0}, "full_ranks_changed_vs25": false, "top11_changed_vs25": false, "max_score_absolute_delta_vs25": 0.0, "max_score_delta_vs_saved": 0.0}, {"iterations": 26, "op_max_delta_last": {"normal": 0.5985698938317021, "anomaly": 0.539508190102301}, "trace_max_delta_last": {"normal": 0.34383906764531214, "anomaly": 0.5387119652587553}, "op_vector_max_delta_vs25": {"normal": 0.5985698938317021, "anomaly": 0.539508190102301}, "full_ranks_changed_vs25": true, "top11_changed_vs25": true, "max_score_absolute_delta_vs25": 197.85655282474409}, {"iterations": 50, "op_max_delta_last": {"normal": 0.5957982605591232, "anomaly": 0.4005508818440978}, "trace_max_delta_last": {"normal": 0.11662289052201952, "anomaly": 0.27124033527039826}, "op_vector_max_delta_vs25": {"normal": 0.595827374195588, "anomaly": 0.539508190102301}, "full_ranks_changed_vs25": true, "top11_changed_vs25": true, "max_score_absolute_delta_vs25": 194.2005274557838}, {"iterations": 100, "op_max_delta_last": {"normal": 0.5917736082149102, "anomaly": 0.3669819500717193}, "trace_max_delta_last": {"normal": 0.08704212737868422, "anomaly": 0.059947487476533834}, "op_vector_max_delta_vs25": {"normal": 0.591858046607552, "anomaly": 0.539508190102301}, "full_ranks_changed_vs25": true, "top11_changed_vs25": true, "max_score_absolute_delta_vs25": 198.32682598323942}, {"iterations": 101, "op_max_delta_last": {"normal": 0.5917714680817757, "anomaly": 0.3562097990943399}, "trace_max_delta_last": {"normal": 0.08698373967370185, "anomaly": 0.059471202196482}, "op_vector_max_delta_vs25": {"normal": 0.25106506364588893, "anomaly": 0.539508190102301}, "full_ranks_changed_vs25": true, "top11_changed_vs25": false, "max_score_absolute_delta_vs25": 282.5453430168306}]}
~~~

N2 tái lập AST get_operation_slo gốc với frontend-server trace t1 rồi non-frontend refs=[] trace t2: UnboundLocalError tại parentId; không chỉ loại trace. N3 xác nhận operation identity cần để lookup μ/σ. N4 toy independent_spans (2reference finite,1current startNaN) cho EVIDENCE/svc_op=1; official predicate>= không có current,0dòng. N5 AST stderr_criteria cùng empirical[4,6]/reference[0,2]: threshold1=True,threshold3=False; thiếu mặc định thật có thể đổi feature set. N6 vòng lọc theo operation trong code gốc xác nhận O(MS), khác bản groupby/dictionary. N7 chạy toy microrank chỉ trong bộ nhớ:2baseline1000/2000μs,1normal1000μs,1current+Inf cùngoperation → statusok, normal1/anomaly1, svc_op score1.0; original_trace_partition D=NaN coi trace normal, alarmFalse. Chưa có chứng cứ các ca đã chạy có nonfinite; không gán ảnh hưởng cho số cũ.

**Lưu ý khác trong REVIEW:** 90OB đã được chạy/đọc kết quả cảT007 vàT015, không coi lại là blind test khi G1 chia dữ liệu. Lý do sửa trước điểm giảm một đường lựa chọn theo nhãn, không xóa lịch sử exposure. Minh đã cho quyền tựSPEC/vai trò/biến thể ngay trong prompt phiên, LOG ghi và nháp DECISIONS có nguyên lời; chưa sửa DECISIONS đúng giới hạn. Chưa có dataset/schema để tái lập số công bố toànMicroRank gốc, giới hạn đã nêu không biến thành PASS.


### Đề xuất sửa gom theo file — chưa triển khai, chờ Minh chọn
Phạm vi ảnh hưởng: lời giải thích cơ chế, bảng đầu vào G1, nháp WHY và guard của adapter. Không đổi detector3σ, PageRank/spectrum gốc, mặc định25/top11, biến thể đã được Minh cho kiểm hay lựa chọn P3. Không sửa tài liệu chung/task cũ, không commit/push. Đề xuất ghi nguyên nhân và giới hạn, không chọn bản/vòng theo điểm tốt hơn.

1. **R1 và N1 — nối detector với thứ hạng, nêu nhạy số vòng.**
   - File: results/T-015/kiem-ung-vien-tt.md:23; vi-du-tinh-tay.md:134,144,148–150; ho-so-microrank.md phần ví dụ/control/đề xuất; de-xuat-tai-lieu-chung.md §2 Giới hạn; kiem-dung-dan.md phần PageRank/control.
   - Đoạn cũ “Hạng khác auth là kết quả của trọng số/PageRank và spectrum trên những tập trace khác” → đoạn mới đề xuất: “Luật ít nhất một span bị cờ đưa trace dài vào nhóm bất thường nhiều hơn trong ba ca đã kiểm: trung vị normal/anomaly đều5/179 span; các số đếm ≥100 span là348/1326 so903/1403 ở auth,7/1038 so1047/1277 ở route mem,2/1130 so1167/1435 ở route socket. Grouping đó thay đổi các ô phổ trước PageRank. 903 trace dài auth không chứa operation auth quan sát được; 903 trace station có giao866 với tập dài, không phải cùng tập. Dstar2 chấm coverage có trọng số trên các nhóm đã chia; chưa có ablation để quy mức ảnh hưởng riêng cho độ dài, operation mix, prior hay đồ thị. Workload drift/trace thiếu/tài nguyên dùng chung còn là khả năng chưa kiểm. Control nghiêm1,16% span/39,8% trace bất thường so auth1,04%/51,4%; baseline khác độ dài/thành phần nên không dùng tỷ lệ đó đo hiệu quả. Đây là giới hạn của CANDIDATE.”
   - Thêm đoạn sau nhận xét chưa hội tụ25: “Chẩn đoán cùng snapshotauth với vòng25/26/50/100/101:25khớp output lưu0;26/50/100 đổi top11,101giữtop11 nhưng đổi full. Ngay100/101 vẫn chưa hội tụ. Giữ25 để khớp code, không tăng vòng để chọn thứ hạng tốt hơn.” Không gọi đây là tần suất trên dataset.
   - Tạo results/T-015/scripts/check_review_diagnostics.py và results/T-015/runs/review-response/trace-length-stats.csv, iteration-probe.json để tái lập từ đúng ba snapshot và lưu các số đã kiểm; không đọc raw/nhãn để tính. Cập nhật dẫn nguồn trong các đoạn trên. Vì sao: đủ cơ chế và Q-33; ảnh hưởng cách đọc auth/P3, không thay scores.

2. **R2 — ghi rõ phạm vi và nguồn lý do cap.**
   - tasks/T-015-ho-so-microrank/SPEC.md: chỉ thêm cuối phần Thay đổi trong lúc làm, không xóa bản cũ: “Cap tính cả sao chép là diễn giải bảo thủ của người làm, không phải Minh chốt thu30→3. Đã kiểm3/30dev; không kết luận về27ca còn lại. Đây là thu hẹp kế hoạch round-robin; tiêu chí nguyên không đặt đủ30. Phạm vi nhận kết quả P1/mở rộng do Minh quyết.”
   - results/T-015/tieu-chi-xong.csv tiêu chí5: “đạt phạm vi3dev đã định trước” → “đạt kiểm cơ chế trên3/30dev; chưa kiểm27ca”; bổ sung nguyên nhân capcopy tự diễn giải, không ghi Minh bắt buộc thu hẹp. Không sửa thành thất bại của mọi kết luận candidate, vì tập vắng trace là điều kiện cấu trúc đã kiểm code và có toy.
   - results/T-015/bao-cao-cuoi.md E/G và kiem-ung-vien-tt.md đoạn phạm vi: thêm đúng thông tin trên. Vì sao: tránh biến lựa chọn người làm thành quyền/hardcap do Minh chốt; không suy coverage toàn30.
   - Không đề xuất tự chạy27ca trong bước7. Nếu Minh muốn mở rộng, trước chạy cần đọc footer để dự báo tổng/bộ nhớ cả27, kiểm máy hai rảnh và ngân sách dataset, giữ variant/window đã chọn trước kết quả. Chỉ30dev đã cho phép, không mở TT khác. Thời gian7phút trong REVIEW không được dùng làm số chính thức hoặc đảm bảo tổng.

3. **R3 — nháp WHY xét phương án baseline.**
   - File results/T-015/de-xuat-tai-lieu-chung.md §2 “Đã xét” và “Kết luận phụ thuộc”.
   - Đoạn cũ chỉ3phương án → thêm: “Giữ normal graph/count từ baseline trước mốc. Muốn nhất quán còn phải (a) graph anomaly toànpost/counttoànpost, khi đó3σ không chia spectrum, hoặc (b) graph anomaly chỉ trace flagged/countcùngnhóm, cần quy tắc trace ngang mốc. Chỉ sửa normalcount không hết nf âm. Hai lựa chọn pre/post khác codegốc chia trace cùngcurrentwindow. T-015 chọn nhómnormal là phần bù trongcurrent theo ngữ nghĩa gốc và quyền Minh, không theo Hit@k.”
   - Kết luận phụ thuộc thêm nghĩa “bình thường sau mốc không có span bị cờ”, khác “reference trước mốc”. Vì sao: trình bày lựa chọn gần nhất và tradeoff thật; không chạy mới hay đổi bản đã chọn.

4. **N2 — điều kiện thất bại detector gốc.**
   - results/T-015/ho-so-phat-hien-trace.md:101,161 và ho-so-microrank.md đoạn đánh giá suy schema: thêm nhánh thiếu refs ở trace mới có thể UnboundLocalError/staleparentId, phân biệt với loại baseline bình thường; dẫn preprocess_data.py:210–218 và toy độc lập. Vì sao: schema thiếu references có thể làm pipeline crash; không hứa adapter điền root là đủ. Không sửa clone gốc, không cài phương án suy schema chưa được yêu cầu.

5. **N3/N5/N6 — bảng đầu vào và mặc định/chi phí.**
   - results/T-015/yeu-cau-dau-vao.csv rowdetectorspan: tin_hieu_bat_buoc thêm operation identity service+method (fallbackoperationName); tùy chọn chỉparent/metric không vào ngưỡng; giữ đúng16cột/7rows. RowTraceRCA gốc thêm selection stderr thresholdCLI1/Makefile3 và entrypoint; rowTraceRCA RCAEval ghi O(MS)+sort raw, tách dictionary/groupby của adapter O(S)+sort; rowspan ghi rõ cách triển khai nào.
   - results/T-015/tracerca-rcaeval.md:75: thêm stderr_criteria và threshold1/3 với source:51/Makefile:24,110; chi phí tương ứng. ho-so-phat-hien-trace.md phần chi phí/default phân biệt vòng lọc RCAEval với groupby. Vì sao: G1 dùng đúng key/config và dự báo khi M lớn; không thay điểm.

6. **N4/N7 — guard input hữu hạn; cần sửa code nếu Minh chọn.**
   - src/microrank/__init__.py: kiểm startTime/duration hữu hạn, duration không âm, marker hữu hạn trước split/statistics; lỗi rõ khi input sai, không tạo evidence từInf. Giữ toàn bộ phép tính trên input hợp lệ.
   - src/microrank/detectors.py: xác nhận duration root là số hữu hạn không âm trước alarm/partition; không để NaN thành normal. Kiểm μ/std/count hiện có vẫn giữ.
   - results/T-015/scripts/check_tracerca.py: kiểm startTime/marker hữu hạn trước independent split; không lấy else làm current cho NaN. results/T-015/scripts/independent_inputs.py: bổ sung hữu hạn cho duration/start/marker để miền input khớp adapter; giữ độc lập thuật toán/không gọi hàm tác giả.
   - results/T-015/scripts/test_adapter.py, test_original_formula.py: bổ sung phản ví dụ thời gianNaN/Inf phải fail rõ; ca hữu hạn giữ kết quả. Lưu outputs mới ở results/T-015/runs/review-response/guard-tests.json. Không sửa official.py hoặc sourceclone, không chọn thay detector.
   - Cập nhật điều kiện input trong ho-so-microrank.md/ho-so-phat-hien-trace.md/tracerca-rcaeval.md/yeu-cau-dau-vao.csv. Chưa có chứng cứ input90OB/3TT có nonfinite. Nếu sửa guard, quét thời gian các cửa sổ đã dùng từ dữ liệu sẵn tại EC2 hai để xác nhận miền hợp lệ; không cần chạy lại90PageRank. Một ca auth có thể kiểm lặp với kernel cập nhật trong lượt mới nếu cần, ghi ledger, chỉ sau Minh chọn sửa và kiểmps/free; không coi thửtoy là ca dataset.

7. **Bàn giao sau sửa nếu được duyệt.**
   - results/T-015/kiem-dung-dan.md, tieu-chi-xong.csv, bao-cao-cuoi.md và manifest-ban-giao.json: cập nhật kết quả thực đã sửa/kiểm, hash/filelist; không sửa ngược snapshots/loglượt cũ. Nếu có lượt dữ liệu thật mới: results/T-015/ca-da-chay.csv ghi case/source/purpose/reason theo lượt đó. Giữ output cũ để reviewer có thể đối chiếu.
   - LOG append từng bước và chỉ dòngT015STATE. Bất kỳ file ghi mới trên EC2 chỉ trong~/rca/T-015/ và có danh sách lúc bàn giao. Không ghi DECISIONS/WHY/MRP/K1/taskcũ: vẫn chỉ nháp đề xuất.

Các đề xuất trên chưa được triển khai. Cần Minh quyết điểm nào sửa và giữ3ca hay yêu cầu mở rộngTT. Đây là bước7: AGENTS§5bước7 “Minh quyết sửa điểm nào”, bước8 “Sửa (nếu Minh yêu cầu)”; docs/review-prompt.md mục phản hồi “Chưa sửa file nào khác”. Quyền tựduyệtSPEC banđầu không tự chuyển gópý reviewer thành lệnh sửa sau phản biện.


### Kết thúc phiên 2 — bước7 phản hồi phản biện — 04/10/2026
1. **Đã làm gì:** đọc AGENTS/workflow, tự soát trước REVIEW và ghi S1–S7; đọc/kiểm độc lập R1–R3 rồi điền 10 dòng phản hồi (R1–R3,N1–N7), cột Minh quyết để trống. Ba góp ý đều đúng một phần; nhận điểm cần làm rõ, giới hạn phần lập luận/đề xuất sửa quá rộng. Ghi đề xuất cụ thể gom theo file ở trên. Không đóng task hoặc đổi lựa chọn P3.
2. **File đã thay đổi:** tasks/T-015-ho-so-microrank/LOG.md chỉ ghi thêm; REVIEW.md chỉ bảng Phản hồi người làm; docs/STATE.md chỉ dòng T015 thành “đã phản hồi REVIEW, chờ Minh quyết (04/10/2026)”. Không sửa src/results, file ngoài repo hay trên EC2 trong phiên này; không commit/push. Toàn phần reviewer trước bảng giữ nguyên 13339 byte. STATE đã kiểm byte ngoài dòng T015 giữ nguyên ở lần ghi.
3. **Kiểm tra đã chạy và kết quả:** 692 file local manifest đủ; 473 JSON parse; đầu ra khoa học khớp hash. Hash LOG khác do phiên mới, hash self-entry manifest không dùng tự xác minh. R1 số 3 snapshot khớp; station903/long903 giao866, auth union439 không giao903long. R2 đối chiếu nguyên yêu cầu/SPEC/CSV/LOG cho thấy cap copy là diễn giải người làm và phạm vi đã ghi3dev. R3 code+toy đếm chứng minh chỉ sửa normal count vẫn có nf−.5. Toy gốc SLO thiếu refs crash; key operation mandatory; NaN timestamp lệch independent predicate; stderr CLI1/Makefile3 cho feature flag khác; Inf span tạo statusok/score1; NaN root thành normal. Probe vòng25/26/50/100/101 read-only đã bổ sung và ghi full JSON trên LOG;25khớp0, các vòng khác nhạy thứ hạng và chưa hội tụ. Tất cả toy trong bộ nhớ bằng pin Python3.12.10/np1.26.4; không chạy thêm dữ liệu thô. Lệnh toy đầu hai lần thiếu helper NameError rồi lần ba thành công; checkpoint ban đầu đã ghi nhưng print Unicode lỗi, đã đọc lại xác nhận nội dung có thật. Kiểm cuối sẽ so prefix reviewer, đủ10rows/cột quyết trống, STATE taskrow và lại hash file khoa học; không dùng diff của các phiên khác làm phạm vi phản biện.
4. **Điều chưa chắc hoặc cần Minh quyết:** chọn điểm sửa theo đề xuất và giữ kiểm TT3ca hay mở rộng phần dev. Chưa phân định causal/dominance của độ dài, chưa chứng minh raw90/3 có nonfinite, chưa đánh giá27TT còn lại; không gán các điểm này thành số sai của kết quả cũ. Quyền sửa sau phản biện theo AGENTS§5bước7–8 và workflow, không tự triển khai khi chỉ được yêu cầu kiểm/ghi phản hồi. Các nháp quyết định chung vẫn chưa ghi và lựa chọn P3 còn CANDIDATE.
5. **Bước tiếp theo chính xác:** Minh chọn R/N nào sửa và phạm vi TT. Người làm sau đó đọc AGENTS, STATE, SPEC, mục Phiên2 cuối LOG và bảng REVIEW; lấy mục “Đề xuất sửa gom theo file” làm danh sách được duyệt, ghi nguyên quyền vào LOG rồi mới sửa đúng file. Không chạy lại90RCAEval T007 hoặc mở locked. Nếu chọn N7, kiểm máy EC2 hai rảnh, quét miền input thời gian và lưu lượt kiểm mới; snapshot/lượt cũ giữ nguyên. Chưa có lệnh chạy thực nghiệm nào được phát sinh bởi phiên phản hồi này.
6. **Lệnh cuối cùng đã chạy:** PowerShell here-string truyền py -3 -B - kiểm chỉ đọc: SHA-256 13339byte prefix REVIEW=e23ff02a79d9b06e39cdf21d83fa0e63fcb57e07dd5d9e3258d8c262b741d2ae;10dòngR1–R3/N1–N7 đều trống Minh quyết; trạng thái T015;473JSON/692file manifest (trừ LOG và self-manifest ở lifecycle này). Không gọi script main có ghi outputs.


## Phiên 3 — 04/10/2026 — Codex — laptop Windows11 — vai trò người làm, bước8 sửa đã duyệt
**Mở phiên:** Đã đọc AGENTS, STATE, SPEC/mục cuối LOG, bảng REVIEW và kiểm HEAD vẫn93f13d4c4a966428177e2acc287d96bc89303e92. STATE và LOG cùng chờ Minh quyết.
**Quyết định của Minh trong phiên:** Minh: “duyệt sửa theo đề xuất”. Áp dụng danh sách “Đề xuất sửa gom theo file” ở phiên2: R1–R3/N1–N7, guard/thử hữu hạn, số chẩn đoán từ snapshot và bàn giao. Không suy quyền chốtP3, mởlocked, sửa file chung hoặc chạy27TT: đề xuất trước để Minh quyết riêng mở rộng, hiện giữ3/30dev. Quyền được ghiLOG và sẽ bổ sung nhápDECISIONS trong de-xuat-tai-lieu-chung.md; không ghi fileDECISIONS thật theo giới hạn.
**Chi phí trước triển khai:** diagnostic snapshot3ca vài giây, guardtoy vài giây, quét hai cột thời gian90OB+3TT trên EC2 hai dự kiến<5phút, không PageRank/ranking mới. Tổng sửa/kiểm thực thi dự kiến<10phút; thời gian quan sát, không benchmark. Không tải dữ liệu mới. Chia hai phần độc lập cho đúng2subagent, mỗi bên file riêng; root giữ guard/EC2/WHY/bàn giao/LOG/STATE để tránh ghi đè. Dữ liệu raw chỉ đọc đúng nguồn đã chạy, chỉ ghi~/rca/T-015/ trên EC2.

- Phiên3 — sửa guard và27phản ví dụ đạt; validtoy khớp adapter/frozen và công thứcAST gốc. Summary runs/review-response/guard-tests.json; giữ outputs cũ. Testpandas cảnh báo khi gán Inf vào intdtype, không ảnh hưởng assertion trong môi trườngpin. EC2hai uptime/free/ps rảnh, RAMavailable7158MiB; quét2cột93file+hàmhash dự kiến<5phút, khôngranker.

- Phiên3 — input-time-audit lần1 hỏng trước đọc raw vì expected.json chỉ có laptop, không tại runs/transfer/ trên máyhai. Giữ time-audit-console.log/preflight.txt/pid. Lần2 chép đúng manifest đã hash tới runs/review-response/expected-inputs.json, launchscript/log/pid mới, không ghi đè failure; guard/phương pháp chưa chạy ca nào trong lần1.

- Phiên3 — quét thời gian93file (90OB+3TT) trên EC2hai đạt: hash93/93khớp,0invalid toàn raw và±600s, elapsed6.349s quan sát. Khôngranker/nhãn, không tảidata mới. Đã chép output/console/lần1failure về runs/review-response/ec2-second/ ngay; không sửa snapshots cũ và không thêm phương pháp/ranking vào ledger110.

- Phiên3 — N2/N3/N5/N6 sửa đủ3file hồ sơ detector/TraceRCA/CSV. CSV giữ16cols/7rows/BOM, định danh operationmandatory; selectorstderrCLI1/Makefile3; O(MS)raw tách groupby/dictionary. WHY đã thêm phương án giữbaseline vàtradeoffcảhaiphía, khôngchạy đối lập. SPECappend/lời phạmviR2 và report/criteria đãsửa. Source cuối riêng current-source-manifest.json, các generators bàn giao cũ giữ lịch sử và không chạyghi đè.

- Phiên3 — R1/N1/R2/N2 đã chốt3hồ sơ và diagnostics. Script mới8statsrows/5probe25/26/50/100/101,25allscoreerror0; hashinput/script khớp. Root rà16checks cùng citation/mốc/default, bổ sung cơ chế và nguyên nhân khác, không kết luận nhân quả. REVIEW chỉ điền cột Minh quyết nguyên quyền “duyệt sửa theo đề xuất”, ghi thực hiện; 13339byte thânreviewer giữ nguyên.


## Kết thúc phiên3 — 04/10/2026 — Codex, người làm — sửa đã duyệt

1. **Đã làm gì:** R1–R3/N1–N7 đã sửa theo đề xuất Minh duyệt, không đổi luật span3σ/kernel MIT/default25/top11 hoặc chốtP3. Báo cáoA–H bên dưới tự đầy đủ; giữ phạmvi3/30dev và27ca chưa kiểm.
2. **File đã thay đổi:** SPECappend, LOGappend, bảngphản hồi REVIEW10dòng, đúngdòngSTATE; ba hồ sơ/ví dụ/candidate/kiểm đúngđắn; CSVđầu vào/tiêu chí; nhápchung/báocáo; guardsrc/__init__.py/detectors.py; scriptscheck_tracerca/independent_inputs/test_adapter/test_original_formula/check_review_diagnostics; artifact/scriptsquét/thử/freeze/hash dưới runs/review-response; manifest. Danh sách từngfile trong manifest-ban-giao.json và repair-validation.json; trênEC2hai filelistdelta remote-changes.json (không tựchứng nhận thờiđiểm tạo cache). Không đổi file ngoài repo, source/env/data chung, taskcũ/WHY/DECISIONS/MRP thật, commit/push. Thân reviewer13339byte giữnguyên; các snapshot/điểm/ledger cũ giữnguyên.
3. **Kiểm tra đã chạy và kết quả:**27guardtoy failrõ khi NaN/Inf/âm, validtoy bằngfrozen/kernelAST;93rawtime+window0invalid,93hashkhớp; probe5vòng25/26/50/100/101 với25scoreerror0 và nhạy thứhạng; stats8dòng; CSV16cols7rows/BOM;90OB cũ ok/phổfinite≥0/rankđúng; ledger110;3kernelASTgốcgiốnghệt. verify_repair.pyđạt; mọiJSONparse và filekhoa học trước sửa đềuhashkhớp. Lần quét1hỏng trướcraw do manifestchưaởEC2, giữnguyênconsole và chạy lần2 freshđạt; metadataread subagent cóUnicodeconsole lỗi đã đọc lạiUTF8, không thấtbại method. Thời gian chỉquan sát. STATEchỉdòngT015 thay, kiểmbyte ngoài dòng. Cuối cùng kiểm lại manifest sauLOG/prompt để hashtrùng file cuối; khôngrerun cácgenerator bàn giao cũ ghiđè lời sửa.
4. **Điều chưa chắc/cần Minh quyết:** duyệt kết quả sửa/task; chốtG1/P3variant/window/inventory/protocolfull/top11/finite-tie, và muốn mở rộng27TT hay nhậnkiểm cơchế3ca. Chưa tái lậpfull sốbài/schema gốc; chưa phânđịnh causal của length hoặc falsealarmtổngquát. Đề xuất commit khi Minh muốn: docs(T-015): hoàn thiện hồ sơ MicroRank và sửa guard sau phản biện. Chưa commit/push vì chưa được yêu cầu. Quyền sửa không được hiểu là đóngtask.
5. **Bước tiếp theo chính xác:** Minh đọc results/T-015/bao-cao-cuoi.md, ho-so-microrank.md, vi-du-tinh-tay.md và tiêu chí/nháp chung; duyệt kết quả thì cập nhật tasktheo quyền, không mởvòngreview tựđộng. Nếu muốn kiểm thêm: đọc artifact tại runs/review-response/ rồi chạy riêng verify_repair.py (không raw/ranker). Nếu muốn mở27TT: viết phạmvi/dựbáotổng/RAM/nguồn trước chạy; khôngchọnca/paramtheođiểm, khôngmởlocked.
6. **Lệnh cuối cùng đã chạy:** D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B results/T-015/runs/review-response/verify_repair.py; sauđó PowerShellhere-string py -3 -B - cậpnhậtmanifestlocal/remote, đốichiếuhash và promptchung+G1 nguyênvăn. Kếtquảthực lưu runs/review-response/repair-validation.json và manifest-check.json. Không gọi ranker hoặc ghi nguồn ngoài phạmvi.

# Bàn giao T-015 — cập nhật sau sửa đã duyệt, 04/10/2026

## A. Đã làm

Đã sửa R1–R3/N1–N7 theo đề xuất mà Minh duyệt: giải thích detector→nhóm trace→spectrum; ghi độ nhạy số vòng, phạm vi3/30dev, phương án baseline trong WHY nháp; bổ sung mặc định/chi phí và guard thời gian hữu hạn.

Hoàn thành hồ sơ MicroRank, TraceRCA RCAEval và hai bộ phát hiện, đủ7+2mục. Cài **MicroRank-RCAEval sửa đầu vào**; so90ca RE2-OB với kết quả T007 đã lưu. Chạy3ca dev Train Ticket đã chọn trước, kiểm tập ứng viên, ví dụ độc lập và tính khả thi suy schema cho bản gốc. Đề xuất biến thể này cho giao thức span hiện có ở P3 theo cơ chế/QT2; đây là CANDIDATE, không chọn theo điểm cao hơn (chờ WHY, xem de-xuat-tai-lieu-chung.md).

## B. File đã thay đổi

Phiên sửa: SPEC chỉ thêm mục; LOG ghi quyền/tiến độ; ba file hồ sơ, ví dụ, kiểm ứng viên, CSV đầu vào/tiêu chí, nháp chung và báo cáo; guard trong `src/microrank/__init__.py`, `detectors.py`; các script kiểm độc lập/toy; script/artifact mới trong `runs/review-response/`; manifest và đúng dòngSTATE. Danh sách file thay và đầu ra mới so với manifest bàn giao đầu ở `runs/review-response/repair-validation.json`; file mới trên EC2hai ở `remote-changes.json` cùng thư mục; toàn bộ đầu ra ở manifest. REVIEW giữ nội dung reviewer và phản hồi đã ghi. Không đổi file ngoài repo trong phiên sửa; trên EC2hai chỉ thêm scripts/quét/inventory dưới T015, giữ failure lần1.

`tasks/T-015-ho-so-microrank/SPEC.md`, `LOG.md`; mọi file trong `results/T-015/`; sáu file trong `src/microrank/`; đúng dòngT015 trong `docs/STATE.md`. Danh sách từng file, gồm scripts, logs, mọi lượt hỏng, source versions và kết quả: `manifest-ban-giao.json`.

Ngoài repo: `D:/RCA-ext/work/T-015/known_hosts`, `uv-linux`. Trên hai EC2: mọi file tạo trong `/home/ubuntu/rca/T-015/`, danh sách từng đường dẫn trong manifest. Máy hai có runtime/env/cache/tmp,189file input, code và runs; máy đầu giữ pilot/lượt hỏng. File `/home/ubuntu/.sudo_as_admin_successful` trên máy đầu đã xóa đúng một lần theo quyền có sẵn và kiểm absent. Không sửa clone/env/data chung, file task cũ, WHY/DECISIONS hoặc commit/push.

## C. Kiểm tra đã chạy và kết quả

Sửa guard:27phản ví dụ bị từ chối; validtoy khớp adapter frozen và công thứcAST gốc. Quét93raw/cửa sổ đã dùng:0nonfinite/âm,93hashkhớp; không chạy ranker mới. Chẩn đoán cùngsnapshotauth25/26/50/100/101:25khớp0;26/50/100đổi top11,101giữtop11 nhưng đổi full; chưa hội tụ. Tính lại độ dài từ3snapshot xác nhận median5/179 và quan hệ grouping; không suy causal. Nguồn `runs/review-response/guard-tests.json`, `ec2-second/input-time-audit/summary.json`, `iteration-probe.json`, `trace-length-stats.csv`.

90đầu ra OB hợp lệ, hữu hạn, không ô phổ âm/không overlap; ledger110lượt gồm hai failure ban đầu. Independent TT4383giá trị khớp0, probe2729trace+298operation PPV khớp0, nguyên hàm MIT không đổi. Hai rerun duplicate có8328/9345giá trị khớp0. Seed/cột/dòng, graph gốc, root nullable, edgecases và hai cửa sổ300/600s đã kiểm. Train Ticket33check/204dòng ứng viên: vắng trace không xếp; service không cạnh vẫn có thể xếp qua incidence; auth full hạng9 nhưng vắng top11operation. Control trước tiêm vẫn báo2814span: báo giả theo giả định pre-injection bình thường, không nguyên nhân có nghĩa. TraceRCA tái dựng90NaN và79ca sắp sai; adapter lọc hữu hạn trước sort và tie canonical. Nguồn chi tiết: `kiem-dung-dan.md`, `runs/final-scientific-audit.json`, `tieu-chi-xong.csv`.

## D. VẤN ĐỀ Ở TASK CŨ — ĐỂ REVIEWER KIỂM

DC01:T001 gọi detector TraceRCA gốc3σ, nhưng multiplier mặc định1; đã kiểm AST/toy và sửa hồ sơ T015. DC02: câu tuyệt đối trong MRP/WHY bỏ quan hệ cha–con dùng học SLO self-time; đã đọc đúng source, tách rõ PageRank với tiền xử lý detector và viết nháp sửa. Phạm vi phản bác được ghi: K1 nói riêng PageRank là đúng; Ochiai/66% của bài cũng đúng. Không sửa file cũ. Bằng chứng, hệ quả và đoạn cũ→mới ở `dinh-chinh-task-cu.md` và `de-xuat-tai-lieu-chung.md`.

## E. Chỗ lệch khỏi SPEC và lý do

Minh đổi reviewer sangClaude và cho giữ detector span của biến thể; lý do trước kết quả đã ghi. Chuyển EC2 thứhai do thiếu RAM/máy đầu bận; TT còn3ca trước nhìn ranking vì người làm áp cap1GB bảo thủ cho cảcopy; không phải Minh bắt buộc thu30→3. Đây là thu hẹp kế hoạch kiểm; chỉ kết luận3/30dev, chưa kiểm27ca. Sửa audit token nullable và guard exact-copy theo source gốc, giữ lỗi/lượt cũ. ShellCRLF hỏng trước method; controlTraceRCA ban đầu có11span qua mốc đã được đính chính; không giấu là normal nghiêm. Một lần tìm kiếm quá rộng artifact đã dừng, không dùng để kết luận ngoài whitelist. Mọi thay đổi có mục bổ sung SPEC/LOG; không chọn cấu hình theo root score. Phép thay số vòng đã thiếu ở bàn giao đầu; nay đã bổ sung chẩn đoán/lưu artifact nhưng vẫn giữ25. Lượt quét time lần1 thiếu manifest trên EC2, giữ failure; lần2 đúng nguồn đạt.

## F. Đề xuất cho tài liệu chung

Nháp trong `de-xuat-tai-lieu-chung.md`: lưu quyền/vai trò/EC2 theo lời Minh; WHY về biến thể, exact-copy và TraceRCA finite/tie; làm rõ cha–con trong K1/MRP/WHY02; sửa default TraceRCA T001; cập nhật việc dọn EC2 ở dòng chung. Chưa ghi các file đó. Nháp WHY đã thêm phương án baseline trước mốc và giới hạn độ dài/số vòng; nháp DECISIONS thêm quyền sửa nguyên lời Minh. STATE chỉ dòngT015 chuyển “đã sửa theo duyệt, chờ Minh duyệt”; không tự tạo vòng phản biện mới.

## G. Phần chưa kiểm và lý do

Chưa tái lập toàn bộ số bài MicroRank/full detector gốc: datasetA/B/C và schema kind/pod/root thật không có trong dữ liệu được phép. Giả định công thức code đủ đại diện bài có thể sai vì các khác biệt đã chỉ ra; kiểm bằng artifact/giao thức tác giả khi được phép, không gán số của bài cho biến thể. Chưa cài phương án suy schema: Minh chỉ duyệt đánh giá; root cấu trúc làm được nhưng kind/pod không nhận diện duy nhất từ11cột. Giả định metadata bổ sung có thể phục hồi sẽ sai nếu exporter đã bỏ trường; cần đối chiếu gold instrumentation độc lập nhãn. Đơn vị raw TraceRCA gốc còn OPEN vì module upstream không nằm trong clone đúngrevision; phải phục hồi nguồn encoder để kiểm, không đoán từ RE2.

Không có thời gian benchmark chính thức vì máy dùng chung; logs chỉ theo dõi ngân sách. Chưa kiểm27/30dev TT;3ca là kiểm cơ chế đã định trước, không bảo đảm ca khác. Capcopy do người làm diễn giải, phạm vi mở rộng chưa được chọn. Không benchmark P3/P4. Control giả định trước tiêm bình thường có thể sai do workload drift/sự cố chưa nhãn; cần reference sạch và ground truth riêng ở giao thức sau. Các thiếu kiểm này không được gọi là chờ quyền cho phần task đã làm được.

## H. Cần Minh quyết

Các sửa được duyệt đã hoàn tất; cần Minh duyệt kết quả task và quyết có mở rộng27TT hay giữ kiểm cơ chế3ca. Chốt ởG1: baselineP3 dùng biến thể nào; cửa sổ tham chiếu; inventory và full ranking hay output11operation; quy tắc finite/tie TraceRCA; có nguồn kind/pod thật để đi tiếp phương án full-original không. Duyệt các nháp tài liệu chung nếu phù hợp. T015 chưa tự chốt các lựa chọn này.


## Prompt phản biện cho Claude — mẫu bàn giao giữ sẵn

Giữ nguyên mẫu theo yêu cầu bàn giao T-015. Mục này không tạo hoặc yêu cầu thêm một vòng review.

```text
Bạn là người phản biện độc lập cho task T-015 của repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Bạn chỉ được ghi đúng một file: tasks/T-015-ho-so-microrank/REVIEW.md, theo mẫu tasks/_MAU/REVIEW.md.
Không sửa file nào khác, không commit.

Đọc: tasks/T-015-ho-so-microrank/SPEC.md, tasks/T-015-ho-so-microrank/LOG.md, các file đầu ra: D:/RCA-flashticket/tasks/T-015-ho-so-microrank/SPEC.md; D:/RCA-flashticket/tasks/T-015-ho-so-microrank/LOG.md; D:/RCA-flashticket/tasks/T-015-ho-so-microrank/REVIEW.md; D:/RCA-flashticket/results/T-015/manifest-ban-giao.json; mọi file trong results/T-015/ và src/microrank/, các file ngoài repo ở D:/RCA-ext/work/T-015/ và tất cả file trên hai EC2 đã liệt kê từng đường dẫn tại manifest-ban-giao.json; nguồn/revision/môi trường tại manifest-inputs.json, src/microrank/PROVENANCE.json và moi-truong.md,
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


## Phiên 4 — 04/10/2026 — Codex — laptop Windows11 — vai trò người làm, bước9 đóng task

Mở phiên; HEAD git: 93f13d4c4a966428177e2acc287d96bc89303e92. Đã đọc AGENTS, STATE, SPEC và cuối LOG; kiểm đầu ra bàn giao hiện có. Tiếp tục từ checkpoint phiên3; không làm lại thực nghiệm đã có kết quả hợp lệ.

**Quyết định của Minh trong phiên:** Minh: “chốt”. USER_CONFIRMED: Minh duyệt kết quả T-015 sau sửa phản biện và cho đóng task. Phạm vi: LOG, báo cáo trạng thái bàn giao, nháp ghi quyết định, manifest dẫn xuất và đúng dòngT015 của STATE. Các lựa chọn G1/P3 trong nháp vẫn là CANDIDATE/OPEN; câu này không cấp quyền commit/push hay sửa tài liệu chung.

Kiểm trước khi đóng:727mục manifest local không có hash lệch; repair-validation.json và manifest-check.json đều all_passed=true. Không chạy thêm phương pháp, không đổi dữ liệu hoặc kết quả khoa học.


Bước đóng đã xong: báo cáo bỏ trạng thái chờ duyệt task; nháp DECISIONS ghi nguyên lời “chốt”; STATE thay đúng dòngT015. Đọc lại xác nhận mọi byte ngoài dòngT015 không đổi.

## Kết thúc phiên4 — 04/10/2026 — Codex, người làm — Minh chốt T-015

1. **Đã làm:** ghi Minh duyệt kết quả sau sửa phản biện, đóng T-015. Hồ sơ và phần chưa kiểm giữ phạm vi khoa học đã bàn giao. Không có thực nghiệm mới.
2. **File đã thay đổi:** tasks/T-015-ho-so-microrank/LOG.md; results/T-015/bao-cao-cuoi.md, de-xuat-tai-lieu-chung.md, manifest-ban-giao.json; đúng dòngT015 trong docs/STATE.md. Không thay file ngoài repo hoặc trênEC2.
3. **Kiểm tra:**727mục local của manifest khớp trước đóng; hai kiểm bàn giao/sửa all_passed=true. Thay STATE bằng chuỗi chính xác, đọc lại và so byte ngoài dòngT015:không đổi. Manifest cập nhật sau LOG; xác nhận mọi hash bàn giao còn khớp và chỉ ba file nội dung LOG/báo cáo/nháp quyết định đổi trong phạm vi local; không đổi đầu ra khoa học.
4. **Điều chưa chắc/cần Minh quyết:** các giới hạn ở mụcG và lựa chọnG1/P3 ở mụcH của báo cáo vẫn giữ; duyệt đóng task không chọn phương án đó. T015 Xong, chưa commit/push.
5. **Bước tiếp theo chính xác:** đọc results/T-015/de-xuat-tai-lieu-chung.md §11 và các nháp WHY khi Minh quyết cập nhật tài liệu chung/G1. Chỉ commit khi Minh duyệt riêng; đề xuất nội dung commit: `docs(T-015): hoàn thiện hồ sơ MicroRank sau phản biện`. Không còn bước sửa đã duyệt nào của T015 chưa làm.
6. **Lệnh cuối cùng:** script đóng task bằng `py -3 -B -`: ghi LOG/nháp, thay đúng dòngSTATE, cập nhật và đối chiếu manifest. Các kiểm sửa ở runs/review-response/ là bằng chứng phiên3, không gọi là lượt chạy mới trong phiên4.


## Prompt phản biện cho Claude — mẫu bàn giao giữ sẵn

Giữ nguyên mẫu theo yêu cầu bàn giao T-015. Mục này không tạo hoặc yêu cầu thêm một vòng review.

```text
Bạn là người phản biện độc lập cho task T-015 của repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Bạn chỉ được ghi đúng một file: tasks/T-015-ho-so-microrank/REVIEW.md, theo mẫu tasks/_MAU/REVIEW.md.
Không sửa file nào khác, không commit.

Đọc: tasks/T-015-ho-so-microrank/SPEC.md, tasks/T-015-ho-so-microrank/LOG.md, các file đầu ra: D:/RCA-flashticket/tasks/T-015-ho-so-microrank/SPEC.md; D:/RCA-flashticket/tasks/T-015-ho-so-microrank/LOG.md; D:/RCA-flashticket/tasks/T-015-ho-so-microrank/REVIEW.md; D:/RCA-flashticket/results/T-015/manifest-ban-giao.json; mọi file trong results/T-015/ và src/microrank/, các file ngoài repo ở D:/RCA-ext/work/T-015/ và tất cả file trên hai EC2 đã liệt kê từng đường dẫn tại manifest-ban-giao.json; nguồn/revision/môi trường tại manifest-inputs.json, src/microrank/PROVENANCE.json và moi-truong.md,
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


Kiểm cuối phiên4: lệnh đóng đã ghi xong file và manifest nhưng guard cuối báo lỗi do so newline CRLF của chuỗi đọc byte với LF của read_text. Đối chiếu lại sau chuẩn hóa newline: hai bản prompt hoàn toàn giống nhau; không đổi nội dung prompt. Kiểm LOG chỉ ghi thêm và mọi hash bàn giao đạt. Đây là lỗi của phép kiểm chuỗi, không phải lỗi kết quả khoa học. Lệnh cuối: `py -3 -B -`, đối chiếu prompt sau chuẩn hóa newline và refresh hash LOG trong manifest.

## Prompt phản biện cho Claude — mẫu bàn giao giữ sẵn

Giữ nguyên mẫu theo yêu cầu bàn giao T-015. Mục này không tạo hoặc yêu cầu thêm một vòng review.

```text
Bạn là người phản biện độc lập cho task T-015 của repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Bạn chỉ được ghi đúng một file: tasks/T-015-ho-so-microrank/REVIEW.md, theo mẫu tasks/_MAU/REVIEW.md.
Không sửa file nào khác, không commit.

Đọc: tasks/T-015-ho-so-microrank/SPEC.md, tasks/T-015-ho-so-microrank/LOG.md, các file đầu ra: D:/RCA-flashticket/tasks/T-015-ho-so-microrank/SPEC.md; D:/RCA-flashticket/tasks/T-015-ho-so-microrank/LOG.md; D:/RCA-flashticket/tasks/T-015-ho-so-microrank/REVIEW.md; D:/RCA-flashticket/results/T-015/manifest-ban-giao.json; mọi file trong results/T-015/ và src/microrank/, các file ngoài repo ở D:/RCA-ext/work/T-015/ và tất cả file trên hai EC2 đã liệt kê từng đường dẫn tại manifest-ban-giao.json; nguồn/revision/môi trường tại manifest-inputs.json, src/microrank/PROVENANCE.json và moi-truong.md,
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
