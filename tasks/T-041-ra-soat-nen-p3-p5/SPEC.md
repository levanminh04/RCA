# T-041 — Rà soát sâu nền P3/P5 và bàn giao đầu vào thiết kế RCA

- **Trạng thái:** đã hoàn thành phân tích và tự kiểm trong quyền Q-184 ngày 21/10/2026, chờ phản biện kết quả; chưa nghiệm thu. Gói tám file Q-182, Q-183 là lịch sử đồng bộ.
- **Ngày ghi SPEC:** 21/10/2026; lời duyệt gói lưu được giữ ngày 20/10/2026 theo Q-182.
- **Người làm:** Codex.
- **Người phản biện:** Claude. Lượt hiện tại chưa cấp quyền ghi REVIEW.
- **Thuộc gói MRP:** chuẩn bị P6, dùng lại bằng chứng P3–P5; **cổng:** trước G3, không đổi cổng.
- **Loại việc:** phân tích code, hợp đồng và trung gian đã lưu; chuẩn bị đầu vào thiết kế. Không phải cài hoặc đánh giá phương pháp P6 mới.
- **Hai phiên công việc:** phiên 1 là T-041 lưu kết quả; phiên 2 dùng đầu ra đó để thiết kế ứng viên ngoài task, chỉ trả lời trong chat khi Minh giao. Không đồng nhất một task với một lượt chat hoặc dự toán số giờ khi chưa đo.

## Nguồn duyệt và điều kiện bắt đầu

Minh duyệt nguyên lời ngày 20/10/2026:

> DUYỆT GÓI 8 FILE VÀ PHẠM VI TRÊN. TẠO SPEC T-041 VÀ CẬP NHẬT ĐẦY ĐỦ HAI PROMPT, GIỮ YÊU CẦU LÀM SÂU; PHIÊN 1 LƯU KẾT QUẢ VÀO REPO, PHIÊN 2 ĐỌC TRỰC TIẾP. CHƯA TRIỂN KHAI TASK.

Q-182 là quyền chuẩn bị ban đầu, chưa giao chạy task ở thời điểm đó. Minh chỉ đạo tiếp ngày 21/10/2026 (Q-183):

> LƯU HAI PROMPT MỚI VÀO LOG T-041, ĐỒNG BỘ SPEC, STATE VÀ DECISIONS VỚI QUYỀN TỰ RÀ, TỰ SỬA SPEC RỒI TRIỂN KHAI. PHIÊN NÀY CHỈ CẬP NHẬT TÀI LIỆU, CHƯA CHẠY TASK.

Quyền của lượt đồng bộ lịch sử Q-183: lượt đó chỉ đồng bộ SPEC, LOG, STATE, DECISIONS và lưu đầy đủ hai prompt mới, không chạy phân tích hoặc tạo bốn đầu ra results/T-041/. Phiên 1 khi được giao thực hiện bằng prompt hiện hành phải tự rà nguồn/SPEC, tự sửa lỗi trong đúng mục tiêu rà nền P3/P5 và gói tám file, ghi bằng chứng/thay đổi/tác động, kiểm lại rồi thực hiện; không cần duyệt lại từng sửa chữa thuộc quyền hoặc chờ Claude rà SPEC. Đây là ủy quyền riêng cho T-041, thay điều kiện chờ duyệt thực hiện và khóa SPEC cũ; không mở rộng mục tiêu, file, dữ liệu, chi phí hay quyền quyết định nghiên cứu. Giữ Q-182 và LOG cũ như lịch sử.

Codex vẫn là người làm; Claude vẫn là người phản biện chính thức. Tự rà không thay phản biện hoặc nghiệm thu của Minh. Phiên 2 tự rà cả đề bài/SPEC nguồn và tự sửa đề bài/phương án thiết kế trong chat; chưa có SPEC ghi riêng, không được sửa file nguồn hoặc lưu thiết kế vào repo.

