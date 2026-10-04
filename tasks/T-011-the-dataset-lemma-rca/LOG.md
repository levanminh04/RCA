# Nhật ký T-011

## Phiên 1 — 03/10/2026 — Codex — Windows 11 — người làm (gói T-003)

**Mở phiên:** đã đọc luật/STATE/mẫu; task mới, chưa có đầu ra cũ. Người phản biện dự kiến Claude; subagent chỉ hỗ trợ người làm.

**Quyết định của Minh trong phiên:** “triển khai toàn bộ task 003 cho tôi, gồm cả các task phụ , sử dụng sub agent với model mạnh nhất nếu cần”. Ghi nguyên lời trong Q-45 của DECISIONS. Chưa có câu trả lời quyền đọc số đo/giữ ngoài/tải lớn.

**Diễn biến:**
- Khởi tạo SPEC/LOG trong gói giao thực hiện. Bắt đầu nguồn/metadata/nhãn riêng; chưa tải archive telemetry.



## Bàn giao phần nguồn/metadata — 03/10/2026 — Codex subagent hỗ trợ người làm

- Đã đọc luật, STATE, SPEC T-011/T-003, LOG gói cha, mẫu T-002 và các nguồn quản trị/nhiệm vụ trực tiếp. Q-46 chỉ cho metadata toàn kho rồi trình file mẫu; chưa là quyền telemetry. Root cấp vùng ghi đúng SPEC; không sửa file chung. Claude vẫn là reviewer dự kiến.
- Lấy metadata/docs/code/nhãn riêng: 34 request, 33 thành công, một lỗi SSL www.lemmarca.info được giữ trong manifest. Tổng thành công 1.097.933 byte; collector 18,157 giây. Các lần web đọc trước đó chỉ đọc, không lưu archive. Không khảo sát nguồn mới sau yêu cầu bàn giao.
- Census bốn HF revision: Original Product Review 4 ZIP /53.633.808.946 byte; Original Cloud 6 ZIP /33.002.132.069; Preprocessed PR 8 ZIP /6.655.484.106; Preprocessed Cloud 11 ZIP /4.737.524.465. Tổng mọi file có README/gitattributes là đại lượng khác, ghi riêng trong count-summary. File/byte/date không là census incident.
- Nhãn riêng Cloud 20240124 đã parse 1 record; FastPC code có 5 cặp folder/pod nhưng 0901 không trong PR release hiện tại nên mapping OPEN. OT evaluator có 14 nhóm root, 6 nhóm đa root, 22 chuỗi entity; WADI segmentation có 14 interval. Hai evaluator có cùng literal. Không thực thi code baseline, không đọc metric/log/trace.
- Kiểm thời gian nhãn riêng: epoch 1706087451 thành 09:10:51 UTC, trong khi inject_time là 03:10:51 không có timezone; lệch 6 giờ chỉ nếu giả sử chuỗi UTC. Lưu label-time-check.json; không tự sửa hoặc áp JST→UTC của PPTX cho JSON này.
- Giữ NC/ND là material conflict: cùng HF README có frontmatter NC và body ND; GitHub README NC/ND và LICENSE NC; paper Appendix F/site ND. Dừng phần sử dụng phụ thuộc. iTrust terms riêng cấm chia sẻ dataset lại; không override bằng license LEMMA. Catalog WADI9/code14/gốc15 và SWaT16/gốc41 giữ đủ nguồn/phạm vi; chưa chốt subset.
- Có thẻ IT hai hệ, mỗi thẻ đủ10mục và phân biệt Original/Preprocessed; OT catalog đủ10mục; conflicts; kế hoạch bảng mọi ZIP. Mẫu đề xuất PR20211203 và Cloud20240124 metric+log gồm4ZIP =1.583.143.326byte; chọn vì nguồn nhãn/mapping/time và hai hệ, không vì nhỏ. Các ngày/schema/root còn lại có dependency để không suy rộng từ mẫu. Chưa tải.

### Tự kiểm và kết quả

