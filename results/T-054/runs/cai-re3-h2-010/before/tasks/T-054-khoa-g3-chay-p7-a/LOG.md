# Nhật ký T-054

Chỉ người làm nối LOG. Claude phản biện; nguồn chat được giữ riêng, không tạo REVIEW.md thay Claude. Không sửa mục cũ. Một task hai pha theo yêu cầu Minh; quyền hiện tại chỉ ghi hồ sơ.

---

## Phiên 1 — 05/11/2026 — Codex — Windows — vai trò: người làm

**Mở phiên:** đã đọc AGENTS, STATE, mẫu SPEC/LOG và phần chi phối của MRP/DT18/cô/WHY/DECISIONS/LESSONS; đọc SPEC và cuối LOG T-052. T-054 chưa có file trước lượt này. T-052 đã nghiệm thu dev/hồ sơ, không mở lại. Nguồn T-052 trước ghi: 576 đầu ra ổn định/93 pin code khớp; pin LOG/STATE giữ mốc lịch sử theo LOG nguồn.

**Công đoạn và mục tiêu nguồn:** đáp lượt soát SPEC cuối, kiểm điều kiện ghi Minh cấp, hợp nhất và ghi một SPEC hai pha G3(a)→P7(a). Bao phủ kế hoạch RQ3b/phần can thiệp RQ3d/vùng nghi ngờ, không báo đã có kết quả mới hoặc đã trả lời RQ3 đầy đủ.

**Quyết định của Minh trong phiên:**

- “nếu không có mâu thuẫn nào với claude hoặc phản đối nào thì cho phép ghi luôn , nếu có mâu thuẫn thì soạn trình claude phản biện”. Đã ghi Q-250. Nguồn nguyên lời tại results/T-054/runs/soan-spec-001/quyen-ghi.txt.
- Codex đã kiểm và nhận N1–N5 của lượt Claude cuối, không còn phản đối đối với phương án ghi. Quyền ghi không là quyền thực thi hay quyết thay các OPEN.

**Tự soát và khai thứ tự đọc:**

- Các lượt soạn/đáp trước đã kiểm nguồn/mã/đầu ra trước đối chiếu kết luận liên quan. Ở lượt này Minh đính kèm bản có cả kết luận/prompt; không khai rằng chưa từng thấy kết luận đó. Đọc lại nguồn trước quyết định tiếp nhận và ghi, không lấy finding thay chứng cứ.
- Gate mọi bảng cần gắn với đủ slot A4, không chỉ seal riêng A4. BLOCKED/PENDING không là kết quả phương pháp.
- C-c/C-g có nguồn T-050; native T-053 hỗn hợp máy từng cửa sổ. Max gap là mất quan sát; thiếu bằng chứng không tự gọi lỗi vận hành/phương pháp.
- Line ending/Git blob không thay gói byte thực chạy; code_root/data_root/output_root phải tách. IP/HostKeyAlias lịch sử không chứng minh hiện trạng máy. Cache phải kiểm ở laptop nơi áp dụng.

**Đánh giá phản biện:**

- Nhận F1–F4 và các sửa của lượt đáp trước. Nhận N1–N5 trong nguồn-phan-bien-002: gate A4 cho mọi bảng; T-050/máy nguồn/parity; max gap với ngưỡng khai trước; kiểm máy lịch sử khi có quyền; cache local và EC2 2 chỉ lô driver cần thiết.
- Bảng đáp và bằng chứng chi tiết ở results/T-054/runs/soan-spec-001/phan-hoi-002.md. Không còn phản đối chưa xử lý; đề xuất dừng phản biện SPEC theo điều kiện Claude nêu, Minh quyết. Không ghi rằng Claude đã kiểm file SPEC hợp nhất sau ghi.

**Diễn biến:**

- Khoảng 01:32 +0700 — kiểm lại nguồn, điều kiện quyền và pin; không SSH/chạy phương pháp/mở telemetry. Seal T-053 và 82 command pins cùng nguồn T-050 đã kiểm.
- Ghi SPEC hợp nhất, lưu nguyên byte hai nguồn phản biện chat và nguồn quyền, ghi bản đáp cuối. Biên tập câu/khoảng trắng trong SPEC, không đổi chính sách hoặc số liệu.
- Nối Q-250/WHY-78, sau đó thêm đúng dòng T-054 STATE. Không sửa AGENTS/MRP/LESSONS/src/kế hoạch hoặc file T-052; các thay đổi sẵn trước lượt được giữ.

**Phạm vi ghi phiên này:** SPEC/LOG T-054; bốn file tại results/T-054/runs/soan-spec-001/; manifest-soan-spec-001.json; nối DECISIONS/WHY và dòng T-054 STATE. Không tạo các script/protocol/env/runtime/test output dự kiến trong SPEC ở lượt này.


**Kết thúc phiên — ghi hồ sơ, chưa triển khai:**

1. **Đã làm:** ghi SPEC hợp nhất một task hai pha, nhận N1–N5 và đề xuất dừng phản biện SPEC. Lưu nguồn nguyên văn và đáp; ghi Q-250/WHY-78, thêm dòng T-054. Chưa có code hay kết quả thực nghiệm T-054.
2. **File thay đổi:** 10 file của gói, gồm SPEC/LOG, ba file docs (DECISIONS/WHY/STATE), bốn file nguồn/đáp tại runs/soan-spec-001 và manifest-soan-spec-001.json. Danh sách/hash đầy đủ trong manifest, không gộp các thay đổi user có sẵn vào gói.
3. **Kiểm:** đọc toàn SPEC hợp nhất; đủ 12 mục mẫu, 8 liên kết nguồn tồn tại, code fence cân; kiểm N1–N5/quyền/OPEN và cấu hình hiệu lực. Đếm G1 và công thức 684 slot baseline/616 core/658 M1-family/tối đa1462 đơn vị/4136 hàng chấm khớp. Seal T-053 và 82 command pins, hai nguồn T-050 khớp. Các nguồn chat giữ nguyên byte. Bảy file đã đổi sẵn ngoài ba docs giữ nguyên byte; DECISIONS/WHY chỉ nối, STATE chỉ thêm đúng dòng T-054. Kiểm hash manifest gói và git diff --check.
4. **Còn mở:** task mới đạt phần SPEC/hồ sơ; chưa hoàn tất pha 1 hoặc có căn cứ khóa G3. Ngoại lệ cạn ngân sách, TORAI A/grant nguồn, nguồn cấp/nhạy/timeout/maxgap/budget/lịch công bố khác và hạn sáng vẫn chờ Minh trước phần phụ thuộc. RQ3a/độ đúng vùng/cơ chế vật lý chưa được trả lời. Không còn bất đồng với Claude về nội dung được ghi; không coi internal check là Claude đã kiểm file sau ghi.
5. **Bước tiếp theo chính xác:** đọc SPEC mục “Phạm vi ghi”, bước 1–8 và bảng OPEN. Trình gói triển khai công cụ/fixture với đúng các file đã liệt kê, quyền pilot/local/SSH/sync TT dev, trần giờ và quyết định OPEN cần trước G3. Chỉ viết/chạy gói đó sau quyền tương ứng; không tự mở test/RE3 hoặc nguồn TORAI A. Nếu Minh muốn kiểm file đã ghi, dùng prompt trung tính bên dưới; không tự gửi hoặc tự mở vòng phản biện.
6. **Lệnh cuối cùng:** git diff --check sau kiểm manifest và file set cuối. Không chạy phương pháp, SSH, mở dữ liệu khóa, commit hoặc push.

**Đề xuất commit khi Minh duyệt riêng:** docs(T-054): ghi SPEC G3(a)-P7(a) sau soát. Chưa commit/push.

**Nguồn phản biện chính xác:** [lượt 1](../../results/T-054/runs/soan-spec-001/nguon-phan-bien-001.txt), [lượt 2](../../results/T-054/runs/soan-spec-001/nguon-phan-bien-002.txt), [bản đáp cuối](../../results/T-054/runs/soan-spec-001/phan-hoi-002.md), [quyền Minh](../../results/T-054/runs/soan-spec-001/quyen-ghi.txt).

---

## Prompt bàn giao của lượt này cho Claude

