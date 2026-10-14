"""Q-120: small pinned public source snapshots; no deployment-version inference."""
from pathlib import Path
import hashlib
import json
import subprocess
import time
import urllib.request

ROOT = Path('D:/RCA-flashticket/results/T-032/runs/instrumentation-source-001')
REV = '94a01ba4c7c79e0c0b2c9da073ba081fcedc4bf1'
FILES = ('README.md', 'src/frontend/main.go', 'src/frontend/handlers.go',
         'src/frontend/rpc.go', 'src/frontend/go.mod',
         'src/checkoutservice/main.go', 'src/checkoutservice/go.mod',
         'src/shippingservice/main.go', 'src/shippingservice/go.mod')
LIMIT = 20 * 1024 * 1024

def main():
    ROOT.mkdir(parents=True, exist_ok=False)
    refs = subprocess.run(['git', 'ls-remote',
            'https://github.com/IntelligentDDS/Augmented-OnlineBoutique.git',
            'refs/heads/master'], text=True, capture_output=True, timeout=30, check=True)
    assert refs.stdout.split()[0] == REV, 'discovery head changed; do not select a new revision'
    (ROOT / 'ls-remote.txt').write_text(refs.stdout, encoding='utf-8')
    rows, total = [], 0
    for relative in FILES:
        url = f'https://raw.githubusercontent.com/IntelligentDDS/Augmented-OnlineBoutique/{REV}/{relative}'
        row = {'url': url, 'revision': REV, 'source_path': relative,
               'requested_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'T032-Q120-public-provenance'})
            with urllib.request.urlopen(request, timeout=30) as response:
                body = response.read(LIMIT - total + 1)
                assert len(body) + total <= LIMIT, 'announced 20 MiB download limit'
                row['response_status'] = response.status
            target = ROOT / 'Augmented-OnlineBoutique' / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('xb') as stream:
                stream.write(body)
            total += len(body)
            row.update(local_path=target.relative_to(ROOT).as_posix(), bytes=len(body),
                       sha256=hashlib.sha256(body).hexdigest(), status='SAVED_PINNED_SOURCE')
        except Exception as error:
            row.update(status='FETCH_FAILED', error_type=type(error).__name__, error=str(error))
        rows.append(row)
        # Receipt is append-only, including failed requests; no retry/overwriting.
        with (ROOT / 'requests.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(row, ensure_ascii=False) + '\n')
    result = {'status': 'PINNED_PUBLIC_SOURCE_ONLY_DEPLOYMENT_BINDING_OPEN',
              'authority': 'Q-120', 'revision': REV, 'downloaded_bytes': total,
              'deployment_revision_of_Nezha_dev': 'OPEN',
              'scientific_use': 'candidate code semantics only until dataset deployment binding established',
              'rows': rows, 'no_dataset_or_test_download': True}
    with (ROOT / 'source-manifest.json').open('x', encoding='utf-8') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
    print(json.dumps({k: result[k] for k in ('status', 'revision', 'downloaded_bytes')}))

if __name__ == '__main__':
    main()
