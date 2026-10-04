# Môi trường T-015

Các clone/môi trường chung chỉ đọc. Revision và hash nguồn nằm trong `manifest-inputs.json` và `src/microrank/PROVENANCE.json`. Không commit/push, không cài phần mềm quản trị.

EC2 đầu dùng lại `~/rca/envs/py312-pin` của T-007, Python3.12.3, numpy1.26.4/pandas2.2.3/pyarrow18.1.0. Pilot tại máy này; log uptime/free/ps lưu cùng console. Dọn `~/.sudo_as_admin_successful` đúng một lần đã xác nhận; không lặp ở máy hai.

Theo Minh, các lượt cần RAM chuyển sang EC2 thứ hai `3.26.62.217`, Ubuntu26.04LTS. Python hệ thống3.14.4 không được dùng tính điểm. Mọi file mới, runtime/cache/tmp/data/run nằm trong `~/rca/T-015/`; không thay hệ thống. Kết nối dùng `D:/RCA-ext/keys/key2.pem`, known_hosts riêng `D:/RCA-ext/work/T-015/known_hosts`. Không sao chép khóa.

Dựng lại bằng `scripts/setup_ec2_2.sh`: uv0.12.22 Linux dùng lại từ env/tools máy đầu, managed CPython3.12.3, venv T015/env; ghim numpy1.26.4, pandas2.2.3, pyarrow18.1.0, python-dateutil2.8.2, pytz2023.3, six1.16.0, tzdata2023.3. `uv pip check` đạt. File freeze/console/hash của setup nằm trong `runs/setup/` sau chép về. Khác compiler/libc với máy đầu được ghi nhận; so pilot giữa hai máy tại `runs/pilot-environment-repeat.json` đạt461 giá trị giống hệt, graph/count/rank cũng khớp.

```bash
export UV_PYTHON_INSTALL_DIR="$HOME/rca/T-015/python"
export UV_PYTHON_BIN_DIR="$HOME/rca/T-015/bin"
export UV_CACHE_DIR="$HOME/rca/T-015/cache"
export XDG_CACHE_HOME="$HOME/rca/T-015/cache"
export TMPDIR="$HOME/rca/T-015/tmp"
bash "$HOME/rca/T-015/bin/setup_ec2_2.sh"
```

Runtime tải64,2MiB; numpy/pandas/arrow67,4MiB theo console. Ước lượng trước là<100MB, thấp hơn thực tế. Đây là phần mềm, tách khỏi ngân sách tải telemetry. Không có telemetry công khai mới được tải. `scripts/transfer_ec2_2.py` chuyển đúng180fileOB và3devTT; `runs/transfer/expected.json` ghi189file, tổng960.754.806B. Chép sớm auth27.766.309B để ví dụ không chờ OB, tổng nếu tính bản chép lặp988.521.115B<1GB. Hash phải khớp trước chạy.

Windows có môi trường `py312-pin` không có parquet engine. I/O/footer nhẹ dùng env `py312` đã có; math dùng pin hoặc EC2. Không cài vào env chung. Laptop thiếu RAM nên không khởi MicroRank TT nặng. Các kiểm rẻ/toy ghi đúng interpreter; không dùng pandas3 cho kết luận số học của bản pin.

Mỗi lúc tối đa một worker nặng trên EC2. BLAS/OMP/MKL1luồng, PYTHONHASHSEED0/1; cache/tmp riêng, không ghi bytecode. Shell LF; lượt CRLF hỏng ở máy đầu được giữ `runs/ob-main/console.log`. Chạy bằng nohup và heartbeat/progress, mỗi khối chép kết quả về ngay. Thời gian tất cả lượt chỉ là chi phí quan sát, không benchmark chính thức trên máy độc quyền.



Kết quả chuyển được kiểm189file đúnghash/byte tại `runs/setup/input-verified.json`. Môi trường/executable/hash kernel và danh sách file riêng từng máy ở `runs/ec2-first-inventory/` và `runs/ec2-second-inventory/`; manifest output bàn giao ghi từng đường dẫn. Sau lỗi nullable và exact-copy, snapshot/lượt cũ được giữ cùng source tương ứng. Source cuối có guard conflict; lõi3hàm MIT không đổi.

Khối90OB chia30/30/29ca saupilot, dự báo17,9phút trước điểm. Tổng ba khối837,091s, pilotmáy2 12,068s; thêm rerun2ca12,864s và kiểm cửa sổ/maths/audit vẫn dưới1giờ, xa trần3giờ. Đây là chi phí quan sát, không số benchmark. Trước mọi lượt thấy một worker T015 hoặc máyidle; không chạy worker T015 cạnh worker nặngT014 máy đầu. Tổng TT mới3ca/controls cũng dưới10phút theo logs. Không Stop/reboot/đổi cấu hình EC2.
