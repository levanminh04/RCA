"""Source/provenance-only supplement. Never open measurement payloads or locked paths."""
from pathlib import Path
import csv,json,hashlib,re,html
from datetime import datetime,timezone
from collections import Counter

ROOT=Path('D:/RCA-flashticket')
OUT=ROOT/'results/T-020/trung-gian/dataset_evidence'
READ={}
CLAIMS=[]
def text(p):
    p=str(p).replace('\\','/')
    assert not p.startswith('data/') and 'locked' not in p.lower(),p
    assert p != 'results/T-010/runs/schema-samples.json','Known mixed schema/raw payload: do not replay'
    if p not in READ:READ[p]=(ROOT/p).read_text(encoding='utf-8-sig')
    return READ[p]
def js(p):return json.loads(text(p))
def rows(p):return list(csv.DictReader(text(p).splitlines()))
def write(n,x):
    (OUT/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def wc(n,x):
    with (OUT/n).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(x[0]));w.writeheader();w.writerows(x)
def source(p,needle='',claim=''):
    s=text(p); matches=[i for i,x in enumerate(s.splitlines(),1) if needle.lower() in x.lower()] if needle else [1]
    assert matches,(p,needle)
    loc=f'{p}:{matches[0]}'
    if needle:CLAIMS.append(dict(claim=claim or needle,path=p,needle=needle,line=matches[0],match=True,scope='Public source or saved original result only; not telemetry reread'))
    return loc
