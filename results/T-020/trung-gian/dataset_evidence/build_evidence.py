from pathlib import Path
import csv, json, hashlib, re, statistics
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta

ROOT = Path('D:/RCA-flashticket')
OUT = ROOT / 'results/T-020/trung-gian/dataset_evidence'
SEED = '20261004'
USED = set()
TEXT_CACHE = {}
CHECKS = []

def txt(p):
    p = str(p).replace('\\', '/')
    assert not p.startswith('data/') and 'locked' not in p.lower(), p
    assert p != 'results/T-010/runs/schema-samples.json', 'Known mixed schema/raw payload: do not replay'
    USED.add(p)
    if p not in TEXT_CACHE:
        TEXT_CACHE[p] = (ROOT / p).read_text(encoding='utf-8-sig')
    return TEXT_CACHE[p]

def js(p): return json.loads(txt(p))
def rows(p): return list(csv.DictReader(txt(p).splitlines()))
def write_json(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def write_csv(name, data, fields=None):
    with (OUT / name).open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields or list(data[0]))
        w.writeheader(); w.writerows(data)
def line(p, needle):
    return next((i for i,s in enumerate(txt(p).splitlines(),1) if needle in s),1)
def src(p,k=''):
    if str(p).endswith('.pdf'):
        assert (ROOT / p).is_file(), p
        USED.add(p)  # Public paper, not a measurement payload; page-level inspection is separate.
    else:
        txt(p)  # A cited local source must exist and be registered, including citations without a key.
    n = line(p, '"' + k.split('.')[-1] + '"') if k and str(p).endswith('.json') else 1
    return f'{p}:{n}' + (f' #{k}' if k else '')
def ck(task,p,k,v,new,calc,meaning=None):
    match = v == new or (isinstance(v,(int,float)) and isinstance(new,(int,float)) and abs(v-new) <= 1e-9 * max(1,abs(v)))
    CHECKS.append(dict(task=task, path=p, key=k, meaning=meaning or re.sub(r'\[\d+\]', '[]', k), original=v, recomputed=new, match=str(match), recompute=calc, reason='Tính lại từ thành phần kết quả gốc; không đọc telemetry', source=src(p,k), sample_sha256=hashlib.sha256(f'{SEED}|{task}|{p}|{k}'.encode()).hexdigest(), seeded_sample=False))
    return new
def fact(msg,p,k=''): return 'FACT đo trên file: ' + msg + '; ' + src(p,k)
def pub(msg,p,k=''): return 'FACT từ nguồn công bố: ' + msg + '; ' + src(p,k)
def op(msg,owner='Người làm P3',inp='nhãn/adapter nguồn phù hợp',gate='P3'): return f'OPEN: {msg}; owner={owner}; input={inp}; giải tại {gate}'

DATASETS = []
TASKS = []
MAPPING = []
LEAKS = []
CENSUS = []
def add(name,family,scope,c, cost, unit, time, ranking, a,b,trace,region=None,exposure='TX1',mapping='',sources=''):
    assert len(c)==9
    DATASETS.append(dict(dataset=name,family=family,scope=scope,exposure=exposure,**{f'C{i+1}':x for i,x in enumerate(c)},cost=cost,sources=sources))
    TASKS.append(dict(dataset=name,unit=unit,time_label=time,ranking=ranking,mode_a=a,mode_b=b,region=region or op('không có nhãn vùng độc lập','Tác giả/Minh','nhãn tập thành phần bị ảnh hưởng','P7/P10'),trace_anomaly=trace,supervised_transfer=op('ngân sách nhãn học/tune/chấm và chuyển hệ chưa chốt','Minh','phương pháp và nhãn dev/test phù hợp','G1'),mapping=mapping))

# RCAEval census: both counts and all nontrivial ratios reconstructed.
pmeta='results/T-002/public-metadata/run-002/count-summary.json'
meta=js(pmeta); casespub=rows('results/T-002/public-metadata/run-002/cases-from-directories.csv')
modsizes=rows('results/T-002/public-metadata/run-002/modality-sizes.csv')
plocal='results/T-002/local-inspection/run-002/summary.json'
local=js(plocal); localcases=js('results/T-002/local-inspection/run-002/cases.json')
schemas=js('results/T-002/local-inspection/run-002/schemas.json')
for idx,m in enumerate(meta):
    suite=m['dataset'].lower().replace('-',''); cc=[x for x in casespub if x['suite']==suite]
    ck('T-002',pmeta,f'[{idx}].n_cases',m['n_cases'],len(cc),'count cases-from-directories.csv suite')
    ck('T-002',pmeta,f'[{idx}].n_root_services',m['n_root_services'],len({x['root_service'] for x in cc}),'nunique root_service')
    ck('T-002',pmeta,f'[{idx}].n_faults',m['n_faults'],len({x['fault'] for x in cc}),'nunique fault')
    cells=Counter((x['root_service'],x['fault']) for x in cc)
    ck('T-002',pmeta,f'[{idx}].n_observed_root_fault_cells',m['n_observed_root_fault_cells'],len(cells),'nunique root × fault')
    ck('T-002',pmeta,f'[{idx}].cell_repetition_min',m['cell_repetition_min'],min(cells.values()),'min cell count')
    ck('T-002',pmeta,f'[{idx}].cell_repetition_max',m['cell_repetition_max'],max(cells.values()),'max cell count')
    ck('T-002',pmeta,f'[{idx}].total_file_bytes',m['total_file_bytes'],sum(int(x['bytes']) for x in modsizes if x['dataset']==m['dataset']),'sum modality-sizes.csv bytes')
    ck('T-002',pmeta,f'[{idx}].files',m['files'],sum(int(x['n_files']) for x in modsizes if x['dataset']==m['dataset']),'sum modality-sizes.csv n_files')
    for root,count in m['root_services_and_case_counts'].items(): ck('T-002',pmeta,f'[{idx}].root_services_and_case_counts.{root}',count,sum(x['root_service']==root for x in cc),'group root count')
    for fault,count in m['faults_and_case_counts'].items(): ck('T-002',pmeta,f'[{idx}].faults_and_case_counts.{fault}',count,sum(x['fault']==fault for x in cc),'group fault count')
    ll=[x for x in localcases if x['dataset']==suite]; s=local[suite]
    ck('T-002',plocal,f'{suite}.n_inspected',s['n_inspected'],len(ll),'count local cases')
    for field,cf in [('n_spans','n_spans'),('parent_reference_count','parent_reference_count'),('parent_resolved_count','parent_resolved_count'),('parent_unresolved_count','parent_unresolved_count'),('status_nonnull','status_nonnull')]:
        ck('T-002',plocal,f'{suite}.{field}',s[field],sum(x.get('trace',{}).get(cf,0) for x in ll),'sum per-case trace.'+cf)
    if ll:
        for field in ['normal_rows_min','normal_rows_max','post_rows_min','post_rows_max']:
            f=field.rsplit('_',1)[0]; agg=min if field.endswith('min') else max
            ck('T-002',plocal,f'{suite}.{field}',s[field],agg(x[f] for x in ll),'range per-case '+f)
        ck('T-002',plocal,f'{suite}.parent_resolution_fraction',s['parent_resolution_fraction'],s['parent_resolved_count']/s['parent_reference_count'],'sum resolved / sum reference')
    if ll:
        parent=fact(f"trace {len(ll)} ca; resolved {s['parent_resolved_count']}/{s['parent_reference_count']}={s['parent_resolution_fraction']:.6%}",plocal,f'{suite}.parent_resolution_fraction')
        modality=fact(f"metric {len(ll)} ca; log {s['n_log_cases']}/{len(ll)}; direct trace/span-ID columns {s['direct_trace_id_columns']}",plocal,suite)
        normal=fact(f"trước tiêm {s['normal_rows_min']}–{s['normal_rows_max']} points, cadence {s['metric_steps']} s",plocal,suite)+'; '+op('đủ calibration/healthy/load đại diện chưa chứng minh',inp='normal sạch phù hợp phương pháp')
    else:
        parent=op('trace có file metadata nhưng schema/parent release chưa kiểm','Người làm P3','schema/parent kiểm sau chọn G1')
        modality=fact(f"file metrics={m['file_counts'].get('metrics.parquet',0)}, logs={m['file_counts'].get('logs.parquet',0)}, traces={m['file_counts'].get('traces.parquet',0)}",pmeta,f'[{idx}].file_counts')+'; '+op('chất lượng thực chưa kiểm')
        normal=op('không có thống kê normal của release','Người làm P3','normal schema/timeline được phép sau G1')
    for x in ll:
        assert x['metric_time_min'] < x['inject_time'] < x['metric_time_max']
        mid=(x['metric_time_min']+x['metric_time_max'])/2-x['inject_time']
        ck('T-002','results/T-002/local-inspection/run-002/cases.json',x['case']+'.midpoint_offset',0,mid,'(metric_min + metric_max)/2 - inject_time','boundary midpoint offset')
        LEAKS.append(dict(dataset=m['dataset'],kind='file boundary',evidence=src('results/T-002/local-inspection/run-002/cases.json',x['case']),value=f"{x['metric_time_min']-x['inject_time']} / {x['metric_time_max']-x['inject_time']} s; midpoint {mid}",consequence='Biên telemetry suy ra injection; xóa nhãn/tên chưa đủ; không là onset'))
        graph=x.get('trace',{}).get('graphs',{}).get('pre_injection',{})
        for degree in graph.get('degrees',[]):
            if degree['service']==x['root']:
                MAPPING.append(dict(dataset=m['dataset'],label=x['root'],target=degree['service'],level='service',status='FACT trên graph ca làm root',source=src('results/T-002/local-inspection/run-002/cases.json',x['case']),detail=f"in={degree['in_degree']}; out={degree['out_degree']}; graph quan sát"))
    c=[pub('công khai; dữ liệu MIT được HF/README tác giả khai báo','results/T-002/public-metadata/run-002/sources/hf-README.md'),fact(f"{m['n_cases']} ca; root/fault/repeat từ directory; inject_time là lúc tiêm",pmeta,f'[{idx}]'),parent,modality,fact(f"{m['n_root_services']} root/{len(cells)} ô; repeats {min(cells.values())}–{max(cells.values())}",pmeta,f'[{idx}]')+'; '+op('vị trí runtime toàn release chưa biết; bậc mẫu không topology mới'),pub('tài nguyên+mạng' if suite.startswith('re2') else 'lỗi mã nguồn f1–f5 theo sửa code','results/T-002/public-metadata/run-002/sources/github-README.md'),fact('probe theo q=.95/.99/.995 chỉ descriptive; không nhãn causal propagation','results/T-002/local-inspection/run-002/probe-case-summary.csv')+'; '+op('lan nhân quả chưa chứng minh',inp='control/load/nhãn độc lập P4') if ll else op('chưa kiểm lan; không vì không có file','Người làm P4','dev được phép sau G1'),normal,pub('tác giả Pham et al.; stress-ng/tc/sửa code; Prometheus/cAdvisor/Istio, Jaeger, Vector/Loki/Elasticsearch; cùng họ','results/T-002/public-metadata/run-002/sources/github-README.md')+'; '+op('C9 cả ba trục chưa chứng minh cặp độc lập','Minh','bằng chứng so các họ','G1')]
    add(m['dataset'],'RCAEval',f"metadata {len(cc)}; telemetry {len(ll)}",c,fact(f"{m['total_file_bytes']} byte metadata whole suite",pmeta,f'[{idx}].total_file_bytes')+'; adapter/RAM OPEN','service','injection, không onset/end','Có root-service; alias frontendservice→frontend phải tường minh','Có điều kiện known-injection window','Chưa có protocol blind hợp lệ: midpoint leakage; normal sạch/negative coverage OPEN','Không nhãn trace anomaly đã xác minh',exposure='TX1/TX2' if ll else 'TX0',mapping='degrees từng ca/root ở root-mapping.csv; không chèn root vắng vào graph')
    CENSUS.extend(dict(dataset=m['dataset'],root=r,fault=f,count=n) for (r,f),n in cells.items())

