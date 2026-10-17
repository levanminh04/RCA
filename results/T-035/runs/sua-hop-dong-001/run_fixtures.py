"""Phát lại đúng fixture đã có và oracle mới; mỗi attempt giữ riêng."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
PYTHON = 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('suite', choices=['legacy', 'oracle'])
    parser.add_argument('--attempt', default='001')
    args = parser.parse_args()
    receipt = BASE / f'{args.suite}-commands-{args.attempt}.json'
    assert not receipt.exists()
    rows = []
    for seed in range(3):
        suffix = f'seed{seed}-{args.attempt}'
        if args.suite == 'legacy':
            jobs = [
                (ROOT / 'results/T-035/fixture/check.py', f'sua-hop-dong-001/fixture-cu-{suffix}'),
                (BASE / 'legacy_messaging.py', f'fixture-messaging-{suffix}'),
                (BASE / 'legacy_missing.py', f'fixture-missing-{suffix}'),
            ]
        else:
            jobs = [(BASE / 'oracle_json.py', f'fixture-oracle-{suffix}')]
        for script, output in jobs:
            command = [PYTHON, '-X', 'utf8', '-B', str(script), output]
            start = time.perf_counter()
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8',
                                    env=dict(os.environ, PYTHONHASHSEED=str(seed), PYTHONUTF8='1'))
            row = {'utc': datetime.now(timezone.utc).isoformat(), 'command': command, 'seed': seed,
                   'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr,
                   'seconds': time.perf_counter() - start}
            rows.append(row)
            print(json.dumps({'suite': args.suite, 'seed': seed, 'output': output,
                              'returncode': result.returncode}), flush=True)
            if result.returncode:
                break
        if rows[-1]['returncode']:
            break
    value = {'commands': rows, 'pass': all(x['returncode'] == 0 for x in rows),
             'builder_sha256': hashlib.sha256((ROOT / 'src/do_thi/builder.py').read_bytes()).hexdigest()}
    with receipt.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
    raise SystemExit(0 if value['pass'] else 1)


if __name__ == '__main__':
    main()
