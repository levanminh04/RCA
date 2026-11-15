# Phản biện T-062 — lượt 2

- **Người phản biện:** Codex.
- **Công đoạn:** kiểm lại phản hồi và sửa; cổng gần nhất G4.
- **Phạm vi:** phần Claude làm: A1, A2, B1, D1, D2, E1, E2, H1. Không phản biện C1 hoặc nghiệm thu G1.
- **Mốc đối chiếu:** repo RCA so với `c3d27f8a`; bản sửa so với `results/T-062/_ban-1/`.
- **Quyền ghi:** bản trả lời này là nội dung để lệnh gọi lưu bằng `-o` vào `tasks/T-062-dem-chang-1-4/REVIEW-2.md`. Không dùng công cụ ghi file, không sửa LOG/STATE, không commit.

**Đã đọc:** AGENTS, STATE, SPEC, BOI-CANH, CHECKPOINT và LOG T-062; DT18; hướng dẫn của cô; phần MRP, WHY, DECISIONS, LESSONS chi phối công việc; kế hoạch giai đoạn 2; yêu cầu R-01–R-10; quy tắc nhãn T-059; hợp đồng chuyển giao T-043; mã và đầu ra liên quan của T-058, T-061, T-062.

**Tự soát độc lập:** đã đọc nguồn, mã và đầu ra hiện tại, lập nhận xét riêng trước khi mở REVIEW.md và bảng phản hồi. Sau đó đối chiếu bản sửa với bản trước sửa và từng ý kiến cũ.

## Kết luận chung

Bản sửa đã đính chính đúng số FLASH, bỏ kết luận báo động giả chưa hợp lệ, bổ sung ma trận baseline/D14 và sửa khẳng định phục hồi lượt chạy. Chín kết quả M1 hiện tại vẫn hợp lệ cho kết luận mô tả của lượt phát triển đầu.

**Chưa đề nghị duyệt nguyên đề xuất chặng 4.** Luật chọn còn bỏ sót lỗi chạy trên ca khỏe, chưa bố trí ca khỏe cho phép kiểm held-out, và chưa thống nhất cách chấm khi ứng viên xếp cạnh chung với nút. R1 và R2 cũng còn phần chưa xử lý hết trong dữ liệu nhãn và trạng thái kiểm chất lượng.

## Các điểm

### R1-tiếp. Dữ liệu phát lại vẫn khẳng định `root = null` khi chưa xác nhận khỏe — CHẶN sử dụng các nhãn này làm đáp án ca khỏe

**Ở đâu:** `results/T-062/e2.py:29–30`; `ket-qua/phat-lai/bang-cham.json#/ca`; bốn file phát lại tương ứng; `bao-cao-sang.md:34–37`.

**Sai gì:** văn bản đã nói đúng rằng bốn ca chưa được xác nhận khỏe. Nhưng dữ liệu chấm vẫn ghi:

```text
00eaea92: root = null (tải tăng khỏe)
6c1a9fd8: root = null (ca bình thường)
a5539fba: root = null (ca bình thường)
e8661e0a: root = null (ca bình thường)
```

Nguồn T-059, `danh-muc-loi.json#/label_rules/5`, chỉ cho gán `root = null` sau khi đạt ngưỡng backend khai trước và checks độc lập. “Không tiêm lỗi mới” chưa xác nhận điều đó.

**Bằng chứng:** đọc trực tiếp `bang-cham.json` và `e2.py::DAP_AN`. Bảng chấm hiện tại trùng byte bản trước sửa; bốn file phát lại của nhóm này cũng trùng byte bản trước sửa.

**Phần có thể phản bác finding:** báo cáo, bảng tổng hợp và đề xuất đã cảnh báo rõ; chưa thấy bản sửa dùng bốn ca này để tính K. Vì vậy không còn căn cứ giữ nguyên phản đối cũ đối với tỷ lệ báo động giả trong phần diễn giải.

**Hậu quả:** lỗi nhãn còn tồn tại ở E2. Một bước chấm sau đọc trường `root` vẫn có thể nhận nhầm đây là đáp án hệ khỏe. Không ảnh hưởng hạng của năm ca tiêm lỗi hoặc việc giữ nguyên chín đầu ra M1.

