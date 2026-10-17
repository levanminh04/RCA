# Nhật ký T-035

Chỉ người làm ghi; chỉ nối thêm. Người làm: Codex. Người phản biện: Claude.

---

## Phiên 1 — 14/10/2026 — Codex — laptop Windows — vai trò: người làm

**Mở phiên:** đã đọc AGENTS, STATE, nguồn đề tài, MRP, WHY, DECISIONS, LESSONS và đề xuất T-035 bản hai. Trước lượt này chưa có thư mục T-035 hoặc T-036; không có đầu ra T-035 để tiếp nhận. Các thay đổi chưa commit có trước lượt này được giữ nguyên.

**Công đoạn và mục tiêu nguồn:** ghi bản SPEC đã chốt theo lời Minh. P5 tạo mô hình phụ thuộc và bộ dựng; khảo sát khả thi của mức operation ngay trên dev. DT18 yêu cầu các quan hệ gọi, thông điệp, dữ liệu và ánh xạ tín hiệu. Task chưa đánh giá hiệu quả RCA, chưa hoàn thành toàn P5.

**Quyết định của Minh trong phiên:**
> đồng ý với các đề xuất, hiện tại tôi cần bạn tạo SPEC giúp tôi luôn, bám sát theo những thông tin đã chốt

Đã ghi Q-150 trước khi cập nhật tài liệu dẫn xuất. Minh đồng ý bản hai và các chỉnh sửa được trình: điều kiện nhận Node là host; bộ đọc Node bổ sung trong phạm vi task; khóa nối thông điệp; trạng thái chưa được cung cấp/chưa kiểm trace FlashTicket. Giữ operation-node để khảo sát ngay trên toàn bộ dev; không biến lựa chọn khảo sát thành kết luận lợi ích hoặc chọn cơ chế P6.

**Diễn biến:**
- Đối chiếu quyền ghi và nguồn; xác nhận mã T-035 chưa dùng, Q-150 và WHY-52 chưa có.
- Ghi Q-150; ghi SPEC bản chốt, nối đúng WHY-52 của phụ lục và tạo LOG này.
- Bổ sung đúng dòng T-035 trong STATE; giữ dòng task cũ và các thay đổi của người dùng.
- Tự kiểm tài liệu, so khác biệt với bản hai và kiểm diff. Không tạo `src/do_thi/` hay `results/T-035/`, không chạy thuật toán.

**Nội dung chốt so với bản hai:**
- C6: chỉ nhận nghĩa host khi tài liệu/mã thu chứng minh nguồn định danh. Tính ổn định và tên nhóm Node* là kiểm nhất quán; thiếu thì OPEN.
- C6: reader bổ sung ở `src/do_thi/`; lọc dev trước xuất Node/PodName, dùng lại selector và kiểm nguồn; giữ bộ đọc baseline.
- Chỉ tên cột Node* thuộc phạm vi đọc; không tự bổ sung chuỗi số Node*.
- Quan hệ thông điệp: định nghĩa nối bản tin cụ thể; correlationId cả giao dịch không đủ. Giữ định danh broker/đích và lần giao lại để v0 định nghĩa.
- FlashTicket: chưa được cung cấp/chưa kiểm trace trong task; không suy từ tìm từ khóa hoặc chuẩn tài liệu sang trạng thái toàn hệ.
- V0 phải định nghĩa phép chiếu hai mức và bằng chứng/số đếm theo loại cạnh; giữ quan hệ nội bộ và thành phần không có operation, không tạo thao tác giả.
- Sửa con trỏ K3 để khớp cấu trúc danh sách JSON. Các số K3 giữ nguyên.
- Giữ ước lượng chi phí mới là chưa đo và pilot hai ca. Không dùng ba số chi phí lịch sử làm căn cứ đã xác nhận vì chưa tìm thấy manifest phủ các báo cáo đó.

**Kiểm đã chạy:**
- Manifest G2 `results/T-034/runs/manifest-cuoi-007/manifest.json`: kiểm toàn bộ 318 file, không mất hoặc lệch.
- `results/T-002/local-inspection/run-002/cases.json` khớp manifest T-002. Lọc `dataset == re2tt`, đếm các danh sách `trace.graphs.full.nodes/edges` và cộng `n_spans/parent_resolved_count/parent_reference_count`: khớp các số K3 trong SPEC.
- Thẻ `results/T-002/the-rcaeval.md` lệch manifest cũ, đã biết từ đề xuất; không dùng làm nguồn số. Các nguồn Nezha trong manifest nguồn T-008 đã kiểm khớp.
- Kiểm mã adapter: đầu ra log hiện không giữ Node, đã quy định reader bổ sung.
- Đối chiếu các phần của SPEC, nguồn duyệt, WHY-52 và prompt bàn giao với mẫu hiện có; kiểm toàn bộ diff trong phạm vi ghi.

**Kết thúc phiên:**
1. Đã làm: tạo SPEC và nhật ký T-035, ghi quyết định và lý do đã duyệt, thêm dòng trạng thái task. Nội dung đủ để người làm tiếp nhận mà không cần attachment hoặc lịch sử chat.
2. File của lượt này: `tasks/T-035-p5-do-thi-tu-trace/SPEC.md`, `LOG.md`, `docs/DECISIONS.md`, `docs/WHY.md`, `docs/STATE.md`.
3. Kiểm: đối chiếu nguồn và tính nhất quán tài liệu; kiểm whitespace/diff. Không có kết quả triển khai hoặc thực nghiệm T-035.
4. Còn OPEN: nghĩa Node, nguồn sinh/phạm vi các danh sách quan hệ Nezha, độ ổn định và ý nghĩa tên thao tác, giả định phía gọi/phía được gọi, trace FlashTicket, độ khớp kiến trúc, lợi ích đồ thị/operation. Cần bằng chứng trong T-035, T-036, P6 và P9 theo phạm vi; chưa xác nhận các giả thuyết đó.
5. Bước tiếp theo: đọc SPEC này và cuối LOG; có prompt soát SPEC đã ghi bên dưới để Minh chuyển cho Claude. Khi Minh giao triển khai, bắt đầu bước 0 (kiểm manifest đầu vào), rồi đặc tả v0 và pilot theo SPEC. Không tự chạy trong lượt ghi tài liệu này.
6. Lệnh kiểm cuối lượt: `git diff --check -- docs/DECISIONS.md docs/WHY.md docs/STATE.md tasks/T-035-p5-do-thi-tu-trace`.

**Đề xuất commit, chưa thực hiện:** `docs: add approved T-035 graph specification`, chỉ năm file của lượt này; phải giữ và phân biệt các hunk của người dùng có trước trong ba file docs. Minh duyệt commit thì mới thực hiện.

---

## Prompt bàn giao của lượt này cho Claude — soát SPEC đã ghi

Minh chọn chuyển hay dừng. Không tự mở phiên hoặc gửi sang Claude. Quyền của lượt soát này chỉ trả lời trong chat.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-035 — P5a: đặc tả đồ thị phụ thuộc và bộ dựng từ trace. SPEC tại D:/RCA-flashticket/tasks/T-035-p5-do-thi-tu-trace/SPEC.md; LOG tại cùng thư mục.
- Công đoạn: soát SPEC đã ghi.
- Gói/cổng: P5; cổng gần nhất đã duyệt G2; cổng kế tiếp G3.
- Người làm và người phản biện chính thức: Codex làm, Claude phản biện. Claude soạn đề xuất ban đầu; Codex rà và ghi bản chốt theo lời Minh.
- Tài liệu gốc: AGENTS.md; docs/STATE.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; tasks/_MAU/SPEC.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md và tài liệu kiến trúc liên quan, chỉ đọc. Commit gốc: 25e71dc4eff86111c6e80dc99a216d9549fdd031. Đọc git status và git diff; giữ các thay đổi chưa commit có trước lượt này.
- Phản biện và phản hồi trước: đề xuất bản hai và lượt Codex rà trong chat trước khi ghi; nội dung chốt và nguồn duyệt đã ghi trong SPEC, WHY và LOG. Nếu cần nguyên văn lịch sử chat, Minh cung cấp.
- Code và kết quả liên quan: src/p3/; src/circa_kien_truc/builder.py; results/T-002/local-inspection/run-002/cases.json; results/T-002/handoff-manifest.json; results/T-008/sources/; results/T-008/runs/run-001/manifest.json; results/T-034/runs/manifest-cuoi-007/manifest.json. Môi trường Windows, PowerShell, Python 3. Lượt tạo SPEC chỉ ghi tài liệu; chưa có mã hoặc kết quả thực nghiệm T-035.
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

## Phiên 2 — 14/10/2026 — Codex — laptop Windows — vai trò: người làm (bàn giao tài liệu)

**Lời Minh:** hỏi T-036 đã có hoặc đã ghi chốt ở đâu; yêu cầu prompt cho một phiên Codex mới vì Claude hết token, đánh giá độc lập, không bị neo, ưu tiên tính chính xác, lợi ích đồ án, hướng đồ thị và mong muốn của Minh; không bám SPEC mà quên luật và mục tiêu nguồn.

**Đã đối chiếu:** T-036 chưa có SPEC riêng. Hướng, phân công và nguồn kiến trúc đã ghi ở DECISIONS, WHY-52, mục Task nối tiếp và bảng trách nhiệm của SPEC T-035. SPEC T-036 dự kiến soạn sau đặc tả v1 của T-035. Không đổi phân công: Codex làm, Claude phản biện kết quả.

**Phạm vi lượt này:** soạn và lưu prompt; nối LOG và cập nhật đúng phần bàn giao của dòng T-035 trong STATE. Giữ SPEC, quyết định và các đoạn cũ. Không tạo T-036, không chạy P5, không tự mở phiên hoặc gửi sang agent khác.

**Kiểm:** đối chiếu nguồn ghi các chốt; prompt giữ nguyên Prompt chung, Soát SPEC và khối G3, chỉ điền metadata; bổ sung riêng yêu cầu trực tiếp của Minh cho lượt soát này. Không đưa finding hay đáp án cũ vào prompt.

**Còn mở:** nội dung chi tiết SPEC T-036 phụ thuộc đặc tả v1; hiệu quả của mô hình và mức operation chưa được xác nhận. Lượt Codex mới là soát độc lập tài liệu, không thay lượt phản biện kết quả của Claude.

**Bước tiếp theo:** Minh mở phiên Codex mới, copy nguyên prompt dưới đây. Phiên đó chỉ trả lời trong chat, lập đánh giá từ mục tiêu nguồn trước SPEC và trước kết luận cũ.

**Lệnh kiểm cuối lượt:** `git diff --check -- docs/STATE.md tasks/T-035-p5-do-thi-tu-trace/LOG.md`.

### Prompt cho phiên Codex mới — soát độc lập

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: P5; SPEC T-035 tại D:/RCA-flashticket/tasks/T-035-p5-do-thi-tu-trace/SPEC.md; định hướng task nối tiếp T-036 trong nguồn quyết định và tài liệu kế hoạch của repo.
- Công đoạn: soát SPEC và đối chiếu mục tiêu nguồn, trong một phiên Codex mới.
- Gói/cổng: P5; cổng gần nhất đã duyệt G2; cổng kế tiếp G3.
- Người làm và người phản biện chính thức: Codex làm T-035; Claude phản biện kết quả. T-036 theo phân công trong nguồn quyết định. Lượt này Minh giao Codex soát độc lập tài liệu trong phiên mới vì Claude hết token; không tự đổi vai trò chính thức hoặc nhận đây là lượt phản biện kết quả của Claude.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; docs/STATE.md; docs/MRP.md; docs/DECISIONS.md; docs/WHY.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; tasks/_MAU/SPEC.md; D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md và phần kiến trúc liên quan, chỉ đọc. Commit gốc: 25e71dc4eff86111c6e80dc99a216d9549fdd031. Kiểm git status và git diff; giữ mọi thay đổi có trước.
- Phản biện và phản hồi trước: có trao đổi trong chat trước khi ghi SPEC; dấu vết bàn giao trong tasks/T-035-p5-do-thi-tu-trace/LOG.md và tài liệu quyết định. Không cung cấp bản tóm tắt finding trong prompt này; chỉ đọc kết luận cũ sau khi lập đánh giá riêng theo yêu cầu bên dưới.
- Code và kết quả liên quan: src/p3/; src/circa_kien_truc/builder.py; results/T-002/local-inspection/run-002/cases.json; results/T-002/handoff-manifest.json; results/T-008/sources/; results/T-008/runs/run-001/manifest.json; results/T-034/ và runs/manifest-cuoi-007/manifest.json. Đọc hiện trạng thực tế. Môi trường Windows, PowerShell, Python 3. Lượt này không có quyền chạy thực nghiệm mới.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat. Không tạo hoặc sửa SPEC, REVIEW, LOG, STATE, WHY, DECISIONS hoặc code trong lượt soát này.

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

Yêu cầu bổ sung trực tiếp của Minh cho lượt này:

Đây phải là phiên mới, đánh giá từ nguồn thật. Không dùng lịch sử chat, bộ nhớ riêng, kết luận của phiên Codex đã ghi SPEC hoặc sự đồng thuận giữa các agent làm căn cứ. Prompt này không cung cấp đáp án hay finding dự kiến. Không cố tìm lỗi để chứng tỏ độc lập; cũng không mặc nhiên bảo vệ bản đã duyệt.

