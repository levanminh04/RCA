# Nhật ký T-052

Chỉ người làm nối LOG. Người làm Codex, người phản biện chính thức Claude. Bản REVIEW chưa được tạo; các bản Claude dưới đây có loại nguồn phản biện qua chat do Minh chuyển. Ghi hồ sơ không đồng nghĩa Claude đã kiểm văn bản cuối hoặc đã nghiệm thu T13.

## Phiên 1 — 04/11/2026 — Codex — laptop Windows — vai trò người làm

### Mở phiên và quyền

Phiên PLAN/đáp phản biện tiếp nối nhiệm vụ Q-243 và prompt cuối LOG T-051. Đã đọc AGENTS/STATE, mục T-052 trong kế hoạch, nguồn DT18/cô/MRP/WHY/LESSONS/DECISIONS, chuỗi P1–P5 và M1 cùng các đính chính có liên quan. Chưa có SPEC/LOG T-052 trước lượt ghi này. HEAD nền nằm trong manifest. Không có diff tracked ban đầu; nhiều kết quả native nặng/untracked và thư mục cache không đọc được đã có từ trước, giữ nguyên.

Minh chỉ đạo ban đầu chỉ đọc, kiểm rẻ trong bộ nhớ và trình SPEC. Sau đó Minh quyết “hoãn b)” và yêu cầu hai bên phản biện thẳng, hoàn thiện phương án. Minh cấp quyền có điều kiện: “nếu không có bất đồng quan điểm nào với claude thì duyệt ghi luôn ,nếu có thì trình phần bất đồng yêu cầu claude xem xét lại”. Ở lượt trước còn bất đồng nên chưa ghi; lượt này nhận phản hồi Claude mới nhất và chấp nhận các sửa với giải thích cụ thể bên dưới. Điều kiện đã đạt cho đúng gói hồ sơ đã trình; ghi Q-245–Q-248 trước các tài liệu dẫn xuất. Quyền thực nghiệm, mở G3/test/RE3, máy mới và commit/push chưa cấp.

Tệp phản hồi mới Minh đính kèm ngày 04/11 có cùng byte với bản được gửi ngay trước trong phiên. Giữ một bản nguyên văn dưới cuối LOG để người tiếp nhận ở máy khác không cần attachment hoặc lịch sử chat. Hash ở manifest, không coi attachment như native receipt.

### Căn cứ tự soát và thứ tự tiếp nhận

Các lượt trước đã dựng lại nguồn/code/kết quả trước đọc phản biện chính thức đầu. Lượt hiện tại đọc phản hồi rồi tính lại các mệnh đề mới; không khai đây là kiểm mù chưa từng thấy ý reviewer. Những nhận xét riêng cần giữ:
- Lợi ích quan hệ trái chiều theo cặp/bộ; bỏ E1 không phải trái dấu vì OB bằng. Mục tiêu ablation chung chưa được dev hỗ trợ.
- K-b chỉ C/VC khi E5 bật, thiếu 2×2 không tự mất nghĩa vụ giải thích tương tác. T-052 giữ giới hạn, không tự thêm lượt chạy.
- Runner T13 cũ thiếu nhanh_z/che_do hiệu lực; parity C-a0/a1 chưa có lượt native mới nên không gọi xong.
- CI percentile ít ô có thể undercoverage cả khi lo<hi. Bộ lọc suy biến không sửa hiệu chuẩn.
- G1 đã có thành viên tập ở phép chia A-phan-tang. Thiếu allowlist test runtime/nhãn tách/U được ghim cho entry point P7, không phải chưa từng chọn tập test.
- T-051 KB/T-053 có RR đủ 52 ca ở ba worlds khớp; điều này không tự chứng minh mọi trường compact đủ dùng.
- Nguồn phụ hỗ trợ đọc/hash là factual assistance, không thay phản biện chính thức Claude.

### Đáp phản biện cuối của Claude

| Điểm | Kết luận và sửa nhận | Phạm vi tác động |
|---|---|---|
| 1, CI suy biến | Đúng. Mô hình ô thưa tái tính chính xác cho cùng hiện tượng. Ghi “đạt E-04 theo công thức; CI suy biến” cùng câu, luôn báo ô hữu hiệu/ô thua/ca cả hai trượt; thêm dòng CI trọn trên 0. Không tự đổi biên hoặc dựng ngưỡng số ô mới. | A4/cách đọc kết quả. |
| 2, tập test | Đúng về thiếu runtime firewall trong SPEC. G1 đã có A-phan-tang; khóa hash nguồn/thành viên và cơ chế mã mờ trước G3, materialize sau quyền test. Chốt U/alias, private labels, seal trước ghép nhãn, không đưa mã/path/root/fault/cell vào API phương pháp. | Trước quyền P7. |
| 3, số thực | Đúng. Giữ hàm bootstrap/seed WHY-28, lưu raw và so cận ROUND_HALF_EVEN 12 chữ số; bằng biên không đạt, cùng policy cho chuyển mức/suy biến. Fixture biên cần triển khai khi được phép. | Công cụ A4. |
| 4, McNemar | Nhận sửa đa số ≥2/3 seed làm bản phụ chính, all-3 làm độ nhạy ổn định. Tiêu chí all-3 tôi từng đề xuất là endpoint khác, gây đối xứng không tốt nếu đọc như so xác suất đúng bình quân. Mỗi ca một cặp, tie-safe root chắc hạng 1, lỗi=0; bảng chính vẫn kỳ vọng hòa/trung bình seed. Tiền lệ GALA+ hỗ trợ một cách làm, không chứng minh đa số là cách duy nhất đúng. | Phép phụ, không quyết A4. |
| 5, chuyển mức | Đồng ý nâng OB 0,025→0,05 chỉ khi P qua E-04 và lo<hi. Ghi “CI hợp lệ/tính được” là kiểm toàn vẹn đầu vào chứ không là hiệu chuẩn. CI suy biến chặn nhận mức; không suy biến vẫn có giới hạn. Cả hai thay đổi Q-211 (Holm và phép chính TT) được ghi. | A4 Q-246. |
| 6, phân tầng | Đúng. Dataset/loại lỗi/vị trí/ô/ca. Giữ Q-60(b), định nghĩa p75/p90 từ T-021, riêng nguồn N/alias và nhóm vắng/OPEN; kiểm lại test sau quyền, không dùng A/hạng để đổi nhóm. | Bảng T13/P7. |
| 7, tiếp xúc | Đúng. Q-60 chấp nhận TX1 khai báo; Nezha ca liền kề và RE3 cùng hệ/công cụ. Giữ sáu câu G3 và sổ xem. Không gọi test mù hoàn toàn. | Phạm vi kết luận độc lập. |
| 8, lý do rộng và hợp nhất | Đúng. Viết theo từng vế, giữ VC×E5, đủ các mục mẫu, tạo một SPEC hiện hành. | Toàn hồ sơ. |

Bất đồng có ảnh hưởng quyết định giữa hai bên đã được xử lý bằng các cách ghi cụ thể ở SPEC/Q-245–Q-248. Nhận xét “0/20 ô khác 0 cho cận khoảng 14%” chỉ đúng dưới mô hình Bernoulli iid có chung xác suất; không dùng số đó như cận hiệu ứng MRR hoặc power thực của test. Bản hợp nhất giữ giới hạn thưa/ít ô mà không cần dùng con số này. Nguồn Canay/Bretz chỉ cung cấp điều kiện lý thuyết, không chứng nhận benchmark thỏa điều kiện.

Hai bên đồng ý không thay bằng chứng khoa học. Đề xuất dừng tranh luận lựa chọn SPEC theo nội dung đã hội tụ; Claude chưa kiểm file cuối và vẫn có thể chỉ lỗi thực ở lượt kiểm văn bản nếu Minh chuyển. Không tự mở thêm vòng hoặc gửi prompt.

### Kiểm rẻ và kết quả

- Kiểm SHA-256 các bảng trực tiếp trước dùng theo manifest upstream; inventory và kết quả từng file trong results/T-052/manifest.json. Không coi hash manifest lịch sử của tài liệu đã sửa là hash hiện hành.
- Đối chiếu RR KB và T-053 52/52 ca, đủ P/S_lo/S_hi ở lượt tổng hợp trước. Tính M1−K-R0/−TORAI B theo ca và bảng ablation từ số đã lưu.
- Tính lại C-e bằng Node đọc ce.json và nhãn dev đã ghim: MRR nhãn root thật 0,07872663922395691, Hit@1=0, n=30, mọi returned=68, 0 hòa đầu, 16 top khác nhau, top hai mỗi 5. H68/68=0,07064791602542894. Nền thật TT MRR=167/180. Top-mass dùng kỳ vọng hòa ở triển khai tổng quát, không mặc định lấy phần tử đầu.
- Tính lại đa seed TORAI B từ T-024/cham-a.json: số ca có 0/1/2/3 seed root chắc hạng 1 là 4/0/0/26. Chưa đọc seed test.
- Số ô TT dev khác tổng chênh 0 là 4/10; phép dịch +0,05 rồi liệt kê dấu cho p minh họa 0,140625, không gọi đó là kiểm hợp lệ E-04. OB 3/13 ô tổng chênh khác 0, lần lượt 1,5; 1; 1.
- Kiểm phản ví dụ synthetic **bằng phân phối nhị thức chính xác trong bộ nhớ**, không chạy phương pháp/dữ liệu mới. K~Bin(20,p); conditional bootstrap K*~Bin(20,K/20), chênh mỗi ô là 0 hoặc −a với a·p=0,05. Cận phân vị lý tưởng 2,5%/97,5%, strict so sau làm tròn. Tỷ lệ đạt công thức ứng với (a,p)=(1;0,05),(1/2;0,1),(1/3;0,15),(1/6;0,3) là 0,3584859224; 0,1215766546; 0,0387595311; 0,0354831323. Ở cặp cuối, riêng đạt với CI không suy biến là 0,0346852096. Đây là phân bố lý tưởng của mô hình giả, không cố tái tạo từng số Monte Carlo 10.000 mẫu của Claude và không ước lượng test thực.
- Kiểm ví dụ float: 0.9−0.95>−0.05 True, 0.85−0.9>−0.05 False. Cần policy biên nhất quán.
- Không đọc data/locked, không chạy phương pháp/pilot, không khởi động EC2 hoặc tạo script tạm ngoài repo.

Công thức kiểm nhị thức để tiếp nhận chỉ đọc: cộng trên k=0..20 xác suất C(20,k)p^k(1−p)^(20−k), tại mỗi k lấy phân vị rời rạc Bin(20,k/20) cho hai đầu rồi nhân −a/20. Tính direct convolution/PMF là phép rẻ trong bộ nhớ; giới hạn ít ô giữ nguyên dù công cụ tính đúng.

### Quyết định của Minh và gói ghi

Q-245 ghi nguyên lời hoãn (b), tách các hệ quả Q-66/P/R/F1. Q-246 ghi rõ A4 mới và cách đọc giới hạn. Q-247 cụ thể hóa C-03/C-15 B đã duyệt hướng. Q-248 ghi quyền có điều kiện tạo hồ sơ, vai trò, các lựa chọn còn lại và phần chưa được quyền chạy. Minh chưa duyệt G3 hoặc P7.

| File | Thay đổi đã thực hiện theo gói trình |
|---|---|
| docs/DECISIONS.md | Nối Q-245–Q-248 trước tài liệu dẫn xuất, giữ lịch sử. |
| tasks/T-052-t13-va-ho-so-g3/SPEC.md | Bản hợp nhất đầy đủ mẫu, ma trận/dev/cơ chế/A4/cohort/quyền/chi phí/rủi ro. |
| tasks/T-052-t13-va-ho-so-g3/LOG.md | Lịch sử, đáp từng điểm, kiểm và prompt; kèm nguyên văn phản biện nhận. |
| docs/STATE.md | Thêm đúng dòng T-052 duyệt ghi hồ sơ, chưa chạy. |
| docs/WHY.md | WHY-04 cách dùng B, WHY-06 A4 hiện hành, nối WHY-76/77 cho nền sau T-051 và căn cứ đánh giá. |
| AGENTS.md | Chỉ đồng bộ dấu hiệu §11 về sửa sau test theo C-15 B; giữ quyền mở dữ liệu. |
| docs/MRP.md | Chỉ các đoạn P7/§6.1/§7/§9 của gói C-15 B, dẫn phạm vi (a) và A4 mới. |
| docs/LESSONS.md | QT6 đồng bộ chính sách B. |
| results/T-052/manifest.json | Lớp hồ sơ, file sửa/tạo, nguồn kiểm hash và quyền; không là kết quả thực nghiệm. |

### Bước tiếp theo và tiếp nhận

1. Đọc Q-245–Q-248, SPEC, manifest, LOG này và các phần nguồn mà câu hỏi phụ thuộc. Kiểm lớp manifest trước dùng bản ghi nặng. Không dùng prompt cũ để mở quyền rộng hơn.
2. Nếu Minh chuyển Claude, dùng prompt cuối LOG để chỉ kiểm văn bản/ghi sổ trong chat; không tự tạo REVIEW.
3. Sau quyền triển khai riêng, thực hiện nguồn→wrapper/fixture→pilot native→reuse/chấm→ca/vùng→B6. Trình số đo pilot và quyền native rộng nếu cần, không tự chạy khi mới có quyền ghi hồ sơ.
4. Trước P7 còn cần công cụ dev đã kiểm, tập ca/firewall, manifest đóng băng, budget/máy và Minh duyệt G3/commit/quyền mở. RQ3a/b độc lập, PRF vùng, FT và LLM vẫn còn các đầu ra sau.
5. Đề xuất commit khi Minh muốn: “docs: freeze T-052 specification and reconcile evaluation decisions”. Chưa commit/push.

### Kết thúc lượt ghi — kiểm văn bản đã hoàn tất

