# File bỏ khỏi `main` của repo lab mà repo RCA chưa có bản sao

Chép nguyên byte bằng `git show truoc-don-2026-11:<đường>` từ repo lab (`github.com/levanminh04/flashticket-rca-lab`, tag `truoc-don-2026-11` = commit `4b6c4b2`), ngày 24/11/2026, trước khi `git rm` ở nhánh `don-2026-11` (kế hoạch `../KE-HOACH-DON.md` §6, K6). Đường dẫn bên dưới giữ nguyên đường trong repo lab.

File bỏ mà repo RCA **đã có** bản trùng blob git (không chép lại): `app-host/scripts/{build,prepare,rollback}-t062.*` → `results/T-062/ha-tang/scripts/`; `campaigns/g1/l8b-xuat.py` → `results/T-065/codex/` (bản này cũng được giữ trong lab dưới tên `rca/lib/g1_export.py`); `campaigns/runner/pool_prom.py` → `results/T-063/thu3/scripts/`; `campaigns/schedules/{lich-2,lich-3,lich-thu-ngan,lich-thu3-ngan}.json` → `results/T-063/`; `load/scenarios/legacy/*.js` → `results/T-062/`; 4 dashboard `90-archive` của T-065 → `results/T-065/grafana*`.
