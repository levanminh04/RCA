# Đổi nguồn normal N trên Nezha-OB — T-042, Q-191

Đã thực hiện gói Minh duyệt: chỉ đổi N trên 22 ca dev, giữ A = 300 giây và các phương pháp/cấu hình. Kết quả không hỗ trợ nhận định rằng chỉ thay N bằng construct_data sẽ khắc phục độ lệch OB. Có tác động thật, gồm mất kênh do thiếu mẫu và kích hoạt fallback; chưa xác định normal có sạch hơn hoặc chương trình sinh bảng công bố.

## Kết quả và cách đọc

Top1/MRR chính dùng kỳ vọng hòa của evaluator P3; “native” là thứ tự trả về thực tế, cùng mẫu số 22. Hai độ đo được tách vì M4 mất metric tạo nhiều hòa. Không so hai quy tắc như cùng một số.

| Phương pháp | Top1 kỳ vọng cũ → N mới | MRR cũ → N mới | Top1 native cũ → N mới | ΔTop1 kỳ vọng, điểm % |
|---|---:|---:|---:|---:|
| M4 | 0.318182 → 0.367424 | 0.537542 → 0.555250 | 7/22 → 6/22 | +4.924 |
| MAIN | 0.681818 → 0.500000 | 0.782147 → 0.684222 | 15/22 → 12/22 | -18.182 |
| MICRO | 0.000000 → 0.000000 | 0.170139 → 0.163059 | 0/22 → 0/22 | +0.000 |

Nguồn số: evaluate-003/evaluation.json#/summary; từng ô ở /by_cell, từng ca ở /cases và evaluate-003/tables.md. M4 có 20 ca OK và 2 ca NO_EVIDENCE khi chấm; không bỏ 2 ca ấy. MAIN vàMicro có 22 ca OK. “OK” ở đây là có đầu ra, không xác nhận phương pháp đúng hoặc nguồn normal sạch.

## Đầu vào thực và phần khác converter

26 file được ghim từ manifest tải T-008, tổng 41.268.767 byte; không tải thêm. Mỗi ngày11 metric, 1 log, 1 trace. Chỉ decode giá trị trong hai phút UTC được duyệt. Giữ 165 kênh và clock Time của P3; không thêm Node, không dùng TimeStamp. Trace giữ start>=low và end<high, log/metric [low,high). Converter dùng TimeStamp, trace-start và biên đóng; các khác biệt ấy không bị giấu thành “tái lập tác giả”. A và membership từng phương pháp giữ nguyên; fingerprint trong input-audit.json mỗi ca. N ngày 23 nằm sau một số ca nên bộ bọc Micro truyền nhóm nguồn trực tiếp, không dịch timestamp.

| Ngày | Mẫu hữu hạn/kênh metric | Span N | Log N | Hull trace / log, giây |
|---|---:|---:|---:|---|
| 2022-08-22 | 1 trên cả 165 kênh | 7934 | 8518 | 19.904 / 19.824 |
| 2022-08-23 | 1 trên cả 165 kênh | 11211 | 12124 | 28.171 / 28.179 |

Miền danh nghĩa một phút chỉ giữ phần capture thực có trong file, không dời file hay kéo thêm phút cho đủ dữ liệu. Không coi tên construct_data/normal là chứng minh khỏe. Hồ sơ T-008 đã cảnh báo metric trùng byte với cây lỗi; điều đó không tự chứng minh hai miền chọn ở đây nhiễm lỗi. MAIN còn dùng normal_metric ở đường dẫn riêng trong source adapter; nguồn chính xác của file lịch sử ấy vẫn OPEN.

## Chuỗi cơ chế và đối chiếu ca đúng/sai

**M4:** một mẫu < min_normal_metric=2 → toàn 3.630 kênh–ca metric unavailable → phiếu metric bằng0; log A giữ nguyên, 16 phiếu trace trong 220 service–ca đổi vì N khác. Đây là mất thông tin do độ phủ đầu vào kết hợp quy tắc đủ mẫu, không phải chứng minh normal sạch hơn.

- Ca dev-3e27669440 (adservice CPU): root metric 32→0, trace 1→1, tổng 33→1; frontend giữ trace+log=2. Root từ hạng 1 xuống2. Cùng điều kiện mất metric nhưng dev-7d3c2fe6d1 (shipping CPU) vẫn hạng 1 vì trace root còn1, các service khác0.
- Ca dev-1ac905bc95 (frontend return): root giữ log 1, các phiếu metric của đối thủ bị mất; root từ vị trí5–6 lên1. Đây là cải thiện nhờ loại bớt bằng chứng cạnh tranh, chưa xác nhận metric cũ là triệu chứng sai hay nền mới tốt hơn.
- Ca dev-2bfc97b01e (checkout network): root metric 16→0, không có phiếu log/trace → cả phương pháp abstain. Không chấm một root được ưu tiên ngẫu nhiên thành đúng.

