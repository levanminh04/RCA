"""T020: evidence only, no telemetry reads, no method run, scoped writes."""
from pathlib import Path
import csv
import hashlib
import json
import math
import statistics

ROOT = Path('D:/RCA-flashticket')
OUT = ROOT / 'results/T-020/trung-gian/method_evidence'
SEED = 20261004

def readj(p):
    p = ROOT / p
    assert p.stat().st_size < 50_000_000, p
    return json.loads(p.read_text(encoding='utf-8-sig'))

def readc(p):
    return list(csv.DictReader((ROOT / p).open(encoding='utf-8-sig', newline='')))

def write(name, content):
    p = (OUT / name).resolve()
    assert p.is_relative_to(OUT.resolve())
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8')

def wc(name, rows, fields=None):
    p = (OUT / name).resolve()
    assert p.is_relative_to(OUT.resolve())
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields or list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def line(path, needle):
    ss = (ROOT / path).read_text(encoding='utf-8-sig').splitlines()
    return next((i for i,s in enumerate(ss,1) if needle in s), 1)

def cit(path, needle=''):
    return f'{path}:{line(path,needle)}' if needle else f'{path}:1'

checks = []
def check(task,path,key,original,recomputed,query,other_source='',tolerance=1e-10):
    match = math.isclose(original,recomputed,abs_tol=tolerance,rel_tol=tolerance) if isinstance(original,(float,int)) else original == recomputed
    h = hashlib.sha256(f'{SEED}|{task}|{path}|{key}'.encode()).hexdigest()
    checks.append(dict(task=task,source=path,key=key,original=original,recomputed=recomputed,match=match,reason=query,component_source=other_source,seed=SEED,selection_hash=h,sampled=False))

headers=[]; merged=[]; header=None
for t in range(13,19):
    p=f'results/T-{t:03}/yeu-cau-dau-vao.csv'
    rs=readc(p); hs=list(rs[0]); header=header or hs
    headers.append(dict(task=f'T-{t:03}',source=p,rows=len(rs),columns=len(hs),header_matches_first=hs==header,original_header=json.dumps(hs,ensure_ascii=False)))
    for i,r in enumerate(rs,2):
        merged.append(dict(source_task=f'T-{t:03}',source=f'{p}:{i}',header_mismatch=hs!=header,chua_kiem_preserved=any('chua_kiem' in str(v) or 'chưa kiểm' in str(v) for v in r.values()),**r))
wc('yeu-cau-hop-nhat.csv',merged)
wc('header-audit.csv',headers)

# T013 corrected R1 source. Recompute ranks to Avg@5 and factorial contrasts.
p13='results/T-013/trung-gian/cua-so-delay-summary.json';j=readj(p13)
c13='results/T-013/runs/sua-R1-20261004-195903/per-case.csv';rs=readc(c13)
a5=lambda rank: max(0,6-int(rank))/5
check('T-013',p13,'cases',j['cases'],len(rs),'count rows',c13)
for variant,col in [('N300-A300','root_rank_N300_A300'),('N360-A300','root_rank_N360_A300'),('N300-A361','root_rank_N300_A361'),('N360-A361','root_rank_N360_A361')]:
    check('T-013',p13,'Avg5_four_variants.'+variant,j['Avg5_four_variants'][variant],statistics.mean(a5(r[col]) for r in rs),'mean max(0,6-root_rank)/5; never copy published Avg5 column',c13)
check('T-013',p13,'changed_ranks',j['changed_ranks'],sum(r['root_rank_N300_A300']!=r['root_rank_N360_A361'] for r in rs),'count changed root ranks',c13)
check('T-013',p13,'down',j['down'],sum(int(r['root_rank_N300_A300'])<int(r['root_rank_N360_A361']) for r in rs),'count rank declines',c13)
check('T-013',p13,'up',j['up'],sum(int(r['root_rank_N300_A300'])>int(r['root_rank_N360_A361']) for r in rs),'count rank improvements',c13)
en=[];ea=[]
for r in rs:
    c0,cn,ca,cna=[a5(r[k]) for k in ('root_rank_N300_A300','root_rank_N360_A300','root_rank_N300_A361','root_rank_N360_A361')]
    en.append(.5*((cn-c0)+(cna-ca)));ea.append(.5*((ca-c0)+(cna-cn)))
check('T-013',p13,'baseline_effect_shapley_average',j['baseline_effect_shapley_average'],statistics.mean(en),'mean .5*((cN-c0)+(cNA-cA)) from four root ranks',c13)
check('T-013',p13,'post_effect_shapley_average',j['post_effect_shapley_average'],statistics.mean(ea),'mean .5*((cA-c0)+(cNA-cN)) from four root ranks',c13)

