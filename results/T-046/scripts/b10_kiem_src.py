"""T-046 bước 10: kiểm hành vi bằng code đã cài trong src (SPEC bước 10; Q-228). Không đọc nhãn, không tính MRR.

Chạy chuỗi `src/m1` không móc, với params.che_do = (G3, D1, E4+T4c), ở cửa sổ A/A, thật và C-e (RE2-TT), cấu hình R0 và
K-đủ, rồi so với số đã đo bằng scripts (lượt b3 và lượt sau khóa, hậu tố -sua2):
- p của từng phép: A/A R0, A/A K-đủ, thật R0 so với bảng b3, từng số;
- số đơn vị có cờ, số đơn vị hợp lệ, qua cổng theo ô, verdict V0: so với lượt sau khóa;
- thật R0: tầng 1, khối đầu và số khối theo T4c, bão hòa;
- blocks của bản ghi trùng `extra.T4c.blocks`;
- QT5 theo ca bằng `results/T-045/scripts/soi_ban_ghi.py`.
Bản ghi không so từng byte với lượt đo: lượt đo chỉ thay cờ ở kênh, còn src mang cờ D1 trong mọi trường của đơn vị đếm.

Chạy: PYTHONHASHSEED=0 $PY -B results/T-046/scripts/b10_kiem_src.py --luot results/T-046/runs/<tên> [--so 4] [--ca a,b]
      PYTHONHASHSEED=<s> $PY -B results/T-046/scripts/b10_kiem_src.py --luot <lượt> --bat-bien <tên> [--xao 0]
      $PY -B results/T-046/scripts/b10_kiem_src.py --luot <lượt> --tong-hop results/T-046/kiem-src.json
"""
import argparse
import hashlib
import json
import os
import random
import statistics
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import t046
from t046 import ROOT
from b3_chay import tat_ha_toc
from m1 import chuoi, e4, runner

sys.path.insert(0, str(ROOT / 'results/T-045/scripts'))
import soi_ban_ghi  # noqa: E402

BAT = {'cong_phan_vi': 'G3', 'cong_dem': 'D1', 'thang': 'E4+T4c'}
B3 = ROOT / 'results/T-046/runs/b3-sua2-aa-001/ca'
B6 = ROOT / 'results/T-046/runs/b6-sau-khoa-sua2-001'
ALPHA = 0.01
BAT_BIEN_CA = (('RE2-TT', 2), ('Nezha-OB', 2))


def chay(ca, t, ten):
    p = runner._params(dict(t046.cau_hinh(ten), che_do=BAT), ca)
    return chuoi.chay(ca['spans'], ca.get('metrics') or [], ca.get('logs') or [], ca.get('inventory') or [],
                      ca.get('aliases') or {}, t, p)


def _nhom_log(rec):
    lop = {f"log|{x['thuc_the']}|mau:{x['mau']}": x['lop'] for x in (rec['extra']['thong_ke_log'].get('cap_drain') or [])}
    return {k: {'loi': 'mau_loi', 'thuong': 'mau_thuong'}.get(v) for k, v in lop.items()}


