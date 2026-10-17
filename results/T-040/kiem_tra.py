"""T-040 — kiểm kết quả đã lưu.

Kiểm bằng đường tính khác `tong_hop.py`:
  K1  phép thử giả cho hàm tính lại (đột biến phải bị bắt; bản gốc không lỗi);
  K2  tính lại kích thước tập từ danh sách S/T đã lưu (không qua members) cho mọi graph,
      so với rows của T-040 và với tóm tắt của task nguồn;
  K3  tong-hop.json khớp tong-hop-raw.json ở mọi số được trích;
  K4  sổ số liệu: mỗi số trong báo cáo .md có đoạn chữ tồn tại và con trỏ JSON trả đúng giá trị;
  K5  chặn bản dự kiến: không số nào lấy từ run đề nghị sửa của reviewer T-038; trường phụ thuộc S của TT
      mang trạng thái chặn;
  K6  phạm vi ghi: STATE chỉ đổi dòng T-040, LOG chỉ nối thêm, tệp được bảo vệ không đổi, git status
      không có thay đổi mới ngoài phạm vi.

Lệnh: py -3 -X utf8 -B results/T-040/kiem_tra.py --run tong-hop-001 --baseline-dir <thư mục ảnh chụp trước>
"""
import argparse
import copy
import gzip
import hashlib
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import tong_hop as th  # noqa: E402

SPEC_SHA = "f3e586de46789f47e0ed147fca520f205cd2c9d79e64094bb2adec02af267dc4"
LOG_OPEN_SHA = "dd04e745a9f17a2cd606e7748cc9a776487e033acd8bc26b3d80ff0a12ae940d"
STATE_OPEN_SHA = "e48a6735a0d571c6fb52e494f6dcf41c57026a355e8d289c0a1c9ecb483b3aa5"
STATE_OPEN_ROW = ("| T-040 | P5b: tổng hợp và bàn giao P6/P9 | P5 (G3) | Claude | Codex | Đã duyệt tạo SPEC 17/10/2026 "
                  "(Q-168); chờ soát SPEC, chưa duyệt triển khai. Prompt tại LOG Phiên 1; giữ phụ thuộc nguồn "
                  "trong SPEC. Chưa commit/push. | `tasks/T-040-p5b-tong-hop/` |")
LOG_P2_MARK = "\n---\n\n## Phiên 2 — 17/10/2026 — Claude"
ALLOWED_PREFIX = ("results/T-040/",)
ALLOWED_FILES = ("docs/STATE.md", "tasks/T-040-p5b-tong-hop/LOG.md", "tasks/T-040-p5b-tong-hop/REVIEW.md")


def P(rel):
    return os.path.join(ROOT, rel.replace("/", os.sep))


def load(rel):
    return th.load_json(rel)


def resolve(obj, pointer):
    cur = obj
    for part in pointer.lstrip("/").split("/") if pointer not in ("", "/") else []:
        part = part.replace("~1", "/").replace("~0", "~")
        if isinstance(cur, list):
            cur = cur[int(part)]
        else:
            cur = cur[part]
    return cur


# ---------------------------------------------------------------- K1

