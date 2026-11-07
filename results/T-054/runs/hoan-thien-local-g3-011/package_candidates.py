"""Create metadata/code staging packets locally; never transfer or dispatch."""
from pathlib import Path
import hashlib
import json
import sys
import tarfile

ROOT=Path(__file__).resolve().parents[4]
RUN=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'results/T-054/scripts'),str(ROOT/'src')]
from bien_nhan import digest,ref,read_pin,Blocked

def pin(path):
    v=ref(path);v['path']=Path(path).resolve().relative_to(ROOT).as_posix();return v

def save(path,value):
    with path.open('x',encoding='utf-8')as f:json.dump(value,f,ensure_ascii=False,separators=(',',':'))

protocol=json.loads((RUN/'protocol-candidate.json').read_bytes())
bundle=json.loads((RUN/'source-bundle-candidate.json').read_bytes())
code=json.loads((RUN/'current-code-pins.json').read_bytes())['files']
out=RUN/'packets';out.mkdir(exist_ok=False)
reports=[]
for host in ['ec2_1','ec2_2','local']:
    files=dict(code)
    def add(reference):
        p=Path(reference['path']);p=p if p.is_absolute()else ROOT/p
        p=p.resolve()
        assert p.is_relative_to(ROOT)and not p.is_relative_to(ROOT/'data'),p
        assert p.stat().st_size==reference['bytes']and digest(p)==reference['sha256'],p
        files[p.relative_to(ROOT).as_posix()]=pin(p)
    for name in ['protocol-candidate.json','dispatch-contract-candidate.json','placement-candidate.json',
                 'failure-policy-candidate.json','local-runtime-environments.json','preparation-authority-source.json',
                 'prepared/'+host+'-plan.json','prepared/'+host+'-authority.json']:
        add(pin(RUN/name))
    add(protocol['cohorts_source']);add(protocol['m1_contract_ref'])
    for reference in protocol['snapshots'].values():add(reference)
    plan=json.loads((RUN/'prepared'/(host+'-plan.json')).read_bytes())
    add(plan['sensitivity_decision_ref'])
    for job in plan['jobs']:
        for key in ['runtime_ref','independent_source_ref','runtime_binding_ref']:
            if key in job:add(job[key])
    policy=json.loads((RUN/'failure-policy-candidate.json').read_bytes())
    for reference in policy['code_evidence']:add(reference)
    # Deliberately omit evaluator tables, labels, raw telemetry, author-A files,
    # source bundle with private evaluator refs, and root mutable metadata.
    archive=out/(host+'-code-metadata.tar.gz')
    with tarfile.open(archive,'x:gz')as tar:
        for rel in sorted(files):tar.add(ROOT/rel,arcname=rel,recursive=False)
    with tarfile.open(archive,'r:gz')as tar:
        members=tar.getmembers();assert len(members)==len(files)
        assert {m.name for m in members}==set(files)
        for member in members:
            assert member.isfile()and not member.name.startswith('/')and '..'not in Path(member.name).parts
            data=tar.extractfile(member).read();v=files[member.name]
            assert len(data)==v['bytes']and hashlib.sha256(data).hexdigest()==v['sha256']
    receipt={'host':host,'scope':'LOCAL_STAGING_CANDIDATE_NOT_TRANSFERRED_NOT_LOCKED',
             'candidate_protocol':pin(RUN/'protocol-candidate.json'),'archive':pin(archive),'files':files,
             'archive_roundtrip':'PASS','raw_data_included':False,'evaluator_labels_included':False,
             'cloud_checked':False,'main_started':False,
             'limits':'External environments, upstream code and raw source data remain separate; current cloud must be verified before G3.'}
    save(out/(host+'-packet.json'),receipt)
    reports.append({'host':host,'files':len(files),'archive_bytes':archive.stat().st_size,'verified':'PASS'})
save(RUN/'packet-validation.json',{'PASS':True,'packets':reports,'cloud_actions':0})
print(json.dumps(reports),flush=True)
