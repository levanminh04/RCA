# T-033 — Lần theo cơ chế báo động trước mốc

- **Trạng thái:** Minh duyệt SPEC và thực hiện ngày 09/10/2026 (Q-91, Q-92; lời duyệt "ĐÃ CHỐT"); SPEC đã khóa. Đang thực hiện các chặng được duyệt; tiến độ ở dòng T-033 STATE và LOG.
- **Phạm vi bổ sung:** giữ tên task, lần theo cả báo động trước mốc, tác động các phần tiền xử lý và độ trễ/không báo sau proxy. Không coi mốc tiêm là onset thật.
- **Người làm:** Codex (Minh chọn ngày 09/10/2026).
- **Người phản biện:** Claude (Minh chọn ngày 09/10/2026).
- **Thuộc gói MRP:** P4 — **Cổng:** G2.
- **Thiết bị tính toán đề xuất:** EC2 3.107.246.249, keys.pem. Laptop điều khiển và nhận kết quả.
- **Phụ thuộc:** kết quả đã đóng T-025 và T-029; không cần đợi T-032. Hai task có thể tính toán song song trên hai EC2. Kết quả dùng cho tổng hợp G2 và căn cứ P6; không tự duyệt G2.

## Mục tiêu

Task phục vụ RQ2 và P4 trong docs/MRP.md: chỉ ra bước tính toán dẫn tới báo động trước proxy, phần tiền xử lý tạo khác biệt và độ trễ/không báo sau proxy ở detector đã chạy trên dev; phân biệt giả định phương pháp, cài đặt, đầu vào và giao thức. Nguồn trực tiếp là docs/reference/sources/advisor-2026-09-23.md §1, đoạn yêu cầu hiểu sâu phương pháp và chỉ ra hạn chế; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md §2, DT18-NV2 và DT18-NV3.

Task lần theo đầu vào → tiền xử lý → thống kê/phân phối → quy tắc báo động → cách chấm, không dùng số cờ hoặc số điểm đổi làm lời giải thích. Báo động trước mốc tiêm không tự chứng minh đó là báo động giả trong vận hành: đoạn trước mốc có thể chứa thay đổi thật, dấu hiệu khác, hoặc vấn đề của giao thức.

Câu hỏi chính là bước nào làm tín hiệu bị chấm bất thường trong điều kiện quan sát được, và bằng chứng nào phân xử các giải thích khác. Hoàn thành task không mặc nhiên giải thích mọi nguyên nhân vật lý, xác định thời gian sự cố thật, chọn detector mới hoặc đóng RQ2/G2.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi và nguồn yêu cầu | Kết luận/lựa chọn cần phân xử; giải thích khác | Phép kiểm và bằng chứng cần có | Kết quả hỗ trợ, bác bỏ hoặc chưa phân xử | Phần còn thiếu, quyết định phụ thuộc và hướng xử lý |
|---|---|---|---|---|
| P4: N-Sigma báo do bước nào? | Giá trị lệch; độ lệch chuẩn nền nhỏ; số quan sát/lịch sử; nhiều cột; tiền xử lý; thay đổi thật trước mốc | Giá trị, số quan sát nền, mean/std quá khứ, ngưỡng, mức vượt và cột bật cờ; so điểm báo và điểm không báo trong cả hai bộ cột | Xác định được phép tính bật cờ thì giải thích cơ chế tính toán; cờ không xác nhận sự cố hoặc nguồn vật lý | Nếu cần hiệu chỉnh ngưỡng/SLI, phải có căn cứ và phép kiểm riêng; không suy từ tỷ lệ báo trước mốc |
| P4: BOCPD tạo điểm đổi qua bước nào? | Đầu vào/tiền xử lý; số chiều/prior; likelihood; posterior/run length; quy tắc suy điểm đổi; vấn đề số học | Lưu ma trận đầu vào, tham số, predictive likelihood, posterior, m và bước suy điểm đổi tại điểm đổi cùng điểm lân cận không đổi | Lần theo đúng bước tạo chênh lệch; số điểm đổi tương tự không tự loại một tham số khỏi nguyên nhân | Thiếu trung gian thì phát lại đúng phần; cần can thiệp thì nêu giả thuyết cạnh tranh, dự đoán và chi phí |
| P4: phần nào của full/I1 tạo khác biệt trước proxy? | Scale; gói tập cột+số chiều+prior; tương tác; suy biến do cột hằng/NaN | Thiết kế hai yếu tố mask × nguồn min/max trên cùng tiền tố, kiểm đường chéo khớp F-prefix/I1 | So scale trong cùng mask có thể phân xử scale; so mask chưa tách riêng cột với prior; báo tương tác | Đủ căn cứ có điều kiện cho thiết kế không nhìn trước P6; mọi nhánh tiền tố vẫn là chẩn đoán, chưa chọn detector online |
| P4: trước mốc có thay đổi thật hay do detector/giao thức? | Thay đổi ở telemetry; tải, lỗi nền, coverage, sampling hoặc đồng hồ; mô hình thống kê không phù hợp | Đối chiếu trace/log và tải ở đúng nhóm cần phân xử, có điểm/ca đối chứng và mô tả coverage | Đồng xuất hiện là bằng chứng hỗ trợ, không tự là nguyên nhân hoặc kiểm độc lập | Thiếu nhãn nền sạch/onset thật thì giữ nguyên phần vật lý OPEN, nêu đúng trường và phép kiểm cần bổ sung |
| P4: độ trễ sau proxy đến từ đâu? | Tín hiệu đầu vào; lịch sử/thống kê hoặc likelihood/posterior; quy tắc suy báo động; onset thật chưa biết | Phát lại native trên toàn bản ghi, lần theo tới báo đầu sau proxy hoặc hết file; đối chiếu ngưỡng N-Sigma cập nhật/cố định và trạng thái BOCPD trước báo | Xác nhận đường tính tạo chênh lệch khi bằng chứng đủ; mốc vượt ngưỡng quan sát không là onset thật | Căn cứ P6 tách trễ theo proxy, tính toán và giới hạn tín hiệu; chấm độ nhạy thời lượng D chỉ là đề xuất kiểm tiếp riêng |

## Đầu vào

