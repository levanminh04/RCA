"""Verify pinned source snippets and TORAI default branch without running methods."""
from pathlib import Path
import ast,csv,hashlib,json
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'results/T-020/trung-gian/root'
checks=[]
input=json.loads((ROOT/'results/T-020/trung-gian/method_evidence/runs/deep-source-audit.json').read_text(encoding='utf-8'))
for row in input['checks']:
    path=Path(row['source']);b=path.read_bytes();s=b.decode('utf-8')
    assert hashlib.sha256(b).hexdigest()==row['sha256']
    if not row['needle'].startswith('AST '):
        lines=[i+1 for i,z in enumerate(s.splitlines()) if row['needle'] in z]
        assert lines==row['lines']
        task='T-015' if 'MicroRank' in str(path) else 'T-016' if 'torai.py' in str(path) else 'T-013' if 'baro' in str(path).lower() else 'T-014'
        checks.append(dict(task=task,source=str(path),key=row['needle'],original=str(row['lines']),recomputed=str(lines),match=True,reason='root read original code lines and rehash'))

def stride_nodes(tree):
    return [n for n in ast.walk(tree) if isinstance(n,ast.Assign) and ast.unparse(n).startswith('metric = metric.iloc[::15, :]')]

raw=ast.parse(Path('D:/RCA-ext/src/RCAEval/RCAEval/e2e/torai.py').read_text(encoding='utf-8'))
fixed=ast.parse((ROOT/'src/torai/torai_sua.py').read_text(encoding='utf-8'))
assert len(stride_nodes(raw))==2
assert len(stride_nodes(fixed))==2  # one remains behind disabled compatibility guard
guard=[n for n in ast.walk(fixed) if isinstance(n,ast.If) and ast.unparse(n.test)=='not sua_giam_mau']
assert len(guard)==1 and len(stride_nodes(guard[0]))==1
funcs=[n for n in fixed.body if isinstance(n,ast.FunctionDef) and n.name in ['torai','_rcd_multimodal']]
for fun in funcs:
    defaults=dict(zip([a.arg for a in fun.args.args][-len(fun.args.defaults):],fun.args.defaults))
    assert ast.literal_eval(defaults['sua_giam_mau']) is True
    assert ast.literal_eval(defaults['sua_ghep']) is True
checks.append(dict(task='T-016',source='src/torai/torai_sua.py:38,39,103',key='default active stride assignments',original=1,recomputed=len(stride_nodes(fixed))-len(stride_nodes(guard[0])),match=True,reason='two literals but inner branch is disabled by sua_giam_mau=True; both functions defaults checked'))
checks.append(dict(task='T-016',source='D:/RCA-ext/src/RCAEval/RCAEval/e2e/torai.py:29,81',key='original active strides',original=2,recomputed=len(stride_nodes(raw)),match=True,reason='unguarded original double subsampling'))
with (OUT/'root-code-checks.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(checks[0]));w.writeheader();w.writerows(checks)
print('root source checks',len(checks),'PASS')
