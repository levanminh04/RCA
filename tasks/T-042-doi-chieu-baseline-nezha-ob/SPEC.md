# T-042 — Đối chiếu baseline Nezha-OB với số công bố

- **Trạng thái:** đã duyệt tạo ngày 23/10/2026; Minh duyệt bổ sung phạm vi normal N ngày 24/10/2026 theo Q-191, sau phản biện kết quả trong chat. Phần bổ sung ở cuối file là quyền hiện hành cho lượt này; các phần trước giữ lịch sử. Codex làm, Claude phản biện; chưa nghiệm thu.
- **Người làm:** Codex.
- **Người phản biện:** Claude.
- **Thuộc gói MRP:** P3–P4, bổ sung căn cứ trước thiết kế P6 và đánh giá P7.
- **Cổng:** trọng tâm G2; G2 đã duyệt, G3 vẫn OPEN. Task này không tự mở lại các task đã đóng.
- **Mã task:** thư mục task hiện có kết thúc ở T-041. Minh chọn T-042 cho đối chiếu. Tham chiếu T-042 dành cho hạ tầng trong kế hoạch sẽ được sửa ở lượt được duyệt riêng.

## Mục tiêu

Tìm những khác biệt nào có thể giải thích kết quả baseline của repo trên Nezha-OB thấp hơn số công bố, trước khi dùng các kết quả này làm căn cứ thiết kế phương pháp.

Nguồn trực tiếp chi phối:

- `D:/RCA-flashticket/docs/reference/sources/DT18-de-tai-va-nhiem-vu.md`, NV3: thực nghiệm, đánh giá và phân tích trường hợp hiệu quả hoặc hạn chế.
- `D:/RCA-flashticket/docs/reference/sources/advisor-2026-09-23.md`, §1: hiểu sâu phương pháp → mở rộng thực nghiệm → chỉ ra hạn chế → thiết kế đồ thị.
- `D:/RCA-flashticket/docs/MRP.md`, RQ1, RQ2; P3 về kiểm tái lập và xử lý độ lệch lớn; P4 về chuỗi bằng chứng và giải thích cạnh tranh; P7 về baseline, điều kiện so sánh và khóa trước test.

Đây là task **đối chiếu nguồn và phân xử nguyên nhân**, không phải tìm cấu hình có điểm gần bài nhất.

Mỗi phần chênh lệch phải được phân loại bằng bằng chứng:

1. Lỗi cài đặt hoặc đầu vào của repo.
2. Khác biệt giao thức có chủ đích.
3. Giới hạn dữ liệu hoặc khác phiên bản.
4. Chưa phân xử được với nguồn và dữ liệu hiện có.

Các nhóm có thể cùng tồn tại. Không ép toàn bộ độ lệch vào một nguyên nhân.

**Phạm vi một phiên được đề xuất:** đối chiếu đầy đủ nguồn hiện có; kiểm đầu vào dev; dùng lại trung gian hợp lệ; chạy các phép phân xử SimpleRCA đã xác định dưới đây. Việc dựng và kiểm pipeline tác giả chưa định danh được tách thành task nối tiếp nếu còn cần. T-042 phải bàn giao hợp đồng, nguồn thiếu, phép chạy và chi phí của phần đó; không coi nó là nghĩa vụ đã hoàn thành.

## Câu hỏi, bằng chứng và quyết định

Tất cả giả thuyết nguyên nhân dưới đây là **CANDIDATE — chưa kiểm**, trừ những quan sát đã có nguồn hợp lệ. Duyệt phép thử không xác nhận giả thuyết.

