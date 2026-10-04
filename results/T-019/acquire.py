"""Pinned metadata census and verified acquisition; no locked data or RCA."""
import argparse, collections, concurrent.futures, csv, hashlib, json, os, pathlib, shutil, time
from urllib.request import Request, urlopen
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / 'results/T-019'
DATA = ROOT / 'data/T-019'
META = ROOT / 'results/T-002/public-metadata/run-002'
REV = 'afeacb11bcc94dadfd1c8f483ee4377b2b8b614e'
PREFIX = ('re1ss_', 're2ss_', 're3ss_')

def dump(p, v):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def csvout(p, rows):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w', encoding='utf-8', newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]) if rows else ['empty']);w.writeheader();w.writerows(rows)

def hashcheck(raw, entry):
    sha=hashlib.sha256(raw).hexdigest()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    expected=entry.get('lfs',{}).get('oid') or entry['oid']
    actual=sha if 'lfs' in entry else blob
    return {'sha256':sha,'git_blob_sha1':blob,'expected_hash':expected,'hash_type':'LFS-SHA256' if 'lfs' in entry else 'git-blob-SHA1','valid':len(raw)==entry['size'] and actual==expected}

def plan():
    source=json.loads((META/'source-manifest.json').read_text())
    checks=[]
    for x in source:
        p=META/x['artifact']; h=hashlib.sha256(p.read_bytes()).hexdigest()
        checks.append({'path':str(p),'sha256':h,'expected':x['sha256'],'valid':h==x['sha256']})
    assert all(x['valid'] for x in checks)
    pages=[]
    for x in source:
        if 'hf-tree-page-' in x['artifact']: pages.extend(json.loads((META/x['artifact']).read_text()))
    tree=json.loads((META/'hf-tree.json').read_text());assert pages==tree
    assert json.loads((META/'run.json').read_text())['hf_revision']==REV
    dump(OUT/'input-metadata-check.json',{'revision':REV,'entries':len(tree),'checks':checks,'pages_equal_tree':True})
    dirs=[x['path'] for x in tree if x['type']=='directory' and x['path'].startswith(PREFIX)]
    files=[x for x in tree if x['type']=='file' and x['path'].startswith(PREFIX)]
    rows=[]; cells=collections.defaultdict(list)
    for d in sorted(dirs):
        ds,root,fault,rep=d.rsplit('_',3); own=[x for x in files if x['path'].split('/')[0]==d]
        names=[x['path'].split('/')[-1] for x in own];cells[(ds,root,fault)].append(int(rep))
        rows.append({'case':d,'dataset':ds.upper().replace('SS','-SS'),'root':root,'fault':fault,'repetition':int(rep),'trace':int('traces.parquet' in names),'log':int('logs.parquet' in names),'metric':int('metrics.parquet' in names),'injection':int('inject_time.txt' in names),'root_cause':int('root_cause.txt' in names),'files':'|'.join(sorted(names)),'bytes':sum(x['size'] for x in own)})
    assert len({(r['dataset'],r['root'],r['fault'],r['repetition']) for r in rows})==len(rows)
    csvout(OUT/'census-cases.csv',rows)
    csvout(OUT/'census-cells.csv',[{'dataset':d.upper().replace('SS','-SS'),'root':r,'fault':f,'cases':len(reps),'repetitions':'|'.join(map(str,sorted(reps)))} for (d,r,f),reps in sorted(cells.items())])
    csvout(OUT/'file-inventory.csv',[{'path':x['path'],'bytes':x['size'],'revision':REV,'source_hash':x.get('lfs',{}).get('oid') or x['oid'],'hash_type':'LFS-SHA256' if 'lfs' in x else 'git-blob-SHA1'} for x in files])
    summaries=[]
    for d in ('RE1-SS','RE2-SS','RE3-SS'):
        rr=[r for r in rows if r['dataset']==d]; cc=[(k,v) for k,v in cells.items() if k[0].upper().replace('SS','-SS')==d]
        summaries.append({'dataset':d,'cases':len(rr),'roots':dict(collections.Counter(r['root'] for r in rr)),'faults':dict(collections.Counter(r['fault'] for r in rr)),'cells':len(cc),'repetitions_histogram':dict(collections.Counter(len(v) for k,v in cc)),'files':sum(len(r['files'].split('|')) for r in rr),'trace_cases':sum(r['trace'] for r in rr),'log_cases':sum(r['log'] for r in rr),'metric_cases':sum(r['metric'] for r in rr),'root_cause_cases':sum(r['root_cause'] for r in rr),'bytes':sum(r['bytes'] for r in rr)})
    dump(OUT/'census-summary.json',summaries)
    reuse=[]
    for e in files:
        p=ROOT/'data/rcaeval'/e['path']
        if p.is_file():
            check=hashcheck(p.read_bytes(),e)
            if check['valid']: reuse.append(e['path'])
    dump(OUT/'download-plan.json',{'revision':REV,'base_url':f'https://huggingface.co/datasets/phamquiluan/RCAEval/resolve/{REV}/','all_file_bytes':sum(x['size'] for x in files),'reuse_paths':reuse,'download_bytes':sum(x['size'] for x in files if x['path'] not in reuse),'files':files,'max_network_bytes':900_000_000})
    print(json.dumps(summaries)); print('download plan',sum(x['size'] for x in files if x['path'] not in reuse),'reuse',len(reuse))

def acquire(run_name='acquisition'):
    assert pathlib.Path(run_name).name==run_name
    p=json.loads((OUT/'download-plan.json').read_text()); run=OUT/run_name
    run.mkdir(exist_ok=False); start=time.monotonic()
    records=[]
    def one(e):
        dst=DATA/e['path'];dst.parent.mkdir(parents=True,exist_ok=True)
        src=ROOT/'data/rcaeval'/e['path']; origin='network'; transferred=0
        if dst.is_file() and hashcheck(dst.read_bytes(),e)['valid']:
            raw=dst.read_bytes();origin='cache-verified'
        elif e['path'] in p['reuse_paths']:
            raw=src.read_bytes();origin='local-verified';shutil.copyfile(src,dst)
        else:
            url=p['base_url']+e['path']
            with urlopen(Request(url,headers={'User-Agent':'T019-dataset-card'}),timeout=90) as response:
                raw=response.read(e['size']+1);transferred=len(raw)
            dst.write_bytes(raw)
        ch=hashcheck(raw,e)
        if not ch['valid']: raise ValueError('hash/size mismatch '+e['path'])
        return {'path':e['path'],'local':str(dst),'revision':REV,'bytes':len(raw),'network_bytes':transferred,'origin':origin,**ch}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        future={pool.submit(one,e):e for e in p['files']}
        for f in concurrent.futures.as_completed(future):
            e=future[f]
            try: row=f.result()
            except Exception as ex: row={'path':e['path'],'error':repr(ex),'valid':False}
            records.append(row)
            with (run/'progress.jsonl').open('a',encoding='utf-8') as log:log.write(json.dumps(row,ensure_ascii=False)+'\n')
            if len(records)%25==0:print('files',len(records),'of',len(p['files']),'elapsed',round(time.monotonic()-start,1),flush=True)
    dump(run/'manifest.json',{'revision':REV,'elapsed_seconds':time.monotonic()-start,'network_bytes':sum(x.get('network_bytes',0) for x in records),'files':records,'success':all(x['valid'] for x in records)})
    assert all(x['valid'] for x in records), 'failed files retained'

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('mode',choices=['plan','acquire']);a.add_argument('--run',default='acquisition');ns=a.parse_args()
    plan() if ns.mode=='plan' else acquire(ns.run)
