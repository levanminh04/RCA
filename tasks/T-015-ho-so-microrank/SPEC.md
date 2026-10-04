# T-015 — Hồ sơ MicroRank, TraceRCA RCAEval và luật phát hiện trace

- **Trạng thái:** đã duyệt theo ủy quyền của Minh ngày 04/10/2026; chưa hoàn thành.
- **Người làm:** Codex.
- **Người phản biện:** Claude (Minh xác nhận trong phiên 04/10/2026).
- **Thuộc gói MRP:** P1 — **Cổng:** G1.

## Mục tiêu

Trả lời nhận xét đầu tiên của cô: "chưa sâu kỹ thuật của từng phương pháp"; phục vụ RQ1, DT18-NV2/NV3 và bảng điều kiện đầu vào của G1. Giải thích cơ chế MicroRank bằng công thức, code gốc, giá trị trung gian và ví dụ tính độc lập. Sửa hai sai lệch dựng đồ thị/chia nhóm của RCAEval theo ngữ nghĩa gốc; đề xuất biến thể cho P3 theo QT2 và cơ chế, không theo điểm tốt hơn. Mọi đề xuất lựa chọn còn là CANDIDATE, không tự chốt P3 hay cửa sổ.

## Đầu vào

- Luật và nguồn đã đọc: AGENTS.md; STATE; LESSONS; review-prompt; mẫu SPEC/LOG; MRP §2–7; WHY; DECISIONS; DT18; advisor-2026-09-23; REVIEW T-003 R1.
- `results/T-001/danh-sach-phuong-phap.md` §1/3/4/8/9; `results/T-007/kiem-dung-dan.md` §2.3/9/10; `results/T-007/cham/`, `runs/py312-pin/`, scripts và REVIEW T-007. Kết quả T-005/T-006 chỉ dùng khi đã kiểm file thật và phạm vi ca.
- RCAEval local `D:/RCA-ext/src/RCAEval`, revision theo T-001 §9; MicroRank gốc và TraceRCA gốc đúng revision của §9; bài MicroRank WWW'21. Ghim revision/hash trong manifest, không sửa clone chung.
- RE2-OB trên EC2 `~/rca/data/re2ob/`; chỉ 30 thư mục dev `data/rcaeval/re2tt_*` trên laptop. Không mở locked, ZIP TT khác hoặc kết quả ngoài whitelist.
- SSH và môi trường dùng đúng prompt Đợt 1; `~/rca/envs`, `~/rca/src`, `~/rca/data`, `D:/RCA-ext/envs`, `D:/RCA-ext/src` chỉ đọc/chạy.

## Đầu ra

- `results/T-015/ho-so-microrank.md`: đủ 7 mục P1, đường nhãn và yêu cầu dataset khác; kèm TraceRCA bản RCAEval.
- `results/T-015/ho-so-phat-hien-trace.md`: hai luật μ+3σ theo span và luật gốc; đủ 7+2 mục.
- `results/T-015/yeu-cau-dau-vao.csv`: đúng 16 cột trong prompt; mỗi phương pháp/biến thể/detector một dòng.
- `results/T-015/so-sanh-tung-ca.csv`, `kiem-dung-dan.md`, `vi-du-tinh-tay.md`; số liệu và trung gian trong `runs/`, code kiểm độc lập trong `scripts/`.
- `ca-da-chay.csv`, `dinh-chinh-task-cu.md`, `de-xuat-tai-lieu-chung.md`, `moi-truong.md`, manifest nguồn/đầu vào/đầu ra.
- `src/microrank/`: bản sửa và adapter nhận bảng span, không nhận đường dẫn/nhãn root/fault.
- SPEC này; LOG append-only, chép nguyên văn khối task; đúng một dòng T-015 trong STATE.

## Phạm vi ghi

