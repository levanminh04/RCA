# T-017 — SimpleRCA cài lại theo mô tả bài (M4)

- **Trạng thái:** tự duyệt theo ủy quyền của Minh ngày 04/10/2026; khóa trước khi chạy dữ liệu dev.
- **Người làm:** Codex. **Người phản biện:** Claude.
- **Thuộc gói MRP:** P1. **Cổng:** G1.
- **Intent:** EXECUTE. Phạm vi, vai trò và ngoại lệ tự duyệt là USER_CONFIRMED trong prompt. Các tham số dưới đây là lựa chọn triển khai của task, không phải quyết định G1/P3 của Minh.

## Mục tiêu

Trả lời nhận xét đầu tiên của cô: chưa sâu kỹ thuật từng phương pháp. Cài độc lập SimpleRCA theo §3.1.2 PDF mới nhất, giải thích từng bước bằng công thức và ví dụ đối chiếu độc lập. Tách luật Type I/II của bài khỏi thuật toán SimpleRCA. Phục vụ đầu vào và điều kiện chạy ở G1, RQ1; không dùng kết quả này để thiết kế đồ thị hay kết luận P4.

## Đầu vào

- Đã đọc toàn bộ AGENTS, STATE, LESSONS, review-prompt, mẫu SPEC/LOG, WHY, DECISIONS, DT18 và hướng dẫn cô; MRP §2–7. T-017 chưa có đầu ra cũ.
- `results/T-001/danh-sach-phuong-phap.md` §3a,6,7,8,9. T001 là nguồn cần đối chiếu, không thay bài.
- PDF arXiv 2510.04711v2 (bản mới nhất xác minh 04/10), tìm bản FSE26 chính thức. Đọc cả PDF, xem ảnh bảng 2/3; ghi số công bố trước mọi lượt chạy.
- Code đúng ba revision T001 §9 và metadata/code Zenodo17105974. Chỉ đọc đối chiếu. Không chép code tác giả vào bản cài; kiểm license và lưu chứng cứ. Không tải telemetry artifact.
- 30 thư mục dev `data/rcaeval/re2tt_*` hiện có. Danh sách allowlist ghi vào manifest trước mở dữ liệu. Hai ca OB đã cho phép chỉ dùng khi thật sự cần schema; không chạy dataset mới.
- T005/T006/T007: kiểm đầu ra thật và dùng lại dữ kiện môi trường, cấu hình cửa sổ và giới hạn. T002 run-002 dùng lại census/schema sau kiểm. Soi nguồn T000–T012, sửa trong T017 nếu tìm được bằng chứng; không sửa task cũ.
- Mốc tiêm từ metadata đã tải `D:/RCA-ext/dl/rcaeval-inject/<dev>/inject_time.txt`, chỉ adapter biết trước mốc nhận mốc này. Nhãn root chỉ đọc sau khi kết quả xếp hạng đã ghi. Lõi không nhận tên ca, path, loại lỗi, nhãn, đồ thị hoặc inject_time.

## Đầu ra

- `src/simplerca/`: lõi cài độc lập, schema/adapter, test tổng hợp có đáp án biết trước, hướng dẫn chạy.
- `results/T-017/ho-so-simplerca.md`: đủ 7 mục P1 + đường nhãn + đầu vào hệ khác.
- `results/T-017/type-i-ii.md`, `so-cong-bo.csv`: định nghĩa chính xác theo PDF, tỷ lệ từng dataset, điểm và thời gian bảng 2. Không tính Type trên dataset mới.
- `results/T-017/doi-chieu-code.md`: khác biệt ở đúng revision, file:dòng, hậu quả; license và artifact inventory.
- `results/T-017/vi-du-tinh-tay.md` và script độc lập không import lõi; bảng trung gian và so từng score.
- `results/T-017/kiem-dung-dan.md`, `moi-truong.md`, `runs/`, `scripts/`, manifest, `tieu-chi-xong.csv` và inventory cuối.
- Bốn file bắt buộc: `yeu-cau-dau-vao.csv` đúng 17 cột user quy định; `ca-da-chay.csv`; `dinh-chinh-task-cu.md`; `de-xuat-tai-lieu-chung.md`. Không có nội dung ghi “không có”.
- Kết quả từng ca dev để kiểm tái lập bộ phận. Không gọi điểm 30 ca là tái lập điểm 90 ca. Chỉ so từng ca tác giả nếu artifact có kết quả và đã lọc allowlist trước đọc/in.

## Phạm vi ghi và bản đồ ảnh hưởng

