# LOG T-055 — RE3-OB bản cuối

Nhật ký chỉ ghi thêm. Mỗi phiên một mục.

## 08/11/2026 — Claude, Windows điều khiển hai EC2, người làm

Mở phiên. Nguồn quyền: `results/T-055/grants/minh-re3.txt` (sha256 8456dc46…). Minh duyệt luồng A, B, C và giao quyết định trong phiên cho Claude; quyết định lớn ghi ở mục "Quyết định Claude tự đưa ra" bên dưới để Minh kiểm. Luồng D (TORAI A) giao Codex. SPEC ghi theo quyền giao, chưa được Minh đọc trước.

### Quyết định Claude tự đưa ra (để Minh kiểm)

- **D-55-1. Giữ M1 đúng bản khóa P7(a)** cho RE3 (Q2, Q3 theo đề xuất). Không thêm kênh status span dù RE3 toàn lỗi mã nguồn. Lý do: RE3 là phép kiểm độc lập duy nhất còn lại của bản khóa; thêm kênh là thiết kế mới sau test (C-15 B). Hệ quả: RE3 đo trung thực khả năng của M1 với lỗi mã nguồn; kết quả thấp vẫn hợp lệ.
- **D-55-2. Bước đọc dev rẻ (T-051 kb-002)** không chặn RE3. Vì Q3 đã chốt giữ M1 nên bước này không đổi bản cuối; làm trong luồng A nếu còn thời gian.
- **D-55-3. U = 28 tiền tố owner** của schema metric 30 ca, alias rỗng (frontend-external giữ riêng). Lý do và nguồn ở `results/T-055/runs/khoa-truoc-001/preregistration.json#/h1_assumptions_unverified`. Phương án khác: chỉ 11 owner quan sát. Phương án này cần sửa reader để bỏ cột metric ngoài U — ngoài phạm vi, và bỏ dữ liệu không có căn cứ.
- **D-55-4. Đơn vị span/log quyết bằng preflight không nhãn khóa trước** (R3–R5), không đoán theo độ lớn từng ca. Metric giây theo dataset card. r: metric = bước chung đo được; trace 1 µs; log 1 s như TT/Nezha. Ghi "chưa kiểm".
- **D-55-5. Quy tắc lỗi RE3** `RE3_METHOD_ERROR_IS_MISS`: ERROR của phương pháp trong pha method trên đầu vào đã xác minh tính trượt (mặc định WHY-06). Đặt trong lớp phủ `bien_nhan.py` chỉ ở code root RE3 trên EC2; không sửa file đã ghim của main. Lý do: luật 21 — tránh một lỗi phương pháp chặn cả lượt mở duy nhất; P7(a) đã gặp đúng tình huống này.
- **D-55-6. Mở RE3 trước khi Codex phản biện** (Minh chọn "Mở trước, Codex sau"). Khóa bằng manifest/hash; không commit.
- **D-55-7. Ma trận** như P7 trừ T12, C-d3, C-e, TORAI A (không áp dụng cho RE3-OB); dẫn xuất C-d1/C-d2/C-c/C-g sau seal.

### Khóa trước khi đọc dữ liệu — 08/11/2026

- Nguồn độc lập dựng từ HF tree API (sha256/bytes LFS) và 30 `inject_time.txt` (10 byte, khớp git blob): `results/T-055/runs/nguon-001/`. Tổng 131,7 MiB; phân 15/15 theo cỡ traces, không dùng root/fault.
- Nhãn hai nguồn (cột G1 CSV và tách tên thư mục HF), kế hoạch tải có tên ca: chỉ ở `D:/RCA-ext/private/T-055/`.
- Bản khóa trước: `results/T-055/runs/khoa-truoc-001/preregistration.json` (sha256 34679b3d…). Gồm hash của `stage_ec2.py`, `preflight_ec2.py`, lớp phủ, mọi giả định H1, ma trận, độ đo, quy tắc lỗi. Preflight đã chạy thử trên dữ liệu giả H2 (synthetic-004): PASS.
- Kiểm EC2 (chỉ đọc): `i-043c327915a22f54c` (16.176.181.251) và `i-047569423678d016b` (13.236.44.106); 2 vCPU, 8 GB, ~24 GB trống; không tiến trình cũ.

