import fs from 'node:fs/promises';
import crypto from 'node:crypto';

const base='results/T-065';
const prefix=(await fs.readFile(base+'/l5-obs.py','utf8')).split("if sys.argv[1]=='inventory'")[0];
const dashboardDir='/opt/flash-ticket-obs/pinned/provisioning/dashboards/RCA FlashTicket/1 · Kết quả hiện hành';
const hash=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
const payload=[];
for(const uid of ['t065-l4-rca','t065-l4-phat-lai']){
 const before=await fs.readFile(base+'/grafana-l4/'+uid+'.json');
 const after=await fs.readFile(base+'/grafana-l5/ui04/'+uid+'.json');
 if(JSON.parse(after).uid!==uid)throw Error('UID khác '+uid);
 payload.push({uid,path:dashboardDir+'/'+uid+'.json',before:hash(before),after:hash(after),data:after.toString('base64')});
}
const data=Buffer.from(JSON.stringify(payload)).toString('base64');
const script=prefix+String.raw`
P=json.loads(base64.b64decode("${data}"))
assert not (pathlib.Path.home()/"rca-dieu-phoi/STOP").exists(), "STOP"
backup=pathlib.Path("/opt/flash-ticket-obs/rca-ket-qua/t065-l4-001/rollback/l5-ui04")
assert not backup.exists(), "Backup exists, check prior deployment before retry"
for entry in P:
    target=pathlib.Path(entry["path"])
    assert sha(target)==entry["before"], "Before hash changed"
    new=base64.b64decode(entry["data"])
    assert hashlib.sha256(new).hexdigest()==entry["after"]
    assert json.loads(new)["uid"]==entry["uid"]
backup.mkdir(parents=True)
original={}
for entry in P:
    target=pathlib.Path(entry["path"])
    original[target]=target.read_bytes()
    (backup/target.name).write_bytes(original[target])
changed=[]
try:
    for entry in P:
        assert not (pathlib.Path.home()/"rca-dieu-phoi/STOP").exists(), "STOP"
        target=pathlib.Path(entry["path"])
        temporary=target.with_suffix(".l5.tmp")
        temporary.write_bytes(base64.b64decode(entry["data"]))
        temporary.replace(target)
        changed.append(target)
        assert sha(target)==entry["after"]
        print(json.dumps({"utc":utc(),"path":str(target),"uid":entry["uid"],"before":entry["before"],"after":entry["after"],"backup":str(backup/target.name)},ensure_ascii=False),flush=True)
except BaseException:
    for target in changed:
        temporary=target.with_suffix(".l5.tmp")
        temporary.write_bytes(original[target])
        temporary.replace(target)
    raise
`;
await fs.writeFile(base+'/l5-ui-deploy.py',script);
await fs.writeFile(base+'/kiem/003-trinh-duyet/ui04-deploy-plan.json',JSON.stringify(payload.map(({data,...entry})=>entry),null,2)+'\n');
console.log(JSON.stringify({files:payload.length}));
