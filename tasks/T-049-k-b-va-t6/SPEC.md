# T-049 — K-b và T6 trên nền z+S1

- **Trạng thái:** đã được Minh duyệt soạn và sử dụng ngày 03/11/2026 (Q-238); chưa triển khai thực nghiệm.
- **Người làm:** Codex.
- **Người phản biện:** Claude. Chưa có lượt soát SPEC này của Claude; không coi tự rà của người làm là phản biện chính thức.
- **Thuộc gói MRP:** P6, chuẩn bị P7 — **Cổng:** G3 chưa mở.
- **Nguồn quyền:** Minh: “hoàn tất nghiệm thu/ghi nhận quyết định và soạn–duyệt SPEC T-049 luôn”. Q-236 nghiệm thu T-048/T-053; Q-237 chốt D24 và nền; Q-238 duyệt phạm vi task này. Quyền chạy dài/chi phí theo mục Chi phí, không mượn trần task trước.

## Mục tiêu

Chọn biến thể gán bằng chứng khoảng ngoài span (E2-C hay E2-VC) và kiểm kênh tần suất trace E3b trên nền dev hiện hành, theo thứ tự K-b → T6 đã khai trước. Đồng thời đưa sửa phục hồi số học z đã kiểm ở T-053 vào code dùng chung, bảo toàn đường tính thông thường và hợp đồng điểm/khóa.

Nguồn trực tiếp: docs/MRP.md §2.3, P6/P7, RQ3; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md §2 đoạn 2–3; docs/reference/sources/advisor-2026-09-23.md §1 bước nghiên cứu 2–4; tasks/T-043-thiet-ke-rca-m1/SPEC.md B1–B4 (bước 9), Phụ lục C; docs/KE-HOACH-SAU-T047.md mục T-049 và cập nhật sau T-053; WHY-70–72.

Đây là cài đặt và lựa chọn thiết kế trên dev, kèm phân tích cơ chế ở mức dữ liệu đã ghi. Chưa phải kiểm hiệu quả độc lập, hoàn thành RQ3, hiệu chuẩn phát hiện hoặc xác nhận lợi ích do cấu trúc phụ thuộc thật. Không dùng kết quả chọn để tự biện minh ngưỡng C-e hoặc coi đồ thị đã đáp ứng toàn bộ mục tiêu DT18.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Giải thích cần phân xử | Phép kiểm và bằng chứng | Kết cục và phần còn thiếu |
|---|---|---|---|
| Phục hồi số học có giữ phương pháp đã chọn? | Trung gian tràn dù điểm cuối còn biểu diễn được; hoặc điểm/khóa thật sự ngoài miền | Đối chiếu native, ứng viên T-053 và bản tích hợp trên fixture biên; kiểm ordinary path, cờ, điểm, khóa, tầng và lỗi; kiểm T1 chịu ảnh hưởng | Chỉ cho dùng lại bản ghi khi có chuỗi hash và tương đương. Đổi chính sách số học hoặc hành vi ngoài quyền thì dừng phần phụ thuộc, trình Minh |
| C/VC khác nhau ở bước nào và có giúp trên nền thắng? | VC định danh thật; không có đỉnh định danh; hoặc chỉ rơi về C do quá 25 đỉnh | Theo ca/thế giới: cạnh có cờ → đồ thị phủ đỉnh → tập định danh → kênh được gán và điểm max → E5/FI → khóa/tầng/hạng; so ca tốt và xấu | Chỉ thay C bằng VC khi cặp ở nền thắng cho GIÚP theo bước 9. Nhánh đầy đủ chỉ báo kèm. Không gọi phần lớn dự phòng là VC vô tác dụng |
| E3b cung cấp thông tin hay đổi tương quan giữa nhóm kênh? | Tần suất thay đổi có ích; nhiễu, thiếu thu; khác thang PV/đếm hoặc tác động qua E5/khóa | Thao tác và n_N/n_A → kênh tần suất lên/xuống → hỗ trợ/cổng → F_raw → lớp lan/kế thừa → FI → max/m/count/sum → thứ hạng. Đối chiếu sai/đúng cùng điều kiện | Luật C theo T6 và ba thế giới. Không đủ tương phản thì giữ OPEN, chỉ rõ trung gian thiếu và bước nghiên cứu phụ thuộc; không chọn cách chuẩn hóa mới từ nhãn |
| Bằng chứng đủ cho lựa chọn hay cho cơ chế? | Cải thiện gộp nhưng hại dataset/ô; phụ thuộc quan sát, bối cảnh hoặc dung sai N1 | ΔRR theo ca/ô/dataset, cặp đối chứng và vế riêng; replay có kiểm khớp native; độ nhạy và độ bền theo ô | Tách số quan sát, kết cục luật, hành động tự động và quyết định Minh. Tương tác VC × E5 chưa được ma trận này phân xử đầy đủ; bàn giao cho gói sau, không suy cơ chế vật lý |

