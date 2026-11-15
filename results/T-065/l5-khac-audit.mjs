import fs from 'node:fs/promises';
import {createReadStream} from 'node:fs';
import {createInterface} from 'node:readline';
import {spawn} from 'node:child_process';
import crypto from 'node:crypto';
import {kind} from './xuat-du-lieu.mjs';
import {attrs} from './lib.mjs';
const base='results/T-065',out=base+'/kiem/003-trinh-duyet';
const read=async p=>JSON.parse((await fs.readFile(p,'utf8')).replace(/^\uFEFF/,''));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const write=async(p,v)=>fs.writeFile(out+'/'+p,JSON.stringify(v,null,2)+'\n');
if(await fs.stat('D:/RCA-overnight/STOP').then(()=>true,()=>false))throw Error('STOP local');
const index=await read('results/T-064/ban-xuat/chi-muc-ban.json'),manifest=await read(base+'/manifest.json');
const inventory=[],cases=[];
for(const c of index.ban[0].cac_ca){
 const file='du-lieu-l4/p7/'+c.ca+'.json',bytes=await fs.readFile(base+'/'+file);
 if(sha(bytes)!==manifest.files[file].sha256)throw Error('Hash lệch '+file);
 const d=JSON.parse(bytes),ops=d.thao_tac.filter(o=>o.loai.split(', ').includes('khac'));
 cases.push({ca:c.ca,source:c.nguon,ops});
 for(const op of ops)inventory.push({ca:c.ca,source:c.nguon,service:op.chu,id:op.id,name:op.ten,type:op.loai,source_file:file});
}
// Chọn số ca ít nhất theo phủ tên service/operation, không dùng nhãn lỗi hoặc hạng.
const uncovered=new Set(inventory.map(x=>x.service+'|'+x.name)),selected=[];
while(uncovered.size){
 const best=cases.filter(c=>!selected.includes(c)).map(c=>({c,cover:new Set(c.ops.map(o=>o.chu+'|'+o.ten).filter(k=>uncovered.has(k)))})).sort((a,b)=>b.cover.size-a.cover.size)[0];
 if(!best?.cover.size)throw Error('Không phủ đủ khac');
 selected.push(best.c);for(const key of best.cover)uncovered.delete(key);
}
await write('khac-audit-plan.json',{utc:new Date().toISOString(),rows:inventory.length,unique:new Set(inventory.map(x=>x.service+'|'+x.name)).size,selected:selected.map(c=>({ca:c.ca,source:c.source,ops:c.ops.length})),selection:'Greedy phủ service/tên thao tác thuộc khac; không dùng nhãn, hạng hay cờ M1.'});
const sources=[],samples=[];
for(const c of selected){
 const expected=new Map();for(const op of c.ops)for(const ex of op.vi_du||[])expected.set(ex.trace_id+'|'+ex.span_id,{op,ex});
 const rawPath=c.source==='dev2'?null:`results/T-062/ca/${c.ca}/cases/${c.ca}/raw-traces.jsonl`;
 let stream,done,expectedSHA;
 if(rawPath){expectedSHA=(await read('results/T-062/manifest.json')).files[`ca/${c.ca}/cases/${c.ca}/raw-traces.jsonl`].sha256;stream=createReadStream(rawPath);done=Promise.resolve();}
 else{
  const m=await read(`${base}/nguon-l4/cases/${c.ca}/manifest.json`);expectedSHA=m.files['raw-traces.jsonl'].sha256;
  const child=spawn('tar',['-xOf',`results/T-063/thu2/ca/${c.ca}.tgz`,`cases/${c.ca}/raw-traces.jsonl`],{stdio:['ignore','pipe','pipe'],windowsHide:true});let error='';child.stderr.on('data',b=>error+=b);stream=child.stdout;done=new Promise((resolve,reject)=>{child.on('error',reject);child.on('close',n=>n===0?resolve():reject(Error(error)));});
 }
 const hash=crypto.createHash('sha256');stream.on('data',b=>hash.update(b));const found=new Set(),current=[];
 for await(const line of createInterface({input:stream,crlfDelay:Infinity}))if(line.trim()){
  for(const resource of JSON.parse(line).resourceSpans||[])for(const scope of resource.scopeSpans||[])for(const span of scope.spans||[]){
   const key=span.traceId+'|'+span.spanId,match=expected.get(key);if(!match)continue;
   const a=attrs(span.attributes),scopeName=scope.scope?.name||'',actualType=kind(span,scopeName,a);
   current.push({ca:c.ca,service:match.op.chu,op:match.op.id,name:match.op.ten,example:match.ex,scope:scopeName,kind:span.kind,attribute_keys:Object.keys(a).sort(),classifier_values:Object.fromEntries(['db.system','db.system.name','messaging.system'].filter(k=>a[k]!==undefined).map(k=>[k,a[k]])),classified:actualType,expected:match.op.loai,span_name:span.name,raw_service:attrs(resource.resource?.attributes)['service.name']});found.add(match.op.id);
  }
 }
 await done;const actualSHA=hash.digest('hex'),match=actualSHA===expectedSHA;
 sources.push({ca:c.ca,source:rawPath||`results/T-063/thu2/ca/${c.ca}.tgz#/cases/${c.ca}/raw-traces.jsonl`,expected_sha256:expectedSHA,actual_sha256:actualSHA,match,operations:c.ops.length,covered:found.size});
 await write('khac-audit-progress.json',{utc:new Date().toISOString(),sources,samples:[...samples,...current]});
 if(!match||found.size!==c.ops.length)throw Error('Raw hash/coverage lệch '+c.ca);
 samples.push(...current);
}
const groups=Object.entries(Object.groupBy(samples,s=>s.scope)).map(([scope,rows])=>({scope,operations:new Set(rows.map(x=>x.service+'|'+x.name)).size,span_kinds:[...new Set(rows.map(x=>x.kind))],attribute_key_sets:[...new Set(rows.map(x=>JSON.stringify(x.attribute_keys)))].map(x=>JSON.parse(x)),examples:rows.slice(0,3).map(x=>({service:x.service,name:x.name,trace_id:x.example.trace_id,span_id:x.example.span_id}))}));
const checkedNames=new Set(samples.map(x=>x.service+'|'+x.name));
const result={utc:new Date().toISOString(),inventory,sources,samples,groups,checks:{all_raw_hashes:sources.every(s=>s.match),all_unique_names_covered:[...new Set(inventory.map(x=>x.service+'|'+x.name))].every(k=>checkedNames.has(k)),all_sample_types: samples.every(x=>x.classified==='khac')},limits:'Đã phủ mọi tên service/operation hiện thuộc khac bằng các span ví dụ đã lưu trong số ca tối thiểu. Không đọc lại mọi span của mọi ca để phân loại lại; kiểm raw chỉ dùng cho audit hiển thị, không đổi phương pháp/hạng/cờ hoặc nhãn loại đã xuất.'};
await write('khac-audit.json',result);
console.log(JSON.stringify({rows:inventory.length,unique:checkedNames.size,cases:selected.map(c=>c.ca),samples:samples.length,groups,checks:result.checks}));
