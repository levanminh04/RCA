"""Khóa bản ghi dev rồi chấm cặp T11 theo luật C và N1."""
import argparse
import gzip
import sys
from collections import Counter
from fractions import Fraction

from run_t11 import OUT, ROOT, digest, encoded, read, save, source

sys.path[:0] = [str(ROOT / name) for name in ("results/T-045/scripts", "results/T-047/scripts")]
import numpy as np
from pha2_khoi_k import nap_nhan
from luat_c_t047 import DD, _cap_voi_ve, ve_n1
from m1_danh_gia import luat_c, pha2, rr

ARMS = ("off", "on")


def phase1(run):
    entries, _ = source()
    inputs = {f"{e['index']:02d}.json": digest(run / f"{e['index']:02d}.json") for e in entries}
    assert read(run / "plan.json")["indices"] == list(range(82))
    target = run / "sealed"
    target.mkdir()
    rows, ce = [], {arm: {} for arm in ARMS}
    for e in entries:
        filename = f"{e['index']:02d}.json"
        result = pha2.giai_ma_json(read(run / filename))
        assert result["index"] == e["index"] and result["job"] == e["job"]
        job, worlds = result["job"], result["worlds"]
        assert set(worlds) == set(pha2.WORLDS)
        oid = job["opaque_id"]
        for i, arm in enumerate(ARMS):
            p = worlds["P"]
            blocks = p["rank"][i]["blocks"]
            flags = {w: [dict(worlds[w]["flagged"][ma], ma=ma, F_I=fi)
                         for ma, fi in worlds[w]["effect"][i]["F_I"].items()]
                     for w in pha2.WORLDS}
            record = {"config_id": arm, "opaque_id": oid,
                      "status": "OK" if blocks else "NO_EVIDENCE",
                      "blocks": blocks, "verdict": p["verdict"][i],
                      "worlds": {w: {"blocks": worlds[w]["rank"][i]["blocks"]}
                                 for w in pha2.WORLDS},
                      "extra": {"G_N": result["G_N"], "tang_P": p["rank"][i]["tang"],
                                "kenh_co_the_gioi": flags}}
            if job["window"] == "that":
                rows.append(record)
            else:
                assert job["window"] == "ce" and job["dataset"] == "RE2-TT"
                ce[arm][oid] = record
    assert len(rows) == 104 and all(len(ce[arm]) == 30 for arm in ARMS)
    with (target / "ban-ghi.jsonl").open("x", encoding="utf-8") as stream:
        for row in rows:
            stream.write(encoded(row) + "\n")
    save(target / "pha1.json", {
        "tep": "ban-ghi.jsonl", "sha256": digest(target / "ban-ghi.jsonl"),
        "so_ban_ghi": len(rows), "so_ca": 52, "cau_hinh": sorted(ARMS)})
    save(target / "ce.json", ce)
    save(target / "seal.json", {
        "inputs": inputs, "plan": digest(run / "plan.json"),
        "files": {name: digest(target / name) for name in ("pha1.json", "ban-ghi.jsonl", "ce.json")},
        "runner": digest(__file__)})
    print("SEAL", digest(target / "seal.json"), flush=True)


def mechanisms(run, scores, labels, component):
    output = []
    for filename in sorted(read(run / "sealed/seal.json")["inputs"]):
        row = pha2.giai_ma_json(read(run / filename))
        job = row["job"]
        record = {"index": row["index"], "dataset": job["dataset"], "window": job["window"],
                  "opaque_id": job["opaque_id"], "worlds": {}}
        if job["window"] == "that":
            record.update(labels[job["opaque_id"]])
        for world, frame in row["worlds"].items():
            off, on = frame["effect"]
            by_channel = {p["ma"]: p["ly_do_E9"] for p in on["inherited_by"]}
            changed = [ma for ma, fi in on["F_I"].items() if fi != off["F_I"][ma]]
            summary = {"changes_F_I": changed,
                       "changes_tier": sorted(e for e, tier in frame["rank"][0]["tang"].items()
                                              if frame["rank"][1]["tang"][e] != tier),
                       "same_groups": frame["rank"][0]["blocks"] == frame["rank"][1]["blocks"],
                       "same_tie_order": [b["groups"] for b in frame["rank"][0]["blocks"]]
                       == [b["groups"] for b in frame["rank"][1]["blocks"]]}
            if component == "E9":
                summary["states"] = Counter(by_channel.values())
                summary["no_proposal"] = len(frame["no_proposal"])
            if job["window"] == "that":
                oid = job["opaque_id"]
                values = [scores["cau_hinh"][arm]["ca"][oid]["theo_the_gioi"][world]["RR"] for arm in ARMS]
                summary["rr"] = values
                summary["delta"] = values[1] - values[0]
            if world == "P":
                summary["region"] = frame["region"]
            record["worlds"][world] = summary
        if component == "T12":
            record["static"] = row["static"]
            record["controls"] = row["controls"]
            record["control_seconds"] = row["control_seconds"]
        output.append(record)
    return output