# SS: full census, empty trace release and boundary leakage.
pss='results/T-019/census-summary.json'; ss=js(pss); ssc=rows('results/T-019/census-cases.csv'); scases=js('results/T-019/inspection/cases.json'); sb=rows('results/T-019/inspection/boundaries.csv')
for idx,m in enumerate(ss):
    cc=[x for x in ssc if x['dataset']==m['dataset']]; ll=[x for x in scases if x['dataset']==m['dataset']]; bounds=[x for x in sb if x['dataset']==m['dataset'] and x['modality']=='metric']
    cells=Counter((x['root'],x['fault']) for x in cc)
    for key,n in [('cases',len(cc)),('cells',len(cells)),('trace_cases',sum(int(x['trace']) for x in cc)),('log_cases',sum(int(x['log']) for x in cc)),('metric_cases',sum(int(x['metric']) for x in cc)),('bytes',sum(int(x['bytes']) for x in cc)),('root_cause_cases',sum(int(x['root_cause']) for x in cc))]: ck('T-019',pss,f'[{idx}].{key}',m[key],n,'sum/count census-cases.csv '+key)
    for root,n in m['roots'].items():ck('T-019',pss,f'[{idx}].roots.{root}',n,sum(x['root']==root for x in cc),'group census root')
    for fault,n in m['faults'].items():ck('T-019',pss,f'[{idx}].faults.{fault}',n,sum(x['fault']==fault for x in cc),'group census fault')
    for x in bounds:
        mid=(float(x['min_epoch'])+float(x['max_epoch']))/2-next(z['injection'] for z in ll if z['case']==x['case'])
        ck('T-019','results/T-019/inspection/boundaries.csv',x['case']+'.midpoint_minus_injection',float(x['midpoint_minus_injection']),mid,'min/max epoch and per-case injection','SS midpoint')
    window=sorted({(x['start_minus_injection'],x['end_minus_injection'],x['pre_rows'],x['post_rows']) for x in bounds})
    c=[pub('MIT từ HF/tác giả; không suy quyền bên thứ ba','results/T-019/sources-audit/source-report.md'),fact(f"{len(cc)} ca, {len(m['roots'])} root; inject_time, không onset/end",pss,f'[{idx}]'),fact(f"0 trace file/{len(cc)} ca; parent không xác định",pss,f'[{idx}].trace_cases'),fact(f"metric {m['metric_cases']}; log {m['log_cases']}; không trace để join",pss,f'[{idx}]'),fact(f"{len(m['roots'])} root/{len(cells)} ô; kiến trúc tĩnh có giới hạn",pss,f'[{idx}]')+'; '+op('runtime root position không đo được từ release không trace'),pub('lỗi code f1–f4; bảng HF f1–f5 lệch tree' if m['dataset']=='RE3-SS' else 'tài nguyên/mạng; RE1 không socket, RE2 có socket','results/T-019/sources-audit/source-report.md'),fact('probe paired entity 3q có control; không nhân quả','results/T-019/inspection/probe-summary.csv')+'; '+op('lan nhân quả cần nguồn độc lập P4'),fact('biên metric/pre/post rows '+str(window),'results/T-019/inspection/boundaries.csv')+'; '+op('healthy và adequacy theo phương pháp chưa chứng minh'),pub('cùng RCAEval: author/injector/collector chung','results/T-019/sources-audit/source-report.md')+'; '+op('không đủ C9 chỉ vì khác hệ','Minh','họ khác có ba trục','G1')]
    add(m['dataset'],'RCAEval','toàn SS release metadata/telemetry',c,fact(f"{m['bytes']} byte",pss,f'[{idx}].bytes')+'; adapter/RAM OPEN','service','injection; 8 root_cause indicator file RE3 không là onset','Root-service được nhãn; metric/architecture task; trace ranking không chạy','Known-injection có điều kiện','Chưa blind: tất cả metric midpoint=injection; protocol negative/clock OPEN','Không nhãn trace và không trace release',exposure='TX1/TX2',mapping='architecture-root-positions.csv là hình tĩnh, không runtime')
    LEAKS.append(dict(dataset=m['dataset'],kind='file boundary',evidence=src('results/T-019/inspection/boundaries.csv'),value=str(window),consequence='midpoint injection dù bỏ inject_time/path'))
    CENSUS.extend(dict(dataset=m['dataset'],root=r,fault=f,count=n) for (r,f),n in cells.items())

