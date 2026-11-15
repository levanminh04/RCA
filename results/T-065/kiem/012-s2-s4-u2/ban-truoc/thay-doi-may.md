# T-065 — thay đổi exp-obs và hoàn tác

Chỉ thay đổi phạm vi Grafana do L3 phụ trách. Giờ chính xác từ lệnh remote ở `codex/obs-truoc.txt`, `restart-grafana*.txt`, `obs-sau-cuoi.txt`. Các mốc nhịp trong checkpoint là gần đúng; lệnh remote là nguồn giờ thao tác.

| Phạm vi | Trước | Sau |
|---|---|---|
| `pinned/provisioning/dashboards/t065-rca.json`, `t065-phat-lai.json` | Chưa có; guard đã kiểm | Hai file mới, khớp byte local. Hash đầy đủ từng file ở `kiem/001/kiem-hash-may.json#/new_match`. |
| `rca-ket-qua/t065-l3-001/` | Chưa có; guard đã kiểm | 175 file dữ liệu/chỉ mục/cấu hình mới. Hash đầy đủ ở cùng `new_match`. |
| compose, Prometheus, Collector, Loki, Tempo, provider, hai dashboard bản 6 | Hash đã đọc trước ghi | 8/8 giữ nguyên. Cặp hash trước/sau đầy đủ ở `kiem/001/kiem-hash-may.json#/existing_unchanged`. |

Snapshot hash là [manifest máy](kiem/001/kiem-hash-may.json); giữ hash trong tạo tác máy đọc được, không rải vào lời báo cáo. `compose.json` trước lượt này đã khác mốc T-061 vì T-063 đổi retention; L3 không sửa compose.

Trình tự:

1. SSH chỉ đọc và chụp hash; kiểm tên thư mục/file mới chưa tồn tại.
2. SCP thư mục dữ liệu mới và hai file dashboard mới. Các lần hoàn thiện chỉ ghi đè file do L3 tạo. Không ghi đè thư mục hoặc dashboard bản 6.
3. File mới chưa được provisioning nạp sau vài phút, dù đã thấy trong container. Restart riêng `flash-ticket-obs-grafana` lần 1 để nạp; thời gian ở `codex/restart-grafana.txt`.
4. Giữ các lượt API lỗi; sửa JSONata, biên cuối, phân loại OTLP. Thử hai panel status mới không đạt sau ba lần; đã rút khỏi bản bàn giao.
5. Restart riêng Grafana lần 2 khi chốt cấu hình trong `codex/restart-grafana-2.txt`; thay đổi sau đó được provisioning nạp. API cuối: UID mới version 6/3, hai UID cũ vẫn 6/6. Không restart Prometheus/Loki/Tempo/Collector.
6. Kiểm 177 file mới khớp local, 8 file cũ giữ hash. Không có đường hầm hoặc browser riêng được mở. Không tạo credential/API key.

Hoàn tác (chỉ là hướng dẫn, chưa thực hiện):

```bash
rm /opt/flash-ticket-obs/pinned/provisioning/dashboards/t065-rca.json
rm /opt/flash-ticket-obs/pinned/provisioning/dashboards/t065-phat-lai.json
rm -r /opt/flash-ticket-obs/rca-ket-qua/t065-l3-001
docker restart flash-ticket-obs-grafana
```

Chỉ xóa đúng hai file và thư mục mới ở trên. Giữ provider, dashboard bản 6, cấu hình kho và mọi thư mục kết quả có trước.


## L4 — 2026-11-14T01:58:59.069Z

