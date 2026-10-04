# Sổ quan hệ ca đã nhìn — T-019, bước 7

## Đã kiểm

Đếm trực tiếp 505 ca local: fse-ss 100, torai-SS 90, RE1-SS 125, fse-ob 100, torai-OB 90. Manifest giữ đường dẫn, mốc tiêm, size và hash từng file nguồn trong `local-file-manifest.json`. Không chạy phương pháp RCA (root cause analysis, chẩn đoán nguyên nhân gốc) hay bộ phát hiện.

Đọc toàn 125 ca HF RE1-SS, 90 ca HF RE2-SS và 90 ca HF RE2-OB trong revision ghim của `download-plan.json`. SS do người làm chính tải; subagent chỉ tải 180 file metric/tiêm RE2-OB, tổng 14.215.893 byte. Từng file đúng size và SHA256 LFS hoặc git blob SHA1 của metadata. `download-manifest.json` và `outside-files.csv` giữ đủ nguồn, revision, hash và đường dẫn ngoài repo.

Sổ `so-ca-da-nhin.csv` có 910 dòng, không trùng khóa nguồn × ca × họ public × ca public. Có 405 cặp đo nội dung. 400 cặp khớp toàn bộ cột, vector thời gian, vị trí NaN và giá trị metric trong sai số rtol/atol 1e-12. 5 cặp khớp sau khi bỏ riêng dòng không có thời gian khỏi bản CSV. Không dùng tên ca hoặc cùng mốc tiêm để tự kết luận trùng. Chi tiết nằm trong `public-metric-comparisons.json`; số tổng nằm trong `summary.json`.

| Quan hệ | Bằng chứng trên file thật | Kết luận đúng phạm vi |
|---|---|---|
| fse-ss → local RE1-SS | 100/100 cặp cùng byte ở cả raw data.csv, simple_data.csv và cùng mốc tiêm | 100 ca non-disk là cùng file local; 25 disk chỉ có ở RE1-SS |
| fse-ss → HF RE1-SS | 99 bảng khớp toàn bộ; user_mem_1 khớp toàn bộ các dòng có thời gian | Cùng ghi đo metric đã phát hành ở hai định dạng; HF không giữ các dòng thiếu time |
| local RE1-SS → HF RE1-SS | 123 bảng khớp toàn bộ; user_mem_1 và catalogue_disk_3 khớp toàn bộ các dòng có thời gian | Đủ 125 ca được nối bằng nội dung; hai bảng không giống hệt vì HF thiếu dòng |
| torai-SS → HF RE2-SS | 90/90 bảng metric khớp toàn bộ, cùng mốc tiêm | Đủ 90 ca nối với RE2-SS; không suy ra từ một mẫu |
| torai-OB → HF RE2-OB | 88 bảng khớp toàn bộ; checkoutservice_cpu_2 và checkoutservice_mem_2 khớp toàn bộ các dòng có thời gian | Đủ 90 ca nối với RE2-OB; hai bảng không giống hệt vì HF thiếu dòng |
| fse-ss/local RE1-SS → RE2-SS; torai-SS → RE1-SS; fse-ob → RE2-OB | Toàn release không có mốc tiêm hay vector thời gian trùng; các cửa sổ metric không giao nhau | Không tìm thấy cùng bản ghi theo clock nguồn. Chưa khẳng định độc lập khoa học nếu clock hay provenance bị đổi mà nguồn không khai báo |

Khả năng khác cần giữ: CSV→parquet có thể đổi biểu diễn số; đây là lý do so số với sai số rất nhỏ và cả NaN, không so byte để kết luận khác recording. Việc HF thiếu dòng có thể do lọc thời gian khi xuất bản, do bản nguồn khác, hoặc do chuyển đổi. Task xác nhận khác biệt và nội dung còn lại; không xác định lịch sử thao tác của tác giả chỉ từ file hiện tại.

## Các dòng HF không giữ

| Nguồn local/ca | Số dòng thiếu time local | Số ô metric khác time còn non-null trong các dòng đó | Số dòng local/HF |
|---|---:|---:|---:|
| fse-ss và RE1-SS / user_mem_1 | 114 | 2.203 | 721 / 607 |
| RE1-SS / catalogue_disk_3 | 74 | 1.628 | 721 / 647 |
| torai-OB / checkoutservice_cpu_2 | 256 | 5.716 | 1.186 / 930 |
| torai-OB / checkoutservice_mem_2 | 258 | 5.585 | 1.262 / 1.004 |

Những dòng này không rỗng toàn bộ. Vì vậy không gọi hai bảng là giống hệt và không suy rằng không mất thông tin. Các giá trị không có thời gian không xác định được quan hệ trước/sau tiêm; task không tự gán thời gian cho chúng. Số lấy từ `public-metric-comparisons.json`.

## Task đã chạy và mức đã nhìn

