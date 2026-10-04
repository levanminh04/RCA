# T-006 — X1: chốt bộ thư viện cho Python 3.12

Ghi ngày 03/10/2026, khoảng 14:20. Người làm: Claude. Đọc bởi: T-007 (bước E2, E3).

## Kết luận

**Đã dùng `py312-pin` cho các khối Python 3.12 (T-006 sau X1; T-007 E2, E3). Minh quyết ngày 04/10/2026: giữ `py312-pin`, không dừng** (REVIEW T-006 R1; WHY-15). Ghi thẳng: luật được làm rõ sau khi đã thấy kết quả. Kết quả không phụ thuộc cách hiểu luật với mốc loại B, vì hai bộ giống nhau ở mọi ô.

Luật chốt (viết trong SPEC T-006 trước khi chạy): bộ ghim khớp mốc thì dùng bộ ghim (LESSONS SL29); không bộ nào khớp thì dừng. Luật không tách mốc loại A với loại B. X1 xác nhận đúng hai điều:
- (a) Cả hai bộ khớp mọi mốc loại A: ví dụ BARO, `reproduce_baro` 5/5 ô.
- (b) CIRCA trên torai-OB (mốc loại B) lệch quá 0,02 ở nhiều ô (MEM +0,057, DISK +0,150; AVERAGE +0,037). Kết quả giống nhau ở hai bộ, và cả hai rơi vào nhánh dự phòng ở 1 ca (`checkoutservice_cpu_2`).

Phiên 1 đã hiểu luật là chỉ xét mốc A, rồi ghi là "luật chọn bộ ghim", mà không hỏi Minh. Nếu mốc B cũng phải khớp, luật sẽ ra "dừng". Hai bộ cho cùng kết quả ở mọi ô, nên X1 không phân biệt được bộ nào tốt hơn.

## Bộ thư viện đã chốt: `py312-pin`

