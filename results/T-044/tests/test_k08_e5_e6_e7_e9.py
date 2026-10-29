"""Khối 8: E5 (8, 57, 58, 71, 80; nhóm vòng CĐ3), E6a/E6b (14–16, 69; Đ10, đặc tả v1 dòng 349),
E7 (70; CĐ8), E9 (B2–B5; CĐ9), cạnh tĩnh (58)."""
import pytest

from conftest import fx, bx, gan_bang, tu_lap, DAP_AN_THANH_PHAN, DAP_AN_VAN_BAN

LOP = {'lan_nguoc': 'lan_nguoc', 'tai_nguyen_tang': 'khong_lan', 'khong_lan': 'khong_lan', 'lan_xuoi': 'lan_xuoi'}


def kenh_tu_fixture(kenh_dict):
    """Kênh của fixture chuỗi: [tên, lớp, điểm]; mọi kênh có F_raw = 1, hướng lên (lớp lan xuôi: hướng xuống)."""
    from m1.kieu import Kenh
    out = []
    for e, ds in kenh_dict.items():
        for ten, lop, s in ds:
            l = LOP[lop]
            out.append(Kenh(e, ten, 'xuong' if l == 'lan_xuoi' else 'len', l, s))
    return out


def _chay_E5(ca, **kw):
    from m1 import e5, xep_hang
    kenh = kenh_tu_fixture(ca['kenh'])
    canh = [tuple(c) for c in ca['canh']]
    p = e5.phan_loai(kenh, canh, bat=ca.get('E5', True), **kw)
    xh = xep_hang.xep(kenh, F_I=p['F_I'], thuc_the_co_kenh_OK={k.thuc_the for k in kenh})
    return p, xh


@pytest.mark.parametrize('ma_ca', ['8a', '8b'])
def test_8_scc(ma_ca, ma):
    ca = next(c for c in fx(8)['ca'] if c['ma'] == ma_ca)
    ma(f'8-{ma_ca}')
    p, xh = _chay_E5(ca)
    da = ca['dap_an']
    assert xh['thu_tu'] == da['thu_tu']
    assert {e: list(v) for e, v in xh['K_I'].items()} == da['K_I']
    assert sorted([list(x) for x in p['ke_thua']]) == sorted(da['ke_thua'])


@pytest.mark.parametrize('i', [57, 71])
def test_chuoi_kenh(i, ma):
    ca = fx(i)['ca'][0]
    ma(f'{i}-{ca["ma"]}')
    p, xh = _chay_E5(ca)
    da = ca['dap_an']
    assert xh['thu_tu'] == da['thu_tu']
    assert {e: list(v) for e, v in xh['K_I'].items()} == da['K_I']
    assert xh['tang'] == da['tang']
    if 'ke_thua' in da:
        assert sorted([list(x) for x in p['ke_thua']]) == sorted(da['ke_thua'])


def test_58_d19(ma):
    ca = fx(58)['ca'][0]
    ma('58-58')
    p, xh = _chay_E5(ca)
    assert xh['thu_tu'] == ca['dap_an']['thu_tu']
    assert {e: list(v) for e, v in xh['K_I'].items()} == ca['dap_an']['K_I']


def test_58_phuong_an_khong_dung(ma):
    """Phương án không dùng của D19: nhóm vòng xét trên toàn đồ thị."""
    ca = fx(58)['ca'][0]
    ma('58-58-pa')
    p, xh = _chay_E5(ca, pham_vi_nhom_vong='toan_do_thi')
    assert xh['thu_tu'] == ca['dap_an']['phuong_an_khong_dung']['thu_tu']


def test_80_dau_vet_phuong_phap(ma):
    """Phần phương pháp của fixture 80: inherited_by trên dữ liệu fixture 57."""
    ca = fx(57)['ca'][0]
    f = fx(80)
    ma('80-phuong-phap')
    p, xh = _chay_E5(ca)
    ib = sorted([[x['thuc_the'], x['kenh'], x['giai_thich'][0], x['giai_thich'][1], list(x['duong']), x['quy_tac'],
                  x['trang_thai']] for x in p['inherited_by']])
    assert ib == sorted(f['dap_an']['inherited_by'])
    assert list(xh['K_I']['Payment']) == f['dap_an']['K_I_Payment']


@pytest.mark.parametrize('muc', ['SCC1', 'SCC2', 'SCC3', 'SCC4'])
@pytest.mark.parametrize('doc', ['co_vong', 'ke_canh'])
def test_nhom_vong_tu_lap(muc, doc, ma):
    """CĐ3: vòng 3 nút như RE2-TT; cách đọc chính (C′) và cách đọc chẩn đoán (A)."""
    m = tu_lap(DAP_AN_THANH_PHAN, muc)
    ma(f'{muc}-{doc}')
    ca = dict(m['dau_vao'], E5=True)
    p, xh = _chay_E5(ca, doc_nhom_vong=doc)
    da = m['dap_an'][doc]
    assert sorted([list(x) for x in p['ke_thua']]) == sorted(da['ke_thua'])
    assert xh['thu_tu'] == da['thu_tu']


