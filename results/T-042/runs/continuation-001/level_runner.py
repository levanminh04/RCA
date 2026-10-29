"""Exact Nezha log/vote kernels over observed severity histograms, no raw reread."""
from collections import defaultdict
from datetime import datetime, timezone
import contextlib
import json
import math
import os
from pathlib import Path
import sys
import time
import traceback
import pandas as pd
from simple_runner import ROOT, OUT, load_kernels, read, sha, write, tie_groups


def frames(hist, branch):
    rows={'N':[],'A':[]}
    for record in hist['resolved_histogram']:
        level=record['value']
        if branch!='L0' and isinstance(level,str):level=level.upper()
        rows[record['phase']].extend([(record['service'],level)]*record['count'])
    if branch!='L2':
        for record in hist['unknown_histogram']:
            rows[record['phase']].extend([(record['service'],None)]*record['count'])
    return {p:pd.DataFrame(value,columns=['service_name','level']) for p,value in rows.items()}


def independent(frame, native):
    counts={}
    for p in ['N','A']:
        counts[p]={str(s):dict(total=len(g),info=int((g.level=='INFO').sum()),nonINFO=int((g.level!='INFO').sum()),
                       unknown=int(g.level.isna().sum())) for s,g in frame[p].groupby('service_name')}
    allservices=set(counts['N'])|set(counts['A']);changes={};drops={}
    for s in allservices:
        n=counts['N'].get(s,dict(total=0,info=0,nonINFO=0));a=counts['A'].get(s,dict(total=0,info=0,nonINFO=0))
        nr=n['nonINFO']/n['total'] if n['total'] else 0;ar=a['nonINFO']/a['total'] if a['total'] else 0
        if ar>1.5*nr and a['nonINFO']>0 and a['total']>10:changes[s]=ar-nr
        if n['info']>40 and a['info']<.6*n['info']:drops[s]=(n['info']-a['info'])/n['info']
    if changes:
        stage='error_ratio_increase';values=changes
    elif drops:
        stage='INFO_count_reduction';values=drops
    else:
        stage='abnormal_nonINFO_count';values={s:c['nonINFO'] for s,c in counts['A'].items() if c['nonINFO']}
        if len(values)>=2:values={s:v for s,v in values.items() if 'frontend' not in s.lower()}
    # The exact kernel may choose any ordering inside a component tie.
    expected=sorted(values.values(),reverse=True)[:5]
    assert [values[s] for s in native]==expected,(stage,native,expected)
    return dict(status='PASS',stage=stage,counts=counts,eligible_scores=values,
                component_ties=tie_groups(values),native_order=native,
                unknown_semantics='None != INFO is True in the exact pandas kernel; unknown is not asserted to be an observed error')


def main():
    seed=sys.argv[1];assert os.environ.get('PYTHONHASHSEED')==seed
    folder=OUT/f'level-seed{seed}-001';folder.mkdir(exist_ok=False)
    write(folder/'config.json',dict(seed=seed,branches=['L0','L1','L2'],plan_sha256=sha(OUT/'supplementary-plan.json'),
                                  labels_read=False,script_sha256=sha(__file__),utc=datetime.now(timezone.utc).isoformat()))
    histdir=OUT/'contracts/histogram-001';manifest=read(histdir/'full-summary.json');assert manifest['status']=='PASS' and manifest['cases']==22
    for rec in manifest['records']:assert sha(ROOT/rec['path'])==rec['sha256']
    # Histogram producer manifest schema is checked explicitly by the caller.
    hfiles={p.stem:p for p in (histdir/'cases').glob('dev-*.json')}
    assert len(hfiles)==22
    frozen=read(OUT/'simple-full-001/diagnoses-frozen.json')
    partial={row['opaque_id']:row for row in frozen['records'] if row['branch']=='N1-partial'}
    kernels,pins=load_kernels();nz=kernels[2];write(folder/'source-pins.json',pins)
    start=time.perf_counter();records=[]
    with (folder/'stdout.txt').open('x',encoding='utf-8') as stdout:
        with contextlib.redirect_stdout(stdout):
            for oid,path in sorted(hfiles.items()):
                h=read(path);assert h['status']=='PASS' and not h['labels_read']
                source=partial[oid];assert sha(ROOT/source['path'])==source['sha256']
                mt=read(ROOT/source['path'])['result']
                for branch in ['L0','L1','L2']:
                    frame=frames(h['histogram'],branch)
                    result=nz['_detect_log_anomalies'](frame['N'],frame['A'])
                    audit=independent(frame,result)
                    rank=nz['_vote_combine_results'](mt['metric_ranks'],mt['trace_ranks'],result)
                    scores={}
                    for nodes,weight in [(mt['metric_ranks'],1.2),(mt['trace_ranks'],1.),(result,1.)]:
                        for i,s in enumerate(nodes[:5]):scores[s]=scores.get(s,0)+(5-i)*weight
                    assert rank==sorted(scores,key=lambda s:-scores[s])[:5]
                    dest=folder/f'{oid}-{branch}.json'
                    write(dest,dict(opaque_id=oid,branch=branch,seed=seed,result=dict(log_ranks=result,
                         metric_ranks=mt['metric_ranks'],trace_ranks=mt['trace_ranks'],scores=scores,
                         native_ranks=rank,tie_groups=tie_groups(scores),log_audit=audit),
                         sources=dict(histogram=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha(path)),metric_trace=source),
                         labels_read=False,raw_payload_saved=False))
                    records.append(dict(opaque_id=oid,branch=branch,path=dest.relative_to(ROOT).as_posix(),sha256=sha(dest)))
    write(folder/'diagnoses-frozen.json',dict(records=records,labels_read=False,completed=True,seed=seed,
                                            utc=datetime.now(timezone.utc).isoformat()))
    write(folder/'cost.json',dict(wall_s=time.perf_counter()-start,records=len(records)))
    print(json.dumps(dict(seed=seed,status='FROZEN',records=len(records))))


if __name__=='__main__':main()
