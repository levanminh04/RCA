# Cài adapter RE3 H2 — checkpoint010

## Kết quả và phạm vi

Đã cài phần H2 theo Minh: “Duyệt cài H2 theo báo cáo009”, sau đó “Duyệt bổ sung 2 file CIRCA”. Đã tự kiểm bằng dữ liệu tổng hợp. Đây là kết quả cài đặt và kiểm hợp đồng, chưa là nghiệm thu độc lập hoặc bằng chứng hiệu quả RCA.

Không mở telemetry RE3, không chạy main, không SSH/sync hoặc thay đổi máy. H1 về đơn vị, inventory/alias và độ phân giải quan sát vẫn OPEN. Các profile, grant, nhãn và protocol mang tên FICTIONAL/GENERATED trong thư mục kiểm chỉ là fixture; không ghi quyết định Minh đã mở dữ liệu hoặc tạo quyền thực thi thật.

Nguồn duyệt, snapshot trước sửa, các mốc và bước tiếp nằm trong `checkpoint.json`. Nguồn quyết định và lý do được ghi DECISIONS/WHY/SPEC trước sửa code. Vai trò giữ Codex người làm, Claude phản biện.

## Thay đổi

| Nhóm | File | Hành vi |
|---|---|---|
| Đọc và chuẩn hóa RE3 | `src/p3/re3.py` (mới) | Profile đơn vị/U/alias/r và nguồn khai bắt buộc; không đoán theo độ lớn số. Chuẩn hóa số nguyên, giữ null và ID, cắt đúng biên, giữ coverage toàn file riêng với cửa sổ. Worker đối chiếu đúng hash của các byte thực đọc trước parse. |
| M1 | `src/m1/adapter.py` | Thêm profile/ca RE3; giữ log ns chính xác, metric null thành None; map suffix tường minh. Không truyền đường dẫn hay chứng cứ profile vào API phương pháp. Tên owner metric không biểu diễn được bằng delimiter của lõi thì dừng thay vì gán sai. |
| Baseline | `src/p3/adapters/baro.py`, `circa.py`, `tracerca.py`, `torai.py` | Dataset tùy chọn giữ mặc định TT; TORAI có nhánh OB không lọc ts-*. Giữ kernel, khóa/hòa, seed, graph normal-only và các variant. |
| Nguồn/quyền | `results/T-054/scripts/nguon.py` | Miền heldout/grant RE3 riêng; cần G3 và protocol bản cuối. Ghim profile, runtime, nguồn độc lập, binding, code/config/env; ma trận/partition không thiếu/trùng/chồng. Có dispatch riêng từng host. Chưa tạo grant thật. |
| Worker | `results/T-054/scripts/worker.py` | Dispatch RE3 tường minh; profile trước đọc file, nguồn đúng byte; invocation và prep TORAI giữ profile ref. Chặn locator/mã ca trong giá trị đầu vào, kể cả bảng dữ liệu. TORAI chạy Python3.8 chỉ đọc CSV; kiểm profile không buộc nạp PyArrow. |
| Bảng held-out | `results/T-054/scripts/cham.py` | Bảng RE3 riêng theo ca/ô/vế/seed/world, kiểm đủ protocol và snapshot trước ghép nhãn; không gọi A4. Độ đo/support/seed phải khai trước, không tự lấy quy tắc TT/Nezha. |
| Bổ sung CIRCA đã duyệt | `results/T-054/scripts/dieu_phoi.py`, `bien_nhan.py` | Đúng ba điều kiện: RE3 nhận đủ hai variant CIRCA, kiểm current và tạo đủ hai bản ghi TIMEOUT khi đủ điều kiện. Không nới phân loại lỗi/deadline. |

Tổng là 11 file code, gồm 9 file gốc và 2 file bổ sung đã duyệt. Ba tài liệu: SPEC T054, WHY và DECISIONS. Ngoài ra nối LOG, đổi đúng dòng T054 STATE và ghi output/manifest010 trong phạm vi task. `src/m1/chuoi.py`, công thức/nền đã chọn và kernel baseline giữ hash cũ. Diff đầy đủ: `code-diff.patch`, `documents-diff.patch`; số liệu kiểm ở `audit.json`.

