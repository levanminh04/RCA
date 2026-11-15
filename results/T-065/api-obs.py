"""Chạy qua SSH stdin trên exp-obs. Chỉ đọc cấu hình và gọi API truy vấn.
Không in credential/cookie. Không ghi file hoặc đổi cấu hình trên exp-obs.
"""
import base64
import json
import pathlib
import sys
import re
import time
import urllib.error
import urllib.request

BASE = pathlib.Path('/opt/flash-ticket-obs/pinned')
compose = json.loads((BASE / 'compose.json').read_text())
grafana = compose['services']['grafana']
env = dict(grafana.get('environment') or {})
for file in grafana.get('env_file', []):
    for line in pathlib.Path(file).read_text().splitlines():
        if '=' in line and not line.lstrip().startswith('#'):
            k, v = line.split('=', 1)
            env.setdefault(k.strip(), v.strip().strip('"').strip("'"))
auth = base64.b64encode((env.get('GF_SECURITY_ADMIN_USER', 'admin') + ':' +
                         env['GF_SECURITY_ADMIN_PASSWORD']).encode()).decode()
URL = 'http://10.0.0.215:3000'

def api(endpoint, body=None):
    request = urllib.request.Request(URL + endpoint,
        data=json.dumps(body, ensure_ascii=False).encode() if body is not None else None,
        headers={'Authorization': 'Basic ' + auth, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(request, timeout=65) as response:
            return {'http': response.status, 'data': json.load(response)}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode()
        try:
            raw = json.loads(raw)
        except ValueError:
            pass
        return {'http': exc.code, 'data': raw}

def clean_response(response):
    if isinstance(response, dict):
        for k in list(response):
            # Infinity trả cả tài liệu nguồn trong meta.custom.data, bỏ bản lặp lớn này.
            if k == 'custom' and isinstance(response[k], dict):
                response[k].pop('data', None)
            clean_response(response[k])
    elif isinstance(response, list):
        for item in response:
            clean_response(item)
    return response

def query_panels(panels, variables, window):
    targets = []
    for panel in panels:
        for target in panel.get('targets', []):
            if target.get('hide'):
                continue
            serialized = json.dumps(target, ensure_ascii=False)
            for key, value in variables.items():
                serialized = serialized.replace('${' + key + '}', str(value))
                serialized = serialized.replace('${' + key + ':value}', str(value))
                serialized = serialized.replace('${' + key + ':raw}', str(value))
            target = json.loads(serialized)
            target['refId'] = str(panel['id']) + '_' + target['refId']
            target.update(intervalMs=15000, maxDataPoints=1000)
            targets.append(target)
    request = {'from': str(window[0]), 'to': str(window[1]), 'queries': targets}
    result = api('/api/ds/query', request)
    return {'request': request, 'response': clean_response(result)}

action = sys.argv[1] if len(sys.argv) > 1 else 'inventory'
if action == 'inventory':
    result = {'health': api('/api/health'),
              'datasources': api('/api/datasources'),
              'old_main': api('/api/dashboards/uid/rca-g2'),
              'old_replay': api('/api/dashboards/uid/rca-g2-phat-lai')}
    # API datasources chỉ trả secureJsonFields, nhưng vẫn bỏ mọi khóa có thể mang credential.
    for ds in result['datasources'].get('data', []):
        ds.pop('basicAuthPassword', None)
        ds.pop('password', None)
        ds.pop('user', None)
    print(json.dumps(result, ensure_ascii=False))
elif action in ('verify', 'verify-quick', 'links', 'links-extra'):
    folder = pathlib.Path('/opt/flash-ticket-obs/rca-ket-qua/t065-l3-001')
    provision = BASE / 'provisioning/dashboards'
    dashboards = {uid: json.loads((provision / (uid + '.json')).read_text())
                  for uid in ('t065-rca', 't065-phat-lai')}
    if action in ('verify', 'verify-quick'):
        result = {'dashboard_api': {uid: api('/api/dashboards/uid/' + uid) for uid in dashboards},
                  'cases': {}, 'services': {}, 'variables': {}}
        index = json.loads((folder / 'p7/chi-muc/danh-sach-su-co.json').read_text())
        for sc in index['su_co'][:1] if action == 'verify-quick' else index['su_co']:
            ca = sc['ma']
            case = json.loads((folder / ('p7/' + ca + '.json')).read_text())
            dv = next(n['id'] for n in case['nut'] if n.get('noi_bat'))
            window = [sc['tu'], sc['den']]
            ops = [o for o in case['thao_tac'] if o['chu'] == dv]
            selected = next((o for o in ops if o['co_m1']), ops[0] if ops else {'id': ''})
            variables = {'ban': 'p7', 'ca': ca, 'dv': dv,
                         'dv_svc': {'config-discovery': 'discovery-server'}.get(dv, dv),
                         'op': selected['id'], 't_tu': window[0], 't_den': window[1],
                         't_tu_s': str(window[0] // 1000), 't_den_s': str(window[1] / 1000),
                         't_tu_ns': str(window[0]) + '000000',
                         't_den_ns': str(window[1]) + '999999'}
            result['cases'][ca] = {}
            for uid, d in dashboards.items():
                result['cases'][ca][uid] = query_panels(d['panels'], variables, window)
                variable_panels = [{'id': v['name'], 'targets': [dict(v['query']['infinityQuery'], refId='v')]}
                                   for v in d['templating']['list'] if v.get('type') == 'query']
                result['variables'][ca + '/' + uid] = query_panels(variable_panels, variables, window)
            for node in [] if action == 'verify-quick' else case['nut']:
                svc = node['id']
                operations = [o for o in case['thao_tac'] if o['chu'] == svc]
                selected = next((o for o in operations if o['co_m1']), operations[0] if operations else {'id': ''})
                variables.update(dv=svc, op=selected['id'])
                panels = [p for p in dashboards['t065-rca']['panels'] if p['id'] in (21, 22, 23, 24, 25, 26)]
                result['services'][ca + '/' + svc] = query_panels(panels, variables, window)
        print(json.dumps(result, ensure_ascii=False))
    else:
        # API kiểm link không thay cho phép bấm thật. Mỗi truy vấn chỉ 600 giây.
        result = []
        cases = ('e8661e0a', 'a89954d1', '00eaea92') if action == 'links' else tuple(
            x['ma'] for x in json.loads((folder / 'p7/chi-muc/danh-sach-su-co.json').read_text())['su_co'])
        for ca in cases:
            case = json.loads((folder / ('p7/' + ca + '.json')).read_text())
            if action == 'links-extra':
                chosen = [l for b in case['bang_chung'] for l in b['lien_ket'] if l['kho'] == 'loki']
                correlated = next((l for o in case['thao_tac'] for l in o['lien_ket']
                                   if l['kho'] == 'loki' and l['pham_vi'] == 'trace_tuong_quan'), None)
                if correlated:
                    chosen.append(correlated)
            else:
                chosen = [next(l for o in case['thao_tac'] for l in o['lien_ket'] if l['kho'] == kho)
                          for kho in ('tempo', 'loki', 'prometheus')]
            for lk in chosen:
                kho = lk['kho']
                from urllib.parse import urlparse, parse_qs
                pane = json.loads(parse_qs(urlparse(lk['url']).query)['panes'][0])['a']
                request = {'from': pane['range']['from'], 'to': pane['range']['to'],
                           'queries': [dict(pane['queries'][0], intervalMs=15000, maxDataPoints=1000)]}
                response = api('/api/ds/query', request)
                result.append({'ca': ca, 'kho': kho, 'link': lk, 'request': request,
                               'response': clean_response(response), 'bam_that': False})
        print(json.dumps(result, ensure_ascii=False))
