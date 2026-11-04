# T-047 — kết quả Phiên 6

Trạng thái: **đã bổ sung F9/F10 theo duyệt Minh; chờ Minh quyết các điểm còn mở; chưa đề nghị nghiệm thu hoặc dùng làm nền task (2)**. Claude đã kiểm bản Phiên7, không còn lỗi chặn trong bản ấy; phần bổ sung Phiên8 chưa được kiểm độc lập. Bản Phiên6 giữ tại `runs/dap-phan-bien-001/before/bao-cao.md`, bản trước bổ sung này tại `runs/bo-sung-f9-f10-001/before/bao-cao.md`. Không tự đóng task, khóa G3 hoặc cho phép mở test.

## Kết quả chính và mức căn cứ

Luật chọn đã khóa trả về **E1+E2** tại P, S_lo và S_hi. Mức HẠI chính h=1 giữ nguyên; h=0,5 và 2 cũng trả về cùng cấu hình. **Bước 8 trình Minh về E5 trái chiều theo dataset.** `khoi-k.json#/buoc8/P/trinh_Minh` chứa E5, trong khi `#/mac_dinh_ap` rỗng do helper báo mặc định bỏ sót nhánh này; không được đọc trường rỗng thành không còn cờ. Đây là kết quả bộ chọn trên dev, chưa là quyết định dùng nền task (2) của Minh.

Tại cấu hình thắng, thêm E1 trên nền E2 và thêm E2 trên nền E1 đều GIÚP; thêm E3 HẠI; thêm E5 TRÁI CHIỀU theo dataset. Gói sửa văn bản không sửa helper hoặc bổ sung luật mặc định. E5 và cách xử lý nhánh trái chiều bước 8 còn chờ Minh trước khi chuyển nền. Nguồn: `khoi-k.json#/cap`, `#/buoc8`, và `runs/dap-phan-bien-001/ket-qua.json#/f6`; chi tiết lỗi helper ở `dinh-chinh-cai-dat.md`.

| Cấu hình | MRR dev gộp | RE2-TT | Nezha-OB | N1 trung bình cửa sổ giả |
|---|---|---|---|---|
| R0 | 0.681309 | 0.765000 | 0.567186 | 169/10 |
| E1+E2 | 0.799359 | 0.822222 | 0.768182 | 499/30 |
| E1+E2+E3+E5 | 0.674047 | 0.620014 | 0.747727 | 617/30 |

Nguồn: `khoi-k.json#/chon_khoi`, `#/cau_hinh`, `#/do_nhay_muc_HAI`, `#/mac_dinh_ap`. Có 30 ca RE2-TT và22 Nezha-OB; dữ liệu dev được dùng nhiều lần, số này lạc quan và không độc lập với thiết kế. N1 của cấu hình chọn là 499/30 thực thể/cửa sổ; V0 vẫn CAUSE_FOUND ở30/30 cửa sổ giả của cấu hình này. Vế HẠI tương đối không hiệu chuẩn số cảnh báo tuyệt đối và không chứng minh phương pháp đã phân biệt sự cố với biến động nền.

## Câu hỏi nguồn và số liệu bổ sung cho E5

Các câu Q1/Q3/Q6/Q8 lấy trực tiếp từ SPEC T-043; kết cục dưới đây áp tại cấu hình khối được chọn trên 52 ca dev, chưa là xác nhận cơ chế hoặc kết quả chuỗi cuối.

| Câu hỏi | Phép đối chiếu trong khối | Kết cục và phần chưa trả lời |
|---|---|---|
| Q1: thời gian độc quyền có đưa root lên khi bên gọi chờ root? | E2 → E1+E2 | GIÚP theo luật C. Hỗ trợ giữ E1-U trong bối cảnh này; chưa chứng minh đường chờ vật lý cho mọi ca hoặc xử lý được thiếu span con. |
| Q3: gán khoảng ngoài span cho bên được gọi có giúp? | E1 → E1+E2 | GIÚP. Trên RE2-TT MRR giữ nguyên; cải thiện gộp đến từ Nezha-OB. Chưa khẳng định E2 giúp ở mọi dataset, hoặc đã định danh nguyên nhân trên một cạnh. |
| Q6: tín hiệu hai chiều và log theo mẫu có giúp return/exception mà không hỏng ca đúng? | E1+E2 → E1+E2+E3 | HẠI, có UV-6. Không đạt yêu cầu trong bối cảnh đã kiểm; không suy mọi cách dùng log/tín hiệu hai chiều đều hại. |
| Q8: tách tự sinh/kế thừa có giảm bên gọi đứng trên root mà không gây hại? | E1+E2 → E1+E2+E5 | TRÁI CHIỀU theo dataset. M5 giảm 8 còn 4 ca nhưng có sáu ca tụt RR; chưa đạt kết luận giúp đồng đều hoặc xác nhận cơ chế lan. E5 còn chờ Minh. |

