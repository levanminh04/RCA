"""Audit saved T-003 source evidence offline; this is not RCA or telemetry.

The checkpoint report explicitly leaves the research package incomplete.
Never scans data/, never overwrites a prior verification run.
"""
import argparse
from collections import Counter
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import urllib.parse

REPO = Path(__file__).resolve().parents[3]
BASE = REPO / "results" / "T-003"
TASKS = ("T-008", "T-009", "T-010", "T-011", "T-012")


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sources():
    manifests, rows = [], []
    for task in TASKS:
        task_dir = REPO / "results" / task
        run_dir = task_dir / "runs" / "run-001"
        path = run_dir / ("source-manifest.json" if task == "T-012" else "manifest.json")
        m = read(path)
        manifests.append({"task": task, "path": path.relative_to(REPO).as_posix(), "sha256": digest(path),
                          "revision": m.get("revision", m.get("github_revision")),
                          "dataset_revisions": m.get("dataset_revisions", {}),
                          "network_bytes": m.get("network_bytes", m.get("downloaded_bytes", sum(x.get("bytes", 0) for x in m.get("items", []))))})
        for item in m.get("sources", m.get("items", [])):
            out = dict(item, task=task)
            if "path" in item:
                parent = task_dir if task in ("T-008", "T-009", "T-012") else run_dir
                p = (parent / item["path"]).resolve()
                if task_dir not in p.parents:
                    raise ValueError("Source path outside task results")
                raw = p.read_bytes()
                if len(raw) != item["bytes"] or hashlib.sha256(raw).hexdigest() != item["sha256"]:
                    raise ValueError("Source bytes/hash mismatch: " + str(p))
                out["repository_path"] = p.relative_to(REPO).as_posix()
            rows.append(out)
    return {"stage": "source-metadata checkpoint", "telemetry_read": False,
            "created_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            "manifests": manifests, "sources": rows}


def census(task):
    task_dir = REPO / "results" / task
    run_dir = task_dir / "runs" / "run-001"
    summary, rows, cells = (read(run_dir / (name + ".json")) for name in ("summary", "labels", "cells"))
    raw_counts = Counter()
    for source in sorted({r["source"] for r in rows}):
        raw = read(task_dir / source)
        dataset = next(r["dataset"] for r in rows if r["source"] == source)
        if task == "T-008":
            raw_counts[dataset] += sum(len(group) for group in raw.values())
        else:
            raw_counts[dataset] += len(raw["faults"])
    checks = []
    for dataset, values in summary.items():
        subset = [r for r in rows if r["dataset"] == dataset]
        table = Counter((r["service"], r["fault"]) for r in subset)
        saved = {(r["service"], r["fault"]): r["count"] for r in cells if r["dataset"] == dataset}
        checks.append({"task": task, "dataset": dataset, "raw_label_records": raw_counts[dataset],
                       "derived_events": len(subset), "root_count": len({r["service"] for r in subset}),
                       "cells": len(table),
                       "ok": raw_counts[dataset] == values["events"] == len(subset)
                             and saved == dict(table)
                             and len(table) == values["cells"]
                             and len({r["service"] for r in subset}) == values["root_count"]})
    return checks


def links(path):
    text = path.read_text(encoding="utf-8")
    missing = []
    for target in re.findall(r"(?<!!)\[[^\]\n]+\]\(([^\n]+?)\)", text):
        target = target.strip().strip("<>")
        if urllib.parse.urlparse(target).scheme or target.startswith("#"):
            continue
        target = urllib.parse.unquote(target.split("#", 1)[0])
        p = (path.parent / target).resolve()
        # Only task results are followed. Other references are reported as scope.
        if (REPO / "results") not in p.parents:
            continue
        if not p.exists():
            missing.append(target)
    return {"path": path.relative_to(REPO).as_posix(), "missing_local_links": missing}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", action="store_true", required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.run_id):
        parser.error("Invalid run id")
    out_dir = BASE / "runs" / args.run_id
    out_dir.mkdir(parents=True, exist_ok=False)
    report = {"package_complete": False, "stage": "source-metadata checkpoint",
              "open": ["telemetry permission and inspection", "T-012 source comparison/cards/census", "final G1 synthesis and independent review"]}
    report["disk_free_bytes_at_check"] = shutil.disk_usage(REPO).free
    try:
        unified = sources()
        save(BASE / "source-manifest.json", unified)
        report["source_manifest"] = {"path": "results/T-003/source-manifest.json", "sha256": digest(BASE / "source-manifest.json"),
                                     "snapshots": sum("repository_path" in row for row in unified["sources"]),
                                     "source_failures_retained": sum("repository_path" not in row for row in unified["sources"]),
                                     "network_bytes": sum(row["network_bytes"] for row in unified["manifests"])}
        commands = []
        for task in TASKS:
            script = REPO / "results" / task / "scripts" / ("capture_sources.py" if task == "T-012" else "collect_metadata.py")
            tail = ["--run", "run-001", "--verify"] if task == "T-012" else ["--verify", "--validate-counts"]
            completed = subprocess.run([sys.executable, "-B", str(script), *tail], cwd=REPO, text=True, capture_output=True, encoding="utf-8")
            commands.append({"task": task, "exit_code": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr})
        report["offline_checks"] = commands
        report["independent_raw_label_census"] = census("T-008") + census("T-009")
        card_checks, link_checks = [], []
        for task, expected in (("T-008", 2), ("T-009", 2), ("T-010", 1), ("T-011", 2)):
            p = REPO / "results" / task / "the-dataset.md"
            if not p.exists():
                card_checks.append({"task": task, "exists": False, "ok": False})
                continue
            text = p.read_text(encoding="utf-8")
            counts = {str(i): len(re.findall(r"^## " + str(i) + r"\. ", text, flags=re.M)) for i in range(1, 11)}
            card_checks.append({"task": task, "sections_per_number": counts, "ok": all(n == expected for n in counts.values())})
            link_checks.append(links(p))
            plan = p.parent / "inspection-plan.md"
            if plan.exists(): link_checks.append(links(plan))
        for p in BASE.glob("*.md"):
            link_checks.append(links(p))
        report["card_structure"] = card_checks
        report["local_links"] = link_checks
        ot = REPO / "results" / "T-011" / "catalog-ot.md"
        ot_text = ot.read_text(encoding="utf-8")
        ot_counts = {str(i): len(re.findall(r"^## " + str(i) + r"\. ", ot_text, flags=re.M)) for i in range(1, 11)}
        card_checks.append({"task": "T-011 OT catalog", "sections_per_number": ot_counts, "ok": all(n == 1 for n in ot_counts.values())})
        link_checks.append(links(ot))
        nz = read(REPO / "results/T-008/runs/run-001/summary.json")
        ez = read(REPO / "results/T-009/sources/zenodo.json")
        deep = read(REPO / "results/T-010/runs/run-001/count-summary.json")["groups"]
        lemma = read(REPO / "results/T-011/runs/run-001/inspection-proposal.json")
        nz_bytes = sum(x["proposed_bytes"] for x in nz.values())
        ez_files = ez.get("files", [])
        ez_bytes = sum(x["size"] for x in ez_files)
        deep_raw = deep["fault_archives"]["bytes"] + deep["normal_archives"]["bytes"]
        deep_raw_graph = deep_raw + deep["graph_parts"]["bytes"]
        lemma_bytes = sum(int(x["bytes"]) for x in lemma["selected_preprocessed_files"])
        if lemma_bytes != lemma["selected_zip_bytes"]:
            raise ValueError("LEMMA selected file byte sum mismatch")
        report["proposed_download_bytes"] = {
            "status": "CANDIDATE; not approved or downloaded", "source": "saved inventories/proposals",
            "nezha_raw_all": nz_bytes, "eadro_two_zip": ez_bytes,
            "deep_raw": deep_raw, "deep_raw_plus_graph": deep_raw_graph,
            "deep_optional_alllog": deep["alllog_parts"]["bytes"],
            "lemma_four_sample_zip": lemma_bytes,
            "nezha_eadro_deep_raw_graph": nz_bytes + ez_bytes + deep_raw_graph,
            "including_lemma_sample": nz_bytes + ez_bytes + deep_raw_graph + lemma_bytes,
            "including_lemma_and_optional_alllog": nz_bytes + ez_bytes + deep_raw_graph + lemma_bytes + deep["alllog_parts"]["bytes"]}
        report["checkpoint_verified"] = (all(x["exit_code"] == 0 for x in commands)
                                         and all(x["ok"] for x in report["independent_raw_label_census"])
                                         and all(x["ok"] for x in card_checks)
                                         and not any(x["missing_local_links"] for x in link_checks))
    except Exception as error:
        report["checkpoint_verified"] = False
        report["error"] = repr(error)
    save(out_dir / "verification.json", report)
    print(json.dumps({"checkpoint_verified": report["checkpoint_verified"], "package_complete": False,
                      "report": (out_dir / "verification.json").relative_to(REPO).as_posix()}, ensure_ascii=False))
    raise SystemExit(0 if report["checkpoint_verified"] else 1)


if __name__ == "__main__":
    main()
