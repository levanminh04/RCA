"""Literal serialized application outcomes, no physical labels or engine change."""
import collections,hashlib,importlib.util,json,pathlib,re,time
import numpy as np,pandas as pd
sp=importlib.util.spec_from_file_location('l',pathlib.Path(__file__).with_name('log_correlation.py'))
# Do not import executable correlation module; reuse the frozen worker only.
sp=importlib.util.spec_from_file_location('w',pathlib.Path(__file__).with_name('worker-v3.py'));w=importlib.util.module_from_spec(sp);sp.loader.exec_module(w)
MARKER=re.compile(r'\bResponse\(')
APPLICATION=re.compile(r'\bResponse\(status=([+-]?\d+),\s*msg=(.*?),\s*data=',re.S)
SPRING=re.compile(r'\]\s+([A-Za-z0-9_.$]+)\s*:\s*(.*)',re.S)
SERIALIZED_HTTP=re.compile(r'<([1-5]\d\d),$')
HEADERS=re.compile(r'x-application-context=\[([^\]]+)\]',re.I)
CORR=re.compile(r'\b(trace[-_ ]?id|span[-_ ]?id|request[-_ ]?id|correlation[-_ ]?id|x-b3-traceid|x-b3-spanid|traceparent)\s*[:=]\s*[\'\"]?([A-Za-z0-9-]+)',re.I)
def decode(msg):
 markers=[m.start() for m in MARKER.finditer(msg)];found=[];parsed_starts=set()
 spring=SPRING.search(msg);logger=spring.group(1) if spring else None;payloadstart=spring.start(2) if spring else None
 for m in APPLICATION.finditer(msg):
  if 'Response(' in m.group(2):continue
  parsed_starts.add(m.start());prefix=msg[:m.start()];http=SERIALIZED_HTTP.search(prefix)
  # A returned status must begin a literal ResponseEntity <code,Response
  # token within the logger payload, not arbitrary preceding digits.
  returned=int(http.group(1)) if http and (payloadstart is not None and http.start()>=payloadstart) else None
  operation=msg[payloadstart:m.start()] if payloadstart is not None else None
  found.append({'marker_offset':m.start(),'application_status_literal':int(m.group(1)),'msg_literal':m.group(2),'serialized_HTTP_code_literal':returned,'logger_literal':logger,'operation_prefix_literal':operation,'application_context_header_literals':HEADERS.findall(msg),'correlation_key_literals':CORR.findall(msg),'multiple_Response_markers_in_message':len(markers)>1,'status_semantics':'UNKNOWN_APPLICATION_CONVENTION; no status0/1 success/failure mapping','serialized_HTTP_semantics':'literal serialized ResponseEntity code; not verified wire response or invocation join' if returned is not None else 'N/A_NOT_CERTIFIED_SERIALIZED_HTTP_GRAMMAR'})
 return found,[x for x in markers if x not in parsed_starts],markers
def fixture():
 checks=[]
 a,b,c=decode('2024-01-24 INFO [thread] seat.service.Impl : Get result is : <200,Response(status=0, msg=Seat is Null., data=null),{x-application-context=[ts-order-other-service:123]}')
 assert len(a)==1 and not b and a[0]['application_status_literal']==0 and a[0]['msg_literal']=='Seat is Null.' and a[0]['serialized_HTTP_code_literal']==200;checks.append('serialized_HTTP_exact_literal_no_appstatus_semantics')
 a,b,c=decode('INFO [thread] travel.Impl : HTTPnumber200 Response(status=1, msg=Success, data=null)')
 assert a[0]['serialized_HTTP_code_literal'] is None;checks.append('arbitrary_HTTPnumber_not_decoded')
 a,b,c=decode('Response(status=1, msg=outer Response(status=0, msg=inner, data=null), data=x)')
 assert len(c)==2 and len(a)==0 and len(b)==2;checks.append('nested_ambiguous_unparsed_preserved')
 a,b,c=decode('Response(status=true, msg=Success, data=null)')
 assert not a and len(b)==1;checks.append('noninteger_appstatus_NA')
 return checks
