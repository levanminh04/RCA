# Phản biện T-063 — lượt 4, kết quả thu bù 3

- **Người phản biện:** Codex — **Ngày:** 14/11/2026. **Commit/diff đã đọc:** RCA HEAD hiện hành, đầu ra chưa commit; FlashTicket commit nêu trong prompt và cha của nó, đối chiếu worktree build thực.
- **Công đoạn/cổng và bản lượt:** soát kết quả; chiến dịch M1-FlashTicket, M3; chỉ tạo `REVIEW-4.md`. Đã liệt kê thư mục, chưa có bản này. Claude làm; Codex phản biện.
- **Đã đọc:** AGENTS, STATE, SPEC và mục cuối LOG T-063; brief phiên B; chiến dịch mục 4–7; mục tiêu/RQ trong MRP, DT18, hướng dẫn cô, LESSONS; DECISIONS phần quyền chiến dịch, hook H3, hai sửa hậu kiểm và đáp án H4; WHY liên quan. Đọc kế hoạch/checkpoint, thay đổi máy, điều kiện, lịch, script, manifest, sổ, audit, tải và gói thật thu3; runner3/inj2/exporter/P7; báo cáo, ô dev, đóng băng và yêu cầu phiên C. Sau tự soát mới đọc REVIEW, REVIEW-2, REVIEW-3 và phản hồi.
- **Tự soát độc lập:** kiểm hash trước dùng; lần tiêm → đầu dò → hậu kiểm → gói → input/output P7. Đọc nguyên bản RECREATE-PAY trên exp-obs; log test và worktree build trên exp-app. Lập nhận xét riêng trước kết luận cũ. Không chạy lại tải, tiêm hay M1.

## Kết luận chung

**Không có điểm CHẶN việc dùng dữ liệu thu bù 3 để phân tích dev.** H3/H4 có can thiệp được xác nhận, đối chứng ×3 hợp lệ theo sửa Minh đã nhận; RECREATE-PAY có dữ liệu thật và đúng điều kiện lỗi adapter. R7 là lỗi khớp manifest của tài liệu hiện hành, không phải hỏng dữ liệu thu.

Phần thu bù đạt mục tiêu cung cấp đầu vào của brief B. Chưa từ đó kết luận H3/H4 có ích, hoàn tất M3, nghiệm thu toàn T-063 hoặc trả lời hiệu quả đồ thị/RQ5. Phần ấy cần kết quả và phân tích T-064 cùng các câu hỏi còn mở của T-063.

## Các điểm

### R7. Manifest thu3 chưa bao phủ dòng duyệt nối thêm — KHÔNG CHẶN dữ liệu

