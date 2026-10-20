"""Prepare byte-identical TraceRCA import closure and a path-only replay v2.

Standard-library metadata/copy work only. No package/method import, native
execution, dataset access, SSH, environment mutation, or fixture execution.
The original package/wrapper are retained. Every output must be new.
"""
from __future__ import annotations

import ast
import difflib
import hashlib
import json
from pathlib import Path
import subprocess

REPO = Path("D:/RCA-flashticket")
EXTERNAL = Path("D:/RCA-ext/src/RCAEval")
REVISION = "259ea4167160256a74ad30004aa3d96a998c846e"
OUTPUT = REPO / "results/T-032/runs/tracerca-path-002"
REMOTE_PARENT = "/home/ubuntu/rca/T-032/sources/rcaeval"
REMOTE_INVENTORY = "/home/ubuntu/rca/T-032/sources/tracerca-path-002-inventory.json"


def sha_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def sha(path):
    return sha_bytes(Path(path).read_bytes())


def git(*arguments):
    return subprocess.check_output(["git", "-C", str(EXTERNAL), *arguments])


def write_new(path, raw):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as target:
        target.write(raw)


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def module_name(relative):
    parts = list(Path(relative).parts)
    if parts[-1] == "__init__.py":
        parts.pop()
    else:
        parts[-1] = Path(parts[-1]).stem
    return ".".join(parts)


def source_closure():
    assert git("rev-parse", "HEAD").decode().strip() == REVISION
    tracked = git("ls-tree", "-r", "--name-only", REVISION, "RCAEval").decode().splitlines()
    candidates = [relative for relative in tracked if relative.endswith(".py")
                  and not any(part.lower() in ("test", "tests", "__pycache__")
                              for part in Path(relative).parts)
                  and not Path(relative).name.lower().startswith("test_")]
    modules = {module_name(relative): relative for relative in candidates}
    parsed = {}
    pending, visited = ["RCAEval.e2e.tracerca"], set()
    while pending:
        name = pending.pop()
        if name in visited or name not in modules:
            continue
        visited.add(name)
        relative = modules[name]
        source = EXTERNAL / relative
        raw = source.read_bytes()
        blob = git("show", REVISION + ":" + relative)
        assert raw.replace(b"\r\n", b"\n") == blob.replace(b"\r\n", b"\n"), relative
        tree = ast.parse(raw.decode("utf-8-sig"), filename=relative)
        parsed[name] = (relative, raw, blob, tree)
        # Ancestor initializers and all statically reachable package imports.
        pending.extend(".".join(name.split(".")[:length]) for length in range(1, len(name.split("."))))
        package = name if Path(relative).name == "__init__.py" else name.rsplit(".", 1)[0]
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                pending.extend(item.name for item in node.names if item.name.startswith("RCAEval"))
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    prefix = package.split(".")[:len(package.split(".")) - node.level + 1]
                    base = ".".join(prefix + ([node.module] if node.module else []))
                else:
                    base = node.module or ""
                if base == "RCAEval" or base.startswith("RCAEval."):
                    pending.append(base)
                    pending.extend(base + "." + item.name for item in node.names if item.name != "*")
            elif isinstance(node, ast.Assign) and any(isinstance(target, ast.Name)
                    and target.id == "_METHOD_MODULES" for target in node.targets):
                menu = ast.literal_eval(node.value)
                pending.extend(name + "." + child for child in menu)
    assert "RCAEval" in visited and "RCAEval.e2e" in visited and "RCAEval.e2e.tracerca" in visited
    return parsed


