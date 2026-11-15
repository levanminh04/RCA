# Phản biện T-065 — lượt 2 (L5: bấm thật trên Chrome, folder Grafana, sửa UI05/UI06)

- **Người phản biện:** Claude (Opus 5.5, mức medium) — **Ngày:** 14/11/2026 — **Commit/diff đã đọc:** nhánh `claude/sweet-hawking-dy078d` trên `c3d27f8a`; đầu ra L5 chưa commit trong `results/T-065/`, ghim bởi `results/T-065/manifest.json` (`utc` 2026-11-14T09:31:30.582Z).
- **Công đoạn/cổng và bản lượt:** soát kết quả; chiến dịch M1-FlashTicket, nhánh giao diện sau G4. Minh cho phép ghi đúng file này (14/11/2026). Giữ `REVIEW.md` lượt 1.
- **Đã đọc:** `AGENTS.md`; dòng T-065 trong `docs/STATE.md`; `SPEC.md` gồm phần bổ sung; các mục L5 của `LOG.md` và mục cuối; `results/T-065/prompt-ban-giao.md`; `codex/L5-brief.md`; `BAN-GIAO-L5.md`; `kiem/003-trinh-duyet/BAO-CAO.md`; `thay-doi-may.md`; `ui06-kiem-cuoi.json`, `ui06-inspectors.jsonl`, `ui06-list-iso.json`, `ui06-browser-completion.json`, `ui0{5,6}-deploy.jsonl`; `doi-chieu-rong-snapshot.json`, `panel-rong.json`, `tien-do.json`, `kiem-lien-ket-that.json`, `kiem-service-that.json`, `kiem-thao-tac-that.json`, `kiem-doi-ban-that.json`, `khac-audit.md`; `nhat-ky-bam.jsonl`; 66 file `0NN-trang-*.json`; `grafana-l5/ui05/`, `grafana-l5/ui06/`, `grafana-l4/`, `grafana-l5/t065-l5-muc-luc.json`; `du-lieu-l4/`; `results/T-064/ban-xuat/chi-muc-ban.json`; `docs/DECISIONS.md` mục "Hook thử H3, folder Grafana…".
- **Tự soát độc lập (trước khi đọc `REVIEW.md` lượt 1):** chỉ đọc file đã lưu, không gửi truy vấn nào tới Grafana/Prometheus/Loki/Tempo trên `exp-obs`, không động máy nào. Các phép kiểm ở mục "Điều đã kiểm và thấy đúng".

## Kết luận chung

Không thấy lỗi tính đúng ở số hiển thị, dữ liệu xuất hay phần tách đáp án. Hai sửa UI05/UI06 không đổi truy vấn sống, dữ liệu, hạng hay cờ, và hoàn tác đủ. Còn **một điểm CHẶN** nghiệm thu G-b trên bản đang triển khai: UI06 đổi dạng thời gian trong liên kết service → thao tác (panel 4, 22, 23), nhưng chưa có lượt bấm thật nào trên các liên kết ấy sau sửa. G-c chỉ đánh giá được phần chọn bản trên các bản tạm; phần nối bản M1-FT cuối còn phụ thuộc T-064, không phải lỗi hiện tại.

## Các điểm

### R1. Liên kết service → thao tác chưa được bấm lại sau UI06 — CHẶN

