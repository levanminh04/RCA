"""C-c/C-g từ bản ghi P3 đã ghim, chỉ dùng phiếu và thứ hạng trước nhãn."""
import gzip
import json
import math
import sys
from collections import Counter
from pathlib import Path

from replay import ROOT, digest, encode
from m1 import doi_chung
from p3.danh_gia import khoi_tu_ban_ghi

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent / "T-049/scripts"))
from kiem_tai_su_dung import records


def read(path):
    return json.loads(path.read_bytes())


def verified(path, proof):
    assert path.stat().st_size == proof["bytes"], path
    assert digest(path) == proof["sha256"], path
    return read(path)


def load_sources():
    re = ROOT / "results/T-024"
    nz = ROOT / "results/T-026"
    re_manifest = read(re / "work/danh-sach-tep-cuoi.json")
    nz_manifest = read(nz / "runs/session-005/handoff-manifest.json")
    tables = {}
    for dataset, folder, manifest in (
            ("RE2-TT", re, {p["path"]: p for p in re_manifest["results_files"]}),
            ("Nezha-OB", nz, nz_manifest["files"])):
        path = folder / "ban-ghi-dua-vao-cham.json"
        table = verified(path, manifest[path.relative_to(ROOT).as_posix()])
        rows = table["records"] if dataset == "RE2-TT" else table["tables"]["main"]["records"]
        variants = {"baro": "native", "simplerca": "native" if dataset == "RE2-TT" else "M4",
                    "tracerca": "native" if dataset == "RE2-TT" else "finite"}
        seen = {}
        for row in rows:
            method = row["method"]
            if variants.get(method) != row["variant"]:
                continue
            record_path = ROOT / row["path"]
            proof = manifest[record_path.relative_to(ROOT).as_posix()]
            assert row["sha256"] == proof["sha256"], row["path"]
            record = verified(record_path, proof)
            assert all(record[k] == row[k] for k in ("opaque_id", "method", "seed"))
            assert record["mode"] == "a"
            key = row["opaque_id"], method
            assert key not in seen
            seen[key] = row, record
        assert len(seen) == (90 if dataset == "RE2-TT" else 66)
        tables[dataset] = seen
    return tables


def groups(blocks):
    return [sorted(group) for block in blocks for group in block["groups"]]


def votes(record):
    ranking = record["entity_ranking"]
    grouped = groups(khoi_tu_ban_ghi(record))
    by_entity = {r["entity"]: r for r in ranking}
    assert len(by_entity) == len(ranking) == record["sets"]["returned"]
    assert set(by_entity) == {e for g in grouped for e in g}
    values = {}
    for i, group in enumerate(grouped):
        keys = []
        for entity in group:
            row = by_entity[entity]
            assert row["tie_group"] == i
            value, = row["key"]
            assert math.isfinite(value) and value >= 0 and value == int(value)
            keys.append(value)
            values[entity] = int(value)
        assert len(set(keys)) == 1
    return values


def main(input_dir, target):
    sources = load_sources()
    rows, counts = [], Counter()
    for entry in read(input_dir / "index.json"):
        job = entry["job"]
        if job["window"] != "that":
            continue
        oid, dataset = job["opaque_id"], job["dataset"]
        base = records(entry["native"]["path"], entry["native"], {entry["source_config"]})[entry["source_config"]]
        source = input_dir / entry["file"]
        assert digest(source) == entry["sha256"]
        graph = json.loads(gzip.decompress(source.read_bytes()))["input"]["edges"]
        picked, rankings = {}, {}
        for method in ("baro", "simplerca", "tracerca"):
            row, record = sources[dataset][oid, method]
            windows = record["window"]
            actual = ({w: [int(s) * 10**9 for s in windows[w]] for w in ("N", "A")}
                      if dataset == "RE2-TT" else {w: windows[w + "_ns"] for w in ("N", "A")})
            assert all(actual[w] == base["window"][w] for w in ("N", "A")), (oid, method)
            assert record["status"] in ("OK", "NO_EVIDENCE", "ERROR")
            picked[method] = {"path": row["path"], "sha256": row["sha256"], "status": record["status"]}
            rankings[method] = None if record["status"] == "ERROR" else groups(khoi_tu_ban_ghi(record))
        simple = sources[dataset][oid, "simplerca"][1]
        if simple["status"] == "ERROR":
            cg = {"trang_thai": "ERROR", "blocks": []}
            counts["error"] += 1
        else:
            cg = doi_chung.cg(votes(simple), rankings["simplerca"], [tuple(e) for e in graph])
            if cg["trang_thai"] == "NO_EVIDENCE":
                counts["no_evidence"] += 1
            elif cg.get("ghi_chu") == "tong_s_g_bang_0":
                counts["fallback"] += 1
            else:
                counts["positive"] += 1
                counts["changed"] += groups(cg["blocks"]) != rankings["simplerca"]
        cc = doi_chung.cc(rankings, k=60)
        rows.append({"opaque_id": oid, "dataset": dataset, "sources": picked,
                     "simple_groups": rankings["simplerca"], "C-c": cc, "C-g": cg})
    assert len(rows) == 52
    with target.open("xb") as stream:
        stream.write(encode({"rows": rows, "counts": counts,
                             "degenerate": not counts["error"] and not counts["changed"]}))


if __name__ == "__main__":
    main(OUT / sys.argv[1], OUT / sys.argv[2])