Chỉ dùng nếu Minh chọn chuyển để kiểm file đã ghi; Codex đề xuất dừng soát SPEC vì đã nhận các sửa. Prompt không tự cấp quyền ghi hoặc mở lại task/cổng, và không được tự gửi.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-054, tasks/T-054-khoa-g3-chay-p7-a/SPEC.md; hồ sơ đã ghi trong repo.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: chuẩn bị G3(a), thực thi và báo cáo P7(a).
- Người làm và người phản biện chính thức: Codex người làm, Claude người phản biện theo SPEC.
- Tài liệu gốc: AGENTS.md; docs/STATE.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; tasks/T-054-khoa-g3-chay-p7-a/SPEC.md.
- Phản biện và phản hồi trước: results/T-054/runs/soan-spec-001/nguon-phan-bien-001.txt; nguon-phan-bien-002.txt; phan-hoi-002.md; tasks/T-054-khoa-g3-chay-p7-a/LOG.md.
- Code và kết quả liên quan: results/T-054/manifest-soan-spec-001.json; results/T-052/manifest-dinh-chinh-g3-004.json; results/T-052/giao-thuc-p7-a-003.json; results/T-050/manifest-chay-lai-002.json; results/T-053/manifest.json. Môi trường và lệnh ở LOG T-052/T-054.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat nếu Minh chuyển prompt; không có quyền ghi từ prompt này.

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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```


## Phiên 2 — 05/11/2026 — Codex — Windows — người làm

Mở phiên: tiếp nhận từ Codex phiên 1, giữ vai trò người làm; Claude là phản biện chính thức. Minh giao tự soát độc lập từ nguồn rồi triển khai nếu không còn lỗi nghiêm trọng/CHẶN đối với phần tiếp theo. Nguồn nguyên văn: results/T-054/runs/trien-khai-001/quyen-minh.txt. Quyền này mở triển khai công cụ trong phạm vi SPEC; không chốt OPEN, không mở test/RE3/TORAI A, không commit/push. Nội dung hành chính về quyền cũ trong SPEC/STATE được đọc theo mốc lịch sử, không coi là mâu thuẫn với lệnh mới.

Thứ tự đọc: đọc luật/STATE/hành chính SPEC; dựng yêu cầu từ DT18/cô/MRP/WHY/DECISIONS/LESSONS, G1/P3/P4/P5/P6/T052 và code; ghi 5 nhận xét riêng trong chat trước khi đọc toàn SPEC và kết luận phản biện cũ. Không tạo REVIEW thay Claude.

Nhận xét riêng từ nguồn: (1) P7(a) kiểm xếp hạng và can thiệp tính toán, chưa trả lời phát hiện/vùng ảnh hưởng/topology thật. (2) Dev trái chiều theo TT/OB; chuỗi tính toán không chứng minh vị trí tiêm hay nguyên nhân vật lý. (3) Tái dùng cần đúng ca/cửa sổ/config/seed/env. (4) Guard ứng viên thiếu liên kết nhãn G1, đầu vào thực chạy và pha timeout; chặn khóa/chấm, không chặn cài wrapper. (5) Trước khóa cần driver/fixture/dev parity; sau grant mới chạy khóa, seal rồi ghép nhãn.

Kiểm nguồn trước dùng: 576 đầu ra ổn định T052, 297 mục T050, 2654 đầu ra T053, 93 pin code giao thức 003 khớp; LOG/STATE T052 là pin lịch sử đã loại riêng. Manifest soạn SPEC T054 có 9/9 mục khớp trước ghi. Cây có thay đổi user; before.json giữ dấu vân tay trước phiên.

Đối chiếu SPEC/nhận xét cũ: F1–F4/N1 đã có điều kiện xử lý trong SPEC; không còn lỗi nghiêm trọng chặn triển khai công cụ. Các thiếu A/B1/B2/C và quyền/OPEN còn chặn G3/test, không tự nhận đã gỡ. Triển khai đúng các nhóm Đầu ra trong results/T054, LOG và dòng STATE; không sửa nguồn/src/SPEC hoặc sổ quyết định.


### Đính chính thứ tự đọc và diễn biến triển khai

Lệnh đọc SPEC ban đầu đã xuất 48 dòng, gồm mục tiêu/bảng câu hỏi, rộng hơn hành chính. Không nhận lượt này là soát mù hoàn toàn. Năm nhận xét riêng trong chat có trước đọc toàn SPEC và kết luận reviewer; các kết luận giữ lại có đối chiếu nguồn/mã/đầu ra/phép kiểm. Đính chính này bổ sung mô tả mở phiên ở trên, không sửa lịch sử LOG.

Đã cài chín script task riêng: bien_nhan, nguon, worker, dieu_phoi, cham, p7, fixtures, pilot, lap_ho_so. Có CLI, nguồn/nhãn độc lập, invocation trước method, pha/monitor, process identity/token/claim/resume, M1/baseline/TORAI prep-method, C-d3 riêng, snapshot và chấm. Không sửa src/SPEC/nguồn lịch sử. Source-manifest được cập nhật có bản trước cho hai sửa nhỏ CLI UTF-8 và serialization NumPy; các freeze cũ giữ nguyên.

Tất cả lượt ở runs/trien-khai-001/attempt-history.json. Giữ fixtures-002 (thiếu drain3), 003 (epoch giả không hợp đồng SimpleRCA), 006/007 (chuyển cấu trúc khối/cạnh), và CLI lỗi encoding. Đã sửa wrapper/bộ sinh, không nới hợp đồng baseline. Không tính các lần kiểm lặp là kiểm độc lập.

### Kết thúc checkpoint phiên 2

1. **Đã làm:** tự dựng mục tiêu/bằng chứng từ nguồn, đối chiếu từng F/N và SPEC; không thấy lỗi nghiêm trọng mới chặn cài công cụ. Đã triển khai thực tế công cụ/fixture và hồ sơ ứng viên. Không coi nhận xét này là phản biện chính thức hoặc gỡ A/B1/B2/C ở G3. Quyết định khoa học thêm/đổi: không có. Nguồn quyền Minh lưu nguyên văn; các OPEN không được chốt thay Minh.
2. **File thay đổi:** chỉ LOG này, đúng dòng T054 STATE và các đầu ra trong results/T054: chín script, protocol/matrix/source/env/reuse/pilot-plan/authorization, ho-so-g3/runbook/report, các run/biên nhận/freeze/manifest. Không sửa SPEC, DECISIONS, WHY, MRP, AGENTS, src hoặc task nguồn; giữ mọi thay đổi user có sẵn. File set/hash cuối ở manifest-trien-khai-001.json.
3. **Kiểm đạt:** sources 576/297/2654 và 93 code pins; package SPEC 9 mục; bổ sung nguồn P4/P5/G1/T024/T026 và 82 native command pins. Fixtures004 83 kiểm với reader/core thật trên dữ liệu tự sinh; fixtures009 60 kiểm vận hành, gồm controller restart/adopt và C-d3 riêng. Fixtures008: 28 slot tổng hợp, A4/bảng 89 dòng, 4 vùng/2 vị trí. Semantic verifier 16 reader outputs; serialization NumPy/AST; CLI status/drain/resume/verify giữ một attempt. Freeze cuối 003 gồm 107 file đúng byte, chưa là G3. Kết quả/raw/tài nguyên giả đã giữ; không nhận là pilot hay hiệu quả thực nghiệm.
4. **Còn thiếu/cần Minh:** task chưa hoàn tất pha1; chưa có pilot thật/parity native mới/ba seed TORAI/cache-byte/đo concurrency/ETA toàn bundle/identity EC2. Giữ ERROR/TIMEOUT chưa phân loại là BLOCKED, không tự chấm 0. Chưa materialize nguồn/nhãn riêng, mở test/RE3/TORAI A, SSH/sync, commit/push. Cạn ngân sách, TORAI A, nguồn cấp, nhạy, hạn/monitor/budget/máy và G3/grant test còn OPEN. Hai câu hỏi về cạn ngân sách/TORAI A đã gửi Minh trong chat, chưa nhận câu trả lời lúc ghi checkpoint. RQ3b/d độc lập, RQ3a, độ đúng vùng, LLM/FT và giải thích vật lý chưa được trả lời mới.
5. **Bước tiếp theo chính xác:** đọc reports/tu-soat-001/bao-cao.md, ho-so-g3.md, pilot-plan.json và runbook.md; chạy CLI status bằng operator-fixture.json nếu cần kiểm công cụ. Sau khi Minh cấp đúng pilot/budget/nguồn: ghim plan dev tối thiểu từ candidates/native refs, map nguồn độc lập, môi trường prep/method, phân loại lỗi theo chính sách được duyệt; nối main seal với job C-d3 trong plan thật; pilot đủ tuyến/parity/chi phí trước đề nghị G3. Không phát lô test chỉ từ quyền triển khai. Xem mã nguon.authorize, worker.setup và p7.load_plan để xác định WAIT trước I/O.
6. **Lệnh cuối của checkpoint:** D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B results/T-054/runs/trien-khai-001/kiem_cuoi.py. Đây là validator chỉ đọc sau khi tạo manifest; kết quả in trong phiên.

Đề xuất commit sau khi Minh muốn lưu checkpoint: feat(T-054): công cụ P7 và kiểm dữ liệu giả. Chưa commit/push. Nội dung cần vào tài liệu chính thức sau duyệt: nguồn quyền triển khai mới và các quyết định OPEN khi Minh trả lời; phiên này chưa tự nối sổ DECISIONS/WHY.

### Prompt bàn giao dự phòng cho Claude — Minh tự chọn chuyển hoặc dừng

Không tự gửi hoặc mở vòng mới. Prompt chuẩn dưới đây không thay kết quả và không nhận task đã xong.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-054, tasks/T-054-khoa-g3-chay-p7-a/.
- Công đoạn: soát kết quả.
- Gói/cổng: P6/P7, G3.
- Người làm và người phản biện chính thức: Codex làm, Claude phản biện.
- Tài liệu gốc: AGENTS.md, docs/STATE.md, SPEC/LOG task; docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và advisor-2026-09-23.md.
- Phản biện và phản hồi trước: results/T-054/runs/soan-spec-001/nguon-phan-bien-001.txt, nguon-phan-bien-002.txt, phan-hoi-002.md.
- Code và kết quả liên quan: src/m1/, src/m1_danh_gia/, src/p3/; results/T-054/scripts/, reports/, manifest-trien-khai-001.json và runbook.md; các nguồn/pin được dẫn trong SPEC và source-manifest.json.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; chưa cấp file phản biện mới.

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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

Kiểm cuối lượt đầu dừng ở lỗi kiểu dữ liệu của validator: pin code lịch sử có cả chuỗi SHA và object. Chưa thấy hash lệch. Đã sửa đúng validator để đọc hai biểu diễn, giữ final-validation-001.json và manifest trước sửa; không sửa nguồn hoặc nới so hash. Lệnh kiểm cuối vẫn là kiem_cuoi.py nêu trên.


### Bổ sung trả lời Minh — 05/11/2026 — thời gian và TORAI A

Nguồn: Minh trả lời trực tiếp hai câu hỏi trong cùng chat.

- Về ngân sách, nguyên văn: “NGÂN SÁCH LÀ VỀ THỜI GIAN ? NẾU VẬY THÌ CHO TĂNG THỜI GIAN”. Câu hỏi đã gửi nói về trần thời gian chạy. Ghi nhận Minh cho tăng thời gian; chưa có mức trần mới bằng số. Tách tổng thời gian của lô với timeout mỗi lượt vì timeout đủ điều kiện có thể ảnh hưởng điểm. Không suy câu trả lời thành chọn một quy tắc chấm lượt chưa chạy khi cạn trần. Người làm lập dự toán mức cụ thể để trình, không yêu cầu Minh đoán số.
- Về TORAI A, nguyên văn: “Giữ TORAI A ở bảng phụ; cấp quyền nguồn riêng sau”. Giữ A ở bảng phụ ngoài A4. Chưa cấp quyền mở nguồn CSV tác giả. Ghi chú OPEN về giữ/bỏ A trong hồ sơ trước là mốc lịch sử trước câu trả lời này.

Đã làm: đối chiếu SPEC và lưu lời Minh. File thay đổi: chỉ nối LOG và tạo results/T-054/manifest-quyet-dinh-001.json. Kiểm: hash LOG trước ghi, SPEC theo manifest soạn SPEC và chín script theo manifest triển khai khớp; prefix LOG giữ nguyên. Chưa chạy thêm hay mở nguồn. Còn cần: dự toán trần thời gian cụ thể, quyền pilot, các chính sách/nguồn trước khóa. Không sửa SPEC/protocol/cách chấm hoặc ghi đè manifest cũ. Pin LOG trong manifest triển khai trở thành pin lịch sử từ bổ sung này; dùng manifest nguồn trả lời mới để tiếp nhận.

Bước tiếp: dùng lời Minh khi hoàn thiện gói pilot và trình cập nhật quyết định chính thức; TORAI A tiếp tục chờ grant nguồn. Nội dung đề xuất ghi DECISIONS: “Minh cho tăng thời gian thực hiện T-054, mức cụ thể cần dự toán; giữ TORAI A ở bảng phụ ngoài A4, cấp quyền nguồn riêng sau.” Chưa có quyền ghi dòng sổ cụ thể nên chưa nối DECISIONS/WHY.


## Phiên 3 — 05/11/2026 — Codex — Windows — người làm

Mở phiên theo prompt Minh dán lại, nguồn nguyên văn runs/trien-khai-002/quyen-minh.txt; nội dung trùng quyền triển khai có điều kiện đã có, không mở thêm quyền dữ liệu/pilot/SSH. Giữ Codex làm, Claude phản biện. Tiếp nhận kết quả phiên2 và trả lời Minh trong manifest-quyet-dinh-001: giữ TORAI A bảng phụ, grant nguồn sau; cho tăng thời gian nhưng chưa chốt số hoặc quy tắc chấm cạn trần. Không tự ghi nhận đây là soát mù mới: đã biết lịch sử phiên trước.

Trước đối chiếu lại SPEC/kết luận cũ đã ghi nhận xét riêng trong chat từ nguồn và code hiện tại: mục tiêu P7 vẫn cần bằng chứng mới, dev trái chiều và fixture không thay pilot; thiếu thực thi trần tổng, drain TORAI và phục hồi journal dở có thể chặn phát lô thật. Các chỗ này thuộc công cụ theo SPEC bước5/7 và phần điều phối, không thay thiết kế. Tiếp tục phần được phép thay vì dừng toàn task vì OPEN pha sau.

Kiểm trước tái dùng: 1364 mục checkpoint trước (trừ pin LOG lịch sử) khớp; LOG mới khớp manifest-quyet-dinh-001. Không khôi phục LOG/STATE cũ. before.json ghi file set/hash trước phiên, giữ mọi đầu ra cũ. Phạm vi công bố thay đổi đã nêu trong chat: chín script T054 nếu cần, LOG, dòng T054 STATE và các đầu ra trong results/T054; không sửa src/AGENTS/MRP/SPEC hoặc quyết thay Minh.

### Checkpoint khi ngữ cảnh nén — 05/11/2026

Theo AGENTS §5a.2, lưu ngay trạng thái tiếp nhận. Chưa hoàn tất T-054 và chưa nghiệm thu pha công cụ. Không mở test/RE3, nguồn TORAI A thật, SSH, pilot thật; không commit/push. Codex vẫn là người làm, Claude phản biện. Nguồn quyền mới nằm ở `results/T-054/runs/trien-khai-002/quyen-minh.txt`.

Đã triển khai trong chín script được SPEC cho phép: phục hồi journal bị cắt ở đuôi và khóa ghi đồng thời; tính trần thời gian toàn lô/theo nhóm qua resume; DRAIN trước pipeline TORAI; bám PID worker thật thay PID launcher Python trên Windows; phụ thuộc main→C-d3 bất biến với kiểm liên kết; nhánh prep/run TORAI A qua metadata nguồn có pin và grant riêng; kiểm đủ cohort/seed A4 trước khi đọc nhãn. A vẫn bảng phụ, không đưa vào A4. Trần chạy thử tự sinh được kiểm; chưa chốt quy tắc chấm cạn trần cho lô thật. Có đề xuất pilot bằng metadata, chưa cấp quyền chạy.

Bằng chứng mới trong `results/T-054/runs/trien-khai-002/`: `queue-fixtures-004/` đạt 25 kiểm; `regression-transport-002/` đạt 60 kiểm; `torai-a-fixtures-001/` chạy đủ ba seed bằng TORAI Python 3.8 trên dữ liệu tự sinh, prep khớp byte giữa seed; `a4-guard-fixtures-001/` bác tám đầu vào sai mà chưa đọc nhãn; `regression-report-001/` tạo 89 dòng báo cáo tự sinh. Các lượt lỗi trước (`queue-fixtures-003`, `regression-transport-001`, tái hiện journal) được giữ. Các số này cần kiểm lại từ file tóm tắt khi chốt báo cáo, không phải kết quả khoa học của P7.

Đang thiếu: phân loại ERROR/TIMEOUT đủ căn cứ để đưa vào chấm (hiện còn BLOCKED); biên dịch plan thật từ nguồn dev gốc độc lập và kiểm điều kiện C-e; đo/tối ưu đồng thời (scheduler hiện nối tiếp); đồng bộ ma trận/hồ sơ hiện hành với quyết định A bảng phụ; đóng gói freeze/manifest mới. `source-manifest.json` và freeze-003 còn là pin code trước sửa; không dùng để nhận rằng code hiện tại đã khóa. Toàn bộ 93 pin code nền đã được kiểm lại khớp trước khi dùng; không sửa src. Không chạy lại `runs/trien-khai-001/kiem_cuoi.py` để ép code/LOG hiện tại khớp mốc lịch sử.

Bước còn lại ngay trong lượt này chỉ là hoàn thiện điểm bàn giao: kiểm file tóm tắt nêu trên, ghi báo cáo tu-soat-002, kiểm phạm vi thay đổi/prefix LOG, cập nhật đúng dòng T-054 STATE, lập manifest checkpoint mới và prompt trung tính. Sau đó đề nghị Minh mở phiên mới theo §5a.2. Bước tiếp của phiên mới: đọc SPEC, checkpoint này, báo cáo mới và các code liên quan; kiểm pin mới; đọc `results/T-052/giao-thuc-p7-a-003.json#/C_e` và nguồn chi phối trước khi tiếp tục phần còn thiếu. Lệnh cuối trước nén là đọc mục C_e bằng Python; đầu ra quá dài cho ngữ cảnh, chưa dùng nó để kết luận.


### Kết thúc phiên 3 — checkpoint 002, chưa hoàn tất pha 1

1. Đã làm: tiếp tục tự soát nguồn và code, sửa lỗi journal/trần thời gian/DRAIN/PID Windows; nối phụ thuộc main→C-d3 bất biến; prep/run A trên dữ liệu tự sinh; gate đủ cohort/seed trước nhãn; lập đề xuất pilot. Báo cáo chi tiết: `results/T-054/reports/tu-soat-002/bao-cao.md`. Giữ đúng giới hạn nhận xét nguồn từ báo cáo 001; không nhận là review chính thức hoặc soát mù mới.
2. File đổi: chín script T-054, LOG chỉ nối, đúng dòng T-054 STATE; thêm đầu ra dưới results/T-054/runs/trien-khai-002, reports/tu-soat-002, freeze-cong-cu-004 và manifest-trien-khai-002. Không sửa SPEC/src/sổ hoặc file lịch sử; các thay đổi có sẵn ngoài T-054 được giữ. Danh mục đầy đủ và pin nằm trong manifest mới. Freeze004 là 107 file đúng byte; protocol/matrix bên trong là ứng viên lịch sử, không là cấu hình đã khóa.
3. Kiểm: queue-fixtures-004 25 PASS; regression-transport-002 60 PASS; TORAI A thật bằng Python 3.8 trên dữ liệu tự sinh đủ seed 0/1/2, prep khớp byte; a4-guard tám phản ví dụ không đọc nhãn; regression-report 28 slot/89 dòng/bốn vùng/hai vị trí N PASS. Không cộng các lượt lặp thành tổng độc lập. Giữ các lượt lỗi, gồm queue-fixtures-003 và regression-transport-001. Kiểm đóng gói/phạm vi sẽ lưu tại runs/trien-khai-002/validation.json; sau đó pin toàn bộ đầu ra vào manifest, kiểm lại chỉ đọc bằng lệnh cuối bên dưới.
4. Chưa chắc/cần Minh: chưa có pilot thật, ETA hoặc bằng chứng parity mới, chưa khóa G3/test. Thiếu plan thực từ nguồn gốc độc lập, binding nguồn/nhãn, grant materialize/pilot/SSH/sync, nguồn A, môi trường, chính sách lỗi/timeout/cạn trần/độ nhạy; chưa có scheduler nhiều worker và số đo đủ. Giữ A bảng phụ đã USER_CONFIRMED; grant nguồn sau. Cho tăng thời gian đã USER_CONFIRMED nhưng chưa có số. Đề xuất pilot 3 giờ trôi/tối đa 9 giờ-máy trong pilot-proposal.json là CANDIDATE CHƯA KIỂM, không phải quyền/ETA. Chưa xin phát lô khi nguồn/môi trường chưa hoàn chỉnh. Chưa nghiệm thu task hoặc trả lời hiệu quả độc lập RQ3b/d và các câu hỏi nguồn còn mở.

Minh nhắn tiếp trong lượt: “KHI NÀO XONG BƯỚC PILOT VÀ ƯỚC LƯỢNG ,CHUẨN BỊ SANG CHẠY CHÍNH THÌ BÁO TÔI NHÉ, SẮP HẾT USAGE”; sau đó “VẬY SAU BƯỚC NÀY BÁO CÁO LẠI TÔI LUÔN”. Ghi yêu cầu báo sau bước hiện tại và báo mốc xong pilot/dự toán trước chạy chính; không nhận các câu này là đã khóa G3, duyệt trần bằng số hay mở nguồn/test/SSH. Không lập automation hoặc tự mở chat.

Ngữ cảnh đã nén: đã ghi checkpoint ngay theo AGENTS §5a.2 và đề nghị mở phiên mới. Phiên tiếp nhận đọc manifest mới, kiểm pin source-current thay own_scripts cũ; không chạy generator lap_ho_so.build_documents vì vẫn mang giả định A OPEN. Root protocol/matrix/source-manifest/pilot-plan/ho-so-g3 từ checkpoint001 chưa đồng bộ; phải cập nhật generator/hồ sơ từ nguồn quyết định trước dùng. Giữ mọi lịch sử.

Bước tiếp chính xác:
- Đọc AGENTS, dòng T-054 STATE, SPEC, mục cuối LOG và reports/tu-soat-002/bao-cao.md. Kiểm manifest-trien-khai-002 cùng validation.json và source-current.json.
- Đọc results/T-052/giao-thuc-p7-a-003.json mục C_e, nguồn P3/G1 và metadata dev gốc trước khi nối plan thật; không đọc raw test/A. Bản đồ độc lập phải có nguồn gốc, không hai bản tự sinh cùng dữ kiện.
- Hoàn thiện phần công cụ còn thiếu: finalization lỗi đủ chứng cứ, plan/source binding, C-e support, generator/hồ sơ hiện hành, scheduler và phép đo được SPEC yêu cầu. Không tự chọn chính sách khoa học.
- Khi có plan cụ thể, trình đúng gói pilot/nguồn/máy/thời gian và grant còn thiếu theo SPEC §7; sau pilot báo Minh số đo/dự toán và điều kiện còn thiếu trước chạy chính. Không dùng cap đề nghị làm ETA.

Đề xuất sổ chính thức chưa ghi: docs/DECISIONS.md nối “Minh cho tăng thời gian thực hiện T-054, mức cụ thể cần dự toán; giữ TORAI A ở bảng phụ ngoài A4, cấp quyền nguồn riêng sau.” Cần Minh duyệt đúng dòng/phạm vi trước ghi. Chưa có quyết định mới về cơ chế phương pháp.

Lệnh cuối dự kiến và được chạy để chốt checkpoint: `& 'D:/RCA-ext/envs/T-014-main/Scripts/python.exe' -X utf8 -B 'results/T-054/runs/trien-khai-002/kiem_checkpoint.py' --manifest 'results/T-054/manifest-trien-khai-002.json'`. Bản thân lệnh này chỉ đọc. Không chạy lại validator checkpoint001 vì pin của nó đã thành lịch sử.

