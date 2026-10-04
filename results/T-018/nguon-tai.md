# Nguồn đã tải trong T-018

Mọi file nằm ở `D:\RCA-ext\work\T-018\nguon\` (ngoài repo, không đưa vào git). Báo trước trong LOG trước khi tải. Tổng dưới 5 MB, dưới giới hạn 1 GB.

| File | Nguồn | Kích thước (B) | Kiểm | SHA-256 |
|---|---|---|---|---|
| `decomprca-2609.36686v1.pdf` | `https://arxiv.org/pdf/2609.36686v1` | 659 472 | Content-Length khớp; tải hai lần, SHA-256 trùng | `2269ec70025494a7b4659ae6835360c113e4f2a6a3328cdad7219e8c9ec9468d` |
| `gdn-2106.06947.pdf` | `https://arxiv.org/pdf/2106.06947` (v1, 13/06/2021) | 1 408 689 | như trên | `e2b32f5f4f806de754a9c6e8157a96948da5f9c5f3f565daad16b3bb608dfcef` |
| `decomprca.txt` | `pdftotext -layout` (MSYS2 `/mingw64/bin/pdftotext`) từ PDF trên | — | dùng để dẫn "PDF dòng N" | `773614466c9dad6ad0811561f1af75ba439406d9d906d3bea23b09c95b167740` |
| `gdn.txt` | như trên | — | dùng để dẫn "bài, dòng N" | `e9ca3ae7fe751f0d931d5e86859603fd537b4f221e95962e545fc38d609234d1` |
| `DecompRCA/` | `git clone https://github.com/cruiseresearchgroup/DecompRCA` | 1 911 249 (cả `.git`) | commit HEAD `f99d2172ad3ba1d584d947c075d69fc9bbc09064` (29/09/2026); 76 file theo `git ls-files`; không có file kết quả từng ca | — |
| `rcaeval-inject/<ca>/inject_time.txt` (30 ca dev RE2-TT) | HF `phamquiluan/RCAEval` revision `afeacb11bcc94dadfd1c8f483ee4377b2b8b614e`, đường dẫn `<ca>/inject_time.txt` | 10 mỗi file, tổng 300 | git blob oid khớp HF 30/30; 30/30 bằng điểm giữa timestamp metric; 5 file trùng bản T-005 (`D:\RCA-ext\dl\rcaeval-inject\`), 1 file trùng bản có sẵn trong `data/` (`runs/tai-moc-tiem.json`; `scripts/tai_moc_tiem.py`) | xem `runs/tai-moc-tiem.json` (oid) |

Lấy lại trên máy khác:

```
curl -L -o decomprca-2609.36686v1.pdf https://arxiv.org/pdf/2609.36686v1
curl -L -o gdn-2106.06947.pdf https://arxiv.org/pdf/2106.06947
git clone https://github.com/cruiseresearchgroup/DecompRCA && git -C DecompRCA checkout f99d2172ad3ba1d584d947c075d69fc9bbc09064
pdftotext -layout decomprca-2609.36686v1.pdf decomprca.txt
pdftotext -layout gdn-2106.06947.pdf gdn.txt
D:/RCA-ext/envs/py312/Scripts/python.exe results/T-018/scripts/tai_moc_tiem.py
```

Số dòng văn bản PDF phụ thuộc bản `pdftotext`; dùng đúng SHA-256 của file `.txt` ở bảng trên để đối chiếu.
