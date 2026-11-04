# T-048 — Nhật ký

## Phiên 0 — Duyệt tạo SPEC và bàn giao — 03/11/2026

- Codex người làm, Claude phản biện. Máy Windows của Minh. Phiên này ghi hồ sơ bàn giao.
- Minh duyệt tạo SPEC ngày 03/11/2026. Nguồn: Minh nhắn “DUYỆT TẠO FILE LUÔN” trong phiên soạn đề xuất. Bản SPEC giữ nguyên nội dung đã trình, cập nhật dòng trạng thái.
- Minh yêu cầu phiên Codex mới tự rà độc lập tính đúng và độ đầy đủ trước khi triển khai; được điều chỉnh để ưu tiên tính đúng. Ghi rõ căn cứ và hệ quả của điều chỉnh. Thay đổi quyết định đã duyệt hoặc phạm vi ghi/chạy xử lý theo AGENTS.md.
- Minh yêu cầu kiểm tài nguyên EC2 và cho phép xóa tài nguyên task cũ đã xác định không còn tác dụng nếu thiếu chỗ. Phải nhận diện đúng instance, kiểm phụ thuộc và khả năng khôi phục trước khi xóa. Danh tính/cấu hình/chi phí EC2 và trần lượt dài còn chờ. Chưa kết nối EC2, chuyển dữ liệu hoặc chạy thử.
- Bước tiếp: đọc AGENTS.md, STATE, SPEC và mục này. Đối chiếu nguồn trực tiếp, code và hash; ghi kết quả tự rà trước khi chạy. Phần phụ thuộc phát hiện lỗi hoặc thiếu quyền phải dừng để xử lý; triển khai phần đủ căn cứ trong phạm vi được duyệt.

## Phiên 1 — 03/11/2026 — Codex, Windows của Minh, người làm

- EXECUTE. Minh giao triển khai trong phạm vi T-048, cho điều chỉnh kỹ thuật đúng phạm vi và cung cấp IP/PEM. Claude giữ vai trò phản biện chính thức.
- Tự rà trước lượt chạy: đọc AGENTS, STATE, SPEC, LOG, kế hoạch sau T-047 và đối chiếu B0–B5. HEAD đúng revision ghim, cây phương pháp không có diff. Hai allowlist 30/22, hợp đồng/ma trận/đính chính T-043, lệnh và bản ghi T-047 đã đối chiếu manifest. Cấu hình R0/E1+E2 đồng nhất giữa lệnh thật và C-e. Hash chỉ chứng minh toàn vẹn đầu ra nguồn.
- Đường tính: adapter cấp mẫu N/A và mốc; G3 hoặc G0 dự phòng tính p phân vị, D1 dùng phơi nhiễm và phi cho đếm; cờ qua ngưỡng strict; E4 tính tỷ phần vượt biên và z thay điểm phân vị sau cổng. E2-C gán cạnh có cờ cho đích, nên phải đối chiếu từng gán trước khi giữ cố định trong replay. E6a xếp theo tầng rồi khóa. m của S1 lấy cực đại trên các kênh đủ điều kiện, có thể đến từ kênh khác kênh điểm tối đa. Bản ghi T-047 chưa đủ trung gian trước z/khóa chính xác cho B4.
- Bão hòa và lấn át có thể cùng xảy ra: thay một kênh phân vị bão hòa bằng z cũng có thể làm kênh đó vượt đối thủ có điểm đếm. Tách đối chiếu phân vị với phân vị và phân vị với đếm, đọc thành phần khóa đầu tiên và đối chiếu nhóm chồng lấn. Tách r_A=1 khỏi e=1. Nếu hai phép phát lại cùng đảo hạng thì giữ OPEN phần quy nguyên nhân duy nhất.
- Ngoại lệ dự kiến từ code chuoi.py: với N=[1e308]*11, A=[-1e308]+[1.5e308]*20, hướng lên có z hữu hạn còn hướng xuống tràn. Nếu cổng đặt cờ lên, nhánh thay điểm vẫn xóa cờ và đánh dấu đơn vị không hợp lệ. Phải kiểm điều này trước N1/V0 và giữ bản native. Hai điểm z hữu hạn lớn còn có thể làm tổng khóa tràn khi đổi Fraction sang float. Ghi lỗi nếu gặp, giữ mẫu số theo giao thức. Các phản ví dụ ở đây dựa trên đọc code, chưa chạy fixture.
- Helper T-047 chốt khoi_K; T-048 gọi trực tiếp pha2.ket_cuc_cap với luat_C, 23 ô đã ghim, không truyền vế C-e hoặc kích hoạt UV-6/E5. So cả ba kết cục và kết hợp; dựng fixture khiến hai chế độ cho kết quả khác nhau.
- Cache có sẵn G0/G3 đưa alpha vào khóa; chưa có bằng chứng tiết kiệm khi tái dùng p qua alpha. Dự toán ban đầu tính chạy riêng.
- EC2: SSH strict tại IP Minh cấp dùng HostKeyAlias của máy cũ; khóa máy chủ khớp và PEM đăng nhập được bằng quyền hiện hành. IMDS trả i-06c1d9173fb30932e, m7i-flex.large, ap-southeast-2b. 2 vCPU, RAM 7,6 GiB, khả dụng 7,1 GiB, swap 0, ổ gốc ext4 19 GiB trống trên đĩa 40 GiB, không thấy tiến trình thí nghiệm trong danh sách tiến trình CPU cao; có kiểm cập nhật hệ điều hành. Không sửa ACL hay dọn đĩa. Bảng giá AWS khu vực: 0,1197 USD/giờ Linux On-Demand Shared, giá tài khoản chưa xác minh. Nguồn https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/ap-southeast-2/index.json.
- Đã trình Minh chốt danh tính và ngân sách pilot, một worker mỗi máy, 45 phút chạy/máy, 60 phút hoạt động EC2. Lượt dài chờ dự toán đo được và duyệt riêng.
- Minh xác nhận cho phép pilot cả hai máy nếu giúp tối ưu thời gian, ưu tiên tính đúng, và không đặt chi phí tiền máy làm tiêu chí chọn. Giữ trần vận hành pilot đã trình. Sẽ chạy cùng lát cắt để kiểm chéo trước khi chọn máy.
- Kiểm EC2 chỉ đọc: hệ điều hành Ubuntu 26.04, Python hệ thống 3.14.4, có môi trường cũ Python 3.12. Không có tiến trình Python trong lần kiểm. Nezha 154/154 nguồn khớp tại ~/rca/T-032/repo; dùng trực tiếp ở vị trí đã có. RE2 chưa có ở bốn gốc tra theo allowlist. Không xóa hoặc chuyển Nezha.
- Hồi quy cục bộ: py -3.12 -B thiếu NumPy. Chạy lại môi trường ghim với PYTHONPATH T-016: oracle z qua, assert đầu tiên kỳ vọng sai biểu diễn không áp dụng của UV-6/E5. Sửa kỳ vọng thành KHONG_AP theo hàm native và chạy lại PASS. P GIUP, S_lo KHONG_TAC_DUNG, S_hi HAI; luat_C KHONG_DU_CA, khoi_K GIUP. Chưa chạy fixture đầu-cuối qua chuỗi với z tràn.
- Lát cắt pilot đã khóa trong results/T-048/pilot.json, chọn nhẹ/vừa/nặng theo tổng byte allowlist, phá hòa theo ID mờ. Có 6 ca thật và 3 C-e, 4 cấu hình mỗi cửa sổ. Mốc RE2 chiếu thành ID → t/t−300; không chuyển tệp nhãn chấm.
- Manifest chốt trước chuyển. EC2 xác minh 67 mục code/hợp đồng/nguồn với byte và SHA-256. RE2 chỉ chuyển 9 file dev của pilot, 67.761.268 byte, laptop giữ bản gốc. Nezha dùng 154 bản đã khớp ở vị trí cũ; không chuyển dữ liệu Nezha. Chuyển và xác minh 18,203 giây. EC2 dùng Python 3.12.3 của môi trường có sẵn theo chế độ không ghi bytecode. Laptop dùng 3.12.10; NumPy/SciPy/pandas/PyArrow cùng 1.26.4/1.14.1/2.2.3/18.1.0.
- Pilot bắt đầu trên hai máy, giữ hai thư mục lượt riêng. Quan sát bước đầu cho thấy có bản ghi OK trên cả hai. Chưa tính tỷ lệ tăng tốc hay ngoại suy khi chưa có thời gian toàn đợt và bảng so đầu ra.

