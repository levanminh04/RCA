"""Fetch pinned public metadata, label-only files and code. Never download ZIP data."""
import argparse
import ast
import csv
import hashlib
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REV = "c560d8cc39c19f04c9ae74fac2404b1e5e8c3b4d"
DATASETS = {
    "Product_Review_Original": "63aa4abe7dd7217d9b0b108894c7d893e2b29aef",
    "Product_Review_Preprocessed": "df25484004e50483de6f6756c3a4d7ab03174b83",
    "Cloud_Computing_Original": "9e5ad23fa390f6b596f41be014233fe446679bcd",
    "Cloud_Computing_Preprocessed": "03f82a2c4b16afe09e9315def9f5d6990427000a",
}
CODE_PATHS = ["README.md", "LICENSE", "IT/data preprocessing/README.md",
    "IT/data preprocessing/metric_json2npy.py", "IT/data preprocessing/json2message.py",
    "Baseline/metric_only/RCA_methods_metric.py", "Baseline/FastPC/baseline_evaluation.py",
    "Baseline/Nezha/20240124/20240124-fault_list.json", "Baseline/Nezha/20240124/root_cause_hipster.json",
    "OT/data_preprocessing/Readme.md", "OT/data_preprocessing/SWaT/data_segment.py",
    "OT/data_preprocessing/WADI/data_segment.py", "Baseline/SWAT&WADI/pyrca-evaluation.py",
    "Baseline/SWAT&WADI/baro-evaluation.py"]


def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


def local_code(path):
    return "code__" + path.replace("/", "__").replace(" ", "_").replace("&", "_")


def collect(run):
    run.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    manifest = {"started_utc": datetime.now(timezone.utc).isoformat(), "github_revision": REV,
                "dataset_revisions": DATASETS, "scope": "metadata/docs/code and separate labels only; zero telemetry archives", "sources": []}
    def fetch(name, url, cap=8_000_000):
        item = {"id": name, "url": url, "requested_utc": datetime.now(timezone.utc).isoformat()}
        manifest["sources"].append(item)
        dump(run / "manifest.json", manifest)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "RCA-dataset-metadata-audit/1"})
            with urllib.request.urlopen(req, timeout=35) as response:
                payload = response.read(cap+1)
                if len(payload) > cap: raise ValueError("source exceeds byte cap")
                item.update(status=response.status, final_url=response.url,
                            content_type=response.headers.get("Content-Type"), link_header=response.headers.get("Link"))
            path = run / "sources" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
            item.update(path=str(path.relative_to(run)).replace("\\", "/"), bytes=len(payload), sha256=hashlib.sha256(payload).hexdigest())
            print(name, len(payload), flush=True)
            return payload
        except Exception as exc:
            item["error"] = str(exc)
            print(name, "FAILED", str(exc), flush=True)
            return None
        finally: dump(run / "manifest.json", manifest)
    fetch("github-tree.json", f"https://api.github.com/repos/lemma-rca/rca_baselines/git/trees/{REV}?recursive=1")
    for path in CODE_PATHS:
        fetch(local_code(path), f"https://raw.githubusercontent.com/lemma-rca/rca_baselines/{REV}/"+urllib.parse.quote(path, safe="/"))
    for name, revision in DATASETS.items():
        fetch(name+"__info.json", f"https://huggingface.co/api/datasets/Lemma-RCA-NEC/{name}/revision/{revision}")
        fetch(name+"__tree.json", f"https://huggingface.co/api/datasets/Lemma-RCA-NEC/{name}/tree/{revision}?recursive=true&limit=1000")
        fetch(name+"__README.md", f"https://huggingface.co/datasets/Lemma-RCA-NEC/{name}/raw/{revision}/README.md")
    for name, url in {
        "paper-v4.html": "https://arxiv.org/html/2406.05375v4",
        "author-site.html": "https://lemma-rca.github.io/",
        "author-catalog.html": "https://lemma-rca.github.io/docs/data.html",
        "author-current-site.html": "https://www.lemmarca.info/",
        "itrust-terms.html": "https://www.sutd.edu.sg/itrust/itrust-labs/datasets/terms-of-usage/",
        "itrust-swat.html": "https://www.sutd.edu.sg/itrust/itrust-labs/datasets/dataset-characteristics/swat/",
        "itrust-wadi.html": "https://www.sutd.edu.sg/itrust/itrust-labs/datasets/dataset-characteristics/wadi/",
    }.items(): fetch(name, url)
    manifest.update(elapsed_seconds=round(time.monotonic()-start, 3), downloaded_bytes=sum(x.get("bytes",0) for x in manifest["sources"]))
    dump(run / "manifest.json", manifest)
    summarize(run)


def literal_assignments(path, wanted):
    out = {}
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8-sig"))):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in wanted:
                    try: out[target.id] = ast.literal_eval(node.value)
                    except (ValueError, TypeError): pass
    return out