Nguồn: `khoi-k.json#/cap`; phép tổng hợp và con trỏ từng cặp tại `runs/bo-sung-f9-f10-001/ket-qua.json#/questions`. GIÚP/HẠI là kết cục luật đã khóa, không phải khẳng định nhân quả độc lập. Các phân tích trung gian và điều kiện thất bại giữ ở các mục sau.

| Cấu hình | Phạm vi | MRR | Hit@1 | Hit@3 | Hit@5 | NDCG@5 | Rerank@1, K=5 |
|---|---|---|---|---|---|---|---|
| E1+E2 | Gộp | 0,7994 | 0,6538 | 0,9231 | 1,0000 | 0,8501 | 0,6538 |
| E1+E2 | RE2-TT | 0,8222 | 0,7000 | 0,9333 | 1,0000 | 0,8672 | 0,7000 |
| E1+E2 | Nezha-OB | 0,7682 | 0,5909 | 0,9091 | 1,0000 | 0,8268 | 0,5909 |
| E2+E5 | Gộp | 0,7863 | 0,6731 | 0,8846 | 0,9038 | 0,8089 | 0,7447 |
| E2+E5 | RE2-TT | 0,7229 | 0,6000 | 0,8333 | 0,8333 | 0,7385 | 0,7200 |
| E2+E5 | Nezha-OB | 0,8727 | 0,7727 | 0,9545 | 1,0000 | 0,9050 | 0,7727 |
| E1+E2+E5 | Gộp | 0,7848 | 0,6731 | 0,8846 | 0,9038 | 0,8064 | 0,7447 |
| E1+E2+E5 | RE2-TT | 0,7203 | 0,6000 | 0,8333 | 0,8333 | 0,7341 | 0,7200 |
| E1+E2+E5 | Nezha-OB | 0,8727 | 0,7727 | 0,9545 | 1,0000 | 0,9050 | 0,7727 |

Retrieval@5 theo giao thức chấm bằng Hit@5 trong bảng. Rerank@1 là tỷ lệ tổng Hit@1 trên tổng Hit@5, không phải trung bình tỷ lệ riêng từng ca. E1+E2 có root trong top5 ở 52/52 ca; E2+E5 và E1+E2+E5 ở 47/52. Hai cấu hình có E5 hơn Hit@1 gộp một ca ròng và Rerank có điều kiện; E1+E2 hơn MRR, Hit@3, Hit@5 và NDCG@5. Không dùng riêng một chỉ số hoặc mẫu số đã chọn lọc để kết luận E5 tốt hơn/kém hơn nói chung. Mọi số vẫn là dev đã dùng chọn thiết kế, có nguy cơ lạc quan.

Thêm E5 vào E1+E2 làm MRR gộp giảm khoảng 0,0146; RE2-TT giảm 0,1019, Nezha-OB tăng 0,1045. Sáu ca tụt, chín ca lên và 37 ca giữ RR. Sáu ca tụt gồm:

| Ca | Ô | RR trước E5 | RR sau E5 |
|---|---|---|---|
| dev-20acb4402d | RE2-TT, ts-order-service loss | 1 | 1/6 |
| dev-f36d0647d5 | RE2-TT, ts-order-service loss | 1 | 1/11 |
| dev-7f1b6b071d | RE2-TT, ts-travel-service loss | 1 | 1/8 |
| dev-a5cabe5fa7 | RE2-TT, ts-travel-service loss | 1 | 1/12 |
| dev-a915aa2424 | RE2-TT, ts-travel-service loss | 1/2 | 1/7 |
| dev-5ada15752d | Nezha-OB, frontend return | 1 | 1/2 |

Chín ca lên là dev-27252dca60, dev-3b92690644, dev-5467884de4, dev-55f99f3e0a, dev-8ecd9880ed, dev-98bc73c499, dev-a505ab3f65, dev-b0f8b2e3ac và dev-fbc45b0c67. Dataset, ô và RR trước/sau của toàn bộ 52 ca nằm tại `runs/bo-sung-f9-f10-001/ket-qua.json#/e5_changes`. Đây là đối chiếu thêm E5 trên cùng nền E1+E2; không tráo với phép so E2+E5 hay phép giả định thay RR một ca.