# Nezha count/hash from per-file evidence, injection-conditioned traces separated from daily metrics.
pn='results/T-008/runs/run-001/summary.json'; ns=js(pn); nl=js('results/T-008/runs/run-001/labels.json'); ne=js('results/T-008/runs/evidence-002/summary.json'); na=js('results/T-008/runs/file-audit-001/summary.json'); leak=js('results/T-008/runs/sampling-leakage-001/result.json')
for ds in ['OB','TT']:
    labels=[x for x in nl if x['dataset']==ds]; ffiles=[x for x in na['results'] if x['path'].startswith('online-boutique/' if ds=='OB' else 'train-ticket/')]
    s=ne['datasets'][ds]; ncells=Counter((x['service'],x['fault']) for x in labels)
    for key,n in [('files',len(ffiles)),('bytes',sum(x['bytes'] for x in ffiles)),('rows',sum(x.get('rows',0) for x in ffiles)),('trace_files',sum('/trace/' in x['path'] for x in ffiles)),('metric_files',sum(bool(x.get('numeric')) for x in ffiles))]: ck('T-008','results/T-008/runs/evidence-002/summary.json',f'datasets.{ds}.{key}',s[key],n,'sum per-file audit '+key+'; resource numeric file definition, not all paths /metric/')
    ck('T-008','results/T-008/runs/evidence-002/summary.json',f'datasets.{ds}.unique_parent_fraction',s['unique_parent_fraction'],s['span_parent']['unique_resolved_within_file']/s['nonroot_denominator'],'resolved / nonroot denominator')
    for x in labels:MAPPING.append(dict(dataset='Nezha-'+ds,label=x['entity_raw'],target=x['service'],level='pod→service',status='FACT source labels alias; clock separate',source=src('results/T-008/runs/run-001/labels.json',f'{ds}:{x["date"]}:{x["hour"]}:{x["index_in_hour"]}'),detail='không dùng alias để chọn SLI'))
    normal_durations=[x['end']-x['start'] for x in s['normal_trace_windows']]
    for modality in ['trace+log','metric ngày']:
        c=[fact('download/hash khớp, '+str(s['files'])+' CSV', 'results/T-008/runs/evidence-002/summary.json',f'datasets.{ds}.files')+'; '+op('repo MIT/artifact other-open chưa đủ scope dataset','Tác giả/Minh','quyền data release','trước P3'),fact(f"{len(labels)} injection records/{len({x['service'] for x in labels})} roots/{len(ncells)} cells; text–epoch riêng",'results/T-008/runs/run-001/labels.json'),fact(f"resolved {s['span_parent']['unique_resolved_within_file']}/{s['nonroot_denominator']}; ambiguous {s['span_parent'].get('ambiguous_within_file',0)}",'results/T-008/runs/evidence-002/summary.json',f'datasets.{ds}.span_parent') if modality=='trace+log' else fact('phần metric không có trace span; trace có release riêng','results/T-008/runs/evidence-002/summary.json',f'datasets.{ds}'),fact(str(s['log_join']), 'results/T-008/runs/evidence-002/summary.json',f'datasets.{ds}.log_join') if modality=='trace+log' else fact(f"{s['metric_files']} metric CSV; TimeStamp−Time text distributions riêng",'results/T-008/runs/evidence-002/summary.json',f'datasets.{ds}.metric_timestamp_minus_text_seconds'),fact(f"{len({x['service'] for x in labels})} root/{len(ncells)} cells; graph clock hypotheses trong root_windows",'results/T-008/runs/evidence-002/summary.json','root_windows')+'; '+op('vị trí/clock toàn bộ chưa khóa'),fact(str(dict(Counter(x['fault'] for x in labels))),'results/T-008/runs/run-001/labels.json'),fact('Duration probe 3q ngoài declared root có control; không vùng/nhân quả','results/T-008/runs/trace-symptoms-002/result.json')+'; '+op('causal propagation chưa chứng minh'),fact('normal trace observed duration s='+str(normal_durations),'results/T-008/runs/evidence-002/summary.json',f'datasets.{ds}.normal_trace_windows')+'; '+op('construct metric có duplicate fault; không đủ clean normal','Người làm P3/tác giả','normal capture riêng'),pub('Yu et al.; code Byteman/Hypno/Failpoint; OTel/Tempo, Promtail/Loki, Prometheus','results/T-008/sources/README.md')+'; '+op('injector resource và C9 đủ ba trục chưa khóa','Minh','source injector+collector','G1')]
        add(f'Nezha-{ds} / {modality}','Nezha',modality,c,fact(f"whole system CSV {s['bytes']} byte (hai modality chia sẻ, không cộng lại)",'results/T-008/runs/evidence-002/summary.json',f'datasets.{ds}.bytes')+'; adapter OPEN','service/pod alias','injection text + epoch; TT có clock conflict','Có root service sau clock/mapping','Known-window conditional','Trace/log: không continuous blind F1; chỉ phút tiêm,+1,+2, thiếu negatives' if modality=='trace+log' else 'Metric ngày: có negative coverage tiềm năng nhưng clock/normal/continuous protocol OPEN','Không nhãn anomalous từng trace đã xác minh',mapping='root-mapping.csv và root_windows nguồn',exposure='TX1')
    CENSUS.extend(dict(dataset='Nezha-'+ds,root=r,fault=f,count=n) for (r,f),n in ncells.items())
for gi,g in enumerate(leak['groups']):
    for modality,m in g['modalities'].items():
        ck('T-008','results/T-008/runs/sampling-leakage-001/result.json',f'groups[{gi}].modalities.{modality}.files',m['files'],3*g['label_records'],'3 × labels of date','injection-conditioned file count')
        assert m['matches'] and not m['unexpected'] and not m['missing']
        LEAKS.append(dict(dataset='Nezha-'+g['dataset'],kind='sampling/file existence/path',evidence=src('results/T-008/runs/sampling-leakage-001/result.json',f'groups[{gi}]'),value=f"{g['date']}: {m['files']} {modality} files = 3×{g['label_records']} records",consequence='Chỉ phút injection,+1,+2; không có file không đồng nghĩa healthy'))

