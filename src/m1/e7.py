"""E7 — vùng nghi ngờ (SPEC T-043 B2 E7; D19, D20; dinh-chinh-cai-dat.md CĐ8). Chỉ mô tả, không đổi thứ hạng.

Trên đồ thị con gồm nút có kênh F_raw = 1 (cạnh N ∪ A, cộng cạnh tĩnh khi T12 bật):
- cách 1: R_r = {r} ∪ Lên ∪ Xuống; Lên = {a: có đường a → … → r, mọi kênh F_raw của a có giải thích};
  Xuống = {b: có đường r → … → b, b có ít nhất một kênh F_raw lớp lan xuôi có giải thích}. "Có giải thích": mục
  `inherited_by` ở trạng thái 'de_xuat' (E5 tắt) hoặc 'ap_dung' (E5 bật); 'bi_E9_phu_quyet' không tính.
- cách 2: thành phần liên thông vô hướng chứa r.
- Đồ thị con rỗng: R = ∅.
"""


def _toi(nodes, ke, goc):
    seen, st = {goc}, [goc]
    while st:
        u = st.pop()
        for v in ke.get(u, ()):
            if v in nodes and v not in seen:
                seen.add(v)
                st.append(v)
    return seen


def vung(T, kenh, canh, inherited_by, cach=1):
    co = [k for k in kenh if k.co]
    V = {k.thuc_the for k in co}
    E = {(a, b) for a, b in canh if a != b and a in V and b in V}
    if not V:
        return {r: set() for r in T}
    ra, vao, vh = {}, {}, {}
    for a, b in E:
        ra.setdefault(a, set()).add(b)
        vao.setdefault(b, set()).add(a)
        vh.setdefault(a, set()).add(b)
        vh.setdefault(b, set()).add(a)
    gt = {x['ma'] for x in inherited_by if x['trang_thai'] in ('de_xuat', 'ap_dung')}  # theo mã kênh (S12)
    out = {}
    for r in T:
        if r not in V:
            out[r] = set()
            continue
        if cach == 2:
            out[r] = _toi(V, vh, r)
            continue
        len_ = {a for a in _toi(V, vao, r) - {r}
                if all(k.ma in gt for k in co if k.thuc_the == a)}
        xuong = {b for b in _toi(V, ra, r) - {r}
                 if any(k.lop == 'lan_xuoi' and k.ma in gt for k in co if k.thuc_the == b)}
        out[r] = {r} | len_ | xuong
    return out