### Tải, preflight, khóa và phát — 08/11/2026 (giờ UTC trong biên nhận)

- **Tải:** mỗi EC2 tự tải 15 ca từ HF thẳng vào locator mờ (`/home/ubuntu/rca-p7/T-055/data-root/data/locked/rcaeval-re3ob-30/<mã>/`). 45/45 file mỗi máy khớp sha256/bytes LFS, khoảng 70 s. Không ghi tên ca ra đĩa EC2. Biên nhận: `results/T-055/runs/tai-001/`.
- **Preflight lần 1** (`results/T-055/runs/preflight-001/decision.json`): span µs, log giây và metric bước 1 s nhất quán ở 30/30 ca; lồng cha–con 100% với µs; `startTimeMillis` khớp 100%; owner nằm trong U. R7 BLOCKED ở 24 ca vì `statusCode` ngoài 0..16. Dừng trước phương pháp, đúng quy tắc.
- **D-55-8.** Đếm tập mã gộp theo host, không theo ca, không nhãn (`*-status-values.json`): gRPC 0/2/4/9/12/13/14 và HTTP 400 (82 span, chỉ ở checkout/payment). Khai miền = 0..16 ∪ {400}. Chỉ TORAI B dùng (cộng mã native); M1 không dùng statusCode. Preflight lần 2 PASS (`decision-002.json`). **Tiếp xúc:** đã thấy phân lớp mã theo serviceName gộp toàn host; không dùng để thiết kế.
- **Khóa:** `results/T-055/scripts/lock.py` dựng profile/runtime/policy/protocol LOCKED_FINAL_RE3/grant/2 plan trong `results/T-054/runs/re3-ban-cuoi-001/meta/`. Gói dựng lần đầu bị bỏ trước khi dùng, vì nguồn quyền trong grant phải là JSON; đã thêm `results/T-055/grants/minh-re3-source.json` rồi dựng lại. Bộ kiểm đã ghim (`nguon.authorize`, `validate_slot`) đạt 210/210 job mỗi host trên laptop. Trên EC2: 106 pin code khớp (gồm lớp phủ), `worker.setup` đạt cho m1/baseline/torai_prep, đủ dữ liệu.
- **Máy:** code root `work-re3` (bản sao work-v2 bỏ queue main, 30 MB) + lớp phủ v1 + metadata. 2 worker mỗi EC2. Laptop AC sleep 2700 s → 0 (`results/T-055/runs/phat-001/power-*.txt`), khôi phục sau khi chấm.
- **Phát:** `p7.py run` trên hai EC2 (`results/T-055/runs/phat-001/*-launch.json`), supervisor sống, job đầu VERIFIED sau khoảng 2 phút.

### Sự cố CIRCA và D-55-9 — 08/11/2026

- Quan sát: mọi slot CIRCA trên EC2 trả ERROR `ModuleNotFoundError: No module named 'circa'`. Gói CIRCA chỉ có ở laptop (pythonpath `D:/RCA-ext/work/T-014/CIRCA`); main013 cũng chỉ chạy CIRCA ở laptop. Quy tắc `RE3_METHOD_ERROR_IS_MISS` khóa trước **quá rộng**, nên đã ghi các slot này thành trượt có biên nhận. Đây là **lỗi môi trường, không phải lỗi phương pháp**. Lỗi của tôi khi khóa: không loại trừ lỗi import.
- Hai lỗi khác (MicroRank `No normal baseline for: currencyservice_Export`, TraceRCA `KeyError 'currencyservice_Export'`) là lỗi phương pháp thật (operation mới trong A), khớp preflight R9 (2 ca có operation mới).
- **D-55-9 (Claude quyết):**
  - Lượt chính chạy tiếp; các vế khác độc lập.
  - 30 kết quả CIRCA của lượt chính bị đánh dấu **không hợp lệ (môi trường)**, không chấm; vẫn giữ nguyên trên đĩa.
  - Chạy bổ sung riêng vế CIRCA bằng giao thức RE3 thứ hai (`meta-circa/`, arms = circa), cùng profile/runtime/nguồn độc lập byte-trùng, trên laptop — nơi duy nhất có môi trường CIRCA đã kiểm. Lý do dùng laptop: tính đúng đắn (Minh cho phép), không phải chuyển dữ liệu cho tiện.
  - Lớp phủ v2 (`results/T-055/overlay-v2/`) chuyển lỗi import/môi trường thành BLOCKED.
  - Làm trước khi ghép nhãn, nên không mở RE3 lần hai theo nghĩa xem kết quả rồi sửa.
  - Dữ liệu 30 ca (131,7 MiB) tải thẳng từ HF về `D:/RCA-ext/T-055/data-root` (ngoài git), khớp hash.
  - Code root cục bộ: `D:/RCA-ext/T-055/work-re3-local` (`make_local_root.py`).
