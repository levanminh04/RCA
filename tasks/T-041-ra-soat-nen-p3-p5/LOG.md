# Nhật ký T-041 — Rà soát sâu nền P3/P5

Chỉ người làm ghi, chỉ nối thêm. Người làm: Codex. Người phản biện: Claude.

## Phiên 1 — 21/10/2026 — Codex — Windows, D:/RCA-flashticket — người làm, chuẩn bị SPEC

**Mở phiên:** đã đọc AGENTS, STATE, mẫu SPEC/LOG, mục tiêu MRP/DT18/hướng dẫn cô, các lý do/quyết định liên quan, LESSONS, kế hoạch P6 và đề xuất Grafana. Mã task và bốn đầu ra chưa tồn tại tại lần kiểm trước ghi. Không có kết quả phân tích T-041 để tiếp nhận.

**Công đoạn và quyền:** tạo SPEC chờ duyệt thực hiện và lưu đầy đủ hai prompt sau khi Minh duyệt gói tám file. Đây là chuẩn bị đặc tả/bàn giao, không phải thực hiện phân tích code và trung gian của T-041. Bốn file kết quả trong results/T-041/ chưa được tạo.

**Quyết định của Minh trong phiên** (lời duyệt nhận ngày 20/10/2026, đã nối DECISIONS Q-182 trước khi cập nhật dẫn xuất):

> DUYỆT GÓI 8 FILE VÀ PHẠM VI TRÊN. TẠO SPEC T-041 VÀ CẬP NHẬT ĐẦY ĐỦ HAI PROMPT, GIỮ YÊU CẦU LÀM SÂU; PHIÊN 1 LƯU KẾT QUẢ VÀO REPO, PHIÊN 2 ĐỌC TRỰC TIẾP. CHƯA TRIỂN KHAI TASK.

Ngày ghi tài liệu đã sang 21/10/2026; giữ nguyên ngày và nội dung lời duyệt nguồn, không suy lời duyệt thực hiện.

**Diễn biến:**
- Xác nhận T-041 và Q-182 chưa dùng; ghi nhận trạng thái trước sửa và hash các file bảo vệ trong bộ nhớ để tự kiểm phạm vi.
- Nối Q-182, giữ nguyên byte phần trước của DECISIONS.
- Soạn SPEC theo mẫu với mục tiêu nguồn, câu hỏi phân xử, đầu vào, đầu ra, tám file và quyền theo giai đoạn, bước, kiểm đúng đắn, tiêu chí xong, chi phí chưa đo và rủi ro.
- Giữ Codex làm/Claude phản biện; quyền rà SPEC chỉ trả lời chat, chưa có quyền ghi REVIEW.
- Lưu toàn văn Prompt 1 và Prompt 2 dưới đây để agent khác đọc mà không cần lịch sử chat. Prompt 1 chỉ được thực hiện sau duyệt SPEC; Prompt 2 đọc trực tiếp gói lưu và tiếp tục trong chat.
- Soạn prompt Claude rà SPEC nguyên mẫu hiện hành; chưa tự gửi.
- Chỉ cập nhật thông tin T-041 trong STATE, giữ các quyết định/cổng và hướng Grafana đang chờ. Kết quả tự kiểm cuối phiên được nối ở cuối LOG sau các khối prompt.

**Tự soát đặc tả trước phản biện:**
- Không cho phép gói lưu trở thành quyền chạy: SPEC và Prompt 1 có điều kiện bắt đầu rõ.
- Không cấp quyền cho mọi file trong results/T-041/: chỉ đúng bốn file, LOG và dòng STATE khi được thực hiện; SPEC/DECISIONS sửa tiếp cần quyền riêng.
- Tách kiểm nền và thiết kế ứng viên; phiên 2 không ghi kết quả thiết kế vào T-041, không tự nhận là phản biện của task mình.
- Đầu ra phải có chuỗi bằng chứng, ca đúng/sai, phản ví dụ và đủ G2-H01–H26; OPEN phải có phần bằng chứng thiếu và quyết định phụ thuộc.
- Không coi graph P5, R1–R4, bảy nhóm A–G hoặc việc nghiệm thu là bằng chứng phương pháp hiệu quả.
- Manifest không tự băm hoặc khóa LOG/STATE/DECISIONS đang tiếp tục đổi; kiểm đầu ra và nguồn dùng, không đòi copy chat.
- Phần nguồn hiện hành khác đề xuất phát hiện được giữ như quyết định còn chờ, không tự sửa MRP/WHY.
- Chưa có bản phản biện chính thức để đáp hoặc kết quả task để nghiệm thu.

## Prompt 1 — Thực hiện T-041 sau khi SPEC được duyệt

Toàn văn cập nhật; không dùng riêng khối này làm bằng chứng Minh đã duyệt thực hiện.

```text
Bạn là Codex, người làm T-041 trong repo D:/RCA-flashticket. Claude là người phản biện chính thức.

MỤC TIÊU VÀ ĐIỀU KIỆN THỰC HIỆN

Thực hiện phân tích kỹ thuật sâu nền P3/P5 để chuẩn bị thiết kế RCA: kiểm chính xác phần dùng lại được, phần cần điều chỉnh và bằng chứng còn thiếu. Phải làm tới báo cáo và gói bàn giao tự đủ trong repo; không dừng ở danh sách việc cần làm.

Trạng thái khi soạn prompt: Minh đã duyệt tạo SPEC và gói 8 file, nhưng CHƯA DUYỆT TRIỂN KHAI T-041. Prompt này không phải lời duyệt thực hiện. Trước tiên đọc:
- D:/RCA-flashticket/AGENTS.md
- D:/RCA-flashticket/docs/STATE.md
- D:/RCA-flashticket/tasks/T-041-ra-soat-nen-p3-p5/SPEC.md
- mục cuối D:/RCA-flashticket/tasks/T-041-ra-soat-nen-p3-p5/LOG.md
- quyết định hiện hành trong D:/RCA-flashticket/docs/DECISIONS.md.

Chỉ thực hiện khi có bằng chứng Minh đã duyệt đúng SPEC để thực hiện. Nếu chưa có, báo đúng điểm chờ và dừng phần thực hiện; không tạo bốn file kết quả, không suy lời duyệt gói lưu là duyệt chạy. Nếu đã được giao thực hiện sau duyệt, ghi nguyên lời duyệt và mở phiên vào LOG, rồi làm tiếp tới đầu ra.

PHẠM VI GHI SAU DUYỆT THỰC HIỆN

Chỉ được ghi:
1. D:/RCA-flashticket/results/T-041/bao-cao.md
2. D:/RCA-flashticket/results/T-041/bang-chung.jsonl
3. D:/RCA-flashticket/results/T-041/ban-giao-phien-2.md
4. D:/RCA-flashticket/results/T-041/manifest.json
5. Nối thêm D:/RCA-flashticket/tasks/T-041-ra-soat-nen-p3-p5/LOG.md.
6. Cập nhật đúng dòng T-041 trong D:/RCA-flashticket/docs/STATE.md theo quyền SPEC.

SPEC đã duyệt thì khóa. DECISIONS không được nối quyết định mới mặc định; trình Minh trước. Không ghi file khác, kể cả scripts/, runs/, file tạm/cache, code chung, dữ liệu và đầu ra task cũ. Cần thêm file thì trình đường dẫn, nội dung, lý do và ảnh hưởng. Không tự tạo REVIEW.

Được tìm kiếm/đọc, kiểm hash và phép tính nhỏ trong bộ nhớ; ghi lệnh/kết quả vào bang-chung.jsonl. Trước khi gọi code phải kiểm tác dụng phụ, Python dùng -B. Không tự chạy bộ test/runner có thể ghi file ngoài quyền.

Không mở test/giữ ngoài hoặc repo RCA lưu trữ D:/Project/flash-ticket-rca-research. Không chạy ma trận baseline hay thực nghiệm ứng viên mới, SSH/bật EC2, tải dữ liệu, cài môi trường, triển khai Grafana, deep research, commit/push, tự mở phiên/subagent hoặc gửi prompt sang agent khác. Đọc nguồn hẹp chính thức khi kết luận phụ thuộc; không mở khảo sát rộng.

NGUỒN PHẢI ĐỌC VÀ XÁC MINH

- D:/RCA-flashticket/docs/reference/sources/DT18-de-tai-va-nhiem-vu.md
- D:/RCA-flashticket/docs/reference/sources/advisor-2026-09-23.md
- D:/RCA-flashticket/docs/MRP.md: mục tiêu, RQ2/RQ3/RQ5, phần P4–P7/P9 trực tiếp chi phối.
- D:/RCA-flashticket/docs/WHY.md, LESSONS.md, PLAN-P6.md và DE-XUAT-HUONG-GRAFANA-RCA.md: đọc phần liên quan trực tiếp. Kế hoạch và đề xuất không thay nguồn quyết định.
- D:/RCA-flashticket/results/T-034/goi-g2.md, ban-do-g2.json và nguồn trực tiếp được dẫn. Xác định manifest hiện hành từ LOG.
- D:/RCA-flashticket/results/T-035/dac-ta-do-thi.md, hợp đồng T-036 hiện hành theo LOG/manifests.
- D:/RCA-flashticket/results/T-040/ban-giao-p6.md, yeu-cau-quan-sat-p9.md, con-mo.json và manifest.json.
- D:/RCA-flashticket/src/p3/, src/do_thi/, src/do_thi_tinh/; code nguồn phương pháp, fixture và trung gian trực tiếp được chúng dẫn tới.
Các tên file được liệt kê cùng một thư mục phải được hiểu ở đúng thư mục tuyệt đối đứng trước; không lấy bản cùng tên ở nơi khác.

Đọc SPEC và mục cuối LOG task nguồn khi cần xác định hợp đồng/phiên bản; dữ liệu dev chỉ đọc sau khi kiểm miền được phép từ nguồn/allowlist. Trước dùng kết quả cũ, kiểm hash theo manifest phù hợp; lệch thì ghi và dừng phần phụ thuộc, không tự tạo manifest mới để hợp thức hóa. Phân biệt snapshot lịch sử với quyết định hiện hành. Nếu dùng T-032 về H6/H8/CIRCA/KT-11, đọc đính chính được STATE/LOG chỉ tới.

BẢY NHÓM PHẢI BAO PHỦ

A. Vị trí ghi bằng chứng và cấp độ xác định bất thường.
B. Tín hiệu bị bỏ qua hoặc biểu diễn chưa phù hợp.
C. Nền, thang đo và cách cộng bằng chứng.
D. Thành phần dùng quan hệ có thể không đóng góp hoặc làm hại.
E. Tập ứng viên, thiếu bằng chứng và thao tác thiếu nền.
F. Mốc phân tích, tính nhân quả theo thời gian và chuỗi phát hiện.
G. Quan hệ ngoài lời gọi, ánh xạ hạ tầng và schema.

Đó là cách nhóm đối chiếu, chưa là cơ chế được chọn. Kiểm đủ G2-H01–H26 và yêu cầu đề tài. Không biến R1–R4 hoặc A–G thành toàn bộ G2; không ép một cơ chế để đóng bảng.

CÁCH LÀM SÂU

1. Dựng đường dữ liệu và đường gọi thật

Nguồn → selector/adapter → cửa sổ/nền → trace/log/metric → graph/đặc trưng → điểm → tập ứng viên → thứ hạng → evaluator.

Với mỗi bước, chỉ file/hàm/lớp, kiểu vào–ra và trung gian. Tách RE2-TT/Nezha, biết mốc/tự phát hiện, code chung/adapter/logic riêng, nhãn/evaluator/phương pháp, graph tĩnh/quan sát/cây span.

2. Kiểm dùng lại tới hợp đồng thật

Đọc và đối chiếu:
- timestamp, đơn vị, biên cửa sổ, span kết thúc và thời điểm dữ liệu khả dụng;
- chọn cột, missing/fill, nền hằng/thưa, cadence và hàng lặp;
- alias và service/operation/resource scope;
- parent/link, thiếu cha, trùng span, chồng lấn, kind và quan hệ chưa phân kiểu;
- log: khóa nối, trường động, mẫu log, đếm trùng;
- tập mô hình/quan sát/chấm/trả về;
- số không hữu hạn, cực trị, hòa, ERROR/UNSUPPORTED, fallback;
- runner/cache/revision và điều kiện dùng lại kết quả.

Không kết luận dùng lại chỉ vì module đã có. Nêu phần hợp đồng đã thỏa, phần chưa thỏa với nhu cầu P6. Kiểm fixture/trung gian hiện có; phép kiểm nhỏ phải có câu hỏi và kết quả phân biệt được.

3. Lần chuỗi bằng chứng, kiểm cả phản ví dụ

Với nhóm quan trọng, chọn ca sai và ca đúng có điều kiện tương ứng, giải thích cách chọn. Mở rộng đọc khi phát hiện giải thích cạnh tranh hoặc phản ví dụ.

Mỗi nhận định quan trọng phải có:
đầu vào cụ thể → dòng/hàm xử lý → giá trị/trạng thái trung gian → đầu ra.

Kết luận cơ chế phải chỉ điều kiện X, bước Y và thông tin Z bị mất/chấm sai. Nếu chỉ có liên hệ hoặc vị trí tín hiệu, giữ đúng mức đó. Không dùng kết quả cuối khớp, tên thuật toán, cờ cơ chế hoặc đặc tính chung làm bằng chứng thay chuỗi trên. Kiểm fallback có thực sự quyết định đầu ra không.

4. Làm rõ ranh giới cho thiết kế mới

Trả lời:
- Graph gộp P5 đã giữ/mất thông tin request/thời gian gì?
- Phân bổ owner–caller–callee cần span gốc hay trung gian hiện có đã đủ?
- Phép nào chỉ cần quan hệ span quan sát; phép nào đòi kind/CLIENT–SERVER/messaging đã xác minh?
- Cùng lõi offline/online được tới đâu về ngữ nghĩa, không chỉ định dạng?
- Đầu ra thao tác gộp/chấm ở service thế nào khi nhãn chỉ có service?
- Thiếu tín hiệu/cạnh/nền được biểu diễn ra sao mà không bịa bằng chứng?
- Thông tin nào Collector chuyển được; thông tin nào instrumentation/giao thức thực nghiệm phải ghi từ đầu?

Khi kết luận phụ thuộc bản cài khác bài gốc, đọc code/bài chính thức ở revision liên quan. Không biến lỗi adapter/thư viện thành khoảng trống chung của phương pháp.

LƯU KẾT QUẢ NGAY TRONG QUÁ TRÌNH

- Sau bước con: ghi bằng chứng và lỗi vào bang-chung.jsonl; cập nhật báo cáo theo phần đã làm; nối LOG. Không dồn mọi thứ vào cuối rồi mất tiến độ.
- bang-chung.jsonl: ID, thời điểm, câu hỏi, lệnh/phép tính, đầu vào/nguồn/JSON pointer, kết quả, lỗi và giới hạn; giữ mọi lần thử.
- bao-cao.md: bản đồ xử lý; ma trận dùng lại tới hàm; đủ G2-H01–H26; chuỗi cơ chế và phản ví dụ; hợp đồng tối thiểu; danh sách ảnh hưởng thiết kế và phần cần bổ sung.
- ban-giao-phien-2.md: trạng thái thật, thứ tự đọc, hợp đồng đã xác minh, kết luận có điều kiện, phần còn thiếu, quyết định phụ thuộc và bước tiếp. Trỏ bằng chứng, không chép toàn báo cáo. Agent khác không cần lịch sử chat.
- manifest.json: revision/dấu vết nguồn thực sự dùng và kiểm hash, hash ba file kết quả và SPEC; không tự băm manifest; LOG/STATE/DECISIONS đang đổi không được coi là hash đầu ra bất biến. Cập nhật manifest cuối sau khi hoàn thiện các đầu ra.

TIÊU CHÍ HOÀN THÀNH

- Mỗi phần được đề nghị dùng lại đã kiểm tới hàm/hợp đồng và nguồn thật.
- Nhóm quan trọng có chuỗi và ca đối chiếu; thiếu cơ chế có đúng bằng chứng cần thêm.
- Đủ G2-H01–H26, A–G và yêu cầu đề tài, gồm cả bằng chứng bất lợi.
- Phần còn đọc/kiểm hợp lý trong quyền đã làm; không để “phiên sau đọc code/trung gian đang có” chỉ vì dừng ở mô tả.
- Mọi OPEN tách rõ chưa kiểm, file chưa tiếp cận, thiếu đầu vào, giới hạn dữ liệu hoặc cần Minh quyết; có phép phân xử, phạm vi, chi phí đã biết/chưa đo và quyết định bị ảnh hưởng.
- Gói lưu đủ để phiên 2 đọc trực tiếp; liên kết, JSONL, manifest và phạm vi diff được tự kiểm.
- Không nhận là đã chọn phương pháp, xác nhận hiệu quả, hoàn thành P6 hay đóng RQ/cổng.

Nếu thiếu phép chạy ngoài quyền, hoàn thành phần độc lập và trình chính xác phần bổ sung; không dùng “ngoài SPEC” để xóa nghĩa vụ nghiên cứu. Tuân thủ đính chính về phiên/ngữ cảnh: khôi phục nguồn sau nén, tiếp tục khi còn xác định được mục tiêu/quyền/trạng thái; khi cần chuyển phải ghi checkpoint vào LOG và báo cáo trong phạm vi được phép. Không hạ chiều sâu để vừa một lượt.

Cuối phiên: báo bốn mục theo AGENTS, ghi bước tiếp và lệnh cuối vào LOG; cập nhật đúng dòng T-041 thành chờ phản biện khi phù hợp, chưa tự nghiệm thu. Soạn prompt phản biện kết quả trung tính, chép đúng mẫu hiện hành trong docs/review-prompt.md vào LOG. Không tự gửi.

Phiên thiết kế tiếp theo đọc trực tiếp D:/RCA-flashticket/results/T-041/ban-giao-phien-2.md và manifest.json; không yêu cầu Minh copy báo cáo chat.

```

## Prompt 2 — Thiết kế ứng viên từ gói T-041

Toàn văn cập nhật; chỉ dùng khi Minh giao phiên thiết kế. Báo cáo phiên 1 được đọc trực tiếp từ repo.