# Eadro source-level session dedup: repeated hashes do not double incident count.
pe='results/T-009/runs/inspect-004/independent-summary.json'; es=js(pe); el=js('results/T-009/runs/inspect-004/labels-all.json'); sessions=js('results/T-009/runs/inspect-004/raw-sessions.json')
for ds in ['SN','TT']:
    events=[]; seen=set()
    for x in el:
        if x['dataset']!=ds:continue
        for f in x['label']['faults']:
            key=(f['name'],f['fault'],f['start'],f['duration'])
            if key not in seen:seen.add(key);events.append(f)
    s=es['datasets'][ds]
    # outer label names give service by published Docker naming; nginx alias stays unresolved.
    roots={re.sub(r'-\d+$','',re.sub('^(socialnetwork|trainticket)-','',f['name'])) for f in events}
    ecells=Counter((re.sub(r'-\d+$','',re.sub('^(socialnetwork|trainticket)-','',f['name'])),f['fault']) for f in events)
    ps='results/T-009/runs/run-001/summary.json'; ms=js(ps)[ds]
    for k,v in ms.items():
        if isinstance(v,(int,float)) and not isinstance(v,bool):
            if 'injection' in k or k=='events': ck('T-009',ps,f'{ds}.{k}',v,len(events),'union original fault tuples')
            elif k in ['root_services','roots','root_service_count']:ck('T-009',ps,f'{ds}.{k}',v,len(roots),'nunique normalized declared root')
            elif k in ['cells','root_fault_cells','observed_cells']:ck('T-009',ps,f'{ds}.{k}',v,len(ecells),'nunique declared root × fault')
    # Reconstruct dedup identity from one representative per canonical session.
    reps={}
    for x in sessions:
        if x['dataset']==ds:
            name=x['case'].split('/')[-1];reps.setdefault(name,x)
    for k in ['spans','parent_references','parent_unique_identity','parent_missing','parent_ambiguous']:
        ck('T-009',pe,f'datasets.{ds}.trace_counts.{k}',s['trace_counts'][k],sum(x['trace']['counts'].get(k,0) for x in reps.values()),'sum representative canonical raw sessions; duplicates same content')
    ck('T-009',pe,f'datasets.{ds}.unique_raw_sessions',s['unique_raw_sessions'],len(reps),'nunique canonical session')
    for k in ['metric_files','metric_rows']:
        value=sum(len(x['metrics']) if k=='metric_files' else sum(z['rows'] for z in x['metrics']) for x in reps.values())
        ck('T-009',pe,f'datasets.{ds}.{k}',s[k],value,'count/sum metrics per unique session')
    declared=js('results/T-009/runs/run-001/source_claims.json')
    c=[fact('ZIP hash/CRC inspected','results/T-009/runs/inspect-004/summary.json')+'; '+op('data/code license scope chưa có điều khoản rõ','Tác giả/Minh','permission nguồn','trước P3'),fact(f"{len(events)} incident labels; {len(roots)} roots/{len(ecells)} cells; mỗi ô một repeat",'results/T-009/runs/inspect-004/labels-all.json')+f"; FACT công bố {declared['reported_injections'][ds]} injections (định nghĩa khác artifact)",fact(f"strict parent refs {s['trace_counts']['parent_references']}; missing {s['trace_counts']['parent_missing']}; unique identity {s['trace_counts']['parent_unique_identity']}",pe,f'datasets.{ds}.trace_counts'),fact(f"metrics {s['metric_rows']} rows/{s['metric_files']} files; log {s['log_counts']}",pe,f'datasets.{ds}'),fact(f"{len(roots)} roots/{len(ecells)} ô; graph whole-file, không injection-time graph",'results/T-009/runs/inspect-004/root-degree-whole-file.json')+'; '+op('clock injection vs span chưa khóa'),fact(str(dict(Counter(x['fault'] for x in events))),'results/T-009/runs/inspect-004/labels-all.json'),fact('metric probe3q/reference normal/control, chưa causal labels','results/T-009/runs/inspect-004/symptom-metrics.json')+'; '+op('ngoài root alias nginx-thrift chưa đủ và causal propagation OPEN'),fact('có phiên faults=[] riêng; warmup/load đại diện chưa chứng minh','results/T-009/runs/inspect-004/labels-all.json')+'; '+op('normal adequacy theo phương pháp'),pub('Lee/Yang/Chen/Su/Lyu; Chaosblade; Jaeger,cAdvisor/Prometheus→InfluxDB,Fluentd/ELK','results/T-009/runs/run-001/source_claims.json')+'; '+op('collector overlap RCAEval; C9 ba trục chưa đủ','Minh','source comparison','G1')]
    add('Eadro-'+ds,'Eadro','all released ZIP + nested member representations',c,pub(f"ZIP {78753809 if ds=='SN' else 48923113} byte; adapter/RAM OPEN",'results/T-009/runs/download-001/manifest.json'),'service','start/duration/end injection; chưa onset/recovery','Có root-service sau alias/clock; root vắng trace giữ denominator','Known injection conditional','Chưa blind hợp lệ: source capture/clock chưa đủ; align.py overlapping sliding samples; checkpoint test-HR@1 phải đổi protocol','Không nhãn trace anomaly',mapping='Docker name→service từ source; nginx-thrift→nginx-web-server CANDIDATE, chưa gold')
    CENSUS.extend(dict(dataset='Eadro-'+ds,root=r,fault=f,count=n) for (r,f),n in ecells.items())

# DeepTraLog raw and graph; trace-label task is not root ranking.
pd='results/T-010/runs/inspect-005/summary.json'; d=js(pd); raw=js('results/T-010/runs/inspect-002/raw-cases.json'); dr=js('results/T-010/runs/inspect-002/summary.json'); dg=js('results/T-010/runs/inspect-005/graph-audit.json'); cov=js('results/T-010/runs/inspect-008/summary.json')
ck('T-010','results/T-010/runs/inspect-002/summary.json','span_rows',dr['span_rows'],sum(x['span_rows'] for x in raw),'sum raw-case span_rows')
for k in ['graph_records','graph_total_nodes','graph_total_edges','graph_bad_edges']:
    field={'graph_records':'graphs','graph_total_nodes':'nodes','graph_total_edges':'edges','graph_bad_edges':'bad_edge_indices'}[k]
    ck('T-010',pd,k,d[k],sum(x['counts'][field] for x in dg),'sum graph-audit counts.'+field)
dcoverage=js('results/T-010/runs/inspect-008/per-label-coverage.json')
ck('T-010',pd,'abnormal_graph_in_raw_normal',d['abnormal_graph_in_raw_normal'],sum(v['in_raw_normal_span'] for k,v in dcoverage.items() if k!='normal'),'sum abnormal per-label raw-normal overlaps')
ck('T-010',pd,'lineage.abnormal_trace_in_named_case',d['lineage']['abnormal_trace_in_named_case'],sum(d['abnormal_case_counts'].values()),'sum abnormal_case_counts')
ck('T-010',pd,'lineage.graph_trace_absent_raw',d['lineage']['graph_trace_absent_raw'],d['graph_records']-d['lineage']['graph_trace_in_raw'],'total graph - in raw')
ck('T-010','results/T-010/runs/inspect-008/summary.json','total_graphs',cov['total_graphs'],sum(v['graph'] for v in dcoverage.values()),'sum graph labels per-label-coverage')
for part in ['raw trace+log','processed event graph']:
    c=[fact('file hash/CRC, 37 files incl all-log','results/T-010/runs/download-003/manifest.json')+'; '+op('permission data/code OPEN','Tác giả/Minh','license source','trước P3'),fact('132485 trace labels; 23334 abnormal/109151 normal; root/time gold per instance absent',pd)+'; '+op('root/incident/time mapping không thể suy F-code','Tác giả/Minh','branch+instance binding','G1/P3'),fact(f"raw spans {dr['span_rows']}; scoped parent; event graph không service call graph",'results/T-010/runs/inspect-002/raw-cases.json'),fact('resource metric riêng không có; log SW_CTX; graph/raw same lineage','results/T-010/runs/run-001/count-summary.json')+'; '+op('C4 resource metric không có trong release kiểm'),fact('35 observed raw services; root position undefined do thiếu gold','results/T-010/runs/inspect-006/tables.json')+'; '+op('root position thiếu input'),pub('faulty code branches Fudan/14 kinds; graph70 instance labels; catalogF23–25 không có','results/T-010/runs/catalog-review-001/catalog.json'),op('không định nghĩa ngoài-root vì thiếu root gold/resource metric','Tác giả/Người làm P3','branch/instance nhãn root','P3'),fact('10 normal ZIP, 81037 raw normal trace-ID; 28116 graph normal thiếu raw span',pd)+'; '+op('warmup/timeline/normal clean chưa chứng minh'),pub('FudanSELab; faulty branches; SkyWalking/Elasticsearch','results/T-010/runs/run-001/sources/README.md')+'; '+op('reuse upstream TT với họ khác chưa khóa, C9 chưa đủ','Minh','branch/revision lineage','G1')]
    add('DeepTraLog-TT / '+part,'DeepTraLog',part,c,fact('728831613 byte tải cả raw+graph+all-log; shared, không cộng hai hàng','results/T-010/runs/download-003/manifest.json')+'; adapter/embedding source OPEN','trace; root-ranking OPEN','không injection/onset/end thật trong graph; không suy ID','OPEN root gold; catalog chỉ gợi ý một phần','Không time labels thật','Không chấm temporal blind bằng trace_bool/ID; path F/normal và graph class/type lộ nhãn','Trace anomaly có 132485 labels; raw coverage 104369/132485 cần conditional reporting',mapping='id_service có 35 entities; F5/F12 catalog không per-instance gold')

