"""Snapshot only the authorized supplement trees; preserve historical files."""
from pathlib import Path
import hashlib, json, datetime, subprocess
P = Path(__file__).resolve().parent
R = P.parents[3]
Q = R / 'results/T-033/runs/bo-sung-toan-dien-20261012-001'
def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()
def save(p, d):
    assert not p.exists(), p
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
controls = [x['path'] for x in json.loads((P/'control-before.json').read_text(encoding='utf-8'))]
diff = subprocess.run(['git','-c','core.autocrlf=false','-c','core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol','diff','--check','--',*controls],cwd=R,capture_output=True,text=True)
assert diff.returncode == 0, diff.stdout+diff.stderr
excluded = {'manifest-final.json','final-verification.json','automation-pause-receipt.json'}
files = sorted(p for base in (P,Q) for p in base.rglob('*') if p.is_file() and not (p.parent==P and p.name in excluded))
rows = [dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in files]
control_rows = [dict(path=x,bytes=(R/x).stat().st_size,sha256=sha(R/x)) for x in controls]
manifest = dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Two supplement trees only; historical failures retained. Old immutable verification referenced, not rerun.',excluded_root_files=sorted(excluded),files=rows,controls=control_rows)
save(P/'manifest-final.json',manifest)
errors = [x['path'] for x in rows+control_rows if (R/x['path']).stat().st_size != x['bytes'] or sha(R/x['path']) != x['sha256']]
ledger = json.loads((P/'closure-ledger.json').read_text(encoding='utf-8'))
for x in ledger['questions']:
    if sha(R/x['source_file']) != x['source_sha256']: errors.append('ledger:'+x['id'])
audit = json.loads((P/'audit/audit-index-002.json').read_text(encoding='utf-8'))
for x in audit['results']:
    if sha(P/'audit'/x['file']) != x['sha256']: errors.append('audit:'+x['file'])
assert not errors, errors
assert json.loads((P/'controlled-verification-final.json').read_text(encoding='utf-8'))['status']=='PASS'
save(P/'final-verification.json',dict(status='PASS',at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),manifest_sha256=sha(P/'manifest-final.json'),supplement_files=len(rows),supplement_bytes=sum(x['bytes'] for x in rows),controlled_files=len(control_rows),ledger_rows=len(ledger['questions']),audit_pins=len(audit['results']),hash_errors=errors,diff_check_exit=diff.returncode,old_immutable_verification={'path':'old-immutable-verification.json','sha256':sha(P/'old-immutable-verification.json'),'rerun':False},scope='Re-read every new snapshot hash; exact controlled prefixes and two STATE rows checked separately. Historical source scan previously passed; no claim of rerunning all scientific methods.'))
print(json.dumps({'status':'PASS','files':len(rows),'bytes':sum(x['bytes'] for x in rows),'audit_pins':len(audit['results'])}))
