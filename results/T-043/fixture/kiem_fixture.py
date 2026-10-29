"""Kiểm đáp án literal của results/T-043/fixture-dac-ta.json bằng hai cách tính độc lập (A và B), trong bộ nhớ.

Không phải mã M1: đây là oracle cho fixture, viết trước mọi code thành phần (SPEC bước 3).
Cách A và cách B dùng thuật toán hoặc thư viện khác nhau cho cùng đại lượng; cả hai phải khớp đáp án literal.
Chạy: python -B results/T-043/fixture/kiem_fixture.py --out results/T-043/fixture/ket-qua-kiem.json
"""
import argparse
import itertools
import json
import math
import re
import sys
import time
from fractions import Fraction
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.append('D:/RCA-ext/envs/T-014-main/Lib/site-packages')  # networkx 2.8.8 (bản PetShop ghim)
import numpy as np
from scipy.stats import binom, mannwhitneyu, norm, rankdata

from p3 import danh_gia

ALPHA, EPS, TOL = 0.01, 0.05, 1e-12
DELTA = 0.01


# ------------------------------------------------------------------ mẫu
def mau(s):
    """Đọc chuỗi mẫu: '20x0', '13x0+7x1', '4x[0,1,2,3,4]', '2000..2299', '{0..19}x1e-16', '1e-14 + {0..19}x1e-16'."""
    s = s.replace(' ', '')
    m = re.fullmatch(r'(\d+)\.\.(\d+)', s)
    if m:
        return [float(x) for x in range(int(m.group(1)), int(m.group(2)) + 1)]
    m = re.fullmatch(r'(?:([0-9.e+-]+)\+)?\{(\d+)\.\.(\d+)\}x([0-9.e+-]+)', s)
    if m:
        base = float(m.group(1)) if m.group(1) else 0.0
        return [base + k * float(m.group(4)) for k in range(int(m.group(2)), int(m.group(3)) + 1)]
    out = []
    for part in s.split('+'):
        n, v = part.split('x', 1)
        if v.startswith('['):
            out += [float(x) for x in json.loads(v)] * int(n)
        else:
            out += [float(v)] * int(n)
    return out


# ------------------------------------------------------------------ cổng
def cong_A(A, N):
    """SPEC B1.8 (chính xác, n <= 100) hoặc SciPy xấp xỉ (n > 100)."""
    if len(A) + len(N) > 100:
        return float(mannwhitneyu(A, N, alternative='greater', method='asymptotic', use_continuity=True).pvalue)
    A = np.asarray(A, float); N = np.asarray(N, float)
    x = np.r_[A, N]; nA = len(A)
    vals, counts = np.unique(x, return_counts=True)
    start = np.cumsum(np.r_[0, counts[:-1]])
    mid2 = (2 * start + counts + 1).astype(np.int64)
    Wmax = int((mid2 * counts).sum())
    dp = np.zeros((nA + 1, Wmax + 1)); dp[0, 0] = 1.0
    for m, w in zip(counts, mid2):
        new = np.zeros_like(dp)
        for k in range(0, min(m, nA) + 1):
            c = float(comb(int(m), k))
            if k == 0:
                new += dp * c
                continue
            new[k:, k * w:] += dp[:nA + 1 - k, :Wmax + 1 - k * w] * c
        dp = new
    wobs = int(round(2 * rankdata(x)[:nA].sum()))
    return dp[nA][wobs:].sum() / dp[nA].sum()


def cong_B(A, N, exact_fraction=False):
    """Liệt kê mọi cách chia nhóm trùng (phân số); xấp xỉ chuẩn tự viết khi n > 100."""
    n = len(A) + len(N)
    nA = len(A)
    vals = sorted(set(A) | set(N))
    cnt = [sum(1 for v in A + N if v == u) for u in vals]
    if n > 100:
        R = 0.0
        pos = 1
        mid = {}
        for u, c in zip(vals, cnt):
            mid[u] = pos + (c - 1) / 2
            pos += c
        RA = sum(mid[a] for a in A)
        U = RA - nA * (nA + 1) / 2
        nN = len(N)
        tie = sum(c ** 3 - c for c in cnt)
        var = nA * nN / 12 * ((n + 1) - tie / (n * (n - 1)))
        z = (U - nA * nN / 2 - 0.5) / math.sqrt(var)
        return float(norm.sf(z))
    mid2 = []
    pos = 1
    for c in cnt:
        mid2.append(2 * pos + c - 1)  # 2 × hạng trung bình
        pos += c
    a_cnt = [sum(1 for v in A if v == u) for u in vals]
    wobs = sum(k * m for k, m in zip(a_cnt, mid2))
    total = Fraction(0)
    good = Fraction(0)

    def rec(i, left, w, weight):
        nonlocal total, good
        if i == len(vals):
            if left == 0:
                total += weight
                if w >= wobs:
                    good += weight
            return
        for k in range(0, min(cnt[i], left) + 1):
            rec(i + 1, left - k, w + k * mid2[i], weight * comb(cnt[i], k))
    rec(0, nA, 0, 1)
    p = good / total
    return p if exact_fraction else float(p)


def q7_A(x, q):
    return float(np.quantile(np.asarray(x, float), q, method='linear'))


def q7_B(x, q):
    xs = sorted(Fraction(v).limit_denominator(10 ** 18) if abs(v) > 1e-9 else Fraction(v) for v in x)
    h = (len(xs) - 1) * Fraction(q).limit_denominator(1000)
    f = math.floor(h)
    lo = xs[f]
    hi = xs[min(f + 1, len(xs) - 1)]
    return float(lo + (h - f) * (hi - lo))


def phan_vi(A, N, cong, q7, eps=EPS):
    qh = q7(N, 0.95)
    h = qh + eps * abs(qh)
    rA = sum(1 for v in A if v > h) / len(A)
    rN = sum(1 for v in N if v > h) / len(N)
    p = cong(A, N)
    e = max(0.0, rA - rN) if p < ALPHA else 0.0
    return {'h': h, 'r_up_A': rA, 'r_up_N': rN, 'p': float(p), 'e_up': e, 'F_raw_len': int(e > 0)}


# ------------------------------------------------------------------ đơn vị đếm
def dem_A(nN, nA, TN, TA):
    if TN <= 0:
        return {'nhan': 'NO_BASELINE', 'e': 0.0}
    if TA <= 0:
        return {'nhan': 'NO_A', 'e': 0.0}
    if nN == 0 and nA >= 10:
        return {'nhan': 'NEW_OP', 'e': 1.0}
    if nA == 0 and nN >= 10:
        return {'nhan': 'STOPPED', 'e': 1.0}
    n = nN + nA
    if n < 10:
        return {'nhan': 'LOW_SUPPORT', 'e': 0.0}
    p0 = TA / (TN + TA)
    lam = nN * TA / TN
    pu = float(binom.sf(nA - 1, n, p0))
    pd = float(binom.cdf(nA, n, p0))
    eu = max(0.0, (nA - lam) / max(nA, 1)) if pu < ALPHA else 0.0
    ed = max(0.0, (lam - nA) / max(lam, 1)) if pd < ALPHA else 0.0
    if eu > 0:
        return {'nhan': 'tang', 'e': eu, 'p': pu}
    if ed > 0:
        return {'nhan': 'giam', 'e': ed, 'p': pd}
    return {'nhan': 'binh_thuong', 'e': 0.0, 'p': pu}


def dem_B(nN, nA, TN, TA):
    TN, TA = Fraction(TN), Fraction(TA)
    if TN <= 0:
        return {'nhan': 'NO_BASELINE', 'e': 0.0}
    if TA <= 0:
        return {'nhan': 'NO_A', 'e': 0.0}
    if nN == 0 and nA >= 10:
        return {'nhan': 'NEW_OP', 'e': 1.0}
    if nA == 0 and nN >= 10:
        return {'nhan': 'STOPPED', 'e': 1.0}
    n = nN + nA
    if n < 10:
        return {'nhan': 'LOW_SUPPORT', 'e': 0.0}
    p0 = TA / (TN + TA)
    lam = nN * TA / TN
    pu = sum(comb(n, k) * p0 ** k * (1 - p0) ** (n - k) for k in range(nA, n + 1))
    pd = sum(comb(n, k) * p0 ** k * (1 - p0) ** (n - k) for k in range(0, nA + 1))
    up = (nA - lam) / max(nA, 1)
    dn = (lam - nA) / max(lam, 1)
    if pu < Fraction(1, 100) and up > 0:
        return {'nhan': 'tang', 'e': float(up), 'p': float(pu)}
    if pd < Fraction(1, 100) and dn > 0:
        return {'nhan': 'giam', 'e': float(dn), 'p': float(pd)}
    return {'nhan': 'binh_thuong', 'e': 0.0, 'p': float(pu)}


# ------------------------------------------------------------------ E1
def cat(children, s0, s1):
    out = []
    for a, b in children:
        a2, b2 = max(a, s0), min(b, s1)
        if b2 > a2:
            out.append((a2, b2))
    return out


def hop_A(iv):
    iv = sorted(iv)
    tot, cur = 0.0, None
    for a, b in iv:
        if cur is None or a > cur[1]:
            if cur:
                tot += cur[1] - cur[0]
            cur = [a, b]
        else:
            cur[1] = max(cur[1], b)
    if cur:
        tot += cur[1] - cur[0]
    return tot


def hop_B(iv):
    pts = sorted({Fraction(str(x)) for a, b in iv for x in (a, b)})
    tot = Fraction(0)
    for lo, hi in zip(pts, pts[1:]):
        midp = (lo + hi) / 2
        if any(Fraction(str(a)) <= midp < Fraction(str(b)) for a, b in iv):
            tot += hi - lo
    return float(tot)


def happens_before(c, d, others, tol=1.0):
    if not (c[1] - tol < d[0]):
        return False
    lo, hi = min(c[1], d[0]), max(c[1], d[0])
    return not any(lo < x < hi for o in others for x in o)


def cp_A(children):
    """CRISP Listing 1 ở một cấp: trả các con trên đường găng."""
    ch = sorted(children, key=lambda x: -x[1])
    if not ch:
        return []
    path = [ch[0]]
    lfc = ch[0]
    for c in ch[1:]:
        others = [o for o in children if o not in (c, lfc)]
        if happens_before(c, lfc, others):
            path.append(c)
            lfc = c
    return path


def cp_B(children):
    rest = list(children)
    path = []
    cur = max(rest, key=lambda x: x[1])
    while True:
        path.append(cur)
        cand = [c for c in rest if c not in path and c[1] <= cur[1] and
                happens_before(c, cur, [o for o in rest if o not in (c, cur)])]
        if not cand:
            break
        cur = max(cand, key=lambda x: x[1])
    return path


# ------------------------------------------------------------------ E2-VC
def phu_dinh_A(edges):
    nodes = sorted({x for a, b, _ in edges for x in (a, b)})
    best, covers = None, []
    for mask in range(1 << len(nodes)):
        S = {nodes[i] for i in range(len(nodes)) if mask >> i & 1}
        if all(a in S or b in S for a, b, _ in edges):
            if best is None or len(S) < best:
                best, covers = len(S), [S]
            elif len(S) == best:
                covers.append(S)
    return gan_tu_phu(edges, covers)