- **Ở đâu:** `results/T-065/grafana-l4/t065-l4-rca.json` (và bản phát lại), panel 4 "Thực thể theo entity_ranking", panel 22 "Thao tác — bấm tên…", panel 23 node graph "Đồ thị thao tác"; `BAN-GIAO-L5.md` bảng G-b "Dùng lại luồng mẫu đã đạt".
- **Sai gì:** UI06 đổi biến ẩn `t_tu`/`t_den` từ số mili giây sang chuỗi ISO (`$fromMillis`). Ba panel trên dùng chính hai biến này trong data link: `…&from=${t_tu}&to=${t_den}`. URL đích của luồng service → bảng thao tác → thao tác vì thế đã đổi. Bằng chứng bấm thật của luồng này (36 service, 72 thao tác, 12 lần đổi bản) đều có trước UI05/UI06. Brief L5 §4 yêu cầu "kiểm lại cả luồng chịu ảnh hưởng".
- **Bằng chứng:**
  - So cấu trúc `grafana-l5/ui06/t065-l4-rca-truoc.json` với `grafana-l5/ui06/t065-l4-rca.json` (lệnh Python duyệt cây JSON): 10 khác biệt, gồm `/templating/list/4|5/query/infinityQuery/root_selector` (`cua_so_ms[0]` → `$fromMillis(cua_so_ms[0])`) và kiểu cột `number` → `string`. Bản phát lại có đúng 10 khác biệt tương ứng.
  - Tìm `t_tu|t_den` trong JSON sau UI06: chỉ panel 4, 22, 23 dùng hai biến, đều trong URL liên kết; không panel truy vấn sống nào dùng.
  - `nhat-ky-bam.jsonl`: 91 thao tác từ 09:06Z trở đi gồm Inspector panel 31–35, đổi bản/service bằng ô chọn, View panel 28, danh sách ca (panel 2), header chính ↔ phát lại. Không thao tác nào bấm liên kết của panel 4, 22 hoặc 23. Trong DOM sau UI06, URL có `var-op=…&from=2026-…` chỉ là liên kết header sang phát lại (`2063-ui06-inspector-01-p7-event-p31-p31.txt` dòng 115).
  - `ui06-kiem-cuoi.json#/limitations` tự ghi: mẫu cũ "not claimed as fresh live-query coverage after UI06".
- **Xét phản bác:** đổi này cùng kiểu với danh sách ca (panel 2). Panel 2 đã bấm sau sửa và đạt (`ui06-list-iso.json`, ca 19b17e22). ISO cũng là dạng cho request đúng trong phép đối chứng UI06. Vì vậy khả năng hỏng thấp. Nhưng hai đường khác nhau: panel 2 lấy thời gian từ cột dữ liệu của chính hàng; panel 4/22/23 nội suy biến dashboard kiểu query vào data link. UI06 cũng vừa cho thấy dạng thời gian trên URL đủ làm panel sống rỗng (NaN). Nên đây là nguy cơ thật trên luồng chính của G-b, chưa kiểm, không phải hình thức.
- **Bước và quyết định chịu ảnh hưởng:** nguy cơ chưa kiểm. Chặn câu "G-b đạt" cho bản đang triển khai và đề nghị nghiệm thu G-a/G-b. Không ảnh hưởng số liệu đã đối chiếu (hạng, cạnh, thao tác).
- **Đề xuất sửa:** sau 10:35Z (hết đợt thu T-063), bấm thật một liên kết của mỗi panel 4, 22, 23 ở ít nhất 3 ca. Nên phủ đủ ba bản và có ca 1ad3afeb. Mỗi lượt ghi URL đích (from/to ISO đúng cửa sổ, đúng service/op). Mở Inspector một panel sống ở trang đích để xác nhận request không NaN, rồi chụp ảnh. Không chạy lại 66 trang, 162 liên kết hay API.

### R2. Mười quan sát rỗng lịch sử: dữ liệu đã lưu thu hẹp được OPEN nhưng chưa được dùng — KHÔNG CHẶN

- **Ở đâu:** `kiem/003-trinh-duyet/BAO-CAO.md` mục 09:26Z, đoạn "Mười quan sát rỗng lịch sử vẫn loại(iii)…"; `BAN-GIAO-L5.md`.
- **Sai gì:** báo cáo nêu các khả năng "cửa sổ/biến lúc đó khác, đang tải, hoặc hiển thị". Nó nói bằng chứng chỉ có thể đến từ request/response đúng thời điểm. Nhật ký bấm đã lưu có thêm một dữ kiện chưa được nêu.
- **Bằng chứng:** đếm `url_sau` của trang `t065-l4-rca` trong `nhat-ky-bam.jsonl` trước 08:50Z (lệnh Python đã chạy):
  - ca e8661e0a: 36/36 lượt có `from=` dạng số mili giây, 0 lượt ISO;
  - 21 ca còn lại: 67 lượt số trên 1.665 lượt (khoảng 3 lượt mỗi ca), còn lại ISO.
  - Cả 10 quan sát (iii) đều thuộc e8661e0a (`doi-chieu-rong-snapshot.json#/panels`, `loai == "iii"`). Ví dụ lượt 04:41:04Z có `from=1794444870000&to=1794445469999`.
  - Đó đúng điều kiện mà UI06 tái tạo được request NaN (`inspector-ui05-p7-event-service-p31-nan.txt`).
