**Đề xuất tiếp tục phản biện T-075.** Tôi tái lập được **18/18 đầu ra khớp mong đợi và 0/30 cặp chéo lọt**. Tuy nhiên, một đầu ra E5 được chấm đúng có câu vượt quá bằng chứng được dẫn. Bộ kiểm cũng chấp nhận đầu ra vừa tuyên bố “không đủ bằng chứng” vừa đưa ra suy luận và gợi ý giảm thiểu. Hai lỗi này ảnh hưởng trực tiếp đến quyết định dùng bộ kiểm để hiện câu trả lời trong demo. [Kết quả đã lưu](D:/RCA-flashticket/results/T-075/ket-qua-thu.json) · [Tiêu chí xong của SPEC](D:/RCA-flashticket/tasks/T-075-w8-llm-toi-thieu/SPEC.md:42)

### Các điểm phản biện

**R1 — CHẶN kết luận mẫu E5 chỉ dùng bằng chứng đã dẫn.** Tại `#/goi_y_xu_ly/0`, mẫu viết “sau t̂ không còn span, log và metric bắt buộc”. Hai con trỏ của câu dẫn tới bảng **span** và danh sách **nguồn thiếu phủ**. Không con trỏ nào dẫn tới số log. Danh sách thiếu phủ cũng không cho biết mẫu cuối nằm trước hay sau t̂. Đối chiếu dữ liệu gốc cho thấy trong cửa sổ sự cố Payment vẫn có 20 mẫu `live-down` và 20 mẫu `live-ms`, đếm tại `prometheus-bo-sung.json#/bundles/16/result/3/values` và `#/bundles/17/result/3/values` với điều kiện `t̂ ≤ timestamp < t̂+300`. Đính chính E5 phân biệt sáu nguồn cơ sở thiếu phủ với hai kênh này. Ở `#/khang_dinh/1`, hai con trỏ cuối cũng chỉ trả về `50` và `60`, chưa dẫn tên hai luật cảnh báo mà câu nêu. Cả mẫu nhận `loi=[]` tại `ket-qua-thu.json#/ca/e5/dau_ra/dung`. [Mẫu E5](D:/RCA-flashticket/results/T-075/ca-thu/e5/dau-ra-dung.json:10) · [Đính chính E5 §1](D:/RCA-flashticket/results/T-073/dap-cx21/dinh-chinh-e5-2.md:17)

Sửa tối thiểu là dẫn riêng hai trường span/log của Payment cùng quy ước khóa vắng, viết “sáu nguồn metric cơ sở thiếu phủ cửa sổ”, và dẫn đối tượng cảnh báo hoặc trường `ma_luat` tương ứng. Có thể giữ gợi ý kiểm tra Payment và giữ nguyên Booking ở hạng 1. Mẫu vẫn là ví dụ viết tay của người đã biết ô E5.

**R2 — CHẶN duyệt nghĩa của các trường gửi đi trên ca W5.** Hai nhánh đóng gói đặt số hàng metric dưới `so_mau_vao_loi`. Trên E5, `#/du_lieu_loi/hang_metric` cho `1212 + 1100 + 2399 = 4711` hàng, gồm cả hàng ngoài cửa sổ. Nguồn tự ghi ở `#/du_lieu_loi/nguon_dau_vao_loi/kieu` rằng đây là đầu vào P7 được V082 đọc lại. Sau bổ sung liveness, V082 dùng **5367 hàng, 77 nguồn metric**. Nhánh `su_co` còn gán `ket_qua_rca.trang_thai_chay` từ `p7_status` bên cạnh tên bản và kết luận V082. Hai trạng thái cùng là `OK` ở E5, nên ca này không phát hiện được việc lấy nhầm nguồn trạng thái. [Bộ dựng gói](D:/RCA-flashticket/results/T-075/goi_bang_chung.py:151) · [Đối chiếu số hàng, `#/p7_so_hang_metric` và `#/duong_v082`](D:/RCA-flashticket/results/T-073/dap-cx21/so-hang-metric.json)

Sửa tối thiểu là ghi rõ phạm vi P7 cơ sở cho số hàng và độ phủ, tách hàng ngoài cửa sổ, lấy trạng thái V082 từ nguồn V082 khi có. Nếu nguồn sự cố thiếu một trường, ghi rõ thiếu. Với G1 chế độ (b), nên giữ giới hạn sẵn có ở `#/che_do_b/gioi_han` rằng nửa nền có thể chứa phần đầu sự cố. Điều này ảnh hưởng cách đọc câu “trước/sau cảnh báo”. Không cần sửa hay chạy lại lõi RCA.

