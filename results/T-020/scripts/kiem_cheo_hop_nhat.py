"""Normalize actual recomputations; copying a numeric leaf is never a check."""
from pathlib import Path
from collections import Counter,defaultdict
import csv,json,hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'results/T-020'
merged=[]

def read(p):
    with (OUT/p).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))

def add(task,quantity,source,key,original,recomputed,status,calculation,components='',sampled='False',pool=''):
    merged.append(dict(task=task,dai_luong=quantity,nguon=source,khoa=key,gia_tri_goc=original,
        gia_tri_tinh_lai=recomputed,ket_qua=status,cach_tinh=calculation,nguon_thanh_phan=components,
        lay_mau=sampled,seed='20261004',pham_vi=pool))

for r in read('trung-gian/dataset_evidence/checks.csv'):
    add(r['task'],r['meaning'],r['path'],r['key'],r['original'],r['recomputed'],'MATCH' if r['match']=='True' else 'MISMATCH',r['recompute'],r['source'],r['seeded_sample'],'dataset source component checks')
for r in read('trung-gian/method_evidence/checks-normalized.csv'):
    status='MATCH' if r['match'] in ['PASS','True','MATCH'] else r['match']
    add(r['task'],r['key'],r['source'],r['key'],r['original_value'],r['recomputed_value'],status,r['query'],r['component_source'],'True' if r['selection_hash'] else 'False','method component, replay and source checks; '+r['reason'])
for r in read('trung-gian/exposure_ledger/numeric-check-all.csv'):
    add(r['task'],r['meaning'],r['path'],r['key'],r['published'],r['recomputed'],'MATCH' if r['ok']=='True' else 'MISMATCH',r['calculation'],r['check_reference'],'False','execution ledger/source output checks')
for name in ['independent-counts.csv','root-code-checks.csv','root-cost-checks.csv']:
    for r in read('trung-gian/root/'+name):
        add(r['task'],r.get('quantity',r['key']),r['source'],r['key'],r['original'],r['recomputed'],'MATCH' if r['match']=='True' else 'MISMATCH',r['reason'],'','False','root independent')
for name in ['dataset_evidence/root-selected-checks.csv']:
    if not (OUT/'trung-gian'/name).exists():continue
    rs=read('trung-gian/'+name)
    for r in rs:
        state=r.get('match',r.get('status','OPEN'))
        state='MATCH' if state in ['PASS','MATCH','True'] else 'OPEN' if state in ['OPEN','chua_kiem','SKIP'] else state
        add(r['task'],r.get('meaning',r['key']),r.get('path',r.get('source','')),r['key'],r.get('original_value',r.get('original',r.get('value',''))),r.get('recomputed_value',r.get('recomputed','')),state,r.get('query',r.get('calculation',r.get('reason',''))),r.get('reason',''),'True','root full-leaf inventory hash samples; OPEN retained')

# Independent aggregation of public labels; no telemetry.
nezha=json.loads((ROOT/'results/T-008/runs/run-001/labels.json').read_text(encoding='utf-8-sig'))
for ds,expected in [('OB',56),('TT',45)]:
    rs=[x for x in nezha if x['dataset']==ds]
    add('T-008',f'Nezha {ds} label records','results/T-008/runs/run-001/labels.json',f'dataset={ds}',expected,len(rs),'MATCH' if len(rs)==expected else 'MISMATCH','root count label records, not physical unique injections','','False','critical G1')
    nc=len({(x['service'],x['fault']) for x in rs});expectedc=33 if ds=='OB' else 23
    add('T-008',f'Nezha {ds} root×fault cells','results/T-008/runs/run-001/labels.json',f'dataset={ds};service,fault',expectedc,nc,'MATCH' if nc==expectedc else 'MISMATCH','root set(service,fault)','','False','critical G1')
eadro=json.loads((ROOT/'results/T-009/runs/inspect-004/labels-all.json').read_text(encoding='utf-8-sig'))
for ds,exp in [('SN',36),('TT',81)]:
    labels=[f for r in eadro if r['dataset']==ds and r['origin']=='outer' for f in r['label']['faults']]
    # No duplicate labels from inner archive mirrors.
    add('T-009',f'Eadro {ds} outer fault records','results/T-009/runs/inspect-004/labels-all.json',f'{ds},origin=outer,faults',exp,len(labels),'MATCH' if len(labels)==exp else 'MISMATCH','root flatten outer labels only; inner copy excluded','','False','critical G1')
    nc=len({(r['name'],r['fault']) for r in labels})
    add('T-009',f'Eadro {ds} cells','results/T-009/runs/inspect-004/labels-all.json',f'{ds},name,fault',exp,nc,'MATCH' if nc==exp else 'MISMATCH','root root-container×fault set; service mapping separate','','False','critical G1')