**Sửa tối thiểu đề xuất:** giữ riêng thông tin “không tiêm lỗi mới”; đánh dấu đáp án sức khỏe chưa xác nhận thay cho khẳng định `root = null`. Cập nhật các trường và bảng dẫn xuất tương ứng, giữ bản cũ. Không chạy lại M1. Phương án chỉ thêm chú thích trong báo cáo nhỏ hơn nhưng không sửa được ý nghĩa trường dữ liệu.

### R2-tiếp. R-05 vẫn trả ĐẠT đầy đủ khi phần định danh/binding chưa kiểm — KHÔNG CHẶN kết quả M1 hiện tại

**Ở đâu:** `kiem-du-lieu/kiem-r.py:95–129`; `r-a5539fba.json#/R/R-05`; `bao-cao-B1.md:17`.

**Sai gì:** bản 2 đã thực sự kiểm instance trong thân log với trace. Nhưng nó coi trường hợp không kiểm được instance metric là đạt điều kiện tổng:

```python
c_ = not any(khop_metric.values())
'dat': 'DAT' if a and b_ and c_ else 'THIEU'
```

Khi không có đối tượng được đối chiếu, `khop_metric` rỗng và `c_` vẫn đúng. Host mới được kiểm hiện diện, chưa đối chiếu binding với manifest.

**Bằng chứng hiện tại:**

```text
#/R/R-05/dat = DAT
#/R/R-05/so_do/c_metric_instance
  = “không có nhãn service_instance_id trong các kênh metric M1 dùng”
#/R/R-05/so_do/KHONG_KHOP_RESOURCE_LOG
  = có lệch ở gateway, payment, ticket
```

Báo cáo cũng ghi bảng service→instance→host theo thời gian chưa kiểm.

Câu “các kênh metric M1 dùng không có nhãn instance” còn quá rộng: `prometheus.json` có năm chuỗi `db-size` mang `service_instance_id`. Bộ kiểm bỏ chúng khỏi đối chiếu instance vì không có `service_name`; đây là thiếu phép nối theo loại thực thể, không phải không tồn tại nhãn.

**Phần có thể phản bác finding:** phép nối thân log↔trace của ba service có log là đúng. Đếm độc lập trên gói `a5539fba` được 7.500/7.500 log B16 nối đúng cặp trace/span; instance thân log của nhóm này khớp trace. Không có căn cứ gọi toàn bộ định danh đã hỏng.

**Hậu quả:** B1 chưa chứng minh đầy đủ R-05 của nguồn P9. Trạng thái ĐẠT vẫn mạnh hơn phép kiểm đã thực hiện. Không có bằng chứng việc này làm sai chín hạng M1 hiện tại.

**Sửa tối thiểu đề xuất:** báo tổng R-05 là một phần/chưa kiểm đủ; giữ kết quả đạt của từng phép con. Nêu đúng nhóm metric đã kiểm và nhóm chưa nối được. Đây là cách sửa ít nhất trên dữ liệu sẵn có. Hoàn thiện binding là phương án khác, cần phạm vi riêng; chưa cần thu lại chiến dịch.

### R6. Tiêu chí K có thể thưởng lỗi chạy và không kiểm được trên held-out hiện ghi — CHẶN duyệt luật chọn

**Ở đâu:** `spec-chang-4-de-xuat.md:30–35,67–75`.

**Sai gì:** có hai khoảng trống trong cùng tiêu chí ca khỏe.

Thứ nhất, ERROR/UNSUPPORTED chỉ được quy định là trượt ở **X**, trên ca lỗi. **K** chỉ đếm `CAUSE_FOUND` trên ca khỏe. Chưa có quy tắc ngăn một bản lỗi trên ca khỏe được nhận là cải thiện K.

Phản ví dụ logic đã tính trong bộ nhớ, không phải kết quả thực nghiệm:

| Đại lượng | Bản gốc | Bản ứng viên |
|---|---:|---:|
| AC@3 trên 18 ca lỗi | 18 | 18 |
| Sáu ca khỏe | sáu `CAUSE_FOUND` | sáu `ERROR`, verdict rỗng |
| K theo định nghĩa hiện tại | 6 | 0 |

Nhánh giữ thành phần số 2 chấp nhận sự thay đổi này. Lỗi có thể tất định và trả nhanh nên điều kiện trùng SHA/thời gian không tự loại được nó.

Thứ hai, hàng held-out chỉ có một lặp mới cho **mỗi ô lỗi**, tổng 6 hoặc 5 ca. Nhưng dòng 75 yêu cầu kiểm cả AC@3 **và K** trên held-out. K được định nghĩa trên ca khỏe; tập held-out hiện ghi không có ca khỏe.

