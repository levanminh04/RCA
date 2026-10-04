"""Count RCAEval cases from public directory metadata only (Python stdlib).

Never reads local data/; never downloads telemetry or cases.parquet. Each run
uses a new output directory and preserves responses/errors for reproduction.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

HF_REPO = "phamquiluan/RCAEval"
HF_REVISION = "afeacb11bcc94dadfd1c8f483ee4377b2b8b614e"
TARGETS = {"re2tt": "RE2-TT", "re2ob": "RE2-OB", "re3tt": "RE3-TT", "re3ob": "RE3-OB"}
CASE_RE = re.compile(r"^(re[123](?:tt|ob|ss))_(.+)_([^_]+)_(\d+)$")


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def get(url, output, manifest, *, revision=None, max_bytes=2_000_000):
    request = urllib.request.Request(url, headers={"User-Agent": "RCA-T002-public-metadata/1.0"})
    entry = {"url": url, "revision": revision, "artifact": f"sources/{output.name}", "requested_at_utc": datetime.now(timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read(max_bytes + 1)
            if len(body) > max_bytes:
                raise ValueError(f"Metadata response exceeds {max_bytes} bytes")
            entry.update(status=response.status, resolved_url=response.geturl(), bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
            output.write_bytes(body)
            manifest.append(entry)
            return body, dict(response.headers)
    except Exception as error:
        entry.update(error=f"{type(error).__name__}: {error}")
        manifest.append(entry)
        raise


def csv_write(path, rows, fields):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    allowed = Path(__file__).resolve().parent
    output = args.output.resolve()
    if not output.is_relative_to(allowed):
        parser.error("Output must be below results/T-002, beside this script")
    output.mkdir(parents=True, exist_ok=False)
    sources = output / "sources"
    sources.mkdir()
    manifest = []
    run = {"started_at_utc": datetime.now(timezone.utc).isoformat(), "hf_revision": HF_REVISION, "mode": "public file-tree metadata only; no telemetry or cases.parquet contents"}
    try:
        # Hugging Face paginates using the response Link header. Retain every page.
        url = f"https://huggingface.co/api/datasets/{HF_REPO}/tree/{HF_REVISION}?recursive=true&expand=false&limit=1000"
        entries = []
        page = 1
        while url:
            body, headers = get(url, sources / f"hf-tree-page-{page:03}.json", manifest, revision=HF_REVISION)
            records = json.loads(body)
            if not isinstance(records, list):
                raise ValueError("Tree API did not return a list")
            entries.extend(records)
            link = headers.get("Link", headers.get("link", ""))
            match = re.search(r'<([^>]+)>;\s*rel="next"', link)
            url = match.group(1) if match else None
            page += 1
        paths = [x["path"] for x in entries]
        if len(paths) != len(set(paths)):
            raise ValueError("Duplicate paths across tree pages")
        write_json(output / "hf-tree.json", entries)
        directories = sorted(x["path"] for x in entries if x["type"] == "directory" and "/" not in x["path"])
        cases = []
        for directory in directories:
            match = CASE_RE.fullmatch(directory)
            if match:
                suite, root, fault, repeat = match.groups()
                cases.append({"case": directory, "suite": suite, "root_service": root, "fault": fault, "repeat": int(repeat)})
        target_cases = [x for x in cases if x["suite"] in TARGETS]
        csv_write(output / "cases-from-directories.csv", target_cases, ["case", "suite", "root_service", "fault", "repeat"])
        by_case = defaultdict(list)
        for entry in entries:
            if entry["type"] == "file" and "/" in entry["path"]:
                by_case[entry["path"].split("/", 1)[0]].append(entry)
        cells = []
        summaries = []
        modality_rows = []
        for suite, label in TARGETS.items():
            selected = [x for x in target_cases if x["suite"] == suite]
            roots = Counter(x["root_service"] for x in selected)
            faults = Counter(x["fault"] for x in selected)
            cell_groups = defaultdict(list)
            for case in selected:
                cell_groups[(case["root_service"], case["fault"])].append(case["repeat"])
            for (root, fault), repeats in sorted(cell_groups.items()):
                cells.append({"dataset": label, "root_service": root, "fault": fault, "n_cases": len(repeats), "repeat_ids": ",".join(map(str, sorted(repeats))), "unique_repeat_ids": len(set(repeats))})
            suite_files = [entry for case in selected for entry in by_case[case["case"]]]
            modalities = Counter(Path(x["path"]).name for x in suite_files)
            total = sum(x.get("size", 0) for x in suite_files)
            summaries.append({"dataset": label, "n_cases": len(selected), "n_root_services": len(roots), "root_services_and_case_counts": dict(sorted(roots.items())), "n_faults": len(faults), "faults_and_case_counts": dict(sorted(faults.items())), "n_observed_root_fault_cells": len(cell_groups), "possible_root_fault_cells": len(roots)*len(faults), "cell_repetition_min": min(map(len, cell_groups.values()), default=0), "cell_repetition_max": max(map(len, cell_groups.values()), default=0), "files": len(suite_files), "total_file_bytes": total, "total_file_MB_decimal": round(total/1_000_000, 3), "total_file_MiB": round(total/1024**2, 3), "file_counts": dict(sorted(modalities.items())), "missing_files_by_name": {name: sorted(case["case"] for case in selected if name not in {Path(x["path"]).name for x in by_case[case["case"]]}) for name in ("metrics.parquet", "traces.parquet", "logs.parquet", "inject_time.txt")}})
            for filename in sorted(modalities):
                files = [x for x in suite_files if Path(x["path"]).name == filename]
                modality_rows.append({"dataset": label, "file": filename, "n_files": len(files), "bytes": sum(x.get("size", 0) for x in files), "content_opened": False})
        csv_write(output / "root-fault-cells.csv", cells, ["dataset", "root_service", "fault", "n_cases", "repeat_ids", "unique_repeat_ids"])
        csv_write(output / "modality-sizes.csv", modality_rows, ["dataset", "file", "n_files", "bytes", "content_opened"])
        write_json(output / "count-summary.json", summaries)
        run.update(n_api_entries=len(entries), n_directories=len(directories), n_all_parsed_cases=len(cases), n_target_cases=len(target_cases))
        # Snapshot the dataset card and pinned GitHub README/LICENSE only.
        get(f"https://huggingface.co/datasets/{HF_REPO}/raw/{HF_REVISION}/README.md", sources / "hf-README.md", manifest, revision=HF_REVISION)
        body, _ = get("https://api.github.com/repos/phamquiluan/RCAEval/commits/main", sources / "github-main-commit.json", manifest)
        commit = json.loads(body)["sha"]
        run["github_revision"] = commit
        for name in ("README.md", "LICENSE"):
            get(f"https://raw.githubusercontent.com/phamquiluan/RCAEval/{commit}/{name}", sources / f"github-{name}", manifest, revision=commit)
        get("https://arxiv.org/html/2412.17015v2", sources / "paper-v2.html", manifest, revision="2412.17015v2")
        run["status"] = "success"
        print(json.dumps({"output": str(output), "summary": summaries, "run": run}, ensure_ascii=False, indent=2))
    except Exception as error:
        run.update(status="failed", error=f"{type(error).__name__}: {error}")
        print(run["error"], file=sys.stderr)
        raise
    finally:
        run["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
        run["downloaded_bytes"] = sum(x.get("bytes", 0) for x in manifest)
        write_json(output / "source-manifest.json", manifest)
        write_json(output / "run.json", run)


if __name__ == "__main__":
    main()
