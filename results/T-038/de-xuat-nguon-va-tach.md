# Đề xuất nguồn và phạm vi tiếp theo cho T-038

**CANDIDATE — chưa duyệt tải, chọn snapshot hoặc sửa SPEC.** Ngày 16/10/2026. Đề xuất này không tự thu hẹp nghĩa vụ P5b. T-038 hiện chưa hoàn thành.

## 1. Căn cứ và lựa chọn cần Minh quyết

Đầu vào cũ đã kiểm hash. Nguồn RCAEval được lưu chỉ dẫn tới repository FudanSELab/train-ticket, không ghim revision ứng dụng sinh RE2-TT. Paper đã lưu tại T-002 mô tả stack thu thập ở `#S3.SS3.p1.1`; không có image digest, build, revision instrumentation hoặc manifest deployment. Code RCAEval và revision dataset không thay được các thông tin đó.

Đề xuất dùng **release v1.0.0 làm snapshot tham khảo có điều kiện** vì đây là một mốc release có tên, bất biến theo commit được ghim, dễ tái kiểm trên máy khác. Đây là lựa chọn nguồn để khảo sát; chưa chọn nó làm nguồn sinh dataset và chưa kiểm nó phù hợp hơn các release khác. Không chọn bằng mức khớp graph, tên service trong trace hoặc nhãn. Phương án khác là chờ tác giả/Minh cung cấp đúng build/deployment rồi mới khảo sát; cách đó tránh đọc một bản tham khảo khác revision nhưng chưa có thời điểm nhận nguồn. Không tự liên hệ tác giả.

