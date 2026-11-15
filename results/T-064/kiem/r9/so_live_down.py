# -*- coding: utf-8 -*-
"""REVIEW-4 R9 — phép kiểm CHỈ ĐỌC trên exp-obs: kênh `live-down` đã lưu trong các gói bổ sung (biểu thức T-063
`max by(http_url)(httpcheck_error) or (0 * ...)`, giữ mẫu cũ trong lookback) so với biểu thức chỉ dùng mẫu mới
`max by(http_url)(max_over_time(httpcheck_error[15s])) or (0 * max by(http_url)(httpcheck_duration_milliseconds))`,
cùng cửa sổ/bước/khúc. Áp lại đúng logic `_chet_im` (src/m1_ft/thanh_phan/h4_h5.py, ngưỡng 60 s) lên cả hai để biết
slot nào đổi kết luận chết im. Không ghi gì lên máy; in JSON ra stdout.
Dùng: ssh exp-obs 'python3 -' < so_live_down.py > so-live-down.json"""
import glob, json, os, sys, time, urllib.parse, urllib.request

B = 'http://localhost:9090/api/v1/'
Q_MOI = 'max by(http_url) (max_over_time(httpcheck_error[15s])) or (0 * max by(http_url) (httpcheck_duration_milliseconds))'
CONG = {'8081': 'api-gateway', '8082': 'booking-service', '8083': 'payment-service', '8084': 'ticket-service',
        '8085': 'user-service', '8086': 'event-service', '8761': 'discovery-server', '8080': 'keycloak'}
GOI = (sorted(glob.glob('/opt/rca-m1ft/bo-sung-dev2/*/prometheus-bo-sung.json')) + sorted(glob.glob('/opt/rca-m1ft/bo-sung-dev3/*/prometheus-bo-sung.json'))
       + sorted(glob.glob('/opt/rca-m1ft/bo-sung/*/prometheus-bo-sung.json')) + sorted(glob.glob('/opt/rca-m1ft/out/l5-bo-sung-dt/d*/*/prometheus-bo-sung.json'))
       + sorted(glob.glob('/opt/rca-m1ft/out/pc-bo-sung-dt/d*/*/prometheus-bo-sung.json')))


def q_range(q, s, e, step):
    u = B + 'query_range?' + urllib.parse.urlencode({'query': q, 'start': s, 'end': e, 'step': step})
    r = json.load(urllib.request.urlopen(u, timeout=60))
    assert r.get('status') == 'success', str(r)[:200]
    return r['data']['result']


def lay(q, S, E, step=15, khuc=600):
    gop, s = {}, S
    while s <= E:
        e = min(E, s + khuc - step)
        for x in q_range(q, s, e, step):
            g = gop.setdefault(x['metric'].get('http_url', ''), {})
            for t0, v in x['values']:
                g.setdefault(float(t0), float(v))
        s = e + step
        time.sleep(0.2)
    return gop


def sv(url):
    return CONG.get(url.split('://', 1)[-1].split('/', 1)[0].rsplit(':', 1)[-1])


def chet_im(series, t, toi_thieu=60.0):
    out = {}
    for url, d in series.items():
        if not sv(url):
            continue
        v = sorted(d.items())
        N = [x for ts, x in v if ts < t]; A = [(ts, x) for ts, x in v if ts >= t]
        if len(N) < 4 or any(x != 0 for x in N) or not A:
            continue
        i = next((j for j, (_, x) in enumerate(A) if x == 1), None)
        if i is None or any(x != 1 for _, x in A[i:]) or A[-1][0] - A[i][0] < toi_thieu:
            continue
        out.setdefault(sv(url), []).append({'url': url, 'tu': A[i][0], 'den': A[-1][0], 'so_mau': len(A) - i})
    return out


kq = []
for f in GOI:
    doc = json.load(open(f, encoding='utf-8'))
    t = float(doc['t']); S, E = doc['cua_so']
    b = next((x for x in doc['bundles'] if x['channel'] == 'live-down'), None)
    if b is None:
        kq.append({'goi': f, 't': t, 'khong_co_live_down': True}); continue
    cu = {x['metric'].get('http_url', ''): {float(a): float(c) for a, c in x['values']} for x in b['result']}
    try:
        moi = lay(Q_MOI, S, E)
    except Exception as ex:
        kq.append({'goi': f, 'loi': repr(ex)[:200]}); continue
    lech = {}
    for url in set(cu) | set(moi):
        a, c = cu.get(url, {}), moi.get(url, {})
        n = sum(1 for ts in set(a) | set(c) if a.get(ts) != c.get(ts))
        if n:
            lech[url] = n
    ci_cu, ci_moi = chet_im(cu, t), chet_im(moi, t)
    kq.append({'goi': f, 't': t, 'so_url_cu': len(cu), 'so_url_moi': len(moi), 'diem_lech_theo_url': lech,
               'chet_im_cu': ci_cu, 'chet_im_moi': ci_moi, 'doi_chet_im': sorted(ci_cu) != sorted(ci_moi)})
json.dump({'q_moi': Q_MOI, 'so_goi': len(GOI), 'ket_qua': kq}, sys.stdout, ensure_ascii=False, indent=1)
