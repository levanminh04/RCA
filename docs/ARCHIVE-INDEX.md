# Chỉ mục dữ liệu lưu trữ trên máy

Những gì không kéo về laptop, giữ trên máy ở `/srv/flashticket-rca/archive/<đợt>/`. Mỗi đợt có `README.md` ngay trên máy (đường cũ, nội dung, dung lượng, ngày dời). Không xóa khi Minh chưa duyệt.

## Đợt 2026-11 (dọn repo lab và ba máy, 24/11/2026)

- **Kế hoạch:** `results/T-070/don/KE-HOACH-DON.md`.
- **Bảng tra tên cũ → mới:** repo lab, `docs/name-map.md`.
- **Bản chép README trên máy:** `results/T-070/don/sau-don/archive-README-{obs,app,tai}.md`.

| Máy | Mục trong `archive/2026-11/` | Đường cũ | Nội dung | Dung lượng |
|---|---|---|---|---|
| exp-obs | `runs/` | `/srv/rca-lab/runs/*` | Nhật ký các lượt chạy T-068…T-073, e2e-001, tempo-do-t066; bộ nhận cảnh báo E3 (`t072-e3-01*`). ubuntu 700: có tên ô | 1,3 GB |
| exp-obs | `ledger/` | `/srv/rca-lab/ledger/*.jsonl` | Sổ tiêm lỗi của các lượt e2e-001, t069-chinh, t069-lap, t069-thu, t073-e5-01 (nhãn). ledger 700, user rca không đọc được | 260 KB |
| exp-obs | `rca-results/` | `/srv/rca-lab/rca-results` (trừ `t065-l11-001`) | Các bộ hiển thị cũ: t065-l3/l4/l8/l8b-001, t073-dev-001, t073-e5-001, JSON gốc, chi-muc, mau, phat-lai | 988 MB |
| exp-obs | `load-tai-out/` | `/srv/rca-lab/load-controller/tai-out` | Bản k6 thô nhận về exp-obs (47 tag); repo RCA có bản tóm tắt | 3,5 GB |
| exp-obs | `trace-goi/` | `/srv/rca-lab/trace-goi` | Gói trace ca lịch sử cho `service_graph.py --goi` | 2,0 GB |
| exp-obs | `venv-m1/` | `/srv/rca-lab/venv-m1` | Venv V082 cũ; venv mới `/srv/flashticket-rca/rca/venv` có `pip freeze` trùng | 451 MB |
| exp-obs | `m1/` | `/srv/rca-lab/m1/t069-phan-tich` | Phân tích T-069 (root:rca 750) | 8,3 MB |
| exp-obs | `home/`, `rca-results-chep-2026-11-17.sha256` | `/home/ubuntu/t063`, `/srv/rca-lab/` | File lẻ T-063; danh sách hash khi chép rca-results 17/11 | 1,1 MB |
| exp-app | `flash-ticket-app/` | `/opt/flash-ticket-app` (phần còn lại) | Compose và env cũ (compose, compose-exp, compose-t062, env, env-t062), collector cũ, l1-fixtures, state, file .bak | 1,3 GB |
| exp-app | `compose-t067/` | `/opt/flash-ticket-build/t067-compose` | Bộ Compose hiệu lực T-067 (đường cũ) | 144 KB |
| exp-app | `backups/` | `/srv/rca-lab/backups` | Sao lưu đích hoàn tác T-067 (`t067-20261118`) | 100 MB |
| exp-app | `build/` | `/opt/flash-ticket-build/t067-36a3725d-logs` | Log build bản 36a3725d; tiến độ triển khai lúc dọn | 6,7 MB |
| exp-app | `home/` | `/home/ubuntu/{t058,t062,t063,t071,…}` | Script và log T-058…T-071; `t071/db-moc` là mốc PostgreSQL của T-071 | 91 MB |
| exp-app | `opt-docs/` | `/opt/docs` | Nguồn bind MongoDB cũ (thư mục rỗng) | 20 KB |
| máy tải | `load-runs/` | `/srv/rca-lab/load-runs` | Bản k6 thô trên máy tải (47 tag) | 3,5 GB |
| máy tải | `home/` | `/home/ubuntu/{x86-check,uvenv,…}` | Thử kiến trúc máy tải ngày 10/11 | 450 MB |

Ngoài archive, vẫn giữ tại chỗ:
- `/opt/rca-tai` trên máy tải (quyết định Q5 ngày 23/11).
- Bộ ca dev `/srv/flashticket-rca/rca/online-dev` trên exp-obs, dùng để kiểm tuyến RCA trực tuyến.