| Câu hỏi và nguồn yêu cầu | Kết luận/lựa chọn cần phân xử; giải thích khác | Phép kiểm và bằng chứng cần có | Kết quả hỗ trợ, bác bỏ hoặc chưa phân xử | Phần còn thiếu, quyết định phụ thuộc và hướng xử lý |
|---|---|---|---|---|
| Hai bên đang đo cùng đại lượng và cùng đối tượng không? P3, P7 | Khác tập ca, mức service/pod, mẫu số, hòa, trạng thái lỗi hoặc cách tính độ đo | Đọc định nghĩa trong hai bài, evaluator và danh sách chấm. Đặt cạnh thứ hạng gốc, kỳ vọng khi hòa và các cận trên cùng bản ghi dev | Nếu chấm lại cùng thứ hạng làm đổi số thì định lượng phần do chấm. Nếu không đổi thì bác bỏ cách chấm đó như giải thích đủ | Thiếu thứ hạng tác giả hoặc định nghĩa đủ rõ thì chưa xác nhận so trực tiếp. Không mở test để khớp trung bình |
| Chỉ khác tập ca có giải thích được độ lệch SimpleRCA không? P3 | Dev khó hơn toàn bộ tập; hoặc hai bên khác chương trình/đầu vào/cách chấm | Kiểm phép chặn số học bằng số dev đã lưu và metadata công bố. Với điều kiện dev22 thuộc đúng full56 và cùng Top@1, cận tốt nhất là `(7+34)/56` | Cận 0,732 thấp hơn 0,91 chỉ loại giải thích “chỉ khác tập ca” dưới các điều kiện trên. Không xác định lỗi nằm ở đâu | Danh tính full56 tác giả và cách chấm còn cần xác minh; không dùng cận này như quan sát trên 34 ca test |
| Adapter có vi phạm hợp đồng đã duyệt không? P3, P4 | Sai đơn vị, thời gian, ánh xạ, biên cửa sổ, mất kênh hoặc xử lý bản lặp; đối lập là thực hiện đúng giao thức nhưng giao thức khác bài | Lần raw dev → bộ lọc → payload → đầu vào lõi. Tính độc lập số dòng, membership N/A, đơn vị duration/metric, ánh xạ service và bộ cột | Chỉ gọi lỗi cài đặt khi chỉ được hợp đồng bị vi phạm và ca/đầu vào chịu ảnh hưởng. Làm đúng Q-84/Q-85 nhưng khác tác giả là khác giao thức | Phát hiện lỗi cần sửa thì trình đúng patch và phạm vi chạy lại; không tự sửa `src` hoặc thay số P3 |
| Các quy ước M4 có góp phần làm SimpleRCA thấp không? WHY-17/33, P4 | Ngưỡng metric hoặc đơn vị đếm cảnh báo; đối lập là thiếu tín hiệu, kênh/cửa sổ hoặc chương trình tác giả khác hẳn | Trên cùng payload dev, so thiết kế 2×2: `sigma=3`/`P95` × `events`/`channels`. Giữ trace, log, cửa sổ, tập ứng viên và cách chấm. Lưu ngưỡng, count, phiếu từng nguồn và hạng | Đổi một yếu tố làm điểm/hạng thay đổi theo chuỗi dự đoán thì xác nhận tác động của yếu tố đó trong M4. Không đổi hoặc làm hỏng ca đúng thì bác bỏ giải thích “đủ để sửa” | Dù điểm tăng, vẫn chưa chứng minh đó là chương trình sinh 0,91. Không chọn cấu hình thắng thành baseline mới |
| MicroRank của repo khác bản tạo số công bố ở bước nào? P3, P4 | Bộ chia trace, đầu vào operation, PageRank/spectrum, nguồn nền hoặc quy tắc chấm | Đọc code ghim; dùng lại chuỗi và can thiệp T-032/T-034. Đối chiếu nhóm trace, coverage, trọng số, spectrum và thứ hạng trước/sau phép đổi | Phân biệt phần đã có can thiệp, phần mới chỉ quan sát và phần còn lại chưa giải thích. Không gọi bộ chia thay thế của repo là MicroRank gốc | Thiếu bản cài/cấu hình MicroRank được tác giả Nezha dùng thì chưa tái lập Table 3. Nêu nguồn cần từ tác giả và phép chạy nối tiếp |
| Nền, cửa sổ, kênh và tập ứng viên có khác có chủ đích không? WHY-22/26/37 | Nền ngắn hoặc không đại diện; cắt theo start/end; bỏ Node*; khác đơn vị service/pod; đối lập là lỗi adapter hoặc thuật toán | So hợp đồng bài–code–repo; đọc các bảng độ nhạy T-026 và trung gian dev đã lưu. Xác minh sự thiếu hụt ở đầu vào thật | Ghi “khác có chủ đích” khi có quyết định nguồn. Chỉ quy tác động khi có phép so giữ các yếu tố còn lại hoặc chuỗi bằng chứng trực tiếp | Không tự thêm construct_data, kéo cửa sổ, gán host về service, nội suy hay giả status. Nếu cần, trình nguồn, miền thời gian và phép thử riêng |
| Có thể quy cho dữ liệu hoặc phiên bản không? P4 | Release, preprocessing, schema hoặc quan sát khác; đối lập là lựa chọn cài đặt/giao thức | Đối chiếu revision, inventory, schema, metadata ca và input contract. Đọc cả ca sai và ca đúng có điều kiện tương ứng | Thiếu trường/quan sát được xác minh là giới hạn đầu vào; chưa tự chứng minh nó gây độ lệch. Không có provenance tương đương thì giữ khác phiên bản ở mức OPEN | Tác giả cung cấp code/config/preprocessing và kết quả đúng ca dev; Minh quyết bổ sung nguồn. Hạn chế quan sát xác nhận phải nêu hệ quả P9/FlashTicket |

## Đầu vào

### Quyền dữ liệu

- Chỉ 22 ca dev trong `D:/RCA-flashticket/results/T-026/allowlist-dev.json`.
- Nhãn tại `D:/RCA-flashticket/results/T-026/nhan-dev.json` chỉ dùng ở evaluator và phân tích sau khi ghi đầu ra.
- Không đọc telemetry hoặc kết quả từng ca của 34 ca test; không đọc `data/locked/`.
- Bộ đọc phải chọn đúng ca và lọc miền thời gian trước khi trả giá trị đo. Người phân tích không mở nguyên CSV ngày có chứa phần test.
- Metadata tổng hợp công bố được dùng để đối chiếu; không phải quyền mở dữ liệu từng ca.
- Mốc tiêm chỉ được dùng ở adapter chế độ (a). Root, loại lỗi, tên ca và đường dẫn không đi vào lõi phương pháp.