```text
Bạn là Codex trong phiên thiết kế nghiên cứu RCA từ gói T-041 tại D:/RCA-flashticket. Minh không cần dán báo cáo phiên trước: đọc trực tiếp repo.

MỤC TIÊU VÀ QUYỀN HẠN

Từ yêu cầu đề tài, toàn bộ G2 và code/trung gian đã được kiểm, xây các phương án RCA cụ thể cùng giao thức phân xử. Đầu ra phải tới công thức, đường đi thông tin, đối chứng, phản ví dụ và điều kiện bác bỏ; không dừng ở “dùng đồ thị”, “kết hợp ba tín hiệu” hoặc “chọn công thức khi cài”.

Đây là phân tích/thiết kế ứng viên ngoài task, chỉ bắt đầu khi Minh giao phiên này. Không tự nhận là phản biện chính thức T-041 hoặc mở lại task đã đóng. Chưa chọn phương pháp, hiệu quả chưa kiểm.

Chỉ đọc và trả lời trong chat. Không ghi kết quả thiết kế vào T-041 hoặc file khác; không tạo SPEC/task/LOG, sửa quyết định/plan/code/baseline. Được kiểm hash và tính nhỏ trong bộ nhớ để kiểm logic, sau khi kiểm tác dụng phụ; Python dùng -B.

Không mở test/giữ ngoài, repo RCA lưu trữ, chạy thực nghiệm mới, tải dữ liệu, cài môi trường, SSH/bật EC2, dựng Grafana, deep research, commit/push, tự mở phiên/subagent hoặc gửi sang agent khác. Cần vượt quyền thì trình đúng phần bổ sung, tiếp tục phần độc lập.

ĐỌC TRỰC TIẾP ĐẦU VÀO

Trước tiên đọc nguồn gốc để tự dựng câu hỏi và nghĩa vụ:
- D:/RCA-flashticket/AGENTS.md
- D:/RCA-flashticket/docs/STATE.md
- D:/RCA-flashticket/docs/reference/sources/DT18-de-tai-va-nhiem-vu.md
- D:/RCA-flashticket/docs/reference/sources/advisor-2026-09-23.md
- D:/RCA-flashticket/docs/MRP.md, WHY.md, DECISIONS.md, LESSONS.md, PLAN-P6.md và DE-XUAT-HUONG-GRAFANA-RCA.md.
Các tên file liệt kê cùng thư mục được hiểu ở đúng thư mục tuyệt đối đứng trước.

Sau đó đọc:
1. D:/RCA-flashticket/tasks/T-041-ra-soat-nen-p3-p5/SPEC.md và mục cuối LOG.md cùng thư mục để biết phạm vi/trạng thái.
2. D:/RCA-flashticket/results/T-041/ban-giao-phien-2.md
3. D:/RCA-flashticket/results/T-041/manifest.json
4. D:/RCA-flashticket/results/T-041/bao-cao.md
5. D:/RCA-flashticket/results/T-041/bang-chung.jsonl và các nguồn được trỏ khi kết luận phụ thuộc.

Kiểm hash đầu ra theo manifest, đối chiếu nguồn/code thực sự dùng và trạng thái phản biện/nghiệm thu. Không coi chưa phản biện hoặc chưa được Minh quyết là đã duyệt. Nếu nguồn đổi sau T-041, xác định kết luận nào còn dùng được và phần cần kiểm lại; không âm thầm dùng hash mới thay hash cũ.

Nếu gói chưa có, đang dang dở hoặc lệch hash, nêu đúng phần bị chặn. Có thể làm phần độc lập từ nguồn đã xác minh; không bịa kết quả T-041, yêu cầu copy chat hoặc dựng lại toàn bộ điều tra như một cách bỏ qua đầu vào thiếu.

Kiểm lại đoạn code/hợp đồng/trung gian mà lựa chọn thiết kế thực sự phụ thuộc. Không lặp công việc đã có đầu ra hợp lệ, không mặc nhiên tin kết luận phiên trước.

Nguồn đối chiếu tiếp:
- D:/RCA-flashticket/results/T-034/goi-g2.md, ban-do-g2.json và manifests hiện hành.
- D:/RCA-flashticket/results/T-040/ban-giao-p6.md, yeu-cau-quan-sat-p9.md.
- Các module/nguồn được T-041 trỏ; không theo link sang repo lưu trữ.

BỐI CẢNH PHẢI GIỮ ĐÚNG

Hướng Grafana vẫn là đề xuất. MRP/WHY hiện hành yêu cầu đồ thị tham gia trực tiếp vào điểm bất thường; đề xuất dùng luật cảnh báo rồi RCA là khác biệt phạm vi cần quyết. Không tự chọn một hướng để hoàn tất bảng.

P5 được nghiệm thu không chứng minh quan hệ giúp RCA. Tách căn cứ sửa hạn chế, yêu cầu DT18 và nhu cầu kỹ thuật. A–G chỉ là cách nhóm: vị trí bằng chứng; biểu diễn tín hiệu; nền/thang/gộp; vai trò quan hệ; tập ứng viên/thiếu dữ liệu; mốc/phát hiện; quan hệ ngoài lời gọi/schema. Kiểm đủ G2-H01–H26 và mục tiêu nguồn.

CÔNG VIỆC PHẢI ĐI ĐẾN ĐẦU RA

1. Câu hỏi có thể bác bỏ

Phát biểu rõ:
- Phân bổ theo quan hệ bổ sung thông tin gì so với gán cho owner?
- Log/tín hiệu giảm giúp lỗi return theo cơ chế nào?
- Cải thiện có thể chỉ do thêm tín hiệu, đổi nền/cửa sổ, lưu lượng hoặc tập ứng viên không?
- Những trường hợp nào không đủ thông tin để định vị root?

Đọc cả ca đúng và bằng chứng bất lợi. Không ép mọi ca sai thành “nhầm triệu chứng”; không dùng báo trước mốc làm bằng chứng độ trễ lan truyền.

2. Tập hữu hạn phương án có căn cứ

Xét phương án trực tiếp liên quan, nêu vì sao giữ hoặc không thử. Không cài mặc định mọi UV hoặc mọi họ thuật toán. Khi cần prior work, đọc bài/code chính thức đúng phần liên quan; tra hẹp, không mở khảo sát rộng.

Mỗi phương án giữ phải có:
- mục tiêu, căn cứ và phương án cạnh tranh đủ mạnh;
- nút, cạnh, hướng, loại quan hệ, địa chỉ và scope log/trace/metric;
- công thức/giả mã đủ để người khác cài mà không tự bịa lựa chọn khoa học;
- thông tin được giữ/mất/chuyển từ nơi ghi sang nơi nhận điểm;
- đầu vào thật sự có trên từng dataset/FlashTicket;
- giả định, điều kiện thất bại và kết quả bác bỏ;
- code dùng lại, phần cần bổ sung và phép kiểm của chính thành phần.

3. Đặc tả phần dùng chung

Giải quyết cụ thể:
- nguồn nền; vai trò học/chọn cấu hình/hiệu chỉnh/đánh giá; thiếu nền;
- điểm tăng/giảm, nền hằng/gần hằng/thưa/trôi, cadence và hàng lặp;
- đơn vị, chuẩn hóa và gộp tín hiệu; không để nhiều mẫu/cột tự tạo trọng số áp đảo;
- log trùng/trường động; số dòng khác số request;
- thời lượng phía gọi/phía nhận/phần chưa bị con phủ nếu dùng; chồng lấn, song song, bất đồng bộ, mất span;
- cực trị hợp lệ khác lỗi số học; không mặc định cắt mọi điểm lớn;
- root không có cạnh/tín hiệu, thao tác mới không nền; thiếu bằng chứng khác điểm bình thường;
- tập mô hình/quan sát/chấm/trả về, hòa, ERROR/UNSUPPORTED; gộp thao tác lên service và đơn vị đáp án service/thao tác/cạnh;
- thời gian sự kiện/nhận/quyết định/công bố; mốc chốt và độ trễ toàn chuỗi;
- đường nhãn, tên ca, mốc tiêm và schema liên hệ root có thể lọt vào tự phát hiện.

Không coi cạnh trace chưa phân kiểu là đồng bộ đã xác minh, không suy messaging/host từ tên. Nêu phần chỉ kiểm được khi có đầu vào online phù hợp. Mọi giả thuyết mới phải ghi “chưa kiểm”, giả định, khi sai và kết luận phụ thuộc.

4. Vai trò tính toán của quan hệ

Chỉ phép nhận cạnh và đầu ra đổi khi thay quan hệ, giữ phần còn lại tương đương ở mức có thể.

Nếu gộp/lan: định nghĩa và biện minh; kiểm truyền nhiễu, lặp bằng chứng, khuếch đại theo bậc/lưu lượng; xét phương án đơn giản hơn không lan. Không mặc định PageRank, không chọn theo độ chênh có–không đồ thị.

Tách cây trace và graph service. Nhánh còn self-time theo cây vẫn dùng cấu trúc. Với DB/cache/messaging/tài nguyên chung, nêu phép tính, đầu vào phải xác minh và phép kiểm; không thêm chỉ để hình đủ loại cạnh.

5. Hai nhánh phát hiện để Minh quyết

Tách lõi RCA dùng chung khỏi:
- giữ yêu cầu đồ thị trực tiếp tham gia điểm/quyết định bất thường;
- luật cảnh báo mở sự cố rồi gọi RCA, nếu Minh duyệt thu hẹp.

Mỗi nhánh nêu đầu vào, hiệu chỉnh, baseline, phép chấm, chi phí có căn cứ hoặc chưa đo, và phần đáp ứng/chưa đáp ứng nguồn hiện hành. Xác định phần chung/điểm rẽ; không xây hai hệ thống hoàn chỉnh. Chờ cô không làm phần RCA dùng chung bị bỏ trống, cũng không cho phép tự đổi MRP.

6. Ma trận kiểm chứng vừa đủ để phân xử

Phân biệt:
- thêm tín hiệu với dùng quan hệ;
- nơi gán bằng chứng với chuẩn hóa/gộp;
- cấu trúc đúng với graph ngẫu nhiên;
- ranker tốt hơn với detector chọn mốc thuận lợi;
- sửa ca khó với làm hỏng ca đang đúng.

Chọn baseline theo dataset, trạng thái hỗ trợ và phiên bản. Giữ số P3 lịch sử, biến thể mới riêng. Xem xét nhánh chẩn đoán G2 khi sức mạnh phép so phụ thuộc; không chỉ chọn bản yếu để dễ thắng.

Mỗi phép so ghi:
giữ gì → đổi gì → đo gì → dự đoán đối lập → hỗ trợ/bác bỏ/chưa phân xử → kết luận được phép.

Giữ cùng tín hiệu, coverage, cửa sổ, ứng viên và ngân sách ở phần không chủ ý thay; nếu không giữ được, giới hạn kết luận. Graph ngẫu nhiên phải có nghĩa với cách gắn bằng chứng, không tạo đầu vào phi lý rồi lấy thất bại làm bằng chứng cấu trúc thật có ích.

Dev để thiết kế; test/giữ ngoài sau khóa và có quyền riêng. Không bỏ nhóm khó hoặc đánh giá độc lập.

7. Kiểm logic và tìm phản ví dụ

Dùng tính tay/tính nhỏ trong bộ nhớ cho trường hợp thật sự phân biệt phương án: tín hiệu phía gọi, return không tăng trễ, nền gần hằng, lệch lưu lượng, root cô lập, thao tác thiếu nền, thiếu span, đến muộn, tài nguyên chung khi liên quan.

Ghi đầu vào, trung gian, kết quả. Chủ động tìm ca phương án sai hoặc hai phương án không phân biệt được. Ví dụ tính tay không chứng minh hiệu quả thật. Nếu công thức chưa nhất quán, tiếp tục giải thiết kế trong quyền; không che bằng “đến lúc cài sẽ chọn”.

ĐẦU RA BẮT BUỘC TRONG CHAT

A. Phạm vi dùng chung, điểm rẽ chờ quyết, phần mục tiêu chưa bao phủ.
B. Bảng phương án đã xét: giữ để thử/không ưu tiên/không áp dụng, căn cứ và điều kiện đổi quyết định.
C. Đặc tả ứng viên: ký hiệu, công thức/giả mã, hợp đồng dữ liệu, ngoại lệ, trạng thái thiếu bằng chứng; liên kết code dùng lại/phần bổ sung.
D. Kết quả kiểm logic, phản ví dụ và giới hạn.
E. Ma trận baseline/đối chứng/dataset/phép phân xử, giao thức chọn cấu hình/hiệu chỉnh/khóa.
F. Đủ G2-H01–H26 và yêu cầu đề tài: thành phần xử lý, điều kiện tính đúng, không áp dụng có lý do, hoặc OPEN có hệ quả; không ép mỗi hạn chế thành thuật toán.
G. Tổ chức tiếp theo theo phụ thuộc: phần dùng lại, bổ sung, thử sớm, có thể hoãn/bỏ để tránh overengineering. Không tự chốt số task/phiên khi chưa có căn cứ.
H. Phần thật sự cần Minh quyết hoặc duyệt chạy: đề xuất, lý do, bằng chứng thiếu, phạm vi file/đầu ra, chi phí biết/chưa đo. Không đẩy việc đọc/kiểm nhỏ trong quyền vào đây để kết thúc sớm.

TIÊU CHÍ KẾT THÚC

Người cài đặt sau này phải hiểu phép tính, giao diện và phép chấm mà không tự bịa lựa chọn khoa học. Khép hết phần đọc/kiểm logic làm được hợp lý trong quyền. Câu cần thực nghiệm vẫn OPEN nhưng có phép phân xử, đầu vào, điều kiện và quyết định phụ thuộc; không hứa giải mọi câu hỏi trước khi có bằng chứng.

Không nhận đã hoàn thành P6, xác nhận cơ chế hoặc lợi ích từ bảng thiết kế/tính tay. Không tự chuyển nhận định sang DECIDED.

Làm tới báo cáo hoàn chỉnh. Sau nén, khôi phục nguồn và trạng thái; không giảm chiều sâu để vừa một lượt. Nếu buộc chuyển, checkpoint đầy đủ trong chat, không ghi file.

Cuối cùng báo bốn mục theo AGENTS và soạn prompt phản biện trung tính, chép đúng mẫu hiện hành D:/RCA-flashticket/docs/review-prompt.md. Không tự gửi. Muốn lưu thiết kế vào repo phải trình gói file và quyền riêng; không ghi tiếp vào kết quả T-041.

```

## Prompt Claude soát SPEC

Chép nguyên văn Prompt chung, Khối soát SPEC và Khối G3 từ docs/review-prompt.md; chỉ điền trường thông tin trung tính. Minh chuyển thủ công; Claude chỉ trả lời chat.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-041, D:/RCA-flashticket/tasks/T-041-ra-soat-nen-p3-p5/SPEC.md.
- Công đoạn: soát SPEC.
- Gói/cổng: chuẩn bị P6, trước G3.
- Người làm và người phản biện chính thức: Codex làm; Claude phản biện.
- Tài liệu gốc: SPEC và LOG tại D:/RCA-flashticket/tasks/T-041-ra-soat-nen-p3-p5/; D:/RCA-flashticket/docs/MRP.md, WHY.md, DECISIONS.md, LESSONS.md, PLAN-P6.md, DE-XUAT-HUONG-GRAFANA-RCA.md; nguồn đề tài được nêu bên dưới; đối chiếu diff hiện có của các file T-041.
- Phản biện và phản hồi trước: chưa có phản biện chính thức SPEC T-041.
- Code và kết quả liên quan: D:/RCA-flashticket/src/p3/, src/do_thi/, src/do_thi_tinh/; D:/RCA-flashticket/results/T-034/goi-g2.md, ban-do-g2.json và runs/manifest-cuoi-007/manifest.json; D:/RCA-flashticket/results/T-040/ban-giao-p6.md, yeu-cau-quan-sat-p9.md và manifest.json. Chưa triển khai T-041, chưa có bốn file kết quả của task.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; không tạo REVIEW hoặc sửa file.

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


## Kết thúc phiên chuẩn bị SPEC — 21/10/2026 — Codex

1. **Đã làm:** tạo SPEC T-041 chờ duyệt thực hiện; lưu đầy đủ hai prompt công việc và prompt Claude soát SPEC trong LOG; ghi Q-182 trước khi cập nhật STATE. Chưa thực hiện phân tích nền P3/P5 của task.
2. **File đã thay đổi:** tasks/T-041-ra-soat-nen-p3-p5/SPEC.md, LOG.md; docs/DECISIONS.md, docs/STATE.md. Bốn file results/T-041/ chưa tạo; không tạo REVIEW hoặc file ngoài gói.
3. **Kiểm đã chạy và kết quả:** toàn văn hai file mới khớp bản soạn; đủ 12 mục mẫu SPEC; ba prompt đầy đủ, khối code cân bằng; UTF-8 và khoảng trắng hợp lệ. Kiểm byte phần cũ DECISIONS giữ nguyên; đảo đúng các thay đổi STATE khôi phục hash gốc. 42 file bảo vệ (luật, nguồn, kế hoạch và code liên quan) không đổi; trạng thái đường dẫn ngoài phạm vi và HEAD không đổi. git diff --check đạt; đã đọc diff đầy đủ các file chung và đối chiếu toàn văn hai file mới. Lượt đọc snapshot đầu có đầu ra quá dài, đã chạy lại chỉ giữ metadata trong bộ nhớ, không tạo file phụ; không dùng lượt đó làm kết quả phân tích khoa học.
4. **Còn chờ:** Claude rà SPEC trong chat và Minh duyệt SPEC để thực hiện. Gói lưu đã được duyệt, task chưa được duyệt triển khai. Câu hỏi nguồn mới được bao phủ ở mức đề bài/tiêu chí; chưa có bằng chứng mới về code, cơ chế, khả năng dùng lại hoặc hiệu quả RCA. Các lựa chọn phương pháp, phát hiện và hướng Grafana vẫn theo nguồn hiện hành, chưa chốt thêm. Đề xuất kết thúc phần chuẩn bị và chuyển soát SPEC; không có lượt phản biện nào được tự khởi động.
5. **Bước tiếp theo chính xác:** Minh dùng khối “Prompt Claude soát SPEC” trong LOG này; Claude đọc SPEC, luật và nguồn trực tiếp, chỉ trả lời chat. Sau khi Minh duyệt đúng SPEC để thực hiện, dùng khối “Prompt 1”. Khi gói T-041 đã có và Minh giao thiết kế, dùng khối “Prompt 2”: đọc results/T-041/ban-giao-phien-2.md, manifest.json, bao-cao.md và bang-chung.jsonl, không cần copy báo cáo chat. Không chạy các bước đó trong phiên chuẩn bị này.
6. **Lệnh cuối dự kiến thực hiện ngay sau ghi mục này:** git diff --check -- docs/DECISIONS.md docs/STATE.md tasks/T-041-ra-soat-nen-p3-p5/SPEC.md tasks/T-041-ra-soat-nen-p3-p5/LOG.md

**Nội dung commit đề xuất khi Minh cho phép riêng:** “docs: add T-041 audit specification and repository handoff prompts”. Chưa commit hoặc push.


## Phiên chuẩn bị bổ sung — 21/10/2026 — Codex — đồng bộ quyền và prompt, chưa chạy task

- Thiết bị: Windows 11, workspace D:/RCA-flashticket.
- Vai trò: Codex là người làm T-041; Claude là người phản biện chính thức. Đây không phải phiên phản biện hoặc phiên thiết kế thứ hai.
- Loại yêu cầu: EXECUTE tài liệu. Lượt này chỉ cập nhật SPEC, nối LOG, nối DECISIONS và đồng bộ thông tin T-041 trong STATE; chưa thực hiện phân tích của T-041.
- Nguồn quyền: lời Minh ngày 21/10/2026, đã nối Q-183 trong docs/DECISIONS.md trước khi đồng bộ SPEC/trạng thái:

> LƯU HAI PROMPT MỚI VÀO LOG T-041, ĐỒNG BỘ SPEC, STATE VÀ DECISIONS VỚI QUYỀN TỰ RÀ, TỰ SỬA SPEC RỒI TRIỂN KHAI. PHIÊN NÀY CHỈ CẬP NHẬT TÀI LIỆU, CHƯA CHẠY TASK.

