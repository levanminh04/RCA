# Phản biện T-030

- **Người phản biện:** Codex — **Ngày:** 06/10/2026 — **Commit/diff đã đọc:** `git diff 3b1e0dd`; đầu ra T-030 chưa được theo dõi trong Git nên đọc trực tiếp.
- **Đã đọc:** `AGENTS.md`, `docs/STATE.md`, SPEC và LOG T-030, mẫu REVIEW và `docs/review-prompt.md`; mọi file Python trong `src/p3/`; ba JSON đầu ra, `results/T-030/scripts/`, `tests/`, `runs/` và các bản ghi fixture liên quan trong `work/`; giao thức, cấu hình V2, allowlist, bảng mốc và universe của T-022; `docs/WHY.md`, `LESSONS.md`, các quyết định P3 trong `DECISIONS.md`, phần liên quan của MRP và PLAN-P3-G2; hai nguồn DT18 và hướng dẫn giảng viên. Đối chiếu code `src/{microrank,simplerca,torai,circa_kien_truc}`, RCAEval, BARO và CIRCA tại đúng revision được giao; dữ liệu tác giả torai-TT và đầu ra cũ T-016/T-017 trong phạm vi dev.

**Kết luận hiện hành sau kiểm lại ngày 06/10/2026:** R1, R2 và N1 đã được khắc phục trong bản sửa người làm ghi ở LOG "Phiên 2 (tiếp)". Còn **R3 CHẶN**: TORAI nguồn A lỗi khi ghi thông tin cửa sổ có nửa N rỗng. Bằng chứng và phạm vi ở mục "Kiểm lại sau sửa" dưới đây; phần phản biện ban đầu và bảng phản hồi được giữ làm lịch sử.

## Kết luận chung

Có **hai điểm CHẶN** trong mã chung: CIRCA làm mất thông tin hồi quy từng nút; nhánh TIMEOUT không giữ đúng biến thể và số bản ghi của CIRCA/MicroRank. D1, phát lại và số tổng K-B1 khớp; chưa thấy nhãn lọt vào phương pháp. Hai lỗi cài đặt khiến tiêu chí mã thực hiện đủ giao thức chưa đạt; chưa có bằng chứng accuracy P3 đã bị sai.

## Các điểm

### R1. CIRCA bỏ thông tin hồi quy từng nút khi trả kết quả — CHẶN

- **Ở đâu:** `src/p3/adapters/circa.py:124–140`; đối chiếu dòng 85–86, 99–100 của cùng file. Bước 4 T-030; giao thức V2 §6.5, dòng 185 và 190; WHY-30.
- **Sai gì:** `cham_svr` và `cham` đã có `regression_route` (nhánh hồi quy), `regression_error` và cha hiệu lực cho từng nút. Nhưng `chay` bỏ `snap['nodes']`, chỉ trả tổng số theo nhánh, tên nút fallback và thống kê đồ thị. `worker` và `runner` lưu kết quả này, không lưu snapshot ở nơi khác. Giao thức yêu cầu ghi nhánh và thông điệp lỗi từng nút cho cả SVR và OLS.
- **Bằng chứng:** chạy fixture có sẵn bằng Python được giao, chỉ trong bộ nhớ: `fixture.metrics/traces → cua_so.cat_ca → circa.chay`, với `mo_hinh='ols'` và `'svr'`. Mỗi mô hình có 18 nút, gồm 12 nút `no_effective_parents` và 6 nút hồi quy. Đầu ra chỉ giữ hai số tổng; không có bảng nút hoặc thông điệp lỗi. Code nguồn RHT bắt `ValueError` rồi dùng z-score trực tiếp; snapshot của adapter tính đúng các trường này nhưng không truyền ra bản ghi.
- **Hậu quả:** khi T-031 kiểm mô hình, bản ghi không cho biết sáu nút nào đã hồi quy và không giữ nguyên nhân của lỗi dự phòng nếu có. P4 cũng mất bằng chứng để phân biệt lỗi riêng của mô hình với lỗi đầu vào. Đây là thiếu dữ liệu ngay trong đầu ra đã cài, không phải yêu cầu chạy sớm các phép kiểm 30 ca của T-031.
- **Đã xét phản bác:** tổng nhánh và danh sách fallback vẫn cho biết có fallback hay không; finding không phủ nhận điều đó. Chúng không thay được yêu cầu ghi từng nút và thông điệp lỗi. Docstring nói đã ghi từng nút, nhưng đường trả kết quả không giữ chúng.
- **Đề xuất sửa:** giữ `snap['nodes']` trong `diagnostics` hoặc `extra` của hai bản ghi CIRCA. Dùng lại dữ liệu đã tính; không đổi scorer hoặc cách chọn mô hình.