def summarize(run):
    summary = {"scope": "HF public file inventory, not ZIP member census", "datasets": {},
               "telemetry_archives_downloaded": 0, "telemetry_cases_inspected": 0}
    rows = []
    for name, rev in DATASETS.items():
        info = json.loads((run / "sources" / (name+"__info.json")).read_text(encoding="utf-8"))
        tree = json.loads((run / "sources" / (name+"__tree.json")).read_text(encoding="utf-8"))
        assert info["sha"] == rev
        assert len({x["path"] for x in tree}) == len(tree)
        files = [x for x in tree if x["type"] == "file"]
        archives = [x for x in files if x["path"].endswith(".zip")]
        dates = sorted({Path(x["path"]).stem for x in archives})
        log_dates = sorted({Path(x["path"]).stem for x in archives if x["path"].startswith("Log Data/")})
        metric_dates = sorted({Path(x["path"]).stem for x in archives if x["path"].startswith("Metrics Data/")})
        summary["datasets"][name] = {"revision": rev, "tree_items": len(tree), "files": len(files), "all_file_bytes": sum(x["size"] for x in files),
            "archive_files": len(archives), "archive_bytes": sum(x["size"] for x in archives), "date_tokens": dates,
            "log_archive_dates": log_dates, "metric_archive_dates": metric_dates,
            "card_license": info.get("cardData",{}).get("license"), "root_label_census": None}
        for x in files:
            rows.append({"dataset": name, "revision": rev, "path": x["path"], "bytes": x["size"],
                         "oid": x["oid"], "lfs_sha256": x.get("lfs",{}).get("oid", ""), "telemetry_downloaded": "no"})
    with (run / "inventory.csv").open("w", newline="", encoding="utf-8") as fh:
        writer=csv.DictWriter(fh, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    fault = json.loads((run / "sources" / local_code("Baseline/Nezha/20240124/20240124-fault_list.json")).read_text())
    labels = {"cloud_20240124_separate_label": fault,
       "fastpc_label_constants": literal_assignments(run / "sources" / local_code("Baseline/FastPC/baseline_evaluation.py"), {"folders", "reals"}),
       "ot_evaluation_label_constants": literal_assignments(run / "sources" / local_code("Baseline/SWAT&WADI/pyrca-evaluation.py"), {"reals"}),
       "wadi_segment_constants": literal_assignments(run / "sources" / local_code("OT/data_preprocessing/WADI/data_segment.py"), {"attack_time_ranges"}),
       "scope": "literal code and standalone label only; code never executed; mapping to current archives not fully verified"}
    ot = labels["ot_evaluation_label_constants"]["reals"]
    labels["counts"] = {"separate_fault_records": sum(len(x) for x in fault.values()),
       "fastpc_label_groups": len(labels["fastpc_label_constants"]["reals"]),
       "ot_label_groups": len(ot), "ot_multiroot_groups": sum(len(x)>1 for x in ot),
       "ot_unique_entity_strings": len(set(y for x in ot for y in x)),
       "wadi_segment_intervals": len(labels["wadi_segment_constants"]["attack_time_ranges"])}
    record = fault["2024-01-24"][0]
    epoch_utc = datetime.fromtimestamp(int(record["inject_timestamp"]), timezone.utc)
    text_as_utc = datetime.fromisoformat(record["inject_time"]).replace(tzinfo=timezone.utc)
    dump(run / "label-time-check.json", {
        "source": local_code("Baseline/Nezha/20240124/20240124-fault_list.json"),
        "original_record": record, "epoch_utc": epoch_utc.isoformat(),
        "text_timezone_declared": False,
        "epoch_minus_text_if_interpreted_utc_seconds": (epoch_utc-text_as_utc).total_seconds(),
        "conclusion": "OPEN: text has no timezone; do not infer UTC or apply PPTX JST correction to this JSON. No label was changed."})
    dump(run / "labels-from-code.json", labels)
    dump(run / "count-summary.json", summary)


def verify(run):
    manifest=json.loads((run/"manifest.json").read_text(encoding="utf-8"))
    tree=json.loads((run/"sources/github-tree.json").read_text(encoding="utf-8"))
    assert tree["sha"] == REV and not tree["truncated"]
    for item in manifest["sources"]:
        if "path" not in item: continue
        payload=(run/item["path"]).read_bytes()
        assert len(payload)==item["bytes"] and hashlib.sha256(payload).hexdigest()==item["sha256"]
        assert not (item.get("link_header") and 'rel="next"' in item["link_header"]), "HF pagination not exhausted"
        if "raw.githubusercontent.com" in item["url"]:
            path=urllib.parse.unquote(item["url"].split(REV+"/",1)[1])
            expected=next(x for x in tree["tree"] if x["path"]==path)
            assert hashlib.sha1(b"blob "+str(len(payload)).encode()+b"\0"+payload).hexdigest()==expected["sha"]
    summary=json.loads((run/"count-summary.json").read_text(encoding="utf-8"))
    rows=list(csv.DictReader((run/"inventory.csv").open(encoding="utf-8")))
    for name, result in summary["datasets"].items():
        items=[x for x in rows if x["dataset"]==name]
        assert len(items)==result["files"] and sum(int(x["bytes"]) for x in items)==result["all_file_bytes"]
        archived=[x for x in items if x["path"].endswith(".zip")]
        assert len(archived)==result["archive_files"] and sum(int(x["bytes"]) for x in archived)==result["archive_bytes"]
    labels=json.loads((run/"labels-from-code.json").read_text(encoding="utf-8"))
    other=literal_assignments(run/"sources"/local_code("Baseline/SWAT&WADI/baro-evaluation.py"),{"reals"})
    assert other["reals"]==labels["ot_evaluation_label_constants"]["reals"]
    timing=json.loads((run/"label-time-check.json").read_text(encoding="utf-8"))
    record=labels["cloud_20240124_separate_label"]["2024-01-24"][0]
    assert datetime.fromisoformat(timing["epoch_utc"]).timestamp()==int(record["inject_timestamp"])
    assert summary["telemetry_archives_downloaded"]==summary["telemetry_cases_inspected"]==0
    print("PASS hashes, Git blob hashes, complete HF inventories, matching OT label constants; zero telemetry")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run",default="run-001")
    parser.add_argument("--sources",action="store_true")
    parser.add_argument("--validate-counts",action="store_true")
    parser.add_argument("--verify",action="store_true")
    args=parser.parse_args(); run=BASE/"runs"/args.run
    if args.sources: collect(run)
    if args.validate_counts or args.verify: verify(run)