### Quyết định của Minh trong phiên và tác động

- Q-183 cho phép phiên 1 được giao sau này tự rà theo nguồn gốc, tự sửa lỗi/thiếu sót SPEC trong đúng mục tiêu rà nền P3/P5 và gói tám file Q-182; ghi bằng chứng, thay đổi, tác động; kiểm lại rồi thực hiện, không chờ Minh duyệt lại từng sửa chữa thuộc quyền hoặc chờ Claude rà SPEC.
- Quyền mới thay điều kiện chờ duyệt thực hiện/khóa SPEC cũ của riêng T-041. Không đổi vai trò chính thức; tự rà không thay phản biện, quyết định khoa học hoặc nghiệm thu.
- Phiên 2 đọc trực tiếp đầu ra T-041, tự rà cả đề bài/SPEC nguồn và giả định; tự sửa đề bài/phương án đang xây trong chat rồi tiếp tục. Phiên này chưa có SPEC ghi riêng và không có quyền sửa file T-041/lưu thiết kế.
- Giữ Q-182 và toàn bộ prompt cũ làm lịch sử. Hai khối “Prompt 1 hiện hành” và “Prompt 2 hiện hành” dưới đây là bản dùng cho các phiên công việc tiếp theo. Không áp điều kiện chờ duyệt cũ của prompt lịch sử cho quyền Q-183.
- Không mở rộng mục tiêu, tám đường dẫn, quyền dữ liệu, chi phí hoặc sửa nguồn/baseline/kết quả cũ. Ngoài quyền hoặc còn mâu thuẫn thực chất giữa các nguồn có thẩm quyền: dừng phần sửa/kết luận phụ thuộc, báo nguồn/bằng chứng/đề xuất; tiếp tục phần độc lập hợp lệ.
- Không tạo bốn file đầu ra hoặc placeholder ở lượt này. Không chạy T-041, thực nghiệm hay phương án thiết kế phiên 2.

### Đồng bộ theo file: nội dung cũ → mới, lý do và ảnh hưởng

| File | Cũ → mới | Vì sao và ảnh hưởng |
|---|---|---|
| docs/DECISIONS.md | Q-182 là quyền chuẩn bị → nối Q-183 ghi lời giao mới, giữ nguyên Q-182 | Lưu quyền bền vững; không sửa lại lời duyệt lịch sử hoặc tạo quyết định phương pháp |
| SPEC.md của T-041 | Chờ duyệt thực hiện; SPEC khóa → quyền tự rà/sửa có giới hạn rồi thực hiện ở phiên được giao | Đồng bộ nguồn duyệt, điều kiện bắt đầu, giai đoạn đầu ra, bảng quyền ghi, bước 0, kiểm phạm vi và con trỏ prompt; giữ câu hỏi, độ sâu khoa học, tám file và giới hạn thực nghiệm |
| docs/STATE.md | T-041 chờ soát/duyệt → có quyền Q-183 nhưng hiện chưa chạy | Chỉ sửa các mô tả T-041; không đổi cổng, trạng thái task khác hoặc hướng đang chờ cô |
| LOG.md của T-041 | Hai prompt lịch sử → nối đầy đủ hai prompt hiện hành và prompt Claude soát SPEC | Giữ lịch sử; phiên mới đọc trực tiếp repo, không cần copy báo cáo chat hoặc xin lại quyền đã giao |

Điểm điều chỉnh cơ học trong Prompt 1: Q-183 đã được ghi ở lượt này nên phiên thực hiện phải kiểm và dẫn lại, không nối một quyết định trùng. Phiên 2 “tự sửa” áp dụng cho đề bài/phương án trong chat; không ngầm cho ghi SPEC nguồn ngoài phạm vi đã duyệt.

### Chi phí và ảnh hưởng tới file cũ

- T-041 dự kiến đọc code/trung gian đã lưu, kiểm hash và phép tính nhỏ trong bộ nhớ; không huấn luyện, chạy lại baseline/ma trận hay thử phương pháp mới trên dữ liệu thật. Đọc/hash đầu ra lớn vẫn có thể tốn I/O; chưa đo nên không gán số phút/giờ.
- Không yêu cầu tải dataset/model, cài môi trường hoặc dùng EC2. Không có gói tải nặng được giao cho hai phiên.
- Phiên 1 có thể tự sửa SPEC T-041 trong quyền, nối LOG, cập nhật thông tin T-041 trong STATE và tạo/hoàn thiện đúng bốn đầu ra mới. Q-183 ở DECISIONS đã có thì không ghi trùng. Không sửa code, dataset, baseline, SPEC hoặc kết quả của task cũ.
- Phiên 2 chỉ đọc và thiết kế trong chat; không sửa file repo. Việc thật sự cần chạy nặng, tải hoặc thêm file phải trình riêng, không cắt nghĩa vụ nghiên cứu để tránh báo phần thiếu.

## Prompt 1 hiện hành — Tự rà, tự sửa SPEC rồi thực hiện T-041 (Q-183)

```text
Tôi là Minh. Tôi giao Codex tự rà SPEC, sửa các lỗi trong phạm vi được ủy quyền rồi thực hiện T-041 tại D:/RCA-flashticket.

Đây là chỉ đạo mới thay cho trạng thái “chờ duyệt thực hiện” trong SPEC/LOG trước đó. Không yêu cầu tôi duyệt lại từng sửa chữa SPEC thuộc đúng phạm vi dưới đây. Không dừng sau khi chỉ báo lỗi hoặc lập kế hoạch. Chỉ đạo này đã được lưu tại Q-183; phiên chuẩn bị tài liệu ngày 21/10/2026 chưa chạy task. Prompt này giao phiên nhận nó bắt đầu công việc thực hiện.

QUYỀN ĐƯỢC GIAO

1. Đọc nguồn chi phối và tự rà SPEC trước khi triển khai. Không tin tuyệt đối SPEC, LOG, báo cáo G2, kết luận agent trước hay chính giả định của mình.
2. Được tự sửa lỗi, thiếu sót và điểm chưa nhất quán của SPEC trong đúng mục tiêu và gói tám file đã duyệt. Ghi bằng chứng, thay đổi và tác động; kiểm lại rồi thực hiện ngay, không chờ duyệt từng sửa chữa đó.
3. Quyền sửa bao gồm: câu hỏi và phép phân xử còn thiếu trong mục tiêu rà nền; đường dẫn/revision sai; logic, thứ tự phụ thuộc, hợp đồng và tiêu chí xong chưa đúng; phép kiểm nhỏ phù hợp; nội dung bàn giao thiếu. Sửa SPEC để khớp nguồn có thẩm quyền, không sửa nguồn hoặc thu hẹp nghĩa vụ nghiên cứu để làm SPEC dễ đạt.
4. Giữ T-041 là rà sâu code, hợp đồng và trung gian P3/P5 đã có để chuẩn bị thiết kế RCA. Không biến task thành cài phương pháp P6, chạy thực nghiệm mới hoặc chọn phương án thay Minh.
5. Không mở rộng danh sách file, quyền đọc test/giữ ngoài, mục tiêu nghiên cứu, chi phí hoặc quyền sửa baseline/nguồn cũ. Không đổi MRP/PLAN-P6/WHY hay chốt hướng Grafana. Nếu cần vượt quyền, hoặc các nguồn có thẩm quyền còn mâu thuẫn thực chất chưa được chỉ đạo này giải quyết: dừng phần sửa và kết luận phụ thuộc, nêu bằng chứng và đề xuất cụ thể; tiếp tục phần độc lập hợp lệ.
6. Đây là tự kiểm của người làm. Codex vẫn là người làm; Claude vẫn là người phản biện chính thức. Không cần chờ Claude rà SPEC để bắt đầu phiên được giao này. Tự kiểm không thay nghiệm thu của Minh hay phản biện chính thức.

GHI NHẬN QUYỀN VÀ TRẠNG THÁI TRƯỚC KHI LÀM

- Kiểm Q-182 và Q-183 trong docs/DECISIONS.md, SPEC hiện hành, STATE và mục cuối LOG. Giữ Q-182 cùng mọi mục LOG cũ như lịch sử; quyền mới theo Q-183. Không nối lại một quyết định đã được ghi, không coi trạng thái chờ duyệt cũ trong prompt lịch sử là trạng thái hiện hành.
- Mở phiên trong LOG, ghi nguồn quyền, ngày, agent, thiết bị và vai trò. Ghi đúng việc đã bắt đầu, không nhận là Minh đã duyệt một công thức, lựa chọn khoa học hay hiệu quả chưa kiểm.
- Nếu bản repo nhận được thiếu Q-183 hoặc khác phạm vi so với lời giao này: kiểm nguồn thật, trình rõ phần lệch; không bịa quyết định hay ghi lùi ngày.

PHẠM VI GHI: ĐÚNG TÁM FILE

1. D:/RCA-flashticket/tasks/T-041-ra-soat-nen-p3-p5/SPEC.md
2. D:/RCA-flashticket/tasks/T-041-ra-soat-nen-p3-p5/LOG.md
3. D:/RCA-flashticket/results/T-041/bao-cao.md
4. D:/RCA-flashticket/results/T-041/bang-chung.jsonl
5. D:/RCA-flashticket/results/T-041/ban-giao-phien-2.md
6. D:/RCA-flashticket/results/T-041/manifest.json
7. D:/RCA-flashticket/docs/DECISIONS.md
8. D:/RCA-flashticket/docs/STATE.md

- SPEC chỉ tự sửa theo quyền nêu trên. LOG và bang-chung.jsonl chỉ nối thêm, giữ cả lượt hỏng.
- DECISIONS chỉ ghi lời chỉ đạo của Minh thực sự được phép ghi; Q-183 đã có thì không ghi trùng. Không tự thêm quyết định nghiên cứu dưới danh nghĩa “đồng bộ”.
- STATE chỉ cập nhật thông tin và dòng T-041 theo công việc thật; không tự nghiệm thu, đóng task/cổng hoặc đổi hướng đang chờ cô.
- Bốn file results là đầu ra mới của T-041; được hoàn thiện trong phạm vi. Không ghi lại kết quả task cũ.
- Không tạo file helper, script, cache, runs hoặc file tạm khác. Phép kiểm nhỏ dùng lệnh inline/bộ nhớ; lưu lệnh và kết quả vào bằng chứng. Nếu thật sự cần file ngoài danh sách, trình đường dẫn, nội dung, lý do, tác động và chi phí trước.

BƯỚC ĐẦU: TỰ RÀ ĐỘC LẬP RỒI SỬA SPEC

Đọc mục tiêu gốc trước khi dùng SPEC làm danh sách công việc. Tự xác định câu hỏi nguồn, phần task bao phủ, bằng chứng nào phân biệt các giải thích và kết quả nào có thể bác nhận định. Sau đó đối chiếu SPEC:
- Có khớp DT18, hướng dẫn cô, MRP và phạm vi P3–P6/P9 không?
- Có biến ứng viên, giả thuyết hoặc suy luận thành sự thật/quyết định không?
- Có bỏ nhóm quan trọng, ca phản bác hoặc phép kiểm cần thiết chỉ để vừa task không?
- Code và trung gian thật có hỗ trợ điều được hứa không? Thiếu đầu vào nào không thể khắc phục bằng đọc thêm?
- Có mâu thuẫn quyền ghi, phụ thuộc, tiêu chí xong chỉ đếm file, giả định không thể kiểm hoặc kết luận vượt quyền không?
- Có lặp điều tra đã có đầu ra hợp lệ, thêm hạ tầng/quy trình không cần thiết hoặc cài thuật toán khi chưa có câu hỏi cần nó không?
- Phần nào làm được ngay bằng dữ kiện/quyền hiện có, phần nào thật sự cần Minh quyết?

Lưu bảng tự rà: vấn đề → nguồn/bằng chứng → tác động → sửa hoặc giữ và lý do. Với lỗi thuộc quyền: tự sửa SPEC, ghi đoạn cũ → mới hoặc mô tả đủ rõ, lý do và hệ quả trong LOG; kiểm lại rồi tiếp tục thực hiện. Không chỉ đưa danh sách lỗi rồi chờ duyệt. Nếu không có lỗi đáng kể, nói rõ đã kiểm gì; không tạo lỗi cho đủ số lượng.

NGUỒN PHẢI ĐỌC THEO PHỤ THUỘC

Root chuẩn D:/RCA-flashticket; các đường dẫn dưới đây thuộc root này:
- AGENTS.md; docs/STATE.md; SPEC và mục cuối LOG T-041.
- docs/DECISIONS.md, docs/MRP.md, docs/WHY.md, docs/LESSONS.md; phần hiện hành docs/PLAN-P6.md, docs/DE-XUAT-HUONG-GRAFANA-RCA.md. Đề xuất Grafana chưa tự thành quyết định.
- docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và advisor-2026-09-23.md.
- results/T-034/goi-g2.md, ban-do-g2.json, bang-baseline.json, hai-phep-kiem.md/json; manifest và nguồn hiện hành theo LOG task T-034.
- results/T-035/dac-ta-do-thi.md, kiem-dung-dan.md; hợp đồng và bàn giao T-036 hiện hành theo LOG/manifest, kể cả bản SMTP V2 khi liên quan.
- results/T-040/ban-giao-p6.md, yeu-cau-quan-sat-p9.md, con-mo.json và manifest.json.
- src/p3/, src/do_thi/, src/do_thi_tinh/; đường gọi, fixture, adapter và trung gian thật do các nguồn này dẫn tới.
- SPEC/LOG và đầu ra liên quan T-022, T-024, T-025, T-026, T-028–T-034; hồ sơ phương pháp/dataset và code nguồn chính thức khi kết luận phụ thuộc. Đọc đính chính hiện hành trước khi dùng kết quả cũ.

Không chỉ đọc tóm tắt hoặc dừng ở danh sách tên file. Kiểm hash theo manifest phù hợp trước dùng đầu ra cũ; lệch thì giữ bằng chứng, dừng phần phụ thuộc và báo, không tạo manifest mới để hợp thức hóa. Xác minh allowlist và miền dev trước mở dữ liệu. Không đọc archive D:/Project/flash-ticket-rca-research, data/locked/, test hoặc nội dung giữ ngoài, dù có đường dẫn xuất hiện trong báo cáo.

NỘI DUNG PHẢI PHÂN TÍCH SÂU

1. Dựng đường xử lý thực tế:
nguồn → selector/adapter → cửa sổ/nền → metric/log/trace → đồ thị/đặc trưng → điểm → tập ứng viên → thứ hạng → evaluator.
Ghi file/hàm, kiểu vào–ra, trung gian và điều kiện từng nhánh. Tách dataset/chế độ, mã chung/riêng, đầu vào phương pháp/nhãn đánh giá, graph tĩnh/graph quan sát/cây span. Không coi định dạng giống nhau là cùng ngữ nghĩa.

2. Kiểm khả năng dùng lại tới hợp đồng thật:
- thời gian, đơn vị, biên và thời điểm thông tin khả dụng;
- cột, thiếu dữ liệu, fill, nền thưa/hằng/trôi, cadence và mẫu lặp;
- alias, scope service/operation/resource;
- parent/link/kind, span mồ côi/trùng, khoảng thời gian chồng lấn;
- log join, template động và đếm trùng;
- các tập ứng viên theo định nghĩa nguồn; chỉ rõ bộ bốn tập khi có, không tự đồng nhất;
- trị số cực đoan, lỗi số học, hòa, ERROR/UNSUPPORTED và fallback;
- cache, revision, điều kiện tái dùng và phần phải đổi.
Đối chiếu code, fixture và đầu ra đã lưu; tên module hoặc chạy không lỗi không phải bằng chứng đủ.

3. Lần cơ chế ở nhóm quan trọng:
Đọc code và trung gian trước. Chọn ca sai và ca đúng có điều kiện tương ứng, ghi tiêu chí chọn, mở rộng khi có phản ví dụ. Chỉ ra trong điều kiện X, bước Y làm mất/đánh giá sai thông tin Z, bằng chuỗi đầu vào → hàm/xử lý → trung gian → đầu ra. Xét giải thích khác và phần có thể bác nhận định. Nếu chưa xác định Y, giữ đúng quan sát và bằng chứng thiếu; không gán đặc tính chung của thuật toán cho mọi ca sai. Không thay phân tích này bằng cờ, số tổng hoặc nhãn hạn chế.

4. Kiểm ranh giới cho P6:
Graph gộp mất thông tin request/thời gian gì? Khi nào cần span gốc để phân biệt owner/caller/callee? Quan hệ span quan sát khác cạnh có ngữ nghĩa gọi/thông điệp/dữ liệu ở đâu? Offline và online chung được phần nào? Ánh xạ operation → service/nhãn có hợp lệ không? Bằng chứng thiếu ảnh hưởng kết luận nào? Collector không khôi phục được thông tin chưa từng được ghi; tách collector, instrumentation và giao thức.

5. Đối chiếu toàn bộ nguồn:
Bao phủ đủ G2-H01–H26, bảy nhóm A–G, các ứng viên trong nguồn và DT18/MRP. Không mặc định R1–R4 là toàn bộ G2, không ép mỗi hạn chế thành một thuật toán. Tách hạn chế dữ liệu/đầu vào, giao thức, adapter/cài đặt và giả định/phép tính. Nếu viện dẫn hạn chế phương pháp, kiểm bài/code gốc khi cần, tránh biến lỗi bản cài thành khoảng trống nghiên cứu.

ĐƯỢC KIỂM GÌ, KHÔNG TỰ CHẠY GÌ

- Đọc, tìm kiếm, kiểm hash và phép tính nhỏ trong bộ nhớ đã xét tác dụng phụ; Python dùng -B. Đọc có chọn lọc trung gian lớn đã lưu khi cần bằng chứng; ghi thời gian thực tế, không hứa thời lượng khi chưa đo.
- Không chạy lại ma trận baseline, huấn luyện, runner/test tự ghi cache/kết quả ngoài quyền, thử ứng viên trên dữ liệu thật hoặc sửa cấu hình lịch sử.
- Không SSH/bật EC2, tải dataset/model, cài môi trường, chạy Grafana S1–S4 hay sửa FlashTicket. Tra hẹp nguồn chính thức chỉ khi nhận định phụ thuộc; không tự deep research.
- Không commit/push, tự mở phiên/subagent hoặc gửi prompt cho agent khác. Minh chuyển thủ công.
- Nếu thiếu phép chạy/đầu vào cần thiết: nêu phép phân xử, dữ liệu, file cần ghi, chi phí đã biết/chưa đo và quyết định phụ thuộc. Không chạy vượt quyền, cũng không bỏ nghĩa vụ nghiên cứu bằng câu “ngoài SPEC”.

LƯU ĐẦU RA TRONG REPO, ĐỦ ĐỂ PHIÊN 2 ĐỌC TRỰC TIẾP

- bao-cao.md: bản đồ đường xử lý, bảng dùng lại có hợp đồng, đối chiếu đủ nguồn, chuỗi cơ chế/ca đối chiếu, giải thích khác, giao diện tối thiểu và phần còn thiếu.
- bang-chung.jsonl: mỗi phép đọc/kiểm quan trọng có ID ổn định, thời điểm, câu hỏi, lệnh/phép tính, nguồn/JSON pointer, kết quả và lỗi. Chỉ nối thêm; không chép khối dữ liệu thô lớn.
- ban-giao-phien-2.md: trạng thái thật, thứ tự đọc, hợp đồng đã xác minh, điều kiện dùng lại, giả định, phần thiếu, quyết định/bước tiếp phụ thuộc và liên kết tới bằng chứng. Không cần lịch sử chat, không chép lại cả báo cáo.
- manifest.json: revision/nguồn/code thực sự dùng, hash nguồn và kết quả kiểm theo manifest phù hợp; hash ba đầu ra cùng SPEC. Không tự hash manifest, không nhận LOG đang nối thêm hay STATE/DECISIONS là bất biến.
- LOG: mở phiên, tự rà/sửa SPEC, tiến độ sau từng bước, checkpoint, quyết định của Minh thực sự có trong phiên, báo cáo cuối và prompt bàn giao. Tách FACT, USER_CONFIRMED, CANDIDATE, DECIDED, OPEN; ghi lựa chọn kỹ thuật là ứng viên khi chưa được quyết.

TIÊU CHÍ KẾT THÚC: LÀM HẾT PHẦN KIỂM ĐƯỢC, KHÔNG ĐỂ LẠI VIỆC ĐỌC ĐANG LÀM ĐƯỢC

- Mọi phép đọc/kiểm hợp lý trong quyền đã thực hiện. Không để “phiên sau đọc code/trung gian đang có” chỉ vì dừng ở mô tả.
- Mỗi OPEN phân biệt: chưa kiểm; file chưa tiếp cận; thông tin chưa từng ghi/giới hạn dữ liệu; cần thực nghiệm mới; cần Minh quyết. Có bằng chứng tối thiểu cần bổ sung, phép phân xử, owner, phạm vi/chi phí đã biết hoặc chưa đo và kết luận phụ thuộc. Không tuyên bố mọi câu hỏi khoa học đã đóng.
- Tự kiểm cả bằng chứng phản bác, liên kết, JSONL, hash/manifest, toàn bộ diff và phạm vi ghi. Lỗi SPEC/đầu ra thuộc quyền thì tự sửa, kiểm lại rồi tiếp tục; không xin duyệt lại từng lỗi đã được ủy quyền.
- Không nhận hoàn thành rà nền là đã xác nhận hiệu quả RCA, hoàn thành P6/M1 hoặc đủ quyền mở test.
- Nếu ngữ cảnh bị nén: checkpoint trong file được phép, phục hồi từ repo, không giảm độ sâu hoặc bỏ nhánh khó để vừa phiên. Nếu cần chuyển phiên, bàn giao phần đã làm và bước còn lại đủ cụ thể, không làm lại đầu ra hợp lệ.
- Cuối phiên báo bốn mục theo AGENTS; LOG có bước tiếp chính xác và lệnh cuối. Cập nhật dòng T-041 theo thực tế, khi hoàn tất rà nền là chờ phản biện, chưa nghiệm thu.
- Soạn prompt Claude theo nguyên văn Prompt chung + đúng khối công đoạn + khối cổng hiện hành trong docs/review-prompt.md, chỉ điền thông tin trung tính. Không tự gửi. Hai prompt công việc không thay prompt phản biện chính thức.
- Phiên 2 phải đọc trực tiếp gói results/T-041 và trạng thái task, không yêu cầu Minh copy báo cáo chat.
```

