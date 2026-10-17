# Sửa bộ kiểm dtype TraceRCA — CHƯA DUYỆT

Codex người làm, Claude người phản biện T-032. Phạm vi chỉ results/T-032, LOG/STATE dòngT-032 và ~/rca/T-032. Không sửa SPEC/code chung/môi trường/native/adapter/capture, không dùng tolerance MicroRank.

## Bằng chứng, hậu quả

Lượt path-001 mới chạy nền `runs/tracerca-path-pilots-001/`: fixture6 PASS (15,713s), RE2 ERROR dev-03d4910932 tự dừng lúc13:07:44(+07). Tổng supervisor132,510s, peak tree RSS1.619.939.328B, output khoảng31,6MB; không vượt30phút/200MiB. Không khởi RE2 OK/Nezha. Trạng thái này không là lỗi RAM: guard không báo exhaustion; child TypeError khiến controller dừng.

`re2-error/progress.jsonl`: FROZEN_COMPARE_DONE/match=true. `capture/capture.json`: adapter_returned_status=ERROR, adapter_threw=false, native_outcome=exception với KeyError gốc, hook phục hồi. Path mới đã trả đúng phân loại nguồn, nhưng chưa có verdict trung gian đạt nên **không dùng trung gian làm bằng chứng cơ chế**.

`re2-error/check.json#/traceback`: replay_tracerca_v2.py:205 gọi replay_microrank.table_columns:285, `np.asarray(...,dtype='string')` ném TypeError. Kiểu string/Int64 là extension dtype của pandas, không phải dtype NumPy. Fixture cũ dùng cột object/int thông thường nên không bắt nhánh này. Cùng bộ giải mã đã được sửa cho SimpleRCA và chuẩn bị CIRCA trong task; không thay thuật toán của TraceRCA.

## Sửa tối thiểu đề nghị

1. Tạo replay_tracerca_v3.py từ v2; thêm helper local khôi phục bằng `pandas_dtype`, `pd.array` cho extension và NumPy cho dtype thông thường, decode tagged scalar nguyên trạng. Giữ value/missing/nonfinite/dtype logic/index/order/signature checks. Đọc Parquet verifier `use_threads=False` như bộ đọc SimpleRCA/CIRCA; không tác động native/import/conversion trước phương pháp. Dùng nguyên hàm table_columns trong replay_circa_v2.py đã soát, có pin/AST; không sửa helper chung hoặc script v2.
2. Thêm fixture khôi phục cho string/Int64/boolean/Float64 có/khôngNA, object lẫn None/NA/NaN/inf và float -0/inf. Fixture qua serializer TraceRCA hiện có, phải exact ordered signature; thiếu schema/giá trị lạ dừng. Thêm fixture TraceRCA trên frame extension dtype để bắt đường thật; giữ nguyên6 fixture native/observed hiện có và exact assertions. Không coi chỉ kiểm dtype là chứng nhận phương pháp.
3. Tạo audit_tracerca_posthoc_v1.py: bind hash của toàn output gốc/check/capture/record/source/invocation và nguồn frozen; chỉ đọc ca ERROR đã lưu, chạy nguyên so record và verify_tracerca v3. Lưu verdict mới riêng, không ghi PASS vào lượt FAIL cũ, không chạy phương pháp lại. Kiểm original source audits/actual imports/hooks/formulas/adapter ERROR và khôngmutation; gộp fixture+posthoc≤5phút/50MiB, lỗi dừng/trình/không retry.
4. Chỉ nếu các kiểm sửa và ERROR posthoc đạt: tạo run_tracerca_path_pilots_v2.py với pin v3, tái kiểm ERROR đã lưu và chạy đúng hai pilot còn thiếu RE2OK dev12a1a88069/NezhaOK dev14701a3bbb. Mỗi pilot≤10phút, tổng2pilot≤20phút/150MiB; fail-stop, khôngcohort. Giữ các invariant/source/hash/capture/exact record của controller v1; không bỏ kiểm nào vì đã sửa decoder. Đo lại RAM/bytes/global8GiB trước lượt; tăng vượt dự toán dừng trình.

**Giới hạn:** capture cũ không ghi string storage backend identity. Kiểm exact giá trị, missing scalar, logical dtype và order, không nhận backend đã exact. Đây là giới hạn serialization; không đổi native/backend đang được dùng. Nếu chính giới hạn này khiến verifier không phân xử được mutation, phải dừng trình, không cast tùy tiện. Record/status/điểm/thứ tự/hòa vẫn exact; chưa cho phép sửa native haylaptopTraceRCA.

## File, ngân sách và ảnh hưởng

Tạo3script v3/audit/v2controller như trên; `runs/tracerca-dtype-repair-001/` và monitor lưufixture/posthoc/source/artifact receipts; `runs/tracerca-path-pilots-002/` và monitor lưu2pilot, commands/PIDs/stdout/stderr/progress/cost. Code sửa chỉ trong T-032, inventory/hash2đầu khi chuyển. Giữ toàn v1/v2/lượt lỗi. LOG chỉ nối và STATE chỉ dòngT-032 đọc lại trước sửa.

RAM thực đo lượt path vừaqua khoảng1,62GB; EC2 sau dừng/trướcCIRCAfixture13:11:03 còn7.490.928.640B RAM và23.505.911.808B đĩa, task3.156.779.936B. Đây chỉ snapshot; chờ CIRCA đang chạy kết thúc và đo lại trước sửaTrace. Dự toán posthoc RAM≤2,5GB là chưakiểm, thời gian có thể cao do decode nhiều cột; guard5phút/50MiB không bảo đảm xong. Hai pilot theo số cũ dự kiến2–4phút máy là chưakiểm, guard20phút/150MiB. Tổng sửa+2pilot≤25phút/200MiB, trong global8GiB. Công code/soát khoảng1–2giờ agent dự trù. Mỗi lúc một việc nặng EC2; không chen native mới khiCIRCA đang chạy.

Phương án khác: không sửa bộ kiểm thì TraceRCA chưa có eligibility, tiếp phần độc lập và giữ nghĩa vụOPEN; chạy native lại ca ERROR tốn capture mà không sửa TypeError, không chọn; sửa helper chung ảnh hưởng các phương pháp khác, không chọn. Không nới số/tự bỏ trung gian.

## Dòng DECISIONS xin phép nối cùng lời duyệt

Q-99 vàQ-100 đang được đề xuất riêng; đọc lại DECISIONS trước nối, mã đã có thì trình mã khác, không ghi đè.

| Q-101 | 10/10/2026 | Minh duyệt đúng results/T-032/de-xuat-tracerca-dtype-002.md: chỉ verifier TraceRCA v3 khôi phục pandas logical extension dtype, giữ exact value/missing/dtype/index/order và mọi native/capture/record invariant; không sửa code chung/SPEC/tolerance. Fixture dtype/adapter và6fixture cũ+posthoc ERROR đã lưu ≤5phút/50MiB đạt mới chạy đúng2pilot còn thiếu bằng controller v2, mỗi≤10phút, tổng≤20phút/150MiB, khôngcohort/retry; giữ mọi bản/lượt lỗi, không dùng trung gian trước kiểm đạt, string backend lịch sử chưa được ghi vẫnOPEN; đoRAM/global8GiB trước lượt và một việc nặng EC2, lỗi/vượt dừngtrình; cho nối đúng dòng này sau đọc lại DECISIONS. | lời duyệt Minh; results/T-032/de-xuat-tracerca-dtype-002.md |
