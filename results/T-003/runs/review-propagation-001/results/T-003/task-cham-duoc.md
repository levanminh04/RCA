# Task chấm được — nhãn, đơn vị, phạm vi và giới hạn

Cập nhật 03/10/2026. Khả năng theo nhãn đã kiểm hoặc nguồn nêu rõ, không quyết G1. MRR/Hit@k/NDCG cần root đúng entity; P/R/F1 thời gian cần nhãn đúng đơn vị; injection/narrative chưa onset. Chi phí riêng, khôngscore.

| Biến thể/phạm vi | Ranking root | Phát hiện thời gian | Vùng ảnh hưởng | Bất thường từng trace |
|---|---|---|---|---|
| Nezha OB toànCSV approved | 56record/10service/33ô; CANDIDATE sau clock/mapping/protocol | Injection, chưa onset/end thật; không F1onset từtiêm | Chưa nhãn; Duration exceed khôngthay label | Chưa nhãn trực tiếp |
| Nezha TT toànCSV approved | 45record/10service/23ô; text/epoch mâu thuẫn giữ | NhưOB, clock theo record | Không từ graph/root | Không gán mọitrace sau tiêm |
| Eadro SN toànZIP/nested | 36record/12service/36ô, paper72; aliasnginx-thriftOPEN | start/durationtiêm, injection-regime nếu clock phù hợp; thiếu onset/recovery | Probe3q khônglabel vùng | Chưa nhãn trace |
| Eadro TT toànZIP/nested | 81record/27service/81ô, paper162; mỗiô1lần | NhưSN; graphwhole-file khôngfaultinterval | Không root-onlyregion | Chưa nhãntrace |
| Deep graph/toàn raw/all-logtải | Khôngroot serviceGT; error_trace_type/IsError khôngroot | Graph không injection/onset/end, khôngsuy từID | TEG/attention khôngregionGT | 132.485label nhấtquán, P/R/F1trace cócăn cứ;28.116normalID thiếu span raw, logkhôngthayspan |
| LEMMA PR20211203 Preprocessedmẫu | CANDIDATE đúngunitMongoDB benchmark; NFSexternalcause khácunit | Timeline normal/injection thiếu, KPI46case chưa fullmatch | SơđồPPTX khôngregion/traceGT | Khôngspan/nhãntrace trongmẫu |
| LEMMA Cloud20240124 Preprocessedmẫu | CANDIDATE instancei-078923fb30cac1ede, khôngtựservice | PPTXbug03:10Z/failure03:10:51Z, JSONlệch6h; chưa onsetGT | Bands khônglabel vùng | Khôngspan/nhãntrace trongmẫu |
| LEMMA Original/ngày khác | Chỉmetadata, khôngsample thànhcensus | Chưa raw ngoài mẫu, khôngchờquyềnsamplecũ | OPEN | OriginaltraceOPEN |

Nguồn: [Nezha](../T-008/the-dataset.md), [Eadro](../T-009/the-dataset.md), [Deep](../T-010/the-dataset.md), [LEMMA](../T-011/the-dataset.md). Từngrecord/ô/clock/rawcoverage ở artifacts nhánh. Representation/q/span khôngindependentincident.

## T-012 — khả năng theo nguồn, chưa census archive