## Đầu vào và nền khóa

1. Nguồn quản trị: AGENTS.md; STATE, MRP, DECISIONS, WHY, LESSONS, review-prompt; nguồn đề tài ở trên. Hồ sơ khởi tạo và hash tại results/T-049/manifest-khoi-tao.json. Ba nguồn quản trị trước cập nhật Q-236–238 lưu nguyên byte tại results/T-049/nguon-truoc-ghi-quyet-dinh/; dùng các bản này để đối chiếu hash cũ trong manifest T-048/T-053. Không sửa manifest cũ nhằm làm như quyết định mới đã tồn tại khi chạy.
2. Nguồn giao thức: results/T-043/manifest.json, ma-tran-thu.json và ks16/dem-khong-nhan.json; các đính chính đã áp tại T-044/T-045; T0/KS-16 và tập E_X đã ghim. Kiểm hash đúng manifest trước khi dùng, không định nghĩa lại ô kích hoạt sau khi nhìn điểm K-b/T6.
3. Kết quả trước: results/T-047/manifest.json và scripts/luat_c_t047.py (chỉ đọc); results/T-048/manifest.json, t4.json, t4b.json, luat-c.json; results/T-053/manifest.json, runs/k-dong-pha1-001/seal.json, runs/k-cham-001/, runs/bootstrap-ec2-001/do-ben.json và runs/dap-phan-bien-001/kiem-tra.json. T-048/T-053 đã nghiệm thu theo Q-236 nhưng báo cáo/manifest giữ trạng thái lịch sử trước nghiệm thu. Không chạy lại vì câu trạng thái cũ.
4. Code hiện hành: src/m1/ và src/m1_danh_gia/; candidate số học results/T-053/scripts/z_on_dinh.py và fixture T-053; tests hiện có ở results/T-044/tests/ và các phép hồi quy T-047/T-048/T-053. Khóa hash mọi code đầu vào trước sửa, lưu diff và revision thực chạy.
5. Chỉ 52 ca dev: 30 RE2-TT, 22 Nezha-OB, cùng 23 ô đã ghim; 30 cửa sổ giả RE2-TT theo giao thức cũ. Chế độ (a): N/A 300 giây, chỉ adapter được đọc mốc thời gian; nhãn root/loại lỗi/ô không đi vào phương pháp. Dữ liệu và allowlist theo data/README.md, manifest T-022/T-026/T-043 và bản ghim T-053. Không đọc data/locked/, test, RE3-OB hoặc repo RCA lưu trữ.
6. **Nền Q-237:** z+S1, epsilon=0,05; alpha=0,01; cổng G3/D1 (mã cấu hình cổng, không phải quyền mở cổng nghiên cứu G3); E1=U, E2=C, E3(a)=False, E3b=False, E5=True, E6=a, E9=False, T12=False; cạnh quan sát. Áp S1 theo hợp đồng E6a ở cả P/S_lo/S_hi. Ghi rõ cả tham số nhanh_z và chế độ thang/khóa; không chỉ đặt tên cấu hình có chữ z.
7. Nút là service/owner đã chuẩn hóa; cạnh gọi từ span cha–con. Metric/log gắn vào nút; thời gian thao tác vào owner; khoảng ngoài span nằm trên cạnh và được E2 gán; E1 dùng cấu trúc span tạo thời gian độc quyền; E3b tạo kênh tần suất theo thao tác; E5 dùng quan hệ và lớp kênh để tách bằng chứng; E6a dùng khóa cục bộ, chưa lan truyền điểm. Chỉ dùng cạnh quan sát, không đổi schema/nút hoặc thêm cạnh tĩnh.

