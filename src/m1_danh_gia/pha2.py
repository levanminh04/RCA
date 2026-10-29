"""Pha 2: đọc bản ghi pha 1 đã băm, kiểm hash, ghép nhãn, tính RR, Hit@1, hạng kỳ vọng, cờ M5 theo ba thế giới,
MRR theo dataset và gộp, WORLD_DEPENDENT (SPEC T-044 bước 5; SPEC T-043 B1.3b, Phụ lục C; CĐ2, CĐ6).
Chỉ package này đọc nhãn. Ca không OK có RR = 0 (WHY-28).
"""
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from m1_danh_gia import luat_c, m5, rr, the_gioi, uv6 as uv6_mod

WORLDS = ('P', 'S_lo', 'S_hi')


class LoiHash(ValueError):
    """Bản ghi pha 1 không khớp hash đã nhận."""


def _so(x):
    return None if x is None else float(x)


def doc(thu_muc, sha256):
    thu_muc = Path(thu_muc)
    meta = json.loads((thu_muc / 'pha1.json').read_text(encoding='utf-8'))
    du_lieu = (thu_muc / meta['tep']).read_bytes()
    h = hashlib.sha256(du_lieu).hexdigest()
    if h != sha256 or meta['sha256'] != sha256:
        raise LoiHash(f'hash lệch: tệp {h}, pha1.json {meta["sha256"]}, nhận {sha256}')
    return meta, [json.loads(x) for x in du_lieu.decode('utf-8').splitlines() if x]


def _blocks(rec, w):
    if rec.get('status') != 'OK':
        return []
    if w == 'P':
        return rec.get('blocks') or []
    return (rec.get('worlds') or {}).get(w, {}).get('blocks') or []


def cham(thu_muc, sha256, nhan):
    """nhan: {mã mờ: {'root', 'dataset', 'o', 'loai_loi'?}}. Trả {'cau_hinh': {config_id: {...}}, 'sha256'}."""
    meta, recs = doc(thu_muc, sha256)
    out = {}
    for rec in recs:
        cid, oid = rec['config_id'], rec['opaque_id']
        lab = nhan[oid]
        root, ok = lab['root'], rec.get('status') == 'OK'
        G_N = {tuple(c) for c in (rec.get('extra') or {}).get('G_N') or []}
        kq = out.setdefault(cid, {'ca': {}})
        theo_w = {}
        for w in WORLDS:
            b = _blocks(rec, w)
            theo_w[w] = {'RR': rr.rr_ca(b, root, ok), 'hit1': rr.hit1_ca(b, root, ok),
                         'hang': rr.hang_ky_vong(b, root) if ok else None, 'M5': ok and m5.co_M5(b, root, G_N)}
        wd = the_gioi.world_dependent({w: _blocks(rec, w) for w in WORLDS}, root) if ok else {'WORLD_DEPENDENT': False}
        kq['ca'][oid] = {'dataset': lab['dataset'], 'o': lab['o'], 'loai_loi': lab.get('loai_loi'),
                         'status': rec.get('status'), 'verdict': rec.get('verdict'), 'theo_the_gioi': theo_w,
                         'WORLD_DEPENDENT': wd['WORLD_DEPENDENT']}
    for cid, kq in out.items():
        ca = kq['ca']
        kq['MRR'] = {}
        kq['MRR_the_gioi'] = {}
        for w in WORLDS:
            r = {oid: c['theo_the_gioi'][w]['RR'] for oid, c in ca.items()}
            m = {'gop': rr.mrr(r)}
            for d in sorted({c['dataset'] for c in ca.values()}):
                m[d] = rr.mrr(r, {oid for oid, c in ca.items() if c['dataset'] == d})
            kq['MRR_the_gioi'][w] = {k: float(v) for k, v in m.items()}
        kq['MRR'] = kq['MRR_the_gioi']['P']
        kq['WORLD_DEPENDENT'] = sorted(oid for oid, c in ca.items() if c['WORLD_DEPENDENT'])
    return {'cau_hinh': out, 'sha256': sha256, 'so_ban_ghi': meta['so_ban_ghi']}


def ket_cuc_cap(kq, cid_tat, cid_bat, E_X, thanh_phan, buoc, moc_gia=None, trong_so=None, delta_d_co_dinh=None):
    """Luật C cho cặp (cid_tat, cid_bat) trong cả ba thế giới, rồi kết hợp theo phụ thuộc quan sát (CĐ6.2).
    Cặp E5 tự đếm cờ M5 theo thế giới; cặp E3 tự tính UV-6 theo thế giới (CĐ2). moc_gia: số đếm của hai nhánh."""
    tat, bat = kq['cau_hinh'][cid_tat]['ca'], kq['cau_hinh'][cid_bat]['ca']
    if set(tat) != set(bat):
        raise ValueError('hai cấu hình khác tập ca')
    ds = [{'ma': oid, 'dataset': tat[oid]['dataset'], 'o': tat[oid]['o']} for oid in sorted(tat)]
    theo = {}
    for w in WORLDS:
        rt = {oid: tat[oid]['theo_the_gioi'][w]['RR'] for oid in tat}
        rb = {oid: bat[oid]['theo_the_gioi'][w]['RR'] for oid in bat}
        them = {}
        if thanh_phan == 'E5':
            them['M5'] = (sum(tat[o]['theo_the_gioi'][w]['M5'] for o in tat),
                          sum(bat[o]['theo_the_gioi'][w]['M5'] for o in bat))
        if thanh_phan == 'E3':
            them['uv6'] = uv6_mod.dem([{'dataset': tat[o]['dataset'], 'loai_loi': tat[o]['loai_loi'],
                                        'hit1_tat': tat[o]['theo_the_gioi'][w]['hit1'],
                                        'hit1_bat': bat[o]['theo_the_gioi'][w]['hit1'],
                                        'hang_tat': tat[o]['theo_the_gioi'][w]['hang'],
                                        'hang_bat': bat[o]['theo_the_gioi'][w]['hang']} for o in sorted(tat)])
        theo[w] = luat_c.ap_dung(ds, rt, rb, E_X, thanh_phan=thanh_phan, moc_gia=moc_gia, trong_so=trong_so,
                                 delta_d_co_dinh=delta_d_co_dinh, **them)
    return {'theo_the_gioi': theo,
            'ket_hop': luat_c.ket_hop_the_gioi({w: theo[w]['ket_cuc'] for w in WORLDS}, buoc)}


def dem_moc_gia(kq_moc_gia, cid_tat, cid_bat):
    """Từ kết quả `cham` của lượt mốc giả: (CAUSE_FOUND, n) của hai nhánh trên mẫu số chung (D2f)."""
    tat, bat = kq_moc_gia['cau_hinh'][cid_tat]['ca'], kq_moc_gia['cau_hinh'][cid_bat]['ca']
    cap = [(tat[o]['verdict'], bat[o]['verdict']) for o in sorted(set(tat) & set(bat))]
    giu = [(a, b) for a, b in cap if 'INSUFFICIENT_EVIDENCE' not in (a, b) and None not in (a, b)]
    n = len(giu)
    return ((sum(a == 'CAUSE_FOUND' for a, _ in giu), n), (sum(b == 'CAUSE_FOUND' for _, b in giu), n),
            {'bi_loai': len(cap) - n})
