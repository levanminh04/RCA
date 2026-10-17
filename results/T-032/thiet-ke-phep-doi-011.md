# T-032 — Thiết kế bản 011: hai phép kiểm ngoài gói cho TraceRCA (Minh duyệt trong chat ngày 11/10/2026)

Viết ngày 11/10/2026, trước khi chạy. Người viết: Claude. Lời Minh: "duyệt Hai phép kiểm ngoài gói". Hai phép này tôi đề xuất ở cuối lượt trước, sau khi đã xem `ket-qua-phien-11.md` mục 2.1 và mục 5; vì vậy kết quả chỉ là bằng chứng trên dev cho một ứng viên, không phải kiểm định độc lập.

## 1. Điều tôi đã thấy trước khi viết

- Ở RE2-TT, 12/15 thực thể đứng trên root của TraceRCA có tỷ lệ span mang cờ a/n thấp hơn root nhưng số span mang cờ a lớn hơn; ở Nezha-OB 39/75. Ở 3/5 và 5/18 ca sai, root có tỷ lệ cao hơn mọi thực thể đứng trên nó (`runs/tracerca-ratio-vs-count-001/summary.json`).
- Ở các cặp xét được, 4/4 cặp phía trên của RE2-TT và 9/15 của Nezha-OB có span mang cờ chủ yếu là span chờ root.
- Bài TraceRCA gốc xếp hạng bằng chỉ số Jaccard của tập dịch vụ nhân với hiệu số trace có lời gọi bất thường đi vào và đi ra (mục 5 của `ket-qua-phien-11.md`).

## 2. Phép T-R — đổi công thức điểm của bản thư viện sang tỷ lệ

**Câu hỏi:** công thức điểm 2a/(n + H) có phải là bước làm root mất hạng không, hay chỉ là quan sát đi kèm.

**Giữ nguyên:** bảng span, cờ từng span (đúng luật của bản thư viện), tập thao tác ứng viên (thao tác có ít nhất một span mang cờ), phép lấy điểm lớn nhất theo dịch vụ, cách xếp hạng và xử lý hòa. Số a, n, H lấy từ lượt `chain-spanpass-001` (tổng cờ đã khớp `H_native` 48/48 ca).

**Bước duy nhất bị đổi:** điểm của thao tác.

| Nhánh | Điểm của thao tác | Ghi chú |
|---|---|---|
| `sham` | 2a/(n + H) | hạng của mọi dịch vụ phải trùng bản ghi đóng băng ở mọi ca OK |
| `tr1` | a/n | tỷ lệ span của thao tác vượt nền |
| `tr1m` | a/n, chỉ với thao tác có n ≥ 20 | tránh thao tác chỉ có vài span; mốc 20 trùng mốc số lời gọi đã dùng ở bảng C2 |
| `ts` | a | số span mang cờ tuyệt đối; để đo công thức gốc gần với thứ tự theo a tới đâu |

**Dự đoán khai trước.**

- Nếu công thức điểm là bước làm root mất hạng: dưới `tr1` hoặc `tr1m`, root lên hạng 1 ở phần lớn ca sai mà hiện root có tỷ lệ cao nhất trong nhóm (3 ca RE2-TT, 5 ca Nezha-OB), và không làm hỏng các ca đang đúng.
- Nếu không: root không lên, hoặc lên ở vài ca nhưng nhiều ca đúng thành sai (vì thao tác ít span có tỷ lệ cao do ngẫu nhiên). Khi đó "tỷ lệ" không phải cách chữa, và hạn chế phải ghi là "công thức không tách được tỷ lệ với khối lượng", không phải "sai công thức".
- `ts`: nếu thực thể đứng đầu theo a trùng thực thể đứng đầu theo công thức gốc ở phần lớn ca thì câu "thứ tự gần như theo số tuyệt đối" được xác nhận.

**Báo:** theo dataset: root tăng, không đổi, giảm hạng (theo hạng tốt nhất); Hit@1, Hit@5 tính bi quan khi hòa; số cặp (thực thể đứng trên root, root) còn, mất, mới; số ca thực thể đứng đầu trùng công thức gốc. Mẫu số: 47 ca root được xếp ở bản gốc; ca khác đếm riêng.

