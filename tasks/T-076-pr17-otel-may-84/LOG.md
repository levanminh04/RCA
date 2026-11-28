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

## Phiên 2 — 26/11/2026 (Claude, laptop, người làm)

- 15:20Z — Minh chuyển kết quả Codex `REVIEW.md` (R1–R7; 6 chặn, 1 không chặn). **Tự soát trước khi đọc kết luận:** không độc lập (Minh dán tóm tắt cùng lúc). Kiểm từng điểm trên code: R1 `25550d2a5:src/m1/adapter_flashticket.py:24–36`, lab `gateway.yaml:114–153`; R2 FlashTicket `f178870:deploy/scripts/deploy-k8s-service.sh:196–236`, `deploy/k8s/discovery-server/statefulset.yaml`; R3 `agent-docker-host.yaml:161–182,225–234`; R4 SPEC C5 so với bước 9, `deploy-k8s-service.sh:171–175`; R5 `bb84d64:_maven-verify.yml:94`; R6 `f178870:_deploy-service.yml:79–82,118` (lỗi của người làm ở Q3); R7 lab `c1da15f`. **R1–R7 đúng cả.** Đáp trong chat theo phạm vi prompt.
- 15:40Z — **Minh "Duyệt viết bản 2"** (kèm điền bảng REVIEW và LOG). Đọc thêm (chỉ đọc): obs RAM trống ~10 GB/12 GB, đĩa 46%, 6 container quan sát; `cd.yml:6–18` có `restart` (sau khi cập nhật `ENV_<SVC>`) và `rollback`; pod `runAsNonRoot`, không `readOnlyRootFilesystem`; file mẫu Secret có mục `# Optional`.
  - Giữ bản 1: `SPEC.ban-1.md` (sha256 `b3bb3583…`, trùng bản Codex soát).
  - Viết `SPEC.md` bản 2. Thay đổi chính: tách đường máy 84 ở lớp thu (`collector-production` + `prometheus-production`, không qua gateway/`capture`, không sửa `rca/`, luật, bản phương pháp); token và `OTEL_AGENT_ENABLED` qua mục `# Optional` của file mẫu Secret, CA qua ConfigMap + entrypoint; merge với agent tắt, bật/tắt bằng `ENV_<SVC>` + CD `restart`; log máy 84 tắt lần đầu (Q1 (c)); CI B16 theo danh sách; Q3 sửa lý do; ngưỡng C5 (Q7), lấy mẫu (Q8), người giữ `ENV_<SVC>` (Q9); lab `c1da15f`, quyền obs bước 6–7.
  - Điền bảng phản hồi cuối `REVIEW.md`, cột Minh quyết để trống.
  - **Chưa kiểm:** header/CA qua biến môi trường; khả năng `rollback` thật của CD; IP ra Internet của máy 84.
  - **Bước tiếp:** Minh gửi prompt dưới cho Codex (ghi `REVIEW-2.md`), hoặc duyệt SPEC bản 2 với Q1–Q9 và IP máy 84 → bước 1 (bảng C1, chỉ đọc).
  - Lệnh cuối: `cp -p SPEC.md SPEC.ban-1.md`.