Prompt trung tính để Minh chọn chuyển sang Claude (chưa tự gửi, chưa đề nghị nghiệm thu; chưa có quyền ghi REVIEW mới):

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-054; tasks/T-054-khoa-g3-chay-p7-a/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P6/G3(a), chuẩn bị P7(a).
- Người làm và người phản biện chính thức: Codex làm; Claude phản biện.
- Tài liệu gốc: tasks/T-054-khoa-g3-chay-p7-a/SPEC.md; các nguồn trực tiếp được dẫn trong SPEC.
- Phản biện và phản hồi trước: results/T-054/runs/soan-spec-001/nguon-phan-bien-001.txt, nguon-phan-bien-002.txt, phan-hoi-002.md.
- Code và kết quả liên quan: results/T-054/scripts/; manifest-trien-khai-002.json; runs/trien-khai-002/source-current.json; runbook.md; các nguồn/code được dẫn trong các manifest.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; chưa cấp file phản biện mới.

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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```


## Phiên 4 — 05/11/2026 — Codex — Windows — người làm

Minh giao tiếp tục triển khai phần tiếp theo, đọc kỹ yêu cầu trước, sửa câu chữ sai, ghi checkpoint cẩn thận và dừng báo trước chạy chính. Nguồn nguyên văn: results/T-054/runs/trien-khai-003/quyen-minh.txt. Tiếp nhận checkpoint002: toàn bộ 2179 pin đầu ra khớp trước sửa, không làm lại kết quả đã hợp lệ. Codex làm, Claude phản biện; không tự mở review.

Phân loại EXECUTE. Phạm vi: outputs/công cụ T054, LOG nối, dòng STATE và sửa câu chữ SPEC theo quyền Minh; không thay thiết kế hoặc tự khóa G3. Hiểu lệnh tiếp tục tới trước chạy chính là quyền chuẩn bị và pilot dev local cần thiết trong SPEC, mỗi lô tối đa một giờ theo cap đã đề nghị trong SPEC; không phải quyền test/RE3, SSH/sync, commit/push hoặc tăng cap bằng số. TORAI A thật giữ grant riêng sau như Minh đã nói. Nguồn/dev private bindings cần cho pilot nằm đúng vùng private SPEC, không gói git/cloud. Phần chưa có quyền hoặc lựa chọn nghiên cứu OPEN giữ dừng đúng nhánh.

Ưu tiên: đồng bộ B chính/A phụ (không mở lại lựa chọn baseline), ghi rõ cap không phải ETA; hợp đồng RE3 metadata/schema; nối plan từ nguồn dev gốc và pilot đủ quyền có parity/thời gian thực. Chưa coi xong pha1. before.json lưu file set/hash; lịch sử cũ không sửa.


### Quyết định Minh trong phiên 4 — nguồn A dev

Minh cấp quyền đúng ba CSV tác giả logts/tracets_err/tracets_lat của duy nhất ca dev-a5cabe5fa7 cho pilot ba seed so baseline cũ, trả lời nguyên văn “Cấp quyền đúng ca dev này”. Nguồn câu hỏi/trả lời lưu runs/trien-khai-003/grant-A-dev.json. Không mở các ca A khác/test/RE3; chưa đổi G3 hoặc quyền chạy chính. Giữ B chính/A phụ.


### Checkpoint đang chạy — phiên 4

Đã sửa câu chữ SPEC và hồ sơ runbook/ho-so-g3: B chính/A phụ, cap không phải ETA, nghĩa vụ hợp đồng RE3 pha1. Nguồn dev mới không dùng hai bản tự sinh làm bằng chứng độc lập: descriptor đọc lại allowlist/G1/command lịch sử, kiểm runtime trước API. Tám phản ví dụ nguồn đạt ở source-original-checks.json; upstream ngoài repo đúng ba revision/tracked clean ở external-code-checks.json. Hợp đồng RE3 metadata/schema/code đã có: 30ca/10ô/138129790byte; chưa có schema RE3-OB local, chưa tải/mở telemetry.

Pilot local001 dừng trước worker vì authorize đọc nguồn quyền TXT như JSON; đã sửa xác minh byte/hash không ép parse. Pilot002 đã chạy thật và đạt sáu vế TT; phát DRAIN để sửa kiểm kê py38 (append/prepend đường thư viện khác nhau), không sửa code phương pháp. Giữ môi trường trước/sau; source/record các vế đạt không đổi. Pilot003/004 là lỗi chuẩn bị nhận tiếp (utc trùng, rồi create-only từ chối file nguồn A đã có), chưa phát worker, giữ failure/partial. Đã kiểm lại và nhận tiếp thành pilot005: cùng kết quả VERIFIED cũ, cùng mốc/cost ngân sách, sửa đúng ba slot TORAI B chưa chạy về môi trường py38 thật; thêm ba slot A trên đúng ca Minh cấp. Không chạy lại sáu vế đạt. Toàn plan32slot gồm hai slot unsupported OB không gọi solver. Mọi job/pin/authority và source A riêng trong metadata/continuation của005.

checkpoint-running-001.json là trạng thái sống, chưa nghiệm thu. Chưa sửa production code đã pin trong lúc worker chạy. Các script hoan_thien_code_sau_pilot.py, cap_nhat_ho_so.py và cham_pilot_thuc.py chuẩn bị bước sau; chưa chạy. Dừng trước chạy chính; chưa G3/test/RE3/SSH/commit.


### Quyết định Minh trong phiên 4 — chẩn đoán số luồng

Minh trả lời “Cho chạy chẩn đoán đúng ca này” cho một lượt MicroRank dev-607751ac0a để kiểm giả thuyết sai khác số cuối do cấu hình luồng, giữ cả kết quả, chưa đổi cấu hình chính/dung sai. Nguồn: grant-diagnostic-thread.json. Đính chính ngay trong chat: hồ sơ WHY ghi current16 lúc kiểm kê, source thread lịch sử còn OPEN; câu hỏi đã diễn đạt quá mạnh “nguồn cũ16”, không dùng câu ấy làm sự thật. Quyền thao tác một lượt vẫn đúng phạm vi đã hỏi; không suy kết quả từ tiền đề chưa xác minh.


### Checkpoint sau gói pilot đầu — phiên 4

Pilot005 đủ32slot; C-d3 lỗi wrapper vì cạnh ở extra.canh, không trong dau_vao_cd3. Đối chiếu helper T052 xác nhận cách nối, giữ main seal; sửa wrapper và chỉ lặp C-d3 ở006. Hai ERROR TT MicroRank/TraceRCA được audit code và tín hiệu: operation mới có0span N/210span A tại đúng nguồn/cửa sổ; bản baseline cũ cùngERROR. Thêm receipt chỉ DEV để giữ ERROR và chấmtrượt đúng tái hiện; không mở policy test/TIMEOUT. 006 đạt32VERIFIED (không đồng nghĩa32OK), seal→nhãnG1độc lập→A4/bảng dev ở reports/pilot-local-001.

Parity tiếp phát hiện CIRCA thiếu window.circa_current mặc dùdiagnostics/rank đúng. Sửa worker lấy mốc thực từdiagnostics nhưworkerP3;007chỉ lặp đúngCIRCA, giữ006/reportđầu, ghi DEV_labels_already_viewed. Reports/pilot-local-002 và007summary/parity-complete là đầu ra mới; nguồn/code/kết quả cũgiữnguyên. Chín script nguồn đã chụp trước sửa tại code-pilot-002. Transport60PASS; new-guard-checks16PASS (giảreceiptERROR/TIMEOUTrehash, testgate, G1nhãnpoison vàCIRCAcurrent).

MicroRankOB607 ở1luồng lệch1ULP tại mộtkey, khôngđổi hạng. Minh cấp riêngchẩn đoán mộtca; diagnostic-thread-001/summary.json ghi11.469s: normalized inputkhớp1luồng; thư việnthực16luồng; scientificfieldskhớpbảnT026cũ,từ1luồngkhác1ULP. Không suy source threadlịchsử16 (vẫnOPEN), khôngtựchọnmaind16hoặcdung sai. Cấu hìnhchínhvẫn1theoSPECchờMinhquyếtngoại lệ.

Đang chạy pilot008 gồmM1/T12, B3seedTT/M4OB trênca dev03d4910932 và2bfc97b01e,8slot; khônglặp lại toànmatrix. Dùngcùngmốcbudgetbắtđầutừ002vàcostnhómđãtiêu, khôngresetcap1giờ; sourcegốc/privatebindingsriêngtheoquyềnDEVlocal. Chưachạyrootcap_nhat_ho_so.pyvì008cònchạy; phảiđợiđónglô. Bướcđóngsauđó: cham_pilot_thuc.py pilot-local-008 pilot-local-003; doi_chieu_day_du.py pilot-local-008; cậpnhậthồsơ,tổnghợpthờigian/cácgiớihạn,kiểmbảotoànvàmanifest003,freeze005,promptchuẩn. Khôngmởtest/RE3/SSH/commit;dừngbáotrướcchạychính.


### Kết thúc phiên 4 — checkpoint 003, chưa đủ G3/chưa chạy chính

**1. Đã làm.** Đọc lại yêu cầu và tiếp nhận checkpoint002 (2.179 pin khớp). Sửa câu chữ hiện hành trong SPEC/hồ sơ: B chính/A phụ đã có, cap không phải ETA, RE3 phải chuẩn bị hợp đồng trong pha1; không chọn lại baseline. Hoàn thiện source/label reader từ nguồn G1/allowlist/command gốc, rồi chạy hai gói dev local thật. Bốn ca: TT a5cabe5fa7/03d4910932, OB 607751ac0a/2bfc97b01e. Gói cuối007 có32slot và008 có8slot; seal trước ghép nhãn dev, báo cáo lần lượt reports/pilot-local-002 và003. Giữ report đầu ở pilot-local-001.

Nguồn quyền nằm trong quyen-minh.txt, grant-A-dev.json và grant-diagnostic-thread.json tại runs/trien-khai-003. A chỉ đúng một ca dev được cấp ba CSV/ba seed; không phải quyền toàn cohort. Chẩn đoán luồng chỉ đúng một ca OB; không phải thay cấu hình main. Đã đính chính tiền đề “nguồn lịch sử16”: current16 không chứng minh source thread lịch sử, phần ấy vẫn OPEN.

**2. File thay đổi.** Bảy script T054: bien_nhan, nguon, worker, dieu_phoi, cham, pilot, lap_ho_so; p7/fixtures giữ byte. SPEC sửa mô tả quyền/trạng thái theo nguồn Minh, không thay thiết kế. Chín hồ sơ hiện hành trong results/T054 được đồng bộ; LOG chỉ nối, STATE chỉ dòng T054. Thêm runs/trien-khai-003, reports/tu-soat-003, ba báo cáo pilot dev, freeze-cong-cu-005 và manifest003. File set chính xác ở manifest; trước phiên ở before.json. Không sửa src/AGENTS/MRP/DECISIONS/WHY hoặc đầu ra task cũ. Các thay đổi có sẵn của Minh được giữ.

Sửa lỗi công cụ có bằng chứng: authorize ép nguồn quyền TXT thành JSON; probe môi trường py38 có thứ tự đường thư viện sai; C-d3 thiếu cạnh từ extra.canh; CIRCA thiếu window.circa_current; snapshot ERROR thiếu kiểm phân loại. Chỉ lặp C-d3/CIRCA do lỗi wrapper, giữ main và kết quả đầu; không retry phương pháp để tìm điểm tốt. Sửa CIRCA sau xem bảng dev được khai riêng, chưa dùng test.

**3. Kiểm và số đo.** Transport60PASS, tám kiểm nguồn gốcPASS, 16 kiểm guard mớiPASS, code nền93pin và ba upstream revision/tracked-clean khớp. Hai gói đủ40VERIFIED, không đồng nghĩa40OK: giữ hai ERROR TT, hai UNSUPPORTED OB và C-d3 UNSUPPORTED_CYCLIC trong gói đầu. Hai ERROR có audit operation0spanN/210spanA, đúng code và ERROR baseline cũ; receipt chỉ DEV, không được áp test/TIMEOUT. TORAI A/B đủ ba seed trên ca đầu, B thêm ca TT thứ hai; prep byte và normalized digest khớp giữa seed trên laptop. C-c/C-g khớp T050 ở bốn phép đối chiếu hai ca. Chín script hợp lệ cú pháp; export metadata không ghi đè hồ sơ/quyền.

Thời gian trong thoi-gian-va-kich-ban.json: 42attempt cócost gồm lượt sửa, tổng2383,192giây, chẩn đoán riêng11,469giây. Hai gói từmốcđầutớisupervisorcuốidừng3369,694giây (~56,16phút, gồm ngắt kiểm/sửa); tổng việc máy khoảng40phút. Giữ cùng start/cost cap qua chuyển plan, không reset hoặc đổi chưa chạy thành trượt. M1TT hai ca khoảng118/212giây; M1OB49/51giây. Ngoại suy lạnh một worker cho ma trận chính+A phụ khoảng24,71giờ, giả sử C-e60 cùng chi phí mainTT thêm1,97giờ; đây là CANDIDATE CHƯA KIỂM, không ETA/cap/cận trên, chưa dự đoán C-d3 hỗ trợ hoặc hiệu quả cache/song song. Không phát main từ các số ấy.

Parity cuối: gói007 chỉ MicroRank OB1luồng lệch1ULP; cùng normalized input, diagnostic thư viện thực16luồng khớp nguồn, hạng không đổi. Gói008 M1/T12 OB so nguồnEC2 còn lệch tối đa2ULP/1ULP; các trường rời rạc/thứ tự/vùng đã so không đổi, nguyên nhân riêng cònOPEN. Không thêm dung sai, không sửa số để khớp. Các giá trị/diff nằm trong parity-complete/parity/numeric-parity-analysis. Biên nhận kiểm toàn checkpoint tại validation.json chỉ xác nhận toàn vẹn/quyền/phạm vi, không thay G3 hoặc bằng chứng khoa học.

**4. Phần chưa xong.** Pha1 chưa hoàn tất. Còn bundle/cache dữ liệu và E4 giữa vế, cache prep thực sự dùng lại, scheduler/throughput1→2/3, C-e và các cặp giúp/hại/không đổi chưa phủ đủ; finalization ERROR/TIMEOUT main, monitor/clock/sleep, quy tắc cạn trần, độ nhạy, nguồn test/A cả cohort và revision trước G3. Mọi mục giữ nghĩa vụ nguồn/SPEC; không bỏ vì chưa làm. RE3 H0 hợp đồng có rồi (30ca/10ô/138129790byte theo metadata đã pin), chưa có schema local, chưa H1/H2 adapter, chưa H3/H4; không tải/mở telemetry hay sửa src. Cần trình đúng quyền/file/schema trước phần phụ thuộc. Chưa có kết quả test trả lời RQ3b/d; detector, vùng thật, cơ chế vật lý và P8–P10 vẫn theo MRP.

Điểm tiếp nhận chi tiết: runs/trien-khai-003/buoc-tiep-theo.md; báo cáo chính reports/tu-soat-003/bao-cao.md. Đọc hai file này trước bắt đầu việc mới. Code đúng byte mỗi gói tại code-version-lineage.json và code-pilot-*; phiên bản006 được dựng lại từ bản007 bằng đảo đúng patch CIRCA rồi đối hash job. Lần dựng đầu sai LF/CRLF được giữ trong code-pilot-006/reconstruction-failure.json; bản đúng ở code-pilot-006-r2. Freeze005 là code hiện tại, không phải byte đã tạo mọi kết quả cũ hoặc khóa G3. Data/private refs không nằm trong gói code. Nếu máy khác thiếu ref private, dựng lại từ recipe/nguồn gốc đúng quyền và lưu lineage, không đọc repo RCA lưu trữ/test.

Không chạy lại chot_va_sua_cd3/hoan_thien_code_sau_pilot/nhan_tiep_env: các bước đó đã áp dụng, có đích create-only và lịch sử. Đầu ra đã hợp lệ không làm lại. Bước tiếp là triển khai phần công cụ/cache/điều phối còn thiếu trong đúng SPEC và so với các bản lạnh đã có; chốt lựa chọn khoa học với Minh trước phần phụ thuộc, không xin lại quyền công cụ/dev đã cấp. Phân biệt phần chưa làm với dữ kiện cần Minh cấp. Dừng báo trước main theo lệnh Minh; hiện chưa xin G3/chạy chính khi bằng chứng còn thiếu.

Các quyết định cần sổ chính thức đã trình trong de-xuat-so-quyet-dinh.md và ghi nguồn nguyên văn trong LOG/grant; chưa nối sổ khi chưa duyệt đúng dòng. Chưa commit/push. Đề xuất nội dung commit checkpoint nếu Minh duyệt đúng file: “T-054: pilot dev local, sửa binding/C-d3/CIRCA và cập nhật hồ sơ”; cần chọn file trước, không tự thêm dữ liệu/private vào git.

Lệnh cuối được dùng chốt checkpoint (chỉ đọc, kết quả sau khi lập manifest):
`& 'D:/RCA-ext/envs/T-014-main/Scripts/python.exe' -X utf8 -B 'results/T-054/runs/trien-khai-003/kiem_checkpoint.py' --manifest 'results/T-054/manifest-trien-khai-003.json'`

Prompt trung tính để Minh chọn chuyển sang Claude; chưa tự gửi, chưa mở REVIEW hoặc đề nghị nghiệm thu:

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-054; tasks/T-054-khoa-g3-chay-p7-a/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P6/G3(a), P7(a).
- Người làm và người phản biện chính thức: Codex làm; Claude phản biện.
- Tài liệu gốc: tasks/T-054-khoa-g3-chay-p7-a/SPEC.md; các nguồn trực tiếp được dẫn trong SPEC.
- Phản biện và phản hồi trước: results/T-054/runs/soan-spec-001/nguon-phan-bien-001.txt, nguon-phan-bien-002.txt, phan-hoi-002.md.
- Code và kết quả liên quan: results/T-054/scripts/; manifest-trien-khai-003.json; runs/trien-khai-003/; source-manifest.json; runbook.md; các source/revision được dẫn trong manifest.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; chưa cấp file phản biện mới.

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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```


