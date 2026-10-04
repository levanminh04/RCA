# Nhật ký T-012

## Phiên 1 — 03/10/2026 — Codex — Windows 11 — người làm (gói T-003)

**Mở phiên:** đã đọc luật/STATE/mẫu; task mới, chưa có đầu ra cũ. Người phản biện dự kiến Claude; subagent chỉ hỗ trợ người làm.

**Quyết định của Minh trong phiên:** “triển khai toàn bộ task 003 cho tôi, gồm cả các task phụ , sử dụng sub agent với model mạnh nhất nếu cần”. Ghi nguyên lời trong Q-45 của DECISIONS. Chưa có câu trả lời quyền đọc số đo/giữ ngoài/tải lớn.

**Diễn biến:**
- Khởi tạo SPEC/LOG trong gói giao thực hiện. Bắt đầu nguồn/metadata/nhãn riêng; chưa tải archive telemetry.

### Checkpoint sau khi ngữ cảnh bị nén — 03/10/2026

**Đã làm:** dùng bốn truy vấn web, nhận diện bảy hồ sơ và lưu 10 snapshot tài liệu/metadata chính thức từ các đầu mối đã đọc. Không tìm thêm sau checkpoint. Xem `results/T-012/search-ledger.md` và `metadata-checkpoint.md`.

**File đã ghi:** `results/T-012/source-list.json`, `scripts/capture_sources.py`, `search-ledger.md`, `metadata-checkpoint.md`, `runs/run-001/source-manifest.json`, `record-summary.json` và 10 snapshot trong `runs/run-001/sources/`. Chưa có thẻ hoàn chỉnh, inspection-plan hoặc census nhãn.

**Kiểm:** chế độ `--verify` tính lại byte/hash của 10 snapshot và summary của năm record, đều khớp. Đọc tiêu đề/cấu trúc bốn HTML arXiv và danh tính record. Bước lưu nguồn tải 1.278.428 byte, thời gian 1,960 giây. Telemetry 0 byte; không tải archive, không mở dữ liệu khóa. Thời gian toàn lượt tìm trước checkpoint chưa được ghi thành phép đo nên không báo số ước lượng như số thực đo.

**Còn mở:** latest version, README/commit/license phạm vi dữ liệu/code, nhãn/census, schema thật, quan hệ tái sử dụng giữa các benchmark, thẻ đủ 10 mục và kế hoạch mẫu. FSE artifact rút gọn không tự có số ca toàn bài; LO2 record nói có LO2v2 thay thế. Câu hỏi bảo toàn ứng viên/đọc số đo của gói cha chưa được trả lời.

**Bước tiếp theo:** đọc các file trên; chạy `py -3 -B results/T-012/scripts/capture_sources.py --run run-001 --verify` tại D:/RCA-flashticket. Tiếp tục đối chiếu nguồn hiện hành và inventory/nhãn riêng; còn hai truy vấn và tối đa 12 hồ sơ theo SPEC. Không đọc telemetry cho đến khi có quyết định rõ trong LOG gói cha. Dùng run-id mới cho mọi lượt online, giữ cả lượt hỏng.

**Lệnh cuối:** kiểm offline bằng `capture_sources.py --run run-001 --verify`, đọc record-summary và kiểm tiêu đề/mô tả snapshot bằng Python thư viện chuẩn. Trạng thái: đang làm, chưa đủ tiêu chí xong/chờ phản biện. Theo AGENTS §5a.2, đề nghị mở phiên mới để tiếp nhận.


## 03/10/2026 — mở lượt hoàn thiện Q-47
Codex, laptop Windows và EC2 mới, người làm. Minh duyệt bổ sung SPEC Q-47; bỏ OT, giao chọn bảo toàn, cho kiểm các bộ còn lại, gộp Claude REVIEW parent; tự phản biện trước bàn giao. Không dùng instance T-007, không mở locked.

## Phiên 2 — 03/10/2026 — Codex — Windows 11 — subagent hỗ trợ người làm

