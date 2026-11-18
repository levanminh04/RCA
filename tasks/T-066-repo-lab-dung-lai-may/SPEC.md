# T-066 — Repo lab chạy được; dựng lại exp-obs và máy tải (W1)

- **Trạng thái:** đã duyệt (17/11/2026, bản 2)
- **Người làm:** Claude
- **Người phản biện:** Codex
- **Thuộc gói MRP:** P9, P10 (hạ tầng cho demo và đánh giá) — **Cổng:** chuẩn bị G6

Lịch sử soạn: bản 1 và bản 2 trình trong chat 17/11/2026; Codex soát bản 1 (7 điểm chặn, Claude kiểm cả 7 đều đúng); bản 2 sửa theo các điểm đó. File này là bản 2 ghép đầy đủ. Quyết định của Minh ghi ở `LOG.md` phiên 1.

## Mục tiêu

Kế hoạch [giai đoạn 2 §8.2](../../docs/techstack/KE-HOACH-GIAI-DOAN-2.md) W1. MRP P9b yêu cầu dịch vụ RCA đọc kho quan sát. DT18-NV3 yêu cầu áp dụng phương pháp trên hệ bán vé.

Đây là task **cài đặt và chuyển hạ tầng**, không phải đánh giá. Xong task này mới đủ điều kiện làm W2–W5 trên hạ tầng mới. Task không trả lời câu hỏi nghiên cứu nào; nó chỉ bảo đảm chuyển chỗ chạy không làm đổi kết quả M1 và tuyến chạy một ca mới đi trọn.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Giải thích khác cần loại | Phép kiểm và bằng chứng | Phần còn mở |
|---|---|---|---|
| Chuyển code sang repo lab có làm đổi kết quả M1 không? | Đổi đường dẫn, phiên bản thư viện hoặc biến môi trường có thể đổi đầu ra | Chạy V082 từ vị trí mới trên 2 ca đã lưu: 46aab4be và ebd5ef38. So `method-output-1.json` ở `d=0` với manifest-3 của T-064, phải trùng từng byte. Không so `summary.json`, vì file này chứa thời gian chạy. Ghim đầu vào (gói ca, gói bổ sung, gói R9 của ebd5ef38), mã, cấu hình, phiên bản Python và `pip freeze`. | Lệch thì dừng, lần nguyên nhân, không tiếp tục các bước phụ thuộc. |
| Bộ xuất chung có tính `live-down` đúng như R9 không? | Công thức tổng quát hóa có thể khác bản R9 viết riêng cho một ca; công thức cũ làm mất trạng thái PAUSE (WHY-99) | Chuẩn là các gói đã lưu trong archive. So từng bộ `(URL, timestamp, giá trị)` với 6 gói R9 của ebd5ef38 **và** gói của 46aab4be (ca PAUSE) ở `d=0`. Trước khi xuất lại từ Prometheus, kiểm kho còn đủ dữ liệu ở các mốc cần (giới hạn 30 ngày / 40 GB). | Prometheus còn dữ liệu tới khoảng 10/12, nên phép so phải làm trước mốc đó. |
| Tuyến chạy một ca mới từ repo lab có đi trọn không? | Mỗi khâu chạy riêng thì ổn, ghép lại thì gãy | Tuyến nghiệm thu: tải → stage (đọc vùng ghi mới trong `/srv/rca-lab/collector-gateway`) → xuất bổ sung theo R9 → V082 (`chay_ca.py`, `cau-hinh-de-xuat.json`, bản chụp mã `goc-12`) → chuyển G1 → cập nhật chỉ mục → **mở đúng mã ca vừa chạy** trong Grafana. Kiểm `cau_hinh_sha256` và `ma_nguon_sha256` trong đầu ra của ca mới. Chạy trên bản hệ thống hiện tại (`6b21ed55`). | — |
| Hai user `rca`, `ledger` có cách ly sổ tiêm (nhãn) khỏi phương pháp không? | Tạo user nhưng tiến trình vẫn đọc được sổ | Tiến trình M1 chạy bằng user `rca`; `sudo -u rca cat <sổ tiêm>` phải bị từ chối; user `ledger` ghi được sổ; sổ chỉ được đọc ở bước ghép nhãn, sau khi đầu ra đã băm. | — |
| Dọn được gì trên máy? | Thư mục tưởng là rác nhưng còn được dùng | Đối chiếu từng đầu vào lịch sử với `D:/RCA-archive`; grep đường dẫn trong code của lab. | Danh sách xóa trình Minh; **không xóa trong task nếu chưa duyệt danh sách**. |

## Đầu vào

