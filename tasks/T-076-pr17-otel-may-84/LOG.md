# Nhật ký T-076

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối, không sửa mục cũ.

---

## Phiên 1 — 26/11/2026 — Claude — laptop — vai trò: người làm

**Mở phiên:** tiếp từ phiên T-070 (cùng phiên chat). Đã đọc AGENTS, STATE, mẫu SPEC/LOG.

**Công đoạn và mục tiêu nguồn:** trình SPEC. DT18-NV1, NV2; MRP P9a, P10. Minh cho viết SPEC ("Duyệt, viết SPEC", 26/11) sau đề xuất làm lại PR #17 thành một PR duy nhất.

**Diễn biến:**
- 26/11 — Kiểm chỉ đọc: repo FlashTicket laptop @`36a3725` (`rca/exp-2026-11`); `origin/main` `f178870` (22/11) hơn `640dbaf` 52 commit/171 file; PR #17 OPEN CONFLICTING, ahead 10/behind 92, 124 file; `git merge-tree` → 13 file xung đột; main: 10 service `runtime: k8s`, CD tự triển khai lên 84 khi push main, cấu hình ở `deploy/k8s/<svc>/configmap.yaml`; Dockerfile main không có agent; entrypoint PR #17 đặt `OTEL_LOGS_EXPORTER=none` khi bật agent (log không đi qua agent).
- 26/11 — Viết `SPEC.md` (đề xuất). Sửa câu sai ở `results/T-070/don/KE-HOACH-DON.md` §12 (ghi "image có agent" trong khi main chưa có) và trỏ hai dòng việc sau sang T-076 (Minh duyệt sửa trong đề xuất 26/11). Thêm dòng T-076 vào STATE.

**Quyết định của Minh trong phiên:**
- "dọn cả PR 17 những chỗ lỗi thời cho tôi, PR 1 cái thôi, không phải merge PR 17 lại tạo 1 PR nữa" (26/11).
- "không có chuyện vào set thủ công nhé" (bật agent cho máy 84, 26/11).
- "Duyệt, viết SPEC" (26/11). Chưa ghi DECISIONS.

**Kết thúc phiên:**
1. Đã làm gì: kiểm hiện trạng (chỉ đọc), viết SPEC đề xuất.
2. File đã thay đổi: `tasks/T-076-pr17-otel-may-84/{SPEC.md,LOG.md}`, `docs/STATE.md` (dòng T-076), `results/T-070/don/KE-HOACH-DON.md` (§12, 2 dòng).
3. Kiểm đã chạy: `gh pr view/list`, `gh api compare`, `git merge-tree`, đọc `services.json`, `cd.yml`, `_deploy-service.yml`, Dockerfile, `docker-entrypoint.sh`, `configmap.yaml`, `deployment.yaml`.
4. Cần Minh quyết: duyệt SPEC cùng Q1–Q6 (bảng cuối SPEC), gồm chữ ngoại lệ `AGENTS.md` §12 (Q5).

**Bước tiếp theo:** Minh duyệt SPEC (hoặc gửi prompt dưới cho Codex soát trước) → bước 1 (kiểm kê từng file PR, chỉ đọc).

**Lệnh cuối đã chạy:** `git merge-tree --write-tree --name-only --no-messages origin/main origin/rca/quan-sat-log` (repo FlashTicket).

### Prompt cho Codex soát SPEC

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076 — tasks/T-076-pr17-otel-may-84/SPEC.md (trạng thái: đề xuất, chưa duyệt).
- Công đoạn: soát SPEC.
- Gói/cổng: P9, P10; việc tích hợp ngoài cổng G0–G4 nên không kèm khối trọng tâm cổng.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex.
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/SPEC.md; repo FlashTicket D:/Project/flash-ticket-platform (origin/main f178870, origin/rca/quan-sat-log bb84d64 = PR #17, origin/rca/exp-2026-11 36a3725; chỉ đọc); repo lab D:/Project/flashticket-rca-lab @85ace52; results/T-070/don/KE-HOACH-DON.md §12; results/T-067/, results/T-070/don/q4/; docs/MRP.md P9, P10; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; AGENTS.md §12.
- Phản biện và phản hồi trước: không có.
- Code và kết quả liên quan: đọc GitHub bằng gh (repo levanminh04/flash-ticket-platform) và git cục bộ, chỉ đọc. Được đọc trên máy bằng: bash results/T-070/kiem-ke/tho/lenh/ssh.sh app|obs|tai, đưa script qua stdin; chỉ lệnh đọc. Không vào máy 84.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-076-pr17-otel-may-84/REVIEW.md (chưa có; theo mẫu tasks/_MAU/REVIEW.md). Không sửa file nào khác.

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

Công đoạn: soát SPEC.
Kiểm câu hỏi nguồn, phần mục tiêu được bao phủ, giả thuyết khác, khả năng phân xử của dữ liệu, phép kiểm dự kiến, phụ thuộc bước, chi phí, phạm vi và tiêu chí xong. Phần không làm phải có lý do, hệ quả và quyết định phụ thuộc.
Đánh giá kế hoạch và bằng chứng đã có; không đòi có kết quả của thực nghiệm chưa được duyệt. Phân biệt ứng viên để thử với lựa chọn đã chốt.
Chỉ ghi bản phản biện được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat nếu chưa có quyền ghi. Không tự sửa SPEC.

Yêu cầu của Minh cho task (nguyên văn, 26/11): "dọn cả PR 17 những chỗ lỗi thời cho tôi, PR 1 cái thôi, không phải merge PR 17 lại tạo 1 PR nữa"; về bật agent cho máy 84: "không có chuyện vào set thủ công nhé". Yêu cầu chung (24/11): "đừng quá overengerning. kiểm xem có sai lệch nào hoặc lỗ hổng nào bị bỏ sót không".
Không dùng subagent (Minh dặn ngày 24/11).
```
