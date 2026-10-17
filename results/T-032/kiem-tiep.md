# T-032 — Các câu còn phải kiểm, và cách kiểm

Người làm: Claude, phiên 12 (11/10/2026); cập nhật ở phiên 13 cùng ngày. Mỗi mục ghi: câu hỏi; đã thử gì và ra gì; các giải thích còn cạnh tranh; phép kiểm cụ thể; thứ giữ cố định; dự đoán phân biệt; phạm vi và chi phí; quyết định bị ảnh hưởng. Minh đã duyệt chạy (Q-141) và phiên 13 đã chạy: KT-1, KT-2, KT-8 (nửa TraceRCA), KT-9, KT-12, bảng nối của KT-3, và đọc tay nốt (KT-14). Kết quả ở `ket-qua-phien-13.md` (KQ13). Ở mỗi mục đã chạy, phần kết quả đặt ở đầu, chữ viết trước khi chạy giữ nguyên bên dưới để đối chiếu. Các mục chưa chạy: chi phí là ước lượng, chưa đo.

Ba loại trạng thái, ghi ở đầu mỗi mục:

- **Chưa chạy:** dữ liệu và công cụ có sẵn, chỉ cần quyền và thời gian.
- **Thiếu dữ kiện:** phải thu hoặc dựng thêm thứ chưa có.
- **Không phân xử được bằng dữ liệu hiện có:** thông tin cần thiết chưa từng được ghi; chỉ hệ đo mới (FlashTicket) trả lời được.

Mục nào đã có một phần câu trả lời trong phiên 12 thì ghi rõ phần đã trả lời.

## Bảng tóm tắt

| Mã | Câu hỏi | Trạng thái | Chi phí | Quyết định phụ thuộc |
|---|---|---|---|---|
| KT-1 | Vì sao khoảng nửa trace sau mốc mang cờ dù không gắn với root | **Đã chạy ở phiên 13**; phần lớn là mức tự nhiên của luật chia | — | Tiêu chí "trace bất thường" ở P6 |
| KT-2 | Thao tác đông span có 2–9% span mang cờ: nền tự nhiên hay do sự cố | **Đã chạy ở phiên 13**; cả hai, tách được theo vị trí so với root | — | Có cần hiệu chỉnh ngưỡng theo thao tác ở P6 |
| KT-3 | 25–26/47 ca MicroRank chưa hạng 1 sau thay bộ chia | Đã chạy phiên 12–13; ba dạng quan sát, còn ca chưa rõ và ca không gắn nhưng có root | — | Có lấy kiểu xếp hạng MicroRank làm ứng viên |
| KT-4 | 40 cặp "chung phía trên" của TraceRCA ở Nezha-OB | **Đã trả lời phần lớn trong phiên 12** | — | — |
| KT-5 | Gắn tín hiệu của span phía gọi cho dịch vụ được gọi có tách được root không | Chưa chạy; thuộc P5–P6 | 0,5–1 phiên | Chọn cơ chế tầng 1–2 của P6 |
| KT-6 | Vì sao cột metric của dịch vụ không liên hệ đổi tại mốc | Không phân xử được | — | Yêu cầu quan sát FlashTicket |
| KT-7 | TORAI với bảng của tác giả: vì sao nguồn độ trễ trace nghiêng về dịch vụ khác | Chưa chạy | 15 phút EC2 | Không ảnh hưởng P5–P6 |
| KT-8 | Bốn ca ERROR: bỏ thao tác thiếu nền thì root xếp thứ mấy | **Đã chạy cả hai nửa** (phiên 12, 13) | — | Cách ghi 4 ca này ở bảng G2 |
| KT-9 | CIRCA nhạy với cửa sổ hay số cha | Đã chạy phiên 13; trung vị tỷ số thấp hơn trong hai nhánh, chưa tách riêng nguyên nhân | — | Có dùng hồi quy theo cấu trúc ở P6 |
| KT-10 | "Lan có đáng kể" không; điều kiện để định nghĩa nhãn lan | Thuộc tổng hợp G2 | — | Có tách nhãn lan ở G3 |
| KT-11 | Mã của tác giả TraceRCA cho kết quả gì trên dev | Thiếu dữ kiện (phải dựng định dạng) | 0,5–1 phiên | Mức chắc của câu "phương án có sẵn không đủ" |
| KT-12 | Cột độ trễ của root phản ứng ở ca này, không ở ca kia cùng ô | **Đã chạy ở phiên 13**; ba cặp, ba lý do | — | Phân loại "lỗi không hiện ở metric" |
| KT-13 | Phần chậm nằm ngoài span của root là gì | Không phân xử được | — | Yêu cầu quan sát FlashTicket |
| KT-14 | Đọc tay đủ 192 đơn vị sai | **Đã làm ở phiên 13**: 144 đơn vị đọc, 48 ghi theo lý do | — | Mức chắc của phần đọc tay |
| KT-15 | DA có bất lợi cho dịch vụ không có cạnh không | **Đã chạy trong phiên 12**; cách đọc ban đầu bị sửa; KT-9 thêm một điều chỉnh | — | Thiết kế bước lan điểm ở P6 |
| KT-16 | Các kết luận có giữ trên test không | Chờ G3 | — | Mọi khẳng định hiệu quả |


## Bổ sung sau REVIEW được Minh duyệt 11/10