### Tài liệu và kết quả

1. `D:/RCA-flashticket/AGENTS.md`; `docs/STATE.md`, `MRP.md`, `DECISIONS.md`, `WHY.md`, `LESSONS.md`, `review-prompt.md` trong cùng repo.
2. `D:/RCA-flashticket/docs/KHAO-SAT-SAU-K1-K6.md`: §1 điểm 1, KS-15, A.1, A.3; chỉ dùng như danh sách nhận định cần kiểm.
3. `D:/RCA-flashticket/tasks/T-026-nezha-ob-che-do-a/SPEC.md` và LOG, đặc biệt phiên 7–8.
4. Tại `D:/RCA-flashticket/results/T-026/`: allowlist, nhãn dev, mappings, config, `ban-ghi-dua-vao-cham.json`, `cham-a.json`, chi phí và bản ghi được danh sách chấm trỏ tới.
5. `D:/RCA-flashticket/results/T-026/runs/session-005/`: `handoff-manifest.json`, `external-code-manifest.json`, `published-reference.json`.
6. `D:/RCA-flashticket/results/T-008/the-dataset.md`, nguồn bài Nezha và các manifest được thẻ dẫn.
7. Tại `D:/RCA-flashticket/results/T-017/`: `ho-so-simplerca.md`, `so-cong-bo.csv`, `doi-chieu-code.md`, `type-i-ii.md`, nguồn FSE26, `inventory-files.csv`, manifest sửa/đóng tương ứng.
8. `D:/RCA-flashticket/results/T-034/goi-g2.md`, `bang-baseline.json`, `ban-do-g2.json`; manifest tại `runs/manifest-cuoi-007/manifest.json`.
9. Chỉ những code/trung gian dev của T-032 và T-041 mà các nguồn trên dẫn trực tiếp; kiểm manifest tương ứng trước dùng, không quét toàn bộ kho kết quả.

Các quyết định trọng yếu: quyền dùng Nezha; chia theo ô; chế độ biết mốc; giao thức P3; mốc thời gian và đầu vào riêng Nezha; trạng thái G2. Đọc Q-59, Q-61–66, Q-74/76, Q-84/85, Q-149 cùng WHY-17, 22–24, 26–28, 31–33, 37 và phần WHY của các can thiệp T-032 được sử dụng.

**Xử lý hash:** dùng manifest phù hợp với phiên bản thực tế. `cham-a.md` T-026 đã sửa sau manifest bàn giao; không dùng nó làm nguồn số. JSON đã khớp là nguồn số. Mismatch chưa giải thích thì dừng phần phụ thuộc; không tự cập nhật manifest để hợp thức hóa.

### Code, revision và giấy phép

| Code | Nơi ghim revision/hash | Cách dùng trong T-042 |
|---|---|---|
| M4 và adapter P3 | `D:/RCA-flashticket/results/T-026/ban-ghi-dua-vao-cham.json`, `source_hashes`; `src/simplerca/`, `src/p3/` trong repo | Đọc và gọi code đã có; không sửa code dùng chung |
| RCAEval và BARO | `D:/RCA-flashticket/results/T-026/runs/session-005/external-code-manifest.json`, `rcaeval_revision`, `baro_revision` | Đối chiếu các bản được T-026 dùng. LICENSE local của cả hai là MIT |
| MicroRank tác giả | `D:/RCA-flashticket/src/microrank/PROVENANCE.json`, `revision`; LICENSE đi kèm là MIT | Đối chiếu hàm chính thức với bản RCAEval sửa đầu vào; không đồng nhất chúng |
| Nezha tác giả | `D:/RCA-flashticket/results/T-008/runs/run-001/manifest.json`, `revision`; nguồn code MIT | Đọc giao thức và evaluator. Không chạy entrypoint đọc toàn tập |
| SimpleRCA `orig`, `rcaeval`, `rcaeval_re3_ss` | `D:/RCA-flashticket/results/T-017/sources/download-manifest.json`, các mục tree/URL ghim revision và file hash | Đọc ba snapshot tại `D:/RCA-ext/work/T-017/sources-audit/github/`. Xác định đường chạy, schema, nhãn, fusion và khác biệt |
| Artifact FSE chứa SimpleRCA | `D:/RCA-flashticket/results/T-017/sources/fse-new-artifact-code-comparison.json` | Dùng kiểm provenance. Không suy giấy phép Apache ở root áp dụng cho vendor SimpleRCA |

Ba snapshot SimpleRCA không có LICENSE/COPYING trong tree đã kiểm. Phạm vi giấy phép upstream còn OPEN; T-042 không chép chúng vào `src` hoặc phát hành lại.

`orig` yêu cầu Python ≥3.13 và rcabench-platform; entrypoint mặc định gọi NezhaRCA, nhận sáu parquet normal/abnormal. Chưa xác định chuỗi chuyển CSV Nezha thành đầu vào sinh Bảng 2. T-042 không gọi nhánh này là tái lập bài.