- **Ở đâu:** `results/T-063/thu3/manifest.json#/file/dieu-kien-xac-nhan-3.md`; file điều kiện hiện tại, dòng cuối ghi Minh nhận hai sửa. Manifest tổng `results/T-063/manifest.json#/file_tong_thu_muc_con/thu3/` vẫn ghim manifest con cũ.
- **Sai gì:** kiểm toàn vẹn theo bản kê hiện có thất bại cho tài liệu điều kiện hiện hành. Đã báo lệch và dừng dùng nó như bản khóa để truy nguyên. Không có bằng chứng đổi lén điều kiện hay dữ liệu.
- **Bằng chứng:** 85/86 mục `file` cộng `ngoai_thu3` khớp; chỉ file trên lệch. Node crypto kiểm: cắt đúng đoạn bắt đầu `**Minh nhận`, `trimEnd()` rồi thêm một newline cuối cho lại đúng hash manifest con. Cắt thêm mục `## Sửa sau` theo cùng cách cho lại hash điều kiện trong `dong-bang-3.json#/laptop_file_sha256`. `scripts/xac_nhan_ca_3-ban-chot.py` cũng khớp pin script trước sửa. DECISIONS có nguyên lời Minh nhận hai sửa; đây là nối ghi nhận quyết định, không phải sửa điều kiện không khai báo.
- **Bước/quyết định chịu ảnh hưởng:** lỗi đóng gói hồ sơ đã xảy ra; không chặn H3/H4/H8 hay buộc thu lại. Chưa thể gọi toàn bộ tài liệu thu3 hiện hành đã khớp manifest con. Agent sau kiểm hash đúng luật sẽ phải truy nguyên lại lệch này.
- **Đề xuất sửa tối thiểu:** giữ manifest/bản khóa cũ. Trong gói hồ sơ được phép, tạo `results/T-063/thu3/manifest-2.json` ghim tài liệu sau dòng duyệt và `results/T-063/manifest-2.json` dẫn bản kê con mới, dùng cơ chế manifest hiện có. Không sửa dữ liệu, script, điều kiện khóa hoặc kết quả. Ưu tiên cách này vì giữ hai trạng thái; mặt trái là thêm phiên bản cần dẫn rõ. Sửa đè manifest cũ ít file hơn nhưng mất bản kê bàn giao đầu nên không đề xuất.
- **Ảnh hưởng pin:** manifest con cũ đang được manifest tổng ghim. Hai file đề xuất chưa tồn tại lúc soát; tạo chúng không đổi pin lượt thu hoặc byte dữ liệu T-064 tính. Không cập nhật âm thầm pin cũ cho khớp. Reviewer chưa sửa các file ấy.

## Đối chiếu các lượt trước

Không tự mở lại phần đã xử lý ở lượt 3. Bảng này kiểm phản hồi đối với hiện trạng/thu3, không nhận đã lặp toàn bộ phân tích thu2.

| Điểm và phản hồi | Đánh giá độc lập lượt này |
|---|---|
| R1 — cleanup lỗi vẫn sang ô sau | **Đúng; sửa còn trong đường thực thi.** `runner4.py:98–118,200–206,242–251` truyền lỗi dọn, verify trước ô, dừng khi không sạch; inj3 giữ tự hết hạn toxic/pause. Code khớp đóng băng 3; sổ thu3 không dirty/cycle-error. Không suy mọi lỗi hạ tầng đã được thử. |
| R2 — tích hợp cuối/phục hồi | **Đúng; có bằng chứng cho thay đổi thu3.** Lượt ngắn có gói/băm, năm gói chính qua đường thật. H4 bị guard chặn đã stage lại mã mới cùng t, giữ lần cũ rồi có output; nhánh trước đây chưa gặp ở thu2 nay đã được dùng. RECREATE-PAY lỗi cả hai lần, vẫn giữ ca và không dừng lượt. |
| R3 — xác nhận hậu kiểm | **Đúng; xử lý hợp lệ.** Thu3 có bản điều kiện băm trước phát. Hai JSON giữ riêng, chỉ C0 của `1e5a3dc5` và điều kiện phục hồi httpcheck của `ebd5ef38` đổi false→true. Minh đã nhận cả hai; không xin lại quyền. |
| R4 — cách tiêm CPU khác chứng minh cô lập | **Đúng ở mức giới hạn đã sửa.** Đã đọc đính chính `chay/D2B-KET-QUA.md`; vẫn tách hai mức. Thu3 không chạy CPU, không có chứng cứ mới nâng kết luận. Không kiểm lại số CPU thu2 trong lượt này. |
| R5 — thiếu cha/CLIENT khác | **Đúng; phản hồi giữ giới hạn.** Báo cáo §7 phân biệt cha ngoài cửa sổ với Payment thiếu cha trong cửa sổ, nêu hai giải thích/dữ liệu thiếu; không quy hạng M1 cho số span. Không truy lại toàn bộ thu2 ở lượt này. H3/H4 thiếu ô nay đã có đầu vào tương ứng. |
| R6 — đã loại autovacuum/checkpoint | **Đúng; câu sửa không còn nói đã loại.** Báo cáo §3/§7 nói phép đếm chưa phân biệt; vắng log khóa không loại khóa ngắn. Thu3 không phân xử nguyên nhân cờ nền thu2, không buộc thu mới để đóng finding đã sửa. |
| N1 — hash sổ | **Đúng; thu3 kiểm trực tiếp 60 dòng**, seq và prev_sha256 đúng. |
| N2 — hết hạn → chờ → tự gọi lại | **Chưa kiểm được chu trình thật trong lượt này.** Không có đầu ra điều phối mới được trình cho thu3; thu tự chủ trên máy không thay phép thử ấy. Giữ theo hồ sơ M0, không chặn nhánh độc lập. |
| N4 — P7 theo ca | **Đúng trong phạm vi thu3:** kiểm năm cặp output, không chỉ nhật ký. RECREATE-PAY được báo ERROR adapter, không gộp vào P7 OK. Không kiểm lại 13 cặp thu2. |
| Đích PUT/GET trong phản hồi lượt 3 | **Chưa kiểm lại** dữ liệu thu2 ở lượt này; không nâng mức từ lời hai agent đồng ý. Báo cáo vẫn ghi rõ nguồn của nhận định. |

