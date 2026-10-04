"""R1: independent arithmetic decomposition of the 25 saved fse-ob DELAY cases.

No official method calls. Reuse T006 metric rankings as endpoint evidence.
Run: py312-pin/Scripts/python.exe results/T-013/scripts/kiem_cua_so_delay.py
All writes are in the explicitly approved R1 scope; keep failed runs.
"""
import os
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['OMP_NUM_THREADS'] = os.environ['OPENBLAS_NUM_THREADS'] = '1'
import csv
import datetime as dt
import hashlib
import json
import sys
import time
import traceback
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path('D:/RCA-flashticket')
OUT = ROOT / 'results/T-013'
RAW = Path('D:/RCA-ext/data/fse-ob')
P10 = Path('D:/RCA-ext/work/T-006/l4-nsigma-fse-ob-len10-lan1/output/results')
P20 = Path('D:/RCA-ext/work/T-006/l4-nsigma-fse-ob-lan1/output/results')
ZONE = dt.timezone(dt.timedelta(hours=7))
RUN = OUT / 'runs' / ('sua-R1-' + dt.datetime.now(ZONE).strftime('%Y%m%d-%H%M%S'))
RUN.mkdir(exist_ok=False)
START = time.perf_counter()
MANIFEST = {'run_dir': str(RUN), 'started_at': dt.datetime.now(ZONE).isoformat(),
            'python': sys.version, 'executable': sys.executable,
            'numpy': np.__version__, 'pandas': pd.__version__, 'sources': [],
            'method_calls': 'none; independent mean/variance/max arithmetic only',
            'scope': '25 previously run fse-ob DELAY cases; no locked data'}

