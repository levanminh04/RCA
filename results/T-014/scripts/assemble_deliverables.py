"""Assemble derived tables and notes from already saved task evidence."""
import csv,json,hashlib,collections
from pathlib import Path
out=Path('D:/RCA-flashticket/results/T-014');runs=out/'runs'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
# Input table has exactly the prompt's columns; no additional detector inferred.
with (out/'paper/yeu-cau-dau-vao-draft.csv').open(encoding='utf-8-sig',newline='') as f:
    reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
for r in rows:
    if r['bien_the']=='PC-RHT RCAEval':
        r['tin_hieu_tuy_chon']='không; log/trace không được scorer này dùng'
        r['chi_phi']='ca dev chọn trước273metric: PC1796.269s; RHT0.832s; RSS quan sát~5.2GB; EC2 có instrumentation; không là runtime chính thức toàn dataset'
        r['ghi_chu']+='; adjacency273×273 phải ghép pc_input names bỏ time; wrapper node_names thừa time; helperT014 suffix hữu hạn; normal-PC graph học riêng chua_kiem: ngân sáchQ40 đã dành default/cap/repeat, chưa có lượt normalPC riêng'
    elif 'Kiến trúc-RHT tham chiếu' in r['bien_the']:
        n=load(runs/'example-architecture/interpretation.json')
        r['chi_phi']=f"scoring+ghi snapshot một ca {n['elapsed_diagnostic']:.6f}s; builder30ca có log riêng; laptop dùng chung nên không runtime chính thức"
        r['ghi_chu']+='; schema30devTT unknown0; rawlegacy unknown liệt kê;24call/meta cyclic; graphseed0/1 đổi cạnh24; normalcontrol FAIL60/270≥3; chỉ call trace trước mốc, preprocessing600điểm gồm sau mốc quyết metric membership/forwarding'
    elif 'Kiến trúc-RHT+DA' in r['bien_the']:
        r['chi_phi']='DA trên snapshot kiến trúc272metric đã chạy; overhead riêng chua_kiem: chưa đo cô lập khỏi ghi diagnostic và RHT'
        r['ghi_chu']+='; 272metric/2176phép so độc lập PASS; threshold3 không lọc output code; không thay RHT tham chiếu'
    else:
        r['chi_phi']='PC dùng lại defaultgraph; RHT/DA270metric đã chạy và kiểm2160phép; overhead DA riêng chua_kiem: chưa đo cô lập'
        r['ghi_chu']+='; actualgraph112SCC tổng,6SCC có>1node,largest149; toy vàca thật đổi25/270score DA theo hashseed; không có bảo đảm DAG của bài'
# Distinguish the author's empirical architecture model from the task's common
# linear scorer; give every actually audited regressor/DA combination a row.
reference_arch=next(r for r in rows if 'Kiến trúc-RHT tham chiếu' in r['bien_the'])
empirical=dict(reference_arch)
empirical.update(bien_the='Kiến trúc empirical SVR+RHT+DA; CaseData gốc',vai_tro='RCA prior work; không tái lập toàn Oracle trong T014',
    du_lieu_binh_thuong_toi_thieu='CaseData default interval1min lookup120 detect10:111 điểm train trước mốc; chua_kiem: cấu hình sampling/window thực tế sinh toàn bảngOracle chưa tái lập',
    tham_so_mac_dinh_quan_trong='SVR kernel sigmoid mặc địnhsklearn C1 epsilon.1 gamma scale; RHT tau0 max use_confidenceFalse; DA threshold3; CaseData default interval1min lookup120 detect10 current=mốc+300s',
    chi_phi='chua_kiem: không có lượt architecture SVR+DA interval1min với dữ liệuOracle trongallowlist; runtime paper ở paper/cong-bo-circa.csv không thay phép đo task',
    ghi_chu='Prior work/config gốc models.py580–586,629–634; khác linearRHT1sT014; không coi default CaseData là bằng chứng tái lập giao thức mọi bảng; mapping T014 (chờ WHY, xem de-xuat-tai-lieu-chung.md)')
rows.append(empirical)
reference_pc=next(r for r in rows if r['bien_the']=='PC-RHT RCAEval')
for regression,da in [('linear',False),('SVR_sigmoid',False),('linear',True),('SVR_sigmoid',True)]:
    r=dict(reference_pc)
    r.update(bien_the=f'PC backend R/pcalg audit MEM25; {regression}RHT'+('+DA3' if da else ''),
        vai_tro='kiểm cơ chế/giao thức ô công bố; không chọn baseline từ accuracy',
        can_do_thi='tự học PC bằng causal.R/pcalg, giữ graph node cô lập; graph cached cho factorial scorer',
        tham_so_mac_dinh_quan_trong='R4.4.2 pcalg2.7-12 CI gauss alpha.05 m.maxInf numCores1; '+('SVR sigmoid C1 epsilon.1 gamma scale' if regression!='linear' else 'LinearRegression')+'; tau0 max confidenceFalse interval1s lookup120 detect10 current=mốc+300s'+('; DA threshold3' if da else '; không DA'),
        chi_phi='25PC R-body150.02s (một graph reused); factorial75scorer18.594s aggregate; không runtime cô lập của từng cấu hình; audit/cost-summary.json',
        ghi_chu='Audit trên25MEMfseOB đã được phép và đã từng chạy; không RE2TT mới, không Oracle; cùnggraph/window chỉ đổi scorer/DA; backend+hướng+coverage không cô lập; audit/mem-target-summary.json và mem-prior-config-summary.json; không tự coi graphR là true causal; (chờ WHY, xem de-xuat-tai-lieu-chung.md)')
    rows.append(r)
