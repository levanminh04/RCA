import {json,read,write,assert,ROOT,fs,path} from './lib.mjs';
const load=async p=>JSON.parse((await read(p)).replace(/^\uFEFF/,''));
const rows=r=>(r?.frames||[]).flatMap(f=>{
  const fields=f.schema.fields.map(x=>x.name),values=f.data.values;
  return Array.from({length:values[0]?.length||0},(_,i)=>Object.fromEntries(fields.map((k,j)=>[k,values[j][i]])));
});
const canonical=v=>Array.isArray(v)?v.map(canonical):v&&typeof v==='object'?Object.fromEntries(Object.keys(v).sort().map(k=>[k,canonical(v[k])])):v;
const eq=(a,b,msg)=>assert(JSON.stringify(canonical(a))===JSON.stringify(canonical(b)),msg);
const setEq=(a,b,msg)=>eq([...a].sort(),[...b].sort(),msg);
export async function verifyApi(filename='api-panels-2.json',linkFilename='api-links-2.json') {
  const data=await load('results/T-065/kiem/001/'+filename);
  const report={dashboards:[],cases:[],services:[],requests:0,targets:0,errors:[]};
  for(const[uid,d]of Object.entries(data.dashboard_api)) {
    assert(d.http===200,'Dashboard chưa được nạp '+uid);
    const local=await json('results/T-065/grafana/'+uid+'.json');
    eq(d.data.dashboard.panels,local.panels,'Panel API khác local');
    report.dashboards.push({uid,version:d.data.dashboard.version,panels_match:true});
  }
  for(const[name,e]of [...Object.entries(data.cases).flatMap(([ca,ds])=>Object.entries(ds).map(([uid,e])=>[ca+'/'+uid,e])),...Object.entries(data.services),...Object.entries(data.variables||{})]) {
    report.requests++;report.targets+=e.request.queries.length;
    assert(e.response.http===200,'HTTP lỗi '+name);
    for(const [ref,r]of Object.entries(e.response.data.results))assert(!r.error&&r.status===200,name+': '+ref+' '+r.error);
    const ca=name.split('/')[0],base=await json(`results/T-065/du-lieu/p7/${ca}.json`),w=[base.su_co.cua_so_nen.tu_ms,base.su_co.cua_so_su_co.den_ms-1];
    eq([e.request.from,e.request.to],w.map(String),'Sai cửa sổ request '+name);
  }
  report.variables=[];
  for(const[key,e]of Object.entries(data.variables||{})) {
    const ca=key.split('/')[0],base=await json(`results/T-065/du-lieu/p7/${ca}.json`),lo=base.su_co.cua_so_nen.tu_ms,hi=base.su_co.cua_so_su_co.den_ms;
    const results=e.response.data.results;
    const expected={t_tu:String(lo),t_den:String(hi-1),t_tu_s:String(lo/1000),t_den_s:String((hi-1)/1000),t_tu_ns:String(lo)+'000000',t_den_ns:String(hi-1)+'999999'};
    for(const[k,v]of Object.entries(expected)) if(results[k+'_v'])assert(rows(results[k+'_v'])[0].v===v,'Biến cửa sổ sai '+key+'/'+k);
    report.variables.push({key,window_match:true});
  }
  for(const[ca,ds]of Object.entries(data.cases)) {
    const base=await json(`results/T-065/du-lieu/p7/${ca}.json`);
    for(const[uid,e]of Object.entries(ds)) {
      const r=e.response.data.results;
      const list=rows(r['2_ds']);assert(list.length===9,'Danh sách thiếu ca');
      for(const sc of list)assert(Number(sc.den)-Number(sc.tu)===599999,'List time chưa loại biên phải');
      const graph=rows(r['4_nodes']),edges=rows(r['4_edges']),ranking=rows(r['5_hang']);
      assert(graph.length===base.nut.length&&edges.length===base.canh.length&&ranking.length===base.nut.length,'Hồi quy số dòng');
      setEq(graph.map(x=>x.id),base.nut.map(n=>n.id),'Sai nút service');
      setEq(edges.map(x=>x.source+'->'+x.target),base.canh.map(c=>c.nguon+'->'+c.dich),'Sai cạnh service');
      for(const n of base.nut) {
        const actual=graph.find(x=>x.id===n.id);assert(actual.color===n.hien_thi.mau,'Sai màu vai trò');
        const rk=ranking.find(x=>x.ten===n.id);assert(rk,'Thiếu dòng hạng');
        const expected=['nghi_nguon','bi_keo_theo'].includes(n.vai_tro)?'#'+n.hang:n.vai_tro==='thieu_du_lieu'?'?':'';
        assert(rk.hang===expected,'Sai hạng hiển thị '+ca+'/'+n.id);
      }
      const evidence=rows(r['6_bc']);
      const selected=e.request.queries.find(q=>q.refId==='6_bc').root_selector.match(/thuc_the="([^"]+)"/)[1];
      const expected=base.bang_chung.filter(b=>b.thuc_the===selected).flatMap(b=>b.lien_ket.length?b.lien_ket.map(l=>l.url):[null]);
      assert(evidence.length===expected.length,'Sai số dòng bằng chứng');
      setEq(evidence.filter(x=>x.url).map(x=>x.url),expected.filter(Boolean),'Sai URL bằng chứng');
      report.cases.push({ca,uid,list:list.length,nodes:graph.length,edges:edges.length,ranking:ranking.length,evidence:evidence.length,match:true});
    }
  }
  for(const[key,e]of Object.entries(data.services)) {
    const[ca,svc]=key.split('/'),source=await json(`results/T-065/du-lieu/p7/thao-tac/${ca}/${svc}.json`),r=e.response.data.results;
    const ops=rows(r['22_ops']),nodes=rows(r['23_nodes']),edges=rows(r['23_edges']),examples=rows(r['26_relations']);
    assert(ops.length===source.thao_tac.length,'Sai số thao tác API '+key);
    setEq(ops.map(o=>o.id),source.thao_tac.map(o=>o.id),'Sai tập thao tác '+key);
    for(const expected of source.thao_tac) {
      const o=ops.find(x=>x.id===expected.id);
      for(const[a,b]of [['span_N','n_N'],['span_A','n_A'],['mau_N','mau_N'],['mau_A','mau_A'],['boc','span_boc'],['len','co_len'],['xuong','co_xuong'],['trang_thai','trang_thai_m1']])
        assert(o[a]===expected[b],key+': '+expected.ten+' '+a+' khác nguồn');
      assert(o.co===(expected.co_m1?'có cờ M1':'không có cờ M1'),'Sai cờ thao tác');
    }
    setEq(nodes.map(o=>o.id),source.nut.map(o=>o.id),'Sai nút op '+key);
    assert(nodes.every(n=>n.nodeRadius===32),'Bán kính op không cố định');
    setEq(edges.map(o=>o.id),source.canh.map(o=>o.id),'Sai cạnh op '+key);
    for(const c of source.canh) {
      const a=edges.find(e=>e.id===c.id);assert(a.source===c.source&&a.target===c.target&&a.mainstat===c.so_quan_he,'Sai hướng/số cạnh');
    }
    const expectedExamples=source.canh.flatMap(c=>c.vi_du.map(v=>[c.id,v.trace_id,v.cha_span_id,v.con_span_id].join('|')));
    setEq(examples.map(x=>[x.canh,x.trace_id,x.cha,x.con].join('|')),expectedExamples,'Sai ví dụ cạnh '+key);
    const selected=e.request.queries.find(q=>q.refId==='24_detail').root_selector.match(/id="([^"]*)"/)[1];
    const detail=rows(r['24_detail']),links=rows(r['25_oplinks']);
    if(source.thao_tac.length) {
      const op=source.thao_tac.find(o=>o.id===selected);assert(op,'Chọn op không tồn tại');assert(detail.length===1,'Thiếu chi tiết');
      for(const k of ['e_len','e_xuong'])assert((detail[0][k]??null)===(op.don_vi_m1?.[k]??null),'Sai e chi tiết');
      setEq(links.map(l=>l.url),op.lien_ket.map(l=>l.url),'Sai link thao tác');
    }
    const info=rows(r['21_status']);assert(info.length===1&&info[0].ket_qua===source.thong_bao,'Sai thông báo snapshot');
    report.services.push({ca,svc,ops:ops.length,nodes:nodes.length,edges:edges.length,examples:examples.length,match:true});
  }
  const linkData=await load('results/T-065/kiem/001/'+linkFilename);
  report.link_samples=linkData.map(x=>{
    assert(x.response.http===200,'Link API lỗi');
    const results=Object.values(x.response.data.results);assert(results.every(r=>r.status===200&&!r.error),'Link query lỗi');
    return {ca:x.ca,kho:x.kho,scope:x.link.pham_vi,query_ok:true,rows:results.flatMap(r=>(r.frames||[]).map(f=>f.data.values[0]?.length||0)),bam_that:false};
  });
  await write('kiem/001/doi-chieu-api.json',report);
  return {requests:report.requests,targets:report.targets,cases:report.cases.length,services:report.services.length,link_samples:report.link_samples.length};
}