## Đầu ra và phạm vi ghi

- results/T-049/: scripts/, tests/, runs/ (giữ mọi lượt kể cả hỏng), hash đầu vào, snapshot/diff code, hồ sơ môi trường/tài nguyên/pilot/chi phí, cấu hình thực chạy, bản ghi pha 1, seal, số chấm/luật, dấu vết theo ca và kênh, độ nhạy/độ bền, báo cáo và manifest cuối. Tên kết quả chính: bao-cao.md, ma-tran.json, tai-su-dung.json, k-b.json, t6.json, co-che.json, do-ben.json, so-lan-nhin.jsonl, manifest.json. Trỏ số bằng đường dẫn và con trỏ JSON.
- **Chỉ một file code dùng chung được sửa:** src/m1/e4.py, để tích hợp phục hồi trung gian số học tương đương candidate T-053. Không đổi công thức, cờ, thang kênh đếm, khóa S1 hoặc hành vi khi điểm/khóa thật sự ngoài miền. Tests mới ở results/T-049/tests/; không sửa tests lịch sử để làm chúng đạt.
- LOG.md của task này chỉ ghi thêm; chỉ dòng T-049 trong docs/STATE.md khi triển khai. SPEC này khóa sau khi ghi theo Q-238; sửa thiết kế/phạm vi phải trình Minh.
- Không có quyền thường xuyên sửa DECISIONS/WHY/kế hoạch hoặc LOG task khác trong lúc chạy T-049. Gói ghi sổ và đóng task ở lượt khởi tạo được Q-238 cho phép riêng. Claude chỉ phản biện theo quyền của lượt Minh chuyển; Codex không viết REVIEW thay Claude.

## Thứ tự và ma trận

### 0. Tự rà, số học và công cụ trước thực nghiệm