### Prompt Claude — soát phần đã thực hiện, Minh chuyển thủ công

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-048, tasks/T-048-thang-diem-tham-so-e4/SPEC.md.
- Công đoạn: soát kết quả đã có.
- Gói/cổng: P6, chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex làm, Claude phản biện.
- Tài liệu gốc: docs/KE-HOACH-SAU-T047.md và các nguồn tại mục Đầu vào của SPEC.
- Phản biện và phản hồi trước: không có.
- Code và kết quả liên quan: results/T-048/, revision phương pháp 6d9744ab0147dd526a0979ddcc7cc035f091d35d, manifest.json và command.json tại từng lượt.
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

### Kiểm trong khi pilot chạy

- Fixture tổng hợp toàn chuỗi: dùng _ca_metric từ results/T-044/tests/test_k12_luot4.py, N=[8e307]*20, A=[-1.5e308]+[1.5e308]*20, G3/D1 và S1. G3 rơi về G0 chính xác. E4 và z đều p_lên=7,802951335119161e−11. E4 có F_raw,lên=1, hop_le=True, S tầng 1, CAUSE_FOUND. z_lên hữu hạn nhưng z_xuống tràn. Native z có F_raw,lên=0, hop_le=False, S tầng 3, INSUFFICIENT_EVIDENCE. Đây là phản ví dụ toàn chuỗi, chưa cho biết tần suất dev. B2 phải đứng trước vế N1/V0.
- Đối chiếu sớm năm bản ghi đã xuất giữa hai máy thấy chênh trường số. Bản ghi C-e R0 mặc định đầu tiên có cùng thứ tự và nhóm hòa trong cả ba thế giới. Ví dụ m tại một khóa là 0,03178304632839908 và 0,031783046328399074. Một p là 2,9396896191596594e−07 và 2,9396896191596583e−07. Đây chỉ là kiểm sớm, chờ đủ bảng chênh cờ/tầng/khóa/hòa/hạng/N1/V0 trước chọn máy. Chưa quy nguyên nhân cho thư viện cụ thể.

### Chốt phần B0 pilot

1. Đã hoàn thành pilot trên hai máy và kiểm ghi gọn. T-048 vẫn đang làm. Dự toán cấu hình EC2 khoảng 8,6 giờ, lấy mức tối đa từng nhóm pilot khoảng 13,7 giờ trước phần chuẩn bị/kiểm/chấm. Đề xuất một worker, trần 16 giờ máy tổng cộng và giá niêm yết 1,9152 USD, chờ Minh duyệt. Máy đã kết thúc pilot; chưa có tiến trình dài.
2. File ghi trong lượt: LOG này, dòng T-048 tại docs/STATE.md, các script chay/kiem/cham, ma-tran, manifest, pilot, so-lan-nhin, báo cáo và ba thư mục lượt trong results/T-048. SPEC giữ khóa. Bản pilot cũ của chay.py và kế hoạch đầu vào còn giữ trên EC2, SHA theo manifest.
3. Đủ 36 cặp OK, 29 cặp có chênh native/trung gian; không khác trường quyết định, không qua ngưỡng alpha. Khóa và p sai khác số thực được ghi trong pilot.json#/comparison. Laptop 9/9 R0 khớp bản ghi lịch sử sau bỏ tên cấu hình, EC2 8/9 khác trường số. Fixture z, helper, kiểm lại pha 2 với nhãn tổng hợp, replay S1 bản ghi đầu và kiểm ghi gọn một ca dev đều đạt trong phạm vi đã ghi. Không thấy z không hữu hạn trên 3.408 đơn vị pilot của mỗi máy. Chưa đo cold/warm có đối chứng hoặc peak RAM toàn đợt trên cả hai máy. Chưa kiểm cache alpha, không tính lợi ích.
4. Còn mở: tái lập R0 đủ 82 cửa sổ, phân loại chênh với T-047, T4, T4b, và phân xử bão hòa/lấn át. Dự toán từ lát cắt theo byte, chưa kiểm hai worker. Nếu Minh duyệt, chuẩn bị manifest những file RE2 còn thiếu, dùng trực tiếp Nezha tại gốc đã kiểm. Chạy R0 mặc định với chế độ ghi gọn và ghim cấu hình trước, kiểm kết quả rồi mới tiếp phần phụ thuộc. Không có cơ sở chọn tham số/thang hoặc dùng nền T-049 từ pilot.
- Bước kế tiếp: đọc results/T-048/pilot.json#/proposed_long và bao-cao.md. Sau duyệt, dựng kế hoạch R0 gồm đủ 30 RE2 thật + 22 Nezha thật + 30 RE2 C-e từ hai allowlist, chỉ chiếu mốc, giữ nhãn chấm riêng. Dùng chay.py <run-id> <kế-hoạch> --compact --limit <trần-phần-R0> --re-root ~/rca-t048/staging --nz-root ~/rca/T-032/repo, xác minh hash code/đầu vào trước chạy. Kiểm hash kết quả trước pha 2, ghép T1/K-R0 từng ca, từng thế giới. Trình lại nếu ảnh hưởng kết luận hoặc chưa giải thích.
- Lệnh chốt: py -3 -B đọc stdin để chốt số R0 pilot và SHA đầu ra vào manifest; git diff --check -- docs/STATE.md và kiểm file theo manifest. Prompt Claude cho phần đã có nằm ở mục “Prompt Claude — soát phần đã thực hiện, Minh chuyển thủ công” trong phiên này.

## Phiên 2 — 03/11/2026 — Codex, Windows của Minh, người làm

- EXECUTE. Minh giao tự quyết mức chạy tối đa phù hợp trên laptop và EC2, tính trước tài nguyên rồi chạy phần độc lập song song; giữ tuần tự các phụ thuộc, ưu tiên phần nặng trên EC2, dừng phần có vấn đề. Quyền chạy chính thức R0, T4/T4b trong phạm vi SPEC được tiếp tục sau các kiểm phụ thuộc. Giữ trần dự phòng tổng 16 giờ đã trình để theo dõi, không coi là dự báo thời gian cần dùng. Không đổi ma trận hay quyết định nghiên cứu.
- Phạm vi tác động trong lượt gồm chay/kiem/cham.py và đầu ra đã liệt kê của T-048, nối LOG, đúng dòng T-048 của STATE. EC2 chỉ ghi cây rca-t048 đã duyệt. Dữ liệu nguồn chỉ đọc. Chia theo ca/cửa sổ, giữ mọi cấu hình của mỗi phép so trên cùng máy. R0 đủ 82 cửa sổ tái lập trên EC2 trước.
- Tài nguyên mới kiểm: EC2 2 vCPU, 7,56 GB RAM khả dụng, đĩa 18,19 GB trống. Laptop i5-1240P 12 core/16 luồng nhưng RAM khả dụng chỉ khoảng 3,50 GB, đĩa D khoảng 6,85 GB trống. Vì vậy số luồng không quyết số worker. Bắt đầu tối đa 2 worker EC2, laptop đo riêng 1 worker nặng hoặc 2 worker nhẹ, luôn đo RAM thực và dừng cấp việc khi thiếu.
- Tối ưu cần kiểm trước dùng: cache p qua alpha giữ nguyên toàn bộ khóa còn lại và không lưu cờ đã áp alpha. Code p_G3/p_theo_G3 và p_cong không đọc alpha. D1 tính lại nguyên vẹn theo thế giới. So với chạy riêng đủ bản ghi native/trung gian trên lát cắt khai trước; chỉ tính lợi ích sau đo cả đợt. Nếu không khớp, giữ đường riêng. Sửa dấu vết ghi để đủ cả ba thế giới ở nhánh S0; bản native phải khớp đường không ghi dấu vết.

### B0 đã khởi chạy độc lập trên EC2

