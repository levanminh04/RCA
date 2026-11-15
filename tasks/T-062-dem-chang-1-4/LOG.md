# Nhật ký T-062

Chỉ ghi thêm. Mỗi phiên/agent một mục: ngày giờ UTC, agent, việc, file, kiểm, việc tiếp.

## 12/11/2026 ~01:15 (giờ VN) — Claude (phiên gốc) — chuẩn bị

- Minh duyệt chạy liên tục, xem nguyên văn ở `SPEC.md`.
- Đã kiểm: `codex exec` chạy được (`codex-cli 0.167.0`, `gpt-6.1-sol`, reasoning high, đăng nhập ChatGPT); `gh` 2.103.3 cài xong, chưa đăng nhập; máy tải `3.24.8.49` SSH được (x86, 2 vCPU, 7,7 GB, chưa Docker/k6); 7 service FlashTicket `mvnw clean verify -DskipTests` đạt; `cd.yml` triển khai production khi push `main`, `ci.yml` chạy trên PR.
- Sao lưu: `D:/RCA-ext/backup-flashticket-20261112/`, `D:/RCA-ext/backup-rca-20261112/`.
- Ghi `SPEC.md`, `CHECKPOINT.md`, `PROMPT-DIEU-PHOI.md`; tạo lịch `t062-tiep-nhan`; mở phiên điều phối.

## 11/11/2026 18:30Z (12/11 01:30 VN) — Claude (phiên tiếp quản, tài khoản mới), laptop — điều phối, người làm A1/A2/D1/D2/E1/E2/B1

- Tiếp nhận từ phiên Claude gốc (dừng vì đổi tài khoản; CHECKPOINT ghi DIEU_PHOI TRỐNG). Lệnh Codex C1 của phiên gốc lỗi tách tham số, chưa chạy gì.
- Cổng: Security List Oracle Minh mở xong (8080 vào được). 8081 bị `iptables` INPUT REJECT trên exp-app (Gateway host network). Bộ phân loại an toàn của ứng dụng chặn 3 việc (mở iptables, Codex bỏ sandbox, mở phiên G1) cho tới khi Minh bật chế độ bỏ qua quyền (~18:37Z); sau đó mở 8081 cho `3.24.8.49/32` (`results/T-062/ha-tang/thay-doi.md`).
- C1 giao Codex (`results/T-062/codex/C1-brief-v3.md`): XONG (`results/T-062/tai/bao-cao-C1.md`).
- G1 giao phiên Claude riêng `t062-giao-dien`: dashboard dựng xong (`results/T-062/giao-dien/XONG.md`).
- A1: review diff 78 file sửa + 62 file mới (không thấy lỗi chặn; ghi chú trong báo cáo sáng); 6 commit nhóm trên nhánh `rca/quan-sat-log`, PR nháp levanminh04/flash-ticket-platform#17; PR xung đột với `main` (15 commit mới) → merge `origin/main` vào nhánh, gỡ 4 xung đột, build 7 service + 2 profile rca-test đạt → `6b21ed55`.
- A2: build ARM trên exp-app và triển khai 2 lượt (lượt 1 `ac331553`, lượt 2 `6b21ed55` đang dùng). `results/T-062/ha-tang/A2-kiem.md`.
- D1: Toxiproxy cố định + hook rca-test + CPU trong cgroup Booking (`results/T-062/tiem-loi/o-loi.md`).
- Lỗi nền có sẵn: route tickets 500 (thứ tự @RestControllerAdvice của Ticket), không sửa, chờ Minh.

## 12/11/2026 01:23Z — Claude (phiên tiếp quản) — kết thúc lượt chạy

