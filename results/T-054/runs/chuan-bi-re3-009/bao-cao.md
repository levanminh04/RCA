# Chuẩn bị RE3 — checkpoint009

## Vì sao còn thiếu

Codex đã chuyển từ schema RE3 sang bản vá OB và kiểm kê hệ quả AWS, rồi kết thúc checkpoint008 khi H1/H2 còn mở. Đây là phần người làm chưa hoàn tất trong gói bước1–4 đã duyệt. AWS chỉ làm dừng SSH/sync/cloud; không chặn công việc metadata và adapter ở local. Không có căn cứ nói chỉ cần khôi phục cloud là có thể chạy chính.

Checkpoint này tiếp tục quyền đã có. Không mở dữ liệu đo RE3, không chạy phương pháp trên RE3, không đổi trạng thái G3 và không sửa lõi. RE3 vẫn dành cho bản cuối, mở riêng một lần. Trạng thái hiện tại: **H1 đã có phân tích cụ thể hơn; H1 chưa đủ nguồn để khóa; H2 chưa cài**.

## Đã thực hiện thêm

- Kiểm hash toàn bộ 590 output008 trước dùng; kiểm đúng output schema007 theo manifest007. Giữ nguyên các checkpoint cũ. Không lấy lại 90 footer.
- Phân tích đủ 30 schema metric thành 5 nhóm; lưu tên cột, tập owner và nguồn từng nhóm trong `inventory-schema.json`.
- Tách khai báo của nguồn, suy luận và phần chưa biết về thời gian/quan sát trong `time-and-observation-contract.json`.
- Lần code cho M1, sáu baseline và hai nguồn TORAI; lưu 8 dòng hỗ trợ trong `method-support.json`. Đây là khả năng theo schema/code, chưa phải kết quả hỗ trợ trên ca thật.
- Chạy 27 kiểm tổng hợp bằng helper hiện hành và prototype quy đổi đơn vị khai tường minh. Kết quả ở `synthetic-checks.json#/checks`; chưa thay kiểm adapter RE3 đầy đủ sau cài.

## Inventory: điều schema thật sự cho biết

`inventory-schema.json` cho thấy 12 tiền tố owner chung và 28 tiền tố trong hợp các schema. Hai ca có thêm tên thuộc namespace thường gặp ở Sock Shop. Không đọc giá trị nên chưa biết các cột thêm có toàn null, hằng, có tín hiệu thật hay xuất phát từ đâu. Không gọi đây là nhiễm dữ liệu đã xác nhận.

Không được lấy 4 service gốc của nhãn làm U. Cũng chưa được lấy hợp 28 tiền tố làm inventory của deployment OB. `frontend-external` và `frontend` hiện giữ riêng: chưa có nguồn nối namespace đã triển khai của RE3. Snapshot T-039 thuộc Nezha-OB; không thể chuyển nó thành inventory RE3 chỉ vì cùng tên benchmark.

Cần nguồn deployment/export RE3 hoặc một lựa chọn U/alias được Minh duyệt với giới hạn khai rõ. Trước đó adapter phải nhận inventory/alias đã ghim, không tự tạo từ root hay âm thầm gộp/bỏ tên lạ. Chưa chọn cách loại các cột thêm.

## Đơn vị thời gian và quan sát

- `metrics.time`: nguồn dataset card đã ghim khai Unix giây; chưa kiểm giá trị RE3.
- `startTime`/`duration`: ứng viên microsecond. Bài RCAEval nói dùng Jaeger; model JSON Jaeger khai hai trường này bằng microsecond. Đây là chuỗi suy luận về exporter, chưa phải chứng minh exporter RCAEval giữ nguyên đơn vị.
- `logs.timestamp`: vẫn thiếu khai báo riêng cho RE3. Adapter RE2-TT dùng giây không xác nhận RE3 cũng vậy.
- `startTimeMillis`: không dùng tên trường để chốt millisecond. Chuỗi `time` của trace chưa rõ format/timezone nên không dùng làm đồng hồ dự phòng.
- Nhịp lấy mẫu và độ phân giải quan sát `r` khác với đơn vị mã hóa. Không tự chép `r` của TT sang RE3. Các trường này ảnh hưởng coverage, thời lượng T, E2 và xử lý cửa sổ.

