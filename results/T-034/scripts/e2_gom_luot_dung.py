"""T-034 E2: gom bốn chuỗi dùng để kết luận vào một thư mục lượt, chép nguyên file và kiểm mã băm.

PF lấy từ lượt e2-002, FF lấy từ lượt e2-003 (cùng script v3, cùng cấu hình luồng của nguồn); ví dụ nhỏ lấy từ
e2-fixtures-ec2-004-v3; phép kiểm tất định lấy từ e2-determinism-001. Không tính lại gì.

Dùng: python e2_gom_luot_dung.py results/T-034/runs/e2-used-001
"""
import hashlib
import json
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUNS = "results/T-034/runs/"
PLAN = [("out", RUNS + "e2-002/out", "dev-*--PF--*"), ("out", RUNS + "e2-003/out", "dev-*--FF--*"),
        ("fixtures-ec2", RUNS + "e2-fixtures-ec2-004-v3/out", "*"), ("determinism", RUNS + "e2-determinism-001/out", "*.json")]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    out = ROOT / sys.argv[1]
    out.mkdir(parents=True, exist_ok=False)
    files = []
    for sub, src_dir, pattern in PLAN:
        (out / sub).mkdir(exist_ok=True)
        for src in sorted((ROOT / src_dir).glob(pattern)):
            dst = out / sub / src.name
            shutil.copyfile(src, dst)
            a, b = sha(src), sha(dst)
            assert a == b, src
            files.append({"path": str(dst.relative_to(ROOT)).replace("\\", "/"), "from": str(src.relative_to(ROOT)).replace("\\", "/"), "sha256": a, "bytes": dst.stat().st_size})
    labels = sorted({f["path"].split("/")[-1].split("--summary")[0] for f in files if f["path"].endswith("--summary.json")})
    assert labels == ["dev-3ae0a6c15a--FF", "dev-3ae0a6c15a--PF", "dev-ba831dbeb8--FF", "dev-ba831dbeb8--PF"], labels
    manifest = {"schema": "T034-E2-used-run-v1", "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "note": "Bản gom chỉ chép file; lượt gốc giữ nguyên. PF: e2-002; FF: e2-003; cùng script e2_bocpd_log_v3.py và cấu hình luồng của nguồn.",
                "chains": labels, "files": files}
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("files", len(files), "chains", labels)


if __name__ == "__main__":
    main()
