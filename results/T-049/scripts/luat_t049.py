"""Kết cục và hành động K-b/T6 trên đầu ra đã ghép nhãn."""
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / path) for path in ('src', 'results/T-047/scripts')]

from luat_c_t047 import DD, H, _cap_voi_ve, ve_n1
from m1_danh_gia.luat_c import ket_hop_the_gioi


def hanh_dong(buoc, hop, ve):
    p = hop['ket_cuc_P']
    phu_thuoc = hop['phu_thuoc_quan_sat']
    trai_chieu = p in ('TRAI_CHIEU_O', 'TRAI_CHIEU_DATASET')
    if buoc == 'K-b':
        if phu_thuoc or trai_chieu or (p == 'GIUP' and ve == 'CHUA_KIEM_DUOC'):
            return 'GIU_C_CHO_MINH'
        return 'THAY_BANG_VC' if p == 'GIUP' else 'GIU_C'
    if buoc != 'T6':
        raise ValueError(buoc)
    if phu_thuoc:
        return 'GIU_BAT_CHUA_PHAN_XU'
    if trai_chieu:
        return 'TRINH_MINH'
    return {
        'HAI': 'BO',
        'GIUP': 'GIU_BAT',
        'KHONG_DU_CA': 'GIU_BAT_CHUA_PHAN_XU',
        'KHONG_TAC_DUNG': 'DE_XUAT_BO',
    }[p]


def danh_gia(kq, tat, bat, E_X, ce, *, buoc, trong_so=None, h=H, delta=Fraction(1, 100)):
    """Tính cùng luật ở điểm chính và khi đổi đúng một ngưỡng độ nhạy."""
    mode, component = {'K-b': ('khoi_K', 'E2'), 'T6': ('luat_C', 'E3b')}[buoc]
    ve = ve_n1(ce[tat], ce[bat], trong_so, h)
    result = _cap_voi_ve(kq, tat, bat, E_X, component, mode, ve, trong_so, DD)
    if delta != Fraction(1, 100):
        field = {Fraction(5, 1000): 'ket_cuc_delta_0005', Fraction(2, 100): 'ket_cuc_delta_002'}[delta]
        outcomes = {w: r['bao_kem'][field] for w, r in result['theo_the_gioi'].items()}
        result['ket_hop_do_nhay'] = ket_hop_the_gioi(outcomes, mode)
    hop = result.get('ket_hop_do_nhay', result['ket_hop'])
    result['hanh_dong'] = hanh_dong(buoc, hop, ve['ve'])
    return result
