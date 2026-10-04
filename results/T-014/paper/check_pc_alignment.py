"""Kiểm identity/endpoint/cửa sổ từ raw và adjacency EC2; không gọi RCAEval."""
from collections import Counter
import hashlib
import json
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

from independent_window import prepare

paper = Path(__file__).resolve().parent
task = paper.parent
ec2 = task / 'runs/ec2-default-003'
snapshot_path = task / 'runs/example-pc/snapshot.json'
snapshot = json.loads(snapshot_path.read_text(encoding='utf-8'))
names = json.loads((ec2 / 'nodes.json').read_text(encoding='utf-8'))
metadata = json.loads((ec2 / 'input.json').read_text(encoding='utf-8'))
adj = np.load(ec2 / 'adj.npy', allow_pickle=False)
window = json.loads((paper / 'window-example-pc-001/window-comparison.json').read_text(encoding='utf-8'))
selected = json.loads((task / 'runs/selection-before-scores.json').read_text(encoding='utf-8'))['selected']
inventory = json.loads((task / 'runs/inventory.json').read_text(encoding='utf-8'))
assert len(inventory) == 30 and selected in {r['case'] for r in inventory}
row = next(r for r in inventory if r['case'] == selected)
raw_path = Path(row['source'])
assert raw_path.parent.name == selected and not any(p.lower() == 'locked' for p in raw_path.parts)
raw = pd.read_parquet(raw_path)
time, prepared, constants = prepare(raw, row['inject_time'], normal=False)
assert adj.shape == (len(names), len(names)) and len(set(names)) == len(names)

# causal-learn a->b: endpoint at a=-1 (tail), at b=1 (arrow).
# rht.py first adds that direction, then graph.reverse flips directed edges.
edges, counts, unexpected = set(), Counter(), []
directed_examples = []
for a in range(len(names)):
    for b in range(a + 1, len(names)):
        pair = (int(adj[a, b]), int(adj[b, a]))
        if pair == (0, 0):
            counts['no_edge_pairs'] += 1
        elif pair == (-1, -1):
            counts['undirected_pairs'] += 1
            edges.update([(names[a], names[b]), (names[b], names[a])])
        elif pair in [(-1, 1), (1, -1)]:
            counts['directed_pairs'] += 1
            pc_source, pc_target = (names[a], names[b]) if pair == (-1, 1) else (names[b], names[a])
            edges.add((pc_target, pc_source))
            directed_examples.append({'PC_source': pc_source, 'PC_target': pc_target,
                                      'scorer_source': pc_target, 'scorer_target': pc_source})
        else:
            unexpected.append({'a': names[a], 'b': names[b], 'endpoints': pair})
graph = nx.DiGraph()
graph.add_edges_from(edges)
snapshot_edges = {tuple(e) for e in snapshot['graph']['edges']}
components = sorted((sorted(c) for c in nx.strongly_connected_components(graph)),
                    key=lambda c: (-len(c), c))
metric = snapshot['ranks'][0][0]
root_component = next(c for c in components if metric in c)
root_parent_set = {a for a, b in edges if b == metric and a in snapshot['nodes']}
source_hashes = {}
for path in [ec2/'adj.npy', ec2/'nodes.json', ec2/'input.json', snapshot_path, raw_path]:
    source_hashes[str(path.resolve())] = {
        'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
checks = {
    'EC2_names_equal_input_columns': names == metadata['columns'],
    'EC2_names_equal_independent_processed_raw_columns': names == list(prepared),
    'identity_has_exactly_one_underscore': all(n.count('_') == 1 for n in names),
    'identity_parser_lossless': all('_'.join(n.split('_')[:2]) == n for n in names),
    'PC_input_rows_600': len(time) == metadata['shape'][0] == 600,
    'PC_input_column_count_matches': metadata['shape'][1] == len(names) + 1,
    'PC_first_timestamp_matches_raw': float(time[0]) == metadata['pc_first'],
    'PC_last_timestamp_matches_raw': float(time[-1]) == metadata['pc_last'],
    'endpoint_values_supported': not unexpected,
    'endpoint_diagonal_zero': bool(np.all(np.diag(adj) == 0)),
    'rebuilt_edges_equal_snapshot': edges == snapshot_edges,
    'edge_nodes_equal_snapshot_graph': set(graph) == set(snapshot['graph']['nodes']),
    'selected_metric_effective_parents_equal': root_parent_set == set(snapshot['nodes'][metric]['parents']),
    'raw_window_comparison_PASS': window['pass'],
    'snapshot_bytes_match_window': window['snapshot_sha256'] == source_hashes[str(snapshot_path.resolve())]['sha256'],
}
report = {
    'case': selected, 'method': 'PC default causal-learn 0.1.3.8, alpha .05; no depth cap',
    'pass': all(checks.values()), 'checks': checks,
    'source_hashes': source_hashes, 'source_node_count': len(names),
    'processed_constant_columns': constants, 'PC_time_bounds': [float(time[0]), float(time[-1])],
    'endpoint_pair_counts': dict(counts), 'unexpected_endpoint_pairs': unexpected,
    'rebuilt_edge_count': len(edges), 'edge_node_count': len(graph),
    'source_isolates_dropped_by_wrapper': sorted(set(names) - set(graph)),
    'graph_nodes_pruned_by_CaseData': window['dropped_nodes'],
    'is_DAG': nx.is_directed_acyclic_graph(graph),
    'SCC_count': len(components), 'nontrivial_SCCs': [c for c in components if len(c) > 1],
    'selected_metric': metric, 'selected_metric_SCC': root_component,
    'selected_metric_effective_parents': sorted(root_parent_set),
    'selected_metric_resampling': window['raw_to_grid'][metric],
    'directed_edge_reversal_examples': directed_examples[:10],
    'scope': 'Kiểm bytes/identity/endpoint adapter và raw->window của ca đã chọn; không khẳng định true causal graph hoặc tái lập số paper.'
}
(paper/'pc-source-alignment.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({k: report[k] for k in ['pass', 'source_node_count', 'rebuilt_edge_count',
                                       'edge_node_count', 'is_DAG', 'SCC_count',
                                       'source_isolates_dropped_by_wrapper',
                                       'graph_nodes_pruned_by_CaseData']}, ensure_ascii=False))
raise SystemExit(0 if report['pass'] else 1)
