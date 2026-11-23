# Claude: kế hoạch điều phối bản 4 (đáp phản biện bản 3)

> Nguyên văn, trích bằng script từ `debcb98c-9a36-447f-b07c-8820bd290ab4.jsonl` (dòng 1295). Không biên tập.

Đã đối chiếu xong. Lưu ý về tính độc lập: kết luận của Codex được dán cùng yêu cầu, nên lượt này không có phần tự soát độc lập. Phần tự soát độc lập duy nhất là 10 điểm N1–N10 ở lượt trước. Nếu Minh cần một lượt soát độc lập thật, làm theo đề xuất của Codex: mở phiên Claude mới bằng khối A, dán khối B sau. Phiên này không chạy đoạn PowerShell của khối A, vì nó dành cho phiên mới và đọc file đính kèm của Codex. Lượt này chỉ đọc, không sửa file nào.

## 1. Kiểm từng điểm của Codex

| Điểm | Kết luận | Bằng chứng riêng |
|---|---|---|
| Q1: duyệt ngoại lệ cho demo; thu hẹp câu "không bản nào tốt hơn"; khai trước ca nghiệm thu W5, giữ lần đầu kể cả trượt | **Đúng** | Kết luận chỉ đúng cho 5 bản (P7, V060, V061, V066, V082) trên 3 gói đã kiểm (`phan-tich/bien-the/hang.txt`) |
| Q2: cập nhật theo **giá trị đích** đã có ở Event/Booking, không "+14 ngày" | **Đúng, và tốt hơn đề xuất của tôi** | Nếu đứt kết nối giữa chừng, chạy lại theo giá trị đích không bị cộng hai lần; điều kiện `WHERE` cũ của T-069 chỉ chặn được vì khớp giá trị cũ |
| Q3: bỏ lập luận "mốc nhỏ = xóa dữ liệu" | **Đúng** | Có thể dựng mốc nhỏ trên một bản sao riêng nếu sau này cần phân xử |
| Q4: không tăng bậc được ở phút 40 | **Đúng, đã kiểm** | `tai_linux.py:234` đòi `minRefreshRemaining > step + 60` (> 2460 s); 24/24 lượt T-069 chỉ có 1784–1787 s |
| Q4: liveness phải phân biệt lần dò tốt, lần dò lỗi và thiếu hẳn lần dò | **Đúng** | Khớp N7 của tôi: `httpcheck_error` chỉ có chuỗi khi có lỗi |
| Q4: không mặc định token mới làm Keycloak lớn lên; không áp hệ số ×3 cho cả DB | **Đúng** | N4/N5 của tôi chỉ là lý do để đo, không phải kết luận |
| Q5, Q6 | **Đúng** | — |
| Q7: chưa đóng hay commit cả gói ngay | **Đúng** | Lượt Codex kiểm lại T-069 (LOG:396) chưa chạy; nghiệm thu là quyền Minh. 198.855.654 byte `raw.json` có trong cả hai manifest (đã đếm) |
| Q7: chỉ stage dòng T-069 trong STATE | **Đúng** | `docs/STATE.md` lẫn thay đổi của T-066/67/68 |
| E2: chốt tập chọn ngưỡng và ngân sách trước khi phát; không kéo dài theo tiến độ viết luật | **Đúng** | Đề xuất "kéo dài tới khi T-071 sẵn sàng" của tôi để tiến độ một phiên quyết định lượng dữ liệu dùng chọn ngưỡng. Bỏ |
| I3–I5: Prometheus đang phục vụ đo nền thì truy vấn đoạn lịch sử vẫn có thể làm nó quá tải | **Đúng** | Phân tích nặng phải chạy trên dữ liệu đã xuất riêng |
| Bộ tải đòi cây triển khai sạch | **Đúng, đã kiểm** | `tai_linux.py:119–128`: `git status --porcelain -- load campaigns inventory` phải rỗng. Code đang viết phải ở checkout khác |
| "Lỗi chỉ mất tối đa một lượt" | **Đúng** | Chỉ đúng với lỗi cục bộ. Sai luật, sai nguồn hoặc mất telemetry nhiều giờ làm hỏng nhiều lượt; ngược lại, laptop mất mạng không mất lượt nào (lượt lặp T-069 xong 4/4) |
| Bài học lịch cũ: khoảng trống 75 phút; lượt dò chỉ thấy `codex.exe` mà không biết mã việc | **Đúng** | `LICH-TU-TIEP-NHAN.md` mục "Sửa cơ chế 14/11". Lịch M1 cũ đã không còn (danh sách lịch hiện rỗng) |

Không có điểm nào tôi cho là Codex sai.

## 2. Kế hoạch điều phối bản 4

