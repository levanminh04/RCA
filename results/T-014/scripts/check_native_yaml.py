"""Compare adapter output with a native YAML Config and StructuralGraphFactory."""
import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys,json,networkx as nx,yaml
from pathlib import Path
sys.path.insert(0,'D:/RCA-ext/work/T-014/CIRCA')
from circa.graph.structural import StructuralGraph,StructuralGraphFactory
from circa.model.case import CaseData
from circa.model.data_loader import MemoryDataLoader
out=Path('D:/RCA-flashticket/results/T-014');configs=out/'graphs/native-yaml';configs.mkdir(exist_ok=True);checks=[]
reference=yaml.safe_load(Path('D:/RCA-ext/work/T-014/CIRCA/tests/alg/sgraph/index.yml').read_text().split('components:',1)[0])
for p in sorted((out/'graphs').glob('re2tt_*.json')):
    r=json.loads(p.read_text(encoding='utf-8'));mapped=[m for m in r['mapping'] if m['status']=='mapped'];calls=nx.DiGraph(r['call_edges'])
    cfg=dict(types=reference['types'],assumptions=reference['assumptions'],components=[])
    # Native YAML retains exact meaning; no author source edits.
    for s in sorted(set(calls)|{m['service'] for m in mapped}):
        cfg['components'].append(dict(name=s,dependencies={s:sorted(calls.successors(s))} if s in calls else {},mappings={m['metric']:[dict(type=m['type'],component=s)] for m in mapped if m['service']==s}))
    path=configs/f'{r["case"]}.yml';path.write_text(yaml.safe_dump(cfg,sort_keys=False),encoding='utf-8')
    data={}
    for m in mapped:data.setdefault(m['service'],{})[m['metric']]=[(0.,0.),(1.,1.)]
    case=CaseData(MemoryDataLoader(data),None,0.)
    original=StructuralGraphFactory(StructuralGraph(filename=str(path))).create(case,1.)
    serialized=configs/f'{r["case"]}-native.json'
    original.dump(str(serialized))
    native=json.loads(serialized.read_text(encoding='utf-8'))
    native_names=[f"{n['entity']}_{n['metric']}" for n in native['nodes']]
    edges={(native_names[a],native_names[b]) for a,b in native['edges']}
    saved={tuple(e) for e in r['edges']}
    native_nodes=set(native_names)
    expected=set(r['nodes'])-set(r['original_missing_nodes'])
    checks.append(dict(case=r['case'],edges_equal=edges==saved,native_node_coverage_equal=native_nodes==expected,edge_symmetric_difference=sorted(edges^saved)))
    assert edges==saved and native_nodes==expected,checks[-1]
(out/'runs/native-yaml-equivalence.json').write_text(json.dumps(dict(cases=len(checks),pass_=True,source='actual Config YAML and StructuralGraphFactory.create; label-free two-point loader only supplies metric mask',checks=checks),indent=2))
print(f'{len(checks)} native YAML/factory graphs match all adapter edges and original candidate nodes')
