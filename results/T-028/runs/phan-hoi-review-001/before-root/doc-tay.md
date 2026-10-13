# Đọc tay các ca theo codebook

Mẫu được chọn trước đọc theo codebook §8, gộp mục trùng và giữ mọi yêu cầu theo k/cơ chế. Ghi nhận gốc: `results/T-028/runs/buoc3-005/manual-re2.json` và `manual-nezha.json`. Bản hợp nhất: `results/T-028/runs/buoc3-005/manual-reading.json`.

Đã đọc 70 mục phương pháp × ca, tương ứng 106 yêu cầu nhóm; không thấy gán tự động lệch tiêu chí đã duyệt. Nguồn số: `manual-reading.json` → `case_method_n`, `requirements_n`, `criterion_mismatches_n`. Khớp tiêu chí quan sát chưa xác nhận giải thích nhân quả. Không sửa codebook.

Mỗi mục dưới là ví dụ cho các nhóm được ghi ở dòng Yêu cầu. Giá trị đầy đủ, availability/N/A và seed nằm trong `observed_values` của bản hợp nhất; đọc tay không điền trung gian bằng chạy lại phương pháp.

## Nezha-OB · baro · dev-1ac905bc95

Root phân tích: `frontend`. Yêu cầu: k=1, M0; k=5, M0.

BARO trả frontend ở hạng 10, key 1.1889938916035074, sau chín entity có key lớn hơn. Root có trong O và R; không hòa cắt biên. Graph N không quan sát ancestor của frontend nên M5=False và P0=0 dù b=9. M6 của BARO là N/A. Vì không có M1–M6 True, M0 đúng ở cả k=1 và k=5. Metric theo quy ước SimpleRCA có 21 kênh với events=0 nhưng log A có 1040 dòng keyword; không được gọi root là không có lỗi. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/0`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/181`.

