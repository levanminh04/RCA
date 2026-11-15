# Nhật ký T-061

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối.

Minh duyệt SPEC ngày 11/11/2026 (chat: "t59 codex làm, t61 claude làm, ... nếu không có bất đồng quản điểm thì duyệt ghi"). SPEC do Claude ghi theo lời duyệt, sau hai lượt phản biện SPEC của Codex và một lượt đáp của Claude trong chat.

## Phiên 1 — 11/11/2026 — Claude — laptop Windows — người làm

Mở phiên theo AGENTS §6: đọc AGENTS, STATE, SPEC, LOG; `git status` (thư mục task T-058/T-059/T-061 và `docs/techstack/` chưa commit; chưa có `results/T-061/`). Không có đầu ra cũ để tiếp nhận.

### Tự rà trước khi viết schema/code

Hash: hai `method-output-1.json` và `rca-ban-dau.md` khớp `results/T-058/dem-2026-11-10/artifacts-sha256.json`. Khớp thêm `src/m1/adapter_flashticket.py` (bản lượt đêm), `m1-execution-plan-v2.json`, `ledger-received.jsonl` (hai file cuối chỉ dùng ở lớp phát lại).

Nguồn yêu cầu: DT18 (giao diện minh họa), MRP P10/Q-28 (báo sự cố → đồ thị con bất thường → danh sách nguyên nhân → giải thích), M6 (A trước, G2 do Minh làm), KE-HOACH-GIAI-DOAN-2 §7 G1 (vai trò 4 loại, xếp hạng, vùng, bằng chứng, liên kết), PLAN §5.2–5.3 (nhãn chỉ ghép sau khi băm). `DE-XUAT-HUONG-GRAFANA-RCA.md` §6.4/§7.2 là tham khảo (Q-188): màu, kích thước nút theo điểm, trace mẫu, đường lan truyền là ý tưởng, không phải yêu cầu. Tài liệu Grafana Node graph (bản latest): khung cạnh bắt buộc `id/source/target`; `highlighted` của cạnh đã bỏ từ 10.5 (dùng `color`).

Lần theo dữ liệu M1 (code `src/m1/chuoi.py`, `xep_hang.py`, `e7.py`, `span.py`):
- `extra/canh` = (chủ span cha, chủ span con), tức bên gọi → bên được gọi; quan sát N∪A; `so_canh_tinh`=0 ở cả hai ca nên mọi cạnh là quan sát. 8 cạnh, 7 thực thể có cạnh; 10 thực thể (DB, broker, cache, keycloak, mongodb) không có cạnh nào → hiện nút rời, không bịa cạnh (rủi ro SPEC đã nêu, nay xác nhận).
- `classes`: `tu_sinh` = tầng 1, `ke_thua` = tầng 2, `binh_thuong` = tầng 3, `thieu_du_lieu` = không có kênh OK.
- `entity_ranking[].tie_group` = chỉ số khối (hạng gọn); `key` = (3−tầng, max s, [m T4c], số kênh, Σs). Điểm `s` khác đơn vị giữa các kênh → không dùng làm kích thước nút.
- `region.T` = nhóm đứng đầu của khối đầu, **bất kể tầng**. Ca bình thường: `T` gồm cả 17 thực thể tầng 3, `cach_1/cach_2` rỗng. Nếu hiện `T` như "gốc vùng" sẽ sai nghĩa → quy tắc dẫn xuất: chỉ coi là gốc vùng khi `verdict=CAUSE_FOUND`; giữ nguyên `T` trong phần truy vết.
- Ca pause: M1 dự đoán api-gateway (tầng 1, nhóm 0), ticket-service (tầng 1, nhóm 1), config-discovery (tầng 2, nhóm 2), 13 thực thể đồng hạng nhóm 3; event-service `thieu_du_lieu`, không có trong `entity_ranking`. Vùng cách 1 {api-gateway, config-discovery}, cách 2 thêm ticket-service (nối qua config-discovery, vô hướng).
- `evidence_refs` = đơn vị của kênh có cờ ở thế giới P; chi tiết kênh ở `extra/kenh_co` (thực thể, kênh, hướng, lớp, s, khởi phát ns). `op|svc|tên` là tên span thô; `metric|<thực thể>_<kênh>` ứng với 7 truy vấn cố định của adapter.
- Thời gian: `window` tính ns; Grafana dùng ms.
- Mốc chế độ `a`: bộ chuyển đổi ghi cùng một câu "mốc tham chiếu do bộ điều phối cấp" cho mọi ca; không phân biệt ca bình thường/ca lỗi (phân biệt là nhãn).

