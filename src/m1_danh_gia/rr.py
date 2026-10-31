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


def boi_so(trong_so, ma):
    """Bội số của ca `ma` (S25). `trong_so` None: mọi ca 1. Map đã truyền (kể cả map rỗng) phải có đủ mọi ca, gồm ca
    bội số 0; thiếu khóa là lỗi của bên gọi, không tự lấy 1."""
    if trong_so is None:
        return Fraction(1)
    if ma not in trong_so:
        raise ValueError(f'map bội số thiếu ca {ma}')
    w = trong_so[ma]
    if isinstance(w, bool) or not isinstance(w, (int, Fraction)) or w < 0 or Fraction(w).denominator != 1:
        raise ValueError(f'bội số của ca {ma} không hợp lệ: {w!r}')
    return Fraction(w)


def lay_mau_o(ds, rng):
    """Một mẫu theo ô cho phép độ bền (SPEC T-045 bước 7; C8, S37). ds: [{'ma', 'dataset', 'o'}] gồm mọi ca. Trong
    từng dataset (theo tên), lấy có hoàn lại đúng số ô của dataset trên danh sách ô đã sắp; ô được lấy k lần thì mọi
    ca của ô có bội số k. Trả map bội số đủ mọi ca (gồm bội số 0). rng: numpy Generator (`default_rng(seed)`)."""
    o_cua, ds_cua_o = {}, {}
    for c in ds:
        if c['ma'] in o_cua:
            raise ValueError(f"mã ca trùng: {c['ma']}")
        o_cua[c['ma']] = c['o']
        if ds_cua_o.setdefault(c['o'], c['dataset']) != c['dataset']:
            raise ValueError(f"mã ô {c['o']} trùng giữa hai dataset")
    dem = {}
    for d in sorted(set(ds_cua_o.values())):
        o_ds = sorted(o for o, x in ds_cua_o.items() if x == d)
        for i in rng.integers(0, len(o_ds), size=len(o_ds)):
            dem[o_ds[int(i)]] = dem.get(o_ds[int(i)], 0) + 1
    return {ma: dem.get(o, 0) for ma, o in o_cua.items()}


def rr_o(rr_theo_ca, o_cua_ca, trong_so=None):
    """RR_o = trung bình (có trọng số) RR_ca trên các ca của ô. Ô có tổng trọng số 0 (không được lấy vào mẫu, SPEC
    T-045 bước 7) không có RR_o và không đóng góp vào P, M; tập E_X và số ô của E_X do luật C giữ từ T0."""
    tong, dem = {}, {}
    for ma, r in rr_theo_ca.items():
        o = o_cua_ca[ma]
        w = boi_so(trong_so, ma)
        tong[o] = tong.get(o, Fraction(0)) + w * r
        dem[o] = dem.get(o, Fraction(0)) + w
    return {o: tong[o] / dem[o] for o in tong if dem[o] != 0}


def mrr(rr_theo_ca, chon=None, trong_so=None):
    """Trung bình (có trọng số) RR trên các ca được chọn."""
    ds = [m for m in rr_theo_ca if chon is None or m in chon]
    if not ds:
        return Fraction(0)
    w = {m: boi_so(trong_so, m) for m in ds}
    if sum(w.values()) == 0:
        # lấy mẫu trong từng dataset giữ số ô nên không xảy ra; xảy ra là lỗi của bên gọi
        raise ValueError('tổng trọng số của các ca được chọn bằng 0')
    return sum((w[m] * rr_theo_ca[m] for m in ds), Fraction(0)) / sum(w.values())
