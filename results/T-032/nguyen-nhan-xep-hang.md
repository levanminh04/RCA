# T-032 — Vì sao các phương pháp RCA xếp sai dịch vụ gốc: bản đồ hạn chế trên tập dev

Người làm lịch sử: Claude. Bản tổng hợp phiên 12–13 ngày 11/10/2026; Codex sửa sau REVIEW theo lời Minh duyệt ngày 11/10; hoàn thiện ngày 12/10/2026. Trạng thái: chờ phiên Codex mới kiểm lại. Bản trước phiên 12–13 ở các thư mục tong-hop-phien-12-001/ban-truoc/ và tong-hop-phien-13-001/ban-truoc/; bản trước lượt sửa này ở runs/sua-review-001/ban-truoc/. Không đổi kết quả đóng băng.

Task này phục vụ câu hỏi nghiên cứu RQ2 và gói P4 của kế hoạch nghiên cứu: các phương pháp RCA đã có thất bại ở ca nào và **vì bước tính nào**. Nó ứng với yêu cầu của cô "chỉ ra vấn đề còn tồn đọng, hạn chế của các phương pháp đã có" trước khi tiếp cận phương pháp đồ thị. Task xong không có nghĩa RQ2 hay cổng G2 đã đóng.

## 0. Tóm tắt

Sáu phương pháp đã chạy trên 52 ca dev (30 ca Train Ticket của RCAEval, viết RE2-TT; 22 ca Online Boutique của Nezha, viết Nezha-OB). Với mỗi phương pháp, chúng tôi phát lại đúng bản đã chấm, lấy giá trị trung gian, rồi **đổi đúng một bước tính** để xem bước nào làm dịch vụ gốc (root) mất hạng. Sáu điều chính:

1. **Chỗ hỏng lớn nhất tìm được ở mỗi phương pháp là một bước khác nhau; không có một nguyên nhân chung.** MicroRank: bước chia trace thành "bất thường" và "bình thường". TraceRCA: bước gắn cờ theo thời lượng cả span và công thức điểm. BARO: thang chuẩn hóa. SimpleRCA: cách đếm phiếu. CIRCA: một lỗi số học lan qua đồ thị. TORAI: nguồn log. Ở phương pháp nào cũng còn một phần ca sai chưa bước nào giải thích (mục 7).
2. **Ba trong các chỗ hỏng lớn nhất thuộc bản cài trong thư viện hoặc đầu vào do chúng tôi dựng, không thuộc bài báo gốc:** bước chia trace của MicroRank, cả hai hạn chế của TraceRCA, và nguồn log của TORAI. Phải nói rõ điều này trước khi gọi đó là "hạn chế của phương pháp".
3. **Dịch vụ gọi bị chấm cao vì phải chờ root có bằng chứng ở một phần ca, tùy phương pháp.** Với TraceRCA, chuỗi tính toán được xác nhận ở 4/4 và 9/15 cặp xét được. Với MicroRank, tiêu chí liên kết hiện tại không hỗ trợ cách giải thích này ở đa số cặp (0/10 và 4/16); phép đổi thời lượng chưa đủ bác bỏ đường cờ → nhóm trace → điểm. Với BARO ở RE2-TT, chỉ 5/103 cặp vừa trên chuỗi gọi vừa có cột đổi tại mốc. Chờ cũng có ở ca đúng, nên riêng hiện tượng này không phân biệt ca sai.
4. **Thông tin để định vị root có trong trace nhưng nằm ở chỗ các phương pháp không nhìn:** ở phần của span không do span con phủ (tách được root ở 26/26 ca RE2-TT có bảng span), và ở span phía gọi của lời gọi tới root (với lỗi trễ mạng ở Nezha-OB: 5/6 ca). Đây là căn cứ để **đề xuất ứng viên** dùng cạnh gọi; chưa phải bằng chứng đồ thị giúp.
5. **Có những ca chưa định vị được root bằng cách chấm hiện tại.** Ở 3/4 ca return của Nezha-OB, root không đứng hạng 1 dưới các cách chấm trong bảng kiểm; điều này chưa chứng minh dữ liệu không có dấu hiệu do lỗi. Ở 8/52 ca không có cạnh gọi đi vào root, nên cách dựa riêng vào cạnh đi vào không áp dụng. Một số dịch vụ không liên hệ có metric đổi tại mốc mà dữ liệu chưa cho biết vì sao.
6. **Việc "dịch vụ gọi chờ root" chỉ đo được chắc ở 16 ca Nezha-OB;** ở 21 ca RE2-TT chỉ đo được một phần vì dataset không công bố công cụ ghi span; 15 ca không đo được.
7. **Bổ sung ở phiên 13, từ phép thử mốc giả (không có lỗi trong đoạn xét):** luật chia trace của bản thư viện xếp 37% trace là bất thường ngay cả khi không có sự cố; còn sự cố thì làm tăng tỷ lệ span mang cờ **có chọn lọc ở thao tác phía trên root** (0,8% lên 6,2%) trong khi thao tác không liên hệ gần như không đổi (1,1% lên 1,2%). Điều thứ nhất củng cố điểm 2; điều thứ hai là bằng chứng mô tả, có đối chứng, rằng dịch vụ gọi dài ra theo root (KQ13 mục 1, 2).

Mọi con số là trên 52 ca dev. Nhiều phép đổi được nghĩ ra sau khi đã xem kết quả dev, nên chúng là bằng chứng cho ứng viên, không phải số đo trên dữ liệu chưa nhìn. Chưa ca test nào được mở.

## 1. Phạm vi và cách đọc

**Sáu phương pháp và bản đã dùng.** BARO (thư viện RCAEval); SimpleRCA (bản M4 theo quy ước của task T-017); MicroRank (biến thể trong RCAEval, sửa đầu vào); TraceRCA (bản trong RCAEval, có lọc giá trị không hữu hạn); CIRCA (hồi quy OLS, đồ thị kiến trúc, có bước DA); TORAI với bảng đầu vào do chúng tôi dựng (gọi là nguồn B). CIRCA và TORAI không chạy được trên Nezha-OB.

**Đơn vị đếm.** Một đơn vị là một ca × một phương pháp × một seed. Danh mục đã khóa có 372 đơn vị, gồm 192 đơn vị sai hoặc không chạy được, chia thành 52 nhóm theo dataset, phương pháp, k (hạng 1 hoặc 5 hạng đầu) và cờ mô tả của task T-028. "Cặp" là (một thực thể được xếp trên root, root). Hạng tính bi quan khi hòa.

**Từ dùng.** *Root*: dịch vụ gốc của sự cố theo nhãn. *Trên root*: được phương pháp xếp hạng tốt hơn root. *Phía trên root*: dịch vụ gọi root trực tiếp hoặc qua dịch vụ khác; *phía dưới*: dịch vụ được root gọi. *Span*: một bản ghi thời gian của một thao tác trong một yêu cầu; mỗi lời gọi giữa hai dịch vụ có một span phía gọi và một span phía được gọi. *Span mang cờ*: span có thời lượng vượt mức nền theo luật của phương pháp. *Phép đổi*: chạy lại phương pháp với đúng một bước tính được thay, mọi thứ khác giữ nguyên.

**Ba mức kết luận.** *Xác nhận ở mức tính toán*: có phép đổi đúng một bước làm đổi hạng, hoặc đẳng thức đã kiểm bằng số. *Quan sát*: thấy trên giá trị trung gian, chưa có phép đổi. *Chưa phân xử*: còn từ hai giải thích trở lên. Không kết luận nào ở đây là về nguyên nhân vật lý của sự cố.