- Đọc nguồn/code trực tiếp, kiểm hash; ghi tự tìm được vào LOG trước kết luận review. Đo tài nguyên và dựng ma trận JSON đầy đủ cờ, không dựa các default ngầm của runner.
- Tích hợp candidate z: giữ native trên đường thông thường; chỉ phục hồi trung gian tràn trên mẫu hữu hạn theo đúng nội suy tứ phân vị và thang đã dùng. Không clip, không thay vô cực bằng hằng số, không cứu riêng một hướng. Khi điểm cuối hay tổng khóa thật sự ngoài miền, giữ hợp đồng hiện hành và ghi đúng lỗi; không biến lỗi thành NO_EVIDENCE hay cấu hình hợp lệ.
- Kiểm fixture T-053 (IQR/median/hiệu tràn, điểm cuối biểu diễn được/không được, IQR sát ngưỡng, dấu, thiếu/không hữu hạn, khóa tổng tràn); đối chiếu ordinary path và native bitwise ở các trường được hợp đồng yêu cầu. Chạy hồi quy E4, chuỗi, runner và luật chịu ảnh hưởng. Không yêu cầu bất biến khi tùy ý đổi chung giá trị kênh đếm; kiểm quy ước đơn vị của adapter FlashTicket thuộc bước tích hợp sau.
- Lập bảng trường phụ thuộc của T1. Bản T1 T-053 chỉ tái sử dụng nếu hash, code tương đương, đầu vào và trường cần kiểm đều đủ. Phần không chứng minh được phải chạy lại đúng phạm vi chịu ảnh hưởng. Cờ/hợp lệ/U/FI/tầng lệch thì chặn kết luận đổi điểm thuần túy và mọi bước phụ thuộc, không bỏ qua vì điểm cuối khớp.
- Helper riêng T-049 nhận buoc rõ ràng: K-b dùng khoi_K để kết hợp thế giới theo bước 9; T6 dùng luat_C. Giữ Fraction, δ=0,01, δ_d=1/n_d với n_d gốc 30/22, UV-6 theo đúng thành phần, điều kiện E5 chỉ khi cặp xét E5, vế C-e N1 của WHY-70 với h=1. Độ nhạy h=0,5/2, δ=0,005/0,02 chỉ báo kèm; không chọn lại ngưỡng. E3b không bị tự gán UV-6 của E3(a).
- Sửa F1 ở bản công cụ mới: kết quả cần trình Minh phải có hành động/tình trạng rõ; không để trường mặc định rỗng làm mất nhánh TRÁI_CHIỀU_O hoặc TRÁI_CHIỀU_DATASET. Không sửa helper/bản kết quả T-047. Hồi quy kiểm kết cục và hành động cho K-b với GIÚP/HẠI/GIÚP, GIÚP kèm C-e chưa kiểm được và TRÁI CHIỀU tại P. Kiểm phân biệt hai chế độ, biên dấu >, cờ phụ thuộc quan sát, cặp thiếu/sai trạng thái và mẫu số C-e=0.
- Lấy E_X từ results/T-043/ks16/dem-sau-ghep-nhan.json#/o_kich_hoat: cả hai cặp C→VC dùng E2-VC, T6 dùng E3b. Lưu tập ô và hash trước khi chấm. Báo trạng thái thực thi VC theo ca/thế giới, tách khỏi ô kích hoạt đã ghim; tổng hợp theo trong/ngoài E_X. Nếu nguồn không đủ để xác định duy nhất thì giữ OPEN, trình đúng phần thiếu; không tự dùng tất cả 23 ô thay thế.

### 1. K-b — thay riêng biến thể theo bước 9

Kiểm điều kiện E1-CP từ KS-16: số cha có con chồng lấn / số cha có ít nhất hai con không suy biến, dung sai hơn 1 ms. Nguồn hiện có: RE2-TT 0/494815; Nezha-OB 444/277534, đều dưới 5%; không chạy E1-CP. Xác nhận định nghĩa/miền còn giống trước khi dùng lại. Đầu vào hoặc điều kiện khác thì trình phần phát sinh, không lén thêm CP.

| Vế | E1 | E2 | E3(a) | E5 | Vai trò |
|---|---|---|---|---|---|
| K-thang-C | U | C | tắt | bật | Nền Q-237; tái sử dụng có kiểm |
| K-thang-VC | U | VC | tắt | bật | Phép chọn chính, chỉ thay E2 |
| K-day-du-C | U | C | bật | bật | Nền đầy đủ của khối K, tái sử dụng có kiểm |
| K-day-du-VC | U | VC | bật | bật | Báo kèm theo bước 9; không lấy nhánh này để chọn VC |

Mọi hàng giữ E3b tắt và các cờ nền khác. Giữ cả nhánh đầy đủ dù E3(a) không được chọn trong K. Theo mỗi ca/thế giới lưu số đỉnh/cạnh thực sự vào VC, danh sách phủ tối thiểu/đỉnh định danh hoặc dấu vết tương đương đủ tái kiểm, cạnh gán và kênh điểm. Phân biệt: có định danh; không có đỉnh định danh (kể cả đồ thị rỗng, ghi riêng nguyên do); dự phòng về C khi số đỉnh vượt 25. Không suy từ tên cấu hình rằng VC đã được thực thi hữu ích.

