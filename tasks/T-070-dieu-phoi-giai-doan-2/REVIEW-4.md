# Phản biện T-070 — kiểm bản sửa sau dọn repo lab

- **Người phản biện** Codex. **Người làm** Claude. **Ngày** 26/11/2026.
- **Công đoạn** Kiểm lại phản hồi và sửa, lượt 4. Giai đoạn 2, vận hành ngoài G0–G4. Minh cho ghi riêng `REVIEW-4.md`.
- **Đã đọc** AGENTS hai repo, lab `85ace52 → 3ac0d07` và toàn đợt từ tag `truoc-don-2026-11` (`4b6c4b2`), RCA `ee16127` cùng hồ sơ đang sửa. Đọc SPEC, kế hoạch bản 3.1, STATE, checkpoint, LOG và hiện vật theo manifest. Đối chiếu DT18-NV2/NV3, hướng dẫn cô ngày 23/09, MRP P9/P10/RQ5, WHY-08/98–101/110–111, DECISIONS 16–24/11 và LESSONS SL37/QT18.
- **Tự soát độc lập** Lần lại nhánh phát/tiếp nhận tải, điểm ghi G1 bằng root và chuỗi mốc Q4 từ mã, hiện vật và metadata máy trước khi mở bảng phản hồi cũ. Dùng phép giả lập trong bộ nhớ ở nhánh tải. Đối chiếu 3 checkout bằng SSH chỉ đọc.

## Kết luận chung

**Giữ bản triển khai hiện tại. Hai điểm còn chặn theo đúng đường sử dụng.** Bộ chạy chuỗi có thể tính nhầm một container cũ thành lượt mới sau khi lệnh phát đã từ chối tag. Bộ xuất G1 đã khóa đường đi cấp trên nhưng chưa bảo đảm vùng ghi đối với bộ đã tồn tại. Sửa hẹp hai điểm này trước khi phát lịch qua bộ chuỗi và trước khi xác nhận cách ly để bật lại RCA trực tuyến.

Bản sửa giữ phần bảo toàn hiện vật, tín hiệu và hiển thị của P9/P10 đã kiểm ở đợt dọn. Q4 vẫn đạt theo tiêu chí tín hiệu khai trước. T-070 là task điều phối với tiêu chí riêng về W4/W5, W8, W9a và checkpoint. W7 đang hoãn, W9a chưa diễn tập. Hiện vật cũ tại `85ace52` vẫn đủ cho kết luận hồi quy và phát lại dev tương ứng, còn kết luận webhook thật → G1 ở `3ac0d07` cần một lượt tích hợp đã được Minh cấp quyền. Hai điểm còn lại không làm đổi lõi V082, kết quả cũ hay câu hỏi nghiên cứu.

## Các điểm

### R1. Bộ chạy chuỗi vẫn nhận container cũ sau khi chốt từ chối tag — CHẶN phát lịch qua bộ chuỗi

- **Ở đâu** Lab `load/controller/tai_linux.py:225–251`, `load/controller/chuoi_tai.py:139–150,257–304,326–346,360–395`.
- **Sai gì** Chốt mới tìm được dấu vết cũ và từ chối `start` trước đăng nhập hoặc đổi token. Tuy vậy, nhánh nhận lại của `phat()` gọi `get` sau mọi lỗi phát. Hễ có container thì coi đã phát. `cho_xong()` coi container đã thoát là xong mà chưa ràng buộc thời điểm bắt đầu với `sap_phat`. Nhánh tiếp nhận sau gián đoạn cũng đi qua đường chờ này. Nếu tag chỉ còn ở archive, lỗi từ chối mới hiện bị xếp thành “chưa xác minh” dù đã biết lượt chưa phát.
- **Bằng chứng** Trên obs, gọi trực tiếp hàm chỉ đọc `tag_da_dung` cho một tag đang lưu hiện hành, hai tag archive và một tên kiểm mới. Số dấu vết lần lượt **3, 2, 2, 0**. Trên máy tải, `docker inspect` xác nhận container Q4 cũ đã thoát mã 0. Dùng trạng thái chuẩn trong `q4/k6-state.json` với bộ gọi CLI được thay bằng phản hồi giả trong bộ nhớ. `start` trả lỗi từ chối tag, `get` trả trạng thái container cũ. `chay_luot()` trả `xong`, ghi `phat_loi → phat_co_container → xong → kiem_dat` khi giả lập telemetry có dữ liệu. Trường hợp `get` trả lỗi cho tag chỉ còn archive cho `chua_xac_minh`. Không phát tải hay ghi nhật ký thật.
- **Hậu quả** Đây là lỗi phân loại đã tái hiện ở logic bộ chuỗi. Nếu dữ liệu cũ còn đủ, lượt và thời gian quan sát cũ có thể bị chấm theo lịch mới. Khi thiếu dữ liệu, hậu quả có thể chỉ là dừng chuỗi. Q4 dùng tag mới và hoàn thành trước commit sửa; chưa thấy lượt thực nào bị nhận nhầm.
- **Sửa tối thiểu** Xử lý từ chối tag đã dùng trước nhánh tiếp nhận, ghi đúng lý do rồi dừng để người vận hành kiểm lịch. Với nhánh gián đoạn thực sự, chỉ nhận container khi bằng chứng thuộc lần phát đang theo dõi. Chặn trạng thái bắt đầu từ trước mốc `sap_phat`, có tính sai lệch đồng hồ nếu hai mốc sát nhau. Giữ đường nhận lại sau lỗi SSH khi bằng chứng khớp. Có thể xác nhận bằng phép giả lập trên và một trường hợp tiếp nhận đúng, tốn vài phút. Chỉ dựa vào chạy khô hoặc đổi prefix tránh tag đang biết nhưng bỏ sót nhánh tiếp nhận tự động.