**Phần có thể phản bác finding:** §5 đã yêu cầu ngưỡng sức khỏe trước khi đo K. Điều đó xác nhận tình trạng của dữ liệu, nhưng không quy định cách chấm lỗi phương pháp. Sáu ca khỏe dev đã bố trí đều dùng để chọn, chưa được khai là tập giữ lại.

**Hậu quả:** mâu thuẫn thiết kế trước thực nghiệm, chưa phải bằng chứng đã chọn sai biến thể. Nếu duyệt nguyên văn, có thể chọn một bản giảm khả năng trả kết luận hợp lệ hoặc báo đã kiểm K độc lập khi chưa có mẫu phù hợp.

**Sửa tối thiểu đề xuất:** giữ mục tiêu chọn theo X và K, nhưng khai trước cách xử lý ERROR/UNSUPPORTED/thiếu bằng chứng trên ca khỏe; không tính lỗi chạy là bằng chứng kết luận khỏe đúng. Bố trí phần ca khỏe giữ lại để kiểm K sau chọn, có thể phân bổ từ số ca đã dự kiến và tính lại chi phí.

Mặt trái của việc chia số ca hiện có là giảm mẫu dùng để chọn. Phương án khác là held-out chỉ kiểm X và khai K chưa được kiểm trên tập giữ lại; khi đó phải thu hẹp kết luận tương ứng.

### R7. C4-a xếp cạnh cùng nút nhưng luật chọn chỉ chấm nút — CHẶN duyệt phần chọn C4-a

**Ở đâu:** `spec-chang-4-de-xuat.md:41,51,67`; T-059 `danh-muc-loi.json#/label_rules/2`.

**Sai gì:** C4-a dự kiến “cờ cạnh được xếp hạng cùng nút”. Ma trận lại yêu cầu tập ứng viên giống nhau; X chỉ lấy hạng tốt nhất trong tập nút chấp nhận T-059. Chưa quy định cách chiếu danh sách hỗn hợp cạnh–nút về bảng xếp hạng thực thể chung, hoặc cách đo lợi ích tìm đúng cạnh.

**Phản ví dụ logic:** trên NET-GW-BOOK, một bản trả đúng cạnh `api-gateway→booking-service` ở hạng 1, Booking ở hạng 2. Nếu dùng trực tiếp hạng danh sách hỗn hợp, X chỉ thấy Booking hạng 2 và không ghi nhận việc tìm đúng cạnh. Trong khi đó P7 chỉ xếp nút, Booking đang hạng 1.

T-059 đã yêu cầu tách ba phần: khớp root thật; định vị qua tập nút chấp nhận chung; định vị cạnh với định danh/binding. Không có đầu ra cạnh thì ghi UNSUPPORTED cho phần tương ứng.

**Phần có thể phản bác finding:** bản đề xuất đã phân biệt đúng điểm nút với tìm đúng cạnh ở §1b. Nhưng phân biệt đó chưa đi vào luật chọn và bảng đầu ra. Đây là đề xuất chưa chạy, không phải lỗi điểm hiện tại.

**Hậu quả:** chưa có phép so tương đương để chọn thành phần mở rộng sang cạnh. Có thể loại cải thiện đúng mục tiêu chỉ vì thay loại đối tượng được xếp hạng.

**Sửa tối thiểu đề xuất:** áp đúng các bảng chấm đã có trong T-059; khai quy tắc lấy hạng thực thể chung khi có cạnh trong đầu ra, và đại lượng cạnh nào tham gia chọn C4-a. P7 giữ UNSUPPORTED ở phần không hỗ trợ cạnh. Phương án chỉ chọn bằng điểm thực thể vẫn khả thi, nhưng phải bỏ mục tiêu dùng luật ấy để chọn lợi ích định vị cạnh.

### R8. Mốc FLASH lệch lịch k6 khoảng 21 giây — KHÔNG CHẶN giữ kết quả mô tả hiện tại

**Ở đâu:** `chay/runner.py:87,174,182`; `chay/k6/workload-t062-flash.js:38`; `chay/k6-theo-pha.py`; ca `00eaea92`.

**Sai gì:** k6 tự chuyển pha sau 600 giây từ lúc scenario bắt đầu. Runner chờ 20 giây kiểm k6 còn sống, rồi mới đặt `S`; tiếp đó ghi mốc FLASH bằng `S+600`. Hai đồng hồ pha không cùng gốc.

