"""Pha 1 T-053. Mỗi tiến trình đọc một cửa sổ, ghi các vế đã định trước."""
import argparse
import copy
import gzip
import hashlib
import json
import os
import platform
import sys
import time
from importlib.metadata import version
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / name) for name in
                ("src", "results/T-048/scripts", "results/T-045/scripts")]

import psutil
import chay as previous
from chay_pha1 import tat_ha_toc, xao
from m1 import adapter, chuoi, e4, runner
from p3 import nezha, selector
from z_on_dinh import NATIVE, diem_z


def configs():
    base = ROOT / "results/T-047/runs"
    old = [previous.read(base / f"b3-k-c1-{kind}-001/command.json")["configs"]
           for kind in ("that", "ce")]
    assert old[0] == old[1] and len(old[0]) == 16
    result = {}
    for source in old[0]:
        config = copy.deepcopy(source)
        config["nhanh_z"] = True
        config["ma_noi_dung"] = runner._ma_noi_dung(
            config["bat_tat"], config["tham_so_E4"], True, config["tham_so_E3"], config["tham_so_E5"])
        assert config["che_do"] == dict(cong_dem="D1", cong_phan_vi="G3", thang="E4+T4c")
        result[config["config_id"]] = config
    return result


def emit(file, data):
    file.write(previous.dump(data) + "\n")
    file.flush()


def run(args, folder):
    start = time.monotonic()
    tat_ha_toc()
    plan = previous.read(args.plan)
    for name, expected in plan["sources"].items():
        if previous.sha(ROOT / name) != expected:
            raise ValueError(f"Nguồn không khớp {name}")
    job = plan["jobs"][args.job]
    selected = configs()
    cases = {cid: selected[cid] for cid in plan["stages"][args.stage]}
    if os.environ.get("PYTHONHASHSEED") != str(args.seed):
        raise ValueError("PYTHONHASHSEED không khớp")
    with (folder / "command.json").open("x", encoding="utf-8") as f:
        emit(f, dict(argv=sys.argv, platform=platform.platform(), python=sys.version, job=job, configs=cases,
                     plan_sha256=previous.sha(args.plan), seed=args.seed, shuffle=args.shuffle,
                     versions={n: version(n) for n in ("numpy", "scipy", "pandas", "pyarrow", "psutil")}))
    contract = previous.read(ROOT / "results/T-043/hop-dong.json")
    oid = job["opaque_id"]
    with (folder / "progress.jsonl").open("x", encoding="utf-8") as progress:
        emit(progress, dict(event="load", rss=psutil.Process().memory_info().rss))
        if job["dataset"] == "RE2-TT":
            allow = selector.nap_allowlist(ROOT / "results/T-022/allowlist-dev.json")
            universe = previous.read(ROOT / "results/T-022/mappings/universe-re2tt-dev.json")["U"]
            t = job["t"]
            case = adapter.ca_re2tt(allow, oid, t, args.re_root, contract, universe)
        else:
            allow = nezha.nap_allowlist(ROOT / "results/T-026/allowlist-dev.json")
            case = adapter.ca_nezha(allow, oid, args.nz_root, contract)
            t = case["t"]
        if args.shuffle is not None:
            xao(case, args.shuffle)
        normalized = {key: case.get(key) for key in ("spans", "metrics", "logs", "inventory", "aliases", "params_ca")}
        input_sha256 = hashlib.sha256(previous.dump(dict(normalized, t=t)).encode()).hexdigest()
        del normalized
        emit(progress, dict(event="loaded", seconds=time.monotonic()-start, input_sha256=input_sha256,
                            n={k: len(case.get(k) or []) for k in ("spans", "metrics", "logs")},
                            rss=psutil.Process().memory_info().rss))
        native_path, trace_path = (folder / (n + ".jsonl.gz") for n in ("ban-ghi", "trung-gian"))
        with gzip.open(native_path, "xt", encoding="utf-8", newline="\n", compresslevel=3) as native, \
             gzip.open(trace_path, "xt", encoding="utf-8", newline="\n", compresslevel=3) as intermediate:
            cache = e4.CacheCong()
            for cid, config in cases.items():
                chuoi.CACHE = cache if not args.no_cache else e4.CacheCong()
                before = (chuoi.CACHE.trung, chuoi.CACHE.moi)
                begin, cpu = time.monotonic(), time.process_time()
                events = []
                scorer = NATIVE if args.native else lambda n, a: diem_z(n, a, record=events.append)
                with patch.object(e4, "diem_z", scorer):
                    rec, trace, clocks, effective = previous.capture(
                        case, t, config, compact=True, input_sha256=input_sha256)
                emit(native, dict(rec, opaque_id=oid))
                emit(intermediate, dict(job, config_id=cid, effective_sha256=effective, trace=trace,
                                        numerical_exceptions=events))
                memory = psutil.Process().memory_info()
                emit(progress, dict(event="record", config_id=cid, status=rec["status"],
                                    elapsed=time.monotonic()-begin, cpu_seconds=time.process_time()-cpu,
                                    rss=memory.rss, peak_rss=getattr(memory, "peak_wset", memory.rss),
                                    phases=clocks, cache_hits=chuoi.CACHE.trung-before[0],
                                    cache_misses=chuoi.CACHE.moi-before[1], exceptions=len(events)))
                if rec["status"] not in ("OK", "NO_EVIDENCE") or trace["capture_errors"] or events:
                    raise ValueError("Dừng cửa sổ vì ngoại lệ native/ứng viên, bản ghi đã lưu")
    with (folder / "kiem.json").open("x", encoding="utf-8") as f:
        emit(f, dict(records=len(cases), wall_seconds=time.monotonic()-start, cpu_seconds=time.process_time(),
                     files={p.name: dict(sha256=previous.sha(p), bytes=p.stat().st_size)
                            for p in (native_path, trace_path)}))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("plan", type=Path)
    p.add_argument("stage")
    p.add_argument("job", type=int)
    p.add_argument("run")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--shuffle", type=int)
    p.add_argument("--re-root", type=Path, default=ROOT)
    p.add_argument("--nz-root", type=Path, default=ROOT)
    p.add_argument("--native", action="store_true")
    p.add_argument("--no-cache", action="store_true")
    args = p.parse_args()
    folder = (ROOT / "results/T-053/runs" / args.run).resolve()
    if folder.parent != (ROOT / "results/T-053/runs").resolve():
        raise ValueError("Thư mục ngoài phạm vi")
    folder.mkdir()
    run(args, folder)


if __name__ == "__main__":
    main()
