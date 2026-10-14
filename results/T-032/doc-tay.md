# T-032 — Đọc tay theo 52 nhóm đã khóa

Người làm: Claude, phiên 12 (11/10/2026); mục 8 thêm ở phiên 13 cùng ngày. File này ghi phần đọc tay của bước 4 trong SPEC. Nó đi kèm bảng tự động `doi-chieu-dung-sai.json`; bảng đó phủ đủ 372 đơn vị. Mục 1–7 phủ các đơn vị được chọn theo đường đi (phiên 12); mục 8 đọc nốt mọi đơn vị sai còn lại. Vài câu ở mục 1–6 đã bị kết quả phiên 13 sửa; chỗ đó có ghi chú "Phiên 13:" ngay tại câu.

## Cách đọc file này

- **Đọc tay là gì ở đây.** Với mỗi đơn vị (một ca × một phương pháp × một seed), tôi đi theo chuỗi: đầu vào phương pháp nhận → giá trị trung gian đã lưu → điểm của root và của từng thực thể đứng trên root → thứ hạng → hạng thay đổi thế nào dưới từng phép đổi. Rồi so với một ca đúng có điều kiện tương ứng. Mọi con số lấy từ phiếu đọc của đơn vị, ở `runs/tong-hop-phien-12-001/phieu-doc/<mã>.txt`; phiếu trích từ `doi-chieu-dung-sai.json` → `/don_vi/*/chi_tiet`, nơi ghi đường dẫn và con trỏ tới file kết quả gốc.
- **Chọn đơn vị thế nào.** Quy tắc đặt trước khi đọc phiếu nào (`ke-hoach-doc-tay.json` → `/quy_tac`): trong mỗi nhóm, mỗi "đường đi" khác nhau đọc đơn vị sai có mã nhỏ nhất; đối chứng là ca đúng của chính đơn vị đó ở đúng k của nhóm, ưu tiên cùng ô (cùng dịch vụ gốc và loại lỗi), rồi cùng kênh quan sát, rồi mã nhỏ nhất. Không chọn theo điểm, theo vị trí dịch vụ gọi hay theo kết quả phép đổi. "Đường đi" là chữ ký do script ghép từ các trường của bảng; nó chỉ để chia đơn vị đọc, không phải nguyên nhân.
- **Số lượng.** 100 đơn vị đọc không trùng: 76 đơn vị sai ở hạng 1 hoặc không OK, 24 đối chứng đúng ở hạng 1. Trong 76 đơn vị đó, 74 được chọn theo đường đi và 2 được đọc với vai trò đối chứng ở k = 5 (root nằm trong 5 hạng đầu nhưng không hạng 1). 52/52 nhóm có ít nhất một đơn vị sai được đọc. 110/301 yêu cầu đối chứng không có ca đúng nào cùng dataset, cấu hình và cửa sổ; các nhóm đó ghi rõ "thiếu đối chứng". **Sau phiên 13:** thêm 68 đơn vị sai (mục 8), tổng 168 đơn vị đọc không trùng (144 sai hoặc không OK, 24 đối chứng); 48 đơn vị không chạy được ghi theo lý do.
- **Không dùng file này để đếm.** Một đơn vị đại diện không chứng nhận các đơn vị cùng đường đi. Số "bao nhiêu ca" trong báo cáo chính lấy từ bảng tự động hoặc file kết quả.
- **Từ dùng.** "Root": dịch vụ gốc theo nhãn. "Trên root": được phương pháp xếp hạng tốt hơn root. "Phía trên root": dịch vụ gọi root trực tiếp hoặc gián tiếp. a, n, H của TraceRCA: số span mang cờ của thao tác, số span sau mốc của thao tác, tổng số span mang cờ của cả ca. Hạng ghi [nhỏ nhất, lớn nhất]; hai số khác nhau là có hòa.
- **Mức kết luận của mỗi mục:** *xác nhận ở mức tính toán* (đã có phép đổi đúng một bước làm đổi hạng, hoặc đẳng thức đã kiểm), *quan sát* (thấy trên trung gian, chưa có phép đổi), *chưa phân xử*.

**Đính chính sau REVIEW (Minh duyệt 11/10).** Cờ, phiếu và hạng là đầu ra của cách chấm; chúng không tự xác nhận có/không có đáp ứng do lỗi. Bảng no_signal cũ thực chất đếm không hạng 1. Nezha-OB có mốc giả giữa nền (22/22 ca), nhưng cửa sổ ngắn/không tương đương; BARO/SimpleRCA trong bảng đó được nối từ mốc thật. Không dùng chúng làm đối chứng metric/log ở mốc giả. Đọc tay MicroRank gồm 48 đơn vị: 46 OK sai, 1 ERROR, 1 đối chứng đúng; ngoài phần đọc có 3 ERROR và 1 OK đúng. Bằng chứng kiểm số của mục 8 lưu ở runs/sua-review-001/kiem-so/.

## 1. TraceRCA (bản trong thư viện RCAEval) — 14 nhóm, 20 đơn vị đọc

Phiếu gọn: `runs/tong-hop-phien-12-001/phieu-gon/tracerca.txt`. Chuỗi tính: mỗi thao tác có mean, std ở đoạn nền; span sau mốc vượt mean + 3·std mang cờ; điểm thao tác = 2a/(n + H); điểm dịch vụ là điểm lớn nhất trong các thao tác của nó.

### 1.1 Nhóm `RE2-TT|tracerca|k=1|status:ERROR` và `k=5|status:ERROR` (4 đơn vị, một đường đi)

- **Đơn vị đọc:** `dev-03d4910932` (route|socket). Phương pháp dừng với `KeyError: 'ts-order-other-service_getMore ts.orders'`.
- **Chuỗi:** thao tác này xuất hiện ở đoạn sau mốc nhưng không có ở đoạn nền → bước tra mean, std theo thao tác không có khóa → lỗi, không có điểm nào. Cả 4 đơn vị ERROR có cùng lý do (bảng: `/don_vi/*/chi_tiet/ly_do_khong_OK`).
- **Đối chứng cùng ô:** `dev-b8bd0abf60` (route|socket), root hạng 1 với a = 1.895, n = 4.732. Ca này chạy được vì thao tác trên có mặt ở nền.
- **Phân loại:** thiếu đầu vào ở đoạn nền (dữ liệu) gặp cách cài không xử lý thao tác mới (bản thư viện). Không phải cơ chế xếp hạng. Ở ca ERROR, lời gọi tới root chậm ở 93% lời gọi sau mốc (bảng C2), tức trace có tín hiệu; phương pháp không dùng được nó.
- **Chưa biết:** nếu bỏ qua thao tác thiếu nền thì root xếp thứ mấy. Phép kiểm ghi ở `kiem-tiep.md` mục KT-8.

### 1.2 Nhóm `RE2-TT|tracerca|k=1|M5` (4 đơn vị, ba đường đi) và `k=5|M5` (1 đơn vị)

**Đường đi "chủ yếu là chờ root, xếp theo tỷ lệ không đưa root lên hạng 1": `dev-f36d0647d5` (order|loss), root hạng 3.**

- Root: thao tác `OrderRepository.findByTravelDateAndTrain`, a = 99, n = 816 (12%), điểm 0,0372. H = 4.511.
- Trên root: `ts-seat-service` a = 147, n = 1.300 (11%), điểm 0,0506; `ts-travel-service` a = 104, n = 792 (13%), điểm 0,0392. Cả hai gọi trực tiếp root. Trong các span mang cờ của hai thao tác đó, 61% và 85% là span bao một lời gọi chậm tới root chiếm từ nửa phần vượt.
- Phép đổi: cờ theo phần chưa được span con phủ (T-D) làm `ts-travel-service` rời vị trí trên root, `ts-seat-service` vẫn còn; root lên hạng 2. Xếp theo tỷ lệ a/n làm root xuống hạng 6. Bước xếp hạng của bài gốc (bản cài theo lời văn): root không có điểm dương, hạng 8–27.
- **Đọc:** hai dịch vụ gọi được chấm cao vì span của chúng dài theo lời gọi tới root. Tỷ lệ của root và của hai dịch vụ gọi gần nhau (11–13%), nên thứ tự do số span quyết định. Đây là ca mà "chờ root" và "đếm theo số tuyệt đối" cùng có mặt.

**Đường đi "chủ yếu là chờ root, xếp theo tỷ lệ đưa root lên hạng 1": `dev-12a1a88069` (order|disk), root hạng 2.**

- Root: a = 86, n = 494 (17%), điểm 0,0445. Trên root: `ts-seat-service` a = 130, n = 1.286 (10%), điểm 0,0559; 98% span mang cờ của nó là span chờ root.
- Phép đổi: xếp theo a/n đưa root lên hạng 1. T-D không đổi hạng: phần của span `ts-seat-service` không được span con phủ vẫn vượt ngưỡng.
- **Đối chứng cùng ô:** `dev-1e6d61b5ec` (order|disk), root hạng 1. Ở ca này root chỉ có 29 span ở thao tác cao nhất (a = 8), H = 266, và chỉ 1 trong 19 ứng viên nằm phía trên root; cạnh gọi tới root không đủ 20 lời gọi. **Điều khác giữa ca đúng và ca sai cùng ô không phải loại lỗi mà là tải:** ở ca sai, chuỗi `ts-seat-service → ts-order-service` có hơn một nghìn span trong cửa sổ; ở ca đúng gần như không có dịch vụ gọi nào trong trace. Khi không có span của dịch vụ gọi thì không có gì để chấm nhầm.
- **Đọc:** T-D không gỡ được cặp này dù 98% span mang cờ là span chờ root. Một cách hiểu: phần chậm nằm ngoài span của root (đường truyền hoặc hàng đợi), nên trừ span con không lấy nó đi. Bảng C2 cho lỗi disk: 79% phần vượt nằm trong span của root, 21% nằm ngoài. Chưa kiểm riêng cho cặp này. **Phiên 13:** cách hiểu này không được hỗ trợ khi mở bảng theo cạnh: ở cặp này 106/128 lời gọi chậm (83%) nằm trong span của root; xem mục 8.3 điểm 10.

**Đường đi "không xét được": `dev-260d332c8d` (order|loss), root hạng 9, cũng là đơn vị duy nhất của nhóm `k=5|M5`.**

- Root: a = 6, n = 39 (15%), điểm 0,0248. H = 445. Cạnh gọi tới root dưới 20 lời gọi ở một phía.
- Trên root 8 thực thể: 6 không liên hệ với root trên đồ thị gọi (`ts-auth-service` 41/450, `ts-basic-service` 33/1.044, `ts-ticketinfo-service` 26/1.044, `ts-train-service` 14/478…), 1 gọi trực tiếp (`ts-inside-payment-service` 7/39), 1 phía dưới.
- Phép đổi: xếp theo tỷ lệ đưa root lên hạng 3 (còn 2 thực thể); T-D lên hạng 5; xếp theo số tuyệt đối xuống 9–11.
- **Đối chứng cùng ô (ở k = 5):** `dev-20acb4402d` (order|loss), root hạng 4, tức đúng trong 5 hạng đầu nhưng sai ở hạng 1; đọc ở mục 1.3.
- **Đọc:** cờ M5 của ca này (có dịch vụ phía trên đứng trước root) đúng về vị trí, nhưng thứ đẩy root xuống hạng 9 chủ yếu là sáu dịch vụ **không liên hệ** có 2–9% span mang cờ trên vài trăm tới một nghìn span. Với lỗi mất gói, root chỉ còn 39 span sau mốc. Ca này cho thấy cờ M5 không đồng nghĩa "sai vì dịch vụ gọi".

### 1.3 Nhóm `RE2-TT|tracerca|k=1|M0` (1 đơn vị)

- **Đơn vị đọc:** `dev-20acb4402d` (order|loss), root hạng 4. Root: a = 11, n = 46 (24%), điểm 0,0478; H = 414.
- Trên root: `ts-ticketinfo-service` 48/1.066 (4,5%), `ts-auth-service` 28/452 (6%), `ts-basic-service` 37/1.066 (3%). Cả ba không liên hệ với root; tỷ lệ span chờ root bằng 0.
- Phép đổi: xếp theo a/n đưa root lên hạng 1; T-D lên hạng 2; xếp theo số tuyệt đối xuống hạng 6.
- **Đối chứng (cùng kênh, khác ô):** `dev-14372e1209` (route|mem), root hạng 1 với a = 1.574, n = 4.968. Ở ca đúng root là thao tác đông span nhất trong các thao tác có cờ; ở ca sai root ít span nhất.
- **Kết luận, xác nhận ở mức tính toán cho ca này:** trong điều kiện root có ít span sau mốc (46) và H lớn gấp 9 lần n của root, điểm 2a/(n + H) đi theo a; thao tác đông span có tỷ lệ cờ nền 3–6% thắng root có tỷ lệ 24%. Đổi riêng công thức sang tỷ lệ trả lại hạng 1.
- **Chưa phân xử:** vì sao thao tác của dịch vụ không liên hệ có 3–6% span vượt 3 lần độ lệch chuẩn. Hai giải thích: phân phối thời lượng có đuôi dài nên tỷ lệ vượt nền tự nhiên đã cỡ đó; hoặc lỗi mất gói làm chậm cả dịch vụ không nằm trên chuỗi gọi qua root. Phép thử giả (mốc lùi vào nền) cho bảng vị trí đã có; phép đếm tỷ lệ cờ của chính các thao tác này ở mốc giả chưa làm, ghi ở `kiem-tiep.md` mục KT-2. **Phiên 13 (KT-2):** số span mang cờ ở mốc giả → sau mốc thật, cùng độ dài cửa sổ: `ts-ticketinfo-service` 14/510 → 31/532; `ts-auth-service` 4/216 → 23/231; `ts-basic-service` 13/510 → 20/532. Tức mức tự nhiên của ba thao tác đã là 1,9–2,7%; hai thao tác tăng gấp từ 2 lần sau mốc, một thao tác tăng 1,5 lần. Cả hai giải thích cùng có mặt (`ket-qua-phien-13.md` mục 2).

### 1.4 Nhóm `Nezha-OB|tracerca|k=1|M5` (16 đơn vị, bảy đường đi) và `k=5|M5` (10 đơn vị, năm đường đi)

Nezha-OB chỉ có 2 ca TraceRCA xếp root hạng 1, nên **không đơn vị sai nào ở đây có đối chứng đúng cùng ô**. Đối chứng dùng chung là `dev-9b9397a4dc` (recommendationservice|cpu_consumed; cùng kênh, khác ô) cho k = 1 và `dev-14701a3bbb` cho k = 5. Giới hạn này ghi cho mọi mục con dưới đây.

- **Đối chứng `dev-9b9397a4dc`:** root hạng 1; thao tác cao nhất của root là span **phía gọi** của lời gọi từ root sang `productcatalogservice` (a = 43, n = 313, 14%), H = 284. Root không đứng đầu ở vị trí trace nào của bảng A, và lời gọi tới root gần như không chậm (3%). Tức ở ca đúng, root thắng nhờ chính quy tắc "span thuộc dịch vụ nào thì tính cho dịch vụ đó": span root chờ dịch vụ khác được tính cho root. Cùng bước tính ấy, khi root là bên được gọi, lại tính thời gian chờ root cho dịch vụ gọi.

