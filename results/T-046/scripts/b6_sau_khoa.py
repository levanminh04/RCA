"""T-046 bước 6–7: phép sau khóa (SPEC T-046 bước 6, 7; A5; S9; bản 3 B6). Chỉ chạy sau khi bộ cổng × verdict đã
khóa và hash `ung-vien.json` đã ghi LOG. Không đọc nhãn, không tính MRR.

Bộ khóa đọc từ `ung-vien.json#/luat_chon/to_hop_chon` dạng 'g|c|v' (bản 3); ngưỡng GE/DE từ `#/nguong`.
Phần (theo ca, song song):
- 'ce': C-e RE2-TT (t − 300), R0. Bản ghi G0 phải trùng bản ghi mốc giả T1-R0 của T-045. Bảng phép kiểm theo G0 và
  cổng khóa; verdict theo bộ khóa ((b′)) và theo (G0, D0, V0) để đối chiếu; số đơn vị có cờ theo bộ khóa ((c2));
  phép theo ô cho (a′) khi bộ khóa có GE hoặc DE.
- 'kdu': K-đủ ở cửa sổ A/A và cửa sổ thật, chạy lại chuỗi với bộ khóa (p phân vị phát lại, cờ đếm thay theo D1/DE)
  để có F_I sau E5; verdict V0 (chuỗi), V1, V3; bão hòa trên đơn vị của K-đủ (chỉ báo cáo).
- 'r0': R0 cửa sổ thật với bộ khóa: khóa tầng 1 (K_I) để đếm thực thể hòa ở phần tử đầu (C3).
Ghi `<lượt>/<phần>/<mã>.json`; `progress.jsonl`.

Chạy: $PY -B results/T-046/scripts/b6_sau_khoa.py --ung-vien results/T-046/ung-vien.json --sha256 <hash ở LOG>
      --phan ce|kdu|r0 --luot results/T-046/runs/<tên> [--so 4]
"""
import argparse
import hashlib
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import t046
from t046 import ROOT
from b3_chay import tat_ha_toc

T045_CE = ROOT / 'results/T-045/runs/b2-t1-re2-mocgia-001/ban-ghi.jsonl'
ALPHA = 0.01


def _dong(path, oid, cfg):
    with open(path, encoding='utf-8') as f:
        for x in f:
            if f'"opaque_id":"{oid}"' in x and f'"config_id":"{cfg}"' in x:
                return x.rstrip('\n')
    return None


def nguong_ds(uv, ds):
    out = {}
    for loai in ('GE', 'DE'):
        for k, r in uv['nguong'][loai].items():
            d_, nhom, h = k.split('|')
            if d_ == ds:
                out[(nhom, h)] = r['nguong']
    return out


def _so_co(bang, g, c, ng):
    phep, tt = t046.co_theo_cong(bang, g, c, ng)
    return {'don_vi_co': len({x['ma'] for x in phep if x['F']} | {x['ma'] for x in tt if x['F']}),
            'phep_co': sum(x['F'] for x in phep), 'truc_tiep': sum(x['F'] for x in tt)}


def _bao_hoa(bang, g, ng, F_I=None):
    """Kênh phân vị có cờ theo g (và F_I nếu có): số đạt rA = 1 theo hướng, theo nhóm."""
    out = {}
    for u in bang['pv']:
        if not (u['hop_le'] and u['trong_U']):
            continue
        for d, h in u['huong'].items():
            p = h['p_G4'] if g == 'GE' else h[f'p_{g}']
            a = ng.get((u['nhom'], d), ALPHA) if g == 'GE' else ALPHA
            if not (p < a and h['chenh_duong']):
                continue
            if F_I is not None and not F_I.get((u['ma'], d)):
                continue
            o = out.setdefault(u['nhom'], {'co': 0, 'rA_1': 0})
            o['co'] += 1
            o['rA_1'] += int(h['rA'] == 1.0)
    return out


def _thu_hang(blocks):
    """{thực thể: chỉ số khối} từ danh sách khối (hòa cùng khối)."""
    return {e: i for i, b in enumerate(blocks or []) for grp in b['groups'] for e in grp}


