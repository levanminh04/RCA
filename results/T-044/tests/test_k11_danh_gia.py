"""Khối 11: bộ đánh giá — luật C (34–40, 51–54, 60), luật chọn khối (45–47, 49, 50), bối cảnh (48),
dấu vết E5 phía bộ đánh giá (80); M5, UV-6, bước 8, cặp (R0, c), phụ thuộc quan sát, trọng số (tự lập); Đ17."""
from fractions import Fraction

import pytest

from conftest import fx, gan_bang, phan_so, tu_lap, DAP_AN_THANH_PHAN, DAP_AN_VAN_BAN

KET_CUC = {'GIUP': 'GIUP', 'HAI': 'HAI', 'KHONG_TAC_DUNG': 'KHONG_TAC_DUNG', 'KHONG_DU_CA': 'KHONG_DU_CA',
           'TRAI_CHIEU_DATASET': 'TRAI_CHIEU_DATASET', 'TRAI_CHIEU_O': 'TRAI_CHIEU_O'}


def o_chuan():
    """Cấu trúc ô dev (fixture 45, nhan_ban; dinh-nghia-pha2.json#/nguyen_tac/0): RE2-TT 10 ô × 3 ca;
    Nezha-OB 13 ô: 9 ô × 2 ca, 4 ô × 1 ca. Mã ô o1–o10, n1–n13 theo cách viết của fixture."""
    ca = []
    for j in range(1, 11):
        for k in range(3):
            ca.append({'ma': f'r{j}-{k}', 'dataset': 'RE2-TT', 'o': f'o{j}'})
    for j in range(1, 14):
        for k in range(2 if j <= 9 else 1):
            ca.append({'ma': f'z{j}-{k}', 'dataset': 'Nezha-OB', 'o': f'n{j}'})
    return ca


def _ca_tu_fixture(d, rr_mac_dinh=Fraction(1, 2)):
    """Dựng RR từng ca (tắt, bật). Ca không nêu trong fixture không đổi (RR như nhau ở hai nhánh)."""
    ds = o_chuan()
    tat = {c['ma']: rr_mac_dinh for c in ds}
    bat = dict(tat)
    if 'thay_doi' in d:
        for dsn, v in d['thay_doi'].items():
            for c in ds:
                if c['dataset'] == dsn:
                    tat[c['ma']], bat[c['ma']] = phan_so(v['moi_ca'][0]), phan_so(v['moi_ca'][1])
    for dsn, o, a, b in d.get('ca_doi', []):
        c = next(c for c in ds if c['dataset'] == dsn and c['o'] == o)
        tat[c['ma']], bat[c['ma']] = phan_so(a), phan_so(b)
    return ds, tat, bat


def _E_X(d, ds):
    tat_ca_o = sorted({c['o'] for c in ds}, key=lambda o: (o[0], int(o[1:])))
    if d.get('E_X_toan_bo'):
        return set(tat_ca_o)
    if 'E_X' in d:
        return set(d['E_X'])
    n = d['E_X_so_o']
    # Ô nêu trong ca_doi vào E_X trước; thêm ô khác cho đủ số. Đáp án các fixture này không phụ thuộc chọn ô nào
    # (kết cục không phải GIÚP), xem LOG T-044.
    ex = [o for _, o, _, _ in d.get('ca_doi', [])]
    for o in tat_ca_o:
        if len(ex) >= n:
            break
        if o not in ex:
            ex.append(o)
    return set(ex[:n])


