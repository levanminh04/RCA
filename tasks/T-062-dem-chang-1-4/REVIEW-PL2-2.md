# Phản biện T-062 phụ lục 2 — lượt 2 (L1d: điều khiển tải trên `exp-obs`)

- **Người phản biện:** Claude (điều phối chiến dịch). **Ngày:** 13/11/2026 ~05:50Z.
- **Đầu ra được phản biện:** `results/T-062/tai-2/tai_linux.py`, `linux-source-manifest.json`, `BAN-GIAO-4-linux.md`, `linux/check/`, `out/l1linux20261113{a,b}/`, `out/l1ps20261113{a,b}/`; bản triển khai `exp-obs:~/rca-dieu-phoi/`.
- **Đã tự kiểm:**
  - Đọc toàn bộ `tai_linux.py`.
  - Đối chiếu `linux/check/comparison.json` (`/runs/*/totals`, `/pairs`) với bảng bàn giao: khớp từng số.
  - So sha256 của `tai_linux.py` và `linux-source-manifest.json` giữa repo và `exp-obs`: trùng.
  - Chạy `tai_linux.py stop --tag khong-ton-tai-x` trên `exp-obs`: `ok`, `stopped: []`, không chạm workload khác.
  - Kiểm máy tải trống trước lượt thử của bộ chạy.
  - Dùng `tai_linux.py` qua `runner3.py` trong lượt thử một chu kỳ trên `exp-obs` (kết quả ghi ở T-063).

## Kết luận chung

Đạt yêu cầu của lời nhắn L1d. Bốn lệnh có cùng hành vi với bản PowerShell trên cùng image, script và cấu hình k6. Hai cặp lượt cho thấy:

- Cấu hình chạy bằng nhau (`/pairs/*/runConfigEqual = true`).
- 0 hành trình lỗi, 0 lỗi 401 trong k6, 0 lượt rơi (`dropped_iterations`).
- Mỗi lượt Linux ít hơn 1 hành trình. Bàn giao giải thích bằng lượt bắt đầu cuối ở biên thời lượng: PS có lượt ở 150,001 s / 180,001 s, Linux lượt cuối ở 149,167 s / 179,723 s.

Chênh này cùng cỡ với chênh giữa hai lượt PowerShell đã chấp nhận (0,161%). Nó không ảnh hưởng mục đích dùng: tải nền cho chu kỳ 30 phút. Tôi chấp nhận `tai_linux.py` làm bộ điều khiển tải của đợt thu dev bản 2 chạy trên `exp-obs`.

Việc tìm và sửa lỗi stdin (SSH con nuốt phần script của caller) là phát hiện có ảnh hưởng thật. `runner3.py` cũng phòng lỗi này: `tai()` dùng `stdin=DEVNULL`, và bộ chạy được phát với `</dev/null`.

## Các điểm

**R1 — Linux lượt b có 5 lần refresh token, PS lượt b có 0. KHÔNG CHẶN.**
- Hai bên dùng cùng script k6 và ngưỡng tuổi 200 s. Không có refresh thất bại hay 401.
- Khác biệt có thể do tuổi token ở lúc bắt đầu. Linux cấp pool 40 token ở bước preflight. Phần này chưa được tách riêng.
- Chu kỳ thu dài 1.800 s nên vẫn phải refresh. Lượt chuẩn L1 đã refresh ổn trên PowerShell.
- Sửa tối thiểu: không cần. Bộ chạy theo dõi `token_refresh_failure` và `gateway_401` ở mỗi chu kỳ qua đầu ra k6 đã nhận.

**R2 — Mỗi `start` đều cấp pool mới qua PKCE trên `exp-app` (`force=True`). KHÔNG CHẶN; ghi nhận.**
- Mỗi chu kỳ có thêm một đợt đăng nhập Keycloak trước mốc tải. Đợt này nằm ngoài cửa sổ ±600 s quanh `t`: `t = S + 600`, và cấp pool xong trước `S`.
- Keycloak sẽ có thêm lưu lượng ở đầu nền, giống bản PowerShell. Đây không phải thay đổi mới.

## Bất đồng còn lại / câu hỏi mở

Không có bất đồng với người làm. Mở: R1 (nguồn gốc khác số refresh), theo dõi trong đợt thu.

## Phản hồi của người làm

| Điểm | Người làm kết luận | Minh quyết |
|---|---|---|
| R1 | | |
| R2 | | |
