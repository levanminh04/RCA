"""T-032: chạy trên LAPTOP các nhánh sham / quan sát / phép đổi của CIRCA (K-2, KT-9) và MicroRank (M-D, bộ chia trace bản 009, bản 012).

Bản v8 = v7 + năm nhánh CIRCA của thiet-ke-phep-doi-013.md mục 5 (KT-9; Minh duyệt ngày 11/10/2026, Q-141):
  shamw   hai chỗ móc (CaseData, score_graph) đặt nhưng truyền đúng giá trị native; phải khớp bản đóng băng từng bit
  tf      học trên 291 điểm: CaseData(lookup_window=300) thay cho 120
  t0      chấm 10 điểm ngay sau mốc: current = t + 9
  tfk2, t0k2   như tf, t0 nhưng bỏ mọi cạnh (để tính tỷ số điểm có cạnh / không cạnh)
Chạy: all circa <thư mục> --branches=shamw,tf,tfk2,t0,t0k2. Phần còn lại giống hệt v7. Sinh từ v7 bằng phép thay chuỗi có đếm.

Bản v7 = v6 + năm nhánh MicroRank của thiet-ke-phep-doi-012.md (Minh duyệt chạy trên laptop ngày 11/10/2026):
  shampc   bộ chia native + hàm móc số đếm trả nguyên; phải khớp bản đóng băng từng bit
  c1h      bộ chia native + đếm riêng ở nhóm bất thường (kiểm chỗ móc với M-C1 của phiên 9)
  mo15c1, mo1p50c1   bộ chia theo bài gốc (như mo15, mo1p50) + đếm riêng (KT-3)
  dropnew  bỏ span của thao tác không có ở đoạn nền thay vì ném lỗi (KT-8, nửa MicroRank); ở ca không có thao tác mới phải khớp từng bit
Phần còn lại giống hệt v6. Sinh từ v6 bằng phép thay chuỗi có đếm.

Bản v6 = v5 + tùy chọn vận hành `--datasets=RE2-TT,Nezha-OB` (đặt sau --branches) để chỉ chạy các ca của dataset được nêu. Lý do: ngày 11/10 laptop
chỉ còn 1,2–1,8 GB RAM trống, đủ cho ca Nezha-OB (cần khoảng 1,4 GB) nhưng không đủ cho phần lớn ca RE2-TT (2,0–3,0 GB); lọc theo dataset cho
phép chạy trước phần đủ RAM mà không đổi quy tắc RAM hay phép tính. Phần tính toán giống hệt v5.
Bản v5 = v4 + ba nhánh MicroRank của thiet-ke-phep-doi-009.md (việc 4 gói bổ sung, Q-134, Q-135): shamp (giữ nguyên, phải khớp từng bit),
mo15 và mo1p50 (chia trace theo công thức của bài gốc với span đầu do ta quy ước). Chạy: all microrank <thư mục> --branches=shamp,mo15,mo1p50.
Phần CIRCA và nhánh sham/md của MicroRank không đổi so với v4.

Thiết kế: results/T-032/thiet-ke-phep-doi-003.md (viết trước khi chạy), cùng bản 001 mục 4 và mục 8.
Căn cứ nơi chạy: Q-130, Q-131 mục 2 (Minh cho phát lại CIRCA và chạy M-D trên laptop).

Mỗi nhánh của mỗi ca là một tiến trình con riêng, môi trường như src/p3/runner.py đặt cho worker.
  circa/sham      đường native nguyên vẹn; hai bản ghi phải trùng bản đóng băng từng bit
  circa/obs       như sham + lớp bọc chỉ-đọc quanh circa_kien_truc.scoring.score_graph để giữ trung gian; phải trùng từng bit
  circa/k2        bọc p3.adapters.circa.do_thi để bỏ mọi cạnh (bước duy nhất bị đổi)
  microrank/sham  hàm microrank dựng lại từ mã nguồn native với cột cờ u = duration; phải trùng bản đóng băng từng bit
  microrank/md    cùng hàm, cột cờ u = thời lượng chưa được span con trực tiếp phủ (bước duy nhất bị đổi)
Không sửa file mã nguồn nào. Không dung sai. Chỉ đọc ca dev trong allowlist. Nhãn không được đọc ở đây.

Bản v4 = v3 + ước nhu cầu RAM của tiến trình con bằng RAM đỉnh ĐÃ ĐO của chính ca đó ở lượt runs/circa-laptop-k2-001 (cùng đường chạy),
nhân 1,05, thay cho RAM đỉnh trong bản đóng băng nhân 1,25. Lý do: ở lượt 001 RAM đỉnh đo được bằng 0,998 lần (trung vị) và tối đa 1,011 lần
số trong bản đóng băng, nên hệ số 1,25 thừa khoảng 0,3 GB và làm lượt theo loại cạnh đứng chờ RAM. Phần đệm 6,5% tổng RAM và mốc dừng 95%
giữ nguyên. Không đổi gì ở phần tính toán.
Bản v3 = v2 + hai nhánh CIRCA theo loại cạnh (thiet-ke-phep-doi-005.md): k2x bỏ cạnh giữa hai dịch vụ, k2s bỏ cạnh cùng dịch vụ;
và tùy chọn `all <method> <thư mục> --branches=sham,k2x,k2s` để chỉ chạy một số nhánh (sham luôn chạy trước cho đủ ca).
Bản v2 khác v1 đúng một chỗ: hàm microrank dựng lại được biên dịch với tên file của module src/microrank (xem patch_microrank),
để ca nguồn ERROR cho bản ghi ERROR như đường native. v1 và các lượt đã chạy bằng v1 giữ nguyên.

Dùng:
  python laptop_contrast_v4.py one <circa|microrank> <nhánh> <RE2-TT|Nezha-OB> <opaque_id> <thư mục mới>
  python laptop_contrast_v4.py all <circa|microrank> <thư mục lượt>        (nối tiếp được: bỏ qua nhánh đã có check.json)
  python laptop_contrast_v4.py precheck <circa|microrank>
"""
from __future__ import annotations

import ast
import contextlib
import gzip
import hashlib
import importlib.util
import inspect
import json
import math
import os
import subprocess
import sys
import time
import traceback
from pathlib import Path

REPO = Path("D:/RCA-flashticket")
BASE = REPO / "results/T-032"
PYTHON = Path("D:/RCA-ext/envs/T-014-main/Scripts/python.exe")
PYTHONPATH = ["D:/RCA-ext/src/RCAEval", "D:/RCA-ext/src/baro", str(REPO / "src"), "D:/RCA-ext/work/T-014/CIRCA"]  # thứ tự của runner.PYTHONPATH['main']
THREAD_NAMES = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")
PACKAGES = {"numpy": "1.26.4", "pandas": "2.2.3", "scikit-learn": "1.6.0", "scipy": "1.14.1", "pyarrow": "18.1.0",
            "psutil": "6.1.1", "networkx": "2.8.8"}
