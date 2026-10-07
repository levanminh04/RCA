# T-023 — Kiểm điều kiện dùng Eadro-TT

Kiểm dữ liệu ngày 05/10/2026; sửa báo cáo ngày 06/10/2026 theo đề xuất R1–R3 Minh đã duyệt. Codex làm; Claude phản biện. **Đã kiểm xong phạm vi được duyệt; chưa quyết nhánh dùng Eadro cho T-027.** Kết luận trong bảng [bang-dieu-kien.csv](bang-dieu-kien.csv) chỉ áp cho điều kiện ghi ở từng dòng.

Metric đạt điều kiện numeric/cadence. Trace và log sau B1 không có bản ghi nằm trong phiên hoặc cửa sổ tiêm theo timestamp gốc. Tuy nhiên, phân loại H−8 đã lưu ủng hộ giả thuyết chênh tọa độ 8 giờ giữa trace/log và nhãn/metric, kết hợp export lịch sử. Đây chưa là xác minh clock nguồn hoặc từng cửa sổ tiêm. Reference có số đo đầy đủ, nhưng tính đại diện và khả năng ghép cùng clock còn OPEN. Chưa đủ căn cứ benchmark ba kênh; FAIL native không chứng minh trace không thể ghép.

## 1. Quyền, đơn vị phiên và nguồn bằng chứng

Một **phiên** là một lượt thu thập dữ liệu, giữ mã đúng như metadata nguồn. Ba phiên dev (phần phát triển) được kiểm; sáu phiên test (phần đánh giá sau khóa thiết kế) không được mở member. **Root** trong nhãn là service bị tiêm lỗi, khác với thư mục gốc của repo; nó chỉ dùng cho bảng audit, không chọn đầu vào phương pháp. Một phiên fault có nhiều sự kiện tiêm liên tiếp; không coi mỗi sự kiện là một phiên độc lập.

Minh đã duyệt đúng phương án trước raw, seed 20261004, ba dev/sáu test, reference/control ngày 21/04 và 145 member. Lời duyệt nguyên văn ở [LOG phiên 2](../../tasks/T-023-kiem-eadro/LOG.md) và [allowlist](allowlist-phien.json). Bản trước/sau và phép kiểm giữ nguyên objects nằm tại [approval-001](runs/approval-001/verification.json). Tên phiên không được dùng căn chỉnh thời gian.

Nguồn số cuối: [stream-002/sessions.json](runs/stream-002/sessions.json), [metric-stats.csv](runs/stream-002/metric-stats.csv), [derived-summary.json](runs/stream-002/derived-summary.json). `stream-001` hoàn tất nhưng bị thay thế sau soát lỗi audit; giữ nguyên lượt và [run-status](runs/stream-001/run-status.json). Không lấy số từ lượt đó để kết luận cuối.

## 2. Selector và B1: PASS trong phạm vi phép kiểm

Kế hoạch §8 khóa H0, H+8 và H−8 trước raw. Chỉ lấy timestamp/điểm kết thúc span hoặc prefix thời gian log để quyết loại bỏ. Khoảng test đóng hai đầu, bao label và metric; không nhãn lấy metric metadata. Bản ghi chạm bất kỳ khoảng cấm dưới bất kỳ H bị loại trước giải mã nội dung. Chỉ lưu đếm theo interval/hypothesis; không lưu ID/service/latency/cạnh/message của phần bị loại. Timestamp thiếu/sai bị loại. Các giả thuyết không được dùng đổi timestamp hoặc dựng cửa sổ đã căn chỉnh.

Framing JSON đi qua byte opaque để tìm record/clock; không `json.loads` toàn trace/processes hoặc log map. Chỉ span qua gate mới được giải mã và resolve đúng process/service; chỉ log qua gate mới đọc service/message. Không lưu payload thô. SHA member là chứng cứ toàn vẹn được yêu cầu, không là ID/signature của record bị loại.