Bảy đường đi của nhóm k = 1:

1. **"Chờ root", tỷ lệ không cứu — `dev-14701a3bbb` (shippingservice|cpu_contention), hạng 2** (3 đơn vị cùng đường đi). Root: a = 41, n = 171 (24%). Trên root: `frontend`, thao tác là span phía gọi của lời gọi tới root, a = 122, n = 151 (81%), 100% là span chờ root. Root đứng đầu ở ba vị trí "phía gọi" của bảng A nhưng không ở span của chính nó. T-D không đổi; a/n xuống hạng 3; bước của bài gốc: `frontend` đứng đầu, root hạng 4. **Đọc:** tín hiệu của sự cố nằm ở span phía gọi của lời gọi tới root (81% vượt ngưỡng) nhiều hơn ở span của root (24%); phương pháp gắn span phía gọi cho `frontend`.
2. **"Chờ root", tỷ lệ cứu — `dev-3e27669440` (adservice|cpu_contention), hạng 2** (1 đơn vị). Root 328/489 (67%), `frontend` 379/489 (78%), 100% span chờ root. Xếp theo a/n đưa root lên hạng 1, dù thao tác cao nhất của root có tỷ lệ thấp hơn của `frontend`; suy luận, chưa mở bảng theo thao tác: dưới cách xếp theo tỷ lệ, điểm của root lấy từ một thao tác khác của nó. Hai thao tác ở trên có cùng n = 489: đó là hai đầu của cùng một loại lời gọi.
3. **"Không xét được", tỷ lệ không cứu — `dev-70629373f9` (paymentservice|cpu_contention), hạng 9** (1 đơn vị). Root 2/42 (5%). `checkoutservice` gọi trực tiếp root: 36/42 (86%), nhưng cạnh chỉ có 42 lời gọi sau mốc và dưới 20 ở một phía nên không tính được "lời gọi chậm". Sáu thực thể khác trên root có tỷ lệ 2–4% trên 874–2.996 span. **Đọc:** cùng hình dạng với đường đi 1 (span phía gọi 86%, span của root 5%), thêm phần khối lượng. Không gọi là "chờ root" vì thiếu điều kiện đo.
4. **"Không xét được", tỷ lệ cứu — dev-3b92690644 (checkoutservice|return), hạng 7** (3 đơn vị). Root 4/132 (3%). Các thao tác trên root có 1–4% cờ (currencyservice 101/2.981, frontend 133/4.254). a/n đưa root lên hạng 1; chưa lưu thao tác thắng của root trong nhánh ấy. Tỷ lệ cờ native nhỏ không chứng minh thời lượng không phản ứng với lỗi hoặc thứ hạng chỉ do nhiễu nền.
5. **Không chờ, tỷ lệ không cứu — dev-27252dca60 (productcatalogservice|exception), hạng 8** (2 đơn vị). Root 3/1.089 (0,3%); không đứng đầu ở vị trí trace nào. a/n hạng 8, a/n từ 20 span hạng 5, a hạng 4–5. Đây là quan sát về cờ và cách chấm; đáp ứng thời lượng do lỗi chưa phân xử, chưa quy riêng cho thiếu dữ liệu.
6. **Không chờ, tỷ lệ cứu — `dev-2bfc97b01e` (checkoutservice|network_delay), hạng 6** (2 đơn vị). Root 5/31 (16%). `frontend` 30/828 (4%), chỉ 13% span mang cờ là span chờ root; bốn thực thể khác 2–4% trên 489–3.869 span. a/n đưa root lên hạng 1. Cùng cơ chế với mục 1.3.
7. **"Chờ root" một phần — dev-5467884de4 (recommendationservice|network_delay), hạng 7** (4 đơn vị). Root 7/450 (2%), span phía gọi của frontend 439/450 (98%), 99% là span chờ root. Năm thực thể khác 2–9% cũng đứng trên root. a/n hạng 9, T-D không đổi; bước theo bài đưa root hạng 2. Cờ hiện rõ hơn ở phía gọi; không có nghĩa span của root không đổi. Gắn bằng chứng phía gọi về dịch vụ được gọi là ứng viên cần đánh giá, chưa chứng minh phải dùng cách ấy mới xếp đúng.

Nhóm `k=5|M5` gồm năm trong bảy đường đi trên (các đơn vị 3–7); đối chứng ở k = 5 là `dev-14701a3bbb`, ca có root hạng 2 (đúng trong 5 hạng đầu). So hai bên: ở đối chứng root có 24% span mang cờ; ở năm đơn vị sai root có 0,3–16%.

### 1.5 Nhóm `Nezha-OB|tracerca|k=1|M0` (2 đơn vị, một đường đi)

- **Đơn vị đọc:** `dev-1ac905bc95` (frontend|return), hạng 3. Root là điểm vào của hệ, không có dịch vụ nào phía trên (0/8 ứng viên). Root 11/409 (3%). Trên root: `checkoutservice` 10/38, `currencyservice` 66/2.178, đều là dịch vụ root gọi.
- **Đọc:** root có 11 span mang cờ nhưng không hạng 1. Chưa tách cờ do lỗi khỏi nhiễu nền; không kết luận return không làm đổi thời lượng. Ca này không có cạnh đi vào root, còn cạnh root gọi dịch vụ khác vẫn có.

### 1.6 Nhóm `k=1|M3` và `k=5|M3` (hòa)

- **`dev-396c8dbf7d` (emailservice|cpu_consumed), hạng [1, 3].** Root 38/38 (100%), điểm 0,0808, không thực thể nào có điểm cao hơn nhưng có hai thực thể bằng điểm. Lời gọi tới root chậm ở 100% lời gọi. T-D đưa root về hạng [1, 1]. **Đọc:** mỗi lời gọi tới root có hai span (phía gọi và phía được gọi) cùng số lượng và cùng vượt ngưỡng, nên hai thao tác có cùng a, n và cùng điểm. Bước tính điểm không phân biệt được hai đầu của một lời gọi; bỏ phần được span con phủ thì phân biệt được.
- **dev-8ecd9880ed (checkoutservice|return), hạng[5,6] ở k=5.** Root 2/28; không đứng đầu ở vị trí trace nào, hòa ở biên hạng 5 giữa điểm nhỏ. Chưa có bằng chứng phân xử đáp ứng do lỗi và cờ nền; không suy từ hạng ra dữ liệu không có dấu hiệu.

### 1.7 Nhóm `k=1|M2`, `k=1|M6`, `k=5|M2`, `k=5|M6` (cùng một đơn vị)

- **`dev-7b7c973198` (emailservice|network_delay): root không được xếp.** Không thao tác nào của root có span mang cờ, nên root không có điểm hữu hạn và bị bộ lọc của adapter loại. Trong khi đó lời gọi tới root chậm ở 100% lời gọi, và root đứng đầu ở vị trí `in_u` (span phía gọi, phần chưa được span con phủ).
- **Đọc:** ca này không thao tác nào của root mang cờ theo ngưỡng đang dùng; adapter loại root vì không có điểm hữu hạn. Span phía gọi mang bằng chứng chậm. Đây là chuỗi tính toán cụ thể của ca này, không suy rộng rằng span của root luôn không có tín hiệu ở mọi ca trễ mạng.

### 1.8 Điều rút ra từ phần đọc TraceRCA

- Có ba đường quan sát: gắn span phía gọi cho dịch vụ gọi; thao tác đông span thắng nhờ số tuyệt đối; root ít cờ và không được cách chấm hiện tại tách ra. Hai đường đầu có bằng chứng tính toán theo ca; đường cuối chưa xác nhận lỗi không làm đổi thời lượng. Một ca có thể có nhiều đường.
- Đường (i) có ở cả ca đúng (đối chứng `dev-9b9397a4dc`): cùng quy tắc gắn span cho dịch vụ sở hữu nó giúp root khi root là bên gọi và hại root khi root là bên được gọi.
- Với một phần ca trễ mạng ở Nezha-OB, các phép đổi đã thử chưa đưa root hạng 1 và cờ phía gọi rõ hơn cờ root. Đây là căn cứ đề xuất dùng cạnh; không bác bỏ mọi phép chấm theo nút hoặc mọi tín hiệu của root.
- Ca đúng và ca sai cùng ô ở RE2-TT khác nhau về **tải** (có hay không có span của dịch vụ gọi trong cửa sổ), không khác về loại lỗi.

## 2. MicroRank (biến thể RCAEval sửa đầu vào) — 11 nhóm, 20 đơn vị đọc

Phiếu gọn: `runs/tong-hop-phien-12-001/phieu-gon/microrank_full.txt`. Chuỗi tính: span vượt mean + 3·std của thao tác mang cờ; trace có bất kỳ span mang cờ vào nhóm bất thường (A), còn lại là nhóm bình thường (N); PageRank trên hai nhóm cho trọng số; mỗi thao tác được đếm ở mọi trace A chứa nó (đếm phủ); spectrum dstar2 cho điểm thao tác; điểm dịch vụ là điểm lớn nhất. Trong phiếu: "tự có" là số trace A mà thao tác tự mang cờ; "ngữ cảnh" là số trace A chứa thao tác nhưng thao tác không mang cờ; "gắn root" là tỷ lệ trace A chứa thao tác mà có bất thường gắn với root.

Về đối chứng: MicroRank chỉ xếp root hạng 1 ở 2/26 ca RE2-TT và 0/22 ca Nezha-OB. Vì vậy ở k = 1 mọi đơn vị Nezha-OB **không có đối chứng đúng**, và ở RE2-TT đối chứng gần như luôn là `dev-57546fd87b`. Giới hạn này làm mọi so sánh đúng–sai của MicroRank yếu hơn các phương pháp khác.

### 2.1 Nhóm `RE2-TT|microrank_full|k=1|status:ERROR` và `k=5|status:ERROR` (4 đơn vị)

- **Đơn vị đọc:** `dev-03d4910932` (route|socket): `ValueError: No normal baseline for: ts-order-other-service_getMore ts.orders`. Cùng thao tác thiếu nền như ở TraceRCA (mục 1.1); cả 4 đơn vị cùng lý do.
- **Đối chứng cùng ô ở k = 5:** `dev-b8bd0abf60` (route|socket), root hạng 2. `ts-station-service` đứng trên root: thao tác của nó có mặt ở 630 trace A (tự mang cờ 73, ngữ cảnh 557), 90% trong đó gắn với root. Đếm riêng (M-C1) và bộ chia theo bài gốc đều đưa root lên hạng 1.
- **Phân loại:** như mục 1.1. Phép chia theo bài gốc cũng ERROR ở 4 ca này (thiếu mức nền của đúng thao tác đó).

### 2.2 Nhóm `RE2-TT|microrank_full|k=1|M5` và `k=5|M5` (5 đơn vị, hai đường đi)

- **`dev-7f1b6b071d` (travel|loss), hạng 11.** A = 605 trên 1.434 trace (42%); 406 trace A không chứa dịch vụ root; root tự mang cờ ở 179 trace A. Trên root 10 thực thể: 8 phía dưới root, 2 hai chiều; đứng đầu `ts-station-service` (tự có 153, ngữ cảnh 367, gắn root 0,29). Không thực thể nào có từ nửa số trace A gắn với root. Phép đổi: bỏ trọng số (A′) không đổi; đếm riêng lên hạng 4; cờ theo phần chưa phủ (M-D) không đổi; **chia theo bài gốc lên hạng 1**, khi đó 82% trace bất thường có root.
- **`dev-12a1a88069` (order|disk), hạng 11.** A = 558 (41%); 371 trace A không có root; root tự mang cờ ở 108. Trên root 10: 7 không liên hệ, 2 phía trên, 1 phía dưới; đứng đầu `ts-station-service` (168; 320; 0,24). Đếm riêng chỉ lên hạng 9; chia theo bài gốc lên hạng 2, và thực thể đứng đầu khi đó là `ts-auth-service`, một dịch vụ không liên hệ; chỉ 23% trace bất thường mới có root.
- **Đối chứng** (k = 1: `dev-57546fd87b`, auth|delay, khác ô; k = 5: `dev-14372e1209`, route|mem, khác ô): ở cả hai, root tự mang cờ ở hơn nửa số trace A (398/736 và 577/718). Ở hai đơn vị sai con số đó là 179/605 và 108/558.
- **Đọc:** cờ M5 đúng về vị trí (có dịch vụ hai chiều hoặc phía trên đứng trước root), nhưng thực thể đứng đầu và phần lớn thực thể trên root không nằm phía trên root. Điều kiện chung của hai ca sai: phần lớn trace A không dính tới root. Với ca thứ hai, sau khi thay bộ chia, root vẫn thua một dịch vụ không liên hệ; **chưa có giải thích** (thuộc phần 25–26/47 ca còn lại, `kiem-tiep.md` mục KT-3).

### 2.3 Nhóm `RE2-TT|microrank_full|k=1|M0` (19 đơn vị, sáu đường đi) và `k=5|M0` (8 đơn vị)

1. **Đường đi đông nhất (9 đơn vị): chia theo bài gốc và đếm riêng đều đưa root lên hạng 1 — `dev-14372e1209` (route|mem), hạng 2.** A = 718 (54%); chỉ 84 trace A không có root; root tự mang cờ ở 577. Một thực thể trên root: `ts-station-service` (tự có 129, ngữ cảnh 498), và **93% trace A chứa nó gắn với root**. A′, M-C1, M-D và bộ chia theo bài gốc đều đưa root lên hạng 1. **Đọc:** ở đây `ts-station-service` không ở trên chuỗi gọi tới root nhưng đi cùng trace với chuỗi của root; đếm phủ cho nó điểm của các trace mà root làm chậm. Đây là "đi cùng trace", khác "chờ root".
2. **Chia theo bài gốc không cứu, đếm riêng cứu (4 đơn vị) — `dev-3ae0a6c15a` (train|cpu), hạng 3.** Trên root: `ts-station-service` (185; 418; gắn root 0,83) và `ts-route-service` (70; 511; 0,94). A′ và M-C1 đưa root lên hạng 1. Chia theo bài gốc làm root **xuống hạng 5** (`ts-admin-travel-service` đứng đầu; 53% trace bất thường mới có root); luật chia của code cho hạng 4. **Đọc:** phản ví dụ cho câu "thay bộ chia là đủ": với root `ts-train-service`, bộ chia theo thời gian cả yêu cầu đưa một dịch vụ ở đầu chuỗi lên trên.
3. **`dev-a505ab3f65` (train|delay), hạng 3** (1 đơn vị): giống mục 2; chia theo luật của bài lên hạng 2 (`ts-route-service` đứng đầu), theo luật của code lên hạng 1. Hai luật cho hai kết quả khác nhau ở ca này.
4. **`dev-16597725c1` (auth|cpu), hạng 9** (3 đơn vị ở k = 5): A = 755 (57%); 504 trace A không có root. Tám thực thể trên root đều không liên hệ, tỷ lệ gắn root 0,00 (root không được dịch vụ nào gọi). A′ làm root tụt xuống hạng 11; đếm riêng và chia theo bài gốc đưa lên hạng 1 (97% trace bất thường mới có root). **Đọc:** hơn nửa số trace A là trace không đi qua root nhưng có một span nào đó vượt ngưỡng; đây là dạng rõ nhất của "bước chia quá rộng".
5. **`dev-8017c6dc70` (order|disk), hạng 7** và **`dev-1e6d61b5ec` (order|disk), hạng 8** (1 và 3 đơn vị): hai ca có tỷ lệ trace A thấp ngay ở bản gốc (12% và 11%), root tự mang cờ ở 26 và 12 trace. Chia theo bài gốc đưa lên hạng 1 và hạng 2 (`ts-auth-service` đứng đầu ở ca sau). Ở ca sau, đếm riêng không đổi hạng và A′ làm tệ đi. **Đọc:** khi root có rất ít span mang cờ (lỗi disk ở `ts-order-service` với ít lời gọi), không bước nào của bản thư viện cứu được; bộ chia theo bài gốc cải thiện nhưng chưa trọn.
6. **`dev-746fd74313` (auth|delay), hạng 10** (1 đơn vị, nhánh chia N/A): A = 831 (64%); A′ và M-C1 đưa root lên hạng 1; M-D xuống hạng 11. Bộ chia theo bài gốc không áp được: chỉ 83,5% trace sau mốc có đúng một span đầu, và thiếu mức nền của nhiều thao tác.
   - **Đối chứng cùng ô:** `dev-57546fd87b` (auth|delay), root hạng 1 dưới mọi nhánh. Hai ca có số đếm gần nhau (A 736 so với 831; trace A không có root 338 so với 440; root tự mang cờ 398 so với 391), nhưng điểm của root là 41,5 ở ca đúng và 4,15 ở ca sai, và thao tác cao nhất của root khác nhau (`find ts-auth-mongo.user` so với `UserRepository.findByUsername`). Ca sai là ca mất nhiều span nhất của dev (949/1.293 trace sau mốc có span mất cha). **Chưa phân xử** được mất span có phải lý do không; ghi ở `kiem-tiep.md` mục KT-3.