- Nguồn phương pháp/hash hợp đồng khớp kế hoạch trước chạy. Chuyển phần RE2 còn thiếu theo manifest dương, tổng phần chuyển gồm code/kế hoạch là 588673986 byte, đo 87.672 giây. Kiểm hash toàn bộ 89 file nguồn RE2 sau chuyển, không có lệch. Nezha giữ nguyên tại gốc đã kiểm.
- Controller r0-ec2-001, 2 worker, tối đa 2 giờ cho R0, mỗi cửa sổ có thư mục độc lập. Mọi lượt giữ stdout/stderr, command chứa nguyên nguồn script để tái lập, tiến độ/RAM/CPU và hash đầu ra. Hai cửa sổ nặng đầu có native OK. Đỉnh tổng RSS đo ban đầu khoảng 4,0 GB, RAM còn khoảng 4,3 GB. Chưa chấm nhãn, chưa khẳng định tương đương toàn dev.
- Cách kiểm tiếp từ máy khác: ssh key2 tới IP 3.107.156.186, dùng HostKeyAlias 3.26.62.217 và StrictHostKeyChecking=yes; đọc ~/rca-t048/work/results/T-048/runs/r0-ec2-001/kiem.json khi có, tail progress.jsonl. Mọi controller/worker chỉ ghi cây T-048. Nếu controller thành công, kiểm từng hash con và đủ 82 cửa sổ trước so T-047/ghép nhãn.

### Kết quả tối ưu và phân công theo tài nguyên

- Cache đã đối chiếu 6 bản ghi ở 2 ca (RE2 vừa, Nezha vừa) với đủ ba alpha cùng epsilon=0,2. Hash bản ghi native và trung gian của cache bật/tắt giống hệt, thời gian cả đợt 208,937 → 102,281 giây. Kết quả tại runs/cache-check-001/kiem.json. Lợi ích chỉ đo ở lát cắt đó. Đường D1 không cache, tính lại đầy đủ theo thế giới và phi.
- Bản ghi R0-Nezha trên laptop với 2 worker xong 22/22 trong 203,828 giây, còn chờ so đủ từng bản với T-047. Monitor cũ trên Windows chỉ cộng RSS tiến trình bọc, bỏ sót tiến trình Python con. Đã nhận diện bằng cây PID/PPID, sửa monitor cho lượt sau để cộng cả cây. Số RAM trống hệ điều hành vẫn được giám sát ở lượt cũ. Đây là hạn chế phép đo tài nguyên, không là bằng chứng sai bản ghi.
- Ma trận phân việc khai trước chấm: laptop nhận 22 Nezha và 10 RE2 nhẹ nhất theo tổng byte allowlist, EC2 nhận 20 RE2 nặng hơn. Các vế của cùng ca/cửa sổ chạy trên cùng máy. B0 vẫn tái lập đủ 82 trên EC2. Laptop chạy thêm R0 cho đúng phần nhận để dùng làm đối chứng nội bộ. EC2 tối đa 2 worker; laptop thử tối đa 4 worker nhẹ, 1 worker nặng theo RAM thực. Không chọn ca theo nhãn/hạng.
- Sửa phần thu trung gian S0 để có trạng thái đơn vị cả ba thế giới, oracle E4/z/đếm và hash đầu vào chuẩn hóa. Đã kiểm bốn nhánh E4/z × S0/S1 với mẫu tổng hợp qua đường native, bản ghi trùng hoàn toàn; kiểm thêm D1, NEW_OP/STOPPED, hỗ trợ thấp và phơi nhiễm thiếu. Mã phương pháp src giữ nguyên.

- Cập nhật mức laptop theo đo thực: sau 15/20 cửa sổ RE2 được phân, RSS cả cây có đỉnh 1.223 MB, tính cả controller. Khi hết phép kiểm cache, mức RAM khả dụng dự kiến cho phép 2 worker RE2 nhẹ, vẫn giám sát từ đầu. Khai trong ma-tran trước chạy T4. Nezha dự kiến 4 worker nhẹ; E1/E2 ở T4b phải đo lại vì thêm đơn vị.
- 22/22 bản ghi R0-Nezha laptop khớp toàn bộ native với T1 T-047 sau chuẩn hóa tên cấu hình, kiểm từng hash trước đọc. Kết quả runs/kiem-r0-laptop-nz-001/kiem.json. Chưa suy tương đương của phần EC2 còn chạy.

- Cân lại tải trước chấm sau số đo R0: EC2 hai worker chỉ tăng thông lượng vừa phải so một worker của pilot, và sẽ là nút chờ nếu chỉ giao 10 RE2 cho laptop. Các ca RE2 ở nhóm giữa trên EC2 có RSS cuối khoảng 0,75–0,91 GB, thấp hơn hai ca nặng đầu. Laptop vừa xong phần nhẹ, RAM trống trở lại khoảng 4 GB. Chọn laptop 18 RE2 nhẹ hơn, EC2 giữ 12 RE2 nặng nhất; laptop vẫn nhận 22 Nezha. Chạy thêm R0 cho đúng 8 ca mới trên laptop với 2 worker để đo đỉnh và kiểm tương đương. Giữ mọi đối chứng cùng ca trên cùng máy. Chốt trước chấm trong ma-tran.json; không dùng hạng/nhãn để cân tải.

### Hash R0 trước ghép nhãn

- R0 EC2 đủ 82 cửa sổ, từng SHA pha 1 và trung gian đã kiểm, ghi tại results/T-048/runs/kiem-r0-ec2-001/kiem.json#/hashes. Đọc nhãn chỉ sau mốc này. Các bản lịch sử T1 đã kiểm theo manifest T-047.

### B0 đạt và mở T4 — 03/11/2026

- R0 EC2 xong đủ 52 thật + 30 C-e, 2 worker, 2.075,489 giây, đỉnh RSS cả controller/worker 4.032.356.352 byte. Native có 77/82 cửa sổ lệch số thực so laptop T-047. Đã kiểm toàn bộ trường: chỉ p ở các hàm đuôi xác suất G0/D1 và m T4c/khóa chứa m khác. Không lệch p_G3, cờ, hợp lệ, tầng, tập cạnh/kênh có cờ, hòa/thứ tự, N1/V0. Không có p qua alpha giữa hai bản.
- Định vị số học trên cùng đối số thật: trên laptop/EC2, math.log1p lần lượt 0,08793638887070132 / 0,08793638887070131; p_cong G0 9,058519932589506e−07 / 9,058519932589508e−07. D1 cũng tái lập chênh p từ cùng số đếm, phơi nhiễm và phi. Bản dựng lại nguồn của ca này có cùng hash đầu vào chuẩn hóa và mọi mẫu phân vị. Không dùng lượt replay chẩn đoán đó như kết quả phương pháp. Bằng chứng và đối số đầy đủ ở runs/kiem-so-hoc-hai-may-001/kiem.json.
- Bản ghi T1 và K-R0 lịch sử khớp 52/30 sau chuẩn hóa tên, hash đã kiểm theo manifest T-047. Chấm R0 mới cho toàn bộ RR/Hit/M5 theo ca/thế giới trùng bộ chấm từ bản ghi T1. MRR gộp 346127/508032, M5 17; C-e 30/30 CAUSE_FOUND, mean N1 169/10, trùng ba thế giới. Số lấy từ runs/kiem-r0-ec2-001/kiem.json#/summary. N1 theo thế giới của bản cũ suy từ tiền tố tầng trong blocks; V0 suy được khi N1>0. Các trường hợp không suy được phải giữ OPEN, không có trường hợp như vậy trong lần này.
- Kiểm cache mở rộng sang 1 C-e nhẹ, đủ 9 điểm lưới trên cả ba thế giới: bật/tắt cache trùng hash native và trung gian; tool sources cũng trùng. Thời gian 260,296 → 104,203 giây. Kiểm các biên p=alpha và nextafter hai phía đạt. Lát cắt thật trước có cả G3/G0 và 186 hướng có p trong 0,002 của một mức alpha. Áp cache p với ghi hit/miss, tính lại D1/cờ và hạng đầy đủ.
- Laptop đã có R0 đúng cho 18 RE2 và 22 Nezha được giao; 58 cửa sổ tương ứng khớp native T1 sau chuẩn hóa tên. Thử 4 worker Nezha trên 4 ca lớn nhất xong 27,265 giây, đỉnh RSS 1,752 GB. Hai worker RE2 nhóm giữa đỉnh 2,696 GB. Khi chạy hai loại đồng thời chọn 2 RE2 + 2 Nezha trên laptop, giữ khoảng trống RAM; EC2 2 worker.
- T4 chính thức đã khởi chạy. EC2 giữ 12 RE2 nặng nhất (24 cửa sổ), 8 điểm còn lại sau R0, controller t4-ec2-001. Laptop có t4-laptop-re-001 (36 cửa sổ) và t4-laptop-nz-001 (22 cửa sổ), mỗi controller 2 worker. R0 mặc định được dùng đúng trên máy của từng cặp. Trần mỗi controller T4 10.800 giây, tổng trần dự phòng cả gói giữ 16 giờ. Theo thời gian R0 và kiểm cache, dự kiến pha T4 khoảng 1–2 giờ, cập nhật theo tiến độ thực; chưa gọi đó là thời gian hoàn thành task.
- Lệnh EC2 độc lập SSH, PID controller 5600, nguồn/lệnh đầy đủ ở runs/chuan-bi-t4-001 và command.json của controller. Xem tail ~/rca-t048/work/results/T-048/runs/t4-ec2-001/progress.jsonl; kết thúc có kiem.json với success=true. Local dùng Python ghim, PYTHONPATH T-016, hash seed 0, OMP/OPENBLAS 1; lệnh ở runs/chuan-bi-t4-laptop-001/command.json.
- Bước tiếp: kiểm tính đúng/nguồn và mọi lượt đang chạy. Sau T4 đủ 738 bản ghi chính gồm R0, đối chiếu tập ca/ô/thế giới, hash trước chấm, bảng 9 điểm, điều kiện B1 và đường cờ/khóa. Nếu có ứng viên đổi tham số thì trình Minh theo SPEC, chưa dùng nó để chọn thang. Nếu giữ mặc định theo B1, tiếp T4b trên nền đã xác nhận. T-049 và quyền G3/test vẫn quyết riêng.