def compare(run, component):
    sealed = run / "sealed"
    seal = read(sealed / "seal.json")
    for name, expected in seal["files"].items():
        assert digest(sealed / name) == expected
    for name, expected in seal["inputs"].items():
        assert digest(run / name) == expected
    assert digest(run / "plan.json") == seal["plan"]
    target = run / "score"
    target.mkdir()
    save(target / "receipt.json", {"seal": digest(sealed / "seal.json"), "scope": "dev-a"})
    manifest = read("results/T-050/manifest-chay-lai-002.json")
    for name, item in manifest["labels_dev"].items():
        assert digest(name) == item["sha256"]
    labels = nap_nhan(False)
    assert len(labels) == 52 and len({v["o"] for v in labels.values()}) == 23
    path = "results/T-043/ks16/dem-sau-ghep-nhan.json"
    proof, = [v for v in read("results/T-043/manifest.json")["outputs"] if v["path"] == path]
    assert digest(path) == proof["sha256"]
    activation = read(path)["o_kich_hoat"][component]
    cells = set(activation["RE2-TT"]["o"]) | set(activation["Nezha-OB"]["o"])
    assert len(cells) == {"E9": 10, "T12": 13}[component]
    scores = pha2.cham(sealed, read(sealed / "pha1.json")["sha256"], labels)
    ce = read(sealed / "ce.json")

    def decision(weights=None, h=1):
        side = ve_n1(ce["off"], ce["on"], weights, h)
        return _cap_voi_ve(scores, "off", "on", cells, component, "luat_C", side, weights, DD)

    main = decision()
    save(target / "scores.json", scores)
    save(target / "law.json", main)
    save(target / "mechanisms.json", mechanisms(run, scores, labels, component))
    rows = [{"ma": oid, "dataset": label["dataset"], "o": label["o"]}
            for oid, label in sorted(labels.items())]
    rng = np.random.default_rng(20261104)
    deltas = {world: [] for world in pha2.WORLDS}
    counts = Counter()
    with gzip.open(target / "bootstrap.jsonl.gz", "xt", encoding="utf-8") as stream:
        for i in range(1000):
            weights = rr.lay_mau_o(rows, rng)
            sample = decision(weights)
            out = sample["ket_hop"]["ket_cuc_dung"]
            counts[out] += 1
            changes = {world: sample["theo_the_gioi"][world]["dMRR"] for world in pha2.WORLDS}
            for world, values in changes.items():
                deltas[world].append(float(values["gop"]))
            stream.write(encoded({"i": i, "weights": weights, "outcome": out, "dMRR": changes}) + "\n")
    save(target / "robustness.json", {
        "seed": 20261104, "bootstrap": counts,
        "ci95": {w: np.quantile(x, [.025, .975]).tolist() for w, x in deltas.items()},
        "h": {str(h): decision(h=h)["ket_hop"] for h in (Fraction(1, 2), 2)},
        "delta": {field: luat_c.ket_hop_the_gioi(
            {w: main["theo_the_gioi"][w]["bao_kem"][field] for w in pha2.WORLDS}, "luat_C")
            for field in ("ket_cuc_delta_0005", "ket_cuc_delta_002")}})
    print(encoded(main["ket_hop"]), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("seal", "score"))
    parser.add_argument("run")
    parser.add_argument("--component", choices=("E9", "T12"), default="E9")
    args = parser.parse_args()
    if args.action == "seal":
        phase1(OUT / args.run)
    else:
        compare(OUT / args.run, args.component)
