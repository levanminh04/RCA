import fs from 'node:fs/promises';
import crypto from 'node:crypto';

const base='results/T-065';
const output=base+'/kiem/003-trinh-duyet';
const read=async file=>JSON.parse((await fs.readFile(file,'utf8')).replace(/^\uFEFF/,''));
const versions=(await read('results/T-064/ban-xuat/chi-muc-ban.json')).ban.map(row=>row.ban);
const dashboards=await Promise.all(['t065-l4-rca','t065-l4-phat-lai'].map(uid=>read(base+'/grafana-l5/ui04/'+uid+'.json')));

if(process.argv[2]==='prepare'){
 const jobs=[];
 for(const ban of versions){
  for(const [ca,svc,op]of [['1ad3afeb','event-service','o7a1989261ced824f348c'],['4af494a5','payment-service','oe819fc37fe58d0462c15']]){
   const data=await read(base+'/du-lieu-l4/'+ban+'/thao-tac-vue/'+ca+'/'+svc+'.json');
   const operation=data.thao_tac.find(row=>row.id===op);
   if(!operation)throw Error('Thao tác mẫu thiếu '+ban+'/'+ca+'/'+op);
   const expected=[
    ['Thao tác',operation.ten],['Trạng thái',operation.trang_thai_m1],
    ['e tăng',operation.don_vi_m1?.e_len],['e giảm',operation.don_vi_m1?.e_xuong],
    ['Kênh có cờ',operation.kenh_co.map(row=>row.ma).join('; ')],
    ['Span gốc',operation.goc],['Span mồ côi',operation.mo_coi],
    ['Đích quan sát',operation.dich_quan_sat.join(', ')],
    ['Giới hạn metric',operation.ly_do_khong_prometheus]
   ];
   const target=JSON.parse(JSON.stringify(dashboards[0].panels.find(p=>p.id===24).targets[0]).replaceAll('${ban}',ban).replaceAll('${ca}',ca).replaceAll('${dv}',svc).replaceAll('${op}',op));
   jobs.push({key:ban+'/'+ca+'/detail',panel:24,ban,ca,service:svc,op,expected,request:{from:String(data.cua_so_ms[0]),to:String(data.cua_so_ms[1]-1),queries:[{...target,intervalMs:15000,maxDataPoints:1000}]}});
  }
  for(const ca of ['2e2a5541','4af494a5']){
   const data=await read(base+'/du-lieu-l4/'+ban+'/phat-lai/'+ca+'.json');
   const target=JSON.parse(JSON.stringify(dashboards[1].panels.find(p=>p.id===7).targets[0]).replaceAll('${ban}',ban).replaceAll('${ca}',ca));
   jobs.push({key:ban+'/'+ca+'/replay',panel:7,ban,ca,expected:data.phat_lai?[
    ['Cảnh báo',data.phat_lai.canh_bao],['Thành phần tiêm',data.phat_lai.thanh_phan_tiem],
    ['Họ lỗi',data.phat_lai.ho_loi],['Ô lỗi',data.phat_lai.o_loi],
    ['Root khai trước',data.phat_lai.root_khai_truoc],['Tập chấp nhận',data.phat_lai.tap_chap_nhan.join(', ')],
    ['Sức khỏe',data.phat_lai.suc_khoe===null?null:JSON.stringify(data.phat_lai.suc_khoe)],['Mốc xác nhận',data.phat_lai.moc_xac_nhan_utc],
    ['Nguồn đáp án',data.phat_lai.nguon_dap_an.join(', ')],['Hash đáp án',JSON.stringify(data.phat_lai.sha256_dap_an)],
    ['Giới hạn',data.gioi_han]
   ]:[['Giới hạn',data.gioi_han]],request:{from:String(data.cua_so_ms[0]),to:String(data.cua_so_ms[1]-1),queries:[{...target,intervalMs:15000,maxDataPoints:1000}]}});
  }
 }
 await fs.writeFile(output+'/ui04-plan.json',JSON.stringify(jobs,null,2)+'\n');
 const prefix=(await fs.readFile(base+'/l5-obs.py','utf8')).split("if sys.argv[1]=='inventory'")[0];
 const selected=process.argv[3]==='replay'?jobs.filter(job=>job.panel===7&&job.ca==='2e2a5541'):jobs;
 const payload=Buffer.from(JSON.stringify(selected.map(({key,request})=>({key,request})))).toString('base64');
 const script=prefix+'\nJOBS=json.loads(base64.b64decode("'+payload+'"))\n'+
  'for job in JOBS:\n'+
  '    assert not (pathlib.Path.home()/"rca-dieu-phoi/STOP").exists(), "STOP"\n'+
  '    result=api("/api/ds/query","POST",job["request"])\n'+
  '    rows=[]\n'+
  '    errors=[]\n'+
  '    for entry in result["data"].get("results",{}).values():\n'+
  '        if entry.get("error"): errors.append(entry["error"])\n'+
  '        for frame in entry.get("frames",[]):\n'+
  '            fields=frame["schema"]["fields"]\n'+
  '            values=frame["data"]["values"]\n'+
  '            rows.extend({field["name"]:values[k][i] for k,field in enumerate(fields)} for i in range(len(values[0]) if values else 0))\n'+
  '    print(json.dumps({"utc":utc(),"key":job["key"],"http":result["http"],"errors":errors,"rows":rows},ensure_ascii=False),flush=True)\n';
 await fs.writeFile(base+'/l5-ui-kiem.py',script);
 console.log(JSON.stringify({jobs:selected.length}));
}else if(process.argv[2]==='verify'){
 const jobs=await read(output+'/ui04-plan.json');
 const lines=(await fs.readFile(output+'/ui04-api.jsonl','utf8')).replace(/^\uFEFF/,'').trim().split('\n').map(line=>JSON.parse(line));
 const report=[];
 for(const job of jobs){
  const result=lines.find(row=>row.key===job.key);
  if(!result)throw Error('Thiếu phản hồi '+job.key);
  const fields=new Map(result.rows.map(row=>[row.a_truong,row.b_gia_tri]));
  const mismatches=job.expected.filter(([key,expected])=>{
   const seen=fields.get(key)??'';
   if(typeof expected==='number')return Math.abs(Number(seen)-expected)>1e-12*Math.max(1,Math.abs(expected));
   if(key==='Hash đáp án')return JSON.stringify(JSON.parse(seen))!==expected;
   return String(seen)!==String(expected??'');
  });
  const passed=result.http===200&&!result.errors.length&&result.rows.length===job.expected.length&&!mismatches.length;
  report.push({key:job.key,panel:job.panel,rows:result.rows.length,expected_rows:job.expected.length,passed,mismatches});
 }
 const changes=[];
 for(const dashboard of dashboards){
  const old=await read(base+'/grafana-l5/'+dashboard.uid+'-truoc-ui04.json');
  const unchangedTargets=old.panels.filter(p=>![7,24,28].includes(p.id)).map(p=>p.id);
  for(const id of unchangedTargets){
   const before=old.panels.find(p=>p.id===id).targets;
   const after=dashboard.panels.find(p=>p.id===id).targets;
   if(JSON.stringify(before)!==JSON.stringify(after))throw Error('Truy vấn ngoài phần thay đổi '+id);
  }
  if(dashboard.uid==='t065-l4-rca'&&/root_khai_truoc|tap_chap_nhan|phat_lai\./.test(JSON.stringify(dashboard)))throw Error('Đáp án lẫn trang chính');
  const sha=value=>crypto.createHash('sha256').update(value).digest('hex');
  changes.push({uid:dashboard.uid,before:sha(await fs.readFile(base+'/grafana-l5/'+dashboard.uid+'-truoc-ui04.json')),after:sha(await fs.readFile(base+'/grafana-l5/ui04/'+dashboard.uid+'.json')),unchanged_targets:unchangedTargets});
 }
 const result={utc:new Date().toISOString(),passed:report.every(row=>row.passed),jobs:report,changes};
 await fs.writeFile(output+'/ui04-kiem.json',JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify({passed:result.passed,jobs:report.length,failed:report.filter(row=>!row.passed)}));
 if(!result.passed)process.exitCode=1;
}