- `tasks/T-015-ho-so-microrank/SPEC.md`, `LOG.md`.
- `results/T-015/`, `src/microrank/`.
- `D:/RCA-ext/work/T-015/`; nếu cần môi trường mới: `D:/RCA-ext/envs/T-015-<tên>` và ghi phiên bản/cách dựng.
- EC2: chỉ `~/rca/T-015/`, mọi cache/tmp đặt tại đây; ngoại lệ duy nhất đã duyệt: xóa `~/.sudo_as_admin_successful` đúng một lần.
- Chỉ dòng T-015 của bảng STATE: đọc lại trước ghi; thay chuỗi chính xác/chèn sau dòng cuối bảng; kiểm các byte ngoài dòng không đổi. Không sửa file chung khác, task cũ, commit/push.

## Các bước theo phụ thuộc

1. **Kiểm nguồn và chuẩn bị** (không phụ thuộc chạy): kiểm HEAD/revision, whitelist 30 dev, hash và nội dung từng tar OB T-007; tra số công bố trước đo mới. Tìm nguồn gốc/paper, tối đa 1 GB tải mới, ghi URL/ước lượng byte vào LOG trước tải. Kiểm: `git rev-parse HEAD`; script manifest dùng SHA-256; kiểm tar đọc trong bộ nhớ. Không đọc kết quả TT ngoài whitelist.
2. **So ngữ nghĩa gốc và tự phản biện SPEC** (cần bước 1/code): lần theo preprocessing, detector, partition, đồ thị, PageRank, spectrum, NaN; bảng file:dòng. Đối chiếu từng SL24–33 và R1 T-003. Kiểm: so AST/diff nguồn và phản ví dụ nhỏ độc lập. Ghi thay đổi SPEC vào phần cuối, không xóa kế hoạch cũ.
3. **Cài bản sửa** (cần bước 2): giữ PageRank và spectrum chính thức; tích lũy operation-operation; chia trace rời nhau và dùng cùng tập cho đồ thị/số đếm như gốc. Tách detector gốc và detector span để không gán một luật là luật kia. Adapter chỉ sửa giao thức đầu vào/đầu ra và lỗi rõ ràng; mọi khác biệt với gốc ghi công khai. Không thay công thức vì điểm dev. Kiểm: toy graph có hai lần gọi cùng operation; partition không giao; `ef/nf/ep/np` không âm; so hàm chính thức với tái tính độc lập.
4. **Chạy kiểm EC2** (cần bước 3, số công bố bước 1): kiểm uptime/free/ps trước mỗi khối; tối đa một tiến trình nặng của T-015, nếu máy đang có tiến trình nặng khác thì chờ và làm phần đọc/tài liệu. `nohup` log ngay từ ca đầu. RE2-OB dùng ±600 s tham chiếu WHY-16; so từng ca với T-007 L20, không chạy lại baseline 90 ca. ±300 s chỉ là kiểm độ nhạy trên 1–2 ca định trước: ca đầu và ca cuối theo tên lexical. Mỗi khối xong chép về ngay, kiểm hash. Kiểm dọn file một lần; không Stop/restart.
5. **Train Ticket, edge cases và tính tay** (cần bước 3; độc lập bước 4 nếu EC2 bận): whitelist 30 ca dev từ thư mục hiện có. Thứ tự chạy round-robin: sắp 10 ô theo tên, mỗi vòng lấy lần lặp kế tiếp. Kiểm tập service có metric nhưng vắng trace; service có trace nhưng không cạnh; tập operation đầy đủ so top_max+6; nêu trần Hit@k theo coverage thực, không quy từ số 11 operation. Ví dụ chọn **`re2tt_ts-auth-service_cpu_1`** trước xem kết quả. Nếu đầu vào không đủ để xếp hạng: giữ thất bại, giải thích; ví dụ dự phòng định trước là `re2tt_ts-route-service_mem_1`, không chọn theo vị trí nhãn. Chép lên EC2 chỉ ca dev thực cần. Kiểm độc lập không gọi hàm tác giả; đối chiếu tất cả PageRank/spectrum/điểm, sai số tuyệt đối và tương đối ≤1e-10 (ghi sai số thực). Nhãn root chỉ đọc để giải thích sau khi ranking đã lưu.
6. **TraceRCA và hồ sơ** (cần bước 2; phân tích artifact T-007 có thể làm ngay): dựng lại lỗi NaN/sắp xếp từ số đã lưu; kiểm trực tiếp code gốc để phân biệt lỗi/chủ ý. Adapter bỏ hoặc định nghĩa rõ zero-support trước sort, tie theo khóa ổn định; không biến kết quả rỗng thành dự đoán. Chạy trên ca dev TT đã chọn vì quy mô mới. Viết 7+2 mục, nguồn công thức/tham số, giới hạn do tác giả nêu tách khỏi giả thuyết riêng. Kiểm: hoán vị cột/dòng, hash seed, không-rỗng và không fallback.
7. **Rà và bàn giao** (cần mọi bước): đối chiếu từng tiêu chí; mọi việc làm được trong giới hạn phải làm. Tự kiểm task T-000–T-012 qua tài liệu có liên quan, sửa kiểm chứng chỉ trong results/T-015; không sửa nguồn cũ. Kiểm toàn file set/diff, byte phần STATE ngoài dòng T-015, số tài liệu từ file kết quả. LOG đủ A–H và 6 mục mẫu; prompt phản biện nguyên văn chung+G1, đủ mọi đầu ra ngoài repo/EC2. STATE chỉ chuyển chờ phản biện khi đủ tiêu chí, nếu thiếu ghi đang làm/chặn tương ứng.