**Bốn loại nguồn hạn chế.** D: dữ liệu hoặc thiếu đầu vào. G: giao thức đánh giá. A: bản cài, adapter hoặc đầu vào do ta dựng. M: giả định hoặc cách tính của phương pháp theo bài gốc.

**Kiểm nguồn và phát lại.** Mọi phép đổi chạy trên bản phát lại đã khớp bản đóng băng **từng bit**: BARO 52/52, SimpleRCA 52/52, MicroRank 52/52 (48 chạy được, 4 lỗi tái lập đúng lỗi), TraceRCA 52/52, CIRCA 30/30, TORAI 90/90 (`ket-qua-phien-9.md` mục 1; `ket-qua-phien-10.md` mục 1.1, 5). Bảng tự động của phiên 12 nối lại các kết quả đó cho đủ 372 đơn vị và đạt 13/13 phép tự kiểm (`runs/tong-hop-phien-12-001/tu-kiem.json`). 372 bản ghi đóng băng trùng mã băm trong danh mục.

**Nơi có số.** Ba file kết quả theo phiên: `ket-qua-phien-9.md` (viết tắt KQ9), `ket-qua-phien-10.md` (KQ10), `ket-qua-phien-11.md` (KQ11), `ket-qua-phien-12.md` (KQ12) cho ba phép kiểm chạy sau, và `ket-qua-phien-13.md` (KQ13) cho sáu phép kiểm còn lại; mỗi số ở ba file đầu có đường dẫn và con trỏ JSON, đã soát bằng script (187 và 762 con số, 0 lệch). Bảng theo ca: `doi-chieu-dung-sai.json`. Phần đọc từng ca: `doc-tay.md`.

**Lưu ý sau REVIEW.** Các bản theo phiên và khóa no_signal trong JSON cũ được giữ để bảo toàn lịch sử. Khóa ấy chỉ đếm root không hạng 1 theo các cách chấm; không chứng minh không có đáp ứng do lỗi. Đọc kết luận hiện tại ở bản này và phần đính chính sau REVIEW của KQ13. Bằng chứng, bản trước và manifest mới ở runs/sua-review-001/.

## 2. Kết quả gốc cần giải thích

Số ca root đứng hạng 1 trên số ca chạy được (`doi-chieu-dung-sai.json` → `/dem_theo_phuong_phap`):

| Phương pháp | RE2-TT | Nezha-OB |
|---|---|---|
| BARO | 21/30 | 8/22 |
| SimpleRCA | 25/30 | 7/22 |
| MicroRank | 2/26 (4 ca lỗi) | 0/22 |
| TraceRCA | 21/26 (4 ca lỗi) | 2/22 (1 ca root không được xếp) |
| CIRCA | 16/30 | không chạy được (22 ca) |
| TORAI B | 26/30 (ba seed giống nhau) | không chạy được (22 ca) |

## 3. Bản đồ hạn chế

Mỗi dòng viết theo dạng: trong điều kiện X, bước Y làm mất hoặc đánh giá sai thông tin Z. Cột "Số ca" ghi n/N kèm nơi có số. Cột "Tác giả" ghi tác giả bài gốc có tự nêu không (dựa trên hồ sơ phương pháp của gói P1; riêng TraceRCA và MicroRank đã đọc lại bài và mã gốc trong task này). Các dòng có thể chồng lên nhau trên cùng một ca; **không cộng các dòng thành tỷ lệ nguyên nhân**. Bảng đối chiếu chi tiết từng dòng với lời của tác giả nằm ở `doi-chieu-tai-lieu-goc-phien-10.md` (mục 1, 3, 4).

### 3.1 MicroRank

| Mã | Điều kiện → bước → thông tin bị mất | Số ca | Mức | Tác giả | Loại |
|---|---|---|---|---|---|
| H1 | Trace có nhiều span → bước chia "trace có bất kỳ span nào vượt mức nền cộng 3 lần độ lệch chuẩn" của bản thư viện xếp khoảng một nửa trace vào nhóm bất thường → mất thông tin "trace nào thật sự chậm" | Thay riêng bước chia bằng công thức của bài gốc (span đầu do ta quy ước): tỷ lệ trace bất thường 50% → 10–12% (RE2-TT), 33% → 1,5–2,6% (Nezha-OB); root tăng hạng ở 19–20/25 và 13–15/22 ca; số ca hạng 1 từ 2/47 lên 21–22; 176–177/243 cặp mất. KQ11 mục 4.2. Phép thử mốc giả: không có lỗi nào vẫn có 36,6% trace bị xếp bất thường (trung vị 26 ca RE2-TT); trace không có root bị xếp bất thường ở 15,9% (mốc giả) so với 20,8% (mốc thật). KQ13 mục 1 | Xác nhận tính toán | Không áp dụng: bài gốc chia theo thời gian cả yêu cầu | A |
| H2 | Nhiều trace bất thường → bước đếm phủ của spectrum tính một thao tác cho mọi trace bất thường chứa nó → mất thông tin "thao tác nào tự chậm" | Đếm riêng thay đếm phủ: 115/252 cặp mất (RE2-TT 89/132, Nezha-OB 26/120); số ca hạng 1 từ 2 lên 19 trên 48. KQ9 mục 2 | Xác nhận tính toán | Không nêu | M |
| H3 | Trọng số PageRank theo nhóm trace nhân vào spectrum → tạo ưu thế cho một phần thực thể | Trọng số bằng 1: 28/252 cặp mất (RE2-TT 25/132, Nezha-OB 3/120); số ca hạng 1 từ 2 lên 11. KQ9 mục 2 | Xác nhận tính toán | Không nêu | M |

Phép đổi cờ sang phần span chưa được span con phủ giữ nguyên 248/252 cặp và 19/20 cặp dịch vụ gọi (KQ10 mục 2). Kết quả cho thấy đổi riêng đại lượng thời lượng chưa gỡ được đa số cặp; chưa đủ kết luận dịch vụ gọi không bị ảnh hưởng bởi chờ. Mã MicroRank chia một trace vào nhóm bất thường khi bất kỳ span nào mang cờ, rồi dùng mọi span của trace đó để dựng đồ thị và đếm phủ. Nếu cờ của dịch vụ gọi mất nhưng cờ của root hoặc dịch vụ khác còn, trace vẫn ở nhóm cũ; riêng thay đổi cờ ấy không đổi đồ thị/đếm phủ. Phần cờ giữ nhóm và chuyển nhóm đã thu bổ sung; tác dụng trọng số/điểm khi nhóm đổi còn OPEN.

**Bằng chứng M-D bổ sung sau REVIEW.** Bảng cờ theo trace khớp nguồn ở 48 ca chạy được, 4 ca ERROR giữ N/A; không chạy PageRank. Cả 20 ca có caller trực tiếp trên root ở native đều có trace mất toàn bộ cờ của một caller nhưng vẫn A do root/dịch vụ khác; 19 ca còn caller trên root dưới M-D. Ví dụ dev-5467884de4 có 7 trace như vậy, root hạng 5 → 5; tổng A cùng 484 nhưng có 1 A → N và 1 N → A. Do đó tổng nhóm/hạng gần giữ chưa bác bỏ chờ. Nhóm A/N là nhóm yêu cầu/trace, không gộp các dịch vụ thành một nguyên nhân. Thiếu đối chứng native đúng cùng dataset/fault cho 20 ca; chưa tách tác dụng trọng số khi nhóm đổi. Nguồn: runs/sua-review-001/md-partition/attempt-003/summary.json → /cases (postanalysis, transitions); kiểm độc lập kiem-md-doc-lap.json. Chi phí cả ba lượt 4 phút 47 giây, giữ cả hai lượt lỗi.