1. Đã hợp nhất SPEC, nhận các sửa Claude có căn cứ, ghi quyết định và đồng bộ chính sách B trong đúng gói trình. Đầu ra hiện là hồ sơ được duyệt ghi; T13 chưa chạy và task chưa nghiệm thu.
2. File đổi đúng chín đường dẫn trong bảng phạm vi ở trên, gồm sáu file tracked cập nhật và SPEC/LOG/manifest mới. Giữ nguyên src, dữ liệu và kết quả cũ. Manifest không tự băm, các đầu ra còn lại ghim byte/SHA-256.
3. Kiểm 29 nguồn theo con trỏ hash upstream đều khớp. Thêm năm nguồn G1 khớp Git blob nền; không gọi chúng là có manifest gốc độc lập nếu chưa tìm thấy. Đủ 12 mục mẫu SPEC, 20 liên kết local trong SPEC tồn tại, Q-245–Q-248 mỗi mã một dòng, prompt chung chỉ thay ô trung tính và giữ nguyên khối công đoạn/G3. Đã đọc toàn bộ thay đổi chủ đích, git diff --check và cached --check qua sau sửa dòng trống EOF. Chuẩn hóa policy biên/seed/multi-seed/worlds và kiểu kết luận có điều kiện nhất quán giữa SPEC, WHY và DECISIONS. JSON manifest parse được và kiểm lại hash đầu ra sau cùng.
4. Không còn phản đối có ảnh hưởng lựa chọn giữa Codex với phản hồi Claude mới nhất sau tiếp nhận sửa. Giới hạn khoa học còn A0, dev chọn lặp, M4 tái lập, VC×E5, snapshot revision, ít ô/bootstrap/hoán đổi dấu, TX1 và miền RE3. Đã chỉ rõ phần cần kiểm trước G3 trong SPEC. Claude chưa kiểm văn bản ghi lần này; đồng thuận phương án không thay nghiệm thu/căn cứ hiệu quả.
5. Bước tiếp theo là quyền triển khai dev và kiểm công cụ/pilot theo SPEC, hoặc Claude kiểm văn bản nếu Minh chuyển prompt dưới đây. Không suy việc ghi hồ sơ thành quyền mở dữ liệu hoặc chạy máy.
6. Lệnh kiểm cuối: git diff --check; git diff --cached --check; git diff --name-only; git diff -- src docs/review-prompt.md data. Phép Node chỉ đọc kiểm JSON/SHA-256, mục mẫu/link và đối chiếu prompt; lệnh ghi cuối là làm mới manifest cho byte LOG sau mục kết thúc này. Biên nhận hash đầu ra giữ trong manifest.

## Phản biện Claude nhận qua Minh — nguyên văn nguồn chat cuối


<details>
<summary>Bản nhận nguyên văn, không phải REVIEW.md đã ghi bởi Claude</summary>

Tôi sẽ kiểm độc lập ba việc: điều kiện chuyển mức A4 có xử lý được phản ví dụ không, quy tắc McNemar với TORAI B, và số C-e mới. Ngoài ra tôi rà xem hồ sơ G3 còn thiếu gì ngoài các điểm hai bên đang tranh luận. A4 sẽ được kiểm bằng mô phỏng số giả trong bộ nhớ, không dùng dữ liệu dự án.

# Đánh giá phản hồi Codex và phần còn thiếu

**Kết luận:** Codex đúng ở phần lớn các điểm, và tôi rút lại hai nhận định của mình. Tuy vậy vẫn thiếu 2 điểm chặn việc khóa G3: câu kết luận E-04 khi CI suy biến và danh sách ca test. T13 trên dev không bị chặn.

## Thiếu và CHẶN khóa G3

**Điểm 1. Điều kiện của Codex chỉ bảo vệ OB, câu kết luận chính về TT vẫn hở**
- **Chặn:** bảng diễn giải và dòng A4. Không chặn T13.
- **Sai gì:** khi CI suy biến, Codex chặn OB nhận thêm mức kiểm định nhưng vẫn báo "kết quả áp công thức E-04". Nếu `[0; 0]` không đủ cho OB, thì cũng chưa đủ để câu đầu chỉ ghi "đạt E-04".
- **Bằng chứng:** tôi mô phỏng số giả với 20 ô, đúng tại biên θ = −0,05, dùng phân vị như [`danh_gia.bootstrap`](src/p3/danh_gia.py:245).

| Mô hình ô thua | Tỷ lệ "đạt E-04" (mức khai 2,5%) | Trong đó CI `[lo = hi]` |
|---|---:|---:|
| −1, 5% số ô | 35,4% | 35,4% |
| −1/2, 10% số ô | 12,2% | 12,2% |
| −1/3, 15% số ô | 3,9% | 3,9% |
| −1/6, 30% số ô | 3,6% | 0,05% |

- **Đọc đúng:** đây là số giả, không phải xác suất trên test. Nó cho thấy CI suy biến có thể đi cùng bác bỏ sai thật, không chỉ trường hợp hai bên cùng trượt.
- **Hậu quả:** câu kết luận chính có thể mạnh hơn bằng chứng. [Q-211](docs/DECISIONS.md:304) mục 4 đã yêu cầu cảnh báo khi ít ô, nhưng bảng phản hồi của Codex chỉ xử lý ba thế giới và McNemar ở Điểm 4, bỏ phần này.
- **Sửa tối thiểu, không thêm ngưỡng số ô:**
  - Câu E-04 luôn kèm số ô khác 0, số ô M1 thua và số ca hai bên cùng trượt.
  - Khi `lo = hi`, ghi rõ "đạt theo công thức, CI suy biến".
  - Thêm câu về giới hạn: ví dụ 0/20 ô khác 0 chỉ cho biết tỷ lệ ô khác 0 dưới khoảng 14% ở mức 95%.
  - Thêm dòng "CI nằm trọn trên 0" vào bảng.

**Điểm 2. Chưa có danh sách ca test làm mờ và cách ghép nhãn**
- **Chặn:** mục "tập ca" của G3 và quyền chạy P7.
- **Sai gì:** bản đầu có "tập ca", bản sửa bỏ khỏi danh mục B6. Tìm trong `results/T-021` đến `T-026` không thấy allowlist hay universe cho test; [T-022](results/T-022/) chỉ có `allowlist-dev.json` và `nhan-dev.json`.
- **Hậu quả:** thư mục RE2-TT chứa tên root, ví dụ `re2tt_ts-auth-service_cpu_1`. Nếu tạo danh sách lúc mở test mà không khóa trước, đây là đường nhãn có thể lọt vào.
- **Sửa tối thiểu:** thêm đầu ra gồm script sinh mã mờ, quy tắc không in tên, nơi giữ nhãn, thứ tự đóng dấu rồi mới ghép nhãn, và U của test ([WHY-26](docs/WHY.md:286)). Việc chạy thật chờ quyền mở test.

## Thiếu nhưng KHÔNG CHẶN

**Điểm 3. Cận đúng bằng −0,05 có thể đổi kết quả do số thực**
- **Bằng chứng:** `0.9 - 0.95 > -0.05` cho `True`, còn `0.85 - 0.9 > -0.05` cho `False`, dù cùng giá trị thật. Hàm bootstrap [trừ hai mảng số thực](src/p3/danh_gia.py:254). Trong một mô hình giả, cận rơi sát biên ở 13,7% lượt.
- **Sửa:** khóa cách so, chẳng hạn làm tròn 12 chữ số trước khi so. Bằng biên thì không đạt.

**Điểm 4. Tiêu chí McNemar của Codex thiên về M1**
- **Sai gì:** M1 chạy một lần, còn TORAI B phải chắc hạng 1 ở cả ba seed. Khi seed lẫn kết quả, cặp lệch sẽ nghiêng về M1. Số 26/4/0 trên dev khớp, nên dev chưa lộ vấn đề này.
- **Sửa:** dùng đa số phiếu làm bản chính, theo [tiền lệ GALA+](docs/KHAO-SAT-SAU-K1-K6.md:129). Báo tiêu chí cả ba seed làm độ nhạy.

**Điểm 5. Điều kiện chuyển mức cần viết chặt hơn**
- "TT phải tính được CI" gần như không lọc gì, vì ca lỗi có RR 0 và hàm [chỉ báo lỗi khi thiếu ca](src/p3/danh_gia.py:217).
- "Không suy biến" cần định nghĩa là `lo < hi`.
- Điều kiện này không phủ hết trường hợp. Chỉ một ô −0,3 cho CI [−0,045; 0], vẫn qua dù 19 ô còn lại bằng 0. Vì vậy các số đếm ở Điểm 1 vẫn cần báo.

**Điểm 6. Thiếu báo cáo theo loại lỗi và vị trí root**
- [MRP P7](docs/MRP.md:273) yêu cầu báo theo dataset, loại lỗi và vị trí thành phần gốc. Bản sửa chỉ nêu bộ, ô và ca.
- Vị trí root trên test mới [suy theo root, chưa kiểm](results/T-021/goi-g1.md:174), nên phải khóa định nghĩa trước khi mở.

**Điểm 7. Thiếu phần khai mức tiếp xúc**
- [Q-60](docs/DECISIONS.md:68) và [T-021](results/T-021/goi-g1.md:158) yêu cầu khai báo khi báo kết quả: test là TX1 và có ca đã dò triệu chứng.
- Nezha còn có [ca liền kề nằm hai phía](results/T-021/goi-g1.md:160).
- RE3 có [giới hạn tính độc lập](results/T-021/goi-g1.md:179).
- Hồ sơ G3 cần một mục riêng, cùng [sáu câu ở cổng](docs/MRP.md:339).

**Điểm 8. Một lý do viết quá rộng và SPEC đang rời rạc**
- Câu "dấu chênh TT và OB trái nhau" đúng với bỏ E2, bỏ E5 và K-R0. Với bỏ E1 thì TT giảm, OB không đổi. Nên viết theo từng vế.
- SPEC hiện nằm rải ở ba tin nhắn. Luật 0 cần một đề xuất đúng nội dung, nên Minh cần một bản hợp nhất đầy đủ mới duyệt được.

## Phản hồi từng ý của Codex

| Ý của Codex | Kết luận | Bằng chứng riêng |
|---|---|---|
| Chuyển mức một chiều hợp lệ, không cần p của TT | **Đúng.** | Lập luận tự kiểm; lần trước lưới p không có vi phạm |
| "Cần từng phép kiểm đạt mức đã khai" | **Đúng một phần.** Khi chỉ H0 của OB đúng, sai số OB ≤ 0,05 không phụ thuộc TT. Khi cả hai H0 đúng, TT yếu gây hại như nhau ở mọi phương án, kể cả cố định 0,025. Vậy đây không phải lý do riêng chống chuyển mức. | Xét theo trường hợp |
| Phản ví dụ `[0; 0]` khi hai bên cùng trượt | **Đúng một phần.** Trong ví dụ đó θ = 0 nên H0 của TT sai, và OB ở 0,05 không thêm sai số gia đình so với Holm. Nhưng mô phỏng cho thấy CI suy biến cũng có thể là bác bỏ sai, nên điều kiện có ích hơn tôi nghĩ ban đầu. | Điểm 1 |
| Thêm điều kiện cho chuyển mức | **Tôi chấp nhận**, với định nghĩa ở Điểm 5. Nó không làm tăng sai số vì chỉ bớt bác bỏ. Nó chưa thay được Điểm 1. | Bảng mô phỏng |
| Ở OB, đảo dấu chỉ là phép tính chính xác, phép kiểm cần H0 hoán đổi dấu | **Đúng**, khớp [KS-08](docs/KHAO-SAT-SAU-K1-K6.md:271). Đề xuất dừng ở kết luận có điều kiện, không mở thêm phép suy luận về trung bình. Dòng A4 phải ghi đúng H0 này. | KS-08 |
| Bỏ 0,50/0,31 khỏi dự toán sức kiểm định | **Đúng. Tôi rút lại các số này.** Mốc "5 hay 6 ô" vẫn đúng. | Mô hình của tôi quá đơn giản |
| C-e: root MRR không trả lời câu hỏi thiên lệch | **Đúng. Tôi rút lại cách viết cũ.** Nên giữ cột RR của root cho [MRP §6.7](docs/MRP.md:332), ghi rõ là root của ca thật. | 16 thực thể khác nhau, 10/30, 0 hòa, 68 thực thể, tái tính khớp |
| Chạy C-e mô tả trên test cho M1 | **Hợp lý.** Không cần nhãn cho phần xếp hạng. Cần đóng dấu trước khi ghép RR và đưa 60 cửa sổ vào dự toán P7. Dữ liệu tới t−600 chưa kiểm được trước khi mở. Minh quyết. | [Hợp đồng C-e](tasks/T-043-thiet-ke-rca-m1/SPEC.md:724) |
| Seed 20261005, dùng lại hàm bootstrap | **Đúng**, thêm Điểm 3. | [WHY-28](docs/WHY.md:308) |
| VC × E5 và ablation | **Đúng**, với sửa ở Điểm 8. | [WHY-72](docs/WHY.md:1110) |
| Ba thế giới, đã xem khác đã dùng, nguồn \|O\| | **Đúng.** | Đã đọc 52 bản ghi native ở lượt trước |

**Nguồn chưa đọc được:** PDF của Canay không đọc được vì thiếu công cụ, và tôi không mở bài Bretz. Lập luận trên không dựa vào hai bài này.

## Việc Minh cần quyết

1. **Ngưỡng OB:** tôi vẫn khuyến nghị 0,025, nâng lên 0,05 khi E-04 đạt với `lo < hi`. Cố định 0,025 cũng hợp lệ và đơn giản hơn.
2. **Câu E-04 khi CI suy biến:** tôi khuyến nghị giữ "đạt theo công thức" kèm cảnh báo trong cùng câu, vì Q-211 đã cho phép. Nếu đổi thành "chưa chứng minh được" thì phải sửa cách đọc M-45.
3. **C-e trên test:** chạy mô tả cho M1, hoặc chỉ báo dev và ghi rõ chưa kiểm lại.

## Báo cáo lượt

1. **Đã làm:** kiểm từng ý của Codex, mô phỏng điều kiện chuyển mức, tái tính C-e và TORAI B, rà phần thiếu so với MRP, G1 và B6.
2. **File đã thay đổi:** không sửa file nào trong repo. Script nằm tại C:\Users\84583\AppData\Local\Temp\claude\5926e3c52aa473a7\163f5095-b9e6-4c82-8373-cf6359c86e1b\scratchpad\s12.py và C:\Users\84583\AppData\Local\Temp\claude\5926e3c52aa473a7\163f5095-b9e6-4c82-8373-cf6359c86e1b\scratchpad\s13.py.
3. **Kiểm đã chạy:** mô phỏng số giả chạy trong môi trường `py312-pin`; số C-e đọc từ `results/T-051/kb-002/ce.json`, số TORAI đọc từ `results/T-024/cham-a.json`. Không chạy phương pháp, không mở dữ liệu khóa.
4. **Còn lại:**
   - **Task đạt tới đâu:** chưa có bản SPEC hợp nhất để duyệt.
   - **Câu hỏi nguồn:** RQ3a, P/R/F1 của M1 và lợi ích độc lập vẫn OPEN.
   - **Bất đồng còn lại:** Điểm 1 và Điểm 4; điều kiện chuyển mức ở Điểm 5 chỉ còn phần câu chữ.
   - **Quyết định bị ảnh hưởng:** khóa A4 và G3.

