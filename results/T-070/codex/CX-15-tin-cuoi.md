**Đề nghị Minh cho Claude đáp thêm một lượt trước khi khóa W7.** Bản 3 đã sửa đúng phép che liveness của D14, bỏ hai suy luận nhân quả thiếu căn cứ và tính đúng tám phương án thu. Còn bốn điểm có thể làm đổi ca được giữ, mẫu số phát hiện hoặc điểm baseline dù người triển khai làm đúng theo hồ sơ. Các điểm này xử lý được ở mức thiết kế, không cần phát lượt máy mới.

### Các điểm còn ảnh hưởng đến quyết định

**1. CHẶN khóa quy tắc giữ ca và thay lượt.** §B.2 coi `fault-start-failed` là bằng chứng “chưa có can thiệp”. Ở revision `407b4f5`, `runner4.py` ghi sự kiện này cho mọi ngoại lệ của `inj('start', …)`. Ngoại lệ có thể xảy ra khi chờ hoặc giải mã phản hồi sau khi máy đích đã thực hiện thao tác. Trong trường hợp đó, `fault_ok` là `False` và runner bỏ qua lệnh `stop` thông thường. Với ô mới `TICKET-PAUSE`, hậu quả còn lan sang chu kỳ sau: đầu dò `payment_state`, phép kiểm trạng thái sạch và nhánh gỡ pause quá hạn hiện đều chỉ đích danh **Payment**. Thêm một mục Ticket vào bảng ô như §4.2 chưa đủ để xác nhận Ticket đã chạy lại. Đây là đường lỗi có thể xảy ra trong thiết kế. Tôi không thấy bằng chứng nó đã xảy ra ở W7. [Quy tắc bản 3](D:/RCA-flashticket/results/T-074/thiet-ke-w6-3.md:47) · [Runner](D:/Project/flashticket-rca-lab/campaigns/runner/runner4.py:270) · [Bộ tiêm và phép kiểm trạng thái sạch](D:/Project/flashticket-rca-lab/faults/injectors/docker/inj3.py:284)

**Đề xuất Minh:** chỉ bù theo nhánh “chưa tiêm” khi đầu dò hoặc nhật ký đích xác nhận điều đó. Nếu chỉ mất phản hồi, giữ lượt ở nhóm chưa xác nhận và dùng bằng chứng trên đúng container để quyết định có thể bắt đầu chu kỳ kế tiếp hay chưa. Gói code W7 cần tính cả phần dò, xác nhận sạch và gỡ pause của Ticket. Cách này có thể để lại một ô thiếu lần lặp. Tự động bù ngay thì có nguy cơ đếm lại một can thiệp đã diễn ra.

**2. CHẶN khóa mẫu số ở tải ×3 cố định.** §B.3 đề xuất dùng nguyên bộ phân loại T-071. Tuy nhiên `phan_loai_phut.py:189` chỉ đặt `muc='x3'` khi có `buoc_tai` và đã qua mốc tăng bậc. W7 lại chủ ý chạy ×3 **ngay từ đầu**, không tăng bậc, để thay đổi tải không trùng mốc tiêm. Nếu tái dùng nguyên code, phút của chu kỳ ×3 cố định đi vào nhánh ×1 và có thể nhận nhãn `khoe_x1`. Điều đó làm sai cả tử số lẫn mẫu số, kể cả khi dùng cách gọi mới “sự cố trên giờ quan sát ×3”. Ngoài ra, §8.4 vẫn đòi phần nền N khỏe để nhận ca vào mẫu số chính, trong khi §B.3 chưa xác định điều kiện nhận ca ×3 này. [Thiết kế tải](D:/RCA-flashticket/results/T-074/thiet-ke-w6-2.md:171) · [Quy tắc bản 3](D:/RCA-flashticket/results/T-074/thiet-ke-w6-3.md:57) · [Code phân loại phút](D:/RCA-flashticket/results/T-071/phan_loai_phut.py:189)

