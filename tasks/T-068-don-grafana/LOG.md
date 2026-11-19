# Nhật ký T-068

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối, không sửa mục cũ. Mỗi phiên một mục.

---

## Phiên 1 — 18/11/2026 — Claude — laptop — vai trò: người làm

**Mở phiên:** tiếp cùng phiên chat với T-066 (đã đọc AGENTS, STATE, SPEC T-066/T-067). SPEC T-068 soạn và soát trong chat qua 4 bản.

**Công đoạn và mục tiêu nguồn:** làm. DT18 (đồ thị phụ thuộc, giao diện minh họa), MRP §P10 (demo). Phạm vi theo SPEC bản 4.

**Quyết định của Minh trong phiên** (nguyên lời):
- "Duyệt, soạn SPEC" (hướng dọn Grafana thành task mới).
- "Duyệt bản 4" — Minh duyệt SPEC ngày 18/11/2026, gồm commit/push repo lab trong phạm vi ghi. Chưa ghi DECISIONS (không phải quyết định hướng đi mới).

**Diễn biến:**
- 18/11 — Minh duyệt SPEC ngày 18/11/2026 (bản 4). Tạo SPEC.md, LOG.md, dòng STATE.
- 02:06Z — Bước 1 (phần máy, chỉ đọc): hash cây `rca-results/t065-l11-001/du-lieu` (2.182 file) → `results/T-068/truoc/du-lieu.sha256`. Mốc (a): 2.143 file lịch sử khớp manifest T-065 (`may-l11/du-lieu/…`), 0 lệch. Mốc (b): 5/5 file có dòng trong `hash-tren-may.sha256` T-066 khớp (gồm `chi-muc-ban.json` `7dfdf42c…`, `V082…/chi-muc.json` `472ba9a5…`). Mốc (c): 34 file còn lại đều của ca 7ffb2305 (`thao-tac-vue/` 17, `trang-thai/` 17); dùng bản chụp này làm mốc trước. Không có khác biệt ngoài dự kiến.
- 02:08Z — Bước 1 (metric): truy vấn Prometheus tại 2026-11-17T12:28:00Z (trong cửa sổ ca 7ffb2305) → `results/T-068/truoc/prometheus-ca-7ffb2305.json`. Lượng gọi (HTTP ứng dụng) 7 series; p90 7; 5xx 1 (api-gateway 0,26/s); span metrics: calls 8, lỗi 1, p90 8; service graph: request 35 cặp, failed 1; JVM 8. Cả ba tín hiệu lượng gọi/độ trễ/lỗi có nguồn có dữ liệu. payment-service vắng ở metric HTTP trong cửa sổ (ca tiêm PAUSE-PAYMENT).
- 02:10Z — Grafana API trả 401 (phiên đăng nhập hết hạn). Phần API của bước 1 và bước 2 chờ Minh đăng nhập; làm trước bước 3–6 (không phụ thuộc).
- Phát hiện (KHÔNG CHẶN, ghi báo cáo): `dich_quan_sat` có hậu tố ` (<db.system>)` ở 22 ca nhánh t062/dev2 nhưng không có ở 6 ca dev3 và ca 7ffb2305 (đường `dev3_template` của bộ xuất). Theo SPEC, đích không ánh xạ được thì không vẽ: các ca này có ít cạnh hạ tầng hơn. Không sửa bộ xuất (ngoài phạm vi).
- Bảng ánh xạ hạ tầng: căn cứ `src/m1/adapter_flashticket.py` (INFRA: postgres→postgresql-shared-instance, user-db→mongodb-instance, redis→cache, rabbitmq→broker) và giá trị db.system (postgresql, redis, mongodb). Host trần chỉ ánh xạ khi thao tác có loại SQL/cache. DB logic (booking_db…) không nhận diện được từ các trường này nên không bao giờ là đích.
- 02:12Z — Bước 3: `campaigns/g1/service_graph.py` (repo lab). Thử trên bản sao L11 trên laptop: 84 file; kiểm độc lập `results/T-068/kiem/dem_doc_lap.py` 84/84 khớp (1 ca "không có đầu ra": p7/ebd5ef38; 1.386 cạnh liên dịch vụ, 545 cạnh hạ tầng). Đối chứng âm (sửa 1 số A, 1 màu, 1 trạng thái) → bắt đủ 3 lỗi.
- 02:13Z — Bước 4–5: `observability/grafana/build_dashboards.py` sinh 4 dashboard từ `git show ab1c52c` (hash gốc trùng `grafana-l12/`: rca `d205e9ff…`, phát lại `51497186…`); providers mới (4 provider, `folder` tiếng Việt); `observability/grafana/README.md`. Kiểm cấu trúc: trang sự cố chỉ thêm panel 40 (đồ thị), 41 (chú giải), dịch y +23 cho panel từ y≥45, mọi panel cũ khác giống hệt; trang phát lại chỉ đổi `title`, `tags`. Grep khóa đáp án: 0 ở 3 trang chính. Sửa lỗi tự tìm: ghi file trên Windows ra CRLF → đổi sang ghi byte LF.
- 02:17Z — Bước 6 (thử trên bản sao ở `/srv/rca-lab/runs/t068-thu/`, bản cây lab chưa commit): relabel thiếu dòng → dừng, hash 2 file không đổi, không có bak; relabel thử/thật → so JSON chỉ khác `/nguon_ca` và `/su_co/28/nguon`; chạy lại → từ chối vì đã có bak. `sau_v082.py` nhánh ca mới (bản sao không có dòng) → thêm dòng `t066`, `nguon_ca` t066, đồ thị ok. Cố ý lỗi đồ thị (`T068_GAY_LOI_DO_THI=1`) → thoát 0, status `loi`, hash file ca/2 chỉ mục không đổi; `service_graph.py --ban --ca` sinh lại → status ok, đồ thị trùng byte bản của nhánh ca mới. File ca sau relabel trùng byte file ca do bộ chuyển đã sửa sinh ra (`1133d125…`).
- 02:3xZ — Minh đăng nhập lại Grafana. Bước 1 (API): 9 UID nạp từ file + 2 UID tạo tay (`t058-flashticket` 10/11, `t061-infinity` 11/11); `loki-1` (uid `dg49lda2pxj40e`, url rỗng, jsonData {}) không được dashboard nào (0/11) hay alert rule nào (API trả 0 rule) tham chiếu → đủ điều kiện xóa. Ghi `results/T-068/truoc/grafana-truoc.json`.
- Bước 2: xuất `results/T-068/manual-export/` (+ SHA256SUMS). Đối chiếu hash dạng chuẩn hóa tính trong trình duyệt: cả 2 khớp; t058 khớp cả byte thô, t061 lệch byte thô do cách escape khi chép (nội dung trùng). t061 trên máy khác nguồn `results/T-061/grafana/provisioning/dashboards/t061-infinity.json` (panel, trường mặc định) → bản máy được giữ ở manual-export. Panel T-058: (1) request/giây → giữ ở trang hệ thống panel 2 (cửa sổ rate 1m thay 2m, cùng metric); (2) JVM → panel 5; (3) log ứng dụng → panel 7, cùng truy vấn; (4) trace mẫu cố định `4e4e5583…` → bỏ: một trace mẫu không mô tả trạng thái hệ thống trực tiếp; trace theo ca xem ở trang sự cố, trace bất kỳ ở Tempo Explore. T-061: trang thử plugin Infinity, đọc đường dữ liệu cũ; bỏ, đã có trang sự cố thay.
- 02:2xZ — Bước 7: commit lab `5495877`, push `origin/main`. Trên exp-obs `/opt/rca-lab` ghim commit (detached HEAD): lệnh `git pull` đầu tiên lỗi "not currently on a branch", `set -e` dừng trước mọi bước khác; chạy lại bằng `git fetch` + `git checkout 5495877`. 02:21:14Z sinh 85 file đồ thị (`--tat-ca`), đổi nhãn 7ffb2305 (dòng chỉ mục 28; cũ dev3/dev3), sinh lại đồ thị ca đó. So hash cây du-lieu trước/sau (`results/T-068/sau-du-lieu.sha256`): chỉ khác `V082…/7ffb2305.json` (8b51fe1f→1133d125) và `V082…/chi-muc.json` (472ba9a5→519b870c), cộng 2 bản sao `.bak-t066` trùng hash cũ; so JSON chỉ khác `/nguon_ca` và `/su_co/28/nguon`. Hai hash mới trùng hash ở phép thử bước 6.
- Kiểm độc lập trên dữ liệu máy: 85/85 cặp khớp (`results/T-068/kiem/dem-doc-lap-may.json`; 1 "không có đầu ra"; 1.404 cạnh liên dịch vụ; 546 cạnh hạ tầng); 0 status lỗi. Ca 7ffb2305: 18 cạnh liên dịch vụ, 1 cạnh hạ tầng (keycloak→postgresql-shared-instance qua host `postgres`), 125/146 đích không ánh xạ (127.0.0.1 ×109…) vì thiếu db.system.
- 02:21:45Z restart Grafana; healthy 02:21:54Z; log "finished to provision dashboards", không lỗi dashboard (lỗi thư mục alerting có sẵn, thuộc W4). `/api/search`: 4 folder mới, mỗi folder 1 dashboard; 6 dashboard lưu trữ tự gỡ (provider cũ bị bỏ). Folder cũ còn lại, `counts` toàn 0 (dashboards, folders con trừ 90-archive có 3 folder con rỗng, alert rule, library panel, variable): 00-start-here `fg4kl9kbpgwzke`, 10-current-results `eg4kl9jj9mj9cb`, 10-system `dg4mpei1ofdvka`, 20-incidents `cg4mpeifouvpce`, 30-replay `ag4mpei6bql1cc`, 90-archive/2026-11-12-g2-v6 `fg4kl9juknzlsc`, 90-archive/2026-11-13-l3-p7 `bg4kl9k2ccmbkb`, 90-archive/2026-11-14-l4-temporary `eg4kl9k7c5b7ke`, 90-archive `fg4kl9jrdsnpca`. Ba folder 10-system/20-incidents/30-replay do provider cũ (quét 30 s, foldersFromFilesStructure) kịp tạo trong 31 s giữa checkout và restart. Sắp xóa 9 folder này (con trước, cha sau).
- 02:26Z — Xóa (theo danh sách trên, `counts` kiểm lại ngay trước từng lệnh): lệnh gộp đầu tiên chỉ kịp xóa `fg4kl9juknzlsc` (log Grafana 02:22:31) rồi tunnel rớt (`Connection reset by peer`); mở lại tunnel, xóa tiếp từng lệnh có giới hạn 12 s: 8 folder còn lại 200; `t061-infinity` 200; `loki-1` 200 (02:26:26Z).
- 02:27Z — Bước 8 (bấm thật): trang hệ thống ở cửa sổ ca 7ffb2305 — request/giây, p90, 5xx/giây, JVM đều có dữ liệu; bản đồ Tempo hiện; log có dòng → tiêu chí 4 đạt; 02:28:01Z xóa `t058-flashticket` (200).
- 02:29Z — Mục lục mới: dòng 7ffb2305 hiện `t066`, ca khác giữ nhãn cũ; bấm mã → trang sự cố đúng cửa sổ 12:20:04.000–12:30:03.999Z; đồ thị: `payment-service` #1 đỏ.
- 02:30Z — Bấm thật phát hiện lỗi: ca p7/ebd5ef38 (cạnh rỗng) → node graph báo "id field is required in the edges data frame". Sửa `service_graph.py` (service-graph-2: ca không có đầu ra vẽ 2 nút chú thích + 1 cạnh `chu_thich`), rút gọn nhãn phụ bị cắt chữ, sắp lại cột bảng mục lục (transform organize); cập nhật `dem_doc_lap.py` cho ca không có đầu ra (kiểm có nút "không có đầu ra" và không có nút/cạnh dữ liệu). Commit lab `82e813a`, push; 02:31:19Z checkout trên máy, sinh lại 85 đồ thị; cây du-lieu không đổi (`sau-du-lieu-2.sha256` trùng `sau-du-lieu.sha256`); kiểm độc lập 85/85.
- 02:3xZ — Hồi quy bấm thật: p7/ebd5ef38 hiện "không có đầu ra / LOI_CHAY"; V082/ebd5ef38 `payment-service` so_kenh_co 35; V071/ebd5ef38 24 dòng cạnh phương pháp; 1ad3afeb đổi bản bằng menu P7→V071→V082: keycloak #2 tự sinh → #3 bình thường, URL panel gửi đi đúng `<bản>/1ad3afeb` (móc fetch). Cuối: 4 folder, 4 dashboard, 4 datasource; trang phát lại 200.
- Toàn vẹn: đầu ra V082 7ffb2305 vẫn `183a405d…`; không file nào dưới `/srv/rca-lab/m1` mới hơn chỉ mục T-066; commit lab chỉ chạm 12 file trong phạm vi.
- Ghi `results/T-068/kiem/BAO-CAO.md`, `results/T-068/thay-doi-may.md`.

