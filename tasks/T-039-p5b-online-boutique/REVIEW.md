# Phản biện T-039

- **Người phản biện:** Codex, phiên độc lập được Minh chỉ định thay Claude — **Ngày:** 16/10/2026.
- **Công đoạn/cổng và bản lượt:** soát kết quả T-039; P5, chuẩn bị G3; REVIEW.md.
- **Vai trò và quyền:** Codex phiên triển khai là người làm. Minh chỉ định phiên Codex độc lập làm người phản biện chính thức kết quả thay Claude; đây là ngoại lệ cho kết quả, khác ngoại lệ soát SPEC lịch sử. Lượt đánh giá ban đầu chỉ đọc, trả lời chat. Sau báo cáo, Minh duyệt ghi nhận phản biện, ngoại lệ phân công và đóng task. Giữ phân công lịch sử trong SPEC; không đổi vai thành người làm.
- **Đã đọc:** AGENTS.md, STATE; SPEC và các mục LOG liên quan của T-039; MRP phần mục tiêu/RQ3/RQ5/P5/P6/P9/G3; DT18 và hướng dẫn cô; WHY-52/53, DECISIONS, LESSONS; code src/do_thi_tinh và phần dựng T-035 chi phối đối chiếu; nguồn ứng dụng/metadata ghim, registry, coverage, bản ghi, mapping, graph, oracle, các báo cáo/runs và manifest T-039; hợp đồng/pin và lịch sử T-036; plan SMTP V2. Đối chiếu code, bản trước và đầu ra theo manifest; không nhận diff toàn workspace là thay đổi của riêng T-039.
- **Tự soát độc lập:** soát nguồn, bản ghi, mapping, code và đầu ra thật trước khi đối chiếu các nhận xét lịch sử. Không dùng LOG thay bằng chứng. Không dùng subagent, không mở dataset khóa hoặc repo RCA lưu trữ.

## Kết luận chung

Không phát hiện lỗi CHẶN mới trong kết quả tham chiếu hiện hành. Phần dựng/mapping/đối chiếu trong miền dev-adapter đã có bằng chứng kiểm; inventory toàn deployment và một phần lineage nguồn vẫn đạt một phần. Không suy từ kết quả này thành xác nhận nguyên nhân vật lý, telemetry đầy đủ, lợi ích RCA, chọn P6 hoặc khóa G3.

**Quyết định sau phản biện:** Minh nói nguyên văn: “Duyệt, chấp nhận giới hạn lịch sử và phần nguồn còn OPEN. Ghi nhận phản biện, ngoại lệ phân công và đóng T-039 giúp tôi; chưa duyệt G3 hay mở test.” Quyết định được lưu tại docs/DECISIONS.md, Q-165. T-039 đóng ngày 16/10/2026 với giới hạn lịch sử được chấp nhận và các câu nguồn còn OPEN. Đóng task không biến phần nguồn đạt một phần thành đầy đủ. Các manifest/SPEC/báo cáo triển khai giữ snapshot lịch sử trước nghiệm thu; trạng thái đóng hiện hành theo quyết định này, LOG và dòng T-039 trong STATE.

## Các điểm

### R1. Không còn byte đầu ra gốc của hai lượt lịch sử — KHÔNG CHẶN kết quả hiện hành

- **Ở đâu:** results/T-039/runs/khoi-phuc-lich-su-001/receipt.json, các con trỏ /rows/0 và /rows/1; results/T-039/kiem-dung-dan.md, phần báo cáo trước chuyển giữ làm lịch sử.
- **Sai gì:** runner đầu ghi đè đầu ra canonical mà chưa lưu riêng theo attempt. Đây là thiếu sót đã xảy ra đối với nghĩa vụ giữ mọi lượt chạy, không phải lỗi mới của comparator V2.
- **Bằng chứng:** /rows/0/reconstructed_graphs = 3 cho thuc-thi-snapshot-002; /rows/1/reconstructed_graphs = 132 cho thuc-thi-snapshot-003. Cả hai có /state = RECONSTRUCTED_NOT_ORIGINAL_BYTES. Tổng 135 là phép cộng hai trường này. Code retain_attempts.py và phần khai trong kiem-dung-dan.md xác nhận việc tái dựng, không chứng minh byte gốc.
- **Bước và quyết định chịu ảnh hưởng:** không thể kiểm nguyên trạng đầu ra hai lượt ấy; không được nhận bản tái dựng là bản gốc hoặc nói mọi đầu ra lịch sử còn nguyên byte. Không chặn dùng số hiện hành: archive lượt 004 giữ riêng, V2 có đầu ra riêng, và kết quả hiện hành đã được tính lại trong bộ nhớ khớp nội dung JSON.
- **Xét bằng chứng phản bác:** inputs, failures và bản tái dựng vẫn còn; thiếu sót đã được khai rõ và runner hiện lưu per-run outputs. Những điều đó giảm phạm vi ảnh hưởng, nhưng không khôi phục chứng cứ byte gốc đã mất.
- **Xử lý tối thiểu:** giữ nhãn tái dựng và giới hạn kiểm lịch sử; không cần chạy lại để giả làm bản gốc. Minh đã chấp nhận giới hạn lịch sử khi đóng task; không còn yêu cầu sửa chưa xử lý từ R1 đối với kết quả hiện hành.

