# Nezha Online Boutique — thẻ đã kiểm file trong phạm vi

## 1. Danh tính, nguồn và phạm vi đã kiểm

Nezha FSE 2023, nhóm Guangba Yu và cộng sự. Nguồn chính: [README ghim](sources/README.md), [bài](sources/FSE2023_Nezha.pdf), [manifest nguồn/revision](runs/run-001/manifest.json). Stack công bố OTel/Tempo, Promtail/Loki, cAdvisor/Istio/Node Exporter/Prometheus. Công cụ lỗi code Byteman/Hypno/Failpoint; công cụ CPU/network cụ thể chưa khóa từ nguồn đã kiểm, không suy từ tên lỗi.

Repo LICENSE MIT; artifact Zenodo ghi other-open. Chưa xác nhận phạm vi license riêng của dữ liệu và quan hệ phiên bản artifact; công khai không tự chứng minh mọi quyền. Tải ghim Git revision, byte và Git blob hash khớp [download](runs/download-001/manifest.json), không chạy code RCA tác giả.

Trong biến thể này đã đọc toàn 566 CSV được đề xuất, 2677369464 byte, 7753495 hàng CSV tính theo file (không phải unique incident/span), gồm construct/rca trên hai ngày. Không lấy kết quả phương pháp. Quyền Q47; OpenRCA Bank giữ ngoài là bộ khác. [File audit](runs/file-audit-001/summary.json) không parse error; thẻ này không đại diện release khác hoặc phần ngoài inventory.

## 2. Bảng chung tiêu chí MRP §4

| Tiêu chí | Bằng chứng và giới hạn |
|---|---|
| 1. Công khai/giấy phép | Tải thành công, revision/hash khớp. Repo MIT; license data/artifact cần giữ đúng scope, chưa chốt thay tác giả. |
| 2. Root/time | 56 record tiêm, 10 service gốc; thời điểm tiêm không phải onset; clock và bản ghi trùng xem mục5. |
| 3. Cha–con | 170 trace CSV đã đọc; parent scoped trace_id+span_id, root sentinel riêng. Số theo mục4; duplicate/ambiguous không tự resolve. |
| 4. Metric/log/liên kết | 40 resource metric CSV và log có ID; linkage thật theo từng file. Cột TimeStamp có vấn đề ở OB, không sửa dữ liệu. |
| 5. Root/vị trí | Đếm từng root tại cửa sổ quanh tiêm và hai cách hiểu clock; không kết luận bằng graph trung bình. |
| 6. Lỗi | Nhãn nguyên bản nhiều nhóm; không tự tạo nhóm thiếu hoặc suy biểu hiện từ tên nhãn. |
| 7. Triệu chứng ngoài root | Đã khảo sát Duration theo pod+operation, q/control, xem mục6. Vượt ngưỡng không là nhãn vùng hoặc bằng chứng nhân quả. |
| 8. Normal | Trace construct có cửa sổ ngắn; resource metric construct trùng fault ở nhiều file. Strict mask không đủ train/control. |
| 9. Độc lập | Nhóm/collector/công cụ/reuse đối chiếu [ma trận](../T-012/independence-matrix.md); TT/OB cùng họ không tự là hai bộ độc lập. |

## 3. Ca, root, loại lỗi, lần lặp và vị trí

Record tiêm/cell/root lấy từ [labels](runs/run-001/labels.json), [cells](runs/run-001/cells.json), [summary](runs/run-001/summary.json), không đếm CSV thành ca. Loại lỗi: `{"cpu_contention": 16, "return": 7, "cpu_consumed": 10, "exception": 7, "network_delay": 16}`. Giữ lặp từng root×fault/date trong cells; không cộng hai cách hiểu clock thành hai lần lặp.

Graph là quan hệ gọi parent→child giữa service suy từ pod theo alias tên nguồn; không có bằng chứng đủ cạnh message/data-dependency. Dùng toàn minute-file chạm injection±60s, không gọi đó là interval sự cố. Root không thấy không gọi cô lập. [Từng ca/cả hai clock](runs/evidence-002/summary.json).

