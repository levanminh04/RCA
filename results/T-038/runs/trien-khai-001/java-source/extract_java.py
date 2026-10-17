"""T-038: verified, conservative source survey; does not execute application code.

Only writes below its own java-source/ directory. Literal facts are separated
from dynamic templates and from runtime claims. Java lexical tokens ignore
comments, preserve source offsets, and balance parentheses/braces.
"""
from __future__ import annotations
import collections
import datetime
import hashlib
import json
import pathlib
import re
import sys
import time
import xml.etree.ElementTree as ET

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[4]
PLAN = REPO / 'results/T-038/runs/metadata-de-xuat-001/de-xuat-tai.json'
ACQUISITION = REPO / 'results/T-038/runs/tai-nguon-001/manifest.json'
TOKEN = re.compile(r'(?P<space>\s+)|(?P<comment>//[^\n]*|/\*[\s\S]*?\*/)|(?P<string>"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|(?P<id>[A-Za-z_$][\w$]*)|(?P<number>\d+(?:\.\d+)*)|(?P<symbol>.)')
MAP_NAMES = {'RequestMapping', 'GetMapping', 'PostMapping', 'PutMapping', 'DeleteMapping', 'PatchMapping'}
MAP_VERBS = {'GetMapping':'GET', 'PostMapping':'POST', 'PutMapping':'PUT', 'DeleteMapping':'DELETE', 'PatchMapping':'PATCH'}
HTTP_METHODS = {'exchange', 'getForObject', 'getForEntity', 'postForObject', 'postForEntity', 'put', 'delete', 'patchForObject', 'execute', 'headForHeaders', 'optionsForAllow'}