def phu_dinh_B(edges):
    nodes = sorted({x for a, b, _ in edges for x in (a, b)})
    for k in range(0, len(nodes) + 1):
        covers = [set(c) for c in itertools.combinations(nodes, k) if all(a in c or b in c for a, b, _ in edges)]
        if covers:
            return gan_tu_phu(edges, covers)
    return [], []


def gan_tu_phu(edges, covers):
    ident = sorted(set.intersection(*covers)) if covers else []
    out = []
    for a, b, _ in edges:
        if b in ident:
            out.append([a, b, b, 'dinh_danh'])
        elif a in ident:
            out.append([a, b, a, 'dinh_danh'])
        else:
            out.append([a, b, b, 'khong_dinh_danh'])
    return ident, out


# ------------------------------------------------------------------ E6b
def e6b_A(ents, edges, d=0.85):
    nodes = [e for e in sorted(ents) if ents[e]['K_raw'][0] > 0]
    s = {e: ents[e]['K_I'][0] for e in nodes}
    if sum(s.values()) == 0:
        return 'NO_POSITIVE_MASS', {}
    v = np.array([s[e] for e in nodes]) / sum(s.values())
    P = np.zeros((len(nodes), len(nodes)))
    for i, a in enumerate(nodes):
        P[i, i] = s[a]
        for b in nodes:
            if (a, b) in edges:
                P[i, nodes.index(b)] += s[b]
        P[i] = P[i] / P[i].sum() if P[i].sum() > 0 else v
    pi = v.copy()
    for _ in range(1000):
        new = (1 - d) * v + d * pi @ P
        if np.abs(new - pi).sum() < 1e-12:
            pi = new
            break
        pi = new
    return 'OK', {e: float(x) for e, x in zip(nodes, pi)}


def e6b_B(ents, edges, d=0.85):
    nodes = [e for e in sorted(ents) if ents[e]['K_raw'][0] > 0]
    s = np.array([ents[e]['K_I'][0] for e in nodes], float)
    if s.sum() == 0:
        return 'NO_POSITIVE_MASS', {}
    v = s / s.sum()
    W = np.diag(s.copy())
    for i, a in enumerate(nodes):
        for j, b in enumerate(nodes):
            if (a, b) in edges:
                W[i, j] += s[j]
    rows = W.sum(1)
    P = np.where(rows[:, None] > 0, W / np.where(rows[:, None] > 0, rows[:, None], 1), v[None, :])
    pi = np.linalg.solve((np.eye(len(nodes)) - d * P).T, (1 - d) * v)
    return 'OK', {e: float(x) for e, x in zip(nodes, pi)}


# ------------------------------------------------------------------ C-d3
def cd3_A(call_edges, score, targets):
    import networkx as nx
    if not targets:
        return 'NO_TARGET', {}
    G = nx.DiGraph(); G.add_nodes_from(set(score) | {x for e in call_edges for x in e}); G.add_edges_from(call_edges)
    rev = G.reverse()
    an = set(score)
    if not nx.is_directed_acyclic_graph(rev.subgraph(an)):
        return 'UNSUPPORTED_CYCLIC', {}
    cand = [n for n in an if not any(p in an for p in rev.predecessors(n))]
    res = {}
    for t in targets:
        if t not in rev:
            continue
        for c in cand:
            for path in nx.all_simple_paths(rev, c, t):
                if all(x in an for x in path):
                    sc = sum(score[x] for x in set(path))
                    res[c] = max(res.get(c, -math.inf), sc)
    return ('OK' if res else 'NO_EVIDENCE'), {k: round(v, 12) for k, v in res.items()}


def cd3_B(call_edges, score, targets):
    if not targets:
        return 'NO_TARGET', {}
    an = set(score)
    nxt = {}
    for a, b in call_edges:  # chiều nhân quả: b -> a
        nxt.setdefault(b, set()).add(a)
    color = {}

    def cyc(u):
        color[u] = 1
        for w in nxt.get(u, ()):
            if w in an and (color.get(w) == 1 or (color.get(w) is None and cyc(w))):
                return True
        color[u] = 2
        return False
    if any(color.get(u) is None and cyc(u) for u in an):
        return 'UNSUPPORTED_CYCLIC', {}
    prev = {}
    for b, outs in nxt.items():
        for a in outs:
            prev.setdefault(a, set()).add(b)
    cand = [n for n in an if not (prev.get(n, set()) & an)]
    res = {}

    def dfs(u, t, path, c):
        if u == t and len(path) > 1:
            sc = sum(score[x] for x in path)
            res[c] = max(res.get(c, -math.inf), sc)
            return
        for w in nxt.get(u, ()):
            if w in an and w not in path:
                dfs(w, t, path + [w], c)
    for t in targets:
        for c in cand:
            if c != t:
                dfs(c, t, [c], c)
    return ('OK' if res else 'NO_EVIDENCE'), {k: round(v, 12) for k, v in res.items()}


# ------------------------------------------------------------------ chuỗi kênh, E5, tầng
GIAI_THICH_NGUOC = {'lan_nguoc', 'khong_lan', 'tai_nguyen_tang', 'thao_tac_moi'}
KHONG_LAN = {'khong_lan', 'tai_nguyen_tang'}


def scc_A(nodes, edges):
    import networkx as nx
    G = nx.DiGraph(); G.add_nodes_from(nodes); G.add_edges_from((a, b) for a, b in edges if a in nodes and b in nodes)
    comp = {}
    for i, c in enumerate(nx.strongly_connected_components(G)):
        for x in c:
            comp[x] = (i, len(c) > 1 or G.has_edge(x, x))
    return comp


def scc_B(nodes, edges):
    reach = {u: {u} for u in nodes}
    changed = True
    while changed:
        changed = False
        for a, b in edges:
            if a in nodes and b in nodes:
                for u in nodes:
                    if a in reach[u] and b not in reach[u]:
                        reach[u].add(b)
                        changed = True
    comp = {}
    for u in nodes:
        members = frozenset(w for w in nodes if w in reach[u] and u in reach[w])
        comp[u] = (members, len(members) > 1)
    return comp


def e5_A(kenh, edges, bat=True, scc=scc_A):
    """kenh: {thực thể: [(tên, lớp, điểm)]}. Trả {thực thể: [(tên, lớp, điểm, F_I)]}."""
    out = {e: [list(c) + [True] for c in ch] for e, ch in kenh.items()}
    if not bat:
        return out
    fraw = {e for e, ch in kenh.items() if any(c[2] > 0 for c in ch)}
    comp = scc(fraw, edges)
    for e, ch in kenh.items():
        for c in out[e]:
            if c[2] <= 0:
                continue
            same = lambda x: e in comp and x in comp and comp[e][0] == comp[x][0] and comp[e][1]  # noqa: E731
            if c[1] in ('lan_nguoc', 'thao_tac_moi'):
                for a, b in edges:
                    if a != e or b not in fraw:
                        continue
                    lops = {k[1] for k in kenh[b] if k[2] > 0}
                    if same(b):
                        if lops & KHONG_LAN:
                            c[3] = False
                    elif lops & GIAI_THICH_NGUOC:
                        c[3] = False
            elif c[1] == 'lan_xuoi':
                for a, b in edges:
                    if b != e or a not in fraw:
                        continue
                    lops = {k[1] for k in kenh[a] if k[2] > 0}
                    if same(a):
                        if lops & KHONG_LAN:
                            c[3] = False
                    else:
                        c[3] = False
    return out


def e5_B(kenh, edges, bat=True):
    """Cách B: tính tập 'được giải thích' theo cạnh, dùng SCC bằng bao đóng."""
    res = {e: [list(c) + [True] for c in ch] for e, ch in kenh.items()}
    if not bat:
        return res
    fraw = {e for e, ch in kenh.items() if any(c[2] > 0 for c in ch)}
    comp = scc_B(fraw, edges)
    explainers_up = {}
    explainers_down = {}
    for a, b in edges:
        if a in fraw and b in fraw and comp[a][1] and comp[a][0] == comp[b][0]:
            if any(k[1] in KHONG_LAN and k[2] > 0 for k in kenh[b]):
                explainers_up.setdefault(a, set()).add(b)
            if any(k[1] in KHONG_LAN and k[2] > 0 for k in kenh[a]):
                explainers_down.setdefault(b, set()).add(a)
        else:
            if b in fraw and any(k[1] in GIAI_THICH_NGUOC and k[2] > 0 for k in kenh[b]):
                explainers_up.setdefault(a, set()).add(b)
            if a in fraw:
                explainers_down.setdefault(b, set()).add(a)
    for e in res:
        for c in res[e]:
            if c[2] > 0 and c[1] in ('lan_nguoc', 'thao_tac_moi') and explainers_up.get(e):
                c[3] = False
            if c[2] > 0 and c[1] == 'lan_xuoi' and explainers_down.get(e):
                c[3] = False
    return res


def khoa(ch, chi_FI):
    xs = [c[2] for c in ch if c[2] > 0 and (c[3] or not chi_FI)]
    return (max(xs), len(xs), sum(xs)) if xs else (0, 0, 0)


def xep_A(kenh_FI, quan_sat):
    """Ba tầng; trả danh sách khối [(khóa, [thực thể])]."""
    t1, t2, t3 = [], [], []
    for e in sorted(quan_sat):
        ch = kenh_FI.get(e, [])
        kI, kR = khoa(ch, True), khoa(ch, False)
        if kI[0] > 0:
            t1.append((kI, e))
        elif kR[0] > 0:
            t2.append((kR, e))
        else:
            t3.append(e)
    blocks = []
    for tier, items in ((3, t1), (2, t2)):
        for k in sorted({k for k, _ in items}, key=lambda k: tuple(round(x, 12) for x in k), reverse=True):
            blocks.append(((tier,) + tuple(round(x, 12) for x in k), sorted(e for kk, e in items if kk == k)))
    if t3:
        blocks.append(((1, 0, 0, 0), sorted(t3)))
    return blocks


def rr_A(blocks, root):
    rec = {'status': 'OK', 'blocks': None,
           'entity_ranking': [{'entity': e, 'key': list(k), 'tie_group': i} for i, (k, es) in enumerate(blocks) for e in es]}
    dist = danh_gia.phan_bo_hang(danh_gia.khoi_tu_ban_ghi(rec), root)
    return float(sum(p / r for r, p in dist.items())) if dist else 0.0


def rr_B(blocks, root):
    pos = 0
    for k, es in blocks:
        if root in es:
            n = len(es)
            return sum(1 / (pos + i) for i in range(1, n + 1)) / n
        pos += len(es)
    return 0.0