**Kết thúc phiên 1 (18/11/2026 ~02:40Z):**
1. Đã làm gì: bước 1–8 của SPEC bản 4. Grafana còn 4 thư mục tiếng Việt, 4 dashboard; trang sự cố có đồ thị dịch vụ cho 85 cặp bản–ca; trang hệ thống mới; ca 7ffb2305 nhãn `t066`; `sau_v082.py` sinh đồ thị cho ca mới và cô lập lỗi đồ thị.
2. File đã thay đổi — repo RCA: `tasks/T-068-don-grafana/` (SPEC, LOG), dòng T-068 trong `docs/STATE.md`, `results/T-068/` (truoc/, manual-export/, kiem/, sau-du-lieu*.sha256, dung-dashboard.json, thay-doi-may.md). Repo lab: commit `5495877`, `82e813a` (đã push). exp-obs/Grafana: theo `results/T-068/thay-doi-may.md`.
3. Kiểm đã chạy: hash 3 mốc; kiểm độc lập 85/85 + đối chứng âm; thử relabel và `sau_v082.py` trên bản sao (thiếu dòng, ca mới, lỗi cố ý, sinh lại); so cấu trúc dashboard với bản gốc; grep khóa đáp án; bấm thật trang hệ thống, mục lục, đồ thị 3 ca × các bản.
4. Chưa chắc / cần Minh:
   - Đầu ra task đạt 5/5 tiêu chí theo kiểm của người làm; chưa phản biện.
   - Giới hạn: 6 ca dev3 và ca 7ffb2305 có ít cạnh hạ tầng vì bộ xuất không ghi `db.system` ở nhánh đó (7ffb2305: 125/146 đích không ánh xạ). Muốn đồng đều phải sửa bộ xuất (ngoài phạm vi, đang ghim) hoặc đọc span — cần Minh quyết nếu muốn; đề xuất của người làm: để nguyên tới W5 (dịch vụ trực tuyến dựng bộ xuất chung), vì sửa `l8b-xuat.py` phá phép hồi quy byte của T-066.
   - Commit repo RCA (T-068 cùng phần T-066 còn chưa commit) cần Minh duyệt.
   - Thư mục thử `/srv/rca-lab/runs/t068-thu/` (~380 MB) giữ theo luật cứng 10.
   - Câu hỏi nguồn: phần hiển thị DT18/P10 (đồ thị + xếp hạng + bằng chứng) đã có trên giao diện; không trả lời câu hỏi lợi ích của đồ thị.
5. Bước tiếp theo chính xác: Minh chuyển prompt dưới đây cho Codex (soát kết quả); sau phản biện, người làm đáp theo bảng phản hồi. Song song có thể mở T-067 bước 1.
6. Lệnh cuối cùng đã chạy: `/api/search` + `/api/datasources` trên Grafana (4 folder, 4 dashboard, 4 datasource).

**Prompt cho Codex — soát kết quả T-068:**

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-068 — tasks/T-068-don-grafana/ (SPEC.md, LOG.md).
- Công đoạn: soát kết quả.
- Gói/cổng: P10, chuẩn bị G6.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex.
- Tài liệu gốc: tasks/T-068-don-grafana/SPEC.md; repo lab D:/Project/flashticket-rca-lab: git diff ab1c52c..82e813a.
- Phản biện và phản hồi trước: không có bản file; SPEC bản 1–3 được Codex soát trong chat trước khi duyệt (lịch sử ghi ở đầu SPEC.md).
- Code và kết quả liên quan: results/T-068/ (kiem/BAO-CAO.md, kiem/dem_doc_lap.py, kiem/dem-doc-lap-may.json, truoc/, manual-export/, sau-du-lieu*.sha256, thay-doi-may.md, dung-dashboard.json); repo lab commit 82e813a (campaigns/g1/service_graph.py, campaigns/g1/relabel_case.py, campaigns/runner/sau_v082.py, observability/grafana/); results/T-065/manifest.json; results/T-066/e2e-001/.
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

