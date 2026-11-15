import * as fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
export const HERE = path.dirname(fileURLToPath(import.meta.url));
export const ROOT = path.resolve(HERE, '../..');
export const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
export const read = p => fs.readFile(path.resolve(ROOT,p),'utf8');
export const json = async p => JSON.parse(await read(p));
// Giữ nguyên số nguyên ns của nguồn, không làm tròn khi mở rộng định dạng 0.2.
export const lossless = s => JSON.parse(s,(k,v,c) =>
  typeof v==='number' && !Number.isSafeInteger(v) && /^-?\d+$/.test(c.source)
    ? JSON.rawJSON(c.source) : v);
export const num = v => Number(v?.rawJSON ?? v);
export async function write(p, value) {
  p = path.resolve(HERE,p); await fs.mkdir(path.dirname(p),{recursive:true});
  await fs.writeFile(p,typeof value==='string'?value:JSON.stringify(value,null,1)+'\n','utf8');
}
export function explore(kho,query,window) {
  const type={tempo:'tempo',loki:'loki',prometheus:'prometheus'}[kho];
  const q={refId:'A',datasource:{type,uid:kho},...query};
  return '/explore?schemaVersion=1&orgId=1&panes='+encodeURIComponent(JSON.stringify({a:{
    datasource:kho,queries:[q],range:{from:String(window[0]),to:String(window[1]-1)}}}));
}
export const link = (kho,truy_van,w,pham_vi,ghi_chu='') => ({kho,loai:kho==='tempo'?'trace_tim_kiem':kho==='loki'?'log':'metric',
  cach_lay:'dan_xuat',truy_van,cua_so_ms:w,pham_vi,ghi_chu,
  url:explore(kho,kho==='tempo'?{queryType:'traceql',query:truy_van,limit:50,tableType:'traces'}:
    kho==='loki'?{expr:truy_van,queryType:'range',maxLines:200}:{expr:truy_van,range:true},w)});
export function existingLink(lk) {
  let q=lk.truy_van;
  if(lk.kho==='prometheus') {
    const entries=Object.entries(lk.bo_loc_chuoi||{});
    if(entries.length) {
      const filters=entries.map(([k,v])=>`label_replace(vector(1), ${JSON.stringify(k)}, ${JSON.stringify(v)}, "", "")`);
      q=`(${q}) and on(${entries.map(([k])=>k).join(',')}) (${filters.join(' * ')})`;
    }
  }
  return {...lk,...link(lk.kho,q,lk.cua_so_ms,'kenh_m1',lk.ghi_chu)};
}
export const attrs = a => Object.fromEntries((a||[]).map(x=>[x.key,
  x.value?.stringValue ?? x.value?.intValue ?? x.value?.doubleValue ?? x.value?.boolValue]));
export async function checkFile(rel,entry,base='results/T-062') {
  if(!entry) throw Error('Không có trong manifest: '+rel);
  const b=await fs.readFile(path.resolve(ROOT,base,rel)); const actual=hash(b);
  if(actual!==entry.sha256 || (entry.bytes!==undefined && b.length!==entry.bytes))
    throw Error('Hash lệch: '+base+'/'+rel);
  return {file:base+'/'+rel,sha256:actual,bytes:b.length};
}
export function assert(cond,msg) {if(!cond) throw Error(msg);}
export {fs,path};