### R2. TIMEOUT đổi biến thể và bỏ một bản ghi CIRCA — CHẶN

- **Ở đâu:** `src/p3/runner.py:156–170`, đối chiếu dòng 178–190; `src/p3/adapters/circa.py:136–140`. Bước 3 T-030; giao thức §6.3, §6.5, §8.3 và §13.
- **Sai gì:** khi thành công, MicroRank có `variant='full'`; CIRCA trả hai bản ghi `<model>+rht_da` và `<model>+rht`. Khi timeout, `_ket_thuc` trả đúng một bản ghi `variant='native'` cho cả hai phương pháp. Hàm cũng không nhận mô hình CIRCA đã yêu cầu.
- **Bằng chứng:** gọi nhánh xử lý có sẵn với `cost['timed_out']=True`, thay `_ghi` bằng hàm trả danh sách để không ghi file:

  ```python
  runner._ghi = lambda directory, recs: recs
  runner._ket_thuc(None, None, [cost], base, method, 'a')
  ```

  Kết quả CIRCA: `[('TIMEOUT', 'native')]`; MicroRank: `[('TIMEOUT', 'native')]`. Đối chứng TORAI B giữ `B`, BARO giữ `native`. Không chạy phương pháp hoặc tạo lượt mới để kiểm nhánh này.
- **Hậu quả:** bản ghi ca quá hạn không thuộc đúng biến thể của các ca thành công. Hai bảng CIRCA không có đủ hai bản ghi thất bại cho cùng ca; lọc theo biến thể sẽ bỏ ca này, trái quy định mọi trạng thái ở mẫu số. Nếu gom chung `native`, lại mất phân biệt mô hình và scorer. Đây là lỗi hợp đồng đầu ra đã tái hiện; việc mất ca trong bảng accuracy tương lai chưa xảy ra trong kết quả T-030.
- **Đã xét phản bác:** evaluator chấm một bản ghi TIMEOUT bằng 0 là đúng. Nhưng nó không khôi phục được biến thể đã mất hoặc bản ghi CIRCA thứ hai. `job.json` còn tên mô hình cũng không sửa các bản ghi được trả cho evaluator. Phép kiểm TIMEOUT đã lưu chỉ dùng BARO, vốn có biến thể `native`, nên không lộ lỗi này.
- **Đề xuất sửa:** truyền mô hình/biến thể dự kiến từ `chay_luot` vào nhánh kết thúc. TIMEOUT giữ `full` cho MicroRank và trả đủ hai biến thể CIRCA của mô hình được yêu cầu, cùng chi phí của lượt đó. Giữ cách chấm TIMEOUT bằng 0.

## Điều đã kiểm và thấy đúng

