"""Đính chính các cờ đã đọc nguồn; không đổi input, quan hệ hay mapping."""
import hashlib
import json
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[4]
RUN=Path(__file__).resolve().parent
OUT=ROOT/'results/T-038'
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
save=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
oracle=load(RUN/'manual-branch-oracle.json')['cases']
flags=load(OUT/'runs/lap-ban-ghi-005/unresolved.json')
acquisition={r['source_path']:r for r in load(OUT/'runs/tai-nguon-001/manifest.json')['files']}
proofs=[]
for case in oracle:
    matches=[r for r in flags if r['kind']=='http_target_unresolved_alternative' and r['fact']['owner']==case['owner'] and r['fact']['java_method']==case['method'] and r['fact']['line']==case['call_line']]
    assert len(matches)==1
    f=matches[0]['fact'];p=ROOT/acquisition[f['source_path']]['path']
    assert sha(p)==acquisition[f['source_path']]['sha256']
    lines=p.read_text(encoding='utf-8').splitlines();get=lambda line:lines[line-1].strip()
    assert case['variable']+' = "";' in get(case['init_line'])
    assert get(case['if_line']).startswith('if (') and '} else {' in get(case['else_line'])
    assert all(case['variable']+' =' in get(case[key]) for key in ['then_assignment','else_assignment'])
    assert all('"/api/v1/' in get(case[key]) for key in ['then_assignment','else_assignment'])
    assert case['call_line']>case['else_assignment']>case['then_assignment']>case['init_line']
    proofs.append(dict(case,source_path=f['source_path'],sha256=sha(p),locator=f"L{case['init_line']}-L{f['end_line']}",
        classification='CLOSED_INITIALIZER_OVERAPPROXIMATION',
        reasoning='Manual control-flow proof: condition completes into exactly one of two assigning branches; exceptional evaluation does not reach this call. No path retaining the initial empty string reaches the call normally. Actual selected service, input values and success remain runtime conditions.',
        nonempty_alternatives=[r for r in f['url_alternatives'] if r['url_template']],
        lines=[dict(line=i,text=lines[i-1]) for i in range(case['init_line'],f['end_line']+1)]))
assert len(proofs)==9
closed={(r['source_path'],r['call_line']) for r in proofs}
rows=[]
for index,r in enumerate(flags):
    f=r['fact'];kind=r['kind']
    if kind=='http_target_unresolved_alternative':
        assert (f['source_path'],f['line']) in closed
        status='closed_parser_overapproximation'
        input_needed=None
    elif kind=='http_no_handler_evidence':
        status='source_external_or_literal_discrepancy_examined'
        input_needed='External service implementation/build for AsyncTask, or runtime/revision evidence before claiming the source method/path discrepancies occurred in RE2.'
    elif kind=='target_handler_candidate_not_verified':
        status='conditional_target_operation_not_silently_verified'
        input_needed='Actual URL/value constraints and routing/profile identity to verify runtime handler; current source candidates and mismatch code already retained.'
    else:
        assert kind=='http_path_or_branch_resolution_open'
        status='source_branch_or_value_conditions_retained'
        input_needed='Runtime inputs/branch activation only if asking which call occurred; not needed to list the union of declared source alternatives.'
    rows.append(dict(original_index=index,original_kind=kind,status=status,source_path=f['source_path'],locator=f"L{f['line']}-L{f['end_line']}",source_flag_is_not_unfinished_task_by_itself=True,additional_input_for_stronger_claim=input_needed))
hashes={name:sha(OUT/name) for name in ['ban-ghi.json','mapping.json','nguon.json','do-thi/thuc-the.json','do-thi/thao-tac.json']}
save(RUN/'source-flag-resolution.json',dict(ok=True,original_flags=len(flags),resolution_counts=dict(Counter(r['status'] for r in rows)),nine_initializer_proofs=proofs,rows=rows,model_input_hashes_unchanged=hashes,
    active_parser_or_graph_changed=False,
    limits='The 151 records overlap; not 151 distinct scientific questions or causal proportions. The 9 closed records remain in immutable assembly005 history, with this classification superseding their OPEN status. No runtime mapping has been promoted to verified.'))
print(json.dumps(dict(ok=True,closed_initializers=9,flags_classified=len(rows),counts=dict(Counter(r['status'] for r in rows))),ensure_ascii=False))
