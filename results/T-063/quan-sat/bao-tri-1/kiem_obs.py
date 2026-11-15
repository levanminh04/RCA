# Chạy trên exp-obs (python3 - < file): kiểm sau bảo trì lượt 1 — Loki theo service, Tempo span job Keycloak, httpcheck. Chỉ ĐỌC.
import json, time, urllib.parse, urllib.request
now = int(time.time())
def get(u): return json.load(urllib.request.urlopen(u, timeout=30))
q = 'sum by (service_name) (count_over_time({deployment_environment="exp"}[5m]))'
r = get('http://localhost:3100/loki/api/v1/query?' + urllib.parse.urlencode({'query': q, 'time': now}))
print('LOKI dòng/5 phút theo service:', {x['metric'].get('service_name'): x['value'][1] for x in r['data']['result']})
r = get('http://localhost:3200/api/search?' + urllib.parse.urlencode({'tags': 'service.name=keycloak', 'start': now - 600, 'end': now, 'limit': 50}))
names = {}
for t in r.get('traces', []): names[t.get('rootTraceName')] = names.get(t.get('rootTraceName'), 0) + 1
print('TEMPO keycloak root (10 phút):', names)
r = get('http://localhost:9090/api/v1/query?' + urllib.parse.urlencode({'query': 'httpcheck_status{http_status_class="2xx"} or httpcheck_status{http_status_class="4xx"}'}))
print('HTTPCHECK:', sorted({(x['metric'].get('http_url'), x['metric'].get('http_status_class'), x['value'][1]) for x in r['data']['result'] if x['value'][1] == '1'}))
