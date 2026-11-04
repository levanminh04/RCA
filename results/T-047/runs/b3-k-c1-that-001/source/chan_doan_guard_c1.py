"""Dò guard trên đường chưa có, có tạo cha đồng thời; không nạp dữ liệu/M1."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import chay_t047_v3 as driver
import adapter_t047 as ad


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--run', required=True)
    p.add_argument('--child', type=int)
    a = p.parse_args()
    out = Path(a.run).resolve()
    if a.child is not None:
        errors = []
        for i in range(256):
            target = out / 'race' / str(i) / 'cases' / f'probe-{a.child}'
            try:
                q = ad.duong_ra(target)
                q.mkdir(parents=True, exist_ok=False)
            except Exception as e:
                errors.append(dict(i=i, error=repr(e), path=str(target)))
        ad.ghi(out / f'child-{a.child}.json', dict(n=256, errors=errors))
        return
    ad.duong_ra(out).mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    jobs = []
    for i in range(3):
        stdout = (out / f'child-{i}.stdout').open('xb')
        stderr = (out / f'child-{i}.stderr').open('xb')
        proc = subprocess.Popen([sys.executable, '-B', __file__, '--run', str(out), '--child', str(i)],
                                cwd=ad.ROOT, stdout=stdout, stderr=stderr)
        jobs.append((proc, stdout, stderr))
    for proc, stdout, stderr in jobs:
        proc.wait()
        stdout.close(); stderr.close()
    results = [json.loads((out / f'child-{i}.json').read_text(encoding='utf-8')) for i in range(3)]
    result = dict(calls=768, errors=sum(len(x['errors']) for x in results),
                  exits=[x[0].returncode for x in jobs], seconds=time.monotonic()-start,
                  method_executed=False, labels_read=False, method_modules_imported=True,
                  inputs='đường con chưa có trong T047, tạo cha đồng thời')
    ad.ghi(out / 'summary.json', result)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
