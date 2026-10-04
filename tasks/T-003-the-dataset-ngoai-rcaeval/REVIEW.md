# Phản biện T-003 (gộp T-008–T-012)

- **Người phản biện:** Claude — **Ngày:** 03/10/2026 — **Commit/diff đã đọc:** HEAD `38d3c1b` cộng cây làm việc chưa commit (`git diff HEAD` của docs/STATE, DECISIONS, WHY, data/README; file untracked của tasks/T-003, T-008–T-012 và results/T-003, T-008–T-012).
- **Đã đọc:** AGENTS.md; SPEC và LOG T-003; SPEC T-012, LOG T-010, T-012; results/T-003 (thẻ tổng, bang-tieu-chi, task-cham-duoc, bao-toan-openrca-bank, tu-phan-bien-doc-lap); thẻ T-008, T-009 (mục 8), T-010, T-011 (mục 8), thẻ OpenRCA Bank trong T-012, final-leads; MRP §3, §4, P2, §6, §7; WHY-13, WHY-14; DECISIONS Q-37–Q-50; LESSONS. Code gốc: Eadro `preprocess/align.py` (bản lưu ở results/T-009/sources/codes); README của FudanSELab/train-ticket-fault-replicate (đọc online).

## Kết luận chung

Số liệu chính khớp file kết quả. Ranh giới nhãn ở Eadro, DeepTraLog và LEMMA được ghi cẩn thận. Có hai lỗi chặn. (1) Ba ứng viên 2025–2026 có archive nhỏ (tổng khoảng 0,63 GB), Q-47 đã cho kiểm số đo, nhưng chưa được kiểm và cũng chưa được đề xuất kiểm; vậy mà gói đã bàn giao như đã xong. (2) Nezha có một đường lộ thời điểm tiêm lỗi qua cấu trúc file, nhưng thẻ và bảng task không ghi. Hai điểm không chặn liên quan bộ bảo toàn Bank và nhãn root của DeepTraLog.

Phần câu hỏi cuối prompt về danh sách phương pháp và hồ sơ kỹ thuật thuộc T-001, không thuộc T-003. T-003 chưa chọn dataset thí nghiệm hay chia dev/test, nên chỉ xét được câu "có đường nào để nhãn lọt vào phương pháp không" (R2) và bộ bảo toàn (R3).

## Các điểm

### R1. Ba ứng viên 2025–2026 có archive nhỏ chưa được kiểm, dù đã có quyền — CHẶN

- **Ở đâu:** results/T-012/the-dataset.md (thẻ AnoMod SN/TT, TRCA TT/OB, FSE artifact); results/T-003/the-dataset-ngoai-rcaeval.md §1, §10; LOG T-003, mục "Kết thúc thực hiện" điểm 4; LOG T-012, phiên 3, điểm 4.
- **Sai gì:** Bổ sung Q-47 trong SPEC ghi "các ứng viên còn lại được kiểm số đo theo SPEC". Tiêu chí xong của T-003 ghi "tất cả phần kiểm được và được phép đã làm" và "Không báo gói xong nếu phần Minh đã giao vẫn còn và chưa có quyết định giới hạn". Ba archive dưới đây nhỏ, công khai, giấy phép mở, nhưng tải 0 byte. Cũng không có đề xuất tải nào gửi Minh. Thẻ ghi người chịu trách nhiệm là "Codex sau quyền phù hợp", như thể còn thiếu quyền. Ở đây việc chưa làm bị trình bày thành việc chờ quyền.
- **Bằng chứng:** `results/T-012/runs/run-002/record-summary.json`:
  - AnoMod.zip (record 18342898, CC-BY-4.0): 201.917.396 byte, gồm hai hệ SN và TT.
  - TRCA.zip (record 19335897, CC-BY-4.0): 335.076.044 byte.
  - FSE_26_RCA_dataset_study_reviewer.tar.gz (record 19522409, Apache-2.0): 91.418.171 byte.
  - Tổng 628.411.611 byte, dưới ngưỡng 5 GB của luật cứng 8.
  
  Thẻ T-012 dòng 3 ghi: "telemetry đã tải = 0 byte; số ca thực đọc telemetry = 0". Đây là những bộ có thể bù đúng các chỗ yếu mà phần đã kiểm để lại:
  - Lỗi mã nguồn (tiêu chí 6). AnoMod công bố nhóm lỗi "code". DeepTraLog có lỗi mã nhưng không có nhãn root. Nezha chỉ có return/exception. Eadro không có lỗi mã.
  - Nhãn root và mốc tiêm. Bài FSE công bố root phân cấp và mốc tiêm.
  - Một nhóm tác giả khác (tiêu chí 9). AnoMod thuộc Helsinki.