### R2. Kiểm vùng ghi G1 chưa bao hết bộ đã có — CHẶN xác nhận cách ly vùng ghi khi bật lại trực tuyến

- **Ở đâu** Lab `rca/online/g1_b.py:29–55,68–82,106–159`, `rca/online/orchestrator.py:73–74,151–154,251–256`, `rca/lib/g1_export.py:46–50`, `rca/batch/sau_v082.py:105–134,197–225`.
- **Sai gì** Đích chuẩn hóa giờ phải là một bộ `online-*` trực tiếp dưới gốc. Bộ điều phối kiểm sớm, và nguồn chép được kiểm cây. Phần đích sẵn có chỉ kiểm liên kết tượng trưng ở gốc bộ và hai mục cấp trên. Các điểm ghi bằng root còn mở tệp và thư mục sâu hơn trong cây. Nếu bộ có chỉ mục, `khoi_tao()` coi là đã có và đi thẳng tới ghi. Điều kiện hiện tại không áp cho các đường sâu thực sự được ghi. Ngoài ra, đường nguồn `chep:` được kiểm bằng đối tượng đường dẫn rồi đối số gốc tiếp tục được ghép vào chuỗi shell. Kiểm đường dẫn và truyền nguyên đối số là hai việc khác nhau.
- **Bằng chứng** Rà tĩnh từ `kiem_dich()` đến thao tác ghi JSON và đồ thị. SSH `stat` cho gốc chung do ubuntu sở hữu, hai bộ hiện có thuộc root 755. `find ... -type l` trên `dev` và `online-dev-001` trả **0**. Bộ nhận T-073 đang tắt. Những dữ kiện này giảm rủi ro ở cây hiện có, nhưng không chứng minh điều kiện cho mọi bộ đang được tiếp nhận. Không thử ghi qua liên kết hay chạy lệnh ngoài phạm vi.
- **Hậu quả** Di chuyển cửa kiểm lên trước làm đúng phần bố trí. Cam kết cách ly đích đã tồn tại vẫn thiếu. Đây là thiếu sót kiểm soát ghi đặc quyền, với điều kiện tác động là cây được dùng có đường dẫn bất thường hoặc do một tài khoản có quyền ghi tạo. Lượt này xác nhận bằng chứng tĩnh và trạng thái hiện thời; chưa có bằng chứng ghi sai hay truy cập từ mạng.
- **Sửa tối thiểu** Dùng bộ riêng với đường kiểm thực hiện ngay ở điểm ghi root. Nếu cần tiếp tục ghi vào bộ đã có, kiểm cả cây đích tại các nhánh sẽ ghi, gồm tệp và thư mục, và chỉ tiếp nhận bộ có quyền sở hữu phù hợp với đường ghi này. Với `chep:`, truyền đường đã chuẩn hóa dưới dạng một đối số thay vì ghép lại từ chuỗi gốc. Dùng riêng bộ mới do tiến trình tạo đơn giản hơn, nhưng làm mất khả năng tiếp nhận cùng bộ sau gián đoạn. Một kiểm tĩnh và phép kiểm cục bộ được duyệt chỉ cần vài phút. Chưa cần mở cổng hay phát lại toàn tuyến để sửa điều kiện đường dẫn.

### R3. Đính chính Q4 vẫn khẳng định quá mức về nguồn mất mẫu — KHÔNG CHẶN Q4 đạt tín hiệu

