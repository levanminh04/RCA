"""Xác minh từng đầu ra EC2 và khóa bản ghi pha 1 trước ghép nhãn."""
import gzip
import hashlib
import json
import sys
from pathlib import Path

from controls import groups, read, records
from replay import ROOT, WORLDS, digest, encode

OUT = Path(__file__).resolve().parent
CONFIGS = ("S1", "S0", "E6b", "C-c", "C-g")


def write(path, value):
    with path.open("xb") as stream:
        stream.write(encode(value) + b"\n")


def main(input_dir, received, controls, target):
    plan_path = OUT / "pilot-plan.json"
    plan = read(plan_path)
    assert digest(input_dir / "index.json") == plan["index_sha256"]
    for name, sha in plan["sources"].items():
        assert digest(ROOT / name) == sha, name
    assert len(list(received.glob("*/complete.json"))) == 82
    assert any("pilot + verified resume PASS" in p.read_text(encoding="utf-8")
               and "82 windows complete" in p.read_text(encoding="utf-8")
               for p in received.glob("controller-*.log"))
    control = {r["opaque_id"]: r for r in read(controls)["rows"]}
    rows, sidecars = [], []
    for e in read(input_dir / "index.json"):
        index, job = e["index"], e["job"]
        slot = received / f"{index:02d}"
        receipt = read(slot / "complete.json")
        proof = receipt["provenance"]
        assert proof["input"] == e["sha256"] and proof["index"] == index
        assert proof["pilot"] == (index in plan["pilot"])
        assert proof["runner"] == digest(OUT / "run_ec2.py") and proof["replay"] == digest(OUT / "replay.py")
        assert proof["config"] == hashlib.sha256(encode(plan["config"])).hexdigest()
        assert set(receipt["files"]) == ({"result.json", "native.json.gz"} if proof["pilot"] else {"result.json"})
        attempt = slot / receipt["attempt"]
        for name, sha in receipt["files"].items():
            assert digest(attempt / name) == sha, (index, name)
        source = input_dir / e["file"]
        assert digest(source) == e["sha256"]
        data = json.loads(gzip.decompress(source.read_bytes()))["input"]
        replay = read(attempt / "result.json")
        assert set(replay) == set(WORLDS)
        sidecars.append({"job": job, "index": index, "replay": (attempt / "result.json").relative_to(ROOT).as_posix(),
                         "sha256": receipt["files"]["result.json"], "U": data["U"],
                         "input": source.relative_to(ROOT).as_posix(), "input_sha256": e["sha256"],
                         "observed": sorted({k["thuc_the"] for k in data["frames"]["P"]["kenh"]}),
                         "status": data["status"]})
        if job["window"] != "that":
            continue
        rec = records(e["native"]["path"], e["native"], {e["source_config"]})[e["source_config"]]
        for cid in CONFIGS:
            oid = job["opaque_id"]
            if cid in ("S1", "S0", "E6b"):
                blocks = {w: replay[w][cid]["blocks"] for w in WORLDS}
                status = rec["status"]
                extra = {k: rec["extra"][k] for k in ("G_N", "kenh_co_the_gioi")}
            else:
                method = control[oid][cid]
                blocks = {w: method["blocks"] if w == "P" else [] for w in WORLDS}
                status = method["trang_thai"]
                extra = {}
            for world in WORLDS:
                assert len([e for g in groups(blocks[world]) for e in g]) == len(
                    {e for g in groups(blocks[world]) for e in g})
            rows.append({"config_id": cid, "opaque_id": oid, "status": status, "blocks": blocks["P"],
                         "verdict": rec["verdict"] if extra else None, "extra": extra,
                         "worlds": {w: {"blocks": blocks[w]} for w in WORLDS}})
    assert len(rows) == 52 * len(CONFIGS) and len(sidecars) == 82
    target.mkdir()
    file = target / "ban-ghi.jsonl"
    with file.open("xb") as stream:
        for row in rows:
            stream.write(encode(row) + b"\n")
    write(target / "pha1.json", {"tep": file.name, "sha256": digest(file),
                                "so_ban_ghi": len(rows), "so_ca": 52, "cau_hinh": sorted(CONFIGS)})
    write(target / "sidecars.json", sidecars)
    sources = [input_dir / "index.json", plan_path, controls,
               file, target / "pha1.json", target / "sidecars.json"]
    write(target / "seal.json", {p.relative_to(ROOT).as_posix(): digest(p) for p in sources})


if __name__ == "__main__":
    main(*(OUT / arg for arg in sys.argv[1:]))
