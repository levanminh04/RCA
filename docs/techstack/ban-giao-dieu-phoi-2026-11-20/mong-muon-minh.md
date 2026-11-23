# Mong muốn và quyết định của Minh (phiên 19–20/11/2026)

Nguồn nguyên văn: `lich-su/01-minh-tin-nhan.md`. File này gồm ba phần: 17 tin nhắn trong chat Claude; **tin nhắn Minh gửi Codex lúc 20/11 03:33:57Z**; tin duyệt mới nhất. Bảng dưới tóm theo chủ đề. Câu trong ngoặc kép là nguyên văn. Giờ là UTC.

Mức độ chắc chắn:
- **Trực tiếp:** Minh tự viết, trong chat Claude hoặc trong tin gửi Codex.
- **Đã ghi chính thức:** đã nằm trong `docs/DECISIONS.md` hoặc LOG task.
- **Chờ duyệt:** đề xuất của agent, Minh chưa quyết.

*(Bản đầu của file này xếp nhầm các yêu cầu điều phối vào mức "Codex ghi", vì bỏ sót tin Minh gửi Codex lúc 03:33:57Z. Đã sửa theo lượt soát gói của Codex, `lich-su/12`, và duyệt của Minh, `lich-su/01` phần cuối.)*

## 1. Cách làm việc chung

| Mong muốn | Nguồn | Mức |
|---|---|---|
| Tối ưu thời gian: "tôi muốn tôi ưu thời gian nhất có thể"; "cần tận dụng mọi khoảng thời trống, tránh để thời gian trống vô ích"; "tận dụng thời gian tối đa có thể" | chat 20/11 01:03Z; 19/11 17:46Z; 20/11 03:10Z | Trực tiếp |
| **Tính đúng ưu tiên cao nhất:** "tính đúng đắn vẫn ưu tiên cao nhất" | chat 20/11 03:10Z | Trực tiếp |
| Không đợi đêm: "không cần phải đợi đến đêm, tôi có thời gian, không tự giới hạn bản thân" | chat 20/11 02:01Z | Trực tiếp |
| Song song nhiều phiên, một phiên điều phối, việc phụ thuộc thì tuần tự: "sử dụng tính tăng multi-sessions của claude để làm nhé, 1 phiên điều phối, phần nào cần tuần tự thì tuần tự" | chat 20/11 03:10Z | Trực tiếp |
| **Các phiên không dẫm chân nhau:** "cần claude thiết kế phiên điều phối chuẩn chỉnh, các phiên không dẫm chân nhau" | Codex 20/11 03:33:57Z | Trực tiếp |
| Một plan duy nhất: "cần bạn tổng hợp thông tin thành 1 plan duy nhất để tránh 2 phiên mâu thuật" | chat 20/11 03:10Z | Trực tiếp |
| Xem xét kỹ, không bỏ sót; soi lại plan trước khi tổng hợp với Codex | chat 20/11 01:03Z, 03:10Z | Trực tiếp |
| Codex phản biện plan: tìm lỗ hổng, điểm phụ thuộc, khả năng song song hoàn toàn; "không coi claude đã đúng" | chat 20/11 01:03Z; Codex 03:33:57Z | Trực tiếp |
| **Phiên Claude điều phối mới hoàn toàn, đủ ngữ cảnh:** "tôi muốn sang phiên claude mới hoàn toàn với đầy đủ ngữ cảnh phiên đó sẽ điều phối" | Codex 03:33:57Z; chat 10:03Z ("tôi cần đổi account … cái tôi cần là đủ ngữ cảnh") | Trực tiếp |
| **Mức model:** "phiên điều phối tôi sẽ sử dụng opus 5.5 mức high hoặc xhigh (việc này tôi sẽ chọn khi dán prompt vào phiên mới) các phiên làm việc của claude thì chọn medium hoặc high tùy độ khó của công việc, cần claude tự đánh giá nếu model không tăng hiệu quả hoặc sai liên tục thì báo Minh để xem xét tăng mức cho model"; "việc khó để claude làm" | Codex 03:33:57Z | Trực tiếp |
| **Codex qua terminal làm việc phụ:** "sử dụng codex qua terminal để yêu cầu codex làm những việc phụ, nếu codex hết usage cần báo tôi đổi account, model cho codex sẽ là gpt 6.2 astra mức high" | Codex 03:33:57Z | Trực tiếp |
| **Lịch đánh thức và chống làm lại:** "vì có thể hết usage hoặc mất mạng giữ chừng do tôi phải di chuyển nên cần phiên điều phối có lịch đánh thức phù hợp, đảm bảo dữ liệu và tiến trình không bị làm lại sau khi bị tạm dừng" | Codex 03:33:57Z | Trực tiếp |
| **Không ép hoàn hảo đổi lấy sai:** "nếu phần nào là bắt buộc phải giữ kết nối ổn định thì tôi hoàn toàn hiểu, không ép cứng là mọi thứ phải hoàn hảo, tôi chỉ nhấn mạnh là về việc tối thiểu hóa rủi ro, chứ không ép phải hoàn hảo 100% để rồi lại giảm đi sự chính xác của toàn bộ luồng" | Codex 03:33:57Z | Trực tiếp |
| **Bài học lịch thức dài:** "trước đó đã có 1 đợt chạy dài với phiên điều phối (… khoảng task 58-61) có việc claude điều phối nhưng không tận dụng tối đa thời gian rảnh do lịch đánh thức dài". Hồ sơ: `results/T-058/dem-2026-11-10/dieu-phoi/`; khoảng trống 75 phút ở `tasks/T-062-dem-chang-1-4/LICH-TU-TIEP-NHAN.md`; DECISIONS "Sửa cơ chế lịch tự tiếp nhận" | Codex 03:33:57Z | Trực tiếp |
| Tự đánh thức, không đợi Minh: "tôi sẽ treo máy nên bạn cần tự đánh thức khi xong, không đợi tôi đánh thức" | chat 19/11 17:46Z | Trực tiếp |
| Quyền tự quyết trong phạm vi mong muốn: "tôi cho bạn quyền quyết định các phần nằm trong mong muốn của tôi, sau đó trình kế hoạch tiếp theo" (phạm vi: phân tích sau lượt T-069) | chat 19/11 17:46Z | Trực tiếp; đã ghi LOG T-069 |
| Ghi đủ những gì Claude và Codex đã thống nhất, mọi mong muốn của Minh; Codex soát lệch "vì claude có thể quên" | chat 20/11 10:06Z | Trực tiếp |
| **Duyệt sửa gói và cho phiên mới triển khai:** "duyệt sửa, sau đó soạn prompt chi tiết cho phiên claude mới yêu cầu triển khai task , trước khi triển khai cần phiên tự rà soát lại toàn bộ plan một lượt nếu phát hiện có điểm xung đột hoặc rủi ro dẫm chân nhau giữa các phiên thì cần sửa ngay, nếu là lỗi nhỏ có thể sửa ngay sau đó duyệt triển khai task luôn, lỗi chặn thì dừng trình" | chat 20/11 (tin cuối trong `01`) | Trực tiếp |
| Chu kỳ dò dự phòng cụ thể (ví dụ 15 phút) và nội dung lịch | Codex `12`; `thong-nhat.md` §2 | **Chờ duyệt**: Minh yêu cầu "lịch đánh thức phù hợp", nhưng chưa duyệt cấu hình cụ thể |