### B2 — kiểm biên số học mở rộng trong khi T4 chạy

- Đã giữ 5 fixture toàn chuỗi tại results/T-048/runs/kiem-cuc-tri-z-001/{command,kiem}.json. Cả hai vế chạy native G3/D1, S1.
- Khi cờ đều 0, N=[8e307]×20, A=[8e307]×20 cộng hai cực trị, E4 có N1=0 và NO_INTRINSIC_ANOMALY; z vẫn N1=0 nhưng INSUFFICIENT_EVIDENCE vì mất hợp lệ. N1 bằng nhau không đủ xác nhận vế C-e.
- Trung vị và phép chia có thể tràn từ mẫu hữu hạn. IQR cũng có thể tràn thành vô hạn nhưng z hai hướng bằng 0 vẫn khiến trường huu_han=True. Vì vậy phải kiểm riêng med_N/IQR/c, không dùng riêng cờ huu_han làm bằng chứng mọi trung gian hợp lệ.
- Hai kênh z=1e308 đều hữu hạn có thể làm tổng khóa tràn ở xep_hang._thuc, native trả ERROR thay cho verdict. Giữ nguyên bản ERROR. Không thay Inf/NaN hoặc tự chọn điểm thay thế.
- Các phản ví dụ này giới hạn tuyên bố ổn định trên toàn miền hữu hạn. Chưa xác nhận chúng xảy ra trên dev. Nếu dev có ngoại lệ, phần kết luận thuần đổi điểm và hành động theo B5 phụ thuộc dừng theo SPEC. Sửa src/m1 nằm ngoài quyền ghi T-048, cần đề xuất riêng cho Minh, không tự áp sửa.
- Cache m thuần túy (tính lại cờ và chọn max m như cũ) đã kiểm native/trung gian exact trên 12 bản ghi hai cửa sổ, đủ R0/E1+E2 × E4+S1/z+S1/z+S0. Thời gian cả đợt 110,031 → 85,750 giây. Kết quả tại runs/cache-m-check-001/kiem.json. Đang giữ T4 chạy với phiên bản đã khởi động; phép tối ưu chuẩn bị cho bước sau sau khi nguồn công cụ được ghim lại.

### Tái chia tải laptop tại ranh giới cửa sổ

- Sau Nezha và các phép thử, RAM được giải phóng. Controller điều phối cũ được tạm ngừng cấp việc; các child tiếp tục hoàn tất. Chỉ sau khi hết child sống và kiểm toàn bộ hash/8 bản ghi mỗi cửa sổ mới đóng controller cũ. Giữ 13 cửa sổ hoàn tất, chia đúng 23 cửa sổ chưa chạy sang controller t4-laptop-re-002, 3 worker. Không có cửa sổ đang tính bị cắt.
- Lượt điều phối t4-laptop-re-001 được giữ với success=false, error=resource_repartition, partial_verified=true, danh sách child đã đóng và phần còn lại. Đây là lịch sử tái chia tài nguyên. Bộ ghép chỉ nhận child có hash hợp lệ; cuối cùng vẫn phải kiểm đủ tích cấu hình × 52 thật/30 giả và không trùng mã ca/cửa sổ. Bằng chứng và lệnh tại runs/tai-chia-laptop-001. Tất cả mẫu/cấu hình/thế giới và cách chấm giữ theo nguồn đã duyệt.
- Công cụ chay.py tiếp tục đúng phiên bản đã dùng ở T4, cache m chưa áp. Kiểm m trên lưới C-e đủ 9 điểm trùng hash native và trung gian, nhưng thời gian 129,312 giây so 104,203 của lượt cũ; chưa có căn cứ tính lợi ích m cho lưới này. Kết quả ở runs/cache-m-grid-check-001/kiem.json. Phép 12 bản ghi T4b riêng trước đó có thời gian 110,031/85,750; lợi ích phụ thuộc workload và điều kiện chạy.
- Thông số RSS các controller là cực đại quan sát theo chu kỳ 2 giây, không phải chứng nhận cực đại vật lý liên tục. Monitor mới trên Windows cộng cả cây tiến trình. Số 3 worker laptop được quyết theo đỉnh đã đo và RAM trống hiện hành, với kiểm tài nguyên suốt lượt.

### Checkpoint triển khai — T4 còn chạy

