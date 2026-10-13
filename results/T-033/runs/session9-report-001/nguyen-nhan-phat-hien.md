# T-033 — Cơ chế phát hiện và giới hạn diễn giải

**Kết quả:** đã lần theo phép tính trên mọi đường xử lý và điểm đã khóa. N-Sigma bật cờ vì độ lệch hai phía vượt ngưỡng quá khứ ở ít nhất một cột. BOCPD bật CP vì MAP run length đổi hơn một đơn vị sau cạnh tranh likelihood × posterior giữa các run length. Phân rã cùng tiền tố xác định tác động nguồn min/max; tác động mask vẫn gắn với số chiều và prior. Chưa xác định nguyên nhân vật lý của mọi báo trước proxy, onset thật, tác động riêng prior hoặc lợi ích của phương pháp đồ thị.

Đây là đầu ra người làm, chờ Claude phản biện và Minh nghiệm thu. Không đóng RQ2/G2, không chọn detector P6, không sửa kết quả P3. Những nhận định dưới đây là quan sát và cơ chế tính toán có điều kiện. Các thiết kế mới là **CANDIDATE, chưa kiểm**. Không có quyết định khoa học mới được tự ghi vào WHY/DECISIONS.

## 1. Câu hỏi nguồn và phạm vi bằng chứng

MRP RQ2/P4 yêu cầu hiểu bước dẫn tới thất bại, thay vì gán nguyên nhân bằng cờ mô tả. DT18-NV2/NV3 và hướng dẫn cô §1 yêu cầu hiểu phương pháp, hạn chế và căn cứ thiết kế đồ thị dùng log/trace/metric. T-033 trả lời phần bộ phát hiện trên RE2-TT dev; xếp hạng, nhiều dataset và đánh giá phương pháp mới còn thuộc công việc khác. Bằng chứng ở đây đủ đề xuất có điều kiện cho P6, chưa đủ chọn thiết kế hoặc khẳng định khắc phục hạn chế.

Tất cả số nghiên cứu lấy từ các file cạnh báo cáo này. `source-catalog.json` ánh xạ đường dẫn EC2 trong JSON sang file laptop đã nhận và manifest tương ứng. Khi ghi `file#/a/b`, `/a/b` là con trỏ JSON; với NPZ, tên array và row được giữ trong `source_pointer`/index. Hash chỉ nằm trong manifest. `additional-source-verification.json` kiểm code chấm, định nghĩa nhóm T-029 và tài liệu B16 đã đọc trực tiếp. Code BARO chính thức được giữ tại `../checkpoint-handoff-001/source-native/`, revision nguồn e35f4ec; đây là căn cứ mô tả triển khai, không gán phát hiện thực nghiệm của T-033 cho tác giả.

Có 210 đơn vị ca × đường xử lý, 968 điểm khóa, 64 nhóm bắt buộc. Mọi scalar điểm khóa và cột làm chứng/cặp cùng cột đã được đọc; không nhận đã đọc từng raw cell hoặc mọi ma trận covariance. Dữ liệu đầy đủ vẫn nằm trong gzip/NPZ. Mẫu số và phép kiểm: `validation.json#/all_units`, `/locked_points`, `/groups`; `doc-tay.md` giữ từng đường và từng nhóm. 120 nhánh factorial đều có đầu ra hợp lệ; 84 nhánh có range0; không có lỗi native hoặc nhánh không có kênh trong mẫu số này. 180 contrasts được định nghĩa. Không bịa ca lỗi để đủ nhóm, không chuyển null thành zero. Nguồn: `supplemental-stats.json#/denominators`.

Khóa nhóm, điểm và matching giữ nguyên. Đối chứng ngoài nhóm thường khác ô, số chiều hoặc observed coverage; collector completeness và việc đối chứng “đúng vật lý” đều OPEN. Một số nhóm không có ca ngoài nhóm. Đối chứng cùng ca/điểm/nhánh vẫn được giữ, nhưng không đổi điểm để tìm kết quả thuận lợi. `bao-phu-nhom.json#/groups` khai từng hạn chế; bảng ở `doc-tay.md` chỉ cơ chế tính toán của từng đường, không lan từ đại diện sang mọi thành viên.

