# Phản biện T-040

- **Người phản biện:** Codex, phiên độc lập — **Ngày:** 17/10/2026 — **Commit/diff đã đọc:** commit gốc `25e71dc4`, git status và diff workspace hiện hành; T-040 và các nhánh nguồn chưa commit. Không quy mọi thay đổi workspace cho T-040.
- **Công đoạn/cổng và bản lượt:** soát kết quả; P5b, chuẩn bị G3; `REVIEW.md`. Claude vẫn là người làm, Codex vẫn là người phản biện.
- **Quyền lưu:** lượt phản biện ban đầu chỉ đọc và đã trả lời trong chat. Sau đó Minh nói nguyên văn: “Duyệt lưu bản phản biện và prompt bàn giao vào tasks/T-040-p5b-tong-hop/REVIEW.md để tôi chuyển cho Claude đáp, prompt cho claude cần chi tiết , tuân thủ rule để tôi dùng cho phiên claude mới. Cập nhật LOG hay STATE nếu có chỗ đang lệch,”. Lượt ghi nhận này tạo bản này, nối LOG T-040 và đồng bộ phần T-040 trong STATE theo quyền riêng đó; không đổi vai trò, sửa kết quả hoặc tự mở vòng phản biện mới.
- **Đã đọc:** AGENTS; STATE; SPEC và LOG T-040; phần mục tiêu/RQ3/RQ5/P5–P6/P9/G3 trong MRP; DT18 và hướng dẫn giảng viên; WHY, DECISIONS, LESSONS liên quan; code và đầu ra T-040, manifest và đầu ra nguồn T-034–T-039 liên quan; SPEC/LOG/REVIEW nguồn khi có; code do_thi/do_thi_tinh liên quan; B16 chỉ đọc. Tên file và đường dẫn đầu vào hiện hành tại `results/T-040/dau-vao.json`.
- **Tự soát độc lập:** đọc yêu cầu, code và đầu ra gốc trước kết luận các lượt trước; kiểm hash rồi tính trong bộ nhớ. Hai nhánh hỗ trợ nội bộ chỉ đọc kiểm tập và bàn giao, không là các vòng phản biện chính thức riêng và không ghi file.

## Kết luận chung

Có hai điểm CHẶN phần bàn giao P9 và một điểm KHÔNG CHẶN số hiện hành. Không tìm thấy lỗi tập, mẫu số, gom nhóm hoặc phép chiếu trong kết quả tổng hợp đã kiểm. Phần mô tả cấu trúc P5 đạt trong miền bằng chứng đã khai; chưa thể giữ nguyên nhận định toàn bộ bàn giao đã đạt tiêu chí xong khi R1/R2 còn chưa xử lý. T-040 chưa được nghiệm thu; không tự đóng P5/RQ3/RQ5/G3, chọn P6 hoặc mở test.

## Các điểm

### R1. So tổng trace với tổng request gateway không kiểm được độ đầy đủ — CHẶN tiêu chí R-08

- **Ở đâu:** `results/T-040/yeu-cau-quan-sat-p9.md:20`, R-08, cột Cách kiểm; `D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md:38–43`.
- **Sai gì:** yêu cầu “số trace khớp số request ở gateway” không xác định miền trace dùng để so, trong khi hệ thống chủ động tạo trace từ những nguồn ngoài request gateway. Dùng hai tổng cho toàn dữ liệu không kiểm được telemetry đầy đủ.
- **Bằng chứng:** B16 §3 quy định scheduler expiry/refund/delivery tạo trace riêng; consumer có thể dùng parent hoặc link, callback có trace mới. Phản ví dụ theo thiết kế: một request gateway và một lượt scheduler đều được ghi đầy đủ tạo hai trace nhưng chỉ một request gateway; nếu mất trace request mà còn trace scheduler thì hai tổng lại bằng nhau. Đây là phản ví dụ logic, không phải số runtime đã đo.
- **Xét phản chứng:** B16 §7 cho phép sampling 100% ở run hữu hạn; điều này không biến mọi trace nền thành request gateway. Nếu tác giả chỉ muốn đếm trace chứa gateway thì cần ghi rõ miền đó và khóa đối chiếu; câu hiện tại chưa quy định.
- **Bước và quyết định chịu ảnh hưởng:** lỗi đặc tả bàn giao đã có. Chặn dùng nguyên tiêu chí này để nghiệm thu độ đầy đủ đầu vào P9 hoặc suy độ phủ cạnh. Không chặn nhu cầu ghi sampling/drop/retention và không bác bỏ số graph dev của T-040.
- **Đề xuất sửa tối thiểu:** đối chiếu request nhận tại gateway với span SERVER gateway tương ứng theo khóa request/trace context trong cùng miền thời gian và chính sách sampling; kiểm trace callback/scheduler/consumer theo nguồn riêng. Không cần triển khai P9 hoặc thu runtime mới để sửa đặc tả này.

