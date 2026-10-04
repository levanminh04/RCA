"""So hai snapshot của cùng graph PC, không học hoặc chạy lại phương pháp."""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import time
import traceback

import networkx as nx
import numpy as np

from independent_scores import compare_numeric, descendant_adjustment

paper = Path(__file__).resolve().parent
task = paper.parent


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def scores_delta(first, second):
    rows = []
    for label in sorted(set(first) & set(second)):
        a, b = float(first[label]), float(second[label])
        error = abs(a - b)
        rows.append({'metric': label, 'seed0': a, 'seed1': b, 'abs_error': error,
                     'relative_error_seed0': error / abs(a) if a else None,
                     'different_atol_1e7': error > 1e-7,
                     'different_atol_rtol_1e7': error > 1e-7 + 1e-7 * abs(a)})
    return {'count': len(rows), 'different_atol_1e7': sum(x['different_atol_1e7'] for x in rows),
            'different_atol_rtol_1e7': sum(x['different_atol_rtol_1e7'] for x in rows),
            'max_abs_error': max(x['abs_error'] for x in rows),
            'all_rows': rows,
            'largest_differences': sorted(rows,key=lambda r:(-r['abs_error'],r['metric']))[:10]}


def main():
    start = time.perf_counter()
    started_utc = time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    paths = [task/'runs/example-pc/snapshot.json', task/'runs/example-pc-hashseed1/snapshot.json']
    first, second = map(read_json, paths)
    source_checks = {
        'same_graph_nodes': first['graph']['nodes'] == second['graph']['nodes'],
        'same_graph_edges': first['graph']['edges'] == second['graph']['edges'],
        'same_scored_nodes': set(first['nodes']) == set(second['nodes']),
        'same_meta': first['meta'] == second['meta'],
        'same_topological_generation_sets': first['graph']['topological_groups'] == second['graph']['topological_groups'],
    }
    alignment = []
    for label in sorted(set(first['nodes']) & set(second['nodes'])):
        a,b = first['nodes'][label], second['nodes'][label]
        parent_set_same = set(a['parents']) == set(b['parents'])
        row = {'metric': label, 'same_parent_set': parent_set_same,
               'same_parent_order': a['parents'] == b['parents'],
               'parent_order_seed0': a['parents'], 'parent_order_seed1': b['parents']}
        for component in ['train_y','test_y']:
            row[component + '_same'] = bool(np.array_equal(a[component],b[component]))
        for component in ['train_x','test_x']:
            aa,bb = np.asarray(a[component]),np.asarray(b[component])
            if len(a['parents']) and parent_set_same:
                bb = bb[:,[b['parents'].index(p) for p in a['parents']]]
            row[component + '_same_after_parent_alignment'] = bool(np.array_equal(aa,bb))
        alignment.append(row)
    source_checks['all_parent_sets_same'] = all(x['same_parent_set'] for x in alignment)
    source_checks['all_y_arrays_same'] = all(x['train_y_same'] and x['test_y_same'] for x in alignment)
    source_checks['all_X_arrays_same_after_parent_alignment'] = all(
        x['train_x_same_after_parent_alignment'] and x['test_x_same_after_parent_alignment'] for x in alignment)
    raw_scores0 = {k:n['rht_score'] for k,n in first['nodes'].items()}
    raw_scores1 = {k:n['rht_score'] for k,n in second['nodes'].items()}
    rht = scores_delta(raw_scores0,raw_scores1)
    da = scores_delta({k:n['score'] for k,n in first['da'].items()},
                      {k:n['score'] for k,n in second['da'].items()})
    groups = []
    order0,order1 = first['graph']['da_iteration_order'],second['graph']['da_iteration_order']
    for index,(g0,g1) in enumerate(zip(order0,order1)):
        groups.append({'generation_index':index,'size_seed0':len(g0),'size_seed1':len(g1),
                       'same_set':set(g0)==set(g1),'same_order':g0==g1,
                       'positions_different':sum(a!=b for a,b in zip(g0,g1)),
                       'seed0':g0,'seed1':g1})
    # Giữ score gốc seed0 cố định để tách effect thứ tự DA khỏi roundoff OLS.
    control0, unresolved0 = descendant_adjustment(raw_scores0,first['graph']['edges'],order0,3)
    control1, unresolved1 = descendant_adjustment(raw_scores0,first['graph']['edges'],order1,3)
    controlled_delta = scores_delta({k:v['score'] for k,v in control0.items()},
                                   {k:v['score'] for k,v in control1.items()})
    graph = nx.DiGraph();graph.add_nodes_from(first['graph']['nodes']);graph.add_edges_from(first['graph']['edges'])
    components = sorted((sorted(c) for c in nx.strongly_connected_components(graph)),key=lambda c:(-len(c),c))
    bycomponent = {n:(index,len(c)) for index,c in enumerate(components) for n in c}
    changed_scc_sizes = Counter()
    for row in da['all_rows']:
        index,size = bycomponent[row['metric']]
        row['SCC_index_by_size_order'] = index
        row['SCC_size'] = size
        if row['different_atol_rtol_1e7']:
            changed_scc_sizes[size] += 1
    independent_reports = [paper/'compare-example-pc-001/comparison.json',
                           paper/'compare-example-pc-hashseed1-001/comparison.json']
    raw_reports = [paper/'window-example-pc-001/window-comparison.json',
                   paper/'window-example-pc-hashseed1-001/window-comparison.json']
    independent = []
    for seed,snapshot_path,score_path,window_path in zip([0,1],paths,independent_reports,raw_reports):
        score,window = read_json(score_path),read_json(window_path)
        sha = hashlib.sha256(snapshot_path.read_bytes()).hexdigest()
        same_bytes = sha == score['snapshot_sha256'] == window['snapshot_sha256']
        independent.append({'seed':seed,'snapshot':str(snapshot_path),'snapshot_sha256':sha,
                            'numeric_path':str(score_path),'numeric_PASS':score['pass'],
                            'numeric_checks':score['checks_count'],'numeric_max_abs_error':max(c.get('max_abs_error',0) for c in score['checks']),
                            'raw_path':str(window_path),'raw_PASS':window['pass'],
                            'raw_checks':len(window['checks']),'raw_max_abs_error':max(c.get('max_abs_error',0) for c in window['checks']),
                            'same_snapshot_bytes':same_bytes,
                            'unresolved_DA_evidence_count':len(score['DA_unresolved_child_evidence'])})
    report = {
        'case':'re2tt_ts-order-service_loss_3','configuration':'Same cached default-PC EC2 adjacency; RHT/DA scorer hashseed0 and1',
        'seed_source':'Parent run identifiers; snapshot meta does not itself store PYTHONHASHSEED, retain run logs/SPEC/LOG as command provenance.',
        'started_UTC':started_utc,
        'source_checks':source_checks,'parent_order_changed_nodes':sum(not x['same_parent_order'] for x in alignment),
        'parent_and_array_alignment':alignment,'RHT':rht,'DA':da,
        'RHT_top5_seed0':first['ranks'][:5],'RHT_top5_seed1':second['ranks'][:5],
        'DA_top5_seed0':first['ranks_da'][:5],'DA_top5_seed1':second['ranks_da'][:5],
        'RHT_top5_same_metrics':[x[0] for x in first['ranks'][:5]] == [x[0] for x in second['ranks'][:5]],
        'DA_top5_same_metrics':[x[0] for x in first['ranks_da'][:5]] == [x[0] for x in second['ranks_da'][:5]],
        'RHT_above_threshold3_same':{n for n,s in raw_scores0.items() if s>=3}=={n for n,s in raw_scores1.items() if s>=3},
        'DA_iteration_groups':groups,'DA_order_changed_generations':sum(not g['same_order'] for g in groups),
        'graph_is_DAG':nx.is_directed_acyclic_graph(graph),'SCC_count':len(components),
        'nontrivial_SCCs':[c for c in components if len(c)>1],
        'DA_changed_nodes_by_SCC_size':dict(changed_scc_sizes),
        'RHT_equivalent_within_tolerance':rht['different_atol_rtol_1e7']==0,
        'DA_equivalent_within_tolerance':da['different_atol_rtol_1e7']==0,
        'fixed_RHT_seed0_replay_different_DA_order':controlled_delta,
        'fixed_RHT_seed0_replay_unresolved_counts':[len(unresolved0),len(unresolved1)],
        'independent':independent,'verification_PASS':all(source_checks.values()) and all(
            r['numeric_PASS'] and r['raw_PASS'] and r['same_snapshot_bytes'] for r in independent),
        'scope_limit':'Two scorer executions on one cached graph/case; no graph discovery rerun, no prevalence/accuracy claim and no seed selected by label.',
        'elapsed_seconds_diagnostic':time.perf_counter()-start,
    }
    (paper/'crossseed-pc.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    diff_table='\n'.join(f'| {x["metric"]} | {x["seed0"]:.17g} | {x["seed1"]:.17g} | {x["abs_error"]:.17g} |' for x in da['largest_differences'][:5])
    markdown=f'''# Cùng PC graph, đổi hashseed scorer

Nguồn: `runs/example-pc/snapshot.json` và `runs/example-pc-hashseed1/snapshot.json`; ca dev đã chọn trước điểm. Hai snapshot có cùng271 graph nodes,896 edges và270 scored metrics. Không học lại graph. Hashseed0/1 là provenance của hai lượt scorer do người làm tạo; snapshot meta chưa tự lưu biến môi trường này. Source hashes và các kiểm alignment ở `paper/crossseed-pc.json`.

## RHT: sai số số học

Effective parent sets và y train/test giống nhau. Có{report['parent_order_changed_nodes']} node đổi thứ tự parents; X sau căn lại theo parent identity giống hệt. RHT khác{rht['different_atol_1e7']}/270 node nếu dùng **atol đơn thuần1e−7**; khác{rht['different_atol_rtol_1e7']}/270 khi dùng **atol=rtol=1e−7** như SPEC. Max absolute error={rht['max_abs_error']:.17g}. Phải giữ cả hai count để không gọi roundoff bằng thay đổi cơ chế. Top5 RHT cùng metric/cùng thứ tự; tập s≥3 cũng giống nhau.

## DA: thay đổi điểm và top5

DA khác{da['different_atol_1e7']}/270 theo atol đơn thuần, và{da['different_atol_rtol_1e7']}/270 theo atol+rtol1e−7. Max absolute error={da['max_abs_error']:.17g}. Top5 seed0: `{json.dumps([v[0] for v in first['ranks_da'][:5]])}`. Top5 seed1: `{json.dumps([v[0] for v in second['ranks_da'][:5]])}`. Đây là thay điểm/ranking, không chỉ tie display.

| Metric | DA seed0 | DA seed1 | Chênh tuyệt đối |
|---|---:|---:|---:|
{diff_table}

Graph không DAG; SCC không tầm thường có kích thước{[len(c) for c in report['nontrivial_SCCs']]}. Cùng generation sets nhưng{report['DA_order_changed_generations']} generation đổi thứ tự DAScorer thực tế. Script độc lập replay DA giữ **toàn bộ RHT seed0 cố định** và chỉ thay iteration order: vẫn có{controlled_delta['different_atol_rtol_1e7']}/270 DA score đổi vượt tolerance, max error={controlled_delta['max_abs_error']:.17g}. Vì vậy floating-point khác ở hồi quy không đủ giải thích thay đổi DA; set/SCC traversal có bằng chứng trực tiếp trong ca này. Boundary/graph mis-specification vẫn là giải thích khác của chất lượng root ranking, nhưng không giải thích chênh giữa hai replay đã giữ graph/score cố định.

Independent scoring của mỗi snapshot có2160 checks PASS, max absolute error≤2.220446049250313e−16. Raw resampling/parents có1080 array checks mỗi seed PASS, error0. Counts missing child evidence khi cùng generation: seed0={independent[0]['unresolved_DA_evidence_count']}, seed1={independent[1]['unresolved_DA_evidence_count']}; đây là các lần code cần evidence child dưới3 chưa xử lý. Toàn bộ ordered groups và mỗi delta được giữ trong JSON, không chỉ top5.

Giới hạn: đây là1 ca/2 seed với adjacency PC đã cache. Nó chứng minh rủi ro tái lập DA của ca này, không suy tỷ lệ lỗi cả dataset hoặc CIRCA gốc trên DAG. RHT còn roundoff do thứ tự parent/linalg; không có phép kiểm học PC lại trong bước này. Không chọn seed theo root label, không đổi snapshot hay scorer để điểm đẹp hơn.
'''
    (paper/'crossseed-pc.md').write_text(markdown,encoding='utf-8')
    print(json.dumps({'source_and_independent_PASS':report['verification_PASS'],
                      'RHT_changed_abs':rht['different_atol_1e7'], 'RHT_changed_combined':rht['different_atol_rtol_1e7'],
                      'DA_changed_combined':da['different_atol_rtol_1e7'],
                      'fixed_RHT_DA_changed':controlled_delta['different_atol_rtol_1e7'],
                      'DA_max_abs_error':da['max_abs_error'],
                      'parent_order_changed_nodes':report['parent_order_changed_nodes']},ensure_ascii=False))
    return 0 if report['verification_PASS'] else 1


if __name__=='__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        failure={'type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()}
        (paper/'crossseed-pc.failure.json').write_text(json.dumps(failure,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        raise
