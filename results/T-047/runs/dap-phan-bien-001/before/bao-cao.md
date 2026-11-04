# T-047 — kết quả Phiên 6

Trạng thái: **hoàn tất phần thực nghiệm/hậu xử lý trong phạm vi được duyệt; chờ Claude phản biện và Minh nghiệm thu**. Ghi 2026-11-02T22:03:53+07:00. Không tự đóng task, khóa G3 hoặc cho phép mở test.

## Kết quả chính và mức căn cứ

Luật chọn đã khóa giữ **E1+E2** tại P, S_lo và S_hi. Mức HẠI chính h=1 giữ nguyên; h=0,5 và 2 đều chạy lại đủ cặp/bộ chọn và vẫn chọn cùng cấu hình. Không có cờ mặc định phải trình thêm tại lựa chọn chính. Đây là kết cục trên dev, không phải quyết định mới của Minh hoặc xác nhận cơ chế/hiệu quả RCA.

| Cấu hình | MRR dev gộp | RE2-TT | Nezha-OB | N1 trung bình cửa sổ giả |
|---|---|---|---|---|
| R0 | 0.681309 | 0.765000 | 0.567186 | 169/10 |
| E1+E2 | 0.799359 | 0.822222 | 0.768182 | 499/30 |
| E1+E2+E3+E5 | 0.674047 | 0.620014 | 0.747727 | 617/30 |

Nguồn: `khoi-k.json#/chon_khoi`, `#/cau_hinh`, `#/do_nhay_muc_HAI`, `#/mac_dinh_ap`. Có 30 ca RE2-TT và22 Nezha-OB; dữ liệu dev được dùng nhiều lần, số này lạc quan và không độc lập với thiết kế. N1 của cấu hình chọn là 499/30 thực thể/cửa sổ; V0 vẫn CAUSE_FOUND ở30/30 cửa sổ giả của cấu hình này. Vế HẠI tương đối không hiệu chuẩn số cảnh báo tuyệt đối và không chứng minh phương pháp đã phân biệt sự cố với biến động nền.

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

Còn một mẫu chọn R0, không đạt điều kiện có E1/E2/E5; giữ với mã dừng bước8. 999mẫu có lựa chọn đạt điều kiện; không dùng999 làm mẫu số để làm đẹp tần suất. Không có mẫu C-e chưa kiểm được;109mẫu có cờ trái chiều dataset cần trình theo luật,77mẫu có trái chiều ở cặp liên quan cấu hình thắng. Nguồn `do-ben.json#/loai`, `#/tan_suat_thang`, `#/tan_suat_co`; từng mẫu tại `runs/b6-c1-do-ben-001/samples.jsonl`. Lựa chọn chính còn mong manh theo ô; việc h=0,5/1/2 không đổi cấu hình không xóa giới hạn này. Không đổi h hoặc chọn theo bootstrap.

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

Nguồn `runs/c1-tong-hop-so-001/summary.json#/changed_pairs`; các bước/reasons/RRtheoô đầy đủ ở `khoi-k.json#/cap`. Không đồng nhất đổi kết cục luật với đổi một cơ chế riêng. Cả gói cổng/thang/vếC-e thay cùng lượt.

Đã trích chuỗi đầy đủ từng ca của15cặp cần đọc (các cặp đổi và đảo tại cấu hình thắng), thêm phân tíchE1/E2 theo52ca; không dừng ở gán cờ. Phân tích người làm có ở:

- `runs/c1-method-analysis-e1-e2-001/analysis.md`: E1/E2, ba cặp thêmE1 đổi kết cục, ca hại/lên/đúng, raw trace→mẫu→G0/G3 ở ba đơn vị; mọi trường chung tái lập. Tương tácE1×E3×E5 trên30cửa sổ giả giữ log/metric/coverage/graph, E1 đổi mẫu/lớp thao tác; replayE5 60/60 nhánh khớp. Lớp không lan làm một số kênh giữF_I, tăngN1; có cả cửa sổ giảm/không đổi. Đây là đường tính, không chứng minh kênh ấy thật sự tự sinh.
- `runs/c1-method-analysis-e3-e5-001/analysis.md`: đủ4cặp×52ca, raw log→Drain→cổng298đơn vị ở4ca không lệch; E5 replay156/156ca khớp. E3 có cả ca làm đối thủ vượt root và ca giúp root qua khóa độ lớn. NEW_OP/STOPPED s=1 là nhánh trực tiếp đã khai, không tự là lỗi bỏphi. Severity/nhãnKHONG_LOI của bộ phân lớp không chứng minh hoạt động lành. E5 có ca root bị hạF_I nhưng thứ hạng vẫn cải thiện nhờ đối thủ hạ nhiều hơn; M5 không bao mọi ca tụt hạng.

`co-che-khoi-k.json` trỏ tới diễn giải và các OPEN; bản trích FACT nguyên gốc vẫn ở `runs/b5-c1-co-che-001/co-che-khoi-k.json`. RR/Hit1/M5 từng ca giống giữa ba thế giới trên832bản, không chỉ cùng MRR trung bình; kênh/khóa số có khác (`runs/c1-tong-hop-so-001/world-*.json`). Không mượn tầng/khóaP thay non-P vốn chưa được native lưu riêng.

