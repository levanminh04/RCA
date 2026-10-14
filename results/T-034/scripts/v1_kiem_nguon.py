"""T-034 V1: kiểm nguồn trước khi dùng số hoặc nối WHY. Chỉ đọc, trừ file kết quả của chính lượt.

Ba loại nguồn (SPEC mục "Kiểm đúng đắn", V1):
  A. Kết quả bất biến: phải khớp manifest đúng phiên bản.
     - hai cây bổ sung T-032/T-033: manifest-final.json (toàn bộ file);
     - gói đính chính 13/10: manifest-review-001.json (files, source_pins);
     - kết quả cũ T-006..T-033: old-files-before.json (bản ghim trước gói bổ sung).
  B. Tài liệu chỉ nối (WHY, DECISIONS, LOG T-032/T-033): phần đầu phải khớp bản đã chứng nhận;
     phần nối thêm được in ra để đối chiếu nguồn duyệt.
  C. Tài liệu khung và SPEC: ghim phiên bản đang dùng (không ép khớp bản cũ).

Dùng: python v1_kiem_nguon.py <thư mục lượt> [--full-t032]
"""
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SUP = ROOT / "results/T-032/runs/bo-sung-toan-dien-20261012-001"
BS = chr(92)

# Tài liệu chỉ nối: đường dẫn -> nguồn chứng nhận phần đầu
APPEND_ONLY = ["docs/WHY.md", "docs/DECISIONS.md", "tasks/T-032-g2-nguyen-nhan-xep-hang/LOG.md",
               "tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md"]
# Tài liệu khung ghim theo phiên bản đang dùng
FRAME = ["AGENTS.md", "CLAUDE.md", "docs/MRP.md", "docs/PLAN-P3-G2.md", "docs/DECISIONS.md", "docs/LESSONS.md",
         "docs/WHY.md", "docs/STATE.md", "docs/review-prompt.md", "docs/reference/sources/DT18-de-tai-va-nhiem-vu.md",
         "docs/reference/sources/advisor-2026-09-23.md", "tasks/T-034-g2-goi-trinh/SPEC.md", "tasks/_MAU/LOG.md",
         "tasks/_MAU/REVIEW.md", "tasks/_MAU/SPEC.md", "tasks/T-032-g2-nguyen-nhan-xep-hang/SPEC.md",
         "tasks/T-033-g2-nguyen-nhan-phat-hien/SPEC.md"]
EXTERNAL = {"B16": Path("D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md"),
            "BARO_bocpd": Path("D:/RCA-ext/src/baro/baro/_bocpd.py"),
            "BARO_utility": Path("D:/RCA-ext/src/baro/baro/utility.py")}
# Thư mục kết quả cũ được kiểm toàn bộ theo old-files-before.json (T-032 cũ: chỉ khi --full-t032; nếu không, kiểm phần T-034 dùng)
OLD_FULL = ["results/T-006", "results/T-007", "results/T-013", "results/T-014", "results/T-015", "results/T-016", "results/T-017",
            "results/T-018", "results/T-021", "results/T-022", "results/T-024", "results/T-025", "results/T-026", "results/T-028",
            "results/T-029", "results/T-031", "results/T-033", "src/"]
T032_USED_PREFIX = ["results/T-032/nguyen-nhan-xep-hang.md", "results/T-032/kiem-tiep.md", "results/T-032/doc-tay.md",
                    "results/T-032/ket-qua-phien-", "results/T-032/thiet-ke-", "results/T-032/goi-bo-sung-", "results/T-032/scripts/",
                    "results/T-032/runs/tracerca-original-ranking-001/", "results/T-032/runs/sua-review-001/",
                    "results/T-032/bao-phu", "results/T-032/caller-root", "results/T-032/kha-nang-do", "results/T-032/lan"]


def sha(path, n=None):
    h = hashlib.sha256()
    left = n
    with open(path, "rb") as f:
        while True:
            size = 1 << 20 if left is None else min(1 << 20, left)
            if size == 0:
                break
            block = f.read(size)
            if not block:
                break
            h.update(block)
            if left is not None:
                left -= len(block)
    return h.hexdigest()