# LEMMA IT: separate complete sample inspection from original metadata release.
lp='results/T-011/file-inspection-summary.json'; ls=js(lp); lmeta=js('results/T-011/runs/run-001/count-summary.json'); lfiles=js('results/T-011/runs/inspect-008/summaries.json'); la=js('results/T-011/runs/inspect-008/archives.json')
for ds,key in [('PR','Product_Review'),('Cloud','Cloud_Computing')]:
    a=ls['datasets'][key]
    relevant=[x for x in lfiles if key in str(x.get('archive',''))]
    archives=[x for x in la if key in x['path']]
    ck('T-011',lp,f'datasets.{key}.zip_bytes',a['zip_bytes'],sum(x['zip_bytes'] for x in archives),'sum zip bytes of sample archives')
    ck('T-011',lp,f'datasets.{key}.member_bytes',a['member_bytes'],sum(m['bytes'] for x in archives for m in x['members']),'sum all sample member bytes')
    for k in ['csv_rows','csv_files','npy_files']:
        filt=[x for x in relevant if str(x.get('member','')).endswith('.csv' if k.startswith('csv') else '.npy')]
        n=sum(x.get('rows',0) for x in filt) if k=='csv_rows' else len(filt)
        if filt:ck('T-011',lp,f'datasets.{key}.{k}',a[k],n,'sum/count summaries.json member extension')
    for form in ['Preprocessed sample','Original metadata']:
        mk=key+('_Preprocessed' if form.startswith('Pre') else '_Original'); size=lmeta['datasets'][mk]['archive_bytes']
        c=[fact('public HF revision/LFS byte metadata', 'results/T-011/runs/run-001/count-summary.json','datasets.'+mk)+'; '+op('NC/ND contradictory statements; internal research inspection authorized but redistribution scope unresolved','Tác giả/Minh','exact license statement','trước P3/công bố'),pub('PR MongoDB-v1 vs external NFS disk-full' if ds=='PR' else 'Cloud root AP instance i-078923fb30cac1ede; PPTX bug03:10Z/failure03:10:51Z; JSON6h conflict','results/T-011/the-dataset.md')+'; trích thẻ, chưa kiểm lại timeline gốc; '+op('root/time toàn release census OPEN','Tác giả/P3','per-incident timeline/mapping'),fact('0 span table trong mẫu preprocessed; Original parent OPEN',lp) if form.startswith('Pre') else op('Original schema parent chưa kiểm','P3','schema Original theo quyền G1'),fact(f"{a['csv_rows']} CSV rows/{a['npy_files']} NPY; chỉ ngày mẫu",lp,f'datasets.{key}') if form.startswith('Pre') else pub('metric/log theo source inventory; actual quality OPEN','results/T-011/runs/run-001/count-summary.json','datasets.'+mk),op('census incident/root position toàn release chưa có','Tác giả/P3','root labels/graph thật'),pub('PR external storage disk full; Cloud API infinite loop→CPU','results/T-011/the-dataset.md')+'; trích thẻ, chưa kiểm lại PPTX/source-config',op('PR thiếu normal/time đủ; Cloud band/control descriptive không nhân quả','P3','normal đúngclock/label indépendante'),op('PR normal timeline chưa khóa; Cloud trướcbug24h chưa healthyGT','Tác giả/P3','timeline nhãn và healthy capture'),pub('Zheng et al.; PR OpenShift/Prometheus/Elasticsearch; Cloud CloudWatch/JMeter; injector từng scenario OPEN','results/T-011/xac-minh-nguon-va-doc-lap.md')+'; '+op('Original/Preprocessed cùng raw; C9 injector chưa đủ','Minh','injector campaign sources','G1')]
        add('LEMMA-'+ds+' / '+form,'LEMMA IT',form,c,fact(f"whole release archive {size} byte; sample {a['zip_bytes']} byte nếu Preprocessed",'results/T-011/runs/run-001/count-summary.json','datasets.'+mk)+'; adapter/RAM OPEN','benchmark MongoDB pod vs NFS cause' if ds=='PR' else 'AWS instance','PR timing OPEN; Cloud bug/failure source and epoch conflict','Có điều kiện đúng unit sau nguồn timeline','Conditional timeline chưa đủ','Chưa blind: KPI selector/data provenance, normal clock unresolved; không chọn arbitrary first segment','Không span-level labels/trace verified',exposure='TX1' if form.startswith('Pre') else 'TX0',mapping='PR không đổi benchmark MongoDB thành NFS; Cloud instance không tự service')