| Root | Vị trí quan sát trong từng cửa sổ, text hiểu UTC |
|---|---|
| adservice | `{'leaf': 7}` |
| cartservice | `{'leaf': 4}` |
| checkoutservice | `{'intermediate': 8}` |
| currencyservice | `{'leaf': 4}` |
| emailservice | `{'leaf': 5}` |
| frontend | `{'source': 8}` |
| paymentservice | `{'leaf': 4}` |
| productcatalogservice | `{'leaf': 5}` |
| recommendationservice | `{'intermediate': 6}` |
| shippingservice | `{'leaf': 5}` |

## 4. Trace, metric, log và liên kết

Parent counts (đơn vị hàng span theo file): `{'root_sentinel': 82273, 'unique_resolved_within_file': 3580468}`. Mẫu số không-root 3580468; resolved duy nhất 3580468, ambiguous 0. 0 khóa span trùng theo file. Boundary file/lấy mẫu có thể giải thích missing, không tự gọi lỗi tracing. [SQL kiểm độc lập](runs/independent-check-001/result.json) đối chiếu first/last trace mỗi phase/date, toàn bộ census do file-audit thực hiện.

Log cùng tên phút: `{'log_rows': 3958203, 'trace_id_present': 3958203, 'span_id_present': 3958203, 'unique_span_link': 3949012, 'missing_span_link': 9191}`. Khớp (TraceID,SpanID) duy nhất khác có ID khác ghép được clock giữa metric/log/trace. Metric clock TimeStamp−Time text: `{'200000000.0': 2192, '200000210.0': 26, '200000140.0': 24, '200002100.0': 22, '200002000.0': 18, '200001400.0': 22, '200002210.0': 2, '200021000.0': 30, '200021210.0': 2, '200020000.0': 26, '200022100.0': 2, '200020140.0': 2, '200014000.0': 34, '200000200.0': 16, '0.0': 36182}`; không tự sửa. [Schema/kênh/cadence/gap/NaN/constant từng file](runs/file-audit-001/summary.json). Counts overlap giữa normal/fault không là observations độc lập.

## 5. Dữ liệu bình thường, nhãn và mốc thời gian

Root từ pod→service trong labels/cells; inner-service mapping riêng không thay root service. Nhãn có inject_time và inject_timestamp, injection chưa phải onset. Một số TT lệch text/epoch; giữ từng record và hai clock hypotheses trong evidence/trace-symptoms, không đoán timezone hoặc chữa nhãn. Timestamp metric OB có độ lệch lớn so Time text đã kiểm; ghép nguồn phải chọn clock có bằng chứng ở bước dùng sau, không chọn vì kết quả đẹp.

### Dữ liệu bình thường

README gọi construct_data fault-free, nhưng toàn họ có 122 path normal/fault khớp SHA256, gồm resource metric. Do đó không dùng cả construct metric để học clean threshold. Cửa sổ trace normal trong biến thể:

- `online-boutique/construct_data/2022-08-22/trace/03_51_trace.csv`: 23842 span rows, start 1661140219.1492414, end 1661140279.9039414; không tự mở rộng phút ngoài bounds.
- `online-boutique/construct_data/2022-08-23/trace/17_00_trace.csv`: 22969 span rows, start 1661273967.9919088, end 1661274028.1889231; không tự mở rộng phút ngoài bounds.

Metric strict trace bounds không đủ chia ≥2 điểm reference và ≥2 control trên các ngày. [symptoms-003](runs/symptoms-003/result.json) đã kiểm và không sinh calibration hợp lệ; không phải bỏ kiểm do chi phí. symptoms-001 và 002 giữ lại cùng cảnh báo invalid/limited, không dùng kết luận. Trace normal đủ nhiều span để khảo sát Duration nhưng chỉ cửa sổ ngắn, load/recovery/correlation chưa chứng minh sạch/đủ học ngưỡng cho toàn nhiệm vụ.

## 6. Khảo sát triệu chứng ngoài root

Đã kiểm toàn trace normal/fault theo pod+operation, raw Duration (đối chiếu [units](runs/units-001/result.json) với End−Start, đơn vị µs), chronological first half normal reference/second half control, median absolute deviations q=.95/.99/.995; root ghép sau đo. [Kết quả/từng ca/kênh/q/control](runs/trace-symptoms-002/result.json). Không OR qua operation/kênh hoặc gọi exceedance là propagation. Ref n thấp nhất 9, cao nhất 1423; tail có ít mẫu phải đọc n/control ngay cùng số, các span không là quan sát độc lập.