Nguồn Jaeger đã lưu cùng hash và URL trong `source-pins.json`. Model chuẩn không thay thế tài liệu biến đổi của exporter. Những trường còn thiếu tiếp tục OPEN; không chọn đơn vị bằng độ lớn số hay xem thử telemetry.

## Khả năng hỗ trợ và lỗi adapter đã phân xử

27 kiểm tổng hợp PASS bao gồm kiểm tất cả 5 schema. Bộ lọc `ts-*` hiện hành của TORAI dành cho TT làm mất toàn bộ cột metric OB trong cả 5 schema. Đây là lỗi tuyến tiền xử lý đã tái hiện với giá trị giả, chưa là lỗi phương pháp TORAI hay kết quả đánh giá RE3.

Tất cả suffix metric của 5 schema ánh xạ được sang loại nút CIRCA hiện hành. Điều này không chứng minh graph thực tế đủ cạnh hoặc hồi quy chạy được. Span cha được helper CIRCA ghép theo cả traceID và spanID trong kiểm tổng hợp.

Hai nhận định cần thu hẹp so với checklist cũ003: literal `dataset='re2-tt'` không tự chứng minh sai số BARO/CIRCA vì preprocess đã ghim dùng cùng nhánh tổng quát cho các dataset này; TraceRCA đã ghim không dùng tham số dataset trong phép tính. Vẫn cần định danh RE3 đúng trong binding và giao thức. Không biến việc đổi tên tham số thành bằng chứng đã sửa sai thuật toán.

M4/MicroRank/TraceRCA có trường cần thiết theo schema, nhưng units, dữ liệu bình thường và điều kiện ca thực vẫn chưa kiểm. TORAI A chưa có nguồn bảng tác giả riêng cho RE3 trong hồ sơ đã kiểm; không gọi B dựng lại là A hoặc kết luận phương pháp UNSUPPORTED vì thiếu adapter. `statusCode` có kiểu int không xác định nghĩa mã; không mặc nhiên coi tổng mã là số lỗi.

## Bản vá H2 cụ thể trình duyệt — chưa áp dụng

Mục tiêu: cài và kiểm tuyến RE3 riêng bằng dữ liệu tổng hợp trong khi nguồn đơn vị/inventory còn được hoàn thiện. Bản vá không tự duyệt U/alias/r/đơn vị chưa xác nhận; những trường đó bắt buộc khai tường minh và ghim trước chạy. Thiếu hồ sơ thì BLOCKED trước method. Quyền cài không làm H1 đủ, không mở G3 hoặc RE3.

| File | Thay đổi cụ thể | Vì sao và ảnh hưởng |
|---|---|---|
| `src/p3/re3.py` (mới) | Reader/validator RE3 nhận nguồn đã kiểm và profile thời gian/U/alias/r; chuẩn hóa bằng số nguyên, cắt cửa sổ đúng biên; giữ null, timestamp và ID; xuất provenance/shape; thiếu profile hoặc schema lạ dừng trước method. Không đọc nhãn/inject_time/tên ca trong method. | Tách RE3 khỏi TT và Nezha, không suy clock hoặc ownership. |
| `src/m1/adapter.py` | Thêm profile RE3-OB và `ca_re3`; dùng các bảng đã chuẩn hóa; map đủ 8 suffix bằng bảng khai tường minh; rule log nhận trong profile, không tái dùng parser severity Nezha. Coverage/r phải từ profile đã ghim; không thêm mặc định RE3. | Đưa tín hiệu vào API M1 hiện hành, giữ công thức/nền. |
| `src/p3/adapters/baro.py` | Tham số dataset tùy chọn, mặc định giữ TT; truyền cùng giá trị vào kernel và dựng lại khóa. | Binding RE3 đúng, kiểm mặc định không đổi. |
| `src/p3/adapters/circa.py` | Dataset tùy chọn cho preprocess; giữ mặc định TT, graph normal-only, isolates, actual current, SVR/OLS. | Tách định danh, không chọn lại graph/hồi quy. |
| `src/p3/adapters/tracerca.py` | Dataset tùy chọn xuyên wrapper; mặc định TT; giữ kernel và finite-ji. | Không gắn nhầm tên dataset trong tuyến RE3. |
| `src/p3/adapters/torai.py` | Thêm lựa chọn lọc metric theo profile: default TT giữ `ts-*`, RE3 không lọc TT; tuyến B giữ bin/seed/kernel. Không tạo nguồn A giả. | Sửa lỗi rỗng metric đã tái hiện; thay đổi chỉ opt-in RE3. |
| `results/T-054/scripts/nguon.py` | Dataset RE3 riêng, validate grant/profile/member/source/binding độc lập; không mở rộng grant TT/Nezha, không tự cấp grant RE3. | Quyền dữ liệu vẫn riêng và tách nhãn. |
| `results/T-054/scripts/worker.py` | Dispatch RE3 tường minh, không rơi vào nhánh else Nezha; dùng reader/profile/adapter trên, ghi pha/digest/config đúng dataset. Không phát job. | Toàn tuyến nhận đúng dữ liệu và identity. |
| `results/T-054/scripts/cham.py` | Nhánh bảng held-out riêng, kiểm danh sách vế/seed/support theo giao thức RE3 được cấp; không tái dùng mẫu số/ngưỡng A4 60TT/34OB. Thiếu giao thức thì BLOCKED. Không ghép nhãn/chấm ca thật trong gói cài. | Tránh coi RE3 là tập con của bảng main. |
| `tasks/T-054-khoa-g3-chay-p7-a/SPEC.md` | Snapshot trước sửa, thêm đúng quyền 9 file code trên và kiểm synthetic; các quyền dữ liệu/main giữ nguyên. | Phạm vi viết rõ, không sửa task đã đóng. |
| `docs/WHY.md` | Nối lý do profile tường minh, lựa chọn thay thế, căn cứ schema/code, điều kiện thất bại và các OPEN; không chốt số chưa kiểm. | Lựa chọn kỹ thuật có nguồn, không hợp thức hóa giả thuyết. |
| `docs/DECISIONS.md` | Chỉ nối nguyên văn quyết định Minh nếu được duyệt, giới hạn là cài adapter/synthetic. | Không tự ghi nguồn/đơn vị/inventory thành quyết định. |

