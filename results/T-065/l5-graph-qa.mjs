import fs from 'node:fs/promises';
const base='D:/RCA-flashticket/results/T-065',out=base+'/kiem/003-trinh-duyet';
const read=async p=>JSON.parse((await fs.readFile(p,'utf8')).replace(/^\uFEFF/,''));
export class L5GraphQA {
 constructor(runner,tab){this.r=runner;this.tab=tab;}
 async init(){
  this.services=await read(out+'/kiem-service-that.json');
  this.rows=await read(out+'/kiem-anh-graph.json').catch(e=>{if(e.code!=='ENOENT')throw e;return [];});
  return this.summary();
 }
 summary(){return {saved:this.rows.length,current:this.current?.i,zoom:this.current?.zoom};}
 async step(){
  if(!this.current){
   const i=this.services.findIndex((s,i)=>!this.rows.some(r=>r.index===i));if(i<0)return 'done';
   const s=this.services[i],data=await read(base+'/du-lieu-l4/'+s.ban+'/thao-tac-vue/'+s.ca+'/'+s.service+'.json');
   const url=new URL(s.url);url.searchParams.set('viewPanel','panel-23');url.searchParams.set('var-dv',s.service);url.searchParams.set('var-dv_svc',s.service);
   this.current={i,s,data,start:Date.now(),zoom:0};
   await this.r.action('Bổ sung ảnh graph '+i,'Đúng bản/ca/service, chỉ xem panel',()=>this.tab.goto(url.href),'graph-bo-sung-'+i+'-mo');return 'pending';
  }
  const c=this.current,p=this.r.panel(23);
  if(c.data.nut.length){try{await p.locator('[data-node-id="'+c.data.nut[0].id+'"]').waitFor({state:'attached',timeout:15000});}catch(error){await fs.appendFile(out+'/graph-qa-runtime.jsonl',JSON.stringify({utc:new Date().toISOString(),index:c.i,error:String(error),stage:'cho_node_dung_xong'})+'\n');if(Date.now()-c.start>120000)throw error;return 'pending';}}
  const dom=await this.tab.playwright.domSnapshot();
  if(dom.includes('Loading Grafana')||!(await p.getByRole('heading').textContent())?.includes(c.s.service))return 'pending';
  const graph=await p.evaluate(e=>{const box=x=>{const r=x.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,width:r.width,height:r.height};};return {panel:box(e),nodes:Array.from(e.querySelectorAll('[data-node-id]')).map(n=>({id:n.getAttribute('data-node-id'),text:n.textContent,stroke:n.querySelector('circle[stroke]')?.getAttribute('stroke'),radius:n.querySelector('circle')?.getAttribute('r'),box:box(n)})),edges:Array.from(e.querySelectorAll('[aria-label^="Edge from:"]')).map(n=>n.getAttribute('aria-label')),text:e.textContent};});
  const ids=graph.nodes.map(n=>n.id).sort(),expectedIds=c.data.nut.map(n=>n.id).sort();
  if(JSON.stringify(ids)!==JSON.stringify(expectedIds)||graph.text.includes('Computing layout'))return 'pending';
  const expectedEdges=c.data.canh.map(e=>'Edge from: '+e.source+' to: '+e.target).sort();
  const checks={nodes:JSON.stringify(ids)===JSON.stringify(expectedIds),edges:JSON.stringify([...graph.edges].sort())===JSON.stringify(expectedEdges),colors:c.data.nut.every(n=>graph.nodes.find(x=>x.id===n.id)?.stroke?.toLowerCase()===n.mau.toLowerCase()),radius:graph.nodes.every(n=>n.radius==='32'),titles:c.data.nut.every(n=>graph.nodes.find(x=>x.id===n.id)?.text.includes(n.ten))};
  if(!Object.values(checks).every(Boolean))throw Error('Graph DOM không khớp nguồn '+c.i+' '+JSON.stringify(checks));
  const rect=graph.panel;
  const fit=graph.nodes.every(n=>n.box.x>=rect.x-2&&n.box.right<=rect.right+2&&n.box.y>=rect.y+30&&n.box.bottom<=rect.bottom-20);
  const zoomEnabled=await p.getByRole('button',{name:'Zoom out',exact:true}).isEnabled();
  if(!fit&&c.zoom<8&&zoomEnabled){await this.r.action('Thu graph vừa khung '+c.i,'Thấy toàn bộ nút trong panel',()=>p.getByRole('button',{name:'Zoom out',exact:true}).click(),'graph-bo-sung-'+c.i+'-zoom'+c.zoom);c.zoom++;return 'continue';}
  const tag='graph-bo-sung-'+String(c.i).padStart(2,'0')+'-'+c.s.ban.replaceAll('+','_')+'-'+c.s.ca+'-'+c.s.service+(c.retryName||'');
  await fs.writeFile(out+'/'+tag+'.txt',dom);
  const views=[];
  const capture=async suffix=>{const visible=await p.evaluate(e=>{const r=e.getBoundingClientRect();return Array.from(e.querySelectorAll('[data-node-id]')).filter(n=>{const b=n.getBoundingClientRect();return b.x>=r.x&&b.right<=r.right&&b.y>=r.y+40&&b.bottom<=r.bottom-30;}).map(n=>n.getAttribute('data-node-id'));});await fs.writeFile(out+'/anh/'+tag+suffix+'.jpg',await this.tab.screenshot({fullPage:false}));views.push({anh:'anh/'+tag+suffix+'.png',visible_ids:visible});};
  await capture('');
  if(!fit){
   const x=Math.round(rect.right-80),y=Math.round((rect.y+rect.bottom)/2);
   for(const side of ['tren','duoi']){
    const delta=await p.evaluate((e,side)=>{const r=e.getBoundingClientRect(),ns=Array.from(e.querySelectorAll('[data-node-id]')).map(n=>n.getBoundingClientRect());return side==='tren'?r.y+48-Math.min(...ns.map(n=>n.y)):r.bottom-40-Math.max(...ns.map(n=>n.bottom));},side);
    await this.r.action('Kéo graph để thấy phần '+side+' '+c.i,'Chỉ đổi khung nhìn',()=>this.tab.drag([x,y],[x,Math.round(y+Math.max(-250,Math.min(250,delta)))]),tag+'-pan-'+side);await capture('-'+side);
   }
  }
  const covered=new Set(views.flatMap(v=>v.visible_ids)),missing=expectedIds.filter(id=>!covered.has(id));
  this.rows.push({utc:new Date().toISOString(),index:c.i,ban:c.s.ban,ca:c.s.ca,service:c.s.service,url:await this.tab.url(),checks,fit,zoom_min:!zoomEnabled,views,missing_visible_nodes:missing,zoom_out:c.zoom,wait_ms:Date.now()-c.start,measurement:'Từ mở View panel đến đối chiếu DOM và ảnh; gồm các lượt đọc/chụp/zoom, không là benchmark renderer.',source:'du-lieu-l4/'+c.s.ban+'/thao-tac-vue/'+c.s.ca+'/'+c.s.service+'.json',original:c.s.anh,anh:'anh/'+tag+'.png',dom:tag+'.txt',graph});
  await fs.writeFile(out+'/kiem-anh-graph.json',JSON.stringify(this.rows,null,2)+'\n');
  const status=await read(base+'/codex/L5-trang-thai.json');status.cap_nhat=new Date().toISOString();status.buoc='graph_QA '+this.rows.length+'/36';await fs.writeFile(base+'/codex/L5-trang-thai.json',JSON.stringify(status,null,2)+'\n');
  this.current=null;return 'saved';
 }
 async advance(max=5){for(let i=0;i<max;i++){const r=await this.step();if(r==='pending'||r==='done')break;}return this.summary();}
}