Môi trường chạy nhánh M4: môi trường Python 3.12 hiện có đã dùng cho các kiểm trước, ghim danh sách thư viện trước chạy. Dùng `-B`, không tạo bytecode. Không cài môi trường mới hoặc tải thêm trong phạm vi task này.

## Đầu ra

Trong `D:/RCA-flashticket/results/T-042/`:

| File | Nội dung |
|---|---|
| `nguon.json` | Nguồn, revision, giấy phép, hash, phạm vi đọc, đường dẫn nguồn local; kết quả kiểm khả dụng |
| `doi-chieu.md` | Bảng bài–code tác giả–repo: tập ca, phiên bản, đầu vào, N/A, đơn vị, ứng viên, luật từng nguồn, fusion, hòa, lỗi, thời gian |
| `ke-hoach-chay.json` | Cấu hình các nhánh, ca dev, nguồn trung gian dùng lại, phụ thuộc, dự đoán và ngân sách trước chạy |
| `phan-xu.json` | Từng giả thuyết: quan sát, phép kiểm, kết quả, giải thích cạnh tranh, mức kết luận và bằng chứng thiếu |
| `bao-cao.md` | Trả lời mục tiêu nguồn; tác động tới các hạn chế Nezha-OB và quyết định P6/P7; đề xuất phần nối tiếp |
| `manifest.json` | Hash và danh mục đầu ra cuối |
| `scripts/doi_chieu.py` | Kiểm nguồn và tổng hợp kết quả cũ |
| `scripts/chay_dev.py` | Bộ bọc dev, audit đầu vào và các nhánh M4 đã nêu |
| `scripts/kiem_doc_lap.py` | Tính độc lập phiếu, thứ hạng, hòa và độ đo |
| `runs/<run-id>/` | Config, tiến độ, thời gian/RSS, stdout/stderr, bản ghi từng ca, summary và kết quả kiểm; giữ cả lượt hỏng |

Bản ghi từng ca dùng mã mờ. Chỉ lưu thống kê, ngưỡng, phiếu, điểm và provenance cần kiểm; không lưu payload span/log/CSV thô. Dữ liệu phương pháp ở RAM.

Báo cáo phải có đủ:

1. Hạn chế đã xác nhận và điều kiện.
2. Lỗi cài đặt hoặc thiếu đầu vào.
3. Khác biệt giao thức và giả định/cách tính, kèm giải thích khác.
4. Thông tin quan hệ có thể bổ sung; chưa khẳng định đồ thị giúp.
5. Câu còn mở, bằng chứng thiếu, người cung cấp và quyết định phụ thuộc.

Kết luận cơ chế phải dẫn được đầu vào → bước xử lý → trung gian → đầu ra. Nếu chưa xác định bước gây sai thì ghi đúng phần chưa biết.

## Phạm vi ghi

**Lượt tạo ngày 23/10/2026:** chỉ lưu SPEC, LOG và bàn giao của T-042, ghi quyết định tại `docs/DECISIONS.md`, đồng bộ dòng T-042 trong `docs/STATE.md`; chưa triển khai nghiên cứu, chưa ghi WHY. Phiên Codex mới thực hiện quyền có điều kiện theo Q-189: tự soát trước; có điểm bất hợp lý thì dừng báo Minh, không tự sửa SPEC; nếu không có thì triển khai ngay trong phạm vi dưới đây. Nội dung WHY đã nêu bên dưới được ghi trước khi dùng lựa chọn trong kết quả.

Phạm vi đã được Minh duyệt cho T-042:

- Tạo `D:/RCA-flashticket/tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md` từ bản được duyệt; sau đó khóa.
- Ghi thêm `D:/RCA-flashticket/tasks/T-042-doi-chieu-baseline-nezha-ob/LOG.md`.
- Tạo các đầu ra đã liệt kê trong `D:/RCA-flashticket/results/T-042/`; mỗi lượt dùng thư mục mới, không ghi đè lịch sử.
- `D:/RCA-flashticket/docs/STATE.md`: chỉ thêm/cập nhật dòng T-042.
- `D:/RCA-flashticket/docs/DECISIONS.md`: chỉ nối quyết định Minh về giao vai trò, chọn mã T-042 và quyền thực hiện thực tế đã được duyệt; không ghi giả thuyết thành quyết định.
- `D:/RCA-flashticket/docs/WHY.md`: chỉ nối mục lý do T-042 dưới đây, trước khi dùng lựa chọn trong kết quả.

**Nội dung WHY đề xuất:**

“Đối chiếu chương trình, đầu vào và cách chấm trước khi diễn giải độ lệch Nezha-OB. Dùng lại kết quả hợp lệ; trên dev kiểm riêng hai quy ước M4 mà bài chưa khóa đủ: ngưỡng metric và đơn vị đếm cảnh báo. Thiết kế 2×2 cho phép quan sát tác động riêng và tương tác, giữ các thành phần khác. Không chọn nhánh theo mức gần số công bố. Phương án chạy ngay CLI tác giả chưa phù hợp vì chưa xác định preprocessing sinh bảng và có loader ngoài miền dev. Các phép M4 chỉ phân xử quy ước M4; không xác nhận code sinh Bảng 2. Các kết luận P4 dựa trên M4 và việc chọn baseline P7 phụ thuộc giới hạn này.”

