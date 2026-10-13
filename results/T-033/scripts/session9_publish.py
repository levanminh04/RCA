"""EC2: verify saved intermediates, annotate read chains, arrange final outputs. No detector replay."""
import pathlib,json,hashlib,gzip,time,math,shutil,collections
import numpy as np,psutil
H=pathlib.Path('/home/ubuntu/rca/T-033');OUT=H/'runs/session9-final-001';OUT.mkdir(exist_ok=False)
verified={}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def checked(r):
 p=(H/r).resolve();assert p.is_relative_to(H)
 if r not in verified:
  m=INPUT['pins'][r];assert p.stat().st_size==m['bytes'] and sha(p)==m['sha256'],r;verified[r]=m
 return p
def read(r):return json.loads(checked(r).read_text())
def clean(x):
 if isinstance(x,np.ndarray):return clean(x.tolist())
 if isinstance(x,np.generic):return clean(x.item())
 if isinstance(x,float) and not math.isfinite(x):return None
 if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [clean(v) for v in x]
 return x
def put(n,b):
 used=sum(p.stat().st_size for p in H.rglob('*') if p.is_file())
 assert used+len(b)+8*2**20<5*2**30 and shutil.disk_usage(H).free>len(b)+8*2**20
 assert time.perf_counter()-_start<_ledger['remaining_approved_s'] and psutil.virtual_memory().percent<95
 p=OUT/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
