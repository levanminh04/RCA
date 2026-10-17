"""T-040 — tổng hợp P5b từ đầu ra đã lưu.

Chỉ đọc: results/T-034..T-039, src/do_thi_tinh, tasks/T-03x (REVIEW/LOG), docs/DECISIONS.md,
B16 của FlashTicket. Ghi: results/T-040/ (dau-vao.json, tong-hop.json, runs/<run>/).
Không chạy RCA, không dựng lại graph, không đọc telemetry thô, test hoặc dữ liệu khóa.
Không nhận nhãn, tên ca hoặc mốc tiêm; mã ca opaque chỉ để điều phối.

Lệnh: py -3 -X utf8 -B results/T-040/tong_hop.py --run tong-hop-001
"""
import argparse
import ctypes
import gzip
import hashlib
import json
import os
import subprocess
import sys
import time
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "results", "T-040")
FT_REPO = "D:/Project/flash-ticket-platform"
FT_B16 = FT_REPO + "/docs/architecture/B16-observability-baseline.md"

MANIFESTS = [
    # id, đường dẫn manifest, gốc của task để tìm tệp ngoài manifest
    ("T-034", "results/T-034/runs/manifest-cuoi-007/manifest.json", "results/T-034"),
    ("T-035", "results/T-035/manifest.json", "results/T-035"),
    ("T-036-R1", "results/T-036/manifest.json", "results/T-036"),
    ("T-036-V2", "results/T-036/runs/doi-chieu-smtp-001/manifest.json", "results/T-036"),
    ("T-036-V2-artifacts", "results/T-036/runs/doi-chieu-smtp-001/artifact-manifest.json", "results/T-036"),
    ("T-037", "results/T-037/manifest.json", "results/T-037"),
    ("T-038", "results/T-038/manifest.json", "results/T-038"),
    ("T-038-sua-r1", "results/T-038/runs/sua-r1-20261017-001/manifest.json", "results/T-038"),
    ("T-039", "results/T-039/manifest.json", "results/T-039"),
]

BRANCH_PINS = {
    "FT": "results/T-037/runs/doi-chieu-smtp-001/pin.json",
    "TT": "results/T-038/runs/doi-chieu-smtp-001/pin.json",
    "OB": "results/T-039/runs/doi-chieu-smtp-001/pin.json",
}

STATIC_MODELS = {
    # bản hiện hành theo manifest/bàn giao của từng nhánh
    "FT": {"entity": "results/T-037/do-thi/thuc-the.json",
           "operation": "results/T-037/do-thi/thao-tac.json",
           "projection": "results/T-037/do-thi/phep-chieu.json"},
    # bản sửa R1 của người làm T-038 (ban-giao-T040.json); gói sửa đã dừng phản biện (Q-171), T-038 chưa nghiệm thu
    "TT": {"entity": "results/T-038/do-thi/thuc-the.json",
           "operation": "results/T-038/do-thi/thao-tac.json",
           "projection": "results/T-038/do-thi/chieu-thao-tac.json"},
    "OB": {"entity": "results/T-039/runs/doi-chieu-smtp-001/do-thi/thuc-the.json",
           "operation": "results/T-039/runs/doi-chieu-smtp-001/do-thi/thao-tac.json",
           "projection": "results/T-039/runs/doi-chieu-smtp-001/do-thi/chieu-thuc-the.json"},
}

COMPARE_SUMMARIES = {
    "TT": "results/T-038/runs/sua-r1-20261017-001/checks/full1069-002/summary.json",
    "OB": "results/T-039/runs/doi-chieu-smtp-001/summary.json",
}

LIVE_CODE = ["src/do_thi_tinh/__init__.py", "src/do_thi_tinh/build.py", "src/do_thi_tinh/compare.py"]


# ---------------------------------------------------------------- tiện ích

def p(rel):
    return os.path.join(ROOT, rel.replace("/", os.sep))


def sha256_file(path, bufsize=1 << 20):
    h = hashlib.sha256()
    n = 0
    with open(path, "rb") as f:
        while True:
            b = f.read(bufsize)
            if not b:
                break
            h.update(b)
            n += len(b)
    return h.hexdigest(), n


def load_json(rel):
    path = p(rel)
    if path.endswith(".gz"):
        with gzip.open(path, "rt", encoding="utf-8") as f:
            return json.load(f)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def dump_json(obj, path, gz=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=False)
    if gz:
        with gzip.open(path, "wt", encoding="utf-8") as f:
            f.write(data)
    else:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(data + "\n")


def peak_rss_bytes():
    """Peak working set của tiến trình (Windows). Lỗi thì trả None, không dừng lượt."""
    try:
        class PMC(ctypes.Structure):
            _fields_ = [("cb", ctypes.c_ulong), ("PageFaultCount", ctypes.c_ulong),
                        ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
                        ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t), ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                        ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t)]
        c = PMC()
        c.cb = ctypes.sizeof(PMC)
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        psapi = ctypes.WinDLL("psapi", use_last_error=True)
        k32.GetCurrentProcess.restype = ctypes.c_void_p
        psapi.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(PMC), ctypes.c_ulong]
        ok = psapi.GetProcessMemoryInfo(k32.GetCurrentProcess(), ctypes.byref(c), c.cb)
        return int(c.PeakWorkingSetSize) if ok else None
    except Exception:
        return None