- **Return và vị trí tín hiệu: OPEN.** Root không hạng 1 khác với dữ liệu không có đáp ứng. Đã có mốc giả giữa nền Nezha ở runs/root-signal-placebo-003/; nền ngắn, cửa sổ/baseline khác mốc thật và BARO/SimpleRCA được nối từ số thật. Cần đối chứng đáp ứng cùng đại lượng và cửa sổ đủ tương đương để tách lỗi khỏi nền; hiện chưa đủ kết luận không có tín hiệu. Ảnh hưởng: không quy H8 hoàn toàn cho dataset, không loại thiết kế quan sát chỉ từ hạng. FlashTicket cần log mã lỗi và nền phù hợp; collector không khôi phục dữ liệu chưa ghi.
- **MicroRank M-D, cờ → nhóm → điểm: đã thu bổ sung** tại runs/sua-review-001/md-partition/. Dựng lại cờ duration/uncovered và OR theo trace từ đầu vào cũ; lưu dịch vụ giữ nhóm, trace đổi A/N và coverage/count theo thao tác; không chạy lại PageRank. Nhãn chỉ nối sau để diễn giải. Chi phí đề xuất 20–30 phút là ước lượng; thực tính cả ba lượt 4 phút 47 giây. Khi nhóm bất thường/bình thường và đồ thị đầu vào không đổi, xóa cờ riêng caller không làm đổi đếm phủ; khi nhóm đổi, chưa suy được hạng nếu chưa lần theo trọng số/điểm. Bảng khớp 48 ca chạy được, 4 ERROR giữ N/A; 20/20 ca caller trực tiếp trên root có trace caller mất cờ nhưng vẫn A do root/other, 19 ca còn caller trên root dưới M-D. Không có đối chứng native đúng cùng dataset/fault cho 20 ca. Nguồn: md-partition/attempt-003/summary.json và kiem-md-doc-lap.json trong gói; không tách tác dụng trọng số khi nhóm đổi. Ảnh hưởng: kết luận bước OR/đếm đã kiểm, không bác chờ vật lý.
- **Ca ghép chưa rõ: OPEN.** dev-14701a3bbb dưới cả hai luật, dev-607751ac0a luật code có root nhưng không gắn theo cây con. Thiếu chuỗi đồ thị → trọng số → số đếm → điểm theo thao tác cho đúng các ca này và đối chứng tương ứng; đọc trung gian cũ trước khi đề xuất lượt mới. Chưa có chi phí đáng tin cho phần thu thêm (nếu thiếu), không tự chạy ngoài quyền. Ảnh hưởng: chưa chọn thành phần để chữa phần còn lại chỉ từ ba dạng quan sát.
- **CIRCA: OPEN về nguyên nhân độ nhạy cửa sổ.** Giữ số và hai mốc không đạt trọn. Muốn tách nguyên nhân cần giữ tập nút và tách thay đổi độ dài khỏi phân phối/giai đoạn lỗi; chưa có thiết kế hay chi phí cho phép mới, không dùng như căn cứ đã xác nhận.

## KT-1. Vì sao khoảng một nửa trace sau mốc mang cờ dù không gắn với root

**Kết quả phiên 13 (KQ13 mục 1; `runs/fake-marker-001/summary.json`; `runs/tong-hop-phien-13-001/derived-013.json → /kt1`).** Tự kiểm với H_native và lượt `chain-spanpass-001` đạt 26/26.

- Không có lỗi nào trong đoạn xét, luật chia vẫn xếp 36,6% trace là bất thường (trung vị 26 ca; từ 11% tới 43%); mốc thật cùng độ dài cửa sổ: 51,9%.
- Ba mốc khai trước: (a) không đạt ở vế "độc lập" (1/26 ca), (b) không đạt (0/26), (c) không đạt (0/26 ca đổi theo vị trí mốc). Theo mốc: "không phân xử rõ". Mốc (a), (b) của tôi so hai tập trace khác loại; ghi rõ ở KQ13.
- So cùng loại trace (tính sau khi xem kết quả): trace không có root 15,9% ở mốc giả so với 20,8% ở mốc thật, tỷ số theo ca trung vị 0,93; trace có root 46,7% so với 93,5%.
- **Trả lời:** giải thích (a) được hỗ trợ về bản chất (trace không dính root bị xếp bất thường gần bằng tần suất lúc không có sự cố), trừ phần "độc lập"; (b) chỉ đóng phần nhỏ; (c) không được hỗ trợ.
- **Còn mở:** Nezha-OB không kiểm được (nền quá ngắn).

Phần dưới đây là mục như đã viết trước khi chạy, giữ để đối chiếu. Lưu ý: dòng "giữ cố định độ dài cửa sổ nền" không làm được với mốc giả; thiết kế 013 đã thay bằng so mốc thật và mốc giả ở cùng độ dài cửa sổ.

- **Đã có.** Tỷ lệ trace bị xếp bất thường: trung vị 50% ở RE2-TT, 33% ở Nezha-OB (`ket-qua-phien-9.md` mục 2). Trong các trace bất thường chứa thao tác của thực thể đứng trên root, khoảng một nửa gắn với một dịch vụ không phải root (`ket-qua-phien-11.md` mục 2.2). Thay bộ chia bằng công thức của bài gốc đưa tỷ lệ xuống 10–12% và 1,5–2,6% (mục 4.2). Đọc tay: ở ca `dev-16597725c1`, 504/755 trace bất thường không đi qua root (`doc-tay.md` mục 2.3).
- **Giải thích cạnh tranh.** (a) Thuần xác suất: một trace có hàng chục tới hàng trăm span; mỗi span có xác suất nhỏ vượt 3 lần độ lệch chuẩn; xác suất "ít nhất một span vượt" vì vậy lớn, kể cả khi không có sự cố. (b) Sự cố làm chậm thật nhiều trace không đi qua root (tài nguyên chung). (c) Nền 300 giây không đại diện.
- **Phép kiểm.** Trên bảng span đã lưu của 26 ca RE2-TT: đặt mốc giả lùi 150 giây (không có lỗi trong khoảng xét, như phép thử giả của bảng A), áp đúng luật gắn cờ và luật chia của bản thư viện, đo tỷ lệ trace bất thường. Đồng thời tính tỷ lệ dự đoán từ số span của từng trace và tỷ lệ vượt nền theo thao tác.
- **Giữ cố định:** luật cờ, tập thao tác, độ dài cửa sổ nền. **Chỉ đổi:** vị trí mốc.
- **Dự đoán phân biệt.** Nếu (a): tỷ lệ ở mốc giả gần tỷ lệ ở mốc thật của các trace không đi qua root, và khớp tỷ lệ dự đoán từ số span. Nếu (b): tỷ lệ ở mốc thật cao hơn hẳn mốc giả. Nếu (c): tỷ lệ ở mốc giả đã cao và đổi theo vị trí mốc.
- **Phạm vi, chi phí.** RE2-TT 26 ca; Nezha-OB không làm được (nền 41–97 giây). Khoảng 20 phút EC2.
- **Quyết định phụ thuộc.** Tiêu chí "trace bất thường" của tầng ánh xạ ở P6: theo từng span hay theo cả yêu cầu.

