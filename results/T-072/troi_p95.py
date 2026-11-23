# -*- coding: utf-8 -*-
"""T-072 — mô tả trôi p95 payment/ticket E2 → E4 (chỉ dữ liệu đã xuất; không Prometheus, không SSH).

Nguồn (đã kiểm hash theo manifest T-071 và SHA256SUMS T-072):
  e2/ra/ra/xuat/<tag>/chuoi/tho__gw-bucket.json.gz, e4/ra/ra/... (counter bucket thô, mỗi 10 s)
  e2/xuat, e4/xuat (*.t072.json: tin-hieu/t072-p95-*, phu/tong-*), e2/phut.json, e4/phut.json
  e2/ra/ra/luot/<tag>/run.json|state.json (giờ lượt), k6-phut.json (request/phút)
Đầu ra: troi-p95-e2-e4.json.
Phép tính:
  A. Theo lượt: phân bố thời gian request của route trong [StartedAt, FinishedAt] (tăng của counter bucket, cộng mọi
     chuỗi nhãn; giảm = reset → lấy giá trị sau), tỷ lệ request > 0,1 / > 0,25 / > 0,5 s, p50/p95/p99 nội suy bucket.
  B. Theo cửa sổ 5 phút trong phút khỏe ×1 (bước 10 s): S(t) = p95 duy trì 60 s (như quy tắc chọn ngưỡng); tần suất
     S > 0,7θ / 0,84θ / θ; số đợt vượt (đợt = chuỗi bước liên tiếp vượt); trên đỉnh: số request trong cửa sổ và số
     request > 0,1 s (đếm từ bucket).
  C. Độ phân tán: số request > 0,1 s trong các cửa sổ 5 phút rời nhau so với Poisson cùng trung bình (chỉ số phân tán).
"""
import gzip, json, glob, math, pathlib, collections, datetime as dt
G = pathlib.Path(__file__).parent
ROUTES = ['payment', 'ticket', 'booking', 'event']
NG = json.loads((G / 'nguong.json').read_text(encoding='utf-8'))['nguong']


def ep(s):
    s = s.replace('Z', '')
    a, _, f = s.partition('.')
    return dt.datetime.fromisoformat(a + '+00:00').timestamp() + (float('0.' + f) if f else 0)


def tai_bucket(f):
    """{route: {le: [(t, v_cum)] gộp theo chuỗi}} — trả list chuỗi, mỗi chuỗi (route, le, [(t, v)])."""
    d = json.load(gzip.open(f, 'rt', encoding='utf-8'))
    out = []
    for x in d['result']:
        m = x['metric']
        out.append((m['http_route'], m['le'], [(float(t), float(v)) for t, v in x['values']]))
    return out


def tang(vals, a, b):
    """Tăng của counter trong (a, b]: cộng các bước dương, reset (giảm) → cộng giá trị sau reset."""
    pts = [(t, v) for t, v in vals if a - 15 <= t <= b]
    s = 0.0
    for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
        if t1 <= a:
            continue
        s += v1 - v0 if v1 >= v0 else v1
    return s


def phan_bo(series, route, a, b):
    le = collections.defaultdict(float)
    for r, l, vals in series:
        if r == route:
            le[l] += tang(vals, a, b)
    mocs = sorted((float('inf') if k == '+Inf' else float(k), v) for k, v in le.items())
    return mocs


def quantile(mocs, q):
    n = mocs[-1][1] if mocs else 0
    if n <= 0:
        return None
    r = q * n
    prev_b, prev_c = 0.0, 0.0
    for b, c in mocs:
        if c >= r:
            if b == float('inf'):
                return prev_b
            return prev_b + (b - prev_b) * ((r - prev_c) / (c - prev_c) if c > prev_c else 0)
        prev_b, prev_c = b, c
    return prev_b


def ty_le_tren(mocs, x):
    n = mocs[-1][1] if mocs else 0
    c = dict(mocs).get(x)
    return None if not n or c is None else round(1 - c / n, 5)


def dem_tren(series, route, a, b, x=0.1):
    m = phan_bo(series, route, a, b)
    n = m[-1][1] if m else 0
    c = dict(m).get(x, 0)
    return n, n - c


