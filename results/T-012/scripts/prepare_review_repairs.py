"""Fetch only approved R1 release metadata and R3 Drive listing; pin R4 source."""
import concurrent.futures,datetime,hashlib,json,urllib.request
from pathlib import Path
R=Path(__file__).resolve().parents[3];B=R/'results/T-012';O=B/'runs/review-sources-001'
def fetch(name,url):
    row=dict(name=name,url=url)
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 T003 source inspection'}),timeout=60) as f:
            data=f.read();row.update(final_url=f.url,status=f.status)
        p=O/'sources'/name;p.write_bytes(data)
        row.update(path='sources/'+name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
    except Exception as e:row.update(error=str(e))
    return row
def main():
    (O/'sources').mkdir(parents=True,exist_ok=False)
    targets=[('zenodo-'+str(i)+'.json','https://zenodo.org/api/records/'+str(i)) for i in (18342898,19335897,19522409)]
    targets += [('drive-root.html','https://drive.google.com/drive/folders/1wGiEnu4OkWrjPxfx5ZTROnU37-5UDoPM'),('fault-catalog-commit.json','https://api.github.com/repos/FudanSELab/train-ticket-fault-replicate/commits/master')]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as p:rows=list(p.map(lambda x:fetch(*x),targets))
    save=lambda name,x:(O/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    commit=next(x for x in rows if x['name']=='fault-catalog-commit.json')
    if 'path' in commit:
        rev=json.loads((O/commit['path']).read_text(encoding='utf-8'))['sha']
        rows.append(fetch('fault-catalog-README.md','https://raw.githubusercontent.com/FudanSELab/train-ticket-fault-replicate/'+rev+'/README.md'))
    plans=[]
    for i,folder in [(18342898,'anomod'),(19335897,'trca'),(19522409,'fse')]:
        p=O/'sources'/('zenodo-'+str(i)+'.json')
        if not p.exists():continue
        m=json.loads(p.read_text());assert m['id']==i
        f=m['files'][0]
        plans.append(dict(path=folder+'/'+f['key'],url=f['links']['self'],bytes=f['size'],md5=f['checksum'].split(':')[1],record_id=i,doi=m['doi'],license=m['metadata']['license']))
    assert sum(x['bytes'] for x in plans)==628411611
    save('manifest.json',dict(sources=rows,created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),bank_telemetry_read=False))
    save('download-plan.json',plans)
    print(json.dumps(dict(plans=plans,source_errors=[x for x in rows if 'error' in x]),ensure_ascii=False))
if __name__=='__main__':main()
