"""Post-hoc T-028 bridge for the approved T-032 MicroRank comparator.

This file never imports or runs an RCA method, reads raw telemetry or a label
file, or writes an output file.  Call it only after the observed record has been
written, hashed, and compared with the native and frozen outputs.  The two
record byte hashes and the two prerequisite verdicts are supplied by the
trusted coordinator; this bridge independently binds them to the read objects.

API (keyword arguments only)::

    check_t028(repo_root=..., dataset=..., opaque_id=...,
               frozen_record_path=..., frozen_record_sha256=...,
               observed_record_path=..., observed_record_sha256=...,
               trusted_check={
                   'frozen_record_sha256': ...,
                   'observed_record_sha256': ...,
                   'native_observed_exact': True,
                   'approved_record_comparison_passed': True})

The graph is NOT reconstructed.  Ancestors/caller_relation come from the
hash-verified final T-028 row.  Reuse is conditional on exact input hashes,
window, input_shape and observed entity inventory.  M6 uses the frozen
operations_end/local_nonpositive feature, through the actual T-028 local_flag.
Root information is joined here, after the observed method output is saved;
none of this analysis data is supplied to a method.

T-028 functions are compiled from selected, unmodified AST definitions in
their verified snapshots.  No snapshot top-level runner/import/write code is
executed.  analysis_rows is the original function; its graph_relation binding
returns the frozen relation, and its import of ranking_evidence is temporarily
bound to the verified pure helpers.  Both bindings are restored on return.

Score values in the input records are never replaced, normalized or rounded.
Only the frozen-to-observed ranking comparison omits entity_keys and block key
numbers, whose narrow numeric acceptance belongs to the approved comparator.
The frozen self-check keeps those numbers exact.  All other ranking metadata,
tie partitions, locations, probabilities, metrics, flags and N/A reasons stay
exact.  Nezha T-028 stored Hit@1/5 and rank bounds; all Hit@1..10 are additionally
recomputed and compared between the two actual records, not attributed to
fields absent from the saved Nezha row.

CLI prints JSON to stdout.  Fixtures are pure saved-ranking checks, intended
to run on the approved EC2; they are not mechanism evidence or method runs.
"""

import argparse
import ast
import copy
import hashlib
import json
import math
import sys
import types
from contextlib import contextmanager
from fractions import Fraction
from pathlib import Path


SCHEMA = 'T032-MicroRank-T028-bridge-v1'
METHOD = 'microrank_full'
KS = (1, 5)
ALL_KS = tuple(range(1, 11))
MAX_SCRIPT_BYTES = 100 * 1024
MAX_STDOUT_BYTES = 4 * 1024 * 1024

# Immutable authority roots read during this script's approved preparation.
# Descendant data/code hashes are obtained from these manifests/indexes.
ANCHORS = {
    'results/T-028/runs/phan-hoi-review-001/manifest.json':
        '9608215b6499359b9c4914678a31ce789378851bc6a496ea298b984eb3b23c6f',
    'results/T-028/runs/buoc3-005/manifest.json':
        '11e67c17dff71b3e1c66813e00616621211a54fbdf9881700ebd0dde21cda8d9',
    'results/T-024/ban-ghi-dua-vao-cham.json':
        '2d8a11fa8beb83e07989d89f08fc604dff9bd85d1856acc707326a52e9f2e285',
}
LATEST = 'results/T-028/runs/phan-hoi-review-001'
PRIOR = 'results/T-028/runs/buoc3-005'
P3_FUNCTIONS = (
    '_khoa', 'khoi_tu_ban_ghi', 'phan_bo_hang', 'do_ca', 'cham_ca',
)
RANK_FUNCTIONS = (
    '_ks', '_ratio', 'ranking_summary', 'certain_before', 'p0_value',
)
ANALYSIS_FUNCTIONS = ('val', 'local_flag', 'merge_flags', 'assigned', 'analysis_rows')


class BridgeError(Exception):
    """Missing, drifted or unsupported evidence: eligibility must be false."""


def _pointer(part):
    return str(part).replace('~', '~0').replace('/', '~1')


def _digest_bytes(blob):
    return hashlib.sha256(blob).hexdigest()


def _object_digest(obj):
    # Additional object binding; it never substitutes for a record byte hash.
    return _digest_bytes(json.dumps(obj, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':'), allow_nan=False).encode('utf-8'))


def _hash_shape(value):
    return (isinstance(value, str) and len(value) == 64 and
            all(c in '0123456789abcdef' for c in value))


