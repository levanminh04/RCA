# Phản biện T-063 — hồ sơ trước lượt thu chính dev bản 2

- **Người phản biện:** Codex. **Ngày:** 13/11/2026. **Commit/diff đã đọc:** HEAD `c3d27f8a`; đầu ra T-063 chưa commit; diff các tài liệu sống liên quan và file thật của gói.
- **Công đoạn/cổng và bản lượt:** soát kết quả trước lượt dài theo luật 21, M1→M2 của chiến dịch M1-FlashTicket. Bản đầu `REVIEW.md`, theo quyền trong brief. Claude làm; Codex phản biện.
- **Đã đọc:** AGENTS; STATE; SPEC/LOG T-063; hồ sơ chiến dịch; MRP mục tiêu/RQ; DT18 và hướng dẫn cô; LESSONS; DECISIONS phần chiến dịch và quyền bổ sung; WHY-81..84; hồ sơ lượt, thiết kế runner, lịch; hồ sơ/script đóng băng; runner2/inj2; exporter bổ sung, bảng tín hiệu, sổ thay đổi máy; phân tích CPU/ca nền/span gốc; gói R, D2 và sổ tiêm; stage/run/safe-export ghim T-058; tiêu chí T-064; code tải, bàn giao sau bảo trì và manifest L1 bổ sung. Sau tự soát mới đọc REVIEW-PL2.
- **Tự soát độc lập:** lần đường tải → tiêm/đầu dò → phục hồi → stage → M1 → xuất/nhận; kiểm pin trước dùng. Hai mô phỏng chỉ trong bộ nhớ xác nhận nhánh dọn lỗi vẫn sang ô sau và nhánh đầu dò báo không pause vẫn xếp M1. Đối chiếu độc lập bằng chứng tích hợp cuối trước khi đọc kết luận tải liên quan.

## Kết luận chung

**Chưa đề nghị phát lượt dài bằng bản runner hiện tại:** R1 và R2 chặn bước này. Hồ sơ đã khai lịch, chi phí và tình huống 10/50/99%, nhưng đường phục hồi chưa giữ phạm vi lỗi như mô tả và thiếu bằng chứng tích hợp trên cấu hình cuối. Đây là kiểm chuẩn bị dữ liệu áp dụng FlashTicket; chưa nghiệm thu toàn T-063, chọn M1-FT hay trả lời hiệu quả đồ thị/RQ5.

## Các điểm

### R1. Dọn can thiệp thất bại vẫn phát ô sau — CHẶN

- **Ở đâu:** `results/T-063/chay/runner2.py:81`, `:188`, `:198`; `results/T-063/tiem-loi/inj2.py:102`, `:106`, `:172`; HO-SO-LUOT bảng xử lý lỗi.
- **Sai gì:** ngoại lệ trong chu kỳ gọi cleanup, nhưng ngoại lệ cleanup bị bỏ qua rồi phát chu kỳ kế tiếp. Ngay khi SSH thành công, cleanup vẫn có thể hỏng: `inj2.cleanup()` bắt lỗi từng ô và chỉ in `cleanup-error`; `runner2.inj()` lấy JSON cuối, bỏ các lỗi trước. Xóa toxic lỗi vẫn in `stop`; `docker unpause` dùng `check=False`. Không xác nhận trạng thái sạch trước ô sau.
- **Bằng chứng:** mô phỏng A cho `stop` và `cleanup` cùng lỗi. Trace vẫn có `cycle-error → cycle-end → cycle-begin → mark → m1-queued` ở ô BINH-THUONG sau PAUSE-PAYMENT. Kết quả `second_cycle_started_after_cleanup_failure=true`. Đây là lỗi logic điều phối đã tái hiện; chưa khẳng định có ca thu chính bị nhiễm.
- **Phạm vi thực:** toxic không có hạn tự hết trong `inj2.start`; pause chỉ ghi `.pause-deadline`, không có đoạn đọc/thực thi deadline trong bộ tiêm/bộ chạy được trình. Lỗi có thể còn ở nền ô kế tiếp. CPU có timeout, hook có lease: giảm rủi ro hai nhánh này, không bảo vệ toxic/pause. Việc có gọi cleanup chưa bác bỏ finding vì chưa chứng minh cleanup thành công.
- **Bước và quyết định chịu ảnh hưởng:** chặn phát bản hiện tại và bảo đảm lỗi tiêm chỉ mất một chu kỳ/30 phút. Lỗi nguồn/hạ tầng được phép dừng lượt theo luật 21. Nếu cố chạy tiếp, nhiều cửa sổ sau, gồm ca khỏe, có thể hỏng rồi bị diễn giải thành tính chất phương pháp.
- **Đề xuất sửa tối thiểu:** truyền đủ kết quả/mã lỗi dọn; xác nhận không còn toxic/pause/burn/hook trước phát ô sau. Dọn không xác nhận được thì dừng phần phụ thuộc môi trường ấy, giữ dữ liệu và ghi khoảng ảnh hưởng. Khai đúng hành vi mất bộ điều khiển và ý nghĩa `--seconds` đối với pause/toxic; ghi deadline không tự là phục hồi. Không yêu cầu hệ thống điều phối mới. Code sửa làm đổi pin; xem bản đồ ảnh hưởng.

