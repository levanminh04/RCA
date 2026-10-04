"""Read and verify every owned output and neutral reviewer prompt."""
import json,csv,ast,subprocess,hashlib,sys,re,math
from collections import defaultdict
from pathlib import Path
ROOT=Path('D:/RCA-flashticket');OUT=ROOT/'results/T-013';TASK=ROOT/'tasks/T-013-ho-so-baro'
FIX=OUT/'runs/sua-N1-20261004-195501'
def no_constant(v):raise ValueError('Nonstandard JSON constant '+v)
files=sorted(OUT.rglob('*')); files=[p for p in files if p.is_file()]
issues=[];parse_counts={'json':0,'csv':0,'python':0,'npz':0,'markdown':0};verified=[]
required=['ho-so-baro.md','ho-so-bocpd.md','ho-so-nsigma-phat-hien.md','vi-du-tinh-tay.md','cua-so-va-che-do-b.md','yeu-cau-dau-vao.csv','ca-da-chay.csv','dinh-chinh-task-cu.md','de-xuat-tai-lieu-chung.md','moi-truong.md','manifest.json','kiem-tra.json','doi-chieu-moc.json','doi-chieu-tieu-chi.md']
assert all((OUT/p).is_file() for p in required)
for p in files:
    suffix=p.suffix
    if suffix=='.json':
        try:json.loads(p.read_text(encoding='utf-8-sig'),parse_constant=no_constant)
        except Exception as e:issues.append({'file':str(p),'error':str(e)})
        parse_counts['json']+=1
    elif suffix=='.csv':
        with p.open(encoding='utf-8-sig',newline='') as f:
            rows=list(csv.reader(f)); assert rows and all(len(r)==len(rows[0]) for r in rows)
        parse_counts['csv']+=1
        if p.name.endswith('-metric.csv') and 'official_score' in rows[0]:
            import math
            h=rows[0];si=h.index('score');oi=h.index('official_score')
            for r in rows[1:]:
                if r[si] and r[oi]:assert abs(float(r[si])-float(r[oi]))<=1e-10*max(1,abs(float(r[oi])))
    elif suffix=='.py':ast.parse(p.read_text(encoding='utf-8-sig'));parse_counts['python']+=1
    elif suffix=='.npz':
        import numpy as np
        with np.load(p,allow_pickle=False) as x:
            if 'independent' in x:assert np.max(np.abs(x['independent']-x['official']))<=1e-10
        parse_counts['npz']+=1
    elif suffix=='.md':
        t=p.read_text(encoding='utf-8-sig');parse_counts['markdown']+=1
        if p.name.startswith('ho-so-'):assert all(re.search(r'^## '+str(i)+r'\.',t,re.M) for i in range(1,10))
    verified.append(str(p.relative_to(ROOT)).replace('\\','/'))
