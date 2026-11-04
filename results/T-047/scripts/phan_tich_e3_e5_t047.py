"""Người làm phân tích E3/E5 từ chuỗi đã trích; không chạy lại M1 hoặc chọn thiết kế."""
import collections
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT/'src'), str(ROOT/'results/T-047/scripts')]
import adapter_t047 as ad
from m1_danh_gia import pha2
import co_che_t047 as mech

OUT = ad.OUT/'runs/c1-method-analysis-e3-e5-001'
BASE = ad.OUT/'runs/b5-c1-co-che-001'
PAIRS = ('E1+E2|E1+E2+E3', 'E1+E2|E1+E2+E5', 'E1|E1+E5', 'E2|E2+E5')


def read(path):
    return pha2.giai_ma_json(json.loads(Path(path).read_text(encoding='utf-8')))


def rank_map(s):
    return {e: dict(key=b['key'], block=i) for i,b in enumerate(s['blocks']) for g in b['groups'] for e in g}


def sig(s):
    return {ma: {k:v for k,v in x['value'].items() if k!='F_I'} for ma,x in s['channels'].items()}


def native_hash(s):
    source=s['source']; p=ROOT/source['file']
    # Parent/source was checked before extraction. Record the immutable pointer/hash;
    # snapshot hashing below also fixes exactly what was read for interpretation.
    if not source.get('sha256') or not p.is_file(): raise ValueError('native pointer/hash thiếu')
    return source


def case_facts(off,on):
    label=on['label']; root=label['root']
    a,b=off['rank']['P'],on['rank']['P']
    da,db=rank_map(off),rank_map(on)
    changed_entities=[e for e in sorted(set(off['tang'])|set(on['tang']))
                      if any((off[f] or {}).get(e)!=(on[f] or {}).get(e) for f in ('tang','K_raw','K_I'))]
    new_channels=[x['value'] for ma,x in on['channels'].items() if ma not in off['channels']]
    removed_channels=[x['value'] for ma,x in off['channels'].items() if ma not in on['channels']]
    root_removed=[x['value'] for ma,x in on['channels'].items() if x['value']['thuc_the']==root
                  and x['value'].get('F_I')==0 and off['channels'].get(ma,{}).get('value',{}).get('F_I')==1]
    inherited=[x for x in on['inherited_by'] if x['thuc_the'] in changed_entities]
    before_root=set(mech.before_root(off['blocks'],root)); after_root=set(mech.before_root(on['blocks'],root))
    rivals=after_root-before_root
    rival_chains={}
    for e in sorted(rivals):
        channels=[x['value'] for x in on['channels'].values() if x['value']['thuc_the']==e]
        units={k['don_vi']:on['units'].get(k['don_vi']) or on['worlds']['P']['units'].get(k['don_vi']) for k in channels}
        k0=da.get(root,{}).get('key'); kr=db.get(root,{}).get('key'); ke=db.get(e,{}).get('key')
        first=next((i for i,(x,y) in enumerate(zip(ke,kr)) if x!=y),None) if ke is not None and kr is not None else None
        rival_chains[e]=dict(new_key=ke,root_new_key=kr,root_old_key=k0,first_key_difference=first,
            key_fields=['tier','max_s','max_m','channel_count','sum_s'],channels=channels,units=units,
            new_channel_count=sum(k['thuc_the']==e for k in new_channels),
            drain_templates=[x for x in ((on.get('thong_ke_log') or {}).get('cap_drain') or []) if x['thuc_the']==e],
            unmatched_A_count=((on.get('thong_ke_log') or {}).get('mau_moi') or {}).get(e))
    matching=mech.signal_signature(off,label)
    return dict(label=label,delta_RR=b['RR']-a['RR'],RR_before=a['RR'],RR_after=b['RR'],
        expected_rank_before=a['expected_rank'],expected_rank_after=b['expected_rank'],
        hit1_before=a['hit1'],hit1_after=b['hit1'],M5_before=a['M5'],M5_after=b['M5'],
        coverage_same=off['coverage']==on['coverage'],window_same=off['window']==on['window'],
        G_N_same=off['G_N']==on['G_N'],graph_same=off['canh']==on['canh'],
        pv_units_same=off['units']==on['units'],counted_units_same=off['worlds']['P']['units']==on['worlds']['P']['units'],
        raw_channels_same_ignoring_FI=sig(off)==sig(on),changed_entities=changed_entities,
        root_channels_reclassified=root_removed,inherited_by=inherited,
        added_channels=new_channels,removed_channels=removed_channels,
        rivals_newly_before_root=rival_chains,condition=matching,
        root_keys={f:dict(before=off[f].get(root),after=on[f].get(root)) for f in ('tang','K_I','K_raw')},
        source=dict(off=native_hash(off),on=native_hash(on)))