Chỉ đạo thực hiện hiện hành Q-184 được nối nguyên văn trong LOG ngày 21/10/2026. Minh giao tự rà/sửa/kiểm lại SPEC rồi thực hiện ngay; không chờ duyệt lại từng sửa chữa trong quyền. Q-182/Q-183 giữ lịch sử. DECISIONS được nối đúng chỉ đạo này, không thêm lựa chọn khoa học.

Điều kiện bắt đầu phiên thực hiện:
1. Đọc AGENTS, STATE, SPEC, mục cuối LOG và nguồn quyết định hiện hành; kiểm quyền Q-184 và lời giao thực hiện. Không coi lượt cập nhật tài liệu này là task đã chạy hoặc prompt lịch sử là quyền hiện hành.
2. Tự rà độc lập theo mục tiêu gốc trước khi tin SPEC/LOG; ghi vấn đề → nguồn/bằng chứng → tác động → sửa hoặc giữ và lý do. Được tự sửa câu hỏi/phép phân xử còn thiếu trong mục tiêu, đường dẫn/revision, logic/hợp đồng, thứ tự phụ thuộc, phép kiểm nhỏ, tiêu chí và bàn giao. Nối LOG nêu cũ → mới, lý do/tác động; kiểm lại rồi triển khai. Không thu hẹp nghĩa vụ hoặc sửa nguồn có thẩm quyền cho khớp SPEC.
3. Nếu cần đổi mục tiêu/phạm vi/quyền hoặc các nguồn có thẩm quyền còn mâu thuẫn thực chất chưa được Q-184 giải quyết, dừng phần sửa và kết luận phụ thuộc, báo đúng nguồn/hệ quả và đề xuất; phần độc lập hợp lệ được tiếp tục. Không tự hợp thức hóa quyết định nghiên cứu.
4. Xác định đầu vào dev được phép từ allowlist/manifests và hồ sơ sở hữu. Không suy quyền đọc test từ đường dẫn xuất hiện trong báo cáo.
5. Đối chiếu đầu ra đã có và hash trước khi làm; dùng lại phần hợp lệ, không tự chạy lại công việc đã có.

## Mục tiêu

DT18-NV2 yêu cầu mô hình phụ thuộc có quan hệ gọi, thông điệp, dữ liệu và ánh xạ log/trace/metric phục vụ phát hiện, vùng và xếp hạng. DT18-NV3 yêu cầu nghiên cứu trên dữ liệu công khai trước khi áp dụng FlashTicket. Hướng dẫn cô yêu cầu hiểu sâu phương pháp và hạn chế trước khi thiết kế. MRP §0, §2, RQ2/RQ3/RQ5, P4–P7/P9 và WHY-01 yêu cầu phân biệt căn cứ sửa hạn chế, đáp ứng đề tài và nhu cầu kỹ thuật.

T-041 kiểm chính xác phần nào của P3/P5 có thể dùng lại, phần nào phải đổi hoặc bổ sung, và thông tin nào dữ liệu hiện có không cung cấp. Kết quả phải giúp phiên thiết kế biết code, hợp đồng, mức bằng chứng và phụ thuộc thật, thay vì đọc lại toàn bộ điều tra.

