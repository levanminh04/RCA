"""Luật C (SPEC T-043 Phụ lục C; D2b, D2f; ma-tran-thu.json#/luat_C; dinh-nghia-pha2.json#/rr_theo_o;
dinh-chinh-cai-dat.md CĐ2, CĐ6.2, CĐ6.4, CĐ13). Chạy sau ghép nhãn. Mọi phép so dùng phân số chính xác.

Áp theo thứ tự, dừng ở bước đầu tiên khớp:
1. HẠI riêng: UV-6 (cặp E3); điều kiện M5 (cặp E5); vế mốc giả; M + M′ >= 3 và P + P′ = 0.
2. TRÁI CHIỀU theo dataset: ΔMRR_d > δ_d ở một dataset và ΔMRR_d′ < −δ_d′ ở dataset kia.
3. HẠI gộp: ΔMRR gộp < −δ.
4. KHÔNG ĐỦ CA: |E_X| < 6.
5. GIÚP: ΔMRR gộp > δ, P > M, không dataset nào ΔMRR_d < −δ_d.
6. KHÔNG TÁC DỤNG: |ΔMRR gộp| <= δ.
7. TRÁI CHIỀU theo ô.
Cặp (R0, c) nhiều thành phần (thanh_phan = 'R0,c'): không áp UV-6 và M5 (CĐ6.4).
Trọng số (CĐ13; SPEC T-045 bước 7): `trong_so` là bội số của ô, gán cho mọi ca của ô (ô được lấy k lần thì mọi ca
của ô có trọng số k). MRR, RR_o tính có trọng số; P, M, P′, M′ đếm ô theo bội số. Tập E_X, số ô của E_X (cho KHÔNG
ĐỦ CA) và δ_d giữ cố định từ T0; δ_d truyền qua `delta_d_co_dinh`.
RR_o tăng khi ΔRR_o > 1e-12, giảm khi ΔRR_o < −1e-12 (rr_theo_o#/tang_giam).
"""
from fractions import Fraction
from math import comb

from m1_danh_gia import moc_gia as moc_gia_mod, rr

DELTA = Fraction(1, 100)
NGUONG_O = Fraction(1, 10 ** 12)
O_TOI_THIEU = 6
M_TOI_THIEU = 3
N_MAC_DINH = {'RE2-TT': 30, 'Nezha-OB': 22}
NHIEU_THANH_PHAN = 'R0,c'


def _fr(x):
    """Số dùng để quyết định phải chính xác (CĐ16): Fraction hoặc int; số thực, chuỗi, bool là lỗi."""
    if isinstance(x, bool) or not isinstance(x, (Fraction, int)):
        raise TypeError(f'cần phân số chính xác, nhận {type(x).__name__}: {x!r}')
    return Fraction(x)