## Edge case và cách kiểm/xử lý

| Trường hợp | Kiểm | Xử lý/giới hạn |
|---|---|---|
| Micro giây | schema, duration/end-start, ngưỡng chia 1000 ra ms | mốc s đổi sang μs đúng một lần; assert số hợp lệ |
| Mất cha, nhiều root | toy và census dev: lookup theo (traceID,spanID), đếm root unresolved | không nối sang trace khác; gốc đặc biệt xử lý root nào phải ghi; thiếu đầu vào thì fail rõ, không đoán |
| Operation cùng tên hai service | toy cùng methodName | khóa service+method; kiểm va chạm dấu phân cách, không âm thầm gộp |
| top_max+6 | so đầy đủ và top-11 | giữ output gốc cho so T-007; đưa full scores riêng cho mapping service đề xuất, chưa chốt P3 |
| d/alpha/iterations/convergence | ghi code:dòng; độc lập 25 vòng, thay số vòng để chẩn đoán | mặc định gốc; không gọi 25 vòng là đã hội tụ nếu chưa có bằng chứng |
| Trace ngang biên cửa sổ/mốc | toy có root trước/con sau; đếm trace thiếu span tại biên | cùng luật startTime [lo,hi) như T-007 để so; ghi trace cắt, không tự thêm dữ liệu ngoài cửa sổ |
| ±300/±600 s | cùng ca định trước, chỉ biến cửa sổ | tham chiếu 600 theo WHY-16; P3 còn OPEN theo Q-54 |
| Không trace bất thường | toy và hai đoạn bình thường | trả trạng thái không đủ bằng chứng/không báo động; không fallback thứ tự cột |
| Hash seed | hai tiến trình PYTHONHASHSEED=0/1, cùng dữ liệu | điểm phải khớp; tie canonical, giữ output raw để so |
| Operation không có baseline/1 span, std NaN | toy | lỗi đầu vào hoặc UNKNOWN rõ; không điền ngưỡng bằng nhãn |
| SpanID trùng giữa trace, dòng trùng | toy | khóa kép, kiểm trùng trong trace; nêu lệch adapter với gốc |
| Nhóm bình thường rỗng/đồ thị rỗng, chia 0 | toy | explicit status, không chấm như thành công |
| Điểm NaN/Inf, ef/nf âm | lưu phổ và check finite/nonnegative | giữ lượt lỗi, giải thích, không âm thầm loại ca khỏi mẫu |
| Service không trace hoặc không cạnh | dev TT, ghép inventory metric độc lập nhãn | phân biệt vắng candidate với có candidate score thấp; trần coverage theo từng ca |