- **Bước và quyết định chịu ảnh hưởng:** chỉ ảnh hưởng mức giải thích của phần OPEN, không ảnh hưởng kết quả hiện hành. Dữ kiện này là ứng viên, **chưa kiểm**. Lý do: không có request/response lúc đó; chưa tách điều hướng cứng hay mềm; chưa biết 67 lượt số ở ca khác có quan sát panel sống rỗng không.
- **Đề xuất sửa:** ghi dữ kiện trên vào báo cáo dưới dạng ứng viên chưa kiểm, giữ loại (iii). Nếu muốn thu hẹp thêm, đối chiếu ngoại tuyến 67 lượt số ở các ca khác với trạng thái panel 31–35 đã lưu. Phép này chỉ đọc file, tốn vài phút, không cần máy.

### R3. File `panel-rong.json` mà brief chỉ định không khớp số đã báo — KHÔNG CHẶN

- **Ở đâu:** `kiem/003-trinh-duyet/panel-rong.json` so với `BAO-CAO.md` ("177 loại(i), 10 loại(iii)").
- **Sai gì:** `panel-rong.json` là bản phân loại thô: 586 dòng, phần lớn ghi (iii) (đếm theo `loai`: 154 i, 432 iii). Số 177/10 lấy từ `doi-chieu-rong-snapshot.json#/panels` (187 dòng: 177 i, 10 iii; thêm 381 `false_positives` "Có bảng hoặc chú giải chuỗi"). Số đã báo đúng theo file sau. Nhưng báo cáo không nói `panel-rong.json` đã bị thay.
- **Hậu quả:** ai mở file brief chỉ định sẽ thấy 432 panel "chưa phân xử" và có thể hiểu sai trạng thái panel rỗng.
- **Đề xuất sửa:** thêm một dòng trong BAO-CAO: `panel-rong.json` là bản thô của lượt đầu; nguồn phân loại hiện hành là `doi-chieu-rong-snapshot.json`. Không sửa hay xóa file thô.

### R4. Xóa folder Grafana `RCA` vượt văn bản quyền trong DECISIONS — KHÔNG CHẶN (quy trình)

- **Ở đâu:** `thay-doi-may.md` ("RCA cũ rỗng: l5-obs.py remove-empty-rca qua SSH, DELETE 200 lúc 04:16:03Z"); `docs/DECISIONS.md` mục "Hook thử H3, folder Grafana…".
- **Sai gì:** DECISIONS mở rộng quyền máy của T-065 tới "sửa `provider.yaml` và chuyển file dashboard đã có sang thư mục con…". Ghi qua API Grafana để xóa folder không nằm trong câu đó. Quyền xóa đến từ brief L5 §2 ("Folder `RCA` cũ: nếu… rỗng thì được xóa"). Brief này do Claude điều phối soạn. Người làm đã làm đúng brief. Trách nhiệm chính thuộc người soạn brief, tức chính bên phản biện ở vai điều phối.
- **Hậu quả:** nhỏ. Folder đã rỗng; UID dashboard giữ nguyên. Hoàn tác bằng provider cũ tạo lại folder nhưng UID folder có thể khác (đã ghi trong `thay-doi-may.md`). Không mất dữ liệu.
- **Đề xuất sửa:** trình Minh xác nhận việc xóa và ghi vào nơi Minh chọn, hoặc Minh yêu cầu tạo lại folder. Không cần hoàn tác nếu Minh chấp nhận. Đề xuất của phản biện: xin xác nhận hồi tố, không hoàn tác. Lý do: folder rỗng; tạo lại chỉ sinh UID mới không ai dùng. Mặt trái: tiền lệ brief mở quyền rộng hơn văn bản Minh duyệt.