Task chỉ trả lời phần nền tảng và tính hợp lệ của việc dùng lại. Nó không chọn công thức, xác nhận hiệu quả RCA, hoàn thành M1/P6, nghiệm thu nguồn cũ hay đóng RQ2/RQ3/RQ5/G3.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi và nguồn | Các khả năng phải phân biệt | Phép kiểm/bằng chứng | Mức kết luận và phụ thuộc |
|---|---|---|---|
| P3/P5 dùng lại được tới đâu? MRP P5–P6, PLAN-P6 | Đã thỏa hợp đồng; chỉ giống tên; phải điều chỉnh; không đủ dữ liệu | File/hàm, kiểu vào–ra, đường gọi, fixture và trung gian đã lưu | Kết luận khả năng dùng lại theo điều kiện, không suy hiệu quả phương pháp |
| Bằng chứng nằm ở đâu, còn giữ thông tin gì? G2, A/E/G | Owner span; caller/callee; service/operation/resource; graph gộp mất thông tin request/thời gian | Đầu vào → biến đổi → trung gian → đầu ra; hợp đồng builder/adapter | Chỉ rõ tín hiệu còn/mất và nơi phải đọc lại; không suy kiểu cạnh hay cơ chế vật lý chưa xác minh |
| Nhóm quan trọng sai ở bước nào? MRP P4, G2-H01–H26 | Dữ liệu, giao thức, adapter/bản cài, giả định/cách tính; hiện tượng chung có cả ở ca đúng | Code và trung gian, ca sai và ca đúng điều kiện tương ứng, phản ví dụ | CT/ĐC/LĐ/MT/CK thuộc đúng phần đã kiểm; phần chưa phân xử ghi giải thích khác và bằng chứng thiếu |
| Cửa sổ/nền/nhãn/số học có đổi ý nghĩa phép so? B/C/F/G | Tương lai lọt vào; gộp khác đơn vị; thiếu nền; trạng thái lỗi/hòa bị đổi; schema liên hệ root | Selector/adapter/scorer/evaluator/runner, thời điểm khả dụng, bộ cột và nhánh dự phòng | Ghi yêu cầu tính đúng chung; không sửa baseline hoặc protocol đã khóa |
| Lõi offline và online chung được phần nào? DT18, WHY-08, P9 | Cùng ngữ nghĩa; chỉ cùng định dạng; thiếu kind/link/binding/clock | Hợp đồng T-035/T-036, bàn giao T-040, dữ liệu dev đã được phép | Giao diện tối thiểu và yêu cầu quan sát; không nhận Collector khôi phục dữ liệu chưa ghi |
| Phần chưa trả lời ảnh hưởng quyết định nào? MRP §3/P4/P6 | Chưa đọc nhưng có sẵn; file chưa tiếp cận; chưa từng ghi; cần phép chạy hoặc Minh quyết | Kiểm vị trí nguồn, nguồn quyền, thông tin tối thiểu và phép phân xử | Làm hết phần kiểm được trong quyền; phần khác trình phạm vi/chi phí/owner, không xóa nghĩa vụ nghiên cứu |

## Đầu vào

Root chuẩn: D:/RCA-flashticket. Các đường dẫn dưới đây tính từ root này.

- Luật/trạng thái: AGENTS.md; docs/STATE.md; SPEC và LOG task liên quan; docs/DECISIONS.md, LESSONS.md, WHY.md, review-prompt.md.
- Nguồn đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; advisor-2026-09-23.md.
- Phạm vi nghiên cứu: docs/MRP.md; docs/PLAN-P6.md (phần hiện hành, không lấy quyền lịch sử trong phụ lục); docs/DE-XUAT-HUONG-GRAFANA-RCA.md (vẫn là đề xuất).
- G2: results/T-034/goi-g2.md, ban-do-g2.json, bang-baseline.json, hai-phep-kiem.md/json và nguồn được chúng trực tiếp dẫn; manifest hiện hành theo LOG, hiện trỏ runs/manifest-cuoi-007/manifest.json.
- P5: results/T-035/dac-ta-do-thi.md, kiem-dung-dan.md; hợp đồng T-036 hiện hành tại results/T-036/runs/doi-chieu-smtp-001/hop-dong.md và manifest.json (pin SMTP V2), artifact-manifest.json cho phần tiếp nhận; đối chiếu code snapshot với src/do_thi_tinh/. Root hop-dong.md/manifest.json là lịch sử R1; results/T-040/ban-giao-p6.md, yeu-cau-quan-sat-p9.md, con-mo.json và manifest.json.
- Code: src/p3/, src/do_thi/, src/do_thi_tinh/; code nguồn phương pháp, fixture, trung gian được các module và hồ sơ dẫn trực tiếp.
- Nguồn P3/P4: SPEC/LOG và đầu ra liên quan của T-022, T-024, T-025, T-026, T-028–T-034; chỉ mở đúng phần cần lần chuỗi. Nếu dùng đầu ra T-032 về H6/H8/CIRCA/KT-11, đọc đính chính hiện hành được STATE/LOG chỉ tới.
- Thẻ dataset/hồ sơ phương pháp trong results/ và docs/knowledge/ theo phụ thuộc thực tế. Không đọc repo RCA lưu trữ, kể cả khi link trong tài liệu cũ trỏ tới đó.
- Chỉ dữ liệu/trung gian dev đã được cho phép, có nguồn và miền đọc xác minh được. Không mở data/locked/, test nằm nơi khác hoặc nội dung giữ ngoài. Không copy dữ liệu thô sang đầu ra task.