def main():
    # The caller preflight checked both complete phase1 hashes and LOG before labels.
    preflight=read(OUT/'preflight.json')
    preliminary=read(OUT/'pairs-preliminary.json')
    index_path=BASE/'co-che-khoi-k.json'
    if index_path.is_file():
        index=read(index_path)
        if index['sources']['T047']['hash_pha1']!={k:v['sha256'] for k,v in preflight['verified'].items()}:
            raise ValueError('index cơ chế khác hai hash đã kiểm')
    else:
        # Chỉ các snapshot hoàn tất; không cần chờ extractor lặp mọi chain.
        index={'selected_pairs':{}}
        for key in PAIRS:
            off,on=('K-'+name for name in key.split('|'))
            cases={}
            for file in sorted((BASE/'native/T047/that'/off).glob('*.json')):
                oid=file.stem
                native={name:(BASE/'native'/version/'that'/cid/(oid+'.json')).relative_to(ROOT).as_posix()
                        for name,version,cid in [('old_off','T045',off),('old_on','T045',on),
                                                 ('new_off','T047',off),('new_on','T047',on)]}
                snaps={name:read(ROOT/path) for name,path in native.items()}
                group=mech.group_case(**snaps)
                condition=mech.signal_signature(snaps['new_off'],snaps['new_off']['label'])
                pair_file=OUT/'input-pairs'/key.replace('|','__')/(oid+'.json')
                ad.ghi(pair_file,dict(native=native,group=group))
                cases[oid]=dict(file=pair_file.relative_to(ROOT).as_posix(),group=group,condition=condition)
            if len(cases)!=52: raise ValueError('snapshot chưa đủ52; không đọc ca đang ghi')
            index['selected_pairs'][key]=dict(cases=cases)
    results={}; all_sources={}
    for key in PAIRS:
        entry=index['selected_pairs'][key]
        rows={}; counts=collections.Counter(); dataset={}
        for oid,row in sorted(entry['cases'].items()):
            pair=read(ROOT/row['file'])
            snaps={name:read(ROOT/path) for name,path in pair['native'].items()}
            current=case_facts(snaps['new_off'],snaps['new_on'])
            previous=case_facts(snaps['old_off'],snaps['old_on'])
            for path in pair['native'].values():
                all_sources[path]=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
            d=current['delta_RR']; effect='tut' if d<0 else 'len' if d>0 else 'khong_doi'
            counts[effect]+=1
            ds=current['label']['dataset']; ds_counts=dataset.setdefault(ds,collections.Counter())
            ds_counts[effect]+=1
            ds_counts['delta_RR_sum']+=d
            counts['root_FI_reclassified']+=bool(current['root_channels_reclassified'])
            counts['new_M5']+=current['M5_after'] and not current['M5_before']
            counts['removed_M5']+=current['M5_before'] and not current['M5_after']
            counts['raw_changed']+=not current['raw_channels_same_ignoring_FI']
            counts['coverage_changed']+=not current['coverage_same']
            counts['pv_changed']+=not current['pv_units_same']
            counts['counted_changed']+=not current['counted_units_same']
            if current['hit1_before']==1 and current['hit1_after']<1: counts['UV6_hong']+=1
            if ds=='Nezha-OB' and current['label']['loai_loi'] in ('return','exception') and current['hit1_before']<1 and current['hit1_after']==1: counts['UV6_sua']+=1
            correct=[o for o,r in entry['cases'].items() if o!=oid and r['group']['correctness']=='dung'
                     and r['condition']==row['condition']]
            # Preserve matching failure rather than silently drop a difficult group.
            current['counterparts_same_condition_correct']=correct
            current['counterpart_status']='AVAILABLE' if correct else 'OPEN_NO_EXACT_CONDITION_CORRECT'
            target=OUT/'pairs'/key.replace('|','__')/(oid+'.json')
            ad.ghi(target,dict(current=current,previous=previous,group=pair['group'],
                              mechanism_chain_source=row['file'],native_snapshots=pair['native'],
                              claims='FACTS_ON_NATIVE; interpretation in pair summary, not causal validation'))
            rows[oid]=dict(file=target.relative_to(ROOT).as_posix(),dataset=ds,root=current['label']['root'],
                loai_loi=current['label']['loai_loi'],effect=effect,delta_RR=d,
                hit1_before=current['hit1_before'],hit1_after=current['hit1_after'],
                root_reclassified=bool(current['root_channels_reclassified']),
                added_new_pattern_rivals=sum(any('mau_moi' in c['don_vi'] for c in r['channels'])
                                             for r in current['rivals_newly_before_root'].values()),
                counterparts=correct)
        for ds,c in dataset.items():
            c['dMRR']=c['delta_RR_sum']/sum(x['dataset']==ds for x in rows.values())
        main=preliminary[key]['new']['theo_the_gioi']['P']
        old=preliminary[key]['old']['theo_the_gioi']['P']
        results[key]=dict(old_verdict=old['ket_cuc'],new_verdict=main['ket_cuc'],
            old_reasons=old['ly_do_hai_rieng'],new_reasons=main['ly_do_hai_rieng'],
            old_dMRR=old['dMRR'],new_dMRR=main['dMRR'],counts=dict(counts),
            by_dataset={ds:dict(x) for ds,x in dataset.items()},
            N1_new={k:v for k,v in main['moc_gia'].items() if k!='cua_so'},cases=rows,
            interpretation_status='NEEDS_HUMAN_READ',OPEN=['Chưa có suy luận cơ chế trong file tự động; người làm đọc chuỗi và đối chứng.'])
        print(json.dumps(pha2.ma_hoa_json({'pair':key,'counts':dict(counts),'by_dataset':results[key]['by_dataset']}),ensure_ascii=False),flush=True)
    ad.ghi(OUT/'facts-all-pairs.json',dict(schema='T047-E3-E5-method-facts-v1',pairs=results,
        sources=all_sources,index_source=str(index_path.relative_to(ROOT)) if index_path.is_file() else None,
        index_sha256=hashlib.sha256(index_path.read_bytes()).hexdigest() if index_path.is_file() else None,
        snapshot_fallback_used=not index_path.is_file(),
        formal_review=False,claims='FACTS; no design selection or causal attribution'))