[fixture-002](runs/fixture-002/verification.json) đạt 15 nhóm: payload bẫy, escaped clock alias, clock thiếu/trùng, biên, ba giả thuyết, mọi vai trò, JSON framing, selector, ID/conflict/scope và pre không chứa mốc injection. Kiểm độc lập [check-004](runs/check-004/verification.json) đạt 93 kiểm; [check-005](runs/check-005/verification.json) bổ sung so bảng kết luận/operation/cửa sổ, đạt 96 kiểm. Không mở raw trong hai lượt kiểm độc lập. Phép kiểm này chứng minh hành vi code/fixture và tập output, không chứng minh clock nguồn đúng.

[archive-verification](runs/stream-002/archive-verification.json) xác minh 48.923.113 byte/SHA-256 với manifest T-009 trước mở member. [opened-members.csv](runs/stream-002/opened-members.csv) có đúng 145 member, tất cả byte/hash khớp metadata cũ. Không `testzip()`, không mở TT-all.txz, TT-no-fault.txz, member test, data/locked hoặc repo lưu trữ.

| Mã phiên | Vai trò | Span tổng theo framing | Span loại B1 | Span được phân tích | Log tổng theo framing | Log loại B1 | Log được phân tích |
|---|---|---:|---:|---:|---:|---:|---:|
| 04-18T150729 | dev | 18.544 | 17.162 | 1.382 | 5.663 | 5.663 | 0 |
| 04-18T165807 | dev | 18.429 | 10.583 | 7.846 | 9.713 | 5.713 | 4.000 |
| 04-18T184759 | dev | 18.491 | 0 | 18.491 | 10.016 | 0 | 10.016 |
| 04-21T105158 | reference | 32.420 | 8.751 | 23.669 | 13.668 | 0 | 13.668 |
| 04-21T153246 | control | 32.420 | 0 | 32.420 | 13.668 | 0 | 13.668 |

Nguồn: `sessions.json → trace/log.gate`. Không có record unknown_clock trong năm phiên này. “Được phân tích” chỉ có nghĩa qua B1, chưa có nghĩa thuộc phiên. Min/max phủ khoảng test không chứng minh có record ở mọi khoảng: phiên dev thứ ba có range rộng nhưng không record nào chạm vùng cấm dưới ba H. Reference có 8.751 span bị loại theo H−8 vì rơi vào phiên không nhãn; nội dung chúng không được kiểm.

## 3. Clock, phiên và log identity

**FAIL cho ghép theo timestamp native hiện tại.** Toàn năm phiên có 0 span và 0 dòng log safe trong khoảng session native. Cả 54 cửa sổ pre/post của 27 sự kiện dev đều có 0 span/log safe theo clock đó. Nguồn: [trace-window-coverage](runs/stream-002/trace-window-coverage.csv), [log-window-coverage](runs/stream-002/log-window-coverage.csv), [event-audit](runs/stream-002/event-audit.csv). Không diễn giải số 0 này là không có lỗi hoặc root là service cô lập.

Phân loại đã lưu trong `sessions.json → trace/log.gate.admitted_classifications` cung cấp bằng chứng khác với coverage native. H0/H+8 đều có 0 bản ghi safe khớp chính khoảng phiên; H−8 cho bảng dưới. Các giả thuyết này đã khóa trước raw để loại bỏ theo B1. Trình bày số đếm không đổi timestamp đầu vào và không lựa chọn clock.

| Phiên | Span safe | H−8 khớp chính khoảng phiên | H−8 khớp phiên khác | H−8 ngoài khoảng đã biết | Log safe | Log H−8 khớp chính khoảng phiên |
|---|---:|---:|---:|---:|---:|---:|
| dev 150729 | 1.382 | 0 | 0 | 1.382 | 0 | 0 |
| dev 165807 | 7.846 | 6.814 | 0 | 1.032 | 4.000 | 4.000 |
| dev 184759 | 18.491 | 17.196 | 263, dev 165807 | 1.032 | 10.016 | 10.016 |
| reference | 23.669 | 23.669 | 0 | 0 | 13.668 | 13.668 |
| control | 32.420 | 23.719 | 8.701, reference | 0 | 13.668 | 13.668 |