Tiếp nhận phạm vi từ root theo Q-47: hoàn tất lượt nguồn/metadata giới hạn, thẻ T-012 và so lineage. Không đọc số đo; không chọn holdout, không sửa SPEC/DECISIONS/WHY/STATE/REVIEW. Đã đọc AGENTS, STATE, SPEC/LOG T-003 và T-012, MRP§4, LESSONS, mẫu T-002, các thẻ nhánh và nguồn lưu. Kiểm lại các snapshot hiện có trước khi bổ sung nguồn.

## Phiên 3 — 03/10/2026 — Codex GPT-6.1 Sol high — Windows 11 — hỗ trợ người làm

Tiếp nhận nhánh recent_independence_final bị ngắt usage theo yêu cầu Minh dùng GPT-6.1 Sol high. Đọc AGENTS/STATE, SPEC và cuối LOG T-003/T-012, Q-47–49 và WHY-13/14, LESSONS và mẫu T-002. Khôi phục từ đầu ra thật: run-002, 14 profiles/cards, lineage/task/inspection-plan đã có và hợp lệ; không làm lại.

**Quyết định trong lượt:** không thêm quyết định Minh. Giữ Q-49/WHY-13 của root về Bank và AIOps lineage; không đọc số đo Bank, data/locked hoặc kết quả dự đoán agent.

**1. Đã làm:** kết thúc hai truy vấn còn lại S5/S6, tổng sáu truy vấn/11 hồ sơ. Lưu ba đầu mối K3: hai bài reuse OpenRCA, FAMOS TT record 2024 ngoài cửa sổ năm; không tạo bộ độc lập mới từ bài reuse. Giữ 14 thẻ đủ 10 mục và matrices. Tự phản biện độc lập nguồn/giao thức Nezha theo Q-47, gửi root trước sửa code: bounds normal minute-envelope vượt trace, 2+2 điểm không phân xử quantile tail, clock chưa khớp, file-level parent/join và trùng corpus cần giữ phạm vi. Không tự sửa Nezha.

**2. File thay đổi trong lượt:** `results/T-012/scripts/final_sources.py`, `verify_final.py`; `runs/run-003/source-manifest.json` và ba snapshot; `runs/final-check-001/verification.json`; `final-leads.md`, cập nhật `search-ledger.md`, thêm thông tin kiểm cuối `inspection-plan.md`; `results/T-003/tu-phan-bien-nguon-va-giao-thuc.md`; LOG này chỉ ghi thêm. Không sửa profile/card cũ vì phép kiểm đạt, không sửa SPEC/STATE/WHY/DECISIONS/data README hoặc root code.

**3. Kiểm:** `capture_sources.py --run run-001 --verify` PASS 10 nguồn và summary; `complete_metadata.py --run run-002 --verify` PASS21 nguồn; `verify_final.py` PASS34 snapshot hash/byte, 14 cards×10 mục và source paths. Kiểm lại số FSE/AnoMod/LO2 trên source gốc. Nezha đọc metric đã được phép để kiểm lại bounds: TT29/01 envelope4 nhưng strict2 điểm/pod; TT30/01 envelope1 strict0; OB22/08 strict1, OB23/08 strict2. Có 765 calibration rows TT29/01, 345 zero-band, chỉ2+2 điểm; epoch clock17.595/21.420 dòng rỗng. Các số trỏ verification, không làm nhãn vùng. Hai lỗi encoding Windows khi đọc/in nguồn được sửa bằng UTF-8; không lặp nghiên cứu hoặc báo thiếu nguồn từ lỗi đó. Không chạy RCA/tải telemetry T012/commit/push.

**4. OPEN:** census nhãn archive T012, quality/schema/parent/normal/symptom chưa kiểm, đúng giới hạn source-only. Bank giữ tới G3. Tiêu chí9 không đủ bằng chứng injector/collector/raw lineage giữa mọi họ. Thời gian web lượt trước checkpoint không có phép đo; không dựng lại thành thời gian thật. Không báo task đã kiểm dataset xong hoặc tự chuyển chờ phản biện trước root tổng hợp.