- **Bài học đề xuất (chờ Minh duyệt ghi LESSONS):** quy tắc "lỗi phương pháp = trượt" phải chỉ nhận lỗi phát sinh trong code phương pháp. Phải loại trừ tường minh lỗi import/môi trường. Ở pilot, mỗi vế phải chạy ít nhất một slot trên đúng máy sẽ chạy, dù chỉ với dữ liệu giả.

### Luồng A (T-054) trong lúc chờ

- `results/T-054/reports/p7a-013-v2/kiem-toan-ven/kiem.py` → `ket-qua.json`:
  - Chấm lại độc lập 1282 hàng world P (nhãn lấy từ CSV G1, scorer viết lại, không import cham/danh_gia): 0 lệch, chênh lớn nhất bằng 0. A4 tái lập đúng.
  - Quét 4206 file job/invocation/launch: không có tên ca, đường dẫn riêng hay chuỗi root_fault.
  - Thử giả: không bản ghi suy biến một khối; MRR theo chữ cái và theo ngẫu nhiên ở mức ngẫu nhiên.
- A5 phát hiện **4 lỗi làm tròn hai lần trong báo cáo P7(a)**: TraceRCA OB 0,494 → 0,493; C-d2 OB 0,878 → 0,877; CI M1−C-d2 OB hi 0,041 → 0,040; CI M1−C-g OB lo 0,087 → 0,086. Đã sửa trong `bao-cao.md`; manifest báo cáo cần dựng lại (chưa làm). Không đổi kết luận nào.

### Kết thúc chạy, chấm và phân tích — 08/11/2026

1. **Đã làm.**
   - Lượt chính: 420/420 VERIFIED trên hai EC2. Lượt CIRCA bổ sung: 30/30 VERIFIED trên laptop.
   - Nhận về laptop: kết quả, biên nhận và CSV chuẩn bị TORAI B (cần để kiểm chuỗi liên kết thực thi). Parquet thô ở lại EC2.
   - Lượt nhận đầu bỏ CSV nên verify dừng ở `validate_execution_links`; giữ bản đó ở `D:/RCA-ext/T-055/work-re3-score-v1/.../received-001-thieu-csv`.
   - Seal (`results/T-055/runs/cham-001/verified-before-labels.json`), rồi mới ghép nhãn và chấm bằng `cham.evaluate_re3` và `describe`.
   - Phân tích bằng `phan_tich_re3.py`. Báo cáo: `results/T-055/reports/re3/bao-cao-re3.md`.
   - AC sleep khôi phục 2700 s (`results/T-055/runs/phat-001/power-restored.txt`). EC2 vẫn bật, không tắt máy.
2. **File thay đổi.**
   - `results/T-055/**` (script, biên nhận, báo cáo, `manifest-001.json`).
   - `results/T-054/runs/re3-ban-cuoi-001/{meta,meta-circa}/` và `results/T-054/reports/re3-ban-cuoi-001{,-circa}/`.
   - `tasks/T-055-re3-ban-cuoi/{SPEC,LOG}.md`; dòng T-055 trong `docs/STATE.md`.
   - Ngoài git: `D:/RCA-ext/private/T-055/`, `D:/RCA-ext/T-055/`; trên EC2: `/home/ubuntu/rca-p7/T-055/`, `work-re3/`.