Bootstrap cho tần suất được bật: E1 527/1000, E2 954/1000, E3 0/1000, E5 439/1000. Các thành phần cùng có thể bật, nên không cộng thành số mẫu hoặc dùng như xác suất thành phần thật sự có lợi. Nguồn: `runs/bo-sung-f9-f10-001/ket-qua.json#/component_frequency`, tính từ từng lựa chọn ở `runs/b6-c1-do-ben-001/samples.jsonl`. Bảng độ đo đủ 16 cấu hình, từng dataset và gộp tại `ket-qua.json#/metrics` trong lượt bổ sung; lấy từ `khoi-k/kq.json#/cau_hinh/K-<cấu hình>/ca/<ca>/theo_the_gioi/P/do`, kiểm MRR/Hit@1 với trường chấm chính. Số Fraction giữ nguyên trong JSON; bảng chỉ làm tròn để đọc. Các độ đo báo kèm không thay luật chọn MRR.

## Kiểm nguồn, cài đặt và lượt chạy

- Đã tự rà SPEC từ nguồn DT18-NV2/NV3, hướng dẫn cô, MRP P6/P7, WHY/DECISIONS/LESSONS và code/đầu ra gốc trước khi dùng nhận xét cũ. SPEC là quyền thực hiện, không là chứng nhận phương pháp đúng. Điểm chặn C1 đã được điều tra bằng raw và Minh duyệt đúng patch; không có mâu thuẫn mới buộc đổi thiết kế trong phần đã kiểm.
- C1 chỉ đổi hai hàm `o_1s`/`tu_tuong_quan` theo patch đã duyệt: tổng bù và thứ tự tính cố định. Nguồn chạy là revision nền cộng C1, metadata ghi hash code thực. Một commit C1/Q-233 đã có; không commit thêm hoặc push. Receipt ở `runs/c1-ap-dung-001/commit.json`. Không sửa SPEC đã khóa, WHY, luật chọn hoặc tham số.
- Hồi quy sau C1: T-044 374, T-045 16, T-046 46 test qua; T-047 sau sửa guard171 test qua. Nguồn JUnit tại `runs/c1-T-044-001/`, `c1-T-045-001/`, `c1-T-046-001/`, `c1-guard-hoi-quy-002/`. Helper luật C giữ hash đã ghim; test qua chỉ xác nhận phạm vi đã kiểm.
- T1 mới đủ238 lượt:52ca×3seed,52ca xáo,30 cửa sổ giả. Các seed/xáo trùng byte. Native52thật/30giả trước-sau C1 giống hệt;82 tóm tắt R0 với T-046 không lệch. D5 D1 có58đơn vị hợp lệ,0đổi cờ khi thời gian quan sát lệch±1%. Nguồn `t1.json`, `runs/c1-delta-that-001/summary.json`, `runs/c1-delta-ce-001/summary.json`.
- K đủ16×52=832 thật và16×30=480 giả. Không bỏ ca hoặc bản ghi lỗi. R0 khớp T1 và K-đủ khớp phần tóm tắt tương ứng T-046, cả thật/giả; không có lệch ở các đại lượng chung cần miễn hoặc đổi tiêu chí. Không nhận là đã chạy lại toàn bộ A/A của T-046 hoặc có toàn bộ native lịch sử để so mọi trường. Nguồn `runs/b3-k-c1-*/kiem-k-pha1.json`.
- Hai hash K đã ghi LOG trước đọc nhãn, kể cả D2. D2 tái lập12/12 baseline. Chấm đúng52ca dev, không dữ liệu khóa/cloud. QT5 đã rà đủ832/480bản: Kthật108groupdom+2toanhoa; giả98groupdom, không lỗi cài đặt chưa giải thích. Có đơn vị hợp lệ trong ca toàn hòa, không gán thành dữ liệu rỗng. Nguồn `runs/c1-qt5-audit-001/summary-corrected-002.json`, `runs/c1-qt5-ce-audit-001/summary.json`, `tai-lap-baseline.json`.

## Luật C, lựa chọn và độ bền

Đủ43cặp ở ba thế giới, dùng cùng helper cho pha2/bootstrap/độ nhạy. N1 lấy tạiP trên cùng tập cửa sổ hợp lệ của hai nhánh, Fraction và dấu > chính xác. UV-6, điều kiện E5 và M+M′ được giữ; `khong_moc_gia` và kết hợp thế giới tính lại. Không áp trần tỷ lệ V0 vào số đếm N1. Kiểm trực tiếp lại43 chênh từ tầng, trung bình từng ô bảng2×2 và bảo toàn mẫu đạt: `runs/c1-kiem-hau-xu-ly-001/checks.json`.

