"""Read saved source records and all canonical comparisons; no graph mutation."""
import sys
sys.dont_write_bytecode=True
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]; B=ROOT/'results/T-039'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def write(p,x):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

run=B/'runs'/(sys.argv[1] if len(sys.argv)>1 else 'phan-tich-002');run.mkdir(exist_ok=False)
summary=read(B/'doi-chieu/tong-hop.json');doc=read(B/'ban-ghi.json');mapping=read(B/'mapping.json')
assert read(B/'runs/thuc-thi-snapshot-004/verification.json')['status']=='PASS'
reg=read(B/'nguon.json'); sources={s['id']:s for s in reg['sources']}
for s in sources.values():assert sha(ROOT/s['path'])==s['sha256']
graphs={level:read(B/'do-thi'/file) for level,file in [('entity','thuc-the.json'),('operation','thao-tac.json')]}
mapidx={(x['level'],x['original']):x for x in mapping['rows']}
records={x['id']:x for x in doc['relations']}
chains={};excluded={};cells=[];node_status=Counter()
for row in summary['rows']:
    result=read(ROOT/row['output']);v=result['views']['endpoints'];t=read(ROOT/row['path'])
    statuses=Counter(n['status'] for n in result['nodes']['trace']);node_status.update(statuses)
    cells.append(dict(input=row['path'],output=row['output'],opaque_id=row['opaque_id'],level=row['level'],window=row['window'],interval_ns=row['interval_ns'],raw_trace_edges=len(t['edges']),eligible_trace_edges=sum(len(x['members']) for x in v['members']['trace']),excluded_trace_edges=len(v['exclusions']['trace']),excluded_reasons=dict(Counter(x['reason'] for x in v['exclusions']['trace'])),mapping_node_statuses=dict(statuses),views=row['views']))
    for group in ['intersection','static_only','trace_only']:
        for key in v[group]:
            ident=canon([row['level'],key])
            if ident not in chains:
                sm=[x for x in v['members']['static'] if x['key']==key]
                tm=[x for x in v['members']['trace'] if x['key']==key]
                mids=sorted({record for x in sm for member in x['members'] for record in member['original']['record_ids']})
                chains[ident]=dict(level=row['level'],key=key,static_members=sm,source_records=[records[k] for k in mids],first_trace_members=tm,occurrences={})
            chain=chains[ident];chain['occurrences'].setdefault(group,[]).append(dict(opaque_id=row['opaque_id'],window=row['window'],output=row['output']))
            if not chain['first_trace_members']:
                chain['first_trace_members']=[x for x in v['members']['trace'] if x['key']==key]
    for x in v['exclusions']['trace']:
        edge=x['original'];ident=canon([row['level'],edge['source'],edge['target'],x['reason']])
        if ident not in excluded:
            endpoints={}
            for end in ['source','target']:
                ident2=edge[end];level='operation' if ident2 in dict(t.get('belongs_to',[])) else 'entity'
                endpoints[end]=mapidx.get((level,ident2))
            excluded[ident]=dict(level=row['level'],reason=x['reason'],original_example=edge,endpoint_mappings=endpoints,occurrences=[])
        excluded[ident]['occurrences'].append(dict(output=row['output'],edge_index=x['index'],opaque_id=row['opaque_id'],window=row['window']))

def key(level,s,t):return canon([level,[s,t,None,None]])
def op(owner,name):return canon([owner,'hipstershop.'+name])
def refs(level,s,t):
    k=key(level,s,t);assert k in chains,(level,s,t)
    return k
def source(p,l):
    sid='OB:'+p;assert sid in sources
    return dict(source_id=sid,path=sources[sid]['path'],locator=l,sha256=sources[sid]['sha256'])