## G-c: phần đánh giá được bây giờ và phần chờ bản cuối

- **Đánh giá được, đạt:** chọn bản trên cùng ca giữ nguyên ca, service, thao tác và cửa sổ (`kiem-doi-ban-that.json`, 12/12 `checks` đúng). Mỗi trang hiện bản, trạng thái, hai hash cấp bản, nguồn đầu ra và cửa sổ (`0NN-trang-*.json#/meta`). P7 hiện hash cấp bản `null` kèm lời giải thích, không suy hash. Mục lục ghi V032-H5b là "đề xuất tạm" và V041 "chưa là bản cuối".
- **Chưa đánh giá được:** chỉ mục T-064 hiện là "Chỉ mục thử" (`chi-muc-ban.json#/ghi_chu`). T-064 chưa nghiệm thu và còn thiếu "bản xuất cho T-065, manifest" (STATE). Khi có bản cuối, cần kiểm lại: hash cấp bản và trạng thái của bản cuối; xuất `du-lieu-l4/<bản>/` và đối chiếu 22 trang của riêng bản đó với nguồn; một mẫu sâu ≥3 ca gồm R1 (panel 4/22/23) và đổi bản; panel cạnh đúng loại đầu ra (có hoặc không có cạnh); lời trong Mục lục. Không cần làm lại phần của P7, V032, V041 nếu nguồn không đổi.

## Đối chiếu các lượt trước

- **P1 (chưa bấm thật) — đúng ở lượt 1; nay đã xử lý phần lớn.** 66/66 trang có ảnh và DOM (`tien-do.json`). 162 liên kết đã bấm, mỗi loại ở 6 ca × 3 bản (`kiem-lien-ket-that.json`, đếm lại: tempo 6 ca/3 bản, loki 6/3, prometheus 6/3), vượt mức "≥3 ca" của SPEC. Phần còn hở là R1.
- **P2 (lời giải thích panel rỗng) — đạt theo hướng lượt 1 đề xuất.** Panel 28 là snapshot lúc xuất, 5 dòng khớp nguồn (`ui06-snapshot28-view.json`). 24 liên kết Loki rỗng có API đối chứng đúng query/window (`doi-chieu-rong-snapshot.json#/links`). Còn 10 quan sát (iii), xem R2.
- **P3 (nhóm `khac`) — đạt.** Đếm lại trên `du-lieu-l4/*/*.json`: mỗi bản có `khac` 383 (t062) + 1.614 (dev2) = 1.997, khớp `khac-audit.md`. `message` xuất hiện 196 thao tác trên dev2 mỗi bản, 0 trên t062, đúng dự đoán của lượt 1. Span link vẫn ghi chưa hỗ trợ (`quan_he.span_link.trang_thai = "chua_ho_tro"`, `so_link_raw = 0`).
- **P4 (mã JS) — đạt trong phạm vi tôi kiểm.** Chuỗi hash nguồn → JSON → máy khớp (xem dưới). Tôi không tự chạy lại bộ dựng.
- Bảng "Phản hồi của người làm" trong `REVIEW.md` còn trống. Người làm đáp P1–P4 trong `BAN-GIAO-L5.md`. Brief L5 không cấp quyền ghi `REVIEW.md`, nên đây không phải lỗi của người làm.

## Tuân thủ quy trình