- Giao thức, cách chấm và cấu hình detector đã duyệt trong tasks/T-022-giao-thuc-p3/, results/T-022/ và task nguồn T-025.
- Bản ghi dự đoán của T-025; bản đồ hạn chế, bảng theo ca, các nhánh BOCPD và phép kiểm N-Sigma đã lưu của T-029. Nguồn tại results/T-025/ và results/T-029/.
- src/p3/adapters/phat_hien.py, code chấm trong src/p3/ và code BARO revision e35f4ec đã dùng cho detector. Môi trường/revision tại results/T-031/moi-truong.json và manifest của lượt nguồn tương ứng.
- Phạm vi: toàn bộ RE2-TT dev được cho phép trong T-025/T-029, gồm hai bộ cột N-Sigma và các nhánh chính BOCPD. Giữ trạng thái lỗi và kênh log thiếu là N/A; không loại nhóm khó.
- Manifest nền: results/T-029/runs/review4-repair-001/verification.json cho đầu ra sau sửa; manifest T-025 và manifest dữ liệu tương ứng. Lấy tên file từ manifest hoặc liệt kê thư mục trước khi đọc.
- Trước khi dùng đầu ra cũ, kiểm hash theo manifest phù hợp. Lệch thì dừng phần phụ thuộc, báo Minh và ghi LOG khi đã có quyền.
- Chỉ đọc dev trong allowlist đã duyệt; không mở data/locked/, test hoặc dataset giữ ngoài.

Môi trường tính toán phải khớp môi trường đã dùng: đọc results/T-031/moi-truong.json → /lenh_chay và /moi_truong. Dùng Python với -B -X utf8 và PYTHONDONTWRITEBYTECODE=1. Trên EC2 thay đường dẫn bằng môi trường/code đã kiểm, không tự cài package hoặc đổi phiên bản.

## Đầu ra

Trong results/T-033/:

- nguyen-nhan-phat-hien.md: cơ chế tính toán ở các nhóm báo động, giải thích cạnh tranh, giới hạn nguyên nhân vật lý/giao thức và quyết định P6.
- chuoi-bang-chung.json: theo ca/nhánh/điểm, nối đầu vào → tiền xử lý → thống kê hoặc phân phối → quy tắc báo động → chấm.
- bao-phu-nhom.json: nhóm bắt buộc, ca/điểm đại diện không trùng, đối chứng và điều kiện ghép/thiếu; ánh xạ toàn bộ ca vào các đường xử lý, không suy cơ chế từ đại diện.
- phan-ra-tien-xu-ly.json: FF/FP/PF/PP, mask/cột/order, fill, min/max, d/prior, suy biến, vector m/cờ CP và contrasts theo ca; nguồn của từng nhánh và mức được phân xử.
- do-tre-sau-moc.json: báo đầu toàn file và báo đầu sau proxy t_hat_plus, độ lệch có dấu với proxy, mật độ báo trước proxy và chuỗi cờ liên tiếp qua proxy, nhóm không báo, trạng thái tính toán/tín hiệu/chưa phân xử, bằng chứng ở mỗi bước và quyết định P6 phụ thuộc.
- nsigma-nguong-co-dinh.json: chẩn đoán ngưỡng nền cố định trước proxy so với ngưỡng cập nhật native, mọi cột/ca, điều kiện suy biến và giới hạn; không là detector được chọn.
- nsigma-trung-gian/: giá trị, số quan sát, mean/std quá khứ, ngưỡng, mức vượt và cột bật cờ của cả hai bộ cột; dữ liệu tại điểm không báo để đối chiếu.
- bocpd-trung-gian/: đầu vào, cột, scale/fill, số chiều/prior, m, posterior và predictive likelihood/cập nhật tại điểm đổi cùng điểm lân cận không đổi.
- doi-chieu.json: bảng toàn bộ ca, đối chiếu full/I1 và các nhóm báo/không báo; lựa chọn ca đọc tay theo điều kiện.
- tai-log.json: tải, dấu hiệu trace/log, coverage và giới hạn diễn giải ở nhóm cần kiểm; không gọi các kênh này độc lập thống kê.
- doc-tay.md: các chuỗi bằng chứng có điểm/ca đối chứng; phân biệt quan sát với cơ chế.
- kiem-tiep.md: mỗi câu còn cần kiểm có giải thích cạnh tranh, phép can thiệp/thu thêm, yếu tố cố định, dự đoán phân biệt, phạm vi, chi phí và quyết định bị ảnh hưởng.
- scripts/ và runs/: wrapper chẩn đoán, cấu hình, lệnh, thời gian, manifest và trung gian; giữ lượt hỏng.

Báo cáo đủ năm mục P4: hạn chế xác nhận và điều kiện; lỗi cài đặt/thiếu đầu vào; hạn chế giả định/cách tính; thông tin quan hệ có thể bổ sung; câu chưa trả lời và bằng chứng thiếu. Tách dữ liệu, giao thức, adapter/cài đặt và phương pháp; nêu hệ quả hạn chế dữ liệu cho đánh giá và quan sát FlashTicket.

## Phạm vi ghi

Phạm vi dưới đây chỉ có hiệu lực sau khi Minh duyệt thực hiện SPEC:

- results/T-033/, dùng thư mục lượt mới trong scripts/ và runs/.
- tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md: chỉ nối thêm.
- Duy nhất dòng T-033 trong docs/STATE.md.
- Trên EC2 3.107.246.249: chỉ thư mục mới ~/rca/T-033/.
- docs/WHY.md: chỉ nối WHY-41 đúng nội dung phụ lục được Minh duyệt, trước khi dùng lựa chọn trong kết quả.

Code, môi trường, dữ liệu và thư mục task cũ trên EC2 chỉ đọc. Chép đúng phần allowlist cần dùng vào thư mục mới và kiểm hash nguồn/đích. Laptop chỉ điều khiển, đọc tài liệu và nhận kết quả; toàn bộ tính toán nghiên cứu trên EC2.

Các lượt sửa nháp ngày 09/10 chỉ được sửa hai SPEC và nối DECISIONS theo Q-91/Q-92; không ghi STATE, WHY chính thức, LOG, dữ liệu hoặc đầu ra nghiên cứu. Người phản biện chỉ ghi bản lượt được Minh cho phép, hoặc trả lời trong chat.

