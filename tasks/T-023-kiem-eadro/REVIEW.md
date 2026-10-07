# Phản biện T-023

- **Người phản biện:** Claude — **Ngày:** 06/10/2026 — **Commit/diff đã đọc:** `git diff 3b1e0dd` (chỉ docs/DECISIONS.md, docs/STATE.md tracked); results/T-023 và tasks/T-023 chưa tracked, đọc tại cây làm việc.
- **Đã đọc:** SPEC.md, LOG.md (phiên 1–2), kiem-eadro.md, bang-dieu-kien.csv, de-xuat-chia-phien.csv/.md, allowlist-phien.json (B1, intervals), ke-hoach-kiem.md, de-xuat-why.md; scripts b1_reader.py, inspect_approved.py, verify_approved.py; runs/stream-002 (sessions.json, *-safe-spans.csv, cross-session-overlap.csv, metric-stats.csv, normal-quarters.csv, derived-summary.json, cost.json), runs/stream-001/run-status.json, runs/metadata-001/events.csv; DECISIONS Q-61–Q-74; LESSONS; DT18 và hướng dẫn của cô.
- **Ghi chú:** bản này thay bản REVIEW cùng ngày lúc 02:47. Bản cũ kết luận "không có lỗi" nhưng chưa đọc phần phân loại theo giả thuyết trong `sessions.json`. Bảng phản hồi của bản cũ còn trống, không mất phản hồi nào.

## Kết luận chung

Selector, B1, hash và số liệu đều khớp file kết quả. Không thấy nhãn lọt vào phương pháp. Có một lỗi CHẶN. Output của chính stream-002 đã phân loại mọi bản ghi qua B1 theo H−8, và phần lớn rơi đúng vào phiên của nó. Báo cáo không nêu bằng chứng này. Vì thế kết luận clock "OPEN, chưa có căn cứ" và đề xuất CANDIDATE chỉ dùng metric dựa trên bức tranh thiếu. Đây là đúng câu Q-61 cần trả lời. Hai điểm KHÔNG CHẶN.

## Các điểm

### R1. Bằng chứng H−8 đã có trong output nhưng không được báo; kết luận clock và CANDIDATE lệch — CHẶN

