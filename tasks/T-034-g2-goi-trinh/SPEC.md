# T-034 — Gói trình G2: baseline, bản đồ hạn chế có nguyên nhân, câu trả lời cho cô

- **Trạng thái:** Minh duyệt bản 3 ngày 13/10/2026 và giao Claude triển khai; sau đó duyệt sửa R1–R5, bước tự kiểm trước triển khai và đưa hai phép E1/E2 vào T-034 kèm điều phối tài nguyên. Bản đề xuất do Claude soạn ngày 09/10/2026; Codex ghi các bản sửa đã duyệt và tự kiểm. SPEC này đã khóa; không tự sửa khi triển khai. Khóa quyền sửa không miễn tự kiểm tính đúng của SPEC.
- **Người làm:** Claude.
- **Người phản biện kết quả:** Codex.
- **Thuộc gói MRP:** P3, P4 (tổng hợp và hai phép phân xử bổ sung trên dev) — **Cổng:** G2.
- **Điều kiện bắt đầu:** Minh đã đóng T-032 và T-033. Nếu một task chưa đóng thì dừng, ghi LOG, báo Minh; không dùng số chưa được chấp nhận.

**Nguồn duyệt ngày 13/10/2026 — nguyên lời Minh:** “DUYỆT. TẠO SPEC GIÚP TÔI, TRONG QUÁ TRÌNH TẠO KIỂM LẠI 1 LẦN NỮA, KHÔNG DÙNG SUBAGENT, SAU ĐÓ TẠO PROMPT YÊU CẦU CLAUDE TRIỂN KHAI TASK 34, SAU ĐÓ LIỆT KÊ CHO TÔI CÁC LƯU Ý VỀ TASK NÀY ĐỂ TRÁNH VIỆC CLAUDE LÀM XONG RỒI TÔI MỚI PHÁT HIỆN CÓ ĐIỀU GÌ ĐÓ VƯỢT TRÁI MONG MUỐN CỦA TÔI CŨNG NHƯ ẢNH HƯỞNG KẾT QUẢ BẢO VỆ ĐỒ ÁN”. Phạm vi duyệt là bản 2 cộng S7″, S14″, S15, S16 (bản 3), gồm phụ lục WHY-51. Việc duyệt và giao triển khai không nghiệm thu G2, chọn baseline mới hoặc chọn thành phần P5/P6.

**Nguồn duyệt bổ sung ngày 13/10/2026 — nguyên lời Minh:** “DUYỆT SỬA SPEC R1–R5, bước tự kiểm trước triển khai”. Phần sửa gồm: kiểm lại giới hạn theo nguồn mới nhất (R1), kiểm lập luận thay vì chỉ quét từ (R2), phân biệt chưa biết với kết quả âm (R3), gọi độ đo phát hiện đúng nhãn proxy (R4), dự toán và lựa chọn máy theo loại việc (R5), cùng tự kiểm SPEC trước khi thực hiện. Không mở rộng quyền chạy thực nghiệm mới hoặc chọn thiết kế P5/P6.

**Nguồn duyệt mở rộng ngày 13/10/2026 — nguyên lời Minh:** “vậy 2 phép kiểm này làm trong t34 luôn ? nếu vậy thì duyệt sửa spec, điều phối sử dụng tài nguyên phù hợp”. Hai phép E1 (quy tắc pattern TraceRCA) và E2 (BOCPD đầy đủ trong miền log) nay thuộc T-034, gồm thiết kế chi tiết trước chạy, kiểm đúng đắn, chạy, phân tích và tổng hợp. Quyền này thay các giới hạn cũ chỉ tổng hợp đối với đúng E1/E2; không chọn phương pháp P5/P6, thay baseline đã khóa hoặc mở test. Claude được điều phối laptop và hai EC2 hiện có theo mục tài nguyên; không dùng subagent.

## Mục tiêu

MRP §7 đặt G2 sau P3 và P4. Minh duyệt "bảng baseline trên dev, bản đồ hạn chế". PLAN-P3-G2 §8 yêu cầu tóm tắt ba câu:
- phương pháp nào tốt trong điều kiện nào;
- thất bại ở đâu;
- hạn chế nào cần P5/P6 giải quyết.

Hồ sơ vẫn phải trả lời đủ sáu câu của MRP §7.

Gói này là cầu nối logic mà cô yêu cầu: "chỉ ra vấn đề còn tồn đọng, hạn chế của các phương pháp đã có → tiếp cận phương pháp đồ thị". Theo MRP §2.1 và WHY-01, thành phần nhằm sửa hạn chế nối với bằng chứng P4; thành phần khác ghi đúng căn cứ DT18 hoặc nhu cầu kỹ thuật. Vì vậy gói phải cho biết với mỗi hạn chế:
- bằng chứng mạnh tới đâu;
- nguyên nhân đã tìm được hay chưa;
- nếu chưa, vì sao và câu đó sẽ được phân xử ở đâu.

Gói trả lời bảy câu:

- **K1 — Sáu câu của MRP §7** cho cổng G2.
- **K2 — Bảng baseline dev,** gồm phát hiện và xếp hạng, hai chế độ, hai dataset, trạng thái kiểm tái lập.
- **K3 — Bản đồ hạn chế hợp nhất.** Gộp HP-n (T-029), M-n (T-028), H1–H17 và D1–D7 trong `results/T-032/nguyen-nhan-xep-hang.md`; đối chiếu KT1–KT16 và K1–K7 tại `results/T-032/runs/bo-sung-toan-dien-20261012-001/closure-ledger.json#/questions`, cùng đính chính trong `closure-ledger-review-001.json` (dẫn ledger gốc qua `/source_ledger`). Mỗi dòng ghi trạng thái nguyên nhân và mức bằng chứng theo một thang chung.
- **K4 — Lan có đáng kể không (Q-86),** kèm nháp định nghĩa nhãn "lan" nếu đủ căn cứ; nếu chưa thì nêu bằng chứng còn thiếu và quyết định phụ thuộc. Minh quyết có khóa nhãn ở G3 không (MRP P4).
- **K5 — Căn cứ → ứng viên cho P5/P6.** Ứng viên nhằm sửa hạn chế P4 dẫn dòng G2-Hn tương ứng; ứng viên theo DT18 hoặc nhu cầu kỹ thuật dẫn căn cứ đúng loại. Mỗi ứng viên có dự đoán bác bỏ được trên dev. Đây là ứng viên, không phải lựa chọn; lựa chọn chốt ở spec P6 (MRP P6).
- **K6 — Câu còn mở và nơi phân xử:** tách câu còn kiểm được trên dev hiện có; câu thiếu quan sát hoặc nhãn độc lập; câu thuộc đánh giá sau khóa thiết kế. Nêu bằng chứng cần thêm, bước xử lý và quyết định phụ thuộc; không dùng test để hoàn tất lựa chọn thiết kế.
- **K7 — Hỏi–đáp cho cô:** các câu cô có thể hỏi về P3/P4, câu trả lời ngắn, mức bằng chứng và nguồn.

## Đầu vào (chỉ đọc)

- **Baseline:**
  - `results/T-024/cham-a.json`, `cham-a.md`;
  - `results/T-025/phat-hien.json`, `cham-b.json`, `cham-b.md`;
  - `results/T-026/cham-a.json`, `cham-a.md`.
- **Kiểm tái lập và kiểm đúng đắn:**
  - `results/T-006/kiem-dung-dan.md`, `results/T-007/kiem-dung-dan.md`;
  - đoạn so với số công bố trong `results/T-024/cham-a.md` (mục đối chiếu README RCAEval) và `results/T-026/cham-a.md`;
  - hồ sơ P1 `results/T-013`–`T-017`.
