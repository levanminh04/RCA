import {ROOT,HERE,fs,path,json,read,write,hash,assert,num} from './lib.mjs';
import {prepare,kind} from './xuat-du-lieu.mjs';

// Kiểm các keyword JSON Schema được dùng bởi bản 0.2/0.3; từ chối schema có keyword chưa triển khai.
export function validate(schema,value,root=schema,at='$') {
  let errors=[]; const fail=s=>errors.push(at+': '+s);
  if(schema.$ref) {
    assert(schema.$ref.startsWith('#/'),'Chỉ hỗ trợ ref nội bộ');
    let def=root;for(const k of schema.$ref.slice(2).split('/'))def=def[k];
    return validate(def,value,root,at);
  }
  const allowed=new Set(['$schema','$id','title','description','type','properties','$defs','additionalProperties','required','const','minLength','oneOf','$ref','enum','allOf','if','then','else','minimum','items','maximum','minItems','maxItems','pattern']);
  for(const k of Object.keys(schema)) assert(allowed.has(k),'Keyword chưa hỗ trợ: '+k);
  const typeOk=t=>t==='null'?value===null:t==='array'?Array.isArray(value):t==='object'?value!==null&&typeof value==='object'&&!Array.isArray(value):t==='integer'?typeof value==='number'&&Number.isInteger(value):typeof value===t;
  if(schema.type && !(Array.isArray(schema.type)?schema.type:[schema.type]).some(typeOk))return [at+': type '+schema.type];
  if('const' in schema && JSON.stringify(schema.const)!==JSON.stringify(value))fail('const');
  if(schema.enum&&!schema.enum.some(v=>JSON.stringify(v)===JSON.stringify(value)))fail('enum');
  if(typeof value==='number') {
    if(schema.minimum!==undefined&&value<schema.minimum)fail('minimum');
    if(schema.maximum!==undefined&&value>schema.maximum)fail('maximum');
  }
  if(typeof value==='string') {
    if(schema.minLength!==undefined&&value.length<schema.minLength)fail('minLength');
    if(schema.pattern&&!new RegExp(schema.pattern).test(value))fail('pattern');
  }
  if(Array.isArray(value)) {
    if(schema.minItems!==undefined&&value.length<schema.minItems)fail('minItems');
    if(schema.maxItems!==undefined&&value.length>schema.maxItems)fail('maxItems');
    if(schema.items)for(const [i,v]of value.entries())errors.push(...validate(schema.items,v,root,at+'['+i+']'));
  } else if(value!==null&&typeof value==='object') {
    for(const k of schema.required||[])if(!(k in value))fail('thiếu '+k);
    for(const [k,v]of Object.entries(value)) {
      if(schema.properties?.[k])errors.push(...validate(schema.properties[k],v,root,at+'.'+k));
      else if(schema.additionalProperties===false)fail('khóa lạ '+k);
      else if(typeof schema.additionalProperties==='object')errors.push(...validate(schema.additionalProperties,v,root,at+'.'+k));
    }
  }
  for(const s of schema.allOf||[])errors.push(...validate(s,value,root,at));
  if(schema.oneOf&&schema.oneOf.filter(s=>validate(s,value,root,at).length===0).length!==1)fail('oneOf');
  if(schema.if) {const cond=validate(schema.if,value,root,at).length===0;
    if(cond&&schema.then)errors.push(...validate(schema.then,value,root,at));
    if(!cond&&schema.else)errors.push(...validate(schema.else,value,root,at));}
  return errors;
}
export async function makeSchema() {
  const s=await json('results/T-061/schema.json');
  s.$id='urn:flashticket:rca:result:0.3';s.title='FlashTicket RCA 0.3 — bản và thao tác';
  s.properties.phien_ban_dinh_dang.const='0.3';
  Object.assign(s.$defs.phat_lai.properties,{
    sha256_manifest_ket_qua:{$ref:'#/$defs/sha256'},o_loi:{type:'string'},root_khai_truoc:{type:['string','null']},
    tap_chap_nhan:{type:'array',items:{type:'string'}},suc_khoe:{type:['string','null']},
    hang_trong_tap:{type:'object'},hang_tot_nhat:{type:['number','null']}});
  s.required.push('ban');
  s.$defs.lien_ket.properties.url={type:'string',pattern:'^/explore\\?'};
  s.$defs.lien_ket.properties.pham_vi={type:'string'};
  const base={ban:{type:'string',minLength:1},trang_thai:{type:'string'},method_version:{type:'string'},variant:{type:'string'},config_id:{type:'string'},
    cau_hinh_sha256:{$ref:'#/$defs/sha256'},cau_hinh_file:{type:'string'},nguon_output:{type:'string'},sha256_output:{$ref:'#/$defs/sha256'},
    nguon_input:{type:'string'},sha256_input:{$ref:'#/$defs/sha256'},hop_dong:{type:'string'}};
  s.properties.ban={type:'object',additionalProperties:false,required:Object.keys(base),properties:base};
  const op={id:{type:'string'},chu:{type:'string'},ten:{type:'string'},loai:{type:'string'},
    n_N:{type:'integer',minimum:0},n_A:{type:'integer',minimum:0},mau_N:{type:'integer',minimum:0},mau_A:{type:'integer',minimum:0},
    span_boc:{type:'integer',minimum:0},goc:{type:'integer',minimum:0},mo_coi:{type:'integer',minimum:0},
    dich_quan_sat:{type:'array',items:{type:'string'}},trang_thai_m1:{type:'string'},co_len:{enum:[0,1]},co_xuong:{enum:[0,1]},
    co_m1:{type:'boolean'},so_kenh_co:{type:'integer',minimum:0},kenh_co:{type:'array'},don_vi_m1:{type:['object','null']},
    mau:{type:'string',pattern:'^#[0-9A-Fa-f]{6}$'},ban_kinh:{const:32},lien_ket:{type:'array',items:{$ref:'#/$defs/lien_ket'}},
    ly_do_khong_prometheus:{type:['string','null']},vi_du:{type:'array'}};
  s.properties.thao_tac={type:'array',items:{type:'object',additionalProperties:false,required:Object.keys(op),properties:op}};
  s.properties.canh_thao_tac={type:'array',items:{type:'object',additionalProperties:false,
    required:['id','source','target','loai','so_quan_he','so_N','so_A','vi_du'],properties:{id:{type:'string'},source:{type:'string'},target:{type:'string'},
      loai:{const:'span_cha_con'},so_quan_he:{type:'integer',minimum:1},so_N:{type:'integer',minimum:0},so_A:{type:'integer',minimum:0},vi_du:{type:'array',minItems:1}}}};
  s.properties.tien_xu_ly={type:'object'};s.properties.quan_he={type:'object'};
  await write('dinh-dang/schema-0.3.json',s);return s;
}
export async function verify() {
  const schema=await makeSchema();const idx=await json('results/T-065/du-lieu/p7/chi-muc/danh-sach-su-co.json');
  const report={schema:[],links:[],cases:[],tests:[]};
  for(const sc of idx.su_co) {
    const ca=sc.ma,base=await json(`results/T-065/du-lieu/p7/${ca}.json`),old=await json(`results/T-062/ket-qua/${ca}.json`);
    assert(!('phat_lai' in base),'Rò đáp án');
    for(const k of ['su_co','nut','canh','xep_hang','vung','giai_thich_ke_thua'])
      assert(JSON.stringify(base[k])===JSON.stringify(old[k]),ca+': hồi quy trường '+k);
    const m1=await json(`results/T-062/ca/${ca}/outputs/${ca}/method-output-1.json`);
    const units=m1.extra.don_vi_phan_vi.filter(x=>x.ma.startsWith('op|'));
    const flags=m1.extra.kenh_co.filter(x=>x.don_vi.startsWith('op|'));
    for(const u of units) {
      const o=base.thao_tac.find(o=>'op|'+o.chu+'|'+o.ten===u.ma);assert(o,'Thiếu op '+u.ma);
      assert(JSON.stringify(o.don_vi_m1)===JSON.stringify(u),'Sai trạng thái/e/cờ nguồn');
      assert(o.mau_N===u.n_N&&o.mau_A===u.n_A,'Sai số mẫu');
    }
    assert(base.thao_tac.reduce((n,o)=>n+o.kenh_co.length,0)===flags.length,'Thiếu kênh có cờ');
    const inp=await json(`results/T-062/ca/${ca}/outputs/${ca}/method-input.json`);
    const prep=prepare(inp[0],inp[4],inp[5],inp[6].don_vi_thoi_gian['spans.start_us']);
    const nodeById=new Map(base.thao_tac.map(o=>[o.id,o]));
    let totalRelations=0;
    for(const e of base.canh_thao_tac) {
      assert(nodeById.has(e.source)&&nodeById.has(e.target),'Đầu mút cạnh không có nút');
      assert(e.so_quan_he===e.so_N+e.so_A,'Sai số cạnh N/A');totalRelations+=e.so_quan_he;
      for(const sample of e.vi_du) {
        const child=prep.spans.get(sample.trace_id+'|'+sample.con_span_id),parent=prep.spans.get(sample.trace_id+'|'+sample.cha_span_id);
        assert(child&&parent&&child.parent===parent.key,'Mẫu cạnh không quan sát trong nguồn');
        assert(nodeById.get(e.source).ten===parent.operation&&nodeById.get(e.target).ten===child.operation,'Sai ánh xạ thao tác');
      }
    }
    assert(totalRelations===[...prep.spans.values()].filter(s=>s.parent).length,'Mất/gán thêm quan hệ cha–con');
    for(const replay of [false,true]) {
      const filename=`du-lieu/p7/${replay?'phat-lai/':''}${ca}${replay?'.phat-lai':''}.json`;
      const d=await json('results/T-065/'+filename),errors=validate(schema,d);
      report.schema.push({file:filename,ok:errors.length===0,errors});assert(!errors.length,errors.slice(0,5).join('\n'));
    }
    report.cases.push({ca,regression:true,units:units.length,flags:flags.length,relations:totalRelations,graph_samples:true});
  }
  const links=await json('results/T-065/kiem/001/lien-ket.json');
  for(const l of links) {
    const u=new URL(l.url,'http://grafana.invalid'),panes=JSON.parse(u.searchParams.get('panes')),a=panes.a;
    assert(a.datasource===l.kho&&a.queries[0].datasource.uid===l.kho,'Sai datasource');
    assert(a.range.from===String(l.cua_so_ms[0])&&a.range.to===String(l.cua_so_ms[1]-1),'Sai cửa sổ đóng/mở');
    assert((a.queries[0].expr||a.queries[0].query)===l.truy_van,'Sai query sau giải mã một lần');
    assert(l.cua_so_ms[1]-l.cua_so_ms[0]===600000,'Cửa sổ không phải 600s');
  }
  report.links={total:links.length,decode_once:true,by_store:Object.fromEntries(['tempo','loki','prometheus'].map(k=>[k,links.filter(l=>l.kho===k).length])),
    evidence:Object.fromEntries(['tempo','loki','prometheus'].map(k=>[k,links.filter(l=>l.source==='bang_chung'&&l.kho===k).length]))};
  // Biên phải mở, alias, khóa theo trace, bỏ duplicate và span bọc. Không cần nhãn.
  const fixture=[
    {traceID:'t',spanID:'a',parentSpanID:'',owner:'old',operation:'root',start_us:700e6,duration_us:1000000},
    {traceID:'t',spanID:'b',parentSpanID:'a',owner:'old',operation:'wrapper',start_us:700100000,duration_us:500000},
    {traceID:'t',spanID:'c',parentSpanID:'b',owner:'db',operation:'SQL',start_us:700200000,duration_us:100000},
    {traceID:'t',spanID:'right',parentSpanID:'',owner:'old',operation:'outside',start_us:1299999999,duration_us:1},
  ];
  const prep=prepare([...fixture,fixture[0]],{old:'new'},1000);
  assert(prep.diagnostics.so_span===3&&prep.diagnostics.bo_lap===1&&prep.diagnostics.span_boc===1,'Sai fixture biên/alias/bọc');
  assert([...prep.spans.values()].every(s=>s.owner!=='old'),'Sai alias fixture');
  let rejected=false;try{prepare([...fixture,{...fixture[0],duration_us:2}],{old:'new'},1000);}catch{rejected=true;}
  assert(rejected,'Không từ chối khóa trùng khác nội dung');
  report.tests.push({boundary_alias_wrapper_duplicate:true,conflicting_duplicate_rejected:true});
  const sample=await json(`results/T-065/du-lieu/p7/${idx.su_co[0].ma}.json`);
  sample.thao_tac[0].ban_kinh=2;
  assert(validate(schema,sample).length>0,'Schema không phát hiện bán kính sai');
  report.tests.push({schema_rejects_variable_radius:true});
  assert(kind({kind:3},'',{'db.system':'postgresql'})==='SQL/cache','CLIENT SQL bị phân loại nhầm');
  assert(kind({kind:3},'',{'http.request.method':'GET'})==='HTTP','CLIENT HTTP bị phân loại nhầm');
  assert(kind({kind:4},'',{})==='message'&&kind({kind:5},'',{})==='message','Sai enum PRODUCER/CONSUMER');
  report.tests.push({otlp_span_kind_client_producer_consumer:true});
  await write('kiem/001/kiem-cuc-bo.json',report);return report;
}