Nguồn chính thức: [repository](https://github.com/FudanSELab/train-ticket), [release v1.0.0](https://github.com/FudanSELab/train-ticket/releases/tag/v1.0.0). Commit và Git tree cụ thể nằm trong JSON đề xuất, không dùng HEAD. Tag→commit→tree đã kiểm qua API Git metadata; tính lại toàn bộ tree object từ danh sách con đều khớp. Điều này kiểm danh sách đối tượng Git, chưa xác minh nội dung blob chưa tải hoặc liên hệ với dataset.

## 2. Gói tải đề xuất

Danh sách **từng đường dẫn, URL, mode, Git blob ID và byte** ở `runs/metadata-de-xuat-001/de-xuat-tai.json#/proposed_files`. Có 2.827 blob trong toàn cây 3.921 mục. Không dùng whitelist đuôi file. Bảng từng thư mục cấp đầu và tổng byte ở `#/groups`; đây là danh sách đề xuất, không là inventory ứng dụng đã khảo sát.

| Nhóm đối tượng | Vì sao cần và cách xử lý sau duyệt |
|---|---|
| Toàn bộ module ứng dụng, shared/common, client/handler/repository và tài nguyên đi kèm | Lập inventory, operation, quan hệ HTTP/RPC/data/messaging/nền từ nguồn; chưa biết nội dung trước tải. Không giới hạn theo service thấy trong trace. |
| deployment, root compose, cấu hình runtime, build/CI/script/Dockerfile, wrapper và lockfile | Lần theo image/build, cấu hình, template, schema, tham chiếu ngoài và nguồn sinh định danh/quan hệ. Không chạy build hay tải dependency. |
| Frontend, vendor/node_modules đã được commit, template/interface/mã sinh nếu có | Chưa thể chứng minh vô can bằng tên/đuôi file. Tải để phân loại, lần theo đầu vào và quan hệ thực sự; không mặc nhiên bỏ generated/vendor. |
| README, CHANGELOG, old-docs, image và tài liệu định dạng khác | Có thể chứa sơ đồ, mô tả triển khai hoặc quan hệ không hiện ở code. Tách tài liệu cũ với nguồn thực thi, không coi sơ đồ là runtime. |
| Symlink và archive/JAR có trong cây | Giữ mode và nội dung link như blob, không tạo link trỏ ra workspace. Archive/JAR chỉ giữ nguyên để kiểm provenance và liệt kê cấu trúc trước; không chạy, giải nén hàng loạt hoặc mở telemetry bên trong. Nội dung cần đọc/giải nén thêm phải được phân loại và trình đúng phạm vi/byte nếu chưa đủ quyền. |
| Git metadata định danh snapshot | Đề xuất lưu response metadata commit/tree/tag sau duyệt cùng manifest tải để coverage toàn cây kiểm được. Metadata tra hiện tại chỉ dùng trong bộ nhớ và danh sách đề xuất dẫn xuất. |

**Đường dẫn lưu đề xuất:** `results/T-038/sources/train-ticket-v1.0.0/`, manifest tải và mọi partial/lượt lỗi ở `results/T-038/runs/`. Không ghi `data/README.md` hoặc `data/`. Không clone Git history; không tải archive cả repo, image/container, dependency từ registry, wiki/PR, repo khác, LFS object bên ngoài hoặc submodule ngoài cây bằng quyền này. Metadata cây không có gitlink; chưa đọc `.gitattributes`/pointer nên LFS vẫn OPEN. Nguồn ngoài được code/build tham chiếu phải ghi chưa lấy, ảnh hưởng và đề xuất bổ sung; không gọi toàn Git tree là toàn bộ hệ đã triển khai.

**Cách tải đề xuất:** lấy từng blob theo URL commit đã liệt kê, đối chiếu byte và Git blob hash trước nhận; lưu SHA-256 cho payload thực. Giữ literal symlink, không thực thi file. Có thể gộp request cho blob trùng hash sau khi chứng minh danh sách tái dựng giữ đủ đường dẫn/mode; chưa lấy tiết kiệm dự kiến làm số thực. Chưa viết/chạy downloader.

## 3. Byte mạng, đĩa và chi phí

| Khoản | Trạng thái |
|---|---|
| Tổng nội dung blob nếu tải mỗi đường dẫn một lần | **29.074.015 byte**, tính từ trường size của toàn cây metadata. Đây là payload, không phải số byte mạng đo được. |
| HTTP header/TLS, metadata tải kèm, redirect, retry và lượt lỗi | **Chưa đo / OPEN**; cộng riêng trong acquisition manifest. 2.827 URL blob trước khi tối ưu trùng. |
| Archive nén cả repository | Không đề xuất tải. Byte nén chưa xác định, không dùng để ước lượng mạng. |
| Nội dung cây nguồn trên đĩa | **29.074.015 byte** nếu giữ blob literal theo đường dẫn; chưa gồm metadata, file-system allocation và partial/lượt lỗi. |
| Giải nén archive/JAR nằm bên trong cây | **Chưa đo / OPEN**, chưa được tính là dung lượng giải nén bằng 0. Gói này không tự giải nén chúng. |
| Giờ công truy nguồn/coverage | **CANDIDATE 2–4 giờ, chưa đo**, chưa gồm chờ duyệt/nguồn và phản biện. Phải tăng hoặc trình tách tiếp nếu nguồn ngoài/diagrams/archive làm vượt phạm vi. |
| Giờ công bản ghi → oracle → dựng/mapping → đối chiếu → phân tích → kiểm/bàn giao | **Chưa phân xử** trước khi đọc nguồn. Dự toán cũ 4–6 giờ cho cả TT chưa được kiểm chứng; không dùng làm trần cắt công việc. |
| Giờ máy tải, toàn bộ đối chiếu và tự kiểm; peak RAM | **Chưa đo / OPEN.** Lượt kiểm hash là kiểm toàn vẹn, không là benchmark phép đối chiếu. Không đo cùng việc nặng khác, không dừng tiến trình phiên khác. |
| Tổng lưu mọi lượt của toàn T-038 | **OPEN**, chưa có dự toán đã bao phủ toàn bộ. Công thức ở dưới giữ cả pilot, input/output, code snapshot, tự kiểm và lỗi/lặp; không gọi byte nguồn là tổng đĩa task. |

Kế hoạch tổng lưu cần tính: nguồn literal + metadata + bản ghi/fixtures/mapping/code + graph tĩnh + pilot + một lượt chính trên 1.069 graph + kiểm input không đổi + kiểm đảo thứ tự hợp lệ + toàn bộ lỗi/lặp/partial + LOG/bàn giao/manifest. Nếu chọn lưu đầy đủ mỗi lượt chính/tự kiểm thì phần so có ít nhất ba bộ kết quả theo từng graph; không lấy kích thước graph trace làm kích thước kết quả có members/provenance. Chưa có pilot để tính B_i (byte output từng graph) và t_i (giây xử lý), vì vậy tổng `sum(B_i)` và `sum(t_i)` còn OPEN. Không tự chạy pilot nguồn giả rồi ngoại suy thành chi phí TT.

Ngân sách Q-40 là tối đa ba giờ chờ thực tế cho toàn ca của một dataset theo phương pháp; task này không chạy baseline/RCA. Phần máy liên quan vẫn phải đối chiếu tổng sau pilot. Hiện chưa chứng minh toàn lượt trong ngân sách; nếu một lượt dự kiến hơn một giờ hoặc phát sinh thao tác tốn kém khác thì báo và chờ đúng luật. Không đề xuất EC2/GPU.

## 4. Đề xuất tách, chưa thực hiện

**Ưu tiên tách bước truy nguồn và coverage trước.** Chưa đủ bằng chứng để giữ lời hứa toàn chuỗi vừa một phiên. Không có nguồn ứng dụng trong quyền để kiểm thời gian đọc, nhóm quan hệ, operation mapping hay lượng phân xử chênh lệch. Số graph nhỏ trên đĩa không phân xử được giờ công này.

| Phần | Đầu ra và tiêu chí riêng | Nghĩa vụ chưa được coi là hoàn thành |
|---|---|---|
| A — truy nguồn/coverage | Ghim nguồn đã duyệt, lập chuỗi sáu trục revision, bảng toàn cây: đã đọc/loại trừ/chưa lấy/chưa rõ và ảnh hưởng, nguồn ngoài/owner cần thêm; có bằng chứng về phạm vi và dự toán thực để lập task sau. | Chưa nhận inventory thực thể/quan hệ đầy đủ, chưa dựng/so graph hoặc giải thích cơ chế mismatch. Không nghiệm thu P5b từ coverage. |
| B — bản ghi, dựng, đối chiếu và phân tích | Giữ toàn bộ bước 4–9 và tiêu chí hiện hành về inventory/operation/relations/binding/signals, oracle, mapping, hai mức/hai view/toàn graph, mismatch và match tương ứng, kiểm/bàn giao. Dùng nguồn/coverage A làm đầu vào. | Không bỏ bất kỳ nhóm nguồn, cửa sổ, phép kiểm hoặc phần nghiên cứu nào. SPEC và ước lượng một phiên của B phải soạn sau khi A cung cấp phạm vi thực; nếu B còn rộng thì Minh quyết chia tiếp. |

Đây là đề xuất tổ chức, **không tự tạo task B hoặc gán mã**, không tự sửa/đóng T-038. T-040 phải nhận đủ cả phần A và B; việc đồng bộ hợp đồng vẫn giữ pin T-036 chung với T-037/T-039. Không cần đổi src/T-036/T-035 hay phạm vi hai nhánh kia từ đề xuất này.

**Bản đồ tác động nếu Minh duyệt tách trước A:**

| File | Sửa cụ thể đề xuất; hiện chưa sửa |
|---|---|
| `tasks/T-038-p5b-trainticket/SPEC.md` | Giữ mục tiêu P5b và bản ghi nghĩa vụ gốc. Đổi phạm vi thực thi/đầu ra/tiêu chí task hiện tại thành A như bảng trên; ghi phần B chưa được làm/đóng và cần SPEC riêng sau coverage. Thay dự toán lịch sử bằng bảng chi phí có trạng thái; không chọn v1.0.0 là deployment dataset. Giữ lịch sử bản SPEC trước sửa dưới results/T-038/. |
| `tasks/T-038-p5b-trainticket/LOG.md` | Nối nguyên quyết định Minh và phạm vi mới, dẫn nguồn đề xuất; không thay lịch sử. |
| `docs/STATE.md` | Chỉ dòng T-038: phản ánh phần A được duyệt, B chưa triển khai và nghĩa vụ T-040; không sửa dòng task khác hoặc mục tổng hợp bằng quyền hiện tại. |
| `docs/WHY.md` | Nối WHY-53: tách do chưa phân xử khả thi, giữ toàn nghĩa vụ; ghi căn cứ lựa chọn snapshot tham khảo, phương án chờ đúng deployment và điều kiện thất bại. Chỉ làm khi Minh duyệt phạm vi này riêng/cùng gói rõ ràng. |
| `docs/DECISIONS.md` | Nối đúng lời Minh về duyệt tải/chọn snapshot tham khảo/tách A, sau khi có câu trả lời; không suy thành duyệt toàn B hoặc xác minh revision. Chưa cấp mã quyết định. |

Quyền tải và quyền tách là hai nội dung Minh có thể quyết riêng. Duyệt gói tải này không tự duyệt sửa SPEC, WHY hoặc DECISIONS. Chưa có quyền ghi các file đó từ phiên này; chúng chỉ nằm trong bảng đề xuất. Nếu Minh chỉ duyệt tải, có thể lấy nguồn trong phạm vi đã duyệt rồi báo dữ kiện khả thi, nhưng chưa thực hiện phần vượt điều kiện một phiên.

## 5. Phần đã đạt và còn mở

Đã đạt phần tự rà nguồn/công cụ, xác minh đầu vào cũ, selector toàn graph được giao và đề xuất tải có từng đối tượng. Chưa đạt tiêu chí hoàn thành T-038 hiện hành. Chưa có số khớp, nguồn gây mismatch, inventory đầy đủ hoặc bằng chứng lợi ích RCA.

Chuỗi dataset → application → instrumentation → image → deployment vẫn OPEN. Tác giả/chủ nguồn RCAEval là nơi có thể cung cấp manifest gốc; Minh quyết chờ, cấp nguồn khác hoặc cho khảo sát bản tham khảo. Với P6/P9/T-040, hiện chỉ chuyển được hợp đồng/miền đầu vào và danh sách bằng chứng thiếu. Chưa chuyển được quan hệ hoặc địa chỉ tín hiệu có nguồn TT. Không suy collector có thể bù thông tin chưa từng được ghi.

## 6. Nội dung quyết định hiện tại cần xin ghi chính thức riêng

Phiên này chỉ có quyền ghi LOG, kết quả và dòng STATE nên chưa ghi sổ quyết định. Đề xuất **chỉ nối một mục vào docs/DECISIONS.md**, mã lấy sau khi đọc bản mới nhất, không thay mục cũ:

> Minh giao Codex triển khai T-038 theo SPEC hiện hành có điều kiện: tự rà từ nguồn, kiểm khả thi một phiên và trình nguồn cần tải trước; Claude phản biện kết quả. Minh đã đồng ý dừng lượt phản biện ba SPEC T-037/T-038/T-039. Lời giao này chưa duyệt tải repository hoặc nguồn mới. Phạm vi ghi là results/T-038/, nối LOG T-038 và chỉ dòng T-038 trong STATE; giữ pin T-036 được SPEC liệt kê. Nếu cần sửa SPEC, lệch pin, xung đột nguồn/quyền hoặc chưa phân xử khả thi thì dừng phần phụ thuộc và trình Minh; không tự sửa SPEC hoặc chia task.

Nguồn: nguyên lời giao đã lưu LOG T-038 Phiên 2. Đoạn này chỉ ghi quyết định đã có; không tự ghi đề xuất snapshot/tách thành quyết định được duyệt. Quyền ghi DECISIONS vẫn cần Minh duyệt riêng như lời giao yêu cầu.