**Bản đồ ảnh hưởng:** đầu ra T-042 bổ sung bằng chứng; WHY ghi lý do phép kiểm; LOG/STATE ghi tiến độ; DECISIONS ghi đúng lời duyệt. Không thay số, trạng thái nghiệm thu hoặc nội dung T-026/T-032/T-034/T-041. Không sửa kế hoạch hạ tầng trong task này.

Không sửa `src/`, `data/`, môi trường, nguồn ngoài repo, tài liệu hoặc task khác. Nếu cần làm khác, trình đề xuất mới trước.

## Các bước

### A. Đối chiếu chỉ đọc — chưa chạy phương pháp

1. **Kiểm quyền, nguồn và manifest.**
   - Đọc SPEC/LOG nguồn và quyết định hiện hành.
   - Kiểm hash các file thực dùng.
   - Xác minh allowlist, code và môi trường có thật.
   - Dừng phần phụ thuộc khi thiếu nguồn hoặc hash không khớp; không tải bù tự động.

2. **Lập bảng bài–code–repo.**
   - Bao phủ bốn baseline đã chạy và hai trạng thái UNSUPPORTED.
   - Đối chiếu sâu SimpleRCA với bài FSE 2026 và MicroRank với Table 3 bài Nezha.
   - BARO/TraceRCA: ghi đúng nguồn có hoặc chưa có mốc Nezha-OB tương ứng; không lấy số phương pháp khác làm mốc.
   - Kiểm riêng AS@k, Top@k, Hit@k, mức service/pod, hòa, mẫu số và làm tròn.
   - Tách nhận định đã kiểm của khảo sát khỏi suy luận chưa kiểm.

3. **Đọc chuỗi bằng chứng đã có.**
   - Với MicroRank, đọc các can thiệp bộ chia, coverage/spectrum và phần còn mở; không chạy lại chỉ vì task mới.
   - Với M4, đọc điểm từng nguồn và phép đổi đơn vị đếm đã lưu; xác định phần Nezha-OB đã có đủ bằng chứng.
   - Với cửa sổ/mốc, dùng lại các bảng độ nhạy T-026.
   - Đối chiếu các dòng G2-H01/H02/H06/H07/H08/H16/H17/H18/H19 và dòng khác thực sự phụ thuộc Nezha-OB.
   - Không biến bằng chứng “tín hiệu nằm ở phía gọi” thành bằng chứng phương pháp đồ thị sẽ thắng.

**Đầu ra A:** bảng khác biệt và danh sách phép kiểm còn cần. Phần này không được kết luận nguyên nhân chỉ từ việc hai code khác nhau.

### B. Phép chạy trên dev — chỉ sau khi SPEC được duyệt

4. **Kiểm bộ bọc và đầu vào, trước evaluator.**
   - Từ chối ca ngoài allowlist trước mở telemetry.
   - Kiểm bằng fixture biết đáp án: timestamp/biên, ns–µs, ánh xạ, dữ liệu thiếu, hàng lặp, ca rỗng.
   - Đối chiếu độc lập đầu vào trên đủ 22 ca: số dòng N/A, bộ cột, mapping và membership.
   - Mọi khác biệt với Q-84/Q-85 phải được giải thích trước khi chấm.
   - Lỗi cần sửa ngoài phạm vi thì dừng nhánh và trình patch; không âm thầm “chữa” trong bộ bọc.

5. **Phân xử hai quy ước M4 trên cùng đầu vào.**

   | Nhánh | Ngưỡng metric | Đơn vị đếm |
   |---|---|---|
   | S0 | mean + 3σ, ddof=0 | events — bản chính T-026 |
   | S1 | mean + 3σ, ddof=0 | channels |
   | S2 | P95 tuyến tính của N | events |
   | S3 | P95 tuyến tính của N | channels |

   - Giữ nguyên trace P95×3, log keyword/ngưỡng 0, mapping, cửa sổ, missing policy, tập ứng viên và evaluator.
   - S0 dùng lại nếu đủ trung gian và khớp hash; nếu thiếu thì phát lại đúng cấu hình để thu trung gian.
   - Tối đa 22 ca × 4 nhánh; không quét thêm ngưỡng.
   - Lưu count và vote từng kênh, tổng metric/trace/log, nhóm hòa và thứ hạng.
   - Chỉ so S0↔S1, S0↔S2 và tương tác qua S3 để quy tác động; không lấy nhánh tốt nhất làm kết luận tái lập.

6. **Kiểm không dùng nhãn và chốt đầu ra.**
   - Hoán vị thứ tự hàng/cột, đổi locator nhưng giữ nội dung, chạy lại kiểm tất định.
   - Kiểm constant/NaN/all-zero/missing và nhánh dự phòng.
   - Dùng fixture N=A; đối chứng nền–nền thật chỉ khi có hai miền dev đủ dữ liệu. Nếu không đủ, ghi đúng thiếu hụt; không coi fixture là chứng minh nền sạch.
   - Ghi xong diagnosis và danh sách bản ghi rồi mới nối nhãn dev.

