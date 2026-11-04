"""Giám sát lượt T-053 theo cửa sổ và lưu cả tiến trình thất bại."""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import psutil

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "runs"


def emit(stream, **data):
    stream.write(json.dumps(dict(epoch=time.time(), **data)) + "\n")
    stream.flush()


def measure(proc):
    try:
        processes = [proc, *proc.children(recursive=True)]
        rss = sum(p.memory_info().rss for p in processes)
        io = [p.io_counters() for p in processes]
        cpu = [p.cpu_times() for p in processes]
        return dict(rss=rss, read_bytes=sum(x.read_bytes for x in io),
                    write_bytes=sum(x.write_bytes for x in io),
                    cpu_seconds=sum(x.user+x.system for x in cpu))
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return {}


def run(args):
    folder = OUT / args.name
    folder.mkdir()
    start = time.monotonic()
    jobs = [int(i) for i in args.jobs.split(",")]
    env = dict(os.environ, PYTHONHASHSEED=str(args.seed), OPENBLAS_NUM_THREADS="1",
               OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", NUMEXPR_NUM_THREADS="1")
    pending = list(jobs)
    plan = json.loads((HERE.parent / "ke-hoach-pha1.json").read_bytes())
    live = {}
    errors = []
    with (folder / "progress.jsonl").open("x", encoding="utf-8") as log:
        emit(log, event="start", jobs=jobs, workers=args.workers, limit=args.limit, argv=sys.argv)
        try:
            while pending or live:
                if time.monotonic() - start >= args.limit:
                    raise TimeoutError("Đã tới trần lượt")
                while pending and len(live) < args.workers and not errors:
                    available = psutil.virtual_memory().available
                    if live and available < 600 * 1024**2:
                        break
                    def reserve(i):
                        job = plan["jobs"][i]
                        if job["dataset"] == "Nezha-OB":
                            return 700 * 1024**2
                        size = job["source_bytes"]
                        return (650 if size <= 10e6 else 1450 if size <= 26e6 else 2100) * 1024**2

                    if args.reserve_ram:
                        unallocated = sum(max(0,reserve(i)-measure(probe).get("rss", 0))
                                          for i,(_,probe) in live.items())
                        position = next((index for index,i in enumerate(pending)
                                         if available-unallocated-reserve(i) >= 1200*1024**2), None)
                        if position is None:
                            break
                    else:
                        position = 0
                    job = pending.pop(position)
                    name = f"{args.name}-{job:02d}"
                    cmd = [sys.executable, "-B", str(HERE / "pha1.py"), str(HERE.parent / "ke-hoach-pha1.json"),
                           args.stage, str(job), name, "--seed", str(args.seed)]
                    if args.shuffle is not None:
                        cmd += ["--shuffle", str(args.shuffle)]
                    if args.re_root:
                        cmd += ["--re-root", args.re_root]
                    if args.nz_root:
                        cmd += ["--nz-root", args.nz_root]
                    for flag in ("native", "no_cache"):
                        if getattr(args, flag):
                            cmd.append("--" + flag.replace("_", "-"))
                    with (folder / f"{name}.stdout.log").open("xb") as stdout, \
                         (folder / f"{name}.stderr.log").open("xb") as stderr:
                        proc = subprocess.Popen(cmd, stdout=stdout, stderr=stderr, env=env)
                    live[job] = (proc, psutil.Process(proc.pid))
                    emit(log, event="launch", job=job, pid=proc.pid, command=cmd)
                for job, (proc, probe) in list(live.items()):
                    code = proc.poll()
                    if code is not None:
                        del live[job]
                        emit(log, event="exit", job=job, code=code)
                        if code:
                            errors.append(job)
                    else:
                        emit(log, event="worker", job=job, **measure(probe))
                emit(log, event="host", available=psutil.virtual_memory().available,
                     disk_free=shutil.disk_usage(OUT).free, cpu_percent=psutil.cpu_percent())
                if errors and not live:
                    raise RuntimeError(f"Lượt lỗi tại {errors}")
                if pending or live:
                    time.sleep(2)
        finally:
            for proc, probe in live.values():
                for child in probe.children(recursive=True):
                    child.terminate()
                proc.terminate()
            emit(log, event="end", elapsed=time.monotonic()-start, errors=errors, pending=pending)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("name")
    p.add_argument("stage", choices=["pilot", "T1", "K"])
    p.add_argument("jobs")
    p.add_argument("--workers", type=int, required=True)
    p.add_argument("--limit", type=float, required=True)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--shuffle", type=int)
    p.add_argument("--re-root")
    p.add_argument("--nz-root")
    p.add_argument("--native", action="store_true")
    p.add_argument("--no-cache", action="store_true")
    p.add_argument("--reserve-ram", action="store_true")
    args = p.parse_args()
    if Path(args.name).name != args.name or args.workers < 1:
        p.error("Tên lượt hoặc số tiến trình sai")
    run(args)


if __name__ == "__main__":
    main()
