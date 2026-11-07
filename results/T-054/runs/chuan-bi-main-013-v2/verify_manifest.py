"""Read-only verification. Never grants G3 or reads raw test payloads."""
import argparse
import hashlib
import json
from pathlib import Path

RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[3]


def digest(path):
    h=hashlib.sha256()
    with path.open('rb')as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--documents',action='store_true');args=parser.parse_args()
    manifest=json.loads((RUN/'manifest.json').read_bytes())
    bad=[];count=0
    for group in ['outputs']+(['reviewed_documents']if args.documents else []):
        for rel,meta in manifest[group].items():
            path=ROOT/rel;count+=1
            if not path.is_file()or path.stat().st_size!=meta['bytes']or digest(path)!=meta['sha256']:bad.append(rel)
    for rel,meta in manifest['local_external_code'].items():
        path=Path(rel);count+=1
        if not path.is_file()or path.stat().st_size!=meta['bytes']or digest(path)!=meta['sha256']:bad.append(rel)
    print(json.dumps(dict(PASS=not bad,checked=count,mismatches=bad,real_test_payloads_read=False)))
    if bad:raise SystemExit(1)


if __name__=='__main__':main()