**R3 — CHẶN dùng kết quả “đạt” để quyết định hiển thị câu trả lời.** Tôi gọi trực tiếp `kiem(goi, ra)` trong RAM trên mẫu `cu-1`. Ba phản ví dụ tách được lỗi cấu trúc khỏi giới hạn hiểu tiếng Việt mà tác giả đã khai. [K1](D:/RCA-flashticket/results/T-075/kiem_w8.py:138) · [K4–K5](D:/RCA-flashticket/results/T-075/kiem_w8.py:198) · [Khuôn đầu ra](D:/RCA-flashticket/results/T-075/khuon-dau-ra.md:20)

| Thay đổi trên mẫu | Kết quả thực |
|---|---|
| Chuyển sang `KHONG_DU_BANG_CHUNG`, để danh sách phần thiếu rỗng, giữ một `suy_luan` và một `giam_thieu` | `[]`. K4 chỉ áp các ràng buộc khi bộ kiểm tự kết luận gói thiếu. Khuôn cho phép model chủ động từ chối cả trên gói đủ. |
| Giữ `GIAI_THICH`, bỏ hết khẳng định và gợi ý, chỉ để một mục thiếu có câu rỗng dẫn `/bang_chung_bo_bot` | `[]`. Tên trường đếm lọt qua phép so tiền tố `/bang_chung`. Người vận hành không nhận được lời giải thích hay bước xử lý. |
| Đưa `null` vào danh sách `khang_dinh` | `AttributeError`. Bộ kiểm dừng trước khi trả danh sách lỗi mà phương án gọi lại cần dùng. |

Sửa tối thiểu là kiểm kiểu và nội dung bắt buộc trước khi đọc từng mục, áp ràng buộc theo **trạng thái đầu ra** ở cả hai nhánh, và buộc lời giải thích dẫn mục bằng chứng thực. Prompt hoặc lược đồ đi kèm lời gọi cần cung cấp đủ cấu trúc đó. Đề xuất rút câu “demo không bao giờ hiện câu bịa”. Nếu đầu ra sai khuôn, thông báo phù hợp là “Không tạo được giải thích hợp lệ”. Chỉ báo “không đủ bằng chứng” khi có căn cứ về bằng chứng của ca. [Prompt mẫu](D:/RCA-flashticket/results/T-075/prompt-mau.md) · [Đề xuất xử lý khi trượt](D:/RCA-flashticket/results/T-075/de-xuat-minh.md:35)

**R4 — CHẶN coi quy tắc “có một mục cùng thực thể hạng 1” là đủ để giải thích hạng.** Trên G1 E5 thật, Booking có hai mục SQL với `F_I=1` và một mục `workload` với `F_I=0`. G1 ghi kế thừa cho `workload` tại `#/ke_thua/4` đến `#/ke_thua/6`. Tôi bỏ riêng hai mục SQL khỏi bản gói trong RAM. `phai_khong_du` vẫn trả `False`, dù mục còn lại của Booking không phải kênh đưa nó vào tầng hạng đầu. Đây là phản ví dụ cho quy tắc; gói E5 đầy đủ thực tế vẫn giữ cả hai mục SQL. [Quy tắc đủ bằng chứng](D:/RCA-flashticket/results/T-075/kiem_w8.py:53) · [Cách lõi dùng `F_I` để xếp tầng](D:/RCA-flashticket/src/m1/xep_hang.py:98) · [G1 E5 gốc](D:/RCA-flashticket/results/T-073/e5/ca-7577dd5b/srv/rca-lab/rca-results/t073-e5-001/du-lieu/V082-V066+H8a/7577dd5b.json)

Đề xuất buộc câu giải thích *vì sao đứng đầu* dẫn bằng chứng của nhánh thực sự tạo hạng. Với E5 đó là kênh riêng. Không áp `F_I=1` máy móc cho nhánh H5 có thể thay hạng bằng quy tắc riêng. Nếu gói rút gọn chỉ giữ được thứ hạng, vẫn có thể báo thứ hạng và nói rõ thiếu căn cứ giải thích. `WHY-98` giải thích việc chọn V082. Tôi không tìm thấy mục WHY cho lựa chọn khác là cắt 20 mục rồi dùng phép kiểm trùng tên để quyết định đủ bằng chứng. Có thể giữ quy tắc này làm **ứng viên** trong lúc sửa. [Bước cắt gói](D:/RCA-flashticket/results/T-075/goi_bang_chung.py:90) · [Nhánh H5](D:/RCA-flashticket/src/m1_ft/thanh_phan/h4_h5.py:156) · [WHY-98](D:/RCA-flashticket/docs/WHY.md:1417)