**Đã làm:**
- D2 xong (`results/T-062/tiem-loi/d2-tong-hop.md`): 5 ô đạt; REDIS-BOOK bỏ; EVENT-DB-LAT hạ 200→30 ms.
- E1: 9 chu kỳ 20:39–01:20Z (`results/T-062/chay/`). Lượt E1 đầu dừng 20:37Z vì Collector ghim log theo ID container cũ (KP-19); đã sửa `include` và chạy lại.
- M1 bản khóa P7: 9/9 OK, tất định.
- E2: chuyển 0.2, băm đợt, chỉ mục, phát lại, đẩy lên exp-obs.
- B1: `results/T-062/kiem-du-lieu/bao-cao-B1.md`. G1 (phiên `t062-giao-dien`): `results/T-062/giao-dien/XONG.md`.
- Báo cáo `results/T-062/bao-cao-sang.md`, đề xuất `results/T-062/spec-chang-4-de-xuat.md`, `results/T-062/manifest.json`.

**File đã thay đổi:**
- Repo RCA: `results/T-062/**`, `tasks/T-062-dem-chang-1-4/{CHECKPOINT,LOG}.md`, dòng T-062 trong `docs/STATE.md`.
- FlashTicket: nhánh `rca/quan-sat-log` (7 commit, đã push, PR nháp #17, không merge).
- Máy: `results/T-062/ha-tang/thay-doi.md`, `tai/thay-doi-may-tai.md`, `giao-dien/thay-doi.md`.

**Kiểm đã chạy:**
- CI PR xanh (14 đạt).
- Build local 7+2 đạt.
- Health/telemetry sau triển khai.
- D2 bằng đầu dò độc lập.
- Số k6 theo pha (`chay/k6-theo-pha.md`).
- Hash adapter/config M1 khớp khóa.
- Chuỗi hash của sổ.
- B1 so T-058.

**Task đạt gì / câu hỏi trả lời tới đâu:**
- Đạt đích 1–7 của SPEC, trừ REDIS-BOOK (không xác nhận can thiệp).
- Kết quả M1 (n = 1/ô): 5/5 ô lỗi có đáp án ở hạng 1, nhưng 4/4 ca không lỗi bị kết luận `CAUSE_FOUND`. Chưa đủ để nói M1 tốt trên FlashTicket; chặng 4 phải đo phân biệt lỗi/không lỗi.
- NET-GW-BOOK cho thấy M1 không biểu diễn root là cạnh.

**Còn mở và việc chờ Minh:** `bao-cao-sang.md` §7–§8.

**Bước tiếp theo chính xác:**
1. Minh đọc `results/T-062/bao-cao-sang.md`.
2. Minh mở dashboard theo §3.
3. Quyết các mục §8.
4. Nếu chạy thêm: `py -3 -B results/T-062/chay/runner.py e1 --lich <lịch mới>` (exp-app vẫn ở topology D1), sau đó `py -3 -B results/T-062/e2.py --phat-lai --day`.

**Lệnh cuối cùng đã chạy:** `py -3 -B results/T-062/e2.py --phat-lai --day`; `py -3 -B results/T-062/bang-ket-qua.py`; `py -3 -B results/T-062/chay/k6-theo-pha.py`; `py -3 -B results/T-062/tao-manifest.py`.

**Prompt phản biện:** chưa soạn, vì Minh chưa chỉ định người phản biện (SPEC). Khi Minh chỉ định, soạn theo `docs/review-prompt.md`.


## 12/11/2026 ~02:00Z — Claude (người làm) — kiểm Grafana thật, phản biện Codex, đáp phản biện

- Minh (chat 12/11): "tôi cấp quyền cho bạn đọc mật khẩu grafana để xem dashboard và test lại, cấp cho codex nữa … hãy sử dụng codex phản biện … không xung đột với codex đang chạy". Claude không tự đăng nhập bằng mật khẩu (chính sách, SPEC luật 8) → giao Codex.
- Codex kiểm Grafana exp-obs thật, chỉ đọc (`results/T-062/codex/G1-that-brief.md`, kết quả `G1-that-ketqua.md`, `g1-that/BAO-CAO.md`, 16 ảnh): ĐẠT MỘT PHẦN — 9/9 ca hiển thị khớp nguồn; liên kết Explore từ menu nút đạt; 47/47 liên kết ở bảng bằng chứng mã hóa hai lần (lỗi G1). Đã báo phiên G1.
- Codex phản biện phần điều phối (`tasks/T-062-dem-chang-1-4/REVIEW.md`, prompt `results/T-062/codex/phan-bien-T062-prompt.txt`, chạy `-s read-only`): R1, R3, R4, R5 CHẶN; R2 không chặn. Chạy song song tối đa 2 lượt Codex.
- Đáp phản biện: điền bảng cuối REVIEW.md — R1–R5 đúng (R1: FLASH có 244×429 + 840×500, câu "không có 5xx/429" và suy luận về chế độ a trong báo cáo sáng sai); thêm N1 (đọc kết luận trước khi tự soát), N2 (`e2.py` `thanh_phan_tiem = accept[0]` gây R1 của G1), N3 (liên kết Explore bảng bằng chứng).
- **Chưa sửa file kết quả/báo cáo nào** (chờ Minh quyết). Đề xuất sửa gom theo file: `bao-cao-sang.md` bản đính chính (§1–§3), `spec-chang-4-de-xuat.md` (luật hai hướng, mẫu số 18/15, baseline, bỏ khẳng định phục hồi), `chay/HO-SO-LUOT-E1.md` (đường phục hồi), `kiem-du-lieu/kiem-r.py` + `bao-cao-B1.md` (R-05), `chay/k6-theo-pha.py` (cột 429), `e2.py` (N2). Giữ byte cũ, ghi revision mới, cập nhật manifest sau khi duyệt.
- File đã thay đổi trong mục này: `tasks/T-062-dem-chang-1-4/REVIEW.md` (chỉ bảng phản hồi), LOG, CHECKPOINT, dòng STATE; `results/T-062/codex/` (brief, prompt, log, kết quả Codex).
- Bước tiếp theo: Minh quyết sửa điểm nào; gửi prompt dưới cho Codex (kiểm lại phản hồi) nếu muốn tiếp: `Get-Content results\T-062\codex\phan-bien-T062-luot2-prompt.txt -Raw | codex exec -s read-only -C D:\RCA-flashticket -o tasks\T-062-dem-chang-1-4\REVIEW-2.md -`.

### Prompt cho người phản biện kiểm lại (Codex)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-062, tasks/T-062-dem-chang-1-4/ — phạm vi như REVIEW.md: A1, A2, B1, D1, D2, E1, E2, H1, results/T-062/bao-cao-sang.md, results/T-062/spec-chang-4-de-xuat.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: Kế hoạch giai đoạn 2 chặng 1a, 2, 3, 4 (lượt đầu), nhánh G; cổng gần nhất G4.
- Người làm và người phản biện chính thức: Người làm: Claude (phần trên), Codex (C1). Người phản biện lượt này: Codex (Minh cho phép chat 12/11/2026).
- Tài liệu gốc: như REVIEW.md mục đầu; repo RCA so với commit c3d27f8a.
- Phản biện và phản hồi trước: tasks/T-062-dem-chang-1-4/REVIEW.md (gồm bảng "Phản hồi của người làm"); mục LOG ngày 12/11/2026 ~02:00Z.
- Code và kết quả liên quan: results/T-062/ (manifest.json); results/T-062/codex/g1-that/ (kiểm Grafana thật, ngoài phạm vi chính nhưng được nhắc ở N3). Chưa có thay đổi sửa nào được duyệt hoặc thực hiện.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ file tasks/T-062-dem-chang-1-4/REVIEW-2.md, ghi bằng tùy chọn -o của lệnh chạy.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```

- ~02:45Z: Codex hết lượt khi kiểm Grafana thật bản 6 (G1). Đặt lệnh nền tự chạy lại 06:10Z (`results/T-062/codex/cho-codex-G1-that-2.sh`, brief `G1-that-2-brief.md`). Lần hỏng giữ ở `G1-that-2-lan1-het-luot.log`.

## 12/11/2026 ~13:00Z — Claude (người làm) — sửa theo REVIEW.md (Minh duyệt "duyệt sửa")

- Tác vụ nền thất bại báo trên ứng dụng: lệnh chờ chạy lại lượt Codex kiểm Grafana thật lúc 06:10Z (`codex/cho-codex-G1-that-2.sh`) bị ngắt (mã 4) do ứng dụng khởi động lại khi đang chờ; Codex chưa được gọi, không có dữ liệu mất. Chạy lại tay sau sửa.
- Bản trước sửa giữ nguyên ở `results/T-062/_ban-1/` (23 file, cùng đường dẫn tương đối).
- **R1:** `bao-cao-sang.md` bản 2 (khối đính chính đầu bài; số FLASH 244×429 + 840×500; bỏ "báo động giả"; bỏ suy luận chế độ a; câu Explore). `chay/k6-theo-pha.py` thêm cột 429, sinh lại `.md` (429 chỉ ở FLASH pha giữa). `bang-ket-qua.py` đổi chữ nhóm ca không tiêm lỗi, sinh lại `.md`.
- **R2:** `kiem-du-lieu/kiem-r.py` R-05 bản 2 tách (a) host, (b) instance thân log ↔ trace, (c) metric. Lần chạy đầu bản 2 báo thiếu host ở 32 chuỗi metric gộp `sum by(service_name)` → (a) phần metric chỉ xét kênh gốc — **sửa thêm sau khi thấy kết quả**, ghi trong `bao-cao-B1.md`. Kết quả: T-062 `a5539fba` R-05 ĐẠT (còn lệch resource log ID tĩnh; metric không có nhãn instance); T-058 `c12e47ab` THIẾU.
- **R3, R4:** `spec-chang-4-de-xuat.md` bản 2: mẫu số 18 (15) ca lỗi; luật giữ thành phần hai hướng (X xếp hạng / K kết luận ở ca khỏe), ưu tiên X khi đánh đổi (đề xuất); ca khỏe phải đạt ngưỡng khai trước; ma trận D14 (1)–(4) + baseline `src/p3/adapters/` (chỉ báo cáo, Minh chọn); C4-c/d/e OPEN vì không có ô dev.
- **R5:** `chay/HO-SO-LUOT-E1.md` bản 2 bỏ khẳng định "stage lại đúng mã"; đề xuất chặng 4 đưa wrapper tiếp nhận vào điều kiện vào.
- **N2:** `e2.py` `thanh_phan_tiem` chỉ điền khi root một nút; root cạnh → null. Chạy lại `e2.py --phat-lai --day`: 9 kết quả chính **không đổi byte** (hash trước/sau trùng); phát lại và chỉ mục phát lại sinh lại và đẩy lên exp-obs (f728fce2, 1ad3afeb: `dap_an_thanh_phan` "—", `m1_trong_tap` đủ hai đầu).
- Manifest `results/T-062/manifest.json` sinh lại (568 file).
- Tiếp: Codex kiểm lại phản hồi và sửa (`REVIEW-2.md`, prompt `results/T-062/codex/phan-bien-T062-luot2-prompt.txt`); Codex kiểm Grafana thật bản 6 (`codex/G1-that-2-brief.md`).

## 12/11/2026 ~13:30Z — Claude (người làm) — đáp REVIEW-2.md

- Codex lượt 2 (`tasks/T-062-dem-chang-1-4/REVIEW-2.md`, `-s read-only`): R1–R5, N2 sửa đúng; còn R1-tiếp (nhãn `root = null` của 4 ca không tiêm lỗi trong E2/bảng chấm), R2-tiếp (R-05 ĐẠT rỗng ở phần metric/binding), R6 (K thưởng ERROR, held-out không có ca khỏe), R7 (C4-a: luật chỉ chấm nút), R8 (mốc FLASH lệch k6 ~21 s do `sleep(20)` trước `S`).
- Đã kiểm trên code/dữ liệu: cả 5 đúng (R8 xác nhận `runner.py:87` và `:174`; R2-tiếp xác nhận 5 chuỗi `db-size` có `service_instance_id`). Điền bảng phản hồi cuối REVIEW-2.md kèm đề xuất sửa; **chưa sửa** — các điểm mới cần Minh quyết.
- Đề xuất sửa gom theo file: `e2.py` (nhãn sức khỏe chưa xác nhận, sinh lại phát lại/bảng chấm/chỉ mục, giữ bản cũ `_ban-2/`); `kiem-du-lieu/kiem-r.py` + `bao-cao-B1.md` (R-05 `MOT_PHAN`); `spec-chang-4-de-xuat.md` (K' tính ERROR là không đạt, thêm 2 ca khỏe held-out, ba bảng chấm T-059 cho C4-a); `bao-cao-sang.md` (đính chính cửa sổ FLASH); `chay/runner.py` cho lượt sau (lấy `S` từ `start-utc.txt` của k6).
- Prompt kiểm lại tiếp (nếu Minh muốn lượt 3): `results/T-062/codex/phan-bien-T062-luot2-prompt.txt` đổi đích `REVIEW-3.md` và mục "Phản biện và phản hồi trước" thêm REVIEW-2.md.

- ~14:00Z: Codex kiểm Grafana thật bản dashboard 6 (`results/T-062/codex/G1-that-2-ketqua.md`, `g1-that-2/`): ĐẠT MỘT PHẦN — 9/9 ca khớp nguồn, 13 liên kết Explore (menu + bảng bằng chứng) mở đúng; chưa có liên kết Loki ở bảng bằng chứng; panel 5xx/log rỗng ở nhiều ca (API thành công). Đã báo phiên G1.

## 12/11/2026 ~15:00Z — Claude (người làm) — sửa REVIEW-2 (Minh duyệt), lần nguyên nhân ca nền, danh sách chờ duyệt

- Sửa R1-tiếp, R2-tiếp, R6, R7, R8 (chi tiết cuối REVIEW-2.md). Bản trước ở `results/T-062/_ban-2/`. Kết quả chính 9 ca không đổi byte.
- Lần nguyên nhân CAUSE_FOUND ở 4 ca không tiêm lỗi: `results/T-062/chay/thu-gia/LAN-CA-NEN.md`. FLASH: tải tăng thật (hợp lý theo thiết kế M1). 3 ca bình thường: cờ ở thao tác nền tần suất cao, độ dịch rất nhỏ; placebo dời mốc t (+120/+240 s, 6 lần M1 bản khóa, mã `gia*`, khám phá): 1/6 CAUSE_FOUND so với 3/3 ở mốc khai báo → ứng viên H1 đầu dò bộ chạy lúc t+63 (khớp lịch), H2 làm mới token (không khớp), H3 ngẫu nhiên; phép kiểm trực tiếp chưa phân xử (đo sai đại lượng — tổng thay vì thời gian độc quyền). Phát hiện kèm: CPU-BOOK làm chậm mọi service (không cô lập).
- Danh sách việc chưa làm/chờ duyệt có phân loại lý do: `results/T-062/viec-cho-duyet.md`.

## Phiên điều phối (tiếp) — 12–13/11/2026 — Claude — laptop Minh — lập và trình gói chiến dịch M1-FlashTicket

**Diễn biến**
- PR FlashTicket #17: Auto-fix báo xung đột với `main`; merge `origin/main` vào `rca/quan-sat-log`, gỡ 1 xung đột (`.github/scripts/detect-changes.sh`, giữ cả luật `deploy/observability/*` và phần K3s), chạy 2 phép kiểm CI trên `exp-obs` trong thư mục tạm (đạt), push `fba6bc8`. Không merge PR. `exp-app` vẫn chạy `6b21ed55`.
- Minh nêu các chốt (baseline sau khi khóa; tải đủ đặt vé/thanh toán; một lần thu mỗi ca; giữ tín hiệu + chú thích thao tác nền; Collector cách A; kiểm CPU trước; kiểm span cha rỗng; phản biện B16). Claude trình plan → Codex phản biện 3 lượt trong chat (R1–R4; điểm 1–5; lượt ba về giới hạn tự đặt) → Claude đáp, chỉnh gói. Không có bất đồng còn lại.
- Lý do tải T-062 chỉ đọc: SPEC T-062 dòng C1 (Claude soạn) lấy `deploy/rca-test/workload.js` làm gốc, thu hẹp kế hoạch chặng 2 mà không nêu hệ quả (SL26). Trở ngại thật: `exp-app` chưa có VNPay giả, 1 tài khoản mua, 3 đơn `CANCELLED`.
- Kiểm thêm (có số ở `CHIEN-DICH-M1-FT.md` mục 2): span gốc ca `a5539fba`; gói ca chỉ 7 truy vấn metric; tên metric trên Prometheus; **retention 2 ngày**; chuỗi đồng hạng (`_nhom` → `tie_group + 1`; `e2.py` chấm theo hạng nhóm, khác quy ước kỳ vọng của `src/p3/danh_gia.py`).
- 13/11 ~02:15 giờ VN: Minh duyệt tổng thể và lệnh ghi file. Đã ghi: `CHIEN-DICH-M1-FT.md`, `SPEC-PHU-LUC-2.md`, `CHECKPOINT-CHIEN-DICH.md`, `PROMPT-PHIEN-MOI.md` (thư mục này); SPEC + LOG của T-063, T-064, T-065; `results/T-064/tieu-chi-chon.md`; mục DECISIONS 12–13/11; dòng STATE.
- Xuất metric bổ sung của cửa sổ D2+E1 từ Prometheus: `results/T-062/ca/_metric-bo-sung/` — file chính 217 metric, 10.496 chuỗi, 16.025.774 mẫu; phần bù 4 metric (cắt khúc 10 phút, 57 khúc mỗi metric, 0 lỗi): `up` 10.259 mẫu, span-metrics `_count`/`_sum` mỗi loại 1.474.612 mẫu, `_bucket` 25.068.404 mẫu. **Sự cố:** truy vấn một phát của `_bucket` làm Prometheus tự khởi động lại 1 lần lúc 19:16:33Z (sẵn sàng lại 19:16:42Z); sau lượt bù `RestartCount` vẫn 1. Biên bản: `_metric-bo-sung/SU-CO.md`. Nguyên nhân chính xác chưa xác định.

**Quyết định của Minh trong phiên:** đã chép nguyên lời vào `docs/DECISIONS.md` (mục "Chiến dịch M1-FlashTicket", 12–13/11/2026).

**Kết thúc phiên**
1. Đã làm: như trên. Chưa bắt đầu bước nào của bốn hồ sơ.
2. File đã thay đổi: các file liệt kê ở trên; `docs/STATE.md`, `docs/DECISIONS.md` (thêm mục); repo FlashTicket nhánh `rca/quan-sat-log` (merge `fba6bc8`, đã push).
3. Kiểm đã chạy: hash 6 file T-062 khớp manifest (trước khi ghi file mới); lượt xuất metric `rc=0` cả hai; `RestartCount=1`. **`results/T-062/manifest.json` chưa cập nhật** cho `_metric-bo-sung/` và file mới (việc của phiên kế).
4. Cần Minh quyết: 4 điểm ở `CHIEN-DICH-M1-FT.md` mục 9.
- Bước tiếp theo chính xác: Minh dán khối prompt trong `PROMPT-PHIEN-MOI.md` vào phiên mới; phiên đó làm theo "Việc tiếp theo" của `CHECKPOINT-CHIEN-DICH.md`.
- Lệnh cuối đã chạy: `ssh exp-obs 'python3 -' < xuat-phan-con-thieu.py | gzip > prometheus-tho-phan-con-thieu.jsonl.gz` (rc=0).
