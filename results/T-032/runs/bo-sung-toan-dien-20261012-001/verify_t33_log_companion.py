"""Root takeover check of received decoder outputs; distinct from independent audit."""
import pathlib,json,hashlib,collections,sys
import numpy as np
P=pathlib.Path('results/T-033/runs/bo-sung-toan-dien-20261012-001/t33');rows=[];allstatuses=collections.Counter();windows=0
h=json.loads((P/'root-companions-receipt-001.json').read_text(encoding='utf-8'))
for rel,m in h.items():
 f=P/rel;assert f.stat().st_size==m['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==m['sha256'],rel
s=json.loads((P/'log-semantics-summary-001.json').read_text(encoding='utf-8'));corr=json.loads((P/'log-correlation-summary-001.json').read_text(encoding='utf-8'))
for case in s['cases']:
 oid=case['opaque_id']
 if case['status']=='N/A_MISSING_CHANNEL':rows.append({'opaque_id':oid,'status':case['status']});continue
 v=json.loads((P/case['source']).read_text(encoding='utf-8'));assert sum(c['rows'] for c in v['all_template_classes'].values())+v['missing_messages']==v['region_rows']
 a=np.load(P/v['http_access']['parsed_row_index_artifact']['file'],allow_pickle=False);cnt=collections.Counter(str(i) for i in a['status']);families=collections.Counter(str(i//100)+'xx' for i in a['status']);assert dict(cnt)==v['http_access']['status_counts']==case['HTTP_access']['status_counts'];assert dict(families)==v['http_access']['status_family_counts'];assert len(a['status'])==v['http_access']['parsed_rows'];allstatuses.update(cnt)
 for win in case['windows']:
  assert sum(win['HTTP_status_counts'].values())==win['observed_HTTP_request_rows'];assert sum(win['HTTP_status_family_counts'].values())==win['observed_HTTP_request_rows'];assert sum(win['container_counts'].values())==win['observed_HTTP_request_rows'];windows+=1
 cr=next(x for x in corr['cases'] if x['opaque_id']==oid);assert cr['HTTP_observed_rows']==len(a['status']);assert sum(cr['same_literal_entity_same_second_coarse_candidate_histogram'].values())==len(a['status'])
 rows.append({'opaque_id':oid,'status':'PASS','region_rows':v['region_rows'],'HTTP_rows':len(a['status']),'template_classes':len(v['all_template_classes']),'explicit_correlation_key_rows':len(cr['explicit_correlation_ID_rows']),'known_correlation_token_without_parse_rows':len(cr['correlation_token_without_parse_source_rows'])})
assert dict(allstatuses)==s['all_HTTP_status_counts_in_union_regions'];assert len(rows)==30
out={'status':'PASS_ROOT_SOURCE_AND_CONSERVATION','received_hashes':len(h),'cases':rows,'HTTP_status_counts':dict(allstatuses),'windows_checked':windows,'scope':'Root count/hash/array checks, not independent GPT6.1 audit or certified raw-message semantic/invocation join. Overlapping windows are not independent; INFO/status200 not system health or negative truth.'}
target=P/'root-log-companion-verification-001.json';assert not target.exists();target.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in out.items() if k!='cases'},ensure_ascii=False))