## 2. N-Sigma: đầu vào → thống kê quá khứ → cờ cột → OR → chấm

Adapter dùng Inf→NaN rồi forward fill (điền từ quá khứ). Native bắt đầu ở i100, tính mean/std mẫu với ddof=1 trên `[:i]`, và báo khi `abs(x_i−mean_past)>3*std_past`. Phép so là strict `>` và hai phía. Không có sàn std. Cờ gộp là OR mọi cột, nên không giữ hướng tăng/giảm hay nguồn cột trong timestamp báo động trả về. Code: `src/p3/adapters/phat_hien.py`, native `anomaly_detection.py`; các arrays x/count/mean/std/threshold/margin/Z nối tại `nsigma-trung-gian/index.json`.

**Giá trị thay đổi đủ xa khỏi nền:** dev-03, security latency tại i125 có x=0,046875, mean=0,03967056, std=0,00164125, margin=+0,00228068; cùng cột tại i124 có margin=−0,00203139. Cột này đủ làm OR bật. Chuỗi này phân xử phép so tại hai điểm gần nhau; tải hoặc lỗi vật lý gây thay đổi x vẫn chưa biết. Nguồn chính xác: `nsigma-trung-gian/same-column-controls.json#/rows/0/same_column_values/0`.

**Giảm latency cũng bật cờ:** dev-f81, contacts latency tại i490 giảm xuống 0,00962448 so với mean=0,01744161; margin=+0,00310751. i489 margin âm. Đây là hệ quả trực tiếp của quy tắc hai phía. Gọi mọi báo động là “latency tăng” sẽ sai. Ngược lại, giảm latency chưa chứng minh bình thường hoặc false alarm: tải/coverage/phép đo có thể thay đổi. Nguồn: cùng file `#/rows/108/same_column_values/0`.

**Lịch sử có vai trò tính toán riêng:** dev-3def, travel2 latency có đúng cùng x=0,018946784922394676 tại i100 và i106. Mean/std đổi từ 0,01927899/0,00010569 sang 0,01926018/0,00012838; margin đổi +0,00001512→−0,00007175. Vì x giữ nguyên, gói mean/std lịch sử giải thích quyết định khác ở cặp này. Chưa tách riêng mean khỏi std; không suy nền i106 sạch. Nguồn: cùng file `#/rows/36/same_column_values/0`.

**Số quan sát khác độ dài thời gian:** dev-143 preserve latency báo tại i107 với count75; điểm không báo i106 có count74. Current x hữu hạn giảm từ 1,75 xuống 1,28978579, margin chuyển âm→dương. Những đoạn thiếu trước đó làm count khác index; chưa đủ quy positive alarm cho thiếu dữ liệu. Nguồn: cùng file `#/rows/8/same_column_values/0`.

**Std0 là một đường OR có thật, chưa là nguyên nhân độc quyền:** dev-3def bộ rộng có admin-route socket i100: x4, mean3, std0, threshold0, margin1, True. Cùng cột tại i570 không báo. Nhưng first i100 có 12 cột bật, gồm các cột std hữu hạn. Loại riêng socket std0 không loại được báo đầu gộp này. Nguồn: cùng file `#/rows/38/same_column_values/9`; `chuoi-bang-chung.json#/units/69/points/0`. Bộ hẹp không có cột std0 kích hoạt tại first trong các ca hiện hữu; bộ rộng có ba ca. Nguồn: `stats.json#/detectors/*/first_pre_any_zero_std_trigger`.

**NaN không phải số zero và False không phải bình thường:** dev-12, consign error có count0 và x/mean/std/margin null, native False; UI latency hữu hạn mới bật first. Tại điểm khóa, không có trigger đi cùng thống kê nonfinite. Có 461 cell thống kê nonfinite trong 304 điểm N-Sigma đã khóa; đây là cell, không phải ca hay tỷ lệ nguyên nhân. Nguồn: `supplemental-stats.json#/point_safety`; full gzip dev-12 `#/units/5/points` theo source-catalog. Phép so NaN làm False là hành vi native; nó không xác nhận tín hiệu ổn định và có thể không cung cấp thông tin cho phát hiện.

### Bộ cột rộng và ý nghĩa cờ N1–N4