Bootstrap đủ1000 mẫu, seed 20261102, mức chính1, lấy lại ô ghép cặp và dùng đúng helper. Bội số tất cả ca bằng1 tái lập toàn bộ kết quả chính. Giữ mọi mẫu, không bỏ mẫu không chọn được.

| Cấu hình được chọn trong mẫu hợp lệ | Tần suất trên toàn bộ1000mẫu |
|---|---|
| E1+E2 | 518/1000 |
| E2+E5 | 403/1000 |
| E5 | 36/1000 |
| E2 | 33/1000 |
| E1 | 9/1000 |

Còn một mẫu chọn R0, không đạt điều kiện có E1/E2/E5; giữ với mã dừng bước 8. Có 999 mẫu có lựa chọn đạt điều kiện; mẫu số báo cáo vẫn là 1000. Không có mẫu C-e chưa kiểm được. Số 109 là cờ trái chiều dataset trong lý do trình ở bước chọn; số 77 chỉ đếm cặp có phía bật thêm bằng cấu hình thắng, không bao quát các cặp kiểm ở bước 8.

Đếm trực tiếp `buoc8/P/trinh_Minh` cho thấy **521/1000 mẫu có cờ**, gồm 520 mẫu chọn hợp lệ và một mẫu R0 bị dừng. E5 có cờ ở 426 mẫu, E2 ở 102, E1 ở 25; 489 mẫu có một thành phần, 32 mẫu có hai, nên không cộng các số thành phần thành số mẫu. Nguồn số gốc: `do-ben.json#/loai`, `#/tan_suat_thang`, `#/tan_suat_co` và `runs/b6-c1-do-ben-001/samples.jsonl`; phép tái lập: `runs/dap-phan-bien-001/ket-qua.json#/bootstrap`.

Hai ô loss của ts-order-service và ts-travel-service có ảnh hưởng lớn. Khi tổng bội số lấy lại của hai ô lần lượt là 0, 1, 2, 3 và từ 4 trở lên, số mẫu chọn cấu hình chứa E5 / không chứa E5 / bị dừng lần lượt là 101/0/0; 215/43/0; 107/199/0; 15/200/0; 1/118/1. Đây là quan hệ mô tả trong bootstrap. Hai ô có sáu ca; phép tính giả định chỉ xét năm ca loss tụt hạng được liệt kê ở mục Q8 phía trên, không phải toàn bộ sáu ca của hai ô. Cho riêng từng ca ấy nhận RR của E1+E2 ở cấu hình E2+E5 làm bộ chọn đổi sang E2+E5 ở bốn trong năm ca; ca dev-a915aa2424 vẫn giữ E1+E2. Phép này chỉ thay RR, giữ Hit@1/M5, không là kết quả một biến thể phương pháp. Nguồn: `ket-qua.json#/bootstrap` và `#/rr_gia_dinh` trong lượt đáp trên.

So với T-045, tần suất chọn E1+E2 giảm từ 767 còn 518, E2+E5 tăng từ 190 lên 403 trên 1000 mẫu mỗi lượt. Hai lượt khác seed, cổng, thang và vế cửa sổ giả; không coi chúng là mẫu ghép cặp để quy riêng thay đổi cho một thành phần. Lựa chọn chính còn mong manh theo ô; không đổi h hoặc chọn lại theo bootstrap.

Ba thế giới cho cùng thứ tự ứng viên và RR/Hit@1/M5 trên đủ 832 bản ghi thật. Vế N1 làm đổi 5/43 kết cục cặp tại P nhưng không đổi cấu hình thắng khi bỏ vế này. Cả tám cấu hình có E3 đã bị UV-6 loại; trong nhóm còn lại, chênh N1 lớn nhất là 13/30, dưới cả ba mức đã thử. Vì vậy cùng cấu hình thắng ở ba thế giới và các mức h chỉ là tính bất biến trong phạm vi này, không phải các bằng chứng độc lập về độ bền hoặc hiệu chuẩn. Nguồn: `ket-qua.json#/n1`, `#/world_h` và các bản ghi gốc được chỉ trong đó.

## Bảng2×2 tạiP