Thứ tự đọc để tránh bị neo: đọc AGENTS; đọc STATE để xác định quyền, vai trò và hiện trạng; sau đó đọc DT18, hướng dẫn của cô, mục tiêu/câu hỏi MRP, LESSONS và các quyết định của Minh trực tiếp chi phối. Phân biệt lời duyệt phạm vi và lựa chọn với nhận định khoa học cần bằng chứng. Trước khi đọc SPEC, LOG và lập luận của các lượt cũ, ghi trong chat cách bạn tự hiểu mục tiêu P5, yêu cầu mô hình và những câu hỏi cần bằng chứng để phân xử. Sau đó đọc SPEC, code, nguồn và đầu ra gốc để kiểm; cuối cùng mới đối chiếu lịch sử phản biện/phản hồi nếu có.

Ưu tiên tính chính xác và giá trị thật của đồ án. Đánh giá P5 có phục vụ nghiên cứu phương pháp đồ thị và việc áp dụng trên FlashTicket không: quan hệ nào cung cấp thông tin, thông tin được giữ và ánh xạ ra sao, phép tính về sau cần nó làm gì, và bằng chứng nào sẽ kiểm được điều đó. Đạt đủ mục hoặc đủ file trong SPEC không tự trả lời mục tiêu nghiên cứu.

Hướng đồ thị phụ thuộc là hướng của đề tài. Hãy đánh giá cách hiện thực hướng này có căn cứ, có vai trò tính toán và phù hợp hệ thống thật. Lợi ích của đồ thị phải được kiểm bằng bằng chứng; không mặc định đồ thị sẽ thắng, không làm thuật toán phức tạp chỉ để tạo khác biệt, không thu hẹp mô hình chỉ theo những trường dữ liệu công khai đang có. Phần dữ liệu thiếu phải dẫn tới câu hỏi hoặc yêu cầu quan sát cụ thể.

Mong muốn của Minh là giữ operation-node như một hướng có thể dùng nếu khả thi, và khảo sát ngay trong P5. Đánh giá công bằng khả năng dựng, ý nghĩa thông tin, cách nối với mức dịch vụ/thành phần và cách so sánh về sau. Không loại hướng này chỉ vì SPEC cũ, một dataset hoặc một cách biểu diễn chưa hỗ trợ; cũng không coi mong muốn giữ hướng là bằng chứng phương án có ích. Nếu không đủ dữ liệu, nêu đúng phần thiếu và việc nào có thể làm ngay trong quyền hiện có.

SPEC là hợp đồng thực hiện đã duyệt, phải được đặt trong toàn bộ hệ thống mục tiêu, luật, nguồn và phụ thuộc. Nếu SPEC thiếu, thu hẹp hoặc mâu thuẫn với mục tiêu nguồn hay quyết định của Minh, chỉ rõ nguồn, ảnh hưởng và đề xuất sửa tối thiểu để Minh quyết. Không tự thay nguồn, bỏ nghĩa vụ nghiên cứu hoặc chạy vượt quyền; không dùng câu “ngoài SPEC” để kết thúc một câu hỏi quan trọng mà không có bước xử lý.

Đánh giá cả trách nhiệm của T-035, task nối tiếp T-036 và các phần P6/P9 liên quan. Kiểm những gì đã được ghi bền vững trong repo để phiên sau không phải dựa vào trí nhớ. Phân biệt hướng đã chốt, việc chưa có SPEC chi tiết và bằng chứng chưa thu; không tự tạo task hoặc sửa hồ sơ.

Kết quả phải giúp Minh quyết định việc thực sự ảnh hưởng đồ án. Mỗi nhận xét cần bằng chứng, hậu quả và sửa tối thiểu hoặc phần kiểm cần thiết; xét cả bằng chứng có thể bác nhận xét của chính bạn. Báo rõ phần đang tốt, phần có lỗi, phần chưa phân xử và lựa chọn bị ảnh hưởng. Không đặt thêm cổng hoặc đòi hoàn thành các gói sau để nghiệm thu một task mô tả.