def check_list(items, label, out, select=None):
    began = time.perf_counter()
    ok = bad = missing = total_bytes = 0
    problems = []
    for it in items:
        rel = it["path"].replace(BS, "/")
        if select and not select(rel):
            continue
        p = ROOT / rel
        if not p.is_file():
            missing += 1
            problems.append({"path": rel, "kind": "missing"})
            continue
        size = p.stat().st_size
        if size != it["bytes"] or sha(p) != it["sha256"]:
            bad += 1
            problems.append({"path": rel, "kind": "mismatch", "bytes_now": size, "bytes_pinned": it["bytes"]})
        else:
            ok += 1
            total_bytes += size
    out[label] = {"ok": ok, "mismatch": bad, "missing": missing, "bytes_ok": total_bytes, "elapsed_s": round(time.perf_counter() - began, 3),
                  "problems": problems[:200], "problems_total": len(problems)}
    print(label, {k: v for k, v in out[label].items() if k != "problems"}, flush=True)


def main():
    run = Path(sys.argv[1])
    run.mkdir(parents=True, exist_ok=False)
    full_t032 = "--full-t032" in sys.argv
    out = {"schema": "T034-V1-v1", "started": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "root": str(ROOT), "full_t032": full_t032, "groups": {}}
    g = out["groups"]

    # A1. hai cây bổ sung
    mf = json.loads((SUP / "manifest-final.json").read_text(encoding="utf-8"))
    out["manifest_final"] = {"sha256": sha(SUP / "manifest-final.json"), "files": len(mf["files"])}
    check_list(mf["files"], "A1_supplement_manifest_final", g)

    # A2. gói đính chính
    mr = json.loads((SUP / "manifest-review-001.json").read_text(encoding="utf-8"))
    out["manifest_review"] = {"sha256": sha(SUP / "manifest-review-001.json"),
                              "pins_manifest_final_sha256": mr["scientific_output_immutable_manifest"]["sha256"],
                              "pins_manifest_final_match": mr["scientific_output_immutable_manifest"]["sha256"] == out["manifest_final"]["sha256"]}
    append_now = set(APPEND_ONLY)
    check_list([f for f in mr["files"] if f["path"] not in append_now], "A2_review_files", g)
    # Lượt v1-001 tính SPEC T-034 là kết quả bất biến nên báo FAIL: bản ghim trong source_pins là bản nháp 09/10 (17.068 byte),
    # còn bản đang dùng là SPEC đã duyệt 13/10. SPEC quy định tài liệu khung và SPEC ghim theo phiên bản đang dùng, không ép khớp
    # bản nháp cũ. Từ lượt v1-002: tài liệu khung có trong source_pins được báo riêng, không tính vào nhóm bất biến.
    frame_set = set(FRAME)
    check_list([f for f in mr["source_pins"] if f["path"] not in frame_set], "A2_review_source_pins", g)
    out["frame_docs_in_review_pins"] = []
    for f in mr["source_pins"]:
        if f["path"] in frame_set:
            p = ROOT / f["path"]
            out["frame_docs_in_review_pins"].append({"path": f["path"], "pinned_bytes": f["bytes"], "pinned_sha256": f["sha256"],
                                                     "bytes_now": p.stat().st_size, "sha256_now": sha(p),
                                                     "equal": sha(p) == f["sha256"]})

    # A3. kết quả cũ
    old = json.loads((SUP / "old-files-before.json").read_text(encoding="utf-8"))["files"]

    def sel_full(rel):
        return any(rel.startswith(p) for p in OLD_FULL)

    def sel_t032(rel):
        if not rel.startswith("results/T-032/"):
            return False
        return full_t032 or any(rel.startswith(p) for p in T032_USED_PREFIX)

    check_list(old, "A3_old_results_full_dirs", g, sel_full)
    check_list(old, "A3_old_T032_" + ("all" if full_t032 else "used_subset"), g, sel_t032)
    out["old_files_before"] = {"sha256": sha(SUP / "old-files-before.json"), "entries": len(old),
                               "T032_entries": sum(f["path"].replace(BS, "/").startswith("results/T-032/") for f in old)}

    # B. tài liệu chỉ nối: phần đầu khớp bản chứng nhận mới nhất có trong manifest
    cert = {}
    for f in old:
        if f["path"] in append_now:
            cert.setdefault(f["path"], []).append(("old-files-before.json", f["bytes"], f["sha256"]))
    for f in mf["controls"]:
        if f["path"] in append_now:
            cert.setdefault(f["path"], []).append(("manifest-final.json#/controls", f["bytes"], f["sha256"]))
    for key in ("files", "readonly_controls_unchanged", "before_controls"):
        for f in mr.get(key, []):
            if f["path"] in append_now:
                cert.setdefault(f["path"], []).append(("manifest-review-001.json#/" + key, f["bytes"], f["sha256"]))
    out["append_only"] = {}
    for rel in APPEND_ONLY:
        p = ROOT / rel
        size = p.stat().st_size
        rows = []
        for source, n, h in sorted(set(cert.get(rel, [])), key=lambda z: z[1]):
            rows.append({"certificate": source, "bytes": n, "prefix_ok": size >= n and sha(p, n) == h})
        latest = max((r for r in rows if r["prefix_ok"]), key=lambda r: r["bytes"], default=None)
        tail = b""
        if latest:
            with open(p, "rb") as f:
                f.seek(latest["bytes"])
                tail = f.read()
        out["append_only"][rel] = {"bytes_now": size, "sha256_now": sha(p), "certificates": rows,
                                   "all_prefix_ok": all(r["prefix_ok"] for r in rows) and bool(rows),
                                   "appended_after_latest_bytes": len(tail),
                                   "appended_after_latest_text": tail.decode("utf-8", errors="replace")[:6000]}
        print("B", rel, size, [(r["bytes"], r["prefix_ok"]) for r in rows], "tail", len(tail), flush=True)

    # C. tài liệu khung và nguồn ngoài: ghim phiên bản đang dùng
    out["frame"] = {}
    for rel in FRAME:
        p = ROOT / rel
        out["frame"][rel] = {"bytes": p.stat().st_size, "sha256": sha(p)}
    out["external"] = {k: {"path": str(p), "bytes": p.stat().st_size, "sha256": sha(p)} for k, p in EXTERNAL.items()}
    for name, repo in (("repo_HEAD", ROOT), ("flash_ticket_platform_HEAD", "D:/Project/flash-ticket-platform"), ("baro_HEAD", "D:/RCA-ext/src/baro")):
        r = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True)
        out[name] = r.stdout.strip()
    # nhắc: STATE không phải file chỉ nối; so với chứng nhận 13/10 chỉ để biết đã đổi
    state_cert = [f for f in mr["readonly_controls_unchanged"] if f["path"] == "docs/STATE.md"][0]
    out["state_vs_review_certificate"] = {"certificate_sha256": state_cert["sha256"], "equal": out["frame"]["docs/STATE.md"]["sha256"] == state_cert["sha256"]}
    agents_cert = [f for f in mr["readonly_controls_unchanged"] if f["path"] == "AGENTS.md"][0]
    out["agents_vs_review_certificate"] = {"equal": out["frame"]["AGENTS.md"]["sha256"] == agents_cert["sha256"]}

    bad = sum(v["mismatch"] + v["missing"] for v in g.values())
    prefix_bad = [k for k, v in out["append_only"].items() if not v["all_prefix_ok"]]
    out["status"] = "PASS" if bad == 0 and not prefix_bad and out["manifest_review"]["pins_manifest_final_match"] else "FAIL"
    out["immutable_problems"] = bad
    out["prefix_problems"] = prefix_bad
    out["finished"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    (run / "v1.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("STATUS", out["status"], "immutable_problems", bad, "prefix_problems", prefix_bad, flush=True)


if __name__ == "__main__":
    main()
