# -*- coding: utf-8 -*-
"""T-063 thu3 — kiểm ba điều kiện "exp-obs yên" của brief phiên B mục 2e trước khi phát lượt thu (chỉ đọc).
Dùng: py -3 -B results/T-063/thu3/scripts/kiem_truoc_phat.py   → in JSON; exit 0 nếu được phát, 1 nếu không."""
import json, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path(__file__).resolve().parents[4]
OBS = ['ssh', '-i', 'D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key', '-o', 'BatchMode=yes', '-o',
       'UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts', 'ubuntu@213.35.116.128']
kq = {}
r = subprocess.run(OBS + ['ps -eo cmd | grep -c "[c]hay_ca.py"; ps -eo cmd | grep -c "[r]unner[34].py thu"; '
                          'docker ps --format "{{.Names}}" | grep -c rca-tai- ; ls ~/rca-dieu-phoi/STOP 2>/dev/null | wc -l'],
                   capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=60)
n = [int(x) for x in r.stdout.split()]
kq['chay_ca_py'] = n[0]; kq['runner_thu'] = n[1]; kq['container_tai'] = n[2]; kq['stop_exp_obs'] = n[3]
kq['stop_laptop'] = Path('D:/RCA-overnight/STOP').exists()
d = json.loads((R / 'tasks/T-062-dem-chang-1-4/DIEU-PHOI-TRANG-THAI.json').read_text(encoding='utf-8'))
kq['dieu_phoi_lenh_nen_exp_obs'] = [x.get('mo_ta', '')[:80] for x in d.get('lenh_nen', []) if 'exp-obs' in x.get('loai', '')]
pc = R / 'results/T-064/phien-c/TRANG-THAI.json'
kq['phien_c_lo_exp_obs'] = json.loads(pc.read_text(encoding='utf-8')).get('lo_exp_obs') if pc.exists() else None
ok = (kq['chay_ca_py'] == 0 and kq['runner_thu'] == 0 and kq['container_tai'] == 0 and not kq['stop_exp_obs'] and not kq['stop_laptop']
      and not kq['dieu_phoi_lenh_nen_exp_obs'] and kq['phien_c_lo_exp_obs'] != 'dang_chay')
kq['duoc_phat'] = ok
print(json.dumps(kq, ensure_ascii=False))
sys.exit(0 if ok else 1)
