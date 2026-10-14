"""T-032 bản 013 mục 3 (KT-8, nửa TraceRCA): bỏ span của thao tác không có ở đoạn nền rồi gọi adapter TraceRCA nguyên trạng. Chạy trên EC2.

Bước duy nhất bị đổi là ĐẦU VÀO: các span kết thúc từ mốc trở đi thuộc thao tác không có span nào kết thúc trước mốc bị bỏ khỏi bảng.
Sau đó gọi p3.adapters.tracerca.chay(spans, t) không sửa. Kết quả không thay số đã chấm.
Tự kiểm: ở ca nguồn OK không span nào bị bỏ và hạng (tốt nhất, xấu nhất) của mọi thực thể phải trùng bản ghi đóng băng.
48 ca đọc bảng span adapter đã lưu; 4 ca nguồn ERROR đọc parquet gốc qua cua_so.cat_span (như chain_spanpass_v1.py).
Mọi thực thể được tính trước; nhãn root nối sau cùng.
Dùng: python tracerca_dropnew_v1.py <thư mục lượt mới> [dataset:opaque_id]
"""
import json
import sys
import time
from collections import Counter
from pathlib import Path

import pandas as pd

BASE = Path("/home/ubuntu/rca/T-032")
sys.path.insert(0, str(BASE / "scripts"))
import tracerca_core_and_td_v1 as td  # noqa: E402
import chain_position_v1 as cp  # noqa: E402


def rank_of(scores):
    out, offset = {}, 0
    for value in sorted(set(scores.values()), reverse=True):
        group = [e for e, s in scores.items() if s == value]
        for e in group:
            out[e] = (offset + 1, offset + len(group))
        offset += len(group)
    return out


