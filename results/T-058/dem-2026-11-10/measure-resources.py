#!/usr/bin/env python3
"""Two consecutive one-hour windows, timestamped samples on each Oracle."""
import datetime
import json
import os
from pathlib import Path
import re
import statistics
import subprocess
import sys
import time
import urllib.request

role=sys.argv[1]
start=datetime.datetime.fromisoformat(sys.argv[2].replace('Z','+00:00')).timestamp()
half=int(sys.argv[3]) if len(sys.argv)>3 else 3600
runid=sys.argv[4] if len(sys.argv)>4 else 'resources'
output=Path('/home/ubuntu/t058')/(runid+'-'+role+'.jsonl')
if output.exists(): raise SystemExit('Refuse to overwrite a measurement run')
period=15
def cpu(): return [int(x) for x in Path('/proc/stat').read_text().splitlines()[0].split()[1:9]]
def usage(paths):
    total=0
    for path in paths:
        for folder,dirs,files in os.walk(path):
            for f in files:
                try: total+=os.stat(os.path.join(folder,f)).st_size
                except FileNotFoundError: pass
    return total
storage=[Path('/opt/flash-ticket-app/collector/data')] if role=='app' else [Path('/opt/flash-ticket-obs/pinned/data')]
if role=='obs':
    names=subprocess.check_output(['docker','volume','ls','--format','{{.Name}}'],text=True).splitlines()
    for name in names:
        if name.startswith('flash-ticket-obs-pinned_'):
            storage.append(Path(json.loads(subprocess.check_output(['docker','volume','inspect',name]))[0]['Mountpoint']))
rows=[]
prev=None
for tick in range((2*half)//period+1):
    scheduled=start+tick*period
    time.sleep(max(0,scheduled-time.time()))
    stamp=time.time(); current=cpu()
    memory={k:int(v.split()[0])*1024 for k,v in (line.split(':',1) for line in Path('/proc/meminfo').read_text().splitlines())}
    current_total=sum(current); current_idle=current[3]+current[4]
    utilization=None
    if prev:
        dt=current_total-prev[0]
        utilization=100*(1-(current_idle-prev[1])/dt) if dt else None
    prev=(current_total,current_idle)
    raw=subprocess.check_output(['docker','stats','--no-stream','--format','{{json .}}'],text=True)
    stats=[json.loads(line) for line in raw.splitlines() if line]
    ids=subprocess.check_output(['docker','ps','-aq'],text=True).split()
    states=json.loads(subprocess.check_output(['docker','inspect',*ids]))
    counters=[]
    try:
        with urllib.request.urlopen('http://127.0.0.1:8888/metrics',timeout=5) as r: text=r.read().decode()
        counters=[line for line in text.splitlines() if not line.startswith('#') and any(w in line for w in ['receiver_refused','exporter_send_failed','exporter_enqueue_failed','exporter_queue_size','receiver_accepted','exporter_sent'])]
    except Exception as e:
        counters=['UNAVAILABLE '+type(e).__name__]
    fs=os.statvfs('/')
    record={'scheduled_epoch':scheduled,'epoch':stamp,'utc':datetime.datetime.fromtimestamp(stamp,datetime.timezone.utc).isoformat(),
            'phase':'idle' if tick*period<half else 'light_load','role':role,'cpu_percent':utilization,
            'memory_total_bytes':memory['MemTotal'],'memory_available_bytes':memory['MemAvailable'],
            'memory_available_percent':100*memory['MemAvailable']/memory['MemTotal'],
            'root_used_bytes':(fs.f_blocks-fs.f_bfree)*fs.f_frsize,'telemetry_storage_bytes':usage(storage),
            'docker_stats':stats,
            'containers':[{'name':s['Name'],'status':s['State']['Status'],'oom_killed':s['State']['OOMKilled'],'restart_count':s['RestartCount']} for s in states],
            'collector_counters':counters}
    with output.open('a') as f: f.write(json.dumps(record,separators=(',',':'))+'\n')
    rows.append(record)
    if tick%4==0: print(record['utc'],record['phase'],'sample',tick,flush=True)
summary={'role':role,'planned_start':start,'planned_end':start+2*half,'window_seconds':half,'sample_count':len(rows),'sampling_seconds':period,'storage_paths':[str(x) for x in storage],'windows':{}}
for phase,lo,hi in [('idle',start,start+half),('light_load',start+half,start+2*half)]:
    data=[r for r in rows if lo<=r['scheduled_epoch']<=hi]
    cpus=[r['cpu_percent'] for r in data if r['cpu_percent'] is not None]
    summary['windows'][phase]={'samples':len(data),'first_utc':data[0]['utc'],'last_utc':data[-1]['utc'],
        'actual_seconds':data[-1]['epoch']-data[0]['epoch'],'cpu_mean_percent':statistics.mean(cpus),'cpu_max_percent':max(cpus),
        'minimum_memory_available_percent':min(r['memory_available_percent'] for r in data),
        'telemetry_bytes_growth':data[-1]['telemetry_storage_bytes']-data[0]['telemetry_storage_bytes'],
        'telemetry_gb_per_hour':(data[-1]['telemetry_storage_bytes']-data[0]['telemetry_storage_bytes'])/1e9*3600/(data[-1]['epoch']-data[0]['epoch']),
        'oom_seen':any(s['oom_killed'] for r in data for s in r['containers']),
        'first_container_states':data[0]['containers'],'last_container_states':data[-1]['containers'],
        'first_collector_counters':data[0]['collector_counters'],'last_collector_counters':data[-1]['collector_counters']}
Path('/home/ubuntu/t058/'+runid+'-'+role+'-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
Path('/home/ubuntu/t058/'+runid+'-'+role+'.done').touch()
print('RESOURCE_WINDOWS_COMPLETE',flush=True)