Mọi x/count/mean/std/threshold/margin/Z của cột chung hẹp/rộng khớp trên toàn bản ghi, cả mask NaN. Có 17 ca bộ rộng báo đầu sớm hơn và 13 ca bằng nhau. Vì cờ cột chung giữ nguyên và OR có thêm cột, những first sớm hơn phải có trigger từ cột bổ sung. Đây là phân xử tính toán cho các ca đó; chưa phải phép đo false alarm do multiplicity hoặc lợi ích bộ hẹp. Nguồn: `doi-chieu.json#/common_column_all_points_checks`, `stats.json#/wide_vs_narrow`; dev-03 first rộng i100 do các cột CPU/memory/latency90 trong `chuoi-bang-chung.json#/units/6/points/0`, còn first hẹp i125.

N1 so mật độ đầu/đuôi, N2 so tỷ lệ cột first-trigger với k×0,0027, N3 là first trước proxy và phủ định N2 tại cùng mức, N4 tìm std0 của một first-trigger. N1 không xác nhận “lịch sử ngắn làm std nhỏ”; N3 không kiểm tính độc lập giữa các cột. Ví dụ dev-143 có tỷ lệ đoạn `[400,720)` bằng zero nên N1 có thể True dù không chứng minh nguyên nhân ấy. Nguồn định nghĩa: `results/T-029/scripts/nsigma_flags.py`, `features-no-label/nsigma/dev-14372e1209--nsigma.json#/history/400:720/ti_le`; hash ở additional-source-verification. Vì vậy các nhóm N1/N2/N3 được giữ là mô tả; cơ chế tại điểm lấy từ x→margin→OR và các đối chứng đã khóa. Giải thích đuôi dày, nền đổi, lượng hóa, tải và lịch sử cho mật độ toàn nhóm vẫn OPEN.

## 3. BOCPD: predictive density → mass → posterior → MAP → CP

Preprocessing native lấy mask bằng `(df!=df.iloc[0]).any()` trên raw trước fill; rồi ffill/fill0, min–max, ffill/fill0. Full dùng tương lai qua mask/minmax. Prior native phụ thuộc d: dof=d+1, kappa1, mu0 và identity precision. Predictive MultivariateT còn dùng dof−dims+1; không coi thay dof danh nghĩa là can thiệp prior độc lập. Code: `utility.py:64–68`, `_bocpd.py:60–101`, adapter `phat_hien.py:20–40`.

Ở bước i, predictive density từng parent nhân posterior parent trước và 0,98 tạo growth mass; reset mass là tổng density×posterior×0,02. Normalize rồi lấy MAP m. Native update theta **sau** posterior hiện tại để dùng bước sau. Quy tắc CP là `i>=1 and abs(m_i−m_(i−1))>1`. Không chỉ reset về r0 hoặc r1 mới tạo CP. R[0,t]≈0,02 là quan hệ cấu tạo constant hazard khi normalization hợp lệ; không dùng làm anomaly score và không kết luận hazard vô tác dụng. Code `_bocpd.py:204–223`; trung gian nối ở `bocpd-trung-gian/index.json`.

**Dev-03 E-gần, i683→684:** i683 MAP tiếp tục tới684, không CP. Tại i684, parent424 có density 57523198756,112755 và posterior trước 0,07717670; growth mass nhánh425 là 4350661743,074765, lớn hơn continuation của MAP cũ 543041514,8796632. Normalize cho MAP425=0,62104857; m684→425 làm CP=True. Density lớn nhất riêng lẻ không phải nguyên nhân đủ; mass đã nhân posterior mới quyết cạnh tranh. Nguồn: `chuoi-bang-chung.json#/units/4/points/0`, `/1`.

Theta saved ở đúng CP có dof trước `[29,453,454,713]`→sau `[30,454,455,714]`, kappa `[1,425,426,685]`→`[2,426,427,686]`, với parent `[0,424,425,684]`; mu/scale trước/sau có trong full gzip dev-03 `#/units/4/points/1/theta`. Đây kiểm đường update, không quy update sau i684 thành nguyên nhân posterior tại i684.

