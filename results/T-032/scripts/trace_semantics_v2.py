"""T-032 mục 4 (Q-120): ngữ nghĩa lời gọi theo mã nguồn, và mức đo được "dịch vụ gọi chờ root" theo từng ca dev.

Chạy trên EC2, chỉ đọc. Không gọi phương pháp, không chạy mã của ba kho nguồn (chỉ git grep / git show).
Phần 1 — vị trí lời gọi trong mã nguồn:
  Train Ticket: với mỗi tag ứng viên (các tag mà source_fingerprint_v1 cho khớp đủ tập tên span) và mỗi loại lời gọi quan sát được
  (dịch vụ gọi A -> route của dịch vụ được gọi B): tìm phần tĩnh của đường dẫn route trong `A/src/main`; với mỗi chỗ tìm thấy,
  xét 4 dòng kết thúc ở dòng đó có `restTemplate.exchange(` hay không (lời gọi đồng bộ, luồng gọi chờ trả lời), và file đó có
  cấu trúc chạy song song/bất đồng bộ (`executorService`, `@Async`, `CompletableFuture`, `Future<`, `new Thread`) hay không.
  Augmented-OnlineBoutique (một commit): với mỗi loại lời gọi (A -> rpc của B): tìm `.Method(` trong `src/A`; ghi có `go func`/`go `
  trong 3 dòng trước (goroutine) hay `.future(` (Python) hay không; ghi file có gắn client interceptor của OpenTelemetry không.
Phần 2 — theo ca (52 ca dev): dùng runs/call-interval-001 (48 ca có bảng span đã lưu); 4 ca RE2 nguồn TraceRCA ERROR được tính
  thêm từ parquet gốc qua đúng bước cắt cửa sổ của runner (cua_so.cat_ca), bằng cùng hàm của call_interval_table_v1.
  Mức đo được, theo định nghĩa của SPEC, với tiêu chí khai trước ở đây:
    C1 (quan hệ): root có ít nhất một cạnh gọi tới với >= 20 lời gọi ở mỗi phía mốc.
    C2 (khoảng hợp lệ): ở đoạn nền của cạnh đó, tỷ lệ lời gọi có gap = d_p - d_c < 0 không quá 1%
        (span phía được gọi không dài hơn span phía gọi; đại lượng này không phụ thuộc lệch đồng hồ).
    C3 (ngữ nghĩa theo mã nguồn): mọi chỗ gọi tìm được của cặp (A, root) là lời gọi đồng bộ, ở mọi phiên bản ứng viên.
    "đo được (có điều kiện)": C1, C2, C3 đều đạt cho ít nhất một cạnh. Điều kiện: mã đã triển khai gọi theo cùng cách với phiên bản
        ứng viên, và span phía gọi do thư viện/agent tạo bao quanh lời gọi. Đại lượng đo được là thời lượng span phía gọi (thời gian
        dịch vụ gọi chờ lời gọi tới root trả về), tách thành phần nằm trong span của root (d_c) và phần ngoài (gap).
    "đo được một phần": có C1 nhưng thiếu C2 hoặc C3.
    "không đo được": không có C1 (root không được dịch vụ nào gọi trong trace, hoặc quá ít lời gọi).
  Không mức nào cho biết phần gap gồm đường truyền, hàng đợi hay xử lý phía gọi.
Bản v2 (viết sau khi đã xem kết quả lượt trace-semantics-001, trước khi chạy lượt 002). Sửa ba chỗ của phép quét mã nguồn, vì bản v1
đếm sai chỗ gọi; tiêu chí C1, C2 không đổi, C3 được nêu lại cho chính xác:
  - Train Ticket: một chỗ tìm thấy được xếp loại "lời gọi" (đường dẫn nằm trong 5 dòng của `restTemplate.exchange(`), hoặc
    "hằng được dùng trong lời gọi" (dòng gán chuỗi cho một tên, và tên đó xuất hiện trong 5 dòng của một `restTemplate.exchange(`
    cùng file), hoặc "khác". Bản v1 coi dòng khai hằng là chỗ gọi không đồng bộ, và hạ cả cặp chỉ vì file có cấu trúc song song.
  - C3 (nêu lại): ở mọi tag ứng viên, cặp (A, root) có ít nhất một chỗ gọi và mọi chỗ tìm thấy thuộc hai loại đầu, tức là lời gọi
    yêu cầu–trả lời chặn qua `restTemplate.exchange`. Việc file có `ExecutorService`/`@Async` được ghi riêng thành cờ lưu ý
    `parallel_construct_in_file`, không làm rớt C3: lời gọi chặn nằm trong luồng nào thì span phía gọi vẫn là thời gian chờ lời gọi đó.
  - Augmented-OnlineBoutique: nhận cả lời gọi viết xuống dòng (`...Client(conn).` rồi `Method(ctx, ...)` ở dòng sau); loại file sinh tự động
    và file `__failpoint_stash__` theo tên file (bản v1 loại nhầm dòng gọi có chữ `_pb2`); interceptor phía gọi xét theo cả dịch vụ.
Dùng: python trace_semantics_v2.py <thư mục lượt mới>
"""
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

