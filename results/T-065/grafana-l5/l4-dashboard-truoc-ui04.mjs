import {json,write} from './lib.mjs';
export const BASE='http://localhost:3000/public/rca/t065-l4-001';
export const UID='t065-l4-rca',REPLAY='t065-l4-phat-lai';
const DS={type:'yesoreyeram-infinity-datasource',uid:'infinity-rca'};
const caseurl=BASE+'/${ban}/vue/${ca}.json',svcurl=BASE+'/${ban}/thao-tac-vue/${ca}/${dv}.json';
function inf(ref,url,root,cols){return {refId:ref,datasource:DS,type:'json',source:'url',parser:'backend',format:'table',url,url_options:{method:'GET',data:''},root_selector:root,columns:cols.map(c=>({selector:c[0],text:c[0],type:c[1]||'string'}))};}
const col=(name,properties)=>({matcher:{id:'byName',options:name},properties:Object.entries(properties).map(([id,value])=>({id,value}))});
const page=(uid,ca='${ca}',svc='${dv}',op='${op}',tu='${t_tu}',den='${t_den}')=>`/d/${uid}?var-ban=\${ban:percentencode}&var-ca=${ca}&var-dv=${svc}&var-op=${op}&from=${tu}&to=${den}`;
function table(id,title,y,h,target,overrides=[]){return {id,type:'table',title,gridPos:{x:0,y,w:24,h},datasource:DS,targets:[target],fieldConfig:{defaults:{custom:{cellOptions:{type:'auto'}},noValue:'—'},overrides},options:{showHeader:true,cellHeight:'sm',footer:{show:false}}};}
function variable(name,target,hide=0){return {name,label:name,type:'query',datasource:DS,query:{queryType:'infinity',infinityQuery:target,query:'',refId:'variable'},refresh:1,hide,includeAll:false,multi:false,current:{},options:[]};}
export async function dashboardL4({ui03=false}={}){
 const old=await json('results/T-065/grafana/t065-rca.json');
 for(const replay of [false,true]){
  const url=replay?BASE+'/${ban}/phat-lai/${ca}.json':caseurl;
  const vars=[variable('ban',inf('v',BASE+'/chi-muc-ban.json','$$.([ban.{"__text":ban & " — " & trang_thai,"__value":ban}])',[['__text'],['__value']])),
   variable('ca',inf('v',BASE+'/${ban}/chi-muc.json','$$.([su_co.{"__text":ma & " (" & nguon & ")","__value":ma}])',[['__text'],['__value']]),2),
   variable('dv',inf('v',caseurl,'$$.([ranking_rows.{"__text":entity,"__value":entity}])',[['__text'],['__value']])),
   variable('dv_svc',inf('v',caseurl,'$$.([{"v":"${dv}"="config-discovery"?"discovery-server":"${dv}"}])',[['v']]),2),
   variable('t_tu',inf('v',caseurl,'$$.([{"v":cua_so_ms[0]}])',[['v','number']]),2),
   variable('t_den',inf('v',caseurl,'$$.([{"v":cua_so_ms[1]-1}])',[['v','number']]),2),
   variable('op',inf('v',svcurl,'$$.([thao_tac.{"__text":ten,"__value":id}])',[['__text'],['__value']]))];
  vars[0].current={text:'p7',value:'p7'};vars[1].current={text:'00eaea92',value:'00eaea92'};vars[2].current={text:'payment-service',value:'payment-service'};
  const d={uid:replay?REPLAY:UID,id:null,version:1,title:replay?'T-065 L4 — phát lại CÓ ĐÁP ÁN':'T-065 L4 — chọn bản M1 cùng ca',tags:['RCA','T-065','L4'],timezone:'utc',editable:false,schemaVersion:42,refresh:'',timepicker:{hidden:true},time:old.time,templating:{list:vars},links:[],panels:[]};
  d.panels.push({id:1,type:'text',title:'Kết quả theo bản và ca',gridPos:{x:0,y:0,w:24,h:5},options:{mode:'markdown',content:'Bản **${ban}**, ca **${ca}**. Đổi bản giữ cùng ca; chọn ca bằng bảng bên dưới để đặt đúng khung giờ. Hạng/cờ lấy nguyên từ đầu ra phương pháp; nhóm nút là tie_group + 1, không chấm lại. Điểm e chỉ ở chi tiết thao tác. Cửa sổ **[t−300,t+300)**. Trạng thái truy vấn là snapshot tại giờ ghi, có thể khác dữ liệu sống sau đó. LLM chưa triển khai.\n\n['+(replay?'Về trang chính':'Mở trang phát lại (sau khi chấm xong)')+']('+page(replay?UID:REPLAY)+')'}});
  d.panels.push(table(2,'Danh sách ca — bấm mã để mở đúng cửa sổ',5,8,inf('list',BASE+'/${ban}/chi-muc.json','su_co',[['ma'],['nguon'],['ket_luan'],['tu','number'],['den','number']]),[col('ma',{links:[{title:'Mở ca',url:page(replay?REPLAY:UID,'${__data.fields.ma}','${dv}','', '${__data.fields.tu}','${__data.fields.den}')}]})]));
  d.panels.push(table(3,'Bản, hash, trạng thái và cửa sổ',13,7,inf('meta',caseurl,'$$.([{"ban":ban.ban,"trang_thai":ban.trang_thai,"cau_hinh_sha256":ban.cau_hinh_sha256,"ma_nguon_sha256":ban.ma_nguon_sha256,"ghi_chu_hash":ban.ghi_chu_hash,"tu":tu_utc,"den_loai_tru":den_loai_tru,"ket_luan":su_co.ket_luan,"nguon":ban.nguon_output,"gioi_han":gioi_han}])',[['ban'],['trang_thai'],['cau_hinh_sha256'],['ma_nguon_sha256'],['ghi_chu_hash'],['tu'],['den_loai_tru'],['ket_luan'],['nguon'],['gioi_han']])));
  d.panels.push(table(4,'Thực thể theo entity_ranking — giữ thứ tự nguồn',20,10,inf('rank',url,'ranking_rows',[['entity'],['hang','number'],['tie_group','number'],['lop'],['so_kenh_co','number']]),[col('hang',{displayName:'Nhóm (tie_group + 1)'}),col('entity',{links:[{title:'Mở service và thao tác',url:page(UID,'${ca}','${__data.fields.entity}','')}]})]));
  d.panels.push(table(5,'Trạng thái đầu ra cạnh',30,3,inf('edge_state',caseurl,'$$.([{"ket_qua":trang_thai_canh}])',[['ket_qua']])));
  d.panels.push(table(6,'Cạnh xếp hạng M1-FT — nguyên thứ tự và hạng nguồn',33,10,inf('edge_rank',url,'canh_xep_hang',[['nguon'],['dich'],['loai'],['hang','number'],['tie_group','number'],['co','number'],['trang_thai'],['nguon_xac_minh']])));
  if(replay){d.panels.push(table(7,'Phát lại — lớp dữ liệu tách riêng',43,10,inf('replay',url,'$$.([{"phat_lai":$string(phat_lai),"gioi_han":gioi_han}])',[['phat_lai'],['gioi_han']])));}
  else{
   d.panels.push(table(8,'Vùng nghi ngờ từ phương pháp',43,5,inf('region',caseurl,'$$.([{"goc":$join(region.T,", "),"cach_1":$join(region.hop_cach_1,", "),"cach_2":$join(region.hop_cach_2,", ")}])',[['goc'],['cach_1'],['cach_2']])));
   d.panels.push(table(9,'Toàn bộ cờ M1 của bản đang xem',48,10,inf('flags',caseurl,'co_m1',[['ma'],['thuc_the'],['don_vi'],['ten'],['huong'],['lop'],['F_I','number']])));
   d.panels.push(table(10,'Bằng chứng có cờ — ${dv}',58,9,inf('evidence',caseurl,'$$.([bang_chung[thuc_the="${dv}"].($b:=$;lien_ket.{"don_vi":$b.don_vi,"kho":kho,"pham_vi":pham_vi,"ghi_chu":ghi_chu,"url":url})])',[['don_vi'],['kho'],['pham_vi'],['ghi_chu'],['url']]),[col('url',{links:[{title:'Mở Explore',url:'${__value.raw}',targetBlank:true}]})]));
   for(const source of old.panels.filter(p=>p.id>=21&&p.id<=26)){
    const p=JSON.parse(JSON.stringify(source).replaceAll('http://localhost:3000/public/rca/t065-l3-001',BASE).replaceAll('/thao-tac/','/thao-tac-vue/').replaceAll('t065-rca',UID).replaceAll('var-ban=${ban}','var-ban=${ban:percentencode}'));
    p.gridPos.y+=17;p.description=(p.description||'').replaceAll('của P7','của bản đang xem');d.panels.push(p);
   }
   const snapshot = table(28,'Trạng thái từng truy vấn sống — snapshot API',128,9,inf('query_state',BASE+'/trang-thai/${ca}/${dv}.json','queries',[['panel','number'],['kho'],['trang_thai'],['so_dong','number'],['utc'],['tu_utc'],['den_loai_tru'],['dien_giai'],['loi']]));
   if(ui03){
    snapshot.targets[0].columns=snapshot.targets[0].columns.filter(column=>column.selector!=='dien_giai');
    snapshot.fieldConfig.overrides=[col('trang_thai',{mappings:[{type:'value',options:{rong:{text:'0 dòng khớp'},co_du_lieu:{text:'Có dữ liệu khớp'},loi:{text:'Truy vấn báo lỗi'}}}]})];
   }
   d.panels.push(snapshot);
   d.panels.push(table(29,'Metric dev — truy vấn nguyên văn đã lưu',137,6,inf('metric_links',caseurl,'metric_links',[['kho'],['ghi_chu'],['truy_van'],['url']]),[col('url',{links:[{title:'Mở metric đã lưu',url:'${__value.raw}',targetBlank:true}]})]));
   for(const p0 of old.panels.filter(p=>p.id>=31)){const p=JSON.parse(JSON.stringify(p0));p.gridPos.y+=30;d.panels.push(p);}
  }
  // L5: metadata hai cột để hash/nguồn/cửa sổ không bị cắt ở viewport thường.
  const meta=d.panels.find(p=>p.id===3);
  meta.targets=[inf('meta',caseurl,'$$.([{"a_truong":"Bản","b_gia_tri":ban.ban},{"a_truong":"Trạng thái","b_gia_tri":ban.trang_thai},{"a_truong":"Hash cấu hình","b_gia_tri":ban.cau_hinh_sha256 ? ban.cau_hinh_sha256 : "null — chỉ mục nguồn chưa cấp"},{"a_truong":"Hash mã nguồn","b_gia_tri":ban.ma_nguon_sha256 ? ban.ma_nguon_sha256 : "null — chỉ mục nguồn chưa cấp"},{"a_truong":"Bắt đầu (bao gồm)","b_gia_tri":tu_utc},{"a_truong":"Kết thúc (loại trừ)","b_gia_tri":den_loai_tru},{"a_truong":"Nguồn đầu ra","b_gia_tri":ban.nguon_output},{"a_truong":"Kết luận phương pháp","b_gia_tri":su_co.ket_luan},{"a_truong":"Ghi chú hash","b_gia_tri":ban.ghi_chu_hash},{"a_truong":"Giới hạn","b_gia_tri":gioi_han}])',[['a_truong'],['b_gia_tri']])];
  meta.gridPos.h=16;
  meta.fieldConfig.defaults.custom.wrapText=true;
  meta.fieldConfig.overrides=[col('a_truong',{displayName:'Trường','custom.width':220}),col('b_gia_tri',{displayName:'Giá trị','custom.wrapText':true})];
  for(const p of d.panels)if(p.id!==3&&p.gridPos.y>=20)p.gridPos.y+=9;
  const empty={6:'Không có dòng cạnh trong đầu ra của bản/ca này. Xem trạng thái đầu ra cạnh ở trên.',9:'Đầu ra của bản/ca này không có cờ M1.',10:'Không có liên kết bằng chứng có cờ cho service đang chọn. Xem bảng thao tác bên dưới.',22:'Nguồn không có thao tác cho service đang chọn.',23:'Nguồn không có đồ thị thao tác cho service đang chọn.',24:'Chưa có thao tác được chọn. Bấm tên trong bảng thao tác.',25:'Không có liên kết bằng chứng cho thao tác đang chọn.',26:'Không có ví dụ span cha–con trong nguồn cho service đang chọn.',29:'Không có liên kết metric dev cho ca này. Với T-062, dùng bằng chứng thao tác ở trên.',31:'Truy vấn request trả 0 chuỗi cho service/cửa sổ này. Đối chiếu snapshot API ở trên.',32:'Truy vấn p90 trả 0 chuỗi cho service/cửa sổ này. Đối chiếu snapshot API ở trên.',33:'Truy vấn 5xx trả 0 chuỗi cho service/cửa sổ này. Đối chiếu snapshot API ở trên.',34:'Tìm trace trả 0 dòng cho service/cửa sổ này. Đối chiếu snapshot API ở trên.',35:'Truy vấn log error/exception/warn trả 0 dòng cho service/cửa sổ này. Đối chiếu snapshot API ở trên.'};
  if(ui03)Object.assign(empty,{24:'Chưa có giá trị cho trường này.',31:'—',32:'—',33:'—',34:'Chưa có dòng trace hiển thị. Xem snapshot API để đối chiếu.',35:'—'});
  for(const p of d.panels)if(empty[p.id]){p.fieldConfig??={defaults:{},overrides:[]};p.fieldConfig.defaults??={};p.fieldConfig.defaults.noValue=empty[p.id];}
  // No data là trạng thái hiển thị. Chỉ snapshot xác nhận số dòng tại giờ xuất.
  if(ui03)for(const panel of d.panels.filter(p=>[31,32,33,35].includes(p.id))){
   panel.title+=' — nếu rỗng, xem snapshot API';
   panel.description='Panel đang hiển thị dữ liệu truy vấn sống cho service và cửa sổ đã chọn. Nếu panel rỗng, đối chiếu trạng thái, số dòng và giờ truy vấn ở bảng snapshot API.';
  }
  if(!ui03){const logs=d.panels.find(p=>p.id===35);if(logs)logs.title+=' — rỗng: 0 dòng khớp trong cửa sổ';}
  await write(`${ui03?'grafana-l5/ui03':'grafana-l4'}/${d.uid}.json`,d);
 }
 return [UID,REPLAY];
}
