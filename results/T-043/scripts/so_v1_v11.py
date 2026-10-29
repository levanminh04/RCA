"""Phiên 8 T-043: so đầu ra KS-16 theo luật F v1 (pha1-001, pha2-001) với luật F v1.1 (pha1-002, pha2-002). Chỉ đọc file kết quả.

Liệt kê mọi con trỏ JSON có giá trị khác nhau, trừ siêu dữ liệu lượt chạy (run, created_utc, cost), gom theo mẫu đường dẫn
(mã ca và chỉ số danh sách thay bằng *), kèm vài ví dụ cũ → mới. Tóm tắt trạng thái ô và T của từng nguồn ở hai bản.
Đếm đơn vị đếm đổi quyết định khi T đổi (không nhãn, chỉ dùng file pha 1): phép nhị thức của KS-16 pha 2
(p0 = T_A / (T_N + T_A), α = 0,01, hai phía, tổng >= 10), không phải điểm E4 đầy đủ.
Phần pha 2 đọc file sau barrier (có nhãn root, loại lỗi); không đọc file nhãn gốc.
Tính điểm sau cổng của đơn vị đếm (SPEC B1.3: λ = n_N · T_A / T_N, e_up, e_dn) ở thế giới P cho hai bản T.
Chạy: python -B results/T-043/scripts/so_v1_v11.py --out results/T-043/runs/so-v1-v11-004
(giữ lại: so-v1-v11-001 dùng bản đầu của script, chưa tách khác kiểu số; so-v1-v11-002 còn tính thời gian chạy
 theo ca (cases/*/cost) là khác giá trị, nên danh sách ca có khác giá trị gồm đủ 52 ca; so-v1-v11-003 chưa có phần điểm.)
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

from scipy.stats import binom

ROOT = Path(__file__).resolve().parents[3]
ALPHA = 0.01
M_COUNT = 10
CAP = {
    'pha1': ('results/T-043/ks16/runs/pha1-001/dem-khong-nhan.json', 'results/T-043/ks16/runs/pha1-002/dem-khong-nhan.json'),
    'pha2': ('results/T-043/ks16/runs/pha2-001/dem-sau-ghep-nhan.json', 'results/T-043/ks16/runs/pha2-002/dem-sau-ghep-nhan.json'),
}
BO_QUA = {'run', 'created_utc', 'cost'}
MA_CA = re.compile(r'^dev-[0-9a-f]{10}$')


def sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()


def doc(p):
    """Đọc JSON; nếu `cases` là danh sách có opaque_id thì đổi thành dict theo opaque_id để con trỏ mang mã ca."""
    with open(ROOT / p, encoding='utf-8') as f:
        d = json.load(f)
    c = d.get('cases')
    if isinstance(c, list) and all(isinstance(x, dict) and 'opaque_id' in x for x in c):
        d['cases'] = {x['opaque_id']: x for x in c}
    return d


def thoat(k):
    return str(k).replace('~', '~0').replace('/', '~1')


def la_so(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def phang(x):
    """Danh sách khoảng một phần tử [[a, b]] (v1.1) coi như [a, b] (v1) khi so dạng biểu diễn."""
    if isinstance(x, list) and len(x) == 1 and isinstance(x[0], list):
        return x[0]
    return x


def so(a, b, path, out):
    """out nhận (path, a, b, loai): loai 'gia_tri' khi khác giá trị; 'kieu' khi chỉ khác kiểu số (300 và 300.0)
    hoặc khác dạng danh sách khoảng một phần tử."""
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b), key=str):
            if (not path and k in BO_QUA) or (len(path) == 2 and path[0] == 'cases' and k == 'cost'):
                continue
            p = path + [k]
            if k not in a or k not in b:
                out.append((p, a.get(k, '<không có>'), b.get(k, '<không có>'), 'gia_tri'))
            else:
                so(a[k], b[k], p, out)
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            so(x, y, path + [i], out)
    elif isinstance(a, list) and isinstance(b, list) and phang(a) == phang(b):
        out.append((path, a, b, 'kieu'))
    elif la_so(a) and la_so(b) and a == b:
        if type(a) is not type(b):
            out.append((path, a, b, 'kieu'))
    elif a != b or type(a) is not type(b):
        out.append((path, a, b, 'gia_tri'))


def mau(path, ds_cua_ca):
    parts = []
    for i, k in enumerate(path):
        if i == 1 and path[0] == 'cases' and MA_CA.match(str(k)):
            parts.append(ds_cua_ca.get(k, '?') + ':*')
        elif isinstance(k, int) or MA_CA.match(str(k)):
            parts.append('*')
        else:
            parts.append(thoat(k))
    return '/' + '/'.join(parts)


def gom(diffs, ds_cua_ca):
    nhom = {}
    for p, a, b, loai in diffs:
        g = nhom.setdefault(loai, {}).setdefault(mau(p, ds_cua_ca), {'so_con_tro': 0, 'lech_tuyet_doi_lon_nhat': None, 'vi_du': []})
        g['so_con_tro'] += 1
        if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
            d = abs(b - a)
            g['lech_tuyet_doi_lon_nhat'] = d if g['lech_tuyet_doi_lon_nhat'] is None else max(g['lech_tuyet_doi_lon_nhat'], d)
        if len(g['vi_du']) < 4:
            g['vi_du'].append({'con_tro': '/' + '/'.join(thoat(k) for k in p), 'v1': a, 'v1_1': b})
    return nhom


def tom_tat_quan_sat(d):
    out = {}
    for ds, th in d['tong_hop'].items():
        out[ds] = {src: {'o': v['o'], 'T': v['T'], 'ca_co_o_OPEN': v['ca_co_o_OPEN']} for src, v in th['quan_sat'].items()}
    return out


def T_theo_ca(d, ds, src):
    r = {}
    for oid, c in d['cases'].items():
        if c.get('dataset') != ds:
            continue
        qs = c.get('quan_sat', {}).get(src)
        if qs is None:
            continue
        r[oid] = {side: qs['T'][side] for side in ('N', 'A') if side in qs.get('T', {})}
    return r


def quyet(nN, nA, TN, TA):
    if nN + nA < M_COUNT or TN <= 0 or TA <= 0:
        return None
    p0 = TA / (TN + TA)
    n = nN + nA
    return bool(binom.sf(nA - 1, n, p0) < ALPHA or binom.cdf(nA, n, p0) < ALPHA)


def diem(nN, nA, TN, TA):
    """Điểm sau cổng theo SPEC B1.3: e_d nếu qua kiểm nhị thức hướng d và e_d > 0, ngược lại 0. Không áp hướng chấm của kênh."""
    if nN + nA < M_COUNT or TN <= 0 or TA <= 0:
        return None
    p0 = TA / (TN + TA)
    n = nN + nA
    lam = nN * TA / TN
    e_up = max(0.0, (nA - lam) / max(nA, 1))
    e_dn = max(0.0, (lam - nA) / max(lam, 1))
    s_up = e_up if binom.sf(nA - 1, n, p0) < ALPHA and e_up > 0 else 0.0
    s_dn = e_dn if binom.cdf(nA, n, p0) < ALPHA and e_dn > 0 else 0.0
    return e_up, e_dn, s_up, s_dn


def doi_diem(a, b):
    """Thế giới P. Lệch lớn nhất của e thô và điểm sau cổng giữa v1 và v1.1, theo dataset và loại đơn vị."""
    out = {}
    for oid, ca in a['cases'].items():
        cb = b['cases'][oid]
        for src, loai, khoa, nN, nA in don_vi_dem(ca):
            qa, qb = ca.get('quan_sat', {}).get(src), cb.get('quan_sat', {}).get(src)
            if qa is None or qb is None:
                continue
            d1, d2 = diem(nN, nA, *qa['worlds']['P']), diem(nN, nA, *qb['worlds']['P'])
            if d1 is None or d2 is None:
                continue
            g = out.setdefault(ca['dataset'], {}).setdefault(loai, {
                'don_vi': 0, 'max_lech_e_tho': 0.0, 'max_lech_diem_sau_cong': 0.0, 'so_don_vi_diem_doi': 0, 'vi_du_lech_diem_lon_nhat': None})
            g['don_vi'] += 1
            g['max_lech_e_tho'] = max(g['max_lech_e_tho'], abs(d1[0] - d2[0]), abs(d1[1] - d2[1]))
            ld = max(abs(d1[2] - d2[2]), abs(d1[3] - d2[3]))
            if ld > 0:
                g['so_don_vi_diem_doi'] += 1
            if ld > g['max_lech_diem_sau_cong']:
                g['max_lech_diem_sau_cong'] = ld
                g['vi_du_lech_diem_lon_nhat'] = {'ca': oid, 'khoa': khoa, 'nN': nN, 'nA': nA,
                                                 'v1_s_up_s_dn': [d1[2], d1[3]], 'v1_1_s_up_s_dn': [d2[2], d2[3]]}
    return out


def don_vi_dem(c):
    """(nguồn, loại, khóa, nN, nA). Tần suất thao tác bỏ nN = 0 hoặc nA = 0 (NEW_OP/STOPPED không dùng T)."""
    out = []
    for r in c.get('op_rows', []):
        if r[2] > 0 and r[3] > 0:
            out.append(('trace', 'tan_suat_thao_tac', f'{r[0]}|{r[1]}', r[2], r[3]))
    for r in c.get('log_rows', []):
        out.append(('log', 'log_tong_theo_thuc_the', r[0], r[1], r[2]))
        out.append(('log', 'log_loi_theo_thuc_the', r[0], r[3], r[4]))
    return out


def lat_dem(a, b):
    tong = {}
    lat = []
    for oid, ca in a['cases'].items():
        cb = b['cases'][oid]
        ds = ca['dataset']
        for src, loai, khoa, nN, nA in don_vi_dem(ca):
            qa, qb = ca.get('quan_sat', {}).get(src), cb.get('quan_sat', {}).get(src)
            if qa is None or qb is None:
                continue
            for w in ('P', 'S_lo', 'S_hi'):
                d1 = quyet(nN, nA, *qa['worlds'][w])
                d2 = quyet(nN, nA, *qb['worlds'][w])
                if d1 is None and d2 is None:
                    continue
                g = tong.setdefault(ds, {}).setdefault(loai, {}).setdefault(w, {'kiem': 0, 'co_v1': 0, 'co_v1_1': 0, 'lat': 0})
                g['kiem'] += 1
                g['co_v1'] += int(bool(d1))
                g['co_v1_1'] += int(bool(d2))
                if d1 != d2:
                    g['lat'] += 1
                    lat.append({'ca': oid, 'the_gioi': w, 'loai': loai, 'khoa': khoa, 'nN': nN, 'nA': nA, 'v1': d1, 'v1_1': d2})
    return {'tong': tong, 'don_vi_lat': lat}


def T_tuong_doi(a, b):
    out = {}
    for src in ('trace', 'log'):
        lon_nhat = None
        for oid, ca in a['cases'].items():
            if ca['dataset'] != 'Nezha-OB':
                continue
            for side in ('N', 'A'):
                x = ca['quan_sat'][src]['T'][side]['chac']
                y = b['cases'][oid]['quan_sat'][src]['T'][side]['chac']
                if x != y:
                    rel = (x - y) / x
                    if lon_nhat is None or rel > lon_nhat['ty_le_giam']:
                        lon_nhat = {'ca': oid, 'phia': side, 'v1': x, 'v1_1': y, 'giam_s': x - y, 'ty_le_giam': rel}
        out[src] = lon_nhat
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    out_dir = ROOT / args.out
    out_dir.mkdir(parents=True, exist_ok=False)
    ket_qua = {'schema': 'T043-so-v1-v11-v2', 'labels_read': 'pha 1: không; pha 2: đọc file sau barrier (có root, loại lỗi), không đọc file nhãn gốc',
               'dau_vao': {}, 'so_sanh': {}}
    docs = {}
    for ten, (p_cu, p_moi) in CAP.items():
        ket_qua['dau_vao'][ten] = {p_cu: sha(p_cu), p_moi: sha(p_moi)}
        a, b = doc(p_cu), doc(p_moi)
        docs[ten] = (a, b)
        diffs = []
        so(a, b, [], diffs)
        ds_cua_ca = {oid: c.get('dataset', '?') for oid, c in a.get('cases', {}).items()}
        ket_qua['so_sanh'][ten] = {
            'bo_qua_cap_goc': sorted(BO_QUA),
            'so_con_tro_khac_gia_tri': sum(1 for d in diffs if d[3] == 'gia_tri'),
            'so_con_tro_chi_khac_kieu': sum(1 for d in diffs if d[3] == 'kieu'),
            'ca_co_khac_gia_tri': sorted({d[0][1] for d in diffs if d[3] == 'gia_tri' and d[0][0] == 'cases'}),
            'nhom': gom(diffs, ds_cua_ca),
        }
    a, b = docs['pha1']
    ket_qua['quan_sat_tong_hop'] = {'v1': tom_tat_quan_sat(a), 'v1_1': tom_tat_quan_sat(b)}
    lech_T = {}
    for src in ('trace', 'log'):
        t1, t2 = T_theo_ca(a, 'Nezha-OB', src), T_theo_ca(b, 'Nezha-OB', src)
        rows = {}
        for oid in sorted(t1):
            for side in ('N', 'A'):
                x, y = t1[oid].get(side), t2[oid].get(side)
                if x != y:
                    rows.setdefault(oid, {})[side] = {'v1': x, 'v1_1': y}
        lech_T[src] = rows
    ket_qua['T_Nezha_OB_theo_ca_khac'] = lech_T
    ket_qua['T_Nezha_OB_giam_tuong_doi_lon_nhat'] = T_tuong_doi(a, b)
    ket_qua['don_vi_dem_doi_quyet_dinh'] = lat_dem(a, b)
    ket_qua['don_vi_dem_doi_diem_the_gioi_P'] = doi_diem(a, b)
    a2, b2 = docs['pha2']
    ket_qua['pha2_kich_hoat_giong_nhau_moi_ca'] = all(a2['cases'][k]['kich_hoat'] == b2['cases'][k]['kich_hoat'] for k in a2['cases'])
    ket_qua['pha2_do_dai_ly_do_E3b'] = {
        'giong_nhau_moi_ca': all(len(a2['cases'][k]['ly_do'].get('E3b', [])) == len(b2['cases'][k]['ly_do'].get('E3b', [])) for k in a2['cases']),
        'dai_nhat': max(len(c['ly_do'].get('E3b', [])) for c in b2['cases'].values()),
        'tran_cat': 20,
    }
    (out_dir / 'ket-qua.json').write_text(json.dumps(ket_qua, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({t: {'so_con_tro_khac_gia_tri': v['so_con_tro_khac_gia_tri'], 'so_con_tro_chi_khac_kieu': v['so_con_tro_chi_khac_kieu'],
                          'ca_co_khac_gia_tri': len(v['ca_co_khac_gia_tri']),
                          'nhom_gia_tri': {k: [g['so_con_tro'], g['lech_tuyet_doi_lon_nhat']] for k, g in v['nhom'].get('gia_tri', {}).items()}}
                      for t, v in ket_qua['so_sanh'].items()}, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