@pytest.mark.parametrize('i', [34, 35, 36, 37, 38, 39, 40, 51, 52, 53, 54, 60])
def test_luat_C(i, ma):
    from m1_danh_gia import luat_c
    f = fx(i)
    ma(str(i))
    d, da = f['dau_vao'], f['dap_an']
    ds, tat, bat = _ca_tu_fixture(d)
    them = {}
    if 'M5' in d:
        them['M5'] = tuple(d['M5'])
    if 'moc_gia' in d:
        them['moc_gia'] = (tuple(d['moc_gia']['tat']), tuple(d['moc_gia']['bat']))
    kq = luat_c.ap_dung(ds, tat, bat, _E_X(d, ds), thanh_phan=d.get('thanh_phan', 'X'), **them)
    assert kq['ket_cuc'] == KET_CUC[da['ket_cuc']]
    if 'dMRR_gop' in da:
        assert gan_bang(kq['dMRR']['gop'], da['dMRR_gop'])
    if 'dMRR' in da:
        for k, v in da['dMRR'].items():
            assert gan_bang(kq['dMRR'][k], v), k
    if 'buoc' in da:
        assert kq['buoc'] == da['buoc']
    if 'dieu_kien_E5' in da:
        assert kq['dieu_kien_E5'] == da['dieu_kien_E5']
    if 've_moc_gia' in da:
        assert kq['moc_gia']['ve'] == da['ve_moc_gia']
        assert gan_bang(kq['moc_gia']['tang'], da['tang']) and kq['moc_gia']['n'] == da['n']


def test_45_khoi_tu_kenh(ma):
    from m1 import chuoi
    from m1_danh_gia import rr, chon_khoi, luat_c, m5
    f = fx(45)
    ma('45')
    d, da = f['dau_vao'], f['dap_an']
    canh = [tuple(c) for c in d['canh']]
    cau_hinh = {'R0': {'E1': 'tat', 'E5': False}, 'E1': {'E1': 'U', 'E5': False},
                'E5': {'E1': 'tat', 'E5': True}, 'E1+E5': {'E1': 'U', 'E5': True}}
    rr_th = {}
    blocks_th = {}
    for ten, ch in cau_hinh.items():
        rr_th[ten], blocks_th[ten] = {}, {}
        for th, kenh in d['tinh_huong'].items():
            k = {'F': kenh['F'], 'R': kenh['R_bat_E1' if ch['E1'] != 'tat' else 'R_tat_E1'], 'X': kenh['X']}
            kq = chuoi.xep_tu_kenh_fixture(k, canh, bat_E5=ch['E5'])
            rr_th[ten][th] = rr.rr_ca(kq['blocks'], d['root'])
            blocks_th[ten][th] = kq['blocks']
            assert gan_bang(rr_th[ten][th], da['rr'][ten][th]), (ten, th)
    # Nhân bản: mỗi tình huống 26 ca theo cấu trúc ô của fixture.
    ds = []
    for j in range(1, 11):
        for th in (('A', 'A', 'B') if j <= 5 else ('A', 'B', 'B')):
            ds.append({'ma': f'r{j}-{len(ds)}', 'dataset': 'RE2-TT', 'o': f'o{j}', 'th': th})
    for j in range(1, 10):
        for th in ('A', 'B'):
            ds.append({'ma': f'z{j}-{len(ds)}', 'dataset': 'Nezha-OB', 'o': f'n{j}', 'th': th})
    for j, th in zip(range(10, 14), ('A', 'A', 'B', 'B')):
        ds.append({'ma': f'z{j}-{len(ds)}', 'dataset': 'Nezha-OB', 'o': f'n{j}', 'th': th})
    rr_ca = {ten: {c['ma']: rr_th[ten][c['th']] for c in ds} for ten in cau_hinh}
    mrr = {ten: sum(v.values()) / len(v) for ten, v in rr_ca.items()}
    for ten, v in da['MRR'].items():
        assert gan_bang(mrr[ten], v), ten
    E_X = {c['o'] for c in ds}
    G_N = set(canh)
    m5_dem = {ten: sum(m5.co_M5(blocks_th[ten][c['th']], d['root'], G_N) for c in ds) for ten in cau_hinh}
    cap = {}
    for x, y in (('R0', 'E1'), ('R0', 'E5'), ('E1', 'E1+E5'), ('E5', 'E1+E5'), ('R0', 'E1+E5')):
        tp = 'E5' if (x, y) in (('R0', 'E5'), ('E1', 'E1+E5')) else ('E1' if (x, y) != ('R0', 'E1+E5') else None)
        them = {'M5': (m5_dem[x], m5_dem[y])} if tp == 'E5' else {}
        cap[f'{x}|{y}'] = luat_c.ap_dung(ds, rr_ca[x], rr_ca[y], E_X, thanh_phan=tp or 'R0,c', **them)['ket_cuc']
    kq = chon_khoi.chon(['E1', 'E5'], it_ca=[], do_thi=['E1', 'E5'], MRR=mrr, cap=cap)
    assert kq['chon'] == da['chon']


