"""Khối 9: verdict (31, 42, 82), chuỗi S1–S7 (fixture 1) ở mức kênh, và đầu-cuối từ span (CĐ14)."""
from fractions import Fraction

import pytest

from conftest import fx, mau, FIXTURE

TS = {'m_span': 20, 'm_metric': 5, 'alpha': 0.01, 'epsilon': 0.05, 'q_hi': 0.95, 'q_lo': 0.05,
      'n_exact_max': 100, 'count_min': 10}

# fixture-dac-ta.json#/cau_hinh_S: C0 là C-a0; C1–C5 bật dần.
CAU_HINH_S = {
    'C0': {'E1': 'tat', 'E2': 'tat', 'E3': False, 'E3b': False, 'E5': False, 'E6': 'a'},
    'C1': {'E1': 'U', 'E2': 'tat', 'E3': False, 'E3b': False, 'E5': False, 'E6': 'a'},
    'C2': {'E1': 'U', 'E2': 'C', 'E3': False, 'E3b': False, 'E5': False, 'E6': 'a'},
    'C3': {'E1': 'U', 'E2': 'VC', 'E3': False, 'E3b': False, 'E5': False, 'E6': 'a'},
    'C4': {'E1': 'U', 'E2': 'VC', 'E3': False, 'E3b': False, 'E5': True, 'E6': 'a'},
    'C5': {'E1': 'U', 'E2': 'VC', 'E3': False, 'E3b': True, 'E5': True, 'E6': 'a'},
}
S_CA = [c['ma'] for c in fx(1)['ca']]


def _don_vi_co(dv):
    """Đơn vị có thay đổi của fixture 1 (giá trị 1: đổi cả 20 mẫu A, e = 1, qua cổng)."""
    out = []
    for e, op, v in dv['op_full']:
        out.append({'nhom': 'op_full', 'thuc_the': e, 'ten': op, 's': float(v)})
    for e, op, v in dv['op_excl']:
        out.append({'nhom': 'op_excl', 'thuc_the': e, 'ten': op, 's': float(v)})
    for a, b, v in dv['edge']:
        out.append({'nhom': 'canh', 'ben_goi': a, 'ben_duoc_goi': b, 's': float(v)})
    for e, v in dv['log']:
        out.append({'nhom': 'log_loi', 'thuc_the': e, 's': float(v)})
    for e, op, kieu, v in dv['freq']:
        out.append({'nhom': 'tan_suat', 'thuc_the': e, 'ten': op, 'kieu': kieu, 's': float(v)})
    return out


@pytest.mark.parametrize('ma_s', S_CA)
def test_1_chuoi_S_muc_kenh(ma_s, ma):
    from m1 import chuoi
    from m1_danh_gia import rr
    ca = next(c for c in fx(1)['ca'] if c['ma'] == ma_s)
    ma(f'1-{ma_s}')
    for ten_ch, ch in CAU_HINH_S.items():
        kq = chuoi.xep_tu_don_vi(_don_vi_co(ca['don_vi']), [tuple(c) for c in ca['canh']], set(ca['quan_sat']), ch)
        da = ca['dap_an'][ten_ch]
        assert sorted(kq['blocks'][0]['groups'][0]) == da['dau'], ten_ch
        r = rr.rr_ca(kq['blocks'], ca['root']) if ca['root'] in ca['quan_sat'] else Fraction(0)
        assert abs(float(r) - da['rr']) <= 1e-12, ten_ch


def test_31_low_support(ma):
    from m1 import xep_hang, e7, e5
    from m1.kieu import Kenh
    f = fx(31)
    ma('31')
    kenh = [Kenh(e, 'k', 'len', 'lan_nguoc', s, F_raw=0, trang_thai=tt, hop_le=False) for e, tt, s in f['dau_vao']['kenh']]
    xh = xep_hang.xep(kenh, thuc_the_co_kenh_OK=set())
    assert xep_hang.verdict(xh['tang'], so_cham_hop_le=sum(k.hop_le for k in kenh)) == f['dap_an']['verdict']
    p = e5.phan_loai(kenh, [], bat=True)
    for cach, ten in ((1, 'duong_lan'), (2, 'lien_thong')):
        R = e7.vung(xh['T'], kenh, [], p['inherited_by'], cach=cach)
        assert (sorted(set().union(*R.values())) if R else []) == f['dap_an']['vung_E7'][ten]