- **Hạn chế:**
  - `results/T-028/ban-do-han-che-xep-hang.md`, `codebook.md`, `runs/phan-hoi-review-001/summary-tables.json`, `ca-sai.json`;
  - `results/T-029/ban-do-han-che-phat-hien.md`, `dinh-vi.md`, `a-so-b.md`, `nhan-proxy-va-schema.md`, JSON tương ứng;
  - `results/T-032/` và `results/T-033/` (toàn bộ đầu ra sau khi Minh đóng task).
  - **Thứ tự đọc bắt buộc cho phần diễn giải hiện tại:** `results/T-032/runs/bo-sung-toan-dien-20261012-001/doi-chieu-dien-giai-review-001.md` → `bo-sung-bao-cao-review-001.md` → `BAO-CAO-TONG-HOP.md` trong cùng thư mục → `results/T-033/runs/bo-sung-toan-dien-20261012-001/t33/report-final-004.md`, rồi mới dùng các báo cáo cũ. Câu cũ đã có trong bảng đối chiếu phải dùng trạng thái đính chính; giữ nguồn cũ để truy lịch sử. Đọc `closure-ledger.json` cùng `closure-ledger-review-001.json`, kiểm bằng `manifest-final.json` và `manifest-review-001.json` phù hợp.
- **Khung:**
  - `docs/MRP.md` §2, §3, §5 (P4–P7, P9, P10), §6, §7;
  - `docs/PLAN-P3-G2.md` §8;
  - `docs/WHY.md` (WHY-01 và WHY-22–50, gồm các phần nối ngày 13/10), `docs/DECISIONS.md`, `docs/LESSONS.md`;
  - `docs/reference/sources/DT18-de-tai-va-nhiem-vu.md`, `docs/reference/sources/advisor-2026-09-23.md`;
  - chuẩn quan sát FlashTicket `D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md` (chỉ đọc).
- **Hai phép bổ sung:** code và trung gian TraceRCA của T-032 (gồm `scripts/tracerca_original_ranking_v1.py`, bản tác giả đã ghim trong gói bổ sung, `cases.json`, Full008 và `closure-ledger-review-001.json#/h6_pair_audit`, `/pattern_candidate`); code BOCPD đã ghim, `zero-lineage-summary-001.json`, `engine-final-summary-001.json`, source catalog và các NPZ được chúng dẫn tới của T-033. Chỉ đọc đúng ca dev được phép ở E1/E2; khi thiếu trung gian được tái tạo từ đầu vào dev và cấu hình đã ghim trong phạm vi hai phép này. Bản nguồn, môi trường cũ và kết quả cũ giữ nguyên; bản instrument/code sửa nằm dưới T-034. Kiểm manifest phù hợp trước dùng.

## Thiết kế — khóa trước khi viết

### Thang mức bằng chứng chung

Mỗi dòng bản đồ ghi đúng một mức cao nhất mà bằng chứng **thực sự** đạt, kèm mức của từng nguồn con. Mức cao hơn không được suy từ nhiều mức thấp cộng lại.

| Mức | Nghĩa | Ví dụ nguồn |
|---|---|---|
| CT — can thiệp | Đổi đầu vào hay tham số có kiểm soát, quan sát đầu ra của chính phương pháp | I1, I2, I3 (T-029); thử giả (T-032); chuỗi thay thế (T-033) |
| ĐC — đo cơ chế | Đo trực tiếp đại lượng mà cơ chế giả định, không suy từ thứ hạng | phân rã độ trễ theo cây lời gọi (T-032) |
| LĐ — liên hệ có đối chứng | Cờ hay đặc trưng đặt cạnh tỉ lệ ở điểm đối chứng | V7 (T-029); tải và log lỗi (T-033); P0 (T-028) |
| MT — mô tả | Đếm, phân bố, đọc tay không có đối chứng | M0, schema, định vị |
| CK — chưa kiểm | Kèm lý do không kiểm được trong task và nơi sẽ kiểm | D, onset, nền sạch, tác động chung qua hạ tầng |

### Quy tắc hợp nhất

- **Mã mới G2-Hn.** Mỗi dòng trỏ về các mã gốc liên quan: HP-n, M-n, H1–H17, D1–D7; câu hỏi KT1–KT16 của T-032 và K1–K7 của T-033 tại `closure-ledger.json#/questions`. Dùng đính chính trong `closure-ledger-review-001.json`, có `/source_ledger` dẫn về ledger gốc. Ghi đầy đủ task nguồn để không nhầm K1–K7 của T-033 với K1–K7 của gói T-034; mọi số có con trỏ JSON nguồn.
- **Không đổi số hay nhãn của task gốc.** Khi hai task cho kết luận khác nhau về cùng hiện tượng, ghi cả hai và nêu lý do có thể. Không chọn bên nào nếu bằng chứng không phân xử.
- **Mỗi dòng ghi:**
  - phương pháp; dataset; chế độ;
  - số ca/tổng theo ô;
  - hiện tượng;
  - nguyên nhân đã xác lập (nếu có), kèm mức;
  - giải thích khác còn lại;
  - tác giả có nêu không (dẫn nguồn hoặc "chưa thấy trong nguồn đã khảo sát");
  - ảnh hưởng tới RQ nào.
- **Phân biệt ba trạng thái** của câu "vì sao":
  - "đã xác lập ở mức X";
  - "đã loại được giải thích Y";
  - "chưa phân xử, vì Z".

  Không viết "nguyên nhân là…" khi mức chỉ là LĐ hoặc MT.

### Bảng baseline (K2)

- Bảng baseline chính chỉ đọc số đã có, không chạy lại để thay bảng. E1/E2 là chẩn đoán bổ sung, báo riêng; không tự thay số, cấu hình hoặc cách chấm baseline.
- **Xếp hạng chế độ (a):** RE2-TT dev30 và Nezha-OB main. Hit@1/3/5, MRR, NDCG@5, AC@k và Avg@5, Retrieval@K và Rerank@1 (Q-65). Khoảng bootstrap theo ô đã có. Trạng thái non-OK giữ trong mẫu số. CIRCA báo riêng cohort Q-82.
- **Phát hiện:** P, R, F1 theo cửa sổ và số báo động sai mỗi giờ bình thường theo giao thức/nhãn proxy của T-025; độ trễ tính từ mốc tiêm trong giao thức. Ghi rõ nhãn proxy không xác nhận độc lập khoảng khỏe, onset hoặc thời điểm hết lỗi; không gọi các số này là chất lượng báo động sai trong vận hành thực hay độ trễ từ onset vật lý. Cạnh đó là bảng độ nhạy D (T-033). Giữ nguyên số và cách chấm đã khóa.
- **Chế độ (b):** RCA tại báo động đầu (T-025) và bảng G (T-029).
- **Trạng thái kiểm tái lập** theo từng phương pháp: "đã tái lập số công bố", "chỉ so tham khảo", "chưa có số công bố", kèm nguồn. Phương pháp chưa tái lập được ghi rõ, không gọi "khớp".
- **Câu "phương pháp nào tốt trong điều kiện nào"** chỉ dựa trên số tách theo ô và theo ca, không dựa trên trung bình chung (SL14, QT15).
- **Nhánh chẩn đoán báo riêng:** TraceRCA mã tác giả được đầu vào hỗ trợ (latency-only), cả hai ngưỡng chọn đặc trưng 1 và 3; ghi đơn vị, hợp đồng đầu vào, trạng thái thiếu bằng chứng và quy tắc hòa của từng cấu hình. Ghi rõ "chẩn đoán trên dev, chưa là baseline"; không gọi là tái lập đầy đủ bài/default hoặc gộp vào bảng chính. Dòng MicroRank với bộ chia theo bài gốc cũng báo riêng, ghi rõ quy ước dựng đầu vào và phạm vi so sánh. Các số lấy từ đầu ra đã lưu, không chọn cấu hình theo điểm đẹp.

