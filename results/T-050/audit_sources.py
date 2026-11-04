"""Kiểm bản ghi baseline đã khóa với giao thức, mapping và nguồn nhãn dev."""
import sys
from collections import Counter
from pathlib import Path

from replay import ROOT, digest
from score import save
from seal import read

OUT = Path(__file__).resolve().parent
from pha2_khoi_k import NHAN


def main():
    inputs = read(OUT / "pha1-001/sidecars.json")
    t024 = read(ROOT / "results/T-024/ban-ghi-dua-vao-cham.json")
    t026 = read(ROOT / "results/T-026/ban-ghi-dua-vao-cham.json")
    m024 = {row["path"]: row for row in read(ROOT / "results/T-024/work/danh-sach-tep-cuoi.json")["results_files"]}
    m026 = read(ROOT / "results/T-026/runs/session-005/handoff-manifest.json")["files"]
    assert t024["protocol"] == "results/T-022/giao-thuc-v2.md"
    assert t024["configuration"] == "results/T-022/cau-hinh/p3-re2tt-v2.json"
    re_specs = {(r["opaque_id"], r["method"]): r for r in t024["records"]
                if r["method"] in ("baro", "tracerca", "simplerca")}
    assert len(re_specs) == 90
    re_mapping = "results/T-022/mappings/universe-re2tt-dev.json"
    assert digest(ROOT / re_mapping) == read(OUT / "pilot-plan.json")["sources"][re_mapping]
    nz_mapping = "results/T-026/mappings/ob.json"
    assert digest(ROOT / nz_mapping) == m026[nz_mapping]["sha256"] == t026["source_hashes"][nz_mapping]
    nz_plan = t026["plan_path"]
    assert digest(ROOT / nz_plan) == m026[nz_plan]["sha256"] == t026["plan_sha256"]
    expected_u = {"RE2-TT": read(ROOT / re_mapping)["U"], "Nezha-OB": read(ROOT / nz_mapping)["universe"]}
    cases = {r["job"]["opaque_id"]: r for r in inputs if r["job"]["window"] == "that"}
    label_t = {}
    for path, (ds, sha) in NHAN.items():
        assert digest(ROOT / path) == sha, path
        if ds == "Nezha-OB":
            assert sha == m026[path]["sha256"] == t026["source_hashes"][path]
        for row in read(ROOT / path)["cases"]:
            label_t[row["opaque_id"]] = row
    assert set(label_t) == set(cases)
    statuses, outside = Counter(), Counter()
    for row in read(OUT / "doi-chung-002.json")["rows"]:
        oid, ds = row["opaque_id"], row["dataset"]
        U = set(cases[oid]["U"])
        assert U == set(expected_u[ds])
        for method, proof in row["sources"].items():
            record = read(ROOT / proof["path"])
            assert digest(ROOT / proof["path"]) == proof["sha256"]
            assert record["opaque_id"] == oid and record["method"] == method and record["mode"] == "a"
            if ds == "RE2-TT":
                source = re_specs[oid, method]
                config = source["source_config"]
                assert digest(ROOT / config) == source["source_config_sha256"] == m024[config]["sha256"]
                meta = read(ROOT / config)
                assert meta["protocol"] == t024["protocol"] and meta["config"] == t024["configuration"]
                assert oid in meta["opaque_ids"] and record["config_id"] == "p3-re2tt-v2"
                assert record["window"]["t"] == label_t[oid]["inject_time"]
            else:
                assert record["config_id"] == "t026-ob-q85-native-v1"
                assert record["window"]["trace_guard_s"] == 0
                assert record["window"]["t_ns"] == label_t[oid]["t_ns"]
            if method == "simplerca":
                assert "M4" in record["method_version"]
            if method == "tracerca":
                assert "hữu hạn" in record["method_version"]
            statuses[f"{ds}|{method}|{record['status']}"] += 1
            for entity in {r["entity"] for r in record["entity_ranking"]} - U:
                outside[f"{ds}|{method}|{entity}"] += 1
    save(OUT / "kiem-nguon-doi-chung-001.json", {"records": sum(statuses.values()), "statuses": statuses,
                                                "outside_U_kept": outside})


if __name__ == "__main__":
    main()
