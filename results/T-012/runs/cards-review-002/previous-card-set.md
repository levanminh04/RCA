# Thẻ dataset 2025–2026 — khảo sát nguồn có giới hạn

Ngày truy cập 03/10/2026. Hoàn tất thẻ trong phạm vi **nguồn/metadata**, không phải hoàn tất kiểm chất lượng dữ liệu. Tất cả biến thể dưới đây: telemetry đã tải = 0 byte; số ca thực đọc telemetry = 0. Không đọc dữ liệu khóa hoặc hàng Bank. FACT nguồn chỉ xác nhận điều tài liệu công bố. Không chuyển thành FACT file. Q-47 cho phép chọn bảo toàn và chấp nhận phần chất lượng chưa xác minh; quyết định của gói xem WHY, không lấy thẻ này thay quyết định.

Nguồn và revision: [manifest mới](runs/run-002/source-manifest.json), [manifest cũ](runs/run-001/source-manifest.json), [record summary tính lại](runs/run-002/record-summary.json). [Sổ tìm](search-ledger.md) ghi giới hạn truy vấn; [lineage](independence-matrix.md) xét đủ các trục; [kế hoạch kiểm](inspection-plan.md) giữ nguyên giới hạn metadata.



# FSE fault-propagation benchmark — artifact rút gọn

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Fang và cộng sự, TrainTicket; bài arXiv v2 năm 2025, artifact FSE năm 2026. ChaosMesh; OpenTelemetry, Hubble và Prometheus trong pipeline mô tả bài.

Nguồn: [paper v2](runs/run-001/sources/fse-paper-v2.html); [latest metadata](runs/run-002/sources/zenodo-19513398-latest.json).

Giấy phép dữ liệu/code: Artifact record: Apache-2.0. Giấy phép bài arXiv khác phạm vi, không thay license artifact.

Latest của record cũ 19513398 trả record 19522409; giữ cả hai, không ghi đè. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | FACT nguồn công khai; payload chưa tải. |
| 2 | Bài công bố root phân cấp và mốc tiêm; chưa đối chiếu nhãn artifact rút gọn. |
| 3 | FACT nguồn có trace; liên kết cha–con thật còn OPEN. |
| 4 | FACT nguồn có metric/log; chất lượng file OPEN. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | Bài nêu 31 loại thiết kế, 25 loại tạo tác động qua lọc; không coi 31 là 25 loại trong artifact. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Bài có giai đoạn baseline và kiểm SLI; độ dài/sạch của từng ca phát hành chưa kiểm. |
| 9 | Cùng lineage TT upstream với OpenRCA2, tác giả và chiến dịch có quan hệ trực tiếp. Không tính hai họ này là hai bộ độc lập. |

Nguồn cho bảng: [paper v2](runs/run-001/sources/fse-paper-v2.html); [latest metadata](runs/run-002/sources/zenodo-19513398-latest.json).

## 3. Nhãn, số ca và khả năng phân xử

Bài v2 công bố 1.430 failure cases từ 9.152 injection. Đây không phải census artifact reviewer rút gọn; số ca trong archive vẫn OPEN.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. File nhãn riêng không nằm trong metadata record đã công bố; không mở archive chứa telemetry để tìm. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: Bài mô tả telemetry đa nguồn/nhãn phân cấp; schema từng thành viên archive chưa kiểm.

FACT nguồn có trace; liên kết cha–con thật còn OPEN. FACT nguồn có metric/log; chất lượng file OPEN.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Bài có giai đoạn baseline và kiểm SLI; độ dài/sạch của từng ca phát hành chưa kiểm.

Ngữ nghĩa injection/onset/end và timezone còn OPEN. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | CANDIDATE root theo đúng mức nhãn; artifact rút gọn cần census. |
| Phát hiện thời gian | Chỉ có căn cứ mốc tiêm trong thiết kế; onset/end và cửa sổ artifact OPEN. |
| Vùng ảnh hưởng | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. |
| Bất thường trace | OPEN: chưa thấy nhãn từng trace được kiểm. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

Tên ca/thư mục có thể mang nhãn; chưa có adapter để kiểm loại rò.

Cùng lineage TT upstream với OpenRCA2, tác giả và chiến dịch có quan hệ trực tiếp. Không tính hai họ này là hai bộ độc lập. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

Latest artifact: 91.418.171 byte, so record cũ 96.090.000 byte. Cả hai là reviewer tar.gz rút gọn, không phải byte toàn bộ dữ liệu bài.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | File nhãn riêng không nằm trong metadata record đã công bố; không mở archive chứa telemetry để tìm. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | Cùng lineage TT upstream với OpenRCA2, tác giả và chiến dịch có quan hệ trực tiếp. Không tính hai họ này là hai bộ độc lập. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | Bài arXiv v2 và accepted paper trong artifact có thể khác; chưa mở artifact để đối chiếu nên không tự đồng nhất phiên bản/số ca. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.



# AnoMod — SocialNetwork

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Ping, Mazhar, Wang, Song, Mäntylä (Helsinki), MSR 2026. SocialNetwork; EvoMaster/workload, ChaosBlade và container restart theo README SN; Prometheus và Jaeger.

Nguồn: [paper](runs/run-001/sources/anomod-paper-v1.html); [record](runs/run-002/sources/zenodo-18342898-latest.json); [repo README](runs/run-002/sources/anomod-README.md); [collector README](runs/run-002/sources/anomod-SN_collection-scripts__README.md); [code license](runs/run-002/sources/anomod-LICENSE).

Giấy phép dữ liệu/code: Data CC-BY-4.0 (record); code MIT (repo LICENSE).

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | FACT nguồn công khai; payload chưa tải. |
| 2 | Theo thiết kế, tên experiment chứa lỗi và công cụ nhắm service; root/time từng run phát hành chưa census. |
| 3 | FACT nguồn Jaeger thu distributed trace; parent resolve chưa đo. |
| 4 | Nguồn công bố metric, log, trace, API response và coverage; đủ modality không bảo đảm ghép entity/clock. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | Nguồn chia performance, service, database, code. Không tự coi taxonomy có ở mọi hệ/root. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Nguồn mô tả reset trước mỗi run và baseline; normal thực đủ, recovery và clock OPEN. |
| 9 | Nhóm/thu thập mới có nguồn; SN dùng ChaosBlade/Jaeger/Prometheus chồng với Eadro; TT SkyWalking chồng DeepTraLog. Không gọi độc lập đủ ba trục. Cùng nhóm với LO2 ở một số tác giả. |

Nguồn cho bảng: [paper](runs/run-001/sources/anomod-paper-v1.html); [record](runs/run-002/sources/zenodo-18342898-latest.json); [repo README](runs/run-002/sources/anomod-README.md); [collector README](runs/run-002/sources/anomod-SN_collection-scripts__README.md); [code license](runs/run-002/sources/anomod-LICENSE).

## 3. Nhãn, số ca và khả năng phân xử

Bài Table 3 công bố 2.635 trace và 29 metrics; đây không phải số incident/root/repetition.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. File nhãn riêng không nằm trong metadata record đã công bố; không mở archive chứa telemetry để tìm. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: README SocialNetwork mô tả Jaeger JSON/CSV, metric CSV và log theo experiment. Chưa mở release.