**Đề xuất:** tiếp tục đúng một lượt. Codex gửi một bản SPEC hợp nhất, tôi chỉ kiểm bản đó, rồi Minh duyệt. Lý do là các sửa đổi đang rải ở nhiều tin nhắn. Phần thống kê đã hội tụ, không nên tranh luận thêm ngoài ba quyết định trên.

## Prompt bàn giao cho Codex

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-052 — T13 trên dev và hồ sơ G3 cho RCA chế độ (a). Các bản SPEC và phản hồi trong chat do Minh dán nguyên văn kèm prompt này.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P6, chuẩn bị G3 và P7.
- Người làm và người phản biện chính thức: dự kiến Codex làm, Claude phản biện, phân công triển khai chưa chốt.
- Tài liệu gốc: D:/RCA-flashticket/tasks/_MAU/SPEC.md, D:/RCA-flashticket/docs/KE-HOACH-SAU-T047.md, D:/RCA-flashticket/docs/KE-HOACH-GIAI-DOAN-TOI.md, D:/RCA-flashticket/tasks/T-043-thiet-ke-rca-m1/SPEC.md, D:/RCA-flashticket/tasks/T-051-t11-t12-va-kb/LOG.md và các bản đề xuất do Minh gửi kèm.
- Phản biện và phản hồi trước: bản đề xuất, các bản phản biện Claude, các bản đáp Codex và bản kiểm lại mới nhất của Claude, do Minh gửi kèm theo thứ tự thời gian.
- Code và kết quả liên quan: D:/RCA-flashticket/src/m1/, D:/RCA-flashticket/src/m1_danh_gia/, D:/RCA-flashticket/src/p3/, các hồ sơ, revision và manifest được dẫn trong bản đề xuất và phần phản hồi.
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

Công đoạn: người làm đáp phản biện. Giữ vai trò người làm, không là người phản biện chính thức của chính task.
Tự soát yêu cầu và mọi file đầu ra gốc cần để trả lời các câu hỏi như một người chưa từng làm task, TRƯỚC khi mở kết luận các bản phản biện. Ghi danh sách điểm tự tìm được vào LOG trước khi mở các kết luận ấy nếu được phép ghi; phiên chỉ đọc ghi nhận xét trong chat.
Sau đó kiểm từng điểm phản biện trên file/code/dữ liệu thật; chạy lại khi rẻ và được phép. Kết luận đúng / đúng một phần / sai / chưa kiểm được với bằng chứng riêng. Reviewer có thể sai, nói quá hoặc đề xuất sửa có mặt trái.
Nếu được Minh cho phép: điền bảng Phản hồi của người làm ở cuối đúng bản phản biện; thêm N1, N2… cho điểm tự tìm được với CHẶN/KHÔNG CHẶN; để trống cột Minh quyết; nối LOG đủ mục 7 của AGENTS, gồm đề xuất sửa gom theo file; chỉ cập nhật dòng task trong STATE khi được phép. Không sửa nội dung hay prompt của reviewer hoặc tự sửa báo cáo/code.
Nếu chưa có quyền ghi các phần này, trình phản hồi và đề xuất trong chat. Soạn prompt bàn giao cho người phản biện kiểm độc lập.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

</details>

## Prompt bàn giao hiện hành — kiểm văn bản hợp nhất và ghi sổ

Minh chọn chuyển hay dừng. Chưa có quyền ghi file phản biện trong lượt này.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-052 — D:/RCA-flashticket/tasks/T-052-t13-va-ho-so-g3/SPEC.md và LOG.md; hồ sơ ghi ngày 04/11/2026.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P6, chuẩn bị G3/P7.
- Người làm và người phản biện chính thức: Codex làm, Claude phản biện theo SPEC.
- Tài liệu gốc: SPEC và LOG T-052; docs/STATE.md, docs/DECISIONS.md, docs/WHY.md, docs/MRP.md, docs/LESSONS.md, AGENTS.md; docs/KE-HOACH-SAU-T047.md; docs/KE-HOACH-GIAI-DOAN-TOI.md; SPEC T-043 và LOG T-051; diff với commit dc01bc0d3cc4e945f78be7e7b6607581946213a8, cộng file mới liệt kê ở manifest results/T-052/manifest.json.
- Phản biện và phản hồi trước: các bản đề xuất, phản biện Claude và đáp Codex do Minh chuyển trong chat; bản phản biện Claude cuối cùng và bảng đáp được giữ ở LOG T-052, theo thứ tự nhận và ghi hồ sơ.
- Code và kết quả liên quan: src/m1/, src/m1_danh_gia/, src/p3/; kết quả và manifest của các task nguồn SPEC dẫn; results/T-052/manifest.json và biên nhận trong LOG; lượt này chưa có thực nghiệm T-052.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; đọc và kiểm rẻ trong bộ nhớ.

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


## Phiên 2 — 04/11/2026 — Codex — laptop Windows — người làm

### Quyết định của Minh trong phiên

Minh trả lời “duyệt sửa” cho đề xuất ghi đúng bảy file. Q-249 ghi quyền này. Phiên thuộc EXECUTE cho chỉnh hồ sơ. Quyền triển khai T-052 vẫn trình riêng.

### Kết quả tự soát và sửa

- KB T-051 giữ blocks của 410 bản ghi trong ba world, khớp native K T-053 trong lượt rà. KB gọn thiếu O, coverage và vùng. Bảng mới chỉ rõ nguồn từng trường. C-d và vùng tại P. C-a cần parity native trước khi dùng phép chiếu.
- Nguồn vị trí lịch sử Nezha quanh mốc tiêm và nhóm ô TT giữ riêng. Ứng viên lấy nút từ native K-R0 giữ span bọc và cạnh từ extra.G_N. Kiểm đọc trên 52 ca dev cho thấy mọi đầu cạnh N thuộc tập nút dựng được. Cửa sổ, alias, nút vắng/bậc 0 cần đối chiếu khi triển khai.
- Dự toán mới tách làm công cụ, máy, phân tích, hồ sơ và phản biện. T-048/T-053 là mốc native theo tải đã đo. T-051 manifest đính chính lượt 1 có phân rã giải nén/nạp JSON. Thời gian T-052 và P7 local chưa đo.

### Kết thúc lượt ghi

1. Đã ghi Q-249, chỉnh SPEC và hai kế hoạch, lưu bản trước sửa và lập manifest lượt này. T13 và G3 vẫn ở bước chuẩn bị.
2. Tập ghi: docs/DECISIONS.md, docs/KE-HOACH-SAU-T047.md, docs/KE-HOACH-GIAI-DOAN-TOI.md, SPEC.md và LOG.md của task, results/T-052/ra-soat-ke-hoach-001/SPEC-truoc-sua.md và results/T-052/manifest-ra-soat-ke-hoach-001.json.
3. Kiểm nguồn trước ghi bằng SHA-256 và kích thước theo manifest gốc. Kiểm diff, tiền tố LOG, bản SPEC lịch sử, liên kết, prompt và tập đầu ra. Lượt này kiểm tài liệu.
4. OPEN: parity native C-a, công cụ A4/cohort, hợp đồng RE3 và ETA P7 local. Claude chưa kiểm bản chỉnh. Minh có thể chuyển prompt bên dưới để kiểm độc lập trước khi duyệt quyền triển khai dev.

**Bước tiếp theo:** đọc SPEC bản chỉnh và manifest lượt sửa. Khi có quyền triển khai, ghim nguồn và chuẩn bị công cụ/parity trên dev theo lịch. Quyền máy và pilot trình cùng phạm vi cụ thể.

**Lệnh kiểm chốt hồ sơ:** git diff --check, git diff --no-index giữa bản SPEC lưu và hiện hành, kiểm SHA-256/byte theo manifest lượt sửa.

## Prompt bàn giao Claude kiểm bản chỉnh kế hoạch

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-052 — tasks/T-052-t13-va-ho-so-g3/SPEC.md và bản chỉnh hồ sơ..
- Công đoạn: kiểm lại phản hồi và sửa..
- Gói/cổng: P6, chuẩn bị G3/P7..
- Người làm và người phản biện chính thức: Codex làm, Claude phản biện..
- Tài liệu gốc: AGENTS.md, docs/STATE.md, docs/MRP.md, docs/DECISIONS.md, docs/WHY.md, docs/LESSONS.md, hai kế hoạch được dẫn trong SPEC và bản trước sửa tại results/T-052/ra-soat-ke-hoach-001/SPEC-truoc-sua.md..
- Phản biện và phản hồi trước: tasks/T-052-t13-va-ho-so-g3/LOG.md theo thứ tự thời gian và trao đổi do Minh chuyển nếu có..
- Code và kết quả liên quan: results/T-052/manifest.json, results/T-052/manifest-ra-soat-ke-hoach-001.json, src/m1/, src/m1_danh_gia/, src/p3/ và nguồn ghim trong SPEC..
- Phạm vi ghi được Minh cho phép trong lượt này: Chỉ đọc và trả lời trong chat theo quyền Minh cấp khi chuyển..

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

## Phiên 3 — 04/11/2026 — Codex — laptop Windows — người làm

### Mở phiên và quyền

Minh trả lời “duyệt sửa” sau khi nhận báo cáo và đề xuất đúng ba file. Quyền lượt này là sửa SPEC T-052 ở hai điểm đã trình, nối LOG và tạo `results/T-052/manifest-ra-soat-ke-hoach-002.json` để ghi dấu vết trước/sau. Đây là lượt sửa kế hoạch. Quyền triển khai, G3 và quyền dữ liệu xét riêng.

### Bằng chứng và nội dung sửa

- **Phân loại lỗi trước chấm.** Trong lượt rà chỉ đọc, `m1.chuoi.chay([], [], [], [], {}, 0, {"config_id": "synthetic-bad-runner-params"})` trả `ERROR` vì thiếu `params.bat_tat`. `p3.danh_gia.cham_ca` cho RR = 0 và Hit@5 = 0 nếu đưa bản ghi đó vào chấm. Q-74 và giao thức P3 §8.3 yêu cầu xử lý lỗi dữ liệu/runner trước bảng khoa học. SPEC giờ buộc lớp điều phối phân biệt lỗi vận hành với lỗi phương pháp trên đầu vào hợp lệ trước khi seal để chấm. Giữ biên nhận và phạm vi chạy lại theo quyền. Giữ cách chấm ca lỗi phương pháp và thành viên tập đã duyệt.
- **Đường chạy P7.** Kiểm `p3.selector` trong bộ nhớ cho thấy mã `test-a123456789` bị từ chối, và một mã dev với đường dẫn giả `data/locked/synthetic/metrics.parquet` vẫn bị chặn. `m1.adapter.ca_re2tt` và `p3.runner.chay_luot` gọi bộ chọn này. `p3.nezha.chon_ca` cũng ràng buộc mã và nguồn dev. SPEC giờ giao điểm vào P7 riêng trên local cho M1 và baseline. Trước khi trình khóa G3, fixture phải đi qua đúng bộ chọn/đọc/cắt, kiểm quyền và giới hạn ca, kiểm lỗi, tách nhãn rồi seal trước ghép. Dữ liệu test thật chỉ materialize sau quyền riêng. Bộ chọn dev giữ đúng phạm vi dev.
- Hai sửa được phản ánh trong đầu ra dự kiến, bước thực hiện và tiêu chí xong. Cấu hình khoa học, A4, tập ca G1 và quyết định hoãn (b) giữ theo các quyết định đã ghi. Điểm vào P7 và fixture là nghĩa vụ triển khai, chưa có kết quả trong lượt sửa văn bản.

### Kết thúc lượt ghi

1. Đã sửa SPEC theo hai điểm Minh duyệt và cập nhật bàn giao.
2. Tập ghi gồm SPEC, phần nối thêm LOG và manifest lượt sửa 002. Manifest 001 giữ mốc trước sửa.
3. Tự kiểm các đoạn đổi, các đoạn A4 và giới hạn quyền, tiền tố LOG, ba khối prompt và hash trước/sau. Lệnh cuối của lượt là kiểm SHA-256/byte, đối chiếu diff và tập file.
4. Phần còn mở là công cụ và fixture phân loại lỗi, điểm vào P7, parity C-a, tài nguyên pilot, T13 dev và các điều kiện khóa G3. Lượt sửa này chỉ tháo mâu thuẫn trong kế hoạch. RQ3 vẫn cần bằng chứng ở phạm vi đã ghi.

**Bước tiếp theo:** nếu Minh chuyển Claude, dùng prompt dưới đây để soát bản sửa. Đọc `results/T-052/manifest-ra-soat-ke-hoach-002.json` cùng SPEC. Khi được triển khai, kiểm lại môi trường đã ghim và chạy fixture trước khi đưa bản ghi mới vào chấm. Lượt này chỉ có kiểm tài liệu.

**Nội dung commit đề xuất khi Minh yêu cầu:** `docs(T-052): tách lỗi thực thi và chốt đường chạy P7`.

## Prompt bàn giao Claude kiểm lại bản sửa kế hoạch lượt 002

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-052 — D:/RCA-flashticket/tasks/T-052-t13-va-ho-so-g3/SPEC.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P6, chuẩn bị G3/P7.
- Người làm và người phản biện chính thức: Codex làm, Claude phản biện.
- Tài liệu gốc: docs/STATE.md, docs/MRP.md, docs/DECISIONS.md, docs/WHY.md, docs/LESSONS.md, docs/reference/sources/, tasks/T-052-t13-va-ho-so-g3/SPEC.md và tasks/_MAU/SPEC.md.
- Phản biện và phản hồi trước: tasks/T-052-t13-va-ho-so-g3/LOG.md và lượt Codex do Minh chuyển kèm.
- Code và kết quả liên quan: src/m1/, src/m1_danh_gia/, src/p3/, results/T-022/, results/T-024/, results/T-026/, results/T-034/, results/T-050/, results/T-051/, results/T-053/ và results/T-052/manifest*.json.
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

