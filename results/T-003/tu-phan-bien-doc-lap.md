
## Tự phản biện độc lập trước Claude — T-003

Người làm chịu trách nhiệm kết quả; đây không phải REVIEW chính thức. Root đọc lại bằng chứng và script, kiểm theo đơn vị dữ liệu, nguồn và phạm vi đã duyệt; không trông cậy Claude để phát hiện lỗi thay. [Bản soát nguồn/giao thức của nhánh độc lập](tu-phan-bien-nguon-va-giao-thuc.md) giữ các finding và phản hồi. Các source/hash/khả năng chấm được kiểm từ file, không từ báo cáo chat của subagent.

| Điểm tự tìm | Ảnh hưởng | Sửa và bằng chứng cuối |
|---|---|---|
| Nezha construct metric trùng fault | Dùng làm normal tạo band sai và có thể biến sự cố thành chuẩn | Giữ symptoms-001 INVALID. 122path trùng hash trong evidence-002; metric probe cuối symptoms-003 dùng bounds trace thật,0validcalibration. Không kết luận metric normal đủ. |
| Mask normal theo phút mở ra ngoài cửa sổ trace | Thu thêm mẫu fault và làm ngưỡng có vẻ đủ | Giữ symptoms-002 LIMITED, dùng exact bounds ở symptoms-003. Trace probe độc lập dùng CSV normal, tham chiếu/đối chứng chrono, giới hạn cửa sổ ngắn và số mẫu nhỏ. |
| Count missing-reference nhân số q trong khi before-injection là span | Tử/mẫu khác đơn vị | trace-symptoms-002 đếm per span; kiểm conservation từng dataset/date/clock. Không tăng số incident khi thử2clock. |
| Thẻ còn biểu thức f-string thay số | Số không truy được tới kết quả | card-final-002 đã thay số, dẫn trace-symptoms-002 và n từng calibration. Root kiểm Duration toàn4.180.244row theo End-Start và SQL parent độc lập. |
| Eadro nested có dữ liệu raw lặp | Tăng giả số lặp/ca nếu cộng biểu diễn | Toàn794member kiểm CRC/hash. 32biểu diễn nhưng19phiên duy nhất;117event. Nested hash trùng không tạo lần lặp thứhai. verify_files tính lại trực tiếp6probe CSV và parent balance đạt. |
| Deep graph edges bị hiểu2×E | Sai bậc/endpoint và kéo kết luận đồ thị sai | inspect-002 giữ lịch sử không dùng graph-degree sai. inspect-005 dùngE×2,0endpoint/edge-attr mismatch; kiểm nhãn và raw-ID. Không coi event-node degree là root service degree. |
| Deep normal graph có28.116ID vắng span raw | Không được gọi raw/processed toàn bộ cùng corpus | Tải all-log conditional đúngSPEC: inspect-007/008 chứng minh28.116ID cólog, vẫn không cóspanraw. Giữ giới hạn lineage, không suy log phục hồi parent. All-log7.705.050dòng khớp paper;1565graphID vẫn không thấylog. |
| LEMMA parser schema/UTF-8, objectNPY | Parse thất bại hoặc thực thi pickle sẽ làm census thiếu/không an toàn | static safe_npy whitelist/inert, không gọi GLOBAL/REDUCE; root chạy hostile-input/shape selfcheck đạt. CSV surrogateescape giữbyte; inspect-0080error sau correction,2431CRC. Không gọi decoder error là CRC hỏng. |
| LEMMA metric/entity lẫn log-feature NPY | Tạo giao modality sai | validate-002 giữ lỗi, validate-003 tách metric/logCSV/logNPY. validate-001 chủ ý skip-linkage chỉkiểm KPI; không dùng các mảngrỗng trong lượtđó làm bằng chứng khôngcóentity. |
| Cloud14KPIcase khớp cònPR46case khôngfullmatch | Không tự sửa release hoặc coi mọi KPI là cùng exporter | Kiểm tự tính CSV theo label/second trên từngcase. PR khác có thể do label,đơn vị/KPI/provenance/exporter; chưa phân xử. Cloudđạt là đối chứng reader, không chứng minh mọi payloadPRđúng. |
| Eadro “cận trên” giải nén cũ bỏ phần GZip | Ước lượng31,031GB không là cận trên toànnested | sizes-summary-001 chỉ cộng7XZ, chưa cộng SN-all.tgz sau giải nén. Giữ lịch sử, đánh dấu không dùng làm cận trên toàn bộ. Fullnested có3.520.219.318byte CSV/JSON, trùng1.215.014.584byte; sau bỏtrùng2.305.204.734byte. Báo cáo hiệndùnglogical-member-sizes và resources-final. Không gọi streamingcontent là diskđãchiếm. |

### Kiểm giới hạn của kết luận

Nhãn injection hỗ trợ chấm theo chế độ tiêm, không tự là onset biểu hiện hoặc thời điểm phục hồi. Deep trace_bool là nhãn trace, không root hoặc vùng. LEMMA PPTX Cloud có failuretime nguồn, không onset độc lập; PR benchmark root MongoDB khác nguyên nhân NFS vận hành. Không bộ nào được tạo nhãn vùng bằng q/regex/đồ thị. Khảo sát ngoài root có root gắn sau và tách kênh, không OR/causalclaim.