## Tuân thủ quy trình

- Vai trò đúng SPEC. Chỉ tạo bản review được giao; không LOG/STATE, sửa kết quả/máy, commit/push hoặc gọi agent. Không đọc dữ liệu khóa, ô đánh giá, repo lưu trữ, env, lịch sử shell hay nội dung khóa.
- Quyền hook/build/thu bù có trong DECISIONS/brief B. Diff commit FlashTicket chỉ chạm hai file dưới Event `src/rca-test`. Worktree build thực dùng đúng nền đang chạy cộng bản vá, không lấy đầu nhánh đã đổi nghiệp vụ. Quyền chiến dịch cho điều phối tổ chức review đã có.
- Mức pool, tải ×3 và build riêng có lý do/phương án khác trong kế hoạch và đề xuất WHY; điều phối đã chép WHY theo đường bàn giao trước khi T-064 dùng để chọn. Lệch ngưỡng khả thi H4 được khai trước phép thử trực tiếp. Minh nhận sửa hậu kiểm không biến chúng thành tiêu chí khai trước.
- LOG/BAN-GIAO-B/báo cáo giữ các câu chờ Minh và manifest chưa có của thời điểm bàn giao. DECISIONS/WHY và manifest tổng đã có trạng thái mới. Không hỏi lại hai sửa hoặc A/B của H4 vì câu lịch sử chưa đồng bộ, không sửa đè LOG.
- Python laptop không chạy được trong sandbox; dùng PowerShell băm, Node đọc tar trong bộ nhớ và Git SSH chỉ đọc. Không cài môi trường, đổi ACL hoặc chép khóa. Những lần đọc thiếu quyền/schema được chỉnh về đúng user/cấu trúc, không phát sinh thay đổi máy.

## Điều đã kiểm và thấy đúng

### Toàn vẹn và thực thi