Kết luận tự rà: không có lỗi nghiêm trọng hay điểm chặn trong SPEC; không sửa SPEC. Hai điểm cần quy tắc dẫn xuất (gốc vùng ở ca không có tầng 1; liên kết bằng chứng) được ghi trong tài liệu định dạng. Triển khai ngay.

### Các bước đã làm (phiên 1)

1. Kiểm hash đầu vào (mục tự rà ở trên). Đọc cấu trúc đầu ra M1 và code tạo ra từng trường.
2. Viết `results/T-061/chuyen-doi.py`, `schema.json`; chạy trên hai mẫu → `mau/c12e47ab.json`, `mau/f4a8c021.json`.
3. Viết `bam-mau.py` (băm mẫu → `mau/manifest-mau.json`) và `phat-lai.py` (ghép đáp án sau khi băm) → `mau/*.phat-lai.json`.
4. Viết `khung-grafana.py` (khung `nodes`/`edges` + provisioning, chỉ đọc định dạng). Chạy Grafana 13.3.0 cục bộ (container `t061-grafana`, 127.0.0.1:3061), nguồn TestData Raw frames. Hiển thị được cả bốn panel; ảnh và đo DOM ở `hien-thi/`.
5. Sau lượt xem đầu, rút ngắn chữ trong nút (chữ cũ bị cắt): "không bất thường" → "không cờ"; "nghi là nguồn" → "nghi nguồn"; số kênh chuyển sang menu chi tiết. Thêm `RANK_CHANGED`, `OBS_DEPENDENT` vào `do_phu` khi lập bảng phần tử M1 bị bỏ (ảnh hưởng cách hiểu độ ổn định hạng). Chạy lại toàn bộ đường; dashboard đang phục vụ trùng file hiện tại (đã so).
6. Viết `kiem.py` → `kiem-ket-qua.json`: 89/89 đạt. Ba lần hỏng trước đó đều là dương tính giả của phép kiểm cách ly (ghi ở `kiem-chuyen-doi.md` §6); bộ chuyển đổi không đổi vì chúng.
7. Viết `dinh-dang-ket-qua-rca.md` (trường, nguồn TT/DX, quy tắc D1–D9, phát lại, phần thiếu, đề xuất cấp dữ liệu G2), `kiem-chuyen-doi.md`, `kiem-hien-thi.md`.

### Kết thúc phiên 1 — báo cáo

**Đã làm.** Định dạng 0.1, schema, bộ chuyển đổi, lớp phát lại, hai mẫu và hai bản phát lại, khung Node graph, kiểm chuyển đổi và kiểm hiển thị thật trên Grafana 13.3.0 cục bộ.

**File thay đổi.** Mới: toàn bộ `results/T-061/` (danh sách: `git status results/T-061`). Sửa: `tasks/T-061-dinh-dang-ket-qua-rca/LOG.md` (ghi thêm), dòng T-061 trong `docs/STATE.md`. Container cục bộ `t061-grafana` đang chạy (xóa: `docker rm -f t061-grafana`). Không sửa SPEC, M1, `src/`, `exp-obs`, `exp-app`.

**Kiểm đã chạy.** `bash chay-tat-ca.sh && py -3 kiem.py` → 89/89 (`results/T-061/kiem-ket-qua.json` `/so_hong` = 0): schema 4/4 file; đối chiếu theo con trỏ trên cả hai ca; bốn điều phải giữ; phát lại không đổi dự đoán/hạng/vùng/màu (ở JSON, khung Grafana và DOM thật); cách ly nhãn; tất định trên `method-output-2.json`. Hiển thị: màu, nổi bật, chữ, danh tính 17 nút đo bằng DOM (`hien-thi/dom-mau.json`); menu chi tiết nút chạy; cạnh kiểm bằng mắt và rê chuột.