# T012 releases: original result evidence or explicit published-only/open.
profiles=js('results/T-012/profiles.json'); pf='results/T-012/runs/fse-file-inspect-003/census.json'; fc=js(pf); fcases=js('results/T-012/runs/fse-file-inspect-003/cases.json'); valid=[x for x in fcases if not x['invalid_marker']]
for k,n in [('case_folders',len(fcases)),('valid_cases',len(valid)),('root_count',len({r for x in valid for r in x['roots']}))]:ck('T-012',pf,k,fc[k],n,'count/union fse cases after invalid marker filter')
bankp='results/T-012/runs/bank-label-reproduce-002/census.json'; bank=js(bankp); records=rows('results/T-012/runs/bank-label-reproduce-002/record.csv')
for k,n in [('events',len(records)),('roots',len({x['component'] for x in records})),('reasons',len({x['reason'] for x in records})),('days',len({x['datetime'].split()[0] for x in records})),('root_reason_cells',len({(x['component'],x['reason']) for x in records}))]:ck('T-012',bankp,k,bank[k],n,'record.csv count/nunique '+k)
tz=timezone(timedelta(hours=8)); matches=sum(datetime.strptime(x['datetime'],'%Y-%m-%d %H:%M:%S').replace(tzinfo=tz).timestamp()==float(x['timestamp']) for x in records)
ck('T-012',bankp,'timestamp_matches_utc8',bank['timestamp_matches_utc8'],matches==len(records),'all datetime UTC+8 epoch == original timestamp; 136 matches/136')
for r,n in bank['root_counts'].items():ck('T-012',bankp,'root_counts.'+r,n,sum(x['component']==r for x in records),'group component count')
for r,n in bank['reason_counts'].items():ck('T-012',bankp,'reason_counts.'+r,n,sum(x['reason']==r for x in records),'group reason count')
for (r,f),n in Counter((x['component'],x['reason']) for x in records).items():CENSUS.append(dict(dataset='OpenRCA — Bank',root=r,fault=f,count=n))
for x in records:MAPPING.append(dict(dataset='OpenRCA — Bank',label=x['component'],target=x['component'],level=x['level'],status='FACT label identity; service alias OPEN',source=src('results/T-012/runs/bank-label-reproduce-002/record.csv'),detail='không ép pod label thành service'))
reuse=js('results/T-012/runs/trca-reuse-001/result.json')
ck('T-012','results/T-012/runs/trca-reuse-001/result.json','csv_files',reuse['csv_files'],len(reuse['rows']),'count member hash rows')
ck('T-012','results/T-012/runs/trca-reuse-001/result.json','exact_nezha_matches',reuse['exact_nezha_matches'],sum(x['nezha_match'] for x in reuse['rows']),'sum original member nezha_match')
for p in profiles:
    name=p['name']; ip=p.get('inspection_stage'); public_sources='; '.join(src('results/T-012/'+x['path']) for x in p['sources'])
    psrc='results/T-012/profiles.json'; prefix=f'[{profiles.index(p)}]'
    c=[]
    for k in ['access','labels','trace','modalities','positions','faults','symptoms','normal','independence']:
        val=p.get(k,'thiếu bằng chứng')
        # Published-only entries remain at source evidence level; not promoted to measured.
        if ip in ['file-inspected','metadata-and-labels-only']:
            c.append(op(val,'Tác giả/P3','nguồn release/nhãn/adapter đúng phạm vi','G1/P3')+'; trích profile, chưa kiểm lại' if k in ['positions','normal'] else fact(val,psrc,prefix+'.'+k)+'; trích profile, chưa kiểm lại')
        else:
            c.append(pub(val,psrc,prefix+'.'+k)+'; trích profile, chưa kiểm lại; '+op('chưa có file-release/schema/census tương ứng','Tác giả/P3','public immutable release','G1/P3'))
    c[0]+='; '+op(p['license'],'Tác giả/Minh','data/code license exact scope','trước P3/công bố')
    exposure='TX1' if ip=='file-inspected' else 'TX0'
    if 'FSE fault' in name:
        c[1]=fact(f"8 ca không invalid/10 folders; 11 root services union, multi-root set; start/end injection UTC",pf)
        c[2]=fact('parent/graph từng phase; không gộp root-set vào1 service','results/T-012/runs/fse-file-inspect-003/cases.json')
        c[3]=fact('metric+log+trace schemas đã inspection','results/T-012/runs/fse-file-inspect-003/schemas.json')
        c[4]=fact('11 union roots/8 root-set×fault cells; repeats1',pf)+'; '+op('root degree per-case chưa class hub')
        c[5]=fact('8 fault codes trong8 ca không-invalid, không thay25kindspublished',pf,'fault_types')
        c[6]=fact('3q descriptive control/metric/duration, không GT vùng','results/T-012/runs/fse-file-inspect-003/descriptive-bands.json')+'; '+op('causal propagation OPEN')
        c[7]=fact('normal env pre-duration240s; clean/SLI độc lập chưa xác lập','results/T-012/runs/fse-file-inspect-003/cases.json')+'; '+op('adequacy phương pháp cần kiểm P3')
        for x in valid:
            for r in x['roots']:MAPPING.append(dict(dataset=name,label=r,target=r,level='service set; pod/container/span khác cấp',status='FACT ground_truth source',source=src('results/T-012/runs/fse-file-inspect-003/cases.json',x['case']),detail='không ép multi-root thành single root'))
        LEAKS.append(dict(dataset=name,kind='normal/abnormal phase and capture boundary',evidence=src('results/T-012/runs/fse-file-inspect-003/cases.json','environment'),value='NORMAL_END = ABNORMAL_START = injection',consequence='phase names/concat boundary lộ injection; không temporal blind từ nguyên capture'))
    elif 'AnoMod' in name:
        sys='SN_data' if 'SocialNetwork' in name else 'TT_data'; ac=js('results/T-012/runs/anomod-file-inspect-003/census.json')['by_system'][sys]
        c[1]=fact('13 captures =12faulty+1baseline; target source không runtime root gold','results/T-012/runs/anomod-file-inspect-003/census.json','by_system.'+sys)+'; '+op('incident time/start/end/onset chưa bind','Tác giả/P3','runtime injection timeline')
        c[2]=fact('SN scoped Jaeger, TT segment+span parent; không merge int IDs xuyên segment','results/T-012/runs/anomod-followup-002/trace-export-checks.json')
        c[3]=fact('trace+metric+containerlog; schema thật','results/T-012/runs/anomod-file-inspect-003/files.json')
        c[4]=fact('12 declared targets, không12 gold root incidents','results/T-012/runs/anomod-file-inspect-003/census.json')+'; '+op('root graph positions không gold')
        c[5]=pub('SN Code_Stop là docker stop; TT code return/throw; database/host target không tựservice','results/T-012/runs/anomod-collector-review-001/manifest.json')
        c[6]=fact('duration probe outside declared target, control/3q; không outside gold root','results/T-012/runs/anomod-followup-002/descriptive-bands.json')+'; '+op('true propagation chưa có nhãn')
        c[7]=fact('1baseline capture; reset/load/warmup chưa independentlyhealthy','results/T-012/runs/anomod-file-inspect-003/census.json')+'; '+op('adequacy P3')
    elif 'TRCA' in name:
        ds='TT' if 'TrainTicket' in name else 'OB'
        base=next(x for x in DATASETS if x['dataset']==f'Nezha-{ds} / trace+log')
        c=[base[f'C{i}'] for i in range(1,10)]
        c[0]=fact('1165CSV+4labels match Nezha byte-for-byte; reuse quyền không tự giải','results/T-012/runs/trca-reuse-001/result.json')+'; '+op('license reused input scope','Tác giả/Minh','quyền Nezha/TRCA data','trước P3')
        c[8]=fact('byte-identical Nezha; cùng raw không dataset độc lập','results/T-012/runs/trca-reuse-001/result.json')
        p['detection']+=' Metric ngày là scope riêng như Nezha metric ngày.'
    elif name=='OpenRCA — Bank':
        c[0]=fact('Drive directory/label bytes accessible; record hash/CRC; full ZIP revision mutable','results/T-012/runs/bank-metadata-001/summary.json')+'; '+pub('code MIT', 'results/T-012/runs/run-002/sources/openrca-LICENSE')+'; '+pub('data CC BY-NC 4.0, source statement', 'results/T-012/runs/run-002/sources/openrca-paper.txt')+'; '+op('điều kiện data chính xác và immutable full revision cần khóa trước sử dụng/công bố', 'Minh/Tác giả', 'license áp dữ liệu và full revision', 'trước P3/công bố')
        c[1]=fact(f"{len(records)} labels; timestamp/text UTC+8 matches={matches}; level pod component, occurrence time chưa chứng minh injection/onset",bankp)
        c[2]=pub('schema timestamp,cmdb_id,parent_id,span_id,trace_id,duration; parent quality chưa xem','results/T-012/runs/run-002/sources/openrca-paper.txt')+'; '+op('parent quality tới G3','Người làm P7','giữ ngoài telemetry','G3')
        c[3]=pub('Bank trace+metric+log','results/T-012/runs/run-002/sources/openrca-paper.txt')+'; '+op('schema quality/linkage tới G3','Người làm P7','giữ ngoài telemetry','G3')
        c[4]=fact('14 components/52 root×reason cells/9dates; vị trí graph chưa biết',bankp)+'; '+op('graph root position tớiG3','P7','giữ ngoài telemetry','G3')
        c[5]=fact('8 reasons CPU/memory/disk/network/JVM; không seeded-code label',bankp,'reason_counts')
        c[6]=op('C7 giữ ngoài được MRP cho phép OPEN; không loại vì chưa mở','Người làm P7','telemetry sauMinh cho phép','G3')
        c[7]=op('normal sạch/đủ/load/clock chưa mở','Người làm P7','telemetry sauMinh cho phép','G3')
        c[8]=pub('AIOps raw reuse; tác giả nguồn gốc/injector/collector chưa định danh đủ','results/T-012/runs/run-002/sources/openrca-paper.txt')+'; '+op('C9 đủ ba trục chưa chứng minh','Minh','source AIOps edition/injector/collector','G1')
    # Source-only candidates intentionally have no fake schema pass.
    add(name,'T012:'+p['identity'].split(';')[0],p.get('version','source-only'),c,pub(p['size'],psrc,prefix+'.size')+'; trích profile, chưa kiểm lại; adapter/RAM OPEN','root set/service/pod/instance tùy source','injection' if 'FSE fault' in name or 'OpenRCA 2.0' in name else 'source occurrence/config/test label; onset OPEN',p['ranking'],p['detection'],p['detection']+'; mode b path/capture/query risk ở leakage-data.csv',p['trace_task'],p['region'],exposure,mapping='root-mapping.csv; nếu thiếu mapping thì OPEN, không ép entity unit',sources=public_sources)

# Other preprocessed dates have metadata, not the quality facts of the inspected sample.
for key in ['PR','Cloud']:
    base=next(x for x in DATASETS if x['dataset']==f'LEMMA-{key} / Original metadata')
    sample=next(x for x in DATASETS if x['dataset']==f'LEMMA-{key} / Preprocessed sample')
    c=[base[f'C{i}'] for i in range(1,10)]
    c[2]=op('các ngày Preprocessed ngoài mẫu chưa có schema parent thực','P3','schema/day sample sau G1')
    c[3]=pub('modality metric/log theo archive inventory; không dùng quality của ngày mẫu','results/T-011/runs/run-001/count-summary.json')+'; '+op('quality ngày khác chưa kiểm')
    add(f'LEMMA-{key} / Preprocessed other dates metadata','LEMMA IT','các ngày ngoài PR20211203/Cloud20240124',c,sample['cost'],'pod/node/instance, per-release mapping OPEN','timeline từng ngày chưa census','OPEN đúng root/time/unit từng ngày','Chưa đủ timeline/schema','Chưa có blind protocol/schema đủ','Không nhãn trace đã kiểm',exposure='TX0',mapping='Original/processed cùng raw; phải truyền mức tiếp xúc nếu identity chứng minh')
for name in ['Check Your Trace First (TRCA) — TrainTicket','Check Your Trace First (TRCA) — OnlineBoutique']:
    ds='TT' if 'TrainTicket' in name else 'OB'
    base=next(x for x in DATASETS if x['dataset']==f'Nezha-{ds} / metric ngày')
    reuse_source='results/T-012/runs/trca-reuse-001/result.json'
    c=[base[f'C{i}'] for i in range(1,10)]
    c[0]=fact('cùng byte metric Nezha theo member-hash; license reused source OPEN',reuse_source)
    c[8]=fact('cùng byte Nezha; không independent corpus',reuse_source)
    for x in DATASETS:
        if x['dataset']==name:x['dataset']=name+' / trace+log'
    for x in TASKS:
        if x['dataset']==name:x['dataset']=name+' / trace+log';x['mode_b']='Không continuous blind trace/log: phút injection,+1,+2; thiếu negative coverage'
    add(name+' / metric ngày','TRCA/Nezha','daily metric reused byte-identical',c,base['cost'],'pod→service','injection, TT text/epoch conflict','Root service conditional','Known injection conditional','Daily metric continuous protocol/clock/normal OPEN','Không nhãn anomalous trace',mapping='reuse đúng Nezha alias; không thành dataset độc lập')

