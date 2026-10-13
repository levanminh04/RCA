"""Snapshot vận hành/manifest đã hoàn tất; không đọc lại thuật toán/dataset."""
import hashlib
import json
import os
import argparse
import subprocess
from datetime import datetime,timezone
from pathlib import Path
import psutil
import shutil
H=Path(os.environ['T033_HOME']).resolve()
parser=argparse.ArgumentParser()
parser.add_argument('--name',default='checkpoint-session1-001')
args=parser.parse_args()
assert args.name.startswith('checkpoint-session1-') and '/' not in args.name and '\\' not in args.name
R=H/'runs'/args.name; R.mkdir(exist_ok=False)
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()
def load(p): return json.loads(p.read_text())
snapshot={'utc':datetime.now(timezone.utc).isoformat(),'task_complete':False,
          'statuses':{},'immutable_files':{},'completed_case_branches':[],
          'resources':{'new_bytes':sum(p.stat().st_size for p in H.rglob('*') if p.is_file()),
                       'ram_available_bytes':psutil.virtual_memory().available,
                       'disk_free_bytes':shutil.disk_usage(H).free},
          'ps':subprocess.check_output(['ps','-C','python','-o','pid,etime,rss,%cpu,args'],text=True),
          'scripts':{p.name:sha(p) for p in (H/'scripts').glob('*') if p.is_file()}}
for name in ['nsigma-first-001','nsigma-rest-001','bocpd-first-001','bocpd-first-002','bocpd-rest-001']:
    d=H/'runs'/name
    p=d/'status.json'
    if p.is_file(): snapshot['statuses'][name]=load(p)
    for p in d.glob('dev-*.json'):
        doc=load(p)
        if doc.get('status')=='PASS' and doc.get('npz',doc.get('output_npz')):
            arr=d/doc.get('npz',doc.get('output_npz'))
            assert sha(arr)==doc['sha256']
            snapshot['completed_case_branches'].append({'run':name,'record':p.name,'npz':arr.name,'sha256':doc['sha256']})
for dirname in ['preflight-002','nsigma-first-001','nsigma-rest-001','bocpd-first-001','bocpd-first-002','full-metadata-recheck-001']:
    for p in (H/'runs'/dirname).glob('*'):
        if p.is_file(): snapshot['immutable_files'][str(p.relative_to(H))]={'bytes':p.stat().st_size,'sha256':sha(p)}
snapshot['progress_tail']=(H/'trang-thai.txt').read_text().splitlines()[-30:]
(R/'snapshot.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2))
print(json.dumps({'status':'PASS','snapshot':str(R/'snapshot.json'),'completed_branches':len(snapshot['completed_case_branches']),'resources':snapshot['resources']}))
