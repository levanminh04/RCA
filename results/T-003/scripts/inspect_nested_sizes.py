"""Inspect XZ size indexes of the seven Eadro nested compressed members.

Archive bytes are fetched into memory because the server ignores Range.
No XZ decompression, TAR member access, metric/log/trace parsing or storage
of compressed archive payloads is performed. This is a metadata-only audit.
"""
import argparse
import concurrent.futures
import hashlib
import io
import json
from pathlib import Path
import sys
import time
import urllib.request
import zlib
from inspect_archive_sizes import ROOT, BASE, load, save, xz_index


class MetadataBuffer(io.BytesIO):
    def __init__(self, raw, request_audit):
        super().__init__(raw)
        self.size = len(raw)
        self.requests = [request_audit]


def inspect(item):
    begin = time.perf_counter()
    audit = {"requested_full_compressed_member_for_size_index": True}
    try:
        req = urllib.request.Request(item["url"], headers={"Accept-Encoding": "identity", "User-Agent": "T003-nested-archive-size-index/1.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read(item["download_bytes"] + 1)
            audit.update(status=response.status, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
        if len(raw) != item["download_bytes"]:
            raise ValueError("Compressed member byte count mismatch")
        if zlib.crc32(raw) != item["expected_crc32"]:
            raise ValueError("Compressed member CRC differs from outer ZIP metadata")
        result = xz_index(item, MetadataBuffer(raw, audit))
        result["compressed_member_bytes_fetched"] = len(raw)
        result["crc_matches_outer_zip"] = True
    except Exception as error:
        result = dict(item, status="error", error=repr(error), range_requests=[audit])
    result.update(full_elapsed_seconds=round(time.perf_counter() - begin, 3),
                  archive_payload_saved=False, xz_payload_decompressed=False, telemetry_rows_read=0)
    return result


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    if not args.run_id.replace("-", "").isalnum(): parser.error("Invalid run id")
    directory = BASE / "runs" / args.run_id
    directory.mkdir(parents=True, exist_ok=False)
    inventory = load("results/T-009/runs/run-001/inventory.json")
    items = []
    for x in inventory:
        if not x["key"].startswith("__MACOSX/") and x["key"].endswith((".tar.xz", ".txz")):
            items.append({"id": "eadro-nested-" + x["key"].replace("/", "--"), "task": "T-009", "variant": x["dataset"],
                          "path": x["key"], "url": x["links"]["content"], "download_bytes": x["size"],
                          "expected_crc32": x["crc"], "kind": "nested_xz"})
    total = sum(x["download_bytes"] for x in items)
    if total > 50_000_000 or any(x["download_bytes"] > 15_000_000 for x in items):
        raise ValueError("Metadata-index fallback exceeds explicit byte budget")
    save(directory / "request-plan.json", {"purpose": "XZ size index only; no compressed payload retained/decompressed", "planned_compressed_metadata_container_bytes": total, "items": items})
    print(json.dumps({"planned_compressed_bytes": total, "objects": len(items), "telemetry_rows_to_read": 0}), flush=True)
    start = time.perf_counter()
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for result in pool.map(inspect, items):
            results.append(result)
            save(directory / "nested-index-results.json", results)
    summary = {"successes": sum(x["status"] == "ok" for x in results), "failures_retained": sum(x["status"] != "ok" for x in results),
               "network_compressed_member_bytes": sum(x.get("compressed_member_bytes_fetched", 0) for x in results),
               "payload_files_saved": 0, "telemetry_rows_read": 0, "elapsed_seconds": round(time.perf_counter() - start, 3)}
    save(directory / "summary.json", summary)
    print(json.dumps(summary), flush=True)


if __name__ == "__main__": main()