## Phiên 5 — 05/11/2026 — Codex — Windows — người làm

Tiếp nhận checkpoint003, giữ vai trò người làm; Claude phản biện. Minh duyệt gói thu gọn ở runs/trien-khai-004/quyen-minh.txt. Đã đọc AGENTS/STATE/SPEC/LOG; validator003 --manifest PASS toàn bộ 3.558 pin, 40 slot dev giữ nguyên, không có worker sống. Chưa chạy phương pháp mới, chưa sửa code. Bản trước thay đổi tại before.json/before-files.

Checkpoint khi ngữ cảnh được nén: các đầu ra hiện hành hợp lệ, không lặp baseline. Thứ tự tiếp: hoàn thiện scheduler đúng 1/2 worker; kiểm resume/DRAIN/budget/phân loại; chỉ chạy lô dev ngắn giải quyết concurrency/C-e hoặc sai khác cụ thể; cập nhật hồ sơ để Minh xét G3. Kế hoạch cũ đo 3/4 và cache diện rộng được thay bởi chỉ đạo mới, không tự buộc làm thêm. Những OPEN số học/chính sách/nguồn vẫn OPEN tới khi có bằng chứng và quyết định tương ứng. Không test/RE3/SSH/commit. AGENTS §5a.2 yêu cầu đề nghị phiên mới khi nén; checkpoint này cho phép chuyển phiên nếu Minh cần, công việc tiếp tục trong phạm vi vừa duyệt.
Lệnh kiểm cuối: Python main -X utf8 -B results/T-054/runs/trien-khai-003/kiem_checkpoint.py --manifest results/T-054/manifest-trien-khai-003.json.

### Quyết định Minh phiên 5

Nguồn USER_CONFIRMED: runs/trien-khai-004/quyet-dinh-minh.json. Minh chấp nhận đúng ba sai khác số học đã lưu, giữ 1 luồng, không dung sai chung/không làm tròn. Minh duyệt cả hai công thức độ nhạy trong SPEC. Về thời gian: “trừ khi chạy hàng chục tiếng chưa xong hoặc chạy lỗi. vòng lặp vô tận thì dừng, không thì cứ cho chạy, không tạo trần cố định”. Áp riêng P7: bỏ trần cộng dồn toàn đợt/method×dataset; giữ timeout từng lượt để xử lý treo, theo dõi không tiến triển, lỗi hoặc hàng chục giờ chưa xong phải dừng/báo. Lượt chưa chạy không thành method TIMEOUT, bảng cần đủ cohort vẫn chặn. Đây chưa là G3/test/main. Sổ DECISIONS/WHY sẽ trình đúng dòng để Minh duyệt ghi, không tự ghi.


### Kết thúc phiên5 — checkpoint004, dừng trước G3/main

**Đã làm:** hoàn tất gói thu gọn được Minh duyệt. Giữ G2 và40slot/bốnca cũ; chỉ thêm2slot M1 (TT C-e a5cabe5fa7 và OB607751ac0a) giải tuyến C-e và đo2worker. Lô thật250,171s, overlap55,229s; cảhaiOK/paritytoàntrườngkhớp, OBnormalizedinputkhớp1worker. ĐỉnhRSSđồngthờilấymẫu1.426.219.008byte. Khôngthử3/4, khôngcacheliênvế, khôngđobiênrộng.

**Thay đổi:** bảy script task (bien_nhan,nguon,worker,dieu_phoi,cham,p7,pilot); hai script fixtures/lap_ho_so giữ byte. SPEC cập nhật đúng gói/ba quyết định Minh; LOG chỉ nối, STATE chỉ dòng T054. Đồng bộ bảy hồ sơ root (protocol,source-manifest,authorization,pilot-plan,reuse,environment,ho-so-g3) và runbook; matrix giữ byte. Thêm runs/trien-khai-004, reports/tu-soat-004, freeze006 và manifest004. Tập chính xác/byte trước ở before.json; tập sau trong manifest. Không sửa src/AGENTS/MRP/DECISIONS/WHY/task cũ. Sổ chính thức đề nghị ở de-xuat-ghi-so.md, chưa tự ghi.

**Kiểm:** 60 transport sau driver;9 operational checks có controller restart haiworker thực, DRAIN, method/source timeout, hai ERROR cũ audit không rerun;4 nhánh cuối có same-group serial/WAIT_ERROR/pipeline method timeout; độnhạy seedlỗi/cặprỗng/giữ UNSUPPORTED/NO_EVIDENCE và primary/alpha khôngđổi;6 C-e support metadata; nhánh báoTIMEOUTgiữ N1/O/V0=N/A, C-c độc lập vàC-g thiếugraph khai riêng. Finalvalidation/manifest là phép kiểm chỉ đọc sau đóng hồ sơ, không là nghiệm thu khoa học. Giữ mọi lượt lỗi: helper chấm celllist chưa canonicalize và fixture timestamp trướcdeadline. Sửa đúng lỗi, giữ script/lượt đầu, không lặp method thật. Code thực lô2worker được chụp trong pilot-2-worker-001/code; bản cuối thêm metadata quan sát/sửa timeout/mô tả, không tự nhận code cuối tạo mọi lượt cũ.

**Điểm dừng/còn mở:** sẵn sàng trình xét G3 theo phạm vi gói, không phải đãđạtG3 hoặc đủ quyền phátmain. Còn phảnbiện/duyệt khóa đúng byte/params, ghi sổ chính thức/commit khiMinhduyệt, nguồn/test94 và map nhãn độc lập saugrant, A3CSV đúngcohort. RE3 có hợpđồngmetadata, H1schema/H2adapter/src/quyềnriêng chưa làm; không thuộcgrant94, không bỏ nghĩa vụ. Chưa có ETAtoànmatrix, lônhỏkhông chứng minh speedup hoặczeroOSpaging. Đãbổsung monitor RAM/pagefile, sốhosthiệnở preflight-final; cần theo dõi sức ép RAM/đĩa khi chạyđúnggrant. Khôngtạo trần cộngdồn; lỗi/khôngtiếntriển/hàngchụcgiờchưaxongthìdừng/báo theoMinh. RQ3/test/nhânquả/vùngđúng/P/R/F1pháthiệnchưacóbằngchứngmới.

**Bước tiếp:** KHÔNG chạy thêm pilot mặc định; báo Minh xem reports/tu-soat-004/bao-cao.md, de-xuat-khoa-g3.json, de-xuat-ghi-so.md và chọn chuyển prompt Claude bên dưới. Chờ G3/quyền nguồn trước materialize test/plan; không tự đổi cờ LOCKED/test. Lệnh tiếp nhận: Python main -X utf8 -B results/T-054/runs/trien-khai-004/kiem_checkpoint.py --manifest results/T-054/manifest-trien-khai-004.json. Lệnh kiểm cuối dự kiến và được ghi kết quả trong validation/manifest: chính lệnh này sau dựng gói. Đề nghị nội dung commit (chưa thực hiện): `feat(t054): prepare P7 driver and G3 review package`; trước commit phải trình đúng filelist, không gom thay đổi có sẵn của Minh.

AGENTS §5a.2: đã có checkpoint đầy đủ khi nén; có thể mở phiên mới từ lệnh tiếp nhận trên, không cần khởi động lại pilot.

### Prompt Minh chuyển Claude — chỉ đọc trong chat

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-054; tasks/T-054-khoa-g3-chay-p7-a/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P7(a), chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện.
- Tài liệu gốc: AGENTS.md; docs/MRP.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; SPEC/LOG T-054.
- Phản biện và phản hồi trước: tasks/T-054-khoa-g3-chay-p7-a/LOG.md; results/T-054/runs/soan-spec-001/.
- Code và kết quả liên quan: results/T-054/manifest-trien-khai-004.json; results/T-054/reports/tu-soat-004/bao-cao.md; results/T-054/scripts/; results/T-054/runs/trien-khai-004/buoc-tiep-theo.md; results/T-054/runbook.md.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ đọc và trả lời trong chat; chưa có quyền ghi bản phản biện mới..

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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```


### Checkpoint cuối phiên 5 — ghi rõ để tiếp nhận

Đã hoàn tất gói thu gọn; chỉ thêm hai lượt M1 dev cần thiết, không lặp baseline diện rộng. Driver kiểm 1/2 worker, nhận lại tiến trình/DRAIN, dừng phát khi lỗi, lỗi phương pháp đã phân loại và timeout đủ bằng chứng; C-e có cả tuyến thật và kiểm thiếu lịch sử. Đã chốt ba quyết định theo lời Minh trong quyet-dinh-minh.json; sổ DECISIONS/WHY chưa sửa, có đề xuất dòng ghi riêng.

Soát cuối bổ sung đối chiếu plan với code/config/env/policy khóa trước I/O dữ liệu, tránh plan tự đổi cấu hình rồi tự băm lại. Chín kiểm metadata giả đạt; không phát test. Đường độ nhạy và bảng TIMEOUT đã kiểm riêng; không đổi E-04/mức OB. Giữ code của lô thật và các lượt hỏng, kèm giải thích lineage.

Lô hai slot có producer receipt đủ VERIFIED trước đọc nhãn dev. Helper ghi tệp tên snapshot-before-labels sau lookup nhãn; đã khai điều này trong label-exposure-note.json và báo cáo, không lấy tên tệp làm chứng cứ mù hoặc thời điểm. Đường chấm chính vẫn kiểm snapshot trước nhãn.

Hiện dừng chờ Minh xét hồ sơ G3 và quyền nguồn; không còn lô pilot mặc định. Chưa G3, chưa main/test, chưa adapter/telemetry RE3, chưa SSH/commit. Đọc báo cáo004, de-xuat-khoa-g3.json và de-xuat-ghi-so.md. Prompt Claude ở ngay mục trước, chỉ chuyển khi Minh chọn. Lệnh kiểm tiếp nhận: Python main -X utf8 -B results/T-054/runs/trien-khai-004/kiem_checkpoint.py --manifest results/T-054/manifest-trien-khai-004.json.


Kết quả kiểm cuối checkpoint004: PASS. Đối chiếu3.566 tệp trước phiên; đúng18 tệp cũ thay đổi trong phạm vi, giữ3.548 tệp còn lại; LOG chỉ nối, STATE chỉ dòng T054. Chín script hợp lệ cú pháp,93 pin code nền khớp,40 slot dev cũ và2 slot mới hợp lệ; gói freeze006 có114 tệp đúng byte. Không còn worker/supervisor T054 sống. G3=false, test_opened=false, main_started=false. Chi tiết: runs/trien-khai-004/validation.json. Ba upstream hiện hành đúng revision và tracked-clean. Hai tệp markdown root cũ không có bản byte dự phòng riêng; đã đọc đầy đủ trước sửa, giữ hash trước và khai trong metadata-diff.json. Các JSON/code/SPEC/LOG/STATE trước phiên đã có byte dự phòng hoặc tìm lại đúng hash.

Đã đọc lại hai tệp yêu cầu Minh đính kèm; nội dung trùng nhau và khớp quyền tiếp nhận người làm, không thay mốc dừng mới. Lệnh cuối để kiểm sau dựng manifest: Python main -X utf8 -B results/T-054/runs/trien-khai-004/kiem_checkpoint.py --manifest results/T-054/manifest-trien-khai-004.json. Dừng báo Minh, không tự qua chạy chính.


## Điều chỉnh sau checkpoint004 — 05/11/2026 — Codex, người làm

Ý định: EXECUTE việc Minh yêu cầu bỏ ràng buộc test local; DISCUSS/PLAN phần bố trí nhiều máy. Tác động đã báo trong chat: SPEC và quyết định nguồn thay điều kiện local-only; LOG lưu thay đổi. Đã nối quyết định USER_CONFIRMED trong DECISIONS và sửa SPEC theo đúng chỉ đạo trực tiếp, không sửa AGENTS hoặc quyền mở test.

Đính chính: checkpoint004 hoàn thành gói công cụ local thu gọn, chưa hoàn thành mục tiêu tối ưu bố trí nhiều máy. Driver đã kiểm hai worker đơn máy, chưa hoàn thiện/test tuyến cloud P7. Các hồ sơ results/T054 và guard authorize/locked-plan còn ghim local; giữ chúng là checkpoint lịch sử, không được phát main nguyên gói. Manifest004 từ đây là lịch sử trước quyết định mới; không khôi phục SPEC/DECISIONS để ép khớp.

Hướng đề nghị, chưa quyết: chia các lô ca/vế độc lập trên hai EC2 và laptop; một supervisor mỗi máy, phân vùng cố định, không queue phân tán. Ưu tiên phần TT nặng trên EC2, laptop nhận/kiểm/chấm và nhận phần tính toán phù hợp. Chưa mặc định OB local hoặc cloud; phải xét file ngày dùng chung và chi phí chuyển/đọc. Không chạy lại baseline dev diện rộng; chỉ kiểm khởi chạy/môi trường/chuyển-kết quả cho tuyến cloud thực sự khác. Chưa SSH/truyền dữ liệu/mở test hoặc chạy chính trong lượt này.

File thay đổi: SPEC, DECISIONS (chỉ nối), LOG (chỉ nối). Kiểm: đối chiếu Q-42/Q-43 và lịch máy SPEC; sửa đúng ràng buộc local theo lời Minh. Bước tiếp theo là trình gói sửa driver/hồ sơ và lịch hai EC2+laptop cụ thể, ETA có giả định rõ, rồi triển khai theo quyền đúng bước. Không còn báo sẵn sàng G3 về vận hành nhiều máy khi phần này chưa làm.


### 05/11/2026 — thêm luật ưu tiên EC2 theo lệnh Minh

Minh yêu cầu ghi thành luật EC2 nhanh hơn laptop. Đã đọc toàn AGENTS và Q-42/Q-243/Q-244. Q-42 có cả ưu tiên lượt dài EC2 và cấm chép dữ liệu khóa; Q-243 yêu cầu ưu tiên EC2/tổng thời gian, tiền máy không là ràng buộc. Đã thêm AGENTS §3.19 và nối DECISIONS theo đúng yêu cầu; giữ lịch sử cũ. Không tự bỏ các luật khác. Rà các điểm hạn chế quyền chủ động: Luật0/phạm vi SPEC, ngưỡng xin quyền thao tác tốn kém, tối ưu cần duyệt, ghi WHY/sổ cần duyệt riêng, khóa SPEC, bàn giao phản biện thủ công, checkpoint khi nén, task một phiên, tải dữ liệu và giới hạn source/môi trường/luồng/máy ở quyết định task. Phân biệt chúng với tính đúng nghiên cứu: không mở test trước quyền, không dùng nhãn vào phương pháp, giữ lượt hỏng, không chọn theo test.

File thay đổi đúng ba: AGENTS.md, DECISIONS.md chỉ nối, LOG chỉ nối. Kiểm đoạn mới và bảo toàn phần cũ; không thực nghiệm/SSH/mở test hoặc commit. Tiếp theo: hoàn thiện phương án nhiều máy theo luật mới; gói local checkpoint004 là lịch sử, chưa sẵn sàng main nhiều máy.


## Phiên 6 — 05/11/2026 — Codex, Windows, người làm

Minh duyệt mục1/3 thay luật, không duyệt mục2 chuyển phản biện tự động. Đã cập nhật AGENTS và nối DECISIONS; không sửa review-prompt. Tiếp tục T054 theo lệnh mới: SSH hai EC2 kiểm inventory/môi trường/wrapper/dữ liệu, reuse trước; lập lịch tất cả tài nguyên theo phụ thuộc; sửa tuyến cloud/kiểm dev ngắn; dừng trước main. Snapshot trước ở runs/trien-khai-005/before.json. Không xóa, mở test hoặc chạy chính; dữ liệu khóa chỉ thống kê/hash. Phạm vi dự kiến: AGENTS/DECISIONS/LOG, SPEC/dòng STATE, các script và hồ sơ T054 trong SPEC; nếu dọn nguồn cũ phải trình đúng danh sách.


### Checkpoint kết thúc phiên6 — 05/11/2026 — dừng trước main, Minh báo sắp hết usage

Ý định EXECUTE đúng gói Minh duyệt. Đã áp AGENTS mục1/3: nới một task/phiên và checkpoint khi nén, thêm nghĩa vụ rà/tận dụng kết quả cũ. Không áp mục2; không gửi phản biện tự động. DECISIONS chỉ nối quyền đã có. Không commit/push; không sửa src hoặc task cũ.

Đã SSH cả hai EC2 bằng hostkey pin, kiểm inventory/env/source/wrapper. Dùng lại T025/main+py38; không dựng lại. Minh duyệt xóa đúng /home/ubuntu/rca/envs/py312 (~8,10GB), đã xóa; giữ T025/main và toàn data/results. EC2_1 free1,462→9,563GB sau dọn, cuối~9,481GB; EC2_2 cuối~14,549GB. Không dọn thư mục khác. Quyết định cleanup và bằng chứng ở approved-cleanup-ec2-1.json; không hiểu lời Minh là xóa toàn T025.

TT60 đã sẵn60ca/180parquet/1.309.388.082byte; kiểm hash+byte đúng từng ca/tên tệp với nguồn HF đã pin; không đọc giá trị, không tải lại. Chưa truyền test. transfer-plan005 có90tệp/~0,655GB/mỗiEC2, giữ bản gốc laptop, không labels/OB/A chuyển cloud. Lịch placement005: mỗiEC2 30TT/360vị trí tối đa (family210,B90,C-d3 30,C-e≤30); laptop922 (OB442 gồm68UNSUPPORTED,TT5baseline300,A180). Tổng1642vị trí không trùng, không thiếu; max1574method nếu C-e đủ, phần thiếu lịch sử là support row có nguồn. Worker tối đa2/máy,1luồng số học; admission RAM có dự phòng. Prep→TORAI và M1seal→C-d3 tuần tự; ba queue độc lập đồng thời. Không dựng cache liên vế hoặc queue phân tán mới.

Giữ G2/40slot003+2slot004 và mọi lượt hỏng.005 chỉ chạy2M1trên cùng1DEV dev-a915aa2424, mỗi máy1lượt để kiểm tuyến. EC2_2 wall66,976648s/RSS cây1.746.251.776byte,maxgap0,24055s; trường khoa học đối chiếu khớp native EC2_2. EC2_1 output cũng khớp native EC2_2 nhưng controller chụp argv trước exec, journal BLOCKED/cost không hợp lệ. Giữ nguyên journal/cost và thu hồi output bằng receipt riêng; không rerun method, không dùng cost này cho ETA. Sửa bắt tay token/argv trước pinPID, stdin tách SSH. Ghi rõ producer byte code DEV khác byte công cụ cuối. TORAI_B dùng lại G2Linux/source hash/import; parsed4CSV+t+seed khớp Windows trên cả hai máy, không chạy lại học TORAI.

Đã kiểm:9công cụ giả laptop+haiEC2;60transport current; metadata compiler giả giữ1642vịtrí (1641job+1support), child/aggregate hợp đồng đạt, thiếu job/lô/C-e và protocol chưa khóa bị chặn. Cuối kiểm120tệp freeze007 đúngbyte,93pin nền nguyên,9scriptAST và đúng byte Linuxr2;4.685đầu ra cũ giữ theo manifest004;100tệp nhận cloud đúng hash. LOG/DEC append-only, STATE chỉ dòngT054. Cuối SSH không còn worker T054 ở haiEC2; laptop không còn worker. validation.json chứa tự kiểm; chưa là phản biện độc lập/G3 hoặc chấp nhận nghiên cứu.

Giữ các lần lỗi chuẩn bị: probe import hiển thị __file__ sai đối tượng, collector BLOCKED/systempython thiếu numpy, summary create-only collision, closeout collision tên contract. Không lặp method để sửa lỗi ghi/thu; giữ partial và tên bản sau riêng. closeout.py là helper đã chạy, không chạy lại; freeze.py cũng create-only. Chỉ dùng validator để kiểm nhận tiếp.

Ước5–9giờ chỉ là kịch bản compute+transfer+seal+score, chưa đo toàncohort, không trần/ETA toàntask; giả định cloud40–120s/lượt chỉ có1mẫu67s,2worker khiRAMđủ, baseline timing cũ,setup/chuyển0,25–0,5h. Đọc ca/cơ chế/báo cáo nghiên cứu tính riêng/chưa đủ căn cứ ETA. Không thêm pilot mặc định chỉ để đo. Không đặt trần cộng dồn; lỗi/không tiến triển/lặp vô tận/hàng chục giờ chưa xong thì báo, unrun khôngTIMEOUT.

Hồ sơ hiện hành: reports/tu-soat-005/bao-cao.md, protocol.json→dispatch-contract-005-freeze-candidate.json, freeze007, transfer-plan005, runbook, SPEC và manifest005. Cập nhật root auth/env/pilot/reuse để không còn ghim local/SSHfalse. Checkpoint004 là lịch sử; không phục hồi nguồn mutable mới về hash cũ. Toàn diff5script/AGENTS đã xem; không thay nội dung khoa học nền/cấu hình/cửa sổ/miền/hạng; root metadata và SPEC vận hành đã đối chiếu.

Đạt: phần chuẩn bị nhiều máy được duyệt đã có bằng chứng trình G3. Chưa đạt: G3 chưa khóa, chưa plan test nguồn thật, chưa mở test94 hoặc chấm, chưa chạy main, chưa RE3telemetry/adapter. Câu hỏi RQ3 chưa được trả lời độc lập. TORAI_A vẫn phụ ngoàiA4; quyền1DEV không phải quyềncohort. RE3 có hợp đồngmetadata trước, H1/schema/H2/adapter thật cònOPEN và phải xử lý theo nguồn/quyền riêng, không nhận tương thích sẵn.

Bước tiếp theo chính xác: DỪNG báo Minh. Đọc báo cáo005 + protocol/contract + transfer-plan; Minh xét G3/nguồn test94/chấm và chuyển TT haiEC2/nguồn Acohort. Sau quyền mới materialize/attest nguồn độc lập/runtime/binding/C-e, API materialize_main.build biên dịch plan bất biến theo bảnLOCKED, kiểm trước phát. Không dùng fixture LOCKED/metadata giả làm grant. Không chạy closeout/finish_plan/testmaterializer cũ vào vùng đã tồn tại. Nhận/merge qua receive_paths trong cùng process như runbook, không sửa receipt/path để ép khớp. A grant chưa đủ thì compiler full plan dừng; không tự bỏ A hoặc tự suy quyền.

File thay đổi: AGENTS, DECISIONS chỉ nối, SPEC, LOG chỉ nối, đúng dòngSTATE;5script (bien_nhan,cham,dieu_phoi,nguon,p7),8hồ sơ rootT054; đầu ra/helper/bundle mới chỉ trong results/T054. Bốn script khác và93nguồn nền giữ nguyên. Nội dung commit đề nghị khi Minh muốn: “Chuẩn bị điều phối P7 hai EC2+laptop, giữ kết quả và dừng trước G3”; chưa commit/push.

Lệnh cuối kiểm nhận tiếp (chỉ đọc, sau niêm phong manifest):
D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B results/T-054/runs/trien-khai-005/kiem_checkpoint.py --manifest results/T-054/manifest-trien-khai-005.json

### Prompt Claude — chỉ để Minh chọn chuyển

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-054; tasks/T-054-khoa-g3-chay-p7-a/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P7(a), trình G3.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện.
- Tài liệu gốc: SPEC và LOG task; docs/MRP.md; tài liệu nguồn nêu dưới; snapshot trước005 ở results/T-054/runs/trien-khai-005/before/.
- Phản biện và phản hồi trước: các bản REVIEW theo thứ tự trong tasks/T-054-khoa-g3-chay-p7-a/ và phần đáp trong LOG.
- Code và kết quả liên quan: results/T-054/; manifest-trien-khai-005.json; reports/tu-soat-005/bao-cao.md; Python D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B; lệnh kiểm checkpoint trong runbook.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; chưa cấp bản phản biện ghi mới.

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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```


