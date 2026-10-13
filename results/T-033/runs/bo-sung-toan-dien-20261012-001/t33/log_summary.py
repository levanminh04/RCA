"""Observed outcomes by case and every declared locked comparison window."""
import collections,importlib.util,json,pathlib
import numpy as np
sp=importlib.util.spec_from_file_location('w',pathlib.Path(__file__).with_name('worker-v3.py'));w=importlib.util.module_from_spec(sp);sp.loader.exec_module(w)
rows=[];pins=[];total=collections.Counter()
for item in w.S['cases']:
 oid=item['opaque_id'];q=w.OUT/(oid+'--log-semantics.json');v=json.loads(q.read_text());pins.append({'file':q.name,'bytes':q.stat().st_size,'sha256':w.sha(q)})
 if v['status']=='N/A_MISSING_CHANNEL':rows.append({'opaque_id':oid,'status':v['status']});continue
 a=np.load(w.OUT/v['http_access']['parsed_row_index_artifact']['file'],allow_pickle=False);_,native=w.input_arrays(oid);times=native['times'];windows=[]
 for point in v['region_points']:
  for width in [10,30,60]:
   for side,lo,hi in [('before',max(0,point-width),point),('after',point,min(len(times),point+width))]:
    mask=(a['timestamp']>=times[lo])&(a['timestamp']<times[hi-1]+1) if hi>lo else np.zeros(len(a['timestamp']),bool)
    statuses=a['status'][mask];windows.append({'point':point,'width':width,'side':side,'lo':lo,'hi_exclusive':hi,'observed_HTTP_request_rows':int(mask.sum()),'HTTP_status_counts':dict(collections.Counter(str(x) for x in statuses)),'HTTP_status_family_counts':dict(collections.Counter(str(x//100)+'xx' for x in statuses)),'container_counts':dict(collections.Counter(a['container_name'][mask].tolist()))})
 total.update(v['http_access']['status_counts']);rows.append({'opaque_id':oid,'status':'PASS','region_rows':v['region_rows'],'template_classes':len(v['all_template_classes']),'literal_lexical_indicator_counts':v['literal_lexical_indicator_counts'],'HTTP_access':{k:v['http_access'][k] for k in ['parsed_rows','status_counts','status_family_counts','entities','unparsed_HTTP_like_rows']},'source':q.name,'windows':windows})
corr=w.OUT/'log-correlation-summary-001.json';assert corr.exists();cv=json.loads(corr.read_text());assert cv['status']=='COMPLETE'
w.write('log-semantics-summary-001.json',{'status':'COMPLETE','cases':rows,'source_files':pins,'correlation_source':{'file':corr.name,'bytes':corr.stat().st_size,'sha256':w.sha(corr)},'all_HTTP_status_counts_in_union_regions':dict(total),'cases_with_access_outcomes':sum(x['status']=='PASS' and x['HTTP_access']['parsed_rows']>0 for x in rows),'cases_with_literal_correlation_keys':sum(bool(x.get('explicit_correlation_ID_rows')) for x in cv['cases']),'semantic_statement':'Some recorded HTTP request outcomes are available in accesslog messages. They belong to observed containers/paths; no certified trace invocation join or system-level health/onset standard follows. Outcome missing at method-required location is different from no outcome anywhere in dataset. Every declared window retained; overlapping windows are not independent samples.'});w.emit({'log_summary':'COMPLETE','cases':len(rows),'HTTPstatus':dict(total),'correlationIDcases':sum(bool(x.get('explicit_correlation_ID_rows')) for x in cv['cases'])})
