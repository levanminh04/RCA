"""Lát cắt OB local cho máy P7; M1/T12 cùng tiến trình và bốn baseline hỗ trợ."""
import copy,time
from common import ROOT,RUN,read,save,timing,metadata,native_index,native_rows,event,dump
from m1 import adapter,runner,chuoi,e4
from p3 import nezha,runner as p3runner
from chay import capture

def main():
    start=time.perf_counter();target=RUN/'ob-local-001';target.mkdir()
    es,base,_=metadata();job=es[62]['job'];oid=job['opaque_id']
    allow=nezha.nap_allowlist(ROOT/'results/T-026/allowlist-dev.json')
    tick=time.perf_counter();case=adapter.ca_nezha(allow,oid,ROOT,read('results/T-043/hop-dong.json'))
    read_seconds=time.perf_counter()-tick
    expected=read('results/T-051/t12-001/62.json')
    static=read(expected['static']['source'])
    current_static={'revision':expected['static']['source'],'canh':[[e['source'],e['target']] for e in static['edges']]}
    chuoi.CACHE=e4.CacheCong();results=[]
    for flag in (False,True):
        ch=copy.deepcopy(base);ch['config_id']='T12' if flag else 'M1';ch['bat_tat']['T12']=flag
        ca=case if not flag else dict(case,params_ca=dict(case['params_ca'],canh_tinh=current_static))
        params=runner._params(ch,{});params['tach_cd3']=True
        tick=time.perf_counter();rec,trace,clocks,effective=capture(ca,ca['t'],{'config_id':ch['config_id'],'params':params},compact=True)
        assert rec['status']=='OK' and not trace['capture_errors']
        for w in ('P','S_lo','S_hi'):
            assert [b['groups'] for b in rec['worlds'][w]['blocks']]==[b['groups'] for b in expected['worlds'][w]['rank'][int(flag)]['blocks']]
        save(target/(ch['config_id']+'-record.json'),rec)
        results.append(timing('M1_T12_local',tick,T12=flag,ordered_ties_match=True,clocks=clocks))
    for method in ('baro','simplerca','microrank','tracerca','circa','torai_B'):
        jp=target/(method+'-job.json');rp=target/(method+'-result.json')
        save(jp,{'allowlist_path':str(ROOT/'results/T-026/allowlist-dev.json'),'opaque_id':oid,
                 'repo_root':str(ROOT),'view':'main','method':method,'trace_guard_s':0})
        cost=p3runner.chay_tien_trinh('main',['-m','p3.nezha_worker',str(jp),str(rp)],180,0,target/method)
        assert cost['exit_code']==0 and not cost['timed_out']
        result=read(rp)
        results.append({'method':method,'cost':cost,'statuses':[r['status'] for r in result['ket_qua_nhieu']]})
    save(target/'summary.json',timing('OB_local',start,PASS=True,adapter_seconds=read_seconds,results=results,
               scope='Một ca OB dev; không phải trần thời gian của test. CIRCA/TORAI giữ UNSUPPORTED Q-85.'))
    print('OB local M1/T12 and six baseline routes PASS',flush=True)

if __name__=='__main__':main()
