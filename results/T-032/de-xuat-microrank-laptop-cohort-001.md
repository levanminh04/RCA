# MicroRank: đề xuất phát lại đủ 52 ca trên laptop — CHỜ MINH DUYỆT

Codex người làm, Claude người phản biện T-032. Đây là đề xuất theo nhánh laptop exact của Q-118, chưa là quyền chạy. Q-94 giữ hiệu lực; không áp ngưỡng mới, không chạy tiếp 41 ca trên EC2 hoặc A′ trong gói này. Chỉ hai file đề xuất được tạo lúc soạn; chưa tạo code/cohort.

## Bằng chứng và mục đích

Ca RE2-TT `dev-3defe3d34b` đã hoàn tất chẩn đoán Q-97/Q-100. Receipt `runs/microrank-laptop-diagnostic-verification-001/check.json` có `/status=PASS_SINGLE_CASE_EXACT_DIAGNOSTIC`, `/native_observed_frozen_exact=true`, `/source_input_import_function_hook_checks_passed=true`; PID đã kết thúc ở `/pids_checked_gone`. Đã kiểm hash 77 artifact theo `/verified_files`, controller theo `/controller_sha256` và manifest đóng theo `/closed_sha256`. Native–frozen, observed–native và observed–frozen khớp tuyệt đối các trường của comparator gốc, gồm type và `float.hex`; chỉ `run_id`/`cost` khác được loại theo nguồn. Đây là một ca hiện tại, chưa chứng minh cả cohort hoặc nguyên nhân drift EC2.

Mục đích là có đủ trung gian MicroRank từ các lượt khớp tuyệt đối để làm phần lõi đã duyệt: membership/cờ span, baseline/excess, counts, PageRank, spectrum, ánh xạ operation→service và caller/root. Khớp đầu ra là điều kiện dùng trung gian, không là kết luận caller chờ root hoặc lợi ích đồ thị. Diagnostic hiện chưa eligible trong báo cáo; chưa có audit T-028 bridge v3 cho lượt laptop này. Không sửa cờ eligibility trong artifact cũ để biến nó thành đạt.

## Phạm vi đề nghị và các checkpoint