**Bằng chứng từ dữ liệu đã lưu:**

```text
request.json#/t: 2026-11-12T00:28:19Z
http_req_duration nghiệp vụ đầu tiên:
  hoàn thành khoảng 00:17:58.418Z
  bắt đầu request suy từ duration khoảng 00:17:58.149Z
Khoảng cách tới t: khoảng 620,85 giây.
```

Điều này phù hợp với đoạn chờ 20 giây trong code. Vì vậy cửa sổ được gọi là nền chứa khoảng 21 giây đầu của ramp; cửa sổ hồi phục không phủ đủ pha k6.

Đếm lại theo **đúng t hiện tại** vẫn khớp bản sửa:

| Pha theo t | Request | 429 | 500 |
|---|---:|---:|---:|
| Nền | 3.037 | 0 | 300 |
| Giữa | 8.360 | 244 | 840 |
| Hồi phục | 2.895 | 0 | 287 |

**Phần có thể phản bác finding:** số trong bảng không sai đối với các khoảng `[t−600,t)`, `[t,t+600)`, `[t+600,t+1200)`. Toàn bộ 244 phản hồi 429 vẫn nằm ở pha giữa. Finding không khôi phục kết luận “FLASH khỏe”, cũng không bác bỏ việc tải tăng.

**Hậu quả:** lỗi điều phối đã xảy ra. Không nên gọi các khoảng này là ba pha k6 căn đúng 10/10/10, hoặc dùng cửa sổ nền ấy như đoạn chưa tăng tải để hiệu chuẩn.

**Sửa tối thiểu đề xuất:** đính chính cách gọi cửa sổ của lượt cũ; giữ nguyên request và đầu ra M1. Trước lượt mới, lấy mốc FLASH từ cùng gốc thời gian scenario k6 và lưu mốc đó. Nếu cần bảng pha k6 chính xác cho lượt cũ, tính riêng từ dữ liệu tải đã lưu; không trình như chạy lại độc lập M1.

## Đối chiếu các lượt trước

| Điểm | Đánh giá độc lập | Trạng thái sau sửa |
|---|---|---|
| R1 | **Đúng.** Đếm lại FLASH khớp 7.276×200, 244×429, 840×500 trong pha giữa theo t; ba lượt rơi. | Diễn giải đã sửa đúng. Nhãn `root = null` còn tồn tại: R1-tiếp. |
| R2 | **Đúng.** Bản cũ chỉ kiểm hiện diện host. | Bản mới cải thiện thật nhưng chưa hoàn tất; R2-tiếp. |
| R3 | **Đúng.** Luật cũ loại thành phần chỉ cải thiện ca khỏe; mẫu số cũ sai. | Hai hướng và mẫu số 18/15 đã sửa. Còn khoảng trống K tại R6. Không có bằng chứng đã chọn biến thể bằng luật sai. |
| R4 | **Đúng.** P7 không thay thế baseline của kế hoạch nguồn. | Đã bổ sung baseline, D14 và giới hạn kết luận. Danh sách bắt buộc, adapter và chi phí còn chờ quyết; đây chưa là hồ sơ phát lượt đầy đủ. Không yêu cầu chạy baseline trong phiên phản biện này. |
| R5 | **Đúng.** `stage-m1.py` và `run-m1.py` dùng `exist_ok=False`; runner không nhận lại attempt dở. | Đã sửa đúng trạng thái tài liệu: chưa có phục hồi đã kiểm, wrapper là điều kiện của lượt sau. Không coi đường phục hồi đã được cài. |
| N1 | **Đúng về việc tự khai.** LOG và phản hồi nhận đã đọc kết luận trước tự soát. | Không thể dùng phiên đáp ấy làm bằng chứng độc lập; các kiểm trực tiếp của lượt này không phụ thuộc việc tự khai đó. |
| N2 | **Đúng.** Lấy phần tử đầu tập chấp nhận làm đáp án cạnh là sai nghĩa. | Hai ca cạnh hiện có `thanh_phan_tiem = null`; giữ đầy đủ root và tập chấp nhận. Phần dữ liệu E2 đã sửa đúng. |
| N3 | **Chưa kiểm được trạng thái G1 mới nhất trong lượt này.** | Báo cáo đã phân biệt menu nút với bảng bằng chứng và ghi chờ kiểm thật. Không coi đây là nghiệm thu Grafana bản mới. |