# T014 graph census independently from per-case graphs; no raw trace opened.
p14='results/T-014/graphs/aggregate.json';j=readj(p14)
graphs=[readj(p.relative_to(ROOT).as_posix()) for p in sorted((ROOT/'results/T-014/graphs').glob('re2tt_*.json'))]
check('T-014',p14,'cases',j['cases'],len(graphs),'count per-case graph JSON','results/T-014/graphs/re2tt_*.json')
for key,field,fn in [('unknown_total','unknown',lambda v:len(v)),('metric_dag_cases','dag',bool),('call_dag_cases','call_dag',bool),('meta_dag_cases','meta_dag',bool)]:
    check('T-014',p14,key,j[key],sum(fn(g[field]) for g in graphs),f'sum {field} from 30 graph records','results/T-014/graphs/re2tt_*.json')
for typ,field in [('metric_edges','metric_edges'),('service_edges','call_edges'),('isolates','isolated')]:
    vals=[len(g[field]) if isinstance(g[field],(list,dict)) else g[field] for g in graphs]
    for op,fn in [('min',min),('max',max)]:
        check('T-014',p14,typ+'_'+op,j[typ+'_'+op],fn(vals),f'{op}(len({field})) across per-case graphs','results/T-014/graphs/re2tt_*.json')

# T015 complete current comparison (failed early attempts are separate).
p15='results/T-015/runs/ob-comparison-check-final.json';j=readj(p15)
c15='results/T-015/so-sanh-tung-ca.csv';rs=readc(c15)
check('T-015',p15,'rows',j['rows'],len(rs),'count per-case CSV',c15)
check('T-015',p15,'statuses.ok',j['statuses']['ok'],sum(r['fixed_status']=='ok' for r in rs),'count fixed_status=ok',c15)
for out,field in [('operation_top11_changed','operation_top11_changed'),('service_top11_changed','service_top11_changed')]:
    check('T-015',p15,out,j[out],sum(r[field]=='True' for r in rs),f'count {field}=True',c15)
check('T-015',p15,'root_rank_top11_changed',j['root_rank_top11_changed'],sum(r['baseline_root_rank_service_top11']!=r['fixed_root_rank_service_top11'] for r in rs),'compare serialized baseline/fixed rank including missing candidate',c15)
check('T-015',p15,'ref_overlap_cases',j['ref_overlap_cases'],sum(int(r['rcaeval_reference_overlap'])>0 for r in rs),'count baseline overlaps >0',c15)
check('T-015',p15,'negative_nf_count_factor_cases',j['negative_nf_count_factor_cases'],sum(any(v<0 for v in json.loads(r['rcaeval_negative_nf_count_factor_operations']).values()) for r in rs),'count any negative unweighted nf factor; this is not weighted spectrum nf',c15)
for r in rs:
    check('T-015',c15,'fixed_all_traces.'+r['ca'],int(r['fixed_all_traces']),int(r['fixed_normal_traces'])+int(r['fixed_anomaly_traces']),'sum disjoint group counts from same CSV',c15)

# T016 independent arithmetic from captured intermediates, not copied prose.
p16='results/T-016/runs/s12-tinh-tay-goc.json';j=readj(p16)['tinh_tay'];x=j['X_train'];svc=j['service_list'];means=[sum(row)/len(row) for row in x]
check('T-016',p16,'n_comp',j['n_comp'],1+min(range(len(j['bic'])),key=j['bic'].__getitem__),'argmin BIC + 1 from complete BIC vector',p16+'#tinh_tay.bic')
for ci,original in j['cum_xep']:
    z=[means[i] for i,c in enumerate(j['y_pred']) if c==ci]
    check('T-016',p16,'cluster_mean.'+str(ci),original,statistics.mean(z),'average X_train row means within captured cluster assignment',p16+'#X_train,y_pred')
for ci in j['cac_cum']:
    if 'rcd_vao' not in ci: continue
    check('T-016',p16,'rcd_input_columns.cluster'+str(ci['cum']),len(ci['rcd_vao']['cot']),len(set(ci['rcd_vao']['cot'])),'count unique passed RCD input columns; detects duplicates',p16+'#cac_cum.rcd_vao.cot')
    check('T-016',p16,'fallback.cluster'+str(ci['cum']),ci['du_phong'],len(ci['noi_bo'])!=len(ci['services']),'compare deduplicated RCD service count to cluster service count',p16+'#cac_cum')
    for name,val in ci['aa']:
        check('T-016',p16,'service_severity.'+name,val,means[svc.index(name)],'mean four X_train source components',p16+'#X_train')