“Khớp khoảng phiên” ở đây là giao khoảng span [start,end] với khoảng metadata đóng, hoặc timestamp log nằm trong khoảng đó. Không đồng nghĩa đã kiểm normal/incident theo từng cửa sổ. Đếm này chỉ áp cho bản ghi qua B1; phần bị loại không có phân loại H−8 theo từng record để khôi phục.

Đối chiếu biên từ năm `*-safe-spans.csv` với `allowlist-phien.json → B1.intervals` cho bảng dưới. Mốc so trực tiếp là `metric_start_s`/`metric_end_s`, lấy từ sample metric đầu/cuối; không suy từ tên phiên. Cột `end_s` là biên cuối khoảng phiên B1, có thể muộn hơn sample metric cuối. “Span đầu/cuối” dùng `native_start_s − 28800` nhỏ nhất/lớn nhất trong nhóm khớp chính khoảng phiên.

| Phiên | Span đầu − metric_start_s | Span cuối − metric_end_s | Span cuối − end_s | Span safe gần nhất trước phiên, tọa độ H−8 | Span safe sau end_s |
|---|---:|---:|---:|---|---:|
| dev 150729 | không có | không có | không có | 17/04 22:27:16,415 | 0 |
| dev 165807 | +4.077,633 s (67,961 phút) | −51,069 s | −52,726 s | 16/04 12:44:18,511, khối lịch sử | 0 |
| dev 184759 | +0,343 s | −45,943 s | −47,894 s | 18/04 02:44:55,931, thuộc dev 165807 | 0 |
| reference | +0,090 s | −11,540 s | −12,545 s | không có | 0 |
| control | +0,742 s | −22,388 s | −24,350 s | 20/04 21:06:52,460, thuộc reference | 0 |

Giờ/ngày trong bảng là cách hiển thị tọa độ số sau H−8, chưa xác nhận timezone nguồn. Control không có span safe giữa khối reference và span own đầu; span trước phiên cách sample metric đầu 2 giờ 25 phút 53,540 giây. Trong cả năm file, không span safe nào bắt đầu hoặc kết thúc sau `end_s` dưới H−8. Đây là đối chiếu output đã lưu, không tạo input đã dịch giờ hoặc kiểm từng cửa sổ tiêm.

**Biên đầu khớp metric dưới một giây ở ba phiên, củng cố H−8 kết hợp export lịch sử.** Dev 184759, reference và control lần lượt khớp trong 0,343/0,090/0,742 giây. Bằng chứng này mạnh hơn số đếm giao khoảng phiên và làm giải thích trễ báo đơn thuần yếu đi; không để nó ngang hàng với chênh tọa độ 8 giờ. Bốn phiên còn trace/log safe tại chính khoảng phiên dưới H−8, trong khi H0/H+8 không có; dev đầu không còn bản ghi safe khớp chính phiên. Mẫu overlap ở mục 4 phù hợp với export tích lũy. Nguồn clock, đồng hồ nào lệch và timezone/cách biểu diễn thời gian vẫn OPEN; biên phiên chưa xác nhận quan hệ với từng mốc tiêm.

Span `startTime/duration` được chiếu từ microsecond sang giây theo schema Jaeger/độ lớn đã mô tả ở `results/T-009/the-dataset.md:272`; metric là epoch giây. Log được chiếu từ prefix thời gian, timezone nguồn chưa xác minh: tọa độ wall-time dùng cho B1 không xác nhận UTC thật. Đối chiếu trực tiếp biên span với sample metric ở trên là bằng chứng giữa hai trục thời gian, khác việc so minimum với tên phiên. **OPEN cho mức cửa sổ tiêm và nguồn clock; chưa có nguồn xác nhận hoặc phép kiểm 54 cửa sổ theo H−8, chưa được phép căn chỉnh trong task này.**

