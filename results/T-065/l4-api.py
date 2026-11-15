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

FOLDER = pathlib.Path('/opt/flash-ticket-obs/rca-ket-qua/t065-l4-001')
PROVISION = BASE / 'provisioning/dashboards'
UIDS = ('t065-l4-rca', 't065-l4-phat-lai')
ACTION = sys.argv[1]


def state(response):
    results = response.get('data', {}).get('results', {})
    errors = [str(r.get('error')) for r in results.values() if r.get('error')]
    rows = sum(max((len(v) for v in f.get('data', {}).get('values', [])), default=0)
               for r in results.values() for f in r.get('frames', []))
    status = 'loi' if response.get('http') != 200 or errors else 'co_du_lieu' if rows else 'rong'
    return status, rows, errors


def variables(case, service):
    ops = [o for o in case['thao_tac'] if o['chu'] == service]
    chosen = next((o for o in ops if o['co_m1']), ops[0] if ops else {'id': ''})
    return {'ban': case['ban']['ban'], 'ca': case['ca'], 'dv': service,
            'dv_svc': {'config-discovery': 'discovery-server'}.get(service, service),
            'op': chosen['id'], 't_tu': case['cua_so_ms'][0], 't_den': case['cua_so_ms'][1] - 1}


dashboards = {uid: json.loads((PROVISION / (uid + '.json')).read_text()) for uid in UIDS}
index = json.loads((FOLDER / 'chi-muc-ban.json').read_text())
if ACTION == 'snapshot':
    # Queries independent of version: same ca/service/window, saved once and shared.
    output = {}
    panels = [p for p in dashboards[UIDS[0]]['panels'] if p['id'] >= 31]
    for ca in index['ban'][0]['cac_ca']:
        case = json.loads((FOLDER / 'p7' / (ca + '.json')).read_text())
        for service in sorted({o['chu'] for o in case['thao_tac']} | {r['entity'] for r in case['ranking_rows']}):
            v = variables(case, service)
            window = [case['cua_so_ms'][0], case['cua_so_ms'][1] - 1]
            try:
                answer = query_panels(panels, v, window)
            except Exception as exc:
                answer = {'request': {'queries': []}, 'response': {'http': 0, 'data': {'results': {}}}}
                print('snapshot query error: ' + ca + '/' + service + ': ' + type(exc).__name__, file=sys.stderr)
            response = answer['response']
            entries = []
            results = response.get('data', {}).get('results', {})
            for p in panels:
                for target in p['targets']:
                    ref = str(p['id']) + '_' + target['refId']
                    single = {'http': response['http'], 'data': {'results': {ref: results.get(ref, {'error': 'missing ref'})}}}
                    status, rows, errors = state(single)
                    entries.append({'panel': p['id'], 'kho': target['datasource']['uid'], 'trang_thai': status,
                                    'so_dong': rows, 'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                                    'tu_utc': case['tu_utc'], 'den_loai_tru': case['den_loai_tru'],
                                    'dien_giai': {'loi': 'Lỗi truy vấn; không diễn giải dữ liệu.',
                                                  'rong': 'Truy vấn thành công, không có dữ liệu khớp trong cửa sổ ở kho hiện tại; chưa xác định nguyên nhân rỗng.',
                                                  'co_du_lieu': 'Có dữ liệu khớp truy vấn trong cửa sổ; số dòng có thể bị giới hạn.'}[status],
                                    'loi': '; '.join(errors),
                                    'request': next((q for q in answer['request']['queries'] if q['refId'] == ref), None)})
            output[ca + '/' + service] = {'queries': entries, 'window': window}
            with (FOLDER / 'api-snapshot-slots.jsonl').open('a') as progress:
                progress.write(json.dumps({'key': ca + '/' + service, 'value': output[ca + '/' + service]}, ensure_ascii=False) + '\n')
    print(json.dumps(output, ensure_ascii=False))
elif ACTION in ('verify', 'quick'):
    result = {'dashboard_api': {u: api('/api/dashboards/uid/' + u) for u in UIDS}, 'cases': {}, 'variables': {}, 'services': {}}
    cache_path = FOLDER / 'api-verify-slots-v3.jsonl'
    cache = {}
    if cache_path.exists() and ACTION == 'verify':
        for line in cache_path.read_text().splitlines():
            saved = json.loads(line)
            cache[saved['key']] = saved['value']
    for variant in index['ban']:
        ban = variant['ban']
        for ca in variant['cac_ca'][:1] if ACTION == 'quick' else variant['cac_ca']:
            case = json.loads((FOLDER / ban / (ca + '.json')).read_text())
            service = next((r['entity'] for r in case['ranking_rows'] if any(o['chu'] == r['entity'] for o in case['thao_tac'])), case['ranking_rows'][0]['entity'])
            v = variables(case, service)
            window = [case['cua_so_ms'][0], case['cua_so_ms'][1] - 1]
            key = ban + '/' + ca
            result['cases'][key] = {}
            for uid, d in dashboards.items():
                slot = key + '/' + uid
                if slot in cache:
                    result['cases'][key][uid] = cache[slot]['case']
                    result['variables'][slot] = cache[slot]['variables']
                    continue
                # Live queries already verified by snapshot; do not repeat 5 queries for every variant.
                result['cases'][key][uid] = query_panels([p for p in d['panels'] if p['id'] < 31], v, window)
                vp = [{'id': var['name'], 'targets': [dict(var['query']['infinityQuery'], refId='v')]}
                      for var in d['templating']['list'] if var['type'] == 'query']
                result['variables'][slot] = query_panels(vp, v, window)
                if ACTION == 'verify':
                    with cache_path.open('a') as progress:
                        progress.write(json.dumps({'key': slot, 'value': {'case': result['cases'][key][uid], 'variables': result['variables'][slot]}}, ensure_ascii=False) + '\n')
    print(json.dumps(result, ensure_ascii=False))
elif ACTION == 'links':
    from urllib.parse import urlparse, parse_qs
    result = []
    # Three original regression cases plus three dev2 cases, for every version.
    cases = ('e8661e0a', 'a89954d1', '00eaea92', 'eb48d6b3', '4af494a5', '19b17e22')
    for variant in index['ban']:
        for ca in cases:
            case = json.loads((FOLDER / variant['ban'] / (ca + '.json')).read_text())
            links = [l for o in case['thao_tac'] for l in o['lien_ket']] + case['metric_links']
            for kho in ('tempo', 'loki', 'prometheus'):
                lk = next(l for l in links if l['kho'] == kho)
                pane = json.loads(parse_qs(urlparse(lk['url']).query)['panes'][0])['a']
                request = {'from': pane['range']['from'], 'to': pane['range']['to'],
                           'queries': [dict(pane['queries'][0], intervalMs=15000, maxDataPoints=1000)]}
                response = clean_response(api('/api/ds/query', request))
                status, rows, errors = state(response)
                result.append({'ban': variant['ban'], 'ca': ca, 'kho': kho, 'link': lk, 'request': request,
                               'response': response, 'trang_thai': status, 'so_dong': rows, 'loi': errors, 'bam_that': False})
    print(json.dumps(result, ensure_ascii=False))