## Phiên 4 — 04/11/2026 — Codex — laptop Windows — người làm

Minh trả lời “duyệt sửa” cho đúng gói năm file sau báo cáo tự soát. Gồm SPEC, LOG, src/m1/chuoi.py, src/m1/doi_chung.py và manifest lượt 003. Kiểm trong bộ nhớ bằng dữ liệu giả và trung gian dev đã ghim.

- SPEC đặt việc đóng dấu hạng chính trước C-d3. Ghi giới hạn thời gian và trạng thái riêng của C-d3. Giữ nền, A4, cohort và hoãn (b).
- `chuoi.chay` nhận `params.tach_cd3=True`. Lượt xếp hạng trả hạng và đầu vào phi nhãn để chạy C-d3 riêng. Điểm giữ chính xác dưới dạng cặp tử/mẫu. Mặc định vẫn trả đối chứng như trước.
- C-d3 tính tổng điểm đường lớn nhất theo thứ tự topo ngược trên đồ thị con bất thường. Giữ điều kiện chu trình, thiếu đích, khóa hòa và yêu cầu đi qua ít nhất một cạnh.

### Kiểm và kết thúc lượt sửa

- Đối chiếu mã tại HEAD trên 5.000 đồ thị giả, seed 5203, không lệch. Đồ thị 30 lớp với trung gian không cờ cho NO_EVIDENCE. Cùng đồ thị với mọi nút có cờ cho điểm 32.
- Tiêm lỗi riêng C-d3 ở M1, C-a0, C-a1. Chế độ tách không gọi C-d3 và vẫn trả cùng bản ghi. Giải mã JSON bằng Fraction rồi ghép C-d3 riêng khớp bản mặc định. Kiểu tham số sai bị từ chối.
- Kiểm hash/byte 82 cửa sổ native từ seal T-053, dùng 246 bản ghi K-R0, K-E1 và K-E1+E2+E5. Mã cũ và mới khớp trên đầu vào dựng từ trung gian đã lưu. Trạng thái và nhóm hạng cũng khớp bản ghi lịch sử. Đây chưa là kiểm tương đương C-a trực tiếp từ dữ liệu thô.
- Gói sửa đủ năm file đã duyệt. Chưa chạy pilot dev, chưa dùng EC2 hay mở G3/test/RE3. Chưa commit/push. Bước điều phối P7 và phép kiểm từ đầu tới cuối vẫn thuộc triển khai.
- Bước kế là Claude kiểm độc lập theo prompt bên dưới nếu Minh chuyển. Khi tiếp tục triển khai, đặt `params.tach_cd3=True` ở đường chạy T-052/P7, kiểm điều phối và đóng dấu trước pilot.

Lệnh cuối lượt: kiểm SHA-256/byte theo manifest 003 và `git --no-optional-locks diff --check`. Lệnh tái lập đối chiếu nằm trong manifest.

Commit đề xuất khi Minh yêu cầu: `fix(m1): tách C-d3 khỏi lượt xếp hạng T-052 và P7`.

### Prompt bàn giao Claude kiểm lại bản sửa

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-052 — tasks/T-052-t13-va-ho-so-g3/SPEC.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P6, chuẩn bị G3/P7.
- Người làm và người phản biện chính thức: Codex làm, Claude phản biện.
- Tài liệu gốc: docs/STATE.md, docs/MRP.md, docs/DECISIONS.md, docs/WHY.md, SPEC T-043, SPEC T-052.
- Phản biện và phản hồi trước: tasks/T-052-t13-va-ho-so-g3/LOG.md theo thứ tự các mục.
- Code và kết quả liên quan: src/m1/chuoi.py, src/m1/doi_chung.py, results/T-052/manifest-ra-soat-ke-hoach-003.json và nguồn ghim trong đó.
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

## Phiên 5 — 04/11/2026 — Codex — laptop Windows — người làm

### Quyền của Minh trong phiên — nguyên văn

Minh giao thực hiện đề bài đính kèm và nói: “không cần chờ claude bạn sửa lại cho tôi phần đấy, bám theo yêu cầu của tôi , thực hiện theo nhiệm vụ trong yêu cầu của tôi”. Claude vẫn là người phản biện chính thức. Không coi việc không chờ Claude là nghiệm thu hoặc đổi vai.

## 3. Quyền triển khai có điều kiện do Minh cấp

Sau tự soát và đối chiếu:

### Nếu có lỗi nghiêm trọng hoặc điểm CHẶN

Dừng trước khi sửa file hoặc chạy thực nghiệm. Trình:
- Nguồn và bằng chứng.
- Kết luận hoặc quyết định bị chặn.
- Hậu quả nếu tiếp tục.
- Đề xuất sửa cụ thể theo file và tác động.
- Những phần có thể làm được nhưng còn phụ thuộc quyết định nào.

Lỗi ảnh hưởng thiết kế, giao thức, lựa chọn dữ liệu, nhãn, công thức, tập ứng viên, độ công bằng so sánh, tiêu chí chấm, thống kê, quyền hoặc phạm vi kết luận là lỗi thực chất. Không hạ thành “lỗi nhỏ” chỉ vì sửa ít dòng.

### Nếu không còn lỗi nghiêm trọng hoặc điểm CHẶN

Tôi cho phép triển khai T-052 theo SPEC hiện hành và phạm vi được quy định trong đó.

Cho phép sửa ngay lỗi nhỏ về câu từ, diễn đạt, lỗi gõ hoặc liên kết khi ý nghĩa khoa học, quyền và tiêu chí không đổi. Trước sửa, tự kiểm đoạn cũ và nguồn để bảo đảm đó thực sự chỉ là sửa diễn đạt. Ghi rõ từng sửa trong LOG. Nếu cần thay ý nghĩa hoặc cách làm, dừng phần phụ thuộc và trình tôi.

Phạm vi được phép:
- SPEC T-052, chỉ cho các sửa nhỏ nêu trên.
- LOG của T-052.
- results/T-052/ và công cụ/đầu ra mà SPEC cho phép.
- Đúng dòng T-052 trong docs/STATE.md.
- Làm mới manifest hồ sơ liên quan để phản ánh đúng các file được phép sửa, giữ dấu vết trước/sau và các lượt thực thi.

Đầu phiên triển khai, ghi nguyên văn quyền có điều kiện này và kết quả tự soát vào LOG. Không coi việc bắt đầu chạy là nghiệm thu task hoặc duyệt G3.

Quyền chạy ban đầu theo ngân sách SPEC: pilot và chấm dev từ nguồn đã ghim, tối đa 60 phút máy, sau khi tài nguyên sẵn sàng. Được dùng EC2 hiện có khi Minh đã bật và có quyền truy cập theo quy định repo. Quyền này không bao gồm tự tạo/bật máy mới, mở dữ liệu khóa, chạy native diện rộng hoặc vượt ngân sách. Nếu dự báo cần vượt, trình phần thiếu, dự toán và trần trước khi chạy.

Giữ quyết định hoãn chế độ (b) và mọi lựa chọn đã duyệt. Chưa được mở G3/test/RE3, sửa src ngoài phạm vi đã duyệt, commit hoặc push.


### Tự soát trước triển khai

Thứ tự đã xảy ra: lượt khởi động trước khi nhận tệp yêu cầu đã đọc SPEC T-052 và mục cuối LOG. Vì vậy đây không phải đánh giá mù. Lượt này đọc nguồn DT18/cô, MRP, quyết định/lý do/bài học và kế hoạch, code lõi, bàn giao P5/T-041, chuỗi kết quả M1; lập nhận xét trong bộ nhớ; sau đó mới đọc lại SPEC/mẫu và các phản biện/phản hồi trước.

Nhận xét ban đầu: cần T13 đủ baseline/đối chứng, ablation cùng nền, nhóm/ca, vùng theo O và C-e; phải chứng minh tái dùng từng trường và C-a native, khóa A4 và đường vào P7 trước G3. Dev đã chọn lặp, E2 đánh đổi giữa dataset, R0 thắng M1 trên TT, C-d2 hơn M1 OB. Không có nhãn vùng ảnh hưởng, không có nền lành độc lập để hiệu chuẩn verdict. VC×E5, log–span, chiều PageRank đảo và revision snapshot chưa phân xử; không tự chạy thêm để đóng chúng.

Đã kiểm trực tiếp 29 đầu vào của manifest hồ sơ, 13 manifest upstream và 5 nguồn G1, không lệch byte/hash. Các trạng thái “trước sửa” không được dùng làm hash hiện hành. Bốn đầu ra manifest sửa 003 khớp. Code C-a tắt E2/E5/E7 theo đúng hợp đồng, nhưng projection vẫn cần pilot native. Kiểm trong bộ nhớ: tiêm lỗi C-d3 không làm lỗi M1/C-a0/C-a1 khi tach_cd3=True, ba vế PASS. Môi trường local import numpy/pandas/pyarrow/scipy/networkx/psutil được; đĩa D khoảng 17,2 GB, RAM khả dụng 3,27 GB tại lúc kiểm.

Đối chiếu SPEC: giữ nền, ma trận, cohort, A4 và giới hạn kết luận. Không phát hiện điểm CHẶN triển khai kế hoạch hiện hành; những phép chưa có trong SPEC là nghĩa vụ sắp thực hiện, chưa được gọi là đã đạt. Tám ý Claude ở nguồn chat đã được phản ánh vào kế hoạch; nhận định cận 14% không dùng như cận hiệu ứng/power. Không có sửa nhỏ SPEC trong lượt bắt đầu. Quyền chạy đã được Minh cấp trực tiếp ở đề bài mới, dù các dòng quyền lịch sử ghi “trình riêng”.

### Bắt đầu thực hiện

Phạm vi đúng đề bài: LOG; results/T-052/ và scripts/runs; đúng dòng T-052 STATE. SPEC chỉ sửa nhỏ nếu cần, hiện giữ nguyên. Không sửa src/sổ quyết định, không mở locked/RE3, không commit/push. Ngân sách chạy pilot/chấm tối đa 60 phút máy; tính riêng thời gian làm công cụ, đọc nguồn và hồ sơ. Lượt thực thi đầu: runs/trien-khai-001; giữ mọi lỗi và tiến độ ngay từ đầu.

- EC2: thử SSH read-only tới địa chỉ trong data/README với BatchMode/host-key strict/timeout 8 giây; hết thời gian, chưa xác nhận máy bật, không khởi động máy. Dùng local cho pilot/compact.
- Bộ đọc T-051 từ chối hash src cũ. Đã đối chiếu đúng Git blob và biểu diễn CRLF của chuoi.py; hai thay đổi src thuộc manifest sửa 003. Wrapper T-052 kiểm lineage trước/sau, không sửa hoặc bỏ hash manifest lịch sử.
- Pilot-001 dừng trước gọi phương pháp: wrapper đã gộp params_ca hai lần, runner từ chối khóa trùng. Phân loại EXECUTION_CONFIG_ERROR, không đưa vào bảng khoa học. Giữ failure.json/plan/progress và bản runner trước sửa. Sửa wrapper để chỉ ghép params_ca một lần; chạy pilot-002, không sửa src/hợp đồng.

- Pilot-002: phương pháp đã trả bản ghi hợp lệ nhưng lưu trace thất bại vì trace có set, trong khi bộ ghi mới chưa chuẩn hóa set. Phân loại OUTPUT_SERIALIZATION_ERROR, không chấm. Giữ failure/runner trước sửa. Lượt 003 dùng đúng bộ chuẩn hóa trace của công cụ nguồn và lưu record JSON riêng trước trace để không làm mất hạng nếu lưu trung gian lỗi. Hai lỗi thuộc wrapper mới, không phải bằng chứng phương pháp hỏng.

- Minh cung cấp IP EC2 3.107.156.186 và cho chỉnh quyền khóa nếu cần. Đã kết nối bằng key2.pem đúng T-053, không cần đổi ACL. Máy còn khoảng 7,1 GB RAM và 14 GB đĩa. Chuyển đường pilot sang EC2 sau khi dừng ba lượt local; chọn 0,1,53,62,79 có nguồn K cũ cũng trên EC2, giữ phép so chính xác, không nới dung sai. Bundle chỉ code/metadata/đầu ra dev đã ghim, không truyền raw/locked. SSH điều khiển launch hết 20 giây; giữ biên nhận và dùng kết nối mới kiểm tiến trình trước mọi tiếp nhận, không chạy trùng.

### Checkpoint sau nén ngữ cảnh — 2026-11-04T12:31:55.240709+00:00

Pilot EC2-002 đã PASS 15/15; TT local sáu baseline PASS; OB-local-002 PASS M1/T12 và sáu tuyến baseline. Đã chiếu/kiểm 82 cửa sổ, seal 492 bản ghi gọn, chấm đủ T13 dev; chưa chạy P7/test. Kết quả hiện hành: results/T-052/ket-qua-dev.json, vung-ce-va-vi-tri-001.json. Đã tạo bao-cao-t13.md, ho-so-g3.md, ma-tran-va-nguon.json, ke-hoach-tap-test.json, giao-thuc-p7-a.json. SPEC/src giữ nguyên từ đầu phiên. Các lượt hỏng giữ nguyên dưới runs/trien-khai-001. Chưa đổi STATE hoặc tạo manifest thực thi cuối.

Còn đúng phần chốt: kiểm báo cáo và hash/phạm vi, nối kết thúc phiên và prompt mẫu, đổi một dòng T-052 STATE, tạo manifest thực thi và biên nhận kiểm cuối. Không chạy thêm nghiên cứu. Nếu cần tiếp tục sau phiên này, mở phiên mới đọc AGENTS/STATE/SPEC và mục cuối LOG, không chạy lại đầu ra hợp lệ. Lệnh cuối đã chạy: đọc LOG, bao-cao-t13.md, docs/review-prompt.md và tìm dòng T-052 STATE (chỉ đọc).

### Kết thúc Phiên 5 — tự soát, triển khai T13 dev và hồ sơ G3(a)