**Biên phần safe sát biên cắt B1; phạm vi dev còn lại đã định lượng được.** Dev 150729 có span safe cuối ở native 18/04 06:27:16,415, trước khoảng test 222801 dưới H0 bắt đầu 06:28:01 đúng 44,585 giây. Dev 165807 có span own safe đầu ở native 18/04 10:06:04,632604, sau khoảng test 001753 dưới H0 kết thúc 10:05:34,046788 đúng 30,586 giây; từ khối 16/04 tới đó không có span safe. Nếu H−8 đúng, B1-H0 cấm 67,451 phút đầu của khoảng dev 165807; span own safe đầu xuất hiện sau metric đầu 67,961 phút. Đây là censor (cắt dữ liệu) theo thời gian có hệ thống, nên không thể dùng phần safe rỗng để kết luận export bắt đầu muộn hoặc nguồn không có span. Output không giữ timestamp của phần bị loại để xác định số record own đã mất hoặc loại trừ export cũng thiếu dữ liệu.

| Phiên dev | Span safe khớp chính phiên H−8 | Khoảng từ span own đầu tới cuối | Ô 60 giây có ít nhất một span own / tổng ô phiên |
|---|---:|---|---:|
| 150729 | 0 | rỗng, 0 phút | 0/108 |
| 165807 | 6.814 | 02:06:04,632604–02:44:55,931; 38,855 phút, khoảng 39 phút cuối | 40/108 |
| 184759 | 17.196 | 02:47:59,343–04:34:52,057; 106,879 phút, gần đủ phiên | 107/108 |

Nguồn: cùng safe-spans CSV, B1 và phân loại trong `sessions.json`. Ô phút được neo tại `metric_start_s`: `floor((native_start_s − 28800 − metric_start_s)/60)`; tổng ô là `ceil((metric_end_s − metric_start_s)/60)`. Reference/control đều 135/136 ô theo cùng định nghĩa. Độ dài từ span đầu tới cuối không chứng minh mọi thời điểm giữa chúng có span; ô có một span cũng không xác nhận đủ operation/service hoặc cửa sổ tiêm. Vì vậy khoảng 39 phút của dev 165807 khác số 40 ô phút chạm dữ liệu. Phần dev còn lại lệch về cuối ngày, không phải mẫu ngẫu nhiên của ba phiên.

Output `denied_by_interval_hypothesis` ghi dev 150729 có 14.705 span/5.663 log bị loại bởi H0 tại interval test 222801, và dev 165807 có 9.810 span/5.713 log tại test 001753. Chúng nằm trong member dev đã duyệt. Đây không phải số record own bị mất: một phần có thể thuộc khoảng phiên khác dưới H−8. Số own bị loại **chưa kiểm**, vì không giữ timestamp/phân loại H−8 của từng record bị loại và quyền hiện tại không cho mở lại chúng. Kiểm trên output safe không thể khôi phục phần đã loại; đọc lại phần đó cần Minh duyệt phạm vi B1 mới.

Log `Span reported` vẫn ghép được với identity span đã qua B1: dev thứ hai 1.600 match không conflict, dev thứ ba 3.992, reference/control mỗi phiên 5.494; service khớp ở mọi match này. Q50 chênh log−span native khoảng 0,0044–0,0052 giây, nhưng max hai dev tới 162,1554/65,0390 giây. Dev đầu không còn log safe để ghép. Nguồn: `sessions.json → native_identity_log_join`, các file `*-safe-log-links.csv`. Không dùng match conflict làm một timestamp đại diện.

Ghép ID/service và chênh native nhỏ là bằng chứng trace/log chia sẻ một trục thời gian trong phần ghép được; chưa chứng minh cùng clock với metric hoặc cùng phiên tiêm. Offset kết hợp cumulative export (xuất tích lũy) phù hợp với phân loại H−8 và overlap. Dịch toàn file mà không tách lịch sử không đủ giải quyết lineage (nguồn gốc theo phiên); overlap không bác khả năng tách theo thời gian dưới một clock được xác minh. Chưa áp H−8 hay gọi dữ liệu đủ ba kênh.

## 4. Identity và cấu trúc trong phần safe

Khóa `(session,traceID,spanID)`; signature là toàn span cùng service resolve. Cùng khóa/cùng signature là exact-copy; nhiều signature là conflict, giữ riêng. Không last-wins. Khóa thiếu/sai không thành usable identity; năm phiên có 0 dòng ID thiếu/sai. Graph chỉ dùng child và parent identity không conflict trong phần safe.

