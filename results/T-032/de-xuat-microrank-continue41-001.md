# Đề xuất kiểm tiếp 41 ca MicroRank — CHƯA DUYỆT CHẠY

Người làm: Codex; người phản biện chính thức: Claude. Chỉ T-032/EC2 3.26.62.217. Không sửa SPEC, WHY-42, phương pháp, adapter dùng chung, môi trường hoặc dữ liệu. A′ vẫn bị chặn.

## Chỗ cần đổi, bằng chứng và hậu quả

Cohort cũ dừng đúng quy định tại RE2 `dev-3defe3d34b`. Nguồn hash hai đầu và 15 file đóng kiểm lại PASS: `runs/microrank-cohort-failure-001/transport-check.json`; metadata/dự toán: `runs/microrank-continue41-proposal-001/forecast.json#/source_checks`. Có 10 PASS (hai pilot tái dùng), một blocked, 41 not_run (20 RE2/21 Nezha). Ca blocked có max 41 ULP, relative 4,731118408006869e-15; ngưỡng 16 ULP và 16×2^-52 giữ nguyên.

Native–observed exact, trạng thái, service order/ties, Hit@1..10 và outside-whitelist đều đạt; **cờ T-028 chưa kiểm** (`failed-case/roundoff-comparison.json#/t028_flags/status=NOT_PERFORMED`). Wrapper v3 dòng 465–466 dừng trước bridge; bridge v3 dòng 406–415 bắt buộc prerequisite approved_record_comparison_passed=true. Không được suy rằng mọi kiểm khác đã đạt, cũng không được gán true giả để vượt gate. Dừng toàn cohort làm 41 ca chưa có mức lệch; chạy tiếp sẽ chỉ khảo sát độ khớp, không chữa ca blocked hoặc làm lõi đủ52.

## Đề xuất sửa tối thiểu sau duyệt

1. Giữ nguyên comparator hiện hành, mọi script/run cũ và dữ liệu. Tạo bridge v4 **có lối chẩn đoán riêng** cho record bị chặn chỉ vì score threshold: xác thực hash và verdict comparator đầy đủ, exact native–observed và mọi invariant phi số trước khi tái dùng helpers T-028 nguyên AST. Không giả mạo prerequisite PASS. Lối này tính frozen self-check, observed flags M tại k=1/5, P0/N/reasons/graph-role, đầy đủ Hit@1..10 và ranking view; so exact như bridge v3. Verdict chẩn đoán có `non_numeric_checks_passed` riêng; `record_contract_pass=false`, `eligibility=false`, `intermediates_eligible=false`, status `SCORE_THRESHOLD_BLOCKED` giữ nguyên. Nhánh ca đạt comparator vẫn dùng hợp đồng v3 đầy đủ. Không đổi byte record/điểm hay tolerance.
2. Fixture trước: biên 16/17 ULP, relative, zero/sign/nonfinite; numeric-only nhưng T-028/order/ties/Hit/mapping/metadata/source/hook/observer lỗi phải dừng; verdict thiếu/không ghép được cũng dừng. Kiểm tự-đối-chiếu đủ52 frozen; kiểm posthoc đúng ca blocked đã lưu, không chạy lại native. Gộp fixture/self-check/audit ≤120 giây/15 MiB. Hỏng thì dừng trình, không retry. **Chỉ khi audit ca blocked xác nhận mọi kiểm phi số đạt mới được bước 3.**
3. Wrapper v4 giữ one observed + one independent native như v3, nguồn/F/config/hashseed/capture/formula/import/hook/input checks giữ nguyên. Sau so comparator, luôn hoàn tất bridge phù hợp trước quyết định điều phối. Ca PASS giữ đầy đủ eligibility; ca numeric-only vượt ngưỡng bị chặn riêng chỉ khi mọi điều kiện dưới đây đạt. Không sửa việc so exact native–observed. Ca lỗi khác dừng toàn MicroRank và không khởi ca sau.
4. Controller v4 chỉ chạy đúng 41 not_run theo plan cũ và nguồn frozen đã hash; không chọn theo root/caller/điểm/khả năng cải thiện. Tái kiểm bindings của 10 PASS và ca blocked cũ, không chạy phương pháp lại các ca này. Một worker nặng trên EC2, nền độc lập SSH/laptop; PID/progress/stdout/stderr/time/RSS/bytes/manifest theo ca. Nhánh chặn riêng trả exit code riêng, controller chỉ tiếp khi verdict hoàn chỉnh và tất cả điều kiện đạt, không coi process exit0 là đủ.
5. Giữ bảng đầy đủ52 theo dataset và classification: exact/numeric_only/operation_order/service_order_changed/blocked/not_run; từng ca lưu max ULP/relative và khoảng cách tới ngưỡng. ERROR không có score pairs giữ null. Ghi rõ ca numeric_only ở đây là **PASS dưới ngưỡng**, numeric threshold blocked là nhóm blocked, không nhập hai nhóm. Bảng đếm thiếu và verdict thô được giữ, không che drift.

