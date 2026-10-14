"""T-032 TORAI B, phép đổi nguồn log (thiet-ke-phep-doi-006.md): nhánh sham, tl2 (bỏ cột log có nền không đổi), tl1 (bỏ mọi cột log).

Chạy trên EC2. Đầu vào: bốn bảng `bang/*.csv` của lượt sham trong runs/torai-core-obs-001 (đã khớp bản đóng băng), seed 0.
Chỉ `logts.csv` bị đổi, bằng cách bỏ cột ở mức chuỗi ký tự (không ghi lại số). Bước TORAI chạy bằng worker native
`python -m p3.worker` của môi trường py38 ở ~/rca/T-031, y như runner. Không sửa file mã nguồn nào. Nhãn nối ở bước collect.

python torai_log_contrast_v1.py run <thư mục lượt> [opaque_id]     (nối tiếp được)
python torai_log_contrast_v1.py collect <thư mục lượt>
"""
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

HOME = Path.home()
T031 = HOME / "rca/T-031"
BASE = HOME / "rca/T-032"
CODE_ROOT = T031 / "repo"
SOURCE = BASE / "runs/torai-core-obs-001"
PY38 = str(T031 / "envs/py38/bin/python")
PYTHONPATH = [str(T031 / "src/RCAEval"), str(CODE_ROOT / "src")]
LABELS = BASE / "repo/results/T-028/runs/phan-hoi-review-001/ca-sai.json"
BRANCHES = ("sham", "tl2", "tl1")
TABLES = ("metric.csv", "logts.csv", "tracets_err.csv", "tracets_lat.csv")


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def dump(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=1, allow_nan=True)
        stream.write("\n")


