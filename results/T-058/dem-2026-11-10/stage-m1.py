#!/usr/bin/env python3
"""Freeze bounded prefixes of live Collector files, without reading the ledger."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import grp
import sys

ROOT=Path('/opt/flash-ticket-rca')
sys.path.insert(0,str(ROOT/'src'))
from m1.adapter_flashticket import collect_metrics

def canonical(x):
    return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)

def bounded_documents(path,provenance):
    digest=hashlib.sha256(); complete=0; partial=0
    with path.open('rb') as stream:
        bound=os.fstat(stream.fileno()).st_size
        while stream.tell()<bound:
            raw=stream.readline(bound-stream.tell())
            digest.update(raw)
            if not raw.endswith(b'\n'):
                partial+=len(raw); continue
            complete+=len(raw)
            yield json.loads(raw)
    provenance.append({'path':str(path),'prefix_bytes':bound,'complete_line_bytes':complete,
                       'partial_final_line_bytes':partial,'prefix_sha256':digest.hexdigest()})

def traces(document,lo,hi):
    out=[]
    for resource in document.get('resourceSpans',[]):
        groups=[]
        for group in resource.get('scopeSpans',[]):
            chosen=[s for s in group.get('spans',[]) if int(s['startTimeUnixNano'])>=lo and int(s['endTimeUnixNano'])<hi]
            if chosen: groups.append(dict(group,spans=chosen))
        if groups: out.append(dict(resource,scopeSpans=groups))
    return {'resourceSpans':out} if out else None

def logs(document,lo,hi):
    out=[]
    for resource in document.get('resourceLogs',[]):
        groups=[]
        for group in resource.get('scopeLogs',[]):
            chosen=[s for s in group.get('logRecords',[]) if lo<=int(s.get('timeUnixNano') or s.get('observedTimeUnixNano'))<hi]
            if chosen: groups.append(dict(group,logRecords=chosen))
        if groups: out.append(dict(resource,scopeLogs=groups))
    return {'resourceLogs':out} if out else None

parser=argparse.ArgumentParser()
parser.add_argument('--id',required=True)
parser.add_argument('--t',required=True,type=int)
args=parser.parse_args()
if not args.id.isalnum(): raise SystemExit('Opaque ID must be alphanumeric')
case=ROOT/'cases'/args.id
case.mkdir(parents=True,exist_ok=False)
os.chmod(case,0o750)
lo=(args.t-600)*10**9; hi=(args.t+600)*10**9
capture=Path('/opt/flash-ticket-obs/pinned/data/capture')
sources=[]
counts={}
for prefix,selector in [('traces',traces),('logs',logs)]:
    count=0
    with (case/('raw-'+prefix+'.jsonl')).open('w',encoding='utf8') as output:
        for path in sorted(capture.glob(prefix+'*.jsonl')):
            for doc in bounded_documents(path,sources):
                chosen=selector(doc,lo,hi)
                if chosen:
                    output.write(canonical(chosen)+'\n'); count+=1
    counts[prefix+'_batches']=count
bundles=collect_metrics('http://127.0.0.1:9090',args.t-600,args.t+600,15)
(case/'prometheus.json').write_text(canonical(bundles)+'\n',encoding='utf8')
model=json.loads((ROOT/'flashticket-inventory-source.json').read_text(encoding='utf8'))
inventory=[entity['id'] for entity in model['entities']]
(case/'inventory.json').write_text(canonical(inventory)+'\n',encoding='utf8')
(case/'request.json').write_text(canonical({'t':args.t})+'\n',encoding='utf8')
files={}
for path in sorted(case.iterdir()):
    files[path.name]={'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
manifest={'opaque_id':args.id,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'pack_window_seconds':[args.t-600,args.t+600],'method_window_seconds':[args.t-300,args.t+300],
          'mode':'a','source_prefixes':sources,'files':files,'counts':counts,
          'inventory_source_sha256':model['source_sha256'],
          'note':'Bounded prefixes and immutable extracted files; no ledger or fault labels are read or included'}
(case/'manifest.json').write_text(canonical(manifest)+'\n',encoding='utf8')
for path in case.iterdir(): path.chmod(0o640)
group=grp.getgrnam('rca').gr_gid
os.chown(case,0,group)
for path in case.iterdir(): os.chown(path,0,group)
print(json.dumps({'opaque_id':args.id,'directory':str(case),'counts':counts,'files':files},indent=2))