def runtime_guard_source(inventory_sha):
    return '''
LOWERCASE_PARENT = Path("__REMOTE_PARENT__")
LOWERCASE_INVENTORY = Path("__REMOTE_INVENTORY__")
LOWERCASE_INVENTORY_SHA256 = "__INVENTORY_SHA__"
LOWERCASE_REVISION = "__REVISION__"


def lowercase_file(path, expected, authority, audit):
    path = Path(path)
    task_sources = Path("/home/ubuntu/rca/T-032/sources")
    if task_sources not in path.parents or path.resolve() != path or path.is_symlink():
        raise ReplayError("lowercase code/metadata escaped or redirected")
    actual = sha(path)
    audit.append({"path": str(path), "authority": authority, "expected": expected,
                  "actual": actual, "pass": actual == expected, "bytes": path.stat().st_size})
    if actual != expected:
        raise ReplayError("lowercase source/metadata hash differs: " + str(path))
    return path


def lowercase_closure(audit):
    metadata = read(lowercase_file(LOWERCASE_INVENTORY, LOWERCASE_INVENTORY_SHA256,
                                  "approved byte-identical TraceRCA lowercase closure", audit))
    if metadata.get("revision") != LOWERCASE_REVISION or metadata.get("remote_parent") != str(LOWERCASE_PARENT):
        raise ReplayError("lowercase closure revision/root changed")
    if LOWERCASE_PARENT.resolve() != LOWERCASE_PARENT or LOWERCASE_PARENT.is_symlink():
        raise ReplayError("lowercase closure root redirected")
    rows = metadata["files"]
    if len(rows) != metadata["file_count"] or sum(row["bytes"] for row in rows) != metadata["total_bytes"]:
        raise ReplayError("lowercase closure inventory count/size changed")
    if metadata["total_bytes"] > 5 * 1024 * 1024:
        raise ReplayError("lowercase closure exceeds approved 5 MiB")
    expected_modules = {}
    for row in rows:
        relative = Path(row["package_relative"])
        if (relative.is_absolute() or ".." in relative.parts or relative.parts[0] != "RCAEval"
                or relative.suffix != ".py" or row["module"] in expected_modules):
            raise ReplayError("invalid/duplicate lowercase closure row")
        path = LOWERCASE_PARENT / relative
        if path.resolve() != path or path.is_symlink():
            raise ReplayError("lowercase code redirected: " + str(path))
        lowercase_file(path, row["sha256"], "RCAEval@" + LOWERCASE_REVISION + ":" + relative.as_posix(), audit)
        if path.stat().st_size != row["bytes"]:
            raise ReplayError("lowercase source byte size differs")
        expected_modules[row["module"]] = row
    for name, module in sorted(sys.modules.items()):
        if name != "RCAEval" and not name.startswith("RCAEval."):
            continue
        row = expected_modules.get(name)
        imported_file = getattr(module, "__file__", None)
        if row is None or imported_file is None:
            raise ReplayError("unknown/namespace RCAEval import: " + name)
        path = Path(imported_file).resolve()
        allowed = LOWERCASE_PARENT / row["package_relative"]
        if path != allowed or sha(path) != row["sha256"]:
            raise ReplayError("RCAEval import fell back or changed: " + name)
        audit.append({"module": name, "path": str(path), "expected": row["sha256"],
                      "actual": sha(path), "pass": True, "authority": "lowercase closure actual import"})
    return metadata

'''.replace("__REMOTE_PARENT__", REMOTE_PARENT).replace("__REMOTE_INVENTORY__", REMOTE_INVENTORY).replace(
        "__INVENTORY_SHA__", inventory_sha).replace("__REVISION__", REVISION)