Trước khi dùng đầu ra cũ, kiểm hash theo manifest phù hợp. Lệch hash thì ghi bằng chứng vào bang-chung.jsonl/LOG trong quyền, dừng kết luận phụ thuộc và báo Minh; không tự hợp thức hóa bằng manifest mới. Phân biệt trạng thái lịch sử trong snapshot với quyết định nghiệm thu hiện hành.

## Đầu ra

Bốn đầu ra được tạo trong phiên thực hiện hiện hành theo Q-184, sau bước tự rà/sửa/kiểm lại SPEC; lượt đồng bộ lịch sử Q-183 không tạo các đầu ra này:

1. results/T-041/bao-cao.md:
   - bản đồ đường xử lý và ranh giới thông tin;
   - bảng dùng lại code tới file/hàm, hợp đồng, điều kiện và bằng chứng;
   - bao phủ đủ G2-H01–H26, bảy nhóm A–G và yêu cầu đề tài;
   - chuỗi đầu vào → xử lý → trung gian → đầu ra, ca đúng/sai và giải thích khác;
   - hợp đồng dữ liệu/giao diện tối thiểu, vấn đề ảnh hưởng thiết kế và phần cần bổ sung;
   - tách FACT, USER_CONFIRMED, CANDIDATE, DECIDED, OPEN. Lựa chọn phương pháp vẫn là ứng viên; không ghi quyết định kỹ thuật mới thay WHY.

2. results/T-041/bang-chung.jsonl:
   - ghi nối tiếp từng phép đọc/kiểm quan trọng, lệnh hoặc phép tính đủ tái hiện, đầu vào, kết quả, lỗi và thời điểm; giữ lượt hỏng;
   - mỗi bản ghi có ID ổn định để báo cáo/bàn giao trỏ tới; trỏ file/hàm/dòng và JSON pointer khi thích hợp;
   - kết quả nhỏ có thể giữ trực tiếp; phần lớn trỏ nguồn/hash thay vì chép dữ liệu thô;
   - không dùng nhật ký này thay cho lập luận và phân tích cơ chế trong báo cáo.

3. results/T-041/ban-giao-phien-2.md:
   - điểm bắt đầu tự đủ: mục tiêu, trạng thái, thứ tự đọc và liên kết tới báo cáo/bằng chứng;
   - hợp đồng dùng lại đã xác minh, phần chưa kiểm, giả định, quyết định còn chờ và bước tiếp cụ thể;
   - nêu phần dùng chung và khác biệt giữa yêu cầu phát hiện hiện hành với đề xuất Grafana;
   - phiên 2 kiểm nguồn rồi thiết kế, không cần lịch sử chat hoặc dựng lại toàn bộ điều tra;
   - không chép lại toàn bộ báo cáo, không coi chưa phản biện/nghiệm thu là đã duyệt.

4. results/T-041/manifest.json:
   - mô tả revision và file code/nguồn thực sự dùng, dấu vết thay đổi cục bộ nếu có; hash nguồn cùng manifest phù hợp và kết quả kiểm;
   - hash bao-cao.md, bang-chung.jsonl, ban-giao-phien-2.md và SPEC được dùng; không tự băm manifest;
   - liên kết rõ tới LOG nhưng không cam kết hash LOG đang nối thêm hoặc STATE/DECISIONS có thể đổi bởi phiên được duyệt khác;
   - khai trạng thái hoàn thiện/phản biện/nghiệm thu đúng thực tế. Mỗi lần cập nhật kết luận phải cập nhật manifest cuối, giữ lịch sử kiểm trong bằng chứng/LOG.