def authors(p):
    s=text(p)
    a=re.findall(r'<span class="ltx_personname">(.*?)</span>',s,re.S)
    return ', '.join(re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>','',x))).strip() for x in a)
def open_(s,owner='Minh/Tác giả',input_='campaign/revision/nguồn gốc công cụ đầy đủ'):
    return f'OPEN: {s}; owner={owner}; input={input_}'
def pub(s,p,k=''):return 'FACT công bố: '+s+'; '+source(p,k)
def measured(s,p,k=''):return 'FACT đo trên file kết quả gốc: '+s+'; '+source(p,k)

MATRIX=rows('results/T-020/trung-gian/dataset_evidence/01-bang-tieu-chi-hop-nhat.csv')
PROFILES=js('results/T-012/profiles.json')
# Exposure is governed by the unified identity ledger, not a local card's original stage.
ledger_path='results/T-020/trung-gian/exposure_ledger/dataset-membership-exposure.csv'
ledger={x['dataset']:x for x in rows(ledger_path)}
for d in MATRIX:
    name=d['dataset'];key=name
    if name.startswith('Nezha-'):key=name.split(' / ')[0]
    elif name.startswith('DeepTraLog'):key='DeepTraLog-TT'
    elif name=='FSE fault-propagation benchmark — artifact rút gọn':key='FSE-2026-propagation-TT'
    elif name=='AnoMod — SocialNetwork':key='AnoMod-SN_data'
    elif name=='AnoMod — TrainTicket':key='AnoMod-TT_data'
    elif name=='OpenRCA — Bank':key='OpenRCA-Bank'
    elif name.startswith('Check Your Trace First'):key='Nezha-TT' if 'TrainTicket' in name else 'Nezha-OB'
    if key in ledger:
        x=ledger[key];d['exposure']='; '.join(k+'='+x[k] for k in ['TX0','TX1','TX2'] if int(x[k]))
        if name=='RE1-OB':d['exposure']+='; local125TX2:40FSEmatch+85identityOPEN'
        if name.startswith('Check Your Trace First'):d['exposure']+='; inherited exact Nezha bytes'
        d['sources']+='; '+ledger_path+' #dataset='+key
AXES={}
RCA='results/T-002/public-metadata/run-002/sources/paper-v2.html'
NEZHA='results/T-020/trung-gian/dataset_evidence/nezha-paper-text.json'
EADRO='results/T-009/sources/paper.html'
LEMMA='results/T-011/runs/run-001/sources/paper-v4.html'
FSE='results/T-012/runs/run-001/sources/fse-paper-v2.html'
ORCA='results/T-012/runs/run-002/sources/openrca-paper.txt'
ORCA2='results/T-012/runs/run-001/sources/openrca2-paper-v2.html'
ANOSN='results/T-012/runs/run-002/sources/anomod-SN_collection-scripts__README.md'
ANOTT='results/T-012/runs/run-002/sources/anomod-TT_collection-scripts__chaos-experiments__README.md'
ANOTTTR='results/T-012/runs/anomod-collector-review-001/TT_collection-scripts__T-Dataset__enhanced_trace_collector.py'
LO='results/T-012/runs/run-001/sources/lo2-paper-v1.html'
TTT='results/T-012/runs/run-002/sources/zenodo-17811972-latest.json'

AXES['RCAEval']=(pub(authors(RCA),RCA,'Luan Pham'),pub('stress-ng cho resource, tc cho mạng; lỗi code theo nhánh sửa',RCA,'stress-ng')+'; '+source(RCA,'traffic control (tc)'),pub('Prometheus/cAdvisor/Istio; Vector/Loki/Elasticsearch; Jaeger',RCA,'Datadog Vector'),'RE1/RE2/RE3 và TT/OB/SS chung họ; có thành phần collector trùng các họ khác')
n=js(NEZHA);p8=next(x for x in n['pages'] if x['page']==8)['text'];assert all(x in p8 for x in ['[4, 28, 52]','Grafana Tempo','Prometheus Node Exporter'])
AXES['Nezha']=(pub('Guangba Yu, Pengfei Chen, Yufeng Li, Hongyang Chen, Xiaoyun Li, Zibin Zheng; paper p1',NEZHA,'Guangba Yu'),pub('Java Byteman/Python Hypno/Go Failpoint: p8 refs4/28/52 và p12–13 references',NEZHA,'language-specific')+'; '+open_('CPU/network injector cụ thể chưa khóa'),pub('OpenTelemetry Collector→Tempo; Promtail→Loki; cAdvisor/Istio/NodeExporter→Prometheus; p8',NEZHA,'Grafana Tempo'),'OB/TT và trace/log/metric cùng pipeline; không suy raw independence với RCAEval')
AXES['Eadro']=(pub(authors(EADRO),EADRO,'Cheryl'),pub('Chaosblade',EADRO,'via Chaosblade'),pub('Jaeger; cAdvisor/Prometheus→InfluxDB; Fluentd/Elasticsearch/Kibana',EADRO,'InfluxDB'),'SN/TT chung nhóm/pipeline; Jaeger/Prometheus/Elasticsearch chồng thành phần RCAEval')
web=[dict(url='https://cspengxin.github.io/publications/icse22-DeepTraLog.pdf',location='p1; §4.1.1 p7–8',kind='FACT công bố',authors='Chenxi Zhang, Xin Peng, Chaofeng Sha, Ke Zhang, Zhenqing Fu, Xiya Wu, Qingwei Lin, Dongmei Zhang',injector='Faulty TrainTicket branches; automated Python test controller',collector='Apache SkyWalking; Elasticsearch',retrieval='Narrow official-author PDF browse; no dataset payload',limit='Published 73 faults/14 fault cases does not replace saved release graph70-label census'),dict(url='https://arxiv.org/html/2406.05375v4',location='§3.1 and Appendix B/F',kind='FACT công bố',authors='Lecheng Zheng, Zhengzhang Chen, Dongjie Wang, Chengyuan Deng, Reon Matsuoka, Haifeng Chen',injector='Scenario-specific generation; tool varies with scenario',collector='PR: OpenShift Prometheus/Elasticsearch, JMeter KPI; Cloud: CloudWatch, some Prometheus/JMeter',retrieval='Narrow official arXiv v4 browse; no dataset payload',limit='License exact applicability remains OPEN; do not infer all scenarios share injector')]
write('public-source-verification.json',web)
dw='https://cspengxin.github.io/publications/icse22-DeepTraLog.pdf #p1/§4.1.1 p7–8'
AXES['DeepTraLog']=('FACT công bố: '+web[0]['authors']+'; '+dw,'FACT công bố: faulty TrainTicket branches + Python test controller; '+dw+'; '+open_('exact faulty branch revision per release/capture chưa bind'), 'FACT công bố: SkyWalking/Elasticsearch; '+dw,'raw trace/log và event graph chung raw; TT fault branch reuse với họ khác chưa đối chiếu exact revision')
AXES['LEMMA IT']=(pub(authors(LEMMA),LEMMA,'Lecheng Zheng'),'FACT công bố: scenario-specific; OpenSSL/config/traffic là các cách được paper v4 Appendix B mô tả; https://arxiv.org/html/2406.05375v4 #Appendix B; '+open_('mapping exact injector tới từng archive/day chưa khóa'), 'FACT công bố: PR OpenShift Prometheus/Elasticsearch, JMeter KPI; Cloud CloudWatch và một số Prometheus/JMeter; https://arxiv.org/html/2406.05375v4 #§3.1/Appendix B','Original/Preprocessed cùng raw; PR/Cloud khác miền không tự đủ độc lập injector')
AXES['FSE']=(pub(authors(FSE),FSE,'Aoyang Fang'),pub('ChaosMesh structured fault injection',FSE,'We used ChaosMesh'),pub('OpenTelemetry; pipeline gồm metrics/log/traces/network; Hubble',FSE,'standard observability stack'),'FSE reduced artifact và OpenRCA2 TT upstream chung; không count hai corpus')
AXES['OpenRCA']=(pub('Junjielong Xu, Qinan Zhang, Zhiqing Zhong, Shilin He, Chaoyun Zhang, Qingwei Lin, Dan Pei, Pinjia He, Dongmei Zhang, Qi Zhang',ORCA,'Junjielong Xu')+'; '+open_('original AIOps data providers/authors từng edition chưa định danh đủ'),open_('injector AIOps gốc từng Bank/Telecom/Market chưa có','Tác giả','edition/system + source campaign'),open_('collector AIOps gốc từng hệ chưa có','Tác giả','edition/system + collector source'),pub('AIOps Challenge raw reuse; biến đổi không làm corpus độc lập với upstream',ORCA,'originating from'))
AXES['OpenRCA2']=(pub(authors(ORCA2),ORCA2,'Aoyang Fang'),open_('exact injector per release/system chưa được independently verified; hồ sơ ghi ChaosMesh','Tác giả/P3','public release injection config'),pub('OpenTelemetry multi-modal pipeline; exact per-system collector config OPEN',ORCA2,'OpenTelemetry'),'TrainTicket dùng Fang/FSE upstream; ba hệ cùng nhóm/pipeline; tác giả Xu/He overlap OpenRCA1, không suy raw reuse OpenRCA1')
ano_record='results/T-012/runs/run-002/sources/zenodo-18342898-latest.json'
an=js(ano_record)['metadata']; anauthors=', '.join(x['name'] for x in an['creators'])
AXES['AnoModSN']=(pub(anauthors,ano_record,'creators'),pub('ChaosBlade + targeted container restart; Code_Stop docker stop theo code audit',ANOSN,'Anomaly injection'),pub('Prometheus + Jaeger + container logs',ANOSN,'capture logs, Prometheus metrics'),'campaign mới theo nguồn; dùng thành phần Jaeger/Prometheus/ChaosBlade như Eadro; có tác giả trùng LO2')
AXES['AnoModTT']=(pub(anauthors,ano_record,'creators'),pub('Chaos Mesh YAML; code-level ChaosBlade trong run_experiment.sh',ANOTT,'Code-level anomalies'),pub('SkyWalking enhanced trace collector; Prometheus/container logs theo toolkit',ANOTTTR,'skywalking'),'SkyWalking trùng DeepTraLog; tool overlap FSE/Eadro; có tác giả trùng LO2; campaign labels chưa runtime ground truth')
ttt=js(TTT)['metadata']
AXES['TrainTicketTrace']=(pub(', '.join(x['name'] for x in ttt['creators']),TTT,'creators'),open_('faulty version archives chưa exact injector/branch binding','Tác giả/P3','version/revision + injection campaign'),open_('collector chưa khóa từ metadata','Tác giả/P3','collector specification'), 'F-code/testbed giống DeepTraLog chưa chứng minh raw reuse hoặc độc lập')
AXES['TRCA']=(pub('anonymous deposit; không có identity tác giả thật trong record','results/T-012/runs/run-002/sources/zenodo-19335897-latest.json','creators'), 'FACT đo trên file kết quả gốc: raw reused Nezha; kế thừa injector Nezha trong phạm vi byte-match; '+source('results/T-012/runs/trca-reuse-001/result.json','exact_nezha_matches'), 'FACT đo trên file kết quả gốc: raw reused Nezha; kế thừa collector Nezha trong phạm vi byte-match; '+source('results/T-012/runs/trca-reuse-001/result.json','exact_nezha_matches'),'1165 CSV+4 labels byte-identical Nezha, không independent corpus')
AXES['LO2']=(pub(authors(LO),LO,'Bakhtin'),pub('Locust correct/error API usage, không service-root injection gold',LO,'Locust'),pub('Jaeger/Prometheus + NodeExporter; v2 cAdvisor chỉ record claim chưa file-schema',LO,'Jaeger'),'v1/v2 một lineage; có tác giả Wang/Ping/Mäntylä overlap AnoMod; API class không service-root gold')

def family(name):
    if name=='BARO-FSE-OB':return 'BARO-FSE'
    if name.startswith('RE'):return 'RCAEval'
    if name.startswith('Nezha'):return 'Nezha'
    if name.startswith('Eadro'):return 'Eadro'
    if name.startswith('Deep'):return 'DeepTraLog'
    if name.startswith('LEMMA'):return 'LEMMA IT'
    if name.startswith('FSE'):return 'FSE'
    if name.startswith('AnoMod'):return 'AnoModSN' if 'Social' in name else 'AnoModTT'
    if name.startswith('TrainTicketTrace'):return 'TrainTicketTrace'
    if name.startswith('Check Your Trace'):return 'TRCA'
    if name.startswith('OpenRCA 2'):return 'OpenRCA2'
    if name.startswith('OpenRCA'):return 'OpenRCA'
    if name.startswith('LO2'):return 'LO2'
    raise AssertionError(name)
AXES['BARO-FSE']=(pub('Pham/BARO author family; historical reproduction source','results/T-006/moi-truong.md'),open_('exact historical injector chưa khóa','Tác giả','BARO campaign paper/source'),open_('exact historical collector chưa khóa','Tác giả','BARO campaign paper/source'),'100 local recordings TX2; same author family RCAEval; exact raw lineage dùng saved hash, không ghép bằng basename')
axisrows=[]
for d in MATRIX:
    a,i,c,r=AXES[family(d['dataset'])]
    axisrows.append(dict(dataset=d['dataset'],family=family(d['dataset']),authors=a,injector=i,collector=c,reuse=r,c9_state=open_('chưa có bằng chứng đủ cả ba trục cho cặp độc lập; không cộng điểm',input_='pairwise source/campaign/revision comparison')))
    d['C9']='; '.join([a,i,c,r,axisrows[-1]['c9_state']])
wc('independence-axes.csv',axisrows)

# License/revision: metadata source statements only, not legal interpretation.
license_rows=[]
rcahf='results/T-002/public-metadata/run-002/sources/hf-README.md'
lemmanifest=js('results/T-011/runs/run-001/manifest.json')
for d in MATRIX:
    f=family(d['dataset']);p=None
    if f=='BARO-FSE':
        license_=open_('historical Zenodo11046533 data/code exact license chưa independently khóa','Minh/Tác giả','record/archive license');revision=pub('Zenodo11046533; archive MD5 API taskcũ', 'results/T-006/moi-truong.md','11046533');missing=open_('original campaign revision/injector/collector','Tác giả/P3','BARO paper/release source')
    elif f=='RCAEval':
        license_=pub('data MIT theo HF frontmatter',rcahf,'license: mit');revision=measured('Git commit/HF metadata revisions ghim trong manifest; không lấy code SHA làm data SHA','results/T-002/public-metadata/run-002/source-manifest.json');missing=open_('upstream license scope đối với assets không tự đồng nhất code/data','Minh/Tác giả','license exact data release trước công bố')
    elif f=='Nezha':
        license_=pub('repo MIT; data scope không tự rộng hơn source statement','results/T-008/sources/LICENSE','MIT License');revision=pub('d8140101fdb4e7dfb60d3ef9f64706f382b68470','results/T-008/runs/run-001/manifest.json','revision');missing=open_('derived redistributable assets scope trước công bố','Minh/Tác giả','license data exact scope')
    elif f=='Eadro':
        license_=open_('data/code license exact statement chưa khóa','Minh/Tác giả','repo/archive data license');revision=measured('repo source pinned + ZIP hashes trong manifests','results/T-009/runs/run-001/manifest.json');missing=open_('quyền sử dụng/công bố trước P3','Minh/Tác giả','data license statement')
    elif f=='DeepTraLog':
        license_=open_('không có data permission đủ trong source đã kiểm; paper copyright không là data license','Minh/Tác giả','data license');revision=pub(js('results/T-010/runs/run-001/manifest.json')['revision'],'results/T-010/runs/run-001/manifest.json','revision');missing=open_('faulty branches/capture/data revision mapping','Tác giả/P3','release manifest and permission')
    elif f=='LEMMA IT':
        k=('Product_Review' if 'PR' in d['dataset'] else 'Cloud_Computing')+('_Original' if '/ Original' in d['dataset'] else '_Preprocessed')
        rp='results/T-011/runs/source-final-001/sources/'+k+'__README.md'
        license_=pub('frontmatter cc-by-nc-4.0',rp,'license: cc-by-nc-4.0')+'; '+pub('body cc-by-nd-4.0',rp,'cc-by-nd-4.0');revision=pub(lemmanifest['dataset_revisions'][k],'results/T-011/runs/run-001/manifest.json',k);missing=open_('license conflict/applicability vẫn mở; WHY14 chỉ cho inspection nội bộ phạm vi hẹp','Minh/Tác giả','written exact data terms before publication')
    else:
        name=d['dataset'].replace(' / trace+log','').replace(' / metric ngày','')
        p=next(x for x in PROFILES if x['name']==name)
        license_=pub(p['license'],'results/T-012/profiles.json','"license"')+'; trích profile, kiểm nguồn metadata bên dưới'
        revision=pub(p['version'],'results/T-012/profiles.json','"version"')+'; không dùng latest như revision bất biến'
        missing=open_('data release/permission exact trước sử dụng hoặc công bố','Minh/Tác giả','immutable source/revision and applicable license')
        if f=='OpenRCA':
            license_=pub('telemetry CC BY-NC4.0 theo paper A.1',ORCA,'Data under CC BY-NC 4.0')+'; '+pub('code MIT','results/T-012/runs/run-002/sources/openrca-LICENSE','MIT License');revision=pub(js('results/T-012/runs/run-002/sources/openrca-commit.json')['sha'],'results/T-012/runs/run-002/sources/openrca-commit.json','sha')+'; '+open_('Drive full archive mutable; không whole-data hash')
        if f=='TrainTicketTrace':
            license_=pub(ttt['license']['id'],TTT,'license');revision=pub(ttt['doi'],TTT,'doi')
        if f.startswith('AnoMod'):
            license_=pub(an['license']['id'],ano_record,'license')+'; '+pub('code MIT','results/T-012/runs/run-002/sources/anomod-LICENSE','MIT License');revision=pub(an['doi'],ano_record,'doi')+'; '+pub(js('results/T-012/runs/run-002/sources/anomod-commit.json')['sha'],'results/T-012/runs/run-002/sources/anomod-commit.json','sha')
        if f=='FSE':
            rp='results/T-012/runs/review-sources-001/sources/zenodo-19522409.json';z=js(rp);license_=pub(str(z['metadata']['license']),rp,'license')+'; '+pub('internal LICENSE packaging scope/upstream retained terms','results/T-012/runs/fse-file-inspect-003/LICENSE.txt');revision=pub(z['metadata']['doi'],rp,'doi')+'; '+measured('archive hash saved','results/T-012/runs/fse-file-inspect-003/archive.json')
        if f=='TRCA':
            rp='results/T-012/runs/run-002/sources/zenodo-19335897-latest.json';z=js(rp);license_=pub(str(z['metadata']['license']),rp,'license')+'; '+open_('Nezha reused byte inputs scope chưa giải');revision=pub(z['metadata']['doi'],rp,'doi')
        if f=='LO2':
            rp='results/T-012/runs/run-002/sources/zenodo-'+('18937117' if 'v2' in d['dataset'] else '14938118')+'-latest.json';z=js(rp);license_=pub(str(z['metadata']['license']),rp,'license');revision=pub(z['metadata']['doi'],rp,'doi')
        if f=='OpenRCA2':
            license_=pub('data CC-BY-SA4.0; pipeline Apache2.0 theo A.6',ORCA2,'CC-BY-SA');revision=open_('public full release chưa khóa; paper v2 không data revision','Tác giả/P3','public immutable data release')
    license_rows.append(dict(dataset=d['dataset'],license=license_,revision=revision,open_reason=missing))
wc('license-revision.csv',license_rows)

# Existing actual schema witnesses versus source-only claims: zero new payload reads.
schema_rows=[]
for d in MATRIX:
    name=d['dataset'];f=family(name);schema='';extent='';unsafe=''
    if f=='BARO-FSE':
        schema=open_('saved manifest có metric/inject hash; chưa exact column schema witness trong luồng này','P3','saved schema hoặc V7 exact header plan');extent='100local recordings/20cells TX2; chỉ historical reproduction';unsafe='không giải nén raw để lấp schema; không giả historical run là test mới'
    elif f=='RCAEval':
        if name=='RE3-OB':schema=open_('schema thật chưa có saved witness','P3/P7','schema được phép sau G1/G3');extent='TX0 theo ledger; chỉ file/directory census';unsafe='Binary Parquet không phải dòng header text; không mở first-line binary để suy schema'
        elif name=='RE1-TT':schema=open_('actual metric schema chưa có witness, trace/log absence đã census filename','P3/P7','V7 plan exact schema mechanism phù hợp binary, không telemetry');extent='125public directories/25cells/metrics125/traces0/logs0; TX0';unsafe='Binary Parquet không first-line text; không suy schema từ RE2TT'
        elif name=='RE1-OB':schema=measured('1public metric sample schema saved','results/T-002/local-inspection/run-002/schemas.json');extent='public125 có1TX1; local125TX2=40FSEmatch+85identityOPEN';unsafe='không suy public↔local identity hay safe test từ basename/shape'
        elif name.endswith('SS'):schema=measured('metric CSV schema; không trace; RE2 có logs','results/T-019/inspection/schemas.json');extent='T019 full245 aggregate; TX2/TX1 theo ledger';unsafe='schema không chứng minh normal/propagation; RE3SS30 đã TX1'
        else:schema=measured('schema keys exact saved','results/T-002/local-inspection/run-002/schemas.json');extent='RE2TT30; RE2OB1; RE3TT1 inspected. Không áp sample toàn release';unsafe='TX1/TX2 từ đọc số đo/chạy taskcũ ngoài schema; chỉ schema không tự nâng TX0. Luồng này không đọc số đo mới'
    elif f=='Nezha':schema=measured('actual CSV schema saved per member','results/T-008/runs/file-audit-001/summary.json');extent='trace/log conditional3-minute captures; daily metric separate';unsafe='daily metric coverage không cứu continuous trace/log benchmark'
    elif f=='Eadro':schema=measured('actual CSV schema saved per raw session','results/T-009/runs/inspect-004/raw-sessions.json');extent='distinct sessions7SN/12TT, not every mirror independent';unsafe='identity-unscoped spans không tự parent unique'
    elif f=='DeepTraLog':schema=measured('raw aggregate tables + graph event types saved, không đọc schema sample chứa raw row','results/T-010/runs/inspect-002/raw-cases.json');extent='raw+graph TX1, scope different';unsafe='event graph không replace service call graph; bool class không root/onset; saved header-only witness chưa tách payload trong luồng này'
    elif f=='LEMMA IT':
        sample='/ Preprocessed sample' in name
        schema=measured('sample CSV/NPY metadata saved','results/T-011/runs/inspect-008/summaries.json') if sample else open_('Original/ngày ngoài sample chưa actual schema witness','P3/P7','schema được phép sau G1/G3')
        extent='sample PR20211203/Cloud20240124 TX1; other dates and Original TX0';unsafe='NPY/binary không first-line text; không suy full-release schema từ ngày mẫu'
    elif f=='FSE':schema=measured('actual Parquet schemas saved','results/T-012/runs/fse-file-inspect-003/schemas.json');extent='reduced artifact10folders/8withoutinvalid TX1';unsafe='không suy schema quality toàn benchmark1430'
    elif f.startswith('AnoMod'):schema=measured('actual CSV/JSON schemas saved','results/T-012/runs/anomod-file-inspect-003/files.json');extent='13captures/hệ TX1';unsafe='capture timestamp không runtime injection gold'
    elif f=='TRCA':schema=measured('schema inherit within exact byte match Nezha','results/T-012/runs/trca-reuse-001/result.json');extent='1165CSV+4labels exactmatch; inherited exposure TX1';unsafe='same raw và same schema không independent corpus'
    else:
        schema=open_('chỉ source/paper/metadata schema claim, chưa actual header schema','P3/P7','V7 đã cho phép first-line một file tín hiệu nếu exact newline/no inflation bảo đảm; cần mechanism phù hợp artifact')
        extent='TX0 telemetry; Bank public136labels + ZIP central directory only; no data payload' if name=='OpenRCA — Bank' else 'source-only TX0; runtime payload/schema chưa có witness'
        unsafe='Bank remoteZIP không local: chưa có mechanism bảo đảm exact newline/no inflate (V7 cần exact byte/range plan); đây là thiếu mechanism/artifact, không thiếu quyền' if name=='OpenRCA — Bank' else 'V7 firstline text đã cho phép theo exact newline/no inflation; artifact chưa có mechanism đủ trong luồng này, paper không actual schema'
    schema_rows.append(dict(dataset=name,exposure=d['exposure'],schema_witness=schema,scope=extent,V7_limit=unsafe,c7_state=open_('TX0/held-out tiêu chí7 chưa được đo; không coi OPEN là thất bại hoặc đạt','P7 sau G3','sanctioned original telemetry/control/load') if 'TX0' in d['exposure'] else open_('TX1 không hoàn toàn ngoài thiết kế; C7 probe descriptive không causal','P3/P4','independent controls and labels')))
wc('schema-provenance.csv',schema_rows)
md='# Schema, nguồn gốc và phạm vi giữ ngoài — bằng chứng T-020\n\nKhông có lựa chọn dataset ở đây. TX0 là lịch sử chưa xem telemetry theo ledger, không phải bằng chứng đủ C1–C9. TX1 đã được khảo sát nên không tự mô tả hoàn toàn ngoài thiết kế. Bank Q49 là yêu cầu census, không phải Minh chọn Bank. C7 bộ giữ ngoài là OPEN, được kiểm sau G3 trong phạm vi cho phép.\n\n| Dataset/phần | Schema chứng kiến | Phạm vi | Giới hạn V7 | C7 |\n|---|---|---|---|---|\n'
for x in schema_rows:md+='| '+' | '.join(x[k].replace('|',' / ').replace('\n',' ') for k in ['dataset','schema_witness','scope','V7_limit','c7_state'])+' |\n'
md+='\nC9 ba trục riêng tại independence-axes.csv; mỗi trục có nguồn hoặc OPEN với owner/input. Không có cặp được tự chứng nhận đủ độc lập. License/revision.csv giữ riêng code/data/paper và phạm vi applicability còn OPEN. Bank ZIP directory/record hash ghim metadata và labels; không có whole-data hash hay immutable full revision.\n\nNguồn exposure: results/T-020/trung-gian/exposure_ledger/dataset-exposure.csv và dataset-membership-exposure.csv. Hai phần của LEMMA cùng raw phải truyền exposure khi identity chứng minh; chưa có proof thì OPEN. RE3OB30ca/4roots/5faults/10cells đã tính lại từ census; chat sớm ghi5roots là nhầm với fault-count, không phải lỗi thẻ cũ.\n'
(OUT/'heldout-schema-provenance.md').write_text(md,encoding='utf-8')

# Link current C9 to explicit axes. Preserve all other cells and original definitions.
wc('01-bang-tieu-chi-hop-nhat.csv',MATRIX)
md=text('results/T-020/trung-gian/dataset_evidence/01-bang-tieu-chi-hop-nhat.md').split('| Dataset/release/phần')[0]
md+='| Dataset/release/phần | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | Chi phí |\n|---|---|---|---|---|---|---|---|---|---|---|\n'
for d in MATRIX:md+='| '+' | '.join(d[k].replace('|',' / ').replace('\n',' ') for k in ['dataset',*[f'C{i}' for i in range(1,10)],'cost'])+' |\n'
(OUT/'01-bang-tieu-chi-hop-nhat.md').write_text(md,encoding='utf-8')
s=js('results/T-020/trung-gian/dataset_evidence/supporting.json');s['rows']=MATRIX;s['independence_axes']=axisrows;write('supporting.json',s)
runner='results/T-020/trung-gian/method_evidence/runner-leakage.csv';rr=rows(runner)
wc('runner-leakage-method-worker.csv',rr)
tm=text('results/T-020/trung-gian/dataset_evidence/03-task-cham-duoc-va-che-do-b.md').split('\n## Runner leakage bổ sung')[0]
tm+='\n## Runner leakage bổ sung\n\nTrích audit của methods worker; root kiểm đường quan trọng từ source runner trước ký V4. Không là kết quả chạy mode b trên dataset mới.\n\n| Phương pháp | Đường rò | FACT cơ chế | Trạng thái | Nguồn |\n|---|---|---|---|---|\n'
for x in rr:tm+='| '+' | '.join(str(x[k]).replace('|',' / ') for k in ['method','path','factual_audit','status','source'])+' |\n'
(OUT/'03-task-cham-duoc-va-che-do-b.md').write_text(tm,encoding='utf-8')
wc('public-source-claims-checked.csv',CLAIMS)
write('provenance-input-hashes.json',[dict(path=p,bytes=(ROOT/p).stat().st_size,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in sorted(READ)])
write('T004-no-scientific-pool.json',dict(task='T-004',status='OPEN / chưa triển khai',source='tasks/T-020-tong-hop-g1/SPEC.md:13',scientific_numeric_pool=0,seeded_checks='Không tạo 5 số giả; chưa có task/results T004 scientific source',reason='V1 input mentions reserved P9a, not a completed measurement task'))
write('provenance-run.json',dict(utc=datetime.now(timezone.utc).isoformat(),datasets=len(MATRIX),independence_axes=len(axisrows),schema_rows=len(schema_rows),license_rows=len(license_rows),source_claims_checked=len(CLAIMS),runners=len(rr),new_raw_files_read=False,saved_schema_sample_incident='scope-incident.json; saved header sample unexpectedly contains raw rows, not used for recompute/choice',locked_read=False,recommendation=False))
print(json.dumps(dict(datasets=len(MATRIX),axes=len(axisrows),schema=len(schema_rows),license=len(license_rows),source_claims=len(CLAIMS)),ensure_ascii=False))
