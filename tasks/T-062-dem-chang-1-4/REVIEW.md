# Phản biện T-062

- **Người phản biện:** Codex — **Ngày:** 12/11/2026.
- **Công đoạn/cổng:** soát kết quả; kế hoạch giai đoạn 2, cổng gần nhất G4.
- **Bản lượt:** `tasks/T-062-dem-chang-1-4/REVIEW.md`.
- **Vai trò:** phản biện phần Claude làm: A1, A2, B1, D1, D2, E1, E2, H1. Không phản biện C1 hoặc G1.
- **Revision đối chiếu:** repo RCA so với `c3d27f8a`; FlashTicket nhánh `rca/quan-sat-log`, gồm các commit T-062 và merge cập nhật `main`.
- **Quyền ghi:** chỉ xuất nội dung bản này qua tùy chọn `-o`. Không sửa kết quả, LOG, STATE hoặc code.

**Đã đọc:** AGENTS; STATE; SPEC, BOI-CANH, LOG, CHECKPOINT, PROMPT-DIEU-PHOI của T-062; DT18; hướng dẫn của cô; phần MRP, WHY, DECISIONS, LESSONS chi phối công việc; kế hoạch giai đoạn 2; yêu cầu R-01–R-10; danh mục T-059; hợp đồng chuyển giao T-043; định dạng và bộ chuyển T-061. Đã kiểm code, hồ sơ triển khai, bộ tiêm, runner, sổ, gói ca, trung gian M1, kết quả và dữ liệu tải liên quan.

**Tự soát độc lập:** đọc nguồn và đầu ra thật trước khi lập các nhận xét dưới đây. Không đọc kết luận các bản `REVIEW-G1*.md` hoặc phản hồi G1.

## Kết luận chung

T-062 đã tạo được đầu ra của lượt phát triển đầu: chín ca có M1, kết quả tất định, chuyển định dạng giữ đúng hạng/cạnh/verdict; năm ca tiêm có thành phần thuộc tập chấp nhận đứng hạng 1. Tuy nhiên, kết luận **“4/4 báo động giả trên ca không lỗi” chưa hợp lệ**, và báo cáo bỏ sót phản hồi 429/500 của ca FLASH.

Đề nghị giữ kết quả gốc nhưng chưa duyệt nguyên đề xuất chặng 4. Tiêu chí chọn, phạm vi so sánh và khẳng định khả năng phục hồi lượt chạy cần sửa hoặc làm rõ trước.

## Các điểm

### R1. Gán ca khỏe và kết luận báo động giả trái với dữ liệu đã lưu — CHẶN

- **Ở đâu:** `results/T-062/bao-cao-sang.md:15,48,54`; `bang-ket-qua.py`; `e2.py::DAP_AN`; `ket-qua/phat-lai/bang-cham.json`; đề xuất chặng 4 §1b.
- **Sai gì:** báo cáo ghi FLASH “không có 5xx/429”, đồng thời tính cả bốn ca không tiêm lỗi thành mẫu ca khỏe để kết luận báo động giả. Hai việc này không được bằng chứng hỗ trợ.

**Bằng chứng kiểm lại từ file gốc**

Đã đọc `tai/out/e1-00eaea92/raw.json`, lấy các bản ghi:

```text
type = Point
metric = http_req_duration
route thuộc hỗn hợp nghiệp vụ
t ≤ data.time < t + 600
t lấy từ ca/00eaea92/cases/00eaea92/request.json
```

Kết quả:

| Pha giữa của FLASH | Số request |
|---|---:|
| HTTP 200 | 7.276 |
| HTTP 429 | 244 |
| HTTP 500 | 840 |
| Tổng | 8.360 |

Có thêm ba lượt rơi. Toàn bộ 244 phản hồi 429 thuộc GET event. Đối chiếu `raw-logs.jsonl` của cùng gói thấy 244 dòng Gateway với `routeId = event`, `reasonCode = RATE_LIMIT_EXCEEDED`.

Bảng `chay/k6-theo-pha.md` cũng đã ghi `tickets 840/840` lỗi trong pha giữa của FLASH. Ba ca `BINH-THUONG` đều có `tickets 300/300` lỗi trong pha giữa. Đây là lỗi nền đã được chính `tiem-loi/o-loi.md` khai báo.

T-059 §“Ca khỏe” chỉ cho gán `root = null` sau khi đạt ngưỡng backend khai trước và checks độc lập. Hồ sơ FLASH chưa có ngưỡng ấy; báo cáo §7 cũng thừa nhận chưa xác nhận khỏe.

Ngoài ra, chế độ a không buộc M1 trả `CAUSE_FOUND`. `src/m1/xep_hang.py::verdict` chỉ trả trạng thái này khi có thành phần tầng 1. Phản ví dụ thật đã kiểm hash: T-058 `c12e47ab` cũng chạy chế độ a nhưng trả `NO_INTRINSIC_ANOMALY`.

