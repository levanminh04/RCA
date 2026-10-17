# T-032 — Gói bổ sung 007 (Minh duyệt một lượt ngày 11/10/2026)

Người soạn: Claude. File này lưu nguyên văn gói đã trình trong chat ngày 11/10/2026, để phiên sau làm theo mà không cần lịch sử chat.

- Lời Minh khi yêu cầu trình: "trình toàn bộ để tôi duyệt 1 lượt , ưu tiên mọi hướng cho câu hỏi nghiên cứu, bảo vệ trước giảng viên tốt nhất có thể, hạn chế của dattaset hay thuật toán thì chấp nhận, ghi rõ".
- Lời duyệt của Minh: "duyệt toàn bộ, sửa luôn giúp tôi , ưu tiên mọi hướng cho câu hỏi nghiên cứu, bảo vệ trước giảng viên tốt nhất có thể".
- Mã đã dùng khi ghi giấy tờ ở phần E: xem mục LOG của T-032 ghi ngay sau khi duyệt. Trong nguyên văn dưới đây các chỗ `<mã kế tiếp>` giữ như lúc trình.

Phần dưới đây là nguyên văn gói, từ câu mở tới câu mồi.

---

Dưới đây là toàn bộ gói; Minh trả lời "duyệt" là duyệt cả gói, muốn bỏ việc nào thì nêu số. Tôi chưa sửa file nào. Việc tính toán sẽ làm ở phiên mới vì phiên này đã bị nén ngữ cảnh; sau khi duyệt, phiên này chỉ ghi giấy tờ ở phần E.

Tôi áp lời Minh thành ba nguyên tắc: việc nào làm rõ "phương pháp sai ở bước nào, vì sao" hoặc "quan hệ gọi bổ sung được gì" thì làm; hạn chế của dữ liệu hay thuật toán thì nhận và ghi rõ, không vòng tránh; kết quả bất lợi cho hướng đồ thị cũng ghi đúng như vậy.

## A. Bảy việc làm thêm

Chi phí là ước lượng, chưa đo. Mỗi việc ghi thiết kế ra file trước khi chạy; nhánh giữ nguyên phải khớp bản đóng băng từng bit.

| # | Việc | Câu nó trả lời | Cách đọc kết quả | Nơi chạy, chi phí |
|---|---|---|---|---|
| 1 | Xếp các dịch vụ đứng trên dịch vụ gốc theo vị trí trên chuỗi gọi (phía trên, phía dưới, không liên hệ), cho mọi phương pháp; kèm tỷ lệ nền của mọi dịch vụ trong ca | Sai lầm có nằm dọc chuỗi gọi không | Cao hơn hẳn tỷ lệ nền: đồ thị nhắm trúng. Ngang tỷ lệ nền: đồ thị không nhắm trúng nhóm này | EC2, 20–30 phút |
| 2 | Nối lời gọi chậm tới dịch vụ gốc với các span làm MicroRank và TraceRCA chấm dịch vụ gọi cao | "Nhầm triệu chứng với nguyên nhân" có thật không, bao nhiêu ca | Phần lớn span đó là span chờ dịch vụ gốc: xác nhận ở mức tính toán. Không phải: bác cho hai phương pháp này | EC2, 20 phút |
| 3 | Kênh metric: dịch vụ có cột thắng ở BARO và SimpleRCA nằm đâu so với chuỗi gọi; lưu lượng qua nó trước và sau mốc | Bất thường metric ở dịch vụ khác có đi theo quan hệ gọi không | Chỉ mô tả; không định nghĩa nhãn "lan" vì đề bài task không cho | EC2, 15–20 phút |
| 4 | Thay bước chia trace của MicroRank bằng cách của bài gốc | Hạn chế lớn nhất của MicroRank thuộc bài gốc hay thuộc bản thư viện | Tỷ lệ trace bất thường giảm mạnh và dịch vụ gốc lên hạng: thuộc bản thư viện. Không đổi: thuộc cách tính của bài | Laptop, 10–15 phút |
| 5 | Đọc toàn văn bài TraceRCA gốc | Tác giả có tự nêu hạn chế này không | Điền ô còn trống của bảng đối chiếu | Không cần máy |
| 6 | Phát lại TORAI với bảng log của tác giả (90 bản ghi đã có), lập cùng bảng nguồn log; xem thêm các cột log còn lại | Hạn chế log thuộc TORAI hay thuộc bảng log ta dựng | Hiện tượng lặp lại: của phương pháp. Không lặp lại: của đầu vào ta dựng | EC2, khoảng 50 phút và 15 phút |
| 7 | Chia theo loại lỗi phần đối chiếu metric còn mỏng; sửa câu viết quá tay còn sót ở bảng đối chiếu | Lấp chỗ thiếu của lần soát | | EC2, 5 phút |