Output kiểm, snapshot, manifest, LOG và đúng dòng T054 STATE thuộc phạm vi task đã duyệt. Không sửa `src/m1/chuoi.py`, thuật toán lõi, dữ liệu, baseline lịch sử hoặc cấu hình nghiên cứu đã chọn.

Kiểm sau duyệt: mặc định TT/Nezha giữ tương đương; chuyển s/ms/us/ns tường minh và biên đầy đủ; profile thiếu/sai, alias va chạm, owner ngoài U, schema/ID/parent sai bị bác; metric OB không bị xóa hết; log null/severity không được dựng giả; từng baseline giữ trung gian/khóa/status đúng fixture; grant chéo dataset và nhãn/locator lọt vào method bị bác; bảng RE3 tách A4. Chỉ fixture và dữ liệu dev đã được phép khi cần chứng minh nhánh mặc định; không pilot RE3.

Chi phí dự kiến: không cấp máy, không thuê cloud, không tải dữ liệu đo; kiểm tổng hợp local. Chưa có số đo thời gian cài nên không hứa ETA. Mọi lượt tính toán vượt 1 giờ cần trình đúng quyền trước chạy.

## Chưa đủ để khóa G3

1. H1: nguồn khai đơn vị trace/log, `r`/cadence và inventory/namespace của RE3; hoặc Minh quyết rõ giả định chưa kiểm cùng hệ quả. Không tự chọn giả định để đóng checklist.
2. H2: duyệt đúng bản vá trên, cài/kiểm/pin. Chuẩn bị này thực hiện trước main; đánh giá RE3 vẫn chờ bản cuối.
3. Phần cloud hiện tạm dừng theo Minh và hồ sơ G3/main chưa được duyệt. Các điểm này độc lập với mất raw lịch sử T048; dữ liệu T048 trên cloud không phải input chạy chính.

Bước tiếp: Minh quyết phạm vi vá H2 ở trên; tiếp tục tìm/đối chiếu tài liệu export/deployment khi có nguồn. Sau cài, cập nhật pin/binding/gói mới theo lineage, không sửa checkpoint008. Không gọi H1/H2 xong chỉ vì có tài liệu hoặc kiểm synthetic.

Tệp đổi trong checkpoint này: output dưới `runs/chuan-bi-re3-009/`, manifest009, nối LOG và dòng T054 STATE. Không sửa code sản phẩm, SPEC, WHY, DECISIONS trong lượt này; không commit/push. Prompt bàn giao nằm cuối LOG, Minh chọn chuyển thủ công.
