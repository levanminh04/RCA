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