Chỉ ghi `tasks/T-017-simplerca/SPEC.md`, `LOG.md`; `results/T-017/`; `src/simplerca/`; `D:/RCA-ext/work/T-017/`; môi trường mới `D:/RCA-ext/envs/T-017-*` nếu cần gói mới; đúng một dòng T017 trong STATE. Đây là các đường dẫn và outcome Minh đã cho phép trong prompt.

Lõi và adapter chỉ phục vụ SimpleRCA; chưa tích hợp vào runner chung. Kết quả là đầu vào G1. Các lựa chọn quan trọng chưa có WHY ghi nháp nguyên văn trong de-xuat-tai-lieu-chung và đánh dấu “(chờ WHY, xem de-xuat-tai-lieu-chung.md)” ở nơi dùng. Không đổi quyết định chung hay file task khác.

STATE: đọc sát lúc ghi, thay đúng chuỗi dòng T017 hoặc chèn sau dòng cuối bảng; dùng cập nhật byte có kiểm phiên bản để tránh ghi đè thay đổi đồng thời. Đọc lại và so mọi dòng ngoài T017. Không sửa “Task đang mở”, header ngày hay các dòng task khác.

## Các bước theo phụ thuộc

1. **Nguồn và mốc công bố**, không phụ thuộc code cài: đọc PDF và ghi bảng 2/3; inventory code/Zenodo/license; kiểm ba revision. Kiểm: script nguồn lưu SHA256, URL, byte và revision; đối chiếu ảnh PDF bảng. Nguồn tải dự kiến <30 MB, đã báo trong LOG.
2. **SPEC và lựa chọn**, phụ thuộc mô tả §3.1.2 và luật repo: khóa tham số, rule chọn ca, các edge case dưới đây; tự phản biện trước chạy. Kiểm: đọc lại SPEC, bảng phủ SL24–33 và REVIEW T003 R1; ghi sửa SPEC trong LOG.
3. **Lõi và test**, phụ thuộc bước 2, độc lập audit task cũ: chỉ dùng số đo đã chuẩn hóa cùng hai cửa sổ. Kiểm: `python -m unittest discover -s src/simplerca/tests -v`; đáp án tay cho metric/trace/log, boundary, tie và permutation. Không dùng code tác giả.
4. **Adapter và môi trường**, phụ thuộc schema có sẵn và bước 2, có thể làm cùng bước 3: ghim phiên bản, đọc parquet trong allowlist, tên service và thời gian. Kiểm: schema asserts, kiểm không có label/path ở chữ ký lõi; snapshot input hash. Không ghi env/src có sẵn.
5. **Chạy dev**, phụ thuộc 1,3,4: primary trên 30 dev, repeat và column permutation trên hai ca đầu theo lexicographic (thứ tự từ điển), normal/normal trên cùng hai ca. Ví dụ tính tay chọn ca đầu allowlist theo lexicographic trước kết quả, không chọn theo thứ hạng. Kiểm: output nonempty nếu có tín hiệu, không fallback, every service score = tổng thành phần, stable ties, repeat/permutation bằng nhau; giữ failed run và progress từng ca. Ước lượng tổng trước chạy, dừng nếu dự kiến >1 giờ/lượt.
6. **Tính độc lập và độ nhạy lựa chọn**, phụ thuộc 5: script thứ hai chỉ đọc dữ liệu đầu vào, không import src; so mỗi ngưỡng, count, percentile và score trên ca ví dụ. Chạy cấu hình phụ đã khóa trên ca ví dụ: metric P95 thay 3σ; aggregation channels thay events; log threshold 1 và 10; cửa sổ ±600s thay ±300s; trace factor 2 và 4. Không chọn winner theo nhãn. Kiểm `allclose` 1e-10 cho float; counts/ranks bằng tuyệt đối.
7. **Hồ sơ và audit**, phụ thuộc nguồn, kết quả và thông điệp hai phụ tá: viết hồ sơ, lỗi task cũ có script/chứng cứ; nháp tài liệu chung. Kiểm: mọi số trỏ file, mọi khác bài ghi lý do/phương án/ảnh hưởng, Type không lẫn ranking, đủ input CSV.
8. **Bàn giao**, phụ thuộc tất cả: kiểm complete diff và inventory, bảng tiêu chí xong từng dòng, mọi việc trong giới hạn làm ngay; LOG 6 ý + A–H, prompt chung và G1 nguyên văn chỉ điền trung tính; STATE chờ phản biện. Kiểm script inventory và prompt equality, status không commit/push.

## Lựa chọn triển khai khóa trước dev

