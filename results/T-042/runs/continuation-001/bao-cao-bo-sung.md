# T-042 — Kết quả nối tiếp theo Q-190

Đã phân xử thêm được bằng chứng cụ thể. Chênh lệch ban đầu không thể gói thành “không tìm thấy bằng chứng”. Mã nguồn, trường đầu vào, cách ghép điểm và một số lỗi cài đặt thực sự làm đổi kết quả trên cùng22dev. Chưa định danh được chương trình sinh các bảng công bố; không chọn baseline mới, không nghiệm thu hay đóng task.

Đầu ra trước Q-190 giữ nguyên tại results/T-042/bao-cao.md và manifest.json. Báo cáo này bổ sung và làm rõ những OPEN trước đó: severity có trong phần lớn raw log; cây lời gọi và Eq7 vẫn có thể kiểm được. Quyền nối tiếp ghi ở DECISIONS Q-190, WHY-54 và LOG. SPEC cũ không sửa.

## Kết quả SimpleRCA

| Nhánh | Đúng hạng1 native /22 | MRR native | Ý nghĩa |
|---|---:|---:|---|
| M0 | 15 | 0.789899 | Hàm main.py; duration literal từ converter; time log native |
| M1 | 5 | 0.363528 | M0 đổi duration vềns theo chú thích code |
| M2 | 5 | 0.363528 | M1 thêm timestamp datetime cho log |
| N0-partial | 9 | 0.489394 | Metric+trace NezhaRCA, literal duration; không log |
| N1-partial | 9 | 0.560606 | Metric+trace NezhaRCA, physicalns; không log |
| M4-no-log | 7 | 0.527453 | M4 bỏ log, đối chứng phạm vi modality |

M4 S0 trước nối tiếp đúng7/22. M0/M1/M2 đều là nguyên hàm source trên hợp đồng P3, chưa phải pipeline tác giả: main.py là nhánh khác CLI NezhaRCA, nguồn normal/window khác; không mặc nhiên nhận nó là SimpleRCA trong bài. Không chọn giữ sai đơn vị chỉ vì dev cao hơn. Bảng đầy đủ22ca/13ô và kỳ vọng tie: simple-evaluate-001/tables.md; số JSON: evaluation.json#/summary, /by_cell, /rows.

Duration×1000 đổi điểm22/22 và hạng gốc18/22. Đổi time log làm đổi điểm20/22 nhưng không đổi hạng gốc. Trong main.py, chỉ cần metric>0 là trace bị bỏ khỏi phép ghép; trace của dịch vụ metric=0 vẫn được dùng ở thang thời lượng tuyệt đối. Đây là chuỗi cài đặt xác nhận trong source và số trung gian, không phải nguyên nhân của mọi ca sai.

Đối chiếu cùng ô checkout exception: dev-b0f8b2e3ac có metric160, log100 và trace256180.5 ở M1, nhưng fusion chỉ190, hạng6. dev-55f99f3e0a có metric0, trace190132.2, log100 nên fusion190202.2, hạng1. Với recommendation cpu_consumed, dev-9b9397a4dc có metric100 nên bỏ trace; dev-515c5f2190 có metric0 nên dùng trace và đúng hạng1. Các pool/ngưỡng/đếm và dịch vụ cao điểm hơn được lưu cho mọi ca tại simple-evaluate-001/mechanism-chains.json#/chains.

## Log và trường thời gian

Probe trên22cửa sổ có1539335 lượt dòng log; 1426748 có severity thật ở JSON lồng, 112587 thiếu. Đây là lượt dòng theo ca, không phải đếm log vật lý duy nhất của toàn dataset. Converter chỉ lấy chuỗi log và không xuất level; mất trường là hạn chế converter, không được kết luận raw hoàn toàn không có severity. Tất cả outer log làstring nên helper extract_message chưa str-cast tương đương trên đúng miền đã kiểm.

| Hợp đồng level | Top1 native /22 | MRR native |
|---|---:|---:|
| L0 | 8 | 0.475000 |
| L1 | 10 | 0.599242 |
| L2 | 9 | 0.617424 |

L0 giữ chữ thực và null; L1 uppercase chữ quan sát, null giữ nguyên; L2 uppercase rồi chỉ dùng dòng có severity. L0/L1: null!=INFO trong kernel bị tính non-INFO; không phải bằng chứng dòng đó là lỗi. L2 thiếu độ phủ, không phải toàn bộ log. Mọi dòng thiếu giữ unknown, không gán INFO. Dùng lại metric/trace N1, chỉ chạy kernel log/vote từ histogram. Ba hash seed cho cùng score/ranks trên66cặpca–hợpđồng; không xác nhận ổn định ngoài miền này.