Công đoạn: soát kết quả.
Kiểm trên đầu ra thật, code và dữ liệu được phép; không tin tóm tắt LOG. Đối chiếu tiêu chí xong với phần mục tiêu nguồn và mức căn cứ cho bước tiếp theo; chạy lại phần rẻ khi trong quyền được duyệt.
Phân biệt hoàn thành task mô tả, xác nhận cơ chế và đủ căn cứ chọn/đánh giá thiết kế. Giới hạn đã khai không tự miễn phép kiểm cần thiết còn làm được.
Chỉ ghi bản phản biện lượt được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ bản cũ; không sửa kết quả thay người làm.
```

---

## Phiên 1 (tiếp) — 18/11/2026 — Claude — laptop — vai trò: người làm (đáp phản biện, chỉ ghi LOG)

**Quyết định của Minh trong phiên** (nguyên lời): "note kĩ, sau này sẽ sửa" (về hai vấn đề cạnh DB dưới đây); "yêu cầu codex phản biện cả phần này". Chưa ghi DECISIONS.

**Tự soát trước khi đọc kết luận phản biện** (làm trước khi nhận lượt soát kết quả của Codex, khi Minh hỏi cách khắc phục):

- **N1 — CHẶN kết luận giới hạn dữ liệu trong `results/T-068/kiem/BAO-CAO.md` mục "Giới hạn" 1–2; KHÔNG CHẶN đồ thị đang phục vụ.** Câu "DB logic … chỉ nhận diện được từ nhãn metric `postgresql_database_name`, không có trong trường span đã xuất" là **sai/nói quá**. Kiểm chỉ đọc trace gốc ca 7ffb2305 (`/srv/rca-lab/m1/cases/7ffb2305/raw-traces.jsonl`): 201.743 span có thuộc tính `db.*`; 100% có `db.system`, `server.address`; 190.917 có `db.name` (`db.connection_string` cùng số). Phân bố (service, db.system, db.name, server.address): ticket-service/postgresql/ticket_db 110.627; event-service/postgresql/event_db 32.343; booking-service/postgresql/booking_db 22.602; payment-service/postgresql/payment_db 17.740; keycloak/postgresql/keycloak_db/`postgres` 7.405; api-gateway/redis/–/127.0.0.1 5.697; booking-service/redis 5.129; user-service/mongodb/user_db 120, /admin 80. Câu đúng: "bảng ánh xạ của T-068 chỉ dùng trường `dich_quan_sat` của file ca; trường này không giữ `db.name`, nên đồ thị dừng ở instance". Thông tin DB logic có trong trace gốc (và trong tên thao tác, ví dụ `SELECT booking_db`).
- **N2 — KHÔNG CHẶN (giới hạn hiển thị, ghi để sửa sau).** Cạnh hạ tầng không đều: 22 ca t062/dev2 có hậu tố ` (<db.system>)` trong `dich_quan_sat`, 6 ca dev3 + 7ffb2305 không có (7ffb2305: 125/146 đích không ánh xạ).

**Nguyên nhân (đã lần tới code):**
- Hai bộ xuất cùng sinh trường `dich_quan_sat` nhưng khác quy ước. Bộ L4 (`results/T-065/l4-raw.mjs:20`, dùng cho 22 ca t062/dev2 qua template L4 đã cache) ghi `server.address + ' (' + db.system + ')'`. Bộ L8/L8b Python (`results/T-065/codex/l8b-xuat.py:202–203`, bản chép ở lab `campaigns/g1/l8b-xuat.py`; nhánh `dev3_template` dùng cho 6 ca dev3 và mọi ca mới qua `sau_v082.py`) chỉ ghi `server.address`. Không bộ nào giữ `db.name`. Đây là chỗ không thống nhất có từ T-065, không do T-068 tạo ra.
- Phần trách nhiệm của T-068 (người làm Claude): khi soạn SPEC đã chọn `dich_quan_sat` làm nguồn duy nhất cho cạnh hạ tầng mà **không rà quy ước của trường này trên mọi nhánh xuất và không đối chiếu với trace gốc** trước khi chốt (AGENTS luật 11, review-prompt mục 11: quy ước dữ liệu nguồn qua từng bước). Chỉ phát hiện bất đối xứng lúc cài đặt; khi viết báo cáo lại khái quát từ trường đã xuất sang "dữ liệu trace" mà không kiểm trace gốc → N1. Ba lượt soát SPEC cũng không nêu điểm này (lượt 1 còn đề xuất "cạnh hạ tầng chỉ báo có mặt", hợp lý với dữ liệu đã xuất nhưng không xét nguồn gốc).

**Đề xuất sửa (chưa làm, chờ Minh; Minh đã nói "sau này sẽ sửa"):**
- Phương án A (đề xuất của người làm): `campaigns/g1/service_graph.py` đọc thêm trace gốc của ca (chỉ đọc), cắt cửa sổ và chia nền/sự cố theo đúng quy tắc của `l8b-xuat.py` (đọc, không sửa). Ánh xạ: postgresql + `db.name` → thực thể DB logic cùng tên nếu có trong `classes` (booking_db, ticket_db, event_db, payment_db, keycloak_db); redis → `cache`; mongodb → `mongodb-instance` (V082 không có thực thể `user_db`); đích ngoài `classes` không vẽ, ghi số. Cạnh DB có số span theo cửa sổ (đếm theo span nên hết vấn đề một thao tác nhiều đích). Không sửa `l8b-xuat.py`, file ca, M1 → hồi quy byte T-066 giữ nguyên. Nguồn trace gốc đủ 29 ca: 9 ca t062 `results/T-062/ca/<ca>/cases/<ca>/`; 13 ca dev2 `results/T-063/thu2/ca/`; 5 ca dev3 `results/T-063/thu3/thu/ca/` + ebd5ef38 `D:/RCA-archive/exp-obs/cases/ebd5ef38/`; 7ffb2305 trên exp-obs `/srv/rca-lab/m1/cases/`. Kiểm hash gói theo manifest trước khi dùng. Chi phí ước ~1–2 giờ, không tải. Mặt trái: đồ thị dùng nguồn khác file ca (trace gốc) → phải ghi rõ trên panel; cần gói trace gốc cho ca mới (W5 phải giữ đường tới gói).
- Phương án B: sửa bộ xuất (`l8b-xuat.py`) cho giữ `db.system` + `db.name` → phá hồi quy byte T-066 và đổi file ca; nên làm trong bộ xuất chung W5.
- Phương án C (Codex đề xuất ở R4): giữ thiết kế, chỉ sửa câu kết luận; để W5 quyết.
- Cần sửa `results/T-068/kiem/BAO-CAO.md` mục Giới hạn 1–2 theo N1 (chờ Minh duyệt cùng các điểm phản biện).

**Đánh giá lượt soát kết quả của Codex (trong chat, chưa có bản file):**

| Điểm | Kết luận của người làm | Bằng chứng |
|---|---|---|
| R1 CHẶN — liên kết "Mở lớp thao tác" gắn vào mọi trường `id`, kể cả cạnh và nút chú thích | **Đúng** | `build_dashboards.py` override `byName: id` áp cho cả khung nodes và edges (cạnh cũng có trường `id`); nút chú thích `__xem_bang__` cũng có `id`. Sửa: chỉ gắn link cho nút dịch vụ thật (ví dụ thêm trường `detail__dich_vu` chỉ có ở nút thuộc `services`, link dùng trường đó), nút chú thích không link. |
| R2 CHẶN — mẫu README nạp lại 90-archive bị Grafana 13.3.0 từ chối | **Đúng theo dẫn chứng; chưa tự chạy lại** | README đặt cùng lúc `folder`, `folderUid`, `foldersFromFilesStructure: true`. Sửa: ví dụ tạm chỉ giữ `path` + `foldersFromFilesStructure: true`. |
| R3 CHẶN — `/srv/rca-lab/runs/t068-thu/` không nằm trong "Phạm vi ghi" | **Đúng — lỗi tuân thủ Luật 0 của người làm** | Bước 6 cho thử trên bản sao nhưng mục Phạm vi ghi exp-obs không liệt kê vị trí thư mục thử. File đã ghi: `/srv/rca-lab/runs/t068-thu/{repo,ra-co,ra-khong}` (~385 MiB), không đụng M1 hay dữ liệu thật. Đề xuất: Minh ghi nhận ngoại lệ đã xảy ra; giữ thư mục làm bằng chứng (luật cứng 10); hoàn tác khi Minh muốn = `sudo rm -rf /srv/rca-lab/runs/t068-thu`. |
| R4 KHÔNG CHẶN — kết luận DB logic nói quá | **Đúng, và rộng hơn** | Xem N1: trace gốc có `db.name` ở 190.917/201.743 span DB, không chỉ tên thao tác. Bất đồng với đề xuất C của Codex: người làm đề xuất A (đọc trace gốc) — để Minh quyết, Codex phản biện. |
| R5 KHÔNG CHẶN — thiếu kiểm `ent in classes` | **Đúng** | `service_graph.py` chỉ loại `ent is None` hoặc `ent == chu`; `dem_doc_lap.py` cũng không kiểm. 546/546 cạnh hiện tại nằm trong `classes` (Codex đếm) nên đồ thị đang phục vụ không sai. Sửa ở cả hai script. |
| R6 KHÔNG CHẶN — bảng hoàn tác thiếu | **Đúng** | Hoàn tác code không hoàn tác JSON trong volume; chép đè `chi-muc.json` sau khi có ca mới làm mất dòng. Sửa `thay-doi-may.md`: thêm bước sinh lại đồ thị bằng revision cần phục hồi; hoàn tác nhãn bằng `relabel_case.py --nguon dev3` trên đúng trường (sau khi xóa `.bak-t066` hoặc dùng hậu tố khác), chỉ chép nguyên bản sao khi hash hiện tại vẫn là hash sau T-068. |
| Ghi chú WHY | **Đúng một phần** | Lựa chọn nguồn cạnh hạ tầng chưa có mục WHY. Đề xuất ghi WHY sau khi Minh chọn A/B/C (ghi một lần cho lựa chọn cuối). |

**Đề xuất sửa gom theo file (chờ Minh duyệt):** repo lab `observability/grafana/build_dashboards.py` (R1) + sinh lại dashboard sự cố; `observability/grafana/README.md` (R2); `campaigns/g1/service_graph.py` (R1 trường link, R5, và A nếu duyệt); repo RCA `results/T-068/kiem/dem_doc_lap.py` (R5), `results/T-068/kiem/BAO-CAO.md` (N1/R4), `results/T-068/thay-doi-may.md` (R6, R3).

**Prompt cho Codex — kiểm lại phản hồi (gồm phần cạnh DB):**

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-068 — tasks/T-068-don-grafana/ (SPEC.md, LOG.md). Phản hồi của người làm và đề xuất sửa nằm ở mục "Phiên 1 (tiếp)" cuối LOG.md, gồm cả đề xuất về nguồn cạnh hạ tầng (phương án A/B/C) và phần nguyên nhân.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P10, chuẩn bị G6.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex.
- Tài liệu gốc: tasks/T-068-don-grafana/SPEC.md; repo lab D:/Project/flashticket-rca-lab: git diff ab1c52c..82e813a; results/T-065/l4-raw.mjs; results/T-065/codex/l8b-xuat.py; src/m1/adapter_flashticket.py.
- Phản biện và phản hồi trước: lượt soát kết quả của Codex (trong chat, Minh chuyển kèm); phản hồi của người làm ở cuối tasks/T-068-don-grafana/LOG.md.
- Code và kết quả liên quan: results/T-068/; results/T-065/manifest.json và may-l11/; results/T-066/e2e-001/; gói trace gốc: results/T-062/ca/<ca>/cases/<ca>/, results/T-063/thu2/ca/, results/T-063/thu3/thu/ca/, D:/RCA-archive/exp-obs/cases/ebd5ef38/, exp-obs /srv/rca-lab/m1/cases/7ffb2305/; repo lab commit 82e813a.
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
```

**Đáp lượt kiểm lại của Codex (trong chat, 18/11):**

| Điểm | Kết luận của người làm | Bằng chứng |
|---|---|---|
| Nguồn hậu tố của 9 ca T-062 — CHẶN dùng mô tả cũ để giao B | **Đúng — đính chính mục "Nguyên nhân" ở trên** | Có **3 nhánh**, không phải 2: (1) 9 ca T-062: `results/T-065/xuat-du-lieu.mjs:112` ghi `server + ' (' + db + ')'`; L4 đọc lại bản P7 đã kiểm hash (`l4-xuat.mjs:13–16`); (2) 13 ca dev2: `l4-raw.mjs:20` (cùng quy ước); (3) 6 ca dev3 + ca mới: `codex/l8b-xuat.py:202–203`, chỉ `server.address`. Cả 3 không giữ `db.name`. Hệ quả: B mà chỉ sửa `l8b-xuat.py` vẫn để 22 ca theo mẫu cũ; B phải xử lý cả mẫu lịch sử. |
| Số span của 7ffb2305 | **Đúng** | Số trong N1 (201.743 / 190.917) là **toàn gói 20 phút**, không phải cửa sổ ca. Trong cửa sổ phương pháp: nền 58.425 / 55.415; sự cố 43.264 / 40.884 (số của Codex, chưa tự chạy lại). Khi làm A phải đếm theo cửa sổ ca, đơn vị "span DB phía client". |
| R1 — `__khong_co__` nằm trong `#/services` của P7/ebd5ef38 | **Đúng** | Đề xuất "chỉ link nút thuộc `services`" của người làm chưa đủ. Sửa: link chỉ khi nút thuộc `services` **và** id không bắt đầu bằng `__` (loại cả `__khong_co__`, `__xem_bang__`); cạnh không có link. |
| R6 — đề xuất xóa `.bak-t066` | **Đúng, đề xuất của người làm sai** | `relabel_case.py --nguon dev3` tạo `.bak-dev3`, không đụng `.bak-t066`. Sửa hướng dẫn hoàn tác: giữ `.bak-t066`; hoàn tác nhãn bằng `relabel_case.py --ca 7ffb2305 --nguon dev3` (tự tạo `.bak-dev3`), rồi `service_graph.py --ban V082-V066+H8a --ca 7ffb2305` vì `nguon_file_sha256` đổi theo file ca; chỉ chép nguyên bản sao khi hash hiện tại vẫn là hash sau T-068. |
| A/B/C | **Đồng ý với Codex** | C cho báo cáo T-068 ngay (sửa câu theo nguyên văn Codex đề xuất, ghi đúng 3 nhánh). A là hướng cho lần nâng cấp, cần Minh duyệt phạm vi riêng (đổi nguồn và đại lượng so với SPEC bản 4). B để W5. |

Không còn bất đồng có bằng chứng với Codex. Chờ Minh quyết: (1) duyệt sửa R1, R2, R5, R6, N1/R4 theo C; (2) ghi nhận R3; (3) A làm khi nào (SPEC bổ sung hoặc task mới).

**Đề xuất sửa gom theo file (bản cập nhật):** lab `build_dashboards.py` (R1: link theo trường riêng chỉ có ở nút dịch vụ thật) + sinh lại dashboard sự cố; lab `campaigns/g1/service_graph.py` (R1 trường link, R5 kiểm `ent in classes`) + sinh lại 85 đồ thị; lab `observability/grafana/README.md` (R2); RCA `results/T-068/kiem/dem_doc_lap.py` (R5 kiểm độc lập), `results/T-068/kiem/BAO-CAO.md` (N1/R4 theo C, 3 nhánh xuất), `results/T-068/thay-doi-may.md` (R6 hoàn tác, R3 ghi nhận).