Nhóm `k=5|M0` gồm các đơn vị 4, 5, 6 ở trên; đối chứng ở k = 5 là `dev-14372e1209` (root hạng 2).

### 2.4 Nhóm `Nezha-OB|microrank_full|k=1|M5` (20 đơn vị, năm đường đi) và `k=5|M5` (14 đơn vị)

Không có đối chứng đúng ở k = 1. Ở k = 5 đối chứng là `dev-1ac905bc95` (frontend|return, root hạng 3): root là điểm vào nên có mặt ở mọi trace A.

1. **Không phép đổi nào cứu (6 đơn vị) — `dev-14701a3bbb` (shippingservice|cpu_contention), hạng 6.** A = 342 (45%); root tự mang cờ ở 60 trace. Năm thực thể trên root, đứng đầu `productcatalogservice` (tự có 10, ngữ cảnh 325, gắn root 0,42). A′ không đổi; M-C1 lên hạng 4; chia theo bài gốc giữ hạng 6 (`frontend` đứng đầu; 27% trace bất thường mới có root). Root chỉ đứng đầu ở các vị trí "phía gọi" của bảng A. **Đọc:** tín hiệu của root nằm ở span phía gọi (như mục 1.4 đường 1); MicroRank cũng gắn span đó cho dịch vụ gọi, và không phép đổi nào trong các bước của nó chạm tới điều này.
2. **Chia theo bài gốc tăng nhưng chưa tới hạng 1 (8 đơn vị) — `dev-2bfc97b01e` (checkoutservice|network_delay), hạng 8.** A = 225 (27%); 205 trace A không có root; root tự mang cờ ở 16. Bảy thực thể trên root, tỷ lệ gắn root 0,08. Không phép nào đổi đáng kể (hạng 7–8). **Đọc:** root ít lời gọi (31 span ở mục 1.4 đường 6) và gần như vắng trong nhóm A.
3. **Chia theo bài gốc cứu, đếm riêng không (4 đơn vị) — `dev-3e27669440` (adservice|cpu_contention), hạng 5.** A = 516 (62%); root tự mang cờ ở 333. Bốn thực thể trên root đều có 75–76% trace A gắn với root ("đi cùng trace"). M-C1 lên hạng 2; chia theo bài gốc lên hạng 1 (99% trace bất thường mới có root).
4. **`dev-9fd793feb7` (shippingservice|cpu_consumed), hạng 6** (1 đơn vị): M-C1 và chia theo bài gốc đều đưa lên hạng 1.
5. **`dev-9b9397a4dc` (recommendationservice|cpu_consumed), hạng 5** (1 đơn vị): M-C1 lên hạng 1; chia theo luật của bài làm root **xuống hạng 9** vì không trace bất thường mới nào có root (tỷ lệ 0,00), luật của code lên hạng 1. Số trace bất thường dưới bộ chia mới ở Nezha-OB rất ít (trung vị 12), nên hai luật có thể cho hai kết quả trái nhau; không đọc từng ca.
6. **`dev-55f99f3e0a` (checkoutservice|exception), hạng 8** (đường đi riêng ở k = 5): 379/402 trace A không có root; M-C1 không đổi; chia theo luật của bài lên hạng 1, luật của code hạng 4.

### 2.5 Nhóm `Nezha-OB|microrank_full|k=1|M0` (2 đơn vị) và `k=1|M6`, `k=5|M6` (1 đơn vị)

- **dev-1ac905bc95 (frontend|return), hạng 3.** Root ở điểm vào; hai thực thể trên root là dịch vụ root gọi. A′ cho hạng[1,3]; luật bài lên hạng 1, luật code giữ hạng 3. Kết quả không ổn định giữa luật; đáp ứng thời lượng do return còn OPEN (mục 1.5).
- **`dev-7b7c973198` (emailservice|network_delay), hạng [8, 9].** Root không tự mang cờ ở trace A nào (0/332); đây là nghĩa của cờ M6. Lời gọi tới root chậm ở 100% lời gọi, tín hiệu chỉ ở span phía gọi. Chia theo bài gốc cho hạng [1, 4]: root hòa với ba dịch vụ khác. Cùng ca với mục 1.7.

### 2.6 Điều rút ra từ phần đọc MicroRank

- Thực thể đứng trên root ở RE2-TT thuộc ba dạng khác nhau: **đi cùng trace với chuỗi của root** (`ts-station-service` có 83–93% trace A gắn root, ở các ca root là `ts-route-service`, `ts-train-service`); **không dính gì tới root** (các ca root `ts-auth-service`: tỷ lệ gắn root 0,00, hơn nửa trace A không có root); và **root quá ít span mang cờ** (các ca order|disk). Cùng một thực thể `ts-station-service` đứng đầu ở cả ba dạng, vì nó có mặt ở phần lớn trace.
- Bộ chia theo bài gốc là phép đổi mạnh nhất nhưng **có phản ví dụ đọc được**: `dev-3ae0a6c15a` (xuống hạng 5), `dev-9b9397a4dc` (xuống hạng 9 theo một luật), `dev-12a1a88069` và `dev-1e6d61b5ec` (dịch vụ không liên hệ khác lên đầu).
- Dịch vụ gọi root hiếm khi là lý do: ở các đơn vị đọc, thực thể phía trên root chưa bao giờ là thực thể đứng đầu.
- Ở Nezha-OB, 6 đơn vị cùng đường đi với `dev-14701a3bbb` không được phép đổi nào cứu; lý do đọc được là tín hiệu nằm ở span phía gọi.
- Thiếu đối chứng đúng là giới hạn thật: 0 ca đúng ở Nezha-OB, 2 ca ở RE2-TT.

## 3. BARO — 8 nhóm, 23 đơn vị đọc

Phiếu gọn: `runs/tong-hop-phien-12-001/phieu-gon/baro.txt`. Chuỗi tính: với từng cột metric, lấy median và IQR của đoạn nền; z = |x − median| / IQR, lấy lớn nhất ở đoạn sau mốc; điểm thực thể là z lớn nhất trong các cột của nó. BARO không nhận quan hệ gọi nào. Trong phiếu: "IQR/median" đo độ phẳng của cột ở nền (càng nhỏ càng phẳng); "lệch/median" đo mức đổi thật tại đỉnh so với mức nền. Hai số này cho phép tách "z lớn vì đổi nhiều" với "z lớn vì nền phẳng".

Phép B-1 (không lọc cột hằng) không đổi hạng root ở đơn vị nào đã đọc; cột tốt nhất của root không lần nào là cột được giữ thêm. Không nhắc lại ở từng mục.

### 3.1 Nhóm `RE2-TT|baro|k=1|M0` (6 đơn vị, bốn đường đi) và `k=5|M0` (2 đơn vị)

1. **Root gần như không có tín hiệu metric — `dev-57546fd87b` (auth|delay), hạng 41 trên 68** (2 đơn vị). Cột tốt nhất của root là mem với z = 3,1 và lệch/median 1%. Có 40 thực thể trên root: 20 không liên hệ, 20 không có span; đứng đầu `ts-order-other-service` cột latency, z = 97,5, lệch/median 192%. Thang độ lệch chuẩn (B-2) đưa root lên hạng 22, vẫn rất xa. Ở trace, root đứng đầu theo span của chính nó (`own_d`, `own_u`), và MicroRank xếp đúng ca này. **Đọc:** lỗi trễ mạng ở `ts-auth-service` không làm cột metric nào của root đổi đáng kể; BARO không có gì để xếp. **Phiên 13 (KT-12):** câu "không làm cột metric nào của root đổi đáng kể" chỉ đúng theo thang z. Cột latency của root ở ca này có trung vị 0,69 → 1,60; z nhỏ vì IQR nền 0,54 (`ket-qua-phien-13.md` mục 3).
   - **Đối chứng cùng ô (k = 5):** `dev-746fd74313` (auth|delay), root hạng 3; ở ca này cột latency của root có z = 30,7, lệch/median 293%. Cùng ô, cùng loại lỗi, nhưng cột latency của root phản ứng ở ca này và không phản ứng ở ca kia. **Chưa phân xử** vì sao; cần đọc chuỗi cột latency của root ở hai ca (`kiem-tiep.md` mục KT-12). **Phiên 13 (KT-12) đã phân xử một phần:** cột tăng ở cả hai ca; khác nhau là độ dao động của nền (IQR 0,023 so với 0,537).
2. **`dev-746fd74313` (auth|delay), hạng 3** (1 đơn vị). Trên root: `ts-user-service` cột mem z = 162 với lệch/median chỉ 0,29% trên nền có IQR/median 0,0018%; `ts-contacts-service` cột latency z = 139,7, lệch/median 125%. B-2 làm root xuống hạng 5. **Đọc:** hai thực thể trên root thuộc hai loại khác nhau: một cột gần phẳng bị chia cho IQR rất nhỏ; một cột đổi thật ở dịch vụ không liên hệ.
3. **`dev-14372e1209` (route|mem), hạng 2** (2 đơn vị). Root: mem z = 3.907, lệch/median 176%. Trên root: `ts-consign-price-service` cột latency z = 7.066, lệch/median 645%, lưu lượng qua nó có đổi. B-2 đưa root lên hạng 1.
   - **Đối chứng cùng ô:** `dev-16870e660c` (route|mem), root hạng 1 với z = 9.738,5, lệch/median 187%. Hai ca có mức đổi tương đối của root gần nhau (176% và 187%) nhưng z chênh 2,5 lần, vì IQR/median của nền là 0,045% ở ca sai và 0,019% ở ca đúng. **Đọc:** độ lớn của z do độ phẳng của nền quyết định nhiều hơn do độ lớn của sự cố.
4. **`dev-59f696a169` (auth|cpu), hạng 2** (1 đơn vị). Root: mem z = 102,5, lệch/median 2%. Trên root: `ts-station-service` cột mem z = 103,0, lệch/median 0,32%, IQR/median 0,0031%, thuộc nhóm "bậc tại mốc". B-2 đưa root lên hạng 1.
   - **Đối chứng cùng ô:** `dev-3defe3d34b` (auth|cpu), root hạng 1, mem z = 382, lệch/median 2%. Cùng mức đổi 2% ở root; z khác nhau (102 và 382) vì IQR/median khác nhau (0,017% và 0,0048%).
   - **Đọc, xác nhận ở mức tính toán cho ca này:** một cột mem của dịch vụ không liên hệ đổi 0,32% thắng cột của root đổi 2%, vì nền của nó phẳng hơn 5 lần. Đổi riêng thang chia trả lại hạng 1.

### 3.2 Nhóm `RE2-TT|baro|k=1|M5` (3 đơn vị, ba đường đi) và `k=5|M5` (2 đơn vị)

- **`dev-a915aa2424` (travel|loss), hạng 29.** Cột tốt nhất của root: cpu z = 4,8. Trên root 28 thực thể ở đủ mọi vị trí (4 phía trên, 2 hai chiều, 8 phía dưới, 4 không liên hệ, 10 không có span); đứng đầu `ts-auth-service` cột mem z = 189 với lệch/median 0,62%. B-2 lên hạng 16.
  - **Đối chứng cùng ô:** `dev-7f1b6b071d` (travel|loss), root hạng 1 với cột mem z = 103,3, lệch/median 4%. Cùng loại lỗi: ở ca đúng cột mem của root dịch 4% trên nền phẳng và thắng; ở ca sai root không có cột nào dịch.
  - **Đọc:** cờ M5 có vì 4 dịch vụ phía trên đứng trước root, nhưng cùng lúc 24 thực thể khác cũng đứng trước. Root thua vì không có tín hiệu metric, không vì dịch vụ gọi.
- **`dev-a5cabe5fa7` (travel|loss), hạng 16.** Root: mem z = 17,3, lệch/median 0,35%. Trên root: `ts-order-other-service` cột latency z = 211 (phía dưới root, lệch/median 282%); bốn dịch vụ không có span (`ts-admin-route-service`, `ts-rebook-service`, `ts-execute-service`, `ts-admin-user-service`) có cột cpu đổi 327–402% so với nền. B-2 chỉ lên hạng 15. **Đọc:** nhiều dịch vụ không nằm trong trace có cpu tăng gấp 3–4 lần đúng lúc sự cố. **Không phân xử được bằng dữ liệu hiện có** đây là tài nguyên chung của máy, tải chung hay tác dụng phụ của công cụ tiêm lỗi (`kiem-tiep.md` mục KT-6).
- **`dev-f36d0647d5` (order|loss), hạng 4.** Root: diskio z = 77. Trên root cả ba đều nằm phía trên root: `ts-travel2-service` cột mem z = 270 (lệch/median 4%), `ts-security-service` cột latency z = 151 (lệch/median 1.250%), `ts-seat-service` cột latency z = 90 (175%, bậc tại mốc). B-2 không đổi hạng.
  - **Đối chứng cùng ô:** `dev-20acb4402d` (order|loss), root hạng 1 với cột latency z = 4.209,5, lệch/median 11.320%.
  - **Đọc:** đây là ca BARO duy nhất đã đọc ở RE2-TT mà thực thể trên root đều là dịch vụ gọi và hai trong ba cột thắng là cột độ trễ đổi thật. Nó khớp với việc dịch vụ gọi chờ root (cùng ca ở mục 1.2: 61% và 85% span mang cờ của `ts-seat-service`, `ts-travel-service` là span chờ root). Bảng không nối từng cột với từng lời gọi, nên giữ ở mức quan sát.

Nhóm `k=5|M5` gồm hai đơn vị đầu; đối chứng như trên.

