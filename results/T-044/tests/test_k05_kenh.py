"""Khối 5: severity, kênh log lỗi theo severity, lớp mẫu Drain (fixture 77–79; U1–U6 của Đ15)."""
import pytest

from conftest import fx, uh, gan_bang, gan_lam_tron, T043, _doc

TS = {'m_span': 20, 'm_metric': 5, 'alpha': 0.01, 'epsilon': 0.05, 'q_hi': 0.95, 'q_lo': 0.05,
      'n_exact_max': 100, 'count_min': 10}
HD = _doc(T043 / 'hop-dong.json')
SEV_NEZHA = {'kieu': 'severity', 'loi': HD['severity']['Nezha-OB']['loi'],
             'khong_loi': HD['severity']['Nezha-OB']['khong_loi']}
TU_KHOA = {'kieu': 'tu_khoa', 'tu_khoa': ['ERROR', 'FAIL', 'EXCEPTION']}
E3 = {'khop': 'hoan_toan', 'sim_th': 0.4, 'do_sau': 4}


def test_77_chuan_hoa_severity(ma):
    from m1 import kenh
    f = fx(77)
    ma('77')
    kq = [kenh.chuan_hoa_severity(v, SEV_NEZHA) for v in f['dau_vao']['gia_tri']]
    assert kq == f['dap_an']


def test_78_A_toan_unknown(ma):
    from m1 import kenh
    f = fx(78)
    ma('78')
    d, da = f['dau_vao'], f['dap_an']
    kq = kenh.don_vi_log_loi(d['N'], d['A'], 300, 300, TS, kieu='severity')
    assert kq['trang_thai'] == da['trang_thai']
    assert kq['cham'] == da['cham']
    assert kenh.so_dong_vao_drain(d['A']) == da['dong_A_vao_Drain']


def test_79_do_phu_khac_nhau(ma):
    from m1 import kenh
    f = fx(79)
    ma('79')
    d, da = f['dau_vao'], f['dap_an']
    kq = kenh.don_vi_log_loi(d['N'], d['A'], d['T'][0], d['T'][1], TS, kieu='severity')
    assert kq['trang_thai'] == da['trang_thai']
    assert gan_bang(kq['e_len'], da['e'])
    assert gan_lam_tron(kq['p_len'], da['p'])
    assert kq['do_phu'] == da['do_phu']
    assert kq['ten_kenh'] == da['ten_kenh']


def _dong(n, thuc_the, noi_dung, lop, moc0):
    return [{'moc': moc0 + i, 'thuc_the': thuc_the, 'noi_dung': noi_dung, 'lop': lop} for i in range(n)]


def _dung_U(ma_u):
    """Dựng dòng log cho đúng một cặp (thực thể, mẫu) theo ô văn bản của U1–U6 (dap-an-u-h.json).
    Mọi dòng cùng nội dung, nên Drain học đúng một mẫu; lớp dòng lấy theo severity (Nezha-OB) hoặc từ khóa (RE2-TT)."""
    m = uh(ma_u)['may_doc']
    msg = 'payment processed for order'
    N, A = [], []
    if ma_u == 'U6':
        # 4 dòng có từ khóa và 6 dòng không, cùng token đầu (cây tiền tố của Drain chia theo token đầu),
        # khác một token: Drain gộp thành một mẫu "request <*> code <NUM>".
        N = [{'moc': i, 'thuc_the': 'X', 'noi_dung': f'request status=ERROR code {i}', 'lop': None} for i in range(4)]
        N += [{'moc': 10 + i, 'thuc_the': 'X', 'noi_dung': f'request status=OK code {i}', 'lop': None} for i in range(6)]
        A = [{'moc': 1000 + i, 'thuc_the': 'X', 'noi_dung': f'request status=OK code {i}', 'lop': None}
             for i in range(10)]
        return N, A, TU_KHOA
    lop_cua = {'ERROR': 'LOI', 'INFO': 'KHONG_LOI', 'UNKNOWN': 'UNKNOWN'}
    if ma_u == 'U5':
        N = _dong(5, 'Y', msg, 'KHONG_LOI', 0)
        A = _dong(m['A']['cua_X_khop_mau'], 'X', msg, 'UNKNOWN', 1000)
        return N, A, SEV_NEZHA
    moc = 0
    for sev, n in m['N'].items():
        N += _dong(n, 'X', msg, lop_cua[sev], moc)
        moc += n
    for sev, n in m['A'].items():
        A += _dong(n, 'X', msg, lop_cua.get(sev, 'UNKNOWN'), 1000 + moc)
        moc += n
    return N, A, SEV_NEZHA


@pytest.mark.parametrize('ma_u', ['U1', 'U2', 'U3', 'U4', 'U5', 'U6'])
def test_U_lop_mau(ma_u, ma):
    from m1 import e3, kenh
    ma(ma_u)
    m = uh(ma_u)['may_doc']
    N, A, quy_tac = _dung_U(ma_u)
    kq = e3.hoc_va_dem(N, A, E3, quy_tac)
    kenh_dv = kenh.don_vi_mau_drain(kq)
    if ma_u == 'U5':
        assert kq['mau_moi'].get('X', 0) == m['A_vao_mau_moi']
        assert not [c for c in kq['cap'] if c[0] == 'X']
        return
    cap = [c for c in kq['cap'] if c[0] == 'X']
    assert len(cap) == 1
    c = kq['cap'][cap[0]]
    assert c['lop'] == m['lop']
    if m.get('kenh') is None:
        assert not [u for u in kenh_dv if u['thuc_the'] == 'X' and u['nhom'] in ('mau_loi', 'mau_thuong')]
        assert (c['n_N'], c['n_A']) == (m['luu_so_dong']['N'], m['luu_so_dong']['A'])
        assert kq['mau_moi'].get('X', 0) == m['A_vao_mau_moi']
        return
    k = m['kenh']
    u = [u for u in kenh_dv if u['thuc_the'] == 'X' and u['nhom'] == ('mau_loi' if m['lop'] == 'loi' else 'mau_thuong')]
    assert len(u) == 1
    assert (u[0]['n_N'], u[0]['n_A']) == (k['n_N'], k['n_A'])
    if 'huong' in k:
        assert u[0]['huong_cham'] == [k['huong']]
    if 'bao_kem' in m:
        assert c['loi_xac_dinh_N'] == m['bao_kem']['loi_xac_dinh_N']
        assert c['loi_xac_dinh_A'] == m['bao_kem']['loi_xac_dinh_A']
