# TraceRCA dtype — công cụ đã soát tĩnh, chưa chạy

Codex hỗ trợ người làm T-032. Q-101/Q-108/Q-109 và lời duyệt hiện hành vẫn giữ exact cho TraceRCA. Không SSH, không gọi phương pháp hoặc fixture trên laptop, không đọc test/locked/T-033. Các giá trị ngân sách trong đề xuất cũ là lịch sử; trần hiện hành là 12 GiB tổng, laptop tối đa 2 GiB.

## File và phạm vi

- `scripts/replay_tracerca_v3.py`: giữ nguyên byte bản draft đã chuẩn bị; helper `table_columns` có AST nguyên bản từ CIRCA v2. Phát lại `one` có AST nguyên bản của TraceRCA v2. Bộ kiểm chỉ đổi việc đọc Parquet thành `use_threads=False`; toàn bộ assertion về giá trị, dtype logic, thứ tự/index, input không đổi, partition, SLO, số đếm, support/confidence/ji, lọc finite, output/ERROR và hooks vẫn còn. Sáu fixture cũ còn nguyên nhánh kiểm; thêm mười trường hợp serializer và một fixture adapter có extension dtype. Lịch sử storage backend string chưa được ghi, giữ OPEN.
- `scripts/audit_tracerca_posthoc_v1.py`: giữ nguyên byte draft. Đọc toàn output ERROR đã lưu từ inventory đóng 21 tệp; bind cả check FAIL, invocation, source/audit/import, job, record, capture-start/capture/Parquet. So bản ghi exact với nguồn; kiểm source hiện hành và nguồn hàm đã capture; gọi verifier v3 để kiểm trung gian. Không gọi native/adapter/SLO. Tạo verdict mới riêng; check FAIL cũ vẫn FAIL.
- `scripts/run_tracerca_path_pilots_v2.py`: file mới. Posthoc ERROR → fixture cũ/typed/adapter → RE2 OK dev-12a1a88069 → Nezha OK dev-14701a3bbb, mỗi lúc một child. Audit và fixture chia sẻ 300 giây/50 MiB; đạt cả hai mới sang hai pilot 1200 giây/150 MiB, mỗi pilot tối đa 600 giây. Tổng 1500 giây/200 MiB. Có stdout/stderr, PID, command, progress, chi phí từng child, status và fail-stop. Không cohort/retry/skip. Delta byte tính cả monitor/tạm trong T-032; polling có thể vượt trước khi bị dừng, không là quota cứng.
- Receipt mới `static-full-check-002.json` thay cho việc dùng receipt v3 ban đầu đã cũ; không sửa hay xóa receipt cũ. Hai patch diff mới lưu cùng thư mục. `static_check_002.py` chỉ parse/compile AST và hash/pin, không import code phương pháp hay package khoa học.

## Kiểm đã làm

Đã đọc toàn verifier v3 và audit v1; so với v2 và source helper. Static parse/compile và pin PASS. AST `one`, source/import/path closure không đổi. AST `verify_tracerca` chỉ có thêm `use_threads=False` ở lần đọc storage. Helper AST nguyên bản; nguồn/helper có pin. Hai pilot và hash frozen là đúng hai pilot còn thiếu của controller v1. Capture và shared replay gốc còn đúng hash. Inventory ERROR đóng đúng pin. Controller có toàn bộ kiểm exact, nguồn/capture/import/invariant của v1, cùng gate đủ typed fixture và posthoc. Không có runtime PASS, không có trung gian đủ điều kiện mới.

## Để root ghi LOG và làm tiếp

Lỗi cần ghi LOG: receipt v3 được tạo trước khi khởi tạo cache `_table_content` standalone bổ sung vào draft, nên hash receipt đó không còn là pin cuối. Bằng chứng là `v3-ast-receipt.json` khác byte v3 hiện tại. Cách xử lý: giữ cả receipt lịch sử; tạo receipt mới `static-full-check-002.json` từ byte hiện tại, kiểm helper AST và diff đầy đủ. Không chạy lại phép nghiên cứu và không sửa phương pháp/tiêu chí.

Root đọc cả ba script và receipt mới, xác minh hash/bytes. Chuyển đúng ba script vào `~/rca/T-032/scripts/`, chỉ nếu chưa có cùng tên trên EC2; nếu đã có khác hash thì giữ bản đã có và dùng tên/version mới theo Q-108. Inventory ERROR nguồn đã có tại `~/rca/T-032/runs/tracerca-dtype-source-inventory-001.json`, pin ghi trong receipt. Không cần chép dữ liệu hay native source mới.

Root kiểm lại EC2 không có job nặng khác, RAM/đĩa và tổng dung lượng local+remote+tạm/lượt hỏng. Chỉ launch khi reserve laptop được đo và không vượt 2 GiB, combined cộng 200 MiB không vượt 12 GiB. Generic supervisor/launcher cũ khóa 8 GiB phải được soát và tạo phiên bản mới dùng trần hiện hành, hoặc trần cũ phải còn đủ cho lượt; không giảm kiểm RAM/đĩa/timeout. Bản controller này chưa có startup shell và không tự launch.

Lệnh child/controller chuẩn bị, chưa chạy:

```text
/home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8 /home/ubuntu/rca/T-032/scripts/run_tracerca_path_pilots_v2.py --out /home/ubuntu/rca/T-032/runs/tracerca-path-pilots-002 --baseline-task-bytes <remote-bytes-just-measured> --laptop-reserve-bytes <local-bytes-plus-reserved-growth-within-2GiB>
```

Launcher phải dùng nohup/tmux, interpreter nguồn, PYTHONPATH đã kiểm, hashseed 0 và ghi PID/stdout/stderr/progress. Sau PASS hoặc FAIL, đóng stream/không còn child rồi chốt full inventory/hash hai đầu. Soát mốc đủ fixture+posthoc và pilot đầu trước báo ổn định. Chưa duyệt cohort trong đề xuất này; hai pilot đạt mới báo benchmark và dự toán cohort cho root trình Minh. Lỗi ở bất kỳ bước nào dừng phần phụ thuộc, giữ mọi lượt; không tự bỏ assertion vì nhật ký/serializer khó khớp. Cùng chỗ hỏng ba lần dừng trình theo AGENTS §5a.

## Bốn mục bàn giao

1. Đã soát và chuẩn bị công cụ; chưa giải quyết cơ chế TraceRCA bằng kết quả mới.
2. Phiên tiếp này tạo controller v2 và receipt/diff/notes mới; không sửa v3/audit v1, nguồn, SPEC, LOG/STATE/DECISIONS/WHY hoặc file phương pháp chung.
3. Kiểm AST/diff/pin metadata PASS; không runtime, native hay fixture trên laptop/EC2.
4. Còn thiếu audit/fixture/hai pilot và benchmark/hash đóng để dùng trung gian; câu cơ chế caller/root của TraceRCA vẫn chưa được trả lời từ lượt này. Root cần soát và vận hành; không cần xin Minh duyệt công cụ lại trong Q-108 nếu giữ đúng phạm vi/tiêu chí.

Lệnh cuối: `py -3 -B -X utf8 results/T-032/runs/tracerca-dtype-repair-001/static_check_002.py` (chỉ metadata).