Hai clock có thể phân bổ span khác ca. Interval đến lần tiêm kế tiếp chỉ là cửa sổ mô tả; interval cuối đến hết file không là fault duration. Operation/pod không có normal reference được đếm missing, không zero-score. Thay đổi load, mix operations, lỗi trước chưa recovery và capture boundaries đều có thể gây/che exceedance ngoài root. Vì vậy kết quả hỗ trợ khảo sát thô trên scope, không chứng minh vùng ảnh hưởng hoặc tiêu chí7 đạt mọi ca.

## 7. Task chấm được

| Task | Nhãn và giới hạn |
|---|---|
| Ranking nguyên nhân | Chấm service root theo record tiêm, sau giải clock/mapping/cửa sổ và giao thức G1; nhãn inner-service là task khác. |
| Phát hiện theo thời gian | Trace/log bị cắt theo tiêm, thiếu negative coverage giữa các lần tiêm: không chấm P/R/F1 phát hiện liên tục công bằng từ corpus này riêng lẻ. Metric lưu theo ngày là phạm vi khác; cần giải clock, normal và protocol trước chấm. Injection không phải onset. |
| Vùng ảnh hưởng | Không có nhãn vùng thật đã xác minh; chỉ mô tả vùng nghi ngờ/chứa root khi task sau định nghĩa. |
| Trace anomaly | Không thấy nhãn từng trace trực tiếp; không tự gán mọi trace sau tiêm là anomalous. |

## 8. Rò nhãn và thông tin phục vụ G1

[Kiểm độc lập toàn 101 record](runs/sampling-leakage-001/result.json): trên cả bốn ngày, trace/log/traceid rca_data có đúng các file phút [phút nhãn tiêm, +1, +2], không có các minute-file giữa các lần tiêm. Tổng mỗi modality là 303 = 3×101. Construct chỉ có một trace-file mỗi ngày. Đây là điều kiện chọn khi thu/xuất dữ liệu, không chỉ là cách T008 chọn mẫu. Tên file và việc file tồn tại mang thông tin suy từ nhãn; đổi tên không khôi phục negative coverage bị thiếu. Trace/log phù hợp chấm ranking có điều kiện biết trước cửa sổ, chưa hỗ trợ benchmark tự phát hiện liên tục không biết trước thời điểm từ corpus này riêng lẻ. Không gọi thiếu file là healthy sample hoặc gán trace trong cửa sổ là anomalous.

Toàn họ Nezha có 112 file resource rca được file-audit ghi bounds Time text, mỗi file có cadence/gap trong [bounds từng file](runs/sampling-leakage-001/result.json); đây là file theo service/ngày, không phải 303 minute-file trên. Bounds không chứng minh toàn thời gian là normal; TimeStamp và text có lệch nên không nhập chung clock. Nhãn/tên/path/time và root-derived SLI chỉ dùng census/chấm; adapter chưa có, không claim đã loại mọi rò nhãn. Cùng testbed/stack khác ngày không tự chứng minh độc lập.

## 9. Chi phí và cách dựng lại

Download/hash toàn họ mất 287.828s, whole CSV audit 88.219s; thời gian từng lượt trong manifest/summary, không phải thời gian toàn công việc. Không giải nén file raw. [Plan tải](runs/download-plan-001/plan.json), script `../T-003/scripts/download_verified.py`; kiểm bằng `scripts/inspect_files.py --run <mã_mới>`, `scripts/inspect_trace_symptoms.py --run <mã_mới>` cần run mới nếu chạy lại (không ghi đè). Data không vào git; kết quả/script/manifest giữ repo. Không xóa source sau khảo sát.

## 10. Kết luận phạm vi, phần chưa kiểm và dữ kiện cần

Có root injection và ba nguồn thực, parent/log join đã kiểm toàn file trong inventory, graph/cost/cadence/clock từng file có kết quả. Chưa có onset/end/nhãn vùng hoặc nhãn trace thật để tự suy task; đó là thiếu bằng chứng nhãn, không phải mặc định public dataset phải đủ. Normal resource không đủ bằng chứng sạch, cần timeline/recovery/normal capture bổ sung từ tác giả hoặc giao thức sau có căn cứ. Độ lệch clock và tham chiếu source license cần giải trước dùng kết luận chấm. Không chọn dataset thí nghiệm, không chia dev/test, không RCA/MyRCA. T003 tự phản biện độc lập trước Claude, merged REVIEW tại parent.