FACT nguồn Jaeger thu distributed trace; parent resolve chưa đo. Nguồn công bố metric, log, trace, API response và coverage; đủ modality không bảo đảm ghép entity/clock.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Nguồn mô tả reset trước mỗi run và baseline; normal thực đủ, recovery và clock OPEN.

Paper mô tả kích hoạt lỗi trước workload, dừng khi workload xong; README nói UTC. Đây chưa là kiểm timestamp file. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | CANDIDATE nếu có nhãn root đúng entity; chưa xác nhận census. |
| Phát hiện thời gian | OPEN: cần interval/onset/end đúng nghĩa, không suy từ tên archive. |
| Vùng ảnh hưởng | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. |
| Bất thường trace | OPEN: chưa thấy nhãn từng trace được kiểm. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

Experiment ID chứa fault/root; README TT hướng dẫn encode lỗi trong EXP_NAME. Cần loại khỏi đầu vào phương pháp; chỉ giữ để census/chấm.

Nhóm/thu thập mới có nguồn; SN dùng ChaosBlade/Jaeger/Prometheus chồng với Eadro; TT SkyWalking chồng DeepTraLog. Không gọi độc lập đủ ba trục. Cùng nhóm với LO2 ở một số tác giả. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

AnoMod.zip 201.917.396 byte gồm hai hệ; chưa tách byte SocialNetwork.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | File nhãn riêng không nằm trong metadata record đã công bố; không mở archive chứa telemetry để tìm. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | Nhóm/thu thập mới có nguồn; SN dùng ChaosBlade/Jaeger/Prometheus chồng với Eadro; TT SkyWalking chồng DeepTraLog. Không gọi độc lập đủ ba trục. Cùng nhóm với LO2 ở một số tác giả. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | Paper nói ChaosMesh/ChaosBlade toàn pipeline; SN README cụ thể ChaosBlade. Dùng mô tả theo hệ, không áp một stack đồng nhất cho cả hai. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.



# AnoMod — TrainTicket

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Ping, Mazhar, Wang, Song, Mäntylä (Helsinki), MSR 2026. TrainTicket; EvoMaster/workload, ChaosMesh/ChaosBlade theo README TT; Prometheus và SkyWalking.

Nguồn: [paper](runs/run-001/sources/anomod-paper-v1.html); [record](runs/run-002/sources/zenodo-18342898-latest.json); [repo README](runs/run-002/sources/anomod-README.md); [collector README](runs/run-002/sources/anomod-TT_collection-scripts__T-Dataset__README.md); [code license](runs/run-002/sources/anomod-LICENSE).

Giấy phép dữ liệu/code: Data CC-BY-4.0 (record); code MIT (repo LICENSE).

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | FACT nguồn công khai; payload chưa tải. |
| 2 | Theo thiết kế, tên experiment chứa lỗi và công cụ nhắm service; root/time từng run phát hành chưa census. |
| 3 | FACT nguồn SkyWalking thu distributed trace; parent resolve chưa đo. |
| 4 | Nguồn công bố metric, log, trace, API response và coverage; đủ modality không bảo đảm ghép entity/clock. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | Nguồn chia performance, service, database, code. Không tự coi taxonomy có ở mọi hệ/root. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Nguồn mô tả reset trước mỗi run và baseline; normal thực đủ, recovery và clock OPEN. |
| 9 | Nhóm/thu thập mới có nguồn; SN dùng ChaosBlade/Jaeger/Prometheus chồng với Eadro; TT SkyWalking chồng DeepTraLog. Không gọi độc lập đủ ba trục. Cùng nhóm với LO2 ở một số tác giả. |

Nguồn cho bảng: [paper](runs/run-001/sources/anomod-paper-v1.html); [record](runs/run-002/sources/zenodo-18342898-latest.json); [repo README](runs/run-002/sources/anomod-README.md); [collector README](runs/run-002/sources/anomod-TT_collection-scripts__T-Dataset__README.md); [code license](runs/run-002/sources/anomod-LICENSE).

## 3. Nhãn, số ca và khả năng phân xử

Bài Table 3 công bố 63.975 trace và 33 metrics; đây không phải số incident/root/repetition.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. File nhãn riêng không nằm trong metadata record đã công bố; không mở archive chứa telemetry để tìm. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: README TrainTicket mô tả SkyWalking JSONL/span, metric CSV và log theo experiment. Chưa mở release.

FACT nguồn SkyWalking thu distributed trace; parent resolve chưa đo. Nguồn công bố metric, log, trace, API response và coverage; đủ modality không bảo đảm ghép entity/clock.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Nguồn mô tả reset trước mỗi run và baseline; normal thực đủ, recovery và clock OPEN.

Paper mô tả kích hoạt lỗi trước workload, dừng khi workload xong; README nói UTC. Đây chưa là kiểm timestamp file. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | CANDIDATE nếu có nhãn root đúng entity; chưa xác nhận census. |
| Phát hiện thời gian | OPEN: cần interval/onset/end đúng nghĩa, không suy từ tên archive. |
| Vùng ảnh hưởng | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. |
| Bất thường trace | OPEN: chưa thấy nhãn từng trace được kiểm. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

Experiment ID chứa fault/root; README TT hướng dẫn encode lỗi trong EXP_NAME. Cần loại khỏi đầu vào phương pháp; chỉ giữ để census/chấm.

Nhóm/thu thập mới có nguồn; SN dùng ChaosBlade/Jaeger/Prometheus chồng với Eadro; TT SkyWalking chồng DeepTraLog. Không gọi độc lập đủ ba trục. Cùng nhóm với LO2 ở một số tác giả. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

AnoMod.zip 201.917.396 byte gồm hai hệ; chưa tách byte TrainTicket.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | File nhãn riêng không nằm trong metadata record đã công bố; không mở archive chứa telemetry để tìm. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | Nhóm/thu thập mới có nguồn; SN dùng ChaosBlade/Jaeger/Prometheus chồng với Eadro; TT SkyWalking chồng DeepTraLog. Không gọi độc lập đủ ba trục. Cùng nhóm với LO2 ở một số tác giả. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | Paper nói ChaosMesh/ChaosBlade toàn pipeline; SN README cụ thể ChaosBlade. Dùng mô tả theo hệ, không áp một stack đồng nhất cho cả hai. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.



# TrainTicketTrace

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Urbanke và Fischer, SCCH; dataset Zenodo công bố 2025, trình bày SANER 2026. TrainTicket clean/faulty versions, collector/injector cụ thể chưa khóa.

Nguồn: [record](runs/run-002/sources/zenodo-17811972-latest.json); [conference abstract](runs/run-002/sources/traintickettrace-conference.html).

