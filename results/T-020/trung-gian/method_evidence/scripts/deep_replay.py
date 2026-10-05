"""Only captured TORAI arithmetic and pinned source inspection; no method run."""
from pathlib import Path
import ast,csv,hashlib,json,math,subprocess,time

R=Path('D:/RCA-flashticket');O=R/'results/T-020/trung-gian/method_evidence';t0=time.monotonic()
def jread(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(name,x):
    p=(O/name).resolve();assert p.is_relative_to(O.resolve());p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def status():return subprocess.check_output(['git','-C',str(R),'status','--short'],text=True)
before=status();save('runs/deep-status-before.json',{'git_status':before})
source=[]
def inspect(path,needle,expected=True,why=''):
    p=Path(path);s=p.read_text(encoding='utf-8');ls=s.splitlines();found=[i for i,x in enumerate(ls,1) if needle in x]
    source.append({'source':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'needle':needle,'lines':found,'passed':bool(found)==expected,'meaning':why})

# Both clones checked by Git HEAD. These are exact source revisions T001 §9.
revisions=[]
for p,rev in [('D:/RCA-ext/src/RCAEval','259ea4167160256a74ad30004aa3d96a998c846e'),('D:/RCA-ext/src/baro','e35f4ec1095e5cac891d52de9ad18a5b32a37ec8'),('D:/RCA-ext/work/T-014/CIRCA','0215e1880096aa02a305c697f1c23cac4600ebd2')]:
    actual=subprocess.check_output(['git','-C',p,'rev-parse','HEAD'],text=True).strip()
    revisions.append({'path':p,'expected':rev,'actual':actual,'match':actual==rev})
    assert actual==rev

prov=jread(R/'src/microrank/PROVENANCE.json')
srcpaths={f['function']:Path(f['source']) for f in prov['functions']}
for f in prov['functions']:
    assert hashlib.sha256(Path(f['source']).read_bytes()).hexdigest()==f['source_sha256']
    original=next(n for n in ast.parse(Path(f['source']).read_text(encoding='utf-8')).body if isinstance(n,ast.FunctionDef) and n.name==f['function'])
    copied=next(n for n in ast.parse((R/'src/microrank/official.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name==f['function'])
    assert ast.dump(original,include_attributes=False)==ast.dump(copied,include_attributes=False)
    source.append({'source':f['source'],'sha256':f['source_sha256'],'needle':'AST '+f['function'],'lines':[f['line'],f['end_line']],'passed':True,'meaning':'verbatim extracted function matches pinned original'})
mrroot=srcpaths['trace_pagerank'].parent
inspect(mrroot/'pagerank.py','d=0.85, alpha=0.01',why='damping and call-edge coefficient defaults')
inspect(mrroot/'pagerank.py','iteration = 25',why='fixed25 rounds, no convergence stop')
inspect(mrroot/'pagerank.py','kind_list[trace_list.index(trace_id)] / kind_sum_trace * 0.5',why='abnormal prior is inverse expression, not additive normalized paper mixture')
inspect(mrroot/'online_rca.py','index < top_max + 6',why='topmax5 gives11operations, not11services')
inspect(mrroot/'preprocess_data.py',"temp[parentId]['duration'] -= temp[spanid]['duration']",why='handling time subtracts direct-child duration, overlap union not computed')

base=Path('D:/RCA-ext/src/RCAEval/RCAEval/e2e')
for needle,why in [('metric = metric.iloc[::15, :]','occurs outer and inner:15*15=225s'),('normal_data = pd.concat([normal_data, normal_logts], axis=1)','aligns by row index'),('random_state=0','GMM fixed randomstate'),('y_pred = estimator.predict(X_train)','hard assignment differs paper soft assignment'),('if len(internal_service_ranks) == len(services_of_this_cluster):','otherwise fallback severity'),('return {"ranks": rc}','RCD inner outputs ranking only')]:
    inspect(base/'torai.py',needle,why=why)
inspect(base/'baro.py','score = max(zscores)',why='BARO DataFrame max signed')
inspect('D:/RCA-ext/src/baro/baro/root_cause_analysis.py','score = abs(max_val - median) / iqr',why='dict score differs max absolute deviation')
cir=Path('D:/RCA-ext/work/T-014/CIRCA/circa')
inspect(cir/'alg/ci/__init__.py','if scores[child].score < self._threshold:',why='DA threshold controls descendant evidence')
inspect(cir/'alg/common.py','return sorted(scores.items(), key=lambda item: item[1].key, reverse=True)',why='ranks all scored nodes, no threshold output filter')

# Independent TORAI replay from raw severity scores in the saved TX2 result.
# The old full script imports chay_torai, which reads telemetry. We do not run it.
# Recompute only algebra that can be checked from serialized intermediates.
replays=[]
for variant in ('goc','sua'):
    path=R/f'results/T-016/runs/s12-tinh-tay-{variant}.json';q=jread(path)['tinh_tay'];detail=q['chi_tiet_diem'];maps={}
    for modality in ('metric','log','trace_lat','trace_err'):
        raw=detail[modality];den=sum(v for _,v in raw);norm=[(c,v/den) for c,v in raw] if raw else []
        d={}
        for c,v in norm:
            service=c.split('_')[0]
            if modality.startswith('trace') and service=='frontendservice':service='frontend'
            if modality=='log':d[service]=max(d.get(service,0),v)
            else:d[service]=d.get(service,0)+v
        if modality=='log' and d:
            den2=sum(d.values());d={s:v/den2 for s,v in d.items()}
        maps[modality]=d
    calculated=[[maps[m].get(s,0.0) for m in ('metric','log','trace_lat','trace_err')] for s in q['service_list']]
    diffs=[abs(a-b) for ra,rb in zip(calculated,q['X_train']) for a,b in zip(ra,rb)]
    means=[sum(v)/4 for v in calculated];clusters={}
    for i,c in enumerate(q['y_pred']):clusters.setdefault(c,[]).append(i)
    cluster_order=sorted(clusters,key=lambda c:sum(means[i] for i in clusters[c])/len(clusters[c]),reverse=True)
    cinfo={v['cum']:v for v in q['cac_cum']};rank=[];fallbacks=[]
    for c in cluster_order:
        indices=clusters[c]
        if len(indices)==1:rank.append(q['service_list'][indices[0]]);continue
        info=cinfo[c];rc=info['rcd_ranks'];sv=list(dict.fromkeys(s.split('_')[0] for s in rc));fallback=len(sv)!=len(indices)
        fallbacks.append({'cluster':c,'calc':fallback,'recorded':info['du_phong']})
        rank.extend([q['service_list'][i] for i in sorted(indices,key=lambda i:means[i],reverse=True)] if fallback else sv)
    expected=q['ranks'];calc=[s+'_A' for s in rank]
    record={'source':str(path),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'variant':variant,'case':'torai-OB/checkoutservice_cpu/1','algebra_entries':len(diffs),'X_max_absolute_error':max(diffs),'X_match':max(diffs)<1e-12,'BIC_argmin':1+min(range(len(q['bic'])),key=q['bic'].__getitem__),'recorded_k':q['n_comp'],'cluster_order':cluster_order,'rank_match':calc==expected,'calculated_ranks':calc,'recorded_ranks':expected,'fallbacks':fallbacks,'no_root_label_used':True,'no_author_or_method_import':True,'not_recomputed':'raw max-z score, Gaussian model fit and CI/PC output; this is replay of normalization, grouping, means, order and fallback'}
    assert record['X_match'] and record['rank_match'] and record['BIC_argmin']==q['n_comp'] and all(x['calc']==x['recorded'] for x in fallbacks)
    replays.append(record)
save('runs/torai-arithmetic-001.json',{'status':'PASS','elapsed_seconds':time.monotonic()-t0,'replays':replays})
save('runs/deep-source-audit.json',{'revisions':revisions,'checks':source,'all_passed':all(x['passed'] for x in source),'paper_MICRO':'results/T-015/sources/microrank-paper.txt (PDF text, page5 Eq7 and page7 weighted spectrum)','paper_TORAI':'https://arxiv.org/html/2604.13522v1 §3.2–3.6','arithmetic_not_full_method':True})
assert all(x['passed'] for x in source)
save('runs/deep-status-after.json',{'git_status':status(),'only_own_writes_by_this_script':True})
(O/'deep-source-audit.md').write_text('''# Kiểm sâu bài/code: MicroRank và TORAI

Khóa chọn theo seed ở LOG T020 trước đọc giá trị: MicroRank T015 (Codex), TORAI T016 (Claude). Không lựa chọn protocol. Revision code/hashes/AST từng hàm và file:dòng thật nằm trong `runs/deep-source-audit.json`.

## MicroRank

Đã đối chiếu toàn phần công thức trong PDF text T015 với nguồn pinned MicroRank, AST bản tách trong src/microrank/official.py giữ nguyên. Code PageRank: d=.85,alpha=.01,25vòng; mỗi phía normalize max. Prior bất thường dùng nghịch đảo biểu thức hỗn hợp, khác công thức7bài là hỗn hợp cộng nghịch đảo chuẩn hóa; prior code không tổng1. Spectrum Dstar2=ef²/(ep+nf), absent branch1e-7 và top_max+6 không đổi. Gốc handling-time trừ tổng con trực tiếp, không union thời gian con song song. Detector alarmµ+1.5σ/>8trace, partitionµ+σ+50ms; REspanµ+3σ là bản khác. Các file gốc pagerank.py:139,172; online_rca.py:53,84,149; preprocess_data.py:177–225. Nguồn paper: `results/T-015/sources/microrank-paper.txt` và profile §2/§5. Bản adapter T015 chưa là đầy đủ gốc nếu thiếu kind/instance/root.

Đã chép script tính độc lập sang T020 và thêm guard inputfixture/outputpath. `runs/microrank-fixture-001/summary.json`:24so sánh đúng, sai số0. Fixture không mở telemetry; không xác nhận mọi graph/partition của dataset chỉ bằng số học.

## TORAI

[Bài TORAI v1](https://arxiv.org/html/2604.13522v1) §3.2–3.6 dùng severity, GMM/BIC, nhân quả trong cụm và FineGrainer. Code RCAEval ghim `259ea41` severity có4nguồn (trace táchlat/error), chuẩn hóa theo tổng, GMM gán cứng. Hàm trong cụm không dùng trace và fallback severity nếu sốservice RCD không đủ. FineGrainer không có. Đây là khác biệt bài/code, không sửa tiếp ở T020.

Code gốc torai.py:29và81stride15hai lần, nên metric bước nhân quả cócadence225s;47–48concatindex. Bản sửa src/torai/torai_sua.py bỏ lần hai và ghép vị trí; parent-root sẽ tự kiểm hai thay đổi. Không đồng nhất bản sửa với toàn TORAI bài. Default GMM fullcov,max_iter50,randomstate0;γ5,bins5,localizedTrue; rcd alpha.01/.001,bước.1 tới<1. Seed RE không khóa. Chốt áp dụng/WHY và P3 thuộc nguồn quyết định hiện hành, luồng này không đổi trạng thái.

`runs/torai-arithmetic-001.json` tính lại normalization/grouping từ raw severity đã lưu,56thành phầnvectơ mỗi bản, mean cụm/order/fallback và finalrank; bản gốc/sửa đều PASS. Script tính tay đầy đủ cũ có import harness đọctelemetry, nên không chạy nguyên. Không tái chạymax-z/GMM/CI; dữ liệu trung gian không đủ để tái tínhmax-z và fitGaussian độc lập chỉ bằngstd lib. Phạm vi số học đã kiểm được ghi tường minh, không gọi là tái chạy toànpipeline.

## Nguồn đính chính V9 đã kiểm trực tiếp

BARO DataFrame: baro/root_cause_analysis.py:313–314 và RCAEval/e2e/baro.py:50–51 `max(zscores)` có dấu. Dict BR:229–230 `abs(max(post)-median)`. Counterexample giảm trong T013 edge-falling-ranks.json cóa_cpu=-2.6,b_cpu=1.0. Không viết mọi bảnBARO làmaxabs.

CIRCA DA: circa/alg/ci/__init__.py:144,150 xử lý evidencecon theoθ; Model ởcirca/alg/common.py:225 xếp toàn scores. Không cutoff3output và không detector cấp hệ thống. Paper§4.3/codedifferent giữ riêng; pending K1 là correction mô tả.

MicroRank self-time/default và TORAI double-stride/fallback có source AST/needle assertions ởJSON, không chỉ sao prose. Không sửa docs chung, taskcũ, src, dataset hay môi trường.
''',encoding='utf-8')
print(json.dumps({'source_checks':len(source),'source_all_passed':all(x['passed'] for x in source),'TORAI_replays':len(replays),'elapsed_seconds':time.monotonic()-t0}))
