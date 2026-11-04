"""Chấm dev sau khi xác minh seal, đọc luật C và mô tả vùng E7."""
import gzip
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np

from replay import ROOT, WORLDS, digest, encode, xep_hang
from seal import read, write
from m1_danh_gia import e7, luat_c, pha2, rr

OUT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT / name) for name in ("results/T-045/scripts", "results/T-047/scripts")]
from pha2_khoi_k import nap_nhan
from luat_c_t047 import DD, _cap_voi_ve, ve_n1


def save(path, data):
    write(path, pha2.ma_hoa_json(data))


def outcome(hop):
    return {
        "GIUP": "GIU_E6b", "HAI": "GIU_E6a_S1",
        "KHONG_DU_CA": "GIU_E6b_CHUA_PHAN_XU",
        "TRAI_CHIEU_O": "TRINH_MINH", "TRAI_CHIEU_DATASET": "TRINH_MINH",
        "KHONG_TAC_DUNG": "DE_XUAT_GIU_E6a_S1_TAT_E6b",
    }[hop["ket_cuc_dung"]]


def decision(score, ex, ve, weights=None):
    result = _cap_voi_ve(score, "S1", "E6b", ex, "E6b", "luat_C", ve, weights, DD)
    result["hanh_dong"] = outcome(result["ket_hop"])
    return result


def summary(result):
    worlds = result["theo_the_gioi"]
    sensitivity = {}
    for key in ("ket_cuc_delta_0005", "ket_cuc_delta_002"):
        hop = luat_c.ket_hop_the_gioi({w: worlds[w]["bao_kem"][key] for w in WORLDS}, "luat_C")
        sensitivity[key] = {"ket_hop": hop, "hanh_dong": outcome(hop)}
    return {"ket_hop": result["ket_hop"], "hanh_dong": result["hanh_dong"],
            "dMRR": {w: worlds[w]["dMRR"] for w in WORLDS}, "do_nhay": sensitivity}


def activation():
    relative = "results/T-043/ks16/dem-sau-ghep-nhan.json"
    manifest = read(ROOT / "results/T-043/manifest.json")
    proof, = [x for x in manifest["outputs"] if x["path"] == relative]
    path = ROOT / relative
    assert digest(path) == proof["sha256"] and path.stat().st_size == proof["bytes"]
    x = read(path)["o_kich_hoat"]["E6b"]
    assert len(x["RE2-TT"]["o"]) == 8 and len(x["Nezha-OB"]["o"]) == 13
    return set(x["RE2-TT"]["o"]) | set(x["Nezha-OB"]["o"])


def v_blocks(rank, v):
    items = [(e, (xep_hang._lam_tron_12(v.get(e, 0)), *rank["K_I"][e], *rank["K_raw"][e]))
             for e in rank["tang"]]
    return xep_hang._nhom(xep_hang.sap_khoa(items))


def analyze(side, replay, label, scores):
    root, oid = label["root"], side["job"]["opaque_id"]
    comparison = {}
    for w in WORLDS:
        row = replay[w]
        values = {cid: scores["cau_hinh"][cid]["ca"][oid]["theo_the_gioi"][w]["RR"]
                  for cid in ("S1", "S0", "E6b")}
        rank = row["E6b"]
        mass = row["mass"]
        local_blocks = v_blocks(rank, mass["v"]) if mass else rank["blocks"]
        local_rr = rr.rr_ca(local_blocks, root, side["status"] == "OK")
        comparison[w] = {"rr": values, "rr_v": local_rr, "delta": values["E6b"] - values["S1"],
                         "v_blocks": local_blocks,
                         "rr_edge_step": values["E6b"] - local_rr,
                         "rr_key_step": local_rr - values["S0"],
                         "rr_s1_step": values["S0"] - values["S1"]}
        assert sum(comparison[w][key] for key in ("rr_edge_step", "rr_key_step", "rr_s1_step")) == comparison[w]["delta"]
    return {"opaque_id": oid, "root": root, "dataset": label["dataset"], "cell": label["o"],
            "replay": side["replay"], "comparisons": comparison}


def regions(side, replay, label, configs):
    row = replay["P"]
    root = label["root"]
    source = json.loads(gzip.decompress((ROOT / side["input"]).read_bytes()))["input"]
    subgraph = {k["thuc_the"] for k in source["frames"]["P"]["kenh"] if k["F_raw"] == 1}
    return {"opaque_id": side["job"]["opaque_id"], "dataset": label["dataset"], "root": root,
            "outside_U": root not in side["U"], "outside_subgraph": root not in subgraph,
            "configs": {cid: {f"cach_{i}": e7.mo_ta(
                row["region"][cid]["T"], {r: set(g) for r, g in row["region"][cid][f"cach_{i}"].items()},
                root, len(side["observed"])) for i in (1, 2)} for cid in configs}}