# T017 scores: root labels are only scoring metadata already in results.
p17='results/T-017/runs/fix-n1n2-001/verification.json';j=readj(p17)
c17='results/T-017/diem-dev.csv';rs=readc(c17)
check('T-017',p17,'primary_cases_exactly_match_run004',j['primary_cases_exactly_match_run004'],len(rs),'count complete primary score rows; equality assertion itself not recertified by count',c17)
for k,c in [('hit1_count','hit1_fractional'),('hit3_count','hit3_fractional'),('hit5_count','hit5_fractional')]:
    check('T-017',p17,k,j[k],sum(float(r[c]) for r in rs),'sum per-case tie-aware '+c,c17)
check('T-017',p17,'mrr',j['mrr'],statistics.mean(float(r['mrr_fractional']) for r in rs),'mean per-case reciprocal rank with tie groups',c17)
for i,control in enumerate(j['normal_controls']):
    p=f"results/T-017/runs/run-dev-005/{control['case']}-normal-control.json";q=readj(p);scores=q['scores']
    vals=[v['total'] if isinstance(v,dict) and 'total' in v else v for v in scores.values()]
    if all(isinstance(v,(float,int)) for v in vals):
        check('T-017',p17,f'normal_controls[{i}].positive_services',control['positive_services'],sum(v>0 for v in vals),'count strictly positive service scores in saved normal-control result',p)
        check('T-017',p17,f'normal_controls[{i}].max_score',control['max_score'],max(vals),'max saved service score',p)

# T018 fixed-column and missing-cell census from original CSV records.
p18='results/T-018/cot-re2tt/tom-tat.json';j=readj(p18)
c18='results/T-018/cot-re2tt/ca.csv';rs=readc(c18)
check('T-018',p18,'so_ca',j['so_ca'],len(rs),'count per-case schema census',c18)
for key,col in [('tong_o_thieu','o_thieu'),('tong_o_inf','o_inf'),('ca_co_buoc_time_khac_1s','buoc_time_khac_1s')]:
    check('T-018',p18,key,j[key],sum(int(r[col]) for r in rs),'sum '+col,c18)
cs='results/T-018/cot-re2tt/cot.csv';cols=readc(cs)
check('T-018',p18,'hop',j['hop'],len(cols),'count metric name rows in union census',cs)
check('T-018',p18,'giao_L*',j['giao_L*'],sum(int(r['so_ca'])==len(rs) for r in cols),'count columns present in all30dev cases',cs)
check('T-018',p18,'cot_khong_du_30_ca',j['cot_khong_du_30_ca'],sum(int(r['so_ca'])<len(rs) for r in cols),'count columns absent in at least1dev case',cs)
for i,op in enumerate((min,max)):
    check('T-018',p18,'n_cot_tho_min_max['+str(i)+']',j['n_cot_tho_min_max'][i],op(int(r['n_cot_tho']) for r in rs),'min/max raw column census',c18)

# The seed orders all independently recomputable numerical checks, not winners.
for t in range(13,19):
    pool=sorted([r for r in checks if r['task']==f'T-{t:03}'],key=lambda r:r['selection_hash'])
    seen=set();selected=[]
    for r in pool:
        meaning=r['key'].split('.')[0].split('[')[0]
        if meaning not in seen:
            selected.append(r);seen.add(meaning)
        if len(selected)>=5: break
    if len(selected)<5:
        selected=pool[:5]
    for r in selected:r['sampled']=True
wc('checks.csv',checks)
wc('numeric-sample-candidates.csv',[{k:r[k] for k in ('task','source','key','original','selection_hash','sampled')} for r in checks])

# Existing run ledgers, observations only. Never benchmark an unseen dataset.
runtime=[]
for t in range(13,19):
    p=f'results/T-{t:03}/ca-da-chay.csv';rs=readc(p)
    times=[]
    for r in rs:
        try:
            value=float(r.get('thoi_gian_quan_sat_giay',''))
            if math.isfinite(value): times.append(value)
        except (TypeError,ValueError):
            pass  # Preserve explicit chua_kiem cells as untimed, never zero.
    runtime.append(dict(task=f'T-{t:03}',source=p,execution_rows=len(rs),unique_case_ids=len(set(r['ca'] for r in rs)),timed_rows=len(times),sum_observed_seconds=sum(times) if times else 'chua_kiem',official_dataset_runtime=False,scope='ledger includes repeats/variants/failed runs, cannot extrapolate median as full benchmark',budget_Q40_dataset_seconds=10800,formula='total=sum(cost_per_case*dataset_cases*seeds)+fit/calibration; cap applies total per method per dataset, not per seed',new_dataset_adapter='chua_kiem'))
wc('runtime-ledger.csv',runtime)

