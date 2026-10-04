"""Verify approved repairs against retained outputs; no raw or method execution."""
import ast
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
OUT=ROOT/'results/T-015'
HERE=OUT/'runs/review-response'
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def csvrows(path):
    with path.open(encoding='utf-8-sig',newline='') as stream:return list(csv.DictReader(stream))
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

before=read(HERE/'source-before/results/T-015/manifest-ban-giao.json')
allowed_changed={
    'tasks/T-015-ho-so-microrank/SPEC.md','tasks/T-015-ho-so-microrank/LOG.md',
    'results/T-015/manifest-ban-giao.json','results/T-015/ho-so-microrank.md',
    'results/T-015/ho-so-phat-hien-trace.md','results/T-015/tracerca-rcaeval.md',
    'results/T-015/vi-du-tinh-tay.md','results/T-015/kiem-ung-vien-tt.md',
    'results/T-015/yeu-cau-dau-vao.csv','results/T-015/de-xuat-tai-lieu-chung.md',
    'results/T-015/kiem-dung-dan.md','results/T-015/tieu-chi-xong.csv',
    'results/T-015/bao-cao-cuoi.md','src/microrank/__init__.py','src/microrank/detectors.py',
    'results/T-015/scripts/check_tracerca.py','results/T-015/scripts/independent_inputs.py',
    'results/T-015/scripts/test_adapter.py','results/T-015/scripts/test_original_formula.py',
}
changed=[]
original_paths=set()
for entry in before['local_files']:
    path=Path(entry['path']);original_paths.add(path.resolve())
    assert path.is_file(),f'Missing retained file: {path}'
    if entry.get('sha256') is None:continue
    if digest(path)!=entry['sha256']:
        relative=path.relative_to(ROOT).as_posix()
        assert relative in allowed_changed,f'Unexpected change: {relative}'
        changed.append(relative)

requirements=csvrows(OUT/'yeu-cau-dau-vao.csv')
header='phuong_phap,bien_the,vai_tro,tin_hieu_bat_buoc,tin_hieu_tuy_chon,dinh_dang_va_ten_cot_can,can_do_thi,can_moc_su_co,du_lieu_binh_thuong_toi_thieu,can_nhan_de_hoc,don_vi_xep_hang,tham_so_mac_dinh_quan_trong,phu_thuoc_do_dai_cua_so,chi_phi,duong_nhan_rui_ro,ghi_chu'.split(',')
assert len(requirements)==7 and list(requirements[0])==header
assert (OUT/'yeu-cau-dau-vao.csv').read_bytes().startswith(b'\xef\xbb\xbf')
assert len(csvrows(OUT/'ca-da-chay.csv'))==110
criteria=csvrows(OUT/'tieu-chi-xong.csv')
assert len(criteria)==10 and '3/30' in criteria[4]['ket_luan'] and '27' in criteria[4]['ket_luan']

ob=csvrows(OUT/'so-sanh-tung-ca.csv')
assert len(ob)==90 and len({row['ca'] for row in ob})==90
for row in ob:
    result=read(ROOT/row['fixed_file'])
    assert result['status']=='ok' and result['ranks'] and result['counts']['overlap']==0
    assert result['ranks']==result['full_ranks'][:11]
    assert all(math.isfinite(value) and value>=0 for cells in result['spectrum'].values() for value in cells.values())
    assert all(math.isfinite(value) for value in result['scores'].values())
    assert result['full_ranks']==sorted(result['scores'],key=result['scores'].get,reverse=True)
    assert all(value<=group['trace_count'] for group in result['groups'].values() for value in group['official']['tracecounts'].values())
assert read(OUT/'runs/tt-independent-math/auth/summary.json')['all_passed']
assert read(OUT/'runs/tt-trace-vector-probe/auth/summary.json')['n_comparisons']==3027

guard=read(HERE/'guard-tests.json')
assert guard['all_passed'] and sum(guard[key] for key in ['adapter_guard_cases','independent_tracerca_guard_cases','root_duration_guard_cases'])==27
assert guard['valid_adapter_matches_frozen_exactly'] and guard['independent_valid_input_matches_frozen_exactly']
for path,sha in guard['source_hashes'].items():assert digest(ROOT/path)==sha
raw=read(HERE/'ec2-second/input-time-audit/summary.json')
assert raw['all_passed'] and len(raw['cases'])==93
assert not raw['method_rerun'] and not raw['labels_read']
assert all(case['source_hash_matches_saved'] and case['invalid_time_rows']==case['window_invalid_time_rows']==0 for case in raw['cases'])
assert sum(case['case'].startswith('re2ob_') for case in raw['cases'])==90
assert {case['case'] for case in raw['cases'] if case['case'].startswith('re2tt_')}=={'re2tt_ts-auth-service_cpu_1','re2tt_ts-route-service_mem_1','re2tt_ts-route-service_socket_1'}

