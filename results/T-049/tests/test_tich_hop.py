"""Đối chiếu bản tích hợp với ứng viên T-053 và đường native trước sửa."""
import importlib.util
import struct
import sys
from fractions import Fraction
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / name) for name in ('src', 'results/T-053/scripts', 'results/T-049/scripts')]

from m1 import e4
from m1_danh_gia.luat_c import ket_hop_the_gioi
from luat_t049 import danh_gia, hanh_dong, ve_n1

spec = importlib.util.spec_from_file_location('e4_truoc', ROOT / 'results/T-049/truoc-tich-hop-001/e4.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def test_ung_vien_va_chuoi(monkeypatch):
    integrated = e4.diem_z
    import kiem_z
    import z_on_dinh

    monkeypatch.setattr(e4, 'diem_z', old.diem_z)
    monkeypatch.setattr(z_on_dinh, 'NATIVE', old.diem_z)
    previous = kiem_z.clean(kiem_z.run())

    def compare(normal, active, *, record=None):
        z_on_dinh.diem_z(normal, active, record=record)
        return integrated(normal, active)

    monkeypatch.setattr(kiem_z, 'diem_z', compare)
    current = kiem_z.clean(kiem_z.run())
    for key in previous['checks']:
        if key != 'key':
            assert previous['checks'][key]['candidate'] == current['checks'][key]['candidate'], key
    assert previous['chain'] == current['chain']


@pytest.mark.parametrize('normal,active', [
    ([0.0, 1.0, 2.0, 7.0], [-5.0, 30.0]),
    ([-0.0, 0.0], [-0.0, 0.0]),
    ([0.0, 2**-53], [-1.0, 2.0]),
    ([0.0, 20 * sys.float_info.epsilon], [-1.0, 2.0]),
    ([float('inf'), 1.0], [-1.0, 2.0]),
    ([1.5e308] * 11, [-1.5e308, 1.5e308]),
])
def test_giu_bit_native(normal, active):
    previous = old.diem_z(normal, active)
    current = e4.diem_z(iter(normal), iter(active))
    assert previous['huu_han'] == current['huu_han']
    for key in ('med_N', 'IQR', 'c', 'z_len', 'z_xuong'):
        assert struct.pack('d', previous[key]) == struct.pack('d', current[key])


@pytest.mark.parametrize('p,lo,hi,ve,kb,t6', [
    ('GIUP', 'HAI', 'GIUP', 'KHONG_KICH_HOAT', 'GIU_C_CHO_MINH', 'GIU_BAT_CHUA_PHAN_XU'),
    ('GIUP', 'GIUP', 'GIUP', 'CHUA_KIEM_DUOC', 'GIU_C_CHO_MINH', 'GIU_BAT'),
    ('TRAI_CHIEU_O', 'TRAI_CHIEU_O', 'TRAI_CHIEU_O', 'KHONG_KICH_HOAT', 'GIU_C_CHO_MINH', 'TRINH_MINH'),
    ('TRAI_CHIEU_DATASET', 'TRAI_CHIEU_DATASET', 'TRAI_CHIEU_DATASET', 'KHONG_KICH_HOAT', 'GIU_C_CHO_MINH', 'TRINH_MINH'),
    ('HAI', 'HAI', 'HAI', 'HAI', 'GIU_C', 'BO'),
    ('GIUP', 'GIUP', 'GIUP', 'KHONG_KICH_HOAT', 'THAY_BANG_VC', 'GIU_BAT'),
])
def test_hanh_dong(p, lo, hi, ve, kb, t6):
    worlds = dict(P=p, S_lo=lo, S_hi=hi)
    assert hanh_dong('K-b', ket_hop_the_gioi(worlds, 'khoi_K'), ve) == kb
    assert hanh_dong('T6', ket_hop_the_gioi(worlds, 'luat_C'), ve) == t6


def test_ce_bien_va_thieu():
    def record(n, verdict=None):
        return {'status': 'OK', 'verdict': verdict or ('CAUSE_FOUND' if n else 'NO_INTRINSIC_ANOMALY'),
                'extra': {'tang_P': {str(i): 1 for i in range(n)}}}

    base = {'a': record(0)}
    assert ve_n1(base, {'a': record(1)})['ve'] == 'KHONG_KICH_HOAT'
    assert ve_n1(base, {'a': record(2)})['ve'] == 'HAI'
    insufficient = {'a': record(0, 'INSUFFICIENT_EVIDENCE')}
    assert ve_n1(base, insufficient)['ve'] == 'CHUA_KIEM_DUOC'
    with pytest.raises(ValueError):
        ve_n1(base, {})
    with pytest.raises(ValueError):
        ve_n1(base, {'a': dict(record(1), status='ERROR')})


def test_luat_cap_phan_biet_buoc():
    worlds = ('P', 'S_lo', 'S_hi')
    cells = {f'o{i}' for i in range(6)}
    pairs = {}
    for config, rr in (('off', (1, 1, 1)), ('on', (2, 0, 2))):
        pairs[config] = {'ca': {cell: {
            'dataset': 'RE2-TT' if i < 3 else 'Nezha-OB', 'o': cell,
            'theo_the_gioi': {world: {'RR': Fraction(score, 2)} for world, score in zip(worlds, rr, strict=True)},
        } for i, cell in enumerate(sorted(cells))}}
    quiet = {'status': 'OK', 'verdict': 'NO_INTRINSIC_ANOMALY', 'extra': {'tang_P': {}}}
    ce = {config: {'cua-so-gia': quiet} for config in pairs}
    for step, expected, action in (('K-b', 'GIUP', 'GIU_C_CHO_MINH'),
                                   ('T6', 'KHONG_DU_CA', 'GIU_BAT_CHUA_PHAN_XU')):
        result = danh_gia({'cau_hinh': pairs}, 'off', 'on', cells, ce, buoc=step)
        assert result['ket_hop']['theo_the_gioi'] == dict(P='GIUP', S_lo='HAI', S_hi='GIUP')
        assert result['ket_hop']['ket_cuc_dung'] == expected
        assert result['hanh_dong'] == action
        assert result['theo_the_gioi']['P']['UV6'] == 'KHONG_AP'


def test_do_nhay_giu_ket_cuc_cung_nguong_voi_hanh_dong(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / 'results/T-049/scripts'))
    from cham import decision_summary

    worlds = ('P', 'S_lo', 'S_hi')
    cells = {f'o{i}' for i in range(6)}
    pairs = {}
    for config, score in (('off', Fraction(1, 2)), ('on', Fraction(507, 1000))):
        pairs[config] = {'ca': {cell: {
            'dataset': 'RE2-TT' if i < 3 else 'Nezha-OB', 'o': cell,
            'theo_the_gioi': {world: {'RR': score} for world in worlds},
        } for i, cell in enumerate(sorted(cells))}}
    quiet = {'status': 'OK', 'verdict': 'NO_INTRINSIC_ANOMALY', 'extra': {'tang_P': {}}}
    ce = {config: {'cua-so-gia': quiet} for config in pairs}
    result = danh_gia({'cau_hinh': pairs}, 'off', 'on', cells, ce, buoc='K-b',
                     delta=Fraction(5, 1000))
    assert result['ket_hop']['ket_cuc_P'] == 'KHONG_TAC_DUNG'
    summary = decision_summary(result)
    assert summary['ket_hop']['ket_cuc_P'] == 'GIUP'
    assert summary['hanh_dong'] == 'THAY_BANG_VC'