- **Ở đâu:** kiem-eadro.md §3 (các câu "FAIL cho ghép theo timestamp native", "OPEN cho khả năng khôi phục", "dịch toàn file theo một offset không tự giải quyết lineage", "Không chọn H−8") và §6 (CANDIDATE); bang-dieu-kien.csv các dòng `log_clock_session_mapping`, `trace_reference_control_independence`; de-xuat-why.md mục C ("không đủ evidence nên không dùng") và mục E.
- **Sai gì:** Báo cáo chỉ báo tọa độ H0. SPEC bước 3 yêu cầu "phân biệt offset clock với trace export lịch sử". Q-61 hỏi trace "ghép được với phiên và mốc tiêm" không. Gate đã ghi `admitted_classifications` theo cả ba H. Số đó ủng hộ mạnh giả thuyết lệch cố định 8 giờ, cộng với export tích lũy. Báo cáo lại để các giải thích ngang nhau, rồi đề xuất bỏ trace/log.
- **Bằng chứng:**
  - `sessions.json → trace/log.gate.admitted_classifications`. Theo H0 và H+8: 0 bản ghi trong chính phiên, ở cả năm phiên. Theo H−8:

    | Phiên | Span qua B1 | H−8 trong chính phiên | H−8 ở phiên khác | H−8 ngoài mọi phiên | Log qua B1 | Log H−8 trong chính phiên |
    |---|---:|---:|---:|---:|---:|---:|
    | dev 150729 | 1.382 | 0 | 0 | 1.382 | 0 | — |
    | dev 165807 | 7.846 | 6.814 | 0 | 1.032 | 4.000 | 4.000 |
    | dev 184759 | 18.491 | 17.196 | 263 (dev 165807) | 1.032 | 10.016 | 10.016 |
    | reference | 23.669 | 23.669 | 0 | 0 | 13.668 | 13.668 |
    | control | 32.420 | 23.719 | 8.701 (reference) | 0 | 13.668 | 13.668 |

  - Mốc trong allowlist B1: dev 150729 bắt đầu 2022-04-17T23:07:29Z, bằng tên phiên trừ 16 giờ. Span nhỏ nhất của reference là 2022-04-21T02:51:58Z, bằng tên phiên trừ 8 giờ. Vậy trace/log và nhãn/metric lệch nhau đúng 8 giờ.
  - Overlap không chống lại giả thuyết offset. Tôi đã nhóm `*-safe-spans.csv` theo giờ native. 2.390 variant chung giữa reference và control ứng với 8.701 dòng của control. Tất cả nằm ở 04-21 04–05h UTC, tức đúng khoảng của reference theo H−8. 263 dòng dev 184759 chung với dev 165807 nằm ở 04-18 10h, tức khoảng của dev 165807. Đây là export tích lũy tràn qua biên phiên, tách được theo thời gian. Câu "dịch toàn file… không tự giải quyết lineage" đúng khi chỉ dịch mà không lọc theo khoảng phiên. Câu đó không làm yếu bằng chứng offset.
  - Hệ quả của B1 không được nêu. Dưới H−8, nhánh H0 của B1 có thể đã loại chính dữ liệu trong phiên của dev 150729 và dev 165807. Dev 150729 có 14.705 span và 5.663 log bị loại vì nằm trong khoảng native của test 04-18T222801. Dịch −8h, khoảng đó thành 22:28–00:15Z, chồng với dev 150729 [23:07, 00:55]. Dev 165807 có 9.810 span và 5.713 log rơi vào khoảng test 04-19T001753. Dịch −8h thành 00:17–02:05Z, chồng với dev 165807 [00:58, 02:45]. Đây là suy từ số học khoảng thời gian, **chưa kiểm**: gate không lưu phân loại H−8 của bản ghi bị loại. Hệ quả: theo mọi H, dev 150729 không còn dữ liệu an toàn trong phiên; dev 165807 còn một phần; chỉ dev 184759 gần đủ.
  - **Đoạn có thể phản bác:** allowlist ghi `clock_alignment: forbidden`. Báo cáo không căn chỉnh là đúng. Nhưng báo số đếm gate đã có thì không phải căn chỉnh. Kế hoạch §3 cũng yêu cầu cân các giải thích. Cũng đúng là chưa có nguồn clock bên ngoài, và chưa kiểm 54 cửa sổ theo H−8. Vậy clock nên ghi "bằng chứng nội tại ủng hộ offset 8h, chưa có nguồn xác nhận, chưa kiểm mức cửa sổ". Không nên để là các giải thích ngang nhau.
- **Hậu quả:** Ở Q-61, Minh phải chọn: đưa trace Eadro vào, chỉ dùng metric/log, hay bỏ. Báo cáo hiện kéo quyết định về phía chỉ dùng metric mà không có bằng chứng tương xứng. Hướng dẫn của cô có bước "ánh xạ log/trace lên đồ thị". Eadro là bộ có cả trace và log, nên bỏ trace của nó làm yếu thêm phần "mở rộng dataset". Phần yếu đi này Minh chỉ chấp nhận ở Q-61 cho trường hợp trace thật sự không ghép được.
- **Đề xuất sửa:** Không chạy gì mới. Chép bảng trên từ `sessions.json` vào kiem-eadro §3. Ghi rõ dữ liệu ủng hộ lệch cố định 8h giữa trace/log và nhãn/metric, cộng với export tích lũy. Ghi các giới hạn: chưa có nguồn xác nhận, chưa kiểm mức cửa sổ, B1 đã cắt dev 150729/165807. Sửa câu về lineage ở §3 và câu "không đủ evidence" ở WHY-C. Ở §6, thêm phương án "Minh duyệt kiểm cửa sổ theo H−8 trên phần đã qua B1", nêu đúng bằng chứng hiện có. Minh chọn.