@pytest.mark.parametrize('i', [46, 47, 49, 50])
def test_chon_khoi(i, ma):
    from m1_danh_gia import chon_khoi
    f = fx(i)
    ma(str(i))
    d, da = f['dau_vao'], f['dap_an']
    kq = chon_khoi.chon(d['thanh_phan'], it_ca=d['it_ca'], do_thi=d['do_thi'],
                        MRR={k: phan_so(v) for k, v in d['MRR'].items()}, cap=d['cap'])
    assert kq['chon'] == da['chon']
    if 'co_dinh' in da:
        assert sorted(kq['co_dinh']) == da['co_dinh']
    if 'loai_luot_hai' in da:
        assert sorted(kq['loai_luot_hai']) == da['loai_luot_hai']
    if 'trinh_Minh' in da:
        assert kq['trinh_Minh'] == da['trinh_Minh']
        assert kq['cau_hinh_do_thi_tot_nhat'] == da['cau_hinh_do_thi_tot_nhat']
        assert gan_bang(kq['chenh'], da['chenh'])


def test_48_boi_canh(ma):
    from m1_danh_gia import luat_c, boi_canh
    f = fx(48)
    ma('48')
    d, da = f['dau_vao'], f['dap_an']
    t = d['chuoi_cuoi_dao_X']
    kc = luat_c.ket_cuc_tu_tong_hop({'dMRR': {'gop': phan_so(t['dMRR_gop']),
                                              **{k: phan_so(v) for k, v in t['dMRR_dataset'].items()}},
                                     'P': t['P'], 'M': t['M'], 'P_phay': 0, 'M_phay': 0, 'so_o_E_X': t['E_X_so_o']})
    assert kc['ket_cuc'] == da['ket_cuc_dao']
    kq = boi_canh.kiem(d['luc_chon']['X'], kc['ket_cuc'])
    assert kq['nhan'] == da['nhan'] and kq['trinh_Minh'] == da['trinh_Minh'] and kq['tu_doi'] == da['tu_doi']


def test_80_bo_danh_gia(ma):
    """Fixture 80, phần bộ đánh giá: root mất kênh nào, còn tự sinh không, hạng trước/sau E5."""
    from m1 import e5, xep_hang
    from m1_danh_gia import dau_vet
    from test_k08_e5_e6_e7_e9 import kenh_tu_fixture
    ca = fx(57)['ca'][0]
    f = fx(80)
    ma('80')
    kenh = kenh_tu_fixture(ca['kenh'])
    canh = [tuple(c) for c in ca['canh']]
    bo = xep_hang.xep(kenh, F_I=e5.phan_loai(kenh, canh, bat=False)['F_I'], thuc_the_co_kenh_OK={'Payment', 'payment_db'})
    p = e5.phan_loai(kenh, canh, bat=True)
    bat = xep_hang.xep(kenh, F_I=p['F_I'], thuc_the_co_kenh_OK={'Payment', 'payment_db'})
    kq = dau_vet.root_E5(kenh, p['F_I'], bo['blocks'], bat['blocks'], f['dau_vao']['root_gia_dinh'])
    assert kq == f['dap_an']['bo_danh_gia']


@pytest.mark.parametrize('muc', ['M5-1', 'M5-2', 'M5-3', 'M5-4'])
def test_M5(muc, ma):
    from m1_danh_gia import m5
    m = tu_lap(DAP_AN_THANH_PHAN, muc)
    ma(muc)
    d = m['dau_vao']
    assert m5.co_M5(d['blocks'], d['root'], {tuple(c) for c in d['G_N']}) == m['dap_an']['M5']