- Vai trò vẫn Codex làm, Claude phản biện chính thức. Có thể tiếp từ file, không cần lịch sử chat. Nguồn phương pháp vẫn HEAD ghim, src không đổi.
- Việc đang chạy: EC2 controller t4-ec2-001 (2 worker, 24 cửa sổ), laptop t4-laptop-re-002 (3 worker, 23 cửa sổ còn lại). Phần laptop t4-laptop-re-001 có 13 cửa sổ đã đóng, giữ ở trạng thái partial_verified do tái chia. t4-laptop-nz-001 xong 22 cửa sổ (8 cấu hình mới), R0-Nezha xong 22; bảng phần Nezha ở runs/cham-t4-nz-001/kiem.json.
- Lệnh xem local: Get-Content results/T-048/runs/t4-laptop-re-002/progress.jsonl -Tail 3. EC2: ssh -i D:/RCA-ext/keys/key2.pem -o HostKeyAlias=3.26.62.217 -o StrictHostKeyChecking=yes ubuntu@3.107.156.186 'tail -3 ~/rca-t048/work/results/T-048/runs/t4-ec2-001/progress.jsonl'. Kết thúc xem kiem.json và stdout/stderr tại controller/prepare. Controller cũ t4-laptop-re-001 đã đóng sau child, không resume nó.
- Sau T4 đóng, dùng collect_controllers trong scripts/cham.py, allocation từ ma-tran.json. Nguồn tham chiếu gồm r0-ec2-001 (chỉ chọn 12 RE2 được phân cho EC2), r0-laptop-nz-001, r0-laptop-re-light-001, r0-laptop-re-mid-001. Nguồn T4 gồm t4-ec2-001, t4-laptop-nz-001, partial t4-laptop-re-001 và t4-laptop-re-002. Hàm ghép chấp nhận riêng partial đã kiểm; vẫn kiểm trùng và toàn bộ tập cấu hình/ca/cửa sổ ở bước chấm.
- D laptop còn khoảng 4–5 GB, tránh chép toàn bộ trung gian EC2. Giữ bản đầy đủ tại nguồn remote, dùng export_closed_controller trong scripts/kiem.py sau khi controller EC2 xong: xuất nguyên byte native + phép chiếu N1/V0 theo thế giới sang run export mới có hash/provenance. Bản đầy đủ vẫn ở remote để làm B4. Không sửa script remote khi nó đang được worker khởi nạp. Nếu dùng export, bộ ghép lấy root export controller, trường original_child/source_child_by_window dẫn tới nguồn đầy đủ.
- Sau ghép phải đủ 9 cấu hình × (52 thật + 30 C-e), đủ 23 ô theo T0, cùng máy trong từng ca/vế. Hash pha 1 trước chấm. Dùng nap_nhan(False) từ pha2_khoi_k.py (T-045) hoặc đọc cùng nhãn đã ghim. T0 đã kiểm hash và khớp 52 ca/23 ô, gồm 10 RE2 + 13 Nezha. Không chọn mặc định theo bảng Nezha riêng.
- Gọi tong_hop và t4_candidates, đọc chuỗi cờ/khóa và độ mong manh theo B1 trước trình đổi. Mọi đề xuất tham số/thang theo SPEC vẫn do Minh quyết. Chưa có đề xuất đổi từ T4 vì bảng RE2/C-e chưa xong.
- Trước T4b, ghim lại tool source nếu thay kỹ thuật. Cache m mới là thử tối ưu theo workload, native/trung gian đã trùng 12 bản ghi đủ 6 biến thể trên 2 cửa sổ, và đủ 9 lưới C-e. Kết quả thời gian hai workload khác nhau, không dùng nó để khấu trừ T4. Chưa có m cache trong CLI chay.py của các lượt chính.
- Tự rà B4 đã sửa trước khi dùng trên kết quả chính: tính cả strict→tie; chỉ thành phần khóa theo khóa thực được ghi; lưu kênh tạo max s và tạo m; kiểm cả số đếm/phơi nhiễm/phi và điểm kênh đếm giữ nguyên; phân biệt đối thủ còn dựa vào max đếm dưới z với đối thủ đã do phân vị chi phối. Phép trả về nhóm PV của bên thắng gồm cả kênh dự phòng, ngoài phép riêng các kênh đạt max. Các kiểm prototype và fixture giữ trong runs/kiem-mechanism*, kiem-tie-va-scale*. Không cộng nhóm chồng lấn.
- Các fixture cực trị tại runs/kiem-cuc-tri-z-001 là giới hạn số học đã xác nhận của code. T4 độc lập đang tiếp tục. T4b phải kiểm med/IQR/c lẫn z, số khóa tổng và cờ/hợp lệ trên toàn dev trước N1/V0; native ngoại lệ giữ riêng, phần diễn giải phụ thuộc giữ OPEN. Không tự sửa src ngoài quyền.
- Prompt Claude dùng cuối LOG Phiên 1 theo mẫu chung/G3, chỉ trả lời trong chat khi Minh chuyển. Kết thúc task/lượt cần soạn prompt mới trung tính theo review-prompt.md. Chưa phản biện chính thức, chưa nghiệm thu, chưa commit/push.

- Hash trước pha 2 T4: results/T-048/runs/cham-t4-full-001/command.json#/phase1. Đã kiểm từng native/trung gian trước bước đọc nhãn.

### Checkpoint tiếp tục sau nén ngữ cảnh — T4 đủ lưới

- Codex tiếp tục vai trò người làm trên laptop; Claude phản biện chính thức. Đọc lại AGENTS, STATE, SPEC và mục LOG cuối, dựng trạng thái từ file. T4 đã đóng đủ 738 bản ghi = 9 × (52 thật + 30 giả), 23 ô. Hash được kiểm trước nhãn; bảng và nguồn ở t4.json, kiểm ở runs/cham-t4-full-001/kiem.json.
- Cả tám điểm khác mặc định đều không tăng MRR gộp; không có ứng viên qua điều kiện số B1 ở bất kỳ thế giới nào. Giữ ε=0,05 và α=0,01 cho T4b theo nhánh tiếp theo đã duyệt trong SPEC B1, không đổi quyết định tham số. Phân tích cờ/khóa T4 tiếp tục độc lập trong khi T4b chạy.
- T4b chạy 5 cấu hình mới × 82 cửa sổ, dùng lại R0 mặc định trên đúng máy của từng ca. EC2 2 worker giữ 12 RE2 nặng; laptop 3 worker nhận 18 RE2 và 22 Nezha. Trần controller 10.800 giây, nằm trong trần dự phòng toàn gói 16 giờ đã trình; user đã giao chủ động mức song song theo tài nguyên. Giá máy 0,1197 USD/giờ; dự kiến phần T4b khoảng 45–90 phút EC2, chi phí máy khoảng 0,09–0,18 USD, kiểm lại theo tiến độ. Cache α giữ phiên bản đã chứng minh. Cache m không áp vào lượt chính do lợi ích phụ thuộc workload; không tính khấu trừ từ thử khác tải.
- Không sửa SPEC, src, dữ liệu, DECISIONS/WHY; không mở G3/test hoặc K/T-049.

### T4b khởi chạy và kiểm nối tiếp theo cửa sổ

- EC2 controller t4b-ec2-001, PID 6961; laptop t4b-laptop-001, 58 cửa sổ. Mỗi cửa sổ tính 5 cấu hình còn thiếu, tham chiếu R0 lấy từ chính máy của nó. Lệnh và tài nguyên trước chạy ở runs/chuan-bi-t4b-001/command.json. Không áp cache m. Giữ mã chay.py và kiem.py trong suốt lượt.
- Phân tích T4 theo toàn bộ kênh/cửa sổ chạy độc lập tại duong-t4-laptop-001 và duong-t4-ec2-001. Kiểm lại hash native và trung gian trước root chấm. Kiểm input chuẩn hóa, mẫu N/A và mốc/biên G3 giữ nguyên. Lưu cờ đổi, p/biên/điểm, tầng, khóa root/đối thủ và đường dẫn bản đầy đủ. Bootstrap theo ô ở phan-tich-t4-001, seed và số mẫu chốt trong command trước tính.
- Lượt chuan-bi-duong-t4-001 lỗi SyntaxError ở đóng gói lệnh remote, chưa chạy phân tích. Giữ command/stdout/stderr/kiem; sửa tối thiểu cách truyền chuỗi và chạy ở chuan-bi-duong-t4-002. Không ảnh hưởng phương pháp hoặc tập ca.
- B2 kiểm các cửa sổ T4b đã đóng theo thứ tự hash → hữu hạn med/IQR/c/z và khóa tổng → cờ/hợp lệ/ứng viên/tầng/gán E2/đếm → N1/V0. Không có nhãn trong công cụ B2. Lệnh ở chuan-bi-b2-t4b-001, kết quả tăng dần ở b2-t4b-{laptop,ec2}-001; chỉ tổng kết khi đủ controller. Chưa gọi phép so thuần đổi điểm từ lát cắt.

### T4 hoàn tất phân tích; kiểm lại lát cắt cache chính

- Đường tính T4 đủ 656 lượt ngoài mặc định = 464 laptop + 192 EC2, không trùng. Cả input chuẩn hóa, mẫu N/A, mốc và biên thời gian G3 giữ nguyên giữa các điểm; thay tham số làm đổi p/biên trị số/cờ/tầng/khóa như lưu theo ca. Nhận bản phân tích EC2 18.508.661 byte, khớp manifest hai đầu ở nhan-duong-t4-001. T4 và ví dụ có điều kiện được ghi trong bao-cao.md; số đều dẫn tới t4.json hoặc tong-hop-duong-t4-001 và bản trung gian.
- Kiểm lại 15 bản ghi của lát cắt cache trước đó trên đầu ra T4 chính cùng laptop. Native exact 15/15. Kiểm full trung gian ban đầu ở kiem-cache-main-001 không exact vì phiên bản mới thêm source_bytes, A_extrema và oracle; mọi lệch đã xác định là trường thêm, không sửa kết quả cũ. kiem-cache-main-002 so strict mọi giá trị chung, cấm xóa trường và chỉ chấp nhận đúng ba loại trường chẩn đoán thêm: đạt 15/15. Bật/tắt cache ở cùng phiên bản prototype vẫn trùng hash native/trung gian theo cache-check-001 và cache-ce-check-001. Không dùng dung sai để bỏ qua trường quyết định.
- T4b còn chạy. Chuẩn bị B4 ghép nhãn sau đóng toàn bộ hash và B2 đầy đủ; kiểm replay hai chiều, E4+S0, sat/non-sat, trả điểm nhóm PV thắng, cực trị A. Thu tất cả cặp control không đổi quan hệ có điều kiện tương ứng, gồm ca đúng cả hai vế. Lệnh/source được lưu ở chuan-bi-b4-t4b-001 và chuan-bi-controls-t4b-001. Đây là phân tích của người làm, không là phản biện chính thức.
- Kiểm native bổ sung ở chuan-bi-native-t4b-001 chờ B2 rồi đối chiếu trace với bản ghi thật ở đủ thế giới: blocks/thứ tự, N1, valid_units, V0 và verdict P. EC2 chỉ export sau kiểm này; bản đầy đủ giữ nguyên tại remote.