Seed `single` (nguồn `/main_rows/181/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":9,"group_index":0,"group_size":1,"block_size":1},"root_key":[1.1889938916035074],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"no_native_activation_threshold"},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":10,"a":0,"b":9},"5":{"value":0.0,"availability":"available","reason":null,"n":10,"a":0,"b":9}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /0`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /0`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/181`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate/trace_start/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate/trace_end/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate/logs_A/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate/operations_end`

## Nezha-OB · baro · dev-27252dca60

Root phân tích: `productcatalogservice`. Yêu cầu: k=1, M5; k=5, M5.

BARO trả productcatalogservice hạng 7, key 3.2251980228734562. recommendationservice là caller trực tiếp trong N và có key 26.303030303029693 lớn hơn root, nên M5 đúng ở cả hai k. Checkout/frontend cũng là ancestor nhưng không chắc chắn trước root; không đếm chúng thay cho giao của ancestor với trước root. Root có 9 events metric và 768 keyword log; P95A 3309 không vượt 3×3217. M5 không cần proxy dương và không xác nhận root thiếu tín hiệu. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/1`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/182`.

Seed `single` (nguồn `/main_rows/182/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":6,"group_index":0,"group_size":1,"block_size":1},"root_key":[3.2251980228734562],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"no_native_activation_threshold"},"P0":{"1":{"value":0.9880952380952381,"availability":"available","reason":null,"n":10,"a":3,"b":6},"5":{"value":0.9880952380952381,"availability":"available","reason":null,"n":10,"a":3,"b":6}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /1`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /1`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/182`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-27252dca60.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-27252dca60.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-27252dca60.json → /aggregate/trace_start/productcatalogservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-27252dca60.json → /aggregate/trace_end/productcatalogservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-27252dca60.json → /aggregate/logs_A/productcatalogservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-27252dca60.json → /aggregate/operations_end`

## Nezha-OB · baro · dev-2bfc97b01e

Root phân tích: `checkoutservice`. Yêu cầu: k=1, M0.

BARO trả checkoutservice hạng 2 với key 94.00000000000095, sau emailservice 215.09187676863715. Ancestor duy nhất frontend có key 6.107537522678549 thấp hơn root, vì vậy M5=False. M0 đúng ở k=1; k=5 đã đúng nên không gán cơ chế. Root có 16 events metric, giữ M6=N/A của BARO thay vì suy cờ từ điểm hoặc events. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/2`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/183`.

Seed `single` (nguồn `/main_rows/183/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":1,"group_index":0,"group_size":1,"block_size":1},"root_key":[94.00000000000095],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"no_native_activation_threshold"},"P0":{"1":{"value":0.1111111111111111,"availability":"available","reason":null,"n":10,"a":1,"b":1},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /2`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /2`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/183`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-2bfc97b01e.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-2bfc97b01e.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-2bfc97b01e.json → /aggregate/trace_start/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-2bfc97b01e.json → /aggregate/trace_end/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-2bfc97b01e.json → /aggregate/logs_A/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-2bfc97b01e.json → /aggregate/operations_end`

## Nezha-OB · baro · dev-3b92690644

Root phân tích: `checkoutservice`. Yêu cầu: k=1, M0.

BARO trả checkoutservice hạng 3 với key 40.00000000000073. shippingservice và adservice đứng trước có key 216.00700667720076 và 58.2017545263159 nhưng không là ancestor root; frontend là ancestor và key 26.095852534562376 nằm dưới root. Vì vậy M0 đúng k=1. Root có 17 events metric và 32 keyword log; không thiếu toàn bộ tín hiệu. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/3`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/185`.

Seed `single` (nguồn `/main_rows/185/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":2,"group_index":0,"group_size":1,"block_size":1},"root_key":[40.00000000000073],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"no_native_activation_threshold"},"P0":{"1":{"value":0.2222222222222222,"availability":"available","reason":null,"n":10,"a":1,"b":2},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /3`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /3`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/185`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-3b92690644.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-3b92690644.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-3b92690644.json → /aggregate/trace_start/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-3b92690644.json → /aggregate/trace_end/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-3b92690644.json → /aggregate/logs_A/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-3b92690644.json → /aggregate/operations_end`

## Nezha-OB · baro · dev-5467884de4

Root phân tích: `recommendationservice`. Yêu cầu: k=1, M5.

BARO trả recommendationservice hạng 4, key 64.09803921568745. frontend là ancestor trực tiếp và key 177.3082078349991 đứng trước root, nên M5 đúng k=1; k=5 đúng. P95 trace của root giảm trong cả split, proxy 2/3/4 False, nhưng proxy không là điều kiện M5. Hai metric latency có tổng 3 events; đó là mô tả theo SimpleRCA, không là ngưỡng BARO. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/4`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/188`.

Seed `single` (nguồn `/main_rows/188/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":3,"group_index":0,"group_size":1,"block_size":1},"root_key":[64.09803921568745],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"no_native_activation_threshold"},"P0":{"1":{"value":0.3333333333333333,"availability":"available","reason":null,"n":10,"a":1,"b":3},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /4`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /4`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/188`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5467884de4.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5467884de4.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5467884de4.json → /aggregate/trace_start/recommendationservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5467884de4.json → /aggregate/trace_end/recommendationservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5467884de4.json → /aggregate/logs_A/recommendationservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5467884de4.json → /aggregate/operations_end`

## Nezha-OB · baro · dev-5ada15752d

Root phân tích: `frontend`. Yêu cầu: k=1, M0; k=5, M0.

BARO trả frontend hạng 8, key 3.933649289099526, không hòa tại biên đang xét. Không ancestor quan sát trong graph N, M5=False, P0=0 dù b=7. M6=N/A và không có cờ khác True nên M0 đúng ở k=1 và k=5. Root có 21 metric events=0 nhưng log A có 1100 keyword; không đồng nhất M0 với không có tín hiệu. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/5`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/190`.

Seed `single` (nguồn `/main_rows/190/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":7,"group_index":0,"group_size":1,"block_size":1},"root_key":[3.933649289099526],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"no_native_activation_threshold"},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":10,"a":0,"b":7},"5":{"value":0.0,"availability":"available","reason":null,"n":10,"a":0,"b":7}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /5`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /5`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/190`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate/trace_start/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate/trace_end/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate/logs_A/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate/operations_end`

## Nezha-OB · baro · dev-607751ac0a

Root phân tích: `checkoutservice`. Yêu cầu: k=1, M0; k=5, M0.

BARO trả checkoutservice hạng 8 với key 5.014259252537352. Bảy entity chắc chắn trước root đều không là ancestor; frontend là ancestor nhưng key 2.9602417142183395 thấp hơn root. M0 đúng ở cả k, dù P0=7/9 mô tả cơ hội của null. Root có đủ 16 metric và trace/log nhưng không có phiếu SimpleRCA dương; BARO vẫn giữ M6=N/A. Shipping key 2426.1875000011446 lớn là số native đã lưu, không là ngưỡng hoặc chứng minh nguyên nhân. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/6`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/191`.

Seed `single` (nguồn `/main_rows/191/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":7,"group_index":0,"group_size":1,"block_size":1},"root_key":[5.014259252537352],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"no_native_activation_threshold"},"P0":{"1":{"value":0.7777777777777778,"availability":"available","reason":null,"n":10,"a":1,"b":7},"5":{"value":0.7777777777777778,"availability":"available","reason":null,"n":10,"a":1,"b":7}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /6`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /6`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/191`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-607751ac0a.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-607751ac0a.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-607751ac0a.json → /aggregate/trace_start/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-607751ac0a.json → /aggregate/trace_end/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-607751ac0a.json → /aggregate/logs_A/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-607751ac0a.json → /aggregate/operations_end`

## Nezha-OB · baro · dev-63c30faf34

Root phân tích: `recommendationservice`. Yêu cầu: k=5, M5.

BARO trả recommendationservice hạng 7, key 8.861347416669172; frontend key 73.3287144629281 là ancestor trực tiếp chắc chắn trước. M5 đúng k=5 được yêu cầu và cũng có ở k=1. P0=n10,a1,b6 cho 2/3. Root có 16 metric events=0, log A 1148 dòng nhưng keyword=0, P95A thấp hơn N; không chuyển các số này thành M6 của BARO. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/7`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/192`.

Seed `single` (nguồn `/main_rows/192/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":6,"group_index":0,"group_size":1,"block_size":1},"root_key":[8.861347416669172],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"no_native_activation_threshold"},"P0":{"1":{"value":0.6666666666666666,"availability":"available","reason":null,"n":10,"a":1,"b":6},"5":{"value":0.6666666666666666,"availability":"available","reason":null,"n":10,"a":1,"b":6}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /7`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /7`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/192`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-63c30faf34.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-63c30faf34.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-63c30faf34.json → /aggregate/trace_start/recommendationservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-63c30faf34.json → /aggregate/trace_end/recommendationservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-63c30faf34.json → /aggregate/logs_A/recommendationservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-63c30faf34.json → /aggregate/operations_end`

## Nezha-OB · baro · dev-7b7c973198

Root phân tích: `emailservice`. Yêu cầu: k=1, M0.

BARO trả emailservice hạng 4 với key 10.358974358974356. Ba entity trước root là currency/shipping/ad, không thuộc ancestor checkout/frontend; hai ancestor có key thấp hơn root. M0 đúng k=1, k=5 đúng. Root có 6 events metric, trace P95A 650 thấp hơn N 798.8000000000005 và keyword=0; dữ liệu metric khác luật span native. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/8`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/195`.

Seed `single` (nguồn `/main_rows/195/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":3,"group_index":0,"group_size":1,"block_size":1},"root_key":[10.358974358974356],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"no_native_activation_threshold"},"P0":{"1":{"value":0.5833333333333334,"availability":"available","reason":null,"n":10,"a":2,"b":3},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /8`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /8`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/195`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate/trace_start/emailservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate/trace_end/emailservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate/logs_A/emailservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate/operations_end`

## Nezha-OB · baro · dev-9b9397a4dc

Root phân tích: `recommendationservice`. Yêu cầu: k=1, M0.

BARO trả recommendationservice hạng 2 với key 115.34463585195282, sau adservice 131.33333333333323 không là ancestor. frontend là ancestor nhưng key 111.20691956445376 thấp hơn root. M0 đúng k=1. Có 6 events CPU; P95N trace hơn 3 triệu us khiến proxy False không chứng minh nền sạch. Không dùng điểm robust liên tục để gán M6. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/9`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/199`.

Seed `single` (nguồn `/main_rows/199/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":1,"group_index":0,"group_size":1,"block_size":1},"root_key":[115.34463585195282],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"no_native_activation_threshold"},"P0":{"1":{"value":0.1111111111111111,"availability":"available","reason":null,"n":10,"a":1,"b":1},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /9`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /9`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/199`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-9b9397a4dc.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-9b9397a4dc.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-9b9397a4dc.json → /aggregate/trace_start/recommendationservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-9b9397a4dc.json → /aggregate/trace_end/recommendationservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-9b9397a4dc.json → /aggregate/logs_A/recommendationservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-9b9397a4dc.json → /aggregate/operations_end`

## Nezha-OB · microrank_full · dev-14701a3bbb

Root phân tích: `shippingservice`. Yêu cầu: k=1, M5; k=5, M5.

MicroRank trả shippingservice hạng 6, key 23.911912362580363; frontend key 295.6145278895255 là ancestor trực tiếp chắc chắn trước root, nên M5 đúng k=1 và k=5. Năm operation root có 126 span A bất thường theo ngưỡng riêng, nên M6=False. P95A 99989.25us vượt mọi mốc 2/3/4 so N 526.65us; root vẫn có tín hiệu mạnh. Điểm PageRank/spectrum không được thay bằng tổng count. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/10`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/224`.

Seed `single` (nguồn `/main_rows/224/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":5,"group_index":0,"group_size":1,"block_size":1},"root_key":[23.911912362580363],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.8333333333333334,"availability":"available","reason":null,"n":10,"a":2,"b":5},"5":{"value":0.8333333333333334,"availability":"available","reason":null,"n":10,"a":2,"b":5}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /10`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /10`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/224`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-14701a3bbb.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-14701a3bbb.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-14701a3bbb.json → /aggregate/trace_start/shippingservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-14701a3bbb.json → /aggregate/trace_end/shippingservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-14701a3bbb.json → /aggregate/logs_A/shippingservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-14701a3bbb.json → /aggregate/operations_end`

## Nezha-OB · microrank_full · dev-1ac905bc95

Root phân tích: `frontend`. Yêu cầu: k=1, M0.

MicroRank trả frontend hạng 3, key 423.660168584685, sau currency/productcatalog; graph N không có ancestor frontend. Root có 58 span A bất thường trên 11 operation nên M6=False; O/R phủ root, không hòa biên. M0 đúng k=1, k=5 đúng. Dữ kiện không phân xử thiên hướng spectrum, tải chung hay căn nguyên fault. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/11`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/225`.

Seed `single` (nguồn `/main_rows/225/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":2,"group_index":0,"group_size":1,"block_size":1},"root_key":[423.660168584685],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":10,"a":0,"b":2},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /11`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /11`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/225`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate/trace_start/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate/trace_end/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate/logs_A/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate/operations_end`

## Nezha-OB · microrank_full · dev-27252dca60

Root phân tích: `productcatalogservice`. Yêu cầu: k=1, M5.

MicroRank trả productcatalogservice hạng 3, key 299.297151446084; frontend key 305.5715724995761 là ancestor trực tiếp trước root nên M5 đúng k=1. Sáu operation root có 3 span bất thường, đều ở sql.rows với nN=2939,nA=1089, μ=0.07ms,σ=0.15ms,ngưỡng=0.52ms. Vì tổng lớn hơn 0, M6=False. Root P95 gần như không đổi không thay thế count native. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/12`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/226`.

Seed `single` (nguồn `/main_rows/226/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":2,"group_index":0,"group_size":1,"block_size":1},"root_key":[299.297151446084],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.5833333333333334,"availability":"available","reason":null,"n":10,"a":3,"b":2},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /12`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /12`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/226`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-27252dca60.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-27252dca60.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-27252dca60.json → /aggregate/trace_start/productcatalogservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-27252dca60.json → /aggregate/trace_end/productcatalogservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-27252dca60.json → /aggregate/logs_A/productcatalogservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-27252dca60.json → /aggregate/operations_end`

## Nezha-OB · microrank_full · dev-2bfc97b01e

Root phân tích: `checkoutservice`. Yêu cầu: k=5, M5.

MicroRank trả checkoutservice hạng 8, key 0.07121603422995025. frontend key 49.21771314642473 là ancestor trực tiếp chắc chắn trước, nên M5 đúng k=5. Root có 17 operation với 39 span A bất thường; M6=False dù key rất thấp. Có thể điểm khác do operation coverage và spectrum; không suy từ một key rằng root không phát tín hiệu. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/13`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/227`.

Seed `single` (nguồn `/main_rows/227/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":7,"group_index":0,"group_size":1,"block_size":1},"root_key":[0.07121603422995025],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.7777777777777778,"availability":"available","reason":null,"n":10,"a":1,"b":7},"5":{"value":0.7777777777777778,"availability":"available","reason":null,"n":10,"a":1,"b":7}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /13`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /13`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/227`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-2bfc97b01e.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-2bfc97b01e.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-2bfc97b01e.json → /aggregate/trace_start/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-2bfc97b01e.json → /aggregate/trace_end/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-2bfc97b01e.json → /aggregate/logs_A/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-2bfc97b01e.json → /aggregate/operations_end`

## Nezha-OB · microrank_full · dev-5ada15752d

Root phân tích: `frontend`. Yêu cầu: k=1, M0.

MicroRank trả frontend hạng 4, key 511.7754476225163, sau currency/productcatalog/cart. Graph N không có ancestor root, M5=False; root có 90 span A bất thường trên 11 operation, M6=False. Không có M1–M6 True nên M0 đúng k=1. Log và metric không là đầu vào của nhánh MicroRank này. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/14`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/234`.

Seed `single` (nguồn `/main_rows/234/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":3,"group_index":0,"group_size":1,"block_size":1},"root_key":[511.7754476225163],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":10,"a":0,"b":3},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /14`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /14`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/234`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate/trace_start/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate/trace_end/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate/logs_A/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate/operations_end`

## Nezha-OB · microrank_full · dev-7b7c973198

Root phân tích: `emailservice`. Yêu cầu: k=1, M6; k=5, M6.

MicroRank trả emailservice cùng key 0.26443122238185546 với paymentservice ở vị trí 8–9; hòa này nằm sau cả k đang xét nên M3=False. frontend đứng trước và là ancestor, M5=True. Operation email có nN=20,nA=41, μ=0.57ms,σ=0.24ms,ngưỡng=1.29ms và 0 span bất thường, nên M6=True. Có 39 trace bất thường chứa operation dù span email không bất thường; không lẫn count trace với span. Đa nhãn M5+M6, primary M5, root vẫn ở R nên không M2. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/15`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/239`.

Seed `single` (nguồn `/main_rows/239/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":7,"group_index":0,"group_size":2,"block_size":2},"root_key":[0.26443122238185546],"root_location_availability":"available","local_nonpositive":{"value":true,"availability":"available","reason":null},"P0":{"1":{"value":0.9722222222222222,"availability":"available","reason":null,"n":10,"a":2,"b":7},"5":{"value":0.9722222222222222,"availability":"available","reason":null,"n":10,"a":2,"b":7}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /15`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /15`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/239`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate/trace_start/emailservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate/trace_end/emailservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate/logs_A/emailservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate/operations_end`

## Nezha-OB · simplerca · dev-1ac905bc95

Root phân tích: `frontend`. Yêu cầu: k=1, M0; k=5, M3.

SimpleRCA frontend có score 1=0 events metric+0 trace vote+1 log vote; keyword log là 1040, không phải 1040 điểm. Cartservice cũng score 1 tại khối hạng 5–6 nên Hit@5=1/2 và M3 đúng k=5. Hit@1=0, không có ancestor và local_nonpositive=False nên M0 đúng k=1. Không dùng thứ tự hiển thị trong hòa để gọi frontend chắc chắn đứng sau cartservice. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/16`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/203`.

Seed `single` (nguồn `/main_rows/203/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":4,"group_index":0,"group_size":2,"block_size":2},"root_key":[1.0],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":10,"a":0,"b":4},"5":{"value":0.0,"availability":"available","reason":null,"n":10,"a":0,"b":4}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /16`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /16`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/203`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate/trace_start/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate/trace_end/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate/logs_A/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate/operations_end`

## Nezha-OB · simplerca · dev-396c8dbf7d

Root phân tích: `emailservice`. Yêu cầu: k=1, M5.

SimpleRCA emailservice có score 32=31 events metric+1 trace vote+0 log vote; checkoutservice score 38 là caller trực tiếp trước root. M5 đúng k=1; root đứng thứ 2 nên k=5 đúng. Root có nN22/nA38 trace với P95 661.65/999680.9us; dấu M5 cùng tồn tại với tín hiệu root mạnh, không xác nhận thiếu kênh hoặc lan. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/17`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/206`.

Seed `single` (nguồn `/main_rows/206/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":1,"group_index":0,"group_size":1,"block_size":1},"root_key":[32.0],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.2222222222222222,"availability":"available","reason":null,"n":10,"a":2,"b":1},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /17`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /17`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/206`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-396c8dbf7d.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-396c8dbf7d.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-396c8dbf7d.json → /aggregate/trace_start/emailservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-396c8dbf7d.json → /aggregate/trace_end/emailservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-396c8dbf7d.json → /aggregate/logs_A/emailservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-396c8dbf7d.json → /aggregate/operations_end`

## Nezha-OB · simplerca · dev-3b92690644

Root phân tích: `checkoutservice`. Yêu cầu: k=1, M5.

SimpleRCA checkoutservice score 18=17 events metric+0 trace vote+1 log vote, sau frontend score 32 là ancestor trực tiếp. M5 đúng k=1; k=5 đúng. Log A 734 dòng có 32 keyword, trace P95A 341392.7999999997 không vượt 3×222793.0. Không cộng keyword count trực tiếp vào score hoặc dùng proxy để bác M5. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/18`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/207`.

Seed `single` (nguồn `/main_rows/207/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":1,"group_index":0,"group_size":1,"block_size":1},"root_key":[18.0],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.1111111111111111,"availability":"available","reason":null,"n":10,"a":1,"b":1},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /18`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /18`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/207`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-3b92690644.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-3b92690644.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-3b92690644.json → /aggregate/trace_start/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-3b92690644.json → /aggregate/trace_end/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-3b92690644.json → /aggregate/logs_A/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-3b92690644.json → /aggregate/operations_end`

## Nezha-OB · simplerca · dev-515c5f2190

Root phân tích: `recommendationservice`. Yêu cầu: k=1, M0.

SimpleRCA recommendationservice score 3=2 events CPU+1 trace vote+0 log vote, sau adservice score 4 không là ancestor. Frontend là ancestor nhưng score 1 thấp hơn root; M5=False, M6=False. M0 đúng k=1 dù P95 root tăng từ 24181.999999999996 lên 3109399.9us. Chưa phân loại không có nghĩa thiếu tín hiệu. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/19`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/209`.

Seed `single` (nguồn `/main_rows/209/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":1,"group_index":0,"group_size":1,"block_size":1},"root_key":[3.0],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.1111111111111111,"availability":"available","reason":null,"n":10,"a":1,"b":1},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /19`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /19`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/209`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-515c5f2190.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-515c5f2190.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-515c5f2190.json → /aggregate/trace_start/recommendationservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-515c5f2190.json → /aggregate/trace_end/recommendationservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-515c5f2190.json → /aggregate/logs_A/recommendationservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-515c5f2190.json → /aggregate/operations_end`

## Nezha-OB · simplerca · dev-5ada15752d

Root phân tích: `frontend`. Yêu cầu: k=1, M0; k=5, M0.

SimpleRCA frontend score 1 chỉ từ log vote với 1100 keyword; năm entity score lớn hơn đứng trước nên Hit@1/5 đều 0. Không ancestor quan sát, local_nonpositive=False, không hòa cắt biên; M0 đúng cả hai k. Cửa sổ có 21 metric events=0 và P95 trace giảm, nhưng log có bằng chứng theo luật đã khai. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/20`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/212`.

Seed `single` (nguồn `/main_rows/212/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":4,"group_index":0,"group_size":1,"block_size":1},"root_key":[1.0],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":10,"a":0,"b":5},"5":{"value":0.0,"availability":"available","reason":null,"n":10,"a":0,"b":5}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /20`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /20`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/212`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate/trace_start/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate/trace_end/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate/logs_A/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate/operations_end`

## Nezha-OB · simplerca · dev-607751ac0a

Root phân tích: `checkoutservice`. Yêu cầu: k=1, M6; k=5, M5; k=5, M6.

SimpleRCA checkoutservice có score 0: đủ 16 metric mỗi phía 5 điểm, events=0; trace start nN708/nA688 và P95A188424.9 không vượt 3×246441.44999999995; log A886 dòng, keyword0. M6 đúng, không do kênh thiếu. frontend score4 là ancestor trước root score0, nên đa nhãn M5+M6 và primary M5 ở cả hai k. Theo luật operation khác, raw root có 39 span bất thường; không dùng M6 SimpleRCA làm chuẩn bất thường chung. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/21`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/213`.

Seed `single` (nguồn `/main_rows/213/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":6,"group_index":0,"group_size":2,"block_size":2},"root_key":[0.0],"root_location_availability":"available","local_nonpositive":{"value":true,"availability":"available","reason":null},"P0":{"1":{"value":0.8888888888888888,"availability":"available","reason":null,"n":10,"a":1,"b":8},"5":{"value":0.8888888888888888,"availability":"available","reason":null,"n":10,"a":1,"b":8}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /21`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /21`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/213`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-607751ac0a.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-607751ac0a.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-607751ac0a.json → /aggregate/trace_start/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-607751ac0a.json → /aggregate/trace_end/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-607751ac0a.json → /aggregate/logs_A/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-607751ac0a.json → /aggregate/operations_end`

## Nezha-OB · simplerca · dev-63c30faf34

Root phân tích: `recommendationservice`. Yêu cầu: k=1, M6; k=5, M5; k=5, M6.

SimpleRCA recommendationservice score0 với đủ 16 metric events0, trace start1010/1148 và P95A7769.049999999992 thấp hơn N35077.35, log1148 dòng keyword0. M6 đúng theo phiếu native; frontend score27 là ancestor trước nên M5+M6 và primary M5 ở cả hai k. Theo ngưỡng operation riêng còn 12 span root bất thường; không suy không có lỗi từ score0. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/22`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/214`.

Seed `single` (nguồn `/main_rows/214/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":6,"group_index":0,"group_size":3,"block_size":3},"root_key":[0.0],"root_location_availability":"available","local_nonpositive":{"value":true,"availability":"available","reason":null},"P0":{"1":{"value":0.7777777777777778,"availability":"available","reason":null,"n":10,"a":1,"b":7},"5":{"value":0.7777777777777778,"availability":"available","reason":null,"n":10,"a":1,"b":7}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /22`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /22`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/214`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-63c30faf34.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-63c30faf34.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-63c30faf34.json → /aggregate/trace_start/recommendationservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-63c30faf34.json → /aggregate/trace_end/recommendationservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-63c30faf34.json → /aggregate/logs_A/recommendationservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-63c30faf34.json → /aggregate/operations_end`

## Nezha-OB · simplerca · dev-7b7c973198

Root phân tích: `emailservice`. Yêu cầu: k=1, M0.

SimpleRCA emailservice score6=6 events metric, trace vote0 và log vote0. Cart/currency score9 cùng đứng trước, không là ancestor; checkout score5 và frontend score0 là ancestor nhưng sau root. M0 đúng k=1, k=5 đúng. Hòa top hai entity không chứa root và root không cắt biên, nên không gán M3. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/23`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/217`.

Seed `single` (nguồn `/main_rows/217/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":1,"group_index":0,"group_size":1,"block_size":1},"root_key":[6.0],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.4166666666666667,"availability":"available","reason":null,"n":10,"a":2,"b":2},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /23`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /23`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/217`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate/trace_start/emailservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate/trace_end/emailservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate/logs_A/emailservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate/operations_end`

## Nezha-OB · simplerca · dev-8ecd9880ed

Root phân tích: `checkoutservice`. Yêu cầu: k=1, M0.

SimpleRCA checkoutservice score4=3 events metric+1 log vote, sau ad15/payment10/cart8 không là ancestor. frontend là ancestor nhưng score1 thấp hơn root nên M5=False, M6=False, M0 đúng k=1. Root hòa currency score4 ở hạng4–5, cả khối nằm trong top5 nên Hit@5=1 và không M3. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/24`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/219`.

Seed `single` (nguồn `/main_rows/219/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":3,"group_index":0,"group_size":2,"block_size":2},"root_key":[4.0],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.3333333333333333,"availability":"available","reason":null,"n":10,"a":1,"b":3},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /24`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /24`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/219`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-8ecd9880ed.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-8ecd9880ed.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-8ecd9880ed.json → /aggregate/trace_start/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-8ecd9880ed.json → /aggregate/trace_end/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-8ecd9880ed.json → /aggregate/logs_A/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-8ecd9880ed.json → /aggregate/operations_end`

## Nezha-OB · simplerca · dev-9b9397a4dc

Root phân tích: `recommendationservice`. Yêu cầu: k=1, M0.

SimpleRCA recommendationservice score6 từ hai kênh CPU mỗi kênh3 events; cartservice score10 đứng trước nhưng không là ancestor. Root hòa productcatalog score6 ở hạng2–3, ngoài top1 và nằm trọn top5 nên Hit1=0,Hit5=1, không M3 tại hai biên. Frontend ancestor score0 thấp hơn root; M0 đúng k=1. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/25`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/221`.

Seed `single` (nguồn `/main_rows/221/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":1,"group_index":0,"group_size":2,"block_size":2},"root_key":[6.0],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.1111111111111111,"availability":"available","reason":null,"n":10,"a":1,"b":1},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /25`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /25`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/221`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-9b9397a4dc.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-9b9397a4dc.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-9b9397a4dc.json → /aggregate/trace_start/recommendationservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-9b9397a4dc.json → /aggregate/trace_end/recommendationservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-9b9397a4dc.json → /aggregate/logs_A/recommendationservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-9b9397a4dc.json → /aggregate/operations_end`

## Nezha-OB · tracerca · dev-14701a3bbb

Root phân tích: `shippingservice`. Yêu cầu: k=1, M5.

TraceRCA shippingservice key0.07685098406747891 đứng thứ2 sau frontend key0.23304680038204392, một ancestor trực tiếp, nên M5 đúng k=1. Năm operation shipping có tổng126 span A bất thường, M6=False; k=5 đúng. Root P95 tăng mạnh và có ji hữu hạn, vì vậy M5 ở đây không mô tả root hoàn toàn im lặng. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/26`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/246`.

Seed `single` (nguồn `/main_rows/246/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":1,"group_index":0,"group_size":1,"block_size":1},"root_key":[0.07685098406747891],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.2222222222222222,"availability":"available","reason":null,"n":10,"a":2,"b":1},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /26`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /26`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/246`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-14701a3bbb.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-14701a3bbb.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-14701a3bbb.json → /aggregate/trace_start/shippingservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-14701a3bbb.json → /aggregate/trace_end/shippingservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-14701a3bbb.json → /aggregate/logs_A/shippingservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-14701a3bbb.json → /aggregate/operations_end_tracerca`

## Nezha-OB · tracerca · dev-1ac905bc95

Root phân tích: `frontend`. Yêu cầu: k=1, M0.

TraceRCA frontend key0.0303030303030303 đứng thứ3 sau checkout/currency, không có ancestor frontend trong N. Root có58 span A bất thường nên M6=False; root ở O và R. M0 đúng k=1, k=5 đúng. R chỉ có9 entity nhưng entity bị lọc không phải root; không suy M2 từ tổng ji_nan13. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/27`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/247`.

Seed `single` (nguồn `/main_rows/247/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":2,"group_index":0,"group_size":1,"block_size":1},"root_key":[0.0303030303030303],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":10,"a":0,"b":2},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /27`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /27`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/247`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate/trace_start/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate/trace_end/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate/logs_A/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-1ac905bc95.json → /aggregate/operations_end_tracerca`

## Nezha-OB · tracerca · dev-27252dca60

Root phân tích: `productcatalogservice`. Yêu cầu: k=1, M5; k=5, M5.

TraceRCA productcatalogservice key0.00468384074941452 đứng cuối R gồm8 entity. Frontend key0.07727272727272727 và checkout key0.02912621359223301 là ancestor trước root, nên M5 đúng cả k. Root có3 span bất thường ở sql.rows, M6=False. P0 dùng O10,a3,b7 cho giá trị1, giữ cả vị trí không trả về; không thay n bằng |R|8. P0=1 không là p-value hoặc nhãn lan. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/28`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/248`.

Seed `single` (nguồn `/main_rows/248/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":7,"group_index":0,"group_size":1,"block_size":1},"root_key":[0.00468384074941452],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":1.0,"availability":"available","reason":null,"n":10,"a":3,"b":7},"5":{"value":1.0,"availability":"available","reason":null,"n":10,"a":3,"b":7}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /28`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /28`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/248`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-27252dca60.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-27252dca60.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-27252dca60.json → /aggregate/trace_start/productcatalogservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-27252dca60.json → /aggregate/trace_end/productcatalogservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-27252dca60.json → /aggregate/logs_A/productcatalogservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-27252dca60.json → /aggregate/operations_end_tracerca`

## Nezha-OB · tracerca · dev-2bfc97b01e

Root phân tích: `checkoutservice`. Yêu cầu: k=5, M5.

TraceRCA checkoutservice key0.015923566878980888 đứng thứ6 sau năm entity; frontend key0.04210526315789474 là ancestor trực tiếp chắc chắn trước, nên M5 đúng k=5. Root có39 span bất thường trên17 operation, M6=False. Root vẫn có key hữu hạn trong R9; không suy M2 hoặc thiếu tín hiệu từ hạng6. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/29`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/249`.

Seed `single` (nguồn `/main_rows/249/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":5,"group_index":0,"group_size":1,"block_size":1},"root_key":[0.015923566878980888],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.5555555555555556,"availability":"available","reason":null,"n":10,"a":1,"b":5},"5":{"value":0.5555555555555556,"availability":"available","reason":null,"n":10,"a":1,"b":5}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /29`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /29`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/249`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-2bfc97b01e.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-2bfc97b01e.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-2bfc97b01e.json → /aggregate/trace_start/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-2bfc97b01e.json → /aggregate/trace_end/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-2bfc97b01e.json → /aggregate/logs_A/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-2bfc97b01e.json → /aggregate/operations_end_tracerca`

## Nezha-OB · tracerca · dev-396c8dbf7d

Root phân tích: `emailservice`. Yêu cầu: k=1, M3.

TraceRCA frontend, checkout và emailservice có full key bằng nhau chính xác 0.08076514346439957 tại khối hạng1–3. Email Hit@1=1/3 nên M3 đúng. Hai ancestor frontend/checkout hòa root, không chắc chắn trước; M5=False và b=0,P0=0. Root operation nN22/nA38,ngưỡng0.75ms và38 span A bất thường nên M6=False. Không dùng thứ tự hiển thị hoặc cận hạng trừ một để tạo M5. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/30`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/250`.

Seed `single` (nguồn `/main_rows/250/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":0,"group_index":0,"group_size":3,"block_size":3},"root_key":[0.08076514346439957],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":10,"a":2,"b":0},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /30`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /30`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/250`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-396c8dbf7d.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-396c8dbf7d.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-396c8dbf7d.json → /aggregate/trace_start/emailservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-396c8dbf7d.json → /aggregate/trace_end/emailservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-396c8dbf7d.json → /aggregate/logs_A/emailservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-396c8dbf7d.json → /aggregate/operations_end_tracerca`

## Nezha-OB · tracerca · dev-5ada15752d

Root phân tích: `frontend`. Yêu cầu: k=1, M0.

TraceRCA frontend key0.02707930367504835 đứng thứ3 sau currency/checkout; graph N không có ancestor root nên M5=False. Root có90 span A bất thường trên11 operation, M6=False, nằm trong O/R. M0 đúng k=1 và k=5 đúng; sự hiện diện nhiều span bất thường chưa quyết định thứ hạng ji/service-max. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/31`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/256`.

Seed `single` (nguồn `/main_rows/256/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":2,"group_index":0,"group_size":1,"block_size":1},"root_key":[0.02707930367504835],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":10,"a":0,"b":2},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /31`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /31`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/256`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate/trace_start/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate/trace_end/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate/logs_A/frontend`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-5ada15752d.json → /aggregate/operations_end_tracerca`

## Nezha-OB · tracerca · dev-7b7c973198

Root phân tích: `emailservice`. Yêu cầu: k=1, M2; k=1, M6; k=5, M2; k=5, M6.

TraceRCA emailservice thuộc O10 nhưng ngoài R9 và không có operation email trong ranking hữu hạn. Operation email duy nhất nN20/nA41,μ0.57ms,σ0.24ms,ngưỡng1.29ms,abnormal0; nên M6=True. Trong bản ghi OK, zero abnormal với nền đủ và tổng abnormal996 đã lưu giải thích ji email không hữu hạn bị lọc: M2+M6,primary M2 ở cả k. M5/P0=N/A vì root ngoài R, dù graph có checkout/frontend ancestors. Không suy mọi M2 từ ji_nan hoặc suy ngược M2⇒M6. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/32`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/261`.

Seed `single` (nguồn `/main_rows/261/evidence/seed_evidence/single`): `{"status":"OK","root_location":null,"root_key":null,"root_location_availability":"N/A; root outside R or non-OK","local_nonpositive":{"value":true,"availability":"available","reason":null},"P0":{"1":{"value":null,"availability":"N/A","reason":"root_not_returned"},"5":{"value":null,"availability":"N/A","reason":"root_not_returned"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /32`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /32`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/261`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate/trace_start/emailservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate/trace_end/emailservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate/logs_A/emailservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-7b7c973198.json → /aggregate/operations_end_tracerca`

## Nezha-OB · tracerca · dev-8ecd9880ed

Root phân tích: `checkoutservice`. Yêu cầu: k=5, M3.

TraceRCA checkoutservice và paymentservice có full key bằng nhau chính xác 0.008583690987124463 ở hạng5–6, nên Hit@5=1/2 và M3 đúng. Frontend key0.07792207792207793 là ancestor trước root nên M5 cũng True; primary giữ M3 và đa nhãn M3+M5. Root có9 span A bất thường trên17 operation nên M6=False. P0=n10,a1,b4=4/9 mô tả null, không thay tiêu chí hòa. khớp tiêu chí; cơ chế ứng viên hoặc rào cản trực tiếp theo codebook, chưa kiểm nhân quả

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/33`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/263`.

Seed `single` (nguồn `/main_rows/263/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":4,"group_index":0,"group_size":2,"block_size":2},"root_key":[0.008583690987124463],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.4444444444444444,"availability":"available","reason":null,"n":10,"a":1,"b":4},"5":{"value":0.4444444444444444,"availability":"available","reason":null,"n":10,"a":1,"b":4}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-005/manual-selection.json → /33`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /33`; `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/263`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-8ecd9880ed.json → /aggregate`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-8ecd9880ed.json → /aggregate/metrics`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-8ecd9880ed.json → /aggregate/trace_start/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-8ecd9880ed.json → /aggregate/trace_end/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-8ecd9880ed.json → /aggregate/logs_A/checkoutservice`; `results/T-028/runs/buoc3-002/features-no-label/Nezha-OB/dev-8ecd9880ed.json → /aggregate/operations_end_tracerca`

## RE2-TT · baro · dev-14372e1209

Root phân tích: `ts-route-service`. Yêu cầu: k=1, M0.

Root có nhiều events raw và P95 tăng; khóa BARO lớn nhất của root vẫn nhỏ hơn consign-price. Entity duy nhất chắc chắn trước root không thuộc ancestor quan sát. M0 khớp, không phải không có tín hiệu.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/34`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/2`.

Seed `single` (nguồn `/main_rows/2/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":1,"group_index":0,"group_size":1,"block_size":1},"root_key":[3907.4188034195304],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"no_native_activation_threshold"},"P0":{"1":{"value":0.13432835820895522,"availability":"available","reason":null,"n":68,"a":9,"b":1},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-14372e1209.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /34`; `results/T-024/runs/baro-30-001/luot/baro-a-dev-14372e1209-sNone-h0-9b694a/ban-ghi-0.json → `

## RE2-TT · baro · dev-16597725c1

Root phân tích: `ts-auth-service`. Yêu cầu: k=1, M0.

Khóa mem và latency root đều dương, nhiều metric events; các entity khác vẫn có khóa lớn hơn. Graph không quan sát ancestor root nên M5 False và P0 bằng không khi đủ điều kiện; chưa loại thiếu phụ thuộc thực hoặc cấu trúc chấm điểm.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/35`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/3`.

Seed `single` (nguồn `/main_rows/3/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":3,"group_index":0,"group_size":1,"block_size":1},"root_key":[47.48000000000497],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"no_native_activation_threshold"},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":68,"a":0,"b":3},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-16597725c1.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /35`; `results/T-024/runs/baro-30-001/luot/baro-a-dev-16597725c1-sNone-h0-b83c52/ban-ghi-0.json → `

## RE2-TT · baro · dev-57546fd87b

Root phân tích: `ts-auth-service`. Yêu cầu: k=1, M0; k=5, M0.

Raw latency-50/mem có events nhưng khóa BARO sau preprocessing của root nằm sau nhiều entity. Không ancestor quan sát và không hòa biên; M0 ở cả hai k. Raw events không thay robust-z hoặc tạo M6.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/36`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/12`.

Seed `single` (nguồn `/main_rows/12/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":40,"group_index":0,"group_size":1,"block_size":1},"root_key":[3.105726872246616],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"no_native_activation_threshold"},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":68,"a":0,"b":40},"5":{"value":0.0,"availability":"available","reason":null,"n":68,"a":0,"b":40}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-57546fd87b.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /36`; `results/T-024/runs/baro-30-001/luot/baro-a-dev-57546fd87b-sNone-h0-3fb7f2/ban-ghi-0.json → `

## RE2-TT · baro · dev-59f696a169

Root phân tích: `ts-auth-service`. Yêu cầu: k=1, M0.

Khóa station lớn hơn root rất ít theo số thực đã lưu nhưng không bằng nhau. Giữ strict full key, không tolerance; M0 top1, top5 đúng. Metric root có events nhưng chưa phân xử vì sao station có điểm cao hơn.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/37`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/13`.

Seed `single` (nguồn `/main_rows/13/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":1,"group_index":0,"group_size":1,"block_size":1},"root_key":[102.54545454548047],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"no_native_activation_threshold"},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":68,"a":0,"b":1},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-59f696a169.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /37`; `results/T-024/runs/baro-30-001/luot/baro-a-dev-59f696a169-sNone-h0-db76fe/ban-ghi-0.json → `

## RE2-TT · baro · dev-746fd74313

Root phân tích: `ts-auth-service`. Yêu cầu: k=1, M0.

Root latency key dương, đứng sau user/contacts; không ancestor quan sát nên M0. Proxy đổi giữa mốc chính và độ nhạy cao; orphan nhiều làm quan hệ graph là giới hạn cần giữ, không tự sửa graph.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/38`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/14`.

Seed `single` (nguồn `/main_rows/14/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":2,"group_index":0,"group_size":1,"block_size":1},"root_key":[30.68613180352903],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"no_native_activation_threshold"},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":68,"a":0,"b":2},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-746fd74313.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /38`; `results/T-024/runs/baro-30-001/luot/baro-a-dev-746fd74313-sNone-h0-7cac1b/ban-ghi-0.json → `

## RE2-TT · baro · dev-a5cabe5fa7

Root phân tích: `ts-travel-service`. Yêu cầu: k=1, M5; k=5, M5.

Food và seat là direct caller, khóa lớn hơn root, P95 cả root và hai caller tăng tại cả ba mốc. M5 khớp ở hai k; cùng xuất hiện vẫn phù hợp caller tự bất thường/tác động chung. BARO không nhận graph và M6 N/A.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/39`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/19`.

Seed `single` (nguồn `/main_rows/19/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":15,"group_index":0,"group_size":1,"block_size":1},"root_key":[17.28571428571457],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"no_native_activation_threshold"},"P0":{"1":{"value":0.7959980157861718,"availability":"available","reason":null,"n":68,"a":6,"b":15},"5":{"value":0.7959980157861718,"availability":"available","reason":null,"n":68,"a":6,"b":15}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-a5cabe5fa7.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /39`; `results/T-024/runs/baro-30-001/luot/baro-a-dev-a5cabe5fa7-sNone-h0-5a663b/ban-ghi-0.json → `

## RE2-TT · baro · dev-a915aa2424

Root phân tích: `ts-travel-service`. Yêu cầu: k=1, M5; k=5, M5.

Nhiều proper ancestor chắc chắn trước root. Có caller proxy tăng nhưng preserve/preserve-other/travel2 có cờ độ nhạy khác hoặc đều False. M5 giữ nguyên, không yêu cầu mọi ancestor tăng và chưa xác nhận lan.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/40`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/20`.

Seed `single` (nguồn `/main_rows/20/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":28,"group_index":0,"group_size":1,"block_size":1},"root_key":[4.81283212032114],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"no_native_activation_threshold"},"P0":{"1":{"value":0.9673069768459754,"availability":"available","reason":null,"n":68,"a":6,"b":28},"5":{"value":0.9673069768459754,"availability":"available","reason":null,"n":68,"a":6,"b":28}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-a915aa2424.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /40`; `results/T-024/runs/baro-30-001/luot/baro-a-dev-a915aa2424-sNone-h0-714b10/ban-ghi-0.json → `

## RE2-TT · baro · dev-f81f88234e

Root phân tích: `ts-auth-service`. Yêu cầu: k=1, M0; k=5, M0.

Root còn trong O/R và có khóa dương; các entity ưu tiên không là ancestor quan sát. Metric raw mem/latency có events, M0 không đồng nghĩa không lỗi hoặc không tín hiệu; M6 BARO vẫn N/A.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/41`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/27`.

Seed `single` (nguồn `/main_rows/27/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":10,"group_index":0,"group_size":1,"block_size":1},"root_key":[4.887212977968917],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"no_native_activation_threshold"},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":68,"a":0,"b":10},"5":{"value":0.0,"availability":"available","reason":null,"n":68,"a":0,"b":10}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-f81f88234e.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /41`; `results/T-024/runs/baro-30-001/luot/baro-a-dev-f81f88234e-sNone-h0-ed16f9/ban-ghi-0.json → `

## RE2-TT · circa_ols_da · dev-03d4910932

Root phân tích: `ts-route-service`. Yêu cầu: k=1, M4; k=1, M5.

Thuộc danh sách ca lỗi làm tròn đã khóa, đồng thời ancestor travel/travel2/admin-travel có full DA key lớn hơn. Root nodes sau prune không rỗng và có RHT đạt/vượt ngưỡng nên M6 False. M4 primary, M5 đa nhãn; chưa quy mọi thất bại root cho lỗi ca.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/42`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/120`.

Seed `single` (nguồn `/main_rows/120/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":3,"group_index":0,"group_size":1,"block_size":1},"root_key":[1345.5116288948645,-8.0,558.2690237401874],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.3558918693247051,"availability":"available","reason":null,"n":68,"a":9,"b":3},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-03d4910932.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /42`; `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-03d4910932-sNone-h0-e54417/ban-ghi-0.json → `

## RE2-TT · circa_ols_da · dev-16597725c1

Root phân tích: `ts-auth-service`. Yêu cầu: k=1, M0; k=5, M0.

Root RHT mem/latency vượt ngưỡng, regression routes/parents được lưu; full DA key root vẫn thua nhiều entity. Không ancestor quan sát, không hòa biên, không thuộc cohort lỗi. M0 khớp cả k, không nói metric root bình thường.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/43`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/123`.

Seed `single` (nguồn `/main_rows/123/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":14,"group_index":0,"group_size":1,"block_size":1},"root_key":[1229.3240488740346,-1.0,823.6754411910313],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":68,"a":0,"b":14},"5":{"value":0.0,"availability":"available","reason":null,"n":68,"a":0,"b":14}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-16597725c1.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /43`; `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-16597725c1-sNone-h0-89c66d/ban-ghi-0.json → `

## RE2-TT · circa_ols_da · dev-3ae0a6c15a

Root phân tích: `ts-train-service`. Yêu cầu: k=1, M4; k=1, M5.

M4 theo cohort lỗi, M5 theo ba ancestor có full DA key lớn hơn; root RHT latency vượt ngưỡng. Proxy các caller không tăng tại mốc chính dù M5 True, nên cách giải thích lan chưa được proxy này hỗ trợ; không đổi gán.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/44`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/128`.

Seed `single` (nguồn `/main_rows/128/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":3,"group_index":0,"group_size":1,"block_size":1},"root_key":[5089.800873591814,-8.0,3418.862441469279],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.3558918693247051,"availability":"available","reason":null,"n":68,"a":9,"b":3},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-3ae0a6c15a.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /44`; `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-3ae0a6c15a-sNone-h0-829d79/ban-ghi-0.json → `

## RE2-TT · circa_ols_da · dev-57546fd87b

Root phân tích: `ts-auth-service`. Yêu cầu: k=1, M0; k=5, M0.

Tập nodes sau prune đầy đủ; có RHT cpu/mem vượt ngưỡng, M6 False dù vài metric dưới ngưỡng. Root full key thấp hơn nhiều entity DB/service, không ancestor quan sát; M0 cả hai k. Cấu trúc DA/coverage và nền còn chưa phân xử.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/45`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/132`.

Seed `single` (nguồn `/main_rows/132/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":45,"group_index":0,"group_size":1,"block_size":1},"root_key":[12.902034932230944,-1.0,11.480143269692935],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":68,"a":0,"b":45},"5":{"value":0.0,"availability":"available","reason":null,"n":68,"a":0,"b":45}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-57546fd87b.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /45`; `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-57546fd87b-sNone-h0-862055/ban-ghi-0.json → `

## RE2-TT · circa_ols_da · dev-746fd74313

Root phân tích: `ts-auth-service`. Yêu cầu: k=1, M0.

RHT latency/socket/cpu/mem có phần vượt ngưỡng; xét full DA key thay score đầu đơn lẻ. Root trả về nhưng top1 sai, top5 đúng; M0. Không diễn giải orphan/cột vắng là nguyên nhân đã tách.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/46`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/134`.

Seed `single` (nguồn `/main_rows/134/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":3,"group_index":0,"group_size":1,"block_size":1},"root_key":[66.2058249870179,-1.0,6.845612088582394],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":68,"a":0,"b":3},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-746fd74313.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /46`; `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-746fd74313-sNone-h0-6c30c3/ban-ghi-0.json → `

## RE2-TT · circa_ols_da · dev-f81f88234e

Root phân tích: `ts-auth-service`. Yêu cầu: k=1, M0; k=5, M0.

RHT mem/latency vượt ngưỡng, full key root đứng sau DB/service khác; M0 hai k. Nodes có tuyến hồi quy và parents, không có regression_error; điều này loại thiếu diagnostics cho mẫu nhưng chưa loại bias mô hình/nền.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/47`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/147`.

Seed `single` (nguồn `/main_rows/147/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":21,"group_index":0,"group_size":1,"block_size":1},"root_key":[37.407846231056126,-1.0,7.561158998785279],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":68,"a":0,"b":21},"5":{"value":0.0,"availability":"available","reason":null,"n":68,"a":0,"b":21}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-f81f88234e.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /47`; `results/T-031/runs/circa-ols-h0-001/luot/circa-a-dev-f81f88234e-sNone-h0-5efd38/ban-ghi-0.json → `

## RE2-TT · microrank_full · dev-12a1a88069

Root phân tích: `ts-order-service`. Yêu cầu: k=1, M5; k=5, M5.

Root operations có span A đạt ngưỡng, M6 False. Seat/travel2 là ancestor chắc chắn trước root nhưng proxy caller đều False; M5 khớp, P0 có cơ hội lớn vì nhiều vị trí trước root. Chưa quy điểm MicroRank cho lan hoặc cho raw P95.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/48`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/61`.

Seed `single` (nguồn `/main_rows/61/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":10,"group_index":0,"group_size":1,"block_size":1},"root_key":[13.486001245684848],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.9963386727688787,"availability":"available","reason":null,"n":27,"a":9,"b":10},"5":{"value":0.9963386727688787,"availability":"available","reason":null,"n":27,"a":9,"b":10}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-12a1a88069.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /48`; `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-12a1a88069-sNone-h0-b85991/ban-ghi-0.json → `

## RE2-TT · microrank_full · dev-14372e1209

Root phân tích: `ts-route-service`. Yêu cầu: k=1, M0.

Root operations có nhiều span bất thường theo luật native, score đứng sau station. Station không thuộc ancestor quan sát root; M0 top1. Tín hiệu root dương không bảo đảm root nhận score cao nhất.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/49`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/62`.

Seed `single` (nguồn `/main_rows/62/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":1,"group_index":0,"group_size":1,"block_size":1},"root_key":[989.5508151110374],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.34615384615384615,"availability":"available","reason":null,"n":27,"a":9,"b":1},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-14372e1209.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /49`; `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-14372e1209-sNone-h0-e8c41f/ban-ghi-0.json → `

## RE2-TT · microrank_full · dev-16597725c1

Root phân tích: `ts-auth-service`. Yêu cầu: k=1, M0; k=5, M0.

Root login/repository/find có span A đạt ngưỡng và baseline hữu hạn, nhưng score thấp hơn nhóm đứng đầu. Graph không quan sát ancestor root, M0 hai k. Thiếu tín hiệu cục bộ dương đã bị loại cho mẫu theo đúng luật, nguyên nhân điểm thấp chưa kiểm.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/50`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/63`.

Seed `single` (nguồn `/main_rows/63/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":8,"group_index":0,"group_size":1,"block_size":1},"root_key":[15.236308693573596],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":27,"a":0,"b":8},"5":{"value":0.0,"availability":"available","reason":null,"n":27,"a":0,"b":8}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-16597725c1.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /50`; `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-16597725c1-sNone-h0-55f476/ban-ghi-0.json → `

## RE2-TT · microrank_full · dev-1e6d61b5ec

Root phân tích: `ts-order-service`. Yêu cầu: k=1, M0; k=5, M0.

Có operation root đạt ngưỡng dù một số operation không đạt. Root trong O/R và chỉ một ancestor quan sát không nằm trước root; M0 cả hai k. Không chạy PageRank để giải thích thêm điểm.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/51`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/65`.

Seed `single` (nguồn `/main_rows/65/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":7,"group_index":0,"group_size":1,"block_size":1},"root_key":[0.15168819047395343],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.3684210526315789,"availability":"available","reason":null,"n":20,"a":1,"b":7},"5":{"value":0.3684210526315789,"availability":"available","reason":null,"n":20,"a":1,"b":7}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-1e6d61b5ec.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /51`; `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-1e6d61b5ec-sNone-h0-5ffe14/ban-ghi-0.json → `

## RE2-TT · microrank_full · dev-20acb4402d

Root phân tích: `ts-order-service`. Yêu cầu: k=1, M0; k=5, M0.

Root có span A dương và score trả về, không hòa biên. Ancestor quan sát không thuộc tập chắc chắn trước root nên M0. Khác biệt điểm native với TraceRCA/SimpleRCA không là lỗi arithmetic thống kê.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/52`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/66`.

Seed `single` (nguồn `/main_rows/66/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":7,"group_index":0,"group_size":1,"block_size":1},"root_key":[0.20144423431275388],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.3684210526315789,"availability":"available","reason":null,"n":20,"a":1,"b":7},"5":{"value":0.3684210526315789,"availability":"available","reason":null,"n":20,"a":1,"b":7}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-20acb4402d.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /52`; `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-20acb4402d-sNone-h0-2b1829/ban-ghi-0.json → `

## RE2-TT · microrank_full · dev-260d332c8d

Root phân tích: `ts-order-service`. Yêu cầu: k=1, M0; k=5, M0.

Root operations có nền và span A dương, M6 False; score thấp hơn nhiều entity nhưng không ancestor chắc chắn trước root. M0 hai k; raw P95 tăng không thay điểm native.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/53`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/67`.

Seed `single` (nguồn `/main_rows/67/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":9,"group_index":0,"group_size":1,"block_size":1},"root_key":[0.03170398615368406],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.47368421052631576,"availability":"available","reason":null,"n":20,"a":1,"b":9},"5":{"value":0.47368421052631576,"availability":"available","reason":null,"n":20,"a":1,"b":9}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-260d332c8d.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /53`; `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-260d332c8d-sNone-h0-0d7ac8/ban-ghi-0.json → `

## RE2-TT · microrank_full · dev-3ae0a6c15a

Root phân tích: `ts-train-service`. Yêu cầu: k=1, M0.

Root train có span A dương theo cả ba operation, score sau station/route. Hai entity này không thỏa ancestor-to-root; M0 top1, top5 đúng. Không gán cohort CIRCA cho MicroRank.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/54`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/68`.

Seed `single` (nguồn `/main_rows/68/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":2,"group_index":0,"group_size":1,"block_size":1},"root_key":[418.50421849368524],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.5815384615384616,"availability":"available","reason":null,"n":27,"a":9,"b":2},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-3ae0a6c15a.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /54`; `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-3ae0a6c15a-sNone-h0-7910fe/ban-ghi-0.json → `

## RE2-TT · microrank_full · dev-3defe3d34b

Root phân tích: `ts-auth-service`. Yêu cầu: k=1, M0; k=5, M0.

Root auth có span A dương, M6 False và graph không quan sát ancestor. Score native vẫn thua các service khác, M0 hai k; cần can thiệp/rerun để phân xử cấu trúc chấm điểm, ngoài task.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/55`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/69`.

Seed `single` (nguồn `/main_rows/69/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":9,"group_index":0,"group_size":1,"block_size":1},"root_key":[13.447218624541023],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":27,"a":0,"b":9},"5":{"value":0.0,"availability":"available","reason":null,"n":27,"a":0,"b":9}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-3defe3d34b.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /55`; `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-3defe3d34b-sNone-h0-d38dd0/ban-ghi-0.json → `

## RE2-TT · microrank_full · dev-4f8a844308

Root phân tích: `ts-route-service`. Yêu cầu: k=1, M0.

Root route score đứng sau station, operations root có span A dương. Không có giao ancestor với chắc chắn trước root; M0 top1. Proxy root tăng nhưng không là tiêu chí đổi nhóm.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/56`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/71`.

Seed `single` (nguồn `/main_rows/71/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":1,"group_index":0,"group_size":1,"block_size":1},"root_key":[582.3495339983277],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.34615384615384615,"availability":"available","reason":null,"n":27,"a":9,"b":1},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-4f8a844308.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /56`; `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-4f8a844308-sNone-h0-f0dc53/ban-ghi-0.json → `

## RE2-TT · microrank_full · dev-59f696a169

Root phân tích: `ts-auth-service`. Yêu cầu: k=1, M0; k=5, M0.

Root auth có baseline hữu hạn và span bất thường, nhưng score thấp; không ancestor quan sát và không hòa. M0 hai k, chưa tách hiệu ứng cấu trúc chấm điểm khỏi tải/nền của entity khác.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/57`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/73`.

Seed `single` (nguồn `/main_rows/73/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":8,"group_index":0,"group_size":1,"block_size":1},"root_key":[15.38554539584565],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":27,"a":0,"b":8},"5":{"value":0.0,"availability":"available","reason":null,"n":27,"a":0,"b":8}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-59f696a169.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /57`; `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-59f696a169-sNone-h0-0c32ea/ban-ghi-0.json → `

## RE2-TT · microrank_full · dev-746fd74313

Root phân tích: `ts-auth-service`. Yêu cầu: k=1, M0; k=5, M0.

Các operation root có span A đạt luật native; không quy root sai cho thiếu tín hiệu theo M6. M0 hai k; graph orphan nhiều nhưng không sửa hoặc đoán cạnh, phạm vi phụ thuộc quan sát vẫn hạn chế.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/58`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/74`.

Seed `single` (nguồn `/main_rows/74/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":9,"group_index":0,"group_size":1,"block_size":1},"root_key":[4.151771705801773],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":27,"a":0,"b":9},"5":{"value":0.0,"availability":"available","reason":null,"n":27,"a":0,"b":9}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-746fd74313.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /58`; `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-746fd74313-sNone-h0-8b5d24/ban-ghi-0.json → `

## RE2-TT · microrank_full · dev-7f1b6b071d

Root phân tích: `ts-travel-service`. Yêu cầu: k=1, M5; k=5, M5.

Seat direct caller và travel2 ancestor có score lớn hơn; chỉ seat proxy tăng tại các mốc, travel2 đều False. M5 hai k, root operations dương. P0 giữ cơ hội theo n/a/b, không giữ PageRank/operation bias.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/59`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/75`.

Seed `single` (nguồn `/main_rows/75/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":10,"group_index":0,"group_size":1,"block_size":1},"root_key":[8.27443032773066],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.9652173913043478,"availability":"available","reason":null,"n":27,"a":6,"b":10},"5":{"value":0.9652173913043478,"availability":"available","reason":null,"n":27,"a":6,"b":10}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-7f1b6b071d.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /59`; `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-7f1b6b071d-sNone-h0-851c6c/ban-ghi-0.json → `

## RE2-TT · microrank_full · dev-8017c6dc70

Root phân tích: `ts-order-service`. Yêu cầu: k=5, M0.

Root có span A dương và score trong R, không hòa; ancestor duy nhất không chắc chắn trước root. M0 top5 đúng tiêu chí; đọc cả flags top1 nhưng không mở rộng mẫu top1 sau kết quả.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/60`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/76`.

Seed `single` (nguồn `/main_rows/76/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":6,"group_index":0,"group_size":1,"block_size":1},"root_key":[0.7008015660549183],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.3157894736842105,"availability":"available","reason":null,"n":20,"a":1,"b":6},"5":{"value":0.3157894736842105,"availability":"available","reason":null,"n":20,"a":1,"b":6}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-8017c6dc70.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /60`; `results/T-031/runs/microrank-30-001/luot/microrank-a-dev-8017c6dc70-sNone-h0-023da1/ban-ghi-0.json → `

## RE2-TT · simplerca · dev-20acb4402d

Root phân tích: `ts-order-service`. Yêu cầu: k=1, M5; k=5, M5.

Tổng phiếu root khớp các events metric cộng trace vote; log keyword bằng không. Inside-payment là direct caller có score lớn hơn root và proxy tăng. M5 hai k; còn có entity không phải ancestor đứng cao, chưa coi symptom-count là nhân quả.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/61`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/36`.

Seed `single` (nguồn `/main_rows/36/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":13,"group_index":0,"group_size":1,"block_size":1},"root_key":[241.0],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.208955223880597,"availability":"available","reason":null,"n":68,"a":1,"b":14},"5":{"value":0.208955223880597,"availability":"available","reason":null,"n":68,"a":1,"b":14}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-20acb4402d.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /61`; `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-20acb4402d-sNone-h0-b74713/ban-ghi-0.json → `

## RE2-TT · simplerca · dev-7f1b6b071d

Root phân tích: `ts-travel-service`. Yêu cầu: k=1, M5.

Root nhận phiếu metric, trace và log dương nên M6 False. Admin-travel và seat có score lớn hơn, direct caller và proxy tăng. M5 top1; top5 đúng không gán lời giải thích ca sai. Log count là tổng không lưu nội dung và có thể chứa lỗi nền.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/62`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/45`.

Seed `single` (nguồn `/main_rows/45/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":2,"group_index":0,"group_size":1,"block_size":1},"root_key":[887.0],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.1723202170963365,"availability":"available","reason":null,"n":68,"a":6,"b":2},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-7f1b6b071d.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /62`; `results/T-024/runs/simplerca-30-001/luot/simplerca-a-dev-7f1b6b071d-sNone-h0-0bc47f/ban-ghi-0.json → `

## RE2-TT · torai_B · dev-16597725c1

Root phân tích: `ts-auth-service`. Yêu cầu: k=1, M0.

Đọc cả ba seed: root cùng vị trí nhóm trong block dự phòng, các nhóm trước gồm order-other/seat, không ancestor quan sát. M0 top1, top5 đúng; M6/severity N/A vì không có nghĩa ngưỡng local đã chốt.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/63`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/153`.

Seed `0` (nguồn `/main_rows/153/evidence/seed_evidence/0`): `{"status":"OK","root_location":{"block_index":0,"group_index":2,"group_size":1,"block_size":25},"root_key":[0.02288886631183115],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"intermediate_not_saved_requires_rerun"},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":68,"a":0,"b":2},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Seed `1` (nguồn `/main_rows/153/evidence/seed_evidence/1`): `{"status":"OK","root_location":{"block_index":0,"group_index":2,"group_size":1,"block_size":25},"root_key":[0.02288886631183115],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"intermediate_not_saved_requires_rerun"},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":68,"a":0,"b":2},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Seed `2` (nguồn `/main_rows/153/evidence/seed_evidence/2`): `{"status":"OK","root_location":{"block_index":0,"group_index":2,"group_size":1,"block_size":25},"root_key":[0.02288886631183115],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"intermediate_not_saved_requires_rerun"},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":68,"a":0,"b":2},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-16597725c1.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /63`; `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-16597725c1-s0-h0-b566f3/ban-ghi-0.json → `; `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-16597725c1-s1-h0-990d67/ban-ghi-0.json → `; `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-16597725c1-s2-h0-721a29/ban-ghi-0.json → `

## RE2-TT · torai_B · dev-59f696a169

Root phân tích: `ts-auth-service`. Yêu cầu: k=1, M0.

Ba seed cùng block/key/nhóm root nhưng diagnostics tỷ lệ dự phòng có khác. Root sau seat/order-other, không ancestor quan sát và không hòa biên. M0 top1; không coi khác diagnostics seed là ca mới hoặc cơ chế mới.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/64`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/163`.

Seed `0` (nguồn `/main_rows/163/evidence/seed_evidence/0`): `{"status":"OK","root_location":{"block_index":1,"group_index":0,"group_size":1,"block_size":4},"root_key":[0.043636908639782784],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"intermediate_not_saved_requires_rerun"},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":68,"a":0,"b":2},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Seed `1` (nguồn `/main_rows/163/evidence/seed_evidence/1`): `{"status":"OK","root_location":{"block_index":1,"group_index":0,"group_size":1,"block_size":4},"root_key":[0.043636908639782784],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"intermediate_not_saved_requires_rerun"},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":68,"a":0,"b":2},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Seed `2` (nguồn `/main_rows/163/evidence/seed_evidence/2`): `{"status":"OK","root_location":{"block_index":1,"group_index":0,"group_size":1,"block_size":4},"root_key":[0.043636908639782784],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"intermediate_not_saved_requires_rerun"},"P0":{"1":{"value":0.0,"availability":"available","reason":null,"n":68,"a":0,"b":2},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-59f696a169.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /64`; `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-59f696a169-s0-h0-a6a06d/ban-ghi-0.json → `; `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-59f696a169-s1-h0-fdaf51/ban-ghi-0.json → `; `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-59f696a169-s2-h0-6c5cc6/ban-ghi-0.json → `

## RE2-TT · torai_B · dev-a5cabe5fa7

Root phân tích: `ts-travel-service`. Yêu cầu: k=1, M0.

Ba seed root ở block đơn, block order-other có key lớn hơn nhưng không là ancestor. M0 top1, top5 đúng. Có ancestor graph không đủ M5 nếu không chắc chắn trước root; P0 báo từng seed.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/65`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/169`.

Seed `0` (nguồn `/main_rows/169/evidence/seed_evidence/0`): `{"status":"OK","root_location":{"block_index":1,"group_index":0,"group_size":1,"block_size":1},"root_key":[0.06985202951489221],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"intermediate_not_saved_requires_rerun"},"P0":{"1":{"value":0.08955223880597014,"availability":"available","reason":null,"n":68,"a":6,"b":1},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Seed `1` (nguồn `/main_rows/169/evidence/seed_evidence/1`): `{"status":"OK","root_location":{"block_index":1,"group_index":0,"group_size":1,"block_size":1},"root_key":[0.06985202951489221],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"intermediate_not_saved_requires_rerun"},"P0":{"1":{"value":0.08955223880597014,"availability":"available","reason":null,"n":68,"a":6,"b":1},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Seed `2` (nguồn `/main_rows/169/evidence/seed_evidence/2`): `{"status":"OK","root_location":{"block_index":1,"group_index":0,"group_size":1,"block_size":1},"root_key":[0.06985202951489221],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"intermediate_not_saved_requires_rerun"},"P0":{"1":{"value":0.08955223880597014,"availability":"available","reason":null,"n":68,"a":6,"b":1},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-a5cabe5fa7.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /65`; `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-a5cabe5fa7-s0-h0-c1efea/ban-ghi-0.json → `; `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-a5cabe5fa7-s1-h0-a6f96d/ban-ghi-0.json → `; `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-a5cabe5fa7-s2-h0-faa19b/ban-ghi-0.json → `

## RE2-TT · torai_B · dev-f36d0647d5

Root phân tích: `ts-order-service`. Yêu cầu: k=1, M5.

Cả ba seed có seat/travel2 ở block chắc chắn trước root, là proper ancestor; M5 top1, top5 đúng. Proxy hai caller đều False tại mọi mốc, không hỗ trợ suy lan chỉ từ ranking. P0 và flags giữ từng seed, không OR P0.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/66`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/176`.

Seed `0` (nguồn `/main_rows/176/evidence/seed_evidence/0`): `{"status":"OK","root_location":{"block_index":2,"group_index":0,"group_size":1,"block_size":1},"root_key":[0.0826389375980621],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"intermediate_not_saved_requires_rerun"},"P0":{"1":{"value":0.25237449118046135,"availability":"available","reason":null,"n":68,"a":9,"b":2},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Seed `1` (nguồn `/main_rows/176/evidence/seed_evidence/1`): `{"status":"OK","root_location":{"block_index":2,"group_index":0,"group_size":1,"block_size":1},"root_key":[0.0826389375980621],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"intermediate_not_saved_requires_rerun"},"P0":{"1":{"value":0.25237449118046135,"availability":"available","reason":null,"n":68,"a":9,"b":2},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Seed `2` (nguồn `/main_rows/176/evidence/seed_evidence/2`): `{"status":"OK","root_location":{"block_index":2,"group_index":0,"group_size":1,"block_size":1},"root_key":[0.0826389375980621],"root_location_availability":"available","local_nonpositive":{"value":null,"availability":"N/A","reason":"intermediate_not_saved_requires_rerun"},"P0":{"1":{"value":0.25237449118046135,"availability":"available","reason":null,"n":68,"a":9,"b":2},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-f36d0647d5.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /66`; `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-f36d0647d5-s0-h0-9bcbec/ban-ghi-0.json → `; `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-f36d0647d5-s1-h0-e780e0/ban-ghi-0.json → `; `results/T-031/runs/torai-B-ec2-001/luot/torai_B-a-dev-f36d0647d5-s2-h0-1ea50a/ban-ghi-0.json → `

## RE2-TT · tracerca · dev-12a1a88069

Root phân tích: `ts-order-service`. Yêu cầu: k=1, M5.

Root nhiều operation có ji hữu hạn đã lưu và span A dương. Seat có key lớn hơn, direct caller nhưng proxy không tăng. M5 top1, top5 đúng; không suy ji từ P95 hoặc từ ji_nan toàn ca.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/67`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/91`.

Seed `single` (nguồn `/main_rows/91/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":1,"group_index":0,"group_size":1,"block_size":1},"root_key":[0.04452498058503754],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.34615384615384615,"availability":"available","reason":null,"n":27,"a":9,"b":1},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-12a1a88069.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /67`; `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-12a1a88069-sNone-h0-9f2be2/ban-ghi-0.json → `

## RE2-TT · tracerca · dev-20acb4402d

Root phân tích: `ts-order-service`. Yêu cầu: k=1, M0.

Root có operation ji hữu hạn, span A dương và R ngắn hơn O. Entity đứng trước không giao ancestor duy nhất; M0 top1. Root không bị lọc, nên không quy tổng ji_nan ca cho root.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/68`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/96`.

Seed `single` (nguồn `/main_rows/96/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":3,"group_index":0,"group_size":1,"block_size":1},"root_key":[0.047826086956521734],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.15789473684210525,"availability":"available","reason":null,"n":20,"a":1,"b":3},"5":{"value":null,"availability":"N/A","reason":"not_OK_wrong_at_k"}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-20acb4402d.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /68`; `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-20acb4402d-sNone-h0-ec8a01/ban-ghi-0.json → `

## RE2-TT · tracerca · dev-260d332c8d

Root phân tích: `ts-order-service`. Yêu cầu: k=1, M5; k=5, M5.

Inside-payment direct caller có ji key lớn hơn root và proxy tăng; root vẫn có span A dương và ji hữu hạn. M5 ở hai k, không M2/M6. Cơ chế điểm native/caller tự bất thường còn có thể giải thích.

Nguồn ghi nhận và toàn bộ số: `results/T-028/runs/buoc3-005/manual-reading.json → /cases/69`; evidence đã lưu: `results/T-028/runs/buoc3-005/ca-sai.json → /main_rows/97`.

Seed `single` (nguồn `/main_rows/97/evidence/seed_evidence/single`): `{"status":"OK","root_location":{"block_index":8,"group_index":0,"group_size":1,"block_size":1},"root_key":[0.024793388429752063],"root_location_availability":"available","local_nonpositive":{"value":false,"availability":"available","reason":null},"P0":{"1":{"value":0.42105263157894735,"availability":"available","reason":null,"n":20,"a":1,"b":8},"5":{"value":0.42105263157894735,"availability":"available","reason":null,"n":20,"a":1,"b":8}}}`

Nguồn đối chiếu: `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/dev-260d332c8d.json → /aggregate`; `results/T-028/runs/buoc3-005/manual-excerpts.json → /69`; `results/T-024/runs/tracerca-30-001/luot/tracerca-a-dev-260d332c8d-sNone-h0-6be8b2/ban-ghi-0.json → `

## Giải thích khác còn lại

Các nhóm chỉ là dấu hiệu theo tiêu chí đã khai. Cửa sổ/đồng hồ, nền chưa sạch, coverage và mapping, cấu trúc chấm điểm, loại tín hiệu, thông tin parent hoặc common cause, nhãn gốc và độ đại diện còn có thể giải thích sai hạng. Trạng thái cụ thể theo từng nhóm ở `ban-do-han-che-xep-hang.md` §6 và từng ghi nhận gốc. Phép can thiệp sẽ phân xử cần thay đầu vào/chạy phương pháp, nằm ngoài SPEC. Nơi xử lý câu “lan có đáng kể” giữ OPEN.