### R2. R-09 nâng ứng viên checkout→currency thành cơ chế đã xác nhận — CHẶN kết luận cơ chế trong căn cứ R-09

- **Ở đâu:** `results/T-040/yeu-cau-quan-sat-p9.md:21`, R-09; đối chiếu `results/T-040/bao-cao-p5b.md:85–90` §4.2, `results/T-040/con-mo.json#/items/6` (OM-07), `results/T-039/phan-tich-chenh-lech.md` G1.
- **Sai gì:** câu “OB checkout→currency cho thấy mất ngữ cảnh làm mất cạnh” nói như đã phân xử nguyên nhân, dù chính báo cáo và nguồn giữ đó là ứng viên chưa được xác nhận.
- **Bằng chứng:** `tong-hop.json#/lan_theo/OB_static_only_every_full_graph/rows/2` ghi thao tác phía gọi không xuất hiện và các lời gọi khác của checkout vẫn có. T-039 G1 dẫn code dùng `context.TODO()` cho RPC Convert, nhưng chưa chứng minh bản đó đã chạy khi thu dataset. Báo cáo T-040 §4.2 giữ OPEN về lời gọi có chạy, sampling và revision; OM-07 có `trang_thai=UNG_VIEN_DUOC_CUNG_CO`. Không có bằng chứng mới trong R-09 loại các giải thích cạnh tranh này.
- **Xét phản chứng:** đoạn phân tích §4.2 đúng là hỗ trợ ứng viên mất ngữ cảnh; điều đó chưa đủ chuyển thành nguyên nhân đã xác nhận. Nhu cầu nối trace mới của R-09 còn có căn cứ độc lập từ B16 §3 và không phụ thuộc việc chứng minh cơ chế OB.
- **Bước và quyết định chịu ảnh hưởng:** lỗi diễn giải đã xảy ra khi chuyển kết quả thành yêu cầu P9; chặn dùng R-09 làm bằng chứng cơ chế mất cạnh ở OB. Không chặn nhu cầu R-09 hoặc buộc giải quyết runtime OB trong T-040.
- **Đề xuất sửa tối thiểu:** ghi đúng mức “quan sát hỗ trợ ứng viên mất ngữ cảnh; chưa phân xử việc thực thi, sampling và revision”; giữ căn cứ thiết kế B16 riêng. Không cần đọc span thô hoặc chạy thêm để sửa câu vượt bằng chứng.

### R3. Danh sách mã quyết định cố định báo sai trạng thái nguồn khi chạy lại — KHÔNG CHẶN số snapshot hiện hành

- **Ở đâu:** `results/T-040/tong_hop.py:199–214`, `build_dau_vao()` tại dòng 966; `docs/DECISIONS.md` các dòng quyết định được lệnh dưới đọc.
- **Sai gì:** `decisions_mentions()` lấy mọi dòng nhắc T-038, rồi điều kiện `T038_no_acceptance_decision` chỉ cho một tập mã cố định. Một quyết định mới có nhắc T-038 không đồng nghĩa đã nghiệm thu task. Mã hiện hành chưa phân biệt nội dung hay loại quyết định.
- **Bằng chứng:** đã tái lập chỉ đọc bằng `py -3 -X utf8 -B -` với nội dung sau:

```python
import sys
sys.path.insert(0, "results/T-040")
import tong_hop as th
inputs = th.load_json("results/T-040/runs/tong-hop-007/dau-vao-kiem.json")
inputs["acceptance"]["T038_decisions_mentions"] = th.decisions_mentions("T-038")
out = th.build_dau_vao("read-only-reproduction", inputs)
print(inputs["acceptance"]["T038_decisions_mentions"])
print(out["kiem_trang_thai"]["T038_no_acceptance_decision"])
print(out["all_checks_pass"])
```

Kết quả tại lượt phản biện: danh sách `Q-159, Q-164, Q-169, Q-170, Q-171`; hai giá trị sau đều `False`. Q-170 và Q-171 đều nói chưa nghiệm thu T-038. Hàm trên chỉ tạo đối tượng trong bộ nhớ, không ghi file.

- **Xét phản chứng:** `tong-hop-007` là snapshot trước các quyết định nối sau; trạng thái đạt của snapshot lúc đó không bị bác bỏ bởi phép tái lập này. Số graph và tập/mẫu số hiện hành vẫn khớp. Việc Q-171 ghi nhận dừng phản biện gói sửa cũng không phải nghiệm thu toàn task.
- **Bước và quyết định chịu ảnh hưởng:** lỗi cài đặt đã tái lập ở phép kiểm trạng thái khi làm mới nguồn; có thể tạo đầu ra báo không đạt sai dù dữ liệu không đổi. KHÔNG CHẶN sử dụng số của snapshot `tong-hop-007` trong đúng giới hạn, nhưng phải xử lý trước khi dùng phép kiểm ấy để đánh giá trạng thái lần chạy mới.
- **Đề xuất sửa tối thiểu:** kiểm quyết định nghiệm thu được dẫn cụ thể hoặc tái lập với đúng ảnh chụp quyết định của lượt lịch sử; không suy nghiệm thu từ bất kỳ dòng mới nào nhắc task. Không chỉ mở rộng danh sách mã để che trường hợp vừa gặp. Đề xuất này chưa là lệnh sửa.

## Đối chiếu các lượt trước

- **Lượt Codex soát SPEC trong chat:** chưa kiểm được từng nhận xét, vì không có nội dung đầy đủ trong repo; không dựng lại từ tóm tắt.
- **S1 của Claude, phụ thuộc T-038:** đúng tại thời điểm tự soát Phiên 2. Bản sửa của người làm đã được tiếp nhận ở Phiên 3; graph gốc và model run sửa đồng bộ. Nguồn hiện hành sau đó có Q-171: dừng phản biện gói sửa, chưa nghiệm thu toàn T-038. Không áp trạng thái cũ “chưa kiểm độc lập” thành hiện trạng; giữ nó là ảnh chụp của run 007.
- **S2, trạng thái T-037/T-039 khác snapshot manifest:** đúng. Quyết định và REVIEW nguồn ghi nhận đóng; manifest dùng để kiểm byte, không thay nguồn quyết định. Không mở lại nghiệm thu các task đó.
- **S3, phụ thuộc T-035 và SMTP V2:** đúng theo nguồn đã đọc. Không suy việc các nhánh dùng được là các gói đã được nghiệm thu toàn bộ.
- **S4, yêu cầu P9 chưa ban hành:** đúng. R1/R2 không phải lý do ép triển khai P9 sớm; chúng là lỗi của chính nội dung đang đề xuất.
- **S5, typed T rỗng:** đúng khi tính độc lập toàn miền; giữ null/N/A, không lấp kiểu từ nguồn tĩnh.
- **Phản hồi nguồn T-038:** delta mô hình, phép chiếu, đồng bộ nguồn và kết quả đối chiếu hiện hành khớp phần tính đã kiểm. Nguồn Q-171 ghi nhận kết quả kiểm gói sửa và vẫn giữ OPEN ngữ nghĩa/runtime/lineage. Lượt T-040 không thay nghiệm thu nguồn hay xác nhận inventory ngữ nghĩa đầy đủ. Giới hạn lịch sử của T-039 đã được chấp nhận vẫn được giữ.