## KT-2. Tỷ lệ cờ 2–9% ở thao tác đông span: nền tự nhiên hay do sự cố

**Kết quả phiên 13 (KQ13 mục 2; `runs/fake-marker-001/summary.json → /summary/kt2`; `derived-013.json → /kt2`).**

- 1.021 cặp (thao tác đông span, ca): a/n ở mốc giả có trung vị 1,0%, lớn nhất 8,1%; từ 2% trở lên ở 230 cặp. Hai mốc khai trước đều không đạt (230/1.021 và 492/1.021): "không phân xử rõ", hai giải thích cùng có mặt.
- Tách theo vị trí so với root: thao tác phía trên root 0,8% → 6,2% (161/236 cặp tăng gấp từ 2 lần); thao tác không liên hệ 1,1% → 1,2%.
- Chín cặp đã đọc ở TraceRCA: mốc giả trung vị 1,9%; 4/9 giữ mức tự nhiên, 5/9 tăng sau mốc thật (rõ nhất: đăng nhập của `ts-auth-service`, 0,9–1,9% lên 9–10%).
- **Trả lời:** mức 1–4% ở thao tác đông span không liên hệ là mức tự nhiên của dữ liệu; sự cố làm tăng có chọn lọc theo chuỗi gọi phía trên root. Một số thao tác không liên hệ tăng thật: thuộc KT-6.

Phần dưới đây là mục như đã viết trước khi chạy, giữ để đối chiếu.

- **Đã có.** Ở hai ca TraceRCA sai do khối lượng đã đọc ở RE2-TT, thực thể không liên hệ trên root có 2–9% span mang cờ trên 450–1.066 span, còn root có 15–24% trên 39–46 span (`doc-tay.md` mục 1.2, 1.3). Đổi công thức sang tỷ lệ làm mất 11/15 và 43–46/75 cặp (`ket-qua-phien-11.md` mục 8).
- **Giải thích cạnh tranh.** (a) Phân phối thời lượng có đuôi dài nên 2–9% span vượt mean + 3·std ngay cả khi bình thường. (b) Lỗi (nhất là mất gói) làm chậm cả thao tác không nằm trên chuỗi gọi qua root.
- **Phép kiểm.** Với mốc giả lùi 150 giây ở RE2-TT, đếm a/n theo thao tác; so với a/n sau mốc thật, tách theo vị trí của thao tác so với root.
- **Giữ cố định:** luật cờ, thao tác. **Chỉ đổi:** mốc.
- **Dự đoán phân biệt.** (a): a/n ở mốc giả cũng cỡ 2–9%. (b): a/n ở mốc giả dưới 1%, sau mốc thật tăng lên.
- **Phạm vi, chi phí.** RE2-TT 26 ca; khoảng 15 phút EC2 (dùng lại script phép thử giả của bảng A).
- **Quyết định phụ thuộc.** Nếu (a): mọi cách chấm theo số span cần ngưỡng hiệu chỉnh theo từng thao tác; nếu (b): cần thông tin tài nguyên chung (xem KT-6).

## KT-3. MicroRank: phần còn lại sau khi thay bộ chia — đã chạy trong phiên 12

**Kết quả (`ket-qua-phien-12.md` mục 1; `runs/microrank-kt3-001/collect-001/summary.json`).** Nhánh giữ nguyên khớp bản đóng băng 52/52; chỗ móc đếm riêng trùng M-C1 của phiên 9 ở 48/48 ca.

- Ghép bộ chia theo bài gốc với đếm riêng: số ca hạng 1 từ 21 lên 23 (luật của bài) và từ 22 lên 27 (luật của code) trên 47 ca. Mốc khai trước (hơn từ 4 ca ở ít nhất một luật, số ca tụt ít hơn số ca tăng) đạt ở luật của code, không đạt ở luật của bài.
- RE2-TT: 14 → 17 và 15 → 19 trên 25 ca, không ca đang đúng nào hỏng. Nezha-OB: 7 → 6 và 7 → 8 trên 22 ca, 5–7 ca tụt hạng.
- **Trả lời:** giải thích (a) được hỗ trợ một phần, rõ ở RE2-TT. Còn 20–24/47 ca chưa giải thích.
- **Bảng nối phiên 13** (KQ13 mục 5; runs/microrank-merged-link-001/summary.json). Hai tập trace khớp 47/47 ca theo hai luật. frontend đứng đầu 14/16 và 11/14 ca Nezha còn sai, gắn root ở 3/14 và 3/11; dự đoán H4, H7 không đạt. Có 5/8,3/6 ca RE2 và 5/16,5/14 ca Nezha gắn root; 3 ca RE2,6/4 ca Nezha vắng root trong tập trace tạo số đếm của thao tác đứng đầu; 4/3 ca Nezha ít span. dev-14701a3bbb chưa rõ dưới cả hai luật. dev-607751ac0a luật code không gắn nhưng root có trong 2/6 trace xét. Các dạng này chưa là phân loại nguyên nhân đầy đủ; giữ giải thích(b),(c) chưa kiểm riêng.