**R5 — CHẶN dùng riêng K8 làm căn cứ duyệt danh sách trường gửi ra ngoài.** Tôi không thấy sổ tiêm, đáp án, tên ô, mã ca, đường dẫn nhận diện ca hoặc chú thích hash T-064 trong phần `gui_di` của sáu gói đã lưu và gói G1 E5 dựng lại. Tên Payment trong luật cảnh báo có nguồn quan sát thật. Tuy nhiên, `tom_tat` chép nguyên văn `chu_thich.summary`. Khi đặt mã ca E5 vào đúng trường văn bản này trên một bản sao trong RAM, `quet_goi` trả `[]`. Đây là nguy cơ của danh sách trường đề xuất, chưa có bằng chứng rò dữ liệu thực tế. Tài liệu cũng đã gọi K8 là phép quét gần đúng. [Nguồn của `tom_tat`](D:/RCA-flashticket/results/T-075/goi_bang_chung.py:136) · [Phép quét K8](D:/RCA-flashticket/results/T-075/goi_bang_chung.py:214)

Đề xuất trước mắt bỏ tóm tắt cảnh báo tự do khỏi phần gửi, giữ mã luật, loại tín hiệu và thời gian tương đối. Ba cảnh báo của G1 E5 đều đã có các trường đó; `tom_tat` và `ket_thuc_tuong_doi_s` đều là `null` ở nguồn G1 này. Mặt trái là mất câu mô tả thuận tiện ở nguồn sự cố. Quyết định danh sách và quyền gửi vẫn thuộc Minh.

**R6 — KHÔNG CHẶN các số cuối đã tái lập; ảnh hưởng việc dùng báo cáo tự kiểm làm bằng chứng.** K4b được thêm sau khi thấy hai cặp lọt. Tác giả đã công khai trình tự này. Tuy nhiên, `chay_thu.py` ghi kết quả trước và sau vào cùng tên file, và điều kiện `#/tong/dat` không xét `dat_ngoai_y_muon`. Vì vậy, một lần chạy có cặp chéo lọt vẫn có thể trả mã thành công. Trong 34 mục manifest hiện có chỉ có một `ket-qua-thu.json`. Tôi tái lập được **0/30 sau sửa**; con số **2/30 trước sửa** có tường thuật nhưng không có bản kết quả máy riêng trong gói đó. STATE cũng gọi cả 18 đầu ra là viết tay, trong khi đếm `#/ca/*/dau_ra` cho **7 đầu ra có sẵn và 11 đầu ra sinh bằng code**. [Đối chứng chéo và điều kiện đạt](D:/RCA-flashticket/results/T-075/chay_thu.py:143) · [Tường thuật hai lượt](D:/RCA-flashticket/results/T-075/ket-qua-thu.md:57) · [STATE](D:/RCA-flashticket/docs/STATE.md:18)

Sửa tối thiểu là đưa lỗi đối chứng chéo vào kết quả chung nếu tiếp tục dùng nó làm tiêu chí, giữ riêng hiện vật khi chạy lượt sửa, và ghi đúng nguồn của 18 đầu ra. Không cần chạy lại để dựng một bản lịch sử giả định.

### Báo cáo lượt và quyết định cần Minh