- **Phần có thể phản bác finding:** báo cáo đã ghi “theo định nghĩa đề xuất”, “chỉ khám phá” và n = 1. Những giới hạn này đúng. Chúng không làm câu “không có 5xx/429” đúng, cũng không xác nhận bốn ca là ca khỏe.
- **Bước và quyết định chịu ảnh hưởng:** lỗi diễn giải đã xảy ra ở E2/H1. Chặn sử dụng tỷ lệ 4/4 làm bằng chứng báo động giả trên hệ khỏe hoặc làm căn cứ chọn thành phần chặng 4. Không bác bỏ quan sát chín ca đều trả `CAUSE_FOUND`.
- **Đề xuất sửa tối thiểu:** đính chính số FLASH; gọi đúng nhóm hiện tại là **không tiêm lỗi mới, có lỗi nền**; giữ FLASH ở nhóm chưa xác nhận khỏe/bị giới hạn tại Gateway. Giữ riêng tỷ lệ `CAUSE_FOUND` mô tả; chưa gọi nó là tỷ lệ báo động giả trên ca khỏe.
- **Đề xuất cho Minh:** giữ toàn bộ đầu ra gốc và đính chính cách chấm/diễn giải, chưa chạy lại M1. Phương án khác là định nghĩa phép đo “phát hiện thay đổi so với nền có lỗi cố định”; phép đo này có ý nghĩa khác và phải khai rõ trước lượt dùng để chọn.

### R2. Bộ kiểm R-05 trả ĐẠT khi chưa kiểm định danh trên đủ ba tín hiệu — KHÔNG CHẶN kết quả M1 hiện tại

- **Ở đâu:** `kiem-du-lieu/kiem-r.py:95–103`; `r-a5539fba.json#/R/R-05`; `bao-cao-B1.md`, hàng R-05.
- **Sai gì:** điều kiện trả `DAT` chỉ kiểm `host.id` có giá trị ở resource trace/log:

```python
all(x[1] for x in rs) and all(x[1] for x in lr)
```

Nó không kiểm instance ID, không dùng kết quả kiểm metric vào quyết định, và không đối chiếu binding với manifest. Vì vậy, bỏ instance ID hoặc thiếu host ID của metric vẫn có thể được báo `DAT`.

**Bằng chứng trên dữ liệu thật**

Resource log Gateway dùng `api-gateway-1`, trong khi resource trace dùng UUID của lần khởi động. Payment và Ticket có tình trạng tương tự. Báo cáo đã nhận ra khác biệt này nhưng vẫn kết luận ĐẠT cho R-05.

Đã kiểm thêm phần có thể bác bỏ finding: `body.instanceId` trong log B16 của ba service trên **khớp** instance của trace. Vì vậy, không có căn cứ nói toàn bộ dữ liệu mất khả năng nối định danh. Lỗi là bộ kiểm chưa thực hiện phép đối chiếu ấy và trạng thái ĐẠT đang rộng hơn điều đã kiểm.

- **Bước và quyết định chịu ảnh hưởng:** lỗi trong bộ kiểm B1. Không làm sai hạng của chín ca hiện tại. Chặn việc coi trạng thái `DAT` này là xác nhận đầy đủ R-05 hoặc dùng nó để phát hiện đúng các lần mất định danh sau triển khai.
- **Đề xuất sửa tối thiểu:** phân biệt kiểm hiện diện host với kiểm định danh/binding; kiểm body và resource theo quy ước khai rõ, cùng metric và manifest. Chỉ báo ĐẠT đầy đủ khi các điều kiện tương ứng đã được đối chiếu.
- **Đề xuất cho Minh:** sửa bộ kiểm ở revision mới, dùng lại gói đã đóng băng; chưa cần thu lại dữ liệu hoặc sửa Collector chỉ để xử lý finding này. Đổi nhãn thành “đạt kiểm hiện diện host” là phương án đính chính nhỏ hơn, nhưng chưa hoàn thành phép kiểm R-05.

### R3. Luật chọn loại chính thành phần giảm báo động giả mà đề xuất muốn tìm — CHẶN

- **Ở đâu:** `spec-chang-4-de-xuat.md:17,23,47`.
- **Sai gì:** §1b muốn tìm thành phần “giảm báo động giả mà giữ hạng ở ca lỗi”. Nhưng §4.3 bắt buộc **AC@3 phải tăng ít nhất một ca**, đồng thời báo động giả không tăng.

Một thành phần chỉ giảm báo động giả và giữ nguyên xếp hạng sẽ luôn bị loại. Khi P7 đã đạt trần AC@3 trên một tập ca, không thành phần nào có thể được giữ bằng luật này, bất kể nó cải thiện phân biệt ca khỏe đến đâu.

**Phản ví dụ logic, không phải kết quả thực nghiệm**