- **Ở đâu** `results/T-070/don/q4/README.md`, mục “Hai điều thấy ở cảnh báo”, và dòng T-070 ở `docs/STATE.md`.
- **Bằng chứng đã xác nhận** `lenh-1-dung.out` cho khoảng thao tác 16:29:48–16:31:18Z ngày 24/11, gồm dừng cả Collector agent và Gateway. Mốc `startsAt` là 16:32:00Z. `docker inspect` cho Gateway mới bắt đầu 16:38:32Z và log triển khai ghi health/đăng ký đạt 16:39:13Z. `canh-bao-nhan.out` và `k6-state.json#/StartedAt,FinishedAt` cho 5 tin trước Q4, 9 tin trong Q4. Từ lúc k6 bắt đầu đến khi bộ nhận nhận resolved khoảng 22 s.
- **Phần vượt bằng chứng** Đọc đúng biểu thức A của `t072-mat-gw` bằng GET `/api/v1/query` trên obs. Giá trị tuổi mẫu ở 16:29:40Z là **9,479 s**, ở 16:31:50Z là **119,479 s** và 16:32:00Z là **129,479 s**. Cấu hình đặt `gt 60` và `for: 60s`. Mẫu cũ vẫn còn ở mốc phát cảnh báo; chuỗi mẫu đã quá hạn. Sau khi tạo Gateway, phép đọc tại 16:38:40Z và 16:39:50Z rỗng, cũng rỗng ngay trước Q4 lúc 03:21:20Z. Mẫu mới xuất hiện lúc 03:21:45Z với tuổi **9,667 s**. Những điểm này hỗ trợ mạnh giải thích mất mẫu mới trong bảo trì, rồi chưa thấy chuỗi mới đến sát lúc bắt đầu Q4. Chúng chưa tách được phần do Gateway dừng khỏi phần do Collector agent dừng, hoặc chứng minh suốt thời gian sau khởi động không có request vào bốn route. Cùng kiểu kết quả có thể do request hiếm hoặc đường đo chưa phát mẫu. Câu “đều làm luật này cháy” cần điều kiện quá ngưỡng đủ lâu hoặc gặp NoData theo cấu hình.
- **Sửa tối thiểu** Ghi cơ chế hẹp là tuổi mẫu vượt ngưỡng khi dừng hai thành phần, rồi các mốc không thấy chuỗi mới và có lại khi Q4 bắt đầu. Giữ các mốc và Q4 đạt, không quy nguyên nhân duy nhất. Nếu cần phân xử cho W4/W7, có thể so log truy cập theo route với mốc sống của agent trên khoảng đã biết, vài phút nếu log còn. Chưa cần truy vấn đó để sửa câu hoặc công nhận kết quả giao nhận. Cập nhật đúng dòng manifest theo quyền Minh cho, hoặc giữ báo cáo đã băm và đính chính riêng. Không dùng Q4 để suy tỷ lệ báo động giả.

### R4. STATE gộp nhầm mức của phản biện trước — KHÔNG CHẶN dùng bằng chứng đã xác nhận

- **Ở đâu** `docs/STATE.md:13`, đối chiếu tiêu đề R1–R7 ở `REVIEW-3.md` và `TRANG-THAI.json#/buoc_tiep_dieu_phoi`.
- **Sai gì** Dòng mới đã ghi đúng Q4, hiện trạng máy và việc tạm dừng. Cụm “R1–R7, không chặn” lại ghi sai mức của bản gốc: năm điểm R1–R5 chặn các đường sử dụng cụ thể. Câu “R6, R7 xong” chỉ phù hợp ở mức đã chỉnh hồ sơ, trong khi phần quy nguyên nhân còn hở. Điều này khiến người tiếp nhận dễ hiểu rằng có thể phát lại tuyến ngay.
- **Sửa tối thiểu** Giữ trạng thái đợt dọn, tóm tắt điều kiện còn mở theo đường sử dụng và trỏ đến bản kiểm mới sau khi Minh cho cập nhật. Checkpoint đã ghi lịch cũ làm lịch sử, có thể giữ nguyên các mục lịch cũ. Không cần tái cấu trúc cả STATE hay đổi SPEC.

## Đối chiếu các lượt trước

### REVIEW-3 và phản hồi của Claude

