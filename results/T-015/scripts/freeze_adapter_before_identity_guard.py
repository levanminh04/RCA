"""Recover the pre-guard adapter only if its bytes match the earlier inventory."""
import hashlib,json,pathlib
root=pathlib.Path(__file__).resolve().parents[3];out=root/'results/T-015/runs/source-versions'
data=(root/'src/microrank/__init__.py').read_bytes();newline=b'\r\n' if b'\r\n' in data else b'\n'
lines=[b'    # An exact repeat retains its occurrence, as in the original graph code.',b'    # A reused identity carrying different observations is ambiguous.',b'    identities=df[COLS].drop_duplicates()',b"    if identities.duplicated(['traceID','spanID']).any():raise ValueError('Conflicting observations for traceID/spanID')"]
block=newline.join(lines)+newline;assert data.count(block)==1
old=data.replace(block,b'');expected=json.loads((root/'results/T-015/runs/environment.json').read_text())['kernel_hashes']['src/microrank/__init__.py']
actual=hashlib.sha256(old).hexdigest();assert actual==expected,(actual,expected)
(out/'adapter-before-identity-guard.py').write_bytes(old)
(out/'adapter-recovery-proof.json').write_text(json.dumps({'matches_earlier_environment_inventory':True,'sha256':actual,'removed_only_identity_guard':True},indent=2))
print('PASS: recovered bytes match earlier inventory')
