"""Inventory allowlisted raw trace schemas; no inference of synchronous waiting."""
import csv
import hashlib
import json
from pathlib import Path
import time
import pyarrow.parquet as pq

BASE = Path.home() / 'rca/T-032'
REPO = BASE / 'repo'
OUT = BASE / 'runs/trace-schema-001'

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()

def main():
    OUT.mkdir(parents=True, exist_ok=False)
    start = time.perf_counter()
    cases, schemas = [], {}
    for dataset, source, rawroot in (
        ('RE2-TT', REPO/'results/T-022/allowlist-dev.json', Path.home()/'rca/T-031/repo'),
        ('Nezha-OB', REPO/'results/T-026/allowlist-dev.json', REPO),
    ):
        al = read(source)
        for case in al['cases']:
            records = []
            for name, meta in case['files'].items():
                if meta is None:
                    continue
                rel = meta['path']
                is_trace = name == 'traces.parquet' if dataset == 'RE2-TT' else '/trace/' in rel
                if not is_trace:
                    continue
                p = Path(rel)
                assert not p.is_absolute() and '..' not in p.parts and 'locked' not in p.parts
                full = rawroot / p
                if rel not in schemas:
                    assert sha(full) == meta['sha256'], 'source trace hash changed'
                    if full.suffix == '.parquet':
                        pf = pq.ParquetFile(full)
                        fields = [{'name':f.name, 'type':str(f.type), 'nullable':f.nullable} for f in pf.schema_arrow]
                        rows = pf.metadata.num_rows
                    else:
                        with full.open(encoding='utf-8-sig', newline='') as stream:
                            fields = [{'name':name, 'type':'CSV; header only, values not inspected'}
                                      for name in next(csv.reader(stream))]
                        rows = None
                    schemas[rel] = {'path':rel, 'sha256':meta['sha256'], 'fields':fields,
                                    'rows_from_parquet_metadata':rows, 'semantics':'not inferred from names'}
                records.append(rel)
            cases.append({'dataset':dataset, 'opaque_id':case['opaque_id'], 'trace_files':records,
                          'coverage_and_wait_semantics':'OPEN; headers do not establish waiting/clock/sampling'})
    out = {'status':'PASS', 'purpose':'raw schema inventory only; not final trace capability evaluation',
           'cases':cases, 'schemas':schemas, 'script_sha256':sha(__file__), 'elapsed_s':time.perf_counter()-start,
           'source_allowlist_hashes':{str(p):sha(p) for p in (
               REPO/'results/T-022/allowlist-dev.json', REPO/'results/T-026/allowlist-dev.json')}}
    (OUT/'raw-schema.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'status':'PASS','cases':len(cases),'unique_trace_files':len(schemas),
                      'column_sets':{ds: sorted({tuple(x['name'] for x in schemas[p]['fields'])
                                               for c in cases if c['dataset']==ds for p in c['trace_files']})
                                     for ds in ('RE2-TT','Nezha-OB')}}), flush=True)

if __name__ == '__main__':
    main()