## Prompt 2 hiện hành — Tự rà rồi thiết kế RCA trong chat (Q-183)

```text
Tôi là Minh. Tôi giao Codex thực hiện phiên thiết kế RCA sâu từ gói T-041 tại D:/RCA-flashticket.

Trước khi thiết kế, phải tự rà và phản biện đề bài, SPEC nguồn, báo cáo T-041 và các giả định. Nếu phát hiện lỗi trong phương án thiết kế đang xây, tự sửa trong chat rồi tiếp tục, không chờ tôi duyệt từng sửa chữa thuộc phạm vi phiên này. Không chỉ báo lỗi, đề xuất cách làm rồi dừng.

PHẠM VI VÀ QUYỀN

- Đây là phiên thiết kế ngoài T-041, chỉ đọc repo và trả lời trong chat. Chưa có SPEC riêng được duyệt cho việc ghi thiết kế. Vì vậy, lập đề bài/đặc tả làm việc ngay trong chat, tự rà và tự sửa đề bài/phương án ấy trước và trong khi thiết kế.
- Phải tự rà cả SPEC nguồn T-041; nếu phát hiện sai, kiểm nguồn gốc và nêu đính chính, bằng chứng, tác động trong chat. Quyền tự sửa SPEC T-041 bằng file thuộc phiên 1 theo Q-183, không tự chuyển sang phiên 2. Không ghi đè gói T-041 hoặc tự mở lại task đã đóng.
- Được đọc, kiểm hash, tính toán nhỏ trong bộ nhớ sau khi xét tác dụng phụ; Python dùng -B. Không tạo file, script, cache, task mới hoặc ghi kết quả thiết kế vào repo.
- Không sửa code/baseline/kết quả cũ, DECISIONS/MRP/PLAN-P6/WHY hay quyết định thay Minh; không mở test/giữ ngoài, đọc archive, chạy thực nghiệm dữ liệu thật, tải dataset/model, cài môi trường, SSH/EC2, Grafana S1–S4, deep research, commit/push hoặc tự gửi prompt/mở agent.
- Nếu cần vượt phạm vi hoặc nguồn có thẩm quyền còn mâu thuẫn thực chất: dừng phần phụ thuộc, trình đúng bằng chứng và việc cần Minh quyết; tiếp tục phần độc lập hợp lệ. Không coi điều cần xin quyền là lý do để bỏ các kiểm tra nhỏ đang làm được.

BƯỚC ĐẦU: TỰ RÀ ĐỘC LẬP, KHÔNG MẶC NHIÊN TIN T-041

Đọc yêu cầu gốc, tự xác định câu hỏi nghiên cứu, phạm vi, đầu ra, quyền, bằng chứng để chọn/bác phương án và giới hạn dữ liệu. Sau đó mới dùng SPEC, báo cáo, bàn giao và kết luận T-041 để đối chiếu. Tự lập nhận xét trước khi dựa vào kết luận của agent trước.
Kiểm:
- Đề bài có bị thu hẹp so với DT18/cô/MRP hoặc đổi hướng khi chưa được quyết không?
- Giả thuyết có bị trình bày thành sự thật? “Đã có module/đồ thị” có bị suy thành đã chứng minh lợi ích không?
- Công thức, đơn vị, hợp đồng dữ liệu, thời điểm khả dụng và ngữ nghĩa offline/online có nhất quán không?
- Có thiếu giải thích cạnh tranh, ca phản bác, baseline đủ mạnh hoặc phép phân xử không?
- Có phần overengineering, module chưa có câu hỏi cần nó, hoặc hạ tầng đang lấn mất nội dung nghiên cứu không?
- Kết quả dự kiến có thực sự phân biệt các phương án dẫn tới lựa chọn khác nhau, hay chỉ tạo thêm bảng/số?

Ghi rõ giữ gì, bác gì, sửa gì và lý do/ảnh hưởng. Lỗi trong đề bài/phương án làm việc của phiên này thì tự sửa trong chat rồi tiếp tục. Không đổi yêu cầu gốc hoặc quyết định của Minh. Không tạo lỗi để chứng tỏ có phản biện; đọc cả phần có thể bảo vệ một nhận định.

NGUỒN VÀ THỨ TỰ ĐỌC

Các đường dẫn dưới đây thuộc D:/RCA-flashticket:
1. AGENTS.md; docs/STATE.md; phần trực tiếp chi phối trong docs/MRP.md, docs/DECISIONS.md, docs/WHY.md, docs/LESSONS.md.
2. docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và advisor-2026-09-23.md; phần hiện hành docs/PLAN-P6.md và docs/DE-XUAT-HUONG-GRAFANA-RCA.md.
3. tasks/T-041-ra-soat-nen-p3-p5/SPEC.md, mục cuối LOG.md; results/T-041/ban-giao-phien-2.md, manifest.json, bao-cao.md, bang-chung.jsonl.
4. results/T-034/goi-g2.md, ban-do-g2.json và nguồn hiện hành theo LOG/manifest; results/T-040/ban-giao-p6.md, yeu-cau-quan-sat-p9.md và nguồn liên quan.
5. Code, fixture, trung gian dev đã được phép và bài/code chính thức theo đúng phụ thuộc mà lập luận cần; đọc có mục đích để kiểm hợp đồng, điều kiện thất bại hoặc giải thích khác.

Kiểm revision, hash theo manifest phù hợp và trạng thái phản biện/nghiệm thu. Trạng thái T-041 có thể đổi sau khi bàn giao; không coi snapshot lịch sử là quyền hiện hành. Hash lệch, gói thiếu hoặc đầu ra chưa hoàn tất thì chỉ rõ phần thiết kế bị chặn; không bịa nội dung, yêu cầu copy chat hay tự điều tra lại toàn bộ phiên 1. Phần độc lập có nguồn hợp lệ vẫn làm. Không làm lại bằng chứng đã hợp lệ chỉ để có kết quả của mình. Xác minh allowlist trước đọc dữ liệu; không mở test/giữ ngoài hoặc D:/Project/flash-ticket-rca-research.

KHÔNG MẶC ĐỊNH

- Hướng Grafana vẫn là ứng viên nếu Minh chưa quyết; yêu cầu phát hiện có dùng đồ thị trong MRP và đề xuất dùng luật cảnh báo còn cần phân biệt.
- P5 đã nghiệm thu không chứng minh phương pháp RCA hiệu quả.
- R1–R4 hoặc bảy nhóm A–G không tự thay toàn bộ G2-H01–H26 và yêu cầu đề tài.
- Vị trí xuất hiện tín hiệu không tự là nguyên nhân; báo động trước mốc tiêm không tự là độ trễ lan truyền âm.
- Thêm log/trace/metric tốt hơn không tự chứng minh tác dụng của cạnh.
- Thiếu dữ liệu không có nghĩa bình thường; giữ ứng viên trong danh sách không tạo thêm bằng chứng cho ứng viên ấy.

CÔNG VIỆC PHẢI LÀM SÂU

1. Xác định câu hỏi có thể bác bỏ.
Tách ít nhất các vấn đề thật sự có căn cứ: tín hiệu bị gán cho owner/caller nào; log bổ sung thông tin gì; nền/thang/số lượng/cửa sổ/tập ứng viên gây chênh ra sao; khi nào thông tin không đủ để phân xử. Dùng ca sai, ca đúng điều kiện tương ứng và ca âm/phản ví dụ. Không mặc định mọi nhóm cần một cơ chế mới.

2. Đề xuất một tập hữu hạn phương án có căn cứ, đủ phân xử.
Không liệt kê mọi thuật toán hay triển khai mọi ứng viên trong tài liệu. Với mỗi phương án còn giữ, nêu:
- câu hỏi, bằng chứng xuất phát và phương án đơn giản/đối lập mạnh đã xét;
- nút/cạnh, hướng/kiểu cạnh, nơi đặt từng tín hiệu và scope;
- công thức hoặc pseudocode (mã giả) đủ để người triển khai không phải tự nghĩ lại phần khoa học;
- thông tin giữ/mất/chuyển ở mỗi bước, khả dụng trên dataset offline và FlashTicket;
- giả định, điều kiện thất bại, phản ví dụ và kết quả nào bác phương án;
- code/hợp đồng dùng lại, phần cần đổi hoặc bổ sung và dữ liệu còn thiếu.
Nếu phụ thuộc bài/phương pháp cụ thể, đọc nguồn chính thức và revision liên quan. Không dựng khoảng trống nghiên cứu từ lỗi adapter hoặc bản cài.

3. Làm rõ phần tính toán chung và hợp đồng, không để “lúc code tính tiếp”.
Nêu nguồn nền, phần dùng để chọn/hiệu chỉnh cấu hình và phần đánh giá; xử lý nền tăng/giảm/hằng/trôi/thưa, cadence và mẫu lặp; đơn vị, chuẩn hóa và hợp nhất điểm.
Kiểm log động/đếm trùng và khác biệt log-count/request-count; caller/callee/self-time, span chồng lấn, bất đồng bộ và thiếu span; trị số cực đoan hợp lệ khác lỗi số học.
Nêu hành vi khi không có cạnh, không có bằng chứng, thiếu nền, operation mới; tập quan sát/ứng viên/chấm đúng định nghĩa; hòa/ERROR/UNSUPPORTED và cách tổng hợp.
Tách nhãn đánh giá khỏi đầu vào phương pháp; ánh xạ service/operation/edge; thời điểm event/receive/cắt cửa sổ/xuất kết quả và độ trễ. Không dùng tên ca, đường dẫn nhãn, mốc tiêm hoặc schema suy ra root làm đầu vào. Thiếu kind/link/binding/clock thì ghi yêu cầu quan sát, không đoán kiểu cạnh để lấp chỗ trống.

4. Chỉ rõ cạnh thực sự làm phép tính gì.
Lần thông tin quan hệ từ đầu vào tới điểm và thứ hạng; đối chiếu phương án cùng tín hiệu nhưng không dùng quan hệ theo đúng định nghĩa.
Xét cạnh có giúp gán bằng chứng hay chỉ gom nhiễu/đếm lại/ưu ái bậc hoặc lưu lượng; so với phương án đơn giản không lan truyền.
Không mặc định PageRank hay cơ chế lan truyền chỉ vì task có chữ đồ thị. Phân biệt cây span, graph mức service/operation và quan hệ tĩnh.
Nếu giữ DB/cache/message/resource, nêu chức năng tính toán, dữ liệu và phép phân xử thực sự cần; không thêm nút cho hình vẽ đủ đề tài.

5. Xử lý ranh giới phát hiện và RCA.
Nêu lõi có thể dùng chung. Với phát hiện có đồ thị theo yêu cầu hiện hành và nhánh dùng luật nếu Minh chấp thuận sau này: phân tích phần khác nhau, dữ liệu, hiệu chỉnh, baseline, chi phí đã biết/chưa đo và ảnh hưởng tới mục tiêu.
Không tự dựng hai hệ thống hoàn chỉnh, không chốt đổi hướng trong phiên. Phương án có điều kiện phải giữ đúng điều kiện.

6. Lập ma trận thực nghiệm có khả năng phân xử.
Tách tác dụng thêm tín hiệu khỏi tác dụng quan hệ; gán bằng chứng khỏi chuẩn hóa/hợp nhất; cấu trúc thật khỏi quan hệ ngẫu nhiên phù hợp; bộ xếp hạng khỏi mốc báo động tốt hơn; sửa ca khó khỏi làm hỏng ca đúng.
Baseline phải đủ mạnh và được đối chiếu revision/dữ liệu/chế độ hỗ trợ. Giữ kết quả lịch sử; biến thể sửa hoặc chẩn đoán là nhánh riêng cần được duyệt, không ghi đè.
Mỗi phép so nêu giữ cố định gì, thay gì, đo gì, dự đoán đối lập, kết quả hỗ trợ/bác bỏ/chưa phân xử và kết luận tối đa được phép.
Kiểm tương đương tín hiệu, coverage, cửa sổ, tập ứng viên, tiền xử lý, ngân sách chọn cấu hình và quy tắc chấm ở phần không chủ ý thay. Đồ thị ngẫu nhiên phải giữ/đổi thông tin có chủ đích; kiểm thông tin cấu trúc còn nằm trong đặc trưng/đối chứng.
Chỉ thiết kế trên dev đã được cho phép; test/giữ ngoài dành cho lượt đánh giá được Minh cấp quyền sau khi khóa. Không bỏ nhóm khó hoặc nhóm độc lập với phương án mình thích để kết quả đẹp.

7. Tự thử logic bằng ví dụ nhỏ trong bộ nhớ.
Chọn phản ví dụ sát thiết kế: caller có tín hiệu nhưng callee gây chờ; return nhanh; nền hằng; lưu lượng khác; nút cô lập; operation mới/thiếu nền; span mồ côi hoặc đến muộn; tài nguyên dùng chung khi phương án có dùng nó.
Ghi đầu vào → trung gian → đầu ra dự kiến/thực tế. Chủ động tìm cách làm phương án thất bại. Phát hiện lỗi logic thì tự sửa trong chat và kiểm lại, không xin duyệt từng sửa chữa đó.
Không dùng ví dụ nhỏ để nhận hiệu quả trên dataset thật; không để công thức hay trường hợp biên quan trọng cho người triển khai tự chọn sau.

ĐẦU RA TRONG CHAT, CÓ THỂ DÙNG LÀM CƠ SỞ SOẠN SPEC SAU

A. Kết quả tự rà: nhận định giữ/bác/sửa, bằng chứng và tác động; phân biệt lỗi nguồn với lỗi thiết kế vừa tự sửa.
B. Phần chung, nhánh có điều kiện, yêu cầu còn thiếu và quyết định đang chờ.
C. Bảng phương án còn giữ/loại/tạm hoãn, lý do và điều kiện đổi kết luận.
D. Thiết kế đủ cụ thể: công thức, hợp đồng vào–ra, ánh xạ tín hiệu, ngoại lệ, code dùng lại/thay/bổ sung, dữ liệu còn thiếu.
E. Ví dụ/phản ví dụ, lỗi tìm được, cách tự sửa, kết quả kiểm lại và giới hạn.
F. Baseline/đối chứng, dữ liệu, giao thức, chọn/hiệu chỉnh cấu hình và nội dung cần khóa trước đánh giá.
G. Đối chiếu đủ G2-H01–H26, A–G và yêu cầu đề tài: phần thiết kế xử lý, phần là tính đúng cài đặt, không áp dụng có lý do và OPEN. Không dùng một bảng tên hạn chế thay cơ chế.
H. Thứ tự công việc triển khai tương lai theo phụ thuộc: dùng lại trước, thử gì sớm để có thể bác thiết kế, phần hoãn/bỏ để tránh overengineering. Không ép về số task đã định sẵn.
I. Những điều thật sự cần Minh quyết/cấp quyền, với bằng chứng, phạm vi, chi phí đã biết/chưa đo và kết luận phụ thuộc; không đẩy lại các phép đọc/kiểm nhỏ làm được ngay.

TIÊU CHÍ KẾT THÚC

- Người triển khai đọc kết quả biết phải tính gì và kiểm gì; không còn phải tự phát minh lựa chọn khoa học quan trọng bị bỏ ngỏ.
- Làm hết kiểm nguồn và kiểm logic nhỏ hợp lý trong quyền. OPEN phải cụ thể; không hứa mọi câu hỏi thực nghiệm sẽ hết mở chỉ bằng thiết kế.
- Tự rà lần cuối toàn bộ đề bài, phương án, nguồn phản bác, quyền và khả năng phân xử. Lỗi thuộc quyền thì sửa ngay trong chat rồi kiểm lại, không chỉ liệt kê để phiên sau sửa.
- Không tự chuyển CANDIDATE thành DECIDED, nhận P6 xong hoặc xác nhận lợi ích thực nghiệm từ ví dụ nhỏ.
- Nếu ngữ cảnh bị nén: phục hồi nguồn repo và phần kết quả chat đã có, không viết file checkpoint ngoài quyền, không giảm độ sâu để kết thúc sớm. Nếu cần chuyển phiên, bàn giao đủ phần đã làm/chưa làm.
- Báo bốn mục theo AGENTS; nói rõ không sửa file. Soạn prompt bàn giao theo nguyên văn Prompt chung + khối công đoạn và khối cổng hiện hành trong docs/review-prompt.md, điền trung tính và chỉ quyền trả lời chat; không tự gửi.
- Nếu cần lưu thiết kế, tạo SPEC triển khai hoặc thay nguồn T-041: trình riêng danh sách file và phạm vi để Minh quyết. Không dùng quyền tám file của phiên 1 cho mục đích lưu thiết kế phiên 2.
```

