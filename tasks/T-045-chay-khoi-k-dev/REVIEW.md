# Phản biện T-045 — lượt 1 (soát kết quả)

- **Người phản biện:** Claude, phiên mới độc lập với phiên người làm. Minh chỉ định ngày 01/11/2026 (LOG T-045 mục "Đổi người phản biện chính thức"; SPEC dòng 4 và Q-215 còn ghi Codex). Người làm vẫn là Claude phiên 1. Hai phiên cùng một mô hình; LOG đã ghi giới hạn này. — **Ngày:** 01/11/2026 — **Commit/diff đã đọc:** HEAD `bbef69dd` trên branch `claude/sweet-hawking-dy078d` (hơn `origin` 3 commit, chưa push); `git diff 69ef90b6 bbef69dd -- src/`; working tree chưa commit gồm `results/T-045/`, LOG T-045, dòng T-045 trong STATE.
- **Công đoạn/cổng và bản lượt:** soát kết quả; P6 (M1), chuẩn bị G3; bản đầu `tasks/T-045-chay-khoi-k-dev/REVIEW.md` (trước đó chưa có bản nào). Giữ vai trò: Claude phiên 1 là người làm.
- **Quyền lưu:** lượt này trước hết trả lời trong chat. Sau đó Minh nói nguyên văn: “ghi review và nêu đề xuất của bạn cho các vấn đề trên”. Bản này chỉ ghi file này. Không sửa LOG, STATE, báo cáo, kết quả hay code; không commit.
- **Bổ sung cùng lượt:** sau khi đọc bản này, Minh nói nguyên văn: “duyệt sửa, tôi cho bạn quyền đề xuất, tuy nhiên bám theo điều này giúp tôi. cái tôi quan tâm là các thành phần khác bị loại chỉ vì kết quả kém trên dev và chưa tìm ra được nguyên nhân kém, giả sử như dataset công khai kém nên làm chúng kém, e1 và e2 giúp cải thiện là đáng mừng nhưng tôi sợ nó chỉ là do việc chúng ta nhìn vào kết quả baseline để sửa cho phù hợp với dev”. Người phản biện hiểu “duyệt sửa” là duyệt cho người làm sửa A1–A3. Sau đó Minh nói nguyên văn: “duyệt ghi review và đề xuất, ngoài ra thì đề xuất có nêu việc kiểm xem tên của các mẫu e3 phát hiện là gì không ?”. Theo lời duyệt này, người phản biện thêm mục C và cập nhật hai dòng của prompt. Câu hỏi về tên mẫu E3 được trả lời riêng trong chat, chưa ghi vào bản này.
- **Đã đọc:** AGENTS; STATE; SPEC và LOG T-045; `results/T-045/` (`bao-cao.md`, `dinh-chinh-cai-dat.md`, `so-lan-nhin.jsonl`, `t1.json`, `t4.json`, `t4b.json`, `khoi-k.json`, `khoi-k/`, `co-che-khoi-k.json`, `do-ben.json`, `tai-lap-baseline.json`, `theo-loai-loi.json`, `e3-khong-nhan.json`, `doi-chieu-ks16.json`, `nhom-vong.json`, `manifest.json`, các script pha 2); `src/m1_danh_gia` (`luat_c`, `chon_khoi`, `pha2`, `rr`, `uv6`, `moc_gia`); `src/m1` (`e3`, `e4`, `e5`, `kenh`, `xep_hang`, `doi_chung`, diff ĐC1–ĐC3); SPEC T-043 (B1.3, B3, B4, Phụ lục C, D); `results/T-043/ma-tran-thu.json`, `dinh-nghia-pha2.json`; `results/T-034/bang-baseline.json`; MRP P6, P7; DT18; hướng dẫn của cô; DECISIONS Q-205–Q-215; WHY (WHY-55–65 và đoạn TORAI B trên Nezha-OB); LESSONS; `docs/review-prompt.md`.
- **Tự soát độc lập:** không có lượt phản biện kết quả nào trước. Đọc yêu cầu, code và đầu ra gốc trước; chỉ dùng LOG để biết thứ tự việc. Chạy lại phần rẻ; mọi file tạm để ngoài repo.

## Kết luận chung

Phần chạy, chấm và chọn của T-045 đúng và tái lập được. E1+E2 đúng là cấu hình mà luật khai trước chọn. Task đạt SPEC ở phần chạy, chấm và chọn. Task chỉ đạt một phần mục tiêu nguồn "kiểm hành vi trên dev" (MRP P6): đã phát hiện cổng và `verdict` không phân biệt cửa sổ có lỗi, nhưng chưa sửa (Minh hoãn ở D17, Q-b).

Có một điểm CHẶN: kết luận cơ chế E5 (R1). Điểm này không chặn lựa chọn E1+E2. Có hai điểm KHÔNG CHẶN (R2, R3). Đề xuất chưa nghiệm thu trước khi sửa R1.

## Các điểm

### R1. "E5 hại chủ yếu qua quy tắc nhóm vòng" sai khi tách theo ca và theo ô — CHẶN kết luận cơ chế E5; không chặn lựa chọn E1+E2

- **Ở đâu:** `results/T-045/bao-cao.md:23` (§1, phần suy luận), `:126–130` (§6.4, E5), `:162` (§9.4); `results/T-045/scripts/co_che_khoi_k.py:85` (hàm `so_E5` chỉ xét ca root tụt).
- **Sai gì:**
  - Báo cáo viết: "E5 hại khi đã có E1+E2 chủ yếu qua quy tắc nhóm vòng (mục 6.4). Đây đúng điều kiện thất bại đã khai ở CĐ3."
  - Căn cứ là 428/461 lần xóa (`co-che-khoi-k.json#/E5_E1+E2/quy_tac`). Đây là số kênh, chỉ đếm ở 8 ca root tụt.
  - Báo cáo không đối chiếu với ca root lên. SPEC T-045:115 đòi "so ca đúng và ca sai có điều kiện tương ứng khi báo cờ M5 và dấu vết E5".
- **Bằng chứng:** chạy chỉ đọc trên bản ghi pha 1 đã băm. Nhãn dev đọc qua `pha2_khoi_k.nap_nhan`, sau khi pha 1 đã băm. Lệnh, chạy từ gốc repo sau `source results/T-045/scripts/moi_truong.sh`, bằng `$PY -B -`:

```python
import collections, sys
sys.path[:0] = ['src', 'results/T-045/scripts']
from m1_danh_gia import rr
import pha2_khoi_k as pk

def vi_tri(blocks):
    return {e: (bi, gi) for bi, b in enumerate(blocks or []) for gi, g in enumerate(b['groups']) for e in g}

def truoc(a, r):
    return a[0] < r[0] or (a[0] == r[0] and a[1] < r[1])

nhan = pk.nap_nhan(False)
for L in pk.LUOT_THAT:
    rt, rb = pk.doc_ban_ghi(L, 'K-E1+E2'), pk.doc_ban_ghi(L, 'K-E1+E2+E5')
    for o in sorted(rb):
        root = nhan[o]['root']
        a, b = rr.rr_ca(rt[o]['blocks'] or [], root), rr.rr_ca(rb[o]['blocks'] or [], root)
        if a == b:
            continue
        vt, vb = vi_tri(rt[o]['blocks']), vi_tri(rb[o]['blocks'])
        if b < a:    # root tụt: kênh của chính root bị E5 coi là kế thừa
            ai = {root}
        elif root in vt and root in vb:  # root lên: thực thể từng đứng trước root, nay không còn
            ai = {e for e in vt if truoc(vt[e], vt[root])} - {e for e in vb if truoc(vb[e], vb[root])}
        else:
            ai = set()
        qt = collections.Counter(i['quy_tac'] for i in rb[o]['inherited_by']
                                 if i['thuc_the'] in ai and i['trang_thai'] == 'ap_dung')
        print(o, nhan[o]['o'], 'TUT' if b < a else 'LEN', f'{float(a):.3f}->{float(b):.3f}', dict(qt))
```

  Kết quả (15 ca có RR đổi; 37 ca không đổi):

  | Ca | Ô | RR E1+E2 → E1+E2+E5 | Kênh bị E5 xóa theo quy tắc |
  |---|---|---|---|
  | dev-7f1b6b071d | ts-travel-service\|loss | 0,500 → 0,062 (tụt) | nhóm vòng 174 (kênh root) |
  | dev-a5cabe5fa7 | ts-travel-service\|loss | 1,000 → 0,091 (tụt) | nhóm vòng 125 (kênh root) |
  | dev-a915aa2424 | ts-travel-service\|loss | 0,500 → 0,125 (tụt) | nhóm vòng 129 (kênh root) |
  | dev-20acb4402d | ts-order-service\|loss | 1,000 → 0,029 (tụt) | lan xuôi 6, lan ngược 4 (kênh root) |
  | dev-f36d0647d5 | ts-order-service\|loss | 1,000 → 0,059 (tụt) | lan ngược 8 (kênh root) |
  | dev-1ac905bc95 | frontend\|return | 1,000 → 0,200 (tụt) | lan ngược 6 (kênh root) |
  | dev-5ada15752d | frontend\|return | 1,000 → 0,200 (tụt) | lan ngược 6 (kênh root) |
  | dev-8ecd9880ed | checkoutservice\|return | 0,500 → 0,143 (tụt) | lan ngược 3 (kênh root) |
  | dev-98bc73c499 | ts-train-service\|cpu | 0,250 → 0,500 (lên) | nhóm vòng 320 (kênh thực thể rơi sau root) |
  | dev-a505ab3f65 | ts-train-service\|delay | 0,250 → 0,333 (lên) | lan ngược 22 (như trên) |
  | dev-fbc45b0c67 | ts-train-service\|delay | 0,500 → 1,000 (lên) | lan xuôi 32 |
  | dev-27252dca60 | productcatalogservice\|exception | 0,167 → 0,333 (lên) | lan ngược 13, lan xuôi 3 |
  | dev-5467884de4 | recommendationservice\|network_delay | 0,500 → 1,000 (lên) | lan xuôi 50 |
  | dev-55f99f3e0a | checkoutservice\|exception | 0,500 → 1,000 (lên) | lan ngược 21 |
  | dev-70629373f9 | paymentservice\|cpu_contention | 0,500 → 1,000 (lên) | lan ngược 42 |

  - 8 ca tụt thuộc 4 ô. Nhóm vòng chỉ có ở 3 ca, cả 3 cùng ô `ts-travel-service|loss`; 174 + 125 + 129 = 428 kênh. 5 ca tụt còn lại đi qua quy tắc lan ngược, lan xuôi thường, ở 3 ô.
  - 7 ca root lên: 1 ca qua nhóm vòng, 6 ca qua quy tắc thường.
  - Theo RR: ca tụt qua nhóm vòng mất 1,72; ca tụt qua quy tắc thường mất 3,87; ca lên qua nhóm vòng được 0,25; ca lên qua quy tắc thường được 2,25. Tổng −3,09/52 = −0,0594, khớp `khoi-k.json#/cap/E1+E2|E1+E2+E5/theo_the_gioi/P/dMRR/gop`.
  - Phần ròng: nhóm vòng khoảng −1,47; quy tắc thường khoảng −1,62. Mỗi ca chỉ thuộc một nhóm quy tắc, nên phép chia này không cộng chồng.
  - Nezha-OB không có nhóm vòng nào (`nhom-vong.json`, 0/22 ca), nhưng có 3/8 ca tụt.
- **Xét phản chứng:**
  - §6.4 có nhãn "quan sát cộng suy luận, chưa phân xử". Số 428/461 đếm đúng.
  - Nhưng chữ "chủ yếu" sai khi tính theo ca, theo ô và theo RR. Mẫu hình nhóm vòng đến từ một ô, đúng điều QT15 và SL14 cấm.
  - Ví dụ nhóm vòng {seat, travel, travel2} ở §6.4 vẫn đúng cho ô `ts-travel-service|loss`.
- **Bước và quyết định chịu ảnh hưởng:**
  - Lỗi diễn giải đã xảy ra; thiếu phép đối chiếu mà SPEC đòi.
  - Chặn dùng §1 (ý E5), §6.4 và §9.4 làm căn cứ sửa E5. Sửa riêng quy tắc nhóm vòng C′ chỉ nhắm khoảng một nửa phần hại. D5 lại cho thấy cách đọc C′ và A gần như trùng.
  - Không chặn kết cục HẠI gộp của E5, không chặn lựa chọn E1+E2.
- **Đề xuất sửa:** A1 ở mục Đề xuất.

### R2. Danh sách nguyên nhân báo nhầm của `verdict` thiếu nguyên nhân cấu trúc đã khai — KHÔNG CHẶN

- **Ở đâu:** `bao-cao.md:21` (§1), `:47` (§3), `:159` (§9.1), `:176` (§10, tiêu chí 2).
- **Sai gì:**
  - `verdict` ra CAUSE_FOUND khi tầng 1 không rỗng (`src/m1/xep_hang.py:158`). Quy tắc không xét số phép chấm. SPEC T-043:290 đã khai: "`CAUSE_FOUND` không xét số phép kiểm (B1.7)".
  - Báo cáo chỉ nêu ba nguyên nhân làm cổng của từng đơn vị qua giả. LOG mục trình D17 (Q-b) có nhắc "hiệu chỉnh nhiều phép kiểm", nhưng §1 và §9.1 của báo cáo bỏ ý này.
  - §3 và §10 gọi hiện tượng này là "do dữ liệu", "đặc điểm dữ liệu". Theo luật cứng 17, đây là giả định của phép tính (B1.3: hai mẫu độc lập) gặp dữ liệu tự tương quan.
  - Báo cáo chưa dẫn mô phỏng đã có ở SPEC T-043:415: AR(1), 300 + 300 điểm, không lỗi, tỷ lệ qua cổng 28,8% ở hệ số 0,9 và 38,6% ở hệ số 0,98. T-045 đo hệ số bậc 1 trung vị 0,935 trên 90 đơn vị có cờ (`runs/b2-t1-re2-mocgia-001/kiem-doc-lap-metric.json#/ac1_N_trung_vi`) và tỷ lệ metric qua cổng hướng lên 31,6%. Hai số này cùng bậc. Mẫu 90 đơn vị chọn theo cờ nên hệ số có thể thiên cao. Vì vậy chưa loại được trôi nền, nhưng đã có căn cứ để coi tự tương quan là ứng viên chính.
- **Bằng chứng:**
  - `t1.json#/RE2-TT/moc_gia/cong`: 10.804 + 8.946 + 3.232 + 31 = 23.013 phép chấm trên 30 cửa sổ giả, khoảng 767 phép mỗi cửa sổ.
  - Dù p đúng danh nghĩa và các mẫu độc lập, α = 0,01 vẫn cho kỳ vọng khoảng 7,7 đơn vị qua cổng mỗi cửa sổ. Chỉ một đơn vị qua cổng và vượt biên ε là đủ CAUSE_FOUND.
  - Lạm phát từng đơn vị cũng có thật: ở α = 0,001 vẫn còn 1.581 + 246 + 2 = 1.829 kênh có cờ trên 30 cửa sổ, khoảng 61 mỗi cửa sổ (`t4.json#/cau_hinh/T4-e0.05-a0.001/moc_gia/kenh_co_theo_nhom`). Mức danh nghĩa chỉ khoảng 0,77.
  - Vậy cả hai nguyên nhân cùng góp.
- **Bước và quyết định chịu ảnh hưởng:**
  - Thiếu sót diễn giải; không sai số.
  - Ảnh hưởng phạm vi mục thiết kế riêng cho cổng và `verdict` (D17, Q-b), và quyết định thứ tự của Minh (báo cáo §9). Nếu chỉ sửa phần tự tương quan, `verdict` vẫn có thể báo nhầm ở phần lớn cửa sổ giả.
  - Không chặn kết quả T-045.
- **Đề xuất sửa:** A2.

### R3. Một số câu và số không khớp file — KHÔNG CHẶN

- **(a)** `bao-cao.md:154` viết "Mỗi ô RE2-TT chỉ có 5 ca; một ca đổi hạng làm MRR ô đổi tới 0,2."
  - Hàng theo loại lỗi có 6 ca (cpu, delay, disk, loss) hoặc 3 ca (mem, socket) (`theo-loai-loi.json#/R0/RE2-TT|mem/n` = 3).
  - Mỗi ô (root, loại lỗi) có 3 ca: 10 ô × 3 ca, đếm từ `khoi-k/kq.json#/cau_hinh/K-R0/ca/*/o`.
  - Ở hàng 3 ca, một ca đổi hạng làm MRR đổi tới 1/3.
- **(b)** `bao-cao.md:107` ghi p kiểm dấu bị đảo.
  - E1 (cặp E2|E1+E2; P = 8, M = 2): p = 7/64 (`khoi-k.json#/cap/E2|E1+E2/theo_the_gioi/P/bao_kem/p_kiem_dau`).
  - E2 (cặp E1|E1+E2; P = 4, M = 0): p = 1/8.