def _doi_hang(b_e4, b_t4c, tang):
    """R4 (sau phản biện, 17:57): thay đổi thứ hạng không nhãn giữa khóa E4 và khóa T4c, trên thực thể tầng 1."""
    r1, r2 = _thu_hang(b_e4), _thu_hang(b_t4c)
    t1 = sorted(e for e, tg in tang.items() if tg == 1 and e in r1 and e in r2)
    cap = dao = 0
    for i in range(len(t1)):
        for j in range(i + 1, len(t1)):
            a, b = t1[i], t1[j]
            s1 = (r1[a] > r1[b]) - (r1[a] < r1[b])
            s2 = (r2[a] > r2[b]) - (r2[a] < r2[b])
            cap += 1
            dao += int(s1 != s2)
    dau1 = sorted(b_e4[0]['groups'][0]) if b_e4 else []
    dau2 = sorted(b_t4c[0]['groups'][0]) if b_t4c else []
    return {'so_cap_tang1': cap, 'cap_doi_quan_he': dao, 'doi_khoi_dau': dau1 != dau2,
            'doi_thuc_the_dau_duy_nhat': (len(dau1) == 1 and len(dau2) == 1 and dau1 != dau2)}


def _phep_theo_hau_to(bang, g):
    """M3: theo loại kênh metric (hậu tố) và hướng, số phép và số qua cổng theo g."""
    out = {}
    for u in bang['pv']:
        if not (u['hop_le'] and u['trong_U']) or u['nhom'] != 'metric':
            continue
        hau_to = u['ma'].split('|', 1)[1].split('_', 1)[1]
        for d, h in u['huong'].items():
            o = out.setdefault(f'{hau_to}|{d}', {'n': 0, 'qua': 0})
            o['n'] += 1
            o['qua'] += int(h[f'p_{g}'] < ALPHA)
    return out


def _phep_theo_o(bang, g, c, ng):
    """(a′): theo ô (nhóm, hướng), số phép và số qua cổng theo bộ khóa (phân vị: p < α_ô với GE; đếm: p_D1 < α_ô với DE)."""
    out = {}
    for u in bang['pv']:
        if not (u['hop_le'] and u['trong_U']):
            continue
        for d, h in u['huong'].items():
            p = h['p_G4'] if g == 'GE' else h[f'p_{g}']
            a = ng.get((u['nhom'], d), ALPHA) if g == 'GE' else ALPHA
            o = out.setdefault(f"{u['nhom']}|{d}", {'n': 0, 'qua': 0})
            o['n'] += 1
            o['qua'] += int(p < a)
    for u in bang['dem']:
        if not (u['hop_le'] and u['trong_U']) or u['nhan'] in ('NEW_OP', 'STOPPED') or 'p_D1_len' not in u:
            continue
        for d in u['huong_cham']:
            if c == 'D0':
                p, a = u[f'p_{d}'], ALPHA
            else:
                p = u[f'p_D1_{d}']
                a = ng.get((u['nhom'], d), ALPHA) if c == 'DE' else ALPHA
            o = out.setdefault(f"{u['nhom']}|{d}", {'n': 0, 'qua': 0})
            o['n'] += 1
            o['qua'] += int(p < a)
    return out