---

# Nezha Train Ticket — thẻ đã kiểm file trong phạm vi

## 1. Danh tính, nguồn và phạm vi đã kiểm

Nezha FSE 2023, nhóm Guangba Yu và cộng sự. Nguồn chính: [README ghim](sources/README.md), [bài](sources/FSE2023_Nezha.pdf), [manifest nguồn/revision](runs/run-001/manifest.json). Stack công bố OTel/Tempo, Promtail/Loki, cAdvisor/Istio/Node Exporter/Prometheus. Công cụ lỗi code Byteman/Hypno/Failpoint; công cụ CPU/network cụ thể chưa khóa từ nguồn đã kiểm, không suy từ tên lỗi.

Repo LICENSE MIT; artifact Zenodo ghi other-open. Chưa xác nhận phạm vi license riêng của dữ liệu và quan hệ phiên bản artifact; công khai không tự chứng minh mọi quyền. Tải ghim Git revision, byte và Git blob hash khớp [download](runs/download-001/manifest.json), không chạy code RCA tác giả.

Trong biến thể này đã đọc toàn 599 CSV được đề xuất, 360765178 byte, 953008 hàng CSV tính theo file (không phải unique incident/span), gồm construct/rca trên hai ngày. Không lấy kết quả phương pháp. Quyền Q47; OpenRCA Bank giữ ngoài là bộ khác. [File audit](runs/file-audit-001/summary.json) không parse error; thẻ này không đại diện release khác hoặc phần ngoài inventory.

## 2. Bảng chung tiêu chí MRP §4

| Tiêu chí | Bằng chứng và giới hạn |
|---|---|
| 1. Công khai/giấy phép | Tải thành công, revision/hash khớp. Repo MIT; license data/artifact cần giữ đúng scope, chưa chốt thay tác giả. |
| 2. Root/time | 45 record tiêm, 10 service gốc; thời điểm tiêm không phải onset; clock và bản ghi trùng xem mục5. |
| 3. Cha–con | 137 trace CSV đã đọc; parent scoped trace_id+span_id, root sentinel riêng. Số theo mục4; duplicate/ambiguous không tự resolve. |
| 4. Metric/log/liên kết | 184 resource metric CSV và log có ID; linkage thật theo từng file. Cột TimeStamp có vấn đề ở OB, không sửa dữ liệu. |
| 5. Root/vị trí | Đếm từng root tại cửa sổ quanh tiêm và hai cách hiểu clock; không kết luận bằng graph trung bình. |
| 6. Lỗi | Nhãn nguyên bản nhiều nhóm; không tự tạo nhóm thiếu hoặc suy biểu hiện từ tên nhãn. |
| 7. Triệu chứng ngoài root | Đã khảo sát Duration theo pod+operation, q/control, xem mục6. Vượt ngưỡng không là nhãn vùng hoặc bằng chứng nhân quả. |
| 8. Normal | Trace construct có cửa sổ ngắn; resource metric construct trùng fault ở nhiều file. Strict mask không đủ train/control. |
| 9. Độc lập | Nhóm/collector/công cụ/reuse đối chiếu [ma trận](../T-012/independence-matrix.md); TT/OB cùng họ không tự là hai bộ độc lập. |

## 3. Ca, root, loại lỗi, lần lặp và vị trí

Record tiêm/cell/root lấy từ [labels](runs/run-001/labels.json), [cells](runs/run-001/cells.json), [summary](runs/run-001/summary.json), không đếm CSV thành ca. Loại lỗi: `{"return": 11, "exception": 13, "cpu_contention": 7, "network_delay": 14}`. Giữ lặp từng root×fault/date trong cells; không cộng hai cách hiểu clock thành hai lần lặp.

Graph là quan hệ gọi parent→child giữa service suy từ pod theo alias tên nguồn; không có bằng chứng đủ cạnh message/data-dependency. Dùng toàn minute-file chạm injection±60s, không gọi đó là interval sự cố. Root không thấy không gọi cô lập. [Từng ca/cả hai clock](runs/evidence-002/summary.json).