### Lan (K4)

- Tổng hợp bằng chứng chờ theo từng phương pháp tại mục 5 báo cáo T-032, các bảng theo ca và KT10 trong ledger bổ sung, cùng đính chính có liên quan. Báo riêng khả năng đo: 16 ca Nezha-OB đo được có điều kiện, 21 ca RE2-TT đo được một phần, 15 ca không đo được; kiểm lại số và điều kiện từ nguồn trước dùng. Đây là khả năng quan sát chờ trên 52 ca, không phải nhãn lan, tỷ lệ lan hoặc tỷ lệ nguyên nhân thất bại.
- Trả lời đúng mức bằng chứng: điều gì hỗ trợ, bác bỏ hoặc chưa phân xử câu "lan có đáng kể". Không thay bằng M5, P0 hoặc cộng các cờ chồng lấn. Nếu chưa đủ để nói "đáng kể", ghi đúng như vậy cùng phần thiếu và quyết định phụ thuộc.
- **Nháp định nghĩa nhãn lan là đầu ra có điều kiện.** Nếu đủ căn cứ đã có, nháp phải nêu ngưỡng từ dữ liệu bình thường, độ nhạy có nguồn, tránh định nghĩa vòng lặp và các ca không áp dụng được. Nếu chưa đủ, ghi "chưa đề xuất định nghĩa", nêu bằng chứng hoặc phép kiểm còn thiếu và quyết định phụ thuộc; không tự điền ngưỡng hay độ nhạy chưa được đo. E1/E2 không đo lan vật lý hoặc tạo nhãn lan. Minh quyết có định nghĩa và khóa nhãn ở G3 không.

### Ứng viên P5/P6 (K5)

- Mỗi ứng viên ghi:
  - mục đích: sửa hạn chế P4, đáp ứng DT18, hoặc nhu cầu kỹ thuật; căn cứ đúng loại, dẫn G2-Hn chỉ khi nhằm sửa hạn chế;
  - mức bằng chứng thật và giải thích khác còn lại;
  - cơ chế dự kiến;
  - tín hiệu sử dụng; với cơ chế đồ thị, nêu nút, cạnh, nơi ánh xạ log/trace/metric và phép tính thực sự dùng cạnh theo AGENTS mục 3.18;
  - **dự đoán và điều kiện bác bỏ trên dev**, khai trước khi P6 thử;
  - rủi ro;
  - tầng của khung bốn tầng (MRP P6) — chỉ khi phù hợp, không bắt buộc khung.
- Ghi mức căn cứ đang đạt theo MRP §3: đủ để đề xuất thử cần hiện tượng trên file thật, lý do kỹ thuật khả thi, giải thích khác và dự đoán có thể bác bỏ; thành phần theo DT18 hoặc nhu cầu kỹ thuật phải dẫn đúng yêu cầu/lý do. Nêu phần còn thiếu để chọn thiết kế và để khẳng định hiệu quả. CT/ĐC không tự đủ để chọn thiết kế; LĐ/MT không tự loại một ứng viên có đủ căn cứ đề xuất. Task này chỉ trình ứng viên, không chốt lựa chọn.
- Ứng viên giữ hướng cạnh dùng trạng thái đã đính chính của H6/WHY-47, không dùng suy rộng cũ. Các ứng viên quy tắc pattern, dùng tín hiệu giảm và log tại root ở return ghi đúng mức bằng chứng, giải thích cạnh tranh và phép phân xử còn thiếu. Không biến quan sát hoặc chênh giữa hai pipeline thành nguyên nhân riêng đã xác nhận.
- Không chọn ứng viên, không xếp hạng ứng viên theo kỳ vọng thắng (QT4). Không viết đồ thị sẽ giúp; viết điều kiện để biết nó có giúp hay không.

### Câu còn mở và nơi phân xử (K6)

Tách ba nhóm, không coi "chưa làm" là "dữ liệu không thể phân xử":

1. **Còn kiểm được trên dev hiện có:** ghi phép phân xử, yếu tố cần giữ/đổi, đầu vào hoặc trung gian cần dùng, chi phí đã biết hoặc "chưa đo", người xử lý và quyết định phụ thuộc. E1/E2 đã được giao thực hiện trong T-034: cập nhật trạng thái từ kết quả thật, không tiếp tục ghi là chờ giao. Phần E1/E2 còn chưa phân xử phải chỉ đúng điều đã kiểm và bằng chứng thiếu; phép khác ngoài quyền được trình riêng.
2. **Thiếu quan sát hoặc nhãn độc lập:** ghi chính xác thông tin thiếu, vì sao dữ liệu hiện có không cung cấp, ai cần cung cấp và yêu cầu cho P9a/P10. Đối chiếu B16: mốc fault-on/onset/end, log bộ tạo tải, quan hệ trace/span với outcome, clock/coverage hoặc ánh xạ service → máy khi liên quan. Không coi collector khôi phục được thông tin chưa được ghi.
3. **Thuộc đánh giá sau khóa thiết kế:** nêu giả thuyết và bằng chứng cần ở P7 hoặc P10, cùng quyết định phụ thuộc. Không dùng test để hoàn tất lựa chọn thiết kế trên dev; quyền mở test vẫn cần Minh theo G3.

Không tự sửa yêu cầu P9a hoặc chuyển cổng; chỉ trình nội dung và bước cần Minh quyết.

### E1 — Phân xử tác động riêng của quy tắc pattern TraceRCA

