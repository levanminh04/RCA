import sys,time
from pathlib import Path
sys.path.insert(0, 'D:\\RCA-flashticket\\results\\T-054\\scripts')
from bien_nhan import *
j=read_pin(ref(sys.argv[1]));a=Path(sys.argv[2]);token=sys.argv[3];s=j['slot']
if j['fixture_route']=='torai_prep':
 p=a/'fake.csv';p.write_text('x\n1\n',encoding='utf-8')
 atomic(a/'prepared.json',dict(schema='T054-PREP-1',token=token,slot_sha256=fingerprint(s),tables={'fake':ref(p)}))
else:
 inv=dict(schema='T054-INVOKE-1',slot_sha256=fingerprint(s),token=token,normalized_input_sha256='e'*64,
          **{k:s[k]for k in ['config_sha256','source_sha256','environment_sha256','window','seed']},prepared_ref=j['prepared'])
 atomic(a/'invocation.json',inv)
 append(a/'phases.jsonl',dict(token=token,pid=__import__('os').getpid(),phase='method',state='start',invocation_sha256=fingerprint(inv)))
 time.sleep(10)
