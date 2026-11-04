"""Bốn ô dùng dữ liệu giả; đáp án tính tay, không nạp dataset/nhãn thật."""
import copy
from fractions import Fraction as F

import pytest

import adapter_t047 as ad
import so_sanh_t047 as ss
from m1 import chuoi


def blocks(groups, s1=False):
    return [{'key': [2, float(len(groups) - i), 10.0 - i, 1, float(len(groups) - i)] if s1 else
                    [2, float(len(groups) - i), 1, float(len(groups) - i)],
             'groups': [g]} for i, g in enumerate(groups)]


def test_bang_2x2_tinh_tay_co_hoa_va_root_vang():
    # Ca A: RR bốn ô = (3/4, 1, 1/2, 1); ca B = (0, 1/2, 1, 1/2).
    # RR hòa = E[1/r], không phải 1/E[r]; MRR gộp cân theo ca, không theo dataset.
    labels = {'a': {'root': 'R', 'dataset': 'dA', 'o': 'cellA'},
              'b': {'root': 'R', 'dataset': 'dB', 'o': 'cellB'}}
    group_a = [[['R', 'X']], [['R'], ['X']], [['X'], ['R']], [['R'], ['X']]]
    group_b = [[['X']], [['X'], ['R']], [['R'], ['X']], [['X'], ['R']]]
    cells = {oid: {name: {'status': 'OK', 'blocks': blocks(gs)} for name, gs in zip(ss.CELLS, groups)}
             for oid, groups in [('a', group_a), ('b', group_b)]}
    out = ss.cham_cau_hinh(cells, labels)
    assert [out['MRR'][c]['gop'] for c in ss.CELLS] == [F(3, 8), F(3, 4), F(3, 4), F(3, 4)]
    assert out['MRR']['G0D0_S0']['dA'] == F(3, 4)
    assert out['MRR']['G0D0_S0']['dB'] == 0
    assert out['chenh_MRR']['S1_tru_S0_G0D0']['gop'] == F(3, 8)
    assert out['chenh_MRR']['S1_tru_S0_G3D1']['gop'] == 0
    assert out['chenh_MRR']['G3D1_tru_G0D0_S0']['gop'] == F(3, 8)
    assert out['chenh_MRR']['G3D1_tru_G0D0_S1']['gop'] == 0
    assert out['chenh_MRR']['tuong_tac']['gop'] == -F(3, 8)
    assert out['ca']['a']['hang_ky_vong']['G0D0_S0'] == F(3, 2)
    change = out['ca']['a']['doi_hang']['S1_tru_S0_G0D0']
    assert change['phan_bo_hang_root_doi']
    assert change['quan_he_root_doi'] == [{'thuc_the': 'X', 'truoc': 'hoa', 'sau': 'sau'}]


def test_mrr_gop_can_theo_ca_khong_can_deu_dataset():
    labels = {o: {'root': 'R', 'dataset': 'dA' if o != 'c' else 'dB'} for o in 'abc'}
    cells = {o: {c: {'status': 'OK', 'blocks': blocks([['R']] if o != 'c' else [['X']])}
                  for c in ss.CELLS} for o in labels}
    out = ss.cham_cau_hinh(cells, labels)
    assert out['MRR']['G0D0_S0'] == {'gop': F(2, 3), 'dA': F(1), 'dB': F(0)}


def test_ca_khong_OK_van_o_mau_so():
    labels = {'a': {'root': 'R', 'dataset': 'd'}}
    cells = {'a': {c: {'status': 'ERROR' if c == 'G0D0_S0' else 'OK', 'blocks': blocks([['R']])}
                    for c in ss.CELLS}}
    out = ss.cham_cau_hinh(cells, labels)
    assert out['MRR']['G0D0_S0']['gop'] == 0
    assert out['MRR']['G0D0_S1']['gop'] == 1
    assert out['ca']['a']['hang_ky_vong']['G0D0_S0'] is None


def test_kiem_phuc_dung_bang_trung_gian_khong_giu_thu_tu_S1():
    rec = {'method_version': chuoi.PHIEN_BAN_CHE_DO, 'status': 'OK',
           'blocks': [{'key': [2, 1., 9., 1, 1.], 'groups': [['A']]},
                      {'key': [2, 1., 8., 2, 2.], 'groups': [['B']]},
                      {'key': [2, 1., 7., 1, 1.], 'groups': [['C']]},
                      {'key': [1, .5, 6., 1, .5], 'groups': [['D']]},
                      {'key': [0, 0., 0., 0, 0.], 'groups': [['E']]}],
           'extra': {'che_do': dict(ad.MODE), 'tang_P': {'A': 1, 'B': 1, 'C': 1, 'D': 2, 'E': 3},
                     'K_I_P': {'A': [1., 1, 1.], 'B': [1., 2, 2.], 'C': [1., 1, 1.],
                               'D': [0., 0, 0.], 'E': [0., 0, 0.]},
                     'K_raw_P': {'A': [1., 1, 1.], 'B': [1., 2, 2.], 'C': [1., 1, 1.],
                                 'D': [.5, 1, .5], 'E': [0., 0, 0.]}}}
    expected = [{'key': [2, 1., 2, 2.], 'groups': [['B']]},
                {'key': [2, 1., 1, 1.], 'groups': [['A', 'C']]},
                {'key': [1, .5, 1, .5], 'groups': [['D']]},
                {'key': [0, 0, 0, 0], 'groups': [['E']]}]
    assert ss.kiem_phuc_dung(rec) == expected
    bad = copy.deepcopy(rec)
    bad['extra']['K_I_P']['B'][1] = 1
    with pytest.raises(ValueError, match='OPEN.*lệch'):
        ss.kiem_phuc_dung(bad)
    del bad['extra']['K_raw_P']
    with pytest.raises(ValueError, match='OPEN.*thiếu'):
        ss.kiem_phuc_dung(bad)


def test_thieu_o_va_tap_ca_khong_duoc_tu_bo():
    with pytest.raises(ValueError, match='cùng tập ca'):
        ss.cham_cau_hinh({'a': {}}, {})
    with pytest.raises(ValueError, match='thiếu một'):
        ss.cham_cau_hinh({'a': {}}, {'a': {'root': 'R', 'dataset': 'd'}})


def test_hash_LOG_la_dieu_kien_truoc_nhan(monkeypatch):
    path = ad.OUT / 'runs/synthetic-2x2'
    meta = {'sha256': 'synthetic-hash', 'so_ca': 52, 'so_ban_ghi': 832,
            'cau_hinh': ['K-' + ('+'.join(c) if c else 'R0') for n in range(5)
                         for c in ss.itertools.combinations(('E1', 'E2', 'E3', 'E5'), n)]}
    monkeypatch.setattr(ss.tep_pha1, 'kiem', lambda _: meta)
    with pytest.raises(ValueError, match='chưa được ghi LOG'):
        ss.can_cu_pha1(path, '')
    text = f"- `{path.relative_to(ss.ROOT).as_posix()}`: `synthetic-hash`"
    assert ss.can_cu_pha1(path, text) == (path, meta)
    meta['so_ban_ghi'] -= 1
    with pytest.raises(ValueError, match='16 cấu hình'):
        ss.can_cu_pha1(path, text)