- **(c)** Bảng §8 (`bao-cao.md:145–151`) ghi TORAI B ở Nezha-OB là 0,000 mà không ghi trạng thái.
  - Thực tế TORAI B là UNSUPPORTED ở 22/22 ca (`results/T-034/bang-baseline.json#/ranking_mode_a/Nezha-OB_main/methods/torai_B/status`); RR = 0 theo WHY-28.
  - Người đọc, kể cả cô, dễ hiểu là TORAI B xếp sai mọi ca.
- **(d)** `bao-cao.md:5` viết "Mọi lượt dùng cho kết quả chạy trên `bbef69dd`".
  - Các lượt Nezha-OB của T1 (`b2-t1-nezha-*`), D1 (`b2-d1-kE1E2-nezha-001`) và D3 (`b2b-d3-*-nezha-001`) có `pha1.json` lúc 16:50–17:27 ngày 31/10. Commit `ec10087a` lúc 17:40. Tức là các lượt này chạy trên `69ef90b6`.
  - Đã so: bản ghi K-E3, K-E1, K-E2 của các lượt này trùng `b5-k16-nezha-001` (chạy sau sửa) ở 22/22 ca, sau khi bỏ `config_id`, `variant`. Phần R0 đã được người làm đối chiếu ở đợt `d45-001`.
  - Chỉ sai câu chữ, không sai số.
- **(e)** Hai trạng thái đã cũ:
  - `bao-cao.md:3` còn ghi người phản biện là Codex (Q-215).
  - `dinh-chinh-cai-dat.md:3` còn ghi "Chưa sửa `src/`. Mọi mục chờ Minh duyệt." ĐC1–ĐC3 đã được duyệt và commit (LOG mục "Tiếp chặng 1 — sửa ĐC1–ĐC3").
- **Bước và quyết định chịu ảnh hưởng:** sai câu chữ và trạng thái. Mục (c) có thể tạo ấn tượng sai khi trình cô. Không chặn kết quả.
- **Đề xuất sửa:** A3.

## Đề xuất của người phản biện

Theo lời Minh, mục này nêu đề xuất cho từng vấn đề. Đây là đề xuất, chưa là lệnh sửa. Minh quyết. Mọi ứng viên kỹ thuật dưới đây là **chưa kiểm**.

### A. Trước khi nghiệm thu T-045 (trong "Phạm vi ghi" của SPEC; người làm làm khi Minh duyệt)

**A1 — cho R1.**
- Mở rộng `results/T-045/scripts/co_che_khoi_k.py` cho cặp E1+E2 → E1+E2+E5. Ghi theo ca và theo ô cả ca tụt lẫn ca lên:
  - RR trước và sau;
  - ở ca tụt: kênh của root bị xóa theo quy tắc nào;
  - ở ca lên: kênh của thực thể rơi xuống sau root bị xóa theo quy tắc nào.
  - Đoạn code ở R1 dùng được ngay. Chạy dưới một phút, chỉ đọc bản ghi đã có.
- Cờ M5 (SPEC T-045:115): đối chiếu ca có cờ M5 với ca có cùng điều kiện (có thực thể bất thường có đường tới root trong G_N) nhưng không đứng trước root. Nếu không làm, ghi rõ "chưa làm" và lý do.
- Viết lại §1 (ý E5), §6.4 và §9.4 theo các số trên:
  - E5 tại E1+E2 làm root tụt ở 8 ca, lên ở 7 ca.
  - Có hai đường:
    - nhóm vòng C′: 3 ca tụt, cùng ô `ts-travel-service|loss`; 1 ca lên;
    - quy tắc lan thường: 5 ca tụt ở 3 ô; 6 ca lên.
  - Phần hại ròng chia gần đều giữa hai đường.
  - Bỏ chữ "chủ yếu"; bỏ "đúng điều kiện thất bại CĐ3" khỏi vai trò giải thích chính; cơ chế giữ OPEN.
  - Thêm một quan sát: E5 đạt mục tiêu hẹp của nó (số ca có cờ M5 giảm từ 8 xuống 5: `khoi-k.json#/cau_hinh/K-E1+E2/ca_M5_P` và `#/cau_hinh/K-E1+E2+E5/ca_M5_P`) nhưng vẫn gây HẠI gộp.
- Mặt trái: không có; chỉ thêm bảng và đổi lời.

**A2 — cho R2.**
- Thêm vào §1 và §9.1 nguyên nhân cấu trúc: quy tắc "một đơn vị là đủ", khoảng 767 phép chấm mỗi cửa sổ, không hiệu chỉnh; dẫn SPEC T-043:290 và hai số ở R2.
- Dẫn mô phỏng SPEC T-043:415 cạnh số đo 0,935 và 31,6%. Ghi rõ mẫu hệ số chọn theo cờ.
- Sửa §3 và §10 (tiêu chí 2): "bất biến đạt; cờ QT5 đã truy tới giả định độc lập của cổng (B1.3) gặp dữ liệu tự tương quan; chưa sửa; Minh hoãn theo D17 Q-b".

**A3 — cho R3.**
- Sửa năm chỗ (a)–(e).
- Ở `dinh-chinh-cai-dat.md`, thêm dòng trạng thái: ĐC1–ĐC3 đã duyệt (lời Minh 31/10/2026, dòng DECISIONS Q-216 đang chờ ghi), commit `ec10087a`, `eb14262a`, `bbef69dd`. Giữ phần "Sửa đề xuất" làm lịch sử.

**A4.** Tạo lại manifest; nối LOG; soạn prompt cho lượt kiểm lại. Một lượt kiểm lại ngắn chỉ trên phần sửa là đủ.

### B. Quyết định sau T-045 (ngoài phạm vi T-045)

**B1 — Thứ tự việc. Đề xuất (ii): sửa cổng và `verdict` trước task (2).**
- (i) Mở task (2) ngay trên nền E1+E2, giữ cổng hiện hành.
  - Ưu: nhanh, theo kế hoạch.
  - Nhược: mọi bước của task (2) (K-b, T6, T9, T11, T12, KB) vẫn chấm trên cổng này. Vế mốc giả của luật C tiếp tục không hoạt động ở mọi bước. Nếu sau đó sửa cổng thì phải chạy lại cả khối K lẫn task (2).
- (ii) Mở một task thiết kế ngắn cho cổng và `verdict`. Sau đó chạy lại khối K với luật chọn khối giữ nguyên, rồi mới làm task (2).
  - Chi phí: LOG chặng 1 ước khối K pha 1 RE2-TT khoảng 4,9 giờ máy; chạy song song 4 tiến trình như đợt `d17-002`.
  - Ưu: tránh chạy lại hai lần; vế mốc giả hoạt động lại.
  - Nhược: đổi thiết kế sau khi đã nhìn số dev, nên độ lạc quan của số dev tăng.
- (iii) Khóa như hiện hành. Không đề xuất. `verdict` là đầu ra đã khai (B1.7). B6 đòi khóa "điều kiện của verdict" trước G3. Hiện `verdict` không phân biệt cửa sổ có lỗi.
- **Lý do chọn (ii):** cổng ảnh hưởng cả xếp hạng, không chỉ `verdict`.
  - Ở cửa sổ không lỗi, tầng 1 vẫn chứa 32–50/68 thực thể (`runs/b2-t1-re2-mocgia-001/soi.json#/*/tang/1`).
  - Ở cửa sổ có lỗi, tầng 1 chứa 39–54/68 thực thể (`t1.json#/RE2-TT/theo_ca/*/tang/1`).
  - Suy luận, chưa kiểm: cờ giả làm đông tầng 1, và cung cấp "bên giải thích" cho E5. Vì vậy kết cục của E5, có thể cả E1 và E2, phụ thuộc cổng.
- **Giảm mặt trái của (ii):** chọn cách sửa theo nguyên lý và theo tiêu chí không dùng nhãn (B2); ghi WHY trước khi chạy lại; không đổi luật chọn khối.

**B2 — Phạm vi task thiết kế cổng. Tách hai bài toán.**
- **(a) Cổng của từng đơn vị.** Ảnh hưởng xếp hạng và E5.
  - Mô phỏng ở T-043:415 và số đo của T-045 cùng chỉ về tự tương quan.
  - Ứng viên: chấm trên các khối thời gian không chồng nhau (ví dụ trung bình 10–15 giây); hoặc hiệu chỉnh cỡ mẫu hiệu dụng theo hệ số tự tương quan bậc 1.
  - Điều kiện thất bại: không xử lý được trôi nền; khối lớn làm yếu lỗi ngắn; Nezha-OB (metric 1 phút) có thể không cần sửa.
  - Phương án khác: giữ cổng, chỉ dựa vào biên ε. T4 cho thấy cách này không đủ: siết α hoặc ε, mốc giả vẫn 30/30.