# Independent check for REVIEW T002 R2/R3/R4 and T019 detailed labels.
# Coverage additions requested by root: metadata-only RE1 TT/OB and historical BARO FSE OB.
# Read saved directory/file inventories only, never the referenced raw filesystem paths.
hfpath='results/T-002/public-metadata/run-002/hf-tree.json'; hf=js(hfpath)
for ds in ['TT','OB']:
    pre='re1'+ds.lower()+'_'
    dd=[x for x in hf if x['type']=='directory' and x['path'].startswith(pre) and '/' not in x['path']]
    ff=[x for x in hf if x['type']=='file' and x['path'].startswith(pre)]
    tuples=[x['path'][len(pre):].rsplit('_',2) for x in dd]
    cells=Counter((x[0],x[1]) for x in tuples)
    ck('T-002',hfpath,f'{pre}directory_count',125,len(dd),'count public HF top-level directory members',f'RE1-{ds} public case census')
    ck('T-002',hfpath,f'{pre}root_count',5,len({x[0] for x in tuples}),'nunique root in HF public case names')
    ck('T-002',hfpath,f'{pre}fault_count',5,len({x[1] for x in tuples}),'nunique fault in HF public case names')
    ck('T-002',hfpath,f'{pre}cells',25,len(cells),'nunique root × fault public directory')
    ck('T-002',hfpath,f'{pre}repeats_min',5,min(cells.values()),'minimum repeat count per public cell')
    ck('T-002',hfpath,f'{pre}repeats_max',5,max(cells.values()),'maximum repeat count per public cell')
    kinds=Counter(x['path'].rsplit('/',1)[-1] for x in ff)
    ck('T-002',hfpath,f'{pre}metrics.parquet',125,kinds['metrics.parquet'],'public telemetry filename inventory, no payload')
    ck('T-002',hfpath,f'{pre}traces.parquet',0,kinds['traces.parquet'],'public trace filename absence, not telemetry inspection')
    ck('T-002',hfpath,f'{pre}logs.parquet',0,kinds['logs.parquet'],'public log filename absence, not telemetry inspection')
    c=[pub('HF data MIT statement','results/T-002/public-metadata/run-002/sources/hf-README.md'),fact('125public ca/5roots/5faults/25cells/5repeat; inject_time filename present',hfpath),op('RE1 metric-only: trace không có theo filename census; actual metric schema chưa đọc' if ds=='TT' else 'public RE1OB có1sample metric schema, không áp toànrelease; local125 identity OPEN','P3','schema trong V7 cho phép sau exact file/range plan'),fact('125metrics.parquet; 0traces/0logs trong public release inventory',hfpath),fact('5root/25cells; graph position OPEN',hfpath)+'; '+op('topology runtime toàn release chưa biết'),pub('cpu/mem/disk/delay/loss theo directory/source',hfpath),op('TX0 public chưa probe C7; local method reproduction không proof causal','P3/P7','control/load sau gate'),op('actual normal timeline/calibration chưa kiểm','P3','normal schema/time budget'),pub('RCAEval/Pham family; không independent RE2/RE3','results/T-002/public-metadata/run-002/sources/paper-v2.html')]
    exposure='TX0' if ds=='TT' else 'HF125:124TX0+1TX1; local125TX2 identityOPEN'
    add('RE1-'+ds,'RCAEval','public HF125; '+('no telemetry read' if ds=='TT' else 'local125 separate manifest,40byte-matchFSE+85identityOPEN'),c,fact(f"public file bytes {sum(x['size'] for x in ff)}; no new payload; adapter/RAM OPEN",hfpath),'service','inject_time filename, chưa actual timeline','Root service from directory; metric/architecture variant conditional','Cần actual timeline/window after schema','File boundary/statistics/runner chưa blind audit; không suy từ RE2','Không trace trong public census',exposure=exposure,mapping='public directory mapping; không suy local↔HF identity khi chưa hash-match',sources=src(hfpath))
    LEAKS.append(dict(dataset='RE1-'+ds,kind='path + unmeasured boundary/statistics',evidence=src(hfpath),value='public directory encodes root/fault/repeat; no telemetry boundary recalc',consequence='Xóa path/root từ features; boundary/normal/statistics của release còn OPEN; không suy mode b sạch từ RE2'))
lm='results/T-019/lineage/local-file-manifest.json'; lmc=[x for x in js(lm) if x['source']=='fse-ob']
lmt=[x['case'].rsplit('_',2) for x in lmc];lmcells=Counter((x[0],x[1]) for x in lmt)
for key,v,new,why in [('n_cases',100,len(lmc),'count fse-ob local original manifest'),('n_roots',5,len({x[0] for x in lmt}),'nunique roots from original manifest cases'),('n_faults',4,len({x[1] for x in lmt}),'nunique faults'),('cells',20,len(lmcells),'nunique root × fault'),('repeat_min',5,min(lmcells.values()),'minimum cell repeat'),('repeat_max',5,max(lmcells.values()),'maximum cell repeat')]:ck('T-019',lm,'BARO-FSE-OB.'+key,v,new,why)
c=[op('BARO Zenodo record11046533 license/data exact scope cần khóa','Minh/Tác giả','record/archive license'),fact('100ca/5roots/4faults/20cells/5repeat; saved metric+inject hashes',lm),op('metric-only historical corpus; schema proof có thể từ original result, chưa đọc payload','P3','saved schema exact release'),fact('metric CSV + injection metadata; không trace/log trong inspected manifest',lm),fact('5roots/20cells; runtime graph position OPEN',lm)+'; '+op('graph độc lập cần architecture/input'),fact('cpu/mem/delay/loss source paths',lm),op('method reruns không causal propagation ground truth','P3/P4','controls and independent labels'),op('normal/reset/load chưa độc lập chứng minh','P3','normal calibration'),pub('BARO/Pham lineage, cùng RCAEval author family','results/T-006/moi-truong.md')+'; '+op('exact injector/collector original campaign cần source khóa','Minh/Tác giả','BARO paper/source')]
add('BARO-FSE-OB','RCAEval historical','Zenodo11046533 metric-only historical reproduction',c,pub('fse-ob.zip150740576bytes; MD5 API kiểm taskcũ','results/T-006/moi-truong.md'),'service','saved inject_time metadata; chưa onset/recovery','Known-marker root service; taskcũ reproduction','Known injection conditional','Historical detector runner conditions; không benchmark blind mới','Không trace',exposure='TX2',mapping='local recording hash identity; RE1OB40copies exact +85unresolved không safe test',sources=src(lm)+'; '+src('results/T-006/moi-truong.md'))
LEAKS.append(dict(dataset='BARO-FSE-OB',kind='path + known marker',evidence=src(lm),value='case=root_fault_repeat, inject_time saved metadata; methods already run',consequence='Historical TX2 reproduction; path và marker không tự blind; runner audit source riêng'))

pb='results/T-002/local-inspection/run-002/probe-case-summary.csv'; prs=rows(pb); er=rows('results/T-002/local-inspection/run-002/symptom-entity-rates.csv')
for i,x in enumerate(prs):
    sub=[z for z in er if z['case']==x['case'] and z['q']==x['q'] and z['signal_group']==x['signal_group'] and z['is_root']=='False' and z['business_name_heuristic']=='True' and z['control_exceed_rate'] and z['post_exceed_rate']]
    if sub:
        for k,ek in [('control_mean_service_rate','control_exceed_rate'),('post_mean_service_rate','post_exceed_rate')]:
            ck('T-002',pb,f'row[{i}].{k}',float(x[k]),statistics.mean(float(z[ek]) for z in sub),'mean outside-root business entities from entity-rates, same scope')
