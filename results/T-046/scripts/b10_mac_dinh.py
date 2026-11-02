"""T-046 bước 10, tiêu chí xong 5: chế độ mặc định của src sau khi cài không đổi hành vi. Chạy chuỗi không có
params.che_do ở A/A R0, A/A K-đủ, thật R0 của 52 ca dev; so sha256 bản ghi với lượt b3-sua2 (chạy trên src bbef69dd).
Không đọc nhãn.

Chạy: PYTHONHASHSEED=0 $PY -B results/T-046/scripts/b10_mac_dinh.py --ra results/T-046/kiem-src-mac-dinh.json [--so 4]
"""
import argparse
import hashlib
import json
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import t046
from t046 import ROOT
from b3_chay import tat_ha_toc
from m1 import chuoi, e4, runner

B3 = ROOT / 'results/T-046/runs/b3-sua2-aa-001/ca'
CUA_SO = (('aa', 'R0'), ('aa', 'K-du'), ('that', 'R0'))


def mot_ca(ds, oid):
    tat_ha_toc()
    chuoi.CACHE = e4.CacheCong()
    mt = t046.moi_truong()
    do = json.loads((B3 / f'{oid}.json').read_text(encoding='utf-8'))
    out = {}
    for kieu, ten in CUA_SO:
        ca, t, _ = t046.nap(ds, oid, kieu, mt)
        p = runner._params(t046.cau_hinh(ten), ca)
        rec = chuoi.chay(ca['spans'], ca.get('metrics') or [], ca.get('logs') or [], ca.get('inventory') or [],
                         ca.get('aliases') or {}, t, p)
        h = hashlib.sha256(t046.json_ban_ghi(rec, oid).encode('utf-8')).hexdigest()
        out[f'{kieu}|{ten}'] = h == do['cua_so'][f'{kieu}|{ten}']['sha256_ban_ghi']
    return oid, ds, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ra', required=True)
    ap.add_argument('--so', type=int, default=4)
    a = ap.parse_args()
    ds_ca = t046.danh_sach_ca(t046.moi_truong())
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=a.so) as ex:
        kq = list(ex.map(mot_ca, [c[0] for c in ds_ca], [c[1] for c in ds_ca]))
    tong = {}
    for _, ds, o in kq:
        for k, v in o.items():
            x = tong.setdefault(f'{ds}|{k}', {'trung': 0, 'lech': 0})
            x['trung' if v else 'lech'] += 1
    out = {'so_ca': len(kq), 'theo_cua_so': tong, 'giay': round(time.time() - t0, 1)}
    Path(a.ra).write_bytes((json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + '\n').encode('utf-8'))
    print(json.dumps(out, ensure_ascii=False))


if __name__ == '__main__':
    main()