### 3.2 TraceRCA (bản trong thư viện)

| Mã | Điều kiện → bước → thông tin | Số ca | Mức | Tác giả | Loại |
|---|---|---|---|---|---|
| H4 | Dịch vụ gọi có span bao lời gọi tới root, lời gọi đó chậm đi → gắn cờ theo thời lượng cả span và tính span cho dịch vụ sở hữu nó → thời gian chờ root được chấm thành bất thường của dịch vụ gọi | Ở các cặp xét được: 4/4 cặp phía trên của RE2-TT (3/5 ca sai), 9/15 của Nezha-OB (8/19 ca sai). Có cả ở ca đúng: 83/96 dịch vụ phía trên ở 21 ca root hạng 1. KQ11 mục 2.1 | Xác nhận tính toán (ở RE2-TT kèm giả định về công cụ ghi span, mục 5.4) | Có nêu, và bài gốc có bước xử lý; bản thư viện bỏ bước đó. KQ11 mục 5 | A |
| H5 | Thao tác của root có ít span hơn thao tác của dịch vụ khác → điểm 2a/(n + H) đi theo số span mang cờ tuyệt đối → mất thông tin tỷ lệ | Xếp theo tỷ lệ: mất 11/15 và 43–46/75 cặp; xếp theo số tuyệt đối: giữ 14/15 và 68/75 cặp. Nhưng tỷ lệ làm 10–11/21 ca đang đúng của RE2-TT mất hạng 1. KQ11 mục 8. Mức cờ tự nhiên của thao tác đông span (mốc giả): trung vị 1,0%, tới 8,1%; sự cố chỉ làm tăng rõ ở thao tác phía trên root. KQ13 mục 2 | Xác nhận tính toán | Không áp dụng: bài gốc đếm trace, không đếm span | A |
| H6 | Root ở cuối chuỗi gọi, các dịch vụ phía trên chờ nó → bước xếp hạng của bài gốc lấy **trị tuyệt đối** của hiệu số lời gọi bất thường vào và ra → không mang hướng "ai chờ ai" | Ở các cặp "chủ yếu là chờ root": root đứng trên dịch vụ gọi ở 0/4 (RE2-TT) và 0/8 (Nezha-OB). Bản cài theo lời văn của bài, một đặc trưng; không phải mã của tác giả. KQ11 mục 9 | Xác nhận tính toán cho bản cài này | Nêu một phần (giới hạn khi lan hai chiều) | M + D |

### 3.3 Hai phương pháp trace, theo loại lỗi

| Mã | Điều kiện → bước → thông tin | Số ca | Mức | Tác giả | Loại |
|---|---|---|---|---|---|
| H7 | Trễ mạng → bất thường có thể hiện ở span phía gọi rõ hơn span của root → cách tính theo dịch vụ sở hữu span có thể chấm dịch vụ gọi cao hơn root | Nezha-OB, 6 ca: root đứng đầu theo span của mình ở 1/6, theo span phía gọi ở 5/6; BARO, SimpleRCA, TraceRCA xếp root hạng 1 ở 0 / 1 / 0 trên 6. KQ10 mục 3; KQ11 mục 7 | Quan sát; không suy ra span của root luôn không có tín hiệu hoặc mọi phép chấm theo nút đều thất bại | Nêu một phần | M + D |
| H8 | Return ở Nezha-OB → các cách chấm hiện tại chưa tách được root ở phần lớn ca; đáp ứng do lỗi còn chưa phân xử | 3/4 ca root không hạng 1 dưới các cách chấm trong bảng root-signal-by-fault, KQ11 mục 7. Root vẫn có span mang cờ ở các ca này; đó cũng chưa chứng minh cờ do lỗi | Quan sát về thứ hạng; không phải xác nhận thiếu tín hiệu trong dữ liệu | Bài MicroRank nêu giới hạn khi lỗi không đổi độ trễ; chưa xác nhận điều kiện ấy cho từng ca này | OPEN giữa dữ liệu và cách tính |

### 3.4 SimpleRCA và BARO

| Mã | Điều kiện → bước → thông tin | Số ca | Mức | Tác giả | Loại |
|---|---|---|---|---|---|
| H9 | Một cột metric vượt ngưỡng gần suốt cửa sổ → phiếu metric đếm theo số mẫu (tới 300 mỗi cột) cộng với phiếu trace, log chỉ 0 hoặc 1 → bằng chứng trace, log của root không bù được; mất thông tin biên độ | 60/64 cặp do riêng metric quyết định. Đếm theo cột: 16/20 cặp RE2-TT mất, nhưng số ca hạng 1 tính bi quan từ 25 xuống 10 vì hòa. KQ9 mục 4 | Xác nhận tính toán | Nêu một phần | A + M |
| H10 | Cột của dịch vụ khác gần phẳng ở đoạn nền → BARO chia cho IQR nền → thay đổi nhỏ thành điểm lớn | Đổi sang thang độ lệch chuẩn: 43/103 cặp RE2-TT mất; số ca hạng 1 từ 21 lên 24, không ca đúng nào hỏng. 60/103 cặp còn lại không do thang. KQ9 mục 5 | Xác nhận tính toán (RE2-TT); không kết luận ở Nezha-OB | Không nêu | M |
| H11 | Kênh bộ nhớ của RE2-TT trôi gần tuyến tính ngay trong đoạn nền → chuẩn hóa theo độ biến thiên nền → cột trôi của dịch vụ không liên quan nhận điểm cao | 19/55 cột mem thắng (BARO) và 6/15 (SimpleRCA) thuộc nhóm trôi nền. KQ10 mục 4 | Quan sát (giải thích một phần) | Không nêu | D + M |
| H12 | Thực thể trên root phần lớn nằm ngoài chuỗi gọi qua root → quan hệ gọi tới root không mang thông tin về chúng | BARO ở RE2-TT: 82/103 cặp ngoài chuỗi gọi hoặc không có span; chỉ 5/103 vừa trên chuỗi gọi vừa có cột đổi tại mốc. KQ11 mục 3 | Quan sát | Không áp dụng | D + M |

Giả thuyết bị bác ở BARO: "bước lọc cột hằng làm mất kênh quyết định của root". Không lọc: hạng root không đổi ở 52/52 ca (KQ9 mục 5).

### 3.5 CIRCA