**Đề xuất Minh:** giữ Q-W6-10(a). Lấy mức tải của từng phút từ hệ số khởi đầu và bậc tải trong lịch thực chạy. Chỉ dùng `khoe_x1` cho phút ×1. Với ×3, khai riêng điều kiện nhận phần N bằng bằng chứng tải và hạ tầng độc lập, rồi báo số sự cố trên giờ quan sát đủ điều kiện. Phải nói rõ phút ×3 nào vào Precision và phút nào chỉ báo mô tả. Phương án định nghĩa `khoe_x3` vẫn khả thi nhưng cần căn cứ riêng cho tiêu chí khỏe.

**3. CHẶN khóa adapter baseline.** Có hai chỗ trong hợp đồng đầu vào vẫn cho phép cho ra kết quả khác nhau.

- **Biên N/A.** §C.3 quy định lấy mẫu native muộn nhất trong ô lưới 15 giây, rồi §7.1 chia N/A theo thời gian của hàng. Hồ sơ chưa quy định gốc lưới hoặc yêu cầu chia theo mốc native trước. Tôi đọc đủ các sự kiện `mark` và `fault-start` trong sổ lượt chính T-069. **14/17 mốc** có `t % 15 ≠ 0`. Ví dụ ca `03573b63` có `t=1795085304`. Với lưới neo theo epoch, mẫu đúng `t` rơi vào hàng `1795085295 < t`. BARO có thể học nền bằng một mẫu thuộc sự cố. Đây là phản ví dụ cho quy ước, chưa phải kết quả baseline đã chạy. **Sửa tối thiểu:** cắt bằng thời gian native theo hai khoảng nửa mở, rồi dựng lưới neo tại `t` hoặc `t̂` trong từng nửa. Với BARO, giữ thứ tự điền theo quy ước P3 sau khi đã xác định đúng hàng. [Quy ước lưới](D:/RCA-flashticket/results/T-074/thiet-ke-w6-3.md:81) · [Sổ nguồn, trường `event`, `opaque_id`, `t`](D:/RCA-flashticket/results/T-069/thu/t069-chinh/so.jsonl) · [BARO chia cửa sổ](D:/RCA-ext/src/RCAEval/RCAEval/e2e/baro.py:23)
- **SimpleRCA nhận cả trace và log.** `normalize_spans` trả `owner`, `start_us`, `duration_us`. `normalize_logs` trả `entity`, `timestamp` theo **nano giây**, cùng `message`. `prepare` đòi `serviceName/startTime/duration` cho trace và `container_name/timestamp/message` với timestamp **giây** cho log. Còn có alias kiến trúc `discovery-server → config-discovery` nằm ngoài bảng alias tiền tố metric của §C.1. Nếu tính điểm trước khi hợp nhất hai tên, bằng chứng trace/log và metric của cùng dịch vụ có thể đã bị tách. Đổi tên lúc trả hạng không khôi phục được điểm gộp. **Sửa tối thiểu:** ghi ánh xạ trường, đơn vị và tên chuẩn trước khi SimpleRCA cộng bằng chứng các nguồn. Dùng quy tắc `ffill` của BARO đúng nhánh của nó. Phần xác nhận động thuộc gói adapter trên dev. [Chuẩn hóa FlashTicket](D:/RCA-flashticket/src/m1/adapter_flashticket.py:215) · [Hợp nhất hai bảng alias](D:/RCA-flashticket/src/m1/adapter_flashticket.py:292) · [Hợp đồng SimpleRCA](D:/RCA-flashticket/src/simplerca/adapter.py:61) · [Adapter P3 nhận metric thô](D:/RCA-flashticket/src/p3/adapters/simplerca.py:1)

**4. CHẶN dùng dự toán hiện tại để duyệt lịch chờ chụp gói (b).** Phép tính cửa sổ **lõi** ở §A đúng: nếu `t̂` gần `S+1570`, lõi cần dữ liệu tới gần `S+1870`, vượt biên chu kỳ khoảng 70 giây. Nhưng §8.2 chọn bộ xuất của T-073. Hồ sơ T-073 đã khóa ghi gói thu `[t̂−600,t̂+600)`, `flush_F=150` và lần bắt đầu chụp dưới tải ×1 ở `t̂+750`. Với cùng cảnh báo muộn, đó là gần **`S+2320`**, tức **520 giây sau biên** tới lúc bắt đầu chụp. §A tính “70 giây + thời gian xả” cho một đường thu khác. Câu bản 2 rằng gói W5 chỉ lùi được 300 giây cũng cần đối chiếu lại khi xét D13. [Thiết kế bản 3](D:/RCA-flashticket/results/T-074/thiet-ke-w6-3.md:20) · [Tuyến T1b](D:/RCA-flashticket/results/T-074/thiet-ke-w6-2.md:308) · [Bản khóa T-073, `#/N/thanh_phan_giay` và `#/N/do_duoi_tai_e3`](D:/RCA-flashticket/results/T-073/khai-truoc-e5.json)