groups=[
 dict(id='G1',subject='Entity RPC paths and window-specific absences',classification='FACT + OPEN physical cause',
      observations=['64/66 entity graphs have eligible13/intersection13; two A graphs have11. Same opaque ID N/full contain checkout→email/payment. checkout→currency is static-only in all66.'],
      mismatch_keys=[refs('entity','checkoutservice',t) for t in ['currencyservice','emailservice','paymentservice']],
      matched_counterparts=[refs('entity','checkoutservice',t) for t in ['cartservice','shippingservice','productcatalogservice']],
      source=[source('src/checkoutservice/main.go','L178–239;L451–483'),source('src/frontend/rpc.go','RPC client calls')],
      mechanism='Graph set changes are observed within saved dev windows. Code Convert uses context.TODO at main.go471; this is a candidate context-propagation difference, not proof that this code generated dataset or sole cause. Other checkout RPC calls with propagated ctx are matched at entity level.',
      competing=dict(revision='OPEN: no image/build/deployment link',alias='Exact entity identities verified for this source; still deployment scope conditional',domain_window='SUPPORTED observed difference between A and N/full; full is not whole day',branch='Code has request/error branches; actual execution/calls not known from graph alone',incomplete_static_source='Code call exists, so absence of source record not explanation for this key; external runtime version OPEN',missing_telemetry='Unresolved; no raw-span/export lineage permission/evidence',conversion_error='Set/members/interval checks PASS; graph producer/runtime conversion not proven complete'),
      needed='Exact app/deployment/export lineage and authorized call/context observations before assigning physical missing-edge cause.'),
 dict(id='G2',subject='Source data dependencies versus service-owned SQL spans',classification='FACT + conditional source mechanism',
      observations=['Static ad→logical DB, productcatalog→logical DB, cart→Redis are static-only across entity graphs. Three observed SQL operation names have no source literal candidate; do not map sql.rows into a database entity. DB signals shared on instance retain one binding per logical DB.'],
      mismatch_keys=[refs('entity','adservice','mysql/addatabase'),refs('entity','productcatalogservice','mysql/Productdb'),refs('entity','cartservice','redis-cart')],
      matched_counterparts=[refs('entity','frontend','productcatalogservice'),refs('entity','frontend','cartservice'),refs('operation',op('productcatalogservice','ProductCatalogService/ParseCatalog'),op('productcatalogservice','ProductCatalogService/ReadCatalog'))],
      source=[source('src/adservice/src/main/java/hipstershop/AdService.java','L237–257'),source('src/productcatalogservice/server.go','L55–91;L188–214;L238–298'),source('src/cartservice/src/Startup.cs','Redis vs Local branch'),source('src/cartservice/src/cartstore/RedisCartStore.cs','Redis calls/health/init')],
      mechanism='Source DB/cache endpoint and logical DB name are explicit. Saved operation IDs keep owner application, so SQL spans alone do not supply an independently identified DB/cache component under current mapping. This distinguishes source data capability from trace service-call endpoints; it does not show why all datastore telemetry is absent.',
      competing=dict(revision='OPEN',alias='SQL instrumentation→logical DB identity/operation unverified; cannot turn owner into resource',domain_window='No DB/cache node in all authorized saved graphs; says nothing about whole day',branch='Redis mode conditional on REDIS_ADDR; source configured Redis but actual runtime not verified',incomplete_static_source='Source records exist; exact library/export schema OPEN',missing_telemetry='Cannot separate unrecorded, unexported, unmapped or excluded data using saved graph alone',conversion_error='T039 preserves unknown owner and refuses unsupported aliases; upstream adapter attributes need separately authorized evidence'),
      needed='OTel DB/cache attributes, endpoint namespace and exporter field mapping; logical DB→instance→host validity intervals.'),
 dict(id='G3',subject='Manual span literal versus code function boundaries in AdService',classification='FACT source behavior; CANDIDATE runtime explanation',
      observations=['AdImpl/getAds is an explicit renamed @WithSpan span and maps to canonical GetAds. createAdsMap has no @WithSpan; it calls Span.current().updateName. getAdsByCategory/getRandomAds call createAdsMap before renaming their current span. createAdsMap source operation is inventory capability but not proven independent span.'],
      mismatch_keys=[refs('operation',op('adservice','AdService/getAdsByCategory'),op('adservice','AdService/createAdsMap')),refs('operation',op('adservice','AdService/getRandomAds'),op('adservice','AdService/createAdsMap')),refs('operation',op('adservice','AdService/createAdsMap'),'mysql/addatabase')],
      matched_counterparts=[refs('operation',op('adservice','AdService/GetAds'),op('adservice','AdService/getAdsByCategory')),refs('operation',op('adservice','AdService/GetAds'),op('adservice','AdService/getRandomAds'))],
      source=[source('src/adservice/src/main/java/hipstershop/AdService.java','L116–121;L169–173;L190–197;L227–257')],
      mechanism='Under this source, helper rename changes current span rather than constructing a helper span. Later category/random rename can overwrite that name. Thus function nesting and span nesting can differ even without lost telemetry. Saved SQL edges from category/random are excluded by SQL mapping, not silently declared static mismatch.',
      competing=dict(revision='OPEN: source mechanism not dataset attribution',alias='Handler explicit literal verified; createAdsMap literal exists but no observed node',domain_window='No createAdsMap node in union authorized operation graphs, not universal runtime absence',branch='Context/random paths conditional; both corresponding caller→helper keys observed in some authorized windows',incomplete_static_source='Agent bytecode/filter/library may alter span behavior; not fully inspected',missing_telemetry='Not established; no need to assume loss to explain source function/span discrepancy',conversion_error='Static source calls are intentionally not span-parent; source records/context preserved; independent key checks PASS'),
      needed='Exact runtime agent/source link and span naming lifecycle to select operation-level modeling in P6.'),
 dict(id='G4',subject='Explicit manual spans, generated RPC names and mapping exclusions',classification='FACT comparison eligibility; aliases OPEN',
      observations=['Observed union55 operation nodes:20 verified by explicit runtime literal,32 unverified candidates,3 SQL unmapped. All 66 operation graphs are processed, including raw edges excluded from eligible T. Most63 raw edges reduce to10 eligible; one A reduces9. Trace_fraction1 measures this selected eligible subset.'],
      mismatch_keys=[refs('operation',op('recommendationservice','RecommendationService/ListRecommendations'),op('recommendationservice','ProductCatalogService/ListProducts')),refs('operation',op('frontend','ProductCatalogService/ListProducts'),op('productcatalogservice','ProductCatalogService/ListProducts'))],
      matched_counterparts=[refs('operation',op('shippingservice','ShippingService/CreateQuoteFromCount'),op('shippingservice','ShippingService/CreateQuoteFromFloat')),refs('operation',op('checkoutservice','CheckoutService/PrepareOrderItemsAndShippingQuoteFromCart'),op('checkoutservice','CheckoutService/GetUserCart'))],
      source=[source('src/recommendationservice/recommendation_server.py','L63–84;L98–105'),source('src/recommendationservice/demo_pb2_grpc.py','L143–158'),source('src/frontend/main.go','L212'),source('src/shippingservice/main.go','L285–301'),source('src/checkoutservice/main.go','L275–306;L432–473')],
      mechanism='Entity identity and exact explicit runtime span name require separate evidence. Generated gRPC method path establishes invocation capability/owner, not final instrumentation span name. Same name text without literal proof remains unverified; six slash/grpc prefix candidates are explicit scoped proposals, not automatic normalization. Comparison excludes edges whose endpoint mapping is unverified/unmapped before set intersection.',
      competing=dict(revision='OPEN for every mapping',alias='Exact runtime literals supported20; remaining names not verified even when syntax identical',domain_window='All current dev graphs compared; no new window',branch='No exclusion is evidence branch failed to run; excluded raw edges remain saved',incomplete_static_source='Library naming source/exact deployed version absent',missing_telemetry='Excluded edges are present graph data, so cannot call these telemetry missing merely due fraction',conversion_error='Owner-conflict oracle/independent membership checks; source matching not optimized to eligible fraction'),
      needed='Exact selected library naming/Health binding and binary/build identity, before promoting candidates. Do not create SQL fake operations.'),
 dict(id='G5',subject='Client/browser/loadgenerator and exporter domains',classification='FACT source scope; runtime OPEN',
      observations=['Static-only loadgenerator→frontend, web-client→frontend and two browser stylesheets have source locators. Mysql exporter→mysql exists only in exporter deployment variant. gstatic preconnect kept as inventory hint with no HTTP edge. These are not unseen app-to-app RPC claims.'],
      mismatch_keys=[refs('entity','loadgenerator','frontend'),refs('entity','web-client','frontend'),refs('entity','web-client','fonts.googleapis.com'),refs('entity','web-client','stackpath.bootstrapcdn.com'),refs('entity','mysqld-exporter','mysql')],
      matched_counterparts=[refs('entity','frontend','adservice'),refs('entity','frontend','shippingservice')],
      source=[source('src/loadgenerator/locustfile.py','UserBehavior/tasks and requests'),source('src/frontend/templates/header.html','L26–30'),source('kubernetes-manifests/mysql_exporter.yaml','L38–55'),source('kubernetes-manifests/start_with_istio_exporter.sh','L3–4'),source('kubernetes-manifests/start_demo_with_istio.sh','L3–4')],
      mechanism='Inventory must include source scopes beyond traced services, while comparison remains dev-adapter. Exporter variant, resource browser requests and external resource hints remain conditional; their static-only status cannot imply internal RPC collector failure.',
      competing=dict(revision='Source/deployment image link OPEN',alias='No forced browser/exporter alias to application service',domain_window='SUPPORTED structural scope difference in record contexts; actual sampling boundaries still OPEN',branch='Exporter variants not unioned as simultaneous deployment; browser fetch may not occur',incomplete_static_source='External CSS/Redis exporter defaults/collector config absent; not invented',missing_telemetry='Unresolved and not inferred from external/static-only scope',conversion_error='Incorrect gstatic edge removed during source audit; records/graph now match allowed source relation semantics'),
      needed='Effective deployment/browser/load profile and collector scope only if runtime coverage claim is requested.'),
 dict(id='G6',subject='Operation difference isolated to one saved A window',classification='FACT per-cell observation; cause OPEN',
      observations=['PrepOrderItems→ConvertCurrency is static-only in one A graph, matched in N/full same opaque ID and other operation graphs. No average is used to hide this cell.'],
      mismatch_keys=[refs('operation',op('checkoutservice','CheckoutService/PrepOrderItems'),op('checkoutservice','CheckoutService/ConvertCurrency'))],
      matched_counterparts=[refs('operation',op('checkoutservice','CheckoutService/PrepareOrderItemsAndShippingQuoteFromCart'),op('checkoutservice','CheckoutService/ConvertCurrency')),refs('operation',op('checkoutservice','CheckoutService/PrepOrderItems'),op('checkoutservice','CheckoutService/ConvertCurrency'))],
      source=[source('src/checkoutservice/main.go','prepOrderItems and convertCurrency call path')],
      mechanism='Same source mapping and normalization yield match in N/full, absence in one A. This controls mapping policy for the comparison but does not identify code execution, sampling, failure or branch cause.',
      competing=dict(revision='Same saved-case graph reference does not resolve deployment provenance',alias='Both endpoints verified explicit literals; mapping policy not changed between windows',domain_window='SUPPORTED observable A vs N/full edge-set difference',branch='Request composition/error return/empty items plausible but not observed here',incomplete_static_source='Call record present; actual runtime revision OPEN',missing_telemetry='Still possible; no evidence separates it from unexecuted branch',conversion_error='Saved output correctly reflects saved graph edge absence under identical mapping; source graph production remains conditional'),
      needed='Authorized request/span sequence and source revision to attribute this per-window absence.'),
 dict(id='G7',subject='Typed unknown, source independence and Node identity',classification='FACT contract behavior; external lineage OPEN',
      observations=['Typed excludes all eligible trace edges as unknown_type, yielding trace denominator0 and null fraction. Unknown type is not known wrong type. Source NodeName from Kubernetes spec.nodeName cannot alone identify dataset Node. Producer of daily Source/Target/Node was not found in seven Python source files audited; not whole repo absence.'],
      mismatch_keys=[],matched_counterparts=[refs('entity','frontend','productcatalogservice')],
      source=[source('kubernetes-manifests/productcatalogservice.yaml','NODE_NAME valueFrom spec.nodeName')],
      mechanism='Endpoints comparison deliberately removes type; typed comparison refuses unknown. Daily metadata might share trace provenance; alarm.NetworkP90 code derives from trace. None proves independently collected host/network measurements. Lineage.md has exact Nezha source locators.',
      competing=dict(revision='OPEN',alias='Resource schema/Node mapping OPEN',domain_window='Daily metadata domain not equivalent to dev-adapter windows',branch='Not resolved from type/metadata',incomplete_static_source='Exporter/collector producer not in audited files, exact missing sources identified',missing_telemetry='Cannot infer from unknown typing alone',conversion_error='T039 keeps type unknown and null denominator, oracle verifies this behavior'),
      needed='Producer/config/input schema/version/effective time; explicit service-instance-pod-host bindings and OTel semantic fields for P9.')
]
output=dict(task='T-039',run='thuc-thi-snapshot-004',interpretation='conditional structural comparison, not causal counts or RCA efficacy',cells=cells,chains=[dict(id=k,**v) for k,v in sorted(chains.items())],excluded_edge_groups=list(excluded.values()),groups=groups,source_audit='runs/doc-nguon-002/backend-source-audit.json',lineage='runs/doc-nguon-002/lineage.md',source_tree='bao-phu-nguon.json',mapping='mapping.json',no_cause_percentages=True,source_hashes_verified=len(sources),files_used=[dict(path=str(p.relative_to(ROOT)).replace('\\','/'),sha256=sha(p)) for p in [B/'ban-ghi.json',B/'mapping.json',B/'doi-chieu/tong-hop.json']])
write(run/'source-to-difference.json',output)
counts=Counter((c['level'],c['window'],c['raw_trace_edges'],c['eligible_trace_edges'],c['excluded_trace_edges']) for c in cells)
table='\n'.join(f'| {a} | {w} | {count} | {raw} | {eligible} | {excluded_count} |' for (a,w,raw,eligible,excluded_count),count in sorted(counts.items()))
report='''# Phân tích chênh lệch nguồn và graph T-039

Kết quả **tham khảo có điều kiện** vì chưa xác minh ứng dụng/build/image/deployment sinh dataset. Đã dùng đủ graph dev được giao, không chọn ca theo nhãn, không đọc telemetry thô. Đây là phân tích mô tả và source mechanism candidate; chưa có kết luận nguyên nhân vật lý của mọi cạnh thiếu hoặc lợi ích RCA.

Chuỗi bằng chứng máy đọc nằm tại `runs/ANALYSIS_RUN/source-to-difference.json`: `/cells` có từng graph/interval/mẫu số; `/chains` có toàn khóa match/static-only/trace-only, source records/provenance, member gốc và danh sách cửa sổ; `/excluded_edge_groups` giữ raw edge, mapping từng đầu và tất cả vị trí bị loại. `/groups` phân xử từng giải thích revision/alias/domain/window/branch/static/telemetry/conversion, không cộng cờ thành phần trăm nguyên nhân.

| Mức | Cửa sổ | Số graph | Cạnh trace gốc | Cạnh đủ điều kiện endpoints | Bị loại |
|---|---|---:|---:|---:|---:|
'''+table+'\n\n'
for g in groups:
    report+=f"## {g['id']}. {g['subject']}\n\n"
    report+=' '.join(g['observations'])+'\n\n'+g['mechanism']+'\n\n'
    report+='Bằng chứng: '+ '; '.join(f"`{s['path']}:{s['locator']}`" for s in g['source'])+'. Các key và source records/members tương ứng lấy bằng ID trong `/groups/*/mismatch_keys` và `matched_counterparts`, dẫn `/chains/*/id`; không chỉ một hình đồ thị.\n\n'
    report+='Phân xử: '+'; '.join(k+': '+v for k,v in g['competing'].items())+'.\n\n'
    report+='Phần cần thêm: '+g['needed']+'\n\n'
