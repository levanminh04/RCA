"""RR theo ca, theo ô, MRR (dinh-nghia-pha2.json#/rr_theo_o). Tính bằng phân số chính xác (CĐ16) từ phân bố hạng
của src/p3/danh_gia (hòa theo kỳ vọng; root vắng hoặc ca không OK cho RR = 0, WHY-28)."""
from fractions import Fraction

from p3 import danh_gia


def phan_bo(blocks, root):
    """Phân bố chính xác của hạng root ({} khi root vắng)."""
    return danh_gia.phan_bo_hang(danh_gia.khoi_tu_ban_ghi({'blocks': blocks}), root)


def rr_ca(blocks, root, ok=True):
    if not ok:
        return Fraction(0)
    d = phan_bo(blocks, root)
    return sum((Fraction(p) / r for r, p in d.items()), Fraction(0))


def hit1_ca(blocks, root, ok=True):
    if not ok:
        return Fraction(0)
    return Fraction(phan_bo(blocks, root).get(1, 0))


def hang_ky_vong(blocks, root):
    d = phan_bo(blocks, root)
    if not d:
        return None
    return sum((Fraction(p) * r for r, p in d.items()), Fraction(0))


def rr_o(rr_theo_ca, o_cua_ca, trong_so=None):
    """RR_o = trung bình (có trọng số) RR_ca trên các ca của ô."""
    tong, dem = {}, {}
    for ma, r in rr_theo_ca.items():
        o = o_cua_ca[ma]
        w = Fraction(trong_so.get(ma, 1)) if trong_so else Fraction(1)
        tong[o] = tong.get(o, Fraction(0)) + w * r
        dem[o] = dem.get(o, Fraction(0)) + w
    return {o: tong[o] / dem[o] for o in tong}


def mrr(rr_theo_ca, chon=None, trong_so=None):
    """Trung bình (có trọng số) RR trên các ca được chọn."""
    ds = [m for m in rr_theo_ca if chon is None or m in chon]
    if not ds:
        return Fraction(0)
    w = {m: Fraction(trong_so.get(m, 1)) if trong_so else Fraction(1) for m in ds}
    return sum((w[m] * rr_theo_ca[m] for m in ds), Fraction(0)) / sum(w.values())
