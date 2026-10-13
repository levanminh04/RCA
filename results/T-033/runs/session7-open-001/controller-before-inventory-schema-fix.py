"""Laptop: metadata/hash, pinned SSH transport and conservative timing only."""
import datetime, hashlib, json, pathlib, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parents[3]
OPEN = ROOT / 'results/T-033/runs/session7-open-001'
PY = '/home/ubuntu/rca/T-025/envs/main/bin/python'
SSH = ['ssh', '-i', 'D:/RCA-ext/keys/keys.pem', '-o',
       'UserKnownHostsFile=' + str(ROOT/'results/T-033/runs/prepare-001/known_hosts'),
       '-o', 'StrictHostKeyChecking=yes', '-o', 'BatchMode=yes', '-o',
       'ConnectTimeout=20', 'ubuntu@3.107.246.249']

def sha(path):
    h = hashlib.sha256()
    with pathlib.Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

def read(path): return json.loads(pathlib.Path(path).read_text(encoding='utf-8-sig'))
def write(path, value):
    with pathlib.Path(path).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n')

def stamp(): return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat()

def integrity():
    records = []
    for name in ('checkpoint-handoff-001', 'session6-compute-checkpoint-001'):
        base = ROOT/'results/T-033/runs'/name
        inv = read(base/'artifact-inventory.json')
        entries = inv['files']
        if isinstance(entries, list):
            entries = {x.get('path', x.get('relative_path')): x for x in entries}
        bad = []
        for rel, meta in entries.items():
            p = base/'artifacts'/rel
            if not p.is_file() or p.stat().st_size != meta['bytes'] or sha(p) != meta['sha256']:
                bad.append(rel)
        records.append({'inventory': str((base/'artifact-inventory.json').relative_to(ROOT)),
                        'files': len(entries), 'mismatch': bad})
        assert not bad, bad
    # The manifest pins a historical LOG/STATE snapshot. Our pre-append copies
    # must match that snapshot; the live LOG is already an authorized append.
    m = read(ROOT/'results/T-033/runs/session6-compute-checkpoint-001/manifest.json')['files']
    for rel, meta in m.items():
        p = OPEN/(pathlib.Path(rel).name+'.before') if rel in (
            'docs/STATE.md', 'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md') else ROOT/rel
        assert p.stat().st_size == meta['bytes'] and sha(p) == meta['sha256'], rel
    native = read(ROOT/'results/T-033/runs/checkpoint-handoff-001/native-source-manifest.json')
    write(OPEN/'integrity.json', {'status':'PASS', 'inventory_checks': records,
        'session6_manifest_files':len(m), 'LOG_STATE_checked_at_before_append':True,
        'native_source_manifest':native, 'at':stamp()})
    print('PASS inventories and session6 manifest', records)

def remote(name, script, input_value=None):
    assert not any((OPEN/(name+s)).exists() for s in ('.stdout','.stderr','.timer.json'))
    old = ROOT/'results/T-033/runs/session6-final-budget-001/ledger.json'
    ledger = read(old)
    charges = []
    for p in sorted(OPEN.glob('*.timer.json')):
        timer = read(p)
        charges.append({'source':str(p.relative_to(ROOT)), 'sha256':sha(p),
                        'charged_processing_s':timer['charged_processing_s'],
                        'basis':timer['basis'], 'exit_code':timer['exit_code']})
    ledger['charges'] += charges
    ledger['new_processing_charged_s'] += sum(x['charged_processing_s'] for x in charges)
    ledger['approved_total_processing_s'] = ledger['approved_prior_processing_s'] + ledger['new_processing_charged_s']
    ledger['remaining_approved_s'] = ledger['approved_max_new_processing_s'] - ledger['new_processing_charged_s']
    ledger['at'] = stamp()
    ledger['previous_snapshot']={'path':str(old.relative_to(ROOT)),'sha256':sha(old)}
    ledger['next_run_requirements']=['Measure every EC2 command including failure; preserve all ledger history',
        'Pin this fresh snapshot before processing; do not relaunch verified detectors']
    assert ledger['remaining_approved_s'] > 0
    budget = ROOT/'results/T-033/runs'/(name+'--budget')
    budget.mkdir(exist_ok=False); write(budget/'ledger.json',ledger)
    b = (budget/'ledger.json').read_bytes(); pin=hashlib.sha256(b).hexdigest()
    payload = (
        'import pathlib,json,hashlib,time\n'
        "H=pathlib.Path('/home/ubuntu/rca/T-033')\n"
        f'_ledger_bytes=bytes.fromhex({b.hex()!r})\n'
        f'assert hashlib.sha256(_ledger_bytes).hexdigest()=={pin!r}\n'
        f"_budget=H/'runs'/{(name+'--budget')!r};_budget.mkdir(exist_ok=False)\n"
        "(_budget/'ledger.json').write_bytes(_ledger_bytes)\n"
        "_ledger=json.loads(_ledger_bytes);assert _ledger['accounting_valid_for_next_run']\n"
        "_start=time.perf_counter()\n"
    )
    if input_value is not None:
        data=json.dumps(input_value,ensure_ascii=False).encode('utf-8')
        payload += f'_input_bytes=bytes.fromhex({data.hex()!r})\nINPUT=json.loads(_input_bytes)\n'
    payload += pathlib.Path(script).read_text(encoding='utf-8-sig')
    write(OPEN/(name+'.payload.json'),{'script':str(pathlib.Path(script).relative_to(ROOT)),
        'script_sha256':sha(script),'ledger':str((budget/'ledger.json').relative_to(ROOT)),
        'ledger_sha256':pin,'input_sha256':hashlib.sha256(data).hexdigest() if input_value is not None else None})
    (OPEN/(name+'.payload.py')).write_text(payload,encoding='utf-8',newline='\n')
    start=stamp(); t=time.perf_counter()
    p=subprocess.run(SSH+['PYTHONDONTWRITEBYTECODE=1 '+PY+' -B -X utf8 -'],
        input=payload.encode('utf-8'),capture_output=True)
    elapsed=time.perf_counter()-t
    (OPEN/(name+'.stdout')).write_bytes(p.stdout);(OPEN/(name+'.stderr')).write_bytes(p.stderr)
    write(OPEN/(name+'.timer.json'),{'started':start,'ended':stamp(),
        'charged_processing_s':elapsed,'basis':'full SSH elapsed upper bound including network/import/exit',
        'exit_code':p.returncode,'payload_sha256':hashlib.sha256(payload.encode('utf-8')).hexdigest()})
    print(name,'exit',p.returncode,'charged_s',elapsed)
    print(p.stdout.decode(errors='replace')[:1000]);print(p.stderr.decode(errors='replace')[:1500])
    return p.returncode

if __name__ == '__main__':
    if sys.argv[1]=='integrity': integrity()
    else:
        inp=read(ROOT/sys.argv[4]) if len(sys.argv)>4 else None
        sys.exit(remote(sys.argv[2],ROOT/sys.argv[3],inp))