| Mã | Điều kiện → bước → thông tin | Số ca | Mức | Tác giả | Loại |
|---|---|---|---|---|---|
| H13 | Một cột đứng yên ở 111 điểm train rồi đổi ở 10 điểm chấm → hồi quy theo nút cha rồi chia phần dư cho độ lệch chuẩn phần dư train (cỡ 1e-17) → điểm cỡ 1e16, mất thang | 11/30 ca, luôn cùng một nút; 0/11 khi bỏ cạnh. KQ10 mục 1.2 | Xác nhận tính toán | Không nêu | M |
| H14 | Một nút có điểm cực lớn → bước DA cộng điểm hậu duệ vào tổ tiên → thứ hạng của các dịch vụ kề bị ghi đè | 41 nút nhận giá trị qua DA. Cả 8 ca sai mang cờ lỗi số học có đúng 3 thực thể trên root và cả 3 đều mang giá trị cực lớn; bỏ cạnh thì root hạng 1 ở 8/8. Ba ca **đúng** còn lại có nút cực lớn là đúng vì chính root nhận giá trị đó (hạng trước DA: 8, 7, 2). KQ10 mục 1.3; `doc-tay.md` mục 5.1 | Xác nhận tính toán | Nêu một phần (DA cần kiểm thêm trên dữ liệu thật) | M |
| H15 | Hồi quy trên 111 điểm, chấm 10 điểm cuối → phần dư train nhỏ mà phần dư chấm không nhỏ theo → điểm có cạnh cao hơn điểm không cạnh | 3.285/4.526 nút; tỷ số tăng theo số cha (KQ10 mục 1.4). Đổi cửa sổ: trung vị nhóm từ 8 cha 7,54 → 3,40 (học 291 điểm), 3,64 (chấm ngay sau mốc); tỷ lệ nút tăng 72,6% → 67,3%, 73,1% (KQ13 mục 6) | Xác nhận phép tính; quan sát độ nhạy cửa sổ. Chưa tách riêng số điểm học, phân phối, vị trí chấm và tập nút | Có nêu dạng tổng quát | M + G |

Hệ quả phải nói rõ: **không đọc số của CIRCA thành "cấu trúc gọi giúp" hay "hại"** khi chưa loại 11 ca dính giá trị cực lớn. Ở 19 ca còn lại, bỏ cạnh không đổi số ca hạng 1 (12 → 12). Đọc tay thấy cả hai chiều: bỏ cạnh làm root tụt từ hạng 3 xuống 29 ở một ca; bước DA đẩy root từ hạng 2 xuống 15 ở một ca không dính lỗi số học, vì điểm lớn (2.027,36) của một nút thuộc dịch vụ không liên quan được cộng nguyên cho 13 thực thể khác (`doc-tay.md` mục 5.2, 5.3; `kiem-tiep.md` mục KT-15). Điểm lớn đó phụ thuộc độ dài đoạn học: trong nhánh chẩn đoán học trên 291 điểm, root của chính ca này về hạng 1 (KQ13 mục 6).

### 3.6 TORAI B

| Mã | Điều kiện → bước → thông tin | Số ca | Mức | Tác giả | Loại |
|---|---|---|---|---|---|
| H16 | Bảng log do ta dựng tách dòng log mang dữ liệu của từng yêu cầu thành nhiều mẫu hiếm → chấm z theo nền gần như không đổi → điểm log dồn về vài dịch vụ, không phụ thuộc root | Log là nguồn chênh lớn nhất ở 7/7 cặp của 4/30 ca sai. Bỏ nguồn log: 2/4 ca sai thành đúng ở cả ba seed, không ca đúng nào hỏng. Với bảng log của tác giả hiện tượng không lặp lại. KQ10 mục 5, 8; KQ11 mục 6 | Xác nhận tính toán | Nêu một phần | A |
| H17 | Bước nhân quả (RCD) không quyết định vị trí root | 0/90 đơn vị root do nhánh RCD xếp; 302/342 cụm nhiều dịch vụ rơi nhánh dự phòng. KQ9 mục 7 | Quan sát trên bản ghi | Không nêu | A |

Hệ quả: không rút kết luận nào về đồ thị nhân quả từ TORAI.

### 3.7 Hạn chế của dữ liệu

| Mã | Hạn chế | Số ca | Hệ quả cho đánh giá |
|---|---|---|---|
| D1 | Nezha-OB: trace chỉ có 41–97 giây nền; metric 5 mẫu mỗi phía | 22/22 | Mọi thống kê nền kém ổn định; phép đổi thang và bảng xu hướng không kết luận được ở Nezha-OB |
| D2 | Root không được dịch vụ nào gọi, hoặc quá ít lời gọi | 15/52 (8 ca root không được ai gọi) | Kết luận về chờ chỉ trên 37 ca; ở 8 ca quan hệ gọi tới root không thể giúp |
| D3 | Cửa sổ dev không có span mang mã lỗi | 30/30 ca RE2-TT | Nguồn lỗi trace của TORAI rỗng |
| D4 | Một thao tác có ở đoạn sau mốc mà không có ở nền | 4 ca RE2-TT | MicroRank và TraceRCA dừng lỗi; hiện tính là trượt. Bỏ thao tác đó thì root hạng 2, 2, 3, 12 (MicroRank) và 2, 1, 1, 1 (TraceRCA). KQ12 mục 2; KQ13 mục 4 |
| D5 | Một ca mất nhiều span (949/1.293 trace sau mốc có span mất cha) | 1 ca RE2-TT | Công thức chia trace của bài gốc không áp được |
| D6 | RE2-TT không công bố phiên bản mã, công cụ ghi span, quan hệ dịch vụ–máy | 30/30 | Việc "chờ" chỉ đo được một phần; không tách được "cùng máy" với "cùng chuỗi gọi" |
| D7 | Nezha-OB: nhịp metric khoảng 60 giây, trace không có mã trạng thái | 22/22 | CIRCA và TORAI không chạy được |

## 4. Hạn chế nào thuộc bản cài hoặc thiếu đầu vào, cần xử lý trước khi quy cho phương pháp

Đây là đầu ra số 2 của P4. Bốn nhóm:

1. **Thuộc bản trong thư viện, không thuộc bài gốc: H1, H4, H5.** Với MicroRank, đã thay bước chia bằng công thức của bài gốc và thấy khác rõ. Với TraceRCA, bài gốc làm việc trên lời gọi theo cặp dịch vụ, chọn đặc trưng, và có bước xét hướng lan; bản thư viện bỏ cả ba (KQ11 mục 5). Câu đúng khi báo cáo: "bản TraceRCA và MicroRank trong thư viện RCAEval có các hạn chế này", không phải "TraceRCA và MicroRank có các hạn chế này".
2. **Thuộc đầu vào do ta dựng: H16.** Nguồn log của TORAI B là bảng chúng tôi dựng vì bảng của tác giả lệch cửa sổ. Hạn chế ở nguồn log là của bảng đó.
3. **Thuộc quy ước ta điền vào chỗ bài không khóa: một nửa của H9** (đơn vị đếm "mỗi mẫu một phiếu" của SimpleRCA là quy ước của T-017).
4. **Thiếu đầu vào: D4, D7, và 44 đơn vị không chạy được ở Nezha-OB.** Không rút được kết luận nào về CIRCA và TORAI trên Nezha-OB.

**Cần sửa baseline hay giao thức không?** Không sửa trong T-032; cấu hình đã khóa và số đã chấm giữ nguyên. Ba điểm để Minh quyết ở tổng hợp G2:

- Có báo thêm, bên cạnh số chính, số của MicroRank với bộ chia theo bài gốc (21–22/47) như một dòng độ nhạy không. Ưu điểm trước giảng viên: cho thấy đã phân biệt bài gốc với bản thư viện. Nhược điểm: bộ chia đó dùng quy ước span đầu của ta, không phải MicroRank gốc; và được nghĩ ra sau khi xem dev.
- Bốn ca lỗi (D4) tính là "phương pháp trượt" như hiện nay, hay tách thành "không chạy được vì đầu vào" (`kiem-tiep.md` mục KT-8). Dữ kiện mới cho MicroRank (KQ12 mục 2): bỏ thao tác thiếu nền thì cả 4 ca chạy được, root hạng 2, 2, 3, 12; tức ở hạng 1 cách ghi nào cũng cho 0/4, ở 5 hạng đầu thì 3/4 ca đang bị tính trượt. Dữ kiện mới cho TraceRCA (KQ13 mục 4): root hạng 2, 1, 1, 1; tức với TraceRCA cách ghi **có đổi số ở hạng 1** (21/26 ca chạy được hiện nay; nếu coi là lỗi đầu vào và bỏ thao tác đó thì 24/30).
- Có giữ TORAI B làm cấu hình chính không, khi nguồn log do ta dựng là chỗ làm sai 2/4 ca.