### 3.3 Nhóm `Nezha-OB|baro|k=1|M0` (7 đơn vị, ba đường đi) và `k=5|M0` (3 đơn vị)

Metric của Nezha-OB chỉ có 5 mẫu mỗi phía, nên median và IQR ước lượng từ 5 điểm. Đối chứng dùng chung là `dev-14701a3bbb` (shippingservice|cpu_contention; khác ô): root hạng 1 với cột mức dùng CPU z = 342, lệch/median 2.869%.

- **`dev-7b7c973198` (emailservice|network_delay), hạng 4** (2 đơn vị). Root: cột độ trễ phía gọi P90, z = 10,4 dù lệch/median 878%, vì IQR/median của nó là 85%. Trên root là ba dịch vụ không liên hệ với z 13–24 và lệch/median 18–451%. B-2 lên hạng 3.
- **dev-5ada15752d (frontend|return), hạng 8** (2 đơn vị) và **dev-1ac905bc95, hạng 10/10** (3 đơn vị). Root z=3,9 và 1,2; mọi thực thể trên root là dịch vụ root gọi, lưu lượng một số dịch vụ đó đổi. B-2 không đổi hạng. Quan sát là khác biệt giữa lưu lượng phía dưới và điểm metric của root; chưa quy thay đổi ấy cho lỗi return hoặc khẳng định metric root không đổi từ hạng thấp.

### 3.4 Nhóm `Nezha-OB|baro|k=1|M5` (7 đơn vị, năm đường đi) và `k=5|M5` (3 đơn vị)

1. **`dev-27252dca60` (productcatalogservice|exception), hạng 7** (2 đơn vị). Root z = 3,2. Trên root 6 thực thể, đứng đầu `cartservice` cột độ trễ phía server P95 z = 28,5 với lệch/median 13% trên nền IQR/median 0,46%. B-2 đưa root lên hạng 2 (5 cặp mất). Lỗi `exception` gần như không để lại tín hiệu metric ở root.
2. **`dev-55f99f3e0a` (checkoutservice|exception), hạng 4** (2 đơn vị). Root: độ trễ phía gọi P99 z = 14,2. Trên root: `productcatalogservice` z = 492 (lệch/median 99%, IQR/median 0,2%), `frontend` z = 157 (phía trên), `adservice` z = 63.
   - **Đối chứng cùng ô:** `dev-b0f8b2e3ac` (checkoutservice|exception), root hạng 1 với độ trễ phía server P99 z = 194,5, lệch/median 393%. B-2 làm chính ca đúng này xuống hạng 4. **Đọc:** cùng ô, cột phản ứng của root khác nhau giữa hai ca; và thang độ lệch chuẩn không phải cách chữa ở Nezha-OB (5 mẫu).
3. **`dev-5467884de4` (recommendationservice|network_delay), hạng 4** (1 đơn vị). Root: độ trễ phía server P99 z = 64, lệch/median 531%. Trên root: `frontend` (gọi trực tiếp root) cột độ trễ phía gọi P95 z = 177, lệch/median 707%; hai dịch vụ không liên hệ. **Đọc:** cột độ trễ phía gọi của dịch vụ gọi đổi nhiều hơn cột của root, khớp với lỗi trễ mạng nằm trên đường tới root (mục 1.4 đường 7).
4. **`dev-9fd793feb7` (shippingservice|cpu_consumed), hạng 4** (1 đơn vị). Root: độ trễ phía gọi P90 lệch/median 2.312% nhưng z chỉ 50, vì IQR/median của cột là 46%. Ba thực thể trên root có lệch/median 100–806% nhưng IQR/median 0,4–8%. B-2 đưa root lên hạng 1. **Đọc:** root đổi gấp 23 lần mức nền vẫn thua cột đổi gấp đôi có nền phẳng. Cùng cơ chế với mục 3.1 điểm 4.
5. **`dev-6c9afc9822` (emailservice|network_delay), hạng 2** (1 đơn vị). Root: lệch/median 9.880%, z = 98 (IQR/median 101%). Trên root: `checkoutservice` (gọi trực tiếp root) cột độ trễ phía server P99 z = 150 với lệch/median 152% và IQR/median 1%. B-2 đưa root lên hạng 1. **Đọc:** dịch vụ gọi có độ trễ tăng 1,5 lần (khớp với chờ root) và thắng root tăng 99 lần, do thang IQR.
6. **`dev-63c30faf34` (recommendationservice|network_delay), hạng 7** (riêng ở k = 5). Cột tốt nhất của root là lưu lượng mạng nhận, z = 8,9. Sáu thực thể trên root; B-2 làm root xuống hạng 9.
   - **Đối chứng cùng ô (k = 5):** `dev-5467884de4` (hạng 4), nơi cột độ trễ phía server của root có z = 64. Cùng ô, một ca cột độ trễ của root phản ứng, một ca không. **Phiên 13 (KT-12):** z = 64 đến từ một mẫu P99 trong 5 mẫu; trung vị các cột độ trễ của root giảm sau mốc ở cả hai ca.

### 3.5 Điều rút ra từ phần đọc BARO

- Có **ba đường thất bại khác nhau**: (i) cột metric của root gần như không đổi (z của root từ 1 tới 5: auth|delay, travel|loss, frontend|return, productcatalogservice|exception); (ii) root đổi thật và đổi nhiều nhưng thua cột có nền phẳng hơn, tức thang IQR (mục 3.1 điểm 3, 4; 3.4 điểm 4, 5), B-2 gỡ được; (iii) cột của dịch vụ khác đổi thật tại mốc (lệch/median hàng trăm phần trăm), B-2 không gỡ được, và nguyên nhân vật lý chưa biết.
- So ca đúng với ca sai **cùng ô** ở RE2-TT (ba cặp): mức đổi tương đối của root gần bằng nhau, còn z khác nhau 2,5–4 lần theo độ phẳng của nền. Vậy "z lớn" không đo độ lớn của sự cố.
- Dịch vụ gọi root đứng trên root với cột độ trễ đổi thật thấy ở ba đơn vị (`dev-f36d0647d5`, `dev-5467884de4`, `dev-6c9afc9822`). Ở hai trong ba, đổi thang đã đủ đưa root lên; quan hệ gọi không phải thứ duy nhất chạm được tới chúng.
- Ở Nezha-OB mọi kết luận về thang chia yếu vì chỉ có 5 mẫu; B-2 giúp ca này và làm hỏng ca khác.

## 4. SimpleRCA (M4, quy ước T-017) — 9 nhóm, 18 đơn vị đọc

Phiếu gọn: `runs/tong-hop-phien-12-001/phieu-gon/simplerca.txt`. Chuỗi tính: mỗi mẫu metric sau mốc vượt mean + 3·std của nền là một phiếu (RE2-TT có 300 mẫu mỗi cột, Nezha-OB có 5); trace và log mỗi kênh cho 0 hoặc 1 phiếu; điểm = phiếu metric + phiếu trace + phiếu log. Phân rã cộng đã kiểm bằng số ở 52/52 ca. Trong phiếu, "m, t, l" là ba loại phiếu; "cột-max" là cột nhiều phiếu nhất của thực thể.

### 4.1 Nhóm `RE2-TT|simplerca|k=1|M5` (5 đơn vị, ba đường đi) và `k=5|M5` (1 đơn vị)

1. **`dev-20acb4402d` (order|loss), hạng 15** (1 đơn vị; cũng là đơn vị của `k=5|M5`). Root: 240 phiếu metric (5/8 cột có phiếu) + 1 phiếu trace = 241. Trên root 14 thực thể: 6 không liên hệ, 7 không có span, 1 phía trên. Năm thực thể đầu đều có cột nhiều phiếu nhất là mem với 280–300 phiếu trên 300 mẫu (`ts-consign-price-service` 449 phiếu, `ts-auth-service` 438…); riêng một cột đó đã nhiều hơn tổng điểm của root. Đếm theo cột (S-1) đưa root lên hạng 1, cả 14 cặp mất.
   - **Đối chứng cùng ô:** `dev-260d332c8d` (order|loss), root hạng 1 với 595 phiếu metric.
   - **Đối chiếu cùng ca với BARO** (chỉ để biết kênh, không thay đối chứng): BARO xếp root của `dev-20acb4402d` hạng 1, cột latency của root có z = 4.209,5 (mục 3.2). Vậy root có tín hiệu metric rất mạnh ở ca này; SimpleRCA thua vì đếm số mẫu vượt ngưỡng: cột mem của dịch vụ khác vượt ngưỡng gần suốt cửa sổ được 300 phiếu, còn root chỉ được 240 phiếu qua mọi cột.
   - **Kết luận, xác nhận ở mức tính toán cho ca này:** trong điều kiện có cột vượt ngưỡng kéo dài ở dịch vụ khác, bước đếm theo mẫu làm mất thông tin "biên độ đổi" và "bao nhiêu kênh cùng đổi". Cờ M5 có vì một dịch vụ phía trên đứng trước root, nhưng 13/14 thực thể trên root không nằm phía trên.
2. **`dev-7f1b6b071d` (travel|loss), hạng 3** (3 đơn vị). Root: 885 + 1 + 1 = 887. Trên root: `ts-admin-travel-service` (phía trên) 954 + 1 + 1, cột nhiều phiếu nhất là latency-50 với 291 phiếu, thuộc nhóm "bậc tại mốc"; `ts-seat-service` (hai chiều) 917 + 1 + 1, cột latency-90 với 269 phiếu. Chênh 69 và 32 phiếu trên khoảng 900. S-1 không đổi hạng.
   - **Đối chứng cùng ô:** `dev-a5cabe5fa7` (travel|loss), root hạng 1 với 884 phiếu metric. Số phiếu metric của root ở ca đúng và ca sai gần như bằng nhau (884 và 885). Thứ khác là dịch vụ gọi có cột độ trễ vượt ngưỡng suốt cửa sổ hay không.
   - **Đọc:** đây là dạng "nhầm triệu chứng với nguyên nhân" ở kênh metric: cột độ trễ của dịch vụ gọi vượt ngưỡng lâu ngang cột của root, nên được số phiếu ngang root, cộng thêm vài phiếu ở cột khác là vượt. Bảng không nối cột độ trễ với từng lời gọi tới root; giữ ở mức quan sát khớp với mục 1.2.
3. **`dev-a915aa2424` (travel|loss), hạng 2** (1 đơn vị). Root 803 + 1; `ts-admin-travel-service` 813 + 1, cột nhiều phiếu nhất là mem 296 phiếu (bậc tại mốc). Chênh 10 phiếu. S-1 cho hạng [1, 3].

### 4.2 Nhóm `Nezha-OB|simplerca|k=1|M0` (6 đơn vị, bốn đường đi), `k=5|M0`, `k=5|M3`

Ở Nezha-OB mỗi cột chỉ có 5 mẫu sau mốc, nên phiếu metric rất nhỏ và chênh 1–2 phiếu đã đổi hạng. Đối chứng dùng chung: `dev-14701a3bbb` (shippingservice|cpu_contention; khác ô), root hạng 1 với 27 phiếu metric ở 7/16 cột.

- **`dev-515c5f2190` (recommendationservice|cpu_consumed), hạng 2** (3 đơn vị): root 2 + 1 = 3; `adservice` (không liên hệ) 4 phiếu. Chênh 1 phiếu. Trace có tín hiệu rõ (root đứng đầu ở cả năm vị trí của bảng A, lời gọi tới root chậm 95%), nhưng kênh trace chỉ góp 1 phiếu.
- **`dev-8ecd9880ed` (checkoutservice|return), hạng [4, 5]** (1 đơn vị): root 3 + 0 + 1 = 4; ba thực thể trên root có 8–15 phiếu, cột nhiều phiếu nhất là bộ nhớ.
- **dev-1ac905bc95 và dev-5ada15752d (frontend|return), hạng[5,6] và 6:** root 0 phiếu metric ở 0/21 cột, 1 phiếu log; các thực thể trên root là dịch vụ root gọi. Không có phiếu theo ngưỡng này không đồng nghĩa metric không đổi do lỗi; đáp ứng return chưa phân xử.

### 4.3 Nhóm `Nezha-OB|simplerca|k=1|M5` (9 đơn vị, sáu đường đi), `k=5|M5`, `k=1|M6`, `k=5|M6`

1. **`dev-3b92690644` (checkoutservice|return), hạng 2** (4 đơn vị): root 17 + 0 + 1 = 18; `frontend` (gọi trực tiếp root) 31 + 0 + 1 = 32, cột nhiều phiếu nhất là độ trễ phía trước P90 (4/5 mẫu). S-1 không đổi.
2. **`dev-396c8dbf7d` (emailservice|cpu_consumed), hạng 2** (1 đơn vị): root 31 + 1 = 32; `checkoutservice` (gọi trực tiếp) 37 + 1 = 38. S-1 đưa root lên hạng 1.
3. **`dev-b0f8b2e3ac` (checkoutservice|exception), hạng 3** và **`dev-6c9afc9822` (emailservice|network_delay), hạng 4**: thực thể trên root gồm cả dịch vụ không liên hệ lẫn dịch vụ gọi; chênh 1–7 phiếu.
4. **Root không có phiếu nào (cờ M6):**
   - **`dev-607751ac0a` (checkoutservice|network_delay), hạng [9, 10].** Root 0 + 0 + 0. **Đối chứng cùng ô:** `dev-2bfc97b01e` (checkoutservice|network_delay), root hạng 1 với 16 phiếu ở 5/16 cột. Cùng ô, root có phiếu ở ca này và không có ở ca kia; lời gọi tới root chậm ở 9% (ca sai) và 26% (ca đúng) số lời gọi. Hai ca cùng loại lỗi có cường độ quan sát được khác nhau. **Phiên 13 (KT-12):** về cột độ trễ của root thì không ca nào trong hai ca phản ứng; z = 94 ở `dev-2bfc97b01e` là do IQR của 5 mẫu nền.
   - **`dev-63c30faf34` (recommendationservice|network_delay), hạng [8, 10].** Root 0 phiếu; `frontend` (gọi trực tiếp) 26 + 1, cột độ trễ phía trước P50. Lời gọi tới root chậm ở 97% lời gọi và root đứng đầu ở ba vị trí phía gọi của bảng A. **Đối chứng cùng ô (k = 5):** `dev-5467884de4`, root hạng 5 với 3 phiếu; `frontend` 28 + 1.
   - **Đọc:** với lỗi trễ mạng, metric của root không vượt ngưỡng; metric độ trễ của dịch vụ gọi vượt. Tín hiệu có trong trace ở span phía gọi (mục 1.4 đường 7), nhưng SimpleRCA chỉ cho trace 1 phiếu và gắn nó theo dịch vụ.

### 4.4 Điều rút ra từ phần đọc SimpleRCA

