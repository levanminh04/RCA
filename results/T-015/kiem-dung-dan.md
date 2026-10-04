# Kiểm cơ chế và đúng đắn T-015

T-015 kiểm P1 và điều kiện G1. Các lượt mới chạy **MicroRank-RCAEval sửa đầu vào**; không gọi đó là MicroRank gốc. T-007 giữ làm mốc RCAEval, không chạy lại90ca của mốc. Lựa chọn P3 là CANDIDATE theo ngữ nghĩa và đầu vào, không chọn theo bản có điểm cao hơn. (chờ WHY, xem de-xuat-tai-lieu-chung.md.)

## 1. Nguồn và tái lập

`manifest-inputs.json` xác nhận đúng revision MicroRank/TraceRCA/RCAEval và whitelist30dev TT. Artifact T-007 có90JSON mỗi lượt OB được tái dùng, không rỗng, case độc nhất và log hoàn tất. Nguồn paper/mốc công bố tra trước run tại `runs/independent-math/published-before-run.json`. Biến thể sửa đầu vào không có số công bố riêng; không được lấy số WWW'21 hoặc T-007 làm mục tiêu để chỉnh nó.

Không có dữ liệu riêng của ba hệ A/B/C bài MicroRank trong phạm vi ca được phép chạy. Vì vậy chưa tái lập các con số toàn bài gốc. Giới hạn này làm yếu kết luận tái lập bài, không phủ nhận kiểm chính xác code/kernel trên đầu vào đã chứng minh. Không thay thiếu phép kiểm đó bằng lời “chạy được”.

## 2. Những phép kiểm có kết quả

| Phép kiểm | Bằng chứng | Kết quả và ý nghĩa |
|---|---|---|
| Tích lũy cạnh so AST gốc, lookup cha theo trace, nhiều root/mấtcha | `runs/graph-toy/result.json` | Đạt; A gọiB vàC ở hai trace giữ cảhai cạnh; orphan không được nối giả |
| Formula hai detector gốc | `runs/original-formula/result.json`; `runs/tracerca-audit/seed0/toy-checks.json` | Công thức counts/SLO toy khớp gốc; chưa chứng minh schema conversion đầy đủ |
| Không evidence, cột/dòng, duplicate, unknownbaseline | `runs/adapter-toy/result.json` | Đạt theo toy; trả trạng thái rõ, không fallback |
| std1, std0, keycollision, top_max+6, crossing END | `runs/extended-edge/result.json` |9checks đạt; std0 và >= có thể biến mọi trace thành anomal; không gọi là baseline khỏe |
| Pilot số học OB độc lập | `runs/independent-math/ob-pilot-rerun/summary.json` |327so sánh error0; điều kiện là graph snapshot |
| Lặp pilot giữa hai EC2 pin | `runs/pilot-environment-repeat.json` |461giá trị numeric error0; graph/count/rank exact |
| TT tính lại từ raw span đến graph | `runs/tt-independent-inputs/auth/comparison.json` |19checks đạt cho baseline/partition/incidence/coverage; audit null protocol ban đầu còn lỗi, xem §4 |
| TT PageRank, prior, weight, spectrum, score | `runs/tt-independent-math/auth/summary.json` |4383giá trị sai số tuyệt đối/tương đối0; không gọi25vòng là hội tụ |
| Đảo cột, shuffle dòng, seed0→1 | `runs/tt-local/auth/*-comparison.json` |13checks mỗi lượt exact; graph canonical không tùy thứ tự cột |
| Null root marker pandas.NA | `runs/null-root-toy/result.json`; `runs/tracerca-audit/parent-null-scalar-audit.json` |None/pd.NA cho graph+audit giống nhau sau sửa; snapshot cũ được giữ |
| TraceRCA T-007 | `runs/tracerca-audit/seed0/t007-audit.json` |90/90artifact tái dựng exact;90NaN và79đảo thứ tự hữu hạn được xác nhận |

## 3. Phép kiểm hai cửa sổ bình thường

Ca auth đã cố định trước kết quả. Control dùng hai đoạn trong600s trước inject, loại cả span có END≥inject. MicroRank trả11operation, normal863/anomaly570/all1433trace,2814span bị flag trong242818span current. Nguồn: `runs/tt-local/auth/two-normal-summary.json`. TraceRCA control nghiêm có cùng2814flag và102operation điểm hữu hạn: `runs/tracerca-audit/normal-boundary/strict-two-normal-windows.json`.

Đây là **báo giả theo giả định đoạn trước tiêm bình thường**. Nhãn thời gian tiêm không chứng minh không có sự cố tự nhiên khác hoặc workload drift; những nguyên nhân khác đó chưa có ground truth độc lập trong task. Không được gọi các thứ hạng này là nguyên nhân có nghĩa. Code chạy không lỗi, output hữu hạn và tính số học đúng vẫn chưa chứng minh detector hợp lệ trong chế độ tự phát hiện. T-015 không sửa ngưỡng theo control để cải thiện điểm; G1/P3 phải quyết giao thức biết mốc/normal reference riêng.