| Cấu hình | G0/D0,S0 | G0/D0,S1 | G3/D1,S0 | G3/D1,S1 |
|---|---|---|---|---|
| E1 | 0.695497 | 0.722741 | 0.720558 | 0.725366 |
| E1+E2 | 0.788462 | 0.798077 | 0.794551 | 0.799359 |
| E1+E2+E3 | 0.451534 | 0.527495 | 0.489995 | 0.532303 |
| E1+E2+E3+E5 | 0.663871 | 0.673486 | 0.674047 | 0.674047 |
| E1+E2+E5 | 0.729013 | 0.738628 | 0.775169 | 0.784784 |
| E1+E3 | 0.438728 | 0.508737 | 0.463358 | 0.509832 |
| E1+E3+E5 | 0.600624 | 0.620954 | 0.619393 | 0.613624 |
| E1+E5 | 0.659487 | 0.678718 | 0.715911 | 0.725526 |
| E2 | 0.710920 | 0.753388 | 0.729006 | 0.753846 |
| E2+E3 | 0.453458 | 0.521728 | 0.483266 | 0.525894 |
| E2+E3+E5 | 0.684851 | 0.694008 | 0.687013 | 0.687013 |
| E2+E5 | 0.735013 | 0.744628 | 0.776648 | 0.786263 |
| E3 | 0.428185 | 0.503963 | 0.453068 | 0.505312 |
| E3+E5 | 0.582332 | 0.599045 | 0.648457 | 0.642901 |
| E5 | 0.650981 | 0.670257 | 0.716282 | 0.725898 |
| R0 | 0.638506 | 0.679371 | 0.650059 | 0.681309 |

Nguồn toàn bộ số, từng dataset, từng ca và tương tác: `so-sanh-t045.json#/cau_hinh`. Phục dựng S0 trải thực thể, bỏ độ lớn, sắp/gộp lại; kiểm độc lập bằng tầng/K_I/K_raw trên đủ832bản mới và bằngT4c trên832bản cũ. MRR ôG3/D1,S1 khớp pha2 ở cả16cấu hình. Ở E1+E2, thay thang trên G3/D1 tăng1/208; thay gói cổng khi giữS1 tăng1/780; đó là mô tảdev, không tách G3 khỏiD1. S1 không có lợi đồng đều: trên nềnE3+E5 hoặcE1+E3+E5, nó làm MRRgộp giảm trong gói cổng mới. Không dùng bảng chọn lại thang/cổng/lượt. ChỉP có đủ bốn ô.

## Thay đổi kết cục và cơ chế đã kiểm

Có 12 cặp đổi kết cục so T-045, giống nhau ở ba thế giới:

| Cặp tắt→bật | T-045 → T-047 |
|---|---|
| E1+E2|E1+E2+E5 | HAI → TRAI_CHIEU_DATASET |
| E1|E1+E5 | HAI → TRAI_CHIEU_DATASET |
| E2+E5|E1+E2+E5 | HAI → KHONG_TAC_DUNG |
| E2|E2+E5 | GIUP → TRAI_CHIEU_DATASET |
| E3+E5|E1+E3+E5 | GIUP → HAI |
| E3|E1+E3 | GIUP → KHONG_TAC_DUNG |
| R0|E1+E2+E3+E5 | TRAI_CHIEU_DATASET → HAI |
| R0|E1+E2+E5 | GIUP → TRAI_CHIEU_DATASET |
| R0|E1+E3+E5 | TRAI_CHIEU_DATASET → HAI |
| R0|E2+E3 | TRAI_CHIEU_DATASET → HAI |
| R0|E2+E5 | GIUP → TRAI_CHIEU_DATASET |
| R0|E3+E5 | HAI → TRAI_CHIEU_DATASET |

Nguồn `runs/c1-tong-hop-so-001/summary.json#/changed_pairs`; các bước/reasons/RR theo ô đầy đủ ở `khoi-k.json#/cap`. Bảng bốn ô cho phép phân xử yếu tố đổi kết cục tại P khi giữ các phần khác của phép đánh giá. G3 và D1 vẫn là một gói; không tách tác động riêng của chúng.

| Cặp tắt → bật | Cổng cũ, S0 | Cổng cũ, S1 | Cổng mới, S0 | Cổng mới, S1 | Yếu tố đổi kết cục tại P |
|---|---|---|---|---|---|
| E1+E2 → E1+E2+E5 | HẠI | HẠI | TC | TC | Gói cổng |
| E2+E5 → E1+E2+E5 | HẠI | HẠI | KTD | KTD | Gói cổng |
| E3+E5 → E1+E3+E5 | GIÚP | GIÚP | HẠI | HẠI | Gói cổng |
| R0 → E3+E5 | HẠI | HẠI | TC | TC | Gói cổng |
| E3 → E1+E3 | GIÚP | KTD | GIÚP | KTD | S1 |
| R0 → E1+E2+E5 | GIÚP | TC | GIÚP | TC | S1 |
| R0 → E2+E5 | GIÚP | TC | GIÚP | TC | S1 |
| E1 → E1+E5 | HẠI | TC | TC | TC | Cổng hoặc S1, mỗi thay đổi đều đủ trong bảng |
| E2 → E2+E5 | GIÚP | KTD | GIÚP | TC | Cần cả cổng mới và S1 để thành TC |
| R0 → E1+E2+E3+E5 | TC | TC | TC | TC | Vế N1 đẩy kết cục mới thành HẠI |
| R0 → E1+E3+E5 | TC | TC | TC | TC | Vế N1 đẩy kết cục mới thành HẠI |
| R0 → E2+E3 | TC | TC | TC | TC | Vế N1 đẩy kết cục mới thành HẠI |