def tom_tat(rec, ca, ten):
    """Các đại lượng đối chiếu, tính từ bản ghi của src, cùng định nghĩa với t046 và b6_sau_khoa."""
    aliases = ca.get('aliases') or {}
    U = set(chuoi._alias(aliases, x) for x in (ca.get('inventory') or []))
    nhom_op = 'op_full' if rec and t046.cau_hinh(ten)['bat_tat']['E1'] == 'tat' else 'op_excl'
    nlog = _nhom_log(rec)
    o, co, hop, bao, tt = {}, set(), set(), {}, {}
    p_pv, p_dem = {}, {}
    for u in rec['extra']['don_vi_phan_vi']:
        ma = u['ma']
        if ma.startswith('metric|'):
            e, nhom = chuoi._ten_metric(ma.split('|', 1)[1], aliases)[0], 'metric'
        elif ma.startswith('op|'):
            e, nhom = ma.split('|')[1], nhom_op
        else:
            e, nhom = ma.split('|')[2], 'canh'
        for d in ('len', 'xuong'):
            if u[f'p_{d}'] is not None:
                p_pv[f'{ma}|{d}'] = u[f'p_{d}']
        if not (u['hop_le'] and e in U):
            continue
        hop.add(ma)
        for d in ('len', 'xuong'):
            if u[f'p_{d}'] is None:
                continue
            x = o.setdefault(f'{nhom}|{d}', {'n': 0, 'qua': 0})
            x['n'] += 1
            x['qua'] += int(u[f'p_{d}'] < ALPHA)
            if u[f'F_raw_{d}']:
                co.add(ma)
                b = bao.setdefault(nhom, {'co': 0, 'rA_1': 0})
                b['co'] += 1
                b['rA_1'] += int(u[f'r_{d}_A'] == 1.0)
    for x in rec['worlds']['P']['don_vi_dem']:
        ma = x['ma']
        if not ma.startswith('log|'):
            continue
        for d in ('len', 'xuong'):
            if x.get(f'p_{d}') is not None:
                p_dem[f'{ma}|{d}'] = x[f'p_{d}']
        e = ma.split('|')[1]
        if x['trang_thai'] != 'OK' or e not in U:
            continue
        hop.add(ma)
        if x['F_raw_len'] or x['F_raw_xuong']:
            co.add(ma)
        if x['loai_thay_doi'] in ('NEW_OP', 'STOPPED'):
            tt[x['loai_thay_doi']] = tt.get(x['loai_thay_doi'], 0) + 1
            continue
        ten_dv = ma.split('|', 2)[2]
        if ten_dv == 'mau_moi':
            continue
        nhom = 'log_loi' if ten_dv == 'log_loi' else nlog.get(ma)
        if nhom is None:
            continue
        d = 'xuong' if nhom == 'mau_thuong' else 'len'
        v = o.setdefault(f'{nhom}|{d}', {'n': 0, 'qua': 0})
        v['n'] += 1
        v['qua'] += int(x[f'p_{d}'] < ALPHA)
    khoi = rec['blocks'] or []
    tang = rec['extra']['tang_P']
    return {'verdict': rec['verdict'], 'status': rec['status'], 'don_vi_co': len(co), 'don_vi_hop_le': len(hop),
            'ty_le': len(co) / max(len(hop), 1), 'phep_theo_o': dict(sorted(o.items())), 'bao_hoa': bao, 'truc_tiep': tt,
            'tang1': sum(1 for v in tang.values() if v == 1), 'khoi_dau': len(khoi[0]['groups'][0]) if khoi else 0,
            'so_khoi': len(khoi), 'blocks_trung_T4c': khoi == (rec['extra']['T4c'] or {}).get('blocks'),
            'so_cham_hop_le': rec['diagnostics']['so_cham_hop_le']}, p_pv, p_dem


def so_b3(do, k, p_pv, p_dem):
    """Số phép lệch so với bảng b3 (cổng G3, D1), từng số."""
    bang = do['cua_so'][k]['bang']
    so, lech, vd = 0, 0, []
    for u in bang['pv']:
        for d, h in u['huong'].items():
            so += 1
            if p_pv.get(f"{u['ma']}|{d}") != h['p_G3']:
                lech += 1
                vd.append([u['ma'], d, p_pv.get(f"{u['ma']}|{d}"), h['p_G3']])
    so_d, lech_d = 0, 0
    for u in bang['dem']:
        if 'p_D1_len' not in u:
            continue
        for d in ('len', 'xuong'):
            so_d += 1
            if p_dem.get(f"{u['ma']}|{d}") != u[f'p_D1_{d}']:
                lech_d += 1
                vd.append([u['ma'], d, p_dem.get(f"{u['ma']}|{d}"), u[f'p_D1_{d}']])
    return {'phan_vi': so, 'lech_phan_vi': lech, 'dem': so_d, 'lech_dem': lech_d, 'vi_du': vd[:5]}


def so_b6(tt, goc):
    """So với phần tương ứng của lượt sau khóa. goc: {khóa: giá trị mong}."""
    return {k: {'src': tt[k], 'do': v} for k, v in goc.items() if tt[k] != v}