| Điểm | Đánh giá bản sửa | Bằng chứng và giới hạn |
|---|---|---|
| R1 | Đúng một phần | Chốt ở `start` và chạy khô dùng cùng phép đọc; lỗi đọc không còn thành “tag chưa dùng”. Nhánh `phat()/cho_xong()` vẫn nhận cũ, như R1 lượt này. |
| R2 | Đúng một phần | Đích chuẩn hóa và cây nguồn được kiểm, điểm gọi kiểm trước khi tạo hồ sơ. Điểm ghi tiếp vào cây đích sâu hơn còn hở, như R2 lượt này. |
| R3 | Đúng trong phạm vi đã sửa | `COMPOSE_CU` bị bỏ, thiếu thư mục hoặc lệch nhãn bị từ chối trước `up`. SSH cho `compose-dir` và nhãn Payment khớp, file đang có, container còn chạy. Nhãn xác nhận đường cấu hình; việc tiêm lại thật chưa chạy và vẫn thuộc quyền phát ô riêng. |
| R4 | Đúng với hai nhãn và các lượt chạy nối tiếp | Tên log có cả nhãn và giây UTC. Cùng nhãn, cùng revision, cùng giây vẫn có thể đụng đường và worktree vẫn dùng chung. Với build nối tiếp như cách sử dụng hiện tại, không còn lỗi ghi đè giữa hai nhãn. Nếu cần chạy đồng thời, cách nhẹ nhất là từ chối thư mục log đã tồn tại và quyết riêng cách dùng worktree; chưa cần làm song song chỉ để kiểm. |
| R5 | Đúng | README về gốc repo và dùng đường tuyệt đối đến đúng file trong Git. Không khởi động bộ nhận hay điều phối để xác nhận lỗi đường tương đối này. |
| R6 | Đúng về trình tự, đúng một phần về nguyên nhân | Mốc, 5/9 và hash khớp. Prometheus xác nhận cơ chế tuổi mẫu ở thời điểm bắt đầu, giới hạn nhân quả ở R3 lượt này. |
| R7 | Đúng về checkpoint, đúng một phần về câu tóm tắt | Q4, revision, trạng thái lịch và tham chiếu STOP đã được cập nhật. Phân loại tổng hợp ở STATE lệch, như R4 lượt này. `HOP-DONG.md` trùng bản commit. |

### REVIEW và REVIEW-2

| Điểm | Kết luận kiểm lại |
|---|---|
| Lượt 1 R1 | **Đúng.** Hiện vật có hash env và metadata chọn lọc. Diff sửa không đụng bộ chụp. |
| Lượt 1 R2 | **Đúng về bộ xuất.** L2 giữ loader/literal và Q6 đã qua ở `85ace52`. Chốt đích mới xem R2 lượt này. |
| Lượt 1 R3 | **Đúng.** Giữ UID ở diff toàn đợt; tái cấu hình dashboard không có trong bảy file sửa. |
| Lượt 1 R4, N2 | **Đúng.** Snapshot sau dời lưu phép từ chối đọc/đi qua thư mục cha của user `rca`. Bản sửa không đụng cấu hình cách ly đó. |
| Lượt 1 R5 | **Đúng về phụ thuộc và mount.** Log bật proxy trước app, nhãn Payment hiện khớp. Môi trường hoàn tác T-067 đã được Minh cho ngừng giữ. Không suy từ nhánh tiêm mới sang hoàn tác. |
| Lượt 1 R6 | **Đúng.** Q4 ghi preflight qua và helper vẫn giữ cách quản lý cũ. Commit sửa không đổi helper. |
| Lượt 1 R7, N1 | **Đúng.** Freeze 18 dòng và Python đối chiếu trong hiện vật đã băm. Q3 dùng đích/cờ từng ca và khớp chuẩn. Hai lỗi của bộ test hợp đồng cũ không dùng làm kết luận. |
| Lượt 1 R8 | **Đúng.** Bộ nhận nhẹ hiện healthy, giữ cấu hình luật/UID từ bản dọn. Q4 xác nhận nhận cả hai trạng thái. |
| Lượt 1 R9 | **Đúng.** Bước 4 giữ `/opt/rca-tai` và các ngoại lệ; kết quả Docker hiện đủ bốn container ngoại lệ. |
| Lượt 1 R10 | **Đúng sau đính chính.** Đếm gốc 34 theo phép lượt 3; checkpoint đã dẫn hai STOP hiện hành; 149 file lock khớp. |
| Lượt 1 N3, N4 | **Đúng.** Lệnh triển khai giữ nhãn toxiproxy cũ. Bản sửa không đổi YAML luật và nguồn lịch sử. |
| Lượt 2 PB1 | **Đúng.** Lệnh hiệu lực và đầu ra bước 3 chứng minh file phủ được ghép với file cơ sở. |
| Lượt 2 PB2 | **Đúng về triển khai chiều đi.** Lệnh dời ghi ba bind Keycloak và đường hoàn tác tại thời điểm được giữ. Tài liệu/LOG ghi Minh đã cho dừng giữ đường lui; không thử lại hoàn tác ở lượt này. |
| Lượt 2 PB3 | **Đúng.** Bộ nhận nhẹ chạy riêng. Lệnh Q3 chuẩn bị cha đích và snapshot đang ở đúng gốc mới. |
| Lượt 2 PB4 | **Đúng.** 102 kết quả so trước xóa nằm trong hiện vật X1. Hiện còn đủ 4 ngoại lệ và container Q4. |
| Lượt 2 PB5 | **Đúng.** Hai bộ điều khiển vẫn lọc `load rca inventory`; checkout sạch. Chốt nhận diện lượt là vấn đề riêng. |
| Lượt 2 PB6 | **Đúng.** Q4 dùng đúng đơn theo JSON và Q6 kiểm từng mục ở dữ liệu cố định. Hai tập bằng chứng vẫn tách biệt. |
| Lượt 2 S3/S4 và ghi chú | **Đúng về venv và đích.** Freeze đã lưu, đích do người vận hành truyền qua `--ra`, còn mặc định `OUT` là nhật ký. Nhận xét về `test -r`, nhãn toxiproxy, thư mục Mongo và đối chiếu YAML giữ phạm vi như lượt 3. |

