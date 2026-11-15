import fs from 'node:fs/promises';
import crypto from 'node:crypto';
const base='results/T-065', dir=base+'/grafana-l5/ui06', out=base+'/kiem/003-trinh-duyet';
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const list='$$.([su_co.{"ma":ma,"nguon":nguon,"ket_luan":ket_luan,"tu":$fromMillis(tu),"den":$fromMillis(den)}])';
await fs.mkdir(dir,{recursive:true});
const source=base+'/l4-dashboard.mjs', beforeSource=await fs.readFile(source);
await fs.writeFile(dir+'/l4-dashboard-truoc-ui06.mjs',beforeSource,{flag:'wx'});
let src=beforeSource.toString();
const edits=[
 ["'$$.([{\"v\":cua_so_ms[0]}])',[['v','number']]", "'$$.([{\"v\":$fromMillis(cua_so_ms[0])}])',[['v']]"],
 ["'$$.([{\"v\":cua_so_ms[1]-1}])',[['v','number']]", "'$$.([{\"v\":$fromMillis(cua_so_ms[1]-1)}])',[['v']]"],
 ["'${__from}','${__to}'", "'${__from:date:iso}','${__to:date:iso}'"],
 ["time:old.time,", "time:Object.fromEntries(Object.entries(old.time).map(([k,v])=>[k,/^\\d+$/.test(v)?new Date(Number(v)).toISOString():v])),"],
 ["'su_co',[['ma'],['nguon'],['ket_luan'],['tu','number'],['den','number']]", JSON.stringify(list)+",[['ma'],['nguon'],['ket_luan'],['tu'],['den']]"]
];
for(const [a,b] of edits){if(src.split(a).length!==2)throw Error('Source pattern differs: '+a); src=src.replace(a,()=>b);}
await fs.writeFile(source,src);
const plan=[];
for(const uid of ['t065-l4-rca','t065-l4-phat-lai']){
 const file=base+'/grafana-l4/'+uid+'.json', before=await fs.readFile(file), d=JSON.parse(before), old=JSON.parse(before);
 for(const v of d.templating.list.filter(v=>['t_tu','t_den'].includes(v.name))){
  const q=v.query.infinityQuery;
  q.root_selector=v.name==='t_tu'?'$$.([{"v":$fromMillis(cua_so_ms[0])}])':'$$.([{"v":$fromMillis(cua_so_ms[1]-1)}])';
  q.columns[0].type='string';
 }
 d.time=Object.fromEntries(Object.entries(d.time).map(([k,v])=>[k,/^\d+$/.test(v)?new Date(Number(v)).toISOString():v]));
 const header=d.panels.find(p=>p.id===1);header.options.content=header.options.content.replace('from=${__from}&to=${__to}','from=${__from:date:iso}&to=${__to:date:iso}');
 const target=d.panels.find(p=>p.id===2).targets[0];target.root_selector=list;for(const c of target.columns)if(['tu','den'].includes(c.selector))c.type='string';
 for(const p of d.panels.filter(p=>p.id!==2))if(JSON.stringify(p.targets)!==JSON.stringify(old.panels.find(x=>x.id===p.id).targets))throw Error('Unexpected target edit');
 const after=Buffer.from(JSON.stringify(d,null,2)+'\n');
 await fs.writeFile(dir+'/'+uid+'-truoc.json',before,{flag:'wx'});await fs.writeFile(dir+'/'+uid+'.json',after,{flag:'wx'});await fs.writeFile(file,after);
 plan.push({uid,path:'/opt/flash-ticket-obs/pinned/provisioning/dashboards/RCA FlashTicket/1 · Kết quả hiện hành/'+uid+'.json',before:sha(before),after:sha(after),data:after.toString('base64')});
}
const priorDeploy=await fs.readFile(base+'/l5-ui05-deploy.py','utf8');
const payload=Buffer.from(JSON.stringify(plan)).toString('base64');
const deploy=priorDeploy.replace(/P=json.loads\(base64.b64decode\('[^']+'\)\)/,"P=json.loads(base64.b64decode('"+payload+"'))").replaceAll('l5-ui05','l5-ui06').replaceAll('.ui05.tmp','.ui06.tmp');
await fs.writeFile(base+'/l5-ui06-deploy.py',deploy);
await fs.writeFile(out+'/ui06-plan.json',JSON.stringify({utc:new Date().toISOString(),reason:'Observed hard navigation with numeric from/to produces NaN request; ISO UTC of identical instants produces valid range and data. Historical observations remain iii.',source:{before:sha(beforeSource),after:sha(Buffer.from(src))},changes:plan.map(({data,...x})=>x),unchanged:'All live queries and panel7/24 targets; source data, ranking and flags unchanged',changed:'URL time representation, default time, two hidden time variables and case-list display time strings'},null,2)+'\n');
console.log(JSON.stringify({dashboards:2,live_targets_unchanged:true}));