- Ở RE2-TT có hai đường: **cột vượt ngưỡng kéo dài của dịch vụ không liên hệ** (đa số là mem; S-1 gỡ được) và **cột độ trễ của dịch vụ gọi vượt ngưỡng lâu ngang root** (S-1 không gỡ được; đây là phần đi theo quan hệ gọi). Ba trong năm ca sai của RE2-TT có thực thể đứng đầu nằm phía trên root.
- So ca đúng và ca sai cùng ô (travel|loss): phiếu metric của root bằng nhau; kết quả do cột của dịch vụ khác quyết định.
- Bằng chứng trace và log của root không bao giờ bù được: mỗi kênh tối đa 1 phiếu, trong khi một cột metric có tới 300 phiếu.
- Ở Nezha-OB, điểm chỉ cỡ 0–38 phiếu; bốn đơn vị đã đọc có root 0 phiếu metric. Các kết luận ở Nezha-OB là về thiếu tín hiệu và số mẫu ít, không phải về cách cộng phiếu.

## 5. CIRCA (OLS, đồ thị kiến trúc; chỉ RE2-TT) — 6 nhóm, 12 đơn vị đọc

Phiếu gọn: `runs/tong-hop-phien-12-001/phieu-gon/circa_ols_da.txt`. Chuỗi tính: mỗi cột metric là một nút; hồi quy nút theo các nút cha trên 111 điểm trước mốc; điểm RHT là phần dư của 10 điểm cuối cửa sổ chia cho độ lệch chuẩn phần dư train; bước DA cộng điểm của hậu duệ vào tổ tiên; thứ hạng lấy theo khóa sau DA. Trong phiếu: "RHT" là hạng root trước DA, "DA" là hạng chính thức, "K2" là hạng khi bỏ mọi cạnh (bảng RHT), "k2x" chỉ giữ cạnh cùng dịch vụ, "k2s" chỉ giữ cạnh giữa hai dịch vụ.

### 5.1 Nhóm `RE2-TT|circa_ols_da|k=1|M4` (8 đơn vị, hai đường đi)

- **`dev-3ae0a6c15a` (train|cpu), hạng 4** (7 đơn vị cùng đường đi). Có một nút cực lớn: `ts-admin-travel-service_latency`, 7 nút cha, độ lệch chuẩn của y ở đoạn train 9,3e-17, điểm RHT 1,7e16; cùng nút đó khi không có cha có điểm 0,24. Hạng root: 2 trước DA, 4 sau DA. Ba thực thể trên root sau DA đều mang khóa cực lớn: `ts-travel-service` và `ts-travel2-service` (gọi trực tiếp root; không đứng trên root trước DA) và `ts-admin-travel-service`. Bỏ mọi cạnh: root hạng 1; chỉ bỏ một loại cạnh: hạng 2.
- **`dev-03d4910932` (route|socket), hạng 4** (1 đơn vị): cùng nút cực lớn (RHT 4e16; không cạnh 0,72); hạng root 4 cả trước và sau DA; bỏ mọi cạnh lên hạng 1.
  - **Đối chứng cùng ô:** `dev-bcbd4f46ae` (route|socket), root hạng 1, **không có nút cực lớn**. Cùng ô, cùng loại lỗi: ca sai là ca mà cột độ trễ của `ts-admin-travel-service` đứng yên trong 111 giây train, ca đúng thì không.
- **Đọc từ bảng đủ 30 ca** (`doi-chieu-dung-sai.json`, các đơn vị CIRCA): cả 8 đơn vị của nhóm M4 có nút cực lớn, có đúng 3 thực thể trên root và cả 3 đều mang khóa cực lớn; bỏ mọi cạnh thì root hạng 1 ở 8/8. Ba ca còn lại có nút cực lớn (`dev-7f1b6b071d`, `dev-a5cabe5fa7`, `dev-f9a8e05ed7`) là ca **đúng**, và ở cả ba root lên hạng 1 nhờ chính nó nhận giá trị cực lớn qua DA (hạng trước DA là 8, 7, 2).
- **Kết luận, xác nhận ở mức tính toán:** trong điều kiện một cột đứng yên ở đoạn train, bước chuẩn hóa phần dư sinh giá trị cực lớn, bước DA chuyển nó sang các dịch vụ kề trên đồ thị metric. Thứ hạng của 11 ca này, đúng hay sai, do việc root có nằm trên đường nhận giá trị đó hay không quyết định. Ba ca đúng nói trên là đúng do hiện tượng số học, không do phương pháp định vị được root.

### 5.2 Nhóm `RE2-TT|circa_ols_da|k=1|M5` (10 đơn vị, bốn đường đi)

Tám đơn vị trùng nhóm M4 (mục 5.1). Hai đơn vị còn lại không có nút cực lớn:

- **`dev-a915aa2424` (travel|loss), hạng 3.** Hạng 3 cả trước và sau DA. Trên root: `ts-user-service` (không liên hệ) và `ts-seat-service` (gọi trực tiếp root). Bỏ mọi cạnh làm root **xuống hạng 29**; chỉ giữ cạnh cùng dịch vụ: hạng 11; chỉ giữ cạnh giữa hai dịch vụ: hạng 4. **Đọc:** ở ca này hồi quy theo nút cha đang giúp root rất nhiều (cột độ trễ của root, sau khi trừ phần giải thích bởi nút cha, nổi lên); phần giúp đến chủ yếu từ cạnh giữa hai dịch vụ. Đây là một ca cho thấy cấu trúc có ích, không phải có hại.
  - **Đối chứng cùng ô:** `dev-7f1b6b071d` (travel|loss), root hạng 1, nhưng là một trong ba ca "đúng nhờ giá trị cực lớn" (hạng trước DA là 8). Vì vậy **cặp này không phải đối chứng sạch**; không có ca travel|loss nào CIRCA đúng mà không dính giá trị cực lớn (`dev-a5cabe5fa7` cũng vậy).
- **`dev-f36d0647d5` (order|loss), hạng 2.** Hạng 5 trước DA, 2 sau DA; còn `ts-travel2-service` (phía trên gián tiếp) đứng trên. Bỏ cạnh: hạng 6.
  - **Đối chứng cùng ô:** `dev-20acb4402d` (order|loss), root hạng 1; hạng 3 trước DA, 1 sau DA; bỏ cạnh: hạng 3. **Đọc:** ở hai ca order|loss, không có giá trị cực lớn, bước DA nâng root lên (5 → 2 và 3 → 1) và bỏ cạnh làm root kém đi. Đây là hai ca DA có ích thật.

### 5.3 Nhóm `RE2-TT|circa_ols_da|k=1|M0` (4 đơn vị, hai đường đi) và `k=5|M0` (3 đơn vị)

- **`dev-16597725c1` (auth|cpu), hạng 15** (3 đơn vị). Không có nút cực lớn. Hạng root: **2 trước DA, 15 sau DA**. 14 thực thể trên root đều không liên hệ; chỉ 1 trong 14 đứng trên root trước DA. Bỏ cạnh: root hạng 1.
  - **Từ bảng đủ 30 ca:** ba đơn vị cùng đường đi này (`dev-16597725c1` 2 → 15, `dev-57546fd87b` 40 → 46, `dev-f81f88234e` 10 → 22) đều có root là `ts-auth-service`, dịch vụ không có cạnh gọi nào trong trace.
  - **Đối chứng cùng ô:** `dev-3defe3d34b` (auth|cpu), root hạng 1 cả trước và sau DA.
  - **Đọc lúc đầu (đã bị phép kiểm KT-15 sửa):** tôi đã đọc là "DA bất lợi cho dịch vụ đứng riêng, vì dịch vụ đứng riêng không được cộng gì". Phép kiểm KT-15 chạy sau đó (`runs/circa-da-addition-001/summary.json`) cho thấy cách đọc này **sai về cơ chế**: root `ts-auth-service` có 5 hậu duệ trong đồ thị metric và cũng được cộng (405,65 ở ca này).
  - **Đọc đúng, theo KT-15:** DA cộng cho mỗi nút có điểm từ 3 trở lên điểm lớn nhất của các nút con của nó. Ở ca này nút `ts-preserve-service_latency` có điểm 2.027,36, cao nhất bảng trước DA; cả 13 thực thể vượt root sau DA đều nhận đúng giá trị đó. Root (điểm 823,68 trước DA, 1.229,32 sau DA) bị 13 thực thể được cộng 2.027,36 vượt qua. Ở hai ca còn lại: 11/12 và 4/7 thực thể vượt root nhận cùng một giá trị từ một nút nguồn. Ở đối chứng, root dẫn đầu đủ xa nên không bị vượt. **Mức kết luận: quan sát trên trung gian**, đẳng thức "khóa sau DA = điểm trước DA + điểm lớn nhất của nút con" đúng ở 1.574/1.574 nút được cộng. Đây là cùng kiểu với mục 5.1 (một điểm lớn của một nút kéo các nút cha lên), chỉ khác là điểm ở đây không phải giá trị lỗi số học mà là một thay đổi thật ở dịch vụ không liên quan. **Phiên 13 (KT-9):** điểm 2.027,36 đó có dưới đoạn học 111 điểm; trong nhánh chẩn đoán học trên 291 điểm, root của ca này về hạng 1 sau DA. Chữ "thay đổi thật" ở cuối đoạn này viết quá tay.
- **`dev-746fd74313` (auth|delay), hạng 4** (1 đơn vị). Hạng 4 dưới mọi nhánh. Ba thực thể trên root không liên hệ, đứng trên root cả khi bỏ cạnh. Cột tốt nhất của root là socket. **Đọc:** cấu trúc không đóng vai trò; root thiếu tín hiệu metric, như mục 3.1 điểm 1 và 2.

### 5.4 Nhóm `Nezha-OB|circa_ols_da|k=1|status:UNSUPPORTED` và `k=5|…` (22 đơn vị)

- **Đơn vị đọc:** `dev-14701a3bbb`. Lý do ghi trong bản ghi (Q-85): metric của Nezha-OB chỉ có 1–2 phép đo thật trong đoạn train; ở 19/22 ca bộ nạp gốc nội suy đuôi đoạn train về điểm sau mốc, làm nền lẫn dữ liệu sau mốc. Không có ca đúng nào để đối chứng.
- **Phân loại:** dữ liệu (nhịp metric khoảng 60 giây) không đáp ứng giả định của cách tính (cần chuỗi train đủ dài). Không rút được kết luận nào về CIRCA trên Nezha-OB.

### 5.5 Điều rút ra từ phần đọc CIRCA

- Ba hiện tượng tách được bằng cách đặt hạng trước DA, sau DA và không cạnh cạnh nhau: **giá trị cực lớn** (11 ca: 8 sai, 3 đúng nhờ may), **DA chuyển điểm lớn của một nút không liên quan cho mọi nút cha của nó** (3 ca root `ts-auth-service`; cách đọc "bất lợi cho dịch vụ đứng riêng" đã bị KT-15 sửa, xem mục 5.3), **DA và hồi quy có ích** (2 ca order|loss; 1 ca travel|loss nơi bỏ cạnh làm root tụt từ 3 xuống 29).
- Không dùng số Hit của CIRCA để nói "cấu trúc gọi giúp" hay "hại" khi chưa loại 11 ca dính giá trị cực lớn.

## 6. TORAI B (chỉ RE2-TT, ba seed) — 4 nhóm, 7 đơn vị đọc

Phiếu gọn: `runs/tong-hop-phien-12-001/phieu-gon/torai_B.txt`. Chuỗi tính: mỗi dịch vụ có vectơ bốn số (metric, log, độ trễ trace, lỗi trace), mỗi số là phần của dịch vụ trong tổng điểm của nguồn đó; severity là trung bình bốn số; phân cụm; cụm xếp theo severity; trong cụm nhiều dịch vụ dùng RCD, không đủ thì theo severity. Nguồn lỗi trace bằng 0 ở mọi ca.

### 6.1 Nhóm `RE2-TT|torai_B|k=1|M0` (9 đơn vị = 3 ca × 3 seed, hai đường đi)

- **`dev-16597725c1` seed 0 (auth|cpu), hạng 3** (7 đơn vị cùng đường đi). Vectơ của root: metric 0,116; log 0,015; độ trễ trace 0,076; severity 0,052. Trên root: `ts-order-other-service` severity 0,079 và `ts-seat-service` 0,057. So từng nguồn với root: metric −0,106 và −0,102 (root cao hơn), **log +0,175 ở cả hai**. Root nằm trong cụm 25 dịch vụ, xếp theo nhánh dự phòng. Bỏ cột log nền không đổi (tl2) và bỏ nguồn log (tl1) đều đưa root lên hạng 1, giống nhau ở ba seed.
  - **Đối chứng cùng ô:** `dev-3defe3d34b` seed 0 (auth|cpu), root hạng 1: metric 0,386; log 0,000; độ trễ trace 0,102; severity 0,122; cụm một dịch vụ. Cùng ô: phần metric của root là 0,386 ở ca đúng và 0,116 ở ca sai; phần log của root gần 0 ở cả hai. **Đọc:** root thắng khi phần metric của nó đủ lớn để bù việc không có điểm log; ở ca sai, hai dịch vụ có mẫu log đổi theo thời gian được 0,19 điểm log và vượt lên.
- **`dev-a5cabe5fa7` seed 1 (travel|loss), hạng 2** (2 đơn vị: seed 1 và seed 2). Root: metric 0,018; log 0,015; độ trễ trace 0,246; severity 0,070. Trên root: `ts-order-other-service` severity 0,134 (metric +0,124; log +0,167; độ trễ trace −0,035). Bỏ nguồn log: hạng 1 ở seed 0, hạng 2 ở seed 1 và 2; tức kết quả phụ thuộc seed.
  - **Đối chứng cùng ô:** `dev-7f1b6b071d` seed 0 (travel|loss), root hạng 1: metric 0,105; **log 0,435**; độ trễ trace 0,335. Ở ca đúng chính root có phần log lớn. **Đọc:** nguồn log không phân biệt dịch vụ gốc với dịch vụ có log đổi; khi nó nghiêng về root thì đúng, nghiêng về dịch vụ khác thì sai.

### 6.2 Nhóm `RE2-TT|torai_B|k=1|M5` (3 đơn vị = 1 ca × 3 seed)

- **`dev-f36d0647d5` seed 0 (order|loss), hạng 3.** Root: metric 0,089; log 0,029; độ trễ trace 0,213; severity 0,083. Trên root là hai dịch vụ phía trên root: `ts-travel2-service` (metric +0,042; log +0,115; độ trễ trace +0,028) và `ts-seat-service` (log +0,109; độ trễ trace +0,032). Bỏ cột log hay bỏ nguồn log đều giữ hạng 3 ở cả ba seed.
  - **Đối chứng cùng ô:** `dev-20acb4402d` seed 0 (order|loss), root hạng 1: metric 0,210; độ trễ trace 0,158.
  - **Đọc:** log là nguồn chênh lớn nhất, nhưng metric và độ trễ trace cũng nghiêng về hai dịch vụ gọi, nên bỏ log không cứu. Phần độ trễ trace nghiêng về dịch vụ gọi khớp với mục 1.2 (span của `ts-seat-service` dài theo lời gọi tới root). Đây là ca TORAI duy nhất có thực thể trên root nằm phía trên root.

### 6.3 Nhóm `Nezha-OB|torai_B|k=1|status:UNSUPPORTED` và `k=5|…` (22 đơn vị)

- **Đơn vị đọc:** `dev-14701a3bbb`. Lý do (Q-85): lược đồ trace của Nezha-OB không có mã trạng thái để dựng bảng lỗi trace; nhịp metric khoảng 60 giây không khớp bước 15 hàng của TORAI. Không có đối chứng. Phân loại: thiếu đầu vào ở dữ liệu.