class Sources:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.read_set = []

    def resolve(self, path):
        path = Path(path)
        return path.resolve() if path.is_absolute() else (self.root / path).resolve()

    def read(self, path, expected, authority):
        if not _hash_shape(expected):
            raise BridgeError('Missing/invalid trusted SHA-256 for %s' % path)
        actual_path = self.resolve(path)
        blob = actual_path.read_bytes()
        actual = _digest_bytes(blob)
        entry = {'path': str(actual_path), 'sha256': actual, 'expected_sha256': expected,
                 'bytes': len(blob), 'authority': authority, 'passed': actual == expected}
        self.read_set.append(entry)
        if actual != expected:
            raise BridgeError('Source SHA-256 mismatch: %s' % actual_path)
        return blob

    def json(self, path, expected, authority):
        return json.loads(self.read(path, expected, authority).decode('utf-8-sig'))

    def anchor(self, path):
        return self.json(path, ANCHORS[path], {'pinned_authority_root': path})


def _unique(rows, predicate, description):
    found = [row for row in rows if predicate(row)]
    if len(found) != 1:
        raise BridgeError('%s: expected one entry, found %s' % (description, len(found)))
    return found[0]


def _compile_defs(blob, filename, names, namespace, class_names=()):
    """Execute only original selected definitions, with no snapshot runner."""
    tree = ast.parse(blob.decode('utf-8-sig'), filename=filename)
    selected = [node for node in tree.body
                if (isinstance(node, ast.FunctionDef) and node.name in names) or
                (isinstance(node, ast.ClassDef) and node.name in class_names)]
    expected = set(names) | set(class_names)
    if {node.name for node in selected} != expected or len(selected) != len(expected):
        raise BridgeError('Verified helper definition set is incomplete: %s' % filename)
    module = ast.Module(body=selected, type_ignores=[])
    exec(compile(module, filename, 'exec'), namespace)
    return tree


def _constant(tree, name):
    rows = [node for node in tree.body if isinstance(node, ast.Assign) and
            any(isinstance(target, ast.Name) and target.id == name for target in node.targets)]
    if len(rows) != 1:
        raise BridgeError('Verified source constant missing: %s' % name)
    return ast.literal_eval(rows[0].value)


def _load_helpers(sources, latest_manifest, prior_manifest, p3_config):
    namespace = {'__name__': '_t032_verified_saved_helpers', '__builtins__': __builtins__,
                 'math': math, 'Fraction': Fraction,
                 'comb': math.comb, 'copy': copy}
    p3path = 'src/p3/danh_gia.py'
    p3hash = p3_config['src_p3']['tep'][p3path]
    p3blob = sources.read(p3path, p3hash, {'source_config': p3_config['_authority_path'],
                                        'json_pointer': '/src_p3/tep/src~1p3~1danh_gia.py'})
    p3tree = _compile_defs(p3blob, str(sources.root / p3path), P3_FUNCTIONS,
                          namespace, ('LoiBanGhi',))
    namespace['TRANG_THAI'] = _constant(p3tree, 'TRANG_THAI')
    rank_entry = _unique(prior_manifest['final_scripts'],
                         lambda r: r['snapshot']['path'].endswith('/ranking_evidence.py'),
                         'ranking_evidence snapshot')['snapshot']
    rankblob = sources.read(rank_entry['path'], rank_entry['sha256'],
                            {'manifest': PRIOR + '/manifest.json',
                             'json_pointer': '/final_scripts/*/snapshot'})
    _compile_defs(rankblob, str(sources.root / rank_entry['path']), RANK_FUNCTIONS, namespace)
    analysis_entry = _unique(latest_manifest['final_scripts'],
                             lambda r: r['path'].endswith('/thuc_hien_buoc3_6.py'),
                             'final T028 analysis snapshot')
    analysisblob = sources.read(analysis_entry['snapshot'], analysis_entry['sha256'],
                                {'manifest': LATEST + '/manifest.json',
                                 'json_pointer': '/final_scripts/*'})
    analysis_tree = _compile_defs(analysisblob, str(sources.root / analysis_entry['snapshot']),
                                 ANALYSIS_FUNCTIONS, namespace)
    namespace['ORDER'] = _constant(analysis_tree, 'ORDER')
    namespace['KS'] = _constant(analysis_tree, 'KS')
    if namespace['KS'] != KS or namespace['ORDER'] != ['M1', 'M2', 'M3', 'M4', 'M5', 'M6']:
        raise BridgeError('Frozen T028 codebook constants differ from this bridge scope')
    return namespace