1. Khóa lại cùng 52 ca: 30 RE2-TT, 22 Nezha-OB, MicroRank full/main, nguồn T-024/T-026/T-031, cấu hình/cửa sổ F/hashseed0 đúng bản đã chấm. Danh mục kiểm chéo từ `runs/microrank-cohort-failure-001/cohort/52-cases.json#/rows`; hash đã khớp entry tương ứng trong `runs/microrank-cohort-failure-001/transport-check.json#/files`. Trạng thái EC2 cũ không phải verdict laptop. Đối chiếu từng source record/config/allowlist với manifest gốc trước dùng; không đổi ca, không bỏ non-OK, không chọn theo điểm hoặc kết quả phát lại mới.
2. Tạo và tự soát các công cụ mới trong bảng ảnh hưởng dưới đây. Giữ code phương pháp/adapter/capture/comparator gốc và bridge v3. Dùng interpreter nguồn `D:/RCA-ext/envs/T-014-main/Scripts/python.exe`, Python3.12.10/package theo pin nguồn, `-B -X utf8`, không ghi bytecode. Năm biến OMP/OPENBLAS/MKL/NUMEXPR/VECLIB hiện unset theo ngoại lệ Q-100; mở rộng ngoại lệ này cho cohort phải được Minh duyệt ở dòng Q-124. Ghi/kiểm BLAS/threadpool/import/function/hooks trước–sau; thread lịch sử vẫn OPEN. Không tự đặt thread hoặc cài package.
3. Fixture đầy đủ của observer/comparator/bridge v3 và frozen self-check đủ 52 hàng T-028 phải đạt. Fixture thêm chỉ cho wrapper laptop hai dataset, binding và fail-stop: đổi một bit float, dấu zero, type, nonfinite, số đếm, mapping/ứng viên, thứ tự operation/service, partition hòa service, Hit/cờ T-028 đều phải bị phát hiện; nguồn/manifest hỏng hoặc lỗi child không được cho chạy observed/ca kế. Kiểm record Nezha đúng nhánh provenance `run.py` hoặc reused `run_pilot.py`, không dùng base/config RE2 cho Nezha. Không bỏ kiểm cũ.
4. Audit hồi cứu ca laptop `dev-3defe3d34b` đã có bằng manifest đóng: so exact độc lập, đủ mapping/counts/Hit@1..10/cờ T-028 qua bridge v3 nguyên nguồn, capture và provenance. Chỉ đọc artifact, không chạy lại native/observed. Nếu lỗi thì dừng toàn nhánh. Audit mới giữ source pointers, không đổi verdict/file diagnostic cũ.
5. Chạy pilot Nezha `dev-14701a3bbb`, là opaque_id nhỏ nhất trong danh mục Nezha source OK đã khóa. Đây là một trong 51 ca mới, không cộng thành ca thứ 53. Đo trọn native/observed/audit/close: wall, RAM, bytes, dữ liệu/quy mô/coverage và code path. Không suy pilot đại diện mọi Nezha hay ca lớn nhất. Trần riêng 10 phút/150 MiB mới; lỗi hoặc vượt thì dừng và trình. Chỉ sau pilot exact và full invariant đạt mới cập nhật dự toán theo dataset, xét metadata quy mô của phần chưa chạy, ghi LOG/forecast và checkpoint trước phần còn lại. Nếu không đủ căn cứ trong trần thì trình dự toán/phạm vi mới, chưa chạy phần đó.
6. Chỉ khi checkpoint pilot chứng minh dự toán còn trong trần đã được duyệt: tuần tự 50 ca mới còn lại, giữ thứ tự dataset rồi opaque_id trong plan; một worker phương pháp tại một thời điểm. Mỗi ca tối đa một native; native exact frozen mới tối đa một observed, rồi observed exact native và frozen. Không retry, bỏ ca, tăng ngưỡng hoặc tiếp qua lỗi. Không chạy công việc nặng khác trên laptop. EC2 chỉ theo lịch một việc nặng tại một thời điểm của Q-123; gói này không xin chạy MicroRank trên EC2.

Tổng là 52 hàng: một ca audit hồi cứu + 51 ca mới, tối đa 102 lời gọi phương pháp mới. Trạng thái non-OK đóng băng vẫn có hàng: phải exact trạng thái, error/diagnostics và nhánh đầu ra. ERROR nguồn được tái hiện exact là quan sát non-OK hợp lệ, không là lỗi mới để bỏ ca; nó không có điểm/intermediate cơ chế hợp lệ nếu nhánh không sinh ra. Lỗi công cụ, lỗi khác nguồn hoặc kiểm không đạt đều dừng toàn nhánh. TIMEOUT không được giả tái lập bằng đổi thời hạn; nếu có trong danh mục mà công cụ chưa hỗ trợ đúng thì dừng trình trước ca đó.

## Hợp đồng kiểm và bảng 52 ca