Phần dưới đây là mục như đã viết trước khi chạy, giữ để đối chiếu.

- **Đã thử và kết quả.** Bốn phép đổi đúng một bước, đủ 48 ca: bỏ trọng số (Hit@1 2 → 11), đếm riêng (2 → 19), cờ theo phần chưa phủ (2 → 4), bộ chia theo bài gốc với hai luật (2/47 → 21 và 22). Còn 25–26/47 ca root chưa hạng 1. Đọc tay cho bốn dạng trong phần còn lại (`doc-tay.md` mục 2.2–2.4): root `ts-train-service` bị bộ chia mới đẩy xuống (`dev-3ae0a6c15a`: 3 → 5); một dịch vụ không liên hệ khác lên đầu (`dev-12a1a88069`, `dev-1e6d61b5ec`: `ts-auth-service`); tín hiệu ở span phía gọi (`dev-14701a3bbb` và 5 đơn vị cùng đường đi); một ca mất span (`dev-746fd74313`, bộ chia mới không áp được).
- **Giải thích cạnh tranh.** (a) Sau khi chia đúng, bước đếm phủ và trọng số vẫn ưu tiên thao tác có mặt ở nhiều trace. (b) Quy ước span đầu của ta sai ở RE2-TT (span đầu thuộc 13 dịch vụ), nên "thời gian cả yêu cầu" không so được giữa các loại yêu cầu. (c) Mức nền học trên 348–1.566 trace quá ngắn.
- **Phép kiểm.** Chạy đồng thời hai phép đổi đã có (bộ chia theo bài gốc + đếm riêng), mọi thứ khác giữ nguyên. Thêm: tách kết quả theo dịch vụ của span đầu.
- **Dự đoán phân biệt.** (a): Hit@1 của nhánh ghép cao hơn hẳn 21–22. (b): các ca còn sai tập trung ở vài dịch vụ span đầu. (c): không phép nào đổi; cần dữ liệu nền dài hơn, tức không kiểm được trên dataset này.
- **Phạm vi, chi phí.** 47 ca; khoảng 15 phút máy laptop, cần 3 GB RAM trống (laptop là nơi MicroRank tái lập từng bit). **Bằng chứng còn thiếu:** kết quả của nhánh ghép; tỷ lệ theo dịch vụ span đầu.
- **Quyết định phụ thuộc.** Có lấy cách xếp hạng kiểu MicroRank (PageRank làm trọng số cho spectrum) làm ứng viên tầng 4 của P6 hay không.

## KT-4. 40 cặp "chung phía trên" của TraceRCA ở Nezha-OB — đã trả lời phần lớn

- **Câu hỏi cũ** (`ket-qua-phien-11.md` mục 2.1): 40/75 cặp ở Nezha-OB là thực thể có chung dịch vụ phía trên với root; chưa có giải thích.
- **Phiên 12 đã làm.** Đếm lại theo lớp từ bảng tự động (`runs/tong-hop-phien-12-001/tracerca-cap-theo-lop.json` → `/theo_dataset/Nezha-OB/chung_phia_tren`): 40 cặp; ở 36/40 số span mang cờ của thực thể lớn hơn của root; trung vị tỷ lệ a/n là 3,4%; ở 24/40 tỷ lệ thấp hơn root. Xếp theo tỷ lệ còn 15/40 cặp; xếp theo số tuyệt đối còn 36/40; T-D còn 36/40. Đọc tay (`doc-tay.md` mục 1.4 đường 3, 4, 6, 7): đó là `currencyservice`, `cartservice`, `productcatalogservice` với 2–4% span mang cờ trên 874–3.869 span.
- **Trả lời.** Phần lớn nhóm này (25/40 cặp mất khi xếp theo tỷ lệ) là thao tác đông span thắng nhờ số tuyệt đối, cùng cơ chế với dòng "khối lượng lấn át". 15 cặp còn lại là các ca root gần như không có span mang cờ (lỗi `return`, `exception`, trễ mạng).
- **Còn mở:** vì sao các thao tác đó có 2–4% span mang cờ ở Nezha-OB: không kiểm được bằng mốc giả vì nền quá ngắn. Ở RE2-TT, KT-2 (phiên 13) cho thấy mức 1–4% ở thao tác đông span không liên hệ là mức tự nhiên; đây là căn cứ gián tiếp, không phải phép đo trên Nezha-OB.

## KT-5. Gắn tín hiệu của span phía gọi cho dịch vụ được gọi