## Phiên7 — 05/11/2026 — Codex, Windows, người làm

EXECUTE đúng ba bước Minh giao: nguồn thật/danh sách ba máy, TT transfer hai EC2 song song, kiểm trước chạy/chốt lệnh/checkpoint rồi dừng. Nguồn quyền runs/chuan-bi-main-006/quyen-minh.txt; quyền chuẩn bị94ca và nguồn Acohort theo đề nghị trước, không tự LOCKED_G3/main/chấm/RE3/commit. Phạm vi ghi: results/T054, LOG chỉ nối và đúng dòngSTATE. Giữ nguyên code khoa học/baseline/pilot, checkpoint005; checkpoint riêng sau mỗi phần.

Checkpoint phần2: hai EC2 nhận đủ90tệp TT/máy, tổng180tệp/1.309.388.082byte. Hash trước gửi, trong stream và đọc đĩa đích đều khớp; vùng partial chỉ rename sau đủ. Bản gốc giữ laptop, không labels/method. Nguồn: runs/chuan-bi-main-006/checkpoint-02-transfer.json và hai receipt.

Checkpoint phần1 nguồn: TT60/OB34 đúng G1 và cohort; TT180hashHF, t từinject_time trong zip tác giả khớpGitblobHF. A180CSV giải nén đúng ca từzip đãpin, không tải mới; OB sourcebytes/Gitblob và mốc native xác minh. C-e phân loại từtimestamp/A0, không chạyM1 hoặc suy khỏe. Nguồn private tách khỏi phương pháp; receipt chuẩn bị không giả G3/attest runtime chính. Chi tiết checkpoint-01-sources.json; chưa chạy/chấm.

Checkpoint phần1 danh sách: đủ1.642vị trí =1.640job+2C-e insufficient; ba plan nguồn thật giữ đúng partition/config/env/seed/phụ thuộc. Metadata nhãn evaluator riêng, chưa ghép output/điểm. Plan candidate và authorityg3=false, không giả khóa để vượtguard. Chi tiết checkpoint-01-plans.json; chờkiểm/staging.

Checkpoint phần3: cả3máy PASS preflight code103pin, executable/env chính, nguồn/locator/hash/cửa sổ/config/seed/phụ thuộc/partition/RAMđĩa. Candidate authority bị WAIT_G3 đúngchủđích; chưa queue/supervisor/main. Laptop cắm điện nhưng sleepAC45phút (chưa đổi), cần giữthức khi main. commands-prepared.json chốt lệnh kiểm/currentcandidate; activate_prepared.py chỉ đóng metadata sau grantG3/main riêng, chuẩn bịgrant bịtừchối trước tạoartifact. Nguồn: checkpoint-03-preflight.json.

Bổ sung cuối phần3: audit timestamp A180CSV phát hiện1logts thiếuN (N0/A41), giữnguyênnguồn/seed/t, khôngchạytest đểthử. Đãđọcnhánhcat20/logskip/minnormal RCD; chưa kếtluậnmethodlỗi. Khai giới hạn trướcG3, khôngtựbù/đổi/tạo cổng mới.58/2C-e khôngđổi, so inttimestamp60ca chínhxác khớp sau normalize tuple/list. Lượtassert chuẩn bị/parse sai đượcgiữ/giải thích; khôngcoi làlượtRCA. Nguồn checkpoint-03-addendum.json và A-input-limitation.json.

Checkpoint cuối phần3: nguồn timestampOB kiểm374cặp (34ca×11nguồn),4ca/30cặp vi phạm guard5N5A thực. Hai ca thiếuN, hai ca cónguồndư1hàng sátbiên. Code reader sẽtừchối trướcmethod; preflightPASS trướcchỉhash/schema/env/partition, khôngnhận readinesscuối. Giữ4ca/nguồn/mốc, chưa sửasrc/nới guard/bù/cắt/loạica/gánđiểm. source-bundle-final-prepared cóopen_before_run; activationhelper kiểm chặntrướcLOCKED, khôngphátmain. DừngbáoMinh và trình phânxử/sửabộđọc–giao thức tối thiểu trướcG3. Nguồn checkpoint-03-final.json, OB-source-blocker.json, activation-source-blocked.json.


### Kết thúc phiên7 — checkpoint006 — dừng báo Minh trước main

**Đã làm:** đúng ba bước chuẩn bị Minh giao. Nguồn thật TT60/OB34 và danh sách ba host đã dựng. Đã kiểm cohort/G1/mã mờ, hash/byte HF cho TT và Git blob Nezha cho OB; mốc TT lấy inject_time trong zip tác giả khớp blob HF từng ca. A lấy đúng180CSV của60ca trong torai-data.zip có sẵn, tổng9.244.910byte, không tải mới hoặc ghi đè thư mục dev. Metadata/nhãn evaluator được chuẩn bị tách riêng; chưa ghép output, chưa chấm. C-e temporal/A0 có58verified/2insufficient, giữ2dòng hỗ trợ gắn sourcehash, không suy nền khỏe hoặc điểm0.

Hai EC2 đã nhận TT song song khoảng110giây sau kiểm đầu gửi;90tệp/máy, tổng180tệp/1.309.388.082byte. Kiểm hash trước gửi/trongstream/đọc đĩa đích và rename partial sau đủ. Bản gốc laptop giữ nguyên. Code packet128tệp/máy đặt trong code_root riêng theo contract005, kèm metadataTT/plan candidate, không labels/OBmap/Acloud. Không dọn thêm ngoài quyền cũ, không đổi nguồn điện, không bật/tắt máy.

Bố trí giữ1642vị trí =1640job+2C-e support: EC2_1 358job+2support, EC2_2 360job, laptop922job. MỗiEC2 nhận30TT (family210,B90,C-d3 30,C-e28/30); laptop OB442gồm68UNSUPPORTED,TT5baseline300,A180. Prep→TORAI;M1seal→C-d3 tuần tự, lôđộc lập ba máy song song, tốiđa2worker khiRAMđủ và1luồng/method. Không cacheliênvế/queuephântán/pilot mới. Không coi68unsupported làlượthọc; max1572method được hỗtrợ.

**Kết quả kiểm và điểm chặn thật:** hash/schema/env/code103pin/placement/executable/cửa sổ/phụ thuộc/RAMđĩa đạt cả3máy; candidateauthority bịWAIT_G3 đúngchủđích. Nhưng kiểm riêng Time11nguồn×34OB phát hiện30/374cặp ca–nguồn vi phạm guardlen10/5normal trong src/p3/nezha.py::_doc_cua_so, thuộc4ca. test-3218391218:11nguồn3N/5A; test-3a1afd6d4f:11nguồn2N/5A; test-9712e01207:nămnguồn6N/5A hoặc5N/6A; test-a8cc0373da:banguồn5N/6A. Reader sẽtừchối trướcmethod. Không gán là RCA thấtbại, không tựnới guard/bù/cắt/dịchmốc/loạica/gánERROR/TIMEOUT/0. Toàn34OB vẫn trong danh sách. Chưa xácđịnh cáchsửa đượcduyệt, cần phânxử bộđọc–giao thức trướcG3. Không lấy PASS vềmáy/hash thay readinesscuối.

A phụ: timestamp180CSV được kiểm;59ca đủít nhất20hàng mỗi phía cả3bảng,1logts test-541642b59e N0/A41. Đọc codecat20/logskip/minnormalRCD; chưa chạy nên chưa biết kếtcục method. Giữ t/seed/nguồn nguyênbản, khaihạnchế trướcG3 và áp policy lỗi đangcó; không tựbỏA hoặc thêmcổng/pilottest. Kiểm lại timestamp log C-e với int(timestamp*NS), chuẩn hóa tuple/list cho60ca khớp F/H/đếmô/phânloại; không đổinguồn hay support.

Laptop đangAC/pin100% nhưng sleepAC45phút, hibernateAC0; chưa đổi thiếtlập, cần giữthức khi main đượcphép. Cuối free EC2_1~8,816GB,EC2_2~13,884GB;laptop~16,791GB lúcpreflight; RAM~7,40/~7,37/~3,26GB. Chưa có worstcase output/temp; quan sát/DRAIN theo quy tắc đãcó. Cuối haiEC2 không cóworkerT054 sống, local không cómainqueue, không cóactivated-001.