Đọc và parse từng kết quả trong sáu archive: T-006 BARO fse-ss 100/100, BARO fse-ob 100/100, TORAI torai-SS 90/90, TORAI torai-OB 90/90; T-007 MicroRank 90/90 và TraceRCA 90/90. Mọi kết quả có rank không rỗng. `run-members.csv` ghi đúng archive/member từng ca; `run-manifest.json` giữ hash archive và meta. Các bộ phương pháp khác ở T-006 cũng đã dùng những nguồn này, nhưng một archive đủ ca mỗi nguồn đã đủ chứng minh đã chạy; không cần chạy lại.

- HF RE2-SS: toàn 90 ca đã qua RCA ở T-006 theo nối metric với torai-SS.
- HF RE1-SS: 100 ca non-disk đã qua RCA ở T-006 theo nối byte local fse-ss và nối metric với HF. Đây là bằng chứng gián tiếp qua cùng dữ liệu, không gọi là một run trực tiếp mang tên RE1-SS.
- 25 ca disk RE1-SS: T-006 có census metadata. `results/T-006/runs/05d-so-re1-fse-ss.log:2` đếm 125/100 ca; dòng 3 liệt kê nhóm disk chỉ có ở RE1. `results/T-006/scripts/so_re1_fse.py:27` chỉ lấy giao tên ca, và dòng 34 chỉ so file của giao đó. Do đó log này không chứng minh đã đọc nội dung 25 ca disk. Quét meta của 88 archive T-006 không tìm thấy command/link trực tiếp RE1-SS (`all-T006-run-commands.json`). Còn OPEN về một run khác chưa lưu trong các archive đó. T-019 đã hash và đọc metric đủ cả 25 ca.
- HF RE2-OB: toàn 90 ca chạy trực tiếp ở T-007, đồng thời nối với 90 torai-OB của T-006. fse-ob 100 ca chạy ở T-006, nhưng không có cửa sổ ghi đo chung với RE2-OB trong dữ liệu đã kiểm.

Không chọn, loại dataset hay chia dev/test. Sổ chỉ ghi phạm vi dữ liệu đã được chạy, đã đọc và bằng chứng trùng để G1 quyết định sau.

## Đối chiếu task cũ

Không có đính chính sai thực tế ở hai khẳng định lineage đã kiểm: `results/T-006/kiem-dung-dan.md:66` đúng với file local; `results/T-007/kiem-dung-dan.md:41` đúng về 90 tên ca/mốc tiêm và nay có thêm bằng chứng metric. Không sửa file task cũ. Những ghi nhận mới về HF thiếu dòng được triển khai bằng manifest/comparison/sổ trong task này; chúng không phủ định câu về local RE1-SS=fse-ss của T-006.

## Tái lập, kiểm cuối và lượt giữ lại

Chạy trong `D:/RCA-flashticket`, dùng Python sẵn có; không tạo hay sửa môi trường:

```powershell
& D:/RCA-ext/envs/py312/Scripts/python.exe results/T-019/lineage/check_lineage.py local
# Ghi LOG nguồn/revision/14.215.893 byte trước dòng tải sau.
& D:/RCA-ext/envs/py312/Scripts/python.exe results/T-019/lineage/check_lineage.py download
& D:/RCA-ext/envs/py312/Scripts/python.exe results/T-019/lineage/check_lineage.py compare --ss-root data/T-019
& D:/RCA-ext/envs/py312/Scripts/python.exe results/T-019/lineage/check_lineage.py verify
```

`verification.json`: tất cả kiểm đều đạt. `source-file-integrity.json`: 1.695 file local và 6 archive dùng để xác nhận kết quả đã hash trước và sau giữ nguyên; 180 file tải ngoài repo vẫn khớp hash. `input-file-final-hashes.json` ghi thêm snapshot cuối của 88 archive có meta được đọc và 5 nguồn văn bản/metadata. Snapshot cuối này không tự chứng minh before/after cho những file không có baseline. Script reader xử lý từng bảng, giới hạn một luồng thư viện toán, không cần cài gói. Phiên kiểm cuối dùng pandas 3.0.6, numpy 1.26.4, pyarrow 25.0.1 trong env py312; manifest giữ phiên bản Python.

Lượt compare đầu còn xếp 5 ca thiếu time vào same-injection-only được giữ nguyên trong `compare-run001/`. Đã bổ sung kiểm toàn bộ dòng có thời gian và số ô không-null trong dòng thiếu thời gian; kết quả hiện tại là lượt compare thứ hai. `progress.log` giữ tiến độ hai lượt. Hai lệnh khám phá ban đầu chỉ đọc bị lỗi: một lệnh giả định torai có data.csv gây StopIteration; một lệnh dùng env py312-pin đọc parquet thiếu pyarrow gây ImportError. Đã sửa cách đọc đúng simple_metrics.csv và dùng env py312 có sẵn, không sửa môi trường hay nguồn. Không có file tải hỏng và không có retry tải.

Chỉ ghi trong `results/T-019/lineage/` và tạo 180 file tại `D:/RCA-ext/work/T-019/lineage/re2ob/`. Không ghi LOG/STATE/SPEC/chung/task khác. Parent cần đưa các đường dẫn này vào inventory phản biện; `outside-files.csv` có đầy đủ từng file ngoài repo.
