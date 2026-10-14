"""T-032 TraceRCA trên EC2: vòng lặp tuần tự gọi replay_tracerca_v3 đã ghim (Q-125, Q-108).

Thay bộ controller/launcher/verifier nháp của lượt cohort. Không đổi wrapper, capture, adapter,
phương pháp, tiêu chí khớp, tập ca. Wrapper tự kiểm hash nguồn, chạy một lần có quan sát,
so tuyệt đối với bản đóng băng và kiểm capture. Driver chỉ:
  - đi theo plan-52 đã khóa, dùng lại ba ca đã đóng, không chạy lại ca nào;
  - một worker, dừng toàn nhánh ở lỗi đầu tiên, không retry/skip/tolerance;
  - trần Q-125: 600 s và 150 MiB mỗi ca; 4,5 giờ và 2,5 GiB cả lượt;
    cây tiến trình không quá 6 GiB RSS và RAM trống không dưới 1 GiB;
  - --max-cases N để dừng ở checkpoint (ca mới đầu, route mới) rồi chạy tiếp bằng lệnh sau.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import traceback
from pathlib import Path

BASE = Path("/home/ubuntu/rca/T-032")
OUT = BASE / "runs/tracerca-cohort-simple-001"
PYTHON = Path("/home/ubuntu/rca/T-025/envs/main/bin/python")
WRAPPER = BASE / "scripts/replay_tracerca_v3.py"
PLAN = BASE / "sources/tracerca-plan-52.json"
PINS = {
    "scripts/replay_tracerca_v3.py": "3127b73285cbce3cf7ba68483a7ca5d651007e097b5d913ac7544dc76ef064ee",
    "scripts/capture_tracerca.py": "a883dfddc56abbb68447052b40764613b10b86621b9e8c80d86e143976f7ebe4",
    "scripts/replay_microrank.py": "193166089f7d0bf30a2f81551c374bec610f705241f6ad495aa5ff7181126562",
    "scripts/capture_microrank.py": "b842b4be0d92470f1fc673e2afb30b5b0b76781c211a4b99ff6518c648b00c8b",
    "sources/tracerca-plan-52.json": "2e26428c26ef2fd699a72abdd9e30662b7cbda61f97aec3c3eca1e33d89b2ebe",
}
REUSED = {"posthoc": BASE / "runs/tracerca-path-pilots-002/posthoc",
          "re2-ok": BASE / "runs/tracerca-path-pilots-002/re2-ok",
          "nezha-ok": BASE / "runs/tracerca-path-pilots-002/nezha-ok"}
MAX_CASE_S = 600.0
MAX_CASE_BYTES = 150 * 1024 * 1024
MAX_RUN_S = 4.5 * 3600
MAX_RUN_BYTES = 5 * 1024 * 1024 * 1024 // 2
MAX_TREE_RSS = 6 * 1024 * 1024 * 1024
MIN_AVAILABLE = 1024 * 1024 * 1024
POLL_S = 1.0
EXCLUDED_FIELDS = ("run_id", "cost")


class Stop(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise Stop(message)


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def dump_new(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")


def append(path, value):
    with Path(path).open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(value, ensure_ascii=False) + "\n")


def tree_bytes(directory):
    total = 0
    for parent, _dirs, files in os.walk(directory):
        for name in files:
            path = Path(parent) / name
            if not path.is_symlink():
                total += path.stat().st_size
    return total


def manifest(directory, excluded=()):
    directory = Path(directory)
    return [{"path": p.relative_to(directory).as_posix(), "bytes": p.stat().st_size, "sha256": sha(p)}
            for p in sorted(directory.rglob("*")) if p.is_file() and p.relative_to(directory).as_posix() not in excluded]


def verify_manifest(directory, rows, excluded):
    directory = Path(directory)
    listed = set()
    for row in rows:
        path = directory / row["path"]
        require(path.is_file() and path.stat().st_size == row["bytes"] and sha(path) == row["sha256"],
                "file đã đóng bị đổi: " + str(path))
        listed.add(row["path"])
    actual = {p.relative_to(directory).as_posix() for p in directory.rglob("*") if p.is_file()}
    require(actual == listed | set(excluded), "tập file khác manifest đã đóng: " + str(directory))


def bit_differences(a, b, path=""):
    if type(a) is not type(b):
        return [path + ": kiểu khác"]
    if isinstance(a, dict):
        out = []
        for key in sorted(set(a) | set(b)):
            if path == "" and key in EXCLUDED_FIELDS:
                continue
            if key not in a or key not in b:
                out.append(path + "/" + key + ": thiếu một bên")
            else:
                out += bit_differences(a[key], b[key], path + "/" + key)
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return [path + ": độ dài khác"]
        out = []
        for index, (x, y) in enumerate(zip(a, b)):
            out += bit_differences(x, y, path + "/" + str(index))
        return out
    if isinstance(a, float):
        return [] if a.hex() == b.hex() else [path + ": float khác"]
    return [] if a == b else [path + ": giá trị khác"]


def checked(directory, row):
    """Kiểm một thư mục ca đã đóng (mới hoặc dùng lại): PASS, đúng nguồn, khớp bit với bản đóng băng."""
    check = read(Path(directory) / "check.json")
    require(check.get("status") == "PASS" and check.get("differences") == [], "check không PASS: " + str(directory))
    require(not (Path(directory) / "failure-after-check.json").exists(), "có lỗi sau check: " + str(directory))
    require((check["dataset"], check["opaque_id"]) == (row["dataset"], row["opaque_id"])
            and check["frozen_sha256"] == row["frozen_sha256"] and check["frozen_status"] == row["source_status"]
            and check["replay_status"] == row["source_status"], "định danh/nguồn/trạng thái khác plan: " + str(directory))
    verify_manifest(directory, check["artifact_manifest"], check.get("manifest_excludes", ["check.json"]))
    frozen_path = BASE / "repo" / row["frozen_path"]
    require(sha(frozen_path) == row["frozen_sha256"], "bản đóng băng trên EC2 khác plan")
    # Ca ERROR đã kiểm hồi cứu (posthoc) giữ bản ghi ở thư mục lượt gốc, không chép sang thư mục posthoc.
    record_dir = Path(directory) if (Path(directory) / "ban-ghi-0.json").is_file() else Path(check["original_run"])
    differences = bit_differences(read(frozen_path), read(record_dir / "ban-ghi-0.json"))
    require(not differences, "bản ghi phát lại lệch bản đóng băng: " + "; ".join(differences[:5]))
    capture = check.get("capture_check") or {}
    return {"dataset": row["dataset"], "opaque_id": row["opaque_id"], "source_status": row["source_status"],
            "result": "exact" if row["source_status"] == "OK" else "non_OK_exact",
            "capture_check_pass": capture.get("pass"), "capture_status": check.get("capture_status"),
            "check_sha256": sha(Path(directory) / "check.json"), "path": str(directory)}


def kill_tree(psutil, pid):
    try:
        parent = psutil.Process(pid)
        targets = parent.children(recursive=True) + [parent]
    except psutil.NoSuchProcess:
        return
    for process in targets:
        try:
            process.kill()
        except psutil.NoSuchProcess:
            pass


def tree_rss(psutil, pid):
    try:
        parent = psutil.Process(pid)
        processes = [parent] + parent.children(recursive=True)
    except psutil.NoSuchProcess:
        return 0
    total = 0
    for process in processes:
        try:
            total += process.memory_info().rss
        except psutil.NoSuchProcess:
            pass
    return total


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--segment", required=True, help="mã đoạn mới, ví dụ 001")
    parser.add_argument("--max-cases", type=int, default=0, help="số ca mới tối đa của đoạn; 0 là chạy hết")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    import psutil
    require(Path(sys.executable).resolve() == PYTHON.resolve() and os.environ.get("PYTHONHASHSEED") == "0",
            "phải chạy bằng Python EC2 đã duyệt với PYTHONHASHSEED=0")
    for relative, expected in PINS.items():
        require(sha(BASE / relative) == expected, "ghim khác: " + relative)
    rows = read(PLAN)["rows"]
    require(len(rows) == 52 and len({(r["dataset"], r["opaque_id"]) for r in rows}) == 52, "plan không đủ 52 ca")
    results = []
    for row in rows:
        reused = row.get("replay_phase_already_valid")
        directory = REUSED[reused] if reused else OUT / "cases" / row["dataset"] / row["opaque_id"]
        if reused or directory.exists():
            item = checked(directory, row)  # thư mục ca dở/hỏng làm dừng tại đây: không chạy lại
            item["reused_closed_case"] = bool(reused)
            results.append(item)
        else:
            results.append(None)
    todo = [row for row, item in zip(rows, results) if item is None]
    summary = {"closed": sum(item is not None for item in results), "to_run": len(todo),
               "to_run_first": [(r["dataset"], r["opaque_id"], r["source_status"]) for r in todo[:3]],
               "available_ram": psutil.virtual_memory().available, "disk_free": os.statvfs(BASE).f_bavail * os.statvfs(BASE).f_frsize,
               "task_bytes": tree_bytes(BASE)}
    if args.check_only:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    segment = OUT / "segments" / args.segment
    require(not segment.exists(), "đoạn đã tồn tại; dùng mã đoạn mới")
    for old in sorted((OUT / "segments").glob("*/terminal.json")) if (OUT / "segments").is_dir() else []:
        require(read(old)["status"] in ("STOP_CHECKPOINT", "PASS_52_EXACT"), "đoạn trước không dừng sạch: " + str(old))
    prior_wall = sum(read(p)["segment_wall_s"] for p in sorted((OUT / "segments").glob("*/terminal.json"))) if (OUT / "segments").is_dir() else 0.0
    prior_bytes = tree_bytes(OUT) if OUT.exists() else 0
    segment.mkdir(parents=True)
    dump_new(segment / "start.json", {"at_utc": now(), "argv": sys.argv, "pid": os.getpid(), "driver_sha256": sha(__file__),
             "pins": PINS, "authority": "Q-125, Q-108", "prior_wall_s": prior_wall, "prior_bytes": prior_bytes, **summary})
    started = time.perf_counter()
    status, error, ran, peak_rss, min_available = "PASS_52_EXACT", None, 0, 0, summary["available_ram"]
    try:
        for index, row in enumerate(rows):
            if results[index] is not None:
                continue
            if args.max_cases and ran >= args.max_cases:
                status = "STOP_CHECKPOINT"
                break
            dataset, opaque_id = row["dataset"], row["opaque_id"]
            directory = OUT / "cases" / dataset / opaque_id
            directory.parent.mkdir(parents=True, exist_ok=True)
            memory = psutil.virtual_memory()
            require(memory.available >= 2 * MIN_AVAILABLE, "RAM trống trước ca dưới 2 GiB; không khởi worker")
            append(segment / "progress.jsonl", {"at_utc": now(), "event": "CASE_START", "dataset": dataset, "opaque_id": opaque_id})
            command = [str(PYTHON), "-B", "-X", "utf8", str(WRAPPER), "one", dataset, opaque_id, str(directory)]
            logs = segment / "logs"
            logs.mkdir(exist_ok=True)
            case_started, stopped, case_peak = time.perf_counter(), None, 0
            with (logs / (opaque_id + ".stdout.txt")).open("x") as stdout, (logs / (opaque_id + ".stderr.txt")).open("x") as stderr:
                child = subprocess.Popen(command, cwd=BASE, env=os.environ.copy(), stdin=subprocess.DEVNULL,
                                         stdout=stdout, stderr=stderr, start_new_session=True)
                while child.poll() is None:
                    rss = tree_rss(psutil, child.pid)
                    case_peak = max(case_peak, rss)
                    available = psutil.virtual_memory().available
                    min_available = min(min_available, available)
                    if time.perf_counter() - case_started >= MAX_CASE_S:
                        stopped = "ca vượt 600 s (Q-125)"
                    elif rss > MAX_TREE_RSS:
                        stopped = "cây tiến trình vượt 6 GiB RSS (Q-125)"
                    elif available < MIN_AVAILABLE:
                        stopped = "RAM trống dưới 1 GiB (Q-125)"
                    elif prior_wall + time.perf_counter() - started >= MAX_RUN_S:
                        stopped = "lượt vượt 4,5 giờ (Q-125)"
                    if stopped:
                        kill_tree(psutil, child.pid)
                        break
                    time.sleep(POLL_S)
                code = child.wait()
            wall = time.perf_counter() - case_started
            peak_rss = max(peak_rss, case_peak)
            dump_new(logs / (opaque_id + ".process.json"), {"command": command, "exit_code": code, "wall_s": wall,
                     "stopped_by_driver": stopped, "sampled_peak_tree_rss_bytes": case_peak})
            require(stopped is None, stopped or "")
            require(code == 0, "wrapper thoát mã " + str(code) + " ở ca " + opaque_id + "; dừng, không retry")
            item = checked(directory, row)
            case_bytes = tree_bytes(directory)
            cost = read(directory / "cost.json")
            item.update(wall_s=wall, case_bytes=case_bytes, worker_cost=cost, sampled_peak_tree_rss_bytes=case_peak,
                        reused_closed_case=False)
            results[index] = item
            ran += 1
            append(segment / "progress.jsonl", {"at_utc": now(), "event": "CASE_PASS", **item,
                   "segment_wall_s": time.perf_counter() - started})
            require(case_bytes <= MAX_CASE_BYTES, "ca vượt 150 MiB (Q-125)")
            require(prior_bytes + tree_bytes(segment) + sum(r.get("case_bytes", 0) for r in results if r and not r["reused_closed_case"])
                    <= MAX_RUN_BYTES, "lượt vượt 2,5 GiB mới (Q-125)")
    except BaseException as failure:
        status = "FAIL_STOP"
        error = {"type": type(failure).__name__, "message": str(failure), "traceback": traceback.format_exc()}
    table = [item if item is not None else {"dataset": row["dataset"], "opaque_id": row["opaque_id"],
             "source_status": row["source_status"], "result": "not_run"} for row, item in zip(rows, results)]
    if status == "PASS_52_EXACT" and any(r["result"] == "not_run" for r in table):
        status = "STOP_CHECKPOINT"
    dump_new(segment / "52-cases.json", {"schema": "T032-tracerca-ec2-simple-driver-v1", "rows": table})
    dump_new(segment / "terminal.json", {"status": status, "at_utc": now(), "error": error, "new_cases_this_segment": ran,
             "counts": {key: sum(r["result"] == key for r in table) for key in ("exact", "non_OK_exact", "not_run")},
             "segment_wall_s": time.perf_counter() - started, "prior_wall_s": prior_wall,
             "sampled_peak_tree_rss_bytes": peak_rss, "min_available_ram_bytes": min_available,
             "run_bytes_now": tree_bytes(OUT), "retry_performed": False})
    dump_new(segment / "manifest.json", {"files": manifest(segment, ("manifest.json",)), "manifest_excludes": ["manifest.json"]})
    print(json.dumps(read(segment / "terminal.json"), ensure_ascii=False))
    return 0 if status in ("PASS_52_EXACT", "STOP_CHECKPOINT") else 1


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