```

## Phiên 3 — 14/10/2026 — Codex — laptop Windows — vai trò: người làm (đáp nhận xét và sửa tài liệu)

**Quyết định của Minh trong phiên:** Minh trả lời “duyệt sửa” cho đúng gói năm file đã trình: WHY, SPEC T-035, STATE, LOG T-035 và DECISIONS. Ghi Q-151 trước khi đồng bộ tài liệu. Phạm vi là hai lập luận WHY-52 và phụ lục tương ứng, trách nhiệm nguồn tĩnh FlashTicket, trạng thái G2/bước kế tiếp, nhật ký và quyết định; chưa triển khai T-035, chưa tạo T-036, không mở test, không commit/push. Codex vẫn là người làm, Claude vẫn là người phản biện kết quả.

**Nguồn nhận xét:** bản đánh giá độc lập của phiên Codex mới do Minh cung cấp nguyên văn trong chat ngày 14/10/2026. Đây là lượt soát tài liệu theo yêu cầu Minh, không thay lượt phản biện kết quả của Claude và không có file REVIEW của T-035.

**Trạng thái dựng lại khi tiếp tục:** SPEC và WHY-52 đã được ghi từ Phiên 1; prompt cho Codex mới đã có ở Phiên 2. Thư mục mã `src/do_thi/`, đầu ra `results/T-035/` và SPEC T-036 chưa có. Giữ mọi thay đổi có trước trong repo. Lượt này chỉ sửa tài liệu đã được Minh duyệt.

**Tự soát và đối chiếu nhận xét:** trước khi trình gói sửa, đã đối chiếu yêu cầu nguồn, SPEC, WHY-52, MRP P5/P9 và quyết định hiện hành. Bảng dưới lưu phần tự kiểm và phản hồi để máy/phiên khác không cần lịch sử chat.

| Điểm trong bản đánh giá Minh cung cấp | Phản hồi của người làm và căn cứ | Sửa đã duyệt; giới hạn |
|---|---|---|
| Lớp thao tác “không mất thông tin” | Đúng. Gộp nút theo tên thao tác không giữ cây span và khoảng thời gian của từng lần thực thi. Hai span con dài như nhau chạy nối tiếp hoặc chồng nhau có thể cho cùng cạnh/số đếm nhưng khác thời gian không được con phủ. SPEC vẫn nhận span gốc; chưa có bản cài, nên không kết luận đã làm mất dữ liệu. | Thu hẹp trong WHY-52 và phụ lục SPEC. Bảng C5 chỉ rõ ứng viên còn cần span gốc. Không thêm đầu ra theo span hoặc đổi phạm vi bộ dựng. |
| Cạnh gửi–nhận trực tiếp “phải giả định luôn biết bên nhận” | Đúng. Có thể chỉ nối khi có bằng chứng, để phần chưa nối OPEN và giữ thông tin broker/hàng đợi riêng. SPEC đã có cạnh logic theo bằng chứng, nên đây là lỗi lập luận loại phương án khác. | Sửa lý do; giữ broker-node để biểu diễn tài nguyên chung và địa chỉ số đo hàng đợi. Không đổi quy tắc nối bản tin. |
| Trách nhiệm nguồn tĩnh FlashTicket chưa rõ | Đúng một phần. MRP P5 đã yêu cầu nguồn tĩnh cho FlashTicket; Q-150 và các câu chung giao nguồn kiến trúc cho T-036, nên chưa có căn cứ nói nghĩa vụ bị bỏ. Bảng trách nhiệm chưa ghi rõ người làm, phiên bản nguồn và phần đối chiếu với trace thật. | Ghi Codex dựng danh mục/đồ thị tĩnh ở T-036, Claude phản biện, nguồn phải có phiên bản/revision. P9b cấp trace thật chuẩn hóa; việc đối chiếu khi có dữ liệu phải được giao trong SPEC tương ứng. SPEC T-036 vẫn soạn sau đặc tả v1. |
| STATE trái nhau về G2 và bước kế tiếp | Đúng về mâu thuẫn trạng thái. Q-149 đã duyệt G2; dòng T-034 và mục Task đang mở vẫn ghi bước trước. Cách sửa chỉ đổi “mười” thành “chín” chưa đủ vì Q-150 đã xử lý một phần lựa chọn sau đó. | Đồng bộ theo quyết định hiện hành; giữ T-034 chờ nghiệm thu. Chỉ rõ T-035 chưa triển khai, T-036 chưa có SPEC, P6/P9 còn phần riêng. Không sửa lịch sử các task khác. |

**Nguồn chi phối đã đối chiếu:** AGENTS; STATE; SPEC và LOG T-035; MRP mục tiêu, P5, P6 và P9; DECISIONS; WHY-52; LESSONS liên quan tới kết luận quá tay, phương án đối lập và bàn giao; DT18 và hướng dẫn của cô. Dùng lại nguồn đã kiểm ở các lượt trước để hiểu phần thiếu, không thêm số thực nghiệm vào bản sửa.

**Đã sửa:** hai câu WHY-52 và bản chép trong SPEC; bảng trách nhiệm/phần chưa bao phủ của SPEC; ngày cập nhật, trạng thái G2, dòng T-034/T-035 và mục Task đang mở của STATE. DECISIONS chỉ nối Q-151; LOG chỉ ghi thêm mục này. Thay đổi không chọn mức thao tác cho P6 và không xác nhận lợi ích đồ thị.

**Kiểm sau khi ghi và bàn giao:** kết quả kiểm, phần còn mở và prompt được nối ngay bên dưới.

**Kiểm đã chạy và kết quả:**
- Đọc toàn bộ phần khác biệt của năm file so với đầu lượt. Dựng ngược riêng các thay đổi đã duyệt và đối chiếu mã băm đầu lượt: nội dung có trước được giữ. DECISIONS và LOG chỉ nối thêm; các file đã thay đổi từ trước ở ngoài gói giữ nguyên.
- WHY-52 và phụ lục SPEC khớp sau khi chuẩn hóa xuống dòng; kiểm cả hai câu mới và bảng trách nhiệm/phần chưa bao phủ.
- STATE thống nhất G2 đã duyệt, T-034 chưa nghiệm thu, T-035 chưa triển khai, T-036 chưa có SPEC. Giữ việc khảo sát operation ngay trên dev và chưa chọn cho P6.
- Tự kiểm phụ trợ chỉ đọc xác nhận hai lập luận và phần bàn giao nhất quán; đây không phải lượt phản biện chính thức.
- `git diff --check` không có lỗi khoảng trắng. Cảnh báo LF/CRLF của Git không làm đổi xuống dòng trong lượt ghi này.
- Prompt bên dưới được ghép nguyên văn Prompt chung, khối Kiểm lại phản hồi và sửa, khối G3; chỉ điền thông tin trung tính.
- Không chạy bộ dựng, thực nghiệm hoặc đọc dữ liệu khóa. Không kiểm lại toàn bộ manifest kết quả cũ trong lượt sửa lời văn này; không thêm số hoặc thay kết quả cũ.

**Điều chưa chắc và quyết định phụ thuộc:** nghĩa của Node, phía gọi/phía được gọi, tính ổn định/ý nghĩa tên thao tác và trace FlashTicket thật vẫn chưa được T-035 kiểm. Lợi ích đồ thị/mức thao tác và việc chọn tín hiệu, cơ chế còn thuộc P6 cùng đánh giá về sau. Nguồn tĩnh FlashTicket đã có người nhận trong định hướng T-036, nhưng phiên bản nguồn cụ thể và SPEC T-036 chưa có; đối chiếu với trace thật cần dữ liệu P9b và SPEC giao việc tương ứng. Không nhận P5, RQ3 hoặc G3 đã hoàn tất; không đóng T-034/RQ2.

**Đề xuất:** dừng lượt soát tài liệu này vì các câu quá mạnh và phần bàn giao đã được sửa theo duyệt; không cần thực nghiệm bổ sung cho chính các điểm đó. Minh quyết gửi kiểm lại hay dừng; prompt vẫn có bên dưới. Việc triển khai T-035 và soạn T-036 là bước riêng theo phạm vi được Minh cho phép, không tự bắt đầu từ lời “duyệt sửa” của lượt này.

**Bước tiếp theo chính xác:** nếu Minh chuyển lượt kiểm, đọc AGENTS, STATE, nguồn mục tiêu và SPEC hiện tại trước; sau đó đối chiếu LOG Phiên 3 và phần sửa. Prompt Claude ở dưới; prompt cho một phiên Codex mới tiếp tục soát độc lập vẫn được giữ nguyên ở LOG Phiên 2. Nếu chuyển sang triển khai, mở SPEC T-035 mục Các bước, bắt đầu bằng kiểm manifest phù hợp của các đầu vào đã liệt kê, đặc tả v0 và fixture; chưa có đầu ra hợp lệ của bộ dựng để dùng lại. SPEC T-036 soạn sau đặc tả v1.

**Đề xuất nội dung commit, chưa thực hiện:** `docs: clarify T-035 graph rationale and FlashTicket handoff`. Chỉ gói năm file/lát sửa đã duyệt của lượt này; các file docs có thay đổi từ trước phải được tách khi lập nội dung commit. Không commit/push khi chưa được Minh yêu cầu hoặc duyệt.

**Lệnh kiểm cuối lượt:** `git diff --check -- docs/WHY.md tasks/T-035-p5-do-thi-tu-trace/SPEC.md docs/STATE.md tasks/T-035-p5-do-thi-tu-trace/LOG.md docs/DECISIONS.md`.

### Prompt cho Claude — kiểm lại phản hồi và sửa tài liệu

Minh copy khối dưới sang phiên Claude nếu muốn kiểm lại; có thể kèm nguyên văn bản đánh giá độc lập đã cung cấp. Không tự gửi.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-035; D:/RCA-flashticket/tasks/T-035-p5-do-thi-tu-trace/SPEC.md; tài liệu lý do, quyết định và trạng thái liên quan trong repo.
- Công đoạn: kiểm lại phản hồi và sửa tài liệu của T-035.
- Gói/cổng: P5; cổng gần nhất đã duyệt G2, cổng kế tiếp G3.
- Người làm và người phản biện chính thức: Codex làm T-035, Claude phản biện kết quả. Lượt Codex mới soát độc lập tài liệu theo lời Minh không đổi phân công chính thức.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; docs/STATE.md; docs/MRP.md; docs/DECISIONS.md; docs/WHY.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; tasks/T-035-p5-do-thi-tu-trace/SPEC.md; D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md và tài liệu kiến trúc liên quan, chỉ đọc. Commit gốc: 25e71dc4eff86111c6e80dc99a216d9549fdd031; kiểm git status và git diff, giữ các thay đổi có trước. File trong gói sửa tài liệu: docs/WHY.md, SPEC T-035, docs/STATE.md, LOG T-035, docs/DECISIONS.md.
- Phản biện và phản hồi trước: tasks/T-035-p5-do-thi-tu-trace/LOG.md, Phiên 1, Phiên 2 và Phiên 3; bản soát độc lập của phiên Codex mới do Minh cung cấp trong chat ngày 14/10/2026. Phản hồi và sửa đã được lưu trong LOG Phiên 3. Chưa có file REVIEW của T-035.
- Code và kết quả liên quan: src/p3/; src/circa_kien_truc/builder.py; results/T-002/local-inspection/run-002/cases.json và results/T-002/handoff-manifest.json; results/T-008/sources/ và results/T-008/runs/run-001/manifest.json; results/T-008/runs/file-audit-001/summary.json, results/T-008/runs/evidence-002/summary.json và results/T-003/runs/final-review-003/artifact-manifest.json; results/T-034/ và results/T-034/runs/manifest-cuoi-007/manifest.json. Windows, PowerShell, Python 3. Lượt này chỉ đọc tài liệu và nguồn hiện có, không chạy thực nghiệm mới.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; không tạo hoặc sửa file.

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


---

## Phiên 4 — 14/10/2026 — Codex — laptop Windows — vai trò: người làm (sửa tài liệu theo duyệt và bàn giao)

**Mở lượt:** tiếp nhận lời Minh sau lượt soát độc lập chỉ đọc trong cùng chat. Đã đọc AGENTS, STATE, SPEC hiện tại, cuối LOG và toàn bộ `docs/review-prompt.md`; kiểm lại code của reader Nezha. Codex giữ vai trò người làm, Claude giữ vai trò phản biện kết quả. T-035 chưa triển khai; chưa có `src/do_thi/` hoặc `results/T-035/`.

**Quyết định của Minh trong lượt — nguyên văn:**
> duyệt sửa theo đề xuất nếu còn, sau đó soạn prompt cho phiên codex mới hoàn toàn sạch. xem prompt mẫu

Đã nối nguyên văn lời duyệt tại Q-152 trước khi đồng bộ nội dung. Phạm vi sửa còn lại: làm rõ miền “toàn file” theo dataset trong SPEC, để đặc tả v0 và thống kê không suy độ phủ file nguồn từ cửa sổ dev Nezha. Đây là làm rõ phạm vi đã duyệt, không thay tập ca, mô hình hai mức, lựa chọn P6 hoặc quyền đọc dữ liệu. Không triển khai từ lời duyệt sửa này.

**Tiếp nhận lượt soát chỉ đọc trước:** không tìm thấy lỗi CHẶN trong SPEC hiện tại; nhận xét KHÔNG CHẶN về tên miền “toàn file” được xử lý trong lượt này. Operation vẫn là hướng khảo sát ngay ở P5, chưa có bằng chứng chọn cho P6 hoặc hiệu quả RCA. Đối chiếu các phản hồi lưu tại Phiên 3: hai lập luận quá mạnh đã được thu hẹp; nguồn tĩnh FlashTicket đã có người nhận; trạng thái hiện tại thống nhất. Không xác minh được toàn bộ snapshot trước sửa từ LOG. Giới hạn độc lập của lượt trước: tìm kiếm đường dẫn đã hiện vài dòng phản hồi cũ trước khi ghi đủ danh sách nhận xét riêng. Prompt mới không đưa các nhận xét hoặc kết luận này vào thông tin bàn giao.

**Bằng chứng của phần sửa:** `src/p3/nezha.py::_doc_cua_so`, dòng 255 đặt lo/hi quanh mốc; dòng 319–321 lọc start/end trước khi xuất span. Reader chỉ trả tập span trong cửa sổ dev được phép. SPEC mục Đầu vào nay phân biệt RE2-TT toàn file ca dev với Nezha toàn tập span trong cửa sổ. V0 và thống kê phải ghi miền thời gian cùng quy tắc giữ span. Chưa có kết quả bộ dựng để kết luận lỗi đã xảy ra.

**File của lượt:** `docs/DECISIONS.md` chỉ nối Q-152; `tasks/T-035-p5-do-thi-tu-trace/SPEC.md` chỉ thêm đoạn miền dữ liệu ở Đầu vào; `LOG.md` chỉ nối mục này và prompt. Trạng thái T-035 vẫn chưa triển khai; STATE đã ghi đúng trạng thái đó, không đổi trạng thái hoặc sửa file thứ tư chỉ để thêm con trỏ prompt. WHY-52 và mọi file có trước được giữ.

**Kiểm sau sửa và kết thúc lượt:** ghi thêm bên dưới sau khi kiểm nội dung, phần khác biệt và prompt. Không chạy thực nghiệm, không đọc dữ liệu khóa, không commit/push.

### Prompt cho phiên Codex mới — soát SPEC từ nguồn trong phiên sạch

Minh mở chat Codex mới và chỉ dán khối dưới đây. Không fork chat hiện tại, không kèm bản tóm tắt kết luận của lượt này. Đây là prompt do Minh yêu cầu, không là việc Codex tự mở hoặc gửi một phiên khác.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: P5; SPEC T-035 tại D:/RCA-flashticket/tasks/T-035-p5-do-thi-tu-trace/SPEC.md; định hướng T-036 trong tài liệu quyết định và kế hoạch của repo.
- Công đoạn: soát SPEC và đối chiếu mục tiêu nguồn trong phiên Codex mới.
- Gói/cổng: P5; cổng gần nhất đã duyệt G2; cổng kế tiếp G3.
- Người làm và người phản biện chính thức: Codex làm T-035, Claude phản biện kết quả; T-036 theo phân công trong nguồn quyết định. Minh giao phiên Codex mới soát độc lập tài liệu; không đổi vai trò chính thức hoặc nhận đây là lượt phản biện kết quả của Claude.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; docs/STATE.md; docs/MRP.md; docs/DECISIONS.md; docs/WHY.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; tasks/_MAU/SPEC.md; docs/review-prompt.md; D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md và tài liệu kiến trúc/cấu hình liên quan, chỉ đọc. Commit gốc: 25e71dc4eff86111c6e80dc99a216d9549fdd031. Kiểm git status và git diff; giữ mọi thay đổi có trước.
- Phản biện và phản hồi trước: tasks/T-035-p5-do-thi-tu-trace/LOG.md, Phiên 1, Phiên 2, Phiên 3 và Phiên 4; nguồn quyết định tại docs/DECISIONS.md. Chưa có file REVIEW của T-035. Chỉ đọc nhận xét và phản hồi cũ sau khi lập đánh giá riêng.
- Code và kết quả liên quan: src/p3/; src/circa_kien_truc/builder.py; results/T-002/local-inspection/run-002/cases.json và results/T-002/handoff-manifest.json; results/T-008/sources/ và results/T-008/runs/run-001/manifest.json; results/T-008/runs/file-audit-001/summary.json, results/T-008/runs/evidence-002/summary.json và results/T-003/runs/final-review-003/artifact-manifest.json; results/T-034/ và results/T-034/runs/manifest-cuoi-007/manifest.json. Đọc hiện trạng thực tế. Windows, PowerShell, Python 3. Lượt này không có quyền chạy thực nghiệm mới.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat. Không tạo hoặc sửa SPEC, REVIEW, LOG, STATE, WHY, DECISIONS hoặc code; không mở dữ liệu khóa, test hoặc heldout.

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

Yêu cầu bổ sung trực tiếp của Minh cho lượt này:

Đây phải là phiên mới, đánh giá từ nguồn thật. Không dùng lịch sử chat, bộ nhớ riêng, kết luận của phiên Codex đã ghi SPEC hoặc sự đồng thuận giữa các agent làm căn cứ. Prompt này không cung cấp đáp án hay finding dự kiến. Không cố tìm lỗi để chứng tỏ độc lập; cũng không mặc nhiên bảo vệ bản đã duyệt.

Thứ tự đọc để tránh bị neo: đọc AGENTS; đọc STATE để xác định quyền, vai trò và hiện trạng; sau đó đọc DT18, hướng dẫn của cô, mục tiêu/câu hỏi MRP, LESSONS và các quyết định của Minh trực tiếp chi phối. Phân biệt lời duyệt phạm vi và lựa chọn với nhận định khoa học cần bằng chứng. Trước khi đọc SPEC, LOG và lập luận của các lượt cũ, ghi trong chat cách bạn tự hiểu mục tiêu P5, yêu cầu mô hình và những câu hỏi cần bằng chứng để phân xử. Sau đó đọc SPEC, code, nguồn và đầu ra gốc để kiểm; cuối cùng mới đối chiếu lịch sử phản biện/phản hồi nếu có.

Ưu tiên tính chính xác và giá trị thật của đồ án. Đánh giá P5 có phục vụ nghiên cứu phương pháp đồ thị và việc áp dụng trên FlashTicket không: quan hệ nào cung cấp thông tin, thông tin được giữ và ánh xạ ra sao, phép tính về sau cần nó làm gì, và bằng chứng nào sẽ kiểm được điều đó. Đạt đủ mục hoặc đủ file trong SPEC không tự trả lời mục tiêu nghiên cứu.

Hướng đồ thị phụ thuộc là hướng của đề tài. Hãy đánh giá cách hiện thực hướng này có căn cứ, có vai trò tính toán và phù hợp hệ thống thật. Lợi ích của đồ thị phải được kiểm bằng bằng chứng; không mặc định đồ thị sẽ thắng, không làm thuật toán phức tạp chỉ để tạo khác biệt, không thu hẹp mô hình chỉ theo những trường dữ liệu công khai đang có. Phần dữ liệu thiếu phải dẫn tới câu hỏi hoặc yêu cầu quan sát cụ thể.

Mong muốn của Minh là giữ operation-node như một hướng có thể dùng nếu khả thi, và khảo sát ngay trong P5. Đánh giá công bằng khả năng dựng, ý nghĩa thông tin, cách nối với mức dịch vụ/thành phần và cách so sánh về sau. Không loại hướng này chỉ vì SPEC cũ, một dataset hoặc một cách biểu diễn chưa hỗ trợ; cũng không coi mong muốn giữ hướng là bằng chứng phương án có ích. Nếu không đủ dữ liệu, nêu đúng phần thiếu và việc nào có thể làm ngay trong quyền hiện có.

SPEC là hợp đồng thực hiện đã duyệt, phải được đặt trong toàn bộ hệ thống mục tiêu, luật, nguồn và phụ thuộc. Nếu SPEC thiếu, thu hẹp hoặc mâu thuẫn với mục tiêu nguồn hay quyết định của Minh, chỉ rõ nguồn, ảnh hưởng và đề xuất sửa tối thiểu để Minh quyết. Không tự thay nguồn, bỏ nghĩa vụ nghiên cứu hoặc chạy vượt quyền; không dùng câu “ngoài SPEC” để kết thúc một câu hỏi quan trọng mà không có bước xử lý.

Đánh giá cả trách nhiệm của T-035, task nối tiếp T-036 và các phần P6/P9 liên quan. Kiểm những gì đã được ghi bền vững trong repo để phiên sau không phải dựa vào trí nhớ. Phân biệt hướng đã chốt, việc chưa có SPEC chi tiết và bằng chứng chưa thu; không tự tạo task hoặc sửa hồ sơ.

Kết quả phải giúp Minh quyết định việc thực sự ảnh hưởng đồ án. Mỗi nhận xét cần bằng chứng, hậu quả và sửa tối thiểu hoặc phần kiểm cần thiết; xét cả bằng chứng có thể bác nhận xét của chính bạn. Báo rõ phần đang tốt, phần có lỗi, phần chưa phân xử và lựa chọn bị ảnh hưởng. Không đặt thêm cổng hoặc đòi hoàn thành các gói sau để nghiệm thu một task mô tả.
```

### Prompt cho Claude — soát SPEC