METHOD_REPOS = {"D:/RCA-ext/src/RCAEval": "259ea4167160256a74ad30004aa3d96a998c846e",
                "D:/RCA-ext/work/T-014/CIRCA": "0215e1880096aa02a305c697f1c23cac4600ebd2"}
M24 = "results/T-029/runs/compare-rca-preparation-001/manifest.json"
I24 = "results/T-024/ban-ghi-dua-vao-cham.json"
M26 = "results/T-026/runs/session-005/handoff-manifest.json"
I26 = "results/T-026/ban-ghi-dua-vao-cham.json"
ALLOW24 = "results/T-022/allowlist-dev.json"
ALLOW26 = "results/T-026/allowlist-dev.json"
TD_SCRIPT = BASE / "scripts/tracerca_core_and_td_v1.py"
TD_SCRIPT_SHA = None  # điền lúc chạy vào check.json; hàm uncovered được nạp nguyên từ file này
EXCLUDED = ("run_id", "cost")
CIRCA_VARIANTS = ("ols+rht_da", "ols+rht")
BRANCHES = {"circa": ("sham", "obs", "k2", "k2x", "k2s", "shamw", "tf", "tfk2", "t0", "t0k2"), "microrank": ("sham", "md", "shamp", "mo15", "mo1p50", "shampc", "c1h", "mo15c1", "mo1p50c1", "dropnew")}
EXACT_BRANCHES = {"circa": ("sham", "obs", "shamw"), "microrank": ("sham", "shamp", "shampc")}
HUGE = 1e10
MAX_CHILD_S = 600
MAX_RAM_PERCENT = 95.0
RAM_NEED_FACTOR = 1.25
RAM_MARGIN_FRACTION = 0.065
MAX_RAM_WAIT_S = 6 * 3600
MAX_ATTEMPTS = 3
WINDOW_BRANCHES = ("shamw", "tf", "tfk2", "t0", "t0k2")
MD_REPLACEMENTS = (
    ("df=data[COLS].copy()", "df=data[COLS].copy();df['u']=__t032_flag_quantity__(df)"),
    ("before.groupby('operation',sort=True).duration.agg(", "before.groupby('operation',sort=True).u.agg("),
    ("after['abnormal']=after.duration/1000 >=", "after['abnormal']=after.u/1000 >="),
)


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def dump(path, value, allow_nan=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=1, allow_nan=allow_nan)
        stream.write("\n")


def append(path, event):
    with Path(path).open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(event, ensure_ascii=False) + "\n")


def exact_differences(expected, actual, pointer=""):
    """Khác biệt đầy đủ: đúng kiểu, đúng thứ tự, số thực so theo hex; không dung sai."""
    differences = []
    if type(expected) is not type(actual):
        return [{"pointer": pointer, "kind": "type", "expected": repr(expected)[:200], "actual": repr(actual)[:200]}]
    if isinstance(expected, dict):
        for key in sorted(set(expected) | set(actual)):
            child = pointer + "/" + key.replace("~", "~0").replace("/", "~1")
            if key not in expected or key not in actual:
                differences.append({"pointer": child, "kind": "key_presence",
                                    "expected_present": key in expected, "actual_present": key in actual})
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
        differences.append({"pointer": pointer, "kind": "value", "expected": repr(expected)[:200], "actual": repr(actual)[:200]})
    return differences


def compare_records(frozen, replay):
    if set(frozen) != set(replay):
        return [{"pointer": "", "kind": "record_keys", "expected": sorted(frozen), "actual": sorted(replay)}]
    return exact_differences({k: v for k, v in frozen.items() if k not in EXCLUDED},
                             {k: v for k, v in replay.items() if k not in EXCLUDED})


def frozen_entries(method, dataset, opaque_id):
    """Trả [(entry, record)] theo thứ tự bản ghi native; kiểm hash chỉ mục theo manifest và hash bản ghi theo chỉ mục."""
    if dataset == "RE2-TT":
        manifest = read(REPO / M24)
        if sha(REPO / I24) != manifest["source_hashes"][I24]:
            raise RuntimeError("chỉ mục T-024 khác hash trong manifest")
        variants = CIRCA_VARIANTS if method == "circa" else ("full",)
        found = {e["variant"]: e for e in read(REPO / I24)["records"]
                 if e["method"] == method and e["opaque_id"] == opaque_id and e.get("variant") in variants and e["seed"] is None}
        if set(found) != set(variants):
            raise RuntimeError("không đủ bản đóng băng cho " + opaque_id)
        entries = [found[v] for v in variants]
    else:
        if method != "microrank":
            raise RuntimeError("Nezha chỉ dùng cho microrank ở script này")
        manifest = read(REPO / M26)
        if sha(REPO / I26) != manifest["files"][I26]["sha256"]:
            raise RuntimeError("chỉ mục T-026 khác hash trong manifest")
        entries = [e for e in read(REPO / I26)["unique_records"]
                   if e["worker_method"] == "microrank" and e["source_view"] == "main" and e["opaque_id"] == opaque_id]
        if len(entries) != 1:
            raise RuntimeError("không có đúng một bản đóng băng main cho " + opaque_id)
    out = []
    for entry in entries:
        path = REPO / entry["path"]
        if sha(path) != entry["sha256"]:
            raise RuntimeError("bản đóng băng khác hash chỉ mục: " + entry["path"])
        out.append((entry, read(path)))
    return out


def case_list(method):
    cases = []
    index24 = read(REPO / I24)["records"]
    first = "ols+rht_da" if method == "circa" else "full"
    for e in index24:
        if e["method"] == method and e.get("variant") == first and e["seed"] is None:
            cases.append(("RE2-TT", e["opaque_id"], e["path"]))
    if method == "microrank":
        for e in read(REPO / I26)["unique_records"]:
            if e["worker_method"] == "microrank" and e["source_view"] == "main":
                cases.append(("Nezha-OB", e["opaque_id"], e["path"]))
    out = []
    for dataset, opaque_id, path in cases:
        cost = read(REPO / path)["cost"]
        out.append({"dataset": dataset, "opaque_id": opaque_id, "frozen_peak_rss_mb": float(cost.get("peak_rss_mb") or 0.0),
                    "frozen_wall_s": float(cost.get("wall_s") or 0.0)})
    return out