### Điều kiện duy nhất cho chặn riêng rồi tiếp

- Comparator chỉ báo các lỗi **điểm operation/service hữu hạn vượt ULP hoặc relative**. Danh sách lỗi whitelist là các mục `operation_score_outside_contract:…:ulp_limit_exceeded|relative_limit_exceeded` hoặc service tương ứng. Zero/sign/nonfinite, schema, đảo operation ngoài hợp đồng, khóa sắp xếp, mọi lỗi khác đều dừng toàn phương pháp.
- Exact trạng thái/service order/service exact tie partition/Hit@1..10/cờ M cùng P0/N/reasons; candidate/mapping/max aggregation/window/input/source/metadata/counts đúng, ngoài whitelist rỗng. Các inversion operation nếu có vẫn phải cùng service và sát ngưỡng **ở cả hai output**, không làm đổi service. Không bỏ kiểm vì ca vượt ngưỡng số.
- Native–observed exact, capture/formula/intermediate/hook/source hash/actual import đều đạt; cờ T-028 chẩn đoán exact đạt. Không có kiểm NOT_PERFORMED, thiếu output hay lỗi tài nguyên. Không chỉ lọc chuỗi thông báo cuối cùng để quyết tiếp.
- Ca bị chặn giữ mọi output để chẩn đoán nhưng **không dùng trung gian, cơ chế hoặc A′**. Nếu chỉ cần một invariant chưa đạt/không xác minh được, dừng toàn phương pháp và trình Minh. Không tự tăng ngưỡng. Lõi toàn52 và A′ vẫn chặn kể cả 41 ca mới đều đạt.

## File sẽ tạo sau duyệt và phạm vi ảnh hưởng

- `scripts/check_microrank_t028_v4.py`: giữ lối v3 và thêm verdict chẩn đoán không cấp eligibility.
- `scripts/replay_microrank_approved_v4.py`: thứ tự kiểm/nhánh verdict nêu trên, pin bridge mới; không đổi native/capture/comparator.
- `scripts/batch_microrank_approved_v4.py`: controller whitelist/41 bindings/pins/table/guard mới.
- `runs/microrank-continue41-prepare-001/`: reviewed plan, 41 IDs/resource estimates, script/source hashes, fixture/self-check/audit receipts.
- `runs/microrank-continue41-check-001/` và `…-monitor/`: fixture+posthoc, stdout/stderr/progress/PID/status/manifest.
- `runs/microrank-continue41-001/` và `…-monitor/`: case outputs/native/observed/comparator/bridge/control table52/events/cost/hash; launcher `.out/.err/.pid` cùng runs.
- `runs/microrank-continue41-export-001/`: nếu cần nhận kết quả, archive/inventory/check hai đầu và bản nhận đúng scope; kiểm tổng bytes trước export.
- LOG chỉ nối; STATE chỉ dòng T-032 đọc lại trước sửa. DECISIONS chỉ dòng Q-99 bên dưới **nếu Minh duyệt nối**. WHY chỉ mục mới theo đoạn dưới **nếu Minh duyệt nối**, đọc lại trước nối và không sửa WHY-42/mục cũ. Mã đã dùng thì dừng trình mã mới, không ghi đè.