Hai việc có điểm phải nói rõ:

- **Việc 4 có một lựa chọn chưa kiểm.** Tôi lấy thời lượng cả trace bằng thời lượng span gốc của trace; mức nền tính theo phần thời gian riêng của từng span; hệ số 1,5 theo bài. Giả định sai khi trace bị cắt ở biên cửa sổ hoặc không có span gốc. Những trace đó tôi đếm riêng và báo, không gán giá trị.
- **Việc 6 nằm ngoài cấu hình chính đã khóa.** Bảng của tác giả lệch cửa sổ so với các phương pháp khác, nên chỉ so hiện tượng, không so độ chính xác. Tôi chưa kiểm bảng của tác giả còn trên EC2 không; thiếu thì báo, không tải lại khi chưa hỏi.

## B. Phần tổng hợp

- **Đọc tay.** Bảng tự động theo từng ca phủ đủ 372 đơn vị của danh mục đã khóa. Đọc tay mỗi nhóm trong 52 nhóm ít nhất một ca sai và một ca đúng cùng điều kiện, cộng mọi ca mà bảng cho thấy đi đường khác. Số "bao nhiêu ca" chỉ lấy từ bảng, không đếm từ ca đại diện. Lý do: đủ để hiểu đường đi mà không mất nhiều phiên. Nếu người phản biện đòi đọc tay đủ 192 ca sai, tôi trình nguyên bất đồng để Minh quyết.
- **Mức đo được "dịch vụ gọi chờ".** Xếp chặt theo ba mức của đề bài:
  - Online Boutique: 16 ca "đo được", kèm điều kiện mã triển khai trùng bản công khai.
  - Train Ticket: 21 ca "đo được một phần", thiếu đúng một bằng chứng là công cụ ghi span.
  - 15 ca còn lại: "không đo được".
  - Lý do: nhãn chặt khó bị bắt bẻ. Quan sát "lời gọi tới dịch vụ gốc chậm ở 19/21 ca" vẫn giữ nguyên.
- **Báo cáo chính.** Theo năm phần của kế hoạch nghiên cứu. Mỗi kết luận viết dạng điều kiện, bước, thông tin bị mất, kèm số ca trên tổng, tác giả có nêu không, thuộc dữ liệu, cài đặt hay cách tính. Tách quan sát, suy luận, ứng viên, câu mở. Xong thì chuyển "chờ phản biện" và soạn lời bàn giao cho Codex theo mẫu.

## C. Giới hạn chấp nhận, ghi rõ trong báo cáo

| Giới hạn | Loại | Hệ quả ghi kèm |
|---|---|---|
| Train Ticket không công bố phiên bản mã và công cụ ghi span; không hỏi tác giả | Dữ liệu | Việc "chờ" chỉ đo được một phần; hệ bán vé phải ghi hai thông tin này |
| Mỗi lời gọi chỉ có hai span | Dữ liệu | Không tách đường truyền, hàng đợi, xử lý bên gọi; hệ bán vé cần thêm mốc lúc yêu cầu tới |
| Online Boutique: nền trace 41–97 giây, metric 5 điểm mỗi phía | Dữ liệu | Thống kê nền kém ổn định; bảng xu hướng và phép đổi thang không kết luận được |
| 15/52 ca không có đủ lời gọi tới dịch vụ gốc | Dữ liệu | Kết luận về chờ chỉ trên 37 ca; 8 ca đồ thị quan hệ gọi không thể giúp |
| Cửa sổ dev không có span mang mã lỗi | Dữ liệu | Nguồn lỗi trace của TORAI rỗng ở 30/30 ca |
| Chỉ 52 ca dev, mỗi ô vài ca, chưa mở test | Giao thức | Không rút mẫu hình theo ô; mọi số là bằng chứng trên dev |
| CIRCA: giá trị cực lớn do chia cho độ lệch gần 0; không tách được ảnh hưởng của cửa sổ vì phải đổi điều đã khóa | Thuật toán | Giữ bản gốc; nêu là hạn chế của cách tính |
| MicroRank: phần cặp còn lại sau mọi phép đổi | Thuật toán | Ghi đúng số còn lại, không ép nguyên nhân |
| SimpleRCA: đếm theo mẫu vừa gây sai vừa là nguồn phân biệt | Thuật toán | Không sửa được bằng đổi cách đếm |
| TORAI: bước nhân quả không tham gia xếp dịch vụ gốc | Cài đặt của thư viện | Không rút kết luận về đồ thị nhân quả từ TORAI |

