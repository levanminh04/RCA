"""Tính hai vế T9 từ dữ liệu dev gốc ở ba cửa sổ làm đổi kết cục."""
import gzip
import hashlib
import json
import sys
import time
from pathlib import Path

import psutil

from replay import ROOT, WORLDS, digest, encode

OUT = Path(__file__).resolve().parent
INDICES = (5, 13, 21)

sys.path[:0] = [str(ROOT / part) for part in ("results/T-048/scripts", "results/T-045/scripts")]
from chay import capture, dump
from chay_pha1 import tat_ha_toc
from m1 import adapter, chuoi, e4
from p3 import selector


def read(path):
    return json.loads(path.read_bytes())


def main(target):
    folder = OUT / target
    folder.mkdir()
    manifest = read(OUT / "manifest.json")
    plan = read(OUT / "pilot-plan.json")
    matrix = ROOT / "results/T-049/ma-tran.json"
    matrix_sha = read(ROOT / "results/T-049/runs/t6-001-seal.json")["matrix_sha256"]
    assert digest(matrix) == matrix_sha
    for name, sha in plan["sources"].items():
        assert digest(ROOT / name) == sha, name
    configs = {"S1": read(matrix)["K-b"]["K-thang-C"], "E6b": plan["config"]}
    index = OUT / "dau-vao-003/index.json"
    assert digest(index) == plan["index_sha256"]
    entries = read(index)
    allow = selector.nap_allowlist(ROOT / "results/T-022/allowlist-dev.json")
    universe = read(ROOT / "results/T-022/mappings/universe-re2tt-dev.json")["U"]
    contract = read(ROOT / "results/T-043/hop-dong.json")
    tat_ha_toc()
    process = psutil.Process()
    results = []
    for i in INDICES:
        print(f"{i}: start", flush=True)
        start = time.monotonic()
        entry = entries[i]
        job = entry["job"]
        assert entry["index"] == i and job["dataset"] == "RE2-TT" and job["window"] == "that"
        case = adapter.ca_re2tt(allow, job["opaque_id"], job["t"], ROOT, contract, universe)
        normalized = {key: case.get(key) for key in ("spans", "metrics", "logs", "inventory", "aliases", "params_ca")}
        input_sha = hashlib.sha256(dump(dict(normalized, t=job["t"])).encode()).hexdigest()
        del normalized
        assert input_sha == entry["normalized_input_sha256"], (i, "normalized input")
        saved = {}
        for name, config in configs.items():
            chuoi.CACHE = e4.CacheCong()
            begin = time.monotonic()
            record, trace, timing, effective = capture(case, job["t"], config, compact=True, input_sha256=input_sha)
            saved[name] = json.loads(dump(dict(record=record, trace=trace, timing=timing, effective=effective)))
            path = folder / f"{i:02d}-{name}.json.gz"
            with path.open("xb") as stream:
                stream.write(gzip.compress(encode(saved[name]), mtime=0))
            print(f"{i}: {name} native {time.monotonic() - begin:.3f}s", flush=True)

        original = OUT / f"ec2-001-download/ec2-001/{i:02d}"
        receipt = read(original / "complete.json")
        previous = original / receipt["attempt"] / "result.json"
        old_sha = manifest["outputs"][previous.relative_to(ROOT).as_posix()]["sha256"]
        assert digest(previous) == old_sha == receipt["files"]["result.json"]
        expected = read(previous)
        projected = OUT / "dau-vao-003" / entry["file"]
        assert digest(projected) == entry["sha256"]
        inputs = json.loads(gzip.decompress(projected.read_bytes()))["input"]
        for name, item in saved.items():
            record, trace = item["record"], item["trace"]
            assert record["status"] == inputs["status"] and not trace["capture_errors"], (i, name, "status")
            assert record["extra"]["canh"] == inputs["edges"], (i, name, "edges")
            assert record["inherited_by"] == inputs["inherited"] and trace["U"] == inputs["U"], (i, name, "U")
            assert record["region"] == expected["P"]["region"][name], (i, name, "region")
            for world, frame in zip(WORLDS, trace["xep"][:3], strict=True):
                for key in ("kenh", "F_I", "co_OK"):
                    assert frame[key] == inputs["frames"][world][key], (i, name, world, key)
                assert frame["m"] == (inputs["frames"][world]["m"] if name == "S1" else None)
                assert frame["ket_qua"] == expected[world][name], (i, name, world, "rank")
                assert record["worlds"][world]["blocks"] == expected[world][name]["blocks"]
                assert all(trace["world_state"][world][key] == value
                           for key, value in inputs["state"][world].items()), (i, name, world, "state")
        elapsed = time.monotonic() - start
        results.append({"index": i, "opaque_id": job["opaque_id"], "worlds": WORLDS,
                        "configurations": list(configs), "input_sha256": input_sha,
                        "seconds": elapsed, "peak_rss_bytes": process.memory_info().peak_wset,
                        "replay_sha256": old_sha})
        print(f"{i}: native/replay PASS ({elapsed:.3f}s)", flush=True)
    with (folder / "doi-chieu.json").open("xb") as stream:
        stream.write(encode({"scope": "dev-a", "selected_after_scoring": True, "rows": results}) + b"\n")


if __name__ == "__main__":
    main(sys.argv[1])