windows=[
('BARO/N-Sigma RCA','known-marker L10','T-013',300,300,300,300,1,'none','fit median/IQR or mean/std on all pre points','max signed post score',cit('results/T-013/ho-so-baro.md','## 4.')),
('BARO RCA','FSE-OB delay L20 actually clipped','T-013',360,361,360,361,1,'none','not600+600: recording bounds','actual360+361=721points; end inclusive in source',c13),
('BOCPD','BR wrapper full/prefix','T-013','variable','variable','T','T','requires timestamp mapping','posterior runlength','minmax full input leaks future; prefix needed','cps are row indices; end sentinel T invalid',cit('results/T-013/ho-so-bocpd.md','## 4.')),
('N-Sigma detector','BR startsfrom100','T-013','>=100','online','100','online',1,'past expanding','sample std ddof1, starts index100','history contaminated after alarms; calibration unresolved',cit('results/T-013/ho-so-nsigma-phat-hien.md','## 4.')),
('CIRCA','RE PC/T014 architecture reference','T-014',111,10,111,10,1,'lookup120 detect10','train t-120..t-10 inclusive; resampled111points','test t+291..t+300; most input unused by RHT; PC sees full table',cit('results/T-014/ho-so-circa-pc.md','Bước 4')),
('CIRCA','author CaseData default','T-014',6660,600,111,10,60,'lookup120 detect10','train covers110*60=6600s between first/last samples; nominal111min','test t-4min..t+5min for current=t+300; can straddle incident',cit('results/T-014/ho-so-circa-kien-truc.md','Với default gốc')),
('MicroRank','author alarm query','T-015','history suggested1hour',60,'operation-dependent','trace count', 'event driven','query60sec','mu/std handling time baseline','code60s alarm query then RCA[-5,+55]sec; paper30s',cit('results/T-015/ho-so-microrank.md','Cửa sổ detector code')),
('MicroRank/TraceRCA span','RE fixed L20','T-015',600,600,'>=2span/operation','event-count','event driven','none','reference spans ending before marker','graph/count post traces same disjoint partition; sample counts vary',cit('results/T-015/ho-so-microrank.md','Trong T-015')),
('TORAI','RE original L10 severity','T-016',300,300,20,20,15,'none','metric input300+300points1s then stride15; logts20+20points15s','causal metric stride15 twice =>225s; some halves1-2points',cit('results/T-016/ho-so-torai.md','Bước 0')),
('TORAI','RE corrected L10','T-016',300,300,20,20,15,'none','single metric stride15; align N/A by position','same reference and incident300sec; not20sec',cit('results/T-016/ho-so-torai.md','Bước 3')),
('TORAI','RE L20','T-016',600,600,40,40,15,'none','inputmetric600+600 at1s; log40+40 at15s','P3 window still unresolved Q54',cit('results/T-016/ho-so-torai.md','Cửa sổ `--length`')),
('RCD','RE L10','T-016',300,300,300,300,1,'none','normal/abnormal F-node; discretizer fit joined segments','num rows>num variables at phase2',cit('results/T-016/ho-so-torai.md','Ràng buộc')),
('SimpleRCA M4','primary T017','T-017',300,300,300,300,1,'none','metric>=2finite; trace>=1span per service/window','event alert count changes with time/sampling/channel count',cit('results/T-017/ho-so-simplerca.md','## 4.')),
('GDN','run.sh default','T-018','normal training','online',5,1,1,'model5ticks smoothing4ticks','fixed columns317 or T005333; val_ratio0.2','train1/5/10cases=720/3600/7200points1s=12/60/120min nominal',cit('results/T-018/ho-so-gdn.md','## 4.')),
]
wr=[dict(method=a,variant=b,task=c,pre_seconds=d,post_seconds=e,pre_points=f,post_points=g,cadence_seconds=h,lookback=i,fit=j,trigger_and_limits=k,source=l,state='FACT prior task; P3 common rule OPEN') for a,b,c,d,e,f,g,h,i,j,k,l in windows]
wc('window-parameters.csv',wr)