## Prompt Claude soát SPEC sau đồng bộ — chỉ trả lời chat

Minh có thể chuyển prompt này theo mục 9 của AGENTS. Đây là bàn giao phản biện theo mẫu, không phải điều kiện chờ trước khi phiên 1 thực hiện theo Q-183. Không tự gửi hoặc mở phiên.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-041 — D:/RCA-flashticket/tasks/T-041-ra-soat-nen-p3-p5/SPEC.md.
- Công đoạn: soát SPEC.
- Gói/cổng: chuẩn bị P6; trước G3.
- Người làm và người phản biện chính thức: Codex làm; Claude phản biện.
- Tài liệu gốc: D:/RCA-flashticket/tasks/T-041-ra-soat-nen-p3-p5/SPEC.md; LOG.md cùng thư mục; D:/RCA-flashticket/docs/DECISIONS.md; D:/RCA-flashticket/docs/STATE.md; nguồn gốc được SPEC dẫn.
- Phản biện và phản hồi trước: không có bản phản biện chính thức của T-041.
- Code và kết quả liên quan: nguồn code và kết quả liên quan được liệt kê trong SPEC; đầu ra T-041 chưa tạo.
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

### Kết thúc lượt đồng bộ tài liệu — 21/10/2026

1. **Đã làm:** lưu đầy đủ hai prompt hiện hành; đồng bộ nguồn quyền Q-183, SPEC, LOG và trạng thái T-041. Giữ yêu cầu làm sâu, tự rà trước khi tin nguồn thứ cấp, tự sửa trong quyền rồi tiếp tục. Phiên 1 lưu kết quả vào repo; phiên 2 đọc trực tiếp và thiết kế trong chat.
2. **File đã đổi trong lượt:** đúng tasks/T-041-ra-soat-nen-p3-p5/SPEC.md, LOG.md, docs/DECISIONS.md, docs/STATE.md. Không tạo results/T-041/, không chạy task, không commit/push.
3. **Kiểm đã chạy:** đối chiếu đầy đủ phần thay đổi với nội dung dự kiến; hai prompt trên đĩa khớp nguyên khối đã soạn; bảng phạm vi vẫn đúng tám file, bốn đầu ra chưa tạo; khối văn bản và khoảng trắng hợp lệ. Prefix byte của LOG/DECISIONS trước lượt được giữ nguyên; Q-183 chỉ có một dòng. Hash 42 nguồn/code được bảo vệ, HEAD và trạng thái Git ngoài phạm vi không đổi. git diff --check đạt, chỉ có thông báo chuyển dòng LF/CRLF của Git. Đây là kiểm tài liệu/quyền, không phải chạy phép phân tích T-041 hoặc kiểm phương pháp.
4. **Điều chưa chắc/cần Minh quyết:** tài liệu giao việc đã đồng bộ; câu hỏi nghiên cứu T-041/P6 chưa được triển khai hoặc trả lời ở lượt này, thời gian thực tế chưa đo. Quyền tự sửa không bao gồm đổi mục tiêu/tám file, dữ liệu khóa, thực nghiệm mới, chi phí ngoài phạm vi hoặc quyết định phương pháp. Nếu phát hiện cần những việc ấy trong phiên thực hiện, phải nêu bằng chứng/phạm vi/chi phí và quyết định phụ thuộc; không tự loại câu hỏi.

Dấu vết thao tác chưa thành công: một lệnh ghi gộp bị Windows từ chối vì độ dài trước khi chạy; một patch STATE dùng đoạn giữa dòng không khớp nên chưa ghi; một lần dựng lệnh kiểm bị lỗi cú pháp trước khi chạy. Đã sửa cách gửi lệnh/khớp dòng và kiểm lại thành công; không tạo helper hoặc thay file ngoài quyền.

**Bước tiếp theo chính xác:** Minh mở phiên thực hiện, dùng “Prompt 1 hiện hành” tại LOG này. Agent đọc D:/RCA-flashticket/AGENTS.md, docs/STATE.md, tasks/T-041-ra-soat-nen-p3-p5/SPEC.md và mục LOG mới nhất; kiểm Q-183, tự rà/sửa/kiểm lại SPEC trong quyền rồi thực hiện. Không cần duyệt lại từng sửa chữa đã ủy quyền. Chỉ khi có gói đầu ra thật/hợp lệ mới dùng “Prompt 2 hiện hành”; không yêu cầu copy báo cáo chat. Prompt Claude soát SPEC ở trên để Minh tùy chọn chuyển, không là điều kiện chờ thực hiện.

**Lệnh cuối cùng của lượt:** git diff --check, chạy tại D:/RCA-flashticket sau khi nối mục kết thúc này. Trạng thái bàn giao: tài liệu đã đồng bộ, T-041 chưa triển khai.

## Phiên thực hiện T-041 — 2026-10-21T00:36:30.402475+07:00

Codex; thiết bị Windows tại D:/RCA-flashticket; vai trò người làm. Phân loại EXECUTE. Quyền mới Q-184; tự rà/sửa SPEC rồi thực hiện trong đúng tám file, không thay phản biện Claude. Chưa có bốn đầu ra khi mở phiên. Thay đổi cục bộ có trước được giữ nguyên.

### Quyết định của Minh trong phiên — nguyên lời giao

```text
Tôi là Minh. Tôi giao Codex tự rà SPEC, sửa các lỗi trong phạm vi được ủy quyền rồi thực hiện T-041 tại D:/RCA-flashticket.

Đây là chỉ đạo mới thay cho trạng thái “chờ duyệt thực hiện” trong SPEC/LOG trước đó. Không yêu cầu tôi duyệt lại từng sửa chữa SPEC thuộc đúng phạm vi dưới đây. Không dừng sau khi chỉ báo lỗi hoặc lập kế hoạch.

QUYỀN ĐƯỢC GIAO

1. Đọc nguồn gốc, tự rà và phản biện SPEC T-041 trước khi triển khai.
2. Nếu phát hiện lỗi, thiếu sót hoặc mâu thuẫn trong SPEC đối với mục tiêu T-041 đã giao, tự sửa SPEC cho đúng, ghi rõ bằng chứng và ảnh hưởng, kiểm lại rồi triển khai.
3. Quyền tự sửa gồm: làm rõ câu hỏi, sửa đường dẫn/phiên bản, sửa lập luận hoặc tiêu chí chưa đúng, bổ sung phần kiểm cần thiết trong phạm vi phân tích đã giao, sửa thứ tự phụ thuộc và điều kiện bàn giao.
4. Giữ nguyên mục tiêu: rà sâu nền P3/P5, dùng code và trung gian đã có để chuẩn bị đầu vào thiết kế RCA. Không tự biến T-041 thành task cài phương pháp hoặc chạy thực nghiệm mới.
5. Không được tự mở rộng số file, mở test/giữ ngoài, thay mục tiêu nghiên cứu, chọn hướng Grafana thay MRP, sửa code/baseline cũ, chạy thao tác tốn kém hoặc ghi hệ thống ngoài. Khi thật sự cần vượt ranh giới này, dừng đúng phần phụ thuộc và trình tôi; tiếp tục phần độc lập.
6. Đây là tự soát của người làm, không thay phản biện chính thức của Claude. Không phải chờ Claude phản biện SPEC mới được thực hiện theo quyền tôi giao trong prompt này.

GHI NHẬN QUYỀN MỚI TRƯỚC KHI LÀM

- Đọc quyết định hiện hành, giữ nguyên lịch sử Q-182 và các mục LOG cũ.
- Trong đúng gói tám file đã được giao, nối một mục DECISIONS ghi đúng chỉ đạo mới trong prompt này, dùng mã kế tiếp sau khi kiểm sổ; không ghi thêm quyết định nghiên cứu chưa được tôi chọn.
- Nối LOG ghi nguyên lời giao, thời điểm, phạm vi tự sửa và thực hiện.
- Sau đó cập nhật điều kiện bắt đầu/trạng thái của SPEC và thông tin T-041 trong STATE cho khớp quyền mới.
- Không viết rằng tôi đã duyệt từng lựa chọn khoa học hoặc xác nhận hiệu quả phương pháp. Đây là ủy quyền tự rà, sửa SPEC trong phạm vi và thực hiện phân tích.

TÁM FILE ĐƯỢC GHI

1. D:/RCA-flashticket/tasks/T-041-ra-soat-nen-p3-p5/SPEC.md
2. D:/RCA-flashticket/tasks/T-041-ra-soat-nen-p3-p5/LOG.md
3. D:/RCA-flashticket/results/T-041/bao-cao.md
4. D:/RCA-flashticket/results/T-041/bang-chung.jsonl
5. D:/RCA-flashticket/results/T-041/ban-giao-phien-2.md
6. D:/RCA-flashticket/results/T-041/manifest.json
7. D:/RCA-flashticket/docs/DECISIONS.md
8. D:/RCA-flashticket/docs/STATE.md

LOG và bằng chứng chỉ ghi thêm, giữ lượt lỗi. DECISIONS chỉ nối chỉ đạo được giao, không sửa lịch sử. STATE chỉ cập nhật thông tin T-041; không tự đổi cổng hoặc nghiệm thu task.

Không tạo file phụ, scripts/, runs/, cache hoặc file tạm ngoài danh sách. Phép kiểm nhỏ chạy inline hoặc trong bộ nhớ, ghi lệnh và kết quả vào bang-chung.jsonl. Cần thêm file phải trình phạm vi mới.

BƯỚC ĐẦU: TỰ RÀ THỰC CHẤT

Đọc AGENTS và nguồn yêu cầu, tự xác định mục tiêu, quyền hạn, bằng chứng cần có và điều kiện xong. Sau đó đối chiếu SPEC. Không lấy SPEC, tóm tắt LOG, kết luận G2 hoặc nhận xét của agent trước làm chân lý.

Phải tự hỏi:
- Đề bài có trả lời đúng DT18/MRP và nhu cầu thiết kế P6 không?
- Có đang coi ứng viên hoặc giả thuyết là điều đã xác nhận?
- Có bỏ nhóm quan trọng, phép kiểm hoặc nguồn phản bác chỉ để khép phạm vi?
- Code và trung gian thật có hỗ trợ cách làm được SPEC mô tả không?
- Có yêu cầu vượt quyền, nguồn mâu thuẫn, tiêu chí chỉ kiểm đủ file hoặc giả định không kiểm được?
- Có việc lặp lại hoặc hạ tầng không cần cho câu hỏi?
- Có thể hoàn thành đầu ra bằng quyền và dữ liệu hiện có tới mức nào?

Lập bảng tự soát gồm: vấn đề → nguồn/bằng chứng → hệ quả → sửa hoặc giữ nguyên có lý do.

Với lỗi trong quyền: tự sửa SPEC, ghi đoạn cũ/mới hoặc mô tả đủ tái hiện, lý do và phạm vi tác động vào LOG; kiểm lại bản sửa rồi tiếp tục. Không chỉ ghi “đề xuất sửa” và dừng chờ tôi.

Nếu thấy SPEC hợp lý, nói rõ phần đã kiểm và bằng chứng; không cần tìm lỗi cho đủ số lượng.

NGUỒN PHẢI ĐỌC

- D:/RCA-flashticket/AGENTS.md
- D:/RCA-flashticket/docs/STATE.md
- D:/RCA-flashticket/tasks/T-041-ra-soat-nen-p3-p5/SPEC.md
- D:/RCA-flashticket/tasks/T-041-ra-soat-nen-p3-p5/LOG.md
- D:/RCA-flashticket/docs/DECISIONS.md
- D:/RCA-flashticket/docs/MRP.md
- D:/RCA-flashticket/docs/WHY.md
- D:/RCA-flashticket/docs/LESSONS.md
- D:/RCA-flashticket/docs/PLAN-P6.md
- D:/RCA-flashticket/docs/DE-XUAT-HUONG-GRAFANA-RCA.md
- D:/RCA-flashticket/docs/reference/sources/DT18-de-tai-va-nhiem-vu.md
- D:/RCA-flashticket/docs/reference/sources/advisor-2026-09-23.md
- D:/RCA-flashticket/results/T-034/goi-g2.md
- D:/RCA-flashticket/results/T-034/ban-do-g2.json
- D:/RCA-flashticket/results/T-035/dac-ta-do-thi.md
- Hợp đồng T-036 hiện hành, xác định từ LOG và manifest của task.
- D:/RCA-flashticket/results/T-040/ban-giao-p6.md
- D:/RCA-flashticket/results/T-040/yeu-cau-quan-sat-p9.md
- D:/RCA-flashticket/src/p3/
- D:/RCA-flashticket/src/do_thi/
- D:/RCA-flashticket/src/do_thi_tinh/

Đọc tiếp code nguồn phương pháp, fixture, trung gian, SPEC và LOG task nguồn theo phụ thuộc thật. Trước dùng đầu ra cũ phải kiểm hash theo manifest phù hợp. Nếu lệch, ghi lại và dừng kết luận phụ thuộc; không tự hợp thức hóa bằng manifest mới.

Không đọc D:/Project/flash-ticket-rca-research, kể cả khi tài liệu cũ có link tới đó. Không mở dữ liệu khóa hoặc test ở bất kỳ thư mục nào. Dữ liệu/trung gian dev chỉ đọc sau khi xác minh miền được phép.

NỘI DUNG PHẢI PHÂN TÍCH SÂU

1. Dựng đường xử lý thật:
nguồn → selector/adapter → cửa sổ/nền → trace/log/metric → graph/đặc trưng → điểm → tập ứng viên → thứ hạng → evaluator.

Chỉ file, hàm/lớp, kiểu đầu vào–đầu ra, đường gọi và trung gian. Tách dataset, biết mốc/tự phát hiện, code chung/riêng, nhãn/phương pháp và graph tĩnh/quan sát/cây span.

2. Kiểm khả năng dùng lại:
- timestamp, đơn vị, biên cửa sổ, span kết thúc, thời điểm dữ liệu khả dụng;
- chọn cột, missing/fill, nền hằng/thưa/trôi, cadence và hàng lặp;
- alias, service/operation/resource scope;
- parent/link, mất cha, trùng span, chồng lấn, kind và quan hệ chưa phân kiểu;
- khóa nối log, trường động, mẫu log, đếm trùng;
- tập mô hình/quan sát/chấm/trả về;
- số học, cực trị, hòa, ERROR/UNSUPPORTED, nhánh dự phòng;
- runner, cache, revision và điều kiện dùng lại kết quả.

Không kết luận “dùng lại được” chỉ vì module đã có hoặc chạy không lỗi.

3. Lần cơ chế:
Với nhóm quan trọng, đọc cả ca sai và ca đúng có điều kiện tương ứng; giải thích cách chọn và mở rộng khi có phản ví dụ.

Mỗi kết luận quan trọng cần:
đầu vào cụ thể → dòng/hàm xử lý → giá trị/trạng thái trung gian → đầu ra.

Kết luận cơ chế phải chỉ điều kiện X, bước Y và thông tin Z bị mất/chấm sai. Nếu chỉ có quan sát hoặc liên hệ, giữ đúng mức ấy. Không dùng cờ, tên thuật toán hoặc số tổng thay chuỗi bằng chứng.

4. Làm rõ đầu vào cho P6:
- Graph gộp P5 giữ/mất thông tin request và thời gian nào?
- Phân bổ owner–caller–callee cần span gốc hay trung gian hiện có?
- Phép nào chỉ cần quan hệ span quan sát; phép nào đòi kiểu/ngữ nghĩa đã xác minh?
- Lõi offline/online chung được tới đâu về ngữ nghĩa?
- Gộp/chấm thao tác lên service thế nào khi nhãn chỉ có service?
- Thiếu tín hiệu/cạnh/nền biểu diễn thế nào mà không bịa điểm?
- Thông tin nào Collector chuyển được, thông tin nào phải ghi từ instrumentation/giao thức thực nghiệm?

5. Bao phủ đầy đủ:
Kiểm G2-H01–H26, yêu cầu DT18/MRP và bảy nhóm:
A vị trí bằng chứng; B biểu diễn tín hiệu; C nền/thang/gộp; D vai trò quan hệ; E tập ứng viên/thiếu bằng chứng; F mốc và phát hiện; G quan hệ ngoài lời gọi/schema.

Không ép mọi hạn chế thành một thuật toán. Phân biệt căn cứ sửa hạn chế, đáp ứng đề tài và nhu cầu kỹ thuật. Khi nhận định phụ thuộc bản cài khác bài gốc, đọc nguồn chính thức đúng revision; không biến lỗi thư viện thành khoảng trống chung của phương pháp.

ĐƯỢC KIỂM GÌ

Được chạy lệnh chỉ đọc, kiểm hash và tính nhỏ trong bộ nhớ có mục đích. Trước khi gọi code phải xét tác dụng phụ; Python dùng -B. Không tự chạy test/runner tạo file ngoài quyền, ma trận baseline, thử ứng viên mới trên dữ liệu thật, SSH/bật EC2, tải dữ liệu, cài môi trường hoặc triển khai Grafana.

Tra hẹp nguồn chính thức khi kết luận phụ thuộc; không mở deep research. Không commit/push hoặc tự mở phiên/subagent/gửi prompt sang agent khác.

LƯU ĐẦU RA TRONG QUÁ TRÌNH

- bao-cao.md: bản đồ xử lý; bảng dùng lại tới hàm/hợp đồng; đủ G2-H01–H26; chuỗi bằng chứng, phản ví dụ; hợp đồng tối thiểu; phần cần bổ sung.
- bang-chung.jsonl: ghi nối tiếp ID, thời điểm, câu hỏi, lệnh/phép tính, đầu vào, nguồn/JSON pointer, kết quả và lỗi; giữ mọi lần thử.
- ban-giao-phien-2.md: trạng thái thật, thứ tự đọc, hợp đồng đã xác minh, kết luận có điều kiện, phần thiếu, quyết định phụ thuộc và bước tiếp; trỏ bằng chứng để agent khác không cần lịch sử chat.
- manifest.json: revision và nguồn thực sự dùng, kết quả kiểm hash, hash ba file kết quả và SPEC; không tự băm manifest hoặc coi LOG/STATE/DECISIONS đang đổi là đầu ra bất biến.
- LOG: mở phiên, tự soát/sửa SPEC, tiến độ sau bước con, checkpoint, kết thúc và prompt bàn giao.

TIÊU CHÍ KẾT THÚC

Làm hết phần đọc/kiểm hợp lý trong quyền. Không để “phiên sau đọc code/trung gian đang có” vì dừng ở mô tả.

Mọi phần còn mở phải phân biệt:
- chưa kiểm;
- file có nguồn nhưng chưa tiếp cận;
- thiếu đầu vào chưa từng được ghi;
- cần thực nghiệm mới;
- cần Minh quyết.

Mỗi phần có bằng chứng thiếu, phép phân xử, phạm vi, chi phí đã biết/chưa đo và quyết định bị ảnh hưởng. Thiếu quyền chạy không xóa nghĩa vụ nghiên cứu và không chặn phần độc lập.

Tự kiểm lại toàn bộ kết luận với nguồn phản bác, liên kết, JSONL, manifest và diff. Nếu thấy lỗi trong SPEC/đầu ra do mình làm thuộc quyền, sửa và kiểm lại ngay. Không nhận là đã chứng minh hiệu quả RCA hoặc hoàn thành P6.

Sau nén ngữ cảnh, khôi phục nguồn và tiến độ; không tự giảm chiều sâu. Khi thực sự cần chuyển phiên, ghi checkpoint đủ để tiếp tục vào LOG/báo cáo trong quyền.

Cuối phiên báo bốn mục theo AGENTS, ghi bước tiếp và lệnh cuối; cập nhật trạng thái T-041 đúng thực tế, chưa tự nghiệm thu. Soạn prompt Claude phản biện kết quả theo đúng mẫu hiện hành, chỉ điền thông tin trung tính; không tự gửi.

Phiên 2 phải đọc trực tiếp gói D:/RCA-flashticket/results/T-041/, không yêu cầu Minh copy báo cáo chat.
```