Bank bảo toàn chưa đọc số đo/predictions, OriginalLEMMA và ngày ngoài mẫu chưa đọc. Bảo toànBank là quyết định theoủyquyền trongWHY13/Q49, không quyết thínghiệmG1. Độc lập injector/collectorBank chưachứngminh; khácdomain/nhóm không làmđạt tiêu chí9. T012 hoàn thành phạmvi tìmnguồn cógiới hạn, không gọi thẻnguồn là fullfilequality. OTbỏkhỏiphạmvimới, nguồn lịch sử còn giữ.

Exactlicense LEMMA vẫnNC/ND, chỉhànhđộnghẹpinternalnoncommercialđượcđốichiếu cảhai legalcode, khôngcấpquyềnphânphối. Eadro/Deep thiếupermissionrõ đượcgiữOPEN. Các vấnđề cầnsource/tác giả hoặcG1/G3 đượcghiownertrongthẻ; khônggọi khônglàm vìscope/chi phí là khôngthểkiểm.

[Kiểm cuối toàn gói](runs/final-002/) kiểm hashnguồn, cúpháp script, nhãnđếmđộc lập, thẻ10mục, link và nhánhvalidation; kiểm kỹthuật đạt không tự đóngmọiOPENkhoahọc. Lượtfinal-001 thấtbại mộtlink vì bản tựphảnbiện chưa được tạo, giữnguyên. KhôngRCA/MyRCA/dev-test/locked/commit/push/StopEC2.


## Tự soát lại sau REVIEW — 04/10/2026

Bản tự soát trước đã bỏ sót R1 và đường lộ điều kiện chọn R2; PASS kỹ thuật cũ không chứng minh đã kiểm đủ khoa học. Người làm chịu trách nhiệm, đã sửa theo Q-51. Không dùng subagent, không nhờ reviewer kiểm thay phần sửa.

- Kiểm trực tiếp nguồn/lượt tải: ba archive đạt checksum, mọi member read-to-end/CRC/hash; TRCA lượt hỏng thiếu20.804byte được giữ, không dùng. Accepted FSE main.pdf vẫn công bố1.430/9.152/25; release reduced chỉ10folder,2marker.invalid. Không gọi marker vắng là tự chứng minh SLI sạch. Mỗi ca/phase có root graph position, parent/linkage denominator kiểm bảo toàn.
- Tự phản bác diễn giải “TRCA là nguồn mới”: toàn1.165CSV và4nhãn samebyteNezha. Tận dụng kiểm chất lượng T008 đúng lineage; không chạy lại RCA hoặc double-count corpus.
- Tự phản bác diễn giải “AnoMod có lỗi code ở cả hai hệ”: SN Code_Stop thực thi dockerstop; TT JVM return/throw có cấu hình thật. Target host/DB không service. Thực26capture: SN2.635/TT63.975trace occurrences khớp Table3, nhưng không13incidents gold/hệ. JSON↔CSV SN trace/span-IDsets khớp. TT lookback24h được kiểm:0traceID overlap kháccapture và0span trướcname timestamp; không gọi nguycơ cấu hình là contamination đã xảy ra. Name time khônginjection/onset.
- Calibration không phươngphápRCA: FSE raw metric/duration, AnoMod duration; chronological firsthalf baseline reference/secondhalf control, baq. Kiểm tử/mẫu, missing/zero-band và monotonic bands; không OR thành vùng, không gán source-target thành rootgold. Counter/unit/raw duration của FSE chưa khóa, window/load/clock vẫn giải thích khảthi khác.
- Tự phản bác “không có nguồn Deep root”: catalog F5/F12 là gợi ý, không perinstancegold. ReleaseF23–F25 còn vắng catalog1–22; bài cho nhiều instance ở service khác. Không tạo label mới hoặc chạyoutside-root bằng nhãn suy chưa duyệt.
- Bank chỉ ZIPdirectory và record.csv qua exactrange,CRC/hash và độc lập đếm136/14/8/9ngày/52ô; level=pod ở136record. WHY13 nhận thiếucensus lúcchọn cũng đúngBank, ghi giới hạn không lỗi mãnguồn. Wholearchivehash OPEN vì bảo toàn payload; không lén tải để “pin revision”.

[Kiểm toàn gói sau sửa](runs/final-review-001/verification.json) PASS302checks,180sourcesnapshots; kiểm hash/cúpháp/liênkết/nhãn và q balances. Đây không chứng minh independence hoàn toàn, onset thật hoặc license rawFSE; các OPEN đó giữ đúng phạm vi và owner trongthẻ. Không sửa phần findingClaude; chỉbảngphản hồi, [hash giữnguyên](runs/review-propagation-001/reviewer-text-preservation.json). Không locked/Bankmeasurements/RCA/dev-test/commit/push/StopEC2. Minh chưa đóngtask.