## Nhóm, đối chứng và thời gian

Bảng tự động phủ mọi ca dev/hai bộ cột N-Sigma và các nhánh BOCPD trong phạm vi. Nhóm đọc tay bắt buộc: detector/bộ cột/nhánh × nhóm S/E/Miss theo proxy đã có, các cờ đa nhãn hoặc chưa giải thích của T-029 có ca, trạng thái non-OK; thêm đường mask/scale có khác biệt, suy biến và đối chứng không khác biệt ở phân rã mới. Không chỉ đọc các ca full/I1 khác nhau hoặc bỏ nhóm khó. Đơn vị đọc tay là ca × đường xử lý; một ca/điểm có thể phủ nhiều nhóm nhưng phải ánh xạ riêng. Khóa chọn trước khi diễn giải: cùng detector/bộ cột/dataset và loại đầu vào, ưu tiên cùng ô/coverage/quy mô; chọn opaque_id nhỏ nhất khi tương đương. Thuộc tính đang phân xử được phép khác, khai rõ. Ca không đổi/điểm không báo là đối chứng, không tự là ca “đúng” vận hành; không có đối chứng phù hợp thì ghi điều kiện thiếu.

Báo độ trễ liên tục cho mọi ca có báo sau proxy, không đặt nhãn Late hoặc ngưỡng trễ mới. Ca không báo tới cuối bản ghi giữ riêng với thời gian theo dõi; không biến số Miss theo proxy thành bằng chứng không bỏ sót thật. Ca đúng theo proxy, ca E có báo sau proxy và các điểm chưa báo trước báo đầu sau proxy đều có trong đối chiếu. Mọi nhận định cơ chế theo ca/đường xử lý, không lan từ một ví dụ sang nhóm.

Đặt độ lệch sau proxy cạnh báo trước proxy: với từng detector/bộ cột/ca, báo số điểm có cờ và số điểm detector được phép đánh giá trong đoạn trước proxy, thời gian đoạn đó và tỷ lệ số điểm có cờ trên mẫu số ấy. Giữ quy tắc bắt đầu/flags native, không chọn đoạn “nền sạch” mới; N-Sigma thêm mẫu số thống kê hữu hạn để phân biệt False do NaN. Lưu các chuỗi cờ True liên tiếp theo lưới thời gian, thời điểm đầu/cuối và chuỗi nào chứa điểm trước proxy lẫn điểm tại/sau proxy; điểm không có trên lưới hoặc trạng thái lỗi không tự nối thành chuỗi. Với BOCPD dùng cờ CP đã khai, không tự gộp CP rời thành một episode. Độ lệch bằng 0 có thể nằm trong chuỗi báo đã bắt đầu trước proxy hoặc là điểm báo riêng; báo đúng trường hợp, không gọi cả hai là vừa phát hiện sự cố. Không đặt ngưỡng mật độ, độ dài chuỗi hoặc nhãn mới; mọi cờ trước proxy chưa tự là false alarm vận hành.

Dùng ánh xạ lưới đã kiểm của nguồn: i_proxy là vị trí mốc tương đối trong bản ghi, t_proxy là timestamp tương ứng. 720 giây/chỉ số theo nguồn không tự là timestamp UTC 720. Kiểm cả time array và index map trước cắt/chấm; mốc sai, trùng hoặc không resolve thì dừng ca liên quan. Engine nhận ma trận/time hợp lệ, không nhận t_proxy/root/nhãn; việc cắt, freeze và chọn điểm đọc tay là chẩn đoán có dùng proxy, khai riêng.

## Phân rã tiền xử lý BOCPD

**Chọn thiết kế hai yếu tố:** M_F/M_P là mask cột giữ sau drop_constant trên raw full/raw tiền tố, trước fill đúng native; S_F/S_P là min/max sau ffill().fillna(0) trên nguồn full/tiền tố. Giữ tập cột tên/thứ tự gốc, hazard và engine. Full đã dùng tương lai qua mask/scale; prefix còn dùng tương lai trong tiền tố.

| Nhánh | Mask | Min/max | Đối chiếu nguồn |
|---|---|---|---|
| FF | M_F | S_F | F-prefix: tiền xử lý full rồi cắt ma trận |
| FP | M_F | S_P | Nhánh chẩn đoán mới |
| PF | M_P | S_F | Nhánh chẩn đoán mới |
| PP | M_P | S_P | I1 đóng băng |

Tạo các ma trận cùng raw tiền tố, lấy mask trước fill; tính nguồn min/max theo đúng từng cột sau fill, scale rồi ffill().fillna(0) đúng adapter. FF phải bằng ma trận prefix của native full, PP phải bằng native I1; không tự gọi scaler khác thay công thức. Nội dung code chi phối: src/p3/adapters/phat_hien.py → tien_xu_ly_bocpd; BARO utility.drop_constant và _bocpd.MultivariateT ở revision nguồn.

