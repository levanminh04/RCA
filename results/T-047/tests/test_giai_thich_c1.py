"""Ca giả tính tay và thay thứ tự có ý nghĩa; không chạm dữ liệu/nhãn thật."""
import copy
import giai_thich_lech_c1 as audit
from m1 import chuoi, cong, e4


def test_delta_giu_truong_co_mat_va_list_khong_cat():
    a = {'x': {'p': .1, 'gone': None}, 'all': [1, 2, 3]}
    b = {'x': {'p': .2, 'new': None}, 'all': [1, 4, 3]}
    rows = {x['pointer']: x for x in audit.delta_fields(a, b)}
    assert set(rows) == {'/x/p', '/x/gone', '/x/new', '/all/1'}
    assert rows['/x/gone']['before_present'] and not rows['/x/gone']['after_present']
    assert not rows['/x/new']['before_present'] and rows['/x/new']['after_present']
    assert rows['/all/1']['before'] == 2 and rows['/all/1']['after'] == 4


def test_C1_o1s_tra_trung_binh_dung_va_khong_le_thuoc_thu_tu():
    # Trong ô gần t: cộng thường của [1e16,1,-1e16] mất 1; tổng chính xác = 1.
    t = 20 * audit.NS
    times = [t - 1, t - 2, t - 3, t - audit.NS - 1]
    values = [1e16, 1., -1e16, 7.]
    original = cong.o_1s(times, values, t, 'N')
    reversed_input = cong.o_1s(times[::-1], values[::-1], t, 'N')
    assert original == reversed_input == {1: 7., 0: 1 / 3}
    assert list(original) == [1, 0]


def test_audit_rho_b_tinh_tay_cho_chuoi_xen_ke():
    # 20 ô xen kẽ 0,2: mean=1, variance=1, rho1=-1 => b bị chặn sàn 5.
    t = 30 * audit.NS
    mN = [t - (j + 1) * audit.NS + 1 for j in range(20)]
    N = [float(2 * (j % 2)) for j in range(20)]
    mA = [t + j * audit.NS for j in range(20)]
    out = audit.audit_intermediates(cong, N, mN, N, mA, t, (t - 20 * audit.NS, t + 20 * audit.NS))
    assert out['mean'] == 1 and out['variance'] == 1
    assert out['rho']['1'] == -1 and out['b'] == 5
    assert out['roi_G0'] == 'it_khoi'  # 20s /5 = 4 khối mỗi phía; cần5.
    assert len(out['lag_products']['1']['pairs']) == 19


def test_explain_unit_khong_cong_nhan_p_only_khi_khong_tai_lap_native():
    ts = dict(m_span=20, m_metric=5, alpha=.01, epsilon=.05, q_hi=.95, q_lo=.05,
              n_exact_max=100, count_min=10)
    t = 100 * audit.NS
    raw = dict(N=[1.] * 5, A=[2.] * 5,
               mN=[t - (i + 1) * audit.NS for i in range(5)],
               mA=[t + i * audit.NS for i in range(5)], t_ns=t,
               bounds=(t - 10 * audit.NS, t + 10 * audit.NS), provenance=[{'synthetic': True}])
    def gate(d):
        return cong.p_theo_G3(raw['N'], raw['mN'], raw['A'], raw['mA'], t, *raw['bounds'], d, ts, 'metric|A_cpu')
    native = chuoi._gon_pv('metric|A_cpu', e4.cham_phan_vi(raw['N'], raw['A'], 5, ts, ham_p=gate))
    claimed = copy.deepcopy(native)
    claimed['p_len'] = .12345
    # Dùng cùng API cho hai bên: chứng minh nhánh so native là điều kiện thực, không chỉ có p đổi.
    explained = audit.explain_unit(raw, native, native, ts, cong)
    bad = audit.explain_unit(raw, native, claimed, ts, cong)
    assert explained['status'] == 'EXPLAINED_BY_C1_ON_IDENTICAL_RAW'
    assert bad['status'] == 'OPEN' and bad['native_mismatches']['after']


def test_downstream_thay_doi_van_OPEN_ke_ca_khong_co_p_delta():
    native = dict(window={'N': [0, 1], 'A': [1, 2]}, coverage={},
                  extra={'don_vi_phan_vi': [], 'tang_P': {'A': 1}}, blocks=[])
    altered = copy.deepcopy(native)
    altered['extra']['tang_P']['A'] = 2
    result = audit.compare_case('synthetic', native, altered, {}, cong, None, lambda **_: None)
    assert result['status'] == 'OPEN'
    assert result['unexplained_fields'][0]['pointer'] == '/extra/tang_P/A'
    assert 'extra.tang_P' in result['downstream']
