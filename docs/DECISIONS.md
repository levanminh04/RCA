# Nhật ký quyết định của Minh

Chỉ ghi điều Minh đã quyết, theo lời Minh. Đề xuất của agent nằm ở MRP hoặc WHY cho tới khi Minh chốt. Sổ quyết định v1 (RCA-001 đến RCA-118) và v2 (D-01 đến D-16) đã đóng. Các quyết định cũ còn giá trị đã được Minh xác nhận lại ngày 02/10 (Q-20, Q-22 đến Q-29).

| Mã | Ngày | Quyết định | Ghi chú |
|---|---|---|---|
| Q-01 | 02/10 | Đập đi xây lại phần RCA, không neo theo v1 và v2. Khảo sát Task A, Task B được tham khảo nhưng phải tự lập luận độc lập. | |
| Q-02 | 02/10 | Đến 20/10 phải có cả kết quả phương pháp đồ thị, càng sớm càng tốt. Thời gian không phải ràng buộc chính vì có Claude và Codex; hướng đi đúng mới là ưu tiên. | MRP §7 |
| Q-03 | 02/10 | Ba dataset cô nêu (Train Ticket, Sock Shop, LEMMA-RCA) chỉ là ví dụ. Chọn dataset theo tiêu chí. | MRP §4 |
| Q-04 | 02/10 | Báo kết quả trung thực, kể cả khi đồ thị không hơn baseline. Báo cô để cô định hướng tiếp; còn nhiều lần báo cáo tiến độ trước khi kết thúc đồ án. | MRP §3 |
| Q-05 | 02/10 | Chưa hỏi cô. Tự diễn giải hướng dẫn và chọn hướng tốt nhất, rồi báo cáo tiến độ để cô định hướng. | MRP §2.3 |
| Q-06 | 02/10 | Kho quan sát: OTel Java Agent → OTel Collector → Tempo (trace); log JSON → Collector → Loki; Actuator/Micrometer → Prometheus; Grafana để truy vấn và hiển thị. Đã duyệt làm baseline kỹ thuật, chưa triển khai hay kiểm chứng runtime; có thể đổi để phù hợp RCA. | MRP §1, P9 |
| Q-07 | 02/10 | FlashTicket vừa để demo vừa là bộ dữ liệu thực nghiệm (tự tiêm lỗi, tự gán nhãn, có chấm điểm). Làm sau phần dataset công khai. | MRP P10 |
| Q-08 | 02/10 | Repo mới ở `D:\RCA-flashticket`, code mới. Repo cũ chỉ để tham khảo; chép dữ liệu thô và tài liệu khảo sát khi cần. | WHY-11. **Sửa sau, cùng ngày:** tài liệu khảo sát đã lọc vào `docs/knowledge/`; không đọc, không chép từ repo cũ (AGENTS luật cứng 7). Dữ liệu thô được mang về nếu khớp hash của nguồn gốc (Q-21) |
| Q-09 | 02/10 | ~~Claude làm chính, Codex phản biện.~~ Thay bằng Q-13. | |
| Q-10 | 02/10 | Mọi lập luận phải có sẵn câu trả lời cho "tại sao chọn X". | `docs/WHY.md` |
| Q-11 | 02/10 | Cần một Master Research Program và cách làm việc nhất quán của agent, kể cả khi mở phiên mới hoặc bị ngắt vì hết usage. | MRP, AGENTS, STATE |
| Q-12 | 02/10 | Agent không tự đoán ý Minh; điều chưa rõ thì hỏi. | AGENTS luật cứng 2 |
| Q-13 | 02/10 | Không bắt buộc Claude làm chính, Codex phản biện. Hai bên có thể đổi vai khi một bên hết token. | AGENTS mục 1, 8; WHY-12 |
| Q-14 | 02/10 | Không dùng settings.json hay hook để cưỡng chế. Dùng các file luật là đủ, ghi rõ và chi tiết. Ở chế độ auto, agent được tạo file mà không hỏi, nhưng vẫn phải nằm trong phạm vi luật cho phép. | AGENTS mục 2 |
| Q-15 | 02/10 | Tổ chức dữ liệu sao cho session mới hay thiết bị mới đọc lại docs vẫn có toàn bộ tiến trình, không mất ngữ cảnh; luật đảm bảo ở mọi nơi. | AGENTS mục 4, 6, 7; `tasks/` |
| Q-16 | 02/10 | Ưu tiên mỗi task là một session mới. | AGENTS mục 5 |
| Q-17 | 02/10 | Duyệt Luật 0 (không sửa khi chưa được Minh duyệt) làm luật quyền cao nhất. | AGENTS mục 2 |
| Q-18 | 02/10 | LLM không bắt buộc phải là Gemini. | MRP P8 |
| Q-19 | 02/10 | Minh dựng bộ tạo tải và bộ tiêm lỗi cho FlashTicket. | MRP P10 |
| Q-20 | 02/10 | Giữ D-01 (trục chính khi bảo vệ là cơ chế giám sát và chẩn đoán dựa trên đồ thị chạy trong FlashTicket; "đồ thị giúp khi nào" là phần hỗ trợ), nhưng không được làm nhẹ phần nghiên cứu. | |
| Q-21 | 02/10 | Dữ liệu cũ dùng được, không bị sửa đổi, không thiếu thì mang về repo mới, coi như mới, tránh tải lại thừa. Cái nào chưa có thì được tải, nhưng phải trình dung lượng dự kiến trước khi tải. | AGENTS luật cứng 7; `data/README.md` |
| Q-22 | 02/10 | Bỏ D-02 ("phải có ít nhất một điều kiện đồ thị hỗ trợ tốt"). | Q-04 |
| Q-23 | 02/10 | Giữ D-03: báo cáo đồ án cuối cùng 30/12/2026. | |
| Q-24 | 02/10 | Giữ D-12: không làm dập khuôn mọi phương pháp cô nêu làm ví dụ. | MRP §2.3 |
| Q-25 | 02/10 | Giữ D-14: laptop 16 GB là cố định; chỉ thử huấn luyện mô hình nếu có căn cứ là hiệu quả. | WHY-10 |
| Q-26 | 02/10 | Giữ D-16: câu hỏi nhanh thì trả lời nhanh, không để hết usage khi việc chính chưa làm. | AGENTS |
| Q-27 | 02/10 | Giữ RCA-002: chấp nhận đóng góp dạng thực nghiệm có kiểm soát và kỹ thuật; không yêu cầu thuật toán mới. | |
| Q-28 | 02/10 | Giữ D-07 (demo ưu tiên phần lõi; làm thủ công trước, nâng cao nếu còn thời gian; Minh tích hợp RCA, Tuyến làm giao diện), nhưng không được xem nhẹ phát hiện bất thường, không chỉ tập trung RCA. | MRP P10 |
| Q-29 | 02/10 | Giữ D-09 theo cả hai nghĩa: (a) không cần thủ tục nặng, chỉ cần vừa đủ để kết quả đúng và chuẩn; (b) không cần cố cắt quy trình cho gọn, bước nào cần để đúng và chuẩn thì giữ, dù quy trình dài hơn. | AGENTS |
| Q-30 | 02/10 | Duyệt D7: phát hiện bất thường có hồ sơ phương pháp (P1), chấm riêng bằng P/R/F1 (P3) và phân tích hạn chế (P4), ghi rõ trong RQ1, RQ2. | MRP §3, P1, P3, P4 |
| Q-31 | 02/10 | Ghi chú để bước chọn dataset không bị thiên vị RCAEval. | MRP §4 |
| Q-32 | 02/10 | Sửa cả 12 điểm phản biện G0 của T-000. R1 theo đề xuất của người làm. R7: Minh giao chốt một hướng nhất quán; hướng đã chốt: phiên phản biện chỉ ghi REVIEW.md, người làm điền bảng phản hồi, ghi LOG và STATE. | AGENTS mục 4–9; `tasks/T-000-nen-tang/REVIEW.md` |
| Q-33 | 02/10 | Mọi nhận định dựa trên một kết quả phải có phản biện đa chiều: kết quả là thế, nhưng còn nguyên nhân khả thi nào khác giải thích nó. Được đọc v1, nhưng kết quả v1 (30 ca dev, 10 ô) không phải bằng chứng mạnh. | AGENTS mục 11 |
| Q-34 | 02/10 | Minh đảm bảo FlashTicket sẽ xong. Agent không nêu lại rủi ro FlashTicket và rủi ro thời hạn. | |
| Q-35 | 02/10 | Kết quả không nhất thiết phải đẹp, nhưng dù tốt hay xấu đều phải chỉ ra lý do. Đi theo hướng cô: tìm chỗ phương pháp đã có làm được và chưa làm được, rồi từ đó tiến tới đồ thị. | MRP §3, P6 |
| Q-36 | 02/10 | Duyệt G0: MRP v3. | MRP |