## Đối chiếu các lượt trước

Chưa có REVIEW chính thức riêng của T-039 trước bản này. Những điểm dưới là nhận xét tự soát/sửa của người làm, không dựng thành các lượt phản biện chưa diễn ra.

- **A1, địa chỉ exporter ad/cart: đúng và đã sửa.** Source YAML dùng OTEL_EXPORTER_OTLP_ENDPOINT; ad dùng OTEL_SERVICE_NAME, cart dùng SERVICE_NAME. signals common:trace:adservice và common:trace:cartservice trong ban-ghi.json giữ đúng các biến đó. Không dùng địa chỉ cũ COLLECTOR_ADDR để suy lineage.
- **A2, capability MySQL exporter: đúng và đã sửa.** mysql_exporter.yaml khai DATA_SOURCE_NAME loopback; relation audit:mysqld-exporter-to-mysql giữ cạnh dữ-liệu/data với điều kiện exporter variant. Không xác nhận đã chạy hoặc đã tạo series dataset.
- **A3, binding DB logic–instance: đúng trong phạm vi nguồn cấu hình.** Hai binding tại ban-ghi.json#/resource_bindings giữ DB logic riêng, cùng mysql instance cấu hình và provenance URL/DSN/config liên quan. Không chứng minh init/provision hoặc physical host.
- **A4, gstatic preconnect: đúng và đã sửa.** header.html là resource hint; ban-ghi.json không còn relation common:asset:fonts.gstatic.com. Inventory vẫn giữ hint có điều kiện; không biến nó thành HTTP request.
- **Owner recommendation, binding trùng và alias candidate:** bản hiện hành giữ client ListProducts thuộc recommendationservice, handler→client nội bộ và client→productcatalog; hợp provenance hai binding logic thay vì nhân tài nguyên; prefix/SQL thiếu căn cứ không tự thành mapping verified. Các sửa phù hợp nguồn và không tối ưu mapping theo tỷ lệ giao.
- **Tiếp nhận SMTP V2:** nội dung JSON của mọi kết quả OB mới bằng kết quả cũ; khác byte do định dạng lưu. Không gọi đó là byte-identical. Nguồn/model/mapping giữ nguyên; unknown không được điền kiểu/channel từ nguồn tĩnh.

## Tuân thủ quy trình

Lượt phản biện ban đầu chỉ đọc và tính trong bộ nhớ với -X utf8 -B; không tạo REVIEW/LOG/STATE hay artifact run trước khi Minh duyệt. Không thấy bằng chứng ghi ngoài phạm vi của T-039 qua các bản trước, quyền trong LOG và gói V2 đã đọc; không nhận mọi thay đổi có sẵn trong workspace là của task. Giới hạn kiểm lịch sử nêu ở R1 được giữ nguyên.

Lượt ghi nhận đóng này là ngoại lệ được Minh duyệt trực tiếp: tạo REVIEW.md, nối docs/DECISIONS.md và LOG.md T-039, chỉ thay dòng T-039 của STATE. Đây là ghi nhận hành chính sau phản biện; không đóng vai người làm, không dựng phản hồi thay người làm và không mở thêm vòng review. SPEC, code, kết quả và manifest giữ nguyên. Không commit/push.

## Điều đã kiểm và thấy đúng

Các phép kiểm chỉ đọc đã chạy trong lượt phản biện, không phải thực nghiệm mới:

- Hash 5.667 mục T-035, 71 mục pin chung T-036 và 1.006 mục T-039 khớp ba manifest; pin và module live khớp snapshot ghim. Nguồn: các manifest tương ứng #/files và pin.json của T-039.
- Tính lại bằng Python trong bộ nhớ từ bản ghi/registry/mapping/graph đã giao: 132/132 kết quả khớp; lập lại độc lập khóa, giao/hiệu, members, exclusions, mẫu số, tỷ lệ, interval và conditional_reference. Nguồn số/đầu ra: results/T-039/doi-chieu/tong-hop.json#/graph_count và /rows; kết quả lệnh inline IN_MEMORY_REPLAY_AND_INDEPENDENT_ALL 132 PASS đã báo trong chat.
- So sánh độc lập V2 với baseline: 132 nội dung JSON bằng nhau, 0 cặp bằng nguyên byte do cách serialization khác nhau; không có thay đổi nội dung tương ứng. Kết quả lệnh inline: total=132, json_equal=132, byte_equal=0.
- 228 nguồn registry khớp hash; 215 blob ứng dụng đã đọc khớp Git blob của toàn cây snapshot. Bốn log.csv bị loại đúng danh sách, không mở nội dung. Nguồn: nguon.json#/sources; bao-phu-nguon.json#/rows; sources/metadata/ob-tree.json; kết quả inline REGISTRY_HASHES 228 True và SOURCE_TREE_BLOBS 215 MATCH.
- Nguồn số inventory hiện hành: doi-chieu/tong-hop.json#/record_counts gồm 23 entity, 68 operation, 82 relation, 2 binding và 53 signal declarations. Đây là khai báo có nguồn, không phải số kênh telemetry độc lập đã đo. /mapping_counts giữ 20 operation verified, 32 unverified và 3 unmapped; không gọi phần đủ mapping là toàn bộ trace.
- Typed loại unknown, giữ mẫu số trace bằng 0 và tỷ lệ null; endpoints không xác minh transport. API không nhận nhãn để chọn quan hệ; đồ thị dùng cho chiếu, chuẩn hóa và giao/hiệu tập, chưa tính điểm bất thường hoặc thứ hạng.
- Hash dependency của báo cáo phân tích lịch sử được đối chiếu với đúng bản summary trước V2 trong before/ và archive 004; không thay hash cũ bằng hash bảng hiện hành để hợp thức hóa nguồn.

## Mức đạt và câu hỏi nguồn còn mở

| Phần SPEC | Kết quả và giới hạn khi đóng |
|---|---|
| Registry/revision | Định danh snapshot và mức xác minh đã ghi; chưa nối app/build/image/deploy với dataset. |
| Inventory/coverage | Đủ phân hoạch cây đã định danh; inventory toàn deployment/library runtime mới đạt một phần, vẫn OPEN. |
| Dựng/mapping/đối chiếu | Có bằng chứng toàn miền graph dev được giao, tập/members/mẫu số/interval; chưa xác nhận runtime ground truth. |
| Giải thích chênh lệch | Có chuỗi nguồn→record→mapping→tập và match tương ứng; context.TODO/current-span rename chỉ là ứng viên giải thích dataset khi thiếu runtime lineage. |
| Miền/nguồn phụ/Node | Giữ miền dev-adapter; chưa xác nhận nguồn metadata độc lập hoặc Node là host. |
| Bàn giao/kiểm/lịch sử | Có báo cáo và đầu ra hiện hành đã kiểm; R1 là giới hạn lịch sử được Minh chấp nhận, không xóa dấu vết. |

Phần nhận tiếp được dẫn tại results/T-039/de-xuat-bo-sung-nguon.md, bao-phu-nguon.json#/external_source_questions và runs/doc-nguon-002/backend-source-audit.json#/open_items:

- **App→dataset/runtime:** cần commit build, image digest, effective deployment và collection version từ tác giả dataset/deployment qua Minh; ảnh hưởng nhận định inventory đầy đủ và quy cạnh thiếu cho telemetry. Chưa có exact artifact list/byte/chi phí để tự tải.
- **Naming/alias:** cần exact library/version/build identity và naming/filter paths trước nâng candidate; owner maintainer nguồn qua Minh. Ảnh hưởng lựa chọn mức/tín hiệu ở P6; không được tự strip prefix hoặc tạo SQL operation giả.
- **Metadata/Node:** cần producer/config/schema, nguồn đầu vào, aggregation/time policy và identity service–pod–instance–host từ tác giả collector/dataset; ảnh hưởng tính độc lập nguồn phụ và ánh xạ host ở P9. Không mở raw values/test để lấp thiếu.
- **Datastore/exporter:** cần init/image thực, scrape labels/schema và Redis target có nguồn; ảnh hưởng logical DB→instance→host/shared signal của P9. Collector mới không khôi phục dữ liệu lịch sử chưa từng ghi.

