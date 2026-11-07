"""Write preparation candidates and pins; never opens a telemetry file."""
from pathlib import Path
import json
import hashlib

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent


def pin(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def save(n, d):
    (RUN/n).write_text(json.dumps(d, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


refs = ['src/m1/adapter.py', 'src/p3/adapters/baro.py', 'src/p3/adapters/circa.py',
        'src/p3/adapters/tracerca.py', 'src/p3/adapters/microrank.py',
        'src/p3/adapters/simplerca.py', 'src/p3/adapters/torai.py', 'src/p3/torai_b.py',
        'src/p3/cua_so.py', 'src/circa_kien_truc/builder.py', 'results/T-054/scripts/nguon.py',
        'results/T-054/scripts/worker.py', 'results/T-054/scripts/cham.py', 'results/T-043/hop-dong.json']
save('source-pins.json', {
    'files': {p: pin(ROOT/p) for p in refs},
    'external_static': {'jaeger-json-model-v1.50.0.go': {
        'url': 'https://raw.githubusercontent.com/jaegertracing/jaeger/v1.50.0/model/json/model.go',
        **pin(RUN/'jaeger-json-model-v1.50.0.go')}},
    'network_failure_retained': {
        'url': 'https://api.github.com/users/phamquiluan/repos?per_page=100',
        'urllib': 'CERTIFICATE_VERIFY_FAILED',
        'fallback': 'PowerShell Invoke-RestMethod, normal Windows certificate verification; no relevant collector repository in returned first page',
        'use_as_proof_of_absence': False},
    'tool_failure_retained': 'Large inline shell writer rejected by automatic policy without a specific reason; replaced with reviewable script file and short invocation'})
save('time-and-observation-contract.json', {
    'status': 'CANDIDATE_WITH_EXPLICIT_OPEN_FIELDS_NOT_G3_READY', 'telemetry_opened': False,
    'fields': {
        'metrics.time': {'unit': 's', 'classification': 'FACT_PUBLISHER_DECLARATION',
                         'source': '../cai-ob-source-native-008/re3-dataset-card.json#/text',
                         'measured_RE3_values_checked': False},
        'traces.startTime': {'unit_candidate': 'us', 'classification': 'CANDIDATE_INFERENCE',
                             'evidence': ['RCAEval paper: Jaeger collection',
                                          'Jaeger JSON Span startTime declares microseconds since epoch',
                                          'RCAEval TraceRCA expected method contract'],
                             'missing': 'original RCAEval export transformation or explicit RE3 declaration; Jaeger alone does not prove exported units'},
        'traces.duration': {'unit_candidate': 'us', 'classification': 'CANDIDATE_INFERENCE',
                            'evidence': 'Jaeger JSON model; RCAEval duration/1000; export transformation not established'},
        'traces.startTimeMillis': {'unit_candidate': 'ms', 'classification': 'OPEN',
                                   'reason': 'field name is not proof; no fallback clock'},
        'logs.timestamp': {'unit_candidate': 's', 'classification': 'OPEN',
                           'evidence': 'RE2-TT adapter expects seconds; not proof for held-out RE3'},
        'traces.time': {'use_candidate': 'not a computation clock', 'classification': 'CANDIDATE',
                        'reason': 'large_string format/timezone unspecified; no heuristic parsing'}},
    'cadence_vs_resolution': {
        'classification': 'OPEN',
        'metric_encoding': 'int64 seconds does not establish cadence or observation r',
        'do_not_copy': 'RE2-TT r=1s log/metric and 1us span without RE3 basis',
        'impact': 'M1 coverage/T, E2 rate, c=1 z branch, window assignment and baseline aggregation'},
    'proposed_adapter_rules': [
        'require pinned declared time/observation profile; missing profile blocks before method',
        'integer arithmetic; never auto-guess unit by magnitude',
        'preserve duration in declared unit until explicit conversion; no score-dependent rescaling',
        'metrics/log [t-300,t+300); complete span start>=lo and end<hi; no padding/resampling',
        'schema-compatible is not valid signal; M1 retains missing/nonfinite; baseline preprocessing declared separately'],
    'resolution_owner': 'export/source documentation; Minh decides any explicitly unverified assumption; actual-data validation only in separately authorized final RE3 opening'})

rows = [
    {'method': 'M1 and declared controls', 'schema': 'required span fields and eight metric suffixes; no structured severity',
     'readiness': 'ADAPTER_PROFILE_MISSING',
     'changes': 'RE3 reader/profile with explicit U/alias/r; candidate keyword log rule, no Nezha JSON/severity parser',
     'unknown': 'runtime names, log unit, trace resolution, cadence and observation support'},
    {'method': 'BARO', 'schema': 'five metric layouts compatible by names/types',
     'readiness': 'CANDIDATE_SCHEMA_COMPATIBLE_NOT_EXECUTED',
     'changes': 'explicit dataset binding, frozen preprocessing/kernel/tie keys and column receipts',
     'note': 'pinned preprocess uses same generic branch for re2-tt and re3-ob when dk_select_useful=False; literal re2-tt alone does not prove a numeric defect'},
    {'method': 'SimpleRCA M4', 'schema': 'required metric/trace/log fields present',
     'readiness': 'CANDIDATE_SCHEMA_COMPATIBLE_NOT_EXECUTED',
     'changes': 'canonical declared time/U/alias inputs before existing adapter; no invented severity',
     'unknown': 'finite/missing values and sufficient normal support'},
    {'method': 'MicroRank', 'schema': 'required trace fields present',
     'readiness': 'CANDIDATE_SCHEMA_COMPATIBLE_NOT_EXECUTED',
     'changes': 'declared us contract, real method/operation fields, unchanged status rules',
     'unknown': 'normal/abnormal operations and support cannot be inferred from schema'},
    {'method': 'TraceRCA', 'schema': 'required trace fields present',
     'readiness': 'CANDIDATE_SCHEMA_COMPATIBLE_NOT_EXECUTED',
     'changes': 'explicit dataset binding, retain finite-ji filtering and raw errors',
     'note': 'dataset argument unused by pinned method; identity correction is not evidence of numeric error'},
    {'method': 'CIRCA architecture', 'schema': 'all columns in five schemas map to existing suffix types; call-graph fields present',
     'readiness': 'CANDIDATE_SCHEMA_COMPATIBLE_NOT_EXECUTED',
     'changes': 'explicit dataset, normal-only call graph, isolates, actual last A observation; same SVR/OLS variants',
     'unknown': 'runtime graph, observation support and regression behavior'},
    {'method': 'TORAI B', 'schema': 'required fields present',
     'readiness': 'CURRENT_ADAPTER_FILTER_FAILURE_CONFIRMED_SYNTHETIC',
     'changes': 'TT-only ts-* filter becomes dataset-specific; OB false; preserve bins/seed/kernel and source-B window',
     'unknown': 'statusCode semantics and derived support; summing a different status encoding need not count errors'},
    {'method': 'TORAI A', 'schema': 'raw metadata does not supply author preaggregated A tables',
     'readiness': 'SOURCE_AVAILABILITY_OPEN_NOT_METHOD_UNSUPPORTED',
     'changes': 'establish independent author-source availability/grant/clock/window; reconstructed B must not be renamed A'}]
save('method-support.json', {
    'status': 'STATIC_SUPPORT_PREPARATION_NOT_EMPIRICAL_SUPPORT', 'telemetry_opened': False,
    'rows': rows,
    'evaluation': 'separate 30case/10cell held-out tables for final only; no TT/Nezha A4 thresholds or denominators; arms/seeds/support require explicit protocol; incomplete adapter is not method UNSUPPORTED'})
print('Saved source pins, time/observation contract and eight support entries')
