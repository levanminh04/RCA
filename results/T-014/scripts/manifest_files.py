"""Inventory every task-owned file; shared STATE is identified by its own row."""
import csv,json,hashlib,subprocess
from pathlib import Path
repo=Path('D:/RCA-flashticket');out=repo/'results/T-014'
targets=[('task',repo/'tasks/T-014-ho-so-circa'),('results',out),('source',repo/'src/circa_kien_truc'),('outside_work',Path('D:/RCA-ext/work/T-014')),('outside_environment',Path('D:/RCA-ext/envs/T-014-main'))]
manifest=out/'manifest-files.csv'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
rows=[]
for scope,base in targets:
    for p in sorted(base.rglob('*')):
        if not p.is_file():continue
        derived=p.name in ['manifest-files.csv','manifest-summary.json','download-sources.csv','download-accounting.json'] and p.parent==out
        rows.append(dict(scope=scope,path=p.as_posix(),bytes='' if derived else p.stat().st_size,sha256='derived inventory metadata: deliberately not hashed' if derived else sha(p),note='created within authorized task directory; includes dependencies and retained failure/cache files'))
remote=out/'runs/external-files.csv'
if remote.exists():
    with remote.open(encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            rows.append(dict(scope='ec2',path=r.get('path',r.get('duong_dan','')),bytes=r.get('bytes',''),sha256=r.get('sha256',''),note='EC2 own directory; inventory generated on host after terminal run; local copyback kept separately'))
    rows.append(dict(scope='ec2',path='/home/ubuntu/rca/T-014/external-files.csv',bytes='',sha256='remote self-inventory: deliberately not hashed',note='The host inventory excludes itself from its own hashes; this row completes the file list.'))
remote2=out/'runs/external-files-ec2-2.csv'
if remote2.exists():
    with remote2.open(encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            rows.append(dict(scope='ec2_2',path=r['path'],bytes=r['bytes'],sha256=r['sha256'],note='host3.26.62.217; own task directory; source/runtime/env/wheels included; equal paths on EC2 first host are different artifacts'))
    rows.append(dict(scope='ec2_2',path='/home/ubuntu/rca/T-014/external-files-ec2-2.csv',bytes='',sha256='remote self-inventory: deliberately not hashed',note='host3.26.62.217; host identity is in scope/note'))
line=next(l for l in (repo/'docs/STATE.md').read_bytes().splitlines() if l.startswith(b'| T-014 |'))
rows.append(dict(scope='shared_row_only',path='D:/RCA-flashticket/docs/STATE.md#T-014',bytes=len(line),sha256=hashlib.sha256(line).hexdigest(),note=line.decode('utf-8')))
with manifest.open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['scope','path','bytes','sha256','note']);w.writeheader();w.writerows(rows)
totals={scope:dict(files=sum(r['scope']==scope for r in rows),logical_bytes=sum(int(r['bytes'] or 0) for r in rows if r['scope']==scope)) for scope in {r['scope'] for r in rows}}
(out/'manifest-summary.json').write_text(json.dumps(dict(scopes=totals,manifest='manifest-files.csv',hash_warning='The four derived inventory metadata files have no self-referential bytes/hash. Shared STATE hash is only authorized row. Rerun after any task mutation. Logical bytes are not network download bytes.'),ensure_ascii=False,indent=2),encoding='utf-8')
# Network sources, distinct from installed/extracted byte counts.
with (out/'audit/source-downloads.csv').open(encoding='utf-8-sig',newline='') as f:downloads=list(csv.DictReader(f))
paper=json.loads((out/'paper/source-manifest.json').read_text())
downloads.append(dict(url=paper['paper_url'],path=(out/'paper/KDD22-CIRCA.pdf').as_posix(),bytes=paper['paper_bytes'],sha256=paper['paper_sha256'],md5='',published_checksum_match='locally pinned SHA256'))
with (out/'download-sources.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['url','path','bytes','sha256','md5','published_checksum_match']);w.writeheader();w.writerows(downloads)
cache=Path('D:/RCA-ext/work/T-014/cache')
cache_logical=sum(p.stat().st_size for p in cache.rglob('*') if p.is_file())
pack=sum(p.stat().st_size for p in Path('D:/RCA-ext/work/T-014/CIRCA/.git/objects/pack').glob('*.pack'))
known=sum(int(r['bytes']) for r in downloads)
(out/'download-accounting.json').write_text(json.dumps(dict(saved_distinct_payload_bytes=known,known_repeated_CRAN_metadata_bytes=971145,known_cumulative_network_bytes=known+971145,python_cache_logical_bytes=cache_logical,git_pack_file_bytes=pack,python_wheels='PyPI pyarrow18.1.0/networkx2.8.8; original compressed wheel byte counts not retained by uv unpacked cache, sha256 of every installed/cache file in manifest',code_source='https://github.com/NetManAIOps/CIRCA.git at pinned revision; pack SHA256 in manifest',declared_limit_bytes=1000000000,conservative_accounting_bytes=known+971145+2*cache_logical+2*pack+10000000,under_limit_conservative=known+971145+2*cache_logical+2*pack+10000000<1000000000,accounting_caveat='Audit downloaded CRAN PACKAGES twice during failed/successful setup; same path overwritten so distinct saved payload differs from cumulative network. Conservative bound includes twice local cache/pack footprint plus10MB metadata allowance; not exact network bill. No new dataset download.'),ensure_ascii=False,indent=2),encoding='utf-8')
downloads2=out/'runs/setup-ec2-2/downloads.json'
if downloads2.exists():
    d=json.loads(downloads2.read_text());acc=json.loads((out/'download-accounting.json').read_text())
    acc['followup_ec2_2_wheels_and_metadata_bytes']=d['payload_and_metadata_bytes']
    acc['known_primary_cumulative_network_bytes']=acc['known_cumulative_network_bytes']
    acc['known_cumulative_network_bytes']+=d['payload_and_metadata_bytes']
    acc['saved_distinct_payload_bytes']+=d['payload_and_metadata_bytes']
    acc['conservative_accounting_bytes']+=d['payload_and_metadata_bytes']
    acc['under_limit_conservative']=acc['conservative_accounting_bytes']<acc['declared_limit_bytes']
    acc['followup_source']='runs/setup-ec2-2/downloads.json; compressed wheels pinned URL/size/PyPI SHA256; setup retries reused verified payloads'
    assert acc['under_limit_conservative']
    (out/'download-accounting.json').write_text(json.dumps(acc,indent=2))
    extra=[dict(url=r['url'],path='/home/ubuntu/rca/T-014/wheels/'+r['filename']+' (host3.26.62.217)',bytes=r['actual_bytes'],sha256=r['sha256'],md5='',published_checksum_match='PyPI SHA256 matches saved Linux wheel; metadata bytes included in download accounting separately') for r in d['wheels']]
    with (out/'download-sources.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['url','path','bytes','sha256','md5','published_checksum_match']);w.writeheader();w.writerows(downloads+extra)
print(json.dumps(dict(files=len(rows),scopes=totals,known_downloaded_bytes=known,python_cache_logical_bytes=cache_logical)))