# Old failed partial JSON can contain NaN: retain originals, document their status.
assert not issues,issues
with (OUT/'yeu-cau-dau-vao.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.reader(f))
header='phuong_phap,bien_the,vai_tro,tin_hieu_bat_buoc,tin_hieu_tuy_chon,dinh_dang_va_ten_cot_can,can_do_thi,can_moc_su_co,du_lieu_binh_thuong_toi_thieu,can_nhan_de_hoc,don_vi_xep_hang,tham_so_mac_dinh_quan_trong,phu_thuoc_do_dai_cua_so,chi_phi,duong_nhan_rui_ro,ghi_chu'.split(',')
assert rows[0]==header and len(rows)==7
s=json.loads((OUT/'kiem-tra.json').read_text(encoding='utf-8'));assert s['status']=='complete'
selected={r['case'] for r in s['selection']['selected']}
with (OUT/'ca-da-chay.csv').open(encoding='utf-8-sig',newline='') as f:ledger=list(csv.DictReader(f))
with (OUT/'trung-gian/cua-so-delay-variants.csv').open(encoding='utf-8-sig',newline='') as f:variants=list(csv.DictReader(f))
assert len(variants)==100 and len({r['case'] for r in variants})==25
delay_cases={'fse-ob/'+r['case'].rsplit('_',1)[0]+'/'+r['case'].rsplit('_',1)[1] for r in variants}
assert all(r['ca'] in selected|delay_cases|{'synthetic'} and r['ly_do'] in {'a','b','c'} for r in ledger)
for r in ledger:
    if r['ca'] in delay_cases:
        assert r['phuong_phap']=='N-Sigma independent window algebra'
        assert Path(r['file_nguon'])==Path('D:/RCA-ext/data')/r['ca']/'simple_data.csv'
focused=json.loads((FIX/'ket-qua.json').read_text(encoding='utf-8'))
assert focused['status']=='pass' and len(focused['checks'])==19
assert focused['real_metric_points_checked']==1316
assert all(c['status']=='pass' for c in focused['checks'])
window=json.loads((OUT/'trung-gian/cua-so-delay-summary.json').read_text(encoding='utf-8'))
assert window['cases']==25 and window['all_endpoint_metric_ranks_exact'] and window['all_endpoint_service_ranks_exact']
assert window['all_repeat_permutation_checks_pass']
assert abs(window['baseline_effect_shapley_average']+window['post_effect_shapley_average']+.256)<1e-10
assert len(window['candidate_change_cases'])==4
R1=Path(window['run_dir'])
for manifest_path,groups in [(R1/'manifest.json',['sources','output_files']),(FIX/'manifest.json',['tested_sources','test_outputs'])]:
    metadata=json.loads(manifest_path.read_text(encoding='utf-8'))
    for group in groups:
        for entry in metadata[group]:
            assert hashlib.sha256(Path(entry['path']).read_bytes()).hexdigest()==entry['sha256'],entry['path']
with (R1/'per-metric.csv').open(encoding='utf-8-sig',newline='') as f:metric_rows=list(csv.DictReader(f))
groups=defaultdict(list)
for row in metric_rows:
    if row['candidate']=='False':
        assert not row['score'] and (row['normal_constant']=='True' or row['post_constant']=='True')
        continue
    mean,scale,maximum,score=(float(row[k]) for k in ['mean','scale_effective','max_post','score'])
    assert abs((maximum-mean)/scale-score)<=1e-10*max(1.,abs(score))
    var=float(row['variance_ddof0_corrected']);bound=float(row['constant_bound'])
    assert (row['near_constant']=='True')==(var<=bound)
    assert scale==(1. if var<=bound else math.sqrt(var))
    groups[row['case'],row['variant']].append(row)
rankings=json.loads((R1/'rankings.json').read_text(encoding='utf-8'))
assert len(groups)==100
for (case,variant),rows_by_metric in groups.items():
    ranks=[r['metric'] for r in sorted(rows_by_metric,key=lambda r:float(r['score']),reverse=True)]
    assert ranks==rankings[case][variant]['metric_ranks']
    services=list(dict.fromkeys(r.split('_')[0].replace('-db','') for r in ranks))
    assert services==rankings[case][variant]['service_ranks']
    if variant in {'N300-A300','N360-A361'}:
        folder='l4-nsigma-fse-ob-len10-lan1' if variant=='N300-A300' else 'l4-nsigma-fse-ob-lan1'
        saved=Path('D:/RCA-ext/work/T-006')/folder/'output/results'/(case+'.json')
        assert ranks==json.loads(saved.read_text(encoding='utf-8'))['0']
with (R1/'per-case.csv').open(encoding='utf-8-sig',newline='') as f:case_rows=list(csv.DictReader(f))
assert len(case_rows)==25
assert abs(sum(float(r['delta_Avg5_L20_minus_L10']) for r in case_rows)/25+.256)<1e-10
for r in case_rows:
    assert abs(float(r['baseline_effect_shapley'])+float(r['post_effect_shapley'])-float(r['delta_Avg5_L20_minus_L10']))<1e-10
old=json.loads((OUT/'trung-gian/cua-so-cu.json').read_text(encoding='utf-8'));assert abs(old['difference']-.256)<1e-10
sources={}
for name,expected in [('baro','e35f4ec'),('RCAEval','259ea41')]:
    d=Path('D:/RCA-ext/src')/name
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=d,text=True).strip()
    status=subprocess.check_output(['git','status','--short'],cwd=d,text=True).strip();assert head.startswith(expected) and not status
    sources[name]={'head':head,'status':status}
# Validate neutral prompt only after it has been appended.
log=(TASK/'LOG.md').read_text(encoding='utf-8');review=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8')
if '## Prompt phản biện cho Claude' in log:
    common=review.split('## Prompt chung',1)[1].split('```text\n',1)[1].split('```',1)[0]
    g1=review.split('**G1 — phương pháp, dataset, cách chia:**',1)[1].split('```text\n',1)[1].split('```',1)[0]
    actual=log.split('## Prompt phản biện cho Claude',1)[1]
    assert g1 in actual
    inventory=json.loads((OUT/'danh-sach-file.json').read_text(encoding='utf-8'))
    assert set(inventory['result_outputs'])==set(verified)
    # The review prompt is a frozen historical artifact. Verify it against the
    # inventory at that handoff, then verify the correction supplement below.
    historical_inventory=json.loads((FIX/'truoc-danh-sach-file.json').read_text(encoding='utf-8'))
    all_paths=historical_inventory['task_outputs']+historical_inventory['result_outputs']+historical_inventory['external_outputs']
    file_list='\n'+'\n'.join('- '+p for p in all_paths)
    expected=common.replace('<T-xxx>','T-013').replace('<T-xxx-tên>','T-013-ho-so-baro')
    expected=expected.replace('<danh sách>',file_list).replace('<commit gốc>','93f13d4c4a966428177e2acc287d96bc89303e92')
    assert expected.rstrip() in actual
    assert all(v in actual for v in verified),[v for v in verified if v not in actual]
    assert 'D:/RCA-ext/work/T-013/metrics-selected.npz' in actual
    assert 'D:/RCA-ext/work/T-013/metrics-selected.json' in actual
    request=Path('C:/Users/84583/.codex/attachments/2f6c5735-a241-4299-bd8c-25d4034a97de/Pasted text.txt').read_text(encoding='utf-8-sig')
    task_block=re.search(r'^<task>\r?\n.*?^</task>',request,re.M|re.S).group(0)
    corrected=log.split('**Khối task đúng nguyên văn, thay cho bản trích dư ở đầu LOG:**',1)[1]
    assert task_block in corrected
    state=(ROOT/'docs/STATE.md').read_text(encoding='utf-8-sig')
    state_record=json.loads((FIX/'chot-ban-giao.json').read_text(encoding='utf-8'))
    expected_state=state_record.get('closure',{}).get('new_own_row',state_record['new_own_row'])
    assert expected_state in state
    assert json.loads((OUT/'trung-gian/kiem-adapter.json').read_text(encoding='utf-8'))['status']=='pass'