Chỉ tự thay C bằng VC khi cặp chính cho GIÚP tại P, không phụ thuộc quan sát, vế C-e kiểm được và các điều kiện hợp lệ đều đạt. Các kết cục còn lại giữ C và ghi đúng kết cục/cờ. Nếu có TRÁI CHIỀU theo ô hoặc dataset, phụ thuộc quan sát, hoặc GIÚP kèm C-e chưa kiểm được, ghi OPEN và trình Minh trước khi dùng nền T6. Lỗi đầu vào hoặc thiếu bản ghi bắt buộc thì dừng phần phụ thuộc. K-b này giữ E5 bật, không đủ bốn ô VC/C × E5 bật/tắt; không kết luận toàn bộ tác động VC/E5. Chỉ chạy cấu hình ghép CP+VC nếu sau này Minh duyệt phạm vi có CP và giao thức yêu cầu, không ghép ứng viên chưa chạy.

### 2. T6 — E3b sau nền K-b hợp lệ

- Nền tắt E3b là nền thắng sau K-b. Thêm đúng một cấu hình E3b bật; mọi cờ khác cố định. Không dùng kết quả ở nền C để chọn E3b nếu nền đã đổi sang VC.
- Chạy 52 cửa sổ thật và 30 mốc giả, đủ P/S_lo/S_hi; thu cả kênh tần suất lên/xuống, hỗ trợ, mẫu N/A, p/alpha, điểm, F_raw, lớp lan_nguoc/lan_xuoi và bước E5/FI, khóa và hạng. Không đổi điểm đếm sang z hoặc chọn lại quy tắc ghép nhóm.
- Trước ghép nhãn: lưu định nghĩa nhóm PV/đếm, bão hòa, chuyển loại max theo cả hai hướng, kênh quyết định, ô kích hoạt và phép replay. Khóa phase 1 từng bước bằng hash; chỉ sau đó bộ đánh giá mới ghép nhãn. T6 phụ thuộc lựa chọn K-b nên là một phase 1/seal mới; ghi rõ đã nhìn kết quả K-b.
- Quyết theo Phụ lục C: GIÚP giữ bật; HẠI bỏ; KHÔNG ĐỦ CA và phụ thuộc quan sát xử lý đúng mặc định của T6 là giữ bật, ghi chưa phân xử và báo riêng P, S_lo, S_hi cùng hành động giữ bật khi phụ thuộc quan sát; KHÔNG TÁC DỤNG đề xuất bỏ theo điều kiện của luật. TRÁI CHIỀU theo ô/dataset trình Minh, chưa đổi nền chính thức; chỉ tiếp tục phần độc lập trên nền đã duyệt. Không áp mặc định của K-b sang T6. Không để lịch chạy tự chốt quyết định còn OPEN.

### 3. Chấm, cơ chế, độ bền và bàn giao