| Root | Vị trí quan sát trong từng cửa sổ, text hiểu UTC |
|---|---|
| ts-basic-service | `{'intermediate': 7}` |
| ts-contacts-service | `{'leaf': 5}` |
| ts-food-service | `{'intermediate': 6}` |
| ts-preserve-service | `{'intermediate': 2}` |
| ts-price-service | `{'leaf': 3}` |
| ts-route-service | `{'leaf': 5}` |
| ts-security-service | `{'intermediate': 2}` |
| ts-travel-service | `{'intermediate': 6}` |
| ts-travel2-service | `{'intermediate': 3}` |
| ts-verification-code-service | `{'leaf': 6}` |

## 4. Trace, metric, log và liên kết

Parent counts (đơn vị hàng span theo file): `{'root_sentinel': 7209, 'unique_resolved_within_file': 510024, 'ambiguous_within_file': 270}`. Mẫu số không-root 510294; resolved duy nhất 510024, ambiguous 270. 136 khóa span trùng theo file. Boundary file/lấy mẫu có thể giải thích missing, không tự gọi lỗi tracing. [SQL kiểm độc lập](runs/independent-check-001/result.json) đối chiếu first/last trace mỗi phase/date, toàn bộ census do file-audit thực hiện.

Log cùng tên phút: `{'log_rows': 272399, 'trace_id_present': 272399, 'span_id_present': 272399, 'unique_span_link': 272223, 'ambiguous_span_link': 176}`. Khớp (TraceID,SpanID) duy nhất khác có ID khác ghép được clock giữa metric/log/trace. Metric clock TimeStamp−Time text: `{'0.0': 152720}`; không tự sửa. [Schema/kênh/cadence/gap/NaN/constant từng file](runs/file-audit-001/summary.json). Counts overlap giữa normal/fault không là observations độc lập.

## 5. Dữ liệu bình thường, nhãn và mốc thời gian

Root từ pod→service trong labels/cells; inner-service mapping riêng không thay root service. Nhãn có inject_time và inject_timestamp, injection chưa phải onset. Một số TT lệch text/epoch; giữ từng record và hai clock hypotheses trong evidence/trace-symptoms, không đoán timezone hoặc chữa nhãn. Timestamp metric OB có độ lệch lớn so Time text đã kiểm; ghép nguồn phải chọn clock có bằng chứng ở bước dùng sau, không chọn vì kết quả đẹp.

### Dữ liệu bình thường

README gọi construct_data fault-free, nhưng toàn họ có 122 path normal/fault khớp SHA256, gồm resource metric. Do đó không dùng cả construct metric để học clean threshold. Cửa sổ trace normal trong biến thể:

- `train-ticket/construct_data/2023-01-29/trace/08_50_trace.csv`: 4890 span rows, start 1674982096.4780002, end 1674982264.1387653; không tự mở rộng phút ngoài bounds.
- `train-ticket/construct_data/2023-01-30/trace/11_39_trace.csv`: 4595 span rows, start 1675078732.0470002, end 1675078791.208629; không tự mở rộng phút ngoài bounds.

Metric strict trace bounds không đủ chia ≥2 điểm reference và ≥2 control trên các ngày. [symptoms-003](runs/symptoms-003/result.json) đã kiểm và không sinh calibration hợp lệ; không phải bỏ kiểm do chi phí. symptoms-001 và 002 giữ lại cùng cảnh báo invalid/limited, không dùng kết luận. Trace normal đủ nhiều span để khảo sát Duration nhưng chỉ cửa sổ ngắn, load/recovery/correlation chưa chứng minh sạch/đủ học ngưỡng cho toàn nhiệm vụ.

## 6. Khảo sát triệu chứng ngoài root

Đã kiểm toàn trace normal/fault theo pod+operation, raw Duration (đối chiếu [units](runs/units-001/result.json) với End−Start, đơn vị µs), chronological first half normal reference/second half control, median absolute deviations q=.95/.99/.995; root ghép sau đo. [Kết quả/từng ca/kênh/q/control](runs/trace-symptoms-002/result.json). Không OR qua operation/kênh hoặc gọi exceedance là propagation. Ref n thấp nhất 2, cao nhất 101; tail có ít mẫu phải đọc n/control ngay cùng số, các span không là quan sát độc lập.

