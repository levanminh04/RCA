"""All compact inputs and intervention X hashes, no likelihood/posterior rerun."""
import hashlib,json,pathlib
import numpy as np,pandas as pd
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[4];compact=ROOT/'results/T-032/runs/bo-sung-toan-dien-20261012-001/t32/t33-migration-001/migration-inputs-001';manifest=json.loads((compact/'manifest.json').read_text());summary=json.loads((P/'engine-final-summary-001.json').read_text());CAT=json.loads((ROOT/'results/T-033/runs/session9-report-002/source-catalog.json').read_text())['files'];rows=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for item in manifest['cases']:
 p=compact/item['file'];assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256'];z=np.load(p,allow_pickle=False);raw=z['causal_raw'];X=z['X'];rel=item['source_native']['relative'];native=ROOT/CAT[rel]['local_path'];assert native.stat().st_size==CAT[rel]['bytes'] and sha(native)==CAT[rel]['sha256'];old=np.load(native,allow_pickle=False)
 for key in ['X','times','columns','m','CP_flags']:assert np.array_equal(z[key],old[key])
 x=pd.DataFrame(raw).replace([np.inf,-np.inf],np.nan).ffill().fillna(0).to_numpy(float);lo=x[:100].min(0);hi=x[:100].max(0);div=np.where(hi>lo,hi-lo,1.);fixed=(x-lo)/div;exp=fixed.copy()
 for i in range(100,len(x)):
  lo=x[:i].min(0);hi=x[:i].max(0);exp[i]=(x[i]-lo)/np.where(hi>lo,hi-lo,1.)
 keep=np.r_[True,np.any(X[1:]!=X[:-1],axis=1)];xs={'prior_df4':X,'prior_kappa4':X,'prior_precision4':X,'causal_fixed':fixed,'causal_expanding':exp,'compressed_row':X[keep],'compressed_calendar':X[keep]}
 for branch,xx in xs.items():
  slot=next(q for q in summary['slots'] if q['opaque_id']==item['opaque_id'] and q['branch']==branch);assert slot['status']=='PASS' and list(xx.shape)==slot['X_shape'] and hashlib.sha256(xx.tobytes()).hexdigest()==slot['X_sha256'];rows.append({'case':item['case'],'opaque_id':item['opaque_id'],'branch':branch,'shape':list(xx.shape),'X_hash_exact':True,'compact_source_hash':item['sha256'],'native_array_copy_exact':True,'native_source':rel})
q=P/'engine-input-verification-all30-001.json';assert not q.exists();q.write_text(json.dumps({'status':'PASS_30CASES_210INTERVENTION_INPUTS','case_count':30,'intervention_input_checks':len(rows),'rows':rows,'scope':'Same compact arrays copied from pinned native arrays, exact intervention matrix hash/dimension, causal realraw warmup and compressed mapping input; no posterior/m/CP recompute'},ensure_ascii=False,indent=2)+'\n');print('PASS',len(rows),'intervention input hashes')
