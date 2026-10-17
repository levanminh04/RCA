"""T039 orchestration only. Run from repository root; never imports current src.
Every attempt gets a new run directory and retains failures. No network/raw data.
"""
import sys
sys.dont_write_bytecode = True
import copy
import ctypes
import hashlib
import importlib.util
import json
import platform
import time
import traceback
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'results/T-039'
SNAP = ROOT / 'results/T-036/runs/kiem-r1-after-002/code'

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def canonical(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def rel(p):
    return Path(p).relative_to(ROOT).as_posix()

def prov(path, loc, condition='Khả năng trong snapshot nguồn; deployment/dataset chưa nối revision.'):
    return dict(source_id='OB:'+path, locator=loc, condition=condition)

def union(rows):
    return [json.loads(x) for x in sorted(set(map(canonical, rows)))]

def pinned():
    manifest=ROOT/'results/T-036/manifest.json'
    assert sha(manifest)=='d10bb327b2cc62334c87f3e33ac9a7c62ad6a4d78f735530604a64c3eb38d2b1'
    hashes=read(SNAP.parent/'code-hashes.json')
    for original, digest in hashes.items():
        assert sha(SNAP/Path(original).name)==digest, original
    spec=importlib.util.spec_from_file_location('t039_pinned', SNAP/'__init__.py', submodule_search_locations=[str(SNAP)])
    module=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    return module

def oracle(api, run):
    literal=read(BASE/'fixtures/oracle.json')
    fixture=literal['fixture']; expected=literal['expected']
    p=[dict(source_id='synthetic', locator='literal oracle', condition='synthetic only')]
    reg={'sources':[dict(id='synthetic',kind='synthetic',revision='1',sha256='0'*64,condition='synthetic only')]}
    doc=dict(scope=dict(system='synthetic',revision='1'),entities=[],operations=[],relations=[],resource_bindings=[],signals=[])
    for name in fixture['entities']:
        doc['entities'].append(dict(id=name,name=name,type='database' if name=='database' else 'service',granularity='logical',role='fixture',provenance=p))
    for owner,name in fixture['operations']:
        doc['operations'].append(dict(entity=owner,name=name,runtime_name=name,provenance=p))
    for r in fixture['relations']:
        doc['relations'].append(dict(id=r['id'],source=dict(zip(['entity','operation'],r['source'])),target=dict(zip(['entity','operation'],r['target'])),type=r['type'],channel=r['channel'],messaging=None,context='synthetic',provenance=p))
    before=copy.deepcopy(doc)
    ent,op=api.build(doc,reg)
    context=dict(system='synthetic',level='entity',domain='synthetic',trace_revision='fixture',revision_link_verified=False,revision_provenance=[])
    trace=dict(level='entity',nodes=[{'id':x} for x in ['alias-alpha','beta']],edges=[dict(source=s,target=t,type=typ,evidence_source='trace',destination=None,event_count=1,witness=[]) for s,t,typ in fixture['trace_entity_edges']],interval_ns=[10,20])
    mappings=[dict(level='entity',original=a,candidates=[b],verified=True,provenance=p) for a,b in fixture['entity_mapping']]
    result=api.compare(ent,trace,mappings,context,reg)
    for view, key in [('endpoints','entity_endpoints'),('typed','entity_typed')]:
        for field,value in expected[key].items():
            assert result['views'][view][field]==value, (view,field)
    projected=api.project(op)
    assert [[x['source'],x['target'],x['type'],x['channel']] for x in projected['edges']]==expected['projection_edges']
    assert [x['record_id'] for x in op['operation_exclusions']]==expected['entity_only_record_ids']
    unverified=copy.deepcopy(mappings);unverified[0]['verified']=False
    assert api.compare(ent,trace,unverified,context,reg)['views']['endpoints']['trace_denominator']==expected['unverified_mapping_trace_denominator']
    # Deliberately wrong operation owner, identical syntax is not sufficient.
    aid=canonical(['alpha','invoke']);bid=canonical(['beta','serve'])
    ot=dict(level='operation',nodes=[dict(id=aid,entity='alpha'),dict(id=bid,entity='beta')],belongs_to=[[aid,'alpha'],[bid,'beta']],component_context=[],edges=[dict(source=aid,target=bid,type='gọi-chưa-phân-kiểu',evidence_source='trace',destination=None,event_count=1,witness=[])],interval_ns=[10,20])
    om=[dict(level='entity',original=x,candidates=[x],verified=True,provenance=p) for x in ['alpha','beta']]+[dict(level='operation',original=aid,candidates=[bid],verified=True,provenance=p),dict(level='operation',original=bid,candidates=[bid],verified=True,provenance=p)]
    wrong=api.compare(op,ot,om,dict(context,level='operation'),reg)
    assert wrong['views']['endpoints']['exclusions']['trace'][0]['reason']==expected['wrong_owner_exclusion']
    empty=copy.deepcopy(ent);empty['edges']=[]
    et=copy.deepcopy(trace);et['edges']=[]
    er=api.compare(empty,et,mappings,context,reg)['views']['endpoints']
    assert [er['static_denominator'],er['trace_denominator']]==expected['empty_both_denominators']
    assert [er['static_fraction'],er['trace_fraction']]==expected['empty_both_fractions']
    assert doc==before
    write(run/'oracle-input.json',dict(document=doc,registry=reg,trace=trace,mappings=mappings,context=context))
    write(run/'oracle-result.json',dict(status='PASS',literal_sha256=sha(BASE/'fixtures/oracle.json'),result=result,wrong_owner=wrong,empty=er,projection=projected))

def merge(run):
    parts=[read(BASE/'parts'/f'{name}.json') for name in ['common','backend','go']]
    doc=dict(scope=parts[0]['scope'])
    audit=[]
    for col in ['entities','operations','relations','resource_bindings','signals']:
        rows={}
        for part in parts:
            for row in part[col]:
                row=copy.deepcopy(row)
                key=canonical([row['entity'],row['name']]) if col=='operations' else row['id']
                if key in rows:
                    old=rows[key]
                    for field in row:
                        if field=='provenance':continue
                        if old[field]!=row[field]:
                            if field=='runtime_name' and (old[field] is None or row[field] is None):
                                old[field]=old[field] or row[field]
                            else:raise ValueError(('merge_conflict',col,key,field,old[field],row[field]))
                    old['provenance']=union(old['provenance']+row['provenance'])
                    audit.append(dict(collection=col,key=key,action='union_provenance'))
                else:rows[key]=row
        doc[col]=[rows[k] for k in sorted(rows)]
    # Reviewed corrections are in orchestration, preserving original specialist fragments.
    for row in doc['operations']:
        if (row['entity'],row['name'])==('adservice','hipstershop.AdService/GetAds'):
            row['runtime_name']='hipstershop.AdServiceImpl/getAds'
            row['provenance']=union(row['provenance']+[prov('src/adservice/src/main/java/hipstershop/AdService.java','L106–121','@WithSpan + Span.current().updateName literal; thư viện/build thực tế chưa xác minh.')])
            audit.append(dict(collection='operations',key=[row['entity'],row['name']],action='retain explicit runtime name'))
    for row in doc['signals']:
        if row['id'] in ['common:trace:adservice','common:trace:cartservice']:
            service=row['entity']; service_var='OTEL_SERVICE_NAME' if service=='adservice' else 'SERVICE_NAME'
            row['address']=['opentelemetry','resource.service.name','${'+service_var+'}','exporter.endpoint','${OTEL_EXPORTER_OTLP_ENDPOINT}']
            row['provenance']=[prov('kubernetes-manifests/'+service+'.yaml','L48–51')]
            audit.append(dict(collection='signals',key=row['id'],action='correct endpoint variables from YAML'))
    for row in doc['resource_bindings']:
        if row['entity']=='mysql/addatabase':
            row['provenance']=union(row['provenance']+[prov('src/adservice/src/main/java/hipstershop/AdService.java','L237–257'),prov('kubernetes-manifests/adservice.yaml','L42–43'),prov('kubernetes-manifests/mysql.yaml','L1–11')])
    removed=[r for r in doc['relations'] if r['id']=='common:asset:fonts.gstatic.com']
    doc['relations']=[r for r in doc['relations'] if r not in removed]
    audit.append(dict(action='exclude resource preconnect hint from HTTP call graph',records=removed,reason='header.html L29 only preconnect; external CSS not inspected. Entity remains inventory hint.'))
    # Source-declared outgoing client method has local ownership, even when the
    # instrumentation name cannot be established from generated RPC path alone.
    cp=[prov('src/recommendationservice/recommendation_server.py','L63–84;L98–105'),prov('src/recommendationservice/demo_pb2_grpc.py','L143–158')]
    doc['operations'].append(dict(entity='recommendationservice',name='hipstershop.ProductCatalogService/ListProducts',runtime_name=None,provenance=cp))
    for r in doc['relations']:
        if r['id']=='backend:recommendation-catalog':
            old=copy.deepcopy(r)
            r['source']['operation']='hipstershop.ProductCatalogService/ListProducts'
            doc['relations'].append(dict(id='audit:recommendation-handler-client',source=old['source'],target=copy.deepcopy(r['source']),type='gọi-đồng-bộ',channel='internal',messaging=None,context='static invocation nesting; not a claim about parent span',provenance=cp))
            break
    additions=BASE/'runs/doc-nguon-002/backend-additions.json'
    if additions.exists():
        extra=read(additions)
        for col in ['entities','operations','relations','resource_bindings','signals']:
            doc[col]+=extra.get(col,[])
        audit.append(dict(action='source-audited additions',path=rel(additions),sha256=sha(additions)))
    # Explicit same-pod DATA_SOURCE_NAME does not require library default assumptions.
    doc['relations'].append(dict(id='audit:mysqld-exporter-to-mysql',source=dict(entity='mysqld-exporter',operation=None),target=dict(entity='mysql',operation=None),type='dữ-liệu',channel='data',messaging=None,context='exporter variant only; explicit loopback DATA_SOURCE_NAME, not app traffic or deployment confirmation',provenance=[prov('kubernetes-manifests/mysql_exporter.yaml','L49–55')]))
    bindings={}
    for row in doc['resource_bindings']:
        key=canonical([row['entity'],row['resource'],row['relation']])
        if key in bindings:
            audit.append(dict(action='merge identical logical placement, retaining source records',record_ids=[bindings[key]['id'],row['id']],key=key))
            bindings[key]['provenance']=union(bindings[key]['provenance']+row['provenance'])
        else:bindings[key]=row
    doc['resource_bindings']=[bindings[k] for k in sorted(bindings)]
    write(run/'merge-audit.json',audit)
    write(run/'document.json',doc)
    return doc

def independent(result, static, trace, mappings):
    """Recompute keys directly from input edges, independent of saved set logic."""
    mi={(x['level'],x['original']):x for x in mappings}
    own=dict(trace.get('belongs_to',[]));so=dict(static.get('belongs_to',[]))
    def resolve(x,operation=False):
        m=mi.get(('operation' if operation else 'entity',x))
        if not m or not m['verified'] or len(set(m['candidates']))!=1:return None
        target=m['candidates'][0]
        if operation and so[target]!=resolve(own[x]):return None
        return target
    for view in ['endpoints','typed']:
        sets={};eligible={}
        for side,g in [('static',static),('trace',trace)]:
            keys=set();ids=set()
            for i,e in enumerate(g['edges']):
                if result['context']['level']=='entity' and (e['source']==e['target'] or e['type']=='span-parent'):continue
                s,t=e['source'],e['target']
                if side=='trace':s,t=resolve(s,s in own),resolve(t,t in own)
                if s is None or t is None:continue
                if result['context']['level']=='entity' and s==t:continue
                assert e['type']!='thông-điệp','OB independent check does not assume messaging address'
                if view=='typed' and e['type']=='gọi-chưa-phân-kiểu':continue
                keys.add(canonical([s,t,e['type'] if view=='typed' else None,None]));ids.add(i)
            sets[side]=keys;eligible[side]=ids
        v=result['views'][view];s,t=sets['static'],sets['trace']
        for k,expected in [('S',s),('T',t),('intersection',s&t),('static_only',s-t),('trace_only',t-s)]:
            assert set(map(canonical,v[k]))==expected, (view,k)
        assert (v['numerator'],v['static_denominator'],v['trace_denominator'])==(len(s&t),len(s),len(t))
        assert v['static_fraction']==(len(s&t)/len(s) if s else None)
        assert v['trace_fraction']==(len(s&t)/len(t) if t else None)
        for side,g in [('static',static),('trace',trace)]:
            members=[m for k in v['members'][side] for m in k['members']]
            assert {m['index'] for m in members}==eligible[side]
            assert len(members)==len(eligible[side])
            assert all(m['original']==g['edges'][m['index']] for m in members)
            excluded=v['exclusions'][side];ix={x['index'] for x in excluded}
            assert len(ix)==len(excluded)
            assert not ix & eligible[side]
            assert ix | eligible[side]==set(range(len(g['edges'])))
    assert result['interval_ns']==trace['interval_ns'] and result['conditional_reference'] is True

def mappings(doc,inventory,reg):
    src={x['id']:x for x in doc['entities']}
    ops=doc['operations'];nodes={};entities=set()
    for item in inventory:
        graph=read(ROOT/item['path'])
        if graph['level']=='entity':entities.update(x['id'] for x in graph['nodes'])
        else:
            for n in graph['nodes']:nodes[n['id']]=n
    output=[];notes=[]
    fallback=[prov('pb/demo.proto','service/message declarations','Dùng làm provenance phạm vi nguồn, không là bằng chứng alias khi chưa có.')]
    for x in sorted(entities):
        output.append(dict(level='entity',original=x,candidates=[x] if x in src else [],verified=x in src,provenance=src[x]['provenance'] if x in src else fallback))
    for ident,n in sorted(nodes.items()):
        runtime=n.get('operation',n.get('name'))
        # Inspect canonical T035 ID, not slash or grpc prefix normalization.
        owner,name=json.loads(ident)
        exact=[o for o in ops if o['entity']==owner and o['runtime_name']==name]
        candidates=exact or [o for o in ops if o['entity']==owner and o['name']==name]
        ids=[canonical([o['entity'],o['name']]) for o in candidates]
        output.append(dict(level='operation',original=ident,candidates=sorted(set(ids)),verified=bool(exact) and len(set(ids))==1,provenance=union([p for o in candidates for p in o['provenance']]) or src.get(owner,{}).get('provenance',fallback)))
        notes.append(dict(original=ident,owner=owner,name=name,status='explicit_runtime_literal' if exact else 'canonical_rpc_name_only' if candidates else 'unmapped_no_literal',candidates=ids))
    proposal=BASE/'runs/mapping-source-001/mapping-proposals.json'
    if proposal.exists():
        candidates=read(proposal)['mappings']
        valid={canonical([o['entity'],o['name']]) for o in ops}
        pi={(m['level'],m['original']):m for m in candidates}
        for row in output:
            other=pi.get((row['level'],row['original']))
            if row['level']=='operation' and not row['candidates'] and other and other['candidates']:
                assert other['verified'] is False
                assert set(other['candidates'])<=valid
                assert all(json.loads(x)[0]==json.loads(row['original'])[0] for x in other['candidates'])
                row['candidates']=other['candidates'];row['provenance']=other['provenance']
                for n in notes:
                    if n['original']==row['original']:
                        n['status']='manual_scoped_rpc_candidate_unverified';n['candidates']=other['candidates']
    return output,notes

def run(name):
    run=BASE/'runs'/name
    run.mkdir(parents=True,exist_ok=False)
    start=time.perf_counter();inputs=[]
    try:
        # Snapshot root outputs before mutation; every previous report remains recoverable.
        for path in BASE.iterdir():
            if path.is_file() and path.suffix in {'.json','.md'}:
                target=run/'before'/path.name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(path.read_bytes())
        protected=[ROOT/'src/do_thi_tinh/build.py',ROOT/'src/do_thi_tinh/compare.py',ROOT/'results/T-036/manifest.json']
        for task in ['T-037','T-038']:
            protected += [ROOT/'results'/task/'manifest.json']
        protected=[p for p in protected if p.is_file()]
        protected_before={rel(p):sha(p) for p in protected}
        write(run/'protected-before.json',protected_before)
        api=pinned();oracle(api,run)
        manifest35=ROOT/'results/T-035/manifest.json'
        assert sha(manifest35)=='9041967bf9fef956f95bf4180992947be0e7dd39e788d4d20741a2a56c35d662'
        index35={x['path']:x for x in read(manifest35)['files']}
        inv=read(BASE/'runs/tien-kiem-001/graph-inventory.json')['rows']
        canonical_paths=read(ROOT/'results/T-035/thong-ke-do-thi.json')['canonical_graph_files']
        assert {x['path'] for x in inv}=={x for x in canonical_paths if '/Nezha-OB/' in x}
        for x in inv:
            p=ROOT/x['path'];assert sha(p)==index35[x['path']]['sha256'];inputs.append(dict(path=x['path'],sha256=sha(p),bytes=p.stat().st_size))
        reg=read(BASE/'nguon.json')
        for s in reg['sources']:
            if s.get('path'):
                assert sha(ROOT/s['path'])==s['sha256'], s['id']
        doc=merge(run)
        before=copy.deepcopy((doc,reg));ent,op=api.build(doc,reg)
        assert before==(doc,reg)
        perm=copy.deepcopy(doc)
        for col in ['entities','operations','relations','resource_bindings','signals']:perm[col].reverse()
        assert api.build(perm,reg)==(ent,op)
        projection=api.project(op)
        # Independently project typed relation signatures and account entity-only.
        def sig(e):return canonical([e['source'],e['target'],e['type'],e['channel'],e['messaging']])
        es={sig(e) for e in ent['edges']};ps={sig(e) for e in projection['edges']}
        assert ps<=es
        write(run/'projection-check.json',dict(projected_subset=True,entity_only_keys=[json.loads(x) for x in sorted(es-ps)],operation_exclusions=op['operation_exclusions']))
        write(BASE/'ban-ghi.json',doc)
        write(BASE/'do-thi/thuc-the.json',ent);write(BASE/'do-thi/thao-tac.json',op);write(BASE/'do-thi/chieu-thuc-the.json',projection)
        write(run/'outputs/ban-ghi.json',doc)
        write(run/'outputs/do-thi/thuc-the.json',ent);write(run/'outputs/do-thi/thao-tac.json',op);write(run/'outputs/do-thi/chieu-thuc-the.json',projection)
        mapping,notes=mappings(doc,inv,reg)
        write(BASE/'mapping.json',dict(scope=doc['scope'],revision_link_verified=False,policy='exact entity identity or explicit runtime_name literal with owner; no inferred prefix aliases',rows=mapping,notes=notes))
        write(run/'outputs/mapping.json',read(BASE/'mapping.json'))
        rows=[];unionkeys={};excluded=Counter()
        for number,item in enumerate(inv,1):
            graph=read(ROOT/item['path']);sg=ent if item['level']=='entity' else op
            active_mapping=[m for m in mapping if item['level']=='operation' or m['level']=='entity']
            context=dict(system='Nezha-OB',level=item['level'],domain='dev-adapter',trace_revision='T035-v2.1-canonical',revision_link_verified=False,revision_provenance=[])
            before=copy.deepcopy((sg,graph,active_mapping,context,reg))
            t=time.perf_counter();result=api.compare(sg,graph,active_mapping,context,reg)
            independent(result,sg,graph,active_mapping)
            assert before==(sg,graph,active_mapping,context,reg)
            assert api.compare(sg,graph,list(reversed(active_mapping)),context,reg)==result
            dest=BASE/'doi-chieu'/item['opaque_id']/item['level']/(item['window']+'.json')
            write(dest,result)
            write(run/'outputs'/dest.relative_to(BASE),result)
            row={k:item[k] for k in ['path','opaque_id','level','window','interval_ns']};row['output']=rel(dest);row['seconds']=time.perf_counter()-t
            row['views']={view:{k:v[k] for k in ['numerator','static_denominator','trace_denominator','static_fraction','trace_fraction']} for view,v in result['views'].items()}
            row['exclusions']={view:{side:dict(Counter(x['reason'] for x in v['exclusions'][side])) for side in ['static','trace']} for view,v in result['views'].items()}
            rows.append(row)
            for view,v in result['views'].items():
                for group in ['S','T','intersection','static_only','trace_only']:
                    unionkeys.setdefault((item['level'],view,group),set()).update(map(canonical,v[group]))
            if number==1:write(run/'pilot.json',dict(input=item,seconds=row['seconds'],interpretation='process timing only; no isolated machine cost inference'))
            if number%22==0:print(f'{number}/{len(inv)} PASS',flush=True)
        summary=dict(task='T-039',run=rel(run),status='COMPUTED_PENDING_SOURCE_AND_REPORT_QA',graph_count=len(rows),rows=rows,unions=[dict(level=a,view=b,group=c,keys=[json.loads(x) for x in sorted(v)]) for (a,b,c),v in sorted(unionkeys.items())],static_counts={level:dict(nodes=len(g['nodes']),edges=len(g['edges']),inventory=len(g['inventory']),signals=len(g['signals']),bindings=len(g['resource_bindings'])) for level,g in [('entity',ent),('operation',op)]},record_counts={k:len(v) for k,v in doc.items() if isinstance(v,list)},mapping_counts=dict(Counter((m['level']+':'+('verified' if m['verified'] else 'unverified' if m['candidates'] else 'unmapped')) for m in mapping)))
        write(BASE/'doi-chieu/tong-hop.json',summary)
        write(run/'outputs/doi-chieu/tong-hop.json',summary)
        protected_after={rel(p):sha(p) for p in protected}
        write(run/'protected-after.json',protected_after)
        changed=[x for x in protected_before if protected_before[x]!=protected_after[x]]
        write(run/'verification.json',dict(status='PASS',oracle=True,graphs=len(rows),independent_sets_members_denominators=True,permutation=True,input_immutable=True,intervals_preserved=True,conditional_reference=True,snapshot_modules={k:str(v.__file__) for k,v in sys.modules.items() if k.startswith('t039_pinned')},protected_changed=changed,protected_interpretation='Concurrent changes may belong to other sessions; this runner writes only T039.',inputs=inputs))
        write(run/'cost.json',dict(elapsed_seconds=time.perf_counter()-start,python=sys.version,platform=platform.platform(),attempt_disk_bytes=sum(p.stat().st_size for p in run.rglob('*') if p.is_file()),all_T039_disk_bytes=sum(p.stat().st_size for p in BASE.rglob('*') if p.is_file()),input_graph_bytes=sum(x['bytes'] for x in inputs),graph_count=len(rows),isolated_benchmark=False,other_workloads='not controlled; no extrapolation from timing',peak_process_rss_bytes=peak_memory()))
        print(json.dumps({k:summary[k] for k in ['graph_count','static_counts','record_counts','mapping_counts']},ensure_ascii=False))
    except Exception:
        write(run/'failure.json',dict(traceback=traceback.format_exc(),elapsed_seconds=time.perf_counter()-start))
        raise

def peak_memory():
    class PMC(ctypes.Structure):
        _fields_=[('cb',ctypes.c_ulong),('PageFaultCount',ctypes.c_ulong)]+[(x,ctypes.c_size_t) for x in ['PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage']]
    counters=PMC();counters.cb=ctypes.sizeof(counters)
    ctypes.windll.kernel32.GetCurrentProcess.restype=ctypes.c_void_p
    ctypes.windll.psapi.GetProcessMemoryInfo.argtypes=[ctypes.c_void_p,ctypes.POINTER(PMC),ctypes.c_ulong]
    handle=ctypes.windll.kernel32.GetCurrentProcess()
    ok=ctypes.windll.psapi.GetProcessMemoryInfo(handle,ctypes.byref(counters),counters.cb)
    return counters.PeakWorkingSetSize if ok else None

if __name__=='__main__':
    run(sys.argv[1])
