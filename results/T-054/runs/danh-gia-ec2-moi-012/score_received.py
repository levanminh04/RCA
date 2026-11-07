"""Reuse the received fixtures and run the existing synthetic evaluator on the laptop."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile

from pack import RUN, ROOT, T054, file_pin, read, require
sys.path.insert(0, str(T054 / "scripts"))
from bien_nhan import ref, verify_envelope

EXE = Path("D:/RCA-ext/envs/T-014-main/Scripts/python.exe")
HOSTS = ("ec2-large-disk", "ec2-small-disk")
OUTPUT = Path("results/T-054/runs/checkpoint012-results")

def validate_archive(path, target):
    files = 0
    with tarfile.open(path) as archive:
        for entry in archive.getmembers():
            if entry.isfile():
                archived = archive.extractfile(entry).read()
                assert archived == (target / entry.name).read_bytes(), entry.name
                files += 1
    return files

def main():
    exe_pin = read(T054 / "runs/hoan-thien-local-g3-011/local-runtime-environments.json")["main"]["snapshot"]["executable"]
    require(EXE, exe_pin)
    env = dict(os.environ, PYTHONHASHSEED="0", OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1",
               MKL_NUM_THREADS="1", PYTHONDONTWRITEBYTECODE="1")
    scores = {}
    for host in HOSTS:
        folder = RUN / "received" / host
        archive = RUN / (host + "-received.tar.gz")
        require(archive, read(RUN / (host + "-receive.json")))
        files = validate_archive(archive, folder)
        fixture = folder / OUTPUT / "fixture"
        checked = read(fixture / "summary.json")
        assert checked["PASS"] and checked["count"] == 92
        readers = sorted(fixture.glob("reader-*"))
        assert len(readers) == 16
        for case in readers:
            job = read(case / "job.json")
            invocation = read(case / "invocation.json")
            records = verify_envelope(read(case / "result.json"), invocation, job["slot"], invocation["token"])
            assert records[0]["status"] == "OK"
        dest = RUN / ("fixture-score-" + host)
        command = [str(EXE), "-X", "utf8", "-B", str(T054 / "scripts/fixtures.py"), str(dest),
                   "--reports-from", str(fixture)]
        process = subprocess.run(command, env=env, capture_output=True, text=True, encoding="utf-8", timeout=120)
        result = {"command": command, "exit": process.returncode, "stdout": process.stdout, "stderr": process.stderr,
                  "fixture_checks": checked["count"], "fixture_reader_envelopes": len(readers), "archive_files_exact": files}
        with (RUN / (host + "-fixture-score.json")).open("x", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        assert process.returncode == 0, (host, process.stderr)
        summary = read(dest / "summary.json")
        scores[host] = {"summary": summary, "a4": file_pin(dest / "report/a4.json"),
                        "tables": file_pin(dest / "report/tables.json")}
        print(host, "received", files, "exact files,", checked["count"], "checks,", summary["rows"], "report rows")
    first, second = (scores[h] for h in HOSTS)
    exact = {field: first[field] == second[field] for field in ("a4", "tables")}
    with (RUN / "fixture-score-parity.json").open("x", encoding="utf-8") as f:
        json.dump({"hosts": scores, "tables_byte_exact": exact}, f, indent=2)
    print("fixture score parity:", exact)
    assert all(exact.values())

if __name__ == "__main__":
    main()
