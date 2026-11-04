# Nhật ký T-047

Chỉ người làm ghi file này; phiên phản biện không ghi (AGENTS mục 9). Chỉ ghi thêm vào cuối, không sửa mục cũ. Mỗi phiên một mục. Mục phải đủ để một agent khác, trên máy khác, không có lịch sử chat, làm tiếp được.

- SPEC do Claude soạn trong chat ngày 01/11/2026; Codex rà bản 1 cùng ngày (hai điểm KHÔNG CHẶN: kiểm manifest lịch sử; đơn vị ngân sách), đã sửa theo cả hai.
- Minh duyệt tạo SPEC ngày 01/11/2026 (lời Minh: “duyệt tạo spec luôn …”, cùng lúc với SPEC T-046). Triển khai sau khi T-046 được nghiệm thu. Quyền chạy dài và qua đêm chờ Minh khi mở task.
- Người làm: Codex. Người phản biện: Claude.

## Phiên 1 — mở phiên 2026-11-02T08:41:23+07:00

- Agent: Codex; thiết bị: LeVanMinh, Windows local của Minh; vai trò: người làm T-047 (Q-229).
- Phân loại: EXECUTE giới hạn — tự rà SPEC và trình đề xuất; chưa chạy thực nghiệm. Quyền theo prompt Minh đính kèm ngày 02/11/2026: bước 0, nối LOG, dòng T-047 của STATE.
- Minh cho phép dùng subagent trong chat; dùng đúng hai subagent chỉ đọc để hỗ trợ tự rà; Claude giữ vai trò phản biện chính thức. Không đọc mục Phiên 1 (tiếp 5) của LOG T-046 trước khi ghi danh sách tự tìm.
- Branch: claude/sweet-hawking-dy078d; HEAD: 2d908df4ec25e429cd262e266c01985a644afd62; code nghiệm thu src: c298188e.
- Bắt đầu kiểm manifest theo revision lịch sử và test -B; không chạy chuỗi dữ liệu, không đọc nhãn dev hay data/locked.

### Bước 0 và tự rà độc lập — 2026-11-02T08:48:20+07:00

Danh sách dưới đây được ghi TRƯỚC khi đọc LOG T-046 mục “Phiên 1 (tiếp 5)”. Hai subagent chỉ hỗ trợ tự rà của người làm, không là lượt phản biện chính thức và không ghi file. Chưa chạy chuỗi T-047, chưa đọc nhãn dùng chấm, chưa mở dữ liệu khóa.

**Kiểm đầu vào:**
- Đối chiếu từng entry và tập file kết quả theo manifest: T-043 69/69; T-044 2.133/2.133; T-045 6.085/6.085; T-046 933/933, không thiếu/thừa/lệch. T-043 10/10 hash đóng băng khớp. Với src/m1, T-044 kiểm bằng git show tại 69ef90b6; T-045 tại bbef69dd (17 file mỗi manifest); T-046 kiểm hiện tại. Không sửa manifest.
- Test T-044: 374 passed, 2 warnings, 45,74 giây. Test T-045: 16 passed, 1 warning, 9,03 giây. Test T-046 đang chạy; kết quả chốt sẽ nối sau. Dùng Python -B và -p no:cacheprovider, PYTHONDONTWRITEBYTECODE=1; không ghi báo cáo test ngoài quyền. Có một lần lệnh in metadata thất bại do cp1252; chạy lại với PYTHONIOENCODING=utf-8. Lệnh inventory thử có bộ lọc pyc không đồng nhất T-045; sửa bộ lọc và xác nhận không thiếu/thừa, không phải mất file. Hai lời gọi test T-045/T-046 ban đầu bị phần hiển thị công cụ lược đầu ra; chạy lại để lấy kết quả xác nhận được, không dùng lượt bị lược làm bằng chứng.
- Môi trường chạy test: D:/RCA-ext/envs/py312-pin/Scripts/python.exe; PYTHONPATH=D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages;D:/RCA-flashticket/src. Python 3.12.10. Branch/HEAD đã ghi ở dòng mở phiên; src đúng code nghiệm thu.

**Nguồn đã tự đọc:** SPEC T-047; DT18-NV2/NV3, hướng dẫn cô bước 2–4; MRP §0–3, P6/P7, §6–7; LESSONS; SPEC T-043 B1.3, B1.7, B4, B6, Phụ lục C/D; SPEC và phần chi phối báo cáo T-045; DECISIONS Q-216–Q-230; WHY-59, WHY-67–69; báo cáo T-046, kiem-src.json, code b10 và progress local; diff bbef69dd..c298188e -- src/m1. Đọc runner, chay_pha1/chay_song_song, pha2_khoi_k, do_ben, moc_gia, pha2, chon_khoi, xep_hang, e5. Chưa dùng LOG kết luận thay bằng chứng.

**Danh sách tự tìm:**

N1 — CHẶN chạy đúng chế độ/phạm vi. SPEC T-047:35,42,73 nói dùng lại script và kiểm che_do trong tham-so.json. runner.py:103–114 sinh T1/16 K thiếu che_do; :182–184 chỉ sao khóa caller cung cấp. chay_pha1.py:36,70–94,190–193,242–246 cố định đường T-045, không gắn/ghi chế độ; runner.py:230 còn ghi phien_ban cũ trong metadata. Chạy nguyên script sẽ chạy mặc định, có thể ghi T-045. Sửa tối thiểu: adapter riêng results/T-047/scripts/, gắn đầy đủ G3/D1/E4+T4c cho mọi T1/K/cửa sổ giả, định tuyến cả pha2/độ bền/D2 về T-047, ghi tham số đầy đủ và kiểm từng bản ghi method_version + extra.che_do. D2 chỉ kiểm scorer trên P3 đóng băng, không phải chạy M1 nên không ép che_do; C-d1/C-d3 là đầu ra nhúng trong bản ghi mới, giữ thuật toán đối chứng. Đây là thiếu kế hoạch thực thi T-047, không là lỗi chế độ mặc định T-046.

N2 — CHẶN luật C và độ bền. SPEC:13,29,62,66 kế thừa luật C/T-045; Q-227/WHY-68 yêu cầu số thực thể tầng 1. pha2.py:88,209–218 chỉ giữ verdict/đếm CAUSE_FOUND; moc_gia.py:14–40 dùng tỷ lệ >0,10 và luật trần D17; pha2_khoi_k.py:138–142, do_ben.py:54–56 vẫn gọi nhánh ấy. Sửa tối thiểu: khai N1(c,i)=số extra.tang_P bằng 1; so chênh trung bình ghép cặp trên cửa sổ hợp lệ chung; mức HẠI do Minh duyệt trước chạy; báo V0 riêng. Giữ N1 theo cửa sổ từ pha1, n/mẫu bị loại, tính lại với bội số ô trong bootstrap bằng cùng helper. Không áp điều kiện trần của tỷ lệ cho số đếm. Giữ thứ tự các vế còn lại, Fraction và toàn bộ mặc định RR/ít ca. Mẫu số 0 là chưa kiểm, không là 0 hoặc đạt. Không sửa lịch sử T-045.

N3 — CHẶN nội dung thiết kế đang xin duyệt. SPEC:1,13,35 nói verdict đã khóa; WHY-68/Q-230 và src cho thấy chưa chọn verdict P7, V0 chỉ giữ. Sửa thành G3/D1/S1, V0 giữ báo cáo; cổng chưa hiệu chuẩn, verdict P7 OPEN. Không diễn giải nghiệm thu T-046 thành đã sửa false-positive hay cho mở G3/test. Phản chứng: code có quy tắc V0 thực thi, nhưng điều đó không tương đương quyết định chọn V0 cho P7.

N4 — CHẶN nếu muốn quy riêng tác động. SPEC:31,65,67 đặt câu hỏi do cổng/thang/nhiễu nhưng chỉ so hai gói đồng thời đổi G0/D0→G3/D1, S0→S1 và vế C-e. Cùng 52 ca và pipeline tất định, khác biệt hai lượt không phải do đã lấy mẫu ca mới; nhiễu mẫu ảnh hưởng suy rộng và độ bền lựa chọn. Sửa tối thiểu câu hỏi/bảng diễn giải: mô tả tác động gói; lần theo input→cờ→F_I→khóa→hạng và so đúng/sai tương ứng; chưa định lượng riêng từng yếu tố. Đây là thu hẹp câu trả lời về quy riêng nguyên nhân, không bỏ nghĩa vụ tìm cơ chế. Phương án giữ mục tiêu rộng: trình riêng đối chiếu chéo S0/S1 trên cùng bản ghi/cổng, kiểm exact trước dùng; CHƯA KIỂM khả năng phục dựng từ số float/Fraction, chưa có quyền chạy thêm, không hứa tách tương tác hoặc nhiễu chọn mẫu.

N5 — CHẶN kế hoạch khi gặp trạng thái lỗi/thiếu bằng chứng. SPEC:59 giữ ERROR tính trượt nhưng dùng lại chay_song_song.py:124–128 dừng phát việc với ERROR/UNSUPPORTED; pha2.py:64–89 chấm khác OK bằng RR=0; dem_moc_gia loại verdict None/INSUFFICIENT. Hai hành vi không xung đột nếu khai dừng chẩn đoán, giữ mọi output, không bỏ ca/không đổi ma trận, xin duyệt sửa src nếu cần rồi mới tiếp tục đủ ma trận. UNSUPPORTED và C-e không có N1 phải có luật trước số; không biến lỗi/thiếu hỗ trợ thành N1=0. Đề xuất: dừng cả phần chọn khi có ERROR/UNSUPPORTED chưa giải thích; INSUFFICIENT giữ mẫu số RR, chỉ loại ghép cặp C-e và báo lý do; n=0 không kết luận đã qua vế.

N6 — KHÔNG CHẶN nếu giới hạn kết luận đúng: số N1 không phản ứng với S1 (xep_hang.py:108–122 tính tầng trước khóa); E5 chỉ hạ F_I từ 1→0 (e5.py:113–188), nên bật riêng E5 không thể tăng N1 và vế HẠI tăng count không bao giờ bắt riêng E5. E2/E3 thêm kênh làm thay cơ hội có cờ. Giữ RR/M5/UV-6; không gọi N1 giảm là chất lượng RCA tăng hay FPR hiệu chuẩn. C-d1/C-d3 giữ khóa E4 trong chuoi.py:590–598 còn M1 dùng S1: phép so chỉ mô tả, chưa cô lập lợi ích cạnh.

N7 — KHÔNG CHẶN riêng: “mốc giả loại hết cấu hình” (SPEC:63) không xảy ra theo luật tương đối hiện hành. chon_khoi.py:104–126 giữ R0 ở lượt1; lượt2 chỉ loại c khi có c+x trong tập cố định; tập hữu hạn còn phần tử tối đại. Nếu mọi cấu hình bật bị loại thì R0 sống và dừng vì không có E1/E2/E5. Sửa mô tả tình huống đúng; giữ nhánh phòng vệ rỗng nhưng không tự thêm lọc tuyệt đối R0. Nguy cơ không đủ cấu hình đồ thị là có thật; rỗng do riêng vế tương đối là không có.

N8 — KHÔNG CHẶN riêng, cần sửa lạc quan/lịch sử và nhãn. SPEC:20 không có căn cứ nói độ lạc quan thực tế chắc lớn hơn T-045; phải nói nguy cơ do tái chọn/thích nghi, chưa định lượng. C-e đã xem ở T-045, T-046 trước hai lần khóa lại, không chỉ “sau khóa”. SPEC:36 “nhãn chỉ đọc pha2” cần tách mốc tiêm dùng chế độ(a) qua nhan.nap_moc (chay_pha1.py:167,238; nhan.py:23–31) khỏi root/fault/cell/E_X để chấm. Code chỉ projection mốc sang phương pháp, chưa thấy bằng chứng root/fault/cell lọt vào chuỗi. Pha2 mở nhãn ngay, không kiểm LOG: phải ghi hash pha1 vào LOG trước khi gọi evaluator, không chỉ tin hash nằm cạnh bản ghi. Không thể gọi đợt mới là dữ liệu độc lập; không chọn giữa hai lượt.