- **(b) Quy tắc `verdict`.** Ảnh hưởng vế mốc giả C-e và đầu ra B1.7.
  - Ứng viên: kiểm soát sai theo cửa sổ trên toàn bộ phép chấm (Holm hoặc Benjamini–Hochberg), chỉ áp cho `verdict`, để không đổi tầng và thứ hạng.
  - Phương án khác: áp hiệu chỉnh cho cả cờ. Cách này đổi luôn thứ hạng và có thể làm mất tín hiệu yếu của root.
- **Tiêu chí chấp nhận khai trước, không dùng nhãn root:**
  - tỷ lệ qua cổng ở cửa sổ không lỗi gần α;
  - tỷ lệ CAUSE_FOUND ở cửa sổ không lỗi dưới một mức Minh đặt trước.
- Nếu dùng cửa sổ không lỗi để chỉnh tham số, phải tách chúng khỏi 30 cửa sổ dùng cho C-e, nếu dữ liệu cho phép. Không tách được thì ghi rõ C-e không còn độc lập.
- Không chọn cách sửa theo MRR dev. Ghi WHY trước khi dùng (luật cứng 3).

**B3 — Thang điểm E4 (D24). Đề xuất không đổi D24 lúc này.**
- Không đổi chỉ vì nhánh z cao hơn trên RE2-TT (0,983 so với 0,718 của R0; `t4b.json#/MRR_z`). Lý do:
  - nhánh z mới thử trên R0;
  - ở Nezha-OB gần như không đổi (0,551 so với 0,530);
  - điểm z không bị chặn, lớn nhất 640.830 (`t4b.json#/phan_bo_z`);
  - chọn theo con số này là chọn sau khi nhìn MRR dev.
- Nếu Minh muốn xét lại, làm theo thứ tự:
  1. Đo không nhãn mức bão hòa trên bản ghi R0 đã có: số đơn vị có mọi mẫu A vượt ngưỡng h (B1.3, "Giới hạn bão hòa"); số thực thể tầng 1 hòa ở phần tử đầu của khóa. Việc này rẻ.
  2. Chỉ khi bão hòa phổ biến mới mở thiết kế lại thang, gộp vào task ở B1–B2, và khai tiêu chí chọn trước.

**B4 — E5. Đề xuất giữ tắt theo luật C.**
- Không mở việc sửa riêng quy tắc nhóm vòng C′ (xem R1).
- Chỉ xét lại E5 sau khi đã sửa cổng. Lý do: E5 xóa kênh dựa trên cờ F_raw của bên gọi và bên được gọi. Ở cửa sổ không lỗi, E5 coi 518/1.256 kênh lớp lan là kế thừa (`khoi-k.json#/dau_vet_E5/E1+E2|E1+E2+E5`).
- Với MRP P6 tầng 2: cấu hình thắng vẫn có E1, E2, nên ràng buộc "đồ thị tham gia điểm bất thường" đạt. Riêng cơ chế tách tự sinh và kế thừa (ứng viên chính của tầng 2) hiện chưa có bằng chứng để giữ.

**B5 — E3. Đề xuất giữ tắt.**
- Nếu xét lại, nhắm vào cách chấm ô "mẫu mới", không nhắm vào ngưỡng Drain. Ô này có n_N = 0, nên e = 1 khi có từ 10 dòng, không qua kiểm định (`src/m1/e4.py:191`).
- Lý do: trên RE2-TT, số thực thể có cờ "mẫu mới" ở cửa sổ không lỗi gần bằng ở cửa sổ có lỗi:
  - cửa sổ không lỗi: 83 thực thể, trong 24/30 cửa sổ (`e3-khong-nhan.json#/RE2-TT/tong_hop/a_mg`);
  - cửa sổ có lỗi: 95 thực thể, trong 23/30 cửa sổ (`#/RE2-TT/tong_hop/a`);
  - ngưỡng 0,8 cho 87 ở cửa sổ không lỗi (`#/RE2-TT/tong_hop/a_sim08_mg`).
- Ngưỡng Drain 0,4 và cách khớp (a) chưa có mục WHY. Cần có WHY trước khi dùng trong bản P7 (luật cứng 3).

**B6 — Vị trí so với TORAI B (A4, Q-211).**
- Trên RE2-TT dev, E1+E2 đạt 0,806; TORAI B đạt 0,917 (`theo-loai-loi.json#/thang E1+E2/RE2-TT|tat_ca/MRR`, `#/baseline torai/B/RE2-TT|tat_ca/MRR`).
- Giả thuyết chính A4 so với chính TORAI B trên test RE2-TT.
- Đề xuất:
  - Minh biết số này khi quyết thứ tự.
  - Không dùng khoảng chênh này làm lý do chọn hay sửa thành phần (QT4). Mọi sửa ở B1–B3 phải dựa vào lỗi đã xác minh và ghi WHY.
  - Q-211 mục 8 đã có đường xử lý khi E-04 không đạt.

**B7 — C-d3.**
- C-d3 suy biến theo thiết kế trên dev:
  - Nezha-OB không có span gốc;
  - RE2-TT có chu trình;
  - ở 6 ca, root nằm trong tập đích (fixture 18 của T-043).
- Đề xuất ghi "suy biến: bỏ, ghi lý do" ở task (3), theo bảng ứng viên.
- Quy tắc đơn giản trên cùng đồ thị (MRP P7) vẫn còn C-d1 và C-d2.

**B8 — Ghi sổ.**
- Nội dung đề xuất Q-216–Q-219 và câu sửa SPEC dòng 4 khớp LOG. Tôi không kiểm được lời gốc trong chat.
- Ghi sổ không phụ thuộc lượt phản biện này. Commit nên làm sau khi sửa A1–A3, giữ local các tệp lớn như cách của Q-181.

### C. Đề xuất bổ sung theo mối lo của Minh (ghi theo lời duyệt ngày 01/11/2026)

Hai mối lo của Minh:
1. E1, E2 cải thiện có thể chỉ vì thiết kế đã dựa vào lỗi của baseline trên chính các ca dev.
2. E3, E5 bị loại khi chưa rõ nguyên nhân kém; có thể do dataset công khai.

Mọi ứng viên kỹ thuật dưới đây là **chưa kiểm**. Đây là đề xuất; Minh quyết.

#### C1. E1, E2: dev không phân biệt được "cơ chế thật" với "khớp dev"

**Bằng chứng:**
- **E2 sinh từ chính các ca dev.**
  - Nguồn là G2-H06 và UV-1, quan sát trên 6 ca trễ mạng Nezha-OB dev: root đứng đầu theo span phía gọi ở 5/6 ca; BARO, SimpleRCA, TraceRCA xếp đúng 0, 1, 0 ca (`results/T-034/goi-g2.md:356`).
  - Gói G2 tự ghi: "Định nghĩa vị trí đặt sau khi xem dev" (`goi-g2.md:360`).
- **Phần lợi của E2 rơi đúng vào các ca đó.**
  - 81% phần RR mà E2 thêm (3,91 trên 4,83; cặp E1|E1+E2) nằm ở 3 ô trễ mạng Nezha-OB: `checkoutservice|network_delay`, `emailservice|network_delay`, `recommendationservice|network_delay`.
  - E1+E2 so với R0: 52% phần tăng (4,04 trên 7,80) đến từ 3 ô này.
  - Cách tính: tổng ΔRR theo ô, từ `results/T-045/khoi-k/kq.json`.
- **E1 cũng vậy.** E1 sinh từ UV-2, cũng là phép đo trên dev: "tách được root ở 26/26 ca RE2-TT" (`goi-g2.md:708`). Phần lợi của E1 (cặp E2|E1+E2) nằm chủ yếu ở các ô RE2-TT dev (`ts-train-service|delay`, `ts-train-service|cpu`, `ts-route-service|socket`, `ts-route-service|mem`) và ô `emailservice|network_delay`.
- **Hai giải thích cho cùng một kết quả.** Cả "cơ chế thật" lẫn "khớp dev" đều dự đoán đúng mẫu hình này. Dev không phân xử được.
- **Giải thích khác, chưa kiểm:** E1, E2 có thể chỉ bù cho điểm E4 bão hòa. Nhánh z (không đồ thị, trên R0) đạt 0,983 ở RE2-TT, so với 0,806 của E1+E2 (`t4b.json#/MRR_z`, `theo-loai-loi.json`).
- **Điều làm giảm lo:**
  - E1, E2 dựa trên ý của công trình trước (CRISP, MicroHECL; `docs/KE-HOACH-GIAI-DOAN-TOI.md:231–232`).
  - Không có tham số nào chỉnh theo MRR dev.
  - Luật chọn và ma trận đóng băng trước khi có số của M1 (`results/T-043/ma-tran-thu.json#/trang_thai`).
  - Vậy rủi ro nằm ở "chọn thành phần theo lỗi đã thấy trên dev", không ở "chỉnh tham số theo điểm".