**CP khi run length tăng:** dev-165 i721 m7→8 không CP, i722 m8→10 có CP; posterior MAP10=0,57487611, continuation9=0,40512389. Dev-1e6 i734 m381→396 cũng CP. Nguồn: `chuoi-bang-chung.json#/units/25/points/3`, `/4`; `/units/39/points/4`. Bốn first-post full có m tăng; không gộp với bảy CP m tăng trong toàn bộ điểm khóa của mọi nhánh. Hai mẫu số khác nhau: `stats.json#/detectors/bocpd/first_post_mode_increased`; `supplemental-stats.json#/point_safety/BO_CP_mode_increase`.

**Ca S và D0 vẫn có cạnh tranh posterior:** dev-3def i747 tiếp tục, i748 MAP413 thắng và CP; dev-f36 i751 tiếp tục, i752 MAP7 thắng và CP. Dev-143 D0 i251 không CP, i252 MAP221=0,50372071 vượt continuation253=0,47627928 rồi CP. Các chuỗi cùng phép tính xuất hiện ở E, S và D0. Chúng xác định bước tạo CP, chưa giải thích tại sao E sai vật lý còn S đúng vật lý. Nguồn: `chuoi-bang-chung.json#/units/67/points`, `/units/186/points`, `/units/18/points`. D0 chỉ là không có primary flag strict True; có thể gồm phép mô tả null.

### B2/B4 không thay thế cơ chế native

B2 là I1 không có CP trong ±δ quanh first full; không phải giảm tổng CP. B4 dùng median hai cửa sổ và MAD quá khứ trên dữ liệu sau fill, trước minmax; nó còn dùng cửa sổ sau điểm. BOCPD không tiêu thụ B4. B4/w30/k3 False ở cả i683 và684 của dev-03 nhưng CP chỉ bật684; B4 True ở cả i127 và128 của dev-12 nhưng CP chỉ bật128. Đây bác việc dùng B4 như điều kiện cần hoặc đủ cho CP trong các cặp ấy. Nguồn: `results/T-029/features-no-label/bocpd/dev-03d4910932.json#/B4_all_Nv/30/683`, `/684`; dev-12 cùng con trỏ `/127`, `/128`; code `bocpd_features.py`; các chain unit4/11. Các cột riêng/covariance tạo multivariate density còn chưa cô lập.

Matching B4 dùng dev-f36 làm đối chứng ngoài nhóm ở một số nhóm, nhưng first752 đã sau proxy nên B4_t_hat invalid, flags=null. Đây không phải B4 đo được là False. `bao-phu-nhom.json#/groups/4`, `/7`, `/10`, `/11` ghi giới hạn. Giữ đối chứng khóa và câu hỏi, không đổi ca để có âm tính đẹp.

Có 160/664 điểm BOCPD đã khóa không giữ theta. Density, normalizer, posterior và m vẫn có; observer chỉ giữ theta theo anchor/CP/lân cận/vùng cần đọc. Thiếu theta row không có nghĩa native không update. Slot parent−1/None là padding, khác thiếu cả theta. Nguồn: `supplemental-stats.json#/point_safety`; `../checkpoint-handoff-001/artifacts/scripts/bocpd_core.py:67–101`. Phần quy khác biệt cho mu/covariance/prior cụ thể tại điểm không lưu theta giữ OPEN; phép thu bổ sung tối thiểu nằm trong kiem-tiep.

## 4. Phân rã preprocessing: phần đã phân xử và phần chưa

FF/FP/PF/PP giữ cùng raw tiền tố/thời gian. F/P thứ nhất là mask; thứ hai là nguồn min/max. FF là processed full cắt tiền tố; PP khớp I1. Giữ mask/d/prior khi so scale; giữ nguồn scale trên cột chung khi so gói mask/d/prior. M_P⊆M_F được kiểm trước fill. Không sửa epsilon, prior hoặc drop lại cột để làm kết quả đẹp. Vector m, CP thêm/mất, báo đầu, signed contrasts và tương tác đầy đủ trong `phan-ra-tien-xu-ly.json`.

