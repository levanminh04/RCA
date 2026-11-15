import {ROOT,fs,path,read,json,write,hash,lossless,num,link,assert} from './lib.mjs';
import {prepare} from './xuat-du-lieu.mjs';
export const OUT='du-lieu-l4';
const clone=x=>lossless(JSON.stringify(x));
const invService=id=>({'config-discovery':'discovery-server','postgresql-shared-instance':'postgres','mongodb-instance':'user-db',cache:'redis',broker:'rabbitmq'}[id]||id);
export async function buildL4(){
 const index=await json('results/T-064/ban-xuat/chi-muc-ban.json'), proofs=[], comparisons=[],links=[];
 // Không dùng đầu ra nào trước khi cả chỉ mục đã qua kiểm hash.
 for(const b of index.ban) for(const c of b.cac_ca){const bytes=await fs.readFile(path.join(ROOT,c.dau_ra));assert(hash(bytes)===c.sha256,'Hash lệch '+c.dau_ra);proofs.push({file:c.dau_ra,sha256:hash(bytes)});}
 const p7mf=await json('results/T-065/manifest.json');
 const templates=new Map(), inputPaths=new Map(), metric=new Map();
 for(const c of index.ban[0].cac_ca){
  const local=c.nguon==='t062'?`results/T-062/ca/${c.ca}/outputs/${c.ca}/method-input.json`:`results/T-065/nguon-l4/outputs/${c.ca}/method-input.json`;
  inputPaths.set(c.ca,local);
  if(c.nguon==='t062'){
   const f=`du-lieu/p7/${c.ca}.json`,bytes=await fs.readFile(path.join(ROOT,'results/T-065',f));assert(hash(bytes)===p7mf.files[f].sha256,'L3 lệch '+f);templates.set(c.ca,lossless(bytes.toString()));
  }else metric.set(c.ca,await json(`results/T-065/nguon-l4/cases/${c.ca}/prometheus.json`));
 }
 const variants=[];
 for(const b of index.ban){const cases=[];
  for(const c of b.cac_ca){
   const m=lossless(await read(c.dau_ra)),plain=JSON.parse(JSON.stringify(m)),inp=await json(inputPaths.get(c.ca)),[rows,,,inventory,aliases,t,params]=inp;
   assert(m.window.don_vi==='ns','Đơn vị cửa sổ');const w=[num(m.window.N[0])/1e6,num(m.window.A[1])/1e6];assert(w[1]-w[0]===600000&&w[0]===(t-300)*1000,'Cửa sổ nguồn');
   const meta={ban:b.ban,mo_ta:b.mo_ta,trang_thai:b.trang_thai,cau_hinh_sha256:b.cau_hinh_sha256,ma_nguon_sha256:b.ma_nguon_sha256,
    ghi_chu_hash:b.ban==='p7'?'Chỉ mục T-064 không cấp hai hash cấp bản (null). Hash từng đầu ra đã kiểm; không suy hash cây mã nguồn.':'Hash do chỉ mục T-064 cấp.',
    method_version:m.method_version,config_id:m.config_id,variant:m.variant,nguon_output:c.dau_ra,sha256_output:c.sha256};
   if(b.ban!=='p7'){for(const k of ['cau_hinh_sha256','ma_nguon_sha256'])assert(m.extra.m1_ft[k]===b[k],'Metadata lệch '+k);}
   const flags=m.extra.kenh_co||[],units=new Map((m.extra.don_vi_phan_vi||[]).map(u=>[u.ma,u]));
   const base=templates.has(c.ca)?clone(templates.get(c.ca)):{thao_tac:[],canh_thao_tac:[],quan_he:{da_ho_tro:['span_cha_con'],span_link:{trang_thai:'chua_ho_tro'}}};
   if(c.nguon==='dev2'){
    const prep=prepare(rows,aliases,t,params.don_vi_thoi_gian['spans.start_us']);
    for(const k of ['so_span','bo_lap','mo_coi','goc','span_boc'])assert(prep.diagnostics[k]===plain.diagnostics.span[k],c.ca+' trung gian '+k);
    const groups=new Map(),edges=new Map();
    for(const s of prep.spans.values()){
     const id='o'+hash(JSON.stringify([s.owner,s.operation])).slice(0,20);s.opid=id;
     if(!groups.has(id))groups.set(id,{id,chu:s.owner,ten:s.operation,loai:'khac (đầu vào chuẩn hóa không giữ thuộc tính loại)',n_N:0,n_A:0,mau_N:0,mau_A:0,span_boc:0,mo_coi:0,goc:0,dich_quan_sat:[],vi_du:[]});
     const g=groups.get(id);g['n_'+s.phase]++;if(params.bat_tat.E1==='tat'||!s.wrapper)g['mau_'+s.phase]++;g.span_boc+=Number(s.wrapper);g.mo_coi+=Number(s.orphan);g.goc+=Number(!s.parentSpanID);
     if(g.vi_du.length<3)g.vi_du.push({trace_id:s.traceID,span_id:s.spanID,parent_span_id:s.parentSpanID,phia:s.phase});
    }
    for(const s of prep.spans.values())if(s.parent){const p=prep.spans.get(s.parent),id=p.opid+'->'+s.opid;
     if(!edges.has(id))edges.set(id,{id,source:p.opid,target:s.opid,loai:'span_cha_con',so_quan_he:0,so_N:0,so_A:0,vi_du:[]});
     const e=edges.get(id);e.so_quan_he++;e['so_'+s.phase]++;if(e.vi_du.length<3)e.vi_du.push({trace_id:s.traceID,cha_span_id:p.spanID,con_span_id:s.spanID});}
    base.thao_tac=[...groups.values()];base.canh_thao_tac=[...edges.values()];base.tien_xu_ly=prep.diagnostics;
   }
   const owners=new Set(rows.map(r=>aliases[r.owner]||r.owner)),logowners=new Set((inp[2]||[]).map(r=>aliases[r.entity]||r.entity));
   const svcs=entity=>Object.keys(aliases).filter(k=>aliases[k]===entity).concat([invService(entity)]).filter((v,i,a)=>a.indexOf(v)===i);
   function evidence(entity,op){
    const result=[];for(const svc of svcs(entity)){
     // Chỉ tạo trace theo owner đã quan sát trong đầu vào M1.
     if(owners.has(entity))result.push(link('tempo',`{ resource.service.name = ${JSON.stringify(svc)}${op?' && name = '+JSON.stringify(op):''} }`,w,op?'tim_span_thao_tac':'ngu_canh_service','Truy vấn từ owner/tên thao tác đã quan sát trong đầu vào; không phải trace do M1 chọn.'));
     if(logowners.has(entity))result.push(link('loki',`{service_name=${JSON.stringify(svc)}}`,w,'ngu_canh_service','Log ngữ cảnh service đã có đầu vào; không khẳng định log do thao tác phát.'));
    }
    return result;
   }
   for(const op of base.thao_tac){const u=units.get('op|'+op.chu+'|'+op.ten),f=flags.filter(k=>k.don_vi==='op|'+op.chu+'|'+op.ten);
    Object.assign(op,{trang_thai_m1:u?.trang_thai||'KHONG_CHAM_SPAN_BOC',co_len:u?.F_raw_len||0,co_xuong:u?.F_raw_xuong||0,co_m1:f.length>0,so_kenh_co:f.length,kenh_co:f,don_vi_m1:u||null,mau:f.length?'#E02F44':u?.trang_thai==='OK'?'#8E8E8E':'#CA95E5',ban_kinh:32});
    if(c.nguon==='dev2')op.lien_ket=evidence(op.chu,op.ten);
   }
   const oldflags=new Map((base.bang_chung||[]).map(f=>[f.id,f]));
   base.bang_chung=flags.map(f=>({id:f.ma,don_vi:f.don_vi,thuc_the:f.thuc_the,kenh:f.ten,huong:f.huong,lop:f.lop,s:f.s,F_I:f.F_I,khoi_phat_ns:f.khoi_phat,
    lien_ket:oldflags.has(f.ma)?clone(oldflags.get(f.ma).lien_ket):evidence(f.thuc_the,f.don_vi.startsWith('op|')?f.don_vi.split('|').slice(2).join('|'):undefined)}));
   const serviceLinks=[];
   if(c.nguon==='dev2'){
    for(const q of metric.get(c.ca)){if(q.query&&q.result?.length)serviceLinks.push(link('prometheus',q.query,w,'truy_van_metric_da_luu','Truy vấn nguyên văn prometheus.json của ca; có thể gồm nhiều service, không phải điểm M1.'));}
   }
   const ranked=m.entity_ranking.map(r=>({...r,hang:r.tie_group+1,lop:m.classes[r.entity],so_kenh_co:flags.filter(f=>f.thuc_the===r.entity).length}));
   const edges=m.extra.m1_ft?.canh_xep_hang;
   Object.assign(base,{phien_ban_dinh_dang:'0.4',ban:meta,ca:c.ca,nguon_ca:c.nguon,cua_so_ms:w,tu_utc:new Date(w[0]).toISOString(),den_loai_tru:new Date(w[1]).toISOString(),
    su_co:{ma:c.ca,ket_luan:m.verdict,trang_thai:m.status,cua_so_nen:{tu_ms:w[0],den_ms:t*1000},cua_so_su_co:{tu_ms:t*1000,den_ms:w[1]}},
    entity_ranking:m.entity_ranking,ranking_rows:ranked,canh_xep_hang:edges||[],trang_thai_canh:edges===undefined?'không có đầu ra cạnh':`${edges.length} dòng cạnh từ extra.m1_ft.canh_xep_hang; không xếp lại`,
    co_m1:flags,don_vi_m1:m.extra.don_vi_phan_vi,region:m.region,classes:m.classes,ke_thua:m.inherited_by,metric_links:serviceLinks,
    nguon:{file_m1:c.dau_ra,sha256_m1:c.sha256,goi_dev:c.nguon==='dev2'?`results/T-063/thu2/ca/${c.ca}.tgz`:null},
    gioi_han:c.nguon==='dev2'?'Có trace/log/metric trong gói đã băm; liên kết log là ngữ cảnh service. Loại thao tác chưa phân loại từ thuộc tính raw. Không suy metric route từ tên thao tác.':'Kế thừa liên kết đã kiểm L3; cờ và hạng thay bằng đầu ra của bản đang xem.'});
   // Dùng trực tiếp dữ liệu nguồn cho đồ thị và trạng thái, không giữ số/nhãn cũ của P7.
   base.nut=ranked.map(r=>({id:r.entity,ten:r.entity,hang:r.hang,nhom_dong_hang:r.tie_group,khoa_m1:r.key,lop_m1:r.lop,co_m1:r.so_kenh_co>0}));
   delete base.xep_hang;delete base.do_phu;delete base.vung;delete base.canh;delete base.giai_thich_ke_thua;
   await write(`${OUT}/${b.ban}/${c.ca}.json`,base);
   for(const svc of new Set([...ranked.map(r=>r.entity),...base.thao_tac.map(o=>o.chu)])){
    const ops=base.thao_tac.filter(o=>o.chu===svc),own=new Set(ops.map(o=>o.id)),es=base.canh_thao_tac.filter(e=>own.has(e.source)||own.has(e.target)),ns=new Set([...own,...es.flatMap(e=>[e.source,e.target])]);
    await write(`${OUT}/${b.ban}/thao-tac/${c.ca}/${svc}.json`,{ban:meta,ca:c.ca,service:svc,cua_so_ms:w,thao_tac:ops,nut:base.thao_tac.filter(o=>ns.has(o.id)).map(o=>({...o,ngoai_service:o.chu!==svc})),canh:es,
     thong_bao:ops.length?`${ops.length} thao tác từ đầu vào; ${ops.filter(o=>o.co_m1).length} có cờ M1 của bản ${b.ban}.`:'Không có thao tác trong đầu vào sau cắt cửa sổ; chưa xác định vì không phát sinh hay không được thu.'});
   }
   if(c.nguon==='t062'){
    const replay=await json(`results/T-065/du-lieu/p7/phat-lai/${c.ca}.phat-lai.json`);
    const answer=Object.fromEntries(Object.entries(replay.phat_lai).filter(([k])=>!['nhan_xet','hang_trong_tap','hang_tot_nhat','sha256_ket_qua_truoc_ghep','sha256_manifest_ket_qua'].includes(k)));
    await write(`${OUT}/${b.ban}/phat-lai/${c.ca}.json`,{ban:meta,ca:c.ca,cua_so_ms:w,ranking_rows:ranked,canh_xep_hang:edges||[],phat_lai:answer,gioi_han:'Chỉ ghép đáp án gốc; không mang nhận xét/hạng chấm của P7 sang bản khác. Giao diện không tự chấm.'});
   }else await write(`${OUT}/${b.ban}/phat-lai/${c.ca}.json`,{ban:meta,ca:c.ca,cua_so_ms:w,ranking_rows:ranked,canh_xep_hang:edges||[],gioi_han:'Chưa cấp nguồn phát lại/đáp án dev2 cho lớp giao diện; không dựng đáp án.'});
   for(const lk of [...base.bang_chung.flatMap(f=>f.lien_ket),...base.thao_tac.flatMap(o=>o.lien_ket),...serviceLinks])links.push({ban:b.ban,ca:c.ca,...lk});
   cases.push({ma:c.ca,ban:b.ban,nguon:c.nguon,tu:w[0],den:w[1]-1,ket_luan:m.verdict,file:c.ca+'.json'});
   comparisons.push({ban:b.ban,ca:c.ca,nguon:c.nguon,ranking:ranked.length,flags:flags.length,units:units.size,edges:edges?.length||0,operations:base.thao_tac.length});
  }
  await write(`${OUT}/${b.ban}/chi-muc.json`,{su_co:cases});variants.push({...b,cac_ca:cases.map(x=>x.ma)});
 }
 await write(`${OUT}/chi-muc-ban.json`,{ban:variants});await write('kiem/002/doi-chieu-xuat.json',comparisons);await write('kiem/002/lien-ket.json',links);return {cases:comparisons.length,links:links.length};
}
