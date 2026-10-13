"""EC2 group/control lock after factorial verification, before manual interpretation."""
import pathlib,json,hashlib,sys,os,datetime
H=pathlib.Path('/home/ubuntu/rca/T-033');sys.path.insert(0,str(H/'scripts/session6-002'))
from common import sha,read,write,guard,load_pins
G=H/'inputs/session6-groups-001/source.json'
assert sha(G)==os.environ['T033_GROUP_INPUT_SHA256'];M=read(G);load_pins();guard(8*2**20)
out=H/'runs/session6-groups-001';out.mkdir(exist_ok=False)
source=read(H/'inputs/source.json');cases={c['opaque_id']:c for c in source['cases']}
context={}
for name in ('channel-pilot-001','channel-rest-001'):
 r=H/'runs'/name;assert read(r/'status.json')['status']=='PASS'
 for oid,m in read(r/'context-index.json')['records'].items():
  assert oid not in context;manifest=read(r/'manifest.json');p=r/m['record'];assert sha(p)==manifest[p.name]['sha256'];context[oid]=read(p)
assert set(context)==set(cases)
factorial={}
for rel,m in M['factorial_records'].items():
 p=H/rel;assert sha(p)==m['sha256'] and p.stat().st_size==m['bytes'];j=read(p);assert j['status']=='PASS';assert j['opaque_id'] not in factorial;factorial[j['opaque_id']]=(rel,j)
assert set(factorial)==set(cases)
labels={(r['opaque_id'],r['detector']):r for r in M['old_rows']}
groups={};units=[];contrasts=[]
def add(key,oid,branch,kind):groups.setdefault(key,[]).append({'opaque_id':oid,'branch':branch,'kind':kind})
for oid,(rel,j) in sorted(factorial.items()):
 assert j['metadata']['M_P_subset_M_F_before_fill']
 for branch,b in j['branches'].items():
  valid=b['valid_computational_output'];empty=b['no_input_channels'];collapse=b['range0_processing'] and valid
  assert empty==(b['metadata']['d']==0)
  unit={'opaque_id':oid,'branch':branch,'valid_computational_output':valid,'native_status':b['result']['status'],'no_input_channels':empty,'native_error':b['native_error'],'valid_native_range0_collapse':collapse,'source_record':rel,'source_pointer':'/branches/'+branch}
  units.append(unit);add('factorial/'+branch+'/valid' if valid else 'factorial/'+branch+'/error',oid,branch,'branch')
  if empty:add('factorial/'+branch+'/no-input-channels',oid,branch,'branch')
  if collapse:add('factorial/'+branch+'/valid-collapse',oid,branch,'branch')
  if valid:add('factorial/'+branch+'/CP-present' if any(b['CP_flags']) else 'factorial/'+branch+'/no-CP',oid,branch,'branch')
 for pair,check in j['same_input_checks'].items():
  equal=check['same_input_shape_order_and_native_params'];ab=pair.split('_vs_');valid=all(j['branches'][b]['valid_computational_output'] for b in ab)
  if equal:
   assert all(check['exact_output_checks'].values());add('input-identical/'+pair,oid,pair,'pair')
  contrasts.append({'opaque_id':oid,'kind':'input-pair','pair':pair,'input_identical':equal,'valid_computational_output':valid,'source':rel+'#/same_input_checks/'+pair})
 for key,c in j['contrasts'].items():
  defined=c['defined'];changed=None
  if defined:
   m=c['signed_m_interaction'] if key=='interaction' else c['signed_m_difference'];cp=c['signed_CP_flag_interaction'] if key=='interaction' else c['signed_CP_flag_difference']
   changed=any(v!=0 for v in m) or any(v!=0 for v in cp)
  add('contrast/'+key+('/different' if changed else '/no-difference') if defined else 'contrast/'+key+'/undefined',oid,key,'contrast')
  contrasts.append({'opaque_id':oid,'kind':'contrast','contrast':key,'defined':defined,'m_or_CP_changed':changed,'source':rel+'#/contrasts/'+key})
