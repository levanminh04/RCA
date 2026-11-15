import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
const root='D:/RCA-flashticket', base=root+'/results/T-065', out=base+'/kiem/003-trinh-duyet';
const read=async p=>JSON.parse((await fs.readFile(p,'utf8')).replace(/^\uFEFF/,''));
const hash=async p=>crypto.createHash('sha256').update(await fs.readFile(p)).digest('hex');
const write=async(p,v)=>fs.writeFile(p,JSON.stringify(v,null,2)+'\n');
if(process.argv[2]==='init'){
 const old=await read(base+'/manifest.json'),idx=await read(root+'/results/T-064/ban-xuat/chi-muc-ban.json');
 const r={utc:new Date().toISOString(),index_sha256:await hash(root+'/results/T-064/ban-xuat/chi-muc-ban.json'),source:[],prior:[],prior_mismatch:[]};
 for(const b of idx.ban)for(const c of b.cac_ca){const actual=await hash(root+'/'+c.dau_ra);r.source.push({ban:b.ban,ca:c.ca,file:c.dau_ra,expected:c.sha256,actual,match:actual===c.sha256});}
 for(const [f,v] of Object.entries(old.files)){let actual=await hash(base+'/'+f);r.prior.push({file:f,match:actual===v.sha256});if(actual!==v.sha256)r.prior_mismatch.push({file:f,expected:v.sha256,actual});}
 await write(out+'/kiem-hash-dau.json',r);await fs.copyFile(base+'/manifest.json',base+'/codex/manifest-L4.json');
 console.log(JSON.stringify({source:r.source.length,source_bad:r.source.filter(x=>!x.match),prior:r.prior.length,prior_bad:r.prior_mismatch}));
}
if(process.argv[2]==='folder'){
 const before=await read(out+'/may-truoc.json');
 const prov='/opt/flash-ticket-obs/pinned/provisioning/dashboards';
 const provider=before.providers[prov+'/provider.yaml'];
 const next=provider.replace('    folder: RCA\n','').replace('foldersFromFilesStructure: false','foldersFromFilesStructure: true');
 await fs.mkdir(base+'/grafana-l5',{recursive:true});
 await fs.writeFile(base+'/grafana-l5/provider-truoc.yaml',provider);await fs.writeFile(base+'/grafana-l5/provider.yaml',next);
 const idx=await read(root+'/results/T-064/ban-xuat/chi-muc-ban.json');
 const bands=idx.ban.map(b=>b.ban+' ('+b.trang_thai+')').join('; ');
 const entries=[
 ['t065-l5-muc-luc','Mục lục RCA','Điểm bắt đầu; chọn đúng dashboard và mốc lưu trữ',bands,'22 ca × 3 bản hiện hành','T-065 / L5','14/11/2026','hiện hành'],
 ['t065-l4-rca','RCA — chọn bản M1 cùng ca','Chọn bản → ca → service → thao tác → bằng chứng',bands,'22 ca (9 T-062 + 13 dev2)','T-065 / L4','14/11/2026','hiện hành'],
 ['t065-l4-phat-lai','Phát lại có đáp án — T-062','Xem riêng đáp án đã tách sau khi xem kết quả',bands,'9 ca T-062 có đáp án; 13 dev2 chỉ có giới hạn','T-065 / L4','14/11/2026','hiện hành'],
 ['t065-rca','L3 — sự cố và thao tác M1','Mốc hồi quy giao diện lớp thao tác','P7 khóa','9 ca T-062','T-065 / L3','13/11/2026','lưu trữ'],
 ['t065-phat-lai','L3 — phát lại có đáp án','Mốc hồi quy trang phát lại','P7 khóa','9 ca T-062','T-065 / L3','13/11/2026','lưu trữ'],
 ['rca-g2','G2 bản 6 — xem sự cố','Mốc hồi quy dashboard G2','P7 khóa','9 ca T-062','T-062 / G1 bản 6','12/11/2026','lưu trữ'],
 ['rca-g2-phat-lai','G2 bản 6 — phát lại có đáp án','Mốc hồi quy phát lại G2','P7 khóa','9 ca T-062','T-062 / G1 bản 6','12/11/2026','lưu trữ']];
 const content='## Chọn nơi bắt đầu\n\n'+entries.map(([uid,name,use,version,count,task,date,status])=>`- **[${name}](/d/${uid})** — ${use}. Bản: ${version}. Số ca: ${count}. Nguồn giao diện: ${task}; ngày ${date}; **${status}**.`).join('\n\n')+'\n\n### Trạng thái và giới hạn\n\nP7 đã khóa. V032-H5b là đề xuất tạm. V041-R1-H1c+H5b+H8s1 là bản thay thế có đầu ra cạnh; chưa là bản cuối đã nghiệm thu.\n\nHai hash cấp bản P7 là null trong chỉ mục T-064; không suy hash từ file đầu ra. Dev bản 2 chưa có đáp án được cấp cho giao diện. Trang chính và mục lục không chứa đáp án. Span link message chưa hỗ trợ.\n\nNguồn bản và ca: results/T-064/ban-xuat/chi-muc-ban.json. Cửa sổ trang ca: [t−300,t+300).';
 const dash={uid:'t065-l5-muc-luc',id:null,version:1,title:'Mục lục RCA',tags:['RCA','T-065','L5','muc-luc'],timezone:'utc',editable:false,schemaVersion:42,refresh:'',time:{from:'now-1h',to:'now'},timepicker:{hidden:true},templating:{list:[]},panels:[{id:1,type:'text',title:'Mục lục RCA FlashTicket',gridPos:{x:0,y:0,w:24,h:30},options:{mode:'markdown',content}}]};
 await write(base+'/grafana-l5/t065-l5-muc-luc.json',dash);
 const dirs={start:'RCA FlashTicket/0 · Bắt đầu tại đây',current:'RCA FlashTicket/1 · Kết quả hiện hành',l3:'RCA FlashTicket/9 · Lưu trữ/L3 · P7 · 13-11',g2:'RCA FlashTicket/9 · Lưu trữ/G2 bản 6 · 12-11'};
 const moves=[['t065-l4-rca.json',dirs.current],['t065-l4-phat-lai.json',dirs.current],['t065-rca.json',dirs.l3],['t065-phat-lai.json',dirs.l3]];
 const jsonfiles=Object.keys(before.files).filter(f=>f.endsWith('.json')&&f.startsWith(prov+'/'));
 for(const f of jsonfiles){if(!moves.some(([name])=>f===prov+'/'+name))moves.push([path.basename(f),dirs.g2]);}
 const payload={provider:next,moves:moves.map(([name,dir])=>({name,dir,before:before.files[prov+'/'+name].sha256})),new_dir:dirs.start,dashboard:dash};
 await write(out+'/folder-plan.json',{...payload,reference:'https://grafana.com/docs/grafana/latest/administration/provisioning/#provision-folders-structure-from-filesystem-to-grafana'});
 const script=`import json, pathlib, hashlib, subprocess\nP=json.loads(${JSON.stringify(JSON.stringify(payload))})\nB=pathlib.Path('${prov}')\nassert not (pathlib.Path.home()/'rca-dieu-phoi/STOP').exists(), 'STOP'\nassert hashlib.sha256((B/'provider.yaml').read_bytes()).hexdigest()=='${before.files[prov+'/provider.yaml'].sha256}'\nfor m in P['moves']:\n assert hashlib.sha256((B/m['name']).read_bytes()).hexdigest()==m['before'], m['name']\n assert not (B/m['dir']/m['name']).exists()\nassert not (B/P['new_dir']/'t065-l5-muc-luc.json').exists()\nprint(subprocess.check_output(['date','-u','+%Y-%m-%dT%H:%M:%SZ'],text=True).strip(),flush=True)\nfor m in P['moves']:\n dest=B/m['dir']/m['name']; dest.parent.mkdir(parents=True,exist_ok=True); (B/m['name']).rename(dest); print('MOVE',m['name'],str(dest),hashlib.sha256(dest.read_bytes()).hexdigest(),flush=True)\np=B/P['new_dir']/'t065-l5-muc-luc.json'; p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(P['dashboard'],ensure_ascii=False,indent=2)+'\\n')\n(B/'provider.yaml').write_text(P['provider'])\nprint('PROVIDER',hashlib.sha256((B/'provider.yaml').read_bytes()).hexdigest(),flush=True)\nprint(subprocess.check_output(['docker','restart','flash-ticket-obs-grafana'],text=True).strip(),flush=True)\nprint(subprocess.check_output(['date','-u','+%Y-%m-%dT%H:%M:%SZ'],text=True).strip(),flush=True)\n`;
 await fs.writeFile(base+'/l5-folder-deploy.py',script);
 console.log(JSON.stringify({moves,root_json:jsonfiles.length,index:dash.uid,provider_sha256:await hash(base+'/grafana-l5/provider.yaml')}));
}
if(process.argv[2]==='verify-folder'){
 const a=await read(out+'/may-truoc.json'),b=await read(out+'/folder-sau.json'),p=await read(out+'/folder-plan.json'),prov='/opt/flash-ticket-obs/pinned/provisioning/dashboards';
 const r={utc:new Date().toISOString(),method:'nested',dashboards:[],unchanged:[],errors:[]};
 for(const m of p.moves){const actual=b.files[prov+'/'+m.dir+'/'+m.name]?.sha256; r.unchanged.push({file:m.name,before:m.before,after:actual,match:actual===m.before});if(actual!==m.before)r.errors.push(m.name);}
 for(const d of b.dashboards){const old=a.dashboards.find(x=>x.uid===d.uid);r.dashboards.push({uid:d.uid,folder:d.meta?.folderTitle,path:d.meta?.provisionedExternalId,existing:!!old,uid_unchanged:old?d.uid===old.uid:null});}
 r.rca_dashboards=b.dashboards.filter(d=>d.uid.startsWith('t065-')||d.uid.startsWith('rca-g2')).length;
 r.nested=b.folders.filter(f=>f.data?.parentUid).map(f=>({uid:f.data.uid,title:f.data.title,parentUid:f.data.parentUid,parents:f.data.parents?.map(x=>({uid:x.uid,title:x.title}))}));
 r.compose_unchanged=a.files['/opt/flash-ticket-obs/pinned/compose.json'].sha256===b.files['/opt/flash-ticket-obs/pinned/compose.json'].sha256;
 r.root_json=Object.keys(b.files).filter(f=>f.startsWith(prov+'/')&&f.endsWith('.json')&&!f.slice(prov.length+1).includes('/'));
 await write(out+'/kiem-folder.json',r);console.log(JSON.stringify({rca:r.rca_dashboards,unchanged:r.unchanged.length,errors:r.errors,nested:r.nested.length,compose_unchanged:r.compose_unchanged,root_json:r.root_json}));
}