Tất cả lựa chọn dưới đây **chờ WHY, xem de-xuat-tai-lieu-chung.md**; không gọi là tham số chính xác tái lập tác giả.

- Hai cửa sổ ±300s quanh mốc biết trước, normal `[t-300,t)`, incident `[t,t+300)`; theo cấu hình kiểm đã có T005, chưa chọn độ dài P3 (Q54). So ±600s trên ca ví dụ để thấy phụ thuộc.
- Metric: ngưỡng upper-tail `mean(normal)+3*std(normal, ddof=0)`; mỗi giá trị hữu hạn vượt **strictly >** là một alert (cảnh báo). Không trị tuyệt đối vì bài chỉ nói vượt; không nhân trọng số. Giữ mọi cột metric hợp lệ, cả latency-50 và latency-90; không chọn theo lỗi/root. Phương án P95 và mỗi channel một phiếu kiểm riêng; bài chưa khóa đơn vị đếm và lựa chọn threshold.
- Trace: một phiếu/service khi P95(duration incident)>3*P95(duration normal), cùng đơn vị; không dùng parentSpanID, graph hay statusCode. P95 tuyến tính như numpy default, threshold strict. Không tự thay P95 bằng p90 tuyệt đối.
- Log: case-insensitive substring ERROR/FAIL/EXCEPTION; mỗi dòng khớp ít nhất một từ chỉ đếm một lần; một alert/service nếu count incident>0. 0 là ngưỡng cấu hình tối thiểu, không suy từ nhãn; bài không cho số. Cấu hình 1/10 kiểm riêng, không chọn theo accuracy. Không coi đây là bộ phát hiện spike đã hiệu chỉnh false-positive.
- Service score = tổng alert metric + một phiếu trace + một phiếu log. Ứng viên là union service quan sát được từ cả ba tín hiệu. Service không quan sát không bịa điểm 0; thiếu normal của một metric/trace đánh dấu unavailable, không fallback. Missing log modality=unavailable, log rỗng hợp lệ=0, phân biệt hai trạng thái.
- Hòa điểm: trả tie groups (nhóm hòa) và thứ tự tên deterministic chỉ để hiển thị. Chấm Hit@k fractional cho tie cắt ranh giới, báo thêm optimistic/pessimistic; không coi thứ tự tên là bằng chứng. Mọi score=0 thì abstain (không có ứng viên có chứng cứ) và không tính top1 có nghĩa.
- Tên service chỉ chuẩn hóa cơ học: metric tách ở `_` cuối (tên metric schema RCAEval không có `_`), log/trace bỏ hậu tố pod dạng Kubernetes đã kiểm trên schema, giữ prefix `ts-` nếu nguồn có. Mọi alias phải tường minh và độc lập nhãn; unknown alias báo unavailable/không đoán. Kiểm collision và synthetic alias.
- Không ffill dữ liệu thiếu mặc định; bỏ nonfinite khỏi thống kê và count, lưu counts missing. Normal≥2 điểm hữu hạn/metric; trace≥1 span mỗi phía; log không cần normal để ngưỡng fixed. Không có evidence hợp lệ thì lỗi input hoặc abstain có trạng thái rõ.

## Edge case và phép kiểm

| Ca biên | Cách kiểm | Cách xử lý và hậu quả |
|---|---|---|
| Không có log | None so với bảng log rỗng synthetic; inventory dev | Thiếu modality ghi unavailable; không tự sinh log, không loại ca |
| Tên khác ba nguồn | Synthetic ts-prefix/pod suffix, kiểm mapping dev | Alias schema tường minh, không nhận root; collision lỗi |
| Đúng ngưỡng | Synthetic bằng/vượt 3σ, trace factor, log count | Strict >; không phiếu ở equality |
| Hòa điểm | Synthetic 2 service cùng score | Tie group, lexical display, fractional Hit |
| Service không có dữ liệu | Synthetic một service chỉ log/trace, absent root ở scorer | Union thực quan sát; absent không lén bổ sung từ nhãn |
| Mốc tiêm | Synthetic điểm đúng t; inspect adapter/core | Chỉ chia cửa sổ chế độ biết mốc, không tự phát hiện |
| Normal rỗng/1 điểm | Synthetic | Channel unavailable; mọi channel thiếu thì input lỗi rõ |
| Std/P95 bằng 0 | Synthetic constant | Không floor/epsilon tùy tiện, strict positive incident kích hoạt |
| NaN/inf hoặc duration âm | Synthetic và counters dev | Nonfinite bỏ có đếm; duration âm lỗi input |
| Normal/normal | Synthetic sạch và hai ca dev | Ghi false alerts nếu có; score không chứng minh nguyên nhân. Không sửa threshold theo kết quả |
| Cột đảo thứ tự | Synthetic và hai ca dev | Điểm/tie groups không đổi; cấm fallback thứ tự cột |
| Log nhiều keyword một dòng | Synthetic mixed case | Một count/dòng, không ba phiếu |
| Timestamp khác đơn vị | Schema và epoch range synthetic | Metric giây, trace microsecond epoch, log theo schema; duration unit không cần đổi cho ratio |
| Không có service/vote | Synthetic | Abstain; không gán top1 lexical làm root |
| Dữ liệu ngoài allowlist/artifact result | Test guard đường dẫn, inventory trước extract | Từ chối trước đọc; lọc case list trước đọc/in kết quả tác giả |