- FF↔FP và PF↔PP: giữ mask/d/prior, đổi nguồn scale; tách được tác động nguồn min/max trong điều kiện mask đó.
- FF↔PF và FP↔PP: đổi gói cột+số chiều+prior, không đổi nguồn scale trên các cột chung. Prior native có d phụ thuộc mask; không gọi đây là hiệu ứng riêng bỏ cột hoặc riêng prior.
- Báo cả hai contrasts và tương tác, không chọn một đường đi để gán tổng full/I1 cho một yếu tố. Với cột thuộc M_F còn hằng-prefix, range S_P=0 gây collapse (co giá trị sau xử lý về 0): native chia rồi NaN→fill0; đây không chỉ là đổi affine khả nghịch. Giữ cùng raw prefix, mask, d và prior, khác biệt đầu vào xử lý đến từ nguồn min/max và đường xử lý range 0 của native. Đây không phải khác biệt raw prefix giữa hai nhánh và không chứng minh hệ thống thay đổi thật. Ghi nguồn collapse, không thêm epsilon hoặc bỏ lại cột để làm nhánh chạy; đầu vào khác chưa bảo đảm likelihood/posterior/CP khác, phải đối chiếu các bước thực tế.
- Với raw tiền tố không rỗng cùng đầu chuỗi và cùng drop_constant native `(df != df.iloc[0]).any()`, M_P phải là tập con M_F, kể cả NaN. Kiểm tập cột thực tế; vi phạm quan hệ này là lỗi input/cắt/version cần dừng, không là effect của NaN. Cột mất/giữ sau fill, NaN/Inf, đầu chuỗi thiếu, range0 và d=0 đều có trạng thái theo ca. Không chèn cột giả, đổi prior hoặc gán zero alarm. Nếu native lỗi thì giữ lỗi; nếu d=0 mà native vẫn trả kết quả, giữ kết quả với nhãn không có kênh đầu vào, không gọi đó là bằng chứng tín hiệu ổn định. Không gom input trùng, collapse hợp lệ, không có kênh và nhánh lỗi thành một trạng thái: cùng ma trận/thứ tự/shape và tham số, đầu ra hợp lệ thì contrast bằng 0; range0 đã qua fill native mà đầu vào/đầu ra hợp lệ vẫn báo contrast tính toán, kể cả bằng 0. d=0 giữ kết quả/lỗi native và nhãn không có kênh, không tự INVALID; không quy nó thành bằng chứng từ tín hiệu. Nhánh lỗi không định nghĩa contrast CP/m thì báo trạng thái/lỗi, không gán 0. Bộ đếm khai mẫu số hợp lệ, không có kênh và không định nghĩa riêng; thiếu chuẩn onset áp dụng cho kết luận vật lý, không xóa contrast tính toán hợp lệ.
- Cờ CP, vector m theo từng chỉ số, tập CP thêm/mất, báo đầu và chênh có dấu là đầu ra chính; không chỉ đếm tổng CP. Khai toàn bộ ca kể cả không khác biệt và lỗi; không điều chỉnh hazard, prior hay scale để tạo hiệu ứng.

**Vì sao không thay prior độc lập ngay:** bỏ cột làm đổi không gian và prior native; “cùng prior” qua hai chiều không có nghĩa duy nhất. Giữ cột rồi đặt zero/rescale prior là một mô hình khác, chưa có căn cứ để coi là phép cô lập prior. Phân rã này trả lời rõ scale, gói cột/d/prior và tương tác; phần chưa tách ghi OPEN cùng phép kiểm cần trình tiếp.

**Giới hạn cho P6:** nhánh PP vẫn nhìn trước ở mask/scale trong tiền tố; FF/FP/PF chứa thông tin full. Không nhánh nào được gọi là detector online không nhìn trước. Kết quả chỉ cho căn cứ về những phép xử lý nào phụ thuộc tương lai và bước cần thay khi thiết kế causal preprocessing. Muốn chọn scaler/feature/prior cập nhật chỉ từ quá khứ còn phải đặc tả, kiểm trên dev và đối chiếu phương án tại P6, không suy ưu thế của detector mới từ CP đổi ở đây.

## Lần theo độ trễ sau proxy

Giữ trạng thái thuật toán từ đầu bản ghi, không reset tại proxy. Phát lại N-Sigma cả hai bộ cột và BOCPD native full trên toàn bản ghi để kiểm nguồn và giải thích trước/sau proxy. Với FF có thể dùng prefix của kết quả full khi ma trận và kiểm tính phụ thuộc prefix đạt, tránh lượt tính trùng; PP và hai nhánh hybrid chỉ chạy tiền tố cho câu hỏi phân rã.

**N-Sigma:** ở mọi điểm/cột lưu x, số quan sát, mean/std của [:i] với ddof=1, |x−mean|, k·std và phép so strict > đúng native, bắt đầu 100. Đối chiếu từ proxy tới báo đầu sau proxy hoặc cuối file; chỉ ra cột và bước bật cờ. Thêm nhánh chẩn đoán nền cố định bằng [:i_proxy], cùng k=3/fill/ddof, chỉ so hậu proxy với nhánh cập nhật. Tại điểm hậu proxy đầu tiên, mask NaN và các giá trị hữu hạn của thống kê hai nhánh phải bằng nhau; lưu chênh ngưỡng và thời điểm vượt theo từng cột/gộp. Khác biệt là tác động cập nhật lịch sử trong điều kiện này, không mặc nhiên là “nền bị nhiễm” hoặc thuật toán sai.
- Thiếu quan sát, std NaN, std=0, đầu chuỗi thiếu và strict > giữ hành vi native; NaN trong phép so cho cờ False, không đổi cờ thành N/A hay ép có báo. N/A chỉ là trạng thái diễn giải contrast khi thiếu thống kê, tách khỏi cờ native. Không sàn std/thêm epsilon.
- Mốc dùng freeze do chẩn đoán; đây không là detector mới hợp lệ cho tự phát hiện. Thời điểm vượt ngưỡng cố định cũng không là onset thật hoặc bằng chứng nền sạch.

**BOCPD:** lưu predictive density theo run length, mass trước chuẩn hóa/normalizer, posterior, m và đối thủ gần nhất, bước cập nhật tham số và |m[i]−m[i−1]| tại CP và các điểm trước đó chưa CP. Lưu đường m/cờ cho toàn file; giữ đủ trạng thái ở vùng proxy→báo đầu sau proxy, ca không báo tới cuối file. Phân biệt đầu vào biến đổi quan sát được, posterior/MAP phản ứng và quy tắc |Δm|>1 bật tại điểm nào. Với constant hazard và normalization hợp lệ, R[0,t] có thể bằng hazard theo cấu tạo: kiểm bằng công thức native, không dùng nó làm xác suất/score phát hiện để gán trễ.
- Các bản raw và processed khác nhau vì tiền xử lý full nhìn trước; ghi nguồn cả hai. Không quy mốc thay đổi tín hiệu thật chỉ từ biến động raw hoặc m.
- Dữ liệu quan sát có thể cho biết thuật toán phản ứng qua bước nào; thiếu onset/semantics độc lập thì chưa phân xử phần trễ do sự cố thật bắt đầu muộn so với proxy. Nêu đúng kênh/sự kiện thiếu và quyết định P6 phụ thuộc.

**Mức kết luận:** BOCPD báo “độ lệch vị trí điểm đổi hồi cứu so proxy”, N-Sigma báo thời gian đến vượt ngưỡng so proxy, không là độ trễ vận hành tính từ onset đã biết. Có thể xác nhận cơ chế tính toán ở một bước, liên hệ tín hiệu hoặc chưa phân xử; không ép một nguồn trễ duy nhất. Không đặt tỷ lệ “trễ do dữ liệu” bằng số ca có biến động raw.

