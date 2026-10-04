"""Independent input-stage calculation for the predetermined TT auth dev case.

No method module or author function is imported. Statistics use Python fsum;
graph relations use a scoped dataframe parent join and grouped sets. Intended
for the pinned EC2 environment, after the primary MicroRank worker exits.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time
import pandas as pd

sys.dont_write_bytecode=True
CASE="re2tt_ts-auth-service_cpu_1"
COLS=["traceID","spanID","parentSpanID","serviceName","methodName",
      "operationName","startTime","duration"]


def digest(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1048576),b""):h.update(b)
    return h.hexdigest()


def write(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,allow_nan=False,indent=2)+"\n",encoding="utf-8")


def graph_from_join(frame):
    """Build topology from a parent join, separate from incidence grouping."""
    d=frame[["traceID","spanID","parentSpanID","operation"]].copy()
    for col in ["traceID","spanID","operation"]:d[col]=d[col].astype(str)
    d["parentSpanID"]=d.parentSpanID.map(lambda x:None if x is None else str(x))
    assert not d.duplicated(["traceID","spanID"]).any(),"duplicate scoped span key"
    # A left join cannot resolve a same-ID span in another trace.
    parent=d[["traceID","spanID","operation"]].rename(columns={"spanID":"parentSpanID","operation":"parent_operation"})
    joined=d.merge(parent,on=["traceID","parentSpanID"],how="left",validate="many_to_one")
    roots=joined.parentSpanID.isin([None,"","0","0000000000000000","nan","None","<NA>"])
    resolved=joined.parent_operation.notna()
    missing=int((~resolved&~roots).sum())
    root_count=int((~resolved&roots).sum())
    edge_pairs=set(zip(joined.loc[resolved,"parent_operation"],joined.loc[resolved,"operation"]))
    operations=sorted(set(d.operation))
    adjacency={op:sorted(y for x,y in edge_pairs if x==op) for op in operations}
    incidence=d.groupby("traceID",sort=True).operation.agg(lambda values:sorted(set(values))).to_dict()
    reverse={op:sorted(set(d.loc[d.operation==op,"traceID"])) for op in operations}
    # The adapter defines repeated-operation order by lexical scoped spanID.
    repeated=d.sort_values(["traceID","spanID"]).groupby("traceID",sort=True).operation.agg(list).to_dict()
    endpoints={op for pair in edge_pairs for op in pair}
    graph={"operation_operation":adjacency,"operation_trace":incidence,
           "trace_operation":reverse,"pr_trace":repeated}
    audit={"missing_parent_spans":missing,"explicit_root_spans":root_count,
           "isolated_operations":sorted(set(operations)-endpoints),
           "operation_edges":len(edge_pairs),"traces":len(incidence),"operations":len(operations)}
    return graph,audit


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input-parquet",required=True,type=Path)
    ap.add_argument("--inject-file",required=True,type=Path)
    ap.add_argument("--snapshot",required=True,type=Path)
    ap.add_argument("--out",required=True,type=Path)
    ap.add_argument("--half-seconds",type=int,default=600,choices=[300,600])
    a=ap.parse_args()
    assert a.input_parquet.parent.name==CASE and a.input_parquet.name=="traces.parquet","only fixed dev auth input"
    assert a.inject_file.parent.resolve()==a.input_parquet.parent.resolve(),"marker/source mismatch"
    assert not a.out.exists(),"retain prior audit: choose a fresh output directory"
    a.out.mkdir(parents=True)
    t0=time.monotonic()
    def progress(phase,**extra):
        rec={"utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"phase":phase,
             "elapsed_observed_seconds":round(time.monotonic()-t0,3),**extra}
        with open(a.out/"progress.jsonl","a",encoding="utf-8") as f:f.write(json.dumps(rec)+"\n")
        print(json.dumps(rec),flush=True)
    progress("start",input=str(a.input_parquet),half_seconds=a.half_seconds,
             python=sys.version,pandas=pd.__version__,hash_seed=os.environ.get("PYTHONHASHSEED"))
    try:
        tau=int(a.inject_file.read_text().strip())*1000000
        raw=pd.read_parquet(a.input_parquet,columns=COLS)
        mask=(raw.startTime>=tau-a.half_seconds*1000000)&(raw.startTime<tau+a.half_seconds*1000000)
        d=raw.loc[mask].copy();raw_count=len(raw);del raw
        d["methodName"]=d.methodName.where(d.methodName.notna(),d.operationName)
        assert d[["serviceName","methodName","traceID","spanID","startTime","duration"]].notna().all().all()
        assert math.isfinite(tau),"nonfinite incident boundary"
        assert all(math.isfinite(float(v)) for col in ['startTime','duration'] for v in d[col]),"nonfinite span time"
        assert (d.duration>=0).all()
        d["operation"]=d.serviceName+"_"+d.methodName
        pairs=d[["operation","serviceName","methodName"]].drop_duplicates()
        assert not pairs.operation.duplicated().any(),"ambiguous service_method key"
        end=d.startTime+d.duration
        before=d.loc[end<tau].copy();after=d.loc[end>=tau].copy()
        progress("window",raw_spans=raw_count,window_spans=len(d),before_spans=len(before),after_spans=len(after))
        stats={}
        for op,part in before.groupby("operation",sort=True):
            values=[float(v) for v in part.duration]
            n=len(values);assert n>=2,"undefined sample std: "+op
            mean=math.fsum(values)/n
            sd=math.sqrt(math.fsum((v-mean)**2 for v in values)/(n-1))
            stats[op]={"mean":round(mean/1000,2),"std":round(sd/1000,2),"count":n}
        assert set(after.operation)<=set(stats),"operation missing reference"
        # Explicit arithmetic, with no pandas mean/std or method function.
        flags=[float(duration)/1000>=stats[op]["mean"]+3*stats[op]["std"]
               for op,duration in zip(after.operation,after.duration)]
        after["independent_flag"]=flags
        anomal={str(t) for t in after.loc[after.independent_flag,"traceID"]}
        all_traces={str(t) for t in after.traceID}
        normal=all_traces-anomal
        raw_normal={str(t) for t in after.loc[~after.independent_flag,"traceID"]}
        counts={"normal":len(normal),"anomaly":len(anomal),"all":len(all_traces),"overlap":0,
                "spans_before":len(before),"spans_after":len(after),"abnormal_spans":sum(flags)}
        reference={"normal_count":len(raw_normal),"anomaly_count":len(anomal),"overlap":len(raw_normal&anomal),
                   "before_graph_trace_count":int(before.traceID.nunique()),"after_graph_trace_count":len(all_traces)}
        progress("statistics_partition",counts=counts,rcaeval_reference=reference)
        groups={}
        for name,ids in [("normal",normal),("anomaly",anomal)]:
            part=after.loc[after.traceID.astype(str).isin(ids)]
            graph,audit=graph_from_join(part)
            groups[name]={"graph":graph,"audit":audit,"trace_count":len(ids)}
            progress("independent_graph",group=name,audit=audit)
        independent={"case_id":CASE,"counts":counts,"baseline_slo_ms":stats,"groups":groups,
                     "rcaeval_partition_reference":reference,
                     "operation_services":dict(zip(pairs.operation,pairs.serviceName)),
                     "source_sha256":digest(a.input_parquet),"snapshot_sha256":digest(a.snapshot),
                     "script_sha256":digest(Path(__file__)),"incident_time_us":tau,
                     "half_seconds":a.half_seconds,"no_author_function":True,"timing_is_official":False}
        write(a.out/"input-calculation.json",independent)
        saved=json.loads(a.snapshot.read_text(encoding="utf-8"))
        assert saved.get("case_id",CASE)==CASE,"wrong snapshot case"
        checks={"counts":saved["counts"]==counts,
                "operation_services":saved["operation_services"]==independent["operation_services"],
                "baseline_operation_set":set(saved["baseline_slo_ms"])==set(stats)}
        errors=[]
        for op,cell in stats.items():
            actual=saved["baseline_slo_ms"][op]
            if cell!=actual:errors.append({"operation":op,"independent":cell,"snapshot":actual})
        checks["baseline_every_cell"]=not errors
        if "rcaeval_partition_reference" in saved:
            checks["rcaeval_partition_reference"]=all(saved["rcaeval_partition_reference"][k]==v for k,v in reference.items())
        for name,group in groups.items():
            actual=saved["groups"][name]
            checks[name+"_trace_count"]=actual["trace_count"]==group["trace_count"]
            checks[name+"_audit"]=actual["audit"]==group["audit"]
            for relation,mapping in group["graph"].items():checks[name+"_"+relation]=mapping==actual["graph"][relation]
            expected_num={op:len(traces) for op,traces in group["graph"]["trace_operation"].items()}
            checks[name+"_spectrum_trace_counts"]=expected_num==actual["official"]["tracecounts"]
        summary={"checks":checks,"all_passed":all(checks.values()),"baseline_mismatches":errors,
                 "counts":counts,"independent_graphs_saved":"input-calculation.json",
                 "timing_is_official":False,"elapsed_observed_seconds":round(time.monotonic()-t0,3)}
        write(a.out/"comparison.json",summary)
        progress("complete",all_passed=summary["all_passed"],checks=len(checks))
        assert summary["all_passed"],summary
    except Exception as exc:
        write(a.out/"failed.json",{"exception":repr(exc),"elapsed_observed_seconds":time.monotonic()-t0})
        progress("failed",exception=repr(exc))
        raise


if __name__=="__main__":main()
