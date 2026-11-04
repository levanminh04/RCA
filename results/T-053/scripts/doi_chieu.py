"""Đối chiếu dấu vết trước nhãn. Tách khóa số thực và quyết định xếp hạng."""
import argparse
import gzip
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUNS = ROOT / "results/T-053/runs"
WORLDS = ("P", "S_lo", "S_hi")


def read(path):
    return json.loads(path.read_bytes())


def sha(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def jsonl(path):
    op = gzip.open if path.suffix == ".gz" else open
    with op(path, "rt", encoding="utf-8") as f:
        yield from map(json.loads, f)


def window(run, i):
    folder = RUNS / f"{run}-{i:02d}"
    meta = read(folder / "kiem.json")
    for name, expected in meta["files"].items():
        p = folder / name
        assert p.stat().st_size == expected["bytes"] and sha(p) == expected["sha256"], str(p)
    records = jsonl(folder / "ban-ghi.jsonl.gz")
    traces = jsonl(folder / "trung-gian.jsonl.gz")
    for record, sidecar in zip(records, traces, strict=True):
        assert record["config_id"] == sidecar["config_id"]
        assert record["opaque_id"] == sidecar["opaque_id"]
        assert not sidecar["numerical_exceptions"] and not sidecar["trace"]["capture_errors"]
        yield record, sidecar


def shape(record):
    return {
        w: [(b["key"][0], b["groups"]) for b in record["worlds"][w]["blocks"]]
        for w in WORLDS
    }


def gate(unit):
    return {k: v for k, v in unit.items() if k not in
            ("p_len", "p_xuong", "e_len", "e_xuong", "e_len_q", "e_xuong_q")}


def structural(record):
    return {
        "common": {k: record[k] for k in ("status", "window", "sets", "coverage", "verdict",
                                         "OBS_DEPENDENT", "classes", "inherited_by", "region")},
        "graph": {k: record["extra"][k] for k in ("canh", "G_N", "nhom_vong_P", "tang_P")},
        "PV": {u["ma"]: gate(u) for u in record["extra"]["don_vi_phan_vi"]},
        "count": {w: {u["ma"]: gate(u) for u in record["worlds"][w]["don_vi_dem"]} for w in WORLDS},
        "rank": shape(record),
    }


def rank_numbers(record):
    return {w: [b["key"] for b in record["worlds"][w]["blocks"]] for w in WORLDS}


class Check:
    def __init__(self):
        self.delta = {}
        self.differences = []
        self.counts = Counter()

    def compare(self, left, right, path, *, allow_float):
        if left == right:
            return
        if isinstance(left, dict) and isinstance(right, dict) and left.keys() == right.keys():
            for k in left:
                self.compare(left[k], right[k], [*path, k], allow_float=allow_float)
        elif isinstance(left, list) and isinstance(right, list) and len(left) == len(right):
            for i, (a, b) in enumerate(zip(left, right)):
                self.compare(a, b, [*path, i], allow_float=allow_float)
        elif allow_float and isinstance(left, float) and isinstance(right, float):
            field = next((k for k in reversed(path) if k in {"p_len","p_xuong","h","l",
                         "z_len","z_xuong","K_I","K_raw","blocks","key","m","s"}), "other")
            self.delta[field] = max(self.delta.get(field, 0), abs(left-right))
            if field.startswith("p_") and (left < 0.01) != (right < 0.01):
                self.issue(path, left, right)
            elif not math.isclose(left, right, abs_tol=1e-14, rel_tol=1e-12):
                self.issue(path, left, right)
        else:
            self.issue(path, left, right)

    def issue(self, path, left, right):
        self.counts[path[0]] += 1
        if len(self.differences) < 40:
            self.differences.append(dict(path=path, left=repr(left)[:250], right=repr(right)[:250]))


def pilot(first, second, indices, exact):
    check = Check()
    count = 0
    for i in indices:
        for (a, x), (b, y) in zip(window(first, i), window(second, i), strict=True):
            prefix = [a["opaque_id"], a["config_id"]]
            for field in ("dataset", "config_id", "window", "effective_sha256"):
                check.compare(x[field], y[field], ["identity", *prefix, field], allow_float=False)
            tx, ty = x["trace"], y["trace"]
            for field in ("U", "normalized_input_sha256", "cong_G3"):
                check.compare(tx[field], ty[field], ["input", *prefix, field], allow_float=False)
            for field, u in structural(a).items():
                check.compare(u, structural(b)[field], [field, *prefix], allow_float=False)
            for w in WORLDS:
                for field in ("N1", "V0", "valid_units"):
                    check.compare(tx["world_state"][w][field], ty["world_state"][w][field],
                                  ["state", *prefix, w, field], allow_float=False)
                ix, iy = WORLDS.index(w), WORLDS.index(w)
                for field in ("F_I", "co_OK"):
                    check.compare(tx["xep"][ix][field], ty["xep"][iy][field],
                                  ["assignment", *prefix, w, field], allow_float=False)
            check.compare(a, b, ["native", *prefix], allow_float=not exact)
            check.compare(tx, ty, ["trace", *prefix], allow_float=not exact)
            count += 1
    return dict(records=count, max_abs_delta=check.delta, differences=check.differences,
                failures=dict(check.counts), PASS=not check.counts)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("first")
    p.add_argument("second")
    p.add_argument("jobs")
    p.add_argument("out", type=Path)
    p.add_argument("--exact", action="store_true")
    args = p.parse_args()
    result = pilot(args.first, args.second, map(int, args.jobs.split(",")), args.exact)
    with args.out.open("x", encoding="utf-8") as out:
        json.dump(result, out, ensure_ascii=False, indent=2, allow_nan=False)
    if not result["PASS"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