## Tuân thủ quy trình

- Vai trò không đổi: Claude người làm; Codex người phản biện. Lượt soát ban đầu không ghi file, không chạy main ghi đầu ra, không mở dữ liệu khóa/trace thô hoặc thu thực nghiệm mới.
- Trước dùng số đã kiểm hash theo manifest phù hợp. Ba lệch của pin R1 lịch sử T-036 đúng phần được V2 thay thế; pin và mã hiện hành khớp V2. Không thay hash cũ để hợp thức hóa nguồn.
- K6 lưu của run 007 đạt tại thời điểm ghi. Khi kiểm lại hiện tại, STATE, DECISIONS và LOG T-038 đã đổi sau snapshot theo những quyền riêng được ghi trong nguồn quyết định. Không dùng sự đổi metadata đó làm bằng chứng T-040 ghi ngoài quyền.
- Lượt lưu bản phản biện/đồng bộ hiện tại được Minh duyệt trực tiếp. Quyền này là ngoại lệ riêng cho reviewer nối mốc hành chính vào LOG và sửa metadata T-040 trong STATE; không truyền quyền sửa kết quả theo finding cho người làm và không đổi luật chung.
- Không sửa nội dung LOG lịch sử, SPEC, kết quả, code chung, quyết định khoa học hoặc manifest. Hash LOG/STATE nằm ngoài payload artifact của manifest vẫn là ảnh chụp trước mốc hành chính này; không sinh lại manifest chỉ để che khác biệt metadata.

## Điều đã kiểm và thấy đúng

Các kiểm dưới đã hoàn tất trong lượt phản biện chỉ đọc trước khi Minh duyệt lưu bản này; không gọi việc lưu tài liệu là thực nghiệm mới.

- Hash T-040: 106/106 artifact khớp `results/T-040/manifest.json#/files`. Các manifest nguồn T-034, T-035, T-037, T-038, bản sửa T-038, T-039 và pin V2 tương ứng khớp; lệch pin R1 lịch sử đã tách ở `dau-vao.json#/manifest`.
- Tính độc lập graph + mapping, không gọi hàm tổng hợp hoặc comparator để tự xác nhận: 1.201 graph, 2.402 views khớp S/T, giao/hiệu, members, exclusions, mẫu số và tỷ lệ; 28 nhóm họ×view khớp union, phần riêng tĩnh ở mọi graph, shape và thành viên. Nguồn đối chiếu: `results/T-040/runs/tong-hop-007/rows-TT.json.gz`, `rows-OB.json.gz`, `tong-hop-raw.json#/comparisons`, cùng summary và graph đầu vào theo `dau-vao.json#/ban_hien_hanh_dung`. Nhánh hỗ trợ chạy lệnh inline chỉ đọc `py -3 -X utf8 -B -` và báo các kết quả trên cho người phản biện; đây là tóm tắt kết quả kiểm, không phải bản stdout nguyên văn hoặc artifact run mới.
- Chiếu lại trực tiếp theo owner và cạnh thao tác: FT projection/entity-only 17/55; TT 122/48; OB 18/4. Nguồn số: `tong-hop.json#/he_thong/<FT|TT|OB>/mo_hinh_tinh/so_dem`, graph tại `dau-vao.json#/ban_hien_hanh_dung`. Không cộng các cửa sổ lặp thành bằng chứng độc lập.
- Lệnh inline chỉ đọc import `kiem_tra` và gọi K3/K3b/K4/K4b/K5 trả: K3 `checked=429, bad=[]`; K3b `checked=20, bad=[]`; K4 `entries=168, bad=[]`; K4b bắt được hai đột biến; K5 `bad=[]`. Không gọi `main()` ghi tệp. Các con trỏ số/chữ tại `so-lieu.json#/entries`.
- Không thấy chốt cơ chế P6, đưa nhãn vào phương pháp hoặc tự nhận lợi ích đồ thị. Bàn giao công khai những quan hệ còn giữ trong các đối chứng; việc chọn/cài/đánh giá vẫn thuộc P6/P7.

