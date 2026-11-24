# NHÁP SPEC W9a — Diễn tập demo RCA trên FlashTicket

**Trạng thái:** đề xuất trong chat, chưa duyệt chạy. Điều phối cấp mã task. **Gói:** MRP P10, phần demo chuẩn bị G6. **Vai trò dự kiến:** Codex soạn nháp, Claude soát nháp độc lập. Khi mở task, đề xuất Claude phụ trách triển khai cùng Minh theo kế hoạch G5, Codex phản biện kết quả. Minh duyệt cuối.

**Điểm cần chốt trước tiên:** đặt chỗ S6 và duyệt vùng ghi cùng cấu hình Grafana dành cho W9a. Ở commit E5, ba dashboard đã sinh sẵn với nguồn `t073-e5-001`, còn `g1_b.py` từ chối tên bộ ngoài tiền tố `t073-`. Chỉ đổi `--ra` khi bật dịch vụ sẽ làm dashboard đọc sai nguồn hoặc làm bước ghi ca thất bại. Đề xuất dùng **một bộ hiển thị mới cho W9a, hai mã lượt riêng**, giữ nguyên bằng chứng E5. [Gói triển khai E5 §1, §4–5](D:/RCA-flashticket/results/T-073/trien-khai-e5.md) · [Hợp đồng I7, I9, I15](D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/HOP-DONG.md)

## 1. Mục tiêu

Người xem theo được một sự cố từ lúc FlashTicket chịu tải đến lúc Grafana cảnh báo, dịch vụ RCA tự tạo ca và giao diện hiện đồ thị, xếp hạng cùng bằng chứng. Khi mất mạng, người trình bày mở lại được đúng ca trên laptop. Bàn giao kịch bản, video và **hai lượt diễn tập trọn tuyến không lỗi**. Demo không có LLM. W9a trả lời phần minh họa phát hiện và chẩn đoán của DT18. Độ chính xác, độ nhạy và khả năng khái quát theo RQ5 thuộc W6–W7. [Kế hoạch §8.2, W9a](D:/RCA-flashticket/docs/techstack/KE-HOACH-GIAI-DOAN-2.md:142) · [DT18](D:/RCA-flashticket/docs/reference/sources/DT18-de-tai-va-nhiem-vu.md) · [Hướng dẫn của cô](D:/RCA-flashticket/docs/reference/sources/advisor-2026-09-23.md) · [MRP P10](D:/RCA-flashticket/docs/MRP.md:303)

## 2. Câu hỏi, phép kiểm và quyết định

| Câu hỏi | Phép kiểm và bằng chứng | Cách quyết |
|---|---|---|
| Ca đang trình bày có do cảnh báo thật của lượt này kích hoạt? | Nối cảnh báo lớp `he-thong` → `startsAt` làm t̂ → giờ nhận webhook → sự cố → `kiem_t` → mã ca mới → lần đầu thấy mã trên giao diện. Đối chiếu sổ tiêm sau lượt, ngoài tiến trình RCA. | Đạt khi chuỗi khớp, đúng nguồn W9a, mở được ca trong **25 phút từ t̂**. Tin Test, ca cũ, hoặc chỉ mục đã ghi nhưng giao diện chưa hiện đều chưa đủ. |
| Khi mất kết nối, có thể trình bày lại cùng bằng chứng? | Đóng tunnel, ngắt mạng laptop, mở phiên trình duyệt mới. Từ gói cục bộ chọn đúng mã ca, xem thời gian, đồ thị, xếp hạng và bằng chứng đã lưu. Mở riêng video và đối chiếu mã ca. | Đạt khi người xem thực hiện lại được các thao tác đã ghi. Video xem được nhưng trang phát lại cần máy từ xa thì phần offline trượt. |
| Sau diễn tập, W7 có nhận lại máy đúng trạng thái? | So trước/sau về lỗi đang tiêm, tải, checkout, chế độ thu, luật cảnh báo, nguồn dashboard và số đơn tăng. | Chỉ trả máy khi trạng thái khớp bàn giao. Ghi lượng tăng DB để W7 nhận diện trôi giữa các khối. |

