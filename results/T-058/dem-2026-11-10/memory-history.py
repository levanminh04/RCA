"""Operator analysis of the failed C3 window; not an agent-overhead A/B test."""
import datetime,json,urllib.parse,urllib.request
from pathlib import Path
queries={
 'heap_used':'sum by(service_name) (jvm_memory_used_bytes{jvm_memory_type="heap"})',
 'non_heap_used':'sum by(service_name) (jvm_memory_used_bytes{jvm_memory_type="non_heap"})',
 'heap_committed':'sum by(service_name) (jvm_memory_committed_bytes{jvm_memory_type="heap"})',
 'non_heap_committed':'sum by(service_name) (jvm_memory_committed_bytes{jvm_memory_type="non_heap"})'}
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'window':['2026-11-10T20:45:00Z','2026-11-10T21:45:00Z'],
        'sampling':'PromQL evaluation grid 15s for descriptive analysis, not source-clock input to M1',
        'limits':['All samples here have the agent attached; no same-host no-agent baseline exists',
                  'Heap used, committed bytes, process RSS and Docker working set have different meanings; do not subtract them as an exact agent overhead',
                  'Historical amd64 host 84 is not accessed and is not a controlled comparison for Oracle ARM'],
        'queries':{}}
for name,q in queries.items():
 url='http://127.0.0.1:9090/api/v1/query_range?'+urllib.parse.urlencode({'query':q,'start':result['window'][0],'end':result['window'][1],'step':15})
 with urllib.request.urlopen(url,timeout=40) as response: data=json.load(response)
 if data['status']!='success': raise SystemExit('Prometheus query failed')
 result['queries'][name]={'query':q,'data':data['data']}
Path('/home/ubuntu/t058/memory-heap-history.json').write_text(json.dumps(result,indent=2)+'\n')
for name,d in result['queries'].items():
 for series in d['data']['result']:
  if series['metric'].get('service_name')=='booking-service':
   values=[float(x[1]) for x in series['values']]
   print(name,'booking min/max MiB',min(values)/1024**2,max(values)/1024**2)