def dump(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')

def progress(event, **kw):
    row = {'time': dt.datetime.now(ZONE).isoformat(), 'elapsed_sec': time.perf_counter()-START,
           'event': event, **kw}
    with (RUN/'tien-do.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps(row, ensure_ascii=False, allow_nan=False)+'\n')
    print(event, kw, flush=True)

def source(path):
    path = Path(path)
    MANIFEST['sources'].append({'path': str(path), 'bytes': path.stat().st_size,
                               'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    return path

def write_csv(path, rows):
    assert rows
    with Path(path).open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)

def preprocess_half(d):
    # Literal independent reconstruction of RE preprocess(dataset='fse-ob', dk=False).
    d = d.drop(columns=['time.1'], errors='ignore')
    if 'time' in d:
        d = d.drop(columns='time')
    elif 'Time' in d:
        d = d.drop(columns='Time')
    d = d.loc[:, (d != d.iloc[0]).any()].copy()
    for c in d:
        if c.endswith('_mem'):
            d[c] = d[c] / 1e6
    return d

def score_parts(normal, post):
    """No case/root label argument. Corrected two-pass population variance.

    Matches sklearn1.6 single-column fit arithmetic, including the near-constant
    numerical error bound. Does not call scaler, author or sklearn helpers.
    """
    a, b = preprocess_half(normal), preprocess_half(post)
    columns = [c for c in a if c in b]
    records = []
    for c in columns:
        x = a[c].to_numpy(dtype=np.float64)
        y = b[c].to_numpy(dtype=np.float64)
        assert np.isfinite(x).all() and np.isfinite(y).all()
        n = len(x)
        mean = np.sum(x, dtype=np.float64)/n
        centered = x-mean
        correction = np.sum(centered, dtype=np.float64)
        var = (np.sum(centered*centered, dtype=np.float64)-correction**2/n)/n
        assert var >= 0
        eps = np.finfo(np.float64).eps
        bound = n*eps*var+(n*mean*eps)**2
        near = bool(var <= bound)
        std = float(np.sqrt(var)); scale = 1. if near else std
        values = (y-mean)/scale
        records.append({'metric': c, 'candidate': True, 'normal_constant': False, 'post_constant': False,
                        'n_normal': n, 'n_post': len(y), 'mean': float(mean),
                        'variance_ddof0_corrected': float(var), 'std_ddof0': std,
                        'constant_bound': float(bound), 'near_constant': near,
                        'scale_effective': scale, 'max_post': float(np.max(y)),
                        'min_post': float(np.min(y)), 'score': float(max(values)),
                        'service': c.split('_')[0].replace('-db','')})
    ranks = [r['metric'] for r in sorted(records, key=lambda r:r['score'], reverse=True)]
    return records, ranks, {'normal_removed': [c for c in normal if c not in a],
                            'post_removed': [c for c in post if c not in b]}

def service_rank(ranks):
    out = []
    for c in ranks:
        s = c.split('_')[0].replace('-db','')
        if s not in out:
            out.append(s)
    return out

def saved_rank(path):
    o = json.loads(source(path).read_text(encoding='utf-8'))
    assert set(o) == {'0'}, (str(path), list(o))
    return o['0']

def endpoint_check(current, previous, rows):
    scores = {r['metric']:r['score'] for r in rows}
    assert set(current) == set(previous)
    # Allow only numerical ties if an endpoint's stable order differs.
    tie_valid = all(scores[previous[i]] >= scores[previous[i+1]]-1e-10*max(1,abs(scores[previous[i]]),abs(scores[previous[i+1]]))
                    for i in range(len(previous)-1))
    assert tie_valid
    return {'exact_metric_ranks': current == previous, 'tie_aware_valid': tie_valid,
            'exact_service_ranks': service_rank(current) == service_rank(previous)}

def main():
    progress('start', budget_seconds=600, output_budget_bytes=10_000_000)
    files = sorted(P10.glob('*_delay_*.json'))
    assert len(files) == 25
    assert {p.name for p in files} == {p.name for p in P20.glob('*_delay_*.json')}
    metrics, cases, comparisons, variants, checks, candidate_rows = [], [], [], {}, [], []
    source(__file__)
    (RUN/'script.py').write_bytes(Path(__file__).read_bytes())
    MANIFEST['script_snapshot'] = str(RUN/'script.py')
    for p in files:
        case = p.stem
        service, fault, trial = case.split('_')
        assert fault == 'delay'
        folder = RAW/(service+'_'+fault)/trial
        raw = pd.read_csv(source(folder/'simple_data.csv'))
        inj = int(source(folder/'inject_time.txt').read_text().strip())
        # Runner cleanup is applied to the full recording before time splitting.
        d = raw.drop(columns=['time.1'], errors='ignore')
        d = d.loc[:,~d.columns.str.endswith('_latency-50')]
        d = d.replace([np.inf,-np.inf],np.nan).ffill().fillna(0)
        d = d.rename(columns={c:c.replace('_latency-90','_latency') for c in d if c.endswith('_latency-90')})
        nfull, afull = d[d.time<inj], d[d.time>=inj]
        assert len(nfull)==360 and len(afull)==361
        assert np.all(np.diff(d.time.to_numpy()) == 1)
        old10, old20 = saved_rank(p), saved_rank(P20/p.name)
        combos = [('N300-A300',nfull.tail(300),afull.head(300)),
                  ('N360-A300',nfull.tail(600),afull.head(300)),
                  ('N300-A361',nfull.tail(300),afull.head(600)),
                  ('N360-A361',nfull.tail(600),afull.head(600))]
        results = {}
        for name,n,a in combos:
            rows, ranks, removed = score_parts(n,a)
            sr = service_rank(ranks)
            # Root label is used only AFTER scoring/ranking to evaluate the saved case.
            root_rank = sr.index(service)+1 if service in sr else len(sr)+1
            contribution = max(0,6-root_rank)/5
            results[name] = {'metric_ranks':ranks,'service_ranks':sr,
                             'root_service_rank':root_rank, 'Avg5_contribution': contribution,
                             'removed':removed, 'rows':rows}
            for row in rows:
                metrics.append({'case':case,'variant':name,**row})
            # Keep non-candidates explicit instead of hiding the constant-column intersection.
            for c in n.columns:
                if c in ['time','Time','time.1'] or c in ranks:
                    continue
                x=n[c].to_numpy(dtype=np.float64); y=a[c].to_numpy(dtype=np.float64)
                if c.endswith('_mem'):
                    x=x/1e6; y=y/1e6
                mean=np.sum(x,dtype=np.float64)/len(x); centered=x-mean
                var=(np.sum(centered*centered,dtype=np.float64)-np.sum(centered,dtype=np.float64)**2/len(x))/len(x)
                bound=len(x)*np.finfo(np.float64).eps*var+(len(x)*mean*np.finfo(np.float64).eps)**2
                metrics.append({'case':case,'variant':name,'metric':c,'candidate':False,
                                'normal_constant':bool(np.all(x==x[0])), 'post_constant':bool(np.all(y==y[0])),
                                'n_normal':len(x),'n_post':len(y),'mean':float(mean),
                                'variance_ddof0_corrected':float(var),'std_ddof0':float(np.sqrt(var)),
                                'constant_bound':float(bound),'near_constant':bool(var<=bound),
                                'scale_effective':None,'max_post':float(max(y)),'min_post':float(min(y)),
                                'score':None,'service':c.split('_')[0].replace('-db','')})
            variant = {'case':case,'source':str(folder/'simple_data.csv'),'variant':name,
                       'n_normal':len(n),'n_post':len(a),'metric_candidates':len(rows),
                       'service_candidates':len(sr),'root_rank':root_rank,'Avg5_contribution':contribution,
                       'top_metric':ranks[0], 'root_winning_metric':next(c for c in ranks if c.split('_')[0].replace('-db','')==service)}
            candidate_rows.append(variant)
            repeated, rr, _ = score_parts(n,a)
            reversed_rows, reversed_ranks, _ = score_parts(n[list(reversed(n.columns))],a[list(reversed(a.columns))])
            base = {r['metric']:r['score'] for r in rows}
            repeat_equal = repeated == rows and rr == ranks
            score_equal = all(np.isclose(r['score'],base[r['metric']],atol=1e-10,rtol=1e-10) for r in reversed_rows)
            assert repeat_equal and score_equal
            reverse_valid = endpoint_check(reversed_ranks,ranks,reversed_rows)
            checks.append({'case':case,'variant':name,'repeat_equal':repeat_equal,
                           'column_permutation_scores_equal':score_equal,
                           'column_permutation_exact_ranks':reversed_ranks==ranks,
                           'column_permutation_tie_aware':reverse_valid['tie_aware_valid']})
        check10 = endpoint_check(results['N300-A300']['metric_ranks'],old10,results['N300-A300']['rows'])
        check20 = endpoint_check(results['N360-A361']['metric_ranks'],old20,results['N360-A361']['rows'])
        assert check10['exact_service_ranks'] and check20['exact_service_ranks']
        c0,cN,cA,cNA = [results[k]['Avg5_contribution'] for k in ['N300-A300','N360-A300','N300-A361','N360-A361']]
        # Order-independent Shapley decomposition includes any candidate-set change.
        effectN = .5*((cN-c0)+(cNA-cA)); effectA = .5*((cA-c0)+(cNA-cN))
        assert np.isclose(effectN+effectA,cNA-c0,atol=1e-12)
        sets = [set(results[k]['metric_ranks']) for k,_,_ in combos]
        r0,rN,rA,rNA = [results[k]['root_service_rank'] for k in ['N300-A300','N360-A300','N300-A361','N360-A361']]
        top0 = results['N300-A300']['metric_ranks'][0]; topNA = results['N360-A361']['metric_ranks'][0]
        cases.append({'case':case,'n_L10':300,'a_L10':300,'n_L20':360,'a_L20':361,
                      'root_rank_N300_A300':r0,'root_rank_N360_A300':rN,'root_rank_N300_A361':rA,'root_rank_N360_A361':rNA,
                      'Avg5_L10':c0,'Avg5_L20':cNA,'delta_Avg5_L20_minus_L10':cNA-c0,
                      'baseline_effect_shapley':effectN,'post_effect_shapley':effectA,
                      'baseline_then_post_baseline_delta':cN-c0,'baseline_then_post_post_delta':cNA-cN,
                      'post_then_baseline_post_delta':cA-c0,'post_then_baseline_baseline_delta':cNA-cA,
                      'candidate_sets_identical':all(s==sets[0] for s in sets),
                      'metric_candidates_L10':len(sets[0]),'metric_candidates_L20':len(sets[-1]),
                      'added_candidates':';'.join(sorted(sets[-1]-sets[0])),
                      'removed_candidates':';'.join(sorted(sets[0]-sets[-1])),
                      'top_metric_L10':top0,'top_metric_L20':topNA,
                      'endpoint10_exact_metric':check10['exact_metric_ranks'],'endpoint20_exact_metric':check20['exact_metric_ranks']})
        variants[case] = {k:{a:b for a,b in v.items() if a!='rows'} for k,v in results.items()}
        comparisons.append({'case':case,'L10':check10,'L20':check20})
        progress('case_complete', case=case, rank_path=[r0,rN,rA,rNA],
                 candidate_change=not cases[-1]['candidate_sets_identical'],elapsed_case_count=len(cases))
        assert time.perf_counter()-START < 600
    write_csv(RUN/'per-metric.csv',metrics)
    write_csv(RUN/'per-case.csv',cases)
    write_csv(RUN/'variants.csv',candidate_rows)
    dump(RUN/'rankings.json',variants)
    dump(RUN/'checks.json',{'endpoints':comparisons,'repeat_permutation':checks})
    avg10 = sum(c['Avg5_L10'] for c in cases)/25; avg20 = sum(c['Avg5_L20'] for c in cases)/25
    bn = sum(c['baseline_effect_shapley'] for c in cases)/25
    pa = sum(c['post_effect_shapley'] for c in cases)/25
    assert np.isclose(avg10,.936,atol=1e-12) and np.isclose(avg20,.680,atol=1e-12)
    assert np.isclose(bn+pa,avg20-avg10,atol=1e-12)
    hybrid_avg = {name:sum(v[name]['Avg5_contribution'] for v in variants.values())/25
                  for name in ['N300-A300','N360-A300','N300-A361','N360-A361']}
    summary = {'run_dir':str(RUN),'cases':25,'Avg5_L10':avg10,'Avg5_L20':avg20,
               'Avg5_four_variants':hybrid_avg,
               'difference_L10_minus_L20':avg10-avg20,'changed_ranks':sum(c['root_rank_N300_A300']!=c['root_rank_N360_A361'] for c in cases),
               'down':sum(c['root_rank_N300_A300']<c['root_rank_N360_A361'] for c in cases),
               'up':sum(c['root_rank_N300_A300']>c['root_rank_N360_A361'] for c in cases),
               'down_top_L20_mem':sum(c['root_rank_N300_A300']<c['root_rank_N360_A361'] and c['top_metric_L20'].endswith('_mem') for c in cases),
               'candidate_change_cases':[c['case'] for c in cases if not c['candidate_sets_identical']],
               'baseline_effect_shapley_average':bn,'post_effect_shapley_average':pa,
               'all_endpoint_metric_ranks_exact':all(c['endpoint10_exact_metric'] and c['endpoint20_exact_metric'] for c in cases),
               'all_endpoint_service_ranks_exact':True,'all_repeat_permutation_checks_pass':True,
               'elapsed_seconds_shared_machine':time.perf_counter()-START,
               'attribution':'arithmetic effect of changed recording bounds; not physical causality or optimal window',
               'shapley_formula':'E_N=0.5*((cN-c0)+(cNA-cA)); E_A=0.5*((cA-c0)+(cNA-cN))',
               'status':'complete'}
    dump(RUN/'summary.json',summary)
    write_csv(OUT/'trung-gian/cua-so-delay-ca.csv',cases)
    write_csv(OUT/'trung-gian/cua-so-delay-metric.csv',metrics)
    write_csv(OUT/'trung-gian/cua-so-delay-variants.csv',candidate_rows)
    dump(OUT/'trung-gian/cua-so-delay-summary.json',summary)
    progress('complete', summary=summary)
    MANIFEST['elapsed_seconds_shared_machine'] = time.perf_counter()-START
    MANIFEST['output_files'] = [{'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
                                for p in sorted(RUN.iterdir()) if p.is_file() and p.name!='manifest.json']
    dump(RUN/'manifest.json',MANIFEST)
    print('OUTPUT_BYTES',sum(p.stat().st_size for p in RUN.iterdir() if p.is_file()),flush=True)

try:
    main()
except Exception:
    (RUN/'failure.txt').write_text(traceback.format_exc(),encoding='utf-8')
    MANIFEST['status']='failed'; MANIFEST['elapsed_seconds_shared_machine']=time.perf_counter()-START
    dump(RUN/'manifest.json',MANIFEST)
    progress('failed',traceback=traceback.format_exc())
    raise