- **Vì sao nêu.** Bảng A: root đứng đầu theo span phía gọi của lời gọi tới nó ở 18–19/20 ca RE2-TT và 11–13/20 ca Nezha-OB, trong khi theo cờ thời lượng mà hai phương pháp trace dùng chỉ 8/26 và 9/22 (`ket-qua-phien-10.md` mục 3). Đọc tay: với lỗi trễ mạng, không phép đổi nào trên điểm của nút cứu được root (`doc-tay.md` mục 1.4 đường 7, 1.7). Bước xét hướng lan có sẵn trong bài TraceRCA, cài theo lời văn, không tách được vì lấy trị tuyệt đối (`ket-qua-phien-11.md` mục 9).
- **Đây là ứng viên cho P5–P6, chưa kiểm.** T-032 không đánh giá phương pháp mới (mục "Không làm" của SPEC). Con số 18–19/20 là mô tả nơi có thông tin, không phải độ chính xác dự kiến.
- **Phép kiểm khi sang P6.** Trên dev: điểm của dịch vụ X = hàm của (tỷ lệ lời gọi **đi vào** X có span phía gọi vượt nền) và (tỷ lệ lời gọi **đi ra** từ X vượt nền), giữ dấu. So với ba đối chứng: cùng điểm nhưng gắn theo dịch vụ sở hữu span (như hiện nay); đồ thị bỏ cạnh; đồ thị ngẫu nhiên giữ bậc.
- **Điều kiện thất bại biết trước.** 15/52 ca thiếu lời gọi tới root, 8 ca không có cạnh đi vào; không đồng nghĩa mọi quan hệ đồ thị đều vô ích. Return/exception có root không hạng 1 và ít cờ ở một số ca; đáp ứng thời lượng do lỗi còn OPEN. Lời gọi song song hoặc bất đồng bộ có thể khác điều kiện dev (chưa thấy ở dev, có thể có ở FlashTicket).
- **Chi phí.** Khoảng 0,5–1 phiên, thuộc task P5–P6.
- **Quyết định phụ thuộc.** Cơ chế chấm điểm ở tầng 1–2 của P6; kiểu cạnh cần có trong mô hình đồ thị P5.

## KT-6. Cột metric của dịch vụ không liên hệ đổi tại mốc — không phân xử được bằng dữ liệu hiện có

- **Đã thử.** Bảng cột thắng theo vị trí, nhóm xu hướng và lưu lượng (`ket-qua-phien-11.md` mục 3): theo góc nhìn BARO, 59 thực thể không liên hệ và 118 thực thể không có span có cột thắng đổi tại mốc; lưu lượng đổi ở 19/100 thực thể có span. Đọc tay: ở `dev-a5cabe5fa7`, bốn dịch vụ không có span có cột cpu tăng 327–402% đúng lúc sự cố (`doc-tay.md` mục 3.2).
- **Giải thích cạnh tranh.** Tài nguyên chung của máy; tải chung; tác dụng phụ của công cụ tiêm lỗi; lan theo quan hệ không thấy trong trace.
- **Vì sao không phân xử được.** RE2-TT không công bố dịch vụ nào chạy trên máy nào, không có metric mức máy, không có nhật ký của công cụ tiêm lỗi. Đã tìm trong bài và kho RCAEval (`ket-qua-phien-10.md` mục 6.1): không có.
- **Bằng chứng cần.** Quan hệ dịch vụ–máy; metric mức máy; thời điểm và đối tượng tiêm lỗi.
- **Hệ quả.** Yêu cầu quan sát cho FlashTicket (P9a): ghi quan hệ triển khai và metric mức máy, để tách "cùng máy" khỏi "cùng chuỗi gọi". Với dataset công khai: giữ là giới hạn; 82/103 cặp sai của BARO ở RE2-TT nằm trong vùng này.

## KT-7. TORAI với bảng của tác giả: nguồn độ trễ trace

- **Đã có.** Ở nguồn A, nguồn nghiêng nhiều nhất về thực thể trên root là độ trễ trace (13/22 cặp); root đứng đầu theo nguồn này ở 10/30 ca, so với 22/30 ở nguồn B (`ket-qua-phien-11.md` mục 6).
- **Giải thích cạnh tranh.** Bảng trace của tác giả dựng với cửa sổ khác; cách gộp theo thao tác khác; hoặc cùng cơ chế "span phía gọi tính cho dịch vụ gọi".
- **Phép kiểm.** Lập cho nguồn A cùng bảng "cột cao nhất theo dịch vụ" đã lập cho log, áp cho nguồn độ trễ trace; xem cột cao nhất của thực thể trên root có phải thao tác phía gọi của lời gọi tới root.
- **Chi phí.** Khoảng 15 phút EC2. **Quyết định phụ thuộc:** không có quyết định P5–P6 nào; nguồn A nằm ngoài cấu hình chính. Ưu tiên thấp.

## KT-8. Bốn ca ERROR của MicroRank và TraceRCA — nửa MicroRank đã chạy trong phiên 12

**Kết quả nửa MicroRank (`ket-qua-phien-12.md` mục 2).** Ở 48 ca không có thao tác mới, nhánh bỏ thao tác khớp bản đóng băng từng bit 48/48. Ở 4 ca lỗi: bỏ 210–527 span của một thao tác (ở 71–195 trace) thì phương pháp chạy được; root hạng 2, 2, 3, 12; `ts-station-service` đứng đầu ở 4/4. Ở hạng 1 cách ghi nào cũng cho 0/4; ở 5 hạng đầu 3/4 ca đang bị tính trượt. 

**Kết quả nửa TraceRCA, phiên 13 (KQ13 mục 4; `runs/tracerca-dropnew-001/summary.json`).** Tự kiểm: ở 48 ca nguồn OK không span nào bị bỏ và hạng mọi thực thể trùng bản đóng băng 48/48. Bốn ca lỗi sau khi bỏ cùng số span như nửa MicroRank: root hạng **2, 1, 1, 1**. Vậy với TraceRCA cách ghi có đổi con số: 3/4 ca đang tính trượt sẽ là hạng 1. Quyết định còn lại cho Minh: ghi ở bảng G2 thế nào (báo cáo chính mục 11).

Phần dưới đây là mục như đã viết trước khi chạy, giữ để đối chiếu.

