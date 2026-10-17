"""Supplemental source oracle and coverage checks, independent expected literals.

The handwritten oracle was made after initial extractor code, from direct source
reads. It is not a claim of an oracle preceding implementation.
"""
import collections
import datetime
import hashlib
import importlib.util
import json
import pathlib
import re
import time

HERE=pathlib.Path(__file__).resolve().parent
REPO=HERE.parents[4]

def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def main():
    started=time.time();facts=load(HERE/'source-facts.json');oracle=load(HERE/'manual-oracle.json')
    plan=load(REPO/'results/T-038/runs/metadata-de-xuat-001/de-xuat-tai.json');root=REPO/plan['proposed_destination'];rows={x['path']:x for x in plan['proposed_files']}
    results=[];cache={}
    def source(p):
        if p not in cache:
            b=(root/p).read_bytes();assert len(b)==rows[p]['bytes'] and blob(b)==rows[p]['git_blob'],p
            cache[p]=b.decode('utf-8-sig')
        return cache[p]
    def check(name,ok,expected=None,actual=None):results.append({'check':name,'ok':bool(ok),'expected':expected,'actual':actual})
    for entry in oracle['checks']:
        text=source(entry['source_path']);expected=entry['source_literals']
        check(entry['id']+':source-literals',all(s in text for s in expected),expected,[s for s in expected if s not in text])
        for prefix in ['constant','config']:
            if prefix+'_source_path' in entry:
                t=source(entry[prefix+'_source_path']);check(entry['id']+':'+prefix+'-literal',entry[prefix+'_literal'] in t)
    c=oracle['checks'][0];actual=sorted([x['http_method'],x['path']] for x in facts['operations'] if x['owner']==c['expected_owner'] and x['kind']=='http_handler')
    check(c['id']+':exact-routes',actual==sorted(c['expected_routes']),sorted(c['expected_routes']),actual)
    c=oracle['checks'][1];actual=[x for x in facts['relations'] if x['kind']=='http_call' and x['source_path']==c['source_path'] and x['java_method']==c['expected_caller_method']]
    match=[x for x in actual if any(a['target_entity']==c['expected_target'] and a['path_template']==c['expected_path'] for a in x['url_alternatives']) and x['http_method']==c['expected_method']]
    check(c['id']+':resolved-call',len(match)==1,1,len(match))
    check(c['id']+':caller-owner',bool(match) and all(x['java_method_id'].startswith(c['expected_source']+'::travel.service.TravelServiceImpl#'+c['expected_caller_method']+'(') for x in match))
    c=oracle['checks'][2];actual=[x for x in facts['relations'] if x['kind']=='messaging_consume' and x['owner']==c['expected_consumer']]
    check(c['id']+':queue',len(actual)==1 and actual[0]['queue']==c['expected_queue'],c['expected_queue'],[x['queue'] for x in actual])
    c=oracle['checks'][3];actual=[x for x in facts['relations'] if x['kind']=='messaging_publish' and x['owner']==c['expected_publisher']]
    check(c['id']+':address',len(actual)==1 and actual[0]['routing_key']==c['expected_address_literal'] and actual[0]['overload_argument_count']==c['expected_argument_count'])
    c=oracle['checks'][4];actual=[x for x in facts['relations'] if x['kind']=='http_call' and x['source_path']==c['source_path']]
    match=[x for x in actual if x['http_method']==c['expected_method'] and any(a['target_entity']==c['expected_target_via_explicit_same_class_argument'] and a['path_template']==c['expected_literal_path'] for a in x['url_alternatives'])]
    check(c['id']+':explicit-argument-chain',len(match)==1,1,len(match))
    check(c['id']+':no-invented-handler',bool(match) and all(not a['target_handler_candidates'] for x in match for a in x['url_alternatives']))
    c=oracle['checks'][5];repos=[x for x in facts['repositories'] if x['source_path']==c['source_path']]
    check(c['id']+':repository-interface',len(repos)==1 and repos[0]['class']==c['expected_repository_class'] and repos[0]['base_interface']==c['expected_base_interface'])
    methods=sorted(x['java_method'] for x in facts['operations'] if x['kind']=='java_repository_method' and x['source_path']==c['source_path'])
    check(c['id']+':declared-methods',methods==sorted(c['expected_methods']),sorted(c['expected_methods']),methods)
    config=[x for x in facts['config_facts'] if x['source_path']==c['config_source_path'] and x['key']=='spring.datasource.url']
    check(c['id']+':datasource-separate',len(config)==1 and config[0]['line']==c['config_line'])
    check(c['id']+':repo-runtime-name-null',all(x['runtime_name'] is None for x in facts['operations'] if x['kind']=='java_repository_method'))
    c=oracle['checks'][6];beans=[x for x in facts['client_beans'] if x['owner']==c['expected_owner']]
    check(c['id']+':bean-annotation',len(beans)==1 and beans[0]['load_balanced_annotation']==c['expected_loadbalanced'])
    # Coverage is counted from the independent acquisition plan, not from facts' summary.
    expected_java=sorted(p for p in rows if p.endswith('.java'))
    check('plan-java-file-coverage',expected_java==sorted(x['source_path'] for x in facts['file_index']),len(expected_java),len(facts['file_index']))
    check('no-pending-source',not facts['pending'])
    check('all-source-delimiters-balanced',all(x['balanced_delimiters'] for x in facts['file_index']))
    check('no-current-relations-from-test-or-old-docs',all('/src/main/' in x['source_path'] and not x['source_path'].startswith('old-docs/') for x in facts['relations']))
    check('every-http-call-has-caller-method-id',all(x.get('java_method_id') for x in facts['relations'] if x['kind']=='http_call'))
    check('every-data-call-has-caller-method-id',all(x.get('caller_method_id') for x in facts['data_calls']))
    check('every-repository-class-resolves-import',all(x.get('repository_class') for x in facts['data_calls']))
    # Independent token count: actual RestTemplate call counts must account for all
    # client method occurrences after removing comments, on declared receiver names.
    # This is an independent simpler scan; exact disagreement remains visible.
    direct_count=0;unaccounted=[];mapping_sites=[]
    for p in expected_java:
        if not any(x['source_path']==p and x['scope']=='current-main' for x in facts['file_index']):continue
        text=source(p)
        # Protect strings so comment stripping does not interpret http:// as a comment.
        lex=re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/')
        clean=lex.sub(lambda m:m[0] if m[0][0] in '\"\'' else re.sub(r'[^\n]',' ',m[0]),text)
        firstclass=re.search(r'\b(?:class|interface)\s+\w+',clean)
        for m in re.finditer(r'@(GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping|RequestMapping)\b',clean):
            if firstclass and m.start()<firstclass.start():continue
            mapping_sites.append((p,clean.count('\n',0,m.start())+1))
        names=set(re.findall(r'\bRestTemplate\s+(\w+)',clean))
        for name in names:
            for m in re.finditer(r'\b'+re.escape(name)+r'\s*\.\s*(exchange|getForObject|getForEntity|postForObject|postForEntity|put|delete|patchForObject|execute|headForHeaders|optionsForAllow)\s*\(',clean):
                direct_count+=1
                line=clean.count('\n',0,m.start())+1
                if not any(x['kind']=='http_call' and x['source_path']==p and x['line']==line for x in facts['relations']):unaccounted.append({'source_path':p,'line':line,'literal':m[0]})
    check('independent-http-callsite-count',direct_count==sum(x['kind']=='http_call' for x in facts['relations']),direct_count,sum(x['kind']=='http_call' for x in facts['relations']))
    check('independent-http-callsite-members',not unaccounted,[],unaccounted)
    actual_mapping_sites=sorted(set((x['source_path'],x['line']) for x in facts['operations'] if x['kind']=='http_handler'))
    check('independent-handler-annotation-sites',sorted(set(mapping_sites))==actual_mapping_sites,len(set(mapping_sites)),len(actual_mapping_sites))
    output={'task':'T-038','kind':'supplemental extraction validation','chronology':oracle['chronology'],
      'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_facts_sha256':hashlib.sha256((HERE/'source-facts.json').read_bytes()).hexdigest(),
      'oracle_sha256':hashlib.sha256((HERE/'manual-oracle.json').read_bytes()).hexdigest(),'checks':results,
      'summary':{'checks':len(results),'passed':sum(x['ok'] for x in results),'failed':sum(not x['ok'] for x in results),'elapsed_seconds':time.time()-started},
      'limits':['Checks do not establish dataset lineage, deployed/runtime reachability, or generic Java type inference.',
                'The direct callsite scanner checks the same explicitly enumerated RestTemplate API family; other client families are surveyed in pattern_index and require inspection.',
                'Handwritten supplemental oracle validates selected real patterns, not every source branch or every method declaration.']}
    (HERE/'checks.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    hist=HERE/'check-history';hist.mkdir(exist_ok=True)
    (hist/(datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'.json')).write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output['summary'],indent=2))
    for x in results:
        if not x['ok']:print(json.dumps(x,ensure_ascii=False))

if __name__=='__main__':main()
