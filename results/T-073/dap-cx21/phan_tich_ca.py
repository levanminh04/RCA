"""T-073 đáp CX-21 (lượt 19): phân tích một ca 7577dd5b trên file đã chép (results/T-073/e5/ca-7577dd5b/), chỉ đọc, trong RAM.
(1) phủ hai kênh live-down/live-ms sau ánh xạ cổng (cùng hàm lỗ của check_core_input.py bản E5);
(2) H5 _chet_im (chép nguyên logic src/m1_ft/thanh_phan/h4_h5.py) khi GIỮ và BỎ mẫu tại t̂+300, cho mọi chuỗi;
(3) giờ mẫu các nguồn Payment trong prometheus.json (đầu vào cơ sở) quanh pause/gỡ, so với Booking làm đối chứng;
(4) thứ hạng P7, V082 và chú thích H5 đã lưu.
    py -3 -I results/T-073/dap-cx21/phan_tich_ca.py <thư mục ca-7577dd5b>
Không đọc sổ tiêm."""
import datetime
import json
import sys
from pathlib import Path

G = Path(sys.argv[1]) / 'srv/rca-lab/m1'
T = 1795400310
NS = 10**9
CONG = {'8081': 'api-gateway', '8082': 'booking-service', '8083': 'payment-service', '8084': 'ticket-service',
        '8085': 'user-service', '8086': 'event-service', '8761': 'discovery-server', '8080': 'keycloak'}


def hm(x):
    return datetime.datetime.fromtimestamp(float(x), datetime.timezone.utc).strftime('%H:%M:%S')


def lo_lon_nhat(times, lo, hi):  # = check_core_input.py bản E5
    x = sorted(v for v in times if lo <= v < hi)
    if not x:
        return (hi - lo), 0
    gaps = [x[0] - lo, hi - x[-1]] + [b - a for a, b in zip(x, x[1:])]
    return max(gaps), len(x)


def chet_im(series, t, toi_thieu):  # = KenhLiveness._chet_im
    out = {}
    for s in series:
        v = sorted((float(a), float(b)) for a, b in s['values'])
        N = [x for ts, x in v if ts < t]
        A = [(ts, x) for ts, x in v if ts >= t]
        if len(N) < 4 or any(x != 0 for x in N) or not A:
            continue
        i = next((j for j, (_, x) in enumerate(A) if x == 1), None)
        if i is None or any(x != 1 for _, x in A[i:]) or A[-1][0] - A[i][0] < toi_thieu:
            continue
        out[s['metric']['service_name']] = {'tu': A[i][0], 'den': A[-1][0], 'so_mau': len(A) - i}
    return out


def ly_do(s, t):
    v = sorted((float(a), float(b)) for a, b in s['values'])
    N = [x for ts, x in v if ts < t]
    A = [(ts, x) for ts, x in v if ts >= t]
    if len(N) < 4:
        return 'N<4'
    if any(x != 0 for x in N):
        return 'N có mẫu khác 0 lúc ' + ','.join(hm(ts) for ts, x in v if ts < t and x != 0)
    if not A:
        return 'A rỗng'
    i = next((j for j, (_, x) in enumerate(A) if x == 1), None)
    if i is None:
        return 'A không có mẫu 1 (luôn phản hồi)'
    if any(x != 1 for _, x in A[i:]):
        return 'phản hồi lại sau mẫu 1 đầu'
    return 'đạt, đoạn %.0f s' % (A[-1][0] - A[i][0])


ra = {'ca': '7577dd5b', 't_hat': T}
bs = json.loads((G / 'bo-sung/7577dd5b/prometheus-bo-sung.json').read_text(encoding='utf-8'))
ra['goi_bo_sung'] = {'phien_ban': bs['phien_ban'], 'cua_so': bs['cua_so']}
lo, hi = (T - 300) * NS, (T + 300) * NS
phu, gan, bo = {}, {}, []
for ch in ('live-down', 'live-ms'):
    b = next(x for x in bs['bundles'] if x['channel'] == ch)
    gan[ch] = []
    for s in b['result']:
        u = s['metric'].get('http_url') or ''
        cong = u.split('://', 1)[-1].split('/', 1)[0].rsplit(':', 1)[-1]
        sv = CONG.get(cong)
        if not sv:
            bo.append([ch, u])
            continue
        gan[ch].append({'metric': {'service_name': sv}, 'values': s['values']})
        g, n = lo_lon_nhat([int(round(float(a))) * NS for a, _ in s['values']], lo, hi)
        phu[f'{ch}:{sv}'] = {'so_mau_trong_cua_so': n, 'so_mau_ca_chuoi': len(s['values']), 'lo_lon_nhat_s': g / NS,
                             'nguong_lo_s': 60, 'du': n > 0 and g <= 60 * NS,
                             'co_mau_dung_t_hat_cong_300': any(abs(float(a) - (T + 300)) < 1e-6 for a, _ in s['values'])}