**Task đạt gì / câu hỏi nguồn trả lời tới đâu.**
- Câu 1–3 của SPEC: đạt trên hai mẫu. Câu 4: Node graph cục bộ hiện đúng hai mẫu qua TestData Raw frames.
- Với mục tiêu G1 của kế hoạch giai đoạn 2: định dạng đủ các trường đã duyệt; liên kết sang trace/metric chỉ ở mức truy vấn dẫn xuất, **chưa chạy trên kho `exp-obs`**; liên kết log không có (hai ca không có bằng chứng log). Trace mẫu không có nguồn (M1 không xuất).
- Chưa trả lời: Infinity hay PostgreSQL chạy được không (chưa thử); hiển thị trên `exp-obs` arm64; chế độ b; bằng chứng cạnh; `INSUFFICIENT_EVIDENCE`/`ERROR`.

**Điều cần Minh quyết (kèm đề xuất).**
1. Xác nhận định dạng đủ để bắt đầu G2 (tiêu chí xong cuối của SPEC). Đề xuất: bắt đầu G2 bằng đường "Raw frames nhúng dashboard" với hai mẫu (đã chứng minh, không cài gì); chọn Infinity hay PostgreSQL khi bắt đầu G3, sau một phép thử cục bộ ngắn. Lý do, mặt trái, phương án khác: `dinh-dang-ket-qua-rca.md` §7.
2. 10/17 thực thể không có cạnh (DB, broker, cache, keycloak, mongodb). Đề xuất: giữ nguyên ở 0.1 (không bịa cạnh). Nếu demo cần thấy service–DB: thêm cạnh tĩnh nét đứt ở lớp trình bày với `nguon_goc = tinh` — quyết định riêng vì khác với cạnh M1 dùng.
3. Vùng nghi ngờ tô theo cách 1 hay cách 2 ở G2. Đề xuất: tô cách 1 (chỉ gồm nút có giải thích E5), hiện cách 2 trong menu chi tiết; mặt trái: cách 1 không gồm ticket-service ở ca pause dù nó là tầng 1.
4. Đưa dashboard thử lên `exp-obs` (thêm nguồn TestData, nhập dashboard) là thay đổi trên máy, chưa làm, cần Minh duyệt nếu muốn.

**Chưa chắc.** Image Grafana 1,46 GB sau giải nén, lớn hơn ước lượng "vài trăm MB" của SPEC (dưới ngưỡng luật cứng 8). Truy vấn liên kết dẫn xuất chưa chạy trên kho thật. Menu chi tiết cạnh chưa mở được trong lượt thử.

**Bước tiếp theo chính xác.** Minh đọc `results/T-061/dinh-dang-ket-qua-rca.md` §7–8 và `kiem-hien-thi.md`; chuyển prompt dưới đây cho Codex (soát kết quả). Chạy lại: trong `results/T-061/`, `bash chay-tat-ca.sh && py -3 kiem.py`.

**Lệnh cuối đã chạy.** `py -3 kiem.py` → `89/89 đạt`; so dashboard Grafana đang phục vụ với `grafana/provisioning/dashboards/t061.json` → trùng.

### Prompt phản biện cho Codex (Minh chuyển; không tự gửi)

Prompt chung + khối "Soát kết quả" chép nguyên văn từ `docs/review-prompt.md`; khối trọng tâm cổng không áp dụng (SPEC: không có cổng riêng).

