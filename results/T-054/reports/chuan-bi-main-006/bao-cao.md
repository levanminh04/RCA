# Chuẩn bị chạy P7 — checkpoint 006

**Chưa sẵn sàng phát main.** Đã chuẩn bị nguồn và danh sách ba máy, chuyển xong TT, kiểm máy và dữ liệu. Kiểm cuối phát hiện **4/34 ca OB bị điều kiện số hàng của bộ đọc hiện tại từ chối trước khi gọi phương pháp**. Dừng báo Minh; chưa chạy RCA, chấm điểm, khóa G3, mở RE3 hoặc commit/push.

## Đã hoàn thành theo ba phần Minh giao

1. **Nguồn và danh sách:** đủ TT60/OB34 theo G1. Có 1.642 vị trí: 1.640 job và 2 dòng C-e thiếu hỗ trợ. Các vế, seed, nguồn, cửa sổ, môi trường và phụ thuộc đã được gắn vào danh sách riêng từng máy. Metadata nhãn evaluator nằm riêng; chưa ghép với đầu ra hay độ đo.
2. **Chuyển TT:** hai EC2 nhận đồng thời, mỗi máy đúng 90 tệp. Hash và byte khớp trước gửi, trong luồng truyền và sau khi đọc lại đĩa đích. Bản gốc laptop được giữ nguyên; không chuyển nhãn, OB hoặc nguồn A lên cloud.
3. **Kiểm trước chạy:** môi trường chính, 103 pin code, đường dẫn, hash nguồn, phân vùng và RAM/đĩa đạt trên cả ba máy. Lệnh `plan`/`status` đã chuẩn bị. Lệnh chạy còn bị `WAIT_G3` chặn. Kiểm timestamp OB sau đó phát hiện điểm chặn nêu dưới; không lấy PASS về máy/hash thay cho readiness toàn tuyến.

Các checkpoint riêng nằm tại `runs/chuan-bi-main-006/checkpoint-01-sources.json`, `checkpoint-01-plans.json`, `checkpoint-02-transfer.json` và **`checkpoint-03-final.json`**. Bản cuối này thay kết luận readiness sơ bộ, giữ nguyên chứng cứ từng bước.

## Bố trí dự kiến

| Máy | Phần việc | Job | C-e thiếu hỗ trợ | TT raw đã chuyển |
|---|---|---:|---:|---:|
| EC2_1 — 13.211.127.97 | 30 TT: M1 và các vế cùng họ 210; TORAI B 90; C-d3 30; C-e 28 | 358 | 2 | 654.702.162 byte / 90 tệp |
| EC2_2 — 3.107.156.186 | 30 TT còn lại: cùng họ M1 210; B 90; C-d3 30; C-e 30 | 360 | 0 | 654.685.920 byte / 90 tệp |
| Laptop | OB 442; năm baseline TT 300; TORAI A phụ 180 | 922 | 0 | Giữ bản gốc |

Trong 442 job OB có 68 dòng UNSUPPORTED theo giao thức hiện hành. Số lượt phương pháp được hỗ trợ tối đa là 1.572; không coi mọi job đều là một lượt học. C-c/C-g/C-d1/2 là dẫn xuất từ kết quả đã khai, không thêm lượt baseline để tạo chúng.

EC2 nhận TT nặng theo chỉ đạo ưu tiên thời gian của Minh. Laptop giữ OB để dùng các tệp ngày và adapter đã có, cùng các baseline phù hợp môi trường Windows. Mỗi máy tối đa hai worker khi RAM cho phép, mỗi phương pháp một luồng số học, một slot cho mỗi nhóm phương pháp × dataset cùng lúc. Hai EC2 và lô laptop độc lập chạy song song; prep phải xong trước TORAI, M1 phải niêm phong trước C-d3. Không thêm cache liên vế hoặc queue phân tán.

Danh sách mã mờ và cơ cấu từng máy: `bo-tri-du-kien.json`. Từng job cụ thể: `prepared/ec2_1-plan.json`, `ec2_2-plan.json`, `local-plan.json`. Các plan này vẫn là ứng viên bị giữ chặn, không phải giấy phép chạy.

## Dữ liệu và nguồn đã đối chiếu