Giấy phép dữ liệu/code: Data CC-BY-4.0 theo record; code license chưa thấy trong metadata đã đọc.

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | FACT nguồn công khai; payload chưa tải. |
| 2 | Tên archive F1/F2/... là nhãn version, chưa chứng minh root/time theo incident. |
| 3 | Abstract công bố trace/metric/log; schema parent và nhãn trace còn OPEN. |
| 4 | FACT nguồn có metric/log; chất lượng file OPEN. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | Seeded faults theo abstract; mapping F-code sang root/fault/line chưa kiểm. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Clean reference version có nguồn; tính tương ứng workload và nhãn normal mỗi trace chưa kiểm. |
| 9 | Nhóm SCCH khác các họ còn lại, cùng TT. Chưa xác định injector/collector hoặc quan hệ với faulty branches DeepTraLog; không suy reuse chỉ từ F-code giống. |

Nguồn cho bảng: [record](runs/run-002/sources/zenodo-17811972-latest.json); [conference abstract](runs/run-002/sources/traintickettrace-conference.html).

## 3. Nhãn, số ca và khả năng phân xử

Record có 11 tar: 10 tên lỗi và 1 cleaned. Abstract hội nghị nói clean + 9 faulty versions. Chưa đồng nhất được hai cách đếm; không dùng tar làm incident.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. File nhãn riêng không nằm trong metadata record đã công bố; không mở archive chứa telemetry để tìm. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: Không có schema file thật trong phạm vi đã đọc.

Abstract công bố trace/metric/log; schema parent và nhãn trace còn OPEN. FACT nguồn có metric/log; chất lượng file OPEN.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Clean reference version có nguồn; tính tương ứng workload và nhãn normal mỗi trace chưa kiểm.

Ngữ nghĩa injection/onset/end và timezone còn OPEN. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | CANDIDATE nếu có nhãn root đúng entity; chưa xác nhận census. |
| Phát hiện thời gian | OPEN: cần interval/onset/end đúng nghĩa, không suy từ tên archive. |
| Vùng ảnh hưởng | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. |
| Bất thường trace | OPEN: chưa thấy nhãn từng trace được kiểm. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

Tên ca/thư mục có thể mang nhãn; chưa có adapter để kiểm loại rò.

Nhóm SCCH khác các họ còn lại, cùng TT. Chưa xác định injector/collector hoặc quan hệ với faulty branches DeepTraLog; không suy reuse chỉ từ F-code giống. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

Tổng 26.920.437.760 byte / 11 tar; từng tar ở record-summary. Không tải.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | File nhãn riêng không nằm trong metadata record đã công bố; không mở archive chứa telemetry để tìm. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | Nhóm SCCH khác các họ còn lại, cùng TT. Chưa xác định injector/collector hoặc quan hệ với faulty branches DeepTraLog; không suy reuse chỉ từ F-code giống. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | Chênh 9 faulty versions ở abstract so 10 tar có F-code; có thể version, scope hoặc archive split. Giữ cả hai; tác giả hoặc nhãn/source cần giải thích. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.



# Check Your Trace First (TRCA) — TrainTicket

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Record anonymous, năm 2026, công bố code TRCA và dữ liệu đa nguồn TrainTicket. Tác giả/injector/collector chưa có trong record.

Nguồn: [record](runs/run-002/sources/zenodo-19335897-latest.json).

Giấy phép dữ liệu/code: CC-BY-4.0 cho record gói TRCA.zip; license riêng code bên trong chưa kiểm.

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | FACT nguồn công khai; payload chưa tải. |
| 2 | Chưa có schema nhãn riêng trong record; root/time còn OPEN. |
| 3 | FACT nguồn có trace; liên kết cha–con thật còn OPEN. |
| 4 | FACT nguồn có metric/log; chất lượng file OPEN. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | OPEN: nhóm lỗi theo release cần nhãn/cấu hình. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Record không mô tả normal theo ca; OPEN. |
| 9 | Anonymous, TT/OB trùng testbed Nezha/RCAEval. Provenance/reuse raw OPEN; không tính thành bộ độc lập mới. |

Nguồn cho bảng: [record](runs/run-002/sources/zenodo-19335897-latest.json).

## 3. Nhãn, số ca và khả năng phân xử

Một TRCA.zip chứa code và hai hệ; không có số incident riêng TrainTicket.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. File nhãn riêng không nằm trong metadata record đã công bố; không mở archive chứa telemetry để tìm. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: Không có schema file thật trong phạm vi đã đọc.

FACT nguồn có trace; liên kết cha–con thật còn OPEN. FACT nguồn có metric/log; chất lượng file OPEN.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Record không mô tả normal theo ca; OPEN.

Ngữ nghĩa injection/onset/end và timezone còn OPEN. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | CANDIDATE nếu có nhãn root đúng entity; chưa xác nhận census. |
| Phát hiện thời gian | OPEN: cần interval/onset/end đúng nghĩa, không suy từ tên archive. |
| Vùng ảnh hưởng | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. |
| Bất thường trace | OPEN: chưa thấy nhãn từng trace được kiểm. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

Tên ca/thư mục có thể mang nhãn; chưa có adapter để kiểm loại rò.

Anonymous, TT/OB trùng testbed Nezha/RCAEval. Provenance/reuse raw OPEN; không tính thành bộ độc lập mới. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

TRCA.zip 335.076.044 byte cho cả hai hệ và code; chưa tách byte TrainTicket.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | File nhãn riêng không nằm trong metadata record đã công bố; không mở archive chứa telemetry để tìm. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | Anonymous, TT/OB trùng testbed Nezha/RCAEval. Provenance/reuse raw OPEN; không tính thành bộ độc lập mới. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | Root/time/license code/provenance cần README bên trong; không dùng tiêu đề paper thay nhãn đã kiểm. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.



# Check Your Trace First (TRCA) — OnlineBoutique

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Record anonymous, năm 2026, công bố code TRCA và dữ liệu đa nguồn OnlineBoutique. Tác giả/injector/collector chưa có trong record.

Nguồn: [record](runs/run-002/sources/zenodo-19335897-latest.json).

Giấy phép dữ liệu/code: CC-BY-4.0 cho record gói TRCA.zip; license riêng code bên trong chưa kiểm.

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | FACT nguồn công khai; payload chưa tải. |
| 2 | Chưa có schema nhãn riêng trong record; root/time còn OPEN. |
| 3 | FACT nguồn có trace; liên kết cha–con thật còn OPEN. |
| 4 | FACT nguồn có metric/log; chất lượng file OPEN. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | OPEN: nhóm lỗi theo release cần nhãn/cấu hình. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Record không mô tả normal theo ca; OPEN. |
| 9 | Anonymous, TT/OB trùng testbed Nezha/RCAEval. Provenance/reuse raw OPEN; không tính thành bộ độc lập mới. |

Nguồn cho bảng: [record](runs/run-002/sources/zenodo-19335897-latest.json).

## 3. Nhãn, số ca và khả năng phân xử

Một TRCA.zip chứa code và hai hệ; không có số incident riêng OnlineBoutique.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. File nhãn riêng không nằm trong metadata record đã công bố; không mở archive chứa telemetry để tìm. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: Không có schema file thật trong phạm vi đã đọc.

FACT nguồn có trace; liên kết cha–con thật còn OPEN. FACT nguồn có metric/log; chất lượng file OPEN.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Record không mô tả normal theo ca; OPEN.

