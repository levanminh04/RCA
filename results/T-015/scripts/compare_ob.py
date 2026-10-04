"""Compare saved T-007 RCAEval predictions with T-015 fixed-input predictions.

Never runs either baseline. Tar bodies are read only for an explicit 90-case OB
whitelist. Labels are used after predictions and mechanism counts are loaded.
No averages, benchmark score optimization, or ablation claims are produced.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import tarfile

ROOT=Path(__file__).resolve().parents[3]
SERVICES=["checkoutservice","currencyservice","emailservice","productcatalogservice","recommendationservice"]
FAULTS=["cpu","mem","disk","socket","delay","loss"]
ALLOWED={"re2ob_"+f"{s}_{f}_{i}" for s in SERVICES for f in FAULTS for i in [1,2,3]}


def digest(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1048576),b""):h.update(b)
    return h.hexdigest()


def load_baseline(tar_path):
    predictions={}
    with tarfile.open(tar_path) as t:
        for m in t.getmembers():
            if not m.isfile() or "/results/" not in m.name or not m.name.endswith(".json"):continue
            case="re2ob_"+Path(m.name).stem
            if case not in ALLOWED:continue  # Enforce scope before reading body.
            value=json.load(t.extractfile(m))
            assert list(value)==["0"],(case,"unexpected T007 prediction schema")
            ranks=value["0"]
            assert ranks and len(ranks)==len(set(ranks)),(case,"empty/duplicate predictions")
            predictions[case]={"ranks":ranks,"tar_member":m.name}
    assert set(predictions)==ALLOWED,"T007 baseline is not the exact 90 OB scope"
    return predictions


def service_ranks(operations,mapping=None):
    seen=[]
    for op in operations:
        service=mapping[op] if mapping else op.split("_",1)[0]
        service=service.removesuffix("-db")
        if service not in seen:seen.append(service)
    return seen


def rank(values,target):return values.index(target)+1 if target in values else "vắng ứng viên"


def build_ledger(runs,out):
    """Real-case executions and controls; reused predictions are not reruns."""
    tt={"re2tt_ts-auth-service_cpu_1","re2tt_ts-route-service_mem_1","re2tt_ts-route-service_socket_1"}
    allowed=ALLOWED|tt
    rows=[]
    recovered_sources=[]
    transfer_manifest_path=runs/'transfer'/'expected.json'
    transferred={item['path']:item for item in json.loads(transfer_manifest_path.read_text(encoding='utf-8'))} if transfer_manifest_path.exists() else {}
    def add(case,source,method,purpose,reason,run,status,result,seconds="chua_kiem: not timed separately"):
        assert case in allowed
        rows.append({"ca":case,"file_nguon":source,"phuong_phap":method,"muc_dich":purpose,"ly_do":reason,
                     "luot_chay":run,"trang_thai":status,"tep_ket_qua":result,
                     "thoi_gian_quan_sat_giay":seconds,"thoi_gian_chinh_thuc":False})
    # The EC2 run_cases runner emits case_end for every attempted case, including
    # a failure. No method result body outside the whitelist is read.
    for p in sorted(runs.rglob("progress.jsonl")):
        if "tracerca-audit" in p.parts:continue
        # run_cases uses one --data root for every case in a block. Failure
        # JSON predates source_file recording. Recover only with the same
        # block's valid source paths and the exact transfer manifest entry.
        block_data_roots=set()
        for candidate in p.parent.glob('re2ob_*.json'):
            if candidate.stem not in ALLOWED:continue
            record=json.loads(candidate.read_text(encoding='utf-8'))
            if record.get('source_file'):
                block_data_roots.add(str(Path(record['source_file']).parent.parent).replace('\\','/'))
        configuration={}
        for line in p.read_text(encoding="utf-8").splitlines():
            item=json.loads(line)
            if item.get("event")=="block_start":configuration=item;continue
            if item.get("event")!="case_end" or item.get("case") not in allowed:continue
            case=item["case"];result=p.parent/(case+".json")
            value=json.loads(result.read_text(encoding="utf-8")) if result.exists() else {}
            source=value.get("source_file","chua_kiem: source not recorded before failed method")
            manifest_entry=transferred.get(case+'/traces.parquet')
            if source.startswith('chua_kiem') and len(block_data_roots)==1 and manifest_entry:
                source=next(iter(block_data_roots))+'/'+case+'/traces.parquet'
                recovered_sources.append({'case':case,'failure_output':str(result),
                                          'source':source,'same_block_data_root':next(iter(block_data_roots)),
                                          'data_manifest':str(transfer_manifest_path),'manifest_entry':manifest_entry,
                                          'proof':'run_cases.py uses one --data root per block; all valid source_file parents agree; exact manifest lists this transferred case/file'})
            purpose=f"{p.parent.name}; half={configuration.get('half_seconds')}; seed={configuration.get('hash_seed')}"
            repeat=any(t in p.parent.name for t in ["repeat","rerun","seed1","lai"])
            reason='c' if p.parent.name=='ob-duplicate-rerun' else ('a' if repeat else 'b')
            add(case,source,"MicroRank-RCAEval sửa đầu vào",purpose,reason,
                str(p),item.get("status"),str(result),item.get("seconds"))
    # Fresh serial TT worker ledger, preserved by the portable runner.
    tt_execution_keys=set()
    for p in sorted(runs.rglob("run-ledger.csv")):
        with open(p,encoding="utf-8-sig",newline="") as stream:
            for item in csv.DictReader(stream):
                if item["case"] not in allowed:continue
                key=tuple(item.get(field) for field in ["case","file_source","method","purpose","reason","exit_code","elapsed_observed_seconds"])
                if key in tt_execution_keys:continue  # Same execution copied back in multiple blocks.
                tt_execution_keys.add(key)
                step=item["purpose"]
                target=p.parent/("example.json" if step=="primary" else step+".json")
                add(item["case"],item["file_source"],item["method"],step,item["reason"],str(p),
                    "ok" if item["exit_code"]=="0" else "failed",str(target),item["elapsed_observed_seconds"])
    # Auth TraceRCA is fixed by its script before input reading. Keep each
    # official permutation execution and the separate independent controls.
    for seed in ["seed0","seed1"]:
        p=runs/"tracerca-audit"/seed/"tt-summary.json"
        if not p.exists():continue
        value=json.loads(p.read_text(encoding="utf-8"));assert value["case"] in tt
        case=value["case"];source=value["source"]
        add(case,source,"TraceRCA RCAEval + kiểm độc lập",value["purpose"],value["reason"],str(p),
            value["status"],str(p),value["elapsed_observed_seconds"])
        for check in value["permutation_checks"]:
            add(case,source,"TraceRCA RCAEval + kiểm độc lập",check["permutation"],"b",str(p),"matched",str(p))
        add(case,source,"Luật span μ+3σ + TraceRCA tính độc lập","two pre-start normal windows (11 crossing spans; kept original)",
            "a" if seed=="seed1" else "b",str(p),"pre_injection_start_control",str(p.parent/"tt-two-normal-windows.json"))
    boundary=runs/"tracerca-audit/normal-boundary/strict-two-normal-windows.json"
    if boundary.exists():
        value=json.loads(boundary.read_text(encoding="utf-8"))
        add("re2tt_ts-auth-service_cpu_1",value["source"],"Luật span μ+3σ + TraceRCA tính độc lập",
            "correct control: remove all11 spans ending at/after injection; subtract saved independent counts and recompute scores",
            "c",str(boundary.parent),value["status"],str(boundary))
    # A graph/math snapshot check is a validation computation on saved output,
    # not another execution of the official method on raw telemetry.
    out.parent.mkdir(parents=True,exist_ok=True)
    assert rows,"no real-case executions found"
    with open(out,"w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
    (runs/'ledger-source-audit.json').write_text(json.dumps({'recovered_failed_sources':recovered_sources,
                                                         'data_manifest_sha256':digest(transfer_manifest_path) if transferred else None},ensure_ascii=False,indent=2),encoding='utf-8')
    return len(rows)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--baseline",type=Path,default=ROOT/"results/T-007/runs/py312-pin/microrank-L20.tar.gz")
    ap.add_argument("--fixed-dir",action="append",type=Path,default=[])
    ap.add_argument("--out",type=Path,default=ROOT/"results/T-015/so-sanh-tung-ca.csv")
    ap.add_argument("--manifest-out",type=Path,default=ROOT/"results/T-015/runs/ob-comparison-manifest.json")
    ap.add_argument("--allow-partial",action="store_true")
    ap.add_argument("--ledger-only",action="store_true")
    ap.add_argument("--runs-dir",type=Path,default=ROOT/"results/T-015/runs")
    ap.add_argument("--ledger-out",type=Path,default=ROOT/"results/T-015/ca-da-chay.csv")
    a=ap.parse_args()
    if a.ledger_only:
        print(json.dumps({"ledger_rows":build_ledger(a.runs_dir,a.ledger_out)}));return
    assert a.fixed_dir,"--fixed-dir required for comparison"
    baseline=load_baseline(a.baseline)
    fixed={}
    for directory in a.fixed_dir:
        for p in directory.glob("re2ob_*.json"):
            case=p.stem
            if case not in ALLOWED:continue
            value=json.loads(p.read_text(encoding="utf-8"))
            assert value.get("case_id")==case,"prediction filename/case mismatch"
            assert value.get("half_seconds")==600,"comparison must use same +/-600s window"
            if case in fixed:
                previous=fixed[case][0]
                if previous.get('status')=='failed' and value.get('status')=='ok':
                    fixed[case]=(value,p);continue
                if previous.get('status')=='ok' and value.get('status')=='failed':continue
                assert previous.get("scores")==value.get("scores"),"duplicate case disagrees"
                continue
            fixed[case]=(value,p)
    if not a.allow_partial:assert set(fixed)==ALLOWED,"fixed results incomplete: use --allow-partial for an explicitly incomplete comparison"
    rows=[];sources=[]
    for case in sorted(ALLOWED):
        # Read predictions first; only below parse the root for evaluation.
        raw=baseline[case]["ranks"]
        raw_services=service_ranks(raw)
        pair=fixed.get(case)
        value=pair[0] if pair else None
        root=case[len("re2ob_"):].rsplit("_",2)[0]
        row={"ca":case,"baseline_tar_member":baseline[case]["tar_member"],
             "baseline_operation_top11":json.dumps(raw,ensure_ascii=False),
             "baseline_service_top11":json.dumps(raw_services,ensure_ascii=False),
             "baseline_root_rank_service_top11":rank(raw_services,root),
             "fixed_status":value.get("status") if value else "chua_chay",
             "fixed_error":value.get("error","") if value else "chua_chay",
             "fixed_file":str(pair[1]) if pair else "chua_chay"}
        if value and value.get("status")=="failed":
            row.update(fixed_operation_top11="[]",fixed_operation_full="[]",fixed_service_top11="[]",fixed_service_full="[]",
                       fixed_root_rank_service_top11="không có ranking: failed",
                       fixed_root_rank_service_full="không có ranking: failed",
                       mechanism_interpretation="Guard duplicate (traceID,spanID) dừng dựng graph. Giữ failure và thông báo lỗi; không deduplicate dữ liệu hoặc gọi đây là no-anomaly, ranking đúng hay fallback.")
        if value and "counts" in value:
            c=value["counts"];ref=value.get("rcaeval_partition_reference",{})
            row.update(fixed_normal_traces=c["normal"],fixed_anomaly_traces=c["anomaly"],
                       fixed_all_traces=c["all"],fixed_overlap=c["overlap"],fixed_abnormal_spans=c["abnormal_spans"],
                       rcaeval_reference_normal_count=ref.get("normal_count","chua_kiem: absent snapshot metadata"),
                       rcaeval_reference_anomaly_count=ref.get("anomaly_count","chua_kiem: absent snapshot metadata"),
                       rcaeval_reference_overlap=ref.get("overlap","chua_kiem: absent snapshot metadata"),
                       rcaeval_before_graph_traces=ref.get("before_graph_trace_count","chua_kiem: absent snapshot metadata"),
                       rcaeval_after_graph_traces=ref.get("after_graph_trace_count","chua_kiem: absent snapshot metadata"))
            if value.get("status")!="ok":
                assert not value.get("ranks"),"evidence-free result must not rank"
                row.update(fixed_operation_top11="[]",fixed_operation_full="[]",fixed_service_top11="[]",fixed_service_full="[]",
                           fixed_root_rank_service_top11="không có ranking: "+value["status"],
                           fixed_root_rank_service_full="không có ranking: "+value["status"],
                           mechanism_interpretation="Giữ trạng thái thiếu bằng chứng và nhóm/counts thực; không diễn giải danh sách rỗng thành ranking hay fallback.")
        if value and value.get("status")=="ok":
            assert value["variant"]=="MicroRank-RCAEval sửa đầu vào"
            assert value["counts"]["overlap"]==0
            assert all(v>=0 for cells in value["spectrum"].values() for v in cells.values())
            mapping=value["operation_services"]
            top,full=value["ranks"],value["full_ranks"]
            top_services,full_services=service_ranks(top,mapping),service_ranks(full,mapping)
            reference=value.get("rcaeval_partition_reference",{})
            after_nums={}
            for group in value["groups"].values():
                for op,count in group["official"]["tracecounts"].items():after_nums[op]=after_nums.get(op,0)+count
            # RCAEval anomaly graph contains all post-boundary traces while its
            # anomaly length counts only traces with >=1 abnormal span. The
            # factor (anomaly_count - operation_trace_count) can be negative.
            negative={op:reference["anomaly_count"]-n for op,n in after_nums.items()
                      if "anomaly_count" in reference and n>reference["anomaly_count"]}
            row.update(fixed_operation_top11=json.dumps(top,ensure_ascii=False),
                       fixed_operation_full=json.dumps(full,ensure_ascii=False),
                       fixed_service_top11=json.dumps(top_services,ensure_ascii=False),
                       fixed_service_full=json.dumps(full_services,ensure_ascii=False),
                       fixed_root_rank_service_top11=rank(top_services,root),
                       fixed_root_rank_service_full=rank(full_services,root),
                       operation_top11_changed=raw!=top,service_top11_changed=raw_services!=top_services,
                       fixed_normal_traces=value["counts"]["normal"],fixed_anomaly_traces=value["counts"]["anomaly"],
                       fixed_all_traces=value["counts"]["all"],fixed_overlap=value["counts"]["overlap"],
                       fixed_abnormal_spans=value["counts"]["abnormal_spans"],
                       rcaeval_reference_normal_count=reference.get("normal_count","chua_kiem: absent old snapshot metadata"),
                       rcaeval_reference_anomaly_count=reference.get("anomaly_count","chua_kiem: absent old snapshot metadata"),
                       rcaeval_reference_overlap=reference.get("overlap","chua_kiem: absent old snapshot metadata"),
                       rcaeval_before_graph_traces=reference.get("before_graph_trace_count","chua_kiem: absent old snapshot metadata"),
                       rcaeval_after_graph_traces=reference.get("after_graph_trace_count","chua_kiem: absent old snapshot metadata"),
                       rcaeval_negative_nf_count_factor_operations=json.dumps(negative,sort_keys=True),
                       fixed_normal_graph_edges=value["groups"]["normal"]["audit"]["operation_edges"],
                       fixed_anomaly_graph_edges=value["groups"]["anomaly"]["audit"]["operation_edges"],
                       fixed_min_spectrum_cell=min(v for cells in value["spectrum"].values() for v in cells.values()),
                       fixed_window_boundary_traces=value.get("boundary_trace_count","chua_kiem: absent metadata"),
                       mechanism_interpretation="Cạnh tích lũy và graph/count cùng hai nhóm rời đã đổi đồng thời; không ablation riêng. nf-count-factor âm được suy từ cùng flags/counts, chưa là số nf có trọng số của lượt baseline. Cửa sổ giữ cùng600s; khác preprocessing/sorting cũng phải giữ trong diễn giải.")
            sources.append({"case":case,"path":str(pair[1]),"sha256":digest(pair[1]),"source_sha256":value.get("source_sha256")})
        rows.append(row)
    fields=list(dict.fromkeys(key for row in rows for key in row))
    for row in rows:
        for field in fields:
            if field not in row:row[field]="chua_kiem: no valid fixed output"
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with open(a.out,"w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fields);w.writeheader();w.writerows(rows)
    manifest={"baseline":str(a.baseline),"baseline_sha256":digest(a.baseline),"baseline_predictions_reused":90,
              "fixed_cases_present":len(fixed),"comparison_rows":len(rows),"complete":set(fixed)==ALLOWED,
              "no_baseline_method_rerun":True,"no_average_scores":True,"sources":sources,
              "missing_fixed_cases":sorted(ALLOWED-set(fixed)),"script_sha256":digest(Path(__file__))}
    a.manifest_out.parent.mkdir(parents=True,exist_ok=True)
    a.manifest_out.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"rows":len(rows),"fixed_present":len(fixed),"complete":manifest["complete"]}))


if __name__=="__main__":main()