- **Phản bác có thể có:** Phạm vi ghi của T-012 chỉ có `data/ngoai-rcaeval/metadata/T-012/`. Q-47 chỉ nêu vị trí lưu trên EC2 cho DeepTraLog và LEMMA. Vì vậy có thể cần duyệt thêm vị trí lưu. Lý do này chỉ đòi một đề xuất gửi Minh, không cho phép bàn giao gói như đã xong. Nó cũng không biến phần này thành "chưa có quyền".
- **Hậu quả:** Ở G1, Minh phải chọn dataset trong khi ba ứng viên mới phù hợp nhất với tiêu chí 5, 6 và 9 chưa có census nhãn nào. Điều này ảnh hưởng tới câu trả lời cho yêu cầu của cô về mở rộng dataset (MRP §4, P2).
- **Đề xuất sửa:** Codex trình Minh kế hoạch tải và kiểm khoảng 0,63 GB cho ba archive này, gồm vị trí lưu, census nhãn và mức kiểm file theo SPEC T-012 bước 2–5. Phương án khác: Minh ghi một quyết định giới hạn T-012 ở mức nguồn cho G1. Dù chọn cách nào, cũng sửa dòng "Codex sau quyền phù hợp" trong thẻ cho đúng lý do.

### R2. Nezha lộ thời điểm tiêm lỗi qua việc file nào tồn tại và qua tên file; thẻ và bảng task không ghi — CHẶN

- **Ở đâu:** results/T-008/the-dataset.md, cả OB và TT. Mục 8 của thẻ thay mục "Rò nhãn" của mẫu T-002 bằng khảo sát triệu chứng, nên thẻ không có mục rò nhãn. Mục 7 "Phát hiện theo thời gian". results/T-003/task-cham-duoc.md, hai dòng Nezha.
- **Sai gì:** Trong `rca_data`, trace và log chỉ có ở ba file phút liên tiếp. File đầu tiên là phút tiêm lỗi. Giữa hai lần tiêm không có file trace hay log nào. Vì vậy việc một file tồn tại, và tên phút của nó, đã mang thời điểm tiêm. Với trace và log, Nezha không có dữ liệu "âm" (không có lỗi) ngoài hai cửa sổ construct dài khoảng một phút mỗi ngày. Hệ quả là chế độ tự phát hiện (MRP P3 chế độ b, §6 mục 8) và P/R/F1 theo thời gian (RQ3a) không chấm được trên trace/log của Nezha mà không dùng thông tin suy từ nhãn. Bảng task chỉ ghi "Injection, chưa onset/end thật". Câu này hiểu lầm vấn đề là thiếu nhãn onset, trong khi vấn đề thật là cấu trúc dữ liệu tự lộ nhãn.
- **Bằng chứng:** Đếm từ `results/T-008/runs/download-plan-001/plan.json` và các file `results/T-008/sources/labels/*-fault_list.json`:
  - OB 22/08: 72 file trace cho 24 lần tiêm. Các file đầu là `03_53, 03_54, 03_55, 04_02, 04_03, 04_04, …`, khớp các lần tiêm `03:53:54, 04:02:07, 04:10:20, …`.
  - TT 30/01: 51 file cho 17 lần tiêm. File `11_51…11_53`, `11_59…12_01` khớp lần tiêm `11:51`, `11:59`.
  - Tổng trace `rca_data` là 72 + 96 + 84 + 51 = 303 file, bằng đúng 3 × 101 bản ghi tiêm. Log và traceid có cùng số file.
  - Kiểm bằng lệnh Python chỉ đọc trên plan.json và fault_list. Không đọc telemetry.
- **Phản bác có thể có:** Thẻ có câu "Dùng toàn minute-file chạm injection±60s". Câu này mô tả cách người làm chọn cửa sổ để dựng đồ thị, không nói rằng dataset chỉ có các file đó. Mục tổng §8 có ghi chung "Tên ca/path… chỉ census/chấm", nhưng không nêu đường lộ cụ thể này.
- **Đề xuất sửa:** Thêm mục rò nhãn vào thẻ Nezha cho cả OB và TT. Mục này nêu: trace/log chỉ có ở [phút tiêm, +2 phút]; tên file mang phút tiêm; vì vậy trace/log Nezha chỉ hợp với chế độ biết trước thời điểm. Sửa hai dòng Nezha trong task-cham-duoc.md cho đúng điều này. Metric được lưu theo file từng service mỗi ngày, không theo phút; thẻ nên ghi phạm vi thời gian của metric từ file-audit đã có, thay vì gộp chung với trace/log.

