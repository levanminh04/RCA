"""Kiểm quy tắc verdict ứng viên V0, V1, V3 trên bảng phép kiểm giả (SPEC T-046 mục Ứng viên, sau sửa S2):
họ phép kiểm chỉ gồm phép hợp lệ của thực thể thuộc U, hướng thuộc huong_cham, không gồm NEW_OP/STOPPED; Holm bước
xuống với ngưỡng chặt; V3 đếm đơn vị khác nhau; INSUFFICIENT_EVIDENCE khi không có phép chấm hợp lệ."""
import t046


def _pv(ma, p, chenh=True, e='a', U=True, hop_le=True, huong='len'):
    return {'ma': ma, 'e': e, 'trong_U': U, 'nhom': 'metric', 'hop_le': hop_le,
            'huong': {huong: {'p_G0': p, 'p_G1': p, 'p_G3': p, 'chenh_duong': chenh}}}


def _dem(ma, p_len, F_len=0, nhan='binh_thuong', U=True, hc=('len',)):
    return {'ma': ma, 'e': 'a', 'trong_U': U, 'nhom': 'log_loi', 'hop_le': True, 'huong_cham': list(hc), 'nhan': nhan,
            'p_len': p_len, 'p_xuong': 1.0, 'F_raw_len': F_len, 'F_raw_xuong': 0}


def _bang(pv, dem=(), so=1):
    return {'pv': list(pv), 'dem': list(dem), 'alpha': 0.01, 'so_cham_hop_le': so}


def test_holm_buoc_xuong_nguong_chat():
    phep = [{'ma': 'a', 'd': 'len', 'p': 0.001}, {'ma': 'b', 'd': 'len', 'p': 0.01},
            {'ma': 'c', 'd': 'len', 'p': 0.02}]
    assert t046.holm_bac(phep, 0.05) == {('a', 'len'), ('b', 'len'), ('c', 'len')}
    phep = [{'ma': 'a', 'd': 'len', 'p': 0.05 / 3}, {'ma': 'b', 'd': 'len', 'p': 0.001 + 0.03},
            {'ma': 'c', 'd': 'len', 'p': 0.04}]
    assert t046.holm_bac(phep, 0.05) == set()  # nhỏ nhất bằng ngưỡng α/3: không bác (chặt), dừng ngay
    phep[0]['p'] = 0.01
    assert t046.holm_bac(phep, 0.05) == {('a', 'len')}  # 0,031 >= α/2 = 0,025: dừng ở bước hai


def test_V0_V3_V1_co_ban():
    nhieu = [_pv(f'u{i}', 0.5) for i in range(100)]
    mot = _bang(nhieu + [_pv('x', 0.005)])  # qua α, không qua α/101
    assert t046.verdict_R0(mot, 'G0', 'V0') == 'CAUSE_FOUND'
    assert t046.verdict_R0(mot, 'G0', 'V3') == 'NO_INTRINSIC_ANOMALY'
    assert t046.verdict_R0(mot, 'G0', 'V1') == 'NO_INTRINSIC_ANOMALY'
    hai = _bang(nhieu + [_pv('x', 0.005), _pv('y', 0.004)])
    assert t046.verdict_R0(hai, 'G0', 'V3') == 'CAUSE_FOUND'
    manh = _bang(nhieu + [_pv('x', 1e-6)])
    assert t046.verdict_R0(manh, 'G0', 'V1') == 'CAUSE_FOUND'


def test_V1_bac_nhung_khong_co_thi_khong_tinh():
    b = _bang([_pv('x', 1e-6, chenh=False)] + [_pv(f'u{i}', 0.5) for i in range(10)])
    assert t046.verdict_R0(b, 'G0', 'V1') == 'NO_INTRINSIC_ANOMALY'


def test_V3_mot_don_vi_hai_huong_khong_du():
    u = {'ma': 'x', 'e': 'a', 'trong_U': True, 'nhom': 'metric', 'hop_le': True,
         'huong': {'len': {'p_G0': 1e-6, 'chenh_duong': True}, 'xuong': {'p_G0': 1e-6, 'chenh_duong': True}}}
    assert t046.verdict_R0(_bang([u]), 'G0', 'V3') == 'NO_INTRINSIC_ANOMALY'


def test_NEW_OP_ngoai_ho_va_du_cho_V1():
    b = _bang([_pv(f'u{i}', 0.5) for i in range(10)], dem=[_dem('log|a|mau_moi', 1e-9, F_len=1, nhan='NEW_OP')])
    phep, tt = t046.co_theo_cong(b, 'G0')
    assert len(phep) == 10 and len(tt) == 1
    assert t046.verdict_R0(b, 'G0', 'V1') == 'CAUSE_FOUND'
    assert t046.chi_nho_truc_tiep(b, 'G0', 'V1')


def test_ngoai_U_va_khong_hop_le_bi_loai():
    b = _bang([_pv('x', 1e-9, U=False), _pv('y', 1e-9, hop_le=False), _pv('z', 0.5)])
    for v in ('V0', 'V1', 'V3'):
        assert t046.verdict_R0(b, 'G0', v) == 'NO_INTRINSIC_ANOMALY'
    assert t046.verdict_R0(_bang([], so=0), 'G0', 'V0') == 'INSUFFICIENT_EVIDENCE'


def test_don_vi_dem_trong_ho_chi_huong_cham():
    b = _bang([], dem=[_dem('log|a|log_loi', 1e-9, F_len=1)])
    phep, _ = t046.co_theo_cong(b, 'G0')
    assert [(x['ma'], x['d']) for x in phep] == [('log|a|log_loi', 'len')]
    assert t046.verdict_R0(b, 'G0', 'V1') == 'CAUSE_FOUND'


def test_V4_k():
    b = _bang([_pv('x', 0.005), _pv('y', 0.004), _pv('z', 0.5)], dem=[_dem('log|a|mau_moi', 1e-9, F_len=1, nhan='NEW_OP')])
    assert t046.so_don_vi_co(b, 'G0') == 3
    assert t046.so_don_vi_hop_le(b) == 4
    assert t046.verdict_R0(b, 'G0', 'V4:0.75') == 'CAUSE_FOUND'
    assert t046.verdict_R0(b, 'G0', 'V4:0.76') == 'NO_INTRINSIC_ANOMALY'