## Tuân thủ quy trình và mục tiêu nguồn

- LOG ghi Minh duyệt bảy điểm và riêng việc cập nhật README/manifest. Diff lab đúng bảy file, năm Python được đọc cú pháp từ blob, một shell qua `bash -n`. `git diff --check` sạch. LOG tự báo đã thêm ngoài phạm vi một ghi chú HOP-DONG rồi hoàn tác. `git diff --quiet HEAD -- HOP-DONG.md` trên đường đầy đủ trả 0. Đây là lần sửa ngoài quyền đã được báo và không còn chênh hiện tại.
- So byte theo **8 manifest / 143 mục** đều khớp. Q4 **12/12** và diff manifest chỉ đổi một dòng của README. Không thấy manifest khác trong T-070 ghim README hoặc manifest con. Các kết quả số và snapshot máy được dùng qua manifest hoặc commit đúng revision. Nháp W7 ghim commit lab khi khóa; nếu Minh duyệt sửa R1/R2 thì hồ sơ lượt tương lai dùng revision lab mới, không thay vân tay ca đã chạy. R3 chỉ đổi báo cáo và dòng băm tương ứng nếu dùng cùng cách đính chính.
- `git diff -M` toàn đợt từ tag có **102** mục, phần mới là bảy file trong đó. Diff riêng bản sửa không đổi `rca/method.lock`, `run_m1.py`, `stage_b.py` hay `observability/`. Mã `src/m1`, `src/m1_ft`, `src/p3` của RCA vẫn trùng HEAD. Trên obs, **149/149** file bản chụp và hai pin P7 trùng. Phần ngữ nghĩa gom cảnh báo, mốc đưa vào lõi, cửa sổ, xử lý trace/log/metric, tập ứng viên và xếp hạng giữ theo kết luận lượt 3 trên phạm vi diff. Thay đổi G1 ở đường ghi sau khi có xếp hạng. Đồ thị hiển thị vẫn đọc cạnh từ trace theo WHY-100, không tự là phép đo tác dụng của đồ thị trong lõi. Chưa thấy đường mới truyền nhãn tiêm vào phương pháp. Không mở dữ liệu khóa.
- Quyết định dọn và cách ghim qua commit có căn cứ ở dự án; lựa chọn V082 đã được ghi theo bằng chứng dev và giới hạn có sẵn. Bản sửa vận hành không làm phát sinh lựa chọn nghiên cứu mới. Cơ chế tuổi mẫu Q4 được đối chiếu bằng truy vấn hẹp trên telemetry có sẵn, không suy thêm về độ chính xác RQ5 hay độ nhạy cảnh báo. Câu hỏi tuyến sống trên revision sau sửa cần lượt có webhook thật và log từng khâu, dùng phép tích hợp W5/W9a đã có nếu Minh mở lại. Chi phí là một ca và khoảng chờ cửa sổ đã khai.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm.** Soát độc lập diff sửa và diff toàn đợt, kiểm ba máy, đọc lại từng điểm đã phản hồi và đối chiếu với nguồn gốc, hiện vật.
2. **File thay đổi.** Chỉ thêm `tasks/T-070-dieu-phoi-giai-doan-2/REVIEW-4.md`. Không commit.
3. **Kiểm đã chạy.** Ba checkout sạch ở `3ac0d07`; app có 14 container liên quan còn chạy, bộ nhận nhẹ healthy, bộ nhận T-073 tắt. Manifest, bản chụp và cú pháp đạt. Phép giả lập tải xác nhận R1. Truy vấn Prometheus chỉ đọc xác nhận phần cơ chế và giới hạn ở R3. Không khởi động, dừng hay phát tải, không thử ghi đặc quyền.
4. **Minh quyết.** Đề xuất Claude đáp một lượt hẹp và trình sửa R1/R2 trước khi dùng hai đường đó; R3/R4 là cập nhật hồ sơ, có thể cùng trình. Giữ các kết quả Q3/Q4/Q6 và phần đã sửa của R3–R5 lượt trước. Không cần lặp hai ca hồi quy hoặc chạy build mới chỉ để xác nhận thay đổi nhỏ. Phương án tạm giữ nguyên nếu chưa bật trực tuyến và chưa dùng bộ chuỗi đáp ứng vận hành hiện tại, nhưng giữ giới hạn nghiệm thu. Chưa có phản hồi của Claude cho các điểm lượt này. A1/A2/D1 và quyền mở lại W7 vẫn theo quyết định riêng của Minh.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-070, tasks/T-070-dieu-phoi-giai-doan-2/. Kết quả dọn repo lab, sửa theo REVIEW-3 và triển khai ba máy.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: giai đoạn 2, việc vận hành dọn repo và máy, ngoài G0–G4.
- Người làm và người phản biện chính thức: Claude làm, Codex phản biện theo SPEC T-070.
- Tài liệu gốc: Repo lab: git diff 85ace52 3ac0d07 và git diff -M truoc-don-2026-11 3ac0d07. Repo RCA: results/T-070/don/{KE-HOACH-DON.md,truoc/,sau-buoc-2/,sau-buoc-3/,sau-buoc-4-5/,q4/,sau-don/}, docs/STATE.md, tasks/T-070-dieu-phoi-giai-doan-2/{SPEC.md,TRANG-THAI.json,LOG.md} và AGENTS.md của hai repo.
- Phản biện và phản hồi trước: tasks/T-070-dieu-phoi-giai-doan-2/{REVIEW.md,REVIEW-2.md,REVIEW-3.md,REVIEW-4.md}. Kiểm cả các đề xuất và phương án khác được nêu trong bản lượt này.
- Code và kết quả liên quan: Lab D:/Project/flashticket-rca-lab tại 3ac0d07, tag trước dọn tại 4b6c4b2, máy app/obs/tải đặt repo tại /opt/flashticket-rca. RCA tại ee16127 với cập nhật hồ sơ chưa commit, hiện vật theo SHA256SUMS trong don/ và kiem-ke/. Nếu quyền chỉ đọc còn hiệu lực, dùng bash results/T-070/kiem-ke/tho/lenh/ssh.sh app|obs|tai với script qua stdin, sudo chỉ cho lệnh đọc.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat nếu Minh chưa cấp quyền ghi riêng cho lượt đáp. Làm trong phiên này, không dùng subagent.