Đây là thay đổi chính sách dừng và bộ kiểm/điều phối, không là thay đổi khoa học của phương pháp. Chưa tạo script v4/run phương pháp trong lượt soạn đề xuất. Mọi ca/lượt lỗi cũ giữ nguyên.

## Chi phí đo lại và dự toán, không coi là upper bound

Nguồn chi tiết/từng41 ca: `runs/microrank-continue41-proposal-001/forecast.json` và plan cũ được hash. Laptop đo 13:01:46 (+07): T-032 866.203.323 byte. EC2 đo 12:57:08: task 3.124.362.990 byte, MemAvailable 7.496.232.960 byte, disk free 23.538.966.528 byte, không tiến trình task. Tổng đo 3.990.566.313 byte (~3,72 GiB). Snapshot này trước chuyển path TraceRCA, **không dùng làm preflight cohort**.

EC2 cohort vừa đo 211,943 giây/peak tree RSS 2.143.158.272 byte cho phần mới; ca blocked 39,856 giây/30.893.030 byte. Forecast lọc đúng41 từ dự toán pilot/shape/source cost với hệ số2 cũ: **3.685,674 giây (~61,43 phút), 1.593.230.095 byte (~1,48 GiB) mới remote, peak dự trù 7.082.750.509 byte**. Peak dự trù chỉ cách RAM khả dụng đo khoảng413 MB, phải đo lại sau Trace và giữ ≥256 MiB khoảng trống theo guard; không có bằng chứng mọi ca đã vừa RAM. Forecast có thể sai vì đường xử lý/RAM không tỷ lệ input, serializer/capture/OS khác nhau; sai thì dừng, không giảm kiểm.

Tính thêm full download cùng lượng output và 200 MiB archive/reserve: dự toán kết hợp 7.386.741.703 byte (~6,88 GiB), dưới trần8GiB; chưa gồm mọi output tương lai CIRCA/TORAI nên **không giữ chỗ ngầm cho chúng**. Đo lại local+remote+temp/cache/archive/lượt hỏng trước mọi lượt lớn; lớn hơn ngân sách/dự toán được duyệt thì checkpoint/dừng/trình.

Đề nghị guard fixture+audit≤120s/15MiB; cohort≤2 giờ tổng, từng ca≤600s/150MiB như cũ, total combined≤8GiB. Thời gian dự kiến khoảng65–80 phút máy gồm kiểm/điều phối là **chưa kiểm**, guard không bảo đảm hoàn thành. Việc làm code/soát/đọc kết quả khoảng2–4 giờ agent là dự trù. TraceRCA pilot phải xong trước cohort; không tự chạy cohort dù đã có quyền chẩn đoán laptop. Không chạy nặng trên laptop trong chẩn đoán MicroRank.

Phương án thay thế: giữ cohort/A′ OPEN và tiếp phương pháp độc lập; hoặc phát lại trên laptop nguồn sau chẩn đoán laptop-001 và benchmark/dự toán được Minh duyệt riêng. Chưa được chạy cohort laptop; chưa có benchmark laptop để so chi phí thực hai máy. Kiểm tiếp41 EC2 cho biết phạm vi drift nhưng không giải thích thành phần môi trường gây drift hoặc khôi phục partition lịch sử.

## Dòng DECISIONS đề nghị nối sau duyệt

