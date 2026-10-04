# Môi trường và cách dựng lại T-014

Task chạy trên Windows 11 và EC2 T-007. Các phiên khác dùng chung máy; mọi thời gian laptop là số chẩn đoán. Các vòng PC được giữ riêng, không gọi một import thành công hay một ranking rỗng là “chạy đúng”.

## Python trên laptop

Môi trường mới `D:/RCA-ext/envs/T-014-main/`, Python 3.12.10. Nó dùng thư viện của `D:/RCA-ext/envs/py312-pin/` qua file `.pth` chỉ trong môi trường mới. Không sửa môi trường nguồn. Hai gói thêm riêng: pyarrow18.1.0 để đọc Parquet và networkx2.8.8 vì CIRCA0215 dùng `topological_generations`, không có trong networkx2.5.1. Distutils shim cũng chỉ nằm trong `.pth` của môi trường mới; giữ lượt import lỗi trước đó.

Phiên bản thực tế ở `runs/environment-python.json`: numpy1.26.4, pandas2.2.3, scipy1.14.1, sklearn1.6.0, causal-learn0.1.3.8, networkx2.8.8, pyarrow18.1.0, PyYAML6.0.2, psutil6.1.1. `runs/python-freeze.txt` khóa toàn bộ thư viện được nhìn thấy, gồm các gói kế thừa. Đây là môi trường task, không phải môi trường tác giả năm2022.

Cách dựng lại tương đương, khi môi trường py312-pin của T-006 đã có (lượt thực tế dùng trình quản lý gói bundled; uv không nằm trên PATH):

```powershell
py -3 -m venv D:/RCA-ext/envs/T-014-main
# t014-readonly-pinned.pth trong site-packages của môi trường mới có hai dòng:
# D:/RCA-ext/envs/py312-pin/Lib/site-packages
# import _distutils_hack; _distutils_hack.add_shim()
# Dùng trình quản lý gói có sẵn, cache của task, thêm đúng hai phiên bản:
& D:/RCA-ext/envs/T-014-main/Scripts/python.exe -m pip install --cache-dir D:/RCA-ext/work/T-014/cache pyarrow==18.1.0 networkx==2.8.8
```

Trên máy khác không có môi trường kế thừa, dựng môi trường riêng từ `python-freeze.txt` và nguồn/revision ở manifest. Không dùng `.pth` trỏ tới đường dẫn chưa tồn tại. Bản khóa gồm nhiều gói không cần cho CIRCA; task không tự sửa requirements chung hoặc cài lại chúng.

Trước mọi lượt khoa học:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONHASHSEED='0'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$env:TEMP='D:/RCA-ext/work/T-014/tmp'
$env:TMP=$env:TEMP
& D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B results/T-014/scripts/run_examples.py
```

Lượt graph đầu không lưu hashseed được giữ trong `graphs/initial-unrecorded-hashseed/`. Graph chính được dựng lại có kiểm soát seed0; `builder-hashseed-0.json` khớp cả30, `builder-hashseed-1.json` khác cạnh ở24graph cyclic. Native YAML/factory kiểm riêng trong `runs/native-yaml-equivalence.json`. Lượt scoring có mảng/điểm snapshot độc lập và không thay bằng graph khác.

## Nguồn code và dữ liệu

CIRCA clone riêng tại `D:/RCA-ext/work/T-014/CIRCA/`, revision ghi trong `paper/source-manifest.json`; RCAEval tại `D:/RCA-ext/src/RCAEval/` chỉ đọc/chạy, revision ghi cùng manifest. Paper805945B từ nguồn tác giả; số công bố được lưu trước phép đo ở `paper/cong-bo-circa.csv`.

Chỉ30ca dev RE2-TT được đọc ở `data/rcaeval/re2tt_*`. Mốc thiếu ở29thư mục dùng metadata đã có của T-002; mỗi nguồn/hash ở `runs/inventory.json`. Chỉ metrics và mốc của ca đã chọn được chép lên EC2, không chép trace, locked hay ca TT khác. Input PC600điểm quanh mốc; RHT train111/test10 sau resample1s. Metadata/schema ở các thư mục legacy được phép chỉ đọc header; đó không phải chạy RCA trên ca mới.

## R/pcalg không cần quyền quản trị

Đã dựng R4.4.2/pcalg2.7-12 và Bioconductor3.20 bằng giải nén vào `D:/RCA-ext/work/T-014/`, không chạy installer hay ghi registry. Quy trình, binary ghim, nguồn tải và checksum ở `audit/moi-truong-r.md`, `r-packages-installed.csv`, `source-downloads.csv`, `external-files.csv`. Giữ lần metadata403 và các cảnh báo locale/build-version. R dùng để điều tra graph/backend, không thay tên bản CIRCA-PC RCAEval.

Artifact Figshare chỉ extract code/config trong whitelist. Không đọc cache Oracle, kết quả từng ca Oracle hay dữ liệu raw mới. Supplementary/update artifact có revision khác checkout task; không gộp chúng thành cùng nguồn số công bố.

## EC2 và giới hạn chi phí

Máy m7i-flex.large2vCPU/7.6GiB RAM/no swap của T-007. Môi trường/source/data chung chỉ đọc; mọi ghi ở `/home/ubuntu/rca/T-014/`, gồm data, scripts, cache, tmp, runs và log. Script `scripts/ec2_run.py` chạy nohup, tiến độ15s, supervisor30s, một worker nặng. Nó tạm dừng đúng process group của mình khi thấy Python/Rscript ngoài task, không tác động phiên khác. Wall-clock vẫn tính thời gian pause. Không stop/restart máy hay sửa hệ thống.

Ước lượng trước chạy nằm ở SPEC/LOG:30ca theo T-005 cần>30h, vượt3h; mốc TORAI9383.1s cho30ca khác dữ liệu/máy, không dùng làm runtime chính thức. Chọn trước một ca nhỏ nhất để kiểm TT scale. Tổng PC mặc định tối đa120phút, PC chẩn đoán tối đa45phút, phần kiểm khác dành15phút; tổng method/dataset≤180phút. Các lần dừng/tranh máy đều tính và giữ. Kết quả thực tế, trạng thái từng lượt và tổng chi phí ở `runs/chi-phi-tong.json`; không suy chi phí toàn30ca từ timing máy đang tranh tải.

Tải mới gồm code/paper/gói Python/R và artifact cấu hình, không tải dataset. Audit có lượng mạng đã biết131175732B. Paper805945B và hai wheel Python/code được ghi trong manifest tải của nhánh chính; toàn task dưới1GB. Dung lượng file sau giải nén không đồng nhất lượng mạng tải. Không commit/push.


## EC2 thứ hai: môi trường kiểm tiếp

Python3.12.3portable được copy từT015 chỉđọc sangT014/python; uv vàenv/source/wheels/cache/tmp đều riêng trongT014.36gói ghim ởrequirements-followup.txt, version thuậttoán trùngEC2₁, networkx2.5 cho hàmrht trựctiếp; adapter snapshot local2.8.8 đượcso tới từngscore. Khôngapt/admin/hệthống. Chạy ec2_followup_setup.sh, ec2_followup.py preflight/supervisor. Sourcegitarchive đúngrevision,5criticalfile vàrawSHA khớp. WheelPyPI giữ compressedfile/metadata/SHA/byte, retryreuse; inventory gắn host3.26.62.217. Cáclượtsetup lỗi giữnguyên. Ngân sáchmethod táchqueueno-worker sauMinhyêucầutiếptục; không tăngtrần3hactual. Xem bo-sung-ec2.md vàenvironment-ec2-2.json.