- Hash trước pha 2 T4b: results/T-048/runs/cham-t4b-full-001/command.json#/phase1. Đã kiểm từng native/trung gian trước bước đọc nhãn.

### Tiếp tục sau gián đoạn usage — kiểm từ trạng thái thật

- Minh yêu cầu báo phần bị ảnh hưởng và tiếp tục. T4/R0 đã đóng trước gián đoạn, không chạy lại. Trong gián đoạn, T4b chính vẫn chạy: laptop đóng thành công 58/58 cửa sổ, 1.731,578 giây, RSS cây tiến trình lớn nhất quan sát 3.895.742.464 byte; EC2 đóng thành công 24/24, 2.235,867 giây. Không có bằng chứng lượt M1 chính bị dừng hoặc mất đầu ra vì usage. Phần giao tiếp, theo dõi thủ công và chốt pha 2 bị chậm.
- B2 đủ 58+24 cửa sổ, 348+144 bản ghi ghép R0, không ngoại lệ hữu hạn hoặc đổi cờ/hợp lệ/tầng. Native/trace khớp blocks, thứ tự, N1, valid_units, V0 ở 1.044+432 trường hợp thế giới. Biên số học fixture vẫn là giới hạn ngoài các ca dev đã chạy, không được suy phổ quát.
- B4 dừng riêng vì KeyError oracle: một số trace R0 được ghi trước khi thêm trường oracle. Laptop giữ 37 hàng cơ chế, 36 hàng context hoàn chỉnh; EC2 giữ 1 hàng cơ chế, 0 context. Đây là lỗi tương thích schema của phân tích, không quy cho usage hoặc dữ liệu/phương pháp. Ghi kiem.json ở các lượt b4-t4b-*-001, giữ nguyên file đã sinh.
- Sửa tối thiểu trong source lệnh pha 2: lấy oracle từ trace z mới, chỉ sau khi kiểm exact toàn bộ hash mẫu PV và kết quả E4 trước thay điểm bằng bản R0 cũ. Không tính lại/đổi native, không sửa SPEC/src/tham số/ma trận. B4 mới -002 tái dùng 36 cặp context+cơ chế laptop đã khớp nguồn, tiếp phần còn thiếu; metadata cũ và hash được kiểm trước tái dùng. Kết quả laptop đủ 80 cặp ca–nền, 240 thế giới, replay exact.
- Lượt chuẩn bị b4-002 chặn an toàn vì B4 remote vừa bắt đầu trước lúc thay; không signal tiến trình nào, không đổi phương pháp. Sau xác nhận B4 cũ đã thoát vì cùng KeyError mới khởi chạy b4-003, giữ lịch sử.
- Tự tìm thêm lỗi helper controls: chỉ kiểm có kiem.json, chưa buộc source B4 closed=true. Lượt cũ chấp nhận phần B4 chưa đủ; giữ nhưng loại khỏi kết luận theo kiem-controls-history-001. Bản controls-002 buộc B4 đóng, kiểm hash và đúng số ca, rồi dùng oracle z với chứng minh mẫu/E4 bằng nhau. Laptop đủ 51 cặp control, gồm 21 cặp đúng top-1 ở cả hai vế (đếm qua ba thế giới). Không coi số cặp này là số ca độc lập.
- Đã nhận 59.007.307 byte metadata/native export/B2 EC2, kiểm manifest hai đầu ở nhan-t4b-ec2-001. Bản trung gian gốc T4 và T4b vẫn trên EC2. Không xóa tài nguyên, thu hồi 0 byte.
- Bước tiếp: chấm 6 × 82 sau hash/B2, lấy B4/control EC2 đã đóng, kiểm phần oracle cũ/mới cho cả ca thật và C-e; ghép luật C đủ 23 ô và ba thế giới, phân tích nhóm/cặp và cập nhật báo cáo/manifest. G3/test, đổi D24 và dùng nền T-049 chưa được suy từ quyền chạy.

### Kết thúc phần triển khai — chờ phản biện chính thức

1. **Đã làm:** R0 tái lập đầy đủ và đối chiếu hai máy/lịch sử; T4 đủ 9 điểm, giữ mặc định theo B1 trước T4b; T4b đủ hai nền và ba biến thể. B2/native/shared-PV đủ toàn bộ; B4 đủ 104 cặp ca–nền/312 thế giới, controls đầy đủ và 12 ví dụ input→cổng→cờ→điểm→khóa→hạng. Luật C gọi đúng luat_C/23 ô/ba thế giới, kết cục GIÚP trên hai nền. Không tự đổi D24, mở K/T-049/G3/test.
2. **File đã đổi trong phạm vi:** ba script chay.py, kiem.py, cham.py; manifest, ma-tran, pilot, t4, t4b, luat-c, co-che, so-lan-nhin, bao-cao và các file lệnh/tiến độ/kết quả/kiểm/stdout/stderr trong runs dưới results/T-048; nối LOG này; chỉ dòng T-048 trong STATE. SPEC và src không đổi. Các thay đổi sẵn có của T-047/DECISIONS/WHY được giữ.
3. **Kiểm:** R0 và E1+E2 E4+S1 mỗi nền đủ 82 khớp trường quyết định T-047; mọi lệch còn lại chỉ p/m backend, không qua ngưỡng. Native T4b khớp trace ở 1.476 bản ghi–thế giới. 70.752 đơn vị nền–cửa sổ gồm 65.556 đủ hỗ trợ z, oracle hữu hạn đầy đủ; 15.982 đơn vị R0 thiếu trường oracle được đối chiếu exact mẫu/E4 với bản mới. Chưa có ngoại lệ dev; các phản ví dụ cực trị giữ nguyên. Hồi quy z/helper, các biên strict, khác biệt luat_C/khoi_K, mẫu số 0, replay, cache và kiểm tập ô đều có nguồn kết quả. Kiểm cuối/hash/diff nằm ở runs/kiem-cuoi-001/kiem.json và manifest.
4. **Phạm vi kết luận và còn mở:** đây là mô tả và chọn thiết kế trên dev đã nhìn nhiều lần, có bằng chứng đường tính theo cặp, không xác nhận cơ chế duy nhất hoặc hiệu quả độc lập. Nhóm bão hòa và lấn át chồng lấn; phần lớn chuyển quan hệ được tái lập bằng nhóm chưa bão hòa. Cổng×điểm thiếu cặp z/E4 cùng S1 ở G0/D0; khái quát cần dữ liệu độc lập; miền số học cực trị của z cần quyết xử lý riêng. C-e không phân xử do cấu tạo. Minh cần quyết D24 sau phản biện; nếu đổi phải có SPEC K mới, kiểm T1 phần điểm/khóa phụ thuộc, rồi mới quyết nền T-049. Quyền test/G3 riêng. Claude chưa phản biện và Minh chưa nghiệm thu.