| Phiên | Khóa span unique | Khóa conflict | Dòng exact-copy dư | Identity dùng được | Parent reference từ child dùng được | Parent unique identity | Parent conflict | Parent thiếu trong safe |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| dev 150729 | 440 | 136 | 734 | 304 | 289 | 160 | 129 | 0 |
| dev 165807 | 1.958 | 136 | 5.680 | 1.822 | 1.548 | 1.417 | 129 | 2 |
| dev 184759 | 4.492 | 148 | 13.749 | 4.344 | 3.641 | 3.510 | 131 | 0 |
| reference | 5.522 | 0 | 18.147 | 5.522 | 4.580 | 4.580 | 0 | 0 |
| control | 7.912 | 0 | 24.508 | 7.912 | 6.668 | 6.668 | 0 | 0 |

Nguồn: `sessions.json → trace.identity`; đếm độc lập ở check-004. Exact-copy dư là tổng multiplicity−1 theo variant, không gồm thêm variant conflict. Mẫu số parent chỉ gồm child identity usable; child conflict không dựng cạnh. Không có multiple-parent trong phần này. Parent lặp exact là nhiều dòng giống hệt một identity, khác parent ambiguous do conflict.

Số conflict ở bảng trên thuộc toàn phần safe của file, chưa là conflict tại incident. Phân tầng thời gian từ ba `*-safe-spans.csv` cho bảng dưới; phép đếm khóa/signature và lệnh tái lập ở [LOG phiên 3](../../tasks/T-023-kiem-eadro/LOG.md). Nhóm H−8 chỉ dùng để mô tả bằng chứng của giả thuyết đã khóa, không là input phương pháp đã căn chỉnh.

| Phiên dev | Dòng ở khối native 16/04 | Khóa unique trong khối | Conflict trong khối | Dòng khớp chính phiên dưới H−8 | Conflict trong nhóm đó |
|---|---:|---:|---:|---:|---:|
| 150729 | 1.032 | 358 | 136 | 0 | 0, nhóm rỗng |
| 165807 | 1.032 | 358 | 136 | 6.814 | 0 |
| 184759 | 1.032 | 358 | 136 | 17.196 | 12 |

Khối native 16/04 ở cả ba dev nằm ngoài mọi khoảng B1 đã biết dưới H0/H+8/H−8. Vì vậy không gán 136 conflict lịch sử cho cửa sổ incident. Dev 184759 vẫn có 12 conflict ở nhóm khớp chính khoảng phiên theo H−8; không kết luận mọi conflict đều vô hại hoặc chỉ thuộc lịch sử. Clock và identity theo từng cửa sổ vẫn chưa xác minh.

**FAIL** cho việc gộp last-wins các conflict toàn phần safe; con số đó không tự chặn mọi trace incident hay xác nhận graph tại injection. Hai parent không có trong safe không chứng minh thiếu trong export gốc: chúng có thể thuộc phần B1 đã cắt. Không kiểm conflict/ID/cạnh xuyên qua phần bị loại vì không được giữ ID phần đó.

[cross-session-overlap.csv](runs/stream-002/cross-session-overlap.csv) có 2.390 variant cùng toàn nội dung span/service giữa reference và control. Chúng ứng với 8.701 dòng control ở khối native 21/04 04–05h, khớp khoảng reference dưới H−8. Ba cặp dev có 222/222/324 variant giống hệt: hai cặp với dev 150729 có 222 variant ứng 688 dòng/file, đều ở khối 16/04; riêng 263 dòng dev 184759 ở khối 18/04 10h là nội dung chung với dev 165807 và khớp khoảng phiên trước dưới H−8. Nguồn: safe-spans CSV của các phiên cùng bảng overlap. Mẫu này phù hợp với export tích lũy; không bác giả thuyết offset kết hợp lọc lịch sử theo thời gian. Toàn export normal chưa được chứng minh độc lập, nhưng cũng chưa kiểm tính độc lập sau một phép ghép/lọc được xác minh. Không gộp identity giữa phiên, gọi cả file clone hoặc coi mọi bản ghi lặp là lỗi.