## Phạm vi ghi

Gói Minh duyệt có đúng tám file, với quyền theo giai đoạn:

| File | Lượt đồng bộ tài liệu theo Q-183 | Phiên thực hiện theo Q-184 |
|---|---|---|
| tasks/T-041-ra-soat-nen-p3-p5/SPEC.md | Đồng bộ quyền và hai giai đoạn, giữ mục tiêu/phạm vi khoa học | Được tự sửa lỗi trong đúng mục tiêu/gói tám file; ghi bằng chứng, cũ → mới và tác động vào LOG, kiểm lại trước khi dùng |
| tasks/T-041-ra-soat-nen-p3-p5/LOG.md | Chỉ nối thêm quyền mới, đầy đủ hai prompt hiện hành và bàn giao; giữ prompt cũ | Chỉ nối thêm; ghi tự rà/sửa SPEC, bước con và checkpoint |
| results/T-041/bao-cao.md | Chưa tạo | Ghi/hoàn thiện báo cáo trong đúng mục tiêu task |
| results/T-041/bang-chung.jsonl | Chưa tạo | Chỉ ghi nối tiếp, giữ lỗi và lần thử |
| results/T-041/ban-giao-phien-2.md | Chưa tạo | Ghi/hoàn thiện gói bàn giao có dẫn nguồn |
| results/T-041/manifest.json | Chưa tạo | Ghi/cập nhật manifest đầu ra và nguồn dùng |
| docs/DECISIONS.md | Lịch sử: chỉ nối Q-183 đúng lời giao, giữ Q-182 | Nối Q-184 đúng chỉ đạo thực hiện mới; không thêm quyết định nghiên cứu |
| docs/STATE.md | Chỉ đồng bộ thông tin T-041: đã có quyền thực hiện sau tự rà, hiện chưa chạy | Chỉ cập nhật thông tin/dòng T-041 trong quyền task; không tự nghiệm thu/đóng task/cổng |

Không có quyền ghi mọi file khác trong results/T-041/, không tạo scripts/, runs/, cache hay file tạm ngoài danh sách. Phép kiểm nhỏ thực hiện bằng lệnh inline/bộ nhớ; ghi lệnh và kết quả vào bang-chung.jsonl. Nếu thực sự cần file khác, trình đường dẫn, nội dung và tác động trước.

Code dùng chung, dữ liệu, baseline, SPEC/kết quả task cũ, AGENTS, MRP, PLAN-P6, WHY, LESSONS và mẫu review chỉ đọc. Claude chưa được cấp quyền tạo REVIEW; lượt rà SPEC hiện tại chỉ trả lời chat.

Phiên thiết kế tiếp theo không thuộc quyền ghi T-041: đọc gói lưu, tự rà đề bài/SPEC nguồn/giả định và tự sửa đề bài/phương án đang xây trong chat khi Minh giao; không sửa file T-041, ghi kết quả thiết kế vào repo hoặc tự tạo task mới. Lỗi nguồn phát hiện ở phiên 2 phải có đính chính/bằng chứng/tác động trong chat; sửa file cần quyền riêng.

## Các bước

