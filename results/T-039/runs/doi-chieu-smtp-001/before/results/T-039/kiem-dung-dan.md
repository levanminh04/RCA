# Tự kiểm T-039

Lượt chuẩn: `runs/thuc-thi-snapshot-004/verification.json` — PASS. Dùng nguyên snapshot T036 đã ghim; các module thực nạp đều từ thư mục snapshot. Không dùng live `src` có SMTP, không đổi pin/spec hay mã task khác. Quyền ngoại lệ nằm trong LOG Phiên4.

- Oracle literal đã có trước code biến đổi: `fixtures/oracle.json`, bản trước transform tại `runs/trien-khai-001/oracle-before-transform.json`. Kiểm giao/phần riêng hai phía, typed unknown, mẫu số0→null, mapping chưa verified, owner conflict và projection/entity-only. Kết quả thật: `runs/thuc-thi-snapshot-004/oracle-result.json`.
- Đủ 132 graph theo canonical allowlist T035 và hash manifest, không lấy runs lịch sử hay dựng cửa sổ mới. API chỉ nhận graph/bản ghi/mapping/context; tên ca, root, loại lỗi, đường dẫn điều phối và mốc tiêm không là input phương pháp.
- Tính lại độc lập từng khóa từ cạnh đầu vào, giao/phần riêng, mẫu số/tỷ lệ; kiểm members trỏ đúng original, eligible/excluded phân hoạch đủ và không trùng. Bảo toàn interval, conditional_reference và miền dev-adapter trên tất cả graph.
- Build sau đảo thứ tự bản ghi cho đầu ra bằng nhau; compare sau đảo mapping cho đầu ra bằng nhau; deep-copy đối chiếu xác nhận không đổi đầu vào. Kiểm chiếu là tập con graph entity và báo entity-only trong `projection-check.json`. Phép so endpoints không xác minh HTTP/RPC; typed không được lấp unknown bằng kiến trúc.
- Mỗi nguồn registry được hash lại; graph input được kiểm theo manifest T035, snapshot4file theo code-hashes/T036. Kiểm JSON/provenance/phạm vi/prompt/manifest cuối ở `runs/ket-thuc-001/verification.json`.

Số lần và chi phí: acquisition và các run chuẩn bị giữ nguyên; execution001 bị root ngắt ở quan sát hash task khác trước oracle; execution002 oracle/build đạt nhưng compare entity nhận nhầm mapping operation nên bị từ chối `mapping_target`; execution003 đạt toàn bộ; execution004 sửa hợp binding/candidate provenance và đo lại. Không sửa hợp đồng chung để bỏ lỗi. Những thay đổi này chỉ ở orchestration T039.

Runner đầu ghi output canonical chưa lưu bản riêng theo attempt. Inputs/failures vẫn có; 135 comparison lịch sử được tái dựng và **ghi rõ RECONSTRUCTED_NOT_ORIGINAL_BYTES** tại `runs/khoi-phuc-lich-su-001/receipt.json`, không giả là byte original. Lượt004 có archive byte đầu ra thật trong `runs/thuc-thi-snapshot-004/outputs/`; runner hiện lưu cả per-run outputs cho các lượt sau.

Lượt004 elapsed 3.669s, peak working set tiến trình 71,557,120 byte; input graph 3,856,723 byte. Đây là quan sát chi phí tiến trình, không benchmark máy cô lập hoặc giờ công toàn task (`cost.json`). Trước lượt này có quan sát CPU workload ngắn, không dừng tiến trình khác (`runs/quan-sat-chi-phi-001/workloads.json`). Pilot/giờ từng graph có trong run và tổng hợp; không ngoại suy hoặc đề xuất EC2. Peak lượt003 không đo được do kiểu handle Windows; không thay null bằng0. Tổng byte thực lưu cuối, gồm failed/replayed/history, nằm ở manifest. Giờ công toàn task không đo liên tục, vẫn OPEN; không dùng thời gian compute để xác nhận dự toán công.

Không có số công bố tương ứng với bộ biến đổi bản ghi; oracle/nguồn/trung gian là căn cứ kiểm. Các kiểm này chứng minh hành vi triển khai trong miền giao, chưa chứng minh ứng dụng đã triển khai, telemetry đầy đủ hoặc lợi ích RCA.