labels=[
('BARO/N-Sigma RCA','no root/fault fit','normal/fault split needs external marker; injection allowed only mode a','dev tuning not done T020','test only score; no root SLI','BOCPD/nsigma may supply trigger after leakage fixes','T-013'),
('CIRCA PC','no root labels; PC fit includes current incident data','normal boundary used by RHT; PC not normal-only','graph/scorer choices unresolved; no selection from observed accuracy','root/case/path only scorer after serialized rank','no built-in incident detector; static topology cannot derive from labels','T-014'),
('CIRCA architecture','no root labels; graph from reference trace or documented architecture','normal reference/mapping must be independent root','T/S/L/E mapping source schema; changing membership from post data mode b issue','test no root-based graph/columns','scorer uses outside incident marker','T-014'),
('MicroRank/TraceRCA','operation/service labels structural; root never fit','normal trace for per-operation mu/std; goc suggests1h, no guarantee','no parameter choice from known root rank','ranking candidate absence retained in denominator','span3sigma local detector not calibrated streaming event detector; no root-kind in RE2-TT','T-015'),
('TORAI/RCD','no root/fault learning; F=normal/abnormal regime','injection/t_det used to create F; unseen mode b need trigger','seed per case; TORAI>=3; RCD>=1 within Q40 pending G1','no true root / SLI input; label only eval','no TORAI internal detector; Figshare trace-lat threshold has future whole-file data','T-016'),
('SimpleRCA','no root/fault labels fit','normal historical window / current split from marker','T017 conventions recorded; P3 not selected','root/fault/Type labels only score; aliases no root inference','rules produce alerts not calibrated incident detector','T-017'),
('GDN','no anomaly label required for regression; labelnormal needed','dev injection used to select pre-injection training720pts/case; budget1/5/10cases','validation checkpoint; threshold val only; fixed column inventory across dev','reportbest uses test labels forbidden; reportval still future median/IQR','fixed-val normalization variant measured45–100%normal tick alarms; not ready as valid b','T-018'),
]
wc('label-budget.csv',[dict(method=a,fit_labels=b,normal_budget=c,dev_labels=d,test_labels=e,mode_b_status=f,source_task=g,state='FACT existing evidence; protocol G1 OPEN') for a,b,c,d,e,f,g in labels])

leaks=[
('T-013','BARO RCA','split marker and injection crop','ranker receives marker; no built-in detector','mode_a_only',cit('results/T-013/ho-so-baro.md','Mốc tiêm và cắt')),
('T-013','BOCPD','full-input minmax / finite file boundary','future normalization plus injection-centered crop','mode_b_not_valid_as_run',cit('results/T-013/ho-so-bocpd.md','## 8.')),
('T-013','N-Sigma detector','runner injection crop; timestamp/index errors','detector raw expanding past; adapter may normalize whole file','mode_b_runner_fix_needed',cit('results/T-013/ho-so-nsigma-phat-hien.md','## 8.')),
('T-014','CIRCA PC/architecture','marker; PC all data; metric membership derived after marker','RHT is conditional score only; threshold3 is DA child-evidence, not output cutoff','mode_a_only_without_external_trigger',cit('results/T-014/ho-so-circa-pc.md','## 8.')),
('T-015','MicroRank/TraceRCA RE','marker crops; reference/candidate membership; lack kind','fixed-span builds disjoint groups but is not whole author detector','local_trace_partition_only',cit('results/T-015/ho-so-phat-hien-trace.md','## 8.')),
('T-016','TORAI/RCD','marker; full-file tracets_lat mu+3sigma threshold','root-derived sli not read by functions; no internal detector','mode_a_only_as_run',cit('results/T-016/ho-so-torai.md','## 8.')),
('T-017','SimpleRCA','injection split; identity names; root-based aliases risk','source identity manifest guard and no root/path accepted in core','known_marker_rules_only',cit('results/T-017/ho-so-simplerca.md','## 8.')),
('T-018','GDN','reportbest testlabels; reportval future normalization; file-centered injection','fixed-val normalization / dev fixed columns remove some paths, calibration still fails','mode_b_unready',cit('results/T-018/ho-so-gdn.md','## 8.')),
]
wc('runner-leakage.csv',[dict(task=a,method=b,path=c,factual_audit=d,status=e,source=f) for a,b,c,d,e,f in leaks])