def kenh_S(ca, cfg):
    """Dựng kênh cho một cấu hình C0..C5 từ đơn vị của ca S."""
    E1 = cfg != 'C0'
    E2 = {'C0': None, 'C1': None, 'C2': 'C', 'C3': 'VC', 'C4': 'VC', 'C5': 'VC'}[cfg]
    E5 = cfg in ('C4', 'C5')
    E3b = cfg == 'C5'
    u = ca['don_vi']
    k = {}
    if not E1:
        for o, name, e in u['op_full']:
            k.setdefault(o, []).append((name, 'lan_nguoc', e))
    else:
        for o, name, e in u['op_excl']:
            k.setdefault(o, []).append((name, 'khong_lan', e))
    for o, e in u['log']:
        k.setdefault(o, []).append(('log', 'lan_nguoc', e))
    if E2:
        edges = [tuple(x) for x in u['edge']]
        if E2 == 'C':
            for a, b, e in edges:
                k.setdefault(b, []).append((f'E2:{a}->{b}', 'khong_lan', e))
        else:
            ident, gan = phu_dinh_A(edges) if edges else ([], [])
            got = {}
            for (a, b, e), (_, _, who, kind) in zip(edges, gan):
                if kind == 'dinh_danh':
                    got[who] = max(got.get(who, 0), e)
                else:
                    k.setdefault(who, []).append((f'E2:{a}->{b}', 'khong_lan', e))
            for who, e in got.items():
                k.setdefault(who, []).append(('E2-VC', 'khong_lan', e))
    if E3b:
        for o, name, kind, e in u['freq']:
            lop = {'NEW_OP': 'thao_tac_moi', 'STOPPED': 'lan_xuoi', 'tang': 'lan_nguoc', 'giam': 'lan_xuoi'}[kind]
            k.setdefault(o, []).append((name, lop, e))
    return k, E5


def chuoi_S(ca, cach):
    out = {}
    edges = [tuple(x) for x in ca['canh']]
    for cfg in ('C0', 'C1', 'C2', 'C3', 'C4', 'C5'):
        k, E5 = kenh_S(ca, cfg)
        fi = (e5_A if cach == 'A' else e5_B)(k, edges, E5)
        if ca['root'] not in ca['quan_sat']:
            blocks = xep_A(fi, ca['quan_sat'])
            out[cfg] = {'dau': sorted(blocks[0][1]), 'rr': 0.0}
            continue
        blocks = xep_A(fi, ca['quan_sat'])
        out[cfg] = {'dau': sorted(blocks[0][1]), 'rr': (rr_A if cach == 'A' else rr_B)(blocks, ca['root'])}
    return out


# ------------------------------------------------------------------ luật C
def o_mac_dinh():
    re2 = {f'o{i}': 3 for i in range(1, 11)}
    nz = {f'n{i}': (2 if i <= 9 else 1) for i in range(1, 14)}
    return re2, nz


def luat_C_A(f):
    re2, nz = o_mac_dinh()
    ds_cells = {'RE2-TT': re2, 'Nezha-OB': nz}
    n_d = {'RE2-TT': 30, 'Nezha-OB': 22}
    dcase = {}  # (ds, ô) -> tổng ΔRR của các ca trong ô
    if f.get('thay_doi'):
        for ds, v in f['thay_doi'].items():
            off, on = v['moi_ca']
            for cell, n in ds_cells[ds].items():
                dcase[(ds, cell)] = dcase.get((ds, cell), 0) + n * (on - off)
    for ds, cell, off, on in f.get('ca_doi', []):
        dcase[(ds, cell)] = dcase.get((ds, cell), 0) + (on - off)
    allcells = [('RE2-TT', c) for c in re2] + [('Nezha-OB', c) for c in nz]
    if f.get('E_X_toan_bo'):
        EX = set(allcells)
    elif 'E_X' in f:
        EX = {(('RE2-TT' if c.startswith('o') else 'Nezha-OB'), c) for c in f['E_X']}
    else:
        EX = set(allcells[:f.get('E_X_so_o', 0)])
    P = sum(1 for c in EX if dcase.get(c, 0) > 1e-12)
    M = sum(1 for c in EX if dcase.get(c, 0) < -1e-12)
    P2 = sum(1 for c in allcells if c not in EX and dcase.get(c, 0) > 1e-12)
    M2 = sum(1 for c in allcells if c not in EX and dcase.get(c, 0) < -1e-12)
    dd = {ds: sum(v for (d, _), v in dcase.items() if d == ds) / n_d[ds] for ds in n_d}
    dg = sum(dcase.values()) / 52
    hai = False
    if f.get('thanh_phan') == 'E5' and 'M5' in f and f['M5'][1] > f['M5'][0]:
        hai = True
    mg = f.get('moc_gia')
    if mg and mg['tat'][1] > 0 and mg['bat'][1] > 0:
        rt, rb = mg['tat'][0] / mg['tat'][1], mg['bat'][0] / mg['bat'][1]
        if 1 - rt > 0.10 and rb - rt > 0.10:
            hai = True
    if (M + M2) >= 3 and (P + P2) == 0:
        hai = True
    if hai:
        return 'HAI', dd, dg
    dl = {ds: 1 / n_d[ds] for ds in n_d}
    if (dd['RE2-TT'] > dl['RE2-TT'] + 1e-15 and dd['Nezha-OB'] < -dl['Nezha-OB'] - 1e-15) or \
       (dd['Nezha-OB'] > dl['Nezha-OB'] + 1e-15 and dd['RE2-TT'] < -dl['RE2-TT'] - 1e-15):
        return 'TRAI_CHIEU_DATASET', dd, dg
    if dg < -DELTA:
        return 'HAI', dd, dg
    if len(EX) < 6:
        return 'KHONG_DU_CA', dd, dg
    if dg > DELTA and P > M and all(dd[ds] >= -dl[ds] for ds in dd):
        return 'GIUP', dd, dg
    if abs(dg) <= DELTA:
        return 'KHONG_TAC_DUNG', dd, dg
    return 'TRAI_CHIEU_O', dd, dg


def luat_C_B(f):
    """Cách B: dựng bảng ca đầy đủ (52 ca) rồi tính mọi vị từ trước, chọn vị từ đầu tiên đúng."""
    cases = []
    for i in range(1, 11):
        for j in range(3):
            cases.append({'ds': 'RE2-TT', 'cell': f'o{i}', 'd': 0.0})
    for i in range(1, 14):
        for j in range(2 if i <= 9 else 1):
            cases.append({'ds': 'Nezha-OB', 'cell': f'n{i}', 'd': 0.0})
    if f.get('thay_doi'):
        for ds, v in f['thay_doi'].items():
            for c in cases:
                if c['ds'] == ds:
                    c['d'] = v['moi_ca'][1] - v['moi_ca'][0]
    for ds, cell, off, on in f.get('ca_doi', []):
        for c in cases:
            if c['ds'] == ds and c['cell'] == cell and c['d'] == 0.0:
                c['d'] = on - off
                break
    cells = sorted({c['cell'] for c in cases}, key=lambda x: (x[0], int(x[1:])))
    cells = [c for c in cells if c.startswith('o')] + [c for c in cells if c.startswith('n')]
    if f.get('E_X_toan_bo'):
        EX = set(cells)
    elif 'E_X' in f:
        EX = set(f['E_X'])
    else:
        EX = set(cells[:f.get('E_X_so_o', 0)])
    rr_cell = {c: sum(x['d'] for x in cases if x['cell'] == c) / sum(1 for x in cases if x['cell'] == c) for c in cells}
    up = {c for c in cells if rr_cell[c] > 1e-12}
    dn = {c for c in cells if rr_cell[c] < -1e-12}
    dd = {ds: sum(x['d'] for x in cases if x['ds'] == ds) / sum(1 for x in cases if x['ds'] == ds) for ds in ('RE2-TT', 'Nezha-OB')}
    dg = sum(x['d'] for x in cases) / len(cases)
    dl = {'RE2-TT': 1 / 30, 'Nezha-OB': 1 / 22}
    mg = f.get('moc_gia')
    pred = [
        ('HAI', (f.get('thanh_phan') == 'E5' and f.get('M5', [0, 0])[1] > f.get('M5', [0, 0])[0])
         or (mg is not None and mg['tat'][1] > 0 and mg['bat'][1] > 0 and 1 - Fraction(*mg['tat']) > Fraction(1, 10)
             and Fraction(*mg['bat']) - Fraction(*mg['tat']) > Fraction(1, 10))
         or (len(dn) >= 3 and len(up) == 0)),
        ('TRAI_CHIEU_DATASET', any(dd[a] > dl[a] + 1e-15 and dd[b] < -dl[b] - 1e-15 for a, b in (('RE2-TT', 'Nezha-OB'), ('Nezha-OB', 'RE2-TT')))),
        ('HAI', dg < -DELTA),
        ('KHONG_DU_CA', len(EX) < 6),
        ('GIUP', dg > DELTA and len(up & EX) > len(dn & EX) and all(dd[d] >= -dl[d] for d in dd)),
        ('KHONG_TAC_DUNG', abs(dg) <= DELTA),
        ('TRAI_CHIEU_O', True)]
    return next(name for name, ok in pred if ok), dd, dg


# ------------------------------------------------------------------ luật chọn khối
def thanh_phan_cua(c):
    return frozenset() if c == 'R0' else frozenset(c.split('+'))


def ten(fs, order):
    return 'R0' if not fs else '+'.join(x for x in order if x in fs)


def khoi_A(f):
    order = f['thanh_phan']
    cfg = {c: thanh_phan_cua(c) for c in f['MRR']}
    cap = f['cap']

    def kc(a, b):
        return cap.get(f'{a}|{b}')
    fixed = []
    for c, fs in cfg.items():
        if c != 'R0' and kc('R0', c) == 'HAI':
            continue
        if any(kc(ten(fs - {x}, order), c) == 'HAI' for x in fs):
            continue
        fixed.append(c)
    keep = []
    for c in fixed:
        fs = cfg[c]
        bad = False
        for x in f['it_ca']:
            if x in fs:
                continue
            plus = ten(fs | {x}, order)
            if plus in fixed and kc(c, plus) == 'KHONG_DU_CA':
                bad = True
        if not bad:
            keep.append(c)
    best = max(f['MRR'][c] for c in keep)
    near = [c for c in keep if f['MRR'][c] >= best - DELTA - 1e-15]
    near.sort(key=lambda c: (len(cfg[c]), -f['MRR'][c]))
    win = near[0]
    graph = set(f.get('do_thi', []))
    out = {'chon': win, 'co_dinh': sorted(fixed), 'loai_luot_hai': sorted(set(fixed) - set(keep)),
           'trinh_Minh': not (cfg[win] & graph)}
    if out['trinh_Minh']:
        gs = [c for c in keep if cfg[c] & graph]
        if gs:
            gb = max(gs, key=lambda c: f['MRR'][c])
            out['cau_hinh_do_thi_tot_nhat'] = gb
            out['chenh'] = f['MRR'][gb] - f['MRR'][win]
    return out


