"""Explicit original/deduplicated theta denominators + diagnostic exclusions."""
import collections,hashlib,json,pathlib
P=pathlib.Path(__file__).resolve().parent
source=P.parents[4]/'results/T-033/runs/session9-report-002/chuoi-bang-chung.json'
assert source.is_file(),source
v=json.loads(source.read_text());u=[x for x in v['units'] if x['detector']=='bocpd'];mapping={};absent=[]
for unit in u:
 for point in unit['points']:
  key=(point['source_pointer']['npz'],point['index']);entry={'source':key[0],'index':key[1],'CP_flag':point['CP_flag'],'m':point['m'],'theta_available':point['theta_available']}
  if key in mapping:assert mapping[key]['CP_flag']==entry['CP_flag'] and mapping[key]['m']==entry['m'] and mapping[key]['theta_available']==entry['theta_available']
  else:mapping[key]=entry
  if not point['theta_available']:absent.append(key)
summary=json.loads((P/'theta-summary-001.json').read_text());locks=json.loads((P/'bocpd-locks.json').read_text());assert set(mapping)=={(x['npz'],i) for x in locks for i in x['points']}
effects={(x['source'],x['index']) for x in summary['growth_margin_decomposition']};cp={(k) for k,x in mapping.items() if x['CP_flag']};m0={k for k in cp if mapping[k]['m']==0}
excluded=cp-effects;assert len(excluded)==0
value={'status':'PASS','source':{'path':str(source),'bytes':source.stat().st_size,'sha256':hashlib.sha256(source.read_bytes()).hexdigest()},'summary_source':{'file':'theta-summary-001.json','sha256':hashlib.sha256((P/'theta-summary-001.json').read_bytes()).hexdigest()},'original_units':len(u),'original_unitpoints':sum(len(x['points']) for x in u),'unique_sourcepoints':len(mapping),'repeated_unitpoint_references':sum(len(x['points']) for x in u)-len(mapping),'theta_absent_original_unitpoints':len(absent),'theta_absent_unique_sourcepoints':len(set(absent)),'reconstructed_theta_absent_unique':summary['original_theta_absent_unique_points_reconstructed'],'locked_point_decomposition_domain':{'not_CP':len(mapping)-len(cp),'CP_growth_positive_mass_and_density':len(effects),'CP_reset_MAP0_excluded':len(m0),'CP_zero_parent_or_density_excluded':len(excluded-m0)},'interpretation':'Previous_m is argmax of prior parent R, so signs prior<=0 and likelihood>=0 for new growth winner are consequences of comparator/equal hazard and MAP selection, not independently identified mechanism rates. Normalizer/residual are dependent algebra terms, not independent causes.','original_to_unique':[{'unit_index':i,'branch':x['branch'],'sourcepoint_keys':[[p['source_pointer']['npz'],p['index']] for p in x['points']]} for i,x in enumerate(u)]}
q=P/'theta-domain-annotations-001.json';assert not q.exists();q.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');print({k:value[k] for k in ['status','original_unitpoints','unique_sourcepoints','theta_absent_original_unitpoints','theta_absent_unique_sourcepoints','locked_point_decomposition_domain']})