1. **Đã làm:** tự soát từ nguồn, đối chiếu SPEC rồi kết quả/phản biện cũ; không phải lượt mù vì đã thấy SPEC/LOG ở lượt trước. Giữ nền/câu hỏi nguồn, không sửa nhỏ SPEC. Sau quyền có điều kiện của Minh, đã triển khai pilot native EC2 15/15; TT local sáu baseline; OB local M1/T12/sáu tuyến; TORAI worker mới so raw với tuyến cũ; seal 492 bản ghi từ 82 cửa sổ và kiểm 328 compact KB; chấm đủ T13 dev, 52 graph-control, nhóm/ca, vùng/C-e. Không chạy native toàn ma trận.
2. **File:** thêm scripts/runs và kết quả/hồ sơ trong results/T-052/, nối LOG này, đổi đúng một dòng T-052 STATE. Hai file src và các sổ có thay đổi từ trước phiên được giữ nguyên theo dấu vân tay lúc nhận việc. Không sửa SPEC/src, không ghi DECISIONS/WHY, không mở locked/RE3, không commit/push/cấp máy/đổi ACL khóa.
3. **Kiểm:** hash 29 đầu vào, 13 manifest upstream, 5 nguồn G1 và lineage 003; input/sample/native parity; chấm lại 372 bản ghi baseline; 16 fixture A4, 21 kiểm điểm vào P7 dữ liệu giả; C-d3 thật/error/timeout/JSON hỏng giữ seal chính. Bổ sung Retrieval/Rerank theo evaluator và bảng native RCAEval baseline tách kỳ vọng hòa. Cột Rerank mẫu số0 ghi null. Đã kiểm JSON, compile công cụ, số/mẫu số/trạng thái và dấu vân tay protected. Biên nhận kiểm và thời gian: runs/trien-khai-001/{final-checks,machine-budget}.json; manifest-thuc-thi-001.json ghim file cuối.
4. **Kết luận/phần mở:** T13 đạt mô tả dev và hồ sơ để Minh xem, không nghiệm thu thay Minh hoặc khóa G3. M1−C-a0 âm TT/dương OB; C-d2 hơn M1 OB, không xác nhận lợi ích đồ thị chung. Chuỗi E2/E5 có bằng chứng tính toán và phản ví dụ, không chứng minh lỗi vật lý hoặc cơ chế chung. E5 thiếu matched control đầy đủ; VC×E5, chiều PageRank đảo, log–span, revision snapshot và nền lành độc lập giữ OPEN. RQ3a/(b), nhãn vùng/P10, LLM/P8 và FlashTicket/P9/P10 chưa được task này trả lời. Quyết định nền hiện hành không đổi. Minh còn quyết phản biện/nghiệm thu, khóa G3, ma trận/worker/timeout/tổng ngân sách và private map trong SPEC P7, quyền dữ liệu; RE3 cần hợp đồng nguồn/U/adapter/schema và quyền riêng trước một lượt mở cuối. Không chạy thêm để tự đóng các câu này.

**Lỗi và cách xử lý:** giữ local001 lỗi gộp params, local002 lưu set, local003 lệch số thực cực nhỏ; không nới comparator, chuyển sang nguồn EC2 cùng nền số và đạt exact. EC2-001 thiếu module observer, SSH điều khiển hết giờ; kiểm worker qua kết nối mới trước nhận, giữ lỗi. EC2-002 thêm đúng phụ thuộc và launch tách PID/timeout, PASS. Một lỗi bookkeeping khi thêm vế chấm giữ script cũ/failure rồi sửa wrapper. OB-local001 thiếu thư mục log, giữ record/failure; hash snapshot bổ sung sau đọc được ghi rõ hậu kiểm. OB-local002 kiểm trước, lưu timing từng bước, PASS. Không gọi lỗi công cụ là lỗi khoa học của phương pháp. Mỗi lỗi thuộc wrapper khác nhau; không thử cùng một lỗi quá ba lần.

**Chi phí:** machine-budget.json ghi tầng đo thời gian và cận trên riêng cho pha hỏng, gồm khoảng chờ nên cố ý đếm dư, vẫn dưới 60 phút ngân sách thực nghiệm. Không thay mốc chưa ghi bằng số thời gian chính xác giả. Chi phí đọc nguồn/làm công cụ/viết hồ sơ tách riêng. Pilot local là lát cắt, không là trần thời gian toàn test.

**Đầu ra chính:** bao-cao-t13.md (tự đánh giá, đối chiếu, thực thi, cơ chế, kết quả, giới hạn, chi phí, phần mở); ho-so-g3.md; ket-qua-dev.json; do-do-bo-sung.json; vung-ce-va-vi-tri-001.json; ma-tran-va-nguon.json; ke-hoach-tap-test.json; giao-thuc-p7-a.json. Bản độc lập trước C-a parity giữ nhãn PARTIAL lịch sử, không là kết quả hiện hành. Giao thức là ứng viên để Minh khóa, không phải giấy phép mở test.

**Nội dung cần ghi sổ sau khi Minh duyệt:** quyền tự soát/triển khai có điều kiện và quyền dùng EC2 hiện có do Minh cấp. Đề xuất dòng ghi ở ho-so-g3.md, chưa tự ghi ngoài phạm vi. Không thay quyết định phương pháp.

**Bước kế tiếp chính xác:** dùng môi trường Python ở lệnh dưới kiểm manifest chỉ đọc; đọc bao-cao-t13.md, ho-so-g3.md và giao-thuc-p7-a.json. Minh có thể copy prompt bên dưới cho Claude; không tự gửi, không chờ Claude để làm phần đã được giao. Khi Minh duyệt G3/quyền chạy, mới trình SPEC P7 đầy đủ ma trận và trần, không dùng task này tự mở test. Do ngữ cảnh đã nén, công việc mới nên mở phiên mới theo AGENTS 5a.2, không chạy lại đầu ra hợp lệ.

Lệnh chốt phiên đang chạy: `& 'C:/Users/84583/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B -S results/T-052/scripts/finalize.py`.
Lệnh kiểm cuối phải chạy ngay sau chốt (chỉ đọc): `& 'C:/Users/84583/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B -S results/T-052/scripts/finalize.py --verify`.
Commit đề xuất, chưa thực hiện: `feat(T-052): hoàn tất T13 dev và hồ sơ chuẩn bị G3(a)`.

### Prompt bàn giao Claude — soát kết quả/G3

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-052, tasks/T-052-t13-va-ho-so-g3/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P6/P7, G3(a).
- Người làm và người phản biện chính thức: Codex người làm, Claude người phản biện.
- Tài liệu gốc: AGENTS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/KE-HOACH-SAU-T047.md; tasks/T-052-t13-va-ho-so-g3/SPEC.md.
- Phản biện và phản hồi trước: tasks/T-052-t13-va-ho-so-g3/LOG.md theo thứ tự thời gian; results/T-052/manifest.json phần review_received; chưa có file REVIEW của task.
- Code và kết quả liên quan: src/m1/; src/m1_danh_gia/; src/p3/; results/T-052/manifest-thuc-thi-001.json; results/T-052/scripts/; results/T-052/runs/; kết quả và nguồn được dẫn trong manifest; lệnh kiểm chỉ đọc: python -B -S results/T-052/scripts/finalize.py --verify theo môi trường ghi trong LOG.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; chỉ ghi bản phản biện khi Minh cấp rõ đường dẫn cho lượt này.

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

## Phiên 6 — 04/11/2026 20:01 +0700 — Codex — Windows — người làm đáp phản biện

### Quyết định của Minh trong phiên

Minh gửi tệp phản biện và giao: “nếu không có mâu thuẫn nào với claude hoặc phản đối nào thì cho phép ghi luôn , nếu có mâu thuẫn thì soạn trình claude phản biện”. Hiểu là quyền có điều kiện đối với gói sửa cụ thể được thống nhất sau kiểm; không là nghiệm thu T-052, khóa G3, mở dữ liệu hoặc commit/push. Claude giữ vai trò người phản biện. Trước khi đọc kết luận tệp mới, tự kiểm đầu ra/code dưới đây; chưa sửa đầu ra nghiên cứu.

### Tự soát trước khi đọc phản biện mới

- Đã đọc AGENTS, STATE, tiêu chí/phạm vi SPEC, cuối LOG; đối chiếu code score_all/thong_ke/p7_entry. Manifest thực thi 001 vừa kiểm PASS cả 392 file, phần đầu LOG, src/SPEC và đúng dòng STATE. Chưa có REVIEW.md trong thư mục task. Không lặp pilot/native đã hợp lệ.
- Bảng dev có đủ vế theo phạm vi world; số/mẫu số và dấu cặp đã được kiểm trong finalize --verify. Bằng chứng đang có là mô tả dev đã chọn lặp, không xác nhận lợi ích đồ thị chung hoặc nguyên nhân vật lý. Không dùng hơn baseline để thay câu hỏi đối chứng.
- Giao thức vẫn ở trạng thái ứng viên: ma trận materialize, vị trí private map và tổng ngân sách/worker/timeout P7 chưa khóa. Đây là phụ thuộc G3/P7 cần chốt, không tự coi đồng thuận reviewer là quyền mở test. Mã có đường đọc/cắt và cô lập C-d3; fixture không thay phép kiểm khoa học toàn test.
- Tự soát hiện chưa xác nhận lỗi số mới. Giới hạn cơ chế E5/VC×E5, log–span, revision snapshot và nền lành giữ OPEN như nguồn; không gọi chúng đã giải quyết chỉ vì kiểm hash/fixture PASS. Kế tiếp đọc nguyên văn tệp Minh chuyển, kiểm từng finding cả phần có thể bác bỏ, rồi mới kết luận quyền sửa có thỏa không.

Lệnh cuối trước khi mở tệp phản biện: finalize.py --verify và đọc code gốc score_all.py, thong_ke.py, p7_entry.py (chỉ đọc). Chưa đọc kết luận phản biện mới khi ghi mục này.

### Đối chiếu phản biện Minh chuyển — F1–F7

Nguồn: tệp “Pasted text.txt” tại đường dẫn đính kèm của Minh, được ghim trong manifest-dap-phan-bien-001.json. Đây là phản biện Claude ở nguồn chat do Minh chuyển; không tạo REVIEW.md hoặc đứng tên Claude. Mục tự soát phía trên được ghi trước khi mở kết luận của tệp này.

| Ý | Kết luận của người làm | Bằng chứng kiểm trực tiếp và hệ quả | Minh quyết |
|---|---|---|---|
| F1 — thiếu chuỗi cơ chế/ca đối chiếu | Đúng — CHẶN nghiệm thu phần phân tích và hồ sơ G3 liên quan | Tính lại từ ket-qua-dev: 38 vết delta_RR dương đều thiếu đối chiếu; 9 vết có ca cùng root/fault mà M1 không hơn. Code chỉ chọn đối chiếu khi delta<0. OB C-a0 có 6 network_delay tăng với tổng chênh 3,938576; OB bỏ E2 có 5 network_delay tăng tổng3,304171. TT hại C-a0 tập trung loss/mem, bỏ E2 chỉ đổi ở loss. Frame E2 nguồn T-053 đã kiểm hash xác nhận còn order tăng86,209133→4708,986842 ngoài train4834,194981, nên kể một đối thủ chưa giải thích đủ RR1→1/3. Cần đọc cả OB giúp, E1, C-d2 thắng và vùng đổi, không chỉ hai ví dụ TT. | |
| F2 — chính sách đường dẫn và thành viên P7 | Đúng — CHẶN khóa code/nhánh OB | p7_entry.select giới hạn root thật dưới data/locked; src/p3/nezha.DATA_PREFIX và data/README đặt OB dưới data/ngoai-rcaeval. Kiểm bằng metadata fixture với policy thật và chặn Path.open: gốc repo bị từ chối trước mở payload. member_sha256 được so với members_locked trong cùng manifest, chưa đối chiếu kế hoạch G1 bên ngoài đã ghim. Mở root repo đơn thuần không đủ; cần ràng buộc cả thành viên, tập file/hash và thời gian/cửa sổ khi dữ liệu dùng chung file. Không đọc test để xác nhận điểm này. | |
| F3 — chưa kiểm tuyến baseline thật của entry | Đúng — CHẶN khóa tuyến và A4 phụ thuộc | Hai pilot trước gọi p3.runner/chay_tien_trinh và p3.nezha_worker; fixture_p7 trả spies trước phần adapter thật. entry.baseline còn chạy trực tiếp năm baseline trong tiến trình chính, thiếu cưỡng chế môi trường/hashseed/timeout và lớp bản ghi như runner. TORAI có process riêng nhưng chuẩn bị còn ở tiến trình chính. Chưa chạy thêm dev trong lượt đáp có bất đồng. Chưa tái lập mọi trạng thái fixture Claude đã chạy; việc thiếu kiểm qua đúng tuyến được xác nhận bằng code/receipt, không suy rằng mọi baseline đã sai số. | |
| F4 — thiếu mục khóa/giao thức | Đúng phần thiếu, phản đối một phần đề nghị về quyền — CHẶN G3 vẫn giữ | Giao thức thiếu nội dung/trỏ chính xác cho diễn giải, tiếp xúc, định nghĩa vị trí N, snapshot/đường cấp cạnh tĩnh, C-e thiếu lịch sử, phép phụ và fixture liên quan, pin phụ thuộc đệ quy/env/revision, kiểm fingerprint theo từng vế. Riêng việc báo thêm bản loại ca lỗi đã được quyết ở Q-211(6) và vẫn ghi rõ WHY-06. Không coi sự tồn tại của bản này là một lựa chọn mới chưa được duyệt; chi tiết cách loại và ghép cặp/seed vẫn cần chốt trước G3. Bất đồng cụ thể trình ngay dưới bảng. | |
| F5 — căn cứ E1 một phía | Đúng — KHÔNG CHẶN riêng | C-a1−C-a0 TT=0, OB≈−0,030716. Tác dụng E1 phụ thuộc nền E2/E5. M1−bỏ E1 TT có 4 ca loss và 1 socket tăng; “tập trung loss” không đồng nghĩa chỉ có loss. Cần đưa bằng chứng trái chiều vào bảng căn cứ. | |
| F6 — dòng C-d3 thiếu trạng thái | Đúng — KHÔNG CHẶN riêng | JSON tại worlds/P/.../summary/C-d3/status có TT4 OK/6 NO_EVIDENCE/20 UNSUPPORTED_CYCLIC, OB22 NO_TARGET. Bảng Markdown chỉ hiện0 nên chưa chuyển tải đúng điều kiện hỗ trợ. Cần ghi trạng thái và mẫu số ngay cạnh số. | |
| F7 — câu thứ tự ghép nhãn | Đúng — KHÔNG CHẶN riêng | Biên nhận bản độc lập18:33, vùng18:35, prepared-seal18:55 giờ Việt Nam. Hai lượt đầu dùng output đã seal ở task nguồn, không phụ thuộc prepared-seal T-052. Code bang_doc_lap/vung_ce xác nhận tái dùng nguồn. Câu “chỉ sau đó” trong báo cáo đã kể sai trình tự, không là bằng chứng nhãn lọt vào phương pháp. Cần mô tả riêng seal nguồn và seal chuẩn hóa T-052. | |

