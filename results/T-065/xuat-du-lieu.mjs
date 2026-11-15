import {HERE,ROOT,fs,path,read,json,write,hash,lossless,num,link,existingLink,attrs,checkFile,assert} from './lib.mjs';

// Không chạy lại M1. Tái dựng miền/cha-con để hiển thị, đối chiếu trung gian M1 đã lưu.
// Quy tắc trực tiếp: src/m1/chuoi.py:299–307; src/m1/span.py:tien_xu_ly/chuan_bi/mau_thao_tac.
export function prepare(rows,aliases,t,unit='us') {
  assert(unit==='us','Chưa hỗ trợ đơn vị span ngoài hợp đồng P7 us');
  const lo=BigInt(t-300)*1000000000n, hi=BigInt(t+300)*1000000000n;
  const seen=new Map(); let duplicates=0,excluded=0;
  for(const row of rows) {
    const st=BigInt(row.start_us)*1000n,en=(BigInt(row.start_us)+BigInt(row.duration_us))*1000n;
    if(st<lo||en>=hi){excluded++;continue;}
    const r={...row,owner:aliases[row.owner]||row.owner};
    const key=r.traceID+'|'+r.spanID;
    if(seen.has(key)) {assert(JSON.stringify(seen.get(key))===JSON.stringify(r),'Span trùng khác nội dung');duplicates++;continue;}
    seen.set(key,r);
  }
  const spans=new Map();
  for(const [key,r] of seen) {
    const pk=r.parentSpanID?r.traceID+'|'+r.parentSpanID:null;
    spans.set(key,{...r,key,parent:seen.has(pk)?pk:null,orphan:!!pk&&!seen.has(pk),children:[],
      phase:r.start_us+r.duration_us>=t*1e6?'A':'N'});
  }
  for(const s of spans.values()) if(s.parent) spans.get(s.parent).children.push(s.key);
  for(const s of spans.values()) s.wrapper=s.children.length===1 &&
    spans.get(s.children[0]).owner!==s.owner && s.parent!==null && spans.get(s.parent).owner===s.owner;
  return {spans,diagnostics:{so_span:spans.size,bo_lap:duplicates,mo_coi:[...spans.values()].filter(s=>s.orphan).length,
    goc:[...spans.values()].filter(s=>!s.parentSpanID).length,span_boc:[...spans.values()].filter(s=>s.wrapper).length,
    ngoai_cua_so:excluded,he_span:1000}};
}
const invService = id => ({'config-discovery':'discovery-server','postgresql-shared-instance':'postgres',
  'mongodb-instance':'user-db',cache:'redis',broker:'rabbitmq'}[id]||id);