## Kiểm đúng đắn

- Tra bài MicroRank và mốc TORAI/T-007 **trước chạy**. Số công bố dùng để đối chiếu giao thức, không chọn biến thể theo độ gần số. Không tái lập toàn artifact MicroRank riêng nếu không có dữ liệu công bố trong phạm vi: giới hạn khả năng xác nhận số gốc, không hạn chế kiểm cơ chế.
- Hai hash seed và chạy lại 1–2 ca; ghi seed, hash đầu vào/đầu ra. Nếu dao động điểm, đo và giải thích trước dùng số.
- Đầu ra có status; không-rỗng chỉ áp với đầu vào có evidence hợp lệ. Không fallback, không trùng thứ tự cột; hoán vị cột phải giữ điểm/rank. Hoán vị dòng kiểm cạnh và tie.
- Hai cửa sổ đều bình thường: lấy hai đoạn trước mốc của ca ví dụ, chia tại trung điểm **đoạn trước mốc**, không dùng root label. Detector có thể báo giả do ngưỡng; phải báo đúng là báo giả, không mô tả thứ hạng là nguyên nhân có nghĩa.
- So trung gian từng operation: đồ thị hai phía, trace count/overlap, prior v, PageRank, trọng số, bốn ô phổ, Dstar2; độc lập khớp ≤1e-10.
- Đổi thứ tự cột và root label không vào hàm; lớp I/O biết đường dẫn chỉ để đọc/lưu. Mốc tiêm chỉ cho chế độ biết mốc; không gọi kết quả này là tự phát hiện.
- Không bỏ kiểm quy mô TT. Không coi thời gian máy dùng chung là benchmark. Thiếu kiểm thực nghiệm vì SSH/budget phải ghi số đã xong, nguyên nhân, giả định có thể sai và kết luận bị yếu đi.

## Tiêu chí xong

1. Nguồn/revision/hash đã kiểm; artifact T-007 tái dùng hợp lệ; không đọc dữ liệu cấm.
2. Hồ sơ MicroRank, đoạn TraceRCA và hai detector đủ 7+2 mục; công thức đúng code/bài, mọi default có file:dòng.
3. Bản sửa tích lũy cạnh/chia trace rời; đồ thị và số đếm cùng tập; không negative spectrum hoặc lỗi bị giấu; edge cases có kết quả.
4. Có so từng ca RE2-OB với baseline T-007, đủ các ca trong ngân sách; thiếu ca phải ghi chưa hoàn thành yêu cầu và lý do, không báo xong.
5. Có kiểm TT trên dev, census candidate absence/isolated/truncation và coverage ceiling từ kết quả; không suy cơ chế từ trung bình.
6. Ví dụ độc lập khớp mọi điểm số chính thức; có giải thích thứ hạng root sau lưu ranking. Nếu không đủ evidence ở cả hai ca định trước, giữ OPEN tiêu chí này.
7. TraceRCA NaN/order: có phản ví dụ và tái dựng artifact, phân loại nguyên nhân/cách adapter xử lý, không chọn theo điểm cao hơn.
8. Tất cả phép kiểm không nhãn nêu trên đã chạy hoặc thật sự không thể trong giới hạn, kèm hệ quả cụ thể; giữ mọi lượt hỏng.
9. CSV đúng schema, danh sách ca/lý do a/b/c, đính chính task cũ/nháp chung dù không có; LOG đủ bàn giao và prompt không neo; đúng file set cho phép, không mất file chung.
10. Đã thử SSH; nếu kết nối được dọn file đã duyệt đúng một lần và kiểm lại; nếu không thì ghi chưa thực hiện rõ.

## Không làm

