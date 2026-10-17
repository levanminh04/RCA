# Kiểm tiền kiểm T-039

Không có công cụ chuyển đổi riêng hoặc thực nghiệm ứng dụng trong lượt này, nên chưa có oracle chuyển đổi/đối chiếu T-039 để nghiệm thu. Oracle độc lập phải được viết trước khi triển khai phần đó. Không lấy test T-036 hoặc một phép đọc manifest làm bằng chứng đã thực hiện toàn SPEC T-039.

| Kiểm đã thực hiện | Bằng chứng |
|---|---|
| Pin created_utc/current_run, toàn artifact T-036 | `runs/tien-kiem-001/input-verification.json#/pin_ok`, `#/t036` |
| Code hiện hành = snapshot = code-hashes | Cùng file, `#/code_snapshot` |
| Nguồn T-008 khớp manifest cuối T-003 trước dùng | Cùng file, `#/t008_final_manifest` |
| Git blob của nguồn nguyên bản khớp cây đã lưu | Cùng file, `#/t008_git_blobs` |
| Graph/tài liệu T-035 được giao khớp manifest | Cùng file, `#/t035_graph_hashes`, `#/t035_documents` |
| Tập path graph đúng canonical, không gom lịch sử | `runs/tien-kiem-001/graph-inventory.json#/canonical_paths_match` |
| Loại object Nezha và cùng thành viên cây | `runs/tien-kiem-001/kiem-loai-object.json` — kiểm metadata, không phải xác nhận deployment |
| Tổng danh sách/byte và phần loại trừ | `de-xuat-tai.json`, assertions trong finalize_preflight.py |
| Không sửa nguồn/pin/SPEC, LOG nối, STATE đúng một dòng, prompt nguyên văn | `runs/tien-kiem-001/final-verification.json`, `changes.diff` và manifest |

Lệnh đã chạy: `py -3 -X utf8 -B results/T-039/preflight.py tien-kiem-001`. Lượt được giữ nguyên, không ghi đè tên run. Lệnh bàn giao: `py -3 -X utf8 -B results/T-039/finalize_preflight.py prepare`; lệnh kiểm cuối: cùng script với `verify`. Script thứ hai chỉ ghi trong results/T-039 và nối LOG ở chế độ prepare; không cấp quyền thực hiện đề xuất.

Chưa đo pilot RAM/chi phí đối chiếu, chưa khảo sát nội dung source mới, chưa dựng/mapping/compare/project cho ứng dụng, chưa phân tích mismatch/match. Phần này bị chặn bởi quyết định phạm vi/nguồn; không tự bỏ nghĩa vụ.


## Kiểm sau thu theo Minh duyệt — 16/10/2026

`runs/thu-nguon-001/acquisition.json`: 223 file nguồn, sáu metadata; 37.524.834 byte payload thực; tất cả Git blob/byte khớp, không có lỗi. `runs/khao-sat-nguon-001/integrity.json`: 229/229 SHA256/byte khớp sau thu. Declaration count và JAR metadata được kiểm độc lập để xét khối lượng; không là semantic inventory hoặc runtime evidence. Không có graph/mapping T-039 đã dựng.

Đã đối chiếu các ví dụ nguồn chính về biến thể deployment, dependency MySQL/Redis có điều kiện, generated khác proto/registration và NodeName chưa nối Node dataset. Các số và locator ở bao-cao-sau-tai.md, không nhận phát biểu của nhánh hỗ trợ là quyết định hoặc bằng chứng coverage toàn snapshot.

Kiểm cuối checkpoint: `py -3 -X utf8 -B results/T-039/finalize_after_acquisition.py verify`. Kiểm nguồn đã thu, proposal đã duyệt, pin/SPEC/nguồn bảo vệ, LOG append-only, STATE chỉ dòng task, prompt nguyên văn và manifest toàn file. Kết quả ở runs/ket-sau-tai-001/final-verification.json. Không chạy lại script preflight cũ sau thu vì điều kiện no-sources của nó là mốc trước cấp quyền tải.
