#!/usr/bin/env python3
"""Run as user rca. Only fixed core code and allowlisted immutable case inputs."""
import argparse
import copy
import datetime
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT=Path('/opt/flash-ticket-rca')
sys.path.insert(0,str(ROOT/'src'))
from m1 import chuoi,e4,hop_dong
from m1.adapter_flashticket import adapt,jsonl

def canonical(x):
    return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)

parser=argparse.ArgumentParser()
parser.add_argument('--id',required=True)
args=parser.parse_args()
if not args.id.isalnum(): raise SystemExit('Expected opaque ID')
case=ROOT/'cases'/args.id
manifest=json.loads((case/'manifest.json').read_text(encoding='utf8'))
for filename,expected in manifest['files'].items():
    path=case/filename
    if path.parent.resolve()!=case.resolve(): raise SystemExit('Input outside the case allowlist')
    if hashlib.sha256(path.read_bytes()).hexdigest()!=expected['sha256']:
        raise SystemExit('Case input hash mismatch')
pin=json.loads((ROOT/'m1-source-pins.json').read_text(encoding='utf8'))
checked={}
for filename,expected in pin['pins'].items():
    actual=hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()
    if actual!=expected: raise SystemExit('Core code pin mismatch: '+filename)
    checked[filename]=actual
request=json.loads((case/'request.json').read_text(encoding='utf8'))
inventory=json.loads((case/'inventory.json').read_text(encoding='utf8'))
bundles=json.loads((case/'prometheus.json').read_text(encoding='utf8'))
converted=adapt(jsonl([case/'raw-traces.jsonl']),jsonl([case/'raw-logs.jsonl']),bundles,inventory,request['t'])
config=json.loads((ROOT/'m1-p7-config.json').read_text(encoding='utf8'))
params=copy.deepcopy(config)
overlap=set(params)&set(converted['params_ca'])
if overlap: raise SystemExit('Adapter attempted to override locked method parameters')
params.update(converted['params_ca'])
chuoi._kiem_params(params)
inputs=[converted['spans'],converted['metrics'],converted['logs'],converted['inventory'],converted['aliases'],request['t'],params]
forbidden=[args.id,str(case),str(ROOT/'cases'),'/var/lib/flash-ticket-ledger','so-tiem-loi.jsonl',
           'fault_service','injected_service','injection_start','scenario_name']
if hop_dong.vi_pham_truong_cam(inputs): raise SystemExit('Forbidden label field found in method inputs')
if hop_dong.vi_pham_gia_tri(params,converted['aliases'],inventory,forbidden): raise SystemExit('Forbidden label value found')
serialized=canonical(inputs)
if any(text in serialized for text in forbidden): raise SystemExit('Case/ledger identifier leaked into method input values')
out=ROOT/'outputs'/args.id
out.mkdir(parents=True,exist_ok=False)
(out/'adapter-diagnostics.json').write_text(canonical(converted['chan_doan_adapter'])+'\n',encoding='utf8')
(out/'method-input.json').write_text(serialized+'\n',encoding='utf8')
records=[]; runtimes=[]
for number in [1,2]:
    chuoi.CACHE=e4.CacheCong()
    stamp=time.monotonic()
    result=chuoi.chay(*inputs)
    runtimes.append(time.monotonic()-stamp)
    hop_dong.kiem_ban_ghi(result)
    encoded=canonical(result)+'\n'
    (out/f'method-output-{number}.json').write_text(encoded,encoding='utf8')
    records.append((result,hashlib.sha256(encoded.encode()).hexdigest()))
result=records[0][0]
summary={'opaque_id':args.id,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'status':result['status'],'error':result.get('error'),'entity_ranking':result.get('entity_ranking'),
         'sets':result.get('sets'),'diagnostics':result.get('diagnostics'),
         'adapter_diagnostics':converted['chan_doan_adapter'],
         'deterministic_repeat':records[0][1]==records[1][1],
         'output_sha256':[x[1] for x in records],'input_sha256':hashlib.sha256((serialized+'\n').encode()).hexdigest(),
         'run_seconds':runtimes,'source_pins_checked':len(checked),
         'no_label_fields':True,'no_opaque_or_ledger_values':True,
         'note':'Feasibility on two windows only; no ranking accuracy or RQ5 conclusion'}
(out/'summary.json').write_text(canonical(summary)+'\n',encoding='utf8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
