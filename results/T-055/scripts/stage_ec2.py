"""Chạy trên EC2 (python3 hệ thống). Nhận stage-<host>.json qua stdin, tải đúng 3 parquet mỗi ca từ HF ở revision
đã ghim, kiểm sha256/bytes LFS, ghi thẳng vào locator mờ. Không ghi tên ca ra đĩa, không mở nội dung parquet.
In ra JSON biên nhận theo mã mờ."""
import hashlib
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

BASE = Path('/home/ubuntu/rca-p7/T-055/data-root')


def fetch(url, dest, size, sha, tries=4):
    for i in range(tries):
        tmp = dest.with_suffix(dest.suffix + '.part')
        try:
            h = hashlib.sha256(); n = 0
            req = urllib.request.Request(url, headers={'User-Agent': 'rca-research'})
            with urllib.request.urlopen(req, timeout=120) as r, open(tmp, 'wb') as f:
                for block in iter(lambda: r.read(1 << 20), b''):
                    f.write(block); h.update(block); n += len(block)
                f.flush(); os.fsync(f.fileno())
            if n != size or h.hexdigest() != sha:
                raise ValueError('hash/bytes khác LFS')
            os.replace(tmp, dest)
            return i + 1
        except Exception as exc:
            if tmp.exists():
                tmp.unlink()
            if i == tries - 1:
                raise RuntimeError(f'{dest.name}: {type(exc).__name__}')
            time.sleep(3 * (i + 1))


def main():
    plan = json.loads(sys.stdin.buffer.read())
    out = {'host': plan['host'], 'revision': plan['revision'], 'cases': {}, 'started': time.time()}
    for opaque, c in sorted(plan['cases'].items()):
        rec = {}
        for name, meta in sorted(c['files'].items()):
            dest = BASE / meta['path']
            assert dest.parent.name == opaque and '..' not in meta['path']
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                ok = dest.stat().st_size == meta['bytes'] and hashlib.sha256(dest.read_bytes()).hexdigest() == meta['sha256']
                if not ok:
                    raise SystemExit('file đã có nhưng khác pin: ' + meta['path'])
                rec[name] = {'bytes': meta['bytes'], 'sha256': meta['sha256'], 'attempts': 0}
                continue
            url = f"https://huggingface.co/datasets/{plan['repo']}/resolve/{plan['revision']}/{c['case']}/{name}"
            tries = fetch(url, dest, meta['bytes'], meta['sha256'])
            rec[name] = {'bytes': meta['bytes'], 'sha256': meta['sha256'], 'attempts': tries}
        out['cases'][opaque] = rec
    out['finished'] = time.time()
    print(json.dumps(out, sort_keys=True))


if __name__ == '__main__':
    main()