@contextmanager
def _ranking_module(namespace):
    module = types.ModuleType('ranking_evidence')
    for name in RANK_FUNCTIONS:
        setattr(module, name, namespace[name])
    marker = object()
    previous = sys.modules.get('ranking_evidence', marker)
    sys.modules['ranking_evidence'] = module
    try:
        yield
    finally:
        if previous is marker:
            sys.modules.pop('ranking_evidence', None)
        else:
            sys.modules['ranking_evidence'] = previous


def _compare(left, right, path='', output=None):
    """Exact value/type/container comparison.  No numeric tolerance here."""
    output = [] if output is None else output
    if type(left) is not type(right):
        output.append({'path': path, 'kind': 'type', 'frozen': left, 'observed': right,
                       'frozen_type': type(left).__name__, 'observed_type': type(right).__name__})
    elif isinstance(left, dict):
        for key in sorted(set(left) | set(right)):
            target = path + '/' + _pointer(key)
            if key not in left or key not in right:
                output.append({'path': target, 'kind': 'missing_key',
                               'frozen_present': key in left, 'observed_present': key in right})
            else:
                _compare(left[key], right[key], target, output)
    elif isinstance(left, list):
        if len(left) != len(right):
            output.append({'path': path, 'kind': 'length', 'frozen': len(left), 'observed': len(right)})
        for index, (a, b) in enumerate(zip(left, right)):
            _compare(a, b, path + '/' + str(index), output)
    elif left != right or (isinstance(left, float) and not math.isfinite(left)):
        output.append({'path': path, 'kind': 'value', 'frozen': left, 'observed': right})
    return output


def _ranking_view(summary, score_exemption=False):
    out = copy.deepcopy(summary)
    if score_exemption:
        out.pop('entity_keys')
        for block in out['blocks']:
            block.pop('key')
    return out


def _row_view(row, score_exemption=False):
    fields = ('status', 'rank_min', 'rank_max', 'hit@1', 'hit@5',
              'wrong_OK_at_1', 'wrong_OK_at_5', 'seed_metrics',
              'status_by_seed_counts', 'rank_distribution_by_seed', 'mechanisms')
    out = {field: copy.deepcopy(row[field]) for field in fields if field in row}
    out['evidence'] = copy.deepcopy(row['evidence'])
    out['evidence'].pop('source')
    for seed in out['evidence']['seed_evidence'].values():
        seed.pop('source')
        seed['ranking'] = _ranking_view(seed['ranking'], score_exemption)
    return out


def _derive(namespace, row, record, aggregate, feature_path, ref_path):
    """Recompute the original analysis_rows, using the saved graph relation."""
    row = copy.deepcopy(row)
    root, ds, oid = row['root'], row['dataset'], row['opaque_id']
    if row['method'] != METHOD or set(row['evidence']['seed_evidence']) != {'single'}:
        raise BridgeError('Bridge supports only the main MicroRank single-seed row')
    frozen_seed = row['evidence']['seed_evidence']['single']
    frozen_ancestors = frozen_seed['ancestors']
    frozen_relation = frozen_seed['caller_relation']
    summary = namespace['ranking_summary'](record)
    full_summary = namespace['ranking_summary'](record, ks=ALL_KS)
    metrics = namespace['cham_ca'](record, root)
    dist = (namespace['phan_bo_hang'](namespace['khoi_tu_ban_ghi'](record), root)
            if record['status'] == 'OK' else {})
    row.update(status=record['status'], rank_min=metrics['rank_min'], rank_max=metrics['rank_max'])
    for k in KS:
        row['hit@%s' % k] = metrics['hit@%s' % k]
        row['wrong_OK_at_%s' % k] = (metrics['hit@%s' % k] < 1
                                    if record['status'] == 'OK' else None)
    if 'seed_metrics' in row:
        if set(row['seed_metrics']) != {'single'}:
            raise BridgeError('Unexpected MicroRank seed metric coverage')
        row['seed_metrics'] = {'single': copy.deepcopy(metrics)}
        row['status_by_seed_counts'] = {record['status']: 1}
        row['rank_distribution_by_seed'] = {'single': {str(k): str(v) for k, v in dist.items()}}
    if frozen_ancestors['availability'] == 'available':
        if frozen_ancestors['value'] is None or frozen_ancestors['reason'] is not None:
            raise BridgeError('Malformed frozen ancestor measurement')
        graph = object()  # Availability token only; never traversed/rebuilt.
    elif frozen_ancestors['availability'] == 'N/A' and frozen_ancestors['value'] is None:
        if frozen_ancestors['reason'] != 'missing_channel':
            raise BridgeError('Unsupported saved graph N/A reason')
        graph = None
    else:
        raise BridgeError('Malformed frozen graph availability')

    def reused_relation(actual_graph, actual_root, entities):
        if actual_graph is not graph or actual_root != root:
            raise BridgeError('Frozen graph relation binding changed')
        if entities != frozen_seed['ranking']['O']:
            raise BridgeError('Cannot reuse frozen graph relation with changed O')
        return copy.deepcopy(frozen_ancestors), copy.deepcopy(frozen_relation)

    marker = object()
    previous = namespace.get('graph_relation', marker)
    namespace['graph_relation'] = reused_relation
    try:
        with _ranking_module(namespace):
            rebuilt = namespace['analysis_rows'](
                {'main_rows': [row], 'circa_dev19_conditional': {'excluded_confirmed_rounding11': []}},
                {(ds, oid): aggregate}, {(ds, oid): {'end': graph}},
                {(ds, oid, METHOD): [({'path': ref_path}, record)]},
                {ref_path: summary}, {(ds, oid): feature_path})[0]
    finally:
        if previous is marker:
            namespace.pop('graph_relation', None)
        else:
            namespace['graph_relation'] = previous
    return {'row': rebuilt, 'metrics': metrics, 'full_ranking': full_summary}


