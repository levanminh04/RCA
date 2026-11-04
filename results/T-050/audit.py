"""Đối chiếu độc lập RR theo vị trí trong nhóm hòa, vùng và mẫu độ bền."""
import gzip
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np

from replay import ROOT, WORLDS, digest
from seal import read
from score import save
from m1_danh_gia.pha2 import giai_ma_json
from m1_danh_gia.rr import lay_mau_o

OUT = Path(__file__).resolve().parent


def expected_rr(groups, root, status):
    if status != "OK":
        return Fraction(0)
    start = 1
    for group in groups:
        n = len(group)
        if root in group:
            return sum((Fraction(1, i) for i in range(start, start + n)), Fraction(0)) / n
        start += n
    return Fraction(0)


def main():
    phase1, scored = OUT / "pha1-001", OUT / "cham-001"
    mechanisms = giai_ma_json(read(scored / "co-che.json"))
    case = {r["opaque_id"]: r for r in mechanisms}
    scoring = giai_ma_json(read(scored / "cham.json"))["cau_hinh"]
    actual, direct = Counter(), {}
    for line in (phase1 / "ban-ghi.jsonl").read_bytes().splitlines():
        row = json.loads(line)
        cid, oid = row["config_id"], row["opaque_id"]
        for world, payload in row["worlds"].items():
            if cid.startswith("C-") and world != "P":
                continue
            blocks = payload["blocks"]
            keys = [b["key"] for b in blocks]
            assert all(a > b for a, b in zip(keys, keys[1:]))
            assert all(len(b["groups"]) == 1 for b in blocks)
            value = expected_rr([b["groups"][0] for b in blocks], case[oid]["root"], row["status"])
            assert value == scoring[cid]["ca"][oid]["theo_the_gioi"][world]["RR"]
            actual[cid] += 1
            direct[cid, oid, world] = value
    for cid, result in scoring.items():
        for world, mrr in result["MRR_the_gioi"].items():
            for dataset, expected in mrr.items():
                values = [direct[cid, oid, world] for oid, r in case.items()
                          if dataset in ("gop", r["dataset"])]
                assert expected == sum(values) / len(values)
    runtime = Counter()
    max_residual = 0.0
    for side in read(phase1 / "sidecars.json"):
        path = ROOT / side["replay"]
        assert digest(path) == side["sha256"]
        r = read(path)
        for world in WORLDS:
            row = r[world]
            runtime[row["E6b"]["trang_thai_E6b"]] += 1
            if row["mass"]:
                max_residual = max(max_residual, row["mass"]["residual_L1"])
            else:
                assert row["E6b"]["blocks"] == row["S0"]["blocks"]
    assert sum(runtime.values()) == 246
    assert max_residual < 1e-12
    regions = read(scored / "vung.json")
    side_by_id = {r["job"]["opaque_id"]: r for r in read(phase1 / "sidecars.json")
                  if r["job"]["window"] == "that"}
    for row in regions["rows"]:
        replay = read(ROOT / side_by_id[row["opaque_id"]]["replay"])["P"]["region"]
        for cid, ways in row["configs"].items():
            for mode, result in ways.items():
                T = replay[cid]["T"]
                actual_regions = replay[cid][mode]
                assert set(actual_regions) == set(T)
                assert result["p"] == (sum(row["root"] in region for region in actual_regions.values()) / len(T) if T else 0)
                assert result["R_ky_vong"] == (sum(map(len, actual_regions.values())) / len(T) if T else 0)
                assert result["hop"] == sorted(set().union(*map(set, actual_regions.values())))
    controls = read(OUT / "doi-chung-002.json")
    simple = {}
    for row in controls["rows"]:
        oid = row["opaque_id"]
        proof = row["sources"]["simplerca"]
        assert digest(ROOT / proof["path"]) == proof["sha256"]
        simple[oid] = expected_rr(row["simple_groups"] or [], case[oid]["root"], proof["status"])
    simple_mrr = {d: sum(values) / len(values) for d in ("gop", "RE2-TT", "Nezha-OB")
                  if (values := [v for oid, v in simple.items() if d in ("gop", case[oid]["dataset"])])}
    ds = [{"ma": oid, "dataset": r["dataset"], "o": r["cell"]} for oid, r in sorted(case.items())]
    rng = np.random.default_rng(20261102)
    frequencies = Counter()
    with gzip.open(scored / "bootstrap.jsonl.gz", "rt", encoding="utf-8") as stream:
        for i, line in enumerate(stream):
            row = giai_ma_json(json.loads(line))
            weights = lay_mau_o(ds, rng)
            assert i == row["i"] and weights == row["weights"]
            for world in WORLDS:
                for d in ("gop", "RE2-TT", "Nezha-OB"):
                    ids = [oid for oid, r in case.items() if d in ("gop", r["dataset"])]
                    delta = sum((direct["E6b", oid, world] - direct["S1", oid, world]) * weights[oid] for oid in ids)
                    n = sum(weights[oid] for oid in ids)
                    assert row["result"]["dMRR"][world][d] == delta / n
            frequencies[row["result"]["hanh_dong"]] += 1
    assert sum(frequencies.values()) == 1000
    assert frequencies == read(scored / "do-ben.json")["bootstrap"]
    save(OUT / "kiem-cuoi-001.json", {"RR": actual, "rank_status": runtime, "max_residual_L1": max_residual,
                                     "bootstrap_samples": 1000, "regions": len(regions["rows"]),
                                     "SimpleRCA_MRR_P": simple_mrr})


if __name__ == "__main__":
    main()
