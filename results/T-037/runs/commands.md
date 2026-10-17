# Lệnh trong phiên

Các lượt đọc nguồn dùng Get-Content, rg và metadata Get-Item/Get-ChildItem trong đúng hai repo hiện hành. Đọc AGENTS/STATE/SPEC/LOG trước, rồi DT18/cô/MRP/LESSONS/WHY/DECISIONS/review-prompt/LOG T036 Phiên1; đọc source/code/output trước REVIEW T036. READMEs/diagrams do helper đọc theo source scope ở nguon.json. Không đọc data/locked hay test data.

Lệnh tạo/kiểm artifact (thứ tự):
1. `py -3 -X utf8 -B results/T-037/preflight.py`
2. Ghi oracle.json, nhận xét độc lập và nguyên lời giao trong LOG; hai helper chỉ tạo records-data/coverage-data và records-flow/coverage-flow.
3. Ghi counterexample-smtp.json trước runner; lấy mẫu CPU với Get-Process hai lần cách1giây, không process >0,25CPU-second.
4. `py -3 -X utf8 -B results/T-037/check-counterexample.py smtp-001` — lỗi đo RAM; giữ failure/code/input/oracle.
5. `py -3 -X utf8 -B results/T-037/check-counterexample.py smtp-002` — tái lập chặn2/2, không sửa input.
6. `py -3 -X utf8 -B results/T-037/collect-sources.py`
7. `py -3 -X utf8 -B results/T-037/finalize-blocked.py`
8. `py -3 -X utf8 -B results/T-037/verify-final.py` — kiểm cuối chỉ đọc kết quả/phạm vi, không thực nghiệm mới.

Hash đọc bằng SHA256 streaming1MiB, byte size và manifest; Python -B không tạo bytecode. Snapshot nguồn chỉ là tài liệu thiết kế đã đọc. Không chạy checker T036 (sẽ ghi ngoài phạm vi) hoặc full T037 graph converter sau chặn. Không download/giải nén/EC2/commit/push/chat ngoài.