- **Câu hỏi và giá trị:** việc cho dịch vụ lấy điểm từ pattern nhiều dịch vụ có góp phần làm caller/frontend đứng trên root, hay chênh quan sát chủ yếu còn do các bước khác? Kết quả ảnh hưởng cách quy nguyên nhân ở K3 và căn cứ đề xuất quy tắc chấm ở K5; không mặc định sẽ dùng TraceRCA trong P6.
- **Phạm vi:** các ca dev trong bảng `h6_pair_audit` của ledger đính chính; khai danh sách ca/cặp/cấu hình trước chạy từ nguồn này, gồm ca không có quan hệ cũ hoặc thiếu bằng chứng để đối chiếu trạng thái, không bỏ vì khó hay điểm xấu. Dùng cả điều kiện có hiện tượng và điều kiện đối chứng trong danh sách; các cặp chung một ca không là mẫu độc lập. Nhánh chính là pipeline tạo ra hiện tượng cũ, với các cấu hình ngưỡng 1 và 3 đã có; số mã tác giả được đối chiếu riêng đúng cấu hình, không lấy chênh hai pipeline làm hiệu ứng riêng của pattern. Không mở rộng sang toàn benchmark để tìm điểm tốt.
- **Trước can thiệp:** đọc phần tương ứng của bài và code đã ghim; xác định khác biệt singleton/pattern nhiều dịch vụ, selection, caps, điểm mặc định và tie. Ghi điều đã xác minh và điều chưa thể quy là lỗi cài bài. Ưu tiên dùng lại trung gian có đủ thành viên pattern; trường `set_size` một mình không đủ. Nếu cần, tái tạo invocation, flags, trace membership và frequent sets đúng code/cấu hình nguồn trên các ca đã khai; không đổi tiền xử lý để làm phép so đẹp hơn.
- **Đối chứng giữ nguyên (sham):** bản instrument không đổi quy tắc phải khớp đầu vào, trạng thái, điểm/hạng và trung gian có nguồn đối chiếu. Ghi chính xác dung sai nếu phép số thực cần dung sai, trước khi xem kết quả nhánh đổi; không nới dung sai để che khác biệt thứ hạng. Lệch sham thì sửa và kiểm lại trong T-034, giữ lượt lỗi; chưa được diễn giải can thiệp khi sham chưa đạt.
- **Chỉ đổi một yếu tố:** trên cùng invocation/flags/membership và cùng tập pattern sau mining/selection/caps, so chấm qua các pattern được giữ như bản nguồn với chỉ cho singleton trong chính tập đó đóng góp điểm. Giữ công thức J và in/out, tập dịch vụ ứng viên, quy tắc thiếu điểm và hòa của pipeline đang kiểm; không khai phá lại, tuyển lại hoặc bù singleton sau khi lọc. Nếu dịch vụ mất mọi pattern hợp lệ, ghi riêng mất bằng chứng, không gọi là điểm chứng minh dịch vụ bình thường. Dùng số học chính xác khi nguồn dùng số hữu tỷ.
- **Lưu và phân xử:** lưu định danh/thành viên pattern, J, in/out, điểm đóng góp, pattern quyết định điểm, độ phủ điểm và hạng root/caller ở cả hai nhánh; kiểm độc lập trên ví dụ nhỏ và các ca quan trọng. Báo tác động lên điểm khác với tác động lên hạng/tie/coverage. Có thay đổi thì chỉ quy phần tác động trong phép đổi đã cô lập; không thay đổi thì loại giải thích tương ứng trong phạm vi đã thử; thay đổi một phần thì nêu điều kiện. Không suy đã xác nhận chờ/lan vật lý, mọi chênh giữa hai pipeline hoặc ưu thế phương pháp mới.

### E2 — BOCPD đầy đủ trong miền log trên hai ca underflow

- **Câu hỏi và giá trị:** underflow (xác suất rất nhỏ bị làm tròn thành 0) có làm đổi posterior đầy đủ, trạng thái có xác suất cao nhất (MAP), hoặc điểm đổi (CP) không? Kết quả ảnh hưởng mức quy tác động số học ở K3 và căn cứ xử lý số học ở K5; không mặc định BOCPD được chọn cho P6.
- **Phạm vi:** `dev-3ae0a6c15a` và `dev-ba831dbeb8`; chạy đầy đủ chuỗi của cả đầu vào full (FF) và nhánh PF được `zero-lineage-summary-001.json` dẫn tới, vì kết luận cũ dựa trên đối chiếu này. Dùng đúng X, thứ tự cột, thời gian, prior của từng nhánh, hazard, cập nhật trạng thái, quy ước chỉ số và quy tắc CP đã ghim. Không thay prior, cửa sổ, tiền xử lý hoặc ngưỡng CP để tối ưu kết quả; nhãn chỉ đối chiếu sau tính.
- **Tính đầy đủ:** dùng log-density ổn định của cùng phân phối dự báo, tính nhánh reset/growth và chuẩn hóa bằng log-sum-exp tại mọi bước; cập nhật posterior miền log xuyên suốt. Không lấy log của PDF đã underflow về 0, không dùng normalizer native giữ cố định, không chỉ phục hồi vài lineage rồi gọi là detector đầy đủ. Không tự thêm sàn, jitter hoặc cắt run length làm thay mô hình.
- **Kiểm tương đương trước diễn giải:** native sham khớp m/CP và nguồn đã lưu; fixture nhỏ không underflow đối chiếu density, posterior, MAP và CP; kiểm chuẩn hóa, giá trị hữu hạn hợp lệ, prior/thứ tự cập nhật và ánh xạ chỉ số. Sai khác số thực cần dung sai có căn cứ khai trước; MAP/tie/CP phải báo riêng, không cho qua chỉ vì posterior gần nhau. Fixture có underflow dùng phép tham chiếu ổn định/độ chính xác cao trên kích thước nhỏ để kiểm phép toán. Lỗi bản cài mới thì sửa trong T-034 và giữ lượt lỗi, không gọi là kết quả khoa học.
- **Đầu ra và phân xử:** so toàn chuỗi native ↔ log-domain trong từng ca/nhánh; chỉ vị trí khác đầu tiên, lượng xác suất mất, chênh posterior, khoảng cách hai trạng thái đầu, m/CP và timestamp thay đổi; phân biệt underflow với nhiễu làm tròn hoặc hòa sát nhau. Lưu thống kê toàn chuỗi và lát cắt cần tái kiểm, không mặc định lưu mọi tensor trung gian lớn. Nếu CP không đổi, chỉ kết luận không đổi trên các chuỗi đã kiểm; nếu đổi, nêu tác động và hệ quả đối với cách dùng số cũ. Không suy detector tốt hơn từ số CP hoặc đổi kết quả baseline đã khóa.

**Thiết kế chi tiết và quyền tự xử lý E1/E2:** trước khi chạy nhánh đổi, Claude ghi danh sách nguồn/ca/cấu hình, phép giữ/đổi, bất biến, kiểm tương đương, bảng diễn giải và dự toán vào `results/T-034/thiet-ke-hai-phep-kiem.md`. Đây là cụ thể hóa hai phép đã duyệt, không là một vòng xin duyệt mới. Tự chọn cách đọc/lưu dữ liệu, chia lô, instrument, cài nhánh tương đương và sửa lỗi trong phạm vi này. Nếu không thể cô lập yếu tố, cần thêm phép khoa học/ca/cấu hình ngoài phạm vi, thay mô hình hoặc vượt quyền tài nguyên, dừng phần phụ thuộc và trình đúng thay đổi; không hạ yêu cầu kiểm để khép kết luận.

### Hỏi–đáp cho cô (K7)

- **Ít nhất 12 câu,** phủ:
  - vì sao chọn dataset và phương pháp;
  - baseline nào mạnh nhất, trong điều kiện nào;
  - phương pháp hỏng ở đâu, vì sao;
  - bộ phát hiện hỏng ở đâu, vì sao;
  - lan có đáng kể không;
  - vì sao Sock Shop, LEMMA-RCA được hay không được dùng (MRP §4);
  - câu nào chưa trả lời được và kế hoạch;
  - đồ thị sẽ nhắm vào hạn chế nào;
  - khi nào biết đồ thị có giúp không.
- **Mỗi câu trả lời:** tối đa 5 câu ngắn; mức bằng chứng; nguồn (đường dẫn và con trỏ). Không có số không có nguồn.
- **Câu trả lời trung thực** cả khi kết quả bất lợi, ví dụ "baseline không đồ thị mạnh trên RE2-TT" hay "nguyên nhân chưa phân xử được" (Q-04, SL20).

## Đầu ra (`results/T-034/`)

- `goi-g2.md` — gói trình chính, viết cho Minh và cô đọc hiểu mà không cần đọc repo:
  - §0 tóm tắt ba câu;
  - §1 K1; §2 K2; §3 K3; §4 K4; §5 K5; §6 K6; §7 K7;
  - §8 điểm Minh quyết ở G2: nhánh TraceRCA mã tác giả có đưa vào kế hoạch baseline G2/P7 không; có định nghĩa nhãn lan không; cách trình bày bốn ca ERROR (giữ cách chấm đã khóa); xử lý đề xuất liên quan TORAI B; cách dùng dòng độ nhạy MicroRank; hệ quả của kết quả E1/E2 và phần thật sự cần bổ sung ngoài hai phép đã giao. Phân biệt quyết định đã có với đề xuất mới; task không tự thay baseline hoặc quy tắc chấm.
