import sys,json,hashlib,inspect
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'src'))
from do_thi.builder import build, project, CORE, edge_key

base=Path(__file__).parent
inputs=json.loads((base/'inputs.json').read_text('utf-8'))
expected=json.loads((base/'expected.json').read_text('utf-8'))
results=[]
for c in inputs:
    x=expected[c['name']];f=pd.DataFrame(c['spans'])
    if f.empty:f=pd.DataFrame(columns=CORE)
    try:
        e,o=build(f,None,{},c['universe'])
        assert not x['error'], 'expected error'
        actual=sorted([q['source'],q['target'],q['type']] for q in e['edges'])
        assert actual==sorted(x['edges']), (actual,x['edges'])
        assert e['stats']['internal_edge_events']==x['internal']
        if x['roots'] is not None:assert e['stats']['roots']==x['roots']
        assert e['stats']['orphans']==x['orphans']
        assert e['stats']['duplicate_rows']==x['duplicate']
        n,edges=project(o)
        assert n=={z['id'] for z in e['nodes']}
        assert edges=={edge_key(z) for z in e['edges']}
        e2,o2=build(f,None,{},c['universe']);assert (e,o)==(e2,o2)
        # Quy tắc thời gian nửa mở: biên phải loại span, cha ngoài biên không được nối.
        if c['name']=='F1':
            cut,_=build(f,[10000,60000],{},c['universe'])
            assert cut['stats']['unique_spans']==1 and cut['stats']['orphans']==1
        results.append({'name':c['name'],'pass':True,'entity':e,'operation':o})
    except ValueError as exc:
        assert str(exc)==x['error'],(c['name'],str(exc),x['error'])
        results.append({'name':c['name'],'pass':True,'expected_error':str(exc)})
# Các cột nhãn và tham số locator không lọt vào hợp đồng.
f=pd.DataFrame(inputs[0]['spans']);f['root']='B'
try:build(f,None,{},inputs[0]['universe']);raise AssertionError('accepted labels')
except ValueError as exc:assert str(exc)=='label_column'
assert list(inspect.signature(build).parameters)==['spans','interval','aliases','universe']
result={'fixtures':results,'signature':str(inspect.signature(build)),'label_rejection':True}
out=ROOT/'results/T-035/runs'/sys.argv[1];out.mkdir(parents=True,exist_ok=False)
(out/'result.json').write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2),'utf-8')
print(json.dumps({'pass':len(results),'sha256':hashlib.sha256((out/'result.json').read_bytes()).hexdigest()}))