### R2. Conflict identity và overlap của dev nằm ở khối lịch sử chung, nhưng được báo như thuộc tính của phiên — KHÔNG CHẶN

- **Ở đâu:** kiem-eadro.md §4 (bảng identity, câu "FAIL nếu dùng identity dev…", câu "Ba cặp dev có 222/222/324 variant"), §6 dòng MicroRank ("FAIL coverage/identity dev hiện tại"); bang-dieu-kien.csv ba dòng `trace_identity_conflicts` của dev.
- **Sai gì:** Báo cáo đếm 136/136/148 conflict theo cả phiên, không tách theo thời gian. Phần lớn conflict nằm ở một khối span ngày 16/04. Khối này giống hệt nhau ở cả ba file dev và nằm ngoài mọi phiên, dưới cả ba H.
- **Bằng chứng:** tôi đã nhóm `*-safe-spans.csv` theo giờ native (chỉ đọc output). Mỗi file dev có cùng khối 1.032 span ở 04-16 13h và 18–20h UTC. Cả 136 conflict của dev 150729 và dev 165807 đều nằm trong khối đó. Dev 184759 có 136 conflict trong khối, cộng 12 conflict ở 04-18 12h. Phần dev 165807 nằm trong phiên theo H−8 có 6.814 span và 0 conflict. Overlap dev 150729–165807 và dev 150729–184759 là 222 variant, ứng với 688 dòng, cũng nằm hết trong khối 16/04. Reference và control có 0 conflict.
- **Đoạn có thể phản bác:** báo cáo có ghi "safe subset only", và câu FAIL ở §4 có điều kiện ("nếu… gộp last-wins"). Vì vậy số liệu không sai. Phần bị thổi lên là hàm ý cho MicroRank/TraceRCA.
- **Hậu quả:** Minh có thể coi conflict là lý do chặn trace dev. Thực ra conflict nằm ở khối không thuộc cửa sổ nào.
- **Đề xuất sửa:** Ở §4, tách đếm identity theo khối thời gian. Dữ liệu đã có trong safe-spans.csv. Ghi rõ conflict tập trung ở khối 16/04. Sửa câu hệ quả của dòng MicroRank ở §6 cho khớp.

### R3. CIRCA-PC được nêu là ứng viên metric cho Eadro-TT, trái Q-67 — KHÔNG CHẶN

- **Ở đâu:** kiem-eadro.md §6, dòng "BARO, N-Sigma scorer, CIRCA-PC"; bang-dieu-kien.csv dòng `BARO_NSigma_scorer_CIRCA_PC`.
- **Sai gì:** Q-67 ghi CIRCA-PC "không chạy đủ trong ngân sách" trên Train Ticket. Q-62 xếp CIRCA-PC vào tầng 2. Eadro-TT là Train Ticket. Ghi "có thể là ứng viên metric" có thể làm lệch phạm vi T-027.
- **Bằng chứng:** DECISIONS dòng Q-67 và Q-62.
- **Đề xuất sửa:** Bỏ CIRCA-PC khỏi dòng ứng viên, hoặc ghi kèm "theo Q-67 không chạy trên TT". PASS schema numeric vẫn giữ.

## Điều đã kiểm và thấy đúng