## Phép thử D chuyển sang kiểm tiếp

Không tạo do-nhay-D.json hoặc chạy lưới D trong lượt thực hiện hiện tại. kiem-tiep.md ghi câu hỏi về giả định **thời điểm kết thúc/thời lượng** đoạn sự cố sau proxy; nó không thay onset và không đổi nhãn S/E của báo đầu. Nếu có căn cứ hoặc Minh duyệt phân tích độ nhạy riêng, phải khai D/nguồn, giữ dự đoán và số P3 gốc, báo cách chấm cạnh nhau. Không suy D đúng từ điểm đẹp; không gọi một đề xuất mới tự nó là sửa giao thức task đã đóng. Phép D vẫn cần Minh quyết trước chạy.

## Các bước

1. **Kiểm nguồn, đọc code và lập bảng trung gian.** Theo cả chuỗi detector và bộ chấm; xác định phần đã lưu/thiếu ở mọi ca và nhóm quan trọng trước khi phát lại.
2. **Lần theo N-Sigma theo đúng code gốc.** Giữ k=3, bắt đầu từ chỉ số 100, thống kê nền quá khứ và ddof=1 cùng hành vi NaN của bản đã chạy. Lưu giá trị, số quan sát, mean/std, ngưỡng, mức vượt và cột kích hoạt theo thời điểm. Cờ của cả hai bộ cột phải khớp nguồn đóng băng; đối chiếu cả điểm báo và không báo.
3. **Phát lại BOCPD native full và hai đường chéo tiền tố.** Full phục vụ cả kiểm nguồn lẫn độ trễ sau proxy; F-prefix/I1 phục vụ câu hỏi trước mốc.
   - **F-prefix:** tiền xử lý toàn bản ghi theo cấu hình full đã khóa, rồi cắt ma trận đã xử lý ở trước mốc 720 giây. Không tiền xử lý lại ma trận tiền tố.
   - **I1:** cắt bản ghi trước mốc trước, rồi tiền xử lý tiền tố theo nhánh I1 đã lưu.
   - Giữ hazard/tham số nguồn, cột/d/prior thực tế. Nhánh full chạy toàn bản ghi, PP chạy tiền tố; FF có thể lấy từ full khi kiểm cùng ma trận/tính prefix đạt. F-prefix còn nhìn trước qua preprocessing full; I1 còn nhìn trước trong tiền tố.
4. **Kiểm phát lại trước khi diễn giải.** Full khớp trạng thái và CP/time khi nguồn OK; khi nguồn non-OK phải tái lập đúng trạng thái/lỗi/diagnostic nguồn. FF kiểm ma trận prefix của full và CP trước proxy khi nguồn có đường hợp lệ; PP khớp I1 theo từng ca. Nếu full ERROR vì R hỏng sau tiền tố, adapter xóa toàn bộ alarms; FF hữu hạn vẫn có thể có CP hợp lệ. Không ép CP của FF bằng alarms rỗng từ full ERROR; chỉ đối chiếu trung gian prefix hợp lệ đã lưu nếu có, còn CP-prefix không có nguồn phải kiểm native cùng ma trận. Sai khác dừng ca/nhánh phụ thuộc, không thay số cũ. Lưu m/R/likelihood/update đủ câu hỏi trước/sau proxy; kiểm shape, hữu hạn, normalization, sentinel và index map. Không yêu cầu R trùng từng bit với máy nguồn; R khác mà CP khớp không tự làm sai contract, nhưng phải ghi provenance/sai khác và không dùng chênh nhỏ đó như hiệu ứng cơ chế.
5. **Phân rã mask × scale và chẩn đoán độ trễ.** Chỉ sau phần phát lại lõi của ca được xác minh, gồm cả tái lập đúng non-OK; không lấy OK làm điều kiện loại ca. Nhánh mới có input/schema hợp lệ vẫn được chạy để giữ lỗi/suy biến riêng; chạy FP/PF và nhánh N-Sigma cố định theo các mục riêng, kiểm nhánh mới rồi tạo contrasts. Không sửa wrapper/lựa chọn lõi để chạy bổ sung.
6. **Đối chiếu ca và điểm.** Bảng toàn bộ và danh mục nhóm/đối chứng theo mục trên; đọc cả nhánh có/không thay đổi, CP/no-CP và đường suy biến. Không kết luận từ một ví dụ hoặc chỉ tổng số điểm đổi.
7. **Đối chiếu kênh khác và giao thức chấm.** Đọc trace/log và tải ở nhóm cần phân xử, nêu coverage/thiếu kênh; tái lập chấm proxy gốc. Mọi mốc biến động/vượt ngưỡng chỉ là quan sát dưới quy tắc đã khai, không onset thật. Phép D chỉ ghi trong kiem-tiep.md, chưa chạy.
8. **Tổng hợp câu trả lời và bước kiểm tiếp.** Nêu điều kiện X, bước Y, thông tin Z, bằng chứng hỗ trợ/bác bỏ và giải thích còn mở. Báo contrast scale, gói cột/d/prior và tương tác; phần không tách được không bị ép thành hiệu ứng riêng. Nêu độ trễ sau proxy đã phân xử ở bước nào và phần onset thật/giải thích khác còn thiếu. Không loại hazard khỏi nguyên nhân chỉ vì số điểm đổi gần nhau. Ghi phép phân xử còn thiếu và quyết định P6 phụ thuộc.

Các detector độc lập có thể xử lý song song trong ngân sách và RAM; không đợi T-032. Tính thống kê cho toàn bộ cột/thực thể trước khi nối nhãn root/loại lỗi để phân tích. Mốc cắt và cửa sổ chấm dùng để chẩn đoán theo giao thức, không đưa root, tên ca, đường dẫn nhãn hoặc mốc tiêm vào detector tự phát hiện. Không gọi các nhánh chẩn đoán này hoàn toàn không dùng thông tin nhãn.

## Kiểm đúng đắn