Phân loại đã kiểm: các raw/API đã tái dựng khớp cài đặt/adapter; không thấy bằng chứng buộc sửa công thức/SPEC/test. Một số giới hạn nằm ở quy tắc/giả định của phương pháp: novelty/mất mẫu, s=1, giả định kênh giải thích theo cạnh và lớp không lan. Coverage không đổi trong cặp không chứng minh không thiếu thu. Không cộng cờ chồng lấn thành tỷ lệ nguyên nhân, không quy mọi ca sai cho dataset, Drain hoặc E5. Cặp R0→nhiều thành phần không phân xử tác động riêng; giữ chuỗi và giới hạn, không ép nguyên nhân duy nhất.

## Đối chiếu nguồn nghiên cứu và phần còn thiếu

DT18-NV2/NV3 và MRP P6 được hỗ trợ ở phần chọn/kiểm thành phần trên dev: nút là dịch vụ/thành phần, log vàmetric gắn nút, span/thao tác và quan hệ cha-con dùng tính mẫu độc quyềnE1; mẫu cạnhE2 được gán cho bên được gọi; E5 dùng cạnh và nhóm vòng để đổiF_I. Cấu hình chọn cóE1/E2 dùng quan hệ trong phép tính, không chỉ vẽ đồ thị. C-d1/C-d3 đều có dùng đồ thị, không là đối chứng bỏ quan hệ.

Task chưa trả lời xong RQ3a–d, chưa đo lợi ích trên dữ liệu không dùng khi thiết kế, chưa xác nhận vùng ảnh hưởng thật hoặc cơ chế vật lý chung. T1/D2/test qua không thay các bằng chứng ấy. Các nghĩa vụ đối chứng tương đương, T4/T4b mới/hiệu chuẩn, chọnverdictP7, hồ sơG3, dữliệuđộc lập vàFlashTicket vẫn theo các task/gói sau; không tự mở hoặc thu hẹp chúng.

OPEN cụ thể: nghĩa vận hành của mẫu log có/mất; quan hệ nhân quả của các kênh giải thích; vai trò thiếu sự kiện/coverage ở nhóm chưa phân xử; chi tiết non-P chưa lưu; G3gần hằng và hiệu chuẩn; độ bền ngoài52ca/dev. Các câu này ảnh hưởng khóa thiết kế/G3 và khả năng chuyển sangFlashTicket. N1 cao và bootstrap phân tán phải đi cùng đề nghị dùng nềnE1+E2; không coi hai agent cùng ý kiến hoặc nghiệm thu task là xác nhận phương pháp.

## Quyền ghi, lịch sử và bàn giao

Giữ mọi lượt lỗi, trước/sauC1 và dùng lại hợp lệ; không đổi ma trận/luật chọn sau nhìn số. Guard Windows được tái lập47/768 do khác dạng tiền tố đường sauresolve, sửa trong adapter results; sau sửa0/768. Hai lỗiT1 lịch sử thiếu giá trị lúc so nên liên hệ cùng cơ chế chỉ là suy luận hồi tố. Một lượt test lỗi11fixture do thiếu thư mục cha đã giữ; sửa cách gọi, không sửa đáp án. Chi tiết ở LOG.

Có vi phạm ghi cache: lệnh test tạo5file ngoài phạm vi tại.pytest_cache. Đã báo Minh, sao lưu/hash, Minh duyệt dọn và5file đã xóa. Ba thư mục rỗng còn do công cụ chặn xóa với lý do“blocked by policy”; không lách chặn. Receipt `runs/c1-cache-vi-pham-001/cleanup.json`. Không ảnh hưởng số liệu, nhưng không gọi phiên là tuân thủ quyền ghi hoàn toàn.

File được sửa theo quyền: results/T-047, nốiLOG, dòngT047STATE; ngoại lệC1/Q233 đúng duyệt và mộtcommit. Giữ các thay đổi có sẵn ởWHY/DECISIONS/SPEC, không sửa chúng theo diễn giải mới. Khôngcommit thêm/push. Chi phí gồm mọi lượt thử/lỗi/chạy lại và toàn bộ thời gian nền; chỉ loại khoảng chờMinh trước duyệtC1 đã lưu. Trần28800giây; thời gian chốt cuối lấy `runs/chot-phien6-001/result.json`, không reset phần đã chạy.

Kiểm cuối/phạm vi/hash: `runs/ket-phien6-kiem-001/kiem-ban-giao.json`, manifest.json sau chốt. Prompt trung tính theo nguyên văn mẫu ở `prompt-claude-phien6.txt`, Minh chuyển thủ công; chưa tự gửi hoặc ghi phản biện thayClaude. Phần output được đề nghị nghiệm thu trong phạm vi mô tả/kiểm đã làm; task và câu hỏi nghiên cứu vẫn doMinh quyết. Bước tiếp: Claude soát độc lập kết quả, sau đóMinh quyết nghiệm thu/sửa hoặc giao task kế tiếp. Không tự khởi độngtask(2).
