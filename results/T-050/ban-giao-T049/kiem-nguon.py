"""Kiểm hồ sơ T-049 theo đúng mốc trước khi ghi quyết định T-050."""

import importlib.util
import json
from pathlib import Path


def main():
    folder = Path(__file__).resolve().parent
    root = folder.parents[2]
    handoff = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    assert handoff['schema'] == 'T050-ban-giao-T049-v1'
    script = root / 'results/T-049/scripts/dong_ho_so.py'
    spec = importlib.util.spec_from_file_location('kiem_ho_so_t049', script)
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)

    verify = checker.verify
    source = handoff['source_manifest']
    verify(source['path'], source)
    previous_spec = handoff['previous_T050_SPEC']
    verify(previous_spec['path'], previous_spec)
    history = handoff['historical_current_sources']
    assert set(history) == {'docs/STATE.md', 'docs/WHY.md', 'docs/DECISIONS.md'}

    def verify_at_handoff(name, expected, actual=None, prefix=False):
        if actual is None and name in history and not prefix:
            snapshot = history[name]
            assert all(snapshot[key] == expected[key] for key in ('bytes', 'sha256'))
            actual = snapshot['path']
        verify(name, expected, actual=actual, prefix=prefix)

    checker.verify = verify_at_handoff
    checker.check_final()


if __name__ == '__main__':
    main()
