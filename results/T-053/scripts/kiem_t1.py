"""Kiểm T1 dưới z+S1 so cùng cửa sổ T-047 và các seed/xáo mới."""
import argparse
import json
import math
from pathlib import Path

from doi_chieu import Check, ROOT, RUNS, WORLDS, jsonl, read, sha, structural, window

OLD = ROOT / "results/T-047"
STAGES = {"seed0":"seed0-001", "seed1":"seed1-001", "seed2":"seed2-001", "xao0":"xao0-002", "ce":"ce-001"}


def flags(record):
    snapshot = structural(record)
    snapshot.pop("rank")
    snapshot["common"].pop("region")
    snapshot["common"]["inherited_by"] = [
        {k: v for k, v in edge.items() if k != "diem_truoc_E5"}
        for edge in snapshot["common"]["inherited_by"]
    ]
    snapshot["validity"] = {k: record["diagnostics"][k]
                            for k in ("so_cham_hop_le","NO_VALID_CHANNEL")}
    snapshot["channels"] = {
        w: {k["ma"]: {field: value for field,value in k.items() if field != "s"}
            for k in record["extra"]["kenh_co_the_gioi"][w]} for w in WORLDS
    }
    return snapshot


def finite(value):
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, dict):
        return all(finite(v) for v in value.values())
    if isinstance(value, list):
        return all(finite(v) for v in value)
    return True


def old_records(manifest, stage):
    path = OLD / f"runs/b2-c1-t1-{STAGES[stage]}" / "ban-ghi.jsonl"
    reference = manifest["outputs"][path.relative_to(ROOT).as_posix()]
    assert sha(path) == reference["sha256"] and path.stat().st_size == reference["bytes"]
    records = {r["opaque_id"]: r for r in jsonl(path)}
    assert len(records) == (30 if stage == "ce" else 52)
    return records


def check_t1(allocation):
    plan = read(RUNS.parent / "ke-hoach-pha1.json")
    manifest = read(OLD / "manifest.json")
    checks = Check()
    rows = []
    for stage, names in allocation.items():
        reference = old_records(manifest, stage)
        for i, job in enumerate(plan["jobs"]):
            if (job["window"] == "ce") != (stage == "ce"):
                continue
            old = reference[job["opaque_id"]]
            name = names[str(i)]
            command = read(RUNS / f"{name}-{i:02d}" / "command.json")
            assert command["job"] == job and command["seed"] == (int(stage[-1]) if stage.startswith("seed") else 0)
            assert command["shuffle"] == (0 if stage == "xao0" else None)
            assert command["plan_sha256"] == sha(RUNS.parent / "ke-hoach-pha1.json")
            (record, sidecar), = (item for item in window(name, i) if item[0]["config_id"] == "K-R0")
            assert record["config_id"] == "K-R0" and record["opaque_id"] == old["opaque_id"]
            assert record["window"] == old["window"]
            assert record["status"] in ("OK","NO_EVIDENCE") and finite(record)
            trace = sidecar["trace"]
            for unit in trace["phan_vi"].values():
                if "z" in unit:
                    z = unit["z"]
                    assert z["huu_han"] and all(isinstance(z[k], (int,float)) and math.isfinite(z[k])
                                              for k in ("med_N","IQR","c","z_len","z_xuong"))
            for w in WORLDS:
                assert trace["world_state"][w]["N1"] == sum(
                    len(g) for b in record["worlds"][w]["blocks"] if b["key"][0] == 2 for g in b["groups"])
                for b in record["worlds"][w]["blocks"]:
                    assert all(math.isfinite(x) for x in b["key"])
            checks.compare(flags(record), flags(old), ["gate", stage, record["opaque_id"]],
                           allow_float=False)
            for current, previous in [(record["extra"]["don_vi_phan_vi"], old["extra"]["don_vi_phan_vi"]),
                                      *((record["worlds"][w]["don_vi_dem"], old["worlds"][w]["don_vi_dem"])
                                        for w in WORLDS)]:
                probabilities = lambda units: {u["ma"]: {d: u["p_" + d] for d in ("len","xuong")} for u in units}
                checks.compare(probabilities(current), probabilities(previous),
                               ["gate_p", stage, record["opaque_id"]], allow_float=True)
            for w in WORLDS:
                scores = lambda r: {u["ma"]:[u["e_len"],u["e_xuong"]] for u in r["worlds"][w]["don_vi_dem"]}
                checks.compare(scores(record), scores(old), ["count_scores", stage, record["opaque_id"], w],
                               allow_float=True)
            if stage in ("seed1","seed2","xao0"):
                base_name = allocation["seed0"][str(i)]
                base_command = read(RUNS / f"{base_name}-{i:02d}" / "command.json")
                assert base_command["platform"] == command["platform"]
                (seed0, baseline), = (item for item in window(base_name, i)
                                      if item[0]["config_id"] == "K-R0")
                checks.compare(record, seed0, ["T1_native", stage, record["opaque_id"]], allow_float=False)
                checks.compare(trace["world_state"], baseline["trace"]["world_state"],
                               ["T1_validity", stage, record["opaque_id"]], allow_float=False)
            used = [(k["s"], k["don_vi"], w) for w in WORLDS
                    for k in trace["xep"][WORLDS.index(w)]["kenh"] if k["F_raw"]]
            rows.append(dict(stage=stage, job=i, status=record["status"],
                             max_used_z=max(used, default=None),
                             large_scores=[v for v in used if abs(v[0]) > 1e6],
                             all_tied={w:len(record["worlds"][w]["blocks"]) == 1 for w in WORLDS},
                             worlds={w: {k: trace["world_state"][w][k] for k in ("N1","V0","valid_units")}
                                     for w in WORLDS}))
    assert set(allocation) == set(STAGES) and len(rows) == 238
    return dict(PASS=not checks.counts, records=len(rows), differences=checks.differences,
                failures=dict(checks.counts), max_abs_delta=checks.delta, windows=rows)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("allocation", type=Path)
    p.add_argument("out", type=Path)
    args = p.parse_args()
    result = check_t1(read(args.allocation))
    with args.out.open("x", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    if not result["PASS"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
