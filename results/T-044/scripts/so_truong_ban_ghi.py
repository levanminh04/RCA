"""T-044: so từng trường bản ghi của bộ ca tất định (scripts/tat_dinh.py) giữa hai cây code, bỏ các trường mới thêm từ
lượt 1 tới lượt 4 (coverage nguồn metric, extra.kenh_co_the_gioi, extra.thong_ke_log, extra.E6b_pi, các trường mã,
inherited_by). In mỗi đường dẫn còn lệch, số lần và một ví dụ (ca, cũ, mới). Dùng để giải thích từng chỗ lệch khi
so_ban_ghi_truoc_sau.py báo bản ghi khác (lượt 4).
Lượt 5 (C7): inherited_by được so (trạng thái, lý do E9, đường, quy tắc; trừ các trường mã); `--day-du` so mọi trường,
không bỏ gì (dùng khi hai cây cùng định dạng mã).

    python -B results/T-044/scripts/so_truong_ban_ghi.py <gốc cây cũ> <gốc cây mới> [--day-du] > <ra>.txt
"""
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter

if len(sys.argv) > 2 and sys.argv[1] == '--mot-cay':
    goc = sys.argv[2]
    sys.argv = ['x']
    spec = importlib.util.spec_from_file_location('td', goc + '/results/T-044/scripts/tat_dinh.py')
    td = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(td)
    out = {}
    for ma_ca, spans, metrics, logs, them in td._ca():
        for ten, ch in td.CAU_HINH.items():
            td.chuoi.CACHE = td.e4.CacheCong()
            out[f'{ma_ca}|{ten}'] = td.chuoi.chay(spans, metrics, logs, td.U, {}, 1000, td._params(ten, ch, them))
    print(json.dumps(out, sort_keys=True, ensure_ascii=False))
    raise SystemExit
py = sys.executable
cu = json.loads(subprocess.run([py, '-B', __file__, '--mot-cay', sys.argv[1]], capture_output=True, text=True,
                               encoding='utf-8').stdout)
moi = json.loads(subprocess.run([py, '-B', __file__, '--mot-cay', sys.argv[2]], capture_output=True, text=True,
                                encoding='utf-8').stdout)
BO = re.compile(r'/extra/kenh_co_the_gioi|/extra/thong_ke_log|/extra/E6b_pi|/coverage/(?!trace|log)|/ma$|/don_vi$'
                r'|/giai_thich_ma$')
if '--day-du' in sys.argv[3:]:
    BO = re.compile(r'(?!)')  # không khớp đường dẫn nào
dem, vi_du, ca_lech = Counter(), {}, set()


def di(a, b, p, ca):
    if BO.search(p):
        return
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                if not BO.search(p + '/' + k):
                    dem[re.sub(r'/\d+', '/#', p + '/' + k) + ' (một bên)'] += 1
                    ca_lech.add(ca)
            else:
                di(a[k], b[k], p + '/' + k, ca)
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            di(x, y, f'{p}/{i}', ca)
    elif a != b or type(a) != type(b):
        k = re.sub(r'/\d+', '/#', p)
        k = re.sub(r'/m_thuc_the/[^/]+', '/m_thuc_the/*', k)
        k = re.sub(r'/m_don_vi/[^/]+', '/m_don_vi/*', k)
        dem[k] += 1
        vi_du.setdefault(k, (ca, a, b))
        ca_lech.add(ca)


for ca in sorted(cu):
    for r in (cu[ca], moi[ca]):  # kenh_co sắp theo mã kênh, mã đổi ở lượt 3: so theo nội dung (bỏ mã)
        ex = r.get('extra') or {}
        if ex.get('kenh_co'):
            ex['kenh_co'] = sorted(({k: v for k, v in x.items() if k != 'ma'} for x in ex['kenh_co']),
                                   key=lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False))
    di(cu[ca], moi[ca], '', ca)
print(json.dumps({'so_ban_ghi': len(cu), 'duong_dan_lech': [{'duong_dan': k, 'so_lan': n, 'vi_du': vi_du.get(k)}
                                                             for k, n in dem.most_common()],
                  'ban_ghi_co_lech': sorted(ca_lech)},
                 ensure_ascii=False, indent=1))
