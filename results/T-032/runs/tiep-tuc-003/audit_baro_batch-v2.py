"""Byte/source audit of completed BARO queue; no method is executed."""
import json
import argparse
import os
from pathlib import Path
import sys
import time
import batch_baro as b

H = Path('/home/ubuntu/rca/T-032')
parser = argparse.ArgumentParser()
parser.add_argument('--run', required=True)
args = parser.parse_args()
assert args.run.startswith('baro-re2-audit-') and '/' not in args.run and '\\' not in args.run
out = b.new_run(H/'runs'/args.run)
plan_dir = H/'runs/baro-re2-plan-001'
queue = H/'runs/baro-re2-batch-001'
t0 = time.perf_counter()
try:
    plan = b.replay.read(plan_dir/'plan.json')
    status = b.replay.read(queue/'status.json')
    b.require(status['status']=='PASS' and status['n_main_valid']==30, 'queue incomplete')
    scripts = b.verify_scripts(plan['scripts'])
    b.require(b.environment()==plan['environment'], 'audit environment differs from plan')
    audit=[]; rows=[]
    ids = b.verified_main_ids(audit)
    for oid in ids:
        source,frozen,_ = b.source_case(oid,audit)
        directory = b.PILOT if oid==b.PILOT_ID else queue/'cases'/oid
        row = b.verify_output(directory,source,frozen,scripts)
        row['opaque_id']=oid
        rows.append(row)
        with (out/'progress.jsonl').open('a') as stream:
            stream.write(json.dumps({'done':len(rows),'total':len(ids),'last':oid})+'\n')
        print('CASE_VERIFIED',len(rows),len(ids),oid,flush=True)
    b.replay.dump(out/'source-checks.json',{'checks':audit})
    result={'status':'PASS','cases':rows,'n_main_valid':len(rows),'source_plan_sha256':b.replay.sha(plan_dir/'plan.json'),
            'queue_status_sha256':b.replay.sha(queue/'status.json'),'wall_s':time.perf_counter()-t0,
            'logical_case_bytes':sum(r['logical_bytes'] for r in rows),
            'allocated_case_bytes':sum(r['allocated_file_bytes'] for r in rows),
            'note':'Full source/byte audit of existing PASS; no repeated method or new causal finding.'}
    b.replay.dump(out/'checks.json',result)
    print(json.dumps({'status':'PASS','cases':len(rows),'case_bytes':result['logical_case_bytes'],'wall_s':result['wall_s']}),flush=True)
except BaseException as exc:
    b.replay.dump(out/'failure.json',{'error':type(exc).__name__+': '+str(exc)})
    raise
finally:
    b.replay.dump(out/'manifest.json',{'files':b.replay.artifact_manifest(out)})