def test_M5_G_N_tu_span(ma):
    """G_N theo codebook §4: cạnh cha–con khác chủ, chỉ khi cả span cha lẫn span con thuộc N."""
    from m1_danh_gia import m5
    m = tu_lap(DAP_AN_THANH_PHAN, 'GN1')
    ma('GN1')
    d = m['dau_vao']
    assert sorted(list(c) for c in m5.G_N_tu_span(d['spans'], d['t'])) == m['dap_an']['G_N']


@pytest.mark.parametrize('muc', ['UV6-1', 'UV6-2'])
def test_UV6(muc, ma):
    from m1_danh_gia import uv6
    m = tu_lap(DAP_AN_THANH_PHAN, muc)
    ma(muc)
    kq = uv6.dem(m['dau_vao']['ca'])
    for k, v in m['dap_an'].items():
        assert kq[k] == v, k


@pytest.mark.parametrize('muc', ['B8-1', 'B8-2', 'B8-3'])
def test_buoc_8(muc, ma):
    from m1_danh_gia import chon_khoi
    m = tu_lap(DAP_AN_THANH_PHAN, muc)
    ma(muc)
    d = m['dau_vao']
    kq = chon_khoi.kiem_cau_hinh_thang(d['thang'], d['thanh_phan'], d['cap'])
    assert sorted(kq['xung_dot']) == sorted(m['dap_an']['xung_dot'])
    assert sorted(kq['trinh_Minh']) == sorted(m['dap_an']['trinh_Minh'])


def test_cap_R0_c(ma):
    """CĐ6.4: cặp (R0, c) nhiều thành phần chỉ áp vế không gắn với thành phần nào; E_X là hợp."""
    from m1_danh_gia import luat_c
    m = tu_lap(DAP_AN_THANH_PHAN, 'R0C1')
    ma('R0C1')
    d = m['dau_vao']
    ds, tat, bat = _ca_tu_fixture(d)
    E_X = set().union(*[set(x) for x in d['E_X_thanh_phan'].values()])
    kq = luat_c.ap_dung(ds, tat, bat, E_X, thanh_phan='R0,c', M5=tuple(d['M5']), uv6=d['uv6'])
    assert kq['ket_cuc'] == m['dap_an']['ket_cuc']
    assert kq['dieu_kien_E5'] == m['dap_an']['dieu_kien_E5']


def test_phu_thuoc_quan_sat(ma):
    """SPEC T-043 Phụ lục C, D2f: kết cục ở ba thế giới; khối K và bước quyết định theo luật C xử lý khác nhau."""
    from m1_danh_gia import luat_c
    m = tu_lap(DAP_AN_THANH_PHAN, 'PTQS1')
    ma('PTQS1')
    for ca in m['dau_vao']['ca']:
        kq = luat_c.ket_hop_the_gioi(ca['ket_cuc'], buoc=ca['buoc'])
        assert kq == ca['dap_an'], ca['buoc']