- Kiểm hash nguồn cũ và hash hai đầu khi chép sang EC2.
- Cờ N-Sigma của cả hai bộ cột khớp nguồn; mean/std chỉ lấy quá khứ theo đúng contract của code, số quan sát và NaN được lưu rõ.
- Native full và các đường chéo FF/PP khớp trạng thái/CP nguồn tương ứng khi nguồn có đường hợp lệ, theo quy tắc phát lại ở bước 4; tái lập non-OK cũng là xác minh lõi. Điểm đổi tính từ R/m phải khớp adapter, gồm sentinel và ánh xạ thời gian; không chỉ khớp số lượng hoặc coi alarms rỗng do ERROR là không phát hiện.
- Kiểm trung gian hữu hạn, shape, tổng xác suất và đường likelihood/update ở điểm đổi cùng đối chứng. Không đòi một bất biến không có trong contract code.
- Phép kiểm giả không nhãn: cột hằng, bước nhảy, giá trị lặp, thiếu đầu chuỗi, NaN/Inf và điểm chạm biên thời gian, theo hành vi hợp lệ của code gốc. Không tự đặt yêu cầu detector phải đúng nhãn ở dữ liệu giả không có chuẩn.
- So trace/log theo điều kiện và coverage; đồng xuất hiện không tự là nguyên nhân hoặc phép kiểm độc lập.
- Tái lập chấm proxy gốc; D chỉ là đề xuất kiểm tiếp, không chọn D/ngưỡng từ kết quả thuận lợi.
- Nhánh mới không có frozen output: wrapper ghi trung gian so với lời gọi native nguyên bản trên đúng ma trận/môi trường; identity FF/PP kiểm input và native đường chéo, sham không thay tham số phải khớp. Kiểm scalar/fixture ngắn cho fill/drop/scale, normalization, m→CP và thống kê N-Sigma bằng tính tay độc lập; không đòi detector phải đúng nhãn của fixture.
- Kiểm các contrasts thật sự giữ mask/prior hoặc nguồn scale như đã khai. Ma trận/tham số trùng và đầu ra hợp lệ cho chênh lệch 0; collapse hợp lệ qua range0/fill vẫn đo likelihood/posterior/m/CP, gắn nguồn xử lý đúng. d=0 giữ output/lỗi và nhãn không có kênh; NaN/Inf/nhánh lỗi giữ native, ghi contrast nào không định nghĩa, không đổi lỗi thành 0 hoặc chữa để đủ bảng. Không yêu cầu mọi input khác phải có CP khác.
- Kiểm số cờ/mẫu số trước proxy từ flags/time array, chuỗi liên tiếp và điểm báo tại/sau proxy của cả hai detector theo đúng lưới/quy tắc bắt đầu. Không nối qua lỗi hoặc khoảng thiếu, không đặt ngưỡng để gọi “báo dày” hay biến chuỗi cờ thành nhãn onset.
- Với ma trận đã xử lý cố định, thêm/bớt suffix phải giữ posterior/m/CP ở phần prefix; preprocessing có dùng suffix thì không đòi invariant này. Nhánh N-Sigma cố định kiểm bằng native statistics[:i_proxy], first-post mask NaN và thống kê hữu hạn bằng nhánh cập nhật; native cờ False khi so NaN giữ nguyên.
- R/m/CP và sai số normalization của wrapper mới so native cùng input/môi trường; không dùng một tolerance posterior để miễn CP lệch nguồn, không chọn tolerance theo effect muốn có. Không biến R[0,t] thành detector mới.
- Mọi số có đường dẫn và con trỏ JSON hoặc lệnh đã chạy kèm kết quả; không cộng cờ chồng lấn thành tỷ lệ nguyên nhân.
- Đối chiếu mục tiêu DT18/cô và năm đầu ra P4 trước nghiệm thu, không chỉ kiểm số khớp và đủ file.

## Tiêu chí xong

1. Nguồn đạt hash; N-Sigma và BOCPD native full/FF/PP khớp trạng thái, cờ/CP/time ở đường có nguồn hợp lệ; non-OK được tái lập đúng và giữ riêng theo bước 4, không bị loại khỏi coverage.
2. Nhóm bắt buộc có chuỗi đầu vào → xử lý → trung gian → đầu ra và đối chứng theo điều kiện, ánh xạ đầy đủ vào bao-phu-nhom; nhóm chưa phân xử ghi đúng bước thiếu/điều kiện thiếu và phép kiểm cần trình Minh, không suy từ đại diện.
3. Có phân rã FF/FP/PF/PP theo ca, effect scale/gói mask-d-prior/tương tác và trạng thái input trùng/collapse hợp lệ/không có kênh/lỗi; giải thích rõ phần tách được/không, thông tin tương lai còn dùng và căn cứ có điều kiện cho causal preprocessing ở P6. Không nhận đã chọn/kiểm detector online.
4. Có chuỗi độ trễ N-Sigma/BOCPD tới báo đầu sau proxy hoặc cuối file, số cờ/mẫu số/mật độ trước proxy và chuỗi báo qua proxy, contrast lịch sử N-Sigma và giới hạn tín hiệu/onset; không đặt Late mới, không nhận báo trước proxy là false alarm vận hành hoặc suy nguyên nhân vật lý.
5. Đủ năm đầu ra P4 và căn cứ/giới hạn P6, dữ liệu/giao thức/quan sát FlashTicket; D ở kiểm tiếp, không thành tiêu chí chính.
6. LOG/checkpoint qua nhiều phiên, diff/phạm vi, dòng STATE và prompt bàn giao đầy đủ theo luật.

Task hoàn thành không tự đóng RQ2/G2. Phần còn OPEN ảnh hưởng chọn detector/thành phần P6 phải được trình bằng phép kiểm cụ thể hoặc giới hạn lựa chọn để Minh quyết.

## Không làm

- Không sửa detector, ranker, P3/P4 đã đóng, giao thức hoặc nhãn; không chọn hazard/ngưỡng mới và không mở test.
- Chưa chạy lô 180 phép thử IAAFT/Gaussian thay thế chuỗi như các can thiệp nguyên nhân đã cô lập. Cần xác định giả thuyết cụ thể, thuộc tính được giữ/đổi và hiệu ứng tiền xử lý trước; nếu trung gian cho thấy cần, trình đúng phép thử và dự đoán phân biệt. Không tự bỏ nghĩa vụ phân xử vì phép ấy chưa có trong lượt này.
- Không tạo “nền sạch”, onset thật hoặc D đúng từ proxy. Thiếu chuẩn phải ghi OPEN và bằng chứng cần bổ sung. Nhánh nền cố định dùng proxy là chẩn đoán, không là detector tự phát hiện mới.
- Không đánh giá lợi ích phương pháp đồ thị mới; đối chứng cấu trúc thuộc bước đánh giá cơ chế tương ứng.
- Không tự cập nhật SPEC T-034 hoặc kết luận gói G2 đủ căn cứ chỉ vì hai task xong.