## Kiểm đúng đắn

- Tra bảng 2/3 trước chạy; lưu literal CSV số công bố. RE2-TT 0,80 là 90 ca, không tái lập đủ vì 60 khóa. Không có dataset đầy đủ cùng bài trong allowlist thì ghi rõ kết luận tái lập bị giới hạn, không biến thiếu dữ liệu thành lệch thuật toán.
- Synthetic known-answer kiểm công thức từng modality; không chỉ “không lỗi”. Repeat/permutation trên hai ca và độc lập script trên ca ví dụ; deterministic, không seed lựa chọn.
- Đầu ra không rỗng khi có alert; allzero abstain. Không có fallback trả cột. Ranking trùng lexical có thể là tie hợp lệ; kiểm score/tie để phân biệt, không loại kết quả chỉ vì nhìn giống.
- Normal/normal: sạch synthetic phải không có cause; thực dev giữ mọi alert và báo mức kiểm không đạt nếu có positive ranking. Không dùng nhãn sửa detector. Đây chỉ là heuristic RCA biết mốc, không có độ hiệu chỉnh ý nghĩa thống kê.
- Soi count từng modality, max/mean/std, quantile, channel unavailable, ties, từng service và từng ca. Score chênh lớn phải giải thích do counts/window/channels, không gọi “giới hạn” mà chưa lần nguyên nhân.
- Bỏ kiểm full 90 ca, dataset mới và Type tự tính vì phạm vi dữ liệu; yếu đi kết luận tái lập công bố/generality. Bỏ thời gian chính thức vì laptop chạy nhiều phiên; elapsed chỉ tiến độ. Không bỏ phép kiểm rẻ được phép nào.

## Tiêu chí xong

1. Có bản cài độc lập/test known-answer và tất cả ca biên trên được kiểm hoặc ghi unavailable thật với bằng chứng.
2. Có đủ 9 mục hồ sơ, công thức, file:dòng tham số, 1 ví dụ dev independently matched từng score; rule chọn ca ghi trước chạy.
3. Đã đọc PDF đầy đủ, bảng 2/3 nhìn ảnh, ghi Type definition/label use/tỷ lệ từng dataset riêng; không tự tính Type trên dữ liệu mới.
4. Ba revision/license và Zenodo được kiểm, khác biệt có nguồn; provenance của số 0,80 chỉ xác nhận nếu có chứng cứ.
5. 30 dev primary và các kiểm rẻ chạy theo allowlist, run logs/input hash/ca-da-chay đầy đủ, không mở khóa; repeat/permutation đạt; normal control báo thật.
6. Bốn file bắt buộc đúng schema; mọi lựa chọn quan trọng có draft WHY và chờ WHY tại nơi dùng; audit T000–T012 có phạm vi/bằng chứng.
7. Mọi chưa kiểm thật sự ngoài giới hạn, ghi giả định/khi sai/phép kiểm tiếp; LOG 6 ý/A–H/prompt nguyên văn; inventory đủ cả file ngoài repo; STATE chỉ dòng T017 chờ phản biện.

## Không làm

Không EC2, locked, archive repo; không tải/giải nén RE2-TT ngoài 30 dev; không P3 toàn dataset, P4 phân tích hạn chế bằng số, thiết kế đồ thị, chọn split/window P3, commit/push hay gửi tin ngoài. Không sửa env/src hiện có hoặc tài liệu/task chung ngoài dòng STATE.

## Chi phí ước lượng

