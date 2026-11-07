# T-054 — điểm dừng trước G3/chạy chính

**Đã hoàn thành gói chuẩn bị thu gọn Minh duyệt. Đang dừng để xét G3; chưa chạy chính, chưa mở test.** Không gọi đây là G3 đã đạt: phản biện/duyệt khóa và quyền nguồn vẫn riêng.

## Kết quả và căn cứ

| Việc | Kết quả | Nguồn |
|---|---|---|
| Tái dùng đầu ra cũ | Checkpoint003 khớp 3.558 pin trước sửa; giữ 40 slot/4 ca, G2 và mọi lượt hỏng. Không lặp baseline dev diện rộng. | LOG phiên5, before.json; manifest003 |
| Điều phối | Plan chỉ 1/2 worker; một supervisor; giữ token/PID khi nhận lại; DRAIN không phát mới; lỗi vận hành dừng phát, unrun không TIMEOUT. Mỗi nhóm method×dataset một slot đồng thời. | operational-checks.json; final2-branch-checks.json |
| Lô mới có mục đích | Hai M1 slot: C-e TT dev-a5cabe5fa7 và main OB dev-607751ac0a. Cả hai OK, khớp toàn trường khoa học so nguồn đã pin. OB khớp normalized input lượt một worker cũ. | pilot-2-worker-001/summary.json#/rows |
| Thực đo 2 worker | 250.171 s trôi; overlap 55.229 s; đỉnh RSS cây đồng thời lấy mẫu 1,426,219,008 byte. Không có clock anomaly, maxgap từng slot <5 s. | cùng summary#/elapsed_s,/overlap_s,/concurrent_sampled_peak_tree_rss,/rows |
| C-e | Tuyến thật từ source/A0→t−300→method→seal→nhãn dev→mô tả đạt. Bằng chứng lịch sử từ native command/coverage đã pin, không gán là nền khỏe. Test phải có mỗi ca một job hỗ trợ hoặc dòng insufficient gắn đúng source; thiếu/trùng/sai bị chặn trước nhãn. | nguon.original_dev_sources; cham.validate_ce_plan; pilot-2-worker-001/descriptive.json |
| ERROR/TIMEOUT | Quy tắc operation mới MicroRank/TraceRCA đọc lại đúng normalized input và đếm N/A; không phân loại chỉ từ chuỗi lỗi. TIMEOUT chỉ từ method start/invocation/deadline/monitor hợp lệ, giữ M4/CIRCA/TORAI variants. Prep/nguồn/clock gap/ERROR lạ vẫn BLOCKED và dừng phát. | failure-policy-g3-candidate.json; operational/final-branch/failure-report checks |
| Độ nhạy | Cả cặp bị loại nếu bất kỳ seed lỗi; giữ NO_EVIDENCE/UNSUPPORTED, CI trên cặp còn lại, rỗng N/A. Hoán vị ca hai phía10.000, seed20261005,+1, so tổng nguyên chính xác. Không đổi phép chính/mức OB. | sensitivity-checks.json; cham.approved_sensitivities |

## Đã chốt theo lời Minh

Nguồn USER_CONFIRMED: quyet-dinh-minh.json. Chấp nhận đúng ba sai khác số học cũ, không dung sai chung; 1 luồng giữ nguyên. Duyệt hai công thức độ nhạy. Không đặt trần cộng dồn P7; chạy đủ, lỗi/không tiến triển/hàng chục giờ chưa xong thì dừng/báo. Đây là ngoại lệ P7, giữ lịch sử Q-40/P3. Sổ chính thức chưa tự ghi; nội dung xin nối nằm trong de-xuat-ghi-so.md.

## Bố trí trình khóa

Local, tối đa2 worker, mỗi phương pháp1 luồng; slot độc lập. Không thêm cache liên vế: đây là lựa chọn vận hành ít công, không biến tối ưu hiệu năng thành điều kiện khoa học. Chọn2 từ bằng chứng overlap/parity và RAM quan sát, không khẳng định nhanh gấp2. Timeout đề nghị600 s/slot, C-d3 60 s; poll0,1 s, maxgap strict<5 s; không tự retry. Các số vận hành này là CANDIDATE để Minh khóa trong de-xuat-khoa-g3.json. Không thay cấu hình phương pháp, cohort hoặc seed.

