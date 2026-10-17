"""T-038 safe coverage followup. Never executes downloaded application source.

Inputs are verified against approved Git tree before decoding. Image observations
were made with view_image after role/metadata checks; this script verifies their
identity/dimensions and records the observations. PDF content is never decoded.
"""
import collections
import datetime
import hashlib
import io
import json
import pathlib
import re
import struct
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
import zipfile

HERE=pathlib.Path(__file__).resolve().parent
REPO=HERE.parents[4]
BASE=REPO/'results/T-038'
PLAN=BASE/'runs/metadata-de-xuat-001/de-xuat-tai.json'
COVERAGE=BASE/'runs/hoan-tat-trong-quyen-001/before-bao-phu-nguon.json'
RUNTIME=pathlib.Path('C:/Users/84583/.cache/codex-runtimes/codex-primary-runtime/dependencies')

def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def main():
    start=time.time();plan=load(PLAN);oracle=load(HERE/'oracle.json');coverage=load(COVERAGE)
    rows={x['path']:x for x in plan['proposed_files']};source=REPO/plan['proposed_destination']
    old_open=[x for x in coverage['files'] if x['status']=='open'];assert len(old_open)==oracle['old_open_count']
    verified={};texts={};checks=[];records=[]
    def check(name,ok,details=None):checks.append({'check':name,'ok':bool(ok),'details':details})
    def read(p):
        b=(source/p).read_bytes();r=rows[p];assert len(b)==r['bytes'] and blob(b)==r['git_blob'],p
        verified[p]={'path':p,'bytes':len(b),'git_blob':r['git_blob'],'sha256':sha(b)}
        return b
    def text(p):
        if p not in texts:texts[p]=read(p).decode('utf-8-sig')
        return texts[p]
    def evidence(p,lo,hi):
        lines=text(p).splitlines();return {'source_path':p,'line':lo,'end_line':hi,'literal':'\n'.join(lines[lo-1:hi])}
    def found(p,term):
        t=text(p);m=re.search(re.escape(term),t);assert m,(p,term)
        lo=t.count('\n',0,m.start())+1;return evidence(p,lo,t.count('\n',0,m.end())+1)
    root_readme='old-docs/README_OLD_v03.md'
    ui_manifest={'role':'theme/example assets, not application dependency declarations',
                 'source_evidence':[found('ts-ui-dashboard/Dockerfile','COPY static /usr/share/nginx/html')],
                 'condition':'Serving an asset does not make its displayed decoration or wireframe a backend service/edge.'}
    source_line_for_root={'main_interface.png':43,'login.png':51,'select_contace.png':54,'confirm_ticket.png':57,
                         'pay_ticket.png':60,'modify_ticket.png':62,'advanced_search.png':64,
                         'admin_login.png':71,'admin_order_list.png':73,'admin_travel_list.png':75,'test_code.PNG':84}
    for p,expected in oracle['images'].items():
        b=read(p);assert b.startswith(b'\x89PNG\r\n\x1a\n') and b[12:16]==b'IHDR'
        w,h=struct.unpack_from('>II',b,16);check('PNG dimensions:'+p,[w,h]==expected[:2],{'actual':[w,h],'expected':expected[:2]})
        source_evidence=[]
        if p.startswith('image/'):
            lo=source_line_for_root[pathlib.PurePosixPath(p).name]
            source_evidence=[evidence(root_readme,max(1,lo-2),lo+1)]
            if p.endswith('main_interface.png'):source_evidence.append(found('README.md','![screenshot](./image/main_interface.png)'))
            impact='Functional UI/source-configuration illustration. It adds no service identity or directed call beyond declarations already read; business flow is not converted into service edges.'
            cls='application-instructions-UI-screenshot' if not p.endswith('test_code.PNG') else 'test-harness-source-screenshot'
        elif p.startswith('ts-avatar-service/'):
            source_evidence=[evidence('ts-avatar-service/readme.md',1,10),evidence('ts-avatar-service/face_detect.py',6,16)]
            impact='Face photograph fixture; no architecture, endpoint, trace or log content. Not used to infer runtime calls or recognition quality.';cls='avatar-image-fixture'
        else:
            source_evidence=ui_manifest['source_evidence'];impact=ui_manifest['condition'];cls='UI-theme-visual-asset'
        records.append({'path':p,'old_status':'open','proposed_status':'read','read_depth':'verified-origin-and-direct-visual-inspection',
                        'classification':cls,'visual_observation':expected[2],'source_evidence':source_evidence,
                        'binary_metadata':{'format':'PNG','width':w,'height':h},'inventory_relation_effect':impact,
                        'telemetry_content_observed':False,'remaining_uncertainty':'Application screenshots are historical instructions, not proof of v1.0.0 deployment or RE2-TT behavior.' if p.startswith('image/') else None})
    # Source chart requirements identify the two release baselines inspected in the
    # official Helm repository. No Helm/build execution or new source file download.
    swp='deployment/kubernetes-manifests/quickstart-k8s/charts/mysql/templates/.statefulset.yaml.swp'
    b=read(swp);check('VIM swap signature',b.startswith(b'b0VIM 8.2'))
    pattern=re.compile(r'^templates/\.[^/][^/]*$')
    for name,expected in oracle['helm_rule_cases']:check('Helm default rule:'+name,bool(pattern.fullmatch(name))==expected)
    helm_refs=[
      {'url':'https://github.com/helm/helm/blob/v2.11.0/pkg/ignore/rules.go#L46-L50','symbol':'Rules.AddDefaults','observation':'Default rule templates/.?* excludes dotfiles directly in templates/.'},
      {'url':'https://github.com/helm/helm/blob/v2.11.0/pkg/chartutil/load.go#L260-L315','symbol':'LoadDir','observation':'Defaults are installed after optional ignore-file parsing and evaluated before file content is read.'},
      {'url':'https://github.com/helm/helm/blob/v3.0.0-beta.3/internal/ignore/rules.go#L46-L50','symbol':'Rules.AddDefaults','observation':'Same default templates/.?* rule.'},
      {'url':'https://github.com/helm/helm/blob/v3.0.0-beta.3/pkg/chart/loader/directory.go#L43-L107','symbol':'LoadDir','observation':'Defaults are installed even when .helmignore does not exist; matching files are skipped before reading.'}]
    records.append({'path':swp,'old_status':'open','proposed_status':'excluded','read_depth':'verified-VIM-header + documented-loader-control-flow + safe-literal-rule-check',
      'classification':'editor-swap-ignored-by-chart-loader','source_evidence':[evidence('deployment/kubernetes-manifests/quickstart-k8s/charts/mysql/README.md',24,28)],
      'external_primary_sources':helm_refs,'rule':'templates/.?*','chart_relative_path':'templates/.statefulset.yaml.swp','matches_rule':True,
      'reason':'Both documented Helm baseline versions ignore this dotfile via defaults; lack of .helmignore is not evidence of loading it.',
      'inventory_relation_effect':'Excluded from the declared chart-template source path. No swap recovery or speculative resource is needed for that path.',
      'remaining_uncertainty':'Actual deployed tool version/package and nonstandard manual consumers are not known; this is a source-path exclusion under documented loaders, not a RE2-TT deployment claim.'})
    # Archive activation: examine current root/module POMs and checked build inputs.
    ns={'m':'http://maven.apache.org/POM/4.0.0'};pom_rows=[];activation_refs=[];converter_refs=[];build_rows=[]
    for p in sorted(rows):
        if p.startswith(('old-docs/','ts-ticket-office-service/node_modules/')):continue
        is_pom=p=='pom.xml' or len(p.split('/'))==2 and p.startswith('ts-') and p.endswith('/pom.xml')
        is_build=pathlib.PurePosixPath(p).name in {'Dockerfile','Makefile'} or p.startswith(('.github/','hack/','script/')) and p.endswith(('.sh','.yml','.yaml','.py'))
        if not is_pom and not is_build:continue
        t=text(p)
        for m in re.finditer(r'(?i)myproject\.microservices|micro-service-monitoring|old-docs/Lib/myproject|ms-monitoring|spring-cloud-(?:starter-)?(?:sleuth|zipkin)',t):
            activation_refs.append(evidence(p,t.count('\n',0,m.start())+1,t.count('\n',0,m.end())+1))
        for m in re.finditer(r'(?i)Json2Shiviz|TraceTranslator|services-analysis',t):
            converter_refs.append(evidence(p,t.count('\n',0,m.start())+1,t.count('\n',0,m.end())+1))
        if is_pom:
            x=ET.fromstring(t);deps=[]
            for el in x.findall('.//m:dependency',ns):deps.append({k:el.findtext('m:'+k,'',ns) for k in ['groupId','artifactId','version','scope']})
            pom_rows.append({'source_path':p,'profiles':[el.findtext('m:id','',ns) for el in x.findall('m:profiles/m:profile',ns)],'dependencies':deps,'systemPath_declared':bool(x.findall('.//m:systemPath',ns))})
        if is_build:
            imports=[]
            for lo,line in enumerate(t.splitlines(),1):
                if re.search(r'(?i)^\s*(?:COPY|ADD|FROM)|mvn\s|\.m2|helm\s',line):imports.append({'line':lo,'literal':line})
            build_rows.append({'source_path':p,'build_input_references':imports})
    check('active POM coverage',len(pom_rows)==oracle['archive']['active_pom_count'],len(pom_rows))
    check('no declared historical monitoring dependency',len(activation_refs)==oracle['archive']['direct_monitoring_dependency_reference_count'],activation_refs)
    modules=ET.fromstring(text('pom.xml')).findall('m:modules/m:module',ns)
    module_names=[el.text for el in modules]
    check('current root modules exclude historical converter',len(module_names)==42 and all(not re.search(r'(?i)Json2Shiviz|services-analysis',m or '') for m in module_names),module_names)
    check('no declared converter build reference',not converter_refs,converter_refs)
    arc='old-docs/Lib/myproject.zip';outer=read(arc);archives=[];java_members=[];poms=[]
    with zipfile.ZipFile(io.BytesIO(outer)) as z:
        check('outer archive entries',len(z.infolist())==oracle['archive']['outer_entries'],len(z.infolist()))
        for ent in z.infolist():
            p=ent.filename
            if p.endswith('.pom'):
                raw=z.read(p);x=ET.fromstring(raw);poms.append({'locator':arc+'!/'+p,'sha256':sha(raw),'groupId':x.findtext('m:groupId','',ns),'artifactId':x.findtext('m:artifactId','',ns),'parent':{k:x.findtext('m:parent/m:'+k,'',ns) for k in ['groupId','artifactId','version']}})
            if not p.endswith('.jar'):continue
            raw=z.read(p)
            with zipfile.ZipFile(io.BytesIO(raw)) as nz:
                names=nz.namelist();classes=[n for n in names if n.endswith('.class')];safe_metadata=[]
                for n in ['META-INF/MANIFEST.MF','META-INF/spring.factories']:
                    if n in names:
                        mb=nz.read(n);safe_metadata.append({'member':n,'sha256':sha(mb),'literal':mb.decode('utf-8-sig')})
                if p.endswith('-sources.jar'):
                    for si in nz.infolist():
                        n=si.filename
                        if n.startswith('org/springframework/cloud/sleuth/') and n.endswith('.java') and not any(v in n.lower() for v in ['/sample/','/example/','/test/']):
                            sb=nz.read(n);st=sb.decode('utf-8-sig');pm=re.search(r'(?m)^package\s+([^;]+);',st)
                            java_members.append({'locator':arc+'!/'+p+'!/'+n,'bytes':len(sb),'sha256':sha(sb),'package':pm[1] if pm else None,'lines':len(st.splitlines())})
                archives.append({'locator':arc+'!/'+p,'sha256':sha(raw),'member_count':len(names),'class_count':len(classes),
                  'all_classes_sleuth_namespace':all(n.startswith('org/springframework/cloud/sleuth/') for n in classes),
                  'class_names':classes,'safe_metadata':safe_metadata,'javadoc_body_read':False,'bytecode_executed':False})
    check('nested archive count',len(archives)==oracle['archive']['nested_jars'],len(archives))
    check('safe embedded source coverage',len(java_members)==oracle['archive']['safe_java_source_members'],len(java_members))
    records.append({'path':arc,'old_status':'open','proposed_status':'read','read_depth':'all-safe-Java-source/POM + nested-container/class/activation-metadata; no bytecode execution or javadoc rendering',
      'classification':'historical-instrumentation-library-artifacts','source_evidence':[evidence('old-docs/Lib/ReadMe.md',1,9),evidence(root_readme,27,34)],
      'active_pom_scan':pom_rows,'active_build_inputs':build_rows,'active_direct_references':activation_refs,
      'embedded_poms':poms,'nested_archives':archives,'safe_java_source_members':java_members,
      'reason':'Library role and auto-configuration entry points are now explicit, not an unclassified binary. Historical instructions install these artifacts in Maven local storage. Current declared POMs have no direct activation/profile/systemPath for them; runtime/transitive activation is a separate unresolved input.',
      'inventory_relation_effect':'Keep historical instrumentation as a distinct conditional library source. Do not add application calls, Zipkin runtime entity, or RE2 operation aliases from its mere presence.',
      'remaining_uncertainty':{'question':'Does the evaluated deployment include these exact artifacts, external/transitive variants or the loose renamed monitoring library?',
        'needed_input':'Application image digest/build manifest and resolved dependencies/instrumentation agent configuration of the RE2-TT capture.',
        'owner':'RCAEval capture owner via Minh','affects':'Dataset-to-instrumentation lineage and runtime naming/propagation interpretation; not whether this saved archive has been classified.',
        'bytecode_to_source_identity_verified':False}})
    # PDF metadata and resource dictionaries only. No Contents.get_data(),
    # extract_text(), image data, rendering, sample log access or quarantined index.
    pdf='old-docs/Json2Shiviz/document/ReadMe.pdf';pb=read(pdf)
    code=r'''from pypdf import PdfReader
import pathlib,io,json,sys,hashlib
b=pathlib.Path(sys.argv[1]).read_bytes()
assert hashlib.sha256(b).hexdigest()==sys.argv[2]
r=PdfReader(io.BytesIO(b));out={'metadata':{str(k):str(v) for k,v in r.metadata.items()},'outlines':r.outline,'pages':[]}
for i,p in enumerate(r.pages,1):
 x=p.get('/Resources',{}).get('/XObject',{});x=x.get_object() if hasattr(x,'get_object') else x;images=[]
 for name,obj in x.items():
  q=obj.get_object()
  if q.get('/Subtype')=='/Image':images.append({'name':str(name),'width':q.get('/Width'),'height':q.get('/Height')})
 out['pages'].append({'page':i,'image_objects':images,'annotation_count':len(p.get('/Annots',[])),'content_stream_present':'/Contents' in p})
print(json.dumps(out,ensure_ascii=False))'''
    proc=subprocess.run([str(RUNTIME/'python/python.exe'),'-X','utf8','-B','-c',code,str(source/pdf),sha(pb)],capture_output=True,text=True,encoding='utf-8')
    assert proc.returncode==0,proc.stderr
    pm=json.loads(proc.stdout);check('PDF page metadata count',len(pm['pages'])==oracle['pdf']['pages'])
    check('PDF image metadata count',[len(x['image_objects']) for x in pm['pages']]==oracle['pdf']['image_objects_per_page'])
    check('PDF outline metadata count',len(pm['outlines'])==oracle['pdf']['outlines'])
    records.append({'path':pdf,'old_status':'open','proposed_status':'open','read_depth':'origin verification, document/page/resource metadata only; no page body, image stream or text read',
      'classification':'historical-log-conversion-manual-with-unclassified-page-bodies','pdf_metadata':pm,
      'source_evidence':[found('old-docs/Json2Shiviz/build.gradle',"mainClassName = 'org.services.analysis.TraceTranslator'"),evidence('old-docs/Json2Shiviz/document/regular_expr.txt',1,7),evidence('pom.xml',17,60)],
      'current_build_partition':{'root_module_names':module_names,'checked_pom_count':len(pom_rows),'checked_build_input_count':len(build_rows),'direct_converter_references':converter_refs,'current_inventory_status':'outside-declared-application-build'},
      'reason':'Adjacent source identifies a trace/log-conversion tool and its parsing schema. Six pages contain ten image objects and no outline; metadata does not distinguish instructions from actual sample log screenshots. Arbitrary page extraction/rendering could open the prohibited samples.',
      'inventory_relation_effect':'Historical offline trace/log-conversion documentation, outside the current root module inventory and without a direct reference in the checked current POM/build inputs. The unread body does not block that declared current-application inventory; old conversion schema, historical instrumentation names and RE2-TT lineage remain separate questions.',
      'remaining_uncertainty':{'needed_input':'Safe page/region list or sanitized manual from the source owner, explicitly identifying sample-free instruction pages; or explicit permission to inspect the relevant historical telemetry samples.',
        'owner':'Minh/source-document owner','affects':'Unread historical documentation content and any claim depending on its schema/naming/lineage; does not block the independently partitioned declared current module inventory.','tool_available':'Bundled pypdf, pdfinfo and pdftoppm are present; no missing-tool claim.',
        'permission_gap':'The user still prohibits actual Json2Shiviz sample logs/telemetry. A file being unclassified is not treated as a general ban; this concrete tool/manual context is the reason for page-body guard.',
        'estimated_minutes':10,'estimate_status':'CANDIDATE; after safe page list, no download/build needed'}})
    check('all old open entries exactly accounted',set(x['path'] for x in records)==set(x['path'] for x in old_open))
    check('no duplicate result rows',len(records)==len({x['path'] for x in records})==27)
    statuses=collections.Counter(x['proposed_status'] for x in records)
    merged=collections.Counter(coverage['statuses']);merged['open']-=27
    for key,count in statuses.items():merged[key]+=count
    check('merged blob partition',sum(merged.values())==coverage['blob_count']==2827)
    out={'task':'T-038','role':'implementation support; not official review','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'inputs':{'coverage':str(COVERAGE.relative_to(REPO)),'coverage_sha256':sha(COVERAGE.read_bytes()),'plan_sha256':sha(PLAN.read_bytes()),'oracle_sha256':sha((HERE/'oracle.json').read_bytes())},
      'records':sorted(records,key=lambda x:x['path']),'summary':{'old_open':27,'reclassified':dict(statuses),'recommended_merged_blob_statuses':dict(merged),'total_blobs':sum(merged.values()),
       'old_open_roles_partitioned':True,'content_scope_complete':False,'source_semantics_complete':False,'remaining_content_open_blocks_declared_current_inventory':False,'evaluated_runtime_lineage_complete':False,'safe_embedded_java_sources':len(java_members),'active_poms_checked':len(pom_rows),'elapsed_seconds':time.time()-start},
      'checks':checks,'all_checks_ok':all(x['ok'] for x in checks),'verified_inputs':sorted(verified.values(),key=lambda x:x['path']),
      'scientific_limits':['Classified saved snapshot content and declared build paths, not evaluated deployment or dataset instrumentation.','Image UI actions are not direct service dependencies.','Archive read_depth is explicit: bytecode/source equivalence and historical library activation are not verified.','One historical PDF remains OPEN for its concrete sample-log boundary; not for lack of a parser.'],
      'output_scope':str(HERE.relative_to(REPO)),'root_files_modified':False,'telemetry_samples_opened':False,'shared_code_modified':False,'downloads_or_build_execution':False,
      'external_readonly_lookup':'Official Helm release source pages viewed through browser/search only; no code/image body saved as a new source snapshot.'}
    (HERE/'findings.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out['summary'],ensure_ascii=False,indent=2));print('all_checks_ok',out['all_checks_ok']);print('findings_sha256',sha((HERE/'findings.json').read_bytes()))

if __name__=='__main__':main()
