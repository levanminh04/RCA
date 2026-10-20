# T-032 — Lần theo nguyên nhân thất bại xếp hạng

- **Trạng thái:** Minh duyệt SPEC và thực hiện ngày 09/10/2026, lời duyệt "ĐÃ CHỐT" (Q-93); chọn A′, được chạy khi lõi đạt điều kiện trong SPEC. Ngân sách theo SPEC, tối đa 8 GiB mới; thực hiện qua nhiều phiên trên EC2 3.26.62.217. Nội dung thiết kế đã khóa.
- **Người làm:** Codex (Minh chọn ngày 09/10/2026).
- **Người phản biện:** Claude (Minh chọn ngày 09/10/2026).
- **Thuộc gói MRP:** P4 — **Cổng:** G2.
- **Thiết bị tính toán đề xuất:** EC2 3.26.62.217, key2.pem. Laptop điều khiển và nhận kết quả.
- **Phụ thuộc:** kết quả đã đóng của T-024, T-026 và T-028; không cần đợi T-033. Hai task có thể tính toán song song trên hai EC2. Kết quả dùng cho tổng hợp G2 và căn cứ P5–P6; không tự duyệt G2.

## Mục tiêu

Task phục vụ RQ2 và P4 trong docs/MRP.md: hiểu những bước của phương pháp RCA làm mất hoặc đánh giá sai thông tin, thay vì chỉ ghi ca nào xếp hạng sai. Nguồn trực tiếp là docs/reference/sources/advisor-2026-09-23.md §1, đoạn yêu cầu hiểu sâu phương pháp, mở rộng thực nghiệm và chỉ ra hạn chế; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md §2, DT18-NV2 và DT18-NV3.

Task lần theo cơ chế của các phương pháp đã chạy trên dev. Câu trọng tâm: trong những ca caller (dịch vụ gọi) đứng trên root (thành phần gốc), phương pháp chấm thời gian chờ dịch vụ phụ thuộc thành bất thường của caller, hay bản thân cách chấm điểm/tập ứng viên ưu tiên caller? Xét thêm đầu vào thiếu, bước lọc và tài nguyên chung; các cơ chế có thể cùng tồn tại. Thứ hạng hoặc độ dài span riêng lẻ không phân xử được các giải thích này.

Đầu ra phải phân biệt cơ chế tính toán đã xác nhận với nguyên nhân vật lý còn mở; chỉ rõ quan hệ giữa dịch vụ có thể bổ sung thông tin ở bước nào. Theo chỉ đạo Minh, task phải đánh giá khả năng đo chờ của từng dataset và tạo bảng theo ca đủ để tổng hợp G2 dùng trực tiếp, không phải đo mới. Minh đã chọn phương án can thiệp tính toán A′ trong thiết kế; quyền chạy và ngân sách vẫn chờ duyệt riêng. Hoàn thành task không mặc nhiên có đủ bằng chứng cho mọi nguyên nhân sai, nhãn lan, lựa chọn phương pháp mới hoặc đóng RQ2/G2.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi và nguồn yêu cầu | Kết luận/lựa chọn cần phân xử; giải thích khác | Phép kiểm và bằng chứng cần có | Kết quả hỗ trợ, bác bỏ hoặc chưa phân xử | Phần còn thiếu, quyết định phụ thuộc và hướng xử lý |
|---|---|---|---|---|
| P4: thông tin của root mất ở đâu? | Thiếu kênh đầu vào; bị lọc cột; không ánh xạ vào thực thể; bị loại khỏi ứng viên; có đầu vào nhưng điểm thấp | Lần theo kênh gốc → cột giữ/bỏ → thực thể quan sát → ứng viên → điểm và hạng, ở ca sai và ca đúng tương ứng | Xác định được bước mất thông tin thì hỗ trợ kết luận tại bước đó; root vẫn còn không bác bỏ lỗi ở bước chấm | Thiếu trung gian nào phải ghi chính xác; ảnh hưởng quyết định sửa adapter, bổ sung quan sát hoặc xử lý trong phương pháp |
| P4: vì sao caller có điểm/hạng cao hơn root? | Tín hiệu caller lệch hơn; công thức/tổng hợp hoặc khóa hòa tạo ưu thế; root thiếu ứng viên; nhiều cơ chế cùng tồn tại | Giá trị gốc, từng thành phần điểm, phép tổng hợp, khóa sắp xếp và nhóm hòa của chính phương pháp | Chỉ kết luận về bước thực sự tạo chênh lệch; hạng không đổi không chứng minh điểm không phản ứng | Nếu cần can thiệp để phân xử ưu thế, trình đúng nhóm ca, thành phần giữ/đổi, dự đoán đối lập và chi phí |
| P4: tín hiệu caller có phải thời gian chờ phụ thuộc? | Chờ đồng bộ; xử lý tại caller; chạy song song/bất đồng bộ; thiếu span; tải hoặc tài nguyên chung | Đọc schema/semantics trace; đối chiếu tín hiệu phương pháp dùng với khoảng thời gian span, quan hệ cha–con, coverage và các kênh liên quan | Parent–child hoặc phần duration chồng lấn chỉ là quan sát; chỉ gọi là chờ khi có bằng chứng về quan hệ chờ | Thiếu loại span, thời điểm hoặc trạng thái chờ thì giữ nguyên nguyên nhân vật lý OPEN; nêu instrumentation cần thiết và hệ quả cho P9a |
| P4: đặc tính ấy có riêng cho nhóm sai không? | Đặc tính chung của thuật toán cũng có ở ca đúng; khác biệt do điều kiện đầu vào/cửa sổ | Đối chiếu ca đúng và ca sai cùng dataset, phương pháp, đường xử lý và điều kiện đầu vào; không ghép theo kết quả caller đứng trên root | Có khác biệt ở bước trung gian mới hỗ trợ giải thích có điều kiện; đặc tính có ở cả hai không đủ quy nguyên nhân cho mọi ca sai | Không có ca đúng tương ứng phải báo thiếu đối chứng, giữ giới hạn kết luận và trình phần bổ sung cần thiết |
| P4 → P5–P6: quan hệ có thể giúp ở đâu? | Quan hệ bổ sung thông tin bị thiếu; hoặc lỗi thuộc dữ liệu/cài đặt nên đồ thị chưa giải quyết được | Nối hạn chế có bằng chứng với thông tin quan hệ cần thêm và phép tính dự kiến sử dụng nó, cùng phương án khác | Đủ căn cứ đề xuất ứng viên khác với đã chứng minh lợi ích của đồ thị | Đối chứng bỏ quan hệ/đồ thị ngẫu nhiên thuộc đánh giá cơ chế đồ thị; không trì hoãn phân tích baseline để đợi chúng |