- **Selector và B1:** đã đọc code. Gate quét byte để lấy clock trước `json.loads`. Process chỉ được giải mã cho span đã qua gate. Log chỉ đọc prefix thời gian trước. Member trong TAR được `require` trước `extractfile`. Hash ZIP được kiểm trước khi mở member, không gọi `testzip`. opened-members có đúng 145 member của 5 phiên đã duyệt. Không thấy test, TT-all, TT-no-fault hay phiên 20/04.
- **Chạy lại rẻ:** gọi `verify_approved.main(stream-002, 'fixture-002')` trong bộ nhớ, với `-B`: PASS 96 kiểm, không ghi file.
- **Số khớp file:** 11 PASS / 13 FAIL / 14 OPEN trên 38 dòng. 6.727.833 = (6.462 + 6.461 + 6.460 + 2 × 8.107) × 189. Kênh hằng 25/27/25/29/25. Pre 2,7065 s và 114,1415–124,4105 s. Tỷ số chuẩn hóa: n = 55, Q50 0,0141, min/max −33,2/+6. Chênh log−span: max 162,1554/65,0390 s. Chi phí 264,109 s và 145.293.312 byte. Tất cả khớp sessions.json, derived-summary.json, cost.json.
- **Nhãn:** root/fault chỉ có ở cột `*_audit_only`. Khoảng test dùng cho B1 là để bảo vệ dữ liệu, không là đầu vào phương pháp. Không có offset, SLI hay kênh nào được chọn theo root.
- **Phạm vi ghi:** file của T-023 chỉ ở results/T-023, LOG và dòng T-023 trong STATE. Không có `__pycache__` hay `work/`. Stream-001 được giữ, có run-status ghi rõ không dùng cho kết luận.
- **WHY/LESSONS:** chia phiên, nguồn normal và B1 đều có nháp WHY. Trạng thái ghi đúng là USER_CONFIRMED hoặc CANDIDATE. Chưa lựa chọn nào được dùng làm cấu hình phương pháp. Số trong văn bản lấy từ file, khớp SL17. Phần reference ghi OPEN tính đại diện, không gọi PASS chỉ vì đủ finite/cadence.

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| R1 | Đúng một phần; đồng ý CHẶN việc chốt báo cáo hiện tại để Minh quyết Q-61 | Kiểm lại `sessions.json → trace/log.gate.admitted_classifications`: H−8 khớp chính khoảng phiên với 0/6.814/17.196/23.669/23.719 span và 0/4.000/10.016/13.668/13.668 log, còn H0/H+8 đều 0. Đây là bằng chứng nội tại quan trọng bị bỏ sót; tự soát trước REVIEW cũng đã bỏ sót. 8.701 dòng control và 263 dòng dev 184759 thuộc khối thời gian phiên trước theo H−8, nên overlap không bác giả thuyết offset kết hợp export tích lũy. Đồng ý bổ sung bảng và cân lại CANDIDATE. Không đồng ý nâng “lệch nhau đúng 8h” thành FACT: tên phiên/minimum không xác minh clock nguồn; count thuộc toàn phiên sau B1 không xác nhận từng cửa sổ/mốc tiêm. OPEN cho khả năng ghép vẫn cần giữ. Số record own bị B1 loại chưa xác định vì không có timestamp/phân loại H−8 của phần bị loại; suy luận reviewer đã ghi chưa kiểm phải giữ mức đó. Đề xuất sửa báo cáo/WHY và thêm phương án kiểm H−8 để Minh cân nhắc; chưa thực hiện kiểm cửa sổ mới hoặc áp offset vì policy hiện tại cấm căn chỉnh. Chi tiết và phạm vi sửa ở LOG phiên 3. | |
| R2 | Đúng một phần; KHÔNG CHẶN | Đếm lại safe-spans: cả ba dev có khối native 16/04 gồm 1.032 dòng, 358 khóa, 136 conflict; khối này ngoài mọi khoảng B1 đã biết dưới H0/±8h. Dev 165807 có 6.814 dòng khớp chính phiên theo H−8 và 0 conflict; dev 184759 có 17.196 dòng tương ứng và vẫn có 12 conflict. Hai overlap 222 variant ứng 688 dòng/file đều ở khối 16/04. Đồng ý thiếu phân tầng và câu MicroRank dễ làm người đọc hiểu conflict rộng hơn bằng chứng. Bảng tổng safe không sai: §4 ghi “trong phần safe”, câu FAIL có điều kiện last-wins, §4 cũng gọi coverage lịch sử. Vì thế không nhận lỗi số hay kết luận tất cả conflict ngoài incident. Đề xuất tách khối thời gian đã biết, giữ giới hạn ba H/clock OPEN và sửa hệ quả MicroRank; không gọi graph tại injection đã PASS. | |
| R3 | Đúng một phần; KHÔNG CHẶN | Q-62 đặt CIRCA-PC ở tầng 2; Q-67 yêu cầu báo không chạy đủ trong ngân sách trên Train Ticket. Đồng ý câu “ứng viên metric” thiếu nhắc giới hạn này, có thể gây hiểu sai phạm vi T-027; đề xuất thêm ghi chú Q-67 và giữ lựa chọn chạy cho Minh. PASS schema numeric không trái Q-67: §6 nói rõ chưa chạy/xác nhận toàn phương pháp, CSV giữ benchmark pending. Chưa có thực nghiệm CIRCA-PC Eadro hay thay quyết định. Cũng chưa có bằng chứng thời gian Eadro: 189 kênh khác các phép đo RE2 273–292 biến, nên không suy bất khả thi thực tế từ cùng tên Train Ticket. | |