0. **Tự rà, sửa SPEC và kiểm lại trước khi thực hiện** — kiểm quyền Q-184/lời giao, ghi mở phiên LOG; đọc mục tiêu nguồn và tự rà độc lập, không tin tuyệt đối SPEC hoặc kết luận cũ. Lỗi trong quyền thì tự sửa SPEC, ghi bằng chứng/cũ → mới/tác động, kiểm lại rồi thực hiện ngay, không dừng ở đề xuất chờ duyệt lại. Kiểm đầu ra có sẵn và miền dev; mâu thuẫn nguồn thực chất còn ngoài quyền hoặc hash lệch thì dừng phần phụ thuộc.
1. **Dựng đường xử lý** — đọc code và hợp đồng: nguồn → selector/adapter → cửa sổ/nền → span/log/metric → graph/đặc trưng → điểm → tập ứng viên → thứ hạng → evaluator. Tách dataset, chế độ, code chung/riêng, nhãn/phương pháp, graph tĩnh/quan sát/cây span. Ghi nguồn và bảng đầu tiên ngay.
2. **Kiểm hợp đồng và khả năng dùng lại** — đọc tới hàm và đường gọi thật. Kiểm thời gian/đơn vị/biên, missing/fill/nền/cadence, alias/scope, parent/link/kind, gộp log, tập ứng viên, số học/hòa/lỗi/fallback, cache/revision. Đối chiếu fixture và kết quả đã lưu; làm phép tính nhỏ có ý nghĩa nếu an toàn và cần thiết.
3. **Lần cơ chế nhóm quan trọng** — trên code/trung gian đã lưu, chọn ca sai và ca đúng có điều kiện tương ứng, ghi tiêu chí chọn; mở rộng khi có phản ví dụ hoặc giải thích cạnh tranh. Không dừng ở cờ hay số tổng. Số dùng phải trỏ nguồn, JSON pointer hoặc lệnh+kết quả.
4. **Kiểm ranh giới cho P6** — chỉ rõ graph gộp mất gì, phải đọc span gốc gì, phép nào cần kiểu quan hệ đã xác minh, phép nào chỉ dùng quan hệ span quan sát, nối service/operation/resource và nhãn ra sao, offline/online dùng chung tới đâu.
5. **Hợp nhất đủ nguồn** — đối chiếu G2-H01–H26, A–G, UV và DT18/MRP/P5. Đánh dấu dùng nguyên/cần đổi/bổ sung/không dùng/còn mở với lý do và quyết định bị ảnh hưởng. Không thêm thuật toán chỉ để đủ nhóm.
6. **Tự kiểm và bàn giao** — đối chiếu lại kết luận với nguồn phản bác, kiểm liên kết/JSONL/hash/phạm vi diff; hoàn thành báo cáo, bàn giao và manifest. Nối LOG đủ bốn mục, bước tiếp, lệnh cuối; cập nhật dòng task thành chờ phản biện, chưa nghiệm thu. Soạn prompt trung tính theo mẫu, không tự gửi.

Bổ sung tự rà 21/10/2026 theo Q-184: kiểm riêng event time (thời gian sự kiện), end time và arrival/available time (thời điểm đã nhận/có thể dùng); thiếu arrival thì không chứng nhận online causal chỉ từ end<cutoff. Kiểm thông tin mất khi gộp graph, witness và chính sách hàng lặp so với bảng span baseline; không thay bảng baseline bằng graph đã gộp. Đọc trạng thái nghiệm thu nguồn theo DECISIONS hiện hành, không sửa snapshot lịch sử. OPEN phải phân loại chưa kiểm/có nguồn chưa tiếp cận/chưa từng ghi/cần thực nghiệm/cần Minh quyết, cùng bằng chứng thiếu, phép phân xử, owner, phạm vi và chi phí đã biết/chưa đo.

Bước 2 dùng đường xử lý đã dựng ở bước 1; các nhánh code không phụ thuộc được đọc cùng đợt để giảm lặp. Bước 3/4 triển khai khi đầu vào tương ứng rõ, không đợi mọi module được đọc xong. Sau mỗi bước con lưu phát hiện/bằng chứng và nối LOG, tránh dồn toàn bộ cuối phiên.

## Kiểm đúng đắn

