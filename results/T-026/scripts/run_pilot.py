"""T-026 bước 2: chọn pilot và chiếu chi phí không dùng nhãn.

Ca được sắp theo tuple yếu tố sau xử lý, rồi mã mờ; lấy nhỏ nhất, trung vị
dưới và lớn nhất. Chiếu tuyến tính từng đoạn theo yếu tố đầu có biến thiên;
nếu không có biến thiên, dùng trung bình ba số đo và khai giới hạn.
Không chạy toàn bộ phương pháp trên 22 ca, không gọi evaluator.
"""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/"src"))
from p3 import ban_ghi, nezha, runner
from p3.adapters import baro
from p3.adapters.nezha import VERSIONS, VARIANTS, _trace
from p3.selector import LoiRunner

OUT=ROOT/"results/T-026"
SUPPORTED=("baro","simplerca","microrank","tracerca")
WHY=["WHY-22","WHY-26","WHY-27","WHY-31","WHY-32","WHY-33","WHY-37"]
FACTOR_NAMES={"baro":["columns_intersection"],
              "simplerca":["metric_columns","selected_spans","log_rows"],
              "microrank":["selected_spans","operations"],
              "tracerca":["selected_spans","operations"]}
CONFIG="t026-ob-q85-native-v1"

def now():
    return datetime.now(timezone.utc).isoformat()

def dump(path,doc):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("x",encoding="utf-8") as f:
        json.dump(doc,f,ensure_ascii=False,indent=2,allow_nan=False)
        f.write("\n")

def progress(out,event,**extra):
    doc={"at_utc":now(),"event":event,**extra}
    with (out/"progress.jsonl").open("a",encoding="utf-8") as f:
        f.write(json.dumps(doc,ensure_ascii=True,allow_nan=False)+"\n")
    print(json.dumps(doc,ensure_ascii=True),flush=True)

def source_hash():
    h=hashlib.sha256(); files={}
    for p in sorted((ROOT/"src/p3").rglob("*.py")):
        data=p.read_bytes();h.update(data)
        files[p.relative_to(ROOT).as_posix()]=hashlib.sha256(data).hexdigest()
    return {"tong":h.hexdigest(),"tep":files}

def tuples(payload,guard):
    from RCAEval.io.time_series import preprocess
    frame=baro.chuan_bi(payload["metric"])
    t=payload["t_ns"]
    n=preprocess(data=frame[frame.time<t],dataset="re2-tt",dk_select_useful=False)
    a=preprocess(data=frame[frame.time>=t],dataset="re2-tt",dk_select_useful=False)
    cols=[c for c in n if c in a]
    sp,diag=_trace(payload,guard)
    op=sp.serviceName+"_"+sp.methodName.fillna(sp.operationName)
    original=payload["spans"]
    simple_N=original._start_ns<t
    if guard:simple_N &= original._end_ns<t-guard*10**9
    simple_keep=simple_N | (original._start_ns>=t)
    # M4 filters nonfinite values within each channel, but never changes its keys.
    usable=sum(np.isfinite(v["normal"]).sum()>=2 and np.isfinite(v["anomalous"]).sum()>=1
               for v in payload["metric_arrays"].values())
    return {"baro":[len(cols)],
            "simplerca":[int(usable),int(simple_keep.sum()),int(len(payload["logs"]))],
            "microrank":[int(len(sp)),int(op.nunique())],
            "tracerca":[int(len(sp)),int(op.nunique())]}