## 3. Đầu vào và lịch máy

- **W5.** Minh đã nhận chức năng E5 cho một ô `PAUSE-PAYMENT` tải ×1. Mốc giao diện là **cận trên 898,8 giây sau t̂**. Ca thiếu phủ sáu chuỗi metric Payment. Đây là căn cứ chọn ô để diễn tập và dự trù thời gian. Commit E5 `81a9273` bật tuyến, P `779f90c` tạm bật sáu trang lưu trữ, H `1bb40ca` hoàn tác. Sổ máy ghi S4 đã đóng ngày 23/11 ở H, bộ nhận T-072 còn chạy. Kiểm lại trạng thái thật khi nhận S6. [Kết quả E5 §1–5](D:/RCA-flashticket/results/T-073/e5-ket-qua.md) · [Đính chính E5](D:/RCA-flashticket/results/T-073/dap-cx21/dinh-chinh-e5-1.md) · [Lịch máy](D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/LICH-MAY.md)
- **W4.** Dùng 11 luật và ngưỡng đã khóa. Bật thu cảnh báo từ trước lúc phát tải. Chạy tải **ít nhất 5 phút trước phần trình bày phát hiện**, giữ cả cảnh báo đầu lượt và khi hồi phục. Tác dụng giảm dao động p95 của cách bố trí này **chưa kiểm**. [Phân tích p95 §4–5](D:/RCA-flashticket/results/T-072/troi-p95-e2-e4.md)
- **Thứ tự.** Theo phương án C, **E6 trước, W7 chạy đêm, W9a ban ngày giữa các khối**. Q9 từng cho E7 đi trước E6 khi W5/W8 sẵn, S4 đã trả trước lúc E6 được duyệt và máy rảnh. Sau quyết định hoãn tích hợp LLM, W9a bỏ W8 khỏi nội dung demo. Muốn áp ngoại lệ Q9 theo điều kiện đã thay đổi, điều phối phải trình Minh và giao S6 rõ ràng. Hạn bán ghi nhận trước E6 là **02/12/2026 lúc 22:16:31 UTC**. E6 chịu trách nhiệm gia hạn, giữ sức chứa 100.000 theo quyết định 24/11. Trước mỗi lượt kiểm hạn thực tế và số vé còn đủ cho cả lượt. [Quyết định Q9 và phương án C](D:/RCA-flashticket/docs/DECISIONS.md:782) · [Nháp E6 §3](D:/RCA-flashticket/results/T-074/e6-spec-nhap-2.md:40) · [Điều kiện bàn giao W7](D:/RCA-flashticket/results/T-074/w7-spec-nhap.md:115)

## 4. Đầu ra và phạm vi ghi đề xuất

| Nơi ghi sau khi được duyệt | Nội dung |
|---|---|
| `results/<mã-W9a>/kich-ban.md` | Kịch bản có lời dẫn ngắn, thứ tự thao tác, mốc chờ, cách chuyển offline và hoàn tác. |
| `results/<mã-W9a>/luot-<nn>/` | Mỗi lần thử có hồ sơ riêng, kể cả lượt hỏng. Lưu mốc UTC, mã sự cố/ca, bằng chứng cảnh báo, ảnh danh sách và trang ca, kết quả kiểm offline và bàn giao. |
| `results/<mã-W9a>/ket-qua.md`, `SHA256SUMS` | Bảng đạt/trượt theo lượt, đường dẫn và trường bằng chứng, giới hạn, vị trí và hash của video/gói offline. Đề xuất giữ hiện vật nặng tại `D:/RCA-archive/<mã-W9a>/`. |
| Repo lab và máy | Trình diff ba dashboard hiện hành sinh từ `RCA_G1_BO` mới, cấu hình bật/gỡ cần thiết theo checkout bàn giao. Đề xuất bộ G1 riêng `rca-results/t073-w9a-<mã>/` để dùng được chốt tiền tố hiện có. `runs`, spool, đầu ra M1, tag tải, sổ tiêm và vùng tạm exp-app phải có đường dẫn riêng được liệt kê trước khi phát. Chỉ mục E5 và bộ `t065-l11-001` là nguồn đọc. |