7. **Chấm và truy nguyên theo ca/ô.**
   - Chấm cùng quy tắc P3; giữ mọi trạng thái trong mẫu số.
   - Báo Hit@1/3/5, MRR, NDCG@5, trạng thái, hòa và tập ứng viên; khoảng bootstrap theo ô khi báo khoảng.
   - Đối chiếu toàn bộ ca tăng, giữ và giảm hạng; đọc cả đúng và sai trong cùng ô khi có.
   - Không có ca đúng cùng điều kiện thì ghi rõ. MicroRank không có ca đúng Hit@1 trong bảng chính; không dựng nhóm đối chứng không tồn tại.
   - Mỗi nhận định quan trọng ghi giải thích cạnh tranh và bằng chứng có thể bác bỏ nó.

8. **Kết luận và bàn giao.**
   - Trả lời từng giả thuyết, không cộng các cờ chồng nhau thành tỷ lệ nguyên nhân.
   - Lập bảng tác động tới từng hạn chế Nezha-OB: giữ căn cứ nào, giới hạn nào cần làm rõ, câu nào còn OPEN. Đây là đề xuất, không sửa tài liệu cũ.
   - Nếu cần pipeline tác giả: bàn giao revision/entrypoint, schema và trường thiếu, nguồn normal, cách bảo vệ dev/test, quyền dùng, môi trường, phép so và chi phí. Trình task nối tiếp chưa cấp mã.
   - Kiểm toàn bộ diff, file set, số và con trỏ nguồn; ghi LOG và prompt bàn giao.

Lệnh thực thi của bộ bọc mới sẽ được ghi trong LOG sau khi cài và kiểm; không trình một lệnh tác giả chưa an toàn như thể đã có thể chạy.

## Kiểm đúng đắn

- Hash nguồn trước dùng và hash đầu ra cuối; giữ riêng provenance code, dữ liệu và evaluator.
- S0 phải khớp score, tập ứng viên, nhóm hòa, trạng thái và hạng của T-026; khớp số tổng hợp một mình chưa đủ.
- Tính độc lập ngưỡng/phiếu/gộp điểm và độ đo; không dùng chính hàm đang kiểm làm oracle.
- Kiểm tham số và input chung giữa các nhánh. Nếu đổi thêm yếu tố thì không quy tác động riêng.
- Cận số học về full56 chỉ là phép tính có điều kiện; không phải thực nghiệm test.
- Đối với MicroRank, kiểm đúng provenance và giới hạn của can thiệp đã lưu; không gọi bản thay bộ chia là toàn bộ phương pháp gốc.
- Đối với mã tác giả SimpleRCA, ghi cả phần dùng quan hệ cha–con trong fallback; không gán nhãn “không đồ thị” cho mọi code cùng tên.
- Không dùng Type III = 0% của bài làm nhãn dev đã xác minh hoặc căn cứ loại đồ thị.
- Kết quả tăng mạnh phải kiểm trung gian, ca bị giảm và đối chứng âm; không chọn cách chấm làm số gần bài nhất.

## Tiêu chí xong

1. Bảng đối chiếu xác định rõ cái gì cùng, khác, có chủ đích hoặc chưa biết; mỗi điểm trọng yếu có nguồn trực tiếp.
2. Các nhận định KS-15/A.1/A.3 thực dùng đã được kiểm, sửa cách diễn đạt hoặc giữ OPEN.
3. Các phép A và B trong quyền được duyệt hoàn tất; kết quả cũ được dùng lại có provenance hợp lệ.
4. Mỗi kết luận nguyên nhân chỉ được bước xử lý và chuỗi bằng chứng; nếu chưa đủ thì chỉ rõ phép kiểm hoặc nguồn nào còn thiếu.
5. Báo được tác động tới những ca đúng lẫn sai, từng ô và từng nhóm quan trọng; không chỉ báo trung bình.
6. Phân biệt rõ:
   - nguyên nhân đã xác nhận trong pipeline repo;
   - khác biệt đã xác nhận nhưng chưa đo tác động;
   - độ nhạy M4;
   - phần chênh với bảng công bố còn chưa giải thích.
7. Có khuyến nghị có điều kiện cho Minh: sửa lỗi; giữ giao thức và đổi phạm vi so sánh; ghi giới hạn dữ liệu/phiên bản; hoặc tiếp tục truy nguồn/chạy bổ sung.
8. Không mở test, không rò nhãn, không đổi nguồn P3 và không tự chọn baseline mới.
9. LOG đủ bàn giao; diff và file set đúng phạm vi; có prompt Claude theo mẫu.

“Chưa phân xử” là đầu ra hợp lệ khi bằng chứng cần thiết không có hoặc dữ liệu không phân xử được, kèm phương án xử lý. Chưa chạy xong vì hết thời gian hoặc thiếu file local chưa phải bằng chứng rằng câu hỏi không thể phân xử.

## Không làm

