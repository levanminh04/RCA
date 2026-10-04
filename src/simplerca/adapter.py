"""RCAEval dev adapter: labels/path stay outside core diagnosis.

Only the split boundary is supplied in known-incident mode. Parent span IDs,
fault categories, and root labels are deliberately not part of the input schema.
"""
import numpy as np
import pandas as pd
from typing import NamedTuple


class PreparedInputs(NamedTuple):
    normal_metrics: pd.DataFrame
    incident_metrics: pd.DataFrame
    normal_traces: pd.DataFrame
    incident_traces: pd.DataFrame
    incident_logs: object
    metric_services: dict
    observed_services: tuple


def canonical_service(name, aliases=None):
    if not isinstance(name,str) or not name:
        raise ValueError('invalid service identifier')
    # Only aliases declared from schema/architecture, never guessed by spelling.
    target=(aliases or {}).get(name,name)
    if not isinstance(target,str) or not target: raise ValueError('invalid alias')
    return target


def prepare(metrics, traces, logs, boundary, half=300, aliases=None):
    if not np.isfinite(boundary) or half <= 0 or 'time' not in metrics:
        raise ValueError('invalid window/time schema')
    mt=pd.to_numeric(metrics['time'],errors='raise').to_numpy()
    if not 1e9 < float(np.median(mt)) < 3e9:
        raise ValueError('metric epoch must be seconds')
    keys=[c for c in metrics if c not in ('time','time.1')]
    if not metrics.columns.is_unique:
        raise ValueError('duplicate metric columns')
    aliases = aliases or {}
    for source,target in aliases.items():
        canonical_service(source,aliases)
        if target in aliases and aliases[target] != target:
            raise ValueError('alias chains/cycles must be resolved explicitly')
    mappings={}
    for c in keys:
        if '_' not in c:
            raise ValueError('metric column must be service_metric')
        s,metric=c.rsplit('_',1)
        if not s or not metric:
            raise ValueError('empty metric/service')
        mappings[c]=canonical_service(s,aliases)
    raw_services={c.rsplit('_',1)[0] for c in keys}
    if len({canonical_service(s,aliases) for s in raw_services}) != len(raw_services):
        raise ValueError('alias collision between metric services')
    nm=metrics.loc[(mt>=boundary-half)&(mt<boundary),keys].copy()
    am=metrics.loc[(mt>=boundary)&(mt<boundary+half),keys].copy()
    nm.insert(0,'time',mt[(mt>=boundary-half)&(mt<boundary)])
    am.insert(0,'time',mt[(mt>=boundary)&(mt<boundary+half)])
    nt,at=pd.DataFrame(columns=['service','duration']),pd.DataFrame(columns=['service','duration'])
    if traces is not None:
        for c in ('serviceName','startTime','duration'):
            if c not in traces: raise ValueError(f'trace missing {c}')
        tt=pd.to_numeric(traces['startTime'],errors='raise').to_numpy()/1e6
        if len(tt) and not 1e9<float(np.median(tt))<3e9:
            raise ValueError('trace startTime must be microsecond epoch')
        t=traces[['serviceName','duration']].rename(columns={'serviceName':'service'}).copy()
        t['service']=t['service'].map(lambda s:canonical_service(s,aliases))
        nt=t.loc[(tt>=boundary-half)&(tt<boundary)].reset_index(drop=True)
        at=t.loc[(tt>=boundary)&(tt<boundary+half)].reset_index(drop=True)
    al=None
    observed=set(mappings.values()) | set(nt['service']) | set(at['service'])
    if logs is not None:
        for c in ('timestamp','container_name','message'):
            if c not in logs: raise ValueError(f'log missing {c}')
        # RE2-TT parquet timestamp is epoch seconds; do not infer from a case label.
        lt=pd.to_numeric(logs['timestamp'],errors='raise').to_numpy()
        if len(lt) and not 1e9<float(np.median(lt))<3e9:
            raise ValueError('log timestamp must be second epoch')
        # Preserve identities in either window, without passing normal messages.
        window_names=logs.loc[(lt>=boundary-half)&(lt<boundary+half),'container_name']
        observed.update(canonical_service(s,aliases) for s in window_names)
        al=logs.loc[(lt>=boundary)&(lt<boundary+half),['container_name','message']].rename(columns={'container_name':'service'}).copy()
        al['service']=al['service'].map(lambda s:canonical_service(s,aliases))
        al['message']=al['message'].fillna('').astype(str)
    return PreparedInputs(nm,am,nt,at,al,mappings,tuple(sorted(observed)))


def core_input(prepared):
    nm,am,nt,at,al,mappings,observed=prepared
    def groups(df,column):
        return {s:g[column].tolist() for s,g in df.groupby('service',sort=True)}
    return {'normal_metrics':{k:nm[k].tolist() for k in mappings},
            'incident_metrics':{k:am[k].tolist() for k in mappings},
            'metric_services':mappings,'normal_traces':groups(nt,'duration'),
            'incident_traces':groups(at,'duration'),
            'incident_logs':None if al is None else groups(al,'message'),
            'observed_services':observed}