def mot_ca(ds, oid, ra):
    tat_ha_toc()
    chuoi.CACHE = e4.CacheCong()
    mt = t046.moi_truong()
    do = json.loads((B3 / f'{oid}.json').read_text(encoding='utf-8'))
    r0 = json.loads((B6 / 'r0' / f'{oid}.json').read_text(encoding='utf-8'))
    kdu = json.loads((B6 / 'kdu' / f'{oid}.json').read_text(encoding='utf-8'))
    ce6 = json.loads((B6 / 'ce' / f'{oid}.json').read_text(encoding='utf-8')) if ds == 'RE2-TT' else None
    out = {'dataset': ds, 'opaque_id': oid, 'cua_so': {}, 'pid': os.getpid()}
    t0 = time.perf_counter()
    for kieu in ('aa', 'that') + (('ce',) if ds == 'RE2-TT' else ()):
        ca, t, _ = t046.nap(ds, oid, kieu, mt)
        for ten in ('R0', 'K-du'):
            t1 = time.perf_counter()
            rec = chay(ca, t, ten)
            tt, p_pv, p_dem = tom_tat(rec, ca, ten)
            r = {'tom_tat': tt, 'giay': round(time.perf_counter() - t1, 1), 'lech_b6': {},
                 'QT5': {a: v for a, v in soi_ban_ghi.soi(dict(rec, opaque_id=oid), False).items()
                         if not isinstance(v, (dict, list))}}
            k = f'{kieu}|{ten}'
            if k in do['cua_so']:
                r['so_b3'] = so_b3(do, k, p_pv, p_dem)
            if ten == 'K-du':
                x = kdu[kieu]
                r['lech_b6'] = so_b6(tt, {'verdict': x['verdict_chuoi'], 'ty_le': x['ty_le_don_vi_co'],
                                          'so_cham_hop_le': x['so_cham_hop_le']})
                for a, b in x['phep_theo_o'].items():
                    if tt['phep_theo_o'].get(a) != b:
                        r['lech_b6'][f'o|{a}'] = {'src': tt['phep_theo_o'].get(a), 'do': b}
            elif kieu == 'that':
                r['lech_b6'] = so_b6(tt, {'verdict': r0['verdict_chuoi'], 'tang1': r0['tang1'], 'ty_le': r0['ty_le_don_vi_co'],
                                          'khoi_dau': r0['so_thuc_the_khoi_dau_T4c'], 'so_khoi': r0['so_khoi_T4c'],
                                          'bao_hoa': r0['bao_hoa']})
            elif kieu == 'ce':
                r['lech_b6'] = so_b6(tt, {'verdict': ce6['verdict_chuoi_bo_khoa'], 'ty_le': ce6['ty_le_don_vi_co'],
                                          'don_vi_co': ce6['so_co']['khoa']['don_vi_co']})
                for a, b in ce6['phep_theo_o'].items():
                    if tt['phep_theo_o'].get(a) != b:
                        r['lech_b6'][f'o|{a}'] = {'src': tt['phep_theo_o'].get(a), 'do': b}
            out['cua_so'][k] = r
    out['giay'] = round(time.perf_counter() - t0, 1)
    out['cache'] = {'trung': chuoi.CACHE.trung, 'moi': chuoi.CACHE.moi}
    (ra / 'ca').mkdir(parents=True, exist_ok=True)
    (ra / 'ca' / f'{oid}.json').write_bytes((json.dumps(out, ensure_ascii=False, sort_keys=True) + '\n').encode('utf-8'))
    return oid, out['giay']


def xao(ca, seed):
    """Như results/T-045/scripts/chay_pha1.py."""
    rng = random.Random(seed)
    rng.shuffle(ca['spans'])
    rng.shuffle(ca['logs'])
    n = len(ca['metrics'])
    hv = list(range(n))
    rng.shuffle(hv)
    ca['metrics'] = [ca['metrics'][i] for i in hv]
    tg = ca['params_ca'].get('thoi_gian_nguon') or {}
    for k, v in list(tg.items()):
        if isinstance(v, list):
            if len(v) != n:
                raise ValueError(f'mốc nguồn {k}: {len(v)} mốc cho {n} hàng')
            tg[k] = [v[i] for i in hv]
    return ca