Prompt đối phương theo nghĩa vụ AGENTS mục 7 và 9; Minh chọn chuyển hoặc dừng. Không tự gửi.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: P5; SPEC T-035 tại D:/RCA-flashticket/tasks/T-035-p5-do-thi-tu-trace/SPEC.md; định hướng T-036 trong tài liệu quyết định và kế hoạch của repo.
- Công đoạn: soát SPEC và đối chiếu mục tiêu nguồn trong phiên Claude.
- Gói/cổng: P5; cổng gần nhất đã duyệt G2; cổng kế tiếp G3.
- Người làm và người phản biện chính thức: Codex làm T-035, Claude phản biện kết quả; T-036 theo phân công trong nguồn quyết định. Claude soát độc lập kế hoạch và các tài liệu hiện tại; giữ phân công chính thức, không thực hiện phản biện kết quả khi chưa có đầu ra triển khai.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; docs/STATE.md; docs/MRP.md; docs/DECISIONS.md; docs/WHY.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; tasks/_MAU/SPEC.md; docs/review-prompt.md; D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md và tài liệu kiến trúc/cấu hình liên quan, chỉ đọc. Commit gốc: 25e71dc4eff86111c6e80dc99a216d9549fdd031. Kiểm git status và git diff; giữ mọi thay đổi có trước.
- Phản biện và phản hồi trước: tasks/T-035-p5-do-thi-tu-trace/LOG.md, Phiên 1, Phiên 2, Phiên 3 và Phiên 4; nguồn quyết định tại docs/DECISIONS.md. Chưa có file REVIEW của T-035. Chỉ đọc nhận xét và phản hồi cũ sau khi lập đánh giá riêng.
- Code và kết quả liên quan: src/p3/; src/circa_kien_truc/builder.py; results/T-002/local-inspection/run-002/cases.json và results/T-002/handoff-manifest.json; results/T-008/sources/ và results/T-008/runs/run-001/manifest.json; results/T-008/runs/file-audit-001/summary.json, results/T-008/runs/evidence-002/summary.json và results/T-003/runs/final-review-003/artifact-manifest.json; results/T-034/ và results/T-034/runs/manifest-cuoi-007/manifest.json. Đọc hiện trạng thực tế. Windows, PowerShell, Python 3. Lượt này không có quyền chạy thực nghiệm mới.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat. Không tạo hoặc sửa SPEC, REVIEW, LOG, STATE, WHY, DECISIONS hoặc code; không mở dữ liệu khóa, test hoặc heldout.

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


### Kiểm cuối lượt và bàn giao

1. **Đã làm:** làm rõ miền “toàn file” trong SPEC; nối nguyên văn lời duyệt Q-152; soạn prompt cho Codex mới và prompt đối phương từ mẫu hiện hành. Prompt Codex giữ nguyên phần yêu cầu bổ sung trực tiếp của Minh trong yêu cầu gốc; không đưa kết luận lượt soát vào metadata.
2. **File thay đổi:** đúng ba file của mục File của lượt. Kiểm dấu vân tay các tài liệu/code trước và sau: không có file khác đổi; Git status giữ nguyên tập mục có trước. LOG và DECISIONS giữ nguyên tiền tố byte của đầu lượt, chỉ nối thêm. Gỡ ngược riêng đoạn miền dữ liệu trong SPEC khôi phục đúng nội dung đầu lượt. WHY-52 và phụ lục SPEC vẫn khớp.
3. **Kiểm:** đọc code reader để đối chiếu start/end; kiểm toàn bộ đoạn SPEC thêm, dòng quyết định và mục LOG; ghép Prompt chung chỉ thay placeholder, khối Soát SPEC và G3 nguyên văn; yêu cầu bổ sung của Minh khớp nguyên văn. Phép kiểm prompt đầu tiên bị AssertionError vì cấm chuỗi “KHÔNG CHẶN” trên toàn prompt, trong khi chính mẫu có chuỗi đó trong quy tắc báo cáo; đã sửa phép kiểm chỉ xét metadata rồi đạt. Không sửa mẫu hoặc bỏ câu của mẫu để qua kiểm. Kiểm khoảng trắng bằng lệnh cuối dưới đây. Không kiểm lại manifest kết quả cũ trong lượt sửa câu chữ; không thêm số kết quả vào SPEC.
4. **Còn mở:** tính khả thi/ý nghĩa operation, nghĩa Node, nghĩa cạnh và trace FlashTicket chưa có bằng chứng mới; T-036/P6/P9 còn nhiệm vụ riêng. Chưa triển khai T-035; không nghiệm thu P5/RQ3/G3 hoặc mở test. Thay đổi chỉ bảo đảm tên miền thống kê không rộng hơn dữ liệu được phép, không chứng minh đồ thị hay operation có ích. Minh quyết chuyển prompt, dừng soát hoặc giao triển khai theo SPEC.

**Bước tiếp theo chính xác:** Minh mở chat Codex mới hoàn toàn, không fork, chỉ copy khối Prompt cho phiên Codex mới ở trên. Phiên nhận đọc AGENTS rồi STATE và nguồn mục tiêu; ghi cách hiểu mục tiêu P5 trong chat trước SPEC/LOG/lập luận cũ; sau đó soát SPEC, code và nguồn gốc, lập nhận xét riêng trước khi đối chiếu lịch sử. Chỉ trả lời trong chat. Khi Minh giao triển khai ở lượt khác, bắt đầu SPEC mục Các bước từ bước 0; không suy quyền chạy từ lời duyệt sửa tài liệu.

**Đề xuất commit, chưa thực hiện:** `docs: clarify T-035 trace scope and clean review handoff`; chỉ phần thay đổi của ba file trong lượt, tách các nội dung có trước. Chờ Minh yêu cầu hoặc duyệt commit/push.

**Lệnh kiểm cuối lượt:** `git diff --check -- docs/DECISIONS.md tasks/T-035-p5-do-thi-tu-trace/SPEC.md tasks/T-035-p5-do-thi-tu-trace/LOG.md`.


---

## Phiên 5 — 14/10/2026 — Codex — laptop Windows — vai trò: người làm (soạn prompt triển khai có tự rà trước)

**Mở lượt:** đọc AGENTS, STATE, SPEC hiện tại, cuối LOG và prompt mẫu. Minh làm rõ prompt cần triển khai T-035 trong phiên Codex mới sau một lần tự rà. Lượt hiện tại chỉ soạn và lưu bàn giao; không bắt đầu cài đặt hoặc thực nghiệm.

**Quyết định của Minh — nguyên văn:**
> prmopt này là prompt triển khai task hay rà soát task, tôi muốn có prompt triển khai, nhưng trước khi triển khai yêu càu codex rà 1 lần nữa, không có vân đề gì mới làm task

Nối nguyên văn lời giao tại Q-153 trước khi đồng bộ bàn giao. Phân công Codex làm/Claude phản biện giữ nguyên. Prompt Phiên 4 là prompt chỉ soát; giữ bản đó làm lịch sử. Prompt mới dưới đây giao triển khai có điều kiện tự rà trước; không là quyết định đổi thiết kế hoặc mở cổng.

**Phạm vi lượt soạn:** DECISIONS chỉ nối Q-153; LOG chỉ nối Phiên 5 và prompt; STATE chỉ dòng T-035 để trỏ prompt triển khai hiện hành. Không sửa SPEC/WHY/code hay kết quả. T-035 hiện vẫn chưa triển khai.

**Nội dung bàn giao:** chặng A tự rà từ nguồn và lập nhận xét riêng trước lịch sử; có vấn đề ảnh hưởng triển khai thì dừng phần phụ thuộc và trình Minh. Nếu không có vấn đề, trong cùng phiên chuyển ngay sang chặng B thực hiện SPEC, không hỏi duyệt chạy lại. Lệnh triển khai xác định riêng quyền viết, dữ liệu, pilot, điều kiện dừng và báo cáo; không dùng quyền triển khai để tự sửa SPEC. Phần tự rà ghép Prompt chung + Soát SPEC + G3 nguyên văn, chỉ thay metadata theo quyền hai chặng; giữ yêu cầu bổ sung trực tiếp của Minh từ prompt gốc.

### Prompt triển khai T-035 — Codex mới tự rà trước, đạt thì làm ngay

Minh mở chat Codex mới hoàn toàn, không fork, và chỉ copy khối sau. Không kèm tóm tắt kết luận hoặc finding của các lượt cũ.