**Mức đạt SPEC và mục tiêu nguồn:** phần tập/số học, phân biệt miền bằng chứng, bàn giao ngữ nghĩa P6 và khai phần mục tiêu còn thiếu đạt trong phạm vi đã kiểm. Tiêu chí 1/2 về diễn giải và tiêu chí 5 về bàn giao P9 còn chịu R1/R2; không giữ nguyên kết luận đạt toàn bộ chỉ vì đủ tệp. Các câu lineage/runtime/lợi ích RCA còn OPEN không tự là lỗi hiện tại. R3 giới hạn khả năng làm mới trạng thái, không bác bỏ số snapshot.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm:** soát kết quả từ nguồn/đầu ra gốc rồi đối chiếu lịch sử; lưu bản phản biện đã báo trong chat và prompt bàn giao theo lời Minh duyệt. Không sửa thay người làm.
2. **File thay đổi:** lượt phản biện đầu không sửa file. Lượt lưu được duyệt: tạo `tasks/T-040-p5b-tong-hop/REVIEW.md`; nối LOG cùng task; sửa dòng và riêng các câu T-040 lỗi thời trong STATE. Không sửa file kết quả hoặc commit/push.
3. **Kiểm:** bằng chứng khoa học chỉ đọc ở mục trên đã hoàn tất. Trước lưu, kiểm lại 106 artifact T-040 khớp, chụp hash nguồn/tài liệu bảo vệ và phạm vi. Kiểm sau ghi gồm nội dung ba file, LOG nối thêm, STATE chỉ phần T-040, nguyên văn ba khối prompt, bảng phản hồi trống và bảo toàn file ngoài quyền; kết quả cuối ghi trong LOG sau kiểm.
4. **Bất đồng/phần thiếu:** R1/R2 còn chưa có phản hồi của người làm, chặn nội dung P9 tương ứng; R3 là lỗi trạng thái tái chạy, không chặn số hiện hành. Chưa có bất đồng giữa hai bên để tự suy đã thống nhất. Cần Claude đáp, rồi Minh quyết sửa gì. Runtime/lineage và lợi ích RCA vẫn cần bằng chứng ở các gói đã giao; không coi lưu REVIEW là nghiệm thu hoặc cấp quyền mở test.

**Đề xuất tiếp tục phản biện:** để Claude tự soát rồi đáp từng điểm và trình sửa tối thiểu. Chưa đề xuất dừng vì còn phản đối ảnh hưởng bàn giao P9. Nội dung nên giữ trong báo cáo chính thức: phân biệt ứng viên với cơ chế đã xác nhận, độ đầy đủ theo nguồn trace, và phạm vi phép đối chiếu tĩnh–trace.

**Đề xuất commit, chưa thực hiện:** `docs: record T-040 review and handoff`; chỉ ba file ghi nhận được duyệt, giữ riêng các thay đổi có sẵn của workspace. Commit/push cần Minh duyệt riêng.

## Prompt bàn giao cho người làm