export function kind(s,scope,a) {
  // OTLP enum: CLIENT=3, PRODUCER=4, CONSUMER=5. Không nhầm client SQL/HTTP thành message.
  if(a['messaging.system']||s.kind===4||s.kind===5) return 'message';
  if(a['db.system']||a['db.system.name']) return 'SQL/cache';
  if(Object.keys(a).some(k=>k.startsWith('http.'))) return 'HTTP';
  if(/scheduling|quartz/.test(scope)) return 'job';
  return 'khac';
}
const opid=(owner,op)=>'o'+hash(JSON.stringify([owner,op])).slice(0,20);
export async function build() {
  const manifest=await json('results/T-062/manifest.json');
  const cm=await json('results/T-062/ca/manifest-ca.json');
  const km=await json('results/T-062/ket-qua/manifest-ket-qua.json');
  const ids=km.ids; assert(ids.length===9,'Phải có 9 ca hồi quy');
  const checks=[];
  for(const f of ['giao-dien/dung-dashboard.py','giao-dien/grafana/dashboards/rca-g2-chinh.json',
    'giao-dien/grafana/dashboards/rca-g2-phat-lai.json','ket-qua/chi-muc/danh-sach-su-co.json',
    'ket-qua/phat-lai/chi-muc/danh-sach-phat-lai.json','ca/_nguon/m1-p7-config.json','ca/_nguon/m1-source-pins.json'])
    checks.push(await checkFile(f,manifest.files[f]));
  const sourcePins=await json('results/T-062/ca/_nguon/m1-source-pins.json');
  // Các pin M1 là nguồn chuẩn để kiểm cài đặt đọc lại. Không đổi code.
  await write('kiem/001/source-pins.json',sourcePins);
  for(const f of ['src/m1/chuoi.py','src/m1/span.py']) {
    const b=await fs.readFile(path.resolve(ROOT,f));assert(hash(b)===sourcePins.pins[f],'Code M1 lệch pin '+f);
    checks.push({file:f,sha256:hash(b),bytes:b.length});
  }
  const configBytes=await read('results/T-062/ca/_nguon/m1-p7-config.json');
  const configSha=hash(configBytes);
  await write('du-lieu/p7/cau-hinh.json',configBytes);
  const comparisons=[],allLinks=[];
  for(const ca of ids) {
    const ip=`ca/${ca}/outputs/${ca}/method-input.json`,op=`ca/${ca}/outputs/${ca}/method-output-1.json`;
    for(const f of [ip,op,`ca/${ca}/cases/${ca}/raw-traces.jsonl`,`ca/${ca}/cases/${ca}/raw-logs.jsonl`,
      `ket-qua/phat-lai/${ca}.phat-lai.json`]) checks.push(await checkFile(f,manifest.files[f]));
    checks.push(await checkFile(`${ca}.json`,km.files[`${ca}.json`],'results/T-062/ket-qua'));
    checks.push(await checkFile(`${ca}/outputs/${ca}/method-output-1.json`,cm.files[`${ca}/outputs/${ca}/method-output-1.json`],'results/T-062/ca'));
    const input=await json('results/T-062/'+ip),m1=lossless(await read('results/T-062/'+op));
    const normal=JSON.parse(JSON.stringify(m1)),[rows,,,inventory,aliases,t,params]=input;
    const prep=prepare(rows,aliases,t,params.don_vi_thoi_gian['spans.start_us']);
    for(const k of ['so_span','bo_lap','mo_coi','goc','span_boc'])
      assert(prep.diagnostics[k]===normal.diagnostics.span[k],`${ca}: trung gian ${k} khác M1`);
    const w=[(t-300)*1000,(t+300)*1000];
    const base=lossless(await read(`results/T-062/ket-qua/${ca}.json`));
    const rawMeta=new Map();let spanLinks=0;
    for(const line of (await read(`results/T-062/ca/${ca}/cases/${ca}/raw-traces.jsonl`)).split('\n')) if(line.trim()) {
      const d=JSON.parse(line);
      for(const resource of d.resourceSpans||[]) {
        const resourceAttrs=attrs(resource.resource?.attributes),svc=resourceAttrs['service.name'];
        for(const scope of resource.scopeSpans||[]) for(const s of scope.spans||[]) {
          const key=s.traceId+'|'+s.spanId;if(!prep.spans.has(key))continue;
          const a=attrs(s.attributes);spanLinks+=(s.links||[]).length;
          rawMeta.set(key,{svc,type:kind(s,scope.scope?.name||'',a),route:a['http.route'],method:a['http.request.method']||a['http.method'],
            server:a['server.address'],db:a['db.system']||a['db.system.name'],message:a['messaging.system'],spanKind:s.kind});
        }
      }
    }
    const logTrace=new Map();
    for(const line of (await read(`results/T-062/ca/${ca}/cases/${ca}/raw-logs.jsonl`)).split('\n')) if(line.trim()) {
      for(const r of JSON.parse(line).resourceLogs||[]) {
        const svc=attrs(r.resource?.attributes)['service.name'];
        for(const scope of r.scopeLogs||[]) for(const l of scope.logRecords||[]) {
          const ns=BigInt(l.timeUnixNano||l.observedTimeUnixNano||0);
          if(ns<BigInt(t-300)*1000000000n||ns>=BigInt(t+300)*1000000000n)continue;
          let body;try{body=JSON.parse(l.body?.stringValue||'{}');}catch{continue;}
          if(body.traceId) {const key=svc+'|'+body.traceId;logTrace.set(key,(logTrace.get(key)||0)+1);}
        }
      }
    }
    const units=new Map((m1.extra.don_vi_phan_vi||[]).filter(u=>u.ma.startsWith('op|')).map(u=>[u.ma,u]));
    const flags=(m1.extra.kenh_co||[]).filter(k=>k.don_vi.startsWith('op|'));
    const groups=new Map();
    for(const s of prep.spans.values()) {
      const id=opid(s.owner,s.operation),meta=rawMeta.get(s.key);
      assert(meta,'Thiếu ánh xạ raw span '+ca+':'+s.key);
      let g=groups.get(id);if(!g){g={id,chu:s.owner,ten:s.operation,n_N:0,n_A:0,mau_N:0,mau_A:0,span_boc:0,
        mo_coi:0,goc:0,loai:new Set(),svcs:new Set(),routes:new Map(),traces:new Set(),vi_du:[],dich:new Set()};groups.set(id,g);}
      g['n_'+s.phase]++;if(params.bat_tat.E1==='tat'||!s.wrapper)g['mau_'+s.phase]++;
      g.span_boc+=Number(s.wrapper);g.mo_coi+=Number(s.orphan);g.goc+=Number(!s.parentSpanID);
      g.loai.add(meta.type);g.svcs.add(meta.svc);g.traces.add(s.traceID);
      if(meta.route&&meta.method)g.routes.set(JSON.stringify([meta.svc,meta.method,meta.route]),meta);
      if(meta.server)g.dich.add(meta.server+(meta.db?' ('+meta.db+')':''));
      if(g.vi_du.length<3)g.vi_du.push({trace_id:s.traceID,span_id:s.spanID,parent_span_id:s.parentSpanID,phia:s.phase});
    }
    const operations=[];
    for(const g of groups.values()) {
      const unit=units.get('op|'+g.chu+'|'+g.ten),fs=flags.filter(f=>f.don_vi==='op|'+g.chu+'|'+g.ten);
      if(unit){assert(num(unit.n_N)===g.mau_N&&num(unit.n_A)===g.mau_A,ca+': số mẫu op khác M1 '+g.ten);}
      else assert(g.mau_N+g.mau_A===0,ca+': thao tác có mẫu nhưng không có đơn vị M1');
      const links=[];
      for(const svc of g.svcs) {
        links.push(link('tempo',`{ resource.service.name = ${JSON.stringify(svc)} && name = ${JSON.stringify(g.ten)} }`,w,
          'tim_span_thao_tac','Tìm span theo service/tên; không phải trace do M1 chọn.'));
        const correlated=[...g.traces].filter(id=>logTrace.has(svc+'|'+id)).sort();
        links.push(link('loki',correlated.length?`{service_name=${JSON.stringify(svc)}} | json | traceId=~${JSON.stringify(correlated.slice(0,20).join('|'))}`:
          `{service_name=${JSON.stringify(svc)}}`,w,correlated.length?'trace_tuong_quan':'ngu_canh_service',
          correlated.length?`Log cùng trace với thao tác; tối đa 20/${correlated.length} trace có log, không khẳng định log do thao tác phát.`:
          'Chỉ ngữ cảnh service; không có trace tương quan trong log đã lưu của cửa sổ.'));
      }
      for(const m of g.routes.values()) links.push(link('prometheus',
        `sum by (http_request_method,http_route) (rate(http_server_request_duration_seconds_count{service_name=${JSON.stringify(m.svc)},http_request_method=${JSON.stringify(m.method)},http_route=${JSON.stringify(m.route)}}[1m]))`,
        w,'route_http_quan_sat','Route/method quan sát trong raw span; biểu thức không phải điểm M1.'));
      operations.push({id:g.id,chu:g.chu,ten:g.ten,loai:[...g.loai].sort().join(', '),n_N:g.n_N,n_A:g.n_A,mau_N:g.mau_N,mau_A:g.mau_A,
        span_boc:g.span_boc,goc:g.goc,mo_coi:g.mo_coi,dich_quan_sat:[...g.dich].sort(),
        trang_thai_m1:unit?.trang_thai||'KHONG_CHAM_SPAN_BOC',co_len:unit?.F_raw_len||0,co_xuong:unit?.F_raw_xuong||0,
        co_m1:fs.length>0,so_kenh_co:fs.length,kenh_co:fs,don_vi_m1:unit||null,
        mau:fs.length?'#E02F44':unit?.trang_thai==='OK'?'#8E8E8E':'#CA95E5',ban_kinh:32,
        lien_ket:links,ly_do_khong_prometheus:links.some(l=>l.kho==='prometheus')?null:
          'Không có cặp http.route/method ở span của thao tác này; không dựng metric SQL/job/message từ tên.',vi_du:g.vi_du});
    }
    const edges=new Map();
    for(const s of prep.spans.values()) if(s.parent) {
      const p=prep.spans.get(s.parent),source=opid(p.owner,p.operation),target=opid(s.owner,s.operation),id=source+'->'+target;
      let e=edges.get(id);if(!e){e={id,source,target,loai:'span_cha_con',so_quan_he:0,so_N:0,so_A:0,vi_du:[]};edges.set(id,e);}
      e.so_quan_he++;e['so_'+s.phase]++;
      if(e.vi_du.length<3)e.vi_du.push({trace_id:s.traceID,cha_span_id:p.spanID,con_span_id:s.spanID});
    }
    for(const b of base.bang_chung) {
      b.lien_ket=(b.lien_ket||[]).map(existingLink);
      if(b.don_vi.startsWith('log|')) {
        // Log_loi do adapter chấm trên severity ERROR/FATAL; Loki body JSON đã quan sát.
        const svc=invService(b.thuc_the);
        b.lien_ket.push(link('loki',`{service_name=${JSON.stringify(svc)}} | json | severity=~"ERROR|FATAL"`,w,
          'kenh_log_loi','Lọc severity ERROR/FATAL theo ho_so_nguon của lượt chạy, không lọc từ khóa message.'));
        b.ly_do_khong_lien_ket=null;
      }
    }
    const ban={ban:'p7',trang_thai:'khoa_P7',method_version:m1.method_version,variant:m1.variant,config_id:m1.config_id,
      cau_hinh_sha256:configSha,cau_hinh_file:'p7/cau-hinh.json',nguon_output:op,sha256_output:hash(await read('results/T-062/'+op)),
      nguon_input:ip,sha256_input:hash(await read('results/T-062/'+ip)),hop_dong:'results/T-064/hop-dong-dau-ra.md#ban-1'};
    Object.assign(base,{phien_ban_dinh_dang:'0.3',ban,thao_tac:operations,canh_thao_tac:[...edges.values()],
      tien_xu_ly:prep.diagnostics,quan_he:{da_ho_tro:['span_cha_con'],span_link:{trang_thai:'chua_ho_tro',so_link_raw:spanLinks},
        dich_loi_goi:'Chỉ hiển thị thuộc tính đích quan sát; không suy cạnh mới từ server.address/DB.'}});
    // File phụ theo service: đồ thị nội bộ và một bước qua biên, giữ đủ hai đầu cạnh.
    for(const svc of new Set([...base.nut.map(n=>n.id),...operations.map(o=>o.chu)])) {
      const own=new Set(operations.filter(o=>o.chu===svc).map(o=>o.id));
      const es=[...edges.values()].filter(e=>own.has(e.source)||own.has(e.target));
      const ns=new Set([...own,...es.flatMap(e=>[e.source,e.target])]);
      const ops=operations.filter(o=>own.has(o.id));
      await write(`du-lieu/p7/thao-tac/${ca}/${svc}.json`,{ban,ca,service:svc,cua_so_ms:w,thao_tac:ops,
        nut:operations.filter(o=>ns.has(o.id)).map(o=>({...o,ngoai_service:o.chu!==svc})),canh:es,
        thong_bao:ops.length?`${ops.length} thao tác quan sát; ${ops.filter(o=>o.co_m1).length} có kênh M1 gắn cờ. Cạnh cha–con quan sát; nút ngoài service là đầu mút qua biên.`:
          'Không có thao tác trong đầu vào M1 sau cắt cửa sổ. Chưa xác định vì không phát sinh hay không được thu.',
        quan_he:base.quan_he});
    }
    await write(`du-lieu/p7/${ca}.json`,base);
    const replay=lossless(await read(`results/T-062/ket-qua/phat-lai/${ca}.phat-lai.json`));
    Object.assign(replay,{phien_ban_dinh_dang:'0.3',ban,bang_chung:base.bang_chung});
    await write(`du-lieu/p7/phat-lai/${ca}.phat-lai.json`,replay);
    for(const b of base.bang_chung) for(const l of b.lien_ket) allLinks.push({ca,source:'bang_chung',id:b.id,...l});
    for(const o of operations) for(const l of o.lien_ket) allLinks.push({ca,source:'thao_tac',id:o.id,...l});
    comparisons.push({ca,so_nut:base.nut.length,so_canh:base.canh.length,so_thao_tac:operations.length,
      so_don_vi_op:units.size,so_kenh_op:flags.length,so_thao_tac_co:operations.filter(o=>o.co_m1).length,
      so_canh_op:edges.size,so_span:prep.spans.size,span_links:spanLinks,trung_gian_khop:true,
      so_mau_khop:true,kenh_op_khop:operations.reduce((n,o)=>n+o.kenh_co.length,0)===flags.length});
  }
  for(const [file,folder] of [['danh-sach-su-co.json',''],['danh-sach-phat-lai.json','phat-lai/']]) {
    const idx=await json(`results/T-062/ket-qua/${folder}chi-muc/${file}`);
    for(const sc of idx.su_co) {
      sc.ban='p7';sc.tu=sc.t_ms-300000;sc.den=sc.t_ms+300000-1;
      sc.sha256_file=hash(await read(`results/T-065/du-lieu/p7/${folder}${sc.file}`));
    }
    idx.phien_ban='0.3';await write(`du-lieu/p7/${folder}chi-muc/${file}`,idx);
  }
  await write('du-lieu/chi-muc-ban.json',{ban:[{ban:'p7',mo_ta:'P7 đã khóa',trang_thai:'khoa_P7',cau_hinh_sha256:configSha,cac_ca:ids}]});
  await write('kiem/001/kiem-hash-nguon.json',{ok:true,files:checks});
  await write('kiem/001/doi-chieu-9-ca.json',comparisons);
  await write('kiem/001/lien-ket.json',allLinks);
  return {ca:ids.length,thao_tac:comparisons.reduce((n,c)=>n+c.so_thao_tac,0),lien_ket:allLinks.length};
}