- **Đã có.** Cả 8 đơn vị dừng vì thao tác `ts-order-other-service_getMore ts.orders` có ở đoạn sau mốc mà không có ở đoạn nền (`doc-tay.md` mục 1.1, 2.1). Bộ chia theo bài gốc cũng ERROR ở 4 ca này. Bảng C2 tính được cho cả 4 ca từ file trace gốc; lời gọi tới root chậm ở phần lớn lời gọi.
- **Giải thích cạnh tranh về cách ghi.** (a) Lỗi của adapter: nên bỏ thao tác thiếu nền. (b) Hạn chế của phương pháp: không xử lý thao tác mới.
- **Phép kiểm.** Lớp bọc bỏ các span của thao tác không có ở nền trước khi gọi phương pháp, mã phương pháp giữ nguyên; chạy 4 ca cho hai phương pháp.
- **Vì sao chưa làm.** Đây là đổi đầu vào đã khóa của giao thức P3 (WHY-31), không phải phép đổi một bước của phương pháp. Cần Minh quyết.
- **Chi phí.** Khoảng 10 phút EC2 (TraceRCA) và 15 phút laptop (MicroRank).
- **Quyết định phụ thuộc.** Ở bảng G2, 4 ca này tính là "phương pháp trượt" (như hiện nay) hay "không chạy được vì đầu vào".

## KT-9. CIRCA: hồi quy theo nút cha làm tăng điểm

**Kết quả phiên 13 (KQ13 mục 6; `runs/circa-kt9-001/collect-001/summary.json`).** Nhánh chẩn đoán; cửa sổ đã khóa và số đã chấm không đổi. Nhánh giữ nguyên khớp bản đóng băng từng bit 30/30.

- Trung vị tỷ số điểm (có cạnh / không cạnh) ở nút từ 8 cha: 7,54 (native) → 3,40 (học 291 điểm) và 3,64 (chấm 10 điểm ngay sau mốc). Tỷ lệ nút tăng: 72,6% → 67,3% và 73,1%.
- Hai vế mốc khai trước cần cùng đạt; vế tỷ số đạt, vế tỷ lệ nút tăng không đạt ở cả hai nhánh. Cả (a),(b) không đạt trọn. Hai nhánh cho trung vị nhóm nhiều cha thấp hơn, còn đa số nút tăng điểm; chưa tách riêng ảnh hưởng số điểm học, phân phối, thời điểm chấm và tập nút.
- Ghi thêm: học trên 291 điểm chỉ bỏ được giá trị cực lớn ở 2/11 ca; ba ca root `ts-auth-service` có hạng sau DA 15 → 1, 22 → 6, 46 → 37.
- **Còn mở:** phần tăng còn lại, có ở mọi cấu hình cửa sổ và tăng theo số nút cha; chưa có phép đổi riêng.

Phần dưới đây là mục như đã viết trước khi chạy, giữ để đối chiếu. Lý do "1–2 giờ máy" nêu ở dưới là ước sai; lượt thật hết 985 giây.

- **Đã có.** Hồi quy làm tăng điểm ở 3.285/4.526 nút; tỷ số tăng theo số nút cha (1,05 với 1 cha tới 8,43 với từ 8 cha) (`ket-qua-phien-10.md` mục 1.4). Phần tăng chủ yếu từ cạnh cùng dịch vụ (mục 7).
- **Giải thích cạnh tranh.** (a) Quá khớp: 111 điểm train, nhiều nút cha. (b) Đoạn chấm là 10 điểm cuối cửa sổ, xa đoạn train.
- **Phép kiểm.** Đổi độ dài đoạn train và vị trí đoạn chấm.
- **Vì sao không làm trong T-032.** Phải đổi cửa sổ đã khóa của giao thức (Q-80, Q-82). Đề xuất tách thành câu hỏi của P6 nếu Minh chọn "hồi quy có điều kiện trên nút cha" làm ứng viên.
- **Chi phí.** 1–2 giờ máy laptop (CIRCA chỉ tái lập từng bit trên laptop).

## KT-10. "Lan có đáng kể" và điều kiện định nghĩa nhãn lan

- **T-032 cung cấp gì** (bảng dùng trực tiếp cho tổng hợp G2: `phan-xu-caller-root.json`, `doi-chieu-dung-sai.json`).
  - Số đơn vị có cờ M5 nguồn: 82 (80 ca × phương pháp), trên 192 đơn vị sai hoặc không OK.
  - Số cặp nằm phía trên root trên tổng số cặp đứng trên root: MicroRank 24/252, TraceRCA 24/90, SimpleRCA 15/64, BARO 15/162, CIRCA 25/110 (`ket-qua-phien-11.md` mục 1).
  - Số cặp có bằng chứng tính toán "chấm thời gian chờ root": TraceRCA 4/4 và 9/15 ở cặp xét được; MicroRank 0/10 và 4/16.
- **T-032 không cung cấp:** nhãn lan theo ca; ngưỡng "đáng kể". SPEC cấm định nghĩa nhãn trong task này.
- **Điều kiện nếu sau G2 định nghĩa nhãn** (theo SPEC): bằng chứng chờ, đồng hồ, độ phủ; đoạn nền phù hợp; cách kiểm ngưỡng. Từ T-032: chỉ 16 ca Nezha-OB đạt mức "đo được"; 21 ca RE2-TT "đo được một phần"; 15 ca không đo được. Nhãn lan định nghĩa trên trace vì vậy chỉ có mẫu số 37 ca, trong đó 21 ca kèm giả định về công cụ ghi span.
- **Ý kiến của người làm, để Minh quyết ở tổng hợp G2:** theo số ở trên, "nhầm triệu chứng với nguyên nhân do chờ" là cơ chế **có thật nhưng không chiếm đa số** các cặp sai ở phương pháp nào trừ CIRCA (nơi nó trộn với giá trị cực lớn). Kế hoạch nghiên cứu ghi: không đáng kể thì không tách nhãn.

## KT-11. Mã của tác giả TraceRCA

