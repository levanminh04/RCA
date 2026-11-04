"""Chạy T1 hai máy rồi K, chỉ khi các kiểm trước nhãn đạt."""
import argparse
import json
import shlex
import subprocess
import sys
import time
from pathlib import Path

from doi_chieu import ROOT, RUNS, read, window
from nhan_ec2 import SSH

HERE = Path(__file__).resolve().parent
REMOTE_ROOTS = ("--re-root", "/home/ubuntu/rca-t048/staging", "--nz-root", "/home/ubuntu/rca/T-032/repo")
REMOTE_PY = "/home/ubuntu/rca/T-025/envs/main/bin/python"
LOG = ROOT / "tasks/T-053-kiem-z-chay-lai-k/LOG.md"


def note(line):
    with LOG.open("a", encoding="utf-8") as f:
        f.write("\n" + line.rstrip() + "\n")


def save(path, value):
    with path.open("x", encoding="utf-8") as f:
        json.dump(value, f, ensure_ascii=False, indent=2)


def call(script, *args, capture=False):
    cmd = [sys.executable, "-B", str(HERE / script), *map(str,args)]
    return subprocess.run(cmd, check=True, text=True, capture_output=capture).stdout


def pair(names, indices, options, allocation, seconds):
    live = {}
    streams = []
    start = time.time()
    try:
        for machine, run in names.items():
            jobs = indices[machine]
            if not jobs:
                continue
            cmd = ["dieu_phoi.py", run, options[0], ",".join(map(str,jobs)),
                   "--workers", str(allocation[machine]["workers"]), "--limit", str(seconds), *options[1:]]
            if machine == "ec2":
                cmd[0] = "results/T-053/scripts/" + cmd[0]
                argv = SSH + ["-n", "cd ~/rca-t053 && " + shlex.join([REMOTE_PY, "-B", *cmd, *REMOTE_ROOTS])]
            else:
                cmd[0] = str(HERE / cmd[0])
                argv = [sys.executable, "-B", *cmd, "--reserve-ram"]
            stream = (RUNS / (run + "-launch.log")).open("xb")
            streams.append(stream)
            live[machine] = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=stream, stderr=subprocess.STDOUT)
        failed = {m: p.wait() for m,p in live.items()}
        if any(failed.values()):
            raise RuntimeError(f"Lỗi lượt {failed}, giữ log và cửa sổ đã đóng")
    finally:
        for proc in live.values():
            if proc.poll() is None:
                proc.terminate()
        for stream in streams:
            stream.close()
    if "ec2" in live:
        call("nhan_ec2.py", RUNS / (names["ec2"] + "-nhan.json"), names["ec2"])
    return time.time() - start


def run(args):
    plan = read(RUNS.parent / "ke-hoach-pha1.json")
    allocation = read(args.schedule)["machine"]
    for path in args.pilot_checks:
        assert read(path)["PASS"], str(path)
    assert len(args.pilot_checks) >= 2
    assert read(args.schedule)["forecast_seconds"] < args.deadline-time.time()
    jobs = plan["jobs"]
    pilot_sources = {"laptop":args.pilot_laptop,"ec2":args.pilot_ec2}
    stages = dict(seed0=(0,None), seed1=(1,None), seed2=(2,None), xao0=(0,0), ce=(0,None))
    all_t1 = {}
    for stage,(seed,shuffle) in stages.items():
        names = {m:f"t1-{stage}-{m}-{args.suffix}" for m in allocation}
        to_run = {}
        sources = {}
        for machine, details in allocation.items():
            selected = [i for i in details["jobs"] if (jobs[i]["window"]=="ce") == (stage=="ce")]
            reuse = set(plan["pilot_indices"]) & set(selected) if stage in ("seed0","ce") else set()
            to_run[machine] = [i for i in selected if i not in reuse]
            sources.update({str(i):pilot_sources[machine] if i in reuse else names[machine] for i in selected})
        opts = ["T1","--seed",str(seed)] + (["--shuffle",str(shuffle)] if shuffle is not None else [])
        if stage == "seed0" and args.resume_seed0:
            for index, name in sources.items():
                records = [r for r, _ in window(name, int(index)) if r["config_id"] == "K-R0"]
                assert len(records) == 1 and records[0]["status"] in ("OK", "NO_EVIDENCE")
            seconds = 0
            note("- Tiếp tục từ seed0 đã đóng, kiểm lại SHA-256 đủ 52 bản ghi trước seed1.")
        else:
            seconds = pair(names,to_run,opts,allocation,args.deadline-time.time())
        all_t1[stage] = sources
        note(f"- T1 {stage} đóng hai máy, {len(sources)} bản ghi, {seconds:.1f} giây gồm nhận bản EC2.")
    t1_map = RUNS / f"t1-phan-bo-{args.suffix}.json"
    t1_check = RUNS / f"t1-kiem-{args.suffix}.json"
    save(t1_map,all_t1)
    call("kiem_t1.py", t1_map,t1_check)
    assert read(t1_check)["PASS"]
    note(f"- T1 đạt {read(t1_check)['records']} bản ghi theo {t1_check.relative_to(ROOT).as_posix()}. Mở pha 1 K.")
    names = {m:f"k-{m}-{args.suffix}" for m in allocation}
    seconds = pair(names,{m:d["jobs"] for m,d in allocation.items()},["K"],allocation,args.deadline-time.time())
    k_map = RUNS / f"k-phan-bo-{args.suffix}.json"
    save(k_map,{str(i):names[m] for m,d in allocation.items() for i in d["jobs"]})
    out = RUNS / f"k-dong-pha1-{args.suffix}"
    seal_line = call("dong_pha1.py",k_map,out,capture=True)
    note(f"- K pha 1 đóng 832 thật + 480 giả, {seconds:.1f} giây gồm nhận bản EC2. Ba thế giới đủ trên từng bản ghi.")
    note(seal_line)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("schedule", type=Path)
    p.add_argument("deadline", type=float)
    p.add_argument("--pilot-checks", type=Path, nargs="+", required=True)
    p.add_argument("--pilot-laptop", required=True)
    p.add_argument("--pilot-ec2", required=True)
    p.add_argument("--suffix", default="001")
    p.add_argument("--resume-seed0", action="store_true")
    run(p.parse_args())


if __name__ == "__main__":
    main()