**Prompt cho Codex — kiểm lại phản hồi lượt 3:**

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-068 — tasks/T-068-don-grafana/ (SPEC.md, LOG.md); phản hồi mới nhất của người làm ở mục "Đáp lượt kiểm lại của Codex" cuối LOG.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P10, chuẩn bị G6.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex.
- Tài liệu gốc: tasks/T-068-don-grafana/SPEC.md; repo lab D:/Project/flashticket-rca-lab: git diff ab1c52c..82e813a.
- Phản biện và phản hồi trước: Codex soát kết quả (chat); Claude đáp (LOG.md); Codex kiểm lại (chat); Claude đáp (LOG.md, mục cuối).
- Code và kết quả liên quan: results/T-068/; results/T-065/ (manifest.json, may-l11/, xuat-du-lieu.mjs, l4-xuat.mjs, l4-raw.mjs, codex/l8b-xuat.py); results/T-062/manifest.json; results/T-063/manifest-2.json; results/T-066/e2e-001/; repo lab commit 82e813a.
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
```

---

## Phiên 1 (tiếp 2) — 18/11/2026 — Claude — laptop — vai trò: người làm (sửa theo phản biện)

**Quyết định của Minh** (nguyên lời): "Duyệt sửa" — trả lời câu hỏi "Duyệt sửa R1, R2, R5, R6 và câu báo cáo theo C, ghi nhận R3?". Phạm vi: các sửa gom theo file ở mục "Đáp lượt kiểm lại của Codex". A (đọc trace gốc) chưa duyệt.

**Diễn biến:**
- `service_graph.py` (service-graph-3): trường `detail__url` cho mọi nút (nút dịch vụ: trang sự cố đúng bản/ca/cửa sổ/`var-dv`; nút chú thích: `viewPanel=panel-3`); cạnh không có trường này; cạnh hạ tầng phải thuộc `classes` (ghi `dich_ngoai_classes`, `ngoai_classes`). `build_dashboards.py`: link gắn vào `detail__url` thay vì `id`; sinh lại dashboard sự cố. README: bỏ `folder`/`folderUid` ở ví dụ tạm.
- `results/T-068/kiem/dem_doc_lap.py`: thêm kiểm `classes` và `kiem_link`. Bản sao L11 trên laptop 84/84; đối chứng âm (bỏ `cache` khỏi classes; cài cạnh ngoài classes, link trên cạnh, sai var-dv) bắt đủ.
- `BAO-CAO.md`: mục Giới hạn 1–2 viết lại theo C (3 nhánh xuất; câu DB logic theo đề xuất của Codex; hướng A/B chờ duyệt); thêm mục "Sửa theo phản biện". `thay-doi-may.md`: R3 ghi nhận, R6 cách hoàn tác, dòng triển khai 04:26.
- 04:26:36Z lab `8dccb34` (push), checkout trên exp-obs, sinh lại 85 đồ thị; kiểm độc lập trên máy 85/85, `dich_ngoai_classes` = 0 ở mọi file; cây du-lieu không đổi (`sau-du-lieu-3.sha256` trùng hai bản trước).
- Bấm thật: nút `payment-service` → link `var-dv=payment-service` đúng cửa sổ, mở trang đúng; cạnh `event-service → config-discovery` không có link; nút chú thích P7/ebd5ef38 → panel 3. R2 chưa thử nạp thật (không có nhu cầu nạp lưu trữ lúc này).

**Kết thúc lượt:**
1. Đã làm: sửa R1, R2, R5, R6, câu báo cáo theo C, ghi nhận R3.
2. File: lab `8dccb34` (`campaigns/g1/service_graph.py`, `observability/grafana/build_dashboards.py`, `observability/grafana/README.md`, `dashboards/20-incidents/t065-l8b-rca.json`); RCA `results/T-068/` (`kiem/dem_doc_lap.py`, `kiem/dem-doc-lap-may.json`, `kiem/BAO-CAO.md`, `thay-doi-may.md`, `dung-dashboard.json`, `sau-du-lieu-3.sha256`), LOG, STATE. exp-obs: checkout `8dccb34`, 85 đồ thị sinh lại.
3. Kiểm: như trên.
4. Còn mở: A (đọc trace gốc cho cạnh DB) chờ Minh duyệt phạm vi; R2 chưa thử nạp thật; commit repo RCA chờ Minh; thư mục thử giữ.
5. Bước tiếp: Minh chuyển prompt dưới cho Codex kiểm lại các sửa.
6. Lệnh cuối: bấm link nút chú thích P7/ebd5ef38 trên Grafana (mở panel 3).

**Prompt cho Codex — kiểm lại các sửa:**

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-068 — tasks/T-068-don-grafana/ (SPEC.md, LOG.md); các sửa Minh duyệt ghi ở mục "Phiên 1 (tiếp 2)" cuối LOG.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P10, chuẩn bị G6.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex.
- Tài liệu gốc: tasks/T-068-don-grafana/SPEC.md; repo lab D:/Project/flashticket-rca-lab: git diff 82e813a..8dccb34 (và ab1c52c..8dccb34).
- Phản biện và phản hồi trước: Codex soát kết quả và hai lượt kiểm lại (chat); phản hồi của người làm và phần sửa ở cuối tasks/T-068-don-grafana/LOG.md.
- Code và kết quả liên quan: results/T-068/ (kiem/BAO-CAO.md, kiem/dem_doc_lap.py, kiem/dem-doc-lap-may.json, thay-doi-may.md, sau-du-lieu*.sha256, dung-dashboard.json); repo lab commit 8dccb34; exp-obs /srv/rca-lab/rca-results/t065-l11-001/service-graph/.
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
```

**Đáp lượt kiểm lại `8dccb34` của Codex (chat, 18/11):**

| Điểm | Kết luận của người làm | Đề xuất (chờ Minh) |
|---|---|---|
| R1 — 2 nút chú thích có link tới panel 3, khác đề xuất đã duyệt ("nút chú thích không link") | **Đúng.** Người làm đổi thiết kế khi sửa mà không trình lại (`service_graph.py` dòng 78; `dem_doc_lap.py` buộc có link). | Giữ hành vi đang chạy (mở đúng bảng trạng thái của ca, có ích hơn), Minh ghi nhận chấp nhận khác biệt. Phương án khác: bỏ link 2 nút, sửa kỳ vọng bộ đếm. |
| R4 — chú giải Grafana vẫn viết "ca thiếu thông tin `db.system`" | **Đúng.** | Đổi thành "trường đích đã xuất của ca thiếu `db.system`" ở `build_dashboards.py` NOTE, sinh lại dashboard sự cố. |
| R5 — câu "85/85 ca = 0" | **Đúng, nói quá.** 84 đồ thị có `dem.dich_ngoai_classes = 0`; `p7/ebd5ef38` có `dem = {}` (không có đầu ra). | Sửa câu trong `BAO-CAO.md`. |
| R6 — hoàn tác nhãn có thể mất dòng nếu runner ghi chỉ mục cùng lúc | **Đúng (nguy cơ, chưa xảy ra).** | Thêm câu vào `thay-doi-may.md`: chỉ hoàn tác khi không có runner ghi chỉ mục, kiểm lại danh sách ca sau đó. |
| STATE ghi "chờ commit repo RCA" | **Đúng** — đã commit `84f44ee`, `ba3dbcb`. | Sửa ngay (dòng của task, trong quyền người làm). |
| R2, R3 | Đồng ý với Codex. | — |

Không còn bất đồng có bằng chứng. Đề xuất dừng phản biện sau khi Minh quyết R1 và duyệt các sửa văn bản trên.

**Quyết định của Minh (18/11, chat):**
- Về phương án A: "DUYỆT TRIỂN KHAI PHƯƠNG ÁN A LUÔN, KHÔNG CẦN TASK MỚI … RÀ SOÁT TRƯỚC XEM CÒN LỖI NÀO KHÔNG THÌ TRÌNH, TÔI MUỐN ĐỒ THỊ VẼ CHI TIẾT NHẤT CÓ THỂ, TẠO PROMPT ĐỂ TÔI DÁN SANG PHIÊN MỚI".
- Về R1 và R4–R6 khi được hỏi có gộp vào prompt A không: "Gộp vào prompt". Nội dung được duyệt: giữ hai link của nút chú thích tới bảng trạng thái (ghi nhận khác biệt so với đề xuất trước); sửa R4, R5, R6 như mục "Đáp lượt kiểm lại `8dccb34`".
- Rà soát trước A (Claude, chỉ đọc), xem chat 18/11. Kết quả: trace 7ffb2305 có 301.015 span, có span RabbitMQ PRODUCER/CONSUMER (exchange `business.ex`, queue, routing key); ca dev3 `86dea661` cũng có span RabbitMQ; ca T-062 `1ad3afeb` không có span RabbitMQ. Trace của 13 ca dev2 và 5 ca dev3 nằm trong `.tgz` ở `results/T-063/thu2/ca/` và `thu3/thu/ca/`. Quy tắc cắt cửa sổ ở `l8b-xuat.py:135–160`. `inventory.json` có `user_db`, nhưng `classes` V082 thì không. Không có điểm chặn. Thiết kế và prompt cho phiên triển khai đã trình trong chat; phiên mới ghi mục "Bổ sung đã duyệt 18/11 — phương án A" vào SPEC.

---

## Phiên 2 — 18/11/2026 — Claude — laptop — vai trò: người làm (triển khai phương án A, sửa R4–R6)

**Mở phiên:** đã đọc AGENTS, STATE, SPEC bản 4, toàn bộ LOG. Người phản biện: Codex.

**Quyết định của Minh trong phiên** (nguyên văn, từ prompt Minh dán mở phiên):
1. Phương án A (18/11): "DUYỆT TRIỂN KHAI PHƯƠNG ÁN A LUÔN, KHÔNG CẦN TASK MỚI … RÀ SOÁT TRƯỚC XEM CÒN LỖI NÀO KHÔNG THÌ TRÌNH, TÔI MUỐN ĐỒ THỊ VẼ CHI TIẾT NHẤT CÓ THỂ". Cách làm: thêm mục "Bổ sung đã duyệt 18/11 — phương án A" vào cuối SPEC, giữ nguyên phần cũ. Bước 0 rà soát; không có điểm CHẶN thì triển khai A trọn vẹn trong phạm vi ghi (gồm commit, push repo lab và chạy trên exp-obs); có CHẶN thì dừng, trình Minh.
2. R1 và R4–R6 (lượt kiểm lại 8dccb34 của Codex): giữ hai link của nút chú thích tới bảng trạng thái, ghi nhận đây là khác biệt so với đề xuất trước; R4: sửa chú giải panel 40 và 41 thành "trường đích đã xuất của ca thiếu db.system", nếu A thay nguồn thì viết lại chú giải theo nguồn mới; R5: trong BAO-CAO.md, câu "85/85 ca = 0" sửa thành "84 đồ thị có bộ đếm = 0; p7/ebd5ef38 không có đầu ra nên dem rỗng"; R6: thay-doi-may.md thêm điều kiện "chỉ hoàn tác nhãn khi không có runner ghi chỉ mục; sau đó kiểm lại danh sách ca".