````text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-061, tasks/T-061-dinh-dang-ket-qua-rca/ (SPEC.md, LOG.md).
- Công đoạn: soát kết quả.
- Gói/cổng: P10, nhánh G (bước G1) của docs/techstack/KE-HOACH-GIAI-DOAN-2.md §7; không có cổng riêng.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex.
- Tài liệu gốc: tasks/T-061-dinh-dang-ket-qua-rca/SPEC.md; docs/techstack/KE-HOACH-GIAI-DOAN-2.md §7; docs/techstack/PLAN-TRIEN-KHAI.md §5; docs/DE-XUAT-HUONG-GRAFANA-RCA.md §6–7; results/T-058/dem-2026-11-10/rca-ban-dau.md; results/T-058/dem-2026-11-10/rca-ban-dau/outputs/c12e47ab/method-output-1.json và .../f4a8c021/method-output-1.json. File của task chưa commit (xem git status results/T-061 tasks/T-061-dinh-dang-ket-qua-rca docs/STATE.md).
- Phản biện và phản hồi trước: không có file (phản biện SPEC diễn ra trong chat).
- Code và kết quả liên quan: results/T-061/ (chuyen-doi.py, phat-lai.py, bam-mau.py, khung-grafana.py, kiem.py, chay-tat-ca.sh, schema.json, mau/, grafana/, hien-thi/, dinh-dang-ket-qua-rca.md, kiem-chuyen-doi.md, kiem-hien-thi.md, kiem-ket-qua.json); code M1 ở src/m1/; manifest đầu vào results/T-058/dem-2026-11-10/artifacts-sha256.json; manifest mẫu results/T-061/mau/manifest-mau.json. Lệnh chạy lại: trong results/T-061, bash chay-tat-ca.sh && py -3 kiem.py (Windows, Python 3.12 gọi bằng py -3, cần jsonschema). Cách chạy Grafana cục bộ: results/T-061/kiem-hien-thi.md §1.
- Phạm vi ghi được Minh cho phép trong lượt này: <Minh điền: chỉ trả lời trong chat, hoặc tasks/T-061-dinh-dang-ket-qua-rca/REVIEW.md>.

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

Công đoạn: soát kết quả.
Kiểm trên đầu ra thật, code và dữ liệu được phép; không tin tóm tắt LOG. Đối chiếu tiêu chí xong với phần mục tiêu nguồn và mức căn cứ cho bước tiếp theo; chạy lại phần rẻ khi trong quyền được duyệt.
Phân biệt hoàn thành task mô tả, xác nhận cơ chế và đủ căn cứ chọn/đánh giá thiết kế. Giới hạn đã khai không tự miễn phép kiểm cần thiết còn làm được.
Chỉ ghi bản phản biện lượt được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ bản cũ; không sửa kết quả thay người làm.
````

## Phiên 2 — 11/11/2026 — Claude — laptop Windows — người làm

Phản biện kết quả và các lượt trao đổi (chat 11/11/2026, Minh chuyển): Codex soát kết quả (5 điểm, điểm 1 CHẶN); Claude đáp (đúng cả 5; tự tìm N1 thiếu lớp thao tác theo WHY-52, N2 nguồn dom-mau.json, N3 dung lượng image/menu cạnh); hai vòng về lớp thao tác và gói sửa; Codex kiểm lại C/D, xác nhận C1–C5 đủ căn cứ, D2 cần sửa. Phát hiện ghi ngoài phạm vi ở phiên 1: `results/T-058/dem-2026-11-10/src/m1/__pycache__/adapter_flashticket.cpython-312.pyc` (tạo 18:00:16 khi importlib nạp adapter) và thư mục tạm Windows của `kiem.py`.

**Minh duyệt gói C ngày 11/11/2026** (chat: "Duyệt gói C"). Phạm vi: (1) xóa đúng file `.pyc` trên; (2) sửa `chuyen-doi.py`, `phat-lai.py`, `kiem.py`, `schema.json`, `khung-grafana.py`, `chay-tat-ca.sh` theo C1 (định dạng 0.2: OK, NO_EVIDENCE, ERROR, UNSUPPORTED; mốc lỗi từ `cases/<mã>/request.json`; chỉ chế độ a), C2 (phát lại kiểm đủ đợt theo `m1-launch-record.json` `/ids`), C4 (adapter nạp từ byte đã kiểm hash, file tạm trong `results/T-061/`, `-B`); (3) làm mới theo C5; (4) thử Infinity trong container `t061-grafana`, đổi ca A → B, bước đầu xác nhận máy chủ Grafana tải được JSON; (5) kiểm lại Raw frames trên 0.2; (6) sửa tài liệu; (7) LOG, STATE, prompt. Phần D (lớp thao tác) chưa duyệt.

### Các bước đã làm (phiên 2, gói C)

