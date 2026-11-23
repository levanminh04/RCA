"""T-073 đáp CX-21 điểm 1 (lượt 19): hàng metric cơ sở mà V082 dựng lại có trùng hàng metric của đầu vào P7 không, và
V082 thêm bao nhiêu hàng/nguồn từ hai kênh H5. Laptop không có numpy nên không import được src/m1_ft/chay.py; dùng
src/m1/adapter_flashticket.py (thuần Python) và CHÉP NGUYÊN thân `dung_lai_metric` (chay.py dòng 100–116) cùng phép ánh xạ
cổng của `KenhLiveness.bien_doi_bundle` (h4_h5.py). Codex CX-21 đã kiểm 59/59 file mã khớp bản chụp b0f79a4d. Một ca, RAM.
    py -3 -I -X utf8 results/T-073/dap-cx21/so_hang_metric.py <thư mục ca-7577dd5b> <gốc repo>"""
import copy
import hashlib
import json
import sys
from pathlib import Path

G = Path(sys.argv[1]) / 'srv/rca-lab/m1'
sys.path.insert(0, str(Path(sys.argv[2]) / 'src'))
from m1 import adapter_flashticket as ad  # noqa: E402

CONG = {'8081': 'api-gateway', '8082': 'booking-service', '8083': 'payment-service', '8084': 'ticket-service',
        '8085': 'user-service', '8086': 'event-service', '8761': 'discovery-server', '8080': 'keycloak'}  # = h4_h5.CONG


def dung_lai_metric(inputs, bundles, kenh_them=None):  # chép nguyên chay.py dòng 100–116
    spans, metrics, logs, inventory, aliases, t, params = inputs
    goc = ad.CHANNELS
    ad.CHANNELS = dict(goc, **(kenh_them or {}))
    try:
        rows, owners, indices, clocks, coverage, m_alias, md = ad.normalize_metrics(bundles, inventory)
    finally:
        ad.CHANNELS = goc
    p = dict(params)
    p['nguon_metric'], p['chi_so_hang_metric'], p['thoi_gian_nguon'] = owners, indices, clocks
    p['coverage'] = {**{k: v for k, v in params['coverage'].items() if not k.startswith('metric:')}, **coverage}
    if kenh_them:
        ho = copy.deepcopy(params['ho_so_nguon'])
        ho['kenh_metric']['bang'] = dict(ho['kenh_metric']['bang'], **kenh_them)
        p['ho_so_nguon'] = ho
    return [spans, rows, logs, inventory, dict(aliases, **m_alias), t, p], md


def anh_xa(bundles):  # = phần ánh xạ của KenhLiveness.bien_doi_bundle
    out, bo = [], 0
    for b in bundles:
        if b['channel'] not in ('live-down', 'live-ms'):
            out.append(b); continue
        gan = []
        for s in b['result']:
            u = s['metric'].get('http_url') or ''
            cong = u.split('://', 1)[-1].split('/', 1)[0].rsplit(':', 1)[-1]
            sv = CONG.get(cong)
            if not sv:
                bo += 1; continue
            gan.append({'metric': {'service_name': sv}, 'values': s['values']})
        out.append(dict(b, result=gan))
    return out, bo


def h(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


raw = (G / 'outputs/7577dd5b/method-input.json').read_bytes()
inputs = json.loads(raw)
prom = json.loads((G / 'cases/7577dd5b/prometheus.json').read_text(encoding='utf-8'))
bs = json.loads((G / 'bo-sung/7577dd5b/prometheus-bo-sung.json').read_text(encoding='utf-8'))
ra = {'method_input_sha256': hashlib.sha256(raw).hexdigest(), 'p7_so_hang_metric': len(inputs[1]),
      'p7_so_nguon_metric': sum(1 for k in inputs[6]['coverage'] if k.startswith('metric:'))}
moi0, _ = dung_lai_metric(inputs, copy.deepcopy(prom), None)
ra['dung_lai_chi_prometheus_json'] = {'so_hang': len(moi0[1]), 'trung_hang_p7': h(moi0[1]) == h(inputs[1]),
                                      'trung_thoi_gian_nguon_p7': h(moi0[6]['thoi_gian_nguon']) == h(inputs[6]['thoi_gian_nguon'])}
km = {'live-down': 'tài nguyên', 'live-ms': 'độ trễ'}  # = KenhLiveness.kenh_moi()
bundles = copy.deepcopy(prom) + [copy.deepcopy(b) for b in bs['bundles'] if b['channel'] in km]
bundles, bo = anh_xa(bundles)
moi, md = dung_lai_metric(inputs, bundles, km)
k = lambda r: json.dumps(r, sort_keys=True, ensure_ascii=False)
s_p7, s_moi = {k(r) for r in inputs[1]}, {k(r) for r in moi[1]}
cov = moi[6]['coverage']
ra['duong_v082'] = {'so_hang': len(moi[1]), 'moi_hang_p7_co_trong_v082': s_p7 <= s_moi, 'so_hang_them': len(s_moi - s_p7),
                    'so_nguon_metric': sum(1 for x in cov if x.startswith('metric:')),
                    'nguon_them': sorted(x for x in cov if x.startswith('metric:') and x not in inputs[6]['coverage']),
                    'nguon_co_so_giu_nguyen_thoi_gian': all(moi[6]['thoi_gian_nguon'].get(x) == inputs[6]['thoi_gian_nguon'].get(x)
                                                            for x in inputs[6]['thoi_gian_nguon']),
                    'chuoi_url_bo': bo, 'unmapped': len(md.get('unmapped_series', [])), 'empty_queries': md.get('empty_queries', [])}
print(json.dumps(ra, ensure_ascii=False, indent=1))