- `ban-do-g2.json` — bản đồ hợp nhất dạng máy đọc: mỗi G2-Hn có mã gốc, mức, số, mẫu số, con trỏ nguồn.
- `bang-baseline.json` — số của K2 kèm con trỏ nguồn.
- `thiet-ke-hai-phep-kiem.md` — thiết kế và bảng diễn giải khai trước nhánh đổi; cập nhật chỉ bằng mục nối có thời điểm, giữ bản đã dùng mỗi lượt.
- `hai-phep-kiem.md`, `hai-phep-kiem.json` — kết quả E1/E2, nguồn, kiểm tương đương, so theo ca, kết luận và phụ thuộc; dẫn vào K3/K5/K6/K7.
- `scripts/`, `runs/<lượt>/` (manifest, hash đầu vào, kiểm V).

## Phạm vi ghi

Chỉ được ghi vào các đường dẫn dưới đây, cộng `LOG.md` của task này và dòng của task trong `docs/STATE.md`. Ghi ra ngoài thì dừng, đề xuất.

- `results/T-034/`.
- Trên hai EC2 hiện có: chỉ tạo/sửa file của T-034 dưới `/home/ubuntu/rca/T-034/` (script, bản sao code cần instrument, đầu vào cần chuyển, môi trường riêng nếu cần, log và kết quả). Nguồn T-032/T-033/T-025 và môi trường cũ chỉ đọc. Kết quả remote phải được đưa về `results/T-034/runs/<lượt>/` với manifest kiểm hash hai đầu trước dùng làm nguồn; laptop là nơi bàn giao đầy đủ. Không xóa file/lượt cũ để lấy chỗ.
- `docs/WHY.md`: chỉ nối nguyên văn WHY-51 ở Phụ lục vào cuối file, ở bước 0; phụ lục hiện gồm căn cứ E1/E2 được duyệt cùng lần mở rộng SPEC. Không sửa mục cũ. Nếu WHY-51 đã tồn tại đúng bản cũ được duyệt thì chỉ nối phần bổ sung E1/E2 còn thiếu vào cuối file, giữ tiêu đề dẫn WHY-51 và nguồn duyệt, không chèn sửa lịch sử; nếu đã có đủ thì không nối trùng. Nếu mã dùng cho nội dung khác thì dừng phần nối và trình Minh, không tự đổi mã.

Không sửa MRP, PLAN, DECISIONS, kết quả task khác, `src/`, `data/`. Đề xuất sửa các tài liệu đó (ví dụ cập nhật PLAN sau G2) ghi ở §8 của `goi-g2.md`, chờ Minh.

## Các bước

Mỗi bước ghi rõ cần đầu ra nào của bước nào (SL32).

0. **Mở phiên.** Phụ thuộc: SPEC đã duyệt; T-032, T-033 đã đóng.
   - **Tự kiểm SPEC trước triển khai:** trước khi tạo kết quả hoặc nối WHY-51, Claude đọc nguồn và tự đối chiếu mục tiêu, thiết kế, phép phân xử, phạm vi và tiêu chí xong với DT18, hướng dẫn của cô, MRP, quyết định hiện hành và bằng chứng mới nhất. Duyệt SPEC không chứng minh SPEC đúng. Nếu có lỗi hoặc mâu thuẫn ảnh hưởng mục tiêu, phép phân xử hay kết luận, dừng phần triển khai phụ thuộc và trình nguồn xung đột, hậu quả, sửa tối thiểu; không tự sửa SPEC hoặc tiếp tục chỉ vì SPEC đã duyệt. Ghi nhận kết quả tự kiểm trong LOG của bước 0. Đây là nghĩa vụ tự kiểm theo AGENTS, không thêm cổng duyệt; khi không có lỗi ảnh hưởng thì tiếp tục phần đã được duyệt, không xin duyệt lại.
   - Claude mở LOG, ghi nguyên lời duyệt và vai trò; thêm/cập nhật riêng dòng T-034 trong STATE. Không sửa lịch sử các task khác.
   - Băm và kiểm đầu vào trước khi nối WHY-51 (V1). Với tài liệu khung, ghim phiên bản thực sự dùng; với WHY/LOG được nối hợp lệ, kiểm phần đầu đã được chứng nhận và nguồn duyệt phần nối.
   - Nối nguyên văn WHY-51 sau khi kiểm nguồn, trước khi dùng lựa chọn trong kết quả. Ghi nhận phần nối và phiên bản WHY sau nối để việc kiểm cuối không coi thay đổi được phép là hỏng nguồn.
1. **Chuẩn bị và chạy E1/E2.** Phụ thuộc: nguồn tương ứng và WHY ở bước 0 đã hợp lệ. Khai thiết kế, kiểm đầu vào/môi trường, native sham và fixture; pilot có thể dùng luôn trong lượt đủ khi khớp thiết kế. Sau kiểm tương đương, chạy các nhánh đã duyệt, phân tích và kiểm V6/V7. E1 và E2 độc lập, có thể chạy trên hai máy cùng lúc; ưu tiên E1 nếu chỉ đủ một máy. Không cần chờ viết xong bảng G2 mới khởi chạy.
2. **Bảng baseline K2 và khung bản đồ K3.** Phụ thuộc: nguồn tổng hợp ở bước 0. Làm trong lúc máy chạy bước 1; kiểm V2/V3. Các dòng K3 phụ thuộc E1/E2 chỉ chốt sau kết quả tương ứng, không lấy giả thuyết thay kết quả.
3. **K4 lan.** Phụ thuộc: nguồn chờ/khả năng đo và các dòng K3 liên quan; phần không phụ thuộc E1/E2 làm ngay. E1/E2 không thay phép đo hoặc nhãn lan.
4. **K5, K6 và chốt K3.** Phụ thuộc: bước 2–3 và kết quả hợp lệ E1/E2 cho các kết luận liên quan. Nếu một phép gặp chặn thật, hoàn thành phần độc lập và báo rõ phần chưa đạt, không coi nhãn OPEN là đã hoàn thành phép được giao.
5. **K1 và K7.** Phụ thuộc: kết luận bước 1–4; cập nhật câu trả lời theo bằng chứng mới.
6. **Kiểm cuối.**
   - V4: script đối chiếu mọi số định lượng trong `goi-g2.md` và `hai-phep-kiem.md` với JSON nguồn.
   - V5: kiểm từng nhận định quan trọng với bằng chứng và phần mục tiêu nguồn; quét từ chỉ hỗ trợ tìm câu cần đọc lại.
   - Ghi LOG mục kết thúc phiên; viết prompt phản biện theo `docs/review-prompt.md`.

## Kiểm đúng đắn