## D. Điều kiện làm việc

- Giữ nguyên như lần trước: dừng báo khi lệch bản đóng băng, RAM laptop 95%, vượt 12 GiB tổng hoặc 4 GiB laptop, một lượt dự kiến quá 1 giờ, cùng chỗ hỏng 3 lần, cần ghi ngoài phạm vi.
- Không subagent, không sửa code phương pháp hay dữ liệu, không mở test, không đụng task kia, không commit.
- EC2 để bật. Dung lượng thêm ước dưới 1 GiB, tổng khoảng 8,3/12 GiB.
- Thứ tự: việc 1, 2 trước vì giá trị cao nhất. Sau đó việc 6 chạy nền trên EC2 trong lúc việc 4 chạy trên laptop và tôi đọc bài ở việc 5. Rồi việc 3, 7.
- Thời gian: việc làm thêm khoảng một phiên, tổng hợp một đến hai phiên. Tôi chưa chắc kịp mốc 15–18/10.

## E. Giấy tờ ghi ngay sau khi Minh duyệt

1. Lưu nguyên văn gói này vào `results/T-032/goi-bo-sung-007.md`.
2. Nối hai dòng vào sổ quyết định, dùng mã trống kế tiếp lúc ghi. Mã tôi nêu ở tin trước đã bị task kia dùng.

```
| <mã kế tiếp> | 11/10/2026 | T-032: Minh trả lời "duyệt" cho ba điểm Claude trình trong phiên 10: (1) giữ mục 11–14 của khối dán kèm prompt mở phiên là lời Minh, tức dừng sau mục 6 và viết báo cáo chính ở phiên mới; (2) chạy thêm hai nhánh bỏ cạnh theo loại cạnh của CIRCA trên laptop, ghi thiết kế vào file trước khi chạy; (3) dùng tiếp EC2 cho phần còn lại của mục 4 và mục 5. | chat 11/10/2026; ba điểm là chữ của Claude, lời Minh là "duyệt"; LOG T-032 phiên 10 |
| <mã kế tiếp> | 11/10/2026 | T-032: Minh duyệt một lượt gói bổ sung Claude trình ngày 11/10. Lời Minh khi yêu cầu trình: "trình toàn bộ để tôi duyệt 1 lượt , ưu tiên mọi hướng cho câu hỏi nghiên cứu, bảo vệ trước giảng viên tốt nhất có thể, hạn chế của dattaset hay thuật toán thì chấp nhận, ghi rõ". Gói gồm bảy việc làm thêm, mức đọc tay, cách xếp mức đo được, danh sách giới hạn chấp nhận, mục WHY mới và điều kiện làm việc như Q-131. Lời duyệt: "<chép nguyên lời Minh>". | chat 11/10/2026; nguyên văn gói ở results/T-032/goi-bo-sung-007.md; LOG T-032 |
```

3. Nối một mục vào sổ lý do, dùng mã trống kế tiếp:

```
## WHY-<mã kế tiếp> — Bảng mô tả, phép đổi thêm và gói bổ sung của T-032 (Minh duyệt ngày 11/10/2026)

Nguồn nguyên văn: results/T-032/thiet-ke-bang-mo-ta-004.md, thiet-ke-phep-doi-003.md, -005.md, -006.md, goi-bo-sung-007.md.

**Chọn:** (1) bốn bảng mô tả không gọi phương pháp, nối nhãn sau cùng: vị trí tín hiệu của root trong trace; xu hướng nền của cột metric; cấu tạo thời gian của lời gọi; tỷ lệ lời gọi chậm theo cạnh. (2) Mốc đếm: cờ theo mean + 3·std của nền; lời gọi chậm là vượt phân vị 95 của chính cạnh ở nền; chỉ xét cạnh có từ 20 lời gọi mỗi phía; mốc báo cáo 50% và 20%. (3) Tiêu chí mức đo được "dịch vụ gọi chờ root" theo ca: có cạnh đủ lời gọi; ở nền, span phía được gọi dài hơn span phía gọi ở không quá 1% lời gọi; mọi chỗ gọi trong mã nguồn là lời gọi chặn ở mọi phiên bản ứng viên. (4) Phép thử giả bằng mốc lùi vào đoạn nền. (5) Phép đổi thêm: bỏ cạnh theo loại ở CIRCA; bỏ cột log ở TORAI B; bộ chia trace theo bài MicroRank gốc. (6) Bảng vị trí trên chuỗi gọi của thực thể đứng trên root; bảng nối lời gọi chậm với span mang cờ; phát lại TORAI nguồn A có quan sát.

**Vì sao:** P4 đòi chỉ ra thông tin của root nằm ở đâu, bước nào làm mất nó, và quan hệ giữa dịch vụ bổ sung được gì. Thứ hạng và cờ không trả lời được; cần bảng theo vị trí và phép đổi đúng một bước.

**Phương án đã xét:** chỉ dùng thứ hạng và cờ (không cho biết vị trí tín hiệu); so trung vị từng phần của lời gọi (che mất ca có hai nhóm lời gọi chậm); ngưỡng cố định theo mili giây (phụ thuộc cạnh); định nghĩa nhãn lan (SPEC không cho); hỏi tác giả về phiên bản Train Ticket (Minh chọn chấp nhận giới hạn).

**Bằng chứng:** results/T-032/ket-qua-phien-10.md cho phần đã chạy. Phần của gói bổ sung chưa có kết quả, là kế hoạch kiểm.

**Giới hạn:** định nghĩa vị trí, mốc đếm và phép đổi thêm đều đặt sau khi đã xem kết quả dev trước đó, nên chỉ là bằng chứng trên dev cho ứng viên. Các mốc 20 lời gọi, phân vị 95, 50% do người làm đặt; số thô được lưu. Bộ chia trace theo bài gốc cần một quy ước lấy thời lượng cả trace, chưa kiểm.

**Kết luận phụ thuộc:** bốn đầu ra đầu của P4 trong T-032; mức đo được theo ca; căn cứ đề xuất ứng viên P5–P6. Lợi ích của đồ thị vẫn cần đánh giá riêng.
```

4. Sửa một câu ở dòng 3 của `doi-chieu-tai-lieu-goc-phien-10.md`:
   - Cũ: "Củng cố dòng 1: thứ hạng do đếm phủ quyết định, không do span của dịch vụ nào mang cờ".
   - Mới: "Thứ hạng ít nhạy với việc span của dịch vụ nào mang cờ. Đếm riêng thay đếm phủ làm đổi 115/252 cặp; 137 cặp còn lại chưa phép đổi nào giải thích".
5. Nối nhật ký của task (quyết định, bước tiếp chính xác) và cập nhật dòng trạng thái của task.

Câu mồi cho phiên mới: "Đọc AGENTS.md, làm tiếp T-032 theo `results/T-032/goi-bo-sung-007.md` và mục cuối của LOG."

---

# Bản sửa việc 4 (nối ngày 11/10/2026, phiên 11)

Phần trên của file là nguyên văn gói đã duyệt, giữ nguyên. Phần này nối thêm, không sửa chữ cũ.

- Lời Minh (chat 11/10/2026, giữa phiên 11): "kiểm tra thông tin này , nếu thấy đúng thì duyệt theo, sai thì phản biện, không dừng các việc khác".
- Thông tin được kiểm: đoạn Claude viết ở phiên trước, Minh dán lại. Nguyên văn ở mục 1 dưới đây.
- Kết quả kiểm của Claude ở phiên 11: ba điểm sửa đều đúng (mục 2). Bản sửa có hiệu lực theo lời Minh; ghi ở Q-135.
- Mục 3 là phần Claude thêm khi kiểm. Nó không đổi bốn điểm của bản sửa; nó nêu các chi tiết phải chốt trong file thiết kế trước khi đếm.

## 1. Nguyên văn đoạn được kiểm

Không phải đoán mò, nhưng cũng chưa phải điều lấy từ nguồn: đó là một chỗ tôi tự đặt thay cho thứ dữ liệu không có. Khi đọc lại hồ sơ MicroRank để trả lời Minh, tôi còn thấy chữ tôi viết cho việc 4 trong gói có ba chỗ chưa khớp với bài và code gốc, nên việc 4 cần sửa trước khi chạy.