def test_trong_so_o(ma):
    """CĐ13; SPEC T-045 dòng 88–89: ô o1 lấy 2 lần cho cùng ΔMRR, P, M, kết cục như thêm một ô bản sao o1′ (mã ô
    mới, vào E_X). |E_X| khác nhau một ô nhưng cả hai đều >= 6, nên không đổi bước 4."""
    from m1_danh_gia import luat_c
    ma('TS1')
    dd = {'RE2-TT': Fraction(1, 30), 'Nezha-OB': Fraction(1, 22)}
    for ca_doi in ([['RE2-TT', 'o1', 0.5, 1.0], ['RE2-TT', 'o2', 0.5, 1.0], ['Nezha-OB', 'n1', 1.0, 0.5]],
                   [['RE2-TT', 'o1', 0.5, 0.25], ['RE2-TT', 'o2', 0.5, 0.25], ['RE2-TT', 'o3', 0.5, 0.25],
                    ['Nezha-OB', 'n1', 0.5, 1.0]]):
        d = {'ca_doi': ca_doi, 'E_X_so_o': 8}
        ds, tat, bat = _ca_tu_fixture(d)
        E_X = _E_X(d, ds)
        w = {c['ma']: (2 if c['o'] == 'o1' else 1) for c in ds}
        kq_w = luat_c.ap_dung(ds, tat, bat, E_X, thanh_phan='X', trong_so=w, delta_d_co_dinh=dd)
        ds2, tat2, bat2 = list(ds), dict(tat), dict(bat)
        for c in ds:
            if c['o'] == 'o1':
                c2 = dict(c, ma=c['ma'] + '-x2', o='o1x')
                ds2.append(c2)
                tat2[c2['ma']], bat2[c2['ma']] = tat[c['ma']], bat[c['ma']]
        kq_x2 = luat_c.ap_dung(ds2, tat2, bat2, E_X | {'o1x'}, thanh_phan='X', delta_d_co_dinh=dd)
        assert kq_w['ket_cuc'] == kq_x2['ket_cuc'] and kq_w['buoc'] == kq_x2['buoc']
        assert kq_w['dMRR'] == kq_x2['dMRR']
        assert (kq_w['P'], kq_w['M'], kq_w['P_phay'], kq_w['M_phay']) == \
            (kq_x2['P'], kq_x2['M'], kq_x2['P_phay'], kq_x2['M_phay'])
        assert kq_w['so_o_E_X'] == 8  # |E_X| cố định từ T0, không nhân bội số


def test_trong_so_o_khac_boi_so(ma):
    """Các ca của cùng một ô phải cùng bội số (bội số là của ô)."""
    from m1_danh_gia import luat_c
    ma('TS1-boi-so-o')
    ds = [{'ma': 'a', 'dataset': 'RE2-TT', 'o': 'o1'}, {'ma': 'b', 'dataset': 'RE2-TT', 'o': 'o1'}]
    with pytest.raises(ValueError):
        luat_c.ap_dung(ds, {'a': 1, 'b': 1}, {'a': 1, 'b': 1}, {'o1'}, trong_so={'a': 2, 'b': 1})
    with pytest.raises(ValueError):
        luat_c.ap_dung(ds, {'a': 1, 'b': 1}, {'a': 1, 'b': 1}, {'o1'}, trong_so={'a': Fraction(3, 2), 'b': Fraction(3, 2)})


def test_TS2_luat_c_boi_so(ma):
    from m1_danh_gia import luat_c
    m = tu_lap(DAP_AN_THANH_PHAN, 'TS2')
    ma('TS2')
    d, da = m['dau_vao'], m['dap_an']
    ds = [{'ma': a, 'dataset': b, 'o': c} for a, b, c in d['ca']]
    tat = {c['ma']: phan_so(d['RR_tat']) for c in ds}
    bat = dict(tat, **{k: phan_so(v) for k, v in d['RR_bat'].items()})
    kq = luat_c.ap_dung(ds, tat, bat, set(d['E_X']), thanh_phan='X', trong_so=d['boi_so'],
                        delta_d_co_dinh={k: phan_so(v) for k, v in d['delta_d'].items()})
    assert (kq['M'], kq['P']) == (da['M'], da['P'])
    assert gan_bang(kq['dMRR']['gop'], da['dMRR_gop'])
    assert (kq['ket_cuc'], kq['buoc']) == (da['ket_cuc'], da['buoc'])


def _kq_tu_ca(ca_tat, ca_bat):
    """Cấu trúc kết quả `pha2.cham` tối thiểu cho hai cấu hình T và B (một thế giới lặp ba lần)."""
    def cfg(ca):
        return {'ca': {o: {'dataset': v['dataset'], 'o': v['o'], 'loai_loi': v.get('loai_loi'),
                           'verdict': v.get('verdict'),
                           'theo_the_gioi': {w: {'RR': v.get('RR', Fraction(1, 2)), 'hit1': v.get('hit1', 0),
                                                 'hang': v.get('hang'), 'M5': v.get('M5', False)}
                                             for w in ('P', 'S_lo', 'S_hi')}} for o, v in ca.items()}}
    return {'cau_hinh': {'T': cfg(ca_tat), 'B': cfg(ca_bat)}}


