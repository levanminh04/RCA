"""Read only the 93 previously used trace files; no detector or ranker is run."""
import argparse
import hashlib
import json
import pathlib
import time
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

ap=argparse.ArgumentParser()
ap.add_argument('--root',type=pathlib.Path,required=True)
ap.add_argument('--expected',type=pathlib.Path,required=True)
ap.add_argument('--output',type=pathlib.Path,required=True)
args=ap.parse_args()
root=args.root.resolve()
assert root==pathlib.Path.home()/'rca/T-015'
assert root in args.output.resolve().parents
assert not args.output.exists(),'Keep prior output'
assert np.__version__=='1.26.4' and pd.__version__=='2.2.3'
expected=json.loads(args.expected.read_text())
allowed_tt={'re2tt_ts-auth-service_cpu_1','re2tt_ts-route-service_mem_1','re2tt_ts-route-service_socket_1'}
inputs=[item for item in expected if pathlib.PurePosixPath(item['path']).name=='traces.parquet']
cases={pathlib.PurePosixPath(item['path']).parent.name for item in inputs}
assert len(inputs)==len(cases)==93
assert {case for case in cases if case.startswith('re2tt_')}==allowed_tt
assert sum(case.startswith('re2ob_') for case in cases)==90
started=time.monotonic()
args.output.mkdir(parents=True)
progress=(args.output/'progress.jsonl').open('x')
def emit(event,**values):
    row=dict(event=event,elapsed_observed_seconds=time.monotonic()-started,**values)
    text=json.dumps(row,allow_nan=False)
    progress.write(text+'\n');progress.flush();print(text,flush=True)
emit('start',cases=93,scope='time columns only; no ranker or labels')
results=[]
for item in sorted(inputs,key=lambda item:item['path']):
    source=root/'data'/item['path']
    assert source.resolve().is_relative_to(root/'data')
    case=source.parent.name
    marker=int((source.parent/'inject_time.txt').read_text().strip())*1000000
    assert np.isfinite(marker)
    counts={'rows':0,'window_rows':0,'invalid_time_rows':0,'window_invalid_time_rows':0}
    for batch in pq.ParquetFile(source).iter_batches(batch_size=65536,columns=['startTime','duration']):
        frame=batch.to_pandas()
        start=frame.startTime.to_numpy(dtype=float)
        duration=frame.duration.to_numpy(dtype=float)
        invalid=~np.isfinite(start)|~np.isfinite(duration)|(duration<0)
        window=(start>=marker-600000000)&(start<marker+600000000)
        counts['rows']+=len(start)
        counts['window_rows']+=int(window.sum())
        counts['invalid_time_rows']+=int(invalid.sum())
        counts['window_invalid_time_rows']+=int((invalid&window).sum())
    digest=hashlib.sha256()
    with source.open('rb') as stream:
        for block in iter(lambda:stream.read(1048576),b''):digest.update(block)
    row=dict(case=case,source=str(source),source_sha256=digest.hexdigest(),
             source_hash_matches_saved=digest.hexdigest()==item['sha256'],**counts)
    row['all_passed']=row['source_hash_matches_saved'] and row['invalid_time_rows']==0 and row['window_invalid_time_rows']==0
    results.append(row)
    emit('case_complete',**row)
summary=dict(all_passed=all(row['all_passed'] for row in results),cases=results,
             method_rerun=False,baseline_ranker_rerun=False,labels_read=False,
             scope='90 OB plus only the three TT dev files already run; raw and ±600-second windows',
             elapsed_observed_seconds=time.monotonic()-started,timing_official=False,
             versions={'numpy':np.__version__,'pandas':pd.__version__})
(args.output/'summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
emit('complete',all_passed=summary['all_passed'],cases=len(results))
progress.close()
assert summary['all_passed']