def main():
    assert not OUTPUT.exists(), "keep every prior preparation; use a new authorized output"
    original = REPO / "results/T-032/scripts/replay_tracerca.py"
    target = REPO / "results/T-032/scripts/replay_tracerca_v2.py"
    assert not target.exists(), "keep existing replay v2"
    source = original.read_bytes()
    text = source.decode("utf-8-sig")
    closure = source_closure()
    external_manifest = json.loads((REPO / "results/T-026/runs/session-005/external-code-manifest.json").read_text(encoding="utf-8-sig"))
    expected_native = external_manifest["external_source_hashes"]["D:/RCA-ext/src/RCAEval/RCAEval/e2e/tracerca.py"]
    assert sha_bytes(closure["RCAEval.e2e.tracerca"][1]) == expected_native
    rows = []
    total = sum(len(item[1]) for item in closure.values())
    assert total <= 5 * 1024 * 1024
    for name, (relative, raw, blob, tree) in sorted(closure.items()):
        destination = OUTPUT / "payload" / "rcaeval" / relative
        write_new(destination, raw)
        assert sha(destination) == sha_bytes(raw)
        rows.append({"module": name, "package_relative": relative, "bytes": len(raw),
                     "sha256": sha_bytes(raw), "revision_blob_sha256": sha_bytes(blob),
                     "canonical_LF_exact_revision": True, "original": str(EXTERNAL / relative),
                     "local_copy": str(destination), "remote": REMOTE_PARENT + "/" + relative,
                     "AST_parsed": True})
    inventory = {"schema": "T-032.tracerca-lowercase-closure.v1", "revision": REVISION,
                 "remote_parent": REMOTE_PARENT, "file_count": len(rows), "total_bytes": total,
                 "files": rows, "root": "RCAEval.e2e.tracerca",
                 "closure_rule": "ancestor initializers + conservative static imports + literal _METHOD_MODULES menu",
                 "excluded": ["tests", "data", ".git", "cache", "SSH keys"],
                 "native_source_hash_matches_T026": True, "methods_executed": False,
                 "limits": "runtime actual imports must match inventory; no fallback; canonical-LF git proof is not a historical raw-byte proof for every module"}
    inventory_raw = json_bytes(inventory)
    write_new(OUTPUT / "inventory.json", inventory_raw)
    inventory_sha = sha_bytes(inventory_raw)
    text = text.replace("def external_sources(audit):", runtime_guard_source(inventory_sha) + "\ndef external_sources(audit):", 1)
    old_path = '    allowed = Path("/home/ubuntu/rca/T-025/src") / suffix'
    assert text.count(old_path) == 1
    text = text.replace(old_path, '    allowed = LOWERCASE_PARENT / "RCAEval/e2e/tracerca.py"')
    old_import = '    path = Path(importlib.import_module(module_name).__file__).resolve()'
    assert text.count(old_import) == 1
    text = text.replace(old_import, '    closure = lowercase_closure(audit)\n' + old_import + '\n    lowercase_closure(audit)')
    text = text.replace('    return {"modules": [row], "versions": versions}',
                        '    return {"modules": [row], "versions": versions, "closure_inventory_sha256": LOWERCASE_INVENTORY_SHA256,\n'
                        '            "closure_count": closure["file_count"], "closure_revision": LOWERCASE_REVISION}')
    text = text.replace('("capture_tracerca.py", "replay_tracerca.py", "capture_microrank.py", "replay_microrank.py")',
                        '("capture_tracerca.py", "replay_tracerca_v2.py", "capture_microrank.py", "replay_microrank.py")')
    tree_before, tree_after = ast.parse(source.decode("utf-8-sig")), ast.parse(text)
    functions_before = {node.name: ast.dump(node, include_attributes=False) for node in tree_before.body if isinstance(node, ast.FunctionDef)}
    functions_after = {node.name: ast.dump(node, include_attributes=False) for node in tree_after.body if isinstance(node, ast.FunctionDef)}
    unchanged = [name for name in functions_before if name not in ("external_sources", "main")]
    assert all(functions_before[name] == functions_after[name] for name in unchanged), "unexpected observer/verification/calculation mutation"
    write_new(target, text.encode("utf-8"))
    diff = "".join(difflib.unified_diff(source.decode("utf-8-sig").splitlines(True), text.splitlines(True),
                                       fromfile="replay_tracerca.py", tofile="replay_tracerca_v2.py"))
    write_new(OUTPUT / "wrapper-diff.patch", diff.encode("utf-8"))
    scripts = [target, REPO / "results/T-032/scripts/capture_tracerca.py",
               REPO / "results/T-032/scripts/replay_microrank.py", REPO / "results/T-032/scripts/capture_microrank.py"]
    receipt = {"status": "LOCAL_PREPARED_NO_RUNTIME_TEST", "original_wrapper_preserved": sha(original) == sha_bytes(source),
               "capture_unchanged": True, "method_bytes_changed": False, "native_or_fixture_executed": False,
               "closure_count": len(rows), "closure_bytes": total, "inventory_sha256": inventory_sha,
               "unchanged_function_AST": unchanged, "only_changed_original_functions": ["external_sources", "main"],
               "scripts": [{"path": str(path), "bytes": path.stat().st_size, "sha256": sha(path)} for path in scripts],
               "next_checks": "root review, transfer/hash both ends, fixtures and three approved guarded pilots",
               "known_unmodified_issue": "shared replay_microrank.table_columns has numpy dtype restoration; RE2 extension string/Int64 may require a separate implementation fix before pilot"}
    write_new(OUTPUT / "self-check.json", json_bytes(receipt))
    print(json.dumps({"status": receipt["status"], "closure_count": len(rows), "closure_bytes": total,
                      "inventory_sha256": inventory_sha, "wrapper_sha256": sha(target)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