- **Bước tiếp theo chính xác:** Minh chuyển prompt dưới cho Claude. Claude đọc AGENTS, STATE, SPEC, nguồn trực tiếp và manifest; tự kiểm nguồn/đầu ra gốc trước nhận xét của người làm. Quyền ghi REVIEW cần Minh cấp. Người làm chờ bản phản biện được Minh chuyển, giữ vai trò Codex. Nếu Minh muốn đổi thang, bước chuẩn bị tiếp là trình SPEC K chạy lại và phạm vi cập nhật quyết định, chưa chạy tự động.
- **Đề xuất commit, chờ Minh:** `T-048: chạy độ nhạy epsilon/alpha và đối chiếu E4-z trên dev`. Chưa commit/push. Phạm vi staging sẽ chỉ gồm file được duyệt, không gộp thay đổi sẵn có khác; cách giữ kết quả nặng theo manifest và nguồn local/EC2 hiện có.
- **Đề xuất ghi docs/DECISIONS.md, chờ Minh duyệt riêng:** mục ngày 03/11/2026 ghi nguyên văn lời Minh về quyền chạy: “chạy tối đa trên laptop và ec2 luôn nếu cần thiết, tính toán mức độ trước sau đó chạy tối đa có thể, trong quá trình làm thấy không ổn thì mới dừng, bạn hãy quyết phương án tối ưu nhất cho tôi. phần nào cần tuần tự thì vẫn chay tuần tự, phần nào song song được thì hãy làm song song, đảm bảo tính đúng đắn nhất không sai sót là được, không cần rút ngắn giai đoạn”. Phần này chỉ lưu quyền điều phối đã dùng, không là quyết định đổi D24 hay mở G3. Không ghi DECISIONS khi chưa duyệt file đó.

### Prompt Claude — soát kết quả, Minh chuyển thủ công

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-048, tasks/T-048-thang-diem-tham-so-e4/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P6, chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex là người làm; Claude là người phản biện chính thức.
- Tài liệu gốc: tasks/T-048-thang-diem-tham-so-e4/SPEC.md, LOG.md của task; docs/KE-HOACH-SAU-T047.md; các nguồn trực tiếp được SPEC dẫn; docs/STATE.md và git diff, toàn bộ file mới của T-048.
- Phản biện và phản hồi trước: không có bản phản biện kết quả chính thức của T-048.
- Code và kết quả liên quan: results/T-048/manifest.json (revision, nguồn, máy, lịch sử công cụ và lượt); results/T-048/{pilot,t4,t4b,luat-c,co-che}.json, ma-tran.json, bao-cao.md, scripts/ và runs/. Python đọc/kiểm trên laptop: D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B; PYTHONPATH=D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages. Lệnh kiểm rẻ không ghi file: Python ghim -B results/T-048/scripts/kiem.py. Vị trí bản đầy đủ trên EC2 được dẫn trong manifest.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; quyền ghi bản phản biện của lượt này chờ Minh cấp riêng.

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

- Kiểm cuối -001 dừng ở bộ quét command.json vì một số command cũ là list argv thay vì object có tool_sources. Đây là lỗi bộ kiểm, xảy ra trước khi ghi STATE/manifest; native và các kết quả không đổi. Giữ command/stderr/kiem. Sửa tối thiểu: chỉ kiểm snapshot tool_sources ở object; list vẫn được giữ và kiểm hash nguyên file. Kiểm cuối chuyển sang -002; con trỏ hiện hành nằm trong manifest khi kiểm xong.

- Đính chính chẩn đoán kiểm cuối -001 sau đọc trực tiếp toàn bộ schema: file list là runs/kiem-cpu-laptop-001/kiem.json (snapshot CPU), không phải command.json. Lỗi thực ở dựng run_inventory dùng .get cho mọi kiem.json. Các kiểm nguồn/native/snapshot đã qua trước đó; STATE đã được ghi chờ phản biện trước khi lỗi inventory, manifest chưa ghi. Đã đưa riêng dòng T-048 về đang kiểm kết thúc. Sửa đúng chỗ: metadata list được phân loại legacy_audit_list và giữ hash nguyên file; chỉ object mới đọc trường trạng thái. Bản kiểm -002 cập nhật STATE sau khi manifest đã kiểm xong. Không đổi kết quả M1 hoặc kết cục. Giữ thông tin chẩn đoán ban đầu trong metadata và LOG để không che nhầm lẫn này.

- Kiểm cuối hiện hành -002: PASS 272 cặp hash native/trung gian local và 130 leaf phương pháp remote; 483 snapshot công cụ tái dựng đúng hash theo LF/CRLF. Các kiểm nguồn/AST/kích thước/luật C/phạm vi/prompt đều đạt. Metadata CPU dạng list được giữ hash, phân loại riêng; không dùng làm trạng thái lượt phương pháp. Manifest đã đọc lại và kiểm mọi hash hiện hành trước khi cập nhật STATE chờ phản biện.
- Lệnh cuối cùng đã chạy: Python ghim -B qua stdin thực hiện kiểm cuối -002, ghi/đọc lại manifest và kiểm diff STATE; kết quả ở runs/kiem-cuoi-002/kiem.json. Bước kế tiếp: Minh chuyển prompt Claude ở trên. Không có M1 đang chạy trên EC2; bản đầy đủ vẫn giữ tại remote.

### Người làm đáp phản biện — Codex, laptop, 2026-11-03

- Tự rà trước khi mở nhận xét Claude: hash đầu ra/công cụ/nguồn điều phối khớp manifest; kiem.py đạt hồi quy z và phân biệt luat_C/khoi_K. Điểm cần soi lại: điều kiện cơ chế chỉ cho bằng chứng theo cặp, độ bền không thay dữ liệu độc lập, và phân biệt bằng chứng hiện có với khả năng người khác tái lập.

- Minh cho sửa ngay những phần Codex xác nhận đúng trong phản biện Claude. Đã dùng đúng phạm vi báo cáo, manifest và LOG. Claude vẫn là người phản biện chính thức. Phản biện lượt 1 do Minh chuyển từ chat, không có file REVIEW để điền.

| Điểm | Phản hồi của người làm | Sửa và kiểm | Minh quyết |
|---|---|---|---|
| F1 | Đúng về thiếu bảng, có ảnh hưởng hồ sơ trình D24. Tính lại từ RR bằng helper đủ 23 ô: E4 GIÚP và z TRÁI_CHIỀU_DATASET trong cả ba thế giới ở phép chẩn đoán không đưa vế mốc giả vào. Đúng về ba chuyển cặp bất lợi qua cạnh ở hai ca được nêu. Chỉ chứng minh đường đổi điểm trên nền E1+E2 cố định. Quy chênh hai nền cho riêng đồ thị hoặc dùng thay bộ chọn K là vượt bằng chứng. | Bổ sung bảng, phạm vi diễn giải và đường tính từng cạnh ở §5–6. | |
| F2 | Đúng về thiếu phân nhóm; không đồng ý mẫu số 27/34 cặp RE2 có lợi. R0/RE2 có 34 cặp đổi quan hệ, gồm 33 có lợi và 1 bất lợi. 27 cặp có lợi có max latency-90. Không đồng ý diễn giải “chỉ nhờ” từ kênh đứng đầu, vì cặp chưa cô lập nhóm metric và chuẩn hóa IQR. | Bổ sung bảng hai nền/hai dataset/hai hướng, kiểm fallback của max bên thắng ở đủ 81 cặp P, thêm OPEN về tử số/IQR/latency-90 và phép phân xử. | |
| F3 | Đúng về thiếu căn cứ giữ S1 dưới z. Nhận định z không bị chặn trên chưa đủ bác bỏ ích lợi của khóa phụ, vì kênh đếm vẫn hòa. Chênh 1/208 xuất phát từ cùng một ca và không đủ chọn S0. | Trình ba phương án với ba mức bằng chứng ở §7. | |
| N1 — không chặn | Ghi “R0 chỉ còn U từ trace” quá rộng. chuoi.py vẫn dựng canh_qs, chạy chẩn đoán C-d1/C-d3, lưu cạnh và G_N. Xếp hạng chính E6a với E1/E2/E5 tắt cần phân biệt với toàn bộ đầu ra. | Làm rõ phạm vi đối chứng QT7 ở §7. | |
| N2 — không chặn | Bổ sung ví dụ T4 RE2 từ bản gốc, theo p, vượt biên, cờ, tầng, khóa và RR. | §3, dev-f81f88234e, trace laptop dòng 282. | |

