"""Tổng hợp kết quả đã lưu, không đọc dữ liệu thô hoặc nhãn."""
from collections import Counter, defaultdict
import gzip
import json
from pathlib import Path
import sys
from engine import ROOT, OUT, load, save, checksum, canon


def main(run_name):
    run = OUT / 'runs' / run_name
    summary = load(run / 'summary.json')
    assert summary['graph_count'] == 1069 and not summary['errors']
    grouped = defaultdict(list)
    full = []
    union = defaultdict(set)
    exclusion_examples = {}
    chains = []
    selected_pairs = {('ts-admin-basic-info-service', 'ts-config-service'),
                      ('ts-food-service', 'ts-station-service'),
                      ('ts-seat-service', 'ts-travel-service'),
                      ('ts-seat-service', 'ts-travel2-service'),
                      ('ts-travel-service', 'ts-order-service'),
                      ('ts-travel2-service', 'ts-order-other-service')}
    for row in summary['rows']:
        family = Path(row['input']).stem.split('-')[0]
        for view, counts in row['views'].items():
            grouped[(row['level'], family, view)].append(counts)
        if family != 'full':
            continue
        path = ROOT / row['output']
        assert checksum(path) == row['output_sha256']
        result = json.loads(gzip.decompress(path.read_bytes()))
        full.append(dict(input=row['input'], output=row['output'], level=row['level'], views=row['views']))
        for view, data in result['views'].items():
            for category in ['S', 'T', 'intersection', 'static_only', 'trace_only']:
                union[(row['level'], view, category)].update(map(canon, data[category]))
            for side, rows in data['exclusions'].items():
                for exclusion in rows:
                    exclusion_examples.setdefault((row['level'], view, side, exclusion['reason']),
                        dict(output=row['output'], exclusion=exclusion))
        if row['level'] == 'entity':
            data = result['views']['endpoints']
            for pair in sorted(selected_pairs):
                key = [*pair, None, None]
                for category in ['intersection', 'static_only', 'trace_only']:
                    if key in data[category]:
                        chains.append(dict(input=row['input'], output=row['output'], key=key, category=category,
                            static_members=[x for x in data['members']['static'] if x['key'] == key],
                            trace_members=[x for x in data['members']['trace'] if x['key'] == key]))
    family_stats = []
    for (level, family, view), rows in sorted(grouped.items()):
        values = {}
        for key in ['S', 'T', 'intersection', 'static_only', 'trace_only', 'static_fraction', 'trace_fraction']:
            distinct = sorted({r[key] for r in rows if r[key] is not None})
            values[key] = dict(min=min(distinct) if distinct else None, max=max(distinct) if distinct else None,
                               null_count=sum(r[key] is None for r in rows), distinct=distinct)
        family_stats.append(dict(level=level, family=family, view=view, graph_count=len(rows), values=values))
    source_doc = load(OUT / 'ban-ghi.json')
    graph = load(OUT / 'do-thi/thuc-the.json')
    data = dict(task='T-038', comparison_run=run_name, conditional_reference=True,
        numerical_source=(run / 'summary.json').relative_to(ROOT).as_posix(),
        family_stats=family_stats, full_graphs=full,
        full_union=[dict(level=k[0], view=k[1], category=k[2], keys=[json.loads(x) for x in sorted(v)]) for k,v in sorted(union.items())],
        exclusions=[dict(level=k[0], view=k[1], side=k[2], reason=k[3], **v) for k,v in sorted(exclusion_examples.items())],
        chain_examples=chains,
        source_counts=dict(entities=len(source_doc['entities']), operations=len(source_doc['operations']),
            relations=len(source_doc['relations']), bindings=len(source_doc['resource_bindings']),
            signals=len(source_doc['signals']), entity_types=dict(Counter(x['type'] for x in source_doc['entities'])),
            signal_kinds=dict(Counter(x['kind'] for x in source_doc['signals'])), entity_graph_edges=len(graph['edges'])),
        do_not_interpret_as=['instrumentation coverage', 'RCA benefit', 'dataset root cause', 'complete semantic source inventory'],
        exclusion_counts_are_overlapping=False,
        exclusion_caution='Counts in each view partition edge indices; reasons across views/groups are not additive causal proportions.')
    save(OUT / 'phan-tich-chenh-lech.json', data)
    # Full input-to-output chains for literal source discrepancies; no source execution.
    acquisition = load(OUT / 'runs/tai-nguon-001/manifest.json')
    indexed = {x['source_path']: x for x in acquisition['files']}
    snippets = []
    selected = [
        ('ts-rebook-service/src/main/java/rebook/service/RebookServiceImpl.java',339,375,'PUT match / POST-delete discrepancy'),
        ('ts-order-service/src/main/java/order/controller/OrderController.java',128,153,'handler verbs'),
        ('ts-order-other-service/src/main/java/other/controller/OrderOtherController.java',125,149,'handler verbs'),
        ('ts-wait-order-service/src/main/java/waitorder/utils/PollThread.java',40,83,'worker wrong literal preserve path'),
        ('ts-preserve-service/src/main/java/preserve/controller/PreserveController.java',16,38,'declared preserve endpoint'),
        ('ts-inside-payment-service/src/main/java/inside_payment/async/AsyncTask.java',14,35,'external endpoint source absent')]
    for path, start, end, meaning in selected:
        entry = indexed.get(path)
        if not entry:
            snippets.append(dict(source_path=path, state='OPEN_PATH_NOT_FOUND', meaning=meaning))
            continue
        actual = ROOT / entry['path']
        assert checksum(actual) == entry['sha256']
        lines = actual.read_text(encoding='utf-8').splitlines()
        snippets.append(dict(source_path=path, sha256=entry['sha256'], revision=acquisition['commit'],
            locator=f'L{start}-L{end}', meaning=meaning, lines=[dict(line=i, text=lines[i-1]) for i in range(start,min(end,len(lines))+1)],
            epistemic_state='FACT source literal; RE2/runtime link OPEN'))
    save(OUT / 'runs' / run_name / 'source-chain-snippets.json', snippets)
    print(canon(dict(family_rows=len(family_stats), full_graphs=len(full), chains=len(chains),
                     trace_only_entity_union=[x['keys'] for x in data['full_union'] if x['level']=='entity' and x['view']=='endpoints' and x['category']=='trace_only'],
                     snippets_open=[x['source_path'] for x in snippets if x.get('state')], source_counts=data['source_counts'])))


if __name__ == '__main__':
    main(sys.argv[1])