### R3. Bộ bảo toàn Bank: chưa kiểm phần được phép kiểm, và WHY-13 thiếu một giới hạn — KHÔNG CHẶN

- **Ở đâu:** docs/WHY.md WHY-13; results/T-003/bao-toan-openrca-bank.md; thẻ OpenRCA Bank trong results/T-012/the-dataset.md, mục 1, 3, 9.
- **Sai gì:**
  - (a) MRP §4 và Q-47 cho đọc metadata, schema và đếm nhãn của bộ bảo toàn. Thẻ Bank chỉ có số công bố: 136 ca, 14 root, 8 reason. Thẻ ghi "Google Drive… chưa kiểm inventory file" và "Data chưa tải". Như vậy cả tiêu chí 1 ("tải được") lẫn revision của bản sẽ mở ở G3 đều chưa được khóa. Liệt kê nội dung thư mục Drive là việc metadata, rẻ, và nằm trong quyền đã cho.
  - (b) Theo thẻ (A.2), các reason của Bank là CPU, memory, disk, network và JVM. Không có lỗi mã nguồn. WHY-13 mục "Kết luận phụ thuộc" không ghi rằng kết luận RQ3 trên bộ giữ ngoài này chỉ áp cho các nhóm lỗi đó. Đây đúng là chỗ MRP §4 tiêu chí 6 nhấn mạnh.
  - (c) Ở mục "Phương án khác", WHY-13 gạt AnoMod và OpenRCA2 một phần vì "nhãn release chưa xác minh". Nhưng nhãn release của Bank cũng chưa xác minh. Lý do này không phân biệt được hai phía.
- **Bằng chứng:** Các trích dẫn ở trên trong thẻ T-012, mục Bank. `results/T-012/runs/run-002/sources/openrca-tree.json` cho thấy repo không chứa record.csv; chỉ có `dataset/README.md` dẫn tới Drive. Trong tree có `rca/archive/agent-Bank.csv`, nhưng không có trong snapshot nguồn. Tôi xác nhận chưa ai mở file này.
- **Phản bác có thể có:** Q-47 giao quyền chọn cho Codex và chấp nhận rằng chất lượng chưa được xác minh. Vì vậy, chọn Bank không sai về thủ tục. Lý do "khác testbed" của Bank cũng mạnh hơn các ứng viên TT/OB/SN. Điểm này chỉ là phần đã được phép nhưng chưa làm, cộng một giới hạn chưa ghi.
- **Đề xuất sửa:** Trước G1, lưu inventory Drive (tên, kích thước, id; không tải telemetry). Nếu record.csv tải riêng được thì đếm root × reason × ngày. Thêm vào WHY-13 (cần Minh duyệt) một câu giới hạn: RQ3 trên Bank không kiểm lỗi mã nguồn.

### R4. DeepTraLog: thẻ nói "chưa có nguồn để lấp nhãn root" nhưng không xét catalog lỗi mà chính dataset dựa vào — KHÔNG CHẶN

- **Ở đâu:** results/T-010/the-dataset.md, mục 6 ("Cần nguồn nhãn root… chưa có bằng chứng để lấp nhãn này trong task") và mục 10.
- **Sai gì:** Các lỗi F của DeepTraLog lấy từ faulty branches của Train Ticket, tức benchmark lỗi của Fudan. README `FudanSELab/train-ticket-fault-replicate` mô tả từng lỗi kèm service liên quan. Một số lỗi có vị trí đơn (F5 "Basic-Info-Service", F12 "Order-Service"). Một số liên quan nhiều service hoặc toàn hệ (F1, F11, F13 là tương tác giữa các service; F3 là cấu hình JVM/Docker; F4 là SSL trên mọi service). Thẻ không ghi đã xét nguồn này. Câu "không có nguồn" vì vậy mạnh hơn bằng chứng. Kết luận đúng hơn là: có nguồn, nhưng nhãn suy từ đó chỉ có cho một phần lỗi; đó là nhãn nhóm tự suy, cần mục WHY; và chưa xác nhận số F của DeepTraLog trùng số F của catalog.
- **Bằng chứng:** README của train-ticket-fault-replicate (đọc online ngày 03/10/2026), phần mô tả F1–F14. Không có trong snapshot nguồn của T-010.
- **Hậu quả:** Trong các bộ đã kiểm, DeepTraLog là bộ duy nhất có nhiều lỗi mã nguồn. Ở G1, Minh nên biết khả năng chấm root của nó là "một phần, có điều kiện", không phải "không có nguồn".
- **Đề xuất sửa:** Thêm một dòng vào mục 6 và mục 10 của thẻ T-010. Dòng này nêu nguồn catalog, lỗi nào có vị trí đơn, lỗi nào không, và việc đối chiếu số F còn mở.