def test_E5_tat_van_de_xuat(ma):
    """E5 tắt: F_I = F_raw; giải thích vẫn ghi với trạng thái 'de_xuat' (hop-dong.json dòng 26; CĐ8)."""
    ca = fx(57)['ca'][0]
    ma('E5-tat')
    p, xh = _chay_E5(dict(ca, E5=False))
    assert not p['ke_thua']
    assert {x['trang_thai'] for x in p['inherited_by']} == {'de_xuat'}
    assert xh['thu_tu'] == ['Payment', 'payment_db']


# ---- E6a / E6b ----

def _thuc_the_6(d):
    from m1.kieu import Kenh
    kenh, F_I = [], {}
    for e, v in d['thuc_the'].items():
        ki, kr = v['K_I'], v['K_raw']
        if kr[1] > 0:
            # Dựng kênh khớp K_raw (số kênh, max, tổng); kênh có F_I theo K_I.
            for j in range(int(kr[1])):
                s = kr[0] if j == 0 else (kr[2] - kr[0]) / (kr[1] - 1)
                k = Kenh(e, f'c{j}', 'len', 'lan_nguoc', s)
                kenh.append(k)
                F_I[k.ma] = 1 if j < ki[1] else 0
    ok = {e for e, v in d['thuc_the'].items() if v['K_raw'][1] > 0 or v.get('co_kenh_OK')}
    return kenh, F_I, ok


@pytest.mark.parametrize('i', [14, 15, 16, 69])
def test_E6b(i, ma):
    from m1 import xep_hang
    f = fx(i)
    ma(str(i))
    d, da = f['dau_vao'], f['dap_an']
    kenh, F_I, ok = _thuc_the_6(d)
    xh = xep_hang.xep(kenh, F_I=F_I, thuc_the_co_kenh_OK=ok, che_do='E6b', canh=[tuple(c) for c in d['canh']])
    if 'trang_thai' in da:
        assert xh['trang_thai_E6b'] == da['trang_thai']
    if 'thu_tu' in da:
        assert xh['thu_tu'] == da['thu_tu']
    if 'pi' in da:
        for e, v in da['pi'].items():
            assert gan_bang(xh['pi'].get(e, 0.0), v), e
    if 'tap_PageRank' in da:
        assert sorted(xh['tap_PageRank']) == da['tap_PageRank']
        assert xh['thu_tu'] == da['danh_sach']


@pytest.mark.parametrize('muc', ['VB-D10a', 'VB-D10b', 'VB-349'])
def test_E6b_van_ban(muc, ma):
    """Đáp án trong văn bản: Đ10 (dinh-chinh-phien9.md dòng 74–76), đặc tả v1 dòng 349."""
    from m1 import xep_hang
    from m1.kieu import Kenh
    m = tu_lap(DAP_AN_VAN_BAN, muc)
    ma(muc)
    d = m['dau_vao']
    kenh = [Kenh(e, 'c', 'len', 'khong_lan', s) for e, s in d['diem'].items()]
    for truong_hop, canh in d['canh'].items():
        xh = xep_hang.xep(kenh, thuc_the_co_kenh_OK=set(d['diem']), che_do='E6b', canh=[tuple(c) for c in canh])
        da = m['dap_an'][truong_hop]
        if 'pi' in da:
            for e, v in da['pi'].items():
                assert abs(xh['pi'][e] - v) <= da.get('sai_so', 5e-5), (truong_hop, e)
        if 'hang_root' in da:
            assert xh['thu_tu'].index(d['root']) + 1 == da['hang_root'], truong_hop


# ---- E7 ----

def test_70_E7c(ma):
    from m1_danh_gia import e7 as e7_dg
    f = fx(70)
    ma('70')
    d, da = f['dau_vao'], f['dap_an']
    kq = e7_dg.mo_ta(d['T'], {k: set(v) for k, v in d['R_r'].items()}, d['root'])
    assert gan_bang(kq['p'], da['p']) and gan_bang(kq['R_ky_vong'], da['R_ky_vong'])
    assert sorted(kq['hop']) == da['hop'] and kq['co_hop'] == da['co_hop']


@pytest.mark.parametrize('muc', ['E7-1', 'E7-2', 'E7-3'])
def test_E7_dung_vung(muc, ma):
    from m1 import e5, e7
    m = tu_lap(DAP_AN_THANH_PHAN, muc)
    ma(muc)
    d = m['dau_vao']
    kenh = kenh_tu_fixture(d['kenh'])
    canh = [tuple(c) for c in d['canh']]
    p = e5.phan_loai(kenh, canh, bat=d['E5'])
    for cach in ('1', '2'):
        R = e7.vung(d['T'], kenh, canh, p['inherited_by'], cach=int(cach))
        assert {r: sorted(v) for r, v in R.items()} == m['dap_an'][cach], cach


# ---- E9 ----

