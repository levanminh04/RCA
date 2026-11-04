"""Ghim nguồn và kiểm tái tạo S1 trước khi đóng gói đầu vào phát lại."""
import gzip
import json
import sys
from collections import Counter

from replay import ROOT, WORLDS, digest, encode, inputs, region, xep_hang

OUT = ROOT / "results/T-050"
sys.path.insert(0, str(ROOT / "results/T-049/scripts"))
from chuan_bi import verified
from kiem_tai_su_dung import records


def main(folder):
    folder.mkdir()
    seal = verified("T-049", "results/T-049/runs/t6-001-seal.json")
    matrix = verified("T-049", "results/T-049/ma-tran.json")
    assert seal["matrix_sha256"] == digest(ROOT / "results/T-049/ma-tran.json")
    base = matrix["K-b"]["K-thang-C"]
    assert base["bat_tat"] == dict(E1="U", E2="C", E3=False, E3b=False, E5=True,
                                  E6="a", E9=False, T12=False)
    for name, sha in matrix["sources"].items():
        assert digest(ROOT / name) == sha, name
    entries = sorted((e for rows in seal["entries"].values() for e in rows
                      if e["config"] == "K-thang-C"), key=lambda e: e["index"])
    assert [e["index"] for e in entries] == list(range(82))
    assert Counter(e["job"]["window"] for e in entries) == {"that": 52, "ce": 30}
    index = []
    for e in entries:
        job = e["job"]
        assert job == matrix["jobs"][e["index"]]
        cid = e["source_config"]
        rec, side = [records(e[k]["path"], e[k], {cid})[cid] for k in ("native", "trace")]
        assert rec["opaque_id"] == job["opaque_id"]
        assert all(side[k] == v for k, v in job.items())
        assert rec["status"] in ("OK", "NO_EVIDENCE") and set(rec["worlds"]) == set(WORLDS)
        assert rec["extra"]["che_do"] == base["che_do"]
        trace = side["trace"]
        assert not trace["capture_errors"] and not side["numerical_exceptions"]
        frames, states, ranks = {}, {}, {}
        edges = rec["extra"]["canh"]
        for world, raw in zip(WORLDS, trace["xep"][:3], strict=True):
            frame = {k: raw[k] for k in ("kenh", "F_I", "co_OK", "m")}
            channels, kwargs = inputs(frame, use_s1=True)
            s1 = xep_hang.xep(channels, **kwargs)
            assert encode(s1) == encode(raw["ket_qua"]), (e["index"], world, "rank")
            assert s1["blocks"] == rec["worlds"][world]["blocks"]
            state = {k: trace["world_state"][world][k] for k in ("N1", "V0", "valid_units")}
            assert sum(v == 1 for v in s1["tang"].values()) == state["N1"]
            assert xep_hang.verdict(s1["tang"], state["valid_units"]) == state["V0"]
            assert set(s1["tang"]) <= set(trace["U"])
            if world == "P":
                assert region(s1, channels, [tuple(edge) for edge in edges],
                              rec["inherited_by"]) == rec["region"], e["index"]
            frames[world], states[world], ranks[world] = frame, state, raw["ket_qua"]
        data = {"frames": frames, "state": states, "edges": edges, "status": rec["status"],
                "inherited": rec["inherited_by"], "U": trace["U"]}
        path = folder / f"{e['index']:02d}.json.gz"
        path.write_bytes(gzip.compress(encode({"input": data, "baseline": ranks}), mtime=0))
        positive = [row[0] for row in ranks["P"]["K_I"].values() if row[0] > 0]
        index.append({**e, "file": path.name, "sha256": digest(path), "bytes": path.stat().st_size,
                      "normalized_input_sha256": trace["normalized_input_sha256"],
                      "positive": len(positive), "max_score": max(positive, default=0),
                      "edges": len(edges)})
        print(e["index"], "PASS S1", flush=True)
    (folder / "index.json").write_bytes(encode(index))


if __name__ == "__main__":
    main(OUT / sys.argv[1])