- **Lưu ý:** đối chứng đồ thị ngẫu nhiên đã bỏ (M-25; `docs/KE-HOACH-GIAI-DOAN-TOI.md:49`). Kể cả ở P7 cũng chỉ nói được "lợi ích của phép dùng quan hệ".

**Đề xuất:**
- **A5 (thêm vào gói sửa, chờ Minh duyệt):** báo cáo ghi rõ bằng chứng dev của E1, E2 không độc lập, vì hai lẽ: cấu hình được chọn trong 16 cấu hình; thành phần được thiết kế từ chính các ca dev đó. Kèm các số trên.
- **B-a (hồ sơ G3, task (3)):** khai trước cách đọc phép bỏ E1, bỏ E2 trên test, theo từng dataset, với khoảng tin cậy theo ô (Q-211 mục 4–5):
  - còn lợi và khoảng tin cậy không chứa 0 → "lặp lại trên ô chưa dùng để thiết kế";
  - khoảng tin cậy chứa 0 → "chưa phân biệt được";
  - ước lượng ≤ 0 → "lợi ích dev không lặp lại".
  Khai thêm nhóm con "lỗi trễ mạng" ở test Nezha-OB, vì đó là nhóm E2 nhắm tới. Test chia theo ô khác dev (WHY-04, `docs/WHY.md:48`), nên phép này phân biệt được hai khả năng.
- **B-b (quyết RE3-OB, đang hoãn ở Q-211):**
  - MRP đòi ít nhất một dataset hoàn toàn ngoài thiết kế (`docs/MRP.md:131`); Q-61, Q-68 đã chọn RE3-OB.
  - Đề xuất dùng RE3-OB ở P7, ít nhất cho chuỗi đã khóa và phép bỏ E1, E2.
  - Trình dung lượng trước khi tải (luật cứng 7).
  - Khai trước kỳ vọng, vì RE3 là lỗi mức mã: E1, E2 dựa trên độ trễ, có thể không giúp ở loại lỗi này.
- **B-c:** không cố cải thiện E1, E2 thêm trên dev.

#### C2. E3, E5: bị loại theo luật C, nguyên nhân chưa phân xử xong

Luật C loại theo kết quả, không đòi nguyên nhân. Tách theo ô thì E3, E5 không "kém đều": trong ô mục tiêu, số ô được giúp nhiều hơn số ô bị hại; phần hại nằm ở chỗ khác. Bằng chứng hiện có nghiêng về cách tính của phương pháp hơn là dataset, nhưng chưa phân xử xong.

**E3:**
- Ô mục tiêu (lỗi mã ở Nezha-OB, 4 ô): P = 3, M = 1. Ngoài mục tiêu: M′ = 15 (`khoi-k.json#/cap/R0|E3`).
- 13/17 ca bị hỏng nằm ở RE2-TT, nơi không có lỗi mã (`khoi-k.json#/ca_hong_sua_P/R0|E3`).
- Ở bối cảnh E1+E2, E3 hại cả Nezha-OB: ΔMRR −0,19 (`khoi-k.json#/cap/E1+E2|E1+E2+E3`).
- Bằng chứng không cần nhãn:
  - ô "mẫu mới" bật ở 95 thực thể (23 cửa sổ) khi có lỗi và 83 thực thể (24 cửa sổ) khi không lỗi (`e3-khong-nhan.json#/RE2-TT/tong_hop/a`, `#/RE2-TT/tong_hop/a_mg`);
  - ô này luôn nhận điểm tối đa (`src/m1/e4.py:191`).
- "Dataset kém" đúng một phần: RE2-TT không có lỗi mã, nên E3 không thể cho thấy lợi ích ở đó. Nhưng phần gây hại là cách chấm ô "mẫu mới".
- **Đề xuất:**
  - Ghi E3 là "không vào bản P7; hại do ô mẫu mới; phần còn lại chưa phân xử".
  - Thiết kế lại ô "mẫu mới" theo nguyên lý (có nền, có kiểm định) ở chặng 2, cùng lúc với D7 (thử LLM tách mẫu log), và kiểm trên FlashTicket.
  - Không chọn lại E3 trên dev.

**E5:**
- Ô mục tiêu (20 ô): P = 6, M = 3; ngoài mục tiêu M′ = 1 (`khoi-k.json#/cap/E1+E2|E1+E2+E5`).
- Số ca có cờ M5 giảm từ 8 xuống 5 (`khoi-k.json#/cau_hinh/K-E1+E2/ca_M5_P`, `#/cau_hinh/K-E1+E2+E5/ca_M5_P`), tức E5 đạt mục tiêu hẹp của nó.
- HẠI gộp −0,059; riêng Nezha-OB −0,013, nằm trong ngưỡng δ_d.
- Bốn nguyên nhân ứng viên:
  1. Cổng qua giả tạo ra "bên giải thích" giả. Ở cửa sổ không lỗi, E5 vẫn coi 518/1.256 kênh lớp lan là kế thừa (`khoi-k.json#/dau_vet_E5/E1+E2|E1+E2+E5`).
  2. E5 không xét thứ tự thời gian. Đây là việc của E9, nhưng E9 chưa từng chạy.
  3. Quy tắc nhóm vòng, chỉ ở 1 ô (R1).
  4. Lỗi mất gói tạo triệu chứng ở cả hai đầu cạnh. Đây là đặc điểm của loại lỗi trong dataset; hệ thật cũng có.
- **Hệ quả dây chuyền:** E5 tắt thì E9 (T11) không có việc (`results/T-043/dinh-nghia-pha2.json#/o_kich_hoat/E9/co_che`); T12 mất nơi dùng chính. Tức là E9 bị loại theo E5 mà chưa được thử.
- **Đề xuất:**
  - Hai phép không cần nhãn, trên bản ghi đã có, chỉ để tìm nguyên nhân, không dùng để chọn lại:
    1. đếm số lần E5 xóa kênh mà E9 sẽ phủ quyết (dùng khởi phát đã lưu, quy tắc Đ11 và CĐ9);
    2. đếm số kênh giải thích cũng có cờ ở cửa sổ giả, cùng đơn vị (RE2-TT).
  - Nếu hai phép này giải thích phần lớn các lần xóa gây hại: thử lại E5 cùng E9 sau khi sửa cổng, với luật khai trước.
  - Nếu không: giữ E5 ngoài bản P7, kiểm trên FlashTicket.
  - SPEC task (2) ghi rõ T11 không phân xử được khi E5 tắt.

**A6 (chờ Minh duyệt):** đổi cách ghi "E3, E5 bị bỏ" thành "không vào bản P7 theo luật C trên dev; nguyên nhân chưa phân xử; giữ làm ứng viên". Cách ghi này khớp đoạn cuối MRP P6 (`docs/MRP.md:257`).

**A7 (chờ Minh duyệt):** thêm vào báo cáo bảng ô mục tiêu và ngoài mục tiêu cho E3, E5; chạy hai phép không nhãn của E5 nêu trên.

#### C3. Giữ cân bằng giữa hai mối lo

Mỗi lần thử lại một thành phần trên cùng 52 ca dev là thêm một lần khớp dev, tức lại rơi vào mối lo thứ nhất. Đề xuất:
- ưu tiên các phép không dùng nhãn để tìm nguyên nhân;
- chỉ thử lại tối đa một lần có khai trước, sau khi sửa cổng;
- phần còn lại để dữ liệu mới phân xử: test sau G3, RE3-OB, FlashTicket.

#### C4. Cần Minh quyết

- Có duyệt A5, A6, A7 không. Ba mục này không nằm trong lời "duyệt sửa" A1–A3.
- Có duyệt hai phép không nhãn của E5 không.
- Quyết RE3-OB (B-b) và thứ tự việc sau T-045 (B1).
- Có duyệt chạy A8 (C5) không. Lời Minh ngày 01/11/2026 chỉ duyệt ghi A8 vào bản này.

#### C5. A8 — kiểm nội dung các mẫu log mà E3 phát hiện (ghi theo lời Minh: “duyệt Thêm A8 (kiểm nội dung mẫu E3) vào REVIEW.md. chủ yếu tôi muốn xem các ca log lạ tên là gì, có rõ tên lỗi hay không”)

**Mục đích:** xem các dòng log "lạ" mà E3 đánh dấu thực chất là gì, và có nêu rõ tên lỗi hay không. Phép này trả lời trực tiếp câu "dataset kém hay cách tính kém" cho E3.

