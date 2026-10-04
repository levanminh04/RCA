"""Complete reports from saved results, preserving historical run artifacts."""
import csv,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[3];OUT=ROOT/'results/T-015'
def j(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def change(path,old,new):
    text=path.read_text(encoding='utf-8-sig');assert old in text,(path,old[:100])
    path.write_text(text.replace(old,new),encoding='utf-8')
def append(path,text):
    with path.open('a',encoding='utf-8') as f:f.write('\n\n'+text+'\n')
profile=OUT/'ho-so-microrank.md'
change(profile,'Đọc cùng bản đính chính audit của T-015.',
       'Audit raw sửa cho root bình thường/bất thường1.326/1.403 và missing-parent0/0; bốn quan hệ graph mỗi phía khớp tuyệt đối (`runs/root-audit-correction/auth/audit-correction.json`). Probe quan sát biến trả về của `official.pageRank` không sửa source:2.729 trace PPV và298 operation PPV khớp0 (`runs/tt-trace-vector-probe/auth/summary.json`). 298 operation là kiểm lặp, không cộng thành số giá trị khác nhau.')
change(profile,'spanID duy nhất trong từng trace;', 'ID trùng phải cùng nội dung quan sát, bản sao giữ số lần xuất hiện; ID trùng khác nội dung bị từ chối;')
change(profile,'toàn worker 14,312s;', 'toàn worker 14,653s;')
append(profile,'''### 9.2. Kết quả đối chiếu từng ca và policy bản sao

`so-sanh-tung-ca.csv` có90hàng, dùng đúng mốc T-007 L20±600s đã lưu và90đầu ra hợp lệ của biến thể. Không có điểm trung bình để chọn bản. Mỗi hàng chứa hai danh sách operation/service, hạng root đọc sau prediction, counts, overlap và cơ chế graph-count. `runs/ob-comparison-check-final.json` kiểm hữu hạn/không âm, counts cùng nhóm và output không rỗng. Phép so là thay đổi kết hợp grouping, tích lũy cạnh, canonical ordering và parent lookup theo trace; chưa có ablation để gán riêng từng chênh lệch cho một sửa.

Hai ca recommendation_loss_1/_2 ban đầu bị guard từ chối. Chẩn đoán tất cả11cột cho48/99key trùng hoàn toàn, không conflict (`runs/duplicate-input-audit/summary.json`). Gốc dùng một lookup `temp[spanID]` nhưng append `pr_trace` mỗi doc (`MR:preprocess_data.py:398–449`). Bản sửa giữ mọi row trong detector/SLO RCAEval và occurrence prior; chỉ lookup cha dùng một identity. Đây không phải nói SLO gốc cũng giữ bản sao: preprocessing SLO gốc duyệt dict span duy nhất. Conflict measurement bị từ chối là guard bổ sung, khác last-wins của gốc. Toy duplicate so AST gốc đạt cả4relations; hai rerun độc lập8.328/9.345so sánh khớp0. Failure và bảng so ban đầu được giữ ở `runs/ob-block-3/` và `runs/so-sanh-tung-ca-before-duplicate-policy.csv`. Lý do sửa ghi trước ranking mới, theo cơ chế (chờ WHY, xem de-xuat-tai-lieu-chung.md).

`kiem-cua-so-ob.csv` so hai ca định trước ở±300/±600s; thay cửa sổ đổi số trace và điểm. T015 dùng±600s để đồng nhất T007 L20 và WHY16; kết quả này không chốt cửa sổ P3. `kiem-ung-vien-tt.md` và204dòng `bang-ung-vien-tt.csv` phân biệt inventory, trace, graph, rank đầy đủ và top11 trên3ca TT, không suy trần cho30ca.''')
example=OUT/'vi-du-tinh-tay.md'
change(example,'Bản đính chính audit riêng của T-015 phải đi kèm khi đọc kết quả này.',
       'Bản raw correction `runs/root-audit-correction/auth/audit-correction.json` xác nhận root1.326/1.403, missing-parent0/0, cả4relations mỗi phía khớp tuyệt đối. Root marker không chứng minh frontend-server root theo policy gốc. Probe `runs/tt-trace-vector-probe/auth/summary.json` so trực tiếp2.729 trace PPV và298 operation PPV với locals của hàm gốc không sửa source:3027comparisons sai số0. Vì vậy vector trace trong ví dụ có đối chiếu trực tiếp, không chỉ suy từ operation output.')
verification=OUT/'kiem-dung-dan.md'
change(verification,'So từngca và tập ứng viên TT sẽ bổ sung sau khối chạy hoàn tất. Không dùng trung bình để thay từngca.',
       'So từngca đã xong:90hàng `so-sanh-tung-ca.csv`,90đầu ra hợp lệ. Tập ứng viên TT đã kiểm3ca/33phép so,204dòng tại `bang-ung-vien-tt.csv` và `kiem-ung-vien-tt.md`. Không dùng trung bình để thay từngca.')
append(verification,'''## 6. Rà kết quả cuối, bản sao span và audit OB

Hai failed gốc được giữ; chẩn đoán11cột chỉ có bản sao hoàn toàn. Sửa lookup nhưng giữ occurrence theo graph gốc, không dedup ngưỡng RCAEval. Toy so AST và guard conflict đạt. Rerun2ca có8.328/9.345phép so độc lập sai số0; bảng so chọn rõ rerun khi đầu ra trước failed. Script không nhận hai output hợp lệ khác điểm là cùng một lượt.

Streaming audit `runs/ob-root-audit-correction-v2/manifest.json` kiểm lại8điều kiện trên88snapshot hợp lệ cũ;2snapshot failed không có metadata nên ghi not-applicable. Hai rerun mới đã dùng policy root nullable đúng và có graph/audit đầy đủ, không trừ null delta lần nữa. Giữ cả lượt audit đầu bị dừng ở failed và source trước sửa. Bản correction chỉ đổi nhãn root/missing, không chạy lại PageRank/phổ hoặc baseline.

`runs/final-scientific-audit.json` và `runs/ob-comparison-check-final.json` là kết quả kiểm đầu ra cuối. `kiem-cua-so-ob.csv` giữ hai phép kiểm cửa sổ300/600s; mọi mốc dữ liệu/hash trùng nhau, chỉ độ dài cửa sổ khác. Vector trace TT có3027so sánh trực tiếp khớp0 ở `runs/tt-trace-vector-probe/auth/summary.json`;298operation là kiểm lặp.

Các phép kiểm đủ để xác nhận công thức và giao thức đã cài trên dữ liệu được phép. Chúng không chứng minh detector ít báo giả, full MicroRank gốc tái lập được trên11cột, hay biến thể tốt hơn phương pháp khác. Chưa benchmark P3 hoặc phân tích hạn chế P4.''')
append(OUT/'de-xuat-tai-lieu-chung.md','''## 7. DECISIONS — EC2 thứ hai theo Minh

**Đoạn cũ:** chưa có chỉ đạo trong phiênT015. **Đoạn mới:** 04/10/2026 — Minh: "chuyển sang 3.26.62.217 , file key2.pem, ssh xem được không"; "nếu thiếu ram thì chuyển lê ec2 nhé, 3.26.62.217 là ec2 thứ 2". T015 được dùng máy hai, mọi ghi mới trong~/rca/T-015/. **Vì sao:** lưu chỉ đạo vận hành, không suy quyền chạy nhiều worker. **Phụ thuộc:** môi trường và nguồn dữ liệu, không chốt protocolP3.

## 8. WHY — bản sao span và guard conflict

**Đoạn cũ:** chưa có policy bản sao. **Đoạn mới:** Giữ mỗi row exact-copy trong SLO/detector RCAEval và pr_trace; lookup cha theo(traceID,spanID) giữ một identity. Chỉ chấp nhận ID trùng nếu8measurement columns cùng nội dung; conflicting identity báo lỗi. Vì sao: graph gốc overwrite lookup nhưng append occurrence mỗi row; không dedup để tự thay prior. Đã xét reject mọi duplicate (bỏ hai ca hợp lệ về quan sát), dedup toànrow (thay detector/prior), last-wins conflict (tùy thứ tự); không chọn theo điểm. SLO full-original duyệt dict unique spans, khác SLO RCAEval đang giữ của biến thể. Bằng chứng: diagnosis48/99exactkeys,0conflict, toy AST graph, hai rerun độc lập. Phụ thuộc: giao thức input và2ca so OB; không suy exporter tạo duplicate vì nguyên nhân gì. Đây là đề xuất G1, không quyết định P3.''')
append(OUT/'moi-truong.md','''
Kết quả chuyển được kiểm189file đúnghash/byte tại `runs/setup/input-verified.json`. Môi trường/executable/hash kernel và danh sách file riêng từng máy ở `runs/ec2-first-inventory/` và `runs/ec2-second-inventory/`; manifest output bàn giao ghi từng đường dẫn. Sau lỗi nullable và exact-copy, snapshot/lượt cũ được giữ cùng source tương ứng. Source cuối có guard conflict; lõi3hàm MIT không đổi.

Khối90OB chia30/30/29ca saupilot, dự báo17,9phút trước điểm. Tổng ba khối837,091s, pilotmáy2 12,068s; thêm rerun2ca12,864s và kiểm cửa sổ/maths/audit vẫn dưới1giờ, xa trần3giờ. Đây là chi phí quan sát, không số benchmark. Trước mọi lượt thấy một worker T015 hoặc máyidle; không chạy worker T015 cạnh worker nặngT014 máy đầu. Tổng TT mới3ca/controls cũng dưới10phút theo logs. Không Stop/reboot/đổi cấu hình EC2.''')
gen=OUT/'scripts/write_input_requirements.py'
change(gen,'runs/pilot, ob-main-ec2-2, tt-local','runs/pilot, ob-block-1/2/3, ob-duplicate-rerun, tt-local')
change(gen,'kiểm key collision','kiểm key collision; exact-copy giữ occurrence, conflict ID báo lỗi')
print('Reports completed from saved artifacts; input CSV generator updated.')
