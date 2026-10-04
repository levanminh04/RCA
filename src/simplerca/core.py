"""SimpleRCA M4. No case IDs, filesystem paths, labels, or graphs in diagnosis.

Underspecified choices are documented in T-017 SPEC and draft WHY. This is a
heuristic candidate ranking, not a calibrated incident/causal significance test.
"""
from dataclasses import asdict, dataclass
import math
import re
import numpy as np


@dataclass(frozen=True)
class Config:
    metric_rule: str = 'sigma'
    sigma: float = 3.0
    metric_quantile: float = 0.95
    trace_quantile: float = 0.95
    trace_factor: float = 3.0
    log_threshold: int = 0
    metric_aggregation: str = 'events'
    min_normal_metric: int = 2
    keywords: tuple = ('ERROR', 'FAIL', 'EXCEPTION')

    def __post_init__(self):
        if self.metric_rule not in ('sigma', 'p95'):
            raise ValueError('unknown metric_rule')
        if self.metric_aggregation not in ('events', 'channels'):
            raise ValueError('unknown aggregation')
        if not 0 < self.metric_quantile < 1 or not 0 < self.trace_quantile < 1:
            raise ValueError('invalid quantile')
        if not math.isfinite(self.sigma) or self.sigma < 0:
            raise ValueError('invalid sigma')
        if not math.isfinite(self.trace_factor) or self.trace_factor <= 0:
            raise ValueError('invalid trace factor')
        if self.log_threshold < 0 or self.min_normal_metric < 2:
            raise ValueError('invalid count threshold')


def _finite(values):
    a = np.asarray(values, dtype=float)
    return a[np.isfinite(a)], int((~np.isfinite(a)).sum())


def diagnose(normal_metrics, incident_metrics, metric_services,
             normal_traces=None, incident_traces=None, incident_logs=None,
             observed_services=(), config=Config()):
    """Mappings of measurement arrays only. Traces grouped by service; logs
    grouped by service. None means unavailable, empty mapping means observed
    but empty. All candidate services are observed in either supplied window.
    """
    if set(normal_metrics) != set(incident_metrics) or set(metric_services) != set(normal_metrics):
        raise ValueError('metric schemas must match explicitly')
    normal_traces = {} if normal_traces is None else normal_traces
    incident_traces = {} if incident_traces is None else incident_traces
    services = set(observed_services) | set(metric_services.values())
    services |= set(normal_traces) | set(incident_traces) | set(incident_logs or {})
    if not services or any(not isinstance(s, str) or not s for s in services):
        raise ValueError('no valid observed service')
    totals = {s: {'metric': 0, 'trace': 0, 'log': 0, 'score': 0} for s in sorted(services)}
    metrics, traces, logs = {}, {}, {}
    usable = 0
    for key in sorted(normal_metrics):
        n, mn = _finite(normal_metrics[key]); a, ma = _finite(incident_metrics[key])
        row = {'service': metric_services[key], 'n_normal':len(n), 'n_incident':len(a),
               'missing_normal':mn, 'missing_incident':ma, 'status':'unavailable', 'count':0, 'vote':0}
        if len(n) >= config.min_normal_metric and len(a):
            mean, std = float(n.mean()), float(n.std(ddof=0))
            threshold = mean + config.sigma * std if config.metric_rule == 'sigma' else float(np.quantile(n, config.metric_quantile, method='linear'))
            count = int(np.sum(a > threshold))
            vote = count if config.metric_aggregation == 'events' else int(count > 0)
            row.update(mean=mean,std=std,threshold=threshold,count=count,vote=vote,max_incident=float(a.max()),status='ok')
            totals[row['service']]['metric'] += vote
            usable += 1
        metrics[key] = row
    for service in sorted(set(normal_traces) | set(incident_traces)):
        n, mn = _finite(normal_traces.get(service, [])); a, ma = _finite(incident_traces.get(service, []))
        if np.any(n < 0) or np.any(a < 0):
            raise ValueError('negative duration')
        row = {'n_normal':len(n),'n_incident':len(a),'missing_normal':mn,'missing_incident':ma,'status':'unavailable','vote':0}
        if len(n) and len(a):
            qn=float(np.quantile(n,config.trace_quantile,method='linear'))
            qa=float(np.quantile(a,config.trace_quantile,method='linear'))
            threshold=config.trace_factor*qn
            row.update(p95_normal=qn,p95_incident=qa,threshold=threshold,vote=int(qa>threshold),status='ok')
            totals[service]['trace'] += row['vote']; usable += 1
        traces[service] = row
    keyword = re.compile('|'.join(re.escape(x) for x in config.keywords), re.IGNORECASE)
    for service in sorted(services):
        if incident_logs is None:
            logs[service] = {'status':'unavailable','count':None,'vote':0}
        else:
            entries=incident_logs.get(service, [])
            if any(not isinstance(x,str) for x in entries):
                raise ValueError('log message must be string')
            count=sum(bool(keyword.search(x)) for x in entries)
            vote=int(count>config.log_threshold)
            logs[service]={'status':'ok','count':count,'threshold':config.log_threshold,'vote':vote}
            totals[service]['log'] += vote
            usable += 1
        totals[service]['score']=sum(totals[service][x] for x in ('metric','trace','log'))
    if usable == 0:
        raise ValueError('no channel has sufficient observations')
    ranks=sorted(totals,key=lambda s:(-totals[s]['score'],s))
    groups=[]
    for s in ranks:
        if not groups or groups[-1]['score']!=totals[s]['score']:
            groups.append({'score':totals[s]['score'],'services':[]})
        groups[-1]['services'].append(s)
    status='abstain' if groups[0]['score']==0 else 'heuristic_alerts'
    return {'config':asdict(config),'status':status,'ranks':ranks,'tie_groups':groups,
            'scores':totals,'metrics':metrics,'traces':traces,'logs':logs,
            'fallback':False,'interpretation':'candidate ranking; scores do not establish a causal root'}


def score_root(result, root, k=1):
    """Evaluation only. Diagnosis must already be serialized before root read.
    Fractional Hit under a uniformly random ordering inside each exact tie.
    """
    if result['status']=='abstain' or root not in result['scores']:
        return {'hit_fractional':0.0,'hit_pessimistic':0.0,'hit_optimistic':0.0,'rank_min':None,'rank_max':None,'mrr_fractional':0.0}
    offset=0
    for group in result['tie_groups']:
        size=len(group['services'])
        if root in group['services']:
            lo,hi=offset+1,offset+size
            return {'hit_fractional':max(0,min(size,k-offset))/size,
                    'hit_pessimistic':float(hi<=k),'hit_optimistic':float(lo<=k),
                    'rank_min':lo,'rank_max':hi,
                    'mrr_fractional':sum(1/r for r in range(lo,hi+1))/size}
        offset += size
    raise AssertionError('root disappeared')
