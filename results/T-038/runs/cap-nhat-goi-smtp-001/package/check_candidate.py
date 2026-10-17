"""Synthetic proposal checks only. Does not import/change active shared package."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
import time
import traceback

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def save(path, obj):
    with path.open('x', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, sort_keys=True, indent=2)
        f.write('\n')

def package(name, folder):
    spec = importlib.util.spec_from_file_location(name, folder/'__init__.py',
                                                submodule_search_locations=[str(folder)])
    obj = importlib.util.module_from_spec(spec)
    sys.modules[name] = obj
    spec.loader.exec_module(obj)
    return obj

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verified(path, manifest):
    rows = {x['path']:x for x in manifest['files']}
    assert sha(ROOT/path) == rows[path]['sha256'], path
    return load(ROOT/path)

def main():
    run = HERE / sys.argv[1]
    run.mkdir(exist_ok=False)
    started = time.perf_counter()
    checks = []
    try:
        oracle = load(HERE/'oracle-before-code.json')
        expected = {x['id']:x for x in oracle['cases']}
        old = package('smtp_old_preview', ROOT/'results/T-037/runs/graph-003/code')
        new = package('smtp_candidate_preview', HERE/'experimental_copy')
        reg = {'sources':[{'id':'oracle','kind':'synthetic','revision':'literal-v1',
                          'sha256':sha(HERE/'oracle-before-code.json'), 'condition':'synthetic, not runtime'}]}
        prov = [{'source_id':'oracle','locator':'cases','condition':'literal synthetic evidence, not actual trace'}]
        doc = {'scope':{'system':'synthetic-SMTP','revision':'literal-v1'},
               'entities':[{'id':x,'name':x,'type':t,'granularity':'logical','role':'synthetic','provenance':prov}
                           for x,t in [('sender','service'),('mail-server','external')]],
               'operations':[{'entity':'sender','name':'send-mail','runtime_name':None,'provenance':prov}],
               'relations':[{'id':'smtp-hop','source':{'entity':'sender','operation':'send-mail'},
                             'target':{'entity':'mail-server','operation':None},
                             'type':'gọi-đồng-bộ','channel':'smtp','messaging':None,
                             'context':'host=mail.test;port=465;ssl=true configured;runtime unverified','provenance':prov}],
               'resource_bindings':[], 'signals':[]}
        mapping = [{'level':'entity','original':x,'candidates':[x],'verified':True,'provenance':prov}
                   for x in ['sender','mail-server']]
        context = {'system':'synthetic-SMTP','level':'entity','domain':'synthetic',
                   'trace_revision':'literal-v1','revision_link_verified':False,'revision_provenance':[]}

        def check(name, actual):
            ok = actual is True
            checks.append({'id':name,'ok':ok,'observed':actual,'oracle':expected.get(name)})
            assert ok, name

        def reject(name, fn, error):
            try:
                fn()
            except ValueError as exc:
                check(name, str(exc) == error)
            else:
                check(name, False)

        def trace(typ='gọi-đồng-bộ', channel='smtp'):
            edge = {'source':'sender','target':'mail-server','type':typ,'evidence_source':'trace',
                    'destination':None,'event_count':1,'witness':[]}
            if channel is not None:
                edge['channel'] = channel
            return {'level':'entity','nodes':[{'id':'sender'},{'id':'mail-server'}],
                    'edges':[edge],'interval_ns':[0,1]}

        def cmp(static_doc, tr, maps=None):
            return new.compare(new.build(static_doc, reg)[0], tr, mapping if maps is None else maps, context, reg)

        def ints(res):
            return [res['views'][v]['numerator'] for v in ['endpoints','typed']]

        e,o = new.build(doc, reg)
        check('smtp_representation_sync_evidence', len(e['edges']) == len(o['edges']) == 1 and
              e['edges'][0]['type']=='gọi-đồng-bộ' and e['edges'][0]['channel']=='smtp' and e['edges'][0]['messaging'] is None)
        unknown = deepcopy(doc); unknown['relations'][0]['type']='gọi-chưa-phân-kiểu'
        eu,ou = new.build(unknown, reg)
        check('smtp_representation_unknown', len(eu['edges'])==len(ou['edges'])==1 and
              eu['edges'][0]['type']=='gọi-chưa-phân-kiểu')
        eo = deepcopy(doc); eo['relations'][0]['source']['operation']=None
        ee,oo = new.build(eo, reg)
        check('smtp_entity_only', len(ee['edges'])==1 and not oo['edges'] and
              oo['operation_exclusions'][0]['reason']=='no_operation_evidence')
        pr = new.project(o)
        check('smtp_projection', len(pr['edges'])==1 and
              {k:pr['edges'][0][k] for k in ['source','target','channel','type']} ==
              {'source':'sender','target':'mail-server','channel':'smtp','type':'gọi-đồng-bộ'})
        result = cmp(doc, trace('gọi-chưa-phân-kiểu'))
        check('smtp_type_unknown_not_upgraded', ints(result)==[1,0] and
              result['views']['typed']['exclusions']['trace'][0]['reason']=='unknown_type')
        check('smtp_explicit_transport_match', ints(cmp(doc,trace()))==[1,1])
        for ident,channel in [('smtp_vs_http_no_match','http'),('smtp_vs_rpc_no_match','rpc'),
                              ('smtp_vs_missing_transport_no_match',None)]:
            res=cmp(doc,trace(channel=channel))
            check(ident, ints(res)==[0,0] and all(len(res['views'][v]['static_only'])==
                  len(res['views'][v]['trace_only'])==1 for v in ['endpoints','typed']))
        res=cmp(doc,trace('gọi-chưa-phân-kiểu',None))
        check('smtp_missing_type_missing_transport_no_match', ints(res)==[0,0] and
              res['views']['typed']['exclusions']['trace'][0]['reason']=='unknown_type')
        hdoc=deepcopy(doc);hdoc['relations'][0]['channel']='http'
        check('http_rpc_legacy_typed_unchanged', ints(cmp(hdoc,trace(channel='rpc')))==[1,1])
        bad=deepcopy(doc);bad['relations'][0]['messaging']={'broker':'mail-server','broker_scope':'x',
                                                        'exchange':None,'routing_key':None,'queue':None}
        reject('smtp_not_message_broker', lambda:new.build(bad,reg), 'unexpected_messaging')
        for ident,typ in [('smtp_with_data_type_rejected','dữ-liệu'),('smtp_with_messaging_type_rejected','thông-điệp')]:
            bad=deepcopy(doc);bad['relations'][0]['type']=typ
            reject(ident, lambda:new.build(bad,reg), 'relation_channel')
        reject('smtp_trace_data_type_rejected', lambda:cmp(doc,trace('dữ-liệu')), 'trace_channel')
        reject('unknown_trace_transport_rejected', lambda:cmp(doc,trace(channel='guessed')), 'trace_channel')
        badmap=deepcopy(mapping);badmap[1]['verified']=False
        res=cmp(doc,trace(),badmap)
        check('smtp_unverified_mapping', ints(res)==[0,0] and
              res['views']['endpoints']['exclusions']['trace'][0]['reason']=='unverified_mapping:target')
        tr=trace();tr['edges']=[];res=cmp(doc,tr)['views']['endpoints']
        check('smtp_empty_trace_denominator', res['static_denominator']==1 and res['trace_denominator']==0 and
              res['trace_fraction'] is None)
        two=deepcopy(doc);second=deepcopy(two['relations'][0]);second['id']='smtp-second-port';
        second['context']='host=mail.test;port=587;STARTTLS configured;runtime unverified';two['relations'].append(second)
        e2,o2=new.build(two,reg)
        check('smtp_context_kept_not_address_verified', len(e2['edges'])==1 and
              len(e2['edges'][0]['contexts'])==2 and set(e2['edges'][0]['contexts'])=={r['context'] for r in two['relations']})
        bdoc,btrace,bmapping=deepcopy(two),deepcopy(trace()),deepcopy(mapping)
        r1=cmp(two,btrace,bmapping);r2=cmp(two,btrace,bmapping)
        two['relations'].reverse();two['entities'].reverse();two['operations'].reverse()
        r3=cmp(two,btrace,list(reversed(bmapping)))
        check('smtp_order_and_input_immutability', r1==r2==r3 and btrace==trace() and bmapping==mapping)
        check('smtp_runtime_name_not_filled', o['nodes'][0]['runtime_name'] is None)
        check('smtp_no_recipient_or_broker_invented', sorted(n['id'] for n in e['nodes'])==['mail-server','sender'] and
              e['edges'][0]['target']=='mail-server' and not any(n['type']=='broker' for n in e['nodes']))
        sig=deepcopy(doc);sig['signals']=[{'id':'metric','kind':'metric','entity':'sender','operation':None,
                                        'address':['synthetic','service','cpu'],'shared':True,'provenance':prov}]
        sig['operations'].append({'entity':'sender','name':'second-op','runtime_name':None,'provenance':prov})
        es,os=new.build(sig,reg)
        check('smtp_shared_metric_not_multiplied', len(es['signals'])==len(os['signals'])==1 and es['signals'][0]['operation'] is None)
        ownerdoc=deepcopy(doc);ownerdoc['operations'].append({'entity':'mail-server','name':'recv','runtime_name':None,'provenance':prov})
        oe,oo=new.build(ownerdoc,reg);ctx=deepcopy(context);ctx['level']='operation'
        tro={'level':'operation','nodes':[{'id':'raw-op','entity':'sender'}], 'belongs_to':[['raw-op','sender']],
             'component_context':[{'id':'mail-server'}], 'edges':[dict(trace()['edges'][0],source='raw-op')], 'interval_ns':[0,1]}
        omap=mapping+[{'level':'operation','original':'raw-op','candidates':['["mail-server","recv"]'], 'verified':True,'provenance':prov}]
        res=new.compare(oo,tro,omap,ctx,reg)
        check('smtp_operation_mapping_owner_conflict', res['views']['endpoints']['exclusions']['trace'][0]['reason']=='operation_owner_conflict:source')
        # Old contract fixtures and frozen TT model must remain exactly identical.
        m36=load(ROOT/'results/T-036/manifest.json');old_doc=verified('results/T-036/fixtures/input.json',m36)
        old_reg=verified('results/T-036/nguon.json',m36)
        legacy_equal=new.build(old_doc,old_reg)==old.build(old_doc,old_reg)
        checks.append({'id':'legacy_T036_fixture_build_exact_equal','ok':legacy_equal});assert legacy_equal
        m38=load(ROOT/'results/T-038/manifest.json')
        tt=verified('results/T-038/ban-ghi.json',m38);ttreg=verified('results/T-038/nguon.json',m38)
        before=deepcopy(tt);oldgraphs=old.build(tt,ttreg);newgraphs=new.build(tt,ttreg)
        eq=oldgraphs==newgraphs
        checks.append({'id':'legacy_T038_frozen_build_exact_equal','ok':eq});assert eq
        # Current sibling models exist; replay full source builds instead of smoke-only assumptions.
        for task, ident in [('T-037','current_T037_SMTP_model_build_exact_equal'),('T-039','current_T039_model_build_exact_equal')]:
            sibling_manifest=load(ROOT/'results'/task/'manifest.json')
            sibling_doc=verified('results/'+task+'/ban-ghi.json',sibling_manifest)
            sibling_registry=verified('results/'+task+'/nguon.json',sibling_manifest)
            check(ident, old.build(sibling_doc,sibling_registry)==new.build(sibling_doc,sibling_registry))
        # Existing comparison intentionally reports structural agreement; proposed keys change that meaning.
        baseline_graph=old.build(doc,reg)[0]
        legacy_trace=trace(channel=None)
        baseline_result=old.compare(baseline_graph,legacy_trace,mapping,context,reg)
        candidate_result=new.compare(new.build(doc,reg)[0],legacy_trace,mapping,context,reg)
        check('current_structural_to_proposed_protocol_comparison',
              len(baseline_result['views']['endpoints']['intersection'])==1 and
              len(candidate_result['views']['endpoints']['intersection'])==0)
        save(run/'comparison-before-after.json',{'status':'PROPOSED_SEMANTICS_NOT_ACTIVE',
              'baseline':baseline_result,'candidate':candidate_result,'source_doc':doc,'trace':legacy_trace})
        # Provenance-backed delta stays in proposal, never added to current TT outputs.
        delta={'id':'SMTP:mail-send:proposed-only',
               'source':{'entity':'ts-notification-service','operation':'java:notification.service.MailService#sendEmail(Mail mail,String template)'},
               'target':{'entity':'smtp.163.com','operation':None},'type':'gọi-chưa-phân-kiểu','channel':'smtp','messaging':None,
               'context':'source default host=smtp.163.com;port=465;ssl.enable=true;auth=true;starttls.enable=true;starttls.required=true; effective library/build/TLS/outcome/runtime OPEN; acceptance is not recipient delivery',
               'provenance':[{'source_id':'TT:ts-notification-service/src/main/java/notification/service/MailService.java','locator':'L22-L23,L30-L46','condition':'JavaMailSender.send interface call; effective implementation/blocking/runtime unverified'},
                             {'source_id':'TT:ts-notification-service/src/main/resources/application.yml','locator':'L12-L14,L19-L25','condition':'literal configured endpoint and TLS flags, not observed negotiated transport'}]}
        tt['relations'].append(delta);tge,tgo=new.build(tt,ttreg)
        deltaedges=[x for x in tge['edges'] if delta['id'] in x['record_ids']]
        deltaop=[x for x in tgo['edges'] if delta['id'] in x['record_ids']]
        assert len(deltaedges)==len(deltaop)==1 and before==verified('results/T-038/ban-ghi.json',m38)
        save(run/'proposed-T038-delta.json',delta)
        save(run/'proposed-T038-edge-preview.json',{'status':'EXPERIMENTAL_COPY_NOT_ACTIVE_PIN','entity':deltaedges,'operation':deltaop,
                                                'prior_edges':[len(g['edges']) for g in oldgraphs],
                                                'candidate_edges':[len(tge['edges']),len(tgo['edges'])],
                                                'runtime_verified':False,'typed_type':'unknown','comparison_rerun':False})
        save(run/'synthetic-input.json',{'document':doc,'registry':reg,'trace':trace(),'mapping':mapping,'context':context})
        save(run/'synthetic-result.json',cmp(doc,trace()))
        assert {x['id'] for x in checks} >= set(expected)
        save(run/'checks.json',{'status':'experimental preview only; not shared pin adoption',
                              'all_ok':all(x['ok'] for x in checks),'checks':checks,
                              'elapsed_seconds':time.perf_counter()-started,'python':sys.version,'platform':platform.platform(),
                              'created_utc':datetime.now(timezone.utc).isoformat(),
                              'oracle_sha256':sha(HERE/'oracle-before-code.json'),
                              'shared_code_unchanged':all(sha(ROOT/x['source'])==x['base_sha256'] for x in load(HERE/'candidate-code-hashes.json'))})
        print('PASS',len(checks),'proposal checks. No shared changes or actual SMTP execution.')
    except Exception as exc:
        save(run/'failure.json',{'error':str(exc),'traceback':traceback.format_exc(),'checks':checks,
                                'elapsed_seconds':time.perf_counter()-started})
        raise

if __name__=='__main__':
    main()
