"""Metadata/docs/code only. Never fetch a telemetry archive. Standard library only."""
import argparse
import csv
import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REV = "04376dcb99d4b0fd0c50850255c2c4f9ec9503c1"


def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def collect(run):
    run.mkdir(parents=True, exist_ok=False)
    manifest = {"started_utc": datetime.now(timezone.utc).isoformat(), "revision": REV,
                "scope": "public metadata, documentation, source code; zero telemetry archives", "sources": []}
    start = time.monotonic()
    def fetch(name, url, cap=8_000_000):
        item = {"id": name, "url": url, "requested_utc": datetime.now(timezone.utc).isoformat()}
        manifest["sources"].append(item)
        dump(run / "manifest.json", manifest)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "RCA-dataset-metadata-audit/1"})
            with urllib.request.urlopen(req, timeout=35) as response:
                payload = response.read(cap + 1)
                if len(payload) > cap:
                    raise ValueError("source exceeds byte cap")
                item.update(status=response.status, final_url=response.url,
                            content_type=response.headers.get("Content-Type"))
            path = run / "sources" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
            item.update(path=str(path.relative_to(run)).replace("\\", "/"), bytes=len(payload),
                        sha256=hashlib.sha256(payload).hexdigest())
            print(name, len(payload), flush=True)
            return payload
        except Exception as exc:
            item["error"] = str(exc)
            print(name, "FAILED", str(exc), flush=True)
            return None
        finally:
            dump(run / "manifest.json", manifest)
    fetch("github-tree.json", f"https://api.github.com/repos/FudanSELab/DeepTraLog/git/trees/{REV}?recursive=1")
    fetch("github-repo.json", "https://api.github.com/repos/FudanSELab/DeepTraLog")
    for path in ("README.md", "model/dataset.py", "model/main.py", "model/model.py", "model/utils.py", "model/requirements"):
        fetch(path.replace("/", "__"), f"https://raw.githubusercontent.com/FudanSELab/DeepTraLog/{REV}/{path}")
    fetch("author-site.html", "https://fudanselab.github.io/DeepTraLog/")
    fetch("paper.pdf", "https://cspengxin.github.io/publications/icse22-DeepTraLog.pdf")
    manifest.update(elapsed_seconds=round(time.monotonic()-start, 3),
                    downloaded_bytes=sum(x.get("bytes", 0) for x in manifest["sources"]))
    dump(run / "manifest.json", manifest)
    summarize(run)


def summarize(run):
    tree = json.loads((run / "sources/github-tree.json").read_text(encoding="utf-8"))
    assert tree["sha"] == REV and not tree["truncated"]
    files = [x for x in tree["tree"] if x["type"] == "blob"]
    assert len({x["path"] for x in files}) == len(files)
    def group(path):
        if re.fullmatch(r"TraceLogData/F\d+\.zip", path): return "fault_archives"
        if path.startswith("TraceLogData/normal/"): return "normal_archives"
        if path.startswith("TraceLogData/alllog/"): return "alllog_parts"
        if path.startswith("GraphData/"): return "graph_parts"
        if path.startswith("results/"): return "published_result_archives"
        return "code_docs"
    groups = {}
    for x in files:
        g = groups.setdefault(group(x["path"]), {"files": 0, "bytes": 0})
        g["files"] += 1
        g["bytes"] += x["size"]
    with (run / "inventory.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["path", "group", "bytes", "git_blob_sha", "downloaded"])
        writer.writeheader()
        for x in files:
            writer.writerow({"path": x["path"], "group": group(x["path"]), "bytes": x["size"],
                             "git_blob_sha": x["sha"], "downloaded": "no" if group(x["path"]) != "code_docs" else "see manifest"})
    dump(run / "count-summary.json", {"revision": REV, "scope": "Git tree file metadata, not archive members or incident census",
         "blob_count": len(files), "total_blob_bytes": sum(x["size"] for x in files), "groups": groups,
         "license_paths": [x["path"] for x in files if re.search(r"license|copying", x["path"], re.I)],
         "fault_archive_ids": [Path(x["path"]).stem for x in files if group(x["path"]) == "fault_archives"],
         "telemetry_archives_downloaded": 0, "telemetry_cases_inspected": 0,
         "raw_parent_quality": None, "root_label_census": None})


def verify(run):
    manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
    for item in manifest["sources"]:
        if "path" in item:
            payload = (run / item["path"]).read_bytes()
            assert len(payload) == item["bytes"]
            assert hashlib.sha256(payload).hexdigest() == item["sha256"]
    tree = json.loads((run / "sources/github-tree.json").read_text(encoding="utf-8"))
    for item in manifest["sources"]:
        if "raw.githubusercontent.com" in item["url"] and "path" in item:
            remote_path = item["url"].split(REV + "/", 1)[1]
            expected = next(x for x in tree["tree"] if x["path"] == remote_path)
            payload = (run / item["path"]).read_bytes()
            assert hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest() == expected["sha"]
    summary = json.loads((run / "count-summary.json").read_text(encoding="utf-8"))
    rows = list(csv.DictReader((run / "inventory.csv").open(encoding="utf-8")))
    assert len(rows) == summary["blob_count"]
    assert sum(int(x["bytes"]) for x in rows) == summary["total_blob_bytes"]
    for group, counts in summary["groups"].items():
        subset = [x for x in rows if x["group"] == group]
        assert len(subset) == counts["files"] and sum(int(x["bytes"]) for x in subset) == counts["bytes"]
    assert summary["telemetry_archives_downloaded"] == summary["telemetry_cases_inspected"] == 0
    print("PASS source hashes, Git blob hashes, complete metadata counts; zero telemetry", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", default="run-001")
    parser.add_argument("--sources", action="store_true")
    parser.add_argument("--validate-counts", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    run = BASE / "runs" / args.run
    if args.sources: collect(run)
    if args.validate_counts or args.verify: verify(run)
