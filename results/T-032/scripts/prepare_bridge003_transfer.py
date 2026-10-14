"""Metadata-only transfer receipt for the user-approved bridge-003 scope."""
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PINS = {
    'check_microrank_t028_v3.py': '324807b59d7b6cbe5062915949b2bd958e0b3ad520cc7e8d1e7dcbff6568a144',
    'replay_microrank_approved_v3.py': 'd94b46873ed18f240222679240e6b7ee11ab067422c0ce4ca14c5bad12d615bb',
    'audit_microrank_posthoc_v3.py': '320a1675794ad2f058f25ed8a15439d10999d6c8fc4c7301a3c96d8870baa102',
    'batch_microrank_approved_v3.py': '4e815473b7e718710e4d1613ce95821447df67310a5c513c4077fbe5e4c60a2d',
}

def digest(blob):
    return hashlib.sha256(blob).hexdigest()

def main():
    files = []
    scripts = ROOT / 'results/T-032/scripts'
    for name, pin in PINS.items():
        blob = (scripts / name).read_bytes()
        if digest(blob) != pin:
            raise ValueError('v3 script pin mismatch: ' + name)
        ast.parse(blob.decode('utf-8-sig'))
        files.append({'path': str((scripts / name).relative_to(ROOT).as_posix()),
                      'remote_path': 'scripts/' + name, 'bytes': len(blob), 'sha256': pin,
                      'authority': 'approved bridge-003 implementation; root diff/AST review'})
    replacements = {
        'check_microrank_t028_v2.py': 'check_microrank_t028_v3.py',
        '2164a24ace9c55a80c6ebf85fc380e8cbcef277cf1e0a8ae51c6e337a41bceef': PINS['check_microrank_t028_v3.py'],
        'replay_microrank_approved_v2.py': 'replay_microrank_approved_v3.py',
        'e988952c402ba9f0a6ce52c1c79835594af68bebee99ba687d229ba6a9250be5': PINS['replay_microrank_approved_v3.py'],
    }
    for name in list(PINS)[1:]:
        before = (scripts / name.replace('_v3.py', '_v2.py')).read_text(encoding='utf-8-sig')
        after = (scripts / name).read_text(encoding='utf-8-sig')
        for old, new in replacements.items():
            before = before.replace(old, new)
        if before != after:
            raise ValueError('downstream change exceeds pin/filename: ' + name)
    mp = 'results/T-028/runs/phan-hoi-review-001/manifest.json'
    raw = (ROOT / mp).read_bytes()
    if digest(raw) != '9608215b6499359b9c4914678a31ce789378851bc6a496ea298b984eb3b23c6f':
        raise ValueError('T028 authority changed')
    manifest = json.loads(raw.decode('utf-8-sig'))
    entries = [x for x in manifest['final_scripts'] if x['path'].endswith('/tong_hop_bao_cao.py')]
    if len(entries) != 1:
        raise ValueError('snapshot cardinality')
    source = entries[0]
    blob = (ROOT / source['snapshot']).read_bytes()
    if digest(blob) != source['sha256']:
        raise ValueError('snapshot hash mismatch')
    files.append({'path': source['snapshot'], 'remote_path': 'repo/' + source['snapshot'],
                  'bytes': len(blob), 'sha256': source['sha256'],
                  'authority': mp + '#/final_scripts/*'})
    out = ROOT / 'results/T-032/runs/tiep-tuc-003/bridge003-transfer.json'
    with out.open('x', encoding='utf-8') as stream:
        json.dump({'status': 'PASS_LOCAL', 'methods_executed': False,
                   'downstream_pin_filename_only': True, 'files': files,
                   'new_bytes_to_transfer': sum(x['bytes'] for x in files)}, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({'status': 'PASS_LOCAL', 'files': len(files),
                      'bytes': sum(x['bytes'] for x in files), 'receipt_sha256': digest(out.read_bytes())}))

if __name__ == '__main__':
    main()