T-040 nhận mô hình tham chiếu và giới hạn; P6/P9 nhận đúng các nghĩa vụ còn mở, không nhận kết luận runtime hoặc lợi ích đã xác nhận. Không mở task mới, không tự cấp quyền bổ sung từ việc đóng T-039.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm:** lưu kết quả phản biện đã báo trong chat; ghi ngoại lệ Codex phiên độc lập phản biện kết quả thay Claude; lưu nguyên lời Minh chấp nhận giới hạn và đóng T-039.
2. **File thay đổi:** REVIEW.md T-039 mới; nối docs/DECISIONS.md và LOG.md T-039; chỉ thay dòng T-039 trong STATE. Không sửa SPEC, code, dữ liệu, kết quả hoặc manifest.
3. **Kiểm:** các kiểm khoa học chỉ đọc ở trên đã hoàn tất trước lời duyệt. Lượt ghi nhận đóng kiểm nội dung bốn file, append-only, dòng STATE, prompt nguyên văn, hash nguồn bảo vệ và diff; kết quả báo ở LOG/chat sau ghi. Không tạo run thực nghiệm.
4. **Bất đồng/phần thiếu:** không còn phản đối chưa xử lý chặn dùng kết quả tham chiếu hiện hành. R1 đã được Minh chấp nhận; các câu nguồn ở trên vẫn OPEN. Đóng task không đóng RQ3/RQ5/P5/G3, không chọn P6 hoặc mở test.

Đề xuất dừng phản biện đã được Minh chấp nhận qua quyết định đóng task. Không tự mở vòng khác. Nội dung nên vào báo cáo đồ án: nguồn tĩnh có điều kiện; inventory khác observed nodes; mẫu số sau mapping; unknown khác sai kiểu; giới hạn lịch sử và thiếu runtime lineage.

## Prompt bàn giao cho người làm

Lưu để giữ nghĩa vụ bàn giao; Minh chọn dùng khi chủ động giao lượt mới. Prompt này không tự mở lại task đã đóng hoặc cấp quyền sửa.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-039; D:/RCA-flashticket/tasks/T-039-p5b-online-boutique/SPEC.md; kết quả D:/RCA-flashticket/results/T-039/; trạng thái đóng theo docs/DECISIONS.md và LOG.md của task.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P5; chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex phiên triển khai là người làm; Codex phiên độc lập là người phản biện chính thức kết quả thay Claude theo ngoại lệ Minh chỉ định, ghi tại REVIEW.md và LOG.md của task. SPEC giữ phân công lịch sử. Phiên nhận prompt giữ vai trò người làm.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; docs/STATE.md; SPEC.md và LOG.md của T-039, gồm phụ lục; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; results/T-039/nguon.json và các nguồn được dẫn.
- Phản biện và phản hồi trước: D:/RCA-flashticket/tasks/T-039-p5b-online-boutique/REVIEW.md; lịch sử tại LOG.md và results/T-039/runs/; hợp đồng chung tại tasks/T-036-p5b-hop-dong-chung/REVIEW.md và LOG.md. Liệt kê lại thư mục trước khi tiếp nhận.
- Code và kết quả liên quan: D:/RCA-flashticket/src/do_thi/; src/do_thi_tinh/; results/T-035/manifest.json; results/T-036/runs/doi-chieu-smtp-001/manifest.json và snapshot được dẫn; results/T-039/manifest.json; results/T-039/runs/doi-chieu-smtp-001/{pin.json,checks/,diff.json}; quyền và kế hoạch tại docs/DECISIONS.md và results/T-038/runs/cap-nhat-goi-smtp-001/package/plan.json; Windows/Python 3.12, -X utf8 -B.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat nếu Minh chủ động giao lượt đáp; không tự mở lại task đã đóng. Chưa có quyền ghi REVIEW, LOG, STATE, SPEC, quyết định, code hoặc kết quả trong lượt đáp. Không chạy script ghi file, thực nghiệm mới, tải nguồn, bật EC2, mở dữ liệu khóa, dùng subagent hoặc tự mở/gửi chat. Có thể kiểm hash và tính lại trong bộ nhớ từ dữ liệu đã được phép đọc.

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

Không điền thay người làm và không dựng lượt đáp chưa diễn ra. Minh đã trực tiếp chấp nhận giới hạn và đóng task; quyết định ấy được ghi ở phần kết luận và DECISIONS, không dùng để giả lập một phản hồi của người làm.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
