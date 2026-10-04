"""Copy precisely the predeclared OB and three TT inputs; never copy private keys."""
import hashlib,json,pathlib,subprocess,time
ROOT=pathlib.Path(__file__).resolve().parents[3]
OUT=ROOT/'results/T-015/runs/transfer'
OUT.mkdir(parents=True,exist_ok=True)
A=['ssh','-o','ConnectTimeout=10','-o','BatchMode=yes','-i','D:/RCA-ext/keys/keys.pem','-o','UserKnownHostsFile=D:/RCA-ext/keys/known_hosts','-o','HostKeyAlias=3.104.124.160','ubuntu@13.239.30.70']
B=['ssh','-o','ConnectTimeout=10','-o','BatchMode=yes','-i','D:/RCA-ext/keys/key2.pem','-o','UserKnownHostsFile=D:/RCA-ext/work/T-015/known_hosts','ubuntu@3.26.62.217']
SCP=['scp','-i','D:/RCA-ext/keys/key2.pem','-o','UserKnownHostsFile=D:/RCA-ext/work/T-015/known_hosts']
TT=['re2tt_ts-auth-service_cpu_1','re2tt_ts-route-service_mem_1','re2tt_ts-route-service_socket_1']
ob=json.loads((ROOT/'results/T-007/runs/e1/manifest-re2ob.json').read_text(encoding='utf-8-sig'))
manifest=json.loads((ROOT/'results/T-015/manifest-inputs.json').read_text(encoding='utf-8-sig'))
expected=[]
inject_sources={}
for f in ob['files']:
    assert f['ok'] and f['case'].startswith('re2ob_') and f['file'] in ['traces.parquet','inject_time.txt']
    expected.append({'path':f['case']+'/'+f['file'],'bytes':f['thuc']['size'],'sha256':f['thuc']['sha256']})
assert len(expected)==180 and len(set(f['path'].split('/')[0] for f in expected))==90
for c in TT:
    row=next(r for r in manifest['dev_cases'] if r['case']==c)
    for f in ['traces.parquet','metrics.parquet','inject_time.txt']:
        if f in row['files']:
            metadata=row['files'][f]
            if f=='inject_time.txt':inject_sources[c]=ROOT/'data/rcaeval'/c/f
        else:
            assert f=='inject_time.txt'
            p=ROOT/'results/T-002/local-inspection/run-002/injection-metadata'/(c+'.txt')
            assert p.exists(),p
            inject_sources[c]=p
            metadata={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
        expected.append({'path':c+'/'+f,**metadata})
assert sum(r['bytes'] for r in expected)==960754806
target=OUT/'expected.json';target.write_text(json.dumps(expected,indent=2),encoding='utf-8')
def event(v):
    v['utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
    with (OUT/'progress.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(v)+'\n')
    print(json.dumps(v),flush=True)
event({'event':'start','total_bytes':sum(r['bytes'] for r in expected),'files':len(expected)})
with (OUT/'ob-source.log').open('wb') as srcerr,(OUT/'ob-target.log').open('wb') as dsterr:
    source=subprocess.Popen(A+['tar -C /home/ubuntu/rca/data/re2ob -cf - '+ ' '.join(f['path'] for f in expected[:180])],stdout=subprocess.PIPE,stderr=srcerr)
    dest=subprocess.Popen(B+['tar -C /home/ubuntu/rca/T-015/data -xf -'],stdin=source.stdout,stdout=dsterr,stderr=dsterr)
    source.stdout.close();d=dest.wait();s=source.wait()
    assert s==d==0,(s,d)
event({'event':'ob_copied','files':180})
for c in TT:
    subprocess.run(B+['mkdir -p /home/ubuntu/rca/T-015/data/'+c],check=True)
    paths=[str(ROOT/'data/rcaeval'/c/f) for f in ['traces.parquet','metrics.parquet']]
    subprocess.run(SCP+paths+['ubuntu@3.26.62.217:rca/T-015/data/'+c+'/'],check=True)
    subprocess.run(SCP+[str(inject_sources[c]),'ubuntu@3.26.62.217:rca/T-015/data/'+c+'/inject_time.txt'],check=True)
    event({'event':'tt_copied','case':c})
subprocess.run(SCP+[str(target),'ubuntu@3.26.62.217:rca/T-015/runs/setup/input-expected.json'],check=True)
event({'event':'copy_end','verify_next':'verify_inputs_ec2.py'})