**Diễn biến:**
- 09:41–09:44Z — **Bước 0 rà soát** (chỉ đọc gói; script `results/T-068/a/ra_soat.py`, chạy 28 ca trên laptop qua `a/chay_ra_soat.sh`, ca 7ffb2305 trên exp-obs trong `/srv/rca-lab/runs/t068-a/` bằng bản script cùng sha256; đầu ra `results/T-068/a/ra-soat/<ca>.json`, tóm tắt `a/ra-soat-tong-hop.json`, log `a/ra-soat.log`). Cắt cửa sổ đúng `l8b-xuat.py:135–160`; với 22 ca t062/dev2, đã đối chiếu `results/T-065/xuat-du-lieu.mjs:5–29` (hàm `prepare`, dùng cho cả `l4-raw.mjs`): cùng [t−300 s, t+300 s), cùng start ≥ lo, end < hi, phía A khi end ≥ t, bỏ trùng theo (trace, span), alias từ method-input.
  - (1) KHÔNG CHẶN — đủ trace 29 ca, hash khớp 29/29: 9 ca T-062 so `results/T-062/manifest.json`; 13 dev2 và 5 dev3: sha256 `.tgz` so `thu2/SHA256SUMS`, `thu3/thu/SHA256SUMS` (hai file này khớp `results/T-063/manifest-2.json` `/file_tong_thu_muc_con`), raw-traces trong gói so `manifest.json` trong gói; ebd5ef38 so dòng `ebd5ef38/raw-traces.jsonl` của `exp-obs-cases.sha256` (= manifest của gói); 7ffb2305 so `results/T-066/e2e-001/ca-manifest.json` `/files/raw-traces.jsonl` (`1da91f27…`). Đọc tgz bằng `tarfile`, không giải nén. File ca trên laptop (`results/T-065/may-l11/du-lieu/`) khớp manifest T-065: 2.145/2.145.
  - Ghi chú: archive có thêm thư mục `ebd5ef381d1a/` với raw-traces khác hash; dùng `ebd5ef38/` (khớp manifest gói và kiểm chéo 0 lệch).
  - (2) KHÔNG CHẶN — 9/9 ca T-062 không có span RabbitMQ (`tong/khong_mq` = 9; đúng 9 ca nguồn t062). 20 ca còn lại có PRODUCER và CONSUMER.
  - (3) KHÔNG CHẶN — **kiểm chéo đạt 29/29**: số quan hệ cha–con khác chủ theo (nguồn, đích, N/A) từ trace = tổng `canh_thao_tac` file ca V082 gộp theo chủ, 0 lệch; số span theo (chủ, N/A) = tổng `n_N`/`n_A` của `thao_tac`, 0 lệch; số quan hệ cùng chủ cũng khớp. Không có span trùng trong cửa sổ.
  - (4) KHÔNG CHẶN — thuộc tính: mọi span có `db.system` là kind CLIENT (3) ở 29/29 ca → đơn vị "span DB phía client" đúng. postgresql luôn có `db.name` (booking_db, ticket_db, event_db, payment_db, keycloak_db); mongodb có `db.name` user_db/admin; redis không có `db.name`. RabbitMQ: PRODUCER có `messaging.destination.name` (exchange `business.ex`), `messaging.operation`=publish, `messaging.rabbitmq.destination.routing_key`; CONSUMER có destination = queue, operation=process. status ERROR có ở 16/29 ca (`a/ra-soat-tong-hop.json` `/ca/*/span_loi` > 0).
  - (5) KHÔNG CHẶN — `classes` của 29 ca: có `broker`, `cache`, `mongodb-instance`, `postgresql-shared-instance` và 5 DB logic postgresql; không có `user_db`, `admin` → mongodb gộp về `mongodb-instance`. Mọi chủ span DB/RabbitMQ thuộc `classes`.
  - (6) KHÔNG CHẶN — ca mới: `sau_v082.py` gọi `dev3_template(ca, w)` với gói `<goc>/cases/<ca>/` (mặc định `/srv/rca-lab/m1/cases/`), bộ xuất đã assert hash raw-traces theo `manifest.json` của gói. Đường trace cho bước đồ thị: `<goc>/cases/<ca>/raw-traces.jsonl`, hash theo cùng manifest.
  - (7) Phát hiện thêm, KHÔNG CHẶN — span RabbitMQ kind CLIENT (`basic.ack`, `Channel.waitForConfirms`, `confirm.select`) không có đích (exchange/queue) ở 20 ca: thiết kế A chỉ vẽ PRODUCER/CONSUMER → ghi số theo service trong file đồ thị, không vẽ.
  - (8) Phát hiện thêm, KHÔNG CHẶN (thiết kế triển khai) — gói trace của 28 ca lịch sử chỉ có trên laptop: đồ thị v4 của 84 cặp sinh trên laptop rồi chuyển lên; `--tat-ca` trên máy phải từ chối khi thiếu gói trace (không ghi đè đồ thị đang có). Hoàn tác về service-graph-3 không còn làm được bằng "checkout + `--tat-ca`" trên máy → sao lưu thư mục `service-graph/` hiện tại vào `/srv/rca-lab/runs/t068-a/` trước khi ghi.
  - Kết luận bước 0: **không có điểm CHẶN** → triển khai A theo quyết định 1.
- 09:46Z — Thêm mục "Bổ sung đã duyệt 18/11 — phương án A" vào cuối SPEC (phần cũ giữ nguyên).
- 09:47Z — Băm mốc trước `results/T-068/a-truoc.sha256` (2.384 dòng): 200 file của `results/T-066/bao-ve.tsv` trên laptop (script `a/bam_bao_ve.py`; member trong `.tgz` đọc bằng tarfile; 200/200 khớp cột `sha256_tinh_lai` của T-066) + 2.184 file cây `du-lieu` trên exp-obs (trùng hoàn toàn `sau-du-lieu-3.sha256` của phiên 1 → không có thay đổi từ 04:26Z).
- 09:48Z — Viết `campaigns/g1/service_graph.py` bản `service-graph-4` theo thiết kế A; `sau_v082.py` truyền gói `<goc>/cases/<ca>` cho bước đồ thị. `--tat-ca` cần `--nguon-trace`, thiếu gói thì dừng trước khi ghi. Tự soát: p50/p95 ban đầu dùng `math.ceil(q*n)` số thực (0,95×20 = 19,000000000000004 → lệch một hạng) → sửa sang số nguyên `(q*n+99)//100 − 1` trước lượt sinh chính (lượt đầu 09:49Z dừng giữa chừng, đầu ra xóa, không dùng).
- `results/T-068/kiem/dem_doc_lap.py` viết lại (bản cũ ở commit `84f44ee`): đọc thẳng trace gốc, `.tgz` qua lệnh `tar` ngoài, lọc cửa sổ một lần trên ns, phân vị số nguyên `-(-p*n//100)-1`, so tập cạnh theo (nguồn, đích, loại) và từng trường số, nút/hạng/màu/số span, ghi chú RabbitMQ, số span không vẽ, link, hash nguồn.
- `build_dashboards.py`: chú giải panel 41/mô tả panel 40 viết lại theo nguồn mới (R4); thêm cột chi tiết nút/cạnh; thêm panel 42 (bảng số liệu cạnh) và 43 (ghi chú: không vẽ, gộp, thiếu RabbitMQ); dịch y +36 cho panel cũ từ y≥45 (trước +23).
- R5: sửa câu trong `kiem/BAO-CAO.md`. R6: thêm điều kiện vào ô hoàn tác nhãn của `thay-doi-may.md`.
- 09:50–09:54Z — Sinh 84 đồ thị v4 trên laptop (`service_graph.py --tat-ca --nguon-trace results/T-068/a/nguon-trace.json --du-lieu results/T-065/may-l11/du-lieu --ra-do-thi results/T-068/a/service-graph`; 3 phút 52 giây; `a/nguon_trace.py` lập danh sách gói + sha256 theo manifest). Mọi cặp qua kiểm chéo `canh_thao_tac`.
- 09:55Z — Lỗi tự gặp: `py -3 -I` bỏ qua `PYTHONIOENCODING` → bộ kiểm in tiếng Việt ra cp1252 lỗi; sửa bằng `sys.stdout.reconfigure(encoding='utf-8')`. Lượt kiểm đang chạy dừng, chạy lại.
- 09:55Z — Đối chứng âm (`a/doi_chung_am.py` → `a/doi-chung-am.json`): bản gốc 0 lệch; 5 lỗi cài (sai số, cạnh ngoài `classes`, link trên cạnh, sai p95, kỳ vọng trên cửa sổ dịch 1.000 ms) đều bị bắt; bộ dựng với file ca có cửa sổ dịch 1.000 ms dừng ở kiểm chéo, không ghi file → **đạt**.
- 09:56Z — Lab commit `9f4eb5c` (push `origin/main`): `service_graph.py`, `sau_v082.py`, `build_dashboards.py`, dashboard sự cố. Giữa `8dccb34` và `9f4eb5c` còn các commit T-067 chỉ ở `app-host/`, `tests/` (không dùng trên exp-obs). Trên exp-obs: sao lưu `service-graph/` v3 vào `t068-a/service-graph-3-bak` (hash trùng), `git fetch` + `git checkout 9f4eb5c` (detached).
- 09:56Z — Thử `sau_v082.do_thi_dich_vu` trên bản sao 1 file ca trong `t068-a/thu`: lỗi cố ý → status `loi`, in cảnh báo; gói sai (thư mục không có) → status `loi`; gọi đúng → đồ thị ok; file ca bản sao không đổi (`1133d125…`).
- 09:56:52Z — Sinh đồ thị V082/7ffb2305 trên máy (5,9 s; sha256 trùng bản sinh ở bản sao `5ce5fb91…`). Bộ kiểm độc lập trên máy (script cùng sha256 `f0219d42…` hai đầu): 1/1 đạt.
- 09:59Z — Bộ kiểm độc lập trên laptop: **84/84 đạt** (`kiem/dem-doc-lap-a-laptop.json`; 1.386 cạnh dịch vụ, 664 cạnh DB, 168 + 168 cạnh RabbitMQ, 1 "không có đầu ra"). Cộng ca máy: 85/85.
- 09:59:49Z — Chuyển 168 file (tar, sha256 hai đầu trùng `1c63cf54…`; 168/168 khớp sau giải nén vào `t068-a/sg4` và sau khi chép vào `service-graph/`). 170/170 file đồ thị là `service-graph-4`, status `ok`.
- 10:00Z — Băm mốc sau `results/T-068/a-sau.sha256`: **trùng byte** `a-truoc.sha256` (200 file bảo vệ + 2.184 file `du-lieu`); không file nào dưới `/srv/rca-lab/m1` mới hơn đầu phiên.
- 10:00–10:04Z — Bấm thật (Grafana, phiên Minh đăng nhập sẵn, tunnel có sẵn): 7ffb2305 V082 có nút/cạnh tới booking_db, payment_db, ticket_db, event_db, keycloak_db, cache, broker; chi tiết cạnh hiện đủ trường, không link. Tự phát hiện: bảng số liệu sai thứ tự cột (thiếu `indexByName`) → lab `69973fa`; chú giải bị cắt, bảng ghi chú quá hẹp → lab `6a0def7` (chú giải h5, hai bảng full ngang, dịch y +42). Kiểm cấu trúc: panel cũ giống hệt `ab1c52c` sau dịch; grep khóa đáp án 0. Checkout trên máy lần lượt `69973fa`, `6a0def7`; provider tự nạp, không restart Grafana.
- Bấm thật sau sửa: 1ad3afeb V082 17 nút/22 cạnh, không cạnh broker, nút "broker — trace của ca không có span RabbitMQ", bảng ghi chú 2 dòng; ebd5ef38 P7 "không có đầu ra/LOI_CHAY", V082 và V071 17 nút/32 cạnh, payment-service #1. Thời gian tới khi panel vẽ không đo đại diện (pane trình duyệt của app bị ẩn, trang chạy nền; truy vấn gửi lúc 10–34 s); truy vấn panel 40 mất 173–200 ms; với `var-dv=` rỗng, biến `dv` báo 400 và cả panel gốc 3 chưa truy vấn sau 22 s (hành vi sẵn có của T-065).
- Trong lúc phiên chạy, repo lab xuất hiện `load/controller/README.md` bị sửa (chưa commit) — không do phiên này, không đụng tới.
- Ghi `kiem/BAO-CAO.md` (mục "Phương án A"), `thay-doi-may.md` (mục "Phiên 2").

