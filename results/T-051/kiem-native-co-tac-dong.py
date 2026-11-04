"""Kiểm hồi cứu native các nhánh có tác động ở T11/T12."""
import gzip
import hashlib
import importlib.metadata
import json
import os
import platform
import sys
import time
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from run_t11 import OUT, ROOT, digest, encoded, read, save, source

sys.path[:0] = [str(ROOT / p) for p in ("results/T-048/scripts", "results/T-045/scripts")]
import psutil
from chay import capture, dump
from chay_pha1 import tat_ha_toc
from m1 import adapter, chuoi, e4
from m1_danh_gia import pha2
from p3 import selector

JOBS = ((55, "E9", False), (55, "E9", True), (43, "T12", True))


def pin_original(path, manifest):
    expected = manifest["outputs"][path.relative_to(ROOT).as_posix()]
    assert path.stat().st_size == expected["bytes"]
    assert digest(path) == expected["sha256"], path


def main(run):
    started = time.perf_counter()
    tat_ha_toc()
    entries, base = source()
    original = read(OUT / "manifest.json")
    contract = read(ROOT / "results/T-043/hop-dong.json")
    allow = selector.nap_allowlist(ROOT / "results/T-022/allowlist-dev.json")
    universe = read(ROOT / "results/T-022/mappings/universe-re2tt-dev.json")["U"]
    target = OUT / run
    target.mkdir()
    process = psutil.Process()
    save(target / "command.json", {
        "jobs": JOBS, "runner_sha256": digest(__file__),
        "original_manifest_sha256": digest(OUT / "manifest.json"),
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "selected_after_scoring": True, "python": sys.version,
        "platform": platform.platform(),
        "versions": {p: importlib.metadata.version(p)
                     for p in ("numpy", "scipy", "pandas", "pyarrow", "drain3", "psutil")},
        "environment": {k: os.environ.get(k) for k in
                        ("PYTHONPATH", "PYTHONHASHSEED", "OPENBLAS_NUM_THREADS", "PYTHONIOENCODING")},
    })
    comparisons = []
    case, previous = None, None
    for index, stage, enabled in JOBS:
        begin = time.perf_counter()
        job = entries[index]["job"]
        assert job["dataset"] == "RE2-TT" and job["window"] == "that"
        folder = target / f"{index:02d}-{stage}-{int(enabled)}"
        folder.mkdir()
        if previous != index:
            case = adapter.ca_re2tt(allow, job["opaque_id"], job["t"], ROOT, contract, universe)
            chuoi.CACHE = e4.CacheCong()
            previous = index
        normalized = {k: case.get(k) for k in
                      ("spans", "metrics", "logs", "inventory", "aliases", "params_ca")}
        input_sha = hashlib.sha256(dump(dict(normalized, t=job["t"])).encode()).hexdigest()
        del normalized
        expected_path = OUT / ("t11-001" if stage == "E9" else "t12-001") / f"{index:02d}.json"
        pin_original(expected_path, original)
        expected = pha2.giai_ma_json(read(expected_path))
        assert input_sha == expected["normalized_input_sha256"]
        config = deepcopy(base)
        config["bat_tat"][stage] = enabled
        method_case = case
        if stage == "T12":
            path = ROOT / expected["static"]["source"]
            pin_original(path, {"outputs": original["sources"]})
            static = {"revision": expected["static"]["source"],
                      "canh": [[edge["source"], edge["target"]] for edge in read(path)["edges"]]}
            method_case = dict(case, params_ca=dict(case["params_ca"], canh_tinh=static))
        save(folder / "input.json", {
            "index": index, "opaque_id": job["opaque_id"], "input_sha256": input_sha,
            "expected_input_sha256": expected["normalized_input_sha256"], "configuration": config,
            "static": method_case.get("params_ca", {}).get("canh_tinh"),
            "expected_output": expected_path.relative_to(ROOT).as_posix(),
            "expected_output_sha256": digest(expected_path),
        })
        record, trace, timing, effective = capture(
            method_case, job["t"], config, compact=True, input_sha256=input_sha)
        native = {"record": record, "trace": trace, "timing": timing, "effective": effective}
        with (folder / "native.json.gz").open("xb") as stream:
            stream.write(gzip.compress(dump(native).encode("utf-8"), mtime=0))
        assert not trace["capture_errors"] and record["status"] in ("OK", "NO_EVIDENCE")
        mismatches, counts = [], {}
        for i, world in enumerate(pha2.WORLDS):
            frame = trace["xep"][i]
            old = expected["worlds"][world]
            checks = {
                "F_I": (frame["F_I"], old["effect"][enabled]["F_I"]),
                "m": (frame["m"], old["m"][enabled]),
                "rank": (frame["ket_qua"], old["rank"][enabled]),
                "V0": (trace["world_state"][world]["V0"], old["verdict"][enabled]),
            }
            if world == "P":
                checks["region"] = (record["region"], old["region"][enabled])
                checks["inheritance"] = (record["inherited_by"], old["effect"][enabled]["inherited_by"])
                if stage == "T12":
                    controls = expected["controls"][enabled]
                    checks["controls"] = ({k: record["extra"]["doi_chung"][k] for k in controls}, controls)
            for field, (actual, wanted) in checks.items():
                if encoded(actual) != encoded(wanted):
                    mismatches.append({"world": world, "field": field, "actual": actual, "expected": wanted})
            counts[world] = {
                "fields_compared": len(checks),
                "changed_F_I_in_saved_pair": sum(
                    value != old["effect"][1]["F_I"][name]
                    for name, value in old["effect"][0]["F_I"].items()),
                "native_tier1": sum(tier == 1 for tier in frame["ket_qua"]["tang"].values()),
            }
        row = {
            "index": index, "stage": stage, "enabled": enabled, "status": record["status"],
            "input_sha256": input_sha, "mismatches": mismatches, "worlds": counts,
            "native_sha256": digest(folder / "native.json.gz"), "timing": timing,
            "elapsed_seconds": time.perf_counter() - begin,
            "peak_process_rss_bytes_since_start": process.memory_info().peak_wset,
            "finished_utc": datetime.now(timezone.utc).isoformat(),
        }
        save(folder / "comparison.json", row)
        print(index, stage, enabled, round(row["elapsed_seconds"], 3),
              "mismatches", len(mismatches), flush=True)
        assert not mismatches, (index, stage)
        comparisons.append(row)
    assert comparisons[1]["worlds"]["P"]["changed_F_I_in_saved_pair"] == 2
    assert comparisons[2]["worlds"]["P"]["changed_F_I_in_saved_pair"] == 4
    save(target / "summary.json", {
        "PASS": True, "comparisons": comparisons, "elapsed_seconds": time.perf_counter() - started,
        "selected_after_scoring": True,
        "scope": "retrospective native parity, no new selection or score",
        "original_prelabel_pilot_not_restored": True,
    })


if __name__ == "__main__":
    main(sys.argv[1])