def raw_e3_cases(oids, output_folder='raw-e3', summary_name='raw-e3-summary.json'):
    """Rebuild log/Drain/D1 intermediates only; no chain execution or design change."""
    import pyarrow.parquet as pq
    from m1 import adapter, e3, kenh, cong, e4
    from p3 import selector
    from giai_thich_lech_c1 import RawInputs
    raw_control=RawInputs()
    results={}
    for oid in oids:
        native=read(BASE/'native/T047/that/K-E1+E2+E3'/(oid+'.json'))
        t=native['window']['A'][0];lo=native['window']['N'][0];hi=native['window']['A'][1]
        ds=raw_control.dataset(oid)
        if ds=='RE2-TT':
            files=selector.chon_ca(raw_control.re,oid,ROOT,tep=['logs.parquet'])
            path=Path(files['logs.parquet'])
            frame=pq.read_table(path).to_pandas()
            logs=[dict(moc=int(float(mc)*10**9),thuc_the=str(e),noi_dung='' if adapter._rong(msg) else str(msg),severity_raw=None)
                for mc,e,msg in frame[['timestamp','container_name','message']].itertuples(index=False,name=None)
                if lo<=float(mc)*10**9<hi]
            rule={'kieu':'tu_khoa','tu_khoa':adapter.TU_KHOA_RE2}
            provenance=[dict(file=path.relative_to(ROOT).as_posix(),sha256=selector.sha256_file(path))]
        else:
            case=adapter.ca_nezha(raw_control.nz,oid,ROOT,raw_control.contract)
            logs=[dict(moc=int(row['timestamp']),thuc_the=row['entity'],noi_dung=row['message'],severity_raw=row.get('severity_raw'))
                for row in case['logs'] if lo<=row['timestamp']<hi]
            rule=case['params_ca']['ho_so_nguon']['quy_tac_log']
            provenance=[dict(file=x['path'],sha256=x['sha256']) for x in raw_control.nz[oid]['files'].values()]
        params=read(ad.OUT/'runs/b3-k-c1-that-001/cases'/oid/'phase1/tham-so.json')
        cfg=next(c for c in params['configs'] if c['config_id']=='K-E1+E2+E3')
        N=[x for x in logs if x['moc']<t];A=[x for x in logs if x['moc']>=t]
        learned=e3.hoc_va_dem(N,A,cfg['tham_so_E3'],rule)
        # Kiểm lớp thật của những dòng A không khớp; không suy từ tên mau_moi.
        from drain3.drain import Drain
        ts3=cfg['tham_so_E3']
        drain=Drain(depth=int(ts3['do_sau']),sim_th=float(ts3['sim_th']),max_children=100,
                    max_clusters=None,extra_delimiters=(),parametrize_numeric_tokens=True)
        known={}
        for row in sorted(N,key=lambda x:(x['moc'],x['thuc_the'],x['noi_dung'])):
            cluster,_=drain.add_log_message(e3.che_token(row['noi_dung']))
            known.setdefault(row['thuc_the'],set()).add(cluster.cluster_id)
        unmatched=collections.Counter();unmatched_examples={}
        for row in sorted(A,key=lambda x:(x['moc'],x['thuc_the'],x['noi_dung'])):
            tokens=drain.get_content_as_tokens(e3.che_token(row['noi_dung']))
            cluster=e3._khop(drain,tokens,known.get(row['thuc_the'],set()),ts3['khop'],ts3['sim_th'])
            if cluster is None:
                cl=e3._lop_dong(row,rule);unmatched[(row['thuc_the'],cl)]+=1
                bucket=unmatched_examples.setdefault(row['thuc_the'],[])
                if len(bucket)<3:bucket.append(dict(moc=row['moc'],text=row['noi_dung'],
                    masked=e3.che_token(row['noi_dung']),severity=row['severity_raw'],classified=cl))
        if any(sum(n for (entity,cl),n in unmatched.items() if entity==e)!=n for e,n in learned['mau_moi'].items()):
            raise ValueError('unmatched replay khác hoc_va_dem')
        rebuilt=[dict({'thuc_the':e,'mau':cid,'khuon':learned['mau'].get(cid)},
                **{k:v[k] for k in ('lop','n_N','n_A','phieu_loi','phieu_khong','unknown_N','unknown_A','loi_xac_dinh_N','loi_xac_dinh_A')})
                for (e,cid),v in sorted(learned['cap'].items())]
        expected=(native['thong_ke_log'] or {})['cap_drain']
        if rebuilt!=expected: raise ValueError('raw Drain mismatch '+oid)
        facts=read(OUT/'pairs/E1+E2__E1+E2+E3'/(oid+'.json'))['current']
        entities={facts['label']['root']}|set(facts['rivals_newly_before_root'])
        events={f'log|{e}|mau:{cid}':value for (e,cid),value in learned['moc_N'].items()}
        h0=min((x['moc'] for x in logs),default=None)
        T=native['coverage']['log']['the_gioi']['P']
        unit_rows={};errors=[]
        fields=('n_N','n_A','T_N','T_A','trang_thai','p_len','p_xuong','e_len','e_xuong','F_raw_len','F_raw_xuong')
        for unit in kenh.don_vi_mau_drain(learned):
            if unit['thuc_the'] not in entities:continue
            ma=f"log|{unit['thuc_the']}|{unit['ten']}"
            phi=cong.he_so_phan_tan(events[ma],h0,t) if ma in events else None
            result=e4.cham_dem(unit['n_N'],unit['n_A'],T[0],T[1],cfg['tham_so_E4'],huong_cham=tuple(unit['huong_cham']),phi_d=phi)
            wanted=native['worlds']['P']['units'][ma]['value']
            mismatch={k:dict(raw=result.get(k),native=wanted.get(k)) for k in fields if result.get(k)!=wanted.get(k)}
            if result['nhan']!=wanted['loai_thay_doi']:mismatch['nhan']=dict(raw=result['nhan'],native=wanted['loai_thay_doi'])
            if mismatch:errors.append(ma)
            unit_rows[ma]=dict(input=unit,T=T,phi_D1=phi,events_N=events.get(ma),h0=h0,
                recomputed={k:result.get(k) for k in (*fields,'nhan','e_len_tho','e_xuong_tho')},
                native=wanted,mismatch=mismatch,gate_branch='direct_NEW_OP_STOPPED' if result['nhan'] in ('NEW_OP','STOPPED') else
                'D1' if phi is not None else 'binomial',
                source_pointer=native['worlds']['P']['units'][ma]['pointer'])
        entity_facts={}
        for e in sorted(entities):
            entity_facts[e]=dict(N_count=sum(x['thuc_the']==e for x in N),A_count=sum(x['thuc_the']==e for x in A),
                N_classes=dict(collections.Counter(e3._lop_dong(x,rule) for x in N if x['thuc_the']==e)),
                A_classes=dict(collections.Counter(e3._lop_dong(x,rule) for x in A if x['thuc_the']==e)),
                unmatched_A=learned['mau_moi'].get(e,0),
                unmatched_A_classes={cl:n for (entity,cl),n in unmatched.items() if entity==e},
                unmatched_A_examples=unmatched_examples.get(e,[]),
                A_examples=[dict(moc=x['moc'],text=x['noi_dung'],masked=e3.che_token(x['noi_dung']),severity=x['severity_raw'])
                            for x in A if x['thuc_the']==e][:3])
        out=dict(opaque_id=oid,dataset=ds,source=provenance,raw_controls=raw_control.controls,
                 log_window=[lo,t,hi],N_count=len(N),A_count=len(A),Drain_matches_native=True,
                 units=unit_rows,entities=entity_facts,mismatching_units=errors,
                 interpretation='Raw/template/cổng tái lập; chưa xác nhận dòng không khớp là nhiễu hay biểu hiện lỗi.',
                 status='OPEN_API_MISMATCH' if errors else 'RAW_TO_UNIT_REPRODUCED')
        target=OUT/output_folder/(oid+'.json');ad.ghi(target,out)
        results[oid]=dict(file=target.relative_to(ROOT).as_posix(),status=out['status'],entities=list(entities),
            units=len(unit_rows),direct_flags=sum(x['gate_branch']=='direct_NEW_OP_STOPPED' for x in unit_rows.values()))
        print(json.dumps(results[oid]),flush=True)
    ad.ghi(OUT/summary_name,results)


if __name__=='__main__': main()
