"""Read assigned output files on both hosts; no remote mutations or engine launches."""
from pathlib import Path
import concurrent.futures, datetime, hashlib, json, subprocess, sys

P = Path(__file__).resolve().parent
M = P / 't32/t33-migration-001/migration-inputs-001/manifest.json'
cases = json.loads(M.read_text(encoding='utf-8'))['cases']
assert len(cases) == 30 and len({c['opaque_id'] for c in cases}) == 30
branches = ['prior_df4', 'prior_kappa4', 'prior_precision4', 'causal_fixed',
            'causal_expanding', 'compressed_row', 'compressed_calendar']
configs = [
    ('T33', '3.107.246.249', 'D:/RCA-ext/keys/keys.pem',
     '/home/ubuntu/rca/T-033/runs/bo-sung-toan-dien-20261012-001/t33', 1, 14),
    ('T32', '3.26.62.217', 'D:/RCA-ext/keys/key2.pem',
     '/home/ubuntu/rca/T-032/runs/bo-sung-toan-dien-20261012-001/t32/t33-migration-001', 15, 30),
]

def check(cfg):
    label, host, key, base, lo, hi = cfg
    owned = [(i + 1, c['opaque_id']) for i, c in enumerate(cases) if lo <= i + 1 <= hi]
    program = '''import pathlib,json,datetime
p=pathlib.Path(BASE); rows=[]
for ci,oid in OWNED:
 for branch in ['native']+BRANCHES:
  name=oid+('--full-sham-thread1.json' if branch=='native' else '--'+branch+'.json')
  f=p/name; r={'case':ci,'opaque_id':oid,'branch':branch,'file':name}
  if not f.exists(): r['status']='PENDING'
  else:
   try:
    d=json.loads(f.read_text())
    r['status']=('PASS' if d.get('native_full_sham_exact') is True else 'INVALID_GATE') if branch=='native' else d.get('status','MISSING_STATUS')
    r['bytes']=f.stat().st_size
   except Exception as e:r['status']='UNREADABLE_OR_IN_PROGRESS';r['error']=repr(e)
  rows.append(r)
print(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':rows}))
'''.replace('BASE', repr(base)).replace('OWNED', repr(owned)).replace('BRANCHES', repr(branches))
    cmd = ['ssh', '-i', key, '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=yes', '-o', 'ConnectTimeout=20']
    if label == 'T33':
        cmd += ['-o', 'UserKnownHostsFile=D:/RCA-flashticket/results/T-033/runs/prepare-001/known_hosts']
    r = subprocess.run(cmd + ['ubuntu@' + host, 'python3 -B -'], input=program.encode(), capture_output=True)
    if r.returncode:
        return {'host': label, 'status': 'TRANSPORT_ERROR', 'stderr': r.stderr.decode(errors='replace')}
    result = json.loads(r.stdout)
    result.update(host=label, expected_slots=len(owned)*8)
    result['counts'] = {s: sum(x['status'] == s for x in result['rows']) for s in sorted({x['status'] for x in result['rows']})}
    result['complete_cases'] = [ci for ci, _ in owned if all(x['status']=='PASS' for x in result['rows'] if x['case']==ci)]
    return result

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    hosts = list(pool.map(check, configs))
out = {'scope': 'Read current files/status only; not hash receipt or independent scientific audit.',
       'source_case_manifest_sha256': hashlib.sha256(M.read_bytes()).hexdigest(),
       'expected_slots': 240, 'hosts': hosts}
out['pass_slots'] = sum(h.get('counts', {}).get('PASS', 0) for h in hosts)
target = P / sys.argv[1]
with target.open('x', encoding='utf-8') as f: json.dump(out, f, ensure_ascii=False, indent=2)
print(json.dumps({'pass_slots': out['pass_slots'], 'expected': 240,
                  'hosts': [{k: v for k, v in h.items() if k != 'rows'} for h in hosts]}, ensure_ascii=False))