- Ba JSON đầu ra tồn tại và parse được. Chạy lại D1 trong bộ nhớ, qua selector và kiểm hash đúng 30 ca allowlist, chỉ lấy mốc tiêm: **0 lệch từng ca**, 7 ca có khác biệt, **1.300/6.033.600 ô**. Biên cửa sổ và thứ tự cắt/tiền xử lý khớp giao thức.
- Chạy lại **19/19 test bộ chấm** bằng `D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B results/T-030/tests/test_buoc2.py`, với `PYTHONDONTWRITEBYTECODE=1` và PYTHONPATH được giao. Chạy riêng **8/8 test cửa sổ** bằng AST trong bộ nhớ, bỏ lệnh tạo thư mục. Kiểm trực tiếp chỉ số posterior BOCPD, cột NaN, N-Sigma khởi động/inf/bỏ trùng và tính nhất quán trên tiền tố chuỗi: đạt. Không chạy toàn bộ test runner vì chúng ghi và xóa fixture.
- Phát lại T-017 và các thành viên TAR T-016 trong bộ nhớ, không giải nén ra đĩa: khớp `phat-lai.json`, cả ba seed TORAI. T-017 có Hit@1 = 0,833333; MRR = 0,891111. T-016 có AC@1 = 0,700; AC@3 = 0,933; Avg@5 = 0,880. Các số 0 trong stdout phát lại là sai lệch, không phải accuracy bằng 0. Đây là đầu ra cũ, không phải accuracy P3 mới.
- So code và cộng lại K-B1 từ từng ca: err **411.612/411.806 = 99,9529 %**; lat **409.274/411.806 = 99,3851 %**. Đạt tiêu chí gộp 30 ca đã duyệt. Một ca lat đạt 83,6 % không tự làm trượt tiêu chí gộp. Không dựng lại toàn bộ trace ở lượt phản biện. Giới hạn err toàn 0 và cột lệch/thiếu đã được LOG nêu; K-B1 chưa chọn nguồn B làm chính vì còn K-B2/K-B3 ở T-031.
- Lần theo dữ liệu và đồ thị tới điểm, ứng viên và thứ hạng; chưa thấy root, loại lỗi hoặc locator được đưa vào adapter. Mốc biết trước chỉ dùng cho chế độ (a); job detector không nhận mốc. N-Sigma đúng D9. BOCPD dùng cả bản ghi và min–max hồi cứu như đã khai báo. TraceRCA operation mơ hồ trả `ERROR`; hòa TORAI giữ khối và thứ tự trong khối.
- DT18/cô quy định mục tiêu và đầu ra nghiên cứu; các lựa chọn P3 là quyết định Minh ở Q-74/Q-76. Khung P6 và đối chứng không đồ thị vẫn là ứng viên/gói sau; T-030 không tạo kết luận đồ thị có ích. WHY giải thích các lựa chọn chính và giới hạn của chúng; chưa thấy cam kết thêm cơ chế trước bằng chứng P4 trong đầu ra task này.
- Các kiểm dữ liệu thật K-SVR, độ nhạy builder, K-B2/K-B3, normal-control và accuracy được SPEC chuyển sang task sau. Không tính phần OPEN này là lỗi T-030. Ngoại suy BOCPD 27–83 giờ vẫn là số thô, chưa kiểm trên cấu hình thật; chưa đủ để kết luận thời gian trên EC2.
- Về phạm vi ghi: file mã/kết quả được báo của T-030 nằm trong hai cây được duyệt. LOG còn ghi việc sửa SPEC, tạo SPEC T-031 và thêm dòng STATE theo lời duyệt riêng đầu phiên; ghi chú scratchpad ngoài repo đã được người làm báo vi phạm, không xác minh trực tiếp ở đây. Diff nền còn chứa thay đổi T-022/T-023, nên không quy mọi thay đổi từ commit nền cho T-030. Trong lượt phản biện này chỉ tạo `REVIEW.md`; không sửa LOG/STATE, không commit, không mở `data/locked/` hoặc repo lưu trữ.

## Kiểm lại sau sửa R1, R2, N1 — 06/10/2026 — Codex

**Vai trò và phạm vi.** REVIEW này là đầu ra của người phản biện theo AGENTS §5 bước 6 và §9, cùng workflow `docs/review-prompt.md`. Đã đọc lại SPEC, LOG cuối, mã và test sau sửa; đối chiếu giao thức V2, cấu hình và WHY-22–35, nguồn DT18/hướng dẫn giảng viên. Chỉ bổ sung file này theo yêu cầu Minh; giữ nguyên bảng phản hồi của người làm. Các thay đổi mã và LOG xảy ra trong lúc đọc là bản sửa của người làm, không phải của phiên phản biện.