Không benchmark P3 toàn dataset mới; không chấm/thiết kế P4–P7; không chốt dataset, cửa sổ P3, nhãn dev/test; không sửa file chung trừ dòng STATE; không mở locked/archive cũ; không gửi tin ngoài; không commit/push; tối đa hai subagent.

## Chi phí ước lượng

Tải code/paper dự kiến <30 MB, dữ liệu mới 0 B. Dùng env đã ghim. Chạy tuần tự, trước mỗi khối dự báo tổng từ thời gian ca pilot và số còn lại, gồm repeat/edge/window/TT, không chỉ tính một ca. Mục tiêu tổng MicroRank RE2-OB <1 giờ; TT <1 giờ; TraceRCA TT <15 phút. Nếu pilot dự báo một khối >1 giờ: báo Minh và chờ đồng ý theo AGENTS luật cứng 8; không tự chạy lượt dài. Trần cứng mỗi dataset/phương pháp 3 giờ, mỗi khối 3 giờ. Quy tắc thu hẹp trước xem điểm: thứ tự lexical OB; TT round-robin ô, chỉ bắt đầu ca mới nếu thời gian dự báo còn lại đủ và tổng <3 giờ; dành 20% ngân sách cho kiểm. Không chọn ca theo kết quả. Thời gian trên máy chia sẻ chỉ là chi phí quan sát, không chính thức. Nếu EC2 bận/không SSH, làm code/tài liệu và kiểm rẻ laptop; không chạy nặng laptop nếu tổng dự kiến >1 giờ.

## Rủi ro và điều chưa chắc

- Chưa kiểm: gốc dùng ES và schema khác; chuyển root/self-time sang parquet có thể thiếu trường, phải đọc gốc trước cài, ghi lệch rõ.
- Chưa kiểm: full paper/artifact có thể không truy cập; chỉ khẳng định chỗ nguồn thực đọc, không suy từ K1 thành FACT.
- Chưa kiểm: EC2 có thể bận; không tranh RAM hoặc thay cấu hình. Nhiều phiên sửa STATE: chỉ đúng dòng và kiểm lại.
- Lựa chọn quan trọng mới chỉ nháp WHY trong `de-xuat-tai-lieu-chung.md`; nơi dùng ghi "(chờ WHY, xem de-xuat-tai-lieu-chung.md)". Không biến đề xuất P3 thành DECIDED.

## Thay đổi trong lúc làm

Chưa có. Chỉ bổ sung tại đây khi có bằng chứng, không xóa nội dung cũ.

### 04/10/2026 — Minh duyệt biến thể sửa đầu vào, trước chạy so T-007

Minh đồng ý phương án 1 kèm (a) tên **MicroRank-RCAEval sửa đầu vào**, không gọi MicroRank gốc; có bảng bước giữ/khác bài/vì sao; (b) lý do chọn ghi trước chạy, theo cơ chế, không theo điểm; không có số công bố để tái lập riêng biến thể này, độ tin cậy từ tính tay và so từng ca T-007; (c) đánh giá khả thi/chi phí của phương án suy kind/root/pod từ dữ liệu không nhãn rồi chạy code+detector gốc, **chưa cài**, để G1 quyết.

Lý do chọn trước kết quả: sửa lỗi đặt lại cạnh và tập trace chồng nhau; khôi phục ngữ nghĩa **cùng hai tập trace rời nhau cho đồ thị và số đếm** như code gốc. Giữ luật span μ+3σ RCAEval để không tạo kind/pod không có trong dữ liệu. Trace sau mốc bất thường khi có ít nhất một span vượt ngưỡng; trace bình thường là phần bù; cả hai đồ thị dựng từ đúng các span sau mốc thuộc nhóm tương ứng. PageRank/phổ lấy nguyên hàm MIT gốc. Đây là biến thể khác detector/self-time/root/pod của gốc; không diễn giải chênh với T-007 là tác động riêng PageRank. Quyết định cho phép kiểm task này, chưa chốt baseline/cửa sổ P3 (chờ WHY, xem de-xuat-tai-lieu-chung.md).