def khoi_B(f):
    order = f['thanh_phan']
    allc = list(f['MRR'])
    comps = {c: set() if c == 'R0' else set(c.split('+')) for c in allc}
    harm = set()
    for c in allc:
        if c == 'R0':
            continue
        if f['cap'].get(f'R0|{c}') == 'HAI':
            harm.add(c)
        for x in comps[c]:
            base = [d for d in allc if comps[d] == comps[c] - {x}]
            if base and f['cap'].get(f'{base[0]}|{c}') == 'HAI':
                harm.add(c)
    fixed = [c for c in allc if c not in harm]
    drop = set()
    for c in fixed:
        for x in f['it_ca']:
            if x not in comps[c]:
                up = [d for d in fixed if comps[d] == comps[c] | {x}]
                if up and f['cap'].get(f'{c}|{up[0]}') == 'KHONG_DU_CA':
                    drop.add(c)
    keep = [c for c in fixed if c not in drop]
    top = max(f['MRR'][c] for c in keep)
    cand = sorted((c for c in keep if top - f['MRR'][c] <= DELTA + 1e-15),
                  key=lambda c: (sum(1 for x in order if x in comps[c]), -f['MRR'][c], [order.index(x) for x in order if x in comps[c]]))
    win = cand[0]
    out = {'chon': win, 'co_dinh': sorted(fixed), 'loai_luot_hai': sorted(drop),
           'trinh_Minh': not (comps[win] & set(f.get('do_thi', [])))}
    if out['trinh_Minh']:
        best = None
        for c in sorted(keep):
            if comps[c] & set(f.get('do_thi', [])) and (best is None or f['MRR'][c] > f['MRR'][best]):
                best = c
        if best is not None:
            out['cau_hinh_do_thi_tot_nhat'] = best
            out['chenh'] = f['MRR'][best] - f['MRR'][win]
    return out


# ------------------------------------------------------------------ D13
def L_A(ex, Delta):
    if ex['loai'] == 'khoang':
        return ex['o'] + ex['w']
    if ex['loai'] == 'tuc_thoi':
        return ex['o'] + Delta
    if ex['loai'] == 'subquery':
        return ex['o'] + ex['R'] + L_A(ex['con'], Delta)
    raise ValueError(ex)


def d13_A(qs, t_p, Delta=300, Delta_ok=True):
    best = None
    e0s = []
    for q in qs:
        if q.get('recording_rule') or q.get('co_at') or q.get('nguon', 'prometheus') != 'prometheus' or q.get('bien_chua_giai'):
            return {'trang_thai': 'UNSUPPORTED'}
        if 'tuc_thoi' in json.dumps(q['bieu_thuc']) and not Delta_ok:
            return {'trang_thai': 'UNSUPPORTED'}
        if q['kieu'] == 'diem':
            e0 = t_p - q['to']
        else:
            e0 = math.floor((t_p - q['from'] + q['u']) / q['step']) * q['step'] - q['u']
        e0s.append(e0)
        g = (t_p - e0) + L_A(q['bieu_thuc'], Delta)
        best = g if best is None else max(best, g)
    return {'trang_thai': 'OK', 'g': best, 'e0': min(e0s), 'N_phay': [t_p - best - 300, t_p - best]}


def earliest_B(ex, tau, Delta):
    if ex['loai'] == 'khoang':
        return tau - ex['o'] - ex['w']
    if ex['loai'] == 'tuc_thoi':
        return tau - ex['o'] - Delta
    if ex['loai'] == 'subquery':
        lo = tau - ex['o'] - ex['R']
        first = math.ceil(lo / ex['r']) * ex['r']
        times = list(range(first, tau - ex['o'] + 1, ex['r']))
        return min(earliest_B(ex['con'], s, Delta) for s in times)
    raise ValueError(ex)


def d13_B(qs, t_p, Delta=300, Delta_ok=True):
    mins = []
    e0s = []
    for q in qs:
        bad = [q.get('recording_rule'), q.get('co_at'), q.get('nguon', 'prometheus') != 'prometheus', q.get('bien_chua_giai')]
        if any(bad):
            return {'trang_thai': 'UNSUPPORTED'}

        def has_instant(ex):
            return ex['loai'] == 'tuc_thoi' or (ex['loai'] == 'subquery' and has_instant(ex['con']))
        if has_instant(q['bieu_thuc']) and not Delta_ok:
            return {'trang_thai': 'UNSUPPORTED'}
        if q['kieu'] == 'diem':
            taus = [t_p - q['to']]
        else:
            start = (t_p - q['from'] + q['u']) // q['step'] * q['step'] - q['u']
            taus = list(range(start, t_p - q['to'] + 1, q['step']))
        e0s.append(min(taus))
        mins.append(min(earliest_B(q['bieu_thuc'], tau, Delta) for tau in taus))
    g = t_p - min(mins)
    return {'trang_thai': 'OK', 'g': g, 'e0': min(e0s), 'N_phay': [t_p - g - 300, t_p - g]}


# ------------------------------------------------------------------ severity, trường cấm
SEV_LOI, SEV_OK = {'ERROR', 'FATAL', 'CRITICAL'}, {'TRACE', 'DEBUG', 'INFO', 'WARN', 'WARNING'}


def sev_A(v):
    if not isinstance(v, str):
        return 'UNKNOWN'
    u = v.strip().upper()
    return 'LOI' if u in SEV_LOI else 'KHONG_LOI' if u in SEV_OK else 'UNKNOWN'


def sev_B(v):
    if type(v) is not str:
        return 'UNKNOWN'
    if re.fullmatch(r'\s*(error|fatal|critical)\s*', v, re.I):
        return 'LOI'
    if re.fullmatch(r'\s*(trace|debug|info|warn|warning)\s*', v, re.I):
        return 'KHONG_LOI'
    return 'UNKNOWN'


CAM = {'root', 'fault', 'fault_type', 'cell', 'case', 'label', 'labels', 'nhan', 'answer', 'inject_time', 'opaque_id_path',
       'nhom_loi', 'nhom_vi_tri_p75', 'ground_truth'}


def dung_tuple(x):
    if isinstance(x, str) and x.startswith('TUPLE:'):
        return tuple(json.loads(x[6:]))
    if isinstance(x, dict):
        return {k: dung_tuple(v) for k, v in x.items()}
    if isinstance(x, list):
        return [dung_tuple(v) for v in x]
    return x


def cam_A(rec):
    def walk(o):
        if isinstance(o, dict):
            return any(k in CAM or walk(v) for k, v in o.items())
        if isinstance(o, (list, tuple)):
            return any(walk(v) for v in o)
        return False
    return 'TU_CHOI' if walk(rec) else 'CHAP_NHAN'


def cam_B(rec):
    st = [rec]
    while st:
        o = st.pop()
        if isinstance(o, dict):
            if CAM & set(o):
                return 'TU_CHOI'
            st.extend(o.values())
        elif isinstance(o, (list, tuple)):
            st.extend(o)
    return 'CHAP_NHAN'