- Giữ nguyên nguồn/job/adapter/cửa sổ/seed/hashseed/ứng viên và phép max service. Nhãn chỉ nối sau phương pháp cho phép chấm/bridge; tên ca/nhãn/root không vào payload MicroRank.
- Laptop dùng **exact**, không dùng quyền dung sai Q-94 cho nhánh này. Giữ exact trạng thái, mapping/tập ứng viên, mọi số đếm, operation và service order, partition hòa service, các khóa/điểm, zero/dấu/nonfinite, Hit@1..10 và mọi trường/cờ T-028. Native–observed exact. Capture phải hợp lệ ở mọi đầu vào/trung gian và nhánh thiếu/N/A; self-check frozen T-028 không thay thế phát lại từng ca.
- Bảng `52-cases.json#/rows` và bản Markdown có từng dataset/opaque_id/source_status/laptop_status, số cặp điểm, max ULP/max tương đối, mọi verdict exact/capture/bridge, lý do blocked/not_run/N/A, và con trỏ source/native/observed/closed manifest. Điểm có cặp exact ghi 0 sau audit thực; không có cặp điểm hoặc chưa có output ghi null, không giả 0. Bảng vẫn đủ 52 hàng khi dừng sớm. Báo riêng exact, non-OK exact, numeric difference, service/order/tie difference, other error và not_run; không gộp thành tỷ lệ cơ chế.
- Mọi khác số, dù dưới 16 ULP, dừng cohort laptop; không chuyển tự động sang tolerance EC2 hoặc 1e-9. Không dùng trung gian ca bị chặn. Ca trước đạt được giữ nhưng kết luận toàn phương pháp/A′ vẫn chặn khi lõi chưa đầy đủ. A′ không thuộc gói này; quyền cũ chỉ kích hoạt sau đủ điều kiện lõi của SPEC.
- Manifest đóng cuối phải hash cả terminal/check/progress/stdout/stderr sau đóng streams, với PID/trạng thái/lệnh đầy đủ. Lỗi được ghi trước manifest cuối; không chạy tiếp trên artifact chưa kiểm.

## Chi phí đã đo và dự toán còn chưa kiểm

Tất cả số đo dưới đây thuộc `runs/microrank-laptop-diagnostic-verification-001/check.json`:

| Đại lượng của một ca RE2 | Giá trị và con trỏ |
|---|---|
| Trọn chẩn đoán | 99,6289197 giây, `/wall_s` |
| Native worker | 7,391556 giây; peak working set 1.255,56640625 MiB, `/mode_summaries/native/cost` |
| Observed worker | 31,634068 giây; peak working set 1.522,27734375 MiB, `/mode_summaries/observed/cost` |
| Guard process tree, đo theo poll | 1.521.946.624 byte, `/guard/peak_tree_rss`; không là cận trên tuyệt đối |
| Dung lượng diagnostic đã đóng | 30.669.327 byte, `/new_bytes_closed` |

Phép ngoại suy chi phí đơn giản, **chưa kiểm trên Nezha hoặc các ca lớn**: `51 × 99,6289197 / 60 = 84,684581745` phút máy, khoảng 1 giờ 25 phút; `51 × 30.669.327 = 1.564.135.677` byte mới (1,4567 GiB). Chưa bao gồm chi phí fixture/audit bổ sung hoặc sự khác nhau của dataset, quy mô và code path. Một ca không cung cấp upper bound RAM, thời gian hoặc dung lượng. Pilot Nezha chỉ bổ sung một phép đo, cũng không trở thành upper bound cohort.

Đề nghị **trần toàn gói 3 giờ máy và 2,5 GiB mới**, gồm code/fixture/pilot/audit/controller/lượt hỏng/manifest; không phải cam kết xong trong ba giờ. Trần từng ca 10 phút/150 MiB và checkpoint giữa các ca; nếu dự toán còn lại vượt ngân sách hoặc các giới hạn thực đo không đủ thì dừng trình, không ép xong bảng. Gate RAM trước mỗi worker giữ ít nhất **4.554.752.000 byte khả dụng**, giới hạn process tree cũ 4.286.316.544 byte; chưa đủ thì báo Minh giải phóng thêm, không hạ gate. Peak worker Windows và peak tree lấy mẫu khác cách đo, không chọn số nhỏ hơn làm bảo đảm.