probe=read(HERE/'iteration-probe.json')
assert probe['fixed_turns_before_probe']==[25,26,50,100,101]
assert [row['iterations'] for row in probe['rows']]==probe['fixed_turns_before_probe']
assert probe['rows'][0]['max_score_delta_vs_saved']==probe['rows'][0]['max_score_relative_delta_vs_saved']==0
assert all(row['top11_changed_vs25'] for row in probe['rows'][1:4])
assert not probe['rows'][4]['top11_changed_vs25'] and probe['rows'][4]['full_ranks_changed_vs25']
for entry in probe['input_manifest']:assert digest(ROOT/entry['path'])==entry['sha256']
assert digest(ROOT/'results/T-015/scripts/check_review_diagnostics.py')==probe['script_sha256']
lengths=csvrows(HERE/'trace-length-stats.csv')
assert len(lengths)==8
for row in lengths:
    assert digest(ROOT/row['source_path'])==row['source_sha256']
auth=next(row for row in lengths if row['case']=='re2tt_ts-auth-service_cpu_1' and row['sample']=='primary' and row['group']=='anomaly')
assert auth['ge100_trace_count']==auth['station_trace_count']=='903'
assert auth['station_and_ge100_trace_count']=='866' and auth['station_and_ge100_sets_equal']=='False'

provenance=read(ROOT/'src/microrank/PROVENANCE.json')
official=ast.parse((ROOT/'src/microrank/official.py').read_text(encoding='utf-8'))
for node in official.body:
    if not isinstance(node,ast.FunctionDef):continue
    source=next(entry for entry in provenance['functions'] if entry['function']==node.name)
    author=ast.parse(Path(source['source']).read_text(encoding='utf-8'))
    target=next(value for value in author.body if isinstance(value,ast.FunctionDef) and value.name==node.name)
    assert ast.dump(node,include_attributes=False)==ast.dump(target,include_attributes=False)
for entry in read(HERE/'current-source-manifest.json')['files']:assert digest(ROOT/entry['path'])==entry['sha256']
syntax=[]
for path in sorted(list((ROOT/'src/microrank').glob('*.py'))+list((OUT/'scripts').glob('*.py'))+list(HERE.glob('*.py'))):
    compile(path.read_text(encoding='utf-8-sig'),str(path),'exec');syntax.append(path.relative_to(ROOT).as_posix())

review=(ROOT/'tasks/T-015-ho-so-microrank/REVIEW.md').read_bytes()
marker='| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |'.encode()
position=review.index(marker)
assert position==13339 and hashlib.sha256(review[:position]).hexdigest()=='e23ff02a79d9b06e39cdf21d83fa0e63fcb57e07dd5d9e3258d8c262b741d2ae'
report=(OUT/'bao-cao-cuoi.md').read_text(encoding='utf-8')
for section in ['A. Đã làm','B. File đã thay đổi','C. Kiểm tra đã chạy','D. VẤN ĐỀ Ở TASK CŨ','E. Chỗ lệch khỏi SPEC','F. Đề xuất cho tài liệu chung','G. Phần chưa kiểm','H. Cần Minh quyết']:assert section in report
state=(ROOT/'docs/STATE.md').read_text(encoding='utf-8')
assert len([line for line in state.splitlines() if line.startswith('| T-015 |')])==1
new_files=[]
for folder in [OUT,ROOT/'src/microrank',ROOT/'tasks/T-015-ho-so-microrank']:
    for path in sorted(folder.rglob('*')):
        if path.is_file() and path.resolve() not in original_paths:new_files.append(path.relative_to(ROOT).as_posix())
json_count=0
for path in OUT.rglob('*.json'):read(path);json_count+=1
result=dict(all_passed=True,approved_existing_files_changed=changed,new_local_files_since_initial_manifest=new_files,
            reviewer_body_preserved=True,original_scientific_outputs_unchanged=True,original_kernel_AST_unchanged=True,
            cases_compared=90,raw_input_time_cases=93,guard_cases=27,case_ledger_rows=110,input_columns=16,input_rows=7,
            TT_method_scope='3/30dev; no additional 27 method runs',no_dataset_ranker_rerun=True,
            diagnostic_turns=probe['fixed_turns_before_probe'],syntax_checked=syntax,json_artifacts_parsed=json_count,
            note='Initial manifest predates REVIEW and its responses. STATE row preservation is checked at each exact update; shared rows are not compared to a stale whole file.')
(HERE/'repair-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({key:result[key] for key in ['all_passed','cases_compared','raw_input_time_cases','guard_cases','case_ledger_rows','json_artifacts_parsed']},ensure_ascii=False))