Không sửa ngoài phạm vi trên, không commit. Chưa có quyền ghi rõ ràng thì chỉ đọc và trả lời trong chat. Giữ các bản lượt cũ. Không đọc dữ liệu khóa hoặc chạy thực nghiệm ngoài quyền được duyệt.

Đọc nguồn và đầu ra gốc trước khi đọc kết luận các lượt phản biện/phản hồi. Lập nhận xét độc lập trước, không lấy tóm tắt trong LOG thay bằng chứng trên file thật.
Nguồn đối chiếu: docs/STATE.md, SPEC và LOG nếu có; phần trực tiếp chi phối trong docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md.
Nguồn đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ và được phép); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.
7. Kiểm cả đạt SPEC và đạt phần mục tiêu nguồn. Nếu chỉ đạt một phần, nêu phần thiếu và quyết định phụ thuộc. Không dùng “chưa kiểm” làm căn cứ đã xác nhận hoặc “ngoài SPEC” để bỏ nghĩa vụ nghiên cứu. Không ép một nguyên nhân vào chỗ chưa biết.
8. Với nhận định quan trọng, hỏi còn nguyên nhân khả thi nào khác giải thích kết quả và bằng chứng có phân xử được không. Trước khi dùng đầu ra cũ, kiểm hash theo manifest phù hợp; lệch thì dừng phần phụ thuộc và báo Minh. Số làm bằng chứng phải có đường dẫn và con trỏ JSON hoặc lệnh đã chạy kèm kết quả.
9. Kiểm tuân thủ quy trình bằng việc thực tế: vai trò, quyền ghi và duyệt phạm vi; nguồn quyết định; tự kiểm; LOG/STATE/bàn giao theo nghĩa vụ của vai trò; tự đổi mục tiêu/tiêu chí/thiết kế; đề nghị chuyển bước khi thiếu căn cứ. Áp dụng luật và quyền có hiệu lực ở thời điểm việc được làm, không tự mở lại task đã đóng. Chỉ báo vi phạm có bằng chứng và ảnh hưởng cụ thể, không chỉ xác nhận đã đọc AGENTS.
10. Sau tự soát, kiểm từng điểm và phản hồi các lượt trước: đúng / đúng một phần / sai / chưa kiểm được, với bằng chứng riêng. Không mặc nhiên đồng ý với bên nào. Nêu phạm vi lỗi rộng/hẹp hơn hoặc mặt trái của đề xuất sửa.
11. Rà cả phần không được nêu trong LOG, báo cáo hay phản biện trước. Với mỗi bước dữ liệu đi qua (đọc → chuyển đổi → tính → chấm), hỏi quy ước của dữ liệu nguồn (giá trị đặc biệt, đơn vị, gốc, alias, rỗng) có được xử lý đúng không. Không coi phần không ai nêu là đã đúng.
12. Một trạng thái xảy ra đồng loạt (100% lỗi, 100% không hỗ trợ, toàn hòa, toàn rỗng) là dấu hiệu cần lần tới đầu vào, không phải kết quả để diễn giải. Không dùng nó làm căn cứ thiết kế trước khi lần.
13. Điểm cuối khớp số công bố, hay "chạy không lỗi", chưa chứng minh thành phần chạy đúng. Kiểm trung gian và phép kiểm không cần nhãn.
14. Câu có "mọi", "đều", "không đổi", "trùng" phải nói rõ đại lượng và có lệnh đếm trên đủ đối tượng.
15. Trước khi đề xuất sửa hoặc ghi vào một file dùng chung (code, script, tài liệu), kiểm file đó có bị ghim trong manifest, plan hoặc vân tay job nào không. Nêu rõ thao tác nào làm đổi hash và ảnh hưởng tới đâu.
16. Kiểm tiêu chí so sánh hoặc chấp nhận được khai trước khi xem kết quả. Đổi tiêu chí sau khi xem phải khai là sửa sau.
17. Với lượt chạy, tách lỗi hạ tầng và điều phối (tiến trình, nguồn điện, kết nối, giới hạn thời gian) khỏi lỗi phương pháp; lỗi hạ tầng không được ghi thành kết quả khoa học.
18. Phản biện một kế hoạch thì kiểm cả đường thực thi thật: code có cho phép làm đúng như kế hoạch nói không (guard, thư mục, trạng thái đã khóa). Không chỉ kiểm lập luận trên giấy.
19. Mỗi phần ghi "chưa xác định", "chưa phân xử", "chưa biết" hoặc OPEN phải kèm giải thích: vì sao chưa xác định được (thiếu dữ kiện gì, hay dữ liệu đã lưu không tách được các giải thích); các giải thích khả thi còn lại; bằng chứng hoặc phép phân tích nào phân xử được, trên dữ liệu nào, chi phí; kết luận nào phụ thuộc. Không dừng ở một câu "chưa xác định".
20. Mỗi phần chờ Minh quyết phải kèm đề xuất của agent trong chính lượt đó: chọn gì, vì sao, mặt trái, phương án khác đã xét. Prompt bàn giao yêu cầu agent đối phương phản biện các đề xuất ấy. Đề xuất không thay quyết định của Minh.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: CHẶN hoặc KHÔNG CHẶN; chặn kết luận/quyết định nào; ở đâu; sai gì;
bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); hậu quả; đề xuất sửa tối thiểu hoặc bằng chứng còn thiếu.
Tiếng Việt, câu ngắn.