Hai bản cùng đúng AC@3 trên toàn bộ ca lỗi. Bản mới giảm `CAUSE_FOUND` sai trên các ca khỏe đã xác nhận xuống 0 và giữ nguyên hạng ca lỗi. Theo mục tiêu §1b, đây là cải thiện cần xét; theo §4.3, nó vẫn trượt.

Mẫu số cũng sai: bảy ô phát triển T-059 gồm **sáu ô lỗi và một FLASH-HEALTHY**. Đã đếm từ `danh-muc-loi.json#/cells`. Ba lặp của sáu ô lỗi là 18 ca lỗi, không phải 21. Nếu bỏ REDIS-BOOK thì còn 15 ca lỗi. Bảng dữ liệu còn liệt kê FLASH riêng nên cần làm rõ số lượt của nhóm này.

- **Phần có thể phản bác finding:** đây mới là đề xuất, chưa chạy biến thể. Do đó chưa có bằng chứng người làm đã chọn sai hoặc đổi tiêu chí sau kết quả biến thể.
- **Bước và quyết định chịu ảnh hưởng:** mâu thuẫn thiết kế ở H1. Chặn duyệt nguyên luật chọn và dự toán dựa trên tập ca hiện ghi.
- **Đề xuất sửa tối thiểu:** khai lại các tập ca lỗi, ca khỏe và ca chưa phân xử; sửa mẫu số và số lượt. Đề xuất luật cho phép xét cả hai hướng: tăng chất lượng xếp hạng mà không tăng báo động giả, hoặc giảm báo động giả mà không giảm chất lượng xếp hạng. Ngưỡng cụ thể vẫn do Minh duyệt trước khi chạy.
- **Đề xuất cho Minh:** dùng luật hai hướng trên, sau khi giải quyết R1. Mặt trái là phải khai rõ ưu tiên khi hai đại lượng đánh đổi. Phương án chỉ ưu tiên AC@3 vẫn có thể được chọn, nhưng khi đó phải bỏ mục tiêu chọn thành phần chỉ nhằm giảm báo động giả.

### R4. Đề xuất chặng 4 chưa bố trí phần baseline của mục tiêu nguồn — CHẶN duyệt đề xuất như kế hoạch đầy đủ

- **Ở đâu:** `spec-chang-4-de-xuat.md` §1–§6; `docs/techstack/KE-HOACH-GIAI-DOAN-2.md` §3, chặng 4.
- **Sai gì:** kế hoạch nguồn yêu cầu “Chạy M1 và baseline trên dữ liệu phát triển”. Đề xuất dẫn lại câu này nhưng ma trận thực hiện chỉ có P7 và các biến thể bỏ thành phần. Không khai baseline nào, đầu vào tương đương, vai trò trong lựa chọn, đầu ra hoặc chi phí.

P7 là đối chứng chuyển thẳng cần giữ. Nó không tự thay thế phần so với baseline hiện có mà kế hoạch nguồn yêu cầu.

Hợp đồng T-043 B1.9/D14 còn yêu cầu tách bản P7, bản FlashTicket và bản FlashTicket che từng nhóm thông tin phong phú; che cả đầu vào lẫn dẫn xuất. Đề xuất chưa chỉ rõ các vế được thực hiện ở chặng nào, và vế nào còn là nghĩa vụ trước kết luận chuyển giao/hiệu quả.

- **Phần có thể phản bác finding:** bảng ứng viên đã yêu cầu đối chứng bỏ từng thành phần. Đây là hướng đúng. Không có yêu cầu phải chạy xong mọi phép so trong T-062 hoặc ngay trong lượt phản biện này.
- **Bước và quyết định chịu ảnh hưởng:** thiếu phạm vi và phụ thuộc trong đề xuất H1. Chặn việc duyệt tài liệu hiện tại như kế hoạch đầy đủ để “chọn xong phiên bản M1 cho FlashTicket”. Không chặn nghiệm thu phần chạy P7 mô tả của T-062.
- **Đề xuất sửa tối thiểu:** bổ sung ma trận so sánh cụ thể; nêu baseline nào chạy trên dev, vế nào phục vụ chọn và vế nào chỉ báo cáo. Ghi nơi nhận các phép so bắt buộc còn lại và giới hạn kết luận khi chưa làm; cộng chi phí tương ứng.
- **Đề xuất cho Minh:** giữ phần baseline trong chặng 4 như kế hoạch nguồn. Nếu muốn tách thành gói sau, cần quyết rõ đầu ra chặng 4 chỉ đạt phần nào và chưa dùng để kết luận gì. Cách tách có thể giảm thời gian trước mắt nhưng chưa hoàn tất mục tiêu nguồn.

### R5. Khẳng định phục hồi lỗi bằng cách stage lại cùng mã chưa khớp đường thực thi — CHẶN tái dùng nguyên hồ sơ cho lượt dài mới