Ca checkout exception dev-b0f8b2e3ac: L0 rơi sang fallback non-INFO, xếp gốc hạng4; L1 giữ sự tăng error thật, gốc hạng1. Ca đúng tương ứng dev-55f99f3e0a vẫn hạng1. Ngược lại ở recommendation cpu_consumed dev-515c5f2190, bỏ unknown chuyển nhánh log sang INFO-count reduction và có thể làm gốc mất hạng1. Do đó không cộng các cờ hoặc gọi một hợp đồng level là chân lý. Histograms/các count N/A/service và nhánh source lưu ở contracts/histogram-001 và level-seed*/. Bảng toàn ca/ô: extra-evaluate-001/tables.md.

Metric có hai trường thời gian không khớp:90hàng đã chọn ở adservice trong9ca nằm ngoài cửa sổ nếu dùng TimeStamp×1e9 của converter;45hàng đổi N/A. Độ lệch lớn nhất khoảng200triệu giây. Không sửa clock. Projection chỉ xét chính hàng đã allowlist, không tìm hàng khác có TimeStamp rơi vào cửa sổ. Native metric audit trước projection khớp bit score/rank cũ. T-M0 tăng15→16ca hạng1; M1 vẫn5; các L vẫn8/10/9. Mâu thuẫn trường là FACT; chưa xác nhận trường nào phản ánh đồng hồ runtime đúng. Kết quả không phải exact author window. Nguồn: contracts/map-and-time-summary.json, metric-time-exceptions.json và time-projection-001/*-audit.json.

## MicroRank

| Phép giữ các yếu tố còn lại | Top1 /22 trước→sau | MRR trước→sau |
|---|---:|---:|
| cache_sham_dstar2 → cache_sham_ochiai | 0→0 | 0.170139→0.167866 |
| cache_md_dstar2 → cache_md_ochiai | 1→1 | 0.197150→0.198801 |
| cache_mo15c1_dstar2 → cache_mo15c1_ochiai | 6→5 | 0.423904→0.400599 |
| cache_mo1p50c1_dstar2 → cache_mo1p50c1_ochiai | 8→8 | 0.519987→0.512159 |
| repaired_sham → upstream_graph_only | 0→0 | 0.170139→0.166667 |

Dstar2/Ochiai dùng lại88bộ weight/count đã ghim, không chạy lại PageRank. Phép đổi graph giữ đúng nhóm trace, incidence và occurrence; khác cạnh thật do builder cũ reset danh sách cạnh theo dòng. Trên cả22ca đổi graph đơn lẻ không cứu Top1; không dùng đặc tính chung của graph làm nguyên nhân mọi sai.

Kernel RCAEval nguyên hàm hoàn tất nhưng INVALID22/22: mỗi ca có16–35 ô spectrum âm. Ví dụ pilot: graph anomaly chứa991trace, anomaly_count chỉ94; normal/anomaly đếm chồng94trace. nf âm vì đếm toàn graph với số nhóm nhỏ hơn. Giữ nguyên output native, không dùng điểm INVALID làm prediction hợp lệ hoặc báo accuracy0 như kết quả của thuật toán hợp lệ. Nguồn: micro-mechanism-chains.json#/upstream_invalid; source kernel/line và revision ở micro/*/source-checks.json. Đây là RCAEval, chưa phải chương trình nguyên thủy sinh Table3.

Đã đọc trực tiếp ảnh bài và xác nhận Eq7 khác biểu thức prior code. Giữ nguyên ma trận và phép PageRank: kiểm normalization-only, Eq7 cùng coverage-set kind, đổi riêng kind A theo cây identity, đổi cả kind N và đổi scope sang uniqueoperation. Đủ19.080trace–ca sau end split có cây identity đơn gốc/không cycle/không missingparent;58trace có bản lặp, chỉ collapse identity để định kind, giữ occurrence trong graph/scope cho tới phép đổi scope. Có74nhóm–ca cùng operation set nhưng khác cây; không dùng thiếu span.kind làm lý do dừng đại số.

| Prior | Top1 /22 | MRR |
|---|---:|---:|
| P0 | 0 | 0.170139 |
| Pscale | 0 | 0.170770 |
| Peq7 | 0 | 0.170770 |
| PtreeA | 0 | 0.170770 |
| PtreeBoth | 0 | 0.170770 |
| PtreeUnique | 0 | 0.170770 |

Tất cả vẫn0/22 ở phân hoạch sham, MRR chỉ đổi rất nhỏ. Kết luận có điều kiện, không phải phủ định prior/đồ thị trên mọi phân hoạch. Các ma trận cố định, vector/weight/spectrum và scope/duplicates lưu tại micro/prior-full-002/; đủ22ca/13ô trong prior-evaluate-002/summary.json. Source graph/operator/order/weights được tự kiểm; một cặp operation không phải max trong shipping đổi thứ tự2ULP, service order/tie/max operation giữ nguyên. Không che khác biệt hoặc sửa manifest cũ.

Matched-case MicroRank: cùng ô recommendation cpu_consumed, dev-9b9397a4dc ở mo15c1 có gốc không nằm trong anomaly support (ef=nf=1e-7), hạng9; mo1p50c1 đưa gốc vào nhóm có support và lên hạng1. dev-515c5f2190 đúng trong mo15c1, nhưng điều kiện nhóm khác. Đổi prior ở sham vẫn giữ counts/coverage nên không thể thay phần bằng chứng bị detector loại. Toàn bộ root/top intermediate và cặp ca đúng/sai được lưu tại micro-mechanism-chains.json#/chains; không suy duy nhất detector giải thích mọi ca sai.