summaries={
'BARO':('Học trung vị và IQR của từng metric trên đoạn bình thường. Bản DataFrame xếp bằng max độ lệch có dấu ở hậu sự cố; giảm mạnh có thể thành điểm âm. Bài viết trị tuyệt đối. Nhánh dict lại lấy abs(max(post)-median), quartile theo chỉ số, nên cũng không đồng nhất. Không dùng đồ thị. N-Sigma RCA thay robust scale bằng mean/std dân số; detector N-Sigma là thuật toán khác. Cần mốc ngoài. Hai cửa sổ bình thường và lỗi quyết định tập cột sau bỏ hằng. Các ca T013 là kiểm cơ chế/tái lập, không chọn cửa sổ P3.','results/T-013/ho-so-baro.md'),
'BOCPD':('Bộ phát hiện điểm đổi giữ phân phối runlength và dùng mô hình Student-t đa biến với hazard1/50, kappa1, nu=d+1. Wrapper tìm điểm đổi từ bước nhảy mode runlength. Đầu ra là chỉ số hàng, không timestamp. Code minmax toàn đầu vào nên nhìn tương lai; cắt quanh injection không hợp tự phát hiện. Ma trận T×T làm chi phí tăng theo bình phương chiều dài, còn phép toán covariance phụ thuộc số cột. Chưa có bảo đảm lượng bình thường tối thiểu hoặc calibration chung.','results/T-013/ho-so-bocpd.md'),
'N-Sigma':('RCA: StandardScaler ddof0 trên nền, lấy max có dấu ở hậu và gộp metric về service. Detector BR: bắt đầu từ index100, nền expanding quá khứ, std mẫu ddof1 và so abs deviation>3std; trả timestamps theo cột có thể trùng và chưa sắp. Đây là hai vai trò riêng. Đã kiểm phép tính hai ca và các edge cases, chưa chứng minh false alarms trên regime bình thường độc lập.','results/T-013/ho-so-nsigma-phat-hien.md'),
'CIRCA':('PC học quan hệ metric từ chính bảng ca; kiến trúc dựng quan hệ T/S/L/E từ call graph normal hoặc cấu hình. RHT dự báo metric bằng các cha rồi chuẩn hóa phần dư và lấy max trị tuyệt đối. DA truyền evidence từ con; threshold3 không cắt output ranking. T014 tham chiếu linear RHT interval1s khác bản empirical SVR sigmoid+DA và CaseData default1min. PC có SCC/cạnh hai chiều và lỗi wrapper có thể trả thứ tự cột. Mỗi nguồn graph/scorer/mapping là một biến thể riêng, không cô lập nguồn graph chỉ bằng so hai bảng điểm. Cần mốc ngoài, không detector sự cố.','results/T-014/ho-so-circa-pc.md'),
'MicroRank':('Chia trace thành hai nhóm, dựng call graph operation và quan hệ trace-operation. PageRank đồng bộ hai vector25vòng với d=.85 alpha=.01, chuẩn hóa theo max từng phía; trọng số operation nhân mean của vector. Trọng số đi vào bốn ô spectrum và Dstar2=ef²/(ep+nf). Code gốc khác công thức prior cộng của bài, khác định nghĩa trace kind và detector/partition. RCAEval dùng span μ+3σ, có nhóm chồng và đặt lại cạnh; bản T015 sửa đầu vào giữ PageRank/spectrum. Gốc dùng handling-time trừ tổng con, chưa xử lý hợp khoảng con song song. Thiếu service trong trace thì không tự thêm root. Các fixture và ca đã chạy có số học độc lập.','results/T-015/ho-so-microrank.md'),
'TraceRCA':('Bản gốc dùng reference latency/status của lời gọi và kết hợp support/confidence qua trace; bản RCAEval không tương đương cả pipeline. RE lấy operation anomalous theo μ+3σ rồi tính support/confidence, không PageRank. Khác MicroRank thêm vai trò detector và độ dài đầu ra nên không quy chênh lệch riêng cho graph. Cần reference cho từng operation hiện tại; thiếu/NaN không được thay bằng thứ tự cột.','results/T-015/tracerca-rcaeval.md'),
'Detector trace':('Span μ+3σ của RE dùng inclusive duration, std mẫu và tối thiểu2span nền/operation. Luật MicroRank gốc học μ/std handling-time, alarm so root latency với tổng count(μ+1.5σ), báo khi>8trace; partition RCA lại μ+σ+50ms. Gốc code query60s nhưng bài30s. Thiếu root kind, instance và xử lý span cắt biên không cho phép tuyên bố đã cài đủ detector gốc.','results/T-015/ho-so-phat-hien-trace.md'),
'TORAI':('Code tính max|z| của metric/log/trace, chuẩn hóa theo tổng từng nguồn, gom service thành vector4chiều. GMM thử k1..n chọn BIC, gán cứng và xếp cụm bằng mean severity. RCD trong cụm thêm F=normal/fault và dùng kiểm CI để xếp biến, nhưng fallback severity khi không xếp đủ service. Gốc metric stride15 hai lần; bản sửa bỏ lần hai và ghép theo vị trí. Code thiếu FineGrainer, không đưa trace vào RCD và khác gán mềm bài. TORAI không tự phát hiện; nhãn root không fit nhưng regime boundary bắt buộc. Seed theo ca, chưa chốt windowP3.','results/T-016/ho-so-torai.md'),
'RCD':('Ghép normal/fault và F-node, rời rạc hóa kmeans tối đa5bin, Ψ-PC chỉ kiểm cạnh kềF bằng chi-square. Pha1 hoán vị và nhóm5biến với alpha.01; pha2 alpha.001 tăng.1 tới<1. Xếp p-value theo list Python khác max(P) trong bài. RE không đặt seed; gốc420. RCD đối chứng metric không gom cụm/không giảm mẫu nên khác TORAI nhiều bước. Đòi causal sufficiency/faithfulness và đủ mẫu; output có thể thiếu biến và root, denominator phải giữ.','results/T-016/ho-so-torai.md'),
'SimpleRCA (M4 theo mô tả bài)':('Bản độc lập theo mô tả, không code tác giả. Metric mỗi point>mean+3std0 là một alert; trace mỗi service một phiếu nếu P95incident>3P95normal; log substringERROR/FAIL/EXCEPTION một count/dòng và phiếu nếu count>0. Cộng phiếu về service, giữ tie groups và zero-score abstain. Events/channels, P95, trace factor2/4, log thresholds và half600 là các quy ước/biến thể riêng; không chọn bằng accuracy. Giữ observed-service union kể cả normal-only log score0. Rules này chưa là detector streaming đã calibration. TypeI/II của bài là luật phân loại riêng, không accuracy SimpleRCA.','results/T-017/ho-so-simplerca.md'),
'GDN (d-ailin/GDN@9853899)':('Detector dự báo metric từ cửa sổ5tick và top-k neighbors học bằng embedding, rồi chuẩn hóa residual theo median/IQR và smoothing4tick; anomaly hệ thống=max metric score. Không xếp root. Default reportbest chọn threshold theo nhãn test; reportval bỏ đường đó nhưng score vẫn dùng thống kê test tương lai. T018 cố định317cột dev và dùng thống kê validation; normal held-aside trong dev vẫn báo45–100%tick. Học normal dùng injection của dev để lấy720point/ca;1/5/10ca là12/60/120phút1s, không bảo đảm đủ. Window5ticks không nghĩa5giá trị độc lập vì cột lặp.','results/T-018/ho-so-gdn.md'),
}
checklist=[]
for r in merged:
    name=r['phuong_phap'];entry=next((v for k,v in summaries.items() if name==k or name.startswith(k)),None)
    if entry:
        profile=entry[1]
        checklist.append(dict(method=name,variant=r['bien_the'],role=r['vai_tro'],requirements=r['source'],mechanism_source=cit(profile,'## 2.'),defaults_source=cit(profile,'## 4.'),paper_code_source=cit(profile,'## 5.'),assumptions_source=cit(profile,'## 6.'),worked_example_source=cit(profile,'## 7.'),run_registry=f"results/{r['source_task']}/ca-da-chay.csv:1",limitations=r['ghi_chu'],state='FACT hồ sơ có; không duyệt protocol'))
    else:
        checklist.append(dict(method=name,variant=r['bien_the'],role=r['vai_tro'],requirements=r['source'],mechanism_source=cit('results/T-018/decomprca.md'),defaults_source=cit('results/T-018/decomprca.md'),paper_code_source=cit('results/T-018/decomprca.md'),assumptions_source=cit('results/T-018/decomprca.md'),worked_example_source='không chạy theo SPEC T018',run_registry='không áp dụng; bài đọc bổ sung, không danh sách P1',limitations=r['ghi_chu'],state='FACT đọc; không là baseline được chọn'))