Người làm ghi LOG của task và dòng tương ứng trong STATE sau duyệt. Theo I15, điều phối giữ quyền ghi `HOP-DONG.md`, `LICH-MAY.md`, `TRANG-THAI.json`. **I7 hiện nêu S2/S4 cho thay đổi Grafana, I9 dành đổi nguồn T-073 cho S4, trong khi lịch để quyền S6 “theo SPEC W9a”.** Đề nghị Minh duyệt quyền cho **đúng chủ S6, đúng đường dẫn và hai chiều bật/hoàn tác**. Lịch trống chưa cấp các quyền đó. [Hợp đồng I7–I15](D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/HOP-DONG.md:40)

## 5. Các bước

1. **Chuẩn bị trên laptop.** So hash đầu vào với manifest. Dùng lại cấu hình E5 đã kiểm, sinh ba dashboard trỏ bộ W9a, rà mọi URL và thử đường ghi của `g1_b.py`. Rà cả `RCA_M1_ROOT` và quyền của tiến trình con vì mặc định M1 ghi vào vùng chung. Trình điều phối diff, đường ghi thật, commit bật và đích hoàn tác. Dùng lại P chỉ khi cần mở trang lưu trữ tạm. Phát lại offline được kiểm riêng.
2. **Nhận S6, bật chế độ (b).** Chụp trạng thái bàn giao trên exp-app, exp-obs, máy tải và Grafana. Kiểm đúng HEAD, cây sạch, không job xung đột, điều kiện ô tiêm, hạn bán và vé còn. Tạo bộ hiển thị mới, ghi danh sách mã ca có sẵn. Bật bộ nhận T-073 với spool mới, giữ bộ nhận T-072. Theo I7, kiểm trước từng lần đổi checkout, báo SHA trước/sau cho điều phối. Nạp lại Grafana, kiểm sức khỏe, 11 luật và hai đích nhận bằng tin Test riêng. Mở dashboard xác nhận nguồn mới. Bật `orchestrator.py chay` với `RCA_ONLINE_OUT`, `RCA_M1_ROOT`, `--ra`, `--spool` đúng vùng duyệt. Tin Test phải vào lớp quan sát.
3. **Diễn tập hai lượt độc lập.** Mỗi lượt dùng tag, spool và hồ sơ mới. Đề xuất cùng ô dev `PAUSE-PAYMENT`, tải ×1 theo E5: **10 phút nền → 10 phút tiêm → 10 phút hồi phục**. Bật quay và ghi cảnh báo từ đầu. Sau ít nhất 5 phút tải mới bắt đầu phần trình bày phát hiện. Kiểm có lưu lượng thật và đầu dò Payment trước tiêm. Trình bày lần lượt tải → tiêm → cảnh báo thật → làm mới danh sách ca → mở đúng ca → xem đồ thị, hạng và bằng chứng → mở trang phát lại. Ghi riêng giờ gây lỗi, t̂, giờ nhận webhook và giờ đầu tiên thấy ca trên giao diện. Phần đối chiếu sổ tiêm thực hiện sau khi đã cố định đầu ra.
4. **Phát lại offline.** Gói các tệp của chính ca vừa diễn tập cùng trang xem và tài nguyên cần thiết trên laptop. Thử lại khi ngắt mạng, đóng tunnel, mở phiên mới để loại trừ dữ liệu còn trong bộ nhớ trình duyệt. Trong video phân biệt đoạn trực tuyến, đoạn chờ được rút ngắn nếu có và đoạn phát lại. Giữ mốc UTC thật.
5. **Hoàn tác, trả máy trước khối W7.** Gỡ lỗi tiêm, kiểm sạch, dừng đúng tag tải. Đặt STOP riêng của lượt, chờ ca đang xử lý kết thúc, dừng bộ điều phối W9a. Phục hồi cấu hình bàn giao theo cơ chế H có lệnh gỡ integration, nạp lại Grafana, kiểm 11 luật, đích T-072 và nguồn trang ca/phát lại. Gỡ bộ nhận riêng, giữ hiện vật. Nếu W7 đã vào lịch, kiểm bộ chụp W7 trở về đúng chế độ **chỉ thu**. Báo thay đổi DB, hiện vật còn giữ, job và trạng thái ba máy cho điều phối đóng S6. Nếu trạng thái nhận máy khác H, phải có đích hoàn tác tương ứng trước khi bắt đầu.

