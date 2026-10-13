"""Independent checks of quoted factual claims; no detector changes."""
import hashlib
import json
from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
LOG = ROOT / 'tasks/T-029-p4-han-che-phat-hien/LOG.md'
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def audit(s):
    with LOG.open('a', encoding='utf-8') as f:
        f.write('\n- '+datetime.now().astimezone().isoformat()+' — Kiểm độc lập Claude: '+s+'\n')
def put(name, obj):
    (RUN/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False)+'\n',encoding='utf-8')

audit('Lệnh có ghi: T-014-main Python -B -W ignore runs/verification-claude-001/check.py; kiểm checkpoint/source SHA trước raw, ghi check.json và LOG.')
cp = json.loads((ROOT/'results/T-029/runs/checkpoint-p1-001/manifest.json').read_text(encoding='utf-8'))
checks = {p: sha(ROOT/p) == v['sha256'] for p,v in cp['files'].items()}
if not all(checks.values()):
    put('dung.json', {'reason':'checkpoint hash mismatch','mismatches':[p for p,v in checks.items() if not v]})
    audit('DỪNG: checkpoint hash lệch; xem dung.json.')
    raise RuntimeError('Checkpoint hash mismatch')
allow = json.loads((ROOT/'results/T-022/allowlist-dev.json').read_text(encoding='utf-8'))['cases']
labels = {x['opaque_id']: x for x in json.loads((ROOT/'results/T-022/nhan-dev.json').read_text(encoding='utf-8'))['cases']}
claims = {'dev-4f8a844308':(750,691,0,0.), 'dev-a5cabe5fa7':(1140,301,15,.067), 'dev-ba831dbeb8':(861,580,0,0.)}
roots = {}; other_counts = {}; guards={}
for item in allow:
    oid=item['opaque_id']; m=item['files']['metrics.parquet']; path=ROOT/m['path']
    guards[oid]=sha(path)==m['sha256']
    if not guards[oid]:
        put('dung.json',{'reason':'V1','opaque_id':oid}); audit('DỪNG V1 '+oid); raise RuntimeError('V1 SHA mismatch')
    df=pd.read_parquet(path)
    assert len(df)==1441 and np.array_equal(df.time.to_numpy()-df.time.iloc[0],np.arange(1441))
    if oid in claims:
        col=labels[oid]['root']+'_error'; s=df[col]; observed=np.flatnonzero(s.notna().to_numpy())
        row={'column':col,'first_observed_index':int(observed[0]),'observed_count':int(s.count()),
             'nonzero_observed_count':int((s.dropna()!=0).sum()),'max':float(s.max()),
             'quoted_claim':list(claims[oid]),'metrics':m}
        expected=claims[oid]
        row['count_claims_match']=(row['first_observed_index'],row['observed_count'],row['nonzero_observed_count'])==expected[:3]
        row['rounded_max_claim_matches']=round(row['max'],3)==expected[3]
        roots[oid]=row
    columns=['ts-basic-service_error','ts-contacts-service_error']
    other_counts[oid]={c:int(df[c].count()) if c in df else None for c in columns}
diagnostic=json.loads((ROOT/'results/T-029/runs/proxy-001/undefined-diagnostic.json').read_text(encoding='utf-8'))
result={'checkpoint_files_checked':len(checks),'checkpoint_hashes_all_match':all(checks.values()),
        'metric_sha_guards':guards,'raw_root_error_claims':roots,'other_error_observed_counts_by_case':other_counts,
        'joint_match_basic659_contacts210':[oid for oid,c in other_counts.items() if list(c.values())==[659,210]],
        'diagnostic_original':diagnostic,
        'correction':'missing_baseline_count and missing_minute_count are observed counts from pandas.count(), not missing counts.',
        'interpretation':'Raw observation presence is distinct from nonzero error values. Zero recorded error does not prove no injected fault. The nonzero row is dev-a5cabe5fa7 (second row in quotation).',
        'script_sha256':sha(__file__)}
put('check.json',result)
audit('PASS checkpoint '+str(len(checks))+' hashes; metric SHA30/30. Ba dòng root/count/max đã đối chiếu raw, xem check.json. Đếm missing_* diagnostic thực chất là observed counts; không sửa lượt cũ.')
print(json.dumps({k:result[k] for k in ['checkpoint_files_checked','raw_root_error_claims','joint_match_basic659_contacts210']},ensure_ascii=False))