## Qua nhiều phiên và lượt chạy dài

Minh quyết giữ cùng T-033 qua nhiều phiên (Q-91), ngoại lệ có chủ ý với AGENTS §5a.4 và yêu cầu một phiên ở §5. Không tạo task mới, không giảm phần sau proxy/phân rã để vừa phiên. Hình thức chạy dài/qua đêm được phép; thực hiện và ngân sách vẫn chờ duyệt.

| Chặng | Phụ thuộc | Checkpoint |
|---|---|---|
| Chuẩn bị | Duyệt thực hiện/ngân sách, WHY-41 được phép nối | Source/hash/allowlist, máy/env, index map, danh mục nhóm, trung gian thiếu, disk/RAM và budget |
| Lõi native | Nguồn đạt cho từng ca/nhánh | N-Sigma toàn file, BOCPD full/PP, FF tái dùng hợp lệ; trạng thái nguồn kể cả non-OK và CP/flags hợp lệ khớp, run/progress/manifest sau mỗi ca |
| Nhánh bổ sung | Lõi ca được xác minh cả OK/non-OK và kiểm wrapper/fixture mới đạt | FP/PF, ngưỡng N-Sigma cố định, trạng thái/suy biến/contrasts theo từng ca; không sửa nguồn lõi |
| Độ trễ/kênh/đọc tay | Trung gian ca đạt | Điểm báo/không báo, mật độ trước proxy/chuỗi báo qua proxy, đối chứng/coverage, trạng thái điều đã biết/chưa biết và nhóm được phủ |
| Tổng hợp | Chặng cần dùng đạt hoặc OPEN có bằng chứng | Năm đầu ra P4, phần chưa phân xử, dự thảo kiểm tiếp cụ thể, kiểm số/diff và prompt Claude |

Một ca/nhánh hợp lệ là đơn vị tiếp tục, không tự chạy lại cả lô. Lượt qua đêm ghi PID, lệnh đầy đủ/môi trường, stdout/stderr/progress, thư mục kết quả riêng T-033; không dựa vào phiên SSH còn mở. Cuối mỗi bước/phiên ghi LOG đủ chặng xong/đang chạy/chưa chạy, last command, ca/nhánh cuối hợp lệ, manifest/hash, vị trí process và điều cần quyết. Người nhận tiếp kiểm process/hash/nguồn rồi tiếp phần thiếu; không khởi trùng lượt đang chạy. Dừng phần phụ thuộc khi hash/CP lệch, wrapper đổi phép tính, hết disk/RAM hoặc quyền chưa rõ; giữ lượt hỏng và trình giải pháp. Ba lần cùng chỗ không tiến triển thì dừng theo §5a trong cùng task.

## Chi phí ước lượng và ngân sách chờ duyệt