## Điều đã kiểm và thấy đúng

- Số đếm khớp file:
  - Nezha OB 56 bản ghi / 10 root / 33 ô (histogram lặp 2:23, 1:10); TT 45 / 10 / 23 (`T-008/runs/run-001/summary.json`).
  - Eadro SN 36 / 12 / 36; TT 81 / 27 / 81 (`T-009/runs/run-001/summary.json`).
  - DeepTraLog 109.151 + 23.334 = 132.485 trace; 28.116 ID normal có log nhưng không có span raw; 1.076 + 489 = 1.565 ID không có log. Tính lại từ `T-010/runs/inspect-008/per-label-coverage.json`.
  - LEMMA 43.314.418 + 20.792.790 = 64.107.208 dòng CSV; 26 + 16 = 42 file NPY.
  - Tổng tải 5.264.569.871 + 213.216.632 = 5.477.786.503 byte.
- Nezha: 122 path construct trùng hash với path fault. Tính lại từ blob SHA trong plan.json: cả 122 đều là file metric, tức toàn bộ metric construct. Kết luận của thẻ "không dùng construct metric làm normal sạch" là đúng.
- Eadro `align.py`: tạo cửa sổ dài 10 giây, trượt bước 1 giây (`range(start, end-chunk_lenth+1)`), rồi `np.random.shuffle` để chia train/test. Thẻ T-009 nêu nguy cơ chồng lấn train/test và dè dặt đúng mức ("chưa chứng minh paper dùng chính lệnh đó").
- WHY-14: cách đọc §2(a)(1)(B) của CC BY-NC 4.0 và CC BY-ND 4.0 đúng. Phần quyền chung của hai giấy phép là sao chép và chỉnh sửa nội bộ cho mục đích phi thương mại, không chia sẻ bản chỉnh sửa. WHY-14 không tự chọn một giấy phép thay tác giả.
- Không thấy dấu hiệu đã mở telemetry Bank, file dự đoán agent, `data/locked` hoặc repo RCA cũ. Không có nhãn nào được dùng làm đầu vào, vì T-003 không chạy phương pháp nào.
- Diff ở docs/STATE và DECISIONS nằm trong phạm vi được cho: các dòng của gói và Q-45–Q-50. Các dòng của T-001, T-002 và T-005–T-007 không do gói này sửa.
- Tôi không chạy lại `verify_final.py`, vì lệnh này ghi vào thư mục run trong results/T-003, ngoài quyền ghi của người phản biện.

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| R1 | Đúng — đã sửa | Đã bỏ sót phần kiểm archive và bàn giao sớm. Nay kiểm toàn ba archive628.411.611byte đạt MD5/CRC, labels/schema/parent/normal/clock/probe đúng phạm vi: results/T-012/the-dataset.md và runs/{fse-file-inspect-003,anomod-file-inspect-003,anomod-followup-002,trca-inventory-001,trca-reuse-001}. TRCA1165CSV+4labels identicalNezha; FSE10folder/2invalid/8khônginvalid không toàn1430ca. AnoMod source-target không runtimegold, nhómSNCode_Stop làdockerstop. LicenseFSE nội bộ cóscope hẹp, không tự blanketApache toànraw. | Minh đã giao sửa điểm người làm đồng ý theo Q-51; chưa đóng task. |
| R2 | Đúng về rò điều kiện chọn — đã sửa | Tự kiểm từng101record vàminute-file mọi4ngày: trace/log/traceid đúng phút texttiêm,+1,+2 (303file mỗi modality). Đã phục hồi mục8Rònhãn đúngmẫu, mục6probe và taskmatrix. KhôngcontinuousblindF1 riêngtrace/log này; đổi tên không phục hồi negativecoverage. Phạm vi “chỉ chế độ biết trước” cần giới hạn vào trace/log phát hành: metriccalendar và bài toán conditional khác vẫn cần xem riêng, không loại toàn Nezha chỉ từ finding. Bằng chứng results/T-008/runs/sampling-leakage-001/result.json và thẻ. | Minh đã giao sửa điểm người làm đồng ý theo Q-51; chưa đóng task. |
| R3 | Đúng — đã sửa | Đã Driveinventory/ZIPdirectory95members, chỉinflate record.csv, CRC/hash vàcensus táilập136/14/8/9ngày/52cells ở results/T-012/runs/bank-label-reproduce-002/census.json. KhôngBankmeasurements/predictions. WHY13 ghi thiếu census lúc chọn đúng cảBank vàAnoMod, không phải lý do phânbiệt; bổ sung khôngchấm lỗi mã nguồn. Drive mutable pinid/size/modified/directory/labelhash, chưaimmutablefullrevision vì không đọc fullZIP. | Minh đã giao sửa điểm người làm đồng ý theo Q-51; chưa đóng task. |
| R4 | Đúng về nguồn bị bỏ sót; không coi catalog là root gold — đã sửa | Đã snapshotofficialcatalog ghimrevision ở results/T-010/runs/catalog-review-001/. F5/F12 cógợiý vịtrí, cònF1/F11/F13 nhiều tươngtác,F3/F4config; paper nóiinstance cóthểở service khác. Releasegraph F23/F24/F25 không có trongcatalogđọc, cho thấykhông đủmapping. Thẻ/matrix ghi khả năng ranking một phần cóđiềukiện sau ghépbranch/instance/WHY; khôngsuygoldhay chạyoutside-root từcatalog. | Minh đã giao sửa điểm người làm đồng ý theo Q-51; chưa đóng task. |