Tự phản biện bổ sung: canonical thứ tự trace/operation để seed không đổi summation; prior anomaly code khác Eq7 bài; code trace-kind là tập operation, bài là cây; normal-only spectrum/epsilon code khác bài. Nhiều con song song có thể làm self-time âm trong gốc, cần nêu khi đánh giá phương án suy schema. Các công thức detector gốc kiểm trên counts giả đúng schema, không suy kind từ nhãn. Không giả xác nhận full MicroRank trên RE2.

### 04/10/2026 — đổi EC2 theo Minh, thu hẹp TT theo cap dữ liệu trước kết quả

Minh chỉ đạo dùng EC2 thứ hai 3.26.62.217, key2.pem, và chuyển việc thiếu RAM lên EC2. Máy hai rảnh nhưng Ubuntu26.04/Python3.14.4, không có môi trường/data của T-007. Tất cả ghi mới vẫn trong `~/rca/T-015/`. Dựng Python3.12.3 riêng bằng uv đã có từ máy đầu; ghim numpy1.26.4/pandas2.2.3/pyarrow18.1.0 và dependency đúng freeze T-007; không cài hệ thống hoặc sửa env chung. Kiểm lặp pilot giữa hai máy trước dùng số.

RE2-OB từ máy đầu 879.283.566 B; full 30 TT trace 548.755.287 B vượt cap1GB khi chuyển cả hai. Thu hẹp phương pháp TT còn **auth_cpu_1, route_mem_1, route_socket_1**, tất cả là dev đã được phép và được chọn theo SPEC trước nhìn thứ hạng MicroRank TT: ví dụ chính, dự phòng, ca quy mô lớn T-005. Chép đúng trace/metric/inject của ba ca 81.471.220 B; tổng telemetry chuyển 960.754.786 B. Schema/footer vẫn đã kiểm30dev. Không suy coverage ceiling cho cả30dev từ ranking3ca; chỉ báo từngca đã chạy và giới hạn khái quát. Tiêu chí chạy TT là kiểm cơ chế/quy mô/candidate trên ba ca; không thành benchmarkP3. Ba ca và giới hạn này định trước kết quả method.

Lượt `ob-main` trên máy đầu hỏng trước method vì CRLF; giữ log, không coi đã chạy89ca. File shell mới phải LF, log vào thư mục lượt mới. Tách preflight và launch: xem ps/free trước, không tự chạy khi có job nặng khác. Mốc T-007 không chạy lại; ca pilot mới là kiểm biến thể và môi trường theo lýdob/a.

### 04/10/2026 — sửa bộ đếm root nullable, không đổi graph/điểm

Rà số TT thấy snapshot audit đếm parent pandas.NA (chuỗi `<NA>`) như mất cha, trong khi census isna nhận root marker. Giữ toàn snapshot/lượt cũ và nguồn kernel trước sửa; bổ sung token `<NA>` chỉ ở phân loại bộ đếm root/missing, không đổi cạnh/incidence hay công thức. Kiểm toy None/NA cho graph và audit giống nhau; kiểm raw scalar và đếm lại3TT lưu correction riêng, không gọi lại phương pháp. Kết quả audit sửa phải dẫn ở hồ sơ; không diễn giải root marker là root frontend/server thật của gốc. Independent inputs cũng phải sửa protocol null; kiểm19đạt trước đó xác nhận khớp adapter cũ, chưa tự chứng nhận phân biệt null/mấtcha.