| Kiểm đã chạy | Kết quả và nguồn |
|---|---|
| Manifest tổng | **186/186** mục `results/T-063/manifest.json#/file` khớp. Không thay kiểm đệ quy manifest con. |
| Manifest thu3 | **85/86** mục trực tiếp/ngoài thu3 khớp; hai SHA256SUMS con đúng hash. `thu/`: **93/93**; `thu-ngan/`: **21/21**. R7 nêu phần duy nhất lệch. |
| Đóng băng | **19/21** pin laptop còn nguyên tại đường gốc; hai pin thay có bản trước sửa khớp như R7. So đủ khóa chung đóng băng 2/3: chỉ image Event đổi trong exp_app_image_id; khóa hash chung app/obs/laptop không đổi. Không suy trạng thái máy bất biến qua toàn thời gian. |
| Sổ/lịch | `thu/tiem-loi/so-thu3.jsonl`: **60** dòng seq liên tục, prev_sha256 bằng SHA256 dòng UTF-8 trước bỏ newline; đầu là 64 số 0. **6** cycle-begin/load-start/cycle-end; không cycle-error/dirty/fault-start-failed. Lịch khớp thu3-begin, phase_s=600. |
| Tải | `thu/tai-out/t3-<mã>/{state,run,summary}.json`: **6/6** ExitCode=0, multiplier đúng sổ, bộ đếm khớp JSON hậu kiểm. Không coi ExitCode=0 là không có hành trình lỗi. |
| Archive P7 | **5/5** hash archive khớp nhật ký; **25/25** file nguồn bên trong khớp byte/hash manifest ca. **5/5** input khớp summary.input_sha256; **10/10** output khớp summary.output_sha256, **5/5** cặp trùng byte, status OK. Là kiểm đầu ra đã lưu, không chạy lại phương pháp. |
| Source P7 | **39/39** pin source local khớp `_nguon/m1-source-pins.json#/pins`; run-m1 khớp pin đóng băng. Đường đọc chỉ lấy case allowlist/bảy đối số, có guard trường/giá trị cấm, không đọc sổ/audit/tên ô để chọn đặc trưng hay ứng viên. Đây là chế độ biết mốc, chưa là kiểm tự phát hiện. |
| Guard H4 | Trong `659a9dfb1ab0.tgz!outputs/659a9dfb1ab0/method-input.json`, mã gốc xuất hiện **1 lần**, tại `[0][93156].spanID`, là chuỗi con của spanId. Không có bằng chứng nhãn lọt. Retry giữ cùng t, không chọn cửa sổ theo điểm. |
| Build thực | Đọc `exp-app:~/t063/thu3/event-test.log`: **8 test, 0 failure/error/skipped**, không chạy test mới. `git diff --name-only HEAD~1 HEAD` của worktree chỉ hai file Event rca-test, cha đúng nền; patch khớp hash đóng băng. |
| Đối chứng cũ/mới | Sau kiểm hash sổ thu2 và file liên quan trong manifest tổng, đối chiếu **7 ca**, bộ đếm tải và **21** trường PSI ở ba mốc trong `so-sanh-o-cu.json` khớp nguồn. Không dùng số cùng cỡ làm bằng chứng mọi điều kiện máy tương đương. |

### Can thiệp và trung gian

Các số hậu kiểm dẫn `results/T-063/thu3/xac-nhan-ca-3-sua-sau.json#/ca/<mã>`. Truy vấn lại Prometheus trên exp-obs chỉ đọc, đúng cửa sổ đã khai, bước 15 s.