**Nguồn hiện hành:** reports/chuan-bi-main-006/bao-cao.md dẫn checkpoint-01-sources/01-plans/02-transfer và checkpoint-03-final. Trạng thái cuối là PREPARATION_AUDIT_COMPLETE_MAIN_BLOCKED_BY_SOURCE_CONTRACT, khôngready main. bo-tri-du-kien.json có mãmờ từnghost/planrefs; prepared/*.json là plan thật nhưngcandidate, không phảigrant. commands-prepared.json chốt lệnh kiểm/currentcandidate; source-bundle-final-prepared.json cóopen_before_run. activate_prepared.py chỉ tạo metadata sauG3/main grantriêng và nguồn đãhợp lệ, khôngphátmethod; đãkiểm preparationgrant bịtừchối và sourceblocker bịchặn trướcLOCKED. Receipt hiện tại PREPARATION không giả runtimeattestationv3. Không tạoquyềnmain từchatchuẩnbị.

Mức tiếp xúc phải khai: đãbăm/chuyển test; đọc TTtimestamp/schema và OBTime/header, metadataG1/native, authorCSVheader/time. Chưa đọc giátrịmetric/logmessage/operation đểphântích, chưa chạyRCA/ranking/chấm/độđo. Code khoa học/worker/cấu hình/cohort/seed/cửa sổ giữ103pin nguyên. Các phép chuẩn bị timestamp là phântíchnguồn, không kếtquảRCA. Nếu sửaadapter/giao thức từ thôngtin này phải khai mức tiếp xúc và ảnhhưởng, không gọi là thiết kế chưa từng thấy nguồn test.

Giữ các lỗi thao tác chuẩn bị và outputđãcó: datetime bịwildcardche, dựkiến11minute OBkhôngkhớpgiaothức nên sửa về3file baseline, so tuple/list chưachuẩnhóa và giảđịnhmọiAđủ20N làm lộnguồnthiếuN. Không dùng chúng làm thựcnghiệm, không chạy lại method. Initialvalidator005 chạy đến cuối lúcLOG đãnối nên báo lệchLOG; không khôi phụcLOG đểép hash, snapshot/prefix006 giữnguyên trướcphiên. Các giảđịnh khôngđạt khôngđược épđạt; evidence/sourceblocker hiện rõ.

**File thay đổi:** sáutệp đãcó so với005: LOG (chỉnối), đúngdòngSTATE, bốn hồsơT054 authorization/source-manifest/ho-so-g3/runbook. Đầu ra/helper/receipt/report mới chỉ trong results/T054 và vùngprivateT054 theoSPEC/quyềnnguồn. AGENTS,DECISIONS,SPEC,src,9scriptworker và dữliệugốc khôngsửa. Dữliệumới chỉ giải nénA vào vùngprivate mới. G2/pilot/kếtquảhỏng cũ giữnguyên. 5291đầura005 khôngthuộc sáufilemutable đượcxácminhgiữnguyên. Manifest006 và validator kiểm đúngtrạngtháicóchặn, khôngnhậnG3/ready.

**Chưa xong/điều cầnMinh:** xử lý4caOB trái hợpđồng reader trướcG3; hạnchếA khai riêng; xétG3/quyềnphát main và giữlaptopthức saukhi nguồn đượcxửlý. Không xin lại quyềnchuẩnbị nguồn/transfer đãcấp. RE3adapter/H1/H2 chưa làm trong lượt này, quyềncuối riêng; chưa giảiquyếtRQ3 hoặc có bằngchứnghiệuquả/cơchế. Không commit/push. Đềnghị nộidungcommit khi Minh muốn: “Chuẩn bị nguồn và phân lô P7 ba máy; ghi điểm chặn hợp đồng OB trước main”.

**Bước tiếp theo chính xác:** DỪNG báo Minh, trình bốtrí dựkiến và OB-source-blocker.json. Nếu đượcgiao tiếp, đọc src/p3/nezha.py::_doc_cua_so, src/m1/adapter.py::ca_nezha, các tuyến baseline OB và hợpđồngQ85/T026 trước; phântíchphươngán giữđúngtimestamp/nativecounts và tươngđươngđầuvào, trình exactpatch/file/ảnhhưởng/quyền rồi mới sửa. Không tự chọn cắt/bù/loạica, không chạy phươngpháp test hoặc adapterRE3 theo grant này. Chỉ kiểmsource/code/synthetic đượcduyệt, giữ đầu ra chuẩn bị/cloud đãhợp lệ; không dựng lại hoặc reuploadTT.

Lệnh kiểm nhận tiếp chỉđọc, cũng là lệnh cuối sau niêm phong:
D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B results/T-054/runs/chuan-bi-main-006/verify_checkpoint.py --manifest results/T-054/manifest-chuan-bi-main-006.json

### Prompt Claude — chỉ để Minh chọn chuyển

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-054; tasks/T-054-khoa-g3-chay-p7-a/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P7(a), chuẩn bị trình G3.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện.
- Tài liệu gốc: SPEC và LOG task; docs/MRP.md; các nguồn đề tài bên dưới; snapshot trước lượt tại results/T-054/runs/chuan-bi-main-006/before/.
- Phản biện và phản hồi trước: các bản REVIEW trong thư mục task theo thứ tự tên và phần đáp tương ứng trong LOG.
- Code và kết quả liên quan: results/T-054/; reports/chuan-bi-main-006/bao-cao.md; manifest-chuan-bi-main-006.json; Python D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B; lệnh kiểm tại runbook.md.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; chưa cấp bản phản biện ghi mới.

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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```


## Phiên 8 — 06/11/2026 — Codex, Windows, người làm — lưu kế hoạch phân bổ

Ý định EXECUTE chỉ việc ghi hồ sơ được Minh duyệt; Codex giữ vai trò người làm T-054, Claude là người phản biện chính thức. Không triển khai code, sinh lại plan thực thi, SSH, chuyển dữ liệu, chạy phương pháp, chấm test, mở telemetry RE3, đổi máy/nguồn điện, commit hoặc push.

### Quyết định của Minh trong phiên

Nguyên văn: “duyệt ghi, lưu ý, trong số 2 ec2, có 1 ec2 có disk lớn hơn, phân bổ hợp lý nếu cần nhiều disk”.

Phạm vi hiểu và thực hiện: lưu bảng phân bổ đã trình cùng lưu ý dung lượng vào LOG; nối nguồn duyệt trong DECISIONS; cập nhật đúng dòng T-054 STATE. Đây là duyệt ghi kế hoạch, không phải duyệt G3, quyền thực thi các sửa src/điều phối, truyền thêm nguồn hay phát main/RE3. Không nhận là phương án đã chứng minh tối ưu. Ma trận phương pháp RE3 vẫn OPEN.

### Kế hoạch phân máy đã trình và được duyệt ghi

Một ca là một sự cố; một lượt là một lần thực thi phương pháp/đối chứng trên một cửa sổ và một seed. TORAI ba seed là ba lượt/ca. M1 được khóa một bản chính; sáu vế phụ là đối chứng đã khai, không phải sáu ứng viên để chọn lại sau test. Bảy vế gồm M1 chính, bỏ E1, bỏ E2, bỏ E5, C-a0, C-a1 và T12 bật cạnh snapshot.

| Máy | Dataset/ca | Dữ liệu | Việc làm | Tối đa đồng thời |
|---|---|---|---|---:|
| EC2_1 — 13.211.127.97 | RE2-TT 35 ca | 105 parquet: metric/trace/log | M1 chính và sáu đối chứng; BARO, SimpleRCA, TraceRCA, TORAI B; C-e, C-d3 | 2 lượt |
| EC2_2 — 3.107.156.186 | RE2-TT 25 ca | 75 parquet thuộc lô; giữ bản đã có ngoài lô, không tự xóa | Các phần TT giống EC2_1 | 2 lượt tổng của máy |
| EC2_2 | Nezha-OB 34 ca | Tổng 226 tệp khác nhau; metric theo nguồn và trace/log đúng giao thức, nhiều ca chung tệp | M1 chính và sáu đối chứng; BARO, SimpleRCA, MicroRank, TraceRCA | Dùng chung giới hạn 2 với TT |
| Laptop | RE2-TT đủ 60 ca, chỉ các phương pháp được giao | CIRCA: metric/trace; MicroRank: trace; TORAI A: metric và 3 CSV tác giả/ca | CIRCA, MicroRank, TORAI A; điều khiển/nhận/kiểm/chấm | Tối đa 2 lượt khi đủ RAM |
| EC2_1 — đợt RE3 | RE3-OB dự kiến 15 ca | Dự kiến 45 parquet, chỉ sau quyền nguồn RE3 riêng | M1 bản cuối và các phương pháp/đối chứng còn phải khóa | 2 lượt |
| EC2_2 — đợt RE3 | RE3-OB 15 ca còn lại | Dự kiến 45 parquet, cùng điều kiện trên | Như EC2_1 | 2 lượt |
| Laptop — đợt RE3 | Tổng hợp 30 ca | Kết quả đã kiểm; nhãn evaluator riêng | Nhận/kiểm/chấm/báo cáo; chưa mặc định giao thêm thuật toán | Không cộng lượt phương pháp |

Laptop và EC2 dùng cùng ca TT nhưng chia phương pháp; không chạy trùng cùng phương pháp/ca. RE3 15–15 là bố trí dự kiến để chuẩn bị, chưa có ma trận thực thi cuối hoặc bằng chứng cân tải RE3.

### Ma trận số lượt đợt chính

| Phương pháp/vế | EC2_1 TT35 | EC2_2 TT25 | EC2_2 Nezha34 | Laptop TT60 | Tổng |
|---|---:|---:|---:|---:|---:|
| M1 chính | 35 | 25 | 34 | 0 | 94 |
| M1 bỏ E1 | 35 | 25 | 34 | 0 | 94 |
| M1 bỏ E2 | 35 | 25 | 34 | 0 | 94 |
| M1 bỏ E5 | 35 | 25 | 34 | 0 | 94 |
| C-a0 | 35 | 25 | 34 | 0 | 94 |
| C-a1 | 35 | 25 | 34 | 0 | 94 |
| T12 bật cạnh snapshot | 35 | 25 | 34 | 0 | 94 |
| BARO | 35 | 25 | 34 | 0 | 94 |
| SimpleRCA | 35 | 25 | 34 | 0 | 94 |
| TraceRCA | 35 | 25 | 34 | 0 | 94 |
| MicroRank | 0 | 0 | 34 | 60 | 94 |
| CIRCA | 0 | 0 | 0 | 60 | 60 |
| TORAI B: ba seed | 105 | 75 | 0 | 0 | 180 |
| TORAI A phụ: ba seed | 0 | 0 | 0 | 180 | 180 |
| C-e đủ lịch sử | 33 | 25 | 0 | 0 | 58 |
| C-d3 TT | 35 | 25 | 0 | 0 | 60 |
| **Tổng** | **523** | **375** | **374** | **300** | **1572** |

| Máy | Lượt thực thi dự kiến | Dòng không hỗ trợ, không gọi lõi | C-e thiếu lịch sử | Tổng vị trí quản lý |
|---|---:|---:|---:|---:|
| EC2_1 | 523 | 0 | 2 | 525 |
| EC2_2 | 749 = 375 TT + 374 Nezha | 68 = CIRCA Nezha34 + TORAI B Nezha34 | 0 | 817 |
| Laptop | 300 | 0 | 0 | 300 |
| Tổng | 1572 | 68 | 2 | 1642 |

1572 là lượt dự kiến có hỗ trợ, không bảo đảm tất cả thành công hoặc mọi lượt C-d3 sẽ thực hiện giải. Nếu công cụ vẫn dùng một tiến trình để tạo dòng UNSUPPORTED, đó là overhead vận hành, không là lần gọi thuật toán. 1640 vị trí thực thi theo cơ cấu cũ cộng 2 dòng C-e hỗ trợ thành 1642; không cộng dòng không hỗ trợ vào số lần học/chẩn đoán.

| Việc khác | Số lượng | Cách đếm |
|---|---:|---|
| Chuẩn bị TORAI B theo hiện trạng | 180: EC2_1 105, EC2_2 75 | Bước trong tuyến TORAI, không thêm vào 1572 lần gọi phương pháp |
| Chuẩn bị TORAI A | 180 trên laptop | Như trên; chưa áp cache mới |
| C-d1/d2 | 188 kết quả dẫn xuất | Không chạy lại M1 |
| C-c/C-g | 188 kết quả dẫn xuất | Dùng đầu ra baseline + graph M1 cần thiết, không chạy lại để tạo chúng |
| C-d3 Nezha | 34 dòng hỗ trợ/mô tả | Không gọi bộ giải mới |

P/S_lo/S_hi tính chung trong lượt M1, không nhân ba số lần gọi. CIRCA chính/phụ và MicroRank chính/phụ cùng lượt, không nhân đôi. Tổng bảy vế M1 là 658 lượt. C-e 58 đủ lịch sử, 2 thiếu; không biến thiếu lịch sử thành 0 hay nền khỏe.

### Dữ liệu tái dùng và dung lượng đĩa

FACT theo các biên nhận đã kiểm hash của 005/006 (đơn vị GB thập phân, không phải số đo máy hiện tại):

| Máy | Đĩa tổng ở inventory005 | Đĩa trống cuối006 | Nguồn |
|---|---:|---:|---|
| EC2_1 | 30.083.776.512 byte, khoảng30,08GB | 8.816.369.664 byte, khoảng8,82GB | runs/trien-khai-005/ec2_1-inventory.json#/stdout (JSON lồng)/disk/total; runs/chuan-bi-main-006/ec2_1-final-idle.json#/stdout (JSON lồng)/free_bytes |
| EC2_2 | 40.424.828.928 byte, khoảng40,42GB | 13.884.280.832 byte, khoảng13,88GB | Các file ec2_2 tương ứng, cùng con trỏ |

EC2_2 có cả đĩa tổng lớn hơn và đĩa trống nhiều hơn tại checkpoint. Đặt toàn Nezha trên máy này phù hợp lưu ý Minh; không cần đảo hai máy chỉ vì cân số lượt. 35–25 là phương án cân công việc tham chiếu thô, chưa kiểm tối ưu toàn cohort.

- EC2_1 dùng lại TT30 đã chuyển; chỉ cần thêm5ca/15parquet/46.083.552byte khi được phép truyền. Năm mã mờ đề xuất từ metadata kích thước: test-053c028c65, test-3a4c777083, test-327ac2a20e, test-071883754c, test-e654f8c5ab. Chưa đổi chủ thực thi hoặc chép tệp.
- EC2_2 đã có nguồn cho25TT được giao; không xóa bản5ca còn lại. Nezha226tệp/1.598.103.311byte là toàn nguồn cần, không phải dung lượng chắc chắn phải truyền thêm. Kiểm inventory/hash bản Nezha cũ rồi chỉ bổ sung phần thiếu/khác; chưa thực hiện SSH/đọc telemetry.
- Laptop có TT và nguồn A180CSV/9.244.910byte. Không giải nén/dựng lại chỉ vì lưu kế hoạch.
- RE3 toàn nguồn metadata138.129.790byte, chưa tải/mở telemetry. Chưa chia byte15ca/máy vì kích thước từng ca khác nhau.
- Trước phát lô phải tính dung lượng đồng thời: nguồn còn thiếu + đầu ra + tệp tạm + mọi lượt hỏng + gói nhận/giải nén. Tái dùng kích thước đầu ra cũ, không chạy lại để lấy dự toán. Chưa có cận trên dung lượng toàn cohort, không gọi là đủ đĩa chỉ từ raw hoặc số ca.
- Nếu phần cần nhiều đĩa vượt khoảng trống của EC2_1, ưu tiên bố trí phần độc lập ấy ở EC2_2; phải cập nhật partition/nguồn/phụ thuộc trước thực thi, không tự chuyển chủ đang chạy hoặc phát trùng. Không tự xóa dữ liệu/kết quả hay mở rộng/thay đổi máy từ lời lưu ý này. RE3 chỉ xét lệch15–15 khi có ma trận, dung lượng và kế hoạch cụ thể; hiện giữ phần đó OPEN.

### Song song, thứ tự và điều kiện

Đợt chính tối đa6lượt tính toán:2mỗi EC2 và2laptop khi đủRAM. Đợt RE3 dự kiến tối đa4lượt trên2EC2; laptop nhận/kiểm/chấm. Đây là trần đề xuất, không là hệ số tăng tốc. Công cụ hiện còn khóa cùng phương pháp; sửa/bỏ khóa và kiểm nó là việc chưa thực hiện và cần quyền triển khai đúng phần.

| Việc | Tuần tự bắt buộc | Phần độc lập |
|---|---|---|
| Nguồn | Quyền/hash/hợp đồng trước dùng | Chuẩn bị theo máy có thể song song |
| TORAI | Chuẩn bị bảng đúng → chạy seed | Các ca/seed độc lập, đầu ra mỗi lượt riêng |
| M1 và C-d3 | M1 chính ca đó niêm phong → C-d3 ca đó | Không chờ M1 toàn cohort |
| M1 và sáu đối chứng | Từng vế đúng cấu hình/nguồn đã khóa | Không bắt chạy bảy vế tuần tự trên từng ca |
| Baseline/M1/C-e | Không có phụ thuộc buộc baseline chờ M1 | Lượt độc lập chạy song song |
| C-c/C-g | Đủ kết quả baseline/graph cần dùng | Dẫn xuất cho ca đủ đầu ra trước |
| Ghép nhãn/chấm | Snapshot/binding và điều kiện A4 đủ | Nhận/kiểm file trước được; không xem điểm sớm |

Ưu tiên đề xuất: M1 chính cùng TORAI B TT và SimpleRCA Nezha; tận dụng phần còn lại cho baseline/đối chứng/C-e; C-d3 ngay sau seal cha; laptop chạy phần riêng đồng thời. Đây là ưu tiên điều phối, không tạo phụ thuộc khoa học mới. Lỗi chưa phân loại vẫn BLOCKED; đề xuất thu hẹp phạm vi dừng theo phụ thuộc chưa được triển khai. Lỗi một máy không tự cho phép chạy bản sao trên máy khác.

### RE3 và phần chưa khóa

Chuẩn bị hợp đồng/schema/đơn vị/inventory/adapter và kiểm tổng hợp phải làm trước G3 theo SPEC; đánh giá RE3 bản cuối theo quyền riêng sau đợt chính và các sửa đổi cần thiết theo Q-247. Không pilot/tune trên telemetry RE3, không nhập RE3 vào bảng A4 của94ca. Dataset RE3 có30ca/10ô; chưa xác định đủ phương pháp hỗ trợ, vế đối chứng, cửa sổ và seed nên không có tổng lượt RE3 hợp lệ. Tổng toàn kế hoạch =1572lượt đợt chính + số lượt RE3 sẽ được khóa, không phải1572+30.

Phần chuẩn bị RE3 còn mở: đơn vị thời gian/duration; inventory/alias và namespace; profile metric/log/coverage; support matrix; adapter và kiểm tổng hợp; code/env/binding/bảng riêng; quyền bản cuối. Hợp đồng nguồn: runs/trien-khai-003/hop-dong-re3.json. Không dùng bốn root nhãn làm inventory hoặc tự áp ma trận TT/Nezha.

### Kiểm, phạm vi file và tiếp nhận

Đã kiểm trước ghi:7file nguồn về inventory/disk/placement/danh sách/kích thước khớp manifest-chuan-bi-main-006.json; phép cộng ma trận và phép gán metadata35/25/Nezha khớp523/375/374/300 và525/817/300vị trí. Không chạy phương pháp để kiểm bảng. Nguồn khối lượng/vế là SPEC T-054 phần Khối lượng, matrix.json và checkpoint006. Các kế hoạch prepared/*.json vẫn30–30/laptop922 theo checkpoint006, chưa đổi thành35–25. Protocol/authority vẫn ứng viên, không có grant main mới.

Chỉ3file được ghi: LOG này (chỉ nối), docs/DECISIONS.md (chỉ nối lời duyệt), đúng dòng T-054 docs/STATE.md. Giữ SPEC, src, AGENTS, WHY, protocol, authorization, các plan/manifest và kết quả cũ. Manifest006 từ đây là mốc lịch sử trước lượt ghi này; không sửa manifest hoặc khôi phục LOG/STATE để ép khớp.

Task đạt: lưu bảng phân bổ và căn cứ đĩa để tiếp nhận. Chưa đạt: sửa/kiểm OB, triển khai lịch mới, hoàn thiện RE3 hoặc G3/main. Câu hỏi nghiên cứu RQ3 chưa có kết quả mới. Chưa có bằng chứng hiệu năng toàn cohort hay cận đĩa; không biến duyệt ghi thành xác nhận các giả định.

Bước tiếp theo chính xác: đọc mục này cùng SPEC, runs/chuan-bi-main-006/OB-source-blocker.json, runs/trien-khai-003/hop-dong-re3.json và quyết định mới cuối DECISIONS; trình/nhận quyền triển khai đúng phần OB/điều phối/nguồn trước sửa. Đối chiếu dung lượng nguồn + đầu ra/tạm/giữ lượt hỏng trước chốt partition, ưu tiên EC2_2 cho phần cần đĩa. Không phát run/resume hoặc activate_prepared.py từ quyền ghi này.

Lệnh cuối cần chạy trong lượt ghi: kiểm đọc-only phép cộng/prefix LOG và DECISIONS, đúng dòng STATE, pin code/plan bảo toàn và diff đủ3file. Không chạy kiểm toàn manifest006 với kỳ vọng LOG/STATE còn ở mốc cũ. Đề xuất nội dung commit khi Minh yêu cầu: “Lưu kế hoạch phân bổ P7 ba máy và ưu tiên dung lượng EC2_2”. Chưa commit/push.

### Prompt Claude — chỉ để Minh chọn chuyển

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-054; tasks/T-054-khoa-g3-chay-p7-a/SPEC.md; mục Phiên 8 trong LOG của task..
- Công đoạn: soát kết quả.
- Gói/cổng: P7(a), chuẩn bị trình G3.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện.
- Tài liệu gốc: SPEC/LOG T-054; docs/STATE.md; docs/DECISIONS.md; docs/MRP.md và các nguồn đề tài bên dưới.
- Phản biện và phản hồi trước: các bản phản biện trong thư mục task và các phần đáp tương ứng trong LOG, theo thứ tự thời gian.
- Code và kết quả liên quan: results/T-054/; manifest-chuan-bi-main-006.json (mốc lịch sử); hướng dẫn kiểm trong LOG/runbook; Python D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; chưa cấp bản phản biện ghi mới.

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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

### Kết thúc lượt ghi ngày 06/11/2026

Đã lưu bảng từng máy/dataset/phương pháp, tổng lượt, thứ tự và song song; ghi lưu ý ưu tiên EC2_2 có đĩa lớn hơn. File đã đổi đúng3: LOG chỉ nối; DECISIONS chỉ nối; STATE đúng dòng T-054. Kiểm sau ghi PASS: prefix LOG/DECISIONS nguyên vẹn;7nguồn khớp manifest006;110file code/nguồn điều phối và kế hoạch cũ được bảo toàn; tổng1572+68+2=1642; prompt chép đúng3khối mẫu; git diff --check không có lỗi whitespace (Git chỉ nhắc quy ước LF/CRLF hiện có). Chưa triển khai, không chạy/chấm/mở dữ liệu, không thay máy. RE3/support/adapter, xử lý OB và G3/main vẫn OPEN. Bước tiếp theo và prompt ở phía trên.

Lệnh cuối của lượt: `git diff --check -- docs/DECISIONS.md docs/STATE.md tasks/T-054-khoa-g3-chay-p7-a/LOG.md`.


## Bổ sung sau Phiên 8 — 06/11/2026 — Codex, Windows, người làm — đáp đánh giá kế hoạch

### Quyền và phạm vi

Minh trả lời nguyên văn “DUYỆT” cho đề xuất nối đúng một mục LOG: phản hồi hai nhận xét, căn cứ giữ từng phương pháp trên laptop, bảng tải kèm giới hạn và con trỏ tới bản lệnh cuối. EXECUTE chỉ ghi mục này. Codex vẫn là người làm; Claude là người phản biện chính thức. Đánh giá Codex bổ sung do Minh chuyển là đầu vào, không tự là lệnh sửa.

Chỉ nối LOG. Không đổi phân máy, code, plan, manifest, STATE hoặc DECISIONS; không SSH, truyền nguồn, thực nghiệm, chấm test, mở telemetry RE3, đổi máy, commit/push. Quyền ghi không tự cấp quyền triển khai hoặc thay trạng thái quyết định nghiên cứu.

### Tự soát và phản hồi

Trong lượt chỉ đọc trước duyệt ghi, đã đối chiếu timing, chứng cứ parity gốc, hai trường con trỏ lệnh và tuyến activate_prepared.py, rồi kiểm từng ý của đánh giá bổ sung.

| Nhận xét | Kết luận | Bằng chứng và xử lý |
|---|---|---|
| Căn cứ giữ phần việc trên laptop còn thiếu | Đúng về hồ sơ; không đồng nghĩa phải chuyển cả ba phương pháp lên EC2 | Phiên 8 chưa lưu đủ lý do riêng và tác động thời gian. Bổ sung dưới đây; không đổi phân máy hoặc nhận 35/25 tối ưu |
| Hai con trỏ /commands ghim bản cũ | Đúng | bo-tri-du-kien.json và checkpoint-03-preflight.json ghim bản 5.952 byte; tệp cuối 6.290 byte khớp manifest 006. Tuyến activate không đọc hai trường đó; chưa có bằng chứng gây chạy sai. Dẫn pin cuối dưới đây, giữ nguyên checkpoint/manifest |

Không có bằng chứng từ hai điểm này buộc đổi nền M1, ma trận khoa học hoặc loại ca. Các chặn OB, RE3 và tuyến mới vẫn phải giải quyết.

### Căn cứ giữ từng phần trên laptop

- **CIRCA TT:** Linux chạy được nhưng từng không đạt parity (đối chiếu số học) với bản tham chiếu laptop. Nguồn `results/T-032/runs/circa-k2-test-001/cases/dev-a5cabe5fa7/sham/check.json#/exact_vs_frozen=false`; `/difference_count_vs_frozen` là 264 ở ols+rht_da và 149 ở ols+rht. Giữ 60 lượt laptop tránh mở thêm việc kiểm/phân xử môi trường trước main; không phải yêu cầu Windows hoặc khẳng định mọi Linux đều khác.
- **MicroRank TT:** nguồn `results/T-032/runs/microrank-cohort-failure-001/comparison-summary.json#/failed_case/numeric_summary` ghi 179 điểm không exact, tối đa 41 ULP và 126 điểm ngoài ngưỡng lịch sử. `/failed_case/service_order_exact` và `/failed_case/service_tie_partition_exact` vẫn true. Sai khác số học chưa chứng minh đổi hạng hoặc sai thuật toán. Ngoại lệ MicroRank OB đã chấp nhận không tự áp cho TT. Giữ 60 lượt laptop tránh phát sinh thêm phép kiểm/quyết định khác biệt này trước main.
- **TORAI A:** có tiền lệ EC2, không bắt buộc Windows hoặc thiếu môi trường. Giữ 180 lượt trên laptop là CANDIDATE phân tải: dùng máy thứ ba trong khi EC2 mang phần M1/TT/Nezha; nguồn A đã có local và tuyến local đã kiểm. Lập luận chỉ phù hợp nếu phần laptop cộng nhận/kiểm/chấm không vượt đường găng EC2; chưa có số đo toàn lô xác nhận. Không coi chuyển A lên EC2 chắc chắn chậm hoặc local luôn tốt. Một logts thiếu N vẫn là giới hạn đầu vào; lỗi chưa phân loại giữ BLOCKED, không tự tính 0.

Hai chứng cứ parity trên đã kiểm qua chuỗi `results/T-032/runs/bo-sung-toan-dien-20261012-001/manifest-final.json#/files` → `old-files-before.json#/files` → từng chứng cứ. Không chạy lại baseline để biện minh lịch.

### Tải tham chiếu ba máy — không phải ETA

Nguồn timing đã kiểm pin theo manifest 006: `results/T-054/runs/trien-khai-003/pilot-local-007/summary.json#/group_wall_s`; C-e từ `results/T-054/runs/trien-khai-004/pilot-2-worker-001/summary.json#/rows/0/cost_s`.

T là tổng timing mẫu một ca TT của bảy vế M1, BARO, SimpleRCA, TraceRCA, TORAI B ba seed và C-d3. C là một lượt C-e. O là một ca Nezha của bảy vế M1 và bốn baseline hỗ trợ. Timing laptop dùng làm thước chung cho hai EC2, chưa là tốc độ cloud. Không cộng UNSUPPORTED vào thời gian lõi.

| Máy | Công thức | Giây tham chiếu | Giờ tham chiếu tuần tự |
|---|---|---:|---:|
| EC2_1 | 35T + 33C | 47.753,54 | 13,27 |
| EC2_2 | 25T + 25C + 34O | 47.764,60 | 13,27 |
| Laptop | 60 CIRCA + 60 MicroRank + 60 × ba seed A | 7.907,50 | 2,20 |

T=1.128,516871 giây; C=250,165208 giây; O=391,104330 giây. Phần laptop gồm CIRCA 1.326,00 giây, MicroRank 986,21 giây và TORAI A 5.595,29 giây. Đây là tổng suy từ mẫu, không phải thời gian đã đo trên 60 ca. Không chia cho hai rồi gọi ETA hoặc hứa tăng tốc theo số tiến trình.

**Giả định và điều kiện sai:** chủ yếu một ca DEV/phương pháp; MicroRank/TraceRCA TT có mẫu ERROR, không đại diện thời gian chạy thành công; C-e từ gói đồng thời khác. Tốc độ tương đối giữa phương pháp chưa được chứng minh giữ nguyên trên EC2. Một ca M1 EC2_2 khoảng 67 giây không đủ áp một hệ số cho toàn ma trận; EC2_1 có output khôi phục nhưng cost/supervisor không hợp lệ để đo. Cold path, tranh chấp CPU/RAM/I/O, ca đuôi dài, lỗi, nhận/hash/giải nén/kiểm/chấm chưa được tính đủ. Laptop thành đường găng nếu tổng các phần đó vượt thời gian thực của hai EC2 hoặc sleep/thiếu RAM/đĩa/lỗi giữ nó lại.

Các số hỗ trợ 35/25 ở mức ứng viên và khả năng dùng laptop; không chứng minh tối ưu hoặc laptop chắc chắn xong sớm. Chỉ kiểm thêm tuyến/môi trường thực sự khác khi được phép, không chạy baseline/pilot diện rộng để bảo vệ phương án.

**Chi phí còn thiếu:** bổ sung 5 TT/15 parquet/46.083.552 byte tới EC2_1 khi có quyền; Nezha 226 tệp/1.598.103.311 byte là toàn nguồn, không là số chắc chắn phải chuyển. Cần kiểm inventory/hash bản cũ EC2_2 rồi chỉ bổ sung phần thiếu/khác. Chưa đo thời gian chuyển/hash phần mới hoặc cận đầu ra/tệp tạm/giữ lượt hỏng; không lấy tốc độ chuyển TT006 làm cam kết. EC2_2 có đĩa lớn hơn nên tiếp tục ưu tiên Nezha ở đó; không suy đủ đĩa chỉ từ raw.

### Con trỏ lệnh cuối cho tiếp nhận

Dùng tệp `results/T-054/runs/chuan-bi-main-006/commands-prepared.json` cuối 6.290 byte và pin tại `results/T-054/manifest-chuan-bi-main-006.json#/outputs/results~1T-054~1runs~1chuan-bi-main-006~1commands-prepared.json` (JSON Pointer). Không dùng pin 5.952 byte trong `/commands` của `bo-tri-du-kien.json` hoặc `checkpoint-03-preflight.json`; đó là tham chiếu sơ bộ lịch sử đã cũ.

Đã đọc `activate_prepared.py::activate`: dùng protocol/source bundle/failure policy/grant, không đọc hai trường cũ. Chưa có bằng chứng chạy sai. Giữ nguyên manifest 006/checkpoint, không khôi phục tệp để ép pin. Bản lệnh cuối vẫn là tuyến 006, không phải bộ lệnh 35/25 đã khóa. Lịch mới cần plan/nguồn/env/lệnh đúng byte và kiểm sau quyền triển khai riêng; không activate/run/resume từ quyền ghi LOG.

### Kết thúc lượt và tiếp nhận

Đã làm: bổ sung phản hồi hai nhận xét, căn cứ laptop, bảng tải và con trỏ lệnh. File duy nhất đổi: LOG này, chỉ nối. Kiểm: nguồn timing/lệnh khớp manifest 006; chứng cứ T032 được kiểm chuỗi pin; tính lại công thức 47.753,54/47.764,60/7.907,50 giây. Sau ghi kiểm prefix LOG, prompt mẫu, pin các file bảo vệ và diff whitespace. Không thực nghiệm hoặc thay quyết định nền/phân máy.

Đề xuất dừng phần phản biện kế hoạch nếu kiểm bổ sung không phát sinh bất đồng mới; Minh quyết chuyển prompt hay dừng. Không còn phản đối hai nhận xét đã kiểm ở trên. Còn OPEN: hợp đồng OB bốn ca; RE3 đơn vị/inventory/support/adapter/bảng riêng; kiểm tuyến mới; dung lượng; khóa G3/quyền main. Bổ sung hồ sơ không gỡ các chặn đó, không trả lời RQ3 hoặc xác nhận cơ chế/hiệu quả.

Bước tiếp theo: đọc mục này cùng Phiên 8, SPEC, OB-source-blocker.json và hop-dong-re3.json; Minh chọn kiểm tiếp hoặc triển khai đúng gói đã trình. Không có quyền triển khai từ “DUYỆT” ghi LOG này. Giữ mọi kết quả, không tự đổi chủ lô/phát trùng/chuyển nguồn/mở RE3. Đề xuất commit khi Minh yêu cầu: “Bổ sung căn cứ phân tải laptop và con trỏ lệnh P7 cuối”; chưa commit/push.

### Prompt kiểm tiếp — Minh chọn chuyển, không tự gửi

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-054; tasks/T-054-khoa-g3-chay-p7-a/SPEC.md; Phiên8 và mục bổ sung ngày06/11 trong LOG task..
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P7(a), chuẩn bị trình G3.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện chính thức. Đánh giá bổ sung Codex trong chat không đổi vai trò..
- Tài liệu gốc: AGENTS.md; docs/STATE.md; SPEC/LOG T054; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; nguồn đề tài bên dưới.
- Phản biện và phản hồi trước: các nguồn phản biện/phản hồi được LOG dẫn theo thời gian; đánh giá Codex bổ sung do Minh chuyển kèm.
- Code và kết quả liên quan: src/; results/T-054/; các manifest nguồn được dẫn trong LOG; nguồn T031/T032/T053 liên quan; môi trường D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc, kiểm chỉ đọc và trả lời trong chat; chưa cấp bản REVIEW hoặc quyền sửa file/thực nghiệm/SSH/truyền nguồn/mở dữ liệu/đổi máy/commit/push.

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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

Lệnh cuối cần chạy: `git diff --check -- tasks/T-054-khoa-g3-chay-p7-a/LOG.md`.


## Phiên dài chuẩn bị trước G3 — 06/11/2026 — Codex, Windows, người làm

Minh: “DUYỆT TRIỂN KHAI PHIÊN DÀI CÁC BƯỚC 1 2 3 4 NHƯ ĐỀ XUẤT, VÌ PHIÊN DÀI NÊN CẦN CHECKPOINT, BÁO CÁO CẨN THẬN, TRÁNH VIỆC BỊ MẤT THÔNG TIN DO CONTEXT BỊ NÉN”. Đã bắt đầu bước1; giữ checkpoint tại results/T-054/runs/phan-xu-truoc-g3-007/bang-chung.json. Vai trò Codex làm, Claude phản biện giữ nguyên. Quyền theo đề xuất: phân xử đầu vào rồi trình patch cụ thể trước sửa lõi; dừng trước main. Không suy quyền mở telemetry RE3/G3, thay máy, commit/push.


### Checkpoint007 — phân xử hợp đồng, trước patch lõi

Đã kiểm103pin code và nguồn006/metadataRE3. Lấy schema90footer bằngexactrange, tổng1.491.735byte;5schema metric/1trace/1log; không data pages/minmax/methodRE3. Metadata partition523/749/300+68+2 đúng1642khóa. Báo cáo và exactscopepatch tại results/T-054/runs/phan-xu-truoc-g3-007/bao-cao.md; bằng chứng và thất bại giữ trong bang-chung.json.

Bước1 đạt code/schema/đếm; hợp đồngOB và RE3 units/inventory cònOPEN. Bước2 chưa cài core; bước3 chưaSSH/chuyển/compileplan; bước4 chưađủG3. Bảnvá cần thêm chuoi.py và worker.py để biểu diễn và bật layoutper-source, ngoài3fileứngviênbanđầu. Theođềxuấtđãduyệt phải trình đúngpatch trướcsửa. Không tựcoi quyềnphiêndài làduyệtthiếtkếchưađược trình.

File đổi đúng5: báo cáo,bằng chứng,manifest007,LOGchỉnối,STATEđúngdòngT054. Src/SPEC/WHY/DECISIONS/codeplan cũ giữnguyên; khôngmain/chấm/telemetryRE3/commit/push. Lệnh tiếp nhận: đọc báo cáo007 vàbang-chung; kiểmmanifest007 rồi tiếp tục sau quyếtđịnhpatch. Đềxuấtcommit khicóyêucầu: “Phân xử hợp đồng OB và bổ sung schema RE3 trước G3”.

### Prompt Claude — Minh chọn chuyển

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-054; đề xuất hợp đồng và patch tại results/T-054/runs/phan-xu-truoc-g3-007/bao-cao.md.
- Công đoạn: soát SPEC.
- Gói/cổng: P7(a), chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện chính thức.
- Tài liệu gốc: AGENTS.md; SPEC/LOG T054; docs/STATE.md, MRP.md, WHY.md, DECISIONS.md, LESSONS.md và nguồn đề tài dưới đây.
- Phản biện và phản hồi trước: các nguồn phản biện/phản hồi T054 được LOG dẫn theo thời gian.
- Code và kết quả liên quan: src/; results/T-054/; manifest-phan-xu-truoc-g3-007.json; môi trường D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; chưa có quyền ghi REVIEW, sửa code hoặc chạy thực nghiệm/SSH/mở dữ liệu/commit/push.

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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```


### Kiểm cuối checkpoint007

Manifest4outputs và9protectedfilesPASS; LOGprefix006giữ nguyên; schema90/90,total1.491.735byte;8fixture BARO tổnghợpPASS, chưa phải fullpatchparity. Đã trình câu hỏi duyệt patch8mục qua chat; chưa có trả lời ở mốc này. Không sửa core/WHY/DECISIONS/SPEC, chưaSSH hoặc phátplan. Tìm README/main/utility upstream chỉ thấy acquisition/đườngdataset, chưa xác nhận đơn vịint64RE3; giữOPEN.

Bước tiếp theo chính xác: đọc báo cáo007 mục Bản vá cụ thể; sau Minh duyệt mới sửa5filecode và đồngbộ3nguồnđược nêu, kiểm nhánh mặcđịnh/native/dev rồi tiếp bước3–4. Giữ90schema đã hợp lệ; không tải/lấy lại chỉ vì đổi phiên. Lệnh cuối: Python kiểm manifest007/protectedpins và git diff --check choLOG/STATE.


## Tiếp tục phiên dài — 06/11/2026 — Codex, Windows, người làm — checkpoint008

Minh: “NẾU BẠN THẤY ỔN THÌ DUYỆT” cho bảnvá8mục007. Tự soát: giữ default và index nguồn tường minh tránh giả mẫu; BARO per-column cho phép thử; chưa có mâu thuẫn chặn cài ứng viên. Đã kiểmmanifest007 trước dùng, snapshot10file vào008/before, ghi nguồnquyếtđịnh/WHY/SPEC trước cài. Không coi điều kiện duyệt là kiểmpari hoặc mởmain. Checkpoint008/checkpoint.json lưu quyền, pin trước và bước tiếp.


### Checkpoint008 — cài và kiểm OB

Đã cài5fileđúngscope;43kiểm OBtổnghợp002 và1TTmặcđịnh003PASS;92kiểm tíchhợpPASS. Giữ001/002hỏng: testnguồnrỗngBAROphảiOKlàsai (giữERRORgốc);fixtureTTthiếumốc t do runnercấp, chỉsửatest. MộtDEV OBdev-607751ac0a qua worker mới: rawrecordtoàn bộ vànormalizedinputdigest exact với receipt005 được007kếthừa, đãkiểmmanifest006. Không pilot4testOB/telemetryRE3. Dùnglaptop choexactparity nguồnlocal; chưa stagecloud.

Bước3: haihost SSH bằngoptions/hostkeypin đều timeoutport22; chưaxácnhận identity/đĩaRAM/env hoặc chuyểnnguồn/code. Không tự bật/tắtmáy. Receipt cloud-inventory-001.json. Tiếp candidateplanphi nhãn, giữ RE3units/inventory vàcloudchặnG3. Checkpoint008/checkpoint.json lưu quyền,pintrước,bằngchứng vàbước tiếp. Locatorrecordbanđầutìmtrực tiếp007khôngthấy; đãlần VERIFIEDinheritedreceiptđúng005, khôngchạylạimethod.


### Chỉ đạo Minh — tạm dừng riêng phần AWS

Minh: “CÓ THỂ TẠM DỪNG KIỂM PHẦN NÀY, SANG PHẦN KHÁC , HIỆN TÀI KHOẢN AWS ĐANG BỊ TẠM KHÓA, BẠN BÁO CÁO NHỮNG HỆ QUẢ KHI MẤT DỮ LIỆU TRÊN 2 EC2 NÀY”. Dừng SSH/sync/staging và kiểmcloud; tiếp phầnlocal vàbáocáohệquả. Không suy dữliệuEC2đãbịxóa từviệctàikhoảnbịkhóa. Đối chiếuinventory005 đãpin vàmanifest/bảnnhậnlocal, khôngtựmởlại taskcũ/chạylạithựcnghiệm. Quyền cloudpause ghiởcheckpoint008; khôngtựđổi sangmainlocal.


### Kết thúc checkpoint008 — báo cáo và tiếp nhận

Đã cài5fileđúngquyền,44kiểm source/defaultsynthetic và92tíchhợp;1DEVOBworkerrawrecord/inputexact. Candidate35/25đủ1642vịtrí,chặnWAIT_G3; rootprotocol/source/authtrỏ008,sourcema trậnkhoahọcgiữnguyên. Đọcbao-cao008đểbiếtgiớihạn. CloudtạmdừngriêngtheoMinh; khôngmain. BáocáoAWSvàkiểmhashgóilocalđãlưutrong008; thiếuđúngfullrawT048ởđườnglocalmanifest,cácnguồnP7cònlocal. KhôngsuydữliệuAWSđãmất. RE3có90schema/cardđúngrevision,metric.timeđãcónguồns;units/inventory/support/H2cònOPEN. Chưahoànthànhbước3cloud/bước4khóaG3hoặctoàntask/RQ3.

Fileđổi:5code;SPEC/WHY/DECISIONS;LOGchỉnối/STATEđúngdòngT054;rootprotocol/source-manifest/authorization/runbook/ho-so-g3;outputs/checkpoint/manifest008. Snapshot/diff/pinđủđểnhậntiếp. Lệnhcuối: kiểmmanifest008,protectedoutputs006vàdiff-check. Bướctiếpchínhxácởbao-cao008; khônglặp90schema/accepteddev/baselineđãhợp lệ. Đềxuấtcommitkhicóyêucầu: “Cài OB source-native, kiểm parity và ghi hệ quả AWS tạm khóa”; chưacommit/push. PromptchoClaudeđểMinhchọnchuyển; khôngtựgửi, chưanhậnClaudeđãkiểm008.

### Prompt Claude — checkpoint008

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-054; tasks/T-054-khoa-g3-chay-p7-a/SPEC.md; checkpoint008 tại results/T-054/runs/cai-ob-source-native-008/.
- Công đoạn: soát kết quả.
- Gói/cổng: P7(a), chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện chính thức.
- Tài liệu gốc: AGENTS.md; SPEC/LOG T054; docs/STATE.md, MRP.md, WHY.md, DECISIONS.md, LESSONS.md vànguồnđềtàibêndưới.
- Phản biện và phản hồi trước: nguồn phản biện/phản hồi được LOG dẫn theo thời gian.
- Code và kết quả liên quan: src/; results/T-054/manifest-cai-ob-source-native-008.json; code-diff.patch,bao-cao.md,checkpoint.json trong008; môi trường D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; không ghi REVIEW/sửa file/chạy phương pháp/SSH/truyền dữ liệu/mở dữ liệu khóa/đổi máy/commit/push.

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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```


## Tiếp tục phiên dài — 06/11/2026 — Codex, Windows, người làm — checkpoint009

Minh hỏi vì sao chưa hoàn thiện RE3 trước G3. Người làm đã dừng phần local quá sớm sau vá OB và báo cáo AWS; AWS chỉ chặn cloud. Tiếp tục bước1–4 đã duyệt: tra nguồn/schema, inventory, support và hợp đồng adapter, không mở telemetry. Đã kiểm 590 output008 và đúng bằng chứng schema007 trước tái dùng. Hai phép kiểm bootstrap áp full hash007 lên LOG/STATE hiện hành dừng vì hai file đã cập nhật008 hợp lệ; lưu thất bại trong checkpoint009, chuyển sang kiểm output bất biến thực sự dùng. Không sửa nguồn nghiên cứu để khớp manifest lịch sử. Exact H2 code/hợp đồng vẫn trình riêng theo003.


### Kết thúc checkpoint009 — chuẩn bị RE3 còn điều kiện

Đã phân tích lại đủ 5 schema metric/30ca từ 90footer đã lưu, không lấy lại footer hoặc mở data page. Inventory-schema ghi 12 owner chung/28 owner hợp; 2ca có tên namespace ngoài nhóm chung; chưa xác nhận dữ liệu thêm có tín hiệu hoặc là lỗi dataset. Đã phân biệt đơn vị mã hóa với cadence/r; metrics.time có nguồn khai giây, trace us là suy luận từ Jaeger/code, log unit/r/inventory vẫn thiếu nguồn RE3. Không dùng T039 Nezha làm deployment RE3.

Đã lập 8 dòng khả năng hỗ trợ theo code/schema, chưa tuyên bố hỗ trợ trên ca thật. 27 kiểm tổng hợp PASS: biên/đơn vị/parent-key/suffix; tái hiện ts-* làm rỗng metric cả5schema trong adapter TORAI TT. Hai literal dataset của BARO/TraceRCA không tự chứng minh lỗi số; đã thu hẹp nhận định003 bằng phân tích code. Không đổi hay mở lại kết quả task cũ. RQ3/RQ5 chưa được phân xử bằng RE3 vì chưa mở held-out; kết quả này chỉ phục vụ hợp đồng trước G3.

Đã trình bản vá H2 chính xác9filecode+SPEC/WHY/DECISIONS tại bao-cao009; chưa cài. Câu hỏi duyệt được gửi cho Minh, chưa coi là đã trả lời. Profile đơn vị/U/alias/r bắt buộc, thiếu thì chặn trước method; duyệt cài không tự chốt giả định chưa kiểm hoặc mở dữ liệu. H1 còn cần tài liệu exporter/deployment hoặc quyết định rõ về giả định chưa kiểm. Cloud vẫn tạm dừng riêng theo Minh, main/G3 chưa được mở.

File thay đổi lượt009: output runs/chuan-bi-re3-009/, manifest-chuan-bi-re3-009.json; LOG nối thêm và đúng dòng T054 STATE. Không sửa core, SPEC, WHY, DECISIONS, dữ liệu hay pin008; chưa commit/push. Hai phép kiểm bootstrap hash lịch sử dừng vì LOG/STATE đã cập nhật hợp lệ; đã đổi sang pin output bất biến dùng lại. urllib GitHub gặp lỗi chứng chỉ; PowerShell dùng trust Windows đọc metadata được. Một lệnh writer inline lớn bị policy từ chối không nêu lý do cụ thể; chuyển sang file script tường minh, không đổi quyền hoặc tắt xác thực.

Bước tiếp chính xác: đọc bao-cao009 mục Bản vá H2 và time-and-observation-contract.json; nhận quyết định Minh. Chỉ sau duyệt exact patch mới cài9filecode và các nguồn được nêu, kiểm synthetic/default rồi tạo checkpoint mới, không ghi đè009. Nếu chưa có nguồn unit/U/r thì giữ OPEN và chặn phần thực thi; không xem thử telemetry để chốt. Không SSH/sync khi AWS còn tạm dừng. Lệnh cuối: python -X utf8 -B results/T-054/runs/chuan-bi-re3-009/finalize.py rồi kiểm manifest009, hash protected008 và git diff --check trong phạm vi. Đề xuất commit khi Minh yêu cầu: “Chuẩn bị hợp đồng RE3, phân xử inventory và adapter trước G3”; chưa commit.

### Prompt Claude — checkpoint009

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-054; tasks/T-054-khoa-g3-chay-p7-a/SPEC.md; results/T-054/runs/chuan-bi-re3-009/bao-cao.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P7(a), chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện.
- Tài liệu gốc: AGENTS.md; SPEC/LOG T-054; docs/STATE.md, MRP.md, WHY.md, DECISIONS.md, LESSONS.md; các nguồn đề tài dưới đây.
- Phản biện và phản hồi trước: Các lượt được LOG T-054 dẫn theo thời gian.
- Code và kết quả liên quan: results/T-054/manifest-chuan-bi-re3-009.json; results/T-054/runs/chuan-bi-re3-009/; source-pins.json; D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ đọc và trả lời trong chat; không sửa file, không chạy phương pháp, không mở dữ liệu khóa, không SSH/sync, không commit/push.

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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```


### Kiểm cuối009

27 kiểm synthetic PASS;588 output008 bất biến giữ hash, LOG008 giữ prefix, STATE008 khớp snapshot trước009 và chỉ thay đúng dòng T054. 14 source file trong source-pins giữ nguyên. Lượt finalize đầu dừng do key path Windows; lượt hai đã ghi LOG/STATE rồi dừng ở phép kiểm full hash STATE008; không replay mutation, hoàn tất bằng finish_validation.py và ghi nguyên thất bại trong checkpoint. Manifest009 pin đầu ra mới; không mở telemetry/main hoặc cloud. Lệnh cuối: finish_validation.py, sau đó kiểm manifest009 và git diff --check. Bước tiếp giữ nguyên: chờ quyết định exact patch H2; H1 thiếu nguồn exporter/deployment, không coi là chỉ thiếu cloud.
