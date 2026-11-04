"""Bảng độ đo, vùng và đối chứng từ đầu ra pha chấm."""
import sys
from collections import Counter
from statistics import mean

from run_t11 import OUT, read, save
from m1_danh_gia import e7, pha2, rr


def main(folder):
    target = folder / "score"
    scores = pha2.giai_ma_json(read(target / "scores.json"))["cau_hinh"]
    metrics = {}
    for cid, configuration in scores.items():
        summary = {}
        for dataset in ("gop", "RE2-TT", "Nezha-OB"):
            cases = [r for r in configuration["ca"].values()
                     if dataset in ("gop", r["dataset"])]
            by_world = {}
            for world in pha2.WORLDS:
                rows = [r["theo_the_gioi"][world] for r in cases]
                values = {field: mean(r["do"][field] for r in rows)
                          for field in ("hit@1", "hit@3", "hit@5", "ndcg@5")}
                values.update(MRR=mean(r["RR"] for r in rows),
                              Retrieval5=values["hit@5"],
                              Rerank1_K5=values["hit@1"] / values["hit@5"] if values["hit@5"] else None)
                by_world[world] = values
            summary[dataset] = by_world
        metrics[cid] = summary
    save(target / "metrics.json", metrics)
    if not (target / "mechanisms.json").exists():
        return
    cases = pha2.giai_ma_json(read(target / "mechanisms.json"))
    if not all("controls" in row for row in cases):
        return
    output = {}
    for dataset in ("RE2-TT", "Nezha-OB"):
        current = [row for row in cases if row["dataset"] == dataset and row["window"] == "that"]
        rows = []
        for row in current:
            regions = row["worlds"]["P"]["region"]
            root = row["root"]
            rows.append({"index": row["index"], "opaque_id": row["opaque_id"],
                         "regions": [{f"cach_{i}": e7.mo_ta(
                             arm["T"], arm[f"cach_{i}"], root) for i in (1, 2)} for arm in regions],
                         "controls": [{name: {"status": r["trang_thai"],
                                               "RR": rr.rr_ca(r["blocks"], root, r["trang_thai"] == "OK")}
                                       for name, r in arm.items()} for arm in row["controls"]]})
        summary = {}
        for i in range(2):
            regions = {f"cach_{kind}": {
                key: mean(r["regions"][i][f"cach_{kind}"][key] for r in rows)
                for key in ("p", "R_ky_vong", "co_hop")} for kind in (1, 2)}
            controls = {name: {
                "statuses": Counter(r["controls"][i][name]["status"] for r in rows),
                "mean_rr_fixed_denominator": mean(r["controls"][i][name]["RR"] for r in rows),
            } for name in rows[0]["controls"][i]}
            summary[("off", "on")[i]] = {"regions": regions, "controls": controls}
        output[dataset] = {"rows": rows, "summary": summary}
    save(target / "regions-controls.json", output)


if __name__ == "__main__":
    main(OUT / sys.argv[1])