```text
Minh giao bạn triển khai T-035 trong một phiên Codex mới hoàn toàn, tại D:/RCA-flashticket. Đây là lệnh triển khai có tự rà trước, không phải phiên chỉ rà soát. Đọc AGENTS.md và giữ mọi luật của repo.

Vai trò chính thức: Codex là người làm T-035; Claude là người phản biện kết quả. Tự rà của bạn là tự kiểm của người làm, không thay phản biện chính thức.

Thực hiện hai chặng trong cùng phiên:

A. Tự rà một lần từ nguồn thật trước khi triển khai.
- Mở phiên mới, không fork hoặc dùng lịch sử chat/bộ nhớ riêng. Đọc AGENTS và STATE; tiếp theo đọc DT18, hướng dẫn của cô, mục tiêu/câu hỏi MRP, LESSONS và các quyết định trực tiếp chi phối. Ghi trong chat cách hiểu mục tiêu P5 và câu hỏi cần bằng chứng trước khi đọc SPEC, LOG và lập luận cũ.
- Đọc SPEC hiện tại, code, nguồn và đầu ra gốc trong quyền cho phép; kiểm manifest phù hợp. Lập nhận xét riêng trước khi đọc kết luận và phản hồi trong LOG; sau đó đối chiếu lịch sử để hoàn thiện tự rà. Không dùng đồng thuận cũ làm bằng chứng.
- Áp dụng nguyên văn khối mẫu Soát SPEC và G3 bên dưới. Chặng này chỉ đọc, không chạy thực nghiệm mới hoặc sửa tài liệu/code.
- Nếu phát hiện vấn đề ảnh hưởng tính đúng, mục tiêu nguồn, quyền ghi, phạm vi, phụ thuộc hoặc tính toàn vẹn đầu vào: báo nguồn, bằng chứng, hậu quả, sửa tối thiểu/phần thiếu; dừng phần phụ thuộc và trình Minh. Không tự sửa SPEC hoặc nới quyền để triển khai. Không coi câu hỏi đã được giao cho T-035 hay gói sau là lỗi chỉ vì chưa có kết quả.
- Nếu không có vấn đề cần Minh xử lý trước triển khai: báo kết luận tự rà ngắn trong chat và chuyển ngay sang B trong cùng phiên. Không kết thúc bằng “rà xong” hoặc hỏi duyệt chạy lại. Minh đã giao triển khai theo điều kiện này.

B. Triển khai trọn T-035 theo SPEC hiện tại.
- Tiếp nhận vai trò người làm; nối mục mở phiên vào LOG, dẫn lời giao việc đã lưu trong DECISIONS; cập nhật đúng dòng T-035 trong STATE. Không ghi đè lịch sử.
- Bắt đầu mục Các bước của SPEC từ bước 0. Kiểm hiện trạng đầu ra và dùng lại phần hợp lệ; không làm lại chỉ vì sang phiên mới. Thực hiện đầy đủ C1–C9, K1–K8 và mọi đầu ra/tiêu chí xong của SPEC.
- Viết đặc tả v0 và kết quả mong đợi của fixture trước khi chạy bộ dựng. Thực hiện pilot hai ca để đo thời gian/RAM trước lượt đầy đủ. Cài bộ dựng, kiểm fixture, dựng và khảo sát mọi ca dev được duyệt ở cả hai mức, tự kiểm, ghi đặc tả v1 và báo cáo; giữ mọi lượt kể cả lỗi. Ghi tiến độ và thời gian từng bước/ca.
- Phạm vi ghi: D:/RCA-flashticket/results/T-035/; D:/RCA-flashticket/src/do_thi/; chỉ nối D:/RCA-flashticket/tasks/T-035-p5-do-thi-tu-trace/LOG.md; đúng dòng T-035 trong D:/RCA-flashticket/docs/STATE.md. Phần WHY trong SPEC chỉ được nối nguyên văn WHY-52 đã duyệt nếu chưa có; không chép trùng hoặc sửa lý do/chọn thêm thành phần. Quyết định mới cần ghi WHY/DECISIONS vẫn trình Minh theo Luật 0.
- Giữ SPEC đã duyệt, src/p3, src/circa_kien_truc, kết quả task cũ và repo FlashTicket. Không tự chọn cơ chế/tín hiệu/mức đồ thị cho P6, dựng nguồn tĩnh T-036 hoặc ban hành yêu cầu P9a. Khi có đặc tả v1, có thể trình đề xuất SPEC T-036 trong chat; tạo/sửa file SPEC riêng vẫn theo Luật 0.
- Dữ liệu chỉ trong quyền SPEC: RE2-TT dev và Nezha-OB dev qua allowlist/adapter, nguồn Nezha bổ sung đúng phạm vi hẹp. Không đọc test, heldout, data/locked hoặc repo RCA lưu trữ. Không tải hoặc dùng EC2.
- Các điều kiện dừng về chi phí, lỗi và hash của AGENTS/SPEC giữ hiệu lực. Nếu dự kiến lượt chạy vượt một giờ, cần tài nguyên/dữ liệu ngoài phạm vi hoặc phải đổi đề xuất đã duyệt, dừng phần phụ thuộc và trình đúng phạm vi/chi phí. Không xin lại quyền cho bước đã được SPEC và lời giao này cho phép.
- Kết thúc: kiểm complete diff và tập file, báo từng tiêu chí đạt/chưa đạt, mức câu trả lời nguồn, giả thuyết còn mở, bằng chứng thiếu và phần T-036/P6/P9 nhận tiếp. Nối LOG đủ bước/lệnh để máy khác tiếp nhận, cập nhật dòng T-035 thành chờ phản biện khi đầu ra đã hoàn tất, soạn prompt Claude soát kết quả theo mẫu. Không tự nghiệm thu/đóng task, mở test, commit/push hoặc gửi sang agent khác.

Khối dưới đây là nội dung tự rà của chặng A, giữ nguyên mẫu hiện hành. Sau khi A không có vấn đề, tiếp tục chặng B theo lệnh ở trên trong cùng phiên.

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: P5; SPEC T-035 tại D:/RCA-flashticket/tasks/T-035-p5-do-thi-tu-trace/SPEC.md; định hướng T-036 trong tài liệu quyết định và kế hoạch của repo.
- Công đoạn: người làm tự rà SPEC và đối chiếu mục tiêu nguồn trước triển khai T-035 trong phiên Codex mới.
- Gói/cổng: P5; cổng gần nhất đã duyệt G2; cổng kế tiếp G3.
- Người làm và người phản biện chính thức: Codex làm T-035, Claude phản biện kết quả; T-036 theo phân công trong nguồn quyết định. Minh giao phiên Codex mới tự rà trước, rồi triển khai T-035 nếu không có vấn đề; đây là tự kiểm của người làm, không đổi vai trò chính thức hoặc thay phản biện kết quả của Claude.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; docs/STATE.md; docs/MRP.md; docs/DECISIONS.md; docs/WHY.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; tasks/_MAU/SPEC.md; docs/review-prompt.md; D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md và tài liệu kiến trúc/cấu hình liên quan, chỉ đọc. Commit gốc: 25e71dc4eff86111c6e80dc99a216d9549fdd031. Kiểm git status và git diff; giữ mọi thay đổi có trước.
- Phản biện và phản hồi trước: tasks/T-035-p5-do-thi-tu-trace/LOG.md, Phiên 1, Phiên 2, Phiên 3, Phiên 4 và Phiên 5; nguồn quyết định tại docs/DECISIONS.md. Chưa có file REVIEW của T-035. Chỉ đọc nhận xét và phản hồi cũ sau khi lập đánh giá riêng.
- Code và kết quả liên quan: src/p3/; src/circa_kien_truc/builder.py; results/T-002/local-inspection/run-002/cases.json và results/T-002/handoff-manifest.json; results/T-008/sources/ và results/T-008/runs/run-001/manifest.json; results/T-008/runs/file-audit-001/summary.json, results/T-008/runs/evidence-002/summary.json và results/T-003/runs/final-review-003/artifact-manifest.json; results/T-034/ và results/T-034/runs/manifest-cuoi-007/manifest.json. Đọc hiện trạng thực tế. Windows, PowerShell, Python 3. Lượt này không có quyền chạy thực nghiệm mới.
- Phạm vi ghi được Minh cho phép trong lượt này: chặng A chỉ đọc và trả lời trong chat; chưa triển khai hoặc chạy thực nghiệm. Chặng B, sau khi tự rà không có vấn đề: thực hiện đúng Phạm vi ghi của SPEC T-035 và lệnh triển khai ở đầu prompt; không mở dữ liệu khóa, test hoặc heldout.

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

Yêu cầu bổ sung trực tiếp của Minh cho lượt này:

Đây phải là phiên mới, đánh giá từ nguồn thật. Không dùng lịch sử chat, bộ nhớ riêng, kết luận của phiên Codex đã ghi SPEC hoặc sự đồng thuận giữa các agent làm căn cứ. Prompt này không cung cấp đáp án hay finding dự kiến. Không cố tìm lỗi để chứng tỏ độc lập; cũng không mặc nhiên bảo vệ bản đã duyệt.

Thứ tự đọc để tránh bị neo: đọc AGENTS; đọc STATE để xác định quyền, vai trò và hiện trạng; sau đó đọc DT18, hướng dẫn của cô, mục tiêu/câu hỏi MRP, LESSONS và các quyết định của Minh trực tiếp chi phối. Phân biệt lời duyệt phạm vi và lựa chọn với nhận định khoa học cần bằng chứng. Trước khi đọc SPEC, LOG và lập luận của các lượt cũ, ghi trong chat cách bạn tự hiểu mục tiêu P5, yêu cầu mô hình và những câu hỏi cần bằng chứng để phân xử. Sau đó đọc SPEC, code, nguồn và đầu ra gốc để kiểm; cuối cùng mới đối chiếu lịch sử phản biện/phản hồi nếu có.

Ưu tiên tính chính xác và giá trị thật của đồ án. Đánh giá P5 có phục vụ nghiên cứu phương pháp đồ thị và việc áp dụng trên FlashTicket không: quan hệ nào cung cấp thông tin, thông tin được giữ và ánh xạ ra sao, phép tính về sau cần nó làm gì, và bằng chứng nào sẽ kiểm được điều đó. Đạt đủ mục hoặc đủ file trong SPEC không tự trả lời mục tiêu nghiên cứu.

Hướng đồ thị phụ thuộc là hướng của đề tài. Hãy đánh giá cách hiện thực hướng này có căn cứ, có vai trò tính toán và phù hợp hệ thống thật. Lợi ích của đồ thị phải được kiểm bằng bằng chứng; không mặc định đồ thị sẽ thắng, không làm thuật toán phức tạp chỉ để tạo khác biệt, không thu hẹp mô hình chỉ theo những trường dữ liệu công khai đang có. Phần dữ liệu thiếu phải dẫn tới câu hỏi hoặc yêu cầu quan sát cụ thể.

Mong muốn của Minh là giữ operation-node như một hướng có thể dùng nếu khả thi, và khảo sát ngay trong P5. Đánh giá công bằng khả năng dựng, ý nghĩa thông tin, cách nối với mức dịch vụ/thành phần và cách so sánh về sau. Không loại hướng này chỉ vì SPEC cũ, một dataset hoặc một cách biểu diễn chưa hỗ trợ; cũng không coi mong muốn giữ hướng là bằng chứng phương án có ích. Nếu không đủ dữ liệu, nêu đúng phần thiếu và việc nào có thể làm ngay trong quyền hiện có.

SPEC là hợp đồng thực hiện đã duyệt, phải được đặt trong toàn bộ hệ thống mục tiêu, luật, nguồn và phụ thuộc. Nếu SPEC thiếu, thu hẹp hoặc mâu thuẫn với mục tiêu nguồn hay quyết định của Minh, chỉ rõ nguồn, ảnh hưởng và đề xuất sửa tối thiểu để Minh quyết. Không tự thay nguồn, bỏ nghĩa vụ nghiên cứu hoặc chạy vượt quyền; không dùng câu “ngoài SPEC” để kết thúc một câu hỏi quan trọng mà không có bước xử lý.

Đánh giá cả trách nhiệm của T-035, task nối tiếp T-036 và các phần P6/P9 liên quan. Kiểm những gì đã được ghi bền vững trong repo để phiên sau không phải dựa vào trí nhớ. Phân biệt hướng đã chốt, việc chưa có SPEC chi tiết và bằng chứng chưa thu; không tự tạo task hoặc sửa hồ sơ.

Kết quả phải giúp Minh quyết định việc thực sự ảnh hưởng đồ án. Mỗi nhận xét cần bằng chứng, hậu quả và sửa tối thiểu hoặc phần kiểm cần thiết; xét cả bằng chứng có thể bác nhận xét của chính bạn. Báo rõ phần đang tốt, phần có lỗi, phần chưa phân xử và lựa chọn bị ảnh hưởng. Không đặt thêm cổng hoặc đòi hoàn thành các gói sau để nghiệm thu một task mô tả.
```


### Kiểm prompt trước phát hành — làm rõ quyền chạy theo chặng

Tự kiểm phát hiện metadata Code của bản vừa ghép còn câu “Lượt này không có quyền chạy thực nghiệm mới” từ prompt chỉ rà. Câu đó dễ bị hiểu thành cấm cả chặng triển khai. Chỉ thu hẹp câu này về chặng A và ghi quyền chạy chặng B theo SPEC, đúng lời giao hiện tại. Giữ bản vừa ghi làm lịch sử theo quy tắc LOG chỉ nối; bản cuối đầy đủ dưới đây là bản cần copy, không ghép thủ công các đoạn.

### Prompt triển khai T-035 — bản cuối cho phiên Codex mới

Chỉ copy khối này vào chat Codex mới, không fork. Bản này giao tự rà trước và triển khai ngay khi không có vấn đề.