### 2.1. Ba lớp quyền, tách rõ
- **Minh đã quyết:** chạy song song bằng nhiều phiên; không đợi đêm; chọn phương án B ở T-069.
- **Codex đồng tình** (với tư cách phản biện; chưa phải duyệt): Q1–Q6 với các sửa ở mục 1; một người giữ T-069; bản nháp gửi FlashTicket.
- **Đề xuất mới chờ Minh duyệt:** mọi nội dung trong mục 2.2–2.8.

### 2.2. Phân công

| Phiên | Task | Model/mức (lý do) | Đầu vào sẵn | Đầu ra / nơi ghi | Tài nguyên | Bắt đầu | Làm ngay khi chờ |
|---|---|---|---|---|---|---|---|
| **Điều phối** | T-070 (mới): điều phối giai đoạn 2 | Opus 5.5 High/XHigh, do Minh chọn | Kế hoạch §8, T-069, các phản biện | `tasks/T-070-…/` gồm SPEC, LOG, `TRANG-THAI.json`, `LICH-MAY.md`, `HOP-DONG.md`; dòng T-070 trong STATE | Không tự chạy máy | Sau duyệt | Soát chéo SPEC, gom câu hỏi |
| *(T-069)* | T-069 | phiên Điều phối giữ | `dinh-chinh-1.md`, LOG phiên 3 | Chỉ nối dòng đính chính hash; còn lại chờ Codex kiểm lại và Minh nghiệm thu | — | Sau duyệt | — |
| **nen-w4** | T-071: W4a, đo nền | High (thao tác máy và dữ liệu có rủi ro) | Bộ tải, bản ghim, sổ T-069 | `results/T-071/`; máy theo khung giờ | **Chủ duy nhất** của exp-app, máy tải AWS và các lượt tải ở E1–E4 | SPEC duyệt | Soạn script ghi số đo theo lượt |
| **luat-w4** | T-072: W4b, luật cảnh báo | High (thống kê, tiêu chí) | Lượt 1 giờ T-067, các ca khỏe T-069 (đã xuất) | `results/T-072/`; nhánh repo lab riêng | Grafana chỉ ở E3 | SPEC duyệt | Viết luật, script chấm offline, bộ nhận webhook nhẹ |
| **rca-w5** | T-073: W5 | High (code tích hợp phức tạp) | Ca T-069 đã xuất, G1 | `results/T-073/`; nhánh repo lab riêng; checkout khác `/opt/rca-lab` | exp-app ở E5 | SPEC duyệt | Bộ xuất cửa sổ bất kỳ, G1 0.3, bộ điều phối, đo thời gian trên dev |
| **danh-gia-w6** | T-074: W6 | High (thiết kế khoa học; lên XHigh nếu lặp lỗi) | T-069, MRP, D14 | `results/T-074/` | exp-app khi rảnh, không nằm trên đường găng | SPEC duyệt | Toàn bộ phần thiết kế |
| **llm-w8** | T-075: W8 | Medium (phạm vi demo tối thiểu) | Đầu ra G1 đã có | `results/T-075/` | Không | Q6 duyệt | Toàn bộ |
| **quyển / tồn đọng** | theo task sẵn có (T-057…) | Medium | Kết quả đã có | Theo SPEC từng task | Không | Minh chọn | — |

**Đổi mức model:** nếu một phiên lặp lỗi hoặc không tiến triển, phiên điều phối ghi ví dụ cụ thể và phần việc bị ảnh hưởng, báo Minh xem xét tăng mức, và giữ checkpoint trước khi đổi. Không tự đổi model của phiên điều phối.

**Codex qua terminal** chỉ nhận việc phụ có đầu vào, đầu ra và tiêu chí rõ: đối chiếu hash, rà đường code, kiểm diff, đối chiếu bảng. Lệnh mẫu chỉ đọc:

```powershell
$brief | codex exec -C D:/RCA-flashticket -m gpt-6.2-astra -c 'model_reasoning_effort="high"' -s read-only --json -
```

Chạy nền; mã việc và thread ID ghi vào `TRANG-THAI.json`. Ba tình trạng xử lý khác nhau: hết usage thì báo Minh ngay để đổi account; mất mạng thì thử lại; lỗi lệnh thì sửa brief. Các lượt này không thay lượt phản biện chính thức.