- Repo lab `D:/Project/flashticket-rca-lab` tại commit `a46c009`.
- `D:/RCA-archive` (đã kiểm hash; có gói ca `ebd5ef38` và gói đầu vào M1 `exp-obs/m1ft-inputs/`).
- `results/T-064/` (`manifest-3.json`, `cau-hinh-de-xuat.json`, `kiem/r9/`).
- `results/T-058/dem-2026-11-10/{stage-m1.py, run-m1.py, safe-export.py}`.
- Ba máy, cách gọi theo `docs/STATE.md`.

Không mở dữ liệu khóa.

## Đầu ra

- **Repo lab:**
  - `campaigns/runner/` có đủ `stage_m1.py`, `run_m1.py`, `safe_export.py`; đường dẫn capture của `stage_m1` trỏ vào `/srv/rca-lab/collector-gateway`;
  - một module đọc `inventory/` (`campaigns/lib/inventory.py`);
  - các script và profile tải không còn IP viết cứng;
  - `xuat_bo_sung.py` dùng cách tính "lần dò mới nhất";
  - danh sách thư viện ghim để dựng lại venv (`pip freeze`);
  - `campaigns/README.md` hướng dẫn chạy.
- **Máy:** exp-obs và máy tải chạy từ `/opt/rca-lab` (đúng commit đã ghim), bí mật ở `/etc/rca-lab`, dữ liệu ở `/srv/rca-lab`. Bản chụp mã M1 ở `/srv/rca-lab/m1-snapshots/<hash mã>/`. `inj3` đặt ở `/opt/rca-lab` trên exp-app, gọi qua repo lab.
- **`results/T-066/`:**
  - `phu-thuoc.md`: mọi đường dẫn mà runner, bộ xuất, stage, tải, tiêm đọc tới; nguồn và hash của từng cái;
  - `hoi-quy-v082.json`: hash `method-output-1.json` cũ và mới của 2 ca, kèm ghim đầu vào, mã, Python, `pip freeze`;
  - `r9-tong-quat.json`: so từng bộ `(URL, timestamp, giá trị)` với 7 gói chuẩn;
  - `cach-ly-nhan.md`: kết quả phép kiểm hai user;
  - `e2e-001/`: tuyến một ca mới, nhật ký và hash;
  - `tempo-tang-truong.md`: tốc độ tăng dung lượng Tempo trong 24 giờ, mức tải lúc đo, mức giữ đề xuất;
  - `danh-sach-xoa.md`: từng mục, bằng chứng còn bản hoặc dựng lại được, dung lượng;
  - `thay-doi-may.md`: mọi thay đổi trên máy, kèm hash trước/sau và cách hoàn tác.

## Phạm vi ghi

Ngoài `LOG.md` của task này và dòng T-066 trong `docs/STATE.md`:

- Repo `D:/Project/flashticket-rca-lab`: mọi thư mục. Commit và push lên `main` của repo lab theo luật cứng 11 (đề xuất nội dung commit, Minh duyệt).
- `results/T-066/`.
- **exp-obs:** tạo `/opt/rca-lab`, `/etc/rca-lab`, `/srv/rca-lab`; tạo user `rca`, `ledger` (PLAN-TRIEN-KHAI §5.1); tạo cặp khóa ed25519 riêng cho bộ điều khiển (Q1(b)); chuyển compose quan sát sang file của repo lab, giữ project `flash-ticket-obs-pinned` và giữ nguyên volume.
- **Máy tải:** tạo `/opt/rca-lab`, `/etc/rca-lab`, `/srv/rca-lab`; thêm một dòng vào `authorized_keys` của user `ubuntu`.
- **exp-app:** tạo `/opt/rca-lab` cho `inj3`; thêm một dòng vào `authorized_keys` của user `ubuntu`; chạy tuyến một ca bằng các công cụ đã có. Không đổi container ứng dụng; việc đó thuộc T-067.
- **Không xóa gì trên máy** cho tới khi Minh duyệt `danh-sach-xoa.md`. Xóa theo danh sách đã duyệt nằm trong phạm vi task.

## Các bước