out = {'luot': [], 'cua_so': {}, 'phan_tan': {}}
for E in ('e2', 'e4'):
    ph = json.loads((G / E / 'phut.json').read_text(encoding='utf-8'))
    lop = {a: l for a, b, l in ph['khoang']}
    sig = {}
    for f in sorted(glob.glob(str(G / E / 'xuat' / '*.t072.json'))):
        d = json.loads(open(f, encoding='utf-8').read())
        for ten in [f'tin-hieu/t072-p95-{r}' for r in ROUTES] + [f'phu/tong-{r}' for r in ROUTES]:
            for x in d['chuoi'].get(ten, []):
                sig.setdefault(ten, {}).update({int(t): float(v) for t, v in x['values']})
    buckets = {}
    for tagdir in sorted(glob.glob(str(G / E / 'ra' / 'ra' / 'luot' / '*'))):
        tag = pathlib.Path(tagdir).name
        st = json.load(open(pathlib.Path(tagdir) / 'state.json'))
        a, b = ep(st['StartedAt']), ep(st['FinishedAt'])
        series = tai_bucket(G / E / 'ra' / 'ra' / 'xuat' / tag / 'chuoi' / 'tho__gw-bucket.json.gz')
        buckets[tag] = (a, b, series)
        rec = {'khoang': E, 'tag': tag, 'bat_dau': st['StartedAt'][:19] + 'Z', 'giay': round(b - a), 'route': {}}
        for r in ROUTES:
            m = phan_bo(series, r, a, b)
            n = m[-1][1] if m else 0
            rec['route'][r] = {'request': n, 'req_moi_5ph': round(n / (b - a) * 300, 1),
                               'p50': quantile(m, .5), 'p95': quantile(m, .95), 'p99': quantile(m, .99),
                               'ty_le_tren_0_1': ty_le_tren(m, 0.1), 'ty_le_tren_0_25': ty_le_tren(m, 0.25), 'ty_le_tren_0_5': ty_le_tren(m, 0.5)}
        out['luot'].append(rec)
    # B: cửa sổ trong phút khỏe ×1
    for r in ROUTES:
        th = NG[f'theta_p95_{r}']
        d = sig.get(f'tin-hieu/t072-p95-{r}', {})
        steps = sorted(t for t in d if lop.get(t // 60 * 60) == 'khoe-x1')
        S = {}
        for t in steps:
            w = [d.get(u) for u in range(t - 60, t + 1, 10)]
            if all(v is not None for v in w):
                S[t] = min(w)
        o = {'buoc': len(S)}
        for k in (0.5, 0.7, 0.84, 1.0):
            vt = sorted(t for t, v in S.items() if v > k * th)
            dot = sum(1 for i, t in enumerate(vt) if i == 0 or t - vt[i - 1] > 10)
            o[f'vuot_{k}'] = {'buoc': len(vt), 'ty_le': round(len(vt) / len(S), 5) if S else None, 'dot': dot}
        if S:
            tmax = max(S, key=S.get)
            tag = next((tg for tg, (a, b, _) in buckets.items() if a <= tmax <= b), None)
            n, cham = (dem_tren(buckets[tag][2], r, tmax - 300, tmax) if tag else (None, None))
            o['dinh'] = {'t': dt.datetime.fromtimestamp(tmax, dt.timezone.utc).isoformat()[:19] + 'Z', 'S': S[tmax], 'S_tren_nguong': round(S[tmax] / th, 3),
                         'luot': tag, 'request_5ph': n, 'request_tren_0_1s_5ph': cham, 'tong_5ph_chuoi_phu': sig.get(f'phu/tong-{r}', {}).get(tmax)}
            # S theo vị trí trong lượt (phút từ đầu lượt): đỉnh có dồn vào đầu lượt không?
            vt = collections.Counter()
            for t, v in S.items():
                if v > 0.7 * th:
                    tg = next((g for g, (a, b, _) in buckets.items() if a <= t <= b), None)
                    if tg:
                        vt[int((t - buckets[tg][0]) // 600) * 10] += 1
            o['vuot_0_7_theo_phut_trong_luot'] = dict(sorted(vt.items()))
        out['cua_so'][f'{E}|{r}'] = o
        # C: phân tán số request chậm trong cửa sổ 5 phút rời nhau (chỉ phút khỏe ×1)
        dem = []
        for tg, (a, b, series) in buckets.items():
            t = a - a % 300 + 300
            while t + 300 <= b:
                if all(lop.get(m) == 'khoe-x1' for m in range(int(t), int(t + 300), 60)):
                    n, c = dem_tren(series, r, t, t + 300)
                    dem.append((n, c))
                t += 300
        if dem:
            cs = [c for n, c in dem]
            mu = sum(cs) / len(cs); var = sum((c - mu) ** 2 for c in cs) / max(len(cs) - 1, 1)
            out['phan_tan'][f'{E}|{r}'] = {'so_cua_so': len(cs), 'request_tb': round(sum(n for n, c in dem) / len(dem), 1),
                                          'cham_tb': round(mu, 3), 'cham_var': round(var, 3), 'chi_so_phan_tan': round(var / mu, 3) if mu else None,
                                          'cham_max': max(cs), 'p_poisson_ge_max': round(1 - sum(math.exp(-mu) * mu ** k / math.factorial(k) for k in range(int(max(cs)))), 6) if mu else None}
(G / 'troi-p95-e2-e4.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('ok')