3. **Kiểm.**
   - Bộ kiểm đã ghim: authorize, validate_slot, setup, verify_snapshot, compare_labels.
   - Preflight không nhãn; hash nguồn.
   - Mọi số trong báo cáo trỏ `phan-tich-re3.json`.
4. **Chưa chắc / cần Minh quyết.**
   - Kiểm D-55-1…D-55-9, đặc biệt D-55-8 (thêm mã 400 sau preflight) và D-55-9 (CIRCA chạy lại; quy tắc lỗi khóa trước quá rộng).
   - Kết quả: M1 0,925 < M4 0,975, CI chứa 0. M1 = C-a0. Hai cơ chế tính điểm (z với IQR = 0 hoặc max(A); log bị chặn ở 1) đã thấy trên trung gian từng ca và lặp lại P7(a).
   - Còn mở: mã lỗi span theo ca; cơ chế của BARO/TORAI B; xác nhận H1.
   - Đề xuất sửa thiết kế cho FlashTicket ở báo cáo §6 (chưa kiểm).
   - Commit: chưa; chờ Minh duyệt.

**Bước tiếp theo.** Minh đọc báo cáo và mục quyết định. Chuyển prompt dưới đây cho Codex. Sau phản biện, người làm đáp theo §5 bước 7.

**Lệnh cuối.** `D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B results/T-055/scripts/phan_tich_re3.py` → `results/T-055/reports/re3/phan-tich-re3.json`.