- **Ở đâu:** `chay/HO-SO-LUOT-E1.md:13`; `spec-chang-4-de-xuat.md:27`; `chay/runner.py::m1_worker`; runner T-058 được tái dùng.
- **Sai gì:** hồ sơ ghi lỗi M1/stage/export có thể “stage lại đúng mã/t”, mất khoảng ba phút. Đề xuất chặng 4 coi bộ chạy T-062 đã đáp ứng xử lý lỗi giữa chừng. Nhưng đường retry ấy chưa thực thi được tổng quát.

**Bằng chứng từ code đã kiểm hash**

- `stage-m1.py:59` tạo thư mục ca bằng `exist_ok=False`, trước khi đóng gói xong.
- `run-m1.py:55` tạo thư mục outputs bằng `exist_ok=False`, trước khi hoàn thành hai lần chạy.
- `runner.py::m1_worker` bắt ngoại lệ rồi ghi log; không có nhánh nhận lại ca/attempt dang dở.

Nếu stage lỗi sau khi tạo thư mục, gọi lại cùng mã sẽ dừng tại `FileExistsError`. Nếu M1 lỗi sau khi tạo outputs, gọi lại cũng bị chặn. Vì vậy không thể coi “stage lại cùng mã” là đường phục hồi đã có với chi phí đã xác nhận.

- **Phần có thể phản bác finding:** chín ca E1 chính đều thành công. Không có bằng chứng lỗi này đã làm sai kết quả hoặc buộc chạy lại cả E1. Bộ chạy cũng đã cách ly ngoại lệ theo ca.
- **Bước và quyết định chịu ảnh hưởng:** mâu thuẫn vận hành cho lượt kế tiếp, không phải lỗi phương pháp quan sát được trong chín ca. Chặn dùng nguyên hồ sơ hiện tại để xác nhận khả năng phục hồi của lượt dài mới.
- **Đề xuất sửa tối thiểu:** bỏ khẳng định đã có đường phục hồi tổng quát. Trước lượt mới, định nghĩa đường tiếp nhận riêng cho gói hợp lệ đã đóng băng và attempt dang dở; giữ mọi attempt cũ. Kiểm đúng tình huống thư mục đã tồn tại trước khi nhận là phục hồi được.
- **Đề xuất cho Minh:** làm phần tiếp nhận trong wrapper của task mới, giữ runner T-058 đã ghim. Mặt trái là thêm một phần cài đặt nhỏ cần kiểm. Phương án sửa trực tiếp runner cũ làm đổi hash trong plan/artifact manifest của T-058 nên không phải sửa cục bộ vô hại. Chi phí phục hồi còn phụ thuộc giai đoạn hỏng và đầu vào còn đủ hay không; hiện chưa có căn cứ giữ con số ba phút cho mọi trường hợp.

## Đối chiếu các lượt trước

Không có lượt phản biện/phản hồi trước trong phạm vi được giao. Không đánh giá lại G1 và không dùng kết luận G1 để lập các finding trên.

## Tuân thủ quy trình

- Minh chỉ định Codex phản biện phần Claude làm trong lượt hiện tại. Không tự đổi vai hoặc phản biện C1.
- Đã kiểm diff RCA và lịch sử nhánh FlashTicket. Diff tổng từ commit gốc chứa thay đổi của nhiều task; không đủ căn cứ gán mọi thay đổi đó cho T-062 hoặc kết luận có sửa ngoài quyền.
- Không thấy bằng chứng thay code lõi M1 để chọn theo kết quả T-062. Bản đề xuất chặng 4 vẫn ghi chưa duyệt; không coi các ứng viên C4 là quyết định.
- D2 đã khai việc đổi ngưỡng xác nhận EVENT-DB-LAT sau khi thấy lượt thử. Đây là sửa sau được công khai, không phải ngưỡng hoàn toàn khai trước. Không suy sự việc này thành chỉnh M1 bằng test.
- LOG thiếu prompt bàn giao với lý do chưa chỉ định reviewer. Lượt hiện tại đã được Minh cung cấp phạm vi và nguồn trực tiếp; không nêu thành finding thủ tục riêng.
- Không thêm quyết định vào DECISIONS hoặc WHY. Các khuyến nghị trong bản này đều là đề xuất, chưa được Minh quyết.

**Ảnh hưởng hash khi sửa:** các file báo cáo, đề xuất và script T-062 nêu trên đang nằm trong `results/T-062/manifest.json`. Sửa chúng sẽ đổi hash. Runner T-058 còn được ghim trong execution plan và artifact manifest; code lõi M1 có pin riêng. Đề nghị giữ bản gốc, ghi đính chính/revision mới và manifest phù hợp sau khi Minh duyệt; không sửa ngầm các byte đã dùng cho lượt chạy.

## Điều đã kiểm và thấy đúng

