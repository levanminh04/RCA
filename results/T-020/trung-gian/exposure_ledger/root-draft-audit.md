# T020 — self-audit bản nháp root

FACT: kiểm 2026-10-04T14:50:37.598501+00:00. Đây là kiểm nội bộ đầu vào, không thay phản biện Claude sau bàn giao. Không ghi file cuối, không quyết hoặc khuyến nghị lựa chọn G1.

Phạm vi: đọc đầy đủ g1/05/06/10 và hai script hợp nhất/chia ô; đối chiếu census công khai, nhãn, timer lưu sẵn, MRP/SPEC và nguồn kết quả. Chỉ các supplemental timer JSONL đã root đăng ký được đọc ở ngoài repo; SHA/byte được kiểm trước tổng. Không chạy hai script root có chức năng ghi, script task cũ hoặc method. Không đọc schema-samples/payload sample, telemetry mới, data/locked, EC2. Điều này chỉ mô tả lượt audit này; không phải tuyên bố toàn T020 chưa từng đọc payload — root đã báo sự cố scope ở luồng dataset và phải giữ disclosure riêng.

Chưa phát hiện split đưa TX2 vào test/giữ ngoài ở ảnh chụp đã kiểm. Những finding P1 về nguồn/nhãn đã báo root ngay sau đối chiếu exact source; trạng thái dưới đã kiểm lại trên draft/bảng1680 ở cuối lượt. Matrix40 đã kiểm 1680 pairs; các artifact09/V9 cuối và V1 merge vẫn do root hoàn thiện, không dùng phần chưa đọc để tuyên bố kiểm toàn gói đạt.

| ID | Mức/phạm vi | Tình trạng | Vị trí | Finding và bằng chứng |
|---|---|---|---|---|
| F1 | P1 — bằng chứng | Đã sửa quan sát | g1-goi-quyet-dinh.md:44 | Câu cũ nói time/unit RCAEval trong A đã kiểm quá rộng; T002/the-rcaeval.md:98,232,363 đều duration unit OPEN. Bản hiện tại đã giới hạn mốc tiêm/phạm vi mẫu và giữ duration trace OPEN. |
| F2 | P1 — phạm vi tín hiệu | Đã sửa và kiểm bảng1680 | scripts/hop_nhat.py:33; 04-phuong-phap-x-dataset.csv:755 | Preprocessed other dates của cả PR/Cloud hiện metric/trace/log chưa kiểm; các TraceRCA variants cũng chưa kiểm. Chỉ mẫu đã inspect mới có kết luận không trace; không mở payload mới. |
| F3 | P1 — nhãn/mode | Đã sửa quan sát đồng nhất | 05-nhan-va-cua-so.md:20; g1-goi-quyet-dinh.md:74 | Root gold chỉ evaluator; mode a mốc ngoài theo ngân sách Minh duyệt, mode b không cấp mốc. MRP §4/P3 time-label test còn cần Minh làm rõ; audit không tự cấp quyền. |
| F4 | P2 — biến thể/rule | Đã sửa và kiểm bảng1680 | scripts/hop_nhat.py:55; 04-phuong-phap-x-dataset.csv:1366 | Metric rule chỉ cần metric time+service_metric tại ba SS; reason không còn gọi đây là bản giảm modality. Rule trace/log vẫn có điều kiện riêng. |
| F5 | P2 — schema chưa kiểm | Đã sửa late guard và kiểm bảng1680 | scripts/hop_nhat.py:88; 04-phuong-phap-x-dataset.csv:39 | BARO RE1TT/OB hiện chưa kiểm, reason nói file inventory không chứng minh numeric schema/cadence/normal. Kiểm output thực, không suy từ AST hoặc mở raw. |
| F6 | P2 — ngôn nghĩa resampling | Đã sửa; giới hạn giữ tường minh | 06-phuong-an-dataset-va-chia.md:79 | Ô là đơn vị gom cụm đề xuất resampling, chưa chứng minh độc lập thống kê; session/workload dependence và ít support giữ rõ. Không đặt ngưỡng CI hoặc thay unit trong audit. |