### 6.4 Điều rút ra từ phần đọc TORAI B

- Ở cả bốn ca sai, root mất hạng ở bước severity; bước phân cụm và bước RCD không quyết định.
- Ba đối chứng cùng ô cho thấy root thắng khi một nguồn của chính nó đủ lớn (metric 0,386; log 0,435; metric 0,210). Nguồn log nghiêng theo dịch vụ có mẫu log mới, không theo root.
- Bảng log là bảng do ta dựng (nguồn B); với bảng của tác giả hiện tượng không lặp lại (KQ11 mục 6). Phần đọc này vì vậy nói về cấu hình chính của ta, không nói về TORAI của tác giả.

## 7. Tổng hợp phần đọc tay

### 7.1 Bảng phủ nhóm

Mỗi dòng là một nhóm; "đọc" là số đơn vị sai đã đọc trên số đơn vị sai của nhóm; "đường đi" là số đường đi khác nhau trong nhóm (mỗi đường đi đọc một đơn vị). Chi tiết từng nhóm ở `ke-hoach-doc-tay.json` → `/nhom`.

| Phương pháp | Số nhóm | Nhóm có đối chứng đúng cùng ô cho ít nhất một đơn vị đọc | Nhóm chỉ có đối chứng khác ô | Nhóm không có đối chứng đúng |
|---|---|---|---|---|
| TraceRCA | 14 | 4 | 10 | 0 |
| MicroRank | 11 | 3 | 5 | 3 (Nezha-OB ở k = 1: M5, M0, M6) |
| BARO | 8 | 6 | 2 | 0 |
| SimpleRCA | 9 | 6 | 3 | 0 |
| CIRCA | 6 | 4 | 0 | 2 (Nezha-OB UNSUPPORTED) |
| TORAI B | 4 | 2 | 0 | 2 (Nezha-OB UNSUPPORTED) |

Bảng này đếm bằng lệnh từ `ke-hoach-doc-tay.json` → `/nhom/*/doc_tay/*/doi_chung_doc` (trường `cung_o`). Tính theo lượt đọc (một đơn vị sai trong một nhóm): 114 lượt, gồm 36 lượt có đối chứng cùng ô, 67 lượt chỉ có đối chứng khác ô, 11 lượt không có đối chứng đúng. Con số về đối chứng trên toàn danh mục (191 yêu cầu có đối chứng, 110 không) ở `doi-chieu-dung-sai.json` → `/cap_doi_chung`.

### 7.2 Những điều chỉ thấy khi đọc từng ca, chưa có trong ba file kết quả

1. **Cờ M5 không đồng nghĩa "sai vì dịch vụ gọi".** Ở nhiều đơn vị mang cờ M5, thực thể đứng đầu và đa số thực thể trên root không nằm phía trên root (mục 1.2 ca thứ ba; 2.2; 3.2 ca thứ nhất; 4.1 điểm 1).
2. **Ca đúng và ca sai cùng ô thường khác nhau ở điều kiện đầu vào, không ở loại lỗi:** có hay không có span của dịch vụ gọi trong cửa sổ (mục 1.2); độ phẳng của cột ở nền (3.1); một cột của dịch vụ khác có đứng yên trong đoạn train không (5.1); cột của dịch vụ gọi có vượt ngưỡng kéo dài không (4.1).
3. **Cùng một quy tắc "span thuộc dịch vụ nào tính cho dịch vụ đó" giúp root khi root là bên gọi và hại root khi root là bên được gọi** (mục 1.4, đối chứng `dev-9b9397a4dc`).
4. **Ba ca CIRCA đúng là đúng nhờ giá trị cực lớn** (mục 5.1), và **ba ca DA hại không dính giá trị cực lớn đều do một nút không liên quan có điểm lớn kéo các nút cha của nó vượt root** (5.3; cách đọc ban đầu "root không có cạnh" đã được sửa sau phép kiểm KT-15).
5. **Bộ chia trace theo bài MicroRank gốc có phản ví dụ** (mục 2.3 điểm 2; 2.4 điểm 5).
6. **Ở return tại điểm vào, lưu lượng dịch vụ phía dưới có đổi trong khi root có điểm thấp hoặc không có phiếu metric** (mục 3.3,4.2). Quan sát hướng phía dưới khác giả thuyết chờ ở phía trên; chưa xác nhận thay đổi do return hay thiếu tín hiệu trong dữ liệu.

### 7.3 Giới hạn của phần đọc tay

- Phiên 12: 100 đơn vị trên 372, mỗi đường đi đọc một đơn vị. Phiên 13 đã đọc nốt 68 đơn vị sai còn lại ở mức phiếu gọn (mục 8); 48 đơn vị không chạy được ghi theo lý do. 156 đơn vị đúng ở hạng 1 không thuộc diện đọc.
- "Đường đi" do tôi định nghĩa; hai đơn vị cùng đường đi có thể khác nhau ở chỗ chữ ký không ghi.
- Với TraceRCA và MicroRank ở Nezha-OB, đối chứng đúng gần như không có; các câu so sánh đúng–sai ở đó yếu.
- Phiếu đọc chỉ in tối đa 4–7 thực thể đầu trên root; phần còn lại xem ở bảng.
- Phần đọc không mở dữ liệu thô; mọi con số là trung gian đã lưu ở phiên 9–11.

## 8. Đọc nốt các đơn vị sai còn lại (phiên 13, 11/10/2026)

Minh duyệt đọc hết (Q-141). Sau phiên 12 còn 116 đơn vị sai hoặc không OK chưa đọc: 68 đơn vị OK xếp sai và 48 đơn vị không chạy được (42 UNSUPPORTED, 6 ERROR). Mục này đọc 68 đơn vị; 48 đơn vị kia ghi theo lý do ở mục 8.7.

- **Phiếu đọc:** `runs/tong-hop-phien-13-001/phieu-gon-chua-doc/<phương pháp>.txt`, sinh bằng `scripts/phieu_gon_v2.py` từ đúng bảng `doi-chieu-dung-sai.json` của phiên 12 (không tính gì mới). Danh sách đơn vị: `danh-sach.json` cùng thư mục.
- **Mức đọc:** phiếu gọn (đầu vào, điểm của root và của các thực thể trên root, tác dụng của từng phép đổi, mức đo được của trace). Mỗi đơn vị được đối chiếu với đơn vị cùng đường đi đã đọc ở phiên 12; điều cần ghi là nó **giống** hay **khác** đơn vị đại diện.
- **Đối chứng:** như đã khóa ở `ke-hoach-doc-tay.json`; không chọn thêm đối chứng mới. Nơi nào kết quả phiên 13 (KT-12, KT-8, bảng nối) nói thêm về chính đơn vị đó thì dẫn tới `ket-qua-phien-13.md`.

### 8.1 BARO — 7 đơn vị

1. **dev-8ecd9880ed (Nezha-OB, checkoutservice|return), hạng 8/10.** Cột tốt nhất root: độ trễ phía gọi P95, z=4,2, IQR/median 34%, lệch/median 143%. adservice z=523,3 (398%, 0,76%); paymentservice z=144 (2%, 0,013%). B-2 hạng 7; 6/7 thực thể trên root không phía trên. Root có thay đổi và có điểm; chưa phân xử phần do lỗi với nền, không thể gọi dữ liệu không có tín hiệu chỉ vì root không hạng 1.
2. **`dev-9b9397a4dc` (Nezha-OB, recommendationservice|cpu_consumed), hạng 2.** Root: độ trễ phía server P90, z = 115,3 với lệch/median 13.931% (gấp 139 lần mức nền) và IQR/median 121%. Trên root: `adservice` (không liên hệ) cột độ trễ phía gọi P99 z = 131,3, lệch/median 100%, IQR/median 0,76%. B-2 làm root **xuống hạng 4**. **Khác** cách đọc ở mục 3.5: đây là đường (ii) "root đổi nhiều nhưng thua cột nền phẳng", nhưng thang độ lệch chuẩn không gỡ được mà còn làm tệ hơn (5 mẫu).
3. **`dev-607751ac0a` (Nezha-OB, checkoutservice|network_delay), hạng 8.** Cột tốt nhất của root là lưu lượng mạng nhận, z = 5,0. Trên root 7 thực thể, đứng đầu `shippingservice` cột độ trễ phía server P99 z = 2.426,2 với lệch/median 59% trên nền IQR/median 0,024%. B-2 xuống hạng 10. Lời gọi tới root chậm ở 9% lời gọi. Chuỗi cột độ trễ của root ở ca này đã in ở KT-12 (`ket-qua-phien-13.md` mục 3): không cột độ trễ nào của root vượt mức nền. **Giống** đơn vị đại diện: root không có tín hiệu metric.
4. **`dev-2bfc97b01e` (Nezha-OB, checkoutservice|network_delay), hạng 2.** Root: độ trễ phía server P99 z = 94,0 (lệch/median 95%, IQR/median 1%). Trên root: `emailservice` (phía dưới root) cột lưu lượng mạng nhận z = 215,1, lệch/median 3.843%, lưu lượng qua nó có đổi. B-2 không đổi. **Điều KT-12 thêm vào:** z = 94 của root là do IQR của 5 mẫu nền gần bằng 0 (0,005); chuỗi sau mốc của cột đó (0,48; 0,49; 0,50; 0,25; 0,97) gần như lặp lại chuỗi nền (0,50; 0,50; 0,97; 0,24; 0,49). Tức root đứng hạng 2 ở ca này không phải vì cột độ trễ của nó phản ứng với sự cố.
5. **dev-3b92690644 (Nezha-OB, checkoutservice|return), hạng 3.** Root độ trễ phía gọi P99, z=40, lệch/median 211%. shippingservice mạng nhận z=216, lệch/median 1.850%; adservice độ trễ phía server P95, z=58,2. B-2 hạng 4. Root có cột đổi cùng lúc phía dưới có cột đổi; chưa quy riêng cho lỗi hay xác nhận hướng lan.
6. **`dev-f81f88234e` (RE2-TT, auth|delay), hạng 11 trên 68.** Root: cột latency z = 4,9 (IQR/median 31%, lệch/median 152%). Trên root 10 thực thể (7 không liên hệ, 3 không có span): `ts-user-service` latency z = 33,6 (lệch/median 57%, IQR/median 2%); `ts-travel2-service` mem z = 14,2 với lệch/median 0,9%. B-2 lên hạng 10. **Khác** đơn vị đại diện `dev-57546fd87b` ở một điểm: ở đây cột latency của root **có đổi** (KT-12: trung vị 0,77 → 1,38; 158/300 mẫu sau mốc vượt mean + 3·std), nhưng nền của cột dao động rộng (IQR 0,24) nên z nhỏ. Vậy câu "root gần như không có tín hiệu metric" ở mục 3.1 điểm 1 chỉ đúng theo thang z; về mức đổi thì cả ba ca auth|delay đều có trung vị cột latency của root tăng 1,8–3,9 lần (`ket-qua-phien-13.md` mục 3).
7. **`dev-16597725c1` (RE2-TT, auth|cpu), hạng 4.** Root: mem z = 47,5 (lệch/median 2%, IQR/median 0,04%). Trên root: `ts-food-service` latency z = 117,4 (lệch/median 315%), `ts-contacts-service` latency z = 100,6 (519%), `ts-ui-dashboard` latency z = 56,2 (188%, bậc tại mốc). B-2 đưa root lên hạng 1, cả 3 cặp mất. **Khác** câu ở mục 3.5: ba cột thắng ở đây là cột độ trễ đổi thật của dịch vụ không liên hệ (đường iii), vậy mà đổi thang chia vẫn gỡ được. Đường (ii) và (iii) không tách sạch bằng "B-2 gỡ được hay không".

**Điều phần đọc nốt thêm cho BARO.** (a) Hai phản ví dụ cho cách chia ở mục 3.5: `dev-9b9397a4dc` (đường ii, B-2 không gỡ) và `dev-16597725c1` (đường iii, B-2 gỡ được). Cách chia ba đường vẫn mô tả được thứ gì thắng root, nhưng không dùng tác dụng của B-2 làm tiêu chí phân loại. (b) Ở auth|delay, khác nhau giữa các ca nằm ở **độ dao động của nền**, không ở việc root có phản ứng hay không. (c) Ở Nezha-OB có thêm một ca (`dev-2bfc97b01e`) mà z lớn của chính root là sản phẩm của IQR tính trên 5 mẫu.

### 8.2 SimpleRCA — 6 đơn vị

1. **`dev-7b7c973198` (Nezha-OB, emailservice|network_delay), hạng 3.** Root: 6 phiếu metric (4/16 cột) + 0 + 0. Trên root: `cartservice` và `currencyservice` (không liên hệ), mỗi bên 9 phiếu; chênh 3 phiếu. Lời gọi tới root chậm ở 100% lời gọi và root đứng đầu ở vị trí `in_u`, nhưng kênh trace cho root 0 phiếu. S-1 giữ hạng tốt nhất 3 nhưng tạo hòa [3,5], nên hạng bi quan là 5. **Giống** đơn vị đại diện (`dev-515c5f2190`): chênh vài phiếu; tín hiệu trên cạnh không được đếm.
2. **`dev-9b9397a4dc` (Nezha-OB, recommendationservice|cpu_consumed), hạng [2, 3].** Root 6 phiếu (2/16 cột); `cartservice` 10 phiếu. S-1 làm root xuống [4, 5]. Giống trên.
3. **`dev-55f99f3e0a` (Nezha-OB, checkoutservice|exception), hạng 2.** Root 10 + 0 + 1 = 11; `frontend` (gọi trực tiếp root) 17 + 0 + 1 = 18, cột nhiều phiếu nhất là độ trễ phía trước P99 (3/5 mẫu). S-1 không đổi. **Giống** `dev-3b92690644`.
4. **`dev-9fd793feb7` (Nezha-OB, shippingservice|cpu_consumed), hạng 2.** Root 16 (9/16 cột) + 1 = 17; `checkoutservice` (gọi trực tiếp root) 19, cột độ trễ phía gọi P95 4/5 mẫu. Lời gọi tới root chậm ở 83% lời gọi. S-1 đưa root lên hạng 1. **Khác** đơn vị đại diện ở tác dụng của S-1 (đại diện: không đổi).
5. **`dev-a505ab3f65` (RE2-TT, train|delay), hạng 2.** Root 1.104 phiếu metric (4/8 cột) + 1; `ts-travel2-service` (phía trên root) 1.128 + 1, cột nhiều phiếu nhất là latency-50 với 289/300 phiếu. Chênh 24 phiếu trên khoảng 1.100. Lời gọi tới root chậm ở 100% lời gọi. S-1 cho hạng [1, 6]. **Giống** `dev-7f1b6b071d`: cột độ trễ của dịch vụ gọi vượt ngưỡng gần suốt cửa sổ.
6. **`dev-fbc45b0c67` (RE2-TT, train|delay), hạng 3.** Root 838 + 1; `ts-travel2-service` 1.012 + 1 (latency-90: 287 phiếu), `ts-admin-travel-service` 896 + 1 (latency-90: 277 phiếu, bậc tại mốc); cả hai nằm phía trên root. S-1 làm root xuống [5, 8]. Giống trên.