def factors(out):
    started=time.perf_counter()
    progress(out,"FACTORS_START",expected_dev=22)
    allow=nezha.nap_allowlist(OUT/"allowlist-dev.json")
    if len(allow)!=22:raise LoiRunner("pilot requires exactly22dev")
    table={"main":{},"trace_guard":{}}
    for i,oid in enumerate(sorted(allow),1):
        progress(out,"READ_START",opaque_id=oid,index=i)
        s=time.perf_counter()
        selection=nezha.chon_ca(allow,oid,ROOT)
        p=nezha.doc_cua_so(selection)
        table["main"][oid]=tuples(p,0)
        table["trace_guard"][oid]=tuples(p,selection["trace_guard_s"])
        progress(out,"READ_FACTORS_DONE",opaque_id=oid,index=i,
                 seconds=round(time.perf_counter()-s,3),guard_s=selection["trace_guard_s"])
        del p,selection
    chosen={}
    for view,bycase in table.items():
        chosen[view]={}
        for method in SUPPORTED:
            if view=="trace_guard" and method=="baro":continue
            ordered=sorted(bycase,key=lambda oid:(tuple(bycase[oid][method]),oid))
            chosen[view][method]=[
                {"role":role,"opaque_id":ordered[index],
                 "factor":bycase[ordered[index]][method]}
                for role,index in [("smallest",0),("lower_median",(len(ordered)-1)//2),("largest",len(ordered)-1)]]
    doc={"created_at":now(),"src_p3":source_hash(),"factor_names":FACTOR_NAMES,
         "selection_rule":"lexicographic tuple then opaque_id; positions0,10,21",
         "projection_rule":"piecewise linear first varying factor; average at duplicate x; sum22",
         "factors":table,"chosen":chosen,"elapsed_s":round(time.perf_counter()-started,3),
         "payload_files":[],"labels_read":False}
    dump(out/"factors.json",doc)
    progress(out,"FACTORS_DONE",elapsed_s=doc["elapsed_s"])
    return doc

def one(out,allow,method,oid,view,guard,hashseed=0,tag=None,allowlist_path=None):
    role=tag or "pilot"
    name=f"{method}-{view}-{oid}-h{hashseed}-{role}"
    d=out/name;d.mkdir(exist_ok=False)
    # Parent validates the opaque selector too; worker revalidates independently.
    if oid not in allow:raise LoiRunner("unknown opaque_id before worker")
    job={"allowlist_path":str(allowlist_path or OUT/"allowlist-dev.json"),"opaque_id":oid,
         "repo_root":str(ROOT),"view":"main","method":method,"trace_guard_s":guard}
    dump(d/"job.json",job)
    progress(out,"METHOD_START",method=method,view=view,opaque_id=oid,hashseed=hashseed)
    cost=runner.chay_tien_trinh("main",["-m","p3.nezha_worker",str(d/"job.json"),str(d/"ket-qua.json")],
                               3600,hashseed,d)
    dump(d/"cost.json",cost)
    if cost["timed_out"]:
        results=[{"status":"TIMEOUT","error":"timeout3600s","items":[],"variant":VARIANTS[method]}]
        output={"window":None,"provenance":{},"input_sha256":{},"buoc_s":{}}
    elif cost["exit_code"]!=0 or not (d/"ket-qua.json").exists():
        dump(d/"loi-runner.json",{"cost":cost,"runner_error":True})
        progress(out,"RUNNER_FAILED",method=method,view=view,opaque_id=oid)
        raise LoiRunner("worker failed; preserve "+str(d))
    else:
        output=json.loads((d/"ket-qua.json").read_text(encoding="utf-8"))
        results=output["ket_qua_nhieu"]
    recs=[]
    for i,kq in enumerate(results):
        unsupported=kq["status"]=="UNSUPPORTED"
        rec=ban_ghi.tao("torai" if method=="torai_B" else method,VERSIONS[method],
                       kq["variant"],"a",kq,output["window"],CONFIG,WHY,
                       seed=None,hashseed=None if unsupported else hashseed,
                       run_id=name,opaque_id=oid)
        rec["cost"]={**cost,"buoc_s":output.get("buoc_s",{})}
        rec["input_sha256"]=output.get("input_sha256",{})
        rec["extra"]["pilot_view"]=view
        rec["extra"]["pilot_only"]=True
        rec["extra"]["source_provenance_file"]="ket-qua.json"
        dump(d/f"ban-ghi-{i}.json",rec)
        recs.append(rec)
    progress(out,"METHOD_DONE",method=method,view=view,opaque_id=oid,
             status=recs[0]["status"],wall_s=cost["wall_s"],peak_rss_mb=cost["peak_rss_mb"])
    return {"method":method,"view":view,"opaque_id":oid,"role":role,"hashseed":hashseed,
            "run_dir":d.relative_to(ROOT).as_posix(),"record":recs[0],"cost":cost}

def projected(rows,table):
    out={}
    for view in ("main","trace_guard"):
        out[view]={}
        for method in SUPPORTED:
            subset=[r for r in rows if r["view"]==view and r["method"]==method and
                    r["role"] in ("smallest","lower_median","largest") and r["hashseed"]==0]
            if not subset:continue
            allfactor={oid:r[method] for oid,r in table[view].items()}
            dimension=next((i for i in range(len(FACTOR_NAMES[method]))
                            if len({v[i] for v in allfactor.values()})>1),None)
            samples=defaultdict(list)
            for r in subset:
                x=allfactor[r["opaque_id"]][dimension] if dimension is not None else 0
                samples[x].append(r["cost"]["wall_s"])
            xs=sorted(samples);ys=[float(np.mean(samples[x])) for x in xs]
            total=float(sum(np.interp(v[dimension] if dimension is not None else 0,xs,ys)
                            for v in allfactor.values()))
            valid=len(subset)==3 and all(r["record"]["status"] in ("OK","NO_EVIDENCE") for r in subset)
            out[view][method]={"unverified":True,"factor":FACTOR_NAMES[method][dimension] if dimension is not None else "all_fixed",
                 "samples":[[x,y] for x,y in zip(xs,ys)],"completed_pilot":len(subset),
                 "projected_valid":valid,"total_22_s":round(total,3) if valid else None,
                 "scenario_22_min_s":round(22*min(ys),3) if valid else None,
                 "scenario_22_max_s":round(22*max(ys),3) if valid else None,
                 "max_peak_rss_mb":max(r["cost"]["peak_rss_mb"] for r in subset),
                 "statuses":[r["record"]["status"] for r in subset],
                 "incomplete":len(subset)<3,"failed_or_censored":not valid,
                 "assumptions":"cost depends on first varying factor and startup/cache stay comparable",
                 "failure_cases":"other factors, cold IO, errors/new operations or runtime variance dominate",
                 "extrapolated_single_run_over_1h":max(ys)>3600}
    return out

def pilot(out,factor_path):
    doc=json.loads(Path(factor_path).read_text(encoding="utf-8"))
    if source_hash()["tong"]!=doc["src_p3"]["tong"]:raise LoiRunner("src_p3 changed since factors")
    allow=nezha.nap_allowlist(OUT/"allowlist-dev.json")
    progress(out,"PILOT_START",timeout_s=3600,labels_read=False)
    rows=[];stopped=set()
    for view,methods in doc["chosen"].items():
        for method,choices in methods.items():
            for c in choices:
                if method in stopped:break
                guard=allow[c["opaque_id"]]["trace_guard_s"] if view=="trace_guard" else 0
                r=one(out,allow,method,c["opaque_id"],view,guard,tag=c["role"])
                rows.append(r)
                if method=="microrank" and r["record"]["status"] in ("ERROR","TIMEOUT"):
                    stopped.add(method)
                    progress(out,"MICRORANK_BRANCH_STOP",reason="Q-77/WHY-31; report Minh")
    # Unsupported contracts are recorded for the three BARO pilot cases, no method invocation.
    for method in ("circa","torai_B"):
        for c in doc["chosen"]["main"]["baro"]:
            rows.append(one(out,allow,method,c["opaque_id"],"main",0,tag=c["role"]))
    # MicroRank pilot check hashseed1 uses the same selected case, never another case.
    if "microrank" not in stopped:
        for view in ("main","trace_guard"):
            c=doc["chosen"][view]["microrank"][1]
            guard=allow[c["opaque_id"]]["trace_guard_s"] if view=="trace_guard" else 0
            replay=one(out,allow,"microrank",c["opaque_id"],view,guard,hashseed=1,tag="hashseed_check")
            rows.append(replay)
            original=next(r for r in rows if r["method"]=="microrank" and r["view"]==view and
                          r["opaque_id"]==c["opaque_id"] and r["hashseed"]==0)
            same=original["record"]["entity_ranking"]==replay["record"]["entity_ranking"]
            dump(out/f"microrank-{view}-hashseed-check.json",{"same_entity_keys":same,"labels_read":False})
    # Đổi mã/locator manifest của một ca pilot thật, giữ nguyên mọi byte nguồn.
    # Manifest replay vẫn chỉ trỏ các nguồn dev được duyệt; không chép payload.
    c=doc["chosen"]["main"]["simplerca"][1]
    original_id=c["opaque_id"]; replacement="dev-000000abcd"
    if replacement in allow:raise LoiRunner("locator replay ID collision")
    replay_doc=json.loads((OUT/"allowlist-dev.json").read_text(encoding="utf-8"))
    for entry in replay_doc["cases"]:
        if entry["opaque_id"]==original_id:entry["opaque_id"]=replacement
    replay_path=out/"locator-replay-allowlist.json"
    dump(replay_path,replay_doc)
    replay_allow=nezha.nap_allowlist(replay_path)
    replay=one(out,replay_allow,"simplerca",replacement,"locator_check",0,
               tag="locator_check",allowlist_path=replay_path)
    rows.append(replay)
    original=next(r for r in rows if r["method"]=="simplerca" and r["view"]=="main" and
                  r["opaque_id"]==original_id)
    fields=("status","ranking_native","ranking","entity_ranking","sets","input_sha256")
    equal={k:original["record"][k]==replay["record"][k] for k in fields}
    dump(out/"locator-check.json",{"original_opaque_id":original_id,"replay_opaque_id":replacement,
         "manifest_locator_changed":True,"source_paths_and_bytes_unchanged":True,
         "equal":equal,"pass":all(equal.values()),"labels_read":False})
    if not all(equal.values()):raise LoiRunner("locator equivalence failed")
    summary={"created_at":now(),"src_p3":source_hash(),"factor_file":str(factor_path),
             "runs":[{k:v for k,v in r.items() if k!="record"} for r in rows],
             "projection":projected(rows,doc["factors"]),"stopped_branches":sorted(stopped),
             "total_measured_wall_s":round(sum(r["cost"]["wall_s"] for r in rows),3),
             "max_peak_rss_mb":max(r["cost"]["peak_rss_mb"] for r in rows),
             "payload_files":[],"labels_read":False,"evaluator_called":False}
    dump(out/"summary.json",summary)
    progress(out,"PILOT_DONE",total_wall_s=summary["total_measured_wall_s"],
             stopped_branches=summary["stopped_branches"])

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("stage",choices=("factors","pilot"))
    ap.add_argument("--run-id",required=True)
    ap.add_argument("--factors")
    args=ap.parse_args()
    if not args.run_id or "/" in args.run_id or "\\" in args.run_id or ".." in args.run_id:
        raise ValueError("invalid run-id")
    out=OUT/"runs"/args.run_id
    out.mkdir(parents=True,exist_ok=False)
    started=time.perf_counter()
    try:
        if args.stage=="factors":factors(out)
        else:
            if not args.factors:raise ValueError("pilot requires --factors")
            pilot(out,args.factors)
    except Exception as exc:
        dump(out/"failure.json",{"error":repr(exc),"elapsed_s":time.perf_counter()-started})
        progress(out,"FAILED",error=repr(exc))
        raise

if __name__=="__main__":
    main()