Lượt TraceRCA control cũ chỉ lọc START trước inject chứa11span END vượt mốc,4trong đó bị flag. Đã giữ lượt cũ và trừ đúng11span khi tái tính độc lập; số2818cũ chỉ đúng cho controlSTART. Không chép nó thành kết quả control bình thường nghiêm. Nguồn biên/correction: `runs/tracerca-audit/normal-boundary/`.

## 4. Lỗi bộ đếm audit nội bộ T-015

Graph builder ban đầu stringify parent pandas.NA thành`<NA>` nhưng tập token root chỉ nhậnNone/nan. Vì vậy parentnull bị báo “mất cha” ở audit, dù cạnh và incidence không đổi. Raw auth cónull thật; census isna đã nhận5567rootmarker trong window. Không được diễn giải các counts sai của snapshot groups thành trace instrumentation mất hàng. Root marker cũng không tự chứng minh frontend-server root theo policy gốc.

Đã freeze hai source trước sửa ở `runs/source-versions/`; thêm`<NA>` chỉ ở bộ đếm, toy None/pdNA đạt. Independent input audit ban đầu cũng dùng token thiếu nên19PASS không tự chứng minh semantic null; phần baseline/partition/graph vẫn có giá trị. Correction raw cho3TT lưu riêng sau khi worker OB xong; hồ sơ phải dùng correction cho root/missing. Chưa gọi đây là lỗi task cũ.

## 5. Cơ chế khác với mốc T-007

Hai sửa đã được định trước điểm: tích lũy mọi cạnh và dùng cùng hai tập trace rời cho graph/count. RCAEval dùng graph bình thường từ trước mốc, graph bất thường từ toàn bộ sau mốc, nhưng lengths lấy số trace có span bình thường/bất thường sau mốc. Một trace có cả loại span nằm ở cảhai lengths. `nf=w_o(N_A-c^A_o)` có thể âm khi c^A_o đếm tất cả trace sau mốc còn N_A chỉ trace flagged. `np` cũng có rủi ro khi graph trước mốc được so length của tập khác. Đây là bất nhất số đếm, không là một giả thuyết mới về đồ thị thắng.

Bản sửa dựng graph normal từ trace không có flaggedspan và graph anomaly từ trace có ít nhất1flaggedspan, giữ mọi span quan sát trong phần sau mốc của mỗi nhóm. Vì mỗi c_o≤N_group, các ô phổ không âm. Ngoài grouping và cạnh, canonical ordering/span-scoped parent lookup có thể góp phần làm thứ hạng khác. Không có ablation riêng từng thay đổi; không được quy chênh từngca riêng cho lợi ích PageRank hoặc riêng lỗi reset cạnh.

So từngca đã xong:90hàng `so-sanh-tung-ca.csv`,90đầu ra hợp lệ. Tập ứng viên TT đã kiểm3ca/33phép so,204dòng tại `bang-ung-vien-tt.csv` và `kiem-ung-vien-tt.md`. Không dùng trung bình để thay từngca.


## 6. Rà kết quả cuối, bản sao span và audit OB

Hai failed gốc được giữ; chẩn đoán11cột chỉ có bản sao hoàn toàn. Sửa lookup nhưng giữ occurrence theo graph gốc, không dedup ngưỡng RCAEval. Toy so AST và guard conflict đạt. Rerun2ca có8.328/9.345phép so độc lập sai số0; bảng so chọn rõ rerun khi đầu ra trước failed. Script không nhận hai output hợp lệ khác điểm là cùng một lượt.

Streaming audit `runs/ob-root-audit-correction-v2/manifest.json` kiểm lại8điều kiện trên88snapshot hợp lệ cũ;2snapshot failed không có metadata nên ghi not-applicable. Hai rerun mới đã dùng policy root nullable đúng và có graph/audit đầy đủ, không trừ null delta lần nữa. Giữ cả lượt audit đầu bị dừng ở failed và source trước sửa. Bản correction chỉ đổi nhãn root/missing, không chạy lại PageRank/phổ hoặc baseline.

`runs/final-scientific-audit.json` và `runs/ob-comparison-check-final.json` là kết quả kiểm đầu ra cuối. `kiem-cua-so-ob.csv` giữ hai phép kiểm cửa sổ300/600s; mọi mốc dữ liệu/hash trùng nhau, chỉ độ dài cửa sổ khác. Vector trace TT có3027so sánh trực tiếp khớp0 ở `runs/tt-trace-vector-probe/auth/summary.json`;298operation là kiểm lặp.

