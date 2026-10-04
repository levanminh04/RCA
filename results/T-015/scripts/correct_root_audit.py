"""Correct missing-parent/root audit metadata without rerunning MicroRank.

The saved points remain immutable. An independent scoped parent join rebuilds
all four input graph relations and must match the original snapshot exactly.
Only root-vs-missing classification changes for the semantic null token <NA>.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
import time
import pandas as pd
from independent_inputs import graph_from_join,digest,write

sys.dont_write_bytecode=True
ALLOWED={"re2tt_ts-auth-service_cpu_1","re2tt_ts-route-service_mem_1","re2tt_ts-route-service_socket_1"}
COLS=["traceID","spanID","parentSpanID","serviceName","methodName","operationName","startTime","duration"]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input-parquet",type=Path,required=True)
    ap.add_argument("--snapshot",type=Path,required=True)
    ap.add_argument("--out",type=Path,required=True)
    a=ap.parse_args()
    case=a.input_parquet.parent.name
    assert case in ALLOWED and a.input_parquet.name=="traces.parquet","not one of the3 predetermined dev cases"
    assert not a.out.exists(),"retain previous audit correction; choose fresh output directory"
    a.out.mkdir(parents=True)
    start=time.monotonic()
    def event(phase,**extra):
        record={"phase":phase,"case":case,"elapsed_observed_seconds":round(time.monotonic()-start,3),**extra}
        with open(a.out/"progress.jsonl","a",encoding="utf-8") as f:f.write(json.dumps(record)+"\n")
        print(json.dumps(record),flush=True)
    try:
        event("start",source=str(a.input_parquet),snapshot=str(a.snapshot))
        saved=json.loads(a.snapshot.read_text(encoding="utf-8"))
        assert saved.get("run_metadata",{}).get("case",saved.get("case_id",case))==case
        assert saved["status"]=="ok" and saved["groups"],"a graph snapshot is required"
        metadata=saved.get("io_metadata",{})
        tau=metadata.get("incident_time_us")
        boundary=metadata.get("boundary_used_us",tau)
        assert tau is not None and boundary is not None,"snapshot must record window/boundary"
        half=metadata.get("half_seconds",saved.get("half_seconds",600))
        raw=pd.read_parquet(a.input_parquet,columns=COLS)
        d=raw.loc[(raw.startTime>=tau-half*1000000)&(raw.startTime<tau+half*1000000)].copy();del raw
        d["methodName"]=d.methodName.where(d.methodName.notna(),d.operationName)
        d["operation"]=d.serviceName+"_"+d.methodName
        after=d.loc[d.startTime+d.duration>=boundary].copy()
        stats=saved["baseline_slo_ms"]
        after["flag"]=[float(duration)/1000>=stats[op]["mean"]+3*stats[op]["std"] for op,duration in zip(after.operation,after.duration)]
        anomal={str(t) for t in after.loc[after.flag,"traceID"]}
        normal={str(t) for t in after.traceID}-anomal
        assert (len(normal),len(anomal),int(after.flag.sum()))==(saved["counts"]["normal"],saved["counts"]["anomaly"],saved["counts"]["abnormal_spans"])
        event("partition_checked",normal=len(normal),anomaly=len(anomal),spans=len(after))
        checks={};groups={}
        for name,ids in [("normal",normal),("anomaly",anomal)]:
            part=after.loc[after.traceID.astype(str).isin(ids)]
            graph,corrected=graph_from_join(part)
            original=saved["groups"][name]
            for relation in ["operation_operation","operation_trace","trace_operation","pr_trace"]:
                checks[name+"_"+relation]=graph[relation]==original["graph"][relation]
            old=original["audit"]
            unknown_delta=old["missing_parent_spans"]-corrected["missing_parent_spans"]
            root_delta=corrected["explicit_root_spans"]-old["explicit_root_spans"]
            checks[name+"_classification_conservation"]=unknown_delta==root_delta
            checks[name+"_nonclassification_audit_unchanged"]=all(old[key]==corrected[key] for key in old if key not in ["missing_parent_spans","explicit_root_spans"])
            null_count=int(part.parentSpanID.isna().sum())
            scalar_types=sorted({type(v).__module__+"."+type(v).__name__ for v in part.loc[part.parentSpanID.isna(),"parentSpanID"]})
            groups[name]={"original_audit":old,"corrected_audit":corrected,
                          "null_parent_spans_by_isna":null_count,"null_scalar_types":scalar_types,
                          "missing_to_explicit_root_delta":root_delta}
            event("group_corrected",group=name,original=old,corrected=corrected)
        all_passed=all(checks.values())
        result={"case":case,"source":str(a.input_parquet),"source_sha256":digest(a.input_parquet),
                "snapshot":str(a.snapshot),"snapshot_sha256":digest(a.snapshot),
                "script_sha256":digest(Path(__file__)),"independent_graph_script_sha256":digest(Path(__file__).parent/"independent_inputs.py"),
                "groups":groups,"checks":checks,"all_passed":all_passed,
                "numeric_graph_input_unchanged":all_passed,"snapshot_points_not_changed":True,
                "interpretation":"Semantic null <NA> is an explicit root marker, never evidence of a missing parent. Four graph relations exactly match; PageRank/spectrum inputs and saved points remain unchanged.",
                "method_not_rerun":True,"timing_is_official":False,"reason":"c","elapsed_observed_seconds":round(time.monotonic()-start,3)}
        write(a.out/"audit-correction.json",result)
        event("complete",all_passed=all_passed)
        assert all_passed,result
    except Exception as exc:
        write(a.out/"failed.json",{"exception":repr(exc),"method_not_rerun":True})
        event("failed",exception=repr(exc));raise


if __name__=="__main__":main()