- Collector --verify/--validate-counts đạt SHA-256, Git blob source, revision/tree/byte/counts, OT literal equality, epoch conversion.
- Kiểm độc lập qua stdin đối chiếu từng tuple HF path/size/oid/LFS hash với inventory; HF siblings trùng tập file tree, manifest không có pagination next; đủ mục1–10 cho hai IT và OT; links nội bộ tồn tại; AST source; proposal cộng byte khớp. Lưu runs/run-001/validation.json.
- Lượt kiểm trước lỗi UnicodeEncodeError khi in comment nguồn tiếng Nhật qua console cp1252, không sửa nguồn hoặc số. Đã sửa stdout UTF-8 cho lệnh kiểm rồi chạy lại thành công; giữ ghi nhận lượt lỗi.
- Số request từng báo root bằng đếm tay bị nhầm, đã đính chính bằng manifest:34/33/1. Không dùng số chat làm nguồn.
- Có47file đầu ra được kiểm và ghi hash tại results/T-011/artifact-manifest.json; chỉ đổi results/T-011/ và append LOG này. Không chạm STATE/DECISIONS/dataREADME hoặc SPEC; không commit/push, không data/locked, không archive cũ.

### Kết thúc phần được phép / tiếp nhận

1. Đã làm: metadata toàn bốn kho HF, code/schema kỳ vọng/nhãn riêng, license/source conflicts, thẻ IT/OT và proposal file mẫu; toàn T-011 còn chưa xong.
2. File thay đổi: results/T-011/scripts/{collect_metadata.py,build_cards.py}; the-dataset.md; catalog-ot.md; license-and-source-conflicts.md; inspection-plan.md; artifact-manifest.json; runs/run-001/{manifest.json,inventory.csv,count-summary.json,labels-from-code.json,label-time-check.json,inspection-proposal.json,validation.json} và33snapshots theo manifest; LOG này chỉ thêm.
3. Kiểm đã chạy và kết quả: nguồn/hash/inventory/label arithmetic/links/sections đạt; không chạy telemetry quality hoặc phương pháp RCA.
4. OPEN cần Minh/tác giả: quyền giữ ngoài/telemetry; license áp cho đúng release; timezone nhãn JSON; nhãn/schema/trace trong archive, mapping raw–processed; subset OT. Không thêm quyết định khoa học hay chọn dataset.

Bước tiếp theo: đọc SPEC, LOG này, thẻ/conflicts và inspection-plan. Chạy `py -3 -B results/T-011/scripts/collect_metadata.py --verify --validate-counts`. Thẻ IT và inspection-plan sinh từ `py -3 -B results/T-011/scripts/build_cards.py`; muốn sửa nội dung sinh phải sửa script trước. Không lấy nguồn lại nếu snapshot hợp lệ; lượt lấy mới cần `--sources --run run-002 --verify`, giữ run cũ. Chỉ sau Minh chốt quyền và phần giấy phép được giải quyết mới tiếp file cụ thể; không đọc archive vì Q-46. Chưa chuyển chờ phản biện/viết prompt như toàn task đã hoàn tất.

Lệnh kiểm cuối: `py -3 -B results/T-011/scripts/collect_metadata.py --verify --validate-counts`, sau đó kiểm whitespace phạm vi. Nội dung commit đề xuất khi Minh yêu cầu/duyệt: `docs: inventory LEMMA variants and preserve access and label uncertainties`. Chưa commit/push.

## 03/10/2026 — mở lượt hoàn thiện Q-47
Codex, laptop Windows và EC2 mới, người làm. Minh duyệt bổ sung SPEC Q-47; bỏ OT, giao chọn bảo toàn, cho kiểm các bộ còn lại, gộp Claude REVIEW parent; tự phản biện trước bàn giao. Không dùng instance T-007, không mở locked.

## 03/10/2026 — mở lượt xác minh nguồn IT theo Q-47
Codex, laptop Windows, subagent hỗ trợ người làm T-003. Đọc AGENTS, STATE, SPEC/LOG T-003 và T-011, thẻ/manifest/source hiện có. Q-47 đã được root ghi trong SPEC: bỏ OT khỏi khảo sát mới; xác minh nguồn IT và license/lineage trước quyết định bảo toàn. Chỉ ghi results/T-011 và LOG; không đọc telemetry, không tải archive, không sửa file chung. Bắt đầu đối chiếu revision hiện hành, README và giấy phép nguồn chính thức; giữ lỗi request và snapshot cũ.

