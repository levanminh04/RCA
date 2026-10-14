"""T-032 TORAI B (chỉ RE2-TT, ba seed): phát lại lõi và lưu trung gian severity/phân cụm. Chạy trên EC2.

Mỗi đơn vị (ca × seed):
  sham: `p3.runner.chay_luot(..., 'torai_B', ...)` đúng như lượt gốc T-031 trên EC2 (hai tiến trình con: chuẩn bị bảng
        bằng môi trường main, chạy TORAI bằng môi trường py38). Bản ghi phải trùng bản đóng băng từng bit
        (trừ run_id, cost). Lệch thì dừng cả lượt.
  obs:  chạy lại bước 'torai_run' trên đúng các bảng mà sham vừa tạo, qua torai_obs_worker_py38.py (chỉ đọc biến cục bộ).
        `ket_qua` của obs phải trùng `ket_qua` của sham; khác thì dừng.
Dùng lại môi trường, mã và dữ liệu của ~/rca/T-031 ở chế độ chỉ đọc (nơi sinh bản đóng băng TORAI B); chỉ ghi dưới
~/rca/T-032. Không sửa file mã nguồn nào. Không đọc nhãn ở đây.

python torai_core_obs_v1.py <thư mục lượt> [opaque_id[:seed]]      (nối tiếp được: bỏ qua đơn vị đã có unit.json)
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HOME = Path.home()
T031 = HOME / "rca/T-031"
BASE = HOME / "rca/T-032"
CODE_ROOT = T031 / "repo"            # mã và dữ liệu đã sinh bản đóng băng TORAI B
FROZEN_REPO = BASE / "repo"          # bản sao chỉ mục và bản ghi đóng băng
I24 = FROZEN_REPO / "results/T-024/ban-ghi-dua-vao-cham.json"
ENVS = {"main": str(T031 / "envs/main/bin/python"), "drain": str(T031 / "envs/main/bin/python"), "py38": str(T031 / "envs/py38/bin/python")}
PYTHONPATH = {"main": [str(T031 / "src/RCAEval"), str(CODE_ROOT / "src")], "drain": [str(CODE_ROOT / "src")],
              "py38": [str(T031 / "src/RCAEval"), str(CODE_ROOT / "src")]}
OBS_WORKER = BASE / "scripts/torai_obs_worker_py38.py"
EXCLUDED = ("run_id", "cost")
SEEDS = (0, 1, 2)
TIMEOUT_S = 3600


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


def exact_differences(expected, actual, pointer=""):
    differences = []
    if type(expected) is not type(actual):
        return [{"pointer": pointer, "kind": "type", "expected": repr(expected)[:160], "actual": repr(actual)[:160]}]
    if isinstance(expected, dict):
        for key in sorted(set(expected) | set(actual)):
            child = pointer + "/" + str(key)
            if key not in expected or key not in actual:
                differences.append({"pointer": child, "kind": "key_presence"})
            else:
                differences.extend(exact_differences(expected[key], actual[key], child))
    elif isinstance(expected, list):
        if len(expected) != len(actual):
            differences.append({"pointer": pointer, "kind": "length", "expected": len(expected), "actual": len(actual)})
        for index, (left, right) in enumerate(zip(expected, actual)):
            differences.extend(exact_differences(left, right, pointer + "/" + str(index)))
    elif isinstance(expected, float):
        if expected.hex() != actual.hex():
            differences.append({"pointer": pointer, "kind": "float_exact", "expected_hex": expected.hex(), "actual_hex": actual.hex()})
    elif expected != actual:
        differences.append({"pointer": pointer, "kind": "value", "expected": repr(expected)[:160], "actual": repr(actual)[:160]})
    return differences


def precheck():
    index = read(I24)["records"]
    entries = [e for e in index if e["method"] == "torai" and e.get("variant") == "B"]
    config = read(FROZEN_REPO / entries[0]["source_config"])
    pins = dict(config["src_p3"]["tep"])
    bad = {p: {"expected": v, "actual": sha(CODE_ROOT / p)} for p, v in sorted(pins.items()) if sha(CODE_ROOT / p) != v}
    torai_files = sorted(p.relative_to(CODE_ROOT).as_posix() for p in (CODE_ROOT / "src/torai").rglob("*.py"))
    torai_pair = {p: {"code_root": sha(CODE_ROOT / p), "t032_copy": sha(FROZEN_REPO / p) if (FROZEN_REPO / p).is_file() else None} for p in torai_files}
    revision = (T031 / "src/RCAEval.REVISION").read_text(encoding="utf-8").strip() if (T031 / "src/RCAEval.REVISION").is_file() else None
    result = {"at_utc": now(), "frozen_units": len(entries), "source_config": entries[0]["source_config"],
              "source_config_sha256_matches_index": sha(FROZEN_REPO / entries[0]["source_config"]) == entries[0]["source_config_sha256"],
              "src_p3_pinned_files": len(pins), "src_p3_mismatches": bad, "src_torai": torai_pair,
              "src_torai_equal_between_copies": all(v["code_root"] == v["t032_copy"] for v in torai_pair.values()),
              "rcaeval_revision_file": revision, "obs_worker_sha256": sha(OBS_WORKER), "this_script_sha256": sha(__file__),
              "index24_sha256": sha(I24), "envs": ENVS}
    result["pass"] = (len(entries) == 90 and not bad and result["source_config_sha256_matches_index"]
                      and result["src_torai_equal_between_copies"])
    return result, entries


def child_env(kind):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = os.pathsep.join(PYTHONPATH[kind])
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONHASHSEED"] = "0"
    return env


def one_unit(out, allow, entry, runner):
    opaque_id, seed = entry["opaque_id"], entry["seed"]
    unit_dir = out / "units" / (opaque_id + "-s" + str(seed))
    if (unit_dir / "unit.json").is_file():
        return read(unit_dir / "unit.json")
    unit_dir.mkdir(parents=True, exist_ok=True)
    if sha(FROZEN_REPO / entry["path"]) != entry["sha256"]:
        raise RuntimeError("bản đóng băng khác hash chỉ mục: " + entry["path"])
    frozen = read(FROZEN_REPO / entry["path"])
    t = frozen["window"]["t"]
    started = time.perf_counter()
    records = runner.chay_luot(allow, opaque_id, "torai_B", "a", t, unit_dir / "luot", TIMEOUT_S, repo_root=CODE_ROOT, seed=seed,
                               hashseed=0, config_id=frozen["config_id"], torai_tt=T031 / "data/torai-TT")
    sham_wall = time.perf_counter() - started
    if len(records) != 1:
        raise RuntimeError("runner không trả đúng một bản ghi")
    run_dir = unit_dir / "luot" / records[0]["run_id"]
    replay = read(run_dir / "ban-ghi-0.json")
    if set(frozen) != set(replay):
        differences = [{"pointer": "", "kind": "record_keys"}]
    else:
        differences = exact_differences({k: v for k, v in frozen.items() if k not in EXCLUDED},
                                        {k: v for k, v in replay.items() if k not in EXCLUDED})
    unit = {"opaque_id": opaque_id, "seed": seed, "frozen_path": entry["path"], "frozen_sha256": entry["sha256"],
            "frozen_status": frozen["status"], "sham_status": replay["status"], "sham_run_dir": run_dir.relative_to(out).as_posix(),
            "sham_exact_vs_frozen": not differences, "sham_difference_count": len(differences), "sham_first_differences": differences[:5],
            "sham_wall_s": round(sham_wall, 3)}
    if differences:
        dump(unit_dir / "unit.json", unit)
        return unit
    obs_dir = unit_dir / "obs"
    obs_dir.mkdir()
    job = run_dir / "torai" / "job.json"
    started = time.perf_counter()
    with (obs_dir / "stdout.txt").open("w", encoding="utf-8") as so, (obs_dir / "stderr.txt").open("w", encoding="utf-8") as se:
        done = subprocess.run([ENVS["py38"], "-B", "-W", "ignore", str(OBS_WORKER), str(job), str(obs_dir / "ket-qua.json"), str(obs_dir / "locals.json")],
                              cwd=str(CODE_ROOT), env=child_env("py38"), stdin=subprocess.DEVNULL, stdout=so, stderr=se, timeout=TIMEOUT_S)
    unit["obs_wall_s"] = round(time.perf_counter() - started, 3)
    unit["obs_exit_code"] = done.returncode
    if done.returncode == 0:
        native = read(run_dir / "torai" / "ket-qua.json")["ket_qua"]
        observed = read(obs_dir / "ket-qua.json")["ket_qua"]
        diff = exact_differences(native, observed)
        state = read(obs_dir / "locals.json")
        unit.update({"obs_ket_qua_exact_vs_sham": not diff, "obs_difference_count": len(diff), "obs_first_differences": diff[:5],
                     "obs_torai_returns": state.get("torai_returns"), "obs_rcd_returns": len(state.get("rcd_returns") or []),
                     "obs_locals_present": state.get("locals_present"),
                     "table_sha256": {name: sha(run_dir / "bang" / name) for name in sorted(os.listdir(run_dir / "bang"))}})
    dump(unit_dir / "unit.json", unit)
    return unit


def main():
    out = Path(sys.argv[1]).resolve()
    if BASE.resolve() not in out.parents:
        raise SystemExit("thư mục lượt phải nằm trong ~/rca/T-032")
    only = sys.argv[2] if len(sys.argv) > 2 else None
    out.mkdir(parents=True, exist_ok=True)
    check, entries = precheck()
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    dump(out / ("precheck-" + stamp + ".json"), check)
    if not check["pass"]:
        raise SystemExit("precheck không đạt")
    sys.path.insert(0, str(CODE_ROOT / "src"))
    from p3 import runner, selector
    runner.ROOT = CODE_ROOT
    runner.ENVS = dict(ENVS)
    runner.PYTHONPATH = {k: list(v) for k, v in PYTHONPATH.items()}
    runner.TORAI_TT = T031 / "data/torai-TT"
    allow = selector.nap_allowlist(CODE_ROOT / "results/T-022/allowlist-dev.json")
    entries = sorted(entries, key=lambda e: (e["opaque_id"], e["seed"]))
    status, error, done = "COMPLETE", None, 0
    started = time.perf_counter()
    for entry in entries:
        tag = entry["opaque_id"] + ":" + str(entry["seed"])
        if only and only not in (tag, entry["opaque_id"]):
            continue
        try:
            unit = one_unit(out, allow, entry, runner)
        except Exception as error_:  # giữ lượt hỏng, dừng
            status, error = "FAIL_STOP", tag + " " + type(error_).__name__ + ": " + str(error_)[:500]
            break
        event = {"at_utc": now(), "unit": tag, "sham_exact_vs_frozen": unit["sham_exact_vs_frozen"],
                 "obs_ket_qua_exact_vs_sham": unit.get("obs_ket_qua_exact_vs_sham"), "sham_wall_s": unit["sham_wall_s"],
                 "obs_wall_s": unit.get("obs_wall_s")}
        with (out / "progress.jsonl").open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(event, ensure_ascii=False) + "\n")
        print(json.dumps(event, ensure_ascii=False), flush=True)
        if not unit["sham_exact_vs_frozen"] or not unit.get("obs_ket_qua_exact_vs_sham"):
            status, error = "FAIL_STOP", tag + ": lệch bản đóng băng hoặc nhánh quan sát khác native"
            break
        done += 1
    terminal = {"at_utc": now(), "status": status, "error": error, "units_ok_this_driver": done, "driver_wall_s": round(time.perf_counter() - started, 3)}
    dump(out / ("terminal-" + stamp + ".json"), terminal)
    print(json.dumps(terminal, ensure_ascii=False), flush=True)
    return 0 if status == "COMPLETE" else 1


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