TC là trái chiều theo dataset; KTD là không tác dụng. Bảng tính phần điểm/ô trước vế cửa sổ giả. Không cặp nào trong bảng thêm riêng E3; ba cặp thêm riêng E5 đã kiểm M5 đủ bốn ô và không kích hoạt HẠI riêng. Số M5 tắt/bật theo bốn ô: E1 là 12/8, 11/8, 11/7, 12/7; E2 là 17/5, 13/5, 15/4, 13/4; E1+E2 là 8/5, 8/5, 7/4, 8/4. Hai đầu khớp T-045 và kết cục T-047 khi bỏ cửa sổ giả ở 12/12 cặp. Nguồn: `runs/dap-phan-bien-001/ket-qua.json#/bon_o` và `#/m5_bon_o`. Đây là phân xử của luật trên dev tại P, chưa xác nhận cơ chế vật lý hoặc lợi ích trên dữ liệu độc lập.

**Đính chính F6:** hai câu “chỉ vế C-e/mốc giả gây HẠI” ở phân tích E1/E2 dòng 13 và E3/E5 dòng 57 là sai. Cặp E3+E5 → E1+E3+E5 vẫn HẠI khi bỏ N1, do chênh MRR gộp khoảng -0,0293 ở bước 3; E2+E3+E5 → E1+E2+E3+E5 cũng vẫn HẠI. Trường lý do HẠI riêng chỉ ghi điều kiện dừng trước; không chứng minh nguyên nhân duy nhất. Giữ hai file phân tích làm lịch sử; các đường N1 đã lần vẫn giải thích việc N1 kích hoạt, không thay kết luận đã đính chính. Nguồn: `khoi-k.json#/cap`, `runs/dap-phan-bien-001/ket-qua.json#/f6`.

Đã trích chuỗi đầy đủ từng ca của15cặp cần đọc (các cặp đổi và đảo tại cấu hình thắng), thêm phân tíchE1/E2 theo52ca; không dừng ở gán cờ. Phân tích người làm có ở:

- `runs/c1-method-analysis-e1-e2-001/analysis.md`: E1/E2, ba cặp thêmE1 đổi kết cục, ca hại/lên/đúng, raw trace→mẫu→G0/G3 ở ba đơn vị; mọi trường chung tái lập. Tương tácE1×E3×E5 trên30cửa sổ giả giữ log/metric/coverage/graph, E1 đổi mẫu/lớp thao tác; replayE5 60/60 nhánh khớp. Lớp không lan làm một số kênh giữF_I, tăngN1; có cả cửa sổ giảm/không đổi. Đây là đường tính, không chứng minh kênh ấy thật sự tự sinh.
- `runs/c1-method-analysis-e3-e5-001/analysis.md`: đủ4cặp×52ca, raw log→Drain→cổng298đơn vị ở4ca không lệch; E5 replay156/156ca khớp. E3 có cả ca làm đối thủ vượt root và ca giúp root qua khóa độ lớn. NEW_OP/STOPPED s=1 là nhánh trực tiếp đã khai, không tự là lỗi bỏphi. Severity/nhãnKHONG_LOI của bộ phân lớp không chứng minh hoạt động lành. E5 có ca root bị hạF_I nhưng thứ hạng vẫn cải thiện nhờ đối thủ hạ nhiều hơn; M5 không bao mọi ca tụt hạng.

`co-che-khoi-k.json` trỏ tới diễn giải và các OPEN; bản trích FACT nguyên gốc vẫn ở `runs/b5-c1-co-che-001/co-che-khoi-k.json`. RR/Hit1/M5 từng ca giống giữa ba thế giới trên832bản, không chỉ cùng MRR trung bình; kênh/khóa số có khác (`runs/c1-tong-hop-so-001/world-*.json`). Không mượn tầng/khóaP thay non-P vốn chưa được native lưu riêng.