### Mở phiên

Đã đọc AGENTS, STATE, SPEC và mục cuối LOG, Q-182–Q-183; kiểm sổ tới Q-183 rồi nối Q-184. Đây là chỉ đạo EXECUTE mới, không coi quyền lịch sử là quyết định khoa học. Bước tiếp: đọc nguồn yêu cầu và manifest hiện hành, tự rà SPEC, lưu bảng bằng chứng rồi sửa/kiểm lại trong quyền.

### Tự rà/sửa SPEC — 2026-10-21T00:40:41.876854+07:00

Bảng đầy đủ S01–S07 ở bao-cao.md §2/E004. Cũ → mới: trạng thái chỉ đồng bộ/chưa chạy → đang thực hiện Q-184; hợp đồng T036 theo LOG chung → pin SMTP V2 và artifact-manifest cụ thể; kiểm cửa sổ chung → phân biệt event/end/arrival và duplicate/lossiness khi dùng graph. Bổ sung OPEN theo loại/owner/phép phân xử/chi phí. Lý do: tránh dùng root R1 với code V2, tránh coi endTime là arrival hoặc graph gộp là span baseline. Không đổi mục tiêu/danh sách file/nghiên cứu, không thêm lựa chọn khoa học. Kiểm lại bản sửa khớp Q-184 và nguồn.

Hash đầu vào E002:1112 mục khớp; E003:47 mục khớp. Không có lệch/mất ở miền đã kiểm. Tiếp: lần phương pháp, trung gian/cặp đúng-sai, kiểm logic nhỏ thuần bộ nhớ và hợp nhất H01–H26. Các lỗi lệnh đã giữ E002/E003.

### Tiến độ code/trung gian — 2026-10-21T00:50:10.724883+07:00

Đã lưu báo cáo §3–4: đường gọi và bảng dùng lại tới API. E005:39 hash baseline code/dependency khớp; E007:55 kiểm bảng đơn vị/trung gian/bản ghi khớp; E008:11 nguồn supplemental khớp. E006 có các cặp theo điều kiện, đã mở rộng native OK cho MicroRank/TraceRCA. E009 đọc12 CSV trace đúng allowlist4 ca return (không test), tính mô tả theo operation trong cửa sổ S1 đã lưu, tổng mẫu khớp trung gian ở mọi cửa sổ. Hướng duration trộn trong cùng ca; chưa quy nguyên nhân vật lý. E010 giữ lỗi harness thiếu Path sau13 kiểm; E011 sửa namespace,17 kiểm nhỏ đạt. Không gọi runner hoặc baseline trên dữ liệu thật. Đã đọc hẹp3 nguồn code chính thức đúng revision; không deep research. Tiếp: hoàn thiện chuỗi cơ chế, đối chiếu H01–H26/A–G, hợp đồng tối thiểu/OPEN rồi kiểm toàn gói.

### Checkpoint và hoàn thiện chuỗi — 2026-10-21T01:06:29.063683+07:00

Đã khôi phục sau nén từ LOG, báo cáo và E020; giữ nguyên mục tiêu/quyền Q-184, không giảm phần kiểm. E012–E017 giữ nguồn chính thức, code catalog, công thức, nguồn đính chính và lỗi nguồn N-Sigma đúng mức. E018 giữ lỗi descriptor return; E019 giữ lỗi môi trường thiếu parquet engine; E020 dùng môi trường T014-main đã có, đọc ba native capture MicroRank, 82 hash file và 54 dense-byte hash/finite khớp. Đã bổ sung chuỗi weights→coverage→ef/nf/ep→DStar2 và ca đúng vào báo cáo §5.3; O05 không còn giao phiên sau đọc lại ba capture này. SPEC đồng bộ các tham chiếu quyền thực hiện hiện hành sang Q-184, giữ đoạn lịch sử Q-183; không đổi mục tiêu/file/phương pháp.

Đang có E001–E020 nối tiếp; báo cáo đủ §1–9, H01–H26/A–G và O01–O12. Tiếp: tạo bàn giao phiên2, manifest nguồn thực dùng; tự kiểm pointer/liên kết/phạm vi/diff; nối prompt Claude đúng mẫu và kết phiên. Không mở nguồn raw O01 khác hash, test, runner hay phiên khác.

## Prompt Claude phản biện kết quả — chỉ trả lời chat

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-041, D:/RCA-flashticket/tasks/T-041-ra-soat-nen-p3-p5/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: chuẩn bị P6 từ nền P3/P5; trước G3.
- Người làm và người phản biện chính thức: Codex là người làm; Claude là người phản biện chính thức.
- Tài liệu gốc: tasks/T-041-ra-soat-nen-p3-p5/SPEC.md và LOG.md; docs/MRP.md, PLAN-P6.md, DE-XUAT-HUONG-GRAFANA-RCA.md; results/T-034/; results/T-035/; results/T-036/runs/doi-chieu-smtp-001/; results/T-040/; git diff từ commit 488013070e56342b74ff0f2ccbc6524bcfb8d550, cộng file chưa theo dõi trong gói T-041.
- Phản biện và phản hồi trước: chưa có lượt phản biện kết quả chính thức của T-041; lịch sử chuẩn bị SPEC và prompt tại LOG.md của task.
- Code và kết quả liên quan: src/p3/, src/do_thi/, src/do_thi_tinh/; các nguồn phương pháp/trung gian được dẫn trong results/T-041/bao-cao.md và bang-chung.jsonl; results/T-041/manifest.json; results/T-041/ban-giao-phien-2.md. Revision và môi trường/lệnh kiểm tại manifest và evidence. Python dùng -B.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; không tạo hoặc sửa file.

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

## Kết thúc phiên thực hiện — 2026-10-21T01:12:12.653402+07:00 — Codex

1. **Đã làm:** tự rà nguồn và SPEC, sửa trong quyền Q-184, kiểm lại rồi thực hiện đủ phần rà nền P3/P5. Bốn đầu ra có bản đồ/API dùng lại, chuỗi vào→xử lý→trung gian→ra và phản ví dụ, đủ H01–H26/A–G, hợp đồng thông tin tối thiểu, OPEN phân loại/owner/chi phí/phép phân xử và bàn giao phiên2. Ghi Q-184 đúng chỉ đạo Minh; không thêm quyết định khoa học, chọn Grafana hoặc công thức P6. Nền RQ2 được làm rõ; không khép RQ2/RQ3/RQ5, P6/G3 hoặc lợi ích RCA.
2. **File thay đổi trong phiên, đúng tám file:** tasks/T-041-ra-soat-nen-p3-p5/SPEC.md; LOG.md cùng thư mục; results/T-041/bao-cao.md, bang-chung.jsonl, ban-giao-phien-2.md, manifest.json; docs/DECISIONS.md; docs/STATE.md. LOG, DECISIONS, JSONL chỉ nối. Không sửa code/baseline/nguồn task cũ, không tạo helper/cache/temp, không commit/push. Thay đổi người dùng đã có ở đầu phiên giữ nguyên.
3. **Kiểm và kết quả:** E022 băm lại1.280 đường dẫn từ các nguồn đã dùng:1.279 PASS, một MISSING đúng O01, không MISMATCH. 17 kiểm synthetic E011 đạt;16 tổng mẫu operation-duration của bốn ca/bốn cửa sổ khớp E009;54 mảng native MicroRank khớp dense hash và finite,8 điểm DStar2 tính lại khớp E020. Đủ26 H/7 nhóm/12 OPEN; JSONL parse và ID/tham chiếu hợp lệ; source-code catalog không đổi. Prefix byte của LOG/DECISIONS so hash trước phiên đạt, HEAD và Git status ngoài tám file giữ nguyên. Diff tracked đã đọc, diff-check đạt; có cảnh báo chuyển LF/CRLF khi Git chạm DECISIONS, không thay byte lịch sử trong phiên này. Manifest/bốn hash đích kiểm sau ghi cuối theo E023. Giữ mọi lỗi/thử, không chạy baseline hoặc toàn test suite.
4. **Còn mở/cần Minh:** chờ Claude phản biện kết quả theo prompt ngay trên, quyền chỉ trả lời chat; Minh quyết xử lý/nghiệm thu, không tự đóng task. O01: context N-Sigma đúng byte thiếu, bản checkpoint khác hash không dùng; chặn kiểm lại raw ca đó, summary đúng hash vẫn chỉ là mô tả. O02/O03/O07 thiếu thời điểm nhận/ngữ nghĩa/nhãn vận hành độc lập; O04/O05/O08/O10/O11 cần giả thuyết/can thiệp mới nếu lựa chọn phụ thuộc; O06 đã có mô tả operation nhưng chưa đánh giá feature; O09/O12 cần quyết định về nhóm lan/hướng P6 từ Minh/cô. Chi tiết evidence, phép phân xử, chi phí đã biết/chưa đo và phụ thuộc ở báo cáo §8; không còn giao lại việc đọc chung code/trung gian đã làm.

**Bước tiếp chính xác:** Minh chuyển nguyên khối “Prompt Claude phản biện kết quả — chỉ trả lời chat” ở trên; phiên nhận đọc AGENTS→STATE→SPEC/mục cuối LOG→results/T-041/manifest.json và kiểm outputs→bao-cao.md/ban-giao-phien-2.md/evidence, rồi các nguồn trực tiếp. Không tự gửi hoặc mở phiên. Khi Minh giao phiên2, dùng Prompt2 hiện hành và đọc gói trực tiếp, thiết kế trong chat; quyền ghi riêng chưa có. Nội dung nên đưa vào tài liệu phương pháp chính thức sau khi Minh chọn hướng: hợp đồng thời gian/quan hệ/tín hiệu/nền/tập ứng viên và các giới hạn quan sát ở báo cáo §7–8; hiện chưa ghi WHY/MRP.

**Lệnh cuối của phiên:** `py -3 -X utf8 -B -` — kiểm kết thúc inline được lưu trong E023 (ID/nguồn hash/prompt/prefix/phạm vi/diff/đầu ra), cập nhật hash bang-chung.jsonl trong manifest sau khi nối E023 rồi xác nhận lại bốn đích. Không ghi file ngoài tám file.

**Commit đề nghị khi Minh yêu cầu:** `T-041: rà nền P3/P5 và bàn giao đầu vào thiết kế RCA`. Chưa commit/push.

## Mở lượt đáp và sửa phản biện — 2026-10-23T15:53:02+07:00 — Codex

- Thiết bị: LeVanMinh, Windows; repo D:/RCA-flashticket. Vai trò giữ nguyên: Codex người làm, Claude người phản biện chính thức. Loại việc EXECUTE trong đúng gói bảy file Minh vừa duyệt, Q-185.
- Lời Minh: **“duyệt sửa luôn trong lượt này”**. Phạm vi là đề xuất bảy file ngay trước lời duyệt; không sửa SPEC hoặc nguồn cũ, không chạy thực nghiệm mới, không tự nghiệm thu. Đã ghi lời duyệt vào DECISIONS trước khi sửa đầu ra.
- Lượt đáp chỉ đọc trước đó: đã nhận cùng tệp có cả kết luận Claude và prompt, nên đã thấy phản biện khi đọc yêu cầu; không gọi phần tự soát sau đó là lượt mù. Chưa sửa file trong lượt chỉ đọc. Có khởi tạo một subagent hỗ trợ đọc trước khi đọc tới lệnh cấm trong SPEC; đã báo Minh và dừng ngay. Không giao vai trò phản biện chính thức, không dùng kết quả hỗ trợ, không phát sinh sửa file từ lượt hỗ trợ. Lượt sửa này không mở subagent/phiên hoặc gửi prompt.
- Điểm tự soát trên đầu ra gốc sau khi nhận yêu cầu: thiếu so cùng operation giữa hai ca MicroRank và thiếu bảng tương thích cửa sổ/biểu diễn Grafana. Các điểm này trùng phần Claude nêu; không nhận là phát hiện độc lập trước khi đọc phản biện. Các kiểm mới sẽ nối E024 trở đi; E001–E023 và LOG cũ giữ nguyên byte.
- Bắt đầu: bốn hash outputs trong manifest cũ khớp; nguồn và quyền đã đối chiếu, HEAD giữ nguyên. Snapshot trước sửa ở bộ nhớ cho diff; hash ban đầu và nguyên văn phản biện đính kèm được giữ trong bằng chứng để phiên khác truy được mà không cần tệp ở máy này.

### Các bước sửa đã thực hiện

1. E025 kiểm lại summary đúng pin và đủ 67 đường dẫn: N-Sigma 27 tăng/3 giảm, std0 trigger cells ở 29 ca; 5 nguồn PASS/62 thiếu theo ba loại. Giữ E022 như kết quả lịch sử, không đổi nguồn để hợp thức hóa.
2. E026 kiểm J0→closed→capture, tính DStar2 đúng biểu thức cho 152/149 operation, khớp toàn bộ điểm lưu; bổ sung station/find giữa hai ca khác ô và hai ca TraceRCA cùng ô, phân tầng loại lỗi. Không chạy PageRank/phương pháp.
3. E027 đối chiếu T-008 với Git đã commit, cộng lại số log-join OB khớp; kiểm một header dev đúng hash có ID và code P3 bỏ ID khỏi bảng lõi. Bổ sung bảng tương thích Grafana, giữ tỷ lệ ghép dev/nguồn điều kiện chờ M1 OPEN. Không tái kiểm raw toàn bộ.
4. Đã sửa bao-cao.md, ban-giao-phien-2.md và đúng một dòng T-041 của STATE; E028 giữ cũ→mới và diff trong bộ nhớ. Đang tự kiểm nội dung/phạm vi/manifest; không sửa SPEC, nguồn cũ hoặc câu chờ M1 ở phần khác của STATE.

### Phản hồi của người làm và kết quả sửa theo Q-185

| Điểm | Kết luận của Codex sau kiểm nguồn | Phần đã sửa và bằng chứng | Phạm vi kết luận còn giữ |
|---|---|---|---|
| R1 | Đúng một phần: thiếu phân bố/std0 và kiểm kê nguồn; số reviewer 61/67 và vị trí stderr cần đính chính | Báo cáo §5.8/H22/O01/§9 và bàn giao dùng 27 tăng/3 giảm, std0 trigger ở 29 ca; 62/67 đường dẫn thiếu (29 context/29 graph/4 theta); dấu vết EC2 ở stdout/timer. E025 giữ đủ danh sách. E022 không đổi | Hai hướng không sai số học nhưng không thay phân bố toàn cohort; std0 chưa là nguyên nhân chính. Chưa biết nguồn còn trên EC2; không gọi 62 file là 62 context hoặc mọi kết luận cùng bị chặn |
| R2 | Đúng về thiếu đối chiếu; chuỗi tính chung đã xác minh không tự thành cơ chế riêng ca sai | Báo cáo §5.1–5.3/H01/H02/H04/O05 và bàn giao ghi cặp MicroRank khác ô; thêm station/find, hai đối chứng TraceRCA cùng ô và đủ loại lỗi. E026; thêm rõ 26 OK và 4 ERROR giữ trong mẫu số chung | Coverage, weights, nhóm trace và ô lỗi cùng khác; chưa cô lập PageRank. Ca cùng ô TraceRCA giữ 1→1 không xóa phản ví dụ khác ô; không chọn ratio như sửa chung |
| R3 | Đúng về mất thông tin ở adapter/bàn giao; không gọi nguồn công khai thiếu ID | Báo cáo §3.1/§4/H19/§7/O07 và bàn giao giữ nguồn T-008, header dev đúng hash và yêu cầu adapter P6 giữ ID/provenance. E027 phân biệt Git snapshot của kết quả T-008 với manifest tải nguồn | Số theo file phút T-008 không thay tỷ lệ ghép dev. Chưa tái kiểm raw toàn bộ, chưa xác nhận liên kết dev/outcome/onset; không sửa adapter P3 |
| R4 | Đúng: bàn giao trước chỉ nêu khác biệt ở mức khái quát | Bàn giao §2 thêm bảng bốn dòng: nền, histogram/duration, luật cảnh báo/nghĩa hẹp, cùng lõi offline/online; báo cáo §7/O12 dẫn bảng. E027 | Không suy toàn dataset thiếu lịch sử dài; không chọn cửa sổ, cơ chế hoặc thay MRP/WHY-02/Grafana. Chưa có triển khai P6 |

Bốn điểm KHÔNG CHẶN việc dùng lại phần nền đã kiểm với đúng giới hạn; phần dùng để quy cơ chế hoặc triển khai đề xuất chỉ được dùng theo nội dung đã sửa, không coi chính việc kiểm số là bằng chứng khoa học mới. Sửa xong không thay quyền nghiệm thu của Minh. Giữ nguyên phản biện Claude trong E024, không sửa lời reviewer hoặc tạo REVIEW thay Claude.

**Nguồn câu chờ M1:** git log -S chỉ ra câu “chờ ý kiến cô qua chương 5…” có từ bản STATE trước T-041. Chưa tìm xác nhận nguyên lời tương ứng trong DECISIONS; E027 giữ dấu vết. Đây là OPEN về nguồn/ý nghĩa điều kiện chờ; Q-185 không được suy thành quyết định đặt/gỡ điều kiện. Chỉ sửa dòng T-041, không sửa câu chờ ở phần khác STATE.

### Kết thúc lượt sửa — 23/10/2026 — Codex