Cuối lượt báo:
1. Đã làm gì.
2. File đã thay đổi, hoặc không sửa file nào.
3. Kiểm đã chạy và kết quả.
4. Bất đồng có bằng chứng, câu hỏi mở, phần thiếu và quyết định bị ảnh hưởng; điều cần Minh quyết.

Đề xuất tiếp tục hoặc dừng phản biện, kèm lý do. Nếu không còn phản đối chưa xử lý ảnh hưởng tính đúng, phạm vi kết luận hoặc quyết định đang xin duyệt, đề xuất dừng; không che bất đồng bên kia còn giữ. Có thể thống nhất giới hạn khi thiếu bằng chứng; kết luận phụ thuộc vẫn OPEN. Minh quyết cuối. Hai agent đồng ý không thay bằng chứng khoa học; dừng phản biện không tự duyệt SPEC, đóng task hoặc mở test.

Sau đó soạn prompt bàn giao cho agent đối phương: chép nguyên văn Prompt chung + đúng Khối công đoạn + Khối cổng hiện có trong docs/review-prompt.md, chỉ điền thông tin trung tính. Giữ vai trò; người làm nhận prompt đáp phản biện, người phản biện nhận prompt kiểm độc lập. Vẫn soạn khi đề xuất dừng để Minh chọn gửi hay dừng; không tự gửi.

