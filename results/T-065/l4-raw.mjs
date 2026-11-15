import {spawn} from 'node:child_process';
import {createInterface} from 'node:readline';
import crypto from 'node:crypto';
import {ROOT,fs,path,json,read,lossless,write,attrs,hash,link,assert} from './lib.mjs';
import {prepare,kind} from './xuat-du-lieu.mjs';
// Đọc streaming từ archive đã kiểm: không bung thêm nhiều GB raw và không chạy M1.
export async function enrichRawL4(){
 const idx=await json('results/T-064/ban-xuat/chi-muc-ban.json'),proof=[];
 for(const c of idx.ban[0].cac_ca.filter(c=>c.nguon==='dev2')){
  const inp=await json(`results/T-065/nguon-l4/outputs/${c.ca}/method-input.json`),[rows,,,inv,aliases,t,params]=inp;
  const prep=prepare(rows,aliases,t,params.don_vi_thoi_gian['spans.start_us']),meta=new Map();
  const manifest=await json(`results/T-065/nguon-l4/cases/${c.ca}/manifest.json`);
  const child=spawn('tar',['-xOf',`results/T-063/thu2/ca/${c.ca}.tgz`,`cases/${c.ca}/raw-traces.jsonl`],{cwd:ROOT,stdio:['ignore','pipe','pipe'],windowsHide:true});
  let error='',count=0,spanLinks=0;child.stderr.on('data',b=>error+=b.toString());const hh=crypto.createHash('sha256');child.stdout.on('data',b=>hh.update(b));
  const done=new Promise((resolve,reject)=>{child.on('error',reject);child.on('close',code=>code===0?resolve():reject(Error(error)));});
  for await(const line of createInterface({input:child.stdout,crlfDelay:Infinity}))if(line.trim()){
   for(const r of JSON.parse(line).resourceSpans||[]){const svc=attrs(r.resource?.attributes)['service.name'];
    for(const scope of r.scopeSpans||[])for(const s of scope.spans||[]){const p=prep.spans.get(s.traceId+'|'+s.spanId);if(!p)continue;
     const id='o'+hash(JSON.stringify([p.owner,p.operation])).slice(0,20),a=attrs(s.attributes);if(!meta.has(id))meta.set(id,{types:new Set(),targets:new Set(),routes:new Map()});const m=meta.get(id);
     m.types.add(kind(s,scope.scope?.name||'',a));if(a['server.address'])m.targets.add(a['server.address']+(a['db.system']?' ('+a['db.system']+')':''));
     const method=a['http.request.method']||a['http.method'];if(a['http.route']&&method){const route={svc,method,route:a['http.route']};m.routes.set(JSON.stringify(route),route);}
     spanLinks+=(s.links||[]).length;count++;
    }
   }
  }
  await done;const sha256=hh.digest('hex');assert(sha256===manifest.files['raw-traces.jsonl'].sha256,'Raw trace hash lệch '+c.ca);assert(count===prep.spans.size,'Raw/normalized không khớp '+c.ca);
  const counts={};for(const b of idx.ban){
   const file=`du-lieu-l4/${b.ban}/${c.ca}.json`,d=lossless(await read('results/T-065/'+file));
   for(const o of d.thao_tac){const m=meta.get(o.id);assert(m,'Thiếu raw thao tác '+o.id);o.loai=[...m.types].sort().join(', ');o.dich_quan_sat=[...m.targets].sort();
    o.lien_ket=o.lien_ket.filter(l=>l.kho!=='prometheus');for(const r of m.routes.values())o.lien_ket.push(link('prometheus',`sum by (http_request_method,http_route) (rate(http_server_request_duration_seconds_count{service_name=${JSON.stringify(r.svc)},http_request_method=${JSON.stringify(r.method)},http_route=${JSON.stringify(r.route)}}[1m]))`,d.cua_so_ms,'route_http_quan_sat','Route/method từ raw span đã băm; không phải điểm M1.'));
    o.ly_do_khong_prometheus=m.routes.size?null:'Không có cặp http.route/method trong raw span của thao tác; không dựng metric SQL/job/message từ tên.';
    if(b.ban==='p7')counts[o.loai]=(counts[o.loai]||0)+1;
   }
   d.gioi_han='Có trace/log/metric trong gói đã băm. Loại thao tác và route/method lấy từ raw span; log là ngữ cảnh service, không khẳng định do thao tác phát. Span link message chưa hỗ trợ.';
   d.quan_he={da_ho_tro:['span_cha_con'],span_link:{trang_thai:'chua_ho_tro',so_link_raw:spanLinks}};
   await write(file,d);const om=new Map(d.thao_tac.map(o=>[o.id,o]));
   for(const service of new Set([...d.ranking_rows.map(r=>r.entity),...d.thao_tac.map(o=>o.chu)])){
    const sf=`du-lieu-l4/${b.ban}/thao-tac/${c.ca}/${service}.json`,s=lossless(await read('results/T-065/'+sf));s.thao_tac=s.thao_tac.map(o=>om.get(o.id));s.nut=s.nut.map(o=>({...om.get(o.id),ngoai_service:o.ngoai_service}));await write(sf,s);
   }
  }
  proof.push({ca:c.ca,raw_traces_sha256:sha256,spans:count,operations:meta.size,types:counts,span_links_raw:spanLinks});await write('kiem/002/kiem-raw-dev2.json',proof);
 }
 return proof;
}