## Đã phân xử tới đâu và vì sao dừng thực nghiệm ở đây

Đã phân biệt được nguồn hạn chế: bất nhất hai trường thời gian và severity không có ở một phần dòng là vấn đề đầu vào; bỏ severity/thiếu bridge pairedfiles và metric wide là converter/adapter; mismatch graph–count là cài đặt RCAEval; gate ghép điểm/scale thời lượng, detector và công thức prior là cách tính/giả định. Các nhóm chồng lấn nên không cộng thành tỷ lệ nguyên nhân. Chưa xác nhận lợi ích của phương pháp đồ thị mới.

Cặp orig NezhaRCA tốiđa5 với report mặc định ZIP không đồng thời giải thích hàng Table2 Top1=Top5=MRR=.91: report lọc hit trước MRR, nên nếu Top1/Top5 đều làm tròn.91 thì conditionalMRR≥.905/.915≈.989, không thể làm tròn.91. single.py còn đường per-case miss=0; vì thiếu script bảng không kết luận cả artifact hay bài sai. Fixture adapter gốc với sáu pairedfiles không tồn tại trả sáu frame rỗng/ranks[]; đường convert Nezha xuất ba singularfiles, chưa có bridge đã định danh trong caller tương ứng. Nguồn/algebra: source-contract-002/fixtures.json và evaluator-contract.json.

Phần chưa phân xử được tiếp bằng nguồn đang có là định danh lịch sử chương trình/bộ dữ liệu/cách chấm đã sinh0.91 và Table3. Cần exact revision+entrypoint+config/cohort, normal inputs, bridge conversion, per-case prediction và script tổng hợp của tác giả. Normal riêng trong construct_data không thuộc allowlist; không mở nó. Nhiều biến thể có thể cho cùng số tổng; thêm cấu hình trên22dev không cung cấp provenance này. Không nhận là mọi thí nghiệm có thể nghĩ ra đã hết: các tổ hợp khác hoặc phương pháp mới vẫn có thể nghiên cứu, nhưng chưa phải bằng chứng để xác nhận pipeline công bố hay đủ căn cứ chọn thiết kế.

Với các giả định cùng56ca/cùngTop1/dev22 là tập con, ngay cả T-M0 đúng16ca thì cận tốt nhất(16+34)/56=.892857<.905, vẫn loại cohort-only cho chính chương trình đó; không đọc34test và không xác nhận giả định cohort tác giả. Con số này không cho phép tự chọn biến thể theo dev.

Hệ quả FlashTicket: cần ghi severity có schema thống nhất, đơn vị thời gian tường minh và đồng hồ đối chiếu; giữ parent/span identity đủ dựng cây và thông tin nhóm cho mọi bước chấm. Đây là yêu cầu quan sát rút từ thiếu/mất trường đã xác nhận; collector tương lai không khôi phục dữ liệu lịch sử chưa ghi. Dữ liệu đủ để đề xuất kiểm ứng viên có căn cứ, chưa đủ xác nhận lợi ích/khóa thiết kế P6 hay mở G3.

## Kiểm, chi phí và bàn giao

Nguồn/revision/AST và manifest được kiểm trước dùng; chỉ22dev, payload RAM; không tải/cài, không mở test/giữngoài, không sửa src/SPEC, không commit/push hoặc gửi Claude. Có132Simple,198severity (3seed×66),110projection,242Micro công thức/graph/native và132prior diagnosis records; số này bao gồm replay/control, không phải814quan sát độc lập. Lượt hợp lệ được dùng lại; mọi lượt hỏng/dừng và lý do ở cost-and-runs.json. Các row/case/ô trung gian giữ đủ.

Lượt full002 bị dừng để giữ đĩa và tiếp bằng gzip chỉ cho file mới; không xóa/nén thay file cũ. Có giới hạn đo chi phí: RSS probe contracts null; full002 không có cost cuối, giữ clock/progress/checkpoint và nêu thiếu CPU/peak. Đọc timing đang song song không dùng so tốc độ method. Xem cost-and-runs.json và invocation/progress/cost từng lượt.

Trạng thái: người làm hoàn tất phần nối tiếp, chờ Claude phản biện chính thức. Minh quyết tiếp nhận giới hạn, yêu cầu nguồn tác giả hoặc lập nghiên cứu tiếp; chưa nghiệm thu/đóng câu hỏi. Prompt trung tính theo mẫu ở cuối LOG T-042.

Kiểm cuối bổ sung: final-verify-002/checks.json đạt; lượt001 là lỗi dựng bản ghi của checker, giữ source/failure. Có308kiểm ordinal API độc lập; đây không thay kiểm exact-score ties. Đã soạn prompt Claude và chuyển đúng dòng STATE sang chờ phản biện.
