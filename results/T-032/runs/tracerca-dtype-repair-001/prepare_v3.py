"""Metadata-only preparation of the approved TraceRCA verifier correction."""
from pathlib import Path
import ast
import hashlib
import json

ROOT = Path(__file__).resolve().parents[4]
S = ROOT / 'results/T-032/scripts'
OUT = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def function(text, name):
    tree = ast.parse(text)
    node = next(n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name)
    return ast.get_source_segment(text, node), ast.dump(node, include_attributes=False)

old = (S / 'replay_tracerca_v2.py').read_text(encoding='utf-8-sig')
helper_source = (S / 'replay_circa_v2.py').read_text(encoding='utf-8-sig')
helper, helper_ast = function(helper_source, 'table_columns')
new = old.replace('compare_records, decode, table_columns, verify_capture,', 'compare_records, decode, verify_capture,')
new = new.replace('\ndef source_for(', '\nTABLE_COLUMNS_PROVENANCE = ' + repr({
    'source': 'replay_circa_v2.py', 'source_sha256': sha(S / 'replay_circa_v2.py'),
    'function': 'table_columns', 'function_ast_sha256': hashlib.sha256(helper_ast.encode()).hexdigest(),
    'logical_dtype_only': True, 'string_storage_backend_identity': 'not historically recorded; OPEN',
}) + '\n\n' + helper + '\n\n\ndef source_for(', 1)
new = new.replace('storage = pd.read_parquet(directory / relative)', 'storage = pd.read_parquet(directory / relative, use_threads=False)')
new = new.replace('"replay_tracerca_v2.py"', '"replay_tracerca_v3.py"')
new = new.replace('"source_repo": str(REPO)})', '"source_repo": str(REPO), "table_columns_provenance": TABLE_COLUMNS_PROVENANCE})')
new = new.replace('    return frame, 100\n', '''    if name == "adapter_extension_tables":
        for column in ("serviceName", "methodName", "operationName", "traceID", "spanID", "parentSpanID"):
            frame[column] = frame[column].astype("string")
        for column in ("startTime", "duration"):
            frame[column] = frame[column].astype("Int64")
        frame["unused_boolean"] = pd.array([True, False, pd.NA, None] * (len(frame) // 4 + 1), dtype="boolean")[:len(frame)]
        frame["unused_float"] = pd.array([1.25, -0.0, pd.NA, None] * (len(frame) // 4 + 1), dtype="Float64")[:len(frame)]
        frame["unused_object"] = pd.Series([None, pd.NA, float("nan"), "kept"] * (len(frame) // 4 + 1), dtype="object").iloc[:len(frame)].to_numpy()
    return frame, 100
''')
new = new.replace('    checks = []\n    for name in ("scalar",', '    serializer_checks = serializer_table_fixtures(directory)\n    checks = []\n    for name in ("scalar",', 1)
new = new.replace('"new_operation_error", "mapping_collision_error"):', '"new_operation_error", "mapping_collision_error", "adapter_extension_tables"):', 1)
new = new.replace('if name == "scalar":\n            counts', 'if name in ("scalar", "adapter_extension_tables"):\n            counts', 1)
new = new.replace('"fixtures": checks,\n', '"fixtures": checks, "serializer_fixtures": serializer_checks,\n')
new = new.replace('\ndef main():', '\n' + (OUT / 'serializer_fixture.fragment.txt').read_text(encoding='utf-8-sig') + '\n\ndef main():', 1)
assert new != old
target = S / 'replay_tracerca_v3.py'
assert not target.exists()
target.write_text(new, encoding='utf-8', newline='\n')
old_tree, new_tree = ast.parse(old), ast.parse(new)
old_f = {n.name: ast.dump(n, include_attributes=False) for n in old_tree.body if isinstance(n, ast.FunctionDef)}
new_f = {n.name: ast.dump(n, include_attributes=False) for n in new_tree.body if isinstance(n, ast.FunctionDef)}
unchanged = [k for k in old_f if old_f[k] == new_f[k]]
changed = [k for k in old_f if old_f[k] != new_f[k]]
assert changed == ['verify_tracerca', 'fixture_data', 'fixtures', 'main'], changed
assert function(new, 'table_columns')[1] == helper_ast
with (OUT / 'v3-ast-receipt.json').open('x', encoding='utf-8') as f:
    json.dump({'status': 'AST_ONLY_NO_RUNTIME', 'original_sha256': sha(S / 'replay_tracerca_v2.py'),
        'new_sha256': sha(target), 'helper_provenance': eval(new.split('TABLE_COLUMNS_PROVENANCE = ',1)[1].split('\n',1)[0]),
        'unchanged_function_ast': unchanged, 'changed_function_ast': changed,
        'native_or_fixture_executed': False, 'root_review_required': True}, f, indent=2)
    f.write('\n')
print('V3_AST_PREPARATION_PASS')