Phần trace safe toàn file dev có 19 service/38 cặp service-operation mỗi phiên; reference/control có 13/24. [normal-operation-coverage.csv](runs/stream-002/normal-operation-coverage.csv) cho 42/114 cặp dev-session×operation không có mẫu reference safe. Đây là coverage lịch sử, chưa là normal/incident cùng cửa sổ. `span.kind` và `http.status_code` có trong mọi span safe, nhưng không thấy tag `error`, `hostname`, `peer.service`, `instance` được kiểm; không suy mọi kiểu instance tag khác đều thiếu. Không dùng status hoặc regex tên service để tự dựng mapping T/S/L/E.

## 5. Metric và tính đại diện của reference

**PASS numeric/cadence.** Năm phiên đều có 27 service × 7 kênh: cpu_usage_system/total/user, memory_usage/working_set, rx_bytes/tx_bytes. Tổng 6.727.833 giá trị finite, 0 invalid, 0 timestamp trùng và 0 bước cadence khác 1 giây. Dev có 6.462/6.461/6.460 điểm mỗi kênh; hai normal mỗi kênh 8.107 điểm. Nguồn: metric-stats và derived-summary. Đơn vị nguồn/biến đổi rx/tx còn OPEN; không tự coi bytes là request traffic, CPU/memory là SLI, hoặc thiếu latency/errors là lỗi của mọi scorer numeric.

Kênh hằng toàn phiên lần lượt 25/27/25/29/25 trên 189 cặp service×kênh mỗi phiên. Reference có 134/189 cặp IQR=0, gồm cả các cặp không hằng toàn phiên. Phiếu/scorer cần variance hoặc IQR phải dùng policy đúng giao thức; không bỏ kênh hoặc thêm epsilon mới trong task. Phân vị mô tả dùng giá trị thứ `floor((n−1)p)` của dãy đã sắp; cột median là Q50 theo quy tắc này, không nội suy. Đây không là cấu hình quantile của một phương pháp RCA.

Đã so reference với control ở đủ 189 cặp service×kênh, và với **mọi 27 đoạn pre đã khóa** ở đủ 5.103 cặp; tổng 5.292 so sánh. Có 24 đoạn dài 114,1415–124,4105 giây và ba đoạn đầu khoảng 2,7 giây. Đoạn đầu chỉ có ba sample, báo riêng và không coi đủ reference 300 giây. Pre/post dùng [start,end), không tính sample đúng mốc injection vào pre. Không bỏ đoạn hoặc chọn “sạch” sau số đo. Nguồn: [reference-comparisons](runs/stream-002/reference-comparisons.csv), metadata events và event-audit.

Chênh Q50 control−reference chia IQR reference chỉ tính được **55/189** cặp; 134 cặp IQR=0 để NA, không gán 0. Với 55 cặp đó, Q50 tỷ số khoảng 0,0141; min/max −33,2/+6. Ví dụ memory của ts-food-service có chênh tuyệt đối rất nhỏ nhưng IQR reference còn nhỏ hơn; tỷ số lớn không tự chứng minh fault hoặc tải khác. Không lấy một trung bình/median chung làm PASS đại diện. Bảng đầy đủ giữ delta, scale và mẫu số cho từng pre/service/kênh.

[normal-quarters.csv](runs/stream-002/normal-quarters.csv) báo Q50 của bốn phần thời gian bằng nhau đã cố định cho mọi service/kênh của hai normal, gồm phần đầu. Đây là kiểm warm-up/drift mô tả, không cắt warm-up hoặc đổi nguồn học. Chênh mức có thể do tải, biến thiên bình thường, scale/đơn vị hay drift; chưa có workload ground truth để phân xử. Nhãn `faults=[]` xác nhận không có sự kiện tiêm được ghi, chưa chứng minh không có sự cố nền, đại diện cho dev hoặc reference calibration tốt. **OPEN đại diện**, không bắt reference PASS từ finite/cadence.

## 6. Điều kiện theo chức năng và đề xuất cho T-027