**Scale có tác động trên cùng mask:** cả hai contrast scale khác m/CP ở 30/30 ca. Dev-03 d28 ở cả FF/FP; tại i235 route raw=after_fill=0,00320910384 nhưng X_F=0,00127753, X_P=0,55805435 vì min/max khác. Cả lịch sử processed đổi; FF i235 MAP236=0,98 không CP, FP MAP111=0,95520615 có CP. First FF684, FP235, signed shift449. Không quy effect riêng cho một raw sample hay route channel. Nguồn: `stats.json#/factorial`; `phan-ra-tien-xu-ly.json#/contrast_chains/0`; `/cases/0/contrasts/scale_with_M_F`; chain units0/1.

**Mask/d/prior là gói, có tương tác:** dev-165 d34 ở FF/FP và33 ở PF/PP; UI error bị M_P bỏ. First CP lần lượt239/177/230/170. Scale shift62 với M_F và60 với M_P; bundle shift9 với S_F và7 với S_P. Signed first-CP interaction2 dù signed CP-count interaction0. Đếm tổng CP sẽ bỏ mất tương tác về vị trí. Nguồn: `phan-ra-tien-xu-ly.json#/cases/3`; `supplemental-stats.json#/interaction_rows/3`; chain units21–24. Cả hai bundle contrasts khác m/CP ở13/30 ca; interaction pointwise khác ở13/30. Đây chưa là tác động prior riêng hoặc riêng cột UI error.

**Đối chứng không đổi:** dev-03 FF=PF và FP=PP, exact input/parameter/output checks đạt; dev-59 cũng là bundle không đổi nhưng scale vẫn đổi. Không đổi là đầu ra hợp lệ, không phải đơn vị thiếu thông tin bị loại. Nguồn `phan-ra-tien-xu-ly.json#/cases/0/same_input_checks`, `/cases/13`; `root_interpretation/identical_inputs`.

**Range0 hợp lệ và noCP khác nhau:** mask raw có thể giữ cột do NaN, nhưng fill làm cột hằng; min–max range0 chia ra NaN rồi fill0. Dev-12 có consign error range0 ở cả bốn nhánh, processed hữu hạn; FF=PF và FP=PP trong khi scale vẫn đổi first128→116. Range0 chung không cô lập được nguyên nhân chênh FF/PP. Đối chứng khóa dev-168 không có range0 vẫn có CP/scale effect, còn khác ô/d/coverage. Nguồn `phan-ra-tien-xu-ly.json#/cases/1`, `/cases/4`; `bao-phu-nhom.json#/groups/52`, `/55`, `/58`, `/61`.

Dev-f36 FF không có CP trong tiền tố nhưng FP/PF/PP có. First shift hoặc interaction theo first giữ null khi không định nghĩa; m/CP-set contrast hợp lệ vẫn giữ. Tại PP i122 m122→121, CP=False dù MAP đổi; FP i140 tương tự. Nguồn `/cases/26`; chain units182–185. Không-CP không xác nhận hệ ổn định vật lý.

Full dùng tương lai, PP vẫn nhìn trước trong tiền tố; các hybrid còn dùng thông tin full. Không nhánh nào ở đây là detector online đã chọn. Effect preprocessing đủ làm căn cứ yêu cầu causal preprocessing cho P6; nó chưa chứng minh một scaler mới sẽ cải thiện phát hiện.

## 5. Sau proxy: đường tính đã biết, trễ vật lý chưa biết

Mọi full ca đều có báo sau proxy. N-Sigma hẹp có offset0–54 giây, rộng0; BOCPD2–317. Tỷ lệ điểm báo trước proxy: hẹp0,046774–0,490323; rộng0,925806–1; BOCPD0–0,025035. Đây là khoảng các tỷ lệ theo ca, không tỷ lệ nguyên nhân. Mẫu số từng ca, thời gian đoạn, hữu hạn-statistics denominator và chuỗi True liên tiếp có trong `do-tre-sau-moc.json#/rows`; tổng ở `stats.json#/detectors`.

Ở bộ rộng, first-post nằm trong chuỗi đã bắt đầu trước proxy ở cả30 ca; hẹp có11 ca; BOCPD không có first-post CP thuộc chuỗi bắt đầu trước proxy. Không gọi offset0 của chuỗi đang tiếp diễn là “vừa phát hiện sự cố”. BOCPD không tự gộp CP rời thành episode.