def test_42_metric_bang_nhau(ma):
    from m1 import e4, xep_hang
    from m1.kieu import Kenh
    f = fx(42)
    ma('42')
    d, da = f['dau_vao'], f['dap_an']
    kq = e4.cham_phan_vi(mau(d['N']), mau(d['A']), TS['m_metric'], TS, huong_cham=('len',))
    assert abs(kq['p_len'] - da['p']) <= 1e-12 and kq['F_raw_len'] == da['F_raw']
    k = Kenh('M', 'metric', 'len', 'lan_nguoc', 0.0, F_raw=kq['F_raw_len'], hop_le=kq['hop_le'])
    xh = xep_hang.xep([k], thuc_the_co_kenh_OK={'M'})
    assert xep_hang.verdict(xh['tang'], so_cham_hop_le=int(k.hop_le)) == da['verdict_E4']
    z = e4.diem_z(mau(d['N']), mau(d['A']))
    hop_le_z = kq['hop_le'] and z['huu_han']
    assert xep_hang.verdict(xh['tang'], so_cham_hop_le=int(hop_le_z)) == da['verdict_z']
    assert xh['T'] == ['M'] and xh['tang']['M'] == 3
    from m1 import e7, e5
    p = e5.phan_loai([k], [], bat=True)
    for cach, ten in ((1, 'duong_lan'), (2, 'lien_thong')):
        R = e7.vung(xh['T'], [k], [], p['inherited_by'], cach=cach)
        assert (sorted(set().union(*R.values())) if R else []) == da['vung_E7'][ten]


def test_82_verdict(ma):
    from m1 import e4, xep_hang
    from m1.kieu import Kenh
    f = fx(82)
    ma('82-verdict')
    d, da = f['dau_vao'], f['dap_an']
    T_N, T_A = d['T']['P']
    kq = e4.cham_dem(d['n_N'], d['n_A'], T_N, T_A, TS)
    k = Kenh('X', 'dem', 'len', 'lan_nguoc', 0.0, F_raw=kq['F_raw_len'], loai='dem', hop_le=kq['hop_le'])
    xh = xep_hang.xep([k], thuc_the_co_kenh_OK={'X'})
    assert xep_hang.verdict(xh['tang'], so_cham_hop_le=int(k.hop_le)) == da['verdict_E4'] == da['verdict_z']


# ---- Đầu-cuối từ span (CĐ14) ----

@pytest.mark.parametrize('ma_s', S_CA)
def test_1_dau_cuoi_tu_span(ma_s, ma):
    from m1 import chuoi
    from m1_danh_gia import rr
    import sinh_trace_S
    ca = next(c for c in fx(1)['ca'] if c['ma'] == ma_s)
    ma(f'1-{ma_s}-dau-cuoi')
    t = 1000
    spans, logs = sinh_trace_S.sinh(ma_s, t=t, mau=FIXTURE['trace_mau_S'])
    for ten_ch, ch in CAU_HINH_S.items():
        params = sinh_trace_S.params(ch)
        rec = chuoi.chay(spans, [], logs, ['A', 'B', 'F', 'I', 'R', 'X'], {}, t, params)
        assert rec['status'] in ('OK', 'NO_EVIDENCE'), (ten_ch, rec.get('error'))
        blocks = rec['extra']['blocks_P']
        da = ca['dap_an'][ten_ch]
        assert sorted(blocks[0]['groups'][0]) == da['dau'], ten_ch
        r = rr.rr_ca(blocks, ca['root'])
        assert abs(float(r) - da['rr']) <= 1e-12, ten_ch


def test_T4c_qua_chuoi(ma):
    """CĐ7: T4c là thứ tự thứ hai trong cùng bản ghi (S1, C0; đáp án tự lập)."""
    from m1 import chuoi
    import sinh_trace_S
    from conftest import tu_lap, DAP_AN_THANH_PHAN
    m = tu_lap(DAP_AN_THANH_PHAN, 'T4C-S1')
    ma('T4C-S1')
    d, da = m['dau_vao'], m['dap_an']
    spans, logs = sinh_trace_S.sinh(d['S'], t=1000, mau=FIXTURE['trace_mau_S'])
    rec = chuoi.chay(spans, [], logs, ['A', 'B', 'F', 'I', 'R', 'X'], {}, 1000, sinh_trace_S.params(CAU_HINH_S[d['cau_hinh']]))
    t4 = rec['extra']['T4c']
    assert [g for b in t4['blocks'] for g in b['groups']] == da['T4c']
    for e, v in da['m'].items():
        assert abs(t4['m_thuc_the'][e][0] - v) <= 1e-12, e