**Làm rõ thuật ngữ trong F1:** tính trên toàn bộ M1_root_channels/kenh_co đã lưu thì 5/6 ca OB bỏ E2 chỉ còn kênh E2; nếu chỉ lọc F_I=1 thì cả6/6. Ở dev-5467884de4 còn ba kênh NetworkReceiveBytes/SyscallRead/SyscallWrite với F_I=0. Không dùng sự khác nhau giữa kênh có cờ đầu vào và kênh tự sinh sau phân lớp để bác số5/6 của Claude hoặc xác nhận cơ chế vật lý.

### Bất đồng cần Claude kiểm lại — sự tồn tại của bản loại ca lỗi

- Claude viết trong F4: “Riêng bản loại ca lỗi cần Minh quyết giữ hay bỏ.”
- Q-211 mục6 trong docs/DECISIONS.md đã duyệt: “ca lỗi tính là trượt, báo thêm bản loại ca lỗi”.
- Q-246 thay các phần A4 được nêu cụ thể, không xóa mục6. Quan trọng hơn, WHY-06 hiện hành vẫn ghi nguyên tắc: “Ca lỗi tính là trượt; báo thêm bản loại ca lỗi để xem độ nhạy.”
- Tôi đồng ý đầu ra T-052 thiếu phần này. Tôi không đồng ý chuyển một nghĩa vụ hiện hành thành OPEN về có/không chỉ vì SPEC/giao thức đã bỏ sót. Việc đó làm sai trạng thái quyết định và có thể khiến mất phép nhạy trước khóa.
- Đề nghị đối chiếu: nếu Claude chỉ muốn Minh chốt **quy tắc loại lỗi, giữ cặp và gộp seed**, thì không có phản đối về nhu cầu cụ thể hóa. Nếu muốn Minh quyết lại **có hay không báo bản nhạy**, cần chỉ ra quyết định nào đã hủy yêu cầu cũ. Chưa có nguồn hủy thì giữ yêu cầu hiện hành; muốn bỏ là một thay đổi cần Minh quyết riêng.
- Bất đồng này không bác F1–F3 hoặc phần thiếu còn lại của F4. T-052 chưa đủ nghiệm thu và G3 chưa đủ khóa. Không lấy đồng thuận về số liệu để suy đủ căn cứ khóa.

### Gói sửa dự kiến sau khi phân xử, chưa thực hiện trong lượt này

| Phạm vi | Việc sửa và vì sao | Tác động |
|---|---|---|
| results/T-052/scripts/score_all.py hoặc công cụ phân tích bổ sung; kết quả truy vết mới; bao-cao-t13.md | Đối chiếu hai chiều, chuỗi đầy đủ TT hại/OB giúp/E1/C-d2/vùng và đọc theo fault/vị trí; giữ số hạng gốc, tách phần chưa phân xử | Đáp F1, không chọn lại nền từ dev |
| results/T-052/scripts/p7_entry.py và fixture/worker task liên quan | Chính sách nguồn theo dataset + đối chiếu cohort ngoài manifest tự tham chiếu; fingerprint theo vế được phép; dùng lớp process/env/timeout/bản ghi đã kiểm của runner; đường T12/C-e theo hợp đồng | Đáp F2/F3 và phần code F4; không sửa src hoặc dùng test để hoàn thiện |
| results/T-052/giao-thuc-p7-a.json, ke-hoach-tap-test.json, ma-tran-va-nguon.json, ho-so-g3.md; scripts/thong_ke.py/fixture và công cụ sinh hồ sơ | Bổ sung nội dung và con trỏ còn thiếu, toàn bộ phụ thuộc/env/revision; tiếp xúc và định nghĩa; các phép phụ/fixture; phục hồi bản nhạy loại lỗi theo nguồn sau phân xử phạm vi | Đáp F4/F5; không tự khóa G3 hay materialize dữ liệu test |
| results/T-052/bao-cao-t13.md và công cụ sinh | Hiện trạng thái C-d3, sửa câu chronology/seal nguồn và seal chuẩn hóa | Đáp F6/F7, không đổi điểm phương pháp |
| LOG, đúng dòng STATE và manifest mới | Ghi quyền, từng sửa, phép kiểm, thời gian và bàn giao; giữ lịch sử | Không ghi thay REVIEW, không commit/push |

Phần F1 và đa số hồ sơ dùng trung gian đã có. F3 dự toán Claude khoảng2,5 phút máy cho một ca TT và một ca OB, chưa là cận cho toàn gói sửa; khi triển khai phải khai vế/seed/timeout và tính vào ngân sách được phép, giữ mọi lượt hỏng. Lượt đáp này không chạy lại phương pháp hoặc mở dữ liệu khóa. Vì còn bất đồng ở trên, theo đúng điều kiện Minh giao, chưa thực hiện gói sửa F1–F7.

### Kết thúc lượt đáp — bốn mục

1. **Đã làm:** tự soát trước phản biện, kiểm từng finding, chấp nhận các thiếu sót khoa học/triển khai chính; nêu riêng bất đồng về nguồn quyết định bản loại ca lỗi. Đính chính lời báo trước của Codex “đã xong phần người làm”: hoàn tất bảng dev không đồng nghĩa đạt tiêu chí phân tích và điểm vào P7; F1–F4 còn chặn.
2. **File thay đổi:** chỉ nối LOG này, đổi đúng dòng T-052 trong STATE sang đang đáp phản biện/chưa đủ nghiệm thu, tạo results/T-052/manifest-dap-phan-bien-001.json. Không sửa đầu ra nghiên cứu, code, SPEC, DECISIONS hoặc WHY; không tạo REVIEW đứng tên Claude.
3. **Kiểm:** trước nối LOG, finalize --verify PASS392 đầu ra. Sau nối, kiểm lại mọi output001 trừ LOG (thay đổi được phép), phần LOG cũ khớp nguyên prefix. Tính lại38/9 vết, nhóm lỗi, cặp E1 và trạng thái C-d3; frame E2 khớp manifest T-053; kiểm policy gốc repo bằng metadata giả với mở payload bị chặn. Một lệnh tra frame ban đầu dùng JSON pointer như một khóa đã KeyError, được sửa thành truy cập hai tầng chỉ đọc. Không có lượt chạy khoa học mới.
4. **Phần mở:** cần Claude đối chiếu bất đồng nguồn đã nêu; F1–F4 chưa sửa; task và G3 giữ mở. RQ3b/d mới có kết quả dev; cơ chế, hiệu quả độc lập, vùng ảnh hưởng/P-R-F1 và các phần hoãn vẫn chưa được trả lời đầy đủ. Đề xuất tiếp tục đúng một lượt kiểm bản đáp, không tự áp số vòng lên các lượt sau. Minh chọn chuyển prompt; agent không tự gửi.

**Bước tiếp chính xác:** Minh copy prompt bên dưới cho Claude ở chế độ chỉ đọc. Claude đọc nguồn/đầu ra trước rồi kiểm bản đáp này; khi không còn bất đồng, áp quyền có điều kiện của Minh vào đúng gói sửa đã thống nhất. Chưa chạy P7 hoặc mở test/RE3. Trước dùng lại output, kiểm manifest-dap-phan-bien-001.json hiện hành, không coi việc manifest001 cũ lệch LOG/STATE sau nối được phép là lệch kết quả khoa học.

Lệnh cuối của lượt ghi: Python chỉ ghi LOG, một dòng STATE và manifest bàn giao hiện hành. Lệnh kiểm cuối dự kiến (chỉ đọc): tải manifest-dap-phan-bien-001.json, kiểm byte/hash từng outputs, đối chiếu LOG prefix và đúng một dòng STATE thay từ bản001; git diff --check.
Commit đề xuất cho gói bàn giao khi Minh yêu cầu, chưa commit/push: `docs(T-052): đáp phản biện và ghi bất đồng nguồn giao thức`.

### Prompt Claude — kiểm lại bản đáp

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-052, tasks/T-052-t13-va-ho-so-g3/SPEC.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P6/P7, G3(a).
- Người làm và người phản biện chính thức: Codex người làm, Claude người phản biện.
- Tài liệu gốc: AGENTS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; tasks/T-052-t13-va-ho-so-g3/SPEC.md.
- Phản biện và phản hồi trước: C:/Users/84583/.codex/attachments/a601dd5a-67c9-473d-b423-d1644102fc56/Pasted text.txt (bản Minh chuyển); tasks/T-052-t13-va-ho-so-g3/LOG.md theo thứ tự thời gian; chưa có REVIEW.md trong thư mục task.
- Code và kết quả liên quan: src/m1/; src/m1_danh_gia/; src/p3/; results/T-052/scripts/; results/T-052/ket-qua-dev.json; results/T-052/bao-cao-t13.md; results/T-052/ho-so-g3.md; results/T-052/giao-thuc-p7-a.json; results/T-052/manifest-thuc-thi-001.json (lịch sử); results/T-052/manifest-dap-phan-bien-001.json (bàn giao hiện hành); nguồn và biên nhận được dẫn trong các manifest.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; không sửa kết quả, LOG, STATE hoặc tự tạo bản phản biện khi Minh chưa cấp rõ đường dẫn cho lượt này.

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

## Phiên 7 — 04/11/2026 — Codex — Windows — người làm

Minh giao: “nếu không có mâu thuẫn nào với claude hoặc phản đối nào thì cho phép ghi luôn , nếu có mâu thuẫn thì soạn trình claude phản biện, các phần đề xuất của 2 bên nếu đã thống nhất thì duyệt ghi”. Claude rút bất đồng F4 về bản loại ca lỗi và không phản đối gói sửa F1–F7. Kiểm đầu lượt: manifest đáp 001 khớp 393/393. Đã đọc lại nguồn, SPEC, bảng dev, thiết kế điểm vào và bản đáp. F8/F9 được kiểm độc lập dưới đây. Lượt này ghi bản sửa mới trong results/T-052, giữ đầu ra cũ và chỉ cập nhật LOG/dòng T-052. Quyền ghi và fixture giả không suy thành quyền pilot baseline thật F3, khóa G3 hay mở test. Chính sách chi tiết bản loại ca lỗi được trình như ứng viên.

Tác động gói sửa: F1/F8 tính từ kết quả dev đã seal, không chạy phương pháp; F5–F7/F9 sửa báo cáo/hồ sơ bản mới; F2–F4 bổ sung điểm vào, giao thức và fixture giả. Số hạng gốc, nền và các quyết định nguồn giữ nguyên. Dùng tên phiên bản mới để Claude đối chiếu từng thay đổi.

### Kiểm bản Claude chuyển lại và triển khai phần thống nhất

Claude rút bất đồng về nghĩa vụ báo bản nhạy loại ca lỗi. Cả hai giữ Q-211(6) và WHY-06. Không có phản đối với sửa F1–F7. Sau kiểm trực tiếp, đồng ý F8 và F9. F8 tái tính đúng sáu hàng trên 180 bản ghi C-e đã seal. F9 được xác nhận từ hồ sơ cũ và hợp đồng T-043, bản đồ G2-H03/H06/H17 và T-041 §5–6. Bản 002 phân biệt P4, DT18, lý do kỹ thuật và luật chọn trên dev. Không thay quyết định M1. Bổ sung Q-211(7) về ghi mỗi lần xem test trong giao thức.

| Điểm | Phản hồi và kết quả | Bằng chứng | Minh quyết |
|---|---|---|---|
| F1 | Đúng. Bổ sung đối chiếu hai chiều, theo fault/vị trí N và chuỗi TT hại, OB giúp, E1, C-d2, vùng đổi. Phân tích hậu kiểm. Giữ OPEN cơ chế vật lý và hiệu quả độc lập. | phan-tich-bo-sung-002.json, bao-cao-t13-002.md, frame T-053 và sidecar T-051. | |
| F2 | Đúng. Thêm bộ kiểm cohort độc lập với manifest runtime, root khác cho TT và OB, đường dẫn/file/byte/hash, mốc theo manifest được ghim. | p7_entry_v2.py, fixture policy cùng nhánh với repo giả. | |
| F3 | Đúng. Đã ghi tuyến worker/timeout/môi trường/bản ghi và script so dev. Chưa chạy ca dev thật qua tuyến này. F3 vẫn chặn khóa G3. | p7_entry_v2.py, p7_ob_worker.py, pilot_f3_v2.py. | |
| F4 | Đúng. Bổ sung giả thuyết/diễn giải, tiếp xúc, vị trí N, snapshot/T12, C-e thiếu lịch sử, A4 theo bản ghi, ghim phụ thuộc/môi trường và dấu vân tay từng vế. Giữ yêu cầu bản nhạy loại lỗi và ghi sổ truy cập. Quy tắc chi tiết bản nhạy, hoán vị ca và điều phối P7 vẫn là ứng viên. | giao-thuc-p7-a-002.json, a4_v2.py, kiem_sua.py, fixture giả. | |
| F5 | Đúng. Thêm E1 trên hai nền và ca socket trong phần phân tích. | ho-so-g3-002.md, bao-cao-t13-002.md. | |
| F6 | Đúng. Bảng mới nêu trạng thái và mẫu số C-d3 TT/OB. | bao-cao-t13-002.md. | |
| F7 | Đúng. Tách seal nguồn của bảng độc lập/vùng và seal chuẩn hóa T-052 khi mô tả thời điểm nhãn. | bao-cao-t13-002.md và ba biên nhận. | |
| F8 | Đúng. Tính sáu vế từ cửa sổ giả đã seal. Mỗi cặp có 30 ca, 0 loại. Bảng bổ sung tổng xác suất đứng đầu, O/U, V0/N1 và RR root tương lai. | phan-tich-bo-sung-002.json#/C_e. | |
| F9 | Đúng. Ghi đồ thị tính gì, căn cứ từng thành phần và phạm vi chưa có căn cứ P4. Dẫn G2-H/T-041/T-043 và quyết định dev, không suy mã hạn chế là cơ chế. | ho-so-g3-002.md. | |