BASE = Path("/home/ubuntu/rca/T-032")
sys.path.insert(0, str(BASE / "scripts"))
SRC = BASE / "sources/instrumentation-002"
TT, AOB = SRC / "train-ticket", SRC / "Augmented-OnlineBoutique"
INVENTORY = BASE / "runs/call-interval-001/inventory.json"
INTERVALS = BASE / "runs/call-interval-001/summary.json"
FINGERPRINT = BASE / "runs/source-fingerprint-001/fingerprint.json"
ASYNC = re.compile(r"executorService|ExecutorService|@Async|CompletableFuture|Future<|new Thread")
MIN_CALLS = 20


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo)] + list(args), capture_output=True, text=True, errors="replace").stdout


def scan_train_ticket(inventory, fingerprint):
    tags = fingerprint["train_ticket"]["tags"]
    observed = fingerprint["train_ticket"]["observed"]
    candidates = [t for t, v in tags.items() if v["routes_found"] == observed["routes"] and v["repository_ok"] == observed["repository_spans"]
                  and v["services_with_directory"] == observed["services"]]
    kinds = []
    for row in inventory["RE2-TT"]["cross_service_calls"]:
        m = re.fullmatch(r"(GET|POST|PUT|DELETE|PATCH) (/.*)", row["callee_op"])
        if m:
            kinds.append((row["caller"], row["callee"], m.group(1), m.group(2), row["count"]))
    files_cache = {}
    out = []
    for caller, callee, method, path, count in sorted(kinds):
        static = path.split("{")[0].rstrip("/")
        per_tag = {}
        for tag in candidates:
            commit = tags[tag]["commit"]
            hits = [line for line in git(TT, "grep", "-n", "-F", "--", static, commit, "--", caller + "/src/main").split("\n") if line.strip()]
            sites = []
            for line in hits:
                _commit, file, number, _rest = line.split(":", 3)
                key = (commit, file)
                if key not in files_cache:
                    files_cache[key] = git(TT, "show", commit + ":" + file).split("\n")
                text = files_cache[key]
                n = int(number)
                window = "\n".join(text[max(0, n - 5):n])
                line_text = text[n - 1] if n - 1 < len(text) else ""
                kind = "khác"
                if "restTemplate.exchange(" in window:
                    kind = "lời gọi"
                elif line_text.strip().startswith(("//", "*", "/*")):
                    kind = "chú thích"
                else:
                    assigned = re.search(r"(\w+)\s*=\s*(?:\w+\s*\+\s*)?\"", line_text) or re.search(r"(\w+)\s*=\s*$", text[n - 2] if n >= 2 else "")
                    if assigned:
                        name = assigned.group(1)
                        for i, row in enumerate(text):
                            if "restTemplate.exchange(" in row and re.search(r"\b" + re.escape(name) + r"\b", "\n".join(text[i:i + 5])):
                                kind = "hằng được dùng trong lời gọi"
                                break
                sites.append({"file": file, "line": n, "kind": kind, "file_has_async_construct": bool(ASYNC.search("\n".join(text)))})
            real = [s for s in sites if s["kind"] != "chú thích"]
            per_tag[tag] = {"sites": len(real), "sites_call": sum(s["kind"] == "lời gọi" for s in real),
                            "sites_constant_used_in_call": sum(s["kind"] == "hằng được dùng trong lời gọi" for s in real),
                            "sites_other": sum(s["kind"] == "khác" for s in real), "sites_comment_only": len(sites) - len(real),
                            "parallel_construct_in_file": any(s["file_has_async_construct"] for s in real),
                            "sites_in_restTemplate_exchange": sum(s["kind"] == "lời gọi" for s in real),
                            "sites_in_file_with_async_construct": sum(s["file_has_async_construct"] for s in real),
                            "locations": [s["file"].split("/", 1)[1].rsplit("/", 1)[-1] + ":" + str(s["line"]) + " (" + s["kind"] + ")" for s in sites][:6]}
        sync_all = all(v["sites"] > 0 and v["sites_other"] == 0 and (v["sites_call"] + v["sites_constant_used_in_call"]) > 0 for v in per_tag.values())
        found_all = all(v["sites"] > 0 for v in per_tag.values())
        out.append({"caller": caller, "callee": callee, "method": method, "path": path, "observed_calls": count, "per_tag": per_tag,
                    "call_site_found_in_every_candidate": found_all, "synchronous_resttemplate_in_every_candidate": sync_all,
                    "parallel_construct_in_file_at_tags": [t for t, v in per_tag.items() if v["parallel_construct_in_file"]]})
    return candidates, out