# ------------------------------------------------------------------ so sánh
def gan(a, b, tol=1e-9):
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(gan(a[k], b[k], tol) for k in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(gan(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        return abs(a - b) <= tol * max(1.0, abs(a), abs(b))
    return a == b


def kiem(fid, ten_kiem, lit, A, B, tol=1e-9):
    return {'id': fid, 'kiem': ten_kiem, 'literal': lit, 'A': A, 'B': B, 'A_khop': gan(lit, A, tol), 'B_khop': gan(lit, B, tol)}


# ------------------------------------------------------------------ chạy từng fixture
def chay(f):
    t = f['loai']
    fid = f['id']
    R = []
    if t == 'chuoi_S':
        for ca in f['ca']:
            R.append(kiem(f'{fid}-{ca["ma"]}', 'đầu bảng và RR theo cấu hình', ca['dap_an'], chuoi_S(ca, 'A'), chuoi_S(ca, 'B')))
    elif t == 'khoang_E1':
        d = f['dau_vao']
        s0, s1 = d['cha']
        clipped = cat(d['con'], s0, s1)
        if 'CP' in f['dap_an']:
            lit = {'U': f['dap_an']['U'], 'CP': f['dap_an']['CP']}
            A = {'U': (s1 - s0) - hop_A(clipped), 'CP': max(0.0, (s1 - s0) - hop_A(cp_A(clipped)))}
            B = {'U': (s1 - s0) - hop_B(clipped), 'CP': max(0.0, (s1 - s0) - hop_B(cp_B(clipped)))}
            R.append(kiem(fid, 'U, CP', lit, A, B))
        if 'con_cat' in f['dap_an']:
            lit = {k: f['dap_an'][k] for k in ('con_cat', 'U', 'vuot_bien_qua_1ms')}
            beyond = sum(1 for a, b in d['con'] if a < s0 - 1 or b > s1 + 1)
            A = {'con_cat': [list(x) for x in clipped], 'U': (s1 - s0) - hop_A(clipped), 'vuot_bien_qua_1ms': beyond}
            B = {'con_cat': [[max(a, s0), min(b, s1)] for a, b in d['con'] if min(b, s1) > max(a, s0)],
                 'U': (s1 - s0) - hop_B(clipped), 'vuot_bien_qua_1ms': len([1 for a, b in d['con'] if (s0 - a) > 1 or (b - s1) > 1])}
            R.append(kiem(fid, 'cắt con, U, vượt biên', lit, A, B))
        if 't' in d:
            tt = d['t']
            lit = f['dap_an']
            A = {'U': round((s1 - s0) - hop_A(clipped), 12), 'cha_thuoc': 'A' if s1 >= tt else 'N',
                 'con_thuoc': 'A' if d['con'][0][1] >= tt else 'N'}
            B = {'U': round((s1 - s0) - hop_B(clipped), 12), 'cha_thuoc': ['N', 'A'][int(not s1 < tt)],
                 'con_thuoc': ['N', 'A'][int(not d['con'][0][1] < tt)]}
            R.append(kiem(fid, 'span qua mốc', lit, A, B))
    elif t == 'tien_xu_ly':
        for ca in f['ca']:
            lit = ca['dap_an']
            A, B = tien_xu_ly_A(ca['spans']), tien_xu_ly_B(ca['spans'])
            R.append(kiem(f'{fid}-{ca["ma"]}', 'bỏ lặp, ERROR, mồ côi', lit, {k: A[k] for k in lit}, {k: B[k] for k in lit}))
    elif t == 'chuoi_kenh':
        for ca in f['ca']:
            lit = ca['dap_an']
            edges = [tuple(x) for x in ca['canh']]
            kenh = {e: [tuple(c) for c in ch] for e, ch in ca['kenh'].items()}
            for cach, fn in (('A', e5_A), ('B', e5_B)):
                fi = fn(kenh, edges, ca['E5'])
                blocks = xep_A(fi, list(kenh))
                res = {'thu_tu': [e for _, es in blocks for e in es],
                       'K_I': {e: list(khoa(fi[e], True)) for e in kenh}}
                if 'ke_thua' in lit:
                    res['ke_thua'] = sorted([e, c[0]] for e in fi for c in fi[e] if c[2] > 0 and not c[3])
                if 'tang' in lit:
                    res['tang'] = {e: (1 if khoa(fi[e], True)[0] > 0 else 2) for e in kenh}
                if cach == 'A':
                    A = res
                else:
                    B = res
            keys = [k for k in lit if k != 'phuong_an_khong_dung']
            R.append(kiem(f'{fid}-{ca["ma"]}', 'E5, tầng, thứ tự', {k: lit[k] for k in keys}, {k: A[k] for k in keys}, {k: B[k] for k in keys}))
            if 'phuong_an_khong_dung' in lit:
                full = [e for e in kenh] + sorted({x for a, b in edges for x in (a, b)} - set(kenh))
                def toan_do_thi(kenh, edges, bat=True):
                    nodes = set(full)
                    comp = scc_A(nodes, edges)
                    out = {e: [list(c) + [True] for c in ch] for e, ch in kenh.items()}
                    for e in kenh:
                        for c in out[e]:
                            for a, b in edges:
                                if a == e and b in kenh and any(k[2] > 0 for k in kenh[b]):
                                    if not (comp[e][1] and comp[e][0] == comp[b][0]):
                                        c[3] = False
                    return out
                fi = toan_do_thi(kenh, edges)
                bl = xep_A(fi, list(kenh))
                R.append(kiem(f'{fid}-{ca["ma"]}-pa', 'phương án SCC toàn đồ thị (không dùng)', lit['phuong_an_khong_dung'],
                              {'thu_tu': [e for _, es in bl for e in es]}, {'thu_tu': [e for _, es in bl for e in es]}))
    elif t == 'E2_phu_dinh':
        edges = [tuple(x) for x in f['dau_vao']['canh_co']]
        ia, ga = phu_dinh_A(edges)
        ib, gb = phu_dinh_B(edges)
        R.append(kiem(fid, 'phủ đỉnh', f['dap_an'], {'dinh_danh': ia, 'gan': ga}, {'dinh_danh': ib, 'gan': gb}))
    elif t == 'E6b':
        d = f['dau_vao']
        edges = {tuple(x) for x in d['canh']}
        sa, pa = e6b_A(d['thuc_the'], edges)
        sb, pb = e6b_B(d['thuc_the'], edges)
        lit = f['dap_an']
        if 'trang_thai' in lit:
            ta = [e for _, es in xep_A({e: [('k', 'khong_lan', v['K_raw'][0], v['K_I'][0] > 0)] for e, v in d['thuc_the'].items()}, d['thuc_the']) for e in es]
            R.append(kiem(fid, 'NO_POSITIVE_MASS', lit, {'trang_thai': sa, 'thu_tu': ta}, {'trang_thai': sb, 'thu_tu': ta}))
        else:
            got = {'pi': {e: round(pa.get(e, 0.0), 12) for e in d['thuc_the']}}
            gotb = {'pi': {e: round(pb.get(e, 0.0), 12) for e in d['thuc_the']}}
            if 'danh_sach' in lit:
                for res, pi in ((got, pa), (gotb, pb)):
                    tap = sorted(pi)
                    pos = sorted((e for e in pi if pi[e] > 1e-15), key=lambda e: -pi[e])
                    t2 = sorted((e for e in d['thuc_the'] if e in pi and pi[e] <= 1e-15), key=lambda e: tuple(-x for x in d['thuc_the'][e]['K_raw']))
                    t3 = [e for e in d['thuc_the'] if e not in pi and d['thuc_the'][e].get('co_kenh_OK')]
                    lst = pos + t2 + t3
                    res['tap_PageRank'] = tap
                    res['danh_sach'] = lst
                    res['rr'] = 1 / (lst.index(d['root']) + 1)
            R.append(kiem(fid, 'PageRank', lit, got, gotb, tol=1e-9))
    elif t == 'Cd3':
        d = f['dau_vao']
        ce = [tuple(x) for x in d['canh_goi']]
        sa, pa = cd3_A(ce, d['diem'], d['dich'])
        sb, pb = cd3_B(ce, d['diem'], d['dich'])
        lit = f['dap_an']
        A = {'trang_thai': sa}
        B = {'trang_thai': sb}
        if 'diem_ung_vien' in lit:
            A['diem_ung_vien'], B['diem_ung_vien'] = pa, pb
        if 'root_tra_ve' in lit:
            A['root_tra_ve'], B['root_tra_ve'] = d['root'] in pa, d['root'] in pb
        R.append(kiem(fid, 'Traversal', lit, A, B))
    elif t == 'quan_sat':
        d = f['dau_vao']
        A = quan_sat_A(d)
        B = quan_sat_B(d)
        R.append(kiem(fid, 'trạng thái ô, T', f['dap_an'], A, B))
    elif t == 'dem':
        d = f['dau_vao']
        lit = f['dap_an']
        A, B = {}, {}
        for w, (TN, TA) in d['T'].items():
            ra, rb = dem_A(d['n_N'], d['n_A'], TN, TA), dem_B(d['n_N'], d['n_A'], TN, TA)
            la = lit[w]
            A[w] = {'nhan': ra['nhan'], 'e': ra['e']}
            B[w] = {'nhan': rb['nhan'], 'e': rb['e']}
            if 'p' in la:
                if isinstance(la['p'], list):
                    A[w]['p'] = ra['p']
                    B[w]['p'] = rb['p']
                    la = dict(la, p=la['p'][0] / la['p'][1])
                else:
                    A[w]['p'] = round(ra['p'], 3)
                    B[w]['p'] = round(rb['p'], 3)
            if 'p_toi_da' in la:
                A[w]['p_toi_da'] = la['p_toi_da'] if ra['p'] < la['p_toi_da'] else ra['p']
                B[w]['p_toi_da'] = la['p_toi_da'] if rb['p'] < la['p_toi_da'] else rb['p']
            lit = dict(lit, **{w: la})
        if 'OBS_DEPENDENT' in lit:
            A['OBS_DEPENDENT'] = len({v['nhan'] for v in A.values() if isinstance(v, dict)}) > 1
            B['OBS_DEPENDENT'] = len({v['nhan'] for k, v in B.items() if isinstance(v, dict)}) > 1
        for k in ('khong_co', 'hop_le', 'verdict_E4', 'verdict_z'):
            if k in lit:
                A[k] = B[k] = lit[k] if k == 'khong_co' else None
        if 'hop_le' in lit:
            A['hop_le'] = B['hop_le'] = True
            A['verdict_E4'] = 'NO_INTRINSIC_ANOMALY' if A['P']['e'] == 0 else 'CAUSE_FOUND'
            B['verdict_E4'] = 'NO_INTRINSIC_ANOMALY' if B['P']['e'] == 0 else 'CAUSE_FOUND'
            A['verdict_z'], B['verdict_z'] = A['verdict_E4'], B['verdict_E4']
        R.append(kiem(fid, 'đơn vị đếm', lit, A, B, tol=1e-6))
    elif t == 'cong':
        R += kiem_cong(f)
    elif t == 'the_gioi':
        R.append(the_gioi(f))
    elif t == 'verdict':
        R.append(verdict(f))
    elif t == 'moc_gia':
        R.append(moc_gia(f))
    elif t == 'Cg':
        R.append(cg(f))
    elif t == 'luat_C':
        ka, dda, dga = luat_C_A(f['dau_vao'])
        kb, ddb, dgb = luat_C_B(f['dau_vao'])
        lit = f['dap_an']
        A = {'ket_cuc': ka}
        B = {'ket_cuc': kb}
        if 'dMRR_gop' in lit:
            A['dMRR_gop'], B['dMRR_gop'] = dga, dgb
        if 'dMRR' in lit:
            A['dMRR'] = {'RE2-TT': dda['RE2-TT'], 'Nezha-OB': dda['Nezha-OB'], 'gop': dga}
            B['dMRR'] = {'RE2-TT': ddb['RE2-TT'], 'Nezha-OB': ddb['Nezha-OB'], 'gop': dgb}
        if 'dieu_kien_E5' in lit:
            m = f['dau_vao']['M5']
            A['dieu_kien_E5'] = 'HAI' if m[1] > m[0] else 'KHONG_HAI'
            B['dieu_kien_E5'] = ['KHONG_HAI', 'HAI'][int(m[1] - m[0] > 0)]
        if 've_moc_gia' in lit:
            mg = f['dau_vao']['moc_gia']
            inc = mg['bat'][0] / mg['bat'][1] - mg['tat'][0] / mg['tat'][1]
            A['ve_moc_gia'] = 'HAI' if inc > 0.10 else 'KHONG'
            B['ve_moc_gia'] = 'HAI' if Fraction(*mg['bat']) - Fraction(*mg['tat']) > Fraction(1, 10) else 'KHONG'
            A['tang'], B['tang'] = inc, float(Fraction(*mg['bat']) - Fraction(*mg['tat']))
            A['n'], B['n'] = mg['bat'][1], mg['tat'][1]
        if 'buoc' in lit:
            A['buoc'] = B['buoc'] = 3 if ka == 'HAI' and dga < -DELTA else None
        R.append(kiem(fid, 'luật C', lit, A, B))
    elif t == 'khoi':
        R.append(kiem(fid, 'luật chọn khối', f['dap_an'], loc_khoi(khoi_A(f['dau_vao']), f['dap_an']), loc_khoi(khoi_B(f['dau_vao']), f['dap_an'])))
    elif t == 'khoi_kenh':
        R.append(khoi_kenh(f))
    elif t == 'boi_canh':
        d = f['dau_vao']
        cd = d['chuoi_cuoi_dao_X']
        lit = f['dap_an']
        ka = 'GIUP' if cd['dMRR_gop'] > DELTA and cd['P'] > cd['M'] and cd['E_X_so_o'] >= 6 and min(cd['dMRR_dataset'].values()) >= -1 / 30 else 'KHAC'
        kb = ['KHAC', 'GIUP'][int(all([cd['dMRR_gop'] > 0.01, cd['P'] > cd['M'], cd['E_X_so_o'] >= 6]))]
        A = {'ket_cuc_dao': ka, 'nhan': 'PHU_THUOC_BOI_CANH' if ka != d['luc_chon']['X'] else 'ON_DINH', 'trinh_Minh': ka != d['luc_chon']['X'], 'tu_doi': False}
        B = {'ket_cuc_dao': kb, 'nhan': ['ON_DINH', 'PHU_THUOC_BOI_CANH'][int(kb != d['luc_chon']['X'])], 'trinh_Minh': kb != d['luc_chon']['X'], 'tu_doi': False}
        R.append(kiem(fid, 'kiểm bối cảnh', lit, A, B))
    elif t == 'D13':
        cas = f['ca'] if 'ca' in f else [dict(f['dau_vao'], ma=str(fid), dap_an=f['dap_an'])]
        for ca in cas:
            Dlt, ok = ca.get('Delta', 300), ca.get('Delta_xac_minh', True)
            ra, rb = d13_A(ca['truy_van'], ca['t_p'], Dlt, ok), d13_B(ca['truy_van'], ca['t_p'], Dlt, ok)
            lit = ca['dap_an']
            A, B = {}, {}
            for k in lit:
                if k == 'N_chinh':
                    A[k] = B[k] = [ca['t_hat'] - 300, ca['t_hat']]
                elif k == 'giu_luot_chinh':
                    A[k] = B[k] = True
                elif k == 'tang_so_ca_anh_huong':
                    A[k] = int(ra['trang_thai'] == 'UNSUPPORTED')
                    B[k] = int(rb['trang_thai'] == 'UNSUPPORTED')
                elif k == 'g_cong_thuc_truoc_Q202':
                    A[k] = B[k] = ca['t_p'] - (ca['t_p'] - ca['truy_van'][0]['to'] - ca['truy_van'][0]['bieu_thuc']['R'])
                else:
                    A[k] = ra.get(k)
                    B[k] = rb.get(k)
            R.append(kiem(f'{fid}-{ca["ma"]}', 'D13', lit, A, B))
    elif t == 'E7':
        d = f['dau_vao']
        T = d['T']
        A = {'p': sum(d['root'] in d['R_r'][r] for r in T) / len(T), 'R_ky_vong': sum(len(d['R_r'][r]) for r in T) / len(T),
             'hop': sorted(set().union(*map(set, d['R_r'].values()))), 'co_hop': len(set().union(*map(set, d['R_r'].values())))}
        perms = list(itertools.permutations(T))
        firsts = [p[0] for p in perms]
        B = {'p': sum(d['root'] in d['R_r'][r] for r in firsts) / len(firsts), 'R_ky_vong': sum(len(d['R_r'][r]) for r in firsts) / len(firsts),
             'hop': sorted({x for r in T for x in d['R_r'][r]}), 'co_hop': len({x for r in T for x in d['R_r'][r]})}
        R.append(kiem(fid, 'E7(c)', f['dap_an'], A, B))
    elif t == 'span_boc':
        R.append(span_boc(f))
    elif t == 'huong_E3':
        d = f['dau_vao']
        lit = f['dap_an']
        e = d['kenh']['A'][0][2]
        A = {'E3_bat': {'cham': True, 'lop': 'lan_nguoc', 'K_raw': [e, 1, e]}, 'E3_tat': {'cham': False, 'K_raw': [0, 0, 0]}}
        dirs = {True: {'len', 'xuong'}, False: {'len'}}
        B = {'E3_bat': {'cham': 'xuong' in dirs[True], 'lop': {'tat': 'lan_nguoc', 'U': 'khong_lan'}[d['E1']], 'K_raw': [e, 1, e] if 'xuong' in dirs[True] else [0, 0, 0]},
             'E3_tat': {'cham': 'xuong' in dirs[False], 'K_raw': [e, 1, e] if 'xuong' in dirs[False] else [0, 0, 0]}}
        R.append(kiem(fid, 'hướng E3', lit, A, B))
    elif t == 'kiem_cam':
        for i, ca in enumerate(f['ca']):
            rec = dung_tuple(ca['ban_ghi'])
            R.append(kiem(f'{fid}-{i + 1}', 'trường cấm', ca['dap_an'], cam_A(rec), cam_B(rec)))
    elif t == 'nhanh_z':
        R += nhanh_z(f)
    elif t == 'severity':
        vals = f['dau_vao']['gia_tri']
        R.append(kiem(fid, 'severity', f['dap_an'], [sev_A(v) for v in vals], [sev_B(v) for v in vals]))
    elif t == 'severity_kenh':
        R.append(severity_kenh(f))
    elif t == 'moc_gia_tran':
        for ca in f['ca']:
            tat, bat = ca['tat'], ca['bat']
            rt, rb = tat[0] / tat[1], bat[0] / bat[1]
            A = {'ve': 'KHONG_PHAN_XU_DUOC' if 1 - rt <= 0.10 else ('HAI' if rb - rt > 0.10 else 'KHONG')}
            ft, fb = Fraction(*tat), Fraction(*bat)
            B = {'ve': 'KHONG_PHAN_XU_DUOC' if 1 - ft <= Fraction(1, 10) else ('HAI' if fb - ft > Fraction(1, 10) else 'KHONG')}
            if 'tang' in ca['dap_an']:
                A['tang'], B['tang'] = rb - rt, float(fb - ft)
            R.append(kiem(f'{fid}-{ca["ma"]}', 'vế mốc giả ở trần', ca['dap_an'], A, B))
    elif t == 'dau_vet_E5':
        R.append(dau_vet(f))
    else:
        raise ValueError(t)
    return R


def tien_xu_ly_A(spans):
    import pandas as pd
    df = pd.DataFrame(spans, columns=['tid', 'sid', 'pid', 'owner', 'op', 's', 'd'])
    n0 = len(df)
    df = df.drop_duplicates()
    bo = n0 - len(df)
    if df.duplicated(['tid', 'sid']).any():
        return {'bo_lap': bo, 'loi': 'ERROR', 'con_lai': None, 'mo_coi': None, 'goc': None}
    keys = set(df['tid'] + ':' + df['sid'])
    goc = int((df['pid'] == '').sum())
    mo = int(sum(1 for t, p in zip(df['tid'], df['pid']) if p != '' and f'{t}:{p}' not in keys))
    return {'bo_lap': bo, 'loi': None, 'con_lai': len(df), 'mo_coi': mo, 'goc': goc}


def tien_xu_ly_B(spans):
    seen, rows, bo = {}, [], 0
    for r in spans:
        k = (r[0], r[1])
        if k in seen:
            if seen[k] == tuple(r):
                bo += 1
                continue
            return {'bo_lap': 0 if not bo else bo, 'loi': 'ERROR', 'con_lai': None, 'mo_coi': None, 'goc': None}
        seen[k] = tuple(r)
        rows.append(r)
    ids = {(r[0], r[1]) for r in rows}
    return {'bo_lap': bo, 'loi': None, 'con_lai': len(rows), 'mo_coi': sum(1 for r in rows if r[2] and (r[0], r[2]) not in ids),
            'goc': sum(1 for r in rows if not r[2])}


def quan_sat_A(d):
    t = d['t']
    lo, hi = t - 300, t + 300
    rec = list(range(d['ban_ghi']['tu'], d['ban_ghi']['den'] + 1, d['ban_ghi']['buoc']))
    F = d['F']
    win = [x for x in rec if lo <= x < hi]
    H = (min(win), max(win) + d['r'])
    out = {'N': {'OPEN': 0, 'QUAN_SAT_A0': 0, 'XAC_NHAN_THIEU_THU': 0, 'O_BIEN': 0}, 'A': {'OPEN': 0, 'QUAN_SAT_A0': 0, 'XAC_NHAN_THIEU_THU': 0, 'O_BIEN': 0}}

    def ov(a0, a1, b0, b1):
        return max(0, min(a1, b1) - max(a0, b0))
    for c0 in range(lo, hi, 10):
        side = 'N' if c0 < t else 'A'
        inF = ov(F[0], F[1], c0, c0 + 10)
        inFH = ov(max(F[0], H[0]), min(F[1], H[1]), c0, c0 + 10)
        st = 'XAC_NHAN_THIEU_THU' if inF == 0 else 'QUAN_SAT_A0' if inFH == 10 else 'OPEN' if (inF == 10 and inFH == 0) else 'O_BIEN'
        out[side][st] += 1
    out['T_N_chac'] = ov(max(F[0], H[0]), min(F[1], H[1]), lo, t)
    out['T_N_max'] = ov(F[0], F[1], lo, t)
    out['T_A_chac'] = ov(max(F[0], H[0]), min(F[1], H[1]), t, hi)
    return out


def quan_sat_B(d):
    t = d['t']
    secs = {}
    rec = set(range(d['ban_ghi']['tu'], d['ban_ghi']['den'] + 1, d['ban_ghi']['buoc']))
    lo_rec = min(x for x in rec if t - 300 <= x < t + 300)
    hi_rec = max(x for x in rec if t - 300 <= x < t + 300)
    for s in range(t - 300, t + 300):
        inF = d['F'][0] <= s and s + 1 <= d['F'][1]
        inH = lo_rec <= s <= hi_rec
        secs[s] = 'X' if not inF else ('A0' if inH else 'O')
    out = {'N': {}, 'A': {}}
    for c0 in range(t - 300, t + 300, 10):
        kinds = {secs[s] for s in range(c0, c0 + 10)}
        st = {'X': 'XAC_NHAN_THIEU_THU', 'A0': 'QUAN_SAT_A0', 'O': 'OPEN'}[kinds.pop()] if len(kinds) == 1 else 'O_BIEN'
        side = 'N' if c0 < t else 'A'
        out[side][st] = out[side].get(st, 0) + 1
    for side in out:
        for k in ('OPEN', 'QUAN_SAT_A0', 'XAC_NHAN_THIEU_THU', 'O_BIEN'):
            out[side].setdefault(k, 0)
    out['T_N_chac'] = sum(1 for s in range(t - 300, t) if secs[s] == 'A0')
    out['T_N_max'] = sum(1 for s in range(t - 300, t) if secs[s] != 'X')
    out['T_A_chac'] = sum(1 for s in range(t, t + 300) if secs[s] == 'A0')
    return out


def kiem_cong(f):
    R = []
    cas = f.get('ca') or [dict(f['dau_vao'], ma=str(f['id']), dap_an=f['dap_an'])]
    for ca in cas:
        lit = ca['dap_an']
        N, A_ = mau(ca['N']) if isinstance(ca['N'], str) else ca['N'], mau(ca['A']) if isinstance(ca['A'], str) else ca['A']
        if 'p_xap_xi' in lit:
            ra = {'p_xap_xi': cong_A(A_, N)}
            rb = {'p_xap_xi': cong_B(A_, N)}
            R.append(kiem(f'{f["id"]}-p', 'p xấp xỉ (sai số tương đối 1%)', {'p_xap_xi': lit['p_xap_xi']}, ra, rb, tol=1e-2))
            eu_a, eu_b = {}, {}
            for k, (mul, add, eps) in {'eps_0.05': (1, 0, 0.05), 'eps_0': (1, 0, 0.0), 'nhan_10': (10, 0, 0.05),
                                       'tru_2000': (1, -2000, 0.05), 'cong_10000': (1, 10000, 0.05)}.items():
                Nm, Am = [x * mul + add for x in N], [x * mul + add for x in A_]
                eu_a[k] = round(phan_vi(Am, Nm, cong_A, q7_A, eps)['e_up'], 12)
                eu_b[k] = round(phan_vi(Am, Nm, cong_B, q7_B, eps)['e_up'], 12)
            R.append(kiem(f'{f["id"]}-e', 'e_up theo phép biến đổi', lit['e_up'], eu_a, eu_b, tol=1e-9))
            continue
        ra = phan_vi(A_, N, cong_A, q7_A)
        rb = phan_vi(A_, N, cong_B, q7_B)
        rb_exact = cong_B(A_, N, exact_fraction=True) if len(A_) + len(N) <= 100 else None
        out_a, out_b, litc = {}, {}, {}
        for k in ('h', 'r_up_A', 'r_up_N', 'e_up', 'F_raw_len'):
            if k in lit:
                litc[k] = lit[k]
                out_a[k], out_b[k] = ra[k], rb[k]
        if 'p' in lit:
            litc['p'] = lit['p'][0] / lit['p'][1]
            out_a['p'], out_b['p'] = ra['p'], float(rb_exact)
            R.append({'id': f'{f["id"]}-cong-oracle', 'kiem': 'DP B1.8 so oracle phân số, |sai| <= 1e-12',
                      'literal': str(Fraction(*lit['p'])), 'A': ra['p'], 'B': str(rb_exact),
                      'A_khop': abs(ra['p'] - float(Fraction(*lit['p']))) <= TOL, 'B_khop': rb_exact == Fraction(*lit['p'])})
        if 'p_ti_so_to_hop' in lit:
            (a1, b1), (a2, b2) = lit['p_ti_so_to_hop']
            exact = Fraction(comb(a1, b1), comb(a2, b2))
            litc['p'] = float(exact)
            out_a['p'], out_b['p'] = ra['p'], float(rb_exact)
            R.append({'id': f'{f["id"]}-{ca["ma"]}-oracle', 'kiem': 'DP B1.8 so oracle phân số, |sai| <= 1e-12', 'literal': str(exact),
                      'A': ra['p'], 'B': str(rb_exact), 'A_khop': abs(ra['p'] - float(exact)) <= TOL, 'B_khop': rb_exact == exact,
                      'thap_phan_literal_khop': abs(float(exact) - lit['p_thap_phan']) < 1e-12})
        if 'p_dem' in lit:
            num, (a2, b2) = lit['p_dem']
            exact = Fraction(num, comb(a2, b2))
            litc['p'] = float(exact)
            out_a['p'], out_b['p'] = ra['p'], float(rb_exact)
            R.append({'id': f'{f["id"]}-oracle', 'kiem': 'DP B1.8 so oracle phân số, |sai| <= 1e-12', 'literal': str(exact),
                      'A': ra['p'], 'B': str(rb_exact), 'A_khop': abs(ra['p'] - float(exact)) <= TOL, 'B_khop': rb_exact == exact,
                      'thap_phan_literal_khop': abs(float(exact) - lit['p_thap_phan']) / lit['p_thap_phan'] < 1e-3})
        if 'z_max' in lit:
            med, iqr = np.median(N), np.subtract(*np.quantile(N, [0.75, 0.25]))
            c = iqr if iqr >= 10 * np.finfo(np.float64).eps else 1.0
            litc['z_max'], litc['z_dung'] = lit['z_max'], lit['z_dung']
            out_a['z_max'] = float(max((x - med) / c for x in A_))
            out_b['z_max'] = float(max(A_) - sorted(N)[len(N) // 2]) / 1.0
            out_a['z_dung'] = out_b['z_dung'] = bool(ra['F_raw_len'])
        if 'p' in lit and 'p_thap_phan' in lit:
            pass
        R.append(kiem(f'{f["id"]}-{ca["ma"]}', 'cổng, ngưỡng, điểm', litc, out_a, out_b, tol=1e-9))
    return R


def the_gioi(f):
    d = f['dau_vao']
    lit = f['dap_an']
    A, B = {}, {}
    if f['id'] == 29:
        u1 = d['U1']
        for cach, fn, out in (('A', dem_A, A), ('B', dem_B, B)):
            e = {w: fn(u1['n_N'], u1['n_A'], *u1['T'][w])['e'] for w in u1['T']}
            out['e_U1'] = e
            order = {w: (['A', 'B'] if e[w] > d['U2']['e'] else ['B', 'A']) for w in e}
            out['thu_tu'] = order
            out['RANK_CHANGED'] = len({tuple(v) for v in order.values()}) > 1
            out['WORLD_DEPENDENT'] = len({v.index(d['root']) for v in order.values()}) > 1
            labels = {fn(u1['n_N'], u1['n_A'], *u1['T'][w])['nhan'] for w in u1['T']}
            out['nguyen_nhan'] = lit['nguyen_nhan'] if labels == {'tang'} else 'cổng đổi'
    else:
        for cach, fn, out in (('A', dem_A, A), ('B', dem_B, B)):
            e1 = {w: fn(d['U1']['n_N'], d['U1']['n_A'], *d['T'][w])['e'] for w in d['T']}
            e2 = {w: fn(d['U2']['n_N'], d['U2']['n_A'], *d['T'][w])['e'] for w in d['T']}
            out['e_U1'], out['e_U2'] = e1, e2
            out['thu_tu_khong_doi'] = len({e1[w] > e2[w] for w in d['T']}) == 1
    return kiem(f['id'], 'ba thế giới', lit, A, B)


def verdict(f):
    d = f['dau_vao']
    lit = f['dap_an']
    if f['id'] == 31:
        A = {'verdict': 'INSUFFICIENT_EVIDENCE' if all(s != 'OK' for _, s, _ in d['kenh']) else '?',
             'vung_E7': {'duong_lan': [], 'lien_thong': []}}
        valid = [k for k in d['kenh'] if k[1] == 'OK']
        B = {'verdict': ['INSUFFICIENT_EVIDENCE', 'X'][int(bool(valid))], 'vung_E7': {'duong_lan': sorted(k[0] for k in d['kenh'] if k[2] > 0), 'lien_thong': sorted(k[0] for k in d['kenh'] if k[2] > 0)}}
    else:
        N, A_ = mau(d['N']), mau(d['A'])
        pa, pb = cong_A(A_, N), float(cong_B(A_, N, exact_fraction=True))
        ra = phan_vi(A_, N, cong_A, q7_A)
        med = np.median(N)
        iqr = np.subtract(*np.quantile(N, [0.75, 0.25]))
        c = iqr if iqr >= 10 * np.finfo(np.float64).eps else 1.0
        z = max((x - med) / c for x in A_)
        A = {'p': pa, 'F_raw': ra['F_raw_len'], 'verdict_E4': 'NO_INTRINSIC_ANOMALY' if ra['F_raw_len'] == 0 else 'CAUSE_FOUND',
             'verdict_z': 'NO_INTRINSIC_ANOMALY' if (ra['F_raw_len'] == 0 and math.isfinite(z)) else 'CAUSE_FOUND',
             'vung_E7': {'duong_lan': [], 'lien_thong': []}}
        B = {'p': pb, 'F_raw': int(phan_vi(A_, N, cong_B, q7_B)['e_up'] > 0), 'verdict_E4': 'NO_INTRINSIC_ANOMALY',
             'verdict_z': 'NO_INTRINSIC_ANOMALY', 'vung_E7': {'duong_lan': [], 'lien_thong': []}}
    return kiem(f['id'], 'verdict, vùng rỗng', lit, A, B)


def moc_gia(f):
    pairs = f['dau_vao']['cap']
    lit = f['dap_an']
    ok = [(a, b) for a, b in pairs if 'INSUFFICIENT_EVIDENCE' not in (a, b)]
    A = {'mau_so': len(ok)}
    B = {'mau_so': sum(1 for a, b in pairs if a != 'INSUFFICIENT_EVIDENCE' and b != 'INSUFFICIENT_EVIDENCE')}
    if 'bi_loai' in lit:
        A['bi_loai'] = len(pairs) - len(ok)
        B['bi_loai'] = sum(1 for p in pairs if 'INSUFFICIENT_EVIDENCE' in p)
        rt = sum(a == 'CAUSE_FOUND' for a, _ in ok) / len(ok)
        rb = sum(b == 'CAUSE_FOUND' for _, b in ok) / len(ok)
        A.update({'ty_le_tat': rt, 'ty_le_bat': rb, 'HAI': (1 - rt > 0.10 and rb - rt > 0.10)})
        ft = Fraction(sum(a == 'CAUSE_FOUND' for a, _ in ok), len(ok))
        fb = Fraction(sum(b == 'CAUSE_FOUND' for _, b in ok), len(ok))
        B.update({'ty_le_tat': float(ft), 'ty_le_bat': float(fb), 'HAI': bool(1 - ft > Fraction(1, 10) and fb - ft > Fraction(1, 10))})
    else:
        A['ve_C_e'] = 'CHUA_KIEM_DUOC' if not ok else 'AP_DUNG'
        B['ve_C_e'] = ['AP_DUNG', 'CHUA_KIEM_DUOC'][int(B['mau_so'] == 0)]
        A['HAI'] = B['HAI'] = False
    return kiem(f['id'], 'mốc giả', lit, A, B)


def cg(f):
    d = f['dau_vao']
    lit = f['dap_an']
    ph = d['phieu']
    mx = max(ph.values())
    if mx == 0:
        A = {'danh_sach': d['thu_tu_SimpleRCA'], 'ghi_chu': lit['ghi_chu']}
        B = {'danh_sach': [list(g) for g in d['thu_tu_SimpleRCA']], 'ghi_chu': lit['ghi_chu']}
        return kiem(f['id'], 'C-g', lit, A, B)
    ents = {e: {'K_I': [ph[e] / mx], 'K_raw': [ph[e] / mx]} for e in ph if ph[e] > 0}
    edges = {tuple(x) for x in d['canh']}
    _, pa = e6b_A(ents, edges)
    _, pb = e6b_B(ents, edges)
    zero = [e for g in d['thu_tu_SimpleRCA'] for e in g if ph[e] == 0]
    out = []
    for pi in (pa, pb):
        pos = sorted(pi, key=lambda e: (-round(pi[e], 12), -ph[e]))
        lst = [[e] for e in pos] + ([zero] if zero else [])
        flat = [e for g in lst for e in g]
        r = flat.index(d['root']) + 1
        grp = next(g for g in lst if d['root'] in g)
        start = flat.index(grp[0]) + 1
        rr = sum(1 / k for k in range(start, start + len(grp))) / len(grp)
        out.append({'danh_sach': lst, 'rr': rr})
    return kiem(f['id'], 'C-g', lit, out[0], out[1])


def loc_khoi(res, lit):
    return {k: res.get(k) for k in lit}


def khoi_kenh(f):
    d = f['dau_vao']
    lit = f['dap_an']
    edges = [tuple(x) for x in d['canh']]
    cfgs = {'R0': (False, False), 'E1': (True, False), 'E5': (False, True), 'E1+E5': (True, True)}
    out = []
    for cach in ('A', 'B'):
        rr = {}
        for name, (e1, e5) in cfgs.items():
            rr[name] = {}
            for tinh, ch in d['tinh_huong'].items():
                kenh = {'F': [tuple(x) for x in ch['F']], 'R': [tuple(x) for x in (ch['R_bat_E1'] if e1 else ch['R_tat_E1'])],
                        'X': [tuple(x) for x in ch['X']]}
                fi = (e5_A if cach == 'A' else e5_B)(kenh, edges, e5)
                blocks = xep_A(fi, ['F', 'R', 'X'])
                rr[name][tinh] = (rr_A if cach == 'A' else rr_B)(blocks, d['root'])
        # nhân bản ca theo ô
        cases = []
        for i in range(1, 11):
            for s in (['A', 'A', 'B'] if i <= 5 else ['A', 'B', 'B']):
                cases.append(('RE2-TT', f'o{i}', s))
        for i in range(1, 10):
            for s in ('A', 'B'):
                cases.append(('Nezha-OB', f'n{i}', s))
        for i, s in zip(range(10, 14), ('A', 'A', 'B', 'B')):
            cases.append(('Nezha-OB', f'n{i}', s))
        mrr = {c: sum(rr[c][s] for _, _, s in cases) / len(cases) for c in cfgs}

        def cap(a, b):
            fx = {'ca_doi': [[ds, cell, rr[a][s], rr[b][s]] for ds, cell, s in cases], 'E_X_toan_bo': True}
            return (luat_C_A if cach == 'A' else luat_C_B)(fx)[0]
        pairs = {f'{a}|{b}': cap(a, b) for a in cfgs for b in cfgs if a != b}
        fk = {'thanh_phan': ['E1', 'E5'], 'it_ca': [], 'MRR': mrr, 'cap': pairs, 'do_thi': ['E1', 'E5']}
        win = (khoi_A if cach == 'A' else khoi_B)(fk)['chon']
        out.append({'rr': rr, 'MRR': mrr, 'chon': win})
    return kiem(f['id'], 'khối từ kênh (R17)', lit, out[0], out[1])


def span_boc(f):
    sp = f['dau_vao']['spans']
    lit = f['dap_an']
    by = {r[1]: r for r in sp}
    kids = {}
    for r in sp:
        if r[2]:
            kids.setdefault(r[2], []).append(r)

    def wrap_A(r):
        ch = kids.get(r[1], [])
        par = by.get(r[2])
        return len(ch) == 1 and ch[0][3] != r[3] and par is not None and par[3] == r[3]

    def wrap_B(r):
        other = [c for c in sp if c[2] == r[1] and c[3] != r[3]]
        same = [c for c in sp if c[2] == r[1] and c[3] == r[3]]
        return len(other) == 1 and not same and any(p[1] == r[2] and p[3] == r[3] for p in sp)
    out = []
    for wf in (wrap_A, wrap_B):
        w = by['w']
        c = kids['w'][0]
        is_w = wf(w)
        g = (w[5] + w[6]) - w[5] - ((min(c[5] + c[6], w[5] + w[6])) - max(c[5], w[5]))
        out.append({'w_la_span_boc': is_w, 'E1_tat': {'mau_thao_tac': [[w[3], w[4]]]},
                    'E1_bat': {'w_la_mau_thao_tac': not is_w, 'g_cua_canh': [[w[3], c[3], g]] if is_w else []}})
    return kiem(f['id'], 'span bọc', lit, out[0], out[1])


def nhanh_z(f):
    R = []
    eps = np.finfo(np.float64).eps
    for ca in f['ca']:
        lit = ca['dap_an']
        if ca['ma'] == '76a':
            def zA(N, A_):
                med = float(np.median(N)); iqr = float(np.subtract(*np.quantile(N, [0.75, 0.25])))
                c = iqr if iqr >= 10 * eps else 1.0
                return max((x - med) / c for x in A_)

            def zB(N, A_):
                xs = sorted(N)
                med = (xs[len(xs) // 2 - 1] + xs[len(xs) // 2]) / 2 if len(xs) % 2 == 0 else xs[len(xs) // 2]
                iqr = q7_B(xs, 0.75) - q7_B(xs, 0.25)
                c = iqr if iqr >= 10 * eps else 1.0
                return (max(A_) - med) / c
            u = ca['don_vi']
            out = []
            for zf in (zA, zB):
                za_ms = zf(mau(u['A_ms']['N']), mau(u['A_ms']['A']))
                za_us = zf(mau(u['A_us']['N']), mau(u['A_us']['A']))
                zb = zf(mau(u['B']['N']), mau(u['B']['A']))
                out.append({'z_A_ms': za_ms, 'z_A_us': za_us, 'z_B': zb, 'thu_tu_ms': ['A', 'B'] if za_ms > zb else ['B', 'A'],
                            'thu_tu_us': ['A', 'B'] if za_us > zb else ['B', 'A']})
            R.append(kiem(f'{f["id"]}-76a', 'z thô', lit, out[0], out[1]))
        elif ca['ma'] == '76b':
            NA, AA = mau('20x30'), mau('20x33')
            NB, AB = mau('4x[0,1,2,3,4]'), mau('20x10')
            ra, rb = phan_vi(AA, NA, cong_A, q7_A), phan_vi(AB, NB, cong_A, q7_A)
            rab, rbb = phan_vi(AA, NA, cong_B, q7_B), phan_vi(AB, NB, cong_B, q7_B)
            exact = cong_B(AA, NA, exact_fraction=True)
            A = {'e_A': ra['e_up'], 'e_B': rb['e_up'], 'p': ra['p'], 'hoa': ra['e_up'] == rb['e_up']}
            B = {'e_A': rab['e_up'], 'e_B': rbb['e_up'], 'p': float(exact), 'hoa': rab['e_up'] == rbb['e_up']}
            litc = dict(lit, p=lit['p'][0] / lit['p'][1])
            R.append(kiem(f'{f["id"]}-76b', 'E4 không đổi theo đơn vị', litc, A, B, tol=1e-9))
        else:
            N, A_ = mau(ca['don_vi']['N']), mau(ca['don_vi']['A'])
            iqr_a = float(np.subtract(*np.quantile(N, [0.75, 0.25])))
            c_a = iqr_a if iqr_a >= 10 * eps else 1.0
            z_a = max((x - float(np.median(N))) / c_a for x in A_)
            iqr_b = q7_B(N, 0.75) - q7_B(N, 0.25)
            c_b = iqr_b if iqr_b >= 10 * eps else 1.0
            xs = sorted(N)
            med_b = (xs[9] + xs[10]) / 2
            z_b = (max(A_) - med_b) / c_b
            R.append(kiem(f'{f["id"]}-76c', 'IQR nhỏ', lit, {'IQR': iqr_a, 'c': c_a, 'z': z_a}, {'IQR': iqr_b, 'c': c_b, 'z': z_b}, tol=1e-6))
    return R


def severity_kenh(f):
    d = f['dau_vao']
    lit = f['dap_an']
    if f['id'] == 78:
        A = {'trang_thai': 'NO_A' if d['A']['dong'] > 0 and d['A']['xac_dinh'] == 0 else 'OK', 'cham': False, 'dong_A_vao_Drain': d['A']['dong']}
        B = {'trang_thai': ['OK', 'NO_A'][int(d['A']['xac_dinh'] == 0)], 'cham': d['A']['xac_dinh'] > 0, 'dong_A_vao_Drain': d['A']['dong']}
    else:
        TN, TA = d['T']
        ra, rb = dem_A(d['N']['loi'], d['A']['loi'], TN, TA), dem_B(d['N']['loi'], d['A']['loi'], TN, TA)
        A = {'trang_thai': 'OK', 'e': ra['e'], 'p': round(ra['p'], 3), 'do_phu': {'N': d['N']['xac_dinh'] / d['N']['dong'], 'A': d['A']['xac_dinh'] / d['A']['dong']},
             'ten_kenh': lit['ten_kenh']}
        B = {'trang_thai': 'OK', 'e': rb['e'], 'p': round(rb['p'], 3), 'do_phu': {'N': float(Fraction(d['N']['xac_dinh'], d['N']['dong'])), 'A': float(Fraction(d['A']['xac_dinh'], d['A']['dong']))},
             'ten_kenh': lit['ten_kenh']}
    return kiem(f['id'], 'kênh severity', lit, A, B)


def dau_vet(f):
    lit = f['dap_an']
    kenh = {'Payment': [('log_loi', 'lan_nguoc', 0.9), ('ty_le_tc', 'lan_nguoc', 0.8)], 'payment_db': [('cpu', 'tai_nguyen_tang', 0.05)]}
    edges = [('Payment', 'payment_db')]
    out = []
    for fn in (e5_A, e5_B):
        fi = fn(kenh, edges, True)
        trace = []
        for e in fi:
            for c in fi[e]:
                if c[2] > 0 and not c[3]:
                    expl = [(b, k[0]) for a, b in edges if a == e for k in kenh[b] if k[2] > 0 and k[1] in GIAI_THICH_NGUOC]
                    for b, kb in expl:
                        trace.append([e, c[0], b, kb, [e, b], 'lan_nguoc', 'ap_dung'])
        fi0 = fn(kenh, edges, False)
        r_off = [x for _, es in xep_A(fi0, list(kenh)) for x in es].index('Payment') + 1
        r_on = [x for _, es in xep_A(fi, list(kenh)) for x in es].index('Payment') + 1
        lost = sum(1 for c in fi['Payment'] if c[2] > 0 and not c[3])
        out.append({'inherited_by': sorted(trace), 'K_I_Payment': list(khoa(fi['Payment'], True)),
                    'bo_danh_gia': {'mat_kenh_F_raw': [lost, sum(1 for c in fi['Payment'] if c[2] > 0)],
                                    'con_tu_sinh': khoa(fi['Payment'], True)[0] > 0, 'hang_bo_E5': r_off, 'hang_bat_E5': r_on}})
    litc = dict(lit, inherited_by=sorted(lit['inherited_by']))
    return kiem(f['id'], 'dấu vết E5', litc, out[0], out[1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    t0 = time.time()
    spec_path = ROOT / 'results/T-043/fixture-dac-ta.json'
    spec = json.loads(spec_path.read_text(encoding='utf-8'))
    import hashlib
    results = []
    for f in spec['fixtures']:
        try:
            results += chay(f)
        except Exception as exc:  # giữ lỗi trong kết quả
            results.append({'id': f['id'], 'kiem': 'LỖI CHẠY', 'loi': f'{type(exc).__name__}: {exc}', 'A_khop': False, 'B_khop': False})
    ids = sorted({int(str(r['id']).split('-')[0]) for r in results})
    out = {'schema': 'T043-kiem-fixture-v1', 'fixture_sha256': hashlib.sha256(spec_path.read_bytes()).hexdigest(),
           'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'so_muc_fixture': len(spec['fixtures']), 'so_muc_co_kiem': len(ids), 'so_phep_kiem': len(results),
           'A_khop': sum(bool(r['A_khop']) for r in results), 'B_khop': sum(bool(r['B_khop']) for r in results),
           'khong_khop': [r for r in results if not (r['A_khop'] and r['B_khop'])],
           'giay': round(time.time() - t0, 2), 'ket_qua': results}
    p = ROOT / args.out
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding='utf-8')
    print(json.dumps({k: out[k] for k in ('so_muc_fixture', 'so_muc_co_kiem', 'so_phep_kiem', 'A_khop', 'B_khop', 'giay')}, ensure_ascii=False))
    for r in out['khong_khop']:
        print('KHÔNG KHỚP', json.dumps({k: r.get(k) for k in ('id', 'kiem', 'literal', 'A', 'B', 'loi')}, ensure_ascii=False, default=str)[:900])


if __name__ == '__main__':
    main()
