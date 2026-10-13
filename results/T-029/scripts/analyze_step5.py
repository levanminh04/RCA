"""T029 step5: join frozen label-free features after all machine dependencies pass."""
import argparse
import csv
import hashlib
import json
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'results/T-029'
LOG=ROOT/'tasks/T-029-p4-han-che-phat-hien/LOG.md'
STARTED=datetime.now().astimezone().isoformat()
TIMER=time.monotonic()
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def log(s):
    with LOG.open('a',encoding='utf-8') as f: f.write('\n- '+datetime.now().astimezone().isoformat()+' — Bước5: '+s+'\n')
def put(p,v):
    p=Path(p); assert not p.exists(),str(p)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,indent=1,allow_nan=False)+'\n',encoding='utf-8')
    log('Ghi '+p.relative_to(ROOT).as_posix())
def source(p): return {'path':Path(p).relative_to(ROOT).as_posix(),'sha256':sha(p)}
def intervention_flags(first,a1,a2,tolerance):
    valid=first is not None and first+tolerance<=719
    in1=any(abs(i-first)<=tolerance for i in a1) if valid else None
    in2=any(abs(i-first)<=tolerance for i in a2) if valid else None
    b2=not in1 if valid else None
    b3=not in2 if valid and not b2 else None
    return {'valid':valid,'I1_point_near_first':in1,'I2_point_near_first':in2,'B2':b2,'B3':b3}
def summarize(rows, field):
    groups=defaultdict(list)
    for r in rows: groups[r[field]].append(r)
    out={}
    for g,rs in sorted(groups.items()):
        counts=Counter(r['first_group'] for r in rs)
        flags=defaultdict(lambda:{'true':0,'false':0,'NA':0})
        for r in rs:
            for key,v in r['flags_flat'].items(): flags[key]['NA' if v is None else 'true' if v else 'false']+=1
        out[g]={'n':len(rs),'first_groups':dict(counts),'Miss':sum(r['Miss'] for r in rs),
                'flags':dict(flags),'case_ids':[r['opaque_id'] for r in rs],
                'delay_seconds':[r['delay_seconds'] for r in rs if r['delay_seconds'] is not None]}
    return out
def locate(feature,root):
    out={}
    for variant,services in feature['E_services'].items():
        values={s: (r['first_after_index'] if r['first_after_index'] is not None else float('inf')) for s,r in services.items()}
        value=values[root]; before=sum(v<value for v in values.values()); tied=sum(v==value for v in values.values())
        count=len(values)
        out[variant]={'root_first_after_index':services[root]['first_after_index'],
                      'rank_min':before+1,'rank_max':before+tied,'expected_rank':before+(tied+1)/2,
                      'root_top1_probability':1/tied if before==0 else 0.,'service_count':count,
                      'root_columns_remaining':services[root]['so_cot'],
                      'uniform_identity_expected_rank':(count+1)/2,'uniform_identity_top1_probability':1/count,
                      'tie_blocks':[{'index':None if k==float('inf') else k,'services':sorted(s for s,v in values.items() if v==k)} for k in sorted(set(values.values()))],
                      'baseline_mean_rank_check':sum(sum(u<v for u in values.values())+(sum(u==v for u in values.values())+1)/2 for v in values.values())/count}
        assert out[variant]['baseline_mean_rank_check']==out[variant]['uniform_identity_expected_rank']
    return out