```text
Minh giao bạn triển khai T-035 trong một phiên Codex mới hoàn toàn, tại D:/RCA-flashticket. Đây là lệnh triển khai có tự rà trước, không phải phiên chỉ rà soát. Đọc AGENTS.md và giữ mọi luật của repo.

Vai trò chính thức: Codex là người làm T-035; Claude là người phản biện kết quả. Tự rà của bạn là tự kiểm của người làm, không thay phản biện chính thức.

Thực hiện hai chặng trong cùng phiên:

A. Tự rà một lần từ nguồn thật trước khi triển khai.
- Mở phiên mới, không fork hoặc dùng lịch sử chat/bộ nhớ riêng. Đọc AGENTS và STATE; tiếp theo đọc DT18, hướng dẫn của cô, mục tiêu/câu hỏi MRP, LESSONS và các quyết định trực tiếp chi phối. Ghi trong chat cách hiểu mục tiêu P5 và câu hỏi cần bằng chứng trước khi đọc SPEC, LOG và lập luận cũ.
- Đọc SPEC hiện tại, code, nguồn và đầu ra gốc trong quyền cho phép; kiểm manifest phù hợp. Lập nhận xét riêng trước khi đọc kết luận và phản hồi trong LOG; sau đó đối chiếu lịch sử để hoàn thiện tự rà. Không dùng đồng thuận cũ làm bằng chứng.
- Áp dụng nguyên văn khối mẫu Soát SPEC và G3 bên dưới. Chặng này chỉ đọc, không chạy thực nghiệm mới hoặc sửa tài liệu/code.
- Nếu phát hiện vấn đề ảnh hưởng tính đúng, mục tiêu nguồn, quyền ghi, phạm vi, phụ thuộc hoặc tính toàn vẹn đầu vào: báo nguồn, bằng chứng, hậu quả, sửa tối thiểu/phần thiếu; dừng phần phụ thuộc và trình Minh. Không tự sửa SPEC hoặc nới quyền để triển khai. Không coi câu hỏi đã được giao cho T-035 hay gói sau là lỗi chỉ vì chưa có kết quả.
- Nếu không có vấn đề cần Minh xử lý trước triển khai: báo kết luận tự rà ngắn trong chat và chuyển ngay sang B trong cùng phiên. Không kết thúc bằng “rà xong” hoặc hỏi duyệt chạy lại. Minh đã giao triển khai theo điều kiện này.

B. Triển khai trọn T-035 theo SPEC hiện tại.
- Tiếp nhận vai trò người làm; nối mục mở phiên vào LOG, dẫn lời giao việc đã lưu trong DECISIONS; cập nhật đúng dòng T-035 trong STATE. Không ghi đè lịch sử.
- Bắt đầu mục Các bước của SPEC từ bước 0. Kiểm hiện trạng đầu ra và dùng lại phần hợp lệ; không làm lại chỉ vì sang phiên mới. Thực hiện đầy đủ C1–C9, K1–K8 và mọi đầu ra/tiêu chí xong của SPEC.
- Viết đặc tả v0 và kết quả mong đợi của fixture trước khi chạy bộ dựng. Thực hiện pilot hai ca để đo thời gian/RAM trước lượt đầy đủ. Cài bộ dựng, kiểm fixture, dựng và khảo sát mọi ca dev được duyệt ở cả hai mức, tự kiểm, ghi đặc tả v1 và báo cáo; giữ mọi lượt kể cả lỗi. Ghi tiến độ và thời gian từng bước/ca.
- Phạm vi ghi: D:/RCA-flashticket/results/T-035/; D:/RCA-flashticket/src/do_thi/; chỉ nối D:/RCA-flashticket/tasks/T-035-p5-do-thi-tu-trace/LOG.md; đúng dòng T-035 trong D:/RCA-flashticket/docs/STATE.md. Phần WHY trong SPEC chỉ được nối nguyên văn WHY-52 đã duyệt nếu chưa có; không chép trùng hoặc sửa lý do/chọn thêm thành phần. Quyết định mới cần ghi WHY/DECISIONS vẫn trình Minh theo Luật 0.
- Giữ SPEC đã duyệt, src/p3, src/circa_kien_truc, kết quả task cũ và repo FlashTicket. Không tự chọn cơ chế/tín hiệu/mức đồ thị cho P6, dựng nguồn tĩnh T-036 hoặc ban hành yêu cầu P9a. Khi có đặc tả v1, có thể trình đề xuất SPEC T-036 trong chat; tạo/sửa file SPEC riêng vẫn theo Luật 0.
- Dữ liệu chỉ trong quyền SPEC: RE2-TT dev và Nezha-OB dev qua allowlist/adapter, nguồn Nezha bổ sung đúng phạm vi hẹp. Không đọc test, heldout, data/locked hoặc repo RCA lưu trữ. Không tải hoặc dùng EC2.
- Các điều kiện dừng về chi phí, lỗi và hash của AGENTS/SPEC giữ hiệu lực. Nếu dự kiến lượt chạy vượt một giờ, cần tài nguyên/dữ liệu ngoài phạm vi hoặc phải đổi đề xuất đã duyệt, dừng phần phụ thuộc và trình đúng phạm vi/chi phí. Không xin lại quyền cho bước đã được SPEC và lời giao này cho phép.
- Kết thúc: kiểm complete diff và tập file, báo từng tiêu chí đạt/chưa đạt, mức câu trả lời nguồn, giả thuyết còn mở, bằng chứng thiếu và phần T-036/P6/P9 nhận tiếp. Nối LOG đủ bước/lệnh để máy khác tiếp nhận, cập nhật dòng T-035 thành chờ phản biện khi đầu ra đã hoàn tất, soạn prompt Claude soát kết quả theo mẫu. Không tự nghiệm thu/đóng task, mở test, commit/push hoặc gửi sang agent khác.

Khối dưới đây là nội dung tự rà của chặng A, giữ nguyên mẫu hiện hành. Sau khi A không có vấn đề, tiếp tục chặng B theo lệnh ở trên trong cùng phiên.

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: P5; SPEC T-035 tại D:/RCA-flashticket/tasks/T-035-p5-do-thi-tu-trace/SPEC.md; định hướng T-036 trong tài liệu quyết định và kế hoạch của repo.
- Công đoạn: người làm tự rà SPEC và đối chiếu mục tiêu nguồn trước triển khai T-035 trong phiên Codex mới.
- Gói/cổng: P5; cổng gần nhất đã duyệt G2; cổng kế tiếp G3.
- Người làm và người phản biện chính thức: Codex làm T-035, Claude phản biện kết quả; T-036 theo phân công trong nguồn quyết định. Minh giao phiên Codex mới tự rà trước, rồi triển khai T-035 nếu không có vấn đề; đây là tự kiểm của người làm, không đổi vai trò chính thức hoặc thay phản biện kết quả của Claude.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; docs/STATE.md; docs/MRP.md; docs/DECISIONS.md; docs/WHY.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; tasks/_MAU/SPEC.md; docs/review-prompt.md; D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md và tài liệu kiến trúc/cấu hình liên quan, chỉ đọc. Commit gốc: 25e71dc4eff86111c6e80dc99a216d9549fdd031. Kiểm git status và git diff; giữ mọi thay đổi có trước.
- Phản biện và phản hồi trước: tasks/T-035-p5-do-thi-tu-trace/LOG.md, Phiên 1, Phiên 2, Phiên 3, Phiên 4 và Phiên 5; nguồn quyết định tại docs/DECISIONS.md. Chưa có file REVIEW của T-035. Chỉ đọc nhận xét và phản hồi cũ sau khi lập đánh giá riêng.
- Code và kết quả liên quan: src/p3/; src/circa_kien_truc/builder.py; results/T-002/local-inspection/run-002/cases.json và results/T-002/handoff-manifest.json; results/T-008/sources/ và results/T-008/runs/run-001/manifest.json; results/T-008/runs/file-audit-001/summary.json, results/T-008/runs/evidence-002/summary.json và results/T-003/runs/final-review-003/artifact-manifest.json; results/T-034/ và results/T-034/runs/manifest-cuoi-007/manifest.json. Đọc hiện trạng thực tế. Windows, PowerShell, Python 3. Chặng A không chạy thực nghiệm mới; chặng B thực hiện các lượt T-035 đúng SPEC và lệnh triển khai ở đầu prompt.
- Phạm vi ghi được Minh cho phép trong lượt này: chặng A chỉ đọc và trả lời trong chat; chưa triển khai hoặc chạy thực nghiệm. Chặng B, sau khi tự rà không có vấn đề: thực hiện đúng Phạm vi ghi của SPEC T-035 và lệnh triển khai ở đầu prompt; không mở dữ liệu khóa, test hoặc heldout.

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

Yêu cầu bổ sung trực tiếp của Minh cho lượt này:

Đây phải là phiên mới, đánh giá từ nguồn thật. Không dùng lịch sử chat, bộ nhớ riêng, kết luận của phiên Codex đã ghi SPEC hoặc sự đồng thuận giữa các agent làm căn cứ. Prompt này không cung cấp đáp án hay finding dự kiến. Không cố tìm lỗi để chứng tỏ độc lập; cũng không mặc nhiên bảo vệ bản đã duyệt.

Thứ tự đọc để tránh bị neo: đọc AGENTS; đọc STATE để xác định quyền, vai trò và hiện trạng; sau đó đọc DT18, hướng dẫn của cô, mục tiêu/câu hỏi MRP, LESSONS và các quyết định của Minh trực tiếp chi phối. Phân biệt lời duyệt phạm vi và lựa chọn với nhận định khoa học cần bằng chứng. Trước khi đọc SPEC, LOG và lập luận của các lượt cũ, ghi trong chat cách bạn tự hiểu mục tiêu P5, yêu cầu mô hình và những câu hỏi cần bằng chứng để phân xử. Sau đó đọc SPEC, code, nguồn và đầu ra gốc để kiểm; cuối cùng mới đối chiếu lịch sử phản biện/phản hồi nếu có.

Ưu tiên tính chính xác và giá trị thật của đồ án. Đánh giá P5 có phục vụ nghiên cứu phương pháp đồ thị và việc áp dụng trên FlashTicket không: quan hệ nào cung cấp thông tin, thông tin được giữ và ánh xạ ra sao, phép tính về sau cần nó làm gì, và bằng chứng nào sẽ kiểm được điều đó. Đạt đủ mục hoặc đủ file trong SPEC không tự trả lời mục tiêu nghiên cứu.

Hướng đồ thị phụ thuộc là hướng của đề tài. Hãy đánh giá cách hiện thực hướng này có căn cứ, có vai trò tính toán và phù hợp hệ thống thật. Lợi ích của đồ thị phải được kiểm bằng bằng chứng; không mặc định đồ thị sẽ thắng, không làm thuật toán phức tạp chỉ để tạo khác biệt, không thu hẹp mô hình chỉ theo những trường dữ liệu công khai đang có. Phần dữ liệu thiếu phải dẫn tới câu hỏi hoặc yêu cầu quan sát cụ thể.

Mong muốn của Minh là giữ operation-node như một hướng có thể dùng nếu khả thi, và khảo sát ngay trong P5. Đánh giá công bằng khả năng dựng, ý nghĩa thông tin, cách nối với mức dịch vụ/thành phần và cách so sánh về sau. Không loại hướng này chỉ vì SPEC cũ, một dataset hoặc một cách biểu diễn chưa hỗ trợ; cũng không coi mong muốn giữ hướng là bằng chứng phương án có ích. Nếu không đủ dữ liệu, nêu đúng phần thiếu và việc nào có thể làm ngay trong quyền hiện có.

SPEC là hợp đồng thực hiện đã duyệt, phải được đặt trong toàn bộ hệ thống mục tiêu, luật, nguồn và phụ thuộc. Nếu SPEC thiếu, thu hẹp hoặc mâu thuẫn với mục tiêu nguồn hay quyết định của Minh, chỉ rõ nguồn, ảnh hưởng và đề xuất sửa tối thiểu để Minh quyết. Không tự thay nguồn, bỏ nghĩa vụ nghiên cứu hoặc chạy vượt quyền; không dùng câu “ngoài SPEC” để kết thúc một câu hỏi quan trọng mà không có bước xử lý.

Đánh giá cả trách nhiệm của T-035, task nối tiếp T-036 và các phần P6/P9 liên quan. Kiểm những gì đã được ghi bền vững trong repo để phiên sau không phải dựa vào trí nhớ. Phân biệt hướng đã chốt, việc chưa có SPEC chi tiết và bằng chứng chưa thu; không tự tạo task hoặc sửa hồ sơ.

Kết quả phải giúp Minh quyết định việc thực sự ảnh hưởng đồ án. Mỗi nhận xét cần bằng chứng, hậu quả và sửa tối thiểu hoặc phần kiểm cần thiết; xét cả bằng chứng có thể bác nhận xét của chính bạn. Báo rõ phần đang tốt, phần có lỗi, phần chưa phân xử và lựa chọn bị ảnh hưởng. Không đặt thêm cổng hoặc đòi hoàn thành các gói sau để nghiệm thu một task mô tả.
```


### Kết thúc lượt soạn prompt triển khai

1. **Đã làm:** lưu prompt triển khai T-035 cho phiên Codex mới; tự rà trước theo mẫu, không có vấn đề thì chuyển ngay sang thực hiện SPEC trong cùng phiên. Bản cần copy là mục “Prompt triển khai T-035 — bản cuối cho phiên Codex mới”. Prompt chỉ rà của Phiên 4 và bản ghép trước đính chính được giữ làm lịch sử.
2. **File thay đổi:** đúng `docs/DECISIONS.md`, `docs/STATE.md` và LOG T-035. DECISIONS/LOG chỉ nối; STATE chỉ thay một đoạn trên dòng T-035. SPEC, WHY, code, mọi nguồn và thay đổi có trước giữ nguyên. T-035 chưa triển khai trong lượt soạn này.
3. **Kiểm đã chạy:** đối chiếu Prompt chung chỉ thay placeholder; Soát SPEC và G3 nguyên văn; metadata không có finding/kết luận dẫn hướng; chặng A/B và quyền chạy nhất quán; có lệnh chuyển sang B ngay sau tự rà đạt. Kiểm tiền tố byte LOG/DECISIONS và dấu vân tay tài liệu/code: chỉ ba file trên đổi; Git status giữ tập mục có trước; ngoài dòng T-035, STATE giữ nguyên. Một bước in dòng kiểm tiếng Việt gặp lỗi encoding stdout Windows; kiểm lại qua JSON đã đạt, không ảnh hưởng nội dung file. Không chạy dữ liệu hoặc thực nghiệm.
4. **Còn mở và người quyết:** phiên nhận tự xác định có vấn đề ngăn triển khai không từ nguồn thật; không lấy lượt rà cũ làm chứng nhận. Có vấn đề cần đổi SPEC/quyền hoặc thiếu nguồn thì trình Minh, không tự sửa. Không có vấn đề thì lời giao hiện tại cho phép làm T-035 ngay trong phạm vi; lợi ích đồ thị, lựa chọn P6, nguồn T-036 và quan sát P9 vẫn theo nhiệm vụ riêng. Không tự đóng task hoặc mở test.

**Bước tiếp theo chính xác:** Minh mở một chat Codex mới hoàn toàn, không fork, copy toàn bộ khối “Prompt triển khai T-035 — bản cuối cho phiên Codex mới”. Phiên nhận thực hiện chặng A rồi B theo điều kiện. Khi hoàn tất T-035, người làm soạn prompt Claude soát kết quả theo Prompt chung + Soát kết quả + G3 của mẫu hiện hành; chỉ bàn giao cho Minh, không tự gửi.

**Đề xuất commit, chưa thực hiện:** `docs: authorize T-035 implementation after independent self-check`; chỉ các phần mới của ba file, giữ nội dung có trước. Không commit/push khi chưa được Minh yêu cầu hoặc duyệt.

**Lệnh kiểm cuối lượt:** `git diff --check -- docs/DECISIONS.md docs/STATE.md tasks/T-035-p5-do-thi-tu-trace/LOG.md`.


## Phiên 6 — 14/10/2026 — Codex — laptop Windows — vai trò: người làm

**Mở phiên:** phiên mới, tự rà từ DT18/cô/MRP/LESSONS/DECISIONS trước SPEC và lịch sử. Lời giao triển khai có tự rà trước được lưu tại Q-153 và LOG Phiên 5; Minh giao đầy đủ hai chặng trong prompt phiên này. Giữ Codex làm, Claude phản biện kết quả.

**Tự rà A:** không tìm thấy vấn đề cần Minh xử lý trước triển khai. K3 tái tính từ cases.json đã khớp manifest T-002; nguồn Nezha và G2 đã khớp manifest phù hợp. Tập đầu vào, quyền ghi và các OPEN không mâu thuẫn nguồn. Sau nhận xét riêng mới đọc lịch sử: phản hồi Phiên 3 về mất cây span, phương án nối thông điệp và trách nhiệm nguồn tĩnh đúng; bản hiện tại đã thu hẹp phù hợp. Làm rõ miền toàn file Nezha ở Phiên 4 đúng theo adapter. Không dùng đồng thuận làm bằng chứng.

**Bước 0:** chưa có đầu ra T-035 để dùng lại; WHY-52 đã có, không nối trùng. Snapshot đầu phiên ở results/T-035/runs/buoc0-001/truoc-phien.json, gồm hash src/p3. Bắt đầu v0/fixture, rồi pilot hai ca; chưa chọn cơ chế P6. Các mục triển khai tiếp được nối dưới đây.