def test_TS3_M5_boi_so(ma):
    from m1_danh_gia import pha2
    m = tu_lap(DAP_AN_THANH_PHAN, 'TS3')
    ma('TS3')
    d, da = m['dau_vao'], m['dap_an']
    tat = {a: {'dataset': b, 'o': o, 'M5': m_t, 'RR': phan_so(d['RR'])} for a, b, o, _, m_t, _ in d['ca']}
    bat = {a: {'dataset': b, 'o': o, 'M5': m_b, 'RR': phan_so(d['RR'])} for a, b, o, _, _, m_b in d['ca']}
    w = {a: k for a, _, _, k, _, _ in d['ca']}
    kq = _kq_tu_ca(tat, bat)
    E_X = {o for _, _, o, _, _, _ in d['ca']}
    cap = pha2.ket_cuc_cap(kq, 'T', 'B', E_X, 'E5', 'khoi_K', trong_so=w)
    cap0 = pha2.ket_cuc_cap(kq, 'T', 'B', E_X, 'E5', 'khoi_K')
    for x in ('P', 'S_lo', 'S_hi'):
        assert cap['theo_the_gioi'][x]['dieu_kien_E5'] == da['dieu_kien_E5']
        assert cap0['theo_the_gioi'][x]['dieu_kien_E5'] == da['dieu_kien_E5_khong_boi_so']
    import m1_danh_gia.luat_c as lc
    goc = lc.ap_dung
    seen = []
    try:
        lc.ap_dung = lambda *a, **k: (seen.append((k.get('M5'), k.get('trong_so'))), goc(*a, **k))[1]
        pha2.ket_cuc_cap(kq, 'T', 'B', E_X, 'E5', 'khoi_K', trong_so=w)
        pha2.ket_cuc_cap(kq, 'T', 'B', E_X, 'E5', 'khoi_K')
    finally:
        lc.ap_dung = goc
    assert [list(x[0]) for x in seen] == [da['M5']] * 3 + [da['M5_khong_boi_so']] * 3


def test_TS4_uv6_boi_so(ma):
    from m1_danh_gia import uv6
    m = tu_lap(DAP_AN_THANH_PHAN, 'TS4')
    ma('TS4')
    kq = uv6.dem(m['dau_vao']['ca'])
    assert {k: kq[k] for k in ('hong', 'sua', 'vi_pham')} == m['dap_an']
    kq1 = uv6.dem([dict(c, trong_so=1) for c in m['dau_vao']['ca']])
    assert kq1['vi_pham'] is False


def test_TS4_uv6_qua_pha2(ma):
    """Cặp E3 qua pha2.ket_cuc_cap: bội số của ca đến được UV-6."""
    from m1_danh_gia import pha2
    m = tu_lap(DAP_AN_THANH_PHAN, 'TS4')
    ma('TS4-pha2')
    ca = m['dau_vao']['ca']
    tat = {f'c{i}': {'dataset': c['dataset'], 'o': f'o{i}', 'loai_loi': c['loai_loi'], 'hit1': c['hit1_tat'],
                     'hang': c['hang_tat']} for i, c in enumerate(ca)}
    bat = {f'c{i}': {'dataset': c['dataset'], 'o': f'o{i}', 'loai_loi': c['loai_loi'], 'hit1': c['hit1_bat'],
                     'hang': c['hang_bat']} for i, c in enumerate(ca)}
    w = {f'c{i}': c['trong_so'] for i, c in enumerate(ca)}
    cap = pha2.ket_cuc_cap(_kq_tu_ca(tat, bat), 'T', 'B', {'o0', 'o1'}, 'E3', 'khoi_K', trong_so=w)
    assert cap['theo_the_gioi']['P']['UV6'] == ('HAI' if m['dap_an']['vi_pham'] else 'KHONG_HAI')
    cap0 = pha2.ket_cuc_cap(_kq_tu_ca(tat, bat), 'T', 'B', {'o0', 'o1'}, 'E3', 'khoi_K')
    assert cap0['theo_the_gioi']['P']['UV6'] == 'KHONG_HAI'