1. Xóa `results/T-058/dem-2026-11-10/src/m1/__pycache__/adapter_flashticket.cpython-312.pyc` và thư mục rỗng (hoàn tác ghi ngoài phạm vi phiên 1).
2. `chuyen-doi.py` → định dạng 0.2: nhận `--request` (`rca-ban-dau/cases/<mã>/request.json`); mã ca phải trùng thư mục file M1 và request; đọc byte một lần, kiểm hash trên chính chuỗi byte; adapter thực thi từ byte đã kiểm (không `.pyc`); OK/NO_EVIDENCE kiểm `t` khớp `/window/A/0`; ERROR/UNSUPPORTED → bản ghi tối thiểu, mốc từ request; chế độ khác a bị từ chối.
3. `schema.json` → 0.2 (bốn trạng thái, cửa sổ/verdict rỗng chỉ khi lỗi, `nguon.request`). `khung-grafana.py`: panel chữ in trạng thái, lỗi, verdict "—".
4. `phat-lai.py` viết lại: xử lý cả đợt theo `m1-launch-record.json` `/ids`, kiểm đủ đợt trước khi mở nguồn đáp án; không đạt thì in "Dừng trước khi mở nguồn đáp án" và trả mã 2.
5. `kiem.py`: `-B`, file tạm `tmp-kiem/`, thêm phép kiểm ràng buộc ca, mốc, chế độ, NO_EVIDENCE (dựng trong bộ nhớ), ERROR/UNSUPPORTED (sinh bằng `src/m1/chuoi.py::_ban_ghi_loi` qua `sinh-ban-ghi-loi.py` trong môi trường đã ghim `D:/RCA-ext/envs/py312-pin` + `T-016-cong-cu`), kiểm đợt (6 phép), không bytecode. Lần đầu 106/107: phép kiểm CLI phát lại hỏng vì thông báo stderr cp1252; bộ phát lại đã dừng đúng chỗ; sửa in qua stdout. Sau sửa **107/107**.
6. Làm mới theo C5: mẫu 0.2 → manifest mẫu → bản phát lại (đợt 2 ca) → khung → kiểm.
7. Thử Infinity: tạo lại container `t061-grafana` có `GF_PLUGINS_PREINSTALL_SYNC=yesoreyeram-infinity-datasource` (bản 4.1.6) và gắn `mau/` vào `/usr/share/grafana/public/t061`. Bước đầu: `docker exec … wget http://localhost:3000/public/t061/c12e47ab.json` trả đúng file (máy chủ Grafana tự tải được). Khai nguồn `infinity-t061`. `infinity-thu.py`: 13/13 phép kiểm phía máy chủ (parser backend đọc thẳng JSON 0.2, `root_selector` và selector lồng). Dashboard `t061-infinity` có biến `ca`: đổi `c12e47ab` → `f4a8c021` qua menu, bản ghi sự cố, nút, bảng hạng đổi đúng; DOM nút trùng bản Raw frames. Hai mẫu có cùng 8 cạnh nên không quan sát được cạnh đổi.
8. Kiểm lại Raw frames trên 0.2: DOM panel ca `f4a8c021` trùng phiên 1; panel chữ có thêm trạng thái.
9. Sửa tài liệu: `dinh-dang-ket-qua-rca.md` (0.2, §2.1, §2.2, D8, D10, §5, §6, §7 kết quả Infinity và đề xuất, §8), `kiem-chuyen-doi.md` (107/107, K_I_P/K_raw_P, đợt, ràng buộc ca, bản ghi lỗi, lỗi gặp), `kiem-hien-thi.md` (lệnh chạy mới, nguồn dom-mau.json, Raw frames 0.2, Infinity).

### Kết thúc phiên 2 — báo cáo

**Đã làm.** Toàn bộ gói C trong phạm vi Minh duyệt. Không làm phần D.

