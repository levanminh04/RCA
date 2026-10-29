"""Runner (SPEC T-044 bước 5, tiêu chí 7): sinh cấu hình từ ma-tran-thu.json sau khi áp đính chính có hiệu lực;
hai pha tách được; hash pha 1 ổn định."""
import pytest

from conftest import tu_lap, DAP_AN_THANH_PHAN, T043, _doc

MA_TRAN = _doc(T043 / 'ma-tran-thu.json')


def test_dinh_chinh_da_ap(ma):
    """Đ16: bỏ C-h khỏi T13, còn 7 đối chứng."""
    from m1 import runner
    ma('runner-dinh-chinh')
    mt = runner.ap_dinh_chinh(MA_TRAN)
    t13 = next(b for b in mt['buoc'] if b['ma'] == 'T13')
    assert 'C-h' not in t13['so_sanh']
    assert t13['so_sanh'] == ['C-a0', 'C-a1', 'C-d1', 'C-d2', 'C-d3', 'C-c', 'C-g', 'C-e']
    assert [x['ma'] for x in mt['dinh_chinh_da_ap']] == ['Đ16']


def test_dem_cau_hinh(ma):
    from m1 import runner
    m = tu_lap(DAP_AN_THANH_PHAN, 'RUN1')
    ma('RUN1')
    d = m['dau_vao']
    ds = runner.sinh_cau_hinh(runner.ap_dinh_chinh(MA_TRAN), thang=d['thang'], chuoi_cuoi=d['chuoi_cuoi'])
    dem = {b: len(v) for b, v in ds.items()}
    assert dem == m['dap_an']['so_cau_hinh']
    ids = [c['config_id'] for v in ds.values() for c in v]
    assert len(ids) == len(set(ids)) or m['dap_an']['cho_phep_trung'] is True
    k = ds['K']
    assert len({tuple(sorted(c['bat_tat'].items())) for c in k}) == 16


def test_ngan_sach(ma):
    from m1 import runner
    ma('runner-ngan-sach')
    # Cấu hình thắng có E2-C và khác cấu hình đầy đủ: K-b có đủ 2 biến thể (ma-tran-thu.json#/ngan_sach/K_Kb_KB).
    thang = {'E1': 'U', 'E2': 'C', 'E3': True, 'E5': False}
    cuoi = dict(thang, E3b=False, E6='a', E9=False, T12=False)
    ds = runner.sinh_cau_hinh(runner.ap_dinh_chinh(MA_TRAN), thang=thang, chuoi_cuoi=cuoi)
    assert (len(ds['K']) + len(ds['K-b']) + len(ds['KB'])) * 52 == 1144 <= 1300
    # Cấu hình thắng trùng cấu hình đầy đủ: hai biến thể trùng nhau, chỉ còn 1.
    thang2 = {'E1': 'U', 'E2': 'C', 'E3': True, 'E5': True}
    ds2 = runner.sinh_cau_hinh(runner.ap_dinh_chinh(MA_TRAN), thang=thang2, chuoi_cuoi=dict(thang2, E3b=False,
                                                                                              E6='a', E9=False,
                                                                                              T12=False))
    assert len(ds2['K-b']) == 1


def test_hai_pha_hash_on_dinh(ma, tmp_path):
    """Pha 1 không đọc nhãn, ghi bản ghi và hash; chạy lại cho cùng hash. Pha 2 đọc bản ghi đã băm và nhãn."""
    from m1 import runner
    from m1_danh_gia import pha2
    import sinh_trace_S
    from conftest import FIXTURE
    ma('runner-hai-pha')
    spans, logs = sinh_trace_S.sinh('S1', t=1000, mau=FIXTURE['trace_mau_S'])
    ca = [{'opaque_id': 'gia-001', 'dataset': 'RE2-TT', 'spans': spans, 'metrics': [], 'logs': logs,
           'inventory': ['A', 'B', 'F', 'I', 'R', 'X'], 'aliases': {}}]
    moc = {'gia-001': 1000}
    cau_hinh = [{'config_id': 'R0', 'params': sinh_trace_S.params({})},
                {'config_id': 'C1', 'params': sinh_trace_S.params({'E1': 'U'})}]
    h1 = runner.pha1(ca, moc, cau_hinh, tmp_path / 'l1')
    h2 = runner.pha1(ca, moc, cau_hinh, tmp_path / 'l2')
    assert h1['sha256'] == h2['sha256']
    kq = pha2.cham(tmp_path / 'l1', h1['sha256'], nhan={'gia-001': {'root': 'R', 'dataset': 'RE2-TT', 'o': 'o1'}})
    assert abs(kq['cau_hinh']['C1']['MRR']['gop'] - 1.0) <= 1e-12
    with pytest.raises(Exception):
        pha2.cham(tmp_path / 'l1', 'sai-hash', nhan={'gia-001': {'root': 'R', 'dataset': 'RE2-TT', 'o': 'o1'}})


