import json
from pathlib import Path
root=Path(__file__).resolve().parent
rows=[json.loads(x) for x in (root/'memory-after-fix.jsonl').read_text().splitlines()]
names=sorted({c['name'] for r in rows for c in r['containers']})
records={}
for name in names:
 data=[c for r in rows for c in r['containers'] if c['name']==name]
 records[name]={'container_ids':sorted({c['id'] for c in data}),
                'limit_bytes':data[-1]['limit_bytes'],
                'sampled_maximum_cgroup_current_bytes':max(c['memory_current_bytes'] for c in data),
                'sampled_maximum_percent':100*max(c['memory_current_bytes']/c['limit_bytes'] for c in data),
                'maximum_cgroup_oom_kill':max(c['memory_events']['oom_kill'] for c in data),
                'maximum_restart_count':max(c['restart_count'] for c in data),
                'paused_samples':sum(c['paused'] for c in data),
                'maximum_java_rss_kib':max(p['rss_kib'] for c in data for p in c['java_processes'])}
result={'first_utc':rows[0]['utc'],'last_utc':rows[-1]['utc'],'samples':len(rows),
        'sample_span_seconds':rows[-1]['epoch']-rows[0]['epoch'],
        'scope':'Post-fix operator monitor, includes deliberate event pause; not a repeat of full C3 or a no-agent comparison',
        'containers':records}
(root/'memory-after-fix-summary.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
print(result['first_utc'],result['last_utc'],'samples',len(rows),'max oom/restart',max(r['maximum_cgroup_oom_kill'] for r in records.values()),max(r['maximum_restart_count'] for r in records.values()))
for n,r in records.items(): print(n,round(r['sampled_maximum_percent'],2),'paused samples',r['paused_samples'])
