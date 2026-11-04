"""Đóng ma trận K và SHA-256 trước khi ghép nhãn."""
import argparse
import json
from collections import Counter
from pathlib import Path

from doi_chieu import ROOT, RUNS, WORLDS, read, sha, window


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("allocation", type=Path, help="Ánh xạ job -> tên lượt K, hoặc tên lượt theo từng cấu hình")
    p.add_argument("out", type=Path)
    args = p.parse_args()
    out = args.out.resolve()
    if out.parent != RUNS:
        raise ValueError("Đường dẫn ngoài runs")
    out.mkdir()
    plan = read(RUNS.parent / "ke-hoach-pha1.json")
    allocation = read(args.allocation)
    assert set(allocation) == {str(i) for i in range(82)}
    configs = set(plan["stages"]["K"])
    counts = Counter()
    jobs = []
    seal = {"that": [], "ce": []}
    for kind in ("that","ce"):
        for i, job in enumerate(plan["jobs"]):
            if job["window"] != kind:
                continue
            name = allocation[str(i)]
            folder = RUNS / f"{name}-{i:02d}"
            command = read(folder / "command.json")
            assert command["job"] == job and command["seed"] == 0 and command["shuffle"] is None
            assert command["plan_sha256"] == sha(RUNS.parent / "ke-hoach-pha1.json")
            files = read(folder / "kiem.json")["files"]
            actual = set()
            for rec, trace in window(name, i):
                cid = rec["config_id"]
                assert cid not in actual and rec["opaque_id"] == job["opaque_id"]
                assert rec["status"] in ("OK","NO_EVIDENCE") and set(rec["worlds"]) == set(WORLDS)
                actual.add(cid)
                counts[kind] += 1
            assert actual == configs == set(command["configs"])
            jobs.append(dict(job=job, run=name, configs=sorted(actual), files=files,
                             command_sha256=sha(folder / "command.json")))
            native, trace = (folder / f"{src}.jsonl.gz" for src in ("ban-ghi","trung-gian"))
            seal[kind].append(dict(path=native.relative_to(ROOT).as_posix(), sha256=files[native.name]["sha256"],
                                   trace=trace.relative_to(ROOT).as_posix(), trace_sha256=files[trace.name]["sha256"]))
    assert dict(counts) == {"that":832,"ce":480}
    (out / "kiem.json").write_text(json.dumps(dict(counts=counts, jobs=jobs), indent=2) + "\n", encoding="utf-8")
    path = out / "seal.json"
    path.write_text(json.dumps(seal, indent=2) + "\n", encoding="utf-8")
    print(f"- `{path.relative_to(ROOT).as_posix()}`: `{sha(path)}`")


if __name__ == "__main__":
    main()
