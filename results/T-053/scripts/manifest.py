"""Lập manifest kết quả T-053. Chạy khi các file được kê đã đóng."""
import argparse
import json
import subprocess
from pathlib import Path

from doi_chieu import ROOT, RUNS, read, sha


def entry(path):
    return dict(bytes=path.stat().st_size, sha256=sha(path))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("state")
    p.add_argument("out", type=Path)
    args = p.parse_args()
    base = RUNS.parent
    excluded = {args.out.resolve()}
    outputs = {f.relative_to(ROOT).as_posix(): entry(f)
               for f in sorted(base.rglob("*")) if f.is_file() and f.resolve() not in excluded}
    sources = ("AGENTS.md", "docs/KE-HOACH-SAU-T047.md", "docs/MRP.md", "docs/WHY.md",
               "docs/DECISIONS.md", "docs/LESSONS.md", "docs/review-prompt.md", "docs/reference/sources/DT18-de-tai-va-nhiem-vu.md",
               "docs/reference/sources/advisor-2026-09-23.md",
               "tasks/T-053-kiem-z-chay-lai-k/SPEC.md", "results/T-047/manifest.json",
               "results/T-048/manifest.json")
    doc = dict(status=args.state,
               revision=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
               declared_sources={s: entry(ROOT / s) for s in sources},
               transfer=read(base / "chuyen-ec2.json"), outputs=outputs,
               output_count=len(outputs), total_logical_bytes=sum(x['bytes'] for x in outputs.values()),
               canonical=dict(report='results/T-053/bao-cao.md', summary='results/T-053/tong-hop.json',
                   phase1_seal='results/T-053/runs/k-dong-pha1-001/seal.json',
                   scores='results/T-053/runs/k-cham-001/kq.json',
                   selector='results/T-053/runs/k-cham-001/khoi-k.json',
                   bootstrap='results/T-053/runs/bootstrap-ec2-001/do-ben.json',
                   metrics='results/T-053/chi-so-day-du.json',
                   mechanisms='results/T-053/phan-tich-cap-003.json',
                   final_checks='results/T-053/runs/kiem-cuoi-001.json'),
               preserved_attempts=dict(pilot_ec2_001='lỗi thiếu networkx',
                   controllers_001_002='remote kết thúc, SSH chờ; resume sau kiểm hash',
                   k_cham_001='chấm chính và độ nhạy hợp lệ; bootstrap dừng do đầy đĩa',
                   paired_001_002='chẩn đoán trước sửa, không dùng kết luận; giữ lossless'),
               decisions=dict(D24="E4+S1", T049="Minh quyết", test_and_G3="chưa mở"))
    with args.out.open("x", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
