"""Read the eight declared SS indicators and compare to their actual logs."""
import csv,hashlib,json
from pathlib import Path
from collections import defaultdict
import pyarrow.parquet as pq
BASE=Path(__file__).resolve().parent; REPO=BASE.parents[2]; DATA=REPO/'data/T-019'
TREE=json.loads((REPO/'results/T-002/public-metadata/run-002/hf-tree.json').read_text(encoding='utf-8'))
labels=[e for e in TREE if e['type']=='file' and e['path'].startswith('re3ss_') and e['path'].endswith('/root_cause.txt')]
assert len(labels)==8
out=[]; hashes=defaultdict(list)
for entry in labels:
    case=entry['path'].split('/')[0]; p=DATA/entry['path']; b=p.read_bytes()
    sha256=hashlib.sha256(b).hexdigest(); oid=hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()
    assert len(b)==entry['size'] and oid==entry['oid']
    rows=list(csv.reader(b.decode('utf-8').splitlines())); assert len(rows)==1 and len(rows[0])==6
    short,ns,service,message,pod,host=rows[0]; epoch=int(ns)//1000000000
    t=pq.read_table(DATA/case/'logs.parquet'); logrows=t.to_pylist(); ts=[r['timestamp'] for r in logrows if r['timestamp'] is not None]
    inj=int((DATA/case/'inject_time.txt').read_text().strip())
    payload=[r for r in logrows if r['container_name']==service and r['message']==message]
    exact=[r for r in payload if r['timestamp']==epoch]
    item=dict(case=case,path=entry['path'],bytes=len(b),sha256=sha256,git_blob_oid=oid,hash_matches_tree=True,rows=1,fields=6,raw_fields=dict(short_time=short,timestamp_ns=int(ns),service=service,message=message,pod=pod,host=host),indicator_kind='warning HTTP method unsupported' if service=='carts' else 'HTTP 500 access log',has_source_code_line=False,has_stack_trace=False,has_trace_id_like_payload=service=='carts',timestamp_epoch_floor=epoch,inject_time=inj,offset_seconds=epoch-inj,log_rows=t.num_rows,log_time_min=min(ts),log_time_max=max(ts),indicator_time_in_log_window=min(ts)<=epoch<=max(ts),service_message_matches=len(payload),service_message_timestamp_exact_matches=len(exact),payload_match_time_min=min([r['timestamp'] for r in payload],default=None),payload_match_time_max=max([r['timestamp'] for r in payload],default=None))
    item['payload_match_timestamps']=[r['timestamp'] for r in payload]
    item['payload_timestamp_minus_indicator_floor_seconds']=[r['timestamp']-epoch for r in payload]
    out.append(item); hashes[sha256].append(case)
result=dict(n_files=len(out),n_unique_file_hashes=len(hashes),duplicate_groups=[v for v in hashes.values() if len(v)>1],entries=out,limitations='Nhãn do tác giả chỉ một dòng triệu chứng, không chứng minh dòng sửa code hay causal root. Same message nhiều lần không đủ mapping từng request. Không có trace phát hành để ghép ID.')
(BASE/'label-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(n_files=len(out),n_unique_file_hashes=len(hashes),duplicate_groups=result['duplicate_groups'],counterparts=[{k:e[k] for k in ['case','offset_seconds','indicator_time_in_log_window','service_message_matches','service_message_timestamp_exact_matches']} for e in out]),ensure_ascii=False,indent=2))
