"""T-032: chép trung gian J0 của MicroRank (lượt laptop đã khớp tuyệt đối) lên EC2 để tính bảng lõi, A′ và C1.

Chạy trên laptop, chỉ đọc lượt cohort. Mỗi ca OK chép ba file của nhánh observed:
native-result.json, native-after.parquet, calls/001-microrank.json. Ca nguồn ERROR chỉ ghi dòng trạng thái.
Không tạo bản sao trung gian trên laptop: ghi thẳng một luồng tar qua ssh. Hash từng file được ghi vào manifest
và kiểm lại trên EC2 sau khi chép.
Dùng: py -3 -B transfer_microrank_j0_v1.py <thư mục biên nhận mới> <thư mục đích trên EC2>
"""
import hashlib
import io
import json
import subprocess
import sys
import tarfile
import time
from pathlib import Path

REPO = Path("D:/RCA-flashticket")
TASK = REPO / "results/T-032"
COHORT = TASK / "runs/microrank-laptop-cohort-001"
DIAGNOSTIC = TASK / "runs/microrank-laptop-diagnostic-001"
KEY = "D:/RCA-ext/keys/key2.pem"
HOST = "ubuntu@3.26.62.217"
FILES = {"native-result.json": "native-result.json", "native-after.parquet": "native-after.parquet",
         "001-microrank.json": "calls/001-microrank.json"}


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def main():
    receipt, remote = Path(sys.argv[1]), sys.argv[2]
    assert remote.startswith("/home/ubuntu/rca/T-032/inputs/") and " " not in remote
    receipt.mkdir(parents=True, exist_ok=False)
    cases, members = [], []
    for row in read(COHORT / "plan-52.json")["rows"]:
        dataset, opaque_id = row["dataset"], row["opaque_id"]
        retrospective = (dataset, opaque_id) == ("RE2-TT", "dev-3defe3d34b")
        closed = (COHORT / "retrospective-dev-3defe3d34b" if retrospective else COHORT / "cases" / dataset / opaque_id) / "closed.json"
        entry = {"dataset": dataset, "opaque_id": opaque_id, "source_status": row["source_status"],
                 "frozen_sha256": row["source_sha256"], "closed_case": closed.is_file(),
                 "closed_sha256": sha(closed) if closed.is_file() else None, "files": {}}
        if closed.is_file() and row["source_status"] == "OK":
            capture = (DIAGNOSTIC if retrospective else COHORT / "cases" / dataset / opaque_id) / "observed/capture"
            for name, relative in FILES.items():
                path = capture / relative
                entry["files"][name] = sha(path)
                members.append((dataset + "/" + opaque_id + "/" + name, path))
        cases.append(entry)
    manifest = {"schema": "T032-microrank-j0-transfer-v1", "at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "source": "nhánh observed của lượt laptop khớp tuyệt đối (Q-124, Q-126)", "remote": remote, "cases": cases,
                "counts": {"cases": len(cases), "closed": sum(c["closed_case"] for c in cases),
                           "with_files": sum(bool(c["files"]) for c in cases), "files": len(members),
                           "bytes": sum(path.stat().st_size for _name, path in members)}}
    text = json.dumps(manifest, ensure_ascii=False, indent=1) + "\n"
    (receipt / "manifest.json").write_text(text, encoding="utf-8", newline="\n")
    started = time.perf_counter()
    ssh = subprocess.Popen(["ssh", "-i", KEY, "-o", "BatchMode=yes", HOST,
                            "test ! -e " + remote + " && mkdir -p " + remote + " && tar xf - -C " + remote],
                           stdin=subprocess.PIPE)
    with tarfile.open(fileobj=ssh.stdin, mode="w|") as archive:
        data = text.encode("utf-8")
        info = tarfile.TarInfo("manifest.json")
        info.size = len(data)
        archive.addfile(info, io.BytesIO(data))
        for name, path in members:
            archive.add(str(path), arcname=name)
    ssh.stdin.close()
    code = ssh.wait()
    check = subprocess.run(["ssh", "-i", KEY, "-o", "BatchMode=yes", HOST, "python3 - " + remote], input=(
        "import hashlib,json,sys,os\n"
        "root=sys.argv[1]; m=json.load(open(root+'/manifest.json'))\n"
        "bad=[c['dataset']+'/'+c['opaque_id']+'/'+n for c in m['cases'] for n,d in c['files'].items()\n"
        "     if hashlib.sha256(open(root+'/'+c['dataset']+'/'+c['opaque_id']+'/'+n,'rb').read()).hexdigest()!=d]\n"
        "print(json.dumps({'manifest_sha256':hashlib.sha256(open(root+'/manifest.json','rb').read()).hexdigest(),\n"
        "  'files_checked':sum(len(c['files']) for c in m['cases']),'mismatches':bad}))\n"), capture_output=True, text=True)
    remote_check = json.loads(check.stdout) if check.returncode == 0 and check.stdout.strip() else {"error": check.stderr[-500:]}
    result = {"tar_exit_code": code, "transfer_s": time.perf_counter() - started, "local_manifest_sha256": sha(receipt / "manifest.json"),
              "remote_check": remote_check, "counts": manifest["counts"],
              "pass": code == 0 and remote_check.get("mismatches") == [] and
                      remote_check.get("manifest_sha256") == sha(receipt / "manifest.json")}
    (receipt / "transfer-check.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