def drop_new(spans, t_us):
    d = spans[["serviceName", "methodName", "operationName"]].copy()
    d["methodName"] = d["methodName"].fillna(d["operationName"])
    operation = d["serviceName"].astype(str) + "_" + d["methodName"].astype(str)
    end = spans["startTime"].astype("int64") + spans["duration"].astype("int64")
    after = end >= t_us
    newops = sorted(set(operation[after]) - set(operation[~after]))
    mask = after & operation.isin(newops)
    info = {"rows": int(len(spans)), "spans_after": int(after.sum()), "traces_after": int(spans.loc[after, "traceID"].nunique()),
            "new_operations": newops, "spans_dropped": int(mask.sum()),
            "traces_touched": int(spans.loc[mask, "traceID"].nunique()) if mask.any() else 0}
    return (spans.loc[~mask].copy() if mask.any() else spans), info


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    (out / "cases").mkdir()
    only = sys.argv[2] if len(sys.argv) > 2 else None
    from replay_tracerca_v3 import table_columns
    from p3 import cua_so, selector
    from p3.adapters import tracerca as adapter_module
    allow = selector.nap_allowlist(BASE / "repo/results/T-022/allowlist-dev.json")
    index = td.read(BASE / "repo/results/T-024/ban-ghi-dua-vao-cham.json")["records"]
    labels = {(r["dataset"], r["opaque_id"]): r for r in td.read(td.LABELS)["main_rows"] if r["method"] == "tracerca"}
    cases = []
    for row in td.read(td.PLAN)["rows"]:
        dataset, opaque_id = row["dataset"], row["opaque_id"]
        if only and only != dataset + ":" + opaque_id:
            continue
        began = time.time()
        label = labels[(dataset, opaque_id)]
        base = {"dataset": dataset, "opaque_id": opaque_id, "source_status": row["source_status"]}
        if row["source_status"] == "OK":
            directory = td.REUSED.get(row.get("replay_phase_already_valid"), td.COHORT / "cases" / dataset / opaque_id)
            entry = td.read(directory / "capture/calls/001-adapter.json")
            spans = pd.DataFrame(table_columns(directory / "capture", entry["entry"]["input"]))
            t = int(entry["entry"]["t_seconds"])
            source = "bảng span adapter TraceRCA đã lưu"
        else:
            e = [e for e in index if e["method"] == "tracerca" and e["opaque_id"] == opaque_id][0]
            t = int(td.read(BASE / "repo" / e["path"])["window"]["t"])
            files = selector.chon_ca(allow, opaque_id, Path("/home/ubuntu/rca/T-031/repo"), kiem_hash=True, tep=["traces.parquet"])
            spans = cua_so.cat_span(pd.read_parquet(files["traces.parquet"]), t)
            source = "parquet gốc qua cua_so.cat_span"
        kept, info = drop_new(spans, t * 1_000_000)
        try:
            result = adapter_module.chay(kept, t)   # mã native, chưa dùng nhãn
        except Exception as error:  # giữ lượt hỏng
            cases.append({**base, "status": "TOOL_ERROR", "error": type(error).__name__ + ": " + str(error)[:300], "drop": info})
            print(dataset, opaque_id, "TOOL_ERROR", error, flush=True)
            continue
        item = {**base, "span_source": source, "t_seconds": t, "drop": info, "branch_status": result["status"], "branch_error": result.get("error")}
        scores, top_op = {}, {}
        for op, svc, key in result.get("items", []):
            if svc not in scores or key[0] > scores[svc]:
                scores[svc], top_op[svc] = key[0], op
        rank = rank_of(scores)
        item["entity_ranking"] = [{"entity": e, "rank_min": r[0], "rank_max": r[1], "score": scores[e], "operation": top_op[e]}
                                  for e, r in sorted(rank.items(), key=lambda x: (x[1][0], x[0]))]
        item["n_entities"] = len(rank)
        # tự kiểm với bản ghi đóng băng (chỉ ca nguồn OK)
        ref = label["source"]["records"][0]
        frozen = td.read(BASE / "repo" / ref["path"])
        item["frozen_status"] = frozen["status"]
        if frozen["status"] == "OK":
            f = {e: tuple(r) for e, r in cp.ranks_of(frozen, "tracerca").items()}
            item["self_check"] = {"no_span_dropped": info["spans_dropped"] == 0, "ranks_equal_frozen": f == rank}
        # --- từ đây nối nhãn ---
        root = label["root"]
        item.update({"root": root, "fault": label["fault"], "cell": label["cell"], "root_ranked": root in rank})
        if root in rank:
            item.update({"root_rank_min": rank[root][0], "root_rank_max": rank[root][1],
                         "above_root": sorted(e for e in rank if e != root and rank[e][1] < rank[root][0])})
        item["top"] = sorted(e for e in rank if rank[e][0] == 1)
        item["wall_s"] = round(time.time() - began, 1)
        (out / "cases" / (dataset + "-" + opaque_id + ".json")).write_text(json.dumps(item, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        cases.append(item)
        print(dataset, opaque_id, row["source_status"], "→", result["status"], "dropped", info["spans_dropped"], item.get("self_check"),
              "root", item.get("root_rank_min"), item.get("root_rank_max"), "top", item["top"], item["wall_s"], flush=True)
    ok_src = [c for c in cases if c.get("frozen_status") == "OK"]
    err_src = [c for c in cases if c.get("source_status") != "OK" and "drop" in c]
    summary = {"n_cases": len(cases), "source_status": dict(Counter(c["source_status"] for c in cases)),
               "tool_errors": sum(c.get("status") == "TOOL_ERROR" for c in cases),
               "self_check": {"cases_source_ok": len(ok_src), "no_span_dropped": sum(c["self_check"]["no_span_dropped"] for c in ok_src),
                              "ranks_equal_frozen": sum(c["self_check"]["ranks_equal_frozen"] for c in ok_src),
                              "not_equal": [c["opaque_id"] for c in ok_src if not c["self_check"]["ranks_equal_frozen"]]},
               "error_source_cases": [{k: c.get(k) for k in ("opaque_id", "cell", "branch_status", "branch_error", "root", "root_ranked", "root_rank_min", "root_rank_max",
                                                               "n_entities", "top", "above_root")} | {"drop": c["drop"]} for c in err_src],
               "error_source_hit1": sum(c.get("root_rank_max") == 1 for c in err_src),
               "error_source_hit5": sum(c.get("root_rank_max") is not None and c["root_rank_max"] <= 5 for c in err_src)}
    result = {"schema": "T032-tracerca-dropnew-v1", "design": "results/T-032/thiet-ke-phep-doi-013.md mục 3",
              "note": "Đổi đầu vào để chẩn đoán; không thay số đã chấm.", "methods_executed": ["tracerca (adapter native, đầu vào đã bỏ thao tác thiếu nền)"],
              "sources": {"plan_sha256": td.sha(td.PLAN), "labels_sha256": td.sha(td.LABELS)}, "summary": summary, "cases": cases}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1), flush=True)
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