- Tạo mới /opt/flash-ticket-obs/rca-ket-qua/t065-l4-001/ và hai file provisioning t065-l4-rca.json, t065-l4-phat-lai.json. Giữ bản 6 và L3. Chỉ cập nhật các file do L4 tạo khi hoàn thiện.
- Trước/sau: codex/l4-obs-truoc.txt và l4-obs-sau.txt; manifest đối chiếu kiem/002/kiem-hash-may.json. 185 file có trước giữ hash; 2.822 file mới khớp local. Cache API/slot và các gói tar của các lượt cũng giữ trong thư mục L4; hash ở remote_only của manifest máy. Không đổi compose/provider/datasource/kho/collector. Folder Grafana vẫn RCA, dữ liệu có thư mục mới.
- File được tự nạp. Agent không phát restart Grafana. Một lần tự restart do Docker ghi oom → die 137 → start lúc 2026-11-14T01:39:46Z; sự kiện có giờ ns trong codex/l4-docker-events.jsonl. Không restart mới trong hai lượt kiểm sau. Không có “hash sau restart do agent” vì agent không restart; hash trước/sau toàn lượt có trong manifest máy.
- Đã giảm tài liệu đọc lặp bằng vue/thao-tac-vue, không tăng RAM hay thay cấu hình. Bản cuối API đạt, không khẳng định chịu mọi tải đồng thời.
- Inventory cuối: bản 6 6/6, L3 6/3, L4 2/2; codex/l4-inventory-cuoi.json. Không có tunnel/browser riêng hoặc tiến trình kiểm còn chạy sau bàn giao. Không tạo credential/API key.

Hoàn tác L4 (hướng dẫn, chưa thực hiện; điều phối duyệt trước khi thay máy): chuyển đúng hai file provisioning L4 ra khỏi thư mục provider, lưu trong t065-l4-001/rollback/. Giữ toàn bộ dữ liệu/cache/lượt chạy L4 để truy vết. Provider disableDeletion=false sẽ gỡ hai UID khi nạp lại; chỉ restart riêng Grafana nếu không tự nạp và đã phối hợp điều phối. Không rút file bản 6/L3 và không đổi provider.

## L5 — 2026-11-14T04:15:16Z — thử folder lồng

- Lệnh: nội dung l5-folder-deploy.py qua Git SSH stdin, python3 -, rồi docker restart flash-ticket-obs-grafana. Chỉ restart Grafana. Guard STOP và sáu hash dashboard + hash provider trước ghi.
- Bỏ folder cố định của provider rca-g2, đặt foldersFromFilesStructure=true. Chuyển sáu file JSON nguyên byte vào cây RCA FlashTicket; thêm UID t065-l5-muc-luc ở 0 · Bắt đầu tại đây. L4 chưa sửa title/tag.
- Hash trước: kiem/003-trinh-duyet/may-truoc.json#/files; hash sau lệnh: folder-deploy.txt; kế hoạch đầy đủ: folder-plan.json. Bản provider cũ: grafana-l5/provider-truoc.yaml. Không sửa compose, datasource, kho hoặc collector.
- Hoàn tác: dùng danh sách moves trong folder-plan.json chuyển đúng sáu file về gốc provisioning (kiểm hash cũ), chuyển file mục lục ra thư mục dữ liệu T-065 để giữ lịch sử, trả provider-truoc.yaml về provider.yaml, rồi restart riêng flash-ticket-obs-grafana. Không xóa dữ liệu/lượt cũ. Chỉ là hướng dẫn, chưa hoàn tác.


- Xác nhận sau nạp: kiem/003-trinh-duyet/kiem-folder.json và folder-sau.json. Dùng cấu trúc lồng vì API parentUid/parents xác nhận đúng. RCA cũ rỗng: l5-obs.py remove-empty-rca qua SSH, DELETE 200 lúc 04:16:03Z. Hoàn tác bằng provider cũ sẽ tạo lại folder RCA; UID folder có thể đổi, UID dashboard vẫn giữ. Hai dashboard General không thuộc bảy dashboard RCA, giữ nguyên.