---

# Phản biện tiếp T-023 — bản sửa R1–R3 ngày 06/10/2026

- **Người phản biện:** Claude — **Ngày:** 06/10/2026.
- **Phạm vi:** Minh yêu cầu phản biện tiếp sau review và phản hồi của người làm. Đối chiếu bản sửa ở LOG phiên 4. Giữ nguyên phần review cũ và bảng phản hồi; chỉ nối thêm phần này.
- **Đã đọc:** AGENTS.md, STATE, docs/review-prompt.md, SPEC, LOG phiên 3–4, bảng phản hồi ở trên; `results/T-023/kiem-eadro.md`, `bang-dieu-kien.csv`, `de-xuat-why.md`, `scripts/summarize_approved.py` (các template điều kiện); `allowlist-phien.json → B1`; `runs/stream-002/sessions.json` và năm `*-safe-spans.csv`. File T-023 chưa tracked nên đọc tại cây làm việc.

## Kết luận chung

R1, R2, R3 đã được xử lý đúng phạm vi Minh duyệt. Bảng H−8, bảng khối 16/04, 12 conflict của dev cuối và ghi chú Q-62/Q-67 đều khớp `sessions.json` và safe-spans. Template script sinh đúng câu mới trong CSV.

Không còn điểm CHẶN. Còn hai điểm KHÔNG CHẶN, cùng một gốc: báo cáo mới dùng số đếm theo khoảng phiên, chưa dùng biên thời gian của phần safe. Biên đó đã có trong output. Nó làm bằng chứng H−8 mạnh hơn mức báo cáo ghi. Nó cũng cho thấy phương án "kiểm cửa sổ H−8 trên phần safe" chỉ phủ được khoảng một nửa thời gian dev. Cả hai ảnh hưởng tới cách Minh cân các phương án ở Q-61.

## Các điểm

### V2-S1. Biên phiên khớp dưới một giây theo H−8, nhưng báo cáo vẫn để "trễ báo" ngang các giải thích khác — KHÔNG CHẶN