**MAIN M0:** CPU/network chỉ 1 N/pool → fallback lấy A tính ngưỡng. Có 440 pool fallback (trước 0), cả 440 không phát cảnh báo. Pool latency vẫn đủ 5 giá trị nhờ gộp nhiều metric tại một thời điểm; không phải 5 mốc normal độc lập. Trace A và score trace không đổi; log normal và fusion giữ nguyên quy tắc gốc.

- Ca dev-2bfc97b01e: CPU root trước 1 alert×100, sau fallback0; latency sau 1 alert×20. Score root 100→20, hạng 1→5. Trong cùng cấu hình fallback, dev-9b9397a4dc (recommendation CPU) lại có 10 alert latency×20, score metric 100→200 và hạng 2→1. Vì vậy không gán mọi ca tăng/giảm cho một lá cờ fallback.

- Đối chiếu cùng ô shipping CPU-contention: dev-14701a3bbb có score root 660,05→280, đối thủ checkout lên 282,41 qua nhánh trace nên root xuống2. Ca dev-7d3c2fe6d1 vẫn giữ hạng 1: root 950→240 còn trên checkout 100. Cùng điều kiện fallback chưa đủ dự đoán sai/đúng; phải lần tiếp phép fusion và đối thủ.

**MicroRank repaired sham:** SLO/nhóm trace thay đổi ở 22/22 ca; đủ operation và std N, không fill. Hai nhóm vẫn rời nhau, A không đổi; weights, spectrum và phép ef²/(ep+nf) đã kiểm. Top1 vẫn 0, MRR giảm khoảng 0,708 điểm %. Điều này loại lời giải “chỉ đổi nguồn N này là đủ cứu sham”, không bác bỏ mọi nguồn N hay mọi bản MicroRank.

- dev-27252dca60:100 trace bất thường thay 94, root productcatalog từhạng 3 xuống4. Operation ReadCatalog của root có mean/std 3,56/5,05 ms→3,50/4,39 ms; score root đại diện 299,297→124,488, trong khi cartservice đạt 136,231 và các đối thủ khác còn cao hơn.
- dev-8ecd9880ed: nhóm bất thường 180→437 trên cùng 751 trace; checkout hạng 9→8, vẫn thấp hơn các service khác. N có tác động nhưng không đủ làm root dẫn đầu. Không dùng “Top1 không đổi” để nói mọi trung gian không đổi.

Nguồn đầy đủ cho mọi ca đúng/sai và đối thủ: evaluate-003/mechanism-chains.json.gz#/chains; số tổng hợp tại mechanism-summary.json. Các ví dụ minh họa chuỗi đã lưu, không thay bảng toàn 13 ô và 22 ca.

## Kiểm đầu–cuối N và giới hạn hồi phục

Đã so hai mẫu đầu/cuối trên 3.630 kênh–ca, bỏ mẫu giữa theo kế hoạch. Thống kê chuẩn hóa xác định ở 3042, còn 588 không xác định vì phương sai0/thiếu. Median |delta|/std5=1.093941, P90=1.866629. Có 1481 delta dương, 1502 âm, 647 bằng 0 theo giá trị binary64. Không coi mỗi dấu khác0 là thay đổi vật lý; có kênh chênh ở độ chính xác lưu số.