class Progress:
    def __init__(self, path):
        self.path = path
        self.t0 = time.time()
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def log(self, step, **kw):
        rec = {"t_s": round(time.time() - self.t0, 3), "step": step}
        rec.update(kw)
        with open(self.path, "a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(json.dumps(rec, ensure_ascii=False), flush=True)


def tuple_key(k):
    """Khóa đối chiếu dạng list (có thể lồng list địa chỉ) → tuple băm được."""
    if isinstance(k, list):
        return tuple(tuple_key(x) for x in k)
    if isinstance(k, dict):
        return tuple(sorted((a, tuple_key(b)) for a, b in k.items()))
    return k


# ---------------------------------------------------------------- bước 1: đầu vào

def verify_manifest(mid, mrel, prog):
    m = load_json(mrel)
    files = m.get("files", [])
    ok = 0
    bad = []
    missing = []
    total = 0
    for f in files:
        path = p(f["path"])
        if not os.path.exists(path):
            missing.append(f["path"])
            continue
        h, n = sha256_file(path)
        total += n
        if h == f["sha256"] and (f.get("bytes") is None or f["bytes"] == n):
            ok += 1
        else:
            bad.append({"path": f["path"], "expected": f["sha256"], "actual": h})
    msha, _ = sha256_file(p(mrel))
    prog.log("manifest", id=mid, files=len(files), ok=ok, mismatch=len(bad), missing=len(missing))
    return {
        "id": mid, "manifest": mrel, "manifest_sha256": msha,
        "created_utc": m.get("created_utc") or m.get("generated"),
        "state_in_manifest": m.get("state") or m.get("task_state") or m.get("status"),
        "task_accepted_in_manifest": m.get("task_accepted"),
        "files": len(files), "ok": ok, "mismatch": bad, "missing": missing, "bytes_checked": total,
        "paths": {f["path"] for f in files},
    }


def extra_files(root_rel, covered):
    out = Counter()
    examples = defaultdict(list)
    base = p(root_rel)
    for dp, dn, fn in os.walk(base):
        for name in fn:
            rel = os.path.relpath(os.path.join(dp, name), ROOT).replace(os.sep, "/")
            if rel in covered:
                continue
            parts = rel[len(root_rel) + 1:].split("/")
            grp = "/".join(parts[:2]) if parts[0] == "runs" and len(parts) > 1 else parts[0]
            out[grp] += 1
            if len(examples[grp]) < 2:
                examples[grp].append(rel)
    return {g: {"files": n, "examples": examples[g]} for g, n in sorted(out.items())}


def decisions_lines(qids):
    txt = open(p("docs/DECISIONS.md"), encoding="utf-8").read()
    found = {}
    for q in qids:
        lines = [ln for ln in txt.split("\n") if ln.startswith("| " + q + " |")]
        found[q] = {"present": bool(lines), "excerpt": lines[0][:260] if lines else None}
    return found


def decisions_mentions(task):
    txt = open(p("docs/DECISIONS.md"), encoding="utf-8").read()
    ids = []
    for ln in txt.split("\n"):
        if ln.startswith("| Q-") and task in ln:
            ids.append(ln.split("|")[1].strip())
    return ids


def decision_line_hashes(task):
    """Q → SHA-256 của dòng DECISIONS nhắc task (bỏ CR cuối dòng). Dùng để so với snapshot đã đọc."""
    txt = open(p("docs/DECISIONS.md"), encoding="utf-8").read()
    out = {}
    for ln in txt.split("\n"):
        ln = ln.rstrip("\r")
        if ln.startswith("| Q-") and task in ln:
            out[ln.split("|")[1].strip()] = hashlib.sha256(ln.encode("utf-8")).hexdigest()
    return out


def compare_decision_snapshot(snapshot_rel, task, snap=None, cur=None):
    """So các dòng quyết định hiện hành với snapshot người làm đã đọc.

    Chỉ trả lời "nguồn quyết định có đổi so với lúc đọc không" (thêm, sửa, xóa).
    Không suy nghiệm thu từ nội dung; khi lệch, người làm đọc lại và lập snapshot mới trong run mới.
    """
    snap = load_json(snapshot_rel) if snap is None else snap
    expect = {q: d["sha256"] for q, d in snap["dong"].items()}
    cur = decision_line_hashes(task) if cur is None else cur
    return {"snapshot": snapshot_rel, "task": task,
            "added": sorted(set(cur) - set(expect)),
            "removed": sorted(set(expect) - set(cur)),
            "changed": sorted(q for q in set(cur) & set(expect) if cur[q] != expect[q]),
            "unchanged": not (set(cur) ^ set(expect)) and all(cur[q] == expect[q] for q in cur),
            "trang_thai_da_doc": snap["trang_thai_da_doc"]}


def review_state_t038():
    path = p("tasks/T-038-p5b-trainticket/REVIEW.md")
    txt = open(path, encoding="utf-8").read()
    h, _ = sha256_file(path)
    r1_blocking = "### R1." in txt and "— CHẶN" in txt.split("### R1.")[1].split("\n")[0]
    tail = txt.split("## Phản hồi của người làm")[-1]
    row = [ln for ln in tail.split("\n") if ln.startswith("| R1 |")]
    cells = [c.strip() for c in row[0].split("|")[2:-1]] if row else None
    return {"path": "tasks/T-038-p5b-trainticket/REVIEW.md", "sha256": h,
            "R1_marked_blocking": r1_blocking,
            "R1_response_row_cells": cells,
            "R1_response_empty": bool(cells is not None and all(c == "" for c in cells)),
            "candidate_run": "results/T-038/runs/reviewer-r1-fix-20261016-001/",
            "candidate_used_as_input": False}


def git_ft():
    def run(args):
        try:
            return subprocess.run(["git", "-C", FT_REPO] + args, capture_output=True, text=True,
                                  encoding="utf-8", timeout=60).stdout.strip()
        except Exception as e:  # noqa
            return "ERROR: %s" % e
    return {"head": run(["rev-parse", "HEAD"]),
            "B16_worktree_status": run(["status", "--porcelain", "--", "docs/architecture/B16-observability-baseline.md"])}


def stage_inputs(prog, decision_snapshot):
    res = {"manifests": [], "pins": {}, "live_code": {}, "flashticket": {}, "acceptance": {}}
    covered = defaultdict(set)
    for mid, mrel, root_rel in MANIFESTS:
        r = verify_manifest(mid, mrel, prog)
        covered[root_rel] |= r.pop("paths")
        covered[root_rel].add(mrel)
        res["manifests"].append(r)
    # T-036-R1 là pin lịch sử: mã chung đã đổi theo Q-164. Tách lệch dự kiến khỏi lệch thật.
    v2 = load_json("results/T-036/runs/doi-chieu-smtp-001/manifest.json")
    v2_sha, _ = sha256_file(p("results/T-036/runs/doi-chieu-smtp-001/manifest.json"))
    for r in res["manifests"]:
        if r["id"] == "T-036-R1":
            r["mismatch_expected_by_V2"] = [x["path"] for x in r["mismatch"]
                                            if x["path"].startswith("src/do_thi_tinh/")]
    # mã chung hiện hành so với pin V2
    for rel in LIVE_CODE:
        h, _ = sha256_file(p(rel))
        res["live_code"][rel] = {"sha256": h,
                                 "equals_V2_pin": h == v2["code_hashes"][os.path.basename(rel)]}
    for br, rel in BRANCH_PINS.items():
        pin = load_json(rel)
        res["pins"][br] = {
            "pin": rel,
            "manifest": pin["manifest"],
            "manifest_sha256_equals_file": pin["manifest_sha256"] == v2_sha,
            "created_utc_equals": pin["created_utc"] == v2["created_utc"],
            "code_hashes_equal_V2": pin["code_hashes"] == v2["code_hashes"],
        }
    # FlashTicket B16 so với registry T-037
    reg = load_json("results/T-037/nguon.json")
    b16 = [s for s in reg["sources"] if s.get("id") == "FT-B16"][0]
    h, n = sha256_file(FT_B16)
    res["flashticket"] = {"B16_path": FT_B16, "B16_sha256": h, "B16_bytes": n,
                          "B16_equals_T037_registry": h == b16["sha256"],
                          "T037_registry_revision": b16["revision"], "git": git_ft()}
    # trạng thái chấp nhận: nguồn quyết định, không suy từ thời gian sửa file
    res["acceptance"] = {
        "decisions": decisions_lines(["Q-149", "Q-158", "Q-164", "Q-165", "Q-167", "Q-168", "Q-171"]),
        "T038_decisions_mentions": decisions_mentions("T-038"),
        "T038_decision_snapshot": compare_decision_snapshot(decision_snapshot, "T-038"),
        "T038_review": review_state_t038(),
        "review_files": {t: os.path.exists(p("tasks/%s/REVIEW.md" % t)) for t in [
            "T-035-p5-do-thi-tu-trace", "T-036-p5b-hop-dong-chung", "T-037-p5b-flashticket",
            "T-038-p5b-trainticket", "T-039-p5b-online-boutique"]},
    }
    res["extra_files_not_in_manifests"] = {root: extra_files(root, cov) for root, cov in covered.items()}
    return res


# ---------------------------------------------------------------- bước 2: mô hình tĩnh

def edge_key_entity(e):
    return (e["source"], e["target"], e.get("type"), e.get("channel"),
            tuple_key(e.get("messaging")) if e.get("messaging") else None)


def messaging_completeness(e):
    m = e.get("messaging") or {}
    ch = e.get("channel")
    need = {"publish": ["broker", "broker_scope", "exchange", "routing_key"],
            "consume": ["broker", "broker_scope", "queue"],
            "logical-message": ["broker", "broker_scope", "exchange", "routing_key", "queue"]}.get(ch)
    if need is None:
        return None
    missing = [k for k in need if m.get(k) is None]
    return "complete" if not missing else "missing:" + ",".join(missing)


def stage_static(prog):
    out = {}
    for sysname, files in STATIC_MODELS.items():
        ent = load_json(files["entity"])
        op = load_json(files["operation"])
        proj = load_json(files["projection"])
        ent_pairs = {(e["source"], e["target"]) for e in ent["edges"]}
        ent_keys = {edge_key_entity(e) for e in ent["edges"]}
        proj_keys = {edge_key_entity(e) for e in proj["edges"]}
        msg = Counter()
        for e in ent["edges"]:
            c = messaging_completeness(e)
            if c is not None:
                msg["%s|%s" % (e.get("channel"), c)] += 1
        sig_kind = Counter(s.get("kind") for s in ent.get("signals", []))
        sig_shared = sum(1 for s in ent.get("signals", []) if s.get("shared"))
        sig_op = sum(1 for s in ent.get("signals", []) if s.get("operation") is not None)
        runtime_null = sum(1 for n in op["nodes"] if n.get("runtime_name") is None)
        rec_type_channel = Counter("%s|%s" % (r.get("type"), r.get("channel")) for r in ent.get("records", []))
        out[sysname] = {
            "files": {k: {"path": v, "sha256": sha256_file(p(v))[0]} for k, v in files.items()},
            "scope": ent.get("scope"),
            "schema_version": ent.get("schema_version"),
            "evidence": ent.get("evidence"),
            "counts": {
                "inventory": len(ent.get("inventory", [])),
                "observed_nodes": len(ent.get("observed_nodes", [])),
                "relation_records": len(ent.get("records", [])),
                "entity_edges": len(ent["edges"]),
                "entity_edge_pairs": len(ent_pairs),
                "entity_edge_keys": len(ent_keys),
                "operations": len(op["nodes"]),
                "operation_edges": len(op["edges"]),
                "operation_exclusions": len(op.get("operation_exclusions", [])),
                "component_context": len(op.get("component_context", [])),
                "projection_edges": len(proj["edges"]),
                "entity_only_edges": len(ent_keys - proj_keys),
                "projection_edges_not_in_entity": len(proj_keys - ent_keys),
                "resource_bindings": len(ent.get("resource_bindings", [])),
                "signals": len(ent.get("signals", [])),
                "signals_shared": sig_shared,
                "signals_with_operation": sig_op,
                "operations_runtime_name_null": runtime_null,
            },
            "entity_types": dict(Counter(n.get("type") for n in ent.get("inventory", []))),
            "entity_granularity": dict(Counter(n.get("granularity") for n in ent.get("inventory", []))),
            "edge_type_channel": dict(Counter("%s|%s" % (e.get("type"), e.get("channel")) for e in ent["edges"])),
            "record_type_channel": dict(rec_type_channel),
            "messaging_address": dict(msg),
            "signal_kinds": dict(sig_kind),
            "binding_relations": dict(Counter(b.get("relation") for b in ent.get("resource_bindings", []))),
        }
        prog.log("static", system=sysname, **{k: out[sysname]["counts"][k] for k in
                                               ["inventory", "entity_edges", "operation_edges", "projection_edges"]})
    return out


# ---------------------------------------------------------------- bước 3: đối chiếu đã lưu

def parse_tt_input(path):
    # results/T-035/do-thi/RE2-TT/<dev-id>/<thuc-the|thao-tac>/<window>.json
    parts = path.split("/")
    win = parts[-1][:-5]
    level = {"thuc-the": "entity", "thao-tac": "operation"}[parts[-2]]
    return parts[-3], level, win


def window_family(win):
    if win.startswith("s60-"):
        return "s60"
    if win.startswith("s300-"):
        return "s300"
    return win


def trace_canon(out):
    canon = {}
    status = {}
    for n in out["nodes"]["trace"]:
        oid = n["original"]["id"]
        status[oid] = n["status"]
        if n["status"] == "mapped":
            canon[oid] = n["canonical_id"]
    return canon, status


def check_view(view, vname, static_edges, trace_edges, canon, status):
    """Tính lại tập/mẫu số từ members, đối chiếu danh sách đã lưu và phân hoạch chỉ số."""
    errs = []
    S_m = [tuple_key(g["key"]) for g in view["members"]["static"]]
    T_m = [tuple_key(g["key"]) for g in view["members"]["trace"]]
    S, T = set(S_m), set(T_m)
    if len(S) != len(S_m) or len(T) != len(T_m):
        errs.append("duplicate_member_key")
    lists = {k: [tuple_key(x) for x in view[k]] for k in ["S", "T", "intersection", "static_only", "trace_only"]}
    for k, v in lists.items():
        if len(set(v)) != len(v):
            errs.append("duplicate_in_list:" + k)
    I, SO, TO = S & T, S - T, T - S
    for k, want in [("S", S), ("T", T), ("intersection", I), ("static_only", SO), ("trace_only", TO)]:
        if set(lists[k]) != want:
            errs.append("set_mismatch:" + k)
    if view["numerator"] != len(I):
        errs.append("numerator")
    if view["static_denominator"] != len(S) or view["trace_denominator"] != len(T):
        errs.append("denominator")
    sf = None if not S else len(I) / len(S)
    tf = None if not T else len(I) / len(T)
    if view["static_fraction"] != sf or view["trace_fraction"] != tf:
        errs.append("fraction")
    # phân hoạch chỉ số cạnh gốc: members + exclusions = toàn bộ, không trùng
    for side, edges, groups in [("static", static_edges, view["members"]["static"]),
                                ("trace", trace_edges, view["members"]["trace"])]:
        idx = []
        for g in groups:
            for mem in g["members"]:
                idx.append(mem["index"])
                if edges[mem["index"]] != mem["original"]:
                    errs.append("member_original_ne_edge:" + side)
        for x in view["exclusions"][side]:
            idx.append(x["index"])
            if edges[x["index"]] != x["original"]:
                errs.append("exclusion_original_ne_edge:" + side)
        if sorted(idx) != list(range(len(edges))):
            errs.append("partition:" + side)
    # khóa phía trace = ánh xạ đã khai của hai đầu; khóa phía tĩnh = đầu mút gốc
    for g in view["members"]["static"]:
        for mem in g["members"]:
            o = mem["original"]
            if g["key"][0] != o["source"] or g["key"][1] != o["target"]:
                errs.append("static_key_endpoints")
            if vname == "typed" and g["key"][2] != o["type"]:
                errs.append("static_key_type")
    for g in view["members"]["trace"]:
        for mem in g["members"]:
            o = mem["original"]
            if canon.get(o["source"]) != g["key"][0] or canon.get(o["target"]) != g["key"][1]:
                errs.append("trace_key_mapping")
    # lý do loại trừ phía trace khớp trạng thái ánh xạ của đúng đầu mút
    for x in view["exclusions"]["trace"]:
        r = x["reason"]
        if ":" in r and r.split(":")[1] in ("source", "target"):
            st, end = r.split(":")
            nid = x["original"][end]
            if status.get(nid, "unmapped") != st:
                errs.append("exclusion_reason_status")
    reasons = {"static": Counter(x["reason"] for x in view["exclusions"]["static"]),
               "trace": Counter(x["reason"] for x in view["exclusions"]["trace"])}
    return {"S": S, "T": T, "I": I, "SO": SO, "TO": TO, "reasons": reasons, "errors": sorted(set(errs))}


def stage_compare(prog, run_dir, limit=None):
    result = {}
    per_graph_rows = {}
    for sysname, srel in COMPARE_SUMMARIES.items():
        summ = load_json(srel)
        st_ent = load_json(STATIC_MODELS[sysname]["entity"])["edges"]
        st_op = load_json(STATIC_MODELS[sysname]["operation"])["edges"]
        fam = defaultdict(lambda: {"graphs": 0, "views": {}})
        rows = []
        unions = defaultdict(lambda: defaultdict(set))
        always_static_only = {}
        shapes = defaultdict(lambda: defaultdict(list))
        excl_union = defaultdict(lambda: defaultdict(set))
        errors_total = Counter()
        t_endpoints = defaultdict(set)
        unmapped_nodes = defaultdict(set)
        for i, r in enumerate(summ["rows"][:limit] if limit else summ["rows"]):
            if sysname == "TT":
                inp = r["input"]
                gid, level, win = parse_tt_input(inp)
            else:
                inp = r["path"]
                gid, level, win = r["opaque_id"], r["level"], r["window"]
            h_out, _ = sha256_file(p(r["output"]))
            h_in, _ = sha256_file(p(inp))
            out = load_json(r["output"])
            tg = load_json(inp)
            canon, status = trace_canon(out)
            for nid, stt in status.items():
                if stt != "mapped" and level == "entity":
                    unmapped_nodes[stt].add(nid)
            static_edges = st_ent if level == "entity" else st_op
            famkey = "%s:%s" % (level, window_family(win))
            row = {"graph": gid, "level": level, "window": win, "family": famkey,
                   "input": inp, "input_sha256_ok": h_in == r["input_sha256"],
                   "output": r["output"], "output_sha256_ok": h_out == r["output_sha256"],
                   "interval_ns": out.get("interval_ns"), "domain": out["context"]["domain"],
                   "revision_link_verified": out["context"]["revision_link_verified"],
                   "conditional_reference": out.get("conditional_reference"),
                   "interval_equals_input": out.get("interval_ns") == tg.get("interval_ns"),
                   "views": {}}
            for vname in ["endpoints", "typed"]:
                c = check_view(out["views"][vname], vname, static_edges, tg["edges"], canon, status)
                errors_total.update(c["errors"])
                saved = r["views"][vname]
                if "S" in saved:  # dạng tóm tắt của T-038
                    summ_ok = (saved["S"] == len(c["S"]) and saved["T"] == len(c["T"]) and
                               saved["intersection"] == len(c["I"]) and saved["static_only"] == len(c["SO"]) and
                               saved["trace_only"] == len(c["TO"]))
                else:  # dạng tóm tắt của T-039: numerator/mẫu số
                    summ_ok = (saved["numerator"] == len(c["I"]) and saved["static_denominator"] == len(c["S"]) and
                               saved["trace_denominator"] == len(c["T"]))
                if not summ_ok:
                    errors_total["source_summary_count_mismatch"] += 1
                row["views"][vname] = {"S": len(c["S"]), "T": len(c["T"]), "I": len(c["I"]),
                                       "SO": len(c["SO"]), "TO": len(c["TO"]),
                                       "trace_fraction_null": not c["T"],
                                       "errors": c["errors"],
                                       "reasons_static": dict(c["reasons"]["static"]),
                                       "reasons_trace": dict(c["reasons"]["trace"])}
                u = unions[(famkey, vname)]
                u["T"] |= c["T"]
                u["I"] |= c["I"]
                u["TO"] |= c["TO"]
                u["S"] |= c["S"]
                k = (famkey, vname)
                always_static_only[k] = c["SO"] if k not in always_static_only else (always_static_only[k] & c["SO"])
                fp = hashlib.sha256(json.dumps([sorted(map(repr, c["S"])), sorted(map(repr, c["T"]))]).encode()).hexdigest()[:16]
                shapes[k][fp].append(gid + "/" + win)
                for x in out["views"][vname]["exclusions"]["trace"]:
                    excl_union[k][x["reason"]].add((x["original"]["source"], x["original"]["target"]))
                if vname == "endpoints":
                    for key in c["T"]:
                        t_endpoints[level].add(key[0])
                        t_endpoints[level].add(key[1])
            for k in ["input_sha256_ok", "output_sha256_ok", "interval_equals_input"]:
                if not row[k]:
                    errors_total[k] += 1
            rows.append(row)
            if (i + 1) % 100 == 0:
                prog.log("compare", system=sysname, done=i + 1, total=len(summ["rows"]),
                         errors=sum(errors_total.values()))
        per_graph_rows[sysname] = rows
        # tổng hợp theo họ graph
        fams = {}
        for row in rows:
            f = fams.setdefault(row["family"], {"graphs": 0, "domain": set(), "views": {}})
            f["graphs"] += 1
            f["domain"].add(row["domain"])
            for vname, v in row["views"].items():
                fv = f["views"].setdefault(vname, {m: [] for m in ["S", "T", "I", "SO", "TO"]} | {"T_empty": 0})
                for m in ["S", "T", "I", "SO", "TO"]:
                    fv[m].append(v[m])
                fv["T_empty"] += 1 if v["trace_fraction_null"] else 0
        fam_out = {}
        for fk, f in sorted(fams.items()):
            vo = {}
            for vname, fv in f["views"].items():
                k = (fk, vname)
                vo[vname] = {
                    **{m: {"min": min(fv[m]), "max": max(fv[m])} for m in ["S", "T", "I", "SO", "TO"]},
                    "graphs_T_empty": fv["T_empty"],
                    "union_T": len(unions[k]["T"]),
                    "union_intersection": len(unions[k]["I"]),
                    "union_trace_only": len(unions[k]["TO"]),
                    "union_trace_only_keys": sorted([list(x) for x in unions[k]["TO"]], key=repr),
                    "static_only_in_every_graph": len(always_static_only[k]),
                    "distinct_ST_shapes": len(shapes[k]),
                    "shape_members": {fp: sorted(v) for fp, v in sorted(shapes[k].items())},
                    "trace_exclusion_pairs_by_reason": {rr: len(v) for rr, v in sorted(excl_union[k].items())},
                }
            fam_out[fk] = {"graphs": f["graphs"], "domain": sorted(f["domain"]), "views": vo}
        # tập ánh xạ trace (mức thực thể) được dùng cho điều kiện phụ thuộc R1 ở TT
        result[sysname] = {
            "summary_source": srel,
            "graph_count": len(rows),
            "recompute_errors": dict(errors_total),
            "families": fam_out,
            "trace_key_endpoints": {lv: sorted(v) for lv, v in t_endpoints.items()},
            "entity_trace_nodes_not_mapped": {k: sorted(v) for k, v in unmapped_nodes.items()},
            "union_full_entity_trace_only": sorted(
                [list(x) for x in unions[("entity:full", "endpoints")]["TO"]], key=repr),
            "union_full_entity_intersection_count": len(unions[("entity:full", "endpoints")]["I"]),
        }
        dump_json(rows, os.path.join(run_dir, "rows-%s.json.gz" % sysname), gz=True)
        prog.log("compare_done", system=sysname, graphs=len(rows), errors=dict(errors_total))
    return result


# ---------------------------------------------------------------- bước 3b: số mô tả trace từ T-035

def stage_t035():
    tk = load_json("results/T-035/thong-ke-do-thi.json")
    out = {"source": "results/T-035/thong-ke-do-thi.json"}
    for ds in ["RE2-TT", "Nezha-OB"]:
        d = tk["datasets"][ds]
        pick = {}
        for k in ["cases", "span_total", "full_entity_shapes", "full_operation_shapes",
                  "N_A_entity_changed", "N_A_operation_changed", "snapshot_shapes",
                  "cross_parent_contains", "cross_parent_events", "same_entity_events"]:
            if k in d and len(json.dumps(d[k])) < 2000:
                pick[k] = {"value": d[k], "pointer": "#/datasets/%s/%s" % (ds, k)}
        out[ds] = {"keys_available": sorted(d.keys()), "picked": pick}
    return out


# ---------------------------------------------------------------- bước 4: lần theo nhóm chênh lệch

TT_STATUS_CODE = "CO_DIEU_KIEN_GOI_SUA_DUNG_PHAN_BIEN_CHUA_NGHIEM_THU"
TT_STATUS_TEXT = "bản sửa R1 của người làm T-038; gói sửa đã được kiểm lại chỉ đọc và dừng phản biện (Q-171, LOG T-038 Phiên 4; không có REVIEW mới); T-038 chưa nghiệm thu; semantics/binding/lineage/runtime OPEN"

HTTP_METHOD_ONLY = {"GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"}


def owner(node_id):
    """ID thao tác là JSON cặp [entity, operation]; endpoint thành phần là ID thực thể."""
    if isinstance(node_id, str) and node_id.startswith("["):
        try:
            v = json.loads(node_id)
            if isinstance(v, list) and len(v) == 2:
                return v[0], v[1]
        except ValueError:
            pass
    return node_id, None


def full_outputs(sysname, level):
    summ = load_json(COMPARE_SUMMARIES[sysname])
    res = []
    for r in summ["rows"]:
        if sysname == "TT":
            gid, lv, win = parse_tt_input(r["input"])
            inp = r["input"]
        else:
            gid, lv, win = r["opaque_id"], r["level"], r["window"]
            inp = r["path"]
        if lv == level and win == "full":
            res.append((gid, inp, r["output"]))
    return res


def trace_op_pairs(inputs):
    """(owner nguồn, owner đích) → Counter((thao tác nguồn, thao tác đích)) trên cạnh khác owner."""
    pairs = defaultdict(Counter)
    as_target = Counter()
    cross_children = Counter()
    for _, inp, _ in inputs:
        g = load_json(inp)
        for e in g["edges"]:
            se, so = owner(e["source"])
            te, to = owner(e["target"])
            as_target[e["target"]] += e["event_count"]
            if se != te:
                pairs[(se, te)][(so, to)] += e["event_count"]
                cross_children[e["source"]] += e["event_count"]
    return pairs, as_target, cross_children


def stage_follow(prog):
    out = {}
    # ---- TT: cặp chỉ có ở trace so với cặp khớp (đối chứng có điều kiện tương ứng)
    ent = full_outputs("TT", "entity")
    ops = full_outputs("TT", "operation")
    inter, tonly = set(), set()
    for _, _, orel in ent:
        v = load_json(orel)["views"]["endpoints"]
        inter |= {tuple(k[:2]) for k in v["intersection"]}
        tonly |= {tuple(k[:2]) for k in v["trace_only"]}
    pairs, _, _ = trace_op_pairs(ops)
    canon = {}
    for _, _, orel in ops:
        o = load_json(orel)
        for n in o["nodes"]["trace"]:
            if n["status"] == "mapped":
                canon[n["original"]["id"]] = n["canonical_id"]
    st_op = load_json(STATIC_MODELS["TT"]["operation"])["edges"]
    static_callers = defaultdict(set)
    for e in st_op:
        static_callers[e["target"]].add(owner(e["source"])[0])

    def describe(pair):
        opc = pairs.get(pair, Counter())
        caller_ops = sorted({a for a, _ in opc})
        callee = sorted({b for _, b in opc})
        callee_ids = [json.dumps([pair[1], b], ensure_ascii=False, separators=(",", ":")) for b in callee]
        mapped = [canon.get(c) for c in callee_ids]
        callers = set()
        for m in mapped:
            if m:
                callers |= static_callers.get(m, set())
        kinds = set()
        for e in st_op:
            (se, so), (te, to) = owner(e["source"]), owner(e["target"])
            if se == pair[0] and te == pair[1]:
                kinds.add(("op" if so else "comp") + "->" + ("op" if to else "comp"))
        return {"pair": list(pair), "trace_op_pairs": [[a, b, n] for (a, b), n in opc.most_common()],
                "static_op_edge_kinds": sorted(kinds),
                "caller_ops_method_only": bool(caller_ops) and all(a in HTTP_METHOD_ONLY for a in caller_ops),
                "callee_ops_all_mapped": bool(mapped) and all(mapped),
                "callee_static_callers": sorted(callers),
                "caller_is_static_caller_of_callee": pair[0] in callers}

    # lý do loại trừ của cạnh trace thao tác khác owner có span phía gọi chỉ mang tên method
    xreason = Counter()
    xtotal = 0
    for _, _, orel in ops:
        v = load_json(orel)["views"]["endpoints"]
        for x in v["exclusions"]["trace"]:
            (se, so), (te, _) = owner(x["original"]["source"]), owner(x["original"]["target"])
            if se != te:
                xtotal += 1
                if so in HTTP_METHOD_ONLY:
                    xreason[x["reason"]] += 1
    rows_to = [describe(pq) for pq in sorted(tonly)]
    rows_i = [describe(pq) for pq in sorted(inter)]

    def summarize(rows):
        return {"pairs": len(rows),
                "caller_method_only": sum(r["caller_ops_method_only"] for r in rows),
                "callee_all_mapped": sum(r["callee_ops_all_mapped"] for r in rows),
                "callee_has_any_static_caller": sum(bool(r["callee_static_callers"]) for r in rows),
                "caller_is_static_caller": sum(r["caller_is_static_caller_of_callee"] for r in rows),
                "no_static_caller_but_op_to_component_edge": sum(
                    (not r["callee_static_callers"]) and ("op->comp" in r["static_op_edge_kinds"]) for r in rows),
                "no_static_caller_and_no_static_op_edge": sum(
                    (not r["callee_static_callers"]) and not r["static_op_edge_kinds"] for r in rows),
                "no_trace_op_pairs": sum(not r["trace_op_pairs"] for r in rows)}

    out["TT_trace_only_vs_intersection"] = {
        "scope": "30 graph entity/full và 30 graph operation/full RE2-TT dev; graph thao tác của T-035; mô hình thao tác tĩnh hiện hành của T-038",
        "trace_only": {"summary": summarize(rows_to), "rows": rows_to},
        "intersection_control": {"summary": summarize(rows_i), "rows": rows_i},
        "operation_cross_owner_trace_exclusions": {"total_over_30_full_graphs": xtotal,
                                                    "method_only_caller_by_reason": dict(xreason)},
        "status": TT_STATUS_CODE + ": " + TT_STATUS_TEXT}
    prog.log("follow", part="TT", trace_only=len(rows_to), control=len(rows_i))

    # ---- OB: cặp chỉ có ở phía tĩnh trong mọi graph thực thể full
    ent = full_outputs("OB", "entity")
    ops = full_outputs("OB", "operation")
    always_so = None
    trace_nodes, called_by = set(), defaultdict(set)
    for gid, inp, orel in ent:
        v = load_json(orel)["views"]["endpoints"]
        so = {tuple(k[:2]) for k in v["static_only"]}
        always_so = so if always_so is None else (always_so & so)
        g = load_json(inp)
        trace_nodes |= {n["id"] for n in g["nodes"]}
        for e in g["edges"]:
            if e["source"] != e["target"]:
                called_by[e["target"]].add(e["source"])
    canon_inv = defaultdict(set)
    for _, _, orel in ops:
        o = load_json(orel)
        for n in o["nodes"]["trace"]:
            if n["status"] == "mapped":
                canon_inv[n["canonical_id"]].add(n["original"]["id"])
    op_pairs, as_target, cross_children = trace_op_pairs(ops)
    trace_ops_by_entity = defaultdict(set)
    for _, inp, _ in ops:
        for n in load_json(inp)["nodes"]:
            trace_ops_by_entity[n["entity"]].add(n["id"])
    st_op = load_json(STATIC_MODELS["OB"]["operation"])["edges"]
    rows = []
    for pair in sorted(always_so):
        src, tgt = pair
        st_edges = [e for e in st_op if owner(e["source"])[0] == src and owner(e["target"])[0] == tgt]
        src_ops = sorted({e["source"] for e in st_edges if owner(e["source"])[1] is not None})
        follow = []
        for so_id in src_ops:
            present = so_id in trace_ops_by_entity.get(src, set()) or bool(canon_inv.get(so_id))
            follow.append({"static_source_op": so_id,
                           "present_in_trace_ops_literal_or_mapped": present,
                           "mapped_trace_ops": sorted(canon_inv.get(so_id, [])),
                           "events_as_child": sum(as_target.get(t, 0) for t in canon_inv.get(so_id, [])),
                           "cross_entity_child_events": sum(cross_children.get(t, 0) for t in canon_inv.get(so_id, []))})
        # các lời gọi đi ra khác thực thể mà nguồn có quan sát trong trace (đối chứng cùng nguồn)
        other_out = sorted({(te, so) for (se, te), c in op_pairs.items() if se == src for (so, _) in c})
        rows.append({"pair": [src, tgt],
                     "target_in_trace_nodes": tgt in trace_nodes,
                     "target_called_by_in_trace": sorted(called_by.get(tgt, [])),
                     "source_in_trace_nodes": src in trace_nodes,
                     "static_op_edges": len(st_edges),
                     "static_source_ops": follow,
                     "source_other_cross_entity_calls_in_trace": [list(x) for x in other_out]})
    cls = Counter()
    for r in rows:
        if not r["target_in_trace_nodes"]:
            cls["target_not_observed"] += 1
        elif r["source_in_trace_nodes"]:
            cls["both_observed_no_edge"] += 1
        else:
            cls["source_not_observed"] += 1
    # ma trận hai đầu (không ưu tiên đích) để đọc cùng cách với TT; classification trên giữ ưu tiên đích như run 007
    m2 = Counter(("src_obs" if r["source_in_trace_nodes"] else "src_not") + "|" +
                 ("tgt_obs" if r["target_in_trace_nodes"] else "tgt_not") for r in rows)
    out["OB_static_only_every_full_graph"] = {
        "scope": "22 graph entity/full và 22 graph operation/full Nezha-OB dev-adapter; T-039 đã đóng (Q-165)",
        "classification": dict(cls),
        "classification_note": "ưu tiên đích: target_not_observed gồm cả cặp có hai đầu không xuất hiện",
        "endpoint_matrix": dict(sorted(m2.items())), "rows": rows}
    prog.log("follow", part="OB", pairs=len(rows), classes=dict(cls))
    out["TT_static_only_every_full_graph"] = follow_tt_static_only(prog)
    return out


def follow_tt_static_only(prog):
    """N2: khóa tĩnh TT vắng ở mọi graph entity/full; phân loại theo nút trace đã ánh xạ và lần theo nhóm hai đầu cùng quan sát.

    Chỉ dùng graph/đối chiếu đã lưu và mô hình tĩnh hiện hành. Đồng xuất hiện trong cùng graph gộp
    không chứng minh các lời gọi thuộc cùng một request.
    """
    summ = load_json(COMPARE_SUMMARIES["TT"])
    always_so, nodes_full, trace_full = None, {}, {}
    excl_full = {}
    present_by_graph = defaultdict(list)  # gid -> [(window, set nút đã ánh xạ)] mức thực thể
    for r in summ["rows"]:
        gid, lv, win = parse_tt_input(r["input"])
        if lv != "entity":
            continue
        o = load_json(r["output"])
        tn = {n["canonical_id"] for n in o["nodes"]["trace"] if n["status"] == "mapped"}
        present_by_graph[gid].append((win, tn))
        if win == "full":
            v = o["views"]["endpoints"]
            so = {tuple(k[:2]) for k in v["static_only"]}
            always_so = so if always_so is None else (always_so & so)
            nodes_full[gid] = tn
            trace_full[gid] = {tuple(k[:2]) for k in v["T"]}
            excl_full[gid] = [(x["original"]["source"], x["original"]["target"], x["reason"])
                              for x in v["exclusions"]["trace"]]
    union_nodes = set().union(*nodes_full.values())
    m2 = Counter()
    both = []
    for a, b in sorted(always_so):
        c = ("src_obs" if a in union_nodes else "src_not") + "|" + ("tgt_obs" if b in union_nodes else "tgt_not")
        m2[c] += 1
        if c == "src_obs|tgt_obs":
            both.append((a, b))
    # mapping thao tác: candidate của các span trace chưa xác minh (graph operation/full)
    cand = defaultdict(Counter)
    for r in summ["rows"]:
        gid, lv, win = parse_tt_input(r["input"])
        if lv != "operation" or win != "full":
            continue
        for mp in load_json(r["output"])["mappings"]:
            cs = mp.get("candidates") or []
            for c in cs:
                cand[c]["verified" if mp.get("verified") else "unverified_candidates_%d" % len(cs)] += 1
    st_op = load_json(STATIC_MODELS["TT"]["operation"])["edges"]
    rows = []
    for a, b in both:
        cases_co = sorted(g for g, tn in nodes_full.items() if a in tn and b in tn)
        per_case = [sum(1 for _, tn in present_by_graph[g] if a in tn and b in tn) for g in cases_co]
        graphs_per_case = [len(present_by_graph[g]) for g in cases_co]
        caller_callees = sorted({t for g in cases_co for s_, t in trace_full[g] if s_ == a})
        callee_callers = sorted({s_ for g in cases_co for s_, t in trace_full[g] if t == b})
        # đường qua nút trace chưa ánh xạ trong cùng graph full: a→X bị loại vì đích chưa ánh xạ và X→b bị loại vì nguồn chưa ánh xạ
        via = Counter()
        for g in cases_co:
            ex = excl_full[g]
            outs = {t for s_, t, rs in ex if s_ == a and rs == "unmapped:target"}
            ins = {s_ for s_, t, rs in ex if t == b and rs == "unmapped:source"}
            for x in sorted(outs & ins):
                via[x] += 1
        st = []
        for e in st_op:
            (se, so_), (te, to_) = owner(e["source"]), owner(e["target"])
            if se == a and te == b:
                pv = (e.get("provenance") or [{}])[0]
                st.append({"source_op": so_, "target": to_ if to_ else te, "type": e.get("type"),
                           "provenance_source": pv.get("source_id"), "provenance_locator": pv.get("locator"),
                           "provenance_condition": pv.get("condition"),
                           "trace_mapping_candidate_counts": dict(cand.get(e["source"], {}))})
        rows.append({"pair": [a, b], "cases_both_endpoints_full": len(cases_co),
                     "entity_graphs_both_present_per_case": [min(per_case), max(per_case)] if per_case else None,
                     "entity_graphs_per_case": [min(graphs_per_case), max(graphs_per_case)] if graphs_per_case else None,
                     "caller_observed_callees_in_same_cases": caller_callees,
                     "callee_observed_callers_in_same_cases": callee_callers,
                     "same_graph_paths_via_unmapped_trace_node": dict(via),
                     "static_op_edges": st,
                     "source_op_is_unverified_trace_candidate": any(
                         any(k.startswith("unverified") for k in x["trace_mapping_candidate_counts"]) for x in st)})
    res = {"scope": "30 graph entity/full (phân loại), mọi graph entity RE2-TT dev (đếm đồng xuất hiện), 30 graph operation/full (mapping); mô hình thao tác tĩnh hiện hành T-038",
           "status": TT_STATUS_CODE + ": " + TT_STATUS_TEXT,
           "static_only_every_full_graph": len(always_so),
           "endpoint_matrix": dict(sorted(m2.items())),
           "endpoint_nodes": "hợp nút trace đã ánh xạ qua 30 graph entity/full",
           "both_observed_pairs": len(rows),
           "both_observed_source_op_unverified_candidate": sum(r["source_op_is_unverified_trace_candidate"] for r in rows),
           "both_observed_with_same_graph_path_via_unmapped": sum(bool(r["same_graph_paths_via_unmapped_trace_node"]) for r in rows),
           "note": "Đồng xuất hiện trong cùng graph gộp không chứng minh cùng request; candidate chưa xác minh không phải span đã mất.",
           "rows": rows}
    prog.log("follow", part="TT_static_only", pairs=len(always_so), matrix=dict(m2), both=len(rows))
    return res


# ---------------------------------------------------------------- bước 5: xuất bản

class Taker:
    """Chép số từ raw sang bản xuất bản và ghi lại cặp con trỏ để kiem_tra.py so lại."""

    def __init__(self, raw):
        self.raw = raw
        self.pairs = []

    def __call__(self, dst_ptr, raw_ptr):
        cur = self.raw
        for part in raw_ptr.strip("/").split("/"):
            cur = cur[int(part)] if isinstance(cur, list) else cur[part]
        self.pairs.append({"tong_hop": dst_ptr, "raw": raw_ptr})
        return cur


def esc(k):
    return k.replace("~", "~0").replace("/", "~1")


def stage_publish(run, inputs, raw):
    take = Taker(raw)
    rp = "results/T-040/runs/%s/tong-hop-raw.json" % run
    he = {}
    for sysname in ["FT", "TT", "OB"]:
        base = "/he_thong/%s/mo_hinh_tinh/so_dem" % sysname
        counts = {k: take("%s/%s" % (base, k), "/static_models/%s/counts/%s" % (sysname, k))
                  for k in raw["static_models"][sysname]["counts"]}
        he[sysname] = {"mo_hinh_tinh": {
            "nguon": rp + "#/static_models/" + sysname,
            "tep": raw["static_models"][sysname]["files"],
            "so_dem": counts,
            "kieu_canh_kenh": take("/he_thong/%s/mo_hinh_tinh/kieu_canh_kenh" % sysname,
                                   "/static_models/%s/edge_type_channel" % sysname),
            "dia_chi_messaging": take("/he_thong/%s/mo_hinh_tinh/dia_chi_messaging" % sysname,
                                      "/static_models/%s/messaging_address" % sysname),
            "loai_tin_hieu": take("/he_thong/%s/mo_hinh_tinh/loai_tin_hieu" % sysname,
                                  "/static_models/%s/signal_kinds" % sysname),
            "kieu_thuc_the": take("/he_thong/%s/mo_hinh_tinh/kieu_thuc_the" % sysname,
                                  "/static_models/%s/entity_types" % sysname),
            "binding": take("/he_thong/%s/mo_hinh_tinh/binding" % sysname,
                            "/static_models/%s/binding_relations" % sysname),
            "evidence": raw["static_models"][sysname]["evidence"],
        }}
    he["FT"]["mo_hinh_tinh"]["trang_thai"] = "CHINH_THUC: T-037 đóng theo Q-167; mô hình thiết kế đích, runtime chưa kiểm"
    he["OB"]["mo_hinh_tinh"]["trang_thai"] = "CHINH_THUC_CO_DIEU_KIEN: T-039 đóng theo Q-165; revision ứng dụng→dataset chưa xác minh"
    he["TT"]["mo_hinh_tinh"]["trang_thai"] = TT_STATUS_CODE + ": " + TT_STATUS_TEXT
    he["FT"]["doi_chieu"] = {"trang_thai": "KHONG_AP_DUNG: chưa có trace FlashTicket được cung cấp; đối chiếu runtime thuộc P9b/SPEC sau"}
    for sysname in ["TT", "OB"]:
        fams = raw["comparisons"][sysname]["families"]
        fam_pub = {}
        for fk, f in fams.items():
            fp = {}
            for vn, v in f["views"].items():
                b = "/comparisons/%s/families/%s/views/%s" % (sysname, esc(fk), vn)
                d = "/he_thong/%s/doi_chieu/ho_graph/%s/views/%s" % (sysname, esc(fk), vn)
                fp[vn] = {m: take("%s/%s" % (d, m), "%s/%s" % (b, m)) for m in
                          ["S", "T", "I", "SO", "TO", "graphs_T_empty", "union_T", "union_intersection",
                           "union_trace_only", "static_only_in_every_graph", "distinct_ST_shapes",
                           "trace_exclusion_pairs_by_reason"]}
            fam_pub[fk] = {"graphs": take("/he_thong/%s/doi_chieu/ho_graph/%s/graphs" % (sysname, esc(fk)),
                                          "/comparisons/%s/families/%s/graphs" % (sysname, esc(fk))),
                           "domain": f["domain"], "views": fp}
        he[sysname]["doi_chieu"] = {
            "nguon": rp + "#/comparisons/" + sysname,
            "tung_graph": "results/T-040/runs/%s/rows-%s.json.gz" % (run, sysname),
            "so_graph": take("/he_thong/%s/doi_chieu/so_graph" % sysname, "/comparisons/%s/graph_count" % sysname),
            "loi_tinh_lai": take("/he_thong/%s/doi_chieu/loi_tinh_lai" % sysname,
                                 "/comparisons/%s/recompute_errors" % sysname),
            "ho_graph": fam_pub,
            "dau_mut_khoa_T": take("/he_thong/%s/doi_chieu/dau_mut_khoa_T" % sysname,
                                   "/comparisons/%s/trace_key_endpoints" % sysname),
            "nut_trace_chua_anh_xa_muc_thuc_the": take("/he_thong/%s/doi_chieu/nut_trace_chua_anh_xa_muc_thuc_the" % sysname,
                                                       "/comparisons/%s/entity_trace_nodes_not_mapped" % sysname),
            "hop_full_trace_only": take("/he_thong/%s/doi_chieu/hop_full_trace_only" % sysname,
                                        "/comparisons/%s/union_full_entity_trace_only" % sysname),
        }
    # Ranh giới phụ thuộc R1 của TT: S-side chặn, giao/trace_only có điều kiện, T-side không phụ thuộc S.
    ST = TT_STATUS_CODE
    he["TT"]["doi_chieu"]["phu_thuoc_S"] = {
        "S": {"trang_thai": ST},
        "static_only": {"trang_thai": ST},
        "static_fraction": {"trang_thai": ST},
        "static_only_in_every_graph": {"trang_thai": ST},
        "entity_only_va_canh_thuc_the": {"trang_thai": ST},
    }
    he["TT"]["doi_chieu"]["nguon_ban_sua"] = "results/T-038/runs/sua-r1-20261017-001/ban-giao-T040.json"
    he["TT"]["doi_chieu"]["khong_phu_thuoc_S"] = [
        "T, dau_mut_khoa_T, lý do loại trừ phía trace, T typed rỗng, T thao tác rỗng (tập trace sau ánh xạ, không dùng quan hệ tĩnh)"]
    pub = {
        "schema": "T040-tong-hop-v1",
        "run": "runs/" + run,
        "nguon_tinh_toan": "results/T-040/tong_hop.py; số thô " + rp,
        "luu_y": [
            "Không cộng hoặc lấy trung bình tỷ lệ giữa ba hệ: miền, nguồn và trạng thái chấp nhận khác nhau.",
            "Khớp đầu mút không xác nhận kiểu, transport, phiên bản hay runtime; typed bỏ unknown.",
            "Mẫu số tính trên phần đủ điều kiện sau ánh xạ; không là độ phủ runtime.",
            "Số TT lấy từ bản sửa R1 của người làm T-038 (gói sửa đã dừng phản biện theo Q-171; T-038 chưa nghiệm thu); không lấy số từ run đề nghị sửa của reviewer.",
        ],
        "hop_dong_chung": {
            "pin": inputs["pins"],
            "ma_chung_hien_hanh": inputs["live_code"],
            "schema_version": {s: raw["static_models"][s]["schema_version"] for s in ["FT", "TT", "OB"]},
        },
        "he_thong": he,
        "lan_theo": raw["follow"],
        "nguon_trace_T035": raw["t035"],
        "_trich_tu_raw": take.pairs,
    }
    return pub


SOURCE_STATUS = [
    # task, trạng thái chấp nhận, nguồn trạng thái, cách T-040 dùng
    ("T-034", "G2 đã duyệt (Q-149); task chờ Minh nghiệm thu", "docs/DECISIONS.md Q-149; docs/STATE.md dòng T-034",
     "Bản đồ hạn chế và ứng viên UV-1..UV-9 của goi-g2.md theo trạng thái đã duyệt cổng; không coi là lựa chọn P6"),
    ("T-035", "Chưa nghiệm thu; chờ phiên Codex sạch tự soát rồi phản biện chính thức", "results/T-035/manifest.json#/task_state",
     "Graph trace dev và thống kê mô tả; mọi đối chiếu TT/OB phụ thuộc trạng thái này"),
    ("T-036", "Gốc đã đóng (Q-158); gói SMTP V2 (Q-164) đã triển khai, chưa có phản biện chính thức", "docs/DECISIONS.md Q-158, Q-164; results/T-036/runs/doi-chieu-smtp-001/ban-giao.md",
     "Hợp đồng và pin chung V2 cho cả ba nhánh"),
    ("T-037", "Đã nghiệm thu và đóng (Q-167); manifest giữ trạng thái trước nghiệm thu", "docs/DECISIONS.md Q-167; tasks/T-037-p5b-flashticket/REVIEW.md",
     "Mô hình thiết kế FlashTicket chính thức trong phạm vi nguồn ghim; runtime chưa kiểm"),
    ("T-038", "Chưa nghiệm thu toàn task; người làm đã đáp REVIEW R1 và tiếp nhận bản sửa; gói sửa đã được kiểm lại chỉ đọc và dừng phản biện (Q-171; không có REVIEW mới); semantics/binding/lineage/runtime OPEN",
     "docs/DECISIONS.md Q-171; tasks/T-038-p5b-trainticket/LOG.md Phiên 4; REVIEW.md (bảng phản hồi); results/T-038/runs/sua-r1-20261017-001/ban-giao-T040.json; manifest T-038 là ảnh chụp trước Q-171",
     "Dùng bản sửa của người làm cho cả phía tĩnh và phía trace, gắn nhãn có điều kiện (T-038 chưa nghiệm thu); không dùng run reviewer-r1-fix làm số"),
    ("T-039", "Đã nghiệm thu và đóng (Q-165) với giới hạn lịch sử và phần nguồn OPEN", "docs/DECISIONS.md Q-165; tasks/T-039-p5b-online-boutique/REVIEW.md",
     "Mô hình tham chiếu và đối chiếu 132 graph chính thức có điều kiện revision"),
]


def tt_root_projection_check():
    """Thư mục do-thi/ gốc của T-038 trộn bản V2 (thuc-the, thao-tac) với phép chiếu cũ; T-040 dùng bản trong run hiện hành."""
    root_proj = load_json("results/T-038/do-thi/chieu-thao-tac.json")
    cur_proj = load_json(STATIC_MODELS["TT"]["projection"])
    root_ent_sha = sha256_file(p("results/T-038/do-thi/thuc-the.json"))[0]
    cur_ent_sha = sha256_file(p(STATIC_MODELS["TT"]["entity"]))[0]
    rk = {edge_key_entity(e) for e in root_proj["edges"]}
    ck = {edge_key_entity(e) for e in cur_proj["edges"]}
    return {"root_projection": "results/T-038/do-thi/chieu-thao-tac.json", "root_projection_edges": len(root_proj["edges"]),
            "current_projection": STATIC_MODELS["TT"]["projection"], "current_projection_edges": len(cur_proj["edges"]),
            "current_minus_root": [list(map(str, k[:4])) for k in sorted(ck - rk, key=repr)],
            "root_minus_current": [list(map(str, k[:4])) for k in sorted(rk - ck, key=repr)],
            "root_entity_graph_equals_current": root_ent_sha == cur_ent_sha}


def tt_root_vs_model_check():
    """Graph gốc do-thi/ của T-038 phải cùng byte với model của run sửa R1."""
    R = "results/T-038/runs/sua-r1-20261017-001/model/"
    out = {}
    for name in ["thuc-the.json", "thao-tac.json", "chieu-thao-tac.json", "chi-thuc-the.json"]:
        out[name] = sha256_file(p("results/T-038/do-thi/" + name))[0] == sha256_file(p(R + name))[0]
    out["all_equal"] = all(out.values())
    return out


def build_dau_vao(run, inputs):
    acc = inputs["acceptance"]
    checks = {
        "Q149_present": acc["decisions"]["Q-149"]["present"],
        "Q158_present": acc["decisions"]["Q-158"]["present"],
        "Q164_present": acc["decisions"]["Q-164"]["present"],
        "Q165_present": acc["decisions"]["Q-165"]["present"],
        "Q167_present": acc["decisions"]["Q-167"]["present"],
        "T038_R1_answered_by_producer": acc["T038_review"]["R1_marked_blocking"] and not acc["T038_review"]["R1_response_empty"],
        "Q171_present": acc["decisions"]["Q-171"]["present"],
        # manifest T-038 là ảnh chụp trước Q-171; trạng thái hiện hành lấy từ DECISIONS/LOG T-038
        "T038_manifest_state_snapshot_CHO_KIEM_BAN_SUA": load_json("results/T-038/manifest.json").get("state") == "CHO_KIEM_BAN_SUA",
        # R3: chỉ kiểm nguồn quyết định không đổi so với snapshot đã đọc; không suy nghiệm thu từ nội dung
        "T038_decision_lines_match_read_snapshot": acc["T038_decision_snapshot"]["unchanged"],
        "T035_no_review_file": not acc["review_files"]["T-035-p5-do-thi-tu-trace"],
    }
    # R5: mọi kiểm hash/phiên bản của đầu vào thực sự được đọc phải nằm trong điều kiện đạt.
    # Tệp ngoài manifest không phải đầu vào được đọc: chỉ báo cáo ở tep_ngoai_manifest.
    tt_root = tt_root_vs_model_check()
    checks["B16_equals_T037_registry"] = bool(inputs["flashticket"].get("B16_equals_T037_registry"))
    for br, pin in sorted(inputs["pins"].items()):
        for k in ("manifest_sha256_equals_file", "created_utc_equals", "code_hashes_equal_V2"):
            checks["pin_%s_%s" % (br, k)] = bool(pin.get(k))
    for rel, v in sorted(inputs["live_code"].items()):
        checks["live_code_equals_V2_pin:" + rel] = bool(v.get("equals_V2_pin"))
    checks["TT_root_equals_fix_model"] = bool(tt_root.get("all_equal"))
    man = []
    for m in inputs["manifests"]:
        man.append({k: m[k] for k in ["id", "manifest", "manifest_sha256", "created_utc", "state_in_manifest",
                                       "task_accepted_in_manifest", "files", "ok", "bytes_checked"]} |
                   {"mismatch": [x["path"] for x in m["mismatch"]], "missing": m["missing"],
                    "mismatch_expected_by_V2": m.get("mismatch_expected_by_V2")})
    return {
        "schema": "T040-dau-vao-v1", "run": "runs/" + run,
        "chi_tiet": "results/T-040/runs/%s/dau-vao-kiem.json" % run,
        "nguyen_tac": "Trạng thái chấp nhận lấy từ DECISIONS/REVIEW/LOG; manifest chỉ để kiểm hash; không coi tệp mới nhất là bản chính thức.",
        "trang_thai_nguon": [{"task": t, "trang_thai": st, "nguon_trang_thai": src, "cach_dung_trong_T040": use}
                             for t, st, src, use in SOURCE_STATUS],
        "kiem_trang_thai": checks,
        "doi_chieu_quyet_dinh_T038": acc["T038_decision_snapshot"],
        "manifest_khop_toan_bo": sum(1 for m in man if not m["mismatch"] and not m["missing"]),
        "manifest": man,
        "pin_chung": inputs["pins"],
        "ma_chung_hien_hanh": inputs["live_code"],
        "flashticket": inputs["flashticket"],
        "tep_ngoai_manifest": inputs["extra_files_not_in_manifests"],
        "ban_hien_hanh_dung": {
            "FT_mo_hinh": STATIC_MODELS["FT"], "TT_mo_hinh": STATIC_MODELS["TT"], "OB_mo_hinh": STATIC_MODELS["OB"],
            "TT_doi_chieu": COMPARE_SUMMARIES["TT"], "OB_doi_chieu": COMPARE_SUMMARIES["OB"],
            "T035_graph": "results/T-035/do-thi/ (đường dẫn từng graph ở rows của task nguồn)",
        },
        "tep_goc_TT_dong_bo_model_sua": tt_root,
        "khong_dung": [
            "results/T-038/runs/reviewer-r1-fix-20261016-001/ (bản đề nghị sửa chưa tiếp nhận)",
            "results/T-038/runs/doi-chieu-smtp-001/ (bản SMTP V2 trước sửa R1; chỉ còn là lịch sử)",
            "các bảng số R1 lịch sử trong phan-tich-chenh-lech.md của T-038 và các manifest trước V2",
        ],
        "all_checks_pass": all(checks.values()) and all(not m["mismatch"] or m.get("mismatch_expected_by_V2") == m["mismatch"]
                                                       for m in man) and all(not m["missing"] for m in man),
    }


# ---------------------------------------------------------------- chính

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--limit", type=int, default=None, help="pilot: chỉ xử lý N graph đầu mỗi hệ")
    ap.add_argument("--skip-inputs", action="store_true", help="pilot: bỏ băm manifest")
    ap.add_argument("--decision-snapshot", required=True,
                    help="snapshot các dòng DECISIONS nhắc T-038 mà người làm đã đọc (runs/<run>/doc-quyet-dinh.json)")
    args = ap.parse_args()
    run_dir = os.path.join(OUT, "runs", args.run)
    if os.path.exists(os.path.join(run_dir, "cost.json")):
        sys.exit("run đã tồn tại; dùng tên run mới để giữ mọi lượt")
    os.makedirs(run_dir, exist_ok=True)
    prog = Progress(os.path.join(run_dir, "progress.jsonl"))
    t0 = time.time()
    prog.log("start", python=sys.version.split()[0], root=ROOT)
    timings = {}
    if args.skip_inputs:
        inputs = {"manifests": [], "skipped": True}
    else:
        s = time.time(); inputs = stage_inputs(prog, args.decision_snapshot); timings["inputs_s"] = round(time.time() - s, 2)
    dump_json(inputs, os.path.join(run_dir, "dau-vao-kiem.json"))

    def stop(reason, **kw):
        """R4 / SPEC bước 1: dừng phần phụ thuộc, giữ bằng chứng trong run, không ghi bản hiện hành."""
        cost = {"wall_s": round(time.time() - t0, 2), **timings, "peak_working_set_bytes": peak_rss_bytes(),
                "bytes_hashed_manifests": sum(m["bytes_checked"] for m in inputs["manifests"]),
                "stopped": reason, "published_current": False}
        dump_json(cost, os.path.join(run_dir, "cost.json"))
        prog.log("stop", reason=reason, published_current=False, **kw)
        sys.exit(2)

    dv = None
    if not args.skip_inputs:
        # cổng 1: kiểm đầu vào phải đạt trước mọi bước phụ thuộc
        dv = build_dau_vao(args.run, inputs)
        dump_json(dv, os.path.join(run_dir, "dau-vao.json"))
        if not dv["all_checks_pass"]:
            stop("kiem_dau_vao_khong_dat",
                 failed=[k for k, v in dv["kiem_trang_thai"].items() if not v],
                 decision_snapshot=dv["doi_chieu_quyet_dinh_T038"])
    s = time.time(); static = stage_static(prog); timings["static_s"] = round(time.time() - s, 2)
    s = time.time(); comp = stage_compare(prog, run_dir, args.limit); timings["compare_s"] = round(time.time() - s, 2)
    # cổng 2: có lỗi tính lại thì giữ chẩn đoán trong run và dừng, không xuất bản
    recompute_errors = {k: sum((v.get("recompute_errors") or {}).values()) for k, v in comp.items() if isinstance(v, dict)}
    if any(recompute_errors.values()):
        dump_json({"schema": "T040-tong-hop-raw-v1", "run": "runs/" + args.run, "partial": "dừng sau đối chiếu",
                   "static_models": static, "comparisons": comp}, os.path.join(run_dir, "tong-hop-raw.json"))
        stop("loi_tinh_lai", recompute_errors=recompute_errors)
    t035 = stage_t035()
    s = time.time(); follow = stage_follow(prog); timings["follow_s"] = round(time.time() - s, 2)
    raw = {"schema": "T040-tong-hop-raw-v1", "run": "runs/" + args.run, "limit": args.limit,
           "inputs_skipped": bool(args.skip_inputs),
           "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "static_models": static, "comparisons": comp, "t035": t035, "follow": follow}
    dump_json(raw, os.path.join(run_dir, "tong-hop-raw.json"))
    if not args.limit and not args.skip_inputs:
        pub = stage_publish(args.run, inputs, raw)
        dump_json(pub, os.path.join(run_dir, "tong-hop.json"))
        # chỉ tới đây khi cả hai cổng đạt
        dump_json(pub, os.path.join(OUT, "tong-hop.json"))
        dump_json(dv, os.path.join(OUT, "dau-vao.json"))
        prog.log("publish", file="results/T-040/dau-vao.json", all_checks_pass=dv["all_checks_pass"])
        prog.log("publish", file="results/T-040/tong-hop.json", copied_pointers=len(pub["_trich_tu_raw"]))
    cost = {"wall_s": round(time.time() - t0, 2), **timings, "peak_working_set_bytes": peak_rss_bytes(),
            "bytes_hashed_manifests": sum(m["bytes_checked"] for m in inputs["manifests"]),
            "note": "Đo trên laptop, không chạy việc nặng khác do task này khởi động; không phải benchmark cô lập."}
    dump_json(cost, os.path.join(run_dir, "cost.json"))
    prog.log("end", **cost)


if __name__ == "__main__":
    main()