**Hai chi tiết cần khóa trước G3.** Với bản nhạy loại lỗi, đề xuất loại nguyên cặp nếu M1 hoặc bất kỳ seed đã khai của baseline có ERROR/TIMEOUT phương pháp. Giữ NO_EVIDENCE/UNSUPPORTED theo giao thức. Bảng chính giữ nguyên ca, quy tắc lỗi trượt và trung bình ba seed. Trình công thức hoán vị ca hai phía bằng đổi dấu 10.000 mẫu, seed 20261005, cộng 1 để Claude kiểm, chưa coi được duyệt. Cả hai chỉ là độ nhạy và không điều khiển chuyển mức OB. Các việc còn lại được liệt kê trong giao thức 002; riêng quản lý dữ liệu phải ghim mốc/tập file/hash khi được quyền tạo manifest thật.

### Kết thúc lượt sửa

1. **Đã làm.** Ghi phần đồng thuận F1–F9 ở bản mới, gồm C-e đủ sáu vế, đường đi tính toán có ca đối chiếu và bản G3 mới. Tuyến F3 và script đã chuẩn bị, chưa có biên nhận tương đương qua ca dev thật. Bảng dev vẫn mô tả RQ3b/d và vùng nghi ngờ, chưa trả lời RQ3a, độ đúng vùng hay lợi ích độc lập.
2. **File.** Báo cáo/hồ sơ/giao thức/phân tích 002, sáu công cụ mới trong results/T-052/scripts, fixture và biên nhận trong runs/trien-khai-001, manifest-dap-phan-bien-002.json, nối LOG này và đúng dòng T-052 STATE. Giữ các bản trước, SPEC, src, sổ quyết định và kết quả hạng gốc. Claude giữ vai trò phản biện chính thức.
3. **Kiểm.** Manifest trước 393/393 khi mở lượt. Compile scripts, nguồn P4 T-034/T-041 khớp manifest, nguồn protocol/snapshot và dấu vân tay, C-e 30×6, tổng chênh theo nhóm/cặp và 23 vùng đổi, 8 mục fixture, Git diff --check. Lượt tính nháp dừng KeyError vì bản gọn thiếu U, giữ biên nhận lỗi rồi lấy U từ kế hoạch G1. Lượt sau PASS. Fixture chỉ dùng repo giả dưới results, không mở dữ liệu khóa thật.
4. **Phần mở.** Không còn bất đồng với Claude về nghĩa vụ loại ca lỗi, F8 hoặc F9. Cần Claude kiểm bản sửa và công thức ứng viên. F3 còn chờ quyền chạy theo yêu cầu Minh mới chỉ duyệt ghi. Dự kiến 2,5 phút máy, trần 10 phút cho một ca TT và một ca OB dev đã dùng, 12 vế, TORAI TT seed 0, mỗi lượt tối đa 180 giây. Nếu lệch, dừng kết luận tương đương, giữ biên nhận. G3 chưa khóa, task chưa nghiệm thu. Quyền dữ liệu, khóa revision, điều phối ma trận P7, giới hạn máy và private map còn chờ.

**Bước kế tiếp.** Khi Minh cấp quyền F3, chạy `& 'C:/Users/84583/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B -S results/T-052/scripts/pilot_f3_v2.py` và kiểm `runs/trien-khai-001/pilot-f3-v2-001/summary.json`. Minh có thể chuyển prompt dưới đây để Claude kiểm bản sửa song song với việc quyết quyền chạy. Lệnh cuối lượt ghi là chốt manifest 002 rồi kiểm byte/hash, LOG prefix, đúng một dòng STATE và `git diff --check`. Commit đề xuất khi Minh yêu cầu là `fix(T-052): xử lý phản biện T13 và bổ sung hồ sơ G3`.

### Prompt Claude — kiểm lại bản sửa 002

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-052, tasks/T-052-t13-va-ho-so-g3/SPEC.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P6/P7, G3(a).
- Người làm và người phản biện chính thức: Codex người làm, Claude người phản biện.
- Tài liệu gốc: AGENTS.md, docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md, docs/reference/sources/DT18-de-tai-va-nhiem-vu.md, docs/reference/sources/advisor-2026-09-23.md, tasks/T-052-t13-va-ho-so-g3/SPEC.md.
- Phản biện và phản hồi trước: results/T-052/manifest-dap-phan-bien-001.json#/source_review, LOG T-052 Phiên 6, results/T-052/manifest-dap-phan-bien-002.json#/source_review, LOG T-052 Phiên 7.
- Code và kết quả liên quan: results/T-052/manifest-dap-phan-bien-002.json, bao-cao-t13-002.md, ho-so-g3-002.md, giao-thuc-p7-a-002.json, phan-tich-bo-sung-002.json và scripts/runs được ghim trong manifest.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat. Quyền ghi bản phản biện hoặc chạy chỉ theo chỉ định riêng của Minh.

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

Ghi chú kiểm cuối: gói này thêm bảy script, gồm cả pilot_f3_v2.py. Đính chính số đếm “sáu” ở mục File. Kiểm byte/hash manifest 002 và git diff --check đã chạy đạt.

## Phiên 8 — 04/11/2026 22:07 — Codex — Windows — người làm

Minh duyệt: “duyệt chạy F3”. Thực hiện lát cắt đã trình: ca RE2-TT và Nezha-OB dev đã có bản nguồn, sáu tuyến mỗi bộ, TORAI TT seed 0, tối đa 180 giây mỗi vế và trần 600 giây toàn đợt. Chỉ dùng allowlist dev. Manifest bàn giao 002 khớp 435 file trước lượt. Chạy pilot_f3_v2.py và giữ biên nhận từng vế, kể cả lỗi.

### Kết thúc Phiên 8 — biên nhận F3

1. **Đã làm.** Chạy đúng hai ca dev đã khai qua tuyến v2. Kết quả PASS, TT 6/6 và OB 6/6. Cận trên thời gian máy 404.16 giây, gồm 310 giây dành cho lượt TT và 94.16 giây đo lượt OB. Nguồn runs/trien-khai-001/pilot-f3-summary-001.json. Trạng thái CIRCA và TORAI B trên OB lần lượt là UNSUPPORTED và UNSUPPORTED.
2. **File.** Ghi bản ghi và biên nhận từng vế ở pilot-f3-v2-001 và pilot-f3-v2-002-ob, nối LOG, cập nhật đúng dòng T-052 STATE và tạo manifest-f3-001.json. Gói bản sửa 002 và kết quả khoa học trước đó giữ lịch sử.
3. **Kiểm.** So hash đầu vào, cửa sổ, trạng thái và nhóm hòa theo 12 biên nhận. Không có mục đối chiếu lệch. Kiểm 435 đầu ra 002 trước chạy, sau chạy đối chiếu prefix LOG và các file gốc, kiểm toàn bộ hash manifest mới và git diff --check.
4. **Phần mở.** F3 đạt trên hai ca đã khai. Phạm vi chỉ gồm ca TT/OB này và TORAI B seed 0. Chưa xác nhận các ca khác, ba seed hoặc toàn ma trận P7. Claude kiểm bản sửa và biên nhận. Minh còn quyết quy tắc độ nhạy, nghiệm thu và khóa G3 sau khi đủ hồ sơ. SPEC P7, môi trường/revision khóa, ma trận và ngân sách, private map, quyền mở test và RE3 giữ trạng thái chờ như giao thức 002.

Lượt đầu hoàn tất sáu vế TT rồi dừng trước gọi OB vì job OB dùng t_ns trong selection, còn script pilot lấy t của TT. Giữ driver-failure.json. Lượt nối chạy đúng sáu vế OB với t tùy chọn, giữ mã điều phối trong pilot-f3-v2-002-ob-driver.py. Không đổi điểm vào P7 v2 hoặc chạy lại TT.
**Bước kế tiếp.** Minh chuyển prompt dưới đây để Claude kiểm lại. Đọc summary.json và từng compare.json trước khi xem kết luận. Đề xuất commit sau nghiệm thu và quyền Minh cấp là fix(T-052): kiểm tuyến P7 v2 trên dev. Lệnh chạy: python -B -S results/T-052/scripts/pilot_f3_v2.py theo môi trường trong Phiên 7. Lệnh cuối: kiểm hash manifest-f3-001.json, LOG prefix và đúng dòng STATE, git diff --check.

### Prompt Claude — kiểm bản sửa 002 và biên nhận F3

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-052, tasks/T-052-t13-va-ho-so-g3/SPEC.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P6/P7, G3(a).
- Người làm và người phản biện chính thức: Codex người làm, Claude người phản biện.
- Tài liệu gốc: AGENTS.md, docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md, docs/reference/sources/DT18-de-tai-va-nhiem-vu.md, docs/reference/sources/advisor-2026-09-23.md, tasks/T-052-t13-va-ho-so-g3/SPEC.md.
- Phản biện và phản hồi trước: results/T-052/manifest-dap-phan-bien-001.json#/source_review, LOG T-052 Phiên 6, results/T-052/manifest-dap-phan-bien-002.json#/source_review, LOG T-052 Phiên 7 và Phiên 8.
- Code và kết quả liên quan: results/T-052/manifest-f3-001.json, results/T-052/manifest-dap-phan-bien-002.json, results/T-052/bao-cao-t13-002.md, results/T-052/ho-so-g3-002.md, results/T-052/giao-thuc-p7-a-002.json, results/T-052/runs/trien-khai-001/pilot-f3-summary-001.json, code và nguồn ghi trong manifest.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat. Quyền ghi bản phản biện hoặc chạy theo chỉ định riêng của Minh.

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

## Phiên 9 — 04/11/2026 22:49 — Codex — Windows — người làm

Minh chỉ định tệp vừa gửi: “đây là thay cho claude phản biện đây”. Tiếp nhận nội dung làm bản phản biện của lượt này, không chờ Claude gửi lại cùng lượt. Ghi đúng nguồn là nhận xét Codex trong chat do Minh chỉ định thay cho lượt này. Tệp ghi Claude vẫn là người phản biện chính thức; việc tiếp nhận không tự thay vai trò trong SPEC hoặc xác nhận đã có phản biện chéo độc lập cho khóa G3.

1. **Đã làm.** Đối chiếu tệp và biên nhận F3. Tiếp nhận kết luận F3 đạt trong lát cắt hai ca dev, TORAI B TT seed 0. Bản 002 đủ căn cứ trình Minh nghiệm thu phần mô tả T13. G3(a) còn hai điểm chặn, F2 và F4. Không còn bất đồng về nội dung các điểm này.
2. **File.** Nối LOG, cập nhật đúng dòng T-052 STATE, tạo manifest-tiep-nhan-phan-bien-001.json lưu nguyên văn bản Minh chỉ định. Bản nghiên cứu và code đã ghim giữ lịch sử.
3. **Kiểm.** Manifest F3 khớp 534/534 trước ghi. Tệp Minh vừa chuyển khớp byte/hash tệp lượt trước. Lượt trước đã tái hiện bằng metadata giả ba phản ví dụ: mốc/hash sai nhưng cùng thành viên, sai biến thể baseline vẫn ghép, lỗi dữ liệu bị tính như lỗi phương pháp. Kiểm cuối xác minh hash, prefix LOG và một dòng STATE. Không có lượt chạy phương pháp mới.
4. **Phần mở.** Minh có thể nghiệm thu riêng phần mô tả dev T13. G3 vẫn cần bằng chứng ở ba liên kết và khóa giao thức P7. Hiệu quả độc lập, cơ chế vật lý, RQ3a và độ đúng vùng ảnh hưởng giữ OPEN. Quyền thay vai trò chính thức, khóa G3 và mở test không suy từ lời chỉ định bản phản biện này.

### Phạm vi đề xuất cho bước G3/P7

- Bộ quản lý dữ liệu kiểm đối chiếu riêng từng mã thành viên G1 với mốc, file, byte/hash và hỗ trợ C-e từ nguồn đã duyệt, trước khi cấp biên nhận runtime. Kiểm bằng metadata giả trước G3. Đối chiếu dữ liệu thật chỉ sau quyền tương ứng. Phép kiểm phải từ chối đổi mốc hoặc đổi file dù mã mờ giữ nguyên.
- Bộ điều phối P7 xác thực đúng danh tính bản ghi trước chấm A4: dataset, ca, vế, phương pháp, biến thể, seed và dấu vân tay đã khai. Trường hợp BARO được đưa vào vế SimpleRCA M4 phải bị từ chối trước A4.
- Phân loại lỗi trước seal. Lỗi dữ liệu, adapter, runner, hạ tầng hoặc chưa phân loại dừng vế phụ thuộc. Lỗi phương pháp đã xác nhận trên đầu vào hợp lệ vẫn vào bảng chính theo giao thức. Fixture cần chứng minh cả nhánh dừng và nhánh tính trượt.
- Khi có bản giao thức kế tiếp, cập nhật dẫn F3 từ manifest-f3-001.json, ghi đúng phạm vi tuyến baseline sau bước chọn nguồn. Chốt quy tắc độ nhạy, driver, máy/ngân sách và private map trong cùng hồ sơ.

**Bước kế tiếp.** Đọc SPEC T-052 mục Tập ca/tiêu chí xong và giao-thuc-p7-a-002.json. Trình gói P7 với ba phép kiểm trên và các mục khóa còn thiếu. Prompt nguyên văn của lượt này nằm trong trường source_review/text_as_received của manifest tiếp nhận; Minh đã chỉ định bản nhận xét hiện tại thay lượt Claude. Khi có bản sửa mới để soát, dùng prompt mẫu kiểm lại phản hồi và sửa của G3. Lệnh cuối lượt: kiểm byte/hash manifest tiếp nhận, prefix LOG, đúng dòng STATE và git diff --check.

## Phiên 10 — 04/11/2026 23:01 — Codex — Windows — người làm

Minh “duyệt sửa” ba liên kết đã phản biện: ca → file/mốc, vế → bản ghi A4, nguồn lỗi/bước hết giờ → chấm hay dừng. Gói sửa thêm phiên bản v3 trong results/T-052, fixture giả và hồ sơ 003. Thay đổi có tác động đến điều kiện được chạy/chấm P7, không đổi phép thống kê A4, cấu hình M1 hay số liệu T13 dev. Tình trạng khóa G3, quyền mở dữ liệu và nghiệm thu là quyết định riêng.