ra['live_url_bo'] = bo
ra['phu_live'] = phu
ld = gan['live-down']
bo_bien = [dict(s, values=[v for v in s['values'] if float(v[0]) < T + 300]) for s in ld]
ra['h5'] = {'giu_mau_bien': chet_im(ld, T, 60), 'bo_mau_bien': chet_im(bo_bien, T, 60),
            'ly_do_giu_bien': {s['metric']['service_name']: ly_do(s, T) for s in ld},
            'ly_do_bo_bien': {s['metric']['service_name']: ly_do(s, T) for s in bo_bien}}
pay = next(s for s in ld if s['metric']['service_name'] == 'payment-service')
ra['live_down_payment_tu_t_tru_90'] = [[hm(a), x] for a, x in pay['values'] if float(a) >= T - 90]

prom = json.loads((G / 'cases/7577dd5b/prometheus.json').read_text(encoding='utf-8'))
pv, mau = {}, {}
for b in prom:
    tt = [float(a) for s in b['result'] for a, _ in s['values']]
    if tt:
        pv[b['channel']] = [hm(min(tt)), hm(max(tt)), len(b['result'])]
    for s in b['result']:
        m = s['metric']
        ten = json.dumps(m, sort_keys=True, ensure_ascii=False)
        if 'payment' not in ten and 'booking-service' not in ten:
            continue
        ts = sorted(float(a) for a, _ in s['values'])
        if not ts:
            continue
        trong = [x for x in ts if T - 300 <= x < T + 300]
        kh = [(b2 - a2, a2, b2) for a2, b2 in zip(ts, ts[1:])]
        lon = max(kh) if kh else (0, ts[0], ts[0])
        mau.setdefault(b['channel'], []).append({
            'nhan': m, 'so_mau_ca_goi': len(ts), 'dau': hm(ts[0]), 'cuoi': hm(ts[-1]),
            'so_mau_trong_cua_so_loi': len(trong), 'mau_dau_trong_cua_so': hm(trong[0]) if trong else None,
            'mau_cuoi_trong_cua_so': hm(trong[-1]) if trong else None,
            'khoang_lon_nhat_s': round(lon[0], 3), 'khoang_lon_nhat_tu_den': [hm(lon[1]), hm(lon[2])]})
ra['prometheus_json'] = {'pham_vi_kenh_dau_cuoi_sochuoi': pv, 'payment_va_booking': mau}
# cpu/mem là nguồn native: giờ mẫu thật lấy từ native_timestamps (timestamp(metric)), không theo lưới truy vấn
# (lưới truy vấn giữ giá trị cũ tới 5 phút do staleness của Prometheus).
nat = {}
for b in prom:
    if not b.get('native_timestamps'):
        continue
    for s in b['native_timestamps']:
        m = s['metric']
        if m.get('service_name') not in ('payment-service', 'booking-service'):
            continue
        raw = sorted({float(x) for _, x in s['values']})
        trong = [x for x in raw if T - 300 <= x < T + 300]
        kh = [(b2 - a2, a2, b2) for a2, b2 in zip(raw, raw[1:])]
        lon = max(kh) if kh else (0, raw[0], raw[0])
        nat[f"{b['channel']}:{m.get('service_name')}"] = {
            'so_mau_tho_ca_goi': len(raw), 'dau': hm(raw[0]), 'cuoi': hm(raw[-1]),
            'so_mau_tho_trong_cua_so_loi': len(trong), 'mau_tho_cuoi_trong_cua_so': hm(trong[-1]) if trong else None,
            'khoang_lon_nhat_s': round(lon[0], 3), 'khoang_lon_nhat_tu_den': [hm(lon[1]), hm(lon[2])]}
ra['prometheus_json']['native_cpu_mem'] = nat

v = json.loads((G / 'v082/7577dd5b/method-output-1.json').read_text(encoding='utf-8'))
ra['v082'] = {'entity_ranking': [[r['entity'], r['tie_group']] for r in v['entity_ranking']],
              'chu_thich_H5': v['extra']['m1_ft']['chu_thich'].get('H5-liveness')}
p7 = json.loads((G / 'outputs/7577dd5b/method-output-1.json').read_text(encoding='utf-8'))
ra['p7_entity_ranking'] = [[r['entity'], r['tie_group']] for r in p7['entity_ranking']]
print(json.dumps(ra, ensure_ascii=False, indent=1))
