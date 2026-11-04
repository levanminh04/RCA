"""T12: thay đúng tập cạnh, giữ E9 theo quyết định đã chấm ở T11."""
import argparse
import time

from run_t11 import OUT, classify, digest, encoded, frames, read, records, region, save, source
from m1 import doi_chung, xep_hang
from m1_danh_gia import pha2

STATIC = {
    "RE2-TT": ("results/T-038/do-thi/thuc-the.json",
               "ee8859de3828429b729f0ae3becab2e0229dd80745f12a98046219a3d164f653"),
    "Nezha-OB": ("results/T-039/do-thi/thuc-the.json",
                 "593adabc905ff0065a5d87346c19d457451fc8658d28fb8fbecf8bb1465fea04"),
}


def controls(channels, edges, co_ok, archived):
    result = {"C-d1": doi_chung.cd1(channels, edges, co_ok),
              "C-d2": doi_chung.cd2_tu_kenh(channels, co_ok)}
    begin = time.monotonic()
    if "C-d3" in archived:
        points = {e: xep_hang.khoa_q(cs)[0] for e, cs in doi_chung._theo_e(channels).items()}
        old = archived["C-d3"]
        result["C-d3"] = dict(doi_chung.cd3(edges, points, old["dich"]),
                              dich=old["dich"], so_span_goc_A=old["so_span_goc_A"])
    return result, time.monotonic() - begin


def case(entry, baseline, enabled, static):
    cid = entry["source_config"]
    native, side = [records(entry[k]["path"], entry[k], {cid})[cid] for k in ("native", "trace")]
    trace = side["trace"]
    observed = {tuple(e) for e in native["extra"]["canh"]}
    edges = sorted(observed | static)
    baseline = pha2.giai_ma_json(baseline)
    assert baseline["trace"] == entry["trace"]
    assert baseline["normalized_input_sha256"] == trace["normalized_input_sha256"]
    for world, channels, old, mask, unit_m in frames(native, trace):
        previous = baseline["worlds"][world]
        effect, magnitude, rank = classify(channels, edges, unit_m, mask,
                                           old["thuc_the_co_kenh_OK"], enabled)
        valid = previous["valid_units"]
        baseline["worlds"][world] = {
            **previous, "rank": [previous["rank"][enabled], rank],
            "m": [previous["m"][enabled], magnitude],
            "effect": [previous["effect"][enabled], effect],
            "verdict": [previous["verdict"][enabled], xep_hang.verdict(rank["tang"], valid)],
        }
        if world != "P":
            continue
        archived = {k: v for k, v in native["extra"]["doi_chung"].items()
                    if k != "C-d3" or entry["job"]["dataset"] == "RE2-TT"}
        dc0, elapsed0 = controls(channels, sorted(observed), old["thuc_the_co_kenh_OK"], archived)
        assert encoded(dc0) == encoded(archived)
        dc1, elapsed1 = controls(channels, edges, old["thuc_the_co_kenh_OK"], archived)
        assert dc0["C-d2"] == dc1["C-d2"]
        baseline["worlds"][world]["region"] = [
            previous["region"][enabled], region(rank, channels, edges, effect["inherited_by"])]
        baseline["controls"] = [dc0, dc1]
        baseline["control_seconds"] = [elapsed0, elapsed1]
    baseline["static"] = {
        "added": sorted(static - observed), "duplicates": sorted(static & observed),
        "outside_U": sorted({e for edge in static for e in edge} - set(trace["U"])),
        "source": STATIC[entry["job"]["dataset"]][0], "revision_verified": False,
    }
    return baseline


def main(args):
    begin = time.monotonic()
    entries, _ = source()
    t11 = OUT / args.t11
    law = read(t11 / "score/law.json")["ket_hop"]
    outcome = law["ket_cuc_dung"]
    assert outcome in ("GIUP", "HAI", "KHONG_TAC_DUNG", "KHONG_DU_CA")
    assert not (outcome == "KHONG_DU_CA" and law["ket_cuc_P"] == "HAI")
    enabled = outcome in ("GIUP", "KHONG_DU_CA")
    seal = read(t11 / "sealed/seal.json")
    static = {}
    for dataset, (path, expected) in STATIC.items():
        assert digest(path) == expected
        static[dataset] = {(e["source"], e["target"]) for e in read(path)["edges"]}
    target = OUT / args.run
    target.mkdir()
    indices = args.indices or list(range(82))
    assert len(indices) == len(set(indices)) and set(indices) <= set(range(82))
    save(target / "plan.json", {"indices": indices, "runner": digest(__file__),
                                "T11": digest(t11 / "score/law.json"), "E9": enabled,
                                "source_static": STATIC})
    for index in indices:
        before = time.monotonic()
        entry = entries[index]
        filename = f"{index:02d}.json"
        assert digest(t11 / filename) == seal["inputs"][filename]
        result = case(entry, read(t11 / filename), enabled, static[entry["job"]["dataset"]])
        save(target / filename, result)
        print(index, f"{time.monotonic() - before:.3f}s", result["control_seconds"], flush=True)
    print("PASS", len(indices), f"{time.monotonic() - begin:.3f}s", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("t11")
    parser.add_argument("run")
    parser.add_argument("indices", type=int, nargs="*")
    main(parser.parse_args())
