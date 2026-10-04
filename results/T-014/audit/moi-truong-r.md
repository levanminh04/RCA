# R/pcalg riêng cho kiểm CIRCA của T-014

Đã chạy được R 4.4.2 và pcalg 2.7-12 bằng quyền user, ngày 04/10/2026. Không chạy installer. Dùng innoextract 1.9 từ release chính thức để giải nén installer R vào `D:/RCA-ext/work/T-014/R/`; không tạo shortcut hay ghi registry. Mọi gói R được giải nén từ Windows binary vào `D:/RCA-ext/work/T-014/R-library/`. Gói đã ghim ở `r-packages-installed.csv`; nguồn, dung lượng và hash ở `r-downloads.json` và manifest ngoài repo. Đây là phiên bản chạy của task, không phải khẳng định môi trường tác giả năm 2022.

Đường dẫn runtime: `D:/RCA-ext/work/T-014/R/app/bin/Rscript.exe`. Python dùng môi trường có sẵn, chỉ đọc: `D:/RCA-ext/envs/py312-pin/Scripts/python.exe`. CIRCA gốc import từ clone của task. Revision nằm trong manifest của nhánh chính.

Nguồn runtime và công cụ: [CRAN R 4.4.2](https://cran.r-project.org/bin/windows/base/old/4.4.2/R-4.4.2-win.exe), [innoextract 1.9](https://github.com/dscharrer/innoextract/releases/tag/1.9). CRAN MD5 xác nhận installer R; các binary gói có MD5 khớp metadata PACKAGES. SHA256 đã lưu để dựng lại. Giải nén archive có kiểm đường dẫn thành viên nằm trong thư mục đích.

`setup_r_packages.py` lấy Depends/Imports của pcalg từ CRAN Windows R 4.4 và Bioconductor 3.20. Host Bioconductor gốc trả HTTP 403 ở lượt một, nên dùng Posit trong [danh sách mirror chính thức](https://bioconductor.org/about/mirrors/). Lượt hỏng giữ ở `r-packages-setup.log`; lượt thành công ở `r-packages-setup-lan2.log`. Không cài Rtools hay gói từ source. Môi trường không cần quyền quản trị.

Các lệnh chạy dùng biến môi trường chỉ trong process PowerShell; không thay cấu hình hệ thống:

```powershell
$env:R_USER='D:/RCA-ext/work/T-014'
$env:R_LIBS_USER='D:/RCA-ext/work/T-014/R-library'
$env:TEMP='D:/RCA-ext/work/T-014/tmp'
$env:TMP=$env:TEMP
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
& D:/RCA-ext/work/T-014/R/app/bin/Rscript.exe results/T-014/audit/run_pcalg.R
& D:/RCA-ext/work/T-014/R/app/bin/Rscript.exe results/T-014/audit/run_mem_pcalg.R
```

Python thêm `PYTHONDONTWRITEBYTECODE=1`, `PYTHONHASHSEED=0`, `PYTHONPATH=D:/RCA-ext/src/RCAEval` rồi dùng `-B`. Không ghi `__pycache__` vào môi trường hoặc source chỉ đọc.

R cảnh báo locale `C.UTF8` không được Windows hỗ trợ và một số binary được build bằng R 4.4.3. Các cảnh báo giữ nguyên trong log. Hai ca PC đầu tiên và target MEM được kiểm bằng kết quả thực, không chỉ dựa vào việc import thành công. RHT gốc được đối chiếu từng điểm với RCAEval trên hai ca trước đó.

Lượt DA đầu hỏng trong `py312-pin`: networkx2.5 thiếu `topological_generations`, giữ ở `mem-prior-scoring.log`. Lượt2 dùng môi trường mới `D:/RCA-ext/envs/T-014-main/Scripts/python.exe` của nhánh chính, networkx2.8.8; không sửa môi trường đó. Numpy1.26.4/pandas2.2.3/scipy1.14.1/sklearn1.6.0 giữ như pin trước. Mọi điểm linear RHT trên25ca tính lại trong runtime mới khớp từng điểm đã lưu ở runtime cũ. Ba cấu hình scorer mới, kiểm DA và fixture SCC dùng runtime này. Môi trường đã có nên nhánh audit không tải thêm Python package.

Dung lượng tải thành công R/công cụ/metadata/gói là 127.248.221 B theo cuối `r-packages-setup-lan2.log`; cộng ba artifact cấu hình Figshare 2.956.366 B. Lượt metadata thất bại trước đó đã tải thêm 971.145 B rồi gặp HTTP 403, nên lượng mạng đã biết cộng dồn là 131.175.732 B, dưới 1 GB. Không tải dữ liệu mới. Hash và byte từng file nằm trong manifest; số này không phải dung lượng R sau giải nén.

