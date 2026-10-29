# Giả lập checkout Windows (CRLF) để kiểm `tao_manifest.py --kiem` (N1)

- Commit: 57234546 (gói sửa sau phản biện lượt 1). Máy: cloud Linux, Python 3.12.3.
- Cách làm: `git worktree add --no-checkout --detach <tạm> 57234546`, rồi trong thư mục tạm, với
  `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.autocrlf GIT_CONFIG_VALUE_0=true`, chạy `git checkout 57234546 -- <đường dẫn>`
  và `python -B results/T-044/scripts/tao_manifest.py --kiem`. Xong thì `git worktree remove --force`.
- `kiem-thieu-gitattributes.json` — lượt hỏng, giữ theo luật cứng 10: chỉ checkout `src/m1`, `src/m1_danh_gia`,
  `results/T-044`, quên `.gitattributes`, nên git đổi cả file trong `results/` sang CRLF. Kết quả FAIL: 278 file trong
  `results/` lệch sha256; 29 file `src/` lệch sha256 nhưng khớp `git_blob`. Lượt này không giống checkout thật.
- `kiem-co-gitattributes.json` — lượt dùng: checkout `.gitattributes` trước, rồi ba thư mục trên. `src/*.py` có CRLF,
  file trong `results/` giữ LF (`results/** -text`). Kết quả PASS: 311 file, 0 lệch, 29 file `src/` ở `khop_git_blob`.
- Giới hạn: giả lập bằng `core.autocrlf=true` trên Linux, chưa chạy trên Windows thật. Trên Windows thật, kết quả còn
  phụ thuộc cấu hình git của máy (`core.autocrlf`); `git hash-object` áp cùng cấu hình đó nên vẫn cho blob đã cam kết.