def test_runner_chan_ro_gia_tri(ma, tmp_path):
    """CĐ12: runner từ chối khi mã mờ lọt vào params."""
    from m1 import runner
    import sinh_trace_S
    from conftest import FIXTURE
    ma('runner-ro-gia-tri')
    spans, logs = sinh_trace_S.sinh('S1', t=1000, mau=FIXTURE['trace_mau_S'])
    ca = [{'opaque_id': 'gia-001', 'dataset': 'RE2-TT', 'spans': spans, 'metrics': [], 'logs': logs,
           'inventory': ['A', 'B', 'F', 'I', 'R', 'X'], 'aliases': {}}]
    p = sinh_trace_S.params({})
    p['config_id'] = 'R0-gia-001'
    with pytest.raises(Exception):
        runner.pha1(ca, {'gia-001': 1000}, [{'config_id': 'R0-gia-001', 'params': p}], tmp_path / 'l3')


def test_tham_so_E4_khop_hop_dong(ma):
    """Tham số E4 runner dùng = hop-dong.json#/vao/params/tham_so_E4; ma trận không ghi đè giá trị khác."""
    from m1 import runner
    ma('runner-tham-so-E4')
    hd = _doc(T043 / 'hop-dong.json')
    assert runner.TS_HOP_DONG == hd['vao']['params']['tham_so_E4']
    mt = runner.ap_dinh_chinh(MA_TRAN)
    for k, v in MA_TRAN['co_dinh_moi_buoc']['tham_so_E4'].items():
        assert runner.TS_HOP_DONG[k] == v, k
    ds = runner.sinh_cau_hinh(mt, thang={'E1': 'U', 'E2': 'C', 'E3': True, 'E5': False},
                              chuoi_cuoi=dict(runner.R0, E1='U', E2='C', E3=True))
    assert ds['T1'][0]['tham_so_E4'] == hd['vao']['params']['tham_so_E4']


def test_T13_doi_chung(ma):
    """T13: bỏ từng thành phần đang bật + 7 đối chứng (Đ16); C-e là vế mốc giả, không là cấu hình."""
    from m1 import runner
    m = tu_lap(DAP_AN_THANH_PHAN, 'RUN1')
    ma('runner-T13')
    ds = runner.sinh_cau_hinh(runner.ap_dinh_chinh(MA_TRAN), thang=m['dau_vao']['thang'],
                              chuoi_cuoi=m['dau_vao']['chuoi_cuoi'])
    dc = [c['doi_chung'] for c in ds['T13'] if 'doi_chung' in c]
    assert dc == ['C-a0', 'C-a1', 'C-d1', 'C-d2', 'C-d3', 'C-c', 'C-g']
    assert {c['doi_chung']: c['chay_M1'] for c in ds['T13'] if 'doi_chung' in c} == \
        {'C-a0': True, 'C-a1': True, 'C-d1': False, 'C-d2': False, 'C-d3': False, 'C-c': False, 'C-g': False}
    assert not any('C-e' in c['config_id'] or 'C-h' in c['config_id'] for c in ds['T13'])


def test_pha2_M5_va_luat_C(ma, tmp_path):
    """Pha 2 trên S1: cờ M5 đọc G_N từ bản ghi (R0: A, F đứng trước R và có đường tới R); luật C ba thế giới."""
    from fractions import Fraction
    from m1 import runner
    from m1_danh_gia import pha2
    import sinh_trace_S
    from conftest import FIXTURE
    ma('pha2-M5-luat-C')
    spans, logs = sinh_trace_S.sinh('S1', t=1000, mau=FIXTURE['trace_mau_S'])
    ca = [{'opaque_id': 'gia-001', 'spans': spans, 'metrics': [], 'logs': logs,
           'inventory': ['A', 'B', 'F', 'I', 'R', 'X'], 'aliases': {}}]
    cau_hinh = [{'config_id': 'R0', 'params': sinh_trace_S.params({})},
                {'config_id': 'C1', 'params': sinh_trace_S.params({'E1': 'U'})}]
    h = runner.pha1(ca, {'gia-001': 1000}, cau_hinh, tmp_path / 'l')
    nhan = {'gia-001': {'root': 'R', 'dataset': 'RE2-TT', 'o': 'o1'}}
    kq = pha2.cham(tmp_path / 'l', h['sha256'], nhan)
    r0, c1 = kq['cau_hinh']['R0']['ca']['gia-001'], kq['cau_hinh']['C1']['ca']['gia-001']
    assert r0['theo_the_gioi']['P']['RR'] == Fraction(1, 3) and r0['theo_the_gioi']['P']['M5'] is True
    assert c1['theo_the_gioi']['P']['RR'] == 1 and c1['theo_the_gioi']['P']['M5'] is False
    cap = pha2.ket_cuc_cap(kq, 'R0', 'C1', E_X={'o1'}, thanh_phan='E1', buoc='khoi_K')
    for w in ('P', 'S_lo', 'S_hi'):
        assert cap['theo_the_gioi'][w]['ket_cuc'] == 'KHONG_DU_CA'
        assert cap['theo_the_gioi'][w]['dMRR']['gop'] == Fraction(2, 3)
    assert cap['ket_hop']['phu_thuoc_quan_sat'] is False
    cap5 = pha2.ket_cuc_cap(kq, 'R0', 'C1', E_X={'o1'}, thanh_phan='E5', buoc='khoi_K')
    assert cap5['theo_the_gioi']['P']['dieu_kien_E5'] == 'KHONG_HAI'