## 5. Hạn chế thuộc cách tính, và câu trọng tâm về dịch vụ gọi

Đây là đầu ra số 3 của P4.

### 5.1 Các hạn chế loại M và giải thích cạnh tranh còn lại

- **H2, H3 (MicroRank, đếm phủ và trọng số).** Sau khi thay bộ chia, còn 25–26/47 ca root chưa hạng 1. Ghép thêm đếm riêng (KQ12 mục 1) tăng số hạng 1 từ 21–22 lên 23–27/47; RE2-TT đạt 17–19/25, Nezha-OB 6–8/22. Còn 20–24 ca. Bảng nối (KQ13 mục 5) cho frontend gắn với root ở 3/14 và 3/11 ca frontend đứng đầu, nên không thể gán toàn bộ cho H4, H7. Ba dạng quan sát được là: thao tác đứng đầu bao lời gọi chậm tới root; các trace tạo số đếm cho thao tác đứng đầu không có root; hoặc dưới 5 span tạo điểm. Đây chưa phải phân loại đầy đủ nguyên nhân: dev-14701a3bbb chưa rõ dưới cả hai luật; dưới luật code, dev-607751ac0a bị xếp không gắn nhưng vẫn có root trong 2/6 trace xét. Không gọi toàn bộ nhóm trace bất thường là không chứa root. Trên 52 đơn vị native có 46 OK sai, 2 OK đúng, 4 ERROR; phần đọc tay có 48 đơn vị gồm 46 OK sai, 1 ERROR và 1 đối chứng đúng (bao-phu-nhom.json → /units, method=microrank_full). Ba phản ví dụ của bộ chia mới được giữ; cơ chế các ca chưa rõ còn OPEN.
- **H10 (BARO, thang IQR).** Xác nhận cho 43/103 cặp. So ca đúng với ca sai cùng dịch vụ gốc và loại lỗi: mức đổi tương đối của root gần bằng nhau, điểm khác nhau 2,5–4 lần theo độ phẳng của nền (`doc-tay.md` mục 3.1). Giải thích cạnh tranh cho 60 cặp còn lại: cột của dịch vụ khác đổi thật tại mốc; nguyên nhân vật lý **không phân xử được bằng dữ liệu hiện có** (KT-6). Phép kiểm chuỗi cột ở ba cặp ca cùng ô (KQ13 mục 3) thêm hai điều: ở auth, delay cột độ trễ của root tăng 1,8–3,9 lần ở cả ba ca, z khác nhau vì nền dao động khác nhau; ở Nezha-OB có ca mà z = 94 của chính root là do IQR tính trên 5 mẫu nền. Đọc nốt cũng cho hai phản ví dụ với cách phân loại "thang gỡ được hay không" (`doc-tay.md` mục 8.1).
- **H13, H14 (CIRCA, giá trị cực lớn).** Chuỗi bằng chứng đủ từ đầu vào tới hạng, không có phản ví dụ: không nút nào mang giá trị cực lớn mà thiếu nguồn.
- **H15 (CIRCA, hồi quy làm tăng điểm).** Hai nhánh đổi cửa sổ cho trung vị tỷ số nhóm từ 8 cha thấp hơn: 7,54 xuống 3,40 và 3,64; vẫn có 67–73% nút tăng điểm (KQ13 mục 6). Cửa sổ có giá trị chẩn đoán vì thứ hạng cũng thay đổi, nhưng chưa xác định riêng nguyên nhân là số điểm học hay khoảng cách đến đoạn chấm: phân phối nền và tập nút đổi cùng. Cả hai mốc khai trước không đạt trọn. Cửa sổ đã khóa và số đã chấm giữ nguyên.
- **H9 (SimpleRCA).** Đếm theo mẫu vừa là thứ gây sai vừa là thứ cho phương pháp khả năng phân biệt; đổi cách đếm không chữa được.

### 5.2 Câu trọng tâm: khi dịch vụ gọi đứng trên root, đó là do chấm thời gian chờ, hay do cách chấm ưu tiên dịch vụ gọi?

Trả lời theo từng phương pháp, ở mức tính toán và chỉ trên dev:

- **TraceRCA: chấm thời gian chờ.** Chuỗi bằng chứng đủ bốn khâu: (1) trong mã nguồn, mọi lời gọi giữa hai dịch vụ quan sát được là lời gọi chặn (63/63 loại lời gọi ở Train Ticket trên cả bảy phiên bản ứng viên; 18/18 ở Online Boutique); (2) lời gọi tới root chậm đi sau mốc ở 19/21 và 10/16 ca đo được, trong khi các cạnh không dính root giữ mức nền; (3) span mang cờ của dịch vụ gọi chính là các span bao lời gọi chậm đó (4/4 và 9/15 cặp); (4) đổi cờ sang phần không được span con phủ làm 3/5 cặp dịch vụ gọi của RE2-TT biến mất. (KQ10 mục 6.2, 6.4; KQ11 mục 2.1; KQ9 mục 3.)
- **MicroRank: chưa phân xử đầy đủ đường chờ → cờ → nhóm trace → điểm.** Các tiêu chí hiện có không hỗ trợ chờ ở đa số cặp: dịch vụ phía trên chỉ 4/132 cặp RE2-TT (kỳ vọng ngẫu nhiên 18,5), và từ nửa trace bất thường gắn root ở 0/10,4/16 cặp. Quan sát nổi bật là thao tác có mặt trong nhiều trace bất thường không gắn root; ts-station-service đứng đầu 21/24 ca sai (KQ11 mục 1,2.2). Những số này không bác bỏ việc cờ do chờ góp phần giữ trace trong nhóm. Bổ sung theo trace được lưu riêng sau REVIEW; không lấy hạng gần như giữ nguyên để kết luận không có chờ.
- **SimpleRCA, BARO (kênh metric): một phần nhỏ.** Cột độ trễ của dịch vụ gọi có đổi theo (khớp với chờ), nhưng trong 103 cặp của BARO ở RE2-TT chỉ 5 cặp vừa nằm trên chuỗi gọi vừa có cột đổi tại mốc. BARO không nhận quan hệ gọi nào trong đầu vào, nên không thể "ưu tiên" dịch vụ gọi.
- **CIRCA:** dịch vụ gọi đứng trên root tập trung rõ (25 cặp so với kỳ vọng 3,5), nhưng cơ chế là giá trị cực lớn đi qua bước DA (H14), không phải chờ.
- **TORAI B:** một ca có dịch vụ gọi trên root; log, metric và độ trễ trace đều nghiêng về chúng.

**Hai điều phải nói kèm, bất lợi cho cách đọc đơn giản "sai vì nhầm triệu chứng":**