Minh copy nguyên khối dưới sang phiên Claude mới. Đây là prompt trung tính: Prompt chung + Người làm đáp phản biện + G3 được trích nguyên văn từ `docs/review-prompt.md`, chỉ điền metadata. Bản phản biện là đầu vào cần kiểm, không phải lệnh sửa. Lượt Claude đáp hiện chỉ đọc/trả lời chat; Minh có thể cho quyền riêng trong phiên mới.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-040 — Tổng hợp P5b và bàn giao P6/P9; D:/RCA-flashticket/tasks/T-040-p5b-tong-hop/SPEC.md.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P5b, chuẩn bị G3.
- Người làm và người phản biện chính thức: Claude người làm; Codex người phản biện. Giữ phân công này trong phiên Claude mới.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; D:/RCA-flashticket/docs/STATE.md; D:/RCA-flashticket/tasks/T-040-p5b-tong-hop/SPEC.md và LOG.md; D:/RCA-flashticket/docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/review-prompt.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md. Các đường dẫn tương đối ở đây thuộc D:/RCA-flashticket. Nguồn task: SPEC/LOG và REVIEW nếu có trong tasks/T-034-g2-goi-trinh/, T-035-p5-do-thi-tu-trace/, T-036-p5b-hop-dong-chung/, T-037-p5b-flashticket/, T-038-p5b-trainticket/, T-039-p5b-online-boutique/. Nguồn hệ thống chỉ đọc: D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md. Commit gốc 25e71dc4; đọc git status và diff hiện hành, phân biệt thay đổi đã có với thay đổi của T-040. Xác định vai trò/quyền từ AGENTS, SPEC và quyết định trước; chưa dùng kết luận LOG/REVIEW thay tự soát đầu ra gốc.
- Phản biện và phản hồi trước: tự soát SPEC và lịch sử triển khai tại D:/RCA-flashticket/tasks/T-040-p5b-tong-hop/LOG.md Phiên 2, rồi Phiên 3; bản phản biện kết quả lượt này tại D:/RCA-flashticket/tasks/T-040-p5b-tong-hop/REVIEW.md; mốc lưu và bàn giao ở LOG.md Phiên 4. Nội dung lượt soát SPEC trong chat trước đây không có bản đầy đủ trên đĩa. Chỉ mở kết luận phản biện/phản hồi sau khi tự soát đầu ra gốc; không dựng lại nội dung chat còn thiếu.
- Code và kết quả liên quan: D:/RCA-flashticket/results/T-040/{tong_hop.py,kiem_tra.py,manifest.json,dau-vao.json,tong-hop.json,so-lieu.json,con-mo.json,bao-cao-p5b.md,ban-giao-p6.md,yeu-cau-quan-sat-p9.md,kiem-dung-dan.md,runs/}; lượt hiện hành runs/tong-hop-007/. Đầu vào T-034–T-039 theo dau-vao.json và manifest tương ứng; mã chung D:/RCA-flashticket/src/do_thi/ và src/do_thi_tinh/. Không chọn bản nguồn chỉ theo thời gian sửa file. Windows; Python dùng py -3 -X utf8 -B. Được đọc file, kiểm hash, tìm kiếm và tính lại trong bộ nhớ bằng chương trình inline không ghi file. tong_hop.py --run và kiem_tra.py --run ... --out đều ghi file: không chạy main của chúng trong lượt chỉ đọc. Lượt đáp phải dựa trên đầu ra gốc và bằng chứng thật; nếu cần thao tác ghi/chạy ngoài quyền để phân xử, trình đúng phạm vi và lý do trong chat.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat cho lượt Claude đáp này; chưa được Minh duyệt ghi bảng phản hồi REVIEW, nối LOG, sửa STATE hoặc sửa báo cáo/code/kết quả theo finding. Quyền Minh cho Codex lưu bản phản biện và đồng bộ metadata trong lượt trước không tự cấp quyền ghi cho Claude. Nếu Minh có chỉ định mới trong phiên Claude, chỉ ghi đúng file/phần được chỉ định; không suy quyền sửa kết quả từ việc chuyển prompt.

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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

## Phản hồi của người làm (người làm điền sau)