def v7(rows, bf):
    cases={}
    for r in rows:
        if r['detector']!='bocpd': continue
        oid=r['opaque_id']; f=bf[oid]; alarm=set(f['alarms_indices'])
        b1=[v for i,v in f['B1_all_Nv'].items() if int(i) not in alarm and v['valid']]
        base={'B1':{'control_n':len(b1),'control_true':sum(v['flag'] for v in b1),
                    'control_rate':sum(v['flag'] for v in b1)/len(b1) if b1 else None,
                    'at_first':f['B1_t_hat']['flag'],'at_first_valid':f['B1_t_hat']['valid']},'B4':{}}
        for w,items in f['B4_all_Nv'].items():
            control=[v for i,v in items.items() if int(i) not in alarm and v['valid']]
            base['B4'][w]={}
            for k in ('2','3','5'):
                num=sum(v['flags'][k] for v in control); den=len(control)
                base['B4'][w][k]={'control_n':den,'control_true':num,'control_rate':num/den if den else None,
                                 'at_first':f['B4_t_hat'][w]['flags'][k],'at_first_valid':f['B4_t_hat'][w]['valid']}
        cases[oid]={'root':r['root'],'fault':r['fault'],'cell':r['cell'],**base}
    aggregate={}
    for name,w,k in [('B1',None,None)]+[('B4',str(w),str(k)) for w in (15,30,60) for k in (2,3,5)]:
        by={}
        for groupfield in ('all','cell','root','fault'):
            groups=defaultdict(list)
            for oid,r in cases.items(): groups['all' if groupfield=='all' else r[groupfield]].append((oid,r[name] if name=='B1' else r[name][w][k]))
            by[groupfield]={}
            for group,pairs in sorted(groups.items()):
                num=sum(r['control_true'] for _,r in pairs); den=sum(r['control_n'] for _,r in pairs)
                first=[r['at_first'] for _,r in pairs if r['at_first_valid']]
                first_rate=sum(first)/len(first) if first else None; control_rate=num/den if den else None
                by[groupfield][group]={'case_n':len(pairs),'at_first_true':sum(first),'at_first_n':len(first),
                                      'at_first_rate':first_rate,'nonalarm_true':num,'nonalarm_n':den,'nonalarm_rate':control_rate,
                                      'case_ids':[oid for oid,_ in pairs],
                                      'rates_exactly_equal':first_rate is not None and first_rate==control_rate}
        aggregate[name if w is None else f'{name}/w{w}/k{k}']=by
    return {'cases':cases,'aggregate':aggregate,
            'other_flags':{'status':'N/A','flags':['N1','N2','N3','N4','B2','B3'],'reason':'Cờ chứa điều kiện báo động'},
            'interpretation':'Pooled rates are descriptive; no new significance/equivalence threshold. A frequent nonalarm flag cannot alone explain alarms. Exact equality is recorded literally, not a statistical test.'}

