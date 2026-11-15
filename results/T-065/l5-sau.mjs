// Chạy trong node_repl của Browser Use, truyền các binding tab và browser.
import fs from 'node:fs/promises';
const root='D:/RCA-flashticket',base=root+'/results/T-065/kiem/003-trinh-duyet';
const read=async p=>JSON.parse((await fs.readFile(p,'utf8')).replace(/^\uFEFF/,''));
const write=async(p,v)=>fs.writeFile(base+'/'+p,JSON.stringify(v,null,2)+'\n');
const epoch=v=>/^\d+$/.test(v||'')?Number(v):Date.parse(v);
const identify=u=>{const x=new URL(u);return {ban:x.searchParams.get('var-ban'),ca:x.searchParams.get('var-ca'),service:x.searchParams.get('var-dv'),op:x.searchParams.get('var-op'),from:epoch(x.searchParams.get('from')),to:epoch(x.searchParams.get('to'))};};
const safe=s=>s.replace(/\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b/g,'[REDACTED]').replace(/((?:password|authorization|api[_-]?key)\s*[=:]\s*["']?)[^\s"',}]+/ig,'$1[REDACTED]');
export function editorFromDOM(dom){const block=dom.match(/  - code:\n([\s\S]*?)    - textbox/);if(!block)return '';return block[1].split('\n').filter(l=>l.startsWith('    - generic: ')).map(l=>{const v=l.slice('    - generic: '.length);try{return JSON.parse(v);}catch{return v;}}).join('');}
export class L5Deep {
 constructor(runner,browser){this.r=runner;this.tab=runner.tab;this.browser=browser;}
 async init(){this.plan=(await read(base+'/mau-sau-plan.json')).cases;this.links=await read(base+'/kiem-lien-ket-that.json').catch(()=>[]);this.ops=await read(base+'/kiem-thao-tac-that.json').catch(()=>[]);this.services=await read(base+'/kiem-service-that.json').catch(()=>[]);this.versions=await read(base+'/kiem-doi-ban-that.json').catch(()=>[]);this.s=await read(base+'/sau-tien-do.json').catch(()=>({pair:0,service:0,op:0,link:0,stage:'case',pending:null}));this.savedUTC=this.s.utc;if(this.s.pending)this.child=await this.browser.tabs.get(this.s.pending.tabId);return this.summary();}
 summary(){return {pair:this.s.pair,service:this.s.service,op:this.s.op,link:this.s.link,stage:this.s.stage,pending:this.s.pending?.kho,links:this.links.length,ops:this.ops.length,services:this.services.length,done:this.s.pair>=this.plan.length};}
 get p(){return this.plan[this.s.pair];}get svc(){return this.p.services[this.s.service];}get op(){return this.svc.ops[this.s.op];}
 tag(s){return 'sau-'+this.s.pair+'-'+this.p.ban.replaceAll('+','_')+'-'+this.p.ca+'-'+this.svc.service+'-'+s;}
 async assertCurrent(){
  const saved=await read(base+'/sau-tien-do.json').catch(error=>{if(error.code==='ENOENT')return {};throw error;});
  if(saved.utc!==this.savedUTC)throw Error('Checkpoint trên đĩa đã đổi. Tạo L5Deep mới và gọi init() trước khi làm tiếp.');
 }
 async save(){
  await this.assertCurrent();
  await write('kiem-lien-ket-that.json',this.links);await write('kiem-thao-tac-that.json',this.ops);await write('kiem-service-that.json',this.services);await write('kiem-doi-ban-that.json',this.versions);
  this.savedUTC=new Date().toISOString();
  await write('sau-tien-do.json',{...this.s,utc:this.savedUTC});
  await fs.writeFile(root+'/results/T-065/codex/L5-trang-thai.json',JSON.stringify({ten:'L5',trang_thai:'dang_chay',nguon:'codex-app',cap_nhat:this.savedUTC,buoc:'kiem_sau '+JSON.stringify(this.summary())},null,2));
 }
 async case(){
  const current=identify(await this.tab.url());
  if(current.ca!==this.p.ca){const url=this.r.pages.find(x=>x.ban===this.p.ban&&x.ca===this.p.ca).url;await this.r.action('Mở mẫu sâu '+this.p.ca,'Đúng ca và cửa sổ từ nguồn',()=>this.tab.goto(url),this.tag('mo-ca'));this.s.stage='case-wait';await this.save();return 'pending';}
  if(current.ban!==this.p.ban){
   await this.r.action('Mở bộ chọn bản','Các bản của cùng ca',()=>this.tab.playwright.getByRole('combobox',{name:'ban',exact:true}).click(),this.tag('ban-menu'));
   const option=this.tab.playwright.getByRole('option').filter({hasText:this.p.ban});
   await this.r.action('Chọn bản '+this.p.ban,'Giữ ca/service/cửa sổ',()=>option.click(),this.tag('ban-chon'));
   const after=identify(await this.tab.url());const check={ban:after.ban===this.p.ban,ca:after.ca===current.ca,service:after.service===current.service,window:after.from===current.from&&after.to===current.to};this.versions.push({utc:new Date().toISOString(),before:current,after,checks:check});if(!Object.values(check).every(Boolean))throw Error('Đổi bản không giữ trạng thái: '+JSON.stringify(check));
  }
  this.s.stage='service';await this.save();return 'continue';
 }
 async service(){
  const expected = this.svc.service;
  await this.r.focus(4,this.tag('service-rank'));
  const link=this.r.panel(4).getByRole('link',{name:expected,exact:true});
  const href=await link.getAttribute('href');
  const target=identify(new URL(href,await this.tab.url()).href);
  if(target.service!==expected||target.ban!==this.p.ban||target.ca!==this.p.ca||target.from!==this.p.cua_so_ms[0]||target.to!==this.p.cua_so_ms[1]-1)return 'pending';
  if(identify(await this.tab.url()).service!==expected){
   await this.r.action('Bấm service '+expected,'Bảng/đồ thị thao tác đúng service',()=>link.click(),this.tag('service-chon'));
   if(identify(await this.tab.url()).service!==expected)return 'pending';
  }
  await this.r.focus(22,this.tag('service-bang'));
  this.s.graphStart=Date.now();
  await this.r.focus(23,this.tag('service-graph'));
  this.s.stage='graph';await this.save();return 'continue';
 }
 async graph(){
  if(identify(await this.tab.url()).service!==this.svc.service)throw Error('Service trong URL không khớp lúc kiểm đồ thị');
  const title=await this.r.panel(23).getByRole('heading').textContent();
  if(!title?.includes(this.svc.service))return 'pending';
  const dom=await this.tab.playwright.domSnapshot();
  const graphDom=await this.r.panel(23).textContent();
  const graphStart=dom.indexOf('region "Đồ thị thao tác');
  const graphAX=graphStart<0?'':dom.slice(graphStart).split('\n    - region ').at(0);
  if(!graphAX.includes('Node:')&&!graphDom.includes('OK')&&!graphDom.includes('LOW_SUPPORT')&&!graphDom.includes('ngoài service'))return 'pending';
  const readyMs=Date.now()-this.s.graphStart;
  await this.r.action('Đưa đồ thị vào vùng ảnh','Thấy tiêu đề và vùng đồ thị',()=>this.r.panel(23).getByRole('heading').click(),this.tag('graph-view'));
  const out=this.r.panel(23).getByRole('button',{name:'Zoom out',exact:true});
  if(await out.count()&&await out.isEnabled())await this.r.action('Thu nhỏ đồ thị','Xem các nút/cạnh trong khung',()=>out.click(),this.tag('graph-zoom0'));
  const rect=await this.r.panel(23).evaluate(e=>{const r=e.getBoundingClientRect();return {top:r.top,bottom:r.bottom,viewport:window.innerHeight};});
  if(rect.bottom>rect.viewport&&rect.top>0){
   const position=await this.r.panel(23).evaluate(e=>{const r=e.getBoundingClientRect();return [Math.round(r.right-16),Math.round(Math.max(120,Math.min(r.top+40,window.innerHeight-20)))];});
   await this.r.action('Cuộn để thấy vùng đồ thị','Tiêu đề và nút cùng trong khung ảnh',()=>this.tab.ax.scroll(position,'down',0.43),this.tag('graph-scroll'));
  }
  const shot=await this.r.shot(this.tag('graph'));
  this.services.push({utc:new Date().toISOString(),ban:this.p.ban,ca:this.p.ca,service:this.svc.service,top1:this.p.top1,top1_covered:this.p.top1_covered,total_operations:this.svc.tong_thao_tac,url:await this.tab.url(),graph_wait_ms:readyMs,anh:shot,graph_dom:safe(graphDom),kiem:'Thời gian từ focus đến khi đồ thị có trạng thái nút. DOM xác nhận tên; kiểm canvas bằng ảnh. Số chi tiết đối chiếu API L4.'});
  this.s.stage='op';await this.save();return 'continue';
 }
 async operation(){
  if(identify(await this.tab.url()).service!==this.svc.service)throw Error('Service trong URL không khớp lúc chọn thao tác');
  await this.r.action('Mở bộ chọn thao tác','Chọn thao tác trong service',()=>this.tab.playwright.getByRole('combobox',{name:'op',exact:true}).click(),this.tag('op-menu-'+this.s.op));
  await this.r.action('Lọc thao tác '+this.op.ten,'Đúng tên trong nguồn',()=>this.tab.playwright.getByRole('combobox',{name:'op',exact:true}).fill(this.op.ten),this.tag('op-loc-'+this.s.op));
  await this.r.action('Chọn thao tác '+this.op.ten,'ID thao tác đúng nguồn',()=>this.tab.playwright.getByRole('option',{name:this.op.ten,exact:true}).click(),this.tag('op-chon-'+this.s.op));
  await this.r.focus(24,this.tag('op-chi-tiet-'+this.s.op));await this.r.focus(25,this.tag('op-bang-chung-'+this.s.op));
  this.s.stage='op-wait';await this.save();return 'continue';
 }
 async opReady(){
  const observed=await this.r.panel(25).getByRole('link').evaluateAll(es=>es.map(e=>({text:e.textContent,href:e.getAttribute('href')})));
  if(!observed.length)return 'pending';
  const current=identify(await this.tab.url());const checks={op:current.op===this.op.id,ca:current.ca===this.p.ca,ban:current.ban===this.p.ban,service:current.service===this.svc.service,window:current.from===this.p.cua_so_ms[0]&&current.to===this.p.cua_so_ms[1]-1,links:this.op.lien_ket.every(l=>observed.some(x=>x.href===l.url))};
  const detail=await this.r.table(24);this.ops.push({utc:new Date().toISOString(),ban:this.p.ban,ca:this.p.ca,service:this.svc.service,op:this.op.id,ten:this.op.ten,loai:this.op.loai,co_m1:this.op.co_m1,expected:this.op,observed_links:observed,detail,checks,url:await this.tab.url()});
  if(!Object.values(checks).every(Boolean))throw Error('Thao tác/link không khớp '+JSON.stringify(checks));
  this.s.link=0;this.s.stage='link';await this.save();return 'continue';
 }
 async openLink(){
  if(this.s.link>=this.op.lien_ket.length){this.s.op++;this.s.link=0;if(this.s.op>=2){this.s.op=0;this.s.service++;this.s.stage='service';if(this.s.service>=2){this.s.service=0;this.s.pair++;this.s.stage='case';}}else this.s.stage='op';await this.save();return 'continue';}
  const lk=this.op.lien_ket[this.s.link];
  if(this.links.some(x=>x.ban===this.p.ban&&x.ca===this.p.ca&&x.service===this.svc.service&&x.op===this.op.id&&x.kho===lk.kho)){this.s.link++;await this.save();return 'continue';}
  const before=await this.tab.url(),tabs=await this.browser.tabs.list();const utc=new Date().toISOString();
  let clickError=null;
  try{await this.r.panel(25).getByRole('link',{name:lk.kho+' ↗',exact:true}).click({timeoutMs:5000});}catch(error){clickError=String(error);}
  const created=(await this.browser.tabs.list()).filter(t=>{
   if(tabs.some(x=>x.id===t.id)||!t.url?.startsWith('http://127.0.0.1:13000/explore'))return false;
   try{
    const [pane]=Object.values(JSON.parse(new URL(t.url).searchParams.get('panes')));
    const q=pane.queries[0];
    return pane.datasource===lk.kho&&(q.query??q.expr)===lk.truy_van&&epoch(pane.range.from)===this.p.cua_so_ms[0]&&epoch(pane.range.to)===this.p.cua_so_ms[1]-1;
   }catch{return false;}
  });
  if(created.length!==1)throw Error(clickError??'Không có đúng một tab Explore mới khớp nguồn');
  this.child=await this.browser.tabs.get(created[0].id);this.s.pending={tabId:created[0].id,kho:lk.kho,expected:lk,utc,before,tag:this.tag('op'+this.s.op+'-'+lk.kho)};
  await fs.appendFile(base+'/nhat-ky-bam.jsonl',JSON.stringify({stt:++this.r.seq,utc,url_truoc:before,url_sau:created[0].url,hanh_dong:'Bấm bằng chứng '+lk.kho,ky_vong:'Đúng datasource/query/window, đọc dữ liệu rồi quay lại',quan_sat:'Mở tab Explore riêng',loi_cong_cu:clickError,ket_qua:'cho_doc_Explore',anh:null})+'\n');
  await this.save();return 'pending';
 }
 async consume(){
  const pending=this.s.pending,rawURL=await this.child.url();
  if(rawURL.includes('/login'))throw Error('Grafana đăng xuất — dừng trình duyệt');
  const dom=await this.child.playwright.domSnapshot();
  if(dom.includes('Loading Grafana')||dom.includes('Loading editor')||!dom.includes('heading "Explore"'))return 'pending';
  const panes=Object.values(JSON.parse(new URL(rawURL).searchParams.get('panes')));if(panes.length!==1)throw Error('Explore không có đúng một pane');
  const pane=panes[0],q=pane.queries[0],expected=pending.expected;
  const check={datasource:pane.datasource===expected.kho,query:(q.query??q.expr)===expected.truy_van,window:epoch(pane.range.from)===this.p.cua_so_ms[0]&&epoch(pane.range.to)===this.p.cua_so_ms[1]-1,query_dom:editorFromDOM(dom)===expected.truy_van||dom.includes(expected.truy_van.replaceAll('"','\\"'))||dom.includes(expected.truy_van)};
  if(!check.datasource||!check.query||!check.window)throw Error('Explore sai datasource, truy vấn hoặc khung giờ');
  if(!check.query_dom){
   await fs.writeFile(base+'/'+pending.tag+'-editor-chua-xac-nhan.txt',safe(dom));
   return 'pending';
  }
  let hasData=null;
  if(expected.kho==='tempo'){if(dom.includes('row "Expand row '))hasData=true;else if(/No (traces|data)|No results/i.test(dom))hasData=false;}
  if(expected.kho==='loki'){if(dom.includes('No logs found.'))hasData=false;else if(/button "Log menu"|Expand log|log-row|Log row|Log line|button "Show context"|[Ll]ines returned/.test(dom))hasData=true;}
  if(expected.kho==='prometheus'){if(dom.includes('button "All series selected"'))hasData=true;else if(/No data|No results/i.test(dom))hasData=false;}
  if(hasData===null){await fs.writeFile(base+'/'+pending.tag+'-chua-phan-xu.txt',safe(dom));return 'pending';}
  const sanitized=safe(dom),secret=sanitized!==dom;await fs.writeFile(base+'/'+pending.tag+'.txt',sanitized);
  let shot=null;if(!secret){await fs.writeFile(base+'/anh/'+pending.tag+'.jpg',await this.child.screenshot({fullPage:false}));shot='anh/'+pending.tag+'.png';}
  const item={utc:new Date().toISOString(),ban:this.p.ban,ca:this.p.ca,service:this.svc.service,op:this.op.id,ten:this.op.ten,kho:expected.kho,url:rawURL,datasource:pane.datasource,query:q.query??q.expr,range:[epoch(pane.range.from),epoch(pane.range.to)],checks:check,co_du_lieu:hasData,dom:pending.tag+'.txt',anh:shot,loai_rong:hasData?null:'iii',can_cu:hasData?'DOM kết quả/legend và ảnh':'Cần đối chiếu API/snapshot chính xác query/window; không suy nguyên nhân',image_skipped_sensitive:secret};this.links.push(item);
  await fs.appendFile(base+'/nhat-ky-bam.jsonl',JSON.stringify({stt:++this.r.seq,utc:item.utc,url_truoc:pending.before,url_sau:rawURL,hanh_dong:'Đọc Explore '+expected.kho,ky_vong:'Datasource/query/window khớp nguồn',quan_sat:{checks:check,co_du_lieu:hasData},ket_qua:Object.values(check).every(Boolean)?'khop_nguon':'loi',anh:shot})+'\n');
  await this.child.close();this.s.pending=null;this.child=null;this.s.link++;await this.tab.playwright.domSnapshot();await this.save();return 'continue';
 }
 async step(){
  await this.assertCurrent();
  if(this.s.pair>=this.plan.length)return 'done';
  if(this.s.pending)return this.consume();
  if(this.s.stage==='case')return this.case();
  if(this.s.stage==='case-wait'){const dom=await this.tab.playwright.domSnapshot();if(dom.includes('Loading Grafana'))return 'pending';this.s.stage='case';return this.case();}
  if(this.s.stage==='service')return this.service();if(this.s.stage==='graph')return this.graph();if(this.s.stage==='op')return this.operation();if(this.s.stage==='op-wait')return this.opReady();if(this.s.stage==='link')return this.openLink();throw Error('Unknown stage');
 }
 async advance(max=6){const start=Date.now();for(let i=0;i<max;i++){const result=await this.step();if(result==='pending'||result==='done'||Date.now()-start>25000)break;}return this.summary();}
}
