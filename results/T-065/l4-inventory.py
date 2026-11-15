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


result = {}
for uid in ('rca-g2', 'rca-g2-phat-lai', 't065-rca', 't065-phat-lai', 't065-l4-rca', 't065-l4-phat-lai'):
    a = api('/api/dashboards/uid/' + uid)
    result[uid] = {'http': a['http'], 'version': a.get('data', {}).get('dashboard', {}).get('version'), 'folder': a.get('data', {}).get('meta', {}).get('folderTitle')}
print(json.dumps(result))