## 6. Kiểm đúng đắn và tiêu chí xong

**Một lượt lỗi** khi thiếu một mắt xích bắt buộc, ca gắn sai lượt hoặc sai t̂, cảnh báo đầu lượt bị che, ca không hiện trên giao diện trong 25 phút, trang ca/phát lại không mở đúng dữ liệu, offline còn cần máy từ xa, hoặc còn lỗi tiêm/cấu hình cản bàn giao. Với ô đề xuất, dùng cửa sổ E5 để đối chiếu sau lượt: cảnh báo hệ thống của ca phải có t̂ trong `[lúc tiêm, lúc tiêm + 600 giây)`. Nếu cảnh báo đầu lượt đã mở một sự cố khiến không tách được ca demo, ghi lượt **chưa đạt** và giữ toàn bộ cảnh báo. Không chọn lại t̂.

**Cách trình bày giới hạn.** Ghi riêng độ phủ thực tế và đầu ra V082, kể cả khi hạng đầu khác thành phần bị tiêm. Liên kết `live-down` đã biết hỏng ở bước tạo truy vấn Prometheus. Dùng bằng chứng đã lưu và nêu giới hạn ngay trên kịch bản. Chú thích “Hash do chỉ mục T-064 cấp” sai cho ca `t073-b`. Đối chiếu hash đầu ra thực của ca, bỏ câu chú thích đó khỏi lời dẫn. Các giới hạn đã công khai không làm trượt chức năng nếu người xem vẫn mở được bằng chứng bắt buộc. [Kết quả và giới hạn E5 §3–5](D:/RCA-flashticket/results/T-073/e5-ket-qua.md) · [Đính chính nguồn hash](D:/RCA-flashticket/results/T-073/dap-cx21/dinh-chinh-e5-1.md)

**Xong** khi có hai lượt trọn tuyến đạt trên cấu hình demo chốt, từng lượt có bằng chứng trực tuyến và offline, video cuối mở được từ laptop, hoàn tác đạt và điều phối nhận máy. Lỗi riêng ở khâu xuất video được xử lý từ bản quay gốc. Nếu sửa cấu hình dùng chung sau một lượt, xác định lượt nào còn tương đương trước khi tính đủ hai lượt. Giữ lịch sử mọi lần thử. Phạm vi W9a không gồm sửa ngưỡng, đổi thuật toán, tích hợp LLM, gia hạn DB hoặc chấm W7.

## 7. Lỗi ở 10%, 50%, 99% và chi phí