Ngữ nghĩa injection/onset/end và timezone còn OPEN. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | CANDIDATE nếu có nhãn root đúng entity; chưa xác nhận census. |
| Phát hiện thời gian | OPEN: cần interval/onset/end đúng nghĩa, không suy từ tên archive. |
| Vùng ảnh hưởng | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. |
| Bất thường trace | OPEN: chưa thấy nhãn từng trace được kiểm. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

Tên ca/thư mục có thể mang nhãn; chưa có adapter để kiểm loại rò.

Anonymous, TT/OB trùng testbed Nezha/RCAEval. Provenance/reuse raw OPEN; không tính thành bộ độc lập mới. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

TRCA.zip 335.076.044 byte cho cả hai hệ và code; chưa tách byte OnlineBoutique.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | File nhãn riêng không nằm trong metadata record đã công bố; không mở archive chứa telemetry để tìm. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | Anonymous, TT/OB trùng testbed Nezha/RCAEval. Provenance/reuse raw OPEN; không tính thành bộ độc lập mới. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | Root/time/license code/provenance cần README bên trong; không dùng tiêu đề paper thay nhãn đã kiểm. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.



# OpenRCA — Telecom

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Xu và cộng sự, ICLR 2025; dữ liệu phát sinh từ AIOps Challenge, qua downsample/đổi tên/hiệu chỉnh/lọc. root có thể OS/pod/database; trace+metric, không có log theo paper A.2.

Nguồn: [official paper](runs/run-002/sources/openrca-paper.pdf); [README pinned](runs/run-002/sources/openrca-README.md); [repo license](runs/run-002/sources/openrca-LICENSE); [task schema](runs/run-002/sources/openrca-main__task_specification.json).

Giấy phép dữ liệu/code: Telemetry CC BY-NC 4.0 theo paper A.1; repo code MIT. Không lấy MIT áp vào telemetry.

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | FACT nguồn công khai; payload chưa tải. |
| 2 | README có root occurrence datetime/component/reason, record.csv và query.csv. Bản phát hành/nhãn thật chưa đọc. |
| 3 | Paper A.3 mô tả timestamp,cmdb_id,parent_id,span_id,trace_id,duration. Parent completeness chưa đo. |
| 4 | Trace+metric, không log theo A.2; schema sample của bài không thay kiểm file. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | CPU/network/database theo A.2. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Nguồn có telemetry theo ngày; chưa chứng minh normal sạch/đủ. Bộ được lọc theo khả năng nhìn thấy root nên có selection bias. |
| 9 | FACT dùng lại AIOps raw, không độc lập với chính nguồn AIOps tương ứng. Nhóm/testbed khác TT/SN/OB là bằng chứng một phần; injector/collector gốc OPEN, chưa đạt đầy đủ tiêu chí9. |

Nguồn cho bảng: [official paper](runs/run-002/sources/openrca-paper.pdf); [README pinned](runs/run-002/sources/openrca-README.md); [repo license](runs/run-002/sources/openrca-LICENSE); [task schema](runs/run-002/sources/openrca-main__task_specification.json).

## 3. Nhãn, số ca và khả năng phân xử

Paper Table 1: 51 failure cases, 15 unique root components, 5 reasons. Đây là số công bố, không census query.csv hoặc record.csv.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. Repo chỉ có dataset/README dẫn Drive; không có nhãn thật riêng trong tree ghim. Không mở Drive telemetry/Bank; census chưa làm. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: CSV theo paper; root/time/reason là nhãn chấm. Giữ nguyên unit pod/node/service đến khi có mapping hợp lệ.

Paper A.3 mô tả timestamp,cmdb_id,parent_id,span_id,trace_id,duration. Parent completeness chưa đo. Trace+metric, không log theo A.2; schema sample của bài không thay kiểm file.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Nguồn có telemetry theo ngày; chưa chứng minh normal sạch/đủ. Bộ được lọc theo khả năng nhìn thấy root nên có selection bias.

README/paper khai báo UTC+8. Occurrence time chưa được độc lập xác nhận là injection hoặc onset quan sát; không suy thời điểm kết thúc. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | CANDIDATE chấm đúng entity OS/pod/database khi census/mapping đủ; không chấm service nếu nhãn chỉ pod. |
| Phát hiện thời gian | Có occurrence time; thiếu định nghĩa onset/end độc lập. Query cho khoảng và số lỗi không tương đương detector tự phát hiện. |
| Vùng ảnh hưởng | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. |
| Bất thường trace | OPEN: chưa thấy nhãn từng trace được kiểm. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

record.csv/query.csv chứa nhãn, query synthesis biết khoảng/số lỗi. main/task_specification.json ghi các đầu vào đó. Không đưa nhãn hoặc số lỗi thật vào detector tự phát hiện.

FACT dùng lại AIOps raw, không độc lập với chính nguồn AIOps tương ứng. Nhóm/testbed khác TT/SN/OB là bằng chứng một phần; injector/collector gốc OPEN, chưa đạt đầy đủ tiêu chí9. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

Paper Table1 ghi 17,6 GB telemetry, không phải byte archive nén hay số byte đã tải. Google Drive có liên kết từ README nhưng chưa kiểm inventory file.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | Repo chỉ có dataset/README dẫn Drive; không có nhãn thật riêng trong tree ghim. Không mở Drive telemetry/Bank; census chưa làm. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | FACT dùng lại AIOps raw, không độc lập với chính nguồn AIOps tương ứng. Nhóm/testbed khác TT/SN/OB là bằng chứng một phần; injector/collector gốc OPEN, chưa đạt đầy đủ tiêu chí9. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | Bản AIOps cụ thể, injector/collector, inventory/revision data và thời gian lỗi chưa khóa. Bảo toàn họ Bank theo quyết định root; các hệ khác không tự suy độc lập với Bank. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.



# OpenRCA — Bank

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Xu và cộng sự, ICLR 2025; dữ liệu phát sinh từ AIOps Challenge, qua downsample/đổi tên/hiệu chỉnh/lọc. root mức pod; README chỉ trace ngang pod, không có vertical deployment structure.

Nguồn: [official paper](runs/run-002/sources/openrca-paper.pdf); [README pinned](runs/run-002/sources/openrca-README.md); [repo license](runs/run-002/sources/openrca-LICENSE); [task schema](runs/run-002/sources/openrca-main__task_specification.json).

Giấy phép dữ liệu/code: Telemetry CC BY-NC 4.0 theo paper A.1; repo code MIT. Không lấy MIT áp vào telemetry.

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | FACT nguồn công khai; payload chưa tải. |
| 2 | README có root occurrence datetime/component/reason, record.csv và query.csv. Bản phát hành/nhãn thật chưa đọc. |
| 3 | Paper A.3 mô tả timestamp,cmdb_id,parent_id,span_id,trace_id,duration. Parent completeness chưa đo. |
| 4 | Metric+trace+log theo A.2; schema sample của bài không thay kiểm file. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | CPU/memory/disk/network/JVM theo A.2. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Nguồn có telemetry theo ngày; chưa chứng minh normal sạch/đủ. Bộ được lọc theo khả năng nhìn thấy root nên có selection bias. |
| 9 | FACT dùng lại AIOps raw, không độc lập với chính nguồn AIOps tương ứng. Nhóm/testbed khác TT/SN/OB là bằng chứng một phần; injector/collector gốc OPEN, chưa đạt đầy đủ tiêu chí9. |