Matrix giữ94 ca chính: TT60/Nezha34, 1.342 slot chính, C-d3 TT60 riêng, C-e tối đa60; A phụ180 ngoài A4. RE3 không thuộc grant94, không bị bỏ: hợp đồng metadata pha1 đã có ở trien-khai-003/hop-dong-re3.json; H1 schema/H2 adapter và quyền sửa src còn riêng, chưa cài adapter RE3 hoặc mở telemetry. Không nhận TT adapter là RE3 adapter.

## Còn trước khi được phát main

1. Minh xét/khóa G3 đúng byte code, cấu hình/env/matrix, policy và ngoại lệ; phản biện theo quy trình Minh chọn chuyển thủ công. Đồng thuận agent không thay bằng chứng/duyệt Minh.
2. Grant nguồn TT60 + OB34, các cửa sổ/vế/chấm đã khai; dựng private source/label bindings từ G1/nguồn độc lập sau grant, kiểm hash và attestation trước dispatch. Chưa mở nguồn để điền checklist.
3. TORAI A vẫn phụ, cần quyền đúng ba CSV tác giả của cohort TT trước phần A. Grant một ca dev không phải grant cohort. Không chọn lại A/B hoặc tự bỏ A.
4. Minh duyệt nội dung nối DECISIONS/WHY và commit khóa nếu dùng. Chưa commit/push. Các nguồn/hạn chế M4, tiếp xúc TX1/file chung, revision benchmark snapshot OPEN, bootstrap ít ô và cơ chế vật lý chưa phân xử giữ nguyên.

Không có lô pilot/benchmark tiếp theo mặc định. Công việc sau grant là dựng/băm/đối chiếu map/plan cụ thể rồi chạy đúng bản khóa; lỗi phát hiện mới thì dừng đúng phần phụ thuộc, giữ đầu ra và báo Minh.

## Thời gian, giới hạn

Lô mới mất khoảng4 phút10 giây, không phải thêm3 giờ pilot. Kịch bản một worker lạnh25–27 giờ trước đây không là ETA toàn task. Lô2 slot không phải phép so thời gian1/2 trên cùng lô; vì vậy không suy tốc độ tăng hay ETA toàn cohort. Không chạy thêm chỉ để săn ETA; tiến độ thật sẽ cung cấp dự báo khi chạy chính được phép.

RAM host/paging chưa được ghi đầy đủ trong lô thật; không tuyên bố không paging. Driver cuối đã bổ sung quan sát RAM khả dụng/pagefile, kiểm trên mẫu giả. Dung lượng tạm/output toàn cohort chưa có upper bound thực đo; phải theo dõi đĩa và dừng vận hành khi thiếu. Lần chấm lô mới đầu hỏng vì helper chưa canonicalize cell; đã giữ lỗi/script đầu và sửa helper, không lặp method. Kiểm pipeline phát hiện timestamp lấy trước deadline; sửa capture thời điểm quan sát hạn và kiểm lại, giữ lượt hỏng.

Task chưa xong pha2, chưa trả lời RQ3 độc lập, không xác nhận vùng ảnh hưởng/nhân quả vật lý hoặc P/R/F1 phát hiện. Kết quả âm và giới hạn dev vẫn giữ.


Bổ sung kiểm cuối: authorize nay đối chiếu plan với hợp đồng code/config/env/policy đã khóa trước khi có I/O dữ liệu. Metadata giả tráo config rồi rehash, thiếu code/độ nhạy, đổi env/timeout/worker/monitor/budget đều bị chặn; không mở dữ liệu để kiểm. Nguồn: locked-plan-contract-checks.json.

Chú ý audit nhãn lô2slot: hai producer receipt đã VERIFIED trước helper đọc nhãn dev; tệp mang tên snapshot-before-labels được helper ghi sau lookup nhãn. Không dùng tên tệp ấy làm bằng chứng về thời điểm hoặc về mù A4. Thời điểm đọc nhãn riêng không được ghi; khai đúng tại label-exposure-note.json. Các nhãn dev này đã được dùng từ trước. Không có test; đường evaluate chính vẫn kiểm đủ snapshot trước đọc nhãn.