### R2. Thiếu bằng chứng tích hợp cuối cho R và đường đóng gói/phục hồi — CHẶN

- **Ở đâu:** SPEC bước 6–9 và phần bổ sung; chiến dịch mục 7; `results/T-063/kiem-r/BAO-CAO.md:21`; `results/T-063/dong-goi/README.md`; LOG mục khóa đợt thu.
- **Sai gì:** trước phát lượt chính, SPEC/chiến dịch yêu cầu xác nhận tải, quan sát, đóng gói, phục hồi, lịch đầu dò trên cấu hình cuối. Hồ sơ chưa chứng minh đủ. Không kết luận hệ thống đã sai; thiếu bằng chứng bắt buộc để chuyển M1→M2.
- **Bằng chứng:** gói R duy nhất trong `results/T-063/kiem-r/` là `krb4a3d5`, `cases/krb4a3d5/request.json#/t = 1794524225`, trước bảo trì TD-04..08. Báo cáo tự ghi còn kiểm lại sau bảo trì. R-07 còn CHƯA KIỂM; R-05 mới một phần. Đóng băng ghi cấu hình/hash, không có kết quả R tích hợp thay thế.
- **Phần có thể phản bác:** L1 có giao dịch/pilot sau bảo trì; exporter đã có thử 24 kênh không lỗi khúc (`dong-goi/thu/bo-sung-1794535812.json`). Chúng xác nhận phần tải và xuất metric, không thay R-04/R-09 toàn gói sau đổi lọc/log/span job. File thử khai `phien_ban=T063-bo-sung-2`, còn exporter khóa là bản 3. Không thấy biên bản hoàn tất wrapper stage→M1→safe-export→nhận gói/bổ sung bản 3, hoặc phép kiểm thư mục đã tồn tại theo SPEC. README còn ghi wrapper/phục hồi/chống trùng là chưa làm; code đã có nên finding là thiếu bằng chứng kiểm, không phải chưa cài.
- **Bước và quyết định chịu ảnh hưởng:** chặn xác nhận nền thu sẵn sàng. Lỗi quan sát sau đổi Collector có thể thành dữ liệu chọn phương pháp; lỗi wrapper có thể lộ sau nhiều giờ. DT18 cần log/trace/metric ánh xạ đúng lên đồ thị; tải chạy được chưa đủ chứng minh phần này.
- **Đề xuất sửa tối thiểu:** dùng lại cửa sổ sạch của pilot L1 sau bảo trì đã lưu, xuất/kiểm R và đường đóng gói cuối; không chạy lại hai lượt tải hay đợt 6,5 giờ. Tách R-05 giới hạn cũ khỏi hỏng do thay mới; không đòi sửa hết B16. Kiểm đường phục hồi/trùng thư mục bằng ca hoặc mô phỏng phù hợp trong quyền, giữ lần lỗi; kiểm hash, lỗi khúc, hai kết quả P7. Ghi bằng chứng/thời gian. Ước theo hồ sơ là phút/gói, chưa là số đo của phép kiểm này. Nếu bằng chứng nằm nơi khác, chỉ rõ và kiểm hợp lệ thay vì chạy lại.

