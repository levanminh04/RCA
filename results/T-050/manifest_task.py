"""Đóng manifest T-050 sau báo cáo, gồm cả lượt kỹ thuật dở."""
import subprocess
from pathlib import Path

from replay import ROOT, digest
from seal import read, write

OUT = Path(__file__).resolve().parent


def inventory(paths):
    return {p.relative_to(ROOT).as_posix(): {"bytes": p.stat().st_size, "sha256": digest(p)}
            for p in sorted(paths)}


def main():
    target = OUT / "manifest.json"
    upstream = ("results/T-049/manifest.json", "results/T-049/runs/t6-001-seal.json",
                "results/T-043/manifest.json", "results/T-024/work/danh-sach-tep-cuoi.json",
                "results/T-026/runs/session-005/handoff-manifest.json")
    sources = ("AGENTS.md", "tasks/T-050-t9-va-t10/SPEC.md", "docs/MRP.md",
               "docs/WHY.md", "docs/DECISIONS.md", "docs/LESSONS.md",
               "docs/KE-HOACH-SAU-T047.md", "docs/reference/sources/DT18-de-tai-va-nhiem-vu.md",
               "docs/reference/sources/advisor-2026-09-23.md",
               "results/T-045/scripts/pha2_khoi_k.py", "results/T-047/scripts/luat_c_t047.py",
               "results/T-049/scripts/kiem_tai_su_dung.py",
               "results/T-049/scripts/chuan_bi.py", "results/T-049/scripts/may_chay.py")
    paths = [p for p in OUT.rglob("*") if p.is_file() and p != target]
    plan = read(OUT / "pilot-plan.json")
    for name, sha in plan["sources"].items():
        assert digest(ROOT / name) == sha, name
    write(target, {"schema": "T050-v1", "status": "cho_phan_bien", "scope": "dev-a",
                   "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                   "runtime": read(ROOT / "results/T-049/manifest.json")["runtime"],
                   "upstream": inventory(ROOT / name for name in upstream),
                   "sources": inventory(ROOT / name for name in sources),
                   "execution_sources": plan["sources"],
                   "labels_dev": inventory(ROOT / name for name in (
                       "results/T-022/nhan-dev.json", "results/T-026/nhan-dev.json")),
                   "phase1_seal": "results/T-050/pha1-001/seal.json",
                   "outputs": inventory(paths), "output_count": len(paths),
                   "mutable_governance": ["docs/STATE.md", "tasks/T-050-t9-va-t10/LOG.md"],
                   "test_locked": True})


if __name__ == "__main__":
    main()
