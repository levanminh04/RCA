"""T-046 bản 4, C2 / A3 điểm 6: tinh p của G3 cho V1. Với cửa sổ A/A R0 và cửa sổ thật R0, các phép G3 (đơn vị hợp lệ,
thực thể thuộc U) có 0 lần vượt trong 2.000 hoán vị ngẫu nhiên đầu được tính lại với B = ⌈m/α⌉ hoán vị cùng dãy seed
(m: cỡ họ phép kiểm của V1 ở cửa sổ đó với (G3, D1)). Kiểm trước: p với B = 2.000 tính lại phải bằng 1/2.001.
Sau phản biện R1: khối theo biên phía (t046.bien_don_vi); `--cu` phải là lượt chạy với biên mới.
Không đọc nhãn. Ghi `<lượt>/ca/<mã>.json`, `progress.jsonl`.

Chạy: $PY -B results/T-046/scripts/b5r_tinh_G3.py --cu results/T-046/runs/b3-aa-001 --moi results/T-046/runs/b3b-aa-001
      --luot results/T-046/runs/<tên> [--so 4]
"""
import argparse
import json
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import cong
import t046
from b3_chay import tat_ha_toc

ALPHA = 0.01
CUA_SO = ('aa|R0', 'that|R0')


def viec_can(ca):
    out = {}
    for oid, x in ca.items():
        for k in CUA_SO:
            b = x['cua_so'][k]['bang']
            phep, _ = t046.co_theo_cong(b, 'G3', 'D1')
            B = math.ceil(len(phep) / ALPHA)
            ds = []
            for u in b['pv']:
                if not (u['hop_le'] and u['trong_U']):
                    continue
                for d, h in u['huong'].items():
                    g = h.get('G3')
                    if h['cach_G3'] == 'G3' and g and g['cach'] == 'ngau_nhien' and g['dem_vuot'] == 0:
                        ds.append((u['ma'], d))
            if ds:
                out.setdefault(oid, {'dataset': x['dataset'], 'cua_so': {}})['cua_so'][k] = {'B': B, 'phep': ds}
    return out


def mot_ca(oid, viec, ra):
    tat_ha_toc()
    mt = t046.moi_truong()
    out = {'opaque_id': oid, 'p_tinh': {}, 'B': {}, 'kiem_2000': 0, 'pid': os.getpid()}
    t0 = time.perf_counter()
    for k, v in viec['cua_so'].items():
        kieu = k.split('|')[0]
        ca, t, meta = t046.nap(viec['dataset'], oid, kieu, mt)
        rec, cap, p = t046.chay_chuoi(ca, t, t046.cau_hinh('R0'), t046.CacheMoc())
        t_ns = int(round(t * t046.NS))
        he_s = t046.chuoi._he_so_ns(p['don_vi_thoi_gian']['spans.start_us'])
        mm = t046._moc_metric(ca, p, t_ns)
        mau = {}
        for (chu, op), m in cap['op'].items():
            mau[f'op|{chu}|{op}'] = (m['N'], [int(x * he_s) for x in m['moc_N']], m['A'], [int(x * he_s) for x in m['moc_A']])
        for ma, x in mm.items():
            mau[ma] = x[:4]
        ts = p['tham_so_E4']
        ra_ds = []
        for ma, d in v['phep']:
            N, mN, A, mA = mau[ma]
            N, A = [float(x) for x in N], [float(x) for x in A]
            bN, bA = t046.bien_don_vi(rec, p, ma, t_ns)  # sửa R1: biên phía theo H (SPEC A3 điểm 3)
            kb = cong.chuan_bi_khoi(N, mN, A, mA, t_ns, bN, bA)
            p2000 = cong.p_G3(kb, d, ts, ma)[0]
            if p2000 != 1 / 2001:
                raise RuntimeError(f'p G3 với B = 2.000 không tái lập: {oid} {k} {ma} {d} {p2000}')
            out['kiem_2000'] += 1
            ra_ds.append([ma, d, cong.p_G3(kb, d, ts, ma, B=v['B'])[0]])
        out['p_tinh'][k] = ra_ds
        out['B'][k] = v['B']
    out['giay'] = round(time.perf_counter() - t0, 1)
    (ra / 'ca' / f'{oid}.json').write_bytes((json.dumps(out, ensure_ascii=False, sort_keys=True) + '\n').encode('utf-8'))
    return oid, out['giay'], out['kiem_2000']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cu', required=True)
    ap.add_argument('--moi', required=True)
    ap.add_argument('--luot', required=True)
    ap.add_argument('--so', type=int, default=4)
    a = ap.parse_args()
    ra = Path(a.luot)
    (ra / 'ca').mkdir(parents=True, exist_ok=True)
    ca, _ = t046.nap_ghep(a.cu, a.moi)
    viec = viec_can(ca)
    lam = [o for o in sorted(viec) if not (ra / 'ca' / f'{o}.json').exists()]
    with open(ra / 'tham-so.json', 'ab') as f:
        f.write((json.dumps({'so_ca': len(viec), 'so_phep': sum(len(w['phep']) for v in viec.values()
                                                                  for w in v['cua_so'].values()),
                             'can_chay': len(lam), 'bat_dau': time.strftime('%Y-%m-%dT%H:%M:%S%z')},
                            ensure_ascii=False) + '\n').encode('utf-8'))
    t0 = time.time()
    with open(ra / 'progress.jsonl', 'ab') as pf, ProcessPoolExecutor(max_workers=a.so) as ex:
        fut = {ex.submit(mot_ca, o, viec[o], ra): o for o in lam}
        for i, f in enumerate(as_completed(fut), 1):
            o = fut[f]
            try:
                oid, giay, k = f.result()
                rec = {'su_kien': 'xong', 'ca': oid, 'giay': giay, 'kiem_2000': k, 'thu_tu': i,
                       'giay_tu_dau': round(time.time() - t0, 1), 'luc': time.strftime('%H:%M:%S')}
            except Exception as ex_:
                rec = {'su_kien': 'loi', 'ca': o, 'loi': f'{type(ex_).__name__}: {ex_}', 'luc': time.strftime('%H:%M:%S')}
            pf.write((json.dumps(rec, ensure_ascii=False) + '\n').encode('utf-8'))
            pf.flush()
            print(json.dumps(rec, ensure_ascii=False)[:200], flush=True)
    print('xong', round(time.time() - t0, 1))


if __name__ == '__main__':
    main()