**Bước 1–3:** v0 và fixture/expected.json được ghi trước mã bộ dựng. 18 fixture/nhánh lỗi đạt, kiểm chữ ký và từ chối cột nhãn đạt. 362 kiểm hash đầu vào đạt. Môi trường numpy/pandas py312-pin giữ nguyên; reader pyarrow đã có ở T-014 được thêm vào đường import trong tiến trình, không cài/sửa môi trường.

**Pilot-001:** dừng để sửa hiệu năng trước lượt đầy đủ; mọi JSON và mã trước tối ưu được giữ trong run. Khâu lấy witness dùng lựa chọn nhiều lần toàn frame; chuyển sang mảng chỉ mục, giữ thứ tự witness. Độ sâu đổi sang memoization O(số span). Chạy lại pilot hai ca để đo chính bản mới và đối chiếu với đầu ra hợp lệ cũ; chưa chạy toàn bộ theo dự kiến chi phí bản chậm.

**Pilot-002:** hai ca đo đạt; run/acceptance.json có số chi phí và đối chiếu. Mọi graph hợp lệ của pilot-001 khớp từng byte với bản tối ưu. K3 của ca RE2 lớn nhất đạt. Ba seed fixture 0/1/2 khớp. Ước lượng bảo thủ 52 ca dưới một giờ, RAM đỉnh khoảng 2 GiB. Lượt day-du-001 chạy tuần tự, dùng lại hai ca pilot-002; không dùng hai tiến trình chưa được Minh duyệt riêng trong mục ít chờ hơn.


**Bước 4–8 và kết thúc phiên:**
1. Đã triển khai toàn bộ 52 ca dev ở hai mức; RE2 có ảnh chụp 60/300 giây. Dùng lại hai ca pilot-002. Bản v0, v1, fixture, graph, từ vựng, Node, nhóm theo nhãn, kiểm đúng đắn, C9 và manifest đủ đầu ra SPEC. Bản dừng hiệu năng và mọi bản trung gian được giữ. Các nhóm thao tác chỉ A/N và thống kê theo ô đã bổ sung, bản trước giữ ở runs/report-001-before-final-groups.
2. File thay đổi chỉ trong results/T-035/, src/do_thi/, LOG này (nối), dòng T-035 trong STATE. Không sửa SPEC, WHY-52 đã có, DECISIONS, baseline, task cũ hay FlashTicket. Phạm vi ảnh hưởng: đầu vào cấu trúc/độ phủ cho T-036/P6/P9, chưa thay phương pháp hoặc số baseline.
3. Kiểm: K1–K8 hoàn tất theo SPEC. Các hash/chi phí/số chi tiết nằm trong JSON/manifest. K3 khớp từng ca/tập/tổng T-002; K4/K5 mọi khoảng; mọi khoảng dựng hai lần; fixture seed0/1/2 và seed thật h1/h2 ở hai dataset khớp. K6 đủ so hai chiều, không xác nhận độc lập. K8 khớp G2-H19, gồm 8 không có cạnh đi vào, 7 quá thưa và D5. Tự kiểm sâu dữ liệu/fixture và code; kiểm AST/JSON/complete diff/file set và bất biến phạm vi ở finish.py. Không mở test/heldout, không tải, EC2, commit hoặc push.
4. Mức câu trả lời nguồn: đã trả lời C1–C9 về biểu diễn/khả năng dựng/thông tin giữ; chưa trả lời RQ3, không xác nhận cơ chế hoặc lợi ích đồ thị/thao tác, không hoàn tất P5/G3. Các OPEN: nghĩa vật lý của cạnh và thời gian; Node host; nguồn sinh/tính độc lập metadata ngày; nguyên nhân vắng cạnh; quy trình đếm hai graph cũ K2; nghĩa tên HTTP chung; trace FlashTicket thật. Thiếu đúng bằng chứng ở báo cáo/C9; T-036 nhận nguồn tĩnh có revision và so hai nguồn, P6 chọn/kiểm tín hiệu/cơ chế/mức, P9a/P9b nhận thông tin quan sát/dữ liệu thật. Không tự chọn thay Minh.

**Quyết định mới:** không có lựa chọn khoa học mới của Minh; không sửa WHY/DECISIONS. Vai trò giữ nguyên. Lời giao thực hiện từ prompt Minh dán: “Minh giao bạn triển khai T-035 trong một phiên Codex mới hoàn toàn, tại D:/RCA-flashticket. Đây là lệnh triển khai có tự rà trước, không phải phiên chỉ rà soát.” Điều kiện/phạm vi chi tiết đã lưu ở LOG Phiên 5, theo Q-153; tự rà A không có vấn đề chặn nên thực hiện B.

**Đường đi lệnh của phiên (để tiếp nhận trên máy khác):**
- Đọc SPEC, nguồn mục tiêu, báo cáo và manifest trước; đầu ra hợp lệ thì dùng lại, không chạy lại vì đổi máy. Dựng dữ liệu theo data/README.md, môi trường theo environment.json/README.
- Python dùng D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B. Trình tự đã chạy: fixture/prepare.py; scripts/verify_inputs.py; fixture/check.py fixture-001; scripts/run.py pilot-001 --pilot (dừng, giữ); scripts/run.py pilot-002 --pilot; fixture/check.py fixture-002-seed0, fixture-003-seed1, fixture-004-seed2 với seed tương ứng; scripts/run.py day-du-001 --reuse pilot-002; scripts/seed_check.py seed-001-h1 và seed-002-h2; scripts/supplement.py bo-sung-001; scripts/report.py; scripts/write_docs.py; scripts/final_groups.py; scripts/finish.py. Lệnh nằm dưới results/T-035/. Không chạy lại các tên run hiện có; chúng từ chối ghi đè. Không bỏ selector/hash guard để tái chạy.
- Bước tiếp theo chính xác: Claude đọc nguồn gốc và SPEC trước, đọc dac-ta-do-thi.md, thong-ke-do-thi.md, kiem-dung-dan.md, C9, JSON/manifest và code; sau tự soát mới đọc LOG này. Minh chọn chuyển prompt hoặc nghiệm thu/sửa; không tự đóng task. T-036 chưa có SPEC, chỉ soạn đề xuất trong chat sau khi Minh giao, chưa tạo file hoặc dựng nguồn tĩnh.
- Lệnh kiểm cuối cùng: & 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe' -B results/T-035/scripts/finish.py. Lệnh này kiểm toàn bộ diff/tập file và ghi manifest, không thực nghiệm mới.

**Điểm tài liệu cần Minh duyệt ngoài quyền hiện tại:** mục “Task đang mở” trong STATE còn hai câu trước triển khai: “T-035 đã có SPEC, đã sửa tài liệu theo Q-151; chưa cài đặt hoặc chạy. Bước tiếp theo: triển khai theo SPEC T-035 trong phạm vi Minh cho phép.” Phạm vi phiên này chỉ cho sửa dòng bảng T-035. Đề xuất thay đúng hai câu ấy bằng: “T-035 đã triển khai, đang chờ Claude phản biện kết quả; prompt bàn giao ở LOG Phiên 6.” Vì sao: tránh phiên sau hiểu nhầm trạng thái. Ảnh hưởng: chỉ đoạn chỉ dẫn tiếp nhận của STATE; không thay nghiệm thu/nguồn khoa học. Chưa sửa phần đó.

**Đề xuất commit, chưa thực hiện:** feat: build trace dependency graphs for T-035; chỉ phạm vi của task và hunk dòng T-035, giữ mọi hunk có trước. Chờ Minh duyệt riêng; không tự commit/push.

### Prompt cho Claude — soát kết quả

Minh chuyển thủ công. Prompt này chưa cấp quyền ghi REVIEW; Minh có thể giao thêm tên bản và quyền ghi riêng. Không tự gửi hoặc mở phiên.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-035 — P5a: đặc tả đồ thị phụ thuộc và bộ dựng từ trace; D:/RCA-flashticket/tasks/T-035-p5-do-thi-tu-trace/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P5; cổng hiện tại G2 đã duyệt, cổng kế tiếp G3.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện chính thức.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; docs/STATE.md, MRP.md, WHY.md, DECISIONS.md, LESSONS.md, review-prompt.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và advisor-2026-09-23.md; tasks/_MAU/SPEC.md, REVIEW.md; D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md và tài liệu kiến trúc liên quan, chỉ đọc; commit gốc 25e71dc4eff86111c6e80dc99a216d9549fdd031; git status/diff, giữ mọi thay đổi có trước.
- Phản biện và phản hồi trước: LOG T-035 Phiên 1–6; chưa có REVIEW của T-035; đọc đánh giá và phản hồi cũ sau tự soát nguồn/đầu ra.
- Code và kết quả liên quan: D:/RCA-flashticket/src/do_thi/; src/p3/; src/circa_kien_truc/builder.py; results/T-035/manifest.json, các báo cáo và runs/; results/T-002/local-inspection/run-002/cases.json, handoff-manifest.json; results/T-008/sources/, runs/run-001/manifest.json, runs/evidence-002/summary.json; results/T-003/runs/final-review-003/artifact-manifest.json; results/T-034/runs/manifest-cuoi-007/manifest.json; allowlist/nhãn dev T-022 và T-026; môi trường Windows/PowerShell, Python py312-pin; hướng dẫn src/do_thi/README.md và LOG T-035; phiên bản/code hash trong manifest, environment.json.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; chưa được phép ghi REVIEW, LOG, STATE, SPEC, code hoặc kết quả; không mở test/heldout/data/locked; dữ liệu dev chỉ qua allowlist/adapter của T-035.

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

**Kiểm cuối — sửa lỗi console:** finish lần đầu đã qua kiểm dữ liệu, phạm vi, LOG/STATE, AST/JSON và diff --check, rồi lỗi giải mã cp1252 khi đọc diff tiếng Việt. Giữ mã/lỗi tại runs/kiem-cuoi-001/finish-attempt-001*. Chỉ đổi bộ đọc subprocess sang UTF-8 và dùng lại phép kiểm đã ghi nếu bằng nhau; không chạy lại thực nghiệm. Lệnh cuối vẫn là scripts/finish.py, kết quả cuối tại final-verification.json và manifest.json. Prompt phía trên giữ nguyên.

**Minh duyệt đồng bộ STATE sau kiểm cuối:** trả lời “Duyệt thay hai câu này” cho đúng đề xuất hai câu ở mục Task đang mở. Thay bằng câu đã trình, bỏ ghi chú chờ đồng bộ trong dòng T-035 (dòng thuộc quyền ghi đã có). Chỉ STATE và LOG nối thêm; cập nhật receipt/manifest trong results/T-035. Không đổi số, kết luận, SPEC hoặc vai trò; không nghiệm thu/đóng task. Kiểm mới ở runs/dong-bo-state-001; final-verification trước đồng bộ giữ nguyên làm lịch sử. Prompt Claude phía trên và file prompt giữ nguyên. Lệnh cuối: phép kiểm và cập nhật manifest trong cùng lệnh đồng bộ STATE ngày 14/10/2026.


## Phiên 7 — 15/10/2026 — Codex — LEVANMINH — Người làm

**Mở phiên / quyền:** EXECUTE theo Q-154. Minh duyệt đúng gói sửa messaging đã trình và yêu cầu prompt cho phiên Codex sạch tự soát T-035 như lần đầu, lập nhận xét độc lập trước lịch sử. Không đổi người phản biện chính thức (Claude), không sửa SPEC.

**Checkpoint đầu phiên:** manifest cũ đã được kiểm toàn bộ và lưu nguyên bản cùng mọi file dự kiến sửa ở runs/sua-n1-001/before/. Phạm vi, trạng thái git và hash trước sửa ở preflight.json. Giữ mọi kết quả cũ. Một trợ lý triển khai hỗ trợ thiết kế fixture độc lập, không mở vòng phản biện. Bước tiếp: chốt nghĩa trường và expected trước sửa code, kiểm fixture, chạy lại đầy đủ dev với cấu hình cũ, đối chiếu và cập nhật tài liệu.

**Bước hợp đồng/fixture:** Q-154 và WHY-52 bổ sung đã ghi trước sử dụng bản sửa. Thiết kế trước code ở design.md; receipt oracle-before-code.json lưu hash inputs/expected trước đổi builder. Trợ lý triển khai soạn oracle từ literal, không lấy output builder làm expected. 18 fixture cũ và 33 fixture mới đạt seed0/1/2; commands/results ở runs/sua-n1-001/. Bản v1 chạy trên oracle mới giữ tại fixture-v1-001: failure gồm cả khác schema, không coi là 33 lỗi riêng. Bộ dựng/runner/kiểm phép chiếu đã đồng bộ địa chỉ.

**Hồi quy đang chạy:** launch_full.py gọi runner mới cho đủ 52 ca, không --reuse, lưu day-du-001 dưới lượt sửa. Chi phí vài ca đầu cao hơn lượt trước; đã báo Minh dự kiến gần 50–55 phút theo tỷ lệ đo, tiếp tục theo dõi trần một giờ. Chưa kết luận dev bằng nhau trước comparison.json. Prompt Codex sạch đã soạn từ mẫu: tự lập nhận xét toàn task trước lịch sử, không thay Claude phản biện chính thức.

