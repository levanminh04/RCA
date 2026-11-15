# Brief cho Codex — kiểm giao diện G2 trên Grafana `exp-obs` THẬT (T-062, bước G1)

Bạn là Codex, được phiên Claude điều phối T-062 giao việc **kiểm vận hành (chỉ đọc)** giao diện G2 trên chính Grafana `exp-obs`. Minh (chủ đồ án) cho phép (chat 12/11/2026): *"tôi cấp quyền cho bạn đọc mật khẩu grafana để xem dashboard và test lại, cấp cho codex nữa … đây là đồ án … hiện chỉ đang demo … rà soát trong phạm vi có thể, vẫn tuân thủ những yêu cầu khác của task"*. Đọc `AGENTS.md` mục 3 và `tasks/T-062-dem-chang-1-4/SPEC.md` (mục "Luật cứng của lượt") trước khi làm.

**Không phải phản biện chính thức.** Đang có một lượt Codex khác phản biện G1 (`tasks/T-062-dem-chang-1-4/REVIEW-G1*.md`, `results/T-062/giao-dien/prompt-phan-bien-g1*.md`). **Không đọc kết luận, không ghi, không đụng** các file đó và không chạm tiến trình đó. Việc của bạn là đo hành vi thật trên Grafana; bản phản biện kia là việc riêng.

## Bối cảnh

- Giao diện: `results/T-062/giao-dien/XONG.md` (cách mở, panel, giới hạn), `dinh-dang-chi-muc.md`, file dashboard `results/T-062/giao-dien/grafana/dashboards/rca-g2-chinh.json` và bộ sinh `dung-dashboard.py`. Dashboard uid `rca-g2` (trang chính, không đáp án) và `rca-g2-phat-lai` (có đáp án).
- Dữ liệu thật: 9 ca T-062 trong `/opt/flash-ticket-obs/rca-ket-qua/` (exp-obs), bản local `results/T-062/ket-qua/` và `ket-qua/phat-lai/` (gồm `bang-cham.json`). Grafana đọc qua `http://localhost:3000/public/rca/...` trong container.
- Máy: `ubuntu@213.35.116.128`, khóa `D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key`, known_hosts `D:/RCA-ext/overnight-T058/out/known_hosts`. Grafana nghe `10.0.0.215:3000`. ssh: `C:/Program Files/Git/usr/bin/ssh.exe`.
- Thông tin đăng nhập: `/opt/flash-ticket-obs/grafana.env` (khóa `GF_SECURITY_ADMIN_USER`, `GF_SECURITY_ADMIN_PASSWORD`, chỉ root đọc).

## Việc

1. Mở đường hầm riêng **cổng 13000** (không dùng 3000 — có thể đang được dùng): `ssh -N -L 13000:10.0.0.215:3000 …` chạy nền; đóng khi xong.
2. Đăng nhập: đọc hai khóa trên **trong bộ nhớ** (ví dụ `ssh … 'sudo grep -E "^GF_SECURITY_ADMIN_(USER|PASSWORD)=" /opt/flash-ticket-obs/grafana.env'` vào biến của một tiến trình Python/Node; không echo, không ghi file, không đưa vào tham số dòng lệnh hiển thị, không lưu cookie/phiên ra đĩa).
3. Kiểm bằng trình duyệt headless nếu có sẵn trên laptop (Playwright/Chromium/Edge qua CDP; được cài gói Python/npm vào thư mục tạm của bạn, **không** cài hệ thống, tải < 1 GB) — nếu không có thì kiểm mức API (`/api/dashboards/uid/...`, `/api/ds/query` với đúng truy vấn và biến của dashboard). Với **mỗi ca trong 9 ca**:
   - Trang chính: danh sách có đủ 9 dòng, đúng mã/mốc/kết luận/nghi nguồn so với `results/T-062/ket-qua/chi-muc/danh-sach-su-co.json`; chọn ca → bản ghi sự cố, đồ thị (số nút, số cạnh, nhãn/màu theo vai trò so với `ket-qua/<mã>.json`), bảng hạng (khớp `nut[].hang`), bằng chứng của thành phần hạng 1 không rỗng; panel nào báo lỗi/"No data" ghi rõ.
   - Liên kết Explore (Tempo/Loki/Prometheus) từ menu nút và bảng bằng chứng: URL đúng datasource, đúng cửa sổ thời gian của ca; thử mở ít nhất một liên kết mỗi loại cho 2 ca và xác nhận có dữ liệu.
   - Trang phát lại: đáp án, họ lỗi, vai trò/hạng hiển thị có khớp `ket-qua/phat-lai/<mã>.phat-lai.json` và `bang-cham.json` không; ghi đúng như thấy (kể cả chỗ hiển thị gây hiểu nhầm), không tự diễn giải thêm.
   - Trang chính không lộ đáp án (không có chữ/trường đáp án).
4. Chụp ảnh màn hình (nếu có trình duyệt) vào `results/T-062/codex/g1-that/anh/`: trang chính có danh sách 9 ca; mỗi ô lỗi một ảnh đồ thị + hạng; một ảnh Explore; trang phát lại.

## Luật cứng (bắt buộc)

1. **Chỉ đọc trên Grafana:** không lưu/sửa/xóa dashboard, datasource, user, org, plugin, cài đặt; không tạo API key/service account. Không đổi gì trên exp-obs (không docker, không sửa file, không restart). Không đụng exp-app, máy tải, máy 84.
2. **Chỉ ghi** trong `results/T-062/codex/g1-that/` và file kết quả `-o` của lệnh này. Không sửa `results/T-062/giao-dien/`, `ket-qua/`, `tasks/`, `docs/`, `src/`, các `results/T-0xx/` khác.
3. **Không in, không ghi** mật khẩu, cookie, token vào bất kỳ file, log hay ảnh nào (ảnh không chụp trang đăng nhập có ô mật khẩu đã điền).
4. Không đọc dữ liệu khóa, không đọc sổ tiêm lỗi `results/T-062/tiem-loi/so.jsonl` (đáp án đã có trong file phát lại).
5. Nếu tồn tại `D:/RCA-overnight/STOP` thì dừng.
6. Không chạy hơn 60 phút; không tải > 1 GB.

## Báo xong

File kết quả (`-o`): dòng đầu `G1-THAT ĐẠT`, `G1-THAT ĐẠT MỘT PHẦN` hoặc `G1-THAT KHÔNG ĐẠT`. Sau đó: cách đã kiểm (trình duyệt hay API, phiên bản), bảng 9 ca × (danh sách, đồ thị, hạng, bằng chứng, Explore, phát lại) đạt/lỗi kèm số đo, danh sách ảnh, lỗi thấy được (panel, ca, thông báo nguyên văn), điều chưa kiểm được và vì sao. Không đề xuất sửa dashboard trừ khi kèm bằng chứng cụ thể.
