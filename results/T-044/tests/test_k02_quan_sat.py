"""Khối 2: cửa sổ, trạng thái quan sát, đơn vị đếm, ba thế giới.

Fixture 21–24, 28–30, 82; B1, B8 (Đ9, Đ20); H1–H6 (Đ19, chép ở dap-an-u-h.json).
"""
import pytest

from conftest import fx, bx, uh, gan_bang, gan_lam_tron, tu_lap, DAP_AN_THANH_PHAN

TS = {'m_span': 20, 'm_metric': 5, 'alpha': 0.01, 'epsilon': 0.05, 'q_hi': 0.95, 'q_lo': 0.05,
      'n_exact_max': 100, 'count_min': 10}

NHAN = {'tang': 'tang', 'giam': 'giam', 'binh_thuong': 'binh_thuong', 'STOPPED': 'STOPPED', 'NEW_OP': 'NEW_OP'}


def test_21_trang_thai_o(ma):
    from m1 import quan_sat
    f = fx(21)
    ma('21')
    d = f['dau_vao']
    t, r = d['t'], d['r']
    ban_ghi = list(range(d['ban_ghi']['tu'], d['ban_ghi']['den'] + 1, d['ban_ghi']['buoc']))
    kq = quan_sat.tinh_nguon(file_khoang=[tuple(d['F'])], moc_ban_ghi=ban_ghi, r=r,
                             cua_so=(t - 300, t + 300), phia={'N': (t - 300, t), 'A': (t, t + 300)}, o_s=10)
    da = f['dap_an']
    for phia in ('N', 'A'):
        for k in ('OPEN', 'QUAN_SAT_A0', 'XAC_NHAN_THIEU_THU', 'O_BIEN'):
            assert kq['o'][phia][k] == da[phia][k], (phia, k)
    assert kq['T_chac']['N'] == da['T_N_chac']
    assert kq['T_max']['N'] == da['T_N_max']
    assert kq['T_chac']['A'] == da['T_A_chac']


@pytest.mark.parametrize('ma_b', ['B1', 'B8'])
def test_khe_file(ma_b, ma):
    from m1 import quan_sat
    f = bx(ma_b)
    ma(ma_b)
    d = f['dau_vao']
    r = d['r_s']
    khoang = [quan_sat.khoang_file(moc, r) for moc in d['file']]
    moc_tat_ca = sorted(x for moc in d['file'] for x in moc)
    kq = quan_sat.tinh_nguon(file_khoang=khoang, moc_ban_ghi=moc_tat_ca, r=r, cua_so=tuple(d['cua_so']),
                             phia={k: tuple(v) for k, v in d['phia'].items()}, o_s=10)
    da = f['dap_an']
    assert [list(k) for k in kq['khe']] == da['khe']
    assert kq['T_chac'] == da['T_chac']
    assert kq['T_max'] == da['T_max']
    assert kq['thieu_thu'] == da['thieu_thu_s']
    assert {k: list(v) for k, v in kq['the_gioi'].items()} == da['the_gioi']


def _cham(d, the_gioi='P'):
    from m1 import e4
    T_N, T_A = d['T'][the_gioi]
    return e4.cham_dem(d['n_N'], d['n_A'], T_N, T_A, TS)


@pytest.mark.parametrize('i', [22, 23, 24, 82])
def test_dem_mot_the_gioi(i, ma):
    f = fx(i)
    ma(str(i))
    kq = _cham(f['dau_vao'])
    da = f['dap_an']['P']
    assert kq['nhan'] == NHAN[da['nhan']]
    huong = 'xuong' if da['nhan'] in ('giam', 'STOPPED') else 'len'
    e = kq['e_' + huong] if da['nhan'] != 'binh_thuong' else max(kq['e_len'], kq['e_xuong'])
    assert gan_bang(e, da['e'])
    if 'p_toi_da' in da:
        assert kq['p_len'] <= da['p_toi_da']
    if 'p' in da:
        assert gan_lam_tron(kq['p_len'], da['p'])
    if i == 82:
        assert kq['trang_thai'] == 'OK' and kq['hop_le'] == f['dap_an']['hop_le']


