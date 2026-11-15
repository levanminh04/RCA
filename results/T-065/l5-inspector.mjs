// Import only inside cua_repl. All browser interaction uses the passed tab.
import fs from 'node:fs/promises';
const base='D:/RCA-flashticket/results/T-065/kiem/003-trinh-duyet';
export class L5Inspector {
 constructor(tab,runner){this.tab=tab;this.runner=runner;}
 async open(slot,label){
  this.slot=slot;this.label=label;
  const tab=this.tab,r=this.runner;
  await r.focus(slot.panel,label);
  await r.action('Phím i trên panel '+slot.panel,'Inspect theo phím tắt đã quan sát trong menu',()=>r.panel(slot.panel).getByRole('heading').press('i'),label+'-inspect');
  await tab.playwright.getByRole('tab',{name:'Query',exact:true}).waitFor({state:'visible',timeout:15000});
  return {label,stage:'query_next'};
 }
 async query(){
  const tab=this.tab,r=this.runner,label=this.label;
  await r.action('Query Inspector','Request và response qua giao diện',()=>tab.playwright.getByRole('tab',{name:'Query',exact:true}).click(),label+'-query');
  await tab.playwright.getByRole('heading',{name:'Query inspector',exact:true}).waitFor({state:'visible',timeout:15000});
  await r.action('Refresh Inspector hiện tại','Không dùng để quy nguyên nhân lịch sử',()=>tab.playwright.getByRole('button',{name:'Refresh',exact:true}).click(),label+'-refresh');
  await tab.playwright.getByRole('button',{name:'Expand all',exact:true}).waitFor({state:'visible',timeout:15000});
  await r.action('Expand all Inspector','Lưu đầy đủ cây JSON đang hiển thị',()=>tab.playwright.getByRole('button',{name:'Expand all',exact:true}).click(),label+'-expand');
  return {label,stage:'capture_next'};
 }
 async capture(){
  const tab=this.tab,slot=this.slot,label=this.label;
  await tab.playwright.getByRole('button',{name:'Collapse all',exact:true}).waitFor({state:'visible',timeout:10000});
  const raw=await tab.playwright.getByRole('dialog').innerText(),dom=await tab.playwright.domSnapshot(),url=await tab.url();
  const text=raw.replaceAll('\\"','"');
  const from=raw.match(/\bfrom:"([^"\n]+)"/)?.[1],to=raw.match(/\bto:"([^"\n]+)"/)?.[1];
  const checks={query:text.includes(slot.query),from:Number(from)===slot.window[0],to:Number(to)===slot.window[1],request:raw.includes('request:Object'),response:raw.includes('response:Object'),not_nan:!raw.includes('from:"NaN"')&&!raw.includes('to:"NaN"')};
  const record={utc:new Date().toISOString(),...slot,url,observed:{from,to,row_summary:raw.match(/[A-Z]:\d+ rows/g),statuses:raw.match(/status:\d+/g)},checks,passed:Object.values(checks).every(Boolean),raw:label+'-request-response.txt',dom:label+'-dom.txt',image:'anh/'+label+'.jpg',historical_class_unchanged:'iii',format:'Full expanded rendered Query Inspector tree; clipboard returned empty, so no claim of native JSON export.'};
  await fs.writeFile(base+'/'+record.raw,raw);await fs.writeFile(base+'/'+record.dom,dom);await fs.writeFile(base+'/'+record.image,await tab.screenshot({fullPage:false}));
  await fs.writeFile(base+'/'+label+'.json',JSON.stringify(record,null,2)+'\n');
  await fs.appendFile(base+'/ui06-inspectors.jsonl',JSON.stringify(record)+'\n');
  return {label,checks,rows:record.observed.row_summary,statuses:record.observed.statuses,bytes:raw.length};
 }
 async close(){return this.runner.action('Đóng Inspector','Tiếp panel kế',()=>this.tab.playwright.getByRole('button',{name:'Close',exact:true}).click(),this.label+'-close');}
}