### Prompt cho Codex kiểm lại SPEC bản 2

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076 (tasks/T-076-pr17-otel-may-84/). SPEC bản 2 (SPEC.md), sửa theo REVIEW.md; bản 1 giữ ở SPEC.ban-1.md.
- Công đoạn: kiểm lại phản hồi và sửa (SPEC chưa duyệt).
- Gói/cổng: P9, P10, việc tích hợp ngoài G0–G4; không kèm khối trọng tâm cổng.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex (theo SPEC T-076).
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,SPEC.ban-1.md,LOG.md}; results/T-070/don/KE-HOACH-DON.md §12; DT18, hướng dẫn của cô, MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md (bảng phản hồi của người làm ở cuối).
- Code và kết quả liên quan: D:/Project/flash-ticket-platform (origin/main f178870, PR #17 bb84d64, nhánh ghim 36a3725); D:/Project/flashticket-rca-lab (main c1da15f); repo RCA 25550d2a5:src/m1/adapter_flashticket.py; results/T-070/don/q4/. Chỉ đọc. Được đọc máy obs bằng: bash results/T-070/kiem-ke/tho/lenh/ssh.sh obs, script qua stdin, chỉ lệnh đọc. Không vào máy 84, không sửa, không dừng/khởi động gì.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-076-pr17-otel-may-84/REVIEW-2.md (chưa có; theo mẫu tasks/_MAU/REVIEW.md). Không sửa file nào khác.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Yêu cầu riêng của Minh (nguyên văn, 24/11): "kiểm tính đúng đắn rủi ro sai lệch, tuy nhiên yêu cầu codex cũng đừng quá overengerning. kiểm xem có sai lệch nào hoặc lỗ hổng nào bị bỏ sót không".
Không dùng subagent (Minh dặn ngày 24/11).
```

## Phiên 3 — 26/11/2026 (Claude, laptop, người làm)

- 16:10Z — Minh chuyển kết quả Codex `REVIEW-2.md` (N1–N4, cả 4 chặn). **Tự soát trước khi đọc kết luận:** không độc lập (Minh dán tóm tắt cùng lúc). Kiểm trên code: N1 `f178870:deploy-k8s-service.sh:170–175,261–271`, `plan-deploy.sh:19–28`; N2 lab `tests/signals/check_purchase_journey.py:41–54`; N4 lab `compose.yaml:77–78`, `datasources.yaml:21–33`; N3 đối chiếu B16 §6 với bước 6 bản 2. **N1–N4 đúng cả.** Đáp trong chat.
- 16:30Z — **Minh "Duyệt viết bản 3"** (kèm điền bảng REVIEW-2 và LOG). Kiểm thêm (SSH obs, chỉ đọc): Tempo cửa sổ Q4, `booking-service` 200/200 trace có `deployment.environment="exp"`, 0 trace khác (giới hạn 200).
  - Giữ bản 2: `SPEC.ban-2.md` (sha256 `7da4b872…`, trùng bản Codex soát ở REVIEW-2).
  - Sửa `SPEC.md` thành bản 3: hiện trạng CD (một `previous`, nhóm `k8s` 10 service, rollback áp lại snapshot Secret) và đọc Tempo; C3 lọc ở nguồn, kiểm payload thô ở bước 4; C4 bộ kiểm tín hiệu lọc `exp`, đối chứng dương, stage chạy truy vấn Prometheus thật; C5 hoàn tác từng service, `rollback` chỉ trong pha agent tắt; C7 mới (datasource riêng, reload API); phạm vi ghi lab thêm `tests/signals/check_purchase_journey.py` (chỉ lọc môi trường); bước 8–9; tiêu chí 2–4; Q10 (giới hạn quay về A sau khi bật).
  - Điền bảng phản hồi cuối `REVIEW-2.md`, cột Minh quyết để trống. Cập nhật dòng T-076 trong STATE.
  - **Chưa kiểm:** cấu hình agent lọc ở nguồn; header/CA qua biến môi trường; reload datasource trên Grafana đang chạy; `rollback` về A thật sự dùng được; IP máy 84.
  - **Bước tiếp:** Minh gửi prompt dưới cho Codex (ghi `REVIEW-3.md`), hoặc duyệt SPEC bản 3 với Q1–Q10 và IP máy 84 → bước 1.
  - Lệnh cuối: `cp -p SPEC.md SPEC.ban-2.md`.

### Prompt cho Codex kiểm lại SPEC bản 3

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076 (tasks/T-076-pr17-otel-may-84/). SPEC bản 3 (SPEC.md), sửa theo REVIEW.md và REVIEW-2.md; bản cũ giữ ở SPEC.ban-1.md, SPEC.ban-2.md.
- Công đoạn: kiểm lại phản hồi và sửa (SPEC chưa duyệt).
- Gói/cổng: P9, P10, việc tích hợp ngoài G0–G4; không kèm khối trọng tâm cổng.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex (theo SPEC T-076).
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,SPEC.ban-1.md,SPEC.ban-2.md,LOG.md}; results/T-070/don/KE-HOACH-DON.md §12; DT18, hướng dẫn của cô, MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md, REVIEW-2.md (bảng phản hồi của người làm ở cuối mỗi bản).
- Code và kết quả liên quan: D:/Project/flash-ticket-platform (origin/main f178870, PR #17 bb84d64, nhánh ghim 36a3725); D:/Project/flashticket-rca-lab (main c1da15f); repo RCA 25550d2a5:src/m1/adapter_flashticket.py; results/T-070/don/q4/. Chỉ đọc. Được đọc máy obs bằng: bash results/T-070/kiem-ke/tho/lenh/ssh.sh obs, script qua stdin, chỉ lệnh đọc. Không vào máy 84, không sửa, không dừng/khởi động gì.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-076-pr17-otel-may-84/REVIEW-3.md (chưa có; theo mẫu tasks/_MAU/REVIEW.md). Không sửa file nào khác.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Yêu cầu riêng của Minh (nguyên văn, 24/11): "kiểm tính đúng đắn rủi ro sai lệch, tuy nhiên yêu cầu codex cũng đừng quá overengerning. kiểm xem có sai lệch nào hoặc lỗ hổng nào bị bỏ sót không".
Không dùng subagent (Minh dặn ngày 24/11).
```

## Phiên 3 (tiếp) — 26/11/2026

- 16:50Z — **Minh duyệt SPEC bản 3 ngày 26/11/2026** ("Duyệt luôn bản 3"; không gửi Codex kiểm bản 3). Duyệt gồm Q1–Q10 theo cột đề xuất của SPEC: Q1 (c) lần đầu chỉ trace và metric; Q2 (a) Assistant chỉ agent; Q3 giữ build hai kiến trúc của main, giữ `SERVICE_VERSION`; Q4 Collector + Prometheus riêng, HTTPS CA tự ký + token, chỉ mở cho IP máy 84; Q5 chữ ngoại lệ `AGENTS.md` §12 ở mục "Phạm vi ghi" (ghi trước bước 2); Q6 pha 4 duyệt riêng; Q7 ngưỡng C5; Q8 lấy mẫu 10%; Q9 người giữ `ENV_<SVC>` cung cấp trước bước 9; Q10 chấp nhận giới hạn quay về image trước merge sau khi bật.
  - Bản duyệt: `SPEC.md` sha256 `48c87bea…` trước khi ghi dòng trạng thái; sau khi ghi dòng trạng thái `1ad8792e…`. Chỉ đổi dòng "Trạng thái".
  - Còn chờ: IP ra Internet của máy 84 (trước bước 6); người giữ bản đầy đủ `ENV_<SVC>` (trước bước 9). Quyết định cần ghi chính thức vào `docs/DECISIONS.md`: trình chữ riêng theo Luật 0.
  - **Bước tiếp:** bước 1 (bảng C1 từng file và hunk của PR #17 so với `origin/main` lúc dựng; chỉ đọc repo FlashTicket, ghi `results/T-076/bang-file-pr17.md`), khi Minh cho bắt đầu.

## Phiên 4 — 26/11/2026 (Claude, laptop, người làm)

- 17:00Z — Mở phiên. Minh "Làm bước 1". Chốt lúc dựng bảng: `origin/main` `f178870`, `origin/rca/quan-sat-log` `bb84d64`, merge-base `d147d49`; PR trước 10 / tụt 92; 124 file (46 thêm, 78 sửa), +5.028/−214.
- 17:40Z — **Bước 1 xong** (chỉ đọc repo FlashTicket, SSH exp-app chỉ đọc). Đầu ra `results/T-076/bang-file-pr17.md` (bảng 124 file) và `results/T-076/bang-file/` (`lap_bang.py` + 3 file đầu vào: danh sách file, 13 file xung đột, 25 file main cũng đổi; `bang.md` là phần bảng sinh ra). Kết quả: **Giữ 93, Sửa khi áp 17, Bỏ 14**.
  - Kiểm thêm để phân loại: file phủ lab `test-environment/overrides/` đã đặt bộ nhớ (booking/event/payment 1g, discovery 768m) và nhãn log cả 7 service → bỏ 7 file `deploy/app/*` không đổi cấu hình hiệu lực exp-app; Keycloak exp-app (`ft-local/keycloak:arm64-776d9c9e`) không có biến `KC_TRACING*`/`KC_LOG_CONSOLE*` → bỏ tracing Keycloak; `FT_FAULT*` của exp-app nằm ở `/opt/flashticket/env/{booking,event}-service.env`; main dừng ở GOV-149 → GOV-150..156 không trùng; `_deploy-service.yml`: diff ròng chỉ còn hunk `SERVICE_VERSION`; Dockerfile main giải nén theo lớp nhưng vẫn `java -jar /app/app.jar`.
  - Số Java ngoài test là 44 (16 thêm, 28 sửa), không phải "39" ghi ở SPEC; bước 5 đọc đủ 44.
  - Lần sinh đầu lỗi in ra màn hình (`-I` bỏ qua `PYTHONIOENCODING`), chạy lại với `-X utf8`. Sửa quy tắc một lần: `CorrelationIdFilter` của gateway xếp vào "mã quan sát".
  - **Chờ Minh duyệt bảng** (5 điểm cần xem kỹ ở đầu file). Bước tiếp sau duyệt: ghi ngoại lệ `AGENTS.md` §12 (Q5), rồi bước 2 dựng lại nhánh.
  - Lệnh cuối: `cat bang-file/dau.md bang-file/bang.md > bang-file-pr17.md` (đã xóa `dau.md` tạm).
- 17:55Z — **Minh "Duyệt bảng"** (`results/T-076/bang-file-pr17.md`: giữ 93, sửa 17, bỏ 14). Ghi ngoại lệ Q5 vào `AGENTS.md` §12 (dòng con dưới "Repo hệ thống FlashTicket", đúng chữ SPEC). Bắt đầu bước 2 trong worktree riêng, không đụng checkout `rca/exp-2026-11` của laptop.
- 18:40Z — **Bước 2 xong** (chỉ local, chưa push). Worktree `D:/Project/ft-pr17-dung-lai`, nhánh local `rca/quan-sat-log-dung-lai` từ `f178870`; checkout `rca/exp-2026-11` của laptop không đổi. Áp diff `d147d49..bb84d64` theo bảng đã duyệt (`git apply --3way`), 5 commit:
  - `005b780` log B16 (67 file); gỡ 3 xung đột Java: `OrderServiceImpl` giữ `orderViewAssembler` của main + dòng telemetry `reserve`; `PromotionServiceImpl` bỏ import `OrderMapper` (main đã thay); `RefundServiceImpl`: main bỏ `claimRefund`/`findUnfinishedAttempt`/`recordGatewayResult` (hoàn tiền chỉ trong DB, commit `782e557` của nhóm) → bỏ khối PR, chuyển telemetry `refund-result` vào `sendRefund` (`before` = trạng thái trước, `outcome` SUCCESS, lý do `DB_ONLY`).
  - `d51b780` hook `rca-test` (10 file mới).
  - `7b1c92a` CI: thêm `deploy/observability/b16-services.txt` (7 service); `_maven-verify.yml` kiểm B16 theo danh sách (biến môi trường, không chèn `${{ }}` vào lệnh); `detect-changes.sh` theo danh sách; hunk `SERVICE_VERSION`.
  - `6445a1d` agent: 7 Dockerfile dựng trên bản main + dòng agent (đối chiếu: Dockerfile PR không có hunk nào khác); 7 entrypoint thêm CA (`OTEL_CA_PEM_B64` → `/tmp/otel-ca.pem`, `OTEL_EXPORTER_OTLP_CERTIFICATE`); `payment-service/.env.example` lấy bản main + khối `OTEL_*` (main đã bỏ NGROK).
  - `533abfd` `decision-register.md` (GOV-150..156).
  - `deploy/observability/README.md` (Sửa) để lại cùng bước 3 (cần nội dung K8s).
  - Kiểm: file đổi so với main = đúng 110 (109 file giữ/sửa của bảng trừ README + `b16-services.txt`), 14 file "Bỏ" không đổi so với main; 81 file giữ mà main không đổi trùng blob PR; `git diff --check` sạch; không có khóa/mật khẩu; `sh -n` 7 entrypoint, `bash -n detect-changes.sh`, YAML `_maven-verify.yml` đạt; chạy giả entrypoint (thay `exec java` bằng echo): bật + CA → file CA đúng, `OTEL_EXPORTER_OTLP_CERTIFICATE` được đặt, `OTEL_LOGS_EXPORTER=none`; tắt → `java -jar`. Lần áp đầu chỉ ra 1 file do danh sách nhóm ghi CRLF; reset worktree mới tạo, bỏ CR, áp lại.
  - **Chưa kiểm:** biên dịch và test (bước 4); `detect-changes.sh` chạy thật (laptop không có `jq`, CI sẽ chạy).
  - **Bước tiếp:** bước 3 (K8s: ConfigMap 7 service, mục `# Optional` trong 7 file mẫu Secret, Assistant có agent, README quan sát viết lại).
  - Lệnh cuối: so blob 81 file giữ với `bb84d64` (0 khác).
- 19:30Z — Minh hỏi bước 3 có sửa cấu hình K8s của nhóm không; trình hai cách (ConfigMap / dồn hết vào `ENV_<SVC>`). Minh: "cứ làm cách tốt nhất… tránh làm tạm bợ chắp vá, tránh đi đường vòng" → giữ cách SPEC (ConfigMap, nhóm review được).
- 20:10Z — **Bước 3 (chưa commit, đã stage trong worktree)**, 23 file:
  - 7 `deploy/k8s/<svc>/configmap.yaml`: thêm khối agent (chỉ thêm dòng, không đổi khóa cũ): `ENVIRONMENT=production`, `OTEL_EXPORTER_OTLP_ENDPOINT=https://213.35.116.128` (cổng 443, còn trống trên obs theo `ss -ltn`), `http/protobuf`, lấy mẫu `parentbased_traceidratio` 0.1 (Q8), metric `otlp`, log `none`, khóa `traceId`/`spanId` cho log; `SPRING_AUTOCONFIGURE_EXCLUDE` (Lettuce observation) ở gateway, booking, assistant; thuộc tính RabbitMQ ở event, booking, payment, ticket. Hai biến cuối chép đúng cấu hình đã chạy trên exp-app (`/opt/flashticket/env/*.env`, SSH chỉ đọc); assistant dùng Redis, Spring Boot 4.1.1 như booking nên tên lớp exclude tồn tại. YAML đọc được, mọi giá trị là chuỗi.
  - 7 `deploy/k8s/examples/<svc>.secret.env.example`: mục `# Optional` thêm `OTEL_AGENT_ENABLED=`, `OTEL_EXPORTER_OTLP_HEADERS=`. Thử đúng đoạn lọc khóa của `deploy-k8s-service.sh` (chép, so diff chỉ khác dòng đầu/chú thích) với dotenv giả: không khai → Secret không có khóa OTEL, không thiếu khóa bắt buộc; khai → hai khóa vào Secret, header giữ nguyên.
  - Assistant: Dockerfile (bản main + dòng agent), `docker-entrypoint.sh` (giống 7 service), `.dockerignore`, khối `OTEL_*` trong `.env.example`.
  - `deploy/observability/README.md` viết lại theo K8s (bỏ nội dung Compose/`deploy/rca-test`).
  - Kiểm K8s có sẵn của nhóm: `test-k8s-deploy.py`, `test-k8s-discovery.py`, `test-https-config.py` đạt; `test-k8s-rollout-hooks.py` cần Docker, Docker Desktop laptop không chạy → chưa chạy được.
  - **Dừng, trình Minh (khác SPEC/chưa có):** (1) `HOST_ID`: SPEC ghi đặt trong ConfigMap, nhưng B16 định nghĩa `hostId` là máy chạy process; đúng nghĩa trên K8s là tên node qua downward API (`spec.nodeName`) → thêm 4 dòng env vào 7 `deployment.yaml` (đề xuất); giá trị tĩnh trong ConfigMap thì phải đoán tên máy và sai khi có nhiều node. (2) `OTEL_CA_PEM_B64`: CA chưa có (SPEC tạo ở bước 6) → đề xuất tạo CA và chứng chỉ máy nhận trên obs ngay bây giờ (chỉ tạo file ở `/etc/flashticket-rca/production/`, root 600, không bật gì), đưa CA công khai vào ConfigMap trước khi push; cách khác: push không có CA rồi thêm commit trước merge. README đã viết theo hai đề xuất này.
  - Đính chính dòng trên: bước 3 hiện là **19 file** (7 ConfigMap, 7 file mẫu Secret, 4 file Assistant, README), không phải 23.
- 01:00Z (27/11) — **Minh "Duyệt cả hai"**: (1) `HOST_ID` lấy tên node qua downward API (`spec.nodeName`) trong 7 `deployment.yaml`; (2) tạo CA và chứng chỉ máy nhận trên obs ngay (file ở `/etc/flashticket-rca/production/`, root 600, không bật dịch vụ nào), CA công khai vào ConfigMap trước khi push.
- 01:20Z (27/11) — **Bước 3 xong**, commit local `ae5a870` trong worktree (26 file; nhánh `rca/quan-sat-log-dung-lai` nay 6 commit, 136 file so với main, chưa push):
  - 7 `deployment.yaml`: env `HOST_ID` = `spec.nodeName` ngay sau `POD_UID` (env có quyền trên envFrom; không ConfigMap nào đặt `HOST_ID`). YAML đọc được, 7 container có `HOST_ID`, frontend/Keycloak không đổi.
  - CA: script mới ở repo lab `observability/tls/tao-chung-chi.sh` (chưa commit lab), chạy bằng root trên obs (gửi qua stdin, file tạm `/tmp/tao-cc.sh` đã xóa): CA EC P-256 10 năm, chứng chỉ máy nhận 825 ngày, SAN `IP:213.35.116.128, IP:10.0.0.215`, `openssl verify` OK; `/etc/flashticket-rca/production/` root 700, 5 file root 600 (`ca.crt`, `ca.key`, `ca.srl`, `server.crt`, `server.key`); không bật dịch vụ nào, khóa riêng không rời obs. Chép `ca.crt` (công khai, 0 dòng `PRIVATE`) về lab `observability/tls/ca.crt`; vân tay SHA-256 trùng giữa obs, file lab và 7 ConfigMap (`OTEL_CA_PEM_B64` giải ra đúng CA).
  - Ghi chú bước 6: container Collector cần đọc `server.key` (hiện root 600) → chỉnh quyền/mount khi dựng Collector, trình lúc đó.
  - Kiểm: `test-k8s-deploy.py`, `test-k8s-discovery.py`, `test-https-config.py` đạt; `git diff --check` sạch; diff không có khóa riêng/token. `test-k8s-rollout-hooks.py` chưa chạy (cần Docker).
  - **Bước tiếp:** bước 4 kiểm cục bộ (cần Docker: build image Booking + Assistant có agent, collector cục bộ TLS + token giả, payload thô có sentinel; `mvn verify` các service đổi). Laptop: Docker Desktop đang tắt — Minh bật, hoặc chọn máy build khác.
  - Lệnh cuối: `git commit` (`ae5a870`) trong `D:/Project/ft-pr17-dung-lai`.
- 02:00–03:10Z (27/11) — Minh bật Docker Desktop. **Bước 4 kiểm cục bộ** (chưa push), kết quả `results/T-076/kiem-cuc-bo/README.md`:
  - Maven như CI: 8/8 `verify` đạt, 7/7 kiểm B16 đạt, `TicketPostgresIT` đạt, Event `-P rca-test` đạt; **Booking `-P rca-test` 453 test, 67 error** — 3 lớp `@WebMvcTest` thiếu bean `RcaFaults`, đã có ở `bb84d64` (LOG T-067: 68 error + 1 failure, để W6). Ba file Java gỡ xung đột qua test.
  - Image Booking (jar production) + Assistant: uid 10001, entrypoint, checksum agent, `SERVICE_VERSION` = `ae5a870…`. Mạng chặn GitHub Releases → jar từ Maven Central, SHA-256 trùng ghim; Dockerfile tạm chỉ thay dòng `ADD`.
  - Agent → Collector thử không processor: token sai/không có 401, đúng 200, không TLS 400. **Lộ ở nguồn:** query (email, điện thoại, token, `vnp_SecureHash`, `code`) trong `url.query` span SERVER và exemplar metric. Không lộ: header Authorization/Cookie, body, client secret, token xuất. SQL đã sanitize. `exception.message` có trong event span, không có cấu hình bỏ. Cấu hình `…sanitization.url.experimental.sensitive-query-parameters` + `OTEL_METRICS_EXEMPLAR_FILTER=always_off` che được tham số có tên trong danh sách (chặn theo tên, không phải whitelist).
  - Bộ nhớ (giới hạn 768 MiB): Booking 381 → 499 MiB khi bật agent, không OOM; Assistant 348 MiB, khởi động 18 s, không lỗi.
  - Sự cố trong lúc chạy (môi trường thử, không phải lỗi nhánh): RabbitMQ CI lần đầu lỗi `.erlang.cookie` (chạy lại đạt); `git` không hiểu `/d/...` khi tắt chuyển đường (dùng `D:/...`); Docker không đọc `/tmp` của Git Bash (đổi chỗ file tạm); env_file của Compose nội suy `$` (thoát `$$`); Booking thiếu role `booking_owner`, schema sai chủ, queue RabbitMQ chưa khai (thêm initdb, cờ `missing-queues-fatal=false` chỉ ở lượt thử).
  - **Dừng, trình Minh:** (1) N3 — cấu hình agent không đạt "whitelist trước khi xuất" (query theo danh sách chặn; `exception.message` không bỏ được); (2) lỗi Booking `-P rca-test` có sẵn, có sửa trong PR này không; (3) thêm `OTEL_METRICS_EXEMPLAR_FILTER=always_off` vào ConfigMap (cần cho mọi phương án).
  - Lệnh cuối: `bash results/T-076/kiem-cuc-bo/agent/chay-assistant.sh …` (Assistant sẵn sàng 18 s).
- 04:00Z (27/11) — Minh cho SSH vào máy 84 (`52.64.237.84`) để **đọc** tài nguyên (khóa `FlashTicket-Control-Diagnosis.ppk`, user `ubuntu`, cách vào và host key như `results/T-058/dem-2026-11-10/dieu-phoi/watchdog2.sh`). Chỉ chạy lệnh đọc.
  - Kết quả đọc máy 84 (05:07Z 27/11, chỉ đọc, `plink`): host `ip-172-31-41-236`, 2 vCPU, RAM 7.776 MiB (dùng 4.273, còn dùng được 3.502), đĩa `/` 29G dùng 88% (còn 3,7G), uptime 15 ngày. Cụm K3s v1.37.2 có **3 node**: `ft84` (172.31.41.236, 7,6 GiB; dùng 4.293Mi/55%; requests 2.188Mi, limits 3.498Mi), `server-1` (172.31.43.219, 1,9 GiB; 1.104Mi/57%; chỉ discovery-server), `server-2` (172.31.44.164, 3,7 GiB; 3.184Mi/**83%**; requests 2.720Mi/71%, limits 4.416Mi/**115%**). Trên `ft84` còn Docker: PostgreSQL 444/2.048 MiB, MongoDB 277/512, RabbitMQ 86/1.024, Redis 4/256, frontend 4/64.
  - Pod (chưa có agent), dùng / giới hạn: booking 654/768 và 411/768 (2 bản, HPA 1–2), payment 689/768 và 368/768, ticket 580/768, keycloak 571/768, event 456/512, gateway 291/768, assistant 256/768, user 256/768, discovery 229/384. Bản booking `hqblg` restart 1 lần (lý do `Error`, không phải OOM, 05:03Z). Nhiều pod tạo trong 04:33–05:07Z (payment có ReplicaSet mới `846fcd559` lúc 05:07Z): nhóm đang triển khai, không phải do phiên này.
  - Hệ quả cho C5 (suy luận, **chưa kiểm** dưới tải): agent thêm ~118 MiB (đo booking trên laptop, bước 4) → booking ~772, payment ~807 vượt 768Mi; event ~574 vượt 512Mi. Bật agent cần nâng giới hạn bộ nhớ, mà `server-2` đã cam kết 115% limits và dùng 83%.

## Phiên 5 — 27/11/2026 (Claude, laptop, người làm)

- 06:00Z — Minh hỏi cách bố trí (cụm K8s, Collector, phí AWS, Grafana, pod bị hủy); trình 4 hướng H1–H4. **Minh "Duyệt hướng H1 + H4, viết SPEC bản 4"**, nhấn mạnh: demo phải chỉn chu; SPEC thiết kế mở — sau này chuyển sang AWS chỉ thêm hoặc sửa nhỏ (IP, cổng, kết nối), không xóa, không đổi cấu trúc thư mục.
  - Kiểm thêm (chỉ đọc): main `deploy/app/` vẫn đủ 7 file service + `frontend.yml`, `keycloak.yml`, không có Assistant (exp-app giữ 7 service); `build.sh` lab build 7 service; tham số query qua `@RequestParam` phần lớn vô hại, cần che `q` và 28 tên `vnp_*`; VNPay `return`/`ipn` là GET có tham số ở query (`PaymentController.java:52,59`).
  - Giữ bản 3 (đã duyệt): `SPEC.ban-3.md` (sha256 `1ad8792e…`, trùng `SPEC.md` trước khi ghi). Viết `SPEC.md` bản 4: Phần A PR #17 agent tắt, đích agent `http://otel-collector:4318` trong cụm, tắt exemplar, che `q` + `vnp_*` ở nguồn, bỏ CA/token khỏi pod, sửa lỗi Booking `-P rca-test`; Phần B dựng lại exp-app từ main mới cho demo (kiểm tín hiệu, lượt nền, hồi quy V082, diễn tập); mục "Mở rộng sang máy 84" chỉ thêm. Q1–Q7 mới; Q2, Q3, Q5 bản 3 giữ.
  - **Chưa kiểm:** cấu hình bản 4 trên laptop (bước 4); bản main mới trên exp-app (bước 8–9).
  - **Bước tiếp:** Minh gửi prompt dưới cho Codex (ghi `REVIEW-3.md`), hoặc duyệt SPEC bản 4 với Q1–Q7 → bước 3.
  - Lệnh cuối: ghi `SPEC.md` bản 4.

### Prompt cho Codex soát SPEC bản 4

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/SPEC.md (bản 4, đề xuất; bản cũ SPEC.ban-1.md, SPEC.ban-2.md, SPEC.ban-3.md — bản 3 đã được Minh duyệt 26/11).
- Công đoạn: soát SPEC.
- Gói/cổng: P9, P10, việc tích hợp ngoài G0–G4; không kèm khối trọng tâm cổng.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex (theo SPEC T-076).
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,SPEC.ban-3.md,LOG.md}; results/T-076/bang-file-pr17.md; results/T-076/kiem-cuc-bo/README.md; results/T-070/don/KE-HOACH-DON.md §12; DT18, hướng dẫn của cô, MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md, REVIEW-2.md (bảng phản hồi của người làm ở cuối mỗi bản).
- Code và kết quả liên quan: D:/Project/flash-ticket-platform (origin/main f178870, PR #17 bb84d64, nhánh ghim 36a3725); worktree D:/Project/ft-pr17-dung-lai nhánh local rca/quan-sat-log-dung-lai (6 commit trên f178870, chưa push); D:/Project/flashticket-rca-lab main c1da15f; results/T-076/kiem-cuc-bo/ (script và kết quả thô). Chỉ đọc. Được đọc máy exp-app/obs bằng bash results/T-070/kiem-ke/tho/lenh/ssh.sh app|obs, script qua stdin, chỉ lệnh đọc. Không vào máy 84; số liệu máy 84 lấy từ LOG phiên 4 (đọc ngày 27/11).
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-076-pr17-otel-may-84/REVIEW-3.md (chưa có; theo mẫu tasks/_MAU/REVIEW.md). Không sửa file nào khác.

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

Không dùng subagent (Minh dặn ngày 24/11).
```

- 07:30Z (27/11) — Minh chuyển kết quả Codex `REVIEW-3.md` (soát SPEC bản 4; R1–R5 chặn, R6–R7 không chặn). **Tự soát trước khi đọc kết luận:** không độc lập (Minh dán tóm tắt cùng lúc). Kiểm (chỉ đọc): T-070 chưa có `REVIEW-5.md`; không service nào có starter OpenTelemetry/Micrometer tracing; `deployment.yaml` nạp ConfigMap rồi Secret; hạn bán sự kiện tải 02/12/2026 22:16Z (`KE-HOACH-DON.md` §2). **R1–R7 đúng cả.** Đáp trong chat theo phạm vi prompt.
- 08:00Z (27/11) — **Minh "Duyệt, viết SPEC bản 5"**. Giữ bản 4: `SPEC.ban-4.md` (sha256 `996e7f2e…`, trùng bản Codex soát). Viết `SPEC.md` bản 5: tắt cứng agent bằng `env:` trong `deployment.yaml` (khác đề xuất R1 giữ công tắc trong Secret; lý do: không phụ thuộc giá trị `ENV_<SVC>` không đọc được), file mẫu Secret không đổi so với main, bỏ `SPRING_AUTOCONFIGURE_EXCLUDE` khỏi Phần A; C4 nền sát merge, so theo service, kiểm chức năng GET (Q8), digest + `rollback`/revert; phạm vi ghi Phần B thêm máy tải, obs, exp-app; bước 10 chờ T-070 REVIEW-5; tiêu chí demo C6 theo N = 25 phút (`khai-truoc-e5.json`); Q5 chỉ dựng demo, W7 để sau; mục Mở rộng thêm `exception.stacktrace` và điều kiện OPEN; bước 8 kiểm ngrok, ngày bán (Q9), schema/fixture, hoàn tác. Điền bảng phản hồi cuối `REVIEW-3.md`, cột Minh quyết để trống.
  - **Bước tiếp:** Minh gửi prompt dưới cho Codex (ghi `REVIEW-4.md`), hoặc duyệt SPEC bản 5 với Q1–Q9 → bước 3. Song song: gửi `results/T-070/don/prompt-codex-6.md` (T-070 REVIEW-5) vì bước 10 phụ thuộc.
  - Lệnh cuối: điền bảng `REVIEW-3.md`.

### Prompt cho Codex kiểm lại SPEC bản 5

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/SPEC.md (bản 5, đề xuất; bản 4 ở SPEC.ban-4.md là bản đã soát ở REVIEW-3).
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P9, P10, việc tích hợp ngoài G0–G4; không kèm khối trọng tâm cổng.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex (theo SPEC T-076).
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,SPEC.ban-4.md,SPEC.ban-3.md,LOG.md}; results/T-076/bang-file-pr17.md; results/T-076/kiem-cuc-bo/README.md; results/T-073/khai-truoc-e5.json; results/T-073/trien-khai-e5.md; results/T-070/don/KE-HOACH-DON.md; DT18, hướng dẫn của cô, MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md, REVIEW-2.md, REVIEW-3.md (bảng phản hồi của người làm ở cuối mỗi bản).
- Code và kết quả liên quan: D:/Project/flash-ticket-platform (origin/main f178870, PR #17 bb84d64, nhánh ghim 36a3725); worktree D:/Project/ft-pr17-dung-lai nhánh local rca/quan-sat-log-dung-lai (6 commit trên f178870, chưa push; commit cuối ae5a870 còn theo bản 3); D:/Project/flashticket-rca-lab main c1da15f; results/T-076/kiem-cuc-bo/. Chỉ đọc. Được đọc máy exp-app/obs bằng bash results/T-070/kiem-ke/tho/lenh/ssh.sh app|obs, script qua stdin, chỉ lệnh đọc. Không vào máy 84; số liệu máy 84 lấy từ LOG phiên 4.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-076-pr17-otel-may-84/REVIEW-4.md (chưa có; theo mẫu tasks/_MAU/REVIEW.md). Không sửa file nào khác.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Không dùng subagent (Minh dặn ngày 24/11).
```

- 09:00Z (27/11) — Minh chuyển kết quả Codex `REVIEW-4.md` (kiểm bản 5; R1–R3 chặn, R4 không chặn). **Tự soát trước khi đọc kết luận:** không độc lập (Minh dán tóm tắt cùng lúc). Kiểm (chỉ đọc): `deploy-k8s-service.sh` lưu trạng thái ở `state/k8s/<svc>/` (`current`, `previous`, `<rev>/image`, `<rev>/secret-env.json`), không có revision trước thì CD chỉ in hướng dẫn. **R1–R4 đúng cả.** Đáp trong chat.
- 09:30Z (27/11) — **Minh "Duyệt, viết SPEC bản 6"**. Giữ bản 5: `SPEC.ban-5.md` (sha256 `d88cfbbf…`, trùng bản Codex kiểm). Sửa `SPEC.md` thành bản 6: hiện trạng CD và tuyến vận hành `c1da15f`; C4 đọc trạng thái CD trước merge (không đọc Secret), hẹn nhóm 60 phút, Q7 "báo và trình", Q8 khai trước, Q10 PR revert khẩn cấp; phạm vi ghi bước 9 (Q4 chạy thẳng `tai_linux.py`) và bước 10 (runbook mới `runbook-online.md` trên `c1da15f`, không checkout bản lab cũ); C6 dùng nguyên tiêu chí chức năng E5 (t̂ trong [tiêm, +600 s), hai cờ, mở được ca trong 25 phút, không có sự cố `he-thong` đang mở trước tiêm); câu "không đổi hành vi app" hẹp lại. Điền bảng phản hồi cuối `REVIEW-4.md`, cột Minh quyết để trống.
  - **Bước tiếp:** Minh gửi prompt dưới cho Codex (ghi `REVIEW-5.md`), hoặc duyệt SPEC bản 6 với Q1–Q10 → bước 3. Bước 10 vẫn chờ T-070 REVIEW-5 (`results/T-070/don/prompt-codex-6.md`).
  - Lệnh cuối: điền bảng `REVIEW-4.md`.

### Prompt cho Codex kiểm lại SPEC bản 6

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/SPEC.md (bản 6, đề xuất; bản 5 ở SPEC.ban-5.md là bản đã kiểm ở REVIEW-4).
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P9, P10, việc tích hợp ngoài G0–G4; không kèm khối trọng tâm cổng.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex (theo SPEC T-076).
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,SPEC.ban-5.md,SPEC.ban-3.md,LOG.md}; results/T-076/bang-file-pr17.md; results/T-076/kiem-cuc-bo/README.md; results/T-073/khai-truoc-e5.json; results/T-073/trien-khai-e5.md; results/T-070/don/q4/README.md; DT18, hướng dẫn của cô, MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md, REVIEW-2.md, REVIEW-3.md, REVIEW-4.md (bảng phản hồi của người làm ở cuối mỗi bản).
- Code và kết quả liên quan: D:/Project/flash-ticket-platform (origin/main f178870, PR #17 bb84d64, nhánh ghim 36a3725); worktree D:/Project/ft-pr17-dung-lai nhánh local rca/quan-sat-log-dung-lai (6 commit trên f178870, chưa push; commit cuối ae5a870 còn theo bản 3); D:/Project/flashticket-rca-lab main c1da15f; results/T-076/kiem-cuc-bo/. Chỉ đọc. Được đọc máy exp-app/obs bằng bash results/T-070/kiem-ke/tho/lenh/ssh.sh app|obs, script qua stdin, chỉ lệnh đọc. Không vào máy 84; số liệu máy 84 lấy từ LOG phiên 4.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-076-pr17-otel-may-84/REVIEW-5.md (chưa có; theo mẫu tasks/_MAU/REVIEW.md). Không sửa file nào khác.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Không dùng subagent (Minh dặn ngày 24/11).
```
- 10:00Z (27/11) — **Minh duyệt SPEC bản 6 ngày 27/11/2026** ("Duyệt luôn bản 6"; không gửi Codex kiểm bản 6), gồm Q1–Q10 theo cột đề xuất (Q1 sửa lỗi `rca-test`; Q2 đích `otel-collector:4318`; Q3 che `q` + `vnp_*`, tắt exemplar; Q4 tắt cứng bằng `env:`, Secret không đổi; Q5 dựng exp-app cho demo sau bước 7, W7 để sau; Q6 kịch bản C6; Q7 báo và trình khi RAM +10%; Q8 GET khai trước; Q9 ngày bán kiểm ở bước 8; Q10 PR revert khẩn cấp). `SPEC.md` sha256 `35a904b3eb4c9149…` trước khi ghi dòng trạng thái, `27c9a8843f84b8ee…` sau; chỉ đổi dòng "Trạng thái". Quyết định cần ghi chính thức vào `docs/DECISIONS.md`: trình chữ riêng. **Bước tiếp:** bước 3 (thay commit `ae5a870` theo C2) khi Minh cho bắt đầu.
- 10:20Z (27/11) — Minh "Làm bước 3, 4". Mở lại commit `ae5a870` trong worktree; giữ bản đó ở nhánh local `rca/quan-sat-log-ban-3`.
- 12:00Z (27/11) — **Bước 3, 4 xong** (chỉ local, chưa push). Kết quả `results/T-076/kiem-cuc-bo/ban-6/README.md`; chênh bảng file ở `results/T-076/bang-file-pr17.md` mục "Chênh bản 5".
  - Bước 3: sửa theo C2 bằng script (7 ConfigMap: đích `otel-collector:4318`, bỏ CA và `SPRING_AUTOCONFIGURE_EXCLUDE`, thêm tắt exemplar và che `q` + 28 `vnp_*`; 7 `deployment.yaml`: `OTEL_AGENT_ENABLED="false"`; 7 file mẫu Secret về bản main; 8 entrypoint bỏ khối CA, trùng bản PR; README viết lại). Sắp lại commit sau `7b1c92a` để commit agent không còn thêm rồi bỏ CA: `32f77cc` agent (8 service), `2ff5d31` GOV, `4ad34d3` K8s, `d46f3ae` sửa `rca-test`. Bản 3 giữ ở nhánh local `rca/quan-sat-log-ban-3` @`ae5a870`; `git diff rca/quan-sat-log-ban-3 HEAD` đúng 32 file dự định. Lỡ tạo nhánh tạm `rca/quan-sat-log-truoc-sap-xep` sai mốc (`533abfd`, vẫn với tới từ `ban-3`), đã xóa. Diff thêm không có khóa/token/CA.
  - Bộ kiểm K8s của nhóm: 4/4 đạt (gồm `test-k8s-rollout-hooks.py`, cần Docker).
  - Bước 4: Booking `-P rca-test verify` 454 test 0 error (trước 67 error); `verify` production 445 đạt; B16 đạt; jar production không có `RcaFaults`. Lần đầu `-P rca-test` 1 error do RabbitMQ CI chết (`.erlang.cookie` eacces); RabbitMQ lỗi ba lần liền khi chạy mặc định, chạy bằng `--user 999:999` thì đạt; giữ log lần lỗi.
  - Agent (env theo thứ tự K8s mô phỏng): Secret giả `true` + `env:` `false` → env cuối `false`, không dòng khởi động agent, Collector 0 byte; không khóa → như trên; ghi đè `true` → gửi tới `otel-collector`, `q`/`vnp_*` thành `REDACTED`, exemplar 0, `deployment.environment=production`, `host.id` từ `HOST_ID`. Log B16 khi tắt có `environment=production`, `hostId`. Bộ nhớ Booking 386–417 MiB (tắt), 492 MiB (bật), giới hạn 768.
  - Lệnh an toàn chặn một `rm -rf` trên đường biến (thư mục chưa tồn tại); chạy lại không cần xóa.
  - **Chưa kiểm:** quy tắc `env` thắng `envFrom` trên K8s thật (bước 7); CI GitHub (bước 5).
  - **Bước tiếp:** bước 5 — push `--force-with-lease` lên `rca/quan-sat-log` (cần Minh duyệt push), mô tả PR, CI, Codex soát PR.
  - Lệnh cuối: phân tích `ban-6/bat-ghi-de`.
- 12:30Z (27/11) — **Minh "Duyệt push"**. GitHub reset kết nối (`git fetch` 4 lần, `gh` 1 lần): **chưa push**, PR #17 vẫn `bb84d64` theo ref local; nhánh dựng lại chứa `origin/main` `f178870` theo ref local. Soạn mô tả PR `results/T-076/mo-ta-pr17.md` (chưa đăng). Lệnh push dự kiến khi mạng lại: `git -C D:/Project/flash-ticket-platform push --force-with-lease=rca/quan-sat-log:bb84d64 origin rca/quan-sat-log-dung-lai:rca/quan-sat-log` (lease khớp đầu PR đã soát), sau đó `gh pr edit 17` với mô tả trên và xem CI.
- 14:00Z (27/11) — GitHub kết nối lại. `git fetch`: **`origin/main` đã tiến `f178870` → `6b77144`** (22 commit 22–27/11, PR #52–#57 của nhóm: replica đọc cho Event/Ticket/Booking, Booking 2 pod + `podAntiAffinity`, frontend, `ShortDescription`); PR #17 vẫn `bb84d64`. Lệnh push đã duyệt giả định main `f178870` nên **dừng, chưa push**; trình lại Minh.
  - Phạm vi đổi của main (113 file): `services/` event 27, ticket 12, booking 12, user 4; `deploy/k8s/` booking/event/ticket (deployment, configmap) và 3 file mẫu Secret (+31 dòng, khóa replica); `deploy/scripts/deploy-k8s-service.sh` +632 dòng; `.github/scripts/test-k8s-deploy.py` +825, `test-k8s-rollout-hooks.py` +34, `test-ticket-replica.sh` mới; frontend; migrations. `deploy/app/` không đổi.
  - 13 file trùng với nhánh. `git merge-tree --write-tree origin/main rca/quan-sat-log-dung-lai` (không đổi ref): **2 xung đột**, `deploy/k8s/event-service/configmap.yaml` và `ticket-service/configmap.yaml`, cùng một dòng: main đổi `SPRING_APPLICATION_JSON` (readiness thêm `db`), nhánh thêm khối `OTEL_*` ngay sau. Gỡ dự kiến: lấy dòng của main + giữ khối `OTEL_*`. 11 file còn lại tự gộp (gồm `OrderServiceImpl`, 3 `application.yaml`, booking/event/ticket `deployment.yaml`).
  - Code mới của main không thêm câu lệnh log nào (`git diff f178870 origin/main -- 'services/*/src/main/**/*.java' | grep '^+.*log.(info|warn|error|debug)('`: rỗng).
  - **CD đổi cách hoàn tác** cho booking/event/ticket: có file `writer-baseline`; `rollback` có thể quay về `writer-baseline` thay `previous`; Booking/Event dừng `rollback` khi revision đang bật reader (`BOOKING_ROLLBACK_REQUIRES_WRITER_REVISION`, `EVENT_ROLLBACK_REQUIRES_WRITER_REVISION`); thêm `pdb`. Hệ quả: C4 (bước 6) phải đọc thêm `writer-baseline`; mục "Hoàn tác" của `mo-ta-pr17.md` cần sửa; Booking 2 pod làm đổi nền bộ nhớ máy 84.
  - **Đề xuất trình Minh** (chưa làm): (1) rebase 7 commit lên `6b77144` trong worktree (nhánh `rca/quan-sat-log-dung-lai`; giữ bản `f178870` ở nhánh local `rca/quan-sat-log-f178870`), gỡ 2 xung đột như trên; (2) kiểm lại phần bị ảnh hưởng vào `results/T-076/kiem-cuc-bo/ban-6-main-6b77144/`: bộ kiểm K8s của nhóm (script đổi), kiểm manifest C2, `verify` + B16 cho booking, event, ticket, user; Booking và Event `-P rca-test`; Ticket `TicketPostgresIT` + `test-ticket-replica.sh` nếu chạy được local; lượt agent `tat-secret-true` với image Booking mới. Không chạy lại `bat-ghi-de` (đường gửi và che không đổi); 4 service khác dùng lại kết quả bản 6. (3) sửa `mo-ta-pr17.md` (gốc `6b77144`, 15 xung đột, mục Hoàn tác theo `writer-baseline`); (4) push `--force-with-lease=rca/quan-sat-log:bb84d64` — cần Minh duyệt lại push. C4 bước 6 đọc thêm `writer-baseline` (chỉ đọc, không đọc `secret-env.json`).
  - Rủi ro: main của nhóm đổi nhanh (22 commit/5 ngày); main tiến tiếp trước merge thì lặp lại rebase. Đề xuất hẹn nhóm giờ merge ngay sau khi Codex và Minh soát xong.
  - **Bước tiếp:** chờ Minh duyệt (1)–(4). Lệnh cuối: `git merge-tree --write-tree --name-only origin/main rca/quan-sat-log-dung-lai`.
- 14:20Z (27/11) — **Minh "Duyệt cả 4 việc"** (rebase lên `6b77144`, kiểm lại phần bị ảnh hưởng, sửa `mo-ta-pr17.md`, push có lease `bb84d64`).
- 14:30Z (27/11) — **Đính chính giờ:** hai mục ghi "14:00Z" và "14:20Z" ở trên thực tế khoảng 13:30Z và 13:45Z (đọc nhầm đồng hồ; `verify` bắt đầu 13:48:42Z theo `tien-do.tsv`). Nội dung hai mục không đổi.
- 14:30Z (27/11) — **Làm 4 việc Minh duyệt.**
  - (1) Rebase 7 commit lên `origin/main` `6b77144` trong worktree; bản cũ giữ ở nhánh local `rca/quan-sat-log-f178870` @`d46f3ae`. Gỡ 2 xung đột ConfigMap Event, Ticket bằng script (`scratchpad/go-xung-dot.py`, kiểm khối HEAD đúng 1 dòng `SPRING_APPLICATION_JSON`): lấy dòng của main, giữ khối `OTEL_*`. `git range-diff`: 5 commit trùng, 2 commit chỉ đổi ngữ cảnh. Đầu mới `2a275b5`, 129 file so với main. Ghi mục "Rebase lên main `6b77144`" trong `results/T-076/bang-file-pr17.md`.
  - (2) Kiểm lại: `results/T-076/kiem-cuc-bo/ban-6-main-6b77144/README.md`. Bộ kiểm K8s 4/4 (routing cần `jq`, để CI); manifest C2 đạt; `verify` user 70, event 178, ticket 229, booking 453, 0 lỗi, B16 đạt cả 4; `-P rca-test` Event 186, Booking 462, 0 lỗi; `TicketPostgresIT` 22; jar production Booking không có `RcaFaults`; lượt `tat-secret-true` image mới: env cuối `false`, 0 dòng agent, 0 byte, 410 MiB. Quét bí mật diff: sạch.
  - (3) `results/T-076/mo-ta-pr17.md`: gốc `6b77144`, 2 xung đột mới, kết quả kiểm lại, mục Hoàn tác theo `writer-baseline`.
  - (4) `git fetch` lại: main `6b77144`, PR `bb84d64` khớp. `git push --force-with-lease=rca/quan-sat-log:bb84d64… origin rca/quan-sat-log-dung-lai:rca/quan-sat-log` → `bb84d64...2a275b5 (forced update)`. `gh pr edit 17` tiêu đề và mô tả theo `mo-ta-pr17.md`. PR #17: OPEN, **draft**, MERGEABLE; CI run 46013069317 đang chạy lúc ghi.
  - **Chưa xong bước 5:** CI xanh; Codex soát PR (prompt dưới, chờ Minh gửi; bản ghi `REVIEW-5.md`); Minh đọc (44 file Java ngoài test); bỏ draft khi Minh quyết. C4 (bước 6) đọc thêm `writer-baseline` của Booking, Event, Ticket.
  - **Bước tiếp:** xem kết quả CI (`gh pr checks 17`); CI đỏ thì đọc log và trình Minh, không tự sửa. Main tiến tiếp trước merge thì lặp rebase, trình lại.
  - Lệnh cuối: `gh pr edit 17 --title … --body-file …`.

Prompt cho Codex soát PR (Minh chuyển):

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/ (SPEC.md bản 6, đã duyệt 27/11/2026).
- Công đoạn: soát kết quả — bước 5 Phần A: PR #17 làm lại (nhánh rca/quan-sat-log) trước khi Minh merge.
- Gói/cổng: P9, P10, việc tích hợp ngoài G0–G4; không kèm khối trọng tâm cổng.
- Người làm và người phản biện chính thức: người làm Claude, người phản biện Codex.
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,LOG.md}; results/T-076/bang-file-pr17.md; results/T-076/mo-ta-pr17.md; results/T-076/kiem-cuc-bo/README.md, kiem-cuc-bo/ban-6/README.md, kiem-cuc-bo/ban-6-main-6b77144/README.md; docs/architecture/B16-observability-baseline.md trong repo FlashTicket; DT18, hướng dẫn của cô, MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md, REVIEW-2.md, REVIEW-3.md, REVIEW-4.md (bảng phản hồi của người làm ở cuối mỗi bản).
- Code và kết quả liên quan: repo FlashTicket D:/Project/flash-ticket-platform, PR #17 https://github.com/levanminh04/flash-ticket-platform/pull/17 (nhánh rca/quan-sat-log @2a275b5, gốc origin/main 6b77144); bản đọc local ở worktree D:/Project/ft-pr17-dung-lai (cùng commit); `git diff 6b77144 2a275b5`; nhánh PR cũ bb84d64; CI của PR trên GitHub (`gh pr checks 17`, `gh run view`). Chỉ đọc. Không vào máy 84, exp-app, obs.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-076-pr17-otel-may-84/REVIEW-5.md (chưa có; theo mẫu tasks/_MAU/REVIEW.md). Không sửa file nào khác, không bình luận lên PR GitHub.

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

Công đoạn: soát kết quả.
Kiểm trên đầu ra thật, code và dữ liệu được phép; không tin tóm tắt LOG. Đối chiếu tiêu chí xong với phần mục tiêu nguồn và mức căn cứ cho bước tiếp theo; chạy lại phần rẻ khi trong quyền được duyệt.
Phân biệt hoàn thành task mô tả, xác nhận cơ chế và đủ căn cứ chọn/đánh giá thiết kế. Giới hạn đã khai không tự miễn phép kiểm cần thiết còn làm được.
Chỉ ghi bản phản biện lượt được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ bản cũ; không sửa kết quả thay người làm.

Không dùng subagent (Minh dặn ngày 24/11).
```

## Phiên 6 — 28/11/2026 (Claude, laptop, người làm) — đáp REVIEW-5

- Mở phiên: Claude, laptop Minh, người làm. Minh dán tóm tắt hai bản REVIEW-5 (T-070, T-076) rồi "Cho ghi cả hai": ghi bảng phản hồi ở cuối `REVIEW-5.md` và mục LOG kèm prompt Codex. Không ghi STATE, không sửa code.
- **Giới hạn tự soát:** Minh dán tóm tắt kết luận trước khi người làm tự soát, nên tự soát không độc lập hoàn toàn với kết luận reviewer. Điểm tự tìm: **N1** 7 ConfigMap đặt khóa MDC của agent `traceId`/`spanId` trong khi lab exp-app dùng mặc định `trace_id`/`span_id` mà customizer ưu tiên; **N2** hai mốc giờ LOG 27/11 sai (đã đính chính 14:30Z 27/11).
- **Phản hồi** (bảng cuối `REVIEW-5.md`): R1 đúng (CHẶN); R2 đúng cơ chế, là điều kiện chặn merge (OPEN, cần nhóm xác nhận trạng thái reader Booking/Event/Ticket trên 84); R3 đúng một phần (vẫn nối A → B qua `requestId` Booking); R4, R5 đúng; R6 đúng, người làm bỏ sót Discovery; R7 đúng một phần (agent tắt đúng; agent bật chưa kiểm); R8 đúng (không chặn); R9a, R9b đúng (R9b là lỗi quy trình: bỏ `test-ticket-replica.sh` đã duyệt mà không trình lại).
- **Kiểm đã chạy (chỉ đọc):** mã `2a275b5` (listener Booking/Payment, `BookingPersistenceIT`, `deploy-k8s-service.sh:385–498`, `BusinessTelemetry` Payment/Booking, `LogFields`, `CorrelationFilter` Booking/Event, `EventLogCustomizer`, `TicketOutboxPublisher`, StatefulSet Discovery, `log.schema.json`); `grep` lab không đặt `OTEL_INSTRUMENTATION_COMMON_LOGGING_*_KEY`. Không chạy profile `integration`; không chạy `test-ticket-replica.sh` (Docker laptop tắt 28/11).
- **Đề xuất sửa, gom theo file (chưa làm, chờ Minh duyệt; commit mới trên PR, ~1,5–2 giờ gồm kiểm):**
  1. `services/booking-service/src/test/.../BookingPersistenceIT.java`: fixture trỏ vào hàm `*Delivery` (R1); chạy `-P integration` cho các ca bị tác động.
  2. `services/payment-service/.../observability/BusinessTelemetry.java`: `stateAfter=UNKNOWN` → `outcome=UNKNOWN`; test ca mã 07 (R4).
  3. `services/payment-service/.../PaymentMessageListener.java`, listener Booking (`SalesConfigurationListener`, `EventCancellationListener`, `AcceptPaymentListener`, `BookingIssuanceResultListener`): RETRY sau NACK requeue, REJECTED khi từ chối đã biết (R5); test listener.
  4. `deploy/k8s/discovery-server/{configmap.yaml,statefulset.yaml}`: `ENVIRONMENT: production`; `env:` thêm `HOST_ID` (`spec.nodeName`), `OTEL_AGENT_ENABLED: "false"` (R6); `test-k8s-discovery.py`.
  5. `services/event-service/.../EventLogCustomizer.java`: bỏ `spanId` khi trùng đoạn span của MDC `traceparent` (R7); 7 `deploy/k8s/*/configmap.yaml`: bỏ 2 dòng `OTEL_INSTRUMENTATION_COMMON_LOGGING_{TRACE,SPAN}_ID_KEY` (N1, lệch SPEC C2).
  6. `services/ticket-service/.../TicketOutboxPublisher.java`, `TicketDeliveryWorker.java`, Payment `PaymentWorker.java`/`MessagingServiceImpl.java`: mã trung tính cho lỗi không thuộc broker, `retryCount = attempt − 1`, chỉ ở log (R8).
  7. Booking `OrderController.java`: trả `X-Correlation-Id` = orderId khi tạo đơn; `GlobalExceptionHandler.java`: cùng mã cho MDC và phản hồi (R3); kiểm gateway có giữ header trả về.
  8. Kiểm lại: `verify` + B16 các service đổi, Booking `-P rca-test` và `-P integration`, bộ kiểm K8s, `test-ticket-replica.sh` (cần Docker), lượt agent `tat-secret-true` nếu đổi entrypoint/manifest Booking; push có lease `2a275b5` (cần Minh duyệt push).
  9. Hồ sơ: `results/T-076/kiem-cuc-bo/README.md` sửa câu "CI GitHub chạy dòng ADD" (R9a); `results/T-076/mo-ta-pr17.md` cập nhật theo bản sửa.
- **Chờ Minh quyết:** (a) hỏi nhóm trạng thái reader ba service trên 84 (R2) — đề xuất: hỏi trước khi sửa xong để chọn giờ merge; nếu đang bật, nhóm về writer trên digest hiện tại trước merge; (b) phạm vi sửa: đề xuất cả 1–9 một vòng (mỗi lần merge cần hẹn nhóm; tách vòng tốn thêm chờ); N1 cần duyệt riêng vì lệch SPEC C2; (c) bật Docker cho bước kiểm.
- **Bước tiếp:** Minh duyệt phạm vi sửa; hoặc gửi prompt dưới cho Codex kiểm phản hồi (`REVIEW-6.md`). Lệnh cuối: đọc `/srv/flashticket-rca/alerts/bo-nhan/webhook.jsonl` trên obs (phục vụ T-070 R3).

Prompt cho Codex kiểm lại phản hồi REVIEW-5 (Minh chuyển):

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/ (SPEC.md bản 6).
- Công đoạn: kiểm lại phản hồi của người làm cho REVIEW-5 (bước 5 Phần A, PR #17 trước merge). Chưa có bản sửa nào được Minh duyệt; các đề xuất sửa nằm trong LOG mục 28/11.
- Gói/cổng: P9/P10, việc tích hợp ngoài G0–G4; không kèm khối trọng tâm cổng.
- Người làm và người phản biện chính thức: người làm Claude, người phản biện Codex.
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,LOG.md}; results/T-076/bang-file-pr17.md; results/T-076/mo-ta-pr17.md; results/T-076/kiem-cuc-bo/ (README từng lượt); docs/architecture/B16-observability-baseline.md và deploy/observability/log.schema.json trong repo FlashTicket; DT18, hướng dẫn của cô, MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md, REVIEW-2.md, REVIEW-3.md, REVIEW-4.md, REVIEW-5.md (bảng "Phản hồi của người làm" ở cuối mỗi bản, gồm N1, N2 ở REVIEW-5).
- Code và kết quả liên quan: repo FlashTicket D:/Project/flash-ticket-platform, PR #17 https://github.com/levanminh04/flash-ticket-platform/pull/17 (nhánh rca/quan-sat-log @2a275b5, gốc origin/main 6b77144); worktree D:/Project/ft-pr17-dung-lai cùng commit; git diff 6b77144 2a275b5; CI run 46013069317. Chỉ đọc. Không vào máy 84, exp-app, obs.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-076-pr17-otel-may-84/REVIEW-6.md (chưa có; theo mẫu tasks/_MAU/REVIEW.md). Không sửa file nào khác, không bình luận lên PR.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Không dùng subagent (Minh dặn ngày 24/11).
```
- 28/11 — **Minh "Duyệt sửa cả hai"**: duyệt đề xuất sửa 1–9 (gồm N1) ở mục Phiên 6. Push lên PR vẫn cần Minh duyệt riêng.
- 28/11 — **Sửa theo REVIEW-5 xong (local, chưa push).** Commit `f29073f` (28 file) trên `2a275b5`, nhánh local `rca/quan-sat-log-dung-lai`. Chi tiết và kết quả: `results/T-076/kiem-cuc-bo/sua-review-5/README.md`.
  - Sửa đúng 1–9 đã duyệt (R1, R3, R4, R5, R6, R7, R8, N1; R9a sửa câu `results/T-076/kiem-cuc-bo/README.md`). R3 không thêm dòng log liên kết riêng: gateway giữ `X-Correlation-Id` do Booking trả (`CorrelationIdFilter` beforeCommit), nên tạo đơn trả orderId là đủ để gateway ghi orderId; trong Booking, nối mã tạm → orderId qua `requestId`. Câu cùng nội dung trong chú thích `results/T-076/kiem-cuc-bo/agent/build-image.sh:4` để nguyên (ngoài phạm vi duyệt).
  - Kiểm: `verify` + B16 payment 144, event 179, ticket 229, booking 457 (0 lỗi); `-P rca-test` Event 187, Booking 466; Booking `-P integration` 173 failsafe (`BookingPersistenceIT` 157) đạt — lần đầu chạy profile này sau R1; `TicketPostgresIT` 22; bộ kiểm K8s 4/4; agent `tat-secret-true` image `f29073f`: `false`, 0 dòng agent, 0 byte, 416 MiB.
  - `test-ticket-replica.sh` (R9b): script nhóm hỏng trên laptop hai chỗ (RabbitMQ eacces; chờ `ping` chưa đủ, `add_vhost` lỗi). Bản sao tạm khác 2 dòng (`--user 999:999`, `check_running`) chạy được ở lần thử thứ 3; đã xóa bản sao. `run … TicketPostgresIT,TicketSagaBrokerIT` 25 đạt; `run verify` 4 failure `TicketLocalConfigurationTests` — main `6b77144` cùng env cũng 4 failure (giới hạn công thức, không do PR). Lỗi chờ RabbitMQ trong script của main: báo nhóm, không sửa trong PR.
  - `results/T-076/mo-ta-pr17.md`: thêm mục "Sửa sau phản biện" và điều kiện reader trước merge.
  - **Chưa kiểm:** tuyến K8s thật và trạng thái reader trên 84 (R2, bước 6–7); Event khi agent bật (thứ tự MDC); đối chứng IT Booking trên `2a275b5`.
  - **Chờ Minh:** (a) duyệt push `f29073f` lên PR (`git push --force-with-lease=rca/quan-sat-log:2a275b5… origin rca/quan-sat-log-dung-lai:rca/quan-sat-log` là đẩy tiến, lease vẫn đặt để chặn thay đổi lạ), rồi `gh pr edit 17` theo `mo-ta-pr17.md`; (b) hỏi nhóm trạng thái reader (R2); (c) gửi prompt dưới cho Codex (`REVIEW-6.md`); (d) commit repo RCA.
  - Lệnh cuối: `chay-agent-v6.sh … sua-review-5 tat-secret-true true`.

Prompt cho Codex kiểm lại phản hồi và bản sửa REVIEW-5 (thay prompt mục Phiên 6; Minh chuyển):

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/ (SPEC.md bản 6).
- Công đoạn: kiểm lại phản hồi của người làm và bản sửa cho REVIEW-5 (bước 5 Phần A, PR #17 trước merge). Minh duyệt sửa 1–9 ngày 28/11; bản sửa là commit f29073f trên nhánh local, chưa push lên PR.
- Gói/cổng: P9/P10, việc tích hợp ngoài G0–G4; không kèm khối trọng tâm cổng.
- Người làm và người phản biện chính thức: người làm Claude, người phản biện Codex.
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,LOG.md}; results/T-076/bang-file-pr17.md; results/T-076/mo-ta-pr17.md; results/T-076/kiem-cuc-bo/ (README từng lượt, gồm sua-review-5/); docs/architecture/B16-observability-baseline.md và deploy/observability/log.schema.json trong repo FlashTicket; DT18, hướng dẫn của cô, MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md, REVIEW-2.md, REVIEW-3.md, REVIEW-4.md, REVIEW-5.md (bảng "Phản hồi của người làm" ở cuối mỗi bản, gồm N1, N2 ở REVIEW-5).
- Code và kết quả liên quan: repo FlashTicket D:/Project/flash-ticket-platform; worktree D:/Project/ft-pr17-dung-lai nhánh local rca/quan-sat-log-dung-lai @f29073f (git diff 2a275b5 f29073f là bản sửa; git diff 6b77144 f29073f là toàn PR); PR #17 https://github.com/levanminh04/flash-ticket-platform/pull/17 còn ở 2a275b5; CI run 46013069317 của 2a275b5. Chỉ đọc. Không vào máy 84, exp-app, obs.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-076-pr17-otel-may-84/REVIEW-6.md (chưa có; theo mẫu tasks/_MAU/REVIEW.md). Không sửa file nào khác, không bình luận lên PR.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Không dùng subagent (Minh dặn ngày 24/11).
```
- 28/11 — **Minh "Duyệt push"** (đẩy `f29073f` lên PR). `git fetch`: `origin/main` lại tiến `6b77144` → `4d57225` (PR #58: Payment đọc báo cáo qua replica, 2 pod HA; 40 file). PR vẫn `2a275b5`. **Chưa push**: `git merge-tree --write-tree origin/main rca/quan-sat-log-dung-lai` có 1 xung đột `services/payment-service/.env.example` (main thêm khối `PAYMENT_REPORT_REPLICA_*`, nhánh thêm khối `OTEL_*`, cùng cuối file; gỡ: giữ cả hai). 8 file Payment trùng (gồm `PaymentService.java`, `RefundServiceImpl.java`, `application.yaml`, `deployment.yaml`, `pom.xml`) tự gộp. CD main có guard writer/cùng digest cho Payment → R2 áp cả Payment. Đẩy `f29073f` lúc này để PR xung đột, CI pull_request không chạy. Trình lại Minh: rebase lên `4d57225`, gỡ xung đột, kiểm lại phần Payment (`verify` + B16, manifest, bộ kiểm K8s), rồi push có lease `2a275b5`.
- 28/11 — **Minh "Duyệt rebase, push"**: rebase lên `4d57225`, gỡ xung đột `.env.example` Payment (giữ cả hai khối), kiểm lại Payment/manifest/K8s, push `--force-with-lease` khớp `2a275b5`.
- 28/11 — **Rebase lên `4d57225` và push xong.** Bản cũ giữ ở nhánh local `rca/quan-sat-log-6b77144` @`f29073f`. Xung đột `services/payment-service/.env.example`: giữ khối replica của main, thêm khối `OTEL_*`. `git range-diff`: 7 commit trùng, 1 commit (agent) chỉ đổi file đó. Kiểm (`results/T-076/kiem-cuc-bo/sua-review-5/main-4d57225/README.md`): Payment `verify` 153 + 57 (failsafe mới của main), 0 lỗi, B16 đạt; manifest 8 service đạt; bộ kiểm K8s 4/4 (gồm fixture Payment HA); quét bí mật 0. `git fetch` trước push: main `4d57225`, PR `2a275b5` khớp. `git push --force-with-lease=rca/quan-sat-log:2a275b5… origin rca/quan-sat-log-dung-lai:rca/quan-sat-log` → `2a275b5...f40b849 (forced update)`. `gh pr edit 17` theo `results/T-076/mo-ta-pr17.md` (gốc `4d57225`, mục sửa sau phản biện, điều kiện reader cho cả Payment). PR #17: draft, MERGEABLE; CI đang chạy lúc ghi.
  - **Chờ:** CI xanh; nhóm xác nhận trạng thái reader Booking/Event/Ticket/Payment trên 84 (R2); Codex `REVIEW-6` (prompt dưới, thay các prompt T-076 trước); commit repo RCA. Main còn tiến thì lặp rebase.
  - Lệnh cuối: `gh pr edit 17 --title … --body-file …`.

Prompt cho Codex kiểm lại phản hồi và bản sửa REVIEW-5 trên PR (bản dùng; Minh chuyển):

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/ (SPEC.md bản 6).
- Công đoạn: kiểm lại phản hồi của người làm và bản sửa cho REVIEW-5 (bước 5 Phần A, PR #17 trước merge). Minh duyệt sửa 1–9 ngày 28/11; bản sửa đã rebase lên main 4d57225 và đẩy lên PR (đầu f40b849).
- Gói/cổng: P9/P10, việc tích hợp ngoài G0–G4; không kèm khối trọng tâm cổng.
- Người làm và người phản biện chính thức: người làm Claude, người phản biện Codex.
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,LOG.md}; results/T-076/bang-file-pr17.md; results/T-076/mo-ta-pr17.md; results/T-076/kiem-cuc-bo/ (README từng lượt, gồm sua-review-5/); docs/architecture/B16-observability-baseline.md và deploy/observability/log.schema.json trong repo FlashTicket; DT18, hướng dẫn của cô, MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md, REVIEW-2.md, REVIEW-3.md, REVIEW-4.md, REVIEW-5.md (bảng "Phản hồi của người làm" ở cuối mỗi bản, gồm N1, N2 ở REVIEW-5).
- Code và kết quả liên quan: repo FlashTicket D:/Project/flash-ticket-platform; PR #17 https://github.com/levanminh04/flash-ticket-platform/pull/17 nhánh rca/quan-sat-log @f40b849, gốc origin/main 4d57225; worktree D:/Project/ft-pr17-dung-lai cùng commit; git diff 4d57225 f40b849 là toàn PR; bản sửa REVIEW-5 là commit cuối (git show f40b849; bản trước rebase: nhánh local rca/quan-sat-log-6b77144 @f29073f, git diff 2a275b5 f29073f); CI của PR trên GitHub (gh pr checks 17). Chỉ đọc. Không vào máy 84, exp-app, obs.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-076-pr17-otel-may-84/REVIEW-6.md (chưa có; theo mẫu tasks/_MAU/REVIEW.md). Không sửa file nào khác, không bình luận lên PR.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Không dùng subagent (Minh dặn ngày 24/11).
```
- 28/11 — Minh "Viết cả hai": viết `results/T-076/exp-app/runbook-online.md` (nháp, Minh duyệt trước bước 10) và `results/T-076/mo-rong-may-84.md` (đầu ra SPEC).
- 28/11 — **Viết xong** `results/T-076/exp-app/runbook-online.md` (nháp) và `results/T-076/mo-rong-may-84.md` (bản 1).
  - Runbook: điều kiện D1–D8, tham số khai trước (lượt `online-demo-001`, tải 1800 s ×1, `PAUSE-PAYMENT` 600 s, N = 25 phút), bước chuẩn bị/chạy/hoàn tác theo lab hiện tại (`/opt/flashticket-rca`, `rca/online/`, `observability/alert-receiver/`), bảng gặp lỗi giữa chừng, chấm theo C6/E5. Lệnh đối chiếu với mã lab `da9c843` (tham số `orchestrator.py`, `g1_b.py --chi-khoi-tao`, `tai_linux.py start|get|stop|receive`, `inject.py start|stop|verify`, `ledger_append.py`).
  - **Đề xuất lệch SPEC (cần Minh quyết, §3 runbook):** (a) thêm integration bằng file provisioning như E5 thay vì API Grafana — API cần mật khẩu admin trong `/etc/flashticket-rca/grafana.env`, agent không đọc file bí mật; contact point do file tạo có thể không sửa được qua API (chưa kiểm); (b) sinh dashboard nguồn `online-demo-001` trên laptop, đưa vào commit lab DEMO, thay vì chạy `build_dashboards.py` trên obs (cây lab bẩn suốt lượt). Hai commit lab DEMO/HOAN-TAC chưa tạo; tạo khi Minh duyệt.
  - `mo-rong-may-84.md`: hiện trạng sau PR #17, bảng việc thêm/sửa nhỏ, số RAM máy 84 (đọc 27/11) và laptop (bản 3 +118 MiB, bản 6 +75…+106 MiB), điều kiện OPEN (sentinel, biên lọc B16 §6, đo dưới tải, phí egress AWS, guard reader của CD, thứ tự MDC Event).
  - Tự kiểm: đối chiếu đường dẫn, tên lệnh với mã lab; số RAM với LOG dòng 336–338 và README bản 3/6; B16 §6 dòng 91. **Chưa kiểm:** cách file provisioning trên bố cục lab mới; tên container payment và máy đặt sổ tiêm trên bản demo (bước 8).
  - **Chờ Minh:** duyệt hoặc sửa runbook (gồm hai điểm lệch); gửi prompt dưới cho Codex.
  - Lệnh cuối: `grep -n "^## " B16-observability-baseline.md`.

Prompt cho Codex soát runbook-online.md và mo-rong-may-84.md (Minh chuyển; gửi sau hoặc cùng lúc với prompt REVIEW-5 ở trên):

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/ (SPEC.md bản 6); hai đầu ra mới: results/T-076/exp-app/runbook-online.md (nháp, cần Minh duyệt trước bước 10) và results/T-076/mo-rong-may-84.md.
- Công đoạn: soát kết quả — hai đầu ra trên (runbook là kế hoạch vận hành bước 10, chưa chạy bước nào).
- Gói/cổng: P9/P10, việc tích hợp ngoài G0–G4; không kèm khối trọng tâm cổng.
- Người làm và người phản biện chính thức: người làm Claude, người phản biện Codex.
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,LOG.md}; results/T-073/khai-truoc-e5.json, results/T-073/trien-khai-e5.md; results/T-070/don/ (Q4); tasks/T-070-dieu-phoi-giai-doan-2/REVIEW-5.md; results/T-076/kiem-cuc-bo/ (README từng lượt); docs/architecture/B16-observability-baseline.md trong repo FlashTicket; DT18, hướng dẫn của cô, MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md … REVIEW-5.md (bảng phản hồi ở cuối mỗi bản). Hai file này chưa được phản biện lần nào.
- Code và kết quả liên quan: repo lab D:/Project/flashticket-rca-lab @da9c843 (rca/online/, observability/alert-receiver/, observability/grafana/{build_dashboards.py,provisioning/}, faults/injectors/docker/inject.py, load/controller/tai_linux.py, rca/lib/ledger_append.py); repo FlashTicket PR #17 @f40b849 (deploy/k8s/, deploy/scripts/deploy-k8s-service.sh). Chỉ đọc. Không vào máy 84, exp-app, obs.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-076-pr17-otel-may-84/REVIEW-7.md nếu REVIEW-6.md đã có, hoặc REVIEW-6.md nếu chưa có (liệt kê thư mục trước khi chọn tên; theo mẫu tasks/_MAU/REVIEW.md). Không sửa file nào khác.

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

Công đoạn: soát kết quả.
Kiểm trên đầu ra thật, code và dữ liệu được phép; không tin tóm tắt LOG. Đối chiếu tiêu chí xong với phần mục tiêu nguồn và mức căn cứ cho bước tiếp theo; chạy lại phần rẻ khi trong quyền được duyệt.
Phân biệt hoàn thành task mô tả, xác nhận cơ chế và đủ căn cứ chọn/đánh giá thiết kế. Giới hạn đã khai không tự miễn phép kiểm cần thiết còn làm được.
Chỉ ghi bản phản biện lượt được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ bản cũ; không sửa kết quả thay người làm.

Không dùng subagent (Minh dặn ngày 24/11).
```
- 28/11 — Minh yêu cầu "mở phiên khác và yêu cầu phản biện độc lập" (ưu tiên đúng đắn, rồi thuận tiện, dễ return/back/move, ít sửa). Mở phiên Claude mới `phan-bien-runbook` (`local_b4507e4d-2458-4b4c-b0cb-32179071ca4e`), context fresh, dùng chung checkout, **chỉ đọc**, trả lời trong chat của phiên đó; soát `exp-app/runbook-online.md`, `mo-rong-may-84.md`, gồm hai điểm lệch SPEC §3. Cùng loại agent với người làm nên là đầu vào bổ sung, không thay phản biện chính thức của Codex (AGENTS §1). Brief: Prompt chung + khối "Soát kết quả" của `docs/review-prompt.md`, thêm yêu cầu nguyên văn của Minh.
- 28/11 — **Minh "Duyệt sửa runbook, mo-rong và đổi tên đường dẫn"**: sửa `runbook-online.md` theo F1–F8 của phiên phản biện bổ sung, sửa 3 chỗ `mo-rong-may-84.md`, đổi đường dẫn bộ nhận `/t073/canh-bao` trong lab (3 file) và URL trong runbook.
- 28/11 — **Phiên phản biện bổ sung** `phan-bien-runbook` xong (chỉ đọc; kết quả trong chat của phiên đó). F1 CHẶN duyệt runbook: B9 kiểm "không có sự cố he-thong đang mở" bằng log và bỏ khoảng ghép 300 s — lặp lỗi REVIEW-4 R3. F2–F8 không chặn: STOP không làm `orchestrator.py` thoát; thiếu `/srv/flashticket-rca/runs/STOP`; giờ sổ tiêm gõ tay, máy sổ chưa rõ; thiếu đường hầm cổng 3000 và phiên Grafana của Minh; tải 1800 s không đủ khi tiêm muộn; lệnh restart Grafana chưa rõ; §3 thiếu hai điểm lệch SPEC (gốc lab, phạm vi ghi `observability/grafana/`). `mo-rong-may-84.md`: 3 sửa nhỏ. Hai điểm Minh quyết: phiên này cũng đề xuất file provisioning; thêm phương án nạp lại bằng API reload (chưa kiểm). Người làm kiểm lại F1 (`incidents.py:172–174,193–194`; Q4 `canh-bao-nhan.out`: p95 hết muộn nhất 03:29:28Z = giây 483) và F2 (`orchestrator.py:216–228`): đúng.
- 28/11 — **Sửa xong (chưa commit):**
  - Lab, cây làm việc trên `da9c843`: đường dẫn bộ nhận `/t073/canh-bao` → `/canh-bao` ở `rca/online/webhook_receiver.py` (mặc định, docstring), `observability/alert-receiver/compose.yaml` (lệnh, healthcheck, chú thích), `rca/online/README.md`; `git grep t073/canh-bao` còn 0; không chỗ nào đọc spool lọc theo đường dẫn. `py_compile`, YAML hợp lệ. **Phát hiện:** `webhook_receiver.py` có sẵn 5 dòng chú thích chưa commit không do người làm viết (sửa lúc 11:40 ngày 28/11: "spool đơn giản là một thư mục…", "Dùng JSONL vì…", "Ghi cảnh báo vào file"); giữ nguyên, không đưa vào commit khi chưa hỏi Minh. Đường dẫn `/t072` của bộ nhận nhẹ giữ (contact point trong `rules.yaml` do script T-072 sinh, không sửa tay).
  - `results/T-076/exp-app/runbook-online.md` bản 2: F1 (B9 kiểm trên `su-co/*.json`: không ca `he-thong` mở, giờ tiêm > `t_het` lớn nhất + 300 s; ca nền ghi riêng; quá giây 900 → "nền chưa sạch"; lệnh thử trên file sự cố giả: đúng ba ca rỗng/đã hết/còn mở), F2 (C1 SIGTERM sau STOP như E5), F3 (D6), F4 (B10 sổ trên obs, giờ obs, ghi trước lệnh tiêm và đầu ra tiêm như `e5_luot.sh`), F5 (D9), F6 (`--seconds 2100`, thời lượng 51–65 phút), F7 (`docker restart flash-ticket-obs-grafana`), F8 (§3 năm điểm lệch SPEC, phương án reload), URL `/canh-bao`.
  - `results/T-076/mo-rong-may-84.md`: dòng Discovery cần khối `OTEL_*` nếu bật; câu suy luận RAM chỉ cho Booking (Payment, Event chưa đo); chú thích "nhóm đang triển khai lúc đọc".
  - **Chờ Minh:** 5 dòng chú thích lạ trong `webhook_receiver.py`; commit lab (sửa đường dẫn, gộp với `da9c843`); duyệt runbook bản 2; gửi Codex prompt soát (cuối LOG) nếu muốn phản biện chính thức.
  - Lệnh cuối: thử lệnh B9 trên `su-co/` giả.
- 28/11 — Minh: 5 dòng chú thích trong `webhook_receiver.py` là của Minh, "cho cả vào commit". Lab commit local `94bb11e` trên `da9c843` (đường dẫn `/canh-bao` + chú thích của Minh; 3 file). Chưa push, chưa triển khai. Kiểm `receiver.env` trên obs theo phản hồi Codex: `T073_SPOOL_DIR` còn giá trị giữ chỗ `/srv/rca-lab/runs/t073-khong-dung-o-e3/spool` — đúng theo kế hoạch dọn dòng 304 (chỉ sửa `T072_RA_DIR`); không ảnh hưởng bộ nhận nhẹ; runbook A3 tạo env riêng cho lượt.
- 28/11 — Minh duyệt soạn lại prompt: prompt dưới thay prompt soát runbook bản 1 (Codex ghi `REVIEW-7.md`). Prompt kiểm bản sửa PR #17 (`REVIEW-6.md`, mục "Rebase lên `4d57225` và push xong") vẫn dùng: PR còn ở `f40b849`; main đã tiến `f0a5d30`, PR vẫn gộp sạch.

Prompt cho Codex soát runbook-online.md bản 2 và mo-rong-may-84.md (bản dùng; Minh chuyển):

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/ (SPEC.md bản 6). Hai đầu ra cần soát: results/T-076/exp-app/runbook-online.md bản 2 (nháp, chưa chạy bước nào, Minh phải duyệt trước bước 10) và results/T-076/mo-rong-may-84.md.
- Công đoạn: soát kết quả — hai đầu ra trên. Chưa có lượt phản biện chính thức nào cho hai file này.
- Gói/cổng: P9/P10, việc tích hợp ngoài G0–G4; không kèm khối trọng tâm cổng.
- Người làm và người phản biện chính thức: người làm Claude, người phản biện Codex.
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,LOG.md}; results/T-073/khai-truoc-e5.json, results/T-073/trien-khai-e5.md, results/T-073/e5/; results/T-070/don/ (Q4); tasks/T-070-dieu-phoi-giai-doan-2/REVIEW-5.md; results/T-076/kiem-cuc-bo/ (README từng lượt); docs/architecture/B16-observability-baseline.md trong repo FlashTicket; DT18, hướng dẫn của cô, MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md … REVIEW-5.md (bảng phản hồi ở cuối mỗi bản); lượt phản biện bổ sung 28/11 do một phiên Claude chỉ đọc (cùng loại agent với người làm; kết quả trong chat của phiên đó, tóm tắt và phần người làm kiểm lại ở LOG T-076 mục 28/11, các điểm F1–F8).
- Code và kết quả liên quan: repo lab D:/Project/flashticket-rca-lab @94bb11e (local, chưa push; máy đang ở c1da15f): rca/online/, observability/alert-receiver/, observability/grafana/{build_dashboards.py,provisioning/}, observability/compose.yaml, faults/injectors/docker/inject.py, load/controller/tai_linux.py, rca/lib/ledger_append.py; repo FlashTicket PR #17 @f40b849 (deploy/k8s/, deploy/scripts/deploy-k8s-service.sh). Chỉ đọc. Không vào máy 84, exp-app, obs.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-076-pr17-otel-may-84/REVIEW-7.md (REVIEW-6.md dành cho lượt kiểm bản sửa PR #17; theo mẫu tasks/_MAU/REVIEW.md). Không sửa file nào khác.

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

Công đoạn: soát kết quả.
Kiểm trên đầu ra thật, code và dữ liệu được phép; không tin tóm tắt LOG. Đối chiếu tiêu chí xong với phần mục tiêu nguồn và mức căn cứ cho bước tiếp theo; chạy lại phần rẻ khi trong quyền được duyệt.
Phân biệt hoàn thành task mô tả, xác nhận cơ chế và đủ căn cứ chọn/đánh giá thiết kế. Giới hạn đã khai không tự miễn phép kiểm cần thiết còn làm được.
Chỉ ghi bản phản biện lượt được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ bản cũ; không sửa kết quả thay người làm.

Yêu cầu riêng của Minh cho lượt soát hai file này (nguyên văn, 28/11/2026): "tôi muốn có sự thuận tiện nhất có thể, dễ dàng return, back, move mà tối thiểu hóa việc sửa, tính đúng đắn vẫn ưu tiên trên hết". Runbook §3 liệt kê các điểm lệch SPEC Minh cần quyết; đánh giá từng điểm theo thứ tự ưu tiên đó, nêu đề xuất, mặt trái và phần chưa kiểm được.

Không dùng subagent (Minh dặn ngày 24/11).
```

## Phiên 7 — 28/11/2026, Claude, laptop, người làm

- 28/11 — Minh giao Claude chạy Codex CLI (`codex exec`, `gpt-6.2-astra`, effort high) với nguyên văn 3 prompt chờ gửi, tuần tự. Lượt 1 (prompt REVIEW-6, mục "Rebase lên `4d57225` và push xong") chạy 06:37:36Z–06:48:20Z, Codex ghi `REVIEW-6.md` (R1–R5); so `git status` 4 repo trước/sau: chỉ thêm file đó. Lượt 2 (prompt REVIEW-7) hỏng lúc 06:50:59Z: Codex hết usage, không ghi file (giữ `r2.jsonl` ở scratchpad phiên). Lượt 3 (T-070 REVIEW-6) chưa chạy.
- 28/11 — **Lệch §5.7:** người làm đọc kết luận REVIEW-6 trước rồi kiểm trên code, không tự soát gốc trước. Kiểm từng điểm trên worktree `f40b849` và main `f0a5d30`: R1–R5 đúng (bảng cuối `REVIEW-6.md`).
- 28/11 — Minh "Duyệt ghi và sửa": điền bảng phản hồi REVIEW-6; sửa R1–R5 trên PR #17 theo đề xuất trong chat (rebase lên `f0a5d30`; R2 mục Hoàn tác `mo-ta-pr17.md`; R3 bắt `ShutdownSignalException` ở 5 hàm bọc Payment; R4 sự kiện `order.correlation-linked`; R5 outbox không dời lịch được → `UNKNOWN/LEASE_CHANGED`, sửa message Payment). Push và sửa body PR chưa duyệt.
- 28/11 — **Sửa REVIEW-6 xong** (worktree `D:/Project/ft-pr17-dung-lai`, nhánh `rca/quan-sat-log-dung-lai`).
  - Commit `943962b` trên `f40b849`. `git rebase origin/main` lên `f0a5d30`, không xung đột → `cd21f17`. `git range-diff`: 8 commit trùng, thêm 1.
  - Sửa: R3 Payment listener bắt `ShutdownSignalException` cùng `IOException` → `UNKNOWN/BROKER_COMMAND_FAILED`. R4 Booking `order.correlation-linked`, `reasonCode=ORDER_CORRELATION_ASSIGNED` (tên mã lý do người làm đặt khi sửa). R5 `rescheduleOutbox` trả boolean, Ticket lấy số hàng dời lịch; 0 → `UNKNOWN/LEASE_CHANGED`; message Payment theo bước. R2 `results/T-076/mo-ta-pr17.md`: mục Hoàn tác viết lại, gốc `f0a5d30`, thêm dòng sửa REVIEW-6. R1: rebase như trên.
  - Kiểm (`results/T-076/kiem-cuc-bo/sua-review-6/README.md`): payment 157 + 57, ticket 229 + `TicketPostgresIT` 23, booking 457, rca-test 466, integration 457 + 173, 0 lỗi; B16 PASS 3/3. Bộ kiểm K8s lượt 1 hỏng hạ tầng (venv không có `yaml`, giữ log); lượt 2 `py -3` 4/4 đạt trên `f0a5d30`.
  - Không làm: push, `gh pr edit` (chờ Minh duyệt). Không sửa SPEC C4. Codex nêu "44 file Java ngoài test" ở bước 5 nay là 46 (bảng file chưa cập nhật, chưa được duyệt sửa).
  - **Chờ Minh:** duyệt push `cd21f17` lên `rca/quan-sat-log` (`--force-with-lease` trên `f40b849`) và sửa body PR theo `mo-ta-pr17.md`; gửi prompt dưới cho Codex (`REVIEW-8`); chạy lại prompt `REVIEW-7` (runbook) khi Codex có usage; nhóm xác nhận reader trên 84.
  - Lệnh cuối: `py -3 .github/scripts/test-k8s-rollout-hooks.py` (lượt 2 bộ kiểm K8s).
  - Bước tiếp theo: sau duyệt push — `git fetch`, kiểm `origin/rca/quan-sat-log` = `f40b849` và main chưa tiến; `git push --force-with-lease=rca/quan-sat-log:f40b849… origin rca/quan-sat-log-dung-lai:rca/quan-sat-log`; `gh pr edit 17 --body-file` (bỏ tiêu đề dòng 1).

Prompt cho Codex kiểm lại phản hồi và bản sửa REVIEW-6 (bản dùng; Minh chuyển):

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/ (SPEC.md bản 6).
- Công đoạn: kiểm lại phản hồi của người làm và bản sửa cho REVIEW-6 (bước 5 Phần A, PR #17 trước merge). Minh duyệt ghi phản hồi và sửa R1–R5 ngày 28/11; bản sửa rebase lên main f0a5d30, commit local cd21f17 trên nhánh rca/quan-sat-log-dung-lai, chưa push (PR #17 trên GitHub vẫn ở f40b849).
- Gói/cổng: P9/P10, việc tích hợp ngoài G0–G4; không kèm khối trọng tâm cổng.
- Người làm và người phản biện chính thức: người làm Claude, người phản biện Codex.
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,LOG.md}; results/T-076/bang-file-pr17.md; results/T-076/mo-ta-pr17.md; results/T-076/kiem-cuc-bo/ (README từng lượt, gồm sua-review-5/ và sua-review-6/); docs/architecture/B16-observability-baseline.md và deploy/observability/log.schema.json trong repo FlashTicket; DT18, hướng dẫn của cô, MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md, REVIEW-2.md, REVIEW-3.md, REVIEW-4.md, REVIEW-5.md, REVIEW-6.md (bảng "Phản hồi của người làm" ở cuối mỗi bản).
- Code và kết quả liên quan: repo FlashTicket D:/Project/flash-ticket-platform, origin/main f0a5d30; worktree D:/Project/ft-pr17-dung-lai nhánh rca/quan-sat-log-dung-lai @cd21f17 (local, chưa push); git diff f0a5d30 cd21f17 là toàn PR sau sửa; bản sửa REVIEW-6 là commit cuối (git show cd21f17); git range-diff 4d57225..f40b849 f0a5d30..cd21f17; PR #17 https://github.com/levanminh04/flash-ticket-platform/pull/17 (đầu f40b849, CI của đầu cũ). Chỉ đọc. Không vào máy 84, exp-app, obs.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-076-pr17-otel-may-84/REVIEW-8.md (chưa có; REVIEW-7.md dành cho lượt soát runbook-online.md và mo-rong-may-84.md; theo mẫu tasks/_MAU/REVIEW.md). Không sửa file nào khác, không bình luận lên PR.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Không dùng subagent (Minh dặn ngày 24/11).
```
- 28/11 — Minh "Duyệt push". `git fetch`: PR `f40b849`, main `f0a5d30` (chưa tiến). `git push --force-with-lease=rca/quan-sat-log:f40b849… origin rca/quan-sat-log-dung-lai:rca/quan-sat-log` → `f40b849...cd21f17 (forced update)`. `gh pr edit 17 --body-file` (bỏ dòng tiêu đề của `mo-ta-pr17.md`); body đọc lại khớp file (chỉ khác dòng trống cuối). PR #17: draft, OPEN, head `cd21f17`; CI run 46127267478 bắt đầu 08:45Z.
  - **Chờ:** CI xanh; Codex `REVIEW-8` (prompt ở mục trên); Codex `REVIEW-7` chạy lại; nhóm xác nhận reader trên 84; commit repo RCA.
  - Lệnh cuối: `gh pr checks 17`.
- 28/11 — Codex CLI lượt 2 (REVIEW-7): lần thử 08:46:43Z hỏng (vẫn hết usage); lần 08:47:11Z–09:02:33Z xong, chỉ ghi `REVIEW-7.md` (R1–R9; so `git status` 4 repo). Lượt 3 (T-070 REVIEW-6) 09:03:01Z hỏng: hết usage tới 20:47 giờ VN, không ghi file. CI PR #17 @`cd21f17`: 14 pass, 1 skipping.
- 28/11 — **Lệch §5.7 (như REVIEW-6):** đọc kết luận REVIEW-7 rồi kiểm trên mã/dữ liệu (`q4/canh-bao-nhan.out` dòng 14, `g1_b.py:87–106,177–183`, `orchestrator.py:216–228`, `rules.yaml`, `git ls-tree 94bb11e -- observability/tls`). R1–R9 đúng.
- 28/11 — Minh "Duyệt ghi và sửa": điền bảng phản hồi REVIEW-7; viết `runbook-online.md` bản 3 và `mo-rong-may-84.md` bản 2 theo đề xuất trong chat. Năm điểm lệch SPEC §3 vẫn là đề xuất chờ Minh duyệt cùng runbook.
- 28/11 — **Viết xong** `results/T-076/exp-app/runbook-online.md` **bản 3** và `results/T-076/mo-rong-may-84.md` **bản 2** theo REVIEW-7 (bảng phản hồi đã điền).
  - Runbook: mã lần phát `<L>` cho OUT/spool/env/tag/sổ, bộ G1 hiển thị cố định (R3); B8 `get` Running, B9 sáu mục (tải chạy, hai tín hiệu k6 như E5, spool đã đọc hết, biên ghép từ `t_het`, luật, không can thiệp tồn dư), sửa ví dụ Q4 thành giờ nhận (R1); mốc chấm = `inj.t` của `fault-start` thành công, nhánh "lỗi thao tác/chưa chấm được", B12 hai giờ (R2); khung ~75 phút (R4); chỉ nhánh file provisioning, A1/C3 ghi trạng thái trước/sau, Test cả hai integration (R5); §3.2 bảng nơi ghi theo máy (R9); D3 ghim đúng `94bb11e`.
  - Mở rộng: bảng §2 thêm đường tin cậy TLS, ba file có sẵn phải sửa (bộ kiểm Tempo, datasource, script CD), Discovery `statefulset.yaml`, nguồn CA (R6); §5 thành các nhánh lọc, mặc định giữ agent tắt (R7); §3 requests/limits, §4 guard theo service, §6 đường quay lại (R8).
  - Tự kiểm: đường dẫn, tên lệnh, trường JSON đối chiếu với lab `94bb11e` (`tai_linux.py:358` lệnh/`--tag`, `inject.py:149` hạn `seconds + 5`, `inject-state/<ô>.het-han.log`, `incidents.doc_spool`, `orchestrator.py:43–53,93,216–228`, `profiles/purchase-journey.json` `gracefulStop` 90s), file E5 (8 file dẫn đều có), `khai-truoc-e5.json` (`tieu_chi/ket_qua_chuc_nang/loi_xu_ly`, `ca_nghiem_thu/so_lan`); HPA `f40b849→cd21f17` 2/2 → 1/1; sentinel email trong `bat-ghi-de/phan-tich.txt`. **Chưa kiểm:** như §7 runbook; script so bản chép G1 (A2) chưa viết.
  - **Chờ Minh:** duyệt runbook bản 3 (năm điểm lệch §3, bảng nơi ghi §3.2, khung ~75 phút) trước bước 10; gửi prompt dưới (`REVIEW-9`) và prompt `REVIEW-8` (mục trên) cho Codex; chạy lại T-070 `REVIEW-6` sau 20:47 giờ VN (Codex hết usage).
  - Lệnh cuối: `git diff f40b849 cd21f17 -- deploy/k8s/{booking-service,payment-service}/hpa.yaml`.

Prompt cho Codex kiểm lại phản hồi và bản sửa REVIEW-7 (bản dùng; Minh chuyển):

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/ (SPEC.md bản 6). Hai đầu ra: results/T-076/exp-app/runbook-online.md bản 3 (nháp, chưa chạy bước nào, Minh phải duyệt trước bước 10) và results/T-076/mo-rong-may-84.md bản 2.
- Công đoạn: kiểm lại phản hồi của người làm và bản sửa cho REVIEW-7. Minh duyệt ghi phản hồi và sửa ngày 28/11; bản 2 của runbook và bản 1 của mo-rong-may-84.md xem git show d31ad6943:<đường dẫn>.
- Gói/cổng: P9/P10, việc tích hợp ngoài G0–G4; không kèm khối trọng tâm cổng.
- Người làm và người phản biện chính thức: người làm Claude, người phản biện Codex.
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,LOG.md}; results/T-073/khai-truoc-e5.json, results/T-073/trien-khai-e5.md, results/T-073/e5/; results/T-070/don/ (Q4); tasks/T-070-dieu-phoi-giai-doan-2/REVIEW-5.md; results/T-076/kiem-cuc-bo/ (README từng lượt); docs/architecture/B16-observability-baseline.md trong repo FlashTicket; DT18, hướng dẫn của cô, MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md … REVIEW-7.md (bảng phản hồi ở cuối mỗi bản; REVIEW-6 là lượt PR); lượt phản biện bổ sung 28/11 do một phiên Claude chỉ đọc (tóm tắt và phần người làm kiểm lại ở LOG T-076 mục 28/11, các điểm F1–F8).
- Code và kết quả liên quan: repo lab D:/Project/flashticket-rca-lab @94bb11e (local, chưa push; máy đang ở c1da15f): rca/online/, observability/alert-receiver/, observability/grafana/{build_dashboards.py,provisioning/}, observability/compose.yaml, faults/injectors/docker/inject.py, load/controller/tai_linux.py, rca/lib/ledger_append.py, tests/signals/check_purchase_journey.py; repo FlashTicket PR #17 @cd21f17 trên main f0a5d30 (deploy/k8s/, deploy/scripts/deploy-k8s-service.sh). Chỉ đọc. Không vào máy 84, exp-app, obs.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-076-pr17-otel-may-84/REVIEW-9.md (chưa có; REVIEW-8.md dành cho lượt kiểm bản sửa PR #17 theo REVIEW-6; theo mẫu tasks/_MAU/REVIEW.md). Không sửa file nào khác.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Yêu cầu riêng của Minh cho các lượt soát hai file này (nguyên văn, 28/11/2026): "tôi muốn có sự thuận tiện nhất có thể, dễ dàng return, back, move mà tối thiểu hóa việc sửa, tính đúng đắn vẫn ưu tiên trên hết". Runbook §3 liệt kê các điểm lệch SPEC Minh cần quyết; đánh giá từng điểm theo thứ tự ưu tiên đó, nêu đề xuất, mặt trái và phần chưa kiểm được.

Không dùng subagent (Minh dặn ngày 24/11).
```
- 28/11 — Minh "chạy tiếp lượt codex bị ngắt": `codex exec resume 01a22182…` (cùng phiên REVIEW-8, `gpt-6.2-astra` high, workspace-write + mạng) 10:41:13Z–10:45:50Z, kèm một câu trung tính (repo có thay đổi T-070 ngoài phạm vi). Chỉ ghi `REVIEW-8.md` (R1–R4; so `git status` 4 repo). **Lệch §5.7:** đọc kết luận rồi kiểm. Kiểm: `strings` trên `CachingConnectionFactory$CachedChannelInvocationHandler.class` của `spring-rabbit-4.1.1.jar` có `Channel closed; cannot ack/nack`; CD dòng 636, 764 (HPA 1/1), 1111–1142 (các nhánh khôi phục); `PaymentWorker` thiếu `correlationId`. R1–R4 đúng. R1 cho thấy sửa REVIEW-6 R3 của người làm (bắt theo kiểu lỗi) chưa đủ.
- 28/11 — Minh "duyệt ghi và sửa". **Sửa xong** (worktree, commit local `e19fc53` trên `cd21f17`; main `f0a5d30` không đổi, không rebase):
  - R1: `RabbitTelemetry.track(channel)` (proxy JDK ghi bước ACK/NACK) + `failed()`; 5 hàm bọc của `PaymentMessageListener` dùng `telemetry.track(channel)`, một nhánh `catch (IOException | RuntimeException)`; không đổi chữ ký hàm trong (`PaymentFlowIntegrationTest`, `PaymentTwoInstanceIT` gọi trực tiếp). R4: `PaymentWorker` thêm `correlationId`. R2, R3: `results/T-076/mo-ta-pr17.md` mục Hoàn tác; thêm dòng sửa REVIEW-8.
  - Kiểm (`results/T-076/kiem-cuc-bo/sua-review-8/README.md`): test mới 10/10; cùng test với mã chính trả về `cd21f17` (`git stash` 3 file) 4 failure → phân biệt được; Payment `verify` 159 + 57, 0 lỗi; B16 PASS; `git diff --check` sạch.
  - **Chờ Minh:** duyệt push `e19fc53` (`--force-with-lease` trên `cd21f17`) và sửa body PR; Codex `REVIEW-10` (prompt dưới); commit repo RCA (gồm cả sửa T-070 REVIEW-7 đang chờ).
  - Lệnh cuối: `bash results/T-076/kiem-cuc-bo/sua-review-8/chay-verify.sh`.

Prompt cho Codex kiểm lại phản hồi và bản sửa REVIEW-8 (bản dùng nếu chưa push; Minh chuyển):

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/ (SPEC.md bản 6).
- Công đoạn: kiểm lại phản hồi của người làm và bản sửa cho REVIEW-8 (bước 5 Phần A, PR #17 trước merge). Minh duyệt ghi phản hồi và sửa R1–R4 ngày 28/11; main f0a5d30 không đổi nên không rebase; bản sửa là commit local e19fc53 trên cd21f17 (nhánh rca/quan-sat-log-dung-lai), chưa push (PR #17 trên GitHub vẫn ở cd21f17).
- Gói/cổng: P9/P10, việc tích hợp ngoài G0–G4; không kèm khối trọng tâm cổng.
- Người làm và người phản biện chính thức: người làm Claude, người phản biện Codex.
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,LOG.md}; results/T-076/bang-file-pr17.md; results/T-076/mo-ta-pr17.md; results/T-076/kiem-cuc-bo/ (README từng lượt, gồm sua-review-6/ và sua-review-8/); docs/architecture/B16-observability-baseline.md và deploy/observability/log.schema.json trong repo FlashTicket; DT18, hướng dẫn của cô, MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md, REVIEW-2.md … REVIEW-6.md, REVIEW-8.md (bảng "Phản hồi của người làm" ở cuối mỗi bản; REVIEW-7 là lượt soát runbook riêng).
- Code và kết quả liên quan: repo FlashTicket D:/Project/flash-ticket-platform, origin/main f0a5d30; worktree D:/Project/ft-pr17-dung-lai nhánh rca/quan-sat-log-dung-lai @e19fc53 (local, chưa push); git diff f0a5d30 e19fc53 là toàn PR sau sửa; bản sửa REVIEW-8 là commit cuối (git show e19fc53); PR #17 https://github.com/levanminh04/flash-ticket-platform/pull/17 (đầu cd21f17, CI của đầu cũ). Chỉ đọc. Không vào máy 84, exp-app, obs.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-076-pr17-otel-may-84/REVIEW-10.md (chưa có; REVIEW-9.md dành cho lượt soát runbook-online.md bản cuối; theo mẫu tasks/_MAU/REVIEW.md). Không sửa file nào khác, không bình luận lên PR.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Không dùng subagent (Minh dặn ngày 24/11).
```
- 28/11 — Minh "Duyệt push, commit". `git fetch`: PR `cd21f17`, main `f0a5d30`. `git push --force-with-lease=rca/quan-sat-log:cd21f17… origin rca/quan-sat-log-dung-lai:rca/quan-sat-log` → `cd21f17..e19fc53` (fast-forward). `gh pr edit 17 --body-file` theo `mo-ta-pr17.md` (bỏ dòng tiêu đề); body đọc lại khớp (chỉ khác dòng trống cuối). PR #17 draft, OPEN, head `e19fc53`; CI bắt đầu ~11:47Z. Prompt `REVIEW-10` ở trên ghi "chưa push": **bản dùng** là bản dưới (chỉ đổi thông tin revision).
  - Lệnh cuối: `gh pr view 17 --json headRefOid,isDraft,state`.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-076, tasks/T-076-pr17-otel-may-84/ (SPEC.md bản 6).
- Công đoạn: kiểm lại phản hồi của người làm và bản sửa cho REVIEW-8 (bước 5 Phần A, PR #17 trước merge). Minh duyệt ghi phản hồi và sửa R1–R4 ngày 28/11; main f0a5d30 không đổi nên không rebase; bản sửa là commit e19fc53 trên cd21f17, đã push lên PR #17 (nhánh rca/quan-sat-log, đầu e19fc53).
- Gói/cổng: P9/P10, việc tích hợp ngoài G0–G4; không kèm khối trọng tâm cổng.
- Người làm và người phản biện chính thức: người làm Claude, người phản biện Codex.
- Tài liệu gốc: tasks/T-076-pr17-otel-may-84/{SPEC.md,LOG.md}; results/T-076/bang-file-pr17.md; results/T-076/mo-ta-pr17.md; results/T-076/kiem-cuc-bo/ (README từng lượt, gồm sua-review-6/ và sua-review-8/); docs/architecture/B16-observability-baseline.md và deploy/observability/log.schema.json trong repo FlashTicket; DT18, hướng dẫn của cô, MRP P9/P10.
- Phản biện và phản hồi trước: tasks/T-076-pr17-otel-may-84/REVIEW.md, REVIEW-2.md … REVIEW-6.md, REVIEW-8.md (bảng "Phản hồi của người làm" ở cuối mỗi bản; REVIEW-7 là lượt soát runbook riêng).
- Code và kết quả liên quan: repo FlashTicket D:/Project/flash-ticket-platform, origin/main f0a5d30; worktree D:/Project/ft-pr17-dung-lai nhánh rca/quan-sat-log-dung-lai @e19fc53 (cùng đầu PR); git diff f0a5d30 e19fc53 là toàn PR sau sửa; bản sửa REVIEW-8 là commit cuối (git show e19fc53); PR #17 https://github.com/levanminh04/flash-ticket-platform/pull/17 (đầu e19fc53; CI của PR trên GitHub, gh pr checks 17 hoặc REST). Chỉ đọc. Không vào máy 84, exp-app, obs.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ ghi tasks/T-076-pr17-otel-may-84/REVIEW-10.md (chưa có; REVIEW-9.md dành cho lượt soát runbook-online.md bản cuối; theo mẫu tasks/_MAU/REVIEW.md). Không sửa file nào khác, không bình luận lên PR.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Không dùng subagent (Minh dặn ngày 24/11).
```