### 04/10/2026 — xử lý bản sao span theo code gốc, trước chạy lại2ca
Chẩn đoán độc lập tất cả11cột raw hai ca recommendation_loss_1/_2:48/99key duplicate, tất cả là exact copies, không có nội dung xung đột. Guard cũ quá nghiêm so ngữ nghĩa gốc preprocess_data.py:410–445: temp[spanid] dùng một bản cho parent lookup, nhưng pr_trace.append chạy mỗi hàng. Không xóa bản sao khỏi SLO, detector hay prior. Sửa graph giữ multiplicity mỗi row trong pr_trace/audit, dùng một identity để tìm cha; chỉ chấp nhận key trùng có8measurement columns giống nhau, reject conflicting identities. Vì sao: bám cơ chế gốc, không vì điểm; chưa nhìn ranking mới hai ca. Freeze code/toy/bảng so trước sửa; giữ2failure và rerun output mới. Kiểm toy duplicate đối chiếu AST gốc cả4relations và multiplicity, conflictreject, permutation; rerun2ca theo lýdo(c). Dự báo<1phút theo ca tương tự, tổng dataset vẫn<1giờ/3giờ. Đây là bổ sung edgecase trong phạm vi sửa adapter; lựa chọn quan trọng (chờ WHY, xem de-xuat-tai-lieu-chung.md).


### 04/10/2026 — rà cuối và lệnh kiểm thực tế

Giữ nguyên SPEC trước đó; đối chiếu10tiêu chí ở `results/T-015/tieu-chi-xong.csv`. Guard cuối đã kiểm raw90cửa sổ bằng `validate_identity_policy_ob.py`; không conflict và chỉ hai ca đã rerun có duplicate current. Lệnh kiểm đầu ra: `D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B results/T-015/scripts/final_scientific_audit.py`. Lệnh kiểm toy source gốc: cùng interpreter chạy `test_graph.py`, `test_adapter.py`, `test_null_root.py`, `test_original_formula.py`. Bảng so: `compare_ob.py --fixed-dir ...ob-pilot-ec2-2 --fixed-dir ...ob-block-1 --fixed-dir ...ob-block-2 --fixed-dir ...ob-block-3 --fixed-dir ...ob-duplicate-rerun`; precedence chỉ thay failed bằng rerunok, không chọn giữa hai kết quả hợp lệ khác điểm. Ledger: `compare_ob.py --ledger-only`. Bàn giao/JSON/file-scope: `complete_handoff.py` rồi `validate_handoff.py`. Normal-control báo giả được ghi là kết quả kiểm không đạt ngữ nghĩa phát hiện, không sửa detector hoặc che thành PASS về chất lượng. Source/units TraceRCA upstream/full số tác giả chưa kiểm và hệ quả ở báo cáoG. Không cần thêm một lượt phương pháp trên dữ liệu mới.


### 04/10/2026 — sửa R1–R3/N1–N7 theo Minh duyệt sau phản biện
Minh: “duyệt sửa theo đề xuất”, áp dụng danh sách gom theo file trong LOG phiên2. Sửa lời/cấu hình đầu vào và guard hữu hạn; không đổi luật span3σ, PageRank/spectrum gốc,25vòng/top11 hay lựa chọnP3. Bổ sung artifact độ dài trace và chẩn đoán25/26/50/100/101 từ snapshot đã lưu, không chọn vòng theo root. Guard được kiểm toy và quét miền thời gian93file đã dùng trên EC2hai, không chạy ranker mới. Giữ toàn snapshot/log cũ.
Cap tính cả sao chép là diễn giải bảo thủ của người làm, không phải Minh chốt thu30→3. Đã kiểm3/30dev; chưa kiểm27ca và không kết luận về coverage/thứ hạng của chúng. Đây là thu hẹp kế hoạch round-robin; tiêu chí5 nguyên không đặt đủ30. Quyền sửa lần này không có lựa chọn mở rộng27TT; phạm vi P1/mở rộng còn do Minh quyết.
N1: phép thay số vòng đã thiếu trước bàn giao; đã chẩn đoán read-only tại phiên2 rồi lưu artifact trong phiên3. Vòng25 khớp điểm đã lưu nhưng kết quả nhạy số vòng và chưa hội tụ, kể cả100/101. Thiếu phép kiểm cũ không làm sai phép tái tính25vòng; làm yếu đánh giá ổn định mặc định. Không đổi sang vòng cho điểm đẹp hơn.
