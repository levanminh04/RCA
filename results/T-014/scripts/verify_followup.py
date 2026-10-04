"""Check terminal evidence and copyback hashes without rerunning methods."""
import json,hashlib,csv,ast
from pathlib import Path
out=Path('D:/RCA-flashticket/results/T-014');checks=[]
def ck(name,value):checks.append(dict(name=name,pass_=bool(value)));assert value,name
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
cost=load(out/'runs/followup-cost.json');ck('aggregate active budget plus reservation <=3h',cost['under_limit'] and cost['total_with_reservation_seconds']<=10800)
env=load(out/'runs/environment-ec2-2.json');oldenv=load(out/'runs/environment.json')
ck('eight core algorithm packages same as primary',all(env['packages'][p]==v for p,v in oldenv['packages'].items()))
ck('source/data preflight hashes all pass',all(load(out/'runs/ec2-2-preflight-check.json').values()))
records=list(csv.DictReader((out/'runs/external-files-ec2-2.csv').open(encoding='utf-8-sig',newline='')))
hashes={r['path']:r['sha256'] for r in records}
for mode in ['permuted','normal']:
    dest=out/'runs'/('ec2-2-'+mode);status=load(dest/'status.json');ck(mode+' terminal returncode present','returncode' in status)
    ck(mode+' actual worker was started',status['active_wall_seconds']>0 and (dest/'input.json').exists())
    for p in dest.glob('*'):
        if p.is_file() and p.name not in ['comparison.json','rank-summary.json']:
            remote='/home/ubuntu/rca/T-014/runs/'+dest.name+'/'+p.name
            ck(mode+' copyback '+p.name,hashlib.sha256(p.read_bytes()).hexdigest()==hashes[remote])
    inp=load(dest/'input.json')
    if mode=='normal':ck('normal PC input and scoring current predate real injection',inp['pc_last']<inp['true_inject_time'] and inp['current']<inp['true_inject_time'])
    if status['complete']:
        c=load(dest/'comparison.json');ck(mode+' evidence comparison status',c['direct_rht_matches_snapshot'] if mode=='permuted' else c['official_same_host_repeat_exact'] and not c['direct_rht_matches_snapshot'] and len(c['cross_platform_mismatch']['diff'])==4)
        for stage,file in [('score','comparison.json'),('raw','window-comparison.json')]:ck(mode+' independent '+stage,load((out/'runs/normal-official-independent-linux/comparison.json' if mode=='normal' and stage=='score' else out/'paper/followup-normal-official-raw/window-comparison.json' if mode=='normal' else out/'paper'/('followup-'+mode+'-'+stage)/file))['pass'])
    else:ck(mode+' failure or timeout retained',(dest/'error.json').exists() or status.get('timeout',False) or status['returncode']!=0)
ck('factor diagnosis independent check',load(out/'audit/graph-factor-verification.json')['pass_'])
ck('controlled orientation-order mechanism independently replayed',load(out/'paper/orientation-order-fixture.json')['only_node_order_changed'] and load(out/'paper/orientation-order-fixture.json')['forward']['independent_rule_matches'] and load(out/'paper/orientation-order-fixture.json')['reverse']['independent_rule_matches'])
for p in (out/'scripts').glob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'))
report=dict(pass_=all(c['pass_'] for c in checks),checks=checks,count=len(checks),scope='Evidence integrity and independent calculations; this does not mark a failed scientific control as passed.')
(out/'runs/followup-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(dict(pass_=report['pass_'],count=len(checks))))