### R3. Đầu dò không xác nhận chưa dẫn tới trạng thái như hồ sơ — KHÔNG CHẶN riêng lượt thu

- **Ở đâu:** HO-SO-LUOT tình huống 10%; `runner2.py:174`–`:190`; tiêu chí chọn T-064 mục 1.
- **Sai gì:** hồ sơ nói “tiêm không lên / đầu dò không xác nhận” dẫn tới `fault-start-failed`/`m1-skipped`. Code chỉ đặt `fault_ok=False` khi start ném ngoại lệ; probe chỉ được lưu, không phân loại hiệu lực từng ca.
- **Bằng chứng:** mô phỏng B cho start thành công nhưng mọi probe báo `payment_state='running false'`, không toxic/burn. PAUSE-PAYMENT vẫn `m1-queued`, không `m1-skipped`.
- **Giới hạn finding:** `m1-queued` không đồng nghĩa vào tập chọn. Tiêu chí T-064 đã cấm ca không xác nhận và yêu cầu danh sách mã mờ trước chấm. Có thể giữ gói/M1 chẩn đoán rồi xác nhận hậu kỳ; không cần chặn thu hay bỏ dữ liệu. Chưa có bằng chứng nhãn sai vào chấm.
- **Bước và quyết định chịu ảnh hưởng:** không coi mọi start thành công là can thiệp được xác nhận; không dự toán thu bù chỉ từ `fault-start-failed`. Chặn dùng ca chưa xác nhận vào tập chọn.
- **Đề xuất sửa:** phân loại probe trong runner theo điều kiện khai trước, hoặc sửa hồ sơ nói xác nhận hậu kiểm và lưu kết quả từng mã mờ trước T-064. Tôi đề xuất hậu kiểm trên sổ nếu đủ tín hiệu, vì không thêm truy vấn trong cửa sổ phương pháp. Mặt trái: phải dự trù thu bù sau kiểm; ĐẠT D2 không thay xác nhận mỗi lần thu. Nhãn/xác nhận ở phía điều khiển/chấm, không đưa vào M1.

### R4. ĐẠT hai ô CPU chưa khớp trọn điều kiện khai trước — KHÔNG CHẶN thu theo số luồng