- Hiện tượng chờ có cả ở ca đúng (83/96). Thứ khác giữa ca đúng và ca sai của TraceRCA là số span mang cờ của dịch vụ gọi có vượt số của root hay không; đọc tay cho thấy điều đó do tải trong cửa sổ quyết định (`doc-tay.md` mục 1.2).
- Cờ "có dịch vụ phía trên đứng trước root" của T-028 (cờ M5) không đồng nghĩa "sai vì dịch vụ gọi": ở nhiều đơn vị mang cờ, thực thể đứng đầu và đa số thực thể trên root không nằm phía trên root.

### 5.3 Bảng theo ca cho các đơn vị có cờ M5

Bảng đầy đủ: `phan-xu-caller-root.json`, 82 đơn vị (80 ca × phương pháp; TORAI tính ba seed), mỗi thực thể phía trên có ba nhóm bằng chứng độc lập (tính toán, tín hiệu, khả năng đo chờ) và phần chưa biết. N của mỗi cột ghi ở đầu cột. Đây không phải nhãn lan và không cho tỷ lệ "lan có đáng kể".

| Dataset, phương pháp | Đơn vị trong cohort | Sai hạng 1 (chạy được) | Có cờ M5 | Trong đơn vị M5: thực thể đứng đầu nằm phía trên root | Thực thể phía trên, theo bằng chứng tính toán |
|---|---|---|---|---|---|
| RE2-TT, TraceRCA | 30 (4 lỗi) | 5 | 4 | 3/4 | 5 thực thể: 4 chấm thời gian chờ (xác nhận); 1 không xét được |
| Nezha-OB, TraceRCA | 22 | 20 | 16 (1 ca không xác định) | 12/16 | 20 thực thể: 9 chấm thời gian chờ; 6 dưới ngưỡng 50%; 5 không xét được |
| RE2-TT, MicroRank | 30 (4 lỗi) | 24 | 5 | 0/5 | 10 thực thể: cả 10 có dưới nửa số trace bất thường gắn với root |
| Nezha-OB, MicroRank | 22 | 22 | 20 | 0/20 | 20 thực thể: 16 dưới nửa; 4 từ nửa trở lên |
| RE2-TT, SimpleRCA | 30 | 5 | 5 | 4/5 | 7 thực thể: 6 do riêng phiếu metric quyết định |
| Nezha-OB, SimpleRCA | 22 | 15 | 9 | 6/9 | 9 thực thể: 6 do riêng phiếu metric quyết định |
| RE2-TT, BARO | 30 | 9 | 3 | 1/3 | 11 thực thể; BARO không nhận quan hệ gọi |
| Nezha-OB, BARO | 22 | 14 | 7 | 2/7 | 7 thực thể |
| RE2-TT, CIRCA | 30 | 14 | 10 | 9/10 | 26 thực thể: 24 mang giá trị cực lớn sau DA; 2 không |
| RE2-TT, TORAI B | 90 (30 ca × 3 seed) | 12 | 3 | 3/3 | 6 thực thể (2 × 3 seed): nguồn chênh lớn nhất là log |

Nguồn: `phan-xu-caller-root.json` → `/dem_theo_dataset_phuong_phap`, `/bang_chung_tinh_toan_theo_thuc_the`; cột thứ năm đếm từ `doi-chieu-dung-sai.json` → `/don_vi/*/vi_tri_chuoi_goi/vi_tri_thuc_the_dung_dau` trên đúng các đơn vị M5. CIRCA và TORAI ở Nezha-OB: 22 đơn vị mỗi phương pháp, không chạy được, không có cờ.

### 5.4 Đo được việc "dịch vụ gọi chờ root" tới đâu

Xếp theo ba mức của đề bài, theo từng ca (`kha-nang-do-trace.json`; tiêu chí và độ phủ ở `coverage-trace.json`):

| Mức | RE2-TT | Nezha-OB | Nghĩa |
|---|---|---|---|
| Đo được | 0 | 16 | Có cạnh gọi tới root đủ lời gọi; khoảng thời gian hợp lệ; mã nguồn cho thấy lời gọi chặn; gắn được phiên bản mã (một commit công khai sinh đủ 55/55 tên span). Điều kiện: mã lúc thu dữ liệu trùng bản công khai |
| Đo được một phần | 21 | 0 | Ba tiêu chí đầu đạt ở cả bảy phiên bản ứng viên; thiếu đúng một bằng chứng: công cụ và phiên bản đã ghi span, tác giả không công bố |
| Không đo được | 9 | 6 | Root không được dịch vụ nào gọi (6 + 2 ca), hoặc cạnh dưới 20 lời gọi ở một phía (3 + 4 ca) |

Ở mọi ca, **không đo được** phần chậm nằm ngoài span của root là gì (đường truyền, hàng đợi, hay xử lý quanh lời gọi), vì mỗi lời gọi chỉ có hai span.

Đã thử gì để gắn phiên bản cho RE2-TT, và kết quả (KQ10 mục 6.1): đọc bài và kho RCAEval (không nêu phiên bản); đối chiếu 58 tuyến, 39 tên span tầng dữ liệu và 27 dịch vụ với mười phiên bản của Train Ticket (bảy phiên bản khớp đủ, ba bị loại); dò thư viện ghi span trong từng phiên bản (khác nhau giữa các phiên bản). Bằng chứng còn thiếu: cấu hình triển khai của nhóm tác giả RCAEval. Việc cần làm nếu muốn nâng mức: hỏi tác giả; Minh đã chọn chấp nhận giới hạn này (gói bổ sung, phần C).

## 6. Quan hệ giữa các dịch vụ có thể bổ sung thông tin gì

Đây là đầu ra số 4 của P4. Mọi mục dưới đây là **căn cứ để đề xuất ứng viên**, theo bậc thứ nhất của bảng mức căn cứ trong kế hoạch nghiên cứu. Chưa mục nào là bằng chứng rằng đồ thị giúp; điều đó cần đối chứng bỏ quan hệ và đồ thị ngẫu nhiên ở gói P6–P7.

**Bốn loại thông tin quan hệ có căn cứ:**

1. **Thời gian của lời gọi, gắn vào cạnh và tính cho dịch vụ được gọi.** Căn cứ: root đứng đầu theo span phía gọi của lời gọi tới nó ở 18–19/20 ca RE2-TT và 11–13/20 ca Nezha-OB; phép thử giả với mốc lùi vào nền cho 0–2 và 0–4 ca (KQ10 mục 3). Nhắm vào H4 và H7. Phép tính dùng cạnh: tỷ lệ lời gọi **đi vào** một dịch vụ có span phía gọi vượt nền.
2. **Phần của span không do span con phủ, cần quan hệ cha–con trong trace.** Căn cứ: tách được root ở 26/26 ca RE2-TT có bảng span, so với 8/26 theo cờ thời lượng đang dùng; phép thử giả 0/26 (KQ10 mục 3). Điều kiện thất bại đã thấy: ở Nezha-OB chỉ 10/22; 19,6% span ở Nezha-OB có span con chạy chồng nhau, nên phép trừ phải xử lý chồng lấn (KQ11 mục 4.1).
3. **Hướng của cạnh phải được giữ.** Căn cứ: bước xét hướng lan của bài TraceRCA, khi lấy trị tuyệt đối, cho 0/4 và 0/8 (H6). Phương án có sẵn trong tài liệu không đủ; phép tính phải phân biệt "lời gọi đi vào bất thường, lời gọi đi ra bình thường".
4. **Tiêu chí "yêu cầu bất thường" theo cả cây lời gọi của một yêu cầu.** Căn cứ: H1. So thời gian cả yêu cầu với tổng mức nền của các thao tác trong cây cho nhóm trace bất thường nhỏ hơn và chứa root nhiều hơn (tỷ lệ trace bất thường có span của root: 52% → 63–70% ở RE2-TT).