1. **Đã làm.** F2 kiểm bản đồ ca theo hash thành viên bằng nguồn riêng được ghim. `attest_runtime` so tập, mốc, file, byte/hash, C-e hoặc trace guard trước cấp biên nhận. Runtime kiểm lại biên nhận khi mở. F4 dùng slot theo giao thức và biên nhận, kiểm method/variant/seed trên bản ghi thật trả về trước seal. Kiểm nguồn lỗi và bước hết giờ bằng biên nhận riêng. Lỗi chưa phân loại dừng. Evaluator xác minh hash và mọi điều kiện trước lần đầu đọc nhãn. A4 v2 là lõi tính toán. Hồ sơ mới dẫn F3 đã đạt 12/12 trên hai ca dev, TORAI TT seed 0.
2. **File.** Thêm p7_guard_v3.py, p7_a4_v3.py, kiem_p7_v3.py, giao-thuc-p7-a-003.json, ho-so-g3-003.md, biên nhận kiem-p7-v3-001, manifest-sua-f2-f4-003.json. Nối LOG và đổi đúng dòng T-052 STATE. Nguồn, các phiên bản đã ghim và src giữ lịch sử.
3. **Kiểm.** 535/535 đầu ra trước lượt khớp. Sáu nhóm fixture đạt, gồm bảy biến đổi binding TT/OB, sai vế, thiếu/trùng, lỗi cấu hình, lỗi hợp đồng dữ liệu, hết giờ khi TORAI chuẩn bị, chặn đọc nhãn khi seal sai, seed lỗi phương pháp đã xác nhận vẫn tính 0. Ví dụ giả TT một seed lỗi cho ΔRR=1/3. 93 file code theo giao thức khớp hash; kiểm compile, hash manifest mới, prefix LOG, đúng dòng STATE và git diff --check. Không chạy phương pháp thật hay mở dữ liệu khóa.
4. **Phần mở.** Code và fixture xử lý phản ví dụ F2/F4 trên dữ liệu giả, chưa đủ kết luận runtime thật đã khớp. Cần Minh quyết nguồn độc lập và người cấp ref bản đồ ca/biên nhận phân loại trong SPEC P7. Bản 003 để thời hạn vế và các pha timeout được tính điểm OPEN, tránh tự đổi quy tắc. Đối chiếu thật sau quyền mở dữ liệu. Còn điều phối full P7, ngân sách, quy tắc độ nhạy, revision, khóa và quyền dữ liệu. T13 vẫn mô tả dev, lợi ích độc lập/cơ chế vật lý/độ đúng vùng còn OPEN.

**Bước kế tiếp.** Dùng prompt dưới để kiểm bản sửa và biên nhận. Lệnh đã chạy: python -B -S results/T-052/scripts/kiem_p7_v3.py với môi trường ở Phiên 7. Lệnh cuối: kiểm hash manifest-sua-f2-f4-003.json, prefix LOG, một dòng STATE và git diff --check. Giữ lại fixture, dùng thư mục lượt mới nếu chạy lại. Commit đề xuất sau quyền Minh cấp là fix(T-052): xác minh ca và chặn bản ghi sai trước A4.

### Prompt kiểm lại bản sửa F2/F4 v3

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-052, tasks/T-052-t13-va-ho-so-g3/SPEC.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P6/P7, G3(a).
- Người làm và người phản biện chính thức: Codex người làm, người phản biện theo chỉ định của Minh và SPEC.
- Tài liệu gốc: AGENTS.md, docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md, docs/reference/sources/DT18-de-tai-va-nhiem-vu.md, docs/reference/sources/advisor-2026-09-23.md, tasks/T-052-t13-va-ho-so-g3/SPEC.md.
- Phản biện và phản hồi trước: results/T-052/manifest-dap-phan-bien-001.json#/source_review, manifest-dap-phan-bien-002.json#/source_review, manifest-tiep-nhan-phan-bien-001.json#/source_review và LOG T-052 theo thứ tự phiên.
- Code và kết quả liên quan: results/T-052/manifest-sua-f2-f4-003.json, ho-so-g3-003.md, giao-thuc-p7-a-003.json, manifest-f3-001.json và code/biên nhận trong manifest sửa.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat. Phạm vi ghi hoặc chạy theo chỉ định riêng của Minh.

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

## Phiên 11 — 04/11/2026 — Codex — Windows — người làm

Minh nói “duyệt sửa theo đề xuất” sau khi đã làm rõ phạm vi là đính chính hồ sơ trước khi xét khóa G3(a). Phạm vi gồm đúng bốn file nêu dưới đây.

1. **Đã làm.** Ghi bản 004 dẫn nguồn và phân biệt phần mô tả T13 dev có thể trình nghiệm thu riêng với bốn nhóm còn chặn G3(a). Bản 004 ghi rõ giới hạn F3, C-e và đối chứng, tình trạng RQ3a và các nghĩa vụ còn lại. Quyền ghi hồ sơ không cấp quyền triển khai mã, thực nghiệm, khóa G3 hay mở dữ liệu.
2. **File.** Thêm `results/T-052/ho-so-g3-004.md` và `results/T-052/manifest-dinh-chinh-g3-004.json`. Nối LOG này và cập nhật đúng dòng T-052 trong `docs/STATE.md`. Manifest 004 kế thừa dấu vân tay đầu ra ổn định từ bản 003 và thay pin của LOG/STATE theo phiên này.
3. **Kiểm.** Dùng Python `-X utf8 -B -S -` với fixture truyền qua đầu vào chuẩn. Kiểm manifest 003 khớp 577/577, code giao thức khớp 93/93 và biên nhận F3 có 12/12 đối chiếu đạt. Với hai ca TT giả và sáu ca OB giả, gọi `evaluate_sealed` với `read_pin` thay bằng seal trong bộ nhớ. Tráo root TT đổi ΔMRR từ 1/3 xuống 0. Gộp ô OB đổi p từ 1/64 lên 1/2. Root ngoài U vẫn được chấm. Tráo hai bản ghi M1 rồi cập nhật hash đổi ΔMRR từ 1/3 xuống −2/3. Sửa riêng `window` hoặc `input_sha256` của baseline, giữ mã ca và cập nhật hash, vẫn qua. Gọi helper C-d3 với cấu trúc `attempts` tái hiện `KeyError(0)`. Gọi `_check_failure` với lượt TORAI pha chưa rõ và biên nhận tự gán pha `method` tái hiện nhánh chấp nhận trong chính sách giả. Gọi `src/p3/runner.py::_ket_thuc` với `timed_out=True` và thay hàm ghi bằng trả kết quả trong bộ nhớ, xác nhận biến thể timeout SimpleRCA/CIRCA như bản 004. Kiểm cuối dùng SHA-256/byte của manifest 004, so prefix LOG, đúng một dòng STATE, liên kết hồ sơ và `git diff --check`.
4. **Còn mở.** T13 trả lời phần mô tả dev của RQ3b/d và vùng nghi ngờ của RQ3c. Hiệu quả độc lập, cơ chế vật lý, RQ3a và độ đúng vùng còn OPEN. G3(a) phụ thuộc các điều kiện A/B1/B2/C trong bản 004. Phạm vi sửa mã ứng viên và pilot cần trình riêng để Minh quyết.

**Bước kế tiếp.** Đọc `results/T-052/ho-so-g3-004.md` cùng `manifest-dinh-chinh-g3-004.json`. Khi Minh chuyển, dùng prompt bên dưới kiểm bản đính chính. Đề xuất trình riêng nghiệm thu phần mô tả dev và các điều kiện khóa G3(a). Lệnh cuối của lượt ghi là `git diff --check` sau kiểm hash và phạm vi. Commit đề xuất khi Minh cấp quyền là `docs(T-052): đính chính hồ sơ trước khóa G3(a)`.

### Prompt cho Claude kiểm bản đính chính

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-052, bản đính chính results/T-052/ho-so-g3-004.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P6/P7, chuẩn bị G3(a).
- Người làm và người phản biện chính thức: Codex làm, Claude phản biện theo SPEC T-052.
- Tài liệu gốc: AGENTS.md, docs/STATE.md, docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md, docs/reference/sources/DT18-de-tai-va-nhiem-vu.md, docs/reference/sources/advisor-2026-09-23.md, tasks/T-043-thiet-ke-rca-m1/SPEC.md, tasks/T-052-t13-va-ho-so-g3/SPEC.md.
- Phản biện và phản hồi trước: results/T-052/manifest-dap-phan-bien-001.json#/source_review, manifest-dap-phan-bien-002.json#/source_review, manifest-tiep-nhan-phan-bien-001.json#/source_review, LOG T-052 và các lượt chat do Minh chuyển.
- Code và kết quả liên quan: results/T-052/manifest-dinh-chinh-g3-004.json và chuỗi manifest, results/T-052/bao-cao-t13-002.md, results/T-052/ho-so-g3-002.md, results/T-052/ho-so-g3-003.md, results/T-052/giao-thuc-p7-a-003.json. Môi trường và lệnh ở LOG T-052.
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

## Phiên 12 — 05/11/2026 — Codex — Windows — người làm

Minh quyết: “không kiểm lại bản đính chính 004, duyệt luôn”. Ghi nhận nghiệm thu và đóng T-052 trong phạm vi mô tả T13 trên dev và hồ sơ đính chính 004 ghi các điều kiện còn chặn G3(a). Bản 004 đã được người làm tự kiểm. Minh duyệt trực tiếp và bỏ lượt kiểm lại độc lập đã dự kiến cho bản này.

1. **Đã làm.** Ghi quyết định nghiệm thu. Phạm vi gồm xếp hạng, đối chứng, C-e, vùng nghi ngờ và lát cắt đối chiếu baseline F3 trên dev. Hồ sơ 004 hoàn thành ở trạng thái nêu đủ các mục còn chặn theo tiêu chí xong 4 của SPEC.
2. **File.** Nối LOG và đổi đúng dòng T-052 trong `docs/STATE.md` sang xong. Hồ sơ 004 và manifest 004 giữ mốc trước nghiệm thu. Khi đối chiếu manifest 004 sau đóng, hai pin LOG/STATE thuộc ảnh chụp trước Phiên 12. LOG có thể kiểm theo tiền tố dài bằng số byte đã ghim. Dòng STATE cũ nằm trong mục mốc đối chiếu bên dưới.
3. **Kiểm.** Trước cập nhật, manifest 004 khớp 578/578 mục. Sau cập nhật, 576 mục đầu ra ổn định khớp. Hai pin lịch sử LOG/STATE kiểm khớp khi dùng tiền tố LOG và khôi phục dòng STATE cũ trong bộ nhớ. Kiểm prefix LOG, đúng một dòng STATE và `git diff --check`. Lượt này ghi quyết định nghiệm thu, không phải lượt kiểm độc lập bản 004.
4. **Còn mở.** T13 cung cấp mô tả dev cho RQ3b/d và vùng nghi ngờ cho RQ3c. Hiệu quả độc lập, cơ chế vật lý, RQ3a và độ đúng vùng còn OPEN. Bốn nhóm A/B1/B2/C trong hồ sơ 004 vẫn là điều kiện trước khi xét khóa G3(a). Khi Minh giao bước tiếp theo, trình SPEC P7 với phạm vi và bằng chứng còn thiếu. Quyền khóa và quyền mở dữ liệu được xét riêng.

**Bàn giao.** Đọc `results/T-052/ho-so-g3-004.md` mục “Điều kiện còn chặn G3(a)” và `giao-thuc-p7-a-003.json` trường `/open_before_execution` khi Minh giao chuẩn bị SPEC P7. Lệnh cuối lượt là `git diff --check` sau kiểm byte/hash và phạm vi. Đề xuất commit khi Minh cấp quyền là `docs(T-052): ghi nghiệm thu dev và bàn giao G3(a)`.

**Đề xuất ghi sổ khi Minh duyệt riêng.** Ngày 05/11/2026, Minh quyết “không kiểm lại bản đính chính 004, duyệt luôn”. T-052 nghiệm thu trong phạm vi mô tả T13 dev, lát cắt F3 và hồ sơ 004 ghi các mục còn chặn. G3(a) và quyền mở dữ liệu xét riêng.

### Mốc đối chiếu manifest 004

Dòng T-052 trong STATE tại thời điểm ghim manifest 004:

```text
- **T-052 — T13 dev và hồ sơ G3(a): đã ghi đính chính 004, chờ kiểm bản sửa (04/11/2026).** Có thể trình Minh nghiệm thu riêng phần mô tả dev, gồm lát cắt F3. G3(a) còn bốn nhóm chặn, cần hoàn thiện SPEC P7 trước khi xét khóa. [Hồ sơ 004](../results/T-052/ho-so-g3-004.md), [manifest](../results/T-052/manifest-dinh-chinh-g3-004.json), [LOG và prompt](../tasks/T-052-t13-va-ho-so-g3/LOG.md).
```

### Prompt soát đề xuất cho bước kế tiếp

Dùng khi Minh giao và dán kèm đề xuất SPEC P7(a) cho lượt mới.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: Đề xuất SPEC P7(a) do Minh chuyển khi mở việc kế tiếp. T-052 là hồ sơ nguồn.
- Công đoạn: soát SPEC.
- Gói/cổng: P6/P7, chuẩn bị G3(a).
- Người làm và người phản biện chính thức: T-052 có Codex làm, Claude phản biện. Vai trò của đề xuất mới theo SPEC và chỉ định của Minh.
- Tài liệu gốc: AGENTS.md, docs/STATE.md, docs/MRP.md, docs/DECISIONS.md, docs/WHY.md, docs/LESSONS.md, docs/reference/sources/DT18-de-tai-va-nhiem-vu.md, docs/reference/sources/advisor-2026-09-23.md, tasks/T-052-t13-va-ho-so-g3/SPEC.md.
- Phản biện và phản hồi trước: tasks/T-052-t13-va-ho-so-g3/LOG.md và các nguồn phản biện dẫn tại đó.
- Code và kết quả liên quan: results/T-052/ho-so-g3-004.md, results/T-052/giao-thuc-p7-a-003.json, results/T-052/manifest-dinh-chinh-g3-004.json. Môi trường và lệnh tại LOG T-052.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat khi Minh chuyển prompt.

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
