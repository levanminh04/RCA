# Prompt tiếp quản chiến dịch M1-FlashTicket nhiều ngày

Cập nhật theo gói sửa Minh duyệt 13/11/2026. Minh dán nguyên khối dưới vào phiên Claude mới trong `D:\RCA-flashticket`. Quyền và mục tiêu có nguồn ở `docs/DECISIONS.md`, mục “Bổ sung quyền điều phối chiến dịch nhiều ngày”.

```text
Bạn tiếp quản vai trò ĐIỀU PHỐI chiến dịch M1-FlashTicket trong repo D:\RCA-flashticket.

MINH ĐÃ DUYỆT
Gói chiến dịch ngày 13/11/2026 và gói sửa bốn SPEC, bốn file điều phối đã được Minh duyệt. Nguyên lời bổ sung: “duyệt sửa, không ảnh hưởng đến plan chính nhé, sau đó soạn prompt đầy đủ chi tiết tôi chỉ việc dán mà không cần duyệt thẻm gì, cho claude toàn quyền điều phối và triển khai”.

Hãy điều phối và triển khai liên tục trong phạm vi đã cấp tới M4. Minh sẵn sàng treo máy nhiều ngày. Báo cáo sáng và các ước lượng ngày công dùng để cập nhật tiến độ. Sau báo cáo, tiếp tục các việc có đủ đầu vào. Các mục tiêu H1–H8, mốc M0–M4, tiêu chí chọn và giới hạn hiện hành của plan chính tiếp tục áp dụng.

1. ĐỌC NGUỒN VÀ KIỂM TRẠNG THÁI

Đọc theo thứ tự, dùng đường dẫn dưới D:\RCA-flashticket.
- AGENTS.md.
- tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md, đặc biệt quyền tại mục 6 và phụ thuộc tại mục 7.
- tasks/T-062-dem-chang-1-4/CHECKPOINT-CHIEN-DICH.md.
- tasks/T-062-dem-chang-1-4/SPEC-PHU-LUC-2.md và phần bổ sung cuối file.
- tasks/T-063-quan-sat-thu-dev-2/SPEC.md và phần bổ sung cuối file.
- tasks/T-064-m1-flashticket/SPEC.md và phần bổ sung cuối file.
- tasks/T-065-giao-dien-grafana/SPEC.md và phần bổ sung cuối file.
- results/T-064/tieu-chi-chon.md, LOG từng task, docs/STATE.md, docs/LESSONS.md.
- Mục “Bổ sung quyền điều phối chiến dịch nhiều ngày” ở docs/DECISIONS.md và các mục WHY liên quan.
- tasks/T-062-dem-chang-1-4/SPEC.md để lấy bảng máy, truy cập và nguồn lịch sử, cùng BOI-CANH.md.
Đọc phần MRP, DT18 và hướng dẫn giảng viên trực tiếp chi phối bước sắp thực hiện.

Trước khi ghi nhịp tim, đọc trạng thái cũ và kiểm phiên điều phối, tiến trình con, lệnh nền đang giữ công việc. Nếu chủ cũ còn hoạt động, phối hợp và tránh phát trùng. Nhịp tim cũ là dấu hiệu cần kiểm thêm. Khi đủ bằng chứng có thể tiếp quản, ghi phiên mới, giờ UTC và trạng thái công việc, rồi nối mục mở phiên vào LOG đúng vai trò.

File trạng thái điều phối `tasks/T-062-dem-chang-1-4/DIEU-PHOI-TRANG-THAI.json` được thêm ngày 14/11/2026 (DECISIONS, mục "Sửa cơ chế lịch tự tiếp nhận"). Lịch 15 phút đọc file này để quyết định tiếp quản. Phiên điều phối giữ file đúng thực tế:
- Khi tiếp quản: ghi `chu` (mã phiên của mình), `trang_thai: "dang_lam"`, `cap_nhat`.
- Khi phát lệnh nền dài: thêm vào `lenh_nen` gồm `loai`, `mo_ta`, `cach_kiem`, `bat_dau`. Nếu chủ dừng chờ lệnh đó thì đặt `trang_thai: "cho_lenh_nen"`.
- Trước khi kết thúc lượt: còn việc trong quyền mà không có lệnh nền giữ thì làm tiếp, không dừng sớm. Buộc phải dừng (hết hạn mức, chờ Minh, chờ lệnh nền) thì ghi `ket_luot` hoặc `cho_lenh_nen`, kèm `buoc_tiep` và `ly_do`.
- Việc Minh giao ngoài chủ (ví dụ Codex qua Codex app) ghi ở `viec_ngoai_chu`. Không phát trùng việc đó.
- Xong M4: ghi `xong_M4`.

Đối chiếu đầu ra, hash, checkpoint và tiến trình thực tế. Dùng lại phần đã hoàn thành hợp lệ, xác định phần thiếu trước khi chạy thêm. Trạng thái M0 và hạn mức trong hồ sơ có thể đã cũ.

2. MỤC TIÊU VÀ CÁC QUYẾT ĐỊNH ĐÃ CẤP QUYỀN

Lấy M1 P7 đã khóa làm nền, phát triển phiên bản thích nghi FlashTicket bằng dữ liệu quan sát phong phú hơn và phân tích hạn chế thực tế. Bàn giao một ứng viên M1-FT đề xuất chọn, có code chạy được, cấu hình, kết quả từng ca, cơ chế giữ/bỏ thay đổi, đánh đổi, phần chưa phân xử và dashboard đã kiểm.

Bốn mục từng chờ Minh xác nhận đã được xử lý.
- Claude tự quyết xuất bù, thu bổ sung/thu lại phần cần cho H1–H8 hoặc phần thu sai, sau khi rà khả năng dùng lại. Ghi phạm vi ảnh hưởng, lý do, chi phí và giữ lượt cũ. Mỗi ca một lần thu chính, các lần lặp để sau.
- Tiếp tục lưu code, cấu hình, kết quả và manifest. Việc chưa commit repo RCA không chặn nghiên cứu, commit/push repo RCA trình sau.
- Áp dụng tiêu chí đã trình tại results/T-064/tieu-chi-chon.md. Claude tự chọn biến thể, tổ hợp và ứng viên theo tiêu chí đó.
- Claude kiểm luồng lõi rồi tự chọn revision phù hợp trong nhánh rca/quan-sat-log, ghi WHY, commit, image và cấu hình thực triển khai trước khi đóng băng.

Claude tự quyết chi tiết kỹ thuật trong mục tiêu và phạm vi đã duyệt. Thiếu đầu vào do cấu hình, instrumentation, adapter hoặc bộ đóng gói trong quyền thì tự khắc phục và thử tiếp. Lựa chọn quan trọng ghi WHY trước khi dùng trong kết quả.

3. PHÂN CÔNG VÀ SONG SONG

Claude chính giữ điều phối, thiết kế phương pháp, phân tích cơ chế khó, tích hợp và lựa chọn ứng viên. Được dùng tối đa hai phiên Claude phụ và hai lượt Codex song song theo gói đã duyệt.

Codex dùng gpt-6.1-sol, reasoning high, full access.
- L1, phụ lục 2 T-062: API lõi, mock VNPay, tài khoản, dữ liệu thử và tải mua vé. Claude thiết kế kịch bản, kiểm và phản biện.
- L2, T-063: Claude làm quan sát, B16, đóng gói và thu dev, Codex phản biện.
- L5, T-064: Claude làm M1-FT, Codex phản biện.
- L3, T-065: Codex làm Grafana, Claude phản biện.

Minh cho Claude tự giao việc và tổ chức các lượt kiểm/phản biện theo phân vai trong chiến dịch, không chờ Minh chuyển prompt giữa các phiên. Phản biện theo docs/review-prompt.md và độc lập với phần người làm đã cài. Tự xử lý các sửa thuộc gói đã duyệt, lưu lịch sử và bằng chứng.

Brief ghi ra file rồi truyền qua stdin. Lưu nhật ký, mã thoát và checkpoint ở results/<task>/codex/. Kiểm báo cáo của agent trên code, dữ liệu và thao tác thực tế.

Phối hợp thay đổi máy theo quyền đã cấp. Tránh ghi đồng thời cùng file, tạo lại container trong lúc nhánh khác đang kiểm và thay đổi cấu hình đang đo. Theo dõi đầu ra từng phần để bắt đầu việc sau sớm nhất có thể.

4. ĐẦU VIỆC BAN ĐẦU VÀ TIẾN TRÌNH TỚI M4

Kiểm rồi tiếp tục phần chưa hoàn thành.
- Metric cũ tại results/T-062/ca/_metric-bo-sung/: đọc SU-CO.md, rc, manifest và nội dung xuất. Hồ sơ trước báo đã xuất xong và Prometheus restart một lần. Không suy đủ dữ liệu chỉ từ rc=0. Thiếu phần nào thì xét còn dữ liệu trên kho để xuất bù đúng phần ấy, cắt khúc truy vấn và theo dõi sức khỏe Prometheus.
- results/T-063/dieu-phoi/: hoàn thiện và kiểm gọi lại Codex, tự tiếp nhận, checkpoint.
- Retention Prometheus: kiểm cấu hình và dung lượng hiện tại, tăng trong quyền đã cấp, ghi thay đổi và kiểm sau khởi động.
- P7 và bộ chấm: kiểm nhóm hòa bằng src/p3/danh_gia.py, dựng src/m1_ft khi tắt thay đổi cho kết quả trùng P7 trên chín ca cũ.
- Phân tích dữ liệu cũ: span gốc, CPU từng container, thời gian độc quyền thao tác nền theo code M1, bảng hướng → tín hiệu.
- Phát L1 và L3 khi Codex sẵn sàng. Claude tiếp tục phần độc lập trong lúc chờ.

Các task chạy theo đầu vào từng phần.
- L1 bàn giao mock/tài khoản, một giao dịch chạy trọn và kịch bản tải khi từng phần đã kiểm.
- T-063 kiểm R trên giao dịch thật, sửa thiếu hụt quan sát rồi kiểm lại. Chuẩn bị đóng gói, phục hồi và ô dev song song khi có thể.
- T-064 thiết kế/cài/kiểm từng hướng khi có đầu vào. Chấm hiệu quả trên dữ liệu tương ứng đã kiểm. Kết luận giữ/bỏ và chọn cuối phải có đủ ca của phép so.
- T-065 G-a/G-b làm trên P7, thống nhất hợp đồng đầu ra với T-064 sớm. G-c tích hợp từ đầu ra phù hợp đầu tiên và kiểm cuối trên ứng viên M1-FT.

Trước lượt thu chính, xác nhận tải, quan sát H1–H8, đóng gói, phục hồi và lịch đầu dò trên cấu hình cuối. Ghim revision/image/workload/cấu hình, xác nhận can thiệp từng ô, lập hồ sơ luật 21 rồi thu và băm. Kiểm tích hợp lại phần chịu ảnh hưởng sau thay đổi máy. M0 chưa xong không chặn việc độc lập đã được phép.

5. PHÁT TRIỂN VÀ CHỌN M1-FLASHTICKET

Bao phủ các hướng đã duyệt.
H1 DB/cache/broker thành nút và xếp hạng cạnh.
H2 JVM/cgroup.
H3 pool kết nối.
H4 queue.
H5 thành phần chết im.
H6 thao tác nền.
H7 tải tăng so với sự cố.
H8 các điều chỉnh khác có lý do kỹ thuật, gồm adapter và log nghiệp vụ.

Mỗi hướng ghi nút/cạnh, nơi đặt tín hiệu, phép tính dùng quan hệ, điều kiện thất bại và đối chứng. Thử các tổ hợp có căn cứ, giữ sổ biến thể trước/sau chấm và mọi đầu ra.

Kiểm hash tiêu chí chọn với LOG T-064 trước khi chấm. Giữ quy ước hòa của P7(a), bảng nút/cạnh riêng và cách đếm K đã khai. Không chỉnh theo đáp án từng ca. Dữ liệu và ca mới dùng để chọn phải được khai đúng lúc trước chấm, phần kiểm cài đặt và hồi quy dùng đúng vai trò.

Tiếp tục tới tiêu chí kết thúc tìm kiếm đã duyệt. Phân tích ca thay đổi và ca sai còn lại, tách quan sát, cơ chế đã kiểm và giả thuyết chưa phân xử. Chọn ứng viên theo bằng chứng, báo cả trường hợp không hướng nào đạt luật giữ.

6. GRAFANA

Giao Codex hoàn thiện trong results/T-065/, lấy bản 6 làm mốc.
- Liên kết Loki ở bảng bằng chứng, điều hướng, khung giờ, vùng nghi ngờ và diễn giải panel rỗng có căn cứ.
- Bấm service mở bảng và đồ thị thao tác HTTP/SQL/job/message theo dữ liệu có, rồi mở bằng chứng từng thao tác.
- Cạnh có nguồn xác minh, loại quan hệ và độ phủ rõ. Hiển thị cờ M1 và hạng theo đúng dữ liệu thực.
- Chọn xem P7 hoặc M1-FT cùng ca, hiện phiên bản, cấu hình và cửa sổ.
- Kiểm bằng thao tác trình duyệt thật, đối chiếu nguồn và giữ bằng chứng.
Thiếu đường xuất, định dạng hoặc chỉ mục trong quyền thì tự hoàn thiện. Thiếu tín hiệu thu nhận thì phối hợp T-063. Chức năng chưa hoàn thành giữ trạng thái đạt một phần và tiếp tục xử lý.

7. PHẠM VI THỰC HIỆN

Nguồn chi tiết là mục 6 hồ sơ chiến dịch và các SPEC cùng phần bổ sung đã duyệt.
- RCA: src/m1_ft/, results/T-062 tới T-065 theo phân vai, hồ sơ task và checkpoint, dòng task trong STATE, thêm mục WHY/DECISIONS trong quyền.
- FlashTicket: D:/Project/flash-ticket-platform, nhánh rca/quan-sat-log, instrumentation và cấu hình quan sát, deploy/rca-test/, deploy/observability/. Được push nhánh và tắt Auto-fix PR #17 theo gói.
- exp-app: build/triển khai bản thử, mock VNPay, tài khoản, dữ liệu thử qua API, Collector, bộ tiêm và cấu hình trong quyền.
- exp-obs: Collector/Prometheus và retention thuộc T-063, dashboard mới và dữ liệu Grafana thuộc T-065. Restart cần được phối hợp và ghi biên bản.
- Máy tải: k6 và phần đã cấp trong phụ lục 2.

Giữ nguồn P7 tại src/m1/ và kết quả task đã khóa, dùng wrapper cho script ghim. Không sửa code nghiệp vụ, không merge/push main, không chạy cd.yml, không chạm máy 84, không mở dữ liệu khóa hoặc ô đánh giá. Baseline làm sau theo quyết định Minh. Không tự khóa M1 hoặc nghiệm thu thay Minh.

Dùng quyền đăng nhập đã cấp và công cụ được phép, các bước đã phân Codex tiếp tục giao Codex. Bí mật không đưa vào repo, log, prompt hoặc báo cáo. Mọi thay đổi máy ghi lệnh, giờ UTC, hash và cách hoàn tác.

8. HẠN MỨC, TIẾP NHẬN VÀ LỖI

Các giờ hồi Claude/Codex ngày 13/11 trong hồ sơ là mốc lịch sử. Mỗi lần lấy thời gian hiện tại và thông báo công cụ để chờ và gọi tiếp. Không kết thúc chiến dịch chỉ vì hết hạn mức.

Hoàn thiện cơ chế gọi lại và lưu bằng chứng kiểm tại results/T-063/dieu-phoi/. Ghi rõ lần thử mô phỏng và phần thực tế đã kiểm.
Kiểm lịch m1ft-tiep-nhan có thật, bật và kích hoạt được. Hồ sơ ghi lần tạo trước bị ứng dụng từ chối, phải tôn trọng kết quả đó. Nếu còn cần Minh tạo tay, báo đúng hành động và lý do từ chối, tiếp tục việc độc lập được phép. Không dùng cơ chế khác để vượt chặn công cụ hoặc tuyên bố tự phục hồi khi chưa kiểm.

Trước tiếp quản, kiểm phiên điều phối và tiến trình con, tránh phát trùng hoặc hai phiên ghi cùng đầu ra.
Sau mỗi bước và ít nhất 30 phút một lần khi hoạt động, ghi checkpoint với giờ UTC, bước, đầu ra, lệnh/session, hạn mức và bước tiếp. Trước nén ngữ cảnh hoặc hết lượt ưu tiên checkpoint. Khi ngủ/chờ, ghi cách đánh thức đã thiết lập thực tế.

Lượt dài phải có hồ sơ lỗi ở 10%, 50%, 99%. Xác định phạm vi lỗi, giữ lượt cũ, tự sửa trong quyền và tiếp tục từ phần hợp lệ. Một nhánh bị chặn chỉ làm chờ phần phụ thuộc. Tuân thủ quy định AGENTS về thử nhiều lần không tiến triển.

Chỉ trình Minh phần thực sự vượt quyền, như sửa nghiệp vụ, đổi tiêu chí sau xem kết quả, mở dữ liệu khóa/ô đánh giá hoặc mở rộng máy/file ngoài gói. Nêu bằng chứng và phương án cụ thể. Khi có D:/RCA-overnight/STOP hoặc Minh yêu cầu dừng, ghi checkpoint và dừng theo quy định.

9. BÁO CÁO VÀ HOÀN THÀNH

Khoảng 07:00 giờ VN mỗi ngày, ghi results/T-063/bao-cao-sang-<ngày>.md theo ngày thực tế. Nếu phiên nhận việc sau mốc cũ, báo trạng thái hiện tại rồi tiếp tục. Báo cáo có việc đã làm, đầu ra có kiểm, việc đang chạy, phần còn mở và bước kế tiếp. Sau báo cáo sáng hay báo cáo mốc, tiếp tục làm tối đa trong quyền tới M4.

Mốc M0–M4 dùng tổng hợp tiến độ. Đủ đầu vào thì chuyển việc kế tiếp ngay, cập nhật ETA từ số đo thực tế. Không tự đặt trần ngày công, số cấu hình hoặc phần tối đa làm trong một đêm.

M4 phải có ứng viên M1-FT, code/cấu hình, bảng từng ca, hồ sơ giữ/bỏ, phân tích đánh đổi và giới hạn, dashboard đã kiểm với bản đề xuất, manifest và cách tái lập, các lượt kiểm/phản biện theo phân vai. Ghi bàn giao cuối và trạng thái lịch tiếp nhận để tránh phát thêm việc khi hoàn thành.

BẮT ĐẦU bằng đọc nguồn, xác minh quyền tiếp quản và đầu ra hiện có, rồi thực hiện công việc chưa hoàn thành có đủ đầu vào.
```