## Kiểm đã chạy

Không cộng số của các lượt lặp thành số phép kiểm độc lập. Bằng chứng cuối được phân theo nhóm:

- `synthetic-004/checks.json`: 48 phép đã đạt trước một assertion sai về MicroRank. Bao gồm bảy cấu hình M1 trên fixture RE3, đồng hồ/biên/null/ID/owner, đầu vào mặc định M1 TT/Nezha khớp bản trước; toàn đầu ra BARO/TraceRCA/CIRCA mặc định khớp, đầu ra khi truyền dataset RE3 khớp nhánh preprocess tương đương; prep TORAI mặc định khớp và nhánh OB giữ metric.
- `integration-001/checks.json`: 23 phép PASS. Worker thực trên dữ liệu giả cho các nhánh còn lại, kiểm envelope/profile, cấp nguồn/quyền giả, bảng RE3 30 ca/10 ô giả và chặn đọc nhãn khi còn slot chưa xong. MicroRank giữ đúng `NO_EVIDENCE/no_normal_traces`; không sửa thuật toán hay dữ liệu để ép OK.
- `integration-003/checks.json`: 27 dòng PASS, trong đó 4 dòng worker được tái dùng từ001, không chạy lại. Phần mới gồm grant có G3 riêng, nguồn/config/mốc không khớp bị bác, ma trận thiếu/trùng và partition chồng/hở bị bác; metadata hai host 15/15 được kiểm, không dùng máy thật. Bảng tính dùng snapshot giả đã xác minh được mock để kiểm phép tính; không tuyên bố đó là thực nghiệm khoa học hoặc kiểm toàn supervisor.
- `edges-005/checks.json`: 23 phép PASS. Đủ 5 schema metric từ footer đã pin với giá trị giả, empty/missing/type/clock/ownership, byte nguồn lệch bị chặn trước parse; receiver bác CIRCA thiếu variant/sai current. Kiểm tạo bản ghi TIMEOUT mock phần phân loại/receipt tiến trình để chỉ kiểm số variant; không giết tiến trình hoặc tuyên bố kiểm lại toàn bộ giám sát.
- `wiring-001/checks.json`: 2 phép PASS cho hai đường reader trong worker truyền đúng source pin. M1 chạy lõi; riêng phép BARO này mock method, vì kernel đã được kiểm ở004.
- `torai-py38-001/validation.json`: bảng giả → CSV → kernel TORAI B thật bằng Python3.8 → output, seed0 trả OK, variant B, profile gắn đúng invocation. Không kiểm thêm seed hoặc đánh giá RE3 thật; API seed/kernel giữ nguyên.
- `environment-main.json`, `environment-py38.json`: ghi interpreter, version và đường import hiệu lực của môi trường kiểm. Probe Py38 kiểm profile không nạp PyArrow PASS. Đây là môi trường fixture local, chưa chứng nhận cloud.

Audit xác nhận 93 pin code kế thừa không đổi, 10 pin đổi đúng quyền và reader mới; ứng viên binding có 104 file. Có 583 output008 không thuộc phạm vi đổi vẫn khớp hash; toàn 15 output009 bất biến giữ nguyên. WHY/DECISIONS/LOG chỉ nối, SPEC chỉ thêm phạm vi đã duyệt, AST và diff-check đạt. Chi tiết/hash ở artifact, không rải trong báo cáo.

## Các lượt hỏng được giữ

- synthetic001: test harness dùng hàm ghi output bất biến để cập nhật tiến độ lần hai, gặp FileExistsError. Đổi riêng cách ghi progress trong thư mục kiểm mới; giữ partial và lượt cũ.
- synthetic002: fixture kỳ vọng chuyển millisecond nhưng chưa làm tròn đồng hồ tham chiếu theo độ chính xác của chính fixture. Sửa kỳ vọng kiểm; reader không bị đổi để vừa số.
- synthetic003: fixture T12 chưa cấp snapshot giả bắt buộc. Cấp snapshot được sinh riêng; không dùng snapshot RE3 thật.
- synthetic004: test yêu cầu mọi baseline trả OK. MicroRank trả NO_EVIDENCE có căn cứ native; sửa test để giữ trạng thái ấy và kiểm lại nhánh này trong integration001.
- edges001: script kiểm thiếu đường dẫn thư viện Drain3 của môi trường công cụ đang dùng; bổ sung đúng đường import đã dùng ở các kiểm khác, không cài package.
- Probe môi trường Py38 đầu: chưa có PyArrow. Qua đó phát hiện import eager của module profile có thể chặn tiến trình TORAI thật. Đã chuyển PyArrow vào riêng hàm reader, kiểm Py38 profile và reader main lại; không cài PyArrow vào Py38. Đây là sửa lỗi code trong đúng phạm vi H2.