- Tham chiếu nhánh I1: results/T-029/runs/ec2-complete-002/artifacts/runs/chuoi-002/i1/*.json → /wall_s cộng wrapper50-adapter.json → /wall_s; hash theo review4-repair-001/verification.json → /files. Tổng 1.984,797 giây, khoảng 33 phút. Không coi đó là giá cố định cho full/hybrid khác chiều/máy.
- **Chưa kiểm — giờ máy dự trù:** 4–12 giờ cho native full, PP, hai hybrid, ghi trung gian, kiểm và N-Sigma; FF tái dùng prefix full khi đủ điều kiện để tránh tính trùng. Phụ thuộc số chiều, độ dài bản ghi và mức ghi R/likelihood; không có phép đo instrumented full/hybrid hiện tại, có thể vượt dự trù. Đây không là timeout.
- **Chưa kiểm — công agent:** viết/kiểm wrapper, factorial và nguồn 8–16 giờ; đọc tay/đối chứng/độ trễ và kênh 8–16 giờ; tổng hợp/tự kiểm/báo cáo 4–8 giờ. Dự toán gồm phần sau proxy, không còn chỉ 2–4 giờ máy tiền tố. Khối lượng nhóm thực tế ghi ở bao-phu-nhom trước đọc tay; không cắt phần khó theo thời gian.
- Dự trù tối đa 4 GiB mới gồm đầu vào, trung gian/tạm và lượt hỏng. Nơi RE2 dev đã có/thiếu trên EC2, số byte cần chuyển và tốc độ route chưa kiểm hiện tại; kiểm allowlist/hash và đo route nhỏ sau duyệt trước lượt chuyển lớn. Không chép lại phần hợp lệ.
- Lưu m/cờ/normalizer cho toàn bộ điểm, R/likelihood/trạng thái đủ cho các vùng cần hỏi; không lưu mọi ma trận hiệp phương sai cho mọi run length/mọi thời điểm. Nếu thiếu trung gian cần đọc thì đề xuất mở rộng lưu, không tự bỏ câu hỏi. Đo output sau ca đầu, cập nhật dự toán cùng task trước vượt dung lượng được duyệt.
- Bắt đầu một worker nặng; tối đa hai nếu RAM thực tế đủ và không chia sẻ mutable state. Không hứa chia thời gian tuyến tính. Kiểm chỗ trống EC2 trước chạy, thiếu thì trình, không xóa dữ liệu/run cũ.
- Minh duyệt thực hiện/ngân sách sau rà SPEC. Cho phép chạy dài/qua đêm khi đã duyệt; không đặt giới hạn một giờ để cắt kiểm. Nếu vượt ngân sách/phạm vi đã duyệt, checkpoint và trình tiếp trong cùng task; thời gian không dùng để giảm tính đúng.

## Rủi ro và điều chưa chắc

- **Chưa kiểm:** đổi từ EC2 nguồn sang EC2 mới/khác máy có thể đổi số học. Mỗi run ghi OS/kiến trúc/Python/package/BLAS/thread/hashseed/code/config nguồn và đích. Trạng thái/CP/time/flags lõi phải khớp tuyệt đối; R không yêu cầu trùng bit với nguồn. CP lệch thì dừng ca/nhánh, trình Minh; không tự thêm tolerance CP, đổi package hoặc chạy laptop.
- **Chưa kiểm:** engine tiền tố giữ hành vi CP như nguồn sau khi cố định ma trận tiền xử lý. Khi wrapper/tham số/chỉ số khác, điểm đổi có thể lệch; phải kiểm từng ca trước khi dùng. Kết luận chuỗi BOCPD phụ thuộc phép khớp này.
- **Chưa kiểm:** factorial có nhánh hữu hạn/đủ chiều và contrast có thông tin. Mask đổi vẫn gắn với prior, scale có range0 không là affine thuần; input/tham số trùng và đầu ra hợp lệ cho contrast 0; collapse hợp lệ vẫn đo được. d=0 khai không có kênh; lỗi giữ trạng thái và contrast CP/m không định nghĩa, không gom thành vô thông tin. Thiếu hiệu ứng không chứng minh yếu tố không quan trọng. Quy riêng prior hoặc lợi ích scaler causal còn phụ thuộc thiết kế/kiểm tiếp.
- **Chưa kiểm:** trace/log có dấu hiệu đủ phân biệt thay đổi thật trước mốc với hành vi thống kê/giao thức. Kênh thiếu hoặc cùng nguồn quan sát có thể làm giải thích chưa phân xử; không dùng đồng xuất hiện như sự thật nguyên nhân.
- Proxy và các thời điểm vượt ngưỡng là quy ước/quan sát, không onset thật. Thuật toán có thể phản ứng muộn do đường tính và tín hiệu thay đổi muộn hoặc yếu; lack of onset không bị chữa bằng threshold mới. Phần false alarm vận hành, trễ vật lý và lựa chọn detector P6 giữ mức căn cứ thích hợp.
- Nhánh mới có thể tốn storage/CPU hoặc làm wrapper thay trạng thái; lõi giữ riêng và được kiểm trước, biến đổi chỉ trên bản sao. Tiêu chí/seed/ngưỡng native và lịch so nhánh đã khai trước kết quả; không chọn nhánh vì số CP đẹp.

## Phụ lục — dự thảo WHY-41

**Chọn:** xác minh lõi native full/FF/I1 theo trạng thái nguồn, kể cả tái lập non-OK, trước; khóa nhóm/đối chứng và ánh xạ ca; phân rã mask × nguồn min/max trên tiền tố, lần theo độ trễ full và contrast ngưỡng N-Sigma cập nhật/cố định trước proxy. D chuyển sang kiem-tiep, chưa chạy. Nhánh mới là chẩn đoán; không chọn detector online hoặc đổi số P3.

**Vì sao:** cờ/số CP không chỉ bước gây báo; full/I1 đổi nhiều yếu tố. Giữ mask để so scale, giữ nguồn scale để so gói cột/d/prior, báo tương tác để không gán tổng effect cho một phần. Full cần cho trạng thái sau proxy; ngưỡng cố định cùng k native kiểm tác động cập nhật lịch sử, không chứng minh nền sạch. Đặt độ lệch sau proxy cạnh mật độ báo trước và chuỗi cờ qua proxy để không gọi báo đang tiếp diễn là vừa phát hiện sự cố; không thêm ngưỡng. Giữ raw prefix/mask/d/prior thì contrast nguồn scale/fill là khác biệt xử lý, không tự là thay đổi thật của hệ thống; đo đường likelihood/posterior/CP, không buộc đầu vào khác phải đổi CP. Tái dùng FF từ full giảm chạy trùng khi invariants đạt.

**Phương án đã xét:** chỉ so số CP (không chỉ bước); chỉ tiền tố (không giải thích sau proxy); thay prior ở khác chiều như cùng mô hình (không định nghĩa duy nhất); zero-padding hoặc thêm epsilon để đủ factorial (đổi phép tính và có thể tạo kết quả hiển nhiên); chạy surrogate rộng (thay nhiều thuộc tính); chọn D để báo hiệu quả (không có onset/end thật). Chọn native full + thiết kế hai yếu tố có giới hạn, giữ phần không tách được. Đã xét loại mọi range0/d0/input trùng/lỗi khỏi contrast: làm mất khác biệt xử lý hợp lệ hoặc biến không có khác biệt thành thiếu bằng chứng; thay bằng bốn trạng thái riêng, giữ output/lỗi native và mẫu số. Không chữa native để có effect. Không bắt mọi yếu tố phải tách độc lập mới cho phép báo căn cứ có điều kiện.

**Bằng chứng:** MRP P4, DT18-NV2/NV3, hướng dẫn cô §1, code detector ở revision đã chạy và nguồn đóng băng T-025/T-029. Chưa có kết quả task này; đây là kế hoạch kiểm, không xác nhận giả thuyết.

**Kết luận phụ thuộc:** căn cứ thành phần tiền xử lý/detector P6 và giới hạn đánh giá; mask/d/prior chưa tách, nhánh prefix/full đều còn nhìn trước, onset thật chưa biết. Các quy tắc native, factorial, ngưỡng cố định từ [:i_proxy] và chỉ số CP/m/delay là lựa chọn chẩn đoán khai trước; không có ngưỡng Late hoặc surrogate chọn từ accuracy. Cơ chế tính toán không tự xác nhận thay đổi vật lý, nền sạch hoặc ưu thế causal detector; thành phần hiệu chỉnh còn OPEN nếu chưa phân xử. Chỉ nối mục này vào docs/WHY.md khi Minh duyệt thực hiện đúng nội dung.

## Prompt bàn giao

Prompt kiểm bản sửa được trình trong chat cùng lượt sửa nháp, theo nguyên văn Prompt chung + Kiểm lại phản hồi và sửa + G2 trong docs/review-prompt.md. Codex là người làm cả T-032/T-033; Claude là người phản biện cả hai. Chưa có quyền ghi LOG hoặc bản REVIEW trong lượt này; Claude chỉ đọc và trả lời trong chat. Các lượt sau ghi prompt vào nơi được Minh cho phép, giữ lịch sử.