| Mã | Kiểm | Đạt khi |
|---|---|---|
| V1 | Kết quả bất biến khớp manifest đúng phiên bản; WHY/LOG được nối thì phần đầu khớp chứng nhận và phần nối có nguồn duyệt; ghim phiên bản tài liệu khung dùng cho T-034 trước/sau phần nối được phép | Không lệch nguồn bất biến hoặc prefix; mọi phần nối và phiên bản dùng truy được. Lệch không giải thích được thì dừng phần phụ thuộc, báo Minh |
| V2 | Tính lại độc lập các số tổng của K2 từ bản ghi và JSON chấm | 0 lệch |
| V3 | Mỗi mã HP-n, M-n, H1–H17, D1–D7 và câu hỏi KT1–KT16/K1–K7 tại `closure-ledger.json#/questions` có mặt trong ít nhất một G2-Hn hoặc danh sách "không đưa vào" kèm lý do; áp đính chính từ `closure-ledger-review-001.json`, giữ task nguồn | Đủ; không mã/câu hỏi nào mất hoặc bị dùng theo trạng thái cũ đã đính chính |
| V4 | Số trong `.md` so với JSON | 0 lệch; 0 số định lượng không có nguồn |
| V5 | Với từng nhận định quan trọng trong `goi-g2.md`, đối chiếu phép kiểm cụ thể, đầu vào → xử lý → trung gian → đầu ra, yếu tố thay/giữ, ca sai và ca đúng tương ứng, giải thích cạnh tranh và phạm vi khái quát. Quét các cụm "nguyên nhân là", "chứng minh", "đồ thị sẽ" chỉ để hỗ trợ rà câu, không thay việc đọc lập luận | Kết luận không mạnh hơn bằng chứng; nói rõ hỗ trợ, bác bỏ hay chưa phân xử và quyết định phụ thuộc. CT/ĐC không tự xác nhận nguyên nhân riêng nếu phép kiểm thay nhiều yếu tố; không có từ bị quét cũng không tự đạt |
| V6 | E1: sham, bất biến đầu vào/tập pattern/caps, ví dụ kiểm độc lập, bao phủ danh sách ca/cấu hình đã khai, điểm/hạng/coverage và diễn giải | Tái lập nhánh giữ nguyên; chỉ yếu tố đã khai được đổi; mọi ca có kết quả/trạng thái có bằng chứng; kết luận không quy chênh giữa hai pipeline cho một bước chưa cô lập |
| V7 | E2: native sham, fixture không underflow/có underflow, cùng tham số và cập nhật, chuẩn hóa toàn chuỗi, MAP/CP/timestamp | Bản miền log được kiểm tương đương; đủ hai ca và nhánh FF/PF đã khai; đối chiếu toàn chuỗi, không thay bằng frozen-normalizer lineage hoặc số CP tổng |

**Xử lý phần chưa kiểm và giới hạn:** kiểm lại từng giới hạn cần dùng của T-024 đến T-033 theo nguồn mới nhất; không mặc nhiên giữ trạng thái cũ vì task đã đóng. Phân biệt: đã kiểm nhưng chưa phân xử; còn kiểm được trên dev; thiếu quan sát không thể phục hồi từ dữ liệu hiện có; thuộc đánh giá sau khóa thiết kế. Gắn các trạng thái này với ba nhóm K6, không gộp "chưa làm" vào "không thể làm".

Đọc code và trung gian đã lưu, đối chiếu ca và tính lại từ bản ghi hiện có thuộc phần kiểm/tổng hợp được phép: làm ngay khi cần trả lời câu hỏi của task và chi phí hợp lý; không dùng "chưa kiểm" thay cho việc này. E1/E2 và các bước tái tạo/kiểm tương đương cần thiết đã được duyệt, phải thực hiện trong phạm vi đã khai, không hỏi lại từng bước. Phép khoa học khác ngoài E1/E2 phải trình đúng thiết kế/phạm vi, chi phí, bằng chứng cần thêm và kết luận/quyết định bị chặn; không tự chạy vượt quyền. Mỗi phần còn mở ghi đã kiểm gì, nguồn ở đâu, vì sao chưa phân xử và bước xử lý. Giới hạn có thể kiểm tiếp không tự trở thành giới hạn dữ liệu. Không có số công bố cho bản đồ hạn chế để đối chiếu.

## Tiêu chí xong

- V1–V7 đạt, hoặc lệch có ghi nguyên nhân và Minh quyết. E1/E2 có kết quả hợp lệ và phân xử đúng câu hỏi trong phạm vi đã khai; không yêu cầu kết quả phải ủng hộ giả thuyết. Nếu chưa chạy/thiếu kiểm tương đương thì báo phần chưa hoàn thành, không tự nghiệm thu bằng ghi "chưa kiểm".
- K1–K7 có trong `goi-g2.md`. Mỗi kết luận có mức bằng chứng và nguồn.
- Mỗi nhận định quan trọng đạt kiểm lập luận V5; mỗi câu còn mở phân loại theo bằng chứng hiện tại và ghi phần đã kiểm, bằng chứng thiếu, bước xử lý và quyết định phụ thuộc. Không còn việc đọc/đối chiếu/tính lại cần thiết, làm được trong phạm vi với chi phí hợp lý, nhưng bị bỏ chỉ bằng nhãn "chưa kiểm". Phép mới ngoài quyền được trình đúng phạm vi, không được dùng phần chưa kiểm làm căn cứ đã xác nhận.
- Mọi G2-Hn có số ca/tổng theo ô, giải thích khác, lời tác giả hoặc "chưa thấy".
- Mỗi ứng viên K5 có mục đích, căn cứ đúng loại, mức bằng chứng thật, giải thích khác, tín hiệu dùng và dự đoán bác bỏ được trên dev. Ứng viên sửa hạn chế dẫn G2-Hn tương ứng; ứng viên DT18/nhu cầu kỹ thuật dẫn đúng nguồn. Phân biệt đủ căn cứ đề xuất với căn cứ còn thiếu để chọn thiết kế hoặc khẳng định hiệu quả; không tự chốt thành phần.
- K7 có ít nhất 12 câu, mỗi câu có nguồn.
- LOG có mục kết thúc phiên theo AGENTS mục 7 và prompt phản biện.

## Không làm

- Không chạy thực nghiệm khoa học ngoài E1/E2 và các kiểm tương đương cần thiết của chúng; không mở thành tối ưu tham số hoặc chạy lại toàn benchmark. Thiếu số khác thì trước hết kiểm nguồn, code và trung gian hiện có; nếu cần phép ngoài quyền, trình phạm vi, chi phí và kết luận phụ thuộc. Được tính lại từ bản ghi để kiểm V2–V7 và đo thời gian/RAM/dung lượng công việc của T-034.
- Không chọn thành phần P5/P6; không viết spec P6.
- Không khóa nhãn lan, không mở test.
- Không sửa MRP, PLAN, DECISIONS hay kết quả task khác.
- Không viết báo cáo tiến độ chính thức cho cô. MRP §8 đặt báo cáo đó ở G4. K7 là đầu vào cho báo cáo đó, không thay nó.

## Chi phí, máy thực hiện và độ khó

