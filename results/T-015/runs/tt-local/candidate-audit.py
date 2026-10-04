"""Audit saved, whitelisted TT predictions; no raw-data or method rerun."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / 'results/T-015/runs/tt-local'
CASES = {
    're2tt_ts-auth-service_cpu_1': 'auth',
    're2tt_ts-route-service_mem_1': 're2tt_ts-route-service_mem_1',
    're2tt_ts-route-service_socket_1': 're2tt_ts-route-service_socket_1',
}

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def first_services(operations, mapping):
    return list(dict.fromkeys(mapping[o] for o in operations))

def run():
    rows, cases = [], []
    for case, folder in CASES.items():
        summary_path, snapshot_path = BASE/folder/'primary-summary.json', BASE/folder/'example.json'
        summary, snapshot = read(summary_path), read(snapshot_path)
        assert summary['status'] == snapshot['status'] == 'ok'
        inv, mapping = summary['inventory'], snapshot['operation_services']
        # Derive candidate and edge sets independently from saved graph relations.
        operations, pairs = set(), set()
        for group in snapshot['groups'].values():
            graph = group['graph']['operation_operation']
            operations.update(graph)
            for parent, children in graph.items():
                pairs.update((parent, child) for child in children)
        graph_services = {mapping[o] for o in operations}
        service_pairs = {(mapping[a], mapping[b]) for a,b in pairs if mapping[a] != mapping[b]}
        edge_services = {s for pair in service_pairs for s in pair}
        any_edge_services = {mapping[o] for pair in pairs for o in pair}
        metric = set(inv['metric_services'])
        trace = set(inv['observed_span_services'])
        full = first_services(snapshot['full_ranks'], mapping)
        truncated = first_services(snapshot['ranks'], mapping)
        checks = {
            'current_graph_services_exact': graph_services == set(inv['current_graph_services']),
            'interservice_edges_exact': service_pairs == {tuple(x) for x in inv['service_edges']},
            'interservice_isolates_exact': graph_services-edge_services == set(inv['services_without_interservice_edge']),
            'operation_edge_isolates_exact': graph_services-any_edge_services == set(inv['services_without_any_operation_edge']),
            'full_service_order_exact': full == summary['service_ranks_full'],
            'top11_service_order_exact': truncated == summary['service_ranks_top11'],
            'full_candidates_equal_current_graph': set(full) == graph_services,
            'no_ranked_service_absent_from_trace': set(full) <= trace,
            'no_duplicate_service_in_mapped_ranks': len(full) == len(set(full)) and len(truncated) == len(set(truncated)),
            'truncated_operations_at_most_11': len(snapshot['ranks']) <= 11,
            'inventory_entity_names_match_metric_columns': metric == {c.split('_')[0] for c in summary['io_metadata']['metric_columns'] if c != 'time'},
        }
        assert all(checks.values()), (case, checks)
        # Labels are read only after all prediction/graph checks are complete.
        label = summary['label_after_ranking']
        gold = label['root_service']
        assert label['rank_full'] == (full.index(gold)+1 if gold in full else None)
        assert label['rank_top11'] == (truncated.index(gold)+1 if gold in truncated else None)
        for service in sorted(metric | trace | graph_services | set(full)):
            rows.append({
                'ca':case, 'thuc_the':service,
                'co_metric':int(service in metric), 'co_trace_cua_so':int(service in trace),
                'co_do_thi_current':int(service in graph_services), 'co_hang_full':int(service in full),
                'co_hang_top11_operation':int(service in truncated),
                'hang_service_full':full.index(service)+1 if service in full else '',
                'hang_service_top11_operation':truncated.index(service)+1 if service in truncated else '',
                'khong_canh_lien_service':int(service in graph_services-edge_services),
                'khong_bat_ky_canh_operation':int(service in graph_services-any_edge_services),
                'nhan_goc_chi_doc_sau_rank':int(service == gold),
                'nguon_summary':str(summary_path.relative_to(ROOT)).replace('\\','/'),
                'nguon_snapshot':str(snapshot_path.relative_to(ROOT)).replace('\\','/'),
            })
        cases.append({
            'case':case, 'checks':checks,
            'counts':{'metric_entities':len(metric),'trace_window_services':len(trace),
                      'current_graph_services':len(graph_services),'full_rank_services':len(full),
                      'top11_operations':len(snapshot['ranks']),'top11_services':len(truncated),
                      'interservice_edges':len(service_pairs),'operation_edges':len(pairs)},
            'absent_trace_ranked':sorted(set(full)-trace),
            'without_interservice_edge':sorted(graph_services-edge_services),
            'without_any_operation_edge':sorted(graph_services-any_edge_services),
            'auth_internal_edges':sorted([list(p) for p in pairs if mapping[p[0]] == mapping[p[1]] == 'ts-auth-service']),
            'gold_after_prediction':label,
            'census':summary['census'],
            'io_metadata_without_metric_columns':{k:v for k,v in summary['io_metadata'].items() if k!='metric_columns'},
            'source_sha256':{str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in [summary_path,snapshot_path]},
        })
    with (ROOT/'results/T-015/bang-ung-vien-tt.csv').open('w',encoding='utf-8-sig',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    result={'whitelist':list(CASES),'case_checks_pass':len(cases),'entity_rows':len(rows),
            'method_rerun':False,'raw_data_opened':False,'cases':cases}
    (BASE/'candidate-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'cases':len(cases),'entity_rows':len(rows),'checks_per_case':len(cases[0]['checks']),'all_pass':True}))

if __name__ == '__main__':
    run()
