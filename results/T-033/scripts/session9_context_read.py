"""Display saved context selections; retrieval only, no calculation."""
import pathlib,json
R=pathlib.Path(__file__).resolve().parents[3]/'results/T-033/runs/session9-report-001'
def read(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
for r in read('duration-at-locked-points.json')['rows']:
 if r['opaque_id']=='dev-03d4910932' and r['index'] in [124,125,683,684,723,724]:
  print(json.dumps({**{k:r[k] for k in ['opaque_id','index','second','source_npz']},'entities':[e for e in r['observed_entities'] if e['entity'] in ['ts-route-service','ts-security-service']]},ensure_ascii=False))
for ri,r in enumerate(read('workload-at-locked-points.json')['rows']):
 if r['opaque_id']=='dev-03d4910932' and r['index'] in [124,125,683,684,723,724]:
  ids=[r['columns'].index(c) for c in ['ts-route-service_workload','ts-security-service_workload'] if c in r['columns']]
  print(json.dumps({'row':ri,'index':r['index'],'source_npz':r['source_npz'],'values':[{k:r[k][i] for k in ['columns','values','missing_mask','inf_mask']} for i in ids]},ensure_ascii=False))