- Pha 2 dùng cùng U/tập ứng viên, tie-aware RR, mẫu số và cách tính đã ghim. ERROR/UNSUPPORTED phải báo và xử lý theo giao thức, không đổi thành điểm 0 hay loại ca theo kết quả. Báo theo ca, ô, dataset, ba thế giới: MRR, NDCG@5, Hit@1/3/5, Retrieval@5 (= Hit@5), Rerank@1 (ΣHit@1 / ΣHit@5, ghi không xác định nếu mẫu số bằng 0), AC@k, Avg@5, M5 khi có nghĩa; C-e báo N1/V0 và mẫu số. E_X, phụ thuộc quan sát, trạng thái hỗ trợ và vế hại phải truy vết được.
- Cặp K-b/T6 áp cùng helper ở điểm chính, độ nhạy, bootstrap 1000 mẫu theo ô (seed 20261102) và bỏ từng ô; không chọn seed theo kết quả. Báo không đủ ca/không xác định rõ, không ép chọn ở mẫu không hợp lệ. Thống kê bootstrap mô tả độ bền trên dev, không coi là kiểm định lợi ích độc lập.
- Đọc trung gian và replay các ca RR/nhóm hạng thay đổi; so ca sai với đúng có điều kiện tương ứng, kiểm cả cổng và E5 thay vì chỉ max. Với VC phải tính lại phép gộp max từ tất cả cạnh phủ ở đỉnh định danh; không thay riêng một cạnh rồi coi là đầu ra VC. Dùng dev-f36d0647d5, dev-a915aa2424 và ca đối chứng dev-a5cabe5fa7 để lần theo gán cạnh → E5/FI → khóa. Với T6, lần theo thực thể vào/ra tầng 1 ở các cửa sổ giả đổi N1, lý do cờ E3b và FI. Replay dùng để chẩn đoán, không thay điểm native chính. Khớp cả hạng/tie group và các phần khóa, ghi sai số được phép có lý do.
- Báo cáo tách lỗi cài đặt, thiếu đầu vào/coverage, hạn chế giao thức và giả định phương pháp. Chỉ quy cơ chế khi chỉ được đầu vào → bước xử lý → trung gian → đầu ra; nếu nhiều giải thích cùng phù hợp, ghi phạm vi chưa phân xử và bằng chứng cần thêm. Không gọi trôi nền/ngoại lai/thiếu quan sát là nguyên nhân vật lý đã xác nhận.
- Đóng manifest, kiểm toàn diff/hash/file set, nối LOG đủ lệnh tiếp nhận, cập nhật dòng T-049 thành chờ phản biện. Đề nghị Minh quyết nền cho T-050 nếu phát sinh cờ chưa được quyết, nêu rõ khi T6 phụ thuộc quan sát mà P là HẠI hoặc TRÁI CHIỀU; không tự nghiệm thu task hoặc mở G3.

## Tái sử dụng, điều phối và kiểm đúng đắn

- Trước tái sử dụng, tai-su-dung.json phải đối chiếu hash nguồn/đầu ra, ma trận cờ, dữ liệu, U, miền cửa sổ, gate/score revision, worlds, lớp/FI/tier/key và trung gian đủ dùng. Phân biệt dùng lại điểm với dùng lại phân tích cơ chế. Source code đổi hợp lệ phải có diff và bằng chứng tương đương; không cập nhật hash cũ để che thay đổi.
- Pilot đối chiếu cùng ca/cấu hình trên laptop và EC2 (có RE2 nặng, Nezha có kênh đếm/OPEN; thứ tự và hash seed theo T1 nếu chịu ảnh hưởng), cache bật/tắt và cấu hình chạy riêng. Chọn cửa sổ có đồ thị cạnh có cờ thực sự đi qua nhánh giải VC và cửa sổ có E3b đủ hỗ trợ. Gộp một lượt đối chiếu xáo thứ tự đại diện cho mỗi nhánh có hoạt động vào pilot và tính lượt đó trong dự toán. Kiểm cờ, điểm, khóa, hạng, tier và trạng thái. Lệch thì dừng phần phụ thuộc và điều tra; không lấy trung bình hai máy.
- Dùng laptop và đúng instance cũ i-06c1d9173fb30932e đã được xác nhận ở T-053; kiểm lại ID, vùng, kiểu máy, quyền đọc dev, dung lượng và môi trường trước khi chạy. Không tạo/đổi instance, không copy dữ liệu khóa. Đường truy cập lấy từ cấu hình hiện có, không lưu khóa bí mật trong hồ sơ.
- Đo RAM/CPU/ổ trống và thông lượng thực tế theo dataset, tối đa hóa số tiến trình chạy ổn định bằng pilot. Không mặc định số worker T-053 vẫn tối ưu. Ưu tiên ca nặng trên EC2; chia các cửa sổ độc lập, giữ các vế so của cùng cửa sổ trên cùng máy. Nếu bản ghi cũ ở máy khác, phải có chứng minh tương đương hoặc chạy lại vế nền tại máy được gán. Ghi host cho từng vế và kiểm tự động điều kiện này.
- Chạy đồng thời các ca/cấu hình K-b độc lập và chuẩn bị công cụ phân tích. Không chạy T6 chọn chính trước khi K-b đã chốt nền theo quyền; không chạy task phụ thuộc sau khi cờ chưa quyết. Giữ mọi lượt hỏng, checkpoint và nguyên nhân dừng. Tái tiếp nhận từ manifest, không lặp lượt đã đủ và hợp lệ.