| Ca | Kiểm độc lập và kết quả |
|---|---|
| POOL-EVENT `86dea661` | Audit đầy đủ có **5** pool.hold.started trong pha; không pool.* ở hai khoảng cấm. Query `max(db_client_connections_usage{service_name="event-service",state="used"})`: tb N/L/sau **0,027/5/0**, L có **37/37** điểm bằng 5. Pending N tb=0, L max=**22**. Khớp pool_used_tb_N_L_sau và pool_pending_tb_N_maxL. Active audit đo trước chiếm, không dùng thay mức pool lúc giữ. |
| H4 `659a9dfb` | Từ sổ probe.rabbit_booking: tồn t+60/t+330/hoi+60 **4/654/0**; toxic đúng booking-amqp rồi hết; cùng connection PID và trạng thái running tại các đầu dò. Đối chứng ×3 tồn **0 ở 4/4** đầu dò, không toxic/burn/pause/hook. Cơ chế là giới hạn giao message, không chứng minh khâu xử lý consumer chậm. |
| RECREATE-PAY `ebd5ef38` | Id đổi, ba đầu dò sau cùng Id, StartedAt khoảng t+5. Range-vector `httpcheck_error{http_url=~".*:8083.*"}[600s]` tại t+570 chỉ có mẫu lỗi ở **t+3,13,23,33,43**. Query_range theo điều kiện cũ vẫn có 1 ở **11** điểm trong t+180…t+570. Khớp lý do sửa lookback, không phải liveness thật hỏng suốt khoảng ấy. |
| RECREATE-PAY, nguồn thô | `exp-obs:/opt/flash-ticket-rca/cases/ebd5ef38/manifest.json#/files`: **5/5** khớp; hash manifest đúng bàn giao. Raw log Payment: **1.440** bản ghi trước t, **1.265** sau t. CPU/mem mỗi kênh có **2** runtime series Payment: native cũ kết thúc t+3,297, mới bắt đầu t+13,300. Adapter local/remote trùng byte; dòng 152–154 từ chối hai identity cho cùng metric logic. Xác nhận chuỗi input → lỗi adapter, không chỉ tin thông báo runner. |
| Bổ sung | Năm gói local khớp nhật ký; **6/6** trên exp-obs khớp `/opt/rca-m1ft/bo-sung-dev3/SHA256SUMS` (bản kê chung ở gốc). POOL có pool-used/pending đúng service; H4 có queue theo tên. Exporter không đọc sổ; thành phần H4 dùng tiền tố queue tĩnh để gán service, không lấy service gốc từ nhãn ca. Chưa đánh giá lợi ích phép ánh xạ trong lượt này. |

Hai JSON hậu kiểm chỉ khác đúng hai trường điều kiện đã nêu ở R3. Minh đã nhận trong DECISIONS; việc hỏi lại trong bàn giao cũ không đảo quyết định ấy. Đáp án H4 cũng đã được chọn A, báo thêm B; giữ khai đây là thay sau khai trước.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm:** soát file/code thật và hai máy chỉ đọc; kiểm pin, sổ, gói, đầu dò và trung gian adapter; đối chiếu các finding/phản hồi cũ sau tự soát. Không thêm quyết định chính thức.
2. **File đổi:** chỉ `tasks/T-063-quan-sat-thu-dev-2/REVIEW-4.md`, gồm prompt và bảng đáp trống. Không LOG/STATE, source, kết quả, manifest, máy hoặc commit.
3. **Kiểm:** các bảng trên; không thực nghiệm mới. Không tái kiểm toàn bộ thu2/mọi thành phần M1-FT; trùng byte không tự là bằng chứng hiệu quả.
4. **Còn mở và đề xuất:**

- **R7:** đề xuất điều phối bổ sung hai manifest phiên bản mới trong quyền, giữ bản cũ. Chi phí băm/ghi hồ sơ dự kiến vài phút, chưa đo; không cần thu hoặc P7 lại. Chưa có phản hồi R7, chưa gọi là bất đồng hai bên.
- **H3/H4/H8:** đề xuất tiếp tục T-064 bằng kết quả đã có, giữ tách bản 2/3 và ×1/×3. Thu xác nhận can thiệp, không phân xử lợi ích phương pháp với tín hiệu/quan hệ khác. Đọc biến thể/trung gian/đối chứng đã lưu trước khi tính phần thiếu, không đề xuất thu mới. Mặt trái: một lần thu mỗi ô, chưa đo dao động, chỉ báo bằng chứng có điều kiện. Chi phí phần phân tích theo hồ sơ T-064 hiện hành, không phát lô thêm ở lượt này.
- **PSI bản 3:** chưa tách được watchdog Event, tải nền theo thời gian hoặc dao động máy từ ba điểm/ca. Đọc CPU/PSI đã lưu quanh hai đối chứng có thể kiểm một phần, dự kiến 10–30 phút chưa đo; không có cặp can thiệp đối chứng đủ để quy riêng tác dụng watchdog. Đề xuất giữ giới hạn, không gọi hai build tương đương hoàn toàn hay thu lại chỉ để làm đẹp nền. Quy nguyên nhân cho build/gộp không phân tầng phụ thuộc bằng chứng bổ sung.
- **Câu hỏi cũ:** Payment thiếu cha còn hai giải thích đến muộn sau snapshot hoặc bị bỏ ở capture/xuất; cần snapshot/log exporter tương ứng nếu còn. Cờ nền còn autovacuum/checkpoint/I/O hoặc khóa ngắn chưa tách bằng đếm. Đề xuất rà nguồn lưu cần cho quyết định cơ chế, dự kiến vài chục phút nếu còn; nếu không còn, giữ giới hạn, không gán nguyên nhân hay tự loại ca. Không mở lại finding đã sửa và không coi thu3 đã làm xong phần này.
- **Trạng thái cần Minh:** hai sửa và A/B của H4 đã có lời quyết, không hỏi lại. Đề xuất nhận phần dữ liệu thu bù đã kiểm; chưa nghiệm thu toàn T-063/M3 chỉ từ review này. Phép thử điều phối/phần hồ sơ còn lại theo nguồn task. RECREATE-PAY chưa có tgz, dữ liệu giữ ở exp-obs đã kiểm tại chỗ; không tạo summary P7 giả để vượt safe-export ghim.