| Q-99 | 10/10/2026 | Minh duyệt đúng results/T-032/de-xuat-microrank-continue41-001.md: chỉ MicroRank, thêm bridge/wrapper/controller v4 với lối chẩn đoán phi số không cấp eligibility; fixture+frozen52 self-check+posthoc ca blocked ≤120 giây/15 MiB đạt mọi kiểm phi số mới kiểm tiếp đúng41 not_run sau pilot TraceRCA xong; chỉ score hữu hạn vượt ngưỡng ULP/relative và mọi invariant/source/capture/native–observed/T-028/Hit/order/ties/mapping đều đạt mới chặn riêng ca rồi tiếp, lỗi khác dừng toàn phương pháp; giữ nguyên ngưỡng/comparator/native/capture/record/các bản cũ, ca blocked không dùng trung gian, lõi toàn52 và A′ vẫn chặn; guard cohort≤2 giờ, từngca≤600s/150MiB, đo lại tổng≤8GiB và RAM trước chạy, vượt dừng/trình; bảng52 từngca max ULP/relative và phân loại/denominator đầy đủ; không cohort laptop/đổi SPEC/WHY-42/code chung/test/commit/push; cho nối đúng dòng này và đoạn WHY bổ sung trong đề xuất sau đọc lại file. | lời duyệt Minh; results/T-032/de-xuat-microrank-continue41-001.md |

## Đoạn WHY mới trình Minh duyệt, không sửa WHY-42

**Chọn:** kiểm tiếp41 ca chưa chạy trên EC2 bằng policy chặn riêng chỉ cho score vượt ngưỡng và mọi kiểm phi số đạt; mọi lỗi khác dừng toàn phương pháp. Giữ ngưỡng, source/record và A′ bị chặn; ca blocked chỉ phục vụ chẩn đoán, không dùng trung gian trong báo cáo cơ chế.

**Vì sao:** một ca vượt ngưỡng chưa cho biết phạm vi lệch trên toàn52. Tiếp có điều kiện giúp đo đầy đủ độ khớp mà không chấp nhận điểm ngoài ngưỡng hoặc che kiểm chưa làm. Cờ T-028 của ca dừng chưa kiểm nên cần lối audit độc lập, không gán prerequisite PASS giả.

**Phương án đã xét:** dừng toàn cohort giữ nghĩa vụ MicroRank OPEN (ít chi phí hơn nhưng còn41 chưa đo); tăng tolerance (trái ngưỡng khóa, không chọn); chạy lại native EC2 ca lỗi (chưa có bằng chứng giúp, không chọn); chuyển cohort laptop (chưa benchmark/dự toán/quyền, chỉ xem sau chẩn đoán một ca). Policy này không thay cho khớp đủ lõi hoặc lý giải nguyên nhân drift.

**Bằng chứng và phần chưa kiểm:** bảng cohort đã hash:10 PASS,1 blocked,41 not_run; native–observed và invariant record đã nêu của ca blocked đạt nhưng cờ T-028 NOT_PERFORMED. Audit phi số/v4 và41 ca chưa chạy; chi phí toàn41 và khả năng vừa RAM chỉ là dự trù. Chẩn đoán laptop-001 đã duyệt nhưng chưa có kết quả. Hash/bindings/dự toán theo receipt trong đề xuất; sau kết quả phải trình đoạn bổ sung về bằng chứng/bảng52 cho Minh duyệt trước dùng MicroRank trong báo cáo, không tự sửa mục cũ.

**Kết luận phụ thuộc:** đo phạm vi drift và eligibility từng ca; không xác nhận cơ chế MicroRank/A′ khi toàn lõi cònblocked, không chứng minh nguyên nhân môi trường, chờ/lan vật lý hoặc partition lịch sử. Ca PASS có thể được lần theo theo invariant đãduyệt, vẫn cần đối chứng cùng điều kiện và nghĩa vụ nhóm đầy đủ; không suy từ subset rằng toàn52 hoặc RQ2/G2 đã xong.