**Đề xuất Minh:** giữ G=370 giây làm cửa sổ ghép chính đề xuất, G=120 giây làm mục tiêu vận hành phụ. Tách ba mốc trong dự toán: hết dữ liệu lõi, hết gói thu và bắt đầu chụp. Nếu cần giữ điều kiện tải đến hết A, chỉ khoảng vượt biên của **A** quyết định thời gian giữ điều kiện đó. Nếu runner phải đợi bộ xuất, tính theo lịch chụp thật. Chụp bất đồng bộ có thể giảm thời gian chờ nhưng phải ghi phần nào trùng chu kỳ sau. Kết quả E3 cho một căn cứ ở ×1. Chi phí và độ đầy đủ ở ×3 vẫn cần số pilot trước khi duyệt lịch.

**5. CHẶN diễn giải RQ5 theo bảng §9.4 hiện tại.** Dòng “sau thích nghi” cho phép kết luận hỗ trợ khi `V082 ≥ P7` ở đa số ô và không ô nào tụt quá hai bậc. Nếu hai bản hòa ở tất cả các ca, kết quả ấy đồng thời thỏa cột “hỗ trợ” và cột “không phân xử”. Cũng không thể suy từ hòa hạng rằng thành phần không kích hoạt. Trong T-069, ở ca `03573b63`, H8s1 đã đổi cờ và phần tử khóa nhưng hạng nút đáp án vẫn bằng nhau. Đây là phản ví dụ đã lưu, có trước W7. **Sửa tối thiểu:** tách kết luận “giữ hạng” khỏi “cải thiện hạng”, và dùng trung gian để xác định thành phần có kích hoạt. Dòng “chuyển thẳng” cũng cần định nghĩa “khoảng của dev” và “tụt rõ” nếu dùng để phân xử. Phương án ít giả định hơn là báo thắng/hòa/thua theo ô và giữ diễn giải mô tả. [Bảng diễn giải](D:/RCA-flashticket/results/T-074/thiet-ke-w6-2.md:399) · [Đính chính T-069, §4](D:/RCA-flashticket/results/T-069/dinh-chinh-1.md) · [Hạng theo biến thể](D:/RCA-flashticket/results/T-069/phan-tich/bien-the/hang.txt)

**6. KHÔNG CHẶN chọn phương án ô. CHẶN dùng nguyên JSON để duyệt ngân sách khi lỗi.** Tôi tính lại độc lập tám dòng `#/phuong_an`. Số chu kỳ, giờ thu cơ sở, đơn bảo thủ và đơn ước hoàn tất đều khớp. Số dư **46.402 vé** đúng theo mô hình tại E1. Tuy nhiên `du-toan-3.json#/thay_cho` giữ hiệu lực các mục cũ ngoài danh sách thay. Vì vậy `du-toan.json#/loi_giua_chung/loi_khoi_phuc_K2` vẫn nói **6–9** chu kỳ, ghi chú mới nói **11–20**, còn bảng theo phương án thực sự cho **9–20**. Mục cũ `#/viec_them/E6_tuy_chon_phan_xu_T069` cũng còn một giờ cho việc §G đã rút. **Sửa tối thiểu:** trong bản kế tiếp, chỉ đích danh các mục hết hiệu lực, lấy kích thước khối từ dòng phương án đã chọn, và tách chi phí chờ gói (b) khỏi giờ thu cơ sở. Không cần tính lại tám dòng đã đúng. [Dự toán bản 3](D:/RCA-flashticket/results/T-074/du-toan-3.json) · [Dự toán được kế thừa](D:/RCA-flashticket/results/T-074/du-toan.json) · [Quyết định rút phép thử trong đề xuất](D:/RCA-flashticket/results/T-074/thiet-ke-w6-3.md:140)