### Quy ước đó là gì

Bài MicroRank gốc coi một yêu cầu (một trace) là bất thường khi thời gian của cả yêu cầu vượt mức dự kiến. Muốn áp vào dữ liệu của ta phải biết "thời gian của cả yêu cầu" lấy ở đâu.

- **Code gốc lấy ở đâu:** ở span của dịch vụ tên `frontend` có nhãn "server". Điều này có trong hồ sơ đã được phản biện, kèm dòng mã.
- **Dữ liệu của ta:** theo cùng hồ sơ, bảng trace mà phương pháp nhận ở bộ Train Ticket không có nhãn đó. Bộ Online Boutique tôi chưa kiểm.
- **Chỗ tôi tự đặt:** lấy span không có span cha trong trace làm span đầu của yêu cầu. Đây là "quy ước".

Gọi là "chưa kiểm" vì tôi chưa đếm trên dữ liệu ba điều:
- bao nhiêu trace có đúng một span như vậy;
- span đó có thật sự bao cả yêu cầu không, vì trace bị cắt ở biên cửa sổ sẽ mất span đầu và một span ở giữa trông như span đầu;
- kết quả có đổi theo quy ước này không.

Hồ sơ cũng cảnh báo đúng điểm này: thiếu nhãn thì không được coi mọi span mất cha là span đầu thật, và không được gọi kết quả là bộ phát hiện của bài gốc.

### Ba chỗ chữ trong gói chưa khớp nguồn

| Tôi đã viết | Nguồn ghi | Sửa thành |
|---|---|---|
| "hệ số 1,5 theo bài" | Bài dùng 1,5 lần độ lệch chuẩn. Code gốc ở bước chia nhóm dùng 1 lần độ lệch chuẩn cộng 50 ms mỗi trace. Hồ sơ dặn ghi cả hai, không chọn theo kết quả. | Chạy cả hai luật, báo riêng. |
| "mức nền theo phần thời gian riêng của từng span", tức trừ phần được span con che | Code gốc trừ tổng thời lượng các span con. Hai cách khác nhau khi span con chạy chồng nhau. | Làm theo code gốc; đếm số span mà hai cách cho kết quả khác. |
| Gọi là "cách của bài gốc" | Dữ liệu thiếu nhãn nên không chạy được đúng bản gốc. | Gọi đúng tên: công thức của bài gốc, với span đầu do ta quy ước. |

### Đề xuất sửa việc 4, chờ Minh duyệt

1. Đếm trước, chưa chạy phương pháp: mỗi ca có bao nhiêu trace có không, một, hoặc nhiều span đầu, và bao nhiêu trace bị cắt ở biên.
2. Nếu dưới 90% trace có đúng một span đầu thì dừng. Khi đó ghi là hạn chế của dữ liệu: không áp được bộ chia của bài gốc. Mốc 90% do tôi đặt và ghi vào file thiết kế trước khi đếm.
3. Nếu đạt: chạy hai nhánh theo hai luật trên, mức nền theo code gốc. Nhánh giữ nguyên vẫn phải khớp bản đóng băng từng bit.
4. Kết quả chỉ được nói về "bản gần nhất với bài gốc mà dữ liệu cho phép", không nói về MicroRank gốc.

- **Vì sao nên giữ việc này:** trước cô, nói được "bản thư viện khác bài gốc ở bước chia trace, dữ liệu công khai thiếu nhãn để chạy đúng bản gốc, chúng em chạy bản gần nhất và ghi rõ chỗ thay" thì chắc hơn là bỏ trống.
- **Cái giá:** thêm khoảng 20–30 phút máy trên laptop (ước lượng), và kết luận chỉ ở mức có điều kiện.
- **Phương án khác:** bỏ việc 4, chỉ ghi giới hạn. Nhanh hơn, nhưng câu "hạn chế lớn nhất của MicroRank thuộc bài gốc hay bản thư viện" để mở.

## 2. Kết quả kiểm (Claude, phiên 11)

Nguồn đã đọc trực tiếp: code `IntelligentDDS/MicroRank` đúng bản ghim `efd85e8e6f0fad30f6f8aaf0555e3324d8f5f982` (bản ghim ghi ở `src/microrank/PROVENANCE.json`), đọc qua địa chỉ file thô của GitHub, không lưu về máy; bản chữ của bài báo ở `results/T-015/sources/microrank-paper.txt`; hồ sơ `results/T-015/ho-so-microrank.md`; hai luật đã cài sẵn ở `src/microrank/detectors.py`.