| Khi phát hiện | Xử lý và phần cần chạy lại | Chi phí tăng ước lượng |
|---|---|---|
| **10%**, sai nguồn, thiếu quyền, hết hạn bán, thiếu vé hoặc đầu dò chưa sẵn | Dừng trước tiêm. Giữ hồ sơ, hoàn tác phần đã bật. Sửa đúng phụ thuộc rồi tiếp từ bước bật/kiểm. Vấn đề ngày bán chuyển E6. | 10–25 phút kiểm lại sau khi đã sửa, chưa gồm thời gian chờ E6. |
| **50%**, tải/tiêm hỏng, không nhận cảnh báo, ca xử lý lỗi | Gỡ lỗi và dừng riêng lượt đó. Giữ spool, sổ và trung gian để phân biệt lỗi tải, nguồn quan sát, xử lý hay giao diện. Chạy lại một lượt bị ảnh hưởng. Lỗi nguồn chung thì dừng cả khung và xác định các lượt liên quan. | 35–50 phút/lượt, cộng thời gian sửa. |
| **99%**, hỏng video/gói offline hoặc hoàn tác chưa đạt | Có bản quay và gói ca hợp lệ thì dựng lại, kiểm offline trên laptop. Thiếu bằng chứng trực tuyến không thể khôi phục thì lặp riêng lượt đó. Hoàn tác chưa đạt thì giữ quyền xử lý và báo điều phối trước giờ W7. | 10–30 phút cục bộ, hoặc 35–50 phút nếu phải diễn tập lại. |

**Ước lượng xin duyệt:** hai lượt tải khoảng 60 phút. Cộng bật dịch vụ, chờ hiển thị và trả máy, dự trù **1,5–2 giờ lịch ban ngày**, tương đương **4,5–6 giờ-máy giữ chỗ** nếu giữ đồng thời ba máy suốt khung. Chuẩn bị kịch bản, đóng gói và kiểm video trên laptop khoảng 1–2 giờ, có thể làm ngoài khung máy. Dung lượng video/gói offline **chưa đo**. Đây là chi phí vận hành demo, ngoài phép tính Q-40 cho một phương pháp trên một dataset. Theo luật 8 và 21, trình Minh duyệt khung dài trước khi phát.

## 8. Việc cần Minh quyết

| Việc | Đề xuất và lý do | Mặt trái / phương án khác |
|---|---|---|
| **Nguồn hiển thị và quyền S6** | Duyệt bộ G1 mới có tiền tố `t073-`, commit dashboard trỏ đúng bộ, các vùng ghi và quyền hoàn tác cụ thể. Cách này giữ được chốt bảo vệ trong code và tách được ca W9a khỏi E5. | Cần soát diff và đổi checkout. Dùng nguyên E5 giảm chuẩn bị nhưng sẽ ghi thêm vào bộ bằng chứng cũ, phải xin quyền riêng và phân biệt rõ các ca phát sinh. |
| **Ô demo và chuẩn đạt** | Chọn `PAUSE-PAYMENT` ×1 hai lần, mốc UI 25 phút, báo trung thực hạng và độ phủ. Đây là ô đã có bằng chứng chức năng và đường gỡ lỗi. | Một ô chỉ minh họa được một tình huống. Chọn ô khác có thể phù hợp lời kể hơn nhưng đường cảnh báo và thời gian hiển thị của ô đó chưa kiểm. |
| **Lịch và bàn giao W7** | Giữ phương án C, chỉ đặt khung ban ngày đủ cho hai lượt và hoàn tác, sau khi có biên nhận E6 và W7 giao máy. | Có thể phải chờ sang ngày sau. Đi trước E6 chỉ đề nghị khi đủ điều kiện Q9 đã cập nhật, hạn bán/vé đủ và Minh duyệt ngoại lệ. |
| **Offline, video và vai trò** | Duyệt gói ca tự mở trên laptop, video từ một lượt đạt, hiện vật nặng ngoài Git. Claude phụ trách triển khai, Minh trình bày/duyệt, Codex soát kết quả. | Cần chuẩn bị tài nguyên cục bộ và bàn giao gói ngoài Git. Chỉ giữ video nhẹ việc hơn nhưng bỏ mất thao tác chọn ca và xem bằng chứng offline. |