- L5 UI-01: trước 04:20:40Z, node dashboardL4 dựng lại hai JSON L4; Git SCP chép đúng hai file vào RCA FlashTicket/1 · Kết quả hiện hành. Bản trước: grafana-l5/*-truoc-ui.json; hash trước trong folder-deploy.txt, hash sau sẽ ở manifest máy cuối. Lệnh dựng/SCP và lỗi gốc ghi loi-va-sua.md. Không restart thêm; provisioning tự nạp. Hoàn tác UI riêng: SCP hai bản trước về đúng tên t065-l4-rca.json và t065-l4-phat-lai.json, giữ cây folder; restart riêng Grafana nếu cần.



- UI-02 bổ sung 2026-11-14T04:30:07.2487507Z: Logs panel không dùng noValue cho No data (quan sát thật trên p7/19b17e22). Đưa lời giải thích 0 dòng khớp vào ngay tiêu đề log. Node dựng hai JSON L4 và Git SCP như lần trước; không đổi query hoặc dữ liệu. Hoàn tác UI như trên. Thời điểm này là sau khi SCP xong.



## 2026-11-14T05:39:29.835Z — kiểm lại máy khi tiếp nhận

- Lệnh đọc: l5-may.ps1 và l5-obs.py qua Git SSH với inventory, resume-empty, dashboard-links. Không phát thao tác ghi lên exp-obs khi tiếp nhận.
- may-cuoi.json và doi-chieu-hash-may-l5.json giữ hash trước/sau của provider và sáu dashboard đã chuyển. Bốn dashboard lưu trữ giữ byte. Cả hai L4 đang chạy khớp bản trong grafana-l4/. Cả 7 UID trả HTTP 200.
- Ứng viên UI-03 ở grafana-l5/ui03/ chỉ dựng cục bộ. Giữ hai bản đang chạy trong grafana-l5/*-truoc-ui03.json để đối chiếu và hoàn tác nếu triển khai ở lượt sau.


## 2026-11-14T07:02:49.3542647Z — mốc máy cuối lượt nối Chrome

- Lệnh đọc cuối `& results/T-065/l5-may.ps1 -Nhom 'L5 V032-H5b 4af494a5 dev-2'`. 06:55:59.810701418Z, 376.7 MiB/768 MiB, runner3=0, restart count 0. Không triển khai thêm hay restart trên exp-obs trong lượt nối.
- Dữ liệu kiểm folder và hash ở may-cuoi.json, doi-chieu-hash-may-l5.json. UI-03 chỉ dựng cục bộ, cách hoàn tác và hash bản trước ở các mục cũ.

## 2026-11-14T07:15:56.2497884Z — UI-03/UI-04

- Lệnh node results/T-065/l5-ui-deploy.mjs, sau đó chuyển l5-ui-deploy.py qua Git SSH stdin tới python3 - ui-deploy. Kiểm STOP và hash trước khi ghi, hai file thay nguyên tử lúc 07:15:00Z. Hash trước/sau và backup chính xác ở kiem/003-trinh-duyet/ui04-deploy.jsonl. Không phát restart.
- Chỉ cập nhật t065-l4-rca.json và t065-l4-phat-lai.json trong RCA FlashTicket/1 · Kết quả hiện hành. Các bản trước nằm ở /opt/flash-ticket-obs/rca-ket-qua/t065-l4-001/rollback/l5-ui04/. Hoàn tác UI riêng bằng chép hai backup về đúng tên provisioning, chờ nạp tự động. Nếu cần restart thì chỉ Grafana. Hoàn tác folder/provider vẫn theo mục L5 cũ.
- API kiểm 12 slot, bảng chi tiết và đáp án của ba bản trên T-062/dev. Nguồn null Sức khỏe giữ null và hiển thị lời thiếu giá trị. Đã giữ phản hồi cả lần comparator cũ chưa xử lý null. Không đổi dữ liệu, query sống, hạng, cờ. Kiểm Chrome đang tiếp.


## 2026-11-14T08:33:29.546Z — lượt chat mới: không đổi máy chủ, tunnel riêng

- Lệnh đọc cuối: l5-obs.py inventory qua GitSSH; may-chat-moi-cuoi.json.9 file provider/compose/dashboard khớp may-cuoi.json;6 UID cũ và mục lục giữ nguyên. Không triển khai hoặc restart trong lượt.
- Sau lỗi ERR_CONNECTION_REFUSED, kiểm Get-NetTCPConnection cho thấy13000 chỉ còn TimeWait, không listener. Mở SSH -N -L127.0.0.1:13000:10.0.0.215:3000 với BatchMode/host key đã ghim. Exec session30562,PID24712, giữ cho bàn giao; không đọc/ghi khóa hoặc env.
- Hoàn tác tunnel: chỉ dừng PID24712 sau khi xác nhận vẫn là tunnel do lượt này mở. Không dừng tunnel của Minh hay PID đã được tái sử dụng. Việc này không đổi file máy chủ. Không cần hoàn tác provisioning/dashboard vì lượt này không sửa.


## 2026-11-14T08:59:04.338078+00:00 — UI05: cửa sổ liên kết chính/phát lại

Lỗi/bằng chứng: kiem/003-trinh-duyet/ui04-suite-replay-race.json và DOM tương ứng. Header xuất from=&to= trước khi biến ẩn t_tu/t_den tải. Sửa nguồn l4-dashboard.mjs và chỉ content panel1 của hai JSON L4 dùng __from/__to; targets và UID giữ nguyên. Lệnh node results/T-065/l5-ui05.mjs; truyền l5-ui05-deploy.py qua SSH exp-obs python3 stdin. Thời điểm, hash trước/sau, đường dẫn máy/backup ở kiem/003-trinh-duyet/ui05-plan.json và ui05-deploy.jsonl. Không restart Grafana. Hoàn tác: chép hai JSON từ /opt/flash-ticket-obs/rca-ket-qua/t065-l4-001/rollback/l5-ui05/ về đúng vị trí provisioning; nguồn local và JSON cũ tại grafana-l5/ui05/*-truoc*; chờ provisioning đọc lại, nạp lại tab. Hoàn tác cần quyền đúng phạm vi.


## 2026-11-14T09:06:17.566951+00:00 — URL thời gian và Inspector hiện tại

UI06: đối chứng hiện tại cùng p7/e8661e0a/event-service/panel31: hard navigation numeric URL tạo request from/to NaN và step8760h; ISO cùng instant tạo from1794444870000/to1794445469999, step15s và40dòng/chuỗi. DOM/ảnh inspector-ui05-* giữ nguyên. Không suy nguyên nhân10quan sát lịch sử. Sửa nguồn và hai JSON L4: default time, header, biến ẩn và thời gian danh sách dùng ISO UTC; mọi panel live targets và panel7/24 targets không đổi. Deploy qua stdin SSH, không restart; hash/backup tại ui06-plan.json, ui06-deploy.jsonl và grafana-l5/ui06. Hoàn tác dùng /opt/flash-ticket-obs/rca-ket-qua/t065-l4-001/rollback/l5-ui06/ về vị trí ghi trong manifest deploy; source local có bản sao trước. Numeric bookmark cũ chưa được biến thành hợp lệ; cần ISO URL hoặc chọn ca sau bản sửa.


## L8 — 2026-11-14T16:52:24.329Z — dừng trước xuất/deploy

- Tạo thư mục mới `/opt/flash-ticket-obs/rca-ket-qua/t065-l8-001/` sau guard chưa tồn tại. Chỉ có payload nguồn chụp, script và `kiem/may-truoc.json`; chưa có dữ liệu `du-lieu/`, chưa có dashboard `grafana/` và chưa tạo file provisioning L8.
- `kiem/005-gc-cuoi/may-truoc.json` và `may-sau-chan.json` ghi hash trước/sau; 3.019 file có trước giữ nguyên. Không đổi compose/provider/datasource/collector, không restart Grafana.
- Dừng vì metadata hash cấu hình V082 khác quy ước giữa chỉ mục và đầu ra. Script chỉ đọc nguồn rồi dừng trước xuất. Giữ lượt lỗi và payload; không xóa thư mục mới.
- Nếu Minh yêu cầu hoàn tác, phạm vi chỉ là thư mục mới `t065-l8-001`; chưa thực hiện xóa. Không có dashboard hay container nào cần hoàn tác. Không tự đụng thư mục L3/L4 hoặc bản 6.


## L8b — 2026-11-14T17:30:25.160Z

- Tạo mới /opt/flash-ticket-obs/rca-ket-qua/t065-l8b-001 và hai file t065-l8b-rca.json, t065-l8b-phat-lai.json trong pinned/provisioning/dashboards/RCA FlashTicket/1 · Kết quả hiện hành. Giữ các dashboard/data trước.
- Grafana tự nạp. Không restart container; StartedAt/RestartCount giữ nguyên trước/sau. Hash/byte đầy đủ ở may-l8b/kiem/may-sau.json và deploy.json. 3.019 file máy có trước và 91 file trong thư mục chặn L8 giữ nguyên.
- Fix01 chỉ đổi hai dashboard mới và thêm projection service_options vào case/vue mới. Bản trước hai dashboard lưu /opt/flash-ticket-obs/rca-ket-qua/t065-l8b-001/rollback/fix01; hash trước/sau ở may-l8b/kiem/deploy-fix01.json. Số M1 giữ nguyên; không chạy lại raw/M1.
- Bản nhận và manifest máy ở may-l8b/. SHA gói hai đầu khớp và 2.477 file đã kiểm. Không nhận raw, không đổi compose/provider/datasource/Collector.
- Hoàn tác nếu Minh yêu cầu: chỉ gỡ đúng hai file provisioning L8b và thư mục t065-l8b-001; nếu cần lùi fix01 thì chép đúng hai backup về vị trí ghi trong deploy-fix01.json. Chưa thực hiện hoàn tác/xóa; không tác động thư mục L4/L3/L8 hoặc bản 6.


## L10 — 2026-11-15T03:45:09.877Z — S1 theo gói L9

Chỉ thay file mục lục trong `RCA FlashTicket/0 · Bắt đầu tại đây/`; chuyển hai L4 từ Hiện hành sang `9 · Lưu trữ/L4 · Bộ bản tạm · 14-11/`, giữ UID/byte. Trước ghi kiểm pin live và đích vắng. Không thay hai L8b, provider/datasource/compose; không restart/reload. Hash và đường dẫn đầy đủ: [hash-truoc-sau.json](kiem/008-s1/hash-truoc-sau.json); biên nhận từng thao tác: [ap-dung-001.jsonl](kiem/008-s1/ap-dung-001.jsonl).

API đã nạp đúng mục lục/folder, còn ảnh chưa làm do browser access host và render lỗi. [Báo cáo](kiem/008-s1/BAO-CAO.md). Hoàn tác có điều kiện bằng lệnh trong [HOAN-TAC.md](kiem/008-s1/HOAN-TAC.md); chưa thực thi. Các file byte trước nằm trong `kiem/008-s1/ban-truoc/`.


## L11/L11b — 2026-11-15T05:24:33.664Z — dữ liệu chỉ mục 3 và ba file hiển thị

Tạo /opt/flash-ticket-obs/rca-ket-qua/t065-l11-001/; giữ cây t065-l8b-001 đúng 2.233 pin nguồn/dữ liệu. Chỉ thay hai file t065-l8b-rca.json, t065-l8b-phat-lai.json trong nhánh Kết quả hiện hành và t065-l5-muc-luc.json trong Bắt đầu tại đây. Giữ UID, đổi nguồn dữ liệu/chữ chỉ mục; Mục lục đổi đúng nội dung panel. GET/hash live trước khớp pin; byte trước lưu tại may-l11/rollback và kiem/010-chi-muc-3/ban-truoc. Hash đầy đủ trước/sau ở may-l11/kiem/deploy.json và kiem/010-chi-muc-3/l11b/hash-du-kien.json. File provisioning khác/compose/provider/datasource giữ hash, không restart.

Hoàn tác chỉ khi Minh yêu cầu: sudo python3 -B /opt/flash-ticket-obs/rca-ket-qua/t065-l11-001/codex/l11-may.py rollback; guard GET/hash sau và byte backup trước; lệch pin dừng. Không xóa dữ liệu mới. Hướng dẫn kiểm sau và byte dự phòng: kiem/010-chi-muc-3/l11b/HOAN-TAC.md. Chưa chạy. API 18 trang và hai audit khóa đạt; ảnh bản 3 còn thiếu do công cụ không cấp quyền Chrome.
