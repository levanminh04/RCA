"""T11: phát lại E5/E9 trên trung gian T-049 đã ghim, chưa đọc nhãn."""
import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT / name) for name in (
    "src", "results/T-049/scripts", "results/T-050")]
from kiem_tai_su_dung import records
from m1 import e5, xep_hang
from m1_danh_gia import pha2
from replay import inputs, region


def read(path):
    return json.loads((ROOT / path).read_bytes())


def digest(path):
    with (ROOT / path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def encoded(value):
    return json.dumps(pha2.ma_hoa_json(value), ensure_ascii=False, allow_nan=False,
                      sort_keys=True, separators=(",", ":"))


def save(path, value):
    with path.open("x", encoding="utf-8") as stream:
        stream.write(encoded(value) + "\n")


def frames(record, trace):
    assert not trace["capture_errors"]
    inventory = set(trace["U"])
    for i, world in enumerate(pha2.WORLDS):
        frame = trace["xep"][i]
        channels, old = inputs(frame, use_s1=True)
        units = trace["world_state"][world]["units"]
        flagged_edges = {(u["don_vi"]["ben_goi"], u["don_vi"]["ben_duoc_goi"])
                         for u in units if u["don_vi"]["nhom"] == "canh"
                         and u["cham"].get("F_raw_len")}
        owners = {u["don_vi"]["thuc_the"] for u in units if u["don_vi"]["nhom"] != "canh"
                  and (u["cham"].get("F_raw_len") or u["cham"].get("F_raw_xuong"))}
        owners.update(b for _, b in flagged_edges)
        assert owners == {k.thuc_the for k in channels if k.co} <= inventory
        assert set(old["F_I"]) == {k.ma for k in channels if k.co}
        assert flagged_edges <= {tuple(x) for x in record["extra"]["canh"]}
        assert all(k.khoi_phat is None or type(k.khoi_phat) is int for k in channels)
        magnitudes = pha2.giai_ma_json(trace["don_vi_the_gioi"][i]["m"])
        yield world, channels, old, flagged_edges, magnitudes


def classify(channels, edges, magnitudes, flagged_edges, co_ok, enabled):
    effect = e5.phan_loai(channels, edges, bat=True, e9={
        "bat": enabled, "o_s": 10_000_000_000, "tau": 1_000_000,
        "canh_E2_bat_thuong": flagged_edges,
    })
    magnitude = {}
    for channel in channels:
        if channel.co:
            m = magnitudes.get(channel.don_vi, 0.0)
            raw, intrinsic = magnitude.get(channel.thuc_the, (0.0, 0.0))
            magnitude[channel.thuc_the] = (
                max(raw, m),
                max(intrinsic, m) if effect["F_I"][channel.ma] else intrinsic,
            )
    rank = xep_hang.xep(channels, F_I=effect["F_I"],
                        thuc_the_co_kenh_OK=co_ok, khoa_T4c=magnitude, canh=edges)
    return effect, magnitude, rank


def case(entry):
    cid = entry["source_config"]
    native, side = [records(entry[k]["path"], entry[k], {cid})[cid] for k in ("native", "trace")]
    job, trace = entry["job"], side["trace"]
    assert all(side[k] == v for k, v in job.items())
    assert native["opaque_id"] == job["opaque_id"]
    assert native["status"] in ("OK", "NO_EVIDENCE") and not side["numerical_exceptions"]
    edges = [tuple(x) for x in native["extra"]["canh"]]
    results = {}
    for i, (world, channels, old, mask, unit_m) in enumerate(frames(native, trace)):
        off, old_m, rank0 = classify(channels, edges, unit_m, mask,
                                    old["thuc_the_co_kenh_OK"], False)
        on, new_m, rank1 = classify(channels, edges, unit_m, mask,
                                    old["thuc_the_co_kenh_OK"], True)
        assert old["F_I"] == off["F_I"]
        assert encoded(old["khoa_T4c"]) == encoded(old_m)
        assert encoded(rank0) == encoded(pha2.giai_ma_json(trace["xep"][i]["ket_qua"]))
        assert rank0["blocks"] == native["worlds"][world]["blocks"]
        assert all(off["F_I"][ma] <= on["F_I"][ma] for ma in off["F_I"])
        valid = trace["world_state"][world]["valid_units"]
        verdicts = [xep_hang.verdict(r["tang"], valid) for r in (rank0, rank1)]
        assert verdicts[0] == trace["world_state"][world]["V0"]
        if world == "P":
            assert encoded(off["inherited_by"]) == encoded(native["inherited_by"])
            assert region(rank0, channels, edges, off["inherited_by"]) == native["region"]
        proposed = {row["ma"] for row in on["inherited_by"]}
        results[world] = {
            "rank": [rank0, rank1], "verdict": verdicts, "effect": [off, on],
            "m": [old_m, new_m], "mask_E2": sorted(mask), "valid_units": valid,
            "onset": {k.ma: k.khoi_phat for k in channels if k.co},
            "flagged": {k.ma: {"thuc_the": k.thuc_the, "s": k.s, "don_vi": k.don_vi,
                               "lop": k.lop, "nhom": k.nhom} for k in channels if k.co},
            "no_proposal": sorted(set(off["F_I"]) - proposed),
        }
        if world == "P":
            results[world]["region"] = [
                native["region"], region(rank1, channels, edges, on["inherited_by"])]
    return {"job": job, "index": entry["index"], "native": entry["native"],
            "trace": entry["trace"], "normalized_input_sha256": trace["normalized_input_sha256"],
            "edges": edges, "G_N": native["extra"]["G_N"], "worlds": results}


def source():
    path = "results/T-049/runs/t6-001-seal.json"
    manifest = read("results/T-050/manifest.json")
    assert digest(path) == manifest["upstream"][path]["sha256"]
    seal = read(path)
    matrix_path = "results/T-049/ma-tran.json"
    assert digest(matrix_path) == seal["matrix_sha256"]
    matrix = read(matrix_path)
    for name, expected in matrix["sources"].items():
        assert digest(name) == expected, name
    entries = sorted((e for rows in seal["entries"].values() for e in rows
                      if e["config"] == "K-thang-C"), key=lambda e: e["index"])
    assert [e["index"] for e in entries] == list(range(82))
    assert all(e["job"] == matrix["jobs"][e["index"]] for e in entries)
    return entries, matrix["K-b"]["K-thang-C"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run")
    parser.add_argument("indices", type=int, nargs="*")
    args = parser.parse_args()
    start = time.monotonic()
    entries, _ = source()
    indices = args.indices or list(range(82))
    assert len(indices) == len(set(indices)) and set(indices) <= set(range(82))
    target = OUT / args.run
    target.mkdir()
    save(target / "plan.json", {"indices": indices, "runner": digest(Path(__file__)),
                                "python": sys.version})
    for index in indices:
        before = time.monotonic()
        save(target / f"{index:02d}.json", case(entries[index]))
        print(index, f"{time.monotonic() - before:.3f}s", flush=True)
    print("PASS", len(indices), f"{time.monotonic() - start:.3f}s", flush=True)


if __name__ == "__main__":
    main()