1. Lập `phu-thuoc.md` bằng lệnh chỉ đọc. Kiểm: grep đường dẫn trong mọi script; so hash bản trên máy với bản trong repo RCA.
2. Viết module `inventory`. Sửa `tai_linux.py`, `runner4.py`, `fixture.py`, `deploy-t062.sh`, `stage_m1` và các profile tải để đọc địa chỉ từ đó. Kiểm: `git grep` không còn IP trong `campaigns/`, `load/`, `app-host/scripts/`, `faults/`.
3. Đưa cách tính R9 vào `xuat_bo_sung.py` cho ca và cửa sổ bất kỳ. Kiểm bằng `r9-tong-quat.json` (7 gói chuẩn).
4. Dựng thư mục và user trên exp-obs và máy tải. Chép (không di chuyển) bí mật sang `/etc/rca-lab`. Kiểm bằng hash của bản chép. Dựng venv từ danh sách ghim.
5. Khóa bộ điều khiển (Q1(b)): tạo cặp ed25519 **ngay trên exp-obs**, khóa riêng không rời máy, quyền 600. Mỗi máy đích thêm một dòng vào `authorized_keys` của `ubuntu`, ghi chú `rca-lab-controller`. Giá trị `from=` lấy theo **địa chỉ nguồn đo thực tế** khi kết nối thử (log sshd ở máy đích). Dự kiến exp-app thấy `10.0.0.215`, máy tải AWS thấy `213.35.116.128` [chưa kiểm]. **Thu hồi:** xóa dòng đó và xóa khóa.
6. Phép cách ly hai user (bảng ở trên); ghi `cach-ly-nhan.md`.
7. Chuyển JSON kết quả và chỉ mục sang `/srv/rca-lab/rca-results`. Bật lại Grafana bằng compose của repo lab. Kiểm: đủ 9 dashboard đúng UID, truy vấn được trace và log ngày 12/11, trang phát lại mở được ca cũ. **Hoàn tác:** chạy lại compose cũ ở `/opt/flash-ticket-obs/pinned`, giữ nguyên tới cuối task.
8. Phép hồi quy V082 trên 2 ca đã lưu.
9. Tuyến một ca mới (bảng ở trên). Khung giờ trên exp-app tách khỏi T-067: T-066 chạy tuyến này trước, T-067 dựng lại container sau.
10. Đo tốc độ tăng của Tempo trong 24 giờ, ghi kèm mức tải lúc đo; chạy song song với phần chuẩn bị của T-067. Đề xuất mức giữ.
11. Lập danh sách xóa, trình Minh; Minh duyệt thì xóa và ghi lại.

## Kiểm đúng đắn

- **Phép chính:** hồi quy từng byte của `method-output-1.json` trên 2 ca; bộ xuất mới trùng 7 gói chuẩn từng bộ `(URL, timestamp, giá trị)`; đầu ra ca mới mang đúng `cau_hinh_sha256` và `ma_nguon_sha256`.
- **Không kiểm được trong task này:** hành vi trên bản FlashTicket mới (T-067, W3).
- **Tách lỗi:** tuyến một ca hỏng vì máy hoặc mạng thì ghi là lỗi hạ tầng, không phải kết quả.

## Tiêu chí xong

1. Hai ca hồi quy: `method-output-1.json` ở `d=0` trùng byte với manifest-3 T-064.
2. Bộ xuất mới trùng 7 gói chuẩn (6 gói R9 ebd5ef38, gói 46aab4be `d=0`).
3. Tuyến một ca mới chạy trọn từ repo lab và mở đúng mã ca đó trong Grafana; hai trường hash khớp.
4. Grafana đủ 9 UID, dữ liệu cũ đọc được.
5. Không còn IP viết cứng ngoài `inventory/`.
6. Phép cách ly hai user đạt.
7. `danh-sach-xoa.md` đã trình kèm bằng chứng.
8. LOG ghi rõ commit của repo lab đã triển khai.

## Không làm

- Đổi phiên bản FlashTicket (T-067).
- Luật cảnh báo (W4).
- Chế độ (b) (W5).
- Tách runner thu dữ liệu và runner RCA cho W7 (thuộc W6).

## Chi phí ước lượng

- Khoảng 1,5–2 ngày công [ước lượng, chưa đo].
- Tuyến một ca dưới 1 giờ; đo Tempo 24 giờ chạy nền, không chiếm máy.
- Không tải thêm dữ liệu. Không thuộc diện luật cứng 8.

## Rủi ro và điều chưa chắc

- Có khóa nằm trên máy chủ (Q1(b)). Gỡ chỉ cần xóa một dòng trong `authorized_keys` ở máy đích và xóa khóa.
- Địa chỉ nguồn mà máy tải AWS thấy [chưa kiểm]; nếu khác dự kiến, `from=` theo số đo thực tế.
- Grafana ngắt vài phút khi chuyển compose.
- Dữ liệu Prometheus ở các mốc của R9 có thể đã bị cắt bớt trước khi so (giới hạn 30 ngày / 40 GB); kiểm trước khi xuất lại.
- Gói ca ebd5ef38 trước đây chỉ có trên exp-obs; nay đã có bản ở `D:/RCA-archive/exp-obs/cases/` (khớp hash).

## Prompt bàn giao

Ở `LOG.md`.