- **Đã thử.** Đọc toàn văn bài; cài bước xếp hạng theo lời văn (một đặc trưng); xem trang kho mã `NetManAIOps/TraceRCA`. Chưa chạy mã: kho nhận định dạng dữ liệu riêng (`results/T-015/tracerca-rcaeval.md` mục 9).
- **Bằng chứng còn thiếu.** Kết quả của mã tác giả với đủ đặc trưng (độ trễ, mã trạng thái, metric tài nguyên).
- **Phép kiểm.** Dựng bộ chuyển từ bảng span sang định dạng của kho; chạy trên 52 ca dev.
- **Điều kiện thất bại biết trước.** RE2-TT không có mã trạng thái (rỗng toàn bộ); Nezha-OB không có trường đó; nền của bài là nhiều ngày.
- **Chi phí.** 0,5–1 phiên. **Quyết định phụ thuộc:** mức chắc của câu "phương án dùng cạnh có sẵn trong tài liệu không đủ"; hiện câu đó chỉ đúng cho bản cài theo lời văn.

## KT-12. Cột độ trễ của root phản ứng ở ca này, không ở ca kia cùng ô

**Kết quả phiên 13 (KQ13 mục 3; `runs/root-latency-001/summary.json`).** Bảy ca, bản ghi khớp bản đóng băng BARO từng bit 7/7.

- auth, delay: cột latency của root tăng ở cả ba ca (trung vị gấp 3,9; 1,8; 2,3 lần); z khác nhau (30,7; 4,9; 2,4) vì IQR nền khác nhau 10–23 lần. Không giải thích nào trong ba giải thích khai trước mô tả đúng.
- recommendationservice, network_delay: lời gọi tới root chậm 97–98% ở cả hai ca, 0% nằm trong span của root; cột độ trễ của root không ghi được sự cố ở cả hai; z = 64 đến từ một mẫu P99. Mốc (a) đạt; phần "vì sao có mẫu đó" để mở.
- checkoutservice, network_delay: mốc (c) đạt theo chữ (26% so với 9%), nhưng chuỗi cho thấy không ca nào phản ứng; z = 94 là do IQR của 5 mẫu nền bằng 0,005.
- **Trả lời cho quyết định phụ thuộc:** các ca này thuộc "cách chuẩn hóa theo nền" (cặp 1, 3) và "cột đo ở phía được gọi" (cặp 2), không thuộc "cường độ lỗi khác nhau".

Phần dưới đây là mục như đã viết trước khi chạy, giữ để đối chiếu.

- **Đã có** (`doc-tay.md` mục 3.1 điểm 1, 3.4 điểm 6, 4.3 điểm 4). auth|delay: z của cột latency của root là 30,7 ở `dev-746fd74313`, còn ở `dev-57546fd87b` cột tốt nhất của root chỉ có z = 3,1. recommendationservice|network_delay: z = 64 ở `dev-5467884de4`, cột độ trễ không phải cột tốt nhất ở `dev-63c30faf34`. checkoutservice|network_delay: root 16 phiếu ở một ca, 0 phiếu ở ca kia.
- **Giải thích cạnh tranh.** (a) Cột latency của root đo phía server, lỗi trễ mạng nằm trước đó. (b) Tải thấp nên cột ít mẫu có giá trị. (c) Cùng nhãn lỗi nhưng cường độ thật khác nhau giữa các lần tiêm.
- **Phép kiểm.** In chuỗi 300 mẫu (RE2-TT) hoặc 10 mẫu (Nezha-OB) của các cột độ trễ của root ở ba cặp ca; đối chiếu với số lời gọi tới root và tỷ lệ lời gọi chậm (bảng C2).
- **Dự đoán phân biệt.** (a): cột server của root phẳng ở cả hai ca, cột phía gọi của dịch vụ gọi tăng. (b): số mẫu khác 0 khác nhau. (c): tỷ lệ lời gọi chậm khác nhau rõ (đã thấy ở checkoutservice: 9% so với 26%).
- **Chi phí.** Khoảng 10 phút EC2, chỉ đọc. **Quyết định phụ thuộc:** các ca này xếp vào "lỗi không hiện ở kênh metric" (dữ liệu) hay "cột đo sai chỗ" (yêu cầu quan sát).

## KT-13. Phần chậm nằm ngoài span của root — không phân xử được bằng dữ liệu hiện có

- **Đã có.** Trong lời gọi chậm tới root, phần vượt nằm **trong** span của root chiếm từ 0,5% (trễ mạng ở Nezha-OB) tới 97% (lỗi delay ở RE2-TT); phần còn lại nằm ngoài (`ket-qua-phien-10.md` mục 6.4). T-D không gỡ được cặp `ts-seat-service` trên root ở `dev-12a1a88069` dù 98% span mang cờ là span chờ root (`doc-tay.md` mục 1.2).
- **Giải thích cạnh tranh.** Đường truyền; hàng đợi trước khi dịch vụ được gọi bắt đầu xử lý; xử lý ở phía gọi quanh lời gọi; lệch đồng hồ.
- **Vì sao không phân xử được.** Mỗi lời gọi chỉ có hai span; không có mốc "yêu cầu tới" ở phía được gọi; đồng hồ hai máy không được công bố độ đồng bộ.
- **Hệ quả.** Yêu cầu quan sát cho FlashTicket: thêm mốc thời gian lúc yêu cầu tới ở phía được gọi; đồng bộ đồng hồ dưới mili giây hoặc không dựa vào hiệu thời điểm giữa hai máy.

## KT-14. Đọc tay đủ 192 đơn vị sai

**Đã làm ở phiên 13 (`doc-tay.md` mục 8; KQ13 mục 7).** Đọc nốt 68 đơn vị OK xếp sai; 48 đơn vị không chạy được ghi theo lý do sau khi soát dòng lý do của cả 48 phiếu. Tổng: 144 đơn vị sai hoặc không OK đã đọc, 24 đối chứng. Không thấy đường thất bại mới; có sáu điều chỉnh so với phần đọc của phiên 12 (KQ13 mục 7). Chữ dưới đây là mục viết trước khi làm.