- **TT:** 180 parquet, **1.309.388.082 byte**. Từng tên ca/tệp, SHA256 và byte đúng nguồn HF revision đã pin. Mốc inject_time của đủ 60 ca lấy từ archive tác giả sẵn có và khớp Git blob inject_time.txt trên HF. Không tải lại dữ liệu.
- **TORAI A:** thư mục cũ chỉ có dev. Đã lấy đúng ba CSV của mỗi ca test từ `torai-data.zip` đã lưu, xác minh SHA256 của archive theo biên nhận cũ. Tổng **180 CSV, 9.244.910 byte**, giải nén vào vùng private mới; không ghi đè thư mục dev và không chuyển A lên cloud.
- **OB:** 34 ca đúng G1 và fault_list native đã pin. Giữ mốc chính inject_time. Mỗi ca dùng 11 nguồn metric và ba minute-file trace + ba log như baseline Q85/T026; không tự mở rộng thành 11 minute-file theo cửa sổ. Có **226 tệp khác nhau, 1.598.103.311 byte**, byte và Git blob khớp nguồn Nezha đã pin.
- **C-e:** 58 ca đủ hỗ trợ, hai ca thiếu. Chứng cứ là timestamp, cận nguồn và A0 theo định nghĩa đang dùng; không phải bằng chứng nền khỏe. Hai ca thiếu giữ dòng hỗ trợ gắn source hash, không tự gán điểm 0 hoặc bỏ khỏi mẫu số khai. Kiểm lại cách đổi timestamp log bằng đúng `int(timestamp*NS)` cho 60 ca không làm đổi F/H, số ô hoặc phân loại.

Nguồn runtime, bản đồ nguồn và nhãn evaluator được quản lý trong `D:/RCA-ext/private/T-054/prepare-main-006/`; pin đầy đủ tại `private-artifact-pins.json`. Packet cloud chỉ mang metadata TT cần thiết, không mang nhãn evaluator hay bản đồ OB/A.

## Điểm chặn OB đã xác nhận

Bộ đọc `src/p3/nezha.py::_doc_cua_so` bắt buộc mỗi nguồn metric có đúng 10 hàng và đúng năm hàng trước mốc t. Kiểm riêng cột Time của 11 nguồn × 34 ca cho thấy **30/374 cặp ca–nguồn vi phạm**, thuộc bốn ca:

| Mã mờ | Quan sát |
|---|---|
| test-3218391218 | 11 nguồn có 3 N / 5 A |
| test-3a1afd6d4f | 11 nguồn có 2 N / 5 A |
| test-9712e01207 | Năm nguồn có 6 N / 5 A hoặc 5 N / 6 A |
| test-a8cc0373da | Ba nguồn có 5 N / 6 A |

Hai ca đầu chỉ có timestamp nguồn bắt đầu muộn hơn t−300; chưa xác định vì sao thiếu phần trước đó. Hai ca sau có hàng sát biên và cadence dao động. Đây là quan sát timestamp và mâu thuẫn với điều kiện bộ đọc, chưa phải kết quả hoặc lỗi của phương pháp RCA. Chạy nguyên bản sẽ bị từ chối trước phương pháp.

**Chưa sửa src, nới điều kiện, dịch mốc, bù/cắt dữ liệu, bỏ ca hoặc gán ERROR/TIMEOUT/0.** Giữ toàn bộ 34 ca và dữ liệu gốc. Cần phân xử hợp đồng đọc và trình sửa tối thiểu trước G3, với ảnh hưởng tới đầu vào các vế và tính so sánh được nêu rõ. Không chọn cách sửa theo điểm test hoặc chạy pilot test để thử cách có lợi.

Chứng cứ: `OB-metric-time-window-check.json`, bản timestamp riêng đã pin và `OB-source-blocker.json`. `source-bundle-final-prepared.json` giữ `open_before_run`; helper kích hoạt từ chối nguồn chưa giải quyết trước khi tạo bản khóa. Đây là áp dụng điểm dừng khi nguồn/adapter chưa hợp lệ, không thêm một cổng khoa học mới.

## Hạn chế riêng của A phụ

Audit timestamp 180 CSV cho thấy 59 ca có ít nhất 20 hàng mỗi phía ở cả ba bảng. Ca `test-541642b59e` có `logts` **N=0, A=41**; hai bảng trace vẫn đủ hai phía.

