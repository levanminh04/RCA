"""Read public archive indexes to estimate disk use without opening telemetry.

Only ZipFile.infolist is used: no member is decompressed or read. Nested XZ
footer/index sizes are parsed, not XZ payloads. Servers ignoring Range are
closed before reading their response bodies. Every success/failure is kept.
"""
import argparse
import concurrent.futures
import csv
import hashlib
import io
import json
from pathlib import Path
import struct
import sys
import threading
import time
import urllib.parse
import urllib.request
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "results/T-003"
PER_READ = 4_000_000
TOTAL_BUDGET = 20_000_000
METER = {"bytes": 0}
LOCK = threading.Lock()


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class RangeReader(io.RawIOBase):
    def __init__(self, url, size):
        self.url, self.size, self.position = url, size, 0
        self.requests = []

    def readable(self): return True
    def seekable(self): return True
    def tell(self): return self.position

    def seek(self, offset, whence=0):
        value = offset if whence == 0 else self.position + offset if whence == 1 else self.size + offset
        if value < 0 or value > self.size: raise ValueError("Seek outside archive")
        self.position = value
        return value

    def read(self, n=-1):
        n = min(self.size - self.position, n if n >= 0 else self.size - self.position)
        if n == 0: return b""
        if n > PER_READ: raise ValueError("Metadata read exceeds announced per-read limit")
        start, end = self.position, self.position + n - 1
        req = urllib.request.Request(self.url, headers={"Range": f"bytes={start}-{end}", "Accept-Encoding": "identity", "User-Agent": "T003-archive-index-audit/1.0"})
        audit = {"start": start, "end": end, "requested_bytes": n}
        self.requests.append(audit)
        with urllib.request.urlopen(req, timeout=20) as response:
            audit.update(status=response.status, content_range=response.headers.get("Content-Range"))
            if response.status != 206 or response.headers.get("Content-Range") != f"bytes {start}-{end}/{self.size}":
                raise ValueError("Server did not honor exact Range; response body not read")
            with LOCK:
                if METER["bytes"] + n > TOTAL_BUDGET:
                    raise ValueError("Total archive-index read budget reached")
                METER["bytes"] += n
            raw = response.read(n + 1)
            if len(raw) != n: raise ValueError("Range body size mismatch")
            audit.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
        self.position = end + 1
        return raw


def zip_index(item):
    began = time.perf_counter()
    result = dict(item, status="error")
    stream = RangeReader(item["url"], item["download_bytes"])
    try:
        with zipfile.ZipFile(stream) as archive:
            entries = [{"path": x.filename, "compressed_bytes": x.compress_size, "uncompressed_bytes": x.file_size,
                        "crc32": x.CRC, "compression_method": x.compress_type, "directory": x.is_dir()}
                       for x in archive.infolist()]
        result.update(status="ok", members=entries, member_count=len(entries),
                      uncompressed_member_bytes=sum(x["uncompressed_bytes"] for x in entries),
                      compressed_member_bytes=sum(x["compressed_bytes"] for x in entries),
                      scope="central directory only; no member opened or decompressed")
    except Exception as error:
        result.update(error=repr(error))
    result.update(range_requests=stream.requests, elapsed_seconds=round(time.perf_counter() - began, 3))
    print(item["id"] + ": " + result["status"], flush=True)
    return result


def vint(raw, pos):
    value = 0
    for n in range(9):
        b = raw[pos]; pos += 1
        value |= (b & 127) << (7 * n)
        if b < 128: return value, pos
    raise ValueError("XZ variable integer too long")


