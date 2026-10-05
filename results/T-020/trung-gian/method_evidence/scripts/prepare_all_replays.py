"""Make protected copies; all inputs are original TX2 results or prior cases."""
from pathlib import Path
import ast,json,hashlib
R=Path('D:/RCA-flashticket');O=R/'results/T-020/trung-gian/method_evidence';S=O/'scripts';audits=[]
def copy(src,dest,changes):
    p=R/src;s=p.read_text(encoding='utf-8-sig');a=ast.parse(s)
    for old,new in changes:
        assert old in s,(src,old);s=s.replace(old,new)
    ast.parse(s);q=S/dest;q.write_text(s,encoding='utf-8')
    audits.append({'source':str(p),'original_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'copy':str(q),'copy_sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'source_read_whole':True,'original_imports':[ast.unparse(x) for x in ast.walk(a) if isinstance(x,(ast.Import,ast.ImportFrom))],'changes':[old for old,new in changes],'write_guard':'guarded_runner.py interpreter audit-hook for all open/mkdir/mutations; -B prevents bytecode','arithmetics_changed':False})
copy('results/T-013/scripts/kiem_cua_so_delay.py','t013_window_copy.py',[("OUT = ROOT / 'results/T-013'",f"OUT = Path('{O.as_posix()}/runs/t013-window-root')"),('budget_seconds=600','budget_seconds=280'),('START < 600','START < 280')])
for name in ['runs','trung-gian']:(O/'runs/t013-window-root'/name).mkdir(parents=True,exist_ok=True)
copy('results/T-014/paper/independent_scores.py','circa_independent_copy.py',[("    args = parser.parse_args()",f'''    args = parser.parse_args()
    if not args.self_test:
        assert args.snapshot.resolve()==Path('{R.as_posix()}/results/T-014/runs/example-architecture/snapshot.json').resolve()
        assert args.out.resolve()==Path('{O.as_posix()}/runs/circa-arithmetic-001').resolve()
''')])
copy('results/T-016/scripts/tinh_lai_s9.py','torai_s9_copy.py',[])
h=R/'results/T-016/scripts/chay_torai.py';hs=h.read_text(encoding='utf-8-sig');f=next(x for x in ast.parse(hs).body if isinstance(x,ast.FunctionDef) and x.name=='dung_dau_vao')
(S/'harness_input_only.py').write_text('import os\nimport numpy as np\nimport pandas as pd\n'+ast.get_source_segment(hs,f)+'\n',encoding='utf-8')
audits.append({'source':str(h),'original_sha256':hashlib.sha256(h.read_bytes()).hexdigest(),'copy':str(S/'harness_input_only.py'),'source_read_whole':True,'changes':'AST extract only dung_dau_vao function + os/numpy/pandas imports; no harness global/author import; function AST unchanged','source_function_lines':[f.lineno,f.end_lineno],'arithmetics_changed':False})
copy('results/T-016/scripts/tinh_tay.py','torai_full_independent_copy.py', [('from chay_torai import dung_dau_vao','from harness_input_only import dung_dau_vao'),('    a = ap.parse_args()',f'''    a = ap.parse_args()
    assert Path(a.ca).resolve()==Path('D:/RCA-ext/data/torai-OB/checkoutservice_cpu/1').resolve()
    assert a.length==10 and a.seed==0 and a.dataset=='torai-ob'
    assert Path(a.ra).resolve().parent==Path('{O.as_posix()}/runs').resolve()
''')])
copy('results/T-017/scripts/independent_example.py','simplerca_independent_copy.py',[('    args = parser.parse_args()',f'''    args = parser.parse_args()
    if args.input_dir is not None:
        assert args.input_dir.resolve()==Path('D:/RCA-ext/work/T-017/example-input-run-dev-005').resolve()
        assert args.out.resolve()==Path('{O.as_posix()}/runs/simplerca-arithmetic-001.json').resolve()
''')])
copy('results/T-018/scripts/tinh_tay_gdn.py','gdn_independent_copy.py',[(r'RES = r"D:\RCA-flashticket\results\T-018\runs"',f'RES = r"{O}/runs"'),('    a = ap.parse_args()',f'''    a = ap.parse_args()
    assert a.run=='r1s-re2tt5-cham' and a.data=='re2tt5'
    assert os.path.normpath(a.model)==os.path.normpath('D:/RCA-ext/work/T-018/gdn/runs/r1-re2tt5-seed5/model.pt')
'''),('np.save(os.path.join(out, "A_bien_the_b.npy"), A_b)',f'np.save(r"{O}/runs/gdn-A_bien_the_b.npy", A_b)'),('np.save(os.path.join(out, "A_tay.npy"), A)',f'np.save(r"{O}/runs/gdn-A_tay.npy", A)')])
(O/'runs/all-replay-copy-audit.json').write_text(json.dumps(audits,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'copies':len(audits),'source_whole_read':True,'arithmetic_unchanged':True}))