- **Phân công ban đầu:** laptop đọc nguồn, kiểm, viết script, tổng hợp; ưu tiên EC2 T-032 (`ubuntu@3.26.62.217`) cho E1 vì dữ liệu/môi trường TraceRCA ở đó; EC2 T-033 (`ubuntu@3.107.246.249`) cho E2 khi đủ chỗ cho đầu ra gọn. Tham khảo cấu hình kết nối chỉ đọc ở `results/T-032/runs/bo-sung-toan-dien-20261012-001/root_remote.py` và `results/T-033/runs/bo-sung-toan-dien-20261012-001/t33/controller.py`; không chạy nguyên các controller cũ vì chúng ghi vào task cũ. Giữ kiểm host key, không xuất nội dung khóa. Không khởi tạo, đổi loại, start/stop EC2 hoặc dịch vụ tính phí mới theo SPEC này.
- **Ảnh chụp tài nguyên chỉ đọc khi sửa SPEC, 13/10/2026:** hai EC2 đều trả `os.cpu_count()=2`; EC2 T-032 có `MemAvailable=7.394.271.232` byte, đĩa trống `20.148.240.384` byte; EC2 T-033 lần lượt `7.496.265.728` và `1.319.182.336` byte. Lệnh qua SSH chạy `python3 -B -`, đọc `/proc/meminfo`, `os.cpu_count()`, `os.getloadavg()` và `os.statvfs('/home/ubuntu/rca')`; load average khi kiểm gần 0. Kiểm lại khi khởi chạy, không coi số chụp là tài nguyên được dành riêng.
- **Quyền điều phối đã duyệt:** Claude tự chọn/chuyển laptop hoặc hai EC2 hiện có theo chỗ có đầu vào, môi trường khớp, RAM/đĩa và thời gian hoàn thành gồm truyền dữ liệu; không hỏi lại việc chia lô, chọn máy hoặc thứ tự các phần độc lập trong phạm vi này. Không đổi môi trường cũ để cứu số; nếu cần môi trường riêng, đặt dưới T-034 và ghim dependency theo nguồn. Chạy Python với `-B`/`PYTHONDONTWRITEBYTECODE=1` khi import code nguồn; đặt cache/log phát sinh dưới T-034 để giữ nguồn chỉ đọc. Hai phép độc lập được chạy đồng thời trên hai máy; bắt đầu tối đa một tiến trình nghiên cứu nặng mỗi máy, ghi cấu hình luồng BLAS để tránh tranh CPU/RAM. Laptop có thể nhận phần phù hợp sau khi kiểm tài nguyên; Minh có thể đóng ứng dụng, không coi RAM trống của lần đo cũ là giới hạn cố định.
- **Giữ chi phí truyền/lưu thấp:** dùng nguồn cũ chỉ đọc tại chỗ; chỉ chuyển script/đầu vào thiếu đã xác minh hash, không chép toàn lịch sử. E1 lưu pattern và thống kê đủ tái kiểm theo ca; E2 lưu kết quả toàn chuỗi gọn và các lát cắt cần giải thích, tái dùng ma trận nguồn. Mục tiêu lập kế hoạch đầu ra mới: E1 dưới 500 MiB, E2 dưới 100 MiB, chưa đo; không là trần để cắt ca hay bằng chứng. Ước kích thước trước chạy, ghi dung lượng thật sau mỗi ca; nếu máy thiếu chỗ thì chuyển máy/đầu ra trong phạm vi đã duyệt, không xóa lịch sử. Máy T-033 ít đĩa nên không lưu tensor lớn hoặc tạo môi trường mới ở đó khi chưa đủ chỗ.
- **Mốc đo chỉ đọc ngày 13/10/2026:** băm tuần tự 6.224 file của `results/T-032/runs/bo-sung-toan-dien-20261012-001/manifest-final.json`, tổng 882.842.856 byte, mất 5,946 giây trên laptop i5-1240P; 0 lệch. Lệnh đã chạy `py -3 -X utf8 -`: đọc `files` của manifest; với mỗi `path`, đọc khối 1 MiB và tính SHA-256, cộng số byte, so `sha256`; đo vòng lặp bằng `time.perf_counter()`. Đây là thời gian kiểm hash trong điều kiện của lượt đó, không phải benchmark tổng hợp hoặc thực nghiệm.
- **Dung lượng nguồn:** lệnh Python chỉ đọc liệt kê file bằng `Path('results', task).rglob('*')`, cộng `stat().st_size` cho T-024/025/026/028/029/032/033 cho tổng 5.830.034.113 byte (khoảng 5,43 GiB) ở lượt kiểm trên. Đây là toàn bộ lịch sử kết quả trong bảy thư mục, không phải lượng phải nạp RAM hoặc chuyển máy. Chưa đo RAM đỉnh và tổng đầu ra mới; ghi số thực từ pilot, không tự đặt trần để bỏ kiểm.
- **Dự toán (chưa đo cho code mới):** tổng hợp vài phút đến vài chục phút máy; đọc/cài/kiểm/diễn giải vài giờ agent. E1 chưa có ETA đáng tin trước kiểm trung gian: chấm lại khác xa khai phá lại tập pattern. E2 có mốc native full của hai ca khoảng 379 và 391 giây ở `results/T-033/runs/bo-sung-toan-dien-20261012-001/t33/engine-final-summary-001.json#/slots` (lọc opaque_id và branch=native_sham); đó không phải thời gian nhánh log-domain hoặc FF+PF. Dự trù E2 vài chục phút đến vài giờ tổng máy cho sham/fixture/nhánh đổi, cập nhật sau pilot hợp lệ; không lấy thời gian một ca làm dự toán toàn gói. Nêu rõ wall-clock, tổng thời gian máy và thời gian agent, tránh cộng thời gian hai máy thành thời gian chờ.
- **Đo từ đầu:** pilot thuộc phạm vi E1/E2, không phải vòng xin phép mới. Ghi thời gian từng bước/ca, RAM đỉnh, đĩa và tiến độ ra file ngay từ đầu; dùng kết quả hợp lệ của pilot trong lượt đủ, không chạy lại vô cớ. Sau pilot cập nhật ETA và bố trí máy, báo Minh khi laptop có tiến trình cần giữ chạy. Nếu cần hơn một phiên thì ghi checkpoint và trình chia theo phụ thuộc theo AGENTS; không giảm phép phân xử cho vừa phiên.
- **Độ khó (đánh giá kế hoạch sau mở rộng):** tổng hợp máy nhẹ, nhưng E1 có rủi ro số lượng pattern; E2 là kiểm số học xác suất. Lập trình và suy luận khoa học cao, phải kiểm bản cài mới tương đương và phân biệt thay đổi số học với thay đổi mô hình. Ít ca hơn các gói rộng T-032/T-033, không mặc nhiên dễ hơn ở các bước then chốt; ưu tiên model có khả năng đọc code và suy luận sâu, một agent thực hiện.
- **Giới hạn tài nguyên còn hiệu lực:** phép/lượt dự kiến dài hơn 1 giờ, tải hơn 5 GB hoặc thao tác tốn kém khác vẫn theo AGENTS mục 3.8: báo dự toán và chờ quyền tương ứng nếu chưa có; không chia vụn để né. Không đặt timeout một giờ rồi bỏ kết quả/nghĩa vụ. Quyền điều phối không mở rộng số ca/cấu hình hoặc cho phép một phép khoa học khác; kiểm thiếu tài nguyên bằng số thật, không dùng ước đoán vô căn cứ để dừng.
- Không dùng subagent theo lời giao của Minh ngày 13/10/2026.

## Rủi ro và điều chưa chắc

- **Nếu T-032, T-033 cho phần lớn "chưa phân xử":** gói phải nói thẳng phần chưa biết, bằng chứng thiếu và quyết định phụ thuộc. Chưa phân xử không chứng minh đồ thị giúp hoặc không giúp. Không suy số ứng viên từ số hạn chế đã xác nhận; xét từng ứng viên theo căn cứ P4, DT18 hoặc nhu cầu kỹ thuật và mức dùng bằng chứng của MRP §3.
- **Thang mức bằng chứng là quy ước của dự án.** Ranh giới CT/ĐC/LĐ có thể bị tranh luận; mỗi dòng ghi mức của từng nguồn con để người đọc tự kiểm.
- **Hai dataset khác nhịp metric và độ dài nền** (WHY-37). So sánh giữa dataset chỉ mô tả.
- **Mốc G2 15–18/10/2026 (Q-70):** T-032 đã đóng 13/10, T-033 đã đóng 11/10; lịch còn tùy ngày duyệt và triển khai SPEC này. Không hạ mức bằng chứng để kịp mốc.

## Nội dung duyệt SPEC và quyết định G2

