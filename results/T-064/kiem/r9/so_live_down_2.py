# -*- coding: utf-8 -*-
"""REVIEW-4 R9 — phép kiểm CHỈ ĐỌC thứ hai (sau so_live_down.py: biểu thức max_over_time[15s] làm mất cả ca PAUSE-PAYMENT
thật, vì khi request treo đầu dò chỉ ghi lỗi mỗi ~30 s). Ngữ nghĩa ứng viên: live-down tại bước s = 1 nếu lần dò MỚI NHẤT
có kết quả trước s là lỗi (mẫu thô httpcheck_error có giá trị 1), = 0 nếu là phản hồi (mẫu thô httpcheck_status = 1, mọi mã);
chưa có lần dò nào trong 5 phút trước s thì bỏ điểm. Dựng từ mẫu thô (range vector) cùng cửa sổ/bước 15 s; áp lại
`_chet_im` (60 s). Không ghi máy. Dùng: ssh exp-obs 'python3 -' < so_live_down_2.py > so-live-down-2.json"""
import glob, json, sys, urllib.parse, urllib.request
B = 'http://localhost:9090/api/v1/'
CONG = {'8081': 'api-gateway', '8082': 'booking-service', '8083': 'payment-service', '8084': 'ticket-service',
        '8085': 'user-service', '8086': 'event-service', '8761': 'discovery-server', '8080': 'keycloak'}
GOI = (sorted(glob.glob('/opt/rca-m1ft/bo-sung-dev2/*/prometheus-bo-sung.json')) + sorted(glob.glob('/opt/rca-m1ft/bo-sung-dev3/*/prometheus-bo-sung.json'))
       + sorted(glob.glob('/opt/rca-m1ft/bo-sung/*/prometheus-bo-sung.json')) + sorted(glob.glob('/opt/rca-m1ft/out/l5-bo-sung-dt/d*/*/prometheus-bo-sung.json'))
       + sorted(glob.glob('/opt/rca-m1ft/out/pc-bo-sung-dt/d*/*/prometheus-bo-sung.json')))
def tho(q, E, rong):
    u = B + 'query?' + urllib.parse.urlencode({'query': f'{q}[{rong}s]', 'time': E})
    r = json.load(urllib.request.urlopen(u, timeout=60)); assert r['status'] == 'success'
    out = {}
    for s in r['data']['result']:
        out.setdefault(s['metric'].get('http_url', ''), []).extend((float(a), float(v)) for a, v in s['values'] if float(v) == 1)
    return out
def sv(url): return CONG.get(url.split('://', 1)[-1].split('/', 1)[0].rsplit(':', 1)[-1])
def chet_im(series, t, toi_thieu=60.0):
    out = {}
    for url, d in series.items():
        if not sv(url): continue
        v = sorted(d.items()); N = [x for ts, x in v if ts < t]; A = [(ts, x) for ts, x in v if ts >= t]
        if len(N) < 4 or any(x != 0 for x in N) or not A: continue
        i = next((j for j, (_, x) in enumerate(A) if x == 1), None)
        if i is None or any(x != 1 for _, x in A[i:]) or A[-1][0] - A[i][0] < toi_thieu: continue
        out[sv(url)] = {'url': url, 'tu': A[i][0], 'den': A[-1][0], 'so_mau': len(A) - i}
    return out
kq = []
for f in GOI:
    doc = json.load(open(f, encoding='utf-8')); t = float(doc['t']); S, E = doc['cua_so']
    b = next((x for x in doc['bundles'] if x['channel'] == 'live-down'), None)
    if b is None: kq.append({'goi': f, 'khong_co_live_down': True}); continue
    cu = {x['metric'].get('http_url', ''): {float(a): float(c) for a, c in x['values']} for x in b['result']}
    rong = int(E - S + 300)
    err = tho('httpcheck_error', E, rong); ok = tho('httpcheck_status', E, rong)
    moi = {}
    for url in set(cu):
        ev = sorted([(ts, 1.0) for ts, _ in err.get(url, [])] + [(ts, 0.0) for ts, _ in ok.get(url, [])])
        d = {}
        for s in sorted(cu[url]):
            truoc = [x for x in ev if x[0] <= s and x[0] > s - 300]
            if truoc: d[s] = truoc[-1][1]
        moi[url] = d
    lech = {u: sum(1 for s in set(cu[u]) | set(moi[u]) if cu[u].get(s) != moi[u].get(s)) for u in cu}
    a, c = chet_im(cu, t), chet_im(moi, t)
    kq.append({'goi': f, 't': t, 'diem_lech_theo_url': {u: n for u, n in lech.items() if n}, 'chet_im_cu': a, 'chet_im_moi': c, 'doi_chet_im': sorted(a) != sorted(c)})
json.dump({'ngu_nghia': 'lan do moi nhat', 'so_goi': len(GOI), 'ket_qua': kq}, sys.stdout, ensure_ascii=False, indent=1)