report+='''## Kết luận giới hạn và bước nhận

Entity endpoints phản ánh các quan hệ service gọi nhau có nguồn; thao tác chỉ so được phần mapping có bằng chứng literal. DB/cache, external/browser, exporter và source-only helper có ý nghĩa/điều kiện khác với các cạnh trace service, nên không gom tất cả thành “trace thiếu”. Graph tĩnh không đại diện một lượt thực thi; graph full không cả ngày. Static-only có thể đồng thời là match ở cửa sổ khác; bảng `/chains/*/occurrences` giữ điều đó.

Sự tương ứng nguồn→bản ghi→khóa→mapping→tập đã kiểm trong T039. Nguyên nhân runtime cần app/deployment/agent/collector lineage cùng dữ liệu được giao đúng quyền. T040 nhận kết quả tham chiếu và các OPEN; P6 chưa được chọn cơ chế từ tỷ lệ; P9 nhận yêu cầu identity, địa chỉ tín hiệu và nguồn độc lập. Đề xuất bổ sung/owner/chi phí tại `de-xuat-bo-sung-nguon.md` và `ban-giao.md`. Chưa nhận đủ inventory toàn deployment, chưa đóng RQ3/RQ5/P5/G3.
'''
report=report.replace('ANALYSIS_RUN',run.name)
(run/'source-to-difference.md').write_text(report,encoding='utf-8')
(B/'phan-tich-chenh-lech.md').write_text(report,encoding='utf-8')
print(json.dumps(dict(chains=len(chains),excluded_edge_groups=len(excluded),cells=len(cells),groups=len(groups)),ensure_ascii=False))
