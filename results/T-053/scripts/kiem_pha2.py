"""Kiểm độc lập độ đo theo nhóm hòa M1 và số đếm C-e sau chấm."""
import gzip
import argparse
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "src"), str(Path(__file__).resolve().parent)]
from cham_k import sealed_inputs, source
from m1_danh_gia.pha2 import giai_ma_json

BASE = ROOT / "results/T-053"
RUNS = BASE / "runs"


def read(path):
    return giai_ma_json(json.loads(path.read_bytes()))


def records(paths):
    for path in paths:
        with gzip.open(path, "rt", encoding="utf-8") as stream:
            yield from map(json.loads, stream)


def oracle(blocks, root):
    """M1 ghi một nhóm trong mỗi khối, các khóa liền nhau khác nhau."""
    offset = 0
    previous = None
    ranks = []
    for block in blocks:
        assert len(block["groups"]) == 1
        key = tuple(block["key"])
        assert previous is None or previous > key
        previous = key
        group = block["groups"][0]
        if root in group:
            ranks = list(range(offset+1, offset+len(group)+1))
        offset += len(group)
    if not ranks:
        return dict(RR=Fraction(0), hit1=Fraction(0), hit3=0.0, hit5=0.0, ndcg5=0.0)
    count = len(ranks)
    return dict(
        RR=sum((Fraction(1, rank) for rank in ranks), Fraction(0))/count,
        hit1=Fraction(sum(rank == 1 for rank in ranks), count),
        hit3=sum(rank <= 3 for rank in ranks)/count,
        hit5=sum(rank <= 5 for rank in ranks)/count,
        ndcg5=sum(1/math.log2(rank+1) for rank in ranks if rank <= 5)/count,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=RUNS / 'kiem-pha2-doc-lap-001.json')
    args = parser.parse_args()
    seal_hash, _, inputs = sealed_inputs(RUNS / "k-dong-pha1-001/seal.json")
    labels = source.nap_nhan(False)
    scored = read(RUNS / "k-cham-001/kq.json")["cau_hinh"]
    law = read(RUNS / "k-cham-001/khoi-k.json")
    checked = 0
    for record in records(inputs["that"][0]):
        cid, oid = record["config_id"], record["opaque_id"]
        for world in ("P", "S_lo", "S_hi"):
            value = scored[cid]["ca"][oid]["theo_the_gioi"][world]
            expected = oracle(record["worlds"][world]["blocks"], labels[oid]["root"])
            assert value["RR"] == expected["RR"] and value["hit1"] == expected["hit1"]
            for field, actual in (("hit3", value["do"]["hit@3"]),
                                  ("hit5", value["do"]["hit@5"]),
                                  ("ndcg5", value["do"]["ndcg@5"])):
                assert math.isclose(actual, expected[field], rel_tol=1e-14, abs_tol=1e-14)
            checked += 1
    assert checked == 832*3
    fake = {}
    for record in records(inputs["ce"][0]):
        cid, oid = record["config_id"], record["opaque_id"]
        fake.setdefault(cid, {})[oid] = (
            sum(tier == 1 for tier in record["extra"]["tang_P"].values()),
            record["verdict"],
        )
    pairs = 0
    for key, result in law["cap"].items():
        off, on = ("K-"+name for name in key.split("|"))
        selected = [oid for oid in fake[off]
                    if fake[off][oid][1] != "INSUFFICIENT_EVIDENCE"
                    and fake[on][oid][1] != "INSUFFICIENT_EVIDENCE"]
        n = len(selected)
        if n:
            old = Fraction(sum(fake[off][oid][0] for oid in selected), n)
            new = Fraction(sum(fake[on][oid][0] for oid in selected), n)
        for world in ("P", "S_lo", "S_hi"):
            saved = result["theo_the_gioi"][world]["moc_gia"]
            assert saved["n"] == n
            if n:
                assert saved["trung_binh_tat"] == old and saved["trung_binh_bat"] == new
                assert saved["tang"] == new-old
                assert (saved["ve"] == "HAI") == (new-old > Fraction(1))
        pairs += 1
    assert pairs == 43
    bootstrap = read(RUNS / "bootstrap-ec2-001/do-ben.json")
    assert bootstrap["n"] == 1000 and sum(bootstrap["loai"].values()) == 1000
    for key, value in bootstrap["mau_goc"].items():
        assert value == law[key]
    partial = json.loads((RUNS / "bootstrap-ec2-001/local-prefix-check.json").read_bytes())
    assert partial["PASS"] and partial["local_complete_samples"] == 448
    result = dict(PASS=True, seal_sha256=seal_hash, score_world_cases=checked,
                  C_e_pairs=pairs, bootstrap_samples=1000, identical_cross_host_prefix=448)
    path = args.out.resolve()
    assert path.is_relative_to(BASE.resolve())
    with path.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
