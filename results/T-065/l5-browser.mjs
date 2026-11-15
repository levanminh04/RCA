// Chỉ import trong cua_repl; mọi UI qua tab binding Browser Use được truyền vào.
import fs from 'node:fs/promises';
const root='D:/RCA-flashticket',base=root+'/results/T-065/kiem/003-trinh-duyet';
const read=async p=>JSON.parse((await fs.readFile(root+'/'+p,'utf8')).replace(/^\uFEFF/,''));
const write=async(p,v)=>fs.writeFile(base+'/'+p,JSON.stringify(v,null,2)+'\n');
export class L5Browser {
 constructor(tab){this.tab=tab;}
 async init(){
  this.index=await read('results/T-064/ban-xuat/chi-muc-ban.json');this.dash=await read('results/T-065/grafana-l4/t065-l4-rca.json');
  this.types=Object.fromEntries(this.dash.panels.map(p=>[p.id,p.type]));
  const journal=await fs.readFile(base+'/nhat-ky-bam.jsonl','utf8').catch(()=> '');this.seq=journal.trim().split('\n').filter(Boolean).reduce((n,l)=>Math.max(n,JSON.parse(l).stt||0),0);
  this.pages=await read('results/T-065/kiem/003-trinh-duyet/doi-chieu-hien-thi.json').catch(()=>[]);
  this.empty=await read('results/T-065/kiem/003-trinh-duyet/panel-rong.json').catch(()=>[]);return {pages:this.pages.map(x=>({ban:x.ban,ca:x.ca,status:x.status})),seq:this.seq};
 }
 async action(action,expect,fn,tag='ui'){
  const before=await this.tab.url(),utc=new Date().toISOString();let error=null;
  try{await fn();}catch(e){error=String(e);}
  const after=await this.tab.url(),dom=await this.tab.playwright.domSnapshot();
  const id=String(++this.seq).padStart(4,'0')+'-'+tag;
  await fs.writeFile(base+'/'+id+'.txt',dom);
  await fs.appendFile(base+'/nhat-ky-bam.jsonl',JSON.stringify({stt:this.seq,utc,url_truoc:before,url_sau:after,hanh_dong:action,ky_vong:expect,quan_sat_file:id+'.txt',ket_qua:error?'loi':'cho_doi_chieu',loi:error,anh:null})+'\n');
  if(error)throw Error(error);return dom;
 }
 panel(id){return this.tab.playwright.getByTestId(this.types[id]+'-panel-'+id);}
 async focus(id,tag){return this.action('Xem panel '+id,'Panel được tải, đúng bản/ca/service',()=>this.panel(id).getByRole('heading').click(),tag+'-p'+id);}
 async table(id){
  const p=this.tab.playwright.getByTestId('table-panel-'+id);
  const headers=await p.getByRole('columnheader').allTextContents({});
  await p.getByRole('row').allTextContents({});
  const rows=await p.getByRole('row').evaluateAll(es=>es.map(e=>Array.from(e.querySelectorAll('[role="gridcell"]')).map(c=>(c.textContent||'').trim())).filter(r=>r.length&&r.some(Boolean)));
  return {headers,rows};
 }
 async shot(name){await fs.writeFile(base+'/anh/'+name+'.jpg',await this.tab.screenshot({fullPage:false}));return 'anh/'+name+'.png';}
 async save(pg){
  this.pages=this.pages.filter(x=>x.ban!==pg.result.ban||x.ca!==pg.result.ca);this.pages.push(pg.result);
  await write(pg.label+'.json',pg.result);await write('doi-chieu-hien-thi.json',this.pages);await write('panel-rong.json',this.empty);
  await fs.writeFile(root+'/results/T-065/codex/L5-trang-thai.json',JSON.stringify({ten:'L5',trang_thai:'dang_chay',nguon:'codex-app',cap_nhat:new Date().toISOString(),buoc:'browser '+pg.result.ban+'/'+pg.result.ca+' '+pg.result.status},null,2));
 }
 async light(bi,ci){
  const b=this.index.ban[bi],c=b.cac_ca[ci],ordinal=bi*22+ci+1;
  const data=await read('results/T-065/du-lieu-l4/'+b.ban+'/vue/'+c.ca+'.json'),src=await read(c.dau_ra);
  const service=data.ranking_rows[0]?.entity||'event-service',label=String(ordinal).padStart(3,'0')+'-trang-'+b.ban.replaceAll('+','_')+'-'+c.ca;
  const url='http://127.0.0.1:13000/d/t065-l4-rca?var-ban='+encodeURIComponent(b.ban)+'&var-ca='+c.ca+'&var-dv='+encodeURIComponent(service)+'&var-op=&from='+data.cua_so_ms[0]+'&to='+(data.cua_so_ms[1]-1);
  const current=new URL(await this.tab.url());
  if(current.searchParams.get('var-ban')!==b.ban||current.searchParams.get('var-ca')!==c.ca){
   const initial=await this.action('Mở trang '+b.ban+'/'+c.ca,'Bản/ca/cửa sổ lấy từ nguồn đã kiểm hash',()=>this.tab.goto(url),label+'-mo');
   if(initial.includes('Loading')){this.current=null;return {pending:true,ban:b.ban,ca:c.ca,reason:'Grafana đang tải; đọc lại ở lời gọi kế tiếp, không nạp lại'};}
  }
  const observed=await this.tab.playwright.domSnapshot();
  if(!observed.includes('heading "Bản, hash, trạng thái và cửa sổ"')){this.current=null;return {pending:true,ban:b.ban,ca:c.ca,reason:'Chưa thấy metadata; giữ tab và chờ trạng thái tiếp theo'};}
  await this.focus(3,label);
  await this.panel(3).getByRole('gridcell',{name:c.dau_ra,exact:true}).waitFor({state:'visible',timeoutMs:15000});
  const meta=await this.table(3);await this.focus(4,label);
  await this.panel(4).getByRole('gridcell',{name:src.entity_ranking[0].entity,exact:true}).waitFor({state:'visible',timeoutMs:10000});
  const rank=await this.table(4),shot=await this.shot(label);await this.focus(6,label);
  await this.panel(5).getByRole('gridcell',{name:data.trang_thai_canh,exact:true}).waitFor({state:'visible',timeoutMs:10000});
  if(data.canh_xep_hang?.length)await this.panel(6).getByRole('gridcell',{name:data.canh_xep_hang[0].nguon,exact:true}).first().waitFor({state:'visible',timeoutMs:10000});
  else await this.panel(6).getByText(this.dash.panels.find(p=>p.id===6).fieldConfig.defaults.noValue,{exact:true}).waitFor({state:'visible',timeoutMs:10000});
  const edge_state=await this.panel(5).textContent(),edges=await this.table(6),md=Object.fromEntries(meta.rows);
  const rr=rank.rows.map(r=>Object.fromEntries(rank.headers.map((h,i)=>[h,r[i]])));
  const er=edges.rows.map(r=>Object.fromEntries(edges.headers.map((h,i)=>[h,r[i]])));
  const expected_ranks=src.entity_ranking.slice(0,3).map(x=>({entity:x.entity,tie_group:x.tie_group,group:x.tie_group+1}));
  const expected_edges=(data.canh_xep_hang||[]).slice(0,3);
  const checks={ban:md['Bản']===b.ban,status:md['Trạng thái']===b.trang_thai,config:md['Hash cấu hình']===(b.cau_hinh_sha256||'null — chỉ mục nguồn chưa cấp'),source_hash:md['Hash mã nguồn']===(b.ma_nguon_sha256||'null — chỉ mục nguồn chưa cấp'),source:md['Nguồn đầu ra']===c.dau_ra,window:md['Bắt đầu (bao gồm)']===data.tu_utc&&md['Kết thúc (loại trừ)']===data.den_loai_tru,ranking:expected_ranks.every((e,i)=>rr[i]?.entity===e.entity&&Number(rr[i]?.tie_group)===e.tie_group&&Number(rr[i]?.['Nhóm (tie_group + 1)'])===e.group),edge_state:edge_state.includes(data.trang_thai_canh),edge_rows:expected_edges.every((e,i)=>er[i]&&['nguon','dich','hang','tie_group','co'].every(k=>String(er[i][k]??'')===String(e[k]??'')))};
  this.current={label,result:{utc:new Date().toISOString(),ban:b.ban,ca:c.ca,nguon:c.dau_ra,service,url:await this.tab.url(),meta,rank_top:rr.slice(0,3),expected_ranks,edges,expected_edges,edge_state,checks,anh:shot,panel_checks:[],status:'dang_kiem_panel'}};
  await this.save(this.current);return {label,checks};
 }
 async scan(){
  const pg=this.current;if(!pg)throw Error('Cần light() hoặc resume() trước');
  for(const id of [9,21,23,25,28,31,33,35])await this.focus(id,pg.label);
  const dom=await this.tab.playwright.domSnapshot();await fs.writeFile(base+'/'+pg.label+'-tat-ca-panel.txt',dom);
  const messages=await this.tab.playwright.getByTestId('data-testid Panel data error message').allTextContents({});
  const defaults=this.dash.panels.map(p=>p.fieldConfig?.defaults?.noValue).filter(Boolean);
  const errors=messages.filter(x=>!defaults.includes(x)&&x!=='—'&&x!=='No data');
  const panels=await this.tab.playwright.evaluate(()=>Array.from(document.querySelectorAll('[data-testid^="table-panel-"],[data-testid^="timeseries-panel-"],[data-testid^="logs-panel-"],[data-testid^="nodeGraph-panel-"]')).map(e=>({id:e.getAttribute('data-testid'),text:e.textContent})));
  pg.result.panel_checks={messages,errors,panels,dom:pg.label+'-tat-ca-panel.txt'};
  pg.result.status=Object.values(pg.result.checks).every(Boolean)&&!errors.length?'dat_dom':'can_soat';
  for(const p of panels){const id=Number(p.id.split('-').at(-1)),def=this.dash.panels.find(x=>x.id===id)?.fieldConfig?.defaults?.noValue;
   if((def&&p.text?.includes(def))||(id===35&&p.text?.includes('No data')))this.empty.push({utc:new Date().toISOString(),ban:pg.result.ban,ca:pg.result.ca,service:pg.result.service,panel:id,quan_sat:p.text,loai:[6,9,10,22,24,25,26,29].includes(id)?'i':'iii',can_cu:[6,9,10,22,24,25,26,29].includes(id)?'Đối chiếu dữ liệu nguồn trong file trang':'Cần đối chiếu snapshot cùng ca/service; không suy nguyên nhân',trang:pg.label});}
  await this.save(pg);return {ban:pg.result.ban,ca:pg.result.ca,status:pg.result.status,checks:pg.result.checks,errors};
 }
 async resume(ban,ca){const r=this.pages.find(x=>x.ban===ban&&x.ca===ca);if(!r)throw Error('Chưa có trang');const ordinal=this.index.ban.findIndex(b=>b.ban===ban)*22+this.index.ban.find(b=>b.ban===ban).cac_ca.findIndex(c=>c.ca===ca)+1;this.current={label:String(ordinal).padStart(3,'0')+'-trang-'+ban.replaceAll('+','_')+'-'+ca,result:r};return this.current;}
}
