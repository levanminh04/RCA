"""Chạy pilot, kiểm đọc lại cửa sổ đã lưu, rồi phát lại phần còn thiếu."""
import fcntl
import gzip
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

from replay import ROOT, WORLDS, digest, encode, run

OUT = Path(__file__).resolve().parent


def native(entry, data, expected, config, folder):
    sys.path[:0] = [str(ROOT / part) for part in ("results/T-048/scripts", "results/T-045/scripts")]
    from chay import capture, dump
    from chay_pha1 import tat_ha_toc
    from m1 import adapter
    from p3 import nezha, selector

    tat_ha_toc()
    job = entry["job"]
    oid = job["opaque_id"]
    contract = json.loads((ROOT / "results/T-043/hop-dong.json").read_bytes())
    if job["dataset"] == "RE2-TT":
        allow = selector.nap_allowlist(ROOT / "results/T-022/allowlist-dev.json")
        universe = json.loads((ROOT / "results/T-022/mappings/universe-re2tt-dev.json").read_bytes())["U"]
        t = job["t"]
        case = adapter.ca_re2tt(allow, oid, t, Path("/home/ubuntu/rca-t048/staging"), contract, universe)
    else:
        allow = nezha.nap_allowlist(ROOT / "results/T-026/allowlist-dev.json")
        case = adapter.ca_nezha(allow, oid, Path("/home/ubuntu/rca/T-032/repo"), contract)
        t = case["t"]
    normalized = {key: case.get(key) for key in ("spans", "metrics", "logs", "inventory", "aliases", "params_ca")}
    input_sha = hashlib.sha256(dump(dict(normalized, t=t)).encode()).hexdigest()
    assert input_sha == entry["normalized_input_sha256"], "normalized input"
    del normalized
    record, trace, timing, effective = capture(case, t, config, compact=True, input_sha256=input_sha)
    raw = json.loads(dump(trace))
    (folder / "native.json.gz").write_bytes(gzip.compress(dump({
        "record": record, "trace": trace, "timing": timing, "effective_sha256": effective
    }).encode(), mtime=0))
    assert not trace["capture_errors"]
    assert record["status"] == data["status"]
    assert encode(record["extra"]["canh"]) == encode(data["edges"])
    assert encode(record["inherited_by"]) == encode(data["inherited"])
    assert encode(raw["U"]) == encode(data["U"])
    assert record["region"] == expected["P"]["region"]["E6b"]
    for world, frame in zip(WORLDS, raw["xep"][:3], strict=True):
        for k in ("kenh", "F_I", "co_OK"):
            assert encode(frame[k]) == encode(data["frames"][world][k]), (world, k)
        assert frame["m"] is None
        assert encode(frame["ket_qua"]) == encode(expected[world]["E6b"]), (world, "rank")
        assert record["worlds"][world]["blocks"] == expected[world]["E6b"]["blocks"]
        assert all(raw["world_state"][world][k] == data["state"][world][k]
                   for k in ("N1", "V0", "valid_units"))


def read(path):
    return json.loads(path.read_bytes())


def window(entry, config, run_dir, input_dir, pilot):
    index = entry["index"]
    source = input_dir / entry["file"]
    assert source.stat().st_size == entry["bytes"] and digest(source) == entry["sha256"]
    provenance = {"input": entry["sha256"], "config": hashlib.sha256(encode(config)).hexdigest(),
                  "runner": digest(Path(__file__)), "replay": digest(OUT / "replay.py"),
                  "index": index, "pilot": pilot}
    slot = run_dir / f"{index:02d}"
    slot.mkdir(exist_ok=True)
    receipt = slot / "complete.json"
    if receipt.exists():
        proof = read(receipt)
        assert proof["provenance"] == provenance
        assert set(proof["files"]) == ({"result.json", "native.json.gz"} if pilot else {"result.json"})
        for name, sha in proof["files"].items():
            assert digest(slot / proof["attempt"] / name) == sha, (index, name)
        print(index, "reuse", flush=True)
        return "reuse"
    attempt = slot / f"attempt-{time.time_ns()}"
    attempt.mkdir()
    start = time.monotonic()
    payload = json.loads(gzip.decompress(source.read_bytes()))
    replay = run(payload["input"], payload["baseline"])
    (attempt / "result.json").write_bytes(encode(replay))
    if pilot:
        native(entry, payload["input"], replay, config, attempt)
    files = {p.name: digest(p) for p in attempt.iterdir()}
    pending = attempt / "receipt.json"
    pending.write_bytes(encode({"files": files, "attempt": attempt.name, "provenance": provenance,
                                "seconds": time.monotonic() - start}))
    os.replace(pending, receipt)
    print(index, "complete", time.monotonic() - start, flush=True)
    return "complete"


def main(input_dir, run_dir, mode="run"):
    input_dir, run_dir = OUT / input_dir, OUT / run_dir
    run_dir.mkdir(exist_ok=True)
    plan = read(OUT / "pilot-plan.json")
    assert digest(input_dir / "index.json") == plan["index_sha256"]
    for name, sha in plan["sources"].items():
        assert digest(ROOT / name) == sha, name
    entries = read(input_dir / "index.json")
    config = plan["config"]
    pilot = [entries[i] for i in plan["pilot"]]
    if mode == "verify-pilot":
        for row in pilot:
            assert (run_dir / f"{row['index']:02d}" / "complete.json").is_file()
            assert window(row, config, run_dir, input_dir, True) == "reuse"
        return
    assert mode == "run"
    with (run_dir / "lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        for row in pilot:
            window(row, config, run_dir, input_dir, True)
        subprocess.run([sys.executable, "-B", __file__, input_dir.name, run_dir.name,
                        "verify-pilot"], check=True)
        print("pilot + verified resume PASS", flush=True)
        for row in entries:
            if row["index"] not in plan["pilot"]:
                window(row, config, run_dir, input_dir, False)
        print("82 windows complete", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