**Giới hạn:** `tr1`, `tr1m` không phải đề xuất phương pháp; chúng chỉ cho biết bước nào làm đổi hạng trên dev.

## 3. Phép T-O — bước xếp hạng của bài TraceRCA gốc, do ta cài theo lời văn của bài

**Tên gọi trong mọi kết quả:** "bước xếp hạng của bài TraceRCA gốc, cài theo lời văn của bài trên dữ liệu của ta". Không phải mã của tác giả và không tái lập bài gốc.

**Câu hỏi:** bước "hiệu số lời gọi bất thường đi vào và đi ra" của bài gốc có tách được root khỏi dịch vụ gọi nó ở các ca dev không. Câu này quyết định bước đó có đáng là một ứng viên dùng cạnh gọi có hướng cho P5–P6 hay không.

**Cài đặt, theo Mục III của bài; chỗ nào bài không quyết thì ghi là lựa chọn của người làm.**

1. **Lời gọi:** cặp (span phía gọi, span con trực tiếp thuộc dịch vụ khác) cùng trace, như bảng C2. Cặp dịch vụ = (dịch vụ gọi, dịch vụ được gọi).
2. **Đặc trưng:** chỉ độ trễ. Dữ liệu không có mã trạng thái (trống ở RE2-TT, không có ở Nezha-OB); bài còn dùng metric tài nguyên của dịch vụ, ở đây không đưa vào. *Lựa chọn của người làm:* độ trễ của lời gọi là thời lượng span phía gọi (nhánh chính `to_p`); thêm nhánh `to_c` dùng thời lượng span phía được gọi để xem độ nhạy.
3. **Nền:** trung bình và độ lệch chuẩn theo từng cặp dịch vụ trên các lời gọi kết thúc trước mốc. Bài dùng thêm dữ liệu cùng khung giờ của ngày trước; dữ liệu của ta không có.
4. **Chọn đặc trưng (bài: ngưỡng 10%):** độ lệch trung bình sau mốc phải lớn hơn độ lệch trung bình trước mốc hơn 10%. Không đạt thì ghi "không có đặc trưng hữu ích", không xếp hạng.
5. **Lời gọi bất thường:** lệch khỏi trung bình hơn 1 lần độ lệch chuẩn (mặc định của bài). Cặp có dưới 2 lời gọi trước mốc hoặc độ lệch chuẩn bằng 0: không xét, đếm riêng.
6. **Trace bất thường:** có ít nhất một lời gọi bất thường. Chỉ xét trace có lời gọi sau mốc.
7. **Tập dịch vụ:** trace "đi qua" dịch vụ khi dịch vụ là đầu gọi hoặc đầu được gọi của một lời gọi sau mốc trong trace. Support = tỷ lệ trace bất thường đi qua mọi dịch vụ của tập; giữ tập có support ≥ 10%; chỉ số Jaccard = số trace vừa đi qua tập vừa bất thường, chia cho số trace đi qua tập hoặc bất thường; giữ 100 tập có chỉ số cao nhất. *Lựa chọn của người làm:* hòa ở vị trí thứ 100 thì giữ hết các tập hòa; liệt kê tập bằng duyệt đủ trên các tổ hợp dịch vụ đạt support (kết quả như khai phá tập phổ biến, không dùng thư viện ngoài). Nếu số tập vượt 2 triệu ở một ca thì dừng ca đó và ghi "quá lớn".
8. **Điểm trong tập:** với dịch vụ m thuộc tập S, trong các trace đi qua S: trị tuyệt đối của (số trace có lời gọi bất thường đi vào m) trừ (số trace có lời gọi bất thường đi ra từ m).
9. **Điểm dịch vụ:** lớn nhất qua các tập chứa nó của (chỉ số Jaccard × điểm trong tập). Xếp giảm dần; hòa ghi hạng tốt nhất và xấu nhất. Dịch vụ không nằm trong tập nào được giữ: không có điểm, xếp sau cùng và hòa nhau.