| Chức năng | Kết luận trong T-023 | Hệ quả |
|---|---|---|
| BARO, N-Sigma scorer, CIRCA-PC | PASS riêng schema numeric | BARO/N-Sigma có thể là ứng viên metric; normal/config vẫn phải hợp lệ. CIRCA-PC thuộc tầng 2 (Q-62); Q-67 yêu cầu báo không chạy đủ trong ngân sách trên Train Ticket, nên PASS schema không đưa nó vào phạm vi chạy T-027. Chưa đo chi phí CIRCA-PC Eadro. |
| N-Sigma/BOCPD detector | OPEN | Chọn cột/cấu hình/reference và ý nghĩa alarm tài nguyên/SLI phải theo giao thức được duyệt; không suy fallback numeric thành cấu hình đã chọn. |
| TORAI bản sửa | OPEN | Cần logts và metric cùng time/service; log native không phủ cửa sổ, trace không thay được log. |
| SimpleRCA M4 | OPEN | Metric đủ numeric; trace/log vote cùng cửa sổ chưa đủ. Chạy partial modality là lựa chọn riêng, không gọi phiếu thiếu là không lỗi. |
| TraceRCA finite | OPEN khả năng dùng; FAIL coverage native hiện tại | Cần operation/service, duration và reference cùng clock/cửa sổ. Không đòi parent cho phiếu span của bản này. |
| MicroRank bản sửa | OPEN khả năng dùng; FAIL coverage native; conflict có trong toàn phần safe | Phần lớn conflict dev ở khối lịch sử 16/04; nhóm khớp chính phiên dưới H−8 của dev 184759 vẫn có 12 conflict. Chưa xác minh identity/graph theo cửa sổ. Ngoài clock cần operation/normal; conflict không gộp. Yêu cầu kind/instance theo đúng nhánh. |
| CIRCA kiến trúc | OPEN | Numeric không đủ mapping T/S/L/E/SLI và graph có provenance cùng clock. Không lấy nhãn root chọn SLI. |

Nguồn điều kiện: hồ sơ T-013–T-017; đặc biệt `results/T-015/tracerca-rcaeval.md` §1/§7, `ho-so-microrank.md` §1 và phần bản sửa; `results/T-014/ho-so-circa-kien-truc.md:170`; T-016 phần đầu vào, T-017 §1/§2. Bảng bang-dieu-kien chỉ chốt từng điều kiện cần, không accuracy hoặc causal graph.

**Các CANDIDATE trình Minh, chưa chọn:**

- Duyệt một phạm vi kiểm cửa sổ theo H−8 trên phần output đã qua B1. Lý do cân nhắc: biên đầu trace/metric khớp dưới một giây ở ba phiên, cùng bằng chứng export lịch sử. Phép kiểm này **chưa kiểm ở mức cửa sổ**, cần duyệt riêng vì quyền hiện tại chỉ dùng H để loại bỏ, cấm căn chỉnh. Phạm vi trace dev thực có: 150729 rỗng; 165807 khoảng 39 phút cuối (38,855 phút từ span đầu tới cuối, 40/108 ô phút); 184759 gần đủ (106,879 phút, 107/108 ô). Nó chủ yếu trả lời cho dev cuối và phần cuối dev thứ hai, chưa đại diện toàn dev và không phục hồi phần B1 đã loại.
- Nếu Minh chấp nhận H−8, cân nhắc duyệt sửa B1 riêng cho member dev, ví dụ bỏ H0 khỏi hợp loại bỏ của các member đó, để kiểm lại phần đang bị cắt. Đây là phương án **CANDIDATE, chưa kiểm**, cần quyền/phạm vi mới trước mọi đọc lại; không đổi allowlist hoặc chạy trong lượt này. Rủi ro: nếu H0 đúng, phần đọc lại có thể là telemetry thuộc thời gian test dù nằm trong member dev đã duyệt. Phương án chỉ mở khả năng khôi phục dữ liệu bị cắt, không bảo đảm dữ liệu own có đủ hoặc giải quyết clock/identity/reference; phải giữ mọi lượt cũ.
- Giữ Eadro như ứng viên metric, báo alarm tài nguyên và kiểm normal theo giao thức; chưa dùng trace/log ghép phiên hoặc graph/ba phiếu. Đây là phương án giới hạn phạm vi, không phải kết luận trace chắc chắn không ghép được.
- Chờ nguồn clock/lineage đủ và một phạm vi kiểm mới được duyệt, hoặc bỏ Eadro khỏi nhánh cần ba kênh, kèm giới hạn cho Q-61.