Các phép kiểm đủ để xác nhận công thức và giao thức đã cài trên dữ liệu được phép. Chúng không chứng minh detector ít báo giả, full MicroRank gốc tái lập được trên11cột, hay biến thể tốt hơn phương pháp khác. Chưa benchmark P3 hoặc phân tích hạn chế P4.


## 7. Tính tương thích của source cuối

Guard identity cuối đã kiểm raw8cột của cả90cửa sổ: không conflict; chỉ hai ca recommendation_loss có duplicate current. Vì vậy88graph/score cũ không bị thay bởi nhánh exact-copy mới; các rows/SLO không bị dedup. Proof ở `runs/final-input-identity-audit/summary.json`. Source adapter trước guard được phục hồi và hash khớp inventory trước đó (`runs/source-versions/adapter-recovery-proof.json`). Source cuối và nguồn MIT trong `runs/final-source-manifest.json`. Root classification sửa độc lập, không gọi lại score. Không suy các lỗi export tạo bản sao từ riêng dữ kiện này.


## 8. Sửa sau REVIEW theo Minh duyệt

Minh duyệt danh sách sửa trong LOG phiên2 ngày04/10/2026. Bộ đếm, PageRank/spectrum MIT và điểm/ranking dataset cũ được giữ nguyên. Có27phản ví dụ thời gianNaN/Inf/durationâm bị từ chối rõ:10adapter,9independentTraceRCA và8root-duration; toy hợp lệ khớp chính xác adapter trước sửa và công thức AST tác giả. Nguồn `runs/review-response/guard-tests.json`; source trước sửa được freeze ở `source-before/`. Đây là guard của biến thể/adapter, không khẳng định code gốc có guard đó.

Quét hai cột thời gian của đúng90OB+3TT đã chạy trên EC2hai:0invalid trong toànraw lẫn cửa sổ±600s,93sourcehash khớp. Nguồn `runs/review-response/ec2-second/input-time-audit/summary.json`. Không gọi detector/PageRank/ranker, không đọc nhãn, không có lượt phương pháp mới; ledger vẫn110. Lần quét đầu hỏng vì manifest chưa nằm trên EC2; giữ console và dùng lần2 mới với manifest đúng. Không dùng thời gian quét làm benchmark.

R1: ba ca có trung vị độ dài normal/anomaly5/179 span; nhóm bất thường giàu trace dài. Luật “ít nhất một span” có nhiều cơ hội flag khi span nhiều, nhưng tương quan chưa xác nhận tác động causal hoặc Dstar2 trực tiếp đo độ dài. Cấu trúc workload, operation mix, prior và tracing có thể cùng tạo chênh. Auth có903trace dài và903trace station nhưng giao866, không cùng tập. Tỷ lệ cờ auth1,04%span/51,4%trace; control1,16%/39,8%. Baseline khác thời lượng/thành phần nên hai tỷ lệ chỉ mô tả, không đo hiệu quả. Số/source đọc từ `runs/review-response/trace-length-stats.csv`; giải thích cụ thể trong ví dụ.

N1: chẩn đoán từ cùng snapshotauth bằng script độc lập với25/26/50/100/101 vòng định trước probe. Vòng25 khớp mọi score lưu (sai số0);26/50/100 đổi full vàtop11;101 đổi full nhưng giữtop11. Ngay100/101 chưa hội tụ. Nguồn `runs/review-response/iteration-probe.json`. Giữ25 để khớp code, không chọn số vòng theo nhãn/thứ hạng. Phép này đã thiếu ở bàn giao đầu, được bổ sung ở phiên phản hồi rồi lưu sau Minh duyệt.

R2: kiểm thực nghiệm là3/30dev, chưa kiểm27ca. Capcopy là diễn giải bảo thủ của người làm, không phải Minh bắt buộc thu hẹp. Đây là thu hẹp kế hoạch round-robin; không dùng kết quả3ca kết luận coverage cả30. R3: phương án baseline trước mốc đã được thêm vào WHY nháp; chỉ sửa normalcount vẫn để nf âm nếu anomalygraph chứa toàncurrent nhưng đếm chỉflaggedsubset. Phải nhất quán cả hai phía; phương án pre/post khác ngữ nghĩa hai nhóm cùngwindow của gốc. Không chạy phương án đối lập sau khi nhìn điểm.

Nguồn cuối sau guard hữu hạn được ghi ở `runs/review-response/current-source-manifest.json`; `runs/final-source-manifest.json` ghi source trước phiên sửa này. Các generator bàn giao cũ phản ánh bản trước REVIEW; không chạy chúng để ghi đè hồ sơ đã sửa. Kết quả kiểm bàn giao sau sửa nằm ở `runs/review-response/repair-validation.json`.
