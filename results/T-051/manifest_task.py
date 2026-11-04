"""Ghim hồ sơ T-051 và nguồn đã dùng theo phạm vi của phiên."""
import sys

from run_t11 import OUT, ROOT, digest, save


def entry(path):
    return {"sha256": digest(path), "bytes": path.stat().st_size}


def main(status):
    sources = (
        "docs/DECISIONS.md", "docs/WHY.md", "docs/STATE.md",
        "tasks/T-051-t11-t12-va-kb/SPEC.md", "tasks/T-051-t11-t12-va-kb/LOG.md",
        "results/T-043/manifest.json", "results/T-049/manifest.json",
        "results/T-049/runs/t6-001-seal.json", "results/T-050/manifest.json",
        "results/T-050/manifest-chay-lai-002.json", "results/T-053/manifest.json",
        "results/T-038/do-thi/thuc-the.json", "results/T-039/do-thi/thuc-the.json",
    )
    outputs = {p.relative_to(ROOT).as_posix(): entry(p)
               for p in sorted(OUT.rglob("*")) if p.is_file() and p.name != "manifest.json"}
    save(OUT / "manifest.json", {
        "status": status, "scope": "dev-a", "test_locked": True,
        "python": sys.version, "output_count": len(outputs), "outputs": outputs,
        "sources": {p: entry(ROOT / p) for p in sources}})
    print("PASS", len(outputs), "SHA256", digest(OUT / "manifest.json"))


if __name__ == "__main__":
    main(sys.argv[1])