- **Tính nguồn:** hash theo manifest trước dùng; xác nhận revision/bản cài và miền dữ liệu.
- **Tính hợp đồng:** trỏ file/hàm, dữ liệu vào–ra thật, fixture và phản ví dụ; tên module hoặc chạy không lỗi chưa đủ.
- **Tính cơ chế:** đúng điều kiện X, bước Y, thông tin Z, chuỗi vào → xử lý → trung gian → ra; đối chiếu ca đúng/sai; không quy tính chất chung thành nguyên nhân riêng.
- **Tính phân biệt:** xem phần có thể bác nhận định; tách tác dụng nhãn, số mẫu, scope, cửa sổ, thang, tín hiệu và cấu trúc.
- **Tính thời gian/nhãn:** kiểm đường nhãn tới phương pháp, tương lai trong chuẩn hóa/chọn cột/ngưỡng; phân biệt biết mốc với tự phát hiện.
- **Tính phủ:** mọi G2-H01–H26 có hàng và mọi nghĩa vụ nguồn được nêu nơi nhận hoặc giới hạn; các nhóm chồng nhau không cộng thành tỷ lệ.
- **Tính bàn giao:** báo cáo có hợp đồng/nguồn/bằng chứng; bàn giao chỉ đúng file; JSONL parse được; manifest không tự băm và không nhầm LOG đang nối thêm; trạng thái chưa nghiệm thu giữ rõ.
- **Tính phạm vi:** kiểm diff cuối và file set; nguồn/code/task cũ không đổi; sửa SPEC có đúng quyền Q-184, căn cứ và dấu vết trong LOG; giữ mọi lượt hỏng trong nhật ký kiểm.

Chỉ được chạy lệnh chỉ đọc, kiểm hash, và phép tính nhỏ trong bộ nhớ đã xét tác dụng phụ. Python dùng -B; không tự gọi bộ test/runner tạo kết quả, cache hoặc nhập module có tác dụng phụ. Không chạy lại ma trận baseline, thay cấu hình phương pháp hay thử ứng viên mới trên dữ liệu thật. Nếu cần tái lập bổ sung để sử dụng một số hoặc chọn baseline, trình đúng việc còn thiếu, không bỏ yêu cầu ấy hoặc chạy vượt quyền.

## Tiêu chí xong

1. Dùng lại được tới đâu được chứng minh theo hợp đồng và hàm thật, không chỉ có danh sách file.
2. Nhóm quan trọng có chuỗi bằng chứng và ca đối chiếu; phần chưa xác định bước gây sai có đúng bằng chứng thiếu và giải thích cạnh tranh.
3. Đủ G2-H01–H26, A–G và yêu cầu nguồn, giữ cả bằng chứng bất lợi; không coi R1–R4 là toàn bộ G2.
4. Phần còn có thể đọc/kiểm hợp lý trong quyền đã làm; không để “phiên sau đọc code/trung gian đang có” chỉ vì dừng ở mô tả.
5. Mọi OPEN phân biệt chưa kiểm, file chưa tiếp cận, thiếu đầu vào, giới hạn dữ liệu hoặc cần Minh quyết; có phép phân xử, phạm vi/chi phí đã biết hoặc chưa đo, owner và quyết định phụ thuộc.
6. Gói bàn giao đủ để phiên thiết kế đọc repo mà không copy chat; kiểm hash và biết nguồn nào vẫn có điều kiện, chưa phản biện/nghiệm thu.
7. Diff đúng phạm vi, LOG đủ và manifest hợp lệ; không sửa nguồn nền hoặc tạo kết quả ngoài quyền.

Đạt các tiêu chí này chỉ hoàn thành phần rà nền và bàn giao. Không xác nhận cơ chế chưa kiểm bằng can thiệp phù hợp, không chọn thuật toán/cuối cấu hình, không đóng câu hỏi nghiên cứu/cổng. Nghiệm thu thuộc Minh.

## Không làm

- Không cài, chạy ma trận hoặc đánh giá hiệu quả phương pháp P6; không chạy thử Grafana S1–S4.
- Không soạn/duyệt SPEC M1 thay task này, không thay MRP/PLAN-P6/WHY-02; giữ hướng Grafana là đề xuất.
- Không mở test/giữ ngoài, SSH/bật EC2, tải dữ liệu, cài môi trường, sửa FlashTicket hoặc ghi hệ thống ngoài.
- Không sửa baseline, ghi lại kết quả/task cũ, mở lại task đã đóng hoặc tự thêm cổng/quy trình.
- Không tự tạo phiên/subagent hoặc gửi prompt sang agent khác; Minh chuyển thủ công.
- Không chạy deep research hay lượt lệnh hơn một giờ. Tra hẹp bài/code chính thức chỉ khi câu kết luận phụ thuộc, không mở khảo sát rộng.
- Không commit/push nếu chưa có lời duyệt riêng.

