"""Independent arithmetic and window audit. No labels in input/method audit."""
import csv
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re


def quantile(values, p=0.95):
    a = sorted(float(v) for v in values if math.isfinite(float(v)))
    x = (len(a)-1)*p
    low = int(math.floor(x))
    high = int(math.ceil(x))
    # Match the documented linear interpolation, independently of numpy.
    return a[low] + (a[high]-a[low])*(x-low)


def arithmetic(inputs, config, result):
    totals = {s: dict(metric=0, trace=0, log=0, score=0) for s in result['scores']}
    max_diff = 0.0
    for key, ns in inputs['normal_metrics'].items():
        n = [float(x) for x in ns if math.isfinite(float(x))]
        a = [float(x) for x in inputs['incident_metrics'][key] if math.isfinite(float(x))]
        row = result['metrics'][key]
        assert row['n_normal'] == len(n) and row['n_incident'] == len(a)
        if len(n) < 2 or not a:
            assert row['status'] == 'unavailable' and row['vote'] == 0
            continue
        mean = math.fsum(n)/len(n)
        std = math.sqrt(math.fsum((v-mean)**2 for v in n)/len(n))
        threshold = mean+config.sigma*std if config.metric_rule == 'sigma' else quantile(n)
        assert math.isclose(threshold, row['threshold'], rel_tol=2e-14, abs_tol=0.0) or threshold == row['threshold']
        max_diff = max(max_diff, abs(threshold-row['threshold']))
        count = sum(v > threshold for v in a)
        vote = count if config.metric_aggregation == 'events' else int(count > 0)
        assert (count, vote) == (row['count'], row['vote']), (key, count, row)
        totals[inputs['metric_services'][key]]['metric'] += vote
    for service, row in result['traces'].items():
        n = [float(x) for x in inputs['normal_traces'].get(service, []) if math.isfinite(float(x))]
        a = [float(x) for x in inputs['incident_traces'].get(service, []) if math.isfinite(float(x))]
        vote = int(quantile(a) > 3*quantile(n)) if n and a else 0
        assert vote == row['vote']
        totals[service]['trace'] = vote
    for service, row in result['logs'].items():
        logs = inputs['incident_logs']
        if logs is None:
            assert row['status'] == 'unavailable'
            continue
        count = sum(any(word in message.upper() for word in ('ERROR', 'FAIL', 'EXCEPTION'))
                    for message in logs.get(service, []))
        assert count == row['count']
        vote = int(count > 0)
        assert vote == row['vote']
        totals[service]['log'] = vote
    for value in totals.values():
        value['score'] = value['metric']+value['trace']+value['log']
    assert totals == result['scores']
    ordered = sorted(totals, key=lambda s: (-totals[s]['score'], s))
    assert ordered == result['ranks']
    expected_groups = []
    for service in ordered:
        score = totals[service]['score']
        if not expected_groups or expected_groups[-1]['score'] != score:
            expected_groups.append(dict(score=score, services=[]))
        expected_groups[-1]['services'].append(service)
    assert expected_groups == result['tie_groups']
    assert result['status'] == ('abstain' if max(x['score'] for x in totals.values()) == 0 else 'heuristic_alerts')
    return dict(pass_all=True, metric_channels=len(result['metrics']),
                threshold_max_abs_roundoff=max_diff, exact_counts_votes_scores_groups=True)


def metric_time(value):
    wall, rest = value.split('.', 1)
    frac = rest.split(' ', 1)[0]
    sec = int(datetime.strptime(wall, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc).timestamp())
    return sec*10**9+int(frac.ljust(9, '0'))


