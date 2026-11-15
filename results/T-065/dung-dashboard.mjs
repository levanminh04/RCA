import {json,write,assert} from './lib.mjs';
const DS={type:'yesoreyeram-infinity-datasource',uid:'infinity-rca'};
const BASE='http://localhost:3000/public/rca/t065-l3-001';
const URL=BASE+'/${ban}';
const UID='t065-rca',REPLAY='t065-phat-lai';
const clone=o=>JSON.parse(JSON.stringify(o));
function inf(ref,url,expr,cols) {
  return {refId:ref,datasource:DS,type:'json',source:'url',parser:'backend',format:'table',url,
    url_options:{method:'GET',data:''},root_selector:'$$.('+expr+')',
    columns:cols.map(c=>({selector:c[0],text:c[0],type:c[1]||'string'}))};
}
function override(name,values){return {matcher:{id:'byName',options:name},properties:Object.entries(values).map(([id,value])=>({id,value}))};}
const hidden=names=>names.map(n=>override(n,{'custom.hidden':true}));
const rawLink=(name,title)=>override(name,{links:[{title,url:'${__data.fields.'+name+':raw}',targetBlank:true}]});
function table(id,title,gp,target,overrides=[],desc='') {
  return {id,type:'table',title,gridPos:gp,datasource:DS,targets:[target],description:desc,
    fieldConfig:{defaults:{custom:{align:'auto',cellOptions:{type:'auto'},inspect:false},noValue:'—'},overrides},
    options:{showHeader:true,cellHeight:'sm',footer:{show:false}}};
}
const pos=(y,h=9,w=24,x=0)=>({y,h,w,x});
const linkPage=(uid,service='${dv}',op='')=>`/d/${uid}?var-ban=\${ban}&var-ca=\${ca}&var-dv=${service}${op?'&var-op='+op:''}&from=\${t_tu}&to=\${t_den}`;
function variable(name,label,target,hide=0) {
  return {name,label,type:'query',datasource:DS,query:{queryType:'infinity',infinityQuery:target,query:'',refId:'variable'},
    definition:label,refresh:1,hide,includeAll:false,multi:false,current:{},options:[]};
}
export async function buildDashboards() {
  const index=await json('results/T-065/du-lieu/p7/chi-muc/danh-sach-su-co.json');
  const initial=index.su_co[0];
  for(const replay of [false,true]) {
    const d=await json('results/T-062/giao-dien/grafana/dashboards/'+(replay?'rca-g2-phat-lai.json':'rca-g2-chinh.json'));
    const livePanels=clone(d.panels.slice(7));
    const uid=replay?REPLAY:UID;
    const file=replay?'${ca}.phat-lai.json':'${ca}.json';
    const folder=replay?URL+'/phat-lai':URL;
    d.uid=uid;d.title=replay?'T-065 — phát lại CÓ ĐÁP ÁN':'T-065 — sự cố và thao tác M1';d.id=null;d.version=1;
    d.tags=['RCA','T-065','P7'];d.timezone='utc';d.editable=false;d.time={from:String(initial.tu),to:String(initial.den)};
    d.timepicker={hidden:true};d.refresh='';d.description='Kết quả theo bản và ca. Các panel đọc snapshot đúng cửa sổ ca; Explore mở dữ liệu sống đúng cửa sổ.';
    // Giữ panel hồi quy. Ẩn bộ chọn ca; mọi điều hướng ca đặt range t±300, tránh dropdown đổi ca mà giữ range cũ.
    d.panels=d.panels.slice(0,7);d.links=[];
    const replaceString=s=>s.replaceAll('http://localhost:3000/public/${thu_muc}',folder)
      .replaceAll('rca-g2-phat-lai',REPLAY).replaceAll('rca-g2',UID)
      .replaceAll('&var-thu_muc=${thu_muc}','&var-ban=${ban}')
      .replaceAll('${__url_time_range}','from=${t_tu}&to=${t_den}')
      .replaceAll('900000','300000').replaceAll('±15 phút','[t−300, t+300)')
      .replaceAll('t_ms + 300000','t_ms + 300000 - 1')
      .replaceAll('Trong trang này/① Xem bằng chứng và thao tác của thành phần này (cuộn xuống)',
        'Điều hướng/① Mở chi tiết và thao tác của thành phần này');
    function walk(o){if(typeof o==='string')return replaceString(o);if(Array.isArray(o))return o.map(walk);
      if(o&&typeof o==='object')return Object.fromEntries(Object.entries(o).map(([k,v])=>[k,walk(v)]));return o;}
    d.panels=walk(d.panels);
    for(const p of d.panels) {
      // Trang chính không có tên cột ẩn liên quan đáp án từ mapping dùng chung của bản cũ.
      if(!replay) for(const tr of p.transformations||[]) if(tr.options?.renameByName) {
        delete tr.options.renameByName.detail__dap_an;delete tr.options.indexByName?.detail__dap_an;
      }
      if(p.id===1) {
        p.gridPos.h=5;
        p.options.content += '<br><b>Bản ${ban}.</b> Dữ liệu trong panel là snapshot của cửa sổ [t−300, t+300). '+
          'Chọn ca bằng danh sách để mở cùng khung giờ. Bấm thành phần để mở chi tiết. '+
          '<a href="'+linkPage(replay?UID:REPLAY)+'">'+(replay?'Về trang chính':'Mở trang phát lại (sau khi chấm xong)')+'</a>.';
      }
    }
    // Không che header panel thứ hai sau hướng dẫn cao hơn.
    d.panels[0].gridPos.h=4;
    const svcurl=URL+'/thao-tac/${ca}/${dv}.json';
    const caseurl=folder+'/'+file;
    const oldVars=d.templating.list;
    const ban=variable('ban','Bản phương pháp',inf('v',BASE+'/chi-muc-ban.json',
      '[ban.{"__text": ban & " — " & mo_ta & " (" & trang_thai & ")", "__value":ban}]',[['__text'],['__value']]));
    ban.current={text:'p7 — P7 đã khóa',value:'p7'};
    const ca=walk(clone(oldVars.find(v=>v.name==='ca')));ca.hide=2;ca.current={text:initial.ma,value:initial.ma};
    const dv=walk(clone(oldVars.find(v=>v.name==='dv')));
    const dvSvc=walk(clone(oldVars.find(v=>v.name==='dv_svc')));
    const tu=walk(clone(oldVars.find(v=>v.name==='t_tu'))),den=walk(clone(oldVars.find(v=>v.name==='t_den')));
    den.query.infinityQuery.root_selector=den.query.infinityQuery.root_selector.replace('su_co.cua_so_su_co.den_ms :','su_co.cua_so_su_co.den_ms - 1 :')
      .replace('1000000) + 300000','1000000) + 300000 - 1');
    const tuS=variable('t_tu_s','đầu cửa sổ (s)',inf('v',caseurl,'[{"v":$string($floor(su_co.cua_so_nen.tu_ms/1000))}]',[['v']]),2);
    const denS=variable('t_den_s','cuối truy vấn (s)',inf('v',caseurl,'[{"v":$string(su_co.cua_so_su_co.den_ms/1000-0.001)}]',[['v']]),2);
    const tuNs=variable('t_tu_ns','đầu cửa sổ (ns)',inf('v',caseurl,'[{"v":$string(su_co.cua_so_nen.tu_ms)&"000000"}]',[['v']]),2);
    const denNs=variable('t_den_ns','cuối truy vấn (ns)',inf('v',caseurl,'[{"v":$string(su_co.cua_so_su_co.den_ms-1)&"999999"}]',[['v']]),2);
    const op=variable('op','Thao tác đang xem',inf('v',svcurl,
      '[thao_tac.{"__text":ten & " — " & trang_thai_m1,"__value":id}]',[['__text'],['__value']]));
    d.templating.list=[ban,ca,dv,dvSvc,tu,den,...(replay?[]:[op])];
    // Thay bảng bằng chứng bằng URL dựng từ bộ xuất, hỗ trợ Loki và ghi rõ phạm vi.
    const evidence=d.panels.find(p=>p.title.startsWith('Bằng chứng của'));
    evidence.targets=[inf('bc',caseurl,
      '[bang_chung[thuc_the="${dv}"].($b:=$; $count(lien_ket)>0 ? lien_ket.{"kenh":$b.kenh,"huong":$b.huong,"s":$b.s,"don_vi":$b.don_vi,"kho":kho,"pham_vi":pham_vi,"ghi_chu":ghi_chu,"url":url,"mo":kho & " ↗"} : {"kenh":kenh,"huong":huong,"s":s,"don_vi":don_vi,"ghi_chu":ly_do_khong_lien_ket})]',
      [['kenh'],['huong'],['s','number'],['don_vi'],['kho'],['pham_vi'],['ghi_chu'],['url'],['mo']])];
    evidence.fieldConfig.overrides=[rawLink('mo','Mở dữ liệu gốc'),...hidden(['url'])];
    // mo link lấy cột url, không phải chữ kho hiển thị.
    evidence.fieldConfig.overrides[0]=override('mo',{displayName:'Mở dữ liệu gốc',links:[{title:'Mở trong Explore',url:'${__data.fields.url:raw}',targetBlank:true}]});
    evidence.description='Mỗi dòng là kênh có cờ hoặc một liên kết của kênh. Loki lọc severity ERROR/FATAL đúng hợp đồng nguồn. Không có link cạnh khi nguồn không cấp truy vấn.';
    d.panels.push(table(20,'Bản, cấu hình và cửa sổ đang xem',pos(44,6),inf('ban',caseurl,
      '[{"ban":ban.ban,"phien_ban":ban.method_version,"bien_the":ban.variant,"cau_hinh":ban.config_id,"cau_hinh_sha256":ban.cau_hinh_sha256,"tu":su_co.cua_so_nen.tu_utc,"den_loai_tru":su_co.cua_so_su_co.den_utc}]',
      [['ban'],['phien_ban'],['bien_the'],['cau_hinh'],['cau_hinh_sha256'],['tu'],['den_loai_tru']])));
    if(!replay) {
      d.panels.push(table(21,'Lớp thao tác của ${dv} — kết quả truy vấn snapshot',pos(50,4),inf('status',svcurl,
        '[{"ket_qua":thong_bao,"quan_he":"Đã hỗ trợ cha–con; span link message chưa hỗ trợ. Đích gọi là thuộc tính, không suy thêm cạnh."}]',[['ket_qua'],['quan_he']])));
      const opExpr='[thao_tac.{"id":id,"thao_tac":ten,"loai":loai,"trang_thai":trang_thai_m1,"co":co_m1?"có cờ M1":"không có cờ M1","len":co_len,"xuong":co_xuong,"span_N":n_N,"span_A":n_A,"mau_N":mau_N,"mau_A":mau_A,"boc":span_boc}]';
      d.panels.push(table(22,'Thao tác — bấm tên để xem chi tiết và bằng chứng',pos(54,13),inf('ops',svcurl,opExpr,
        [['id'],['thao_tac'],['loai'],['trang_thai'],['co'],['len','number'],['xuong','number'],['span_N','number'],['span_A','number'],['mau_N','number'],['mau_A','number'],['boc','number']]),[
          override('thao_tac',{links:[{title:'Mở chi tiết thao tác',url:linkPage(UID,'${dv}','${__data.fields.id}')}]}),...hidden(['id'])],
        'Trạng thái/cờ lấy từ extra.don_vi_phan_vi và extra.kenh_co kênh op của P7. Số span gồm span bọc; số mẫu M1 đã bỏ span bọc khi E1 bật. Không xếp hạng thao tác.'));
      const graph={id:23,type:'nodeGraph',title:'Đồ thị thao tác — ${dv} và đầu mút qua biên',gridPos:pos(67,18),datasource:DS,
        description:'Cạnh quan sát cùng trace: span cha → span con sau cắt cửa sổ/alias. Không suy nhân quả từ quan hệ này. Kích thước nút cố định. Bấm nút để mở chi tiết.',
        targets:[inf('nodes',svcurl,'[nut.{"id":id,"title":ten,"mainstat":co_m1?"có cờ M1":"","secondarystat":ngoai_service?"ngoài service: " & chu:trang_thai_m1,"color":mau,"nodeRadius":32,"detail__chu":chu,"detail__loai":loai,"detail__e_len":don_vi_m1.e_len,"detail__e_xuong":don_vi_m1.e_xuong}]',
          [['id'],['title'],['mainstat'],['secondarystat'],['color'],['nodeRadius','number'],['detail__chu'],['detail__loai'],['detail__e_len','number'],['detail__e_xuong','number']]),
          inf('edges',svcurl,'[canh.{"id":id,"source":source,"target":target,"mainstat":so_quan_he,"detail__loai":loai,"detail__so_N":so_N,"detail__so_A":so_A}]',
          [['id'],['source'],['target'],['mainstat','number'],['detail__loai'],['detail__so_N','number'],['detail__so_A','number']])],
        fieldConfig:{defaults:{},overrides:[override('id',{links:[{title:'Mở chi tiết thao tác',url:linkPage(UID,'${__data.fields.detail__chu}','${__data.fields.id}')} ]})]},
        options:{nodes:{mainStatUnit:'none',secondaryStatUnit:'none',arcs:[]},edges:{mainStatUnit:'none'},layoutAlgorithm:'layered',zoomMode:'cooperative'}};
      d.panels.push(graph);
      d.panels.push(table(24,'Chi tiết thao tác ${op:text} — điểm e chỉ ở đây/menu nút',pos(85,7),inf('detail',svcurl,
        '[thao_tac[id="${op}"].{"thao_tac":ten,"trang_thai":trang_thai_m1,"e_len":don_vi_m1.e_len,"e_xuong":don_vi_m1.e_xuong,"kenh_co":$join(kenh_co.ma,"; "),"span_goc":goc,"mo_coi":mo_coi,"dich_quan_sat":$join(dich_quan_sat,", "),"metric":ly_do_khong_prometheus}]',
        [['thao_tac'],['trang_thai'],['e_len','number'],['e_xuong','number'],['kenh_co'],['span_goc','number'],['mo_coi','number'],['dich_quan_sat'],['metric']])));
      d.panels.push(table(25,'Bằng chứng thao tác — ${op:text}',pos(92,9),inf('oplinks',svcurl,
        '[thao_tac[id="${op}"].lien_ket.{"mo":kho & " ↗","pham_vi":pham_vi,"ghi_chu":ghi_chu,"truy_van":truy_van,"url":url}]',
        [['mo'],['pham_vi'],['ghi_chu'],['truy_van'],['url']]),[override('mo',{links:[{title:'Mở bằng chứng thao tác',url:'${__data.fields.url:raw}',targetBlank:true}]}),...hidden(['url'])],
        'Tempo tìm đúng tên thao tác/service. Loki ghi rõ tương quan trace hay ngữ cảnh service. Prometheus chỉ có khi raw span cấp cặp route/method; không suy metric SQL/job/message.'));
      d.panels.push(table(26,'Ví dụ span cha–con đã quan sát',pos(101,8),inf('relations',svcurl,
        '[canh.($e:=$;vi_du.{"canh":$e.id,"trace_id":trace_id,"cha":cha_span_id,"con":con_span_id,"loai":$e.loai})]',
        [['canh'],['trace_id'],['cha'],['con'],['loai']])));
      d.panels.push({id:27,type:'text',title:'Khi mở dữ liệu sống trong Explore',gridPos:pos(109,5),
        options:{mode:'markdown',content:'Snapshot ở trên lấy từ gói ca đã băm. Trong Explore, truy vấn thành công nhưng rỗng chỉ có nghĩa **không có chuỗi/dòng/span khớp truy vấn trong cửa sổ này ở kho đang truy vấn**. Không suy service khỏe hoặc lỗi thu nhận. Khi có lỗi truy vấn, cần đọc lỗi trước khi diễn giải. Dữ liệu có thể hết retention; chưa xác định nguyên nhân rỗng nếu chưa đối chiếu kho và gói ca.\n\nLLM: chưa triển khai.'}});
      // Giữ các panel sống bản 6. Global range được đặt bởi điểm vào và mọi link đổi ca.
      for(const [i,original] of livePanels.entries()) {
        const p=walk(original);p.id=30+i;p.gridPos.y+=70;
        if(p.description)p.description=p.description.replace(/Bấm ⏱[^.]*\./g,'Khung giờ lấy từ link mở ca [t−300,t+300).');
        d.panels.push(p);
      }
    }
    // Cột e chỉ có trong panel detail và menu. Không chèn số e vào kích thước/nhãn/xếp hạng.
    const txt=JSON.stringify(d);
    if(!replay) {
      for(const s of ['phat_lai.','.phat-lai.json','danh-sach-phat-lai','tap_chap_nhan','đáp án'])assert(!txt.includes(s),'Trang chính chứa '+s);
    }
    await write(`grafana/${uid}.json`,d);
  }
  return {dashboards:[UID,REPLAY]};
}