@pytest.mark.parametrize('ma_b', ['B2', 'B3', 'B4', 'B5'])
def test_E9_phu_quyet(ma_b, ma):
    from m1 import e9
    f = bx(ma_b)
    ma(ma_b)
    d = f['dau_vao']
    pq, ly_do = e9.phu_quyet(d['e']['khoi_phat'], [b['khoi_phat'] for b in d['B']], o_s=10, tau=0.001)
    assert pq == f['dap_an']['phu_quyet']
    assert ly_do == {'không đủ khởi phát': 'khong_du_khoi_phat', 'đã xét, phủ quyết': 'da_xet_phu_quyet',
                     'đã xét, không phủ quyết': 'da_xet_khong_phu_quyet'}[f['dap_an']['ly_do']]


@pytest.mark.parametrize('muc', ['KP1', 'KP2', 'KP3'])
def test_E9_khoi_phat(muc, ma):
    """CĐ9: khởi phát là đầu ô 10 giây đầu tiên trong A có tỷ lệ vượt ngưỡng lớn hơn r_d(N)."""
    from m1 import e9
    m = tu_lap(DAP_AN_THANH_PHAN, muc)
    ma(muc)
    d = m['dau_vao']
    kp = e9.khoi_phat(d['moc_A'], d['gia_tri_A'], nguong=d['nguong'], r_N=d['r_N'], t=d['t'], huong=d['huong'], o_s=10)
    assert kp == m['dap_an']['khoi_phat']


def test_E9_tat_tren_canh_E2(ma):
    """CĐ9: khi E2 bật, cạnh dùng để giải thích có E2 bất thường thì E9 không phủ quyết."""
    from m1 import e5
    from m1.kieu import Kenh
    m = tu_lap(DAP_AN_THANH_PHAN, 'E9E2')
    ma('E9E2')
    d = m['dau_vao']
    kenh = [Kenh(k[0], k[1], k[2], k[3], k[4], khoi_phat=k[5]) for k in d['kenh']]
    for nhanh in ('E2_bat', 'E2_tat'):
        canh_E2 = {tuple(c) for c in d['canh_E2_bat_thuong']} if nhanh == 'E2_bat' else set()
        p = e5.phan_loai(kenh, [tuple(c) for c in d['canh']], bat=True,
                         e9={'bat': True, 'o_s': 10, 'tau': 0.001, 'canh_E2_bat_thuong': canh_E2})
        assert sorted([list(x) for x in p['ke_thua']]) == sorted(m['dap_an'][nhanh]['ke_thua']), nhanh


@pytest.mark.parametrize('muc', ['SCC1', 'SCC2', 'SCC3', 'SCC4'])
def test_nhom_vong_mac_dinh_la_C_phay(muc, ma):
    """CĐ5: không truyền cách đọc thì dùng C′ ('co_vong'), cả ở e5.phan_loai lẫn ở chuỗi khi thiếu tham_so_E5."""
    from m1 import chuoi
    m = tu_lap(DAP_AN_THANH_PHAN, muc)
    ma(f'{muc}-mac-dinh')
    ca = dict(m['dau_vao'], E5=True)
    p, xh = _chay_E5(ca)
    da = m['dap_an']['co_vong']
    assert sorted([list(x) for x in p['ke_thua']]) == sorted(da['ke_thua'])
    assert xh['thu_tu'] == da['thu_tu']
    kenh = kenh_tu_fixture(ca['kenh'])
    kq = chuoi.xep_tu_kenh_fixture(ca['kenh'], [tuple(c) for c in ca['canh']], bat_E5=True)
    assert kq['thu_tu'] == da['thu_tu'] and kenh


def test_chuoi_thieu_tham_so_E5_dung_C_phay(ma, monkeypatch):
    """Chuỗi: thiếu tham_so_E5 thì gọi E5 với cách đọc C′ ('co_vong'); có thì truyền đúng giá trị (CĐ5)."""
    from m1 import chuoi, e5
    import sinh_trace_S
    from conftest import FIXTURE
    ma('E5-mac-dinh-chuoi')
    spans, logs = sinh_trace_S.sinh('S3', t=1000, mau=FIXTURE['trace_mau_S'])
    p1 = sinh_trace_S.params({'E1': 'U', 'E2': 'VC', 'E3b': True, 'E5': True})
    p0 = {k: v for k, v in p1.items() if k != 'tham_so_E5'}
    pA = dict(p1, tham_so_E5={'doc_nhom_vong': 'ke_canh'})
    goc, nhan = e5.phan_loai, []

    def ghi(*a, **kw):
        nhan.append(kw.get('doc_nhom_vong'))
        return goc(*a, **kw)
    monkeypatch.setattr(e5, 'phan_loai', ghi)
    for p, mong in ((p0, 'co_vong'), (p1, 'co_vong'), (pA, 'ke_canh')):
        nhan.clear()
        rec = chuoi.chay(spans, [], logs, ['A', 'B', 'F', 'I', 'R', 'X'], {}, 1000, p)
        assert rec['error'] is None and nhan and set(nhan) == {mong}