for r in rows:
    if '(chờ WHY, xem de-xuat-tai-lieu-chung.md)' not in r['ghi_chu']:
        r['ghi_chu']+='; (chờ WHY, xem de-xuat-tai-lieu-chung.md)'
with (out/'yeu-cau-dau-vao.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
# Preserve each purpose and failed attempt; schemas only are documented separately.
with (out/'audit/cases.csv').open(encoding='utf-8-sig',newline='') as f:registry=list(csv.DictReader(f))
extra_registry=out/'audit/architecture-original-cases.csv'
if extra_registry.exists():
    with extra_registry.open(encoding='utf-8-sig',newline='') as f:registry.extend(csv.DictReader(f))
inv=load(runs/'inventory.json');sel=load(runs/'selection-before-scores.json')['selected'];chosen=next(r for r in inv if r['case']==sel)
def add(case,source,method,purpose,reason):registry.append(dict(ca=case,file_nguon=source,phuong_phap=method,muc_dich=purpose,ly_do=reason))
for r in inv:add(r['case'],r['source']+' + '+str(Path(r['source']).with_name('traces.parquet')),'CIRCA kiến trúc builder','schema/call/meta/metric graph census; raw initial + canonicalseed0 + seed1 + nativeYAML; not RCA benchmark','b')
for mode in ['example-architecture','example-architecture-repeat','example-architecture-original-coverage','example-architecture-permuted','normal-normal-architecture','normal-normal-architecture-pretrace','example-pc','example-pc-repeat','example-pc-permuted-score-only','example-pc-hashseed1','normal-normal-pc-cached-fault-graph']:
    if (runs/mode/'snapshot.json').exists():add(sel,chosen['source'],'CIRCA '+mode+' RHT + RHTDA3','P1 mechanism/score verification; '+('fault graph reused, not full normal-PC control' if 'cached-fault' in mode else 'raw arrays/ranks saved before label interpretation'),'a' if ('repeat' in mode or 'permuted' in mode or 'hashseed' in mode) else 'b')
for mode in ['ec2-default-001','ec2-default-002','ec2-default-003']:
    if (runs/mode/'status.json').exists():add(sel,chosen['source'],'CIRCA-PC RCAEval default '+mode,'TT-scale feasibility; status '+str(load(runs/mode/'status.json')['complete'])+'; failures retained','b')
add(sel,chosen['source'],'CIRCA-PC causal-learn depth0 alpha.05 diagnostic','predeclared capped configuration;45min no output; not pc_default','b')
if (runs/'ec2-default-permuted/progress.jsonl').exists():
    add(sel,chosen['source'],'CIRCA-PC default full column permutation','full graph relearning repeat/permutation; status recorded','a')
with (out/'ca-da-chay.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['ca','file_nguon','phuong_phap','muc_dich','ly_do']);w.writeheader();w.writerows(registry)
# Correction sections are factual evidence from the audit; never edit old task.
audit=(out/'audit/bao-cao.md').read_text(encoding='utf-8-sig')
corrections=audit.split('## 4. Vấn đề ở task cũ — để reviewer kiểm',1)[1].split('## 5.',1)[0]
(out/'dinh-chinh-task-cu.md').write_text('# VẤN ĐỀ Ở TASK CŨ — ĐỂ REVIEWER KIỂM\n\nKhông sửa task cũ. Các điểm dưới đã có bằng chứng và triển khai ở T-014; không tự thay số đã phản biện. Phạm vi soi T000–T012 ở audit/coverage-task-cu.csv: census Markdown, đọc sâu các kết luận CIRCA/chấm/fallback liên quan; không claim audit toàn artifact của mọi phương pháp.\n'+corrections+'\n## Làm rõ K1 của T-000\n\nXem paper/dinh-chinh-k1-threshold.md: paper thật có concept loại dưới3; implementation giữ mọi scored metric. Đây là tách phạm vi paper/code, không phủ nhận nguồn câu cũ. Đoạn cũ→mới nguyên văn và kết luận phụ thuộc đã được đưa vào de-xuat-tai-lieu-chung.md.\n',encoding='utf-8')
# Existing snapshots used a legacy diagnostic boolean: legitimate no-parent is
# not an exception fallback. Derive its route without changing numeric evidence.
routes={}
for p in sorted(runs.glob('*/snapshot.json')):
    s=load(p);counts=collections.Counter()
    for name,n in s.get('nodes',{}).items():
        route=n.get('regression_route')
        if route is None:route='no_effective_parents' if len(n['train_x'])==0 else ('value_error_fallback' if n['regression_fallback'] else 'linear_regression')
        counts[route]+=1
    routes[p.parent.name]=dict(counts)
(runs/'regression-route-summary.json').write_text(json.dumps(dict(legacy_field_note='regression_fallback legacy boolean includes legitimate no-parent route; only value_error_fallback is an exception fallback',runs=routes),indent=2))
print(json.dumps(dict(input_rows=len(rows),case_registry_rows=len(registry),snapshot_routes=len(routes))))