def test_28_doi_nhan_hai_lan(ma):
    from m1 import e4
    f = fx(28)
    ma('28')
    d, da = f['dau_vao'], f['dap_an']
    nhan = {}
    for w in ('P', 'S_lo', 'S_hi'):
        kq = _cham(d, w)
        nhan[w] = kq['nhan']
        huong = {'tang': 'len', 'giam': 'xuong'}.get(da[w]['nhan'])
        e = kq['e_' + huong] if huong else max(kq['e_len'], kq['e_xuong'])
        assert kq['nhan'] == da[w]['nhan'], w
        assert gan_bang(e, da[w]['e']), w
    assert e4.obs_dependent(nhan) == da['OBS_DEPENDENT']


def test_29_the_gioi_doi_thu_tu(ma):
    """Fixture 29: phương pháp xuất RANK_CHANGED; bộ đánh giá tính WORLD_DEPENDENT và nguyên nhân."""
    from m1 import e4, xep_hang
    from m1.kieu import Kenh
    from m1_danh_gia import the_gioi
    f = fx(29)
    ma('29')
    d, da = f['dau_vao'], f['dap_an']
    thu_tu, khoi, kenh_w = {}, {}, {}
    for w in ('P', 'S_lo', 'S_hi'):
        T_N, T_A = d['U1']['T'][w]
        kq = e4.cham_dem(d['U1']['n_N'], d['U1']['n_A'], T_N, T_A, TS)
        assert gan_bang(kq['e_len'], da['e_U1'][w]), w
        kenh = [Kenh('A', 'U1', 'len', 'lan_nguoc', kq['e_len'], F_raw=kq['F_raw_len'], loai='dem'),
                Kenh('B', 'U2', 'len', 'lan_nguoc', d['U2']['e'])]
        xh = xep_hang.xep(kenh, thuc_the_co_kenh_OK={'A', 'B'})
        thu_tu[w] = xh['thu_tu']
        khoi[w] = xh['blocks']
        kenh_w[w] = kenh
    assert thu_tu == da['thu_tu']
    assert xep_hang.rank_changed(thu_tu) == da['RANK_CHANGED']
    wd = the_gioi.world_dependent(khoi, d['root'])
    assert wd['WORLD_DEPENDENT'] == da['WORLD_DEPENDENT']
    # da['nguyen_nhan'] = "chỉ điểm đổi (cổng qua ở cả ba thế giới); cặp (U1 của A, U2 của B)", viết thành cấu trúc.
    nn = the_gioi.nguyen_nhan(kenh_w, d['root'], khoi)
    assert nn['loai'] == 'chi_diem_doi' and nn['cap'] == (('A', 'U1'), ('B', 'U2'))
    assert nn['theo_the_gioi'] == {'S_hi': {'vuot': ['B'], 'bi_vuot': [], 'cap': [(('A', 'U1'), ('B', 'U2'))]}}


def test_30_thu_tu_khong_doi(ma):
    from m1 import e4
    f = fx(30)
    ma('30')
    d, da = f['dau_vao'], f['dap_an']
    for w in ('P', 'S_lo', 'S_hi'):
        T_N, T_A = d['T'][w]
        e1 = e4.cham_dem(d['U1']['n_N'], d['U1']['n_A'], T_N, T_A, TS)['e_len']
        e2 = e4.cham_dem(d['U2']['n_N'], d['U2']['n_A'], T_N, T_A, TS)['e_len']
        assert gan_bang(e1, da['e_U1'][w]) and gan_bang(e2, da['e_U2'][w])
        assert (e1 > e2) == da['thu_tu_khong_doi']


# ---- H1–H6 (Đ19) ----

def test_H1_moc_rieng(ma):
    from m1 import quan_sat
    h = uh('H1')['may_doc']
    ma('H1')
    params = {'thoi_gian_nguon': {'S': h['nguon_S']['moc_rieng_ns']}, 'nguon_metric': {'k1': 'S'}}
    tg = quan_sat.thoi_gian_nguon_metric(params, metrics_time_ns=h['nguon_S']['metrics_time'])
    assert tg['S']['trang_thai'] == 'OK'
    assert tg['S']['moc'] == h['nguon_S']['moc_rieng_ns']


def test_H2_thieu_moc_da_kiem(ma):
    from m1 import quan_sat
    ma('H2')
    params = {'thoi_gian_nguon': {}, 'nguon_metric': {'k1': 'S'}, 'phan_hoach_NA_da_kiem': {'S': True}}
    tg = quan_sat.thoi_gian_nguon_metric(params, metrics_time_ns=[1e9, 61e9])
    assert tg['S']['trang_thai'] == 'UNSUPPORTED'
    assert tg['S']['cham_NA'] is True