Code `cat_20` sẽ giữ phần N rỗng. Nhánh xếp hạng log bỏ qua mảng N rỗng; nhánh RCD, nếu được gọi, ghép theo số hàng nhỏ nhất và có thể còn 0 hàng N. Chưa chạy nên **chưa kết luận phương pháp A sẽ lỗi**. Đề nghị giữ nguồn, t và ba seed nguyên bản, khai hạn chế trước G3 và áp quy tắc lỗi đã có; không tự bỏ A, thay nguồn, bù hàng hoặc dịch mốc. Đây là hạn chế đầu vào cụ thể, không tự biến thành cổng mới hay kết luận dataset nói chung.

Chứng cứ: `source-temporal-final-check.json`, `A-input-limitation.json` và bản timestamp private đã pin.

## Máy, tiếp nhận và lệnh

Hai luồng chuyển TT lần lượt mất khoảng 108,80 và 109,36 giây sau kiểm nguồn đầu gửi; chạy đồng thời nên không cộng thành giờ trôi. Đích mỗi host là `.../ec2_1/main-005/data-root` và `.../ec2_2/main-005/data-root`; tên main-005 là vùng đã khai, **chưa có queue main**. Code nằm ở `.../code`, mỗi host có tiền tố riêng. Packet 128 tệp mỗi máy được hash trước dùng. Dùng lại môi trường T025, không dựng lại.

Sau staging, đĩa trống EC2_1 khoảng 8,816 GB, EC2_2 khoảng 13,884 GB; laptop khoảng 16,791 GB lúc kiểm. RAM khả dụng khoảng 7,40 / 7,37 / 3,26 GB. Ước lượng reserve cho phép hai slot tại thời điểm kiểm, không bảo đảm peak mọi ca; driver vẫn xét RAM động. Chưa có upper bound output/temp toàn cohort, phải theo dõi đĩa và DRAIN khi thiếu.

Laptop cắm điện, pin 100%, nhưng vẫn tự ngủ sau **45 phút** khi dùng AC. Chưa đổi cấu hình nguồn điện. Khi main được phép, cần giữ máy thức; không mặc định laptop sẽ hoạt động suốt đêm.

`commands-prepared.json` có lệnh kiểm cụ thể. `activate_prepared.py` chỉ đóng metadata sau quyết định G3/main riêng và sau khi xử lý điểm chặn nguồn; không phát phương pháp. Khi được phép mới tạo binding runtime v3 thật, policy khóa và plan/authority cuối, chuyển metadata khóa đến từng code_root và kiểm pin. Receipt PREPARATION hiện tại không thay được binding G3. Không dùng quyền chuẩn bị để tạo giấy phép main.

Cơ chế nhận giữ nguyên đã kiểm: nhận vào vùng mới, kiểm manifest/hash, giữ receipt/envelope/path gốc; ánh xạ mỗi remote prefix về bản nhận, kiểm union đủ và không trùng trước nhãn. Không xóa nguồn hoặc bản remote khi chưa được duyệt. Hai EC2 và laptop không có worker T054 đang chạy khi kết thúc.

## Checkpoint và bước tiếp theo

Đã giữ G2, pilot hợp lệ và các lượt hỏng. Không chạy lại baseline hoặc RCA trong lượt này. Code khoa học, worker và cấu hình giữ nguyên **103 pin**; chỉ thêm công cụ chuẩn bị, cập nhật hồ sơ vận hành, nối LOG và đúng dòng STATE.

Các lỗi thao tác chuẩn bị được giữ và giải thích: tên datetime bị import che, giả định ban đầu về minute-file OB không đúng giao thức và phép so tuple/list chưa chuẩn hóa. Không dùng các lỗi này làm kết quả phương pháp. Sau khi nguồn TT/A đã dựng hợp lệ, dùng lại chúng khi tiếp nhận, không giải nén hoặc chạy phương pháp lại để sửa phần OB.

**Dừng báo Minh.** Bước cần trình tiếp là phân xử/sửa tối thiểu bộ đọc–hợp đồng OB, sau đó xét G3 và quyền chạy. Không tự sửa src trong gói hiện tại. Hạn chế A phải được khai; RE3 schema/adapter và quyền cuối vẫn riêng, chưa thực hiện trong lượt này. Chuẩn bị chưa trả lời RQ3 hoặc chứng minh hiệu quả/cơ chế.

Không suy ETA main từ tốc độ hash/chuyển. Kịch bản 5–9 giờ trước đây vẫn có điều kiện, chưa là cam kết hoặc ETA toàn task. Không đặt trần cộng dồn và không giảm ca/seed để vừa giờ.
