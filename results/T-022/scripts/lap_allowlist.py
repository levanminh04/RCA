"""T-022 bước 1: lập allowlist 30 ca dev RE2-TT và file nhãn tách riêng.

Chỉ đọc metadata đã có (T-002, T-021, T-017) và băm file dữ liệu dev trong data/rcaeval/.
Không đọc data/locked/. Không đọc nội dung số đo (chỉ băm byte).

Đầu ra (trong --out, mặc định results/T-022/):
  allowlist-dev.json : phía runner. Mã ca mờ, đường dẫn tương đối, SHA-256, provenance.
  nhan-dev.json      : phía runner/evaluator. root, loại lỗi, ô, mốc tiêm và nguồn mốc.
  cot-bocpd-dev.csv  : số cột theo luật chọn cột của reproduce_bocpd, đếm trên schemas.json.
  runs/<run>/kiem-allowlist.json : kết quả các phép kiểm.

Chạy:  py -3 -B results/T-022/scripts/lap_allowlist.py --run allowlist-001
"""
import argparse
import csv
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SPLIT = "results/T-021/chia-theo-o/A-phan-tang.csv"
CASE_SUMMARY = "results/T-002/local-inspection/run-002/case-summary.csv"
T002_MANIFEST = "results/T-002/local-inspection/run-002/manifest.json"
SCHEMAS = "results/T-002/local-inspection/run-002/schemas.json"
T017_ALLOW = "results/T-017/allowlist.json"
DATA_ROOT = "data/rcaeval"
HF_REVISION = "afeacb11bcc94dadfd1c8f483ee4377b2b8b614e"
FILES = ("metrics.parquet", "traces.parquet", "logs.parquet")


def sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def rel(p):
    return os.path.relpath(p, REPO).replace("\\", "/")


