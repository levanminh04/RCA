"""E5 — tách tự sinh và kế thừa (SPEC T-043 B2 E5; đặc tả v1 §7.6; D19; Đ11; dinh-chinh-cai-dat.md CĐ3, CĐ9).

Luật chung, trên cạnh có hướng N ∪ A (cộng cạnh tĩnh khi T12 bật; bên gọi → bên được gọi):
- kênh lan ngược của e là kế thừa khi có bên được gọi trực tiếp b có kênh F_raw = 1 thuộc lớp lan ngược hoặc không lan
  (E1, E2, tài nguyên tăng; thao tác mới thuộc lan ngược); bắc cầu theo F_raw (b bị giải thích vẫn giải thích được e);
- kênh lan xuôi của e là kế thừa khi có bên gọi trực tiếp a có kênh F_raw = 1 bất kỳ;
- kênh lớp không lan không bao giờ được giải thích.
Nhóm vòng: SCC (cỡ >= 2) của đồ thị con gồm nút có kênh F_raw = 1 (D19). Cách đọc chính (C′, 'co_vong'): co vòng
thành một nút (CĐ3). Cách đọc chẩn đoán (A, 'ke_canh'): kề cạnh; chỉ dùng cho D5 của T-045.
E9 (tùy chọn): phủ quyết theo Đ11; tắt trên cạnh có E2 bất thường khi E2 bật (CĐ9).
"""
from collections import deque

from m1 import e9 as e9_mod

GIAI_THICH_LAN_NGUOC = ('lan_nguoc', 'khong_lan')


def scc(nodes, canh):
    """SCC theo Tarjan, tất định (duyệt theo tên). Trả danh sách frozenset."""
    ke = {v: sorted({b for a, b in canh if a == v and b in nodes}) for v in nodes}
    idx, low, st, tren, out = {}, {}, [], set(), []
    dem = [0]

    def chay(v):
        stack = [(v, iter(ke[v]))]
        idx[v] = low[v] = dem[0]
        dem[0] += 1
        st.append(v)
        tren.add(v)
        while stack:
            u, it = stack[-1]
            nxt = next(it, None)
            if nxt is not None:
                if nxt not in idx:
                    idx[nxt] = low[nxt] = dem[0]
                    dem[0] += 1
                    st.append(nxt)
                    tren.add(nxt)
                    stack.append((nxt, iter(ke[nxt])))
                elif nxt in tren:
                    low[u] = min(low[u], idx[nxt])
                continue
            stack.pop()
            if stack:
                low[stack[-1][0]] = min(low[stack[-1][0]], low[u])
            if low[u] == idx[u]:
                comp = set()
                while True:
                    w = st.pop()
                    tren.discard(w)
                    comp.add(w)
                    if w == u:
                        break
                out.append(frozenset(comp))

    for v in sorted(nodes):
        if v not in idx:
            chay(v)
    return out


def _duong(S, canh, a, b):
    """Đường ngắn nhất a → b trong S (BFS, láng giềng theo tên)."""
    if a == b:
        return [a]
    ke = {v: sorted({y for x, y in canh if x == v and y in S}) for v in S}
    truoc = {a: None}
    q = deque([a])
    while q:
        u = q.popleft()
        for v in ke[u]:
            if v not in truoc:
                truoc[v] = u
                if v == b:
                    p = [b]
                    while truoc[p[-1]] is not None:
                        p.append(truoc[p[-1]])
                    return p[::-1]
                q.append(v)
    return None