Nguồn cho bảng: [official paper](runs/run-002/sources/openrca-paper.pdf); [README pinned](runs/run-002/sources/openrca-README.md); [repo license](runs/run-002/sources/openrca-LICENSE); [task schema](runs/run-002/sources/openrca-main__task_specification.json).

## 3. Nhãn, số ca và khả năng phân xử

Paper Table 1: 136 failure cases, 14 unique root components, 8 reasons. Đây là số công bố, không census query.csv hoặc record.csv.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. Repo chỉ có dataset/README dẫn Drive; không có nhãn thật riêng trong tree ghim. Không mở Drive telemetry/Bank; census chưa làm. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: CSV theo paper; root/time/reason là nhãn chấm. Giữ nguyên unit pod/node/service đến khi có mapping hợp lệ.

Paper A.3 mô tả timestamp,cmdb_id,parent_id,span_id,trace_id,duration. Parent completeness chưa đo. Metric+trace+log theo A.2; schema sample của bài không thay kiểm file.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Nguồn có telemetry theo ngày; chưa chứng minh normal sạch/đủ. Bộ được lọc theo khả năng nhìn thấy root nên có selection bias.

README/paper khai báo UTC+8. Occurrence time chưa được độc lập xác nhận là injection hoặc onset quan sát; không suy thời điểm kết thúc. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | CANDIDATE chấm đúng entity pod khi census/mapping đủ; không chấm service nếu nhãn chỉ pod. |
| Phát hiện thời gian | Có occurrence time; thiếu định nghĩa onset/end độc lập. Query cho khoảng và số lỗi không tương đương detector tự phát hiện. |
| Vùng ảnh hưởng | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. |
| Bất thường trace | OPEN: chưa thấy nhãn từng trace được kiểm. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

record.csv/query.csv chứa nhãn, query synthesis biết khoảng/số lỗi. main/task_specification.json ghi các đầu vào đó. Không đưa nhãn hoặc số lỗi thật vào detector tự phát hiện.

FACT dùng lại AIOps raw, không độc lập với chính nguồn AIOps tương ứng. Nhóm/testbed khác TT/SN/OB là bằng chứng một phần; injector/collector gốc OPEN, chưa đạt đầy đủ tiêu chí9. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

Paper Table1 ghi 26,4 GB telemetry, không phải byte archive nén hay số byte đã tải. Google Drive có liên kết từ README nhưng chưa kiểm inventory file.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | Repo chỉ có dataset/README dẫn Drive; không có nhãn thật riêng trong tree ghim. Không mở Drive telemetry/Bank; census chưa làm. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | FACT dùng lại AIOps raw, không độc lập với chính nguồn AIOps tương ứng. Nhóm/testbed khác TT/SN/OB là bằng chứng một phần; injector/collector gốc OPEN, chưa đạt đầy đủ tiêu chí9. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | Bản AIOps cụ thể, injector/collector, inventory/revision data và thời gian lỗi chưa khóa. Bảo toàn họ Bank theo quyết định root; các hệ khác không tự suy độc lập với Bank. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.



# OpenRCA — Market

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Xu và cộng sự, ICLR 2025; dữ liệu phát sinh từ AIOps Challenge, qua downsample/đổi tên/hiệu chỉnh/lọc. root node/pod/service; hai cloudbed có telemetry thu riêng.

Nguồn: [official paper](runs/run-002/sources/openrca-paper.pdf); [README pinned](runs/run-002/sources/openrca-README.md); [repo license](runs/run-002/sources/openrca-LICENSE); [task schema](runs/run-002/sources/openrca-main__task_specification.json).

Giấy phép dữ liệu/code: Telemetry CC BY-NC 4.0 theo paper A.1; repo code MIT. Không lấy MIT áp vào telemetry.

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | FACT nguồn công khai; payload chưa tải. |
| 2 | README có root occurrence datetime/component/reason, record.csv và query.csv. Bản phát hành/nhãn thật chưa đọc. |
| 3 | Paper A.3 mô tả timestamp,cmdb_id,parent_id,span_id,trace_id,duration. Parent completeness chưa đo. |
| 4 | Metric+trace+log theo A.2; schema sample của bài không thay kiểm file. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | CPU/memory/disk/network/process theo A.2. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Nguồn có telemetry theo ngày; chưa chứng minh normal sạch/đủ. Bộ được lọc theo khả năng nhìn thấy root nên có selection bias. |
| 9 | FACT dùng lại AIOps raw, không độc lập với chính nguồn AIOps tương ứng. Nhóm/testbed khác TT/SN/OB là bằng chứng một phần; injector/collector gốc OPEN, chưa đạt đầy đủ tiêu chí9. |

Nguồn cho bảng: [official paper](runs/run-002/sources/openrca-paper.pdf); [README pinned](runs/run-002/sources/openrca-README.md); [repo license](runs/run-002/sources/openrca-LICENSE); [task schema](runs/run-002/sources/openrca-main__task_specification.json).

## 3. Nhãn, số ca và khả năng phân xử

Paper Table 1: 148 failure cases, 44 unique root components, 15 reasons. Đây là số công bố, không census query.csv hoặc record.csv.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. Repo chỉ có dataset/README dẫn Drive; không có nhãn thật riêng trong tree ghim. Không mở Drive telemetry/Bank; census chưa làm. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: CSV theo paper; root/time/reason là nhãn chấm. Giữ nguyên unit pod/node/service đến khi có mapping hợp lệ.

Paper A.3 mô tả timestamp,cmdb_id,parent_id,span_id,trace_id,duration. Parent completeness chưa đo. Metric+trace+log theo A.2; schema sample của bài không thay kiểm file.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Nguồn có telemetry theo ngày; chưa chứng minh normal sạch/đủ. Bộ được lọc theo khả năng nhìn thấy root nên có selection bias.

README/paper khai báo UTC+8. Occurrence time chưa được độc lập xác nhận là injection hoặc onset quan sát; không suy thời điểm kết thúc. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | CANDIDATE chấm đúng entity node/pod/service khi census/mapping đủ; không chấm service nếu nhãn chỉ pod. |
| Phát hiện thời gian | Có occurrence time; thiếu định nghĩa onset/end độc lập. Query cho khoảng và số lỗi không tương đương detector tự phát hiện. |
| Vùng ảnh hưởng | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. |
| Bất thường trace | OPEN: chưa thấy nhãn từng trace được kiểm. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

record.csv/query.csv chứa nhãn, query synthesis biết khoảng/số lỗi. main/task_specification.json ghi các đầu vào đó. Không đưa nhãn hoặc số lỗi thật vào detector tự phát hiện.

FACT dùng lại AIOps raw, không độc lập với chính nguồn AIOps tương ứng. Nhóm/testbed khác TT/SN/OB là bằng chứng một phần; injector/collector gốc OPEN, chưa đạt đầy đủ tiêu chí9. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