### Đối chiếu các lượt trước

| Điểm | Kết luận độc lập |
|---|---|
| CX-06 #7 | **Đúng, đã xử lý phần chính.** D2 đặt proxy/quota sau E5. R9 đặt việc sửa hạn bán và sức chứa ở E6. K0/K3 vẫn là đề xuất. Riêng mốc 28/11 là đề xuất điều phối theo LOG lượt 3, cần giữ đúng nguồn khi trình Minh. [LOG điều phối](D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/LOG.md:141) |
| CX-06 #8, CX-08 #1 | **Đúng về mâu thuẫn cũ.** Bản 3 tách hai giá trị G, một TP cho mỗi cửa sổ và trạng thái RCA riêng. Phần thời gian chụp còn vướng điểm 4 ở trên. G=370 là quy ước ghép đề xuất theo cấu hình, chưa chứng minh một cảnh báo cuối cửa sổ do lỗi tiêm gây ra. |
| CX-08 #2 | **Đúng một phần ở bản sửa.** Ba lớp thiếu tín hiệu giải quyết được việc quy lỗi chỉ vì cả nguồn rỗng. Nhánh mất phản hồi của bộ tiêm và ×3 cố định vẫn vướng điểm 1–2. |
| CX-06 #9, CX-08 #3 | **Đúng về BARO.** Code tác giả ở `259ea41` bỏ cột hằng riêng từng nửa, lấy giao, rồi lấy max của điểm robust. Adapter local còn bỏ `latency-50`, đổi `latency-90` và điền thiếu. Bản 3 sửa đúng ví dụ IQR=0, alias DB ở đầu ra và phân loại lỗi đa chuỗi. Ca RECREATE-PAY có P7 `ERROR`, V082 `OK` hạng 1 tại `#/hang/16/moi`. Đây là bằng chứng phải tách độ phủ adapter khỏi chất lượng xếp hạng. Hợp đồng thời gian và SimpleRCA còn vướng điểm 3. [Kết quả theo ô](D:/RCA-flashticket/results/T-069/bang-theo-o-chinh.json) |
| CX-08 #4 | **Đúng, đã xử lý ở mức thiết kế.** Tôi đếm `#/extra/kenh_co` theo 17 `ma_moi`: ba ca có `live-ms` là `c446b6ae`, `81af0b51`, `c4d7999f`. §E nay che cả `live-down`, `live-ms` và ghi đè H5b, đồng thời giữ file bổ sung đúng mốc. Phép kiểm dev với `result=[]` vẫn chờ gói code như đã khai. [Danh sách ca](D:/RCA-flashticket/results/T-069/bang-theo-o-2.json) · [H5](D:/RCA-flashticket/src/m1_ft/thanh_phan/h4_h5.py:93) |
| CX-08 #5 | **Đúng về số học và ba khối.** D1, E3, hai phương án ô mốc và mốc K2 sau sửa đã vào bản 3. Còn mâu thuẫn hiệu lực JSON ở điểm 6. |
| CX-08 #6 | **Đúng, đã xử lý phần khoa học.** So BARO–V082 đổi đồng thời nguồn tín hiệu, tiền xử lý và xếp hạng. Dữ liệu cũ cũng chưa tách DB, cache, CPU và thay đổi đường mua. §G đã hạ hai kết luận xuống mô tả. Không cần thêm hai chu kỳ E6 để đóng lượt này. |
| CX-08 #7 | **Đúng, đã xử lý phần tồn tại dữ liệu.** Tôi đọc bản ghi `Point` của `http_req_duration` có `time`, `value`, `route`, `routeId`, `status`, `step`. Dữ liệu cho phép thiết kế offline. Chưa có quy tắc onset, số request tối thiểu hay ánh xạ dự đoán vùng về endpoint để tính độ đúng. Đề nghị giữ độ trễ theo mốc tiêm là số chính. [Gói k6 đã lưu](D:/RCA-flashticket/results/T-069/thu/t069-chinh/tai-out/t3-124242f0/raw.json) |
| RQ3d | **Đúng về giới hạn, chưa được giao sửa.** Nút là thực thể, kênh metric/log/trace mang bằng chứng về thực thể. `DC-bo-quan-he` giữ đầu vào rồi đổi E1/E2/E5. C-d1 dùng cạnh gọi giữa các nút có cờ. C-d2 xếp theo khởi phát và khóa nút. C-d3 dùng đường có hướng, có trạng thái `NO_TARGET` và `UNSUPPORTED_CYCLIC`. Phép so chỉ hỗ trợ kết luận về các bước dùng quan hệ trong **xếp hạng**. Phát cảnh báo bằng luật Grafana, độ đúng vùng và ưu thế của topology thật là các câu riêng. **KHÔNG CHẶN nghiệm thu phần sửa CX-08 #1–7 vì RQ3d.** Đề nghị giữ kết luận rộng OPEN, chỉ giao sửa §3.4/W6-M nếu Minh muốn dùng kết luận ấy trong hồ sơ khóa. [Đối chứng V082](D:/RCA-flashticket/src/m1_ft/thanh_phan/dc_bo_quan_he.py) · [C-d1–d3](D:/RCA-flashticket/src/m1/doi_chung.py) |

