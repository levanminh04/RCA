"""Set construction được kiểm dưới hashseed cố định; không đọc main/src/data."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

code = r'''
import json
types_string=set('TSLE')
types_list=set(['T','S','L','E'])
types_literal={'T','S','L','E'}
records=[]
for sequence in ['SLE','LE','E','T']:
 direct=set(sequence)
 listed=set(list(sequence))
 parsed=listed & types_list
 records.append({'sequence':sequence,'direct':list(direct),'list_constructor':list(listed),
                 'parsed_intersection':list(parsed),'direct_vs_list_same_order':list(direct)==list(listed),
                 'direct_vs_parsed_same_order':list(direct)==list(parsed)})
print(json.dumps({'string':list(types_string),'list_constructor':list(types_list),
 'set_literal':list(types_literal),'string_vs_list_same_membership':types_string==types_list,
 'string_vs_list_same_order':list(types_string)==list(types_list),
 'string_vs_literal_same_order':list(types_string)==list(types_literal),'effects':records}))
'''
p=Path(__file__).resolve().parent
records=[]
for seed in range(6):
    env=dict(os.environ,PYTHONHASHSEED=str(seed),PYTHONDONTWRITEBYTECODE='1')
    tic=time.monotonic()
    result=subprocess.run([sys.executable,'-c',code],env=env,text=True,capture_output=True,check=True)
    records.append({'seed':seed,'elapsed_diagnostic':time.monotonic()-tic,
                    **json.loads(result.stdout)})
report={'requested_expression_pair':"set('TSLE') vs set(['T','S','L','E'])",
        'python_executable':sys.executable,'records':records,
        'all_requested_same_membership':all(r['string_vs_list_same_membership'] for r in records),
        'all_requested_same_iteration_order':all(r['string_vs_list_same_order'] for r in records),
        'scope_limit':'Chỉ loại trừ đúng cặp constructors đã hỏi trên seeds0..5/Python hiện tại. Không chứng minh hai configs/graphs tương đương; literal/intersection/insertion/SCC ordering được báo riêng.'}
(p/'set-construction-comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=True))