**Bước tiếp theo chính xác:** root đọc `results/T-003/tu-phan-bien-nguon-va-giao-thuc.md`, `results/T-012/runs/final-check-001/verification.json`, `final-leads.md`, ghép nguồn/card/task/lineage vào T003. Nếu sửa normal protocol, giữ symptoms001/002 và dùng run-id mới; không lấy PASS nguồn làm PASS science. Claude chỉ REVIEW gộp theo Q-47. `verify_final.py` không chạy lại nguyên lệnh vì tạo run-id cố định lần mới; kiểm lại hash manifest và JSON tại chỗ hoặc tạo run mới rõ ràng nếu cần.

**Lệnh cuối:** `git diff --check -- results/T-012 results/T-003/tu-phan-bien-nguon-va-giao-thuc.md tasks/T-012-khao-sat-dataset-2025-2026/LOG.md`. Root chịu cập nhật STATE và LOG parent.


## 04/10/2026 — Codex kiểm toàn ba archive và nhãn Bank sau R1/R3

Vai trò người làm, Windows, không subagent. Minh giao sửa điểm đồng ý Q-51; SPEC bổ sung đãliệt kê data/ngoai-rcaeval/T-012/{anomod,trca,fse}/. Kế hoạch628.411.611byte báo trước tải. Nguồn officialrecord ghim tại review-sources-001; collectorAnoMod17files tại anomod-collector-review-001.

AnoMod/FSE tải đạtMD5 ởdownload-review-001. TRCA cùnglượt bịthiếu20.804byte, file335.055.240byte giữnguyên; retryofficialURL download-review-002 đạt335.076.044byte/MD5. Toàn memberCRC/hash: FSE3519entry/339.482.164logicalbyte; AnoMod44291/3.076.340.723; TRCA1273/3.048.387.906. Khôngfullunpack/runvendor/pickle/RCA. FSE semantic run003:113parquet,10casefolders,2empty.invalid,8khônginvalid/11rootservice/8faultcodes, rootset/degree/parent/linkage/metricquality/probe3q; acceptedpaper text vẫn1430/9152/25. Giữlượt001tzdata/002nsconversionerror; isolatedpyarrow23.0.1/tzdata2025.2 khôngđổi sharedenv.

AnoMod run003 fulltelemetry:13capture/hệ, SN2635/TT63975traceoccurrences khớp paper. .DS_Store khôngca. Followup002 kiểmJSON↔CSV13SN,26captures, allpairsoverlap0, TTspan_before_name0; lookback24h khôngcontamination đãxảyra. Source-targets/canonicallevelhost/DB khácservice, SNCode_Stop dockerstop; không runtimegold/time.18636probe rows duration/q/control theo source-target cóđiềukiện; không rootlabel mới. Giữmetric timestamp/string and CSV time parse lỗi001/002. TRCAfullhash1165CSV+4labels identicalNezha, reuse toànqualityT008; khôngđếm corpus mới.

Bank chỉDriveinventory/ZIPdirectory95members vàinflate record.csv8668byte; censusreproduce002136events/14roots/8reasons/9days/52cells, tất cảlevelpod vàepochtextUTC+8khớp,CRC/hashPASS. Metadata2.829.139.841nén/26.400.499.433logicalbyte; mutableDrivepinobserved, khôngwholearchivehash. KhôngBankmeasurements/predictions/locked.

Đã sửa14cards (6profile cóbằng chứng mới), matrices/inspection-plan/lineage/profiles; giữcardprevious. Builder nguồn cũ đã superseded, dùng write_review_cards.py --run NEW --baseline runs/cards-review-002/previous-card-set.md. Toàngói final-review-001 PASS302checks/180snapshots; sourcehash/balances/labels/link/AST, khôngđồng nghĩa mọiOPEN đãxong. Bước tiếp Minh đọc REVIEW T003; khôngtự mởreview mới. Lệnh cuối verify_final.py --run final-review-001.
