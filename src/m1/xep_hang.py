"""Xếp hạng (E6a, E6b), khóa K_raw/K_I, tầng, verdict (SPEC T-043 B1.3, B1.6, B1.7, B2 E6a/E6b; đặc tả v1 §6, §7.7–7.8).

- K = (max s, số kênh, Σs) trên các kênh có cờ (F_raw cho K_raw, F_I cho K_I); tập rỗng cho (0; 0; 0).
- Tầng 1: có kênh F_I = 1, sắp theo K_I. Tầng 2: không có F_I nhưng có F_raw, sắp theo K_raw. Tầng 3: còn lại, một khối hòa.
- Khóa khối ghi cho src/p3/danh_gia (khóa không tăng): E6a (3 − tầng, khóa của tầng); E6b (π làm tròn 12 chữ số
  có nghĩa, K_I, K_raw). Hòa theo khóa chính xác; trong nhóm hòa sắp theo tên chỉ để hiển thị.
- T4c (CĐ7): khóa (max s, max m, số kênh, Σs).
"""
import math

DAMPING = 0.85
TOL = 1e-12
MAX_VONG = 1000


def khoa(kenh_co):
    """(max s, số kênh, Σs) của danh sách kênh có cờ."""
    if not kenh_co:
        return (0.0, 0, 0.0)
    s = [float(k.s) for k in kenh_co]
    return (max(s), len(s), math.fsum(s))


def _lam_tron_12(x):
    return float(format(x, '.12g'))


def _nhom(items):
    """items: [(entity, key)] đã sắp giảm theo key; gộp khóa bằng nhau thành nhóm hòa."""
    blocks = []
    for e, k in items:
        if blocks and blocks[-1]['key'] == list(k):
            blocks[-1]['groups'][0].append(e)
        else:
            blocks.append({'key': list(k), 'groups': [[e]]})
    for b in blocks:
        b['groups'][0].sort()
    return blocks


def pagerank(nodes, s, canh):
    """PageRank cá nhân hóa theo SPEC B2 E6b: a → b tỷ lệ s(b), tự lặp tỷ lệ s(a), v tỷ lệ s; dòng tổng 0 nhảy về v."""
    nodes = sorted(nodes)
    tong = math.fsum(s[e] for e in nodes)
    if tong <= 0:
        return None
    v = {e: s[e] / tong for e in nodes}
    ra = {e: sorted({b for a, b in canh if a == e and b in v and b != e}) for e in nodes}
    pi = dict(v)
    for _ in range(MAX_VONG):
        moi = {e: (1 - DAMPING) * v[e] for e in nodes}
        for a in nodes:
            w = {a: s[a]}
            for b in ra[a]:
                w[b] = w.get(b, 0.0) + s[b]
            T = math.fsum(w.values())
            if T <= 0:
                for e in nodes:
                    moi[e] += DAMPING * pi[a] * v[e]
            else:
                for b, x in w.items():
                    moi[b] += DAMPING * pi[a] * x / T
        sai = math.fsum(abs(moi[e] - pi[e]) for e in nodes)
        pi = moi
        if sai < TOL:
            break
    return pi


def xep(kenh, F_I=None, thuc_the_co_kenh_OK=(), che_do='E6a', canh=(), khoa_T4c=None):
    """Xếp thực thể từ kênh. F_I: {mã kênh: 0/1}; mặc định F_I = F_raw (E5 tắt).
    khoa_T4c: {thực thể: (max m của K_raw, max m của K_I)} khi chạy T4c."""
    co = [k for k in kenh if k.co]
    F_I = F_I if F_I is not None else {k.ma: 1 for k in co}
    theo_e = {}
    for k in co:
        theo_e.setdefault(k.thuc_the, []).append(k)
    ten = set(thuc_the_co_kenh_OK) | set(theo_e)
    K_raw, K_I, tang = {}, {}, {}
    for e in ten:
        ds = theo_e.get(e, [])
        K_raw[e] = khoa(ds)
        K_I[e] = khoa([k for k in ds if F_I.get(k.ma, 0) == 1])
        tang[e] = 1 if K_I[e][1] > 0 else (2 if K_raw[e][1] > 0 else 3)
    out = {'tang': tang, 'K_I': K_I, 'K_raw': K_raw, 'trang_thai_E6b': None, 'pi': {}, 'tap_PageRank': []}

    def k_tang(e):
        if khoa_T4c is not None:
            base = K_I[e] if tang[e] == 1 else K_raw[e]
            m = khoa_T4c.get(e, (0.0, 0.0))[1 if tang[e] == 1 else 0]
            return (base[0], m, base[1], base[2])
        return K_I[e] if tang[e] == 1 else (K_raw[e] if tang[e] == 2 else (0.0, 0, 0.0))

    dung_e6a = True
    if che_do == 'E6b':
        nodes = [e for e in ten if tang[e] in (1, 2)]
        out['tap_PageRank'] = sorted(nodes)
        s = {e: K_I[e][0] for e in nodes}
        pi = pagerank(nodes, s, set(canh or ())) if nodes else None
        if pi is None:
            out['trang_thai_E6b'] = 'NO_POSITIVE_MASS'
        else:
            out['trang_thai_E6b'] = 'OK'
            out['pi'] = pi
            dung_e6a = False
            items = []
            for e in ten:
                p = _lam_tron_12(pi.get(e, 0.0))
                items.append((e, (p,) + tuple(K_I[e]) + tuple(K_raw[e])))
            items.sort(key=lambda x: (tuple(-v for v in x[1]), x[0]))
            out['blocks'] = _nhom(items)
    if dung_e6a:
        items = [(e, (3 - tang[e],) + tuple(k_tang(e))) for e in ten]
        items.sort(key=lambda x: (tuple(-v for v in x[1]), x[0]))
        out['blocks'] = _nhom(items)
    out['thu_tu'] = [e for b in out['blocks'] for g in b['groups'] for e in g]
    out['T'] = list(out['blocks'][0]['groups'][0]) if out['blocks'] else []
    return out


def rank_changed(thu_tu_theo_the_gioi):
    """RANK_CHANGED: thứ tự ứng viên đổi giữa ba thế giới (B1.3b). Nhận thứ tự phẳng hoặc danh sách khối."""
    vals = [repr(v) for v in thu_tu_theo_the_gioi.values()]
    return len(set(vals)) > 1


def verdict(tang, so_cham_hop_le):
    """B1.7: CAUSE_FOUND khi tầng 1 không rỗng; NO_INTRINSIC_ANOMALY khi tầng 1 rỗng và có phép chấm hợp lệ;
    INSUFFICIENT_EVIDENCE khi không có phép chấm hợp lệ nào."""
    if any(t == 1 for t in tang.values()):
        return 'CAUSE_FOUND'
    if so_cham_hop_le > 0:
        return 'NO_INTRINSIC_ANOMALY'
    return 'INSUFFICIENT_EVIDENCE'