response=(TASK/'REVIEW.md').read_bytes().split('## Phản hồi của người làm (người làm điền sau)'.encode('utf-8'))[0]
assert hashlib.sha256(response).hexdigest()=='27ff525c10c00da3a4a7492b31084fc4712045d31257c1bafa88b053dedf0283'
assert (TASK/'LOG.md').read_bytes().startswith((FIX/'truoc-LOG.md').read_bytes())
state_change=json.loads((FIX/'chot-ban-giao.json').read_text(encoding='utf-8'))
state_bytes=(ROOT/'docs/STATE.md').read_bytes()
other_state=b''.join(line for line in state_bytes.splitlines(keepends=True) if not line.startswith(b'| T-013 |'))
assert state_change['state_other_bytes_sha256_before']==state_change['state_other_bytes_sha256_after']
latest_state_change=state_change.get('closure',state_change)
assert latest_state_change['state_other_bytes_sha256_before']==latest_state_change['state_other_bytes_sha256_after']
assert hashlib.sha256(other_state).hexdigest()==latest_state_change['state_other_bytes_sha256_after']
before=json.loads((FIX/'manifest.json').read_text(encoding='utf-8'))['before_hashes']
allowed_changes={'ca-da-chay.csv','cua-so-va-che-do-b.md','danh-sach-file.json','de-xuat-tai-lieu-chung.md','doi-chieu-tieu-chi.md','ho-so-bocpd.md','ho-so-nsigma-phat-hien.md','kiem-ban-giao.json','kiem-tra.json','scripts/kiem_co_che.py','scripts/kiem_ban_giao.py'}
historical_count=0
for path in historical_inventory['result_outputs']:
    relative=path.removeprefix('results/T-013/')
    if relative not in allowed_changes:
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==before[path],path
        historical_count+=1
for snapshot,original in [('truoc-ca-da-chay.csv','ca-da-chay.csv'),('truoc-kiem-tra.json','kiem-tra.json'),('truoc-kiem_co_che.py','scripts/kiem_co_che.py'),('truoc-danh-sach-file.json','danh-sach-file.json'),('truoc-kiem_ban_giao.py','scripts/kiem_ban_giao.py')]:
    assert hashlib.sha256((FIX/snapshot).read_bytes()).hexdigest()==before['results/T-013/'+original]
diff=subprocess.check_output(['git','diff','--check','--','docs/STATE.md','tasks/T-013-ho-so-baro','results/T-013'],cwd=ROOT,text=True)
assert not diff
result={'status':'pass','result_files_read':len(files),'parse_counts':parse_counts,'checks_in_mechanism_summary':len(s['checks']),'focused_fix_checks':len(focused['checks']),'real_metric_points_rechecked':focused['real_metric_points_checked'],'R1_endpoints_checked':50,'R1_variants_checked':100,'R1_candidate_scores_recomputed':sum(map(len,groups.values())),'input_csv_columns':len(header),'input_csv_rows':len(rows)-1,'ledger_rows':len(ledger),'method_cases':sorted(selected),'arithmetic_cases_reused':sorted(delay_cases),'historical_files_unchanged':historical_count,'reviewer_body_unchanged':True,'log_append_only':True,'STATE_only_own_row_changed':True,'code_sources_unchanged':sources,'scope':'only T013 authored paths and exactly one own STATE row; unrelated concurrent changes not claimed as ours','git_diff_check':'pass','handoff_prompt_verbatim_and_inventory_complete':'## Prompt phản biện cho Claude' in log,'issues':issues}
(OUT/'kiem-ban-giao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
