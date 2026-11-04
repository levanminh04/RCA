"""Đối chiếu hai lượt chạy độc lập của T-050 theo từng cửa sổ và đầu ra chấm."""
import gzip
import math
from collections import Counter
from pathlib import Path

from replay import ROOT, digest
from seal import read, write

OUT = Path(__file__).resolve().parent


def main():
    old_manifest = OUT / "manifest.json"
    original = read(old_manifest)
    for name, proof in original["outputs"].items():
        path = ROOT / name
        assert path.stat().st_size == proof["bytes"] and digest(path) == proof["sha256"], name

    for name in ("index.json", *(f"{i:02d}.json.gz" for i in range(82))):
        assert digest(OUT / "dau-vao-003" / name) == digest(OUT / "dau-vao-004" / name), name
    assert digest(OUT / "doi-chung-002.json") == digest(OUT / "doi-chung-003.json")
    assert digest(OUT / "pha1-001/ban-ghi.jsonl") == digest(OUT / "pha1-002/ban-ghi.jsonl")

    durations = {"pilot": [], "replay": []}
    for i in range(82):
        older, newer = [OUT / f"ec2-{n:03d}-download/ec2-{n:03d}/{i:02d}" for n in (1, 2)]
        a, b = [read(path / "complete.json") for path in (older, newer)]
        assert a["attempt"] != b["attempt"] and a["provenance"] == b["provenance"], i
        name = "result.json"
        assert digest(newer / b["attempt"] / name) == b["files"][name] == a["files"][name], i
        durations["pilot" if b["provenance"]["pilot"] else "replay"].append(b["seconds"])

    scores = ("cham.json", "luat.json", "do-ben.json", "vung.json")
    for name in scores:
        assert digest(OUT / "cham-001" / name) == digest(OUT / "cham-002" / name), name
    samples = "bootstrap.jsonl.gz"
    a, b = [gzip.decompress((OUT / f"cham-{n:03d}" / samples).read_bytes()) for n in (1, 2)]
    assert a == b and len(b.splitlines()) == 1000
    a, b = [read(OUT / f"cham-{n:03d}/co-che.json") for n in (1, 2)]
    for previous, new in zip(a, b, strict=True):
        assert digest(ROOT / previous.pop("replay")) == digest(ROOT / new.pop("replay"))
        assert previous == new

    score = read(OUT / "cham-002/cham.json")["cau_hinh"]
    rr_counts = Counter({name: sum(len(row["theo_the_gioi"]) for row in value["ca"].values())
                         for name, value in score.items()})
    assert sum(rr_counts.values()) == 572
    luat = read(OUT / "cham-002/luat.json")
    write(OUT / "kiem-chay-lai-002.json", {
        "original_manifest_sha256": digest(old_manifest),
        "original_outputs_unchanged": len(original["outputs"]),
        "projected_windows_identical": 82,
        "fresh_windows_identical": 82,
        "frames": 246,
        "rr_counts": rr_counts,
        "bootstrap_samples_identical": 1000,
        "regions_and_controls_identical": True,
        "mrr_P": {name: score[name]["MRR_the_gioi"]["P"] for name in ("S1", "E6b")},
        "decision": luat["ket_hop"]["ket_cuc_dung"],
        "window_seconds": {name: math.fsum(values) for name, values in durations.items()},
    })


if __name__ == "__main__":
    main()