## Tuân thủ quy trình

- Giữ vai trò phản biện phần Claude làm. Không tự phản biện C1, không mở phiên hoặc gửi cho agent khác.
- Quyền sửa R1–R5/N2 được Minh xác nhận trong yêu cầu lượt này. Các thay đổi đã đối chiếu phù hợp nhóm file được nêu; không có bằng chứng đủ để quy một thay đổi ngoài phạm vi cho gói sửa này.
- Bản trước sửa có 23 file, được giữ trong `_ban-1/`. Manifest hiện tại kiểm khớp các bản đó. Không có manifest cũ riêng trong `_ban-1/` để xác nhận thêm thời điểm sao lưu.
- Việc đổi phép kiểm host của metric sau kết quả lần đầu được khai rõ. Tuy nhiên, khai sửa sau không biến phần chưa kiểm thành ĐẠT đầy đủ.
- STATE còn mô tả “chưa sửa, chờ Minh”; LOG mới nhất đã ghi sửa. Yêu cầu trực tiếp của Minh xác nhận trạng thái mới, nên không dùng dòng STATE cũ để suy rằng chưa được duyệt sửa. Reviewer không sửa STATE.
- Không thấy thay code lõi M1 theo kết quả T-062. Chưa có bằng chứng đổi thiết kế sau khi dùng dữ liệu test trong gói đang xét.
- **Hash lệch:** 567/568 mục manifest T-062 khớp; mục lệch là `codex/phan-bien-T062-luot2-prompt.txt`. Đã loại file này khỏi bằng chứng. Không thấy lệch ở các gói ca và kết quả được dùng trong nhận xét trên.

**Ảnh hưởng khi sửa tiếp:** các file T-062 nêu trong finding đều đang được manifest ghim. Sửa code, báo cáo hoặc dữ liệu dẫn xuất sẽ đổi hash tương ứng và cần manifest mới, giữ lịch sử. Không cần sửa runner T-058 hoặc code P7 đã ghim để xử lý các đề xuất trong bản này. Các đề xuất không tự cấp quyền sửa.

## Điều đã kiểm và thấy đúng

1. **Pin và toàn vẹn:** 39 pin code khớp. Adapter/config/pin của T-062 khớp plan T-058. Plan, stage, run và đầu ra đối chứng T-058 được dùng đã kiểm khớp artifact manifest. Nguồn R-01–R-10 của T-040 và bảng chuyển giao T-043 khớp manifest tương ứng.
2. **Chín ca:** 45 file trong manifest ca khớp; chín hash đầu vào M1 khớp summary; chín cặp đầu ra trùng hash, đều `OK`. Chín kết quả 0.2 khớp manifest kết quả.
3. **Giữ kết quả chính:** bỏ khối `phat_lai` khỏi bản phát lại trước sửa thì nội dung khớp bản kết quả chính hiện tại ở cả chín ca. Bản sửa không đổi nội dung chẩn đoán chính được kiểm theo cách này.
4. **Sổ:** chuỗi 173 dòng không đứt.
5. **Cách ly nhãn:** đường stage/run chỉ đưa đầu vào cho phép vào M1. Quét chín `method-input.json` không thấy mã ca, tên ô hoặc các dấu công cụ tiêm đã kiểm. Mốc t là đầu vào chế độ a được phép.
6. **B1:** đếm độc lập 7.500 log B16 nối đúng cặp trace/span; 6.000 log Gateway nối đúng span SERVER Gateway. Phần cải thiện nối log được dữ liệu hỗ trợ.
7. **Vai trò cạnh:** NET-GW-BOOK có bằng chứng `canh|api-gateway|booking-service`; E2-C gán cho Booking; Booking hạng 1. Không diễn giải thành M1 hoàn toàn không dùng cạnh.
8. **Trung gian ca không tiêm:** thành phần đầu có các kênh tầng 1 thực sự, gồm thao tác nền ở Keycloak/Event và workload/thao tác Payment ở FLASH. Điều này bác bỏ giải thích “chế độ a luôn buộc có nguyên nhân”; chưa xác định nguyên nhân riêng của từng cờ hoặc lợi ích của một sửa thiết kế.
9. **Giới hạn công cụ:** `py` không có trong PATH; launcher Python của venv không khởi động được trong sandbox. Đã dùng Node để băm, đọc JSON/JSONL và đếm độc lập. Không chạy lại M1, không thu dữ liệu mới, không đọc dữ liệu khóa.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm:** tự soát nguồn và đầu ra; đối chiếu bản sửa, phản hồi R1–R5/N1–N3; kiểm pin, gói ca, nhãn, trung gian và tiêu chí chọn.
2. **File thay đổi:** không sửa file nào bằng công cụ. Bản này là đầu ra dành cho `REVIEW-2.md` qua `-o`.
3. **Kiểm và kết quả:** các kiểm toàn vẹn, tất định, nối log và đếm FLASH đạt như trên; một file prompt lệch hash đã được loại khỏi bằng chứng.
4. **Phần còn mở và Minh cần quyết:** T-062 hỗ trợ việc chạy P7 trên lượt phát triển đầu, chưa trả lời RQ5 hoặc hiệu quả trên ca khỏe. Đề nghị Minh giữ chín kết quả chính; yêu cầu người làm đáp các điểm còn lại trước khi duyệt kế hoạch chạy tiếp. Ưu tiên sửa ý nghĩa nhãn, trạng thái R-05 và luật chọn trên dữ liệu/tài liệu sẵn có. Chưa cần phát thực nghiệm mới để phân xử các finding này.