def bocpd_selected(name):
    # Luật chọn cột của reproduce_bocpd (BARO e35f4ec, baro/reproducibility.py:139-145).
    if "queue-master" in name or "rabbitmq_" in name:
        return False
    return ("latency-50" in name) or ("_error" in name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--out", default=os.path.join(REPO, "results", "T-022"))
    args = ap.parse_args()

    t0 = time.perf_counter()
    started = datetime.now(timezone.utc).isoformat()
    run_dir = os.path.join(args.out, "runs", args.run)
    if os.path.exists(run_dir):
        sys.exit(f"run dir đã có, không ghi đè: {run_dir}")
    os.makedirs(run_dir)
    checks = {}

    # 1. Danh sách dev từ chia T-021 (gói A).
    with open(os.path.join(REPO, SPLIT), encoding="utf-8") as f:
        split_rows = [r for r in csv.DictReader(f)]
    dev_rows = [r for r in split_rows if r["dataset"] == "RE2-TT" and r["vai_tro"] == "dev"]
    dev_cases = sorted(r["case"] for r in dev_rows)
    checks["so_ca_dev_T021"] = len(dev_cases)
    checks["ca_dev_duy_nhat"] = len(set(dev_cases)) == len(dev_cases)
    cells = {}
    for r in dev_rows:
        cells.setdefault((r["root"], r["fault"]), []).append(int(r["rep"]))
    checks["so_o_dev"] = len(cells)
    checks["moi_o_du_rep_1_2_3"] = all(sorted(v) == [1, 2, 3] for v in cells.values())

    # 2. Đối chiếu case-summary T-002 và allowlist T-017.
    with open(os.path.join(REPO, CASE_SUMMARY), encoding="utf-8") as f:
        cs = {r["case"]: r for r in csv.DictReader(f)}
    cs_tt = sorted(k for k, v in cs.items() if v["dataset"] == "re2tt")
    checks["tap_dev_trung_case_summary_re2tt"] = cs_tt == dev_cases
    with open(os.path.join(REPO, T017_ALLOW), encoding="utf-8") as f:
        t017 = sorted(json.load(f))
    checks["tap_dev_trung_allowlist_T017"] = t017 == dev_cases

    # 3. Nguồn mốc tiêm: manifest T-002 (hash file inject_time.txt từ HF hoặc bản local).
    with open(os.path.join(REPO, T002_MANIFEST), encoding="utf-8") as f:
        man = json.load(f)
    checks["manifest_T002_hf_revision"] = man.get("hf_revision")
    inj = {x["case"]: x for x in man["injections"]}

    # 4. Từng ca: đường dẫn, băm, nhãn.
    allow_cases, label_cases, bocpd_rows = [], [], []
    path_problems, opaque_seen = [], set()
    with open(os.path.join(REPO, SCHEMAS), encoding="utf-8") as f:
        schemas = json.load(f)
    split_by_case = {r["case"]: r for r in dev_rows}
    for case in dev_cases:
        case_dir = os.path.normpath(os.path.join(REPO, DATA_ROOT, case))
        rp = rel(case_dir)
        if not rp.startswith(DATA_ROOT + "/") or "locked" in rp.split("/") or ".." in rp:
            path_problems.append(rp)
        files = {}
        for fn in FILES:
            p = os.path.join(case_dir, fn)
            if os.path.exists(p):
                files[fn] = {"path": rel(p), "bytes": os.path.getsize(p), "sha256": sha256_file(p)}
            else:
                files[fn] = None
        m_sha = files["metrics.parquet"]["sha256"]
        opaque = "dev-" + m_sha[:10]
        if opaque in opaque_seen:
            sys.exit(f"trùng mã mờ {opaque}")
        opaque_seen.add(opaque)
        allow_cases.append({"opaque_id": opaque, "case_dir": rp, "files": files})

        s = split_by_case[case]
        c = cs[case]
        inject_time = int(c["inject_time"])
        t_min = int(c["metric_time_min"])
        x = inj[case]
        label_cases.append({
            "opaque_id": opaque,
            "case": case,
            "root": s["root"],
            "fault": s["fault"],
            "nhom_loi": s["nhom_loi"],
            "rep": int(s["rep"]),
            "cell": f"{s['root']}|{s['fault']}",
            "nhom_vi_tri_p75": s["nhom_vi_tri_p75"],
            "tx": s["tx"],
            "inject_time": inject_time,
            "inject_time_source": x["source"],
            "inject_time_source_sha256": x["sha256"],
            "metric_time_min": t_min,
            "metric_time_max": int(c["metric_time_max"]),
            "n_metric_rows": int(c["n_metric_rows"]),
            "normal_rows_truoc_moc": int(c["normal_rows"]),
            "moc_tru_dau_file_s": inject_time - t_min,
        })

        names = [col["name"] for col in schemas[f"{case}/metrics.parquet"]]
        sel = [n for n in names if bocpd_selected(n)]
        bocpd_rows.append({
            "opaque_id": opaque,
            "n_cot_metric": len(names),
            "n_cot_bocpd_tho": len(sel),
            "n_latency50": sum("latency-50" in n for n in sel),
            "n_error": sum("_error" in n for n in sel),
        })

    checks["duong_dan_ngoai_data_rcaeval_hoac_locked"] = path_problems
    checks["so_file_thieu"] = {fn: sum(1 for a in allow_cases if a["files"][fn] is None) for fn in FILES}
    checks["ca_thieu_logs"] = [a["opaque_id"] for a in allow_cases if a["files"]["logs.parquet"] is None]
    checks["moc_tru_dau_file_s"] = sorted({lc["moc_tru_dau_file_s"] for lc in label_cases})
    checks["n_metric_rows"] = sorted({lc["n_metric_rows"] for lc in label_cases})
    tong_byte = sum(f["bytes"] for a in allow_cases for f in a["files"].values() if f)
    checks["tong_byte_30_ca"] = tong_byte
    # So byte với case-summary T-002.
    lech_byte = []
    for a, lc in zip(allow_cases, label_cases):
        c = cs[lc["case"]]
        for fn, col in (("metrics.parquet", "metrics_bytes"), ("traces.parquet", "traces_bytes"), ("logs.parquet", "logs_bytes")):
            want = int(c[col]) if c[col] else None
            got = a["files"][fn]["bytes"] if a["files"][fn] else None
            if want != got:
                lech_byte.append([lc["case"], fn, want, got])
    checks["byte_lech_case_summary"] = lech_byte
    # Mốc local inject_time.txt nếu có: kiểm hash khớp manifest.
    local_inj = []
    for lc in label_cases:
        p = os.path.join(REPO, DATA_ROOT, lc["case"], "inject_time.txt")
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                v = int(f.read().strip())
            local_inj.append({"case": lc["case"], "value_khop": v == lc["inject_time"],
                              "sha256_khop": sha256_file(p) == lc["inject_time_source_sha256"]})
    checks["inject_time_local"] = local_inj
    checks["tat_ca_dat"] = (
        checks["so_ca_dev_T021"] == 30 and checks["ca_dev_duy_nhat"] and checks["so_o_dev"] == 10
        and checks["moi_o_du_rep_1_2_3"] and checks["tap_dev_trung_case_summary_re2tt"]
        and checks["tap_dev_trung_allowlist_T017"] and not path_problems and not lech_byte
        and checks["manifest_T002_hf_revision"] == HF_REVISION
        and all(x["value_khop"] and x["sha256_khop"] for x in local_inj)
    )

    # Ghi đầu ra. Thứ tự theo mã mờ để thứ tự không lộ root.
    order = sorted(range(len(allow_cases)), key=lambda i: allow_cases[i]["opaque_id"])
    provenance = {
        "task": "T-022",
        "script": rel(__file__),
        "script_sha256": sha256_file(__file__),
        "run": args.run,
        "tao_luc_utc": started,
        "nguon_du_lieu": {"hf_repo": "phamquiluan/RCAEval", "hf_revision": HF_REVISION, "thu_muc": DATA_ROOT,
                          "ghi_chu": "chép từ lần tải trước, đã kiểm hash HF (data/README.md)"},
        "nguon_chia": {"file": SPLIT, "sha256": sha256_file(os.path.join(REPO, SPLIT)), "goi": "A", "vai_tro": "dev"},
        "doi_chieu": {CASE_SUMMARY: sha256_file(os.path.join(REPO, CASE_SUMMARY)),
                      T017_ALLOW: sha256_file(os.path.join(REPO, T017_ALLOW))},
    }
    allow = {
        "mo_ta": "Allowlist 30 ca dev RE2-TT cho P3. Chỉ runner đọc file này. Phương pháp không nhận case_dir hay opaque_id.",
        "provenance": provenance,
        "so_ca": len(allow_cases),
        "cases": [allow_cases[i] for i in order],
    }
    labels = {
        "mo_ta": "Nhãn 30 ca dev RE2-TT. Chỉ runner (lấy mốc cho chế độ a) và evaluator đọc. Không truyền vào phương pháp.",
        "provenance": dict(provenance, nguon_moc={"file": T002_MANIFEST, "sha256": sha256_file(os.path.join(REPO, T002_MANIFEST))}),
        "so_ca": len(label_cases),
        "cases": [label_cases[i] for i in order],
    }
    with open(os.path.join(args.out, "allowlist-dev.json"), "w", encoding="utf-8") as f:
        json.dump(allow, f, ensure_ascii=False, indent=1)
    with open(os.path.join(args.out, "nhan-dev.json"), "w", encoding="utf-8") as f:
        json.dump(labels, f, ensure_ascii=False, indent=1)
    with open(os.path.join(args.out, "cot-bocpd-dev.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(bocpd_rows[0].keys()))
        w.writeheader()
        for i in order:
            w.writerow(bocpd_rows[i])
    checks["thoi_gian_s"] = round(time.perf_counter() - t0, 3)
    checks["xong_utc"] = datetime.now(timezone.utc).isoformat()
    with open(os.path.join(run_dir, "kiem-allowlist.json"), "w", encoding="utf-8") as f:
        json.dump(checks, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in checks.items() if k != "inject_time_local"}, ensure_ascii=False))
    return 0 if checks["tat_ca_dat"] else 1


if __name__ == "__main__":
    sys.exit(main())
