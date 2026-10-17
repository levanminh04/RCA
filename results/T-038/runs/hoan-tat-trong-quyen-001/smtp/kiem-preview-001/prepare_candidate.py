"""Proposal only: write experimental copies and reviewable patch inside this package."""
from pathlib import Path
import hashlib
import json
import difflib

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
BASE = ROOT / 'results/T-036/runs/kiem-r1-after-002/code'
hashes = json.loads((BASE.parent / 'code-hashes.json').read_text(encoding='utf-8'))
assert (HERE / 'oracle-before-code.json').is_file()
dest = HERE / 'experimental_copy'
dest.mkdir(exist_ok=False)
rows, patches = [], []
for name in ['__init__.py', 'build.py', 'compare.py']:
    before_bytes = (BASE / name).read_bytes()
    assert hashlib.sha256(before_bytes).hexdigest() == hashes['src/do_thi_tinh/' + name]
    before = before_bytes.decode('utf-8')
    after = before
    if name == 'build.py':
        old = "CHANNELS = {'http', 'rpc', 'data', 'publish', 'consume', 'logical-message',"
        new = "CHANNELS = {'http', 'rpc', 'smtp', 'data', 'publish', 'consume', 'logical-message',"
        assert after.count(old) == 1
        after = after.replace(old, new)
        old = "channel not in {'http', 'rpc', 'internal'}"
        new = "channel not in {'http', 'rpc', 'smtp', 'internal'}"
        assert after.count(old) == 1
        after = after.replace(old, new)
    elif name == 'compare.py':
        old = "['messaging', 'queue_metric_address'])"
        new = "['messaging', 'queue_metric_address', 'channel'])"
        assert after.count(old) == 1
        after = after.replace(old, new)
        old = "        if type(row['event_count']) is not int or row['event_count'] < 0:"
        new = """        # Optional protocol evidence on a call hop; never inferred from static.
        if 'channel' in row and (row['channel'] not in {'http', 'rpc', 'smtp', 'internal'} or
                                 row['type'] not in {'gọi-đồng-bộ', 'gọi-chưa-phân-kiểu'}):
            raise ValueError('trace_channel')
        if type(row['event_count']) is not int or row['event_count'] < 0:"""
        assert after.count(old) == 1
        after = after.replace(old, new)
        old = "                    address=[channel, address] if address is not None else None,"
        new = """                    address=[channel, address] if address is not None else
                            ['smtp', None] if edge.get('channel') == 'smtp' else None,"""
        assert after.count(old) == 1
        after = after.replace(old, new)
    (dest / name).write_bytes(after.encode('utf-8'))
    rows.append(dict(source='src/do_thi_tinh/' + name,
                     base_sha256=hashlib.sha256(before_bytes).hexdigest(),
                     candidate_sha256=hashlib.sha256(after.encode('utf-8')).hexdigest()))
    if before != after:
        patches.extend(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                           fromfile='a/src/do_thi_tinh/' + name,
                                           tofile='b/src/do_thi_tinh/' + name))
(HERE / 'proposed-shared-code.patch').write_text(''.join(patches), encoding='utf-8')
(HERE / 'candidate-code-hashes.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
print('Experimental copies only; active shared source and pin unchanged.')
