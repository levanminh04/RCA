"""Đóng gói pilot và nguồn đã ghim cho EC2, không mang nhãn."""
import copy
import json
import sys
import tarfile
from pathlib import Path

from replay import ROOT, digest, encode

OUT = Path(__file__).resolve().parent


def main(name):
    folder = OUT / name
    index = folder / "index.json"
    entries = json.loads(index.read_bytes())
    matrix = json.loads((ROOT / "results/T-049/ma-tran.json").read_bytes())
    config = copy.deepcopy(matrix["K-b"]["K-thang-C"])
    config.update(config_id="T9-E6b", buoc="T9")
    config["bat_tat"]["E6"] = "b"
    from m1.runner import _ma_noi_dung
    config["ma_noi_dung"] = _ma_noi_dung(config["bat_tat"], config["tham_so_E4"],
                                       config["nhanh_z"], config["tham_so_E3"], config["tham_so_E5"])
    pilot = []
    for dataset, window, heavy in (("RE2-TT", "that", True), ("RE2-TT", "ce", False),
                                   ("Nezha-OB", "that", True), ("Nezha-OB", "that", False)):
        options = [e for e in entries if e["host"] == "ec2" and e["index"] not in pilot
                   and (e["job"]["dataset"], e["job"]["window"]) == (dataset, window)]
        options.sort(key=lambda e: (e["job"]["source_bytes"], e["positive"], e["max_score"], e["edges"], e["index"]))
        pilot.append(options[-1 if heavy else 0]["index"])
    sources = {p: sha for p, sha in matrix["sources"].items()
               if p.startswith(("src/", "results/T-022/", "results/T-026/", "results/T-043/",
                                "results/T-045/scripts/", "results/T-048/scripts/"))}
    for path in (OUT / "replay.py", OUT / "run_ec2.py"):
        sources[path.relative_to(ROOT).as_posix()] = digest(path)
    plan = OUT / "pilot-plan.json"
    with plan.open("xb") as stream:
        stream.write(encode({"pilot": pilot, "config": config, "sources": sources, "index_sha256": digest(index)}))
    with tarfile.open(OUT / "ec2-input-001.tar.gz", "x:gz") as archive:
        for path in sorted({*(ROOT / p for p in sources), plan, *folder.iterdir()}):
            rel = path.relative_to(ROOT).as_posix()
            if rel in sources:
                assert digest(path) == sources[rel], rel
            archive.add(path, arcname=rel, recursive=False)
    print("pilot indices:", pilot)


if __name__ == "__main__":
    main(sys.argv[1])