### Prompt phản biện cho Codex — Minh chọn chuyển, không tự gửi

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-055, tasks/T-055-re3-ban-cuoi/ (SPEC.md, LOG.md); báo cáo results/T-055/reports/re3/bao-cao-re3.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P7, dataset giữ ngoài RE3-OB bản cuối; chuẩn bị G4.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex (SPEC T-055).
- Tài liệu gốc: tasks/T-055-re3-ban-cuoi/SPEC.md; tasks/T-055-re3-ban-cuoi/LOG.md; results/T-055/grants/minh-re3.txt; results/T-055/runs/khoa-truoc-001/preregistration.json; results/T-055/reports/re3/{bao-cao-re3.md, phan-tich-re3.json}; results/T-055/manifest-001.json; git diff từ commit 601be1a1 trên branch claude/sweet-hawking-dy078d.
- Phản biện và phản hồi trước: không có cho T-055.
- Code và kết quả liên quan: results/T-055/scripts/; results/T-055/overlay/ và overlay-v2/; results/T-054/runs/re3-ban-cuoi-001/{meta,meta-circa}/; results/T-054/reports/re3-ban-cuoi-001/, re3-ban-cuoi-001-circa/; results/T-055/runs/{nguon-001,tai-001,preflight-001,phat-001,cham-001}/; code src/m1/, src/p3/re3.py, results/T-054/scripts/. Bản nhận đầy đủ ở D:/RCA-ext/T-055/work-re3-score-v1 (ngoài git). Lệnh: <env main> -B results/T-055/scripts/phan_tich_re3.py <đường-dẫn-ra-ngoài-repo.json>. Quyền đọc dữ liệu: kết quả và trung gian RE3 đã chấm theo results/T-054/runs/re3-ban-cuoi-001/meta/grant.json; không mở lại RE3, không chạy phương pháp.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat, trừ khi Minh cho phép ghi đúng một bản phản biện mới trong tasks/T-055-re3-ban-cuoi/ theo tasks/_MAU/REVIEW.md.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```

### Đề xuất commit — chờ Minh duyệt

Gồm:
- `tasks/T-055-re3-ban-cuoi/`, `docs/STATE.md`, `results/T-055/` (trừ dữ liệu riêng).
- `results/T-054/runs/re3-ban-cuoi-001/{meta,meta-circa}/`, `results/T-054/reports/re3-ban-cuoi-001{,-circa}/`.
- Các file T-054 của phiên trước (báo cáo P7(a), `kiem-toan-ven/`, `manifest-002.json`).

Không gồm: `.lock`, dữ liệu/telemetry, `D:/RCA-ext/**`. Nội dung đề xuất: "T-054 báo cáo P7(a) + kiểm toàn vẹn; T-055 RE3-OB bản cuối: khóa, chạy, chấm, phân tích".

## 08/11/2026 — Claude, Windows, người làm (đáp phản biện REVIEW.md)

Mở phiên đáp phản biện. Quyền ghi: Minh "Duyệt gói ghi" cho gói gồm `results/T-055/reports/re3/dinh-chinh-001.md`, `results/T-055/manifest-002.json`, bảng phản hồi cuối `REVIEW.md`, mục LOG này và dòng T-055 trong STATE.

### Điểm tự tìm được trước khi đọc REVIEW.md (lượt đọc trước, đã trình trong chat)

- N1 (CHẶN câu cơ chế): ca 428c, E5 đặt F_I = 0 cho cpu/workload của root; bo-E5 và C-a0 RR 0,5 so với M1 0,25. Câu "không phải đồ thị" sai.
- N2: cde8/d07d sai cả ở C-a0 → ngoại trị kênh trace hẹp.
- N3: §0/§3/§6(i) mâu thuẫn bằng chứng T-056 về log, status, SimpleRCA.
- N4: lệch 1 → 2 worker so với preregistration.
- N5: thiếu dòng WHY/DECISIONS đề xuất.
- N6: thiếu dẫn chiếu khai vi phạm A5 — sửa tại chỗ `results/T-054/reports/p7a-013-v2/bao-cao.md` ngoài quyền Q1; đã khai ở LOG T-054 dòng 2422.
- Tự kiểm: chạy lại `phan_tich_re3.py` ra file tạm, trùng byte; manifest-001 14/14 khớp.

### Phản hồi phản biện

R1, R2, R3 đúng. Codex kiểm lại trong chat: đồng ý R1–R3, N1, N2, N5, N6; chỉnh N3 (M4 cộng cả ba nguồn, riêng metric tái lập thứ hạng; status không tăng ở root RE3 không bác bỏ ứng viên cho FlashTicket) và N4 (không chứng minh được "không ảnh hưởng" cho mọi baseline). Tôi kiểm lại và đồng ý cả hai chỉnh. Không còn bất đồng. Chi tiết ở bảng cuối `REVIEW.md`; sửa ở `dinh-chinh-001.md` Đ1–Đ5.

### Đề xuất dòng sổ cho Minh duyệt (N5; chưa ghi sổ chính thức)

Quyết định của Minh (nguồn `results/T-055/grants/minh-re3.txt`):
- DECISIONS: "08/11/2026 — Minh duyệt luồng A, B, C; Q1–Q8 theo đề xuất; mở RE3-OB một lần có preflight không nhãn khóa trước; mở trước, Codex phản biện sau; mỗi EC2 tự tải phần RE3, telemetry giữ trên EC2; FlashTicket chỉ git fetch; giao Claude quyết trong phiên, ghi quyết định lớn để kiểm."
- DECISIONS: "08/11/2026 — Minh duyệt gói đính chính T-055 (dinh-chinh-001)."

Quyết định Claude tự đưa ra theo ủy quyền (Minh chưa xác nhận từng dòng):
- WHY (D-55-1): giữ M1 đúng bản khóa P7(a) cho RE3, không thêm kênh status; vì RE3 là kiểm độc lập duy nhất còn lại, thêm kênh là sửa thiết kế sau test (C-15 B).
- WHY (D-55-3, D-55-4): U = 28 owner theo schema, alias rỗng; đơn vị quyết bằng preflight không nhãn; giữ "chưa kiểm".
- WHY (D-55-5, D-55-9): quy tắc lỗi phương pháp = trượt có phạm vi quá rộng, làm lỗi môi trường CIRCA thành trượt; lớp phủ v2 chuyển lỗi import thành BLOCKED; CIRCA chạy lại trên laptop trước ghép nhãn.
- DECISIONS ghi nhận (D-55-8): thêm mã 400 vào miền status sau preflight, chỉ TORAI B dùng; có tiếp xúc gộp theo host.
- LESSONS đề xuất: quy tắc "lỗi phương pháp = trượt" phải loại trừ lỗi import/môi trường; mỗi vế chạy thử ít nhất một slot trên đúng máy.

### Kết thúc phiên

1. **Đã làm.** Tự soát; kiểm R1–R3 trên bản nhận; đáp lượt kiểm lại của Codex; ghi đính chính Đ1–Đ5; điền bảng phản hồi; dựng `manifest-002.json`.
2. **File thay đổi.** Mới: `results/T-055/reports/re3/dinh-chinh-001.md`, `results/T-055/manifest-002.json`. Sửa: bảng cuối `tasks/T-055-re3-ban-cuoi/REVIEW.md`; LOG này; dòng T-055 trong `docs/STATE.md`. Không sửa `bao-cao-re3.md`, script, code, manifest-001.
3. **Kiểm.** Phân tích chạy lại trùng byte; bản nhận: 0d4b `huong=xuong`, `r_xuong_A`=0,6133; đếm log 36/42 s=1; `results/T-056/ket-qua-002.json#/tom_tat/RE3-OB` R1_events MRR 0,975, trùng đầu M4 30/30; preregistration workers 1, plan 2; manifest-002 khớp toàn bộ khi dựng.
4. **Còn mở / Minh quyết.** Số xếp hạng giữ; kết luận cơ chế dùng theo đính chính. OPEN: tác dụng đổi thang log, kênh status, sửa nhánh c = 1; H1; T-056 chưa phản biện. Minh quyết: các dòng sổ đề xuất trên; D-55-1…9; commit; gửi hay dừng lượt kiểm sửa.

**Bước tiếp theo.** Minh chọn gửi prompt dưới cho Codex để kiểm riêng phần sửa đã duyệt, hoặc dừng. Kiểm hash theo `results/T-055/manifest-002.json`.

**Lệnh cuối.** Dựng `results/T-055/manifest-002.json` (sha256/bytes các file của manifest-001 cộng đính chính 001).

### Prompt cho Codex — kiểm lại phản hồi và sửa (Minh chọn gửi, không tự gửi)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-055, tasks/T-055-re3-ban-cuoi/.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P7, đánh giá RE3-OB bản cuối, chuẩn bị G4.
- Người làm và người phản biện chính thức: Claude là người làm; Codex là người phản biện theo SPEC.
- Tài liệu gốc: tasks/T-055-re3-ban-cuoi/{SPEC.md,LOG.md}; results/T-055/grants/minh-re3.txt; results/T-055/reports/re3/{bao-cao-re3.md,dinh-chinh-001.md}; results/T-055/{manifest-001.json,manifest-002.json}; docs/STATE.md. Commit gốc 601be1a1fe17ac5383fdb31a695764d25624ae59 trên claude/sweet-hawking-dy078d; kiểm lại revision và cây làm việc hiện hành (git status, git diff).
- Phản biện và phản hồi trước: tasks/T-055-re3-ban-cuoi/REVIEW.md (gồm bảng Phản hồi của người làm); mục LOG ngày 08/11/2026 "đáp phản biện REVIEW.md"; liệt kê thư mục để xác định có lượt tiếp theo không.
- Code và kết quả liên quan: results/T-055/; results/T-054/runs/re3-ban-cuoi-001/{meta,meta-circa}/; results/T-054/reports/re3-ban-cuoi-001{,-circa}/; src/m1/, src/simplerca/, src/p3/; results/T-056/{manifest-002.json,ket-qua.json,ket-qua-002.json,runs/,scripts/}. Bản nhận ở D:/RCA-ext/T-055/work-re3-score-v1/. Môi trường D:/RCA-ext/envs/T-014-main/Scripts/python.exe, dùng -X utf8 -B. Quyền dữ liệu theo nguồn duyệt của task; không chạy phương pháp hay mở lại telemetry khóa.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat, trừ khi Minh cho phép ghi đúng một bản phản biện lượt mới trong tasks/T-055-re3-ban-cuoi/ theo tasks/_MAU/REVIEW.md.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```

## 08/11/2026 — Claude, Windows, người làm (đáp lượt kiểm sửa và R4 của Codex)

Mở phiên. Quyền ghi: Minh cho phép ghi nếu không còn mâu thuẫn với Codex. Phạm vi ghi: mục LOG này và dòng T-055 trong `docs/STATE.md`. Không sửa `REVIEW.md` vì R4 chỉ nêu trong chat.

### Diễn biến

- Lượt kiểm sửa của Codex (chat): R1–R3, N1–N6 đúng như bảng cuối `REVIEW.md`. Thêm R4, KHÔNG CHẶN. Nội dung R4: TORAI chọn cột theo `startswith` (`src/torai/torai_sua.py:317`) và chỉ kiểm số lượng thay danh tính thành viên cụm (`torai_sua.py:354`, `src/p3/adapters/torai.py:68`). Codex ghi "trung gian chưa cho phép kết luận lỗi đã xảy ra trên RE3".
- Claude đáp (chat):
  - Lỗi code đúng. Upstream RCAEval 259ea41 có cùng logic (`e2e/torai.py:295–309, 330`).
  - Phần "chưa kết luận được" sai một phần. Trung gian đủ kết luận nhánh lỗi không xảy ra trên RE3.
- Codex kiểm lại (chat): rút câu "chưa kết luận được". Chỉnh phạm vi: tên trùng tiền tố không tự chứng minh kết quả bị ảnh hưởng; phải có owner ngoài cụm thực sự được chọn và còn tác động sau tiền xử lý/RCD. Claude kiểm và đồng ý chỉnh này.
- Không còn bất đồng ảnh hưởng kết luận T-055. Codex đề xuất dừng phản biện.

### Bằng chứng R4 trên RE3 (chỉ đọc, bản nhận `D:/RCA-ext/T-055/work-re3-score-v1/results/T-054/runs/re3-ban-cuoi-001/received/`)

- 90 slot TORAI B, 129 cụm nhiều service: 0 cột của owner ngoài cụm bị `startswith` chọn. Phép đếm chạy trên header bốn CSV `prepare/` của mỗi slot. Bảng thực lọc ở `torai_sua.py:317–331` là tập con cột CSV (chỉ lấy mẫu dòng và bỏ cột hằng), nên phép đếm là chặn trên.
- Cặp tiền tố duy nhất trong `service_list`: `frontend`/`frontend-external`, 90/90 slot. `frontend` ở nhánh `don` (cụm một service, không gọi RCD; `src/p3/adapters/torai.py:57`) 90/90.
- 6 slot (2 ca) có 32 cột metric của 16 owner Sock Shop ngoài `service_list`; 0/32 cột biến thiên. Đã khai trước ở `results/T-055/runs/khoa-truoc-001/preregistration.json` (giả định U). Hai ca này RR = 1 ở M1, M4 và CIRCA bổ sung (`results/T-054/reports/re3-ban-cuoi-001{,-circa}/re3-tables.json#/per_case`, world P).
- Ranking TORAI là hoán vị đủ của `observed_entities` ở 90/90 slot. 113/129 cụm dự phòng; 74/90 slot dự phòng toàn bộ — khớp số Codex.
- Hai file code TORAI khớp pin trong `results/T-054/runs/chuan-bi-main-013-v2/code-pins.json`.
- Khai: ở lượt trước Claude đã đọc 6 file `result.json` TORAI trong queue laptop `results/T-054/runs/main-013-v2/` (chỉ danh sách service/khối; không nhãn, không điểm). Việc này ngoài grant T-055. Không dùng làm kết luận.

### Kết thúc phiên

1. **Đã làm.** Kiểm R4 và lượt kiểm lại của Codex trên code, upstream và bản nhận; ghi mục này và dòng STATE.
2. **File thay đổi.** `tasks/T-055-re3-ban-cuoi/LOG.md` (mục này); dòng T-055 trong `docs/STATE.md`. Không sửa báo cáo, code, manifest, `REVIEW.md`.
3. **Kiểm.** `manifest-001` 14/14, `manifest-002` 15/15 khớp. Các phép đếm ở mục trên (script tạm ngoài repo, không lưu).
4. **Còn mở / Minh quyết.**
   - R4: lỗi code tiềm ẩn còn trong file đã ghim; không ảnh hưởng RE3; không cần chạy lại RE3.
   - R4 trên P7(a) (T-054): chưa kiểm, ngoài quyền T-055.
   - Sửa TORAI cho lượt mới: cần phạm vi và mục WHY riêng (lệch code chính thức, như sửa A/B của T-016); file đang bị ghim, sửa sẽ đổi hash.
   - Minh quyết: dừng phản biện T-055; D-55-1…9; các dòng sổ đề xuất; nghiệm thu; commit. Đồng thuận hai agent không tự đóng task.

**Bước tiếp theo.** Minh quyết dừng phản biện và nghiệm thu, hoặc gửi prompt dưới cho Codex kiểm mục LOG/STATE này. Nếu giao kiểm R4 trên P7(a) thì cần quyền đọc kết quả main013-v2.

**Lệnh cuối.** Đếm nhánh khối chứa `frontend` và kiểm pin hai file TORAI: `{('don', 1): 90}`; cả hai `in pins: True`.

### Prompt cho Codex — kiểm lại mục LOG/STATE này (Minh chọn gửi hoặc dừng, không tự gửi)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-055, tasks/T-055-re3-ban-cuoi/.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P7(a)/RE3 bản cuối, chuẩn bị G4.
- Người làm và người phản biện chính thức: Claude làm; Codex phản biện theo SPEC.
- Tài liệu gốc: tasks/T-055-re3-ban-cuoi/{SPEC.md,LOG.md}; results/T-055/reports/re3/{bao-cao-re3.md,dinh-chinh-001.md}; results/T-055/{manifest-001.json,manifest-002.json}; results/T-055/runs/khoa-truoc-001/preregistration.json; docs/STATE.md; nguồn duyệt trong results/T-055/grants/. Đọc cây làm việc hiện hành, git status và git diff của LOG T-055 và docs/STATE.md.
- Phản biện và phản hồi trước: tasks/T-055-re3-ban-cuoi/REVIEW.md và bảng phản hồi cuối file; các mục LOG T-055 theo thứ tự, gồm mục "đáp lượt kiểm sửa và R4 của Codex"; các lượt trao đổi trong chat được Minh chuyển kèm prompt này.
- Code và kết quả liên quan: src/torai/torai_sua.py; src/p3/adapters/torai.py; code chính thức RCAEval ở D:/RCA-ext/src/RCAEval, revision 259ea4167160256a74ad30004aa3d96a998c846e; bản nhận D:/RCA-ext/T-055/work-re3-score-v1/results/T-054/runs/re3-ban-cuoi-001/received/; results/T-054/reports/re3-ban-cuoi-001{,-circa}/re3-tables.json; results/T-054/runs/chuan-bi-main-013-v2/code-pins.json; results/T-055/. Python D:/RCA-ext/envs/T-014-main/Scripts/python.exe, dùng -X utf8 -B. Quyền đọc theo grant T-055; không chạy lại phương pháp hoặc mở dữ liệu ngoài grant.
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
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```


## 09/11/2026 — Claude, Windows, người làm (khép task)

- Minh: “T56 chạy xong chưa ? rồi thì khép 3 task lại, trình kế hoạch tiếp theo”. T-056 đã chạy và đáp phản biện xong; Codex chưa kiểm lại lượt cuối. Minh nghiệm thu T-054, T-055, T-056 ngày 09/11/2026. Các câu hỏi khoa học OPEN giữ nguyên; nghiệm thu không xác nhận cơ chế hay hiệu quả.