def k1_mutation():
    res = {"cases": []}
    samples = [
        ("TT-entity", "results/T-038/runs/sua-r1-20261017-001/checks/full1069-002/doi-chieu/dev-03d4910932/thuc-the/full.json.gz",
         "results/T-035/do-thi/RE2-TT/dev-03d4910932/thuc-the/full.json", th.STATIC_MODELS["TT"]["entity"]),
        ("OB-operation", "results/T-039/runs/doi-chieu-smtp-001/checks/full132-001/doi-chieu/dev-14701a3bbb/operation/full.json",
         "results/T-035/do-thi/Nezha-OB/dev-14701a3bbb/thao-tac/full.json", th.STATIC_MODELS["OB"]["operation"]),
    ]

    def run(out, tg, st):
        canon, status = th.trace_canon(out)
        return th.check_view(out["views"]["endpoints"], "endpoints", st, tg["edges"], canon, status)["errors"]

    for name, orel, irel, srel in samples:
        out0 = load(orel)
        tg = load(irel)
        st = load(srel)["edges"]
        base = run(out0, tg, st)
        res["cases"].append({"sample": name, "mutation": "none", "errors": base, "expect_errors": False,
                             "pass": base == []})
        muts = []

        def m_drop_S(o):
            o["views"]["endpoints"]["S"].pop()
        muts.append(("drop_one_S_list_item", m_drop_S))

        def m_add_I(o):
            v = o["views"]["endpoints"]
            v["intersection"].append(v["static_only"][0])
        muts.append(("add_static_only_key_to_intersection", m_add_I))

        def m_num(o):
            o["views"]["endpoints"]["numerator"] += 1
        muts.append(("numerator_plus_one", m_num))

        def m_frac(o):
            v = o["views"]["endpoints"]
            v["trace_fraction"] = 0.0 if v["trace_fraction"] is None else v["trace_fraction"] / 2 + 0.01
        muts.append(("trace_fraction_changed", m_frac))

        def m_index(o):
            g = o["views"]["endpoints"]["members"]["trace"][0]["members"][0]
            g["index"] = (g["index"] + 1) % len(tg["edges"])
        muts.append(("trace_member_index_shift", m_index))

        def m_map(o):
            for n in o["nodes"]["trace"]:
                if n["status"] == "mapped":
                    n["canonical_id"] = n["canonical_id"] + "#gia"
                    break
        muts.append(("trace_mapping_canonical_changed", m_map))

        def m_excl(o):
            o["views"]["endpoints"]["exclusions"]["static"].append(
                copy.deepcopy(o["views"]["endpoints"]["members"]["static"][0]["members"][0]) | {"reason": "gia"})
        muts.append(("duplicate_static_index_in_exclusions", m_excl))

        for mname, fn in muts:
            o = copy.deepcopy(out0)
            fn(o)
            errs = run(o, tg, st)
            res["cases"].append({"sample": name, "mutation": mname, "errors": errs, "expect_errors": True,
                                 "pass": bool(errs)})
    res["pass"] = all(c["pass"] for c in res["cases"])
    return res


# ---------------------------------------------------------------- K2

def k2_lists(run):
    out = {"systems": {}}
    allpass = True
    for sysname, srel in th.COMPARE_SUMMARIES.items():
        rows = json.load(gzip.open(P("results/T-040/runs/%s/rows-%s.json.gz" % (run, sysname)), "rt", encoding="utf-8"))
        by_out = {r["output"]: r for r in rows}
        summ = load(srel)
        bad = []
        n = 0
        for sr in summ["rows"]:
            o = load(sr["output"])
            r = by_out.get(sr["output"])
            if r is None:
                bad.append({"output": sr["output"], "why": "missing_row"})
                continue
            for vname in ["endpoints", "typed"]:
                v = o["views"][vname]
                S = {json.dumps(k) for k in v["S"]}
                T = {json.dumps(k) for k in v["T"]}
                I = {json.dumps(k) for k in v["intersection"]}
                SO = {json.dumps(k) for k in v["static_only"]}
                TO = {json.dumps(k) for k in v["trace_only"]}
                algebra = (I == S & T and SO == S - T and TO == T - S)
                sizes = {"S": len(S), "T": len(T), "I": len(I), "SO": len(SO), "TO": len(TO)}
                mine = {k: r["views"][vname][k] for k in sizes}
                if not algebra or sizes != mine:
                    bad.append({"output": sr["output"], "view": vname, "algebra": algebra, "lists": sizes, "rows": mine})
            n += 1
        out["systems"][sysname] = {"graphs": n, "rows": len(rows), "bad": bad[:20], "bad_count": len(bad)}
        allpass &= (not bad and n == len(rows))
    out["pass"] = allpass
    return out


# ---------------------------------------------------------------- K3/K4/K5