Phân loại đã kiểm: các raw/API đã tái dựng khớp cài đặt/adapter; không thấy bằng chứng buộc sửa công thức/SPEC/test. Một số giới hạn nằm ở quy tắc/giả định của phương pháp: novelty/mất mẫu, s=1, giả định kênh giải thích theo cạnh và lớp không lan. Coverage không đổi trong cặp không chứng minh không thiếu thu. Không cộng cờ chồng lấn thành tỷ lệ nguyên nhân, không quy mọi ca sai cho dataset, Drain hoặc E5. Cặp R0→nhiều thành phần không phân xử tác động riêng; giữ chuỗi và giới hạn, không ép nguyên nhân duy nhất.

## Đối chiếu nguồn nghiên cứu và phần còn thiếu

DT18-NV2/NV3 và MRP P6 được hỗ trợ ở phần chọn/kiểm thành phần trên dev: nút là dịch vụ/thành phần, log và metric gắn nút, span/thao tác và quan hệ cha–con dùng tính mẫu độc quyền E1; mẫu cạnh E2 được gán cho bên được gọi. Ở cấu hình E1+E2 được bộ chọn trả về, quan hệ tham gia tạo bằng chứng E1/E2; E6a sắp theo tầng và khóa, không trực tiếp dùng cạnh. E5 tắt nên K_I=K_raw và tầng2rỗng theo cấu tạo; không chứng minh mọi cờ còn lại thật sự tự sinh. Khi bật, E5 dùng cạnh và nhóm vòng để đổi F_I; E6b mới dùng cạnh trực tiếp trong PageRank. Nguồn code: `src/m1/span.py`, `e2.py`, `e5.py`, `xep_hang.py`. Phân biệt đường dùng quan hệ này với khẳng định đã đáp ứng toàn bộ DT18 hoặc xác nhận lợi ích đồ thị. C-d1/C-d3 đều có dùng đồ thị, không là đối chứng bỏ quan hệ.

Task chưa trả lời xong RQ3a–d, chưa đo lợi ích trên dữ liệu không dùng khi thiết kế, chưa xác nhận vùng ảnh hưởng thật hoặc cơ chế vật lý chung. T1/D2/test qua không thay các bằng chứng ấy. Đối chứng tương đương, chọn verdict P7, hồ sơ G3, dữ liệu độc lập và FlashTicket còn ở các phần việc kế tiếp. Riêng T4/T4b mới chưa được gán task cụ thể; phần bổ sung/chi phí cần trước G3 phải trình Minh, không tự coi đã có task nhận hoặc đã được duyệt chạy.

OPEN cụ thể: nghĩa vận hành của mẫu log có/mất; quan hệ nhân quả của các kênh giải thích; vai trò thiếu sự kiện/coverage ở nhóm chưa phân xử; chi tiết non-P chưa lưu; G3 gần hằng và hiệu chuẩn; độ bền ngoài 52 ca/dev. Các câu này ảnh hưởng khóa thiết kế/G3 và khả năng chuyển sang FlashTicket. **Chưa đề nghị dùng nền E1+E2 cho task (2):** còn cờ E5 trái chiều, trường mặc định thiếu nhánh, N1 cao và bootstrap phân tán. Minh quyết riêng việc dùng nền; đồng thuận phản biện không thay quyết định hoặc xác nhận phương pháp.

Ứng viên E2 tương tác E5 làm đảo chiều giải thích ở nhóm loss **chưa kiểm**. Giả định: bất thường trên cạnh gán cho bên được gọi có thể được E5 dùng để giải thích triệu chứng của root. Trường hợp giả định sai: tổn hại đã xảy ra khi chỉ bật E5, hoặc đến từ nhóm vòng/nhiễu nền thay vì E2. Thực tế bốn trong năm ca loss đã tụt với E5 riêng, một ca không có kênh E2 trong đường giải thích root đã lần; chỉ dev-f36d0647d5 cần E2 để tạo tổn hại đã quan sát. Chưa có bằng chứng chiều mạng/đối chứng phù hợp để phân xử cơ chế; gói sửa chỉ hậu xử lý trung gian đã lưu, không thêm thực nghiệm. Kết luận sửa cơ chế E2/E5 và quyết định E5 phụ thuộc phần này. Đối chiếu cùng ca thấy 1/44 ca–kênh và 6/23 ca–thực thể giải thích trùng cờ cửa sổ giả; mỗi ca chỉ có một cửa sổ giả. Hai tỷ lệ không xác nhận hay loại trừ nhiễu. Nguồn chuỗi và cạnh E2 đi từ root: `runs/dap-phan-bien-001/ket-qua.json#/doi_chieu_moc_gia` và `#/e2_duong_root`.