**File thay đổi.** Trong `results/T-061/`: sửa `chuyen-doi.py`, `phat-lai.py`, `kiem.py`, `schema.json`, `khung-grafana.py`, `chay-tat-ca.sh`, ba tài liệu; làm mới `mau/*`, `grafana/frames/*`, `grafana/provisioning/dashboards/t061.json`, `kiem-ket-qua.json`; mới `sinh-ban-ghi-loi.py`, `infinity-thu.py`, `infinity-ket-qua.json`, `grafana/provisioning/datasources/infinity.yaml`, `grafana/provisioning/dashboards/t061-infinity.json`, `hien-thi/08-…jpg`, `hien-thi/09-…jpg`, thư mục tạm `tmp-kiem/`. Xóa đúng một file `.pyc` ngoài phạm vi (hoàn tác). LOG này, dòng T-061 trong STATE. Container cục bộ tạo lại. Không sửa SPEC, M1, `src/`, `exp-obs`, `exp-app`. Các file `docs/WHY.md`, `docs/DECISIONS.md`, `docs/KE-HOACH-GIAI-DOAN-TOI.md` đang đổi trong working tree không do phiên này.

**Kiểm đã chạy.** `bash chay-tat-ca.sh && py -3 -B kiem.py` → 107/107 (`kiem-ket-qua.json` `/so_hong` = 0). `py -3 -B infinity-thu.py` → 13/13 (`infinity-ket-qua.json`). Không có `__pycache__` mới trong repo sau lượt kiểm.

**Task đạt gì / còn mở.**
- C1: bản ghi lỗi có hợp đồng và đã kiểm bằng hình dạng thật của M1; chưa có lượt M1 thật trả NO_EVIDENCE/ERROR/UNSUPPORTED, chưa vẽ bản ghi lỗi trên Grafana (OPEN; cần ngoại lệ "Không chạy lại M1" nếu muốn kiểm bằng fixture T-044).
- C2: phát lại kiểm đủ đợt trước khi mở đáp án — đạt.
- C3: Infinity đạt cục bộ, đọc thẳng JSON 0.2, đổi ca qua biến đạt. Chưa kiểm: bản arm64 của plugin, nơi đặt JSON và host cho phép trên `exp-obs`, danh sách sự cố động, menu chi tiết qua Infinity. Cạnh không đổi giữa hai mẫu nên phép đổi ca không chứng minh được cạnh đổi.
- Chế độ b chưa hỗ trợ (request.json không có trường chế độ).

**Cần Minh quyết (kèm đề xuất).**
1. Chọn nguồn dữ liệu cho G2: đề xuất **Infinity** (đã chạy với JSON sẵn có, không DB, đổi ca bằng biến). Mặt trái: cài plugin trên `exp-obs` cần duyệt, arm64 chưa kiểm, cần nơi đặt JSON. Chuyển PostgreSQL nếu plugin không cài được/không có arm64, hoặc danh sách sự cố động không làm được, hoặc cần lịch sử bằng SQL.
2. Duyệt cài Infinity trên `exp-obs` và chọn nơi đặt JSON (việc G2 của Minh hoặc task hạ tầng).
3. Phần D (lớp thao tác): SPEC sửa với D2 theo đề xuất đã trình, làm sau khi G2 đổi sự cố chạy được.
4. Kiểm xuyên suốt bản ghi lỗi bằng fixture T-044: đề xuất để OPEN tới khi G3 có ca thật.

**Bước tiếp theo chính xác.** Minh chuyển prompt dưới đây cho Codex (kiểm lại phản hồi và sửa). Chạy lại: trong `results/T-061/`, `bash chay-tat-ca.sh && py -3 -B kiem.py`; thử Infinity theo `kiem-hien-thi.md` §1 rồi `py -3 -B infinity-thu.py`.

**Lệnh cuối đã chạy.** `bash chay-tat-ca.sh && py -3 -B kiem.py` → `107/107 đạt`; `py -3 -B infinity-thu.py` → 13 dòng ĐẠT.

### Prompt cho Codex — kiểm lại phản hồi và sửa (Minh chuyển; không tự gửi)

Prompt chung và khối "Kiểm lại phản hồi và sửa" chép nguyên văn từ `docs/review-prompt.md`; T-061 không có khối cổng.