**Điều phần đọc nốt thêm cho SimpleRCA.** Sáu đơn vị đọc nốt đều thuộc các đường đã nêu ở mục 4.4; không thấy đường mới. Ở hai ca train|delay, **mọi** thực thể trên root đều nằm phía trên root và thắng bằng cột độ trễ; cùng với `dev-7f1b6b071d` đây là ba ca RE2-TT mà dạng "cột độ trễ của dịch vụ gọi vượt ngưỡng lâu ngang root" hiện rõ nhất. Tác dụng của S-1 trong cùng một đường đi không đồng nhất (tăng, không đổi, giảm), nên S-1 chỉ đọc theo ca.

### 8.3 TraceRCA — 10 đơn vị OK (3 đơn vị ERROR xem mục 8.7)

1. **`dev-515c5f2190` (Nezha-OB, recommendationservice|cpu_consumed), hạng 2.** Root: a = 309, n = 325 (95%), điểm 0,3812. Trên root: `frontend`, span phía gọi của lời gọi tới root, a = 311, n = 325 (96%), điểm 0,3837; 94% span mang cờ của nó là span chờ root. Chênh đúng 2 span. Không phép đổi nào đổi hạng (T-D, a/n, a/n từ 20 span, a đều cho hạng 2); bước của bài gốc cho hạng 3, `frontend` đứng đầu. Root đứng đầu ở cả năm vị trí của bảng A. **Giống** đơn vị đại diện (`dev-14701a3bbb`) về cơ chế, và là dạng sát nhất: hai đầu của cùng một loại lời gọi gần như cùng a, cùng n; đầu phía gọi nhỉnh hơn 2 span.
2. **`dev-7d3c2fe6d1` (Nezha-OB, shippingservice|cpu_contention), hạng 2.** Root 52/215 (24%); `frontend` 145/182 (80%), 100% là span chờ root. T-D không đổi; a/n xuống hạng 3; bước của bài gốc hạng 3. Cùng ô và **giống hệt** hình dạng của `dev-14701a3bbb` (41/171 so với 122/151).
3. **`dev-55f99f3e0a` (Nezha-OB, checkoutservice|exception), hạng 3.** Root 19/208 (9%). Trên root: `frontend` 70/1.142 (6%), `currencyservice` 126/3.714 (3%); tỷ lệ span chờ root bằng 0. a/n đưa root lên hạng 1. **Giống** `dev-3b92690644`: thao tác đông span thắng nhờ số tuyệt đối.
4. **`dev-b0f8b2e3ac` (Nezha-OB, checkoutservice|exception), hạng 5.** Root 20/212 (9%). Bốn thực thể trên root có 4–6% span mang cờ trên 726–3.552 span. a/n lên hạng 1; T-D lên hạng 3. Giống trên.
5. **dev-5ada15752d (Nezha-OB, frontend|return), hạng 3.** Root 35/2.201 (2%); currencyservice 94/2.447 (4%), checkoutservice 8/46 (17%). T-D và a/n làm root xuống hạng 6. Như mục 1.5, có cờ nhưng root không hạng 1; đáp ứng do lỗi chưa phân xử.
6. **`dev-607751ac0a` (Nezha-OB, checkoutservice|network_delay), hạng 6.** Root 4/33 (12%); năm thực thể trên root có 3–6% trên 208–2.188 span. a/n lên hạng 1. Lời gọi tới root chậm ở 9% lời gọi. **Giống** `dev-2bfc97b01e`.
7. **`dev-63c30faf34` (Nezha-OB, recommendationservice|network_delay), hạng 8.** Root 6/574 (1%); `frontend` 555/574 (97%), 99% là span chờ root; sáu thực thể khác 1–17%. a/n giữ hạng 8; bước của bài gốc đưa root lên hạng 2, `frontend` đứng đầu. **Giống** `dev-5467884de4`.
8. **`dev-6c9afc9822` (Nezha-OB, emailservice|network_delay), hạng 9.** Root 1/27 (4%). Trên root có **hai** thực thể cùng a = 26, n = 27 (96%), cùng điểm 0,0908, cùng 88% span chờ root: `checkoutservice` (gọi trực tiếp root) và `frontend` (gọi `checkoutservice`). Sáu thực thể không liên hệ 1–4% cũng đứng trên root. Bước của bài gốc: root không có điểm dương, hạng 8–10. **Điều mới so với đơn vị đại diện:** thời gian chờ root hiện ở span phía gọi của dịch vụ gọi trực tiếp **và** của dịch vụ gọi dịch vụ đó, với cùng số span. Tức nếu chỉ "gỡ điểm của dịch vụ gọi" thì còn một tầng nữa; muốn gắn tín hiệu về đúng dịch vụ được gọi phải đi theo cạnh trực tiếp tới tận đầu dưới của chuỗi.
9. **`dev-95e164235f` (Nezha-OB, paymentservice|cpu_contention), hạng 6.** Root 7/36 (19%). Trên root: `checkoutservice` (gọi trực tiếp) 10/36 (28%), 100% span chờ root; `frontend` 132/3.710 (4%); ba dịch vụ không liên hệ 2–6% trên 587–3.786 span. a/n đưa root lên hạng 2, chỉ còn `checkoutservice` đứng trên. Lời gọi tới root chậm ở 28% lời gọi. **Đọc:** ca dính cả hai đường: khối lượng (bốn thực thể, mất khi xếp theo tỷ lệ) và span phía gọi (một thực thể, không phép đổi nào trên nút gỡ được).
10. **`dev-db293894ab` (RE2-TT, travel|disk), hạng 2.** Root 247/804 (31%), điểm 0,0947. Trên root: `ts-seat-service` (hai chiều với root) 545/3.921 (14%), điểm 0,1308; 86% span mang cờ là span chờ root. **T-D đưa root lên hạng 1**; a/n cũng lên hạng 1. **Khác** đơn vị đại diện `dev-12a1a88069`, nơi T-D không đổi hạng dù 98% span là span chờ root. Hai ca cùng loại lỗi (disk), cùng dịch vụ đứng trên (`ts-seat-service`), khác nhau ở tác dụng của T-D. Đã mở bảng lời gọi chậm theo cạnh của hai ca (EC2, `runs/call-slow-001/cases/RE2-TT-<mã>.json` → `/edges`, cạnh `ts-seat-service→<root>`): ở ca này 470 lời gọi chậm, 350 nằm trong span của root (74%); ở `dev-12a1a88069` 128 lời gọi chậm, 106 nằm trong span của root (83%). Vậy cách hiểu nêu ở mục 1.2 ("phần chậm nằm ngoài span của root nên T-D không gỡ được") **không được hỗ trợ**: ca mà T-D không gỡ được lại có tỷ lệ nằm trong span của root cao hơn. Lý do hai ca khác nhau **chưa phân xử**; bằng chứng cần: điểm theo thao tác của `ts-seat-service` và của root dưới T-D ở hai ca (có trong lượt `tracerca-core-td-001`, chưa lập bảng so).

**Phần đọc nốt thêm cho TraceRCA.** Trong 10 đơn vị, quan sát span phía gọi ở 1,2,7,8,9,10; khối lượng ở 3,4,6,9; root ít cờ/không hạng 1 ở 5, chưa xác nhận thiếu đáp ứng do lỗi. Trong 9 đơn vị Nezha, frontend đứng đầu 6 (1,2,3,7,8,9), currencyservice ở 4,5, recommendationservice ở 6. Hai điều mới: chờ qua hai tầng với cùng số span (8), T-D khác nhau ở hai ca RE2-TT cùng dạng (10).

### 8.4 MicroRank — 28 đơn vị OK (3 đơn vị ERROR xem mục 8.7)

Ngoài phiếu gọn, mỗi đơn vị được đọc kèm hai kết quả mới: hạng root dưới nhánh ghép của KT-3 (`runs/microrank-kt3-001/collect-001/summary.json` → `/cases`; viết "ghép: luật của bài / luật của code") và bảng nối theo cây span cho nhánh ghép (`runs/microrank-merged-link-001/summary.json`; mô tả ở `ket-qua-phien-13.md` mục 5). "Gắn với root" là cách đọc theo mốc đã khai ở thiết kế 013 mục 4.

**A. Nezha-OB, không phép đổi nào cứu (5 đơn vị; đại diện `dev-14701a3bbb`).**

1. `dev-3b92690644` (checkoutservice|return), hạng 8: A = 296 trên 935 trace (32%), **286 trace A không có root**; root tự mang cờ ở 6. Bảy thực thể trên root, tỷ lệ gắn root từ 0,00 tới 0,02. Mọi phép đổi cho hạng 8–9. Ghép: 7 / 7, `frontend` đứng đầu; thao tác cao nhất của `frontend` là lời gọi tới `productcatalogservice` hoặc `currencyservice`, và không trace nào trong số trace tạo ra số đếm của nó có root.
2. `dev-8ecd9880ed` (checkoutservice|return), hạng 9: 171/180 trace A không có root. Mọi phép đổi cho hạng 8–9. Ghép: 7 / 7, `frontend` đứng đầu, không gắn.
3. `dev-70629373f9` (paymentservice|cpu_contention), hạng [8, 9]: 262/300 trace A không có root; root tự mang cờ ở 2. Ghép: [7, 9] / [8, 10].
4. `dev-95e164235f` (paymentservice|cpu_contention), hạng [8, 9]: 236/264 trace A không có root; root tự mang cờ ở 7. Ghép: [6, 8] / [5, 8].
5. `dev-27252dca60` (productcatalogservice|exception), hạng 3: A = 94 (9%), mọi trace A đều có root, root tự mang cờ ở 3. Bỏ trọng số và đếm riêng làm root xuống hạng 4 và 5; **cờ theo phần chưa phủ (M-D) đưa root lên hạng 1**. Ghép: [9, 10] / 3.

**Khác** đơn vị đại diện: ở `dev-14701a3bbb` lý do đọc được là tín hiệu nằm ở span phía gọi. Ở bốn đơn vị 1–4, root (`checkoutservice`, `paymentservice`) nằm trên luồng đặt hàng mà ít yêu cầu đi qua, nên vắng ở 87–97% trace A; đây là dạng của `dev-2bfc97b01e` ("root gần như vắng trong nhóm A"), không phải dạng span phía gọi. Đơn vị 5 là ca duy nhất trong 28 đơn vị mà M-D đưa root lên hạng 1.

**B. Nezha-OB, bộ chia theo bài gốc cứu (2 đơn vị; đại diện `dev-3e27669440`).**

6. `dev-515c5f2190` (recommendationservice|cpu_consumed), hạng 5: A = 322 (75%); root tự mang cờ ở 299. Bốn thực thể trên root đều có 94% trace A gắn với root (đi cùng trace). Đếm riêng lên hạng 2; chia theo bài gốc hạng 1. Ghép: 1 / 1. **Giống** đại diện.
7. dev-5467884de4 (recommendationservice|network_delay), hạng 5: A=484 (77%); root tự mang cờ ở 7 trace. Chia theo bài đưa root hạng 1; ghép làm root hạng 4/5, frontend đứng đầu. 97–98% span mang cờ thao tác phía gọi có con trực tiếp root và bao lời gọi chậm; root mang cờ 6–7/67–199 trace ấy. Đếm riêng lấy điểm từ ít cờ root so với phía gọi, không phải root hoàn toàn không mang cờ. Đây là cơ chế tính toán gắn span cho dịch vụ sở hữu nó của ca này.

**C. Nezha-OB, root là điểm vào (1 đơn vị; đại diện `dev-1ac905bc95`).**

8. `dev-5ada15752d` (frontend|return), hạng 4: chia theo luật của bài hạng 1, luật của code hạng 6. Ghép: 1 / 1, nhưng nhóm bất thường mới chỉ có 4 và 1 trace. **Giống** đại diện: kết quả không ổn định giữa hai luật, dựa trên vài trace.

**D. Nezha-OB, bộ chia theo bài gốc tăng nhưng chưa tới hạng 1 (6 đơn vị; đại diện `dev-2bfc97b01e`, `dev-7b7c973198`).**

9. `dev-396c8dbf7d` (emailservice|cpu_consumed), hạng [8, 9]: 286/324 trace A không có root; root tự mang cờ ở 38. Đếm riêng lên hạng 5; chia theo luật của bài [1, 4] (hòa bốn dịch vụ). Ghép: **1 / 1**.
10. `dev-607751ac0a` (checkoutservice|network_delay), hạng 8: root tự mang cờ ở 18; 210/233 trace A không có root. Ghép: [6, 10] / 2.
11. `dev-63c30faf34` (recommendationservice|network_delay), hạng 5: A = 594 (77%), root tự mang cờ ở 6. Chia: 2 / 1. Ghép: 5 / 5, `frontend` đứng đầu bằng span phía gọi của lời gọi tới root (98–99% có span con trực tiếp thuộc root). Cùng dạng với đơn vị 7.
12. `dev-6c9afc9822` (emailservice|network_delay), hạng [8, 9]: root tự mang cờ ở 1 trace. Chia: [1, 4] / [1, 4]. Ghép: [3, 5] / [5, 6], `checkoutservice` đứng đầu bằng span phía gọi của lời gọi tới root (90–92%). Cùng dạng.
13. `dev-7d3c2fe6d1` (shippingservice|cpu_contention), hạng 6: đếm riêng lên 4; chia [5, 7] / 6. Ghép: [4, 7] / 3; thực thể đứng đầu dựa trên 6 và 1 span.
14. `dev-b0f8b2e3ac` (checkoutservice|exception), hạng 8: chia 5 / 1. Ghép: 3 / 1.

**E. RE2-TT, đếm riêng cứu, bộ chia theo bài gốc không (3 đơn vị; đại diện `dev-3ae0a6c15a`).**

15. `dev-98bc73c499` (train|cpu), hạng 3: trên root là `ts-station-service` (gắn root 0,83) và `ts-route-service` (0,94). Bỏ trọng số và đếm riêng đưa root lên hạng 1; chia theo bài gốc xuống 5 / 4. Ghép: 4 / 4, `ts-admin-travel-service` đứng đầu; thao tác cao nhất của nó nằm phía trên root trong cây span ở 100% span mang cờ và bao lời gọi chậm tới root ở 99%. **Giống hệt** đại diện (cùng ô, cùng thực thể đứng đầu).
16. `dev-ba831dbeb8` (train|cpu), hạng 3: đếm riêng hạng 1; chia 3 / 1. Ghép: 2 / 1; dưới luật của bài `ts-travel-service` đứng đầu bằng span phía gọi của lời gọi tới root (89%).
17. `dev-bcbd4f46ae` (route|socket), hạng 2: bỏ trọng số và đếm riêng đưa root lên hạng 1; **chia theo bài gốc xuống 7 / 6** (chỉ 16% trace bất thường mới có root). Ghép: 5 / 5, `ts-auth-service` đứng đầu bằng thao tác đăng nhập; không trace nào trong 12 trace tạo ra số đếm của nó có root.

**F. RE2-TT, bộ chia theo bài gốc cứu, có thực thể phía trên (1 đơn vị; đại diện `dev-7f1b6b071d`).**

18. `dev-a915aa2424` (travel|loss), hạng 12: 373/607 trace A không có root; 11 thực thể trên root (9 phía dưới, 2 hai chiều). Đếm riêng lên hạng 4; chia hạng 1. Ghép: 1 / 1. **Giống** đại diện.

