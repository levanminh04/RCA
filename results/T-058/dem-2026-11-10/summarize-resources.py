"""Summarize preserved samples; no queries or writes to either Oracle host."""
from collections import defaultdict
import datetime
import json
from pathlib import Path
import re
import statistics

ROOT=Path(__file__).resolve().parent

def size(value):
    match=re.fullmatch(r'([0-9.]+)\s*([A-Za-z]*)',value.strip())
    if not match: raise ValueError('Unrecognized Docker memory size: '+value)
    factors={'B':1,'kB':1000,'MB':10**6,'GB':10**9,'KiB':1024,'MiB':1024**2,'GiB':1024**3}
    return float(match[1])*factors[match[2]]

def counters(row):
    result={}
    for line in row['collector_counters']:
        if line.startswith('UNAVAILABLE'): continue
        key,value=line.rsplit(' ',1)
        result[key]=float(value)
    return result

def window(data):
    # Each host CPU value describes the interval ending at that sample. The
    # first endpoint belongs to the preceding window and is not averaged twice.
    cpu=[x['cpu_percent'] for x in data[1:] if x['cpu_percent'] is not None]
    by_container=defaultdict(list)
    for row in data:
        for item in row['docker_stats']: by_container[item['Name']].append(item)
    containers={}
    for name,items in sorted(by_container.items()):
        usage=[size(x['MemUsage'].split('/')[0]) for x in items]
        cpu_values=[float(x['CPUPerc'].rstrip('%')) for x in items]
        containers[name]={'samples':len(items),'cpu_mean_percent_one_core':statistics.mean(cpu_values),
                          'cpu_max_percent_one_core':max(cpu_values),'memory_mean_bytes':statistics.mean(usage),
                          'memory_max_bytes':max(usage)}
    all_counters=[counters(row) for row in data]
    metrics={}
    for key in sorted(set().union(*(set(x) for x in all_counters))):
        points=[(i,x[key]) for i,x in enumerate(all_counters) if key in x]
        values=[x[1] for x in points]
        is_queue='queue_size' in key
        resets=sum(b<a for a,b in zip(values,values[1:]))
        # A reset prevents a raw last-first delta from representing this window.
        metrics[key]={'first':values[0],'last':values[-1],'max':max(values),'samples':len(points),
                      'missing_samples':len(data)-len(points),'resets':resets,
                      'delta':None if is_queue or resets or len(points)!=len(data) else values[-1]-values[0]}
    first={x['name']:x for x in data[0]['containers']}
    last={x['name']:x for x in data[-1]['containers']}
    restarts={name:last[name]['restart_count']-first[name]['restart_count'] for name in first.keys()&last.keys()}
    seconds=data[-1]['epoch']-data[0]['epoch']
    growth=data[-1]['telemetry_storage_bytes']-data[0]['telemetry_storage_bytes']
    return {'samples':len(data),'first_utc':data[0]['utc'],'last_utc':data[-1]['utc'],'actual_seconds':seconds,
            'cpu_mean_percent_machine':statistics.mean(cpu),'cpu_max_percent_machine':max(cpu),
            'minimum_memory_available_bytes':min(x['memory_available_bytes'] for x in data),
            'minimum_memory_available_percent':min(x['memory_available_percent'] for x in data),
            'maximum_root_used_bytes':max(x['root_used_bytes'] for x in data),
            'storage_first_bytes':data[0]['telemetry_storage_bytes'],'storage_last_bytes':data[-1]['telemetry_storage_bytes'],
            'telemetry_storage_growth_bytes':growth,'telemetry_decimal_gb_per_hour':growth/1e9*3600/seconds,
            'container_resources':containers,'collector_counter_series':metrics,
            'collector_unavailable_samples':sum(any(x.startswith('UNAVAILABLE') for x in r['collector_counters']) for r in data),
            'oom_seen':any(s['oom_killed'] for r in data for s in r['containers']),
            'restart_deltas':restarts,'first_container_states':data[0]['containers'],'last_container_states':data[-1]['containers']}

result={'scope':'C3 shortened by STEER #3: 30 min idle + 30 min fixed 1 request/s, not SPEC 1h + 1h',
        'limitations':['Oracle ARM with actual RAM below; not a test of the SPEC 8 GiB machines',
                       'Host CPU uses all machine CPUs; Docker 100% uses one logical CPU',
                       'Storage growth includes OTLP capture/queues and backend data, not steady-state retention capacity',
                       'Exporter send_failed counts failed attempts and retries; it is not a count of permanently lost items',
                       'Collector counters do not measure SDK sampling or items dropped before the Collector',
                       'Shared boundary sample at 21:15Z is included in both windows for endpoint deltas; CPU uses only intervals ending after each start',
                       'Docker stats is a short asynchronous sweep after the recorded host timestamp, not an atomic sample of all containers',
                       'State.OOMKilled may become false after automatic restart; authoritative kernel OOM events are included separately'],
        'hosts':{}}
oom_evidence=json.loads((ROOT/'unplanned-oom.json').read_text(encoding='utf8'))
kernel_events=[]
for line in oom_evidence['kernel_evidence'].splitlines():
    match=re.match(r'Nov 10 ([0-9:]+).*oom-kill:constraint=CONSTRAINT_MEMCG',line)
    if match:
        when=datetime.datetime.fromisoformat('2026-11-10T'+match[1]+'+00:00')
        kernel_events.append({'utc':when.isoformat(),'epoch':when.timestamp(),'container':oom_evidence['container'],'limit_bytes':oom_evidence['limit_bytes'],'scope':'container memory cgroup','source':'unplanned-oom.json#/kernel_evidence'})
result['authoritative_kernel_oom_events']=kernel_events
for role in ['app','obs']:
    data=[json.loads(line) for line in (ROOT/f'resources-30m-{role}.jsonl').read_text().splitlines()]
    planned=json.loads((ROOT/f'resources-30m-{role}-summary.json').read_text())
    start=planned['planned_start']; half=planned['window_seconds']
    result['hosts'][role]={'memory_total_bytes':data[0]['memory_total_bytes'],'sample_count':len(data),
                          'storage_paths':planned['storage_paths'],'windows':{}}
    for name,lo,hi in [('idle',start,start+half),('light_load',start+half,start+2*half)]:
        w=window([r for r in data if lo<=r['scheduled_epoch']<=hi])
        w['kernel_oom_events']=[x for x in kernel_events if role=='app' and lo<=x['epoch']<hi]
        w['stability_passed']=not(w['oom_seen'] or w['kernel_oom_events'] or any(n!=0 for n in w['restart_deltas'].values()))
        result['hosts'][role]['windows'][name]=w
(ROOT/'so-do-tai-nguyen.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf8')
for role,host in result['hosts'].items():
    for phase,w in host['windows'].items():
        errors={key:val['delta'] for key,val in w['collector_counter_series'].items() if any(x in key for x in ['refused','failed'])}
        print(role,phase,round(w['cpu_mean_percent_machine'],2),round(w['minimum_memory_available_percent'],2),
              round(w['telemetry_decimal_gb_per_hour'],4),'OOM',w['oom_seen'],'restarts',sum(w['restart_deltas'].values()),'errors',errors)
