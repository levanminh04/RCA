"""Verify remote count/SHA/bytes, extract solely into T029 and check completed chain."""
import hashlib
import json
import shutil
import tarfile
from datetime import datetime
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parents[3]
RUN=ROOT/'results/T-029/runs/ec2-complete-002'
DEST=RUN/'artifacts'
LOG=ROOT/'tasks/T-029-p4-han-che-phat-hien/LOG.md'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
def audit(s):
    with LOG.open('a',encoding='utf-8') as f: f.write('\n- '+datetime.now().astimezone().isoformat()+' — Copy EC2: '+s+'\n')

audit('Lệnh có ghi: T014-main Python -B -W ignore verify_ec2_transfer.py; chỉ ghi ec2-complete-002/artifacts/transfer-check và LOG.')
try:
    expected=read(RUN/'export-check.json'); archive=RUN/'artifacts.tar.gz'
    assert archive.stat().st_size==expected['archive_bytes']
    assert sha(archive)==expected['archive_sha256'],'Archive SHA mismatch'
    assert not DEST.exists(),'Keep existing extraction; never overwrite'
    with tarfile.open(archive,'r:gz') as tar:
        members=tar.getmembers(); names=[m.name for m in members]
        assert len(names)==len(set(names))==expected['archive_members']
        for m in members:
            p=PurePosixPath(m.name)
            assert m.isfile() and not p.is_absolute() and '..' not in p.parts and '\\' not in m.name
        mdata=tar.extractfile('transfer-manifest.json').read()
        assert hashlib.sha256(mdata).hexdigest()==expected['manifest_sha256']
        manifest=json.loads(mdata)
        assert len(manifest['files'])==manifest['file_count']==expected['file_count']
        assert set(names)==set(manifest['files'])|{'transfer-manifest.json'}
        DEST.mkdir()
        for m in members:
            target=(DEST/m.name).resolve(); assert DEST.resolve() in target.parents
            target.parent.mkdir(parents=True,exist_ok=True)
            with tar.extractfile(m) as src,target.open('xb') as dst: shutil.copyfileobj(src,dst)
    checks={p:sha(DEST/p)==v['sha256'] and (DEST/p).stat().st_size==v['bytes'] for p,v in manifest['files'].items()}
    assert all(checks.values()),'Artifact SHA/bytes mismatch'
    assert len([p for p in DEST.rglob('*') if p.is_file()])==manifest['file_count']+1
    chain=DEST/'runs/chuoi-002'
    states={n:read(chain/(n+'.json')).get('status',read(chain/(n+'.json')).get('V1')) for n in ('guard','v3-check','wrapper50-check','v4-check','ket-thuc')}
    assert set(states.values())=={'PASS'},states
    final=read(DEST/'export-complete-002/final-v1.json'); assert final['status']=='PASS'
    i1=sorted((chain/'i1').glob('dev-*.json')); i2=sorted((chain/'i2').glob('dev-*.json'))
    assert len(i1)==len(i2)==30
    sources=sorted((DEST/'runs').glob('i3-*/source-tplus.json'))
    pairs=[(read(p)['opaque_id'],read(p)['detector']) for p in sources]
    assert len(pairs)==len(set(pairs))==60
    records=sorted(p for s in sources for p in s.parent.glob('luot/*/ban-ghi-*.json'))
    assert len(records)==360
    result={'status':'PASS','archive_sha256':sha(archive),'manifest_sha256':expected['manifest_sha256'],
            'remote_count':manifest['file_count'],'local_count':len(checks),'hash_bytes_matches':sum(checks.values()),
            'chain_checks':states,'final_V1':final['status'],'I1_cases':len(i1),'I2_cases':len(i2),'I3_pairs':len(pairs),'I3_records':len(records)}
    (RUN/'transfer-check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    audit('PASS: '+json.dumps(result)+'; Đã chép về và kiểm hash xong; EC2 có thể tắt. Minh tự tắt, agent không tắt máy.')
    print(json.dumps(result))
except BaseException as e:
    audit('DỪNG kiểm copy: '+type(e).__name__+': '+str(e)+'; giữ mọi tệp, không dùng artifact chưa kiểm.'); raise