**Đề xuất một lượt người làm đáp ngắn cho R7 và các đề xuất trên; không lặp phản biện khoa học toàn thu3 hoặc chạy lại thực nghiệm.** Khi xử lý bản kê tài liệu hoặc Minh chấp nhận giới hạn snapshot đã xác định, không còn phản đối trong phần thu bù này và nên dừng phần đó. Minh quyết cuối; dừng không tự nghiệm thu task, khóa ứng viên, hoàn tất RQ5 hay mở test.

## Prompt bàn giao cho người làm

Chép nguyên văn Prompt chung và khối Người làm đáp phản biện từ `docs/review-prompt.md`, chỉ điền Thông tin lượt này. Giai đoạn 2/M3 không có khối cổng riêng. Reviewer không tự gửi.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-063 (tasks/T-063-quan-sat-thu-dev-2/), phần thu bù 3; người làm đáp REVIEW-4.md và phản biện các đề xuất trong bản đó.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: chiến dịch M1-FlashTicket, mốc M3 (tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md mục 4–7); giai đoạn 2 không có khối trọng tâm cổng riêng trong docs/review-prompt.md.
- Người làm và người phản biện chính thức: người làm Claude (T-063, phiên B và điều phối theo quyền chiến dịch); người phản biện Codex.
- Tài liệu gốc: tasks/T-062-dem-chang-1-4/PHIEN-B-BRIEF.md; tasks/T-063-quan-sat-thu-dev-2/SPEC.md và LOG.md; tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md; docs/DECISIONS.md phần chiến dịch và thu bù 3; docs/WHY.md phần T-063/T-064; results/T-063/bao-cao.md, o-dev-bo-sung.md, dong-bang.md; results/T-064/phien-c/YEU-CAU-O.md; repo FlashTicket D:/Project/flash-ticket-platform nhánh rca/quan-sat-log commit e557307 (cha fba6bc8), chỉ đọc.
- Phản biện và phản hồi trước: tasks/T-063-quan-sat-thu-dev-2/REVIEW.md, REVIEW-2.md, REVIEW-3.md và REVIEW-4.md, gồm các bảng phản hồi đã có.
- Code và kết quả liên quan: results/T-063/thu3/ (KE-HOACH.md, CHECKPOINT.md, BAN-GIAO-B.md, dieu-kien-xac-nhan-3.md, xac-nhan-ca-3*.json, so-sanh-o-cu.json, scripts/, do/, thu/, thu-ngan/, manifest.json); results/T-063/manifest.json; results/T-063/dong-bang/dong-bang-2.json và dong-bang-3.json; results/T-063/chay/runner3.py, tiem-loi/inj2.py, dong-goi/xuat_bo_sung.py; exp-obs và exp-app chỉ đọc theo CHECKPOINT.md, không in khóa.
- Phạm vi ghi được Minh cho phép trong lượt này: theo quyền người làm T-063 của chiến dịch: chỉ điền bảng Phản hồi của người làm cuối tasks/T-063-quan-sat-thu-dev-2/REVIEW-4.md và nối LOG.md của task; các file khác chỉ đọc trong lượt đáp này. Không sửa nhận xét hoặc prompt của reviewer; chưa rõ quyền thì trình phản hồi và đề xuất trong chat.

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
Công đoạn: người làm đáp phản biện. Giữ vai trò người làm, không là người phản biện chính thức của chính task.
Tự soát yêu cầu và mọi file đầu ra gốc cần để trả lời các câu hỏi như một người chưa từng làm task, TRƯỚC khi mở kết luận các bản phản biện. Ghi danh sách điểm tự tìm được vào LOG trước khi mở các kết luận ấy nếu được phép ghi; phiên chỉ đọc ghi nhận xét trong chat.
Sau đó kiểm từng điểm phản biện trên file/code/dữ liệu thật; chạy lại khi rẻ và được phép. Kết luận đúng / đúng một phần / sai / chưa kiểm được với bằng chứng riêng. Reviewer có thể sai, nói quá hoặc đề xuất sửa có mặt trái.
Nếu được Minh cho phép: điền bảng Phản hồi của người làm ở cuối đúng bản phản biện; thêm N1, N2… cho điểm tự tìm được với CHẶN/KHÔNG CHẶN; để trống cột Minh quyết; nối LOG đủ mục 7 của AGENTS, gồm đề xuất sửa gom theo file; chỉ cập nhật dòng task trong STATE khi được phép. Không sửa nội dung hay prompt của reviewer hoặc tự sửa báo cáo/code.
Nếu chưa có quyền ghi các phần này, trình phản hồi và đề xuất trong chat. Soạn prompt bàn giao cho người phản biện kiểm độc lập.
```

## Phản hồi của người làm (người làm điền sau)

Người làm chỉ điền bảng này và LOG theo quyền; giữ nguyên nhận xét/prompt. Thêm N1, N2… cho tự soát, để trống cột Minh quyết. Prompt lượt đáp nằm trong LOG hoặc chat theo quyền.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R7 | Đúng; KHÔNG CHẶN | Tự kiểm 16:00Z: `thu3/manifest.json#/file/dieu-kien-xac-nhan-3.md` = b2501dae…, file hiện tại = 62b42bff…; khác do dòng "Minh nhận Sửa sau 1 và 2" nối sau khi lập manifest (lời Minh có ở DECISIONS). Không đổi dữ liệu hay điều kiện. Sửa đề xuất của phản biện (thêm `thu3/manifest-2.json` và `results/T-063/manifest-2.json`, giữ bản cũ) hợp lý; chờ Minh quyết, chưa làm. | |
| R7 (sửa) | Đã sửa theo duyệt của Minh 14/11 ~16:05Z ("duyệt") | Thêm `results/T-063/thu3/manifest-2.json` (87 file, gồm `dieu-kien-xac-nhan-3.md` sau dòng duyệt và ghim `manifest.json` cũ) và `results/T-063/manifest-2.json` (195 file; `thu3/` dẫn `thu3/manifest-2.json`; ghim `manifest.json` cũ), bằng `thu3/scripts/tao_manifest_thu3_2.py`, `dong-goi/tao_manifest_t063_2.py` (chép từ script cũ, chỉ đổi tên đầu ra). Hai manifest cũ không đổi byte. Kiểm: 0 file lệch, 5 tổng thư mục con khớp. Lập lại sau khi tạo `thu3/scripts/dung_prompt_kiem_lai_r7.py` và `codex/R5-brief.md`; file sinh sau (log, kết quả R5) ngoài bản kê. | |