def lam(phan, ds, oid, bo, uv_nguong, ra, v_bao_cao=()):
    tat_ha_toc()
    g, c, v = bo
    mt = t046.moi_truong()
    ng = nguong_ds({'nguong': uv_nguong}, ds)
    out = {'dataset': ds, 'opaque_id': oid, 'phan': phan, 'bo_khoa': '|'.join(bo), 'pid': os.getpid()}
    t0 = time.perf_counter()
    if phan == 'ce':
        ca, t, meta = t046.nap(ds, oid, 'ce', mt)
        rec_g, bang, p, rec0 = t046.chay_voi_bo(ca, t, t046.cau_hinh('R0'), g, c, ng)
        out['trung_T045'] = (_dong(T045_CE, oid, 'T1-R0') == t046.json_ban_ghi(rec0, oid))
        if not out['trung_T045']:
            raise RuntimeError(f'bản ghi C-e khác T-045: {oid}')
        out['meta'] = meta
        out['verdict'] = {'khoa': t046.verdict_R0(bang, g, v, c=c, nguong=ng),
                          'G0|D0|V0': t046.verdict_R0(bang, 'G0', 'V0')}
        for vv in v_bao_cao:  # bản 4 C3: verdict chỉ báo cáo
            out['verdict'][f'{g}|{c}|{vv}'] = t046.verdict_R0(bang, g, vv, c=c, nguong=ng)
        out['ty_le_don_vi_co'] = t046.so_don_vi_co(bang, g, c, ng) / max(t046.so_don_vi_hop_le(bang), 1)
        out['verdict_chuoi_bo_khoa'] = rec_g['verdict']
        out['so_co'] = {'khoa': _so_co(bang, g, c, ng), 'G0|D0': _so_co(bang, 'G0', 'D0', {})}
        out['chi_nho_truc_tiep'] = t046.chi_nho_truc_tiep(bang, g, v, c, ng)
        out['phep_theo_o'] = _phep_theo_o(bang, g, c, ng)
        out['phep_theo_hau_to'] = _phep_theo_hau_to(bang, g)
        out['so_cham_hop_le'] = bang['so_cham_hop_le']
        # N5 (21:30): G1 chỉ để đối chiếu, không tham gia chọn hay khóa
        _, bang1, _, _ = t046.chay_voi_bo(ca, t, t046.cau_hinh('R0'), 'G1', c, ng)
        out['doi_chung_G1'] = {'verdict_V0': t046.verdict_R0(bang1, 'G1', 'V0', c=c, nguong=ng),
                               'so_co': _so_co(bang1, 'G1', c, ng),
                               'ty_le_don_vi_co': t046.so_don_vi_co(bang1, 'G1', c, ng) / max(t046.so_don_vi_hop_le(bang1), 1),
                               'phep_theo_o': _phep_theo_o(bang1, 'G1', c, ng)}
    elif phan == 'kdu':
        # A5: A/A và thật; thêm C-e (RE2-TT) sau khi thấy A/A 150 giây đánh giá thấp G3 so với cỡ 300 giây (16:03)
        for kieu in ('aa', 'that') + (('ce',) if ds == 'RE2-TT' else ()):
            ca, t, meta = t046.nap(ds, oid, kieu, mt)
            rec_g, bang, p, rec0 = t046.chay_voi_bo(ca, t, t046.cau_hinh('K-du'), g, c, ng)
            FI = t046.F_I_tu_ban_ghi(rec_g)
            out[kieu] = {'meta': meta, 'verdict_chuoi': rec_g['verdict'],
                         'verdict': {vv: t046.verdict_R0(bang, g, vv, F_I=FI, c=c, nguong=ng)
                                     for vv in tuple(v_bao_cao) or ('V0', 'V3')},
                         'bao_hoa': _bao_hoa(bang, g, ng, FI), 'so_cham_hop_le': bang['so_cham_hop_le'],
                         'phep_theo_o': _phep_theo_o(bang, g, c, ng),
                         'ty_le_don_vi_co': t046.so_don_vi_co(bang, g, c, ng) / max(t046.so_don_vi_hop_le(bang), 1)}
    elif phan == 'r0':
        ca, t, meta = t046.nap(ds, oid, 'that', mt)
        rec_g, bang, p, rec0 = t046.chay_voi_bo(ca, t, t046.cau_hinh('R0'), g, c, ng)
        K = rec_g['extra']['K_I_P']
        tang = rec_g['extra']['tang_P']
        t1 = [e for e, tg in tang.items() if tg == 1]
        dau = [K[e][0] for e in t1]
        mx = max(dau) if dau else None
        out['meta'] = meta
        out['verdict_chuoi'] = rec_g['verdict']
        out['verdict_bo_khoa'] = t046.verdict_R0(bang, g, v, c=c, nguong=ng)
        out['verdict_bao_cao'] = {vv: t046.verdict_R0(bang, g, vv, c=c, nguong=ng) for vv in v_bao_cao}
        out['ty_le_don_vi_co'] = t046.so_don_vi_co(bang, g, c, ng) / max(t046.so_don_vi_hop_le(bang), 1)
        out['tang1'] = len(t1)
        out['hoa_phan_tu_dau_o_dinh'] = sum(1 for x in dau if x == mx) if dau else 0
        out['tang1_s_bang_1'] = sum(1 for x in dau if x == 1.0)
        out['bao_hoa'] = _bao_hoa(bang, g, ng)
        out['so_thuc_the_khoi_dau'] = len(rec_g['blocks'][0]['groups'][0]) if rec_g['blocks'] else 0
        # C3 (thêm 16:04): hòa ở khối đầu khi thêm khóa phụ độ lớn T4c (S1), không nhãn; T4c có sẵn trong bản ghi (E6a)
        t4c = (rec_g['extra'].get('T4c') or {}).get('blocks')
        out['so_thuc_the_khoi_dau_T4c'] = len(t4c[0]['groups'][0]) if t4c else None
        out['so_khoi'] = len(rec_g['blocks'] or [])
        out['so_khoi_T4c'] = len(t4c) if t4c else None
        out['doi_hang_T4c'] = _doi_hang(rec_g['blocks'], t4c, tang) if t4c else None
    out['giay'] = round(time.perf_counter() - t0, 1)
    d = ra / phan
    d.mkdir(parents=True, exist_ok=True)
    (d / f'{oid}.json').write_bytes((json.dumps(out, ensure_ascii=False, sort_keys=True) + '\n').encode('utf-8'))
    return oid, out['giay']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ung-vien', required=True)
    ap.add_argument('--sha256', required=True)
    ap.add_argument('--phan', required=True, choices=('ce', 'kdu', 'r0'))
    ap.add_argument('--luot', required=True)
    ap.add_argument('--so', type=int, default=4)
    a = ap.parse_args()
    du = Path(a.ung_vien).read_bytes()
    if hashlib.sha256(du).hexdigest() != a.sha256:
        raise SystemExit('hash ung-vien.json khác hash đã ghi LOG: dừng')
    uv = json.loads(du.decode('utf-8'))
    k = uv['luat_chon']['to_hop_chon']
    if not k:
        raise SystemExit('chưa có bộ khóa')
    bo = tuple(k.split('|'))
    ra = Path(a.luot)
    ra.mkdir(parents=True, exist_ok=True)
    tat_ha_toc()
    mt = t046.moi_truong()
    ds_ca = [x for x in t046.danh_sach_ca(mt) if not (a.phan == 'ce' and x[0] != 'RE2-TT')]
    lam_ = [(ds, o) for ds, o in ds_ca if not (ra / a.phan / f'{o}.json').exists()]
    with open(ra / 'tham-so.json', 'ab') as f:
        f.write((json.dumps({'argv': sys.argv[1:], 'bo_khoa': k, 'PYTHONHASHSEED': os.environ.get('PYTHONHASHSEED'),
                             'bat_dau': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'can_chay': len(lam_)},
                            ensure_ascii=False) + '\n').encode('utf-8'))
    t0 = time.time()
    with open(ra / 'progress.jsonl', 'ab') as pf, ProcessPoolExecutor(max_workers=a.so) as ex:
        vb = tuple((uv.get('khoa') or {}).get('verdict_bao_cao_sau_khoa') or ())
        fut = {ex.submit(lam, a.phan, ds, o, bo, uv['nguong'], ra, vb): (ds, o) for ds, o in lam_}
        for i, f in enumerate(as_completed(fut), 1):
            ds, o = fut[f]
            try:
                oid, giay = f.result()
                rec = {'su_kien': 'xong', 'phan': a.phan, 'ca': oid, 'giay': giay, 'thu_tu': i,
                       'giay_tu_dau': round(time.time() - t0, 1), 'luc': time.strftime('%H:%M:%S')}
            except Exception as ex_:
                rec = {'su_kien': 'loi', 'phan': a.phan, 'ca': o, 'loi': f'{type(ex_).__name__}: {ex_}',
                       'luc': time.strftime('%H:%M:%S')}
            pf.write((json.dumps(rec, ensure_ascii=False) + '\n').encode('utf-8'))
            pf.flush()
            print(json.dumps(rec, ensure_ascii=False)[:200], flush=True)
    print('xong', round(time.time() - t0, 1))


if __name__ == '__main__':
    main()