## 03/10/2026 — tiếp checkpoint bằng GPT-6.1-Sol high
Codex subagent hỗ trợ người làm; laptop Windows và EC2 mới. Đọc AGENTS/STATE/SPEC T003/T011, LOG và WHY-14. Tái dùng bốn ZIP download-001 đã có trên EC2, không tải lại. Bắt đầu kiểm toàn bộ member trong đúng bốn ZIP: CSV đọc luồng, CRC khi EOF; PPTX nhãn/schema; NPY object dùng bộ đọc static opcode inert, không pickle.load/allow_pickle=True và không gọi GLOBAL/REDUCE trong payload. Phép tự kiểm chống GLOBAL nguy hiểm/shape sai và kiểm cú pháp đạt. Lượt chạy có console/progress và thời gian từng member; giữ cả lỗi. Bắt đầu inspect-002, console trong inspect-001. Không RCA/training, không Original telemetry/Bank/locked, không repo lưu trữ.

## 03/10/2026 — kết thúc phần kiểm file Q-47 — Codex GPT-6.1-Sol high

Tiếp nhận checkpoint nhánh lemma_sources_final và download archive_acquisition; vai trò vẫn là subagent hỗ trợ người làm Codex. Claude phản biện gộp T-003, không tạo REVIEW nhánh. Đã đọc luật, STATE, SPEC/LOG T003/T011 và WHY-14; chỉ ghi results/T-011 và LOG này. Không đổi quyết định khoa học, SPEC, docs chung hoặc data README. Quyền tải/kiểm là Q-47; không thêm gói tải hay mở Original/ngày khác/Bank/locked.

### Đã làm và dữ kiện

- Tái dùng bốn ZIP tải trên EC2 mới key2, đúng PR20211203/Cloud20240124 metric+log, tổng1.583.143.326byte. Download-00127,540s, không tải lại. Root đối chiếu SHA-256/byte với HF LFS public revision tại results/T-003/runs/lemma-independent-hash-001/result.json; cả bốn khớp.
- Toàn bộ2.431 file không phải directory trong bốn ZIP đã đọc qua decompressor tới EOF/CRC. Có17.500.872.729byte member,2.387CSV/64.107.208dòng,42NPY và2PPTX. Kết quả hợp lệ cuối inspect-008 tái dùng inspect-007/002; không dùng elapsed2,824s của lượt reuse làm chi phí toàn scan.
- CSV đọc luồng. NPY object đọc bằng static opcode inert, không pickle.load/allow_pickle=True, không import/gọi GLOBAL/REDUCE trong payload. Kiểm shape×dtype×byte và order trước primitive f8/i8/i4. Hostile GLOBAL và shape sai bị chặn trong selfcheck. Không thực thi baseline/RCA/training.
- PR có197.543byte không giải UTF-8 trong16CSV; surrogateescape bảo toàn byte và đếm lỗi, không sửa gốc. Encoding khác có thể giải thích; CRC đạt không gọi file chắc chắn hỏng. Không có ragged row; PR có2 nonfinite ở cột Latency của successful_rate reviews-v2/v3. Constant/duplicate/cadence/gap theo kênh lưu đầy đủ, không gộp alias thành lần lặp.
- Independent KPI check validate-001 chạy --skip-linkage: Cloud14/14 Sequence case khớp toàn bộ CSV means theo label/second. PR46/46 case thiếu label/time hoặc khác KPI; node ratings63.976matched,37.938missing,63.974mismatch. Không sửa hoặc khẳng định exporter lỗi; cần tác giả giải provenance/KPI khác.
- Linkage đúng ở validate-003 (--skip-comparisons), không lấy linkage rỗng validate-001 hoặc union sai validate-002 làm kết quả. Cloud15 metric/15 structured log filenames/giao15,15 log-feature entity; PR224 metric/1.177 log filenames/giao160,302p2n,132 log-feature entity. Giữ riêng ba tập.
- Cloud PPTX ghi AP instance i-078923fb30cac1ede, bug03:10Z/failure03:10:51Z ngày24/01/2024; FACT nguồn, không onset được đo độc lập. JSONepoch09:10:51Z khác sáu giờ, không sửa; PPTX có Z không dịch JST thêm. PR PPTX cause externalNFS đầy đĩa; README nhãn MongoDB-v1 giữ riêng nguyên nhân ngoài cluster. Không tính trace graph từ kiến trúc; Original chỉ metadata.
- Cloud q=.95/.99/.995 mọi kênh/SLI, reference12h/control12h/afterbug24h theo source;807dòng kết quả giữ band, zero band, tử/mẫu. Log CSV dùng giờ UTC đầy đủ bỏ biên; chỉ11reference/control samples, q thô. Cloud PCA kết thúc trước bug, fault denominator0 giữ tỷ lệ trống. Root gắn sau tính; không chọn SLI theo root, không OR/regex thành nhãn vùng. Source normal24h có502 trước lỗi, không healthy ground truth. PR không dựng normal từ phần đầu tùy ý khi mốc/provenance OPEN.

