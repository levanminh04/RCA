"""Audit already completed BARO Nezha artifacts; never call the method."""
import argparse
import json
from pathlib import Path
import time
import batch_baro_nezha as b

p = argparse.ArgumentParser()
p.add_argument('--run', required=True)
a = p.parse_args()
assert a.run.startswith('baro-nezha-audit-') and '/' not in a.run and '\\' not in a.run
out = b.b.new_run(b.H / 'runs' / a.run)
queue = b.H / 'runs/baro-nezha-batch-001'
plan_dir = b.H / 'runs/baro-nezha-plan-001'
started = time.perf_counter()
try:
    plan = b.r.read(plan_dir / 'plan.json')
    status = b.r.read(queue / 'status.json')
    b.b.require(status['status'] == 'PASS' and status['n_main_valid'] == 22, 'queue incomplete')
    b.b.require(plan['scripts'] == b.scripts() and plan['environment'] == b.b.environment(), 'plan changed')
    rows, audit = [], []
    for oid in plan['main_ids']:
        entry, frozen = b.source(oid, audit)
        directory = b.PILOT if oid == b.PILOT_ID else queue / 'cases' / oid
        row = b.check_output(directory, oid, entry, frozen)
        rows.append(row)
        with (out / 'progress.jsonl').open('a') as stream:
            stream.write(json.dumps({'done': len(rows), 'total': 22, 'last': oid}) + '\n')
        print('CASE_VERIFIED', len(rows), 22, oid, flush=True)
    b.r.dump(out / 'source-checks.json', {'checks': audit})
    b.r.dump(out / 'checks.json', {
        'status': 'PASS', 'cases': rows, 'n_main_valid': len(rows),
        'source_plan_sha256': b.r.sha(plan_dir / 'plan.json'),
        'queue_status_sha256': b.r.sha(queue / 'status.json'),
        'wall_s': time.perf_counter() - started,
        'logical_case_bytes': sum(row['logical_bytes'] for row in rows),
        'note': 'Source/exact/capture/byte audit of completed artifacts; no method rerun or causal inference.'})
except BaseException as exc:
    b.r.dump(out / 'failure.json', {'error': type(exc).__name__ + ': ' + str(exc)})
    raise
finally:
    b.r.dump(out / 'manifest.json', {'files': b.r.artifact_manifest(out)})
