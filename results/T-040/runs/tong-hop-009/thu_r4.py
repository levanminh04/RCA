"""Thử trực tiếp hai nhánh dừng của tong_hop.py sau sửa R4.

Nhánh 1 (đầu vào không đạt): chạy CLI thật với snapshot quyết định của run 008, vốn không đạt thật vì
DECISIONS đã có thêm Q-172. Kỳ vọng: thoát mã khác 0; không chạy bước phụ thuộc (không có tong-hop-raw.json,
rows-*.json.gz); bản hiện hành results/T-040/{tong-hop,dau-vao}.json không đổi.

Nhánh 2 (có lỗi tính lại): import tong_hop, bọc stage_compare để chèn một lỗi tính lại giả vào hệ TT, rồi
gọi main() với snapshot hợp lệ của run 009. Kỳ vọng: thoát mã khác 0; giữ chẩn đoán trong run
(tong-hop-raw.json đánh dấu partial, rows-*.json.gz); không có tong-hop.json trong run; bản hiện hành không đổi.
Lỗi chèn giả chỉ chứng minh luồng xử lý, không phải lỗi thật của dữ liệu.

Lệnh: py -3 -X utf8 -B results/T-040/runs/tong-hop-009/thu_r4.py
"""
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
T = os.path.join(ROOT, "results", "T-040")
CUR = ["results/T-040/tong-hop.json", "results/T-040/dau-vao.json"]
PY = [sys.executable, "-X", "utf8", "-B"]


def sha(rel):
    with open(os.path.join(ROOT, rel), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def listing(run):
    d = os.path.join(T, "runs", run)
    return sorted(os.listdir(d)) if os.path.isdir(d) else []


def progress(run):
    path = os.path.join(T, "runs", run, "progress.jsonl")
    return [json.loads(x) for x in open(path, encoding="utf-8")] if os.path.exists(path) else []


def case(run, cmd):
    before = {r: sha(r) for r in CUR}
    t0 = time.time()
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    with open(os.path.join(T, "runs", run + ".stdout.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(p.stdout + ("\n--- stderr ---\n" + p.stderr if p.stderr else ""))
    after = {r: sha(r) for r in CUR}
    files = listing(run)
    stops = [x for x in progress(run) if x.get("step") == "stop"]
    pubs = [x for x in progress(run) if x.get("step") == "publish"]
    return {"run": "runs/" + run, "returncode": p.returncode, "wall_s": round(time.time() - t0, 1),
            "current_unchanged": before == after, "current_sha256": after, "files_in_run": files,
            "stop_events": stops, "publish_events": len(pubs)}


snap008 = "results/T-040/runs/tong-hop-008/doc-quyet-dinh.json"
snap009 = "results/T-040/runs/tong-hop-009/doc-quyet-dinh.json"
res = {"schema": "T040-thu-r4-v1", "started_local": time.strftime("%Y-%m-%d %H:%M:%S")}

r1 = case("thu-r4-dau-vao-001", PY + ["results/T-040/tong_hop.py", "--run", "thu-r4-dau-vao-001",
                                      "--decision-snapshot", snap008])
r1["expect"] = {
    "exit_nonzero": r1["returncode"] != 0,
    "stopped_at_input_gate": bool(r1["stop_events"]) and r1["stop_events"][-1].get("reason") == "kiem_dau_vao_khong_dat",
    "no_dependent_outputs": not any(f.startswith(("tong-hop-raw", "rows-", "tong-hop.json")) for f in r1["files_in_run"]),
    "no_publish": r1["publish_events"] == 0,
    "current_unchanged": r1["current_unchanged"],
}
res["nhanh_dau_vao"] = r1

inject = (
    "import sys; sys.path.insert(0, 'results/T-040'); import tong_hop as th\n"
    "orig = th.stage_compare\n"
    "def bad(*a, **k):\n"
    "    c = orig(*a, **k); c['TT']['recompute_errors'] = dict(c['TT']['recompute_errors'], injected_test_error=1); return c\n"
    "th.stage_compare = bad\n"
    "sys.argv = ['tong_hop.py', '--run', 'thu-r4-tinh-lai-001', '--decision-snapshot', '%s']\n"
    "th.main()\n" % snap009)
r2 = case("thu-r4-tinh-lai-001", PY + ["-c", inject])
r2["expect"] = {
    "exit_nonzero": r2["returncode"] != 0,
    "stopped_at_recompute_gate": bool(r2["stop_events"]) and r2["stop_events"][-1].get("reason") == "loi_tinh_lai",
    "diagnostics_kept": "tong-hop-raw.json" in r2["files_in_run"] and "rows-TT.json.gz" in r2["files_in_run"],
    "no_published_tong_hop_in_run": "tong-hop.json" not in r2["files_in_run"],
    "no_publish": r2["publish_events"] == 0,
    "current_unchanged": r2["current_unchanged"],
}
res["nhanh_tinh_lai"] = r2
res["all_pass"] = all(r1["expect"].values()) and all(r2["expect"].values())
with open(os.path.join(T, "runs", "tong-hop-009", "thu-r4.json"), "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
print(json.dumps({"all_pass": res["all_pass"], "dau_vao": r1["expect"], "tinh_lai": r2["expect"]}, ensure_ascii=False))
