"""Khối 3: tiền xử lý span (fixture 6, 7, 44, 72). Cột span của fixture: traceID, spanID, parentSpanID,
owner, operation, start, duration (fixture 6, lời giải)."""
import pytest

from conftest import fx, gan_bang

COT = ('traceID', 'spanID', 'parentSpanID', 'owner', 'operation', 'start_us', 'duration_us')


def _rows(ds):
    return [dict(zip(COT, r)) for r in ds]


@pytest.mark.parametrize('ma_ca', ['6a', '6b'])
def test_6_bo_lap(ma_ca, ma):
    from m1 import span
    ca = next(c for c in fx(6)['ca'] if c['ma'] == ma_ca)
    ma(f'6-{ma_ca}')
    kq = span.tien_xu_ly(_rows(ca['spans']))
    da = ca['dap_an']
    assert kq['bo_lap'] == da['bo_lap']
    assert kq['loi'] == da['loi']
    assert kq['con_lai'] == da['con_lai']


def test_7_mo_coi(ma):
    from m1 import span
    ca = fx(7)['ca'][0]
    ma('7-7')
    kq = span.tien_xu_ly(_rows(ca['spans']))
    da = ca['dap_an']
    for k in ('bo_lap', 'loi', 'con_lai', 'mo_coi', 'goc'):
        assert kq[k] == da[k], k


def test_44_span_qua_moc(ma):
    """Quan hệ dựng trên toàn miền; tính đặc trưng rồi mới chia theo end (đơn vị ms)."""
    from m1 import span
    f = fx(44)
    ma('44')
    d, da = f['dau_vao'], f['dap_an']
    (c0, c1), = d['con']
    rows = [{'traceID': 'T', 'spanID': 'p', 'parentSpanID': '', 'owner': 'P', 'operation': 'P.op',
             'start_us': d['cha'][0], 'duration_us': d['cha'][1] - d['cha'][0]},
            {'traceID': 'T', 'spanID': 'c', 'parentSpanID': 'p', 'owner': 'P', 'operation': 'P.con',
             'start_us': c0, 'duration_us': c1 - c0}]
    prep = span.chuan_bi(rows, t=d['t'], tau=1)
    p = prep['spans'][('T', 'p')]
    c = prep['spans'][('T', 'c')]
    assert gan_bang(p['u'], da['U'])
    assert p['phia'] == da['cha_thuoc']
    assert c['phia'] == da['con_thuoc']


def test_72_span_boc(ma):
    from m1 import span
    f = fx(72)
    ma('72')
    d, da = f['dau_vao'], f['dap_an']
    prep = span.chuan_bi(_rows(d['spans']), t=1000, tau=1)
    w = prep['spans'][('T1', 'w')]
    assert w['boc'] is True and da['w_la_span_boc'] is True
    tat = span.mau_thao_tac(prep, 'tat')
    assert [list(k) for k in sorted(tat) if k == ('A', 'A.callR')] == da['E1_tat']['mau_thao_tac']
    bat = span.mau_thao_tac(prep, 'U')
    assert (('A', 'A.callR') in bat) == da['E1_bat']['w_la_mau_thao_tac']
    canh = span.mau_canh(prep)
    gs = [[a, b, v] for (a, b), m in sorted(canh.items()) for v in m['N'] + m['A']]
    assert gs == da['E1_bat']['g_cua_canh']