**G. RE2-TT, cả bộ chia theo bài gốc lẫn đếm riêng đều cứu (6 đơn vị; đại diện `dev-14372e1209`, `dev-16597725c1`).**

19–20. `dev-3defe3d34b` và `dev-59f696a169` (auth|cpu), hạng 10 và 9: 483/695 và 480/719 trace A không có root; 9 và 8 thực thể trên root đều không liên hệ, tỷ lệ gắn root 0,00. Bỏ trọng số làm root xuống hạng 11; đếm riêng và chia theo bài gốc đưa lên hạng 1 (97–98% trace bất thường mới có root). Ghép: 1 / 1. **Giống** `dev-16597725c1`.
21. `dev-4f8a844308` (route|mem), hạng 2: `ts-station-service` trên root (gắn root 0,90). Ghép: 1 / 1. **Giống** `dev-14372e1209`.
22–23. `dev-de89e2f9e9` và `dev-f9a8e05ed7` (travel|disk), hạng 3: A chỉ 18% và 17% số trace; hai thực thể phía dưới root đứng trên. Ghép: 1 / 1.
24. `dev-fbc45b0c67` (train|delay), hạng 3: như đơn vị 15 ở bản gốc; chia 1 / 2; ghép 1 / 1.

**H. RE2-TT, bộ chia theo bài gốc tăng nhưng chưa tới hạng 1 (4 đơn vị; đại diện `dev-12a1a88069`, `dev-1e6d61b5ec`).**

25. `dev-db293894ab` (travel|disk), hạng 11: 378/608 trace A không có root. Đếm riêng 4; chia 2 / 1. Ghép: 1 / 1.
26. `dev-f36d0647d5` (order|loss), hạng 11: 391/587 trace A không có root; đếm riêng 7; chia 9 / 9. Ghép: 3 / 3, `ts-seat-service` (gọi trực tiếp root) đứng đầu; 51–55% span mang cờ của thao tác đó bao lời gọi chậm tới root, so với 3% ở span không mang cờ của cùng thao tác.
27–28. `dev-20acb4402d` và `dev-260d332c8d` (order|loss), hạng 8 và 10: A chỉ 13% và 15%; 169/191 và 199/211 trace A không có root; root tự mang cờ ở 20 và 9. Chia: 2 / 2, `ts-auth-service` đứng đầu. Ghép: 2 / 2 và 3 / 2, vẫn `ts-auth-service`, bằng thao tác đăng nhập; không trace nào trong 28 và 41 trace tạo ra số đếm của nó có root. KT-2 cho biết thêm: ở hai ca này tỷ lệ span mang cờ của thao tác đăng nhập là 0,9–1,9% dưới mốc giả và 9–10% sau mốc thật (`ket-qua-phien-13.md` mục 2). Tức `ts-auth-service` chậm lên thật sau khi tiêm lỗi mất gói vào `ts-order-service`, dù hai dịch vụ không nối nhau trên đồ thị gọi.

**Điều phần đọc nốt thêm cho MicroRank.**

- Ba dạng quan sát sau ghép là span phía gọi được tính cho dịch vụ gọi; các trace tạo số đếm của thao tác đứng đầu vắng root; hoặc ít span. Chưa bao phủ mọi ca: dev-14701a3bbb chưa rõ dưới cả hai luật; dev-607751ac0a luật code không gắn theo cây con nhưng root có trong 2/6 trace xét. Nhãn root đã biết; chưa rõ cơ chế xếp sai và cách sửa có căn cứ. Nguồn cụ thể: KQ13 mục 5 và runs/microrank-merged-link-001/summary.json → /cases.
- Câu chưa giải thích ở mục 2.2 và 2.3 ("vì sao `ts-auth-service` lên đầu sau khi thay bộ chia") nay có một phần trả lời: nó chậm lên thật sau mốc (KT-2), và trace của nó không đi qua root. Vì sao nó chậm lên thì **không phân xử được bằng dữ liệu hiện có** (`kiem-tiep.md` mục KT-6).
- Dạng (i) là dạng mà cạnh gọi có thể chỉnh. Dạng (ii) với `ts-auth-service` thì cạnh gọi không chỉnh được: hai dịch vụ không có cạnh.
- 28 đơn vị đọc nốt không chứng nhận ba dạng đã giải thích mọi ca. Bảng nối giữ nguyên ca chưa rõ và ca không gắn nhưng root hiện diện; bốn đơn vị nhóm A được mô tả theo tập trace tạo số đếm của thao tác đứng đầu. M-D có một ca đưa root hạng 1 (đơn vị 5), giữ nguyên phản ví dụ ấy.

### 8.5 CIRCA — 8 đơn vị OK (21 đơn vị UNSUPPORTED xem mục 8.7)

1. **Sáu đơn vị cùng đường đi với `dev-3ae0a6c15a`:** `dev-4e68956051` (train|delay), `dev-4f8a844308` (route|mem), `dev-98bc73c499` (train|cpu), `dev-a505ab3f65` (train|delay), `dev-b8bd0abf60` (route|socket), `dev-ba831dbeb8` (train|cpu). Cả sáu có **cùng một nút cực lớn** `ts-admin-travel-service_latency` (7 nút cha; độ lệch chuẩn của y ở đoạn train từ 7,5e-17 tới 1,3e-16; điểm RHT từ 1,1e16 tới 7e17; cùng nút đó khi không có cha có điểm từ 0,24 tới 9,27). Hạng root sau DA là 4 ở 6/6; trước DA là 2 (bốn đơn vị) hoặc 3 (hai đơn vị train|delay). Ba thực thể trên root sau DA giống nhau ở 6/6: `ts-travel-service`, `ts-travel2-service` (gọi trực tiếp root) và `ts-admin-travel-service`, cả ba mang khóa cực lớn. Bỏ mọi cạnh: root hạng 1 ở 6/6; chỉ bỏ một loại cạnh: hạng 2–4. **Giống hệt** đơn vị đại diện; không có phản ví dụ trong đường đi này. Ghi thêm: `dev-4e68956051` là ca mà MicroRank và TraceRCA dừng vì thao tác thiếu nền, còn CIRCA chạy được vì không dùng thời lượng span.
2. **`dev-57546fd87b` (auth|delay), hạng 46 trên 68.** Không có nút cực lớn. Hạng root: 40 trước DA, 46 sau DA; bỏ mọi cạnh: 34. Có 45 thực thể trên root (23 không liên hệ, 22 không có span); 38/45 đã đứng trên root trước DA. Cột tốt nhất của root là mem. **Khác** đơn vị đại diện `dev-16597725c1` (2 → 15) về mức độ: ở đây DA chỉ lấy thêm 6 hạng; root đã ở rất xa từ trước vì cột của nó có z nhỏ (KT-12: cột latency của root có tăng, nhưng nền dao động rộng). Lý do chính của ca này là kênh metric, không phải bước DA.
3. **`dev-f81f88234e` (auth|delay), hạng 22.** Không có nút cực lớn. Hạng root: 10 trước DA, 22 sau DA; bỏ mọi cạnh: 22; chỉ giữ cạnh cùng dịch vụ: 9. Có 21 thực thể trên root, 9/21 đã đứng trên root trước DA. **Đọc:** ở ca này hồi quy theo nút cha **giúp** root (không cạnh: hạng 22; có cạnh, trước DA: hạng 10), rồi bước DA lấy lại đúng phần đó (KT-15: 11/12 thực thể mới vượt root nhận cùng một giá trị 61,71 từ `ts-preserve-service_latency`). Một ca cho thấy hai bước dùng đồ thị của CIRCA tác động ngược chiều nhau.

**Điều phần đọc nốt thêm cho CIRCA.** Đường "giá trị cực lớn" đồng nhất ở cả 7 đơn vị sai của nó (một nút, ba thực thể trên root, bỏ cạnh thì hạng 1). Ba ca root `ts-auth-service` không đồng nhất: DA quyết định ở `dev-16597725c1` (2 → 15) và `dev-f81f88234e` (10 → 22), còn ở `dev-57546fd87b` root đã ở hạng 40 trước DA.

### 8.6 TORAI B — 9 đơn vị OK (21 đơn vị UNSUPPORTED xem mục 8.7)

Vectơ bốn nguồn và severity của một ca **giống nhau ở cả ba seed** (bước severity không dùng số ngẫu nhiên); seed chỉ có thể đổi thứ tự trong cụm nhiều dịch vụ. Vì vậy các đơn vị khác seed của một ca đã đọc được đối chiếu ở đúng chỗ seed có thể tác động.

1. **`dev-16597725c1` seed 1 và seed 2 (auth|cpu), hạng 3.** Vectơ, severity, cụm 25 dịch vụ và hai thực thể trên root (`ts-order-other-service`, `ts-seat-service`; chênh log +0,175 ở cả hai) trùng seed 0 đã đọc. Bỏ cột log nền không đổi và bỏ nguồn log đều đưa root lên hạng 1. **Giống** seed 0.
2. **`dev-f36d0647d5` seed 1 và seed 2 (order|loss), hạng 3.** Trùng seed 0: trên root là `ts-travel2-service` và `ts-seat-service` (phía trên root); cả hai phép bỏ log giữ hạng 3. **Giống** seed 0.
3. **`dev-a5cabe5fa7` seed 0 và seed 2 (travel|loss), hạng 2.** Vectơ trùng seed 1 đã đọc: root có metric 0,018; log 0,015; độ trễ trace 0,246; `ts-order-other-service` đứng trên (metric +0,124; log +0,167). Khác nhau giữa seed nằm ở phép bỏ nguồn log: hạng 1 ở seed 0, hạng 2 ở seed 2 (và seed 1). Đây là ca duy nhất trong các đơn vị TORAI sai mà kết quả phép đổi phụ thuộc seed.
4. **`dev-59f696a169` seed 0, 1, 2 (auth|cpu), hạng 3** (ca chưa đọc ở phiên 12). Root: metric 0,109; log 0,019; độ trễ trace 0,086; severity 0,054; cụm 4 dịch vụ, xếp theo nhánh dự phòng. Trên root: `ts-seat-service` severity 0,077 (metric −0,089; log +0,160) và `ts-order-other-service` 0,072 (metric −0,093; log +0,167); cả hai không liên hệ với root. Bỏ nguồn log: root hạng 1 ở cả ba seed. **Bỏ cột log nền không đổi làm root xuống hạng 6.** **Khác** `dev-16597725c1` cùng ô, nơi phép này đưa root lên hạng 1. Dưới phép này có 5 thực thể trên root: hai thực thể cũ và thêm `ts-travel2-service`, `ts-travel-service`, `ts-order-service` (`runs/torai-log-contrast-001/summary.json` → `/cases`, ca này, nhánh `tl2`); số khối xếp hạng đổi từ 5 xuống 3. Tức bỏ 107/392 cột log làm đổi cả cách chia khối, không chỉ bớt điểm log của hai thực thể cũ. Vì sao ba dịch vụ đó nổi lên: **chưa phân xử** (cần bảng severity theo nguồn của nhánh `tl2` cho ca này; lượt đã chạy không lưu bảng đó).

**Điều phần đọc nốt thêm cho TORAI B.** Ở 3/4 ca sai, hai dịch vụ `ts-order-other-service` và `ts-seat-service` là thực thể đứng trên root nhờ nguồn log (chênh log từ +0,160 tới +0,175), dù không liên hệ với root ở hai ca auth|cpu. Phép "bỏ cột log nền không đổi" không ổn định giữa hai ca cùng ô (hạng 1 và hạng 6), nên câu "bỏ cột log nền không đổi là đủ" không đứng được; phép "bỏ nguồn log" ổn định hơn (hạng 1 ở 2 ca × 3 seed và ở 1 seed của ca thứ ba).

### 8.7 Bốn mươi tám đơn vị không chạy được, ghi theo lý do

| Số đơn vị | Phương pháp, dataset | Lý do (giống nhau ở mọi đơn vị của dòng) | Đơn vị đã đọc đại diện | Kết quả thêm ở phiên 13 |
|---|---|---|---|---|
| 21 | CIRCA, Nezha-OB (UNSUPPORTED) | Metric chỉ có 1–2 phép đo thật trong đoạn train; bộ nạp nội suy đuôi đoạn train về điểm sau mốc (Q-85) | `dev-14701a3bbb`, mục 5.4 | Không có |
| 21 | TORAI B, Nezha-OB (UNSUPPORTED) | Trace không có mã trạng thái để dựng nguồn lỗi; nhịp metric khoảng 60 giây không khớp bước 15 hàng (Q-85) | `dev-14701a3bbb`, mục 6.3 | Không có |
| 3 | TraceRCA, RE2-TT (ERROR): `dev-16870e660c`, `dev-4e68956051`, `dev-a5cabe5fa7` | Thao tác `ts-order-other-service_getMore ts.orders` có ở đoạn sau mốc, không có ở đoạn nền | `dev-03d4910932`, mục 1.1 | KT-8: bỏ span của thao tác đó thì root hạng 1 ở cả ba ca này; ở `dev-03d4910932` root hạng 2 (`ket-qua-phien-13.md` mục 4) |
| 3 | MicroRank, RE2-TT (ERROR): cùng ba ca | Cùng thao tác thiếu nền | `dev-03d4910932`, mục 2.1 | KT-8 (phiên 12): root hạng 2, 3, 12; ở `dev-03d4910932` hạng 2 (`ket-qua-phien-12.md` mục 2) |

Phiếu của 48 đơn vị này có trong cùng thư mục phiếu; tôi đã soát dòng lý do của từng phiếu: 42 phiếu UNSUPPORTED cùng một lý do theo phương pháp, 6 phiếu ERROR cùng một thông báo lỗi theo phương pháp. Không đơn vị nào trong 48 có lý do khác.


### 8.8 Tổng hợp phần đọc nốt

- **Không có đường thất bại mới** ở phương pháp nào so với mục 1–6. Điều này không chứng minh danh sách đường thất bại là đủ: phần đọc nốt dùng phiếu gọn, chỉ in 4–6 thực thể đầu trên root.
- **Các điều chỉnh với phần đọc của phiên 12:** (1) BARO: tác dụng của B-2 không dùng được làm tiêu chí tách đường (ii) và (iii) (mục 8.1). (2) auth, delay: cột của root có đổi ở cả ba ca; khác nhau ở nền (8.1 điểm 6). (3) TraceRCA: chờ hiện ở hai tầng dịch vụ gọi với cùng số span (8.3 điểm 8); cách hiểu "phần chậm ngoài span của root" không được hỗ trợ (8.3 điểm 10). (4) MicroRank: bốn đơn vị Nezha-OB thuộc dạng "root vắng trong nhóm trace bất thường"; `ts-auth-service` lên đầu vì chậm lên thật và trace của nó không qua root (8.4). (5) CIRCA: ba ca root `ts-auth-service` không đồng nhất (8.5). (6) TORAI B: phép bỏ cột log nền không đổi cho hạng 1 ở một ca, hạng 6 ở ca cùng ô (8.6).
- **Giới hạn riêng của mục 8:** đọc ở mức phiếu gọn; không chọn thêm đối chứng; đơn vị được so với đơn vị đại diện cùng đường đi, mà đường đi là chữ ký do tôi đặt.