- **Ở đâu:** `results/T-063/o-dev-bo-sung.md:11`–`:12`; D2B-KET-QUA; `chay/d2b-d2b-2a7f481a-danh-gia.json`.
- **Sai gì:** khai trước CPU-BOOK-2 throttle ≥80%; CPU-BOOK-1 CPU ~1 lõi, throttle thấp, PSI máy tăng ≤×2. D2 gọi cả hai ĐẠT từ số luồng/throttle, chưa tách xác nhận cách tiêm khỏi đạt điều kiện phân xử cơ chế.
- **Bằng chứng:** JSON `#/ket_qua/CPU-BOOK-2/prom/booking_throttle_ratio/loi/tb = 0.7227`; CPU-BOOK-1 cùng con trỏ = `0.1546`. `burn_procs` tương ứng 2/1; delta `nr_throttled` 804/171. Probe chỉ có pressure cgroup Booking, thiếu PSI CPU toàn máy tương ứng cho điều kiện ≤×2. Số đọc bằng PowerShell trên hai khóa CPU. Tác giả cũng đã khai tải D2 hết sớm; không coi số này xác nhận đầy đủ điều kiện dưới tải mua vé.
- **Phần có thể phản bác:** số luồng/throttling xác nhận can thiệp thật; 72% không chứng minh tiêm thất bại. Thử cũ không k6 đã ghi giới hạn. Không cần lặp để đạt số đẹp; bằng chứng cũ cũng không thay số đo dưới tải mới.
- **Bước và quyết định chịu ảnh hưởng:** không chặn thu công thức 1/2 luồng. Chưa đủ gọi CPU-BOOK-1 là đối chứng ít nhiễu toàn máy hoặc quy chênh M1 riêng cho cục bộ/lan theo phụ thuộc.
- **Đề xuất sửa:** ghi ĐẠT cách tiêm; điều kiện cô lập cơ chế chưa xác nhận, ngưỡng cũ chưa thỏa, thiếu PSI nào. Thay tiêu chí sau xem D2 phải khai là sửa sau. Tôi đề xuất giữ hai cường độ và giới hạn diễn giải, không chỉnh quota/luồng theo số đã xem. Muốn khẳng định tách cơ chế dưới tải mua vé cần CPU/PSI máy và trễ tuyến không qua Booking trong cùng điều kiện, đối chiếu với ảnh hưởng tải; chưa chạy trong lượt này.

## Đối chiếu các lượt trước

Không có phản biện T-063 trước. REVIEW-PL2 là bản tải liên quan, không tự là nghiệm thu tích hợp T-063.

| Điểm REVIEW-PL2 | Đánh giá độc lập |
|---|---|
| R1 tunnel/quyền thay máy | **Đúng một phần.** Có code/bằng chứng giới hạn đường mock. Chưa đủ căn cứ gọi thay đổi vượt quyền chỉ từ mô tả rộng/hẹp: quyền bổ sung cho Claude điều phối/triển khai trong chiến dịch. Chưa kiểm thao tác gỡ khóa/tiến trình; không thử gỡ ở phiên chỉ đọc. |
| R2 pilot 503/504 do pause | **Đúng ở mức bằng chứng hiện có.** Plan/sổ D2 pause và lỗi Gateway/Payment pilot trùng khoảng; đường mock gọi Payment tạo đường gây timeout/503. Đủ bác dùng pilot ấy như lượt khỏe đánh giá sau bảo trì. Không suy không có mọi lỗi nền khác. |
| R3 callback bỏ Gateway | **Đúng.** Cấu hình/bàn giao khai đường mock trực tiếp. Giữ giới hạn cạnh callback khi diễn giải; chưa cần thu lại chiến dịch chỉ vì điểm này. |
| R4 20 VU khi lỗi chậm | **Đúng.** Mã k6 ghim maxVUs; chạy khỏe không bảo đảm đủ khi chậm. Hồ sơ đã nhắc dropped từng chu kỳ, runner mới nhận file; có thể phân tích raw/summary trước chọn, không đổi tải sau xem điểm M1. |

Bảng phản hồi L1 còn trống; không tự nhận thay người làm hay suy hai bên đã thống nhất mọi giới hạn.

## Tuân thủ quy trình

- Vai trò REVIEW; chỉ EXECUTE việc tạo bản phản biện. Không LOG/STATE, code/kết quả, commit hoặc gọi agent khác. Không đọc dữ liệu khóa, RCA lưu trữ, env hay nội dung khóa. SSH chỉ đọc; mô phỏng remote không IO thật.
- Quyền chiến dịch bổ sung đã ở DECISIONS/SPEC; chưa commit RCA không chặn theo quyền đó. Không coi H3/H4 thiếu đầu vào là được bỏ mục tiêu.
- R1/R2 ảnh hưởng thực thi/tự kiểm trước chuyển bước. R3/R4 giữ riêng mức bằng chứng; chưa khẳng định có lỗi khoa học ở lượt chính chưa thu. STATE cũ hơn LOG nhưng vẫn cùng task đang làm/phân vai, không mâu thuẫn giao việc.

