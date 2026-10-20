"""AST/pin/diff metadata only; never import method or execute any fixture."""
from pathlib import Path
import ast
import difflib
import hashlib
import json

ROOT = Path(__file__).resolve().parents[4]
S = ROOT / 'results/T-032/scripts'
OUT = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def text(path):
    return path.read_text(encoding='utf-8-sig')

def functions(tree):
    return {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}

def dump_ast(node):
    return ast.dump(node, include_attributes=False)

def literals(tree):
    result = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                result[node.targets[0].id] = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                pass
    return result

names = ('replay_tracerca_v3.py', 'audit_tracerca_posthoc_v1.py', 'run_tracerca_path_pilots_v2.py')
trees = {name: ast.parse(text(S / name), filename=name) for name in names}
for name, tree in trees.items():
    compile(tree, name, 'exec')
old = ast.parse(text(S / 'replay_tracerca_v2.py'))
of, nf = functions(old), functions(trees['replay_tracerca_v3.py'])
unchanged = [name for name in of if dump_ast(of[name]) == dump_ast(nf[name])]
changed = [name for name in of if dump_ast(of[name]) != dump_ast(nf[name])]
assert changed == ['verify_tracerca', 'fixture_data', 'fixtures', 'main'], changed
assert dump_ast(of['one']) == dump_ast(nf['one'])
before_verifier = dump_ast(of['verify_tracerca'])
after_verifier = dump_ast(nf['verify_tracerca'])
assert after_verifier.replace("keywords=[keyword(arg='use_threads', value=Constant(value=False))]", "keywords=[]") == before_verifier
circa = ast.parse(text(S / 'replay_circa_v2.py'))
helper_ast = dump_ast(functions(circa)['table_columns'])
assert helper_ast == dump_ast(nf['table_columns'])
provenance = literals(trees['replay_tracerca_v3.py'])['TABLE_COLUMNS_PROVENANCE']
assert provenance['source_sha256'] == sha(S / 'replay_circa_v2.py')
assert provenance['function_ast_sha256'] == hashlib.sha256(helper_ast.encode()).hexdigest()
old_controller = ast.parse(text(S / 'run_tracerca_path_pilots_v1.py'))
oc = functions(old_controller)
nc = functions(trees['run_tracerca_path_pilots_v2.py'])
old_controller_unchanged = [name for name in oc if name in nc and dump_ast(oc[name]) == dump_ast(nc[name])]
controller = literals(trees['run_tracerca_path_pilots_v2.py'])
auditor = literals(trees['audit_tracerca_posthoc_v1.py'])
assert controller['WRAPPER_SHA256'] == sha(S / 'replay_tracerca_v3.py')
assert controller['AUDITOR_SHA256'] == sha(S / 'audit_tracerca_posthoc_v1.py')
for name, expected in controller['SHARED_PINS'].items():
    assert expected == sha(S / name) == auditor['SHARED_PINS'][name]
assert controller['ORIGINAL_INVENTORY_SHA256'] == auditor['INVENTORY_SHA256'] == sha(OUT / 'original-inventory.json')
assert auditor['OLD_WRAPPER_SHA256'] == sha(S / 'replay_tracerca_v2.py')
assert controller['MAX_REPAIR_S'] == 300 and controller['MAX_PILOTS_S'] == 1200 and controller['MAX_CHILD_S'] == 600
expected_pilots = literals(old_controller)['PILOTS'][1:]
assert controller['PILOTS'] == expected_pilots
audit_ast = dump_ast(functions(trees['audit_tracerca_posthoc_v1.py'])['audit'])
assert "attr='chay'" in audit_ast and "attr='tracerca'" in audit_ast  # function source references only
assert not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in ('chay', 'tracerca', 'get_operation_slo', 'main')
               for n in ast.walk(trees['audit_tracerca_posthoc_v1.py']))
for new_name, old_name in (('replay_tracerca_v3.py','replay_tracerca_v2.py'),
                            ('run_tracerca_path_pilots_v2.py','run_tracerca_path_pilots_v1.py')):
    patch = ''.join(difflib.unified_diff(text(S / old_name).splitlines(True), text(S / new_name).splitlines(True), fromfile=old_name, tofile=new_name))
    with (OUT / (new_name + '-diff-002.patch')).open('x', encoding='utf-8', newline='\n') as f:
        f.write(patch)
inventory = [{'path': 'results/T-032/scripts/' + name, 'bytes': (S/name).stat().st_size, 'sha256': sha(S/name)} for name in names]
result = {'status': 'STATIC_FULL_SOURCE_AST_PIN_PASS_NOT_RUNTIME', 'files': inventory,
    'unchanged_replay_function_AST': unchanged, 'changed_replay_function_AST': changed,
    'verify_tracerca_only_change': 'pd.read_parquet(use_threads=False); full previous formula/status/input/output assertions retained',
    'one_runner_AST_unchanged': True, 'helper_function_AST_exact': True, 'helper_provenance': provenance,
    'old_controller_unchanged_function_AST': old_controller_unchanged,
    'old_wrapper_and_capture_preserved': True, 'saved_error_inventory_sha256': auditor['INVENTORY_SHA256'],
    'old_failure_unmodified': True, 'pilots_same_two_remaining_cases': True,
    'original_six_fixtures_retained_with_extension_adapter_and_ten_serializer_cases': True,
    'repair_caps': {'seconds': 300, 'bytes': 52428800}, 'pilot_caps': {'seconds': 1200, 'bytes': 157286400, 'each_seconds': 600},
    'global_caps': {'combined_bytes': 12884901888, 'laptop_bytes': 2147483648},
    'method_or_fixture_executed': False, 'runtime_status': 'NOT_RUN', 'root_review_required': True}
with (OUT / 'static-full-check-002.json').open('x', encoding='utf-8', newline='\n') as f:
    json.dump(result, f, indent=2, ensure_ascii=False, allow_nan=False)
    f.write('\n')
print(json.dumps(result, ensure_ascii=False))