### Các điểm cũ sau sửa

- **R1 — đã khắc phục.** `src/p3/adapters/circa.py:127–131` giữ `snap['nodes']` trong `diagnostics` dùng chung cho hai bản ghi. Chạy fixture tổng hợp chỉ trong bộ nhớ cho OLS và SVR: mỗi bản ghi có 18 nút, gồm 12 `no_effective_parents` và 6 nút hồi quy tương ứng. Cả bốn bản ghi giữ `rht_score`, route, thông điệp lỗi và cha; số đếm khớp bảng nút. Qua `ban_ghi.tao` và serialize/parse JSON bằng hàm của worker, bảng nút vẫn nguyên. Không chạy K-SVR trên dữ liệu thật; phần đó thuộc T-031.
- **R2 — đã khắc phục.** `runner.py:142,160–177` truyền mô hình vào nhánh kết thúc. Gọi nhánh TIMEOUT trong bộ nhớ, thay `_ghi` bằng hàm trả danh sách: MicroRank có một `full`; CIRCA OLS có `ols+rht_da`, `ols+rht`; CIRCA SVR có `svr+rht_da`, `svr+rht`. Mọi bản ghi có trạng thái TIMEOUT và cùng chi phí của lượt. Bản ghi vẫn chấm 0 theo evaluator.
- **N1 — đã khắc phục theo đề xuất đã duyệt.** `runner.py:131–138` không còn cho thêm tối thiểu 1 s. Thay selector, `_job` và tiến trình bằng đối tượng giả trong bộ nhớ: khi chi phí chuẩn bị bằng ngân sách, runner trả TIMEOUT và không mở tiến trình TORAI thứ hai. Đây không phải chứng minh độ chính xác thời gian ở mức mili giây; sai số polling không được dùng để nâng thành finding mới.

### R3. TORAI A không xử lý được thông tin cửa sổ khi nửa N rỗng — CHẶN

- **Ở đâu:** `src/p3/adapters/torai.py:35`, hàm `chuan_bi_A`; đường gọi ở `src/p3/worker.py:87`, `src/p3/runner.py:134–135,180–184`. Ảnh hưởng bước 4 T-030, mã cắt cửa sổ chế độ (b); đối chiếu giao thức V2 §5.5, §7.5 dòng 253 và §8.3 dòng 282.
- **Sai gì:** `N_phu` chỉ kiểm `len(lt)`, không kiểm bảng `lt[time < t]`. Khi N rỗng nhưng A có bin, `max(N.time)` là NaN; `int(NaN)` ném `ValueError`. Đây là lỗi tính metadata (thông tin cửa sổ) của adapter, xảy ra trước lời gọi TORAI.
- **Bằng chứng:** dùng bảng tổng hợp trong bộ nhớ, cùng lưới 15 s lệch 10 s của fixture đã có: metric ở giây 0–300; ba bảng tác giả ở giây 10, 25, …, 295. Với `t=3` và `t=10`, `torai.chuan_bi_A(...)` ném `ValueError: cannot convert float NaN to integer` tại dòng 35. Đối chứng `t=11` có 1 bin N/19 bin A, `t=100` có 6 bin N/14 bin A, đều trả kết quả. Mốc tuyệt đối chỉ cộng cùng một giá trị cho cả bảng và t. Gọi `worker.main` với job `torai_prep/torai_A`, thay đọc file/hash bằng dữ liệu trong bộ nhớ, tái hiện cùng lỗi; không có lần tạo thư mục hay ghi output nào. Không chạy TORAI trên ca thật.
- **Vì sao là đầu vào hợp lệ:** §7.5 yêu cầu cắt ở biên file, ghi độ dài thực; nền quá ngắn có thể làm phương pháp ERROR nhưng vẫn phải giữ ca trong mẫu số. BOCPD không có warm-up 100 điểm như N-Sigma và có thể đưa báo động đầu trước bin đầu nguồn A; phép kiểm posterior sẵn có tại `test_buoc34.py:test_diem_doi_tu_R` cũng trả điểm đổi ở chỉ số 3. Không có quy tắc cấm cửa sổ này.
- **Hậu quả:** worker chuẩn bị thoát lỗi; runner tạo lỗi runner và dừng, không có bản ghi RCA để lưu/chấm. Phạm vi là TORAI A với báo động đầu sớm tới bin đầu; chưa thấy lỗi xảy ra trên ca thật hoặc làm sai accuracy. Chế độ (a) quanh mốc 720 không có điều kiện này. Nếu K-B chọn B làm chính thì nhánh tích hợp chính không đi qua lỗi; hiện A vẫn là phương án đã duyệt nếu K-B không đạt, nên không thể mặc định loại khỏi hợp đồng mã T-030.
- **Đã xét phản bác:** runner phân loại lỗi này là lỗi runner phù hợp §8.3; finding không yêu cầu đổi nó thành ERROR bằng cách bắt mọi lỗi chuẩn bị. Điều cần sửa là metadata đang làm một cửa sổ hợp lệ không chạy được. Đây là lỗi mã đã tái hiện bằng fixture, không phải yêu cầu chạy sớm K-B2/K-B3 hoặc benchmark của T-031/T-025.
- **Đề xuất sửa tối thiểu:** trong `src/p3/adapters/torai.py`, chỉ tính `N_phu` khi nửa N có bin; N rỗng thì ghi `None`, tương tự điều kiện đang dùng cho `A_phu`. Giữ cửa sổ, lưới, ngưỡng và việc gọi TORAI; để phương pháp tự xử lý thiếu nền theo hợp đồng trạng thái. Chưa sửa mã; Minh quyết.