labelaudit=js('results/T-019/sources-audit/label-audit.json')
ck('T-019','results/T-019/sources-audit/label-audit.json','n_files',labelaudit['n_files'],len(labelaudit['entries']),'count label metadata entries')
ck('T-019','results/T-019/sources-audit/label-audit.json','n_unique_file_hashes',labelaudit['n_unique_file_hashes'],len({x['sha256'] for x in labelaudit['entries']}),'nunique original label hashes')
detail_label_outside=sum(not x['indicator_time_in_log_window'] for x in labelaudit['entries'])
write_json('review-rechecks.json',dict(T002=dict(midpoint_target_cases=32,small_graphs=[x['case'] for x in localcases if x['dataset']=='re2tt' and len(x['trace']['graphs']['pre_injection']['nodes'])<27],scope='graph inference remains candidate; no raw workload rerun'),T003=dict(Nezha_records=len(nl),Nezha_exact3minute_files=all(m['matches'] for g in leak['groups'] for m in g['modalities'].values()),Bank_labels=len(records),TRCA_hashmatch=reuse['exact_nezha_matches'],Deep_gold_root_mapping=False),T019=dict(indicator_files=labelaudit['n_files'],unique_hashes=labelaudit['n_unique_file_hashes'],indicators_outside_own_log=detail_label_outside,correction_D1='T002 only four full cards; T019 is full SS census; old T003 referral inaccurate; no old file edited')))

# Complete repeated key checks in current dataset cards: case summary ↔ paired probe rows.
pp='results/T-019/inspection/probe-summary.csv'; prows=rows(pp); pc=rows('results/T-019/inspection/probe-cases.csv')
for i,x in enumerate(prows):
    sub=[z for z in pc if z['dataset']==x['dataset'] and z['group']==x['group'] and z['q']==x['q']]
    for k in ['control_mean','post_mean']:
        ck('T-019',pp,f'row[{i}].{k}',float(x[k]),statistics.mean(float(z[k]) for z in sub),'mean paired per-case rates, same entity scope')
    ck('T-019',pp,f'row[{i}].cases',int(x['cases']),len(sub),'count paired per-case rates')

# Aggregate download costs: components, not result winner, remain a separate column.
pr='results/T-003/runs/resources-final-001/summary.json'; rr=js(pr)
ck('T-003',pr,'download_bytes',rr['download_bytes'],sum(x['download_bytes'] for x in rr['downloads']),'sum independent download manifests')
ck('T-003',pr,'logical_expanded_bytes',rr['logical_expanded_bytes'],sum(rr['logical_expansion'].values()),'sum logical_expansion components')
ck('T-003',pr,'conditional_alllog_bytes',rr['conditional_alllog_bytes'],next(x['download_bytes'] for x in rr['downloads'] if x['dataset']=='DeepTraLog all-log'),'all-log manifest component')
ck('T-003',pr,'logical_expansion.eadro_final_member_occurrences',rr['logical_expansion']['eadro_final_member_occurrences'],sum(rr['eadro_final_member_bytes_by_origin'].values()),'sum member bytes by origin; repeated representations counted')
ck('T-003',pr,'logical_expansion.nezha',rr['logical_expansion']['nezha'],sum(v['bytes'] for v in ne['datasets'].values()),'sum Nezha two-system file-audit bytes')

# Seeded minimum: numeric leaf inventory from original aggregate sources used above; no hashes/timestamps.
# Every role-affecting quantity is checked above regardless of whether sampled.
uniq={}
for x in CHECKS:uniq[(x['task'],x['path'],x['key'])]=x
CHECKS=list(uniq.values())
sample=[]
for task in ['T-002','T-003','T-008','T-009','T-010','T-011','T-012','T-019']:
    pool=sorted([x for x in CHECKS if x['task']==task],key=lambda x:x['sample_sha256'])
    meanings=set(); chosen=[]
    for x in pool:
        meaning=re.sub(r'\[[0-9]+\]','[]',x['meaning'])
        if meaning in meanings:continue
        x['seeded_sample']=True; chosen.append(x);meanings.add(meaning)
        if len(chosen)>=5:break
    assert len(chosen)>=5, (task,len(chosen))
    sample.extend(chosen)
assert all(x['match']=='True' for x in CHECKS), [x for x in CHECKS if x['match']!='True']
for x in DATASETS:
    if not x['sources']:x['sources']='; '.join(re.findall(r'results/[^;]+?(?:\.json|\.csv|\.md)(?::\d+)?',x['C1']+';'+x['C2'])) or 'Xem source/key trong C1–C9'
write_csv('checks.csv',CHECKS)
write_csv('seeded-checks.csv',sample)
write_csv('census-cells.csv',CENSUS)
write_csv('root-mapping.csv',MAPPING)
write_csv('leakage-data.csv',LEAKS)
write_csv('01-bang-tieu-chi-hop-nhat.csv',DATASETS)
write_csv('task-matrix.csv',TASKS)
write_json('supporting.json',dict(seed=SEED,checks=len(CHECKS),datasets=len(DATASETS),criteria=9,rows=DATASETS,tasks=TASKS,limits=['Script hiện hành chỉ aggregate/census/schema sources; toàn luồng có scope-incident.md/json về saved sample payload đọc nhầm','Không locked enumerate/open','Không khuyến nghị/chọn dataset','Nguồn profile-only ghi trích thẻ chưa kiểm lại; còn source-quality OPEN']))
mrp=txt('docs/MRP.md'); criterion=[s for s in mrp.splitlines() if re.match(r'^[1-9]\. ',s)]
criterion=criterion[:9]
md='# Chín tiêu chí hợp nhất — bằng chứng dataset T-020\n\nLuồng bằng chứng, không chọn dataset/vai trò thay Minh. FACT đo trên file là tính lại aggregate/census kết quả gốc; FACT công bố chỉ trong phạm vi source. OPEN không bằng đạt. TX1 không đủ nghĩa hoàn toàn ngoài thiết kế. Chi phí riêng, không tính điểm tổng.\n\n'
md+='Định nghĩa nguyên MRP §4:\n\n'+'\n'.join(criterion)+'\n\n'
md+='Danh sách là hợp MRP/P2 và các thẻ T002/T003/T008–T012/T019; tách Deep raw/graph, Nezha trace+log/metric ngày, LEMMA Original/Preprocessed. Các nguồn hồ sơ đủ nhưng chưa có public immutable release vẫn giữ hàng OPEN. LEMMA OT bỏ theo Q47; không phục hồi thành ứng viên mới. RE1-TT/OB bổ sung census public từ HF tree gốc, không mở telemetry; BARO-FSE-OB là corpus historical TX2. Sự cố đọc nhầm saved schema sample trộn payload ghi rõ trong scope-incident.md/json.\n\n'
md+='| Dataset/release/phần | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | Chi phí |\n|---|---|---|---|---|---|---|---|---|---|---|\n'
for d in DATASETS:md+='| '+' | '.join(str(d[k]).replace('|',' / ').replace('\n',' ') for k in ['dataset',*[f'C{i}' for i in range(1,10)],'cost'])+' |\n'
(OUT/'01-bang-tieu-chi-hop-nhat.md').write_text(md,encoding='utf-8')
tm='# Task chấm được và chế độ b — bằng chứng\n\nInjection không là onset. Nếu chỉ lúc tiêm thì chỉ gọi độ trễ tính từ lúc tiêm. Occurrence time Bank chưa chứng minh là injection/onset. Nhãn anomalous trace Deep không temporal gold hay root gold. Source-selected captures không benchmark continuous blind chỉ nhờ bỏ tên/path. Không có bằng chứng nhãn vùng độc lập để chấm RQ3c public trong đầu vào. RQ3d cần graph thật/đối chứng có control, không tự được nhãn root chứng minh.\n\n'
tm+='| Dataset/phần | Đơn vị | Nhãn thời gian | Ranking | a biết trước | b tự phát hiện | Trace anomaly | Vùng | Mapping/chuyển hệ |\n|---|---|---|---|---|---|---|---|---|\n'
for d in TASKS:tm+='| '+' | '.join(str(d[k]).replace('|',' / ').replace('\n',' ') for k in ['dataset','unit','time_label','ranking','mode_a','mode_b','trace_anomaly','region','mapping'])+' |\n'
tm+='\nNguồn leak đo/tính lại ở leakage-data.csv. Bảng runner/adapter T013–T018 do methods worker kiểm độc lập, root cần gắn vào trước kết luận mode b hợp lệ. Không dòng nào ở đây tự chứng nhận runner đã sạch leak.\n'
(OUT/'03-task-cham-duoc-va-che-do-b.md').write_text(tm,encoding='utf-8')
write_json('input-hashes-used.json',[dict(path=p,bytes=(ROOT/p).stat().st_size,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in sorted(USED)])
print(json.dumps(dict(datasets=len(DATASETS),checks=len(CHECKS),seeded=len(sample),mapping=len(MAPPING),leaks=len(LEAKS),all_match=True),ensure_ascii=False))
