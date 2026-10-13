"""All decoded occurrence literals audited against raw source positions."""
import collections,gzip,hashlib,importlib.util,json,pathlib,re
import numpy as np,pandas as pd
sp=importlib.util.spec_from_file_location('w',pathlib.Path(__file__).with_name('worker-v3.py'));w=importlib.util.module_from_spec(sp);sp.loader.exec_module(w)
v=json.loads((w.OUT/'backend-status-summary-001.json').read_text());rows=[];pins=[];total=collections.Counter();http=collections.Counter();checks=0
for ci,item in enumerate(w.S['cases']):
 oid=item['opaque_id'];summary=next(x for x in v['cases'] if x['opaque_id']==oid)
 if summary['status']=='N/A_MISSING_CHANNEL':assert 'logs.parquet' not in item['files'];rows.append({'opaque_id':oid,'status':'N/A_MISSING_CHANNEL'});continue
 artifact=w.OUT/summary['literal_records_artifact']['file'];assert artifact.stat().st_size==summary['literal_records_artifact']['bytes'] and w.sha(artifact)==summary['literal_records_artifact']['sha256'];values=json.loads(gzip.decompress(artifact.read_bytes()));logs=pd.read_parquet(w.raw_path(item,'logs.parquet'));markers=0;byrow=collections.Counter();status=collections.Counter();codes=collections.Counter();hashes={}
 for entry in values['records']:
  ix=entry['source_row'];row=logs.iloc[ix];msg=row['message'];h=hashes.setdefault(ix,hashlib.sha256(msg.encode()).hexdigest());assert h==entry['message_sha256'];assert int(row['timestamp'])==entry['source_time_seconds'] and str(row['container_name'])==entry['container_name_literal'];offset=entry['marker_offset'];literal=msg[offset:];prefix='Response(status='+str(entry['application_status_literal'])+',';assert literal.startswith(prefix)
  # Exact serialized substring, keeping whitespace between comma and msg.
  m=re.match(r'Response\(status=([+-]?\d+),\s*msg=(.*?),\s*data=',literal,re.S);assert m and int(m.group(1))==entry['application_status_literal'] and m.group(2)==entry['msg_literal'];assert 'Response(' not in entry['msg_literal']
  if entry['serialized_HTTP_code_literal'] is not None:assert msg[:offset].endswith('<'+str(entry['serialized_HTTP_code_literal'])+',');codes[str(entry['serialized_HTTP_code_literal'])]+=1
  if entry['logger_literal'] is not None:assert entry['logger_literal'] in msg[:offset] and entry['operation_prefix_literal'] in msg[:offset]
  byrow[ix]+=1;status[str(entry['application_status_literal'])]+=1;checks+=1
 for entry in values['unparsed_markers']:
  row=logs.iloc[entry['source_row']];msg=row['message'];assert msg[entry['marker_offset']:].startswith('Response(') and hashlib.sha256(msg.encode()).hexdigest()==entry['message_sha256']
 assert summary['Response_marker_count']==len(values['records'])+len(values['unparsed_markers']) and summary['decoded_application_status_occurrences']==len(values['records']) and summary['distinct_rows_with_decoded_application_status']==len(byrow) and summary['application_status_literal_counts']==dict(status) and summary['serialized_HTTP_code_literal_counts']==dict(codes)
 windows=0;timestamps=np.array([x['source_time_seconds'] for x in values['records']]);_,z=w.input_arrays(oid)
 for window in summary['windows']:
  lo,hi=window['lo'],window['hi_exclusive'];selected=np.flatnonzero((timestamps>=z['times'][lo])&(timestamps<z['times'][hi-1]+1)) if hi>lo else []
  assert len(selected)==window['decoded_occurrences'] and len(set(values['records'][j]['source_row'] for j in selected))==window['distinct_source_log_rows'];assert dict(collections.Counter(str(values['records'][j]['application_status_literal']) for j in selected))==window['application_status_literal_counts'];windows+=1
 total.update(status);http.update(codes);rows.append({'opaque_id':oid,'status':'PASS','exact_source_occurrence_checks':len(values['records']),'distinct_log_rows':len(byrow),'window_checks':windows,'unparsed_markers':len(values['unparsed_markers'])});pins.append({'file':artifact.name,'bytes':artifact.stat().st_size,'sha256':w.sha(artifact)})
assert v['application_status_literal_counts']==dict(total) and v['serialized_HTTP_code_literal_counts']==dict(http)
w.write('backend-source-verification-001.json',{'status':'PASS_ALL_LITERAL_SOURCE_AND_COUNTS','cases':rows,'source_files':pins,'exact_source_occurrence_checks':checks,'application_status_literal_counts':dict(total),'serialized_HTTP_code_literal_counts':dict(http),'scope':'Raw row/position/status/msg/hash/time/container and totals/windows verified. No independent audit, unknown status convention retained, no certified wire/invocation/health interpretation.'});w.emit({'backend_source_verification':'PASS','exact_occurrences':checks,'HTTP_literals':dict(http)})