Hai clock có thể phân bổ span khác ca. Interval đến lần tiêm kế tiếp chỉ là cửa sổ mô tả; interval cuối đến hết file không là fault duration. Operation/pod không có normal reference được đếm missing, không zero-score. Thay đổi load, mix operations, lỗi trước chưa recovery và capture boundaries đều có thể gây/che exceedance ngoài root. Vì vậy kết quả hỗ trợ khảo sát thô trên scope, không chứng minh vùng ảnh hưởng hoặc tiêu chí7 đạt mọi ca.

## 7. Task chấm được

| Task | Nhãn và giới hạn |
|---|---|
| Ranking nguyên nhân | Chấm service root theo record tiêm, sau giải clock/mapping/cửa sổ và giao thức G1; nhãn inner-service là task khác. |
| Phát hiện theo thời gian | Trace/log bị cắt theo tiêm, thiếu negative coverage giữa các lần tiêm: không chấm P/R/F1 phát hiện liên tục công bằng từ corpus này riêng lẻ. Metric lưu theo ngày là phạm vi khác; cần giải clock, normal và protocol trước chấm. Injection không phải onset. |
| Vùng ảnh hưởng | Không có nhãn vùng thật đã xác minh; chỉ mô tả vùng nghi ngờ/chứa root khi task sau định nghĩa. |
| Trace anomaly | Không thấy nhãn từng trace trực tiếp; không tự gán mọi trace sau tiêm là anomalous. |

## 8. Rò nhãn và thông tin phục vụ G1

[Kiểm độc lập toàn 101 record](runs/sampling-leakage-001/result.json): trên cả bốn ngày, trace/log/traceid rca_data có đúng các file phút [phút nhãn tiêm, +1, +2], không có các minute-file giữa các lần tiêm. Tổng mỗi modality là 303 = 3×101. Construct chỉ có một trace-file mỗi ngày. Đây là điều kiện chọn khi thu/xuất dữ liệu, không chỉ là cách T008 chọn mẫu. Tên file và việc file tồn tại mang thông tin suy từ nhãn; đổi tên không khôi phục negative coverage bị thiếu. Trace/log phù hợp chấm ranking có điều kiện biết trước cửa sổ, chưa hỗ trợ benchmark tự phát hiện liên tục không biết trước thời điểm từ corpus này riêng lẻ. Không gọi thiếu file là healthy sample hoặc gán trace trong cửa sổ là anomalous.

Toàn họ Nezha có 112 file resource rca được file-audit ghi bounds Time text, mỗi file có cadence/gap trong [bounds từng file](runs/sampling-leakage-001/result.json); đây là file theo service/ngày, không phải 303 minute-file trên. Bounds không chứng minh toàn thời gian là normal; TimeStamp và text có lệch nên không nhập chung clock. Nhãn/tên/path/time và root-derived SLI chỉ dùng census/chấm; adapter chưa có, không claim đã loại mọi rò nhãn. Cùng testbed/stack khác ngày không tự chứng minh độc lập.

## 9. Chi phí và cách dựng lại

Download/hash toàn họ mất 287.828s, whole CSV audit 88.219s; thời gian từng lượt trong manifest/summary, không phải thời gian toàn công việc. Không giải nén file raw. [Plan tải](runs/download-plan-001/plan.json), script `../T-003/scripts/download_verified.py`; kiểm bằng `scripts/inspect_files.py --run <mã_mới>`, `scripts/inspect_trace_symptoms.py --run <mã_mới>` cần run mới nếu chạy lại (không ghi đè). Data không vào git; kết quả/script/manifest giữ repo. Không xóa source sau khảo sát.

## 10. Kết luận phạm vi, phần chưa kiểm và dữ kiện cần

Có root injection và ba nguồn thực, parent/log join đã kiểm toàn file trong inventory, graph/cost/cadence/clock từng file có kết quả. Chưa có onset/end/nhãn vùng hoặc nhãn trace thật để tự suy task; đó là thiếu bằng chứng nhãn, không phải mặc định public dataset phải đủ. Normal resource không đủ bằng chứng sạch, cần timeline/recovery/normal capture bổ sung từ tác giả hoặc giao thức sau có căn cứ. Độ lệch clock và tham chiếu source license cần giải trước dùng kết luận chấm. Không chọn dataset thí nghiệm, không chia dev/test, không RCA/MyRCA. T003 tự phản biện độc lập trước Claude, merged REVIEW tại parent.