## Tiêu chí xong

1. Bản tích hợp số học và helper qua các phép kiểm chịu ảnh hưởng; có bảng T1/tái sử dụng, native ordinary không đổi, đúng hành vi điểm/khóa thật sự tràn. Không có lỗi tính toán bị che bằng cờ bằng chứng.
2. Ma trận K-b đúng hai cấu hình VC và hai nền đối ứng; CP được xác nhận không đủ điều kiện bằng nguồn hash hợp lệ. Đủ 52+30 cửa sổ, worlds, dữ kiện định danh/dự phòng và kết cục chính/báo kèm; hoặc báo đúng phần bị chặn và bằng chứng cần thiết, không gọi bước ấy đã chạy xong.
3. T6 chạy trên nền sau K-b hợp lệ, đủ cặp chính và trung gian kênh tần suất. Quyết định/action tách đúng mặc định từng thành phần, cờ theo ô/dataset và phụ thuộc quan sát; không lặp F1.
4. Có phân tích cả ca được sửa và hỏng cùng điều kiện; replay được kiểm native. Báo phần đã phân xử, phần chưa phân xử, dữ liệu còn thiếu và quyết định bị ảnh hưởng, không chỉ khớp số.
5. Số quan sát, kết cục luật và quyết định Minh tách rõ; không vượt giới hạn tương tác VC/E5, mixed PV/đếm, N1 chưa hiệu chuẩn, dữ liệu dev đã nhìn nhiều lần hoặc hiệu quả P7. Báo nền đề nghị bàn giao T-050 với mọi cờ còn OPEN.
6. Hash/seal/manifest/LOG/STATE và prompt trung tính đủ để agent khác tiếp nhận; không sửa kết quả/history task trước, không commit/push hoặc mở test/G3.

## Không làm

Không chạy lại K16 hoặc T4/T4b vì chúng đã có bằng chứng hợp lệ; nếu phát sinh điều kiện phải chạy lại, trình phạm vi và chi phí theo kế hoạch. Không đổi epsilon/alpha, công thức/thang đếm, luật C/h, tập ca/E_X/tập ứng viên, code dùng chung khác e4.py, ma trận hoặc dataset. Không chạy T9/T10/T11/T12/KB/T13, đầy đủ tương tác VC × E5, hiệu chuẩn verdict, chế độ (b), RE3-OB, test hay FlashTicket. Những phần này thuộc gói tiếp theo; thiếu chúng hạn chế quyết định G3/khẳng định lợi ích, không xóa nghĩa vụ nghiên cứu.

## Chi phí ước lượng và quyền chạy