1. **Toàn vẹn:** đã băm 461 mục của manifest T-062. Có 460 mục khớp; một mục lệch là `giao-dien/phan-hoi-g1.md`, ngoài phạm vi. Đã dừng dùng file đó làm bằng chứng. Các đầu ra mới ngoài manifest chủ yếu thuộc lượt G1 và nhật ký điều phối/phản biện; không dùng chúng chứng minh kết quả lượt đêm.
2. **Nguồn cũ:** các file T-058 trực tiếp dùng để đối chiếu, plan M1 và 39 pin code lõi đã kiểm đều khớp. R-01–R-10 khớp manifest T-040. Ba file `_nguon` của T-062 khớp plan khóa T-058.
3. **Gói ca và sổ:** 45 file đầu vào trong chín manifest ca khớp hash; chín hash `method-input` khớp summary; chuỗi sổ 173 dòng không đứt.
4. **Tất định:** chín cặp `method-output-1/2.json` trùng hash; chín ca đều có trạng thái `OK`.
5. **Chuyển đổi:** cả chín ca giữ đúng hạng, cạnh và verdict. Bỏ khối `phat_lai` thì nội dung còn lại trùng bản thường. Chỉ mục đủ đúng chín mã.
6. **Cách ly nhãn:** đã soát đường đọc và quét chín đầu vào M1 theo mã ca, tên ô và các dấu công cụ tiêm liên quan; không tìm thấy các giá trị ấy. Mốc t được cấp ở chế độ a là đầu vào đã được phép.
7. **B1:** đếm lại gói `a5539fba` được 7.500 log B16, cả 7.500 nối đúng cặp trace/span; 6.000 log Gateway nối đúng span Gateway. Gói T-058 đối chiếu có 16 log B16 và không nối được span. Kết quả cải thiện này được dữ liệu hỗ trợ.
8. **Xếp hạng:** năm ca lỗi có thành phần thuộc tập chấp nhận đứng hạng 1. Đây là điểm định vị qua tập chấp nhận, không phải chứng minh tìm đúng cạnh gốc.
9. **NET-GW-BOOK:** đã lần tới cơ chế. Trong cửa sổ M1, GET order phía Booking có 375 span mỗi nửa; trung vị thời lượng N/A là 2.670/2.637 µs. M1 lưu cờ trên `canh|api-gateway|booking-service`; E2-C gán cờ ấy cho Booking, rồi Booking đứng đầu. Do đó có bằng chứng về cạnh, nhưng đầu ra xếp hạng vẫn là nút. Không nên diễn giải thành M1 hoàn toàn không sử dụng được thông tin cạnh.
10. **Giới hạn xác minh:** không chạy lại build, M1 hoặc thực nghiệm. `py -3` không có trong PATH; Python của venv không khởi chạy được dưới tài khoản sandbox. Các phép đếm/hash/đối chiếu được thực hiện chỉ đọc bằng Node REPL. GitHub CLI và SSH bị chặn quyền mạng; chưa xác nhận trực tiếp CI hoặc trạng thái máy hiện tại. Không lấy “CI xanh” trong báo cáo làm kết quả đã kiểm độc lập ở lượt này.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm:** kiểm độc lập phần được giao, từ nguồn yêu cầu qua code, gói dữ liệu, trung gian, chuyển đổi và chấm.
2. **File thay đổi:** không sửa file nào bằng công cụ. Toàn bộ câu trả lời này là nội dung để lệnh `-o` ghi đúng `tasks/T-062-dem-chang-1-4/REVIEW.md`. Không ghi LOG/STATE hoặc commit.
3. **Kiểm và kết quả:** toàn vẹn và chuyển đổi của chín ca trong phạm vi đạt các kiểm nêu trên. Phát hiện sai số FLASH, nhãn khỏe chưa hợp lệ, lỗi phạm vi kiểm R-05 và các thiếu sót trong đề xuất chặng 4.
4. **Phần còn mở và quyết định bị ảnh hưởng:**
   - T-062 hỗ trợ kết luận **chạy P7 và hiển thị kết quả trên một lượt phát triển**; chưa xác nhận hiệu quả trên hệ khỏe hoặc trả lời RQ5.
   - Muốn đo báo động giả trên ca khỏe cần ngưỡng sức khỏe đã khai và dữ liệu đạt điều kiện ấy. Dữ liệu hiện tại phân biệt được không tiêm thêm lỗi, nhưng không tự xác nhận hệ khỏe.
   - Các ứng viên pool, queue và thành phần chết im chưa có nhóm dev mục tiêu tương ứng trong kế hoạch hiện ghi. Claude cần nêu dữ liệu nào phân xử chúng hoặc giữ kết luận ứng viên OPEN; không dùng các ô đánh giá để chọn. Chi phí phụ thuộc tập ô và tải được Minh duyệt, chưa thể lấy dự toán hiện tại làm tổng chi phí đầy đủ.
   - Đề xuất Minh giữ chín kết quả gốc, duyệt đính chính R1; yêu cầu người làm đáp R3–R5 trước khi duyệt nguyên kế hoạch chạy tiếp. R2 xử lý bằng bản kiểm mới trên dữ liệu sẵn có, không cần chạy lại chiến dịch chỉ vì finding này.

