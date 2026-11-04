"""Luật C T-047: vế N1 theo SPEC/WHY-70; không sửa bộ đánh giá gốc.

Không đọc file/nhãn. Caller pha 2 cung cấp kết quả đã chấm và bản ghi C-e.
Điểm nối _gan_ve cũng dùng hồi quy với vế cũ trên dữ liệu giả.
"""
import copy
from fractions import Fraction
from itertools import combinations

from m1_danh_gia import chon_khoi, luat_c, pha2, rr

TP = ('E1', 'E2', 'E3', 'E5')
IT_CA = ('E3',)
DO_THI = ('E1', 'E2', 'E5')
WORLDS = pha2.WORLDS
DD = {'RE2-TT': Fraction(1, 30), 'Nezha-OB': Fraction(1, 22)}
H = Fraction(1)


def _n1(rec):
    status = rec.get('status')
    if status not in ('OK', 'NO_EVIDENCE'):
        raise ValueError(f'C-e có trạng thái lỗi/lạ: {status!r}')
    vd = rec.get('verdict')
    if vd not in ('CAUSE_FOUND', 'NO_INTRINSIC_ANOMALY', 'INSUFFICIENT_EVIDENCE'):
        raise ValueError('C-e thiếu hoặc sai verdict')
    tang = (rec.get('extra') or {}).get('tang_P')
    if not isinstance(tang, dict) or any(type(v) is not int or v not in (1, 2, 3) for v in tang.values()):
        raise ValueError('C-e thiếu hoặc sai tang_P')
    n = sum(v == 1 for v in tang.values())
    if (vd == 'CAUSE_FOUND') != (n > 0):
        raise ValueError('C-e verdict không khớp tầng 1')
    return n


def ve_n1(tat, bat, trong_so=None, h=H):
    """tat/bat: {opaque_id: bản ghi C-e}. Không lấy nhãn, không dùng tỷ lệ V0."""
    h = luat_c._fr(h)
    if h < 0 or set(tat) != set(bat) or not tat:
        raise ValueError('ngưỡng/tập cửa sổ C-e không hợp lệ')
    rows, tong_t, tong_b, n = [], 0, 0, 0
    for oid in sorted(tat):
        a, b = tat[oid], bat[oid]
        na, nb = _n1(a), _n1(b)  # kiểm cả bản ghi có bội số 0; không che lỗi
        w = int(rr.boi_so(trong_so, oid))
        loai = 'INSUFFICIENT_EVIDENCE' in (a['verdict'], b['verdict'])
        rows.append({'opaque_id': oid, 'N1_tat': na, 'N1_bat': nb, 'w': w,
                     'V0_tat': a['verdict'], 'V0_bat': b['verdict'],
                     'bi_loai': loai, 'ly_do': 'INSUFFICIENT_EVIDENCE' if loai else None})
        if not loai:
            n += w
            tong_t += w * na
            tong_b += w * nb
    delta = Fraction(tong_b - tong_t, n) if n else None
    return {'ve': 'CHUA_KIEM_DUOC' if not n else ('HAI' if delta > h else 'KHONG_KICH_HOAT'),
            'h': h, 'n': n, 'tang': delta,
            'trung_binh_tat': Fraction(tong_t, n) if n else None,
            'trung_binh_bat': Fraction(tong_b, n) if n else None,
            'so_cua_so_hop_le': sum(not x['bi_loai'] for x in rows),
            'so_bi_loai': sum(x['bi_loai'] for x in rows),
            'boi_so_bi_loai': sum(x['w'] for x in rows if x['bi_loai']), 'cua_so': rows}


def _gan_ve(nen, ve):
    """Thay vế mốc giả sau tính nền; giữ mọi trường khác, tính lại kết cục/δ."""
    out = copy.deepcopy(nen)
    hai = []
    if out['dieu_kien_E5'] == 'HAI':
        hai.append('dieu_kien_E5')
    if out['UV6'] == 'HAI':
        hai.append('UV-6')
    if ve['ve'] == 'HAI':
        hai.append('moc_gia')
    out.update(luat_c.ket_cuc_tu_tong_hop(out, hai, delta_d=out['delta_d']))
    out['moc_gia'] = copy.deepcopy(ve)
    for key, delta in [('ket_cuc_delta_0005', Fraction(5, 1000)), ('ket_cuc_delta_002', Fraction(2, 100))]:
        out['bao_kem'][key] = luat_c.ket_cuc_tu_tong_hop(out, hai, delta=delta, delta_d=out['delta_d'])['ket_cuc']
    return out