## Điều đã kiểm và thấy đúng

- Get-FileHash laptop và SSH `sudo sha256sum` đúng danh sách đóng băng: khớp **10/10** mục `#/laptop_file_sha256`, **29/29** mục `#/exp_app_file_sha256`, **9/9** mục `#/exp_obs_file_sha256`. Hash chính hồ sơ khớp LOG; không rải hash dài ở đây.
- Gói R khớp **5/5** file `cases/krb4a3d5/manifest.json#/files`. Sổ tiêm **69 dòng**, không lỗi seq/prev_sha256: SHA-256 từng dòng UTF-8 không gồm newline. Lịch **13** chu kỳ, **4** BINH-THUONG, không có hai ô bị loại.
- Manifest L1 bổ sung: **338/339** mục không khai `mutableRuntime` khớp toàn file; mục còn lại `thay-doi-may.md` khớp **8.444.676 byte tiền tố** đã khai, sau đó nối thêm. **14** mục `mutableRuntime=true` được tách khỏi kiểm bất biến. Hai stderr khóa đọc không được coi đã kiểm toàn file. Đã báo lệch, dừng phần phụ thuộc, rồi kiểm quy ước file sống/tiền tố; chưa thấy bằng chứng thay nguồn tĩnh L1. Không dùng phần nhật ký nối thêm như đã ghim ở manifest cũ.
- Stage/run ghim giữ `mkdir(exist_ok=False)` và kiểm pin. Runner retry mã mới, giữ thư mục cũ; M1 có luồng riêng tuần tự. Thiết kế phù hợp giữ lượt lỗi, chưa thay kiểm tích hợp R2.
- Đường tính M1 đã đọc không nhận tên ô/sổ tiêm; chỉ mốc và gói mã mờ. Đây là mode a theo mốc, không chứng minh tự phát hiện không dùng mốc tiêm.
- D2 giữ lượt tải hết sớm và khai sửa thời lượng. Chọn image hiện hành, thay SLOW-BOOK, nền M1 có lý do WHY; không bắt build/thu lại chỉ vì HEAD ứng dụng đổi.

## Phép kiểm nhánh lỗi đã chạy

Python tại sandbox (`py -3`, venv) không khởi động được. Dùng SSH stdin `python3 -B -` trên exp-obs (Python 3.12.3), source runner là đúng byte laptop đã kiểm pin, truyền base64. Không ghi script lên máy. Top-level runner chỉ định nghĩa hằng/hàm khi `__name__='review_read_only'`. Trước gọi chay_lich đã thay mọi hàm IO/tải/tiêm/timing/thread bằng hàm giả.

Đầu ra chính thực nhận của mô phỏng:

```text
A: second_cycle_started_after_cleanup_failure=true; cleanup_attempted=true
B: hai m1-queued, một fault-start, dù probe báo Payment running false
syntax: AST parse thành công; không tải/tiêm thật
```

Mã tái lập tương đương sau khi đọc source vào biến `source`; trong lệnh thực chạy, source được giải mã từ base64 của runner laptop. Đây là phép kiểm logic, không đo hệ thống:

```python
import json, queue, types
# source = byte runner đã kiểm hash, decode UTF-8
ns = {'__name__': 'review_read_only'}
exec(compile(source, 'runner2.py', 'exec'), ns)
class Plan:
    def read_text(self, **k):
        return json.dumps({'chu_ky':[{'o':'PAUSE-PAYMENT'},{'o':'BINH-THUONG'}]})
    def read_bytes(self): return self.read_text().encode()
class DummyThread:
    def __init__(self, **k): pass
    def start(self): pass
events, calls = [], []
ns.update(Path=lambda p:Plan(), log=lambda *a,**k:None,
    state=lambda **k:None, ledger=lambda e,**k:events.append((e,k)),
    stopped=lambda:False, wait_until=lambda *a:None,
    start_load=lambda *a,**k:100000, finish_load=lambda *a:None,
    ssh=lambda *a,**k:'', M1Q=queue.Queue(),
    threading=types.SimpleNamespace(Thread=DummyThread,enumerate=lambda:[]),
    time=types.SimpleNamespace(sleep=lambda *a:None))
def bad_cleanup(op, cell='-', seconds=None):
    calls.append((op,cell))
    if op in ('stop','cleanup'): raise RuntimeError('simulated SSH outage during recovery')
    return {'op':op,'payment_state':'running false'}
ns['inj']=bad_cleanup
ns['chay_lich']('in-memory')
print('A cycles',sum(e=='cycle-begin' for e,k in events))  # 2
print('A cleanup',('cleanup','-') in calls)  # True
events.clear(); ns['M1Q']=queue.Queue()
ns['inj']=lambda op,cell='-',seconds=None:{
    'op':op,'payment_state':'running false','toxics':{},'burn_procs':'0'}
ns['chay_lich']('in-memory')
print('B queued',sum(e=='m1-queued' for e,k in events))  # 2
```

## Bản đồ ảnh hưởng của đề xuất sửa

Đây là đề xuất, không cấp quyền sửa mới. Gói hơn ba file phải trình danh sách/đầu ra theo quyền đang có; giữ ảnh đóng băng cũ.

| File/nhóm | Sửa đề xuất và ảnh hưởng |
|---|---|
| `chay/runner2.py`, `tiem-loi/inj2.py` của T-063 | Truyền lỗi dọn, xác nhận sạch, dừng khi không phục hồi. Cả hai đã ghim; inj2 có bản remote. Sửa byte đổi pin, phải đồng bộ code thực chạy/hồ sơ mới. Không sửa P7/T-058. |
| `results/T-063/kiem-r/`, `dong-goi/` | Bằng chứng kiểm cuối trên cửa sổ đã lưu, manifest mới; giữ lượt lỗi/gói trước bảo trì. |
| `chay/HO-SO-LUOT.md`, `chay/D2B-KET-QUA.md`, `o-dev-bo-sung.md` | Khai đúng phục hồi, xác nhận hậu kiểm và mức kết luận CPU. Không nằm trong pin đóng băng hiện tại nhưng thay kết luận vẫn cần quyền. Không đổi tiêu chí chọn sau xem điểm. |
| `dong-bang.md`, JSON phiên bản mới trong `dong-bang/`; LOG/dòng STATE nếu cần | Cập nhật tham chiếu sau source/bằng chứng hợp lệ. Giữ JSON khóa cũ, không làm như code sửa đã khóa từ đầu; không lan task khác. |

## Báo cáo lượt và đề xuất tiếp tục/dừng

1. **Đã làm:** soát hồ sơ/code/pin/quyền/mục tiêu nguồn, mô phỏng hai nhánh lỗi, rồi đối chiếu bốn ý REVIEW-PL2.
2. **File thay đổi:** chỉ tạo `tasks/T-063-quan-sat-thu-dev-2/REVIEW.md`. Không thêm quyết định hay sửa LOG/STATE/source/kết quả, không commit.
3. **Kiểm:** hash/gói/sổ như trên; hai phản ví dụ logic tái hiện. Không chạy tải, tiêm, M1 thật hoặc mở dữ liệu khóa. Chưa kiểm tích hợp cuối; không giả định đạt.
4. **Đề xuất cho quyết định:** chưa phát runner hiện tại; Claude đáp R1/R2 và xử lý theo quyền chiến dịch, dùng lại pilot sau bảo trì rồi kiểm phần sửa. Mặt trái: chậm bước kiểm ngắn. Phát ngay có rủi ro hỏng nhiều cửa sổ khi phục hồi lỗi nên không đề xuất. Chưa biết lỗi có xảy ra trong lượt chính vì chưa thu; phản ví dụ logic đã đủ yêu cầu sửa đường điều phối.