1. Minh đã duyệt SPEC bản 3 kèm văn bản WHY-51 ở Phụ lục và giao Claude triển khai ngày 13/10/2026; duyệt bổ sung R1–R5, bước tự kiểm trước triển khai, rồi đưa E1/E2 vào T-034 và điều phối tài nguyên. WHY-51 được bổ sung căn cứ hai phép ở Phụ lục để Claude nối trước sử dụng; quyền thực nghiệm giới hạn ở E1/E2 như SPEC này.
2. Vai trò thực hiện: Claude làm, Codex phản biện kết quả. Codex chỉ ghi SPEC đã duyệt và tự kiểm trong lượt chuẩn bị này, không đổi người làm T-034.
3. MRP §7 ghi phản biện chéo ở G2 không bắt buộc; gói này có phản biện kết quả theo phân công trên vì là đầu vào trực tiếp cho câu trả lời với cô. Người làm soạn prompt theo `docs/review-prompt.md`; Minh chuyển hoặc quyết dừng. Duyệt SPEC không tự duyệt các lựa chọn ở §8 của gói G2.

## Phụ lục — Văn bản WHY-51 đã duyệt (Claude nối vào cuối `docs/WHY.md` ở bước 0)

```markdown
## WHY-51. Gói trình G2: thang mức bằng chứng chung và ứng viên P5/P6 có điều kiện bác bỏ — Đã quyết (Minh duyệt SPEC T-034 ngày 13/10/2026)

- **Chọn:** hợp nhất các hạn chế của T-028, T-029, T-032, T-033 thành bản đồ G2-Hn; mỗi dòng ghi một mức bằng chứng cao nhất theo thang CT (can thiệp), ĐC (đo cơ chế), LĐ (liên hệ có đối chứng), MT (mô tả), CK (chưa kiểm), kèm mức của từng nguồn con. Câu "vì sao" ở mỗi dòng ở một trong ba trạng thái: đã xác lập ở mức X, đã loại được giải thích Y, chưa phân xử vì Z. Ứng viên P5/P6 ghi căn cứ đúng mục đích: sửa hạn chế P4, đáp ứng DT18 hoặc nhu cầu kỹ thuật. Mỗi ứng viên có mức bằng chứng thật, giải thích khác, tín hiệu dùng và dự đoán bác bỏ được trên dev; không chọn, không xếp hạng theo kỳ vọng thắng. Tách ba mức dùng bằng chứng của MRP §3: đề xuất để thử, chọn thiết kế trên dev, khẳng định hiệu quả sau đánh giá. CT/ĐC không tự đủ để chọn thiết kế; không loại ứng viên chỉ vì hiện tượng mới đạt LĐ/MT nếu có căn cứ kỹ thuật và dự đoán kiểm được.
- **Vì sao:** cô yêu cầu chuỗi hiểu phương pháp → thực nghiệm → hạn chế → phương pháp đồ thị có liên kết logic (WHY-01). Thang chung giúp không đọc liên hệ thành nguyên nhân (SL23), nhưng không thay việc xét bằng chứng cho từng mục đích. Thành phần sửa hạn chế nối với bằng chứng P4; thành phần theo DT18 hoặc nhu cầu kỹ thuật nêu đúng lý do, không dựng một hạn chế để hợp thức hóa. Giữ ranh giới giữa đề xuất, lựa chọn và hiệu quả giúp tránh thiết kế trước rồi tìm kết quả biện minh (SL1, SL22). Điều kiện bác bỏ khai trước giữ QT4.
- **Phương án đã xét:** giữ nguyên bốn bản đồ riêng (người đọc phải tự hợp nhất, dễ đếm trùng); xếp hạng hạn chế theo "mức đáng kể" khi chưa có định nghĩa được chọn (không đủ căn cứ); viết luôn spec P6 trong gói G2 (vượt phạm vi tổng hợp, MRP đặt lựa chọn sau G2); chỉ cho ứng viên mức CT/ĐC hoặc bắt mọi thành phần dẫn hạn chế (trộn ngưỡng đề xuất với chọn thiết kế và bỏ căn cứ DT18/nhu cầu kỹ thuật); nêu ứng viên chỉ từ mã hạn chế mà không có lý do kỹ thuật, giải thích khác và dự đoán bác bỏ (không đủ căn cứ đề xuất theo MRP §3).
- **Bằng chứng thiết kế:** MRP §2.1, §3, §7, P4, P6; PLAN-P3-G2 §8; WHY-01, WHY-38–50, gồm phần nối ngày 13/10; LESSONS SL1, SL14, SL20, SL22, SL23, QT4, QT15.
- **Kết luận phụ thuộc:** quyết định G2 của Minh; spec P5/P6 dẫn G2-Hn cho thành phần nhằm sửa hạn chế, và dẫn căn cứ DT18 hoặc nhu cầu kỹ thuật cho thành phần khác; câu trả lời với cô về P3/P4. Thang mức bằng chứng là quy ước của dự án, không phải chuẩn ngoài; gói tổng hợp không tự xác nhận cơ chế còn mở hoặc lợi ích đồ thị.

### Bổ sung WHY-51 — Hai phép phân xử trong T-034, Minh duyệt 13/10/2026

- **Chọn:** thực hiện E1 can thiệp riêng quy tắc pattern trên cùng trung gian TraceRCA và E2 tính BOCPD đầy đủ trong miền log trên hai ca underflow, gồm FF/PF liên quan; giữ native sham, fixture, nguồn và baseline cũ. Thiết kế chi tiết trước nhánh đổi theo SPEC; không tối ưu tham số hoặc chọn phương pháp P6.
- **Vì sao:** E1 phân biệt đóng góp của quy tắc chấm với các khác biệt pipeline và giả thuyết chờ/lan; E2 phân biệt tác động tính toán số học với giới hạn của mô hình. Cả hai có kết quả có thể làm đổi mức kết luận P4 hoặc căn cứ đề xuất P6. Biết có underflow hoặc thấy thứ hạng hai pipeline khác nhau chưa trả lời tác động riêng này.
- **Phương án đã xét:** chỉ tổng hợp OPEN (giữ kết luận trung thực nhưng không hoàn thành phép còn làm được có giá trị); dùng chênh hai pipeline hoặc frozen-normalizer lineage thay can thiệp đầy đủ (không cô lập yếu tố hoặc chưa cập nhật đầy đủ posterior); chạy lại mọi baseline/tối ưu tham số (vượt câu hỏi cần phân xử). Chọn hai phép gọn với danh sách ca từ nguồn hiện có và kết luận theo điều kiện.
- **Bằng chứng để giao kiểm, chưa là kết quả:** `results/T-032/runs/bo-sung-toan-dien-20261012-001/closure-ledger-review-001.json#/pattern_candidate`, `/remaining_current_declared_computations`; bản đối chiếu đính chính §3 và §8; `results/T-033/runs/bo-sung-toan-dien-20261012-001/t33/zero-lineage-summary-001.json#/cases`, `/interpretation`. Quyền mới: lời Minh đưa hai phép vào T-034 trong SPEC. Số liệu mới chỉ được dùng sau kiểm tương đương và manifest của T-034.
- **Kết luận phụ thuộc:** mức quy nguyên nhân ở K3, ứng viên K5 và câu còn mở K6; nếu một phép không phân xử, ghi đúng phần đã kiểm và phần thiếu. Không tự đổi baseline, khóa thiết kế, xác nhận lan vật lý hoặc suy detector tốt hơn/lợi ích đồ thị. Phân công máy là lựa chọn thực hiện có thể đổi trong phạm vi tài nguyên đã duyệt, không là lựa chọn khoa học.
```