Freeze mean/std tại `[:i_proxy]` giữ k/fill/ddof và chỉ áp sau proxy. First-post gộp fixed/native bằng nhau30/30 ở mỗi bộ cột. Vì vậy phép này không hỗ trợ lời giải thích hẹp rằng cập nhật sau proxy làm first-post native muộn hơn frozen ở các ca hiện hữu. Nó không bác mọi tác động lịch sử: tập cờ hậu proxy khác ở30/30 hẹp và18/30 rộng. Dev-03 hẹp fixed thêm330/bớt0 điểm gộp; nguồn `nsigma-nguong-co-dinh.json#/rows/0/summary/merged_flag_points`. Không suy fixed tốt hơn từ số báo nhiều hơn.

Full gzip còn lưu các cột nativeFalse/fixedTrue ở cuối file; reduced chỉ giữ cột native nên không đủ đọc mọi tác động freeze. Phải dùng `fixed_baseline` và `fixed_arrays` trên full point theo `nsigma-trung-gian/index.json`. Freeze sử dụng proxy của phân tích; không đưa “đóng băng tại720” vào phương pháp tự phát hiện.

BOCPD có toàn bộ trạng thái proxy→first-post. Dev-03 i723 vẫn continuation, i724 MAP105 thắng → CP, offset4. Dev-f81 i1036 continuation vẫn thắng; i1037 MAP mới đạt0,51929548 so continuation0,45591592 → CP, offset317. Nguồn `chuoi-bang-chung.json#/units/4/points/3`, `/4`; `/units/193/points`. Đây là thời điểm quy tắc vượt cạnh tranh posterior trong bản ghi, không onset thực. Không đủ tách “tín hiệu sự cố xuất hiện muộn” với “mô hình phản ứng muộn” khi thiếu chuẩn onset độc lập.

Bộ chấm dùng proxy→cuối file và báo đầu toàn bản ghi. Có báo sau proxy không đổi việc first toàn file bị chấm E; cũng không xác nhận phát hiện mọi sự cố thật. Code chấm `src/p3/danh_gia.py:260–307` đã pin. Detector engine không nhận nhãn/onset/root; cắt/freeze/chọn điểm và chấm là chẩn đoán có dùng proxy. D về thời lượng kết thúc chỉ là đề xuất kiểm tiếp; không chạy D hoặc đổi nhãn P3.

## 6. Trace/log/tải: dữ kiện và khoảng chưa biết

`tai-log.json` giữ coverage theo ca; `duration-at-locked-points.json` nối đúng second/entity/row NPZ; `workload-at-locked-points.json` giữ raw values và missing/Inf mask. Duration **có** trong context source; projection cũ thiếu không có nghĩa dataset không ghi duration. Đơn vị duration vẫn OPEN_RAW_UNIT. Bin trace theo span start, chưa là span completion hay own-time; distinct traceIDs/root spans chưa xác nhận số external requests. Metric workload chưa có định nghĩa tải độc lập/đơn vị đủ để suy nhân quả.

Trace của dev-03 có duration hữu hạn nhưng statusCode không được ghi ở các rows nguồn; source summary lưu present/missing và alignment riêng. Không dùng count=0 để kết luận không request hoặc không lỗi khi collector coverage chưa biết. `tai-log.json#/cases/0/summary/trace/duration`, `/status_code`, `/alignment`. Dev-3def thiếu kênh log: N/A_MISSING_CHANNEL, không zero log errors. Nguồn `tai-log.json#/cases/9/summary/log`.

Log mẫu first/last ở đúng giây đã khóa không bao trùm mọi message hoặc mọi lỗi. Bản công bố bỏ text, giữ row/container/digest và pointer tới nguồn gốc. Không công bố token/userID. Đồng xuất hiện latency, workload, duration, log chưa là can thiệp độc lập: cùng workload raw không giữ mọi load/sampling/history; không có span ở service/giây đang xét chưa xác nhận service không hoạt động. Chưa quy một tỷ lệ thất bại cho dataset hoặc collector.

Hệ quả đánh giá: chưa xác nhận false alarm vận hành, trễ tính từ onset thật hoặc ý nghĩa error/success từ status thiếu. Đồ thị và collector mới không tái tạo được trường chưa từng ghi. Yêu cầu quan sát FlashTicket có thể rút ra là giữ timestamp nguồn/observed time và clock offset; duration đơn vị rõ; outcome/error semantics; workload generator độc lập; sampling/dropped counters; service/instance/host và correlation/span links. B16-v0.1 §3–8 đã có các yêu cầu liên quan; T-033 chỉ đối chiếu, không sửa chuẩn hoặc nhận đã nghiệm thu runtime. Nguồn read-only: `D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md`.

