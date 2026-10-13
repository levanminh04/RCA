# Phân phối T033 sang hai EC2

T33 giữ ca 1–14. T32 nhận ca 15–30, chia theo parity của thứ tự nguồn, hai worker. Nhánh native full sham và bảy nhánh bổ sung giữ nguyên mỗi ca. Kết quả PASS phải giữ như nguồn; không tạo marker giả.

Payload mới gồm native `_bocpd.py` đúng hash; mỗi ca là NPZ nén chứa nguyên X/times/columns/m/CP_flags từ nguồn đã pin và raw causal selector columns từ metrics đã pin. Không chuyển R, predictive density, nhãn, file raw toàn bộ. Manifest nối hash payload đến nguồn gốc. Wrapper thay đường dẫn/input transport và assignment; giữ nguyên `causal`, `run_engine`, phép biến đổi và gates. Packages numpy/pandas/scipy phải đúng version nguồn. Native full sham từng ca so m và CP EXACT trước dùng kết quả can thiệp. Nếu gate không đạt dừng ca/phần phụ thuộc, giữ attempt.

Worker v3 cũ đọc vòng ca vào memory. Monitor mới không sửa v3: khi stdout ghi START native-full-sham cho ca ngoài ownership (15 hoặc16), kiểm PID/cmdline rồi SIGSTOP, lưu PID/elapsed/log/start mới và trạng thái interrupted, SIGTERM+SIGCONT để kết thúc process. Mọi branch trong ca ownership trước đó đã ghi output trước START này. Không gọi native mới đang bắt đầu là complete. Giữ supervisor/output/attempt cũ. Nếu worker cũ chưa đến boundary thì tiếp tục bình thường. Không kill branch đang làm của ca được giao.

Hai máy ghi roots riêng; nhận kết quả nhỏ có receipt hash vào workroot local rồi tổng hợp theo case/branch ownership. Không sửa output hoặc catalog cũ. Ca bị lỗi trên nhánh bổ sung giữ ERROR và các ca độc lập còn lại được xử lý theo nguồn lỗi; native gate/hash mismatch là dependency stop.