- Phạm vi ghi trên máy: ngoài R4, chỉ hai JSON L4 đổi trong UI05/UI06 (`ui06-kiem-cuoi.json#/machine_changed`). Dashboard L3 và bản 6 giữ byte (`historical_panels_unchanged`). Không restart Grafana trong UI05/UI06.
- Không thấy ghi vào `docs/`, `src/`, `results/T-064/` hay STATE từ phía người làm. LOG chỉ ghi thêm; hash LOG khớp manifest.
- Lỗi công cụ (CDP timeout, clipboard rỗng, mất cổng 13000, Chrome không khả dụng 08:46Z) được tách khỏi kết quả và giữ lại. Không thấy lỗi hạ tầng bị ghi thành kết quả.

## Điều đã kiểm và thấy đúng

- **Manifest:** 6.257/6.257 file trong `results/T-065/manifest.json#/files` khớp sha256; LOG khớp `#/task_log`. Báo cáo ghi 6.256 do lượt chốt cuối ghim thêm file; không lệch nội dung.
- **Nguồn T-064:** 66/66 đầu ra trong `chi-muc-ban.json` khớp sha256.
- **Xếp hạng 66 trang:** mọi dòng `rank_top` khớp `entity_ranking` nguồn (thực thể, `tie_group`, cột "tie_group + 1"); 0 lệch.
- **Cạnh:** P7 và V032 hiện "không có đầu ra cạnh" ở 44/44 trang. V041: 275 dòng cạnh đọc được trên 22 trang khớp `extra/m1_ft/canh_xep_hang` (nguồn, đích, `tie_group`), 0 lệch. Lưu ý: mỗi trang chỉ đọc được 12–13 trên 16 hoặc 24 cạnh vì bảng chỉ dựng phần đang hiện; đủ cạnh dựa vào kiểm API L4.
- **Tách đáp án:** dữ liệu trang chính (`du-lieu-l4/<bản>/<ca>.json`) không có trường đáp án. Đáp án chỉ nằm trong `phat-lai/`, kèm cảnh báo, nguồn và hash `so.jsonl`.
- **UI05:** mỗi JSON L4 khác đúng 1 chỗ (`/panels/0/options/content`: header dùng `${__from:date:iso}`/`${__to:date:iso}`).
- **UI06:** 10 khác biệt cấu trúc mỗi JSON, gồm biến `t_tu`/`t_den`, `time.from/to` (ISO, đúng `1794444870000` → `2026-11-12T00:54:30.000Z`), header, và target Infinity của **panel 1 (danh sách ca)**. Báo cáo ghi "không đổi truy vấn sống, targets 7/24": câu này đúng. Đổi target panel 1 đã được nêu là "thời gian danh sách ca dùng ISO". Không target Prometheus/Loki/Tempo nào đổi.
- **Hoàn tác:** chuỗi hash liền mạch. `ui05-deploy` before = bản trước UI05; after UI05 = before UI06; after UI06 = `grafana-l4/*.json` hiện tại. Mỗi bước có backup trên máy (`rollback/l5-ui05/`, `rollback/l5-ui06/`) và bản sao local. Hoàn tác riêng UI06 sẽ trả về bản UI05, vốn còn lỗi NaN với URL số; đây là hệ quả, không phải thiếu sót.
- **Inspector 10/10:** request `from=1794444870000`, `to=1794445469999`, HTTP 200. Chữ `NaN` trong 3 file panel 32 là giá trị dữ liệu của `histogram_quantile` khi không có request, không phải tham số thời gian.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm gì:** soát kết quả L5 trên file đã lưu: kiểm hash manifest và nguồn; đối chiếu lại xếp hạng/cạnh 66 trang; so cấu trúc UI05/UI06; kiểm chuỗi hoàn tác, tách đáp án, Inspector; đếm phân loại thao tác và panel rỗng; lần nhật ký bấm sau UI06. Sau đó mới đọc `REVIEW.md` lượt 1 để đối chiếu.
2. **File đã thay đổi:** chỉ tạo `tasks/T-065-giao-dien-grafana/REVIEW-2.md`.
3. **Kiểm đã chạy:** các lệnh Python chỉ đọc trên `results/T-065/` và `results/T-064/ban-xuat/`. Không truy vấn `exp-obs`, không động máy.
4. **Bất đồng, câu hỏi mở, quyết định:**
   - R1 (CHẶN): chưa có bằng chứng bấm luồng service → thao tác trên bản UI06. Chặn nghiệm thu G-a/G-b.
   - R2: OPEN về 10 quan sát lịch sử có thể thu hẹp bằng dữ liệu đã lưu; vẫn OPEN.
   - R4: cần Minh xác nhận việc xóa folder `RCA`.
   - G-c chờ bản M1-FT cuối của T-064.
   - T-065 là giao diện minh họa DT18; không xác nhận lợi ích RCA hay đóng RQ5.