1. **Đã làm:** hoàn thành gói sửa văn bản/bằng chứng/bàn giao R1–R4 đúng Q-185. Đã giữ phân bố đủ ca, đối chiếu cùng operation/cùng ô và bằng chứng bất lợi, tách mất ID ở adapter khỏi thiếu nguồn, nêu tương thích Grafana cụ thể. T-041 đạt phần đính chính được giao; nền RQ2 được làm rõ nhưng chưa phân xử nguyên nhân thống kê N-Sigma, tác dụng riêng PageRank, liên kết log-span dev hoặc lợi ích phương pháp.
2. **File thay đổi, đúng bảy:** docs/DECISIONS.md; docs/STATE.md (chỉ dòng T-041); tasks/T-041-ra-soat-nen-p3-p5/LOG.md; results/T-041/bao-cao.md, ban-giao-phien-2.md, bang-chung.jsonl, manifest.json. DECISIONS/LOG/JSONL chỉ nối; SPEC, code/baseline, nguồn task cũ và thay đổi người dùng ngoài gói giữ nguyên. Không commit/push.
3. **Kiểm và kết quả:** E025–E027 giữ phép đọc/tính và pin cụ thể; E028 giữ diff/cũ→mới; E029 có 27 kiểm đạt, gồm số, mức kết luận, 26 H/12 OPEN, bảng Markdown, prefix chỉ nối, nguồn luật/SPEC không đổi, đúng một dòng STATE, Git ngoài quyền/HEAD giữ nguyên và prompt theo mẫu. Toàn bộ điểm DStar2 152/149 operation khớp; không chạy lại PageRank hoặc phương pháp. Kiểm cuối E030 đối chiếu gói thật, manifest/bốn outputs, nguồn được dùng và diff; hash JSONL trong manifest được cập nhật sau khi nối E030 rồi kiểm lại, không tự băm manifest hoặc LOG/STATE/DECISIONS.
4. **Còn mở/cần Minh:** Claude chưa kiểm lại bản sửa, Minh chưa nghiệm thu. Nguồn context/graph/theta còn thiếu theo E025; khả năng tiếp cận EC2 và chi phí chưa đo. Std0, yếu tố MicroRank, ánh xạ dev và hướng P6 vẫn như OPEN trong báo cáo; thiếu đúng phép cô lập/nguồn và quyết định phụ thuộc được ghi tại O01/O05/O07/O12. Không đóng RQ2/RQ3/RQ5/G3 hoặc mở test. Nội dung hợp đồng/biểu diễn/timing/ID cần đưa vào tài liệu phương pháp chính thức sau khi thiết kế được Minh chọn; chưa ghi thay vào WHY/MRP.

**Đề xuất phản biện:** phía Codex không còn phản đối chưa xử lý đối với gói sửa và đề xuất dừng phản biện gói này; Claude chưa kiểm lại nên chưa nhận là hai bên thống nhất. Minh chọn dừng, gửi prompt kiểm lại bên dưới, hoặc yêu cầu xử lý tiếp. Không tự nghiệm thu hoặc đóng task.

**Bước tiếp chính xác:** Minh chuyển nguyên prompt cuối mục này nếu muốn Claude kiểm lại; phiên nhận đọc AGENTS→STATE→SPEC/mục cuối LOG→manifest outputs→bao-cao/bàn giao→E024 nguyên văn phản biện→E025–E030 và nguồn trực tiếp. Quyền reviewer hiện chỉ đọc/trả lời chat, không tự tạo REVIEW. Khi Minh giao thiết kế, dùng Prompt 2 hiện hành và gói đã sửa; chưa ghi thiết kế vào repo.

**Lệnh cuối của lượt:** Node REPL dùng fs.readFile/crypto SHA256 và git status/diff chỉ đọc; mã kết thúc E030 kiểm phạm vi/prefix/nguồn/JSONL/prompt/manifest, sau đó cập nhật hash JSONL và kiểm lại bốn outputs. Các phép Python chỉ dùng difflib/json trong bộ nhớ với -B; không helper/cache/tạm hoặc test suite.

**Commit đề nghị nếu Minh yêu cầu:** `T-041: sửa căn cứ và bàn giao sau phản biện`. Chưa commit/push.

### Prompt Claude kiểm lại phản hồi và sửa — chỉ trả lời chat

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-041, D:/RCA-flashticket/tasks/T-041-ra-soat-nen-p3-p5/SPEC.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: chuẩn bị P6 từ nền P3/P5; trước G3.
- Người làm và người phản biện chính thức: Codex là người làm; Claude là người phản biện chính thức.
- Tài liệu gốc: tasks/T-041-ra-soat-nen-p3-p5/SPEC.md và LOG.md; docs/MRP.md, PLAN-P6.md, DE-XUAT-HUONG-GRAFANA-RCA.md; results/T-034/; results/T-035/; results/T-036/runs/doi-chieu-smtp-001/; results/T-040/; git diff từ commit 488013070e56342b74ff0f2ccbc6524bcfb8d550, cộng file chưa theo dõi trong gói T-041.
- Phản biện và phản hồi trước: phản biện kết quả của Claude ngày 23/10/2026 được Minh dán trong chat, nguyên văn tại bang-chung.jsonl E024 /result/review_input/original_text; phản hồi và gói sửa Codex tại mục LOG ngày 23/10/2026 và E025 trở đi. Chưa có file REVIEW.
- Code và kết quả liên quan: src/p3/, src/microrank/, src/do_thi/, src/do_thi_tinh/; các nguồn được dẫn trong results/T-041/bao-cao.md, bang-chung.jsonl, manifest.json, ban-giao-phien-2.md; results/T-008/the-dataset.md và các nguồn được dẫn trực tiếp. Revision và lệnh kiểm tại manifest/evidence; Python dùng -B. Node dùng hàm thư viện chuẩn trong bộ nhớ ở lượt sửa; không cần tạo helper hoặc cache để đọc gói.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; không tạo hoặc sửa file.

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

## Nghiệm thu và đóng T-041 — 2026-10-23T17:40:13+07:00 — Codex

- Thiết bị: LeVanMinh, Windows; repo D:/RCA-flashticket. Vai trò: Codex là người làm; Claude là người phản biện chính thức, giữ lịch sử vai trò. Loại việc EXECUTE: ghi nghiệm thu/đóng và sửa STATE theo lời Minh.
- **Quyết định của Minh trong lượt:** “nghiệm thu và đóng task, check state và sửa chuẩn” (Q-186). Đã ghi DECISIONS trước khi đổi STATE. Minh nghiệm thu và đóng T-041; không chờ thêm một lượt kiểm lại để ghi đúng mốc đóng theo lời này. Không ghi rằng Claude đã kiểm lại gói sửa; không tự mở lại phản biện/task.
- Phạm vi ghi đúng ba file: docs/DECISIONS.md; LOG.md này; docs/STATE.md. Không đổi SPEC, báo cáo, JSONL hoặc manifest đã chốt trước nghiệm thu. Các trạng thái chờ phản biện/chưa nghiệm thu ở những snapshot đó là lịch sử; Q-186 và mục LOG này là mốc hiện hành, không sửa lại lịch sử. Các hash outputs trong manifest được kiểm trước đóng: 4/4 khớp.
- Rà STATE: tiêu đề ngày còn 21/10, đầu trang/đoạn task đang mở/mục chờ Minh còn T-041 chưa nghiệm thu; dòng T-041 đã sửa nhưng còn chờ kiểm lại. File dài vì chép lịch sử thay vì làm chỉ mục hiện hành. Đã đối chiếu các quyết định đang được STATE dẫn và LOG T-041; không nâng đề xuất Grafana hay điều kiện chờ cô thành quyết định mới.
- Sửa STATE: ngày 23/10; T-041 xong Q-186; loại các chỉ dẫn chờ phản biện/nghiệm thu T-041 khỏi phần hiện hành; giữ OPEN và quyền dữ liệu/cổng, chuyển các mô tả dài về con trỏ LOG; giữ đủ 40 mã task bằng chỉ mục nhóm. Các hạn chế/lịch sử trước đóng không bị xóa khỏi nguồn gốc. Giữ nguyên ý nghĩa chưa xác minh của câu chờ cô trước M1, không tự đặt/gỡ điều kiện.

### Snapshot STATE trước Q-186 — lịch sử, không là trạng thái hiện hành