## 7. Năm đầu ra P4 và căn cứ P6

| Mục P4 | Bằng chứng và mức kết luận | Phần chưa phân xử/ảnh hưởng |
|---|---|---|
| Hạn chế xác nhận, điều kiện | Full preprocessing dùng tương lai; OR có thể tạo first sớm hơn khi thêm cột; CP biểu thị đổi MAP hơn một bước; std0 và NaN có hành vi cụ thể trong native. | Không gọi mọi báo sớm là giả hoặc mọi CP là sự cố. Chưa chọn thay ngưỡng/scaler. |
| Cài đặt/thiếu đầu vào | Khớp source flags/CP/time/sentinel/diagonal và scalar; không phát hiện lỗi cài đặt mới trong các đường đã kiểm. Log một ca thiếu, trace status thiếu, units/coverage semantics còn OPEN. | Không chữa native để đủ bảng; thiếu trường hạn chế đánh giá, không chứng minh nguyên nhân alarm. |
| Giả định/cách tính | History mean/std ảnh hưởng cặp cùng x; scale ảnh hưởng likelihood/posterior trên cùng mask; mask/d/prior và tương tác có effect có điều kiện. | Không cô lập prior/covariance hay nền sạch; BOCPD chung không giải thích riêng E với S. |
| Thông tin quan hệ | Có thể giữ service/path/resource và kênh để xét đồng biến/phụ thuộc thay cho OR chỉ còn bool hoặc density toàn vector. | Chỉ đủ đề xuất; chưa chứng minh cạnh bổ sung thông tin hữu ích, không bảo đảm graph sửa dữ liệu thiếu. |
| Câu chưa trả lời | Onset/negative sạch, load/sampling semantics, per-channel/prior contribution, causal preprocessing và D. | Phép phân xử, input/owner, chi phí và P6 dependency ở kiem-tiep; không loại nhóm khó. |

**Ứng viên, chưa kiểm:** graph có node service/instance, có thể thêm host/resource khi telemetry cho ánh xạ; edge call/message từ span parent/link, và edge chạy-trên từ metadata host. Metric đặt ở node và giữ độ lệch có hướng/cột; log outcome/error đặt ở node rồi nối span bằng trace/correlation hợp lệ; trace latency/status đặt trên edge. Một phép tính ứng viên là residual `r_v(t)=s_v(t)−predict(s_u(t−lag), u thuộc parent(v))`, dùng các cạnh để điều kiện hóa điểm local theo cha; phương án khác là kiểm tính nhất quán của bất thường theo path và evidence của edge, giữ provenance trước gộp. Đây là thiết kế ứng viên cho P6/DT18, chưa được chọn, chưa có tham số hoặc lợi ích dev. Trace log metric không tự độc lập thống kê.

Phương án cần so: local detector có preprocessing causal và provenance tương đương; mô hình multivariate không dùng adjacency; graph dùng quan hệ trace/host đã xác minh. Graph có thể thất bại khi edge sai/thiếu, coverage đổi, đồng cause host, telemetry chậm/không đồng hồ, hoặc quan hệ không bổ sung tín hiệu vượt mô hình không graph. Graph không tự giải quyết onset, range0, missing status hoặc leakage của preprocessing. P6 phải đặc tả cửa sổ causal/tập ứng viên/đầu vào trước chọn trên dev; đối chứng bỏ quan hệ và graph ngẫu nhiên dùng khi đánh giá tác dụng cấu trúc, không trì hoãn phân tích hiện tại.

Phần nên đưa vào tài liệu chính thức sau Minh duyệt: các cơ chế có điều kiện ở mục2–5, sự phân biệt proxy/onset, giới hạn dữ liệu ở mục6 và mức căn cứ ứng viên ở mục7. Không đưa các ứng viên vào WHY như quyết định đã chọn. Phần RQ2 còn mở và phép kiểm không biến mất khi task này được nghiệm thu.