T4/T4b mới chưa được gán vào task cụ thể trong STATE; Minh cần xếp trước G3. T11 chỉ thay E9 ở nhánh E5, nên E5 tắt làm phần xếp hạng đang xét không nhận tác động đó; ghi không áp dụng hoặc đổi vai trò T11 vẫn cần Minh duyệt. T12 thay cạnh tĩnh: có thể đổi xếp hạng qua E6b nếu được chọn và đổi vùng qua E7; không mặc nhiên kiểm tác dụng E1/E2. Quy tắc chung bước8 phải phân biệt trái chiều dataset và theo ô. Phạm vi T11/T12 và nhánh bước8 còn chờ Minh; gói này không quyết thay.

## Quyền ghi, lịch sử và bàn giao

Giữ mọi lượt lỗi, trước/sauC1 và dùng lại hợp lệ; không đổi ma trận/luật chọn sau nhìn số. Guard Windows được tái lập47/768 do khác dạng tiền tố đường sauresolve, sửa trong adapter results; sau sửa0/768. Hai lỗiT1 lịch sử thiếu giá trị lúc so nên liên hệ cùng cơ chế chỉ là suy luận hồi tố. Một lượt test lỗi11fixture do thiếu thư mục cha đã giữ; sửa cách gọi, không sửa đáp án. Chi tiết ở LOG.

Có vi phạm ghi cache: lệnh test tạo5file ngoài phạm vi tại.pytest_cache. Đã báo Minh, sao lưu/hash, Minh duyệt dọn và5file đã xóa. Ba thư mục rỗng còn do công cụ chặn xóa với lý do“blocked by policy”; không lách chặn. Receipt `runs/c1-cache-vi-pham-001/cleanup.json`. Không ảnh hưởng số liệu, nhưng không gọi phiên là tuân thủ quyền ghi hoàn toàn.

File được sửa theo quyền: results/T-047, nối LOG, dòng T-047 STATE; ngoại lệ C1/Q233 đúng duyệt và một commit. Giữ các thay đổi có sẵn ở WHY/DECISIONS/SPEC. Không commit thêm/push. Chi phí giữ mọi lượt thử/lỗi/chạy lại và thời gian nền của gói chạy; khoảng chờ có mốc được giữ theo receipt. Ngân sách Phiên6 và cận trên Phiên7 tại `runs/dap-phan-bien-001/ket-qua.json#/handoff/budget` được mang nguyên sang; phần mới và tổng cận trên tại `runs/bo-sung-f9-f10-001/ket-qua.json#/handoff/budget`. Trần vẫn 28800 giây, không reset hoặc trừ lại các lượt lỗi.

Kiểm cuối Phiên6 giữ tại `runs/ket-phien6-kiem-001/kiem-ban-giao.json`; kiểm bổ sung và nguồn các số mới tại `runs/dap-phan-bien-001/ket-qua.json`, lệnh tái lập ở script cùng thư mục. Các lượt nhìn số sau báo cáo đã nối vào `so-lan-nhin.jsonl`; hai lượt chat trước được đánh dấu ghi muộn, timestamp nhìn gốc chưa xác minh. Không có thay đổi thiết kế sau nhìn số. Thời gian bổ sung và phần ngân sách mang sang ghi trong kết quả lượt đáp; receipt Phiên6 giữ nguyên.

Tiêu chí 5 và 9 vẫn đạt một phần: bộ chọn đã chạy, cờ đã được báo lại đúng, nhưng quyết định E5 và phần cơ chế chưa phân xử còn mở. Tiêu chí 10 đã bổ sung các lượt đọc muộn và sửa trạng thái diễn giải; không coi ghi muộn là ghi ngay thời điểm cũ. Phiên8 bổ sung độ đo báo kèm, câu hỏi nguồn và giới hạn dùng quan hệ; kiểm ở `runs/bo-sung-f9-f10-001/ket-qua.json`, chưa được kiểm độc lập. Các tiêu chí chạy/đối chiếu khác giữ phạm vi bằng chứng Phiên6. **Chưa đề nghị nghiệm thu task hoặc dùng làm nền task (2).** Đề xuất dừng phản biện; Minh quyết gửi kiểm tiếp, nghiệm thu hoặc xử lý các điểm còn mở. Prompt trung tính ở cuối LOG để Minh chọn chuyển thủ công. Không tự gửi hoặc ghi phản biện thay Claude, không tự khởi động task (2).
