"""Approved two-column owner inventory only. No time, signals or per-case output."""
from pathlib import Path
import concurrent.futures
import hashlib
import io
import json
import ssl
import struct
import threading
import urllib.request

import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
evidence_path = ROOT/'results/T-054/runs/phan-xu-truoc-g3-007/bang-chung.json'
manifest = json.loads((ROOT/'results/T-054/manifest-phan-xu-truoc-g3-007.json').read_text(encoding='utf-8'))
assert hashlib.sha256(evidence_path.read_bytes()).hexdigest() == manifest['outputs'][str(evidence_path.relative_to(ROOT)).replace('\\','/')]['sha256']
rows = json.loads(evidence_path.read_text(encoding='utf-8'))['RE3']['metadata_requests']
selected = [(r, 'serviceName' if r['path'].endswith('/traces.parquet') else 'container_name')
            for r in rows if r['path'].endswith(('/traces.parquet', '/logs.parquet'))]
assert len(selected) == 60
ctx = ssl.create_default_context()
certs = []
for store in ('ROOT', 'CA'):
    for cert, encoding, trust in ssl.enum_certificates(store):
        if encoding == 'x509_asn' and (trust is True or '1.3.6.1.5.5.7.3.1' in trust):
            certs.append(ssl.DER_cert_to_PEM_cert(cert))
ctx.load_verify_locations(cadata='\n'.join(certs))
lock = threading.Lock()
budget = {'limit': 16*1024**2, 'reserved': 0, 'received': 0}
receipts, failures = [], []
global_names = {'serviceName': set(), 'container_name': set()}
completed = []


def fetch(row, start, end, purpose):
    n = end-start+1
    with lock:
        if budget['reserved']+n > budget['limit']:
            raise ValueError('approved16MiB budget would be exceeded; stopped before request')
        budget['reserved'] += n
    url = 'https://huggingface.co/datasets/phamquiluan/RCAEval/resolve/'+row['revision']+'/'+row['path']
    request = urllib.request.Request(url, headers={'Range': f'bytes={start}-{end}', 'Accept-Encoding': 'identity'})
    with urllib.request.urlopen(request, context=ctx, timeout=30) as response:
        assert response.status == 206, 'refuse entire-file response'
        assert response.headers.get('Content-Range') == f'bytes {start}-{end}/{row["size"]}'
        body = response.read(n+1)
        assert len(body) == n
        receipt = {'path':row['path'], 'revision':row['revision'], 'range':[start,end], 'bytes':n,
                   'purpose':purpose, 'sha256':hashlib.sha256(body).hexdigest(), 'etag':response.headers.get('ETag')}
        with lock:
            receipts.append(receipt); budget['received'] += n
        return body


def inspect(item):
    row, column = item
    assert column in ('serviceName', 'container_name')
    footer_start = row['size']-row['footer_bytes']-8
    footer = fetch(row, footer_start, row['size']-1, 'footer_schema_metadata')
    assert footer[-4:] == b'PAR1' and struct.unpack('<L', footer[-8:-4])[0] == row['footer_bytes']
    assert hashlib.sha256(footer[:-8]).hexdigest() == row['footer_sha256'], 'pinned007 footer changed'
    metadata = pq.ParquetFile(io.BytesIO(b'PAR1'+footer)).metadata
    index = next(i for i in range(metadata.num_columns) if metadata.schema.column(i).path == column)
    # No .statistics reads; no data page from another column is requested.
    sparse = bytearray(row['size'])
    sparse[:4], sparse[footer_start:] = b'PAR1', footer
    for group in range(metadata.num_row_groups):
        chunk = metadata.row_group(group).column(index)
        offsets = [x for x in (chunk.dictionary_page_offset, chunk.data_page_offset) if x is not None and x > 0]
        start = min(offsets); end = start+chunk.total_compressed_size-1
        assert start >= 4 and end < footer_start
        sparse[start:end+1] = fetch(row, start, end, 'authorized_owner_column:'+column)
    # Other columns consist of zeros, and cannot be decoded as a fallback.
    table = pq.read_table(pa.BufferReader(sparse), columns=[column], pre_buffer=False, use_threads=False)
    assert table.column_names == [column]
    names = {x for x in table.column(0).to_pylist() if x is not None}
    assert all(isinstance(x, str) and x for x in names)
    with lock:
        global_names[column].update(names)
        completed.append({'path':row['path'], 'column':column})
    return column


def checkpoint():
    result = {'schema':'T054-RE3-OWNER-INVENTORY-011', 'status':'COMPLETE' if len(completed)==60 and not failures else 'PARTIAL',
              'authorization':'Minh: Duyệt đọc hai cột như metadata inventory',
              'scope':'only global union of serviceName and container_name; no per-case names/counts/distributions',
              'owners':{k:sorted(v) for k,v in global_names.items()},
              'union':sorted(set.union(*global_names.values())),
              'completed_column_reads':completed, 'requests':receipts, 'budget':budget, 'failures':failures,
              'measured_signals_or_times_read':False, 'methods_run':False, 'raw_pages_or_owner_rows_saved':False}
    (RUN/'inventory-owner-global.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    tasks = {pool.submit(inspect, item):item[0]['path'] for item in selected}
    for future in concurrent.futures.as_completed(tasks):
        try:
            future.result()
        except Exception as exc:
            failures.append({'path':tasks[future], 'error':repr(exc)})
        checkpoint()
        print(json.dumps({'completed_columns':len(completed),'failures':len(failures),'bytes':budget['received']}),flush=True)
checkpoint()
if failures:
    raise SystemExit('Owner metadata incomplete; preserve receipt and stop')
print(json.dumps({'PASS':True,'global_owner_union':sorted(set.union(*global_names.values())),
                  'bytes':budget['received'],'signals_or_time_read':False}),flush=True)