def test_TS5_moc_gia_boi_so(ma):
    from m1_danh_gia import pha2
    m = tu_lap(DAP_AN_THANH_PHAN, 'TS5')
    ma('TS5')
    d, da = m['dau_vao'], m['dap_an']
    tat = {a: {'dataset': 'RE2-TT', 'o': 'o' + a, 'verdict': vt} for a, _, vt, _ in d['ca']}
    bat = {a: {'dataset': 'RE2-TT', 'o': 'o' + a, 'verdict': vb} for a, _, _, vb in d['ca']}
    t, b, phu = pha2.dem_moc_gia(_kq_tu_ca(tat, bat), 'T', 'B', trong_so={a: k for a, k, _, _ in d['ca']})
    assert list(t) == da['tat'] and list(b) == da['bat'] and phu['bi_loai'] == da['bi_loai']


def test_pha2_giai_thich_WD(ma, tmp_path):
    """pha2.cham ghi `nguyen_nhan_WD` từ `extra.kenh_co_the_gioi` của bản ghi khi ca WORLD_DEPENDENT (WD1)."""
    import hashlib
    import json
    from m1_danh_gia import pha2
    m = tu_lap(DAP_AN_THANH_PHAN, 'WD1')
    ma('WD1-pha2')
    d, da = m['dau_vao'], m['dap_an']
    b = lambda xs: [{'key': [len(xs) - i], 'groups': [[e]]} for i, e in enumerate(xs)]
    kenh = [{'thuc_the': e, 'ten': 'k' + e, 'huong': 'len', 'lop': 'lan_nguoc', 's': 1.0, 'F_I': 1} for e in d['P']]
    rec = {'config_id': 'C', 'opaque_id': 'x', 'status': 'OK', 'verdict': 'CAUSE_FOUND', 'blocks': b(d['P']),
           'worlds': {w: {'blocks': b(d[w])} for w in ('S_lo', 'S_hi')},
           'extra': {'G_N': [], 'kenh_co_the_gioi': {w: kenh for w in ('P', 'S_lo', 'S_hi')}}}
    du_lieu = (json.dumps(rec, sort_keys=True) + '\n').encode('utf-8')
    (tmp_path / 'ban-ghi.jsonl').write_bytes(du_lieu)
    h = hashlib.sha256(du_lieu).hexdigest()
    (tmp_path / 'pha1.json').write_text(json.dumps({'tep': 'ban-ghi.jsonl', 'sha256': h, 'so_ban_ghi': 1}),
                                        encoding='utf-8')
    kq = pha2.cham(tmp_path, h, {'x': {'root': d['root'], 'dataset': 'RE2-TT', 'o': 'o1'}})
    c = kq['cau_hinh']['C']['ca']['x']
    assert c['WORLD_DEPENDENT'] is True
    nn = c['nguyen_nhan_WD']
    assert nn['loai'] == da['loai'] and [list(x) for x in nn['cap']] == da['cap']
    assert {w: {'vuot': v['vuot'], 'bi_vuot': v['bi_vuot']} for w, v in nn['theo_the_gioi'].items()} == \
        da['theo_the_gioi']


def test_D17_van_ban(ma):
    """Đ17 (dinh-chinh-phien10.md dòng 81): một ca 5 → 1, hai ca 9 → 10; người làm bổ sung dataset, ô, |E_X|."""
    from m1_danh_gia import luat_c
    m = tu_lap(DAP_AN_VAN_BAN, 'VB-D17')
    ma('VB-D17')
    d = m['dau_vao']
    ds, tat, bat = _ca_tu_fixture({'ca_doi': d['ca_doi']})
    kq = luat_c.ap_dung(ds, tat, bat, set(d['E_X']), thanh_phan='X')
    assert (kq['P'], kq['M']) == tuple(m['dap_an']['P_M'])
    assert gan_bang(kq['dMRR']['gop'], m['dap_an']['dMRR_gop'])
    assert kq['ket_cuc'] == m['dap_an']['ket_cuc']