def exact(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return set(a) == set(b) and all(exact(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(exact(x, y) for x, y in zip(a, b))
    if isinstance(a, float):
        return a.hex() == b.hex()
    return a == b


def write_logts(source, target, branch, t):
    """Bỏ cột ở mức chuỗi. Trả thông tin về số cột bị bỏ."""
    with open(source, newline="", encoding="utf-8") as stream:
        rows = list(csv.reader(stream))
    header, body = rows[0], rows[1:]
    time_index = header.index("time")
    before = [r for r in body if float(r[time_index]) < t]
    keep = [time_index]
    dropped_constant_baseline = 0
    for i, name in enumerate(header):
        if i == time_index:
            continue
        constant = len({float(r[i]) for r in before}) <= 1
        dropped_constant_baseline += constant
        if branch == "tl1":
            continue
        if branch == "tl2" and constant:
            continue
        keep.append(i)
    keep.sort()
    with open(target, "x", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow([header[i] for i in keep])
        for r in body:
            writer.writerow([r[i] for i in keep])
    return {"log_columns_in": len(header) - 1, "log_columns_out": len(keep) - 1, "columns_with_constant_baseline": dropped_constant_baseline,
            "baseline_bins": len(before), "bins": len(body)}


def ranks_from_blocks(result):
    out, offset = {}, 0
    for block in result.get("blocks") or []:
        for group in block["groups"]:
            for entity in group:
                out[entity] = (offset + 1, offset + len(group))
            offset += len(group)
    return out


def run_case(out, unit_dir):
    unit = read(unit_dir / "unit.json")
    opaque_id = unit["opaque_id"]
    case_dir = out / "cases" / opaque_id
    if (case_dir / "case.json").is_file():
        return read(case_dir / "case.json")
    source_run = SOURCE / unit["sham_run_dir"]
    job = read(source_run / "torai/job.json")
    native = read(source_run / "torai/ket-qua.json")["ket_qua"]
    item = {"opaque_id": opaque_id, "seed": job["seed"], "t": job["t"], "source_run": unit["sham_run_dir"], "branches": {}}
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": os.pathsep.join(PYTHONPATH), "PYTHONIOENCODING": "utf-8", "PYTHONHASHSEED": "0"})
    for branch in BRANCHES:
        directory = case_dir / branch
        (directory / "bang").mkdir(parents=True)
        info = {}
        for name in TABLES:
            if name == "logts.csv" and branch != "sham":
                info = write_logts(source_run / "bang" / name, directory / "bang" / name, branch, job["t"])
            else:
                shutil.copyfile(source_run / "bang" / name, directory / "bang" / name)
        new_job = {"kind": "torai_run", "work_dir": str(directory / "bang"), "t": job["t"], "seed": job["seed"]}
        (directory / "job.json").write_text(json.dumps(new_job, ensure_ascii=False, indent=1), encoding="utf-8")
        started = time.perf_counter()
        with (directory / "stdout.txt").open("w") as so, (directory / "stderr.txt").open("w") as se:
            done = subprocess.run([PY38, "-B", "-W", "ignore", "-m", "p3.worker", str(directory / "job.json"), str(directory / "ket-qua.json")],
                                  cwd=str(CODE_ROOT), env=env, stdin=subprocess.DEVNULL, stdout=so, stderr=se, timeout=3600)
        row = {"exit_code": done.returncode, "wall_s": round(time.perf_counter() - started, 3), "logts": info}
        if done.returncode == 0:
            result = read(directory / "ket-qua.json")["ket_qua"]
            row.update({"status": result["status"], "error": result.get("error"), "n_blocks": len(result.get("blocks") or []),
                        "equals_native_ket_qua": exact(native, result)})
        item["branches"][branch] = row
        if branch == "sham" and not row.get("equals_native_ket_qua"):
            item["stop"] = "sham khác lượt gốc"
            break
    dump(case_dir / "case.json", item)
    return item


def run(out, only=None):
    out.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    status, done = "COMPLETE", 0
    started = time.perf_counter()
    for unit_dir in sorted((SOURCE / "units").glob("*-s0")):
        if only and not unit_dir.name.startswith(only):
            continue
        item = run_case(out, unit_dir)
        event = {"at_utc": now(), "opaque_id": item["opaque_id"],
                 "branches": {b: {k: v.get(k) for k in ("exit_code", "status", "equals_native_ket_qua", "wall_s")} for b, v in item["branches"].items()}}
        with (out / "progress.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(event, ensure_ascii=False) + "\n")
        print(json.dumps(event, ensure_ascii=False), flush=True)
        if item.get("stop"):
            status = "FAIL_STOP: " + item["stop"] + " ở " + item["opaque_id"]
            break
        done += 1
    dump(out / ("terminal-" + stamp + ".json"), {"at_utc": now(), "status": status, "cases_done_this_driver": done,
                                                  "driver_wall_s": round(time.perf_counter() - started, 3), "this_script_sha256": sha(__file__)})
    print(status, done, flush=True)
    return 0 if status == "COMPLETE" else 1


def collect(out):
    labels = {r["opaque_id"]: r for r in read(LABELS)["main_rows"] if r["dataset"] == "RE2-TT" and r["method"] == "torai_B"}
    cases = []
    for case_dir in sorted((out / "cases").iterdir()):
        item = read(case_dir / "case.json")
        label = labels[item["opaque_id"]]
        root = label["root"]
        row = {"opaque_id": item["opaque_id"], "root": root, "fault": label["fault"], "cell": label["cell"], "branches": {}}
        for branch, info in item["branches"].items():
            entry = {"status": info.get("status"), "exit_code": info["exit_code"], "logts": info["logts"], "equals_native_ket_qua": info.get("equals_native_ket_qua"),
                     "n_blocks": info.get("n_blocks")}
            if info.get("status") == "OK":
                result = read(case_dir / branch / "ket-qua.json")["ket_qua"]
                rank = ranks_from_blocks(result)
                if root in rank:
                    entry.update({"root_rank_min": rank[root][0], "root_rank_max": rank[root][1],
                                  "above_root": sorted((e for e in rank if rank[e][1] < rank[root][0]), key=lambda e: rank[e][0])[:10]})
            row["branches"][branch] = entry
        sham = row["branches"].get("sham", {})
        row["self_check_sham_rank_equals_t028"] = (label["status"] == "OK" and [sham.get("root_rank_min"), sham.get("root_rank_max")] == [label["rank_min"], label["rank_max"]])
        cases.append(row)

    def effect(a, b):
        return "tăng hạng" if b < a else "giảm hạng" if b > a else "không đổi"

    summary = {"n_cases": len(cases), "sham_equals_native": sum(bool(c["branches"].get("sham", {}).get("equals_native_ket_qua")) for c in cases),
               "self_check_sham_rank_equals_t028": sum(c["self_check_sham_rank_equals_t028"] for c in cases), "seed": 0}
    for branch in ("sham", "tl2", "tl1"):
        ok = [c for c in cases if "root_rank_max" in c["branches"].get(branch, {}) and "root_rank_max" in c["branches"].get("sham", {})]
        block = {"status_counts": dict(Counter(str(c["branches"].get(branch, {}).get("status")) for c in cases)), "n_root_ranked": len(ok),
                 "hit1": sum(c["branches"][branch]["root_rank_max"] == 1 for c in ok), "hit5": sum(c["branches"][branch]["root_rank_max"] <= 5 for c in ok)}
        if branch != "sham":
            block["effect_vs_native"] = dict(Counter(effect(c["branches"]["sham"]["root_rank_min"], c["branches"][branch]["root_rank_min"]) for c in ok))
            wrong = [c for c in ok if c["branches"]["sham"]["root_rank_max"] > 1]
            right = [c for c in ok if c["branches"]["sham"]["root_rank_max"] == 1]
            block["native_wrong"] = {"n": len(wrong), "becomes_hit1": sum(c["branches"][branch]["root_rank_max"] == 1 for c in wrong),
                                     "rows": [{"opaque_id": c["opaque_id"], "cell": c["cell"], "native": [c["branches"]["sham"]["root_rank_min"], c["branches"]["sham"]["root_rank_max"]],
                                               "branch": [c["branches"][branch]["root_rank_min"], c["branches"][branch]["root_rank_max"]],
                                               "above_root_branch": c["branches"][branch]["above_root"]} for c in wrong]}
            block["native_hit1"] = {"n": len(right), "loses_hit1": sum(c["branches"][branch]["root_rank_max"] > 1 for c in right),
                                    "rows_lost": [{"opaque_id": c["opaque_id"], "cell": c["cell"], "branch": [c["branches"][branch]["root_rank_min"], c["branches"][branch]["root_rank_max"]],
                                                   "above_root_branch": c["branches"][branch]["above_root"]} for c in right if c["branches"][branch]["root_rank_max"] > 1]}
            block["log_columns_out_median"] = sorted(c["branches"][branch]["logts"]["log_columns_out"] for c in cases if branch in c["branches"])[len(cases) // 2]
            block["log_columns_in_median"] = sorted(c["branches"][branch]["logts"]["log_columns_in"] for c in cases if branch in c["branches"])[len(cases) // 2]
        summary[branch] = block
    result = {"schema": "T032-TORAI-log-contrast-v1", "design": "results/T-032/thiet-ke-phep-doi-006.md", "this_script_sha256": sha(__file__),
              "labels_sha256": sha(LABELS), "summary": summary, "cases": cases}
    dump(out / "summary.json", result)
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    if len(sys.argv) >= 3 and sys.argv[1] == "run":
        raise SystemExit(run(Path(sys.argv[2]).resolve(), sys.argv[3] if len(sys.argv) > 3 else None))
    if len(sys.argv) == 3 and sys.argv[1] == "collect":
        raise SystemExit(collect(Path(sys.argv[2]).resolve()))
    print(__doc__)
    raise SystemExit(2)