Paper Table1 ghi 24,5 GB telemetry, không phải byte archive nén hay số byte đã tải. Google Drive có liên kết từ README nhưng chưa kiểm inventory file.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | Repo chỉ có dataset/README dẫn Drive; không có nhãn thật riêng trong tree ghim. Không mở Drive telemetry/Bank; census chưa làm. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | FACT dùng lại AIOps raw, không độc lập với chính nguồn AIOps tương ứng. Nhóm/testbed khác TT/SN/OB là bằng chứng một phần; injector/collector gốc OPEN, chưa đạt đầy đủ tiêu chí9. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | Bản AIOps cụ thể, injector/collector, inventory/revision data và thời gian lỗi chưa khóa. Bảo toàn họ Bank theo quyết định root; các hệ khác không tự suy độc lập với Bank. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.



# OpenRCA 2.0 — TrainTicket

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Fang và cộng sự, arXiv v2 năm 2026; TrainTicket; ChaosMesh, OpenTelemetry/Parquet/Prometheus. TT xây trên dữ liệu Fang/FSE; hai hệ còn lại chiến dịch mới theo paper.

Nguồn: [paper v2](runs/run-001/sources/openrca2-paper-v2.html).

Giấy phép dữ liệu/code: Paper A.6 nêu data CC-BY-SA4.0, pipeline Apache2.0. Giấy phép arXiv CC BY-NC-SA của bài là phạm vi khác. Public release chưa khóa.

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | OPEN: A.6 nói preview/full anonymous trong submission, public sau acceptance; không có public archive ghim trong nguồn đã đọc. |
| 2 | Paper có service/pod/container/function/span/metric và injection window; chưa có census release. |
| 3 | FACT nguồn có trace; liên kết cha–con thật còn OPEN. |
| 4 | FACT nguồn có metric/log; chất lượng file OPEN. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | Application/resource/network/pod interventions theo paper; loại cụ thể theo hệ chưa census. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Theo protocol: fresh deploy/warmup/pre-injection baseline, lọc baseline bất thường; chưa kiểm file. |
| 9 | TT dùng lại Fang/FSE. Cả ba hệ chung nhóm/injector/collector. OpenRCA1 khác raw AIOps; vẫn trùng một số tác giả, không đủ ba trục độc lập. |

Nguồn cho bảng: [paper v2](runs/run-001/sources/openrca2-paper-v2.html).

## 3. Nhãn, số ca và khả năng phân xử

Paper nói 500 evaluable instances tổng ba hệ, 27 primary kinds; không gán tổng này cho riêng TrainTicket.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. Nguồn đã đọc chưa có public release nhãn riêng; chỉ paper/submission artifact mô tả. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: Theo A.2/A.4: Parquet trace/metric/log, nhãn root và graph PAVE. Schema thật chưa có payload kiểm.

FACT nguồn có trace; liên kết cha–con thật còn OPEN. FACT nguồn có metric/log; chất lượng file OPEN.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Theo protocol: fresh deploy/warmup/pre-injection baseline, lọc baseline bất thường; chưa kiểm file.

Paper có injection window [t0,t0+duration]; không suy onset thật. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | CANDIDATE root set theo cấp nhãn công bố; cần release/census. |
| Phát hiện thời gian | CANDIDATE injection-regime nếu khoảng tiêm đủ; onset quan sát OPEN. |
| Vùng ảnh hưởng | Có graph propagation do PAVE tạo từ telemetry/quy tắc; không tự xem là nhãn vùng độc lập để chấm RQ3c. |
| Bất thường trace | OPEN: chưa thấy nhãn từng trace được kiểm. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

PAVE dùng root/injection tạo label; cần tách label/graph khỏi input phương pháp. Chọn ca qua SLI/path và loại graph trivial/cycle tạo selection bias.

TT dùng lại Fang/FSE. Cả ba hệ chung nhóm/injector/collector. OpenRCA1 khác raw AIOps; vẫn trùng một số tác giả, không đủ ba trục độc lập. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

OPEN: chưa có inventory public archive ghim; số instance không chuyển thành byte.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | Nguồn đã đọc chưa có public release nhãn riêng; chỉ paper/submission artifact mô tả. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | TT dùng lại Fang/FSE. Cả ba hệ chung nhóm/injector/collector. OpenRCA1 khác raw AIOps; vẫn trùng một số tác giả, không đủ ba trục độc lập. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | Tình trạng public artifact hiện hành chưa xác minh thêm ngoài lượt tìm giới hạn; không khẳng định không tồn tại. Nhãn PAVE không mặc nhiên đáp ứng nhãn vùng độc lập MRP. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.



# OpenRCA 2.0 — OpenTelemetry Demo

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Fang và cộng sự, arXiv v2 năm 2026; OpenTelemetry Demo; ChaosMesh, OpenTelemetry/Parquet/Prometheus. TT xây trên dữ liệu Fang/FSE; hai hệ còn lại chiến dịch mới theo paper.

Nguồn: [paper v2](runs/run-001/sources/openrca2-paper-v2.html).

Giấy phép dữ liệu/code: Paper A.6 nêu data CC-BY-SA4.0, pipeline Apache2.0. Giấy phép arXiv CC BY-NC-SA của bài là phạm vi khác. Public release chưa khóa.

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | OPEN: A.6 nói preview/full anonymous trong submission, public sau acceptance; không có public archive ghim trong nguồn đã đọc. |
| 2 | Paper có service/pod/container/function/span/metric và injection window; chưa có census release. |
| 3 | FACT nguồn có trace; liên kết cha–con thật còn OPEN. |
| 4 | FACT nguồn có metric/log; chất lượng file OPEN. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | Application/resource/network/pod interventions theo paper; loại cụ thể theo hệ chưa census. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Theo protocol: fresh deploy/warmup/pre-injection baseline, lọc baseline bất thường; chưa kiểm file. |
| 9 | TT dùng lại Fang/FSE. Cả ba hệ chung nhóm/injector/collector. OpenRCA1 khác raw AIOps; vẫn trùng một số tác giả, không đủ ba trục độc lập. |

Nguồn cho bảng: [paper v2](runs/run-001/sources/openrca2-paper-v2.html).

## 3. Nhãn, số ca và khả năng phân xử

Paper nói 500 evaluable instances tổng ba hệ, 27 primary kinds; không gán tổng này cho riêng OpenTelemetry Demo.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. Nguồn đã đọc chưa có public release nhãn riêng; chỉ paper/submission artifact mô tả. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: Theo A.2/A.4: Parquet trace/metric/log, nhãn root và graph PAVE. Schema thật chưa có payload kiểm.

FACT nguồn có trace; liên kết cha–con thật còn OPEN. FACT nguồn có metric/log; chất lượng file OPEN.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Theo protocol: fresh deploy/warmup/pre-injection baseline, lọc baseline bất thường; chưa kiểm file.

Paper có injection window [t0,t0+duration]; không suy onset thật. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | CANDIDATE root set theo cấp nhãn công bố; cần release/census. |
| Phát hiện thời gian | CANDIDATE injection-regime nếu khoảng tiêm đủ; onset quan sát OPEN. |
| Vùng ảnh hưởng | Có graph propagation do PAVE tạo từ telemetry/quy tắc; không tự xem là nhãn vùng độc lập để chấm RQ3c. |
| Bất thường trace | OPEN: chưa thấy nhãn từng trace được kiểm. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

