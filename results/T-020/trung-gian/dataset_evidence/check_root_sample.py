from pathlib import Path
import csv, json, re
from functools import lru_cache
ROOT=Path('D:/RCA-flashticket'); OUT=ROOT/'results/T-020/trung-gian/dataset_evidence'
@lru_cache(None)
def load(p):
    assert p.startswith('results/') and 'locked' not in p
    assert p != 'results/T-010/runs/schema-samples.json', 'Known mixed schema/raw payload: do not replay'
    return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def get(d,key):
    for t in key.strip('/').split('/'):
        t=t.replace('~1','/').replace('~0','~')
        d=d[int(t)] if isinstance(d,list) else d[t]
    return d
def csvrows(p):return list(csv.DictReader((ROOT/p).open(encoding='utf-8-sig')))
source=csvrows('results/T-020/trung-gian/root/numeric-leaves.csv')
out=[]
for x in source:
    if x['selected']!='True' or x['task'] not in ['T-002','T-003','T-008','T-009','T-010','T-011','T-012','T-019']:continue
    p=x['path'];k=x['key']; d=load(p); v=get(d,k); new=None; reason='OPEN: cần đọc lại số đo thô TX1; prompt T020 cấm. Giữ original, không coi copy scalar là kiểm.'; support=''; state='OPEN'
    if x['task']=='T-002':
        if k.endswith('/n_inspected'):
            cc=load('results/T-002/local-inspection/run-002/cases.json');new=sum(z['dataset']=='re2tt' for z in cc);reason='Count per-case results';support='results/T-002/local-inspection/run-002/cases.json'
        elif '/faults_and_case_counts/' in k or k.endswith('/n_faults'):
            i=int(k.split('/')[1]);suite=d[i]['dataset'].lower().replace('-','');cc=[z for z in csvrows('results/T-002/public-metadata/run-002/cases-from-directories.csv') if z['suite']==suite]
            new=len({z['fault'] for z in cc}) if k.endswith('/n_faults') else sum(z['fault']==k.split('/')[-1] for z in cc);reason='Group/count original public case metadata';support='results/T-002/public-metadata/run-002/cases-from-directories.csv'
        elif '/artifacts/' in k:
            a=d['artifacts'][int(k.split('/')[2])]; assert a['path'].startswith('results/');new=(ROOT/a['path']).stat().st_size;reason='Current byte count of original result artifact';support=a['path']
    elif x['task']=='T-003':
        if '/members/' in k:
            ai=int(k.split('/')[1]);mi=int(k.split('/')[3]);a=d[ai];m=a['members'][mi]
            originals=load('results/T-011/runs/inspect-008/archives.json')
            candidates=[q for z in originals if a['variant'] in z['path'] and z['path'].endswith(a['path']) for q in z['members'] if q['name']==m['path']]
            if candidates and k.endswith(('compressed_bytes','uncompressed_bytes')):
                field='compressed' if k.endswith('/compressed_bytes') else 'bytes';new=candidates[0][field];reason='Independent CRC-verified archive member metadata, exact name';support='results/T-011/runs/inspect-008/archives.json'
            else:reason='OPEN: compression-method metadata chỉ một central-directory snapshot; không inflate/tải lại ZIP trong T020; file-size checks khác đã làm.'
        elif '/range_requests/' in k:
            q=get(d,k.rsplit('/',1)[0]);new=q['end']-q['start']+1;reason='Range inclusive byte count end-start+1';support=p+k.rsplit('/',1)[0]
        elif k=='/rows/1/archive_bytes':
            s=load('results/T-003/runs/resources-final-001/summary.json');new=sum(z['download_bytes'] for z in s['downloads'] if z['dataset']=='Eadro');reason='Sum two original ZIP downloads';support='results/T-003/runs/resources-final-001/summary.json #downloads'
    elif x['task']=='T-008':
        if k.endswith('/invalid'):
            a=d['results'][int(k.split('/')[2])];prof=get(d,k.rsplit('/',1)[0]);new=a['rows']-prof['finite'];reason='Complement rows - finite; arithmetic consistency, không recount raw';support=p+' #same file rows/finite'
    elif x['task']=='T-009':
        if k=='/datasets/SN/roots':
            labels=load('results/T-009/runs/inspect-004/labels-all.json');new=len({f['name'] for z in labels if z['dataset']=='SN' for f in z['label']['faults']});reason='Unique declared root names after union labels';support='results/T-009/runs/inspect-004/labels-all.json'
        elif '/duplicate_member_pairs/' in k:
            q=d['duplicate_member_pairs'][int(k.split('/')[2])];inv=load('results/T-009/runs/inspect-004/nested-inventory.json'); matches=[z for z in inv if z['member']==q['outer'] and z['sha256']==q['sha256']];new=matches[0]['bytes'] if matches else None;reason='Exact member/hash match in original per-member metadata';support='results/T-009/runs/inspect-004/nested-inventory.json'
    elif x['task']=='T-010':
        rc=load('results/T-010/runs/inspect-002/raw-cases.json')
        if '/raw_case_trace_counts/' in k:
            case=k.split('/')[-1];new=sum(z['trace_ids'] for z in rc if z['case_directory']==case);reason='Sum per-case original inspector counts';support='results/T-010/runs/inspect-002/raw-cases.json'
        else:
            q=d[int(k.split('/')[1])];case=q['case'];rr=[z for z in rc if z['case_directory']==case]
            if k.endswith('/trace_ids'):new=sum(z['trace_ids'] for z in rr)
            elif '/span_is_error/' in k:
                new=sum(z['is_error_values'].get(k.split('/')[-1],0) for z in rr)
                samecase=[z for z in d if z['case']==case]
                if len(samecase)>1:
                    aggregate=sum(z['span_is_error'].get(k.split('/')[-1],0) for z in samecase)
                    assert aggregate==new,(case,aggregate,new)
                    new=None
                    reason=f'OPEN selected member count; per-case aggregate independently matches {aggregate}, but {len(samecase)} span CSV members in case; không chứng minh từng member từ case sum'
            if new is not None:reason='Independent first inspector per-case counters; counts are aggregate, no raw reread'
            support='results/T-010/runs/inspect-002/raw-cases.json #'+case
    elif x['task']=='T-011':
        reason='OPEN: delta histogram/time max từng NPY case muốn recount phải đọc số đo TX1; prompt cấm. Không coi nhắc lại histogram ở summaries là independent recompute. Whole-sample counts/bytes đã kiểm riêng.'
    elif x['task']=='T-012':
        if '/histograms/datetime/' in k:
            date=k.split('/')[-1];new=sum(z['datetime']==date for z in csvrows('results/T-012/runs/bank-label-reproduce-002/record.csv'));reason='Count public label rows, không telemetry';support='results/T-012/runs/bank-label-reproduce-002/record.csv'
        elif '/rows/' in k:
            q=d['rows'][int(k.split('/')[2])];na=load('results/T-008/runs/file-audit-001/summary.json');matches=[z for z in na['results'] if z['path']==q['nezha_path']];new=matches[0]['bytes'];reason='Exact named reused member byte metadata from Nezha original file audit';support='results/T-008/runs/file-audit-001/summary.json #'+q['nezha_path']
    elif x['task']=='T-019':
        if '/roots/' in k or '/faults/' in k:
            i=int(k.split('/')[1]);ds=d[i]['dataset'];cc=csvrows('results/T-019/census-cases.csv');field='root' if '/roots/' in k else 'fault';new=sum(z['dataset']==ds and z[field]==k.split('/')[-1] for z in cc);reason='Group count public census';support='results/T-019/census-cases.csv'
        elif k=='/comparison_count':
            pp=p.rsplit('/',1)[0]+'/public-metric-comparisons.json';new=len(load(pp));reason='Count saved independent pair comparison records';support=pp
        elif k=='/details/received_payload_bytes':
            pref='results/T-019/';sbytes=sum(load(pref+'sources-audit/'+f)['total_bytes'] for f in ['network-manifest.json','architecture-manifest.json','diagram-metadata-manifest.json'])+load(pref+'sources-audit/diagram-manifest.json')['bytes']
            new=load(pref+'acquisition/manifest.json')['network_bytes']+load(pref+'lineage/download-manifest.json')['network_bytes']+sbytes+load(pref+'runner-source/manifest.json')['network_bytes'];reason='Sum disjoint network source/acquisition/lineage/runner manifests';support='results/T-019/verify_final.py:52 + manifests (recomputed, old script not executed)'
    if new is not None:state='MATCH' if new==v else 'MISMATCH'
    out.append(dict(task=x['task'],path=p,key=k,original=v,recomputed='' if new is None else new,status=state,reason=reason,support=support or 'OPEN owner=Người làm P3/Minh; input=được phép recount raw hoặc independent metadata; giải sau G1/G3',sampling_hash=x['sampling_hash']))
with (OUT/'root-selected-checks.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
assert not any(x['status']=='MISMATCH' for x in out),[x for x in out if x['status']=='MISMATCH']
print(json.dumps(dict(rows=len(out),MATCH=sum(x['status']=='MATCH' for x in out),OPEN=sum(x['status']=='OPEN' for x in out)),ensure_ascii=False))