def main(sealed, target):
    pin = digest(sealed / "seal.json")
    log = ROOT / "tasks/T-050-t9-va-t10/LOG.md"
    assert f'- `{(sealed / "seal.json").relative_to(ROOT).as_posix()}` ({pin})' in log.read_text(encoding="utf-8").splitlines()
    for path, sha in read(sealed / "seal.json").items():
        assert digest(ROOT / path) == sha, path
    sidecars = read(sealed / "sidecars.json")
    assert len(sidecars) == 82
    for row in sidecars:
        assert digest(ROOT / row["replay"]) == row["sha256"]
        assert digest(ROOT / row["input"]) == row["input_sha256"]
    target.mkdir()
    save(target / "so-lan-nhin.json", {"seal_sha256": pin, "scope": "dev"})
    labels = nap_nhan(False)
    assert len(labels) == 52 and len({x["o"] for x in labels.values()}) == 23
    assert set(labels) == {r["job"]["opaque_id"] for r in sidecars if r["job"]["window"] == "that"}
    assert all(labels[r["job"]["opaque_id"]]["dataset"] == r["job"]["dataset"]
               for r in sidecars if r["job"]["window"] == "that")
    score = pha2.cham(sealed, read(sealed / "pha1.json")["sha256"], labels)
    for cid in ("C-c", "C-g"):
        result = score["cau_hinh"][cid]
        result["MRR_the_gioi"] = {"P": result["MRR"]}
        del result["WORLD_DEPENDENT"]
        for case in result["ca"].values():
            case["theo_the_gioi"] = {"P": case["theo_the_gioi"]["P"]}
            del case["WORLD_DEPENDENT"], case["nguyen_nhan_WD"]
    save(target / "cham.json", score)
    ce = {"S1": {}, "E6b": {}}
    for row in sidecars:
        if row["job"]["window"] == "ce":
            r = read(ROOT / row["replay"])
            for cid in ce:
                ce[cid][row["job"]["opaque_id"]] = {"status": row["status"], "verdict": r["P"]["V0"],
                                                     "extra": {"tang_P": r["P"][cid]["tang"]}}
    assert len(ce["S1"]) == 30 and ce["S1"] == ce["E6b"]
    ve = ve_n1(ce["S1"], ce["E6b"])
    ex = activation()
    result = decision(score, ex, ve)
    save(target / "luat.json", result)
    ds = [{"ma": oid, "dataset": label["dataset"], "o": label["o"]} for oid, label in sorted(labels.items())]
    rng = np.random.default_rng(20261102)
    frequencies = Counter()
    with gzip.open(target / "bootstrap.jsonl.gz", "xb") as stream:
        for i in range(1000):
            weights = rr.lay_mau_o(ds, rng)
            sample = summary(decision(score, ex, ve, weights))
            frequencies[sample["hanh_dong"]] += 1
            stream.write(encode(pha2.ma_hoa_json({"i": i, "weights": weights, "result": sample})) + b"\n")
    leave_out = {cell: summary(decision(score, ex, ve, {
        row["ma"]: int(row["o"] != cell) for row in ds})) for cell in sorted({row["o"] for row in ds})}
    save(target / "do-ben.json", {"seed": 20261102, "bootstrap": frequencies,
                                 "do_nhay": summary(result), "bo_tung_o": leave_out,
                                 "h": {"trang_thai": "BAT_BIEN" if ve["n"] else "CHUA_KIEM_DUOC",
                                       "thu": [0.5, 2], "n": ve["n"], "delta_N1": ve["tang"]}})
    configs = {"GIU_E6b": ["E6b"], "GIU_E6a_S1": ["S1"],
               "DE_XUAT_GIU_E6a_S1_TAT_E6b": ["S1"],
               "GIU_E6b_CHUA_PHAN_XU": ["E6b"], "TRINH_MINH": ["S1", "E6b"]}[result["hanh_dong"]]
    mechanisms, region_rows = [], []
    for side in sidecars:
        if side["job"]["window"] == "that":
            label = labels[side["job"]["opaque_id"]]
            replay = read(ROOT / side["replay"])
            mechanisms.append(analyze(side, replay, label, score))
            region_rows.append(regions(side, replay, label, configs))
    save(target / "co-che.json", mechanisms)
    grouped = {}
    for dataset in ("RE2-TT", "Nezha-OB"):
        rows = [r for r in region_rows if r["dataset"] == dataset]
        grouped[dataset] = {cid: {f"cach_{i}": {
            field: sum(r["configs"][cid][f"cach_{i}"][field] for r in rows) / len(rows)
            for field in ("p", "R_ky_vong", "co_hop")} for i in (1, 2)} for cid in configs}
    save(target / "vung.json", {"configs": configs, "action": result["hanh_dong"],
                               "rows": region_rows, "datasets": grouped})
    print(summary(result), flush=True)


if __name__ == "__main__":
    main(*(OUT / arg for arg in sys.argv[1:]))