| Điểm trong đoạn | Nguồn | Kết quả |
|---|---|---|
| Thời gian cả yêu cầu lấy ở span của `frontend` có nhãn server | `preprocess_data.py` dòng 311–312, 326–327: cộng `duration` của mọi span có `serviceName == "frontend"` và `span.kind == "server"` | Đúng. Chi tiết thêm: là tổng các span như vậy; trace không có span nào như vậy bị bỏ khỏi cả hai nhóm (dòng 315–320) |
| Bài dùng 1,5 lần độ lệch chuẩn | Bản chữ của bài, dòng 312: "we set n = 1.5 in this paper" | Đúng |
| Code chia nhóm dùng 1 lần độ lệch chuẩn cộng 50 ms mỗi trace | `anormaly_detector.py` dòng 93–105: `expect_duration += count * (mean + std)`; `real_duration > expect_duration + 50` | Đúng. Luật 1,5 lần nằm ở hàm báo động mức hệ thống (dòng 61–70), kèm điều kiện hơn 8 trace |
| Mức nền: code trừ tổng thời lượng span con | `preprocess_data.py` dòng 189–192, 216–219: `temp[parentId]['duration'] -= temp[spanid]['duration']` | Đúng |
| Hồ sơ cảnh báo không coi mọi span mất cha là span đầu thật | `ho-so-microrank.md` dòng 25, 163, 263–264 | Đúng |
| Train Ticket không có dịch vụ tên `frontend` | `ho-so-microrank.md` dòng 269 (kiểm trên một ca) | Đúng theo hồ sơ; phiên 11 đếm lại trên đủ ca ở bước đếm |

Không tìm thấy điểm sai. Con số "20–30 phút máy" là ước lượng, chưa đo.

## 3. Chi tiết Claude thêm khi kiểm (chốt trong file thiết kế trước khi đếm)

Các điểm này lấy từ code gốc, không phải ý mới. Chỗ nào code gốc không nói thì ghi rõ là lựa chọn của người làm.

1. **Vì sao code gốc trừ tổng chứ không trừ phần che.** Với một trace đủ span và có đúng một span đầu, tổng "thời lượng trừ tổng span con" của mọi span bằng đúng thời lượng span đầu. Nhờ vậy "mức dự kiến của cả yêu cầu" (tổng mức nền của các thao tác trong trace) mới so được với thời lượng span đầu. Trừ phần che thì đẳng thức này mất khi span con chạy chồng nhau. Đẳng thức được dùng làm phép tự kiểm cho phần cài đặt.
2. **Mức nền của code gốc còn ba chi tiết:** bỏ trace có span thiếu cha khi học nền; bỏ trace mà span đầu, sau khi trừ span con, dài hơn 1 giây; dùng độ lệch chuẩn tổng thể, làm tròn 4 chữ số theo mili giây. Làm theo cả ba; đếm số trace mỗi bộ lọc bỏ.
3. **Phân biệt hai loại "không có cha":** span khai báo không có cha (trường cha trống) và span có khai báo cha nhưng cha không nằm trong cửa sổ. Chỉ loại đầu được coi là span đầu. Loại sau là dấu hiệu trace bị cắt hoặc mất span. Phải kiểm trường cha của hai dataset có cho phép phân biệt không; không phân biệt được thì báo.
4. **Trace có nhiều span đầu:** code gốc cộng thời lượng. Làm theo; đếm riêng.
5. **Online Boutique có dịch vụ tên `frontend`.** Kiểm bảng trace của Nezha-OB có nhãn loại span không. Có thì chạy thêm đúng luật gốc ở Nezha-OB và so với quy ước span đầu.
6. **Đơn vị của mốc 90% (lựa chọn của người làm, code gốc không nói):** tính theo từng ca trên các trace sau mốc. Ca dưới 90% ghi N/A cho nhánh này. Dataset có hơn một nửa số ca N/A thì dừng cả dataset.
7. **Thao tác xuất hiện sau mốc nhưng không có mức nền:** code gốc sẽ báo lỗi. Bản đóng băng cũng trả ERROR ở 4 ca Train Ticket vì lý do này. Giữ ERROR, không lấp giá trị.