- **Ở đâu:** `kiem-eadro.md` §3 (câu "timezone, cách biểu diễn thời gian và trễ báo vẫn cần phân biệt"; câu "Tên phiên/minimum không là nguồn đồng bộ clock/export"); `de-xuat-why.md` mục C ("chưa phân xử được … trễ báo"); bảng phản hồi R1 ("minimum reference chỉ khớp tên trừ 8h xấp xỉ").
- **Sai gì:** Phản hồi R1 bác bằng chứng minimum vì "tên phiên không là nguồn clock". Nhưng mốc so sánh không phải tên phiên. Nó là `metric_start_s` trong allowlist B1, lấy từ sample metric đầu tiên. So span safe (trừ 8 giờ) với mốc metric, biên đầu khớp dưới một giây ở ba phiên. Đây là phép đối chiếu trực tiếp giữa đồng hồ trace và đồng hồ metric. "Xấp xỉ" là mô tả sai mức khớp.
- **Bằng chứng:** đọc năm `*-safe-spans.csv` và `allowlist-phien.json → B1.intervals`; không mở raw, không đổi input.

  | Phiên | Span đầu trong phiên (H−8) so với sample metric đầu | Span cuối so với mốc cuối của phiên | Span safe gần nhất trước phiên | Span sau mốc cuối |
  |---|---:|---:|---|---:|
  | dev 184759 | +0,343 s | −48 s | 02:44:55,9 (thuộc dev 165807) | 0 |
  | reference | +0,090 s | −13 s | không có | 0 |
  | control | +0,742 s | −24 s | 21:06:52,5, tức trước 2 giờ 26 phút | 0 |
  | dev 165807 | +68,0 phút (xem V2-S2) | −53 s | 04-16 12:44 (khối lịch sử) | 0 |

  Giờ ở bảng là tọa độ metric (native trừ 8 giờ). Ở control, export im lặng 2 giờ 26 phút, rồi có span đầu tiên 0,74 s sau sample metric đầu tiên. Ở cả bốn phiên, không span nào nằm sau mốc cuối. Phủ theo phút: dev 184759 107/108 phút, reference và control 135/136 phút.
- **Đoạn có thể phản bác:** chỉ có biên phiên, chưa có biên từng cửa sổ tiêm. Chưa biết đồng hồ nào lệch: trace có thể đúng UTC còn metric/nhãn lệch, hoặc ngược lại. Vì vậy giữ OPEN cho mức cửa sổ là đúng. Nhưng trễ báo, hoặc một offset khác 8 giờ vài phút, không cho biên đầu khớp dưới một giây ở ba phiên. Còn câu hỏi "đồng hồ nào sai" không ảnh hưởng việc ghép, nếu offset là hằng.
- **Hậu quả:** Minh đọc §3 sẽ thấy H−8 là "giả thuyết được ủng hộ" ngang với trễ báo. Thực tế bằng chứng mạnh hơn thế. Điều này ảnh hưởng tới việc chọn giữa "kiểm H−8", "chỉ metric" hay "bỏ".
- **Đề xuất sửa:** thêm bảng biên ở trên vào §3. Ghi rõ mốc so là sample metric đầu/cuối, không phải tên phiên. Bỏ "trễ báo" khỏi danh sách giải thích ngang hàng, hoặc ghi rằng biên dưới một giây làm nó yếu đi. Giữ OPEN cho mức cửa sổ tiêm và nguồn clock. Sửa câu tương ứng ở WHY-C. Không chạy gì mới.

### V2-S2. Phần safe chỉ phủ khoảng một nửa thời gian dev; danh sách phương án bỏ sót cách duy nhất khôi phục được dev 150729/165807 — KHÔNG CHẶN

- **Ở đâu:** `kiem-eadro.md` §3 (đoạn B1 "chưa kiểm ở mức record… có thể sai nếu…"), §6 CANDIDATE thứ nhất ("có thể không đủ do dev đầu rỗng và dev thứ hai bị cắt"); `de-xuat-why.md` mục D (hạn chế censor) và mục E (các CANDIDATE, "Khác đã xét").
- **Sai gì:** hai việc.
  1. Báo cáo coi việc B1 cắt mất dữ liệu own là suy luận yếu, "có thể sai". Biên safe cho thấy chỗ cắt trùng đúng biên khoảng cấm. Dev 165807: span own đầu tiên ở native 10:06:04,6, tức 30 s sau khi khoảng test 001753 (dưới H0) kết thúc lúc 10:05:34. Từ khối 16/04 tới đó không có span safe nào. Dev 150729: span safe cuối ở native 06:27:16, tức 45 s trước khi khoảng test 222801 (dưới H0) bắt đầu lúc 06:28:01. Ở dev 184759, reference và control, phần own bắt đầu ngay ở giây đầu phiên. Vậy dev 165807 mất 68 trong 108 phút đầu là do B1, không phải do export bắt đầu muộn. Số record own bị mất vẫn chưa biết: một phần 9.810 span bị loại có thể thuộc khoảng của dev 150729 dưới H−8.
  2. Vì thế, phương án "kiểm cửa sổ H−8 trên phần safe" chỉ phủ: dev 150729 = 0 phút; dev 165807 = 39 phút cuối trong 108 phút; dev 184759 = gần đủ. Phần phủ lệch về cuối ngày dev, không ngẫu nhiên. Báo cáo chỉ ghi định tính "có thể không đủ". Danh sách phương án ở §6 và WHY-E không nêu cách duy nhất khôi phục được hai dev đầu: Minh duyệt sửa B1 cho riêng member dev, ví dụ bỏ H0 khỏi hợp loại bỏ nếu Minh chấp nhận H−8. Báo cáo chỉ ghi "không mở lại hoặc phục hồi phần B1 đã loại" như một điều cố định.
