# -*- coding: utf-8 -*-
"""Phiên C — H8-adapter bước 2: đếm, KHÔNG ném lỗi, các metric logic (kênh, thực thể) có > 1 định danh chuỗi runtime
trong gói metric của ca — đúng điều kiện làm `m1.adapter_flashticket.normalize_metrics` ném
'Multiple runtime series map to one logical metric without a declared aggregation'. Chỉ đọc metadata/metric của gói
(không nhãn, không sổ tiêm). Chạy trên exp-obs bằng user rca:
  python -B dem_chuoi_trung.py <src của goc-n> <thư mục cases> <thư mục gói bổ sung 1> [...]
In JSON: theo gói → danh sách {kenh, thuc_the, so_dinh_danh, nhan_khac, khoang_thoi_gian_moi_chuoi, chong_lan}."""
import json, os, sys
from collections import defaultdict
sys.path.insert(0, sys.argv[1])
from m1 import adapter_flashticket as ad

KENH_BO_SUNG = {'live-down', 'live-ms', 'queue-ready', 'queue-unacked', 'throttle', 'throttle-ratio', 'gc', 'heap',
                'threads-blocked', 'jvm-cpu', 'pool-pending', 'pool-used', 'pool-wait', 'queue-consumers', 'queue-publish',
                'queue-ack', 'restarts', 'samples', 'route-rate', 'route-5xx', 'pg-backends', 'pg-ops', 'redis-cmd',
                'redis-clients'}


def quet(bundles, inventory):
    prefixes = {e: e.replace('_', '-') for e in inventory}
    nhom = defaultdict(list)
    for b in bundles:
        for it in b['result']:
            owner = ad._owner(it['metric'], inventory)
            if owner is None:
                continue
            nhom[(b['channel'], owner)].append(it)
    out = []
    for (ch, owner), its in sorted(nhom.items()):
        ids = {ad._labels_key(x['metric']) for x in its}
        if len(ids) <= 1:
            continue
        nhan = [dict(k) for k in sorted(ids)]
        chung = set.intersection(*[set(d.items()) for d in nhan])
        khac = [{k: v for k, v in d.items() if (k, v) not in chung} for d in nhan]
        kh = [[min(float(t) for t, _ in x['values']), max(float(t) for t, _ in x['values']), len(x['values'])] for x in its]
        kh_s = sorted(kh)
        chong = any(kh_s[i + 1][0] <= kh_s[i][1] for i in range(len(kh_s) - 1))
        out.append({'kenh': ch, 'thuc_the': owner, 'so_dinh_danh': len(ids), 'so_chuoi': len(its), 'nhan_khac': khac,
                    'khoang': kh, 'chong_lan': chong})
    return out


kq = {}
cases = sys.argv[2]
for i in sorted(os.listdir(cases)):
    c = os.path.join(cases, i)
    try:
        inv = json.load(open(c + '/inventory.json')); b = json.load(open(c + '/prometheus.json'))
        t = json.load(open(c + '/request.json'))['t']
    except Exception as e:
        kq['ghim:' + i] = {'loi_doc': repr(e)[:120]}; continue
    r = quet(b, inv)
    for x in r:
        x['khoang'] = [[round(a - t), round(z - t), n] for a, z, n in x['khoang']]
    try:
        ad.normalize_metrics(b, inv); nem = None
    except ValueError as e:
        nem = str(e)
    kq['ghim:' + i] = {'trung': r, 'adapter_nem': nem}
    for bs_dir in sys.argv[3:]:
        p = os.path.join(bs_dir, i, 'prometheus-bo-sung.json')
        if not os.path.exists(p):
            continue
        g = json.load(open(p))
        r2 = quet(g['bundles'], inv)
        for x in r2:
            x['khoang'] = [[round(a - t), round(z - t), n] for a, z, n in x['khoang']]
        kq['bo_sung:' + os.path.basename(bs_dir.rstrip('/')) + ':' + i] = {'trung': r2}
tom = {k: len(v.get('trung', [])) for k, v in kq.items()}
print(json.dumps({'tom_tat_so_metric_trung': tom, 'chi_tiet': {k: v for k, v in kq.items() if v.get('trung') or v.get('adapter_nem') or v.get('loi_doc')}}, ensure_ascii=False, indent=1))