### Lượt lỗi, thời gian và file

- inspect-002200,284s/maxRSS901.348KiB: CRC toàn file đạt, giữ lỗi UTF-8/schema đầu.
- inspect-004 dừng tối ưu; progress cuối hoàn tất member có elapsed354,209s, giữ cả checkpoint/console. Không coi đó là tổng thời gian đầy đủ của lượt dừng. Dùng regex C để đếm surrogate, so độc lập với predicate ord đạt; không bỏ phép kiểm.
- inspect-005/006 giữ lỗi/bổ sung Cloud log schema; inspect-007135,206s chỉ kiểm phần lỗi và tái dùng phần đạt; inspect-0082,824s bổ sung PR log NPY layout lồng/3D. validate-00194,707s; validate-002 giữ union cũ; validate-0030,033s sửa đúng modality sets. Có bước chồng thời gian, không benchmark phương pháp/dự báo full release.
- Thêm scripts safe_npy.py, inspect_files.py, validate_files.py, build_file_report.py; sửa build_cards.py để dùng kết quả file hiện hành khi có. Thêm kiem-file.md, file-inspection-summary.json, cloud-descriptive-bands.csv; cập nhật the-dataset.md/inspection-plan.md và callout lịch sử nguồn xac-minh-nguon-va-doc-lap.md. Kết quả download/inspect/validate/console/progress và selfcheck trong runs; nguồn cũ giữ nguyên. Manifest cuối ghi đúng toàn bộ file hiện có sau handoff. Không commit/push; raw/derived payload không được phát hành ngoài phạm vi kiểm nội bộ.

### Tự kiểm cuối và điều chưa chắc

runs/selfcheck-files-001/validation.json PASS: cộng byte/file/CRC/rows độc lập từ JSON,42NPY/2.387CSV,807band rows, tử/mẫu/tỷ lệ trống khi denominator0, KPI14Cloud/46PR, modality sets, thẻ hai hệ mỗi hệ10mục, toàn link nội bộ, AST bảy script. collect_metadata.py --verify --validate-counts và verify_current_sources.py --verify PASS offline; safe_npy.py selfcheck PASS. Không chạy lại full scan/tải lại khi hoàn thiện handoff.

OPEN có owner: tác giả giải exact NC/ND license, PR KPI lineage/mốc normal, Cloud JSON time và log-feature KPI_Label ratings khác scenario8; Minh/Codex xác định đúng unit root cho PR, quyền/byte nếu muốn mở Original hoặc ngày khác và trace parent/nhãn vùng; Minh chọn G1/thí nghiệm. Một ngày mỗi hệ không là census quality toàn release. Quyết định mới trong nhánh: không có. Nội dung cần tài liệu formal sau duyệt là giới hạn nhãn/provenance/normal/license và mức phủ; chưa tự sửa docs chung.

Bước tiếp theo: root đọc the-dataset.md, kiem-file.md, file-inspection-summary.json, runs/selfcheck-files-001/validation.json và artifact-manifest-final.json; đưa phạm vi/OPEN vào tổng hợp T003, gộp Claude REVIEW theo mẫu chung. Không tải/mở thêm dữ liệu để lấp OPEN ngoài bốn ZIP. Dựng lại thẻ bằng `py -3 -B results/T-011/scripts/build_cards.py`; kiểm nguồn offline bằng `py -3 -B results/T-011/scripts/collect_metadata.py --verify --validate-counts` và `py -3 -B results/T-011/scripts/verify_current_sources.py --verify`. Audit remote có thể tái lập với run mới qua scripts/inspect_files.py, nhưng không cần chạy lại khi nhận tiếp kết quả hợp lệ.

Lệnh kiểm cuối: `py -3 -B -` qua stdin, phép assert saved outputs/link/section/numbers/AST được ghi đủ tại runs/selfcheck-files-001/validation.json. Lệnh ghi cuối: thêm mục LOG này và tạo lại manifest SHA-256 cho artifact T011 hiện hành. Commit đề xuất khi Minh yêu cầu/duyệt: `docs: inspect approved LEMMA samples and retain provenance limits`; chưa commit/push. Root tự cập nhật STATE trong đúng dòng task.