LOG T-032 tại mốc 16:25:58 ngày10/10 ghi local trước diagnostic 992.372.033 byte, EC2 3.743.441.061 byte, tổng 4.735.813.094 byte. Cộng diagnostic closed cho ước tính local khoảng 1.023.041.360 byte; đây không phải inventory mới của toàn task vì sau đó còn artifact/receipt khác. Cộng ngoại suy 51 ca cho khoảng 2,4095 GiB local, **không vừa trần local 2 GiB đang có hiệu lực**. Do đó xin Minh đổi riêng trần local thành **4 GiB**, giữ tổng T-032 **12 GiB**, cohort mới tối đa 2,5 GiB; kiểm lại inventory local+EC2, phần tạm/lượt hỏng và chỗ trống ngay trước pilot/batch, không chỉ cộng các lượt PASS. Không tự áp trần mới trước lời duyệt. Công cụ guard polling có thể vượt một ít trong bước đang chạy; không tuyên bố filesystem quota, dừng/ghi mức vượt và trình.

Laptop phải bật suốt mọi lời gọi và audit đang chạy; launcher chạy ẩn độc lập với cửa sổ Codex nhưng phụ thuộc laptop. Báo **CẦN GIỮ LAPTOP MỞ** khi bắt đầu, lý do/ước lượng 1,5–3 giờ sau pilot và lệnh progress trong LOG; không dùng thông báo “EC2 ổn định” để cho tắt laptop khi laptop tính. Checkpoint dừng an toàn cho phép nghỉ máy giữa ca; phiên sau kiểm manifest/PID rồi chỉ tiếp phần chưa chạy trong quyền. Không tự bật/tắt laptop hoặc EC2.

## File sẽ tạo và ảnh hưởng sau lời duyệt

Tất cả đường dưới đây ở `results/T-032/`; giữ mọi bản cũ, không sửa code dùng chung/SPEC/WHY-42 hoặc nguồn đóng băng:

| File/thư mục mới | Nội dung và ảnh hưởng |
|---|---|
| `scripts/replay_microrank_laptop_exact_v1.py` | Bản mới từ diagnostic v2/exact replay gốc: tham số 52 ca hai dataset; giữ native/capture; thêm đúng reconstruction Nezha nguồn, exact/bridge đầy đủ và guards. Không sửa bản cũ. |
| `scripts/batch_microrank_laptop_exact_v1.py` | Plan khóa, audit ca có sẵn, pilot rồi checkpoint, một worker, trần/stop/resume giữa ca; bảng 52 hàng và counts vận hành. |
| `scripts/start_microrank_laptop_cohort_001.ps1` | Launcher ẩn, PID, command, stdout/stderr, watchdog và manifest đóng sau streams; không mở phiên native lặp. |
| `runs/microrank-laptop-cohort-001/source-pin-manifest.json`, `plan-52.json`, `benchmark.json`, `forecast.json` | Pin/source/authority/chi phí; forecast có phạm vi chưa đo và inventory local+EC2 thực. |
| `runs/microrank-laptop-cohort-001/tool-check/` | Diff/AST/source binding, fixture và self-check 52 frozen T-028; manifest/check/stdout/stderr; chưa cấp eligibility cho ca chưa phát lại. |
| `runs/microrank-laptop-cohort-001/retrospective-dev-3defe3d34b/` | Audit chỉ đọc diagnostic đã đóng, exact/bridge/ULP table/binding verdict mới; không sửa run cũ. |
| `runs/microrank-laptop-cohort-001/cases/<dataset>/<opaque_id>/` | 51 thư mục mới, mỗi ca có native/observed/source/env/cost/check/capture/T028 verdict/manifest và con trỏ. Giữ partial/error; không xóa. |
| `runs/microrank-laptop-cohort-001/{52-cases.json,52-cases.md,status.json,progress.jsonl,command.json,launcher.pid,controller.pid,controller-stdout.txt,controller-stderr.txt,terminal.json,manifest.json}` | Kết quả đủ hàng cả khi dừng, trạng thái/PID và kiểm đóng; manifest không tự hash chính nó. |
| `runs/microrank-laptop-cohort-001/root-verification/` | Kiểm độc lập hash/source/52 rows/exact/bridge/counting/inventory trước dùng. |