def window_audit(selection, payload, mapping):
    """Second streaming scan: timestamp predicate before numeric/message fields.

    No full-day CSV is returned or printed. Only equality results/counts/hashes
    are serialized. Every opened path belongs to the validated dev selection.
    """
    t = selection['t_ns']; low = t-300*10**9; high = t+300*10**9
    metrics = {}; expected_spans = []; expected_logs = []; sources = {}
    for rel, meta in sorted(selection['files'].items()):
        kind = Path(rel).parent.name
        kept = []
        with Path(meta['absolute_path']).open(encoding='utf-8-sig', newline='') as stream:
            for row in csv.DictReader(stream):
                if kind == 'metric':
                    ts = metric_time(row['Time'])
                    if not low <= ts < high:
                        continue
                    kept.append((ts, row))
                elif kind == 'trace':
                    start, end = int(row['StartTimeUnixNano']), int(row['EndTimeUnixNano'])
                    if start < low or end >= high:
                        continue
                    duration = int(row['Duration'])
                    assert 0 <= end-start-duration*1000 < 1000
                    assert (end < t) == (start//1000+duration < t//1000)
                    service = mapping['pod_aliases'][row['PodName']]
                    expected_spans.append((row['TraceID'], row['SpanID'], row['ParentID'], service,
                                           row['OperationName'], row['OperationName'], start//1000,
                                           duration, start, end))
                    kept.append((start, end))
                elif kind == 'log':
                    ts = int(row['TimeUnixNano'])
                    if not low <= ts < high:
                        continue
                    expected_logs.append((ts, mapping['pod_aliases'][row['PodName']], row['Log'], ts))
                    kept.append(ts)
        if kind == 'metric':
            kept.sort(key=lambda x: x[0])
            assert len(kept) == 10 and sum(ts < t for ts, _ in kept) == 5
            front = Path(rel).name == 'front_service.csv'
            aliases = mapping['service_aliases'] if front else mapping['pod_aliases']
            ident = 'ServiceName' if front else 'PodName'
            channels = mapping['front_channels'] if front else mapping['resource_channels']
            for original, suffix in channels.items():
                service = aliases[kept[0][1][ident]]
                key = service+'_'+suffix
                assert key not in metrics
                data = [float(row[original]) if row[original].strip() else float('nan') for _, row in kept]
                native = payload['metric_arrays'][key]
                for expected, actual in zip([data[:5], data[5:]], [native['normal'], native['anomalous']]):
                    assert len(expected) == len(actual)
                    assert all(x == y or (math.isnan(x) and math.isnan(y)) for x, y in zip(expected, actual))
                metrics[key] = len(data)
            sources[rel] = dict(kind=kind, N=5, A=5)
        elif kind == 'trace':
            sources[rel] = dict(kind=kind, N_start=sum(s < t for s, e in kept),
                                A_start=sum(s >= t for s, e in kept),
                                N_end=sum(e < t for s, e in kept), A_end=sum(e >= t for s, e in kept))
        else:
            sources[rel] = dict(kind=kind, N=sum(x < t for x in kept), A=sum(x >= t for x in kept))
    actual_spans = list(payload['spans'].itertuples(index=False, name=None))
    actual_logs = list(payload['logs'].itertuples(index=False, name=None))
    assert actual_spans == expected_spans
    assert actual_logs == expected_logs
    assert set(metrics) == set(payload['metric_arrays']) and len(metrics) == 165
    def digest(rows):
        h = hashlib.sha256()
        for row in rows:
            h.update(json.dumps(row, ensure_ascii=True).encode())
            h.update(b'\n')
        return h.hexdigest()
    return dict(pass_all=True, sources=sources, metric_columns=len(metrics),
                trace_rows=len(expected_spans), log_rows=len(expected_logs),
                span_membership_order_mapping_units_equal=True, log_membership_content_equal=True,
                span_membership_digest=digest(expected_spans), log_membership_digest=digest(expected_logs),
                raw_payload_saved=False)


def rank_metrics(result, root):
    ranks = []
    offset = 0
    if result['status'] != 'abstain':
        for group in result['tie_groups']:
            if root in group['services']:
                ranks = list(range(offset+1, offset+len(group['services'])+1)); break
            offset += len(group['services'])
    out = dict(rank_min=min(ranks) if ranks else None, rank_max=max(ranks) if ranks else None)
    for k in (1, 3, 5):
        out['hit@'+str(k)] = sum(r <= k for r in ranks)/len(ranks) if ranks else 0.0
    out['mrr'] = math.fsum(1/r for r in ranks)/len(ranks) if ranks else 0.0
    out['ndcg@5'] = math.fsum(1/math.log2(r+1) for r in ranks if r <= 5)/len(ranks) if ranks else 0.0
    out['native_top1'] = int(bool(ranks) and result['ranks'][0] == root)
    out['optimistic_top1'] = int(bool(ranks) and min(ranks) <= 1)
    out['pessimistic_top1'] = int(bool(ranks) and max(ranks) <= 1)
    return out


def evaluate():
    """Join dev labels only after checking a complete serialized diagnosis list."""
    from doi_chieu import ROOT, OUT, read, sha, write
    import sys
    import random
    from p3 import danh_gia as dg
    folder = OUT/'runs/evaluate-001'
    folder.mkdir(exist_ok=False)
    manifest = read(OUT/'runs/full-001/diagnosis-list.json')
    assert manifest['completed'] and manifest['labels_read'] is False
    records = manifest['records']
    ids = set(read(OUT/'ke-hoach-chay.json')['dev_ids'])
    assert {(x['opaque_id'],x['branch']) for x in records} == {(i,b) for i in ids for b in ('S0','S1','S2','S3')}
    assert len(records)==88
    cache={}
    for row in records:
        assert sha(ROOT/row['path'])==row['sha256']
        d=read(ROOT/row['path']);assert d['labels_read'] is False
        cache[(row['opaque_id'],row['branch'])]=d['diagnosis']
    write(folder/'pre-label-freeze.json',dict(records=records,verified=88,labels_read=False,
                                            diagnosis_list_sha256=sha(OUT/'runs/full-001/diagnosis-list.json')))
    # First label value read by this evaluation process occurs here.
    label_path=ROOT/'results/T-026/nhan-dev.json'
    expected=read(ROOT/'results/T-026/ban-ghi-dua-vao-cham.json')['source_hashes']['results/T-026/nhan-dev.json']
    assert sha(label_path)==expected
    labels={x['opaque_id']:x for x in read(label_path)['cases']}
    assert set(labels)==ids
    metrics={};p3_checks=0
    for (oid,branch),result in cache.items():
        independent=rank_metrics(result,labels[oid]['root'])
        entity_rows=[]
        for i,group in enumerate(result['tie_groups']):
            entity_rows += [dict(entity=s,key=[group['score']],tie_group=i) for s in group['services']]
        record=dict(status='NO_EVIDENCE' if result['status']=='abstain' else 'OK',entity_ranking=entity_rows,blocks=None)
        canonical=dg.cham_ca(record,labels[oid]['root'])
        for key in ['hit@1','hit@3','hit@5','ndcg@5','rank_min','rank_max']:
            assert canonical[key]==independent[key] or (isinstance(canonical[key],float) and math.isclose(canonical[key],independent[key],rel_tol=1e-14,abs_tol=1e-14))
        assert math.isclose(canonical['rr'],independent['mrr'],rel_tol=1e-14,abs_tol=1e-14)
        independent.update(status=record['status'],candidate_count=len(result['ranks']),
                           tie_groups=len(result['tie_groups']),largest_tie=max(len(x['services']) for x in result['tie_groups']))
        metrics[(oid,branch)]=independent;p3_checks+=1
    metric_keys=['hit@1','hit@3','hit@5','mrr','ndcg@5']
    def aggregate(selected,branch):
        rows=[metrics[(i,branch)] for i in selected]
        return dict(n=len(rows),status=dict(Counter(x['status'] for x in rows)),
                    **{k:math.fsum(x[k] for x in rows)/len(rows) for k in metric_keys},
                    native_top1=sum(x['native_top1'] for x in rows),
                    optimistic_top1=sum(x['optimistic_top1'] for x in rows),
                    pessimistic_top1=sum(x['pessimistic_top1'] for x in rows),
                    candidate_sizes=sorted(set(x['candidate_count'] for x in rows)),
                    cases_with_ties=sum(x['largest_tie']>1 for x in rows))
    cells=defaultdict(list);faults=defaultdict(list)
    for oid in sorted(ids):
        cells[labels[oid]['cell']].append(oid);faults[labels[oid]['fault']].append(oid)
    summary={b:aggregate(sorted(ids),b) for b in ('S0','S1','S2','S3')}
    per_case=[]
    for oid in sorted(ids):
        label=labels[oid]
        views={b:metrics[(oid,b)] for b in summary}
        root=label['root']
        root_parts={b:cache[(oid,b)]['scores'].get(root) for b in summary}
        effects={}
        for b in ('S1','S2','S3'):
            before,after=views['S0'],views[b]
            # Mean possible rank is descriptive; tie-aware metrics remain primary.
            r0=(before['rank_min']+before['rank_max'])/2 if before['rank_min'] else math.inf
            r1=(after['rank_min']+after['rank_max'])/2 if after['rank_min'] else math.inf
            effects[b]=dict(rank='improve' if r1<r0 else 'worsen' if r1>r0 else 'same',
                            delta_hit1=after['hit@1']-before['hit@1'],delta_mrr=after['mrr']-before['mrr'])
        pair_evidence={}
        for b in summary:
            result=cache[(oid,b)];rs=result['scores'][root]['score']
            pair_evidence[b]=[dict(service=s,parts=result['scores'][s]) for s in result['ranks'] if result['scores'][s]['score']>rs]
        per_case.append(dict(opaque_id=oid,root=root,fault=label['fault'],cell=label['cell'],
                             views=views,root_parts=root_parts,effects_vs_S0=effects,above_root=pair_evidence))
    contrasts={}
    for a,b in [('S0','S1'),('S0','S2'),('S2','S3'),('S1','S3'),('S0','S3')]:
        key=b+'-'+a
        contrasts[key]=dict(delta={k:summary[b][k]-summary[a][k] for k in metric_keys},
                            improves=sum(metrics[(i,b)]['mrr']>metrics[(i,a)]['mrr'] for i in ids),
                            same=sum(metrics[(i,b)]['mrr']==metrics[(i,a)]['mrr'] for i in ids),
                            worsens=sum(metrics[(i,b)]['mrr']<metrics[(i,a)]['mrr'] for i in ids),
                            loses_certain_top1=[i for i in sorted(ids) if metrics[(i,a)]['hit@1']==1 and metrics[(i,b)]['hit@1']<1],
                            gains_certain_top1=[i for i in sorted(ids) if metrics[(i,a)]['hit@1']<1 and metrics[(i,b)]['hit@1']==1])
    interaction={k:summary['S3'][k]-summary['S2'][k]-summary['S1'][k]+summary['S0'][k] for k in metric_keys}
    # Paired cell bootstrap, all cases of each sampled cell travel together.
    rng=random.Random(20261005);cell_names=sorted(cells);B=10000
    boot={key:[] for key in contrasts}
    for _ in range(B):
        selected=[i for c in rng.choices(cell_names,k=len(cell_names)) for i in cells[c]]
        for key in boot:
            b,a=key.split('-')
            boot[key].append(math.fsum(metrics[(i,b)]['mrr']-metrics[(i,a)]['mrr'] for i in selected)/len(selected))
    def percentile(values,p):
        a=sorted(values);x=(len(a)-1)*p;lo=int(x);hi=math.ceil(x)
        return a[lo]+(a[hi]-a[lo])*(x-lo)
    intervals={k:[percentile(v,.025),percentile(v,.975)] for k,v in boot.items()}
    # Validate the saved historical S1 root ranges, not just its aggregate.
    historical=read(ROOT/'results/T-032/runs/simplerca-s1-001/summary.json')
    old_s1={x['opaque_id']:x for x in historical['cases'] if x['dataset']=='Nezha-OB'}
    assert set(old_s1)==ids
    for oid in ids:
        for b,name in [('S0','native'),('S1','changed')]:
            old=old_s1[oid][name];new=metrics[(oid,b)]
            assert (old['root_rank_min'],old['root_rank_max'])==(new['rank_min'],new['rank_max'])
    result=dict(schema='T042-evaluation-v1',summary=summary,
                by_cell={c:{b:aggregate(v,b) for b in summary} for c,v in cells.items()},
                by_fault={c:{b:aggregate(v,b) for b in summary} for c,v in faults.items()},
                per_case=per_case,contrasts=contrasts,interaction=interaction,
                paired_cell_bootstrap=dict(B=B,seed=20261005,n_cells=len(cells),mrr_difference_percentile95=intervals),
                checks=dict(p3_independent_per_case=p3_checks,historical_S0_S1_root_ranges=44,
                            labels_after_complete_freeze=True),
                conditional_cohort_bound=dict(assumptions=['same full56','dev22 is subset','same Top@1'],
                                              dev_expected_correct=summary['S0']['hit@1']*22,
                                              upper=(summary['S0']['hit@1']*22+34)/56,
                                              paper_top1=.91,test_cases_read=0),
                label_sha256=expected)
    write(folder/'summary.json',result)
    print(json.dumps(dict(summary=summary,checks=result['checks'],cells=len(cells)),ensure_ascii=True))


if __name__=='__main__':
    import sys
    root=Path(__file__).resolve().parents[3]
    sys.path.insert(0,str(root/'src'))
    evaluate()
