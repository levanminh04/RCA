"""Independent offline checks for source cards and Nezha reference claims."""
import collections,csv,datetime as dt,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];B=ROOT/'results/T-012'
def epoch(t):return dt.datetime.fromisoformat(t[:19]).replace(tzinfo=dt.timezone.utc).timestamp()
def main():
    out=B/'runs/final-check-001';out.mkdir(exist_ok=False)
    snapshots=[]
    for run in ['run-001','run-002','run-003']:
        m=json.loads((B/'runs'/run/'source-manifest.json').read_text(encoding='utf-8'))
        for x in m['items']:
            if x.get('status')!='ok':continue
            p=B/x['path']; raw=p.read_bytes();snapshots.append(dict(path=x['path'],ok=len(raw)==x['bytes'] and hashlib.sha256(raw).hexdigest()==x['sha256']))
    profiles=json.loads((B/'profiles.json').read_text(encoding='utf-8'));cards=(B/'the-dataset.md').read_text(encoding='utf-8'); chunks=re.split(r'(?m)^# ',cards)[2:]
    cardscheck=dict(profiles=len(profiles),card_sections=len(chunks),headings=[re.findall(r'(?m)^## (\d+)\.',s) for s in chunks],all_profile_sources_exist=all((B/x['path']).exists() for p in profiles for x in p['sources']))
    cardscheck['ok']=cardscheck['card_sections']==len(profiles) and all(x==[str(i) for i in range(1,11)] for x in cardscheck['headings']) and cardscheck['all_profile_sources_exist']
    n=ROOT/'results/T-008';audit=json.loads((n/'runs/file-audit-001/summary.json').read_text(encoding='utf-8'));sym=json.loads((n/'runs/symptoms-002/result.json').read_text(encoding='utf-8'))
    windows=[]
    for a in audit['results']:
        if '/construct_data/' not in a['path'] or '/trace/' not in a['path']:continue
        system,_,date=a['path'].split('/')[:3];points=collections.defaultdict(list)
        for p in (ROOT/'data/ngoai-rcaeval/nezha'/system/'construct_data'/date/'metric').glob('*_metric.csv'):
            with p.open(encoding='utf-8-sig',newline='') as f:
                for r in csv.DictReader(f):
                    t=epoch(r['Time'])
                    if a['start_epoch']//60*60<=t<(a['end_epoch']//60+1)*60:points[r['PodName']].append(t)
        windows.append(dict(system=system,date=date,trace_start=a['start_epoch'],trace_end=a['end_epoch'],pods=len(points),minute_envelope_n=dict(collections.Counter(len(ts) for ts in points.values())),strict_bounds_n=dict(collections.Counter(sum(a['start_epoch']<=t<=a['end_epoch'] for t in ts) for ts in points.values())),outside_strict_rows=sum(sum(not a['start_epoch']<=t<=a['end_epoch'] for t in ts) for ts in points.values())))
    cal=sym['calibration']; result=dict(source_hash_checks=snapshots,cards=cardscheck,reference_windows=windows,calibration_n=len(cal),calibration_groups=[dict(dataset=k[0],date=k[1],reference_n=k[2],control_n=k[3],rows=v) for k,v in collections.Counter((x['dataset'],x['date'],x['reference_n'],x['control_n']) for x in cal).items()],calibration_zero_band=sum(x['zero_band'] for x in cal),clock_empty_rows=[dict(clock=k[0],empty=k[1],rows=v) for k,v in collections.Counter((x['clock_interpretation'],x['n']==0) for x in sym['results']).items()])
    result['ok']=all(x['ok'] for x in snapshots) and cardscheck['ok']
    (out/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='source_hash_checks'},ensure_ascii=False))
    if not result['ok']:raise SystemExit(1)
if __name__=='__main__':main()