- **Đã làm.** 76 đơn vị sai hoặc không OK và 24 đối chứng đúng, theo quy tắc "mỗi đường đi một đơn vị" (74 đơn vị sai được chọn theo đường đi; 2 đơn vị sai ở hạng 1 được đọc với vai trò đối chứng ở k = 5). 116 đơn vị sai còn lại chỉ có trong bảng tự động (42 trong số đó là UNSUPPORTED cùng một lý do theo từng phương pháp, và 6 là ERROR cùng lý do).
- **Vì sao chưa làm đủ.** Gói đã duyệt chọn mức đọc này (phần B của gói bổ sung 007).
- **Nếu làm:** khoảng một phiên; phiếu đọc sinh bằng `scripts/tong_hop_v1.py` cho mọi đơn vị. **Lợi ích dự kiến:** tìm thêm phản ví dụ trong các đường đi đông (9 đơn vị MicroRank, 8 đơn vị MicroRank Nezha-OB, 7 đơn vị CIRCA).

## KT-15. Bước DA và dịch vụ không có cạnh — đã chạy trong phiên 12

**Kết quả (thiết kế `thiet-ke-phep-doi-012.md` mục 3; `runs/circa-da-addition-001/summary.json`; chỉ đọc trung gian, không chạy phương pháp).**

- Tự kiểm: khóa sau DA bằng điểm trước DA cộng phần được cộng ở 1.574/1.574 nút; nút không được cộng giữ nguyên ở 7.031/7.031; phần được cộng bằng đúng điểm lớn nhất của các nút con với tới ở 1.574/1.574.
- **Cách đọc ban đầu "DA bất lợi cho dịch vụ không có cạnh" sai về cơ chế.** Root `ts-auth-service` có 5 hậu duệ trong đồ thị metric và cũng được cộng (405,65; 29,85; 1,42 ở ba ca).
- Ở ba ca DA làm root tụt hạng không dính giá trị cực lớn, các thực thể vượt root sau DA nhận **cùng một giá trị từ một nút nguồn**: 13/13 thực thể (2.027,36 từ `ts-preserve-service_latency`), 11/12 (61,71 từ cùng nút đó), 4/7 (68,77 từ `ts-preserve-other-service_latency`).
- Hai mốc khai trước, trên 19 ca không có nút cực lớn: (b) "hơn nửa số nút được cộng nhận cùng một giá trị ở từ 2/3 số ca" **không đạt** (0/19 ca; tỷ lệ nút nhận giá trị phổ biến nhất có trung vị 15%, lớn nhất 35%); (a) tương quan hạng giữa số hậu duệ và phần được cộng dương ở 16/19 ca nhưng yếu (trung vị 0,21). Tức xét trên mọi nút, không giải thích nào trong hai giải thích khai trước mô tả đúng; phần được cộng đến từ nhiều nút nguồn.
- **Kết luận dùng được:** DA cộng cho mỗi nút điểm lớn nhất của nút con; khi một nút của dịch vụ không liên quan có điểm cao nhất bảng, mọi nút cha của nó được nâng cùng một lượng và có thể vượt root. Cùng kiểu với H14, khác ở chỗ điểm nguồn là thay đổi thật chứ không phải lỗi số học. Dịch vụ nguồn hay gặp nhất: `ts-preserve-service` (9/19 ca).
- **Còn mở, đã thu hẹp ở phiên 13:** vì sao cột độ trễ của `ts-preserve-service` có điểm cao ở các ca root là `ts-auth-service`. KT-9 cho thấy điểm đó phụ thuộc độ dài đoạn học: học trên 291 điểm thay cho 111 thì hạng root sau DA ở ba ca là 1, 6, 37 (thay cho 15, 22, 46). Vậy câu "điểm nguồn là thay đổi thật" ở trên viết quá tay; đúng hơn: điểm đó lớn dưới đoạn học 111 điểm. Phần còn lại thuộc KT-6.

Phần dưới đây là mục như đã viết trước khi chạy, giữ để đối chiếu.

- **Đã có.** Ba ca DA làm root tụt hạng mà không dính giá trị cực lớn đều có root `ts-auth-service`: hạng 2 → 15, 40 → 46, 10 → 22. Khi bỏ mọi cạnh: hạng 1, 34, 22 (`doc-tay.md` mục 5.3; bảng CIRCA trong `doi-chieu-dung-sai.json`). Chỉ ca đầu là ca root gần đứng đầu; hai ca sau root đã ở xa vì thiếu tín hiệu metric.
- **Giải thích cạnh tranh.** (a) DA có thiên lệch cấu trúc: nút có hậu duệ được cộng thêm. (b) Trùng hợp trên 3 ca cùng một dịch vụ.
- **Phép kiểm.** Trên 19 ca không có nút cực lớn: so tổng điểm DA cộng thêm cho mỗi dịch vụ với số hậu duệ của nó trong đồ thị metric (trung gian đã lưu ở lượt quan sát CIRCA).
- **Dự đoán phân biệt.** (a): phần cộng thêm tăng theo số hậu duệ, độc lập với ca. (b): không có quan hệ.
- **Chi phí.** Khoảng 10 phút laptop, chỉ đọc trung gian. **Quyết định phụ thuộc:** nếu P6 có bước lan điểm theo đồ thị, phải có cách xử lý nút không có cạnh (kế hoạch P6 tầng 4 đã nêu yêu cầu này).

## KT-16. Tập test

- Mọi con số của T-032 là trên 52 ca dev. Nhiều bảng và phép đổi được đặt sau khi đã xem kết quả dev (ghi ở từng mục của ba file kết quả). Chưa ca test nào được mở. Mở test là quyết định của Minh ở G3; T-032 không đề nghị mở.
