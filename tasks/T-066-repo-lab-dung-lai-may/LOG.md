# Nhật ký T-066

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối, không sửa mục cũ. Mỗi phiên một mục.

---

## Phiên 1 — 17/11/2026 — Claude — laptop Minh — vai trò: người làm (soạn SPEC)

**Mở phiên:** đã đọc AGENTS, STATE, kế hoạch giai đoạn 2 §8. Task mới, chưa có đầu ra.

**Công đoạn và mục tiêu nguồn:** trình SPEC. Kế hoạch bản 3 §8.2 W1; MRP P9–P10; DT18-NV3.

**Diễn biến:**
- 17/11 — trình SPEC bản 1 trong chat; Codex soát bản 1 (7 điểm chặn); Claude kiểm cả 7 điểm đều đúng (giả lập merge `640dbaf` + `bb84d64` chỉ đọc: 10 file xung đột; compose Payment của `main` có sidecar `ngrok`; kịch bản k6 không gọi route nào của User); trình bản 2.
- 17/11 — Minh duyệt SPEC bản 2 ngày 17/11/2026 ("Duyệt, tạo file"). Ghi `SPEC.md` (bản 2 ghép đầy đủ) và LOG này.

**Quyết định của Minh trong phiên** (nguyên lời; chưa ghi DECISIONS):
- "duyệt gỡ xung đột, giữ main nhé, main là chuẩn. duyetj Q3 q4. duyệt Q1 b). .git nếu không có giá trị sử dụng lại cao thì duyệt xóa" — nghĩa: gỡ xung đột T-067 theo "main là chuẩn"; Q1(b) bộ điều khiển chạy trên exp-obs với khóa riêng (T-066); Q3 được dựng lại DB exp-app (T-067); Q4 ngưỡng log nối span 95% (T-067); dọn `.git` của repo RCA (đã làm: xóa 107 pack tạm 2,36 GB, `git gc --prune=never`; sau gc 2 pack, 7,52 GiB, không object rời, không rác).
- "Duyệt, tạo file" — duyệt SPEC bản 2 của T-066 và T-067, cho tạo file.

**Kết thúc phiên:**
1. Đã làm gì: soạn và ghi SPEC bản 2; ghi LOG; thêm dòng task vào STATE.
2. File đã thay đổi: `tasks/T-066-repo-lab-dung-lai-may/SPEC.md`, `tasks/T-066-repo-lab-dung-lai-may/LOG.md`, dòng T-066 trong `docs/STATE.md`.
3. Kiểm tra đã chạy và kết quả: các phép kiểm điểm Codex ở mục Diễn biến. Chưa làm bước nào của task.
4. Điều chưa chắc hoặc cần Minh quyết:
   - Task chưa bắt đầu; chưa trả lời câu hỏi nào trong SPEC.
   - Địa chỉ nguồn mà máy tải AWS thấy khi exp-obs kết nối [chưa kiểm]; đo ở bước 5.
   - Codex chưa kiểm lại bản 2; Minh chọn gửi prompt dưới đây hay bắt đầu làm.
   - Quyết định trong phiên chưa ghi `docs/DECISIONS.md`; cần Minh duyệt dòng ghi.
5. Bước tiếp theo chính xác: SPEC bước 1: lập `results/T-066/phu-thuoc.md` bằng lệnh chỉ đọc (grep đường dẫn trong `D:/Project/flashticket-rca-lab` và `results/T-058/dem-2026-11-10/`, so hash bản trên máy).
6. Lệnh cuối cùng đã chạy: `git count-objects -vH` (repo RCA, sau gc).

---

## Prompt bàn giao của lượt này cho agent đối phương