- Không tái lập điểm toàn bộ 56 ca khi 34 ca test còn khóa. Điều này để lại giới hạn về độ khớp đầy đủ với bảng công bố.
- Không chạy chế độ tự phát hiện trên trace/log Nezha; không đánh giá vùng ảnh hưởng thật.
- Không sửa code baseline chính, đổi giao thức V2, thay bảng P3 hoặc sửa các task đã đóng.
- Không thêm Node*, đoán ownership, giả status, đổi đồng hồ hoặc dùng construct_data làm nền sạch.
- Không thiết kế hay khẳng định lợi ích phương pháp đồ thị trong task này.
- Không chạy trọn pipeline SimpleRCA/MicroRank tác giả khi chưa xác định hợp đồng đầu vào và miền dev an toàn.

**Phần nối tiếp cần thiết nếu còn OPEN:** dựng/kiểm pipeline tác giả trên đúng dev, gồm chuyển đổi schema và nguồn normal; so cùng đầu vào với repo rồi thay từng yếu tố. T-042 phải nêu chính xác phần còn thiếu. Chưa có code/config sinh bảng hoặc kết quả tác giả đúng ca thì cần Minh quyết việc lấy nguồn/hỏi tác giả. Không tự gửi thư.

Các quyết định phụ thuộc:

- Baseline và biến thể nào dùng ở P7.
- Hạn chế Nezha-OB nào đủ làm căn cứ chọn thành phần P6.
- Có giữ mục tiêu “cải thiện Nezha-OB” và hiểu nó theo giao thức nào.
- Có cần thêm dữ liệu hoặc quan sát để phân xử.
- Có cần sửa adapter, rồi chạy lại những kết quả nào.

## Chi phí ước lượng

**Đã có mốc lịch sử:** T-026 ghi tổng thời gian nguồn của nhánh chính 22 ca: SimpleRCA khoảng 141 giây, MicroRank khoảng 128 giây. Đây là chi phí bản cài hiện có, không phải mã tác giả. Nguồn: `D:/RCA-flashticket/results/T-026/runs/full-001/summary-continued-001.json`, `runs[*].cost`.

**Ước lượng chưa kiểm cho T-042:**

- Công đọc, cài bộ bọc, kiểm và báo cáo: 3–5 giờ, mục tiêu một phiên.
- Máy local: khoảng 20–60 phút tổng, gồm đọc/hash dev, fixture, thu trung gian và tối đa 88 ca–nhánh M4.
- RAM: dự kiến dưới 2 GB; đĩa đầu ra tổng hợp dự kiến dưới 300 MB.
- Tải dữ liệu/code/môi trường: 0; không EC2, không GPU; không phát sinh tiền máy.
- Dùng lại trung gian và đọc mỗi ca một lần cho các nhánh để giảm I/O. Không chạy tác vụ nặng song song khi đo thời gian.

Đây là dự toán, chưa là phép đo. Pilot không nhãn xác nhận chi phí trước lô. Nếu một lượt dự kiến vượt một giờ hoặc phần cần làm không vừa một phiên thì trình tách phạm vi; không giảm kiểm khoa học để vừa thời gian. Không dùng ngân sách Q-40 như quyền tự chạy vượt giới hạn phải báo trước.

Nhánh dựng môi trường/pipeline tác giả nối tiếp chưa đủ thông tin để chốt chi phí; dự kiến cần một phiên riêng. T-042 phải cập nhật ước lượng từ hợp đồng thực tế, không lấy 5,05 giây trong bài làm ngân sách.

## Rủi ro và điều chưa chắc

- **Chưa kiểm:** hai quy ước metric giải thích được bao nhiêu ca sai. Có thể thay hạng nhưng làm hỏng ca đúng; khi đó không phải cách sửa chung.
- **OPEN:** code/config/preprocessing sinh Bảng 2. Ba snapshot cùng tên chưa giải quyết provenance này.
- **OPEN:** chương trình MicroRank và cấu hình được dùng trong bảng Nezha.
- **OPEN:** độ tương đương release, full cohort và cách chấm của tác giả.
- Nền ngắn, clock, recovery và tải có thể tương tác; thiếu quan sát vật lý không được thay bằng suy đoán.
- Dev đã được phân tích nhiều lần. Kết quả chỉ là chẩn đoán trên dev; lợi ích khái quát phải đánh giá sau khóa thiết kế.
- Nguồn local ngoài repo có thể thiếu trên máy khác. Manifest và đường dựng lại phải được ghi; không dùng scratch như nguồn sự thật độc lập.
- Quyền dùng dữ liệu Nezha theo Q-59; giấy phép code tác giả SimpleRCA phải ghi đúng phạm vi.

## Prompt bàn giao

Dùng Prompt chung + khối Soát SPEC + khối G2 trong `D:/RCA-flashticket/docs/review-prompt.md`. Bản prompt cho Claude nằm ở mục “Prompt Claude” trong `D:/RCA-flashticket/tasks/T-042-doi-chieu-baseline-nezha-ob/LOG.md`; Minh chọn chuyển. Chưa có quyền ghi bản phản biện; Claude chỉ trả lời trong chat. Prompt phiên Codex mới cũng nằm trong LOG: giữ vai trò người làm, tự soát trước theo Q-189; bất hợp lý thì dừng báo Minh, không tự sửa SPEC; nếu không có thì triển khai ngay trong phạm vi, không cần chờ Claude soát SPEC. Tự soát không thay phản biện chính thức.