**Đề xuất tiếp tục một lượt người làm đáp phản biện.** Còn phản đối ảnh hưởng trực tiếp tới diễn giải kết quả và kế hoạch đang xin duyệt. Chưa cần phát thực nghiệm mới để trả lời các finding này. Minh quyết sửa, chấp nhận giới hạn hoặc dừng; bản phản biện không tự đóng task, duyệt SPEC hay mở test.

## Prompt bàn giao cho người làm

Phạm vi ghi của lượt đáp chưa được Minh cấp trong bản này; prompt dưới đây mặc định chỉ trả lời trong chat. Minh có thể duyệt phạm vi cụ thể khi chuyển.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-062, tasks/T-062-dem-chang-1-4/; các bước A1, A2, B1, D1, D2, E1, E2, H1; results/T-062/bao-cao-sang.md và results/T-062/spec-chang-4-de-xuat.md; các đề xuất trong tasks/T-062-dem-chang-1-4/REVIEW.md. C1 và G1 ngoài phạm vi lượt này.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: kế hoạch giai đoạn 2, chặng 1a, 2, 3, 4 lượt đầu và nhánh G; cổng gần nhất G4.
- Người làm và người phản biện chính thức: Claude làm phần điều phối và các bước thuộc phạm vi trên; Codex làm C1. Minh giao Codex phản biện phần Claude làm trong chat 12/11/2026.
- Tài liệu gốc: tasks/T-062-dem-chang-1-4/{SPEC,BOI-CANH,LOG,CHECKPOINT,PROMPT-DIEU-PHOI}.md; docs/techstack/KE-HOACH-GIAI-DOAN-2.md; results/T-059/danh-muc-loi.md và .json; results/T-061/dinh-dang-ket-qua-rca.md; results/T-040/yeu-cau-quan-sat-p9.md; tasks/T-043-thiet-ke-rca-m1/SPEC.md; git diff repo RCA so với c3d27f8a; lịch sử nhánh rca/quan-sat-log trong D:/Project/flash-ticket-platform, PR levanminh04/flash-ticket-platform#17.
- Phản biện và phản hồi trước: tasks/T-062-dem-chang-1-4/REVIEW.md; chưa có phản hồi của người làm cho phạm vi này. REVIEW-G1*.md thuộc lượt riêng.
- Code và kết quả liên quan: results/T-062/manifest.json; ha-tang/, kiem-du-lieu/, tiem-loi/, chay/, ca/, ket-qua/, e2.py, bang-ket-qua.py và dữ liệu tải của E1; results/T-058/dem-2026-11-10/{stage-m1.py,run-m1.py,m1-execution-plan-v2.json,m1-source-pins.json}; src/m1/; bộ chuyển results/T-061/chuyen-doi.py. Python theo hướng dẫn repo: py -3 -B. Máy exp-app/exp-obs chỉ đọc qua SSH theo SPEC; không ghi lên máy.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat nếu Minh chưa cấp thêm quyền ghi cụ thể; không sửa kết quả, code, SPEC, LOG, STATE hoặc bản phản biện.

Không sửa ngoài phạm vi trên, không commit. Chưa có quyền ghi rõ ràng thì chỉ đọc và trả lời trong chat. Giữ các bản lượt cũ. Không đọc dữ liệu khóa hoặc chạy thực nghiệm ngoài quyền được duyệt.

Đọc nguồn và đầu ra gốc trước khi đọc kết luận các lượt phản biện/phản hồi. Lập nhận xét độc lập trước, không lấy tóm tắt trong LOG thay bằng chứng trên file thật.
Nguồn đối chiếu: docs/STATE.md, SPEC và LOG nếu có; phần trực tiếp chi phối trong docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md.
Nguồn đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ và được phép); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.
7. Kiểm cả đạt SPEC và đạt phần mục tiêu nguồn. Nếu chỉ đạt một phần, nêu phần thiếu và quyết định phụ thuộc. Không dùng “chưa kiểm” làm căn cứ đã xác nhận hoặc “ngoài SPEC” để bỏ nghĩa vụ nghiên cứu. Không ép một nguyên nhân vào chỗ chưa biết.
8. Với nhận định quan trọng, hỏi còn nguyên nhân khả thi nào khác giải thích kết quả và bằng chứng có phân xử được không. Trước khi dùng đầu ra cũ, kiểm hash theo manifest phù hợp; lệch thì dừng phần phụ thuộc và báo Minh. Số làm bằng chứng phải có đường dẫn và con trỏ JSON hoặc lệnh đã chạy kèm kết quả.
9. Kiểm tuân thủ quy trình bằng việc thực tế: vai trò, quyền ghi và duyệt phạm vi; nguồn quyết định; tự kiểm; LOG/STATE/bàn giao theo nghĩa vụ của vai trò; tự đổi mục tiêu/tiêu chí/thiết kế; đề nghị chuyển bước khi thiếu căn cứ. Áp dụng luật và quyền có hiệu lực ở thời điểm việc được làm, không tự mở lại task đã đóng. Chỉ báo vi phạm có bằng chứng và ảnh hưởng cụ thể, không chỉ xác nhận đã đọc AGENTS.
10. Sau tự soát, kiểm từng điểm và phản hồi các lượt trước: đúng / đúng một phần / sai / chưa kiểm được, với bằng chứng riêng. Không mặc nhiên đồng ý với bên nào. Nêu phạm vi lỗi rộng/hẹp hơn hoặc mặt trái của đề xuất sửa.
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: CHẶN hoặc KHÔNG CHẶN; chặn kết luận/quyết định nào; ở đâu; sai gì;
bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); hậu quả; đề xuất sửa tối thiểu hoặc bằng chứng còn thiếu.
Tiếng Việt, câu ngắn.

