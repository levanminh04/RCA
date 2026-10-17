# TraceRCA: 49 ca còn thiếu — CHỜ MINH DUYỆT

Codex người làm, Claude người phản biện. Chưa chạy cohort. Q-101/Q-121 chỉ cho các phép sửa, fixture, audit và hai pilot đã hoàn tất; không coi chúng là lời duyệt lượt mới.

## Nguồn và phần không chạy lại

`runs/tracerca-cohort-proposal-001/plan-52.json#/rows` khóa đủ 30 RE2-TT và 22 Nezha-OB từ index T-024/T-026. Index kiểm theo manifest nguồn T-029/T-026, hash từng record đã khớp. RE2 có 26 OK, 4 ERROR; Nezha có 22 OK. Giữ main/native/mode a/hashseed0/cửa sổ F, không đổi ca/cấu hình/nguồn/adapter/phương pháp/threshold.

Ba ca đã hợp lệ được dùng lại sau kiểm hash, không chạy native lại: RE2 `dev-03d4910932` (audit ERROR đã lưu), RE2 `dev-12a1a88069`, Nezha `dev-14701a3bbb`. `runs/tracerca-pilots-root-001/check.json` và `runs/tracerca-pilots-transfer-001/check.json` xác nhận đóng/hash hai đầu, trạng thái và record exact; lượt FAIL cũ giữ nguyên. Bản kế hoạch vừa kiểm lại 198 file theo closed inventory. Còn **28 RE2 và 21 Nezha**, gồm ba ERROR RE2 phải tái hiện đúng nhánh nguồn, không loại khỏi bảng.

## Benchmark và ngoại suy — chưa kiểm cohort

Số đo ở `runs/tracerca-path-pilots-002/status.json#/completed` và record/cost từng pilot:

| Pilot | Span | Operation | Trọn child | Worker gồm capture | Peak worker | Artifact child |
|---|---:|---:|---:|---:|---:|---:|
| RE2 | 443.868 | 152 | 279,160 s | 173,682 s | 1.907,102 MiB | 40.874.683 B |
| Nezha | 67.913 | 55 | 59,306 s | 32,669 s | 742,184 MiB | 9.974.605 B |

Peak cây tiến trình lượt pilot/fixture tổng: 2.265.968.640 B, `runs/tracerca-dtype-pilots-002-monitor/status.json#/peak_tree_rss_bytes`. Đây là lấy mẫu, không bảo đảm cận trên. Metadata nguồn: RE2 51.863–644.791 span, 74–152 operation ở ca OK; Nezha 39.150–73.945 span, 44–55 operation, có route nguồn full và reused pilot. Ca lớn hơn pilot vẫn được giữ. ERROR không có operation count; chưa giả điền từ ca OK.

`forecast.json` trong thư mục kế hoạch ghi công thức theo từng ca: chi phí pilot nhân `max(1, span_ratio × max(1, operation_ratio))`, cộng **50% dự phòng**. Dung lượng theo span ratio và 50% dự phòng. ERROR dùng dự toán route OK một cách bảo thủ và giữ thiếu operation count OPEN. Đây là quy ước dự toán, **chưa kiểm**, không phải mô hình độ phức tạp đã xác nhận hay ngưỡng khoa học. Có thể sai nếu số trace/tập co-occurrence, dtype, route ERROR hoặc chi phí giải mã khác mạnh; guard phải dừng nếu sai.

Ngoại suy: RE2 12.148,706 s và 1.778.818.530 B; Nezha 1.927,823 s và 324.238.269 B; tổng **3 giờ 54 phút 37 giây**, **2.103.056.799 B** mới trước phần controller/receipt/temporary thêm. Đề nghị trần lượt cohort **4,5 giờ máy/2,5 GiB mới** trên EC2, mỗi ca **10 phút/150 MiB** gồm replay, kiểm và đóng; mọi artifact/tạm/lượt hỏng tính trần. Trần toàn T-032 **12 GiB**, laptop **4 GiB** theo Q-124 giữ nguyên. Đo inventory/RAM/đĩa ngay trước lượt; không lấy snapshot cũ làm quyền mở trần. Nếu chi phí cộng dồn của task vượt dự toán SPEC, dừng trình riêng, không dùng trần lượt này để tự mở rộng giờ toàn task.

## Cách thực hiện đề nghị