## Đầu vào

- Giao thức, tập ứng viên, cách chấm và nguồn dữ liệu đã duyệt trong tasks/T-022-giao-thuc-p3/ và results/T-022/.
- Bản ghi xếp hạng đã đóng của T-024 trên RE2-TT dev, T-026 trên Nezha-OB dev; bản đồ hạn chế và trung gian T-028. Nguồn tại results/T-024/, results/T-026/, results/T-028/.
- Code adapter trong src/p3/ và code phương pháp ở revision đã ghi trong results/T-031/moi-truong.json; với phần Nezha theo nguồn T-026. Không dùng bản mới nhất thay bản đã tạo kết quả.
- Phạm vi: toàn bộ tập dev và các phương pháp/cấu hình chính đã được duyệt trong ba task nguồn. Giữ ERROR, NO_EVIDENCE, UNSUPPORTED và các bảng độ nhạy; không chọn bỏ nhóm khó theo điểm.
- Manifest nền: results/T-029/runs/compare-rca-preparation-001/manifest.json cho bản ghi P3 được dẫn; manifest lượt sửa T-028 và manifest T-026 tương ứng với nguồn thực tế. Lấy tên file từ manifest hoặc liệt kê thư mục, không suy tên từ trí nhớ.
- Trước khi dùng mỗi đầu ra cũ, kiểm hash theo manifest phù hợp. Lệch thì dừng phần phụ thuộc, báo Minh và ghi trong LOG khi đã có quyền.
- Chỉ đọc phần dev nằm trong allowlist đã duyệt. Không mở data/locked/, test hoặc dataset giữ ngoài.

Môi trường tính toán phải khớp môi trường đã dùng cho phương pháp: đọc results/T-031/moi-truong.json → /lenh_chay và /moi_truong, cùng nguồn tương ứng T-026. Dùng Python với -B -X utf8 và PYTHONDONTWRITEBYTECODE=1. Trên EC2 thay đường dẫn bằng vị trí môi trường/code đã kiểm, không tự cài package hoặc đổi phiên bản.

## Đầu ra

Trong results/T-032/:

- nguyen-nhan-xep-hang.md: trả lời các câu hỏi trên; tách quan sát, suy luận, cơ chế xác nhận, ứng viên, quyết định cần Minh và OPEN.
- chuoi-bang-chung.json: theo ca/phương pháp/cấu hình/seed, nối đầu vào → xử lý → trung gian → điểm/nhóm hòa/hạng; có đường dẫn và con trỏ nguồn.
- bao-phu-nhom.json: danh mục nhóm, đơn vị đọc tay không trùng, nhóm được mỗi đơn vị phủ, cặp đối chứng và điều kiện ghép/thiếu. Mỗi nhóm bắt buộc có liên kết, không tự bỏ nhóm sau khi thấy kết quả.
- phan-xu-caller-root.json: mọi ca/cấu hình/seed có cờ M5 trong nguồn, từng caller liên quan, trạng thái bằng chứng tính toán, bằng chứng tín hiệu, khả năng đo chờ và phần chưa biết. Có bảng đếm theo dataset/phương pháp/ô, mẫu số và số thiếu; không là nhãn lan.
- kha-nang-do-trace.json: kiểm kê trường thô so với payload phương pháp, semantics instrumentation và coverage theo ca; kết luận từng dataset đo được/đo được một phần/không đo được đối với câu hỏi chờ root, kèm lý do và đầu vào thiếu.
- can-thiep-tinh-toan.json: chỉ tạo sau khi Minh duyệt chạy A′; liên kết về J0 lõi, lưu W-native/W-unit, invariant, trạng thái, điểm/nhóm hòa và giới hạn theo ca; giữ mọi lượt kể cả lỗi, không thay kết quả gốc.
- doi-chieu-dung-sai.json: bảng đối chiếu tự động toàn bộ phạm vi, các cặp ca/điểm đối chiếu bằng điều kiện đầu vào, trường hợp không có đối chứng tương ứng.
- coverage-trace.json: schema, kênh quan sát, liên kết parent/child, chồng lấn, span thiếu và giới hạn cửa sổ; không đặt tên chỉ số là thời gian chờ khi chưa có căn cứ.
- doc-tay.md: lần theo ca sai và ca đúng tương ứng cho các nhóm quan trọng, trình chuỗi bằng chứng và giải thích cạnh tranh.
- kiem-tiep.md: mỗi câu cần kiểm thêm ghi giải thích cạnh tranh, phép can thiệp/thu thêm cụ thể, yếu tố giữ cố định, dự đoán phân biệt, phạm vi, chi phí và quyết định bị ảnh hưởng. Không dùng danh sách chung chung “cần nghiên cứu thêm”.
- scripts/ và runs/: wrapper chẩn đoán, lệnh, cấu hình, thời gian, manifest và trung gian; giữ mọi lượt kể cả hỏng.

Báo cáo phải nêu đủ năm đầu ra P4: hạn chế xác nhận và điều kiện; lỗi cài đặt/thiếu đầu vào; hạn chế giả định/cách tính; thông tin quan hệ có thể bổ sung; câu chưa trả lời và bằng chứng thiếu. Tách dữ liệu, giao thức, adapter/cài đặt và phương pháp. Hạn chế dữ liệu xác nhận phải nêu hệ quả đánh giá và yêu cầu quan sát FlashTicket; không suy collector có thể khôi phục dữ liệu chưa từng được ghi.

## Phạm vi ghi

Phạm vi dưới đây chỉ có hiệu lực sau khi Minh duyệt thực hiện SPEC:

- results/T-032/, dùng thư mục lượt mới trong scripts/ và runs/.
- tasks/T-032-g2-nguyen-nhan-xep-hang/LOG.md: chỉ nối thêm.
- Duy nhất dòng T-032 trong docs/STATE.md.
- Trên EC2 3.26.62.217: chỉ thư mục mới ~/rca/T-032/.
- docs/WHY.md: chỉ nối WHY-40 đúng nội dung phụ lục được Minh duyệt, trước khi dùng lựa chọn trong kết quả.

Code dùng chung, môi trường và dữ liệu cũ trên EC2 chỉ đọc. Nếu cần đầu vào/code cho task, chép đúng phần allowlist vào thư mục mới, kiểm hash nguồn và đích; không ghi vào các task cũ. Laptop chỉ điều khiển, đọc tài liệu và nhận kết quả; toàn bộ tính toán nghiên cứu trên EC2.

Các lượt sửa nháp ngày 09/10 chỉ được sửa hai SPEC và nối DECISIONS theo Q-91/Q-92; không ghi STATE, WHY chính thức, LOG, dữ liệu hoặc đầu ra nghiên cứu. Người phản biện chỉ ghi bản lượt được Minh cho phép, hoặc trả lời trong chat.

## Nhóm bắt buộc, đối chứng và đơn vị đọc tay

- Khóa danh mục từ T-028: dataset × cấu hình chính/phương pháp × k đã có × từng cờ đa nhãn M1–M6 có ca, M0 chưa phân loại; thêm từng trạng thái non-OK có bản ghi. Giữ các bảng độ nhạy cũ ở phần đối chiếu, không mở thêm cấu hình chính. Cờ chỉ dùng để tổ chức kiểm, chưa là nguyên nhân.
- Bảng tự động và bảng caller/root phủ toàn bộ phạm vi. Đơn vị đọc tay là ca × cấu hình phương pháp × đường xử lý; giữ seed riêng nếu trung gian/trạng thái khác. Một lần đọc có thể phủ nhiều k/cờ, nhưng phải trỏ riêng kết luận và đối chứng của mỗi nhóm; không gộp hạng/điểm giữa seed.
- Mỗi nhóm có ít nhất một đơn vị sai để lần theo và một đối chứng đúng cùng phương pháp nếu có. Khóa chọn bằng điều kiện và opaque_id nhỏ nhất khi tương đương trước khi diễn giải cơ chế. Bắt buộc cùng dataset, cấu hình, quy tắc cửa sổ F và loại đầu vào/adapter; ưu tiên cùng ô, kênh quan sát, quy mô và coverage. Thuộc tính đang phân xử có thể khác, phải ghi rõ; không ép ca đúng mang cờ về mặt cấu tạo chỉ có ở ca sai.
- Không ghép theo chênh điểm, caller đứng trên root hoặc kết quả can thiệp. Không có ca đúng hợp điều kiện thì ghi điều kiện thiếu và giới hạn suy luận; vẫn lần theo ca sai. Đối chiếu cùng ca với phương pháp khác là bổ sung: chỉ cho thấy tín hiệu mà phương pháp kia sử dụng, không chứng minh phương pháp đang xét chấm sai hoặc thay đối chứng cùng phương pháp.
- Nhóm khác đường xử lý hoặc xuất hiện phản ví dụ ở bảng toàn bộ phải có đơn vị đọc thêm; không lấy ca đại diện để đếm số ca đã xác nhận cơ chế. Mọi ca M5 phải có trạng thái theo ca, dù phần đọc giải thích chi tiết được tái dùng.

