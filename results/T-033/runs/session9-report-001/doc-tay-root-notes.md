# Đối chiếu đọc tay bổ sung của người làm

File này bổ sung bảng toàn đường/toàn nhóm ở doc-tay.md. Giá trị lấy trực tiếp từ file đã pin, không lấy helper notes làm chứng cứ. Không mở hoặc gửi Claude review.

## Cặp telemetry ở đúng điểm native

Dev-03 full BOCPD trước proxy: i683 noCP→i684 CP. Workload raw của route cùng37,733, nhưng span-start bin route có60→90 span; mean duration raw1652,7667→1822,5111 và median1267→1277. Sau proxy: i723 noCP→i724 CP; workload raw route cùng31,2, span93→33, mean duration12487,3548→35565,4545, median1917→4613. Chuỗi native ở chuoi-bang-chung.json#/units/4/points/0,1,3,4 chỉ đúng bước posterior/MAP đổi tại CP.

Con trỏ nguồn duration: NPZ `runs/channel-pilot-001/dev-03d4910932--context.npz`, entity_index18=ts-route-service; rows8986/8999 cho i683/684, rows9525/9539 cho i723/724. Các array `trace_group_duration_mean_raw`, `trace_group_duration_median_raw`, `trace_group_span_count`, `trace_group_second`, `trace_group_entity`. Projection tại duration-at-locked-points.json giữ source_row và second tương ứng. Workload-at-locked-points.json#/rows/7,8,11,12 có route ở cột18. Source-catalog.json giải đường NPZ sang bản laptop và hash.

Đây là đồng xuất hiện của duration quan sát và quyết định khác khi workload raw của riêng route giữ nguyên. Nó bác cách diễn giải rằng cứ workload raw riêng route tăng mới có CP ở các cặp này. Nó chưa giữ mọi tải/cột/history/sampling, chưa xác nhận duration đúng đơn vị hay tất cả request được ghi; không chứng minh duration là nguyên nhân của CP. Multivariate density tiêu thụ các kênh khác với aggregation duration này. StatusCode ở những span nguồn không được ghi; không suy error/success.

Dev-03 narrow first125 do security latency. Cặp i124→125 có workload security0,067→0,2; không có trace group security quan sát ở hai bin, nhưng có route groups. Chuỗi cùng cột security có margin âm→dương, đã ghi tại same-column-controls.json#/rows/0. Nguồn workload#/rows/1,2; duration projection đúng index/second không có entity20 trong hai bin. Đồng xuất hiện tăng workload hỗ trợ một ứng viên tải, chưa chứng minh tải gây latency; thiếu observed security span chưa chứng minh mất collector hoặc không request. Quan hệ workload unit, request boundary và completeness cần K1/K5.

## Lịch sử fixed khác native ở cùng x, không chỉ số first

Dev-143 narrow end i1440, route latency x=0,011981132075471704. Native mean0,008470126481379089, threshold0,01585171001621652, margin−0,012340704422123904 nên False. Fixed mean0,004249920804543327, threshold0,004141800707526941, margin+0,003589410563401436 nên True. Giữ cùng x/k/fill; thay gói history đủ đổi phép so tại cột này. Không tách riêng mean với std, không nói baseline fixed sạch hoặc tốt hơn.

Nguồn full gzip `runs/session7-manual-rest-001/dev-14372e1209--points.json.gz#/units/5/points/5`: columns/24, x/24, mean/24, threshold/24, margin/24, fixed_baseline/mean_fixed/24, fixed_baseline/threshold_fixed/24, fixed_arrays/margin_fixed/24. Reduced native-only witness tại end không giữ route khi nativeFalse; không lấy reduced làm chứng “freeze không có tác động”.

## Cờ nhóm và cặp CP/noCP

Dev-03 B4/w30/k3 False ở683/684 (max ratio1,468208651/1,919986569); BOCPD chỉ CP684. Dev-12 B4 True ở127/128 (8,215005394/8,025976432); BOCPD chỉ CP128. B4 là descriptor marginal raw-after-fill ngoài detector, nhìn cửa sổ sau điểm. Hai cặp cho thấy B4 không quyết CP; chưa chứng minh covariance là nguyên nhân riêng. Code/feature pin trong additional-source-verification.json; source features B4_all_Nv/30/index tại T-029; native chain units4/11.

Dev-143 N1 có denominator đoạn400:720 hữu hạn nhưng số cờ bằngzero; tỷ lệ tail0. Cờ N1 True không xác nhận lịch sử ngắn gây first. Cột preserve ở first107 có count75, x giảm và positive margin; cặp106 không báo. Đối chứng ca168 báo102 qua order latency, không qua preserve; khác observed coverage. Cần giữ những điều kiện này khi diễn giải N1. Source `results/T-029/features-no-label/nsigma/dev-14372e1209--nsigma.json#/history/400:720`, cùng-cột row8 và bao-phu-nhom.json#/groups/15.

## Các mức bằng chứng giữ nguyên

Quan sát là giá trị/saved intermediate đã hash. Cơ chế tính toán là phép so/normalization/MAP-to-CP trong điều kiện đầu vào ấy. Phân rã scale và gói mask/d/prior là can thiệp chẩn đoán đã được khai, không chọn phương pháp online. Tải, sự cố thật, onset và lợi ích đồ thị là OPEN/candidate. Cặp khác ca không giữ được mọi điều kiện; ca proxy-S không tự là ca đúng vận hành. Các nghĩa vụ nghiên cứu thiếu được ghi K1–K7, không bị xóa vì task đã đủ file.