def phan_loai(kenh, canh, bat=True, doc_nhom_vong='co_vong', pham_vi_nhom_vong='F_raw', e9=None):
    """kenh: [Kenh]; canh: [(bên gọi, bên được gọi)]. Trả F_I, inherited_by, ke_thua, nhom_vong.
    e9: {'bat': bool, 'o_s', 'tau', 'canh_E2_bat_thuong': set cạnh} hoặc None."""
    if doc_nhom_vong not in ('co_vong', 'ke_canh'):
        raise ValueError(doc_nhom_vong)
    ma_all = [k.ma for k in kenh]
    if len(set(ma_all)) != len(ma_all):  # F_I theo mã: hai kênh trùng mã sẽ ghi đè nhau (S12)
        raise ValueError(f'mã kênh trùng: {sorted({m for m in ma_all if ma_all.count(m) > 1})}')
    co = sorted((k for k in kenh if k.co), key=lambda k: k.ma)  # thứ tự chuẩn: đầu ra không phụ thuộc thứ tự vào
    theo_e = {}
    for k in co:
        theo_e.setdefault(k.thuc_the, []).append(k)
    V = set(theo_e)
    E = {(a, b) for a, b in canh if a != b}
    if pham_vi_nhom_vong == 'F_raw':
        E_vong, N_vong = {(a, b) for a, b in E if a in V and b in V}, V
    else:
        E_vong = E
        N_vong = {x for e in E for x in e} | V
    comp = {}
    nhom = [c for c in scc(N_vong, E_vong) if len(c) >= 2]
    for c in nhom:
        for v in c:
            comp[v] = c
    E_co = {(a, b) for a, b in E if a in V and b in V}

    def _them(B, b, ch, duong, quy_tac):
        B.append((b, ch, tuple(duong), quy_tac))

    inherited_by, F_I, ke_thua = [], {}, []
    for c in sorted(co, key=lambda k: k.ma):
        F_I[c.ma] = 1
        if c.lop == 'khong_lan':
            continue
        e = c.thuc_the
        S = comp.get(e)
        B = []
        if c.lop == 'lan_nguoc':
            if S is None:
                for a, b in sorted(E_co):
                    if a == e:
                        for ch in theo_e[b]:
                            if ch.lop in GIAI_THICH_LAN_NGUOC:
                                _them(B, b, ch, [e, b], 'lan_nguoc')
            elif doc_nhom_vong == 'co_vong':
                for m in sorted(S - {e}):
                    for ch in theo_e.get(m, []):
                        if ch.lop == 'khong_lan':
                            _them(B, m, ch, _duong(S, E_vong, e, m), 'nhom_vong')
                for m in sorted(S):
                    for a, b in sorted(E_co):
                        if a == m and b not in S:
                            for ch in theo_e[b]:
                                if ch.lop in GIAI_THICH_LAN_NGUOC:
                                    _them(B, b, ch, _duong(S, E_vong, e, m) + [b], 'nhom_vong')
            else:
                for a, b in sorted(E_co):
                    if a == e:
                        for ch in theo_e[b]:
                            if b not in S and ch.lop in GIAI_THICH_LAN_NGUOC:
                                _them(B, b, ch, [e, b], 'lan_nguoc')
                            elif b in S and ch.lop == 'khong_lan':
                                _them(B, b, ch, [e, b], 'nhom_vong')
        else:  # lan_xuoi
            if S is None:
                for a, b in sorted(E_co):
                    if b == e:
                        for ch in theo_e[a]:
                            _them(B, a, ch, [a, e], 'lan_xuoi')
            elif doc_nhom_vong == 'co_vong':
                for m in sorted(S - {e}):
                    for ch in theo_e.get(m, []):
                        if ch.lop == 'khong_lan':
                            _them(B, m, ch, _duong(S, E_vong, m, e), 'nhom_vong')
                for m in sorted(S):
                    for a, b in sorted(E_co):
                        if b == m and a not in S:
                            for ch in theo_e[a]:
                                _them(B, a, ch, [a] + _duong(S, E_vong, m, e), 'nhom_vong')
            else:
                for a, b in sorted(E_co):
                    if b == e:
                        for ch in theo_e[a]:
                            if a not in S:
                                _them(B, a, ch, [a, e], 'lan_xuoi')
                            elif ch.lop == 'khong_lan':
                                _them(B, a, ch, [a, e], 'nhom_vong')
        if not B:
            continue
        trang_thai, ly_do = ('de_xuat', None)
        if bat:
            trang_thai = 'ap_dung'
            if e9 and e9.get('bat'):
                canh_E2 = set(e9.get('canh_E2_bat_thuong') or ())
                dung_canh_E2 = any((p[i], p[i + 1]) in canh_E2 or (p[i + 1], p[i]) in canh_E2
                                   for _, _, p, _ in B for i in range(len(p) - 1))
                if dung_canh_E2:
                    ly_do = 'tat_tren_canh_E2'
                else:
                    pq, ly_do = e9_mod.phu_quyet(c.khoi_phat, [ch.khoi_phat for _, ch, _, _ in B],
                                                 o_s=e9.get('o_s', 10), tau=e9.get('tau', 0.001))
                    if pq:
                        trang_thai = 'bi_E9_phu_quyet'
        if trang_thai == 'ap_dung':
            F_I[c.ma] = 0
            ke_thua.append((e, c.ten))
        for b, ch, duong, qt in B:
            inherited_by.append({'thuc_the': e, 'kenh': c.ten, 'huong': c.huong, 'ma': c.ma, 'don_vi': c.don_vi,
                                 'diem_truoc_E5': c.s, 'giai_thich': (b, ch.ten), 'giai_thich_ma': ch.ma,
                                 'duong': duong, 'quy_tac': qt, 'trang_thai': trang_thai, 'ly_do_E9': ly_do})
    return {'F_I': F_I, 'inherited_by': inherited_by, 'ke_thua': sorted(set(ke_thua)),
            'nhom_vong': [sorted(c) for c in sorted(nhom, key=lambda x: sorted(x))]}