def scan_online_boutique(inventory):
    commit = git(AOB, "rev-parse", "HEAD").strip()
    out = []
    for row in sorted(inventory["Nezha-OB"]["cross_service_calls"], key=lambda r: (r["caller"], r["callee"], r["callee_op"])):
        rpc = row["caller_op"].lstrip("/").replace("grpc.", "").replace("hipstershop.", "")
        method = rpc.split("/")[-1]
        generated = ("/genproto/", ".pb.go:", "_pb2.py:", "_pb2_grpc.py:", "__failpoint_stash__:", "_test.go:")
        hits = [line for line in git(AOB, "grep", "-n", "-E", "--", r"(\.|^[[:space:]]+)" + method + r"\(", commit, "--", "src/" + row["caller"]).split("\n")
                if line.strip() and not any(g in line for g in generated)]
        service_files = [f for f in git(AOB, "grep", "-l", "-E", "--", r"otelgrpc\.UnaryClientInterceptor|client_interceptor\(\)|GrpcInstrumentorClient",
                                        commit, "--", "src/" + row["caller"]).split("\n") if f.strip() and not any(g.rstrip(":") in f for g in generated)]
        sites = []
        for line in hits:
            _commit, file, number, rest = line.split(":", 3)
            text = git(AOB, "show", commit + ":" + file).split("\n")
            n = int(number)
            before = "\n".join(text[max(0, n - 4):n])
            if re.search(r"\bfunc \(|\bdef " + method + r"\(", rest):
                continue  # dòng định nghĩa hàm cùng tên, không phải chỗ gọi
            sites.append({"file": file, "line": n, "code": rest.strip()[:140], "goroutine_or_future_nearby": bool(re.search(r"\bgo func|\bgo \w+\(|\.future\(|asyncio|await ", before)),
                          "file_has_otel_client_interceptor": bool(service_files)})
        out.append({"caller": row["caller"], "callee": row["callee"], "caller_span": row["caller_op"], "callee_span": row["callee_op"], "observed_calls": row["count"],
                    "sites": sites, "call_site_found": bool(sites), "files_with_client_interceptor_in_service": [f.split(":", 1)[-1] for f in service_files],
                    "synchronous": bool(sites) and not any(s["goroutine_or_future_nearby"] for s in sites),
                    "client_interceptor_in_call_file": any(s["file_has_otel_client_interceptor"] for s in sites)})
    return commit, out


