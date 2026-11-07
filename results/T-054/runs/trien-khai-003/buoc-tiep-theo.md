# Tiếp tục T-054 từ checkpoint003

Codex vẫn là người làm, Claude phản biện. Chưa xong pha1 và chưa được chạy chính. Không chạy lại các script sửa/tiếp nhận pilot001–008: chúng đã được thực hiện, giữ lịch sử create-only. Tất cả worker hiện đã dừng.

1. Đọc AGENTS, STATE, SPEC, LOG mục cuối và reports/tu-soat-003/bao-cao.md. Chạy `kiem_checkpoint.py --manifest results/T-054/manifest-trien-khai-003.json` trong thư mục repo bằng Python main đã ghim. Đây là kiểm chỉ đọc. Không dùng validator001/002 để ép hiện trạng về trước.
2. Đọc thoi-gian-va-kich-ban.json, các parity cuối và numeric-parity-analysis.json. Kịch bản lạnh 25–27 giờ không là ETA. Đừng lấy chữ VERIFIED thay OK hoặc lấy bảng dev một ca/dataset làm A4 test 60/34.
3. Đọc code `CacheCong` và đường source→adapter→chuoi hiện hành trước khi cài cache. SPEC đã giao bundle/cache và phép đo worker; chưa hoàn thành các phần ấy. Giữ toàn bộ đầu ra lạnh làm đối chiếu. Không mở lại thiết kế M1 hoặc baseline A/B.

## Gói công cụ tiếp theo trong phạm vi SPEC

| File được SPEC cấp | Mục đích thay đổi cần triển khai | Phân xử bắt buộc |
|---|---|---|
| scripts/worker.py | Dùng lại dữ liệu đã đọc/cắt và E4 cache giữa các vế cùng ca/cửa sổ; prep TORAI chỉ chia sẻ khi đủ khóa nguồn/cửa sổ/code/env và độc lập seed | Normalized input, cờ/tầng/hòa/hạng/vùng/controls khớp tham chiếu; key sai không được hit; cache không đưa locator/nhãn vào API. Không mặc định pickle/JSON là tương đương số. |
| scripts/dieu_phoi.py | Scheduler số worker được khai trong plan bất biến; tài nguyên/cost/timeout/ownership/resume vẫn đúng từng slot và toàn lô | Không chạy đôi; controller chết giữa bundle không mất output hoặc tự chấm file dở; budget nhóm/toàn lô không reset; DRAIN không phát thêm. |
| scripts/p7.py | Đọc cấu hình worker/bundle từ plan đã pin, phản ánh trạng thái/tiến độ rõ | Không sửa số worker bằng CLI ngoài bản khóa; chưa quyền vẫn WAIT. |
| scripts/bien_nhan.py, nguon.py nếu cần | Liên kết cache producer/input/code/env với lần dùng lại, không tự gán provenance | Tráo/rehash hoặc thay input/window/config/code/env phải bị bác trước chấm; chứng cứ phải đọc từ producer thật. |
| scripts/fixtures.py | Mẫu dương/âm chạm đúng đường cache và nhiều worker | Không chỉ mirror hàm hoặc mock tất cả core; giữ các lượt lỗi và phép kiểm đã có. |
| scripts/pilot.py, lap_ho_so.py | Khai cold/warm, thực đo throughput1→2/3, cập nhật nguồn/hồ sơ theo quyết định | Không chia thời gian cho số worker hoặc tự tạo ETA/cap. Giữ raw số đo, thẩm quyền và mọi giới hạn. |

Không sửa src trong gói trên. Nếu cần đổi hợp đồng lõi, trình đúng patch/phạm vi/chi phí cho Minh, dừng riêng nhánh ấy. Đây là bước còn thiếu đã nêu, chưa được gọi là hoàn tất chỉ vì có bảng đề xuất này. Lợi ích cache/parallel chưa kiểm; có thể không giúp khi I/O, RAM, cache key hoặc mức dùng chung hạn chế. Không giảm ca/seed/vế để vừa phiên.

## Bằng chứng thực nghiệm còn phải bổ sung

- C-e dev theo SPEC §7: chứng nhận hỗ trợ lịch sử/A0 và nguồn t; không suy `ce_history=verified` từ một bản đồ tự khai. Các runtime pilot hiện giữ unknown và không phát C-e. Đọc hợp đồng C_e của T052 và code trung gian hiện có trước đề xuất nguồn/chạy.
- Chỉ thêm đúng ca/vế còn thiếu cho nhóm giúp/hại/không đổi, dựa vào native/trung gian cũ đã pin; không chạy lại cả 52 dev × toàn ma trận. Các ca pilot đã dùng có grant dev; A chỉ đúng ca a5cabe5fa7.
- Đo local cùng lô ở 1 rồi 2/3 worker khi scheduler đã kiểm. Giữ cold/warm/tải cạnh tranh/RSS/đĩa/thời gian nhận/chấm. Nếu một lô dự kiến hơn 1 giờ, trình cap cụ thể theo AGENTS trước chạy; không tự dùng đề xuất 3 giờ cũ.
- Chốt vấn đề số học/luồng với Minh trước G3: MicroRank 1→16 chẩn đoán đã có, source thread lịch sử cònOPEN; M1/T12 OB thứ hai lệch số cuối so nguồn EC2. Chưa có dung sai hoặc ngoại lệ main được duyệt. Không sửa số/khóa để khớp.
- Hoàn thiện đường phân loại ERROR/TIMEOUT main có nguồn/pha/monitor, không mượn receipt dev. Chính sách cạn trần và hai công thức độ nhạy ở SPEC vẫn cần Minh quyết; cho tăng thời gian không thay các quyết định ấy.
- Hoàn thiện H1/H2 hợp đồng RE3 theo hop-dong-re3.json. Chưa có schema local; cần nguồn/schema/footer và phạm vi lấy phù hợp. Tải toàn bộ 138.129.790 byte hoặc sửa src cần trình đúng quyền, không suy từ metadata. RE3 chỉ đánh giá riêng một lần cho bản cuối, không pilot/tune.

## Dựng lại trên máy khác

Data và private runtime/label/A-source không vào gói code. Nguồn gốc/recipe đã có trong chuan_bi_pilot.py, original_dev_sources/original_dev_labels và các ref metadata của mỗi gói. Thiếu private refs thì dựng lại từ đúng G1/allowlist/command đã pin trong vùng private được phép, kiểm hash và ghi lineage mới trước dùng; không tự chép từ repo RCA lưu trữ hoặc mở test. Môi trường thực của từng gói ở metadata/environments; code-version-lineage và các code-pilot-* giữ byte đúng từng job. Không gọi code hiện tại là byte đã tạo mọi kết quả lịch sử.

Trước chạy chính phải báo Minh: bằng chứng đủ tới đâu, các điểm còn chặn, code/env/config/matrix/scoring đã khóa hay chưa, cap/ETA có căn cứ, nguồn/grant đúng phạm vi và các lựa chọn cần chốt. Hiện chưa đủ để xin G3 hoặc phát main. Không commit/push hoặc tự gửi prompt.