| Biến thể | Ranking/unit | Thời gian | Vùng | Trace |
|---|---|---|---|---|
| FSE fault-propagation benchmark — artifact rút gọn | CANDIDATE root theo đúng mức nhãn; artifact rút gọn cần census. | Chỉ có căn cứ mốc tiêm trong thiết kế; onset/end và cửa sổ artifact OPEN. | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. | OPEN: chưa thấy nhãn từng trace được kiểm. |
| AnoMod — SocialNetwork | CANDIDATE nếu có nhãn root đúng entity; chưa xác nhận census. | OPEN: cần interval/onset/end đúng nghĩa, không suy từ tên archive. | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. | OPEN: chưa thấy nhãn từng trace được kiểm. |
| AnoMod — TrainTicket | CANDIDATE nếu có nhãn root đúng entity; chưa xác nhận census. | OPEN: cần interval/onset/end đúng nghĩa, không suy từ tên archive. | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. | OPEN: chưa thấy nhãn từng trace được kiểm. |
| TrainTicketTrace | CANDIDATE nếu có nhãn root đúng entity; chưa xác nhận census. | OPEN: cần interval/onset/end đúng nghĩa, không suy từ tên archive. | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. | OPEN: chưa thấy nhãn từng trace được kiểm. |
| Check Your Trace First (TRCA) — TrainTicket | CANDIDATE nếu có nhãn root đúng entity; chưa xác nhận census. | OPEN: cần interval/onset/end đúng nghĩa, không suy từ tên archive. | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. | OPEN: chưa thấy nhãn từng trace được kiểm. |
| Check Your Trace First (TRCA) — OnlineBoutique | CANDIDATE nếu có nhãn root đúng entity; chưa xác nhận census. | OPEN: cần interval/onset/end đúng nghĩa, không suy từ tên archive. | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. | OPEN: chưa thấy nhãn từng trace được kiểm. |
| OpenRCA — Telecom | CANDIDATE chấm đúng entity OS/pod/database khi census/mapping đủ; không chấm service nếu nhãn chỉ pod. | Có occurrence time; thiếu định nghĩa onset/end độc lập. Query cho khoảng và số lỗi không tương đương detector tự phát hiện. | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. | OPEN: chưa thấy nhãn từng trace được kiểm. |
| OpenRCA — Bank | CANDIDATE chấm đúng entity pod khi census/mapping đủ; không chấm service nếu nhãn chỉ pod. | Có occurrence time; thiếu định nghĩa onset/end độc lập. Query cho khoảng và số lỗi không tương đương detector tự phát hiện. | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. | OPEN: chưa thấy nhãn từng trace được kiểm. |
| OpenRCA — Market | CANDIDATE chấm đúng entity node/pod/service khi census/mapping đủ; không chấm service nếu nhãn chỉ pod. | Có occurrence time; thiếu định nghĩa onset/end độc lập. Query cho khoảng và số lỗi không tương đương detector tự phát hiện. | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. | OPEN: chưa thấy nhãn từng trace được kiểm. |
| OpenRCA 2.0 — TrainTicket | CANDIDATE root set theo cấp nhãn công bố; cần release/census. | CANDIDATE injection-regime nếu khoảng tiêm đủ; onset quan sát OPEN. | Có graph propagation do PAVE tạo từ telemetry/quy tắc; không tự xem là nhãn vùng độc lập để chấm RQ3c. | OPEN: chưa thấy nhãn từng trace được kiểm. |
| OpenRCA 2.0 — OpenTelemetry Demo | CANDIDATE root set theo cấp nhãn công bố; cần release/census. | CANDIDATE injection-regime nếu khoảng tiêm đủ; onset quan sát OPEN. | Có graph propagation do PAVE tạo từ telemetry/quy tắc; không tự xem là nhãn vùng độc lập để chấm RQ3c. | OPEN: chưa thấy nhãn từng trace được kiểm. |
| OpenRCA 2.0 — Hotel Reservation | CANDIDATE root set theo cấp nhãn công bố; cần release/census. | CANDIDATE injection-regime nếu khoảng tiêm đủ; onset quan sát OPEN. | Có graph propagation do PAVE tạo từ telemetry/quy tắc; không tự xem là nhãn vùng độc lập để chấm RQ3c. | OPEN: chưa thấy nhãn từng trace được kiểm. |
| LO2 v1 | Không đủ nhãn root cause service theo nguồn hiện có; đích API không thay nhãn nguyên nhân. | Có thể chấm correct/error ở đơn vị test theo protocol rõ; không mặc định chấm thời gian triệu chứng hoặc service RCA. | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. | Không suy nhãn từng trace từ correct/error của cả test. |
| LO2 v2 | Không đủ nhãn root cause service theo nguồn hiện có; đích API không thay nhãn nguyên nhân. | Có thể chấm correct/error ở đơn vị test theo protocol rõ; không mặc định chấm thời gian triệu chứng hoặc service RCA. | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. | Không suy nhãn từng trace từ correct/error của cả test. |

Nguồn/unit/license từng biến thể: [thẻT-012](../T-012/the-dataset.md), [matrix gốc](../T-012/task-and-source-matrix.md). Khả năng có điều kiện không là census nhãn hay pipeline đã chấm. Bank bảo toàn G3; OpenRCA query/window/sốlỗi cho trước không detector liên tục. PAVEgraph không GT vùng độc lập; LO2correct/errortest không root service.

Tênca/path/root-derivedSLI/mốctiêm không đầu vào detector tự phát hiện. Nhãn chỉ census/chấm hoặc ngân sách họcG1; adapter chưa có nên khôngclaim loại mọi rò nhãn. Loader/shuffle/split công bố không tự splitrepo. Không RCA/training/chọn dev-test trong T003. Không OR symptomprobe thành nhãn vùng hoặc chấmregion từroot.