Nguồn dùng trong kết luận là F2-stable-001/summary.json và /cases/*.json.gz. F2 NumPy ban đầu được giữ để truy vết; 5 kênh gần hằng vượt cận Cauchy do làm tròn mean, nên đã tính lại riêng thống kê bằng hữu tỷ chính xác của cùng binary64, không floor/epsilon, không rerun method. Counts/timestamp/minmax toàn 3.630 khớp; mọi trị chuẩn hóa sau sửa nằm trong sqrt(5). Không dùng F2-summary cũ để diễn giải độ lớn. Trường normalized_lastbit_changes chỉ đếm số tỷ số đã đổi; tên trường không có nghĩa mọi thay đổi ở bit cuối: có tỷ số −3,1623→−1,5811 khi mẫu gần hằng. Xem F2-stable-001/schema-notes.json.

Trace/log so hai nửa 150 giây trong N đã lưu ở F2.json.gz mỗi ca; phần thiếu một nửa được ghi UNAVAILABLE_HALF tại evaluate-003/F2-summary.json#/summary/trace_log_half_availability. Không suy kênh vắng thành khỏe.

Bảy cặp kề trong danh sách dev cách 497–551 giây, N bắt đầu 17–71 giây sau kết thúc danh nghĩa 180 giây của ca trước. Đây không phải toàn lịch tiêm và không có nhãn hồi phục quan sát. Kiểm đã xác nhận có sự thay đổi trong N, chưa phân biệt hồi phục, tải, biến thiên bình thường và cadence. H-F2 giữ OPEN về nguyên nhân.

## Đáp phản biện và đính chính

| Điểm | Đánh giá sau tự kiểm | Xử lý và phần còn lại |
|---|---|---|
| F1 | Đúng một phần; chặn kết luận hết đường phân xử | Đã ghi rõ N/A converter đã biết, trình và chạy N-only sau Q-191. Fixture nguồn cũ đã có thông tin nhưng báo cáo chưa làm rõ. Không còn nói mọi normal phải xin tác giả; exact metric-normal/bridge vẫn thiếu. |
| F2 | Ứng viên hợp lý; chưa xác nhận recovery | Đã kiểm đầu–cuối N đúng phạm vi; có biến động, chưa có chuỗi xác nhận hồi phục lỗi trước. Không dùng RE2-TT điểm cao để coi nền chắc sạch. |
| F3 | Đúng một phần, không chặn | Đính chính M0 là literal Duration theo converter; main chia 1000, NezhaRCA chia 1e6. Hệ quả ngưỡng 100 giây chỉ thuộc nhánh sau. M0 vẫn không là toàn bộ pipeline lịch sử. |

So RE2-TT đúng: repo Hit1=0,833333/MRR=0,891111; bài FSE Top1=0,80/MRR=0,85. Chênh tương ứng 3,33/4,11 điểm %, khác tập ca; không dùng0,80 làm MRR công bố. Prior không đổi counts vẫn có thể đổi weights/spectrum/hạng; phản ví dụ cũ dev-8ecd9880ed hạng 9→8 đã lưu. Có thể nhận ưu tiên N đáng làm sớm hơn, không nhận phép prior tất định vô ích.

Bổ sung bảng đối chiếu nguồn: converter có N một phút construct_data, A tới nextinject−60s (ca cuối+10phút); default CLI và MAIN khác đường, normal_metric/bridge còn thiếu; converter giữ Node không chứng minh MAIN dùng Node. Source-contract.json ghi pin và vị trí code. Giữ báo cáo/kết quả cũ làm lịch sử, bản này là đính chính và bổ sung hiện hành của lượt Q-191.

## Câu hỏi nguồn, hệ quả và bước tiếp

RQ1/P3: đã định lượng tác động của gói lựa chọn N trên cùng A, tách lỗi code/giao thức/thiếu đầu vào. RQ2/P4: xác nhận chuỗi thiếu mẫu→mất phiếu hoặc fallback trong điều kiện cụ thể; chưa xác nhận nền nhiễm lỗi hoặc nguyên nhân duy nhất của khoảng lệch công bố. DT18/cô được đáp ứng ở phân tích trường hợp hiệu quả/hạn chế, chưa là đánh giá phương pháp đồ thị hoặc hoàn tất RQ2.

Đối với FlashTicket: cần ghi nguồn và miền normal, đếm mẫu hữu hạn/độ phủ operation, phân biệt unavailable với khỏe, và công khai fallback trước xếp hạng. Muốn ước lượng theo thời gian phải thu đủ nhiều mốc normal đại diện tại nhịp đo thật; một số giá trị gộp khác loại không thay nhiều mốc độc lập. Collector tương lai không thể phục hồi một normal_metric lịch sử chưa được công bố. Quan hệ có thể giúp phân biệt tín hiệu cạnh tranh, nhưng phép này không chứng minh lợi ích đồ thị hoặc chọn cơ chế P6.

Không nói đã hết phép phân xử. Phần A theo converter chưa kiểm vì Q-191 giữ A = 300 giây. Phép tiếp theo cần đúng thời điểm tiêm liên kề để dựng [inject,nextinject−60s], quyền đọc miền bổ sung nếu chạm vùng khóa, và đối chứng A-only trên cùng N. Không tự lấy ca dev kế tiếp làm ca tiêm kế toàn lịch. Exact metric-normal/bridge/config/per-case output vẫn cần nguồn gốc. Các kết luận P6/P7 phụ thuộc; chưa chọn baseline, mở G3/test hoặc nghiệm thu.

## Kiểm, chi phí và trạng thái

prepare: 1282 output cũ khớp manifest, 26 raw normal khớp hash. Fixture explicit N/A đạt 2 kiểm; pilot replay M4/main cũ và Micro explicit split khớp chính xác. Full dùng lại pilot, freeze 66 record trước nhãn. Evaluator P3 và phép tính độc lập khớp; trợ lý nội bộ kiểm độc lập 22 M4/22 MAIN/22 Micro từ output đã freeze. Không thay phản biện Claude.

Giữ 2 lượt tổng hợp hỏng evaluate-001/002 và source/failure; evaluate-003 đạt. Không method rerun. F2 stable chỉ đọc lại metricN đã được duyệt, không chạy method. Nhánh runner Micro NO_EVIDENCE chưa được tổng quát hóa: nó sẽ dừng lô ở trạng thái khôngok ngoài missingbaseline; nhánh này không kích hoạt ở 22 ca hiện tại. Không gọi runner này đã kiểm trên mọi đầu vào khả dĩ.

Lượt method đầy đủ khoảng 261 giây, pilot khoảng 12 giây; F2 stable khoảng 6 giây. Peak RSS đo sau mỗi ca khoảng 456 MiB, không là đỉnh liên tục. Tổng byte/file cuối và wall từng lượt tại manifest/cost. Không tải/cài, không test, không sửa src/data/kết quả cũ, không commit/push/gửi Claude. Trạng thái: chờ phản biện; chưa nghiệm thu/đóng task.