def k3_tonghop_vs_raw(run):
    th_ = load("results/T-040/tong-hop.json")
    raw = load("results/T-040/runs/%s/tong-hop-raw.json" % run)
    bad = []
    n = 0
    for item in th_.get("_trich_tu_raw", []):
        n += 1
        a = resolve(th_, item["tong_hop"])
        b = resolve(raw, item["raw"])
        if a != b:
            bad.append(item)
    return {"checked": n, "bad": bad, "pass": n > 0 and not bad}


def k3b_t035_picks():
    """Số mô tả trích từ T-035 trong tong-hop.json phải bằng giá trị tại con trỏ của tệp nguồn."""
    th_ = load("results/T-040/tong-hop.json")["nguon_trace_T035"]
    src = load(th_["source"])
    bad, n = [], 0
    for ds in ["RE2-TT", "Nezha-OB"]:
        for k, v in th_[ds]["picked"].items():
            n += 1
            if resolve(src, v["pointer"].lstrip("#")) != v["value"]:
                bad.append({"dataset": ds, "key": k})
    return {"checked": n, "bad": bad, "pass": n > 0 and not bad}


def k4_registry(reg=None, md_override=None):
    reg = reg if reg is not None else load("results/T-040/so-lieu.json")
    bad = []
    cache = {}

    def get(pointer):
        fpath, ptr = pointer.split("#", 1)
        if fpath not in cache:
            cache[fpath] = load(fpath)
        return resolve(cache[fpath], ptr)

    for e in reg["entries"]:
        try:
            op = e.get("op")
            if op == "sum_of":
                val = sum(get(x) for x in e["pointers"])
            elif op == "minus":
                val = get(e["pointers"][0]) - get(e["pointers"][1])
            elif op == "len":
                val = len(get(e["pointer"]))
            else:
                val = get(e["pointer"])
        except Exception as ex:  # noqa
            bad.append({"id": e["id"], "why": "pointer_unresolved", "err": str(ex)})
            continue
        if val != e["value"]:
            bad.append({"id": e["id"], "why": "value_mismatch", "registry": e["value"], "actual": val})
        md = (md_override or {}).get(e["file"]) or open(P("results/T-040/" + e["file"]), encoding="utf-8").read()
        if e["snippet"] not in md:
            bad.append({"id": e["id"], "why": "snippet_missing", "snippet": e["snippet"]})
        # số phải hiện trong đoạn chữ (dạng 1069 hoặc 1.069), trừ mục ghi bằng chữ
        if not e.get("word") and isinstance(val, int):
            forms = {str(val), "{:,}".format(val).replace(",", ".")}
            import re
            if not any(re.search(r"(?<![\d.])" + re.escape(f) + r"(?![\d])", e["snippet"]) for f in forms):
                bad.append({"id": e["id"], "why": "number_not_in_snippet", "value": val, "snippet": e["snippet"]})
    return {"entries": len(reg["entries"]), "bad": bad, "pass": bool(reg["entries"]) and not bad}


def k4_negative():
    """Phép thử giả cho K4: đổi một giá trị trong sổ, hoặc đổi một số trong báo cáo, phải bị bắt."""
    reg = load("results/T-040/so-lieu.json")
    first = next(e for e in reg["entries"] if not e.get("word") and isinstance(e["value"], int))
    r1 = copy.deepcopy(reg)
    for e in r1["entries"]:
        if e["id"] == first["id"]:
            e["value"] += 1
    a = k4_registry(r1)
    md = open(P("results/T-040/" + first["file"]), encoding="utf-8").read()
    b = k4_registry(reg, {first["file"]: md.replace(first["snippet"], first["snippet"] + "X9", 1).replace(first["snippet"], "")})
    return {"value_tamper_caught": not a["pass"], "snippet_tamper_caught": not b["pass"],
            "pass": (not a["pass"]) and (not b["pass"])}