1. **Đã làm.** Tôi tự soát đầu ra thật, nguồn E5, hai G1 cũ, code và quyết định trực tiếp chi phối. Đây là lượt phản biện kết quả đầu tiên, chưa có phản hồi của Claude để phân xử. DT18 yêu cầu phần đồ thị và chẩn đoán. Bước 5 của cô yêu cầu LLM diễn giải và gợi ý xử lý. Minh chọn **mức demo** cho W8. Lượt ngoại tuyến đã có khuôn và bộ ví dụ. Tiêu chí chạy LLM trong demo W5 vẫn còn mở. RQ4 về chất lượng, tính hữu ích và so đồ thị với danh sách cũng còn mở vì lượt này không có đầu ra model, đánh giá của người vận hành hay hai điều kiện so sánh. [DT18](D:/RCA-flashticket/docs/reference/sources/DT18-de-tai-va-nhiem-vu.md) · [Bước 5 của cô](D:/RCA-flashticket/docs/reference/sources/advisor-2026-09-23.md:20) · [MRP P8](D:/RCA-flashticket/docs/MRP.md:278) · [Q6–Q7](D:/RCA-flashticket/docs/DECISIONS.md:779)
2. **File thay đổi.** Tôi không sửa file nào, không commit, không SSH, không dùng subagent và không gửi dữ liệu ra ngoài. Các file của lượt làm mà tôi nhận diện được nằm trong `results/T-075/`, LOG và dòng STATE được SPEC liệt kê. Có một khác biệt về **phạm vi dữ liệu** cần Minh xác nhận. Q7 ghi “kiểm trích dẫn ngoại tuyến bằng ca giả”, còn `NGUON` và kết quả lưu dùng thêm ba nguồn thật. SPEC tổng thể có nêu ca sẵn có và W5. Đề xuất giữ hiện vật, ghi rõ phạm vi Minh cho phép trước khi dùng ba nguồn thật làm bằng chứng nghiệm thu Q7. [Q7 được duyệt](D:/RCA-flashticket/docs/DECISIONS.md:780) · [Danh sách đầu vào đã chạy](D:/RCA-flashticket/results/T-075/chay_thu.py:22)
3. **Kiểm đã chạy.** `Get-FileHash` khớp **34/34** mục T-075, **52/52** mục E5, **58/58** mục của bản chép; hai G1 T-065 cũng khớp manifest bàn giao. Dùng Python 3.12 với `-I -B -X utf8`, tôi dựng lại sáu gói và gọi trực tiếp hàm chấm trong RAM. Sáu gói khớp bản lưu, 18 kết quả khớp và 30 cặp chéo đều bị loại. Trên ba nguồn của lượt đầu, cặp `(thực thể, hạng)` khớp lần lượt **1/1, 17/17, 17/17**; nguồn sự cố E5 chỉ có nhóm đầu. Trên **G1 E5 đầy đủ**, bảng hạng khớp **17/17**, Booking hạng 1, có **10** mục bằng chứng, giữ **20/21** mục kế thừa, và `phai_khong_du=False`. Cả **58** con trỏ nguồn được xuất trong gói G1 phân giải được. Hai hash V082 ở `#/che_do_b/du_lieu_loi/v082/output_sha256` khớp hai file đầu ra thật và chỉ nằm trong phần kiểm toán. [Manifest T-075](D:/RCA-flashticket/results/T-075/SHA256SUMS) · [Manifest E5](D:/RCA-flashticket/results/T-073/e5/SHA256SUMS) · [Manifest bản chép](D:/RCA-flashticket/results/T-073/e5/ca-7577dd5b.SHA256SUMS) · [Manifest T-065](D:/RCA-flashticket/results/T-065/may-l11/kiem/manifest-ban-giao.json)
4. **Điều cần Minh quyết.** Đề xuất cho Claude **đáp phản biện ngoại tuyến trước**, giữ R3 và hoãn chọn nhà cung cấp. Chọn model ngay không phân xử được R1–R5; đổi lại phải lùi lượt thử API. Khi cập nhật bàn giao, bỏ việc “chờ T-073 chép G1”. LOG T-073 ghi đã chép lúc **05:31:40Z**, trước khi điều phối ghi T-075 kết thúc lúc **05:43Z**. Nên giữ mẫu từ file sự cố để minh họa trường hợp thiếu và dùng G1 như nguồn riêng. Nếu Minh duyệt sửa, các script, khuôn, mẫu và kết quả T-075 nêu trên đều được ghim trong `results/T-075/SHA256SUMS`; sửa nội dung sẽ đổi hash của mục tương ứng. Có thể giải quyết các điểm trên mà không sửa nguồn T-073/T-065. [Mốc chép G1](D:/RCA-flashticket/tasks/T-073-w5-rca-truc-tuyen/LOG.md:418) · [Mốc kết thúc lượt T-075](D:/RCA-flashticket/tasks/T-070-dieu-phoi-giai-doan-2/LOG.md:351)

### Prompt bàn giao cho Claude

Mẫu hiện có khối cổng G0–G4. Với G6, phần dưới dùng nguyên văn Prompt chung và khối **Người làm đáp phản biện**. Minh có thể chuyển phần phản biện ở trên cùng prompt này. [Mẫu bàn giao](D:/RCA-flashticket/docs/review-prompt.md:117)

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-075, tasks/T-075-w8-llm-toi-thieu/, lượt 1 ngoại tuyến.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P8/P10, W8, chuẩn bị G6.
- Người làm và người phản biện chính thức: Claude là người làm T-075, phiên llm-w8; Codex là người phản biện.
- Tài liệu gốc: tasks/T-075-w8-llm-toi-thieu/SPEC.md và LOG.md; docs/STATE.md; docs/MRP.md; docs/WHY.md; docs/LESSONS.md; docs/DECISIONS.md khối 23/11/2026; docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8.2; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md.
- Phản biện và phản hồi trước: phản biện kết quả lượt 1 của Codex trong chat do Minh chuyển kèm; chưa có phản hồi của người làm.
- Code và kết quả liên quan: results/T-075/ và SHA256SUMS; results/T-073/e5/su-co/bbc0a6d44f.json, results/T-073/e5/SHA256SUMS, results/T-073/e5/ca-7577dd5b/ và ca-7577dd5b.SHA256SUMS; results/T-073/dap-cx21/dinh-chinh-e5-1.md và dinh-chinh-e5-2.md; results/T-065/may-l11/du-lieu/V082-V066+H8a/1e5a3dc5.json và 729604d2.json, results/T-065/may-l11/kiem/manifest-ban-giao.json. Python 3.12, thư viện chuẩn.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; chỉ đọc trên laptop, đọc có chọn lọc, không SSH, không gửi dữ liệu ra ngoài, không dùng subagent hay agent con.

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
```