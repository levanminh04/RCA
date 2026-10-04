# Môi trường dùng trong T-018

Không tạo môi trường mới, không cài gói nào. Chỉ dùng môi trường có sẵn, không sửa.

| Môi trường | Dùng cho | Kiểm |
|---|---|---|
| `D:\RCA-ext\envs\py38-gdn` (Python 3.8.10; torch 1.5.1+cpu, torch_geometric 1.5.0, numpy 1.19.5, pandas 1.4.4, scipy 1.10.1) | `scripts/chay_gdn.py`, `tinh_tay_gdn.py`, `phan_tich_gdn.py` | `pip freeze` ngày 04/10 trùng hệt `results/T-005/runs/freeze-py38-gdn.txt` (LOG). Cách dựng: `results/T-005/moi-truong.md` mục 5 |
| `D:\RCA-ext\envs\py312` (Python 3.12; pandas 3.0.6, numpy 1.26.4, pyarrow 25.0.1) | `scripts/chuan_bi_gdn.py`, `dem_cot.py`, `tai_moc_tiem.py`, `tao_bien_the.py`, `retrieval_ngau_nhien.py` | Cùng môi trường T-005 dùng để dựng dữ liệu GDN; chọn để file CSV dựng lại so được từng byte với T-005 (đã trùng SHA-256). Phiên bản theo `results/T-005/runs/freeze-py312.txt` |
| Python hệ thống `py -3` | `kiem_dan_dong.py` (chỉ thư viện chuẩn) | — |
| `pdftotext` của MSYS2 (`/mingw64/bin/pdftotext`, đi kèm Git Bash) | trích văn bản PDF | — |

Code: GDN `D:\RCA-ext\src\GDN` revision `9853899`, `git status` sạch trước và sau task (kiểm ở cuối LOG). RCAEval `D:\RCA-ext\src\RCAEval` chỉ đọc (`git show` ở commit `fb8f20a`).

Số luồng: R1 dùng mặc định của torch (12, như T-005); các lượt khác ghi `--threads` trong `runs/<nhan>.log` và `tom-tat.json`.