````text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-061, tasks/T-061-dinh-dang-ket-qua-rca/ (SPEC.md; LOG.md mục "Phiên 2", gồm phạm vi gói C Minh duyệt và báo cáo kết thúc phiên 2).
- Công đoạn: người phản biện kiểm lại phản hồi và sửa.
- Gói/cổng: P10, nhánh G (bước G1) của docs/techstack/KE-HOACH-GIAI-DOAN-2.md §7; không có cổng riêng.
- Người làm và người phản biện chính thức: Claude làm, Codex phản biện.
- Tài liệu gốc: tasks/T-061-dinh-dang-ket-qua-rca/SPEC.md; docs/techstack/KE-HOACH-GIAI-DOAN-2.md §7; docs/techstack/PLAN-TRIEN-KHAI.md §5; docs/DE-XUAT-HUONG-GRAFANA-RCA.md §6–7; docs/WHY.md WHY-52. File T-061 chưa commit; xem git status results/T-061 tasks/T-061-dinh-dang-ket-qua-rca và dòng T-061 trong docs/STATE.md.
- Phản biện và phản hồi trước: các lượt trong chat ngày 11/11/2026 giữa Codex và Claude (soát kết quả, đáp, lớp thao tác, gói C/D), tóm tắt ở đầu mục "Phiên 2" của LOG T-061.
- Code và kết quả liên quan: results/T-061/ (chuyen-doi.py, phat-lai.py, bam-mau.py, khung-grafana.py, kiem.py, sinh-ban-ghi-loi.py, infinity-thu.py, chay-tat-ca.sh, schema.json, mau/, grafana/, hien-thi/, kiem-ket-qua.json, infinity-ket-qua.json, dinh-dang-ket-qua-rca.md, kiem-chuyen-doi.md, kiem-hien-thi.md); src/m1/; results/T-058/dem-2026-11-10/ (artifacts-sha256.json, m1-launch-record.json, rca-ban-dau/cases/, rca-ban-dau/outputs/). Windows, Python 3.12 (`py -3 -B`, jsonschema); môi trường M1 D:/RCA-ext/envs/py312-pin với PYTHONPATH D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages; Grafana cục bộ 13.3.0 với Infinity 4.1.6 theo results/T-061/kiem-hien-thi.md §1.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.
````

**Minh duyệt ngày 11/11/2026** (chat: "duyệt theo đề xuất"): (1) sửa §7 `dinh-dang-ket-qua-rca.md` — bỏ điều kiện "lịch sử và chấm lại bằng SQL", việc chấm giữ bằng script đọc file đã băm; (2) thử file chỉ mục danh sách sự cố cho Infinity trên Grafana cục bộ. Điều kiện chuyển PostgreSQL: plugin không cài được/không có arm64 trên `exp-obs`; danh sách sự cố bằng file chỉ mục không dùng được; hoặc G3 sinh sự cố liên tục tới mức file không quản lý nổi.

### Phần thêm của phiên 2 — file chỉ mục danh sách sự cố (theo duyệt "duyệt theo đề xuất")

1. Mới `chi-muc.py`: sinh `mau/chi-muc/danh-sach-su-co.json` chỉ từ mẫu đã băm (kiểm byte theo manifest mẫu, không đọc bản phát lại); thư mục con nên không lẫn vào manifest mẫu và kiểm đợt. `chay-tat-ca.sh` gọi sau `bam-mau.py`.
2. `infinity-thu.py`: thêm truy vấn danh sách và panel bảng có liên kết `var-ca=${__value.raw}` ở cột mã. Phía máy chủ 15/15 (`infinity-ket-qua.json`). Giao diện: đang ở `f4a8c021`, bấm `c12e47ab` mở đúng sự cố; ảnh `hien-thi/10-…`, `11-…`.
3. `kiem.py`: thêm 3 phép kiểm chỉ mục → **110/110**.
4. Sửa `dinh-dang-ket-qua-rca.md` §7 (danh sách bằng file chỉ mục; việc chấm không làm trong Grafana; điều kiện chuyển PostgreSQL theo duyệt; bảng phương án), `kiem-chuyen-doi.md`, `kiem-hien-thi.md`.

Lệnh cuối: `bash chay-tat-ca.sh && py -3 -B kiem.py` → 110/110; `py -3 -B infinity-thu.py` → 15/15. Prompt phản biện ở trên (mục "Prompt cho Codex — kiểm lại phản hồi và sửa") vẫn dùng được; phạm vi kiểm gồm cả phần thêm này.