**Đề xuất tiếp tục một lượt người làm đáp.** Còn phản đối có bằng chứng ảnh hưởng trực tiếp tới nhãn và kế hoạch đang xin duyệt. R4/R5 không còn bị phản đối theo nội dung cũ; những phần baseline và phục hồi chưa thực hiện vẫn là phụ thuộc của lượt sau. Minh quyết sửa, chấp nhận giới hạn hoặc dừng. Không tự đóng task, duyệt SPEC hoặc mở test.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-062, tasks/T-062-dem-chang-1-4/; phần Claude làm A1, A2, B1, D1, D2, E1, E2, H1; results/T-062/bao-cao-sang.md và results/T-062/spec-chang-4-de-xuat.md. Đánh giá cả các đề xuất trong bản phản biện lượt 2. C1 và G1 ngoài phạm vi chính của lượt này.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: kế hoạch giai đoạn 2 chặng 1a, 2, 3, 4 lượt đầu và nhánh G; cổng gần nhất G4.
- Người làm và người phản biện chính thức: Claude làm phần thuộc phạm vi trên; Codex làm C1. Minh giao Codex phản biện phần Claude làm trong chat 12/11/2026.
- Tài liệu gốc: tasks/T-062-dem-chang-1-4/{SPEC,BOI-CANH,LOG,CHECKPOINT,PROMPT-DIEU-PHOI}.md; docs/techstack/KE-HOACH-GIAI-DOAN-2.md; results/T-059/danh-muc-loi.md và .json; results/T-040/yeu-cau-quan-sat-p9.md; results/T-043/bang-chuyen-giao.json; tasks/T-043-thiet-ke-rca-m1/SPEC.md; results/T-061/dinh-dang-ket-qua-rca.md; repo RCA so với c3d27f8a; lịch sử nhánh rca/quan-sat-log trong D:/Project/flash-ticket-platform.
- Phản biện và phản hồi trước: tasks/T-062-dem-chang-1-4/REVIEW.md gồm bảng phản hồi; bản phản biện lượt 2 trong REVIEW-2.md hoặc nội dung chat do Minh chuyển; các mục LOG ngày 12/11/2026.
- Code và kết quả liên quan: results/T-062/manifest.json; results/T-062/_ban-1/; ha-tang/, kiem-du-lieu/, tiem-loi/, chay/, ca/, ket-qua/, e2.py, bang-ket-qua.py và dữ liệu tải E1; results/T-058/dem-2026-11-10/{stage-m1.py,run-m1.py,m1-execution-plan-v2.json,artifacts-sha256.json}; src/m1/; results/T-061/chuyen-doi.py. Môi trường Python theo hướng dẫn repo; chỉ chạy phần đọc hoặc phân tích trong quyền đã duyệt.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat nếu Minh chưa cấp thêm quyền cụ thể cho lượt đáp; không tự sửa kết quả, code, SPEC, LOG, STATE hoặc nội dung phản biện.

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

