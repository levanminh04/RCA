"""Retain failed runs; retry three unchanged arithmetic copies in existing env."""
from pathlib import Path
import ast
O=Path('D:/RCA-flashticket/results/T-020/trung-gian/method_evidence');S=O/'scripts'
s=(S/'run_additional_replays.py').read_text(encoding='utf-8');t=ast.parse(s);n=next(x for x in t.body if isinstance(x,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='jobs' for a in x.targets));jobs=ast.literal_eval(n.value)[:3];jobs=[(task,name+' compatible-env-retry','D:/RCA-ext/envs/T-014-main/Scripts/python.exe',script,[str(x).replace('microrank-inputs-001','microrank-inputs-002').replace('circa-window-001','circa-window-002') for x in args],source,reason,why+'; original failed run retained: py312-pin lacks pyarrow/networkx.topological_generations') for task,name,python,script,args,source,reason,why in jobs]
old=ast.get_source_segment(s,n);s=s.replace(old,'jobs='+repr(jobs)).replace('enumerate(jobs,9)','enumerate(jobs,14)')
(S/'run_retry_replays.py').write_text(s,encoding='utf-8');print('retries use existing T-014-main only; no install, arithmetic unchanged')
