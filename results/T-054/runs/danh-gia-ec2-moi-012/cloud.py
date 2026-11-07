"""Run one already approved checkpoint012 stage on both new EC2s."""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path, PurePosixPath
import shlex
import subprocess
import tarfile
import time

RUN = Path(__file__).resolve().parent
REMOTE = "/home/ubuntu/rca-p7/T-054/checkpoint012"
HOSTS = (
    ("ec2-large-disk", "16.176.181.251", "D:/RCA-ext/keys/key4.pem"),
    ("ec2-small-disk", "13.236.44.106", "D:/RCA-ext/keys/key3.pem"),
)

def ssh(host, command, *, payload=None, timeout=120):
    name, ip, key = host
    args = ["ssh", "-i", key, "-o", "BatchMode=yes", "-o", "IdentitiesOnly=yes",
            "-o", "StrictHostKeyChecking=yes", "-o", "UpdateHostKeys=no",
            "-o", "UserKnownHostsFile=C:/Users/84583/.ssh/known_hosts",
            "-o", "ConnectTimeout=12", "-o", "ServerAliveInterval=15",
            "-o", "ServerAliveCountMax=3", "ubuntu@" + ip, command]
    started = time.monotonic()
    proc = subprocess.run(args, input=payload, capture_output=True, timeout=timeout)
    return {"host": name, "ip": ip, "exit": proc.returncode,
            "seconds": time.monotonic()-started}, proc.stdout, proc.stderr

def bootstrap(host):
    result, stdout, stderr = ssh(host, "python3 -B -", payload=(RUN / "bootstrap.py").read_bytes(), timeout=1500)
    result.update(stdout=stdout.decode("utf-8", errors="replace"), stderr=stderr.decode("utf-8", errors="replace"))
    with (RUN / f"{host[0]}-bootstrap.json").open("x", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(host[0], "bootstrap", result["exit"], f"{result['seconds']:.2f}s", flush=True)
    if result["exit"] != 0:
        print(result["stderr"], result["stdout"][-2500:], flush=True)
    return result["exit"]

def save_attempt(path, result, stdout, stderr):
    result.update(stdout=stdout.decode("utf-8", errors="replace"), stderr=stderr.decode("utf-8", errors="replace"))
    with path.open("x", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(path.name, "exit", result["exit"], f"{result['seconds']:.2f}s", flush=True)
    if result["exit"] != 0:
        print(result["stderr"][-1800:], result["stdout"][-2200:], flush=True)

def pilot(host):
    name = host[0]
    package = RUN / "dev-and-code.tar.gz"
    manifest = json.loads((RUN / "package.json").read_bytes())
    sha = manifest["archive"]["sha256"]
    data = package.read_bytes()
    assert len(data) == manifest["archive"]["bytes"] and hashlib.sha256(data).hexdigest() == sha
    stage = """
import hashlib,json,sys,tarfile
from pathlib import Path,PurePosixPath
r=Path('/home/ubuntu/rca-p7/T-054/checkpoint012')
archive=r/'dev-and-code.tar.gz'
with archive.open('xb') as f: f.write(sys.stdin.buffer.read())
assert hashlib.sha256(archive.read_bytes()).hexdigest()==EXPECTED
work=r/'work'; work.mkdir(exist_ok=False)
with tarfile.open(archive) as tar:
 for m in tar.getmembers():
  p=PurePosixPath(m.name)
  assert m.isfile() and not p.is_absolute() and '..' not in p.parts
 tar.extractall(work,filter='data')
pins=json.loads((work/'files.json').read_bytes())
for path,pin in pins.items():
 data=(work/path).read_bytes()
 assert len(data)==pin['bytes'] and hashlib.sha256(data).hexdigest()==pin['sha256'],path
print(json.dumps({'verified_files':len(pins),'archive_sha256':EXPECTED}))
""".replace("EXPECTED", repr(sha))
    result, stdout, stderr = ssh(host, "python3 -B -c " + shlex.quote(stage), payload=data, timeout=180)
    save_attempt(RUN / f"{name}-stage.json", result, stdout, stderr)
    if result["exit"] != 0:
        return result["exit"]
    dependency = (
        "cd " + REMOTE + " && XDG_CACHE_HOME=" + REMOTE + "/cache TMPDIR=" + REMOTE
        + "/tmp UV_CACHE_DIR=" + REMOTE + "/cache/uv ./tools/uv pip install --no-cache"
        + " --python ./envs/main/bin/python pytest==8.3.5"
    )
    result, stdout, stderr = ssh(host, dependency, timeout=180)
    save_attempt(RUN / f"{name}-fixture-dependencies.json", result, stdout, stderr)
    if result["exit"] != 0:
        return result["exit"]
    command = (
        "cd " + REMOTE + "/work && OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1"
        + " PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 " + REMOTE
        + "/envs/main/bin/python -B results/T-054/runs/checkpoint012-tools/remote_checks.py " + name
    )
    result, stdout, stderr = ssh(host, command, timeout=1450)
    save_attempt(RUN / f"{name}-pilot.json", result, stdout, stderr)
    pilot_exit = result["exit"]
    archive_root = "results/T-054/runs/checkpoint012-results"
    transfer, stdout, stderr = ssh(host, "tar -C " + REMOTE + "/work -czf - " + archive_root, timeout=240)
    transfer.update(bytes=len(stdout), sha256=hashlib.sha256(stdout).hexdigest(),
                    stderr=stderr.decode("utf-8", errors="replace"))
    with (RUN / f"{name}-receive.json").open("x", encoding="utf-8") as f:
        json.dump(transfer, f, indent=2)
    if transfer["exit"] != 0:
        print(transfer["stderr"], flush=True)
        return transfer["exit"]
    path = RUN / f"{name}-received.tar.gz"
    with path.open("xb") as f:
        f.write(stdout)
    received = RUN / "received" / name
    received.mkdir(parents=True, exist_ok=False)
    with tarfile.open(path) as tar:
        for item in tar.getmembers():
            rel = PurePosixPath(item.name)
            assert rel.is_relative_to(archive_root) and ".." not in rel.parts and (item.isfile() or item.isdir())
        tar.extractall(received, filter="data")
    print(name, "received", len(stdout), "bytes", flush=True)
    return pilot_exit

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["bootstrap", "pilot"])
    args = parser.parse_args()
    action = {"bootstrap": bootstrap, "pilot": pilot}[args.stage]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(action, HOSTS))
    return 0 if results == [0, 0] else 1

if __name__ == "__main__":
    raise SystemExit(main())