```text
# Trạng thái

Cập nhật: 21/10/2026. Không quá một trang. Chi tiết từng task nằm ở `tasks/<mã>/LOG.md`.

- **Cổng hiện tại:** G2 đã duyệt ngày 14/10/2026 (Q-149); P5 đã đóng theo quyết định Minh ngày 18/10/2026 (Q-176); kế hoạch P6 đã lưu theo yêu cầu Minh (Q-177–Q-178) tại [PLAN-P6.md](PLAN-P6.md): 13 phần việc chính + 15 nhánh có điều kiện; T-041 đã hoàn thành phân tích/tự kiểm theo Q-184, chờ phản biện kết quả, chưa nghiệm thu; SPEC M1 vẫn chờ định hướng của cô. G1 đã duyệt ngày 05/10/2026 (Q-61–Q-69; chốt G1 ở Q-70). G0 đã duyệt ngày 02/10/2026 (Q-36). Đề xuất đổi hướng P6 (stack Grafana làm hạ tầng, RCA trên đồ thị mức thao tác) tại [DE-XUAT-HUONG-GRAFANA-RCA.md](DE-XUAT-HUONG-GRAFANA-RCA.md), chưa duyệt; phản biện định hướng dừng 20/10/2026 (Q-179); chờ ý kiến cô qua chương 5 báo cáo tiến độ trước khi soạn SPEC M1.
- **Test và dataset giữ ngoài:** test: 60 ca RE2-TT (TX1, `data/locked/`) và phần test theo ô của Nezha-OB (Q-61, Q-63); Eadro-TT đã duyệt 3 dev/6 test ngày 05/10, danh sách tại `results/T-023/allowlist-phien.json`. Không dùng Eadro trong thực nghiệm tới G2 (Q-83); giữ ngoài: RE3-OB (chưa tải).
- **Remote git:** `github.com/levanminh04/RCA`. Đã commit/push gói cập nhật ngày 17/10/2026 theo Q-175; HEAD khớp origin/master tại lần kiểm 18/10. Đã commit/push gói 18/10 (Q-176–Q-178, PLAN-P6), Q-179 và đề xuất `docs/DE-XUAT-HUONG-GRAFANA-RCA.md` ngày 20/10/2026.

## Mục lục task

| Mã | Tên | Gói | Người làm | Người phản biện | Trạng thái | Thư mục |
|---|---|---|---|---|---|---|
| T-000 | Nền tảng: MRP v3 và quy trình | P0 | Claude | Codex | Xong (02/10) | `tasks/T-000-nen-tang/` |
| T-001 | Chốt danh sách phương pháp | P1 | Claude | Codex | Xong (03/10) | `tasks/T-001-danh-sach-phuong-phap/` |
| T-002 | Thẻ dataset họ RCAEval | P2 | Codex | Claude | Xong (04/10) | `tasks/T-002-the-dataset-rcaeval/` |
| T-003 | Gói thẻ dataset ngoài RCAEval | P2 | Codex | Claude | Xong (04/10) | `tasks/T-003-the-dataset-ngoai-rcaeval/` |
| T-005 | Đo khả thi môi trường và thời gian chạy | P1 | Claude | Codex | Xong (04/10) | `tasks/T-005-do-kha-thi/` |
| T-006 | Kiểm đúng đắn các phương pháp trên laptop | P1 | Claude | Codex | Xong (04/10). WHY-15 đã ghi. Q-52–54 đã ghi DECISIONS (Minh duyệt 04/10). Mục 11 điểm 3–6 của `kiem-dung-dan.md`: chuyển cho T-014 (CIRCA) và T-016 (RCD) đánh giá | `tasks/T-006-kiem-dung-dan-laptop/` |
| T-007 | Kiểm đúng đắn trên EC2 (MicroRank, TraceRCA, BOCPD) | P1 | Claude | Codex | Xong (04/10). Việc dọn còn lại: xóa `~/.sudo_as_admin_successful` khi bật lại EC2 của T-007 | `tasks/T-007-kiem-dung-dan-ec2/` |
| T-008 | Thẻ Nezha OB/TT | P2 | Codex | Claude | Xong (04/10) | `tasks/T-008-the-dataset-nezha/` |
| T-009 | Thẻ Eadro TT/SN | P2 | Codex | Claude | Xong (04/10) | `tasks/T-009-the-dataset-eadro/` |
| T-010 | Thẻ DeepTraLog TT | P2 | Codex | Claude | Xong (04/10) | `tasks/T-010-the-dataset-deeptralog/` |
| T-011 | Thẻ LEMMA-RCA | P2 | Codex | Claude | Xong (04/10) | `tasks/T-011-the-dataset-lemma-rca/` |
| T-012 | Khảo sát dataset 2025–2026 | P2 | Codex | Claude | Xong (04/10) | `tasks/T-012-khao-sat-dataset-2025-2026/` |
| T-014 | Hồ sơ CIRCA PC và kiến trúc | P1 | Codex | Claude | Xong (04/10/2026) | `tasks/T-014-ho-so-circa/` |
| T-013 | Hồ sơ BARO và bộ phát hiện | P1 | Codex | Claude | Xong (04/10/2026); Minh duyệt sau sửa R1 và N1–N3 | `tasks/T-013-ho-so-baro/` |
| T-015 | Hồ sơ MicroRank, TraceRCA và detector trace | P1 | Codex | Claude | Xong (04/10/2026) | `tasks/T-015-ho-so-microrank/` |
| T-019 | Thẻ Sock Shop RCAEval | P2 | Codex | Claude | Xong (04/10/2026) | `tasks/T-019-the-sock-shop/` |
| T-016 | Hồ sơ TORAI, lõi RCD và biến thể RCD | P1 | Claude | Codex | Xong (04/10). Đã áp WHY-19, WHY-20, SL36, K1 C.5/C.8, Q-57; đính chính T-001/T-005/T-006 (D1–D6) | `tasks/T-016-ho-so-torai/` |
| T-017 | Hồ sơ SimpleRCA M4 và luật Type I/II | P1 | Codex | Claude | Xong (04/10/2026); Q-55 | `tasks/T-017-simplerca/` |
| T-018 | Hồ sơ GDN và đọc DecompRCA | P1 | Claude | Codex | Xong (04/10/2026); Q-56, WHY-18. E2 chuyển G1 | `tasks/T-018-ho-so-gdn-decomprca/` |
| T-020 | Tổng hợp G1: phương pháp, dataset, cách chia | P1, P2 | Codex | Claude | Đóng 05/10/2026: thay bằng T-021 (Minh đồng ý đề xuất 0); R1–R3 xử lý ở `results/T-021/goi-g1.md` mục 7 | `tasks/T-020-tong-hop-g1/` |
| T-021 | Gói G1 thu gọn | P1, P2 | Claude | Codex | Xong 05/10/2026: Minh trả lời 7 câu G1 (Q-61–Q-69), không thêm vòng phản biện (đề xuất 0) | `tasks/T-021-goi-g1-thu-gon/` |
| T-022 | Giao thức P3, adapter RE2, bộ chấm, pilot | P3 | Claude | Codex | Xong (06/10, Minh duyệt đóng). Giao thức V2 + WHY-22–35 (Q-74, Q-76); code/pilot chuyển T-030. Còn: ghi sổ Q-75 (mã để trống) | `tasks/T-022-giao-thuc-p3/` |
| T-023 | Kiểm điều kiện dùng Eadro-TT | P3 | Codex | Claude | Xong (06/10, Minh duyệt đóng; Q-83). Không đưa Eadro vào thực nghiệm tới G2; không triển khai T-027 trong đợt này. Giữ kết quả kiểm và mọi run; clock/cửa sổ/lineage/reference còn OPEN. | `tasks/T-023-kiem-eadro/` |
| T-030 | Cài giao thức P3 trên RE2-TT dev: mã chung, fixture, D1, K-B1 | P3 | Claude | Codex | Xong (06/10, Minh duyệt đóng). Mã `src/p3/`, 57 test đạt; D1, phát lại khớp, K-B1 đạt. Phản biện Codex hai lượt: R1, R2, N1 đã sửa, Codex xác nhận; R3 đã sửa theo lời duyệt, Codex chưa kiểm lại. Chuyển sang T-031: chi phí BOCPD đo trên dữ liệu tổng hợp ≈ 27–83 giờ/30 ca, vượt Q-72; T-031 đo lại trên tiền tố (Q-77). | `tasks/T-030-cai-dat-p3/` |
| T-031 | Chạy P3 trên RE2-TT dev: kiểm khóa cấu hình, pilot chi phí | P3 | Claude | Codex | Xong (06/10, Minh duyệt đóng). Khóa CIRCA OLS (Q-80, Q-82; 11 ca vượt ngưỡng 1e10 báo riêng), TORAI nguồn B; MicroRank 4 ERROR tính trượt; chi phí và đề xuất T-024/T-025 ở `results/T-031/do-chi-phi.md`. Phản biện hai lượt: REVIEW R1–R4 và REVIEW-2 R1–R3 đã xử lý, Codex chưa kiểm lại lượt 2. | `tasks/T-031-chay-khoa-pilot/` |
| T-024 | Chấm tầng 1 chế độ (a) trên 30 ca dev RE2-TT | P3 | Codex | Claude | Xong (07/10, Minh duyệt đóng). Hai lượt phản biện đã xử lý; 420 bản ghi và số/bảng giữ nguyên. Nguồn code TORAI EC2 đã đối chiếu khớp (LOG phiên 7). Giới hạn CIRCA làm tròn và hòa ẩn RCD giữ rõ trong báo cáo. | `tasks/T-024-cham-che-do-a/` |
| T-025 | Chế độ (b): N-Sigma, BOCPD (EC2, TIMEOUT 6 giờ/ca), RCA tại báo động đầu | P3 | Claude | Codex | Xong (07/10, Minh duyệt đóng). Báo động đầu đúng BOCPD 3/30, N-Sigma 0/30; thành công chung bị chặn trước hết ở bộ phát hiện. Phản biện R1–R3, N1–N4 đã xử lý (sửa mô tả, tách số TORAI, WHY-35 "biên file"). Hai EC2 đã tắt. | `tasks/T-025-che-do-b/` |
| T-026 | Adapter và chấm tầng 1 chế độ (a) trên Nezha-OB dev (22 ca) | P3 | Codex | Claude | Xong (07/10, Minh duyệt đóng). R1/R2 đã sửa và kiểm đạt; 248 nguồn/số chấm giữ nguyên. Giữ 1 ERROR MicroRank cắt N; CIRCA/TORAI B UNSUPPORTED. Các OPEN nguyên nhân/nền/clock/test/license giữ trong báo cáo và LOG phiên7–8. | `tasks/T-026-nezha-ob-che-do-a/` |
| T-028 | P4: hạn chế xếp hạng chế độ (a) | P4 | Codex | Claude | Xong (08/10/2026), Minh duyệt đóng. Đã sửa R1–R4 và bổ sung R5; kết quả runs/phan-hoi-review-001, phép đo gốc buoc3-005. Nơi xử lý "lan có đáng kể" còn OPEN; chưa phân xử nhân quả. | `tasks/T-028-p4-han-che-xep-hang/` |
| T-029 | P4: hạn chế phát hiện chế độ (b) | P4 | Codex | Claude | Xong (09/10, Minh duyệt đóng theo Q-87). Đã sửa REVIEW-4 và P1/P2; REVIEW-5 không có lỗi đáng kể. Giữ các giới hạn đã khai. | `tasks/T-029-p4-han-che-phat-hien/` |
| T-032 | Lần theo nguyên nhân thất bại xếp hạng | P4 | Claude | Codex | Xong (13/10/2026, Minh đóng bằng lời “ĐÓNG T-032”). Không đóng RQ2/G2. Trước khi dùng H6, H8, CIRCA, KT-11 đọc runs/bo-sung-toan-dien-20261012-001/doi-chieu-dien-giai-review-001.md. Lịch sử trước khi đóng: chờ kiểm lại bản sửa (12/10/2026). Minh duyệt Codex sửa sau REVIEW và yêu cầu phiên Codex mới kiểm (Q-142), thêm câu S-1 (Q-143); giữ vai trò lịch sử trong SPEC. Bốn báo cáo đã sửa; tiêu chí3 đạt một phần, không đóng RQ2/G2. Gói results/T-032/runs/sua-review-001/: M-D48PASS+4N/A, kiểm số412/412 và17bổ sung, A46/D15/E61đạt; giữ cả lượt lỗi. REVIEW chỉ bảng phản hồi, LOG nối thêm. Còn OPEN: đáp ứng return, trọng số khi nhóm đổi, ca ghép chưa rõ, nguyên nhân độ nhạy cửa sổ; quyết định G2/P5–P6 chưa chốt. Prompt mới đầy đủ ở cuối LOG và prompt-codex-kiem-lai.txt; phiên mới mặc định chỉ đọc. Không sửa baseline/test. EC2 chưa thao tác trong lượt sửa.; bổ sung Q-144 hoàn tất phép kiểm13/10, chờ Minh xem báo cáo; giới hạn và kết quả/nghiệm thu cũ giữ rõ; xem LOG và runs/bo-sung-toan-dien-20261012-001/BAO-CAO-TONG-HOP.md | `tasks/T-032-g2-nguyen-nhan-xep-hang/` |
| T-033 | Lần theo cơ chế báo động trước mốc | P4 | Codex | Claude | Xong (11/10/2026, Minh nghiệm thu; Q-137–Q-140). Mục1–3 hoàn tất; số bổ sung EC2 khớp Claude, phản biện dừng. Xác nhận chuỗi N-Sigma/BOCPD, hướng tiền xử lý nhìn trước, cờ khác bắt đầu đoạn MAP, freeze19/60. OPEN: câu4/onset thật/báo giả vận hành/prior riêng/tác động bậc thang/lợi ích đồ thị/D; không so cửa sổ trong T033. T034 dùng câu thay mục6 bo-sung-bao-cao.md, không câu cũ report002. Không đóng RQ2/G2 hoặc chọn P6; bổ sung Q-144 hoàn tất phép kiểm13/10, chờ Minh xem báo cáo; giới hạn và kết quả/nghiệm thu cũ giữ rõ; xem LOG và runs/bo-sung-toan-dien-20261012-001/BAO-CAO-TONG-HOP.md | `tasks/T-033-g2-nguyen-nhan-phat-hien/` |
| T-034 | Gói trình G2: baseline, bản đồ hạn chế hợp nhất, hai phép E1/E2 | P3, P4 (G2) | Claude | Codex | Xong (20/10/2026, Minh nghiệm thu, Q-180); giữ các OPEN dưới đây. Phản biện dừng 14/10 sau sáu lượt sửa (Q-147, Q-148); lượt sửa cuối chỉ đổi lời văn, Codex chưa kiểm. Đầu ra ở `results/T-034/`, bản hiện tại theo `runs/manifest-cuoi-007/`. E1, E2 đã chạy xong trên dev. G2 đã duyệt (Q-149). Các lựa chọn ở mục 8 của `goi-g2.md` theo quyết định hiện hành trong `docs/DECISIONS.md`; lựa chọn chưa được quyết vẫn chờ Minh. Còn mở: lan có đáng kể, đóng góp của chờ ở CIRCA, chênh hai bản TraceRCA, underflow ngoài hai ca, thời điểm sự cố bắt đầu. Kết quả, LOG và cập nhật docs đã có trong lịch sử Git tới đợt push 17/10 (Q-175) | `tasks/T-034-g2-goi-trinh/` |
| T-035 | P5a: đặc tả đồ thị phụ thuộc và bộ dựng từ trace | P5 (G3) | Codex | Claude | Xong (20/10/2026, Minh nghiệm thu, bỏ qua phản biện chính thức, Q-180). Đã đồng bộ văn bản span-parent với bộ dựng theo Q-156 (15/10/2026); giữ kết quả dev đã kiểm. Kiểm kỹ thuật chỉ đọc 18/10: manifest khớp, fixture gốc đạt, oracle bổ sung khớp nội dung JSON sau chuẩn hóa tuple/list. Lượt này không thay tự soát toàn task như lần đầu hoặc phản biện chính thức; Minh chọn bỏ qua phản biện chính thức (Q-180). Prompt hiện hành tại results/T-035/runs/dong-bo-span-parent-001/, LOG Phiên 9. Chưa chọn P6. | `tasks/T-035-p5-do-thi-tu-trace/` |
| T-036 | P5b: hợp đồng nguồn tĩnh và đối chiếu | P5 (G3) | Codex | Claude | Xong (20/10/2026, Q-180). Gốc đã đóng15/10 theo Q-158; gói kỹ thuật SMTP V2 Minh duyệt Q-164 đã triển khai/kiểm16/10. Chung221R1/100SMTPbaseline/29V2 đạt; FT1598/TT1069/OB132 đã tiếp nhận cùng manifest mới. Bàn giao results/T-036/runs/doi-chieu-smtp-001/. Kiểm kỹ thuật chỉ đọc 18/10: manifest V2, pin ba nhánh và mã hiện hành khớp; các kiểm SMTP chạy lại trên mã chung đạt. Gói SMTP V2: Minh nghiệm thu, bỏ qua phản biện chính thức (Q-180). Chưa G3/test. | `tasks/T-036-p5b-hop-dong-chung/` |
| T-037 | P5b: FlashTicket đầy đủ theo thiết kế | P5 (G3) | Codex | Codex phiên sạch (ngoại lệ Q-166) | Xong (16/10/2026, Minh nghiệm thu/đóng Q-167; dừng phản biện). REVIEW.md lưu phản biện độc lập mô hình thiết kế và tiếp nhận SMTP V2; pin chung T036 runs/doi-chieu-smtp-001. Giữ bảy nhóm OPEN tại bao-phu-nguon.json#/open_items; runtime/queue/scope/operation/deployment và lợi ích RCA chưa xác minh, RQ3/RQ5/G3 chưa đóng. SPEC/kết quả giữ lịch sử trước nghiệm thu; mốc đóng tại REVIEW, LOG Phiên 4 và DECISIONS. | `tasks/T-037-p5b-flashticket/` |
| T-038 | P5b: nguồn tĩnh Train Ticket và RE2-TT dev | P5 (G3) | Codex | Claude (kết quả; ngoại lệ Codex theo REVIEW) | Xong (20/10/2026, Minh nghiệm thu, Q-180). Đã dừng phản biện gói sửa17/10/2026 theo Q-171; người làm đã đáp/tiếp nhận R1, đồng bộ graph170/343, chiếu122 và entity-only48; đủ1069graph đạt,90operation giữ tập/số,đổi mô tả SMTP,T/giao giữ nguyên. Current manifest/index và bàn giao T040 tại results/T-038/runs/sua-r1-20261017-001/. Giữ pin SMTP V2 và lịch sử. Semantic/protocol/binding/lineage/runtime OPEN; chưa P6/G3/test. | `tasks/T-038-p5b-trainticket/` |
| T-039 | P5b: nguồn tĩnh Online Boutique và Nezha-OB dev | P5 (G3) | Codex | Codex phiên độc lập (SPEC/kết quả, ngoại lệ Minh) | Xong 16/10/2026 theo Q-165. Minh chấp nhận giới hạn lịch sử R1 và phần nguồn OPEN; phản biện chính thức tại REVIEW.md. Kết quả tham chiếu132graph đã kiểm; inventory toàn deployment/runtime/Node/alias vẫn OPEN. Chưa duyệt G3/mở test/chọn P6 hoặc đóng RQ3/RQ5. | `tasks/T-039-p5b-online-boutique/` |
| T-040 | P5b: tổng hợp và bàn giao P6/P9 | P5 (G3) | Claude | Codex | Đã sửa theo REVIEW R1–R3, N1–N4 (LOG Phiên 5, Q-172), R4 (luồng dừng; LOG Phiên 6, Q-173) và R5 (điều kiện đạt đầu vào gồm B16/pin/mã chung/graph gốc; LOG Phiên 7). OM-11 chuyển sang P9a, OM-07 hoãn ngoài P5 (Q-175; LOG Phiên 8). Lượt hiện hành runs/tong-hop-011 (mọi số trùng run 010; thử ở runs/tong-hop-009/thu-r4.json, runs/tong-hop-010/thu-r5.json). Codex đã kiểm R5 và tính lại toàn bộ đối chiếu chỉ đọc ngày 18/10: đạt, khớp run 011; kiểm số liệu và tình huống giả đầu vào sai đạt. Xong (20/10/2026, Minh nghiệm thu, Q-180). Số TT từng có điều kiện chờ T-038; T-038 đã nghiệm thu (Q-180). Prompt ở LOG Phiên 7 (lượt hiện hành nay là 011); commit/push theo Q-175; chưa G3/test. | `tasks/T-040-p5b-tong-hop/` |
| T-041 | Rà soát sâu nền P3/P5 và bàn giao đầu vào thiết kế RCA | Chuẩn bị P6 | Codex | Claude | Đã đáp và sửa phản biện trong gói bảy file Q-185 (23/10/2026); đã tự kiểm, chờ Claude kiểm lại qua prompt cuối LOG. Giữ SPEC/lịch sử Q-184; chưa nghiệm thu/chọn cơ chế/G3/test. | `tasks/T-041-ra-soat-nen-p3-p5/` |

## Task đang mở

G2 đã duyệt (Q-149); T-034 đã nghiệm thu (Q-180), không đóng RQ2. P5 đã đóng theo quyết định Minh ngày 18/10/2026 (Q-176), giữ các OPEN và lịch sử nghiệm thu/phản biện riêng của từng task. Kiểm trực tiếp chỉ đọc ngày 18/10 không thấy lỗi kỹ thuật chặn bàn giao trong phạm vi đã kiểm. T-035 và gói SMTP V2 của T-036 đã nghiệm thu, bỏ qua phản biện chính thức (Q-180); T-037 và T-039 đã đóng (Q-167, Q-165). T-038 và T-040 đã nghiệm thu (Q-180). Không còn task P5 mở; RQ3/RQ5/G3 vẫn OPEN. Kế hoạch P6 đã lưu theo yêu cầu Minh tại [PLAN-P6.md](PLAN-P6.md), gồm bản hợp nhất 13 + 15, sửa cuối đã được phản biện chấp nhận, đính chính về thời gian/phiên/nén ngữ cảnh và nguồn nguyên văn để chuyển máy (Q-177–Q-178). Đã đồng bộ SPEC T-041 rà nền P3/P5 theo Q-183: phiên thực hiện được tự rà/sửa SPEC trong gói đã duyệt rồi triển khai; hai prompt hiện hành nối ở cuối tasks/T-041-ra-soat-nen-p3-p5/LOG.md. Theo Q-184, Codex đã hoàn thành phân tích/tự kiểm T-041 sau tự rà/sửa SPEC, chờ phản biện kết quả; báo cáo/bằng chứng/bàn giao/manifest tại results/T-041/, prompt Claude ở cuối LOG; chưa nghiệm thu, triển khai P6, chọn cơ chế hoặc mở G3/test; SPEC M1 vẫn chờ định hướng của cô. Bàn giao tại `results/T-040/ban-giao-p6.md`. P9a (T-004, chưa triển khai) nhận R-01…R-10 tại `results/T-040/yeu-cau-quan-sat-p9.md` làm bộ yêu cầu ban đầu, được bổ sung sau (Q-175); chưa gửi nhóm hệ thống. OM-07 hoãn ngoài P5 theo Q-175. P9b cung cấp trace FlashTicket chuẩn hóa; đối chiếu nguồn tĩnh khi có dữ liệu phải được giao trong SPEC của task tương ứng. Giữ các OPEN về kiểu cạnh, lineage/revision, runtime, cơ chế và lợi ích RCA tại nguồn task. Các commit theo Q-175 đã có trong lịch sử Git; `results/T-032/runs/`: file nhẹ ở gốc mỗi lượt đã commit, phần nặng giữ trên máy local theo quyết định Minh (Q-181), không còn việc tồn đọng.

## Đang chờ Minh

- T-003, T-012 đã đóng 04/10 (Minh xác nhận Q-51 gồm cả việc sửa SPEC T-012). License/clock/lineage còn OPEN theo thẻ. EC2 đã Stop (Minh báo 04/10); dữ liệu trên EC2 giữ nguyên.
- T-022: ghi sổ Q-75 (chưa có dòng trong DECISIONS); xóa ghi chú scratchpad phiên 1 của T-030 (ngoài repo). Commit của T-022–T-031 đã có trong `git log`.
- Nghiệm thu T-034, T-035, T-036 (gói SMTP V2), T-038, T-040 đã xong ngày 20/10/2026 (Q-180). P5 đã đóng theo Q-176; kế hoạch P6 đã lưu (Q-177–Q-178); T-041 chờ phản biện kết quả theo prompt cuối LOG, chưa nghiệm thu; phần phân tích/tự kiểm Q-184 đã có tại results/T-041/; SPEC M1 chờ định hướng của cô, chưa duyệt triển khai P6 hoặc G3/test.

```

### Báo cáo kết thúc lượt nghiệm thu/đóng — 23/10/2026

1. **Đã làm:** ghi nguyên lời Minh nghiệm thu/đóng T-041 (Q-186), kiểm và chuẩn hóa STATE theo quyết định hiện hành. T-041 đã xong phần rà nền/bàn giao được nghiệm thu; bỏ trạng thái chờ phản biện/nghiệm thu T-041 khỏi phần hiện hành. Không coi Claude đã kiểm lại gói sửa.
2. **File thay đổi, đúng ba:** docs/DECISIONS.md và LOG này chỉ nối; docs/STATE.md rút còn 31 dòng/482 từ, giữ đủ 40 mã task và con trỏ LOG. Snapshot STATE cũ giữ nguyên nội dung ở mục trên để không mất lịch sử. SPEC, bốn file results/T-041 và nguồn luật/code/kế hoạch giữ nguyên.
3. **Kiểm và kết quả:** 22 kiểm đạt: bốn hash outputs khớp manifest; 49 liên kết STATE tồn tại; 40 mã task cũ xuất hiện đúng một lần trong mục lục; không còn câu T-041 chờ nghiệm thu ở STATE; trạng thái G0–G2/P5/P6/test và OPEN giữ đúng nguồn; DECISIONS/LOG giữ prefix byte; 12 file hồ sơ/nguồn được giữ nguyên; Git ngoài ba file và HEAD không đổi; diff-check đạt. Diff ba file đã đối chiếu cũ→mới: DECISIONS thêm lời quyết định, LOG thêm mốc/snapshot/bàn giao, STATE thay phần lịch sử dài bằng trạng thái/nghĩa vụ và chỉ mục tương ứng. Không chạy baseline/thực nghiệm mới, không đọc test hoặc gọi EC2.
4. **Còn mở:** không còn quyết định chờ nghiệm thu T-041. O01–O12/những phần chưa phân xử và phụ thuộc nghiên cứu giữ tại báo cáo; việc đóng task không đóng RQ2/RQ3/RQ5/G3 hoặc xác nhận hiệu quả/giả thuyết. Hướng P6 và nguồn/ý nghĩa câu chờ cô trước M1 chưa được quyết bởi lời đóng này; không tự đặt/gỡ điều kiện. Những nội dung hợp đồng/timing/ID và giới hạn quan sát cần được nhận vào tài liệu phương pháp khi Minh chọn thiết kế, không ghi thêm WHY/MRP trong lượt đóng.

**Bước tiếp chính xác:** không tự mở thêm phản biện T-041. Khi Minh giao bước thiết kế, đọc AGENTS→STATE→mục đóng mới nhất LOG T-041→manifest outputs→bàn giao và báo cáo/E024–E030; dùng Prompt 2 đang lưu trong LOG cho thiết kế trong chat, đối chiếu PLAN-P6 trước khi trình SPEC M1. Chưa có quyền triển khai M1, sửa thiết kế nguồn, mở G3/test hoặc gửi yêu cầu nhóm hệ thống.

**Lệnh cuối:** Node REPL fs.readFile/crypto kiểm hash/prefix/link, git status --porcelain=v1 -uall, git rev-parse HEAD, git diff --check; difflib/json trong bộ nhớ qua `py -3 -X utf8 -B -c` để đối chiếu diff. Sau nối LOG, kiểm lại bốn hash outputs, prefix, trạng thái ngoài phạm vi và prompt. Không tạo helper/tạm/cache.

**Phản biện và nghiệm thu:** dừng việc chờ phản biện/nghiệm thu T-041 theo quyết định đóng của Minh. Prompt cũ chỉ là lịch sử. Prompt bàn giao tùy chọn dưới đây được soạn theo nghĩa vụ AGENTS; không tự gửi hoặc khởi động lượt mới, không là yêu cầu mở lại task.

**Commit đề nghị khi Minh yêu cầu:** `T-041: nghiệm thu, đóng task và chuẩn hóa STATE`. Chưa commit/push.

### Prompt bàn giao sau đóng — chỉ dùng khi Minh chọn chuyển

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: hồ sơ nghiệm thu/đóng T-041 và cập nhật docs/STATE.md; tasks/T-041-ra-soat-nen-p3-p5/SPEC.md. T-041 đã được Minh nghiệm thu và đóng ngày 23/10/2026; không tự mở lại task.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: bàn giao sau khi đóng task chuẩn bị P6; trước G3.
- Người làm và người phản biện chính thức: Codex là người làm; Claude là người phản biện chính thức; giữ lịch sử vai trò.
- Tài liệu gốc: docs/STATE.md, docs/DECISIONS.md, tasks/T-041-ra-soat-nen-p3-p5/LOG.md mục nghiệm thu và snapshot STATE trước cập nhật; SPEC.md cùng task; docs/MRP.md, PLAN-P6.md, WHY.md, LESSONS.md; git diff từ commit 488013070e56342b74ff0f2ccbc6524bcfb8d550 và các file T-041 chưa theo dõi.
- Phản biện và phản hồi trước: nguyên văn phản biện nhận trong chat tại results/T-041/bang-chung.jsonl E024 /result/review_input/original_text; phản hồi và sửa ngày 23/10/2026 trong LOG T-041 và E025–E030. Lượt đóng task ghi tiếp trong LOG; chưa có file REVIEW và chưa có lượt Claude kiểm lại bản sửa.
- Code và kết quả liên quan: results/T-041/bao-cao.md, ban-giao-phien-2.md, bang-chung.jsonl, manifest.json; source/revision tại manifest và evidence; src/p3/, src/microrank/, src/do_thi/, src/do_thi_tinh/. Kiểm hash chỉ đọc; Python dùng -B, không tạo helper/cache.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat nếu Minh chọn chuyển prompt này; không tạo/sửa file, không tự mở lại task.

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

**Đính chính số lượng file kiểm giữ nguyên trong báo cáo lượt đóng:** danh sách `closeFrozen` của phép kiểm có **11 file**, không phải 12 như câu ở mục 3 trên. Tổng 22 kiểm đạt, 4/4 hash outputs, 49 liên kết và 40 mã task không đổi. Giữ câu cũ như lịch sử; đính chính này không đổi kết quả hoặc phạm vi.
