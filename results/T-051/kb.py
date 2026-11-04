"""Khóa và chấm bốn phép đảo KB trên nền đã chọn."""
import argparse
import sys
from collections import Counter
from fractions import Fraction

from run_t11 import OUT, ROOT, classify, digest, encoded, frames, read, records, save, source
from run_t12 import STATIC
from kiem_tai_su_dung import check_z
from m1 import xep_hang
from m1_danh_gia import luat_c, pha2, rr

sys.path[:0] = [str(ROOT / p) for p in ("results/T-045/scripts", "results/T-047/scripts")]
import numpy as np
from luat_c_t047 import DD, _cap_voi_ve, ve_n1
from pha2_khoi_k import nap_nhan

BASE = "K-E1+E2+E5"
PAIRS = {
    "E1": ("K-E2+E5", BASE, "GIUP"),
    "E2": ("K-E1+E5", BASE, "TRAI_CHIEU_DATASET"),
    "E3": (BASE, "K-E1+E2+E3+E5", "HAI"),
    "E5": ("K-E1+E2", BASE, "GIUP"),
}
CIDS = {cid for pair in PAIRS.values() for cid in pair[:2]}
OLD = "results/T-053/"


def validate_sources(manifest):
    path = OLD + "ke-hoach-pha1.json"
    assert digest(path) == manifest["outputs"][path]["sha256"]
    plan = read(path)
    for name, sha in plan["sources"].items():
        pinned = "results/T-049/truoc-tich-hop-001/e4.py" if name == "src/m1/e4.py" else name
        assert digest(pinned) == sha, pinned
    return plan


def config_check(config, base, cid):
    expected = dict(base["bat_tat"])
    if cid == "K-E2+E5":
        expected["E1"] = "tat"
    if cid == "K-E1+E5":
        expected["E2"] = "tat"
    if cid == "K-E1+E2+E3+E5":
        expected["E3"] = True
    if cid == "K-E1+E2":
        expected["E5"] = False
    assert config["bat_tat"] == expected, cid
    ignored = {"config_id", "buoc", "ma_noi_dung", "ma_noi_dung_T047", "bat_tat"}
    assert {k: v for k, v in config.items() if k not in ignored} == {
        k: v for k, v in base.items() if k not in ignored}, cid


def rerank(native, trace, config, static):
    if not static or not config["bat_tat"]["E5"]:
        return native
    graph = sorted({tuple(e) for e in native["extra"]["canh"]} | static)
    for world, channels, old, mask, unit_m in frames(native, trace):
        effect, _, rank = classify(channels, graph, unit_m, mask,
                                   old["thuc_the_co_kenh_OK"], False)
        native["worlds"][world]["blocks"] = rank["blocks"]
        flags = native["extra"]["kenh_co_the_gioi"][world]
        for channel in flags:
            channel["F_I"] = effect["F_I"][channel["ma"]]
        if world == "P":
            native["extra"]["tang_P"] = rank["tang"]
            native["blocks"] = rank["blocks"]
            native["verdict"] = xep_hang.verdict(
                rank["tang"], trace["world_state"][world]["valid_units"])
    return native