def tong_hop(ds, tat, bat, E_X, trong_so=None):
    """ds: [{'ma', 'dataset', 'o'}]; tat, bat: {ma: RR}. Trả ΔMRR theo dataset và gộp, P, M, P′, M′, RR_o."""
    o_cua, ds_cua = {}, {}
    for c in ds:
        if c['ma'] in o_cua:
            raise ValueError(f"mã ca trùng trong ds: {c['ma']}")
        o_cua[c['ma']] = c['o']
        if ds_cua.setdefault(c['o'], c['dataset']) != c['dataset']:
            raise ValueError(f"mã ô {c['o']} trùng giữa hai dataset")
    if isinstance(E_X, str) or not set(E_X) <= set(o_cua.values()):
        raise ValueError(f'E_X có ô không thuộc ds: {sorted(map(repr, set(E_X) - set(o_cua.values())))[:5]}')
    rt = {c['ma']: _fr(tat[c['ma']]) for c in ds}
    rb = {c['ma']: _fr(bat[c['ma']]) for c in ds}
    datasets = sorted({c['dataset'] for c in ds})
    MRR_t, MRR_b, dM = {}, {}, {}
    for d in datasets:
        chon = {c['ma'] for c in ds if c['dataset'] == d}
        MRR_t[d], MRR_b[d] = rr.mrr(rt, chon, trong_so), rr.mrr(rb, chon, trong_so)
        dM[d] = MRR_b[d] - MRR_t[d]
    MRR_t['gop'], MRR_b['gop'] = rr.mrr(rt, None, trong_so), rr.mrr(rb, None, trong_so)
    dM['gop'] = MRR_b['gop'] - MRR_t['gop']
    o_t, o_b = rr.rr_o(rt, o_cua, trong_so), rr.rr_o(rb, o_cua, trong_so)
    boi = {}
    for c in ds:
        w = rr.boi_so(trong_so, c['ma'])  # map thưa là lỗi (S25)
        if w < 0 or w.denominator != 1:
            raise ValueError(f"bội số của ca {c['ma']} phải là số nguyên không âm")
        if boi.setdefault(c['o'], w) != w:
            raise ValueError(f"các ca của ô {c['o']} có bội số khác nhau")
    P = M = Pp = Mp = 0
    huong_o = {}
    for o in sorted(o_t):
        x = o_b[o] - o_t[o]
        h = 1 if x > NGUONG_O else (-1 if x < -NGUONG_O else 0)
        huong_o[o] = h
        k = boi[o]
        if o in E_X:
            P, M = P + k * (h > 0), M + k * (h < 0)
        else:
            Pp, Mp = Pp + k * (h > 0), Mp + k * (h < 0)
    P, M, Pp, Mp = (int(x) for x in (P, M, Pp, Mp))
    return {'dMRR': dM, 'MRR_tat': MRR_t, 'MRR_bat': MRR_b, 'P': P, 'M': M, 'P_phay': Pp, 'M_phay': Mp,
            'so_o_E_X': len(set(E_X)), 'huong_o': huong_o, 'datasets': datasets}


def ket_cuc_tu_tong_hop(t, hai_rieng=(), delta=DELTA, delta_d=None):
    """t: {'dMRR': {'gop', dataset...}, 'P', 'M', 'P_phay', 'M_phay', 'so_o_E_X'}; hai_rieng: lý do HẠI riêng đã tính."""
    dM = {k: _fr(v) for k, v in t['dMRR'].items()}
    ds = sorted(k for k in dM if k != 'gop')
    dd = {d: _fr(delta_d[d]) if delta_d and d in delta_d else Fraction(1, N_MAC_DINH[d]) for d in ds}
    delta = _fr(delta)
    ly_do = list(hai_rieng)
    if t['M'] + t['M_phay'] >= M_TOI_THIEU and t['P'] + t['P_phay'] == 0:
        ly_do.append('M_cong_M_phay')
    if ly_do:
        return {'ket_cuc': 'HAI', 'buoc': 1, 'ly_do_hai_rieng': ly_do, 'delta_d': dd}
    if any(dM[a] > dd[a] for a in ds) and any(dM[b] < -dd[b] for b in ds):
        return {'ket_cuc': 'TRAI_CHIEU_DATASET', 'buoc': 2, 'ly_do_hai_rieng': [], 'delta_d': dd}
    if dM['gop'] < -delta:
        return {'ket_cuc': 'HAI', 'buoc': 3, 'ly_do_hai_rieng': [], 'delta_d': dd}
    if t['so_o_E_X'] < O_TOI_THIEU:
        return {'ket_cuc': 'KHONG_DU_CA', 'buoc': 4, 'ly_do_hai_rieng': [], 'delta_d': dd}
    if dM['gop'] > delta and t['P'] > t['M'] and not any(dM[d] < -dd[d] for d in ds):
        return {'ket_cuc': 'GIUP', 'buoc': 5, 'ly_do_hai_rieng': [], 'delta_d': dd}
    if abs(dM['gop']) <= delta:
        return {'ket_cuc': 'KHONG_TAC_DUNG', 'buoc': 6, 'ly_do_hai_rieng': [], 'delta_d': dd}
    return {'ket_cuc': 'TRAI_CHIEU_O', 'buoc': 7, 'ly_do_hai_rieng': [], 'delta_d': dd}


def p_kiem_dau(P, M):
    """Kiểm dấu chính xác hai phía trên các ô lệch (báo kèm, không dùng để quyết định)."""
    n = P + M
    if n == 0:
        return Fraction(1)
    k = min(P, M)
    return min(Fraction(1), 2 * Fraction(sum(comb(n, i) for i in range(k + 1)), 2 ** n))