def bat_bien(ra, ten, so_xao):
    mt = t046.moi_truong()
    ds_ca = t046.danh_sach_ca(mt)
    chon = [x for ds, n in BAT_BIEN_CA for x in [c for c in ds_ca if c[0] == ds][:n]]
    out = {'PYTHONHASHSEED': os.environ.get('PYTHONHASHSEED'), 'xao': so_xao, 'ca': {}}
    for ds, oid in chon:
        for kieu in ('that',):
            ca, t, _ = t046.nap(ds, oid, kieu, mt)
            if so_xao is not None:
                ca = xao(ca, so_xao)
            for c in ('R0', 'K-du'):
                chuoi.CACHE = e4.CacheCong()
                rec = chay(ca, t, c)
                out['ca'][f'{oid}|{kieu}|{c}'] = hashlib.sha256(t046.json_ban_ghi(rec, oid).encode('utf-8')).hexdigest()
    (ra / 'bat-bien').mkdir(parents=True, exist_ok=True)
    (ra / 'bat-bien' / f'{ten}.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(ten, out['ca'])


def tong_hop(ra, tep):
    ca = [json.loads(f.read_text(encoding='utf-8')) for f in sorted((ra / 'ca').glob('*.json'))]
    k = {'so_ca': len(ca), 'so_b3': {'phan_vi': 0, 'lech_phan_vi': 0, 'dem': 0, 'lech_dem': 0}, 'lech_b6': [], 'vi_du_b3': [],
         'blocks_khong_trung_T4c': 0, 'status': {}, 'gop_o': {}, 'ty_le': {}, 'verdict': {}, 'QT5': {}}
    for x in ca:
        for w, r in x['cua_so'].items():
            tt = r['tom_tat']
            k['status'][tt['status']] = k['status'].get(tt['status'], 0) + 1
            k['blocks_khong_trung_T4c'] += int(not tt['blocks_trung_T4c'])
            if 'so_b3' in r:
                for a in k['so_b3']:
                    k['so_b3'][a] += r['so_b3'][a]
                k['vi_du_b3'] += [[x['opaque_id'], w] + v for v in r['so_b3']['vi_du']][:2]
            if r['lech_b6']:
                k['lech_b6'].append({'ca': x['opaque_id'], 'cua_so': w, 'lech': r['lech_b6']})
            n = f"{x['dataset']}|{w}"
            k['ty_le'].setdefault(n, []).append(tt['ty_le'])
            v = k['verdict'].setdefault(n, {})
            v[tt['verdict']] = v.get(tt['verdict'], 0) + 1
            o = k['gop_o'].setdefault(n, {})
            for a, b in tt['phep_theo_o'].items():
                t = o.setdefault(a, {'n': 0, 'qua': 0})
                t['n'] += b['n']
                t['qua'] += b['qua']
            q = k['QT5'].setdefault(n, {})
            for a, b in r['QT5'].items():
                if isinstance(b, bool):
                    q[a] = q.get(a, 0) + int(b)
                elif isinstance(b, (int, float)) and a.startswith(('so_diem', 'diem', 'nguong')):
                    q[a] = max(q.get(a, b), b)
    k['ty_le'] = {a: round(statistics.median(b), 6) for a, b in k['ty_le'].items()}
    bb = {}
    d = ra / 'bat-bien'
    if d.exists():
        lg = {f.stem: json.loads(f.read_text(encoding='utf-8'))['ca'] for f in sorted(d.glob('*.json'))}
        bb = {'luot': sorted(lg), 'trung_het': len({json.dumps(v, sort_keys=True) for v in lg.values()}) == 1,
              'so_ban_ghi': len(next(iter(lg.values()))) if lg else 0}
    k['bat_bien'] = bb
    k['giay_trung_vi_ca'] = statistics.median(x['giay'] for x in ca)
    Path(tep).write_bytes((json.dumps(k, ensure_ascii=False, indent=1, sort_keys=True) + '\n').encode('utf-8'))
    print(json.dumps({a: k[a] for a in ('so_ca', 'so_b3', 'status', 'blocks_khong_trung_T4c', 'bat_bien')}, ensure_ascii=False))
    print('so cua so lech b6', len(k['lech_b6']))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--luot', required=True)
    ap.add_argument('--so', type=int, default=4)
    ap.add_argument('--ca', default=None)
    ap.add_argument('--bat-bien', default=None)
    ap.add_argument('--xao', type=int, default=None)
    ap.add_argument('--tong-hop', default=None)
    a = ap.parse_args()
    ra = Path(a.luot)
    ra.mkdir(parents=True, exist_ok=True)
    if a.tong_hop:
        tong_hop(ra, a.tong_hop)
        return
    if a.bat_bien:
        bat_bien(ra, a.bat_bien, a.xao)
        return
    mt = t046.moi_truong()
    ds_ca = t046.danh_sach_ca(mt)
    if a.ca:
        chon = set(a.ca.split(','))
        ds_ca = [c for c in ds_ca if c[1] in chon]
    lam = [c for c in ds_ca if not (ra / 'ca' / f'{c[1]}.json').exists()]
    with open(ra / 'tham-so.json', 'ab') as f:
        f.write((json.dumps({'argv': sys.argv[1:], 'che_do': BAT, 'PYTHONHASHSEED': os.environ.get('PYTHONHASHSEED'),
                             'can_chay': len(lam), 'phien_ban': chuoi.PHIEN_BAN_CHE_DO,
                             'bat_dau': time.strftime('%Y-%m-%dT%H:%M:%S%z')}, ensure_ascii=False) + '\n').encode('utf-8'))
    t0 = time.time()
    with open(ra / 'progress.jsonl', 'ab') as pf, ProcessPoolExecutor(max_workers=a.so) as ex:
        fut = {ex.submit(mot_ca, ds, o, ra): (ds, o) for ds, o in lam}
        for i, f in enumerate(as_completed(fut), 1):
            ds, o = fut[f]
            try:
                _, giay = f.result()
                rec = {'su_kien': 'xong', 'ca': o, 'dataset': ds, 'giay': giay, 'thu_tu': i,
                       'giay_tu_dau': round(time.time() - t0, 1), 'luc': time.strftime('%H:%M:%S')}
            except Exception as ex_:
                rec = {'su_kien': 'loi', 'ca': o, 'loi': f'{type(ex_).__name__}: {ex_}', 'luc': time.strftime('%H:%M:%S')}
            pf.write((json.dumps(rec, ensure_ascii=False) + '\n').encode('utf-8'))
            pf.flush()
            print(json.dumps(rec, ensure_ascii=False)[:240], flush=True)
    print('xong', round(time.time() - t0, 1))


if __name__ == '__main__':
    main()