**Hai yêu cầu kỹ thuật cho mọi bước lan điểm trên đồ thị** (rút từ CIRCA): chặn giá trị không hợp lệ ở một nút trước khi lan (H13, H14); không chép nguyên điểm lớn nhất của nút con sang mọi nút cha, vì một điểm lớn ở dịch vụ không liên quan sẽ kéo cả dãy nút cha vượt root (thấy ở ba ca không dính lỗi số học, `kiem-tiep.md` mục KT-15; điểm lớn đó phụ thuộc độ dài đoạn học, KQ13 mục 6).

**Sáu điều bất lợi cho hướng dùng quan hệ gọi tới root, ghi đúng như đã thấy:**

1. Phần lớn cặp sai của MicroRank và BARO không nằm phía trên root: 24/252 và 15/162 cặp (KQ11 mục 1). Một thành phần chỉ "trừ phần kế thừa từ phía dưới" không chạm tới chúng.
2. "Span chờ root" có cả ở ca đúng (83/96), nên tự nó không phân biệt ca sai.
3. Với kênh metric ở RE2-TT, quan hệ gọi chỉ chạm 5/103 cặp của BARO; 82/103 nằm ngoài chuỗi gọi hoặc không có span.
4. Bước xét hướng lan có sẵn trong tài liệu không tách được root (H6).
5. 15/52 ca không đủ lời gọi tới root; trong 8 ca không có cạnh gọi đi vào root. Các quan hệ đi ra, cha–con, máy–dịch vụ hoặc log/metric chưa được phép này đánh giá. Với return, root không đứng đầu dưới cách chấm hiện tại; đáp ứng do lỗi vẫn OPEN.
6. Một bước dùng cấu trúc (DA của CIRCA) đã làm hỏng thứ hạng khi gặp một giá trị lỗi.

**Hai điều thuận:** với TraceRCA chuỗi bằng chứng "dịch vụ gọi chờ root rồi bị chấm bất thường" đủ bốn khâu; với MicroRank, chỗ hỏng lớn nhất là bước chia của bản thư viện, không phải phần dùng đồ thị của bài gốc.

**Thêm ở phiên 13, một thuận và một giới hạn.** Tỷ lệ cờ thao tác phía trên root tăng 0,8% → 6,2% giữa mốc giả/thật cùng độ dài cửa sổ, còn thao tác không liên hệ giữ 1,1–1,2% (KQ13 mục 2); với TraceRCA có chờ qua hai tầng gọi với cùng số span (doc-tay mục 8.3 điểm 8). Đây là căn cứ đề xuất thử gắn theo từng cạnh. Trong phần MicroRank còn sai, 8–10/20–24 ca có thao tác đứng đầu gắn root theo tiêu chí bảng nối; các ca khác gồm không gắn, ít span và chưa rõ, không tự chứng minh mọi quan hệ đồ thị đều không giúp.

**Nối với các ứng viên trong kế hoạch nghiên cứu (P6):**

- Ứng viên "tách bất thường tự sinh và kế thừa theo đồ thị" (tầng 2): có căn cứ ở dạng mục 1 và 2 ở trên, cho kênh trace. Kế hoạch ghi "chỉ giữ nếu P4 xác nhận hạn chế đó trên dev": P4 xác nhận nó cho TraceRCA và cho lỗi trễ mạng, **không** xác nhận nó là cơ chế chiếm đa số. Giữ hay không là quyết định của Minh.
- Cách "quy tắc phân rã theo cây lời gọi": có căn cứ (mục 2), kèm điều kiện thất bại về chồng lấn.
- Cách "hồi quy có điều kiện trên nút cha, giống CIRCA": bằng chứng trên dev **bất lợi** (H13–H15), trừ khi xử lý được giá trị cực lớn và cửa sổ.
- Cách xếp hạng "kiểu MicroRank": ghép bộ chia và đếm riêng cho 17–19/25 ca RE2-TT, 6–8/22 ca Nezha-OB hạng 1 (KQ12 mục 1). Phần còn lại có ba dạng quan sát cùng ca chưa rõ và một ca không gắn nhưng vẫn có root trong trace xét (KQ13 mục 5). Chưa đủ chọn hay loại thiết kế. Luật theo từng span xếp 37% trace bất thường ở mốc giả (KQ13 mục 1), là căn cứ thử tiêu chí cả yêu cầu, chưa xác nhận lợi ích trên test.

## 7. Câu chưa trả lời

Đây là đầu ra số 5 của P4. Chi tiết từng câu (giải thích cạnh tranh, phép kiểm, thứ giữ cố định, dự đoán, chi phí, quyết định phụ thuộc) ở `kiem-tiep.md`, 16 mục. Xếp theo loại:

- **Chưa chạy, rẻ, dữ liệu có sẵn:** TORAI với bảng của tác giả (KT-7, 15 phút; không ảnh hưởng P5–P6).
- **Đã chạy ở phiên 12–13:** KT-3 và bảng nối MicroRank; KT-15 về DA; KT-8 cả hai nửa; KT-1, KT-2 mốc giả; KT-12 chuỗi độ trễ; KT-9 cửa sổ; đọc tay nốt. Bảng nối có ba dạng quan sát và ca chưa rõ. Nezha-OB có phép thử giả giữa nền ở runs/root-signal-placebo-003/ (22/22 ca), nhưng nền ngắn và cửa sổ không tương đương mốc thật; không thay phép KT-1 lùi 150 giây. BARO/SimpleRCA trong bảng placebo là số mốc thật được nối vào, không phải đo lại ở mốc giả. Đáp ứng return còn OPEN; phần tăng điểm CIRCA và một mẫu P99 cũng còn mở.
- **Thiếu dữ kiện:** mã của tác giả TraceRCA (KT-11; phải dựng định dạng dữ liệu riêng, 0,5–1 phiên).
- **Không phân xử được bằng dữ liệu hiện có:** vì sao metric và thời lượng span của dịch vụ không liên hệ đổi tại mốc (KT-6; ví dụ mới: đăng nhập của `ts-auth-service` ở các ca order, loss); phần chậm ngoài span của root là gì (KT-13).
- **Thuộc gói sau:** ứng viên dùng cạnh có tách được root không (KT-5, thuộc P5–P6); "lan có đáng kể" không (KT-10, thuộc tổng hợp G2); kết quả trên test (KT-16, sau G3).
- **Mức đọc tay:** đã đọc 144/192 đơn vị sai hoặc không OK; 48 đơn vị không chạy được ghi theo lý do (KT-14; `doc-tay.md` mục 8).

- **Bổ sung sau REVIEW được Minh duyệt:** đã thu cờ/nhóm trace MicroRank M-D và kiểm số đọc tay từ đầu vào/kết quả cũ, không chạy lại PageRank (gói runs/sua-review-001/). Ca dev-14701a3bbb chưa phân xử vì sao thao tác đứng đầu được chấm cao; dev-607751ac0a dưới luật code không gắn theo cây con dù root có trong một phần trace xét. Nhãn dịch vụ gây lỗi đã biết; điều chưa rõ là bước nào làm xếp sai và cách sửa nào có căn cứ.

## 8. Yêu cầu quan sát rút ra cho hệ bán vé FlashTicket

