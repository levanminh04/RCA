"""Mô tả vùng E7 sau ghép nhãn (SPEC T-043 B2 E7; D20): p = Σ 1[root ∈ R_r]/|T|; |R| kỳ vọng = Σ|R_r|/|T|;
vùng hợp chỉ là đầu ra phụ."""
from fractions import Fraction


def mo_ta(T, R_r, root, so_quan_sat=None):
    n = len(T)
    if n == 0:
        return {'p': 0.0, 'R_ky_vong': 0.0, 'hop': [], 'co_hop': 0, 'R_ky_vong_tren_O': None}
    p = Fraction(sum(1 for r in T if root in R_r.get(r, set())), n)
    rk = Fraction(sum(len(R_r.get(r, set())) for r in T), n)
    hop = sorted(set().union(*[R_r.get(r, set()) for r in T]))
    return {'p': float(p), 'R_ky_vong': float(rk), 'hop': hop, 'co_hop': len(hop),
            'R_ky_vong_tren_O': float(rk / so_quan_sat) if so_quan_sat else None}
