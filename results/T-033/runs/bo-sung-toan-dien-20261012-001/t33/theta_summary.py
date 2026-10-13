import collections,hashlib,json,pathlib,sys
P=pathlib.Path(__file__).resolve().parent
files=sorted(P.glob('dev-*--theta-target-density-*.json'));rows=[];mapping={};pins=[]
for p in files:
 d=json.loads(p.read_text());assert d['status']=='PASS';pins.append({'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 for r in d['rows']:mapping[(d['source'],r['index'])]=(p.name,r)
 rows.extend({'source':d['source'],'file':p.name,**r} for r in d['rows'] if r['was_locked'])
locks=json.loads((P/'bocpd-locks.json').read_text());expected=sum(len(x['points']) for x in locks)
coverage=[]
for unit in locks:
 for i in unit['points']:coverage.append({'source':unit['npz'],'index':i,'present':(unit['npz'],i) in mapping})
effects=[]
for r in rows:
 if not r['CP_flag'] or r['m']==0 or r['previous_m'] is None:continue
 a=next(v for v in r['parents'] if v['parent']==r['m']-1);b=next(v for v in r['parents'] if v['parent']==r['previous_m'])
 if min(a['prior_parent_posterior'],b['prior_parent_posterior'],a['pdf_authoritative_saved'],b['pdf_authoritative_saved'])<=0:continue
 import math
 prior=math.log(a['prior_parent_posterior'])-math.log(b['prior_parent_posterior']);density=math.log(a['pdf_authoritative_saved'])-math.log(b['pdf_authoritative_saved']);normal=a['logpdf_normalizer']-b['logpdf_normalizer'];resid=a['logpdf_residual']-b['logpdf_residual'];total=prior+density;assert abs(density-(normal+resid))<2e-10
 effects.append({'source':r['source'],'index':r['index'],'m':r['m'],'previous_m':r['previous_m'],'log_parent_posterior_advantage':prior,'log_density_advantage':density,'log_normalizer_advantage':normal,'log_residual_advantage':resid,'log_growth_advantage':total,'numeric_source':'saved density/R; reconstructed native exacttheta, independent algebra bounded before run','interpretation':'Winner against previous MAP continuation; not physical-cause or prior-alone attribution'})
value={'status':'COMPLETE' if len(files)==len(locks) and all(x['present'] for x in coverage) else 'PARTIAL','sources':len(files),'expected_sources':len(locks),'locked_points_present':len(rows),'expected_unique_locked_points':expected,'original_theta_absent_unique_points_reconstructed':sum(not x['had_saved_theta'] for x in rows),'exact_stored_theta_checks':sum(json.loads(p.read_text())['theta_exact_stored_checks'] for p in files),'native_selected_batch_max_relative_difference':max([json.loads(p.read_text())['native_selected_batch_max_relative_difference'] for p in files],default=None),'manual_log_density_max_abs_error':max([json.loads(p.read_text())['log_density_max_abs_error'] for p in files],default=None),'files':pins,'coverage':coverage,'growth_margin_decomposition':effects,'growth_margin_summary':{'rows':len(effects),'source_prior_posterior_opposes_MAP':sum(x['log_parent_posterior_advantage']<0 for x in effects),'likelihood_opposes_MAP':sum(x['log_density_advantage']<0 for x in effects),'volume_normalizer_opposes_MAP':sum(x['log_normalizer_advantage']<0 for x in effects),'residual_opposes_MAP':sum(x['log_residual_advantage']<0 for x in effects)},'limits':['607 unique NPZ/point counts deduplicated; 664 original unit-points may repeat same sourcepoint; report both denominators before comparing','No CP threshold, prior, input or result altered; decomposition conditional on native model and observed processed history','Statistical decomposition is not independent physical onset or operational correctness evidence']}
q=P/sys.argv[1];assert not q.exists();q.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:value[k] for k in ['status','sources','locked_points_present','original_theta_absent_unique_points_reconstructed','exact_stored_theta_checks','manual_log_density_max_abs_error','native_selected_batch_max_relative_difference','growth_margin_summary']},ensure_ascii=False))