def ap_dung(ds, tat, bat, E_X, thanh_phan='X', M5=None, moc_gia=None, uv6=None, trong_so=None,
            delta_d_co_dinh=None, delta=DELTA):
    """Kết cục luật C cho cặp (tắt, bật).
    M5: (số ca có cờ M5 của c bỏ E5, của c); moc_gia: ((CAUSE_FOUND, n) nhánh tắt, (CAUSE_FOUND, n) nhánh bật);
    uv6: kết quả uv6.dem (cần 'vi_pham'); trong_so: {ma: bội số}; delta_d_co_dinh: {dataset: δ_d}."""
    E_X = set(E_X)
    t = tong_hop(ds, tat, bat, E_X, trong_so)
    if delta_d_co_dinh:
        dd = {d: _fr(delta_d_co_dinh[d]) for d in t['datasets']}
    else:
        dd = {d: Fraction(1, sum(1 for c in ds if c['dataset'] == d)) for d in t['datasets']}
    hai = []
    if thanh_phan == 'E5':
        if M5 is None:
            raise ValueError('cặp E5 cần số ca có cờ M5 của hai nhánh')
        dk5 = 'HAI' if M5[1] > M5[0] else 'KHONG_HAI'
        if dk5 == 'HAI':
            hai.append('dieu_kien_E5')
    else:
        dk5 = 'KHONG_AP'
    if thanh_phan == 'E3':
        if uv6 is None:
            raise ValueError('cặp E3 cần kết quả UV-6')
        dk3 = 'HAI' if uv6['vi_pham'] else 'KHONG_HAI'
        if dk3 == 'HAI':
            hai.append('UV-6')
    else:
        dk3 = 'KHONG_AP'
    mg = None
    if moc_gia is not None:
        mg = moc_gia_mod.ve_tu_dem(tuple(moc_gia[0]), tuple(moc_gia[1]))
        if mg['ve'] == 'HAI':
            hai.append('moc_gia')
    kc = ket_cuc_tu_tong_hop(t, hai, delta=delta, delta_d=dd)
    bao_kem = {'p_kiem_dau': p_kiem_dau(t['P'], t['M']),
               'ket_cuc_delta_0005': ket_cuc_tu_tong_hop(t, hai, delta=Fraction(5, 1000), delta_d=dd)['ket_cuc'],
               'ket_cuc_delta_002': ket_cuc_tu_tong_hop(t, hai, delta=Fraction(2, 100), delta_d=dd)['ket_cuc']}
    return dict(kc, thanh_phan=thanh_phan, dMRR=t['dMRR'], MRR_tat=t['MRR_tat'], MRR_bat=t['MRR_bat'], P=t['P'],
                M=t['M'], P_phay=t['P_phay'], M_phay=t['M_phay'], so_o_E_X=t['so_o_E_X'], huong_o=t['huong_o'],
                dieu_kien_E5=dk5, UV6=dk3, moc_gia=mg, bao_kem=bao_kem)


def ket_hop_the_gioi(ket_cuc, buoc):
    """Phụ thuộc quan sát (Phụ lục C; D2f; CĐ6.2). ket_cuc: {'P', 'S_lo', 'S_hi'}; buoc: 'khoi_K' hoặc 'luat_C'.
    Khối K: kết cục tại P vẫn ghi, cặp phụ thuộc quan sát không là căn cứ loại. Bước theo luật C (T6, T9, T11, T12):
    xử lý như KHÔNG ĐỦ CA."""
    if buoc not in ('khoi_K', 'luat_C'):
        raise ValueError(buoc)
    P = ket_cuc['P']
    ptqs = any(ket_cuc[w] != P for w in ('S_lo', 'S_hi'))
    dung = 'KHONG_DU_CA' if (ptqs and buoc == 'luat_C') else P
    return {'ket_cuc_P': P, 'theo_the_gioi': {w: ket_cuc[w] for w in ('P', 'S_lo', 'S_hi')},
            'phu_thuoc_quan_sat': ptqs, 'ket_cuc_dung': dung, 'can_cu_loai': (not ptqs) and P == 'HAI'}
