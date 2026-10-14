"""T-034: manifest của toàn bộ `results/T-034/` và kiểm phạm vi ghi. Chỉ đọc, trừ file manifest của chính lượt.

- Băm mọi file dưới results/T-034/ (trừ thư mục lượt manifest đang ghi).
- Kiểm phạm vi: so `git status --porcelain` với danh sách đường dẫn có trước phiên (ảnh chụp đầu phiên ghi trong LOG) để chỉ ra
  đường dẫn nào do T-034 tạo hoặc sửa; mọi đường dẫn mới phải nằm trong phạm vi ghi của SPEC.

Dùng: python manifest_cuoi.py <thư mục lượt>
"""
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCOPE = ("results/T-034/", "tasks/T-034-g2-goi-trinh/LOG.md", "docs/STATE.md", "docs/WHY.md")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main():
    run = ROOT / sys.argv[1]
    run.mkdir(parents=True, exist_ok=False)
    base = ROOT / "results/T-034"
    files, total = [], 0
    for p in sorted(base.rglob("*")):
        if p.is_file() and run not in p.parents:
            size = p.stat().st_size
            total += size
            files.append({"path": str(p.relative_to(ROOT)).replace("\\", "/"), "bytes": size, "sha256": sha(p)})
    status = subprocess.run(["git", "-c", "core.quotepath=false", "status", "--porcelain", "--untracked-files=all", "--", "tasks/T-034-g2-goi-trinh", "docs", "AGENTS.md", "CLAUDE.md", "src", "tasks/_MAU"],
                            cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout.splitlines()
    t034_task = [line for line in status if "tasks/T-034-g2-goi-trinh" in line]
    out = {"schema": "T034-manifest-v1", "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "root": "results/T-034", "n_files": len(files), "bytes": total,
           "write_scope": list(SCOPE), "git_status_docs_tasks_src": status, "git_status_task_T034": t034_task, "files": files}
    (run / "manifest.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("files", len(files), "bytes", total)
    for line in status:
        print("  ", line)


if __name__ == "__main__":
    main()