## Phản hồi của người làm

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R1-tiếp | **Đúng.** CHẶN dùng nhãn này làm đáp án ca khỏe. | `e2.py::DAP_AN` dòng 29–30 vẫn ghi `root = null (…)` cho BINH-THUONG/FLASH; `bang-cham.json` và 4 file phát lại mang nhãn đó. T-059 `label_rules/5` chỉ cho `root = null` sau khi đạt ngưỡng khỏe. **Đề xuất sửa:** đổi đáp án nhóm này thành "không tiêm lỗi mới — sức khỏe chưa xác nhận (T-059 chưa có ngưỡng)", thêm trường `suc_khoe: chua_xac_nhan`, không dùng chữ `root = null`; sinh lại phát lại/bảng chấm/chỉ mục (kết quả chính không đổi), giữ bản cũ ở `_ban-2/`. | |
| R2-tiếp | **Đúng.** KHÔNG CHẶN. | `c_` đúng một cách rỗng khi không có gì để đối chiếu; host mới kiểm hiện diện. Câu "kênh metric không có nhãn instance" sai: 5 chuỗi `db-size` có `service_instance_id` (instance PostgreSQL chung) nhưng không có `service_name` nên bị bỏ. **Đề xuất sửa:** R-05 trả `MOT_PHAN` khi (c) hoặc binding chưa kiểm; ghi đúng "metric dịch vụ không mang instance; metric DB có instance của PostgreSQL chung, chưa nối theo loại thực thể"; giữ kết quả từng phép con. | |
| R6 | **Đúng.** CHẶN duyệt luật chọn. | Phản ví dụ hợp lệ: bản trả ERROR trên ca khỏe làm K giảm. Held-out không có ca khỏe nên không kiểm được K. **Đề xuất sửa:** trên ca khỏe, ERROR/UNSUPPORTED/INSUFFICIENT_EVIDENCE tính là *không đạt* (K' = số ca khỏe **không** trả `NO_INTRINSIC_ANOMALY`); tách 2 trong ≥ 6 ca khỏe làm held-out (chọn trên 4) hoặc thêm 2 ca khỏe (+1 giờ máy). Đề xuất thêm 2 ca để không giảm mẫu chọn. | |
| R7 | **Đúng.** CHẶN phần chọn C4-a. | Luật X chỉ chấm nút; chưa có quy tắc chiếu danh sách hỗn hợp cạnh–nút. **Đề xuất sửa:** áp ba bảng chấm T-059 `label_rules/2`: (i) X-nút = hạng tốt nhất của **thực thể** trong tập chấp nhận sau khi chiếu mỗi cạnh về hai đầu (cạnh hạng k → hai đầu nhận hạng k nếu chưa có hạng tốt hơn); (ii) X-cạnh = hạng của đúng cạnh root trong danh sách cạnh (P7: UNSUPPORTED); C4-a được giữ nếu X-nút không giảm và X-cạnh từ UNSUPPORTED thành có hạng ≤ 3 trên ≥ một nửa ô cạnh. Minh duyệt ngưỡng. | |
| R8 | **Đúng.** KHÔNG CHẶN kết quả mô tả. | `runner.py:87` `sleep(20)` trước `S = time.time()` (dòng 174): mọi chu kỳ `S` trễ ~20 s so với lúc k6 bắt đầu. Chỉ FLASH bị ảnh hưởng vì pha do k6 tự đếm; ô lỗi lấy `t` từ lúc bật lỗi thật, ca bình thường không có pha tải. **Đề xuất sửa:** đính chính trong báo cáo (cửa sổ FLASH theo `t` không trùng pha k6, lệch ~21 s); lượt sau lấy `S` từ `start-utc.txt` của k6 (cùng gốc) và lưu mốc ramp. Không chạy lại M1. | |

**Cập nhật người làm (12/11, sau khi Minh duyệt sửa cả 5 điểm):** đã sửa R1-tiếp (`e2.py` bản 3: nhãn "không tiêm lỗi mới — sức khỏe chưa xác nhận", trường `suc_khoe`; phát lại/bảng chấm/chỉ mục sinh lại và đẩy; 9 kết quả chính không đổi byte), R2-tiếp (`kiem-r.py` bản 3: R-05 → MOT_PHAN; báo cáo B1), R6 + R7 (`spec-chang-4-de-xuat.md` bản 3: K', 2 ca khỏe held-out, X-cạnh theo T-059), R8 (`chay/runner.py` bản 3: S lấy lúc k6 chạy; đính chính FLASH trong `bao-cao-sang.md`). Bản trước ở `results/T-062/_ban-2/`.
