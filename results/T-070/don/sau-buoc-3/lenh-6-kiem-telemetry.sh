python3 - <<'PY'
import json,urllib.request,urllib.parse,time
def q(u):
    with urllib.request.urlopen(u,timeout=30) as r: return json.load(r)
now=int(time.time())
print('utc',time.strftime('%FT%TZ',time.gmtime()))
r=q('http://127.0.0.1:3100/loki/api/v1/query?'+urllib.parse.urlencode({'query':'sum by (service_name) (count_over_time({service_name=~".+"}[3m]))','time':now*10**9}))['data']['result']
print('loki 3 phut:',sorted((x['metric'].get('service_name'),x['value'][1]) for x in r))
r=q('http://127.0.0.1:9090/api/v1/query?'+urllib.parse.urlencode({'query':'count by (job) (up)','time':now}))['data']['result']
print('prom up theo job:',sorted((x['metric'].get('job'),x['value'][1]) for x in r))
r=q('http://127.0.0.1:3200/api/search?'+urllib.parse.urlencode({'start':now-300,'end':now,'limit':1000}))
print('tempo 5 phut:',len(r.get('traces',[])),'trace')
PY
