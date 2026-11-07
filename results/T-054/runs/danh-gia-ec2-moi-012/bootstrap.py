"""Build an isolated Python 3.12 environment for TT dev and synthetic checks."""
import hashlib
import importlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
from urllib.request import urlopen
import zipfile

root = Path("/home/ubuntu/rca-p7/T-054/checkpoint012")
root.mkdir(parents=True, exist_ok=False)
uv_version = "0.12.22"
requirements = (
    "numpy==1.26.4 pandas==2.2.3 scipy==1.14.1 pyarrow==18.1.0 psutil==6.1.1 "
    "scikit-learn==1.6.0 joblib==1.2.0 threadpoolctl==3.1.0 networkx==2.8.8 "
    "drain3==0.9.11 cachetools==4.2.1 jsonpickle==1.5.1 python-dateutil==2.8.2 "
    "pytz==2023.3 tzdata==2023.3 six==1.17.0 setuptools==75.6.0"
).split()
for name in ("cache", "tmp", "python", "envs", "tools"):
    (root / name).mkdir()

env = dict(os.environ,
           XDG_CACHE_HOME=str(root / "cache"), UV_CACHE_DIR=str(root / "cache/uv"),
           TMPDIR=str(root / "tmp"), UV_PYTHON_INSTALL_DIR=str(root / "python"),
           UV_PYTHON_BIN_DIR=str(root / "tools"), PYTHONDONTWRITEBYTECODE="1",
           PYTHONHASHSEED="0", OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1")
started = time.monotonic()
uv = root / "tools/uv"
logs = []

def run(args, timeout=720):
    tick = time.monotonic()
    proc = subprocess.run([str(a) for a in args], env=env, text=True, capture_output=True, timeout=timeout)
    record = {"args": [str(a) for a in args], "exit": proc.returncode, "stdout": proc.stdout,
              "stderr": proc.stderr, "seconds": time.monotonic() - tick}
    logs.append(record)
    print(json.dumps({"stage": str(args[1]), "exit": proc.returncode, "seconds": record["seconds"]}), flush=True)
    if proc.returncode != 0:
        raise RuntimeError(str(args[1]) + " failed; see bootstrap.json")
    return proc.stdout

try:
    with urlopen(f"https://pypi.org/pypi/uv/{uv_version}/json", timeout=45) as response:
        metadata = json.load(response)
    wheels = [item for item in metadata["urls"] if "manylinux" in item["filename"]
              and item["filename"].endswith("x86_64.whl")]
    assert len(wheels) == 1, [item["filename"] for item in wheels]
    wheel = wheels[0]
    with urlopen(wheel["url"], timeout=90) as response:
        data = response.read(64 * 1024 * 1024 + 1)
    assert len(data) == wheel["size"] and hashlib.sha256(data).hexdigest() == wheel["digests"]["sha256"]
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        members = [name for name in archive.namelist() if name.endswith(".data/scripts/uv")]
        assert len(members) == 1, members
        uv.write_bytes(archive.read(members[0]))
        uv.chmod(0o755)
    run([uv, "--version"])
    run([uv, "python", "install", "3.12.3", "--no-cache"])
    run([uv, "venv", "--python", "3.12.3", "--no-python-downloads", root / "envs/main"])
    exe = root / "envs/main/bin/python"
    run([uv, "pip", "install", "--no-cache", "--python", exe, *requirements])
    run([uv, "pip", "check", "--python", exe])
    packages = run([uv, "pip", "freeze", "--python", exe])
    import_check = "import sys,numpy,pandas,scipy,pyarrow,psutil,sklearn,networkx,drain3; print(sys.version); print(sys.executable)"
    python = run([exe, "-B", "-c", import_check])
    summary = {"PASS": True, "python": python, "requirements": requirements, "packages": packages,
               "uv_wheel": {"filename": wheel["filename"], "sha256": wheel["digests"]["sha256"], "bytes": wheel["size"]},
               "uv_sha256": hashlib.sha256(uv.read_bytes()).hexdigest()}
except BaseException as error:
    summary = {"PASS": False, "error": repr(error)}
summary.update(logs=logs, disk_free=shutil.disk_usage(root).free, elapsed_s=time.monotonic()-started)
(root / "bootstrap.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps(summary), flush=True)
if not summary["PASS"]:
    raise SystemExit(1)
