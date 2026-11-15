"""L1 SSH transport. No credentials in command arguments or retained stdout."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
SSH = 'C:/Program Files/Git/usr/bin/ssh.exe'
TARGETS = {
    'app': ('129.221.208.47', 'D:/RCA-ext/keys/exp-app/ssh-key-2026-11-10 (1).key', 'D:/RCA-ext/overnight-T058/out/known_hosts'),
    'tai': ('3.24.8.49', 'D:/RCA-ext/keys/Hahaa123.pem', 'D:/RCA-ext/keys/known_hosts'),
    'obs': ('213.35.116.128', 'D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key', 'D:/RCA-ext/overnight-T058/out/known_hosts'),
}

def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def command(machine):
    host, key, known = TARGETS[machine]
    return [SSH, '-i', key, '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=15', '-o',
            'StrictHostKeyChecking=yes', '-o', 'UserKnownHostsFile=' + known, 'ubuntu@' + host]

def remote(machine, source, mutation=False):
    if Path('D:/RCA-overnight/STOP').exists():
        raise RuntimeError('STOP exists')
    if mutation and machine == 'obs':
        raise RuntimeError('exp-obs read only')
    if mutation:
        with (ROOT / 'thay-doi-may.md').open('a', encoding='utf-8') as out:
            out.write(f'\n## {utc()} — {machine}\n\n```sh\n{source}\n```\n')
    result = subprocess.run(command(machine) + ['bash -s'], input=source.encode(), capture_output=True)
    if mutation:
        with (ROOT / 'thay-doi-may.md').open('a', encoding='utf-8') as out:
            out.write(f'\nExit: {result.returncode}.\n')
    return result

def main():
    p = argparse.ArgumentParser()
    p.add_argument('machine', choices=TARGETS)
    p.add_argument('script', type=Path)
    p.add_argument('--mutation', action='store_true')
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    source = a.script.read_text(encoding='utf-8-sig')
    result = remote(a.machine, source, a.mutation)
    if a.output:
        a.output.write_bytes(result.stdout)
    else:
        print(result.stdout.decode('utf-8', errors='replace'), end='')
    if result.stderr:
        print(result.stderr.decode('utf-8', errors='replace'), end='')
    raise SystemExit(result.returncode)

if __name__ == '__main__':
    main()