## Đánh giá lại sau khi người làm sửa — Claude, 04/10/2026

Minh duyệt ghi mục này. Người phản biện chỉ đọc file, không chạy lại script ghi vào results/.

**Kết luận:** R1–R4 đã được sửa đúng. Không có lỗi mới đủ để chặn. Phần nhận xét R1–R4 ở trên không bị sửa.

| Điểm | Đánh giá | Bằng chứng đã kiểm |
|---|---|---|
| R1 | Đã sửa | Ba archive AnoMod, TRCA, FSE (628.411.611 byte) đã tải và kiểm. Thẻ T-012 ghi số theo file thật, không còn ghi "chờ quyền". |
| R2 | Đã sửa | `results/T-008/runs/sampling-leakage-001/result.json`: cả 4 ngày, cả trace/log/traceid, mỗi lần tiêm đúng 3 file phút, không thiếu, không thừa. Thẻ Nezha có mục 8 "Rò nhãn". Bảng task ghi không chấm phát hiện tự động trên trace/log. Metric theo ngày được xét riêng, không loại cả Nezha. Phạm vi kết luận này đúng. |
| R3 | Đã sửa | `results/T-012/runs/bank-label-reproduce-002/census.json`: 136 ca, 14 root, 8 reason, 9 ngày, 52 ô. Cộng lại theo root và theo reason đều ra 136. `bank-metadata-001/summary.json`: chỉ giải nén `record.csv` (8.668 byte), không đọc telemetry, không đọc file dự đoán. WHY-13 đã thêm giới hạn "không kiểm lỗi mã nguồn" và tự đính chính so sánh không công bằng. |
| R4 | Đã sửa | Catalog đã ghim ở `results/T-010/runs/catalog-review-001/`. Thẻ DeepTraLog ghi: F5, F12 có gợi ý vị trí; các lỗi khác nhiều service hoặc cấu hình; F23–F25 không có trong catalog. Không tự tạo nhãn root. |

**Không chặn, ghi để Minh biết:**

- SPEC T-012 được sửa thêm vùng `data/ngoai-rcaeval/T-012/` với căn cứ Q-51. Q-51 nói "đồng ý review nào thì sửa luôn". Minh cần xác nhận Q-51 bao gồm cả việc sửa SPEC (Luật 0).
- Revision của Bank chưa bất biến, vì Google Drive có thể đổi. Hiện đã ghim id, kích thước và hash file nhãn, chưa có hash toàn archive. Thẻ đã ghi đây là giới hạn.

**Kết quả mới ảnh hưởng tới G1:**

- TRCA giống Nezha từng byte (1.165 CSV và 4 file nhãn). Không tính là bộ riêng.
- AnoMod: mỗi hệ 12 lần chạy lỗi và 1 lần chạy bình thường, mỗi loại lỗi chạy một lần, không có nhãn root xác nhận lúc chạy. Với SN, nhóm "lỗi mã" là `docker stop`.
- Bản rút gọn FSE chỉ có 8 ca không bị đánh dấu invalid, không đại diện cho 1.430 ca của bài.
