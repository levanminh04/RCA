#!/usr/bin/env python3
import datetime
import json
from pathlib import Path
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
import threading

start=datetime.datetime.fromisoformat(sys.argv[1].replace('Z','+00:00')).timestamp()
seconds=int(sys.argv[2])
fixture=json.loads(Path('/home/ubuntu/t058/seed-fixture.json').read_text())
paths=['/api/v1/events','/api/v1/events/'+fixture['event_id'],'/api/v1/events/'+fixture['event_id']+'/availability']
output=Path('/home/ubuntu/t058/light-load.jsonl')
if output.exists(): raise SystemExit('Refuse to overwrite existing load run')
lock=threading.Lock()
def send(i,due,path):
    stamp=time.time()
    status=None; error=None
    try:
        with urllib.request.urlopen('http://10.0.0.158:8081'+path,timeout=35) as response:
            status=response.status; response.read()
    except urllib.error.HTTPError as e:
        status=e.code
    except Exception as e:
        error=type(e).__name__
    completed=time.time()
    row={'utc':datetime.datetime.fromtimestamp(stamp,datetime.timezone.utc).isoformat(),'epoch':stamp,'completed_epoch':completed,'scheduled_epoch':due,'sequence':i,
         'path':path,'status':status,'error':error,'latency_ms':round((completed-stamp)*1000,3),'schedule_lag_ms':round((stamp-due)*1000,3)}
    with lock:
        with output.open('a') as f: f.write(json.dumps(row,separators=(',',':'))+'\n')
    if i%60==0: print(row['utc'],'request',i,'status',status,flush=True)
with ThreadPoolExecutor(max_workers=32) as pool:
    for i in range(seconds):
        due=start+i
        time.sleep(max(0,due-time.time()))
        pool.submit(send,i,due,paths[i%len(paths)])
Path('/home/ubuntu/t058/light-load.done').touch()
print('LIGHT_LOAD_COMPLETE',flush=True)