- **Bằng chứng:** cùng lệnh ở cuối phần này; `sessions.json → denied_by_interval_hypothesis` (dev 150729: 14.705 span ở 222801; dev 165807: 9.810 span ở 001753). Phần bị loại nằm trong member dev đã được duyệt, không phải member test.
- **Đoạn có thể phản bác:** B1 dùng hợp ba H là để bảo vệ test khi chưa biết clock (kế hoạch §8). Nếu H0 mới đúng, đọc lại phần đó là đọc telemetry đúng thời gian test, dù nằm trong file dev. Rủi ro này có thật. T-023 cũng không được tự đổi quyền. Vì vậy đây không phải lỗi của B1 hay của việc không đọc lại. Điểm này chỉ nói danh sách phương án trình Minh chưa đủ, và giới hạn của phương án đầu chưa được định lượng.
- **Hậu quả:** Minh có thể duyệt kiểm H−8 trên phần safe mà không biết trước rằng nó chủ yếu trả lời cho dev 184759 cộng phần cuối dev 165807. Minh cũng không thấy phương án đổi B1 cùng rủi ro của nó. Lựa chọn ở Q-61 vì vậy dựa trên danh sách thiếu.
- **Đề xuất sửa:** ở §3 và WHY-D, ghi biên cắt trùng biên khoảng cấm, kèm số phút phủ của từng dev. Vẫn ghi số record bị mất là chưa kiểm. Ở §6 và WHY-E, ghi phạm vi phủ thật của phương án đầu. Thêm phương án "Minh duyệt sửa B1 cho member dev nếu chấp nhận H−8", nêu rõ rủi ro nếu H0 đúng. Không chọn phương án, không chạy gì mới.

## Điều đã kiểm và thấy đúng

- **R1:** bảng H−8 ở §3 khớp `sessions.json → admitted_classifications` từng số: span 0/6.814/17.196/23.669/23.719, log 0/4.000/10.016/13.668/13.668, 263 và 8.701 khớp phiên khác. H0/H+8 own đều 0. Câu "FAIL native không chứng minh trace không thể ghép" đã có ở phần tóm tắt và §3. Phương án kiểm H−8 đã vào §6 và WHY-E. Câu về lineage đã viết lại đúng.
- **R2:** bảng khối 16/04 (1.032 dòng, 358 khóa, 136 conflict mỗi dev; 0/0/12 conflict ở nhóm own) khớp đếm của tôi trên safe-spans. Dòng MicroRank ở §6 và ba dòng `trace_identity_conflicts` trong CSV đã ghi phạm vi "toàn phần safe, chưa là incident".
- **R3:** dòng CIRCA-PC ở §6 và CSV đã ghi Q-62/Q-67. PASS schema không còn hàm ý đưa vào T-027.
- **Script:** template `summarize_approved.py` dòng 118–145 sinh đúng câu đang có trong CSV, kể cả nhánh "own H-8 safe group empty here" cho dev 150729. Verdict 11 PASS/13 FAIL/14 OPEN không đổi.
- **Phạm vi ghi:** theo LOG, phiên 4 chỉ đổi bốn file đã duyệt, LOG và STATE. Người làm giữ ý kiến khác (không nâng H−8 thành FACT). Đó là quyền của người làm, không tính là lỗi; V2-S1 chỉ nói về mức khớp ở biên phiên.

