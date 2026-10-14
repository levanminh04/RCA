"""T-032 TORAI B, phép đổi nguồn log: kiểm seed 1 và 2 (bổ sung của thiet-ke-phep-doi-006.md, mục 8). Chạy trên EC2.

Bước RCD dùng seed và chỉ quyết định thứ tự trong cụm nhiều dịch vụ mà RCD trả đủ (nhánh 'rcd'). Chọn không dùng nhãn: mọi cặp
(ca, nhánh tl2/tl1) mà ở seed 0 có ít nhất một khối do nhánh 'rcd' xếp. Với mỗi cặp, chạy lại bước TORAI bằng worker native trên
đúng các bảng seed 0 đã tạo, với seed 1 và seed 2. Nhãn chỉ nối khi tổng hợp.
Dùng: python3 torai_log_contrast_seeds_v2.py <thư mục lượt mới>
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HOME = Path.home()
T031 = HOME / "rca/T-031"
BASE = HOME / "rca/T-032"
SOURCE = BASE / "runs/torai-log-contrast-001"
LABELS = BASE / "repo/results/T-028/runs/phan-hoi-review-001/ca-sai.json"
PY38 = str(T031 / "envs/py38/bin/python")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def ranks(result):
    out, offset = {}, 0
    for block in result.get("blocks") or []:
        for group in block["groups"]:
            for entity in group:
                out[entity] = (offset + 1, offset + len(group))
            offset += len(group)
    return out


def main():
    out = Path(sys.argv[1]).resolve()
    out.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": os.pathsep.join([str(T031 / "src/RCAEval"), str(T031 / "repo/src")]),
                "PYTHONIOENCODING": "utf-8", "PYTHONHASHSEED": "0"})
    labels = {r["opaque_id"]: r for r in read(LABELS)["main_rows"] if r["dataset"] == "RE2-TT" and r["method"] == "torai_B"}
    rows = []
    for case_dir in sorted((SOURCE / "cases").iterdir()):
        for branch in ("tl2", "tl1"):
            base = read(case_dir / branch / "ket-qua.json")["ket_qua"]
            # v2: phần còn thiếu của lượt 001. Chọn các cặp mà ở seed 0 root nằm trong một cụm NHIỀU dịch vụ (seed có thể đổi nhánh
            # xếp trong cụm), trừ các cặp đã chạy ở lượt 001 (có khối 'rcd'). Việc chọn này dùng nhãn root, chỉ để quyết chạy thêm seed nào.
            root_ = labels[case_dir.name]["root"]
            multi = any(root_ in [s for g in blk["groups"] for s in g] and sum(len(g) for g in blk["groups"]) > 1 for blk in base["blocks"])
            if not multi or "rcd" in base["extra"]["nhanh_khoi"]:
                continue
            job0 = read(case_dir / branch / "job.json")
            per_seed = {0: base}
            for seed in (1, 2):
                directory = out / "runs" / case_dir.name / (branch + "-s" + str(seed))
                directory.mkdir(parents=True)
                job = {"kind": "torai_run", "work_dir": job0["work_dir"], "t": job0["t"], "seed": seed}
                (directory / "job.json").write_text(json.dumps(job, ensure_ascii=False, indent=1), encoding="utf-8")
                with (directory / "stdout.txt").open("w") as so, (directory / "stderr.txt").open("w") as se:
                    done = subprocess.run([PY38, "-B", "-W", "ignore", "-m", "p3.worker", str(directory / "job.json"), str(directory / "ket-qua.json")],
                                          cwd=str(T031 / "repo"), env=env, stdin=subprocess.DEVNULL, stdout=so, stderr=se, timeout=3600)
                per_seed[seed] = read(directory / "ket-qua.json")["ket_qua"] if done.returncode == 0 else {"status": "RUN_FAILED", "blocks": []}
            # --- nối nhãn ---
            root = labels[case_dir.name]["root"]
            item = {"opaque_id": case_dir.name, "branch": branch, "cell": labels[case_dir.name]["cell"], "seeds": {}}
            for seed, result in per_seed.items():
                rank = ranks(result)
                position = next((i for i, b in enumerate(result.get("blocks") or []) if any(root in g for g in b["groups"])), None)
                item["seeds"][str(seed)] = {"status": result.get("status"), "root_rank": list(rank[root]) if root in rank else None,
                                            "root_block": position,
                                            "root_block_branch": result["extra"]["nhanh_khoi"][position] if position is not None else None,
                                            "branches": result.get("extra", {}).get("nhanh_khoi")}
            item["root_rank_same_across_seeds"] = len({json.dumps(v["root_rank"]) for v in item["seeds"].values()}) == 1
            item["root_in_rcd_block_at_seed0"] = item["seeds"]["0"]["root_block_branch"] == "rcd"
            rows.append(item)
            print(case_dir.name, branch, {s: v["root_rank"] for s, v in item["seeds"].items()}, item["root_in_rcd_block_at_seed0"], flush=True)
    summary = {"pairs_checked": len(rows), "root_rank_same_across_seeds": sum(r["root_rank_same_across_seeds"] for r in rows),
               "pairs_root_in_rcd_block_at_seed0": sum(r["root_in_rcd_block_at_seed0"] for r in rows),
               "pairs_root_in_rcd_block_same_rank": sum(r["root_in_rcd_block_at_seed0"] and r["root_rank_same_across_seeds"] for r in rows),
               "differing": [r for r in rows if not r["root_rank_same_across_seeds"]],
               "at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    (out / "summary.json").write_text(json.dumps({"schema": "T032-TORAI-log-contrast-seeds-v2", "summary": summary, "rows": rows}, ensure_ascii=False, indent=1) + "\n",
                                      encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "differing"}, ensure_ascii=False))
    print("differing:", [(r["opaque_id"], r["branch"], {s: v["root_rank"] for s, v in r["seeds"].items()}) for r in summary["differing"]])
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