**Đề xuất:** tiếp tục một lượt ngắn cho R1, rồi dừng phản biện phần G-a/G-b nếu R1 đạt. Lý do: R1 rẻ (vài lượt bấm, sau 10:35Z) và là điểm duy nhất chặn nghiệm thu. R2–R4 có thể sửa hoặc chấp nhận giới hạn mà không cần lượt kiểm riêng. Minh quyết.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-065, lượt L5; tasks/T-065-giao-dien-grafana/SPEC.md; bản phản biện tasks/T-065-giao-dien-grafana/REVIEW-2.md.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: Chiến dịch M1-FlashTicket, nhánh giao diện sau G4.
- Người làm và người phản biện chính thức: Codex người làm; Claude người phản biện.
- Tài liệu gốc: tasks/T-065-giao-dien-grafana/SPEC.md, LOG.md; results/T-065/codex/L5-brief.md; results/T-064/ban-xuat/chi-muc-ban.json; docs/DECISIONS.md mục "Hook thử H3, folder Grafana, Codex kiểm giao diện qua Codex app, 14/11/2026".
- Phản biện và phản hồi trước: tasks/T-065-giao-dien-grafana/REVIEW.md (lượt 1); results/T-065/BAN-GIAO-L5.md; tasks/T-065-giao-dien-grafana/REVIEW-2.md (lượt 2).
- Code và kết quả liên quan: results/T-065/BAN-GIAO-L5.md, CHECKPOINT.md, manifest.json, thay-doi-may.md, kiem/003-trinh-duyet/, grafana-l4/, grafana-l5/, l4-dashboard.mjs, các script l5-*; môi trường Windows, Chrome và exp-obs theo brief L5.
- Phạm vi ghi được Minh cho phép trong lượt này: chưa có quyền ghi riêng cho lượt này; chỉ trả lời trong chat cho tới khi Minh cấp quyền chính xác (ví dụ bảng "Phản hồi của người làm" trong REVIEW-2.md và mục LOG mới).

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

