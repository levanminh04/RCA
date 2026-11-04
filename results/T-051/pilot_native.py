"""Đối chiếu hai vế T11 với đường chạy M1 trên chính laptop, không ghép nhãn."""
import hashlib
import sys
import time
from copy import deepcopy

from run_t11 import OUT, ROOT, digest, encoded, read, save, source

sys.path[:0] = [str(ROOT / p) for p in ("results/T-048/scripts", "results/T-045/scripts")]
import psutil
from chay import capture, dump
from chay_pha1 import tat_ha_toc
from m1 import adapter, chuoi, e4
from m1_danh_gia import pha2
from p3 import nezha, selector


def main(replay_run, name, stage="E9"):
    tat_ha_toc()
    target = OUT / name
    target.mkdir()
    replay = OUT / replay_run
    plan = read(replay / "plan.json")
    indices = plan["indices"]
    entries, base = source()
    save(target / "plan.json", {"indices": indices, "replay_plan": digest(replay / "plan.json"),
                                "runner": digest(__file__), "python": sys.version})
    contract = read("results/T-043/hop-dong.json")
    process = psutil.Process()
    for index in indices:
        begin = time.monotonic()
        expected = pha2.giai_ma_json(read(replay / f"{index:02d}.json"))
        job = entries[index]["job"]
        oid = job["opaque_id"]
        if job["dataset"] == "RE2-TT":
            allow = selector.nap_allowlist(ROOT / "results/T-022/allowlist-dev.json")
            universe = read("results/T-022/mappings/universe-re2tt-dev.json")["U"]
            t = job["t"]
            case = adapter.ca_re2tt(allow, oid, t, ROOT, contract, universe)
        else:
            allow = nezha.nap_allowlist(ROOT / "results/T-026/allowlist-dev.json")
            case = adapter.ca_nezha(allow, oid, ROOT, contract)
            t = case["t"]
        normalized = {k: case.get(k) for k in ("spans", "metrics", "logs", "inventory", "aliases", "params_ca")}
        input_sha = hashlib.sha256(dump(dict(normalized, t=t)).encode()).hexdigest()
        del normalized
        save(target / f"{index:02d}-input.json", {
            "actual": input_sha, "expected": expected["normalized_input_sha256"]})
        assert input_sha == expected["normalized_input_sha256"], (index, "normalized input")
        chuoi.CACHE = e4.CacheCong()
        for enabled in ((True,) if stage == "T12" else (False, True)):
            config = deepcopy(base)
            config["bat_tat"][stage] = enabled
            method_case = case
            if stage == "T12":
                config["bat_tat"]["E9"] = plan["E9"]
                path = expected["static"]["source"]
                static = {"revision": path, "canh": [
                    [e["source"], e["target"]] for e in read(path)["edges"]]}
                method_case = dict(case, params_ca=dict(case["params_ca"], canh_tinh=static))
            record, trace, timing, effective = capture(
                method_case, t, config, compact=True, input_sha256=input_sha)
            if trace["capture_errors"] or record["status"] not in ("OK", "NO_EVIDENCE"):
                save(target / f"{index:02d}-{int(enabled)}-error.json", {
                    "index": index, "status": record["status"], "error": record["error"],
                    "capture_errors": trace["capture_errors"]})
                raise ValueError((index, record["status"], record["error"]))
            native = pha2.giai_ma_json(read(replay / f"{index:02d}.json"))["worlds"]
            mismatches = []
            for i, world in enumerate(pha2.WORLDS):
                frame = trace["xep"][i]
                old = native[world]
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
                        control = expected["controls"][enabled]
                        checks["controls"] = ({k: record["extra"]["doi_chung"][k] for k in control}, control)
                for field, (actual, want) in checks.items():
                    if encoded(actual) != encoded(want):
                        mismatches.append({"world": world, "field": field,
                                           "actual": actual, "expected": want})
            save(target / f"{index:02d}-{int(enabled)}.json", {
                "index": index, stage: enabled, "status": record["status"],
                "capture_errors": trace["capture_errors"], "mismatches": mismatches,
                "timing": timing, "effective": effective, "seconds": time.monotonic() - begin,
                "peak_rss": getattr(process.memory_info(), "peak_wset", None)})
            assert not trace["capture_errors"] and record["status"] in ("OK", "NO_EVIDENCE")
        print(index, round(time.monotonic() - begin, 3), flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:])