**Phần mục tiêu còn mở:** POOL-EVENT và CONSUMER-BOOK-SLOW chưa có can thiệp dev hợp lệ. Đó là thiếu đầu vào phân xử H3/H4, không phải bằng chứng pool/queue vô ích. Pool dưới trễ JDBC không thay cạn pool độc lập; queue không tồn không thay consumer tụt sau. Tôi đề xuất thu các ca độc lập sau xử lý R1/R2, đồng thời trình phần hook kiểm thử còn thiếu để hoàn thiện H3/H4; không tuyên bố H1–H8 hoàn tất từ lịch này. Phương án tăng lưu lượng message giữ hook cũ có thể đổi tải; hook chậm xử lý consumer/cạn pool trực tiếp hơn nhưng cần rõ đường dẫn/quyền sửa/build. Chưa đo chi phí hoặc khẳng định cách nào thành công; phải rà code/đầu ra cũ rồi trình chi phí trước chạy. Không yêu cầu reviewer chạy thêm hoặc chặn mọi ca độc lập vì phần còn mở này.

**Đề xuất tiếp tục phản biện phần chặn sau khi người làm đáp.** Chưa có phản hồi T-063 nên chưa gọi là bất đồng hai bên đã xác lập. Minh quyết sửa/phát/giới hạn. Không tự nghiệm thu task, chọn thiết kế, mở test hay gửi prompt sang agent khác.

## Prompt bàn giao cho người làm

