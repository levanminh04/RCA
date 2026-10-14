"""Read only the authenticated retained SimpleRCA metadata, no method call."""
import collections
import json
from pathlib import Path
import replay_simplerca as r

run = Path('/home/ubuntu/rca/T-032/runs/simplerca-re2-first-001')
summary_path = run/'capture/capture.json'
if r.sha(summary_path) != '119183c17dcb2f1a5d60df47d7cc35e1f0e028a179ccbb32fc0ed2a3e51779c2':
    raise r.ReplayError('capture summary changed')
summary = r.read(summary_path)
hashes = {row['path']:row for row in summary['artifacts']}
tables = {}
def collect(value):
    if isinstance(value,dict):
        if {'path','rows','columns','index_levels'} <= set(value):
            if value['path'] in tables and tables[value['path']]!=value:
                raise r.ReplayError('conflicting table metadata')
            tables[value['path']] = value
        for child in value.values():
            collect(child)
    elif isinstance(value,list):
        for child in value:
            collect(child)
for call in summary['calls']:
    row=hashes[call['path']]
    path=run/'capture'/call['path']
    if r.sha(path)!=row['sha256'] or path.stat().st_size!=row['bytes']:
        raise r.ReplayError('call metadata changed')
    collect(r.read(path))
types=collections.Counter((column['dtype'],column['encoding']) for table in tables.values() for column in table['columns'])
print(json.dumps({'n_tables':len(tables),'dtype_encoding_counts':[{ 'dtype':d,'encoding':e,'columns':n} for (d,e),n in sorted(types.items())]},indent=2))
