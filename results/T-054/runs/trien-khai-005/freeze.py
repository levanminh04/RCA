"""Đóng gói ứng viên hiện hành, không tự khóa G3."""
from pathlib import Path
import sys,json,tarfile,shutil
ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'results/T-054';RUN=Path(__file__).resolve().parent
sys.path.insert(0,str(OUT/'scripts'))
from bien_nhan import *
def pin(path):
    p=ref(path);p['path']=Path(path).resolve().relative_to(ROOT).as_posix();return p
keys=set(read_pin(ref(OUT/'runs/freeze-cong-cu-006/files.json'))['files'])
keys.update(['results/T-052/ke-hoach-tap-test.json',
 'results/T-054/runs/trien-khai-005/materialize_main.py',
 'results/T-054/runs/trien-khai-005/dispatch-contract-005-freeze-candidate.json',
 'results/T-054/runs/trien-khai-005/placement-005.json',
 'results/T-054/runs/trien-khai-005/failure-policy-g3-005.json',
 'results/T-054/runs/trien-khai-005/code-evidence/tracerca.py'])
keys.update(read_pin(ref(OUT/'protocol.json'))['source_code'])
freeze=OUT/'runs/freeze-cong-cu-007';freeze.mkdir(exist_ok=False)
files={}
for rel in sorted(keys):
    src=ROOT/rel;dst=freeze/'code'/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);files[rel]=pin(src)
atomic(freeze/'files.json',dict(files=files,scope='Code and public metadata only; no telemetry/labels/private map; candidate not locked'))
with tarfile.open(freeze/'code.tar.gz','w:gz')as t:
    for rel in sorted(files):t.add(freeze/'code'/rel,arcname=rel,recursive=False)
atomic(freeze/'package.json',dict(G3=False,test_opened=False,main_started=False,files=pin(freeze/'files.json'),archive=pin(freeze/'code.tar.gz'),
    source_code_unchanged_legacy=93,own_scripts=9,runtime_compiler=1,
    note='Final tool code differs from actual DEV package retained005; Linux r2 tested same9script bytes. Freeze007 becomes historical after explicit G3 protocol/plan grants; no silent mutation.'))
print(json.dumps({'freeze':str(freeze),'files':len(files),'G3':False}))