assertions=json.loads((OUT/'runs/split-assertions.json').read_text(encoding='utf-8'))
for package,data in assertions.items():
    rs=read(f'chia-theo-o/{package}.csv')
    for r in data['summary']:
        selected=[x for x in rs if x['dataset']==r['dataset'] and x['vai_tro']==r['role']]
        counts=Counter((x['root'],x['fault']) for x in selected)
        for key,got in [('cases',len(selected)),('cells',len(counts)),('single_repeat_cells',sum(v==1 for v in counts.values()))]:
            add('T-020',f'{package} {r["dataset"]} {r["role"]} {key}','results/T-020/runs/split-assertions.json',f'{package}/{r["dataset"]}/{r["role"]}/{key}',r[key],got,'MATCH' if got==r[key] else 'MISMATCH','root independent DictReader/set/Counter of proposed split rows',f'results/T-020/chia-theo-o/{package}.csv','False','critical G1 split')

for fname,expected,quantity in [('01-bang-tieu-chi-hop-nhat.csv',40,'dataset parts'),('yeu-cau-dau-vao-hop-nhat.csv',42,'method/variant requirement rows'),('04-phuong-phap-x-dataset.csv',1680,'method×part pairs')]:
    rs=read(fname);got=len(rs)
    add('T-020',quantity,'results/T-020/'+fname,'DictReader rows',expected,got,'MATCH' if got==expected else 'MISMATCH','count data rows','','False','critical G1')
coverage=json.loads((OUT/'trung-gian/root/g1-coverage.json').read_text(encoding='utf-8'))
v1=read('08-so-chuyen-g1.csv')
# Every matched source occurrence has an explicit occurrence row; extra rows are separate.
import re
found=[]
for path in coverage['files']:
    for i,line in enumerate((ROOT/path).read_text(encoding='utf-8-sig',errors='replace').splitlines(),1):
        if re.search('G1|chốt ở',line,re.I):found.append(f'{path}:{i}')
mapped={r['nguon'] for r in v1 if re.fullmatch(r'G1-\d+',r['id'])}
assert set(found)==mapped
for key,got in [('matches',len(found)),('mapped',len(mapped))]:
    add('T-020','G1 occurrence '+key,'results/T-020/trung-gian/root/g1-coverage.json',key,coverage[key],got,'MATCH' if coverage[key]==got else 'MISMATCH','root rescan exact original file lines; semantic review overrides separate','','False','critical G1')
axes=read('trung-gian/dataset_evidence/independence-axes.csv')
assert all('OPEN' in r['c9_state'] for r in axes)
add('T-020','candidates proven all3 C9 axes','results/T-020/trung-gian/dataset_evidence/independence-axes.csv','c9_state, 40 parts',0,0,'MATCH','all rows retain OPEN; does not assert no qualifying dataset exists in the world','','False','critical G1')
assert all(r['gia_tri_goc']!='' and r['gia_tri_tinh_lai']!='' for r in merged if r['ket_qua']=='MATCH')

with (OUT/'09-kiem-cheo-so-lieu.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(merged[0]));w.writeheader();w.writerows(merged)
report={'rows':len(merged),'states':dict(Counter(r['ket_qua'] for r in merged)),
        'per_task':dict(Counter(r['task'] for r in merged)),
        'critical_rows':[r for r in merged if r['pham_vi'].startswith('critical G1')],
        'not_coverage_claim':'Numeric leaf inventory is not verified. Source pools and OPEN selected leaves are retained. No raw TX0/TX1 recount.'}
(OUT/'runs/crosscheck-merge-assertions.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
explained={(r['source'],r['key']) for r in read('trung-gian/method_evidence/mismatches.csv')}
actual={(r['nguon'],r['khoa']) for r in merged if r['ket_qua']=='MISMATCH'}
assert actual==explained and len(actual)==4,(actual,explained)
print('normalized',report['rows'],report['states'],report['per_task'])