## 2. Quyết định về T-069 (đã ghi LOG T-069)

| Quyết định | Nguồn |
|---|---|
| Khôi phục tải mua vé: "A: gia hạn qua API", sau đó (A không làm được bằng API) "B: SQL dời mốc" | chat 19/11 09:12Z, 09:18Z; LOG T-069 phiên 2 |
| Phân tích nguyên nhân ô tụt: "tôi muốn tìm nguyên nhân của các ca tụt, lí do tụt, do code thay đổi hay do tải , log trace metric thay đổi ?" | chat 19/11 17:46Z; LOG T-069 |
| Duyệt sửa theo phản biện kết quả T-069 (phiên fork): "đuyệt đề xuất sửa, sau đó trình kế hoạch tiếp theo" | LOG T-069 phiên 3 (20/11 02:31Z) |

## 3. Câu hỏi Minh đã hỏi (để phiên mới biết Minh quan tâm gì)

- Lỗi P7 ở RECREATE-PAY là tích cực hay tiêu cực (19/11 08:22Z).
- Tiến độ, giờ xong, điểm tiêu cực (ba lần, 19/11).
- Lệnh nền báo lỗi mà việc vẫn xong là sao (20/11 00:05Z).
- Nền là bắn tải nhiều giờ hay để im; có nên thử tải tối đa (20/11 01:03Z, 02:01Z).
- Ngày sự kiện ở Ticket/Payment; số bản ghi DB; bằng chứng truy vấn chậm; mốc nào; **"nếu reset như vậy thì có phải đang sửa để làm kết quả ?"**; W4/5/6/8 có song song được không (20/11 02:24Z).

Câu trả lời: `lich-su/02`, `03`, `04`.

## 4. Đề xuất ghi `docs/DECISIONS.md` (CHỜ MINH DUYỆT — chưa ghi)

Theo AGENTS §4, quyết định nói trong chat phải ghi vào DECISIONS khi được duyệt. Phiên điều phối mới trình Minh duyệt khối này:

```markdown
## Điều phối giai đoạn 2 sau T-069 (chat Claude và tin gửi Codex, 19–20/11/2026)

- Minh (20/11/2026): "tận dụng thời gian tối đa có thể nhưng tính đúng đắn vẫn ưu tiên cao nhất"; "1 phiên điều phối, phần nào cần tuần tự thì tuần tự"; "tổng hợp thông tin thành 1 plan duy nhất để tránh 2 phiên mâu thuật"; "cần claude thiết kế phiên điều phối chuẩn chỉnh, các phiên không dẫm chân nhau".
- Minh (20/11/2026): "không cần phải đợi đến đêm, tôi có thời gian, không tự giới hạn bản thân".
- Minh (20/11/2026, gửi Codex 03:33:57Z): phiên điều phối Opus 5.5 high hoặc xhigh do Minh chọn; phiên làm việc Claude medium hoặc high theo độ khó, sai liên tục thì báo Minh xem xét tăng mức; Codex qua terminal làm việc phụ, model gpt 6.2 astra mức high, hết usage thì báo Minh đổi account; lịch đánh thức phù hợp, không làm lại sau tạm dừng nhưng "không ép phải hoàn hảo 100% để rồi lại giảm đi sự chính xác của toàn bộ luồng".
- Minh (20/11/2026): chuyển sang phiên Claude điều phối mới, đổi account; bàn giao bằng `docs/techstack/ban-giao-dieu-phoi-2026-11-20/`; phiên mới tự rà soát toàn bộ plan, sửa ngay lỗi nhỏ hoặc xung đột giữa các phiên rồi triển khai, gặp lỗi chặn thì dừng trình.
```