## Bổ sung đã được Minh duyệt ngày 24/10/2026 — Q-191

Đây là sửa SPEC có quyền mới, sau lượt đáp phản biện; không suy quyền từ Q-190. Bản SPEC trước bổ sung nằm tại results/T-042/runs/normal-source-001/before/tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md. Không đổi code hoặc kết quả cũ, không tự nghiệm thu.

### Câu hỏi và phép phân xử bổ sung

- H-N (CANDIDATE): nguồn nền trước tiêm của P3 góp phần gây kết quả OB thấp. So riêng nguồn N theo phút normal do converter xác định, giữ A=[t,t+300s), native clock Time của metric P3, kênh, mapping, cấu hình và evaluator. Đây là phép đổi nguồn/độ dài/độ phủ N cùng nhau, không chứng minh riêng độ sạch, số mẫu hoặc đúng toàn bộ pipeline lịch sử. Chạy M4 S0, main M0 literal Duration và repaired MicroRank sham; không chọn nhánh theo điểm.
- H-F2 (CANDIDATE): N trước tiêm không ổn định, có thể do phần hồi phục lỗi trước. So hai mẫu đầu với hai mẫu cuối của mỗi kênh trong năm mẫu N của 22 ca; bỏ mẫu giữa theo kế hoạch trước chạy. Nếu log/trace đủ cả hai nửa thời gian thì lưu thống kê hai nửa, nếu không ghi thiếu. Kết quả chỉ cho thấy thay đổi, chưa phân biệt hồi phục với tải/nhịp đo/giải thích khác.
- H-N được hỗ trợ trong cấu hình kiểm khi chuỗi N -> thống kê/ngưỡng -> nhóm/phiếu/điểm -> hạng đổi theo dự đoán. Không đổi trên đầu vào đủ điều kiện thì loại tác động ở cấu hình đó; thiếu mẫu/operation hoặc fallback thì giữ phần tương ứng OPEN, không coi là bác bỏ.
- MicroRank nhận N/A tách riêng trong bộ bọc task; không đổi timestamp để ép N trước mốc. Kiểm tương đương bộ bọc với hàm gốc trên fixture và một ca dev trước khi dùng kết quả. Không sửa lõi dùng chung, không mở sweep.

### Quyền dữ liệu bổ sung

Chỉ thêm hai khoảng UTC: [2022-08-22T03:51:00Z,03:52:00Z] và [2022-08-23T17:00:00Z,17:01:00Z] trong online-boutique/construct_data. Đây là miền normal ứng viên theo filename loader, chưa xác nhận sạch.

Allowlist riêng chỉ gồm metric front_service và các pod có alias P3 theo ngày, log 03_51/17_00 và trace 03_51/17_00, ghim hash/size từ manifest tải T-008. Không mở toàn bộ ngày để phân tích; đọc timestamp trước, chỉ giải mã giá trị đo trong miền được phép. Không dùng dependency, traceid hoặc nguồn/dataset khác. Metric giữ Time; TimeStamp converter khác được nêu là giới hạn, không âm thầm đổi clock. Trace/log giữ timestamp và Duration nguồn, duplicates và alias P3; trace giữ giới hạn end của reader P3 trong miền N, A giữ đúng membership đã duyệt. Không dịch, nội suy, kéo dài, bổ sung dữ liệu A cho N hoặc giả severity. Nhánh native main fallback A do thiếu N phải được giữ và đếm rõ; không gọi nó là bằng chứng độc lập về nền N.

### Phạm vi ghi, chi phí và tiêu chí xong bổ sung

- Được sửa SPEC này đúng bổ sung trên; nối DECISIONS Q-191, WHY-54 và LOG; chỉ cập nhật dòng T-042 STATE.
- Đầu ra bổ sung duy nhất: results/T-042/runs/normal-source-001/ gồm bản trước, nguồn/allowlist/plan, script riêng, fixture, mọi lượt kể cả hỏng, audit, trung gian, diagnosis trước nhãn, evaluator, đính chính/phản hồi, báo cáo, manifest và prompt. Không lưu payload telemetry thô.
- Ước lượng chưa kiểm: dưới 30 phút máy sau thăm dò; 2–4 giờ chuẩn bị và phân tích. Đầu ra mới tối đa 20.000.000 byte. Dừng trình nếu dự kiến vượt ngân sách hoặc một lượt vượt một giờ; không tải/cài hoặc sửa môi trường.
- Tiêu chí xong: kiểm nguồn/hash; kiểm số mẫu/phủ và fallback; fixture/bộ bọc đạt; có kết quả từng ca/kênh/pool/operation đủ để lần cơ chế, giữ mọi trạng thái lỗi; chấm sau freeze bằng evaluator P3 và đối chiếu độc lập; diễn giải từng giả thuyết và phần nguồn còn thiếu, không chọn baseline. Kiểm diff/file set; LOG đủ bàn giao, dòng T-042 chờ phản biện và prompt chuẩn cho Claude. Không đóng task/G3/test.