PAVE dùng root/injection tạo label; cần tách label/graph khỏi input phương pháp. Chọn ca qua SLI/path và loại graph trivial/cycle tạo selection bias.

TT dùng lại Fang/FSE. Cả ba hệ chung nhóm/injector/collector. OpenRCA1 khác raw AIOps; vẫn trùng một số tác giả, không đủ ba trục độc lập. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

OPEN: chưa có inventory public archive ghim; số instance không chuyển thành byte.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | Nguồn đã đọc chưa có public release nhãn riêng; chỉ paper/submission artifact mô tả. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | TT dùng lại Fang/FSE. Cả ba hệ chung nhóm/injector/collector. OpenRCA1 khác raw AIOps; vẫn trùng một số tác giả, không đủ ba trục độc lập. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | Tình trạng public artifact hiện hành chưa xác minh thêm ngoài lượt tìm giới hạn; không khẳng định không tồn tại. Nhãn PAVE không mặc nhiên đáp ứng nhãn vùng độc lập MRP. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.



# OpenRCA 2.0 — Hotel Reservation

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Fang và cộng sự, arXiv v2 năm 2026; Hotel Reservation; ChaosMesh, OpenTelemetry/Parquet/Prometheus. TT xây trên dữ liệu Fang/FSE; hai hệ còn lại chiến dịch mới theo paper.

Nguồn: [paper v2](runs/run-001/sources/openrca2-paper-v2.html).

Giấy phép dữ liệu/code: Paper A.6 nêu data CC-BY-SA4.0, pipeline Apache2.0. Giấy phép arXiv CC BY-NC-SA của bài là phạm vi khác. Public release chưa khóa.

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | OPEN: A.6 nói preview/full anonymous trong submission, public sau acceptance; không có public archive ghim trong nguồn đã đọc. |
| 2 | Paper có service/pod/container/function/span/metric và injection window; chưa có census release. |
| 3 | FACT nguồn có trace; liên kết cha–con thật còn OPEN. |
| 4 | FACT nguồn có metric/log; chất lượng file OPEN. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | Application/resource/network/pod interventions theo paper; loại cụ thể theo hệ chưa census. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Theo protocol: fresh deploy/warmup/pre-injection baseline, lọc baseline bất thường; chưa kiểm file. |
| 9 | TT dùng lại Fang/FSE. Cả ba hệ chung nhóm/injector/collector. OpenRCA1 khác raw AIOps; vẫn trùng một số tác giả, không đủ ba trục độc lập. |

Nguồn cho bảng: [paper v2](runs/run-001/sources/openrca2-paper-v2.html).

## 3. Nhãn, số ca và khả năng phân xử

Paper nói 500 evaluable instances tổng ba hệ, 27 primary kinds; không gán tổng này cho riêng Hotel Reservation.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. Nguồn đã đọc chưa có public release nhãn riêng; chỉ paper/submission artifact mô tả. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: Theo A.2/A.4: Parquet trace/metric/log, nhãn root và graph PAVE. Schema thật chưa có payload kiểm.

FACT nguồn có trace; liên kết cha–con thật còn OPEN. FACT nguồn có metric/log; chất lượng file OPEN.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Theo protocol: fresh deploy/warmup/pre-injection baseline, lọc baseline bất thường; chưa kiểm file.

Paper có injection window [t0,t0+duration]; không suy onset thật. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | CANDIDATE root set theo cấp nhãn công bố; cần release/census. |
| Phát hiện thời gian | CANDIDATE injection-regime nếu khoảng tiêm đủ; onset quan sát OPEN. |
| Vùng ảnh hưởng | Có graph propagation do PAVE tạo từ telemetry/quy tắc; không tự xem là nhãn vùng độc lập để chấm RQ3c. |
| Bất thường trace | OPEN: chưa thấy nhãn từng trace được kiểm. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

PAVE dùng root/injection tạo label; cần tách label/graph khỏi input phương pháp. Chọn ca qua SLI/path và loại graph trivial/cycle tạo selection bias.

TT dùng lại Fang/FSE. Cả ba hệ chung nhóm/injector/collector. OpenRCA1 khác raw AIOps; vẫn trùng một số tác giả, không đủ ba trục độc lập. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

OPEN: chưa có inventory public archive ghim; số instance không chuyển thành byte.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | Nguồn đã đọc chưa có public release nhãn riêng; chỉ paper/submission artifact mô tả. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | TT dùng lại Fang/FSE. Cả ba hệ chung nhóm/injector/collector. OpenRCA1 khác raw AIOps; vẫn trùng một số tác giả, không đủ ba trục độc lập. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | Tình trạng public artifact hiện hành chưa xác minh thêm ngoài lượt tìm giới hạn; không khẳng định không tồn tại. Nhãn PAVE không mặc nhiên đáp ứng nhãn vùng độc lập MRP. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.



# LO2 v1

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Nhóm Oulu/Helsinki (Bakhtin, Nyyssölä, Wang, Ping, Mäntylä và cộng sự), Light-OAuth2. Locust correct/error API tasks; Docker/Prometheus/Jaeger, v2 bổ sung cAdvisor.

Nguồn: [LO2 paper](runs/run-001/sources/lo2-paper-v1.html); [record current](runs/run-002/sources/zenodo-14938118-latest.json).

Giấy phép dữ liệu/code: Data CC-BY4.0; v2 record nêu code Apache2.0; license code v1 không thay bằng license data.

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | FACT nguồn công khai; payload chưa tải. |
| 2 | Correct/error API test labels, không phải root cause service của incident. v2 run log có start/end test theo mô tả. |
| 3 | v1 §4.3: mỗi trace một span, nhiều file rỗng; không đủ call graph cha–con. v2 record nói có trace CSV nhưng không chứng minh hạn chế này đã sửa. |
| 4 | FACT nguồn có metric/log; chất lượng file OPEN. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | Erroneous API usage, không phải hardware/network fault injection theo paper v1. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Có correct test; error test trộn correct requests với thêm error task, nên không gán mọi event trong error test là bất thường. |
| 9 | v1/v2 cùng lineage; không là hai bộ độc lập. Một số tác giả chung AnoMod, collector Prometheus/Jaeger chung Eadro; khác miền OAuth2 không tự đủ MRP§4. |

Nguồn cho bảng: [LO2 paper](runs/run-001/sources/lo2-paper-v1.html); [record current](runs/run-002/sources/zenodo-14938118-latest.json).

## 3. Nhãn, số ca và khả năng phân xử

Paper v1: 1.740 runs × 54 tests, gồm correct + 53 error tasks. Test API không là incident RCA độc lập.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. Index v2 riêng 31.028.530 byte vượt dự kiến nguồn 25MB của SPEC; không mở rộng tải. Nhãn root/time incident không có chỉ từ index mô tả. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: Trace CSV công bố Trace ID/Span ID/Operation Name/Start/End/Tags; v1 thiếu cha xuyên operation. JSON metrics và container logs; v2 run_log/index chứa thời gian test.