## Lệnh đã chạy

Chỉ đọc, `py -3 -B -c` tại `results/T-023`, không ghi file. Với mỗi phiên trong `approved_sessions`: đọc `runs/stream-002/<phiên>-safe-spans.csv`, lấy `native_start_s − 28800`, so với `start_s`, `end_s`, `metric_start_s`, `metric_end_s` của phiên trong `allowlist-phien.json → B1.intervals`. In span cuối trước phiên, span đầu và cuối trong phiên, số span sau phiên, số phút có ít nhất một span. Không đối chiếu với mốc tiêm từng sự kiện, không tạo input đã dịch giờ cho phương pháp. Không mở archive, `data/locked/` hay repo lưu trữ.

Phiên phản biện này chỉ nối thêm phần trên vào REVIEW.md. Không sửa LOG, STATE hay file kết quả. Không commit.

**Cần Minh quyết:** có sửa theo V2-S1, V2-S2 không. Nhánh Eadro cho T-027 và việc ghi DECISIONS/WHY chung vẫn chờ Minh như LOG phiên 4 đã ghi.

## Phản hồi của người làm cho phần phản biện tiếp (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| V2-S1 | Đúng về mức khớp biên và thiếu bằng chứng trong báo cáo; đã sửa theo đề xuất | Kiểm năm safe-spans CSV và B1: span own đầu H−8 so với sample metric đầu ở dev 184759/reference/control là +0,343/+0,090/+0,742 s. Đồng ý đây là đối chiếu trực tiếp với metric, không phải tên phiên; cách diễn giải cũ đánh giá thấp bằng chứng. Span cuối so metric_end_s là −45,943/−11,540/−22,388 s, còn so end_s là −47,894/−12,545/−24,350 s; tách hai mốc để không gọi số làm tròn của reviewer là chênh với sample cuối. Không span safe nào vượt end_s dưới H−8 ở cả năm file. Đã bổ sung bảng §3 và WHY-C, làm yếu giải thích trễ báo đơn thuần. Giữ OPEN nguồn clock/từng cửa sổ, chưa áp H−8. Phần R1 cũ được giữ làm lịch sử; phản hồi này cập nhật bằng chứng biên. | Minh đã duyệt nguyên lời: “đồng ý sửa theo V2-S1 và V2-S2”. Đã thực hiện sửa báo cáo, không chọn clock/nhánh. |
| V2-S2 | Đúng về biên cắt, giới hạn phần safe và thiếu phương án; số own bị loại chưa kiểm | Kiểm B1/safe-spans: dev 150729 có safe cuối 44,585 s trước test 222801 H0; dev 165807 có own safe đầu 30,586 s sau test 001753 H0, trễ metric đầu 67,961 phút. Own safe là 0/6.814/17.196 span; khoảng từ span đầu tới cuối là 0/38,855/106,879 phút. Đếm nhất quán ô 60 s neo metric_start_s cho 0/40/107 trên 108 ô, khác khoảng thời gian “39 phút cuối”. Denied counts 14.705 và 9.810 span khớp sessions.json, nhưng không là số own mất vì thiếu timestamp/phân loại record bị loại. B1 cắt có hệ thống nếu H−8 đúng; output safe không loại trừ nguồn cũng thiếu dữ liệu, nên không khẳng định export chắc chắn không bắt đầu muộn. Đã sửa §3/§6, WHY-D/E, định lượng phương án kiểm safe và thêm CANDIDATE Minh duyệt sửa B1 riêng member dev nếu chấp nhận H−8, nêu rủi ro đọc thời gian test nếu H0 đúng. Chưa đổi quyền, đọc lại hoặc chọn phương án. | Minh đã duyệt nguyên lời: “đồng ý sửa theo V2-S1 và V2-S2”. Đã thực hiện sửa báo cáo; phương án B1 mới vẫn chưa được chọn/duyệt thực hiện. |