Dựng trên laptop (Windows 11, Python 3.12.10), từ `D:\RCA-ext\`:

```
py -3.12 -m venv envs/tools && envs/tools/Scripts/python.exe -m pip install uv      # uv 0.12.22
envs/tools/Scripts/uv.exe venv --python <python 3.12> envs/py312-pin
cd src/RCAEval     # RCAEval 259ea41
../../envs/tools/Scripts/uv.exe pip install --python ../../envs/py312-pin/Scripts/python.exe --exclude-newer 2024-12-22 -e ".[default]"
```

- 22/12/2024 là ngày nộp bài RCAEval (SPEC T-006). Không cần phương án dự phòng: mọi gói đều có bản trước ngày đó.
- Bản chính đã cài: pandas 2.2.3, numpy 1.26.4, causal-learn 0.1.3.8, scikit-learn 1.6.0, scipy 1.14.1, statsmodels 0.14.4, networkx 2.5, torch 2.5.1, tigramite 5.2.7.0, pyagrum 1.17.2.
- `uv pip check`: sạch. Danh sách đầy đủ: `runs/freeze-py312-pin.txt` (174 gói). Log: `runs/11b-cai-uv-py312-pin-lan2.log`, `runs/12-kiem-py312-pin.log`.
- Gợi ý cho T-007 trên EC2 (Linux): dùng cùng lệnh `uv ... --exclude-newer 2024-12-22`, rồi so bản các gói chính ở trên. Nếu khác bản, ghi lại. File freeze có gói chỉ có trên Windows (ví dụ pywin32), nên không cài thẳng từ file đó trên Linux.

So với `py312` (bản mới nhất ngày 03/10/2026, dựng ở T-005): pandas 3.0.6, causal-learn 0.1.4.8, scikit-learn 1.7.2, scipy 1.17.1, torch 2.8.0; numpy cùng 1.26.4 (`results/T-005/runs/freeze-py312.txt`).

## Kết quả X1

Mỗi ô dưới đây chạy bằng cả hai bộ, mỗi bộ một khối riêng. Log và đầu ra: `runs/x1-<bộ>-<khối>.tar.gz`. Chấm CIRCA: `cham/x1-<bộ>-circa-torai-ob.json`.

| Phép kiểm | Mốc | Nguồn mốc | `py312` | `py312-pin` |
|---|---|---|---|---|
| Ví dụ cơ bản BARO (`simple_data.csv`, BOCPD + RobustScorer) | A: phát hiện ở bước 243; top 5 `checkoutservice_latency, cartservice_mem, cartservice_latency, cartservice_cpu, main_mem` | README BARO e35f4ec | bước 243; top 5 trùng đúng thứ tự | bước 243; top 5 trùng đúng thứ tự |
| `reproduce_baro` trên fse-ob (BARO `main.py --dataset OnlineBoutique --fault-type <lỗi>`) | A: Avg@5 CPU 0,91, MEM 0,96, DELAY 0,95, LOSS 0,62, ALL 0,86 | README BARO; Bảng 3 bài BARO | 0,91 / 0,96 / 0,95 / 0,62 / 0,86 | 0,91 / 0,96 / 0,95 / 0,62 / 0,86 |
| CIRCA trên torai-OB (RCAEval `main.py --method circa --dataset torai-ob --length 10`), Avg@5 | B: 0,88 / 0,89 / 0,85 / 0,83 / 0,75 / 0,88; AVERAGE 0,85 | Bảng 2 bài TORAI, dòng Metric | 0,853 / 0,947 / 1,000 / 0,893 / 0,800 / 0,827; AVERAGE 0,887 | giống hệt `py312` ở mọi ô |

Thứ tự cột của dòng CIRCA: CPU / MEM / DISK / SOCKET / DELAY / LOSS.

Ghi chú về CIRCA:
- `cham.py` tính lại từ file từng ca ra đúng Avg@5 `main.py` in, ở cả hai bộ.
- Cả hai bộ rơi vào nhánh dự phòng (trả thứ tự cột) ở cùng một ca, `checkoutservice_cpu_2`. Lỗi: `Data correlation matrix is singular. Cannot run fisherz test`. Vậy lỗi này không do khác bản causal-learn (0.1.3.8 hay 0.1.4.8).
- Thứ hạng hai bộ giống hệt ở 68/90 ca. 22 ca còn lại khác thứ tự, nhưng điểm mức service không đổi.
- So với bài TORAI, AVERAGE cao hơn 0,04; các ô lệch từ −0,05 đến +0,15. Đây là mốc loại B, nên chưa kết luận đúng hay sai; phân tích ở `kiem-dung-dan.md`.

## Giới hạn của X1

- X1 chỉ kiểm BARO (BOCPD, RobustScorer) và CIRCA. MicroRank, TraceRCA chưa được kiểm ở đây (T-007 kiểm). Hai bộ cho cùng kết quả ở mọi phép kiểm X1, nên X1 không cho biết bộ nào đúng hơn với các phương pháp khác. Chọn bộ ghim là theo luật đã viết trước, không phải vì bộ ghim cho số tốt hơn.
- Các phép kiểm chạy trên Windows. Trên Linux, uv có thể chọn bản dựng khác của cùng phiên bản.

## Cập nhật phiên 2 (03/10/2026, chiều tối)

Phát hiện về độ dài cửa sổ, có thể ảnh hưởng cách so mốc ở T-007 (chi tiết và bằng chứng: `kiem-dung-dan.md` mục 2.1; LOG T-006 phiên 2):
- `--length` của `main.py` RCAEval mặc định 10 tới commit `977c1a8` (22/12/2024), từ `61326e5` (27/12/2024) mặc định 20.
- Cửa sổ 20 tái lập được dòng BARO Bảng 3 bài TORAI: BARO `main.py --length 20` trên torai-SS trùng đến 2 chữ số mọi ô T1, T3, A5; `--length 10` thì không. Đây là ứng viên cho cấu hình các baseline khác của bài, chưa xác nhận. Bài chỉ ghi dùng mã công khai với tham số mặc định của từng bài (§4.3) (sửa theo REVIEW R3).
- Mốc MicroRank, TraceRCA của T-007 (dòng Trace Bảng 2 bài TORAI) vì vậy nhiều khả năng cũng chạy với cửa sổ 20. Điều này chưa kiểm ở T-006.
- CIRCA torai-OB ở bảng X1 trên chạy `--length 10`; số so với bài TORAI ở đó vì vậy không cùng cấu hình với bài.