def _derived_report(derived):
    row = derived['row']
    seed = row['evidence']['seed_evidence']['single']
    return {'metrics': copy.deepcopy(derived['metrics']),
            'ranking_without_numeric_scores': _ranking_view(derived['full_ranking'], True),
            'local_nonpositive': copy.deepcopy(seed['local_nonpositive']),
            'certain_before_root': copy.deepcopy(seed['certain_before_root']),
            'by_k': copy.deepcopy(seed['by_k']), 'mechanisms': copy.deepcopy(row['mechanisms']),
            'wrong_OK_at_1': row['wrong_OK_at_1'], 'wrong_OK_at_5': row['wrong_OK_at_5']}


def _new_verdict(dataset, opaque_id):
    return {'schema': SCHEMA, 'dataset': dataset, 'opaque_id': opaque_id,
            'status': 'ERROR', 'passed': False, 'eligibility': False,
            'source_verified': False, 'frozen_self_check_passed': False,
            'observed_equivalence_passed': False, 'graph_reconstructed': False,
            'record_inputs_mutated': False, 'score_policy':
                'No input score edits; numeric acceptance belongs to the prerequisite comparator',
            'differences': [], 'read_set': [], 'frozen': None, 'observed': None}


def check_t028(*, repo_root, dataset, opaque_id, frozen_record_path,
               frozen_record_sha256, observed_record_path,
               observed_record_sha256, trusted_check):
    """Return a fail-closed, JSON-ready post-hoc flag/metric bridge verdict.

    Source/schema/check exceptions are recorded with type/message and leave all
    eligibility fields false.  A PASS here is conditional on the supplied,
    hash-bound prerequisite native-exact and approved-comparator PASS verdicts.
    It does not certify historical trace memberships or rebuild the graph.
    """
    verdict = _new_verdict(dataset, opaque_id)
    sources = Sources(repo_root)
    try:
        if dataset not in ('RE2-TT', 'Nezha-OB'):
            raise BridgeError('Dataset outside the approved MicroRank main cohort')
        if not isinstance(trusted_check, dict):
            raise BridgeError('trusted_check must be the coordinator binding object')
        required = {'frozen_record_sha256': frozen_record_sha256,
                    'observed_record_sha256': observed_record_sha256,
                    'native_observed_exact': True,
                    'approved_record_comparison_passed': True}
        for key, expected in required.items():
            if key not in trusted_check or type(trusted_check[key]) is not type(expected) or trusted_check[key] != expected:
                raise BridgeError('Trusted prerequisite missing/mismatched: %s' % key)
        verdict['trusted_prerequisites'] = copy.deepcopy(required)
        latest = sources.anchor(LATEST + '/manifest.json')
        prior = sources.anchor(PRIOR + '/manifest.json')
        index24 = sources.anchor('results/T-024/ban-ghi-dua-vao-cham.json')
        config_ref = _unique(index24['records'],
                             lambda r: r['method'] == 'microrank' and r['variant'] == 'full' and
                             r['opaque_id'] == 'dev-03d4910932' and r['seed'] is None,
                             'verified P3 helper source config')
        config = sources.json(config_ref['source_config'], config_ref['source_config_sha256'],
                              {'index': 'results/T-024/ban-ghi-dua-vao-cham.json',
                               'json_pointer': '/records/*/source_config_sha256'})
        config['_authority_path'] = config_ref['source_config']
        namespace = _load_helpers(sources, latest, prior, config)
        analysis_entry = _unique(latest['outputs'],
                                 lambda r: r['path'] == LATEST + '/ca-sai.json',
                                 'final T028 analysis')
        analysis = sources.json(analysis_entry['path'], analysis_entry['sha256'],
                                {'manifest': LATEST + '/manifest.json', 'json_pointer': '/outputs/*'})
        matching_rows = [(i, row) for i, row in enumerate(analysis['main_rows'])
                         if (row['dataset'], row['method'], row['opaque_id']) == (dataset, METHOD, opaque_id)]
        if len(matching_rows) != 1:
            raise BridgeError('MicroRank case missing/duplicated in frozen T028 main_rows')
        row_index, saved_row = matching_rows[0]
        saved_seed = saved_row['evidence']['seed_evidence']['single']
        if set(saved_row['evidence']['seed_evidence']) != {'single'}:
            raise BridgeError('Frozen MicroRank seed evidence must be single')
        source_ref = _unique(saved_row['source']['records'], lambda r: r['seed'] is None,
                             'frozen T028 record binding')
        if len(saved_row['source']['records']) != 1:
            raise BridgeError('Unexpected frozen MicroRank record count')
        if source_ref['sha256'] != frozen_record_sha256:
            raise BridgeError('Injected frozen record hash is not the frozen T028 source hash')
        if saved_seed['source'] != {'path': source_ref['path'], 'json_pointer': ''}:
            raise BridgeError('Frozen seed source does not bind the frozen record')
        index_entry = _unique(latest['outputs'],
                              lambda r: r['path'] == LATEST + '/features-no-label-index.json',
                              'final no-label feature index')
        feature_index = sources.json(index_entry['path'], index_entry['sha256'],
                                     {'manifest': LATEST + '/manifest.json', 'json_pointer': '/outputs/*'})
        feature_ref = feature_index['cases'][dataset][opaque_id]
        feature = sources.json(feature_ref['path'], feature_ref['sha256'],
                               {'index': index_entry['path'],
                                'json_pointer': '/cases/%s/%s' % (_pointer(dataset), _pointer(opaque_id))})
        if (feature['dataset'], feature['opaque_id']) != (dataset, opaque_id):
            raise BridgeError('Frozen feature identity mismatch')
        feature_method = feature['saved_methods'][METHOD]
        if set(feature_method) != {'single'}:
            raise BridgeError('Frozen feature MicroRank seed coverage mismatch')
        feature_source = feature_method['single']['record_source']
        if (feature_source['path'], feature_source['sha256'], feature_source['seed']) != (
                source_ref['path'], source_ref['sha256'], None):
            raise BridgeError('Frozen feature and T028 row record bindings differ')
        if saved_row['evidence']['source'] != {'path': feature_ref['path'], 'json_pointer': '/aggregate'}:
            raise BridgeError('Frozen T028 aggregate source binding differs')
        frozen = sources.json(frozen_record_path, frozen_record_sha256,
                              {'T028_analysis': analysis_entry['path'],
                               'json_pointer': '/main_rows/%s/source/records/0' % row_index})
        observed = sources.json(observed_record_path, observed_record_sha256,
                                {'injected_coordinator_sha256': observed_record_sha256})
        frozen_before, observed_before = _object_digest(frozen), _object_digest(observed)
        for name, record in (('frozen', frozen), ('observed', observed)):
            if (record['opaque_id'], record['method'], record['variant'], record['mode'], record['seed']) != (
                    opaque_id, 'microrank', 'full', 'a', None):
                raise BridgeError('%s MicroRank record identity/configuration mismatch' % name)
        verdict['source_verified'] = True
        verdict['bindings'] = {
            'T028_row': {'path': analysis_entry['path'], 'json_pointer': '/main_rows/%s' % row_index},
            'frozen_record': {'path': str(sources.resolve(frozen_record_path)),
                              'sha256': frozen_record_sha256, 'object_sha256': frozen_before},
            'observed_record': {'path': str(sources.resolve(observed_record_path)),
                                'sha256': observed_record_sha256, 'object_sha256': observed_before},
            'feature': {'path': feature_ref['path'], 'sha256': feature_ref['sha256']}}
        verdict['graph_reuse'] = {
            'reconstructed': False, 'source': analysis_entry['path'],
            'ancestors_pointer': '/main_rows/%s/evidence/seed_evidence/single/ancestors' % row_index,
            'caller_relation_pointer': '/main_rows/%s/evidence/seed_evidence/single/caller_relation' % row_index,
            'condition': 'Exact input_sha256/window/input_shape/sets, unchanged frozen feature bytes',
            'historical_partition_certified': False}
        input_differences = []
        for field in ('input_sha256', 'window', 'input_shape', 'sets'):
            _compare(frozen[field], observed[field], '/input_binding/' + field, input_differences)
        if input_differences:
            verdict['differences'].extend(input_differences)
            raise BridgeError('Frozen graph/aggregate cannot be reused with changed inputs or inventory')
        aggregate = feature['aggregate']
        # Require the actual native-end aggregate schema.  Missing measurements
        # remain their saved N/A objects; missing schema never becomes PASS.
        if not isinstance(aggregate['operations_end']['services'], dict):
            raise BridgeError('Frozen operations_end/services schema is incomplete')
        fresh_frozen = _derive(namespace, saved_row, frozen, aggregate,
                               feature_ref['path'], source_ref['path'])
        self_diff = _compare(_row_view(saved_row), _row_view(fresh_frozen['row']), '/frozen_self_check')
        _compare(feature_method['single']['ranking_summary'],
                 fresh_frozen['row']['evidence']['seed_evidence']['single']['ranking'],
                 '/frozen_feature_ranking_self_check', self_diff)
        verdict['frozen'] = _derived_report(fresh_frozen)
        verdict['t028_saved_metric_fields'] = sorted(
            [key for key in saved_row if key.startswith('hit@') or key in ('rank_min', 'rank_max')] +
            (['seed_metrics/single/' + key for key in saved_row['seed_metrics']['single']]
             if 'seed_metrics' in saved_row else []))
        verdict['frozen_self_check_passed'] = not self_diff
        verdict['differences'].extend(self_diff)
        if self_diff:
            raise BridgeError('Recomputed frozen output does not match final frozen T028')
        fresh_observed = _derive(namespace, saved_row, observed, aggregate,
                                 feature_ref['path'], str(sources.resolve(observed_record_path)))
        verdict['observed'] = _derived_report(fresh_observed)
        observed_diff = _compare(_row_view(fresh_frozen['row'], True),
                                 _row_view(fresh_observed['row'], True), '/observed_equivalence')
        _compare(fresh_frozen['metrics'], fresh_observed['metrics'],
                 '/all_P3_metrics_Hit1_to_10', observed_diff)
        _compare(_ranking_view(fresh_frozen['full_ranking'], True),
                 _ranking_view(fresh_observed['full_ranking'], True),
                 '/full_ranking_Hit1_to_10', observed_diff)
        for name, fresh in (('frozen', fresh_frozen), ('observed', fresh_observed)):
            summary = fresh['full_ranking']
            if fresh['row']['status'] == 'OK' and summary['availability'] != 'available':
                observed_diff.append({'path': '/' + name + '/ranking/invariant',
                                      'kind': 'invalid_OK_ranking', 'summary': _ranking_view(summary, True)})
        if frozen_before != _object_digest(frozen) or observed_before != _object_digest(observed):
            verdict['record_inputs_mutated'] = True
            observed_diff.append({'path': '/records', 'kind': 'input_object_mutated'})
        verdict['observed_equivalence_passed'] = not observed_diff
        verdict['differences'].extend(observed_diff)
        verdict['passed'] = not verdict['differences']
        verdict['eligibility'] = verdict['passed']
        verdict['status'] = 'PASS' if verdict['passed'] else 'FAIL'
    except Exception as exc:
        verdict['status'] = 'ERROR'
        verdict['passed'] = verdict['eligibility'] = False
        verdict['error'] = {'type': type(exc).__name__, 'message': str(exc)}
    finally:
        verdict['read_set'] = sources.read_set
    return verdict