def _cap_voi_ve(kq, cid_tat, cid_bat, E_X, thanh_phan, buoc, ve, trong_so=None, delta_d_co_dinh=None):
    nen = pha2.ket_cuc_cap(kq, cid_tat, cid_bat, E_X, thanh_phan, buoc,
                          moc_gia=None, trong_so=trong_so, delta_d_co_dinh=delta_d_co_dinh)
    theo = {w: _gan_ve(nen['theo_the_gioi'][w], ve) for w in WORLDS}
    return {'theo_the_gioi': theo,
            'ket_hop': luat_c.ket_hop_the_gioi({w: theo[w]['ket_cuc'] for w in WORLDS}, buoc),
            'khong_moc_gia': {w: nen['theo_the_gioi'][w]['ket_cuc'] for w in WORLDS}}


def ket_cuc_cap(kq, cid_tat, cid_bat, E_X, thanh_phan, ce, trong_so=None, h=H):
    ve = ve_n1(ce[cid_tat], ce[cid_bat], trong_so, h)
    return _cap_voi_ve(kq, cid_tat, cid_bat, E_X, thanh_phan, 'khoi_K', ve,
                      trong_so=trong_so, delta_d_co_dinh=DD)


def cac_cap():
    out = {}
    for n in range(5):
        for combo in combinations(TP, n):
            s = set(combo)
            b = chon_khoi.ten(s, TP)
            if len(s) > 1:
                out['R0|' + b] = ('R0', b, luat_c.NHIEU_THANH_PHAN, sorted(s))
            for x in sorted(s):
                a = chon_khoi.ten(s - {x}, TP)
                out[a + '|' + b] = (a, b, x, [x])
    return out


def danh_gia_khoi(kq, ce, E_X, trong_so=None, h=H):
    """Cùng đường tính cho pha 2, bootstrap và độ nhạy h; đủ bước 1–8/10."""
    if set(ce) != set(kq['cau_hinh']):
        raise ValueError('C-e và cửa sổ thật khác tập cấu hình')
    cap = {}
    for key, (a, b, tp, comps) in cac_cap().items():
        ex = sorted(set().union(*(E_X[x] for x in comps)))
        cap[key] = ket_cuc_cap(kq, 'K-' + a, 'K-' + b, ex, tp, ce, trong_so, h)
    hop = {k: v['ket_hop'] for k, v in cap.items()}
    ch, b8 = {}, {}
    for w in WORLDS:
        mrr = {c[2:]: m['gop'] for c, m in pha2.mrr_cau_hinh(kq, trong_so, w).items()}
        ch[w] = chon_khoi.chon(TP, IT_CA, DO_THI, mrr, hop, the_gioi=w)
        winner = ch[w]['chon']
        flagged = sorted(k for k, v in cap.items() if v['theo_the_gioi']['P']['moc_gia']['ve'] == 'CHUA_KIEM_DUOC')
        relevant = [k for k in flagged if winner in k.split('|')] if winner else []
        ch[w]['cap_Ce_chua_kiem'] = flagged
        ch[w]['cap_Ce_chua_kiem_o_thang'] = relevant
        ch[w]['can_Minh_truoc_task2'] = bool(relevant)
        if relevant:
            ch[w]['trinh_Minh'] = True
            ch[w]['ly_do_trinh_Minh'].append('Ce_chua_kiem_o_thang')
        h8 = hop if w == 'P' else {k: v['theo_the_gioi'][w] for k, v in hop.items()}
        b8[w] = chon_khoi.kiem_cau_hinh_thang(winner, TP, h8, IT_CA) if winner else None
    return {'h': luat_c._fr(h), 'cap': cap, 'chon_khoi': ch, 'buoc8': b8}