wc('method-checklist.csv',checklist)
md=['# V8 — Checklist và đọc nhanh phương pháp','',f'EXECUTE evidence-only. Hợp sáu bảng: {len(merged)} hàng; header audit riêng. Không chọn phương pháp, dataset hay protocol. Danh sách đã chốt là T001 §8 theo Q37/Q38; SPOT không dùng, GDN chỉ detector. T013 dùng bản sau R1/N1–3.','', 'Checklist đầy đủ từng variant/detector: `method-checklist.csv`; nguồn cơ chế, defaults, paper/code, giả định, tính tay và ledger đều giữ riêng.','']
for name,(body,profile) in summaries.items():
    md += ['## '+name,'',body,'',f'Nguồn ghim/hồ sơ: `{profile}`; yêu cầu giữ nguyên trong `yeu-cau-hop-nhat.csv`. Mỗi đoạn dưới350từ.','']
md+=['## Kiểm sâu khóa bằng seed trước đọc','', 'MicroRank T015 và TORAI T016 đã khóa ở LOG T020. `deep-source-audit.md` ghi đối chiếu nguồn gốc; `runs/` giữ phép tính lại. MicroRank replay fixture không mở telemetry. TORAI kiểm arithmetic từ kết quả đã chạy, không gọi pipeline/CI mới; giới hạn không tái chạy toàn Psi-PC.','']
md+=['## Từng biến thể và từng bộ phát hiện','', 'Mỗi đoạn sau giữ đúng biến thể của bảng nguồn. Các quy ước chưa kiểm nằm nguyên văn trong CSV; đoạn đọc nhanh không thay hồ sơ đầy đủ.','']
for r in merged:
    name=r['phuong_phap'];family=next((k for k in summaries if name==k or name.startswith(k)),None)
    graph_role={'CIRCA':'graph cung cấp cha cho hồi quy RHT; DA dùng evidence con; PC là graph học từ metric, architecture là graph từ mapping/call relations',
                'MicroRank':'call/coverage graph lan truyền PageRank rồi weighted spectrum; không phải detector graph/subgraph',
                'TraceRCA':'support/confidence theo coverage, không PageRank; invocation relations của gốc khác RE',
                'TORAI':'không call graph; khung nhân quả cục bộ quanh F trong cụm, chỉ khi không fallback',
                'RCD':'khung nhân quả cục bộ quanh F-node dùng CI; không call graph',
                'GDN (d-ailin/GDN@9853899)':'graph tương quan học từ embedding cung cấp neighbor features cho dự báo; không root ranking'}.get(family,'không graph hoặc không áp dụng trong rule thống kê này')
    para=f"Đầu vào: {r['tin_hieu_bat_buoc']}. Đơn vị: {r['don_vi_xep_hang']}. Vai trò đồ thị: {graph_role}; yêu cầu graph: {r['can_do_thi']}. Mốc: {r['can_moc_su_co']}. Nền tối thiểu: {r['du_lieu_binh_thuong_toi_thieu']}. Defaults: {r['tham_so_mac_dinh_quan_trong']}. Adapter dataset mới: chua_kiem. Nguồn: {r['source']} và method-checklist.csv."
    assert len(para.split())<=350,(name,r['bien_the'],len(para.split()))
    md+=['### '+name+' — '+r['bien_the'],'',para,'']