**Chưa kiểm:** quyền S6 chưa được cấp trong nguồn đã đọc. Chưa thử commit trỏ nguồn mới, quyền ghi M1 tách riêng, bộ phát lại khi máy thật sự mất mạng, thời lượng video hoặc trạng thái máy sau pha ghi E6. Những điểm này quyết định khả năng phát và nghiệm thu hai lượt. Nháp chưa xác nhận W9a đạt.

**Kiểm trong phiên:** chỉ đọc tài liệu và mã tại commit E5. Hash khớp **52/52** hiện vật trong manifest E5, **5/5** tệp của gói p95 và mục nháp E6 bản 2 trong manifest T-074. Không sửa file nào, không dùng subagent, không giữ máy và không phát job.

<details>
<summary>Prompt bàn giao để Minh tự chuyển khi muốn soát nháp</summary>

Dán bản nháp trên cùng prompt dưới đây. W9a chuẩn bị G6. Mẫu hiện có khối cổng đến G4.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: nháp SPEC W9a trong chat, nguyên văn kèm theo.
- Công đoạn: soát SPEC.
- Gói/cổng: P10, phần demo chuẩn bị G6.
- Người làm và người phản biện chính thức: ngoài task, Codex soạn nháp, Claude dự kiến soát nháp.
- Tài liệu gốc: tasks/_MAU/SPEC.md, docs/techstack/KE-HOACH-GIAI-DOAN-2.md, docs/DECISIONS.md, tasks/T-070-dieu-phoi-giai-doan-2/{SPEC.md,LICH-MAY.md,HOP-DONG.md}.
- Phản biện và phản hồi trước: không có bản trước kèm theo.
- Code và kết quả liên quan: results/T-072/troi-p95-e2-e4.md, results/T-073/{trien-khai-e5.md,e5-ket-qua.md,e5/SHA256SUMS,dap-cx21/}, results/T-074/{e6-spec-nhap-2.md,w7-spec-nhap.md}, repo lab tại revision E5/P/H ghi trong hồ sơ triển khai.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc có chọn lọc, tự làm trong phiên, không dùng subagent, chỉ trả lời trong chat.

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

Đề xuất tiếp tục hoặc dừng phản biện, kèm lý do. Nếu không còn phản đối chưa xử lý ảnh hưởng tính đúng, phạm vi kết luận hoặc quyết định đang xin duyệt, đề xuất dừng; không che bất đồng bên kia còn giữ. Có thể thống nhất giới hạn khi thiếu bằng chứng; kết luận phụ thuộc vẫn OPEN. Minh quyết cuối. Hai agent đồng ý không thay bằng chứng; dừng phản biện không tự duyệt SPEC, đóng task hoặc mở test.

Sau đó soạn prompt bàn giao cho agent đối phương: chép nguyên văn Prompt chung + đúng Khối công đoạn + Khối cổng hiện có trong docs/review-prompt.md, chỉ điền thông tin trung tính. Giữ vai trò; người làm nhận prompt đáp phản biện, người phản biện nhận prompt kiểm độc lập. Vẫn soạn khi đề xuất dừng để Minh chọn gửi hay dừng; không tự gửi.

Công đoạn: soát SPEC.
Kiểm câu hỏi nguồn, phần mục tiêu được bao phủ, giả thuyết khác, khả năng phân xử của dữ liệu, phép kiểm dự kiến, phụ thuộc bước, chi phí, phạm vi và tiêu chí xong. Phần không làm phải có lý do, hệ quả và quyết định phụ thuộc.
Đánh giá kế hoạch và bằng chứng đã có; không đòi có kết quả của thực nghiệm chưa được duyệt. Phân biệt ứng viên để thử với lựa chọn đã chốt.
Chỉ ghi bản phản biện được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat nếu chưa có quyền ghi. Không tự sửa SPEC.
```

</details>