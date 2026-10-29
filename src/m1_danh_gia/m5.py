"""Cờ M5 cho điều kiện riêng E5 (SPEC T-043 Phụ lục C; results/T-028/codebook.md §4, §5 dòng 95;
dinh-chinh-cai-dat.md CĐ6.1). Đếm ở k = 1 theo ca.

- M5 bật khi có e ≠ root, có đường e → root trong G_N, và e chắc chắn đứng trước root: cả hai được trả về; khối của
  e có khóa lớn hơn khối của root, hoặc cùng khối và nhóm của e đứng trước nhóm của root. Khác khối cùng khóa hay
  cùng nhóm (hòa) không tính.
- G_N: cạnh bên gọi → bên được gọi từ cha–con cùng trace, chỉ khi cả span cha lẫn span con thuộc N (end < t);
  bỏ cạnh cùng chủ; bỏ khóa trùng khác nội dung cùng cạnh trỏ tới nó; parent không resolve là mồ côi.
"""
from collections import deque


def _vi_tri(blocks):
    out = {}
    for bi, b in enumerate(blocks):
        for gi, g in enumerate(b['groups']):
            for e in g:
                out[e] = (bi, gi, tuple(float(x) for x in (b['key'] if isinstance(b['key'], (list, tuple))
                                                           else [b['key']])))
    return out


def _truoc_han(a, r):
    """a, r: (khối, nhóm, khóa). a chắc chắn trước r."""
    if a[0] == r[0]:
        return a[1] < r[1]
    return a[2] > r[2]


def _toi(G_N, dich):
    """Tập nút có đường tới dich trong G_N (không gồm dich nếu không có chu trình qua nó)."""
    vao = {}
    for a, b in G_N:
        vao.setdefault(b, set()).add(a)
    seen, q = set(), deque([dich])
    while q:
        u = q.popleft()
        for v in sorted(vao.get(u, ())):
            if v not in seen:
                seen.add(v)
                q.append(v)
    return seen


def co_M5(blocks, root, G_N):
    vt = _vi_tri(blocks)
    if root not in vt:
        return False
    nguon = _toi({(a, b) for a, b in G_N if a != b}, root) - {root}
    return any(e in vt and _truoc_han(vt[e], vt[root]) for e in nguon)


def G_N_tu_span(spans, t):
    """spans: hàng theo hop-dong.json#/vao/spans (start_us, duration_us cùng đơn vị với t)."""
    seen, xung = {}, set()
    for s in spans:
        k = (s['traceID'], s['spanID'])
        v = (s['owner'], s.get('parentSpanID'), s['start_us'], s['duration_us'])
        if k in seen and seen[k] != v:
            xung.add(k)
        seen.setdefault(k, v)
    ok = {k: v for k, v in seen.items() if k not in xung}
    out = set()
    for (tid, sid), (chu, cha, st, d) in ok.items():
        if cha in (None, ''):
            continue
        kc = (tid, cha)
        if kc not in ok:
            continue
        chu_c, _, st_c, d_c = ok[kc]
        if st + d < t and st_c + d_c < t and chu_c != chu:
            out.add((chu_c, chu))
    return out