def code_pins(method):
    """File mã nguồn đang nạp phải đúng hash đã đóng băng ở nguồn T-031 (RE2) và T-026 (Nezha, microrank)."""
    pins = dict(read(REPO / "results/T-031/moi-truong.json")["src_p3_sau_sua_1"]["tep"])
    for path, value in read(REPO / I26)["source_hashes"].items():
        if path.startswith("src/microrank/") or path in ("src/p3/nezha.py", "src/p3/nezha_worker.py", "src/p3/adapters/nezha.py"):
            pins[path] = value
        elif path.startswith("src/p3/") and path.endswith(".py") and path in pins and pins[path] != value:
            raise RuntimeError("hai nguồn ghim khác nhau cho " + path)
    bad = {path: {"expected": value, "actual": sha(REPO / path)} for path, value in sorted(pins.items()) if sha(REPO / path) != value}
    return pins, bad


def precheck(method):
    import importlib.metadata
    pins, bad = code_pins(method)
    git = {}
    for repo, commit in METHOD_REPOS.items():
        head = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        dirty = subprocess.run(["git", "-C", repo, "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
        git[repo] = {"head": head, "expected": commit, "dirty": dirty, "pass": head == commit and not dirty}
    tracked = subprocess.run(["git", "-C", str(REPO), "status", "--porcelain", "--", "src/circa_kien_truc", "src/microrank", "src/p3"],
                             capture_output=True, text=True).stdout.splitlines()
    modified = [line for line in tracked if not line.startswith("??")]
    head = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    packages = {name: importlib.metadata.version(name) for name in PACKAGES}
    result = {"at_utc": now(), "method": method, "pinned_files": len(pins), "pin_mismatches": bad, "method_repos": git,
              "repo_head": head, "tracked_src_modified": modified, "untracked_src": [l for l in tracked if l.startswith("??")],
              "packages": packages, "packages_expected": PACKAGES, "python": sys.version,
              "index24_sha256": sha(REPO / I24), "index26_sha256": sha(REPO / I26),
              "td_script_sha256": sha(TD_SCRIPT), "this_script_sha256": sha(__file__)}
    result["pass"] = (not bad and all(v["pass"] for v in git.values()) and not modified and packages == PACKAGES)
    return result


def loaded_sources():
    out = []
    root = (REPO / "src").resolve()
    for name, module in sorted(sys.modules.copy().items()):
        if name.split(".")[0] not in ("p3", "microrank", "circa_kien_truc"):
            continue
        raw = getattr(module, "__file__", None)
        if raw is None:
            continue
        path = Path(raw).resolve()
        if root not in path.parents:
            raise RuntimeError("module nạp từ ngoài repo: " + name + " " + str(path))
        out.append({"module": name, "path": path.relative_to(REPO.resolve()).as_posix(), "sha256": sha(path)})
    return out


def literal_constants(path):
    tree = ast.parse(Path(path).read_text(encoding="utf-8-sig"))
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in ("WHY", "CONFIG"):
                    values[target.id] = ast.literal_eval(node.value)
    if set(values) != {"WHY", "CONFIG"}:
        raise RuntimeError("không đọc được WHY/CONFIG của script nguồn")
    return values


def own_cost(started):
    import psutil
    info = psutil.Process().memory_info()
    peak = getattr(info, "peak_wset", info.rss)
    return {"wall_s": round(time.perf_counter() - started, 6), "peak_rss_mb": round(peak / 2**20, 1), "read_bytes": 0,
            "write_bytes": 0, "exit_code": 0, "timed_out": False, "env": "T-032-laptop-in-process", "hashseed": 0,
            "measurement_note": "wall gồm cả phần quan sát; peak là peak working set của tiến trình; IO không đo"}


def summarize(values):
    import numpy as np
    a = np.asarray(values, dtype=float)
    if a.size == 0:
        return {"n": 0}
    return {"n": int(a.size), "min": float(a.min()), "max": float(a.max()), "mean": float(a.mean()),
            "std": float(a.std()), "n_unique": int(np.unique(a).size)}


def circa_snapshot(value):
    """Rút gọn giá trị trả về của score_graph: tóm tắt cho mọi nút, mảng đầy đủ cho nút có |điểm RHT| > 1e10."""
    import numpy as np
    nodes = {}
    for name, s in value["nodes"].items():
        z = np.asarray(s["z"], dtype=float)
        te = np.asarray(s["official_test_residual"], dtype=float)
        item = {"parents": s["parents"], "regression_route": s["regression_route"], "regression_error": s["regression_error"],
                "regression_fallback": s["regression_fallback"], "rht_score": s["rht_score"], "confidence": s["confidence"],
                "coefficient": s["coefficient"], "intercept": s["intercept"], "residual_mean": s["residual_mean"],
                "residual_var": s["residual_var"], "residual_scale": s["residual_scale"], "x_memory_order": s["x_memory_order"],
                "train_y": summarize(s["train_y"]), "test_y": summarize(s["test_y"]),
                "train_residual": summarize(s["official_train_residual"]), "test_residual": summarize(s["official_test_residual"]),
                "argmax_abs_z": int(np.argmax(np.abs(z))) if z.size else None,
                "max_abs_z": float(np.max(np.abs(z))) if z.size else None,
                "max_abs_test_residual": float(np.max(np.abs(te))) if te.size else None}
        if not math.isfinite(s["rht_score"]) or abs(s["rht_score"]) > HUGE:
            item["full"] = {k: s[k] for k in ("train_x", "test_x", "train_y", "test_y", "official_train_residual",
                                               "official_test_residual", "z")}
        nodes[name] = item
    return {"meta": value["meta"], "graph": value["graph"], "nodes": nodes, "da": value["da"],
            "ranks": value["ranks"], "ranks_da": value["ranks_da"]}


def json_default(value):
    import numpy as np
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (tuple, set, frozenset)):
        return list(value)
    raise TypeError(type(value).__name__)


def load_uncovered():
    spec = importlib.util.spec_from_file_location("t032_tracerca_core_and_td_v1", TD_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    fixtures = module.interval_fixtures()
    if not fixtures["pass"]:
        raise RuntimeError("8 trường hợp khoảng tự dựng không đạt")
    return module.uncovered, fixtures


def patch_microrank(branch, info):
    """Dựng lại hàm microrank từ mã nguồn native với đúng ba chỗ thay; gán vào microrank.microrank."""
    if branch in PARTITION_BRANCHES:
        return patch_microrank_partition(branch, info)
    if branch == "dropnew":
        return patch_microrank_dropnew(branch, info)
    import microrank as module
    import pandas as pd
    source = inspect.getsource(module.microrank)
    info["native_function_source_sha256"] = hashlib.sha256(source.encode("utf-8")).hexdigest()
    for old, new in MD_REPLACEMENTS:
        if source.count(old) != 1:
            raise RuntimeError("chuỗi cần thay không xuất hiện đúng một lần: " + old)
        source = source.replace(old, new)
    if source.count("def microrank(") != 1:
        raise RuntimeError("không thấy dòng def microrank")
    source = source.replace("def microrank(", "def __t032_microrank__(")
    info["replacements"] = [list(pair) for pair in MD_REPLACEMENTS]
    info["transformed_function_source_sha256"] = hashlib.sha256(source.encode("utf-8")).hexdigest()
    info["transformed_function_source"] = source
    info["calls"] = []
    if branch == "sham":
        def quantity(df):
            info["calls"].append({"rows": int(len(df)), "quantity": "duration (bản sao nguyên cột)"})
            return df["duration"].copy()
    else:
        uncovered, fixtures = load_uncovered()
        info["interval_fixtures"] = fixtures

        def quantity(df):
            call = {"rows": int(len(df)), "quantity": "uncovered"}
            info["calls"].append(call)
            try:
                u, covered, children, resolved = uncovered(df)
            except Exception as error:  # dữ liệu không hợp lệ: để mã native tự báo lỗi của nó ở các dòng kiểm phía sau
                call["uncovered_error"] = type(error).__name__ + ": " + str(error)[:300]
                return df["duration"].copy()
            duration = df["duration"].to_numpy(dtype="int64")
            call.update({"negative_u": int((u < 0).sum()), "u_gt_duration": int((u > duration).sum()),
                         "spans_with_children": int((children > 0).sum()), "parent_resolved": int(resolved.sum()),
                         "total_duration_us": int(duration.sum()), "total_covered_us": int(covered.sum()),
                         "u_equals_duration": int((u == duration).sum()), "duration_dtype": str(df["duration"].dtype)})
            if call["negative_u"] or call["u_gt_duration"]:
                raise RuntimeError("u ngoài [0, duration]")
            return pd.Series(u, index=df.index).astype(df["duration"].dtype)
    namespace = module.__dict__
    namespace["__t032_flag_quantity__"] = quantity
    # v2: biên dịch với tên file của chính module phương pháp. Adapter (src/p3/adapters/__init__.py, hàm loi) chỉ coi một
    # ngoại lệ là ERROR của phương pháp khi traceback đi qua file trong src/microrank; với tên file giả như ở v1, ca nguồn
    # ERROR bị ném LoiRunner thay vì thành bản ghi ERROR như native.
    exec(compile(source, module.__file__, "exec"), namespace)  # noqa: S102 — mã nguồn native đã thay ba chuỗi
    info["original_function_id_replaced"] = True
    module.microrank = namespace["__t032_microrank__"]


PARTITION_BRANCHES = ("shamp", "mo15", "mo1p50", "shampc", "c1h", "mo15c1", "mo1p50c1")
C1_BRANCHES = ("shampc", "c1h", "mo15c1", "mo1p50c1")
PARTITION_OF = {"shampc": "shamp", "c1h": "shamp", "mo15c1": "mo15", "mo1p50c1": "mo1p50"}
C1_REPLACEMENTS = (("'tracecounts':nums}}", "'tracecounts':__t032_counts__(after,traces,nums,is_anomaly)}}"),)
DROPNEW_REPLACEMENTS = (("if newops:raise ValueError('No normal baseline for: '+','.join(sorted(newops)))", "after=__t032_dropnew__(after,newops)"),)
PARTITION_REPLACEMENTS = (
    ("normal=all_traces-abnormal",
     "all_traces,abnormal=__t032_partition__(df,after,incident_time_us,all_traces,abnormal);normal=all_traces-abnormal"),
)
PARTITION_RULES = {"mo15": "bài và hàm báo động của code: thời gian cả yêu cầu > tổng (mức nền + 1,5 độ lệch chuẩn)",
                   "mo1p50": "hàm chia nhóm của code: thời gian cả yêu cầu > tổng (mức nền + 1 độ lệch chuẩn) + 50 ms"}
ONE_SECOND_US = 1_000_000


def patch_microrank_partition(branch, info):
    """Bản 009: móc đúng một chỗ, ngay trước dòng `normal=all_traces-abnormal`, để thay hai tập trace.

    shamp trả nguyên hai tập native. mo15, mo1p50 chia theo công thức của bài gốc với span đầu do ta quy ước
    (trường cha trống hoặc ghi 'root'); mức nền học như preprocess_data.get_operation_slo của code gốc; hai luật gọi
    nguyên hàm của src/microrank/detectors.py.
    """
    import microrank as module
    import numpy as np
    import pandas as pd
    from microrank import detectors
    c1_branch = branch
    branch = PARTITION_OF.get(branch, branch)   # bản 012: phần chia trace của nhánh ghép giống hệt nhánh gốc tương ứng
    replacements = PARTITION_REPLACEMENTS + (C1_REPLACEMENTS if c1_branch in C1_BRANCHES else ())
    info["partition_rule_branch"] = branch
    info["count_calls"] = []
    source = inspect.getsource(module.microrank)
    info["native_function_source_sha256"] = hashlib.sha256(source.encode("utf-8")).hexdigest()
    for old, new in replacements:
        if source.count(old) != 1:
            raise RuntimeError("chuỗi cần thay không xuất hiện đúng một lần: " + old)
        source = source.replace(old, new)
    if source.count("def microrank(") != 1:
        raise RuntimeError("không thấy dòng def microrank")
    source = source.replace("def microrank(", "def __t032_microrank__(")
    info["replacements"] = [list(pair) for pair in replacements]
    info["transformed_function_source_sha256"] = hashlib.sha256(source.encode("utf-8")).hexdigest()
    info["transformed_function_source"] = source
    info["detectors_sha256"] = sha(detectors.__file__)
    info["calls"] = []

    def hook(df, after, t_us, all_traces, abnormal):
        call = {"rows": int(len(df)), "native_traces": len(all_traces), "native_abnormal": len(abnormal), "rule": PARTITION_RULES.get(branch, "giữ nguyên")}
        info["calls"].append(call)
        if branch == "shamp":
            return all_traces, abnormal
        tid = df.traceID.astype(str).to_numpy()
        par = df.parentSpanID
        declared = (par.isna() | par.astype("string").fillna("").isin(["", "root"])).to_numpy(dtype=bool)
        ident = (df.traceID.astype(str) + "|" + df.spanID.astype(str)).to_numpy()
        position = pd.Series(np.arange(len(df)), index=ident)
        position = position[~position.index.duplicated(keep=False)]
        parent = (df.traceID.astype(str) + "|" + par.astype(str)).map(position).to_numpy(dtype="float64")
        has_parent = ~np.isnan(parent) & ~declared
        p = np.where(has_parent, parent, 0).astype("int64")
        orphan = ~declared & ~has_parent
        duration = df.duration.to_numpy(dtype="int64")
        after_span = (df.startTime.to_numpy(dtype="int64") + duration) >= t_us
        child_sum = np.zeros(len(df), dtype="int64")
        np.add.at(child_sum, p[has_parent], duration[has_parent])
        handling = duration - child_sum
        tcode, tuniq = pd.factorize(tid)
        frame = pd.DataFrame({"t": tcode, "after": after_span, "declared": declared, "orphan": orphan, "dur": duration, "handling": handling})
        g = frame.groupby("t", sort=True).agg(n=("after", "size"), n_after=("after", "sum"), roots=("declared", "sum"), orphans=("orphan", "sum"))
        roots = frame[frame["declared"]].groupby("t", sort=True).agg(root_dur=("dur", "sum"), root_handling_max=("handling", "max"))
        g = g.join(roots)
        if not np.array_equal(g.index.to_numpy(), np.arange(len(tuniq))):
            raise RuntimeError("chỉ số trace không liên tục")
        is_after = (g["n_after"] > 0).to_numpy()
        has_root = (g["roots"] >= 1).to_numpy()
        base_ok = (~is_after) & has_root & (g["orphans"] == 0).to_numpy() & ~(g["root_handling_max"] > ONE_SECOND_US).to_numpy()
        op = df.operation.to_numpy()
        mask = base_ok[tcode]
        slo = {}
        for name, values in pd.Series(handling[mask]).groupby(op[mask], sort=True):
            x = values.to_numpy(dtype="float64")
            slo[name] = [round(float(np.mean(x)) / 1000.0, 4), round(float(np.std(x)) / 1000.0, 4)]   # như code gốc: ms, làm tròn 4, std tổng thể
        keep = is_after & has_root
        if set(tuniq[is_after]) != set(all_traces):
            raise RuntimeError("tập trace sau mốc tính lại khác tập của hàm native")
        sel = keep[tcode]
        counts = pd.DataFrame({"t": tcode[sel], "o": op[sel]}).groupby(["t", "o"], sort=True).size()
        root_dur = g["root_dur"].to_numpy()
        operation_counts = {}
        for (t, o), c in counts.items():
            operation_counts.setdefault(tuniq[t], {"duration": float(root_dur[t])})[o] = int(c)
        needed = {o for d in operation_counts.values() for o in d if o != "duration"}
        call.update({"traces_after": int(is_after.sum()), "traces_after_with_root": int(keep.sum()), "traces_after_dropped_no_root": int((is_after & ~has_root).sum()),
                     "traces_after_multi_root": int((is_after & (g["roots"] >= 2).to_numpy()).sum()), "traces_after_with_orphan": int((keep & (g["orphans"] > 0).to_numpy()).sum()),
                     "traces_after_straddling_t": int((keep & (g["n_after"] < g["n"]).to_numpy()).sum()),
                     "baseline_traces": int((~is_after).sum()), "baseline_traces_used": int(base_ok.sum()), "slo_operations": len(slo),
                     "operations_needed": len(needed), "operations_needed_without_slo": sorted(needed - set(slo))[:20]})
        if branch == "mo15":
            new_abnormal = set(detectors.original_system_alarm(operation_counts, slo)["abnormal_trace_ids"])
        else:
            new_abnormal = set(detectors.original_trace_partition(operation_counts, slo)[0])
        new_all = set(operation_counts)
        svc = df.serviceName.astype(str).to_numpy()

        def by_service(trace_set):
            code_in = np.isin(tuniq, list(trace_set)) if trace_set else np.zeros(len(tuniq), dtype=bool)
            m = code_in[tcode] & after_span
            if not m.any():
                return {}
            return {k: int(v) for k, v in pd.DataFrame({"t": tcode[m], "s": svc[m]}).drop_duplicates().groupby("s").size().items()}

        call.update({"new_traces": len(new_all), "new_abnormal": len(new_abnormal), "new_normal": len(new_all - new_abnormal),
                     "native_abnormal_share": len(abnormal) / len(all_traces) if all_traces else None,
                     "new_abnormal_share": len(new_abnormal) / len(new_all) if new_all else None,
                     "new_abnormal_also_native_abnormal": len(new_abnormal & abnormal),
                     "native_abnormal_traces_by_service": by_service(abnormal), "new_abnormal_traces_by_service": by_service(new_abnormal)})
        return new_all, new_abnormal

    def counts(after, traces, nums, is_anomaly):
        """Bản 012: số đếm của nhóm bất thường = số trace của nhóm mà chính thao tác có span mang cờ (M-C1). Nhóm bình thường giữ nguyên."""
        call = {"is_anomaly": bool(is_anomaly), "operations": len(nums), "mode": "giữ nguyên"}
        info["count_calls"].append(call)
        if c1_branch == "shampc" or not is_anomaly:
            return nums
        part = after[after.abnormal & after.traceID.astype(str).isin(traces)]
        own = part.groupby("operation").traceID.nunique().to_dict()
        new = {op: int(own.get(op, 0)) for op in nums}
        call.update({"mode": "đếm riêng", "group_traces": len(traces), "sum_native": int(sum(nums.values())), "sum_own": int(sum(new.values())),
                     "operations_own_zero": sum(1 for v in new.values() if v == 0), "own_gt_native": sum(1 for op in nums if new[op] > nums[op]),
                     "group_traces_with_flagged_span": int(part.traceID.nunique())})
        return new

    namespace = module.__dict__
    namespace["__t032_partition__"] = hook
    namespace["__t032_counts__"] = counts
    exec(compile(source, module.__file__, "exec"), namespace)  # noqa: S102 — mã nguồn native đã thay đúng một chuỗi
    info["original_function_id_replaced"] = True
    module.microrank = namespace["__t032_microrank__"]


def patch_microrank_dropnew(branch, info):
    """Bản 012 mục 2 (KT-8): thay đúng dòng ném lỗi 'No normal baseline' bằng việc bỏ span của thao tác không có ở đoạn nền."""
    import microrank as module
    source = inspect.getsource(module.microrank)
    info["native_function_source_sha256"] = hashlib.sha256(source.encode("utf-8")).hexdigest()
    for old, new in DROPNEW_REPLACEMENTS:
        if source.count(old) != 1:
            raise RuntimeError("chuỗi cần thay không xuất hiện đúng một lần: " + old)
        source = source.replace(old, new)
    if source.count("def microrank(") != 1:
        raise RuntimeError("không thấy dòng def microrank")
    source = source.replace("def microrank(", "def __t032_microrank__(")
    info["replacements"] = [list(pair) for pair in DROPNEW_REPLACEMENTS]
    info["transformed_function_source_sha256"] = hashlib.sha256(source.encode("utf-8")).hexdigest()
    info["transformed_function_source"] = source
    info["calls"] = []

    def dropnew(after, newops):
        call = {"rows": int(len(after)), "traces_after": int(after.traceID.nunique()), "new_operations": sorted(newops), "spans_dropped": 0}
        info["calls"].append(call)
        if not newops:
            return after
        m = after.operation.isin(newops)
        out = after[~m].copy()
        call.update({"spans_dropped": int(m.sum()), "traces_touched": int(after.loc[m, "traceID"].nunique()),
                     "traces_left": int(out.traceID.nunique()), "rows_left": int(len(out))})
        return out

    namespace = module.__dict__
    namespace["__t032_dropnew__"] = dropnew
    exec(compile(source, module.__file__, "exec"), namespace)  # noqa: S102 — mã nguồn native đã thay đúng một chuỗi
    info["original_function_id_replaced"] = True
    module.microrank = namespace["__t032_microrank__"]


def one(method, branch, dataset, opaque_id, directory):
    if os.environ.get("PYTHONHASHSEED") != "0" or os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
        raise RuntimeError("môi trường tiến trình con sai")
    if any(os.environ.get(name) is not None for name in THREAD_NAMES):
        raise RuntimeError("biến số luồng phải để trống")
    if sys.gettrace() is not None or sys.getprofile() is not None:
        raise RuntimeError("có trace/profile hook sẵn")
    if branch not in BRANCHES[method]:
        raise RuntimeError("nhánh lạ")
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=False)
    pair = frozen_entries(method, dataset, opaque_id)
    frozen = [record for _entry, record in pair]
    from p3 import ban_ghi, runner, selector, worker
    constants = None
    if dataset == "RE2-TT":
        allow = selector.nap_allowlist(REPO / ALLOW24)
        wanted = {name: meta["sha256"] for name, meta in allow[opaque_id]["files"].items() if meta is not None}
        if wanted != frozen[0]["input_sha256"]:
            raise RuntimeError("hash đầu vào theo allowlist khác bản đóng băng")
        files = selector.chon_ca(allow, opaque_id, REPO, kiem_hash=True)
        job = {"kind": "ranker", "method": method, "t": frozen[0]["window"]["t"], "model": "ols" if method == "circa" else None,
               "files": {name: {"path": value, "sha256": wanted[name]} for name, value in files.items()}}
        invoke = worker.main
    else:
        from p3 import nezha, nezha_worker
        from p3.adapters.nezha import VARIANTS, VERSIONS
        index26 = read(REPO / I26)
        allow_path = REPO / ALLOW26
        if sha(allow_path) != index26["source_hashes"][ALLOW26]:
            raise RuntimeError("allowlist Nezha khác hash nguồn T-026")
        allow = nezha.nap_allowlist(allow_path)
        entry = pair[0][0]
        if opaque_id not in allow or entry["trace_guard_s"] != 0:
            raise RuntimeError("ca Nezha ngoài phạm vi main")
        wanted = {path: meta["sha256"] for path, meta in allow[opaque_id]["files"].items()}
        if wanted != frozen[0]["input_sha256"]:
            raise RuntimeError("hash đầu vào Nezha khác bản đóng băng")
        job = {"allowlist_path": str(allow_path), "opaque_id": opaque_id, "repo_root": str(REPO), "view": "main",
               "method": "microrank", "trace_guard_s": 0}
        script = "results/T-026/scripts/run_pilot.py" if entry["reused_pilot"] else "results/T-026/scripts/run.py"
        if sha(REPO / script) != index26["source_hashes"][script]:
            raise RuntimeError("script nguồn T-026 khác hash")
        constants = literal_constants(REPO / script)
        invoke = nezha_worker.main
    (directory / "job.json").write_text(json.dumps(job, ensure_ascii=False, indent=1), encoding="utf-8")
    info = {"method": method, "branch": branch}
    holder = {}
    if method == "circa" and branch == "obs":
        import circa_kien_truc.scoring as scoring
        original_score = scoring.score_graph

        def observed(*args, **kwargs):
            value = original_score(*args, **kwargs)
            holder.setdefault("values", []).append(value)
            return value

        scoring.score_graph = observed
    if method == "circa" and branch in WINDOW_BRANCHES:
        # thiet-ke-phep-doi-013.md mục 5: hai chỗ móc; shamw truyền đúng giá trị native
        import RCAEval.classes.data as rdata
        import circa_kien_truc.scoring as scoring
        native_case = rdata.CaseData
        native_score = scoring.score_graph
        lookup = 300 if branch in ("tf", "tfk2") else 120
        info.update({"lookup_window": lookup, "current_rule": "t + 9" if branch in ("t0", "t0k2") else "native", "case_calls": [], "score_calls": []})

        def case_factory(*args, **kwargs):
            if "lookup_window" in kwargs or len(args) > 4:
                raise RuntimeError("CaseData được gọi với lookup_window; chỗ móc không còn đúng")
            case = native_case(*args, lookup_window=lookup, **kwargs)
            info["case_calls"].append({"train_window": case.train_window, "test_window": case.test_window, "lookup_window_points": lookup})
            return case

        def windowed_score(frame, graph, detect_time, current=None, *args, **kwargs):
            used = detect_time + 9 if branch in ("t0", "t0k2") else current
            info["score_calls"].append({"detect_time": int(detect_time), "current_native": None if current is None else int(current),
                                        "current_used": None if used is None else int(used), "frame_time_min": int(frame["time"].min()),
                                        "frame_time_max": int(frame["time"].max()), "frame_rows": int(len(frame))})
            return native_score(frame, graph, detect_time, used, *args, **kwargs)

        rdata.CaseData = case_factory      # score_graph nạp tên này lúc được gọi
        scoring.score_graph = windowed_score
    if method == "circa" and branch in ("k2", "k2x", "k2s", "tfk2", "t0k2"):
        import p3.adapters.circa as adapter
        original_graph = adapter.do_thi

        def without_edges(columns, spans, t, circa_src=adapter.CIRCA_SRC):
            from circa_kien_truc.builder import metric_mapping
            graph, report = original_graph(columns, spans, t, circa_src)
            graph = graph.copy()
            service = {row["column"]: row["service"] for row in metric_mapping(graph.nodes)}
            edges = list(graph.edges)
            cross = [e for e in edges if service[e[0]] != service[e[1]]]
            same = [e for e in edges if service[e[0]] == service[e[1]]]
            # k2: bỏ mọi cạnh; k2x: bỏ cạnh giữa hai dịch vụ; k2s: bỏ cạnh cùng dịch vụ (thiet-ke-phep-doi-005.md)
            drop = edges if branch in ("k2", "tfk2", "t0k2") else cross if branch == "k2x" else same
            info.update({"nodes": graph.number_of_nodes(), "edges_total": len(edges), "edges_cross_service": len(cross),
                         "edges_same_service": len(same), "edges_removed": len(drop)})
            graph.remove_edges_from(drop)
            info["edges_left"] = graph.number_of_edges()
            return graph, report

        adapter.do_thi = without_edges  # bước duy nhất bị đổi
    if method == "microrank":
        patch_microrank(branch, info)
    started = time.perf_counter()
    with (directory / "worker-stdout.txt").open("x", encoding="utf-8") as stdout, \
            (directory / "worker-stderr.txt").open("x", encoding="utf-8") as stderr:
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            invoke(str(directory / "job.json"), str(directory / "ket-qua.json"))
    cost = own_cost(started)
    output = read(directory / "ket-qua.json")
    if output.get("hashseed") != "0":
        raise RuntimeError("worker báo hashseed khác 0")
    if dataset == "RE2-TT":
        base = {"run_id": directory.name, "opaque_id": opaque_id, "mode": "a", "seed": None, "hashseed": 0,
                "detector": None, "detector_columns": None, "config_id": frozen[0]["config_id"]}
        records = runner._ket_thuc(directory, directory / "ket-qua.json", [cost], base, method, "a",
                                   model="ols" if method == "circa" else None)
    else:
        results = output["ket_qua_nhieu"]
        if len(results) != 1:
            raise RuntimeError("worker Nezha không trả đúng một kết quả")
        record = ban_ghi.tao("microrank", VERSIONS["microrank"], VARIANTS["microrank"], "a", results[0], output["window"],
                             constants["CONFIG"], constants["WHY"], seed=None, hashseed=0, run_id=directory.name, opaque_id=opaque_id)
        record["cost"] = {**cost, "buoc_s": output.get("buoc_s", {})}
        record["input_sha256"] = output["input_sha256"]
        if pair[0][0]["reused_pilot"]:
            record["extra"].update(pilot_view="main", pilot_only=True, source_provenance_file="ket-qua.json")
        else:
            record["extra"].update(source_view="main", pilot_only=False, source_provenance_file="ket-qua.json")
        ban_ghi.kiem(record)
        (directory / "ban-ghi-0.json").write_text(json.dumps(record, ensure_ascii=False, indent=1), encoding="utf-8")
        records = [record]
    if len(records) != len(frozen):
        raise RuntimeError("số bản ghi dựng lại khác số bản đóng băng")
    replay = [read(directory / ("ban-ghi-" + str(i) + ".json")) for i in range(len(frozen))]
    if [r["variant"] for r in replay] != [r["variant"] for r in frozen]:
        raise RuntimeError("thứ tự biến thể khác bản đóng băng")
    differences = [compare_records(frozen[i], replay[i]) for i in range(len(frozen))]
    if method == "circa" and branch == "obs":
        values = holder.get("values", [])
        info["score_graph_calls"] = len(values)
        if len(values) == 1:
            with gzip.open(directory / "score-graph.json.gz", "xt", encoding="utf-8", newline="\n") as stream:
                json.dump(circa_snapshot(values[0]), stream, ensure_ascii=False, allow_nan=True, default=json_default)
    if method == "microrank":
        source_text = info.pop("transformed_function_source")
        (directory / "transformed-function.py.txt").write_text(source_text, encoding="utf-8")
    exact = not any(differences)
    dump(directory / "check.json", {
        "schema": "T032-laptop-contrast-v8", "at_utc": now(), "method": method, "branch": branch, "dataset": dataset,
        "opaque_id": opaque_id, "frozen_paths": [entry["path"] for entry, _r in pair],
        "frozen_sha256": [entry["sha256"] for entry, _r in pair], "frozen_statuses": [r["status"] for r in frozen],
        "branch_statuses": [r["status"] for r in replay], "variants": [r["variant"] for r in frozen],
        "difference_count_vs_frozen": [len(d) for d in differences], "first_differences": [d[:5] for d in differences],
        "exact_vs_frozen": exact, "must_be_exact": branch in EXACT_BRANCHES[method], "excluded_fields": list(EXCLUDED),
        "info": info, "loaded_sources": loaded_sources(), "cost": cost, "td_script_sha256": sha(TD_SCRIPT),
        "this_script_sha256": sha(__file__),
        "thread_environment": {name: os.environ.get(name) for name in THREAD_NAMES}}, allow_nan=True)
    return 0


def child_environment(out):
    env = os.environ.copy()
    for name in THREAD_NAMES:
        env.pop(name, None)
    env["PYTHONHASHSEED"] = "0"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONPATH"] = os.pathsep.join(PYTHONPATH)
    temp = Path(out) / "tmp"
    temp.mkdir(parents=True, exist_ok=True)
    env["TMP"] = env["TEMP"] = str(temp)
    return env


class Stop(Exception):
    pass


def run_child(out, state, method, branch, case):
    """Chờ RAM, chạy một tiến trình con, canh 95% và 600 s. Trả đường dẫn thư mục có check.json."""
    import psutil
    dataset, opaque_id = case["dataset"], case["opaque_id"]
    root = Path(out) / "cases" / dataset / opaque_id
    for attempt in range(1, MAX_ATTEMPTS + 1):
        directory = root / (branch if attempt == 1 else branch + "-lan" + str(attempt))
        if (directory / "check.json").is_file():
            return directory
        if directory.exists():
            continue  # lần trước không cho check.json (bị giết hoặc lỗi); giữ nguyên, dùng tên lần kế
        total = psutil.virtual_memory().total
        need = case.get("need_mb", RAM_NEED_FACTOR * case["frozen_peak_rss_mb"]) * 2**20 + RAM_MARGIN_FRACTION * total
        waited = False
        while True:
            vm = psutil.virtual_memory()
            if vm.available >= need and vm.percent < MAX_RAM_PERCENT:
                break
            if state["ram_wait_s"] >= MAX_RAM_WAIT_S:
                raise Stop("hết thời gian chờ RAM")
            if not waited or int(state["ram_wait_s"]) % 300 < 30:
                append(Path(out) / "progress.jsonl", {"at_utc": now(), "event": "WAIT_RAM", "opaque_id": opaque_id, "branch": branch,
                                                      "available_gb": round(vm.available / 2**30, 2), "need_gb": round(need / 2**30, 2),
                                                      "percent": vm.percent})
            waited = True
            time.sleep(30)
            state["ram_wait_s"] += 30
        command = [str(PYTHON), "-B", "-W", "ignore", str(Path(__file__).resolve()), "one", method, branch, dataset, opaque_id, str(directory)]
        logs = Path(out) / "logs"
        logs.mkdir(parents=True, exist_ok=True)
        tag = "-".join((dataset, opaque_id, directory.name))
        started = time.perf_counter()
        with (logs / (tag + ".out")).open("w", encoding="utf-8") as so, (logs / (tag + ".err")).open("w", encoding="utf-8") as se:
            child = subprocess.Popen(command, cwd=str(REPO), env=child_environment(out), stdin=subprocess.DEVNULL, stdout=so, stderr=se)
            peak_percent, killed = 0.0, None
            while child.poll() is None:
                percent = psutil.virtual_memory().percent
                peak_percent = max(peak_percent, percent)
                if percent >= MAX_RAM_PERCENT:
                    killed = "RAM_95"
                elif time.perf_counter() - started > MAX_CHILD_S:
                    killed = "TIMEOUT_600S"
                if killed:
                    child.kill()
                    child.wait()
                    break
                time.sleep(1)
        wall = time.perf_counter() - started
        state["compute_wall_s"] += wall
        state["peak_system_ram_percent"] = max(state["peak_system_ram_percent"], peak_percent)
        event = {"at_utc": now(), "event": "CHILD", "dataset": dataset, "opaque_id": opaque_id, "branch": branch, "attempt": attempt,
                 "directory": directory.relative_to(BASE).as_posix(), "exit_code": child.returncode, "killed": killed,
                 "wall_s": round(wall, 3), "peak_system_ram_percent": peak_percent}
        if killed == "RAM_95":
            state["ram_kills"] += 1
            append(Path(out) / "progress.jsonl", event)
            time.sleep(30)
            continue
        if killed or child.returncode != 0 or not (directory / "check.json").is_file():
            event["stderr_tail"] = (logs / (tag + ".err")).read_text(encoding="utf-8", errors="replace")[-3000:]
            append(Path(out) / "progress.jsonl", event)
            raise Stop("tiến trình con lỗi: " + tag)
        check = read(directory / "check.json")
        event.update({"exact_vs_frozen": check["exact_vs_frozen"], "branch_statuses": check["branch_statuses"],
                      "difference_count_vs_frozen": check["difference_count_vs_frozen"]})
        append(Path(out) / "progress.jsonl", event)
        print(dataset, opaque_id, branch, "exact" if check["exact_vs_frozen"] else "khác", round(wall, 1), flush=True)
        if check["must_be_exact"] and not check["exact_vs_frozen"]:
            raise Stop("nhánh phải khớp nhưng lệch bản đóng băng: " + tag)
        return directory
    raise Stop("cùng một tiến trình con bị giết vì RAM 3 lần: " + dataset + "/" + opaque_id + "/" + branch)


def run_all(method, out, only_branches=None, only_datasets=None):
    out = Path(out).resolve()
    if BASE.resolve() not in out.parents:
        raise SystemExit("thư mục lượt phải nằm trong results/T-032")
    out.mkdir(parents=True, exist_ok=True)
    check = precheck(method)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    dump(out / ("precheck-" + stamp + ".json"), check)
    if not check["pass"]:
        raise SystemExit("precheck không đạt; xem " + str(out / ("precheck-" + stamp + ".json")))
    cases = case_list(method)
    if only_datasets:
        cases = [c for c in cases if c["dataset"] in only_datasets]
    if method == "circa":
        cases.sort(key=lambda c: (c["opaque_id"] != "dev-a5cabe5fa7", c["frozen_peak_rss_mb"], c["opaque_id"]))
        stages = [("sham",), ("obs", "k2")]
    else:
        cases.sort(key=lambda c: (c["dataset"] != "Nezha-OB", c["frozen_peak_rss_mb"], c["opaque_id"]))
        stages = [("sham", "md")]
    if only_branches:
        if any(b not in BRANCHES[method] for b in only_branches) or only_branches[0] not in ("sham", "shamp", "shampc", "shamw"):
            raise SystemExit("danh sách nhánh phải bắt đầu bằng sham và thuộc " + str(BRANCHES[method]))
        stages = [(only_branches[0],), tuple(only_branches[1:])]
    if not (out / "plan.json").exists() and not only_datasets:
        dump(out / "plan.json", {"method": method, "stages": [list(s) for s in stages], "cases": cases,
                                 "order_rule": "ca thử đầu (CIRCA) hoặc Nezha trước (MicroRank), rồi tăng dần theo RAM đỉnh trong bản đóng băng; không dùng nhãn"})
    measured = {}
    if method == "circa":
        for check in (BASE / "runs/circa-laptop-k2-001/cases/RE2-TT").glob("*/*/check.json"):
            record = read(check)
            measured[record["opaque_id"]] = max(measured.get(record["opaque_id"], 0.0), float(record["cost"]["peak_rss_mb"]))
    for case in cases:
        peak = measured.get(case["opaque_id"])
        case["need_mb"] = 1.05 * peak if peak else RAM_NEED_FACTOR * case["frozen_peak_rss_mb"]
        case["need_basis"] = "RAM đỉnh đo ở lượt 001 x 1,05" if peak else "RAM đỉnh bản đóng băng x 1,25"
    state = {"ram_wait_s": 0.0, "compute_wall_s": 0.0, "peak_system_ram_percent": 0.0, "ram_kills": 0}
    append(out / "progress.jsonl", {"at_utc": now(), "event": "DRIVER_START", "pid": os.getpid(), "method": method, "n_cases": len(cases),
                                     "script": Path(__file__).name, "ram_rule": "need_mb của từng ca + 6,5% tổng RAM; dừng ở 95%",
                                     "cases_with_measured_peak": sum(1 for c in cases if c["need_basis"].startswith("RAM đỉnh đo"))})
    status, error, done = "COMPLETE", None, 0
    started = time.perf_counter()
    try:
        for stage in stages:
            for case in cases:
                for branch in stage:
                    run_child(out, state, method, branch, case)
                    done += 1
            append(out / "progress.jsonl", {"at_utc": now(), "event": "STAGE_DONE", "stage": list(stage)})
    except Stop as stop:
        status, error = "FAIL_STOP", str(stop)
    except Exception:
        status, error = "DRIVER_ERROR", traceback.format_exc()[-3000:]
    terminal = {"at_utc": now(), "status": status, "error": error, "method": method, "children_ok_this_driver": done,
                "children_expected": len(cases) * sum(len(s) for s in stages), "driver_wall_s": round(time.perf_counter() - started, 3), **state}
    dump(out / ("terminal-" + stamp + ".json"), terminal)
    append(out / "progress.jsonl", {"event": "DRIVER_END", **terminal})
    print(json.dumps(terminal, ensure_ascii=False), flush=True)
    return 0 if status == "COMPLETE" else 1


def main():
    sys.dont_write_bytecode = True
    args = sys.argv[1:]
    if len(args) == 6 and args[0] == "one":
        try:
            return one(*args[1:])
        except Exception:
            traceback.print_exc()
            return 1
    if len(args) == 3 and args[0] == "all":
        return run_all(args[1], args[2])
    if len(args) == 5 and args[0] == "all" and args[3].startswith("--branches=") and args[4].startswith("--datasets="):
        return run_all(args[1], args[2], args[3].split("=", 1)[1].split(","), args[4].split("=", 1)[1].split(","))
    if len(args) == 4 and args[0] == "all" and args[3].startswith("--branches="):
        return run_all(args[1], args[2], args[3].split("=", 1)[1].split(","))
    if len(args) == 2 and args[0] == "precheck":
        result = precheck(args[1])
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return 0 if result["pass"] else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