def run():
 checks=fixture();w.write('backend-status-fixtures-001.json',{'status':'PASS','checks':checks});rows=[];pins=[]
 for ci,item in enumerate(w.S['cases']):
  oid=item['opaque_id'];name=oid+'--backend-status.json';destination=w.OUT/name;start=time.perf_counter()
  if 'logs.parquet' not in item['files']:
   v={'status':'N/A_MISSING_CHANNEL','opaque_id':oid};w.write(name,v);rows.append(v);continue
  semantics=w.OUT/(oid+'--log-semantics.json');sv=json.loads(semantics.read_text());assert sv['status']=='PASS'
  logpath=w.raw_path(item,'logs.parquet');logs=pd.read_parquet(logpath);assert set(logs.columns)=={'timestamp','container_name','message'};_,z=w.input_arrays(oid);times=z['times'];region=np.zeros(len(logs),bool)
  for point in sv['region_points']:region|=(logs['timestamp'].to_numpy()>=times[max(0,point-60)])&(logs['timestamp'].to_numpy()<times[min(len(times)-1,point+59)]+1)
  assert int(region.sum())==sv['region_rows'];records=[];unparsed=[];markers=0;missing=0;rows_with=[];coarse=collections.Counter();msgstatus=collections.Counter();httpstatus=collections.Counter();loggercounts=collections.Counter();entities=collections.Counter();multi=0
  # itertuples prevents a large per-row pandas object allocation.
  for ix,timestamp,container,msg in logs.loc[region].itertuples(index=True,name=None):
   if pd.isna(msg):missing+=1;continue
   found,unknown,allmarkers=decode(msg);markers+=len(allmarkers)
   if found:rows_with.append(int(ix))
   if len(allmarkers)>1:multi+=1
   digest=hashlib.sha256(msg.encode()).hexdigest() if allmarkers else None
   for j,entry in enumerate(found):
    record={'source_row':int(ix),'source_time_seconds':int(timestamp),'container_name_literal':str(container),'occurrence_in_row':j,'message_sha256':digest,**entry};records.append(record)
    entities[str(container)]+=1;loggercounts[entry['logger_literal'] or 'N/A_UNPARSED_LOGGER']+=1;msgstatus[(str(container),entry['application_status_literal'],entry['msg_literal'])]+=1
    if entry['serialized_HTTP_code_literal'] is not None:httpstatus[str(entry['serialized_HTTP_code_literal'])]+=1
   for offset in unknown:unparsed.append({'source_row':int(ix),'source_time_seconds':int(timestamp),'container_name_literal':str(container),'marker_offset':offset,'message_sha256':digest,'reason':'N/A_APPLICATION_GRAMMAR_NOT_MATCHED_OR_NESTED_AMBIGUOUS','raw_marker_excerpt':msg[offset:offset+160]})
  assert markers==len(records)+len(unparsed)
  counts=collections.Counter(str(x['application_status_literal']) for x in records);assert sum(counts.values())==len(records)
  artifact=w.OUT/(oid+'--backend-status-literals.json.gz');assert not artifact.exists();import gzip
  artifact.write_bytes(gzip.compress((json.dumps({'records':records,'unparsed_markers':unparsed},ensure_ascii=False,separators=(',',':'))+'\n').encode(),mtime=0))
  windows=[];rt=np.array([x['source_time_seconds'] for x in records],dtype=np.int64);ur=np.array(rows_with,dtype=np.int64)
  for point in sv['region_points']:
   for width in [10,30,60]:
    for side,lo,hi in [('before',max(0,point-width),point),('after',point,min(len(times),point+width))]:
     mask=(rt>=times[lo])&(rt<times[hi-1]+1) if hi>lo else np.zeros(len(rt),bool);selected=[records[j] for j in np.flatnonzero(mask)]
     windows.append({'point':point,'width':width,'side':side,'lo':lo,'hi_exclusive':hi,'decoded_occurrences':len(selected),'distinct_source_log_rows':len(set(x['source_row'] for x in selected)),'application_status_literal_counts':dict(collections.Counter(str(x['application_status_literal']) for x in selected)),'serialized_HTTP_literal_counts':dict(collections.Counter(str(x['serialized_HTTP_code_literal']) for x in selected if x['serialized_HTTP_code_literal'] is not None))})
  v={'status':'PASS','opaque_id':oid,'region_rows':int(region.sum()),'message_missing_rows':missing,'source_logs':sv['source_logs'],'source_semantics':{'file':semantics.name,'bytes':semantics.stat().st_size,'sha256':w.sha(semantics)},'Response_marker_count':markers,'decoded_application_status_occurrences':len(records),'unparsed_Response_markers':len(unparsed),'distinct_rows_with_decoded_application_status':len(set(rows_with)),'multiple_Response_marker_rows':multi,'application_status_literal_counts':dict(counts),'serialized_HTTP_code_literal_counts':dict(httpstatus),'container_occurrence_counts':dict(entities),'logger_occurrence_counts':dict(loggercounts),'application_status_msg_signatures':[{'container_name_literal':k[0],'application_status_literal':k[1],'msg_literal':k[2],'occurrences':n} for k,n in sorted(msgstatus.items())],'literal_records_artifact':{'file':artifact.name,'bytes':artifact.stat().st_size,'sha256':w.sha(artifact)},'windows':windows,'correlation_key_occurrences':sum(bool(x['correlation_key_literals']) for x in records),'interpretation':'These are serialized application status/msg and optional ResponseEntity HTTP code occurrences in observed backend log messages, not request counts, clean-negative labels, verified span outcomes or physical root cause. Application code semantics remains UNKNOWN.','body_wall_s':time.perf_counter()-start};w.write(name,v);rows.append(v);pins.append({'file':name,'bytes':destination.stat().st_size,'sha256':w.sha(destination)});w.emit({'backend_case':ci+1,'rows':v['region_rows'],'parsed_occurrences':len(records),'unparsed_markers':len(unparsed),'serialized_HTTP':dict(httpstatus),'wall_s':v['body_wall_s']})
 total=collections.Counter();http=collections.Counter()
 for v in rows:total.update(v.get('application_status_literal_counts',{}));http.update(v.get('serialized_HTTP_code_literal_counts',{}))
 w.write('backend-status-summary-001.json',{'status':'COMPLETE','cases':rows,'source_files':pins,'application_status_literal_counts':dict(total),'serialized_HTTP_code_literal_counts':dict(http),'physical_status':'UNKNOWN_APPLICATION_SEMANTICS_AND_UNVERIFIED_INVOCATION_JOIN; recorded serialized outcomes available, independent operational truth still missing'});w.emit({'backend_status':'COMPLETE','cases':len(rows),'application_status_literals':dict(total),'serialized_HTTP_literals':dict(http)})
if __name__=='__main__':run()