v1 §4.3: mỗi trace một span, nhiều file rỗng; không đủ call graph cha–con. v2 record nói có trace CSV nhưng không chứng minh hạn chế này đã sửa. FACT nguồn có metric/log; chất lượng file OPEN.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Có correct test; error test trộn correct requests với thêm error task, nên không gán mọi event trong error test là bất thường.

Thời gian bắt đầu/kết thúc test API không tự là onset/end của sự cố hệ thống. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | Không đủ nhãn root cause service theo nguồn hiện có; đích API không thay nhãn nguyên nhân. |
| Phát hiện thời gian | Có thể chấm correct/error ở đơn vị test theo protocol rõ; không mặc định chấm thời gian triệu chứng hoặc service RCA. |
| Vùng ảnh hưởng | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. |
| Bất thường trace | Không suy nhãn từng trace từ correct/error của cả test. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

Tên test và log khởi tạo chứa correctness; record v1 nêu reduce_logs.py loại dòng khởi tạo lộ nhãn. v2 shuffle/duration random giảm quy luật thứ tự, không chứng minh sạch rò.

v1/v2 cùng lineage; không là hai bộ độc lập. Một số tác giả chung AnoMod, collector Prometheus/Jaeger chung Eadro; khác miền OAuth2 không tự đủ MRP§4. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

v1 toàn raw lo2-data.zip 46.483.584.345 byte; sample 1.070.011.492 byte chỉ log/metric, không thay raw.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | Index v2 riêng 31.028.530 byte vượt dự kiến nguồn 25MB của SPEC; không mở rộng tải. Nhãn root/time incident không có chỉ từ index mô tả. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | v1/v2 cùng lineage; không là hai bộ độc lập. Một số tác giả chung AnoMod, collector Prometheus/Jaeger chung Eadro; khác miền OAuth2 không tự đủ MRP§4. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | v1 record nói superseded bởi v2, nhưng endpoint latest của v1 vẫn chính record cũ: v2 là hồ sơ mới, không âm thầm thay DOI. Trace improvement v2 và mapping root còn OPEN. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.



# LO2 v2

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT nguồn: Nhóm Oulu/Helsinki (Bakhtin, Nyyssölä, Wang, Ping, Mäntylä và cộng sự), Light-OAuth2. Locust correct/error API tasks; Docker/Prometheus/Jaeger, v2 bổ sung cAdvisor.

Nguồn: [LO2 paper](runs/run-001/sources/lo2-paper-v1.html); [record current](runs/run-002/sources/zenodo-18937117-latest.json).

Giấy phép dữ liệu/code: Data CC-BY4.0; v2 record nêu code Apache2.0; license code v1 không thay bằng license data.

Record DOI cố định và repo commit ở manifest; không gán metadata.version=null thành tên version. Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | Kết quả và giới hạn |
|---|---|
| 1 | FACT nguồn công khai; payload chưa tải. |
| 2 | Correct/error API test labels, không phải root cause service của incident. v2 run log có start/end test theo mô tả. |
| 3 | v1 §4.3: mỗi trace một span, nhiều file rỗng; không đủ call graph cha–con. v2 record nói có trace CSV nhưng không chứng minh hạn chế này đã sửa. |
| 4 | FACT nguồn có metric/log; chất lượng file OPEN. |
| 5 | OPEN: chưa đếm root theo vị trí đồ thị. |
| 6 | Erroneous API usage, không phải hardware/network fault injection theo paper v1. |
| 7 | OPEN — chưa kiểm số đo; không suy lan từ mô tả bài. |
| 8 | Có correct test; error test trộn correct requests với thêm error task, nên không gán mọi event trong error test là bất thường. |
| 9 | v1/v2 cùng lineage; không là hai bộ độc lập. Một số tác giả chung AnoMod, collector Prometheus/Jaeger chung Eadro; khác miền OAuth2 không tự đủ MRP§4. |

Nguồn cho bảng: [LO2 paper](runs/run-001/sources/lo2-paper-v1.html); [record current](runs/run-002/sources/zenodo-18937117-latest.json).

## 3. Nhãn, số ca và khả năng phân xử

Record v2: 115 runs × 54 tests; chỉ là số công bố, không census index. Test API không là incident RCA độc lập.

Root × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. Index v2 riêng 31.028.530 byte vượt dự kiến nguồn 25MB của SPEC; không mở rộng tải. Nhãn root/time incident không có chỉ từ index mô tả. Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.

Vị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

Schema công bố: Trace CSV công bố Trace ID/Span ID/Operation Name/Start/End/Tags; v1 thiếu cha xuyên operation. JSON metrics và container logs; v2 run_log/index chứa thời gian test.

v1 §4.3: mỗi trace một span, nhiều file rỗng; không đủ call graph cha–con. v2 record nói có trace CSV nhưng không chứng minh hạn chế này đã sửa. FACT nguồn có metric/log; chất lượng file OPEN.

Schema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.

## 5. Dữ liệu bình thường và mốc thời gian

Có correct test; error test trộn correct requests với thêm error task, nên không gán mọi event trong error test là bất thường.

Thời gian bắt đầu/kết thúc test API không tự là onset/end của sự cố hệ thống. Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Chấm được đến đâu theo nguồn |
|---|---|
| Xếp hạng | Không đủ nhãn root cause service theo nguồn hiện có; đích API không thay nhãn nguyên nhân. |
| Phát hiện thời gian | Có thể chấm correct/error ở đơn vị test theo protocol rõ; không mặc định chấm thời gian triệu chứng hoặc service RCA. |
| Vùng ảnh hưởng | Không có bằng chứng nhãn vùng thật độc lập trong nguồn đã đọc. |
| Bất thường trace | Không suy nhãn từng trace từ correct/error của cả test. |

Các khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.

## 8. Rò nhãn và thông tin phục vụ G1

Tên test và log khởi tạo chứa correctness; record v1 nêu reduce_logs.py loại dòng khởi tạo lộ nhãn. v2 shuffle/duration random giảm quy luật thứ tự, không chứng minh sạch rò.

v1/v2 cùng lineage; không là hai bộ độc lập. Một số tác giả chung AnoMod, collector Prometheus/Jaeger chung Eadro; khác miền OAuth2 không tự đủ MRP§4. Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.

## 9. Kích thước và chi phí

v2 full LO2v2.zip 65.613.664.046 byte; index riêng 31.028.530 byte. Chưa tải; tất cả file/byte ở record-summary.

Nguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.

## 10. Những điều còn mở

| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |
|---|---|---|
| Nhãn/census và nguồn release | Index v2 riêng 31.028.530 byte vượt dự kiến nguồn 25MB của SPEC; không mở rộng tải. Nhãn root/time incident không có chỉ từ index mô tả. | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |
| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |
| Độc lập | v1/v2 cùng lineage; không là hai bộ độc lập. Một số tác giả chung AnoMod, collector Prometheus/Jaeger chung Eadro; khác miền OAuth2 không tự đủ MRP§4. | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |
| Ràng buộc nguồn riêng | v1 record nói superseded bởi v2, nhưng endpoint latest của v1 vẫn chính record cũ: v2 là hồ sơ mới, không âm thầm thay DOI. Trace improvement v2 và mapping root còn OPEN. | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |

Phạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo.
