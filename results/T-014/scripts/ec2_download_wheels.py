"""Save exact compatible pinned wheels, verified against PyPI SHA256 metadata."""
import urllib.request,json,hashlib,time,re
from pathlib import Path
base=Path('/home/ubuntu/rca/T-014');dest=base/'wheels';dest.mkdir(exist_ok=True)
records=[];total=0
for line in (base/'requirements-followup.txt').read_text().splitlines():
    name,version=line.split('==');url=f'https://pypi.org/pypi/{name}/{version}/json'
    meta_path=dest/f'{name}-{version}.metadata.json'
    meta=meta_path.read_bytes() if meta_path.exists() else urllib.request.urlopen(url).read()
    meta_path.write_bytes(meta)
    choices=[]
    for r in json.loads(meta)['urls']:
        fn=r['filename']
        if not fn.endswith('.whl'):continue
        if fn.endswith('none-any.whl') and ('-py3-' in fn or '-py2.py3-' in fn):choices.append(r)
        elif '-cp312-cp312-' in fn and 'manylinux' in fn and fn.endswith('x86_64.whl'):choices.append(r)
        elif re.search(r'-cp3(?:[6-9]|1[0-2])-abi3-',fn) and 'manylinux' in fn and fn.endswith('x86_64.whl'):choices.append(r)
    if not choices:raise RuntimeError(f'No permitted cp312 Linux wheel: {name}=={version}')
    row=sorted(choices,key=lambda x:x['filename'])[0];total+=row['size']+len(meta)
    if total>250_000_000:raise RuntimeError('Predeclared250MB followup download bound exceeded')
    record=dict(package=name,version=version,url=row['url'],filename=row['filename'],expected_bytes=row['size'],expected_sha256=row['digests']['sha256'])
    with (base/'runs/setup-ec2-2/download-progress.jsonl').open('a') as f:f.write(json.dumps(dict(event='before_download',**record))+'\n')
    wheel_path=dest/row['filename'];reused=wheel_path.exists()
    payload=wheel_path.read_bytes() if reused else urllib.request.urlopen(row['url']).read();actual=hashlib.sha256(payload).hexdigest()
    assert len(payload)==row['size'] and actual==row['digests']['sha256']
    wheel_path.write_bytes(payload);record.update(actual_bytes=len(payload),sha256=actual,reused_verified_payload=reused);records.append(record)
    print(json.dumps(record),flush=True)
(base/'runs/setup-ec2-2/downloads.json').write_text(json.dumps(dict(wheels=records,payload_and_metadata_bytes=total,limit_bytes=250_000_000),indent=2))