def extra_cases(done):
    """4 ca RE2 không có bảng span đã lưu (nguồn TraceRCA ERROR): tính từ parquet gốc qua cua_so.cat_ca."""
    import pandas as pd
    import call_interval_table_v1 as ci
    import tracerca_core_and_td_v1 as td
    from p3 import cua_so, selector
    allow = selector.nap_allowlist(BASE / "repo/results/T-022/allowlist-dev.json")
    labels = {(r["dataset"], r["opaque_id"]): r for r in td.read(td.LABELS)["main_rows"] if r["method"] == "tracerca"}
    index = read(BASE / "repo/results/T-024/ban-ghi-dua-vao-cham.json")["records"]
    out = []
    for row in td.read(td.PLAN)["rows"]:
        key = (row["dataset"], row["opaque_id"])
        if key in done or row["dataset"] != "RE2-TT":
            continue
        entry = [e for e in index if e["method"] == "tracerca" and e["opaque_id"] == row["opaque_id"]][0]
        t = read(BASE / "repo" / entry["path"])["window"]["t"]
        files = selector.chon_ca(allow, row["opaque_id"], Path("/home/ubuntu/rca/T-031/repo"), kiem_hash=True, tep=["traces.parquet"])
        traces = pd.read_parquet(files["traces.parquet"])
        spans = cua_so.cat_span(traces, t)
        spans = spans.copy()
        spans["methodName"] = spans["methodName"].fillna(spans["operationName"])
        import numpy as np
        start = spans["startTime"].to_numpy(dtype="int64")
        duration = spans["duration"].to_numpy(dtype="int64")
        end = start + duration
        t_us = int(t) * 1_000_000
        service = spans["serviceName"].astype(str).to_numpy()
        ident = (spans["traceID"].astype(str) + "|" + spans["spanID"].astype(str)).to_numpy()
        position = pd.Series(np.arange(len(spans)), index=ident)
        position = position[~position.index.duplicated(keep=False)]
        parent = (spans["traceID"].astype(str) + "|" + spans["parentSpanID"].astype(str)).map(position).to_numpy(dtype="float64")
        has_parent = ~np.isnan(parent)
        p = np.where(has_parent, parent, 0).astype("int64")
        cross = has_parent & (service[p] != service)
        c_index, p_index = np.flatnonzero(cross), p[cross]
        calls = pd.DataFrame({"caller": service[p_index], "callee": service[c_index], "d_p": duration[p_index], "d_c": duration[c_index],
                              "pre": start[c_index] - start[p_index], "post": end[p_index] - end[c_index], "after": end[p_index] >= t_us})
        calls["gap"] = calls["d_p"] - calls["d_c"]
        label = labels[key]
        incoming = {}
        for (a, b), g in calls[calls["callee"] == label["root"]].groupby(["caller", "callee"], sort=True):
            before, after = ci.block(g[~g["after"]]), ci.block(g[g["after"]])
            incoming[a + "→" + b] = {"caller": a, "callee": b, "before": before, "after": after,
                                          "ratio_after_over_before": {k: ci.ratio(after, before, k) for k in ("median_d_c_us", "median_gap_us")}}
        out.append({"dataset": "RE2-TT", "opaque_id": row["opaque_id"], "root": label["root"], "fault": label["fault"], "cell": label["cell"],
                    "status": "OK", "span_source": "parquet gốc qua cua_so.cat_span (TraceRCA nguồn ERROR, không có bảng đã lưu)",
                    "n_calls": int(len(calls)), "incoming_to_root": incoming})
    return out


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    inventory, fingerprint, intervals = read(INVENTORY), read(FINGERPRINT), read(INTERVALS)
    candidates, tt_sites = scan_train_ticket(inventory, fingerprint)
    ob_commit, ob_sites = scan_online_boutique(inventory)
    tt_pair = {}
    for row in tt_sites:
        pair = tt_pair.setdefault((row["caller"], row["callee"]), {"kinds": 0, "sync_all": True, "found_all": True})
        pair["kinds"] += 1
        pair["sync_all"] &= row["synchronous_resttemplate_in_every_candidate"]
        pair["found_all"] &= row["call_site_found_in_every_candidate"]
    ob_pair = {}
    for row in ob_sites:
        pair = ob_pair.setdefault((row["caller"], row["callee"]), {"kinds": 0, "sync_all": True, "found_all": True, "interceptor": True})
        pair["kinds"] += 1
        pair["sync_all"] &= row["synchronous"]
        pair["found_all"] &= row["call_site_found"]
        pair["interceptor"] &= row["client_interceptor_in_call_file"]
    cases = [c for c in intervals["cases"] if c["status"] == "OK"]
    for c in cases:
        c["span_source"] = "bảng span adapter TraceRCA đã lưu"
    done = {(c["dataset"], c["opaque_id"]) for c in cases}
    cases.extend(extra_cases(done))
    table = []
    for c in sorted(cases, key=lambda c: (c["dataset"], c["opaque_id"])):
        pairs = tt_pair if c["dataset"] == "RE2-TT" else ob_pair
        edges = []
        for name, v in c["incoming_to_root"].items():
            enough = v["before"]["n"] >= MIN_CALLS and v["after"]["n"] >= MIN_CALLS
            source = pairs.get((v["caller"], v["callee"]))
            c2 = enough and v["before"]["gap_negative_share"] <= 0.01
            c3 = bool(source and source["found_all"] and source["sync_all"])
            r = v["ratio_after_over_before"]
            dc, gp = r.get("median_d_c_us"), r.get("median_gap_us")
            grew = (None if not enough or dc is None or gp is None else "cả hai" if dc >= 2 and gp >= 2 else "trong span của root" if dc >= 2
                    else "ngoài span của root" if gp >= 2 else "không phần nào gấp đôi")
            edges.append({"edge": name, "n_before": v["before"]["n"], "n_after": v["after"]["n"], "C1_enough_calls": enough,
                          "nested_share_before": v["before"].get("nested_share"), "gap_negative_share_before": v["before"].get("gap_negative_share"),
                          "C2_interval_valid": bool(c2), "C3_source_synchronous": c3, "source_pair_found": bool(source and source["found_all"]),
                          "d_c_ratio": dc, "gap_ratio": gp, "what_grew": grew,
                          "median_d_p_before_us": v["before"].get("median_d_p_us"), "median_d_p_after_us": v["after"].get("median_d_p_us")})
        c1 = any(e["C1_enough_calls"] for e in edges)
        full = any(e["C1_enough_calls"] and e["C2_interval_valid"] and e["C3_source_synchronous"] for e in edges)
        level = "đo được (có điều kiện)" if full else "đo được một phần" if c1 else "không đo được"
        reason = ("có cạnh gọi tới root đủ lời gọi, khoảng hợp lệ, mã nguồn ứng viên gọi đồng bộ" if full else
                  "có cạnh gọi tới root nhưng thiếu C2 hoặc C3" if c1 else
                  "root không được dịch vụ nào gọi trong trace" if not edges else "cạnh gọi tới root có dưới 20 lời gọi ở một phía mốc")
        table.append({"dataset": c["dataset"], "opaque_id": c["opaque_id"], "root": c["root"], "fault": c["fault"], "cell": c["cell"],
                      "span_source": c["span_source"], "incoming_edges": len(edges), "level": level, "reason": reason, "edges": edges})
    summary = {}
    for dataset in ("RE2-TT", "Nezha-OB"):
        rows = [t for t in table if t["dataset"] == dataset]
        summary[dataset] = {"n_cases": len(rows), "by_level": dict(Counter(t["level"] for t in rows)), "by_reason": dict(Counter(t["reason"] for t in rows)),
                            "by_fault_level": {f: dict(Counter(t["level"] for t in rows if t["fault"] == f)) for f in sorted({t["fault"] for t in rows})},
                            "not_measurable_roots": dict(Counter(t["root"] for t in rows if t["level"] == "không đo được")),
                            "edges_C1": sum(e["C1_enough_calls"] for t in rows for e in t["edges"]),
                            "edges_C1_C2": sum(e["C1_enough_calls"] and e["C2_interval_valid"] for t in rows for e in t["edges"]),
                            "edges_C1_C2_C3": sum(e["C1_enough_calls"] and e["C2_interval_valid"] and e["C3_source_synchronous"] for t in rows for e in t["edges"]),
                            "edges_what_grew": dict(Counter(str(e["what_grew"]) for t in rows for e in t["edges"] if e["C1_enough_calls"]))}
    observed_names = [r["name"] for r in inventory["RE2-TT"]["service_span_names"]]
    stash = [f for f in git(AOB, "ls-tree", "-r", "--name-only", "HEAD").split("\n") if "failpoint" in f.lower()]
    source = {"facts": {"re2_left_parallel_route_observed": any("left_parallel" in n for n in observed_names),
                        "re2_trips_left_route_observed": any(n.endswith("/trips/left") for n in observed_names),
                        "augmented_ob_failpoint_files": stash},
              "train_ticket": {"candidate_tags": candidates, "call_kinds": len(tt_sites),
                               "call_kinds_found_in_every_candidate": sum(r["call_site_found_in_every_candidate"] for r in tt_sites),
                               "call_kinds_synchronous_in_every_candidate": sum(r["synchronous_resttemplate_in_every_candidate"] for r in tt_sites),
                               "service_pairs": len(tt_pair), "service_pairs_synchronous": sum(v["sync_all"] and v["found_all"] for v in tt_pair.values()),
                               "call_kinds_with_parallel_construct_in_file": {t: sum(t in r["parallel_construct_in_file_at_tags"] for r in tt_sites) for t in candidates},
                               "rows": tt_sites},
              "online_boutique": {"commit": ob_commit, "call_kinds": len(ob_sites), "call_kinds_found": sum(r["call_site_found"] for r in ob_sites),
                                  "call_kinds_synchronous": sum(r["synchronous"] for r in ob_sites),
                                  "call_kinds_with_client_interceptor_in_file": sum(r["client_interceptor_in_call_file"] for r in ob_sites),
                                  "service_pairs": len(ob_pair), "rows": ob_sites}}
    result = {"schema": "T032-trace-semantics-v2", "methods_executed": False,
              "sources": {"inventory_sha256": sha(INVENTORY), "intervals_sha256": sha(INTERVALS), "fingerprint_sha256": sha(FINGERPRINT),
                          "this_script_sha256": sha(__file__)},
              "criteria": "xem phần đầu script: C1 >= 20 lời gọi mỗi phía; C2 gap âm <= 1% ở nền; C3 mọi chỗ gọi đồng bộ ở mọi phiên bản ứng viên",
              "summary": summary, "source_scan": source, "cases": table}
    (out / "semantics.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "rows"} for k, v in source.items()}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