**Dữ liệu đã có và còn thiếu:**
- Tên mẫu của kênh "mẫu lỗi", "mẫu thường" đã lưu trong bản ghi pha 1: `extra.thong_ke_log.cap_drain[*].khuon`.
- Ô "mẫu mới" chỉ lưu số dòng (`extra.thong_ke_log.mau_moi`). Muốn xem nội dung phải chạy lại riêng bước Drain của E3 (`src/m1/e3.py`, hàm `hoc_va_dem`) trên log của ca được chọn. Không cần sửa `src`.

**Xem thử một ca mỗi dataset (người phản biện, không dùng nhãn; chưa phải kết luận):**
- RE2-TT, `dev-03d4910932` (cấu hình K-E3): 261/288 mẫu bắt đầu bằng ngày, giờ, mức log, luồng; 64/288 mẫu có cả phần nội dung thành `<*>`.
- Nezha-OB, `dev-14701a3bbb`: 71/71 mẫu mang tiền tố `TraceID: <HEX> SpanID: <HEX>`.
- Giả thuyết (chưa kiểm): phần đầu dòng log nằm trong chuỗi đưa vào Drain (CĐ4.1 dùng `message` nguyên văn), nên mẫu thô; dòng có số token chưa gặp ở nền rơi vào "mẫu mới". Nếu đúng, "mẫu mới" đo độ dài câu log, không đo sự kiện mới.

**Cách làm (khai trước, trước khi xem nội dung):**
1. Chọn ca theo quy tắc cố định: mọi ca root tụt RR khi bật E3 ở cặp (R0, E3) (33 ca, theo `co_che_khoi_k.py`), cộng cửa sổ giả của các ca RE2-TT đó.
2. Với mỗi thực thể vượt lên trên root có kênh mạnh nhất là "mẫu mới" hoặc mẫu Drain: in tên mẫu, và các dòng rơi vào "mẫu mới" gom theo dạng đã che token, kèm số dòng và 3 dòng gốc làm ví dụ.
3. Phân loại tự động theo luật khai trước:
   - (a) có tên lỗi rõ: có từ khóa lỗi (RE2-TT: bộ từ khóa SimpleRCA; Nezha-OB: severity lỗi) hoặc tên ngoại lệ dạng `...Exception`, `...Error`, mã HTTP 4xx/5xx, `timeout`, `refused`;
   - (b) dòng bình thường nhưng hiếm;
   - (c) chỉ khác mẫu nền ở số token hoặc phần đầu dòng;
   - (d) dòng hỏng (rỗng, cắt cụt).
4. So tỷ lệ bốn loại giữa cửa sổ có lỗi và cửa sổ giả; tách bên gọi root với thực thể khác.

**Cách đọc:**
- (a) chiếm nhiều ở bên gọi root → triệu chứng lan thật, log có tên lỗi rõ; E3 cần đi cùng xử lý lan.
- (c) chiếm nhiều → nguyên nhân là cách tách mẫu (một phần do định dạng log của dataset); sửa tiền xử lý theo prior work, ghi WHY.
- (b) chiếm nhiều → cách chấm ô "mẫu mới" thiếu nền.
- (d) chiếm nhiều → vấn đề dữ liệu.

**Chi phí và giới hạn:** dưới 30 phút máy. Đầu ra chỉ để tìm nguyên nhân và thiết kế E3 cho chặng 2; không dùng để chọn lại E3 trên dev. Phân loại là theo luật từ khóa, nên có thể sót tên lỗi viết khác; ghi số dòng không phân loại được.

## Đối chiếu các lượt trước

Chưa có bản phản biện kết quả nào trước. Lượt rà SPEC của Codex (29/10/2026) chỉ có trong chat; không kiểm được.

## Tuân thủ quy trình

- **Phạm vi ghi:** đúng. Người làm chỉ ghi `results/T-045/`, LOG và dòng T-045 trong STATE. `src` chỉ có ĐC1–ĐC3 đã duyệt, mỗi sửa một commit, có test, chưa push.
- **Điểm dừng D17:** đúng. Quyết định của Minh được đặt sau khi xem số T1, có ghi.
- **Nhãn:** lần đọc đầu lúc 01:30:23 (`tai-lap-baseline.json`). Mọi `pha1.json` có giờ tệp sớm hơn; muộn nhất là 01:28.
  - Không kiểm độc lập được giờ ghi dòng hash trong LOG.
  - Toàn vẹn bản ghi vẫn được giữ bằng `pha1.json` và bước kiểm hash trong `pha2.doc`.
- **Seed phép độ bền:** ghi ở LOG lúc "01:34". Lượt bắt đầu khoảng 01:34:23 (giờ tệp `do-ben.json` 01:39:59 trừ 336 giây). Lượt thử trước dùng seed 1, n = 3.
- **Lượt dài:** chạy quá 1 giờ, chạy qua đêm, chạy 4 tiến trình đều có lời Minh duyệt (LOG).
- **Giờ ghi:** LOG và `so-lan-nhin.jsonl` nhiều lần ghi giờ ước sai. Người làm đã nối đính chính; thứ tự việc đúng theo giờ tệp.
- **Trạng thái cũ** ở báo cáo và đính chính: xem R3(e).

## Điều đã kiểm và thấy đúng

- Test: T-045 16/16; T-044 374/374 (code `bbef69dd`, môi trường `results/T-045/scripts/moi_truong.sh`).
- `tao_manifest.py --kiem`: PASS, 6.071/6.071 tệp.
- Chạy lại `pha2_khoi_k.py` ra thư mục ngoài repo:
  - `kq.json`, `kq_mg.json` trùng sha256;
  - mọi khóa của `khoi-k.json` trùng, trừ `giay` và `ca_hong_sua_P` (do `bo_sung_khoi_k.py` thêm sau).
- Chạy lại `do_ben.py --seed 20261101 --n 1000`: trùng mọi trường.
- Luật C, luật chọn khối, bước 8 và bước 10 áp đúng SPEC T-043 (B4, Phụ lục C).
  - 43 cặp: 22 GIÚP, 15 HẠI, 2 KHÔNG TÁC DỤNG, 4 TRÁI CHIỀU.
  - Vế mốc giả "không phân xử được" ở 43/43 cặp.
- Phép độ bền đúng SPEC T-045 bước 7: lấy mẫu ô trong từng dataset; ghép cặp; E_X và nhóm "ít ca" giữ cố định; mốc giả tính theo bội số.
- D2 khớp 12/12. Số ở §1, §3, §5, §6.2, §7 khớp file.
- Bản ghi Nezha-OB chạy trước sửa trùng bản ghi sau sửa (K-E3, K-E1, K-E2: 22/22 ca).
- R0 không dùng quan hệ trong điểm và xếp hạng.
- C-d3 có trạng thái OK mà RR = 0 là hành vi đã khai, không phải lỗi cài đặt.

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm gì:** soát toàn bộ kết quả T-045 theo SPEC và mục tiêu nguồn; chạy lại các phần rẻ; đối chiếu E5 theo từng ca; nêu đề xuất cho từng vấn đề theo lời Minh.
2. **File đã thay đổi:** chỉ tạo `tasks/T-045-chay-khoi-k-dev/REVIEW.md` (bản này). Các file tạm (kết quả chạy lại, script đối chiếu) nằm trong scratchpad của phiên phản biện, ngoài repo; chúng không phải nguồn. Đoạn code ở R1 đủ để dựng lại số.
3. **Kiểm đã chạy và kết quả:** như mục "Điều đã kiểm và thấy đúng"; cộng phép đối chiếu E5 theo ca ở R1 và phép so bản ghi Nezha-OB trước và sau sửa ở R3(d). Không chạy lại pha 1 vì tốn nhiều giờ máy.
4. **Bất đồng, câu hỏi mở và điều cần Minh quyết:**
   - Bất đồng có bằng chứng với báo cáo: R1 (cơ chế E5), R2 (nguyên nhân báo nhầm của `verdict`).
   - Câu hỏi mở: mức bão hòa của E4 (B3); vị trí so với TORAI B (B6); C-d3 suy biến (B7); hai phiên cùng một mô hình.
   - Cần Minh quyết:
     - có duyệt sửa A1–A3 hay không;
     - thứ tự việc sau T-045 (B1);
     - ghi sổ Q-216–Q-219 và sửa SPEC dòng 4;
     - commit.
   - Lượt này không nghiệm thu task, không mở test, không duyệt commit.