def xz_index(item, stream_override=None):
    began = time.perf_counter()
    result = dict(item, status="error")
    stream = stream_override if stream_override is not None else RangeReader(item["url"], item["download_bytes"])
    try:
        stream.seek(-12, 2); footer = stream.read(12)
        if footer[10:] != b"YZ": raise ValueError("XZ footer missing; padding or another format needs inspection")
        if zlib.crc32(footer[4:10]) != struct.unpack("<I", footer[:4])[0]: raise ValueError("XZ footer CRC mismatch")
        index_size = (struct.unpack("<I", footer[4:8])[0] + 1) * 4
        stream.seek(stream.size - 12 - index_size); index = stream.read(index_size)
        if index[0] != 0 or zlib.crc32(index[:-4]) != struct.unpack("<I", index[-4:])[0]: raise ValueError("XZ index CRC mismatch")
        count, pos = vint(index, 1)
        records = []
        for _ in range(count):
            unpadded, pos = vint(index, pos); uncompressed, pos = vint(index, pos)
            records.append({"unpadded_block_bytes": unpadded, "uncompressed_block_bytes": uncompressed})
        if any(index[pos:-4]): raise ValueError("Unexpected XZ index padding")
        calculated_size = 12 + sum((x["unpadded_block_bytes"] + 3) // 4 * 4 for x in records) + index_size + 12
        if calculated_size != stream.size: raise ValueError("Not verified as a single complete XZ stream")
        stream.seek(0); header = stream.read(12)
        if header[:6] != b"\xfd7zXZ\x00" or header[6:8] != footer[8:10]: raise ValueError("XZ header/footer flags mismatch")
        result.update(status="ok", block_count=count, uncompressed_stream_bytes=sum(x["uncompressed_block_bytes"] for x in records),
                      single_stream_verified=True, scope="XZ index only; uncompressed stream is TAR including headers/padding, not exact extracted member sizes")
    except Exception as error:
        result.update(error=repr(error))
    result.update(range_requests=stream.requests, elapsed_seconds=round(time.perf_counter() - began, 3))
    print(item["id"] + ": " + result["status"], flush=True)
    return result


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    if not args.run_id.replace("-", "").isalnum(): parser.error("Invalid run id")
    run = BASE / "runs" / args.run_id
    run.mkdir(parents=True, exist_ok=False)
    began = time.perf_counter()
    items = []
    lemma = load("results/T-011/runs/run-001/inspection-proposal.json")
    for i, x in enumerate(lemma["selected_preprocessed_files"]):
        url = "https://huggingface.co/datasets/Lemma-RCA-NEC/" + x["dataset"] + "/resolve/" + x["revision"] + "/" + urllib.parse.quote(x["path"])
        items.append({"id": f"lemma-{i+1}", "task": "T-011", "variant": x["dataset"], "path": x["path"], "url": url, "download_bytes": int(x["bytes"]), "kind": "zip"})
    for x in load("results/T-009/sources/zenodo.json")["files"]:
        items.append({"id": "eadro-" + x["key"][:2], "task": "T-009", "variant": x["key"][:2], "path": x["key"],
                      "url": x["links"]["self"], "download_bytes": x["size"], "kind": "zip"})
    deep_revision = load("results/T-010/runs/run-001/count-summary.json")["revision"]
    with (ROOT / "results/T-010/runs/run-001/inventory.csv").open(encoding="utf-8") as fh:
        for x in csv.DictReader(fh):
            if x["group"] in ("fault_archives", "normal_archives") or x["path"] == "GraphData/graph_data.zip":
                items.append({"id": "deep-" + x["path"].replace("/", "--"), "task": "T-010", "variant": x["group"], "path": x["path"],
                              "url": f"https://raw.githubusercontent.com/FudanSELab/DeepTraLog/{deep_revision}/" + urllib.parse.quote(x["path"]),
                              "download_bytes": int(x["bytes"]), "kind": "zip"})
    nested = []
    for x in load("results/T-009/runs/run-001/inventory.json"):
        if not x["key"].startswith("__MACOSX/") and x["key"].endswith((".txz", ".tar.xz")):
            nested.append({"id": "eadro-nested-" + x["key"].replace("/", "--"), "task": "T-009", "variant": x["dataset"], "path": x["key"],
                           "url": x["links"]["content"], "download_bytes": x["size"], "kind": "nested_xz"})
    save(run / "request-plan.json", {"scope": "public archive index metadata; no telemetry members", "per_read_limit": PER_READ, "total_metadata_byte_budget": TOTAL_BUDGET, "items": items + nested})
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(zip_index if x["kind"] == "zip" else xz_index, x): x for x in items + nested}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
            save(run / "archive-index-results.json", results)
    summary = {"scope": "index metadata only", "telemetry_members_opened": 0, "archive_index_bytes_read": METER["bytes"],
               "elapsed_seconds": round(time.perf_counter() - began, 3), "successes": sum(x["status"] == "ok" for x in results),
               "failures_retained": sum(x["status"] != "ok" for x in results)}
    save(run / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False), flush=True)


if __name__ == "__main__": main()