- Kiểm lại: SHA đầu ra/công cụ/nguồn khớp manifest sau cập nhật, các liên kết tương đối của báo cáo tồn tại, git diff --check đạt. kiem.py đạt hồi quy z và luật C. Hai vế E4/z vẫn có bằng chứng về xếp hạng trên dev. Tác dụng riêng của đồ thị, cơ chế chi tiết của nhóm chưa bão hòa, D24 và nền T-049 còn mở.
- File sửa: results/T-048/bao-cao.md, manifest.json và LOG này. Nguồn kết quả và SPEC giữ nguyên theo hash. STATE hiện hành chờ phản biện vẫn đúng.
- Đề xuất tiếp tục một lượt để Claude kiểm lại các bất đồng trong bảng trên. Bước sau: Minh chuyển prompt. Lệnh kiểm cuối: py -3 -B đọc SHA theo manifest, kiểm liên kết và git diff --check.

### Prompt Claude — kiểm lại phản hồi và sửa

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-048, tasks/T-048-thang-diem-tham-so-e4/SPEC.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P6, chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex là người làm, Claude là người phản biện chính thức.
- Tài liệu gốc: AGENTS.md, docs/STATE.md, SPEC và LOG T-048, docs/KE-HOACH-SAU-T047.md và các nguồn trực tiếp trong SPEC.
- Phản biện và phản hồi trước: Phản biện lượt 1 của Claude trong chat do Minh chuyển, và mục Người làm đáp phản biện ở LOG T-048.
- Code và kết quả liên quan: results/T-048/{bao-cao.md,manifest.json,t4.json,t4b.json,luat-c.json,co-che.json,scripts/,runs/}. Revision, hash và môi trường theo manifest. Lệnh kiểm rẻ trong LOG.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat, trừ khi Minh cấp quyền ghi bản phản biện riêng cho lượt này.

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

### Codex đáp lượt kiểm lại — laptop

- Tự rà trước khi đọc phản biện: kiem.py đạt; bảng kênh thắng cần phân biệt tổng cặp với tập có bên thắng; đoạn cuối báo cáo vẫn nói chưa phản biện dù đã qua một lượt, cần chỉnh trạng thái.

- Ngày 2026-11-03. Minh cho sửa trực tiếp những điểm xác nhận đúng trong lượt 2; Claude vẫn phản biện chính thức.
- Đồng ý điểm không chặn về nguồn số. Lưu kết quả và lệnh tái lập trong runs/kiem-lai-phan-bien-002/kiem.json và command.json cùng lượt. Helper đủ 23 ô cho GIÚP dưới E4 và TRÁI_CHIỀU_DATASET dưới z ở cả ba thế giới, trong phép chẩn đoán hai nền cố định, moc_gia=None.
- So toàn bộ 81 cặp ở P qua hai trace B2 local. 81 cặp có bên thắng; 0 có max PV bên thắng dùng fallback c=1, 6 có max PV bên đứng sau dùng fallback. Phân biệt rõ phạm vi với câu “81 cặp không dùng c=1”. Hai bên đồng ý các kết luận F1–F3 và N1–N2 ở phạm vi đã ghi.
- File sửa: báo cáo, manifest, LOG; thêm command.json và kiem.json trong một lượt kiểm pha 2. Kiểm hash đầu vào, hồi quy kiem.py, nguồn đầu ra và git diff --check đạt. Nguồn M1 và kết quả chính giữ nguyên. Không chạy thêm phương pháp.
- Đề xuất dừng phản biện vì không còn bất đồng có ảnh hưởng. D24, nghiệm thu, nền T-049 và G3/test chờ Minh. Bước sau: Minh quyết dừng hay chuyển prompt tùy chọn bên dưới. Lệnh tái lập: dùng Python ghim -B -c với trường replay_python_c trong command.json của lượt kiểm và PYTHONPATH như các lượt trước. Lệnh cuối: py -3 -B qua stdin kiểm hash và git diff --check rồi nối LOG.

### Prompt Claude — kiểm lại nếu Minh chọn chuyển

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-048, tasks/T-048-thang-diem-tham-so-e4/SPEC.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P6, chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex là người làm, Claude là người phản biện chính thức.
- Tài liệu gốc: AGENTS.md, docs/STATE.md, SPEC, LOG và các nguồn trực tiếp trong SPEC.
- Phản biện và phản hồi trước: Hai lượt Claude trong chat do Minh chuyển, các mục đáp trong LOG T-048.
- Code và kết quả liên quan: results/T-048/manifest.json, bao-cao.md, scripts/, các kết quả và lượt dẫn trong báo cáo. Môi trường theo manifest và lệnh kiểm theo LOG.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat, trừ khi Minh cấp quyền ghi riêng.

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


## Nghiệm thu theo lệnh Minh — 2026-11-03T20:53:58+07:00

- Codex, laptop Windows, người làm T-048; Claude giữ vai trò phản biện. Intent EXECUTE. Minh: “hoàn tất nghiệm thu/ghi nhận quyết định và soạn–duyệt SPEC T-049 luôn”. Quyết định hiện hành lưu Q-236–238, lý do WHY-71–72.
- Đã nghiệm thu/đóng phần T4/T4b, so thang và phân tích dev; giữ epsilon/alpha mặc định. D24 hiện hành là z+S1, nền T-049 là E1-U+E2-C+E5 sau K chạy lại ở T-053. Không còn để hai lựa chọn này ở trạng thái chờ Minh. Bằng chứng chạy cũ và manifest giữ nguyên tại mốc lịch sử; không sửa báo cáo để giả như quyết định đã có từ đầu.
- Kiểm trước ghi: 8 outputs, 2160 closed_outputs, 4 governing_sources, 3 current_tools, 47 source_sha256 và 4 upstream_manifests của T-048 đều khớp. T-053 kiểm độc lập PASS toàn 2654 đầu ra/12 nguồn trước cập nhật sổ. Không chạy lại M1, không đọc locked hoặc dùng EC2 trong lượt này.
- Giới hạn nghiệm thu: mới là bằng chứng dev và phân tích trong dữ liệu đã ghi, không xác nhận cơ chế vật lý/hiệu chuẩn verdict/hiệu quả trên dữ liệu độc lập. Bản sửa hồ sơ cuối T-053 mới tự kiểm; không ghi Claude đã kiểm riêng bản ấy. Các câu hỏi P7/G3, chế độ (b), RE3 và FlashTicket vẫn OPEN.
- File của gói đóng: DECISIONS/WHY/kế hoạch/STATE, LOG hai task, bộ SPEC/LOG và hồ sơ nguồn T-049 theo Q-238. Báo cáo/manifest T-048 không đổi. Snapshot nguồn quản trị trước cập nhật ở results/T-049/nguon-truoc-ghi-quyet-dinh/; manifest khởi tạo T-049 liên kết các hash cũ.
- Bước tiếp: đọc tasks/T-049-k-b-va-t6/SPEC.md và LOG.md, sau đó chuẩn bị số học/công cụ theo bước 0. Chưa chạy T-049; dự toán lượt dài phải trình trước theo luật hiện hành. Không commit/push.
- Lệnh kiểm dùng: Python -B đọc manifest và tính SHA-256 (mã/receipt của lượt khởi tạo ghi trong hồ sơ T-049). Kiểm cuối gói đóng theo results/T-049/scripts/kiem_ho_so.py; kết quả được chép ở mục xác nhận cuối LOG T-049. Không mở lại nghiên cứu T-048.

### Prompt chuyển Claude — kiểm hồ sơ kết thúc

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-048 và T-053; tasks/T-048-thang-diem-tham-so-e4/ và tasks/T-053-kiem-z-chay-lai-k/.
- Công đoạn: Kiểm lại phản hồi và sửa.
- Gói/cổng: P6, chuẩn bị hồ sơ G3; G3 chưa mở.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện chính thức.
- Tài liệu gốc: AGENTS.md; docs/STATE.md; SPEC/LOG hai task; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/KE-HOACH-SAU-T047.md; nguồn đề tài theo mẫu; snapshot tại results/T-049/nguon-truoc-ghi-quyet-dinh/.
- Phản biện và phản hồi trước: Các lượt chat được lưu theo thứ tự ở results/T-053/runs/dap-phan-bien-001/kiem-tra.json; LOG hai task.
- Code và kết quả liên quan: results/T-048/manifest.json; results/T-053/manifest.json; results/T-049/manifest-khoi-tao.json; src/m1/; src/m1_danh_gia/; bản nguồn ghim và môi trường theo LOG hai task.
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ đọc và trả lời trong chat; không sửa file.

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