## Điều còn mở và hệ quả

1. **H1 chưa xong:** chưa có nguồn RE3 đủ chốt đơn vị trace/log, `r`/cadence và U/alias. Không lấy union prefix hoặc nhãn root làm U thật. Fixture dùng profile giả để kiểm cài đặt, không xác nhận các giả định này. TORAI còn giả định lấy mỗi15hàng metric trong kernel đã ghim; cần đối chiếu cadence thực, không suy nó thành15giây từ schema.
2. **Chưa có protocol/grant RE3 thật:** cần khóa vế/seed/variant/world/độ đo/support/nguồn/cửa sổ/môi trường và chính sách lỗi cho bản cuối. Nhánh bảng hiện hỗ trợ cách bình quân đủ seed trong ca khi được khai tường minh; đây chưa là quyết định chọn công thức thật. TORAI A chưa có nguồn RE3 riêng; không lấy B dựng lại đặt tên A.
3. **ERROR phương pháp chưa được tự chấp nhận cho RE3:** bộ audit ERROR hiện hành chỉ có cơ chế đã khai cho TT. H2 giữ output lỗi và dừng xác minh nếu chưa có quy tắc phù hợp; không tự tính0 hoặc gán lỗi hạ tầng thành lỗi phương pháp. Trước H3 cần hoàn thiện đúng chính sách/bằng chứng liên quan; chỉ đề xuất sửa/run thêm khi có căn cứ và quyền, không tự mở dữ liệu để tìm luật.
4. **Pin/bundle main:** các plan/protocol008 là mốc trước H2. Không dùng nguyên pin ấy chạy code hiện tại. `code-binding-candidate.json` chỉ là ứng viên hash local, chưa phải gói cloud hoặc bản G3. Cần cập nhật binding/bundle/plan đúng phần code đổi và kiểm tuyến/môi trường liên quan trước khóa; dùng lại kết quả khoa học còn hợp lệ, không chạy lại baseline diện rộng.
5. **Cloud vẫn tạm dừng theo Minh.** Chưa stage hoặc kiểm lại môi trường EC2. Chưa khóa G3/main. Vì vậy chưa thể nói chỉ còn bật cloud là chạy chính.

Task đã đạt phần cài và tự kiểm H2 trong phạm vi nêu trên. Chưa có kết quả held-out để trả lời RQ3/RQ5, chưa xác nhận lợi ích đồ thị hay hỗ trợ trên RE3 thật. Nút/cạnh và phép tính M1/CIRCA giữ thiết kế đã chọn; adapter chỉ chuyển nguồn đúng hợp đồng.

## Tiếp nhận

Đọc `checkpoint.json`, báo cáo này, `audit.json` và hai manifest009/010 trước tiếp tục. Không chạy lại bootstrap, check_h2 hoặc các script tạo output vào thư mục đã tồn tại. Mọi lượt mới dùng run/attempt mới; giữ lượt cũ.

Bước tiếp: hoàn thiện H1 bằng nguồn metadata/export/deployment được phép; xử lý các quyết định protocol còn mở, cập nhật bản ghim thực thi và hồ sơ G3. Chưa đọc telemetry RE3. Claude chưa kiểm checkpoint010; prompt trung tính nằm ở `prompt-claude.txt` và cuối LOG để Minh chọn chuyển thủ công.

Đề xuất nội dung commit khi Minh muốn: “Cài adapter RE3 H2 và kiểm tuyến held-out bằng fixture”. Chưa commit/push.
