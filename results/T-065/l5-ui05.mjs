import fs from 'node:fs/promises';
import crypto from 'node:crypto';
const base='results/T-065', out=base+'/kiem/003-trinh-duyet';
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const dir=base+'/grafana-l5/ui05';
await fs.mkdir(dir,{recursive:true});
const source=base+'/l4-dashboard.mjs', sourceBytes=await fs.readFile(source);
const oldCall='page(replay?UID:REPLAY)', newCall="page(replay?UID:REPLAY,'${ca}','${dv}','${op}','${__from}','${__to}')";
if(sourceBytes.toString().split(oldCall).length!==2)throw Error('Source differs');
await fs.writeFile(dir+'/l4-dashboard-truoc-ui05.mjs',sourceBytes,{flag:'wx'});
await fs.writeFile(source,sourceBytes.toString().replace(oldCall,newCall));
const plan=[];
for(const uid of ['t065-l4-rca','t065-l4-phat-lai']){
 const file=base+'/grafana-l4/'+uid+'.json', before=await fs.readFile(file), d=JSON.parse(before);
 const panel=d.panels.find(p=>p.id===1), old=panel.options.content;
 if(!old.includes('from=${t_tu}&to=${t_den}'))throw Error('Header differs');
 panel.options.content=old.replace('from=${t_tu}&to=${t_den}','from=${__from}&to=${__to}');
 const after=Buffer.from(JSON.stringify(d,null,2)+'\n');
 await fs.writeFile(dir+'/'+uid+'-truoc.json',before,{flag:'wx'});
 await fs.writeFile(dir+'/'+uid+'.json',after,{flag:'wx'});
 await fs.writeFile(file,after);
 const prior=JSON.parse(before); panel.options.content=old;
 if(JSON.stringify(d)!==JSON.stringify(prior))throw Error('Other dashboard field changed');
 plan.push({uid,path:'/opt/flash-ticket-obs/pinned/provisioning/dashboards/RCA FlashTicket/1 · Kết quả hiện hành/'+uid+'.json',before:sha(before),after:sha(after),data:after.toString('base64')});
}
const payload=Buffer.from(JSON.stringify(plan)).toString('base64');
const script=`import pathlib,json,hashlib,base64,datetime
P=json.loads(base64.b64decode('${payload}'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
assert not (pathlib.Path.home()/'rca-dieu-phoi/STOP').exists(), 'STOP remote'
B=pathlib.Path('/opt/flash-ticket-obs/rca-ket-qua/t065-l4-001/rollback/l5-ui05')
assert not B.exists(), 'Backup already exists'
for e in P:
 p=pathlib.Path(e['path']); assert sha(p)==e['before'], 'Before hash changed'
 raw=base64.b64decode(e['data']); assert hashlib.sha256(raw).hexdigest()==e['after']; assert json.loads(raw)['uid']==e['uid']
B.mkdir(parents=True)
for e in P:
 assert not (pathlib.Path.home()/'rca-dieu-phoi/STOP').exists(), 'STOP remote'
 p=pathlib.Path(e['path']); (B/p.name).write_bytes(p.read_bytes()); t=p.with_suffix('.ui05.tmp'); t.write_bytes(base64.b64decode(e['data'])); t.replace(p)
 print(json.dumps({'utc':utc(),'uid':e['uid'],'path':str(p),'before':e['before'],'after':sha(p),'backup':str(B/p.name)}),flush=True)
`;
await fs.writeFile(base+'/l5-ui05-deploy.py',script);
await fs.writeFile(out+'/ui05-plan.json',JSON.stringify({utc:new Date().toISOString(),reason:'Header navigation before hidden time variables load emitted from=&to=; use current dashboard time for round trips.',source:{before:sha(sourceBytes),after:sha(await fs.readFile(source))},changes:plan.map(({data,...x})=>x),other_fields_unchanged:true,targets_unchanged:true},null,2)+'\n');
console.log(JSON.stringify({dashboards:plan.length,targets_unchanged:true}));