Nguyên văn Prompt chung + khối Người làm đáp phản biện, chỉ điền metadata. Mẫu hiện không có khối riêng M1→M2; không tự thêm cổng hoặc gán mốc này thành G3/G4.
```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-063, tasks/T-063-quan-sat-thu-dev-2/, hồ sơ trước lượt thu chính dev bản 2.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: chiến dịch M1-FlashTicket, M1→M2 theo tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md mục 7.
- Người làm và người phản biện chính thức: Claude làm, Codex phản biện theo SPEC T-063.
- Tài liệu gốc: tasks/T-063-quan-sat-thu-dev-2/SPEC.md và LOG.md; tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md; results/T-063/quan-sat/thay-doi-may.md; results/T-063/o-dev-bo-sung.md; docs/WHY.md; commit gốc c3d27f8a, đầu ra chưa commit.
- Phản biện và phản hồi trước: tasks/T-063-quan-sat-thu-dev-2/REVIEW.md; liên quan tasks/T-062-dem-chang-1-4/REVIEW-PL2.md; chưa có phản hồi T-063.
- Code và kết quả liên quan: results/T-063/chay/, tiem-loi/, dong-goi/, kiem-r/, dong-bang.md và dong-bang/dong-bang.json; results/T-062/tai-2/; results/T-064/tieu-chi-chon.md. Máy exp-app/exp-obs chỉ đọc qua SSH theo results/T-062/chay/runner.py trong lượt đáp này; không chạy tải hoặc tiêm lỗi.
- Phạm vi ghi được Minh cho phép trong lượt này: prompt này đề nghị trả lời trong chat, không tự cấp thêm quyền ghi/sửa. Nếu Minh cho phép ghi phản hồi thì chỉ bảng Phản hồi của người làm cuối REVIEW.md và nối LOG.md của T-063; giữ nguyên nhận xét và prompt reviewer.

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

## Phản hồi của người làm (người làm điền sau)

Người làm chỉ điền bảng này và LOG khi được phép; không sửa nhận xét hoặc prompt. Thêm N1, N2… cho điểm tự tìm được, nêu mức và bằng chứng. Để trống cột Minh quyết. Prompt lượt đáp nằm ở LOG mới hoặc chat theo quyền.

| Điểm | Ý kiến người làm: đúng / đúng một phần / sai / chưa kiểm được; mức | Lý do, bằng chứng, hậu quả và phần còn thiếu | Minh quyết |
|---|---|---|---|
| R1 | **Đúng; CHẶN — đã sửa.** | Tự soát trước khi đọc kết luận: `runner2.inj()` lấy JSON cuối nên bỏ `cleanup-error` (xác nhận đúng như finding). Sửa: `inj()` ném lỗi khi có `cleanup-error`; `bao_dam_sach()` gọi `verify` trước mỗi chu kỳ và sau mỗi lỗi chu kỳ, dọn một lần, không sạch thì ghi `run-abort-dirty` và dừng lượt; `inj2.py` thêm tiến trình tự hết hạn (`_het_han`, dừng toxic/pause ở hạn +5 s) và `verify`. Bằng chứng: mô phỏng `results/T-063/chay/kiem-sua-R1/mo-phong.txt` (chỉ 1 chu kỳ bắt đầu, rồi `run-abort-dirty`); `results/T-063/tiem-loi/kiem-het-han/ket-qua.txt` (A: hết hạn tự dừng; B: dừng sớm hủy hẹn giờ; `verify` sạch). Còn lại: mất bộ điều khiển giữa chu kỳ → lỗi tự hết hạn, nhưng chu kỳ đó không có M1 (dữ liệu thô giữ). Bộ chạy chuyển lên `exp-obs` (`runner3.py`, DECISIONS 13/11) giữ nguyên logic này, chỉ đổi vận chuyển; đổi pin → hồ sơ đóng băng bản 2. | |
| R2 | **Đúng; CHẶN — đã bổ sung bằng chứng.** | Gói `kt57fcd7` trên cấu hình cuối (sau TD-04..09): P7 `status OK`, hai lần trùng SHA, 39/39 pin; chốt chặn thư mục đã tồn tại hoạt động (`FileExistsError`); safe-export + gói bổ sung bản 3 nhận về, hash khớp. R-04 960/960, R-09 0 mồ côi; R-08 120 thiếu đều là đầu dò liveness Gateway (`routeId=unmatched`). Bằng chứng: `results/T-063/kiem-tich-hop/BAO-CAO.md`, `ket-qua-kt57fcd7.json`, `kiem-r-kt57fcd7.json`. Giữ cả hai lần lỗi `kte4878e`, `kteb5f6d` (dẫn tới TD-09). Còn lại: R-05 một phần, R-07 không đổi; đường phục hồi stage lại mã mới chỉ kiểm bằng chốt chặn, chưa có ca M1 lỗi thật. Cách vận chuyển mới (`runner3` trên `exp-obs`) sẽ được kiểm bằng lượt chạy thử ngắn trước khi phát. | |
| R3 | **Đúng; KHÔNG CHẶN — chọn hậu kiểm.** | Runner không tự phân loại đầu dò. `HO-SO-LUOT.md` dòng 8 nay ghi: ca vẫn `m1-queued`, xác nhận hậu kiểm trên sổ (đầu dò t+60/t+330) theo điều kiện `D2B-KET-QUA.md`, ghi từng mã mờ vào `results/T-063/chay/xac-nhan-ca.json` **trước** khi T-064 khai tập chọn; ca không xác nhận ra khỏi tập chọn. Không thêm truy vấn trong cửa sổ phương pháp. Hệ quả: có thể cần lượt bù sau hậu kiểm. | |
| R4 | **Đúng; KHÔNG CHẶN.** | `D2B-KET-QUA.md` mục "Đính chính theo REVIEW T-063 R4": cách tiêm ĐẠT; điều kiện cô lập chưa thỏa (CPU-BOOK-2 72% < 80%; CPU-BOOK-1 thiếu PSI máy; tải D2 hết sớm). Giữ hai cường độ, không chỉnh theo số đã xem. Đầu dò `inj2 probe` thêm PSI CPU toàn máy (`psi_cpu_may`), nên đợt thu sẽ có số này dưới tải mua vé; diễn giải CPU-BOOK-1 là "ít nhiễu toàn máy" chỉ sau khi xem số ấy. | |