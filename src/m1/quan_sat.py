"""Trạng thái quan sát theo nguồn và thời lượng quan sát T (đặc tả v1 §2.2, sửa bởi Đ9 phiên 9 và Đ19, Đ20 phiên 10).

- Mỗi file của nguồn s phủ [bản ghi đầu, bản ghi cuối + r). Bao F_s = [đầu của mọi file, cuối của mọi file + r).
  Khe K_s = phần của F_s không thuộc file nào (hợp khoảng trước khi tìm khe, Đ20).
- H_s = [min x, max x + r) trên bản ghi của s trong cả cửa sổ đang xét.
- Trạng thái: ngoài F_s: XÁC NHẬN THIẾU THU; trong K_s: OPEN; trong F_s ∩ H_s, ngoài K_s: QUAN SÁT THEO A0;
  trong F_s, ngoài H_s: OPEN. Ô 10 giây nhiều trạng thái là ô biên.
- T^chắc = |(F ∩ H) \\ K ∩ phía|; T^max = |F ∩ phía|. P = (T_N^chắc, T_A^chắc); S_lo = (T_N^max, T_A^chắc);
  S_hi = (T_N^chắc, T_A^max).
Hàm làm việc trên một đơn vị thời gian bất kỳ, miễn mọi đối số cùng đơn vị (M1 dùng ns, Đ19 điểm 2).
"""

THIEU_THU = 'XAC_NHAN_THIEU_THU'
OPEN = 'OPEN'
A0 = 'QUAN_SAT_A0'
O_BIEN = 'O_BIEN'


def _hop(ds):
    """Hợp các khoảng nửa mở; trả danh sách rời nhau đã sắp."""
    ds = sorted((a, b) for a, b in ds if b > a)
    out = []
    for a, b in ds:
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def _giao(X, Y):
    out = []
    for a, b in X:
        for c, d in Y:
            lo, hi = max(a, c), min(b, d)
            if hi > lo:
                out.append((lo, hi))
    return _hop(out)


def _tru(X, Y):
    out = []
    for a, b in X:
        cur = [(a, b)]
        for c, d in Y:
            nxt = []
            for p, q in cur:
                if d <= p or c >= q:
                    nxt.append((p, q))
                    continue
                if c > p:
                    nxt.append((p, c))
                if d < q:
                    nxt.append((d, q))
            cur = nxt
        out += cur
    return _hop(out)


def _dai(X):
    return sum(b - a for a, b in X)


def khoang_file(moc, r):
    """Khoảng ghi của một file: [bản ghi đầu, bản ghi cuối + r)."""
    return (min(moc), max(moc) + r)


def bao_va_khe(file_khoang):
    """Bao F (một khoảng) và khe K (phần của bao không thuộc file nào)."""
    if not file_khoang:
        return [], []
    hop = _hop(file_khoang)
    bao = [(hop[0][0], hop[-1][1])]
    return bao, _tru(bao, hop)


def tinh_nguon(file_khoang, moc_ban_ghi, r, cua_so, phia, o_s=10, goc_o=None):
    """Trạng thái ô, T^chắc, T^max và ba thế giới cho một nguồn.

    file_khoang: [(đầu, cuối)) đã cộng r; moc_ban_ghi: mốc bản ghi của nguồn (mọi thực thể);
    cua_so: (lo, hi); phia: {'N': (a, b), 'A': (b, c)}; ô dài o_s, gốc ô mặc định là lo."""
    lo, hi = cua_so
    F, K = bao_va_khe(file_khoang)
    trong = [x for x in moc_ban_ghi if lo <= x < hi]
    H = [(min(trong), max(trong) + r)] if trong else []
    chac = _tru(_giao(F, H), K)
    out = {'F': F[0] if F else None, 'khe': K, 'H': H[0] if H else None, 'T_chac': {}, 'T_max': {}, 'o': {}}
    for ten, (a, b) in phia.items():
        p = [(a, b)]
        out['T_chac'][ten] = _dai(_giao(chac, p))
        out['T_max'][ten] = _dai(_giao(F, p))
        out['o'][ten] = _dem_o(a, b, F, K, H, o_s, lo if goc_o is None else goc_o)
    out['thieu_thu'] = _dai(_tru([(lo, hi)], F))
    Tc, Tm = out['T_chac'], out['T_max']
    if 'N' in phia and 'A' in phia:
        out['the_gioi'] = {'P': (Tc['N'], Tc['A']), 'S_lo': (Tm['N'], Tc['A']), 'S_hi': (Tc['N'], Tm['A'])}
    return out


def _trang_thai_doan(X, F, K, H):
    """Tập trạng thái có mặt trong đoạn X (danh sách khoảng)."""
    tt = set()
    if _dai(_tru(X, F)) > 0:
        tt.add(THIEU_THU)
    trong_F = _giao(X, F)
    if _dai(_giao(trong_F, K)) > 0:
        tt.add(OPEN)
    ngoai_K = _tru(trong_F, K)
    if _dai(_giao(ngoai_K, H)) > 0:
        tt.add(A0)
    if _dai(_tru(ngoai_K, H)) > 0:
        tt.add(OPEN)
    return tt


def _dem_o(a, b, F, K, H, o_s, goc):
    dem = {OPEN: 0, A0: 0, THIEU_THU: 0, O_BIEN: 0}
    import math
    k0 = math.floor((a - goc) / o_s)
    k = k0
    while goc + k * o_s < b:
        x0, x1 = max(a, goc + k * o_s), min(b, goc + (k + 1) * o_s)
        if x1 > x0:
            tt = _trang_thai_doan([(x0, x1)], F, K, H)
            dem[tt.pop() if len(tt) == 1 else O_BIEN] += 1
        k += 1
    return dem


def thoi_gian_nguon_metric(params, metrics_time_ns):
    """Đ19 điểm 3: mốc thời gian theo nguồn metric.

    `thoi_gian_nguon[nguồn]` là danh sách mốc ns, hoặc chuỗi "metrics.time" khi adapter xác nhận cột chung là thời
    gian thật của nguồn. Thiếu cả hai: F/H, ô, khởi phát của nguồn là UNSUPPORTED; kênh vẫn được chấm N/A chỉ khi
    `phan_hoach_NA_da_kiem[nguồn]` là true. Không thay bằng thời gian của nguồn khác."""
    tg = params.get('thoi_gian_nguon') or {}
    da_kiem = params.get('phan_hoach_NA_da_kiem') or {}
    out = {}
    for s in sorted(set((params.get('nguon_metric') or {}).values())):
        if s in tg:
            moc = list(metrics_time_ns) if tg[s] == 'metrics.time' else list(tg[s])
            out[s] = {'trang_thai': 'OK', 'moc': moc, 'cham_NA': True}
        else:
            out[s] = {'trang_thai': 'UNSUPPORTED', 'moc': None, 'cham_NA': da_kiem.get(s) is True}
    return out