write('07-checklist-doc-nhanh.md','\n'.join(md))

counts={t:len([c for c in checks if c['task']==f'T-{t:03}']) for t in range(13,19)}
failed=[r for r in checks if not r['match']]
write('05-evidence.md',f'''# V6 — Nhãn, cửa sổ và mode b: bằng chứng

T020 không chốt protocol. `window-parameters.csv` giữ giây, điểm, cadence, pre/post, lookback và trigger riêng. `label-budget.csv` tách fit-normal/regime, tune-dev và score-test. `runner-leakage.csv` là audit hồ sơ từng adapter, không tuyên bố b đã hợp lệ chỉ từ chữ ký hàm.

T013 L20 trên ôdelay FSE-OB hiện chỉ có360trước+361sau do giới hạn recording, khác ý định600+600. T014111điểm1s khác111điểm1min;10testpoints tại+291..+300khác+(-4)..+5phút của default. TORAI L10=300s mỗi phía;20logts points15s. GDN model5tick ở1s không bảo đảm5giá trị độc lập. Giữ đủ bình thường thống kê là OPEN, không dùng minimum để gọi calibrated.

`checks.csv` có phép tính từ CSV hoặc thành phần JSON gốc: {counts}. Số chọn bằng SHA256 seed20261004 trong pool đại lượng tính lại, mọi aggregate trọng yếu trong pool đều kiểm; không chọn theo kết quả. `numeric-sample-candidates.csv` chứa toàn pool kiểm lại của luồng này; nó không thay inventory tất cả lá số đầu vào của root. Số mismatch hiện: {len(failed)}. Mismatch giữ nguyên và lý do trong bảng, không sửa task cũ.

Giới hạn runtime: `runtime.csv` đếm execution ledger, không coi tất cả ca/lần chạy là benchmark một dataset. Q40 áp total dataset×seed, không10800s mỗi seed. Nếu runtime một seed gần ngân sách thì số seed khả thi cần tính bằng total, không nhân ngân sách theo seed. Dataset mới: adapter và runtime `chua_kiem`; không chạy mới T020.

Nhãn gốc/fault không được fit. Regime normal/fault dùng mốc nhãn ởmodea; GDN lấy normal của dev bằng mốc tiêm cũng là labelbudget thật. Chế độb phải xử lý marker,crop,future-normalization và candidate selection trước đo. Testlabels không chọn threshold/checkpoint; root/path/SLI không truyền vào phương pháp. Đồ thị PC học incident data trongmodea không tự là ròroot nhưng khác normal-only topology. Biên file-centered injection vẫn là đường lộ trongmodeb.
''')
write('runs/build-summary.json',json.dumps(dict(requirement_rows=len(merged),header_mismatches=sum(not r['header_matches_first'] for r in headers),checks=len(checks),failed=failed,per_task=counts,no_raw_telemetry=True,no_method_run=True,write_root=str(OUT)),ensure_ascii=False,indent=2))
print(json.dumps(dict(requirement_rows=len(merged),check_rows=len(checks),per_task=counts,failed=len(failed)),ensure_ascii=False))
