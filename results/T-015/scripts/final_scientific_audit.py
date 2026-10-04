"""Validate existing authorized artifacts; no method or raw-data execution."""
import ast,csv,hashlib,json,math,pathlib,collections
ROOT=pathlib.Path(__file__).resolve().parents[3]; OUT=ROOT/'results/T-015'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
def csvread(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
rows=csvread(OUT/'so-sanh-tung-ca.csv');assert len(rows)==90 and len({r['ca'] for r in rows})==90
checks=[]; evidence=[]
for row in rows:
    result=read(ROOT/pathlib.Path(row['fixed_file']))
    assert result['status']=='ok' and result['ranks'] and len(set(result['ranks']))==len(result['ranks'])
    assert result['ranks']==result['full_ranks'][:11]
    assert result['full_ranks']==sorted(result['scores'],key=result['scores'].get,reverse=True)
    assert all(math.isfinite(v) for v in result['scores'].values())
    assert all(math.isfinite(v) and v>=0 for c in result['spectrum'].values() for v in c.values())
    assert result['counts']['overlap']==0
    assert result['counts']['normal']+result['counts']['anomaly']==result['counts']['all']
    assert all(n<=g['trace_count'] for g in result['groups'].values() for n in g['official']['tracecounts'].values())
    evidence.append({'case':row['ca'],'selected':row['fixed_file'],'root_rank_full':row['fixed_root_rank_service_full']})
check={'rows':len(rows),'statuses':dict(collections.Counter(r['fixed_status'] for r in rows)),
       'operation_top11_changed':sum(r['operation_top11_changed']=='True' for r in rows),
       'service_top11_changed':sum(r['service_top11_changed']=='True' for r in rows),
       'root_rank_top11_changed':sum(r['baseline_root_rank_service_top11']!=r['fixed_root_rank_service_top11'] for r in rows),
       'all_valid_fixed_overlap_zero':True,'numerical_spectrum_nonnegative':True,'rank_unique_nonempty_evidence':True,
       'ref_overlap_cases':sum(int(r['rcaeval_reference_overlap'])>0 for r in rows),
       'negative_nf_count_factor_cases':sum(bool(json.loads(r['rcaeval_negative_nf_count_factor_operations'])) for r in rows),
       'preserved_initial_failures':[], 'source_selection':evidence}
for name in ['re2ob_recommendationservice_loss_1','re2ob_recommendationservice_loss_2']:
    failed=OUT/'runs/ob-block-3'/(name+'.json'); value=read(failed)
    assert value['status']=='failed'
    check['preserved_initial_failures'].append(str(failed.relative_to(ROOT)))
    summary=read(OUT/'runs/ob-duplicate-math'/name/'summary.json');assert summary['all_passed'] and summary['max_absolute_error']==0
save(OUT/'runs/ob-comparison-check-final.json',check)
windows=[]
for path in sorted((OUT/'runs/ob-window300').glob('re2ob_*.json')):
    v300=read(path); row=next(r for r in rows if r['ca']==v300['case_id']); v600=read(ROOT/pathlib.Path(row['fixed_file']))
    assert v300['status']=='ok' and v300['source_sha256']==v600['source_sha256'] and v300['half_seconds']==300
    windows.append({'ca':row['ca'],'half300_normal':v300['counts']['normal'],'half300_anomaly':v300['counts']['anomaly'],
                    'half600_normal':v600['counts']['normal'],'half600_anomaly':v600['counts']['anomaly'],
                    'operation_top11_changed':v300['ranks']!=v600['ranks'],
                    'service_top11_changed':v300['service_ranks_top11']!=v600['service_ranks_top11'],
                    'scores_equal':v300['scores']==v600['scores'],'file300':str(path.relative_to(ROOT)),'file600':row['fixed_file']})
assert len(windows)==2
with (OUT/'kiem-cua-so-ob.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(windows[0]));w.writeheader();w.writerows(windows)
header='phuong_phap,bien_the,vai_tro,tin_hieu_bat_buoc,tin_hieu_tuy_chon,dinh_dang_va_ten_cot_can,can_do_thi,can_moc_su_co,du_lieu_binh_thuong_toi_thieu,can_nhan_de_hoc,don_vi_xep_hang,tham_so_mac_dinh_quan_trong,phu_thuoc_do_dai_cua_so,chi_phi,duong_nhan_rui_ro,ghi_chu'.split(',')
requirements=csvread(OUT/'yeu-cau-dau-vao.csv');assert len(requirements)==7 and list(requirements[0])==header
ledger=csvread(OUT/'ca-da-chay.csv'); assert len(ledger)==110
assert all(r['ly_do'] in ['a','b','c'] and r['file_nguon'] and not r['file_nguon'].startswith('chua_kiem') for r in ledger)
assert sum(r['trang_thai']=='failed' for r in ledger)==2
for p in (OUT/'runs/root-audit-correction').rglob('audit-correction.json'):assert read(p)['all_passed']
probe=read(OUT/'runs/tt-trace-vector-probe/auth/summary.json');assert probe['source_unchanged'] and probe['all_passed'] and probe['n_comparisons']==3027
identity=read(OUT/'runs/final-input-identity-audit/summary.json');assert identity['all_passed'] and len(identity['cases'])==90
assert set(identity['cases_with_current_duplicates'])=={'re2ob_recommendationservice_loss_1','re2ob_recommendationservice_loss_2'}
assert all(v['current_duplicate_occurrences']==0 for v in identity['cases'] if v['case'] not in identity['cases_with_current_duplicates'])
metadata=read(OUT/'runs/ob-root-audit-correction-v2/manifest.json');assert metadata['metadata_audited_cases']==88
assert set(metadata['metadata_not_applicable_cases'])==set(identity['cases_with_current_duplicates'])
assert metadata['all_available_metadata_passed']
original=pathlib.Path('C:/Users/84583/AppData/Local/Temp/claude/D--RCA-flashticket/faa9e437-da55-49ba-b763-6e8484c8c9a6/scratchpad/ext/MicroRank')
ours=ast.parse((ROOT/'src/microrank/official.py').read_text(encoding='utf-8'))
source_nodes={}
for p in original.glob('*.py'):
    for n in ast.parse(p.read_text(encoding='utf-8-sig')).body:
        if isinstance(n,ast.FunctionDef):source_nodes[n.name]=ast.dump(n,include_attributes=False)
for n in ours.body:
    if isinstance(n,ast.FunctionDef):assert ast.dump(n,include_attributes=False)==source_nodes[n.name],n.name
syntax=[]
for p in list((ROOT/'src/microrank').glob('*.py'))+list((OUT/'scripts').glob('*.py')):
    compile(p.read_text(encoding='utf-8-sig'),str(p),'exec');syntax.append(str(p.relative_to(ROOT)))
save(OUT/'runs/final-scientific-audit.json',{'all_passed':True,'comparison_cases':90,'input_rows':7,'exact_input_header':header,
    'case_ledger_rows':110,'preserved_failed_executions':2,'two_window_cases':windows,
    'unchanged_official_ast':True,'final_identity_guard_raw_audit_cases':90,'current_duplicates_only_in_repaired_cases':True,
    'corrected_old_root_audits':88,'new_two_root_audits_already_use_fixed_policy':True,
    'syntax_checked':syntax,'raw_data_not_read_by_this_script':True,'method_not_rerun':True})
print(json.dumps({'status':'pass','cases':90,'ledger':110,'syntax_files':len(syntax)}))