def main(ec2):
    log('Lệnhcóghi: T014main Python -B -W ignore analyze_step5.py --ec2 '+str(ec2)+'; kiểm mọi phụ thuộc/hash trước nối nhãn.')
    run=OUT/'runs/step5-001'; assert not run.exists(); run.mkdir()
    put(run/'invocation.json',{'started':STARTED,'script_sha256':sha(__file__),'ec2':str(ec2),'status':'RUNNING'})
    chain=ec2/'runs/chuoi-002'
    for name in ('guard','v3-check','wrapper50-check','v4-check','ket-thuc'):
        doc=read(chain/(name+'.json'))
        assert doc.get('status',doc.get('V1'))=='PASS',name
    nm=read(OUT/'runs/nsigma-002/manifest.json'); assert nm['status']=='PASS' and nm['V2']['so_cap']==60 and nm['V2']['status']=='PASS'
    ni=read(OUT/'features-no-label/nsigma/manifest.json'); assert ni['status']=='PASS' and len(ni['cases'])==30
    bm=read(OUT/'runs/bocpd-features-001/manifest.json'); assert bm['status']=='PASS' and len(bm['cases'])==30
    bf={}; nf={}; frozen=[]
    for oid,ds in ni['cases'].items():
        for det,s in ds.items():
            assert sha(ROOT/s['path'])==s['sha256']; nf[(oid,det)]=read(ROOT/s['path']); frozen.append(s)
    for p,h in bm['outputs'].items(): assert sha(ROOT/p)==h
    for oid in bm['cases']:
        p=OUT/f'features-no-label/bocpd/{oid}.json'; bf[oid]=read(p); frozen.append(source(p))
    put(run/'features-frozen.json',{'status':'PASS','label_free_feature_count':len(frozen),'files':frozen})
    log('Đãkiểm/băm90featuretrướcnốinhãn; từđâyđọclabelroot/fault/cellchỉevaluatortheoSPEC.')
    labs={r['opaque_id']:r for r in read(ROOT/'results/T-022/nhan-dev.json')['cases']}
    bd=read(ROOT/'results/T-025/bao-dong.json')['bo_phat_hien']; ph=read(ROOT/'results/T-025/phat-hien.json')['bo_phat_hien']
    old=read(ROOT/'results/T-025/cham/phan-tich-b.json')['theo_ca']
    rows=[]; boc={}; ns={}; location={}
    for oid,lab in sorted(labs.items()):
        location[oid]={'root':lab['root'],'fault':lab['fault'],'cell':lab['cell'],'nsigma':{},
                       'bocpd':{'output':'Multivariate changepoint; no service or column attribution.',
                                'heuristic':bf[oid]['B4_t_hat_plus_heuristic']}}
        for det in ('bocpd','nsigma','nsigma_doi_chung'):
            f=bf[oid] if det=='bocpd' else nf[(oid,det)]; th=f['t_hat_index']; plus=f['t_hat_plus_index']
            group='No-first' if th is None else 'S' if th>=720 else 'E-gần' if old[oid][det]['A_chua_moc'] else 'E-xa'
            flags={**{f'N1/{k}':None for k in (1.5,2.,3.)},
                   **{f'{n}/{k}':None for n in ('N2','N3') for k in (5,10,20)},'N4':None,'B1':None,
                   **{f'{n}/{k}':None for n in ('B2','B3') for k in (2,5,10)},
                   **{f'B4/w{w}/k{k}':None for w in (15,30,60) for k in (2,3,5)}}
            if det=='bocpd':
                flags['B1']=f['B1_t_hat']['flag']
                i1=read(chain/f'i1/{oid}.json'); i2=read(chain/f'i2/{oid}.json')
                a1=i1['result']['chi_so']; a2=i2['result']['chi_so']; interventions={}
                for tolerance in (2,5,10):
                    decision=intervention_flags(th,a1,a2,tolerance)
                    flags['B2/'+str(tolerance)]=decision['B2']; flags['B3/'+str(tolerance)]=decision['B3']
                    interventions[str(tolerance)]=decision
                for w in ('15','30','60'):
                    for k in ('2','3','5'): flags[f'B4/w{w}/k{k}']=f['B4_t_hat'][w]['flags'][k]
                active=[n for n,v in [('B1',flags['B1']),('B2',flags['B2/5']),('B3',flags['B3/5']),('B4',flags['B4/w30/k3'])] if v is True]
                boc[oid]={'root':lab['root'],'fault':lab['fault'],'cell':lab['cell'],'d':f['d'],
                          'full':f['alarms_indices'],'I1':a1,'I2':a2,'sensitivity':interventions,
                          'cp_counts_Nv':{'full':sum(1<=i<720 for i in f['alarms_indices']),'I1':sum(1<=i<720 for i in a1),'I2':sum(1<=i<720 for i in a2)},
                          'B4_t_hat':f['B4_t_hat'],'source':{'I1':source(chain/f'i1/{oid}.json'),'I2':source(chain/f'i2/{oid}.json')}}
                fp=OUT/f'features-no-label/bocpd/{oid}.json'
            else:
                for n in ('N1','N2','N3'):
                    flags.update({n+'/'+k:v for k,v in f[n].items()})
                flags['N4']=f['N4']; active=[n for n,v in [('N1',flags['N1/2.0']),('N2',flags['N2/10']),('N3',flags['N3/10']),('N4',flags['N4'])] if v]
                ns.setdefault(oid,{})[det]=f
                location[oid]['nsigma'][det]=locate(f,lab['root'])
                fp=OUT/f'features-no-label/nsigma/{oid}--{det}.json'
            rows.append({'opaque_id':oid,'detector':det,'root':lab['root'],'fault':lab['fault'],'cell':lab['cell'],
                         't_hat_index':th,'t_hat_plus_index':plus,'first_group':group,'Miss':plus is None,
                         'delay_seconds':plus-720 if plus is not None else None,
                         'delay_interpretation':'Độ lệch vị trí điểm đổi hồi cứu' if det=='bocpd' else 'Đặt cạnh r_obs Nv; không tự coi là thời gian phát hiện',
                         'false_alarms_Nv_T025':ph[det]['ca'][oid].get('bao_dong_sai'),
                         'r_obs_Nv':None if det=='bocpd' else f['r_obs'],
                         'd':f['d'],'flags_flat':flags,'primary_flags':active,'D0':not active,
                         'feature_source':source(fp),
                         'source_pointers':{'alarms':f'results/T-025/bao-dong.json#/bo_phat_hien/{det}/{oid}',
                                            'first_group':f'results/T-025/cham/phan-tich-b.json#/theo_ca/{oid}/{det}/A_chua_moc',
                                            'false_alarms':f'results/T-025/phat-hien.json#/bo_phat_hien/{det}/ca/{oid}/bao_dong_sai',
                                            'labels':f'results/T-022/nhan-dev.json#/cases/{list(labs).index(oid)}',
                                            'B2_B3':f'results/T-029/bocpd-can-thiep.json#/cases/{oid}/sensitivity' if det=='bocpd' else 'N/A: not BOCPD'}})
    put(OUT/'theo-ca.json',{'rows':rows,'row_count':len(rows),'per_detector':{det:{'all':summarize([r for r in rows if r['detector']==det],'detector'),**{k:summarize([r for r in rows if r['detector']==det],k) for k in ('cell','root','fault')}} for det in bd},'features_frozen':source(run/'features-frozen.json')})
    path=OUT/'theo-ca.csv'; assert not path.exists()
    with path.open('w',encoding='utf-8-sig',newline='') as handle:
        fields=[k for k in rows[0] if k not in ('flags_flat','primary_flags','feature_source','source_pointers')]+['flags_flat','primary_flags','feature_source','source_pointers']
        writer=csv.DictWriter(handle,fieldnames=fields); writer.writeheader()
        for r in rows: writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()})
    log('Ghi theo-ca.csv90dòng.')
    put(OUT/'n-sigma-cot.json',{'cases':ns,'no_causal_claim':True})
    put(OUT/'bocpd-can-thiep.json',{'cases':boc,'B5_by_cell':{cell:[{'opaque_id':oid,'d':r['d'],'cp_counts_Nv':r['cp_counts_Nv']} for oid,r in boc.items() if r['cell']==cell] for cell in sorted({r['cell'] for r in boc.values()})},
                                  'intervention_limit':'I1 excludes only indices720+, still preprocesses full prefix. B2=False does not prove no look-ahead. I2 addresses pre-injection false alarms only.'})
    put(OUT/'dinh-vi.json',{'cases':location,'interpretation':'Temporal order is not causality; BOCPD heuristic is not detector output. Uniform baseline shuffles service identities over fixed tie blocks.'})
    schema={}
    for det in ('bocpd','nsigma','nsigma_doi_chung'):
        columns={oid:set(bd[det][oid]['detector_columns']) for oid in labs}; union=sorted(set.union(*columns.values()))
        incidence=[]
        for c in union:
            byroot={root:{'present':sum(c in columns[o] for o in labs if labs[o]['root']==root),'n':sum(labs[o]['root']==root for o in labs)} for root in sorted({r['root'] for r in labs.values()})}
            deterministic=all(x['present'] in (0,x['n']) for x in byroot.values())
            varies=len({x['present']>0 for x in byroot.values()})>1
            incidence.append({'column':c,'by_root':byroot,'perfect_binary_root_partition':deterministic and varies,
                              'present_roots':[k for k,v in byroot.items() if v['present']==v['n']],
                              'absent_roots':[k for k,v in byroot.items() if v['present']==0]})
        audit=ph[det]['audit_cot']['ca']
        assert all(set(audit[o]['vang'])==set(union)-columns[o] and audit[o]['so_cot']==len(columns[o]) for o in labs)
        cases={o:{**{k:labs[o][k] for k in ('root','fault','cell')},'column_count':len(columns[o]),'d':next(r['d'] for r in rows if r['opaque_id']==o and r['detector']==det),'absent':audit[o]['vang']} for o in labs}
        by={}
        for field in ('root','fault','cell'):
            groups=defaultdict(list)
            for o,r in cases.items(): groups[r[field]].append(o)
            by[field]={g:{'n':len(ids),'case_ids':ids,'column_counts':[cases[o]['column_count'] for o in ids],
                          'd':[cases[o]['d'] for o in ids],'absent_column_counts':{c:sum(c not in columns[o] for o in ids) for c in union}} for g,ids in sorted(groups.items())}
        schema[det]={'cases':cases,'by_group':by,'presence_by_column':incidence,
                     'perfect_partition_columns':[r['column'] for r in incidence if r['perfect_binary_root_partition']],
                     'meaning':'Binary presence separates root subsets only; it need not uniquely identify every root. Not fed to any method.'}
    proxy={}
    for o in labs:
        p=OUT/f'runs/proxy-002/{o}.json'; r=read(p)
        r['source']={**r['source'],'labels':f'results/T-022/nhan-dev.json#/cases/{list(labs).index(o)}','proxy_record':source(p)}
        proxy[o]=r
    put(OUT/'nhan-proxy-va-schema.json',{'P1':{'cases':proxy,'source_duration':read(OUT/'runs/proxy-001/sources-002.json'),
                                             'missing_rule':'Minh approved: N/A if no observation in Nv or minute; eligible-column denominator with coverage; zero eligible => N/A.',
                                             'duration_D':None,'rescore_performed':False,'verification':source(OUT/'runs/proxy-002/verification.json')},'P2':schema})
    put(run/'V7.json',v7(rows,bf))
    from verify_flags_independent import check
    checks=check(rows); put(run/'V5.json',checks)
    assert checks['status']=='PASS','V5 mismatch; preserve outputs, report, do not silently fix'
    put(run/'manifest.json',{'status':'PASS','rows':len(rows),'script_sha256':sha(__file__),
                            'started':STARTED,'completed':datetime.now().astimezone().isoformat(),'wall_seconds':time.monotonic()-TIMER,
                            'dependencies':{p.name:sha(p) for p in chain.glob('*.json')},
                            'inputs':{p:sha(ROOT/p) for p in ['results/T-022/nhan-dev.json','results/T-022/mappings/universe-re2tt-dev.json','results/T-025/bao-dong.json','results/T-025/phat-hien.json','results/T-025/cham/phan-tich-b.json','results/T-029/runs/nsigma-002/manifest.json','results/T-029/runs/bocpd-features-001/manifest.json','results/T-029/runs/proxy-002/manifest.json']},
                            'label_free_features':source(run/'features-frozen.json'),
                            'outputs':{p.name:sha(p) for p in OUT.glob('*.json')}})
    log('Bước5 A/N/B/E/P2/V5/V7PASS; G chạyriêngsauI3. Khôngviếtkếtluậnkhibáocáochưađượckiểm.')
    print(json.dumps({'status':'PASS','rows':len(rows),'V5':checks['mismatch_count']}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--ec2',required=True,type=Path)
    args=parser.parse_args()
    try: main(args.ec2.resolve())
    except BaseException as e:
        run=OUT/'runs/step5-001'
        if run.exists() and not (run/'manifest.json').exists():
            put(run/'manifest.json',{'status':'STOP','started':STARTED,'completed':datetime.now().astimezone().isoformat(),
                                    'wall_seconds':time.monotonic()-TIMER,'script_sha256':sha(__file__),
                                    'error_type':type(e).__name__,'error':str(e)})
        log('DỪNG bước5/phụthuộc: '+type(e).__name__+': '+str(e)+'; giữmọioutput, khôngtựđổiSPEC.'); raise