**Đề xuất tiếp tục.** Người làm đáp R1–R3 và các đề xuất A. Sau đó làm một lượt kiểm lại ngắn chỉ trên phần sửa. Lý do: R1 làm sai một kết luận sẽ dẫn quyết định sửa E5, và cách sửa rẻ. Minh quyết.

## Prompt bàn giao cho người làm

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-045, tasks/T-045-chay-khoi-k-dev/SPEC.md; toàn bộ bước 0 → bước 8, xong ngày 01/11/2026.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: P6 (M1); chuẩn bị G3.
- Người làm và người phản biện chính thức: người làm Claude (phiên 1 của T-045); người phản biện chính thức là một phiên Claude mới độc lập với phiên người làm, theo lời Minh trong chat ngày 01/11/2026 (LOG T-045 mục "Đổi người phản biện chính thức"; SPEC dòng 4 và Q-215 còn ghi Codex).
- Tài liệu gốc: tasks/T-045-chay-khoi-k-dev/SPEC.md; tasks/T-045-chay-khoi-k-dev/LOG.md (phiên 1); results/T-045/bao-cao.md; tasks/T-043-thiet-ke-rca-m1/SPEC.md (B1–B4, Phụ lục C, D); results/T-043/ma-tran-thu.json; results/T-043/dinh-nghia-pha2.json; results/T-043/ks16/dem-khong-nhan.json, ks16/runs/pha1-002/dem-khong-nhan.json, ks16/dem-sau-ghep-nhan.json; results/T-044/bao-cao.md; results/T-044/dinh-chinh-cai-dat.md; git diff 69ef90b6 bbef69dd -- src/ (ba commit sửa ec10087a, eb14262a, bbef69dd). Nguồn là file trong repo; không dùng transcript, lịch sử chat hay bộ nhớ của các phiên trước (AGENTS mục 4).
- Phản biện và phản hồi trước: tasks/T-045-chay-khoi-k-dev/REVIEW.md (lượt 1 của người phản biện chính thức, ngày 01/11/2026, gồm mục C "Đề xuất bổ sung theo mối lo của Minh"). Lượt rà SPEC của Codex ngày 29/10/2026 nằm trong chat (SPEC dòng 3).
- Code và kết quả liên quan: src/m1, src/m1_danh_gia ở commit bbef69dd; results/T-045/ (manifest.json; dinh-chinh-cai-dat.md; so-lan-nhin.jsonl; t1.json, doi-chieu-ks16.json, e1-cp.json, e3-khong-nhan.json, nhom-vong.json, tai-lap-baseline.json, khoi-k.json và khoi-k/, co-che-khoi-k.json, t4.json, t4b.json, theo-loai-loi.json, do-ben.json; scripts/; tests/; runs/). Kết quả, LOG, STATE chưa commit, và bản ghi lớn trong runs/ chỉ giữ local: làm trực tiếp trên thư mục D:\RCA-flashticket (branch claude/sweet-hawking-dy078d), không dùng worktree mới. Môi trường: source results/T-045/scripts/moi_truong.sh; lệnh dựng lại ở bao-cao.md mục 12; test: cd results/T-045/tests và cd results/T-044/tests, $PY -B -m pytest -q -p no:cacheprovider. Dữ liệu dev theo data/README.md.
- Phạm vi ghi được Minh cho phép trong lượt này: Minh duyệt sửa A1–A3 ở tasks/T-045-chay-khoi-k-dev/REVIEW.md (lời Minh trong chat ngày 01/11/2026: “duyệt sửa”). Được ghi: results/T-045/bao-cao.md, results/T-045/dinh-chinh-cai-dat.md, results/T-045/scripts/co_che_khoi_k.py và đầu ra results/T-045/co-che-khoi-k.json, results/T-045/manifest.json; mục mới cuối tasks/T-045-chay-khoi-k-dev/LOG.md; bảng "Phản hồi của người làm" ở cuối tasks/T-045-chay-khoi-k-dev/REVIEW.md; dòng T-045 trong docs/STATE.md. Các đề xuất khác trong REVIEW.md (A5–A7, mục B, mục C) chưa được duyệt sửa: chỉ trả lời và đề xuất trong chat.

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

## Phản hồi của người làm (người làm điền sau)