### 2.3. Hợp đồng giữa các phiên (ghi vào `HOP-DONG.md` trước khi trình các SPEC)
- **I1 — Bản ghi cảnh báo:** gồm ba thời điểm khác nhau: t̂ là lúc luật chuyển sang firing theo lần đánh giá; giờ webhook tới; khoảng dữ liệu lõi RCA thực nhận. Kèm mã luật, nhãn và giá trị tín hiệu. Chế độ (b) không đọc sổ tiêm.
- **I2 — Lịch tải nền:**
  - Lượt ×1: 3600 s, không tăng bậc.
  - Lượt flash: 1800 s, tăng bậc ở 600 s, đúng cấu hình đã chạy khỏe (`124242f0`).
  - Khai trước thứ tự lượt và số phút khỏe cần thu cho từng mức tải.
  - Biên giữa hai lượt bị loại khỏi mẫu số.
  - "Không tiêm" không đồng nghĩa "khỏe": giờ khỏe phải đạt tiêu chí độc lập (k6: hành trình xong, `dropped_iterations`, 429, lỗi HTTP; cộng kiểm backend).
  - Mất quan sát, quota và suy giảm thật được ghi riêng từng loại.
  - Liveness ghi ba trạng thái: dò tốt, dò lỗi, thiếu lần dò.
  - Flash ở mức **chỉ mô tả**: số giờ quá ít để đặt tiêu chí đạt/trượt.
- **I3 — Phân tích nặng:** chỉ chạy trên dữ liệu đã xuất ra file riêng, không truy vấn Prometheus đang phục vụ đo nền.
- **I4 — Một chủ theo khung giờ** cho exp-app, máy tải AWS, Grafana và phần exp-obs chịu tải. Thay đổi Grafana chỉ ở E3. Bàn giao chủ ở E5 được ghi vào `LICH-MAY.md`.
- **I5 — Code:** code đang phát triển nằm ở nhánh hoặc checkout riêng. `/opt/rca-lab` chỉ checkout commit đã duyệt và phải sạch.
- **I6 — Ghi file chung:** mỗi phiên chỉ cập nhật dòng task của mình trong STATE, theo AGENTS, và lần lượt từng phiên. DECISIONS và WHY chỉ do phiên điều phối ghi, sau khi Minh duyệt.

### 2.4. Thứ tự dùng exp-app (ngân sách khai trước; không cam kết giờ xong)

| Bước | Việc | Ngân sách |
|---|---|---|
| E1 | Q2: đồng bộ theo giá trị đích, đọc lại cả hai phía; rồi chụp mốc DB, ghi số dòng thật và trạng thái đơn dở, hàng đợi, mock | Chưa đo; ghi thời gian thật |
| E2 | **Khoảng 1** (tập chọn ngưỡng, **cố định trước khi phát**): ví dụ 6 lượt ×1 + 2 lượt flash. Hết ngân sách thì dừng; luat-w4 dùng dữ liệu đã xuất | ≈ 7 giờ tải + khoảng chuyển lượt (chưa đo) |
| E3 | Chốt ngưỡng; nạp luật; xác nhận luật đang được đánh giá; ghi giờ luật có hiệu lực; kiểm webhook bằng một tín hiệu dương có kiểm soát, **ngoài** khoảng chấm. exp-app nghỉ trong lúc chờ | Ghi thời gian thật |
| E4 | **Khoảng 2**: cùng cơ cấu lượt như E2; chỉ tính sau giờ luật có hiệu lực | ≈ 7 giờ |
| E5 | Bàn giao chủ cho rca-w5; nghiệm thu W5 trên ca đã khai trước, giữ lần đầu | 1–3 chu kỳ × ~31 phút (đã đo) |
| E7 | Diễn tập W9a | — |
| E6 | W6 đo khôi phục DB khi exp-app rảnh; **không nằm trên đường găng W9a** | — |

Nếu trôi ở khoảng 2 buộc đổi ngưỡng, giữ kết quả lần đầu và kiểm bản sửa trên một khoảng mới.

### 2.5. Thức dậy và tiếp nhận (sửa đúng hai lỗi cũ)
- **Đánh thức chủ động, kèm tên việc:**
  - Các phiên con do phiên điều phối mở báo về khi kết thúc lượt; ứng dụng gửi tin có tên và mã phiên. Điều này sửa lỗi "chỉ thấy `codex.exe`".
  - Mỗi việc chạy trên server có một lệnh nền theo dõi, thoát khi việc chuyển sang trạng thái cuối.
  - Mỗi việc Codex chạy nền ghi mã việc và thread ID.
- **Dự phòng:** một lịch 15 phút bằng scheduled-tasks. Lịch chỉ đọc `TRANG-THAI.json` và nhắc phiên điều phối; không phát việc. Lịch cần ứng dụng Claude đang mở và có mạng. Xác nhận lịch chạy bằng `list_task_runs` sau lần kích hoạt đầu. **Tạo lịch là thay đổi cấu hình bền, cần Minh duyệt riêng.** Không bật lại lịch M1 cũ.
- **Mỗi lần thức:** xét xem có việc độc lập đủ điều kiện để phát không, rồi mới quay lại chờ.