**Tự kiểm biên thiếu dữ liệu:** consumer có kind nhưng attributes/links đều null hoặc vắng đã bỏ qua nhánh đếm unresolved. Thuộc cùng hợp đồng thiếu bằng chứng của gói đã duyệt. Ghi oracle check_missing_attributes.py và receipt boundary-oracle-before-code.json trước sửa, giữ bản trước ở boundary-before/. Lượt boundary-before-001 fail; sau sửa 3 ca biên đạt seed0/1/2. Phát lại 18+33 fixture bằng code cuối, tất cả đạt, giữ kết quả mới đuôi -002 và mọi -001. Lượt dev day-du-001 đã dừng và giữ sau khoảng 12,5 phút (số chính xác full-command.json), ghi rõ interruption.json; không coi là lượt đầy đủ. launch_full_final.py đang chạy đủ 52 ca vào day-du-002, không reuse, để bằng chứng dùng đúng code cuối.

**Checkpoint tiếp tục phiên — 2026-10-15T06:18:59.479303+00:00 UTC:** ngữ cảnh đã được nén; tiếp tục đúng gói Q-154. Lượt đầy đủ cuối day-du-002 còn chạy, không khởi động lại. Bộ dựng và runner đã đóng băng; fixture cuối ba seed đã đạt. Bước còn lại: chờ summary.json và full-command-002.json, chạy compare_full.py, sinh tài liệu qua scripts/write_docs.py, kiểm diff rồi finalize.py trong runs/sua-n1-001/. Prompt phiên sạch đã soạn, chưa gửi hoặc mở phiên mới.

**Kết thúc Phiên 7 — sửa hợp đồng và hồi quy:**

1. **Đã làm:** sửa hợp đồng v2 và bộ dựng để tách địa chỉ phát, queue nhận, phạm vi định danh; giữ địa chỉ qua cạnh/phép chiếu/fingerprint. Thêm diagnostic và điều kiện từ chối nối mâu thuẫn/đa nghĩa. Thiết kế/WHY và oracle được ghi trước code. Đã soạn prompt Codex sạch theo yêu cầu Minh, soát toàn T-035 như lần đầu; Claude vẫn là người phản biện chính thức.
2. **File:** đúng danh sách Q-154/preflight.json, cộng đầu ra dưới results/T-035/runs/sua-n1-001/. LOG chỉ nối, STATE chỉ dòng T-035. Giữ mọi kết quả/lượt cũ; bản trước của file sửa trong before/, bản sau trong after/. Không sửa SPEC, AGENTS, MRP, LESSONS, baseline, src/p3, task khác hoặc hệ FlashTicket. Không commit/push.
3. **Kiểm:** 362 kiểm đầu vào cũ đạt trước chạy; manifest cũ đầy đủ đã kiểm ở preflight. 18 fixture cũ, 33 fixture messaging và 3 ca thiếu toàn attributes/links đạt seed0/1/2; outputs fixture giữa seed giống nhau. Bản v1 chạy trên oracle mới giữ riêng, không gọi số fail schema là số lỗi ngữ nghĩa. Lượt day-du-001 dừng sau tự kiểm để sửa nhánh thiếu dữ liệu; giữ interruption.json và toàn bộ output. Toàn bộ 52 ca ở day-du-002 chạy mới bằng code cuối (kiểm hash), không reuse, 1045 khoảng K1/K2/K4/K5 đạt; 1201 graph byte bằng cũ, nội dung ca/vocabulary/Node/coverage/checks bằng cũ ngoài chi phí máy. Nguồn: comparison.json và các result.json trong lượt sửa. Chi phí thực 37.38 phút, RAM đỉnh 2.65 GiB. Kiểm cuối gồm source/diff/file set, JSON/AST, oracle bất biến, tái sinh tài liệu, hash manifest; receipt tại final-verification.json.
4. **Mức kết luận:** N1 đã được xử lý trong hợp đồng/bộ dựng theo fixture; chưa là kiểm routing hoặc instrumentation FlashTicket thật. Dev không có messaging nên hồi quy không thay bằng chứng fixture. Tiêu chí 1/9 được trình lại ở mức hợp đồng v2, chờ tự soát phiên sạch, phản biện chính thức và Minh nghiệm thu. C1–C9 vẫn là mô tả khả năng dựng/giữ thông tin; chưa trả lời RQ3, chưa chọn P6, chưa hoàn tất P5/G3. Node host, semantics cạnh/thời gian, nguồn sinh metadata mức ngày, nguyên nhân vắng cạnh và trace FlashTicket thật còn OPEN như báo cáo. Không thêm giả thuyết khoa học đã xác nhận.

**Quyết định của Minh trong phiên:** Q-154 ghi nguyên văn lời duyệt gói và yêu cầu prompt Codex sạch. Không đổi vai trò chính thức hoặc nghiệm thu task. Thiết kế kỹ thuật bổ sung WHY-52 ghi đúng mục đích DT18/nhu cầu kỹ thuật, không dựng hạn chế RCA để biện minh.

**Bước tiếp theo chính xác:** Minh mở phiên Codex mới, dán toàn bộ prompt-codex-sach-soat-t035.txt dưới lượt này. Phiên đó chỉ đọc/tự soát toàn task, lập nhận xét trước lịch sử, không phải chỉ kiểm bản sửa. Nguồn đầu: AGENTS, SPEC, mục tiêu MRP/DT18/cô, code và graph/JSON theo manifest. Không chạy lại dev đã có đầu ra hợp lệ hoặc mở locked. Prompt Claude vẫn được soạn để Minh chọn chuyển thủ công; không tự mở/gửi phiên.

**Lệnh đã chạy:** Python D:/RCA-ext/envs/py312-pin/Scripts/python.exe -X utf8 -B. Fixture cũ: results/T-035/fixture/check.py với tên sua-n1-001/fixture-cu-seed0-002, fixture-cu-seed1-002, fixture-cu-seed2-002. Fixture mới: runs/sua-n1-001/check_messaging.py với fixture-v1-001 --builder-path before/src/do_thi/builder.py và fixture-v2-seed0-002, fixture-v2-seed1-002, fixture-v2-seed2-002. Ba ca thiếu thuộc tính: check_missing_attributes.py với boundary-seed0-002, boundary-seed1-002, boundary-seed2-002 trong cùng lượt. Lượt đầy đủ cuối: runs/sua-n1-001/launch_full_final.py gọi scripts/run.py sua-n1-001/day-du-002. Đối chiếu: runs/sua-n1-001/compare_full.py. Tài liệu: scripts/write_docs.py. Mọi đường script tương đối tính từ results/T-035/ nếu chưa có prefix đó. Không dùng lại tên output đã tồn tại.

**Lệnh kết thúc/kiểm cuối:** & 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe' -X utf8 -B results/T-035/runs/sua-n1-001/finalize.py; sau đó đọc lại hash manifest và trạng thái git chỉ đọc. Các kiểm cuối chỉ xác nhận phạm vi và tính nhất quán đầu ra, không thêm thực nghiệm hoặc cổng.

**Đề xuất commit, chưa thực hiện:** fix: separate messaging identity and queue addresses in T-035. Minh duyệt riêng commit/push; phiên này giữ working tree.

### Prompt Codex sạch — tự soát toàn T-035

```text
Minh yêu cầu một phiên Codex sạch, đánh giá toàn bộ T-035 như lượt đầu. Không tiếp nhận kết luận hoặc danh sách lỗi từ phiên trước để định hướng tìm kiếm. Đây là lượt tự soát độc lập về ngữ cảnh của người làm; Claude vẫn là người phản biện chính thức theo SPEC.

Thứ tự đọc riêng Minh yêu cầu cho lượt này: đọc yêu cầu nguồn, SPEC, hợp đồng hiện hành, code và bằng chứng đầu vào/trung gian/đầu ra trước. Dùng STATE và quyết định để xác định vai trò/quyền, không lấy trạng thái hoàn thành làm kết luận. Chưa đọc nhận xét/kết luận trong LOG, REVIEW, báo cáo tự kiểm, bản trước sửa, diff lịch sử hoặc prompt cũ. Ghi rõ danh sách nhận xét độc lập vào chat rồi mới đối chiếu lịch sử và các báo cáo để kiểm từng điểm. Không chỉ rà phần vừa sửa; không giới hạn trước số lỗi hoặc mặc định phải có lỗi. Thứ tự này áp dụng trước các chỉ dẫn đọc lịch sử thông thường, theo lời Minh trong lượt giao việc.

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-035 — P5a: đặc tả đồ thị phụ thuộc và bộ dựng từ trace; D:/RCA-flashticket/tasks/T-035-p5-do-thi-tu-trace/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P5; G2 đã duyệt, G3 là cổng kế tiếp.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện chính thức. Minh giao phiên Codex mới tự soát toàn task độc lập về ngữ cảnh; không đổi vai trò trong SPEC.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; tasks/T-035-p5-do-thi-tu-trace/SPEC.md; docs/MRP.md, WHY.md, DECISIONS.md, LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và advisor-2026-09-23.md; docs/review-prompt.md; tasks/_MAU/REVIEW.md. D:/Project/flash-ticket-platform/docs/architecture/B13-api-and-event-contracts.md, B16-observability-baseline.md và nguồn kiến trúc liên quan, chỉ đọc. Kiểm git status đầu phiên để giữ thay đổi có trước; git diff từ commit gốc được ghi trong manifest dùng ở bước đối chiếu lịch sử sau tự soát.
- Phản biện và phản hồi trước: Lịch sử nằm trong tasks/T-035-p5-do-thi-tu-trace/LOG.md và results/T-035/runs/; bản phản biện nếu có phải liệt kê tại thư mục task. Chỉ mở các nhận xét, phản hồi, prompt cũ và bản trước sửa SAU khi đã ghi danh sách nhận xét độc lập trong chat. Không nhận tóm tắt findings từ phiên trước.
- Code và kết quả liên quan: D:/RCA-flashticket/src/do_thi/; src/p3/; src/circa_kien_truc/builder.py; results/T-035/dac-ta-do-thi.md, manifest.json, graph/JSON, fixture, scripts, báo cáo và các run được manifest chỉ tới. Đối chiếu nguồn T-002, T-003, T-008, T-034 theo manifest đầu vào; allowlist/nhãn dev T-022, T-026. Revision/hash/môi trường trong manifest và environment.json; hướng dẫn src/do_thi/README.md. Python D:/RCA-ext/envs/py312-pin/Scripts/python.exe -X utf8 -B; Windows/PowerShell. Kiểm hash trước dùng số; không chạy script có ghi file trong lượt chỉ đọc.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat. Không ghi REVIEW, LOG, STATE, SPEC, code hoặc kết quả; không commit/push. Không mở test/heldout/data/locked, không đọc repo RCA lưu trữ. Dữ liệu dev chỉ qua allowlist/adapter và phạm vi SPEC T-035; phép phát lại rẻ chỉ làm trong bộ nhớ, không chạy thực nghiệm mới.

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

### Prompt Claude — soát kết quả

Minh chuyển thủ công nếu muốn; chưa cấp quyền ghi REVIEW.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-035 — P5a: đặc tả đồ thị phụ thuộc và bộ dựng từ trace; D:/RCA-flashticket/tasks/T-035-p5-do-thi-tu-trace/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P5; G2 đã duyệt, G3 là cổng kế tiếp.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện chính thức.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; tasks/T-035-p5-do-thi-tu-trace/SPEC.md; docs/MRP.md, WHY.md, DECISIONS.md, LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và advisor-2026-09-23.md; docs/review-prompt.md; tasks/_MAU/REVIEW.md. D:/Project/flash-ticket-platform/docs/architecture/B13-api-and-event-contracts.md, B16-observability-baseline.md và nguồn kiến trúc liên quan, chỉ đọc. Kiểm git status đầu phiên để giữ thay đổi có trước; git diff từ commit gốc được ghi trong manifest dùng ở bước đối chiếu lịch sử sau tự soát.
- Phản biện và phản hồi trước: Lịch sử nằm trong tasks/T-035-p5-do-thi-tu-trace/LOG.md và results/T-035/runs/; bản phản biện nếu có phải liệt kê tại thư mục task. Chỉ mở các nhận xét, phản hồi, prompt cũ và bản trước sửa SAU khi đã ghi danh sách nhận xét độc lập trong chat. Không nhận tóm tắt findings từ phiên trước.
- Code và kết quả liên quan: D:/RCA-flashticket/src/do_thi/; src/p3/; src/circa_kien_truc/builder.py; results/T-035/dac-ta-do-thi.md, manifest.json, graph/JSON, fixture, scripts, báo cáo và các run được manifest chỉ tới. Đối chiếu nguồn T-002, T-003, T-008, T-034 theo manifest đầu vào; allowlist/nhãn dev T-022, T-026. Revision/hash/môi trường trong manifest và environment.json; hướng dẫn src/do_thi/README.md. Python D:/RCA-ext/envs/py312-pin/Scripts/python.exe -X utf8 -B; Windows/PowerShell. Kiểm hash trước dùng số; không chạy script có ghi file trong lượt chỉ đọc.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat. Không ghi REVIEW, LOG, STATE, SPEC, code hoặc kết quả; không commit/push. Không mở test/heldout/data/locked, không đọc repo RCA lưu trữ. Dữ liệu dev chỉ qua allowlist/adapter và phạm vi SPEC T-035; phép phát lại rẻ chỉ làm trong bộ nhớ, không chạy thực nghiệm mới.

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
