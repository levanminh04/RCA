"""Oracle trước sửa biên: kind bản tin đã biết nhưng không có attributes/links."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import pandas as pd

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[3]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('output');parser.add_argument('--builder-path',type=Path)
    args=parser.parse_args();out=(BASE/args.output).resolve();assert out.parent==BASE;out.mkdir(exist_ok=False)
    path=args.builder_path or ROOT/'src/do_thi/builder.py'
    spec=importlib.util.spec_from_file_location('boundary_builder',path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    base=dict(traceID='t',spanID='c',parentSpanID='',serviceName='C',operationName='process',startTime=0,duration=1,kind='CONSUMER')
    issues={'identity_unverified':{'count':1,'witness':[['t','c']]},'queue_address_incomplete':{'count':1,'witness':[['t','c']]}}
    # Expected là literal, không lấy từ builder; ca thứ hai bỏ hẳn hai cột.
    cases=[('consumer-null',dict(base,attributes=None,links=None),1,issues),
           ('consumer-columns-absent',base,1,issues),
           ('producer-columns-absent',dict(base,kind='PRODUCER'),0,{})]
    results=[]
    for name,row,unresolved,diagnostics in cases:
        e,o=module.build(pd.DataFrame([row]),None,{}, {'C':'service'})
        actual={'entity_edges':e['edges'],'operation_edges':o['edges'],'entity_unresolved':e['stats']['unresolved_messages'],
                'operation_unresolved':o['stats']['unresolved_messages'],'entity_diagnostics':e.get('messaging_diagnostics'),
                'operation_diagnostics':o.get('messaging_diagnostics')}
        actual=json.loads(json.dumps(actual))
        expected={'entity_edges':[],'operation_edges':[],'entity_unresolved':unresolved,'operation_unresolved':unresolved,
                  'entity_diagnostics':diagnostics,'operation_diagnostics':diagnostics}
        results.append({'name':name,'input':row,'actual':actual,'expected':expected,'pass':actual==expected})
    result={'utc':datetime.now(timezone.utc).isoformat(),'builder_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'oracle_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'cases':results,'pass':all(x['pass'] for x in results)}
    (out/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf-8')
    print(json.dumps({'pass':result['pass'],'cases':len(results)}));return 0 if result['pass'] else 1


if __name__=='__main__':raise SystemExit(main())