locked=[]
for key,members in sorted(groups.items()):
 members.sort(key=lambda r:r['opaque_id']);rep=members[0];oid=rep['opaque_id'];in_group={r['opaque_id'] for r in members};cell=labels[(oid,'bocpd')]['cell'];d=labels[(oid,'bocpd')]['d'] or 0
 def metrics(x):
  summ=context[x]['summary'];al=summ['trace']['alignment'];return ('logs.parquet' in cases[x]['files'],al['metric_seconds_with_observed_events'],al['on_metric_grid_rows'])
 rep_coverage=metrics(oid)
 candidates=[x for x in sorted(cases) if x not in in_group]
 candidates.sort(key=lambda x:(labels[(x,'bocpd')]['cell']!=cell,metrics(x)[0]!=rep_coverage[0],abs(metrics(x)[1]-rep_coverage[1]),abs(metrics(x)[2]-rep_coverage[2]),abs((labels[(x,'bocpd')]['d'] or 0)-d),x))
 ctrl=candidates[0] if candidates else None
 locked.append({'group':key,'members':members,'representative':rep,'control':None if ctrl is None else {'opaque_id':ctrl,'branch':rep['branch'],'kind':rep['kind']},'matching':{'detector':'bocpd','dataset':'RE2-TT dev','same_input_type':True,'same_cell':None if ctrl is None else labels[(ctrl,'bocpd')]['cell']==cell,'same_trace_grid_counts_and_log_presence':None if ctrl is None else metrics(ctrl)==rep_coverage,'same_d':None if ctrl is None else (labels[(ctrl,'bocpd')]['d'] or 0)==d,'collector_coverage':'OPEN; observed bin coverage does not establish collector completeness'},'missing_condition':'No outside-group case; select within-case no-CP point in manual reading' if ctrl is None else None,'interpretation_status':'LOCK_ONLY_NOT_READ'})
denominators={'branch_units':len(units),'valid_output_units':sum(u['valid_computational_output'] for u in units),'native_error_units':sum(not u['valid_computational_output'] for u in units),'no_input_channel_units':sum(u['no_input_channels'] for u in units),'valid_collapse_units':sum(u['valid_native_range0_collapse'] for u in units),'input_pairs':sum(c['kind']=='input-pair' for c in contrasts),'contrasts':sum(c['kind']=='contrast' for c in contrasts),'defined_contrasts':sum(c['kind']=='contrast' and c['defined'] for c in contrasts),'undefined_contrasts':sum(c['kind']=='contrast' and not c['defined'] for c in contrasts)}
assert denominators['branch_units']==120 and denominators['valid_output_units']+denominators['native_error_units']==120
write(out/'bao-phu-nhom.json',{'status':'LOCKED_AFTER_FACTORIAL_BEFORE_MANUAL_INTERPRETATION','original_groups_preserved':M['old_groups'],'new_groups':locked,'branch_units':units,'contrast_units':contrasts,'denominators':denominators,'category_note':'Input equality is a pair relation; collapse/no-channel/error are distinct stored fields, can overlap. Do not sum them as causes. Undefined contrasts never become zero.','selection_rule':'same detector/branch/dataset/input type; representative smallest opaque ID; prefer same cell, log presence/observed trace coverage/scale and d; tie smallest ID. No physical correct control inferred.','point_control_rule':'CP/flag versus adjacent available no-CP/no-flag on same grid, resolved during manual reading; missing neighbor remains OPEN.','source_sha256':M['source_sha256'],'all_case_paths':M['old_groups']['all_case_paths'],'context_pointers':{oid:'runs/'+('channel-pilot-001' if oid==source['cases'][0]['opaque_id'] else 'channel-rest-001')+'/'+context[oid]['output_npz'] for oid in cases},'interpretation_status':'No manual chains/mechanism/synthesis yet'})
write(out/'verification.json',{'status':'PASS','full_30_factorial_and_context':True,'separate_denominators':denominators,'source_inputs_pinned':True,'old_group_output_preserved':True,'resources':guard(),'at':datetime.datetime.now(datetime.timezone.utc).isoformat()})
write(out/'manifest.json',{p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in out.iterdir() if p.is_file() and p.name!='manifest.json'})
print(json.dumps({'status':'PASS','groups':len(locked),'denominators':denominators}))
