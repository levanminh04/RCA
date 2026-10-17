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
