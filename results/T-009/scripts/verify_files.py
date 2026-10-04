"""Independent balances, checksum and direct scalar probe recomputation."""
import argparse,codecs,collections,csv,hashlib,json,math,statistics,tarfile,zipfile
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--run',required=True);a=ap.parse_args();run=Path('results/T-009/runs')/a.run
load=lambda n:json.loads((run/(n+'.json')).read_text())
raw=load('raw-sessions');sym=load('symptom-metrics');ind=load('independent-summary');checks=[]
for r in raw:
    c=collections.Counter(r['trace']['counts']);assert c['spans']==c['root_no_CHILD_OF']+c['span_parent_required'];assert c['parent_references']==c['parent_unique']+c['parent_missing']+c['parent_ambiguous'];assert c['parent_references']==c['parent_unique_identity']+c['parent_missing']+c['parent_conflicting_identity']
    assert len(r['metrics']) in (12,27);assert all(m['rows']>0 for m in r['metrics']);assert r['logs']
for x in sym:assert 0<=x['exceed']<=x['n'] and x['reference_n']>0 and x['band']>=0
groups=collections.defaultdict(list)
for x in sym:groups[(x['dataset'],x['case'],x['service'],x['channel'],x['regime'],json.dumps(x['label'],sort_keys=True))].append(x)
for rows in groups.values():
    rows=sorted(rows,key=lambda x:x['q']);assert len(rows)==3;assert rows[0]['band']<=rows[1]['band']<=rows[2]['band'];assert rows[0]['exceed']>=rows[1]['exceed']>=rows[2]['exceed']
manifest=json.loads(Path('results/T-009/runs/download-001/manifest.json').read_text())
for x in manifest['items']:
    f=Path('data/ngoai-rcaeval/eadro')/x['path'];h=hashlib.sha256();m=hashlib.md5()
    with f.open('rb') as src:
        for ch in iter(lambda:src.read(1024*1024),b''):h.update(ch);m.update(ch)
    assert h.hexdigest()==x['sha256'] and m.hexdigest()==x['md5'];checks.append(dict(archive=x['path'],sha256_ok=True,official_md5_ok=True))
def read_metric(z,origin,case,svc):
    suffix=case+'/metrics/'+svc+'.csv'
    if origin=='outer':
        name=next(n for n in z.namelist() if n.endswith(suffix) and '__MACOSX' not in n)
        with z.open(name) as src:return list(csv.DictReader(codecs.getreader('utf-8')(src)))
    with z.open(origin) as src,tarfile.open(fileobj=src,mode='r|*') as tar:
        for m in tar:
            if m.name.endswith(suffix):return list(csv.DictReader(codecs.getreader('utf-8')(tar.extractfile(m))))
    raise ValueError(suffix)
direct=[]
for ds in ('SN','TT'):
    choices=[x for x in sym if x['dataset']==ds and x['regime']=='injection' and x['channel']=='cpu_usage_total']
    x=choices[0];f=Path('data/ngoai-rcaeval/eadro')/('social-network/SN Dataset.zip' if ds=='SN' else 'train-ticket/TT Dataset.zip')
    with zipfile.ZipFile(f) as z:
        _,ori,case=x['reference'].split('|',2);rs=read_metric(z,ori,case,x['service']);ref=[float(r[x['channel']]) for r in rs];median=statistics.median(ref);dev=sorted(abs(v-median) for v in ref)
        _,ori,case=x['case'].split('|',2);fault=read_metric(z,ori,case,x['service']);start=x['label']['start'];end=start+x['label']['duration'];xs=[float(r[x['channel']]) for r in fault if start<=float(r['timestamp'])<=end]
    for q in (.95,.99,.995):
        p=(len(dev)-1)*q;lo=math.floor(p);hi=math.ceil(p);band=dev[lo]+(dev[hi]-dev[lo])*(p-lo);actual=sum(abs(v-median)>band for v in xs)
        saved=next(r for r in choices if r['case']==x['case'] and r['service']==x['service'] and r['label']==x['label'] and r['q']==q)
        assert saved['reference_n']==len(ref) and saved['n']==len(xs) and saved['median']==median and saved['band']==band and saved['exceed']==actual
        direct.append(dict(dataset=ds,case=x['case'],service=x['service'],channel=x['channel'],q=q,reference_n=len(ref),n=len(xs),band=band,exceed=actual,ok=True))
assert ind['datasets']['SN']['label_events']==36 and ind['datasets']['TT']['label_events']==81
assert ind['datasets']['SN']['unique_raw_sessions']==7 and ind['datasets']['TT']['unique_raw_sessions']==12
v=dict(ok=True,all_parent_balances=True,all_probe_balances_and_monotonicity=True,metadata_label_counts_match=True,archive_checksums=checks,direct_scalar_recomputation=direct,raw_representations=len(raw),unique_raw_sessions=19,probe_rows=len(sym),note='independent direct CSV paths, median/quantile/exceed recomputed from archives; no model')
(run/'validation.json').write_text(json.dumps(v,indent=2),encoding='utf-8');print(json.dumps(v))
