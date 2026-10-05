"""Independent metadata-only validation; never import the builder or read data/."""
import csv
import hashlib
import io
import json
import time
from collections import Counter, defaultdict
from pathlib import Path

STARTED = time.perf_counter()
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]


def rows(path):
    return list(csv.DictReader(path.open(encoding="utf-8-sig", newline="")))


def saved(path):
    assert path.startswith("results/") and "locked" not in path
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


ledger = rows(OUT / "02-so-ca-da-nhin.csv")
units = {r["identity"]: r for r in ledger}
assert len(units) == len(ledger)
evidence = rows(OUT / "exposure-evidence.csv")
groups = defaultdict(list)
for r in evidence:
    groups[r["identity"]].append(r)
assert set(groups) == set(units)
for identity, source_rows in groups.items():
    assert units[identity]["factual_seen"] == max(r["factual_seen"] for r in source_rows)
    assert units[identity]["ran_method"] == str(any(r["ran_method"] == "True" for r in source_rows))
sources = defaultdict(set)
for r in evidence:
    sources[r["source"]].add(r["identity"])
assert len(set.union(*sources.values())) == len(units)
reconciliation = rows(OUT / "source-reconciliation.csv")
assert sum(int(r["new_to_union"]) for r in reconciliation) == len(units)
for r in rows(OUT / "source-intersections.csv"):
    assert int(r["intersection_identity_units"]) == len(sources[r["source_a"]] & sources[r["source_b"]])

hf = saved("results/T-002/public-metadata/run-002/hf-tree.json")
catalog_cases = {r["path"] for r in hf if r["type"] == "directory" and "/" not in r["path"] and r["path"].startswith(("re1", "re2", "re3"))}
public_rows = [r for r in ledger if r["case"] in catalog_cases]
assert len(catalog_cases) == len(public_rows) == 735
tt = {r["path"] for r in hf if r["type"] == "directory" and r["path"].startswith("re2tt_")}
dev = set(saved("results/T-017/allowlist.json"))
locked = tt - dev
assert len(tt) == 90 and len(dev) == 30 and len(locked) == 60
locked_rows = [r for r in public_rows if r["case"] in locked]
locked_ids = {r["identity"] for r in locked_rows}
assert len(locked_ids) == 60
assert all(r["factual_seen"] == "TX0" and r["ran_method"] == "False" and r["ranking_seen"] == "False" and r["detector_seen"] == "False" for r in locked_rows)
assert not any(r["identity"] in locked_ids and (r["factual_seen"] == "TX2" or r["ran_method"] == "True") for r in evidence)
assert not any(r["identity"] in locked_ids and r["source"] not in ["T-002-public-census"] for r in evidence)

# Reconstruct T019 union directly using source fingerprints and saved content crosswalk.
t19 = rows(ROOT / "results/T-019/so-ca-da-nhin.csv")
assert len(t19) == 1245
crosswalk = {(r["source"].lower(), r["local_case"]): r["public_case"] for r in saved("results/T-019/lineage/public-metric-comparisons.json")
    if r["inject_value_equal"] and r["finite_time_content_equal"] and r["value_columns_different"] == 0}
local = {(r["source"].lower(), r["case"]): r for r in saved("results/T-019/lineage/local-file-manifest.json")}
t19union = set()
for r in t19:
    source = r["source"].lower()
    key = (source, r["case"])
    if key in crosswalk:
        t19union.add("public:" + crosswalk[key])
    elif key in local:
        x = local[key]
        metric = x["files"].get("simple_data.csv", x["files"].get("simple_metrics.csv", x["files"].get("data.csv")))
        t19union.add("local:" + x["inject_time"] + ":" + metric["sha256"])
    elif r["case"] in catalog_cases:
        t19union.add("public:" + r["case"])
    else:
        assert r["public_case"] in catalog_cases, r
        t19union.add("public:" + r["public_case"])
assert len(t19union) == len(sources["T-019-ledger"]) == 435

membership = rows(OUT / "dataset-census-membership.csv")
local_re1 = [r for r in membership if r["dataset"] == "RE1-OB-local-Zenodo"]
fse_ob = [r for r in membership if r["dataset"] == "BARO-FSE-OB"]
assert len(local_re1) == 125 and len(fse_ob) == 100
assert len({r["identity"] for r in local_re1} & {r["identity"] for r in fse_ob}) == 40
bank = rows(ROOT / "results/T-012/runs/bank-label-reproduce-002/record.csv")
assert len(bank) == 136 and len({(r["component"], r["reason"]) for r in bank}) == 52
bank_rows = [r for r in ledger if r["dataset"] == "OpenRCA-Bank"]
assert len(bank_rows) == 136 and all(r["factual_seen"] == "TX0" for r in bank_rows)
nezha = saved("results/T-008/runs/run-001/labels.json")
assert Counter(r["dataset"] for r in nezha) == {"TT": 45, "OB": 56}
assert len([r for r in ledger if r["dataset"] == "Nezha-TT"]) == 45
eadro = saved("results/T-009/runs/run-001/labels.json")
assert Counter(r["dataset"] for r in eadro) == {"TT": 81, "SN": 36}
numeric = rows(OUT / "numeric-check-all.csv")
assert len(numeric) == 1762 and all(r["ok"] == "True" for r in numeric)
selected = rows(OUT / "numeric-check-selected.csv")
assert Counter(r["task"] for r in selected) == {"T-005": 5, "T-006": 5, "T-007": 5, "T-019": 5}
for task in ["T-005", "T-006", "T-007", "T-019"]:
    group = [r for r in selected if r["task"] == task]
    assert len({r["meaning"] for r in group}) == 5
    for r in group:
        assert r["selection_sha256"] == hashlib.sha256(f"20261004|{task}|{r['path']}|{r['key']}".encode()).hexdigest()

freeze = saved("results/T-020/trung-gian/input-freeze.json")
frozen = {r["path"]: r for r in freeze["inputs"]}
manifest = json.loads((OUT / "input-read-manifest.json").read_text())
for path, meta in manifest["inputs_read"].items():
    assert path.startswith("results/") and "/locked/" not in path
    actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
    assert actual == meta["sha256"] == frozen[path]["sha256"]
result = {"status": "pass", "public_RCAEval_cases": 735, "locked_public_ids": 60, "locked_result_exposure_rows": 0,
    "T019_relational_rows": 1245, "T019_union_identity_units": 435, "local_RE1OB_members": 125,
    "local_RE1OB_FSEOB_proven_intersection": 40, "Bank_labels": 136, "Bank_cells": 52,
    "Nezha_label_rows": 101, "Eadro_incident_labels": 117, "numeric_checks": len(numeric),
    "unique_identity_units_mixed_units_not_incident_denominator": len(units),
    "source_sets_union": len(units), "frozen_inputs_rehashed": len(manifest["inputs_read"]),
    "elapsed_seconds": round(time.perf_counter() - STARTED, 6)}
(OUT / "independent-assertions.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
