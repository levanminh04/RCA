"""E2 — gán bằng chứng khoảng ngoài span theo cạnh (SPEC T-043 B2 E2; đặc tả v1 §7.2; fixture 9–13).

- E2-C: gán mọi cạnh có cờ cho bên được gọi; kênh 'E2:a->b' ở bên được gọi; nhãn 'khong_dinh_danh'.
- E2-VC: S là tập cạnh có F_raw,lên = 1. Đỉnh nằm trong mọi phủ đỉnh nhỏ nhất của S là đỉnh định danh; nó nhận một
  kênh 'E2VC:<đỉnh>' với điểm lớn nhất của các cạnh nó phủ. Cạnh còn lại gán cho bên được gọi, nhãn 'khong_dinh_danh'.
  S có hơn 25 đỉnh thì dùng E2-C cho mọi cạnh và đếm số lần dự phòng.
- Đỉnh v thuộc mọi phủ nhỏ nhất khi và chỉ khi cấm v (buộc mọi láng giềng vào phủ) làm cỡ phủ nhỏ nhất tăng.
- Cạnh nối hai đỉnh định danh: ghi gán cho bên được gọi; cả hai đỉnh vẫn tính cạnh này vào điểm của mình.
"""
from functools import lru_cache

TOI_DA_DINH = 25


def _co_phu_nho_nhat(canh):
    """Cỡ phủ đỉnh nhỏ nhất của đồ thị vô hướng (frozenset các cặp đã sắp)."""
    @lru_cache(maxsize=None)
    def tau(es):
        if not es:
            return 0
        u, v = min(es)
        bo_u = frozenset(e for e in es if u not in e)
        bo_v = frozenset(e for e in es if v not in e)
        return 1 + min(tau(bo_u), tau(bo_v))
    return tau(frozenset(canh)), tau


def gan_canh(canh_co, che_do='VC', toi_da_dinh=TOI_DA_DINH):
    """canh_co: [(a, b, s)] theo thứ tự đầu vào. Trả dinh_danh, gan [(a, b, nhận, nhãn)], kenh [(thực thể, tên, s)],
    du_phong."""
    canh_co = [(a, b, float(s)) for a, b, s in canh_co]
    dinh = sorted({x for a, b, _ in canh_co for x in (a, b)})
    if che_do == 'C' or (che_do == 'VC' and len(dinh) > toi_da_dinh):
        gan = [(a, b, b, 'khong_dinh_danh') for a, b, _ in canh_co]
        kenh = [(b, f'E2:{a}->{b}', s) for a, b, s in canh_co]
        return {'dinh_danh': [], 'gan': gan, 'kenh': kenh, 'du_phong': che_do == 'VC'}
    vo_huong = {tuple(sorted((a, b))) for a, b, _ in canh_co if a != b}
    tau0, tau = _co_phu_nho_nhat(vo_huong)
    dinh_danh = []
    for v in dinh:
        lang_gieng = {x for e in vo_huong if v in e for x in e if x != v}
        con_lai = frozenset(e for e in vo_huong if not (set(e) & (lang_gieng | {v})))
        if len(lang_gieng) + tau(con_lai) > tau0:
            dinh_danh.append(v)
    dd = set(dinh_danh)
    gan, kenh = [], []
    diem_dd = {}
    for a, b, s in canh_co:
        if b in dd or a in dd:
            gan.append((a, b, b if b in dd else a, 'dinh_danh'))
            for v in (a, b):
                if v in dd:
                    diem_dd[v] = max(diem_dd.get(v, 0.0), s)
        else:
            gan.append((a, b, b, 'khong_dinh_danh'))
            kenh.append((b, f'E2:{a}->{b}', s))
    kenh = [(v, f'E2VC:{v}', diem_dd[v]) for v in sorted(diem_dd)] + kenh
    return {'dinh_danh': dinh_danh, 'gan': gan, 'kenh': kenh, 'du_phong': False}
