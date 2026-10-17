# Lệnh và lượt tiền kiểm, 15–16/10/2026

Môi trường Python/thiết bị nằm ở environment.json; quan sát dung lượng/RAM và lệnh tương ứng ở capacity-observation.json. Không cài gói, không sinh bytecode. Một subagent hỗ trợ chỉ đọc kiểm pin/inventory; không là phản biện chính thức và không ghi file.

## Lượt đọc/kiểm không tạo run ứng dụng

- Get-Content -Raw/-Tail/-Skip/Select-Object: yêu cầu đính kèm, AGENTS, STATE, SPEC/LOG T-039, DT18/cô, mẫu SPEC, MRP/LESSONS/WHY/DECISIONS/review-prompt và LOG T-036 phương án gốc. Sau khi ghi nhận xét độc lập mới đọc REVIEW và mốc đóng T-036. Không đọc kết luận phản biện T-039 cũ.
- git status --short; git diff --numstat; rg --files/rg -n trên nguồn tài liệu/code được giao. Không mở data/locked hoặc archive.
- Python inline -X utf8 -B đọc manifest bằng JSON, kiểm SHA256/byte/Git blob trước dùng nguồn; không nhập hoặc chạy code Nezha. Toàn phép kiểm chính được đóng gói lại ở preflight.py và kết quả ở input-verification.json.
- Get-Content/rg trên README, registry/hợp đồng/bàn giao T-036, API build/compare và data_integrate.py đã xác minh. Chỉ đọc code thu/analysis; không chạy đọc dữ liệu của chúng.
- Get-PSDrive và Get-CimInstance chỉ đọc capacity; không đo hiệu năng hoặc dừng tiến trình khác.

## Metadata công khai chỉ đọc trong bộ nhớ

Python urllib.request với User-Agent RCA-T039-readonly-metadata, Accept application/vnd.github+json, Accept-Encoding identity, timeout 30 giây; json.loads response trong bộ nhớ, in bản tóm tắt. Không lưu raw response hoặc code nguồn mới xuống đĩa.

1. GET repository Augmented-OnlineBoutique: 7.240 byte body.
2. GET commits?per_page=2: 3.076 byte; trả một root commit.
3. GET git/trees/{tree ở commit}?recursive=1: 71.984 byte; tree không truncated. Lập toàn danh sách đề xuất theo path/type/blob/size, phân nhóm và actions. Đây chưa là coverage nội dung.
4. GET Nezha git/ref/heads/main: 338 byte. GET URL git/commits của object trả về: 2.593 byte. Không dùng ref để đổi pin.
5. Kiểm lại GET git/commits/{revision đã lưu}: 2.593 byte; GET tree canonical recursive: 336.966 byte. So toàn tuple path/mode/type/blob/size với tree đã lưu: bằng nhau. Bản tóm tắt/URL/hashes ở kiem-loai-object.json.

Tổng body metadata của các request urllib thành công trên là 424.790 byte, không bao gồm wire overhead. Đã dùng web.open xem trang repository để đối chiếu metadata; dung lượng web không được tool báo. Không tính các truy vấn này là source snapshot/code đã tải hoặc là bằng chứng ứng dụng sinh dataset. Không lưu response web mới thành source.

## Lượt lỗi/đọc lại được giữ

- rg --files với đối số tasks/T-036* báo Windows invalid filename, exit code 1. Sau đó dùng đúng literal path/thư mục; không có file thay đổi hoặc thí nghiệm mất.
- Các lệnh in toàn manifest lớn bị tool cắt output. Sau đó dùng json.loads lọc đúng entries và kiểm hash trên byte thật; không dùng phần output bị cắt để tính số. Không có thay đổi input hoặc sửa hash.
- web.open Git trees API báo không truy cập được; web.open commit Nezha báo timeout. Dùng urllib read-only metadata ở đúng endpoint, HTTP 200; không chuyển nguồn/upstream hoặc tải code.
- Không có lượt chạy ứng dụng hoặc benchmark thất bại; chưa chạy chúng. Tiền kiểm có một run tien-kiem-001 thành công. Không xóa/ghi đè run lỗi, graph, baseline hoặc task khác.
- Lần đầu cập nhật STATE dừng trước ghi: regex có `$` với CRLF không khớp cuối dòng, báo `T-039 row count mismatch`; bản backup trước ghi chưa được tạo và STATE không đổi. Đọc lại dòng bằng rg xác nhận tồn tại, bỏ anchor cuối không phù hợp CRLF rồi thử lại; vẫn yêu cầu đúng một dòng và giữ khóa file độc quyền.

## Các lệnh ghi trong quyền

1. Nối LOG mở Phiên 2, nguyên văn lời giao và quyền.
2. Tạo các báo cáo/script/JSON bên trong results/T-039 bằng apply_patch; không tạo sources/.
3. py -3 -X utf8 -B results/T-039/preflight.py tien-kiem-001.
4. py -3 -X utf8 -B results/T-039/finalize_preflight.py prepare.
5. Cập nhật STATE bằng khóa file độc quyền, đọc bản mới nhất, lưu bản ngay trước ghi trong run và chỉ thay dòng T-039; không sửa phần chung hoặc dòng task khác.
6. py -3 -X utf8 -B results/T-039/finalize_preflight.py verify. Đây là lệnh cuối dự kiến trước báo cáo; đầu ra kiểm nằm ở final-verification.json và manifest, không chạy source acquisition.