Công đoạn: người làm đáp phản biện. Giữ vai trò người làm, không là người phản biện chính thức của chính task.
Tự soát yêu cầu và mọi file đầu ra gốc cần để trả lời các câu hỏi như một người chưa từng làm task, TRƯỚC khi mở kết luận các bản phản biện. Ghi danh sách điểm tự tìm được vào LOG trước khi mở các kết luận ấy nếu được phép ghi; phiên chỉ đọc ghi nhận xét trong chat.
Sau đó kiểm từng điểm phản biện trên file/code/dữ liệu thật; chạy lại khi rẻ và được phép. Kết luận đúng / đúng một phần / sai / chưa kiểm được với bằng chứng riêng. Reviewer có thể sai, nói quá hoặc đề xuất sửa có mặt trái.
Nếu được Minh cho phép: điền bảng Phản hồi của người làm ở cuối đúng bản phản biện; thêm N1, N2… cho điểm tự tìm được với CHẶN/KHÔNG CHẶN; để trống cột Minh quyết; nối LOG đủ mục 7 của AGENTS, gồm đề xuất sửa gom theo file; chỉ cập nhật dòng task trong STATE khi được phép. Không sửa nội dung hay prompt của reviewer hoặc tự sửa báo cáo/code.
Nếu chưa có quyền ghi các phần này, trình phản hồi và đề xuất trong chat. Soạn prompt bàn giao cho người phản biện kiểm độc lập.
```

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R1 | Đúng; CHẶN phát lịch qua `chuoi_tai` (tới khi sửa) | Đọc `chuoi_tai.py` `phat()`, `cho_xong()`: start bị từ chối vẫn gọi `get`, container cũ được nhận thành lượt mới. Lỗi có từ trước đợt dọn; bản sửa REVIEW-3 chỉ chặn ở `start`. Sửa (Minh duyệt 26/11, lab `c1da15f`): từ chối tag → `tag_da_dung`, dừng chuỗi, không gọi `get`, giữ trạng thái khi chạy lại; chỉ nhận container bắt đầu không sớm hơn `sap_phat` quá 120 s ở nhánh start lỗi và lúc chờ/tiếp nhận. Giả lập trong bộ nhớ trên obs (không SSH máy tải, không tải): 15/15 đúng, gồm nhận lại đúng sau lỗi SSH, tiếp nhận đúng lần, lệch đồng hồ 60 s nhận / 300 s từ chối; bản cũ sai 11/15. Chưa thử trên lượt tải thật. | |
| R2 | Đúng; CHẶN bật lại RCA trực tuyến (tới khi sửa) | `kiem_dich` chỉ kiểm 2 thư mục con; điểm ghi root đi sâu hơn; `orchestrator.py` ghép `--khoi-tao` vào chuỗi shell. Rủi ro hiện tại thấp: `dev` 4.025 mục, `online-dev-001` 62 mục, 0 mục không thuộc root, 0 symlink. Sửa (lab `c1da15f`): quét cả cây đích và nguồn không theo liên kết, từ chối symlink, mục không thuộc root, file nhiều hard link; quét lại ngay trước ghi ca; truyền đường chuẩn hóa, `shlex.quote`; `--khoi-tao` chỉ nhận `rong`/`chep:`. Kiểm bằng root trên obs với gốc tạm: 22/22 đúng, gồm 2 bộ thật qua và đường có dấu cách, `;`, `$(...)` giữ nguyên một đối số; bản cũ sai 5. Chưa chạy toàn tuyến webhook → G1. | |
| R3 | Đúng; KHÔNG CHẶN | Chạy lại cùng truy vấn Prometheus 7 mốc: khớp cả 7 số của Codex. Đọc `rules.yaml`: `gt 60`, `for: 60s`, `noDataState: Alerting`, đánh giá 10 s. Lệnh dừng gồm cả Collector agent và gateway, không tách được. Sửa `q4/README.md` (giữ cơ chế tuổi mẫu và mốc đo, ghi "chưa kiểm" cho "không có request", hệ quả có điều kiện) và dòng README trong `q4/SHA256SUMS` (12/12 OK). | |
| R4 | Đúng; KHÔNG CHẶN | `REVIEW-3` ghi R1–R5 là CHẶN từng đường dùng; STATE ghi "R1–R7, không chặn". Sửa dòng T-070: mức đúng của hai lượt, lab `c1da15f`, chưa phát lịch qua `chuoi_tai` và chưa bật lại trực tuyến tới khi Codex kiểm. `TRANG-THAI.json` còn ghi `3ac0d07` và prompt 5: không nằm trong file được duyệt lượt này, trình riêng. | |
