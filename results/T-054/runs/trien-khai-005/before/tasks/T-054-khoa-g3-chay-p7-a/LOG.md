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