1. Tạo controller/launcher/root verifier bản mới trong bảng dưới; pin nguyên `replay_tracerca_v3.py`, capture, shared code, adapter và RCAEval lowercase closure revision259ea41 đã duyệt Q-98. Kiểm tĩnh/diff/source/fail-stop; không lặp bộ fixture đã valid nếu pin không đổi. Nếu phải sửa verifier, theo Q-108, giữ mọi bản/lượt hỏng; không đổi tiêu chí và không bỏ phép kiểm.
2. Bảng đủ52 ngay từ đầu, source pointers/status/score/order/tie/capture/exact và lý do N/A/not_run. Nhập ba ca cũ bằng hash đóng, không sửa eligibility của lượt FAIL. Một worker EC2, thứ tự dataset rồi opaque_id cho phần thiếu. Native quan sát tối đa một lần mỗi ca bằng wrapper đã qua fixture/pilot, so tuyệt đối frozen và kiểm đầy đủ trung gian/formula/source/import/hook; nhãn chỉ nối sau phương pháp. ERROR nguồn exact có hàng non-OK hợp lệ, không dùng điểm/trung gian không tồn tại để nhận cơ chế OK.
3. Checkpoint sau ca mới đầu và sau route chưa được xác minh nếu xuất hiện; đo tốc độ/RAM/bytes và kiểm source/manifest/record trước tiếp. Không retry, skip, tăng tolerance, giả status hay tiếp qua lỗi. Lỗi/vượt tự dừng toàn TraceRCA, ghi status/progress/streams/PID/full command và manifest sau đóng streams. Dừng an toàn giữa các ca đã đóng có thể tiếp phần chưa chạy sau kiểm thật; không chạy lại ca hợp lệ.
4. Guard EC2 theo tài nguyên đo thực; ứng viên RSS tối đa6GiB với phần RAM dự phòng ít nhất1GiB, chưa là bảo đảm. Chỉ chạy khi đủ tài nguyên; vượt guard dừng trình, không tự tăng. Đĩa dự phòng phải đủ trần lượt. Không chạy việc nặng EC2 khác cùng lúc. Nếu MicroRank laptop đang ở segment có remote budget snapshot cố định, chờ segment dừng ở checkpoint trước tạo output EC2 này.
5. Lưu capture nặng trên EC2; thu manifest, bảng/check/root receipts và phần đọc tay cần thiết về laptop trong tối đa50MiB ban đầu, hash hai đầu. Không thu toàn2,1GB cùng MicroRank để vượt local4GiB; không xóa/move bản cũ. Thu thêm phải đo lại và nằm SPEC/ngân sách. Lượt chuyển nào chưa có tốc độ đo phải đo một phần nhỏ trước và ghi dự toán.

## File mới và ảnh hưởng

Trong `results/T-032/` và bản tương ứng `~/rca/T-032/`:

- `scripts/run_tracerca_cohort_v1.py`: một worker, reuse ba ca đóng, exact/source/capture/hash fail-stop, bảng52 và checkpoint.
- `scripts/start_tracerca_cohort_001.py`: supervisor nền độc lập SSH/laptop, resource/time/bytes watchdog, streams/PID/status/command/manifest sau đóng.
- `scripts/verify_tracerca_cohort_001.py`: root kiểm các closed manifest/source pins/bảng52/verdict, không gọi lại native.
- `runs/tracerca-cohort-001/`: plan/source/benchmark/forecast, `cases/`, bảng52, progress/status/streams/PIDs/terminal/manifests; giữ mọi partial/error.
- `runs/tracerca-cohort-root-001/`, `runs/tracerca-cohort-transfer-001/`: root/transfer/source/hash receipts, không sửa artifact cũ.

LOG chỉ nối sau từng bước; STATE chỉ dòngT-032 freshread. Không sửa SPEC/WHY-42/code dùng chung/môi trường/dữ liệu, không test/locked/T-033/commit/push. Đề xuất không tạo một phép kiểm khoa học mới; giữ các phép hiện có của SPEC và Q-98/Q-101. Full cohort exact là điều kiện dùng trung gian, chưa trả lời cơ chế caller/root, chờ vật lý, hay nghiệm thu G2; đọc tay/đối chứng/T-028/bảng cơ chế vẫn làm sau đó.

## Dòng DECISIONS dự thảo

Q-125 đang trống khi soạn; freshread trước nối, đã dùng thì trình mã khác. Chỉ nối sau Minh duyệt:

| Q-125 | 10/10/2026 | Minh duyệt đúng results/T-032/de-xuat-tracerca-cohort-001.md: dùng lại ba ca TraceRCA đã đóng/hash/exact, phát lại 49 ca dev còn thiếu (28RE2+21Nezha) bằng v3/capture/native/adapter/closure nguyên pin, đủ52source/main/F/a/h0/status và exact mọi record/order/tie/capture/formula/source/import/hook, giữ non-OK/N/A; một worker EC2 3.26.62.217 nền độc lập SSH/laptop, checkpoint ca đầu/route mới, fail-stop mọi lỗi/vượt, khôngretry/skip/tolerance; trần lượt4,5giờ/2,5GiB mới, mỗi ca10phút/150MiB, tổngT03212GiB/local4GiB giữ, đo tài nguyên/cộng dồnSPEC trước lượt; tạo đúng công cụ/run/receipt mới đề xuất, giữ mọi bản/lượt cũ, khôngSPEC/WHY42/shared/environment/test/locked/T033/commitpush, capture nặng giữEC2/transfer ban đầu≤50MiB/hashhaiđầu; không chen EC2 output vào segmentMicroLaptop dùngsnapshot cốđịnh; cho nối đúng dòng này sau freshreadDECISIONS. | Lời duyệt Minh; results/T-032/de-xuat-tracerca-cohort-001.md |
