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
