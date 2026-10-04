"""Capture an explicit list of official documents/metadata, never data files.

Run with py -3 -B. Each run is retained, including HTTP failures. --verify
checks saved bytes offline and does not contact any server.
"""
import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = Path(__file__).resolve().parents[1]
HOSTS = {"arxiv.org", "zenodo.org", "api.github.com"}
LIMIT_PER_SOURCE = 2_500_000


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def capture(item, directory):
    began = time.perf_counter()
    out = dict(item, fetched_at_utc=dt.datetime.now(dt.timezone.utc).isoformat())
    parsed = urllib.parse.urlparse(item["url"])
    if parsed.hostname not in HOSTS or parsed.scheme != "https":
        raise ValueError("URL outside source allowlist")
    if parsed.hostname == "zenodo.org" and not parsed.path.startswith("/api/records/"):
        raise ValueError("Only record metadata may be fetched from Zenodo")
    request = urllib.request.Request(item["url"], headers={"User-Agent": "T012-source-metadata-audit/1.0", "Accept": "application/json,text/html"})
    try:
        with urllib.request.urlopen(request, timeout=35) as response:
            final = urllib.parse.urlparse(response.geturl())
            if final.hostname not in HOSTS:
                raise ValueError("Redirect outside source allowlist")
            if final.hostname == "zenodo.org" and "/files/" in final.path:
                raise ValueError("Redirect to data file is forbidden")
            raw = response.read(LIMIT_PER_SOURCE + 1)
            if len(raw) > LIMIT_PER_SOURCE:
                raise ValueError("Source exceeds announced per-source byte limit")
            suffix = ".json" if item["kind"].endswith("metadata") else ".html"
            path = directory / (item["id"] + suffix)
            path.write_bytes(raw)
            out.update(status="ok", http_status=response.status, final_url=response.geturl(), content_type=response.headers.get("Content-Type"), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), path=path.relative_to(BASE).as_posix())
    except (OSError, ValueError, urllib.error.HTTPError) as error:
        out.update(status="error", error_type=type(error).__name__, error=str(error))
    out["elapsed_seconds"] = round(time.perf_counter() - began, 3)
    return out


def summaries(manifest):
    rows = []
    for item in manifest["items"]:
        if item["status"] != "ok" or item["kind"] != "zenodo_metadata":
            continue
        data = json.loads((BASE / item["path"]).read_text(encoding="utf-8"))
        meta = data.get("metadata", {})
        files = data.get("files", [])
        if isinstance(files, dict):
            files = list(files.get("entries", {}).values())
        rows.append({
            "source_id": item["id"], "record_id": data.get("id"),
            "title": meta.get("title"), "publication_date": meta.get("publication_date"),
            "version": meta.get("version"), "license": meta.get("license"),
            "doi": data.get("doi"), "links": data.get("links", {}),
            "file_count": len(files),
            "file_bytes_sum": sum(f.get("size", 0) for f in files),
            "files": [{"key": f.get("key"), "bytes": f.get("size"), "checksum": f.get("checksum")} for f in files],
            "scope": "metadata only; file payloads not downloaded",
            "source_path": item["path"]
        })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True, help="new run id; never overwrites an existing run")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if not args.run.replace("-", "").replace("_", "").isalnum():
        parser.error("run id must be alphanumeric, hyphen or underscore")
    run_dir = BASE / "runs" / args.run
    if args.verify:
        manifest = json.loads((run_dir / "source-manifest.json").read_text(encoding="utf-8"))
        checks = []
        for item in manifest["items"]:
            if item["status"] != "ok":
                continue
            path = (BASE / item["path"]).resolve()
            if BASE not in path.parents:
                raise ValueError("Snapshot path outside task results")
            raw = path.read_bytes()
            checks.append({"id": item["id"], "ok": len(raw) == item["bytes"] and hashlib.sha256(raw).hexdigest() == item["sha256"]})
        calculated = summaries(manifest)
        saved = json.loads((run_dir / "record-summary.json").read_text(encoding="utf-8"))
        ok = all(row["ok"] for row in checks) and calculated == saved
        print(json.dumps({"ok": ok, "snapshot_checks": checks, "record_summary_matches": calculated == saved}, ensure_ascii=False))
        raise SystemExit(0 if ok else 1)
    run_dir.mkdir(parents=True, exist_ok=False)
    source_dir = run_dir / "sources"
    source_dir.mkdir()
    inputs = json.loads((BASE / "source-list.json").read_text(encoding="utf-8"))
    begin = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        items = list(pool.map(lambda item: capture(item, source_dir), inputs["items"]))
    manifest = {"scope": inputs["scope"], "run_id": args.run, "elapsed_seconds": round(time.perf_counter() - begin, 3), "items": items}
    dump(run_dir / "source-manifest.json", manifest)
    dump(run_dir / "record-summary.json", summaries(manifest))
    print(json.dumps({"run_id": args.run, "sources_ok": sum(i["status"] == "ok" for i in items), "sources_failed": sum(i["status"] == "error" for i in items), "downloaded_source_bytes": sum(i.get("bytes", 0) for i in items), "elapsed_seconds": manifest["elapsed_seconds"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
