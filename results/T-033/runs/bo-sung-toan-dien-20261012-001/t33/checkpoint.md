# T033 bổ sung — checkpoint 12/10/2026

Đây là checkpoint hỗ trợ người làm, không là REVIEW chính thức hoặc nghiệm thu.

## Đã kiểm và giữ nguồn

- Native _bocpd/utility/anomaly_detection/phat_hien khớp manifest checkpoint nguồn. Catalog1186 tệp cấp đường dẫn và hash; từng nguồn dùng phải đạt trước đọc. Mọi ghi trong t33/ mới; source/results cũ chỉ đọc.
- Pilot2: Student-t shape, marginal NIW và suffix fixtures PASS; native128 exactm/CP1,935s; native1441×28 exactm/CP224,363s. Pilot1 fixture đặt nhầm shape2I thayI, đã giữ code/stdout/stderr và sửa độc lập theo κ1,df2. Predictive df2 không có covariance hữu hạn; dùng thuật ngữ predictive shape.
- Fastcontext30/30 và graph-probe30/30 xong. Full messages trong union các cửa sổ khóa đã đọc, không chỉ first/last. Window10/30/60s giữ count-weighted duration; không coi INFO là request-success hoặc nền sạch. N-Sigma directprevious100rows, không giả định independence/normality.
- Fast narrow rolling100 first-post: earlier18/equal7/later5; wideequal30. BOCPD anypostCP tạiD30/60/120/300/600s=12/23/27/29/30. Nguồn: fast-summary-001.json và pin/case pointers trong file. Giữ earlyfirst, không thay P3 hoặc dựng onset/end thật.
- Graph scores chỉ computational dependency; degree-preserving rewiring được kiểm. Nút lấy từ whole-record conditional inventory, cạnh parent-span theo start100s chưa bảo đảm availableonline; formula/single seed không là phương pháp P6 đã chọn hoặc bằng chứng benefit.

## Đang chạy

TrênEC2 3.107.246.249, thư mục /home/ubuntu/rca/T-033/runs/bo-sung-toan-dien-20261012-001/t33/:

- theta-v3.py PID50943:120nguồn/607điểmBOCPD uniqueNPZ, targetstates/log-density. Giữ threadsunset như nguồn để exactnativeθ/density. Trial1 scalar vàtrial2nativebatchdướithreads1 có relative densitydiff5.3e-14; đã dừng và giữ lỗi, không miễn gate. Trial3unset đãPASS nhiều nguồn. Manual log-density algebra đối chiếu scipy.logpdf, fixedbound1e-10 chỉchoalgebra, khôngCP. Mẫu trước max2.2e-13.
- engine_supervisor.py PID51070; workerpart0 PID51071:15ca parity0 ×nativefullsham+7canthiệp. Nativefullshamthread1ca1PASS241,458s; prior_df4ca1PASS241,949s. Mỗi ca phải nativefullm/CP exact trước branch mới. Part1 được coordinator khởi sautheta xong để mỗi lúc tối đa2luồngnặng. Envthreads1 chỉ các engine mới, nguồn cũ không đổi.
- Trạng thái/logs: theta-v3-unset.stdout/stderr; engine-part0.stdout/stderr; engine-queue-status.json; supervisor-events.jsonl; sauhaiworker engine-part{0,1}-complete.json. Queue xử lý finiteall30, không tự retry lỗi.

## Còn phải làm để có báo cáo hoàn chỉnh

1. Hoàn tất và audit theta120nguồn/607điểm, gồm cácθabsent trước; không gọi partial thànhxong.
2. Hoàn tất7enginebranches×30ca, ghi outcomes/error đúng native và coverage. Chưa có kết quả prior/causal/staircase toànlô; không chọn kết quả cađầu.
3. Nhận immutable outputs/hash2đầu, chạy summary mới (không ghi đè fast-summary-001), kiểm bổ sung arithmetic/mapping/coverage/sourceunchanged và báo mọi ca.
4. Bổ sung rollingfinitecounts khi diễn giải missinghistory; curveD dùnginclusiveproxy, không physicaltruth. Marginal NIW thực tế/coherence cần nối derivation/nativecode/fixture và dữ kiện inputcommon, không gọi dof danh nghĩa là prior-confounding riêng.
5. K1 physicalonset/negative/end/requestoutcome/completeness chưa ghi không thể tạo từ các phép này. Nêu chính xác thiếu trường, hệ quả đánh giá và yêu cầu quan sátFlashTicket; không đẩy phần vẫn kiểm được sang giới hạndata.

Ngân sách mới do Minh cho phép qua đêm; estimateengine2workers~8–10hwall còn phải cập nhật từcase/schema thực. Native d22–39, rawselector25–48 theo sourceinput; causal đổi schema/mask/d/prior cùngscale, không quy effect riêng causal. Thetaunsetd≥33 có thể chậm hơnpilotd28; xem logactual trướcETAcuối. Không có tiến trình tính nặngT033 trênlaptop, có thể tắt laptop sauhandoff khi nguồn/kết quả đã nhận và cácjobEC2 được xácminh. Đừng tắtEC2 khiqueuechưa xong.
