import {fs,path,ROOT,json,write,assert,hash,lossless,read} from './lib.mjs';
const eq=(a,b,msg)=>assert(JSON.stringify(a)===JSON.stringify(b),msg);
export async function verifyL4(){
 const idx=await json('results/T-064/ban-xuat/chi-muc-ban.json');let rank=0,flags=0,units=0,edges=0,ops=0,urls=0;const rows=[],allLinks=[];
 for(const b of idx.ban)for(const c of b.cac_ca){
  const src=lossless(await read(c.dau_ra)),d=lossless(await read(`results/T-065/du-lieu-l4/${b.ban}/${c.ca}.json`));
  eq(d.entity_ranking,src.entity_ranking,'entity_ranking '+c.ca);eq(d.co_m1,src.extra.kenh_co,'flags '+c.ca);
  eq(d.don_vi_m1,src.extra.don_vi_phan_vi,'units '+c.ca);eq(d.canh_xep_hang,src.extra.m1_ft?.canh_xep_hang||[],'edges '+c.ca);eq(d.region,src.region,'region '+c.ca);
  eq(d.ranking_rows.map(r=>({entity:r.entity,key:r.key,tie_group:r.tie_group})),src.entity_ranking,'ordre '+c.ca);
  assert(d.ban.ban===b.ban&&d.ban.trang_thai===b.trang_thai,'meta');for(const k of ['cau_hinh_sha256','ma_nguon_sha256'])eq(d.ban[k],b[k],'hash meta');
  eq(d.ranking_rows.map(r=>r.so_kenh_co),src.entity_ranking.map(r=>src.extra.kenh_co.filter(f=>f.thuc_the===r.entity).length),'node flags');
  let opflags=0;for(const o of d.thao_tac){const u=src.extra.don_vi_phan_vi.find(x=>x.ma==='op|'+o.chu+'|'+o.ten),ff=src.extra.kenh_co.filter(x=>x.don_vi==='op|'+o.chu+'|'+o.ten);
   eq(o.kenh_co,ff,'op flags');eq(o.don_vi_m1,u||null,'op unit');assert(o.co_m1===(ff.length>0),'flag bool');
   if(u){assert(o.mau_N===u.n_N&&o.mau_A===u.n_A,'op sample '+c.ca+'/'+o.ten);}opflags+=ff.length;
  }
  assert(opflags===src.extra.kenh_co.filter(f=>f.don_vi.startsWith('op|')).length,'missing op flag');
  const all=[...d.thao_tac.flatMap(o=>o.lien_ket),...d.bang_chung.flatMap(f=>f.lien_ket),...d.metric_links];
  for(const l of all){const params=new URL(l.url,'http://localhost').searchParams,p=JSON.parse(params.get('panes')).a,q=p.queries[0];
   assert(p.datasource===l.kho&&q.datasource.uid===l.kho,'datasource');eq(q.query||q.expr,l.truy_van,'query decoding');
   eq([Number(p.range.from),Number(p.range.to)],[d.cua_so_ms[0],d.cua_so_ms[1]-1],'window');urls++;allLinks.push({ban:b.ban,ca:c.ca,...l});
  }
  if(c.nguon==='t062'&&b.ban==='p7'){const old=lossless(await read(`results/T-065/du-lieu/p7/${c.ca}.json`));
   eq(d.thao_tac,old.thao_tac,'P7 operations regression');eq(d.canh_thao_tac,old.canh_thao_tac,'P7 edges regression');
   eq(d.bang_chung.map(f=>f.lien_ket),old.bang_chung.map(f=>f.lien_ket),'P7 evidence regression');
  }
  const txt=JSON.stringify(d);for(const forbidden of ['tap_chap_nhan','root_khai_truoc','o_loi','thanh_phan_tiem'])assert(!txt.includes('"'+forbidden+'"'),'label '+forbidden);
  rank+=d.entity_ranking.length;flags+=d.co_m1.length;units+=d.don_vi_m1.length;edges+=d.canh_xep_hang.length;ops+=d.thao_tac.length;
  rows.push({ban:b.ban,ca:c.ca,rank:d.entity_ranking.length,flags:d.co_m1.length,units:d.don_vi_m1.length,edges:d.canh_xep_hang.length,operations:d.thao_tac.length,ok:true});
 }
 for(const uid of ['t065-l4-rca','t065-l4-phat-lai']){const d=await json(`results/T-065/grafana-l4/${uid}.json`);assert(d.uid===uid,'UID');
  if(uid==='t065-l4-rca'){const txt=JSON.stringify(d);for(const s of ['root_khai_truoc','tap_chap_nhan','phat_lai.'])assert(!txt.includes(s),'main labels');}
 }
 const result={ok:true,cases:rows.length,rank_rows:rank,flag_rows:flags,unit_rows:units,edge_rows:edges,operation_rows:ops,urls,rows};await write('kiem/002/kiem-cuc-bo.json',result);await write('kiem/002/lien-ket.json',allLinks);return result;
}
export async function verifyApiL4(filename){
 const a=await json('results/T-065/kiem/002/'+filename),errors=[],report=[];let targets=0;
 function frames(answer){const rr=answer.response;assert(rr.http===200,'http '+rr.http);const results=rr.data.results;
  for(const [ref,r]of Object.entries(results)){targets++;if(r.error)errors.push({ref,error:r.error});}
  return Object.fromEntries(Object.entries(results).map(([ref,r])=>[ref,(r.frames||[]).flatMap(f=>{
   const ff=f.schema.fields,vv=f.data.values;return Array.from({length:vv[0]?.length||0},(_,i)=>Object.fromEntries(ff.map((c,k)=>[c.name,vv[k][i]])));})]));
 }
 for(const [key,pages]of Object.entries(a.cases)){
  const k=key.lastIndexOf('/'),ban=key.slice(0,k),ca=key.slice(k+1),d=await json(`results/T-065/du-lieu-l4/${ban}/${ca}.json`);
  for(const [uid,answer]of Object.entries(pages)){const f=frames(answer);
   eq(f['4_rank'].map(x=>[x.entity,x.hang,x.tie_group,x.lop,x.so_kenh_co]),d.ranking_rows.map(x=>[x.entity,x.hang,x.tie_group,x.lop,x.so_kenh_co]),'API rank '+key);
   eq(f['6_edge_rank'].map(x=>[x.nguon,x.dich,x.loai,x.hang,x.tie_group,x.co,x.trang_thai,x.nguon_xac_minh]),d.canh_xep_hang.map(x=>[x.nguon,x.dich,x.loai,x.hang,x.tie_group,x.co,x.trang_thai,x.nguon_xac_minh]),'API edge '+key);
   if(uid==='t065-l4-rca'){
    eq(f['9_flags'].map(x=>[x.ma,x.thuc_the,x.don_vi,x.ten,x.huong,x.lop,x.F_I]),d.co_m1.map(x=>[x.ma,x.thuc_the,x.don_vi,x.ten,x.huong,x.lop,x.F_I]),'API flag '+key);
    const m=f['3_meta'][0];assert(m.ban===ban&&m.trang_thai===d.ban.trang_thai,'API meta');for(const k of ['cau_hinh_sha256','ma_nguon_sha256'])eq(m[k],d.ban[k],'API hash');
    const opsq=answer.request.queries.find(q=>q.refId==='22_ops'),svc=opsq.url.split('/').at(-1).replace('.json',''),ops=d.thao_tac.filter(o=>o.chu===svc);
    eq(f['22_ops'].map(x=>[x.id,x.loai,x.trang_thai,x.co,x.len,x.xuong,x.mau_N,x.mau_A]),ops.map(o=>[o.id,o.loai,o.trang_thai_m1,o.co_m1?'có cờ M1':'không có cờ M1',o.co_len,o.co_xuong,o.mau_N,o.mau_A]),'API ops '+key);
    const selected=answer.request.queries.find(q=>q.refId==='25_oplinks').root_selector.match(/id="([^"]*)"/)[1],op=d.thao_tac.find(o=>o.id===selected);
    eq(f['25_oplinks'].map(x=>[x.url,x.truy_van,x.pham_vi,x.ghi_chu]),(op?.lien_ket||[]).map(l=>[l.url,l.truy_van,l.pham_vi,l.ghi_chu]),'API operation links '+key);
    const status=await json(`results/T-065/du-lieu-l4/trang-thai/${ca}/${svc}.json`);eq(f['28_query_state'].map(x=>[x.panel,x.kho,x.trang_thai,x.so_dong,x.utc,x.dien_giai,x.loi]),status.queries.map(x=>[x.panel,x.kho,x.trang_thai,x.so_dong,x.utc,x.dien_giai,x.loi]),'API status '+key);
   }
   report.push({key,uid,rank:f['4_rank'].length,edges:f['6_edge_rank'].length,ok:true});
  }
 }
 for(const [key,v]of Object.entries(a.variables)){
  const f=frames(v),parts=key.split('/'),ban=parts[0],ca=parts[1],d=await json(`results/T-065/du-lieu-l4/${ban}/${ca}.json`),idx=await json('results/T-064/ban-xuat/chi-muc-ban.json');
  eq(f.ban_v.map(x=>x.__value),idx.ban.map(b=>b.ban),'version variable');eq(f.ca_v.map(x=>x.__value),idx.ban.find(b=>b.ban===ban).cac_ca.map(c=>c.ca),'case variable');
  eq(f.dv_v.map(x=>x.__value),d.ranking_rows.map(r=>r.entity),'service variable');eq(f.t_tu_v[0].v,d.cua_so_ms[0],'from var');eq(f.t_den_v[0].v,d.cua_so_ms[1]-1,'to var');
 }
 assert(errors.length===0,JSON.stringify(errors.slice(0,10)));const result={ok:true,pages:report.length,targets,report};await write('kiem/002/doi-chieu-api.json',result);return result;
}
