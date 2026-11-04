"""Nhận đúng các lượt T-053 đã đóng từ EC2, đối chiếu SHA-256 và byte."""
import argparse
import json
import re
import shlex
import shutil
import subprocess
import tarfile
from pathlib import Path

from doi_chieu import RUNS, sha

SSH = ["ssh", "-i", "D:/RCA-ext/keys/key2.pem", "-o", "HostKeyAlias=3.26.62.217",
       "-o", "StrictHostKeyChecking=yes", "ubuntu@3.107.156.186"]

REMOTE = """
import hashlib,json,pathlib,sys
root=pathlib.Path.home()/'rca-t053/results/T-053/runs'
rows={}
for prefix in sys.argv[1:]:
    for folder in sorted(root.iterdir()):
        if folder.name != prefix and not folder.name.startswith(prefix+'-'):
            continue
        for p in sorted(folder.rglob('*')):
            if p.is_file() and not p.is_symlink():
                with p.open('rb') as f:
                    rows[p.relative_to(root).as_posix()]={'bytes':p.stat().st_size,
                        'sha256':hashlib.file_digest(f,'sha256').hexdigest()}
print(json.dumps(rows))
"""


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("receipt", type=Path)
    p.add_argument("prefix", nargs="+")
    p.add_argument("--reserve-bytes", type=int, default=256*1024**2)
    args = p.parse_args()
    if any(not re.fullmatch(r"[A-Za-z0-9-]+", v) for v in args.prefix):
        raise ValueError("Tiền tố không hợp lệ")
    manifest = json.loads(subprocess.check_output(
        SSH + ["python3 -B - " + shlex.join(args.prefix)], input=REMOTE.encode()))
    if not manifest or any(not re.fullmatch(r"[A-Za-z0-9._/-]+", name) or
                           any(part in (".","..") for part in Path(name).parts) or name.startswith("/")
                           for name in manifest):
        raise ValueError("Manifest đầu gửi rỗng hoặc có đường dẫn ngoài phạm vi")
    expected = {name: row for name,row in manifest.items() if not (RUNS / name).is_file()}
    for name, row in manifest.items():
        path = RUNS / name
        if path.is_file() and (path.stat().st_size != row["bytes"] or sha(path) != row["sha256"]):
            raise ValueError(f"Bản hiện có khác đầu gửi: {name}")
    if args.reserve_bytes < 0:
        raise ValueError("Dư đĩa không thể âm")
    if sum(r["bytes"] for r in expected.values()) + args.reserve_bytes > shutil.disk_usage(RUNS).free:
        raise ValueError("Không đủ ổ để nhận lượt")
    with args.receipt.open("x", encoding="utf-8") as f:
        json.dump(dict(expected=manifest, transferred=list(expected)), f, ensure_ascii=False, indent=2)
    if expected:
        command = "cd ~/rca-t053/results/T-053/runs && tar --null -T - -cf -"
        with subprocess.Popen(SSH + [command], stdin=subprocess.PIPE, stdout=subprocess.PIPE) as remote:
            remote.stdin.write(b"".join(name.encode() + b"\0" for name in expected))
            remote.stdin.close()
            with tarfile.open(fileobj=remote.stdout, mode="r|") as archive:
                for member in archive:
                    if not member.isfile() or member.name not in expected:
                        raise ValueError(f"Thành viên tar ngoài manifest: {member.name}")
                    dest = RUNS / member.name
                    dest.parent.mkdir(exist_ok=True, parents=True)
                    with archive.extractfile(member) as source, dest.open("xb") as target:
                        shutil.copyfileobj(source, target)
            if remote.wait():
                raise RuntimeError("Lỗi truyền từ EC2")
    for name, row in manifest.items():
        path = RUNS / name
        if path.stat().st_size != row["bytes"] or sha(path) != row["sha256"]:
            raise ValueError(f"Lệch bản nhận: {name}")
    print(f"PASS {len(manifest)} files")


if __name__ == "__main__":
    main()