def k5_guard():
    bad = []
    for rel in ["results/T-040/tong-hop.json", "results/T-040/so-lieu.json", "results/T-040/con-mo.json"]:
        txt = open(P(rel), encoding="utf-8").read()
        if "reviewer-r1-fix" in txt:
            # chỉ được nhắc như bằng chứng trạng thái, không làm nguồn số
            for line in txt.split("\n"):
                if "reviewer-r1-fix" in line and '"pointer"' in line:
                    bad.append({"file": rel, "line": line.strip()[:200]})
    tt = load("results/T-040/tong-hop.json")["he_thong"]["TT"]
    for k, v in tt["doi_chieu"]["phu_thuoc_S"].items():
        if v.get("trang_thai") != th.TT_STATUS_CODE:
            bad.append({"field": k, "why": "S-dependent field lacks conditional status"})
    # R3: kiểm nguồn quyết định theo snapshot đã đọc phải bắt được thêm/sửa/xóa/xóa hết
    dv = load("results/T-040/dau-vao.json")
    rel = dv["doi_chieu_quyet_dinh_T038"]["snapshot"]
    snap = load(rel)
    cur = th.decision_line_hashes("T-038")
    base = th.compare_decision_snapshot(rel, "T-038", snap, cur)["unchanged"]
    q0 = sorted(cur)[0]
    tamper = {
        "removed_line": {q: h for q, h in cur.items() if q != q0},
        "added_line": dict(cur, **{"Q-999": "0" * 64}),
        "changed_line": dict(cur, **{q0: "0" * 64}),
        "all_removed": {},
    }
    caught = {k: not th.compare_decision_snapshot(rel, "T-038", snap, c)["unchanged"] for k, c in tamper.items()}
    if not base:
        bad.append({"why": "decision lines differ from read snapshot", "detail": dv["doi_chieu_quyet_dinh_T038"]})
    if not all(caught.values()):
        bad.append({"why": "decision snapshot check misses tamper", "caught": caught})
    return {"bad": bad, "decision_snapshot_current_unchanged": base, "decision_tamper_caught": caught, "pass": not bad}


# ---------------------------------------------------------------- K6

def sha(b):
    return hashlib.sha256(b).hexdigest()


def k6_scope(baseline_dir):
    res = {}
    pv = os.path.join(baseline_dir, "pham-vi-truoc.json")
    if os.path.exists(pv):  # mốc mở của phiên sau: LOG chỉ nối sau độ dài đã ghi
        cfg = json.load(open(pv, encoding="utf-8"))
        st = open(P("docs/STATE.md"), "rb").read()
        lines = st.split(b"\n")
        idx = [i for i, ln in enumerate(lines) if ln.startswith("| T-040 |".encode())]
        ok_state = len(idx) == 1
        if ok_state:
            l2 = list(lines)
            l2[idx[0]] = cfg["state_open_row"].encode("utf-8") + (b"\r" if lines[idx[0]].endswith(b"\r") else b"")
            ok_state = sha(b"\n".join(l2)) == cfg["state_open_sha"]
        res["state_only_T040_row_changed"] = ok_state
        lg = open(P("tasks/T-040-p5b-tong-hop/LOG.md"), "rb").read()
        res["log_append_only"] = sha(lg[:cfg["log_open_len"]]) == cfg["log_open_sha_full"]
        res["spec_unchanged"] = sha(open(P("tasks/T-040-p5b-tong-hop/SPEC.md"), "rb").read()) == cfg["spec_sha"]
        if "review_open_len" in cfg:  # Phiên 5: người làm chỉ điền bảng phản hồi ở cuối REVIEW
            rv = open(P("tasks/T-040-p5b-tong-hop/REVIEW.md"), "rb").read()
            res["review_append_only"] = sha(rv[:cfg["review_open_len"]]) == cfg["review_open_sha_full"]
            ok_state = ok_state and res["review_append_only"]
        return _k6_rest(baseline_dir, res, ok_state)
    st = open(P("docs/STATE.md"), "rb").read()
    lines = st.split(b"\n")
    idx = [i for i, ln in enumerate(lines) if ln.startswith("| T-040 |".encode())]
    ok_state = len(idx) == 1
    if ok_state:
        l2 = list(lines)
        l2[idx[0]] = STATE_OPEN_ROW.encode("utf-8") + (b"\r" if lines[idx[0]].endswith(b"\r") else b"")
        ok_state = sha(b"\n".join(l2)) == STATE_OPEN_SHA
    res["state_only_T040_row_changed"] = ok_state
    lg = open(P("tasks/T-040-p5b-tong-hop/LOG.md"), "rb").read()
    i = lg.find(LOG_P2_MARK.encode("utf-8"))
    res["log_append_only"] = i > 0 and sha(lg[:i]) == LOG_OPEN_SHA
    res["spec_unchanged"] = sha(open(P("tasks/T-040-p5b-tong-hop/SPEC.md"), "rb").read()) == SPEC_SHA
    return _k6_rest(baseline_dir, res, ok_state)