def write(n,x):put(n,(json.dumps(clean(x),ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n').encode())
E='runs/session8-evidence-001/';M='runs/session9-manual-001/';ST='runs/session8-stats-001/'
C=read(M+'unit-dossiers.json');G=read(M+'group-dossiers.json');F=read(E+'phan-ra-tien-xu-ly.json');D=read(E+'do-tre-sau-moc.json');N=read(E+'nsigma-nguong-co-dinh.json');T=read(E+'tai-log.json');J=read(E+'doi-chieu.json')
oldG=read(E+'bao-phu-nhom.json');stats=read(ST+'stats.json');sup=read(M+'supplemental-stats.json');pairs=read(M+'nsigma-same-column-controls.json')
checks=[];detailed=[];nsindex=[];boindex=[];chain_table=[];group_table=[]
for oid in sorted({u['opaque_id'] for u in C['units']}):
 rel='runs/'+('session7-manual-pilot-001' if oid=='dev-03d4910932' else 'session7-manual-rest-001')+'/'+oid+'--points.json.gz'
 body=json.loads(gzip.decompress(checked(rel).read_bytes()))
 narrow=next(u for u in body['units'] if u['detector']=='nsigma');wide=next(u for u in body['units'] if u['detector']=='nsigma_doi_chung')
 sourceN=narrow['points'][0]['source_arrays_pointer']['npz'];sourceW=wide['points'][0]['source_arrays_pointer']['npz']
 with np.load(checked(sourceN),allow_pickle=False) as a,np.load(checked(sourceW),allow_pickle=False) as b:
  ca=a['columns'].tolist();cb=b['columns'].tolist();ib=[cb.index(c) for c in ca]
  cc={'opaque_id':oid,'common_columns':len(ca),'common_columns_subset':set(ca)<=set(cb),'all_times_exact':np.array_equal(a['times'],b['times'])}
  for k in ['x','mean','std','count','threshold','margin','Z']:
   assert k in a.files and k in b.files,(oid,k)
   cc[k+'_all_points_exact']=np.array_equal(a[k],b[k][:,ib],equal_nan=True)
  assert all(v is True for k,v in cc.items() if k.endswith('_exact')) and cc['common_columns_subset'],cc
  cc['narrow_npz']=sourceN;cc['wide_npz']=sourceW;checks.append(cc)
 for u in body['units']:
  det,br=u['detector'],u['branch'];ri=next(i for i,r in enumerate(C['units']) if (r['opaque_id'],r['detector'],r['branch'])==(oid,det,br));r=C['units'][ri]
  r['manual_reading']={'status':'READ_SAVED_SCALAR_CHAIN','reader':'Codex worker','extent':'All locked scalar points, triggering witnesses and same-column controls; full vectors/arrays remain source, not a claim to read every raw cell','full_points_json_pointer':'#/units/'+str(body['units'].index(u)),'competing_physical_explanation':'OPEN','source_catalog':'source-catalog.json'}
  r['scientific_status']={'observation':'SAVED_NATIVE_RESULT','computational_mechanism':'VERIFIED_AT_LOCKED_POINTS','physical_cause':'OPEN','onset':'OPEN','method_selection':'OPEN'}
  r['mechanism']={'condition':'this fixed native configuration and saved observed input','step':'pdf × prior parent posterior → growth mass → normalize → MAP → abs(delta m)>1' if det=='bocpd' else 'Inf→NaN/ffill → past mean/std(ddof1) → abs(x-mean)>3std → OR over columns','information':'CP is a posterior-mode displacement, not severity/onset' if det=='bocpd' else 'signed direction and channel provenance are lost at merged boolean alarm','limits':'General computation does not explain why an early case is physically false while a proxy-S case is physically correct'}
  r['scoring']={'source':'src/p3/danh_gia.py:260-307','protocol':'proxy start to file end; first alarm is scored separately from existence of a later post-proxy alarm','diagnostic_uses_proxy':True,'engine_receives_labels':False}
  summary=[]
  for pi,p in enumerate(u['points']):
   reduced=r['points'][pi];assert p['index']==reduced['index']
   if det=='bocpd':
    assert p['CP_flag']==(p['index']>=1 and p['absolute_m_change']>1)
    assert math.isfinite(p['normalizer']) and p['normalizer']>0
    details={'unit_index':ri,'point_index':pi,'opaque_id':oid,'branch':br,'index':p['index'],'CP':p['CP_flag'],'m':p['m'],'previous_m':p['previous_m'],'theta_available':p['theta_available'],'source':rel,'source_point_pointer':'#/units/'+str(body['units'].index(u))+'/points/'+str(pi),'predictive_parent_indices':p.get('predictive_parent_indices'),'theta_keys':list(p.get('theta',{}))}
    boindex.append(details)
    summary.append(f"i{p['index']}:m{p['previous_m']}→{p['m']},CP={p['CP_flag']},MAP={p['MAP_posterior']:.9g},cont={reduced['previous_MAP_continuation_posterior']:.9g},theta={p['theta_available']}")
   else:
    assert p['merged_flag']==any(p['flags'])
    ids=[j for j,v in enumerate(p['flags']) if v]
    assert not any(p['flags'][j] and not p['finite_statistics_mask'][j] for j in range(len(p['columns'])))
    nsindex.append({'unit_index':ri,'point_index':pi,'opaque_id':oid,'detector':det,'index':p['index'],'flag':p['merged_flag'],'trigger_columns':[p['columns'][j] for j in ids],'source':rel,'source_point_pointer':'#/units/'+str(body['units'].index(u))+'/points/'+str(pi),'nonfinite_statistics_columns':[c for c,v in zip(p['columns'],p['finite_statistics_mask']) if not v]})
    witness=ids[0] if ids else next((j for j,v in enumerate(p['finite_statistics_mask']) if v),None)
    summary.append(f"i{p['index']}:flag={p['merged_flag']},ntrigger={len(ids)}"+(f",witness={p['columns'][witness]},x={p['x'][witness]},n={p['count'][witness]},mu={p['mean'][witness]},sd={p['std'][witness]},margin={p['margin'][witness]}" if witness is not None else ',no finite witness'))
  chain_table.append('| '+str(ri)+' | '+oid+'/'+det+'/'+br+' | '+'<br>'.join(summary)+' | `chuoi-bang-chung.json#/units/'+str(ri)+'` |')
  if det!='bocpd':
   for q in r['same_column_controls']:
    if q['control_index'] is None:continue
    for c in q['same_column_values']:
     assert c['alarm']['flags'] and not c['control']['flags']
     assert c['alarm']['finite_statistics_mask']
for gi,g in enumerate(G['groups']):
 name=g['group'];family=name.split('/')[0]
 if '/N1/' in name:obs='N1 compares early/late flag rates. Locked points show the strict threshold path, not stationary-baseline validity.';resolved='Local margin/OR is explained; whole-group cause of early-to-late rate change remains OPEN.'
 elif '/N2/' in name:obs='N2 groups first-trigger columns by empirical rate versus k*0.0027. Rate is not a Gaussian-tail diagnosis.';resolved='Finite value/mean/std explains flags at read points; non-Gaussianity, history and real changes not separately identified.'
 elif '/N3/' in name:obs='N3 is first-before-proxy and NOT N2 at that level, not a test of independent-column multiplicity.';resolved='Narrow/wide common-column statistics exact; added columns can add an OR alarm. Independent-test false alarm rate remains OPEN.'
 elif name.endswith('/N4'):obs='A first-trigger column has exact std0: any nonzero residual exceeds zero threshold. Other columns also trigger.';resolved='Std0 explains one OR path, not a unique physical cause or the necessity of that column.'
 elif '/B2/' in name:obs='B2 records absence of I1 CP around first full CP within locked delta. It is not a total-count contrast.';resolved='Factorial isolates scale with mask fixed and mask/d/prior as a bundle; absence near a timestamp does not identify prior alone.'
 elif '/B4/' in name:obs='B4 records per-column window shift/std crossing near first full CP under fixed w,k, not the multivariate BOCPD decision.';resolved='Saved density/mass/posterior/MAP explain CP; per-channel shift association does not assign causal weight to one channel.'
 elif name.startswith('D0/') or name.startswith('unexplained-primary/'):obs='No active primary flags is a grouping residual, not absence of a computational mechanism.';resolved='The representative and locked control both have posterior competition and CP/noCP chains. Physical reason remains OPEN.'
 elif name.startswith('contrast/interaction/'):obs='Both scale and mask contrasts plus signed interaction are stored pointwise.';resolved='Interaction in m/CP is distinct from interaction in total count; neither isolates prior.'
 elif name.startswith('contrast/mask_d_prior'):obs='Same scale source on common columns; mask/order/shape/d/prior change together.';resolved='Bundle effect or exact no-effect established on this prefix; prior-only effect OPEN.'
 elif name.startswith('contrast/scale') or name.startswith('contrast/total'):obs='Same-case/same-prefix branches retain raw input; scale holds mask/d/prior fixed; total changes both factors.';resolved='Changed processed history→density/posterior→m/CP. No outside-group case; branch comparison is retained.'
 elif name.startswith('input-identical/'):obs='Exact matrix/order/shape/native-parameter equivalence checked; exact m/CP equivalence checked.';resolved='No-effect is valid evidence for that pair, not a discarded experiment.'
 elif 'valid-collapse' in name:obs='Raw-before-fill mask may retain a column that becomes constant after fill; range0 division then fill0 produces valid zeros.';resolved='Collapse is computationally valid and distinct from d0/error. It does not alone explain CP contrasts.'
 elif '/no-CP' in name:obs='No CP within this valid prefix; m may continue or move by one without satisfying abs(delta m)>1.';resolved='First-CP shift stays null where absent; valid m/CP-set contrasts are retained. Not evidence of physical stability.'
 elif name.startswith('native-status/'):obs='Native OK means returned valid frozen output, not correct operational diagnosis.';resolved='All observed statuses retained; no non-OK case exists in this denominator. No outside-group comparator fabricated.'
 elif name.startswith('proxy-first/'):obs='S/E categories use first alarm relative to injection proxy; later post-proxy alarm and locked no-alarm point retained.';resolved='Threshold or MAP-to-CP path explained for each case. S does not establish true detection, E does not establish operational false alarm.'
 else:obs='Valid branch and CP-present path retained with all locked points.';resolved='Computational decision supported; no new physical or online-detector conclusion.'
 g['interpretation']={'observed_chain':obs,'discriminated':resolved,'reader':'Codex worker','same_case_point_controls':'all locked CP/noCP points and same-column pairs referenced in unit dossiers; absence preserved','physical_cause':'OPEN','cross_case_matching':'; '.join(g['missing_conditions']),'not_inferred_from_group_flag':True}
 if '/B4/' in name and g['control']=='dev-f36d0647d5':
  g['interpretation']['control_feature_validity']='B4 control feature valid=false / flag=null because first full CP is after proxy; outside group does not mean measured B4=false'
  resolved+=' Locked control B4 is invalid/null; it is not a measured negative for the window statistic.'
 g['chain_pointers']=['chuoi-bang-chung.json#/units/'+str(i) for i in g['representative_unit_indices']+g['control_unit_indices']]
 group_table.append('| '+str(gi)+' | '+name+' | '+g['representative']+' | '+str(g['control'])+' | '+obs+' '+resolved+' | '+'; '.join(g['missing_conditions'])+' |')
C['root_manual_reading']='COMPLETED_SAVED_SCALAR_AND_WITNESS_CHAINS; not every raw cell; physical attribution OPEN';C['no_detector_rerun']=True
G['root_manual_reading']='COMPLETED_GROUP_TO_CHAIN_AND_MATCHING';G['original_frozen_coverage']=oldG;G['all_units']=[{'unit_index':i,'opaque_id':u['opaque_id'],'detector':u['detector'],'branch':u['branch'],'chain_pointer':'chuoi-bang-chung.json#/units/'+str(i)} for i,u in enumerate(C['units'])]
write('chuoi-bang-chung.json',C);write('bao-phu-nhom.json',G)
F['root_interpretation']={'status':'COMPUTATIONAL_CONTRASTS_RESOLVED_WITH_LIMITS','scale':'Isolated within each fixed mask/d/prior','mask':'column/d/prior bundle only','interaction':'pointwise, not only total count','prior_alone':'OPEN','online_design':'NOT_SELECTED','all_input_states':sup['range0_rows'],'interaction_rows':sup['interaction_rows'],'identical_inputs':sup['input_identical_rows']}
write('phan-ra-tien-xu-ly.json',F)
for r in D['rows']:
 ri=next(i for i,u in enumerate(C['units']) if (u['opaque_id'],u['detector'],u['branch'])==(r['opaque_id'],r['detector'],'full'))
 r['mechanism_status']='COMPUTATIONAL_CHAIN_RESOLVED_AT_LOCKED_POINTS; physical delay OPEN';r['chain_pointer']='chuoi-bang-chung.json#/units/'+str(ri)
 r['P6_dependency']='Need true onset/clean negative and causal preprocessing to select operational detector';r['physical_delay']=None
write('do-tre-sau-moc.json',D);write('nsigma-nguong-co-dinh.json',N)
J['all_paths']=G['all_units'];J['group_table']='bao-phu-nhom.json#/groups';J['common_column_all_points_checks']=checks;write('doi-chieu.json',J)
for li,r in enumerate(T['log_excerpts']):
 for si,s in enumerate(r.get('samples',[])):
  s.pop('message',None);s['raw_message_source']=E+'tai-log.json#/log_excerpts/'+str(li)+'/samples/'+str(si)+'/message'
T['privacy']='Text omitted from publication; original deterministic row/digest source preserved; no token/userID printed';T['duration_projection']='duration-at-locked-points.json';T['workload_projection']='workload-at-locked-points.json';write('tai-log.json',T)
for n,r in [('duration-at-locked-points.json',M+'duration-at-locked-points.json'),('nsigma-trung-gian/same-column-controls.json',M+'nsigma-same-column-controls.json'),('workload-at-locked-points.json',ST+'workload-at-locked-points.json'),('stats.json',ST+'stats.json'),('supplemental-stats.json',M+'supplemental-stats.json')]:put(n,checked(r).read_bytes())
write('nsigma-trung-gian/index.json',{'points':nsindex,'full_array_catalog':'../source-catalog.json','same_column_controls':'same-column-controls.json','common_columns_all_points_checks':checks})
write('bocpd-trung-gian/index.json',{'points':boindex,'full_array_catalog':'../source-catalog.json','theta_absence':'observer retention, not absent native update','likelihood_mass_chain':'../chuoi-bang-chung.json'})
write('source-catalog.json',{'repository_root':'D:/RCA-flashticket','remote_root':str(H),'files':INPUT['catalog'],'all_remote_relative_pointers_resolve_here':True})
intro='''# Đọc tay T-033 — toàn bộ đường và nhóm đã khóa

Codex là người làm. Đây là tổng hợp chuỗi gốc, không phải Claude phản biện. Đã đọc scalar ở mọi điểm khóa và các cột làm chứng/cặp cùng cột. Không nhận đã đọc từng raw cell hay mọi covariance. Nguồn đầy đủ giữ trong gzip/NPZ theo source-catalog.json; chữ READ chỉ phạm vi đọc này.

`nguyen-nhan-phat-hien.md` trình giải thích cạnh tranh và chuỗi chi tiết. `kiem-tiep.md` ghi phép phân xử còn thiếu. Cột witness đủ chỉ một đường làm OR=True; không nói đó là cột duy nhất gây báo. CP/noCP trong bảng là phép tính; S/E chỉ chấm theo proxy. Các cặp khác ca còn sai khác matching nêu rõ ở bảng nhóm. Không dùng đại diện để suy nguyên nhân cho mọi thành viên.

## Mọi ca × đường xử lý

Mỗi dòng giữ toàn bộ điểm khóa, kể cả không báo, collapse, đầu/cuối và điểm contrast. Với N-Sigma, lấy đối chứng đúng cùng cột từ nsigma-trung-gian/same-column-controls.json; không dùng witness của noalarm như thể cùng cột của alarm. Với BOCPD, cont là posterior của continuation từ MAP trước; theta=False nghĩa observer không giữ theta tại điểm đó. Toàn bộ input channels, density, mass và trạng thái được nối qua JSON/gzip/NPZ.

| Unit | Ca/đường | Các scalar đã đọc | Con trỏ |
|---|---|---|---|
'''
doc=intro+'\n'.join(chain_table)+'\n\n## Mọi nhóm bắt buộc và đối chứng khóa\n\nKhông có outside-group case được giữ nguyên; đối chứng điểm/nhánh cùng ca không bị thay bằng ca thuận lợi. Các trường missing_conditions là điều kiện chưa ghép, không bằng chứng dataset gây lỗi.\n\n| Nhóm | Tên khóa | Đại diện | Đối chứng ca | Chuỗi và mức phân xử | Matching còn thiếu |\n|---|---|---|---|---|---|\n'+'\n'.join(group_table)+'\n'
put('doc-tay.md',doc.encode())
write('validation.json',{'status':'PASS','no_detector_rerun':True,'source_files_verified':verified,'common_columns_all_points_checks':checks,'point_safety':sup['point_safety'],'all_units':len(C['units']),'locked_points':sum(len(u['points']) for u in C['units']),'groups':len(G['groups']),'branch_denominators':sup['denominators'],'root_reading_extent':C['root_manual_reading'],'physical_cause':'OPEN','native_source_unchanged':sha(H/'inputs/source.json'),'body_s':time.perf_counter()-_start})
write('manifest.json',{str(p.relative_to(OUT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in OUT.rglob('*') if p.is_file()})
print(json.dumps({'status':'PASS','run':'session9-final-001','files':{str(p.relative_to(OUT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in OUT.rglob('*') if p.is_file()},'detectors_reexecuted':False},ensure_ascii=False))