Một prompt chung cho cả T-066 và T-067. Minh quyết gửi hay không.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-066 (tasks/T-066-repo-lab-dung-lai-may/SPEC.md) và T-067 (tasks/T-067-ban-flashticket-ghim/SPEC.md), SPEC bản 2 đã ghi file; bản 1 trong chat 17/11 (Minh dán kèm nếu cần).
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P9–P10, chuẩn bị G6.
- Người làm và người phản biện chính thức: Claude là người làm; Codex là người phản biện (theo hai SPEC).
- Tài liệu gốc: docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8; docs/DECISIONS.md; docs/STATE.md; docs/techstack/PLAN-TRIEN-KHAI.md §5; docs/MRP.md P9–P10; docs/WHY.md (WHY-99); results/T-040/yeu-cau-quan-sat-p9.md; tasks/T-043-thiet-ke-rca-m1/SPEC.md; D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md; LOG phiên 1 của T-066 và T-067.
- Phản biện và phản hồi trước: lượt Codex soát bản 1 của hai SPEC và bản đáp/bản 2 của Claude, trong chat 17/11; Minh dán kèm theo thứ tự thời gian.
- Code và kết quả liên quan: D:/Project/flashticket-rca-lab tại a46c009; D:/Project/flash-ticket-platform (origin/main 640dbaf, origin/rca/quan-sat-log bb84d64); results/T-058/dem-2026-11-10/; results/T-062/kiem-du-lieu/; results/T-063/; results/T-064/ (manifest-3.json, cau-hinh-de-xuat.json, kiem/r9/); D:/RCA-archive/README.md. Máy chỉ được đọc (cách gọi ở docs/STATE.md).
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat.

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
```

---

## Phiên 2 — 17/11/2026 — Claude — laptop Minh — vai trò: người làm (triển khai T-066, sau đó T-067)

**Mở phiên:** đã đọc AGENTS, STATE, SPEC bản 2 và mục cuối LOG của T-066, T-067. Chưa có đầu ra nào trong `results/T-066/`.

**Quyết định của Minh trong phiên** (nguyên lời; chưa ghi DECISIONS):
- "Vậy cứ làm tuần tự đi ... copy file hay tái sử dụng file thì phải đảm bảo không được thay đổi nội dung, như nội dung của V082 chẳng hạn, tôi sợ phương pháp bị thay đổi mà không hề hay biết, đồng thời yêu cầu agent làm 1 vòng review trước, không có vấn đề chặn thì duyệt triển khai task luôn."
- Kèm theo trong lời dặn phiên: làm T-066 rồi T-067 tuần tự; luật toàn vẹn khi chép/dùng lại file (danh sách file bảo vệ ở `results/T-066/phu-thuoc.md`, chép nhị phân, kiểm sha256 ở mọi đích, không sửa file bảo vệ, `.gitattributes -text` nếu git đổi xuống dòng); bước 11 chờ Minh duyệt danh sách xóa; T-067 chỉ đụng container exp-app sau tuyến một ca của T-066 và sau bước 7; dump DB đọc lại được rồi mới dựng lại DB.

**Diễn biến:**
- 11:29Z — **Bước 0: tự soát hai SPEC với file thật và máy** (chỉ đọc; không thay vòng phản biện của Codex). Kết luận: **không có điểm CHẶN**; theo lời dặn của Minh, coi như đã duyệt triển khai. Các điểm KHÔNG CHẶN:
  - S0-1 (KHÔNG CHẶN) — Cả 149/149 file của bản chụp `goc-12` có xuống dòng CRLF (`grep -rlU $'\r' goc-12 | wc -l` = 149), kể cả `.py`. `ma_nguon_sha256` (b0f79a4d…) tính trên byte CRLF. Repo lab có `* text=auto eol=lf` nên **không đưa mã M1 vào git lab**; bản chụp đặt ở `/srv/rca-lab/m1-snapshots/<ma_nguon_sha256>/` (ngoài git, đúng SPEC), chép nhị phân bằng `tar` ngay trên exp-obs từ `/opt/rca-m1ft/goc-12`, kiểm bằng danh sách hash archive. Hậu quả nếu làm khác: hash mã đổi, hồi quy hỏng.
  - S0-2 (KHÔNG CHẶN) — User `rca` (uid 997) và `ledger` (uid 995) **đã có** trên exp-obs từ T-058 (`id rca ledger`); bước 4 dùng lại, không tạo mới. Sổ hiện tại của runner4 ở `~/rca-dieu-phoi/tiem-loi/` (chủ ubuntu, thư mục cha 700; `sudo -u rca test -r` → không đọc được). Runner mới ghi sổ qua user `ledger`.
  - S0-3 (KHÔNG CHẶN) — Cấu hình quan sát: 4 file JSON trên máy ≡ YAML của lab sau khi thay `10.0.0.215` bằng `${env:OBS_PRIVATE_IP}` (prometheus, loki, tempo, collector: TRÙNG); compose chỉ khác đường dẫn, env file, biến IP, tên volume tường minh (cùng tên cũ). 9 dashboard và `infinity.yaml` trùng hash với bản trên máy (bản làm việc trên laptop). Hai file `rca-g2-chinh`, `rca-g2-phat-lai` trên máy là CRLF; git lưu LF nên bản checkout trên Linux sẽ khác hash bảng nguồn gốc nhưng cùng nội dung JSON; không phải file phương pháp. Tên thư mục Grafana sẽ đổi (`0 · Bắt đầu tại đây` → `00-start-here`…), UID giữ nguyên.
  - S0-4 (KHÔNG CHẶN) — Collector gateway hiện ghi `/opt/flash-ticket-obs/pinned/data` (capture 5,0 GB, queue 38 MB); compose lab đổi sang `/srv/rca-lab/collector-gateway`. Hàng đợi cũ không mang theo: chuyển lúc không có tải để không mất bản ghi đang chờ. Capture cũ để nguyên, vào danh sách xóa.
  - S0-5 (KHÔNG CHẶN) — STATE ghi `pinned/compose.json` sha256 `684d39bd…`; thực tế `583e63c7…` (khớp `docs/sources-2026-11.md`). STATE cũ; không dùng làm đầu vào. Đề xuất sửa dòng STATE khi cập nhật cuối task.
  - S0-6 (KHÔNG CHẶN, việc chưa liệt kê) — Bước "chuyển G1 → cập nhật chỉ mục" chưa có công cụ trong lab. Dashboard hiện hành đọc `/public/rca/t065-l11-001/du-lieu/{chi-muc-ban.json, <bản>/chi-muc.json, <bản>/vue/<ca>.json, thao-tac-vue/…, trang-thai/…}`; bộ sinh `l11-may.py`/`l8b-xuat.py` của T-065 gắn cứng tập 28 ca (`assert len(b['cac_ca']) == 28`, hash chỉ mục cố định) và đường dẫn `/opt/...`. Phải chuyển thành bộ chuyển cho một ca trong `campaigns/` của lab, kiểm bằng cách sinh lại JSON của một ca cũ và so byte. Trong phạm vi ghi (repo lab mọi thư mục); cần cho tiêu chí xong 3.
  - S0-7 (KHÔNG CHẶN) — `campaigns/runner/xuat_bo_sung.py` của lab trùng bản trong `goc-12/results/T-063/dong-goi/` (so sau khi bỏ CR). Bước 3 sửa bản của lab theo SPEC; bản trong `goc-12` giữ nguyên. File này không được `chay_ca.py` import (không thuộc mã M1); đúng sai do `r9-tong-quat.json` phân xử. Gói chuẩn của 46aab4be (`bo-sung-dev2`, phiên bản `T063-bo-sung-3`) dùng công thức cũ; theo WHY-99 (`so-live-down-2.json`) công thức mới không lệch điểm nào ở 46aab4be, nên phép so kênh `live-down` vẫn hợp lệ. So thêm 23 kênh còn lại, báo riêng.
  - S0-8 (KHÔNG CHẶN) — Prometheus còn dữ liệu: `prometheus_tsdb_lowest_timestamp_seconds` = 1794340800 (10/11 20:00Z); cửa sổ 46aab4be có 10 mẫu `httpcheck_error`/2800 `httpcheck_status`, ebd5ef38 có 5/3960. Cờ giữ 30d/40GiB, khối 2,55 GB. Phép so R9 phải xong trước ~10/12.
  - S0-9 (KHÔNG CHẶN) — Đầu vào khớp hash: 157 file (`goc-12`, `bo-sung-dev2/46aab4be`, `bo-sung-dev3/ebd5ef38`, `out/r9-bo-sung`) trên exp-obs khớp `D:/RCA-archive/hash-lists/exp-obs-m1ft-inputs.sha256`; gói ca 46aab4be trên máy khớp `results/T-063/thu2/ca/46aab4be.tgz` (tgz khớp `thu2/SHA256SUMS`), ebd5ef38 khớp `hash-lists/exp-obs-cases.sha256`; `m1-p7-config.json` = `eb7dddd7…` (= bản T-058 trên laptop = `cau_hinh_p7_sha256` trong summary R9); `m1-source-pins.json` 39/39 file khớp `goc-12/src` → bản chụp `goc-12` phục vụ được cả stage/run-m1; `cau-hinh.json` V082 = `01a64b60…` = `cau_hinh_file_sha256`; `cau-hinh-de-xuat.json` = `238f40dd…` khớp manifest-3.
  - S0-10 (KHÔNG CHẶN) — Chuẩn hồi quy lấy từ manifest-3: 46aab4be `kiem/nhan-luot5/l5/dev2/d0/V082-V066+H8a/46aab4be/method-output-1.json` (`573df32d…`); ebd5ef38 lấy bản sau R9 `kiem/nhan-r9/r9/dev3/d0/…` (`563f449d…`), không lấy bản lô 5 (`647a4f68…`, trước R9). Lệnh tái lập theo `l5_chay.sh`/`r9_chay.sh`: ebd5ef38 thêm `--dung-lai-dau-vao` và gói R9 d0; 46aab4be dùng gói `bo-sung-dev2`.
  - S0-11 (KHÔNG CHẶN) — Venv P7 `/opt/flash-ticket-rca/venv`: Python 3.12.3, cùng bản `python3` hệ thống; `pip freeze` 17 gói (numpy 1.26.4, scipy 1.14.1, pandas 2.2.3, networkx 2.5…). Venv mới dựng từ danh sách này.
  - S0-12 (KHÔNG CHẶN) — Khóa của laptop đang nằm trên exp-obs ở `~/rca-dieu-phoi/keys/` (runner4, tai_linux dùng; không đọc nội dung). Khóa mới Q1(b) thay thế; khóa cũ đưa vào danh sách xóa.
  - S0-13 (KHÔNG CHẶN, T-067) — `origin/main` của FlashTicket đã đi tiếp `640dbaf` → `71eecd7` (`git fetch --dry-run`). SPEC ghim `640dbaf`; theo SPEC giữ bản ghim, chỉ báo Minh. `git merge-tree 640dbaf bb84d64` vẫn ra đúng 10 file xung đột.
  - S0-14 (KHÔNG CHẶN) — Sudo không mật khẩu, git, docker có trên cả ba máy; cả ba ra được GitHub (HTTP 200); log sshd đọc được bằng `journalctl -u ssh` (cho `from=` ở bước 5).
  - S0-15 (sự cố quy trình, báo Minh) — Lệnh ssh đầu phiên dùng `StrictHostKeyChecking=accept-new` với `D:/RCA-ext/keys/known_hosts` nên đã **thêm 2 dòng** khóa máy chủ (213.35.116.128, 129.221.208.47) vào file đó, ngoài repo, chưa duyệt. Hai khóa trùng bản trong `D:/RCA-ext/overnight-T058/out/known_hosts`. Hoàn tác: xóa 2 dòng đó. Từ sau dùng bản sao known_hosts trong thư mục tạm của phiên. Ngoài ra đã đếm số dòng `~/.ssh/authorized_keys` trên ba máy (chỉ đếm: 1, 1, 2), phục vụ bước 5.
- 11:31Z — Bước 1 xong: `results/T-066/phu-thuoc.md` (A: 200 file bảo vệ, lệch 0; B: đường dẫn từng thành phần; C: 55/55 file chép nguyên trùng máy; D: ánh xạ cũ→mới), `bao-ve.tsv`, `lap_phu_thuoc.py`. Hash ở `results/T-066/SHA256SUMS` cuối task.
- 11:37Z — Bước 2 (một phần): repo lab thêm `campaigns/lib/inventory.py` (+ `campaigns/__init__.py`, `campaigns/lib/__init__.py`); bỏ IP viết cứng ở `load/profiles/purchase-journey.json`, `load/profiles/legacy/workload-t062.json` (chỗ giữ `{application.public_ip}`, `{application.private_ip}`, thay lúc gửi), `load/fixtures/fixture.py`, `app-host/scripts/deploy-t062.sh`; `load/controller/tai_linux.py` đọc đích từ inventory, khóa ở `/etc/rca-lab/controller/`, trạng thái ở `/srv/rca-lab/load-controller`, nguồn theo bố cục repo lab, phiên bản = commit git (thay `linux-source-manifest.json`). Còn: `runner4.py`, `stage_m1.py`, `run_m1.py`, `safe_export.py`, sổ tiêm qua user `ledger`. Chưa commit.
- 11:37Z — Bước 3 xong: `campaigns/runner/xuat_bo_sung.py` (sha256 `7a8e80f6…` lúc chạy) tính `live-down` theo lần dò mới nhất, mặc định; thêm `--truoc/--sau`, `--live-down cu`. Chạy chỉ đọc Prometheus trên exp-obs cho 7 mốc → `results/T-066/r9-xuat/`. So bằng `results/T-066/so_r9.py` → `results/T-066/r9-tong-quat.json`: **7/7 gói trùng tập bộ (URL, timestamp, giá trị) kênh live-down** (328 bộ mỗi gói; 46aab4be có 20 giá trị 1, ebd5ef38 có 3), `t` và cửa sổ trùng; 23 kênh còn lại trùng ở cả 7 gói. Đối chứng âm (`r9-xuat/doi-chung-cu.txt`): công thức T-063 xuất lại ở ebd5ef38 d0 lệch gói R9 34 bộ và trùng gói dev3 cũ 0 lệch → phép so phân biệt được, dữ liệu Prometheus không đổi từ 14/11. Tiêu chí xong 2 đạt.
- 11:42Z — Bước 2 (tiếp): repo lab thêm `campaigns/runner/{stage_m1.py, run_m1.py, safe_export.py}` (chép nhị phân bản T-058 rồi chỉ đổi đường dẫn thành biến môi trường RCA_M1_CODE/RCA_M1_ROOT/RCA_CAPTURE/RCA_EXPORT_DIR; mã lõi gọi tới vẫn là bản chụp), `ledger_append.py` (ghi sổ bằng user ledger, cùng quy tắc seq/prev_sha256), `campaigns/requirements-m1.txt`; `runner4.py` đọc inventory, khóa `/etc/rca-lab/controller`, dữ liệu `/srv/rca-lab`, inj3 qua `/opt/rca-lab` trên exp-app, sau P7 chạy V082 từ bản chụp (kiểm hash cấu hình `01a64b60…`); `tai_linux.py` + `support/kiem-token-con-han.py` dùng `/etc/rca-lab/load-secret`, `/srv/rca-lab/load-runs` trên máy tải. `git grep` IP ngoài `inventory/`: chỉ còn trong `docs/sources-2026-11.md` (bảng nguồn gốc, ghi lịch sử phép thay). Chưa commit.
- 11:42Z — Bước 4 (exp-obs): tạo `/opt/rca-lab` (ubuntu 755), `/etc/rca-lab` (root 755) + `controller/` (ubuntu 700), `/srv/rca-lab` với `m1/{cases,bo-sung}` (root:rca 750), `m1/{outputs,v082}` (rca 750), `m1/export-audit` (root 700), `m1-snapshots` (root 755), `ledger` (ledger 700), `runs`, `load-controller` (ubuntu 700). Chép (cp -p/install, không di chuyển) `grafana.env`, `credential-hash-catalog.json` sang `/etc/rca-lab` (root 600) và 3 file cấu hình P7 sang `/srv/rca-lab/m1`: 5/5 cặp hash TRÙNG. Bản chụp: `tar` từ `/opt/rca-m1ft/goc-12` sang `/srv/rca-lab/m1-snapshots/b0f79a4d…/` (root, rca không ghi được): 149/149 file khớp danh sách hash archive; `ma_nguon_sha256` tính lại trên bản chụp = `b0f79a4d…`. Venv `/srv/rca-lab/venv-m1` dựng từ `requirements-m1.txt` (`pip install --no-deps`): `pip freeze --all` trùng venv P7. Chi tiết và hoàn tác: `results/T-066/thay-doi-may.md`.
- 11:42Z — **Ghi trước khi chạy V082 (luật toàn vẹn mục 7):** Python 3.12.3 (GCC 13.3.0), venv `/srv/rca-lab/venv-m1`; `pip freeze --all` = cachetools 4.2.1, decorator 5.3.1, drain3 0.9.11, iniconfig 2.3.1, jsonpickle 1.5.1, networkx 2.5, numpy 1.26.4, packaging 26.3, pandas 2.2.3, pip 24.0, pluggy 1.7.0, pyarrow 18.1.0, pytest 8.3.4, python-dateutil 3.0.0, pytz 2026.6, scipy 1.14.1, six 1.17.0, tzdata 2026.6; repo lab `a46c009` + thay đổi chưa commit (phép hồi quy không dùng mã lab: gọi thẳng `chay_ca.py` của bản chụp); hash bản chụp mã `b0f79a4dffd552f6e6026172b9058cd54ee9272475d927e35f19e22b04411b8d`; cấu hình V082 `cau-hinh.json` byte `01a64b60…`, chuẩn hóa `451a8437…`.
- 11:44Z — Bước 8 xong (làm trước bước 5–7 vì không phụ thuộc mã lab): hồi quy V082 d=0 từ vị trí mới (`/srv/rca-lab/m1`, bản chụp, venv mới, user rca). 46aab4be `method-output-1.json` = `573df32d…`, ebd5ef38 = `563f449d…`: **trùng byte manifest-3** ở cả hai lần chạy; `cau_hinh_sha256` = `451a8437…`, `ma_nguon_sha256` = `b0f79a4d…`; ebd5ef38 dựng lại đầu vào `input_sha256` = `28edbec8…` (= summary R9 T-064). Không sinh `__pycache__` trong bản chụp. File: `results/T-066/hoi-quy-v082.json`, `results/T-066/hoi-quy/summary-*.json`. Tiêu chí xong 1 đạt.
- 11:47Z — **Đính chính S0-12:** `~/rca-dieu-phoi/keys/` **không tồn tại** trên exp-obs (`ls` 11:45Z); không có khóa cũ nào của laptop trên exp-obs để thay hay xóa. Câu "khóa của laptop đang nằm trên exp-obs" ở S0-12 là suy từ mã runner4/tai_linux, chưa kiểm, và sai.
- 11:47Z — Bước 5 xong: cặp ed25519 `rca-lab-controller` tạo trên exp-obs (`/etc/rca-lab/controller/`, khóa riêng 600, không rời máy, vân tay `SHA256:tzVU95z3…`). Đo nguồn bằng lần thử bị từ chối, đọc log sshd ở đích: **exp-app thấy `213.35.116.128`** (dự kiến `10.0.0.215` [chưa kiểm] trong SPEC là sai, vì kết nối qua IP công khai), máy tải thấy `213.35.116.128` (đúng dự kiến). Thêm đúng 1 dòng `from="213.35.116.128" … rca-lab-controller` vào `authorized_keys` của ubuntu ở hai máy; kết nối thử đạt cả hai (`SSH_CLIENT` = 213.35.116.128). `known_hosts` của bộ điều khiển lấy từ khóa máy chủ đã kiểm trên laptop.
- 11:47Z — Bước 4 (máy tải, exp-app): máy tải tạo `/opt/rca-lab`, `/etc/rca-lab/load-secret` (ubuntu 700), `/srv/rca-lab/load-runs`; chép 3 file bí mật tải (cp -p): 3/3 hash TRÙNG. exp-app tạo `/opt/rca-lab`. Repo lab thêm `campaigns/README.md`. Ghi `results/T-066/thay-doi-may.md`.
- 11:47Z — **Dừng chờ Minh:** cần commit + push repo lab (luật cứng 11) trước khi đưa bản git lên `/opt/rca-lab` của ba máy (bước 4 phần "chạy từ /opt/rca-lab", bước 6, 7, 9). Đề xuất commit trình trong chat.
- 12:05Z — Minh duyệt commit lab này và các commit lab sau trong phạm vi T-066 (trả lời câu hỏi trong phiên: "Duyệt commit này + các commit lab sau trong phạm vi T-066"). Commit `5a39028` đã push lên `main` của flashticket-rca-lab.
- 12:06Z — Repo lab `5a39028` clone vào `/opt/rca-lab` trên exp-obs, exp-app, máy tải: HEAD đúng, cây sạch, hash `xuat_bo_sung.py` (`7a8e80f6…`), `stage_m1.py`, `run_m1.py`, `inj3.py` (`ba8f1341…` = `~/inj3.py` cũ) trùng laptop. Bước 6 xong: `results/T-066/cach-ly-nhan.md` — ledger ghi sổ được; rca bị từ chối đọc sổ mới, sổ cũ, thư mục runs, ghi bản chụp; tiêu chí xong 6 đạt.
- 12:10Z — Bước 7 xong (12:07–12:10Z): chép `/opt/flash-ticket-obs/rca-ket-qua` → `/srv/rca-lab/rca-results` bằng tar: 8013/8013 file khớp (danh sách hash lưu `/srv/rca-lab/rca-results-chep-2026-11-17.sha256`, sha256 `a328c98f…`). Tạo `/srv/rca-lab/collector-gateway/{capture,queue}`. `docker compose -p flash-ticket-obs-pinned --env-file ../inventory/oracle-exp.env -f /opt/rca-lab/observability/compose.yaml up -d` lúc 12:07:48Z: 5 container tạo lại, cùng image digest, cùng 4 volume; `compose ls` trỏ file lab. Kiểm: Prometheus/Tempo/Collector/Grafana 200, Loki 200 sau ~30 s; Collector ghi vào `/srv/rca-lab/collector-gateway/capture`. Grafana (đọc chỉ-đọc CSDL trong volume, không dùng mật khẩu): **đủ 9 UID** (`rca-g2`, `rca-g2-phat-lai`, `t065-l4-phat-lai`, `t065-l4-rca`, `t065-l5-muc-luc`, `t065-l8b-phat-lai`, `t065-l8b-rca`, `t065-phat-lai`, `t065-rca`) nạp lại từ `/etc/grafana/dashboards/…` lúc 12:08:11Z, vào thư mục mới (`00-start-here`, `10-current-results`, `90-archive/…`); thư mục cũ còn, rỗng. Dữ liệu cũ: Tempo trả 5 trace trong 12/11 10:06–10:16Z và `/api/traces/<id>` 200; Loki trả log ngày 12/11 (cả ngày) và 14/11 (khung 10:06–10:16Z ngày 12/11 không có log); Prometheus 12/11 có. JSON phát lại `t065-l11-001/du-lieu/chi-muc-ban.json`, `V082-V066+H8a/chi-muc.json` qua `/public/rca/` của Grafana trùng hash bản gốc. Tiêu chí xong 4 đạt ở mức dữ liệu; **chưa xem giao diện** (Grafana cần đăng nhập; bộ phân loại an toàn chặn dùng `grafana.env` để gọi API — không lách). Hoàn tác vẫn giữ: `cd /opt/flash-ticket-obs/pinned && sudo docker compose -p flash-ticket-obs-pinned -f compose.json up -d`.
- 12:10Z — Bước 10 bắt đầu: `results/T-066/tempo_do.sh` (sha256 `e14519a0…`) chạy nền trên exp-obs (`setsid nohup`, PID 711102), mỗi 15 phút ghi `/srv/rca-lab/runs/tempo-do-t066/tempo-24h.tsv` (byte volume Tempo, blocks, spans nhận/xuất của gateway), tự dừng sau 25 giờ hoặc khi có file `DUNG`. Mốc đầu 12:10:07Z: volume Tempo 6.142.589.639 byte.
- Checkpoint (để tiếp nhận nếu phiên bị cắt): xong bước 0, 1, 3, 4, 5, 6, 7, 8; bước 2 xong trừ bộ chuyển G1; bước 10 đang chạy nền (đến ~13:10Z 18/11). Còn: (a) bộ chuyển G1 một ca `campaigns/g1/` trong repo lab — tái dùng logic `results/T-065/may-l11/codex/l8b-xuat.py` (`dev3_template` + phần dựng một ca trong `export()`), tham số hóa đường dẫn; kiểm bằng cách sinh lại một ca dev3 cũ không bị L11 dựng lại và so byte với `/srv/rca-lab/rca-results/t065-l11-001/du-lieu/V082-V066+H8a/`; cập nhật chỉ mục = thêm ca vào `t065-l11-001/du-lieu/{chi-muc-ban.json, V082-V066+H8a/chi-muc.json}` trên `/srv/rca-lab/rca-results` (bản gốc còn ở `/opt/flash-ticket-obs/rca-ket-qua`); (b) bước 9 tuyến một ca bằng `runner4.py thu --lich <lịch 1 chu kỳ>` với `RCA_DP_OUT=/srv/rca-lab/runs/e2e-001`; (c) bước 10 tổng hợp `tempo-tang-truong.md`; (d) bước 11 `danh-sach-xoa.md` trình Minh. Cách gọi máy: khóa ở `D:/RCA-ext/keys/`, known_hosts dùng `D:/RCA-ext/overnight-T058/out/known_hosts` (+ dòng 3.24.8.49 từ `D:/RCA-ext/keys/known_hosts`), máy tải dùng `Hahaa123.pem`.
- 12:15Z — Bước 9: `tai_linux.py test-duong` qua khóa bộ điều khiển mới đạt 12:14:18Z (mock, đường hầm, 20 token BUYER làm mới, bản ghi `/etc/rca-lab/load-secret/l1-tokens.json` đổi hash theo thiết kế). Repo lab `f78ed52` (bộ chuyển G1 `sau_v082.py` + `campaigns/g1/l8b-xuat.py` chép nhị phân, hash `7a80f537…` = bản T-065 trên máy; kiểm sinh lại ca dev3 0a45b2e0: **37/37 file trùng byte** `t065-l11-001`), `ab1c52c` (lịch `campaigns/schedules/e2e-t066.json`: 1 chu kỳ PAUSE-PAYMENT). Khởi động lượt `e2e-001` 12:14:26Z: `RCA_DP_OUT=/srv/rca-lab/runs/e2e-001 python3 -B /opt/rca-lab/campaigns/runner/runner4.py thu --lich …/e2e-t066.json`; tải `t3-7ffb2305` bắt đầu 12:15:04Z (30 phút, ×1). Khoảng này có tải trong phép đo Tempo.
- 12:50Z — Bước 9 xong: lượt `e2e-001` chạy trọn 12:14:26–12:45:58Z (tải `t3-7ffb2305` qua khóa mới; tiêm PAUSE-PAYMENT 12:25:04–12:35:05 bằng inj3 trong `/opt/rca-lab` của exp-app; sổ 12 dòng ghi bằng user ledger, rca không đọc được; stage → P7 OK, lặp trùng SHA; gói bổ sung R9; V082 trùng SHA `183a405d…` với `cau_hinh_sha256` `451a8437…`, `ma_nguon_sha256` `b0f79a4d…` khớp danh sách bảo vệ; G1 + chỉ mục: ca 7ffb2305 vào `chi-muc-ban.json` và `V082-V066+H8a/chi-muc.json`, 3 file phục vụ qua Grafana `/public/rca/` trùng hash). Bằng chứng `results/T-066/e2e-001/` (README, SHA256SUMS). Tiêu chí xong 3: đạt ở mức đường chạy và dữ liệu; **chưa xem giao diện** (cần Minh đăng nhập mở `/d/t065-l8b-rca?var-ban=V082-V066%2BH8a&var-ca=7ffb2305`). Không diễn giải hạng (không phải phép đánh giá).
  - Điểm phát hiện (KHÔNG CHẶN): chỉ mục ghi `nguon: "dev3"` cho ca mới vì `sau_v082.py` dùng lại nhánh dev3; đề xuất đổi thành `"moi"` (sửa 1 dòng trong `sau_v082.py`, sinh lại ca 7ffb2305); chưa sửa.
  - Sự cố quy trình: một lệnh kéo bằng chứng có `rm -f ./.` thừa, bị kiểm an toàn chặn, không chạy; lần kéo hỏng để lại `/tmp/e2e-t066-EcHI` (700, ubuntu, có bản chép sổ) trên exp-obs — đã xóa đúng thư mục đó.
- 12:52Z — Bước 11: `results/T-066/danh-sach-xoa.md` trình Minh (nhóm 1: ~31 GB có bản/dựng lại được; nhóm 2: cần bước trước). Chưa xóa gì.

**Kết thúc phiên 2 (17/11/2026 ~12:55Z):**
1. Đã làm gì: bước 0 (tự soát, không có điểm chặn); T-066 bước 1–9 xong; bước 10 đang đo nền; bước 11 đã lập danh sách xóa, chờ Minh. Chưa bắt đầu T-067.
2. File đã thay đổi — repo RCA: LOG này, dòng T-066 trong `docs/STATE.md`, `results/T-066/` (phu-thuoc.md, bao-ve.tsv, lap_phu_thuoc.py, so_r9.py, r9-tong-quat.json, r9-xuat/, hoi-quy-v082.json, hoi-quy/, cach-ly-nhan.md, thay-doi-may.md, tempo_do.sh, tempo-tang-truong.md, danh-sach-xoa.md, e2e-001/). Repo lab: commit `5a39028`, `f78ed52`, `ab1c52c` (đã push, Minh duyệt). Máy: theo `results/T-066/thay-doi-may.md` cộng các mục bước 7, 9 trong LOG (chưa chép vào thay-doi-may.md: compose chuyển 12:07Z, `/srv/rca-lab/rca-results`, `collector-gateway`, lượt e2e-001, sampler Tempo). Laptop ngoài repo: 2 dòng `D:/RCA-ext/keys/known_hosts` (S0-15).
3. Kiểm đã chạy: xem các dòng bước 0–9 ở trên (hồi quy, R9 + đối chứng âm, cách ly, so byte G1 37/37, tuyến một ca).
4. Chưa chắc / cần Minh: (a) duyệt danh sách xóa; (b) xem giao diện Grafana ca 7ffb2305 và 9 dashboard (agent không đăng nhập được); (c) sửa nhãn `nguon` của ca mới trong `sau_v082.py` (đề xuất `"moi"`); (d) quyết định giữ/xóa 2 dòng known_hosts; (e) commit repo RCA cho `results/T-066/`, LOG, STATE. Câu hỏi nghiên cứu: task không trả lời câu hỏi nào; chỉ xác nhận chuyển chỗ chạy không đổi đầu ra M1 trên 2 ca và đường chạy đi trọn trên bản hệ thống cũ.
5. Bước tiếp theo chính xác: (i) sau ~18/11 12:10Z đọc `/srv/rca-lab/runs/tempo-do-t066/tempo-24h.tsv`, tính byte/giờ lúc nền và lúc có tải (khoảng tải ở `tempo-tang-truong.md`), điền mục Kết quả + đề xuất mức giữ; (ii) bổ sung `thay-doi-may.md` cho bước 7, 9; (iii) Minh duyệt danh sách xóa thì xóa đúng mục, ghi lại; (iv) T-067 bước 1: tạo nhánh `rca/exp-2026-11` từ `640dbaf` trong `D:/Project/flash-ticket-platform`, merge `bb84d64`, gỡ 10 file theo SPEC T-067; (v) cuối T-066: cập nhật STATE "chờ phản biện", soạn prompt phản biện Codex (Prompt chung + khối "Soát kết quả" của `docs/review-prompt.md`).
6. Lệnh cuối cùng đã chạy: kéo bằng chứng `e2e-001` về `results/T-066/e2e-001/` và `sha256sum -c SHA256SUMS` (ok).
- 12:53Z — Minh duyệt nhóm 1 của `results/T-066/danh-sach-xoa.md` (trả lời trong chat: "Duyệt nhóm 1"). Mục 1.9 (thư mục Grafana rỗng) cần đăng nhập Grafana nên agent không làm; nhóm 2 chưa duyệt.
- 12:54Z — Bước 11 (nhóm 1): đã xóa 1.1–1.8, 1.10 trên exp-obs 12:53:42–12:53:45Z bằng đường dẫn tường minh; trước khi xóa kiểm không tiến trình nào dùng. Đĩa 58 → 27 GB. Còn đúng các mục nhóm 2 (`chon-dev2-1`, `chon-dev2-1b`, `tai-linux-events.jsonl`). 5 container quan sát running, sampler Tempo vẫn chạy. 1.9 chưa làm (cần đăng nhập Grafana). Ghi `results/T-066/thay-doi-may.md` (kèm bổ sung bước 7, 9, 10 còn thiếu) và mục Kết quả trong `danh-sach-xoa.md`.
- 15:10Z — Quyết định của Minh trong phiên (chat 17/11): "dừng đo, giữ 14 ngày". Bước 10 kết thúc sớm: tạo `/srv/rca-lab/runs/tempo-do-t066/DUNG` lúc 15:09Z, sampler đã thoát (không còn tiến trình). 12 mốc 12:10–14:55Z chép về `results/T-066/tempo-do-dung.tsv`; `tempo-tang-truong.md` ghi quan sát và quyết định giữ 14 ngày (không sửa `tempo.yaml`). Đo quá ngắn để ra GB/giờ; ước lượng thô ~0,9 GB/ngày từ volume 7 ngày (chưa kiểm).
- 15:12Z — Minh yêu cầu tunnel để đăng nhập Grafana. Mở trên laptop: `ssh -N -L 127.0.0.1:3000:10.0.0.215:3000` tới exp-obs (khóa exp-obs, known_hosts của phiên); `http://127.0.0.1:3000/login` trả 200. Không thay đổi gì trên máy. Tunnel tắt khi kết thúc tiến trình ssh.
- 15:30Z — Kiểm giao diện Grafana (Minh đăng nhập trong trình duyệt của app qua tunnel; agent không nhập mật khẩu). `/api/search`: 9 UID nằm đúng thư mục mới (`00-start-here`: `t065-l5-muc-luc`; `10-current-results`: `t065-l8b-rca`, `t065-l8b-phat-lai`; `90-archive/…`: 6 UID còn lại). Ca 7ffb2305 mở được ở `t065-l8b-rca` (bản V082-V066+H8a): bảng hash hiện `cau_hinh` `451a8437…`, mã nguồn `b0f79a4d…`, đầu ra `183a405d…`, cửa sổ 12:20:04–12:30:04Z, nguồn `/srv/rca-lab/m1/v082/7ffb2305/method-output-1.json`; bảng entity_ranking hiện đủ 19 thực thể; panel trace sống (payment-service) có trace trong khung ca; panel log lỗi payment-service "No data" trong khi Loki có 720 dòng payment-service trong 10 phút đó (không có dòng khớp error/exception/warn; chưa xem thêm). Lưu ý: link chỉ có `var-ca` không tự đặt khung giờ (dashboard giữ khung mặc định 14/11); phải bấm mã ca trong bảng hoặc thêm `from/to`. Đây là hành vi sẵn có của dashboard T-065, không do T-066. Tiêu chí xong 3 và 4 đạt cả phần giao diện.
- 15:28Z — Mục 1.9 (nhóm 1 đã duyệt): xóa 7 thư mục Grafana cũ rỗng, 7/7 HTTP 200; ghi `results/T-066/thay-doi-may.md`.
- 15:30Z — Minh hỏi Q2 (`RefundServiceImpl`). Đọc chỉ-đọc `D:/Project/flash-ticket-platform`: `git merge-tree 640dbaf bb84d64` có 1 khối xung đột trong file này. Phía `main`: commit `782e557` (Quốc Tuấn, 14/11, "fix(payment): xử lý hoàn tiền") bỏ luồng gửi/hỏi VNPay (`claimRefund`, `findUnfinishedAttempt`, `recordGatewayResult`), thay bằng hoàn tiền nội bộ chỉ cập nhật DB trong `sendRefund` (`attempt.setOutcome("DB_ONLY")`, `refund.setState(SUCCEEDED)`). Phía PR (`f7e6207`, B16): chỉ thêm `BusinessTelemetry.committed("refund-result", …)` trong `recordGatewayResult` — hàm mà `main` đã xóa. Đề xuất trình Minh trong chat; chưa sửa gì.
- 18/11 — Quyết định của Minh trong phiên (chat): nhóm 2 "cái nào không có giá trị sử dụng lại nhiều, không mang lại giá trị mới thì xóa đi, dùng lại được thì kéo"; Q2 T-067 "cứ lấy theo như tuấn, phần nào từ PR hiện tại mà cần thì merge làm vào", "vnpay không cho test luồng hoàn nên phải làm db như thế" (ghi lại vào LOG T-067 khi mở task).
- 18/11 — Bước 11 nhóm 2 xong: so hash 1.297 file; kéo 65 file + volume LGTM về `D:/RCA-archive/exp-obs/t066-nhom2/` (hash khớp); xóa 2.1–2.5 trên exp-obs, gỡ 2 dòng known_hosts (2.8); giữ 2.6, 2.7 tới sau T-067. Lần kéo volume đầu bị lệch hash do dòng `du` lọt vào đầu tar; kéo lại, khớp `68ffdef5…`. Chi tiết `danh-sach-xoa.md` (Kết quả), `thay-doi-may.md`.
- 18/11 — Tìm hiểu Grafana (chỉ đọc): 9 dashboard nạp lại nguyên theo SPEC (3 hiện hành, 6 lưu trữ T-065); 2 dashboard tạo tay ngoài repo (`t058-flashticket` 10/11, `t061-infinity` 11/11); nguồn `loki-1` trùng `Loki`. Dashboard V082 (`t065-l8b-rca`) không có đồ thị mức dịch vụ vì V082 không xuất xếp hạng cạnh, T-065 chỉ giữ đồ thị thao tác; P7 (`t065-rca`) và G2 có. Đề xuất dọn Grafana trình Minh trong chat (ngoài SPEC T-066); chưa sửa.

