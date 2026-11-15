import fs from 'node:fs/promises';
const root='D:/RCA-flashticket',base=root+'/results/T-065';
const read=async p=>JSON.parse((await fs.readFile(root+'/'+p,'utf8')).replace(/^\uFEFF/,''));
const index=await read('results/T-064/ban-xuat/chi-muc-ban.json');
const cases=['1ad3afeb','00eaea92','2e2a5541','eb48d6b3','4af494a5','19b17e22'];
const svcs={'1ad3afeb':['event-service','booking-service'],'00eaea92':['payment-service','booking-service'],'2e2a5541':['booking-service','payment-service'],'eb48d6b3':['booking-service','event-service'],'4af494a5':['payment-service','event-service'],'19b17e22':['booking-service','event-service']};
const plan=[];
for(const ca of cases)for(const b of index.ban){
 const d=await read('results/T-065/du-lieu-l4/'+b.ban+'/vue/'+ca+'.json');
 const services=[];
 for(const s of svcs[ca]){
  const z=await read('results/T-065/du-lieu-l4/'+b.ban+'/thao-tac-vue/'+ca+'/'+s+'.json'),ops=z.thao_tac;
  const first=(ca==='1ad3afeb'&&s==='event-service'?ops.find(o=>o.ten==='SELECT event_db'):null)||(ca==='19b17e22'?ops.find(o=>o.loai==='message'&&o.co_m1):null)||ops.find(o=>o.co_m1)||ops[0];
  const second=ops.find(o=>o.id!==first.id&&o.lien_ket?.some(l=>l.kho==='prometheus'))||ops.find(o=>o.id!==first.id);
  services.push({service:s,co_thao_tac_co:ops.some(o=>o.co_m1),tong_thao_tac:ops.length,ops:[first,second].map(o=>({id:o.id,ten:o.ten,loai:o.loai,co_m1:o.co_m1,lien_ket:o.lien_ket,ly_do_khong_prometheus:o.ly_do_khong_prometheus}))});
 }
 plan.push({ban:b.ban,ca,nguon:index.ban[0].cac_ca.find(c=>c.ca===ca).nguon,cua_so_ms:d.cua_so_ms,top1:d.ranking_rows[0].entity,top1_covered:svcs[ca].includes(d.ranking_rows[0].entity),services});
}
const r={utc:new Date().toISOString(),ly_do:'Ba ca T-062 đầu bao gồm ca bắt buộc 1ad3afeb và các kết quả trên tải đọc; ba ca dev2 đầu bao gồm HTTP/SQL và message. Chọn hai service chung qua ba bản, bao phủ service đứng đầu của từng bản. Chọn ít nhất một thao tác có cờ nếu có, thêm thao tác có metric route nếu có. Không đọc nhãn để chọn. Tại 19b17e22 ưu tiên message có cờ để kiểm phân loại; tại 1ad3afeb bắt buộc SELECT event_db.',cases:plan};
await fs.writeFile(base+'/kiem/003-trinh-duyet/mau-sau-plan.json',JSON.stringify(r,null,2)+'\n');
console.log(JSON.stringify({case_versions:plan.length,services:plan.flatMap(p=>p.services).length,ops:plan.flatMap(p=>p.services.flatMap(s=>s.ops)).length,links:plan.flatMap(p=>p.services.flatMap(s=>s.ops.flatMap(o=>o.lien_ket))).length,top1:plan.every(p=>p.top1_covered)}));
