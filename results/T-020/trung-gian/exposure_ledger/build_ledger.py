"""T020 ledger: reads only frozen saved results; writes only this directory.

No data/ access, raw measurements, external runtime, model execution or split.
Source identities remain separate unless a saved content/injection comparison proves a link.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import re
import tarfile
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
SEED = "20261004"
STARTED = time.perf_counter()
FREEZE = ROOT / "results/T-020/trung-gian/input-freeze.json"
freeze = json.loads(FREEZE.read_text(encoding="utf-8-sig"))
frozen = {x["path"].replace("\\", "/"): x for x in freeze["inputs"]}
used = {}


def read(path):
    p = str(path).replace("\\", "/")
    assert p.startswith("results/") and not "/locked/" in p and not p.startswith("results/T-020/"), p
    assert p in frozen, p
    b = (ROOT / p).read_bytes()
    h = hashlib.sha256(b).hexdigest()
    assert h == frozen[p]["sha256"], (p, "input changed")
    used[p] = {"sha256": h, "bytes": len(b)}
    return b


def js(path):
    return json.loads(read(path).decode("utf-8-sig"))


def cs(path):
    return list(csv.DictReader(io.StringIO(read(path).decode("utf-8-sig"))))


def write_json(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(name, rows, fields=None):
    rows = list(rows)
    fields = fields or (list(rows[0]) if rows else ["note"])
    with (OUT / name).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def digest(value):
    return hashlib.sha256(str(value).encode()).hexdigest()


def parse_case(case):
    c = case.replace("\\", "/").strip("/")
    c = re.sub(r"_(full|win|failed)$", "", c)
    m = re.search(r"(re[123](?:tt|ob|ss))_([^/]+)_(cpu|mem|disk|delay|loss|socket|f\d+)_(\d+)", c)
    if m:
        return m.group(1), m.group(2), m.group(3), m.group(4)
    m = re.search(r"([^/]+)_(cpu|mem|disk|delay|loss|socket|f\d+)[_/](\d+)", c)
    if m:
        return "", m.group(1), m.group(2), m.group(3)
    return None


records = {}
aliases = {}
evidence_rows = []
source_rows = Counter()
source_sets = defaultdict(set)
open_relations = []


def add(identity, dataset, case, root="", fault="", repeat="", unit="incident", proof="", status="FACT"):
    if identity not in records:
        records[identity] = {"identity": identity, "dataset": dataset, "case": case, "root": root,
            "fault": fault, "repetition": repeat, "unit": unit, "identity_evidence": proof,
            "identity_status": status, "factual_seen": "TX0", "ran_method": False,
            "ranking_seen": False, "detector_seen": False, "exposure_ambiguity": "",
            "source_invalid_marker": False,
            "locked_public_complement": False, "dev_v1_allowlist": False,
            "sources": set(), "evidence": set(), "aliases": set()}
    return identity


def expose(identity, tx, source, ref, ran=False, rank=False, detector=False, ambiguity=""):
    assert identity in records, identity
    q = records[identity]
    q["factual_seen"] = max(q["factual_seen"], tx)
    q["ran_method"] |= ran
    q["ranking_seen"] |= rank
    q["detector_seen"] |= detector
    if ambiguity:
        q["exposure_ambiguity"] = ambiguity
    q["sources"].add(source)
    q["evidence"].add(ref)
    source_rows[source] += 1
    source_sets[source].add(identity)
    evidence_rows.append({"source": source, "identity": identity, "factual_seen": tx,
        "reference": ref, "ran_method": ran, "ranking_seen": rank, "detector_seen": detector})


suite_names = {"re1ob": "RE1-OB", "re1ss": "RE1-SS", "re1tt": "RE1-TT", "re2ob": "RE2-OB",
    "re2ss": "RE2-SS", "re2tt": "RE2-TT", "re3ob": "RE3-OB", "re3ss": "RE3-SS", "re3tt": "RE3-TT"}
hf_path = "results/T-002/public-metadata/run-002/hf-tree.json"
hf = js(hf_path)
hf_files = {x["path"]: x for x in hf if x["type"] == "file"}
public_ids = {}
for x in hf:
    p = x["path"]
    if x["type"] != "directory" or "/" in p or not parse_case(p):
        continue
    family, root, fault, rep = parse_case(p)
    metric = hf_files.get(p + "/metrics.parquet", {})
    injection = hf_files.get(p + "/inject_time.txt", {})
    fingerprint = (metric.get("lfs", {}).get("oid", metric.get("oid", "")), injection.get("oid", ""))
    ident = "RCAEval-public:" + digest((family, fingerprint))[:24]
    assert all(fingerprint), p
    add(ident, suite_names[family], p, root, fault, rep,
        proof=f"{hf_path}#{p}; metric content hash + inject Git oid; directory oid {x['oid']}")
    public_ids[p] = ident
    aliases[(family, root, fault, rep)] = ident
    records[ident]["aliases"].add(p)
    expose(ident, "TX0", "T-002-public-census", hf_path + "#" + p)
assert len(public_ids) == 735, len(public_ids)

# Existing descriptive inspections: only result metadata, plus a public injection oid check.
t2_cases = "results/T-002/local-inspection/run-002/cases.json"
for idx, x in enumerate(js(t2_cases)):
    case = x["case"]
    value = str(int(x["inject_time"])).encode()
    git_oid = hashlib.sha1(b"blob " + str(len(value)).encode() + b"\0" + value).hexdigest()
    assert git_oid == hf_files[case + "/inject_time.txt"]["oid"], case
    assert x["metrics_bytes"] == hf_files[case + "/metrics.parquet"]["size"], case
    records[public_ids[case]]["identity_evidence"] += f"; {t2_cases}#{idx}; injection git oid verified from saved timestamp"
    expose(public_ids[case], "TX1", "T-002-descriptive", t2_cases + "#" + str(idx))

# Saved local recording fingerprints and proven public content crosswalk.
local_path = "results/T-019/lineage/local-file-manifest.json"
locals_ = js(local_path)
local_lookup = {}
comparisons = js("results/T-019/lineage/public-metric-comparisons.json")
proven = {}
for i, x in enumerate(comparisons):
    assert x["inject_value_equal"] and x["inject_byte_sha_equal"], i
    assert x["column_set_equal"] and x["finite_time_content_equal"], i
    assert x["finite_time_vector_equal"] and x["value_columns_different"] == 0, i
    proven[(x["source"].lower(), x["local_case"])] = (public_ids[x["public_case"]], i)
for i, x in enumerate(locals_):
    source = x["source"].lower()
    _, root, fault, rep = parse_case(x["case"])
    k = (source, x["case"])
    if k in proven:
        ident, cidx = proven[k]
        records[ident]["identity_evidence"] += "; results/T-019/lineage/public-metric-comparisons.json#" + str(cidx)
    else:
        met = x["files"].get("simple_data.csv", x["files"].get("simple_metrics.csv", x["files"].get("data.csv", {})))
        ident = "local-recording:" + digest((x["inject_time"], met.get("sha256")))[:24]
        add(ident, "BARO-FSE-OB" if source == "fse-ob" else x["source"], source + "/" + x["case"], root, fault, rep,
            proof=f"{local_path}#{i}; injection + metric SHA256")
    local_lookup[k] = ident
    aliases[(source, root, fault, rep)] = ident
    records[ident]["aliases"].add(source + "/" + x["case"])
    expose(ident, "TX1", "T-019-local-lineage", local_path + "#" + str(i))

# RE1-OB local results are not automatically the public HF release. Forty FSE aliases
# are proved by full-file SHA256 aggregate groups; remaining 85 remain source-scoped.
log_a = read("results/T-006/runs/05b-so-re1-fse-ob-simple.log").decode("utf-8", "replace")
log_b = read("results/T-006/runs/05c-so-re1-fse-ob-theo-loi.log").decode("utf-8", "replace")
assert "file cùng SHA-256: 40/80" in log_a
assert "'delay': (20, 20)" in log_b and "'loss': (20, 20)" in log_b
local_re1ob = {}
for root in ["adservice", "cartservice", "checkoutservice", "currencyservice", "productcatalogservice"]:
    for fault in ["cpu", "mem", "disk", "delay", "loss"]:
        for rep in map(str, range(1, 6)):
            if root != "adservice" and fault in ["delay", "loss"]:
                ident = aliases[("fse-ob", root, fault, rep)]
            else:
                ident = "local-RE1OB:" + digest(("Zenodo14590730/13305663", root, fault, rep))[:24]
                add(ident, "RE1-OB-local-Zenodo", f"local-re1ob/{root}_{fault}_{rep}", root, fault, rep,
                    proof="T006 archive metadata --dataset online-boutique + source-link; saved ZIP CRC/size crosswalk",
                    status="OPEN public-HF recording identity")
            aliases[("local-re1ob", root, fault, rep)] = ident
            local_re1ob[(root, fault, rep)] = ident
            records[ident]["aliases"].add(f"local-re1ob/{root}_{fault}_{rep}")
            public = f"re1ob_{root}_{fault}_{rep}"
            if public in public_ids:
                records[public_ids[public]]["exposure_ambiguity"] = "OPEN copy relation to local RE1OB that has per-case method results; do not infer exposure or eligibility from names"
                open_relations.append({"left": ident, "right": public_ids[public], "relation": "local RE1OB to HF RE1OB",
                    "status": "OPEN", "evidence": "names plus common release provenance; no saved per-case HF content crosswalk",
                    "needed": "public injection/content crosswalk from authorized saved evidence", "owner": "Minh/G1"})
read("results/T-006/runs/02-so-zip-13305663-re1.log")

# TT copies: compare recorded matrix content and injection, never infer by name.
for p in ["results/T-016/runs/s0-cung-ca.json", "results/T-016/runs/s10-cung-ca.json"]:
    for i, x in enumerate(js(p)):
        if not x.get("trung"):
            continue
        assert x["moc_tiem_trung"] and x["so_o_lech_qua_lam_tron"] == 0
        case = Path(x["rcaeval"].replace("\\", "/")).name
        ident = public_ids[case]
        family, root, fault, rep = parse_case(case)
        source = "torai-tt" if family == "re2tt" else "torai-ob"
        aliases[(source, root, fault, rep)] = ident
        records[ident]["aliases"].add(f"{source}/{root}_{fault}/{rep}")
        records[ident]["identity_evidence"] += "; " + p + "#" + str(i)


def resolve(case, file_source="", source_hint=""):
    found = parse_case(case)
    if not found:
        return None
    family, root, fault, rep = found
    if family:
        return aliases.get((family, root, fault, rep))
    s = (str(file_source) + " " + source_hint + " " + str(case)).lower().replace("\\", "/")
    if source_hint in suite_names:
        return aliases.get((source_hint, root, fault, rep))
    for source in ["fse-ob", "fse-ss", "torai-ob", "torai-ss", "torai-tt", "local-re1ob", "re1-ss"]:
        if source in s:
            return aliases.get((source, root, fault, rep))
    return None


# T005 timing-only: factual TX1; code/result inspected did not show per-case ranks.
t5 = [json.loads(s) for s in read("results/T-005/runs/ket-qua-do.jsonl").decode("utf-8-sig").splitlines() if s.strip()]
t5code = read("results/T-005/scripts/chuan_bi_dau_vao.py").decode("utf-8")
t5run = read("results/T-005/scripts/chay_mot_luot.py").decode("utf-8")
assert "KHÔNG in ra, không đọc" in t5run
t5cases = re.findall(r'"(re2tt_[^"]+)"', t5code)
for case in sorted(set(t5cases)):
    expose(public_ids[case], "TX1", "T-005-timing-only", "results/T-005/scripts/chuan_bi_dau_vao.py#CASE/GDN_TRAIN",
        ran=True, ambiguity="timing-only runs; no per-case rank viewing evidence in T005; method execution eligibility policy OPEN")

# Parse saved method result archives; archive data members are never opened.
archive_records = {}
archive_audit = []
unresolved = []
for p in sorted(frozen):
    if not p.endswith(".tar.gz") or not p.startswith(("results/T-006/runs/", "results/T-007/runs/")):
        continue
    task = p.split("/")[1]
    b = read(p)
    result_rows = []
    with tarfile.open(fileobj=io.BytesIO(b), mode="r:gz") as tar:
        members = tar.getmembers()
        meta_members = [m for m in members if m.isfile() and m.name.endswith("/meta.json")]
        meta = json.load(tar.extractfile(meta_members[0])) if meta_members else {}
        cmd = meta.get("cmd", [])
        dataset = cmd[cmd.index("--dataset") + 1].lower() if "--dataset" in cmd else ""
        if dataset in ["online-boutique", "re1-ob"]:
            dataset = "local-re1ob"
        if not dataset and task == "T-007":
            dataset = "re2ob" if any(z in p for z in ["microrank", "tracerca", "thu-work"]) else "fse-ob"
        for m in members:
            if not m.isfile():
                continue
            if m.name.endswith("/ket-qua-gdn.json") and "gdn-msl" in p:
                value = json.load(tar.extractfile(m))
                ident = add("GDN-MSL:bundled-sample", "MSL-bundled-GDN", "bundled sample",
                    unit="multivariate time series sample; incident census OPEN", proof=p + "!" + m.name,
                    status="OPEN incident mapping")
                expose(ident, "TX2", task + "-runs", p + "!" + m.name, ran=True, detector=True)
            elif m.name.endswith("/ket-qua-vi-du.json") and "vi-du-baro" in p:
                value = json.load(tar.extractfile(m))
                ident = add("BARO:bundled-example", "BARO-bundled-example", "bundled example",
                    unit="example time series; incident identity OPEN", proof=p + "!" + m.name, status="OPEN incident mapping")
                expose(ident, "TX2", task + "-runs", p + "!" + m.name, ran=True, rank=True, detector=True)
            elif "/results/" in m.name and m.name.endswith(".json"):
                value = json.load(tar.extractfile(m))
                case = Path(m.name).stem
                ident = resolve(case, source_hint=dataset)
                if ident is None:
                    unresolved.append({"source": p, "case": case, "source_hint": dataset, "reason": "OPEN identity; no proven alias"})
                    continue
                rank = any(isinstance(x, list) and bool(x) for x in value.values())
                detector = "phat-hien" in p
                expose(ident, "TX2", task + "-runs", p + "!" + m.name, ran=True, rank=rank and not detector, detector=detector)
                result_rows.append((case, value, m.name))
            elif m.name.endswith("/tien-do.jsonl") and "bocpd" in p:
                lines = tar.extractfile(m).read().decode("utf-8", "replace").splitlines()
                for idx, line in enumerate(lines):
                    try:
                        value = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    case = value.get("case", "")
                    ident = resolve(case, source_hint="fse-ob")
                    if ident and value.get("cps") is not None:
                        expose(ident, "TX2", task + "-runs", p + "!" + m.name + "#" + str(idx), ran=True, detector=True)
    archive_records[p] = result_rows
    archive_audit.append({"archive": p, "sha256": digest(b) if False else hashlib.sha256(b).hexdigest(),
        "result_rows_resolved": len(result_rows), "dataset_metadata": dataset, "meta_result_count": meta.get("so_file_ket_qua", "")})

# Every requested case ledger, including historic T017. Different column names normalized.
csv_audit = []
for task in range(13, 19):
    for name in ["ca-da-chay.csv"] + (["ca-da-chay-lich-su.csv"] if task == 17 else []):
        p = f"results/T-{task:03d}/{name}"
        rows = cs(p)
        resolved = 0
        for idx, x in enumerate(rows):
            case = x.get("ca", x.get("case", ""))
            src = x.get("file_nguon", x.get("source", ""))
            ident = resolve(case, src)
            if ident:
                detector = "phát hiện" in x.get("phuong_phap", "").lower() or "bocpd" in x.get("phuong_phap", "").lower()
                expose(ident, "TX2", f"T-{task:03d}-" + name, p + "#row=" + str(idx + 2), ran=True,
                    rank=not detector, detector=detector)
                resolved += 1
            elif "synthetic" in case.lower():
                ident = add("fixture:" + digest((p, case))[:24], "Synthetic", case, unit="fixture",
                    proof=p + "#row=" + str(idx + 2))
                expose(ident, "TX2", f"T-{task:03d}-" + name, p + "#row=" + str(idx + 2), ran=True)
                resolved += 1
            else:
                unresolved.append({"source": p, "case": case, "source_hint": src, "reason": "OPEN identity; no proven alias"})
        csv_audit.append({"source": p, "rows": len(rows), "resolved": resolved, "unresolved": len(rows) - resolved,
            "original_columns": "|".join(rows[0]) if rows else ""})

# T019 relational ledger. Do not treat unestablished relation rows as new incidents.
t19path = "results/T-019/so-ca-da-nhin.csv"
t19rows = cs(t19path)
for idx, x in enumerate(t19rows):
    source = x["source"].lower()
    if x.get("public_case") and (source.startswith("hf") or source == "t019"):
        ident = public_ids.get(x["public_case"])
    else:
        ident = resolve(x["case"], source_hint=source)
    if ident is None and x["case"] in public_ids:
        ident = public_ids[x["case"]]
    if ident is None:
        unresolved.append({"source": t19path, "case": x["case"], "source_hint": source, "reason": "OPEN identity; no proven alias"})
        continue
    is_rank = x["exposure"] == "RCA_result"
    expose(ident, "TX2" if is_rank else "TX1", "T-019-ledger", t19path + "#row=" + str(idx + 2), ran=is_rank, rank=is_rank)
t19summary = js("results/T-019/ledger-summary.json")
assert len(t19rows) == t19summary["total_rows"] == 1245
assert Counter(x["exposure"] for x in t19rows) == t19summary["exposure_counts"]

# Public label census from Nezha and Eadro, with saved descriptive inspections.
for task, dataset_prefix, labelpath in [(8, "Nezha", "results/T-008/runs/run-001/labels.json"),
        (9, "Eadro", "results/T-009/runs/run-001/labels.json")]:
    labels = js(labelpath)
    inspected_ref = "results/T-008/runs/evidence-002/summary.json" if task == 8 else "results/T-009/runs/inspect-004/summary.json"
    js(inspected_ref)
    for i, x in enumerate(labels):
        dataset = dataset_prefix + "-" + x["dataset"]
        timestamp = x.get("inject_timestamp_raw", x.get("start"))
        # Two Nezha TT records have the same raw epoch but different textual injection times.
        # Keep separate label records; a clock conflict is not evidence of duplicate incidents.
        time_text = x.get("inject_time_raw", "")
        ident = dataset_prefix + ":" + digest((x["dataset"], x["entity_raw"], x["fault"], timestamp, time_text))[:24]
        is_clock_open = task == 8 and x["dataset"] == "TT"
        add(ident, dataset, f"{dataset}/{timestamp}/{x['service']}/{x['fault']}", x["service"], x["fault"],
            unit="labelled incident (clock mapping OPEN)" if is_clock_open else "incident",
            proof=f"{labelpath}#{i}; entity + fault + injection timestamp + textual time tuple",
            status="OPEN native injection clocks" if is_clock_open else "FACT")
        expose(ident, "TX1", f"T-{task:03d}-descriptive", inspected_ref + "; " + labelpath + "#" + str(i))
    if task == 8:
        epoch_groups = defaultdict(list)
        for i, x in enumerate(labels):
            epoch_groups[(x["dataset"], x["entity_raw"], x["fault"], x["inject_timestamp_raw"])].append((i, x))
        for group in epoch_groups.values():
            if len(group) <= 1:
                continue
            (ia, a), (ib, b) = group
            ida = "Nezha:" + digest((a["dataset"], a["entity_raw"], a["fault"], a["inject_timestamp_raw"], a["inject_time_raw"]))[:24]
            idb = "Nezha:" + digest((b["dataset"], b["entity_raw"], b["fault"], b["inject_timestamp_raw"], b["inject_time_raw"]))[:24]
            open_relations.append({"left": ida, "right": idb, "relation": "same native epoch but different textual injection times",
                "status": "OPEN", "evidence": f"{labelpath}#{ia}/{ib}; epoch={a['inject_timestamp_raw']}; text {a['inject_time_raw']} versus {b['inject_time_raw']}",
                "needed": "label clock/provenance correction; determine distinct injections without method scores", "owner": "Minh/G1"})

# Bank labels are metadata, not measurements. Root is component/pod, not service.
bankpath = "results/T-012/runs/bank-label-reproduce-002/record.csv"
bank = cs(bankpath)
for i, x in enumerate(bank):
    ident = "OpenRCA-Bank:" + digest((x["level"], x["component"], x["timestamp"], x["reason"]))[:24]
    add(ident, "OpenRCA-Bank", f"Bank/{x['timestamp']}/{x['component']}", x["component"], x["reason"],
        unit="labelled incident at pod/component level", proof=bankpath + f"#row={i + 2}; component+time+reason+level")
    expose(ident, "TX0", "T-012-Bank-labels", bankpath + f"#row={i + 2}")

# Remaining survey units: retain nonincident semantics; never fabricate root×fault cells.
deep = js("results/T-010/runs/inspect-005/summary.json")
deep_cases = js("results/T-010/runs/inspect-002/raw-cases.json")
for idx, x in enumerate(deep_cases):
    case = x["case_directory"]
    ident = add("DeepTraLog-capture:" + digest((x["archive"], case, x.get("time_min_ms"), x.get("time_max_ms"), x["span_rows"]))[:24],
        "DeepTraLog-TT", case, unit="storage capture",
        proof="results/T-010/runs/inspect-002/raw-cases.json#" + str(idx) + "; archive + saved clock bounds + span rows; not root/onset census", status="OPEN incident mapping")
    expose(ident, "TX1", "T-010-descriptive", "results/T-010/runs/inspect-002/raw-cases.json#" + str(idx))
lemma = js("results/T-011/file-inspection-summary.json")
lemma_catalog = js("results/T-011/runs/run-001/count-summary.json")
for dataset, info in lemma_catalog["datasets"].items():
    for date in info["date_tokens"]:
        name = "LEMMA-" + dataset.replace("_Preprocessed", "-Preprocessed").replace("_Original", "-Original")
        ident = add("LEMMA-capture:" + digest((dataset, date, info["revision"]))[:24], name, date,
            unit="date capture", proof="results/T-011/runs/run-001/count-summary.json#datasets/" + dataset + "; public revision+date token",
            status="OPEN per-incident census")
        inspected = (dataset, date) in [("Product_Review_Preprocessed", "20211203"), ("Cloud_Computing_Preprocessed", "20240124")]
        expose(ident, "TX1" if inspected else "TX0", "T-011-descriptive" if inspected else "T-011-public-catalog",
            "results/T-011/file-inspection-summary.json#scope" if inspected else "results/T-011/runs/run-001/count-summary.json#datasets/" + dataset)
fsep = "results/T-012/runs/fse-file-inspect-003/cases.json"
for i, x in enumerate(js(fsep)):
    inj = x["injection"]
    roots = "|".join(x["roots"])
    ident = add("FSE-propagation:" + digest((inj["task_id"], inj["id"], inj["start_time"]))[:24], "FSE-2026-propagation-TT",
        x["case"], roots, str(inj["fault_type"]), unit="injection event (possibly multiple roots)", proof=fsep + "#" + str(i))
    records[ident]["source_invalid_marker"] = x["invalid_marker"]
    expose(ident, "TX1", "T-012-FSE-descriptive", fsep + "#" + str(i))
anop = "results/T-012/runs/anomod-file-inspect-003/cases.json"
for i, x in enumerate(js(anop)):
    if x["case"] == ".DS_Store":
        continue
    ident = add("AnoMod-capture:" + digest((x["system"], x["case"]))[:24], "AnoMod-" + x["system"], x["case"],
        unit="experiment capture; root binding OPEN", proof=anop + "#" + str(i), status="OPEN incident/root binding")
    expose(ident, "TX1", "T-012-AnoMod-descriptive", anop + "#" + str(i))

# Locked IDs inferred only from complete public census minus the saved v1 allowlist.
allowlist = set(js("results/T-017/allowlist.json"))
tt = {x for x in public_ids if x.startswith("re2tt_")}
locked = sorted(tt - allowlist)
assert len(tt) == 90 and len(allowlist) == 30 and allowlist <= tt and len(locked) == 60
for case in tt:
    q = records[public_ids[case]]
    q["locked_public_complement"] = case in locked
    q["dev_v1_allowlist"] = case in allowlist
assert all(records[public_ids[c]]["factual_seen"] == "TX0" for c in locked)
assert not any(records[public_ids[c]]["ran_method"] for c in locked)
assert len({(records[public_ids[c]]["root"], records[public_ids[c]]["fault"]) for c in allowlist}) == 10

# Save unique records and the observation-to-identity reconciliation.
final = []
for q in sorted(records.values(), key=lambda q: (q["dataset"], q["case"])):
    row = dict(q)
    for key in ["sources", "evidence", "aliases"]:
        row[key] = "|".join(sorted(q[key]))
    final.append(row)
write_csv("02-so-ca-da-nhin.csv", final)
write_csv("exposure-evidence.csv", evidence_rows)
write_csv("public-census.csv", [x for x in final if x["root"] and x["fault"]])
write_csv("locked-public-60.csv", [x for x in final if x["locked_public_complement"]])
write_csv("unresolved-aliases.csv", open_relations)
write_csv("unresolved-source-rows.csv", unresolved, ["source", "case", "source_hint", "reason"])
write_csv("archive-audit.csv", archive_audit)
write_csv("csv-normalization-audit.csv", csv_audit)

# Dataset membership is separate from canonical union ownership: local RE1OB has125
# members,40 already owned by the FSE identity namespace. Do not show85 as its census.
memberships = []
for case, ident in public_ids.items():
    q = records[ident]
    memberships.append({"dataset": q["dataset"], "case": case, "identity": ident, "root": q["root"], "fault": q["fault"],
        "repetition": q["repetition"], "factual_seen": q["factual_seen"], "membership_proof": hf_path + "#" + case})
for (root, fault, rep), ident in sorted(local_re1ob.items()):
    memberships.append({"dataset": "RE1-OB-local-Zenodo", "case": f"{root}_{fault}_{rep}", "identity": ident,
        "root": root, "fault": fault, "repetition": rep, "factual_seen": records[ident]["factual_seen"],
        "membership_proof": "T006 archive metadata/source-link; forty delay/loss SHA256 aliases in 05b/05c logs"})
for dataset, source in [("BARO-FSE-OB", "fse-ob"), ("BARO-FSE-SS", "fse-ss"), ("TORAI-OB", "torai-ob"), ("TORAI-SS", "torai-ss")]:
    for (s, case), ident in local_lookup.items():
        if s != source:
            continue
        q = records[ident]
        memberships.append({"dataset": dataset, "case": case, "identity": ident, "root": q["root"], "fault": q["fault"],
            "repetition": q["repetition"], "factual_seen": q["factual_seen"], "membership_proof": local_path + "#" + source + "/" + case})
for q in final:
    if not q["dataset"].startswith("RE") and q["dataset"] != "BARO-FSE-OB":
        memberships.append({"dataset": q["dataset"], "case": q["case"], "identity": q["identity"], "root": q["root"], "fault": q["fault"],
            "repetition": q["repetition"], "factual_seen": q["factual_seen"], "membership_proof": q["identity_evidence"]})
write_csv("dataset-census-membership.csv", memberships)

dataset_rows = []
cell_rows = []
for dataset in sorted({q["dataset"] for q in records.values()}):
    qs = [q for q in records.values() if q["dataset"] == dataset]
    by_tx = Counter(q["factual_seen"] for q in qs)
    cells = defaultdict(list)
    for q in qs:
        if q["root"] and q["fault"]:
            cells[(q["root"], q["fault"])].append(q)
    dataset_rows.append({"dataset": dataset, "units": "|".join(sorted({q["unit"] for q in qs})),
        "catalog_units": len(qs), "highest_seen": max(q["factual_seen"] for q in qs),
        "TX0": by_tx["TX0"], "TX1": by_tx["TX1"], "TX2": by_tx["TX2"],
        "remain_TX0_or_TX1": by_tx["TX0"] + by_tx["TX1"], "label_cells": len(cells),
        "identity_open_units": sum(q["identity_status"].startswith("OPEN") for q in qs)})
    for (root, fault), group in sorted(cells.items()):
        cell_rows.append({"dataset": dataset, "root": root, "fault": fault, "unit": "|".join(sorted({q["unit"] for q in group})),
            "catalog_units": len(group), "highest_seen": max(q["factual_seen"] for q in group),
            "TX0": sum(q["factual_seen"] == "TX0" for q in group), "TX1": sum(q["factual_seen"] == "TX1" for q in group),
            "TX2": sum(q["factual_seen"] == "TX2" for q in group), "identity_open_units": sum(q["identity_status"].startswith("OPEN") for q in group)})
write_csv("dataset-exposure.csv", dataset_rows)
write_csv("cell-exposure.csv", cell_rows)
membership_summary = []
for dataset in sorted({q["dataset"] for q in memberships}):
    group = [q for q in memberships if q["dataset"] == dataset]
    tx = Counter(q["factual_seen"] for q in group)
    membership_summary.append({"dataset": dataset, "dataset_members": len(group), "unique_identity_units": len({q["identity"] for q in group}),
        "TX0": tx["TX0"], "TX1": tx["TX1"], "TX2": tx["TX2"],
        "highest_seen": max(q["factual_seen"] for q in group), "cells": len({(q["root"], q["fault"]) for q in group if q["root"] and q["fault"]})})
write_csv("dataset-membership-exposure.csv", membership_summary)
ordered_sources = sorted(source_sets)
reconcile = []
seen = set()
for source in ordered_sources:
    s = source_sets[source]
    reconcile.append({"source": source, "source_rows": source_rows[source], "unique_identity_units": len(s),
        "overlap_prior_sources": len(s & seen), "new_to_union": len(s - seen), "union_after": len(s | seen)})
    seen |= s
write_csv("source-reconciliation.csv", reconcile)
intersections = []
for i, a in enumerate(ordered_sources):
    for b in ordered_sources[i + 1:]:
        common = source_sets[a] & source_sets[b]
        if common:
            intersections.append({"source_a": a, "source_b": b, "intersection_identity_units": len(common)})
write_csv("source-intersections.csv", intersections)
assert sum(x["new_to_union"] for x in reconcile) == len(seen) == len(records)
assert all(len({q["identity"] for q in source_sets and [records[z] for z in source_sets[s]]}) == len(source_sets[s]) for s in ordered_sources)

# Numeric audit pool: save scalar leaves and independent recomputation, seed selection.
number_pool = []


def number(task, path, key, value, calculated, meaning, check_ref, rule):
    ok = isinstance(calculated, (int, float)) and math.isclose(value, calculated, rel_tol=1e-10, abs_tol=1e-9)
    number_pool.append({"task": task, "path": path, "key": key, "published": value, "recomputed": calculated,
        "meaning": meaning, "check_reference": check_ref, "calculation": rule, "ok": ok,
        "selection_sha256": digest(f"{SEED}|{task}|{path}|{key}")})


# T005: emitted raw log values independently reconciled to JSONL. No new measurements.
for idx, row in enumerate(t5):
    logfile = f"results/T-005/runs/do-{row['muc']}-{row['bien_the']}-lan{row['lan']}.log"
    if logfile not in frozen:
        continue
    text = read(logfile).decode("utf-8", "replace")
    emitted = [json.loads(s.split("KET_QUA ", 1)[1]) for s in text.splitlines() if s.startswith("KET_QUA ")]
    if not emitted:
        continue
    raw = emitted[-1]
    for key in ["import_s", "load_s", "method_s", "ws_before_method_mb", "peak_ws_mb", "peak_private_mb", "ws_mb"]:
        if key in row and key in raw:
            number("T-005", "results/T-005/runs/ket-qua-do.jsonl", f"[{idx}].{key}", row[key], raw[key], key,
                logfile + "#KET_QUA", "compare independent raw stdout line; timings are historical observations")


def score_rows(rows):
    by_fault = defaultdict(list)
    rank_lens = []
    for case, value, member in rows:
        parse = parse_case(case)
        if not parse or "error" in value:
            continue
        _, root, fault, rep = parse
        for rank in value.values():
            if not isinstance(rank, list) or any(not isinstance(x, str) for x in rank):
                continue
            sr = list(dict.fromkeys(x.split("_")[0].replace("-db", "") for x in rank))
            pos = sr.index(root) + 1 if root in sr else math.inf
            by_fault[fault].append(pos)
            rank_lens.append(len(rank))
    by_fault["ALL"] = [p for f, group in by_fault.items() for p in group]
    return by_fault, rank_lens


# T006: all directly matching cham files, reconstructed from per-case archived ranks.
for archive, rows in archive_records.items():
    if not archive.startswith("results/T-006/") or not rows:
        continue
    name = Path(archive).name[:-7]
    p = "results/T-006/cham/" + name + ".json"
    if p not in frozen:
        continue
    summary = js(p)
    if not isinstance(summary, dict) or "diem" not in summary:
        continue
    groups, lengths = score_rows(rows)
    for fault, values in summary["diem"].items():
        group = groups["ALL" if fault == "AVERAGE" else fault]
        if not group:
            continue
        n = len(group)
        calc = {"n": n, "AC1": sum(pos <= 1 for pos in group) / n, "AC3": sum(pos <= 3 for pos in group) / n,
            "Avg5": sum(sum(pos <= k for k in range(1, 6)) / 5 for pos in group) / n}
        for key in calc:
            number("T-006", p, f"diem.{fault}.{key}", values[key], calc[key], key, archive + "!*/results/*.json",
                "group/count; unique service rank; Hits@k summed over every rank; Avg5 mean of Hits@1..5")
    if lengths and summary.get("kiem", {}).get("do_dai_rank"):
        for key, value in [("min", min(lengths)), ("max", max(lengths))]:
            number("T-006", p, "kiem.do_dai_rank." + key, summary["kiem"]["do_dai_rank"][key], value,
                "rank_length", archive + "!*/results/*.json", "min/max raw rank list lengths")

# T007: both full ranking tables, using archived results and original unit mapping.
for method in ["microrank", "tracerca"]:
    p = f"results/T-007/cham/py312-pin-{method}.json"
    summary = js(p)[0]
    archive = f"results/T-007/runs/py312-pin/{method}.tar.gz"
    groups, lengths = score_rows(archive_records[archive])
    for fault, values in summary["bo_ca_loi"].items():
        if fault == "AVERAGE" or values is None:
            continue
        group = groups[fault]
        n = len(group)
        calculated = {"n": n, "AC@1": sum(pos <= 1 for pos in group) / n,
            "AC@3": sum(pos <= 3 for pos in group) / n, "AC@5": sum(pos <= 5 for pos in group) / n,
            "Avg@5": sum(sum(pos <= k for k in range(1, 6)) / 5 for pos in group) / n}
        for key in calculated:
            number("T-007", p, f"[0].bo_ca_loi.{fault}.{key}", values[key], calculated[key], key,
                archive + "!*/results/*.json", "group/count; unique service rank; sum hits then divide n")

# T019: CSV count/group/sum, including row count vs incident count warning.
census = cs("results/T-019/census-cases.csv")
summaries = js("results/T-019/census-summary.json")
for idx, summary in enumerate(summaries):
    subset = [x for x in census if x["dataset"] == summary["dataset"]]
    calc = {"cases": len(subset), "cells": len({(x["root"], x["fault"]) for x in subset}),
        "files": sum(len(x["files"].split("|")) for x in subset), "trace_cases": sum(int(x["trace"]) for x in subset),
        "log_cases": sum(int(x["log"]) for x in subset), "metric_cases": sum(int(x["metric"]) for x in subset),
        "root_cause_cases": sum(int(x["root_cause"]) for x in subset), "bytes": sum(int(x["bytes"]) for x in subset)}
    for key in calc:
        number("T-019", "results/T-019/census-summary.json", f"[{idx}].{key}", summary[key], calc[key], key,
            "results/T-019/census-cases.csv#" + summary["dataset"], "filter dataset; count/group or sum columns")
for key, actual in [("total_rows", len(t19rows)), ("prior_ledger_rows", len(cs("results/T-019/lineage/so-ca-da-nhin.csv"))),
        ("T019_inspected_cases", sum(x["source"].startswith("HF_RCAEval_T019_") for x in t19rows))]:
    number("T-019", "results/T-019/ledger-summary.json", key, t19summary[key], actual, key, t19path,
        "count rows using source/exposure, not incident denominator")
selected = []
for task in ["T-005", "T-006", "T-007", "T-019"]:
    pool = sorted([x for x in number_pool if x["task"] == task], key=lambda x: x["selection_sha256"])
    meanings = set()
    for x in pool:
        if x["meaning"] not in meanings:
            selected.append(x)
            meanings.add(x["meaning"])
        if len(meanings) == 5:
            break
    assert len(meanings) >= 5, (task, meanings)
write_csv("numeric-leaf-pool.csv", number_pool)
write_csv("numeric-check-selected.csv", selected)
write_csv("numeric-check-all.csv", number_pool)
numeric_failed = [x for x in number_pool if not x["ok"]]

checks = {"no_locked_reads": True, "no_raw_measurement_reads": True, "read_paths_are_frozen_results_only": True,
    "public_RCAEval_cases": len(public_ids), "RE2TT_public_cases": len(tt), "v1_allowlist": len(allowlist),
    "locked_public_complement": len(locked), "locked_TX2_count": sum(records[public_ids[c]]["factual_seen"] == "TX2" for c in locked),
    "locked_ran_method_count": sum(records[public_ids[c]]["ran_method"] for c in locked),
    "allowlist_whole_cells": 10, "T019_original_relation_rows": len(t19rows),
    "T019_union_identity_units": len(source_sets["T-019-ledger"]), "all_source_row_count": len(evidence_rows),
    "all_source_unique_identity_units": len(records), "sum_source_identity_counts": sum(map(len, source_sets.values())),
    "overlap_removal_count": sum(map(len, source_sets.values())) - len(records),
    "source_reconciliation_sum_new_equals_union": True, "unresolved_source_rows": len(unresolved),
    "unresolved_alias_relations": len(open_relations), "numeric_checks": len(number_pool), "numeric_failed": numeric_failed,
    "seeded_numeric_selected_per_task": dict(Counter(x["task"] for x in selected)),
    "input_files_read": len(used), "elapsed_seconds": round(time.perf_counter() - STARTED, 6),
    "limitations": ["Global union is proven-identity union; source-scoped local RE1OB to HF identity remains OPEN, not an exact biological incident total.",
        "A file/date/storage capture is not an incident. Units must not be added across datasets.",
        "No dev/test/holdout roles selected; public census is metadata evidence only.",
        "T005 method calls do not prove ranks were viewed; factual_seen remains TX1 unless later saved evidence supplies TX2.",
        "Nezha TT45 label rows do not prove45 unique physical injections: two rows share epoch with different textual times; keep OPEN.",
        "Dataset membership and canonical union ownership differ: local RE1OB125 includes40 FSE-owned identity aliases and85 new source-scoped units."]}
write_json("run-assertions.json", checks)
write_json("input-read-manifest.json", {"freeze_sha256": hashlib.sha256(FREEZE.read_bytes()).hexdigest(), "frozen_head": freeze["head"], "inputs_read": used})

lines = ["# Sổ ca đã nhìn — bằng chứng trung gian T-020", "", "Đơn vị union là identity có bằng chứng đã lưu. TX0 chỉ metadata/nhãn; TX1 số đo mô tả đã đọc; TX2 đã có kết quả phương pháp theo ca. T005 timing-only có ran_method=true nhưng không tự khẳng định đã thấy rank. Không chọn chính sách hay chia tập.", "",
    "735 ca RCAEval public được lấy từ HF catalog đã lưu; identity dùng content hash metric và Git oid inject. 60 RE2-TT suy từ census90 trừ allowlist30, không mở/đếm thư mục locked. Cả60 có factual_seen TX0 và không có ran_method.", "",
    f"T019 có {len(t19rows)} dòng quan hệ nhưng {len(source_sets['T-019-ledger'])} identity unit trong union đã chứng minh. Tổng row/case-source không phải số ca duy nhất. source-reconciliation.csv và source-intersections.csv giải thích từng nguồn và phần giao.", "",
    "T006 bổ sung125 local RE1OB;40 delay/loss (4 roots×2 faults×5 repeats) cùng SHA256 với fseOB đã được nối. Quan hệ local RE1OB↔HF RE1OB còn OPEN; không đẩy TX2 theo tên. T019 xác nhận toraiSS↔RE2SS90, toraiOB↔RE2OB90 và RE1SS125↔HF nội dung. T016 xác nhận TT bằng toàn bảng metric, không chỉ cùng tên/mốc.", "",
    "| Dataset | Đơn vị | Tổng | TX0 | TX1 | TX2 | Ô nhãn | Identity OPEN |", "|---|---|---:|---:|---:|---:|---:|---:|"]
for x in dataset_rows:
    lines.append(f"| {x['dataset']} | {x['units']} | {x['catalog_units']} | {x['TX0']} | {x['TX1']} | {x['TX2']} | {x['label_cells']} | {x['identity_open_units']} |")
lines += ["", "Census Nezha/Eadro dùng tuple entity+fault+inject timestamp. NezhaTT45 là label records; hai dòng cùng epoch nhưng text giờ tiêm khác giữ riêng, quan hệ OPEN. Bank dùng tuple level+component+timestamp+reason, chưa đọc telemetry; root là component/pod. DeepTraLog83 là storage capture/trace labels;82 có trace-ID census. AnoMod26 là experiment capture, mapping nhãn gốc OPEN. LEMMA có20 date/release captures,2 preprocessed đã đọc và18 chỉ metadata. Không cộng những đơn vị này như sự cố, không giả thành ô service×fault.", "",
    "dataset-census-membership.csv giữ census đầy đủ mỗi release/copy; dataset-membership-exposure.csv có local RE1OB125=40 identity fseOB+85 source-scoped units. Bảng trên là ownership của canonical union nên localRE1OB85 là phần tăng union, không phải tổng ca dataset. FSE propagation có10 injection folders,2 invalid markers và8 valid theo nguồn; không tự chọn dùng tất cả10.", "",
    f"Kiểm số: {len(number_pool)} leaf có phép tính đối chiếu, chọn SHA256(seed|task|path|key) tối thiểu5 nghĩa/task tại numeric-check-selected.csv. Giữ cả pool trước chọn. Có {len(numeric_failed)} số lệch/chưa tái lập đúng; xem run-assertions.json. Mọi số kết luận-trọng yếu census, sources, intersections đều tính lại count/group/sum.", "",
    "Root cần kiểm độc lập số trọng yếu trước dùng file cuối. Chưa quyết định, chưa khuyến nghị, chưa chia dev/test; chưa xem số đo mới TX0/TX1; không chạy script task cũ hay RCA/detector."]
(OUT / "02-so-ca-da-nhin.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps({k: v for k, v in checks.items() if k not in ["numeric_failed", "limitations"]}, ensure_ascii=False, indent=2))
if numeric_failed:
    print("NUMERIC_FAILURES", len(numeric_failed))