def _fixture_record(order=('caller', 'other', 'root'), observed=None, tie=False):
    keys = [2.0, 2.0, 1.0] if tie else [3.0, 2.0, 1.0]
    entities = [{'entity': entity, 'key': [keys[i]], 'tie_group': (0 if i < 2 else 1) if tie else i}
                for i, entity in enumerate(order)]
    return {'opaque_id': 'fixture', 'method': 'microrank', 'variant': 'full', 'mode': 'a',
            'seed': None, 'status': 'OK', 'entity_ranking': entities, 'ranking': [], 'blocks': None,
            'sets': {'observed_entities': sorted(observed or ['caller', 'other', 'root'])},
            'diagnostics': {}, 'extra': {}, 'input_shape': {'spans': 4},
            'window': {'t': 10}, 'input_sha256': {'traces.parquet': 'fixture-only'}}


def fixtures(repo_root):
    """Pure small ranking/flag fixtures, no real case or method is executed."""
    sources = Sources(repo_root)
    latest = sources.anchor(LATEST + '/manifest.json')
    prior = sources.anchor(PRIOR + '/manifest.json')
    index = sources.anchor('results/T-024/ban-ghi-dua-vao-cham.json')
    ref = _unique(index['records'], lambda r: r['method'] == 'microrank' and r['variant'] == 'full' and
                  r['opaque_id'] == 'dev-03d4910932' and r['seed'] is None, 'fixture helper config')
    config = sources.json(ref['source_config'], ref['source_config_sha256'], {'frozen_index': ref['source_config']})
    config['_authority_path'] = ref['source_config']
    namespace = _load_helpers(sources, latest, prior, config)
    base = _fixture_record()
    saved_summary = namespace['ranking_summary'](base)
    row = {'dataset': 'fixture', 'opaque_id': 'fixture', 'method': METHOD, 'root': 'root',
           'status': 'OK', 'rank_min': 3, 'rank_max': 3, 'hit@1': 0.0, 'hit@5': 1.0,
           'wrong_OK_at_1': True, 'wrong_OK_at_5': False,
           'evidence': {'seed_evidence': {'single': {
               'ranking': saved_summary, 'ancestors': namespace['val'](['caller']),
               'caller_relation': {'caller': {'path_to_root': True}, 'other': {'path_to_root': False},
                                   'root': {'path_to_root': False}}}}}}
    aggregate = {'metrics': {}, 'trace_start': {}, 'trace_end': {}, 'logs_A': {},
                 'operations_end': {'operations': {}, 'services': {
                     'root': {'local_nonpositive': namespace['val'](False)}}}}
    original = copy.deepcopy((base, row, aggregate))
    checks = []

    def check(name, condition, details=None):
        checks.append({'name': name, 'passed': bool(condition), 'details': details})

    frozen = _derive(namespace, row, base, aggregate, 'fixture-feature', 'fixture-record')
    changed = _derive(namespace, row, _fixture_record(('root', 'other', 'caller')),
                      aggregate, 'fixture-feature', 'fixture-observed')
    diff = _compare(_row_view(frozen['row'], True), _row_view(changed['row'], True))
    check('changed_M5_Hit_assignment_is_detected', bool(diff) and
          frozen['row']['evidence']['seed_evidence']['single']['by_k']['1']['flags']['M5']['value'] is True and
          changed['row']['evidence']['seed_evidence']['single']['by_k']['1']['flags']['M5']['value'] is False)
    local_changed = copy.deepcopy(aggregate)
    local_changed['operations_end']['services']['root']['local_nonpositive'] = namespace['val'](True)
    local = _derive(namespace, row, base, local_changed, 'fixture-feature', 'fixture-record')
    check('operations_end_M6_change_is_detected', bool(_compare(_row_view(frozen['row'], True),
                                                               _row_view(local['row'], True))) and
          local['row']['evidence']['seed_evidence']['single']['by_k']['1']['flags']['M6']['value'] is True)
    reordered = _derive(namespace, row, _fixture_record(('other', 'caller', 'root')),
                        aggregate, 'fixture-feature', 'fixture-observed')
    check('cross_service_order_is_detected_even_with_same_root_Hit',
          frozen['metrics'] == reordered['metrics'] and
          bool(_compare(_ranking_view(frozen['full_ranking'], True),
                        _ranking_view(reordered['full_ranking'], True))))
    invalid = _fixture_record(observed=['caller', 'root'])
    invalid_row = copy.deepcopy(row)
    invalid_row['evidence']['seed_evidence']['single']['ranking'] = namespace['ranking_summary'](invalid)
    malformed = _derive(namespace, invalid_row, invalid, aggregate, 'fixture-feature', 'fixture-record')
    invalid_seed = malformed['row']['evidence']['seed_evidence']['single']
    check('invalid_invariant_stays_NA_with_reason',
          malformed['full_ranking']['availability'] == 'N/A' and
          invalid_seed['by_k']['1']['P0']['reason'] == 'invalid_ranking_invariant' and
          invalid_seed['by_k']['1']['flags']['M5']['reason'] == 'invalid_ranking_invariant')
    missing_graph_row = copy.deepcopy(row)
    missing_graph_row['evidence']['seed_evidence']['single']['ancestors'] = namespace['val'](None, 'missing_channel')
    missing_graph_row['evidence']['seed_evidence']['single']['caller_relation'] = {}
    missing = _derive(namespace, missing_graph_row, base, aggregate, 'fixture-feature', 'fixture-record')
    m5 = missing['row']['mechanisms']['1']['base_flags_all_OK_seeds']['M5']
    check('merged_NA_reason_is_preserved', m5['value'] is None and m5['reason'] == 'missing_channel' and
          m5['n_seed_NA'] == 1 and m5['n_seed_eligible'] == 1)
    drift = copy.deepcopy(base)
    drift['entity_ranking'][0]['key'][0] = math.nextafter(drift['entity_ranking'][0]['key'][0], math.inf)
    drifted = _derive(namespace, row, drift, aggregate, 'fixture-feature', 'fixture-observed')
    check('score_only_drift_does_not_edit_records_or_hide_semantic_fields',
          not _compare(_row_view(frozen['row'], True), _row_view(drifted['row'], True)) and
          bool(_compare(_row_view(frozen['row']), _row_view(drifted['row']))) and
          drift['entity_ranking'][0]['key'][0] != base['entity_ranking'][0]['key'][0])
    tied = _fixture_record(tie=True)
    broken = copy.deepcopy(tied)
    broken['entity_ranking'][1]['key'][0] = math.nextafter(2.0, 0.0)
    broken['entity_ranking'][1]['tie_group'] = 1
    broken['entity_ranking'][2]['tie_group'] = 2
    check('tie_partition_change_is_detected', bool(_compare(
        _ranking_view(namespace['ranking_summary'](tied), True),
        _ranking_view(namespace['ranking_summary'](broken), True))))
    check('pure_helpers_preserve_fixture_input_objects', (base, row, aggregate) == original)
    return {'schema': SCHEMA, 'scope': 'pure fixtures only; not mechanism evidence',
            'status': 'PASS' if all(x['passed'] for x in checks) else 'FAIL',
            'passed': all(x['passed'] for x in checks), 'checks': checks,
            'read_set': sources.read_set, 'graph_reconstructed': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    fixture = sub.add_parser('fixtures')
    fixture.add_argument('--repo-root', required=True)
    one = sub.add_parser('check')
    one.add_argument('--repo-root', required=True)
    one.add_argument('--dataset', required=True, choices=('RE2-TT', 'Nezha-OB'))
    one.add_argument('--opaque-id', required=True)
    one.add_argument('--frozen-record', required=True)
    one.add_argument('--frozen-sha256', required=True)
    one.add_argument('--observed-record', required=True)
    one.add_argument('--observed-sha256', required=True)
    one.add_argument('--trusted-check', required=True)
    one.add_argument('--trusted-check-sha256', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'fixtures':
            result = fixtures(args.repo_root)
        else:
            trusted_sources = Sources(args.repo_root)
            trusted = trusted_sources.json(args.trusted_check, args.trusted_check_sha256,
                                            {'injected_coordinator_sha256': args.trusted_check_sha256})
            result = check_t028(repo_root=args.repo_root, dataset=args.dataset,
                                opaque_id=args.opaque_id, frozen_record_path=args.frozen_record,
                                frozen_record_sha256=args.frozen_sha256,
                                observed_record_path=args.observed_record,
                                observed_record_sha256=args.observed_sha256, trusted_check=trusted)
            result['read_set'] = trusted_sources.read_set + result['read_set']
    except Exception as exc:
        result = {'schema': SCHEMA, 'status': 'ERROR', 'passed': False, 'eligibility': False,
                  'error': {'type': type(exc).__name__, 'message': str(exc)}}
    serialized = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)
    if len(serialized.encode('utf-8')) > MAX_STDOUT_BYTES:
        result['status'] = 'ERROR'
        result['passed'] = result['eligibility'] = False
        result['error'] = {'type': 'BridgeError', 'message': 'Full bridge output exceeds declared 4 MiB bound'}
        result.pop('frozen', None)
        result.pop('observed', None)
        result['differences_omitted_for_stdout_size'] = len(result.pop('differences', []))
        serialized = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)
    print(serialized)
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    raise SystemExit(main())