**Đề xuất việc tiếp theo (Minh quyết):**
1. Codex kiểm phiên 2 của T-061 (prompt ở trên). Sau đó Minh nghiệm thu T-061 theo tiêu chí "Minh xác nhận định dạng đủ để bắt đầu G2".
2. Claude phản biện bản T-059 đã ghi (prompt ở LOG T-059) — đang chặn việc 2i/B4.
3. Minh dựng bố cục G2 trên dashboard `t061-infinity` cục bộ.
4. Một việc hạ tầng nhỏ (cần Minh duyệt, thay đổi trên máy): kiểm Infinity có bản arm64, cài trên `exp-obs`, chọn nơi đặt JSON mà Grafana trên `exp-obs` gọi tới được.
5. Sau khi G2 đổi sự cố chạy được: trình sửa SPEC T-061 phần D (lớp thao tác) với D2 đã sửa.
6. G3 (dịch vụ RCA trực tuyến ghi định dạng 0.2 và chỉ mục) theo kế hoạch, sau luật cảnh báo chặng 3.

## Nghiệm thu — 11/11/2026

**Minh nghiệm thu T-061 ngày 11/11/2026** (chat: "duyệt T59 61, dọn dẹp STATE cho đúng và nghiệm thu"). Nghiệm thu khi Codex **chưa kiểm** phiên 2 (gói C, file chỉ mục); kết quả tự kiểm 110/110 và Infinity 15/15 là của người làm. Phần D (lớp thao tác) chưa duyệt, không thuộc phạm vi nghiệm thu. OPEN giữ nguyên như `dinh-dang-ket-qua-rca.md` §6.

**Minh duyệt việc 4** (chat: "duyệt việc 4"; "Claude làm luôn, không gọi lại Codex T58 nữa"): cài Infinity 4.1.6 trên `exp-obs` theo kế hoạch đã trình trong chat (sao lưu và sửa `pinned/compose.json` phần grafana: biến cài plugin ghim phiên bản, gắn `/opt/flash-ticket-obs/rca-ket-qua` vào `public/rca` chỉ đọc; thêm `pinned/provisioning/datasources/infinity.yaml`; chỉ tạo lại container grafana; chép hai mẫu và file chỉ mục, không chép bản phát lại; ghi cấu hình trước/sau và hash vào `results/T-061/exp-obs/`). Đổi hash cấu hình ghim của T-058 do Claude tự ghi nhận trong repo, không báo Codex.

### Việc 4 đã làm — 11/11/2026

- Cài Infinity 4.1.6 (`gpx_infinity_linux_arm64`) trên `exp-obs`, nguồn `infinity-rca`, dữ liệu mẫu ở `/opt/flash-ticket-obs/rca-ket-qua/` (hai mẫu + chỉ mục, không bản phát lại). Chỉ container Grafana tạo lại (14:50:57Z). Kiểm: health ok, plugin đã đăng ký, nguồn được nạp, máy chủ Grafana tải được JSON, bộ nhớ 340,6/768 MB. Biên bản, hash trước/sau, hoàn tác: `results/T-061/exp-obs/README.md`.
- Sự cố: lần `docker compose up` đầu thiếu `-p`, tạo network rỗng `pinned_default` rồi dừng do trùng tên container (container cũ không bị đụng); đã xóa network đó, chạy lại với `-p flash-ticket-obs-pinned`.
- Chưa kiểm: truy vấn Infinity thật trên `exp-obs` (cần đăng nhập; Minh kiểm trên giao diện).
- Hash cấu hình ghim T-058 đổi `c6be32e0…` → `684d39bd…`: ghi trong biên bản và mục "Lưu ý cho mọi agent" của STATE; không báo Codex theo lệnh Minh.
- Dọn `docs/STATE.md` theo lệnh Minh: còn 47 dòng; task đã nghiệm thu chuyển vào mục lục (thêm T-042…T-056, T-059, T-061); sửa dòng "dữ liệu khóa" và "P6" đã cũ; gom các nghiệm thu khi chưa kiểm lần cuối thành một dòng lưu ý; mọi liên kết kiểm tồn tại.
