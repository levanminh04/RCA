"""Đối chiếu cố định cấu hình E4 ↔ z trước diễn giải số K."""
import gzip
import json
from collections import Counter
from pathlib import Path

from doi_chieu import Check, ROOT, RUNS, WORLDS, read, sha
from kiem_t1 import flags, finite


def main():
    plan = read(RUNS.parent / "ke-hoach-pha1.json")
    allocation = read(RUNS / "k-phan-bo-001.json")
    manifest = read(ROOT / "results/T-047/manifest.json")["outputs"]
    command_path = ROOT / "results/T-047/runs/b3-k-c1-that-001/command.json"
    assert sha(command_path) == manifest[command_path.relative_to(ROOT).as_posix()]["sha256"]
    ids = sorted(c["config_id"] for c in read(command_path)["configs"])
    checks = Check()
    counts, changes = Counter(), []
    used = []
    for index, job in enumerate(plan["jobs"]):
        folder = RUNS / f"{allocation[str(index)]}-{index:02d}"
        meta = read(folder / "kiem.json")
        native = folder / "ban-ghi.jsonl.gz"
        assert sha(native) == meta["files"][native.name]["sha256"]
        reference = ROOT / f"results/T-047/runs/b3-k-c1-{job['window']}-001/cases/{job['opaque_id']}/phase1/records"
        with gzip.open(native, "rt", encoding="utf-8") as stream:
            seen = set()
            for line in stream:
                record = json.loads(line)
                cid, oid = record["config_id"], record["opaque_id"]
                assert oid == job["opaque_id"] and cid not in seen and finite(record)
                seen.add(cid)
                path = reference / f"{ids.index(cid):05d}.json"
                rel = path.relative_to(ROOT).as_posix()
                assert sha(path) == manifest[rel]["sha256"], rel
                old = read(path)
                assert old["config_id"] == cid and old["opaque_id"] == oid
                checks.compare(flags(record), flags(old), ["gate_assignment", oid, cid], allow_float=False)
                for world in WORLDS:
                    counts["world_comparisons"] += 1
                    before, after = old["worlds"][world]["blocks"], record["worlds"][world]["blocks"]
                    n1 = lambda blocks: sum(len(g) for b in blocks if b["key"][0] == 2 for g in b["groups"])
                    assert n1(before) == n1(after)
                    if before != after:
                        changes.append(dict(opaque_id=oid, config_id=cid, window=job["window"], world=world,
                                            order_or_tie_changed=[b["groups"] for b in before]
                                            != [b["groups"] for b in after]))
                for channel in record["extra"]["kenh_co"]:
                    used.append(dict(score=channel["s"], unit=channel["don_vi"],
                                     opaque_id=oid,config_id=cid,window=job["window"]))
                counts[job["window"]] += 1
        assert seen == set(ids)
    assert counts["that"] == 832 and counts["ce"] == 480
    result = dict(PASS=not checks.counts, counts=dict(counts), failures=dict(checks.counts),
                  differences=checks.differences, changed_blocks=changes,
                  largest_scores=sorted(used,key=lambda r:-abs(r["score"]))[:30])
    with (RUNS / "kiem-k-day-du-001.json").open("x",encoding="utf-8") as stream:
        json.dump(result,stream,ensure_ascii=False,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ("changed_blocks","largest_scores")}))
    if checks.counts:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
