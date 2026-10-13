"""Finite observation counts in exactly previous100 row slots."""
import collections,importlib.util,json,pathlib
import numpy as np
sp=importlib.util.spec_from_file_location('c',pathlib.Path(__file__).with_name('context.py'));c=importlib.util.module_from_spec(sp);sp.loader.exec_module(c);w=c.w
rows=[]
for item in w.S['cases']:
 oid=item['opaque_id']
 for det in ['nsigma','nsigma_doi_chung']:
  rel=c.nsigma_rel(oid,det);z=np.load(w.source(rel),allow_pickle=False);X=z['x'];counts=np.zeros(X.shape,dtype=np.int64);finite=np.isfinite(X)
  cumulative=np.vstack([np.zeros((1,X.shape[1]),dtype=np.int64),np.cumsum(finite,axis=0,dtype=np.int64)])
  for i in range(100,len(X)):counts[i]=cumulative[i]-cumulative[i-100]
  q=w.OUT/(oid+'--'+det+'--rolling-finite-counts.npz');assert not q.exists();np.savez_compressed(q,previous100rows_finite_count=counts,columns=z['columns'],start_index=np.array(100))
  rows.append({'opaque_id':oid,'detector':det,'source':rel,'file':q.name,'sha256':w.sha(q),'bytes':q.stat().st_size,'dimension':X.shape[1],'evaluation_cell_count':int(counts[100:].size),'finite_count_histogram':dict(collections.Counter(str(x) for x in counts[100:].ravel())),'columns_with_any_count_less100':z['columns'][np.any(counts[100:]<100,axis=0)].tolist(),'count_less2_cells':int((counts[100:]<2).sum()),'count_100_cells':int((counts[100:]==100).sum())})
w.write('rolling-finite-counts-summary-001.json',{'status':'COMPLETE','case_detectors':len(rows),'rows':rows,'interpretation':'100 previous rows/time slots, not necessarily100 finite observations. pandas skips NaN for mean/std; ddof1 needs count>=2. Frozen filled X preserved, no detector changed.'});w.emit({'rolling_finite_counts':'COMPLETE','case_detectors':len(rows),'count_less100_cells':sum(x['evaluation_cell_count']-x['count_100_cells'] for x in rows)})