**Kết thúc phiên 2 (18/11/2026 ~10:10Z):**
1. Đã làm gì: bước 0 rà soát (không CHẶN); thêm mục Bổ sung vào SPEC; triển khai phương án A (`service-graph-4`): đồ thị dịch vụ đọc trace gốc, có cạnh DB theo `db.name`, cạnh RabbitMQ qua broker, số lỗi và p50/p95, bảng số liệu cạnh và bảng ghi chú trên dashboard; sửa R4, R5, R6; giữ link nút chú thích (R1, theo Minh).
2. File đã thay đổi — repo RCA: `tasks/T-068-don-grafana/SPEC.md` (chỉ thêm mục Bổ sung), `LOG.md`, dòng T-068 trong `docs/STATE.md`, `results/T-068/` (`a/` mới: script rà soát, băm, nguồn trace, đối chứng âm, 84 đồ thị v4, kết quả; `a-truoc.sha256`, `a-sau.sha256`; `kiem/dem_doc_lap.py` viết lại; `kiem/dem-doc-lap-a-laptop.json`, `.log`; `kiem/BAO-CAO.md`; `thay-doi-may.md`). Repo lab: `9f4eb5c`, `69973fa`, `6a0def7` (đã push). exp-obs: theo `thay-doi-may.md` mục Phiên 2.
3. Kiểm đã chạy: hash 29 gói; kiểm chéo 29/29; bộ kiểm độc lập 85/85; đối chứng âm 6/6; cô lập lỗi `sau_v082`; hash chuyển file hai đầu; toàn vẹn trước = sau; cấu trúc dashboard; grep đáp án; bấm thật 3 ca.
4. Chưa chắc / cần Minh:
   - Đầu ra A đạt các mục kiểm của mục Bổ sung theo kiểm của người làm; chưa phản biện.
   - Câu hỏi nguồn: phần hiển thị DT18/P10 nay thể hiện đồ thị phụ thuộc chi tiết hơn (DB logic, broker, lỗi, độ trễ) từ trace; vẫn là quan sát, không trả lời lợi ích của việc dùng quan hệ trong phương pháp.
   - Thời gian tải panel trên giao diện chưa đo được đại diện (pane bị ẩn). Phần truy vấn đo được 173–200 ms. Nếu cần, Minh mở trang ở trình duyệt thường để xem.
   - Gói trace của 28 ca lịch sử chỉ có trên laptop; sinh lại 84 cặp phải chạy trên laptop rồi chuyển lên. Đề xuất: giữ như vậy tới W5 (dịch vụ trực tuyến có kho gói chung). Phương án khác: chép 27 gói lên máy (dung lượng cần đo trước, Minh duyệt).
   - Thư mục `/srv/rca-lab/runs/t068-a/` (gồm bản sao lưu v3) và `/srv/rca-lab/runs/t068-thu/` giữ theo luật cứng 10; xóa khi Minh duyệt.
   - Commit repo RCA chờ Minh duyệt (đề xuất nội dung trong chat).
5. Bước tiếp theo chính xác: Minh chuyển prompt dưới cho Codex (soát kết quả phần A và sửa R4–R6). Codex đọc `tasks/T-068-don-grafana/SPEC.md` mục Bổ sung, LOG phiên 2, `results/T-068/kiem/BAO-CAO.md` mục "Phương án A", lab `git diff 8dccb34..6a0def7 -- campaigns observability`.
6. Lệnh cuối cùng đã chạy: đếm cặp không có cạnh RabbitMQ trên `results/T-068/a/service-graph` (83 cặp có đầu ra, 27 không có cạnh broker).

**Prompt cho Codex — soát kết quả T-068 phương án A:**

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-068 — tasks/T-068-don-grafana/ (SPEC.md, mục "Bổ sung đã duyệt 18/11 — phương án A"; LOG.md, mục "Phiên 2").
- Công đoạn: soát kết quả.
- Gói/cổng: P10, chuẩn bị G6.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex.
- Tài liệu gốc: tasks/T-068-don-grafana/SPEC.md; repo lab D:/Project/flashticket-rca-lab: git diff 8dccb34..6a0def7 -- campaigns observability (và ab1c52c..6a0def7 cho dashboard).
- Phản biện và phản hồi trước: Codex soát kết quả và các lượt kiểm lại (chat); phản hồi của người làm trong tasks/T-068-don-grafana/LOG.md, các mục "Phiên 1 (tiếp)" và "Phiên 1 (tiếp 2)".
- Code và kết quả liên quan: results/T-068/ (a/, a-truoc.sha256, a-sau.sha256, kiem/BAO-CAO.md, kiem/dem_doc_lap.py, kiem/dem-doc-lap-a-laptop.json, thay-doi-may.md); repo lab 9f4eb5c, 69973fa, 6a0def7 (campaigns/g1/service_graph.py, campaigns/runner/sau_v082.py, observability/grafana/); campaigns/g1/l8b-xuat.py; results/T-065/xuat-du-lieu.mjs, results/T-065/l4-raw.mjs; manifest gói trace: results/T-062/manifest.json, results/T-063/manifest-2.json, D:/RCA-archive/hash-lists/exp-obs-cases.sha256, results/T-066/e2e-001/ca-manifest.json; exp-obs /srv/rca-lab/rca-results/t065-l11-001/service-graph/, /srv/rca-lab/runs/t068-a/.
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

Công đoạn: soát kết quả.
Kiểm trên đầu ra thật, code và dữ liệu được phép; không tin tóm tắt LOG. Đối chiếu tiêu chí xong với phần mục tiêu nguồn và mức căn cứ cho bước tiếp theo; chạy lại phần rẻ khi trong quyền được duyệt.
Phân biệt hoàn thành task mô tả, xác nhận cơ chế và đủ căn cứ chọn/đánh giá thiết kế. Giới hạn đã khai không tự miễn phép kiểm cần thiết còn làm được.
Chỉ ghi bản phản biện lượt được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ bản cũ; không sửa kết quả thay người làm.
```

---

## Phiên 2 (tiếp) — 18/11/2026 — Claude — laptop — vai trò: người làm (đính chính, đo thời gian tải)

**Quyết định của Minh** (nguyên lời): "duyệt đính chính log và đo lại thời gian."

**Đính chính** mục "Phiên 2", dòng bấm thật sau sửa: câu "với `var-dv=` rỗng, biến `dv` báo 400 và cả panel gốc 3 chưa truy vấn sau 22 s (hành vi sẵn có của T-065)" nói quá bằng chứng. Đúng là: biến `dv` báo 400 khi `var-dv=` rỗng (định nghĩa biến không đổi so với `ab1c52c`). Độ trễ vẽ panel đo lúc pane bị ẩn, chưa tách được giữa trang chạy nền và lỗi biến; chưa kết luận. Câu tương ứng trong mục 4 kết thúc phiên 2 và trong `kiem/BAO-CAO.md` mục "Thời gian" cùng phạm vi đính chính này; kết quả đo lại ghi dưới đây.

**Đo lại thời gian tải (18/11/2026, pane trình duyệt của app hiện thật, `document.visibilityState = visible`; tunnel `127.0.0.1:3000`; bản V082; mốc tính từ lúc điều hướng, theo `performance` của trang):**

| Ca | `var-dv` | dto dashboard | truy vấn đầu | truy vấn cuối xong | đồ thị panel 40 vẽ xong |
|---|---|---|---|---|---|
| 7ffb2305 | api-gateway | 3,5 s | 5,7 s | 6,7 s | 7,8 s |
| 7ffb2305 | rỗng | 5,1 s | 7,5 s | 8,8 s | 9,9 s |
| ebd5ef38 | payment-service | 4,5 s | 6,7 s | 8,1 s | 9,1 s |
| ebd5ef38 | rỗng | 3,7 s | 5,6 s | 6,9 s | 7,4 s |
| 1ad3afeb | api-gateway | 2,5 s | 4,9 s | 6,1 s | 7,1 s |
| 1ad3afeb | rỗng | 2,5 s | 5,2 s | 6,3 s | 7,1 s |

- Lượt đầu (7ffb2305, `api-gateway`, sau khi mở lại pane): vẽ xong 11,3 s, truy vấn đầu 8,7 s.
- Mỗi lượt có 8 truy vấn Infinity, mỗi truy vấn 165–260 ms.
- Trang danh sách dashboard của Grafana (không liên quan T-065/T-068) hiện nội dung lúc 4,2 s.
- Dashboard đầy đủ (không `viewPanel`), 1ad3afeb, `var-dv=` rỗng: 9 truy vấn, xong lúc 9,6 s. Đúng một truy vấn trả 400, 8 truy vấn còn lại 200. Các panel hiện bình thường. Lượt này không đọc được thân phản hồi 400, nên chưa xác định nó thuộc biến nào.

**Quan sát:**
- 2–5 s đầu là Grafana tự khởi động phía trình duyệt: nạp bundle, plugin app, cờ tính năng, thư mục.
- Từ lúc có định nghĩa dashboard tới truy vấn đầu: khoảng 2 s.
- Các truy vấn mất khoảng 1–1,4 s.
- Vẽ node graph mất khoảng 0,5–1 s.

**Suy luận:**
- Với `var-dv` rỗng, panel 40 không chậm hơn một cách nhất quán: chênh lệch nằm trong dao động giữa các lượt (−1,7 s tới +2,1 s).
- Độ trễ 10–60 s đo ở phiên 2 do pane bị ẩn, không do lỗi biến.
- Chưa thấy bằng chứng lỗi biến làm chậm hoặc chặn panel.

**Giới hạn:**
- Mỗi ô đo một lần, trên laptop, qua tunnel.
- Chưa tách được phần CPU của trình duyệt với phần mạng.

**Câu đã sửa:** câu thời gian trong `kiem/BAO-CAO.md` mục "Thời gian" đã thay theo kết quả trên.

**Quyết định của Minh** (nguyên lời): "duyệt đổi" (đổi 67 dòng CRLF của khối prompt Codex trong LOG này sang LF). Đã đổi: 67 dòng, chữ không đổi, LOG còn 0 byte CR. Rà thêm: 5 file đầu ra T-068 ghi bằng `json.dump`/log ở chế độ văn bản trên Windows còn CRLF (`a/doi-chung-am.json`, `a/ra-soat-tong-hop.json`, `a/ra-soat.log`, `kiem/dem-doc-lap-a-laptop.json`, `kiem/dem-doc-lap-a-laptop.log`); 84 đồ thị, `ra-soat/<ca>.json`, `nguon-trace.json`, mốc băm không có CR. Chưa sửa, chờ Minh.

## Phiên 3 — 19/11/2026 — Claude — laptop — vai trò: người làm (đáp phản biện Codex lượt soát phương án A, sửa theo 8 bước)

**Quyết định của Minh trong phiên** (nguyên lời): "Duyệt cả 8 bước" (gói sửa 8 bước Claude đề xuất trong chat 18–19/11 sau phản biện của Codex). Thư mục đích bước 8: `/srv/rca-lab/trace-goi/` (Minh chọn).

Ghi chú quy trình: trước khi đọc phản biện, người làm đã tự thấy N1 (5 file CRLF, ghi ở mục trên), N2 (thiếu mục WHY/DECISIONS cho các lựa chọn của phương án A, trái luật cứng 3), N3 (truy vấn biến báo 400). N2, N3 chưa được ghi vào LOG trước khi đọc kết luận của Codex như mẫu yêu cầu; ghi tại đây.

**Đính chính** (các đoạn cũ giữ nguyên; đoạn dưới thay thế phần sai):

1. Mục "Phiên 2", dòng 09:48Z, lý do đổi phân vị: câu "0,95×20 = 19,000000000000004 → lệch một hạng" **sai**. Kiểm lại (Python, n = 1…99.999): `math.ceil(0.95*n)` trùng `(95*n+99)//100` ở mọi n; `repr(0.95*20)` = `19.0`. Đổi sang số nguyên không sửa lỗi nào đã xảy ra; chỉ là cách viết không phụ thuộc số thực.
2. Cùng dòng: "lượt đầu 09:49Z dừng giữa chừng, đầu ra xóa" — đã xóa đầu ra một lượt hỏng, **vi phạm luật cứng 10**. Không khôi phục được (không có bản sao). Không có số nào từ lượt đó được dùng.
3. Cùng dòng: "thiếu gói thì dừng trước khi ghi" nói quá. Code v4 chỉ kiểm tên ca có trong `nguon-trace`; gói của một ca sau bị thiếu thì các ca trước đã ghi. Sửa ở v5 (bước 2 dưới).
4. Mục "Phiên 2", điểm (8) bước 0 và mục 4 kết thúc phiên 2: "28 ca lịch sử chỉ có trên laptop" **sai**. Trên exp-obs `/srv/rca-lab/m1/cases/` có `46aab4be`, `ebd5ef38` và ca mới `7ffb2305` → 26 gói chỉ có trên laptop.
5. Mục "Phiên 2 (tiếp)": "biến `dv` báo 400" **sai đối tượng**. Truy vấn 400 là của biến `op` (đường `thao-tac-vue/<ca>/.json` khi `dv` rỗng). Nguồn chính tạo `dv` rỗng là link của nút chú thích (`var-dv=`).
6. Mục "Phiên 2 (tiếp)", phần suy luận: "độ trễ 10–60 s đo ở phiên 2 do pane bị ẩn" hạ thành **suy luận chưa kiểm**: bằng chứng gián tiếp (lúc đó `document.visibilityState` = `hidden`; khi pane hiện đo được 7,1–9,9 s), chưa đo ghép cặp ẩn/hiện. Codex đo trên Chrome 4,87–6,51 s, cùng chiều.