**Nhánh thêm `to_p3` (thêm lúc 06:30Z ngày 11/10, sau khi đã thấy kết quả phép T-R, trước khi chạy bất kỳ nhánh T-O nào).** Như `to_p` nhưng lời gọi là bất thường khi lệch quá 3 lần độ lệch chuẩn, tức ngưỡng của bản thư viện. Lý do: với ngưỡng 1 lần độ lệch chuẩn và phép so hai phía, dưới phân phối chuẩn khoảng 32% lời gọi bình thường đã bị gắn cờ, nên gần như mọi trace có thể thành bất thường và bước xếp hạng không còn gì để phân biệt. Nhánh này tách tác dụng của bước xếp hạng khỏi ngưỡng phát hiện. Ba nhánh `to_p`, `to_c`, `to_p3` báo riêng; nhánh theo đúng mặc định của bài là `to_p`.

**Lưu ý đọc từ ví dụ của bài (ghi trước khi chạy):** hiệu số lấy trị tuyệt đối, nên dịch vụ chỉ có lời gọi **đi ra** bất thường (đầu trên của chuỗi) cũng nhận điểm cao như dịch vụ chỉ có lời gọi **đi vào** bất thường (đầu dưới). Trong Hình 2 của bài, dịch vụ được coi là nguyên nhân chính là đầu trên. Vậy bước này tách được dịch vụ **giữa chuỗi**, còn hai đầu chuỗi phải nhờ chỉ số Jaccard của tập phân xử. Dự đoán thêm: dịch vụ đầu vào của hệ (ví dụ `frontend`) sẽ là đối thủ chính của root dưới T-O.

**Kiểm không có bản đóng băng:** ví dụ Hình 2 của bài dựng lại bằng tay (năm trace, ba trace bất thường): tập {A, B} phải có support 1 và điểm trong tập của A là 3, của B là 0. Thêm ba trường hợp tự dựng: root là lá của chuỗi gọi (chỉ có lời gọi vào bất thường); dịch vụ giữa chuỗi có cả lời gọi vào và ra bất thường; không có lời gọi bất thường.

**Dự đoán khai trước.**

- Nếu bước của bài gốc xử lý được hiện tượng "dịch vụ gọi chờ root": ở các ca mà bản thư viện xếp dịch vụ gọi trên root và cặp đó thuộc loại "chủ yếu là chờ root" (3 ca RE2-TT, 8 ca Nezha-OB), root đứng trên dịch vụ gọi đó dưới T-O.
- Nếu không: dịch vụ gọi vẫn đứng trên root, hoặc root không có điểm. Trường hợp dự kiến trước là khó: root gọi tiếp dịch vụ khác và lời gọi đi ra của root cũng bất thường (bài tự nêu giới hạn lan hai chiều); root không được dịch vụ nào gọi (6 ca `ts-auth-service`, 2 ca `frontend`) thì không có lời gọi đi vào.
- Không so Hit@1 của T-O với các phương pháp khác như một bảng xếp hạng phương pháp: T-O chỉ dùng một đặc trưng và nền ngắn. Báo Hit@1, Hit@5 để biết hướng, kèm số ca không xếp được.

**Báo:** theo dataset và theo loại lỗi: số ca xếp được; hạng root; số ca root đứng trên mọi dịch vụ gọi trực tiếp nó; riêng 11 ca "chủ yếu là chờ root" của bản thư viện: root có đứng trên dịch vụ gọi đó không; số ca không có đặc trưng hữu ích; số ca root không có điểm và lý do.

**Giới hạn:** một đặc trưng; nền 300 giây (RE2-TT) hoặc 41–97 giây (Nezha-OB) thay cho nền nhiều ngày; ngưỡng 1 lần độ lệch chuẩn của bài sẽ gắn cờ nhiều lời gọi ngay cả khi không có lỗi; cài theo lời văn, chưa đối chiếu mã của tác giả.

## 4. Đầu ra

- EC2 `~/rca/T-032/runs/tracerca-score-contrast-001/` (T-R), `runs/tracerca-original-ranking-001/` (T-O); file tổng hợp chép về laptop.
- Script: `scripts/tracerca_score_contrast_v1.py`, `scripts/tracerca_original_ranking_v1.py`.
- Diễn giải: `ket-qua-phien-11.md` mục 8 và 9.