N9 — KHÔNG CHẶN riêng: SPEC:104 “bước10 chỉ R0” sai trên code/output; b10_kiem_src.py:156–167 chạy R0/K-đủ ở A/A, thật, C-e RE2. Nó lưu summary/p, không full phase1 rec. T1 phải khai đại lượng chung để so, không coi hash full rec phải trùng summary. Không cần thêm A/A T-047 chỉ để trùng toàn bộ B10; đối chiếu phạm vi đã chạy là R0 thật/C-e (K-đủ ở khối K sau). D2 giữ vai trò kiểm scorer 12/12 baseline.

N10 — KHÔNG CHẶN thiết kế nhưng CHẶN coi ngân sách 2,5–5 giờ là đã xác nhận. Progress b10 có 52 xong, giay_tu_dau cuối 3215,2 giây (4 tiến trình, tham-so.json), 268 lời gọi; RE2-TT R0 thật tổng 2435,6 giây, C-e 2275; K-đủ thật 2331,3, C-e 2336,4; Nezha R0 thật185,2, K-đủ254,7. Thời gian ca bao cả 6/4 lời gọi và cache, không lấy trung vị121,8 nhân thẳng 1550. Theo R0 từng cửa sổ, T1 sơ bộ (4×2620,8+2275)/4=3189,55 giây trước overhead; K nếu không dùng chung cache khoảng 5,4–5,5 giờ riêng. CHƯA KIỂM dự báo T-047: T1 1–2h, K1,5–4h nhờ xử lý16 cấu hình/ca cùng tiến trình/cache, pha2/độ bền 10–30phút (T045 do-ben.json#/giay=336,1). Không hứa cache lợi bao nhiêu; đo pilot 2 dataset và đổi dự báo trước full run, dừng khi vượt trần duyệt. Đề xuất sơ bộ tổng3–6,5h máy, quyền dài/qua đêm trình Minh, chưa dùng quyền T045 cho T047.

**Phạm vi nguồn:** T047 có thể kiểm cài đặt và chọn khối trên dev, không hoàn tất RQ3/khẳng định lợi ích quan hệ. K-b/T6–T12/KB/T13/A4, đối chứng mạnh, phát hiện ở chế độ(b), vùng có nhãn và ngoài thiết kế vẫn thuộc task sau; nghiệm thu khối không xóa các nghĩa vụ này. T4/T4b code mới đang hoãn: chưa có độ nhạy α/ε gói mới, không lấy số cũ làm chứng nhận; không cần ép chạy lại để tự rà SPEC nhưng phải trình hệ quả trước G3.

**Ứng viên mức HẠI, chưa quyết:** Δmean N1 > 0,10 thực thể/cửa sổ, strict >, so phân số chính xác. Với n=30, cần tổng tăng ít nhất4 thực thể. Đây là dung sai thực dụng chuyển đơn vị từ tỷ lệ sự kiện sang số thực thể kỳ vọng; không được suy từ 0,10 cũ là mức tương đương/đã hiệu chuẩn. Lựa chọn thay: Δmean>0 (không cho tăng ròng) quá nhạy một cửa sổ; ngưỡng tỷ lệ theo U/số kênh sẽ đổi câu hỏi Q227 và cần Minh quyết lại. Giả định: cùng cửa sổ/U/coverage, count có ý nghĩa như độ rộng tập bị gắn tự sinh. Sai khi ít count che mất nguyên nhân thật, khi kênh/coverage thay, hoặc trôi làm tăng count không do thành phần; E5 có lợi cấu trúc trong vế này. Chưa có ground truth thực thể bất thường ở C-e để hiệu chuẩn. Minh phải chốt.

**Khai đã nhìn C-e trước đề xuất mức:** đã đọc báo cáo T045 (V0 30/30 ở mọi cấu hình, 43/43 cặp không phân xử; nhóm metric/op); WHY67/68 và báo cáo T046 (V0/V3 30/30; V4; tỷ lệ theo loại đơn vị, nhóm kênh, R0/K-đủ); kiem-src.json#/verdict,ty_le,gop_o; các summary b10-kiem-src-001/ca/*#/cua_so/ce|R0,tom_tat và ce|K-du,tom_tat. Lệnh chỉ đọc tổng hợp count N1 cũ: R0 n30 tổng507 trung bình16,9 trung vị16 min11 max26; K-đủ tổng617 trung bình20,5667 trung vị19 min11 max33. Có thấy các tệp summary cũ, không đọc nhãn. Không có số mới T047. Không chọn ngưỡng bằng cách tối ưu giữ/loại cấu hình trên các số này; nhưng đề xuất không độc lập với lịch sử đã xem và phải công bố. Số count khác đơn vị-có-cờ (không nhầm trung vị19 của đơn vị với số thực thể).

Tiếp theo mới đọc đúng mục LOG T046 mà Minh chỉ định, kiểm từng ý; không sửa SPEC/src/WHY/DECISIONS, không chạy dữ liệu.

### Kiểm nguồn sau tự rà và chốt lượt — 2026-11-02T08:51:54+07:00

- Sau mốc đã ghi danh sách độc lập ở trên, mới đọc LOG T-046 mục Phiên 1 (tiếp 5), phần “Việc SPEC T-047 phải sửa” (dòng1181–1187). Kiểm từng ý: (1) verdict chưa khóa: ĐÚNG, WHY-68/src; (2) mức HẠI phải chốt và giới hạn số kênh: ĐÚNG, nhưng chưa đủ để thực thi nếu không sửa cả adapter pha2/độ bền như N2; (3) B10 có R0 và K-đủ: ĐÚNG trên loop/code và local output; (4) khóa che_do G3/D1/E4+T4c, commit nghiệm thu: ĐÚNG, nhưng phải kiểm từng bản ghi/định tuyến như N1; (5) “Q-224 ghi khi được duyệt”: ĐÚNG MỘT PHẦN về sửa câu SPEC, nhưng trạng thái “chờ ghi” đã lỗi thời: Q-224/Q-229/Q-230 hiện có trong DECISIONS, không cần tạo quyết định phân công mới.
- Test T-046 chốt: 46 passed, 1 warning, 74,29 giây. Tất cả ba bộ test đạt. Không dùng số test thay bằng chứng hiệu quả.
- Bổ sung làm rõ N2: đề xuất tối thiểu giữ vế C-e dựa trên thế giới P như verdict cũ; N1_P tính từ extra.tang_P, cùng một vế ghép cặp áp vào luật C của ba thế giới. Báo rõ giới hạn này; không tự đổi thành ba vế C-e theo thế giới. Nếu Minh muốn kiểm riêng C-e ở S_lo/S_hi thì là mở rộng cần duyệt. C-e INSUFFICIENT: không gán N1=0; vế không đo được phải hiện trong lựa chọn, không ghi đã qua. ERROR/UNSUPPORTED chưa giải thích: dừng trước chọn như N5.
- Bổ sung N4: khuyến nghị giữ câu hỏi phân tách bằng đề xuất đối chiếu S0/S1 từ trung gian của cùng cổng, trước hết kiểm phục dựng khớp chính xác; không chạy lại dữ liệu chỉ để đối chiếu nếu bản ghi đủ. CHƯA KIỂM việc phục dựng do khóa số thực có thể mất chính xác; nếu không đủ thì trình đúng phép chạy bổ sung/chi phí, không coi việc mô tả gói đã trả lời riêng cổng/thang điểm. Phương án tối thiểu chỉ mô tả gói là thu hẹp câu trả lời quy riêng tác động và cần Minh chấp nhận rõ, không tự chọn.
- Các đề xuất sửa được trình trong chat; SPEC, WHY, DECISIONS, src và kết quả cũ giữ nguyên. Quyết định dùng subagent trong lượt này là USER_CONFIRMED, đã lưu LOG theo quyền; chưa thêm DECISIONS vì chưa được phép. Các mức HẠI/ngân sách/phương án phân tách là CANDIDATE, không phải DECIDED.

**Bốn mục kết lượt:**
1. Đã làm: bước0, tự rà SPEC độc lập, ghi danh sách trước LOG cũ, kiểm năm ý bàn giao, dự báo chi phí bằng output đã kiểm hash. Chỉ đạt rà/đề xuất; chưa chạy T1/K T047, chưa chọn cấu hình, chưa trả lời hiệu quả/cơ chế riêng từng thay đổi.
2. File đổi: nối LOG này; chỉ dòng T047 trong docs/STATE.md để ghi “đã tự rà; chờ duyệt sửa SPEC, mức HẠI và quyền chạy”. Không commit/push.
3. Kiểm: bốn manifest và tập file khớp; T043 freeze10/10; tests374/16/46 passed. Diff cuối kiểm đúng hai file, LOG chỉ thêm, STATE chỉ dòngT047; không mở test/locked hay đọc nhãn dùng chấm.
4. OPEN/Minh quyết: gói sửa SPEC, HẠI count0,10 ứng viên, phương án giữ hay thu hẹp câu hỏi phân tách, quyền chạy local4 tiến trình/dài/qua đêm và trần giờ. Cổng chưa hiệu chuẩn; verdict P7, lợi íchS1, RQ3, độ nhạy α/ε mới và nghĩa vụ task sau vẫn OPEN. Thiếu sốT047/bằng chứng controlled để phân tách; không tự xác nhận lợi ích đồ thị.

Bước tiếp theo chính xác: Minh duyệt nội dung sửa được trình trong chat; cập nhật SPEC/WHY/DECISIONS chỉ khi được cho phép đúng tệp/nội dung. Claude soát SPEC bằng prompt nguyên văn mẫu trong chat (quyền phiên này chỉ nối LOG tự rà; prompt không tạo thành file mới). Chưa chạy bước1 trước khi Minh duyệt bản sửa, mức HẠI và quyền chạy. Khi được chạy, dùng adapter results/T047 được SPEC cho phép, đo2 ca, ghi dự báo trước fullrun; hash pha1 vào LOG trước gọi bộ chấm nhãn. Không dùng lại quyền chạy qua đêm T045 cho T047.
Lệnh test cuối: D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B -m pytest -q -p no:cacheprovider, cwd results/T-046/tests (PYTHONPATH theo đầu phiên). Lệnh cuối của lượt: git diff --check; git diff -- tasks/T-047-khoi-k-luot-2/LOG.md docs/STATE.md; git status --short --untracked-files=no (kiểm cuối, không sửa).

## Phiên 1 (tiếp 2) — 2026-11-02T09:54:07+07:00 — Codex ghi bản sửa đã duyệt

- Agent: Codex; thiết bị: LeVanMinh, Windows local; vai trò: người làm T-047. Branch giữ nguyên claude/sweet-hawking-dy078d.
- Phân loại: EXECUTE — ghi tài liệu theo đúng bản câu chữ đã trình; không cài code, chạy test hoặc thực nghiệm trong lượt này.
- Quyết định của Minh, nguyên văn ngày 02/11/2026: “duyệt ghi”. Lời này trả lời bản trình nguyên văn SPEC T-047, mục WHY-70 và dòng Q-231. Không lấy lời duyệt mẫu của Claude làm lời Minh. Đã ghi đúng dòng Q-231 được duyệt; ngoại lệ ngoài phạm vi gốc chỉ gồm WHY-70 và Q-231.
- Bản SPEC hiện tại thay bản cũ theo nguyên văn đã duyệt. Các câu “đề nghị duyệt” được giữ đúng bản trình; Q-231 và lời Minh ở mục này xác định việc duyệt đã có. Lượt này dừng ở ghi tài liệu, chưa bước 1. Quyền chạy và trần trong Q-231 được giữ đúng phạm vi, không dùng để mở G3/test hoặc commit/push.

### Tổng hợp phản hồi trước khi ghi

- Hai lượt chỉ đọc trước đã kiểm phản biện trên code và đầu ra cũ, không sửa file. Người làm rút khuyến nghị count0,10; hạ mức của vấn đề phân tách và xử lý lỗi; giữ vấn đề dùng nguyên script T-045 là chặn thực thi vì đường ra/chế độ.
- Kết quả phép kiểm chỉ đọc đã báo trong chat: bảng ngưỡng C-e G0/D0 khớp; phục dựng S0, S1 và chiếu S1 về S0 khớp 1.312/1.312 bản ghi T-045 (480 C-e RE2-TT, 480 thật RE2-TT, 352 thật Nezha-OB). Nguồn pha1: results/T-045/runs/b2b-k16-re2-mocgia-001/ban-ghi.jsonl, b2b-k16-re2-001/ban-ghi.jsonl, b5-k16-nezha-001/ban-ghi.jsonl; con trỏ extra.tang_P, K_I_P, K_raw_P, T4c.m_thuc_the, T4c.blocks và blocks; hash từng tệp khớp manifest T-045 trước dùng. Lệnh đọc qua py -3 -B -, so nguyên khóa và nhóm thực thể, không nhãn; không có output mới T-047 để viện làm bằng chứng.
- Claude đã chuyển bản kiểm lại cuối, rút nhận định “kết quả gần như định sẵn” và lý do chọn ngưỡng để tách E3/E2; đề xuất dừng phản biện thiết kế. Người làm không còn bảo lưu hai lập luận đó. Đồng thuận không xác nhận hiệu chuẩn hoặc lợi ích RCA.

### Năm yêu cầu của Claude đã thành nghĩa vụ cụ thể

1. SPEC mục Helper luật C và hồi quy: giữ dieu_kien_E5/UV6; không sao nguyên ly_do_hai_rieng; M_cong_M_phay chỉ thêm một lần; giữ khong_moc_gia; tính lại ket_hop và bao_kem.
2. Test hồi quy với vế cũ phải đối chiếu đầy đủ với ap_dung và pha2.ket_cuc_cap, gồm ba thế giới, trọng số, điều kiện riêng và metadata; chạy trước bước 1. Trạng thái hiện tại: CHƯA CÀI, CHƯA CHẠY. Các test T-044/045/046 hoặc phép phục dựng cũ không thay test helper mới.
3. Bảng2×2 tại P khai MRR gộp52 và theo dataset, chênh khi giữ yếu tố còn lại, lưu so-sanh-t045.json; G3/D1 là một gói; không chọn lại thang/lượt.
4. Độ nhạy0,5/2 phải tính lại toàn bộ luật C và bộ chọn bước1–8,10, không chỉ đếm cấu hình loại; chỉ báo cáo, không chọn lại h=1.
5. Ngoại lệ ghi đúng WHY-70 và Q-231 được nêu trong SPEC, WHY và DECISIONS; không mở quyền ghi chung. WHY đã ghi trước mọi triển khai/dùng ngưỡng trong kết quả.

### Thao tác và kiểm cuối

- Thứ tự ghi: DECISIONS Q-231 → WHY-70 → SPEC T-047 → nối LOG này → dòng T-047 trong STATE. Source quyết định hợp lệ trước cập nhật tài liệu phụ thuộc.
- Giữ nguyên toàn bộ prefix của DECISIONS, WHY, LOG; giữ xuống dòng CRLF của DECISIONS và LF của các tệp còn lại. SPEC thay toàn bộ đúng bản duyệt. STATE chỉ đổi dòng T-047, không đổi phần khác.
- Đã đối chiếu toàn bộ diff, đúng năm tệp; kiểm git diff --check, nội dung/mã duy nhất, năm nghĩa vụ Claude, nguyên văn SPEC/WHY/Q-231 và prefix các tệp nối. Các mục kiểm chưa cài không được ghi thành đã đạt.

### Bốn mục kết lượt

1. Đã làm: ghi bản sửa SPEC, WHY-70 và Q-231 theo “duyệt ghi”; lưu diễn biến, quyền và điểm tiếp tục. Chỉ hoàn tất bước ghi tài liệu; chưa hoàn thành T-047 hoặc câu hỏi nghiên cứu.
2. Tệp đổi: tasks/T-047-khoi-k-luot-2/SPEC.md, docs/WHY.md, docs/DECISIONS.md, tasks/T-047-khoi-k-luot-2/LOG.md và chỉ dòng T-047 của docs/STATE.md. Giữ các thay đổi khác và kết quả cũ.
3. Kiểm: nội dung khớp bản duyệt; append-only các tệp nối; STATE chỉ một dòng; git diff --check đạt. Không chạy lại test hoặc chuỗi vì lượt này chỉ ghi tài liệu. Không đọc dữ liệu/nhãn, không commit/push.
4. OPEN: helper/adapter chưa cài, hồi quy mới chưa chạy, T1/K chưa chạy; h=1 là dung sai thực dụng đã chốt về cách thử, chưa hiệu chuẩn. Cổng, verdict P7, lợi ích RCA, tác động toàn khối G3/D1 và nghĩa vụ các task sau vẫn OPEN. Không cần xin lại các quyền đã nằm trong Q-231; phát sinh ngoài phạm vi phải trình Minh.

Bước tiếp theo chính xác: đọc SPEC hiện tại và mục này; làm phần còn lại của bước0, cài results/T-047/scripts/luat_c_t047.py cùng adapter trong results/T-047/, thêm test dữ liệu giả và tạo kiem-helper.json, chạy hồi quy trước bước1. Không tạo/sửa src. Sau khi hồi quy đạt mới chạy thử R0 theo bước1 và cập nhật dự báo tổng7giờ. Chỉ đọc nhãn dùng chấm sau hash pha1 đã ghi LOG.
Lệnh cuối của lượt: git diff --check; git diff -- tasks/T-047-khoi-k-luot-2/SPEC.md docs/WHY.md docs/DECISIONS.md tasks/T-047-khoi-k-luot-2/LOG.md docs/STATE.md; git status --short (đối chiếu với snapshot trước lượt).
Nội dung commit đề xuất, CHƯA THỰC HIỆN: docs(T-047): ghi SPEC sửa, WHY-70 và Q-231 đã duyệt.

## Prompt bàn giao — chỉ dùng nếu Minh chọn chuyển

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-047, tasks/T-047-khoi-k-luot-2/SPEC.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P6, chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex làm; Claude phản biện.
- Tài liệu gốc: SPEC và LOG T-047; docs/WHY.md; docs/DECISIONS.md; docs/STATE.md; diff của năm tệp tài liệu trong working tree.
- Phản biện và phản hồi trước: tự rà trong LOG T-047; các bản soát và phản hồi trong chat ngày 02/11/2026 do Minh chuyển kèm.
- Code và kết quả liên quan: src/m1 và src/m1_danh_gia tại c298188e; manifest T-043–T-046; môi trường results/T-045/scripts/moi_truong.sh.
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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

## Phiên 2 — 2026-11-02T11:18:44+07:00 — Codex, LeVanMinh, người làm

Minh yêu cầu rà soát trước; không có mâu thuẫn thì triển khai task theo phạm vi hiện hành; có mâu thuẫn thì dừng trình. Không dùng subagent. Đang kiểm bước 0 và SPEC hiện tại; chưa chạy thực nghiệm, chưa đọc nhãn dev. Giữ các thay đổi tài liệu có sẵn.

### Tự rà độc lập: mâu thuẫn cần trình — 2026-11-02T11:22:05+07:00

R1 — CHẶN triển khai helper và lựa chọn khối; mâu thuẫn thiết kế, chưa phải lỗi thực nghiệm.
- FACT: SPEC T-047:100 yêu cầu mẫu số C-e bằng 0 ghi CHUA_KIEM_DUOC, không áp vế này, giữ cờ trong kết quả và lựa chọn. Dòng 166 giữ cả mẫu bootstrap C-e chưa kiểm được trong báo cáo.
- FACT: WHY-70 (docs/WHY.md:1087) yêu cầu khi đại lượng không tính được phải dừng phần phụ thuộc và trình bằng chứng thiếu. Chênh N1 với mẫu số 0 không tính được, nên hai câu hiện cho hành động khác nhau đối với cùng tình huống.
- Bằng chứng code: src/m1_danh_gia/luat_c.py, ket_cuc_tu_tong_hop và ket_hop_the_gioi chỉ tính kết cục/loại theo các điều kiện được truyền; src/m1_danh_gia/chon_khoi.py:36–53,61 đọc ket_cuc_dung/can_cu_loai. Gắn một cờ bổ sung không tự chặn bộ chọn. Helper T-047 chưa có nên chưa có lỗi chạy thực tế.
- Điều có thể bác bỏ hoặc thu hẹp nhận định: SPEC T-043 Phụ lục C (D2f) đã cho mẫu số 0 không áp vế; SPEC T-047 kế thừa đúng quy tắc này. Có thể WHY-70 chỉ muốn nói lỗi dữ liệu/cài đặt, không nói mẫu số 0 hợp lệ. Nhưng câu đã duyệt chưa phân biệt hai trường hợp; không tự chọn cách hiểu thay Minh.
- Hậu quả: có thể công bố lựa chọn kèm cờ dù thiếu vế C-e, hoặc phải dừng trước lựa chọn. Đây là quyền chuyển bước và phạm vi kết luận, không chỉ văn phong. Chưa kiểm tình huống này có xảy ra trên dữ liệu T-047; không đọc dữ liệu để quyết luật sau khi thấy số.
- CANDIDATE sửa tối thiểu: chỉ thay câu thứ hai của mục Điều kiện diễn giải thất bại WHY-70, nêu ngoại lệ mẫu số 0 hợp lệ theo D2f/SPEC: ghi CHUA_KIEM_DUOC, không áp C-e, tiếp tục các vế và bộ chọn với cờ được giữ; không gọi đã qua C-e. Lỗi tính toán, hồi quy, thiếu trường bắt buộc, ERROR/UNSUPPORTED vẫn dừng theo SPEC. Đề xuất này nới cách hiểu dừng tuyệt đối của câu WHY hiện tại, nhưng giữ quy tắc SPEC và D2f; không đổi h, ma trận hay mục tiêu nghiên cứu. Chờ Minh, chưa sửa WHY/SPEC.

Dừng triển khai theo chỉ đạo mới của Minh. Rà soát chưa hoàn tất toàn bộ a–i; chưa mở LOG T-046 mục Phiên 1 (tiếp 5), chưa kiểm các ý của lượt đó. Không nhận rằng đây là mâu thuẫn duy nhất hoặc các phần còn lại đã đạt. Lượt hash đang chạy được hoàn tất để giữ kết quả; không mở thực nghiệm, không đọc nhãn dev hay dữ liệu khóa.

### Prompt cho Claude — soát SPEC hiện tại

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-047, tasks/T-047-khoi-k-luot-2/SPEC.md; đề xuất trong LOG T-047 phiên 2.
- Công đoạn: soát SPEC.
- Gói/cổng: P6, chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex làm; Claude phản biện.
- Tài liệu gốc: SPEC T-047; docs/WHY.md; docs/DECISIONS.md; docs/STATE.md; nguồn đề tài và MRP.
- Phản biện và phản hồi trước: LOG T-047 theo thứ tự các phiên; các phản hồi trong chat do Minh chuyển kèm nếu có.
- Code và kết quả liên quan: src/m1, src/m1_danh_gia tại c298188e; manifest T-043–T-046; results/T-045/scripts/moi_truong.sh.
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

Công đoạn: soát SPEC.
Kiểm câu hỏi nguồn, phần mục tiêu được bao phủ, giả thuyết khác, khả năng phân xử của dữ liệu, phép kiểm dự kiến, phụ thuộc bước, chi phí, phạm vi và tiêu chí xong. Phần không làm phải có lý do, hệ quả và quyết định phụ thuộc.
Đánh giá kế hoạch và bằng chứng đã có; không đòi có kết quả của thực nghiệm chưa được duyệt. Phân biệt ứng viên để thử với lựa chọn đã chốt.
Chỉ ghi bản phản biện được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat nếu chưa có quyền ghi. Không tự sửa SPEC.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

### Kết lượt rà soát — 2026-11-02T11:24:17+07:00

1. Đã làm: mở phiên, đọc SPEC hiện tại, nguồn DT18/cô, MRP P6/P7, LESSONS, WHY-59/67–70 và quyết định liên quan; đọc code runner/chuỗi/luật C/bộ chọn. Tự tìm R1 và dừng trình. Chưa hoàn tất toàn bộ danh sách rà a–i; không xác nhận SPEC sẵn sàng chạy.
2. Tệp đổi: chỉ nối LOG T-047 và đổi dòng T-047 của docs/STATE.md. Giữ thay đổi có sẵn. Không sửa SPEC/WHY/DECISIONS/src/kết quả cũ; không dùng subagent, không commit/push.
3. Kiểm: Python -B kiểm các mục outputs/files/tep trong manifest. T-043: 69 mục không lệch; T-044: 2.133 mục; T-045: 6.085 mục, không có lệch ngoài khác biệt xuống dòng đã đối chiếu bằng git_blob. Toàn bộ 17 tệp src/m1 mỗi manifest khớp blob tại revision lịch sử SPEC chỉ định (git show/rev-parse). T-046: 933 mục khớp SHA. Lượt sơ bộ so SHA byte git show với SHA checkout CRLF báo 6 và 4 mục src/m1; đối chiếu blob lịch sử xác nhận đều khớp, không phải lỗi dữ liệu. Một lượt chỉ đọc khởi chạy trước chưa thu stdout; chỉ dùng lượt thu đủ stdout làm bằng chứng. Chưa kiểm các cấu trúc phụ khác của manifest hoặc dữ liệu đầu vào. git diff --check đạt. Chưa chạy test trong phiên 2 do dừng ở mâu thuẫn. Một lệnh nối kết lượt lỗi SyntaxError trước khi ghi do bytes literal Unicode; giữ thông tin lỗi này, chạy lại câu lệnh đã sửa.
4. OPEN: cần Minh phân xử R1. Chưa có kết quả T-047 hoặc bằng chứng mới về hiệu quả/cơ chế; mức h và quyền Q-231 giữ nguyên. Còn phần rà a–i, bước 0, hồi quy và thực nghiệm. Không đọc nhãn dev hoặc dữ liệu khóa. Prompt Claude ở trên, chưa gửi.

Đề xuất chưa duyệt: trong docs/WHY.md:1087, thay câu “Nếu hồi quy tích hợp lệch hoặc đại lượng không tính được, dừng phần phụ thuộc và trình bằng chứng thiếu, không gọi là đã qua vế C-e.” bằng:
“Nếu hồi quy tích hợp lệch hoặc không tính được đại lượng do lỗi tính toán, thiếu trường bắt buộc hay bản ghi ERROR/UNSUPPORTED, dừng phần phụ thuộc và trình bằng chứng thiếu. Riêng mẫu số C-e bằng 0 sau khi lọc các cửa sổ hợp lệ hoặc áp bội số: ghi CHUA_KIEM_DUOC, không áp vế C-e, tiếp tục các vế khác và bộ chọn theo SPEC; giữ cờ trong kết quả, lựa chọn và báo cáo bootstrap, không gọi là đã qua C-e.”
Lý do/ảnh hưởng: thống nhất WHY-70 với SPEC T-047:100,166 và D2f. Chỉ sửa một câu trong WHY; không đổi ngưỡng, ma trận hay mục tiêu. Có nới hành vi dừng nếu hiểu WHY hiện tại áp tuyệt đối cho mọi mẫu số 0; Minh quyết, không tự chốt.

Bước tiếp theo: Minh phân xử R1; nếu duyệt thì ghi đúng câu WHY-70, nối LOG/dòng STATE theo quyền; hoàn tất rà a–i và bước 0 trước khi cài/chạy. Không xin lại quyền chạy Q-231. Nhãn chỉ sau hash pha 1 ghi LOG.
Lệnh cuối kiểm: git diff --check; kiểm prompt nguyên văn theo docs/review-prompt.md; git status --short --untracked-files=no.
Commit đề xuất: docs(T-047): ghi điểm dừng rà soát SPEC và bàn giao. Chưa commit/push.

## Phiên 2 (tiếp) — 2026-11-02T11:38:02+07:00 — Codex, LeVanMinh, người làm

Minh xác nhận nguyên văn: “Duyệt ghi gói sửa; tiếp tục rà và test, chưa chạy bước 1”. Đã ghi Q-232 trước WHY/SPEC. Không dùng subagent. Giữ quyền chạy thực nghiệm tạm dừng trước bước 1 theo lời mới.

Câu WHY-70 đã ghi đúng đề xuất:
Nếu hồi quy tích hợp lệch, hoặc đại lượng không tính được do lỗi tính toán, thiếu trường bắt buộc, ERROR hay UNSUPPORTED, dừng phần phụ thuộc và trình bằng chứng thiếu. Riêng mẫu số C-e bằng 0 vì mọi cửa sổ của cặp đều bị loại do INSUFFICIENT_EVIDENCE (D2f): ghi CHUA_KIEM_DUOC, không áp vế này, tiếp tục các vế còn lại và bộ chọn với cờ được giữ; không gọi là đã qua vế C-e. Cấu hình thắng có cặp mang cờ này thì trình Minh trước khi dùng làm nền cho task (2).

Dòng SPEC đã ghi:
- Mẫu số bằng 0 ghi `CHUA_KIEM_DUOC`, không áp vế này và không ghi đã qua. Giữ cờ đó trong kết quả và lựa chọn. Cấu hình thắng có cặp mang cờ này thì trình Minh trước khi dùng làm nền cho task (2). Helper phải đưa cờ này vào kết quả chọn, vì `chon_khoi.py` không đọc nó.

Phản hồi người làm: đồng ý mâu thuẫn hẹp và cần cờ trong kết quả chọn; không coi đây là bằng chứng có lỗi thực nghiệm. Số C-e Claude báo chưa tự kiểm lại trong lượt này; không dùng làm căn cứ miễn kiểm. Cờ cấu hình thắng phải trình trước task (2); bootstrap vẫn chỉ báo cáo. Tiếp tục rà và test. Bản trước lượt giữ trong results/T-047/runs/ra-soat-003/before/.

### Rà độc lập bản hiện tại a–i, trước khi đọc mục T-046 tiếp 5

Phạm vi: kế hoạch và code hiện có; helper/adapter T-047 chưa cài. Không biến kiểm kế hoạch thành kiểm tích hợp hoặc kết quả thực nghiệm. R1 đã sửa đúng Q-232. Chưa tìm mâu thuẫn CHẶN mới trong phần kế hoạch đã đối chiếu dưới đây.

a. Nguồn: DT18-NV2/NV3, advisor bước 1–4 và MRP P6/P7 yêu cầu đồ thị tham gia điểm, thực nghiệm và đối chiếu; SPEC T-047 mục Mục tiêu và Phần nguồn chưa bao phủ giới hạn đúng vào dev/T1/K. K-b, KB và đối chứng mạnh phải tới các task (2)/(3); T4/T4b mới còn thiếu và đã nêu hệ quả trước G3. T-047 không xác nhận RQ3d, hiệu chuẩn, phát hiện (b), vùng có nhãn hay áp dụng FlashTicket. Không biến kế hoạch chưa chạy thành thiếu sót kết quả.

b. Nhất quán với code T-046: src/m1/chuoi.py:142–149 kiểm đủ ba khóa; 434–457 D1 chỉ điều chỉnh đơn vị log có mốc N (mẫu mới/NEW_OP và nhánh rơi dự phòng giữ quy tắc tương ứng); 465–474 G3 cho phân vị; 562–571 S1 chỉ ở E6a, đủ ba thế giới; 677–683 ghi method_version/extra.che_do. G3 rơi G0 khi thiếu khối là hành vi đã khóa, không là quên bật. S1 không đổi F_I/tầng/V0. Các câu B1.3 cũ “không Monte Carlo” và D24 cũ đã được thay có chủ đích bởi WHY-67/69, Q-228/Q-230; không mở lại quyết định. kiem-src.json khớp manifest; so_b3 không lệch, lech_b6 rỗng, blocks_khong_trung_T4c=0; bat_bien mới kiểm 8 bản ghi, không thay T1 đủ 52 ca.

c. Thực thi: runner.sinh_cau_hinh và chay_pha1.cau_hinh sinh K/T1 không tự gắn che_do. SPEC đã yêu cầu adapter mới gắn vào từng cấu hình sau mọi thao tác sinh/tái tạo; runner._params:175–193 truyền xuống chuỗi. T1 seed/xáo, K thật/giả phải cùng adapter. Metadata pha1 của runner/chay_pha1 cũ dùng PHIEN_BAN mặc định: SPEC yêu cầu metadata mới đầy đủ và kiểm từng bản ghi, không dùng nguyên script cũ. C-d1/C-d3 tại chuoi:590–599 dùng kênh của chế độ mới nhưng giữ chính quy tắc đối chứng, không áp S1 vào đối chứng. D2 đọc baseline đóng băng, không phải M1. Pha2/độ bền dùng cùng helper là nghĩa vụ chưa kiểm, không có sẵn.

d. Phân xử: luật C vẫn phản ứng với RR, UV-6, M5 và N1; E3 ít ca chỉ được giữ khi không có HẠI đứng trước. E5 bật riêng không tăng N1, S1 không thay N1/V0: vế này không bắt mọi tác hại, SPEC đã nói rõ. Bộ chọn giữ R0 khỏi HẠI tương đối; kiểm tập rỗng chỉ phòng vệ. S_lo/S_hi từng trùng P ở T-045 không suy ra luôn trùng khi thay D1. Bảng 2×2 ở P tách hiệu ứng gói G3/D1 và S1 trên cùng ca; chưa tách G3 riêng/D1 riêng và không tự tách cơ chế khỏi khớp dev. xep_hang.py:109–154 có khóa S1=(tầng,max s,max m,n,sum); bỏ đúng phần max m rồi sắp/gộp lại phục dựng S0, không giữ thứ tự S1. Phải kiểm phục dựng trước dùng như SPEC; không tuyên bố đã chạy kiểm ấy. Bộ chọn chạy lại ở h=0,5/2, không chỉ đổi cờ. Không cần lượt chuỗi riêng cho thang khi bản ghi đủ.

e. Luật quyết: SPEC đã khai dừng ERROR/UNSUPPORTED, trạng thái lạ, lỗi hash/hồi quy, hết ngân sách, thắng không đồ thị; bảng mặc định T-045 xử lý trái chiều/quan sát/xung đột, không chọn sau thấy số. Q-232 thêm trình cấu hình thắng có cặp C-e chưa kiểm trước task (2), giữ bootstrap báo cáo. Cờ phải được adapter/helper đưa ra cùng lựa chọn; src chon_khoi không làm thay. Chưa có helper nên kiểm này còn bắt buộc trước bước 1. Mẫu số bootstrap dùng bội số hiệu dụng; ca bội số 0 không đóng góp mẫu được xét, không phải lỗi dữ liệu. Không dùng “giữ cờ” để nhận C-e đã qua.

f. Lạc quan: lần chọn thứ hai trên cùng 52 ca, thiết kế từ lỗi dev, đã xem C-e và T4c trước khóa; SPEC và WHY-70 đã khai. Không định lượng được mức lạc quan thực tế từ bootstrap nội bộ; bootstrap chỉ mô tả mong manh. Nguồn cũ T-045 báo cả ca đúng/sai và giải thích khác; T-047 phải kiểm lại trung gian mới, không sao kết luận cũ. G3/test vẫn khóa.

g. Nhãn/thứ tự: chay_pha1 chỉ gọi p3.nhan.nap_moc để lấy projection inject_time (code src/p3/nhan.py:20–27), không truyền root/fault/cell; runner kiểm chuỗi cấm trước chuoi.chay. Đọc bytes của file nhãn để projection không phải truyền nhãn chấm vào phương pháp; đây là ngoại lệ đã duyệt chế độ (a), không áp cho (b). Pha2_khoi_k.main đọc nhãn ngay khi chạy: adapter phải được gọi sau ghi hash LOG, không dựa vào hash nằm cạnh tệp. D2 cũng pha 2. Chưa có hash pha 1 T-047, nên chưa được đọc nhãn chấm.

h. Chi phí: đã kiểm hash và đọc progress b10-kiem-src-001, 52 ca, wall 3215,2 giây, tổng thời gian các worker 12783,8 giây. RE2-TT trung vị 423,45 giây/ca; Nezha-OB 41,4; đây gồm R0/K-đủ và các cửa sổ của T-046, không ngoại suy tuyến tính sang 16 cấu hình. Chi tiết ở results/T-047/runs/ra-soat-003/thoi-gian-t046.json. G3 2.000 hoán vị và nhiều mẫu có thể tốn thời gian; dự báo 3–6,5 giờ và trần 7 giờ vẫn là chưa kiểm cho T-047, phải đo bước 1. Cache đặt lại theo ca, khóa gồm đơn vị/mẫu/mốc/biên/tham số/hướng; giữ các cấu hình cùng ca một worker để dùng lại cache. Không dùng lại p khác cửa sổ hoặc E1 làm đổi mẫu. Dùng hậu xử lý bảng 2×2/h và không chạy lại đầu ra hợp lệ là cách tiết kiệm đã nằm trong SPEC; không đề xuất đổi ngưỡng hoặc bỏ phép kiểm.

i. Quyền/đầu ra/tiêu chí: SPEC cho results/T-047, nối LOG/dòng STATE; Q-232 duyệt đúng sửa ba tài liệu nguồn, không mở quyền src. Đầu ra đủ chứa báo cáo, manifest, test/helper, từng lượt và sổ nhìn. Gói ghi Q-232 đã làm đúng thứ tự nguồn trước dẫn xuất. Chưa có adapter/helper thì chưa đạt tiêu chí 1/4/7; đây là công việc bước 0 phải làm, không là mâu thuẫn SPEC. Chưa sang bước 1 và chưa nhận hoàn thành task.

Tự rà kế hoạch không phát hiện thêm lỗi đáng kể cần sửa ngay. Những điều chưa kiểm đã được nêu tại từng mục và phải kiểm trong triển khai, không miễn bằng “chưa kiểm”. Danh sách này ghi trước khi đọc phần Việc SPEC T-047 phải sửa của LOG T-046 tiếp 5; bước tiếp theo là đối chiếu từng ý đó.

### Đối chiếu sau tự rà và kết lượt — 2026-11-02T11:43:54+07:00

Năm ý ở LOG T-046 phiên 1 (tiếp 5), mục Việc SPEC T-047 phải sửa:
1. ĐÚNG: verdict chưa khóa; WHY-68 và src/xep_hang.verdict vẫn V0. SPEC hiện tại đã nói đúng.
2. ĐÚNG: dùng N1 và mức HẠI cụ thể; Q-231/WHY-70/SPEC hiện đã khóa h=1, độ nhạy 0,5/2, nêu lệch số kênh. Không thay bằng tỷ lệ cũ.
3. ĐÚNG: T-046 bước 10 đã kiểm R0/K-đủ; kiểm-src.json#/status, #/verdict, #/bat_bien xác nhận phạm vi thật/C-e/A/A. Không coi 8 bản ghi bất biến là T1 đầy đủ.
4. ĐÚNG: che_do phải gắn tường minh; runner truyền được nhưng sinh cấu hình không tự bật; adapter mới còn phải cài/kiểm.
5. ĐÚNG về nghĩa vụ ghi Q-224; đã được xử lý trong DECISIONS hiện tại, không cần ghi trùng.

Nhận xét Claude Minh vừa chuyển: đồng ý sửa hẹp R1 và thêm tác dụng cờ theo Q-232; không đổi bootstrap. Đã đếm lại số cũ: 480 bản ghi OK/CAUSE_FOUND, 16 cấu hình, 120 cặp không thứ tự đều n=30; đây là toàn bộ cặp, khác 43 cặp luật chọn K. Nguồn kiểm ở runs/ra-soat-003/doi-chieu-phan-hoi.json; hash nguồn đã kiểm trong lượt trước. T046 kiem-src.json#/verdict cho C-e R0/K-đủ đều 30 CAUSE_FOUND. Không suy 14 cấu hình G3 còn lại cũng vậy; không dùng số cũ miễn xử lý n=0. Hai agent đồng ý chưa thay phản biện toàn bộ SPEC mới.

Bốn mục kết lượt:
1. Đã làm: ghi Q-232 từ xác nhận trực tiếp của Minh, sửa đúng WHY-70/SPEC; hoàn tất lượt rà kế hoạch a–i và đối chiếu năm ý LOG T-046; kiểm số cũ Claude dẫn; chạy ba bộ test cũ. Chưa phát hiện mâu thuẫn CHẶN mới trong rà kế hoạch. R1 đã xử lý ở tài liệu; cờ có tác dụng trong code vẫn phải kiểm khi cài helper.
2. File đổi: docs/DECISIONS.md (nối Q-232), docs/WHY.md (một câu WHY-70), SPEC T-047 (bổ sung dòng mẫu số 0), LOG T-047 (chỉ nối), dòng T-047 của docs/STATE.md; đầu ra kiểm và bản trước lượt trong results/T-047/runs/ra-soat-003/, sổ nhìn results/T-047/so-lan-nhin.jsonl. Các thay đổi có sẵn giữ nguyên. Không sửa src, không commit/push, không dùng subagent.
3. Kiểm: T044 374/374, T045 16/16, T046 46/46; tổng 436 qua, không lỗi/trượt/bỏ. Lệnh và thời gian ở runs/ra-soat-003/tests.json; stdout, junit và dữ liệu giả giữ ở thư mục test-T-*/. Chạy Python ghim -B, PYTHONDONTWRITEBYTECODE=1, PYTHONHASHSEED=0, no:cacheprovider, basetemp riêng trong T047. Cảnh báo cũ về record_property/JUnit và datetime của networkx; không làm trượt test. Test không đọc nhãn dev và không chạy chuỗi dữ liệu thật. Manifest các đầu ra cũ đã kiểm ở phiên 2; đối chiếu thêm hash kiem-src/progress trước dùng số. Kiểm diff theo bản before của lượt này, chỉ thay đúng câu/dòng; DECISIONS/LOG nối; prompt nguyên văn; git diff --check.
4. OPEN: đây là hoàn tất rà kế hoạch và bộ test cũ của bước 0, KHÔNG hoàn tất toàn bộ bước 0 hoặc T-047. Helper/adapter mới và hồi quy tích hợp chưa cài/chạy; vẫn cần trước bước 1. Kiểm trên dev, độ nhạy, bảng 2×2 và cơ chế chưa có. Chưa có kết luận RCA mới; quyền mở G3/test không thay. Không chuyển bước 1 trong lượt này theo Q-232. Prompt dưới để Minh chuyển Claude soát toàn bộ SPEC đã sửa; không tự gửi.

Bước tiếp theo: Claude soát SPEC hiện tại theo prompt (Minh chuyển); Codex giữ vai trò người làm. Sau xử lý ý kiến theo quyền, hoàn tất phần cài adapter/helper và hồi quy trong results/T-047/ theo SPEC mục Helper và Adapter. Không chạy script T045 nguyên trạng vì ghi cố định vào T045; không đọc nhãn chấm trước hash pha 1 ghi LOG. Trước chạy dữ liệu phải đáp ứng toàn bộ điều kiện bước 0 và chỉ đạo mới nhất của Minh.
Lệnh cuối kiểm: đối chiếu byte với runs/ra-soat-003/before/, parse JUnit, kiểm prompt nguyên văn, git diff --check và git status --short --untracked-files=no.
Commit đề xuất (chưa thực hiện): docs(T-047): thống nhất C-e mẫu số 0, ghi Q-232 và kết quả rà SPEC.

### Prompt Claude soát toàn bộ SPEC sau sửa

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-047, tasks/T-047-khoi-k-luot-2/SPEC.md.
- Công đoạn: soát SPEC.
- Gói/cổng: P6, chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex làm; Claude phản biện.
- Tài liệu gốc: SPEC T-047; docs/WHY.md; docs/DECISIONS.md; docs/STATE.md; diff và bản trước lượt trong results/T-047/runs/ra-soat-003.
- Phản biện và phản hồi trước: LOG T-047 theo thứ tự thời gian; nhận xét trong chat do Minh chuyển kèm.
- Code và kết quả liên quan: src/m1 và src/m1_danh_gia tại c298188e; manifest T-043–T-046; results/T-047/runs/ra-soat-003; results/T-045/scripts/moi_truong.sh.
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

Công đoạn: soát SPEC.
Kiểm câu hỏi nguồn, phần mục tiêu được bao phủ, giả thuyết khác, khả năng phân xử của dữ liệu, phép kiểm dự kiến, phụ thuộc bước, chi phí, phạm vi và tiêu chí xong. Phần không làm phải có lý do, hệ quả và quyết định phụ thuộc.
Đánh giá kế hoạch và bằng chứng đã có; không đòi có kết quả của thực nghiệm chưa được duyệt. Phân biệt ứng viên để thử với lựa chọn đã chốt.
Chỉ ghi bản phản biện được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat nếu chưa có quyền ghi. Không tự sửa SPEC.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

## Phiên 3 — 2026-11-02T12:01:50+07:00 — Codex, LeVanMinh, người làm

Minh: “duyệt tiếp tục”. Tiếp tục phần cài helper/adapter và hồi quy bước 0 trong phạm vi SPEC; không dùng subagent, không sửa src. Đã đọc AGENTS/STATE/SPEC và kiểm đầu ra test phiên trước có thật.

Đính chính báo cáo phiên trước: câu “Test không … chạy chuỗi dữ liệu thật” sai đối với tests/test_che_do_src.py của T-046. Fixture ban_ghi và test_che_do_sai_la_ERROR gọi t046.nap với một ca Nezha-OB dev; các test so code với số cũ và kiểm chế độ. Đây là bộ test bước 0 đã được phép, không phải thực nghiệm T-047 hay MRR mới. Hồi quy helper T-047 mới chỉ dùng dữ liệu giả. Giữ nguyên lịch sử, không xóa câu cũ.

### Checkpoint ngữ cảnh — 2026-11-02T12:05:50+07:00

Ngữ cảnh vừa được nén; ghi checkpoint theo AGENTS mục 5a.2. Vai trò không đổi: Codex làm, Claude phản biện. Minh đã nói “duyệt tiếp tục”; không xin duyệt lại gói helper/adapter bước 0. Chưa chạy bước 1; không commit/push; không dùng subagent.

Đã tạo hai bản cài đầu tiên trong results/T-047/scripts/: luat_c_t047.py và adapter_t047.py. Helper có vế N1 bằng Fraction, ghép kết cục ba thế giới qua nền pha2, 43 cặp khối K, giữ cờ C-e chưa kiểm trong lựa chọn. Adapter có cấu hình chế độ mới, lưu bản ghi trước kiểm lỗi, hash/LOG, đường gọi chung pha 2/độ bền/độ nhạy và phục dựng S0. Đây là code CHƯA KIỂM: chưa có bộ tests T-047 và chưa có kiem-helper.json; không coi các chức năng này là đạt SPEC.

Ba bộ test cũ và rà a–i nằm ở Phiên 2, results/T-047/runs/ra-soat-003/. Giữ đính chính Phiên 3 về fixture T-046 đọc một ca dev. Không dùng kết quả ba bộ test cũ thay hồi quy helper mới.

Việc tiếp: đọc lại hai script, API src/m1_danh_gia/luat_c.py, pha2.py, chon_khoi.py, rr.py, uv6.py, moc_gia.py và src/m1/runner.py, hop_dong.py, xep_hang.py; hoàn thiện tests bằng dữ liệu giả theo đầy đủ năm mục SPEC Helper. Kiểm điểm nối vế cũ bằng so toàn bộ dict; wrapper ba thế giới; M_cong_M_phay không lặp; N1 strict, trọng số, loại cặp và mẫu số 0; cờ cấu hình thắng; pha2/bootstrap cùng trọng số; metadata/trạng thái lỗi; phục dựng S0 phải sắp lại. Không sửa hoặc monkeypatch src/m1_danh_gia. Chưa được đọc nhãn dev phục vụ pha 2.

Lệnh dự kiến sau khi tests đã tồn tại (chọn thư mục runs mới chưa có, không xóa lượt cũ): Python ghim D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B -m pytest results/T-047/tests -p no:cacheprovider --basetemp=<runs mới>/tmp --junitxml=<runs mới>/junit.xml. Đặt PYTHONPATH=D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages;D:/RCA-flashticket/src;D:/RCA-flashticket/results/T-047/scripts, PYTHONDONTWRITEBYTECODE=1, PYTHONHASHSEED=0, PYTHONIOENCODING=utf-8. Giữ stdout/thời gian/mã thoát và ghi kiem-helper.json. Hồi quy/tích hợp lệch thì giữ lượt hỏng và dừng trước bước 1 trình nguyên nhân theo SPEC. Chỉ xem xét bước 1 sau khi bước 0 hoàn tất, đã báo rà soát và theo chỉ đạo mới nhất của Minh.

### Kết lượt và bàn giao Phiên 3

1. Đã làm: viết bản đầu helper/adapter bước 0; đính chính mô tả phạm vi test T-046; ghi checkpoint khi ngữ cảnh nén. Chưa chạy bước 1. Không thêm hoặc đổi quyết định nghiên cứu; lời “duyệt tiếp tục” nằm ở mở Phiên 3, không suy thành quyền commit/push.
2. File đổi trong Phiên 3: results/T-047/scripts/luat_c_t047.py, results/T-047/scripts/adapter_t047.py; results/T-047/runs/checkpoint-phien3-001/kiem-cu-phap.json và kiem-ban-giao.json; nối LOG này; chỉ dòng T-047 trong docs/STATE.md. Các sửa DECISIONS/WHY/SPEC từ trước giữ nguyên. Không sửa src, task khác, dữ liệu; không dùng subagent.
3. Kiểm: ast.parse hai script đạt; git diff --check đạt; git diff c298188e -- src rỗng. Chỉ xác nhận cú pháp, chưa xác nhận hành vi. Thư mục tests T-047 hiện rỗng; chưa chạy hồi quy helper, chưa có kiem-helper.json. Bộ test cũ giữ tại ra-soat-003; không chạy lại trong Phiên 3.
4. OPEN: bước 0 chưa xong. Phải cài và chạy đủ hồi quy helper/adapter theo checkpoint trước khi chạy dữ liệu. Chưa có kết quả T-047 để chọn cấu hình, kết luận cơ chế hay hiệu quả. Không phát hiện thêm mâu thuẫn tài liệu qua kiểm bàn giao; code vẫn chưa kiểm. Đề nghị mở phiên Codex mới theo AGENTS 5a.2, tiếp tục đúng quyền đã duyệt, không xin lại gói này. Prompt Claude dưới là bàn giao soát SPEC theo nghĩa vụ, Minh tự chọn chuyển; không tự mở vòng phản biện.

Bước tiếp theo chính xác và lệnh dự kiến: theo checkpoint ngay phía trên. Lệnh cuối: script kiểm byte/phạm vi dòng STATE, parse JUnit cũ, kiểm prompt theo mẫu, ast.parse và git diff --check; kết quả lưu runs/checkpoint-phien3-001/kiem-ban-giao.json. Commit chưa đề nghị thực hiện với code chưa hồi quy; nội dung dự kiến sau bước 0: feat(T-047): thêm helper C-e N1, adapter và hồi quy bước 0. Chờ Minh duyệt commit/push riêng.

### Prompt Claude soát SPEC — bàn giao Phiên 3

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-047, tasks/T-047-khoi-k-luot-2/SPEC.md.
- Công đoạn: soát SPEC.
- Gói/cổng: P6, chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex làm; Claude phản biện.
- Tài liệu gốc: SPEC T-047; docs/WHY.md; docs/DECISIONS.md; docs/STATE.md; git diff từ c298188e.
- Phản biện và phản hồi trước: LOG T-047 theo thứ tự thời gian; nhận xét trong chat do Minh chuyển kèm.
- Code và kết quả liên quan: src/m1 và src/m1_danh_gia tại c298188e; manifest T-043–T-046; results/T-047/scripts; results/T-047/runs/ra-soat-003; results/T-047/runs/checkpoint-phien3-001; results/T-045/scripts/moi_truong.sh.
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

Công đoạn: soát SPEC.
Kiểm câu hỏi nguồn, phần mục tiêu được bao phủ, giả thuyết khác, khả năng phân xử của dữ liệu, phép kiểm dự kiến, phụ thuộc bước, chi phí, phạm vi và tiêu chí xong. Phần không làm phải có lý do, hệ quả và quyết định phụ thuộc.
Đánh giá kế hoạch và bằng chứng đã có; không đòi có kết quả của thực nghiệm chưa được duyệt. Phân biệt ứng viên để thử với lựa chọn đã chốt.
Chỉ ghi bản phản biện được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat nếu chưa có quyền ghi. Không tự sửa SPEC.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

## Phiên 4 — 2026-11-02T12:09:52+07:00 — Codex, LeVanMinh, người làm

Minh: “Đọc AGENTS.md, tiếp tục T-047 theo checkpoint Phiên 3; hoàn tất bước 0”. Phân loại EXECUTE trong SPEC đã duyệt. Tiếp tục helper/adapter và hồi quy dữ liệu giả; không dùng subagent, không sửa src, không chạy bước 1 hoặc đọc nhãn chấm dev. Đã đọc AGENTS, STATE, SPEC, checkpoint và kiểm các đầu ra được bàn giao có thật. Giữ các thay đổi có sẵn. Phạm vi ghi: results/T-047, nối LOG này, chỉ dòng T-047 của STATE. Bản trước lượt nằm ở results/T-047/runs/buoc0-phien4-001/before/.

### Hồi quy lượt đầu và chẩn đoán test — 2026-11-02T12:18:11+07:00

Lượt runs/buoc0-phien4-001/hoi-quy-001 giữ nguyên source snapshot, stdout, stderr, JUnit và command.json: 127 qua, 2 trượt. Hai lỗi thuộc dữ liệu/kỳ vọng của test mới, không có lệch helper–API gốc: (1) tmp_path.parent vẫn thuộc results/T-047 nên adapter cho ghi là đúng; đổi điểm kiểm ngoài phạm vi thành ROOT.parent. (2) ca giả có 4 ca mỗi dataset nên luat_c.ap_dung mặc định delta_d=1/4, mức +/-1/10 chưa trái chiều đáng kể; đổi riêng đầu vào ca test thành +/-1/3 để thực sự kiểm bước 2. Không đổi luật, mức h, dữ liệu, helper, adapter hoặc src. Tiếp tục hoàn thiện hồi quy bước 0 trong phạm vi đã duyệt; vẫn dừng trước bước 1. Nếu có lệch hành vi helper/tích hợp thật thì dừng phần phụ thuộc trình Minh theo SPEC.

### Hoàn tất bước 0 — 2026-11-02T12:22:37+07:00

1. Đã làm: đọc lại helper/adapter và API gốc; cài bộ hồi quy bằng dữ liệu giả; so toàn bộ dict với vế cũ tại cùng điểm nối, ba thế giới và kết hợp; kiểm N1 Fraction/strict, mẫu số 0, trọng số, cờ tới lựa chọn, pha 2/độ bền cùng đường tính; kiểm metadata/trạng thái lỗi, hash/LOG và phục dựng S0. Quan sát kiểm cài đặt đã đạt bước 0 theo SPEC. Không thêm hoặc thay quyết định nghiên cứu; không chạy bước 1.
2. File đổi trong Phiên 4: thêm results/T-047/tests/conftest.py, test_luat_c.py, test_tich_hop.py, test_adapter.py; results/T-047/kiem-helper.json; các đầu ra/bản trước lượt/source snapshot trong results/T-047/runs/buoc0-phien4-001/; chỉ nối LOG này và đổi đúng dòng T-047 của docs/STATE.md. Hai script helper/adapter giữ nguyên byte so checkpoint Phiên 3. WHY, DECISIONS, SPEC và các thay đổi có sẵn được giữ nguyên; không sửa src, task khác hoặc dữ liệu. Không dùng subagent, không commit/push.
3. Kiểm: lượt mới hoi-quy-002 có 129/129 qua, 0 trượt/lỗi/bỏ; một cảnh báo cũ của networkx (DeprecationWarning). Lượt hoi-quy-001 giữ 127 qua/2 trượt, nguyên nhân ở ca test như mục trên, không có thay đổi cài đặt sau lượt này. Chi tiết command/env/thời gian/stdout/JUnit và source mỗi lượt được giữ; kết quả tổng ở kiem-helper.json#/new_regression. Ba bộ test cũ giữ dùng từ ra-soat-003: T-044 374/374, T-045 16/16, T-046 46/46; không chạy lại trong Phiên 4 vì nguồn không đổi. Kiểm lại hash 69/2133/6085/933 entry tương ứng T-043–T-046 và 10 file đóng băng T-043 đều khớp (kiem-hash.json, kiem-dong-bang.json); src/m1 lịch sử T-044/T-045 kiểm bằng git show theo SPEC. Đã đọc toàn bộ diff bốn file test mới, git diff --check qua; git diff c298188e -- src rỗng. Kiểm bàn giao sau cùng ghi kiem-ban-giao.json trong thư mục lượt.
4. OPEN: bước 0 hoàn tất trong phạm vi kiểm cài đặt bằng dữ liệu giả, chưa hoàn tất T-047. Chưa có dữ liệu thực nghiệm mới để chọn khối hay xác nhận cơ chế/hiệu quả; RQ3 và các nghĩa vụ nguồn của các bước sau giữ mở. Phục dựng S0 mới kiểm trên dữ liệu giả, còn phải đối chiếu bản ghi dev khi tới bảng 2×2. T1/QT5/thời gian/RAM, đối chiếu T-046, khối K, D2, độ bền 1.000 mẫu chính và phân tích cơ chế còn chưa làm. Không có lệch helper/API gốc hoặc tích hợp trên bộ ca giả còn chưa xử lý; điều này không xác nhận hành vi trên mọi dữ liệu thật. Giữ dừng trước bước 1 theo phạm vi Minh giao và chỉ đạo đang có. Không đọc nhãn chấm dev hoặc dữ liệu khóa trong phiên này. Prompt dưới để Minh tùy chọn chuyển Claude; chưa tự mở hoặc gửi lượt phản biện.

Bước tiếp theo chính xác: Minh xem results/T-047/kiem-helper.json và mục Phiên 4 này. Phiên nhận tiếp đọc AGENTS.md, docs/STATE.md, SPEC T-047 và cuối LOG; lệnh đọc kết quả: Get-Content -LiteralPath results/T-047/kiem-helper.json -Raw. Giữ dừng trước bước 1 cho tới chỉ đạo tiếp. Khi được tiếp bước 1, đọc results/T-047/scripts/adapter_t047.py và các hàm nạp ca/projection mốc của results/T-045/scripts/chay_pha1.py; cài driver chạy thử riêng trong results/T-047, không gọi script T-045 nguyên trạng. Chạy R0 mới trên một ca mỗi dataset theo SPEC bước 1, giữ lượt mới, đo QT5/thời gian/RAM và dự báo lại trong trần tổng đã duyệt; chưa đọc nhãn chấm. Không chạy lại các kiểm hợp lệ nếu không có thay đổi hoặc lo ngại mới.

Lệnh hồi quy đã chạy: Python ghim D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B -m pytest results/T-047/tests -q -p no:cacheprovider --basetemp=D:/RCA-flashticket/results/T-047/runs/buoc0-phien4-001/hoi-quy-002/tmp --junitxml=D:/RCA-flashticket/results/T-047/runs/buoc0-phien4-001/hoi-quy-002/junit.xml. Không dùng lại basetemp/lượt đã có. PYTHONPATH=D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages;D:/RCA-flashticket/src;D:/RCA-flashticket/results/T-047/scripts; PYTHONDONTWRITEBYTECODE=1, PYTHONHASHSEED=0, PYTHONIOENCODING=utf-8. Lệnh cuối của phiên: kiểm byte/phạm vi, hash source theo lượt test, prompt theo mẫu, JUnit và git diff --check; ghi kiem-ban-giao.json trong thư mục lượt.

Nội dung commit đề xuất (chưa thực hiện): test(T-047): hoàn tất hồi quy helper C-e N1 và adapter bước 0. Chưa đề nghị commit các quyết định hoặc tài liệu có sẵn ngoài gói; commit/push chờ Minh duyệt phạm vi riêng.

### Prompt Claude soát kết quả bước 0 — bàn giao Phiên 4

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-047, bước 0; tasks/T-047-khoi-k-luot-2/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P6, chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex làm; Claude phản biện.
- Tài liệu gốc: SPEC T-047; docs/WHY.md; docs/DECISIONS.md; docs/STATE.md; git diff từ c298188e; results/T-047/scripts và results/T-047/tests.
- Phản biện và phản hồi trước: LOG T-047 theo thứ tự thời gian; nhận xét trong chat do Minh chuyển kèm nếu có.
- Code và kết quả liên quan: src/m1 và src/m1_danh_gia tại c298188e; manifest T-043–T-046; results/T-047/kiem-helper.json; results/T-047/runs/ra-soat-003; results/T-047/runs/buoc0-phien4-001; môi trường và lệnh ở command.json của các lượt hồi quy.
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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

## Phiên 5 — 2026-11-02T12:30:07.5680542+07:00 — Codex, máy Windows của Minh, người làm

Minh giao tiếp tục triển khai sau tự rà độc lập; phân loại EXECUTE. Đã đọc AGENTS, STATE, SPEC, checkpoint và kết Phiên 4. Quyền hiện hành cho phép bước 1 trở đi theo SPEC nếu không có điểm chặn; thay chỉ đạo dừng trước bước 1 của phiên trước. Chỉ ghi results/T-047, nối LOG, dòng T-047 của STATE. Giữ nguồn đã khóa, tối đa 4 tiến trình local và trần tổng 7 giờ thời gian thực gồm thử/hỏng/chạy lại. Minh bổ sung cho phép dùng subagent; dùng hai subagent chỉ đọc để hỗ trợ tự rà, không thay Claude và không mở lượt phản biện chính thức. Chưa đọc nhãn chấm dev; không sửa src/SPEC/WHY/DECISIONS, không cloud/commit/push.

### Tự rà độc lập trước bước 1 — Phiên 5

FACT: đọc trực tiếp nguồn DT18-NV2/NV3, advisor bước 1–4, MRP P6/P7/§6, WHY-67–70, Q-224–232, LESSONS; SPEC không thay mục tiêu nguồn. Chưa thấy mâu thuẫn chặn bước 1: phạm vi chọn khối trên dev có T1, ba thế giới, luật C, độ bền, độ nhạy h và bảng 2×2; các nghĩa vụ chuỗi cuối, đối chứng, T4/T4b mới và đánh giá độc lập được nêu giữ OPEN. Mức h=1 là DECIDED về cách thử, chưa là ngưỡng đã hiệu chuẩn; E5 được lợi cấu trúc N1, dev tái dùng và G3/D1 đi chung giới hạn suy luận. Số lượt chính kiểm tay: T1=238; K=1312; tổng=1550 chưa gồm thử/test/rerun. C-e Fraction strict đúng: đủ 30 thì tổng tăng 31 mới vượt h=1.

Đã tự đọc helper, adapter, test và API runner/chuoi/pha2/luat_c/chon_khoi/rr; hai subagent chỉ đọc hỗ trợ, không là lượt review chính thức. Không thấy lỗi chặn ở 43 cặp, ba thế giới, trọng số hay đường hash/nhãn. QT5 và phục dựng S0 còn phải kiểm trên dev; test qua chưa xác nhận phương pháp. Không đọc kết luận review cũ để lập nhận xét. Kiểm lại 69/2133/6085/933 entry manifest T-043–046, src lịch sử đúng revision và toàn bộ source/JUnit bước 0 đều khớp: results/T-047/runs/phien5-tiep-nhan-001/kiem-tiep-nhan.json. Giữ dùng đầu ra hợp lệ; không chạy lại bộ test cũ/helper không đổi.

Đủ căn cứ chuyển sang pilot theo chỉ đạo Minh đầu phiên. Thêm driver riêng results/T-047/scripts/chay_t047.py, chỉ gọi hàm nạp/projection/xáo của T-045 và adapter T-047; không gọi main/đường ghi T-045. Chạy R0 (T1) một ca mỗi dataset, seed 0; đo load/pha1/RAM/QT5 từ đầu, không đọc nhãn chấm. Tối đa ba worker cộng một điều phối (không quá bốn tiến trình). Ngân sách ghi runs/ngan-sach.json, cộng thời gian các lượt test bước 0 đã giữ và bảo thủ tính thời gian thực từ pilot, kể cả khoảng chuẩn bị giữa lượt.
### Pilot và thích nghi Đ5 — Phiên 5

Pilot b1-pilot-001: hai ca OK, QT5 không điểm>1e6/toàn hòa/ngưỡng cực lớn/nhóm>90%; toàn bộ trường QT5 chung khớp T-046 bước 10. Thời gian worker RE2-TT 53,562s, đỉnh 1.271.115.776 byte; Nezha-OB 11,531s, đỉnh 400.920.576 byte. Nguồn: cases/*/summary.json và qt5.json; bảng đối chiếu/dự báo tại kiem-pilot.json. Dự báo CHƯA KIỂM tổng khoảng 5,69h với hai worker, dựa pilot và thời gian K cũ cộng mô hình chi phí G3; giả định, điều kiện sai và phụ thuộc lưu trong projection. K mới chưa đo cache; tiếp tục cập nhật theo thực chạy, vượt trần thì dừng. Chọn hai worker để giảm áp lực RAM, không đổi ma trận/phương pháp.

Lỗi đo phụ trợ: monitor pilot chỉ nhìn launcher Python nhỏ; đỉnh RAM từ bên trong worker đúng. Giữ source trước sửa tại b1-pilot-001/chay_t047-before-monitor-fix.py; driver sau đó tính cả cây tiến trình con. Không cần chạy lại phương pháp vì QT5/records và peak_rss worker vẫn hợp lệ.

Tự rà thêm trước T1: không được dùng nguyên helper Đ5 của T-045: doi_quyet_dinh_khi_T_lech gọi cham_dem mặc định D0 và hai hướng, trong khi R0 mới dùng D1/chỉ hướng lên. Schema bản ghi không lưu phi; dữ liệu thô có đủ. Phân loại là thiếu trung gian/đường thích nghi bộ báo cáo, không phải dữ liệu thô thiếu hoặc bằng chứng phương pháp sai. Thêm d5_t047.py trong phạm vi results: dựng sự kiện N/h0/phi từ logs đang nạp theo cùng API; đối chiếu số sự kiện, p/e/F gốc với bản ghi trước khi perturb 3×3 T±1%, giữ phi và chỉ hướng lên. Không sửa src/SPEC hoặc đổi công thức D1; chi phí phụ sẽ đo trong worker. Không dùng số D0 cũ làm số D1 mới. Pilot hợp lệ được giữ; T1 chạy lượt riêng để có companion Đ5 và đo lại khả năng tái lập.

### Tiến độ và tài nguyên — 2026-11-02T12:52:53+07:00

Minh đã dọn tiến trình phụ và yêu cầu tận dụng RAM. Giữ seed0 đang chạy để tránh chạy lại; các lượt sau dùng driver v2 với ba worker + một điều phối. Hai driver không chạy chuỗi đồng thời: tiep_t1.py chờ result.json seed0 hợp lệ rồi chạy seed1, seed2, xáo0 và C-e tuần tự. Không đổi cấu hình hay seed.

Đã thêm phép Đ5 D1 và test burst tổng hợp (1/1 qua), ghép tuần tự và test so byte với pha1 chung (1/1 qua), tại d5-hoi-quy-001 và driver-hoi-quy-001. Không chạy lại test cũ/helper không đổi. Driver v2 lưu source từng lượt, đo RSS cả cây Python, dừng cả cây với khoảng dư 15 giây trước trần; v1 giữ nguyên trong lượt đã chạy. K sẽ dùng ghép/tách tuần tự để tránh nạp cả khối lớn vào RAM. Phép dừng cả cây chưa kiểm bằng tiến trình thật; cần kiểm trước khi dùng nhánh đó. Dự báo sau 19 ca T1, dùng ba worker cho phần sau: khoảng 4,33 giờ toàn gói (du_bao_t047.py), CHƯA KIỂM vì K mới chưa đo. Tới trần/dự báo vượt phải dừng.

Các script pha2/bảng2×2 đang được hai subagent hỗ trợ viết trong đúng file results được giao; chỉ đọc source, chưa được thực thi hoặc đọc nhãn/E_X/số chấm cũ. Codex chịu trách nhiệm tự kiểm trước dùng; không là review chính thức.

### Hash pha 1 trước đọc nhãn — 2026-11-02T13:00:29+07:00

- `results/T-047/runs/b2-t1-seed0-001`: `ff6509acb4e278cfff729cf291612675728d79fa0b12336584a0e62c5ad94998`

- T1 seed0 xong 52/52, không lỗi worker; result.json giữ thời gian thực 1262,5 giây trước ghép. Kiểm giữa lượt 41 ca: toàn bộ tom_tat chung khớp T-046, S0 dựng từ tầng/khóa khớp chiếu S1. Chưa phải T1 bất biến hoàn tất; seed1/2/xáo/C-e còn chạy. T1 seed1 dùng ba worker. Phép dừng cây thật đã đạt: runs/kiem-dung-cay-001/result.json, mọi PID của lượt thử đã dừng.

### Tiếp nhận sau gián đoạn usage — 2026-11-02T13:13:46+07:00

Minh giao báo ảnh hưởng/thời gian dự kiến rồi tiếp tục phần bị dừng. EXECUTE tiếp trong phạm vi cũ; Codex làm/Claude phản biện không đổi. Tiến trình tiep_t1 và worker vẫn chạy, chưa có lỗi worker; seed0 đủ 52, seed1 đang tiếp. Kiểm mọi pha1 ca đã hoàn tất và source helper/adapter bước0 khớp; chứng cứ tại runs/tiep-sau-usage-001/kiem-toan-ven.json. Giữ nguồn hợp lệ, không rerun. Script co_che_t047.py/test_co_che.py có thật và đầy đủ cấu trúc, nhưng chưa qua kiểm khi gián đoạn; đang tự đọc và test trước dùng. Dự báo tại 13:13 còn 13709 giây (~3h49), giờ dự kiến khoảng 17:00; K chưa đo nên CHƯA KIỂM. Trần25200giây giữ nguyên, không reset ngân sách khi usage ngắt. Chưa đọc nhãn chấm hay E_X.

- Tiến độ Phiên 5 2026-11-02T13:15:22+07:00: xong T1 seed1; đầu ra results/T-047/runs/b2-t1-seed1-001/result.json; chưa đọc nhãn chấm.

### Hash pha 1 trước đọc nhãn — 2026-11-02T13:15:38+07:00

- `results/T-047/runs/b2-t1-seed1-001`: `ff6509acb4e278cfff729cf291612675728d79fa0b12336584a0e62c5ad94998`
### Seed 2 dừng trước dữ liệu và tiếp nhận cài đặt — Phiên 5

Seed1 đủ52/52, hash trùng seed0. Seed2 lượt001 dừng vì dev-03d4910932 báo ValueError ở ad.duong_ra trước tạo thư mục/nạp raw; không có bản ghi phương pháp cho ca đó. Hai worker đã phát trước lỗi hoàn tất hợp lệ, giữ tại lượt001. Chưa xác định được vì sao phép kiểm path trả false ở đúng tiến trình lỗi: stderr cũ không lưu resolved target/out/module; không suy là lỗi dữ liệu hoặc phương pháp. Kiểm source adapter vẫn khớp bước0, không có junction ở repo/T047; bốn subprocess chỉ đọc tái hiện cùng seed/path đều trả is_relative=true (duong-ghi-chan-doan-001). Giữ OPEN nguồn cụ thể của lỗi điều phối; không nới hoặc bỏ kiểm đường ghi.

Driver v3 chỉ thêm log chẩn đoán chi tiết nếu lỗi path lặp, và dùng lại ca hợp lệ sau kiểm hash/config/seed/mode/shuffle; không đổi input hay phương pháp. Seed2 lượt002 sẽ giữ nguồn hai ca từ001, chỉ chạy phần thiếu. Test dùng lại dữ liệu giả có đáp án byte trùng, khác seed bị từ chối: lượt001 1qua/1trượt do fixture chưa dựng script trong ROOT giả; chỉ sửa layout fixture; lượt002 2/2qua, giữ cả hai lượt. Phần tổng hợp T1 thêm phân bố điểm/tổng QT5; ast đã bắt một lỗi thiếu ngoặc trước khi thực thi, giữ source lỗi tại tiep-sau-usage-001/t1_t047-syntax-error.py rồi sửa; không ảnh hưởng records đã chạy. Hậu xử lý cơ chế và pha2 thêm8 test giả đã qua; chưa dùng nhãn thật.
- Cập nhật sau tiếp: seed2 lượt002 đã chạy lại ca chưa có output thành công; seed2 lượt001 giữ nguyên. Không tái hiện lỗi path trong lượt mới, chưa gọi là đã tìm được nguyên nhân. Dự báo sửa bộ đếm chỉ tính một lần mỗi (seed,xáo,mốc giả,ca) khi có output dùng lại, tránh giảm giả phần việc còn lại; thời gian lượt hỏng vẫn trong budget đã dùng.
- Tự rà extractor cơ chế trước dùng: đang bỏ kênh/F_I theo S_lo/S_hi dù native có extra.kenh_co_the_gioi, trong khi select_pairs xét cả ba thế giới. Chặn diễn giải nonP của extractor cũ, không chặn T1/K. Giữ bản trước sửa tại tiep-sau-usage-001/before-world-fix; đang sửa đúng extractor/tests để giữ chuỗi theo world. Chưa chạy extractor trên dev hoặc dùng thiếu trung gian này làm kết luận.
### Checkpoint tiến độ và tự kiểm — Phiên 5 tiếp sau usage

Quyền triển khai ban đầu và lời Minh mới vẫn có hiệu lực; không xin lại phạm vi. Codex làm, Claude phản biện; không sửa src/SPEC/WHY/DECISIONS, không testkhóa/cloud/commit/push. Các nguồn yêu cầu trực tiếp đã đọc ở đầu Phiên5, tự rà không có điểm chặn bước1. Bước0 dùng lại hash/JUnit hợp lệ. Pilot đạt. T1 seed0/seed1 đủ52/52, hash đã ghi LOG và trùng nhau. Seed2-001 có2ca hợp lệ và1 lỗi guard trước nạp; chưa có nguyên nhân cụ thể cho lần false duy nhất, giữ OPEN. Bốn chẩn đoán read-only và seed2-002 chưa lặp. Driver giữ guard không nới, thêm diagnostic khilặp, reuse2ca đãhash/config/seed/mode kiểm. K/chấm chưa chạy; chưa đọc nhãn chấm/E_X.

Tiến trình hiện hành: tiep_t1_v2.py, exec session37026. Lượt điều phối results/T-047/runs/t1-tiep-002/; tự chạy seed2-002 rồi xao0-001 rồi ce-001, đều driver chay_t047_v3.py với3worker. Đầu ra result.json mỗi lượt và monitor.jsonl. Source/command mỗi lượt có snapshot. Lượt tiep_t1.py cũ đã dừng khi seed2-001 lỗi, giữ log. Mọi ngân sách đọc runs/ngan-sach.json, không reset sau usage; dự báo du_bao_t047.py đã loại đếm trùng các ca reuse. Hiện khoảng1giờ đã dùng từ12:33 cộng236,719s test cũ; trần25200s. Forecast trướcK vẫn CHƯA KIỂM, khoảng17:00–17:15 dự kiến, cần đo K để cập nhật; dự báo vượttrần thìdừng.

Script đã có và kiểm: pha2_t047.py (gate streaming/LOG trước D2/nhãn, 12/12, helper và độnhạy, bootstrapseed20261102/n1000); so_sanh_t047.py (2x2P, phục dựngS0, kiểmoldmanifest); co_che_t047.py (chỉtríchFACT, cònphải người làm đọc raw/code và diễn giải); kiem_k_pha1.py (Kdu đối chiếuT046 vàR0 byte trừcid/variant soT1); t1_t047.py (fullT1sau5lượt, QT5/distribution/D5D1/N1/T046); tep_pha1.py (streamverify/split/log). Chưa tự chạy chấm vì thiếuKhash. Hậu xử lý cơchế đã sửa kênh/F_I nonP bị bỏ sót; giữchain_by_world và OPENtrường chưa native lưu, không mượnP. Lượt co-che-world-hoi-quy-001:6/6qua. Hồi quypha2+bảng2x2:10/10qua; sau sửa phân biệt cờtráichiềutrìnhMinh vớicờđúngởwinner và thêmmechanismtest:8/8qua; resume002:2/2qua. Tấtcảlượttrượt/codesnapshot đều giữ. Không dùngtestqua làm bằngchứnghiệuquả.

QT5 R0 seed0:12ca có tỷtrọngnhóm>90%; không cóđiểm>1e6/ngưỡngcựclớn/toànhòa. Dừngphân tích cáccờtrướcK: đọc tấtcảđếmđơnvị/trạngthái và vídụ p/rN/rA/F_raw từrecord, so ca cùngdataset khôngbịcờ. Bằngchứng runs/b2-t1-seed0-001/qt5-phan-xu.json. Nhóm khác vẫnđượcchấm (vd70opOK nhưng0cờ; hoặc154metricOK nhưng0cờ), logthườngthiếuhỗtrợ/severitykhôngxácđịnh. Có ca logNEW_OP nN0/nA1040 tạo1kênh, cáckênhkhác khôngquacổng. Quan sát nàygiảithích tỷtrọngđãghi, khôngxácnhậnbấtthườngthậthoặcquylỗidataset. Khôngđổitham số/ma trận/h. T1bảngcuối phải đưa flag/linkdiagnosis, chưa gọiT1hoàntấttrướclượt xáo/Ce.

Bước tiếp: theo dõi result/progress của t1-tiep-002. Khi T1xong, đọc t1.json, tự kiểm QT5/C-e và đốichiếuT046, ghi hashcả5lượt vàoLOG bằng tep_pha1.ghi_log. Nếuđạt thìchạy K thật rồiK C-e với3worker trong trần, vídụ PYTHONHASHSEED0 Python ghim -B results/T-047/scripts/chay_t047_v3.py --run results/T-047/runs/b3-k-that-001 --group K --workers3 (CLI thực tế dùng --workers 3); C-e thêm --fake. Đo K sớmtừ summary/progress theo từngca, cậpnhậtdựbáotoàngói; không tinmôhìnhcachecũ. Xong kiểm kiem_k_pha1.py, QT5; ghi2hashK trước pha2 D2. Rồiphase2, cơchế, độbền1000, độnhạy và2x2, báo cáo/manifest/tựkiểm/phạmviLOG/STATE vàpromptClaude. Nếu thiếu trunggian/phépkiểm ngoàiquyền thìtrìnhđúngbằngchứng/chi phí, khôngtựbỏnhóm.

- Tiến độ Phiên 5 2026-11-02T13:37:48+07:00: xong T1 seed2; đầu ra results/T-047/runs/b2-t1-seed2-002/result.json; chưa đọc nhãn chấm.

### Hash pha 1 trước đọc nhãn — 2026-11-02T13:39:12+07:00

- `results/T-047/runs/b2-t1-seed2-002`: `ff6509acb4e278cfff729cf291612675728d79fa0b12336584a0e62c5ad94998`

- Seed2 lượt002 đủ52/52, hash trùng seed0/1; dùng lại2ca từ001, không bỏ ca. Console cũ hiển thị tử số gồm2ca reuse nhưng mẫu số chỉ50ca còn chạy (vd52/50); result.json đúng done52/planned52/reused2. Sửa đúng mẫu số hiển thị của driver v3 cho lượt sau, không đổi đầu ra hoặc phương pháp. Xáo0 đang chạy, C-e chưa xong.

- Tiến độ Phiên 5 2026-11-02T13:56:36+07:00: xong T1 xao0; đầu ra results/T-047/runs/b2-t1-xao0-001/result.json; chưa đọc nhãn chấm.

- Tiến độ Phiên 5 2026-11-02T14:10:35+07:00: xong T1 ce; đầu ra results/T-047/runs/b2-t1-ce-001/result.json; chưa đọc nhãn chấm.

### Hash pha 1 trước đọc nhãn — 2026-11-02T14:17:36+07:00

- `results/T-047/runs/b2-t1-seed0-001`: `ff6509acb4e278cfff729cf291612675728d79fa0b12336584a0e62c5ad94998`
- `results/T-047/runs/b2-t1-seed1-001`: `ff6509acb4e278cfff729cf291612675728d79fa0b12336584a0e62c5ad94998`
- `results/T-047/runs/b2-t1-seed2-002`: `ff6509acb4e278cfff729cf291612675728d79fa0b12336584a0e62c5ad94998`
- `results/T-047/runs/b2-t1-xao0-001`: `742a912d8a37aa893085fd8537da1ff2cfe5165ff2f2725a5312a4bdfb09933b`
- `results/T-047/runs/b2-t1-ce-001`: `6f3b9a86e27c917a74d090b395a05526ccee17d0b2d3e4695704b968fe6ab229`

### Kết thúc Phiên 5 tại điểm chặn — 2026-11-02T14:17:33+07:00

1. Đã làm: tiếp sau usage, giữ kết quả hợp lệ, hoàn tất 238 lượt T1 chính và pilot; tự rà code/nguồn, helper/adapter/driver, Đ5 D1, kiểm trung gian, đối chiếu T-046 và chẩn đoán C1. T1 không đạt bất biến xáo hàng; dừng trước K. Không thêm hoặc đổi quyết định nghiên cứu.
2. File đổi: scripts/tests/runs, kiem-helper giữ nguyên, t1.json, so-lan-nhin.jsonl, dinh-chinh-cai-dat.md, bao-cao.md, prompt-claude-phien5.txt và manifest/kiểm bàn giao trong results/T-047; chỉ nối LOG này, chỉ dòng T-047 trong STATE. Không sửa src/SPEC/WHY/DECISIONS hoặc dữ liệu; giữ các thay đổi có sẵn. Không cloud/commit/push.
3. Kiểm: hash cũ và nguồn bước0 khớp; seed0/1/2 trùng byte; R0 thật/C-e khớp 82 tóm tắt T-046; xáo lệch đúng2 trường p ở2ca. Đ5 D1 58 đơn vị, 0 đổi quyết định. Cuối phiên 152/152 test giả qua; ứng viên C1 riêng qua3 test và3 đơn vị thật, chưa tích hợp. Lượt lỗi/test trượt/các bản patch trước đều giữ. Báo cáo và đính chính chứa con trỏ nguồn; không coi test qua là T1 qua.
4. OPEN/chờ Minh: quyền sửa src C1 và ngoại lệ nguồn code c298188e cộng patch, dòng Q-233 nếu duyệt; quyết ngân sách vì chạy lại T1/K có thể vượt phần còn lại trần7giờ. Đề nghị trần tổng8giờ, chưa nới. Lỗi guard duy nhất trước nạp còn chưa giải thích cụ thể. Ý nghĩa G3 trên chuỗi gần hằng chưa xác nhận. Chưa có K, D2 mới, chọn khối, cơ chế khối, bootstrap, độ nhạy hay2×2; không trả lời xong RQ3, hiệu chuẩn hoặc hiệu quả RCA. Hai agent hỗ trợ chỉ là người làm phụ, chưa có phản biện chính thức của Claude.

Bước tiếp theo chính xác: đọc báo cáo/đính chính C1 và patch runs/de-xuat-c1-003/de-xuat.patch; chờ Minh duyệt phần ngoài quyền. Không chạy K với T1 đang trượt. Nếu được duyệt, áp đúng patch src, cập nhật metadata nguồn T-047 theo hash code thực và ghi đúng lời duyệt/phạm vi; giữ mọi kết quả cũ. Kiểm mặc định/hồi quy và pilot đo lại; kiểm dự báo trong trần Minh cho phép trước chạy T1 mới, rồi K và các bước còn lại nếu đạt. Không tự thêm epsilon/sàn phương sai hoặc đổi G3/D1/S1/h/ma trận/luật chọn. Nguồn T-046 cũ kiểm src bằng git show c298188e khi C1 đã được phép; không sửa manifest cũ. Chưa có quyền đổi tiêu chí so T-046 nếu sau sửa vẫn lệch chưa giải thích.

Lệnh kiểm cuối: scripts/kiem_ket_phien5.py (kiểm phạm vi/hash/diff/JUnit, manifest và dừng tiến trình; sẽ ghi output sau mục này). Mọi tiến trình phương pháp đã dừng sau T1; không có tự động chạy K. Nội dung commit đề xuất sau khi Minh duyệt phạm vi: feat(T-047): thêm driver, T1 và chẩn đoán bất biến G3. Chưa commit/push.

### Prompt Claude — bàn giao Phiên 5, Minh chuyển thủ công

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-047; tasks/T-047-khoi-k-luot-2/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P6, chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex làm; Claude phản biện.
- Tài liệu gốc: SPEC T-047; docs/STATE.md; docs/WHY.md; docs/DECISIONS.md; git diff từ c298188e; results/T-047/bao-cao.md; results/T-047/dinh-chinh-cai-dat.md.
- Phản biện và phản hồi trước: LOG T-047 theo thứ tự thời gian; các nhận xét trong chat Minh chuyển kèm nếu có.
- Code và kết quả liên quan: src/m1, src/m1_danh_gia tại c298188e; manifest T-043–T-046; results/T-047/manifest.json; scripts/tests/runs của T-047; patch tại runs/de-xuat-c1-003; môi trường và lệnh trong LOG và command.json/JUnit từng lượt.
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

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

Chốt bàn giao: kiểm phạm vi/hash/diff/JUnit đạt (integrity_PASS), task_PASS=false vì C1. Manifest checkpoint giữ mọi lượt/candidate, chưa có K/nhãn chấm. Đã dùng 112.36 phút; còn 307.64 phút của trần7giờ. Bắt đầu chờ Minh; chỉ thời gian chờ này được loại theo SPEC khi có chỉ đạo tiếp, giữ nguyên phần đã dùng. Lệnh cuối thực tế: Python ghim -B results/T-047/scripts/chot_ngan_sach_phien5.py. Bước tiếp theo vẫn là duyệt phạm vi C1/ngân sách; không chạy K tự động.