Cuối lượt báo:
1. Đã làm gì.
2. File đã thay đổi, hoặc không sửa file nào.
3. Kiểm đã chạy và kết quả.
4. Bất đồng có bằng chứng, câu hỏi mở, phần thiếu và quyết định bị ảnh hưởng; điều cần Minh quyết.

Đề xuất tiếp tục hoặc dừng phản biện, kèm lý do. Nếu không còn phản đối chưa xử lý ảnh hưởng tính đúng, phạm vi kết luận hoặc quyết định đang xin duyệt, đề xuất dừng; không che bất đồng bên kia còn giữ. Có thể thống nhất giới hạn khi thiếu bằng chứng; kết luận phụ thuộc vẫn OPEN. Minh quyết cuối. Hai agent đồng ý không thay bằng chứng khoa học; dừng phản biện không tự duyệt SPEC, đóng task hoặc mở test.

Sau đó soạn prompt bàn giao cho agent đối phương: chép nguyên văn Prompt chung + đúng Khối công đoạn + Khối cổng hiện có trong docs/review-prompt.md, chỉ điền thông tin trung tính. Giữ vai trò; người làm nhận prompt đáp phản biện, người phản biện nhận prompt kiểm độc lập. Vẫn soạn khi đề xuất dừng để Minh chọn gửi hay dừng; không tự gửi.

