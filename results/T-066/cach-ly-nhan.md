# T-066 — Phép cách ly sổ tiêm (nhãn) khỏi phương pháp

Bước 6, 17/11/2026 12:05Z, exp-obs, repo lab `5a39028` (`/opt/rca-lab`). Lệnh: một khối `ssh exp-obs` chạy các phép dưới đây bằng `sudo -n -u <user>`; đầu ra nguyên văn ở cuối file.

## Thiết kế đang kiểm

- Sổ tiêm của lượt mới: `/srv/rca-lab/ledger/<lượt>.jsonl`, thư mục `ledger:ledger 700`, file `600`.
- Runner (user ubuntu) ghi sổ qua `sudo -n -u ledger python3 -B /opt/rca-lab/campaigns/runner/ledger_append.py <sổ>`; `seq`, `prev_sha256` do helper tính (cùng quy tắc bản cũ).
- Tiến trình phương pháp: `run_m1.py` (P7) và `chay_ca.py` (V082) chạy bằng `sudo -n -u rca` (mã `runner4.py`: `chay_v082`, `m1_worker`). `stage_m1.py` chạy root, chỉ đọc vùng ghi Collector và Prometheus, không đọc sổ.
- Vùng phương pháp `/srv/rca-lab/m1` (`root:rca 750`); nhật ký lượt `/srv/rca-lab/runs` (`ubuntu 700`, có tên ô trong nhật ký) — rca không đọc được.

## Kết quả

| Phép | Mong đợi | Kết quả |
|---|---|---|
| ledger ghi sổ qua `ledger_append.py` (2 dòng) | được | ĐƯỢC; chuỗi `seq` 0→1, `prev_sha256` đúng |
| `sudo -u rca cat <sổ mới>` | từ chối | BỊ TỪ CHỐI |
| rca liệt kê `/srv/rca-lab/ledger` | từ chối | BỊ TỪ CHỐI |
| rca đọc sổ cũ `/var/lib/flash-ticket-ledger/ledger.jsonl` | từ chối | BỊ TỪ CHỐI |
| rca đọc sổ cũ `~ubuntu/rca-dieu-phoi/tiem-loi/so-thu2.jsonl` | từ chối | BỊ TỪ CHỐI |
| rca liệt kê `/srv/rca-lab/runs` | từ chối | BỊ TỪ CHỐI |
| rca ghi sổ qua `ledger_append.py` | từ chối | BỊ TỪ CHỐI |
| rca ghi vào bản chụp mã | từ chối | BỊ TỪ CHỐI |
| rca đọc `/srv/rca-lab/m1/cases` | được | ĐƯỢC |
| ledger đọc `/srv/rca-lab/m1/cases` | từ chối | BỊ TỪ CHỐI |

**Kết luận:** phép cách ly hai user đạt (tiêu chí xong 6). Trong tuyến của T-066 không bước nào đọc sổ: không có bước ghép nhãn (bộ chuyển G1 ở bước 9 không đọc sổ). Bước ghép nhãn (chấm điểm, phát lại có đáp án) sau này phải chạy sau khi đầu ra đã băm và bằng user ledger; điều này chưa kiểm trong task này vì chưa có bước đó.

Giới hạn: root và user ubuntu vẫn đọc được sổ (sudo). Phép kiểm chỉ bảo đảm tiến trình phương pháp chạy bằng rca không đọc được sổ; nó không chặn người vận hành.

File thử `/srv/rca-lab/ledger/kiem-cach-ly-t066.jsonl` (2 dòng thử, không phải sổ thật) giữ lại, vào danh sách xóa.

## Đầu ra nguyên văn

```text
2026-11-17T12:05:55Z
ledger ghi sổ: ĐƯỢC
ledger ghi dòng 2: ĐƯỢC
ledger đọc sổ (sudo -u ledger cat)                        ĐƯỢC
chuỗi hash: 0 1 True True
rca đọc sổ (sudo -u rca cat <sổ>)                       BỊ TỪ CHỐI (rc=1)
rca liệt kê thư mục sổ                                 BỊ TỪ CHỐI (rc=2)
rca đọc sổ cũ /var/lib/flash-ticket-ledger/ledger.jsonl  BỊ TỪ CHỐI (rc=1)
rca đọc sổ cũ ~ubuntu/rca-dieu-phoi/tiem-loi/so-thu2.jsonl BỊ TỪ CHỐI (rc=1)
rca liệt kê /srv/rca-lab/runs (nhật ký lượt có tên ô) BỊ TỪ CHỐI (rc=2)
rca ghi vào sổ qua ledger_append                            BỊ TỪ CHỐI (rc=1)
rca ghi vào bản chụp mã                                  BỊ TỪ CHỐI (rc=1)
rca đọc vùng M1 (cases)                                    ĐƯỢC
ledger đọc vùng M1 (cases)                                 BỊ TỪ CHỐI (rc=2)
/srv/rca-lab/ledger ledger:ledger 700
/srv/rca-lab/ledger/kiem-cach-ly-t066.jsonl ledger:ledger 600
uid=997(rca) gid=987(rca) groups=987(rca)
uid=995(ledger) gid=986(ledger) groups=986(ledger)
```