def _k6_rest(baseline_dir, res, ok_state):
    prot = json.load(open(os.path.join(baseline_dir, "protected-hashes-truoc.json"), encoding="utf-8"))
    changed = []
    for rel, h in prot["files"].items():
        path = P(rel)
        if not os.path.exists(path):
            changed.append({"path": rel, "why": "missing"})
        elif sha(open(path, "rb").read()) != h:
            changed.append({"path": rel, "why": "changed"})
    res["protected_files"] = len(prot["files"])
    res["protected_changed"] = changed
    gs = os.path.join(baseline_dir, "git-status-truoc.txt")
    if os.path.exists(gs + ".gz"):
        before = set(gzip.open(gs + ".gz", "rt", encoding="utf-8").read().splitlines())
    else:
        before = set(open(gs, encoding="utf-8").read().splitlines())
    now = subprocess.run(["git", "-C", ROOT, "status", "--porcelain=v1", "--untracked-files=all"],
                         capture_output=True, text=True, encoding="utf-8").stdout.splitlines()
    new = [ln for ln in now if ln not in before]
    outside = [ln for ln in new if not (ln[3:].startswith(ALLOWED_PREFIX) or ln[3:] in ALLOWED_FILES)]
    res["git_status_new_entries"] = len(new)
    res["git_status_new_outside_scope"] = outside
    res["pass"] = (ok_state and res["log_append_only"] and res["spec_unchanged"] and not changed and not outside)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--baseline-dir", required=True)
    ap.add_argument("--out", required=True, help="tên tệp kết quả trong runs/<run>/")
    a = ap.parse_args()
    t0 = time.time()
    res = {"run": a.run, "started_local": time.strftime("%Y-%m-%d %H:%M:%S")}
    for name, fn in [("K1_mutation", k1_mutation), ("K2_lists", lambda: k2_lists(a.run)),
                     ("K3_tonghop_vs_raw", lambda: k3_tonghop_vs_raw(a.run)), ("K3b_t035", k3b_t035_picks), ("K4_registry", k4_registry), ("K4b_negative", k4_negative),
                     ("K5_guard", k5_guard), ("K6_scope", lambda: k6_scope(a.baseline_dir))]:
        s = time.time()
        try:
            res[name] = fn()
        except Exception as ex:  # giữ lỗi, không dừng các phép khác
            res[name] = {"pass": False, "exception": repr(ex)}
        res[name]["seconds"] = round(time.time() - s, 2)
        print(name, "PASS" if res[name].get("pass") else "FAIL", res[name]["seconds"], flush=True)
    res["all_pass"] = all(res[k].get("pass") for k in res if k.startswith("K"))
    res["wall_s"] = round(time.time() - t0, 2)
    res["peak_working_set_bytes"] = th.peak_rss_bytes()
    th.dump_json(res, P("results/T-040/runs/%s/%s" % (a.run, a.out)))
    print("ALL", "PASS" if res["all_pass"] else "FAIL")


if __name__ == "__main__":
    main()