Công đoạn: người làm đáp phản biện. Giữ vai trò người làm, không là người phản biện chính thức của chính task.
Tự soát yêu cầu và mọi file đầu ra gốc cần để trả lời các câu hỏi như một người chưa từng làm task, TRƯỚC khi mở kết luận các bản phản biện. Ghi danh sách điểm tự tìm được vào LOG trước khi mở các kết luận ấy nếu được phép ghi; phiên chỉ đọc ghi nhận xét trong chat.
Sau đó kiểm từng điểm phản biện trên file/code/dữ liệu thật; chạy lại khi rẻ và được phép. Kết luận đúng / đúng một phần / sai / chưa kiểm được với bằng chứng riêng. Reviewer có thể sai, nói quá hoặc đề xuất sửa có mặt trái.
Nếu được Minh cho phép: điền bảng Phản hồi của người làm ở cuối đúng bản phản biện; thêm N1, N2… cho điểm tự tìm được với CHẶN/KHÔNG CHẶN; để trống cột Minh quyết; nối LOG đủ mục 7 của AGENTS, gồm đề xuất sửa gom theo file; chỉ cập nhật dòng task trong STATE khi được phép. Không sửa nội dung hay prompt của reviewer hoặc tự sửa báo cáo/code.
Nếu chưa có quyền ghi các phần này, trình phản hồi và đề xuất trong chat. Soạn prompt bàn giao cho người phản biện kiểm độc lập.

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```

## Phản hồi của người làm (người làm điền sau)

Người làm chỉ điền trong quyền Minh duyệt. Không sửa nhận xét hoặc prompt của người phản biện. Để trống cột “Minh quyết”.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|| R1 | **Đúng.** CHẶN như reviewer nêu. | Đếm lại `tai/out/e1-00eaea92/raw.json`, pha [t, t+600) với t trong `ca/00eaea92/cases/00eaea92/request.json`: 200 = 7.276, 500 = 840 (tickets), 429 = 244 (cả 244 ở GET event), tổng 8.360. Câu "không có 5xx/429" ở `bao-cao-sang.md` §2 là sai: bảng `chay/k6-theo-pha.md` tôi lập chỉ có cột 5xx cho event/order/payment, không có cột 429, nên tôi đọc thiếu. Câu "ở chế độ a M1 luôn đi tìm nguyên nhân" cũng sai: `src/m1/xep_hang.py::verdict` trả `NO_INTRINSIC_ANOMALY` khi tầng 1 rỗng; T-058 `c12e47ab` là phản ví dụ. Ba ca BINH-THUONG có lỗi nền tickets 500 (300/300 mỗi pha), nên gọi là "không tiêm lỗi mới, có lỗi nền", chưa phải ca khỏe theo T-059. **Đề xuất sửa:** không sửa byte cũ; ghi bản đính chính mới cho `bao-cao-sang.md` §1–§2 và `spec-chang-4-de-xuat.md` §1b (số FLASH, tên nhóm, bỏ chữ "báo động giả", bỏ suy luận chế độ a), thêm cột 429 vào `k6-theo-pha.py` ở revision mới. Không chạy lại M1. | |
| R2 | **Đúng.** KHÔNG CHẶN. | `kiem-r.py` R-05 chỉ kiểm `host.id` có mặt ở resource trace/log; không dùng kết quả metric, không đối chiếu instance/binding. Tôi đã thấy lệch `service.instance.id` (log tĩnh `<svc>-1`, trace UUID) nhưng vẫn ghi ĐẠT "có lưu ý" — mạnh hơn điều đã kiểm. **Đề xuất:** bản kiểm mới tách "hiện diện host" với "định danh khớp" (so `body.instanceId` của log B16 với resource trace, có metric), chạy lại trên gói đã đóng băng; đổi nhãn R-05 trong `bao-cao-B1.md` bản đính chính. | |
| R3 | **Đúng.** CHẶN duyệt luật chọn hiện tại. | Luật §4.3 bắt AC@3 tăng ≥1 ca nên loại thành phần chỉ giảm `CAUSE_FOUND` ở ca không lỗi — mâu thuẫn §1b tôi thêm sau. Mẫu số sai: 7 ô dev T-059 gồm 6 ô lỗi + FLASH → 3 lặp = 18 ca lỗi (15 nếu bỏ REDIS-BOOK), không phải 21. **Đề xuất:** luật hai hướng như reviewer nêu, khai thứ tự ưu tiên khi đánh đổi; tập ca khỏe chỉ gồm ca đạt ngưỡng sức khỏe khai trước (cần ngưỡng FLASH/T-059). | |
| R4 | **Đúng.** CHẶN duyệt đề xuất như kế hoạch đầy đủ. | Kế hoạch nguồn ghi "Chạy M1 và baseline trên dữ liệu phát triển"; đề xuất chỉ có P7 và biến thể bỏ thành phần. **Đề xuất:** thêm ma trận: baseline đã cài (P3, `src/p3/adapters/`) chạy trên cùng gói dev, vai trò báo cáo/so sánh; vế che thông tin phong phú theo T-043 B1.9/D14; nêu phần nào để gói sau và giới hạn kết luận; cộng chi phí. Cần Minh chọn baseline nào. | |
| R5 | **Đúng.** CHẶN dùng nguyên hồ sơ cho lượt mới. | `stage-m1.py:59`, `run-m1.py:55` đều `exist_ok=False`; `runner.py::m1_worker` không có nhánh tiếp nhận. Câu "stage lại đúng mã/t" trong `HO-SO-LUOT-E1.md` sai. Một đường khả thi chưa kiểm: stage lại cùng `t` với mã mờ **mới** (stage-m1 nhận mã bất kỳ), giữ attempt cũ; chưa chạy thử nên không được coi là đã có. **Đề xuất:** wrapper tiếp nhận ở task mới (không sửa runner T-058 đã ghim), kiểm đúng tình huống thư mục đã tồn tại trước lượt dài. | |
| N1 | Tự tìm — KHÔNG CHẶN (quy trình) | Tôi đọc kết luận REVIEW.md trước khi tự soát lại đầu ra (trái thứ tự AGENTS §5.7); sau đó kiểm từng điểm trên file thật. Ghi nhận để Minh biết mức độc lập của phần đáp này. | |
| N2 | Tự tìm — liên quan R1 của REVIEW-G1 | Quy tắc `thanh_phan_tiem = accept[0]` trong `e2.py::buoc_4` là nguồn gốc dữ liệu khiến trang phát lại gọi một đầu cạnh là "đáp án" (ca `f728fce2`: api-gateway #4 trong khi booking-service #1). Sửa phía E2 nên đi cùng F1–F4 của G1 (ví dụ bỏ `thanh_phan_tiem` hoặc để `null` khi root là cạnh). Chờ Minh. | |
| N3 | Tự tìm — KHÔNG CHẶN | Kiểm vận hành Grafana thật (Codex, `results/T-062/codex/G1-that-ketqua.md`): 47/47 liên kết Explore ở bảng bằng chứng bị mã hóa URL hai lần → "Could not parse Explore URL". Báo cáo sáng §3 nói liên kết Explore dùng được — chỉ đúng với liên kết ở menu nút. Thuộc G1; đính chính câu trong báo cáo cùng R1. | |