Rút từ các hạn chế dữ liệu đã xác nhận. Bộ thu thập không khôi phục được thông tin chưa từng được ghi, nên các điểm này phải có từ lúc gắn công cụ đo.

1. Ghi cả span phía gọi và span phía được gọi cho mọi lời gọi giữa hai thành phần, có loại span và mã trạng thái (từ H4, H7, D3).
2. Thêm một mốc thời gian ở phía được gọi lúc yêu cầu tới, trước hàng đợi (từ KT-13).
3. Ghi phiên bản mã, công cụ ghi span và cấu hình lấy mẫu cùng với dữ liệu (từ D6).
4. Ghi quan hệ dịch vụ–máy và metric mức máy (từ H12, KT-6).
5. Đoạn nền đủ dài và metric đủ dày: Nezha-OB chỉ có 41–97 giây trace và 5 mẫu metric mỗi phía (từ D1).
6. Đồng bộ đồng hồ giữa các máy, hoặc không dựa vào hiệu thời điểm giữa hai máy (từ KQ10 mục 6.3).
7. Ghi thời điểm và đối tượng của mỗi lần tiêm lỗi (từ KT-6).
8. Mẫu log ổn định: không để dữ liệu của từng yêu cầu làm sinh mẫu mới (từ H16).

## 9. Mười giới hạn đã chấp nhận

Theo phần C của gói bổ sung Minh duyệt ngày 11/10/2026.

| Giới hạn | Loại | Hệ quả |
|---|---|---|
| Train Ticket không công bố phiên bản mã và công cụ ghi span; không hỏi tác giả | Dữ liệu | Việc "chờ" chỉ đo được một phần ở 21 ca |
| Mỗi lời gọi chỉ có hai span | Dữ liệu | Không tách đường truyền, hàng đợi, xử lý bên gọi |
| Online Boutique: nền trace 41–97 giây, metric 5 mẫu mỗi phía | Dữ liệu | Thống kê nền kém ổn định; bảng xu hướng và phép đổi thang không kết luận được |
| 15/52 ca không đủ lời gọi tới root | Dữ liệu | Kết luận về chờ trên 37 ca; ở 8 ca cách dựa riêng vào cạnh đi vào root không áp dụng. Chưa kết luận về mọi loại quan hệ đồ thị |
| Cửa sổ dev không có span mang mã lỗi | Dữ liệu | Nguồn lỗi trace của TORAI rỗng ở 30/30 ca |
| Chỉ 52 ca dev, mỗi ô vài ca, chưa mở test | Giao thức | Không rút mẫu hình theo ô; mọi số là bằng chứng trên dev |
| CIRCA: giá trị cực lớn; ảnh hưởng của cửa sổ chỉ tách được một phần, trong nhánh chẩn đoán (KQ13 mục 6) | Thuật toán | Giữ bản gốc; nêu là hạn chế của cách tính |
| MicroRank: phần cặp còn lại sau các phép đổi | Thuật toán | Còn 25–26/47 ca sau thay bộ chia, 20–24/47 sau ghép đếm riêng; có ba dạng quan sát, ca chưa rõ và ca không gắn nhưng root vẫn hiện diện (KQ13 mục 5). Không ép thành ba nguyên nhân bao trùm |
| SimpleRCA: đếm theo mẫu vừa gây sai vừa là nguồn phân biệt | Thuật toán | Không sửa được bằng đổi cách đếm |
| TORAI: bước nhân quả không tham gia xếp root | Cài đặt của thư viện | Không rút kết luận về đồ thị nhân quả từ TORAI |

Giới hạn thêm của chính task này: các định nghĩa vị trí, mốc đếm (phân vị 95, 20 lời gọi, 50%, 90%) và phần lớn phép đổi do người làm đặt sau khi đã xem kết quả dev trước đó; số thô được lưu để kiểm lại với mốc khác.

## 10. Đối chiếu với tiêu chí xong của đề bài task

| Tiêu chí | Trạng thái | Ghi chú |
|---|---|---|
| 1. Kiểm nguồn đạt, phát lại khớp, không thay kết quả đóng băng | Đạt | Mục 1 |
| 2. Danh mục nhóm được phủ bởi bảng toàn bộ và đơn vị đọc tay; mọi đơn vị M5 có trạng thái theo ca | Đạt | Bảng phủ 372/372; đọc tay 52/52 nhóm, 168 đơn vị (144 sai hoặc không OK, 24 đối chứng); 48 đơn vị không chạy được ghi theo lý do; 82/82 đơn vị M5 |
| 3. Chỉ nhận cơ chế khi có chuỗi đầu vào → xử lý → trung gian → đầu ra | Đạt một phần | Một số chuỗi tính toán đã xác nhận; đáp ứng return, tác dụng trọng số/điểm khi nhóm MicroRank đổi, ca ghép chưa rõ và nguyên nhân độ nhạy cửa sổ chưa phân xử hết |
| 4. Đủ năm đầu ra P4; mức đo chờ theo dataset; bảng theo ca cho tổng hợp G2 | Đạt | Mục 3–7; `kha-nang-do-trace.json`; `phan-xu-caller-root.json` |
| 5. Phép đổi trọng số A′: thiết kế, quyền chạy, trạng thái | Đạt | Đã chọn (Q-92), duyệt chạy (Q-93), chạy ở phiên 9 trên 48 ca đủ điều kiện, 4 ca không đủ; chi tiết theo ca ở `can-thiep-tinh-toan.json`. A′ chỉ so toàn gói trọng số, không phân xử câu dịch vụ gọi |
| 6. Nhật ký và bàn giao | Đạt | LOG phiên 12–13 và mục sửa sau REVIEW; bản sửa chờ kiểm lại độc lập |

**Phần mục tiêu nguồn mà task này chưa phủ:** (a) chưa có số trên test; (b) chưa trả lời "lan có đáng kể" (để tổng hợp G2 quyết); (c) chưa đánh giá ứng viên đồ thị nào; (d) nguyên nhân vật lý của các thay đổi ở dịch vụ không liên hệ; (e) TraceRCA và MicroRank đúng bản của tác giả chưa chạy được.

## 11. Điều cần Minh quyết

1. **Mức đọc tay:** đã đọc hết theo lời duyệt của Minh (Q-141); không còn gì để quyết.
2. **Các phép kiểm còn lại:** đã chạy hết các phép Minh duyệt (KQ13). Còn hai phép chưa chạy, cả hai tôi đề nghị không chạy trước G2: KT-7 (không ảnh hưởng P5–P6) và KT-11 (0,5–1 phiên; chỉ nâng mức chắc của câu "phương án có sẵn trong tài liệu không đủ").
3. **Cách ghi bốn ca lỗi và số độ nhạy ở bảng G2** (mục 4). Dữ kiện mới: với TraceRCA, 3/4 ca lỗi sẽ là hạng 1 nếu bỏ thao tác thiếu nền. Giữ số chính như đã khóa và thêm một dòng độ nhạy thì ưu điểm trước giảng viên là không phải sửa giao thức mà vẫn cho thấy đã tách lỗi đầu vào khỏi lỗi phương pháp; nhược điểm là thêm một con số được nghĩ ra sau khi xem dev.
4. **"Lan có đáng kể" hay không, và có định nghĩa nhãn lan không** (KT-10): thuộc tổng hợp G2; T-032 chỉ cung cấp bảng.
5. **Ứng viên nào ở mục 6 được đưa vào đề bài P5–P6.**