### 2.6. Khi Minh di chuyển, mất mạng hoặc hết usage
- `TRANG-THAI.json` ghi cho mỗi việc: mã slot/tag, phiên chủ, lệnh đã phát, revision, máy, nơi đầu ra, hash, lần kiểm cuối, bước tiếp.
- **Trước khi phát lại bất kỳ thứ gì:** kiểm tag trên máy tải, container, nhật ký runner và manifest. Nhận lại đầu ra nếu việc đã xong. Không gọi lại nguyên lịch (runner sẽ sinh mã ca mới từ đầu); chỉ chạy lịch con cho phần thiếu.
- Chưa xác định được trạng thái thì giữ nguyên job đang chạy và làm việc độc lập khác.
- **Phạm vi lỗi:** lỗi trong một lượt chỉ hỏng lượt đó. Sai luật hoặc cấu hình, mất telemetry, Prometheus khởi động lại có thể hỏng nhiều lượt; mỗi lượt kiểm telemetry (Prometheus sống, số mẫu) để phát hiện sớm.
- Giữ cả kết quả lỗi. Chạy lại khi tính đúng đòi hỏi; mục tiêu "không làm lại" không được đặt trên chất lượng.

### 2.7. T-069 (tách khỏi kế hoạch này)
- Nối dòng đính chính hash vào LOG: `410d9923…` là danh sách tới M11; bản cuối là bản đã thêm M12, M13 và dòng kiểm DB chỉ đọc.
- Lượt Codex kiểm lại kết quả T-069 dùng prompt ở LOG:396, tách khỏi lượt phản biện kế hoạch này. Sau đó Minh mới nghiệm thu.
- Commit gồm: file T-069; chỉ dòng T-069 của STATE; DECISIONS và WHY phần T-069. Ba `raw.json` để ngoài Git, ghi đường nguồn trên exp-obs, đường đích và hash (đã có trong `nhan.sha256`) để máy mới dựng lại. Phiên fork bàn giao xong thì lưu trữ khi Minh đồng ý.

### 2.8. Minh quyết một lần
1. Q1–Q6 như mục 1; Q2 làm theo giá trị đích.
2. Mở task T-070 điều phối và các phiên T-071–T-075 như mục 2.2, mỗi phiên tự soạn SPEC; phiên điều phối soát chéo theo `HOP-DONG.md` trước khi trình.
3. Ngân sách E2 và E4: 6 lượt ×1 + 2 lượt flash mỗi khoảng, kèm ngưỡng báo giả ứng viên ≤ 1 sự cố mỗi 6 giờ khỏe ×1. Ngưỡng này Minh duyệt chính thức trong SPEC T-071/T-072.
4. Tạo lịch dự phòng 15 phút.
5. T-069: nối đính chính; gửi Codex prompt kiểm lại; chưa commit.
6. Chạy tiếp ở phiên này, hay mở phiên Claude mới theo khối A của Codex để có lượt soát độc lập.

## 3. Prompt cho Codex kiểm lại

Dán kèm nguyên văn mục 2 ở trên vào chỗ đánh dấu:

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: kế hoạch điều phối bản 4 cho W4, W5, W6, W8, W9a sau T-069 và phản hồi của người soạn cho phản biện kế hoạch bản 3, đang trong chat. Nguyên văn kế hoạch: <Minh dán nguyên văn mục "2. Kế hoạch điều phối bản 4">.
- Công đoạn: người phản biện kiểm lại phản hồi và sửa.
- Gói/cổng: kế hoạch giai đoạn 2 §8, chuẩn bị G6; đề xuất ngoài task.
- Người làm và người phản biện chính thức: ngoài task; người soạn Claude (phiên điều phối), người phản biện dự kiến Codex.
- Tài liệu gốc: docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8; docs/STATE.md; tasks/T-069-v082-ban-ghim/SPEC.md và LOG.md (phiên 1–3); results/T-069/dinh-chinh-1.md, results/T-069/phan-tich/ (troi-trong-luot.txt, bien-the/hang.txt, kiem-db.txt); docs/WHY.md WHY-102; docs/DECISIONS.md mục T-069 và mục "Sửa cơ chế lịch tự tiếp nhận"; tasks/T-062-dem-chang-1-4/LICH-TU-TIEP-NHAN.md, CHECKPOINT-CHIEN-DICH.md; results/T-058/dem-2026-11-10/dieu-phoi/GHI-CHU-CLAUDE-SANG.md.
- Phản biện và phản hồi trước: phản biện kế hoạch bản 2 và bản 3 của Codex (chat), phản hồi của người soạn (chat).
- Code và kết quả liên quan: results/T-069/ (SHA256SUMS, SHA256SUMS-2); D:/Project/flashticket-rca-lab commit 407b4f5 (load/controller/tai_linux.py, load/scenarios/purchase-journey.js, campaigns/runner/runner4.py, observability/grafana/); D:/Project/flash-ticket-platform revision 36a3725d.
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
```

```text
Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.
```

`docs/review-prompt.md` chưa có khối trọng tâm cho cổng G6.