Các số đã tính lại độc lập, không chạy script split root:

| Gói | Rows/identity | Ô dataset×root×fault | Kiểm |
|---|---:|---:|---|
| A | 438 | 189 | role từ hash/allowlist; toàn ô cùng phía, census và summary khớp; khôngTX2test/holdout |
| B | 365 | 104 | cùng các kiểm trên |
| C | 473 | 186 | cùng các kiểm trên; toàn testTX0 |

Mỗi bảng06 tại ảnh chụp có số ô, số rows, singleton, TX, min/maxrepeat khớp split-assertions và CSV từngca; A/B/C dùng cùng RE2TT30dev/60test. Hashorder seed20261004 đúng SPEC:28, ceil(remaining/3), forcedTX2dev. RE1OB có unresolved local/HFcopy không được đưa vào test. Census/locked proof là public metadata + allowlist, không mở khóa.

| Timer lưu sẵn | Rows | Sum giây | Phép chiếu90×3 |
|---|---:|---:|---:|
| T016 RCD-OBL20 seed0 | 90 | 5623.3043326419975 | 16869.912997925992 |
| T016 RCD-TT30L10 seed0 | 30 | 1481.5980411359924 | 13334.382370223932 |
| T016 TORAI-gốcTT30L10 seed0 | 30 | 45.16271692498776 | 406.46445232488986 |
| T016 TORAI-sửaTT30L10 seed0 | 30 | 65.6531029810103 | 590.8779268290928 |
| T017 run005 gồm kiểm | 30 | 46.190673000062816 | 138.57201900018845 cho90×1 |

Nguồn timers: root/supplemental-inputs.json bốn exactpath/hash/byte và original savedrecords; T017 results/T-017/runs/run-dev-005/summary.json elapsed_seconds_concurrent_laptop từng30record. Phép chiếu là arithmetic có giả định chưa kiểm, không benchmark hoặc authorization. T014 followup-cost.json:36–46 cộng9335.006157792996worker+4171.454560292999queue=13506.460718085995s, không cộng reservation900 thành đo; vượt10800theo accounting này và exception vẫnOPEN. Các số làm tròn trong10 khớp. T005101.053×90=9094.77, ×3=27284.31;237.518×90=21376.62, ×3=64129.86; BOCPD1440.133×90=129611.97. GDN fit/infer được tách, không nhântrainingmỗiincident.

Authorization: g1/06 đềuCANDIDATE/chờWHY, D1–D6 không ghi là Minh đã chọn; P3 không chạy trongT020, test chỉ mở sauG3; seed/split chỉ nhãn/metadata theoSPEC. Q49 bảo toànBank không được đổi thành Minh chọnBankthí nghiệm. T013R1 dùng trạng thái đã sửa/đóng; nhápallocationWHY vẫnOPEN. T016WHY19/20 đã ghi nhưng headingvẫnĐềxuấtG1. Không dùngtiming-onlyT005làmpermissionđọcraw.

Integration checkpoint cuối: ma trận output có40datasetparts×42variants=1680pairs. F2/F4/F5 đã kiểm từ CSV thực; F1/F3/F6 đã đọc lại câu đã sửa. Hash snapshots của sáu draft/script và matrix ở `root-draft-audit-snapshots.json`, không phải hash của bản bàn giao cuối root còn đang hợp nhất. V1 audit độc lập877rows/683overrides nằm trong `v1-semantic-overrides.csv`; đây là đầu vào root kiểm, không lựa chọn khoa học.

AST của hai script parseđạt. Mọi assert split/timer/summary nêu trên đạt. Không kiểm payload/header Bank, không gọi đủC9 hoặc calibration bằng sốcensus. Những giới hạn incident-unit khác (NezhaTT45labelrecords clock, Bankpod/component, Eadrorecords, LEMMAcaptures, Deeptrace labels) vẫn giữ từ evidence, không tự hợp nhất hoặc tạoô.