Dự trù từ nguồn đã lưu: 44 nhóm đa nhãn, 38 nhóm theo nhãn chính, 8 dòng dataset/phương pháp/k có non-OK, tổng M5 qua k là 118 lượt; nguồn results/T-028/runs/phan-hoi-review-001/summary-tables.json → /mechanism_tables, lọc group_field=overall và đếm trường multi/primary/n_non_OK. Hợp ca có M5 ở k=1 hoặc k=5 còn 80 ca × phương pháp; nguồn ca-sai.json cùng lượt → /main_rows/*/mechanisms/{1,5}/assignment/multi. Hai file kiểm hash theo manifest.json → /outputs. Đây không phải 118 ca độc lập, không phải số ca đọc tay sau ghép đối chứng; số seed cần đọc giữ riêng. Đơn vị đọc tay cuối cùng và số bổ sung theo đường xử lý được ghi trong bao-phu-nhom.json trước bước đọc tay, không cắt số để vừa một phiên.

## Phân xử caller/root và khả năng đo chờ

Với từng đơn vị M5, ghi các trường bằng chứng độc lập, cho phép cùng tồn tại:
- Bước tập ứng viên/lọc/khóa hòa hoặc thành phần chấm nào tạo ưu thế caller; xác nhận ở mức tính toán, chưa phân xử, hoặc không áp dụng, kèm chuỗi và phản ví dụ.
- Caller tự có tín hiệu vượt quy tắc native hay chỉ nhận bằng chứng qua trace chứa bất thường ở operation khác; mức liên hệ caller–descendant/root, counts và coverage, cùng khả năng tải chung/đầu vào chung.
- Khoảng span con chồng lấn quan sát được; bằng chứng riêng về chờ đồng bộ nếu thực sự có; phần thời gian/quan hệ không quan sát được. Không đổi tên chồng lấn thành chờ.
- Kết luận nào được hỗ trợ, giải thích nào bị bác bỏ, giải thích còn mở và đúng trung gian/phép kiểm cần bổ sung. Không buộc một nguyên nhân độc quyền.

Bảng tổng hợp ghi n/N riêng theo dataset, phương pháp, cấu hình, k và ô; N là số ca sai OK, số ca M5 đủ điều kiện hoặc toàn cohort tương ứng, khai ngay bên số. ERROR/UNSUPPORTED/thiếu coverage nằm trong bảng riêng và mẫu số toàn cohort, không biến thành cơ chế đã phân xử. Các trường bằng chứng chồng lấn không cộng thành tỷ lệ nguyên nhân. K4 của tổng hợp G2 có thể dùng trực tiếp bảng này, nhưng số M5 hoặc số chồng lấn không trả lời “lan có đáng kể”.

Đánh giá trace trên mọi ca dev của từng dataset: đọc schema thô, trường còn/đã mất qua adapter, đơn vị thời gian/đồng hồ, resolve parent, biên cửa sổ, sampling, loại span và semantics được tài liệu instrumentation hỗ trợ. Mỗi ca ghi:
- **Đo được:** có quan hệ cùng request và bằng chứng semantics/interval của chờ đồng bộ đã kiểm, phân biệt được xử lý caller, song song/bất đồng bộ và thiếu span trong điều kiện được nêu.
- **Đo được một phần:** có quan hệ và khoảng quan sát hợp lệ, đo được chồng lấn/coverage nhưng thiếu bằng chứng để gọi khoảng ấy là chờ hoặc để loại giải thích khác.
- **Không đo được:** thiếu quan hệ/thời điểm/semantics hoặc coverage khiến câu hỏi chờ root không phân xử được; vẫn giữ những đại lượng khác đo được.

Kết luận dataset giữ sự khác nhau giữa các ca, nêu số ca từng mức và giới hạn suy rộng. Payload phương pháp thiếu trường không chứng minh file thô thiếu trường; kiểm file thô allowlist và nguồn instrumentation trước khi kết luận hạn chế dataset. Parent–child, SpanKind hoặc duration riêng lẻ chưa chứng minh caller đang await root. Không gọi phần parent chưa được con phủ là self-time. Nếu phải định nghĩa nhãn lan sau G2, cần nêu trước bằng chứng chờ/đồng hồ/coverage, đoạn nền phù hợp và cách kiểm ngưỡng; task này không định nghĩa nhãn, không chọn ngưỡng lan.

## Các bước

1. **Kiểm nguồn và đọc code/trung gian đã lưu.** Kiểm manifest; lập bảng những trung gian đã có và còn thiếu trên toàn bộ phạm vi, gồm nhóm lỗi/không hỗ trợ. Đọc code thật trước khi quyết định chạy lại.
2. **Phát lại đúng phần thiếu tại cửa sổ F đã khóa.** Dùng cùng cấu hình, seed, tiền xử lý, cửa sổ, ứng viên và dữ liệu. Wrapper nằm trong task, không sửa lõi phương pháp. Đối chiếu trạng thái, điểm/khóa sắp xếp, nhóm hòa và thứ tự với bản ghi đóng băng trước khi dùng trung gian. Lệch thì dừng phần phụ thuộc để tìm nguyên nhân, không thay số cũ.
3. **Lần theo chuỗi của từng phương pháp.**
   - BARO: tiền xử lý → median/IQR → robust-z → chỉ số đóng góp cao nhất và điểm thực thể.
   - SimpleRCA: bằng chứng metric/trace/log → từng thành phần → phép cộng/tổng hợp → hạng.
   - MicroRank: ngưỡng operation → nhóm trace → PageRank/count → spectrum → điểm.
   - TraceRCA: mean/std → tập bất thường → support/confidence → ji → lọc hữu hạn → điểm/hạng.
   - CIRCA: đầu vào hồi quy/quan hệ → residual/RHT → DA → khóa xếp hạng; giữ bản gốc theo quyết định đã khóa, không sửa vấn đề làm tròn.
   - TORAI B: tín hiệu nhiều nguồn → severity → cụm → RCD/nhánh dự phòng → nhóm hạng.
4. **Đối chiếu ca đúng/sai theo điều kiện.** Lập bao-phu-nhom.json theo mục nhóm bắt buộc; đọc ca sai/đúng và các đường xử lý khác nhau, giải thích trường hợp không có đối chứng. Bảng caller/root phủ tất cả đơn vị M5. Với MicroRank lưu own abnormal và context-only coverage của mọi operation trước nối nhãn; với TraceRCA lần theo a, n, H và phép max service từ công thức native, không gọi phân rã đại số là thí nghiệm can thiệp.
5. **Đọc semantics trace trước khi diễn giải thời gian.** Với nhóm caller/root cần phân xử, tính hợp các khoảng con được quan sát nằm trong parent, phần parent chưa được các khoảng ấy phủ, chồng lấn và thiếu/bị cắt span. Không lấy tổng duration con làm thời gian chờ, không gọi phần chưa phủ là self-time hoặc tự sinh nếu schema không hỗ trợ. Đối chiếu metric/log và tín hiệu mà phương pháp thực sự đã dùng.
6. **Can thiệp tính toán A′ sau duyệt chạy riêng.** Minh đã chọn A′ trong thiết kế. Chỉ sau phần lõi phát lại đạt, danh mục/đối chứng đã khóa và quyền chạy/ngân sách được duyệt; thực hiện mục riêng dưới đây, tách thư mục lượt và bảng khỏi nguồn lõi. Chưa duyệt chạy thì ghi chưa chạy, không tự thực hiện.
7. **Tổng hợp cơ chế và quyết định.** Với mỗi kết luận quan trọng, ghi điều kiện X, bước Y, thông tin Z, ca đúng/sai, bằng chứng hỗ trợ/bác bỏ, giải thích khác và phần chưa phân xử. Nêu cách thông tin quan hệ có thể tác động vào đúng bước, hoặc lý do cần sửa dữ liệu/cài đặt trước. Ghi phần can thiệp còn cần vào kiem-tiep.md.

Bước 2 chỉ phụ thuộc việc xác định thiếu trung gian và kiểm nguồn ở bước 1; các phương pháp độc lập có thể xử lý song song trong ngân sách. Không chờ T-033. Tính đặc trưng/chỉ số cho mọi thực thể trước khi nối nhãn root và loại lỗi để phân tích. Cửa sổ F có sử dụng mốc theo giao thức chế độ (a); không gọi phân tích này hoàn toàn không dùng nhãn.

## Phương án can thiệp tính toán A′ — đã chọn thiết kế, chưa duyệt chạy

Minh chọn A′ khi duyệt gói sửa nháp ngày 09/10/2026 (Q-92): chỉ so gói trọng số trên dữ liệu gốc J0 của MicroRank. Phương án B không chạy can thiệp đã được xét; việc chọn A′ không tự cấp quyền chạy hoặc ngân sách. Bỏ phép J/hoán đổi/batch khỏi thiết kế thực hiện; không tạo trace/cờ mới.

**Vì sao kiểm MicroRank:** src/microrank/__init__.py gán cờ từng span rồi đưa cả trace có bất kỳ cờ bất thường vào nhóm anomaly. Downstream dùng mọi operation trong trace để tính coverage/count và PageRank, rồi đưa trọng số vào DStar2. A′ giữ dữ liệu/count để kiểm đóng góp của toàn gói trọng số vào ưu thế caller. Phần lõi vẫn lần theo own abnormal (bất thường riêng), context-only (chỉ có bằng chứng qua trace chứa bất thường khác), quan hệ và ca đúng; A′ không thay thế phần ấy. BARO/CIRCA/SimpleRCA/TORAI/TraceRCA vẫn giữ đầy đủ lõi và đối chứng, không được miễn nghĩa vụ vì chọn MicroRank.

**Phạm vi A′ sau duyệt chạy:** ca đọc tay MicroRank đã khóa từ nhóm M5 và đối chứng cùng điều kiện trên mỗi dataset. Chỉ dùng ca phát lại OK có đủ hai nhóm trace N/A; ghi mọi ca không đủ điều kiện hoặc thiếu điểm cặp đang diễn giải. Không cần điều kiện có phép hoán đổi. Không chọn ca theo kết quả W; tính cho mọi operation/service của ca trước khi nối nhãn root và chọn cặp diễn giải. Bảng tự động own abnormal/context-only của phần lõi vẫn phủ mọi ca.

**Giữ và đổi trên bản sao trung gian:**
1. J0 giữ bảng after, duration/cờ native, baseline, cửa sổ, membership/số trace N/A, graph, counts/support, mapping operation→service và tập khóa ứng viên. W-native dùng trọng số đã xác minh trong lõi của chính J0.
2. W-unit đặt trọng số bằng 1 chỉ cho operation có mặt trong dictionary trọng số của từng nhóm N/A, tại đầu vào calculate_spectrum_without_delay_list trong src/microrank/official.py. Không thêm operation vắng hoặc đổi nhánh thiếu. Giữ tracecounts, số trace, spectrum_method='dstar2', epsilon và công thức native của operation thiếu nhóm, gồm normal-only. Không đặt mọi ef/ep/nf bằng counts bằng tay vì các nhánh thiếu có công thức riêng.
3. Tính spectrum, vector điểm operation và ánh xạ điểm service bằng đúng phép max/khóa hòa của lõi; lưu operation đạt max ở từng nhánh. Hook chỉ thay dictionaries trọng số trong lời gọi spectrum trên bản sao, không gọi lại detector hoặc đổi PageRank lõi. Tập khóa ứng viên phải giữ; mất khóa hoặc số học không hợp lệ thì giữ lỗi và không dùng contrast đó.
4. Đây là phép so tất định trên J0, không có RNG/seed hoán đổi. Giữ seed/config nguồn khi cần provenance, không biến hai nhánh thành hai ca độc lập. W-unit thay cả phân bố tương đối và thang trọng số giữa N/A: native weight phụ thuộc vector PageRank và tổng vector riêng của nhóm. Phép so không tách riêng cạnh gọi có hướng, centrality hoặc prior và không là đối chứng “không đồ thị” của phương pháp mới.

**Chỉ số và dự đoán khai trước:** lưu J0/counts/support, trọng số native/unit, ef/ep/nf, trạng thái nhánh thiếu, vector điểm operation/service, operation đạt max và nhóm hòa/cận hạng. Với cặp caller/root có điểm hữu hạn, lưu điểm thô và margin (s_c−s_r)/(|s_c|+|s_r|) ở hai W, cùng ΔW=margin_native−margin_unit; mẫu số 0 là N/A. Không chỉ báo Hit@k hoặc tăng hạng root.
- Margin native>0 nhưng unit≤0 hỗ trợ việc gói trọng số tạo ưu thế caller trong contrast trên J0 này; phải lần theo spectrum và operation đạt max, không quy riêng cho cạnh hoặc gọi là nguyên nhân vật lý.
- Cả hai>0 và native lớn hơn chỉ cho thấy gói trọng số khuếch đại ưu thế trong contrast này, không gọi “nguyên nhân chủ yếu”. Unit>0 cho biết counts/grouping và phép max cố định đủ tạo ưu thế; không phân biệt counts đến từ caller tự bất thường, context của operation khác hay chờ root.
- Chênh bằng 0 là quan sát hợp lệ ở endpoint đã khai, không tự bác bỏ mọi tác dụng trọng số. Trọng số đồng tỷ lệ chưa đủ để gọi contrast vô thông tin: xét tỷ lệ giữa hai nhóm, nhánh epsilon/thiếu support và phép max; chỉ báo bất biến đã kiểm cho đại lượng cụ thể. Báo riêng toàn hòa, điểm không hữu hạn, thiếu root hoặc margin N/A; không tự gán root=0 hay bỏ ca khỏi mẫu số.
- Trên J0, phần lõi đối chiếu cờ/excess caller với descendant resolve được, own abnormal/context-only coverage, khoảng span quan sát và ca đúng tương ứng. Liên hệ có thể do tải chung/nguyên nhân chung; không là bằng chứng chờ hoặc lan vật lý. Thiếu baseline/nhánh điều kiện thì ghi thiếu, không bịa xác suất.

**Kiểm không có kết quả đóng băng:** J0/W-native khớp trạng thái, spectrum, điểm/khóa, nhóm hòa và thứ tự của lõi. Sham sao chép cùng trọng số phải giữ downstream. Trước diễn giải W-unit, kiểm invariant J0/counts/support/ứng viên và scalar oracle/fixture nhỏ tính tay DStar2 riêng cho đủ hai nhóm, thiếu một nhóm và hòa/zero denominator theo hành vi native. Kiểm ánh xạ max service khi operation đại diện đổi. Nhánh mới kiểm đúng công thức, trạng thái và tính hữu hạn, không buộc khớp P3; giữ bản sao gốc có hash và mọi lượt lỗi. Không thay epsilon hoặc chữa điểm để đủ bảng.

**Giới hạn và nghĩa vụ còn lại:** A′ chỉ kiểm toàn gói trọng số trong các ca đủ điều kiện, không phân xử đồng bất thường riêng caller–root hoặc caller chờ root. J một cặp và batch cặp rời giữ số trace N/A chỉ tác động trace có toàn bộ cờ bất thường trong bundle được chuyển sang trace bình thường; không phá sự đồng bất thường giữa các operation khác nhau, nên đã bỏ. Phần lõi vẫn phải đọc đủ nhóm quan trọng và ca đúng. Nếu chưa phân xử được, kiem-tiep.md phải chỉ rõ đã có/thiếu trung gian hoặc semantics nào, giải thích cạnh tranh, phép chạy/thu thêm cụ thể, yếu tố cố định, dự đoán, phạm vi, chi phí và quyết định P5–P6/G2 phụ thuộc. Phân biệt chưa chạy, chưa đọc với dữ liệu không thể phân xử; không chỉ ghi OPEN hoặc coi chọn A′ là đã giải quyết caller/root.

## Kiểm đúng đắn

- Kiểm hash đầu vào cũ và hash hai đầu khi chép sang EC2.
- Mỗi lần phát lại dùng làm bằng chứng phải khớp bản ghi đóng băng ở trạng thái, điểm/khóa, nhóm hòa và thứ tự. Wrapper chỉ quan sát trung gian, không đổi phép tính.
- Kiểm kênh/cột, shape và giá trị hữu hạn ở đầu vào thật của từng thành phần, gồm đường xử lý lỗi/nhánh dự phòng. Không chỉ đối chiếu hạng cuối.
- Phép tính khoảng trace kiểm trên trường hợp lồng nhau, song song, bất đồng bộ, thiếu parent và span chạm biên cửa sổ; kiểm chỉ số phản ánh đúng khoảng quan sát chứ không tự xác nhận semantics chờ.
- Ca đúng phải có điều kiện tương ứng với ca sai, tránh dùng đặc tính chung làm nguyên nhân riêng. Kiểm bao-phu-nhom trỏ đủ nhóm và trường hợp không ghép được; ca đại diện không chứng nhận các ca chưa lần theo.
- Kiểm bảng phân xử phủ từng ca/cấu hình/seed M5 và đối chiếu mẫu số với nguồn; tách chồng lấn, cơ chế chấm và chờ. Kết luận khả năng đo phải có bằng chứng schema thô/adapter/semantics/coverage theo ca.
- A′ đã chọn trong thiết kế nhưng chưa duyệt chạy không được coi là đã có kết quả. Kiểm độc lập/invariant/sham/nhánh thiếu đúng mục A′ trước diễn giải; không đổi wrapper lõi. Thiếu bằng chứng caller/root vẫn phải có phần cần bổ sung và quyết định phụ thuộc, không dùng A′ thay phần lõi.
- Mọi số trong báo cáo có đường dẫn và con trỏ JSON hoặc lệnh đã chạy kèm kết quả. Phân biệt số cờ, số ca và cơ chế; không cộng cờ chồng lấn.
- Các kiểm công bố/không nhãn đã hợp lệ ở task nguồn được dẫn bằng nguồn và manifest; không gọi lần phát lại này là tái lập bài mới.
- Trước nghiệm thu, đối chiếu năm đầu ra P4 và mục tiêu DT18/cô. Giới hạn không tự miễn phép kiểm rẻ, cần thiết và trong quyền đã duyệt.

## Tiêu chí xong

1. Kiểm nguồn đạt, phát lại phần cần thiết khớp; không thay kết quả đóng băng.
2. Danh mục nhóm đã khóa được phủ bởi bảng toàn bộ và các đơn vị đọc tay/đối chứng theo điều kiện, hoặc chỉ đúng bước chưa biết, điều kiện thiếu và phép kiểm bổ sung cần Minh quyết. Mọi đơn vị M5 có trạng thái theo ca với mẫu số; không suy cơ chế toàn nhóm từ một ca.
3. Chỉ nhận cơ chế khi phân xử được giải thích liên quan bằng đầu vào → xử lý → trung gian → đầu ra; kết quả bác bỏ hoặc chưa phân xử được ghi đúng mức. Không ép nguyên nhân vật lý từ quan sát thời gian.
4. Báo cáo đủ năm mục P4; từng dataset có kết luận khả năng đo chờ và bảng theo ca đủ cho tổng hợp G2, điều kiện nếu sau G2 định nghĩa nhãn. Nêu quyết định P5–P6 được hỗ trợ tới mức nào; không định nghĩa nhãn/tỷ lệ lan.
5. A′ ghi rõ đã chọn thiết kế, quyền chạy và trạng thái thực hiện. Sau duyệt chạy, có đối chiếu W-native/unit trên J0, đầu ra/invariant/sham/nhánh thiếu/giới hạn đầy đủ theo ca. Chưa chạy hoặc contrast không định nghĩa thì giữ đúng trạng thái và hậu quả; không nhận đã kiểm trọng số. Câu caller/root còn thiếu có bằng chứng cần bổ sung cụ thể, không coi A′ trả lời toàn bộ câu hỏi.
6. LOG và checkpoint đủ để người khác tiếp tục qua nhiều phiên, kiểm toàn bộ diff/phạm vi ghi; cập nhật dòng task và prompt bàn giao theo docs/review-prompt.md.

Task xong không đồng nghĩa RQ2/G2 xong. Nếu phần còn thiếu ảnh hưởng lựa chọn phương pháp mới hoặc câu “lan có đáng kể”, trình phép kiểm và mức kết luận tương ứng; không tự bỏ câu hỏi.

## Không làm

- Không sửa baseline, giao thức, kết quả P3/P4 cũ, nhãn hoặc code/data dùng chung; không mở test.
- Chưa chạy lại toàn bộ lưới cửa sổ P1/P2. Nếu cần phân xử ưu thế chấm điểm, trình đúng nhóm/cửa sổ với tải, coverage, ứng viên và yếu tố giữ cố định; thay cửa sổ thời gian không phải tự động là can thiệp bỏ lỗi.
- Không dựng nhãn “lan/tự sinh” từ tỷ lệ duration. Nếu dữ liệu thiếu semantics chờ, nêu chính xác trường cần thu; chưa kết luận dataset là nguyên nhân từ cờ thiếu.
- Không đánh giá hiệu quả phương pháp đồ thị mới. Đối chứng bỏ quan hệ và đồ thị ngẫu nhiên dùng ở bước đánh giá cơ chế tương ứng.
- Không tự cập nhật SPEC T-034. Tổng hợp G2 cần quyết phạm vi “lan có đáng kể” từ bằng chứng của hai task, không suy từ việc task đã đóng.

## Qua nhiều phiên và lượt chạy dài

Minh quyết giữ cùng T-032 qua nhiều phiên (Q-91), ngoại lệ có chủ ý với AGENTS §5a.4 và yêu cầu một phiên ở §5. Không tạo task mới, không giảm phép kiểm để vừa phiên. Chỉ đạo này cho phép hình thức chạy dài/qua đêm; A′ đã chọn trong thiết kế, thực hiện và chi phí vẫn cần duyệt riêng.

| Chặng | Điều kiện bắt đầu | Checkpoint và điều kiện tiếp |
|---|---|---|
| Chuẩn bị | SPEC/thực hiện và ngân sách được duyệt; WHY-40 được phép nối | Danh sách source/manifest, nơi dữ liệu và môi trường trên EC2, dung lượng, cấu hình/hash, danh mục nhóm và bảng trung gian thiếu |
| Lõi theo phương pháp | Nguồn/khớp phát lại đạt cho phương pháp đó | Sau mỗi ca/seed ghi run/manifest/trạng thái và LOG; phương pháp độc lập có thể tiếp, không dùng trung gian của lượt lệch |
| Trace/đối chứng/đọc tay | Trung gian lõi của ca đạt | Mỗi đơn vị có nguồn, nhóm được phủ, đối chứng/thiếu và trạng thái phân xử; bảng còn việc chưa đọc |
| A′ sau duyệt chạy | Quyền chạy/ngân sách A′ được duyệt, J0/W-native khớp và phép kiểm mới đạt | Mỗi ca có hai W, invariant, spectrum/điểm, nhánh thiếu/operation max và lý do không hợp lệ; không ghi đè lõi |
| Tổng hợp | Các chặng liên quan đã kiểm hoặc OPEN có bằng chứng cụ thể | Báo cáo, kiểm nguồn/đếm/diff, nghĩa vụ còn thiếu cho G2/P5–P6, prompt cho Claude |

Lệnh chạy nền phải ghi PID, lệnh đầy đủ, đường môi trường, stdout/stderr, progress và vị trí kết quả trong thư mục riêng T-032; không dựa vào phiên SSH đang mở. Trước rời phiên ghi LOG: bước đã xong/đang chạy/chưa chạy, last command, ca/cấu hình/seed cuối hợp lệ, hash/manifest, vị trí process và câu cần Minh quyết. Người nhận tiếp đọc LOG, kiểm process và manifest/hashes trước; chỉ chạy phần thiếu, không khởi lại lượt đang chạy hoặc đã hợp lệ. Dừng phần phụ thuộc khi hash/khớp/invariant lệch, hết đĩa/RAM hay quyền chưa rõ; giữ lượt hỏng, LOG và trình giải pháp. Ba lần không tiến triển ở cùng chỗ thì dừng theo §5a, không tự tạo task mới.

## Chi phí ước lượng và ngân sách chờ duyệt

- Nguồn RE2 chính: results/T-024/ban-ghi-dua-vao-cham.json → /records/*/path; bản ghi được trỏ → /cost/wall_s. Tổng 3.120,781 giây, khoảng 52 phút, cho năm phương pháp trên laptop và TORAI B trên EC2; không là phép đo tất cả trên EC2 hiện tại. Kiểm index/record theo manifest compare-rca-preparation-001.
- Dữ liệu Nezha dự trù khoảng 1,04 GB: results/T-026/runs/full-001/source-integrity-final.json → /files/*/bytes. Trước chuyển phải kiểm nguồn, phần allowlist đã có trên từng EC2 và hash hai đầu; không chuyển lại phần hợp lệ. Tốc độ laptop→EC2 và EC2→EC2 chưa đo hiện tại; không suy từ tốc độ lịch sử. Báo route, số byte thiếu và dự toán từ phép đo nhỏ được duyệt trước chốt lượt lớn; chưa được chuyển trong lượt sửa nháp.
- **Chưa kiểm — giờ máy dự trù:** lõi RE2 2–6 giờ gồm wrapper/trung gian; Nezha 1–4 giờ riêng, chưa có đo phát lại tại EC2 này; chuyển dữ liệu tính riêng. A′ dự trù thêm 0,5–2 giờ máy cho lấy trung gian đã xác minh, tính spectrum/unit, lưu và kiểm theo ca; chưa đo trên EC2 này. A′ không thêm shuffle hoặc PageRank mới ngoài lõi; bỏ dự toán 2–8 giờ của nhánh J cũ. Đây là dự toán, không timeout hay bảo đảm.
- **Chưa kiểm — công agent:** viết/kiểm wrapper và bảng nguồn 8–16 giờ; đọc tay/đối chứng và khả năng đo trace 12–24 giờ; tổng hợp, tự kiểm và báo cáo 4–8 giờ. Phụ thuộc số trung gian tái dùng, đối chứng và đường xử lý; có thể tăng. Các khoảng là ước lượng để Minh duyệt, không số đo kết quả.
- Dự trù tối đa 8 GiB mới cho input/trung gian/tạm/lượt hỏng; kiểm chỗ trống thực tế trước chuyển/chạy, không xóa nguồn hoặc lượt cũ. Lưu trung gian đủ câu hỏi thay vì mọi bản raw/graph trùng; vẫn giữ manifest và mọi lượt.
- Bắt đầu một worker nặng; tối đa hai khi RAM thực tế cho phép và không chia sẻ trạng thái mutable của phương pháp. Không hứa thời gian chia theo worker. Hai task dùng hai EC2 độc lập; các phần tài liệu/đọc tay vẫn cần công.
- Minh đã chọn A′ trong thiết kế; duyệt thực hiện/ngân sách sau rà SPEC, gồm quyền chạy A′. Sau đo chuẩn bị cập nhật dự toán vào LOG trong cùng task; nếu vượt phạm vi/dung lượng được duyệt thì dừng trình, không tự tăng ngân sách hoặc giảm kiểm. Có thể chạy qua đêm khi đã duyệt; ghi progress từng ca ngay từ đầu.

## Rủi ro và điều chưa chắc

- **Chưa kiểm:** phát lại laptop → Linux/EC2 có thể lệch số học dù cùng revision/package/seed. Ghi máy, OS, kiến trúc, Python/package, BLAS, thread, hashseed, code và config nguồn/đích trong từng run. Giữ tiêu chí khớp tuyệt đối trạng thái, điểm/khóa, nhóm hòa và thứ tự của phần lõi; chỉ lệch số học cũng dừng phương pháp đó và trình Minh, không tự thêm tolerance hoặc quay về laptop. Rủi ro này có thể tăng chi phí và làm cơ chế của phương pháp ấy OPEN.
- **Chưa kiểm:** giả định có thể lấy trung gian bằng wrapper không đổi hành vi. Khi instrumentation ảnh hưởng trạng thái/thứ tự số học, kết quả phát lại có thể lệch; không dùng trước khi kiểm khớp. Kết luận cơ chế phụ thuộc vào việc khớp này.
- **Chưa kiểm:** trace có đủ semantics để tách chờ và xử lý tại caller. Span bất đồng bộ, song song, sampling hoặc clock có thể làm suy luận sai. Không biết trước khi đọc schema và coverage; phần nguyên nhân vật lý và yêu cầu quan sát phụ thuộc.
- **Chưa kiểm:** có đủ ca đúng tương ứng ở mọi nhóm. Nếu không, vẫn lần theo tính toán nhưng không gọi đặc tính ấy là nguyên nhân riêng của nhóm sai.
- Tính toán có thể chỉ xác nhận bước chấm/lọc, chưa xác định nguyên nhân vật lý. Kiểm tiếp phải có giả thuyết cạnh tranh và dự đoán phân biệt, không chuyển OPEN thành căn cứ thiết kế đã xác nhận.

## Phụ lục — dự thảo WHY-40

**Chọn:** đọc code/trung gian trước; phát lại đúng phần thiếu tại F đóng băng; khóa nhóm bắt buộc từ cờ đa nhãn/non-OK, đọc đơn vị không trùng với đối chứng cùng điều kiện, lập trạng thái từng ca M5 và khả năng đo chờ. Đối chiếu khác phương pháp chỉ bổ sung bằng chứng kênh. A′ đã được Minh chọn trong thiết kế: giữ J0, so W-native với W-unit tại đầu vào spectrum; chưa là quyết định chạy.

**Vì sao:** phải biết bước nào tạo mất thông tin hoặc chênh điểm trước khi đề xuất xử lý. Caller đứng trên root hoặc duration tăng không phân biệt chờ phụ thuộc, xử lý tại caller, coverage và cách tính điểm.

**Phương án đã xét:** đọc mỗi k/cờ như ca độc lập (lặp công và dễ đếm trùng), chỉ đọc một ca rồi suy cả nhóm (thiếu coverage), dùng phương pháp khác xếp đúng thay đối chứng (khác kênh/công thức), can thiệp mọi phương pháp hoặc hạ duration/xóa caller (đổi nhiều yếu tố, dễ cho kết quả hiển nhiên), xáo trace TraceRCA giữ counts (bất biến theo công thức). Chọn ánh xạ nhóm và lõi toàn bộ, kèm A′ chỉ đổi toàn gói trọng số MicroRank trên J0. Đã xét J một cặp và batch cặp rời: điều kiện giữ số trace N/A và đổi partition giới hạn phép đổi vào sole-trigger bundle; không thay đồng bất thường giữa các operation khác nhau, nên bỏ khỏi thiết kế. B không can thiệp đã được xét nhưng không được chọn; giữ counts/nhóm gốc và đổi W cho câu hỏi trọng số cụ thể, không nhận phân xử toàn bộ caller/root. Đã xét thêm chạy toàn bộ P1/P2 trước khi hiểu bước chấm; đặt nhãn lan/tự sinh theo tỷ lệ duration; chỉ đọc đầu ra đã lưu. Lưới cửa sổ chưa tự phân xử cơ chế; tỷ lệ duration không xác định semantics chờ; chỉ đọc có thể thiếu trung gian ở bước quyết định. Phát lại giới hạn đúng phần thiếu và kiểm khớp giữ được câu hỏi mà giảm chi phí.

**Bằng chứng:** MRP P4, DT18-NV2/NV3, hướng dẫn cô §1 và đường tính trong code phương pháp ở revision đã tạo P3. Chưa có kết quả task này; lựa chọn là kế hoạch kiểm, không xác nhận giả thuyết.

**Kết luận phụ thuộc:** căn cứ cơ chế tính toán/ứng viên P5–P6, đầu vào K4 của tổng hợp G2 và yêu cầu quan sát FlashTicket; nguyên nhân vật lý và lợi ích đồ thị vẫn cần bằng chứng tương ứng. A′ được chọn không biến câu còn mở thành đã xác nhận. Chỉ phép so toàn gói weighting được hỗ trợ; không quy riêng cạnh/prior hoặc nguồn vật lý của counts. Có thể có tương tác với nhánh thiếu support và operation đạt max service, phải lưu trung gian. Khi phần lõi chưa phân xử caller/root, trình đúng bằng chứng/phép kiểm cần bổ sung và lựa chọn phụ thuộc; không dừng ở OPEN. Không chọn nhánh/ca theo tăng hạng root, không thêm seed/ngưỡng mới. Margin chuẩn hóa để so chênh có dấu giữa ca có thang điểm khác nhau, vẫn giữ điểm thô/mẫu số 0. Đây không là ngưỡng lan hoặc lựa chọn theo accuracy. Chỉ nối mục này vào docs/WHY.md khi Minh duyệt thực hiện đúng nội dung.

## Prompt bàn giao

Prompt kiểm bản sửa được trình trong chat cùng lượt sửa nháp, theo nguyên văn Prompt chung + Kiểm lại phản hồi và sửa + G2 trong docs/review-prompt.md. Codex là người làm cả T-032/T-033; Claude là người phản biện cả hai. Chưa có quyền ghi LOG hoặc bản REVIEW trong lượt này; Claude chỉ đọc và trả lời trong chat. Các lượt sau ghi prompt vào nơi được Minh cho phép, giữ lịch sử.