Tổng nguồn <30 MB; môi trường mới nếu cần ~100 MB, ghim version; mọi lượt dự kiến <30 phút, tổng đọc/chạy dev/test <45 phút CPU trên 30 ca, RAM xử lý tuần tự từng ca <2 GB. Laptop có tới 8 phiên khác nên không đo thời gian chính thức. Hai subagent chỉ audit nguồn/task cũ, không benchmark; không deep research. Dự kiến vượt 1 giờ/lượt thì không chạy, ghi Cần Minh quyết. Không tải dữ liệu mới.

## Rủi ro và điều chưa chắc

Code công bố có thể không định danh được cấu hình sinh bảng 2. Bài bỏ ngỏ aggregation/log threshold/window; kết quả phụ thuộc lựa chọn M4, vì vậy không gọi số dev là số tác giả. Normal/normal có thể có alert ngẫu nhiên: phép kiểm nhằm phát hiện điều đó, không đảm bảo mọi normal dữ liệu thực dưới 3σ. Liên hệ Type I/II với độ khó là luận điểm tác giả, chưa là kết luận nhân quả của task.

## Thay đổi trong lúc làm

- 04/10, trước lượt chạy dev: footer và epoch range ca cpu_2 cho log timestamp là giây, không phải millisecond. Adapter dùng seconds và range guard. Đây là thực hiện “theo schema” đã khóa; không đổi threshold/window theo kết quả. Duration unit vẫn không cần xác nhận để chia percentile cùng đơn vị. PDF FSE26 tìm được (Article FSE072, DOI trong manifest): bảng 2/3 giữ nguyên arXiv; dùng FSE làm nguồn chính cho bảng.
- 04/10, run-dev-001: ca đầu đã có kết quả hợp lệ; ca thứ hai lỗi do nguồn metadata bên ngoài chỉ có một số ca. Mốc dùng file inject_time.txt ngay trong từng thư mục dev đã được phép, không tải hay mở ca khác. Giữ failed run; run-dev-002 tiếp từ ca thứ hai, dùng lại ca đầu. Progress run001 dùng naive host time; run002 ghi rõ UTC+07:00 (Asia/Saigon).
- 04/10, run-dev-002 cũng thiếu metadata local ở ca thứ hai. Không chạy lại mù: kiểm manifest T002 đủ nguồn và hash 30 file mốc. Tải riêng metadata 30×10 byte từ đúng allowlist/revision manifest, verify SHA256 trước lượt tiếp; không tải telemetry. Dùng lại kết quả hợp lệ ca đầu, giữ cả hai lượt hỏng. Các run tiếp nhận mốc từ WORK/injection đã xác minh. Các lựa chọn khoa học không đổi.
- 04/10, soi trung gian run001/003 tìm regex tên pod gộp nhầm các service database hợp lệ (ví dụ ts-assurance-mongo→ts). Sửa lỗi adapter theo yêu cầu mapping không đoán: mặc định giữ nguyên; chỉ alias tường minh từ schema. Không đổi ngưỡng/aggregation. Lượt cũ giữ nguyên nhưng không dùng làm số cuối; run-dev-004 chạy lại30 theo lý do(c): bằng chứng đầu ra mapping sai. Normalized input v2 giữ thư mục riêng theo mã run, không ghi đè input cũ. Bổ sung test tên database và alias ba nguồn. Guard kiểm resolve() của chính thư mục ca để chặn đường dẫn symlink ngoài allowlist.
- 04/10, mục Đầu ra ghi nhầm 17 cột: danh sách nguyên văn Minh đưa có 16 cột. Dùng đúng 16 tên và thứ tự đó; đây là sửa lỗi đếm, không thêm/bớt trường yêu cầu. Log sensitivity trên ví dụ không có log chỉ kiểm được invariance khi thiếu modality. Kiểm bổ sung ngưỡng 0/1/10 trên ca thứ hai trong allowlist có log, không chọn cấu hình theo thứ hạng; các ngưỡng đã khóa trước dev. Ước lượng dưới 1 phút tổng, dùng lại normalized input của run004 cho primary và đọc lại đúng ca thứ hai đã chạy để kiểm ngưỡng.
- 04/10, rà cuối bổ sung kiểm collision/cycle alias và cột metric trùng; collision giữa hai service metric phải lỗi, alias trace/log về một service metric vẫn hợp lệ. Guard từng file nguồn phải resolve ở chính ca đã phép, không chỉ guard thư mục. Kiểm tổng hợp path ngoài allowlist và file trỏ ngoài trước đọc; kiểm resolve của toàn bộ file30dev. Dev dùng aliases=None nên không đổi số; kiểm baseline đọc lại ca thứ hai phải bằng run004 sau thay đổi này. Không chạy lại30 khi chưa có bằng chứng số bị ảnh hưởng.