Giới hạn quyền không xóa nghĩa vụ nghiên cứu: thiếu trung gian/kiểm cần thiết phải trình đúng bằng chứng, việc bổ sung và quyết định phụ thuộc. Các nguồn/quan hệ chưa có trong dữ liệu hiện có không bị tự loại khỏi mục tiêu đề tài.

## Chi phí ước lượng

- Không dự toán số giờ agent/phiên khi chưa đo. Các phép kiểm dự kiến chỉ đọc hoặc tính nhỏ trong bộ nhớ, không huấn luyện, chạy lại baseline hay thực nghiệm mới. Đọc/kiểm hash trung gian lớn đã có có thể tốn I/O và thời gian; ghi thời gian thực tế, không hứa nhẹ/nhanh khi chưa đo.
- Không tải dữ liệu hoặc phát sinh chi phí EC2. Chỉ lưu văn bản, bằng chứng nhỏ và manifest; dung lượng thực tế chưa đo, không sao chép dataset.
- Không giảm phần khoa học để vừa một lượt chat. Tổ chức theo phụ thuộc và checkpoint trong LOG/báo cáo được phép; áp dụng đính chính Q-178.
- Khi thấy cần thao tác tốn kém hoặc vượt quyền, trình dự toán và dừng phần phụ thuộc; tiếp tục phần độc lập hợp lệ.

## Rủi ro và điều chưa chắc

- Code/bằng chứng cũ có thể lệch manifest hoặc thiếu trên máy này. Không suy là không tồn tại; nêu nơi được dẫn và phần cần tiếp cận.
- Không có kiểu span, mapping, onset hoặc nền sạch có thể giới hạn kết luận; thêm Collector không tự giải quyết.
- Các giả thuyết về phân bổ bằng chứng, thời gian tự xử lý, log và lan truyền vẫn chưa kiểm hiệu quả. Duyệt thử hoặc có code không biến chúng thành sự thật.
- Phát hiện có đồ thị trong MRP khác đề xuất thu hẹp dùng luật cảnh báo. Task chỉ làm rõ hợp đồng/phần dùng chung và câu cần quyết, không tự chọn hướng.
- Không thể bảo đảm mọi câu hỏi nghiên cứu hết OPEN bằng đọc code. Bảo đảm yêu cầu là làm hết phần kiểm được và trình phần thiếu đủ cụ thể để Minh quyết.

## Prompt bàn giao

LOG.md của task giữ nguyên các prompt cũ như lịch sử, nối đầy đủ bản hiện hành theo Q-183:
- “Prompt 1 hiện hành — Tự rà, tự sửa SPEC rồi thực hiện T-041”: phiên nhận prompt tự rà/sửa/kiểm lại SPEC trong quyền rồi thực hiện, lưu bốn đầu ra và nhật ký/trạng thái đúng phạm vi.
- “Prompt 2 hiện hành — Tự rà rồi thiết kế RCA trong chat”: đọc trực tiếp gói T-041, tự rà nguồn và tự sửa đề bài/phương án trong chat; không cần copy báo cáo và không được ghi repo.
- “Prompt Claude soát SPEC sau đồng bộ”: chép nguyên văn Prompt chung + Khối soát SPEC + Khối G3 hiện hành trong docs/review-prompt.md; chỉ điền trường trung tính, quyền trả lời chat. Minh chọn chuyển; việc này không là điều kiện chờ để phiên 1 thực hiện theo Q-183.

Sau khi thực hiện, Codex nối prompt phản biện kết quả trong LOG theo đúng mẫu hiện hành. Hai prompt công việc không thay prompt phản biện; không tự chuyển/gửi, không tự cấp quyền ghi REVIEW.