Các phương án chưa kiểm hiệu năng/accuracy vì ngoài task. Chúng có thể không phù hợp nếu metric normal không đại diện, mapping không xác minh được, H−8 không là quan hệ clock thật hoặc phần safe không đủ cửa sổ. Bằng chứng H−8 cũng có thể mở khả năng dùng trace nếu được xác minh sau này. Duyệt sửa báo cáo ngày 06/10 không là duyệt phương án kiểm mới hay chọn nhánh T-027; Minh quyết bước kế tiếp.

## 7. Giới hạn, chi phí và bàn giao

Dev chỉ gồm export khoảng 18 nghìn span: 18.544/18.429/18.491 trước B1. Hai phiên test có 33.250/33.332 span; không suy kết luận dev sang kiểu đó. Nguồn: `results/T-009/runs/inspect-004/raw-sessions.json`, bản số/mapping ở [population-metadata](runs/approval-001/population-metadata.json). Ba dev cùng ngày, root dev/test khác nhau, chín đơn vị fault ít; không chọn lại seed. T-009/T-021 đã từng khảo sát telemetry trước split này; test mới không được gọi hoàn toàn chưa nhìn. T-023 không đọc mới nội dung bị cấm và không xóa tiếp xúc lịch sử.

Run cuối stream-002 khoảng **264,109 giây**, RAM peak working set **145.293.312 byte**, logical member **367.776.611 byte**. Run thay thế stream-001 khoảng 234,203 giây; cộng hai lượt streaming khoảng 498,312 giây và 735.553.222 byte logical, không tính đây là I/O vật lý hay benchmark phương pháp. Nguồn: hai `cost.json`; run đầu RAM nội bộ null, có process observation một thời điểm, không giả vờ biết peak toàn lượt. Không có parsing nặng khác/pilot T-022/T-030 tại snapshot trước mỗi lượt. Không tải/cài/EC2/commit. Giữ mọi lượt lỗi metadata và mọi lượt streaming.

Elapsed từng member và progress đã được ghi từ đầu. Timestamp bắt đầu/kết thúc tuyệt đối từng member chưa được thu ở hai lượt, giữ OPEN thay vì dựng lại từ mtime; đây là thiếu trường log so với kế hoạch, không thay các timestamp dữ liệu hoặc hash/order guard đã kiểm. Chi phí là quan sát trên laptop, không là so sánh hiệu năng độc lập giữa phương pháp.

Script chạy lại chỉ khi cần kiểm thay đổi, dùng run-id mới và giữ stdout/stderr. Không chạy `build_metadata.py` sau duyệt: script cũ tạo lại proposal, không là bước tiếp theo. Kế hoạch §1–7 giữ văn bản trước raw; trạng thái “chưa duyệt” trong phần cũ được thay về quyền bởi bổ sung §8 và allowlist, không là trạng thái hiện tại. Kiểm rẻ dùng fixture/check từ output; không mở test hoặc đổi plan/clock cho kết quả đẹp. Nháp WHY đã cập nhật trong phạm vi task; DECISIONS/WHY chung chưa được ghi. Lời duyệt và các lựa chọn mới cần Minh duyệt dòng nguồn chung riêng. Claude đã phản biện, Codex đã phản hồi và sửa R1–R3 theo đề xuất được duyệt; bước tiếp theo là Minh xem bản sửa, quyết nhánh/phạm vi kiểm tiếp và việc ghi nguồn chung. Chưa đóng task hoặc benchmark T-027. Manifest handoff-001 là snapshot trước sửa báo cáo, được giữ nguyên; nguồn số stream-002 không đổi.
