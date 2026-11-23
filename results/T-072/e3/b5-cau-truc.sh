#!/bin/bash
# T-072 E3 bước 5a: CHỈ ĐỌC cấu trúc 3 bảng của grafana.db (mode=ro). Không đọc bảng khác, không chép DB.
sudo -n python3 - <<'PY'
import sqlite3
db='/var/lib/docker/volumes/flash-ticket-obs-pinned_grafana-data/_data/grafana.db'
c=sqlite3.connect(f'file:{db}?mode=ro', uri=True)
for t in ('alert_rule','alert_instance','annotation'):
    r=c.execute("select name from sqlite_master where type='table' and name=?",(t,)).fetchone()
    print(t,'co' if r else 'KHONG CO')
    if r: print('  cot:',[x[1] for x in c.execute(f'pragma table_info({t})')])
PY