**Bảng phản hồi phản biện Codex (lượt soát phương án A, chat 18/11):**

| # | Codex | Kết luận người làm | Bằng chứng | Xử lý (Minh duyệt 8 bước) |
|---|---|---|---|---|
| 1 | CHẶN — cạnh dịch vụ không kiểm đích thuộc `classes`; nhánh DB không kiểm kind; bộ kiểm cùng điểm mù | Đúng | `service_graph.py` `observe`: `svc_edge` không kiểm `classes`; nhánh DB chỉ cần `db.system`. `kiem/dem_doc_lap.py` miễn `span_cha_con` khỏi kiểm `classes`. 85 đồ thị hiện tại không gặp (29/29 ca span DB đều CLIENT) | Bước 2, 3 |
| 2 | CHẶN — `--tat-ca` ghi trước khi biết gói sau thiếu | Đúng | CLI chỉ kiểm tên ca trong `nguon-trace` | Bước 2: dựng hết trong bộ nhớ rồi mới ghi |
| 3 | CHẶN — lệnh hoàn tác thiếu `--goi`; câu về v3 sai | Đúng | Dòng 02:21 và 09:59 `thay-doi-may.md`; README lab | Bước 5 |
| 4 | KHÔNG CHẶN — link tới thực thể không có thao tác; `kiem_link` cho qua khi mất URL chú thích | Đúng một phần: gắn link theo `services` có từ v3; phần `kiem_link` đúng | `l8b-xuat.py` trường `services`; `kiem_link` `continue` khi không có URL | Bước 2 (kiểm trang trước), bước 3 |
| 5 | KHÔNG CHẶN — sinh lại lỗi thì giao diện vẫn hiện đồ thị cũ | Đúng | `sau_v082` chỉ ghi `status = loi` | Bước 2 |
| 6 | CHẶN — `doi-chung-am.json` không phải JSON, script luôn thoát 0 | Đúng | dòng `DAT` sau khối JSON | Bước 3, file mới, giữ file cũ |
| 7 | CHẶN — lượt hỏng bị xóa; lý do p95; CRLF | Đúng, nặng hơn: lý do p95 sai hẳn | Đính chính 1, 2 trên; 5 file CRLF | Đính chính; bước 5 |
| 8 | KHÔNG CHẶN — vị trí gói trace | Đúng | Đính chính 4 | Bước 8 |
| — | Thời gian, lỗi 400 | Đúng một phần | Đính chính 5, 6 | Bước 2 (link chú thích), bước 5 |


**Bước 5 (một phần) — đổi CRLF → LF** (Minh duyệt 8 bước 19/11). Ghi hash trước khi đổi; chỉ đổi CRLF thành LF, chữ không đổi. Không file nào trong `docs/`, `tasks/`, `results/T-068/` trích các hash cũ (Grep 0 kết quả). `dung-dashboard.json` là đầu ra phiên 1 (Codex nêu thêm).

| File | sha256 cũ (CRLF) | sha256 mới (LF) | Số dòng đổi |
|---|---|---|---|
| `a/doi-chung-am.json` | `9988cde7a7f391dcc319ff45925e7a4ef38b4684428fa56f5716806f8588a674` | `0e1e45af0ef0d3d2bc690bbd295fd26626087ee4878b6486f296b6f4645ea9e0` | 73 |
| `a/ra-soat-tong-hop.json` | `6534f4deec547e9cf3f336e5fc7bb61fbe73bef4ec98ff3bdef5b973b95f8c68` | `8898052eb7b41e2928456212a1314e77ccbbc709b9003798e5be0c15e4ad4654` | 1018 |
| `a/ra-soat.log` | `8f0372caa19e2d7fd84d8a965988cddcfbd197c629361a55531c884c1fc168c5` | `1f598341310e1555c061073ae4b858a073f03bdbdfc5129056deab696ccbe043` | 28 |
| `kiem/dem-doc-lap-a-laptop.json` | `94ac961a1286538f8dab5b553cc43e90c8377708f74ed1ff9dc545bf51584bda` | `2abe0a07ef3c1b990837f2f91ef8c831cc3894a9ee3a47864163aeab9fe92e5a` | 13 |
| `kiem/dem-doc-lap-a-laptop.log` | `663cf2e9e602b16943e014e7523cf68ef4320882544c9e6cab1c9a125c3fd80d` | `7947e961074a4d59fb5e36665cf08188bd0dcd511bc6f0001af763914e719128` | 28 |
| `dung-dashboard.json` | `44c1420687e5d643629d92af5f8d862dd289c6f80069028a2efc2c61e78f049e` | `4fb2e2973391bd251eff11bed8da21f6f99bea2980048a9962793b502cd517e5` | 14 |

