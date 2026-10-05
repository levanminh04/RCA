"""Readable synthesis of reviewed records; exact old/new wording remains in CSV."""
from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'results/T-020'
p=OUT/'de-xuat-tai-lieu-chung.md';s=p.read_text(encoding='utf-8')
s=s.split('## Nháp DECISIONS và WHY cho từng lựa chọn G1')[0]
s+='''## Nháp DECISIONS và WHY cho từng lựa chọn G1

**Nháp, chưa duyệt.** Chỉ điền phương án Minh thực sự chọn. Không biến khuyến nghị của Codex thành USER_CONFIRMED. Khi ghi phải kiểm mã kế tiếp, nguồn và phiên bản. Căn cứ, phản đối mạnh nhất và bằng chứng làm đổi lựa chọn nằm ở [sáu thẻ](g1-goi-quyet-dinh.md).

### D1 — Danh sách và biến thể baseline

DECISIONS: “Minh chọn D1-__; giữ danh sách Q-37/Q-38, biến thể theo bảng 07; báo tái lập tác giả riêng với so sánh theo protocol chung.”

WHY: **Chọn:** __. **Vì sao:** __, dựa hồ sơ T-013–T-018 và kiểm sâu. **Đối lập:** code ghim làm bảng chính; bản sửa báo riêng; hoặc bản gốc đầy đủ. **Bằng chứng:** [07](07-danh-sach-phuong-phap-va-doc-nhanh.md), [kiểm sâu](trung-gian/method_evidence/deep-source-audit.md), [09](09-kiem-cheo-so-lieu.md). **Hệ quả:** bản sửa không đồng nhất tái lập toàn bài; báo schema và tập ứng viên thiếu. RQ1/RQ3a/b/d phụ thuộc biến thể, không quy toàn bộ chênh lệch cho đồ thị. **Kiểm ở P3:** normal, fixture, parity và candidates trên dev được duyệt; không chọn theo score. **Làm đổi:** pipeline gốc có schema đủ và kiểm không nhãn chứng minh hợp lệ.

### D2 — Dataset và vai trò

DECISIONS: “Minh chọn gói __ trong 06, vai trò theo CSV __; bộ giữ ngoài __ hoặc chưa có bộ đạt; giấy phép/provenance/schema __ còn OPEN, cần đầu vào __.”

WHY: **Chọn:** __. **Vì sao:** __ theo cùng chín tiêu chí cho 40 phần. **Đối lập:** A đa tín hiệu; B kiến trúc thiếu trace; C test chỉ TX0. Không dùng công adapter hoặc “đã có sẵn” làm điểm phân xử. **Bằng chứng:** [V2](01-bang-tieu-chi-hop-nhat.csv), [ba split](06-phuong-an-dataset-va-chia.md). **Hệ quả:** chưa chứng minh C9 đủ ba trục; public data chưa có nhãn vùng ảnh hưởng độc lập hoặc protocol blind hợp lệ. **Kiểm:** schema/census/provenance phải đủ cho vai trò; chỉ mở test/giữ ngoài sau G3 và Minh cho phép. **Làm đổi:** nguồn bất biến, quyền dùng, normal và nhãn chứng minh bộ ngoài phù hợp.

### D3 — Tiếp xúc và chia theo ô

DECISIONS: “Minh chọn D3-__; TX1 có vai trò __ và giới hạn __; duyệt seed 20261004, quy tắc __ và CSV __; RE2-TT 30/60 giữ __.”

WHY: **Chọn:** __. **Vì sao:** __. **Đối lập:** TX1 test có công bố; test chỉ TX0; TX1 chỉ tái lập. **Bằng chứng:** [sổ tiếp xúc](02-so-ca-da-nhin.csv), [assert chia](runs/split-assertions.json). **Hệ quả:** TX2 kéo toàn ô sang dev; alias cần chứng cứ. TX1 không hoàn toàn ngoài thiết kế, không khôi phục TX0 bằng đổi tên. Ít ô test làm khoảng tin cậy chỉ thăm dò. **Kiểm:** identity/ô/census, không TX2 test, không đưa lookup nhãn vào features. **Làm đổi:** phát hiện output/alias TX2 gián tiếp, hoặc Minh chọn định nghĩa test nghiêm hơn.

### D4 — Ngân sách nhãn và hai chế độ

DECISIONS: “Minh chọn ngân sách __; fit normal __, tune chỉ dev, root gold và test outcome chỉ evaluator; mốc ngoài chế độ a __, chế độ b không nhận mốc tiêm; normal giữ ngoài __.”

WHY: **Chọn:** __. **Vì sao:** __. **Đối lập:** normal từng hệ; zero-shot không normal hệ ngoài; known và blind báo riêng. **Bằng chứng:** [V6](05-nhan-va-cua-so.md). **Hệ quả:** học scale/threshold vẫn dùng thông tin normal/regime; cắt trước tiêm chưa chứng minh healthy. Test labels không fit/tune; mốc ngoài chế độ a được Minh làm rõ __ trước P7. **Kiểm ở P3:** runner, bộ cột, filename, crop và chuẩn hóa nhìn tương lai; phân biệt injection/onset/end. **Làm đổi:** không có normal sạch hoặc evaluator onset hợp lệ.

### D5 — Quy tắc cửa sổ

DECISIONS: “Minh chọn W-__; primary __ khóa từ normal trước score, sensitivity __; ghi rõ coverage thiếu; cấu hình tác giả báo riêng.”

WHY: **Chọn:** __. **Vì sao:** __. **Đối lập:** W-time cố định; W-feasible dựa coverage/fit normal. **Bằng chứng:** [yêu cầu từng phương pháp](yeu-cau-dau-vao-hop-nhat.csv), [V6](05-nhan-va-cua-so.md). **Hệ quả:** số điểm tối thiểu để chạy không bảo đảm calibration; không clip âm thầm hoặc chọn window vì phương pháp thắng. **Kiểm ở P3:** normal-only coverage/fit/calibration rồi khóa trước score; báo sensitivity cho các phương pháp đủ điều kiện. **Làm đổi:** normal control chứng minh thiếu coverage/calibration hoặc cơ chế cần history khác.

### D6 — Retrieval@K và Rerank@1

DECISIONS: “Minh chọn __; K theo service __; báo Rerank có điều kiện cùng độ đo cuối, mẫu số 0 là NA; candidate universe/mapping/ties __.”

WHY: **Chọn:** __. **Vì sao:** __. **Đối lập:** thêm Retrieval/Rerank; chỉ báo độ đo cuối. **Bằng chứng:** đề xuất E2 T-018, evaluator ghim và [D6](g1-goi-quyet-dinh.md). **Hệ quả:** prefix ranking không tự là module truy hồi độc lập; mapping không dùng gold; multiple-root cần evaluator riêng. **Kiểm:** lưu candidates trước cutoff, mapping độc lập nhãn; test labels chỉ score, không tune K. **Làm đổi:** không định nghĩa được candidate universe hoặc mapping hợp lệ.

## Phần chờ Minh ngoài thẻ

Nguồn bất biến và cơ chế đọc tiêu đề cho ứng viên giữ ngoài; điều khoản phái sinh/license còn OPEN. V7 đã cấp quyền first-line theo điều kiện, Bank chưa có artifact/cơ chế đáp ứng. Chi phí CIRCA lịch sử gồm worker và queue đã vượt Q-40; nháp T-014 còn chờ cách xử lý riêng, không thêm cổng G1 hoặc đổi nghĩa ba giờ. Các sửa nguồn chung ở mục pending phải duyệt đúng file/đoạn trước ghi. Không khôi phục T-018 E6/D3 đã loại.
'''
p.write_text(s,encoding='utf-8')
notes={
1:'K1 chưa tách công thức bài hai phía với max có dấu/nhánh dict của code, hoặc case-level TP/FP.',
2:'Scale=1 chưa tự chứng minh IQR=0; T-013 có q25/q75/IQR thô nhưng T-006 chưa dẫn chứng đó.',
3:'Khớp 100 ca chưa chứng minh extraction: sentinel 600 nằm ngoài window 99/100; cần giữ giới hạn.',
4:'Recall=1 chỉ trên các ca đã chạy có alarm; cùng ca có thể góp TP và FP, không bảo đảm mọi dữ liệu.',
5:'Ma trận R 15.864 MiB không đại diện toàn detector: còn covariance và thời gian tính.',
6:'Mục giới hạn, không nâng thành lỗi hoặc đề xuất sửa mới.',
14:'Tên không có dấu gạch dưới có thể IndexError; tên nhiều dấu bị cắt, không chỉ bị bỏ im lặng.',
15:'Hashseed chỉ kiểm top-5 ở bốn ca × sáu hashseed; chưa chứng minh mọi dataset/ranking bất biến.',
16:'PC có thể loại isolate hoặc cho graph rỗng; tập ứng viên không tự bằng toàn metric.',
17:'Adjacency có thể đảo cạnh PC có hướng; hồ sơ cũ chưa nêu khác biệt này.',
18:'Khác graph/DA chưa đủ mô tả: cấu hình bài có empirical SVR sigmoid và DA.',
19:'Cutoff 3 không trực tiếp lọc output ranking trong implementation; phân biệt ý tưởng bài và code.',
29:'TraceRCA gốc mặc định multiplier 1, hai phía; tên hàm 3sigma không chứng minh multiplier 3.',
30:'Self-time SLO gốc dùng quan hệ cha–con; mô tả PageRank riêng không bao phủ toàn pipeline.',
31:'Các lỗi T-007 nêu ở đây đã sửa trước đó; không trình thành lỗi mới.',
32:'Chỉ là phạm vi đọc, không chứng nhận lại toàn task cũ.',
46:'T-001 đã sửa hậu quả double-stride: không còn mô tả đơn giản là nửa cửa sổ lỗi.',
47:'LOG T-006 giữ lịch sử và thêm đính chính; 15 giây thuộc docs/code, không gán cho bài.',
48:'T-006 đã tách khớp số công bố và lỗi cơ chế fallback/metric bên trong.',
49:'Ba vị trí đã cập nhật RCD 90 ca; vài checkpoint lịch sử 46 ca còn nguyên, không rút sửa đã áp.',
50:'Hai vị trí đã ghi kiểm loại giả thuyết Windows/Linux; chỉ dẫn lịch sử còn cần ghi closure riêng.',
51:'Đã thêm bằng chứng ca torai-TT trùng dev trong ô bảng T-005, không suy chỉ từ tên.',
52:'Không có sửa mới trong mục này.',
63:'Đã tách CLI orig NezhaRCA và lớp SimpleRCA riêng; bản thật mô tả đầy đủ hơn nháp.',
64:'Đã tách luật Type metric-hoặc-log với nhận xét log riêng RE3-OB.',
65:'Đã bổ sung endswith ss→sock-shop và chuỗi preprocess; chưa định lượng accuracy RE3-SS.',
66:'Giới hạn đã kiểm, không gọi thành lỗi mới; đơn vị duration và exact program vẫn OPEN.',
71:'Đã thêm đường rò nhãn qua bộ cột ở đúng thẻ RE2-TT được duyệt; không suy mọi thẻ đã sửa.',
72:'Đã làm rõ GDN val-threshold và median/IQR test; chưa biết log chương trình sinh bảng bài.',
73:'Q-56 không áp D3: giữ timing T-005, báo rủi ro tái dùng input; không cấp quyền đọc raw.',
74:'Chú thích DecompRCA/PyRCA/RHT+DA/BARO đã áp; danh sách baseline không đổi.',
83:'T-003 vẫn chỉ dẫn Sock Shop sang T-002/P2; cần cập nhật phạm vi hai mẫu và thẻ T-019.',
84:'Đề xuất bổ sung public sources SS/F1–F5 chưa áp. Tám file không đồng nghĩa tám nhãn hợp lệ.',
85:'Chỉ là phạm vi audit 77 file, không có văn bản đích cần sửa.'}
rs=list(csv.DictReader((OUT/'trung-gian/root/application-audit-final.csv').open(encoding='utf-8-sig')))
cs=[r for r in rs if '/dinh-chinh-task-cu.md:' in r['nguon']]
assert len(cs)==34 and {int(r['row_id']) for r in cs}==set(notes)
p=OUT/'dinh-chinh-task-cu.md';s=p.read_text(encoding='utf-8');tail=s.split('## Phản biện T-002:')[1]
head='''# Đính chính task cũ — triển khai tại T-020, giữ lịch sử

Không sửa file task cũ. Bản đã áp hoặc bị Minh loại giữ đúng hiện trạng. Các mục dưới được kiểm từ JSON/CSV thành phần, code, snapshot và quyết định hiện hành. [CSV 90 mục](trung-gian/root/application-audit-final.csv) giữ nguyên từng đề xuất cũ→mới, lý do, câu đích và file:dòng đã đối chiếu; cột `review_status` là trạng thái kiểm cuối. Một section không tự là một thay đổi riêng.

## Hợp nhất 34 section đính chính T-013–T-019

Mỗi hàng trỏ đúng section và ID trong CSV. Cách triển khai T020: các định nghĩa/giới hạn được dùng trong hồ sơ 07, ma trận 04, nhãn 05 và bảng kiểm 09; không sửa lịch sử nguồn. Với mục đã áp, không lặp lại như sửa mới. Với mục không áp, không đưa vào hàng đợi duyệt lại. Với mục chưa áp, đề xuất sửa nguồn cũ chính là đoạn cũ→mới giữ nguyên trong CSV, cần Minh duyệt đúng file/đoạn.

| ID / nguồn section | Vấn đề hoặc hiện trạng đã kiểm | Sửa nguồn chung | Thẻ ảnh hưởng |
|---|---|---|---|
'''
states={'pending':'chưa áp; chờ Minh','variant':'đã áp biến thể','applied verbatim':'đã áp nguyên văn','notapply':'không áp/sửa mới'}
for r in cs:
    i=int(r['row_id']);card='D2/D3/D4' if i>=83 else 'D1/D4/D5'
    head+=f"| {i} — `{r['nguon']}` | {notes[i]} Bằng chứng đích: `{r['citation_exact_lines']}`. | {states[r['review_status']]} | {card} |\n"
head+='''
T-013 R1/N1–N3 đã sửa và task đã đóng; WHY phân bổ hiệu ứng vẫn pending. Q-57 đã áp các lý do TORAI/RCD và D1–D6 T-016; không đồng nghĩa chọn toàn cấu hình P3. WHY-17 đã ghi conventions M4. Q-56 không áp D3/E6 T-018; Retrieval E2 vẫn chờ G1. Nháp ghi “WHY-18 Retrieval” là mã cũ tạm, WHY-18 hiện là GDN diagnostic.

## Phản biện T-002:'''
p.write_text(head+tail,encoding='utf-8')
print('refined shared drafts and all34 correction sections; exact wording kept in source CSV')