`LOG.md` chỉ nối mỗi bước/checkpoint; `STATE.md` chỉ dòng T-032 sau đọc lại. DECISIONS chỉ nối dòng Q-124 dưới nếu Minh duyệt; WHY chỉ nối nguyên đoạn của `why-microrank-laptop-001.md` khi Minh duyệt riêng đoạn ấy, lấy mã mới sau đọc lại, không sửa WHY-42. Báo cáo nghiên cứu vẫn theo SPEC; đề xuất này chưa nhập diagnostic/capture vào ba master và không cấp quyền chỉnh kết luận khoa học trước audit/WHY đạt.

## Phương án thay thế để Minh chọn

1. **Đề nghị:** full 52 theo exact, local 4 GiB, tổng 12 GiB, các trần/checkpoint trên. Giảm khác môi trường bằng chính laptop vừa exact; vẫn có nguy cơ ca khác lệch/tốn hơn. Chỉ dùng kết quả sau toàn kiểm.
2. **Giữ local 2 GiB:** xin một phạm vi riêng chuyển các chunk đã đóng sang `~/rca/T-032/` trên EC2, kiểm hash hai đầu rồi đổi nơi lưu và cơ chế đọc/audit. Tốn transfer/agent/EC2 storage, cần đo lượt nhỏ/dự toán; bản sao ở hai nơi đều tính dung lượng khi cùng tồn tại. Không tự xóa bản laptop/source/lượt cũ để lách trần; đề xuất này chưa cấp quyền chuyển/xóa/move các chunk laptop mới.
3. **Chỉ pilot Nezha rồi trình:** giảm cam kết trước khi biết cost hai dataset, chưa duyệt 50 ca còn lại. Giữ trần local 2 GiB nếu inventory thực+150 MiB còn đủ; nếu không thì dừng. Chưa đáp ứng lõi đủ52/G2/A′. Đây là lựa chọn hẹp thay cho phương án1; cần Minh chọn rõ, không tự mặc định.

## Một dòng DECISIONS xin duyệt cùng phương án1

Đây là **draft**, chưa nối. Q-124 đang trống khi soạn; đọc lại DECISIONS ngay trước nối, nếu đã dùng thì trình mã mới, không ghi đè:

| Q-124 | 10/10/2026 | Minh duyệt đúng phương án1 tại results/T-032/de-xuat-microrank-laptop-cohort-001.md theo nhánh laptop exact Q-118: một audit hồi cứu ca Q-97/Q-100 và 51 ca dev mới (30RE2+22Nezha toàn bảng), mỗi ca tối đa một native rồi một observed chỉ khi native exact frozen, mọi record/điểm/operation/service/tie/count/mapping/Hit@1..10/cờ T-028 exact qua bridge v3, đầy đủ source/capture/fixture; pilot Nezha dev-14701a3bbb ≤10phút/150MiB đạt rồi đo lại dự toán/checkpoint trước remainder, lỗi hoặc vượt dừng toàn nhánh/không retry/bỏ ca/tolerance; tổng gói ≤3giờ máy/2,5GiB mới, local trần4GiB thay2GiB, giữ tổng12GiB và gateRAM4.554.752.000B, current5threadunset theo ngoại lệQ100 mở rộng chỉ cohort này/thread lịch sửOPEN; chỉ bản code/run mới T032 và LOG/dòngSTATE, giữ mọi bản/lượt cũ, khôngSPEC/WHY42/codechung/test/locked/T033/commitpush; bảng52 maxULP/maxrelative/null đúng trường hợp và source pointers, chưa41EC2/A′, WHY bổ sung cầnMinhduyệt trước dùngMicro trongbáocáo; cho nối đúng dòng này sau đọc lạiDECISIONS. | Lời duyệt Minh; results/T-032/de-xuat-microrank-laptop-cohort-001.md |