def phase1(run, t12):
    entries, base = source()
    law = read(t12 / "score/law.json")["ket_hop"]
    assert law["ket_cuc_dung"] in ("GIUP", "HAI", "KHONG_TAC_DUNG", "KHONG_DU_CA")
    assert not (law["ket_cuc_dung"] == "KHONG_DU_CA" and law["ket_cuc_P"] == "HAI")
    use_static = law["ket_cuc_dung"] in ("GIUP", "KHONG_DU_CA")
    assert read(t12 / "plan.json")["E9"] is False
    static = {}
    for dataset, (path, sha) in STATIC.items():
        assert digest(path) == sha
        static[dataset] = {(e["source"], e["target"]) for e in read(path)["edges"]} if use_static else set()
    manifest = read(OLD + "manifest.json")
    plan = validate_sources(manifest)
    path = manifest["canonical"]["phase1_seal"]
    assert digest(path) == manifest["outputs"][path]["sha256"]
    old_seal = read(path)
    t12_seal = read(t12 / "sealed/seal.json")
    by_job = {(e["job"]["opaque_id"], e["job"]["window"]): e for e in entries}
    run.mkdir()
    save(run / "plan.json", {"T12_law": digest(t12 / "score/law.json"),
                             "T12_seal": digest(t12 / "sealed/seal.json"),
                             "T053_seal": digest(path), "runner": digest(__file__), "T12": use_static})
    rows, ce, proofs = [], {cid: {} for cid in CIDS}, []
    for window, group in old_seal.items():
        for item in group:
            prefix = item["path"].rsplit("/", 1)[0]
            command_file = prefix + "/command.json"
            assert digest(command_file) == manifest["outputs"][command_file]["sha256"]
            command = read(command_file)
            job = command["job"]
            assert job["window"] == window and job in plan["jobs"]
            assert digest(OLD + "ke-hoach-pha1.json") == command["plan_sha256"]
            e = by_job[job["opaque_id"], window]
            assert job == e["job"]
            filename = f"{e['index']:02d}.json"
            assert digest(t12 / filename) == t12_seal["inputs"][filename]
            checked = read(t12 / filename)
            assert item["sha256"] == manifest["outputs"][item["path"]]["sha256"]
            assert item["trace_sha256"] == manifest["outputs"][item["trace"]]["sha256"]
            old_rows, old_trace = [records(item[k], manifest["outputs"][item[k]], CIDS)
                                   for k in ("path", "trace")]
            proof = {"job": job, "path": item, "z_units": {}, "rank_source": {}}
            for cid in sorted(CIDS):
                native, side = old_rows[cid], old_trace[cid]
                config = command["configs"][cid]
                config_check(config, base, cid)
                assert native["opaque_id"] == job["opaque_id"] and all(side[k] == v for k, v in job.items())
                assert native["status"] in ("OK", "NO_EVIDENCE")
                assert side["trace"]["normalized_input_sha256"] == checked["normalized_input_sha256"]
                assert native["extra"]["canh"] == checked["edges"] and native["extra"]["G_N"] == checked["G_N"]
                proof["z_units"][cid] = check_z(side)
                native = rerank(native, side["trace"], config, static[job["dataset"]])
                if cid == BASE:
                    assert all(encoded(native["worlds"][w]["blocks"]) ==
                               encoded(checked["worlds"][w]["rank"][use_static]["blocks"]) for w in pha2.WORLDS)
                    assert native["verdict"] == checked["worlds"]["P"]["verdict"][use_static]
                proof["rank_source"][cid] = "replay_E5" if use_static and config["bat_tat"]["E5"] else "native_T053"
                record = {k: native[k] for k in ("config_id", "opaque_id", "status", "blocks", "verdict", "worlds")}
                record["extra"] = {k: native["extra"][k] for k in ("G_N", "tang_P", "kenh_co_the_gioi")}
                if window == "that":
                    rows.append(record)
                else:
                    ce[cid][job["opaque_id"]] = record
            proofs.append(proof)
            print(e["index"], flush=True)
    assert len(proofs) == 82 and len(rows) == 52 * len(CIDS)
    assert all(len(v) == 30 for v in ce.values())
    with (run / "ban-ghi.jsonl").open("x", encoding="utf-8") as stream:
        for row in rows:
            stream.write(encoded(row) + "\n")
    save(run / "pha1.json", {"tep": "ban-ghi.jsonl", "sha256": digest(run / "ban-ghi.jsonl"),
                            "so_ban_ghi": len(rows), "so_ca": 52, "cau_hinh": sorted(CIDS)})
    save(run / "ce.json", ce)
    save(run / "sources.json", proofs)
    save(run / "seal.json", {name: digest(run / name) for name in (
        "ban-ghi.jsonl", "pha1.json", "ce.json", "sources.json", "plan.json")})
    print("SEAL", digest(run / "seal.json"), flush=True)


def score(run):
    for name, sha in read(run / "seal.json").items():
        assert digest(run / name) == sha
    target = run / "score"
    target.mkdir()
    save(target / "receipt.json", {"seal": digest(run / "seal.json"), "scope": "dev-a"})
    for path, proof in read("results/T-050/manifest-chay-lai-002.json")["labels_dev"].items():
        assert digest(path) == proof["sha256"]
    labels = nap_nhan(False)
    assert len(labels) == 52 and len({v["o"] for v in labels.values()}) == 23
    path = "results/T-043/ks16/dem-sau-ghep-nhan.json"
    proof, = [v for v in read("results/T-043/manifest.json")["outputs"] if v["path"] == path]
    assert digest(path) == proof["sha256"]
    ex = read(path)["o_kich_hoat"]
    ce = read(run / "ce.json")
    scores = pha2.cham(run, read(run / "pha1.json")["sha256"], labels)
    save(target / "scores.json", scores)
    ds = [{"ma": oid, "dataset": v["dataset"], "o": v["o"]} for oid, v in sorted(labels.items())]
    rng = np.random.default_rng(20261104)
    weights = [rr.lay_mau_o(ds, rng) for _ in range(1000)]
    summaries = {}
    for component, (off, on, previous) in PAIRS.items():
        cells = set(ex[component]["RE2-TT"]["o"]) | set(ex[component]["Nezha-OB"]["o"])

        def decision(w=None, h=1):
            side = ve_n1(ce[off], ce[on], w, h)
            return _cap_voi_ve(scores, off, on, cells, component, "khoi_K", side, w, DD)

        result = decision()
        hop = result["ket_hop"]
        summaries[component] = {"previous": previous, "now": hop,
                                "needs_decision": hop["ket_cuc_dung"] != previous or hop["phu_thuoc_quan_sat"]}
        save(target / f"{component}-law.json", result)
        boot = [decision(w) for w in weights]
        save(target / f"{component}-robustness.json", {
            "seed": 20261104,
            "ci95": {w: np.quantile([float(s["theo_the_gioi"][w]["dMRR"]["gop"]) for s in boot],
                                    [.025, .975]).tolist() for w in pha2.WORLDS},
            "bootstrap": Counter(s["ket_hop"]["ket_cuc_dung"] for s in boot),
            "h": {str(h): decision(h=h)["ket_hop"] for h in (Fraction(1, 2), 2)},
            "delta": {key: luat_c.ket_hop_the_gioi(
                {w: result["theo_the_gioi"][w]["bao_kem"][key] for w in pha2.WORLDS}, "khoi_K")
                for key in ("ket_cuc_delta_0005", "ket_cuc_delta_002")}})
        print(component, encoded(summaries[component]), flush=True)
    save(target / "summary.json", summaries)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("seal", "score"))
    parser.add_argument("run")
    parser.add_argument("--t12")
    args = parser.parse_args()
    if args.action == "seal":
        phase1(OUT / args.run, OUT / args.t12)
    else:
        score(OUT / args.run)
