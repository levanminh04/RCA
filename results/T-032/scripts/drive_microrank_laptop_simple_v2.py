"""T-032 MicroRank laptop: vòng lặp tuần tự gọi wrapper v2 đã ghim (Q-108, Q-126). Bản v2.

Khác v1: (1) trước mỗi pha chỉ khởi worker khi RAM trống >= nhu cầu ước + 10% tổng RAM,
để không tiến sát mốc 95%; (2) thời gian chờ RAM không tính vào giờ máy của gói;
(3) nối tiếp được ca dở chưa gọi phương pháp (prepare, source-binding, native chỉ có job.json).

Thay controller/launcher/accountant v2-v3. Không đổi wrapper, phương pháp, adapter,
tiêu chí khớp, tập ca. Wrapper tự làm: kiểm hash nguồn/đầu vào, native khớp bit với bản
đóng băng, observed khớp bit với native, kiểm capture và cờ T-028. Driver chỉ:
  - đi theo plan-52 đã khóa, dùng lại ca đã đóng, không chạy lại ca nào;
  - gọi prepare -> child native -> child observed -> audit, một worker;
  - dừng toàn nhánh ở lỗi đầu tiên, không retry phương pháp;
  - giữ trần Q-124/Q-126: 600 s và 150 MiB mỗi ca, 5 giờ và 2,5 GiB cả gói,
    4 GiB cho results/T-032 trên laptop, dừng khi RAM hệ thống đạt 95%.
Thư mục ca nằm dưới cohort-001 vì wrapper v2 buộc đường dẫn đó; driver không sửa file cũ.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import traceback
from pathlib import Path

REPO = Path("D:/RCA-flashticket")
TASK = REPO / "results/T-032"
COHORT = TASK / "runs/microrank-laptop-cohort-001"
OUT = TASK / "runs/microrank-laptop-simple-driver-002"
WRAPPER = TASK / "scripts/replay_microrank_laptop_exact_v2.py"
WRAPPER_SHA256 = "2cc729cde2f97dee67cf91d5a1cec34790a565effde2c75ad1882db35397dcb1"
PLAN = COHORT / "plan-52.json"
PLAN_SHA256 = "53294858e7fc52ee29c164c1f436b118ea1d5fc2e979ce0658d6888e27b04315"
PYTHON = Path("D:/RCA-ext/envs/T-014-main/Scripts/python.exe")
LOG = REPO / "tasks/T-032-g2-nguyen-nhan-xep-hang/LOG.md"
RETROSPECTIVE = ("RE2-TT", "dev-3defe3d34b")

MAX_CASE_S = 600.0
MAX_CASE_BYTES = 150 * 1024 * 1024
MAX_PACKAGE_S = 5 * 3600.0
MAX_PACKAGE_NEW_BYTES = 5 * 1024 * 1024 * 1024 // 2
MAX_LOCAL_BYTES = 4 * 1024 * 1024 * 1024
MAX_RAM_PERCENT = 95.0
POLL_S = 1.0
RAM_NEED_FACTOR = 1.4
RAM_WAIT_STEP_S = 60.0
MAX_RAM_WAIT_S = 6 * 3600.0  # tổng thời gian chờ RAM của cả lượt; hết thì dừng sạch và báo Minh
RAM_HEADROOM_FRACTION = 0.10  # khoảng cách giữ tới mốc 95% khi khởi worker
DEFAULT_PEAK_MB = {"RE2-TT": 1700.0, "Nezha-OB": 400.0}
# Thời gian đã tính trước driver này: handoff checkpoint.json#/budget
# charged_prior_before_new_v3_tools_s 2163,835 + công cụ v3 đã đo 4,887 + 9,904 + 4,204.
PRIOR_CHARGED_S = 2163.8352518999836 + 4.887440399950061 + 9.9037397 + 4.20391290000407 + 8.790458699979354  # + lượt driver 001
# Dung lượng mới đã dùng trước driver này: segments/002/terminal.json#/guard/peak_new_task_bytes.
PRIOR_NEW_BYTES = 119662283
THREAD_NAMES = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")
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


def tree_bytes(directory):
    total = 0
    stack = [str(directory)]
    while stack:
        with os.scandir(stack.pop()) as entries:
            for entry in entries:
                if entry.is_dir(follow_symlinks=False):
                    stack.append(entry.path)
                elif entry.is_file(follow_symlinks=False):
                    total += entry.stat(follow_symlinks=False).st_size
    return total


def manifest(directory, excluded=()):
    directory = Path(directory)
    rows = []
    for path in sorted(directory.rglob("*")):
        relative = path.relative_to(directory).as_posix()
        if path.is_file() and relative not in excluded:
            rows.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha(path)})
    return rows


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
    """So từng bit hai bản ghi, bỏ các trường EXCLUDED_FIELDS ở mức gốc."""
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


def child_environment():
    env = os.environ.copy()
    for name in THREAD_NAMES:
        env.pop(name, None)
    env["PYTHONHASHSEED"] = "0"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = "D:/RCA-ext/src/RCAEval;D:/RCA-ext/src/baro;D:/RCA-ext/work/T-014/CIRCA;D:/RCA-flashticket/src"
    env["TMP"] = env["TEMP"] = str(COHORT / "tmp")
    env["MPLCONFIGDIR"] = str(COHORT / "cache/mpl")
    return env


class Run:
    def __init__(self):
        import psutil
        self.psutil = psutil
        self.started = time.perf_counter()
        self.peak_ram_percent = 0.0
        self.new_bytes = 0
        self.local_bytes_at_start = tree_bytes(TASK)
        self.case_started = None
        self.first_new_re2_logged = False
        self.ram_wait_s = 0.0

    def package_wall(self):
        return PRIOR_CHARGED_S + time.perf_counter() - self.started - self.ram_wait_s

    def kill_tree(self, pid):
        try:
            parent = self.psutil.Process(pid)
            targets = parent.children(recursive=True) + [parent]
        except self.psutil.NoSuchProcess:
            return
        for process in targets:
            try:
                process.kill()
            except self.psutil.NoSuchProcess:
                pass

    def wait_for_ram(self, need_bytes, opaque_id):
        """Chờ RAM trống đủ cho worker; hết quỹ chờ thì dừng sạch trước khi gọi phương pháp."""
        while True:
            memory = self.psutil.virtual_memory()
            self.peak_ram_percent = max(self.peak_ram_percent, memory.percent)
            if memory.available >= need_bytes + RAM_HEADROOM_FRACTION * memory.total and memory.percent < MAX_RAM_PERCENT:
                return
            require(self.ram_wait_s < MAX_RAM_WAIT_S and self.package_wall() < MAX_PACKAGE_S,
                    "RAM không đủ cho worker ca " + opaque_id + ": cần " + str(int(need_bytes + RAM_HEADROOM_FRACTION * memory.total)) + " byte trống, đang có "
                    + str(memory.available) + " (Q-126 mục 3); chưa gọi phương pháp cho ca này")
            with (OUT / "progress.jsonl").open("a", encoding="utf-8", newline="\n") as stream:
                stream.write(json.dumps({"at_utc": now(), "event": "WAIT_RAM", "opaque_id": opaque_id,
                                         "need_bytes": need_bytes, "available_bytes": memory.available,
                                         "waited_s": self.ram_wait_s}) + "\n")
            time.sleep(RAM_WAIT_STEP_S)
            self.ram_wait_s += RAM_WAIT_STEP_S
            self.case_started += RAM_WAIT_STEP_S  # thời gian chờ RAM không tính vào 600 s xử lý của ca

    def call(self, phase, opaque_id, arguments):
        """Chạy một lệnh con của wrapper, canh RAM/thời gian mỗi giây, đóng stream, trả chi phí."""
        require(sha(WRAPPER) == WRAPPER_SHA256, "wrapper đổi trước khi gọi")
        memory = self.psutil.virtual_memory()
        self.peak_ram_percent = max(self.peak_ram_percent, memory.percent)
        require(memory.percent < MAX_RAM_PERCENT, "RAM hệ thống đạt 95% trước worker (Q-126)")
        token = phase + "-" + opaque_id
        logs = OUT / "logs"
        logs.mkdir(parents=True, exist_ok=True)
        command = [str(PYTHON), "-B", "-W", "ignore", "-X", "utf8", str(WRAPPER)] + arguments
        dump_new(logs / (token + "-command.json"), {"argv": command, "at_utc": now(), "cwd": str(REPO), "phase": phase})
        started = time.perf_counter()
        stopped = None
        with (logs / (token + "-stdout.txt")).open("x", encoding="utf-8") as stdout, \
                (logs / (token + "-stderr.txt")).open("x", encoding="utf-8") as stderr:
            child = subprocess.Popen(command, cwd=REPO, env=child_environment(), stdin=subprocess.DEVNULL,
                                     stdout=stdout, stderr=stderr, creationflags=subprocess.CREATE_NO_WINDOW)
            while child.poll() is None:
                percent = self.psutil.virtual_memory().percent
                self.peak_ram_percent = max(self.peak_ram_percent, percent)
                if percent >= MAX_RAM_PERCENT:
                    stopped = "RAM hệ thống đạt 95% khi worker đang chạy (Q-126)"
                elif time.perf_counter() - self.case_started >= MAX_CASE_S:
                    stopped = "ca vượt 600 s (Q-124)"
                elif self.package_wall() >= MAX_PACKAGE_S:
                    stopped = "gói vượt 5 giờ (Q-126)"
                if stopped:
                    self.kill_tree(child.pid)
                    child.wait()
                    break
                time.sleep(POLL_S)
            code = child.wait()
        cost = {"phase": phase, "exit_code": code, "wall_s": time.perf_counter() - started,
                "stopped_by_driver": stopped, "peak_system_ram_percent_so_far": self.peak_ram_percent}
        dump_new(logs / (token + "-process.json"), cost)
        require(stopped is None, stopped or "")
        require(code == 0, phase + " thoát mã " + str(code) + "; dừng, không retry")
        return cost

    def closed_check(self, directory, phase):
        check = read(Path(directory) / "check.json")
        require(check.get("status") == "PASS" and check.get("passed") is True, phase + " không PASS")
        require(check.get("manifest_excludes") == ["check.json"], phase + " manifest lạ")
        require(not (Path(directory) / "failure-after-check.json").exists(), phase + " có lỗi sau check")
        verify_manifest(directory, check["artifact_manifest"], ["check.json"])
        return check

    def run_case(self, row):
        dataset, opaque_id = row["dataset"], row["opaque_id"]
        directory = COHORT / "cases" / dataset / opaque_id
        self.case_started = time.perf_counter()
        costs = []
        prepare_reused = False
        if directory.exists():
            # Chỉ nối tiếp ca dở CHƯA gọi phương pháp: prepare đã PASS; có thể đã có source-binding.json
            # và native/ chỉ chứa job.json (wrapper ghi invocation.json trước khi gọi worker).
            names = {p.name for p in directory.iterdir()}
            require("prepare" in names and names <= {"prepare", "source-binding.json", "native"},
                    "thư mục ca đã tồn tại với nội dung ngoài trường hợp nối tiếp; không chạy lại")
            if "native" in names:
                require({p.name for p in (directory / "native").iterdir()} == {"job.json"},
                        "native đã có file ngoài job.json; có thể đã gọi phương pháp; không chạy lại")
            prepared_check = self.closed_check(directory / "prepare", "prepare cũ")
            require(prepared_check.get("methods_executed") is False, "prepare cũ đã gọi phương pháp")
            prepare_reused = True
        else:
            directory.mkdir(parents=True)
            self.wait_for_ram(int(DEFAULT_PEAK_MB[dataset] * RAM_NEED_FACTOR * 1024 * 1024), opaque_id)
            costs.append(self.call("prepare", opaque_id, ["prepare", dataset, opaque_id, str(directory / "prepare")]))
            prepared_check = self.closed_check(directory / "prepare", "prepare")
        payload = read(directory / "prepare/prepare.json")
        require(prepared_check["prepare_sha256"] == sha(directory / "prepare/prepare.json"), "prepare.json khác check")
        require(payload["entry"]["sha256"] == row["source_sha256"] and payload["frozen"]["status"] == row["source_status"],
                "bản đóng băng khác plan đã khóa")
        frozen = payload["frozen"]
        # Q-126 mục 3: không khởi worker khi RAM không đủ. Nhu cầu ước từ RAM đỉnh native đã ghi
        # trong bản đóng băng của chính ca này, nhân 1,4 (observed/native đo được 1,21 ở RE2, 1,12 ở Nezha).
        frozen_peak_mb = (frozen.get("cost") or {}).get("peak_rss_mb") or DEFAULT_PEAK_MB[dataset]
        need_bytes = int(frozen_peak_mb * RAM_NEED_FACTOR * 1024 * 1024)
        binding = {key: payload[key] for key in ("entry", "source_checks", "input_checks", "code_hashes", "frozen")}
        if (directory / "source-binding.json").exists():
            require(read(directory / "source-binding.json") == binding, "source-binding.json cũ khác prepare")
        else:
            dump_new(directory / "source-binding.json", binding)
        records = {}
        for mode in ("native", "observed"):
            mode_dir = directory / mode
            if mode == "native" and mode_dir.exists():
                require(read(mode_dir / "job.json") == payload["job"], "job.json cũ khác prepare")
            elif mode == "native":
                mode_dir.mkdir()
                dump_new(mode_dir / "job.json", payload["job"])
            else:
                mode_dir.mkdir()
                shutil.copyfile(directory / "native/job.json", mode_dir / "job.json")
            job_sha = sha(mode_dir / "job.json")
            self.wait_for_ram(need_bytes, opaque_id)
            require(job_sha == sha(directory / "native/job.json"), "job observed khác native")
            costs.append(self.call(mode, opaque_id, ["child", mode, dataset, opaque_id, str(mode_dir),
                                                      "--job-sha256", job_sha, "--frozen-sha256", row["source_sha256"]]))
            check = self.closed_check(mode_dir, mode)
            require((check["dataset"], check["opaque_id"], check["mode"]) == (dataset, opaque_id, mode)
                    and check["job_sha256"] == job_sha and check["frozen_sha256"] == row["source_sha256"],
                    mode + ": định danh/nguồn khác")
            require(check.get("source_checks_passed") is True and check.get("frozen_exact") is True
                    and check.get("differences") == [] and check.get("native_observed_differences") == []
                    and check.get("worker_streams_closed") is True, mode + ": bất biến khớp/nguồn không đạt")
            records[mode] = read(mode_dir / "ban-ghi-0.json")
            differences = bit_differences(frozen, records[mode])
            require(not differences, mode + " lệch bản đóng băng: " + "; ".join(differences[:5]))
            if mode == "native":
                require(check.get("native_observer_absent") is True and check.get("native_frozen_exact") is True,
                        "native: thiếu bất biến")
            else:
                require(check.get("observed_frozen_exact") is True and check.get("native_observed_exact") is True
                        and check.get("capture_check", {}).get("pass") is True, "observed: thiếu bất biến")
                differences = bit_differences(records["native"], records["observed"])
                require(not differences, "observed lệch native: " + "; ".join(differences[:5]))
        self.wait_for_ram(need_bytes, opaque_id)
        costs.append(self.call("audit", opaque_id, ["audit", dataset, opaque_id, str(directory / "native"),
                                                     str(directory / "observed"), str(directory / "audit")]))
        audit = self.closed_check(directory / "audit", "audit")
        for key in ("native_frozen_exact", "observed_frozen_exact", "native_observed_exact", "capture_pass", "t028_pass"):
            require(audit.get(key) is True, "audit thiếu/không đạt: " + key)
        for key in ("numeric_differences", "service_order_tie_differences", "other_differences"):
            require(audit.get(key) == [], "audit có khác biệt: " + key)
        numeric = audit["numeric_summary"]
        if numeric["matched_score_count"]:
            require(numeric["max_ulp_distance"] == 0 and numeric["max_relative"] == 0, "audit có lệch điểm")
        else:
            require(numeric["max_ulp_distance"] is None and numeric["max_relative"] is None, "audit: không có cặp điểm phải để null")
        source_status = audit.get("source_status")
        require((audit["dataset"], audit["opaque_id"]) == (dataset, opaque_id) and source_status == row["source_status"],
                "audit: định danh/trạng thái nguồn khác")
        require(audit.get("intermediates_eligible") is (source_status == "OK"), "audit: eligibility không khớp trạng thái nguồn")
        logs = [path for run_dir in (TASK / "runs/microrank-laptop-simple-driver-001", OUT)
                for path in sorted((run_dir / "logs").glob("*-" + opaque_id + "-*")) if path.is_file()]
        dump_new(directory / "stream-receipts.json", {"all_child_streams_closed": True,
                 "files": [{"path": str(path), "bytes": path.stat().st_size, "sha256": sha(path)} for path in logs],
                 "manifest_note": "log của driver đơn giản nằm ngoài thư mục ca (lượt 001 nếu có và lượt 002), ghim tại đây"})
        case_bytes = tree_bytes(directory) + sum(path.stat().st_size for path in logs)
        wall = time.perf_counter() - self.case_started
        worker_cost = {mode: read(directory / mode / "cost.json") for mode in ("native", "observed")}
        dump_new(directory / "case-terminal.json", {
            "status": "PASS_EXACT" if source_status == "OK" else "PASS_NON_OK_EXACT", "at_utc": now(),
            "dataset": dataset, "opaque_id": opaque_id, "source_status": source_status,
            "audit_check_sha256": sha(directory / "audit/check.json"), "wall_s": wall,
            "new_task_bytes_delta": case_bytes, "prepare_reused_from_segment_002": prepare_reused,
            "driver": "drive_microrank_laptop_simple_v2", "driver_sha256": sha(__file__),
            "guard": {"peak_system_ram_percent": self.peak_ram_percent, "max_case_s": MAX_CASE_S,
                      "max_case_bytes": MAX_CASE_BYTES, "poll_s": POLL_S, "polling_can_overshoot": True},
            "worker_cost": worker_cost, "phase_costs": costs,
            "intermediates_eligible": audit["intermediates_eligible"]})
        closed = {"status": "CLOSED_EXACT_CASE", "files": manifest(directory, ("closed.json",)),
                  "manifest_excludes": ["closed.json"]}
        dump_new(directory / "closed.json", closed)
        verify_manifest(directory, closed["files"], ["closed.json"])
        # Trần kiểm sau khi đóng ca: ca vẫn được giữ nguyên, nhưng nhánh dừng nếu vượt.
        self.new_bytes += case_bytes
        require(wall < MAX_CASE_S, "ca vượt 600 s (Q-124)")
        require(case_bytes <= MAX_CASE_BYTES, "ca vượt 150 MiB (Q-124)")
        require(PRIOR_NEW_BYTES + self.new_bytes <= MAX_PACKAGE_NEW_BYTES, "gói vượt 2,5 GiB mới (Q-124)")
        require(self.local_bytes_at_start + self.new_bytes <= MAX_LOCAL_BYTES, "results/T-032 trên laptop vượt 4 GiB (Q-124)")
        require(self.package_wall() < MAX_PACKAGE_S, "gói vượt 5 giờ (Q-126)")
        result = {"dataset": dataset, "opaque_id": opaque_id, "source_status": source_status, "result": "exact"
                  if source_status == "OK" else "non_OK_exact", "matched_score_count": numeric["matched_score_count"],
                  "max_ulp_distance": numeric["max_ulp_distance"], "max_relative": numeric["max_relative"],
                  "wall_s": wall, "case_bytes": case_bytes, "prepare_reused": prepare_reused,
                  "native_worker_wall_s": worker_cost["native"].get("wall_s"),
                  "observed_worker_wall_s": worker_cost["observed"].get("wall_s"),
                  "native_peak_rss_mb": worker_cost["native"].get("peak_rss_mb"),
                  "observed_peak_rss_mb": worker_cost["observed"].get("peak_rss_mb"),
                  "closed_sha256": sha(directory / "closed.json"), "path": str(directory)}
        if dataset == "RE2-TT" and not self.first_new_re2_logged:
            self.first_new_re2_logged = True
            dump_new(OUT / "first-new-re2-peak.json", result)
            # Q-126 mục 3: ghi RAM đỉnh thật của ca RE2 đầu tiên vào LOG rồi chạy tiếp.
            with LOG.open("a", encoding="utf-8", newline="\n") as stream:
                stream.write("\n- [driver đơn giản v2, " + now() + "] Ca RE2 mới đầu tiên " + opaque_id
                             + " (" + str(source_status) + "): RAM đỉnh worker native "
                             + str(worker_cost["native"].get("peak_rss_mb")) + " MiB, observed "
                             + str(worker_cost["observed"].get("peak_rss_mb"))
                             + " MiB (Windows peak working set, nguồn cases/RE2-TT/" + opaque_id
                             + "/{native,observed}/cost.json); RAM hệ thống đỉnh tới lúc này "
                             + str(self.peak_ram_percent) + "%. Chạy tiếp theo Q-126 mục 3.\n")
        return result


def reused(row):
    dataset, opaque_id = row["dataset"], row["opaque_id"]
    if (dataset, opaque_id) == RETROSPECTIVE:
        directory = COHORT / "retrospective-dev-3defe3d34b"
    else:
        directory = COHORT / "cases" / dataset / opaque_id
    if not (directory / "closed.json").is_file():
        return None
    closed = read(directory / "closed.json")
    verify_manifest(directory, closed["files"], ["closed.json"])
    audit = read(directory / "audit/check.json")
    require(audit.get("status") == "PASS" and audit.get("classification") in ("exact", "non_OK_exact")
            and audit.get("source_status") == row["source_status"], "ca đã đóng không còn hợp lệ: " + opaque_id)
    return {"dataset": dataset, "opaque_id": opaque_id, "source_status": row["source_status"],
            "result": audit["classification"], "reused_closed_case": True,
            "matched_score_count": audit["numeric_summary"]["matched_score_count"],
            "max_ulp_distance": audit["numeric_summary"]["max_ulp_distance"],
            "max_relative": audit["numeric_summary"]["max_relative"],
            "closed_sha256": sha(directory / "closed.json"), "path": str(directory)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true", help="chỉ kiểm ghim, plan và ca đã đóng; không gọi wrapper")
    args = parser.parse_args()
    require(Path(sys.executable).resolve() == PYTHON.resolve(), "phải chạy bằng Python môi trường nguồn")
    require(sha(WRAPPER) == WRAPPER_SHA256 and sha(PLAN) == PLAN_SHA256, "ghim wrapper/plan khác")
    plan = read(PLAN)
    rows = plan["rows"]
    require(len(rows) == 52 and len({(r["dataset"], r["opaque_id"]) for r in rows}) == 52, "plan không đủ 52 ca")
    done = [reused(row) for row in rows]
    todo = [row for row, item in zip(rows, done) if item is None]
    summary = {"closed_reused": sum(item is not None for item in done), "to_run": len(todo),
               "to_run_first": [(r["dataset"], r["opaque_id"], r["source_status"]) for r in todo[:3]],
               "prior_charged_s": PRIOR_CHARGED_S, "local_task_bytes": tree_bytes(TASK)}
    if args.check_only:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    require(not OUT.exists(), "thư mục lượt driver đã tồn tại; không chạy đè")
    OUT.mkdir(parents=True)
    dump_new(OUT / "start.json", {"at_utc": now(), "argv": sys.argv, "pid": os.getpid(), "driver_sha256": sha(__file__),
             "wrapper_sha256": WRAPPER_SHA256, "plan_sha256": PLAN_SHA256, "authority": "Q-108, Q-124, Q-126",
             "limits": {"case_s": MAX_CASE_S, "case_bytes": MAX_CASE_BYTES, "package_s": MAX_PACKAGE_S,
                        "package_new_bytes": MAX_PACKAGE_NEW_BYTES, "local_bytes": MAX_LOCAL_BYTES,
                        "ram_percent": MAX_RAM_PERCENT}, **summary})
    run = Run()
    results = list(done)
    status, error = "PASS_52_EXACT", None
    try:
        for index, row in enumerate(rows):
            if results[index] is not None:
                continue
            with (OUT / "progress.jsonl").open("a", encoding="utf-8", newline="\n") as stream:
                stream.write(json.dumps({"at_utc": now(), "event": "CASE_START", "dataset": row["dataset"],
                                         "opaque_id": row["opaque_id"], "package_wall_s": run.package_wall()}) + "\n")
            results[index] = run.run_case(row)
            with (OUT / "progress.jsonl").open("a", encoding="utf-8", newline="\n") as stream:
                stream.write(json.dumps({"at_utc": now(), "event": "CASE_PASS", **results[index],
                                         "package_wall_s": run.package_wall(),
                                         "peak_system_ram_percent": run.peak_ram_percent}, ensure_ascii=False) + "\n")
    except BaseException as failure:  # dừng toàn nhánh, giữ mọi file dở
        status = "FAIL_STOP"
        error = {"type": type(failure).__name__, "message": str(failure), "traceback": traceback.format_exc()}
    table = [item if item is not None else {"dataset": row["dataset"], "opaque_id": row["opaque_id"],
             "source_status": row["source_status"], "result": "not_run"} for row, item in zip(rows, results)]
    dump_new(OUT / "52-cases.json", {"schema": "T032-microrank-laptop-simple-driver-v2", "rows": table})
    dump_new(OUT / "terminal.json", {"status": status, "at_utc": now(), "error": error,
             "counts": {key: sum(r["result"] == key for r in table) for key in ("exact", "non_OK_exact", "not_run")},
             "driver_wall_s": time.perf_counter() - run.started, "package_wall_s": run.package_wall(),
             "new_bytes_this_driver": run.new_bytes, "peak_system_ram_percent": run.peak_ram_percent,
             "ram_wait_s_excluded_from_package_wall": run.ram_wait_s,
             "retry_performed": False, "a_prime_run": False})
    dump_new(OUT / "manifest.json", {"files": manifest(OUT, ("manifest.json",)), "manifest_excludes": ["manifest.json"]})
    print(json.dumps(read(OUT / "terminal.json"), ensure_ascii=False))
    return 0 if status == "PASS_52_EXACT" else 1


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