### Kết thúc lượt

1. **Đã làm.** Soát bản 3 theo SPEC, §8.3, MRP, DT18 và hướng dẫn của cô. Hồ sơ đạt phần **liệt kê thiết kế, phương án, dự toán và câu hỏi cho Minh**. Phần **quy tắc có thể khóa để hai người triển khai và chấm giống nhau** còn thiếu ở các điểm trên. Các WHY ở §D có trạng thái đề xuất đúng phạm vi. Việc ghi WHY chính thức cần Minh duyệt trước thu. Ở đường đã đọc, sổ và nhãn nằm phía điều phối/chấm, chế độ (b) lấy `t̂` từ cảnh báo. Chưa có adapter và runner W7 hoàn chỉnh để xác nhận điều này đầu cuối.
2. **File thay đổi.** Không sửa file nào, không commit, không SSH, không mở dữ liệu khóa, không chạy thực nghiệm. Bản 3 và các đầu ra được kê nằm trong phạm vi T-074. Checkout dùng chung, hồ sơ chưa commit, nên `git status` không đủ để quy từng thay đổi ở file chung cho một phiên. Không có bằng chứng cụ thể về ghi vượt quyền.
3. **Kiểm đã chạy.** `Get-FileHash` khớp **5/5, 3/3, 4/4** mục của ba manifest T-074 và **318/318, 348/348** mục của hai manifest T-069. Đã đối chiếu dấu băm của nguồn quy tắc T-071/T-072 dùng ở trên và bản khóa E5 của T-073. Đã đọc code bằng `git show` ở revision yêu cầu, tính lại tám dòng dự toán, đếm mốc thời gian và đọc trung gian theo ca. [Manifest bản 3](D:/RCA-flashticket/results/T-074/SHA256SUMS-3) · [Manifest T-069](D:/RCA-flashticket/results/T-069/SHA256SUMS-2)
4. **Cần Minh quyết.** Đề nghị **tiếp tục một lượt đáp của Claude trong chat**, tập trung các điểm 1–6. Chưa cần duyệt chạy máy hoặc sửa file để trả lời chúng. Nếu Minh duyệt sửa sau đó, đề nghị dùng bản kế tiếp của thiết kế, câu hỏi và dự toán chịu ảnh hưởng. Ba manifest hiện ghim các bản cũ, sửa tại chỗ sẽ làm mất khả năng kiểm lại. W4/W5 có thể tiếp tục theo quyền đã có. RQ5, độ đúng vùng và lợi ích xếp hạng trên ô đánh giá vẫn chờ dữ liệu W7 sau khóa.

