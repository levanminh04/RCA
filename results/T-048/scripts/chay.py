"""Pha 1 T-048. Nhận mốc đã chiếu, giữ bản ghi native và dấu vết tính điểm."""
import argparse
import copy
import hashlib
import json
import math
import platform
import os
import shutil
import subprocess
import sys
import time
from contextlib import ExitStack, redirect_stderr, redirect_stdout
from dataclasses import asdict
from importlib.metadata import version
from pathlib import Path
from unittest.mock import patch

import psutil

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results/T-048"
sys.path.insert(0, str(ROOT / "src"))

from m1 import adapter, chuoi, cong, e2, e4, hop_dong, runner, xep_hang
from m1_danh_gia.pha2 import ma_hoa_json
from p3 import nezha, selector


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    with path.open("rb") as file:
        return hashlib.file_digest(file, "sha256").hexdigest()


def dump(obj):
    def clean(value):
        if isinstance(value, float) and not math.isfinite(value):
            return {"float64": repr(value)}
        if isinstance(value, dict):
            return {k: clean(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [clean(v) for v in value]
        if isinstance(value, (set, frozenset)):
            return [clean(v) for v in sorted(value)]
        return value

    return json.dumps(ma_hoa_json(clean(obj)), ensure_ascii=False, sort_keys=True, allow_nan=False)


def configs():
    directory = ROOT / "results/T-047/runs"
    real, fake = (read(directory / f"b3-k-c1-{kind}-001/command.json")
                  for kind in ("that", "ce"))
    wanted = {"K-R0", "K-E1+E2"}
    base, alternate = ({c["config_id"]: c for c in doc["configs"] if c["config_id"] in wanted}
                       for doc in (real, fake))
    if base != alternate or base.keys() != wanted:
        raise ValueError("Cấu hình nguồn thật và C-e khác nhau")

    def make(base_id, config_id, epsilon, alpha, z=False, s1=True):
        config = copy.deepcopy(base[base_id])
        config.pop("ma_noi_dung_T047", None)
        config.update(config_id=config_id, nhanh_z=z)
        config["tham_so_E4"].update(epsilon=epsilon, alpha=alpha)
        config["che_do"]["thang"] = "E4+T4c" if s1 else "E4"
        return config

    result = {}
    for eps in (0, 0.05, 0.2):
        for alpha in (0.001, 0.01, 0.05):
            cid = f"R0-E4-S1-e{eps}-a{alpha}"
            result[cid] = make("K-R0", cid, eps, alpha)
    for base_id in sorted(wanted):
        name = base_id.removeprefix("K-")
        for score, s1 in (("E4", True), ("z", True), ("z", False)):
            if name == "R0" and score == "E4":
                continue
            cid = f"{name}-{score}-S{int(s1)}"
            result[cid] = make(base_id, cid, 0.05, 0.01, score == "z", s1)
    return result



class CacheAlpha(e4.CacheCong):
    """Chỉ bỏ alpha khỏi khóa p, còn cờ và mọi xử lý sau cổng được tính lại."""

    def theo_khoa(self, key, calculate):
        if len(key) != 5 or key[0] != "G3" or not isinstance(key[-1], tuple):
            raise ValueError("Khóa cache ngoài dạng đã kiểm")
        stripped = key[:-1] + (tuple((k, v) for k, v in key[-1] if k != "alpha"),)
        return super().theo_khoa(stripped, calculate)

    def p(self, unit, anomalous, normal, direction, params):
        # Đường G0 độc lập không dùng trong chế độ G3, vẫn giữ khóa gốc.
        return super().p(unit, anomalous, normal, direction, params)


def source_hashes():
    entries = {}
    for package in ("m1", "m1_danh_gia", "p3"):
        for path in sorted((ROOT / "src" / package).glob("*.py")):
            entries[path.relative_to(ROOT).as_posix()] = sha(path)
    for relative in (
        "results/T-043/hop-dong.json", "results/T-022/allowlist-dev.json",
        "results/T-022/mappings/universe-re2tt-dev.json", "results/T-026/allowlist-dev.json",
        "results/T-047/runs/b3-k-c1-that-001/command.json",
        "results/T-047/runs/b3-k-c1-ce-001/command.json",
    ):
        entries[relative] = sha(ROOT / relative)
    return entries


def verify_sources(plan):
    actual = source_hashes()
    if plan.get("source_sha256") != actual:
        raise ValueError("Nguồn khác manifest của kế hoạch")
    return actual


def capture(case, t, config, *, compact=False, input_sha256=None):
    params = runner._params(config, case)
    aliases = case.get("aliases") or {}
    inventory = case.get("inventory") or []
    forbidden = [case["opaque_id"], *case.get("chuoi_cam", [])]
    if hop_dong.vi_pham_gia_tri(params, aliases, inventory, forbidden):
        raise ValueError("Trường cấm trong đầu vào")
    trace = {"phan_vi": {}, "dem": [], "xep": [], "gan_canh": [], "don_vi_the_gioi": []}
    clock = {}
    if compact:
        trace["world_state"] = {}
        trace["U"] = sorted(inventory)
        trace["normalized_input_sha256"] = input_sha256 or hashlib.sha256(dump({
            "spans": case["spans"], "metrics": case.get("metrics") or [],
            "logs": case.get("logs") or [], "inventory": inventory, "aliases": aliases,
            "params_ca": case.get("params_ca"), "t": t,
        }).encode()).hexdigest()
    if compact:
        trace.update(cong_G3={}, capture_errors=[])

    def gate_input(args, kwargs, result):
        unit, observation, time_ns, _ = args
        fields = ("moc_N_cong", "moc_A_cong", "moc_A_ns")
        trace["cong_G3"][unit["ma"]] = {
            "moc_sha256_i64_le": {k: hashlib.sha256(e4.np.asarray(unit[k], dtype="<i8").tobytes()).hexdigest()
                                  for k in fields if k in unit},
            "bien": cong.bien_phia(observation, time_ns),
            "nguon_qs": unit["nguon_qs"],
        }

    def wrap(module, name, collect):
        native = getattr(module, name)

        def wrapped(*args, **kwargs):
            start = time.monotonic()
            result = native(*args, **kwargs)
            clock[name] = clock.get(name, 0.0) + time.monotonic() - start
            collect(args, kwargs, result)
            return result

        return patch.object(module, name, wrapped)

    def quantile(args, kwargs, result):
        normal, anomalous, m, _ = args
        unit = kwargs["khoa_don_vi"]
        trace["phan_vi"][unit] = {
            "mau_sha256": [hashlib.sha256(dump(list(x)).encode()).hexdigest()
                           for x in (normal, anomalous)],
            "n_N": len(normal), "n_A": len(anomalous), "m_toi_thieu": m,
            "cuc_tri": [min(anomalous), max(anomalous)] if len(anomalous) else [],
            "e4": result,
        }
        if result["trang_thai"] == "OK":
            with e4.np.errstate(over="ignore", invalid="ignore", divide="ignore"):
                if compact:
                    try:
                        trace["phan_vi"][unit]["z"] = e4.diem_z(normal, anomalous)
                    except (TypeError, ValueError, OverflowError) as exc:
                        trace["capture_errors"].append({"unit": unit, "z": str(exc)})
                else:
                    trace["phan_vi"][unit]["z"] = e4.diem_z(normal, anomalous)
            if compact and "z" in trace["phan_vi"][unit]:
                from kiem import oracle_phan_vi
                trace["phan_vi"][unit]["oracle"] = oracle_phan_vi(
                    normal, anomalous, m, args[3], kwargs["huong_cham"], result,
                    trace["phan_vi"][unit]["z"])
                values = sorted(float(x) for x in anomalous if x is not None and math.isfinite(float(x)))
                trace["phan_vi"][unit]["A_extrema"] = {
                    "min2": values[:2], "max2": values[-2:],
                    "min_count": values.count(values[0]), "max_count": values.count(values[-1]),
                }

    def count(args, kwargs, result):
        from kiem import oracle_dem
        oracle_dem(args, kwargs, result)
        trace["dem"].append([args, kwargs, result])

    def rank(args, kwargs, result):
        if compact:
            frame = sys._getframe(2)
            if frame.f_code is not chuoi._chay.__code__:
                raise ValueError("Không lấy được khung chuỗi ghim")
            world = frame.f_locals.get("w")
            if world in ("P", "S_lo", "S_hi") and world not in trace["world_state"]:
                units = frame.f_locals["worlds"][world]["don_vi"]
                omit = {"N", "A", "moc_N", "moc_A", "moc_N_cong", "moc_A_cong", "moc_A_ns"}
                trace["world_state"][world] = {
                    "units": [{"don_vi": {k: v for k, v in u.items() if k not in omit}, "cham": scored}
                              for u, scored in units],
                    "N1": sum(tier == 1 for tier in result["tang"].values()),
                    "valid_units": sum(bool(score.get("hop_le")) and u["thuc_the"] in set(inventory)
                                       for u, score in units),
                }
                state = trace["world_state"][world]
                state["V0"] = xep_hang.verdict(result["tang"], state["valid_units"])
            del frame
        trace["xep"].append({
            "kenh": [dict(asdict(channel), ma=channel.ma) for channel in args[0]],
            "F_I": kwargs["F_I"], "co_OK": kwargs["thuc_the_co_kenh_OK"],
            "m": kwargs.get("khoa_T4c"), "ket_qua": result,
        })

    def magnitude(args, kwargs, result):
        omit = {"N", "A", "moc_N", "moc_A"}
        if compact:
            omit.update(("moc_N_cong", "moc_A_cong", "moc_A_ns"))
        units = [{"don_vi": {k: v for k, v in u.items() if k not in omit},
                  "cham": scored} for u, scored in args[0]]
        trace["don_vi_the_gioi"].append({"don_vi": units, "m": result[0]})

    with ExitStack() as stack:
        if compact:
            stack.enter_context(wrap(chuoi, "_ham_G3", gate_input))
        stack.enter_context(wrap(e4, "cham_phan_vi", quantile))
        stack.enter_context(wrap(e4, "cham_dem", count))
        stack.enter_context(wrap(e2, "gan_canh", lambda a, k, r: trace["gan_canh"].append(r)))
        stack.enter_context(wrap(chuoi, "_khoa_T4c", magnitude))
        stack.enter_context(wrap(xep_hang, "xep", rank))
        record = chuoi.chay(case["spans"], case.get("metrics") or [], case.get("logs") or [],
                            inventory, aliases, t, params)
    return record, trace, clock, hashlib.sha256(dump(params).encode()).hexdigest()


def run(args):
    folder = (OUT / "runs" / args.run_id).resolve()
    if folder.parent != (OUT / "runs").resolve():
        raise ValueError("Mã lượt không hợp lệ")
    folder.mkdir(parents=True)
    start = time.monotonic()
    with (folder / "stdout.log").open("x", encoding="utf-8") as stdout, (folder / "stderr.log").open(
        "x", encoding="utf-8"
    ) as stderr, redirect_stdout(stdout), redirect_stderr(stderr):
        try:
            run_cases(args, folder, start)
        except Exception:
            import traceback
            traceback.print_exc()
            raise


def run_cases(args, folder, start):
    document = read(args.plan)
    plan = copy.deepcopy(document.get("plan", document))
    sources = verify_sources(plan)
    if args.stage is not None:
        plan["configs"] = plan["stages"][args.stage]
    if args.dataset is not None:
        plan["jobs"] = [j for j in plan["jobs"] if j["dataset"] == args.dataset]
    if args.machine:
        plan["jobs"] = [j for j in plan["jobs"] if plan["allocation"][j["opaque_id"]] == args.machine]
    if args.case is not None:
        plan["jobs"] = [job for job in plan["jobs"] if job["opaque_id"] == args.case
                        and (args.window is None or job["window"] == args.window)]
    if args.configuration is not None:
        if args.configuration not in plan["configs"]:
            raise ValueError("Cấu hình ngoài kế hoạch")
        plan["configs"] = [args.configuration]
    if not plan["jobs"]:
        raise ValueError("Không có ca theo bộ lọc")
    re = selector.nap_allowlist(ROOT / "results/T-022/allowlist-dev.json")
    nz = nezha.nap_allowlist(ROOT / "results/T-026/allowlist-dev.json")
    contract = read(ROOT / "results/T-043/hop-dong.json")
    universe = read(ROOT / "results/T-022/mappings/universe-re2tt-dev.json")["U"]
    declared = configs()
    selected = {cid: declared[cid] for cid in plan["configs"]}
    (folder / "command.json").write_text(dump({
        "argv": sys.argv, "platform": platform.platform(), "python": sys.version,
        "versions": {p: version(p) for p in ("numpy", "scipy", "pandas", "pyarrow")},
        "plan_sha256": sha(args.plan), "script_sha256": sha(Path(__file__)),
        "configs": selected, "plan": plan, "source_sha256": sources,
        "script_source": Path(__file__).read_text(encoding="utf-8"),
        "cache_alpha": args.cache_alpha, "compact": args.compact,
        "tool_sources": {path.name:dict(sha256=sha(path),source=path.read_text(encoding="utf-8"))
                         for path in Path(__file__).parent.glob("*.py")},
    }) + "\n", encoding="utf-8")

    def emit(file, value):
        file.write(dump(value) + "\n")
        file.flush()

    with (folder / "progress.jsonl").open("x", encoding="utf-8") as progress, (
        folder / "ban-ghi.jsonl"
    ).open("x", encoding="utf-8", newline="\n") as native, (
        folder / "trung-gian.jsonl"
    ).open("x", encoding="utf-8", newline="\n") as intermediates:
        for job in plan["jobs"]:
            dataset, oid, kind = (job[key] for key in ("dataset", "opaque_id", "window"))
            if time.monotonic() - start >= args.limit:
                raise TimeoutError("Đã tới trần lượt")
            emit(progress, dict(job, event="load"))
            load = time.monotonic()
            if dataset == "RE2-TT" and kind in ("that", "ce"):
                t = job["t"]
                case = adapter.ca_re2tt(re, oid, t, args.re_root, contract, universe)
            elif dataset == "Nezha-OB" and kind == "that":
                case = adapter.ca_nezha(nz, oid, args.nz_root, contract)
                t = case["t"]
            else:
                raise ValueError("Cửa sổ không hợp lệ")
            emit(progress, dict(job, event="loaded", elapsed=time.monotonic() - load))
            input_sha256 = hashlib.sha256(dump({
                "spans":case["spans"], "metrics":case.get("metrics") or [], "logs":case.get("logs") or [],
                "inventory":case.get("inventory") or [], "aliases":case.get("aliases") or {},
                "params_ca":case.get("params_ca"), "t":t,
            }).encode()).hexdigest()
            case_cache = CacheAlpha() if args.cache_alpha else None
            for cid, config in selected.items():
                if time.monotonic() - start >= args.limit:
                    raise TimeoutError("Đã tới trần lượt")
                chuoi.CACHE = case_cache if case_cache is not None else e4.CacheCong()
                emit(progress, dict(job, event="start_record", config_id=cid))
                begin = time.monotonic()
                cpu = time.process_time()
                rec, trace, clock, effective = capture(case, t, config, compact=args.compact, input_sha256=input_sha256)
                cpu = time.process_time() - cpu
                emit(native, dict(rec, opaque_id=oid))
                emit(intermediates, dict(job, config_id=cid, effective_sha256=effective, trace=trace))
                memory = psutil.Process().memory_info()
                emit(progress, dict(job, event="record", config_id=cid, status=rec["status"],
                                    elapsed=time.monotonic() - begin, cpu_seconds=cpu, phase_seconds=clock,
                                    rss=memory.rss, cache_hits=chuoi.CACHE.trung, cache_misses=chuoi.CACHE.moi))
                if rec["status"] not in ("OK", "NO_EVIDENCE") or trace.get("capture_errors"):
                    raise ValueError("Bản ghi native hoặc dấu vết lỗi, đã giữ trước khi dừng")
    (folder / "kiem.json").write_text(dump({
        "wall_seconds": time.monotonic() - start, "cpu_seconds": time.process_time(),
        "rss": psutil.Process().memory_info().rss,
        "records": len(plan["jobs"]) * len(selected),
        "phase1_sha256": sha(folder / "ban-ghi.jsonl"),
        "intermediate_sha256": sha(folder / "trung-gian.jsonl"),
    }) + "\n", encoding="utf-8")


def control(args):
    """Mỗi việc có thư mục độc lập, giám sát nguồn, RAM, đĩa và lỗi từ đầu."""
    parent = (OUT / "runs" / args.run_id).resolve()
    if parent.parent != (OUT / "runs").resolve() or not 1 <= args.workers <= 4:
        raise ValueError("Thư mục hoặc số worker ngoài phạm vi")
    parent.mkdir(parents=True)
    original = read(args.plan)
    plan = copy.deepcopy(original.get("plan", original))
    sources = verify_sources(plan)
    if args.stage:
        plan["configs"] = plan["stages"][args.stage]
    if args.dataset:
        plan["jobs"] = [j for j in plan["jobs"] if j["dataset"] == args.dataset]
    if args.machine:
        plan["jobs"] = [j for j in plan["jobs"] if plan["allocation"][j["opaque_id"]] == args.machine]
    if args.case:
        plan["jobs"] = [j for j in plan["jobs"] if j["opaque_id"] == args.case
                        and (args.window is None or j["window"] == args.window)]
    if args.configuration:
        plan["configs"] = [args.configuration]
    if not plan["jobs"] or not plan["configs"]:
        raise ValueError("Kế hoạch rỗng")
    if len({(j["opaque_id"], j["window"]) for j in plan["jobs"]}) != len(plan["jobs"]):
        raise ValueError("Trùng công việc")
    command = dict(argv=sys.argv, plan=plan, source_sha256=sources,
                   script_sha256=sha(Path(__file__)), workers=args.workers,
                   script_source=Path(__file__).read_text(encoding="utf-8"),
                   root=str(ROOT), start_utc=time.time(), seed=os.getenv("PYTHONHASHSEED"))
    (parent / "command.json").write_text(dump(command)+"\n", encoding="utf-8")
    started = time.monotonic()
    active, finished, next_job = {}, [], 0
    peak = 0
    failure = None
    with (parent / "progress.jsonl").open("x", encoding="utf-8") as progress, (
        parent / "stdout.log").open("x", encoding="utf-8") as stdout, (
        parent / "stderr.log").open("x", encoding="utf-8") as stderr:

        def event(**fields):
            progress.write(dump(dict(elapsed=time.monotonic()-started, **fields))+"\n")
            progress.flush()

        try:
            while active or next_job < len(plan["jobs"]):
                if time.monotonic()-started > args.limit:
                    raise TimeoutError("Đã tới trần controller")
                free = shutil.disk_usage(OUT).free
                available = psutil.virtual_memory().available
                if free < 700_000_000 or available < 450_000_000:
                    raise MemoryError(f"Tài nguyên không đủ: RAM={available}, disk={free}")
                while len(active) < args.workers and next_job < len(plan["jobs"]):
                    job = plan["jobs"][next_job]
                    child = f"{args.run_id}-{next_job:03d}"
                    argv = [
                        sys.executable, "-B", str(Path(__file__)), child, str(parent/"command.json"),
                        "--case", job["opaque_id"], "--window", job["window"], "--limit",
                        str(min(3600, args.limit)), "--re-root", str(args.re_root),
                        "--nz-root", str(args.nz_root), "--compact",
                    ]
                    if args.cache_alpha:
                        argv.append("--cache-alpha")
                    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0",
                               OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1")
                    proc = subprocess.Popen(argv, cwd=ROOT, env=env, stdout=stdout, stderr=stderr)
                    active[proc.pid] = (proc, child, job)
                    event(event="launched", child=child, pid=proc.pid, job=job)
                    next_job += 1
                rss = psutil.Process().memory_info().rss
                for pid, (proc, child, job) in list(active.items()):
                    if proc.poll() is None:
                        try:
                            process = psutil.Process(pid)
                            rss += process.memory_info().rss
                            rss += sum(p.memory_info().rss for p in process.children(recursive=True)
                                       if p.is_running())
                        except psutil.NoSuchProcess:
                            pass
                        continue
                    if proc.returncode != 0:
                        raise RuntimeError(f"Lượt {child} kết thúc lỗi {proc.returncode}")
                    meta = read(OUT/"runs"/child/"kiem.json")
                    for name, key in (("ban-ghi.jsonl", "phase1_sha256"),
                                      ("trung-gian.jsonl", "intermediate_sha256")):
                        if sha(OUT/"runs"/child/name) != meta[key]:
                            raise ValueError(f"Hash lượt {child} lệch")
                    event(event="finished", child=child, meta=meta)
                    finished.append(child)
                    del active[pid]
                peak = max(peak, rss)
                event(event="resources", worker_rss=rss, available=available, free_disk=free,
                      running=len(active), completed=len(finished), total=len(plan["jobs"]))
                if active:
                    time.sleep(2)
        except BaseException as exc:
            failure = repr(exc)
            event(event="failed", error=failure)
            for proc, child, job in active.values():
                if proc.poll() is None:
                    root_process = psutil.Process(proc.pid)
                    for descendant in root_process.children(recursive=True):
                        descendant.terminate()
                    proc.terminate()
            for proc, _, _ in active.values():
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
            raise
        finally:
            status = dict(success=failure is None, error=failure, finished=finished,
                          wall_seconds=time.monotonic()-started, peak_worker_rss=peak,
                          dispatched=next_job, jobs=len(plan["jobs"]))
            (parent/"kiem.json").write_text(dump(status)+"\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_id")
    parser.add_argument("plan", type=Path)
    parser.add_argument("--re-root", type=Path, default=ROOT)
    parser.add_argument("--nz-root", type=Path, default=ROOT)
    parser.add_argument("--limit", type=int, required=True)
    parser.add_argument("--compact", action="store_true")
    parser.add_argument("--case")
    parser.add_argument("--window", choices=("that", "ce"))
    parser.add_argument("--configuration")
    parser.add_argument("--dataset", choices=("RE2-TT", "Nezha-OB"))
    parser.add_argument("--stage")
    parser.add_argument("--machine", choices=("ec2", "laptop"))
    parser.add_argument("--cache-alpha", action="store_true")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--control", action="store_true")
    args = parser.parse_args()
    if args.control:
        control(args)
    else:
        run(args)


if __name__ == "__main__":
    main()