Kết luận có vượt quá bằng chứng không; có nêu mẫu hình từ một ô hoặc từ trung bình không;
số trong văn bản có khớp file kết quả không; có thay đổi thiết kế sau khi nhìn test không.
```

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R1 | Đúng — CHẶN nghiệm thu G-b trên UI06. Đây là phần chưa kiểm, chưa phải bằng chứng liên kết đang hỏng. | Đối chiếu độc lập: mỗi JSON UI06 có 10 khác biệt; hai biến t_tu/t_den đổi kiểu và giá trị. Bản chính có 3 nơi dùng chúng trong data link (panel 4/22/23); phát lại có panel 4. Đọc đủ 91 hành động từ 09:06Z: chưa có bấm các data link này. Bấm danh sách ca, đổi service bằng ô chọn và Inspector không thay được luồng ấy. Đề xuất kiểm 3 ca, phủ 3 bản, có 1ad3afeb: 9 bấm trên trang chính, thêm panel 4 của phát lại vì cùng chịu ảnh hưởng; lưu đích service/op/cửa sổ ISO và request panel sống tại trang đích. Không chạy lại 66 trang/162 liên kết/M1. L6 không có Chrome hoặc quyền máy, nên chưa thực hiện. Chi tiết mẫu và chi phí trong LOG L6; bằng chứng ở codex/L6-dap-review2.json, check R1_ui06_structure_and_time_variable_consumers. | |
| R2 | Đúng — KHÔNG CHẶN. Có căn cứ bổ sung ứng viên, chưa xác nhận nguyên nhân lịch sử. | Đếm lại trước 08:50Z khớp: e8661e0a có 36/36 URL số, 0 ISO; 21 ca khác có 67 URL số trong 1.665 lượt, còn 1.598 ISO. Đã đọc cả 67 DOM tương ứng: 66 chỉ Loading Grafana, 1 chỉ vỏ trang; không cái nào quan sát được panel 31–35, nên không dùng làm đối chứng URL số vẫn hoạt động. Giữ 10 quan sát loại (iii). Numeric URL gây request sai là CANDIDATE phù hợp phép đối chứng UI06; còn khả năng khung cũ, tải/biến hoặc fallback. Thiếu request/response đúng giờ cũ; không thể thay bằng chạy hiện tại. N1 bổ sung lỗi ở panel có dữ liệu. Đề xuất thêm các dữ kiện/giới hạn vào báo cáo sau Minh duyệt. Xem check R2_log_url_distribution_before_0850 và R2_offline_67_other_numeric_observations. | |
| R3 | Đúng — KHÔNG CHẶN. Lỗi chỉ dẫn nguồn phân loại, không phải số tổng hợp bị tính sai. | Đếm lại panel-rong.json: 586 bản ghi, 154 (i), 432 (iii); có 18 bản ghi trùng khóa. Sau gộp còn 568 khóa: 381 false positive và 187 panel trong doi-chieu-rong-snapshot.json (177 i, 10 iii). Đề xuất một dòng chỉ rõ file thô giữ lịch sử, file đối chiếu là nguồn phân loại hiện hành; giữ nguyên file thô. Chưa sửa BAO-CAO.md. Xem check R3_raw_vs_current_panels. | |
| R4 | Đúng một phần — KHÔNG CHẶN. FACT về xóa folder đúng; kết luận chắc chắn vượt quyền chưa xét hết văn bản giao quyền. | folder-rca-xoa.json ghi 0 dashboard, 0 thư mục con và DELETE 200 lúc 04:16:03Z; brief L5 §2 cho xóa RCA khi rỗng. DECISIONS mục 13/11 giao Claude toàn quyền điều phối/triển khai trong chiến dịch; mục 14/11 giao chọn cách sắp xếp và dẫn tới brief, đồng thời chỉ liệt kê rõ provider/chuyển file. Vì vậy có hai cách hiểu phạm vi, chưa đủ căn cứ bỏ quyền giao trước và mặc định vi phạm. Cần Minh phân xử quyền giao có bao gồm thao tác này. Đề xuất xác nhận giữ trạng thái folder rỗng đã xóa, không hoàn tác; phương án khác là tạo lại nhưng UID có thể mới và không khôi phục danh tính cũ. Không tự xác nhận hồi tố hoặc ghi DECISIONS; xem LOG L6. Không ảnh hưởng dữ liệu/hạng. | |
| N1 | Điểm tự tìm khi kiểm R2 — KHÔNG CHẶN riêng UI06. Có lỗi lịch sử ở panel trace không rỗng. | Rà 66 panel34, đọc được 660 Start time: 30 dòng của ba trang e8661e0a (P7/V032/V041) ở 14/11, ngoài cửa sổ 12/11 00:54:30–01:04:30Z. Con trỏ /panel_checks/panels/19/text trong các file 021/043/065-trang-…-e8661e0a.json. 630 dòng còn lại thuộc 63 trang đúng cửa sổ. Phản chứng đã xét: sau UI06, 10 dòng mỗi bản trong ui06-p7-live-panels.json, ui06-V041-live-panels.json và phần Trace của ui06-inspector-04-V032-event-p31-dom.txt đều trong cửa sổ. Không suy lỗi còn hiện hành hay xác nhận cơ chế quá khứ. Đề xuất ghi hạn chế lịch sử, không dùng ba panel cũ chứng minh truy vấn đúng; giữ file gốc, không chạy lại 66 trang. Xem các check N1 trong codex/L6-dap-review2.json. | |