### Prompt bàn giao cho Claude

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-074 — W6 khóa bản và thiết kế đánh giá, tasks/T-074-w6-thiet-ke-danh-gia/.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P9, P10 — chuẩn bị G6. docs/review-prompt.md chưa có khối G6; dùng khối G3 hiện có.
- Người làm và người phản biện chính thức: Claude (người làm), Codex (người phản biện).
- Tài liệu gốc: tasks/T-074-w6-thiet-ke-danh-gia/SPEC.md và LOG.md; docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8; tasks/T-070-dieu-phoi-giai-doan-2/LOG.md; các đầu vào tại SPEC. Hồ sơ T-074 chưa commit, không có git diff gốc.
- Phản biện và phản hồi trước: results/T-070/codex/CX-06-tin-cuoi.md; LOG T-074 phiên 2; results/T-070/codex/CX-08-tin-cuoi.md; LOG T-074 phiên 3; phản biện CX-15 trong chat hoặc results/T-070/codex/CX-15.jsonl do phiên điều phối lưu.
- Code và kết quả liên quan: results/T-074/ bản 1, 2, 3 và SHA256SUMS, SHA256SUMS-2, SHA256SUMS-3; results/T-069/ và hai manifest; results/T-071/, results/T-072/, results/T-073/ cùng bản khai và nguồn ghim tương ứng; src/m1/, src/m1_ft/, src/p3/, src/simplerca/; RCAEval 259ea41, repo lab 407b4f5, FlashTicket 36a3725, chỉ đọc.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat.

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
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khởi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: CHẶN hoặc KHÔNG CHẶN; chặn kết luận/quyết định nào; ở đâu; sai gì;
bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); hậu quả; đề xuất sửa tối thiểu hoặc bằng chứng cần thiếu.
Tiếng Việt, câu ngắn.

Cuối lượt báo:
1. Đã làm gì.
2. File đã thay đổi, hoặc không sửa file nào.
3. Kiểm đã chạy và kết quả.
4. Bất đồng có bằng chứng, câu hỏi mở, phần thiếu và quyết định bị ảnh hưởng; điều cần Minh quyết.

Đề xuất tiếp tục hoặc dừng phản biện, kèm lý do. Nếu không còn phản đối chưa xử lý ảnh hưởng tính đúng, phạm vi kết luận hoặc quyết định đang xin duyệt, đề xuất dừng; không che bất đồng bên kia còn giữ. Có thể thống nhất giới hạn khi thiếu bằng chứng rồi đề xuất dừng; kết luận phụ thuộc vẫn OPEN. Minh quyết cuối. Hai agent đồng ý không thay bằng chứng khoa học; dừng phản biện không tự duyệt SPEC, đóng task hoặc mở test.

Sau đó soạn prompt bàn giao cho agent đối phương: chép nguyên văn Prompt chung + đúng Khối công đoạn + Khối cổng hiện có trong docs/review-prompt.md, chỉ điền thông tin trung tính. Giữ vai trò; người làm nhận prompt đáp phản biện, người phản biện nhận prompt kiểm độc lập. Vẫn soạn khi đề xuất dừng để Minh chọn gửi hay dừng; không tự gửi.

Công đoạn: người làm đáp phản biện. Giữ vai trò người làm, không là người phản biện chính thức của chính task.
Tự soát yêu cầu và mọi file đầu ra gốc cần để trả lời các câu hỏi như một người chưa từng làm task, TRƯỚC khi mở kết luận các bản phản biện. Ghi danh sách điểm tự tìm được vào LOG trước khi mở các kết luận ấy nếu được phép ghi; phiên chỉ đọc ghi nhận xét trong chat.
Sau đó kiểm từng điểm phản biện trên file/code/dữ liệu thật; chạy lại khi rẻ và được phép. Kết luận đúng / đúng một phần / sai / chưa kiểm được với bằng chứng riêng. Reviewer có thể sai, nói quá hoặc đề xuất sửa có mặt trái.
Nếu được Minh cho phép: điền bảng Phản hồi của người làm ở cuối đúng bản phản biện; thêm N1, N2… cho điểm tự tìm được với CHẶN/KHÔNG CHẶN; để trống cột Minh quyết; nối LOG đủ mục 7 của AGENTS, gồm đề xuất sửa gom theo file; chỉ cập nhật dòng task trong STATE khi được phép. Không sửa nội dung hay prompt của reviewer hoặc tự sửa báo cáo/code.
Nếu chưa có quyền ghi các phần này, trình phản hồi và đề xuất trong chat. Soạn prompt bàn giao cho người phản biện kiểm độc lập.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```