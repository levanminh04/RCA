"""Chuyển gói và điều khiển lượt EC2 qua SSH đã ghim của T-049."""
import re
import tarfile
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent / "T-049/scripts"))
from may_chay import PY, SSH

REMOTE = "/home/ubuntu/rca-t049/results/T-050/ec2-stage-001"


def call(command, **kwargs):
    return subprocess.run([*SSH, command], check=True, timeout=120, **kwargs)


def main(action, run="ec2-001"):
    assert re.fullmatch(r"ec2-\d{3}", run)
    base = f"cd {REMOTE} && "
    folder = f"results/T-050/{run}"
    if action == "stage":
        with (OUT / "ec2-input-001.tar.gz").open("rb") as stream:
            call(f"mkdir -p {REMOTE.rsplit('/', 1)[0]} && mkdir {REMOTE} && "
                 f"tar -xzf - -C {REMOTE}", stdin=stream)
    elif action == "launch":
        cmd = (f"env PYTHONHASHSEED=0 OPENBLAS_NUM_THREADS=1 timeout --kill-after=15s "
               f'\"$remaining\" {PY} -Bu results/T-050/run_ec2.py dau-vao-003 {run}')
        call(base + f"mkdir -p {folder} && flock -n {folder}/launch.lock bash -c '"
             f"if test -s {folder}/pid && ps -p $(cat {folder}/pid) -o args= | grep -Fq run_ec2.py; then "
             f"echo existing-controller; exit 1; fi; "
             f"deadline=results/T-050/deadline; "
             f"test -s $deadline || echo $(( $(date +%s) + 6900 )) > $deadline; "
             f"remaining=$(( $(cat $deadline) - $(date +%s) )); "
             f"test $remaining -gt 0 || exit 1; "
             f"log={folder}/controller-$(date +%s%N).log; "
             f"nohup {cmd} </dev/null >$log 2>&1 & echo $! | tee {folder}/pid'")
    elif action == "status":
        call(base + f"if test -f {folder}/pid; then "
             f"ps -p $(cat {folder}/pid) -o pid,etime,args || true; "
             f"tail -n 25 $(ls -t {folder}/controller-*.log | head -1); "
             f"find {folder} -name complete.json | wc -l; fi")
    elif action == "receive":
        target = OUT / f"{run}-download"
        target.mkdir()
        archive = target / "run.tar.gz"
        with archive.open("xb") as stream:
            call(base + f"tar -czf - -C results/T-050 -- {run}", stdout=stream)
        with tarfile.open(archive, "r:gz") as stream:
            for member in stream:
                relative = Path(member.name)
                assert relative.parts[0] == run and ".." not in relative.parts
                assert member.isfile() or member.isdir()
                stream.extract(member, target, filter="data")
    else:
        raise ValueError(action)


if __name__ == "__main__":
    main(*sys.argv[1:])
