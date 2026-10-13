"""All observed templates + literal HTTP access outcomes in declared regions."""
import collections,hashlib,importlib.util,json,pathlib,re,time
import numpy as np,pandas as pd
sp=importlib.util.spec_from_file_location('w',pathlib.Path(__file__).with_name('worker-v3.py'));w=importlib.util.module_from_spec(sp);sp.loader.exec_module(w)
pairs=json.loads((w.OUT/'locked-pairs.json').read_text())
ACCESS=re.compile(r'"(?P<method>[A-Z]+) (?P<target>[^\s"]+) (?P<protocol>HTTP/\d(?:\.\d)?)"\s+(?P<status>\d{3})\s+(?P<bytes>\d+|-)')
LEX=re.compile(r'\b(?:fail(?:ed|ure|s)?|error|exception|timeout|success(?:ful)?|denied|refused)\b|timed out',re.I)
def template(s):
 s=re.sub(r'\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:[.,]\d+)?','<datetime>',s)
 s=re.sub(r'\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2}\s+[+-]\d{4}','<access_datetime>',s)
 s=re.sub(r'\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b','<uuid>',s)
 s=re.sub(r'\b[0-9a-fA-F]{16,}\b','<hexid>',s)
 return re.sub(r'(?<![A-Za-z])[-+]?\d+(?:\.\d+)?','<number>',s)
def run():
 catalog=[]
 for ci,item in enumerate(w.S['cases']):
  oid=item['opaque_id'];name=oid+'--log-semantics.json';dest=w.OUT/name
  if dest.exists():v=json.loads(dest.read_text());catalog.append({'file':name,'bytes':dest.stat().st_size,'sha256':w.sha(dest)});continue
  start=time.perf_counter()
  if 'logs.parquet' not in item['files']:
   v={'status':'N/A_MISSING_CHANNEL','opaque_id':oid};w.write(name,v)
  else:
   q=w.raw_path(item,'logs.parquet');df=pd.read_parquet(q);_,z=w.input_arrays(oid);times=z['times'];region=np.zeros(len(df),bool)
   points=sorted(set(p[k] for p in pairs if p['opaque_id']==oid for k in ['alarm_index','control_index'] if p[k] is not None))
   for point in points:region|=(df['timestamp'].to_numpy()>=times[max(0,point-60)])&(df['timestamp'].to_numpy()<times[min(len(times)-1,point+59)]+1)
   classes={};http=collections.Counter();lex=collections.Counter();parsed=[];missing=0;unknown_http_like=0;entities=collections.Counter()
   for ix in np.flatnonzero(region):
    row=df.iloc[ix];entity=str(row['container_name']);entities[entity]+=1;msg=row['message']
    if pd.isna(msg):missing+=1;continue
    assert isinstance(msg,str);tpl=template(msg);tkey=hashlib.sha256(tpl.encode()).hexdigest();hits=[x.lower() for x in LEX.findall(msg)];lex.update(hits)
    if tkey not in classes:classes[tkey]={'template':tpl,'rows':0,'entities':collections.Counter(),'lexical_indicator_counts':collections.Counter(),'first_source_row':int(ix),'first_message_sha256':hashlib.sha256(msg.encode()).hexdigest()}
    c=classes[tkey];assert c['template']==tpl;c['rows']+=1;c['entities'][entity]+=1;c['lexical_indicator_counts'].update(hits)
    m=ACCESS.search(msg)
    if m:
     d=m.groupdict();status=int(d['status']);assert 100<=status<=599
     sig=(entity,d['method'],d['target'],d['protocol'],status);http[sig]+=1
     parsed.append({'source_row':int(ix),'timestamp':int(row['timestamp']),'container_name':entity,'method':d['method'],'target':d['target'],'protocol':d['protocol'],'status':status,'body_bytes_literal':int(d['bytes']) if d['bytes']!='-' else None,'message_sha256':hashlib.sha256(msg.encode()).hexdigest()})
    elif re.search(r'HTTP/\d',msg):unknown_http_like+=1
   assert sum(x['rows'] for x in classes.values())+missing==int(region.sum()) and sum(http.values())==len(parsed)
   statuscounts=collections.Counter(str(x['status']) for x in parsed);families=collections.Counter(str(x['status']//100)+'xx' for x in parsed)
   npz=w.OUT/(oid+'--http-access-observed.npz');assert not npz.exists()
   np.savez_compressed(npz,source_row=np.array([x['source_row'] for x in parsed],dtype=np.int64),timestamp=np.array([x['timestamp'] for x in parsed],dtype=np.int64),container_name=np.array([x['container_name'] for x in parsed],dtype=str),method=np.array([x['method'] for x in parsed],dtype=str),target=np.array([x['target'] for x in parsed],dtype=str),protocol=np.array([x['protocol'] for x in parsed],dtype=str),status=np.array([x['status'] for x in parsed],dtype=np.int64),body_bytes_literal=np.array([x['body_bytes_literal'] if x['body_bytes_literal'] is not None else -1 for x in parsed],dtype=np.int64),message_sha256=np.array([x['message_sha256'] for x in parsed],dtype=str))
   v={'status':'PASS','opaque_id':oid,'source_logs':{'path':str(q),'bytes':q.stat().st_size,'sha256':w.sha(q)},'source_columns':df.columns.tolist(),'region_points':points,'region_rows':int(region.sum()),'missing_messages':missing,'observed_container_counts':dict(entities),'all_template_classes':classes,'template_grouping':'Timestamp/UUID/hexIDs/numbers replaced for grouping only; HTTP status/target and lexical indicators decoded from original message separately. Every class retained.','literal_lexical_indicator_counts':dict(lex),'http_access':{'parsed_rows':len(parsed),'status_counts':dict(statuscounts),'status_family_counts':dict(families),'entities':dict(collections.Counter(x['container_name'] for x in parsed)),'signatures':[{'container_name':sig[0],'method':sig[1],'target':sig[2],'protocol':sig[3],'status':sig[4],'rows':n} for sig,n in sorted(http.items())],'unparsed_HTTP_like_rows':unknown_http_like,'parsed_row_index_artifact':{'file':npz.name,'bytes':npz.stat().st_size,'sha256':w.sha(npz)},'interpretation':'Literal status in observed access messages is available outcome for these recorded HTTP requests, not independent system health/clean-negative/onset/faultgroundtruth.'},'mapping_limits':{'service':'literal container_name; verified canonical alias absent','traceID_spanID':'no structured fields in source schema, no automatic correlation from container/time','status':'only access-message parse, no structured status field across all rows','time':'source timestamp in seconds; embedded clocks/timezone may differ, no offset/completeness evidence','missing':'no collector sampling/drop/heartbeat completeness, fault activation/end or independent clean-negative truth'},'body_wall_s':time.perf_counter()-start};w.write(name,v)
  catalog.append({'file':name,'bytes':dest.stat().st_size,'sha256':w.sha(dest)});w.emit({'log_semantics_case':ci+1,'status':v['status'],'rows':v.get('region_rows'),'templates':len(v.get('all_template_classes',{})),'HTTP':v.get('http_access',{}).get('parsed_rows')})
 w.write('log-semantics-catalog-001.json',{'status':'COMPLETE','files':catalog});w.emit({'log_semantics':'COMPLETE','cases':len(catalog)})
if __name__=='__main__':run()