def test_H3_thieu_moc_chua_kiem(ma):
    from m1 import quan_sat
    ma('H3')
    params = {'thoi_gian_nguon': {}, 'nguon_metric': {'k1': 'S'}}
    tg = quan_sat.thoi_gian_nguon_metric(params, metrics_time_ns=[1e9, 61e9])
    assert tg['S']['trang_thai'] == 'UNSUPPORTED'
    assert tg['S']['cham_NA'] is False


def _ca_nho():
    """Ca giả nhỏ cho H4–H6: hai thực thể, một cạnh, không có lỗi."""
    import random
    rng = random.Random(0)
    spans = []
    t_us = 1000 * 1_000_000
    for i in range(40):
        st = t_us - 290_000_000 + i * 14_000_000
        spans.append({'traceID': f'T{i}', 'spanID': 'a', 'parentSpanID': '', 'owner': 'P', 'operation': 'P.h',
                      'start_us': st, 'duration_us': 10_000 + rng.randrange(100)})
        spans.append({'traceID': f'T{i}', 'spanID': 'b', 'parentSpanID': 'a', 'owner': 'Q', 'operation': 'Q.h',
                      'start_us': st + 100, 'duration_us': 5_000 + rng.randrange(100)})
    return spans


def _params(**them):
    p = {'config_id': 'thu', 'bat_tat': {'E1': 'tat', 'E2': 'tat', 'E3': False, 'E3b': False, 'E5': False,
                                         'E6': 'a', 'E9': False, 'T12': False},
         'the_gioi': ['P', 'S_lo', 'S_hi'], 'nhanh_z': False, 'tham_so_E4': dict(TS),
         'don_vi_thoi_gian': {'spans.start_us': 'us', 'metrics.time': 's', 'logs.timestamp': 's'},
         'coverage': {'trace': {'khoang': [[0, 2000 * 10 ** 9]], 'r_ns': 1000},
                      'log': {'khoang': [], 'r_ns': 10 ** 9}, 'metric': {'khoang': [], 'r_ns': 10 ** 9}},
         'nguon_metric': {}, 'thoi_gian_nguon': {}, 'phan_hoach_NA_da_kiem': {},
         'ho_so_nguon': {'kenh_metric': {'kieu': 'hau_to', 'bang': {'cpu': 'tài nguyên'}},
                         'quy_tac_log': {'kieu': 'tu_khoa', 'tu_khoa': ['ERROR', 'FAIL', 'EXCEPTION']},
                         'nguon_khoi_phat': ['trace', 'metric']},
         'tham_so_E3': {'khop': 'hoan_toan', 'sim_th': 0.4, 'do_sau': 4},
         'tham_so_E5': {'doc_nhom_vong': 'co_vong'}}
    for k, v in them.items():
        if k == 'bat_tat':
            p['bat_tat'].update(v)
        elif v is None:
            p.pop(k, None)
        else:
            p[k] = v
    return p


def test_H4_T12_thieu_canh_tinh(ma):
    from m1 import chuoi
    ma('H4')
    rec = chuoi.chay(_ca_nho(), [], [], ['P', 'Q'], {}, 1000, _params(bat_tat={'T12': True}))
    assert rec['status'] == 'UNSUPPORTED'


def test_H5_T12_canh_rong(ma):
    from m1 import chuoi
    ma('H5')
    r0 = chuoi.chay(_ca_nho(), [], [], ['P', 'Q'], {}, 1000, _params())
    r1 = chuoi.chay(_ca_nho(), [], [], ['P', 'Q'], {}, 1000,
                    _params(bat_tat={'T12': True}, canh_tinh={'revision': 'thu', 'canh': []}))
    assert r1['status'] == r0['status'] and r1['error'] is None
    assert r1['entity_ranking'] == r0['entity_ranking']
    assert r1['diagnostics']['so_canh_tinh'] == 0
    # Ca có bằng chứng và E5 dùng cạnh (S2, cấu hình C4): T12 với cạnh rỗng cho đúng kết quả cạnh quan sát.
    import sinh_trace_S
    from conftest import FIXTURE
    spans, logs = sinh_trace_S.sinh('S2', t=1000, mau=FIXTURE['trace_mau_S'])
    ch = {'E1': 'U', 'E2': 'VC', 'E5': True}
    U = ['A', 'B', 'F', 'I', 'R', 'X']
    s0 = chuoi.chay(spans, [], logs, U, {}, 1000, sinh_trace_S.params(ch))
    p1 = sinh_trace_S.params(dict(ch, T12=True))
    p1['canh_tinh'] = {'revision': 'thu', 'canh': []}
    s1 = chuoi.chay(spans, [], logs, U, {}, 1000, p1)
    assert s0['status'] == s1['status'] == 'OK'
    for k in ('blocks', 'entity_ranking', 'classes', 'inherited_by', 'region', 'verdict'):
        assert s1[k] == s0[k], k
    assert s1['diagnostics']['so_canh_tinh'] == 0


