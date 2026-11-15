import {json,read,lossless,write} from './lib.mjs';
// Giảm tài liệu Infinity phải đọc cho mỗi target; giữ dữ liệu đầy đủ ở file gốc.
export async function projectL4(){
 const idx=await json('results/T-064/ban-xuat/chi-muc-ban.json');let files=0;
 const pick=(o,ks)=>Object.fromEntries(ks.filter(k=>k in o).map(k=>[k,o[k]]));
 for(const b of idx.ban)for(const c of b.cac_ca){
  const root=`du-lieu-l4/${b.ban}`,d=lossless(await read(`results/T-065/${root}/${c.ca}.json`));
  await write(`${root}/vue/${c.ca}.json`,pick(d,['ban','ca','cua_so_ms','tu_utc','den_loai_tru','su_co','ranking_rows','canh_xep_hang','trang_thai_canh','region','co_m1','bang_chung','metric_links','gioi_han']));files++;
  for(const svc of new Set([...d.ranking_rows.map(r=>r.entity),...d.thao_tac.map(o=>o.chu)])){
   const s=lossless(await read(`results/T-065/${root}/thao-tac/${c.ca}/${svc}.json`));
   s.nut=s.nut.map(o=>({...pick(o,['id','ten','co_m1','ngoai_service','chu','trang_thai_m1','mau','loai']),don_vi_m1:pick(o.don_vi_m1||{},['e_len','e_xuong'])}));
   await write(`${root}/thao-tac-vue/${c.ca}/${svc}.json`,s);files++;
  }
 }
 return {files};
}