Để trống; không điền thay Claude hoặc suy quyết định sửa của Minh từ việc duyệt lưu bản phản biện. Khi có quyền ghi, người làm chỉ điền bảng này và các phần được Minh cho phép; không sửa nhận xét/prompt của reviewer. Thêm N1, N2… cho điểm tự tìm được, nêu CHẶN/KHÔNG CHẶN và bằng chứng. Cột Minh quyết để trống.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R1 | Đúng; CHẶN cách kiểm R-08 | B16 §3: scheduler, callback, consumer có link mở trace riêng, nên so tổng trace với tổng request gateway không kiểm được độ đủ. Phạm vi hẹp: chỉ cột cách kiểm R-08; không chạm số T-040. Đã sửa ở `yeu-cau-quan-sat-p9.md` R-08: đối chiếu từng request gateway (`requestId`, `traceId`, B16 §4) với đúng một span SERVER gateway; trace mở ngoài gateway đối chiếu với log có correlation; thiếu `traceId` thì ghi “chưa kiểm được”. Codex xác nhận hướng sửa ở lượt kiểm lại trong chat | |
| R2 | Đúng; CHẶN dùng R-09 làm bằng chứng cơ chế | Câu R-09 cũ nói như đã phân xử, trong khi báo cáo §4.2 và OM-07 giữ ứng viên. Grep: câu nói quá chỉ có ở R-09. Đã sửa căn cứ R-09 về mức ứng viên; nhu cầu R-09 giữ căn cứ riêng từ B16 §3. Phép kiểm của R-09 sửa cùng N4 | |
| R3 | Đúng (lượt đáp đầu ghi “đúng một phần” rồi rút lại); KHÔNG CHẶN số run 007 | Lỗi không chỉ ở tên trường: điều kiện cũ cho True cả khi xóa hết danh sách, nên không kiểm đầu vào còn nguyên. Đã thay bằng so hash các dòng DECISIONS nhắc T-038 với snapshot đã đọc (`runs/tong-hop-008/doc-quyet-dinh.json`); bắt được thêm, sửa, xóa, xóa hết (`runs/tong-hop-008/kiem-tra-002.json#/K5_guard/decision_tamper_caught`); khi lệch chỉ báo nguồn quyết định đã đổi, không suy nghiệm thu. Hash lịch sử không đổi | |
| N1 | Tự tìm; KHÔNG CHẶN | Trạng thái nguồn TT trong tệp xuất bản đã lỗi thời sau Q-171 (“chưa kiểm độc lập”). Đã cập nhật ở `tong_hop.py` (hằng `TT_STATUS_CODE`), `bao-cao-p5b.md`, `ban-giao-p6.md`, `con-mo.json` OM-01, `kiem-dung-dan.md`; run 007 giữ nguyên làm lịch sử. `so-sanh-007-008.json`: chỉ 7 chuỗi trạng thái đổi, mọi số giữ nguyên | |
| N2 | Tự tìm; chặn ghi “Đạt” tiêu chí 3 trước khi sửa | 120 khóa tĩnh TT không bao giờ quan sát chưa được lần theo. Run 008 phân loại 13/23/54/30 theo hai đầu và lần theo 13 cặp hai đầu quan sát được (`tong-hop.json#/lan_theo/TT_static_only_every_full_graph`): bốn nhóm ứng viên A–D ở báo cáo §4.3, OM-13. Giữ giới hạn Codex nêu: chỉ giống checkout→currency về dạng; 11 cặp có thao tác nguồn là candidate chưa xác minh, không gọi là span đã mất; đồng xuất hiện trong graph gộp không chứng minh cùng request; cơ chế OPEN | |
| N3 | Tự tìm; KHÔNG CHẶN | Số 6 đúng theo phân loại ưu tiên đích; đã làm rõ 3 cặp có cả hai đầu không xuất hiện và exporter là đầu nguồn (báo cáo §3.1); thêm ma trận hai đầu `OB_static_only_every_full_graph/endpoint_matrix` | |
| N4 | Tự tìm; CHẶN phép kiểm R-09 cũ (lượt đáp đầu ghi mức không nhất quán) | Đếm span không có cha không tách gốc hợp lệ, cha không có trong export và không thấy parent tại ranh giới phải truyền. Đã sửa R-09 thành ba trường hợp (a)–(c) theo danh sách ranh giới B16 §3; (b), (c) chưa đủ quy cơ chế, cần kiểm instrumentation, export, chuẩn hóa trong cùng miền thu; không miễn kiểm cả service. Đã bỏ câu “mọi SERVER phải có cha CLIENT” và câu “tức context không được truyền” theo lượt kiểm lại | |