def test_H6_thieu_don_vi_thoi_gian(ma):
    from m1 import chuoi
    ma('H6')
    rec = chuoi.chay(_ca_nho(), [], [], ['P', 'Q'], {}, 1000, _params(don_vi_thoi_gian=None))
    assert rec['status'] == 'ERROR'


def _ca_metric_H(nguon):
    """H1–H3 qua chuỗi: một cột S_cpu, ba dòng metric với metrics.time = [1e9, 61e9, 121e9] ns, t = 60 s."""
    p = _params(**nguon)
    p['don_vi_thoi_gian'] = {'spans.start_us': 'us', 'metrics.time': 'ns', 'logs.timestamp': 's'}
    p['coverage'] = dict(p['coverage'], S={'khoang': [[0, 120 * 10 ** 9]], 'r_ns': 10 ** 9})
    metrics = [{'time': x * 10 ** 9, 'S_cpu': 1.0 + i} for i, x in enumerate((1, 61, 121))]
    from m1 import chuoi
    return chuoi.chay([], metrics, [], ['S'], {}, 60, p)


def test_H1_qua_chuoi(ma):
    ma('H1-chuoi')
    rec = _ca_metric_H({'nguon_metric': {'S_cpu': 'S'}, 'thoi_gian_nguon': {'S': [0, 60 * 10 ** 9, 120 * 10 ** 9]}})
    assert rec['error'] is None
    assert rec['coverage']['S']['trang_thai'] == 'OK'
    assert rec['coverage']['S']['H'] == [0, 121 * 10 ** 9]  # theo mốc riêng, không theo metrics.time


def test_H2_qua_chuoi(ma):
    ma('H2-chuoi')
    rec = _ca_metric_H({'nguon_metric': {'S_cpu': 'S'}, 'thoi_gian_nguon': {}, 'phan_hoach_NA_da_kiem': {'S': True}})
    assert rec['coverage']['S'] == {'trang_thai': 'UNSUPPORTED', 'ly_do': 'khong_co_moc_rieng', 'cham_NA': True}
    assert any(d['ma'] == 'metric|S_cpu' for d in rec['extra']['don_vi_phan_vi'])


def test_H3_qua_chuoi(ma):
    ma('H3-chuoi')
    rec = _ca_metric_H({'nguon_metric': {'S_cpu': 'S'}, 'thoi_gian_nguon': {}, 'phan_hoach_NA_da_kiem': {}})
    assert rec['coverage']['S'] == {'trang_thai': 'UNSUPPORTED', 'ly_do': 'khong_co_moc_rieng', 'cham_NA': False}
    assert not any(d['ma'] == 'metric|S_cpu' for d in rec['extra']['don_vi_phan_vi'])
    assert rec['diagnostics']['nguon_metric_unsupported'] == ['S']


def test_WD1_cap_dao_thu_tu(ma):
    from m1.kieu import Kenh
    from m1_danh_gia import the_gioi
    m = tu_lap(DAP_AN_THANH_PHAN, 'WD1')
    ma('WD1')
    d, da = m['dau_vao'], m['dap_an']
    b = lambda xs: [{'key': [len(xs) - i], 'groups': [[e]]} for i, e in enumerate(xs)]
    k = {w: [Kenh(e, 'k' + e, 'len', 'lan_nguoc', 1.0) for e in d['P']] for w in ('P', 'S_lo', 'S_hi')}
    nn = the_gioi.nguyen_nhan(k, d['root'], {w: b(d[w]) for w in ('P', 'S_lo', 'S_hi')})
    assert nn['loai'] == da['loai'] and [list(x) for x in nn['cap']] == da['cap']
    assert {w: {'vuot': v['vuot'], 'bi_vuot': v['bi_vuot']} for w, v in nn['theo_the_gioi'].items()} == da['theo_the_gioi']
    nn2 = the_gioi.nguyen_nhan(k, d['root'], {w: b(d['P']) for w in ('P', 'S_lo', 'S_hi')})
    assert nn2['cap'] == da['khong_doi']['cap'] and nn2['theo_the_gioi'] == da['khong_doi']['theo_the_gioi']