- Lượt hiện tại chỉ ghi nhận quyết định và soạn SPEC/hồ sơ khởi tạo. Chưa chạy phương pháp, chưa phát sinh quyền dùng ngân sách cũ cho T-049.
- Ma trận hiện hành có tối đa 5 cấu hình khác nhau × 82 cửa sổ = 410 bản ghi cấu hình–cửa sổ, chưa tính pilot/kiểm T1/seed/replay. Nếu tái sử dụng hai nền C đúng điều kiện và nền T6 đã có, chỉ 3 cấu hình mới × 82 = 246 bản ghi phương pháp. Ba thế giới phải đủ nhưng cách lưu không mặc nhiên là ba lần chạy trích đặc trưng.
- Tham chiếu thực đo T-053: K16 mất 5935,950 giây thời gian thực với laptop 3 worker và EC2 2 worker. Nhân tỷ lệ cấu hình chỉ cho mốc thô khoảng 0,31–0,52 giờ cho 3–5 cấu hình, chưa tính chi phí VC/tần suất, kiểm code, I/O, replay và bootstrap. VC có độ phức tạp lớn theo đồ thị đến 25 đỉnh, nên không dùng mốc thô làm cam kết thời điểm hoàn tất.
- **Dự toán chưa đo riêng:** 1–3 giờ máy cho phần thực nghiệm/hậu xử lý sau chuẩn bị; có thể vượt khi VC khó hoặc phải chạy lại T1. Phần sửa và kiểm công cụ khoảng 1–2 giờ làm việc, cần checkpoint nếu không vừa một phiên. Tách phần phát sinh cần thiết thành task mới khi phải đổi thiết kế, không kiểm nhẹ đi để vừa giờ.
- Trước lượt dài hơn 1 giờ: đo pilot, ghi phân bổ ca/worker, RAM/CPU/ổ trống/thông lượng, thời gian đã dùng, khoảng ETA, trần wall time và EC2, dung lượng phát sinh/chuyển rồi báo Minh duyệt theo AGENTS mục 3.8. Chưa có trần/chi phí chạy dài T-049 được duyệt tại mốc tạo SPEC. Đơn giá 0,1197 USD/giờ chỉ là tham chiếu lịch sử của T-053, phải kiểm giá/loại máy hiện hành trước tính dự toán mới. So riêng chi phí một cấu hình–dataset với Q-40, không gọi thời gian tìm 16 cấu hình là benchmark phương pháp.
- Không tải dữ liệu mới quá 5 GB hoặc xóa/chuyển dữ liệu để lấy chỗ. Ổ thiếu dung lượng thì checkpoint và báo Minh phạm vi cần xử lý; giữ mọi lượt đã chạy.

## Rủi ro và điều chưa chắc

- Chưa kiểm E2-VC và E3b dưới nền z+S1+E5 hiện hành; candidate không phải bằng chứng đã giúp. Không có định danh hoặc phần lớn dự phòng có thể làm K-b ít khả năng phân xử; báo đúng tỷ lệ và giới hạn.
- E3b giữ điểm đếm E4, còn PV dùng z; mixed PV/đếm và ngoại lai có thể ảnh hưởng. Kết cục không tác dụng không đủ chứng minh thông tin tần suất vô ích. Cần chuỗi trung gian để xác định bước làm mất thông tin, giữ OPEN nếu chưa đủ tương phản.
- C-e N1 và h=1 chưa hiệu chuẩn; V0 ở mốc giả cũ cao. Không có kiểm định độc lập về phát hiện; không dùng đạt vế này để xác nhận an toàn báo động.
- Lựa chọn E1+E2+E5 có cờ trái chiều được Minh chấp nhận, độ bền bootstrap không tập trung vào một cấu hình; dữ liệu dev đã nhìn nhiều lượt. Không đổi nhãn khoa học vì quyết định hành động đã chốt.
- Tương tác VC/E5, lợi ích do cấu trúc thật, FlashTicket/đơn vị và chế độ (b)/RE3 còn OPEN theo nguồn. T-049 chỉ chuyển được các bằng chứng tương ứng cho bước sau, không tự hoàn thành chúng.

## Prompt bàn giao

Prompt soát SPEC nguyên mẫu ở LOG.md mục “Prompt chuyển Claude — soát SPEC T-049”. Prompt nghiệm thu T-048/T-053 nằm trong LOG đóng task tương ứng, dùng đúng khối công đoạn/cổng. Minh chọn gửi; không tự mở phiên hoặc gửi agent khác.