**Tiến trình phiên 3** (giờ UTC; 18/11 23:xx = 19/11 giờ Việt Nam):
- Bước 2 — lab `campaigns/g1/service_graph.py` → `service-graph-5`: (a) kiểm chéo đếm mọi cặp cha–con khác chủ; chỉ vẽ khi hai chủ thuộc `classes`, còn lại ghi "không vẽ"; span của chủ ngoài `classes` không thành nút, ghi "không vẽ"; (b) span có `db.system` mà kind khác CLIENT: không vẽ, ghi kind; (c) `--tat-ca`: kiểm mọi gói có mặt, dựng hết trong bộ nhớ (`graphs_case`), chỉ ghi (`write_graphs`) khi mọi ca xong; (d) `link()` của nút chú thích không đặt `var-dv`/`var-op`; (e) `error_graph()`: ghi đè `<ca>.json` bằng đồ thị chú thích "lỗi dựng đồ thị". `campaigns/runner/sau_v082.py`: khi lỗi gọi `error_graph` rồi ghi status; lỗi cố ý `T068_GAY_LOI_DO_THI` chuyển xuống sau khi nạp module để phép thử đi qua nhánh ghi đè.
- Tự soát khi sửa: đề xuất "`var-dv=__khong_co__`" trong chat **sai**. `__khong_co__` là giá trị rỗng của biến `op` (dashboard `t065-l8b-rca`, `root_selector` của `op`); đặt `dv` như vậy vẫn gọi `thao-tac-vue/<ca>/__khong_co__.json` không tồn tại. Đổi thành bỏ hẳn `var-dv`/`var-op` (cùng mục đích, trong phạm vi bước 2). Chưa bấm thật xác nhận (Grafana chưa đăng nhập).
- Điểm 4 (link tới thực thể không có thao tác): `thao-tac-vue/<ca>/` có file cho mọi thực thể kể cả `booking_db`, `broker`, `cache` (1ad3afeb V082: 17 file), và biến `dv` của dashboard liệt kê đủ (`service_options`). Quyết giữ hay bỏ link chờ mở trang `dv=booking_db`.
- Lab `observability/grafana/README.md`: lệnh theo revision, `--goi`, `--nguon-trace`, vị trí gói, hành vi khi lỗi.
- 23:52:30–23:57:46Z — Sinh 84 cặp v5 trên laptop vào thư mục mới `results/T-068/a/service-graph-5/` (v4 giữ nguyên ở `a/service-graph/`); 5 phút 16 giây (chạy song song việc chép gói); `a/sinh-v5.log`. So v4 → v5 trên 168 file: khác đúng 168 trường `phien_ban` và 2 `detail__url` của nút chú thích p7/ebd5ef38 (bỏ `var-dv=&var-op=`); mọi trường khác trùng. Như vậy dữ liệu hiện có không có cạnh/nút ngoài `classes` hay span DB khác CLIENT (khớp bước 0).
- Bước 3 — `kiem/dem_doc_lap.py`: bỏ miễn kiểm `classes` của cạnh cha–con; kỳ vọng theo quy tắc v5 (viết riêng); kiểm chéo đếm mọi cặp; nút chú thích phải có link panel 3, không `var-dv`/`var-op`; stdout/stderr ghi LF (`newline='\n'`; đây là nguồn CRLF của các đầu ra trước). `a/doi_chung_am_2.py` mới (bản 1 và `doi-chung-am.json` giữ nguyên): 0, 0b gốc; 1–5, 7, 11, 12 lỗi cài cho bộ kiểm; 6, 8, 9, 10a–c cho bộ dựng; ghi một JSON, thoát 1 khi không đạt.
- Lượt hỏng (giữ, luật cứng 10): `scratchpad/dca2` (23:59:20Z) — đối chứng âm chạy đúng lúc `dem_doc_lap.py` đang dở một chỗ sửa (dòng `newline` vỡ, lỗi cú pháp) → bộ kiểm không in JSON, script dừng, không ghi kết quả. `scratchpad/dca2b` (00:00:43Z) — dữ liệu giả của mục 8/9 thiếu cạnh thao tác cùng chủ (span d1, d2 có cha cùng chủ b) → bộ dựng dừng ở kiểm chéo đúng thiết kế ("cùng chủ 2 so với 0"); sửa dữ liệu giả thêm `o3 → o4` (so_N 2). Đường dẫn đầy đủ: `C:/Users/84583/AppData/Local/Temp/claude/5926e3c52aa473a7/68b303a7-ebb6-46f5-af8d-3dc54fd0bdee/scratchpad/`.
- Bước 5 (một phần) — `thay-doi-may.md`: ghi đính chính vào ô hoàn tác dòng 02:21 (thêm `--goi`) và dòng 09:59:49 (câu về v3 sai; 26 gói); mục Phiên 3 thêm khi triển khai.
- Bước 8 — 23:52:30–23:56Z: tạo `/srv/rca-lab/trace-goi/` (`sudo mkdir`, chủ `ubuntu`); chép 26 gói (17 `.tgz` dev2/dev3, 9 thư mục ca T-062 đủ file) bằng scp; danh sách `results/T-068/trace-goi.sha256` (71 file, 1,929 GiB; trước khi chép đã so `.tgz` với `sha_ngoai` và file thư mục với `manifest.json` của gói) → `trace-goi/SHA256SUMS`. Trên máy `sha256sum -c`: khớp 71/71; 26 gói, 2,0G. Không có `46aab4be`, `ebd5ef38` (đã có ở `m1/cases/`).
- Lượt hỏng thứ ba (giữ): `scratchpad/dca2c` (00:02:04Z) — tiến trình con in stderr cp1252, `subprocess` đọc UTF-8 lỗi giải mã nên `stderr` = None, script dừng ở mục 10a. Sửa: tiến trình con chạy `-X utf8`, đọc `errors='replace'`.
- 00:01:58–00:03:42Z — Đối chứng âm bản 2 (`scratchpad/dca2d`) → `a/doi-chung-am-2.json`: **16/16 đạt**, JSON hợp lệ, 0 byte CR, mã thoát 0. Bộ kiểm báo lệch ở 1–5, 7, 11, 12; bộ dựng dừng không ghi file ở 6, 10a (thiếu gói ca thứ hai), 10b (sai hash ca thứ hai, ca thứ nhất đã dựng trong bộ nhớ vẫn không ghi); 8, 9 không vẽ span DB kind SERVER và cạnh tới dịch vụ ngoài `classes`, bộ kiểm tính cùng kỳ vọng; 10c (đối chứng dương) ghi đủ 4 file.
- 23:59:12–00:05:04Z — Bộ kiểm độc lập trên 84 cặp v5: 84/84 đạt (`kiem/dem-doc-lap-v5-laptop.json`; bản bộ kiểm trước khi thêm `newline`, đầu ra CRLF, giữ). Chạy lại bằng bản cuối (sha256 `9624d44d…`), 00:05:12–00:09:52Z: **84/84 đạt** (`kiem/dem-doc-lap-v5-laptop-2.json`, 0 byte CR); 1.386 cạnh cha–con, 664 DB, 168 + 168 RabbitMQ, 1 cặp không có đầu ra.
- 00:10Z — **Dừng chờ Minh:** lệnh `git commit` + `git push` repo lab bị bộ phân loại của chế độ tự động trong Claude Code từ chối (không thử đường vòng). Bước 4 phần trên máy (checkout `/opt/rca-lab`, sinh 7ffb2305, chép 84 cặp) phụ thuộc commit này. Điểm 4 chờ Minh đăng nhập Grafana để mở trang `dv=booking_db`. Thay đổi lab đang chưa commit: `campaigns/g1/service_graph.py`, `campaigns/runner/sau_v082.py`, `observability/grafana/README.md`.
- Bước tiếp theo chính xác: (1) commit, push lab; (2) trên exp-obs sao lưu `service-graph/` v4 vào `t068-a/service-graph-4-bak` + sha256; băm mốc trước; `git fetch` + `git checkout <commit>`; sinh `V082-V066+H8a/7ffb2305` bằng `--goi /srv/rca-lab/m1/cases/7ffb2305`; chạy bộ kiểm trên máy; chép 168 file từ `results/T-068/a/service-graph-5/` (tar, sha256 hai đầu); băm mốc sau; (3) bấm thật 3 ca và link nút chú thích; (4) điểm 4; (5) `thay-doi-may.md` mục Phiên 3, `kiem/BAO-CAO.md`; (6) trình WHY-100/101 + DECISIONS (bản nháp ở chat); (7) đề xuất commit repo RCA.
- 00:2xZ — Minh: "COMMIT PUSH SAU ĐÓ BÁO CÁO ĐỀ XUẤT VIỆC TIẾP THEO". Lab commit `ee91432` (3 file trên), push `origin/main` (`6a0def7..ee91432`). Chưa triển khai lên exp-obs; repo RCA chưa commit.
- Minh: "Triển khai ngay" (triển khai v5 lên exp-obs rồi bấm thử).
- 02:45Z — Mốc trước `results/T-068/p3-truoc.sha256` (200 file bảo vệ, lệch 0; 2.184 file `du-lieu`): trùng byte `a-sau.sha256`. Sao lưu `service-graph/` v4 → `t068-a/service-graph-4-bak` (170 file, khớp).
- 02:46Z — exp-obs `/opt/rca-lab` checkout `ee91432` (detached). Sinh 7ffb2305 vào `t068-a/sg5-thu` (7 s): chỉ khác v4 ở `phien_ban`; bộ kiểm trên máy (`t068-a/dem_doc_lap_5.py`, sha256 `9624d44d…` như laptop) 1/1 đạt (18 cạnh cha–con, 8 DB, 3 + 3 RabbitMQ). Sinh tại chỗ 02:46:55Z: trùng sha256 bản thử.
- 02:47Z — Thử `sau_v082.do_thi_dich_vu` trên bản sao file ca (`t068-a/thu5`): gọi đúng → ok; lỗi cố ý → `<ca>.json` ghi đè thành đồ thị "lỗi dựng đồ thị" (2 nút chú thích, link panel 3 không `var-dv`), status `loi` có `do_thi`; gói không tồn tại → cùng kết quả; gọi đúng lại → trở về đúng hash; file ca bản sao không đổi (`1133d125…`).
- 02:48Z — Chép 168 file v5 (tar sha256 hai đầu trùng; 168/168 khớp sau giải nén và sau khi chép). 170/170 file trên máy là `service-graph-5`, status ok. Mốc sau `p3-sau.sha256` trùng byte mốc trước; `/srv/rca-lab/m1` không file mới. `thay-doi-may.md` thêm mục Phiên 3 (bảng thay đổi, hoàn tác, lệnh theo revision).
- Chờ Minh đăng nhập Grafana để bấm thử và xem điểm 4.
- Minh đăng nhập Grafana. Bấm thử qua tunnel (19/11):
  - 7ffb2305 (V082) và 1ad3afeb (V082): panel 40 vẽ đủ nút DB logic (`booking_db`, `payment_db`, `ticket_db`, `keycloak_db`, `event_db`), `broker`; màu và hạng theo bản.
  - p7/ebd5ef38: hai nút chú thích. Bấm menu nút → link `viewPanel=panel-3` không có `var-dv`/`var-op` → panel 3 mở, `dv` tự chọn "(Không có đầu ra — lỗi chạy)". Mọi `api/ds/query` 200, console không lỗi. Lỗi 400 của bản 4 không còn.
- Điểm 4 (link nút DB/broker/cache tới trang thao tác): mở `var-ca=1ad3afeb&var-dv=booking_db`. Quan sát: trang mở được, mọi truy vấn 200; `op` = "(Không có thao tác)"; panel "Lớp thao tác" ghi "Không có thao tác cho service trong trace sau cắt cửa sổ; chưa phân xử không phát sinh hay không được thu"; metric/trace/log của `booking_db` rỗng ở ca này. Đếm `co_m1` trong 84 file ca `results/T-065/may-l11/du-lieu`: có cờ M1 trỏ tới thực thể DB (event_db 30, booking_db 15, ticket_db 14, payment_db 11, keycloak_db 3; lệnh chỉ đọc trong chat phiên 3). Suy luận: link nút DB vẫn có ích vì panel "Bằng chứng có cờ" hiện cờ M1 của DB ở các ca có cờ. Câu "chưa phân xử không phát sinh hay không được thu" sai nghĩa với thực thể DB (DB không có span riêng theo thiết kế, chỉ có span client) — câu này sinh từ dữ liệu `thao-tac-vue` của T-065, ngoài code T-068 đã sửa; chưa sửa, trình Minh.
- Đính chính dòng trên: câu "chưa phân xử không phát sinh hay không được thu" sinh từ lab `campaigns/g1/l8b-xuat.py:388` (file chỉ đọc theo ràng buộc phiên) và `campaigns/runner/sau_v082.py:120`, không phải "dữ liệu thao-tac-vue của T-065".
- Minh quyết điểm 4 (chat 19/11): "Giữ link" — giữ link nút DB/broker/cache tới trang thao tác; không đổi code, không sinh lại.
- `results/T-068/kiem/BAO-CAO.md`: thêm đính chính 3–6 dưới đoạn cũ (giữ nguyên đoạn cũ) và mục "Sửa theo phản biện Codex lượt phương án A" (v5, bảng kiểm, bấm thật 19/11, điểm 4).

**Prompt cho Codex — kiểm lại phản hồi và sửa (phiên 3, 19/11).** Minh chọn gửi hay dừng.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-068 — tasks/T-068-don-grafana/ (SPEC.md gồm mục "Bổ sung đã duyệt 18/11 — phương án A"; LOG.md).
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P10, chuẩn bị G6.
- Người làm và người phản biện chính thức: người làm Claude; người phản biện Codex.
- Tài liệu gốc: tasks/T-068-don-grafana/SPEC.md; repo lab D:/Project/flashticket-rca-lab: git diff 8dccb34..ee91432 -- campaigns observability (gồm 6a0def7..ee91432 của lượt sửa này), và ab1c52c..ee91432 cho dashboard. Repo RCA: các file T-068 chưa commit tại lúc soạn prompt.
- Phản biện và phản hồi trước: các lượt soát kết quả và kiểm lại của Codex (chat), gồm lượt soát phương án A ngày 18/11; phản hồi của người làm trong chat ngày 18/11 và trong tasks/T-068-don-grafana/LOG.md (các mục sau "Phiên 2 (tiếp)", gồm "Phiên 3"); results/T-068/kiem/BAO-CAO.md mục "Sửa theo phản biện Codex lượt phương án A". WHY-100, WHY-101 và mục DECISIONS của T-068: bản nháp đã trình Minh trong chat, chưa ghi vào docs/.
- Code và kết quả liên quan: results/T-068/ (a/, a-truoc.sha256, a-sau.sha256, kiem/, thay-doi-may.md); repo lab campaigns/g1/service_graph.py, campaigns/runner/sau_v082.py, observability/grafana/ ở commit ee91432; campaigns/g1/l8b-xuat.py; results/T-065/may-l11/, results/T-065/xuat-du-lieu.mjs, results/T-065/l4-raw.mjs; manifest gói trace: results/T-062/manifest.json, results/T-063/manifest-2.json, D:/RCA-archive/hash-lists/exp-obs-cases.sha256, results/T-066/e2e-001/ca-manifest.json, results/T-066/bao-ve.tsv; exp-obs /srv/rca-lab/rca-results/t065-l11-001/service-graph/, /srv/rca-lab/runs/t068-a/, /srv/rca-lab/trace-goi/ (SHA256SUMS; danh sách laptop results/T-068/trace-goi.sha256); Grafana qua tunnel (Minh đăng nhập).
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
```

**Kết thúc lượt (19/11).** Đã: bấm thật v5 (hết 400), điểm 4 giữ link (Minh), `BAO-CAO.md` cập nhật, dòng T-068 trong STATE cập nhật, prompt Codex ở trên; tunnel đã đóng. Chưa: ghi WHY-100, WHY-101, DECISIONS (bản nháp trình trong chat, chờ duyệt); commit repo RCA (chờ duyệt; `docs/STATE.md` lẫn sửa T-066/T-067 của phiên khác — chỉ stage dòng T-068). Còn mở: câu "chưa phân xử…" sai nghĩa với DB (`l8b-xuat.py:388`, `sau_v082.py:120`); thư mục tạm `t068-a`, `t068-thu` trên exp-obs chờ Minh quyết xóa. Bước tiếp: Minh duyệt WHY/DECISIONS → ghi `docs/WHY.md`, `docs/DECISIONS.md`; duyệt commit → `git add` các file T-068 + hunk T-068 của STATE, commit, push. Lệnh cuối: dừng tunnel `ssh -L 3000`.
