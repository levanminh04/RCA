# -*- coding: utf-8 -*-
"""REVIEW-4 R9 (Minh duyệt 15/11/2026 "Duyệt cả ba"; WHY-99). Chạy trên exp-obs. Đọc gói bổ sung cũ của ca ebd5ef38 ở 6 mốc,
dựng lại RIÊNG bundle `live-down` theo "lần dò mới nhất" từ mẫu thô (cùng cách với so_live_down_2.py), giữ nguyên mọi bundle
khác, ghi gói MỚI vào /opt/rca-m1ft/out/r9-bo-sung/d<D>/ebd5ef38/prometheus-bo-sung.json (không ghi đè gói cũ, không ghi đè
gói mới đã có). Chỉ đọc Prometheus.
Dùng: ssh exp-obs 'python3 -' < xuat_live_down_moi.py"""
import hashlib, json, os, sys, urllib.parse, urllib.request
B = 'http://localhost:9090/api/v1/'
CA = 'ebd5ef38'
NGUON = {0: f'/opt/rca-m1ft/bo-sung-dev3/{CA}/prometheus-bo-sung.json'}
NGUON.update({d: f'/opt/rca-m1ft/out/l5-bo-sung-dt/d{d}/{CA}/prometheus-bo-sung.json' for d in (-60, -30, -15, 15, 30)})
RA = '/opt/rca-m1ft/out/r9-bo-sung/d{d}/' + CA + '/prometheus-bo-sung.json'
MO_TA = ('live-down theo lần dò mới nhất (WHY-99): 1 nếu kết quả dò gần nhất trong 5 phút trước bước là lỗi (mẫu thô '
         'httpcheck_error = 1), 0 nếu là phản hồi (mẫu thô httpcheck_status = 1); dựng từ range vector, bước 15 s')


def tho(ten, E, rong):
    u = B + 'query?' + urllib.parse.urlencode({'query': f'{ten}[{rong}s]', 'time': E})
    r = json.load(urllib.request.urlopen(u, timeout=60)); assert r['status'] == 'success'
    out = {}
    for s in r['data']['result']:
        out.setdefault(s['metric'].get('http_url', ''), []).extend(float(a) for a, v in s['values'] if float(v) == 1)
    return out


def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()


bao = []
for d, f in sorted(NGUON.items()):
    doc = json.load(open(f, encoding='utf-8')); S, E = doc['cua_so']
    rong = int(E - S + 300)
    err, ok = tho('httpcheck_error', E, rong), tho('httpcheck_status', E, rong)
    bi = [i for i, b in enumerate(doc['bundles']) if b['channel'] == 'live-down']; assert len(bi) == 1
    b = doc['bundles'][bi[0]]
    moi_res = []
    for x in b['result']:
        url = x['metric'].get('http_url', '')
        ev = sorted([(ts, 1) for ts in err.get(url, [])] + [(ts, 0) for ts in ok.get(url, [])])
        vals = []
        for t0, _ in x['values']:
            s = float(t0)
            truoc = [v for ts, v in ev if s - 300 < ts <= s]
            if truoc:
                vals.append([t0, str(truoc[-1])])
        moi_res.append({'metric': x['metric'], 'values': vals})
    doc['bundles'][bi[0]] = dict(b, query=MO_TA, result=moi_res)
    doc['phien_ban'] = 'T064-r9-live-down-1'
    doc['nguon_r9'] = {'goi_cu': f, 'goi_cu_sha256': sha(f), 'ghi_chu': 'chỉ bundle live-down đổi; WHY-99'}
    ra = RA.format(d=d)
    assert not os.path.exists(ra), ra
    os.makedirs(os.path.dirname(ra), exist_ok=True)
    open(ra, 'w', encoding='utf-8').write(json.dumps(doc, ensure_ascii=False, separators=(',', ':')) + '\n')
    lech = sum(1 for a, c in zip(b['result'], moi_res) for p, q in zip(a['values'], c['values']) if p != q) + \
        sum(abs(len(a['values']) - len(c['values'])) for a, c in zip(b['result'], moi_res))
    bao.append({'d': d, 'goi_cu': f, 'goi_cu_sha256': sha(f), 'goi_moi': ra, 'goi_moi_sha256': sha(ra), 'diem_lech': lech})
json.dump(bao, sys.stdout, ensure_ascii=False, indent=1)