def dump(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def gitblob(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def toks(text):
    return [(m.group(), m.start(), m.end()) for m in TOKEN.finditer(text) if m.lastgroup not in {'space','comment'}]

def join(ts):
    return ''.join(t[0] for t in ts)

def strings(ts):
    out=[]
    for t in ts:
        if t[0].startswith('"'):
            try: out.append(json.loads(t[0]))
            except ValueError: out.append(t[0][1:-1])
    return out

def split_args(ts):
    out=[]; start=0; depth=0
    for i,t in enumerate(ts):
        if t[0] in ('(', '[', '{'):depth+=1
        elif t[0] in (')',']','}'):depth-=1
        elif t[0]==',' and depth==0:out.append(ts[start:i]);start=i+1
    if start < len(ts):out.append(ts[start:])
    return out

def line_at(text, pos): return text.count('\n',0,pos)+1

def evidence(path,text,start,end,limit=1100):
    literal=text[start:end]
    return {'source_path':path,'line':line_at(text,start),'end_line':line_at(text,end),
            'literal':literal if len(literal)<=limit else literal[:limit]+' [TRUNCATED; locator is complete]',
            'literal_truncated':len(literal)>limit}

def balanced(ts):
    pairs={}; stack=[]; depths=[]; depth=0; errors=[]
    for i,(v,*_) in enumerate(ts):
        depths.append(depth)
        if v in ('(','{','['):
            stack.append((v,i))
            if v=='{':depth+=1
        elif v in (')','}',']'):
            if v=='}':depth-=1
            if stack and {'(':')','{':'}','[':']'}[stack[-1][0]]==v:
                _,j=stack.pop();pairs[j]=i;pairs[i]=j
            else:errors.append(i)
    return pairs,depths,errors+([x[1] for x in stack])

def annotations(ts,pairs):
    out=[];i=0
    while i<len(ts)-1:
        if ts[i][0]!='@':i+=1;continue
        j=i+1;name=ts[j][0]
        while j+2<len(ts) and ts[j+1][0]=='.':j+=2;name+='.'+ts[j][0]
        end=j;args=[]
        if j+1<len(ts) and ts[j+1][0]=='(' and j+1 in pairs:
            end=pairs[j+1];args=ts[j+2:end]
        out.append({'name':name.rsplit('.',1)[-1],'start_i':i,'end_i':end,'args':args})
        i=end+1
    return out

def mapping_values(a):
    args=a['args']; named={}; positional=[]
    for part in split_args(args):
        if len(part)>2 and part[1][0]=='=': named[part[0][0]]=part[2:]
        else:positional+=part
    paths=strings(named.get('path',named.get('value',positional)))
    if not paths: paths=['']
    methods=[MAP_VERBS[a['name']]] if a['name'] in MAP_VERBS else [t[0] for t in named.get('method',[]) if t[0] in {'GET','POST','PUT','DELETE','PATCH','HEAD','OPTIONS','TRACE'}]
    if not methods:methods=['ANY']
    constraints={k:join(v) for k,v in named.items() if k not in {'path','value','method'}}
    return paths,methods,constraints

def java_parse(path,text):
    ts=toks(text);pairs,depths,errors=balanced(ts);anns=annotations(ts,pairs)
    cls_i=next((i for i,t in enumerate(ts) if t[0] in {'class','interface','enum'} and i+1<len(ts)),None)
    if cls_i is None:return {'tokens':ts,'pairs':pairs,'depths':depths,'annotations':anns,'methods':[],'class':None,'errors':errors}
    cls=ts[cls_i+1][0]
    cls_open=next((i for i in range(cls_i,len(ts)) if ts[i][0]=='{'),None)
    if cls_open is None:return {'tokens':ts,'pairs':pairs,'depths':depths,'annotations':anns,'methods':[],'class':cls,'errors':errors}
    level=depths[cls_open]+1; methods=[];covered_until=-1;previous=cls_open+1
    class_ranges=[]
    for ci,ct in enumerate(ts):
        if ct[0] not in {'class','interface','enum'} or ci+1>=len(ts) or (ci and ts[ci-1][0]=='.'):continue
        oi=ci+2
        while oi<len(ts) and ts[oi][0] not in {'{',';'}:oi+=1
        if oi<len(ts) and ts[oi][0]=='{' and oi in pairs:
            class_ranges.append({'name':ts[ci+1][0],'open_i':oi,'end_i':pairs[oi],'level':depths[oi]+1})
    for i,t in enumerate(ts):
        if t[0]!='(' or i not in pairs or i<=covered_until or i<cls_open:continue
        containers=[c for c in class_ranges if c['open_i']<i<c['end_i'] and c['level']==depths[i]]
        if not containers:continue
        container=max(containers,key=lambda c:c['open_i']);method_level=container['level'];method_cls_open=container['open_i']
        name=ts[i-1][0] if i else ''
        if not re.fullmatch(r'[A-Za-z_$][\w$]*',name) or name in {'if','for','while','switch','catch','synchronized','new','this','super'}:continue
        if i>1 and ts[i-2][0] in {'.','@','new'}:continue
        if any(a['start_i']<=i<=a['end_i'] for a in anns):continue
        close=pairs[i];j=close+1
        while j<len(ts) and ts[j][0] not in {'{',';','=','}'}:j+=1
        if j>=len(ts) or ts[j][0] not in {'{',';'}:continue
        # A method declaration cannot contain an assignment at the class level.
        k=i-2
        while k>method_cls_open and not (ts[k][0]==';' and depths[k]<=method_level) and not (ts[k][0]=='}' and depths[k]-1<=method_level) and not (ts[k][0]=='{' and depths[k]<method_level):k-=1
        segment=ts[k+1:i-1]
        if any(x[0]=='=' and depths[k+1+n]==method_level and not any(a['start_i']<=k+1+n<=a['end_i'] for a in anns) for n,x in enumerate(segment)):continue
        end=pairs.get(j,j) if ts[j][0]=='{' else j
        start_i=k+1
        own_anns=[a for a in anns if max(previous,method_cls_open+1)<=a['start_i']<i and a['end_i']<i and depths[a['start_i']]==method_level]
        sigstart=ts[start_i][1] if start_i<len(ts) else ts[i-1][1]
        for a in own_anns:
            if a['end_i']<start_i:sigstart=min(sigstart,ts[a['start_i']][1])
        classname='.'.join(c['name'] for c in class_ranges if c['open_i']<i<c['end_i'])
        methods.append({'name':name,'declaring_class':classname,'open_i':i,'close_i':close,'body_i':j,'end_i':end,'start_i':start_i,
                        'start':sigstart,'end':ts[end][2],'annotations':own_anns,
                        'signature':text[ts[start_i][1]:ts[j][1]].strip(),
                        'parameter_text':text[ts[i][2]:ts[close][1]],
                        'has_body':ts[j][0]=='{'})
        covered_until=end;previous=end+1
    class_anns=[a for a in anns if a['end_i']<cls_i]
    package=''
    for i,t in enumerate(ts):
        if t[0]=='package':
            j=i+1
            while j<len(ts) and ts[j][0]!=';':j+=1
            package=join(ts[i+1:j]);break
    return {'tokens':ts,'pairs':pairs,'depths':depths,'annotations':anns,'methods':methods,'class':cls,
            'class_i':cls_i,'class_open':cls_open,'class_annotations':class_anns,'package':package,'errors':errors}

def owner_method(parsed,pos):
    return next((m for m in parsed['methods'] if m['start']<=pos<=m['end']),None)

def assignments(ts,start,end):
    out=collections.defaultdict(list)
    for i in range(start+1,end):
        if ts[i][0]!='=' or not re.fullmatch(r'[A-Za-z_$][\w$]*',ts[i-1][0]):continue
        if i+1<len(ts) and ts[i+1][0]=='=':continue
        j=i+1;depth=0
        while j<end:
            v=ts[j][0]
            if v in ('(','[','{'):depth+=1
            elif v in (')',']','}'):
                if depth<=0:break
                depth-=1
            if depth==0 and v==';':break
            j+=1
        out[ts[i-1][0]].append((i,ts[i+1:j]))
    return out

def resolve(expr,assigns,call_i,helper_literal,seen=None):
    seen=set() if seen is None else set(seen)
    if not expr:return '',True,[]
    while len(expr)>1 and expr[0][0]=='(' and expr[-1][0]==')':expr=expr[1:-1]
    parts=[];dynamic=False;reasons=[];i=0
    while i<len(expr):
        v=expr[i][0]
        if v=='+':i+=1;continue
        if v.startswith('"'):
            try:parts.append(json.loads(v))
            except ValueError:parts.append(v[1:-1])
            i+=1;continue
        if v=='getServiceUrl' and helper_literal and i+3<len(expr) and expr[i+1][0]=='(' and expr[i+3][0]==')' and expr[i+2][0].startswith('"'):
            parts.append('http://'+json.loads(expr[i+2][0]));i+=4;continue
        if re.fullmatch(r'[A-Za-z_$][\w$]*',v) and (i+1==len(expr) or expr[i+1][0] not in {'.','('}):
            prior=[x for x in assigns.get(v,[]) if x[0]<call_i]
            if v not in seen and prior:
                vals=[]
                for at,ex in prior:
                    val,dyn,why=resolve(ex,assigns,at,helper_literal,seen|{v});vals.append(val);dynamic|=dyn;reasons+=why
                if len(set(vals))==1:parts.append(vals[-1])
                else:parts.append('{'+v+'}');dynamic=True;reasons.append('multiple_assignments:'+v)
            else:parts.append('{'+v+'}');dynamic=True
            i+=1;continue
        # Preserve an unresolved expression as one placeholder, never call it a literal.
        rest=join(expr[i:]);parts.append('{EXPR:'+rest+'}');dynamic=True;reasons.append('unresolved_expression');break
    return ''.join(parts),dynamic,sorted(set(reasons))

def resolve_options(expr,assigns,call_i,helper_literal,seen=None):
    """Union source assignments; retain branch alternatives instead of choosing one.

    This is a syntactic may-call survey, not path-sensitive execution. Expressions
    that are not literals remain explicit placeholders. Concatenation preserves
    delimiters around dynamic path fragments.
    """
    seen=set() if seen is None else set(seen)
    if not expr:return ['{EMPTY}'],['empty_expression']
    pieces=[];start=0;depth=0
    for i,t in enumerate(expr):
        if t[0] in ('(','[','{'):depth+=1
        elif t[0] in (')',']','}'):depth-=1
        elif t[0]=='+' and depth==0:pieces.append(expr[start:i]);start=i+1
    pieces.append(expr[start:]);values=[''];reasons=[]
    for part in pieces:
        s=join(part)
        if len(part)==1 and part[0][0].startswith('"'):
            options=strings(part)
        elif len(part)==4 and part[0][0]=='getServiceUrl' and part[1][0]=='(' and part[2][0].startswith('"') and part[3][0]==')' and helper_literal:
            options=['http://'+strings([part[2]])[0]]
        elif len(part)==1 and re.fullmatch(r'[A-Za-z_$][\w$]*',part[0][0]):
            v=part[0][0];prior=[x for x in assigns.get(v,[]) if x[0]<call_i]
            if prior and v not in seen:
                options=[]
                for at,ex in prior:
                    vals,why=resolve_options(ex,assigns,at,helper_literal,seen|{v});options+=vals;reasons+=why
                options=sorted(set(options))
                if len(options)>1:reasons.append('source_assignment_alternatives:'+v)
            else:options=['{'+v+'}'];reasons.append('dynamic_identifier:'+v)
        else:
            options=['{EXPR:'+s+'}'];reasons.append('dynamic_expression:'+s)
        values=sorted(set(a+b for a in values for b in options))
        if len(values)>32:return ['{EXPR:'+join(expr)+'}'],['alternative_limit_exceeded']
    return values,sorted(set(reasons))

def main():
    started=time.time();plan=load(PLAN);root=REPO/plan['proposed_destination'];rows={x['path']:x for x in plan['proposed_files']}
    facts={'task':'T-038','producer':'extract_java.py','status':'source-facts; conditional reference snapshot; not runtime confirmation',
           'repository':plan['repository'],'tag':plan['tag'],'commit':plan['commit'],'tree':plan['tree'],
           'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'plan_sha256':hashlib.sha256(PLAN.read_bytes()).hexdigest(),
           'acquisition_manifest_sha256':hashlib.sha256(ACQUISITION.read_bytes()).hexdigest(),
           'entities':[],'operations':[],'relations':[],'resource_bindings':[],'background':[],'client_beans':[],
           'java_methods':[],'repositories':[],'data_calls':[],'support_calls':[],'pattern_index':[],'config_facts':[],'file_index':[], 'pending':[], 'open':[]}
    sources={};java={};configs={};poms={};verified=[]
    for path,row in sorted(rows.items()):
        if not (path.endswith('.java') or pathlib.PurePosixPath(path).name=='pom.xml' or ('/src/main/resources/' in path and re.search(r'\.(?:ya?ml|properties|xml)$',path))):continue
        f=root/path
        if not f.is_file():facts['pending'].append(path);continue
        b=f.read_bytes()
        if len(b)!=row['bytes'] or gitblob(b)!=row['git_blob']:raise RuntimeError('SOURCE HASH MISMATCH: '+path)
        verified.append({'path':path,'bytes':len(b),'git_blob':row['git_blob'],'sha256':hashlib.sha256(b).hexdigest()})
        text=b.decode('utf-8-sig');sources[path]=text
        if path.endswith('.java'):java[path]=java_parse(path,text)
        elif pathlib.PurePosixPath(path).name=='pom.xml':poms[path]=text
        else:configs[path]=text
    # Maven parent modules are an inventory source independent of observed trace nodes.
    modules=[]
    if 'pom.xml' in poms:
        text=poms['pom.xml'];mods=re.finditer(r'<module>\s*([^<]+)\s*</module>',text)
        for match in mods:
            mod=match[1].strip();modules.append(mod)
            apps=[(p,j) for p,j in java.items() if p.startswith(mod+'/src/main/') and any(a['name']=='SpringBootApplication' for a in j.get('class_annotations',[]))]
            names=[]
            cfg_evidence=[]
            for p,t in configs.items():
                if not p.startswith(mod+'/'):continue
                # Names are also preserved in the complete configuration fact table below.
                for m in re.finditer(r'(?m)^\s*name\s*:\s*([\w${}:.\-]+)\s*$',t):
                    if 'application:' in t[max(0,m.start()-100):m.start()]:names.append(m[1]);cfg_evidence.append(evidence(p,t,m.start(),m.end()))
                for m in re.finditer(r'(?m)^spring\.application\.name\s*=\s*(.+)$',t):names.append(m[1].strip());cfg_evidence.append(evidence(p,t,m.start(),m.end()))
            facts['entities'].append({'id':mod,'owner':mod,'entity_kind':'service' if apps else 'library_or_build_module',
              'application_names':sorted(set(names)),'application_classes':[p for p,_ in apps],
              **evidence('pom.xml',text,match.start(),match.end()),'additional_source_evidence':cfg_evidence,
              'condition':'declared Maven module and source configuration; deployment/runtime activation not inferred'})
    # Flatten key-bearing resource configuration lines, without claiming that every profile is active.
    config_patterns=re.compile(r'(?i)(?:spring\.(?:application|datasource|data\.mongodb|rabbitmq|redis|cloud)|(?:url|uri|host|port|database|server-addr|exchange|routing|queue|name|profiles))')
    for path,text in configs.items():
        module=path.split('/')[0];stack=[]
        for n,line in enumerate(text.splitlines(),1):
            if line.lstrip().startswith(('#','<!--')):continue
            m=re.match(r'^(\s*)([\w.\-]+)\s*:\s*(.*?)\s*$',line)
            if m:
                indent=len(m[1]);key=m[2];value=m[3]
                while stack and stack[-1][0]>=indent:stack.pop()
                full='.'.join([x[1] for x in stack]+[key])
                if not value:stack.append((indent,key));continue
            else:
                m=re.match(r'^\s*([\w.\-]+)\s*=\s*(.*?)\s*$',line)
                if not m:continue
                full=m[1];value=m[2]
            if any(x in full.lower() for x in ['password','username','user.']):continue
            if config_patterns.search(full):facts['config_facts'].append({'owner':module,'key':full,'value_expression':value,'source_path':path,'line':n,'end_line':n,'literal':line,'condition':'configuration candidate; profile/env override/runtime activation must be checked'})
    # Constants in current modules: needed for queue addresses, not inferred from peer names.
    constants={}
    for path,j in java.items():
        if '/src/main/' not in path or path.startswith('old-docs/'):continue
        ts=j['tokens']
        for i in range(1,len(ts)-3):
            if ts[i][0]=='=' and ts[i+1][0].startswith('"') and ts[i+2][0]==';':
                constants[(path.split('/')[0],(j['class'] or '')+'.'+ts[i-1][0])]=(strings([ts[i+1]])[0],evidence(path,sources[path],ts[i-1][1],ts[i+2][2]))
    for path,j in java.items():
        text=sources[path];module=path.split('/')[0];current=module in modules and '/src/main/' in path
        scope='current-main' if current else ('test-source' if '/src/test/' in path else 'historical-source')
        ts=j['tokens'];pairs=j['pairs'];cls=j['class'];fq=(j.get('package','')+'.'+str(cls)).strip('.')
        facts['file_index'].append({'source_path':path,'owner':module,'scope':scope,'class':fq,'method_count':len(j['methods']),'balanced_delimiters':not j['errors'],'lexical_errors':j['errors']})
        classpaths=['']
        for a in j.get('class_annotations',[]):
            if a['name']=='RequestMapping':classpaths=mapping_values(a)[0]
        helper=[m for m in j['methods'] if m['name']=='getServiceUrl']
        helper_literal=bool(helper) and all(re.search(r'return\s*"http://"\s*\+\s*serviceName\s*;',text[m['start']:m['end']]) for m in helper)
        rest_receivers=set(re.findall(r'\bRestTemplate\s+([A-Za-z_$][\w$]*)',join(ts))) # fixed below with spaces
        token_text=' '.join(t[0] for t in ts)
        rest_receivers.update(re.findall(r'\bRestTemplate\s+([A-Za-z_$][\w$]*)',token_text))
        repo_variables={var:typ for typ,var in re.findall(r'\b([A-Za-z_$][\w$]*Repository)\s+([A-Za-z_$][\w$]*)',token_text)}
        def method_ref(method):
            if not method:return None
            mfq=(j.get('package','')+'.'+method.get('declaring_class',cls)).strip('.')
            return f'{module}::{mfq}#{method["name"]}({re.sub(chr(10)," ",method["parameter_text"]).strip()})'
        for m in j['methods']:
            ev=evidence(path,text,m['start'],m['end'],450)
            method_fq=(j.get('package','')+'.'+m.get('declaring_class',cls)).strip('.')
            method_id=f'{module}::{method_fq}#{m["name"]}({re.sub(chr(10)," ",m["parameter_text"]).strip()})'
            rec={'id':method_id,'owner':module,'class':method_fq,'java_method':m['name'],'signature':m['signature'],'scope':scope,
                 'annotation_names':[a['name'] for a in m['annotations']],**ev,'condition':'source declaration; reachability and runtime name not confirmed'}
            facts['java_methods'].append(rec)
            if current:
                maps=[a for a in m['annotations'] if a['name'] in MAP_NAMES]
                for a in maps:
                    paths,verbs,constraints=mapping_values(a)
                    for base in classpaths:
                        for suffix in paths:
                            endpoint='/'+'/'.join((base+'/'+suffix).split('/')[1:]) if (base+'/'+suffix).startswith('/') else '/'+base+'/'+suffix
                            endpoint=re.sub('/+','/',endpoint)
                            for verb in verbs:
                                facts['operations'].append({'id':module+'::'+verb+' '+endpoint,'owner':module,'kind':'http_handler','http_method':verb,'path':endpoint,'java_method_id':method_id,'java_class':fq,'java_method':m['name'],
                                  'constraints':constraints,**evidence(path,text,ts[a['start_i']][1],ts[m['body_i']][1]),'condition':'declared Spring mapping; runtime span name/activation not inferred'})
                if '/service/' in path or '/serivce/' in path or '/repository/' in path:
                    facts['operations'].append({'id':method_id,'owner':module,'kind':'java_repository_method' if '/repository/' in path else 'java_service_method','java_class':method_fq,'java_method':m['name'],'runtime_name':None,**ev,'condition':'source method; not an invented HTTP/span operation'})
                for a in m['annotations']:
                    if a['name'] in {'Async','Scheduled','RabbitListener','EventListener','PostConstruct','PreDestroy','Bean'}:
                        item={'owner':module,'java_method_id':method_id,'kind':a['name'],'annotation_args':join(a['args']),**evidence(path,text,ts[a['start_i']][1],ts[a['end_i']][2]),'condition':'source declaration; activation depends on configuration/call path'}
                        facts['background'].append(item)
                        if a['name']=='RabbitListener':
                            args=join(a['args']);candidate=strings(a['args'])
                            const=next((v for (mod,key),v in constants.items() if mod==module and key in args),None)
                            queue=candidate[0] if candidate else (const[0] if const else None)
                            facts['relations'].append({'kind':'messaging_consume','source_entity':None,'target_entity':module,'owner':module,'java_method_id':method_id,'queue':queue,'queue_expression':args,'exchange':None,'routing_key':None,
                              'queue_constant_evidence':const[1] if const else None,**evidence(path,text,ts[a['start_i']][1],ts[a['end_i']][2]),'condition':'listener declaration; queue address resolved only from same-module source constant; broker instance/runtime delivery OPEN'})
                if 'RestTemplate' in m['signature'] and any(a['name']=='Bean' for a in m['annotations']):
                    facts['client_beans'].append({'owner':module,'java_method_id':method_id,'type':'RestTemplate','load_balanced_annotation':any(a['name']=='LoadBalanced' for a in m['annotations']),**ev,'condition':'bean source declaration; annotation is not a measured discovery request'})
        if not current:continue
        surveyed_patterns={'rpc_or_other_client':{'FeignClient','WebClient','HttpClient','HttpURLConnection','ManagedChannel','Socket','URL','URLConnection'},
          'data_client':{'MongoTemplate','JdbcTemplate','RedisTemplate','StringRedisTemplate','DriverManager','EntityManager'},
          'async_background':{'Thread','Executor','ExecutorService','Executors','ThreadPoolExecutor','ThreadPoolTaskExecutor','Scheduled','Async','Callable','CompletableFuture','TraceCrossThread','AsyncResult','Future'},
          'messaging':{'AmqpTemplate','RabbitTemplate','RabbitListener','Queue','Exchange','Binding','KafkaTemplate','KafkaListener','JmsTemplate'},
          'discovery':{'DiscoveryClient','getInstances','LoadBalanced'},'mail':{'JavaMailSender','sendEmail'}}
        for kind,terms in surveyed_patterns.items():
            for ti,token in enumerate(ts):
                if token[0] in terms:facts['pattern_index'].append({'owner':module,'kind':kind,'token':token[0],**evidence(path,text,token[1],token[2]),'condition':'lexical survey occurrence; declaration/reference/call role must be inspected'})
        # Repository declarations establish the local data adapter, not the DB instance.
        if '/repository/' in path:
            mm=re.search(r'\b(?:interface|class)\s+(\w+)\s+(?:extends|implements)\s+([\w.]+)\s*(?:<([^>]+)>)?',token_text)
            if mm:
                facts['repositories'].append({'owner':module,'class':fq,'base_interface':mm[2],'generic_arguments':mm[3],'source_path':path,'line':line_at(text,ts[j['class_i']][1]),'end_line':line_at(text,ts[j['class_open']][1]),'literal':mm[0],'condition':'data adapter source; concrete DB from configuration is separate'})
        for i in range(2,len(ts)-2):
            if ts[i][0]!='.' or ts[i-1][0] not in repo_variables or ts[i+2][0]!='(' or i+2 not in pairs:continue
            typ=repo_variables[ts[i-1][0]];end=pairs[i+2];method=owner_method(j,ts[i][1])
            imports=re.findall(r'\bimport\s+([\w.]+\.'+re.escape(typ)+r')\s*;',text)
            fqrepo=imports[0] if len(imports)==1 else None
            decl=next((n for n,t in enumerate(ts[:-1]) if t[0]==typ and ts[n+1][0]==ts[i-1][0]),None)
            facts['data_calls'].append({'kind':'repository_call','owner':module,'source_entity':module,'caller_method_id':method_ref(method),
              'java_method':method['name'] if method else None,'repository_variable':ts[i-1][0],'repository_type':typ,'repository_class':fqrepo,
              'repository_method':ts[i+1][0],'runtime_name':None,'field_declaration_evidence':evidence(path,text,ts[decl][1],ts[decl+1][2]) if decl is not None else None,
              **evidence(path,text,ts[i-1][1],ts[end][2]),'condition':'actual source call on declared repository-typed variable; proxy/overload/runtime DB query name OPEN; datasource configuration separate'})
        support_types={var:typ for typ,var in re.findall(r'\b(JavaMailSender|DiscoveryClient|ExecutorService|Executor|ThreadPoolTaskExecutor|PollThread)\s+([A-Za-z_$][\w$]*)',token_text)}
        for i in range(2,len(ts)-2):
            if ts[i][0]!='.' or ts[i-1][0] not in support_types or ts[i+2][0]!='(' or i+2 not in pairs:continue
            typ=support_types[ts[i-1][0]];call=ts[i+1][0];end=pairs[i+2];method=owner_method(j,ts[i][1]);args=split_args(ts[i+3:end])
            kind=None
            if typ=='JavaMailSender' and call=='send':kind='mail_send'
            if typ=='DiscoveryClient' and call=='getInstances':kind='discovery_lookup'
            if typ in {'ExecutorService','Executor','ThreadPoolTaskExecutor'} and call in {'submit','execute','invokeAll','invokeAny'}:kind='executor_dispatch'
            if typ=='PollThread' and call=='start':kind='thread_start'
            if kind:
                facts['support_calls'].append({'kind':kind,'owner':module,'caller_method_id':method_ref(method),'receiver':ts[i-1][0],'declared_type':typ,'called_method':call,'argument_expressions':[join(a) for a in args],
                  **evidence(path,text,ts[i-1][1],ts[end][2]),'condition':'actual source call; external endpoint/dispatch/reachability separate from reference snapshot facts'})
        # Each actual RestTemplate method call is recorded. String constants alone are not calls.
        for i in range(2,len(ts)-2):
            if ts[i][0]!='.' or ts[i-1][0] not in rest_receivers or ts[i+1][0] not in HTTP_METHODS or ts[i+2][0]!='(' or i+2 not in pairs:continue
            method=owner_method(j,ts[i][1]);end=pairs[i+2];args=split_args(ts[i+3:end]);verb=ts[i+1][0]
            methname=method['name'] if method else None
            start=method['body_i'] if method else j.get('class_open',0)
            assigns=assignments(ts,start,i)
            template,dyn,why=resolve(args[0] if args else [],assigns,i,helper_literal)
            option_templates,option_why=resolve_options(args[0] if args else [],assigns,i,helper_literal)
            interprocedural_evidence=[]
            if method:
                parameters=[]
                for part in split_args(ts[method['open_i']+1:method['close_i']]):
                    ids=[v[0] for v in part if re.fullmatch(r'[A-Za-z_$][\w$]*',v[0])]
                    parameters.append(ids[-1] if ids else None)
                # One-class, explicit argument substitution; no inferred call graph.
                for parameter_index,parameter in enumerate(parameters):
                    if not parameter or not any('{'+parameter+'}' in option for option in option_templates):continue
                    same_name=[m for m in j['methods'] if m['name']==method['name']]
                    if len(same_name)!=1:continue
                    parameter_values=[]
                    for ci,ct in enumerate(ts[:-1]):
                        if ct[0]!=method['name'] or ts[ci+1][0]!='(' or ci+1 not in pairs or ci+1==method['open_i']:continue
                        caller=owner_method(j,ct[1])
                        if not caller or caller is method:continue
                        ce=pairs[ci+1];ca=split_args(ts[ci+2:ce])
                        if len(ca)!=len(parameters):continue
                        caller_assigns=assignments(ts,caller['body_i'],ci)
                        vals,reasons=resolve_options(ca[parameter_index],caller_assigns,ci,helper_literal)
                        parameter_values+=vals;option_why+=['same_class_argument_substitution:'+parameter]+reasons
                        interprocedural_evidence.append(evidence(path,text,ct[1],ts[ce][2]))
                        identifiers={x[0] for x in ca[parameter_index]}
                        for name in identifiers:
                            for at,ex in caller_assigns.get(name,[]):
                                if ex:interprocedural_evidence.append(evidence(path,text,ts[at-1][1],ex[-1][2]))
                    if parameter_values:
                        option_templates=sorted(set(option.replace('{'+parameter+'}',val) for option in option_templates for val in parameter_values))
            target=re.match(r'https?://([A-Za-z0-9_.\-]+)(?::([0-9]+))?(.*)',template)
            hm=next((x[0] for x in (args[1] if len(args)>1 else []) if x[0] in {'GET','POST','PUT','DELETE','PATCH','HEAD','OPTIONS','TRACE'}),None)
            if verb!='exchange':hm={'getForObject':'GET','getForEntity':'GET','postForObject':'POST','postForEntity':'POST','put':'PUT','delete':'DELETE','patchForObject':'PATCH','headForHeaders':'HEAD','optionsForAllow':'OPTIONS'}.get(verb,hm)
            alternatives=[]
            for option in option_templates:
                tar=re.match(r'https?://([A-Za-z0-9_.\-]+)(?::([0-9]+))?(.*)',option)
                alternatives.append({'url_template':option,'target_entity':tar[1] if tar else None,'path_template':tar[3] if tar else None,'port_literal':tar[2] if tar else None,'dynamic':'{' in option,'target_handler_candidates':[]})
            facts['relations'].append({'kind':'http_call','owner':module,'source_entity':module,'target_entity':target[1] if target else None,'http_method':hm,'url_template':template,'url_expression':join(args[0]) if args else None,
              'path_template':target[3] if target else None,'port_literal':target[2] if target else None,'dynamic':dyn,'resolution_open':why,
              'url_alternatives':alternatives,'alternative_resolution_open':option_why,
              'same_class_argument_evidence':interprocedural_evidence,
              'java_class':fq,'java_method':methname,'java_method_id':method_ref(method),'client_method':verb,'helper_literal_http_plus_serviceName':helper_literal,
              **evidence(path,text,ts[i-1][1],ts[end][2]),'condition':'call site exists; branch/reachability/discovery resolution/runtime activation OPEN'})
        for i in range(2,len(ts)-2):
            if ts[i][0]!='.' or ts[i+1][0] not in {'convertAndSend','send'} or ts[i+2][0]!='(' or i+2 not in pairs:continue
            if not any(t[0] in {'AmqpTemplate','RabbitTemplate'} for t in ts):continue
            end=pairs[i+2];args=split_args(ts[i+3:end]);first=join(args[0]) if args else ''
            const=constants.get((module,first));lit=strings(args[0]) if args else []
            addr=const[0] if const else (lit[0] if lit else None)
            facts['relations'].append({'kind':'messaging_publish','owner':module,'source_entity':module,'target_entity':None,'queue':None,
              'routing_key':addr if len(args)==2 else None,'exchange':'' if len(args)==2 else None,'address_expression':first,
              'overload_argument_count':len(args),'queue_constant_evidence':const[1] if const else None,
              **evidence(path,text,ts[i-1][1],ts[end][2]),'condition':'AmqpTemplate call; 2-arg overload uses default exchange/routing key; queue binding/runtime message delivery not inferred'})
        for term in ['new Thread','extends Thread','new PollThread','Executors .','@ EnableAsync','JavaMailSender','RedisTemplate','StringRedisTemplate','MongoTemplate','DriverManager','Socket','ManagedChannel','WebClient','HttpClient','FeignClient']:
            if term in token_text:
                facts['background'].append({'owner':module,'kind':'lexical_pattern','pattern':term,'source_path':path,'line':1,'end_line':len(text.splitlines()),'literal':term,'condition':'survey locator; inspect declaration/call path before runtime relation'})
    # Resolve target handler candidates only by literal HTTP method and path-template shape.
    endpoints=[x for x in facts['operations'] if x['kind']=='http_handler']
    for rel in facts['relations']:
        if rel['kind']!='http_call':continue
        path=rel.get('path_template');rel['target_handler_candidates']=[]
        shape=lambda x:re.sub(r'\{[^}]*\}','{*}',x.split('?')[0].rstrip('/'))
        def matches(target,p):
            if not p:return []
            result=[]
            for x in endpoints:
                if x['owner']!=target or x['http_method'] not in {rel['http_method'],'ANY'}:continue
                # A literal outgoing parameter value is compatible with a source
                # path variable but remains a candidate rather than runtime proof.
                regex=re.escape(x['path'].rstrip('/'))
                regex=re.sub(r'\\\{[^}]*\\\}',r'[^/]+',regex)
                if shape(x['path'])==shape(p) or re.fullmatch(regex,p.split('?')[0].rstrip('/')):result.append(x['id'])
            return result
        rel['target_handler_candidates']=matches(rel['target_entity'],path)
        for option in rel['url_alternatives']:option['target_handler_candidates']=matches(option['target_entity'],option['path_template'])
    facts['open']=[
      'Application snapshot is a conditional v1.0.0 reference; dataset-to-application/instrumentation/deployment lineage not established.',
      'Lexical source parser is not javac/type inference. All source files are scanned, but reflective/dynamic calls, generated external dependencies, overload dispatch and runtime reachability remain OPEN.',
      'HTTP relation requires an actual RestTemplate call. getServiceUrl is expanded only where the source helper returns http:// + serviceName. Multiple/dynamic assignments are kept unresolved.',
      'Spring request constraints (headers/params/consumes/produces), proxy path rewriting, security filters and conditional beans can affect activation; route declaration does not prove runtime invocation.',
      'Tests and old-docs Java are indexed/scanned but excluded from current runtime entities/relations; root build and deployment coverage must justify activation.',
      'Repository methods identify source data adapters. Configuration defaults are not proof of deployed DB/broker endpoints.',
      'HTTP client path with a dynamic expression may resolve a service endpoint without resolving target operation. No runtime span operation is invented from a Java method.'
    ]
    summary={'java_files':len(java),'java_scope_counts':dict(collections.Counter(x['scope'] for x in facts['file_index'])),
      'entities':len(facts['entities']),'operations_by_kind':dict(collections.Counter(x['kind'] for x in facts['operations'])),
      'relations_by_kind':dict(collections.Counter(x['kind'] for x in facts['relations'])),
      'http_primary_expression_unresolved':sum(x['kind']=='http_call' and not x.get('target_entity') for x in facts['relations']),
      'http_target_unresolved':sum(x['kind']=='http_call' and not any(a['target_entity'] for a in x['url_alternatives']) for x in facts['relations']),
      'http_operation_candidates_empty':sum(x['kind']=='http_call' and not any(a['target_handler_candidates'] for a in x['url_alternatives']) for x in facts['relations']),
      'http_resolved_target_alternatives':sum(bool(a['target_entity']) for x in facts['relations'] if x['kind']=='http_call' for a in x['url_alternatives']),
      'http_empty_initialization_alternatives':sum(a['url_template']=='' for x in facts['relations'] if x['kind']=='http_call' for a in x['url_alternatives']),
      'repositories':len(facts['repositories']),'java_methods':len(facts['java_methods']),'config_facts':len(facts['config_facts']),
      'repository_call_sites':len(facts['data_calls']),'loadbalanced_resttemplate_beans':sum(x['load_balanced_annotation'] for x in facts['client_beans']),
      'lexical_unbalanced_files':[x['source_path'] for x in facts['file_index'] if not x['balanced_delimiters']],
      'verified_input_files':len(verified),'pending_files':len(facts['pending']),'elapsed_seconds':time.time()-started}
    facts['summary']=summary
    dump('source-facts.json',facts);dump('verified-inputs.json',verified);dump('summary.json',summary)
    retained=HERE/'extraction-history'/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    retained.mkdir(parents=True,exist_ok=False)
    for name in ['extract_java.py','source-facts.json','verified-inputs.json','summary.json']:
        (retained/name).write_bytes((HERE/name).read_bytes())
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