### Kiểm đã chạy và giới hạn

- Dùng Python `D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B` từ stdin, `PYTHONDONTWRITEBYTECODE=1`, PYTHONPATH như LOG; dữ liệu và đối tượng giả đều ở bộ nhớ. Không tạo lượt chạy mới, không chạy toàn bộ test runner vì chúng tạo/xóa fixture.
- Chạy lại **19/19 test bộ chấm** trong `test_buoc2.py`: đạt. Kiểm thêm N-Sigma trên 7 tiền tố, gồm NaN đầu chuỗi, cột toàn NaN, cột xuất hiện muộn và inf: báo động tiền tố khớp phần tương ứng của cả chuỗi. Biên khởi động, điểm cuối và thời gian trơ đúng 300 s: đạt.
- Gọi trực tiếp **11 phép kiểm thuần** có sẵn trong `test_buoc34.py`, bỏ setup tạo file: đường OLS qua scorer SVR khớp `score_graph`; khóa TraceRCA; posterior BOCPD và chuỗi nhỏ; N-Sigma; thời gian trơ; ba kiểm tên cột/so cột TORAI; hai kiểm tách nhãn/bản ghi. Đạt. Bốn bản ghi CIRCA kiểm R1 và các nhánh TIMEOUT/ngân sách kiểm R2/N1 cũng đạt như trên.
- Ba JSON đầu ra parse được. Cộng lại từng ca: D1 vẫn 7/30 ca có khác biệt, 1.300/6.033.600 ô; K-B1 err 411.612/411.806, lat 409.274/411.806, đều đạt tiêu chí gộp đã duyệt. `phat-lai.json` không có sai lệch được lưu. Không chạy lại D1 trên telemetry, dựng K-B1 hoặc phát lại toàn bộ đầu ra cũ vì bản sửa không tác động các phần đó.
- File kết quả test của người làm ghi **14 + 19 + 23 = 56 test đạt**, khớp LOG cuối. Con số 56 là kết quả được lưu của người làm, không phải toàn bộ số test chạy lại trong phiên này. Phần kiểm riêng sau sửa không cho thấy R1/R2/N1 còn lỗi.
- Không thấy finding đáng kể khác trong evaluator/detector: hòa khối, Rerank tỉ số gộp, bootstrap ghép cặp ô, mọi trạng thái ranker ở mẫu số, báo động thô và thành công chung khớp giao thức. Không thấy rò nhãn thêm. Chi phí BOCPD trên cấu hình thật, K-SVR, K-B2/K-B3 và lựa chọn nguồn chính vẫn OPEN ở task sau; không biến chúng thành lỗi của T-030.
- **Lệch trạng thái cần người làm đối chiếu:** `docs/STATE.md:36` và LOG cuối ghi đã sửa/56 test, nhưng STATE dòng 41 còn nói SPEC đề xuất/chưa có code, dòng 46 còn chờ duyệt SPEC và tách; dòng 36 cũng giữ câu 54 test cũ. Hai đoạn tổng hợp này không phù hợp trạng thái đầu ra đã xác minh. Đề xuất đồng bộ STATE theo trạng thái được Minh quyết; người phản biện không sửa STATE và không coi các đoạn cũ là quyết định đổi phạm vi task.
- Phiên này không đổi quyết định nghiên cứu, không sửa mã/LOG/STATE, không mở dữ liệu khóa hoặc repo lưu trữ, không commit/push. Còn R3 để người làm phản hồi và Minh quyết sửa; chưa kết luận đủ điều kiện đóng T-030.

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| R1 | **Đúng.** | Đọc `circa.py:124–140`: `chay` dựng `routes` (đếm) và `value_error_fallback_nodes` rồi bỏ `snap['nodes']`; `_json_default`/worker/runner không lưu chỗ khác. Giao thức §6.5 (K-SVR2, V2-T1) yêu cầu route và thông điệp lỗi từng nút cho cả OLS lẫn SVR; `cham`/`cham_svr` đã tính sẵn. Phạm vi đúng như reviewer nêu: thiếu ở đường ra, scorer không sai. Mặt trái của sửa: bản ghi dài thêm khoảng một dòng mỗi nút. Chưa sửa, chờ Minh. | |
| R2 | **Đúng.** | Đọc `runner.py:_ket_thuc`: nhánh timeout gọi `ban_ghi.tao` một lần với variant `'native'` nếu `ten` không phải torai; `chay_luot` không truyền `model`. MicroRank thành công mang `'full'`, CIRCA mang hai bản ghi `<mô hình>+rht_da` và `+rht`. Giao thức §8.3 đặt TIMEOUT vào mẫu số, nên ca quá hạn của CIRCA mất ở hai bảng, của MicroRank mất ở bảng `full`. Chưa xảy ra trong kết quả T-030 (phép kiểm TIMEOUT chỉ dùng BARO). Sửa như reviewer đề xuất: truyền `method`/`model` vào `_ket_thuc`, TIMEOUT trả đủ biến thể; cần thêm một fixture TIMEOUT cho CIRCA và MicroRank vào test bước 3–4 để phủ lỗi này. | |
| N1 | Tôi tự thấy khi đọc `runner.py:128` (TORAI): `max(con_lai, 1)` cho lượt TORAI ít nhất 1 giây dù ngân sách đã hết, nên tổng một lượt có thể vượt `timeout_s` tới 1 giây. **KHÔNG CHẶN.** | Chỉ lệch ≤ 1 s so với giới hạn khai trước; không đổi trạng thái hay xếp hạng. Sửa gọn: nếu `con_lai <= 0` thì trả TIMEOUT ngay. | |
| R3 | **Đúng.** | `torai.py:35` tính `N_phu` khi `len(lt) > 0` mà không kiểm phần `time < t`; N rỗng → `int(NaN)` → `ValueError`, lỗi runner. Tái hiện trong bộ nhớ: t = 3, 10 lỗi; t = 11 chạy. Chỉ ở chế độ (b), báo động đầu BOCPD trước bin đầu file tác giả. Soát cùng kiểu trong `src/p3`: chỉ dòng này. Đã sửa theo lời duyệt ("duyệt sửa R3 theo 1–6"): `N_phu` tính trên nửa N, rỗng → `None`; thêm `test_n_rong`; 57/57 test đạt (LOG phiên 3). | |