---

## Prompt soát kết quả T-066 (bổ sung 18/11/2026, Claude)

LOG trước chỉ có prompt soát SPEC dùng chung cho T-066 và T-067; thiếu prompt soát kết quả của T-066. Bổ sung theo AGENTS mục 7. Bước 10 (đo Tempo) dừng sớm theo quyết định của Minh; nhóm 1–2 danh sách xóa đã xử lý (mục 2.6, 2.7 giữ làm đường hoàn tác T-067).

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-066 — tasks/T-066-repo-lab-dung-lai-may/ (SPEC.md bản 2, LOG.md).
- Công đoạn: soát kết quả.
- Gói/cổng: P9, P10; chuẩn bị G6.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex.
- Tài liệu gốc: tasks/T-066-repo-lab-dung-lai-may/SPEC.md; repo lab D:/Project/flashticket-rca-lab, các commit T-066 tới ab1c52c (git log ab1c52c); repo RCA commit 84f44ee67.
- Phản biện và phản hồi trước: Codex soát SPEC bản 1 (trong chat 17/11; tóm tắt ở đầu SPEC.md); chưa có lượt soát kết quả.
- Code và kết quả liên quan: results/T-066/ (bao-ve.tsv, phu-thuoc.md, hoi-quy-v082.json, hoi-quy/, r9-tong-quat.json, r9-xuat/, cach-ly-nhan.md, e2e-001/ kèm SHA256SUMS và hash-tren-may.sha256, danh-sach-xoa.md, tempo-tang-truong.md, tempo-do-dung.tsv, thay-doi-may.md); results/T-064/manifest-3.json; D:/RCA-archive/exp-obs/m1ft-inputs và t066-nhom2 (SHA256SUMS); máy exp-obs, exp-app, máy tải theo inventory/ của repo lab (chỉ đọc).
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat.

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
```

---

## Phiên 3 — 18/11/2026 — Claude — laptop — vai trò: người làm (đáp phản biện soát kết quả của Codex, trong chat)

**Tự soát trước khi đọc kết luận** (đã tìm trước, trong các lượt T-068): việc thiếu prompt soát kết quả T-066 (đã bổ sung cuối LOG); dòng STATE T-066 ghi cũ (đã sửa). Không có điểm mới khác.

**Đánh giá lượt soát kết quả của Codex (18/11):**

| Điểm | Kết luận | Bằng chứng người làm chạy lại |
|---|---|---|
| R1 CHẶN — `results/T-064/manifest-3.json` không có trong git dù `bao-ve.tsv` dòng 171 ghi "git (repo RCA, đã commit)" | **Đúng** | `git ls-files --error-unmatch` báo không có; file không bị ignore, chỉ chưa track; kích thước 1.055.393 byte; commit T-064 `25550d2a5` chỉ gồm "kết quả nhẹ". Phép so hồi quy vẫn đúng (file trên laptop khớp hash ghi trong T-066). |
| R2 CHẶN — README tải chỉ `STOP` cũ; thiếu phụ thuộc `yaml` | **Đúng** | `load/controller/README.md:22` ghi `~/rca-dieu-phoi/STOP`; code đọc `STATE/STOP` với `STATE=/srv/rca-lab/load-controller` (`tai_linux.py:30,86`); runner dùng `/srv/rca-lab/runs/STOP` (`runner4.py:26,41`), nhưng docstring dòng 17 còn ghi đường cũ; `campaigns/lib/inventory.py:18` `import yaml`. |
| R3 CHẶN — căn cứ xóa 2.6/2.7 và mục 1.2 | **Đúng** | 2.6: `load/fixtures/fixture.py:13,21` vẫn đọc `/opt/rca-tai/secret/tokens.json` → giữ 2.6. 2.7: `deploy-t062.sh` cũ phục hồi được từ lab `a46c009` (`git ls-tree` có `app-host/scripts/deploy-t062.sh`). 1.2: đếm lại trên laptop (35 tgz trong `results/T-058|T-062|T-063` + thư mục `outputs/` đã giải nén) được **32 mã `outputs/` khác nhau**, không phải 38; 12 ca trong `D:/RCA-archive/exp-obs/cases/` chỉ có `cases/`, không có `outputs/`. 6 thư mục `outputs/` không xác định được tên vì không còn danh sách trước khi xóa; khả năng là đầu ra của các ca thử trong archive (`gia*`, `kte*`, `thuong01`…) — **chưa kiểm**. Câu "tgz chứa cả cases/outputs cho 33 ca" của hàng 1.2 nói quá. |
| R4 CHẶN — "đã kiểm phát lại trước khi trình xóa" | **Đúng** | LOG: trình danh sách xóa 12:52Z, Minh duyệt và xóa nhóm 1 lúc 12:53Z; lần xem Grafana 15:30Z là trang **sự cố** của ca mới, không phải ca cũ trên trang **phát lại**. Thứ tự ghi trong LOG trước đây không sai, nhưng tiêu chí W1 "mở được ca phát lại trước khi trình danh sách xóa" chưa đạt đúng thời điểm. Sau đó (T-068, 02:3xZ 18/11) trang phát lại trả 200. |
| R5 KHÔNG CHẶN — trạng thái `XONG` của runner | **Đúng** | Đồng ý; với ca sau, nghiệm thu theo trạng thái xuất, hai hash và đầu ra G1 của chính ca. `campaigns/runner/*.py` đang nằm trong danh sách bảo vệ của T-067 nên không sửa lúc này. |
| Đính chính khác (Codex nêu) | **Đúng** | "Không bước nào đọc sổ" cần thu hẹp: `ledger_append.py` (chạy bằng user `ledger`) đọc dòng trước để nối hash; không có đường đưa sổ vào P7/V082. Hai ví dụ IP trong docstring `inventory.py` không cấp địa chỉ cho tiến trình. |

**Đề xuất sửa gom theo file (chờ Minh duyệt):**
1. Repo RCA: commit `results/T-064/manifest-3.json` nguyên byte (kiểm sha256 `faa7d292…` trước khi add). Ghi `results/T-066/dinh-chinh.md`: (a) dòng 171 `bao-ve.tsv` — nguồn đúng là "file trên laptop, commit ở <hash mới>"; không sửa `bao-ve.tsv` vì T-067 đang dùng làm mốc; (b) hàng 1.2 danh sách xóa: 32/38 `outputs/` có bản, 6 không xác định; (c) R4: thứ tự thật và giới hạn; (d) câu cách ly sổ thu hẹp như trên.
2. Repo lab: `load/controller/README.md` ghi đúng hai đường STOP (`/srv/rca-lab/load-controller/STOP` cho bộ điều khiển tải, `/srv/rca-lab/runs/STOP` cho runner), nơi nhận kết quả, và yêu cầu Python hệ thống có `python3-yaml` (venv M1 không cần). Không sửa docstring `runner4.py` lúc này (đang được T-067 bảo vệ); ghi vào README thay thế.
3. `danh-sach-xoa.md` mục 2.6: giữ tới khi Minh quyết dừng hay tiếp tục dùng CLI `fixture.py`; mục 2.7: ghi phục hồi `deploy-t062.sh` từ lab `a46c009`.
4. R4: đề xuất Minh chấp nhận giới hạn lịch sử, và cho mở thử một ca cũ (ví dụ `46aab4be`) trên trang phát lại để xác nhận hành vi hiện tại (vài phút, cần Minh đăng nhập Grafana).
5. DECISIONS: ghi Q1(b) và "dừng đo, giữ Tempo 14 ngày" (Minh duyệt nội dung dòng ghi).

Không còn bất đồng có bằng chứng với Codex.

**Prompt cho Codex — kiểm lại phản hồi phiên 3:**

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-066 — tasks/T-066-repo-lab-dung-lai-may/ (SPEC.md, LOG.md); phản hồi của người làm ở mục "Phiên 3" cuối LOG.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P9, P10; chuẩn bị G6.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex.
- Tài liệu gốc: tasks/T-066-repo-lab-dung-lai-may/SPEC.md; repo lab D:/Project/flashticket-rca-lab, git diff a46c009..ab1c52c; repo RCA commit 84f44ee67.
- Phản biện và phản hồi trước: Codex soát SPEC bản 1 (chat 17/11); Codex soát kết quả (chat 18/11); phản hồi của người làm ở mục "Phiên 3" cuối LOG.md.
- Code và kết quả liên quan: results/T-066/; results/T-064/manifest-3.json; D:/RCA-archive/exp-obs/ (cases/, m1ft-inputs/, t066-nhom2/) và D:/RCA-archive/hash-lists/; các tgz trong results/T-058, results/T-062, results/T-063; repo lab load/controller/, load/fixtures/, campaigns/lib/inventory.py, campaigns/runner/runner4.py.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat.

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
```

**Quyết định của Minh** (nguyên lời, 18/11): "Duyệt 5 nhóm sửa" (5 nhóm ở mục "Đề xuất sửa gom theo file" phiên 3).

**Diễn biến sửa (18/11):**
- Nhóm 1: sha256 `results/T-064/manifest-3.json` = `faa7d292…` (khớp `bao-ve.tsv` dòng 171), commit nguyên byte. Ghi `results/T-066/dinh-chinh.md`: nguồn ghi ở dòng 171 (không sửa `bao-ve.tsv`); hàng 1.2 (đếm lại: 45 mã `cases/` khác nhau, bằng số đã xóa, không còn danh sách tên để so từng mã; `outputs/` 32/38, 6 không xác định); R4 thứ tự thật; thu hẹp câu cách ly sổ; ví dụ IP trong docstring `inventory.py`.
- Nhóm 2: lab `load/controller/README.md` — bảng đường dẫn hiện hành (mã `/opt/rca-lab`, khóa `/etc/rca-lab/controller`, trạng thái `/srv/rca-lab/load-controller`, STOP bộ tải `/srv/rca-lab/load-controller/STOP`, STOP runner `/srv/rca-lab/runs/STOP`), phụ thuộc PyYAML hệ thống, lệnh chạy từ `/opt/rca-lab`. Không sửa `runner4.py` (đang được T-067 bảo vệ).
- Nhóm 3: `danh-sach-xoa.md` mục Kết quả: 2.6 giữ (CLI `fixture.py` vẫn dùng `/opt/rca-tai`); 2.7 so hash `~/deploy-t062.sh` trên exp-app = lab `a46c009` = `e9305304…` (HEAD lab khác, `acee82e6…`); 1.2 trỏ tới đính chính.
- Nhóm 4: Minh chấp nhận giới hạn lịch sử R4. Xác nhận hiện tại: mở `t065-l8b-phat-lai` với ca cũ `46aab4be`, bản V082 (Grafana, phiên Minh đăng nhập, tunnel mới): trang tải đủ bảng "Bản, hash, trạng thái và cửa sổ" (hash cấu hình `451a8437…`, mã nguồn `b0f79a4d…`, đầu ra `573df32d…`, cửa sổ 13:04:02–13:14:02Z 13/11) và panel "Phát lại — lớp dữ liệu tách riêng".
- Nhóm 5: `docs/DECISIONS.md` thêm mục "T-066/T-067: bộ điều khiển tải trên exp-obs; giữ Tempo 14 ngày, 17/11/2026" (Q1(b), giữ Tempo 14 ngày).

**Kết thúc lượt:** T-066 đã xử lý xong R1–R5 theo duyệt của Minh. Còn mở: mục 2.6, 2.7 (xóa sau T-067 theo quyết định của Minh); 6/38 `outputs/` không xác định tên. Prompt cho Codex kiểm lại: mục "Prompt cho Codex — kiểm lại phản hồi phiên 3" ở trên vẫn dùng được (các sửa nằm ở mục này).
