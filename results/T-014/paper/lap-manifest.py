"""Chỉ đọc nguồn và ghi manifest của nhánh paper T-014; không chạy RCA."""
import csv
import hashlib
import json
from importlib import metadata
from pathlib import Path
import subprocess

out = Path(__file__).resolve().parent
repo = out.parents[2]
circa = Path('D:/RCA-ext/work/T-014/CIRCA')
rcaeval = Path('D:/RCA-ext/src/RCAEval')
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def revision(path):
    return subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD'], text=True).strip()
files = {
    'CIRCA': ['README.md', 'circa/alg/ci/__init__.py', 'circa/alg/ci/anm.py',
        'circa/alg/ci/base.py', 'circa/alg/common.py', 'circa/alg/base.py',
        'circa/model/case.py', 'circa/model/data_loader.py', 'circa/model/graph.py',
        'circa/graph/structural.py', 'circa/graph/r/__init__.py', 'circa/graph/r/causal.R',
        'circa/experiment/comparison/models.py', 'circa/experiment/comparison/utils.py',
        'circa/utils.py', 'tests/alg/sgraph/index.yml', 'build/requirements.txt',
        'build/requirements.R', 'Dockerfile'],
    'RCAEval': ['RCAEval/e2e/circa.py', 'RCAEval/graph_heads/rht.py',
        'RCAEval/graph_construction/pc.py', 'RCAEval/classes/data.py',
        'RCAEval/classes/graph.py', 'RCAEval/graph_heads/random_walk.py',
        'RCAEval/io/time_series.py', 'RCAEval/e2e/__init__.py'],
}
records=[]
for name, paths in files.items():
    root = circa if name == 'CIRCA' else rcaeval
    for p in paths:
        f=root / p
        records.append({'nguon': name, 'duong_dan': str(f), 'file': p,
            'sha256': sha(f), 'bytes': f.stat().st_size,
            'so_dong': len(f.read_text(encoding='utf-8').splitlines())})
pdf=out/'KDD22-CIRCA.pdf'
library_root = Path('D:/RCA-ext/envs/py312-pin/Lib/site-packages')
library_paths = [
    'causallearn/graph/GraphClass.py',
    'causallearn/search/ConstraintBased/PC.py',
    'causallearn/utils/PCUtils/SkeletonDiscovery.py',
    'causallearn/utils/cit.py',
    'sklearn/linear_model/_base.py',
    'sklearn/preprocessing/_data.py',
    'sklearn/utils/extmath.py',
]
library_records = []
for relative in library_paths:
    f = library_root / relative
    library_records.append({'file': relative, 'duong_dan': str(f),
        'sha256': sha(f), 'bytes': f.stat().st_size,
        'so_dong': len(f.read_text(encoding='utf-8').splitlines())})
manifest={
    'ngay_kiem': '2026-10-04',
    'CIRCA_revision': revision(circa),
    'RCAEval_revision': revision(rcaeval),
    'paper_url':'https://netman.aiops.org/wp-content/uploads/2022/08/KDD22-CIRCA.pdf',
    'paper_doi':'https://doi.org/10.1145/3534678.3539041',
    'paper_bytes':pdf.stat().st_size,
    'paper_sha256':sha(pdf),
    'paper_pages':11,
    'visual_pages_checked':[4,5,7,11],
    'artifact_revision_mentioned_in_README':'1522ddd7efd16db55e9f351fd70324501ce9134e',
    'artifact_downloaded':False,
    'published_numbers':'results/T-014/paper/cong-bo-circa.csv',
    'files':records,
    'library_environment':'D:/RCA-ext/envs/py312-pin',
    'library_versions':{name:metadata.version(name) for name in
                        ['causal-learn','scikit-learn','numpy','scipy']},
    'library_files':library_records,
}
(out/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (out/'cong-bo-circa.csv').open(encoding='utf-8',newline='') as f:
    numbers=list(csv.DictReader(f))
assert len(numbers)==11
assert numbers[0]['ac1']=='0.404'
assert numbers[1]['ac3']=='0.601'
assert numbers[2]['avg5']=='0.603'
print(json.dumps({'source_files':len(records),'published_rows':len(numbers),'pdf_bytes':manifest['paper_bytes'],'revisions_verified':True},ensure_ascii=False))