Người làm chỉ điền bảng này và LOG trong quyền được duyệt; không sửa nhận xét hay prompt của người phản biện. Thêm N1, N2… cho điểm tự tìm được, nêu CHẶN/KHÔNG CHẶN và bằng chứng. Để trống cột Minh quyết. Prompt của lượt đáp nằm trong mục LOG mới hoặc chat.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R1 | Đúng. CHẶN kết luận cơ chế E5; không chặn lựa chọn E1+E2 | Tự chạy lại độc lập (script tạm `kiem_r1.py`, rồi `results/T-045/scripts/co_che_bo_sung.py` → `co-che-bo-sung.json#/A1_E5_theo_ca`): 8 ca tụt (3 qua nhóm vòng, cùng ô `ts-travel-service\|loss`; 5 qua quy tắc thường, 3 ô), 7 ca lên (1 nhóm vòng, 6 thường); ròng nhóm vòng −1,47, quy tắc thường −1,62; tổng −3,09/52 = −0,0594, khớp `khoi-k.json`. Logic đúng: E5 chỉ xóa kênh, nên root tụt chỉ khi root mất kênh, lên chỉ khi thực thể đứng trước mất kênh. Đã sửa theo A1: báo cáo mục 1, 6.4, 9 ý 4. Còn mở: cơ chế E5 (OPEN). | |
| R2 | Đúng. KHÔNG CHẶN | Kiểm: `src/m1/xep_hang.py` hàm `verdict` (CAUSE_FOUND khi tầng 1 không rỗng); SPEC T-043 dòng 290 và 415 đúng như dẫn; `t1.json#/RE2-TT/moc_gia/cong` cộng ra 23.013 phép; `t4.json#/cau_hinh/T4-e0.05-a0.001/moc_gia/kenh_co_theo_nhom` cộng ra 1.829; `ac1_N_trung_vi` = 0,935. Gọi "do dữ liệu" là phân loại sai theo luật cứng 17. Đã sửa theo A2: mục 1, 3, 9 ý 1, 10 tiêu chí 2. | |
| R3 (a) | Đúng. KHÔNG CHẶN | Trùng điểm tự tìm N2 (ghi LOG trước khi mở REVIEW). `theo-loai-loi.json#/R0/RE2-TT\|*/n` = 6, 6, 6, 6, 3, 3. Đã sửa mục 8. | |
| R3 (b) | Đúng. KHÔNG CHẶN | Trùng N3. `khoi-k.json#/cap/E2\|E1+E2/theo_the_gioi/P/bao_kem/p_kiem_dau` = 7/64 (E1). Đã sửa mục 6.3. | |
| R3 (c) | Đúng. KHÔNG CHẶN | Trùng N1. `results/T-034/bang-baseline.json#/ranking_mode_a/Nezha-OB_main/methods/torai_B/status` = {UNSUPPORTED: 22}. Đã sửa bảng mục 8 và thêm chú thích. | |
| R3 (d) | Đúng. KHÔNG CHẶN | `pha1.json` của các lượt Nezha-OB T1, D1, D3 ghi lúc 16:50–17:16 ngày 31/10; commit `ec10087a` lúc 17:40:33. Tự so lại (script tạm `kiem_r3d.py`): K-E1, K-E2, K-E3 và R0 trùng `b5-k16-nezha-001` ở 22/22 ca sau khi bỏ `config_id`, `variant`. Chỉ sai câu chữ. Đã sửa đầu báo cáo. | |
| R3 (e) | Đúng. KHÔNG CHẶN | Trùng N5, N6. Đã sửa dòng người phản biện ở đầu báo cáo; nối mục "Trạng thái" cuối `dinh-chinh-cai-dat.md`, giữ chữ cũ. | |
| A1 | Đúng; đã làm | Gồm: bảng theo ca và ô cả ca tụt lẫn ca lên; đối chiếu ca có điều kiện tương ứng (26 ca root mất kênh: tụt 8, không đổi 14, lên 4); đối chiếu cờ M5 (E1+E2: 37 ca có điều kiện, M5 ở 8; E1+E2+E5: 33 và 5). Phép M5 đã làm, không phải "chưa làm". Mọi số ở `co-che-bo-sung.json`. | |
| A2 | Đúng; đã làm | Như R2. | |
| A3 | Đúng; đã làm | Như R3 (a)–(e). | |
| A4 | Đúng; đã làm | Manifest tạo lại và `--kiem` PASS; LOG phiên 2; prompt kiểm lại ở cuối LOG. | |
| A5 (mục C1) | Đúng; đã làm | Kiểm lại số: 3,91/4,83 = 81%; 4,04/7,80 = 52% (`co-che-bo-sung.json#/A5_dRR_theo_o`, tính từ `khoi-k/kq.json`); `goi-g2.md:356`, `:360`, `:708`; `KE-HOACH-GIAI-DOAN-TOI.md:231–232`; `ma-tran-thu.json#/trang_thai`. Đã thêm mục 1 (suy luận) và mục 9 ý 8. | |
| A6 | Đúng; đã làm, có chỉnh chữ | "Giữ làm ứng viên" khớp MRP P6 (`docs/MRP.md:257`). Người làm thêm "chưa có quyết định thử lại (Minh quyết)" để câu không thành cam kết thử lại. Đã sửa mục 1, 9 ý 3, 4 và dòng STATE. | |
| A7 và hai phép không nhãn của E5 (mục C2) | Đúng; đã làm. Mục C2 về E5: đúng một phần | Bảng ô mục tiêu ở báo cáo mục 6.6. **Phần đúng một phần:** câu "trong ô mục tiêu, số ô được giúp nhiều hơn số ô bị hại; phần hại nằm ở chỗ khác" đúng với E3, sai với E5 tại E1+E2: P = 6 > M = 3 nhưng ΣΔRR trong ô mục tiêu là −1,49 (RE2-TT −2,80), 6/8 ca tụt nằm trong ô mục tiêu (`#/A7_o_muc_tieu`, `#/A1_E5_theo_ca/ca`). **Hai phép không nhãn:** E9 phủ quyết 17/1.055 lần xóa ở cửa sổ thật và 0/20 kênh root ở ca tụt, kể cả khi bỏ miễn trừ CĐ9; kênh giải thích có cờ ở cửa sổ giả: 10,7% mọi cặp, 4,0% ở các lần xóa kênh root của ca tụt (`#/A7_E9_phu_quyet`, `#/A7_giai_thich_co_o_moc_gia`). Theo nhánh khai trước của C2, hai phép này không giải thích phần lớn các lần xóa gây hại. Ứng viên (4) "lỗi mất gói có triệu chứng ở cả hai đầu" khớp việc 5/8 ca tụt ở ô `loss` của RE2-TT, nhưng chưa kiểm. | |
| B-a | Đúng hướng; ngoài phạm vi T-045 | Thuộc hồ sơ G3, task (3). Minh quyết. Gói quyết định ở LOG phiên 2. | |
| B-b | Đúng hướng; ngoài phạm vi T-045 | `docs/MRP.md:131` đòi ít nhất một dataset hoàn toàn ngoài thiết kế; Q-211 đang hoãn RE3-OB. Dung lượng tải chưa trình. Minh quyết. | |
| B-c, C3 | Đúng | Không cố cải thiện E1, E2 thêm trên dev; ưu tiên phép không nhãn; thử lại tối đa một lần có khai trước. Minh quyết. | |
| A8 (C5) | Đúng; đã làm | Kết quả (`results/T-045/e3-noi-dung-mau.json`; báo cáo mục 6.7; 57/57 cửa sổ tái lập đúng bản ghi K-E3): dòng "mẫu mới" của chính root có tên lỗi hoặc là ngoại lệ (Nezha-OB 99,8% có tên lỗi; RE2-TT 90% là dòng khung ngăn xếp). Dòng của thực thể vượt lên trên root gần như không có tên lỗi (RE2-TT 0,4%; Nezha-OB 0%): RE2-TT chủ yếu loại (c) 90,5% (dòng INFO có danh sách dài thay đổi), Nezha-OB chủ yếu loại (b) 79% (dòng nghiệp vụ mang mã sản phẩm không bị che); cùng dạng với cửa sổ giả (RE2-TT loại (c) 93,5%). Theo cách đọc khai trước của C5: nguyên nhân thuộc cách tách mẫu (một phần do định dạng log của dataset) và ô "mẫu mới" thiếu nền. Hai mô tả thêm sau khi xem lượt 001 (tách root; đếm khung ngăn xếp) ghi rõ là thêm sau, không đổi luật chọn ca hay phân loại. Giới hạn: luật từ khóa có thể sót tên lỗi; khung ngăn xếp không mang tên lỗi trên từng dòng. | |
| B1 | Đúng một phần; ngoài phạm vi T-045 | Lý lẽ đúng: cổng ảnh hưởng cả tầng 1 và xếp hạng; B6 T-043 đòi khóa điều kiện `verdict` trước G3, nên (iii) không khả thi. Bổ sung: (1) chi phí "4,9 giờ máy" là ước lượng chạy tuần tự của chặng 1; đợt `d17-002` chạy 4 tiến trình mất khoảng 2,4 giờ thực cho 510 đơn vị; (2) nếu cả cổng (B2) lẫn thang điểm (B3) có thể đổi, quyết cả hai trong cùng một task thiết kế để chỉ chạy lại khối K một lần; (3) phương án tách, chỉ sửa quy tắc `verdict` trước: không đổi tầng và thứ hạng; bản ghi lưu p của mọi đơn vị phân vị (`extra.don_vi_phan_vi`), nên có thể tính lại `verdict` từ bản ghi; đơn vị đếm chưa kiểm. Minh quyết. | |
| B2 | Đúng; ngoài phạm vi T-045 | Đồng ý tách (a) cổng từng đơn vị và (b) quy tắc `verdict`. Nezha-OB không có mốc giả (D6), nên tiêu chí không nhãn chỉ đo được trên RE2-TT. Minh quyết. | |
| B3 | Đúng; ngoài phạm vi T-045 | Đồng ý không đổi D24 lúc này. Phép đo không nhãn mức bão hòa rẻ; nên làm trong cùng task thiết kế với B2 nếu Minh chọn B1 (ii). Minh quyết. | |
| B4 | Đúng | Bằng chứng mới ở A7 ủng hộ: không mở việc sửa riêng nhóm vòng; E9 không cứu kênh root nào ở ca tụt. | |
| B5 | Đúng | Kết quả A8 bổ sung căn cứ (dòng A8). Ngưỡng Drain 0,4 và cách khớp (a) chưa có WHY; vì E3 không vào bản P7, WHY chỉ cần khi thử lại E3. | |
| B6 | Đúng | Trùng điểm tự tìm N8. Không dùng để chọn (QT4). Đưa vào gói quyết định cho Minh. | |
| B7 | Đúng | Tự kiểm (script tạm `kiem_cd3.py`): ở cả 6 ca C-d3 OK, root nằm trong tập đích và không là ứng viên, ở K-R0 và K-E1+E2. Giải đáp điểm tự tìm N7. | |
| B8 | Đúng | Câu chữ đề xuất Q-216–Q-220 và SPEC dòng 4 ở LOG phiên 2. | |
| N1 | KHÔNG CHẶN; trùng R3 (c) | Đã sửa cùng A3. | |
| N2 | KHÔNG CHẶN; trùng R3 (a) | Đã sửa cùng A3. | |
| N3 | KHÔNG CHẶN; trùng R3 (b) | Đã sửa cùng A3. | |
| N4 | KHÔNG CHẶN | Tiêu chí 6 và SPEC bước 2 đòi lệch D1 xử lý qua đính chính; lệch D1 mới được giải thích ở LOG và `doi-chieu-ks16*.json`. Không đổi số. Chưa sửa: không thuộc điểm phản biện; chờ Minh. | |
| N5 | KHÔNG CHẶN; trùng R3 (e) | Đã sửa cùng A3. | |
| N6 | KHÔNG CHẶN; trùng R3 (e) | Đã sửa cùng A3. | |
| N7 | KHÔNG CHẶN; đã có lời giải | B7 và phép kiểm `kiem_cd3.py`: 6/6 ca OK có root trong tập đích. Đề xuất thêm một câu vào báo cáo mục 6.5; chờ Minh. | |
| N8 | KHÔNG CHẶN; trùng B6 | Đề xuất thêm một dòng quan sát vào mục 1 và 9 (không dùng để chọn); chờ Minh. | |
| N9 | KHÔNG CHẶN | Câu "cờ ở cấu hình thắng: TRÁI CHIỀU 12" hẹp hơn đại lượng tính (gồm cả cờ ở cấu hình có MRR cao hơn). Chờ Minh. | |
| N10 | KHÔNG CHẶN | Bước 10 không phân biệt được trên dev: MRR ở S_lo, S_hi trùng P ở cả 16 cấu hình, cả hai dataset. Chờ Minh. | |
| N11 | KHÔNG CHẶN | `so-lan-nhin.jsonl` thiếu vài lần xem của phiên 1 (status, hash; lượt đo giờ phép độ bền). Không lần nào đứng trước quyết định chọn. Chờ Minh. | |
